module SPOT1P64_CACHE_MOD
  implicit none
  private

  type, public :: SPOT1P64_MODE_PLAN
    logical :: ready=.false.
    integer :: nstate=0
    integer :: nblock=0
    double precision, allocatable :: lower(:,:,:)
    double precision, allocatable :: factor(:,:,:)
    double precision, allocatable :: pivot_value(:,:)
    double precision, allocatable :: cprime(:,:,:)
    integer, allocatable :: pivot(:,:)
  end type SPOT1P64_MODE_PLAN

  type, public :: SPOT1P64_GROUP_PLAN
    type(SPOT1P64_MODE_PLAN), allocatable :: mode(:)
  end type SPOT1P64_GROUP_PLAN

  type(SPOT1P64_GROUP_PLAN), allocatable, save, public :: SPOT1P64_PLAN(:)
  logical, save :: cache_enabled=.false.
  integer, save :: factorized_blocks=0
  integer, save :: reused_blocks=0

  public :: SPOT1P64_CACHE_BEGIN,SPOT1P64_CACHE_CLEAR
  public :: SPOT1P64_CACHE_PREPARE,SPOT1P64_CACHE_NOTE_BUILD
  public :: SPOT1P64_CACHE_NOTE_REUSE,SPOT1P64_CACHE_STATS
  public :: SPOT1P64_FACTOR64,SPOT1P64_SOLVE64

contains

  subroutine SPOT1P64_CACHE_BEGIN(ngroup,enable)
    integer, intent(in) :: ngroup
    logical, intent(in) :: enable
    call SPOT1P64_CACHE_CLEAR()
    if (.not.enable) return
    if (ngroup <= 0) call XABORT('SPOT1P64 CACHE: INVALID GROUP COUNT.')
    allocate(SPOT1P64_PLAN(ngroup))
    cache_enabled=.true.
  end subroutine SPOT1P64_CACHE_BEGIN

  subroutine SPOT1P64_CACHE_CLEAR()
    if (allocated(SPOT1P64_PLAN)) deallocate(SPOT1P64_PLAN)
    cache_enabled=.false.
    factorized_blocks=0
    reused_blocks=0
  end subroutine SPOT1P64_CACHE_CLEAR

  subroutine SPOT1P64_CACHE_PREPARE(igroup,nmode,active)
    integer, intent(in) :: igroup,nmode
    logical, intent(out) :: active
    active=.false.
    if (.not.cache_enabled) return
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 CACHE: MISSING FLU LIFECYCLE.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 CACHE: INVALID ENERGY GROUP.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) then
      allocate(SPOT1P64_PLAN(igroup)%mode(nmode))
    else if (size(SPOT1P64_PLAN(igroup)%mode) /= nmode) then
      call XABORT('SPOT1P64 CACHE: MODE COUNT CHANGED INSIDE FLU.')
    endif
    active=.true.
  end subroutine SPOT1P64_CACHE_PREPARE

  subroutine SPOT1P64_CACHE_NOTE_BUILD(nblock)
    integer, intent(in) :: nblock
    factorized_blocks=factorized_blocks+nblock
  end subroutine SPOT1P64_CACHE_NOTE_BUILD

  subroutine SPOT1P64_CACHE_NOTE_REUSE(nblock)
    integer, intent(in) :: nblock
    reused_blocks=reused_blocks+nblock
  end subroutine SPOT1P64_CACHE_NOTE_REUSE

  subroutine SPOT1P64_CACHE_STATS(nfactor,nreuse)
    integer, intent(out) :: nfactor,nreuse
    nfactor=factorized_blocks
    nreuse=reused_blocks
  end subroutine SPOT1P64_CACHE_STATS

  ! Split ALSBD's pivoted elimination from its right-hand-side work while
  ! preserving its pivot rule and each finite column's scalar arithmetic
  ! order.  The factor is valid only for exact reuse of the same matrix.
  subroutine SPOT1P64_FACTOR64(matrix,pivot,pivot_value,info)
    double precision, intent(inout) :: matrix(:,:)
    integer, intent(out) :: pivot(:),info
    double precision, intent(out) :: pivot_value(:)
    integer :: n,jcol,i,j,pivot_row
    double precision :: test,per

    n=size(matrix,1)
    if (size(matrix,2) /= n .or. size(pivot) /= n .or. &
        size(pivot_value) /= n) &
      call XABORT('SPOT1P64 FACTOR: INVALID DIMENSIONS.')
    info=0
    pivot=0
    pivot_value=0.0d0
    if (n == 1) then
      pivot(1)=1
      pivot_value(1)=matrix(1,1)
      if (pivot_value(1) == 0.0d0) info=1
      return
    endif

    do jcol=1,n-1
      test=0.0d0
      pivot_row=0
      do i=jcol,n
        if (abs(matrix(i,jcol)) <= test) cycle
        test=abs(matrix(i,jcol))
        pivot_row=i
      enddo
      if (test == 0.0d0) then
        info=1
        return
      endif
      pivot(jcol)=pivot_row
      pivot_value(jcol)=matrix(pivot_row,jcol)
      matrix(pivot_row,jcol)=matrix(jcol,jcol)
      do j=jcol+1,n
        per=matrix(pivot_row,j)/pivot_value(jcol)
        matrix(pivot_row,j)=matrix(jcol,j)
        matrix(jcol,j)=per
        do i=jcol+1,n
          matrix(i,j)=matrix(i,j)-matrix(i,jcol)*per
        enddo
      enddo
    enddo
    pivot(n)=n
    pivot_value(n)=matrix(n,n)
    if (pivot_value(n) == 0.0d0) info=1
  end subroutine SPOT1P64_FACTOR64

  subroutine SPOT1P64_SOLVE64(factor,pivot,pivot_value,rhs,info)
    double precision, intent(in) :: factor(:,:),pivot_value(:)
    integer, intent(in) :: pivot(:)
    double precision, intent(inout) :: rhs(:,:)
    integer, intent(out) :: info
    integer :: n,nrhs,jcol,j,i,k,pivot_row,iback
    double precision :: per

    n=size(factor,1)
    nrhs=size(rhs,2)
    if (size(factor,2) /= n .or. size(rhs,1) /= n .or. &
        size(pivot) /= n .or. size(pivot_value) /= n) &
      call XABORT('SPOT1P64 SOLVE: INVALID DIMENSIONS.')
    info=0
    if (n == 1) then
      if (pivot_value(1) == 0.0d0) then
        info=1
        return
      endif
      do j=1,nrhs
        rhs(1,j)=rhs(1,j)/pivot_value(1)
      enddo
      return
    endif

    do jcol=1,n-1
      pivot_row=pivot(jcol)
      if (pivot_row < jcol .or. pivot_row > n .or. &
          pivot_value(jcol) == 0.0d0) then
        info=1
        return
      endif
      do j=1,nrhs
        per=rhs(pivot_row,j)/pivot_value(jcol)
        rhs(pivot_row,j)=rhs(jcol,j)
        rhs(jcol,j)=per
        do i=jcol+1,n
          rhs(i,j)=rhs(i,j)-factor(i,jcol)*per
        enddo
      enddo
    enddo
    if (pivot_value(n) == 0.0d0) then
      info=1
      return
    endif
    do j=1,nrhs
      rhs(n,j)=rhs(n,j)/pivot_value(n)
    enddo
    do iback=2,n
      i=n-iback+1
      do j=1,nrhs
        per=rhs(i,j)
        do k=i+1,n
          per=per-factor(i,k)*rhs(k,j)
        enddo
        rhs(i,j)=per
      enddo
    enddo
  end subroutine SPOT1P64_SOLVE64

