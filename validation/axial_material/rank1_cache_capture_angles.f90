! Archival callbacks only. No argument of the production calculation is writable.
! One isolated, predeclared map012 warm replay; all 370 groups, SN32, 48 cells.
module AXMAT_RANK1_CAPTURE_MOD
  use, intrinsic :: iso_fortran_env, only: int32,int64,real32,real64
  implicit none
  private
  public :: AXMAT_CAPTURE_BEGIN,AXMAT_CAPTURE_CONTEXT,AXMAT_CAPTURE_INPUT
  public :: AXMAT_CAPTURE_OUTPUT,AXMAT_CAPTURE_FIELD,AXMAT_CAPTURE_BLOCKS
  public :: AXMAT_CAPTURE_TERMINAL,AXMAT_CAPTURE_PRENORMAL,AXMAT_CAPTURE_PUBLISH
  public :: AXMAT_CAPTURE_KEY,AXMAT_CAPTURE_KEY_VALIDATED,AXMAT_CAPTURE_SLOT7
  integer, parameter :: ng=370,nun=1800,nz=48,na=32,nr=8,nl=3
  logical, save :: armed=.false.,terminal=.false.,prenormal=.false.
  integer, save :: outer=0,inner=0,dispatch=0,pending=0,nmaterial=0
  integer, save :: event_unit,term_int(9)
  real(real64), save :: term_real(7)
  real(real32), save :: last_b2(4)
  integer, allocatable, save :: context(:,:),seen(:),blocks_seen(:),active(:)
  integer, allocatable, save :: block_assemblies(:),last_block_dispatch(:),block_cached(:)
  integer, save :: ni=0,ns=0,nd=0
  integer, save :: key_seen(2,ng)=0,key_calls(2,ng)=0
  integer, save :: key_pending(2,ng)=0,key_length(2,ng)=0
  logical, save :: key_identical(2,ng)=.false.
  integer :: key_unit
  integer(int64),save :: cache_stats(6)=0_int64