end module SPOT1P64_CACHE_MOD

! Independent reduced-rank exact factor cache. No SPOT-PHYS property is set.
module SPOT1P64_R1_GENERIC_CACHE_MOD
  use, intrinsic :: iso_fortran_env, only : int32,int64
  implicit none
  private
  type, public :: SPOT1P64_R1_GENERIC_PLAN
    logical :: ready=.false.,compressed=.false.
    integer :: nstate=0,nblock=0
    integer(int64) :: charged_bytes=0_int64
    integer(int32),allocatable :: key_i(:),key_r32(:)
    integer(int64),allocatable :: key_r64(:)
    integer,allocatable :: positive_row(:),pivot(:,:)
    double precision,allocatable :: lower_positive(:,:,:),lower_full(:,:,:)
    double precision,allocatable :: factor(:,:,:),pivot_value(:,:),cprime(:,:,:)
  end type
  type(SPOT1P64_R1_GENERIC_PLAN),allocatable,save,public :: SPOT1P64_R1_PLAN(:)
  integer(int64),save :: used_bytes=0_int64,maximum_bytes=0_int64
  integer,save :: built_blocks=0,reused_blocks=0,key_misses=0,budget_fallbacks=0
  logical,save :: enabled=.false.
  public :: SPOT1P64_R1_CACHE_BEGIN,SPOT1P64_R1_CACHE_CLEAR,SPOT1P64_R1_CACHE_STATS
  public :: SPOT1P64_R1_TRY,SPOT1P64_R1_STORE_BEGIN,SPOT1P64_R1_LOWER
  public :: SPOT1P64_R1_NOTE_BUILD,SPOT1P64_R1_NOTE_REUSE