contains
  subroutine AXMAT_CAPTURE_BEGIN(ngr,nunk,nreg,nmat,nfun,itype,ileak, &
      leaksw,lrebal,ncptl,ncpta,itpij,nanis,ndim,insb,lscal,nlf,nlin)
    integer,intent(in) :: ngr,nunk,nreg,nmat,nfun,itype,ileak,ncptl,ncpta,itpij,nanis,ndim,insb,nlf,nlin
    logical,intent(in) :: leaksw,lrebal,lscal
    integer :: ios
    if (armed) call XABORT('AXMAT CAPTURE: MORE THAN ONE FLU INVOCATION.')
    if (ngr /= ng .or. nunk /= nun .or. nreg /= nr*nz .or. nfun /= nl &
        .or. itype /= 3 .or. ileak /= 3 .or. .not.leaksw .or. lrebal &
        .or. ncptl /= 3 .or. ncpta /= 0 .or. itpij /= 1 .or. nanis /= 2 &
        .or. ndim /= 1 .or. insb /= 1 .or. lscal .or. nlf /= 32 .or. nlin /= 1 .or. nmat /= 24) &
      call XABORT('AXMAT CAPTURE: OUTSIDE FROZEN PRODUCTION CONTRACT.')
    nmaterial=nmat
    allocate(context(3,ng),seen(ng),blocks_seen(ng))
    allocate(block_assemblies(ng),last_block_dispatch(ng),block_cached(ng))
    context=0;seen=0;blocks_seen=0
    block_assemblies=0;last_block_dispatch=0;block_cached=0
    open(newunit=event_unit,file='angular_capture_events.bin',status='new', &
      access='stream',form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: EVENT ARCHIVE EXISTS OR UNWRITABLE.')
    write(event_unit) 'AXCEV002',int([ng,nun,nreg,nmat,nfun,itype,ileak, &
      merge(1,0,leaksw),merge(1,0,lrebal),ncptl,ncpta,itpij,nanis,ndim,insb, &
      merge(1,0,lscal),nlf,nlin],int32)
    open(newunit=key_unit,file='angular_cache_events.bin',status='new',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: CACHE EVENTS UNWRITABLE.')
    write(key_unit) 'AXCKE001',int([ng,2],int32)
    armed=.true.
  end subroutine

  subroutine AXMAT_CAPTURE_CONTEXT(it,jt)
    integer,intent(in) :: it,jt
    if (.not.armed .or. terminal .or. pending /= 0) &
      call XABORT('AXMAT CAPTURE: INVALID CHRONOLOGICAL CONTEXT.')
    outer=it;inner=jt
  end subroutine

  subroutine AXMAT_CAPTURE_INPUT(ngeff,ngind,nunk,s2,ileak,b2,npsys)
    integer,intent(in) :: ngeff,nunk,ngind(ngeff),ileak,npsys(ng)
    real(real64),intent(in) :: s2(nunk,ngeff)
    real(real32),intent(in) :: b2(4)
    integer :: j,g,unit,ios
    character(64) :: filename
    if (.not.armed .or. terminal .or. pending /= 0 .or. outer <= 0 &
        .or. inner <= 0 .or. nunk /= nun .or. ileak /= 3 .or. b2(4) /= 0.0) &
      call XABORT('AXMAT CAPTURE: INVALID ORIGINAL SOURCE DISPATCH.')
    if (ngeff <= 0 .or. ngeff > ng .or. count(npsys /= 0) /= ngeff) &
      call XABORT('AXMAT CAPTURE: INVALID ORIGINAL ACTIVE GROUP INVENTORY.')
    if (allocated(active)) deallocate(active)
    allocate(active(ngeff));active=ngind
    dispatch=dispatch+1;pending=dispatch;last_b2=b2
    write(event_unit) int([dispatch,outer,inner,ngeff],int32),int(ngind,int32), &
      int(npsys,int32),b2
    do j=1,ngeff
      g=ngind(j)
      if (g < 1 .or. g > ng .or. count(ngind == g) /= 1 .or. npsys(g) == 0) &
        call XABORT('AXMAT CAPTURE: DUPLICATE OR OUTSIDE ACTUAL GROUP.')
      ! Only this group's archival file is replaced, strictly chronologically.
      ! No source, angle, iteration or returned field is chosen by a metric.
      write(filename,'(A,I3.3,A)') 'angular_source_g',g,'.bin'
      open(newunit=unit,file=trim(filename),status='replace',access='stream', &
        form='unformatted',action='write',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: SOURCE ARCHIVE UNWRITABLE.')
      write(unit) 'AXCS2001',int([g,dispatch,outer,inner,nun],int32),s2(:,j)
      close(unit,iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: SOURCE ARCHIVE CLOSE FAILED.')
      context(:,g)=[dispatch,outer,inner]
    enddo
  end subroutine

  subroutine AXMAT_CAPTURE_OUTPUT(ngeff,ngind,nunk,f2)
    integer,intent(in) :: ngeff,nunk,ngind(ngeff)
    real(real64),intent(in) :: f2(nunk,ngeff)
    integer :: j,g,unit,ios
    character(64) :: filename
    if (pending /= dispatch .or. nunk /= nun .or. .not.allocated(active)) &
      call XABORT('AXMAT CAPTURE: UNMATCHED ORIGINAL RETURN.')
    if (size(active) /= ngeff .or. any(active /= ngind)) &
      call XABORT('AXMAT CAPTURE: ORIGINAL RETURN GROUP INVENTORY CHANGED.')
    do j=1,ngeff
      g=ngind(j)
      if (seen(g) /= dispatch) call XABORT('AXMAT CAPTURE: MISSING ANGULAR FIELD.')
      write(filename,'(A,I3.3,A)') 'angular_return_g',g,'.bin'
      open(newunit=unit,file=trim(filename),status='replace',access='stream', &
        form='unformatted',action='write',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: RETURN ARCHIVE UNWRITABLE.')
      write(unit) 'AXCRT001',int([g,dispatch,outer,inner,nun],int32),f2(:,j)
      close(unit,iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: RETURN ARCHIVE CLOSE FAILED.')
    enddo
    pending=0
  end subroutine

  subroutine AXMAT_CAPTURE_BLOCKS(g,lower,diagonal,upper,cached,cache_hit)
    integer,intent(in) :: g
    logical,intent(in) :: cached,cache_hit
    real(real64),intent(in) :: lower(:,:,:),diagonal(:,:,:),upper(:,:,:)
    character(64) :: filename
    integer :: unit,ios
    integer(int32) :: header(8)
    character(8) :: magic
    real(real64),allocatable :: previous_lower(:,:,:),previous_diagonal(:,:,:),previous_upper(:,:,:)
    if (.not.armed .or. pending == 0 .or. g < 1 .or. g > ng .or. &
        .not.cached .or. cache_hit .or. last_block_dispatch(g) == dispatch) &
      call XABORT('AXMAT CAPTURE: INVALID ORIGINAL BLOCK ASSEMBLY.')
    if (any(shape(lower) /= [na,na,nz+1]) .or. &
        any(shape(diagonal) /= shape(lower)) .or. any(shape(upper) /= shape(lower))) &
      call XABORT('AXMAT CAPTURE: ORIGINAL BLOCK DIMENSIONS CHANGED.')
    write(filename,'(A,I3.3,A)') 'angular_collision_g',g,'.bin'
    if (blocks_seen(g) == 0) then
      open(newunit=unit,file=trim(filename),status='new',access='stream', &
        form='unformatted',action='write',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: COLLISION ARCHIVE UNWRITABLE.')
      write(unit) 'AXCBL001',int([g,dispatch,outer,inner,na,nz+1, &
        merge(1,0,cached),merge(1,0,cache_hit)],int32)
      write(unit) lower,diagonal,upper
      close(unit,iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: COLLISION ARCHIVE CLOSE FAILED.')
      blocks_seen(g)=dispatch
    else
      call XABORT('AXMAT CAPTURE: SECOND CACHE MISS IN SAME ORIGINAL LIFECYCLE.')
    endif
    block_assemblies(g)=block_assemblies(g)+1
    last_block_dispatch(g)=dispatch
    block_cached(g)=merge(1,0,cached)
  end subroutine

  subroutine AXMAT_CAPTURE_FIELD(g,nmat,nsnap,mat1d,mat,ncode,opposite, &
      vol1d,total,sgas,basis,vol2d,zcode,du,w,pl,radial2d,qext, &
      weight,mass_m,total_m,radial_m,scat_m,source_m,mn,dn,white_angle, &
      white_mode,cell,face,modal_flux,modal_cour,flux,cour,xnei,white_on,white_row,white_perimeter,ischm,lfixup)
    integer,intent(in) :: g,nmat,nsnap,mat1d(nz),mat(nz,nr),ncode(2),opposite(na)
    logical,intent(in) :: white_on,lfixup
    integer,intent(in) :: white_row,ischm
    real(real64),intent(in) :: white_perimeter
    real(real32),intent(in) :: vol1d(nz),total(0:nmat),sgas(0:nmat,nl)
    real(real32),intent(in) :: basis(nr,1),vol2d(nr),zcode(2),du(na),w(na),pl(nl,na)
    real(real64),intent(in) :: radial2d(nr,nsnap),qext(1,nl,nz,nr)
    real(real64),intent(in) :: weight(nr),mass_m(1,1),total_m(1,1,nz)
    real(real64),intent(in) :: radial_m(1,1,nz),scat_m(1,1,nl,nz),source_m(nl,nz,1)
    real(real64),intent(in) :: mn(na,nl),dn(nl,na),white_angle(na,na),white_mode(1,1)
    real(real64),intent(in) :: cell(na,1,nz),face(na,1,nz+1)
    real(real64),intent(in) :: modal_flux(nl,nz,1),modal_cour(nz+1,1)
    real(real64),intent(in) :: flux(1,nl,nz,nr),cour(nz+1,nr),xnei(na,nr)
    integer(int32),allocatable :: ipack(:)
    real(real32),allocatable :: spack(:)
    real(real64),allocatable :: dpack(:)
    integer(int32),allocatable :: previous_i(:)
    real(real32),allocatable :: previous_s(:)
    real(real64),allocatable :: previous_d(:)
    integer :: stable_count,unit,ios
    logical :: stable_operator
    integer(int32) :: header(8)
    character(8) :: magic
    character(64) :: filename
    if (.not.armed .or. pending == 0 .or. g < 1 .or. g > ng .or. &
        nmat /= nmaterial .or. nsnap /= 3 .or. .not.white_on) &
      call XABORT('AXMAT CAPTURE: OUTSIDE ORIGINAL ANGULAR CALL SCOPE.')
    if (.not.any(active == g) .or. context(1,g) /= dispatch .or. seen(g) == dispatch) &
      call XABORT('AXMAT CAPTURE: UNMATCHED ANGULAR GROUP CALL.')
    ipack=int([mat1d,reshape(mat,[size(mat)]),ncode,opposite,white_row,ischm,merge(1,0,lfixup)],int32)
    spack=[vol1d,total,reshape(sgas,[size(sgas)]),reshape(basis,[size(basis)]), &
      vol2d,zcode,du,w,reshape(pl,[size(pl)])]
    ! The operator prefix contains no source or solved field and must be immutable
    ! across every chronological native iteration. Raw bits are compared below.
    dpack=[white_perimeter,reshape(radial2d,[size(radial2d)]),weight,reshape(mass_m,[1]), &
      reshape(total_m,[size(total_m)]),reshape(radial_m,[size(radial_m)]), &
      reshape(scat_m,[size(scat_m)]),reshape(mn,[size(mn)]),reshape(dn,[size(dn)]), &
      reshape(white_angle,[size(white_angle)]),reshape(white_mode,[1]), &
      reshape(qext,[size(qext)]),reshape(source_m,[size(source_m)]), &
      reshape(cell,[size(cell)]),reshape(face,[size(face)]), &
      reshape(modal_flux,[size(modal_flux)]),reshape(modal_cour,[size(modal_cour)]), &
      reshape(flux,[size(flux)]),reshape(cour,[size(cour)]),reshape(xnei,[size(xnei)])]
    stable_count=1+size(radial2d)+size(weight)+1+2*nz+nl*nz+2*na*nl+na*na+1
    if (nd == 0) then
      ni=size(ipack);ns=size(spack);nd=size(dpack)
    endif
    if (size(dpack) /= nd .or. size(spack) /= ns .or. size(ipack) /= ni) &
      call XABORT('AXMAT CAPTURE: GROUP ARCHIVE LAYOUT CHANGED.')
    write(filename,'(A,I3.3,A)') 'angular_field_g',g,'.bin'
    stable_operator=.true.
    if (seen(g) /= 0) then
      allocate(previous_i(ni),previous_s(ns),previous_d(stable_count))
      open(newunit=unit,file=trim(filename),status='old',access='stream', &
        form='unformatted',action='read',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: PREVIOUS FIELD ARCHIVE MISSING.')
      read(unit) magic,header,previous_i,previous_s,previous_d
      close(unit)
      if (magic /= 'AXCFD001' .or. header(1) /= g .or. header(2) /= seen(g) .or. &
          any(header(5:8) /= [ni,ns,nd,stable_count])) &
        call XABORT('AXMAT CAPTURE: PREVIOUS FIELD ARCHIVE INVALID.')
      if (any(previous_i /= ipack) .or. &
          any(transfer(previous_s,[0_int32],size(spack)) /= &
              transfer(spack,[0_int32],size(spack))) .or. &
          any(transfer(previous_d,[0_int32],2*stable_count) /= &
              transfer(dpack(:stable_count),[0_int32],2*stable_count))) &
        stable_operator=.false.
    endif
    open(newunit=unit,file=trim(filename),status='replace',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: FIELD ARCHIVE UNWRITABLE.')
    write(unit) 'AXCFD001',int([g,dispatch,outer,inner,ni,ns,nd,stable_count],int32)
    write(unit) ipack,spack,dpack
    close(unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: FIELD ARCHIVE CLOSE FAILED.')
    if (.not.stable_operator) call XABORT('AXMAT CAPTURE: ORIGINAL FIXED OPERATOR CHANGED.')
    seen(g)=dispatch
  end subroutine

  subroutine AXMAT_CAPTURE_TERMINAL(iext,iter,igdeb,inr,unk,maxout,maxin, &
      eext,epsout,eunk,epsunk,einr,epsin,akeff,stats,old_outer,slot3,slot7,slot8)
    integer,intent(in) :: iext,iter,igdeb,inr,unk,maxout,maxin
    real(real32),intent(in) :: epsout,epsunk,epsin
    real(real64),intent(in) :: eext,eunk,einr,akeff
    integer(int64),intent(in) :: stats(6)
    real(real64),intent(in) :: old_outer(nun,ng),slot3(nun,ng),slot7(nun,ng),slot8(nun,ng)
    integer :: unit,ios
    if (.not.armed .or. terminal .or. pending /= 0 .or. &
        iext /= 3 .or. iter /= 1 .or. igdeb /= ng+1 .or. inr /= 1 .or. unk /= 1 &
        .or. maxout /= 500 .or. maxin /= 740 .or. &
        any(context(2,:) /= iext) .or. any(context(3,:) /= iter) .or. &
        any(seen == 0) .or. any(blocks_seen == 0) .or. &
        any(block_assemblies /= 1) .or. any(block_cached /= 1) .or. &
        any(key_seen == 0) .or. any(key_calls < 1) .or. &
        stats(1) /= int(ng*(nz+1),int64) .or. stats(2) <= 0_int64 .or. &
        stats(3) /= sum(int(key_calls(2,:)-1,int64)) .or. &
        stats(2) /= stats(3)*int(nz+1,int64) .or. &
        stats(6) /= 536870912_int64 .or. stats(5) > stats(6)) &
      call XABORT('AXMAT CAPTURE: PREDECLARED ORIGINAL FINAL CALL REQUIRED.')
    term_int=[iext,iter,igdeb,inr,unk,maxout,maxin,dispatch,ng]
    term_real=[eext,real(epsout,real64),eunk, &
      real(epsunk,real64),einr,real(epsin,real64),akeff]
    cache_stats=stats
    open(newunit=unit,file='angular_terminal_slots.bin',status='new',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: TERMINAL SLOT ARCHIVE UNWRITABLE.')
    write(unit) 'AXCTS001',int([nun,ng,iext,iter],int32),old_outer,slot3,slot7,slot8
    close(unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: TERMINAL SLOT ARCHIVE CLOSE FAILED.')
    terminal=.true.
  end subroutine

  subroutine AXMAT_CAPTURE_PRENORMAL(nunk,ngr,flux)
    integer,intent(in) :: nunk,ngr
    real(real64),intent(in) :: flux(nunk,ngr)
    integer :: unit,ios
    if (.not.terminal .or. prenormal .or. nunk /= nun .or. ngr /= ng) &
      call XABORT('AXMAT CAPTURE: ORIGINAL PRENORMALIZATION REQUIRED.')
    open(newunit=unit,file='angular_pre_normal.bin',status='new',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: PRENORMAL ARCHIVE UNWRITABLE.')
    write(unit) 'AXCPN001',int([nun,ng],int32),flux
    close(unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: PRENORMAL ARCHIVE CLOSE FAILED.')
    prenormal=.true.
  end subroutine

  subroutine AXMAT_CAPTURE_PUBLISH(nunk,ngr,flux,sour,akeff,fisour)
    integer,intent(in) :: nunk,ngr
    real(real64),intent(in) :: flux(nunk,ngr),sour(nunk,ngr),akeff,fisour
    integer :: unit,ios,g
    if (.not.terminal .or. .not.prenormal .or. nunk /= nun .or. ngr /= ng) &
      call XABORT('AXMAT CAPTURE: ORIGINAL PUBLISHED SOLUTION REQUIRED.')
    open(newunit=unit,file='angular_capture.bin',status='new',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: FINAL ARCHIVE UNWRITABLE.')
    write(unit) 'AXCAP002',int([ng,nun,nz,na,nr,nl,nmaterial,3, &
      ni,ns,nd],int32)
    write(unit) int(term_int,int32),term_real,last_b2,akeff,fisour,cache_stats
    do g=1,ng
      write(unit) int([g,context(:,g),seen(g),blocks_seen(g),block_assemblies(g), &
        last_block_dispatch(g),block_cached(g)],int32)
      write(unit) flux(:,g),sour(:,g)
    enddo
    close(unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: FINAL ARCHIVE CLOSE FAILED.')
    close(event_unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: EVENT ARCHIVE CLOSE FAILED.')
    close(key_unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: CACHE EVENT CLOSE FAILED.')
    write(6,'(A)') 'AXMAT-RANK1-NATIVE-ANGULAR-CAPTURE-PUBLISHED'
  end subroutine

  subroutine AXMAT_CAPTURE_KEY(g,key,phase,eligible)
    integer,intent(in) :: g,phase
    integer(int64),intent(in) :: key(:)
    logical,intent(in) :: eligible
    integer :: unit,ios
    integer(int32) :: header(6)
    integer(int64),allocatable :: previous(:)
    logical :: identical
    character(64) :: filename
    character(8) :: magic
    if (.not.armed .or. terminal .or. pending /= dispatch .or. g < 1 .or. g > ng .or. &
        phase < 1 .or. phase > 2 .or. .not.eligible) &
      call XABORT('AXMAT CAPTURE: OUTSIDE ACTUAL RANK1 KEY VALIDATION.')
    if (.not.any(active == g) .or. size(key) <= 0) &
      call XABORT('AXMAT CAPTURE: KEY HAS NO ACTUAL SOURCE DISPATCH.')
    write(filename,'(A,I1,A,I3.3,A)') 'angular_key_p',phase,'_g',g,'.bin'
    identical=.true.
    if (key_seen(phase,g) /= 0) then
      allocate(previous(size(key)))
      open(newunit=unit,file=trim(filename),status='old',access='stream', &
        form='unformatted',action='read',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: FIRST RAW CACHE KEY MISSING.')
      read(unit,iostat=ios) magic,header,previous
      close(unit)
      identical=ios == 0 .and. magic == 'AXCKY001'
      if (identical) identical=header(1) == g .and. header(2) == phase .and. &
        header(3) == key_seen(phase,g) .and. header(6) == size(key)
      if (identical) identical=all(previous == key)
    else
      open(newunit=unit,file=trim(filename),status='new',access='stream', &
        form='unformatted',action='write',iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: FIRST RAW CACHE KEY UNWRITABLE.')
      write(unit) 'AXCKY001',int([g,phase,dispatch,outer,inner,size(key)],int32),key
      close(unit,iostat=ios)
      if (ios /= 0) call XABORT('AXMAT CAPTURE: FIRST RAW CACHE KEY CLOSE FAILED.')
      key_seen(phase,g)=dispatch
    endif
    ! A failed attempted key is retained before the observer aborts.
    if (.not.identical) then
      write(filename,'(A,I1,A,I3.3,A)') 'angular_key_failure_p',phase,'_g',g,'.bin'
      open(newunit=unit,file=trim(filename),status='new',access='stream',form='unformatted',action='write')
      write(unit) 'AXCKY001',int([g,phase,dispatch,outer,inner,size(key)],int32),key
      close(unit)
    endif
    key_pending(phase,g)=dispatch
    key_length(phase,g)=size(key)
    key_identical(phase,g)=identical
  end subroutine

  subroutine AXMAT_CAPTURE_KEY_VALIDATED(g,phase,active_now)
    integer,intent(in) :: g,phase
    logical,intent(in) :: active_now
    if (g < 1 .or. g > ng .or. phase < 1 .or. phase > 2) &
      call XABORT('AXMAT CAPTURE: INVALID POST-GUARD KEY EVENT.')
    if (.not.active_now .or. key_pending(phase,g) /= dispatch .or. &
        .not.key_identical(phase,g)) &
      call XABORT('AXMAT CAPTURE: ACTUAL VALIDATED OPERATOR KEY CHANGED.')
    ! The event is emitted only after the genuine production guard returned.
    write(key_unit) int([dispatch,outer,inner,g,phase,key_length(phase,g), &
      merge(1,0,key_calls(phase,g) > 0),1],int32)
    flush(key_unit)
    key_calls(phase,g)=key_calls(phase,g)+1
    key_pending(phase,g)=0
  end subroutine

  subroutine AXMAT_CAPTURE_SLOT7(phase,nunk,ngr,igdeb,accelerated,slot6,slot7)
    integer,intent(in) :: phase,nunk,ngr,igdeb,accelerated
    real(real64),intent(in) :: slot6(nunk,ngr),slot7(nunk,ngr)
    integer :: unit,ios
    character(64) :: filename
    if (.not.armed .or. terminal .or. pending /= 0 .or. nunk /= nun .or. ngr /= ng .or. &
        phase < 1 .or. phase > 3) call XABORT('AXMAT CAPTURE: INVALID ACTUAL SLOT7 OBSERVATION.')
    write(filename,'(A,I1,A)') 'angular_slot7_phase',phase,'.bin'
    open(newunit=unit,file=trim(filename),status='replace',access='stream', &
      form='unformatted',action='write',iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: SLOT7 ARCHIVE UNWRITABLE.')
    write(unit) 'AXCS7001',int([phase,nun,ng,outer,inner,igdeb,accelerated],int32),slot6,slot7
    close(unit,iostat=ios)
    if (ios /= 0) call XABORT('AXMAT CAPTURE: SLOT7 ARCHIVE CLOSE FAILED.')
  end subroutine
end module AXMAT_RANK1_CAPTURE_MOD