contains
  subroutine SPOT1P64_R1_CACHE_BEGIN(ngroup,byte_limit)
    integer,intent(in) :: ngroup
    integer(int64),intent(in) :: byte_limit
    type(SPOT1P64_R1_GENERIC_PLAN) :: empty
    integer(int64) :: table_bytes
    call SPOT1P64_R1_CACHE_CLEAR()
    if (ngroup<=0.or.byte_limit<=0_int64) return
    table_bytes=int(ngroup,int64)*int(storage_size(empty)/8,int64)
    if (table_bytes>=byte_limit) return
    allocate(SPOT1P64_R1_PLAN(ngroup))
    used_bytes=table_bytes;maximum_bytes=byte_limit;enabled=.true.
  end subroutine
  subroutine SPOT1P64_R1_CACHE_CLEAR()
    if (allocated(SPOT1P64_R1_PLAN)) deallocate(SPOT1P64_R1_PLAN)
    used_bytes=0_int64;maximum_bytes=0_int64;enabled=.false.
    built_blocks=0;reused_blocks=0;key_misses=0;budget_fallbacks=0
  end subroutine
  subroutine release_group(igroup)
    integer,intent(in) :: igroup
    type(SPOT1P64_R1_GENERIC_PLAN) :: empty
    used_bytes=used_bytes-SPOT1P64_R1_PLAN(igroup)%charged_bytes
    SPOT1P64_R1_PLAN(igroup)=empty
  end subroutine
  subroutine SPOT1P64_R1_CACHE_STATS(nbuild,nreuse,nmiss,nfallback,nbytes,nlimit)
    integer,intent(out) :: nbuild,nreuse,nmiss,nfallback
    integer(int64),intent(out) :: nbytes,nlimit
    nbuild=built_blocks;nreuse=reused_blocks;nmiss=key_misses;nfallback=budget_fallbacks
    nbytes=used_bytes;nlimit=maximum_bytes
  end subroutine
  subroutine SPOT1P64_R1_NOTE_BUILD(nblock)
    integer,intent(in) :: nblock
    built_blocks=built_blocks+nblock
  end subroutine
  subroutine SPOT1P64_R1_NOTE_REUSE(nblock)
    integer,intent(in) :: nblock
    reused_blocks=reused_blocks+nblock
  end subroutine

  ! Keys contain the entire actual LHS construction and all its raw operands.
  ! No source_m/qext/old RHS/flux/keff is stored or reused. Integer bit patterns
  ! are compared exactly, including signed zero; no hash or tolerance is used.
  subroutine SPOT1P64_R1_TRY(igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
      lfixup,translation,mat1d,mat,ncode,opposite,vol1d,total,sgas,basis,vol2d,zcode,du,w,pl, &
      radial2d,mass_m,total_m,radial_m,scat_m,mn,dn,left_albedo,right_albedo,candidate,hit)
    integer,intent(in) :: igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct
    logical,intent(in) :: lfixup,translation
    integer,intent(in) :: mat1d(nfloor),mat(nfloor,nreg2d),ncode(2),opposite(npq)
    real,intent(in) :: vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct),basis(nreg2d,nmode)
    real,intent(in) :: vol2d(nreg2d),zcode(2),du(npq),w(npq),pl(nsct,npq)
    double precision,intent(in) :: radial2d(nreg2d,nsnap),mass_m(nmode,nmode)
    double precision,intent(in) :: total_m(nmode,nmode,nfloor),radial_m(nmode,nmode,nfloor)
    double precision,intent(in) :: scat_m(nmode,nmode,nsct,nfloor),mn(npq,nsct),dn(nsct,npq)
    double precision,intent(in) :: left_albedo,right_albedo
    logical,intent(out) :: candidate,hit
    integer(int32),allocatable :: ki(:),kr32(:)
    integer(int64),allocatable :: kr64(:)
    integer(int64) :: bytes
    candidate=.false.;hit=.false.
    if (.not.enabled) return
    ! This separate route is genuine reduced rank one only. The original
    ! full-rank physical cache and translation solver keep their old paths.
    if (nmode/=1.or.nreg2d<=1.or.translation.or.lfixup.or.ielem/=1.or.ischm/=1) return
    if (igroup<1.or.igroup>size(SPOT1P64_R1_PLAN)) call XABORT('R1 EXACT CACHE: INVALID GROUP.')
    ki=[int([igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
       merge(1,0,lfixup),merge(1,0,translation)],int32),int(mat1d,int32), &
       int(reshape(mat,[size(mat)]),int32),int(ncode,int32),int(opposite,int32)]
    kr32=[transfer(vol1d,[0_int32]),transfer(total,[0_int32]),transfer(sgas,[0_int32]), &
       transfer(basis,[0_int32]),transfer(vol2d,[0_int32]),transfer(zcode,[0_int32]), &
       transfer(du,[0_int32]),transfer(w,[0_int32]),transfer(pl,[0_int32])]
    kr64=[transfer(radial2d,[0_int64]),transfer(mass_m,[0_int64]), &
       transfer(total_m,[0_int64]),transfer(radial_m,[0_int64]),transfer(scat_m,[0_int64]), &
       transfer(mn,[0_int64]),transfer(dn,[0_int64]),transfer([left_albedo,right_albedo],[0_int64])]
    associate(plan=>SPOT1P64_R1_PLAN(igroup))
      if (plan%ready) then
        if (size(plan%key_i)==size(ki).and.size(plan%key_r32)==size(kr32).and. &
            size(plan%key_r64)==size(kr64)) then
          if (all(plan%key_i==ki).and.all(plan%key_r32==kr32).and.all(plan%key_r64==kr64)) then
            candidate=.true.;hit=.true.;return
          endif
        endif
      endif
    end associate
    key_misses=key_misses+1
    call release_group(igroup)
    bytes=int(size(ki),int64)*4_int64+int(size(kr32),int64)*4_int64+int(size(kr64),int64)*8_int64
    if (bytes>maximum_bytes-used_bytes) then
      budget_fallbacks=budget_fallbacks+1;return
    endif
    associate(plan=>SPOT1P64_R1_PLAN(igroup))
      call move_alloc(ki,plan%key_i);call move_alloc(kr32,plan%key_r32);call move_alloc(kr64,plan%key_r64)
      plan%charged_bytes=bytes
    end associate
    used_bytes=used_bytes+bytes;candidate=.true.
  end subroutine

  ! The original construction starts lower at +0. It only writes positive
  ! direction rows. Nevertheless every omitted row is verified by bit value
  ! before compact storage. Any exception uses full dense storage if it fits;
  ! otherwise the current call remains on original uncached ALSBD.
  subroutine SPOT1P64_R1_STORE_BEGIN(igroup,lower,du,store)
    integer,intent(in) :: igroup
    double precision,intent(in) :: lower(:,:,:)
    real,intent(in) :: du(:)
    logical,intent(out) :: store
    integer :: nstate,nblock,npositive,in,j,row
    integer(int64) :: bytes
    logical :: compact
    store=.false.;nstate=size(lower,1);nblock=size(lower,3)
    if (size(lower,2)/=nstate.or.size(du)/=nstate) call XABORT('R1 EXACT CACHE: LOWER SHAPE.')
    npositive=count(du>0.0);compact=.true.
    do in=1,nstate
      if (du(in)>0.0) cycle
      do j=1,nstate
        if (any(transfer(lower(in,j,:),[0_int64])/=0_int64)) compact=.false.
      enddo
    enddo
    bytes=(2_int64*int(nstate,int64)*int(nstate,int64)*int(nblock,int64))*8_int64+ &
      int(nstate,int64)*int(nblock,int64)*(8_int64+int(storage_size(0)/8,int64))
    if (compact) then
      bytes=bytes+int(npositive,int64)*int(nstate,int64)*int(nblock,int64)*8_int64+ &
        int(npositive,int64)*int(storage_size(0)/8,int64)
    else
      bytes=bytes+int(nstate,int64)*int(nstate,int64)*int(nblock,int64)*8_int64
    endif
    if (bytes>maximum_bytes-used_bytes) then
      call release_group(igroup);budget_fallbacks=budget_fallbacks+1;return
    endif
    associate(plan=>SPOT1P64_R1_PLAN(igroup))
      plan%nstate=nstate;plan%nblock=nblock;plan%compressed=compact
      allocate(plan%factor(nstate,nstate,nblock),plan%cprime(nstate,nstate,nblock))
      allocate(plan%pivot(nstate,nblock),plan%pivot_value(nstate,nblock))
      if (compact) then
        allocate(plan%positive_row(npositive),plan%lower_positive(npositive,nstate,nblock))
        row=0
        do in=1,nstate
          if (du(in)<=0.0) cycle
          row=row+1;plan%positive_row(row)=in
          plan%lower_positive(row,:,:)=lower(in,:,:)
        enddo
      else
        allocate(plan%lower_full(nstate,nstate,nblock));plan%lower_full=lower
      endif
      plan%charged_bytes=plan%charged_bytes+bytes
    end associate
    used_bytes=used_bytes+bytes;store=.true.
  end subroutine
  subroutine SPOT1P64_R1_LOWER(igroup,block,dense)
    integer,intent(in) :: igroup,block
    double precision,intent(out) :: dense(:,:)
    integer :: row
    associate(plan=>SPOT1P64_R1_PLAN(igroup))
      if (size(dense,1)/=plan%nstate.or.size(dense,2)/=plan%nstate.or. &
          block<1.or.block>plan%nblock) call XABORT('R1 EXACT CACHE: RESTORED LOWER SHAPE.')
      if (plan%compressed) then
        dense=0.0d0
        do row=1,size(plan%positive_row)
          dense(plan%positive_row(row),:)=plan%lower_positive(row,:,block)
        enddo
      else
        dense=plan%lower_full(:,:,block)
      endif
    end associate
  end subroutine
end module SPOT1P64_R1_GENERIC_CACHE_MOD


!-----------------------------------------------------------------------
!
! Purpose:
!   Solve the coupled one-dimensional SN equations in a radial POD
!   trial space and reconstruct the physical regional flux.
!
! The radial expansion for one energy group is
!
!        psi_i(z,mu) = sum_a B_i^a A_a(z,mu),
!
! where B is any full-rank radial basis.  Material operators, sources,
! and the streaming mass matrix are projected with the same volume inner
! product.  RANK therefore equals
! the number of axial modal unknowns; POD is not an input filter.
!
! This first clean implementation intentionally supports the constant
! diamond spatial approximation only.
!
!-----------------------------------------------------------------------
subroutine SPOT1P64(igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
                  lfixup,mat1d,vol1d,mat,total,sgas,basis,vol2d, &
                  radial2d,ncode,zcode,qext,du,w,pl,flux,cour,xnei)
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use SPOT1P64_CACHE_MOD, only : SPOT1P64_PLAN,SPOT1P64_CACHE_PREPARE, &
    SPOT1P64_CACHE_NOTE_BUILD,SPOT1P64_CACHE_NOTE_REUSE, &
    SPOT1P64_FACTOR64,SPOT1P64_SOLVE64
  use SPOT1P64_R1_GENERIC_CACHE_MOD, only : SPOT1P64_R1_PLAN,SPOT1P64_R1_TRY, &
    SPOT1P64_R1_STORE_BEGIN,SPOT1P64_R1_LOWER,SPOT1P64_R1_NOTE_BUILD,SPOT1P64_R1_NOTE_REUSE
  implicit none
  integer, parameter :: dp=kind(1.0d0)

  integer, intent(in) :: igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode
  integer, intent(in) :: ischm,npq,nsct
  integer, intent(in) :: mat1d(nfloor),mat(nfloor,nreg2d),ncode(2)
  real, intent(in) :: vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct)
  real, intent(in) :: basis(nreg2d,nmode),vol2d(nreg2d),zcode(2)
  double precision, intent(in) :: radial2d(nreg2d,nsnap)
  double precision, intent(in) :: qext(ielem,nsct,nfloor,nreg2d)
  real, intent(in) :: du(npq),w(npq),pl(nsct,npq)
  double precision, intent(out) :: flux(ielem,nsct,nfloor,nreg2d)
  double precision, intent(out) :: cour(nfloor+1,nreg2d),xnei(npq,nreg2d)
  logical, intent(in) :: lfixup

  integer :: i,a,b,n,m,l,ifloor,iface,ibm,isnap,half
  integer :: npositive,nnegative,npair
  double precision :: vtot,wi,scale,albedo_left,albedo_right
  double precision, allocatable :: weight(:),mass_m(:,:),total_m(:,:,:)
  double precision, allocatable :: radial_m(:,:,:)
  double precision, allocatable :: scat_m(:,:,:,:),source_m(:,:,:)
  double precision, allocatable :: mn(:,:),dn(:,:)
  double precision, allocatable :: face(:,:,:),cell(:,:,:)
  double precision, allocatable :: modal_flux(:,:,:),modal_cour(:,:)
  integer, allocatable :: opposite(:)
  logical :: translation,diagonal_basis,mode_separable,use_factor_cache
  logical :: generic_candidate,generic_hit

  if (ielem /= 1 .or. ischm /= 1) &
    call XABORT('SPOT1P: ONLY CONSTANT DIAMOND SPATIAL APPROXIMATION IS SUPPORTED.')
  if (lfixup) &
    call XABORT('SPOT1P: NEGATIVE-FLUX FIXUP IS NOT IMPLEMENTED.')
  if (nmode <= 0 .or. nmode > nreg2d) &
    call XABORT('SPOT1P: INVALID POD MODE COUNT.')
  if (mod(npq,2) /= 0 .or. npq <= 0) &
    call XABORT('SPOT1P: AN EVEN SN ORDER IS REQUIRED.')
  if (any(vol1d <= 0.0) .or. any(vol2d <= 0.0) .or. &
      any(.not.ieee_is_finite(vol1d)) .or. &
      any(.not.ieee_is_finite(vol2d)) .or. &
      any(.not.ieee_is_finite(basis))) &
    call XABORT('SPOT1P: INVALID VOLUME OR BASIS.')
  if (any(.not.ieee_is_finite(total)) .or. &
      any(.not.ieee_is_finite(sgas)) .or. &
      any(.not.ieee_is_finite(radial2d)) .or. &
      any(.not.ieee_is_finite(qext)) .or. &
      any(.not.ieee_is_finite(pl)) .or. &
      any(.not.ieee_is_finite(zcode))) &
    call XABORT('SPOT1P: NON-FINITE OPERATOR OR SOURCE DATA.')
  if (any(.not.ieee_is_finite(du)) .or. &
      any(.not.ieee_is_finite(w)) .or. any(w <= 0.0)) &
    call XABORT('SPOT1P: INVALID SN QUADRATURE DATA.')

  half=npq/2
  npositive=count(du > 0.0)
  nnegative=count(du < 0.0)
  if (npositive /= half .or. nnegative /= half) &
    call XABORT('SPOT1P: INVALID SYMMETRIC SN DIRECTIONS.')
  allocate(opposite(npq))
  opposite=0
  do n=1,npq
    npair=0
    do m=1,npq
      ! Unary negation is exact for a finite stored IEEE real.  Compare
      ! representations so the pairing contains no numerical tolerance.
      if (transfer(du(m),0) == transfer(-du(n),0)) then
        npair=npair+1
        opposite(n)=m
      endif
    enddo
    if (npair /= 1) &
      call XABORT('SPOT1P: SN DIRECTION HAS NO UNIQUE EXACT OPPOSITE.')
  enddo
  do n=1,npq
    if (opposite(opposite(n)) /= n) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT AN INVOLUTION.')
    if (count(opposite == n) /= 1) &
      call XABORT('SPOT1P: SN OPPOSITE MAP IS NOT ONE-TO-ONE.')
    if (transfer(w(opposite(n)),0) /= transfer(w(n),0)) &
      call XABORT('SPOT1P: OPPOSITE SN WEIGHTS DIFFER.')
  enddo
  translation=(ncode(1) == 4 .or. ncode(2) == 4)
  if (translation .and. (ncode(1) /= 4 .or. ncode(2) /= 4)) &
    call XABORT('SPOT1P: TRANSLATION BOUNDARIES MUST BE PAIRED.')
  if (.not.translation) then
    if (.not.(ncode(1) == 1 .or. ncode(1) == 2 .or. ncode(1) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED LEFT BOUNDARY CONDITION.')
    if (.not.(ncode(2) == 1 .or. ncode(2) == 2 .or. ncode(2) == 7)) &
      call XABORT('SPOT1P: UNSUPPORTED RIGHT BOUNDARY CONDITION.')
  endif

  allocate(weight(nreg2d),mass_m(nmode,nmode))
  allocate(total_m(nmode,nmode,nfloor))
  allocate(radial_m(nmode,nmode,nfloor))
  allocate(scat_m(nmode,nmode,nsct,nfloor))
  allocate(source_m(nsct,nfloor,nmode),mn(npq,nsct),dn(nsct,npq))
  vtot=sum(real(vol2d,dp))
  if ((.not.ieee_is_finite(vtot)) .or. vtot <= 0.0d0) &
    call XABORT('SPOT1P: INVALID RADIAL VOLUME SUM.')
  weight=real(vol2d,dp)/vtot
  mass_m=0.0d0
  total_m=0.0d0
  radial_m=0.0d0
  scat_m=0.0d0
  source_m=0.0d0

  ! SPOPHYS produces this exact diagonal coordinate map.  Detect the
  ! algebraic structure from B itself so correctness does not depend on a
  ! provenance flag and avoid forming O(NREG2D*NMODE**2) projections.
  diagonal_basis=nmode == nreg2d
  if (diagonal_basis) then
    do i=1,nreg2d
      do a=1,nmode
        if (i == a) then
          if (basis(i,a) == 0.0) diagonal_basis=.false.
        else
          if (basis(i,a) /= 0.0) diagonal_basis=.false.
        endif
      enddo
    enddo
  endif

  if (diagonal_basis) then
    do i=1,nreg2d
      wi=weight(i)
      scale=real(basis(i,i),dp)
      mass_m(i,i)=wi*scale*scale
    enddo
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      if (isnap < 1 .or. isnap > nsnap) &
        call XABORT('SPOT1P: INVALID SNAPSHOT INDEX.')
      do i=1,nreg2d
        ibm=mat(ifloor,i)
        if (ibm == 0) cycle
        if (ibm < 0 .or. ibm > nmat) &
          call XABORT('SPOT1P: MATERIAL INDEX OVERFLOW.')
        wi=weight(i)
        scale=real(basis(i,i),dp)
        total_m(i,i,ifloor)=wi*scale*real(total(ibm),dp)*scale
        radial_m(i,i,ifloor)=wi*scale*radial2d(i,isnap)*scale
        do l=1,nsct
          scat_m(i,i,l,ifloor)=wi*scale*real(sgas(ibm,l),dp)*scale
          source_m(l,ifloor,i)=wi*scale*qext(1,l,ifloor,i)
        enddo
      enddo
    enddo
  else
    do i=1,nreg2d
      wi=weight(i)
      do b=1,nmode
        do a=1,nmode
          mass_m(a,b)=mass_m(a,b)+wi*real(basis(i,a),dp)* &
            real(basis(i,b),dp)
        enddo
      enddo
    enddo
    do ifloor=1,nfloor
      isnap=mat1d(ifloor)
      if (isnap < 1 .or. isnap > nsnap) &
        call XABORT('SPOT1P: INVALID SNAPSHOT INDEX.')
      do i=1,nreg2d
        ibm=mat(ifloor,i)
        if (ibm == 0) cycle
        if (ibm < 0 .or. ibm > nmat) &
          call XABORT('SPOT1P: MATERIAL INDEX OVERFLOW.')
        wi=weight(i)
        do a=1,nmode
          do b=1,nmode
            total_m(a,b,ifloor)=total_m(a,b,ifloor)+wi* &
              real(basis(i,a),dp)*real(total(ibm),dp)*real(basis(i,b),dp)
            radial_m(a,b,ifloor)=radial_m(a,b,ifloor)+wi* &
              real(basis(i,a),dp)*radial2d(i,isnap)* &
              real(basis(i,b),dp)
            do l=1,nsct
              scat_m(a,b,l,ifloor)=scat_m(a,b,l,ifloor)+wi* &
                real(basis(i,a),dp)*real(sgas(ibm,l),dp)* &
                real(basis(i,b),dp)
            enddo
          enddo
          do l=1,nsct
            source_m(l,ifloor,a)=source_m(l,ifloor,a)+wi* &
              real(basis(i,a),dp)*qext(1,l,ifloor,i)
          enddo
        enddo
      enddo
    enddo
  endif

  ! The boundary and local systems split by radial mode exactly whenever
  ! every stored off-diagonal projected coefficient is zero.
  mode_separable=.true.
  separability: do a=1,nmode
    do b=1,nmode
      if (a == b) cycle
      if (mass_m(a,b) /= 0.0d0 .or. &
          any(total_m(a,b,:) /= 0.0d0) .or. &
          any(radial_m(a,b,:) /= 0.0d0) .or. &
          any(scat_m(a,b,:,:) /= 0.0d0)) then
        mode_separable=.false.
        exit separability
      endif
    enddo
  enddo separability
  use_factor_cache=.false.
  if ((.not.translation).and.diagonal_basis.and.mode_separable) &
    call SPOT1P64_CACHE_PREPARE(igroup,nmode,use_factor_cache)

  do n=1,npq
    do l=1,nsct
      mn(n,l)=0.5d0*real(2*l-1,dp)*real(pl(l,n),dp)
      dn(l,n)=real(w(n),dp)*real(pl(l,n),dp)
    enddo
  enddo

  allocate(face(npq,nmode,nfloor+1),cell(npq,nmode,nfloor))
  allocate(modal_flux(nsct,nfloor,nmode),modal_cour(nfloor+1,nmode))
  face=0.0d0
  cell=0.0d0

  if (translation) then
    albedo_left=real(zcode(1),dp)
    albedo_right=real(zcode(2),dp)
  else
    albedo_left=merge(1.0d0,real(zcode(1),dp),ncode(1) == 2)
    albedo_right=merge(1.0d0,real(zcode(2),dp),ncode(2) == 2)
    if (ncode(1) == 7) albedo_left=0.0d0
    if (ncode(2) == 7) albedo_right=0.0d0
  endif

  call SPOT1P64_R1_TRY(igroup,nreg2d,nfloor,ielem,nmat,nsnap,nmode,ischm,npq,nsct, &
    lfixup,translation,mat1d,mat,ncode,opposite,vol1d,total,sgas,basis,vol2d,zcode,du,w,pl, &
    radial2d,mass_m,total_m,radial_m,scat_m,mn,dn,albedo_left,albedo_right,generic_candidate,generic_hit)

  if (.not.translation) then
    ! Solve the two-point boundary-value problem directly.  The block
    ! tridiagonal system is algebraically identical to diamond differencing
    ! but remains stable when the axial mesh is refined.
    if (mode_separable) then
      do a=1,nmode
        call boundary_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call boundary_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
  else
    ! Translation boundaries couple the two end faces.  Retain the compact
    ! shooting construction for this uncommon cyclic case.
    if (mode_separable) then
      do a=1,nmode
        call translation_solve(a,a,face,cell,albedo_left,albedo_right)
      enddo
    else
      call translation_solve(1,nmode,face,cell,albedo_left,albedo_right)
    endif
  endif

  modal_flux=0.0d0
  do a=1,nmode
    do ifloor=1,nfloor
      do l=1,nsct
        do n=1,npq
          modal_flux(l,ifloor,a)=modal_flux(l,ifloor,a)+dn(l,n)*cell(n,a,ifloor)
        enddo
      enddo
    enddo
  enddo
  modal_cour=0.0d0
  do a=1,nmode
    do iface=1,nfloor+1
      do n=1,npq
        modal_cour(iface,a)=modal_cour(iface,a)+real(w(n),dp)* &
          real(du(n),dp)*face(n,a,iface)
      enddo
    enddo
  enddo

  flux=0.0
  cour=0.0
  xnei=0.0
  do i=1,nreg2d
    do a=1,nmode
      do ifloor=1,nfloor
        do l=1,nsct
          flux(1,l,ifloor,i)=flux(1,l,ifloor,i)+ &
            basis(i,a)*modal_flux(l,ifloor,a)
        enddo
      enddo
      do iface=1,nfloor+1
        cour(iface,i)=cour(iface,i)+basis(i,a)*modal_cour(iface,a)
      enddo
      do n=1,npq
        xnei(n,i)=xnei(n,i)+basis(i,a)*face(n,a,1)
      enddo
    enddo
  enddo
  if (any(.not.ieee_is_finite(flux)) .or. &
      any(.not.ieee_is_finite(cour)) .or. &
      any(.not.ieee_is_finite(xnei))) &
    call XABORT('SPOT1P: NON-FINITE RECONSTRUCTED SOLUTION.')

  deallocate(opposite,modal_cour,modal_flux,cell,face)
  deallocate(dn,mn,source_m,scat_m,radial_m,total_m,mass_m,weight)
  return

contains

  subroutine boundary_solve(first_mode,last_mode,face_flux,cell_flux, &
                            left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: lower(:,:,:),diagonal(:,:,:)
    double precision, allocatable :: upper(:,:,:),right_hand(:,:)
    double precision, allocatable :: cprime(:,:,:),dprime(:,:)
    double precision, allocatable :: solution(:,:),augmented(:,:)
    double precision, allocatable :: solve_pack(:,:),rhs_one(:,:)
    double precision, allocatable :: generic_lower(:,:),generic_rhs(:,:),generic_pack(:,:)
    double precision :: h,kvalue,svalue
    integer :: block,iz,ia,ib,in,jn,il,ir,ic,info,local_state
    logical :: cached_path,cache_hit,generic_store

    local_state=(last_mode-first_mode+1)*npq
    cached_path=use_factor_cache.and.(first_mode == last_mode)
    cache_hit=.false.
    if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        cache_hit=plan%ready
        if (cache_hit) then
          if (plan%nstate /= local_state .or. plan%nblock /= nfloor+1) &
            call XABORT('SPOT1P64 CACHE: BLOCK DIMENSIONS CHANGED INSIDE FLU.')
          if (.not.allocated(plan%lower)) &
            call XABORT('SPOT1P64 CACHE: MISSING STORED LOWER BLOCKS.')
          if (size(plan%lower,1) /= local_state .or. &
              size(plan%lower,2) /= local_state .or. &
              size(plan%lower,3) /= nfloor+1) &
            call XABORT('SPOT1P64 CACHE: INVALID STORED LOWER BLOCKS.')
        endif
      end associate
    endif
    if (generic_hit) then
      if (SPOT1P64_R1_PLAN(igroup)%nstate/=local_state.or. &
          SPOT1P64_R1_PLAN(igroup)%nblock/=nfloor+1) &
        call XABORT('R1 EXACT CACHE: BLOCK DIMENSIONS CHANGED.')
      cache_hit=.true.
    endif
    if (.not.cache_hit) then
      allocate(lower(local_state,local_state,nfloor+1))
      allocate(diagonal(local_state,local_state,nfloor+1))
      allocate(upper(local_state,local_state,nfloor+1))
      lower=0.0d0
      diagonal=0.0d0
      upper=0.0d0
    endif
    allocate(right_hand(local_state,nfloor+1))
    allocate(dprime(local_state,nfloor+1),solution(local_state,nfloor+1))
    if (generic_hit) then
      allocate(generic_lower(local_state,local_state),generic_rhs(local_state,1))
    else if (cached_path) then
      if (cache_hit) then
        allocate(rhs_one(local_state,1))
      else
        allocate(solve_pack(local_state,local_state+1))
      endif
    else
      allocate(cprime(local_state,local_state,nfloor+1))
      allocate(augmented(local_state,2*local_state+1))
    endif
    right_hand=0.0d0

    do block=0,nfloor
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          if (du(in) > 0.0) then
            if (block == 0) then
              if (.not.cache_hit) then
                diagonal(ir,ir,1)=1.0d0
                diagonal(ir,(ia-first_mode)*npq+opposite(in),1)= &
                  -left_albedo
              endif
              cycle
            endif
            iz=block
          else
            if (block == nfloor) then
              if (.not.cache_hit) then
                diagonal(ir,ir,nfloor+1)=1.0d0
                diagonal(ir,(ia-first_mode)*npq+opposite(in),nfloor+1)= &
                  -right_albedo
              endif
              cycle
            endif
            iz=block+1
          endif

          h=real(vol1d(iz),dp)
          svalue=0.0d0
          do il=1,nsct
            svalue=svalue+mn(in,il)*source_m(il,iz,ia)
          enddo
          right_hand(ir,block+1)=h*svalue

          if (cache_hit) cycle

          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
              kvalue=0.0d0
              if (in == jn) kvalue=kvalue+total_m(ia,ib,iz)
              do il=1,nsct
                kvalue=kvalue-mn(in,il)*scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)
              if (du(in) > 0.0) then
                lower(ir,ic,block+1)=0.5d0*h*kvalue
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
              else
                diagonal(ir,ic,block+1)=0.5d0*h*kvalue
                upper(ir,ic,block+1)=0.5d0*h*kvalue
              endif
            enddo
            ic=(ib-first_mode)*npq+in
            if (du(in) > 0.0) then
              lower(ir,ic,block+1)=lower(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            else
              diagonal(ir,ic,block+1)=diagonal(ir,ic,block+1)- &
                real(du(in),dp)*mass_m(ia,ib)
              upper(ir,ic,block+1)=upper(ir,ic,block+1)+ &
                real(du(in),dp)*mass_m(ia,ib)
            endif
          enddo
        enddo
      enddo
    enddo

    generic_store=.false.
    if (generic_candidate.and..not.generic_hit) then
      call SPOT1P64_R1_STORE_BEGIN(igroup,lower,du,generic_store)
      if (generic_store) allocate(generic_pack(local_state,local_state+1))
    endif
    if (generic_hit.or.generic_store) then
      associate(plan => SPOT1P64_R1_PLAN(igroup))
        if (generic_hit) then
          do block=1,nfloor+1
            generic_rhs(:,1)=right_hand(:,block)
            if (block > 1) then
              call SPOT1P64_R1_LOWER(igroup,block,generic_lower)
              generic_rhs(:,1)=generic_rhs(:,1)- &
                matmul(generic_lower,dprime(:,block-1))
            endif
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),generic_rhs,info)
            if (info /= 0) call XABORT('R1 EXACT CACHE: INVALID STORED FACTOR.')
            dprime(:,block)=generic_rhs(:,1)
          enddo
          call SPOT1P64_R1_NOTE_REUSE(nfloor+1)
        else
          do block=1,nfloor+1
            if (block == 1) then
              plan%factor(:,:,block)=diagonal(:,:,block)
              generic_pack(:,local_state+1)=right_hand(:,block)
            else
              plan%factor(:,:,block)=diagonal(:,:,block)- &
                matmul(lower(:,:,block),plan%cprime(:,:,block-1))
              generic_pack(:,local_state+1)=right_hand(:,block)- &
                matmul(lower(:,:,block),dprime(:,block-1))
            endif
            call SPOT1P64_FACTOR64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),info)
            if (info /= 0) then
              if (block == 1) then
                call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
              else
                call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
              endif
            endif
            generic_pack(:,:local_state)=upper(:,:,block)
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),generic_pack,info)
            if (info /= 0) call XABORT('R1 EXACT CACHE: NEW FACTOR SOLVE FAILED.')
            plan%cprime(:,:,block)=generic_pack(:,:local_state)
            dprime(:,block)=generic_pack(:,local_state+1)
          enddo
          plan%ready=.true.
          call SPOT1P64_R1_NOTE_BUILD(nfloor+1)
        endif
      end associate
    else if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        if (cache_hit) then
          do block=1,nfloor+1
            rhs_one(:,1)=right_hand(:,block)
            if (block > 1) rhs_one(:,1)=rhs_one(:,1)- &
              matmul(plan%lower(:,:,block),dprime(:,block-1))
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block), &
              rhs_one,info)
            if (info /= 0) &
              call XABORT('SPOT1P64 CACHE: INVALID STORED FACTOR.')
            dprime(:,block)=rhs_one(:,1)
          enddo
          call SPOT1P64_CACHE_NOTE_REUSE(nfloor+1)
        else
          plan%nstate=local_state
          plan%nblock=nfloor+1
          allocate(plan%factor(local_state,local_state,nfloor+1))
          allocate(plan%pivot(local_state,nfloor+1))
          allocate(plan%pivot_value(local_state,nfloor+1))
          allocate(plan%cprime(local_state,local_state,nfloor+1))
          allocate(plan%lower(local_state,local_state,nfloor+1))
          plan%lower=lower
          do block=1,nfloor+1
            if (block == 1) then
              plan%factor(:,:,block)=diagonal(:,:,block)
              solve_pack(:,local_state+1)=right_hand(:,block)
            else
              plan%factor(:,:,block)=diagonal(:,:,block)- &
                matmul(lower(:,:,block),plan%cprime(:,:,block-1))
              solve_pack(:,local_state+1)=right_hand(:,block)- &
                matmul(lower(:,:,block),dprime(:,block-1))
            endif
            call SPOT1P64_FACTOR64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),info)
            if (info /= 0) then
              if (block == 1) then
                call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
              else
                call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
              endif
            endif
            solve_pack(:,:local_state)=upper(:,:,block)
            call SPOT1P64_SOLVE64(plan%factor(:,:,block), &
              plan%pivot(:,block),plan%pivot_value(:,block),solve_pack,info)
            if (info /= 0) &
              call XABORT('SPOT1P64 CACHE: NEW FACTOR SOLVE FAILED.')
            plan%cprime(:,:,block)=solve_pack(:,:local_state)
            dprime(:,block)=solve_pack(:,local_state+1)
          enddo
          plan%ready=.true.
          call SPOT1P64_CACHE_NOTE_BUILD(nfloor+1)
        endif
      end associate
    else
      augmented=0.0d0
      augmented(:,:local_state)=diagonal(:,:,1)
      augmented(:,local_state+1:2*local_state)=upper(:,:,1)
      augmented(:,2*local_state+1)=right_hand(:,1)
      call ALSBD(local_state,local_state+1,augmented,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR FIRST AXIAL BLOCK.')
      cprime(:,:,1)=augmented(:,local_state+1:2*local_state)
      dprime(:,1)=augmented(:,2*local_state+1)

      do block=2,nfloor+1
        augmented=0.0d0
        augmented(:,:local_state)=diagonal(:,:,block)- &
          matmul(lower(:,:,block),cprime(:,:,block-1))
        augmented(:,local_state+1:2*local_state)=upper(:,:,block)
        augmented(:,2*local_state+1)=right_hand(:,block)- &
          matmul(lower(:,:,block),dprime(:,block-1))
        call ALSBD(local_state,local_state+1,augmented,info,local_state)
        if (info /= 0) call XABORT('SPOT1P: SINGULAR AXIAL SCHUR BLOCK.')
        cprime(:,:,block)=augmented(:,local_state+1:2*local_state)
        dprime(:,block)=augmented(:,2*local_state+1)
      enddo
    endif

    solution(:,nfloor+1)=dprime(:,nfloor+1)
    if (generic_hit.or.generic_store) then
      associate(plan => SPOT1P64_R1_PLAN(igroup))
        do block=nfloor,1,-1
          solution(:,block)=dprime(:,block)- &
            matmul(plan%cprime(:,:,block),solution(:,block+1))
        enddo
      end associate
    else if (cached_path) then
      associate(plan => SPOT1P64_PLAN(igroup)%mode(first_mode))
        do block=nfloor,1,-1
          solution(:,block)=dprime(:,block)- &
            matmul(plan%cprime(:,:,block),solution(:,block+1))
        enddo
      end associate
    else
      do block=nfloor,1,-1
        solution(:,block)=dprime(:,block)- &
          matmul(cprime(:,:,block),solution(:,block+1))
      enddo
    endif
    do block=1,nfloor+1
      do ia=first_mode,last_mode
        do in=1,npq
          face_flux(in,ia,block)= &
            solution((ia-first_mode)*npq+in,block)
        enddo
      enddo
    enddo
    do iz=1,nfloor
      cell_flux(:,first_mode:last_mode,iz)=0.5d0* &
        (face_flux(:,first_mode:last_mode,iz)+ &
         face_flux(:,first_mode:last_mode,iz+1))
    enddo

    if (allocated(generic_lower)) deallocate(generic_lower)
    if (allocated(generic_rhs)) deallocate(generic_rhs)
    if (allocated(generic_pack)) deallocate(generic_pack)
    if (allocated(augmented)) deallocate(augmented)
    if (allocated(solve_pack)) deallocate(solve_pack)
    if (allocated(rhs_one)) deallocate(rhs_one)
    if (allocated(cprime)) deallocate(cprime)
    deallocate(solution,dprime,right_hand)
    if (allocated(upper)) deallocate(upper,diagonal,lower)
  end subroutine boundary_solve

  subroutine translation_solve(first_mode,last_mode,face_flux,cell_flux, &
                               left_albedo,right_albedo)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, intent(in) :: left_albedo,right_albedo
    double precision, allocatable :: affine(:),response(:,:),system(:,:)
    integer :: local_state,ico,ia,ib,in,jn,row,info

    local_state=(last_mode-first_mode+1)*npq
    allocate(affine(local_state),response(local_state,local_state))
    allocate(system(local_state,local_state+1))

    face_flux(:,first_mode:last_mode,:)=0.0d0
    call sweep(first_mode,last_mode,face_flux,cell_flux)
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        affine(row)=face_flux(in,ia,nfloor+1)
      enddo
    enddo

    do ico=1,local_state
      face_flux(:,first_mode:last_mode,:)=0.0d0
      ia=first_mode+(ico-1)/npq
      in=mod(ico-1,npq)+1
      face_flux(in,ia,1)=1.0d0
      call sweep(first_mode,last_mode,face_flux,cell_flux)
      do ib=first_mode,last_mode
        do jn=1,npq
          row=(ib-first_mode)*npq+jn
          response(row,ico)=face_flux(jn,ib,nfloor+1)-affine(row)
        enddo
      enddo
    enddo

    system=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        if (du(in) > 0.0) then
          system(row,:local_state)=-left_albedo*response(row,:)
          system(row,row)=system(row,row)+1.0d0
          system(row,local_state+1)=left_albedo*affine(row)
        else
          system(row,:local_state)=response(row,:)
          system(row,row)=system(row,row)-right_albedo
          system(row,local_state+1)=-affine(row)
        endif
      enddo
    enddo

    call ALSBD(local_state,1,system,info,local_state)
    if (info /= 0) call XABORT('SPOT1P: SINGULAR MODAL BOUNDARY SYSTEM.')
    face_flux(:,first_mode:last_mode,:)=0.0d0
    do ia=first_mode,last_mode
      do in=1,npq
        row=(ia-first_mode)*npq+in
        face_flux(in,ia,1)=system(row,local_state+1)
      enddo
    enddo
    call sweep(first_mode,last_mode,face_flux,cell_flux)

    deallocate(system,response,affine)
  end subroutine translation_solve

  subroutine sweep(first_mode,last_mode,face_flux,cell_flux)
    integer, intent(in) :: first_mode,last_mode
    double precision, intent(inout) :: face_flux(npq,nmode,nfloor+1)
    double precision, intent(inout) :: cell_flux(npq,nmode,nfloor)
    double precision, allocatable :: amat(:,:)
    double precision :: h,rhs
    integer :: iz,ia,ib,in,jn,il,ir,ic,info,local_state

    local_state=(last_mode-first_mode+1)*npq
    allocate(amat(local_state,local_state+1))
    cell_flux(:,first_mode:last_mode,:)=0.0d0
    do iz=1,nfloor
      h=real(vol1d(iz),dp)
      amat=0.0d0
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          rhs=0.0d0
          do ib=first_mode,last_mode
            do jn=1,npq
              ic=(ib-first_mode)*npq+jn
              if (in == jn) amat(ir,ic)=amat(ir,ic)+h*total_m(ia,ib,iz)
              do il=1,nsct
                amat(ir,ic)=amat(ir,ic)-h*mn(in,il)* &
                  scat_m(ia,ib,il,iz)*dn(il,jn)
              enddo
              amat(ir,ic)=amat(ir,ic)+h*mn(in,1)* &
                radial_m(ia,ib,iz)*dn(1,jn)
            enddo
            ic=(ib-first_mode)*npq+in
            amat(ir,ic)=amat(ir,ic)+2.0d0*real(du(in),dp)* &
              mass_m(ia,ib)
            rhs=rhs+2.0d0*real(du(in),dp)*mass_m(ia,ib)* &
              face_flux(in,ib,iz)
          enddo
          do il=1,nsct
            rhs=rhs+h*mn(in,il)*source_m(il,iz,ia)
          enddo
          amat(ir,local_state+1)=rhs
        enddo
      enddo
      call ALSBD(local_state,1,amat,info,local_state)
      if (info /= 0) call XABORT('SPOT1P: SINGULAR LOCAL MODAL SYSTEM.')
      do ia=first_mode,last_mode
        do in=1,npq
          ir=(ia-first_mode)*npq+in
          cell_flux(in,ia,iz)=amat(ir,local_state+1)
          face_flux(in,ia,iz+1)=2.0d0*cell_flux(in,ia,iz)- &
            face_flux(in,ia,iz)
        enddo
      enddo
    enddo
    deallocate(amat)
  end subroutine sweep

end subroutine SPOT1P64
