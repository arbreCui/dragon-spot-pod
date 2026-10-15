module SPOR64_BOOT_CANONICAL64_V2
  ! NEW SOURCE. Full SPOSTATE64 mathematics, canonical write and recomputation.
  ! Context equality and host full-file pins are separate from solver provenance.
  use, intrinsic :: iso_c_binding, only : c_ptr, c_associated
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use GANLIB
  use SPOR64_VERIFY, only : RECORD_MATCHES, CHARACTER_RECORD_MATCHES
  implicit none
  private
  public :: SPOR64_BOOT_CANONICAL64_CHECK,SPOR64_BOOT_CANONICAL64_WRITE
contains
  subroutine SPOR64_BOOT_CANONICAL64_CHECK(ipax,iptrack,ipsystem,ipmacro,ok)
    type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro
    logical, intent(out) :: ok
    call CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,.false.,ok)
  end subroutine SPOR64_BOOT_CANONICAL64_CHECK
  subroutine SPOR64_BOOT_CANONICAL64_WRITE(ipax,iptrack,ipsystem,ipmacro,ok)
    type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro
    logical, intent(out) :: ok
    call CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,.true.,ok)
  end subroutine SPOR64_BOOT_CANONICAL64_WRITE
subroutine CANONICAL_CORE(ipax,iptrack,ipsystem,ipmacro,write_mode,ok)
  ! Construct the canonical fixed-space outer state x=(a,1/k,L) from one
  ! completed axial SPOT solution.
  !
  !   AXFLUX := SPOSTATE64: AXFLUX TRACK_AX SYSTEM_AX MACROLIB3 :: ;
  !
  ! A single global nu-fission-production normalization removes the arbitrary
  ! eigenvector scale. Plane coordinates are obtained by reproducing SPOPROJ's
  ! volume restriction and solving the stored-basis Gram system. Leakage is
  ! independently reconstructed from the same scalar flux and face currents.
  use GANLIB
  use SPOT_LEAKAGE, only : SPOLE1D
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: kind_guard=1/merge(1,0, &
    kind(1)==int32.and.kind(1.0)==real32.and.dp==real64)
  type(c_ptr), intent(in) :: ipax,iptrack,ipsystem,ipmacro
  type(c_ptr) :: kentry(4)
  logical, intent(out) :: ok
  logical, intent(in) :: write_mode
  logical :: solve_ok

  integer :: iflux(nstate),itrack(nstate),isystem(nstate),imacro(nstate)
  integer :: ngrp,nreg,nunk,nreg2d,nfloor,nsnap,nmix,nfis,ll4,ll5
  integer :: igr,ireg,ibm,ifis,ifloor,isnap,i,a,b,nmode
  integer :: ilong,itylcm,indic,nitma,total_coef,total_gram,total_basis,index
  integer :: fixb,version
  integer(int64) :: next_coef64,next_gram64,next_basis64,layout_limit64
  integer, allocatable :: mat(:),keyflx(:),mat1d(:),rank(:)
  integer, allocatable :: offset(:),gram_offset(:),basis_offset(:)
  real :: flott,keff
  real(kind=dp) :: projected64,restriction_weight64
  real, allocatable :: area(:),dz(:),volume(:),mirror32(:,:)
  real, allocatable :: nufis(:),basis(:,:),vol2d(:)
  real, allocatable :: basis_state(:)
  real(kind=dp) :: dflott,norm,production,weight_sum
  real(kind=dp) :: keff64
  real(kind=dp), allocatable :: unknown64(:,:)
  real(kind=dp), allocatable :: phi64(:,:),current64(:,:)
  real(kind=dp), allocatable :: leak64(:),num64(:),den64(:)
  type(c_ptr) :: jpflux64
  real(kind=dp) :: rho,gram_error,offspace2,reconstructed
  real(kind=dp), allocatable :: coordinates(:),leak(:),height(:)
  real(kind=dp), allocatable :: gram_flat(:),offspace(:)
  real(kind=dp), allocatable :: gram(:,:),rhs(:),solution(:),plane(:)
  character(len=4) :: text4
  character(len=12) :: signature,track_type,basis_type,norm_id
  type(c_ptr) :: jpflux,jpmacro,kpmacro,jpsystem,kpsystem

  ok=.false.
  if (.not.c_associated(ipax).or..not.c_associated(iptrack).or. &
      .not.c_associated(ipsystem).or..not.c_associated(ipmacro)) return
  kentry=[ipax,iptrack,ipsystem,ipmacro]

  if (.not. RECORD_MATCHES(kentry(1),'SIGNATURE',3,3)) return
  if (.not. RECORD_MATCHES(kentry(2),'SIGNATURE',3,3)) return
  if (.not. RECORD_MATCHES(kentry(2),'TRACK-TYPE',3,3)) return
  if (.not. RECORD_MATCHES(kentry(3),'SIGNATURE',3,3)) return
  if (.not. RECORD_MATCHES(kentry(4),'SIGNATURE',3,3)) return
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') return
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') return
  call LCMGTC(kentry(2),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') return
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') return
  call LCMGTC(kentry(4),'SIGNATURE',12,signature)
  if (signature /= 'L_MACROLIB') &
    return

  if (.not. RECORD_MATCHES(kentry(1),'STATE-VECTOR',nstate,1)) return
  if (.not. RECORD_MATCHES(kentry(2),'STATE-VECTOR',nstate,1)) return
  if (.not. RECORD_MATCHES(kentry(3),'STATE-VECTOR',nstate,1)) return
  if (.not. RECORD_MATCHES(kentry(4),'STATE-VECTOR',nstate,1)) return
  call LCMGET(kentry(1),'STATE-VECTOR',iflux)
  call LCMGET(kentry(2),'STATE-VECTOR',itrack)
  call LCMGET(kentry(3),'STATE-VECTOR',isystem)
  call LCMGET(kentry(4),'STATE-VECTOR',imacro)
  ngrp=iflux(1)
  if (ngrp /= 370.or.imacro(4) /= 32) return
  nunk=iflux(2)
  nreg=itrack(1)
  nreg2d=itrack(6)
  nfloor=itrack(7)
  nsnap=itrack(8)
  ll4=itrack(11)
  ll5=itrack(12)
  nmix=imacro(2)
  nfis=imacro(4)
  if ((ngrp <= 0).or.(nunk <= 0).or.(nreg2d <= 0).or. &
      (nfloor <= 0).or.(nsnap <= 0).or.(nmix <= 0).or.(nfis <= 0)) &
    return
  if ((nreg /= nreg2d*nfloor).or.(nunk /= itrack(2)).or. &
      (ngrp /= imacro(1)).or.(ngrp /= isystem(8)).or. &
      (nunk /= isystem(9)).or.(ll4 < 0).or. &
      (ll5 /= nreg2d*(nfloor+1)).or.(ll4+ll5 > nunk)) &
    return

  call LCMLEN(kentry(1),'K-EFFECTIVE',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 2)) &
    return
  call LCMGET(kentry(1),'K-EFFECTIVE',keff)
  if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0)) &
    return
  call LCMLEN(kentry(1),'SPOT-KEFF64',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 4)) &
    return
  call LCMGET(kentry(1),'SPOT-KEFF64',keff64)
  if ((.not.ieee_is_finite(keff64)).or.(keff64 <= 0.0_dp)) &
    return
  if (transfer(real(keff64,real32),0_int32) /= transfer(keff,0_int32)) &
    return
  rho=1.0_dp/keff64

  call LCMLEN(kentry(3),'SPOT-FIXB',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 1)) &
    return
  call LCMGET(kentry(3),'SPOT-FIXB',fixb)
  if ((fixb /= 0).and.(fixb /= 1)) &
    return
  call LCMLEN(kentry(3),'SPOT-BTYPE',ilong,itylcm)
  if ((ilong /= 3).or.(itylcm /= 3)) &
    return
  call LCMGTC(kentry(3),'SPOT-BTYPE',12,basis_type)
  if ((basis_type /= 'POD-BUILT').and.(basis_type /= 'POD-FIXED')) &
    return
  if ((fixb == 0).neqv.(basis_type == 'POD-BUILT')) &
    return

  allocate(mat(nreg),keyflx(nreg),mat1d(nfloor),rank(ngrp))
  allocate(area(nreg2d),dz(nfloor),volume(nreg))
  allocate(mirror32(nunk,ngrp))
  if (.not. RECORD_MATCHES(kentry(2),'MATCOD',nreg,1)) return
  if (.not. RECORD_MATCHES(kentry(2),'KEYFLX',nreg,1)) return
  if (.not. RECORD_MATCHES(kentry(2),'MAT1D',nfloor,1)) return
  if (.not. RECORD_MATCHES(kentry(2),'AREA2D',nreg2d,2)) return
  if (.not. RECORD_MATCHES(kentry(2),'VOL1D',nfloor,2)) return
  if (.not. RECORD_MATCHES(kentry(2),'VOLUME',nreg,2)) return
  call LCMGET(kentry(2),'MATCOD',mat)
  call LCMGET(kentry(2),'KEYFLX',keyflx)
  call LCMGET(kentry(2),'MAT1D',mat1d)
  call LCMGET(kentry(2),'AREA2D',area)
  call LCMGET(kentry(2),'VOL1D',dz)
  call LCMGET(kentry(2),'VOLUME',volume)
  if (any((mat1d < 1).or.(mat1d > nsnap))) &
    return
  if (any(.not.ieee_is_finite(area)).or.any(area <= 0.0).or. &
      any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0).or. &
      any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0)) &
    return
  do i=1,nreg2d
    do ifloor=1,nfloor
      ireg=(i-1)*nfloor+ifloor
      if (abs(real(volume(ireg),dp)-real(area(i),dp)*real(dz(ifloor),dp)) &
          > 0.5_dp*real(spacing(volume(ireg)),dp)) &
        return
    enddo
  enddo
  if (any(keyflx < 0).or.any(keyflx > nunk).or. &
      any(mat < 0).or.any(mat > nmix)) &
    return

  if (.not. RECORD_MATCHES(kentry(1),'FLUX',ngrp,10)) return
  jpflux=LCMGID(kentry(1),'FLUX')
  do igr=1,ngrp
    call LCMLEL(jpflux,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 2)) &
      return
    call LCMGDL(jpflux,igr,mirror32(:,igr))
  enddo
  if (any(.not.ieee_is_finite(mirror32))) &
    return
  call LCMLEN(kentry(1),'FLUX64',ilong,itylcm)
  if ((ilong /= ngrp).or.(itylcm /= 10)) &
    return
  jpflux64=LCMGID(kentry(1),'FLUX64')
  allocate(unknown64(nunk,ngrp))
  do igr=1,ngrp
    call LCMLEL(jpflux64,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 4)) &
      return
    call LCMGDL(jpflux64,igr,unknown64(:,igr))
    if (any(.not.ieee_is_finite(unknown64(:,igr)))) &
      return
    do i=1,nunk
      if (transfer(real(unknown64(i,igr),real32),0_int32) /= &
          transfer(mirror32(i,igr),0_int32)) &
        return
    enddo
  enddo
  do ireg=1,nreg
    if ((mat(ireg) > 0).and.(keyflx(ireg) > 0)) then
      do igr=1,ngrp
        if (unknown64(keyflx(ireg),igr) <= 0.0_dp) &
          return
      enddo
    endif
  enddo

  ! One global nu-fission-production normalization.
  allocate(nufis(nmix*nfis))
  jpmacro=LCMGID(kentry(4),'GROUP')
  norm=0.0_dp
  do igr=1,ngrp
    kpmacro=LCMGIL(jpmacro,igr)
    call LCMLEN(kpmacro,'NUSIGF',ilong,itylcm)
    if (ilong == 0) return
    if ((ilong /= nmix*nfis).or.(itylcm /= 2)) &
      return
    call LCMGET(kpmacro,'NUSIGF',nufis)
    if (any(.not.ieee_is_finite(nufis))) &
      return
    do ireg=1,nreg
      ibm=mat(ireg)
      if ((ibm <= 0).or.(keyflx(ireg) <= 0)) cycle
      production=0.0_dp
      do ifis=1,nfis
        production=production+ &
          real(nufis((ifis-1)*nmix+ibm),dp)
      enddo
      norm=norm+real(volume(ireg),dp)* &
        unknown64(keyflx(ireg),igr)*production
    enddo
  enddo
  if ((.not.ieee_is_finite(norm)).or.(norm <= 0.0_dp)) &
    return

  ! Reconstruct the original signed leakage from the same REAL64 field.
  ! SPOLE1D promotes only the unchanged stored geometric measures.
  allocate(leak(ngrp*nsnap))
  allocate(phi64(nfloor,nreg2d),current64(nfloor+1,nreg2d))
  allocate(leak64(nsnap),num64(nsnap),den64(nsnap))
  do igr=1,ngrp
    do i=1,nreg2d
      do ifloor=1,nfloor
        ireg=(i-1)*nfloor+ifloor
        if (keyflx(ireg) > 0) then
          phi64(ifloor,i)=unknown64(keyflx(ireg),igr)
        else
          phi64(ifloor,i)=0.0_dp
        endif
      enddo
      do a=1,nfloor+1
        current64(a,i)=unknown64(ll4+(i-1)*(nfloor+1)+a,igr)
      enddo
    enddo
    call SPOLE1D(nreg2d,nfloor,nsnap,mat1d,dz,area,phi64, &
                 current64,leak64,num64,den64)
    do isnap=1,nsnap
      index=(isnap-1)*ngrp+igr
      leak(index)=leak64(isnap)
    enddo
  enddo
  if (any(.not.ieee_is_finite(leak))) &
    return

  ! Recover the fixed radial basis layout.
  call LCMLEN(kentry(3),'GROUP',ilong,itylcm)
  if ((ilong /= ngrp).or.(itylcm /= 10)) &
    return
  jpsystem=LCMGID(kentry(3),'GROUP')
  allocate(offset(ngrp+1),gram_offset(ngrp+1),basis_offset(ngrp+1))
  offset(1)=0
  gram_offset(1)=0
  basis_offset(1)=0
  layout_limit64=int(huge(total_coef),int64)
  do igr=1,ngrp
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMLEN(kpsystem,'POD-NMODE',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      return
    call LCMGET(kpsystem,'POD-NMODE',rank(igr))
    if ((rank(igr) <= 0).or.(rank(igr) > nreg2d)) &
      return
    next_coef64=int(offset(igr),int64)+ &
      int(nsnap,int64)*int(rank(igr),int64)
    next_gram64=int(gram_offset(igr),int64)+ &
      int(rank(igr),int64)*int(rank(igr),int64)
    next_basis64=int(basis_offset(igr),int64)+ &
      int(nreg2d,int64)*int(rank(igr),int64)
    if ((next_coef64 > layout_limit64).or. &
        (next_gram64 > layout_limit64).or. &
        (next_basis64 > layout_limit64)) &
      return
    offset(igr+1)=int(next_coef64)
    gram_offset(igr+1)=int(next_gram64)
    basis_offset(igr+1)=int(next_basis64)
  enddo
  total_coef=offset(ngrp+1)
  total_gram=gram_offset(ngrp+1)
  total_basis=basis_offset(ngrp+1)
  allocate(coordinates(total_coef),gram_flat(total_gram))
  allocate(basis_state(total_basis))
  allocate(offspace(ngrp*nsnap),height(nsnap))
  coordinates=0.0_dp
  gram_flat=0.0_dp
  basis_state=0.0
  offspace=0.0_dp
  height=0.0_dp
  do ifloor=1,nfloor
    height(mat1d(ifloor))=height(mat1d(ifloor))+real(dz(ifloor),dp)
  enddo
  if (any(height <= 0.0_dp)) &
    return

  gram_error=0.0_dp
  do igr=1,ngrp
    nmode=rank(igr)
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMLEN(kpsystem,'NREG2D',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      return
    call LCMGET(kpsystem,'NREG2D',i)
    if (i /= nreg2d) return
    call LCMLEN(kpsystem,'NSNAP',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      return
    call LCMGET(kpsystem,'NSNAP',i)
    if (i /= nsnap) return
    allocate(basis(nreg2d,nmode),vol2d(nreg2d))
    call LCMLEN(kpsystem,'POD-BASIS',ilong,itylcm)
    if ((ilong /= nreg2d*nmode).or.(itylcm /= 2)) &
      return
    call LCMGET(kpsystem,'POD-BASIS',basis)
    basis_state(basis_offset(igr)+1:basis_offset(igr+1))= &
      reshape(basis,(/nreg2d*nmode/))
    call LCMLEN(kpsystem,'VOL2D',ilong,itylcm)
    if ((ilong /= nreg2d).or.(itylcm /= 2)) &
      return
    call LCMGET(kpsystem,'VOL2D',vol2d)
    if (any(.not.ieee_is_finite(basis)).or. &
        any(.not.ieee_is_finite(vol2d)).or.any(vol2d <= 0.0)) &
      return
    do i=1,nreg2d
      if (transfer(vol2d(i),0) /= transfer(area(i),0)) &
        return
    enddo
    weight_sum=sum(real(vol2d,dp))
    allocate(gram(nmode,nmode),rhs(nmode),solution(nmode))
    allocate(plane(nreg2d))
    gram=0.0_dp
    do a=1,nmode
      do b=1,nmode
        do i=1,nreg2d
          gram(a,b)=gram(a,b)+real(vol2d(i),dp)/weight_sum* &
            real(basis(i,a),dp)*real(basis(i,b),dp)
        enddo
        if (a == b) then
          gram_error=max(gram_error,abs(gram(a,b)-1.0_dp))
        else
          gram_error=max(gram_error,abs(gram(a,b)))
        endif
        index=gram_offset(igr)+(b-1)*nmode+a
        gram_flat(index)=gram(a,b)
      enddo
    enddo

    do isnap=1,nsnap
      plane=0.0_dp
      do i=1,nreg2d
        ! Preserve the original volume restriction and floor order.
        ! Every product, sum and division uses the REAL64 authority.
        projected64=0.0_dp
        restriction_weight64=0.0_dp
        do ifloor=1,nfloor
          if (mat1d(ifloor) /= isnap) cycle
          ireg=(i-1)*nfloor+ifloor
          if (keyflx(ireg) <= 0) cycle
          projected64=projected64+real(volume(ireg),dp)* &
            unknown64(keyflx(ireg),igr)
          restriction_weight64=restriction_weight64+real(volume(ireg),dp)
        enddo
        if (restriction_weight64 <= 0.0_dp) &
          return
        projected64=projected64/restriction_weight64
        if ((.not.ieee_is_finite(projected64)).or. &
            (projected64 <= 0.0_dp)) &
          return
        plane(i)=projected64/norm
      enddo
      rhs=0.0_dp
      do a=1,nmode
        do i=1,nreg2d
          rhs(a)=rhs(a)+real(vol2d(i),dp)/weight_sum* &
            real(basis(i,a),dp)*plane(i)
        enddo
      enddo
      call solve_spd(gram,rhs,solution,nmode,solve_ok)
      if (.not.solve_ok) return
      do a=1,nmode
        index=offset(igr)+(isnap-1)*nmode+a
        coordinates(index)=solution(a)
      enddo
      offspace2=0.0_dp
      do i=1,nreg2d
        reconstructed=0.0_dp
        do a=1,nmode
          reconstructed=reconstructed+ &
            real(basis(i,a),dp)*solution(a)
        enddo
        offspace2=offspace2+real(vol2d(i),dp)/weight_sum* &
          (plane(i)-reconstructed)**2
      enddo
      offspace((igr-1)*nsnap+isnap)=sqrt(max(0.0_dp,offspace2))
    enddo
    deallocate(plane,solution,rhs,gram,vol2d,basis)
  enddo

  if (any(.not.ieee_is_finite(coordinates)).or. &
      any(.not.ieee_is_finite(gram_flat)).or. &
      any(.not.ieee_is_finite(offspace)).or. &
      (.not.ieee_is_finite(gram_error))) &
    return

  version=1
  if (write_mode) then
    call LCMPUT(kentry(1),'SPOT-X-DIMS',4,1,[version,ngrp,nsnap,total_coef])
    call LCMPUT(kentry(1),'SPOT-X-RANK',ngrp,1,rank)
    call LCMPUT(kentry(1),'SPOT-X-OFF',ngrp+1,1,offset)
    call LCMPUT(kentry(1),'SPOT-X-GOFF',ngrp+1,1,gram_offset)
    call LCMPUT(kentry(1),'SPOT-X-BOFF',ngrp+1,1,basis_offset)
    call LCMPUT(kentry(1),'SPOT-X-A',total_coef,4,coordinates)
    call LCMPUT(kentry(1),'SPOT-X-GRAM',total_gram,4,gram_flat)
    call LCMPUT(kentry(1),'SPOT-X-BASIS',total_basis,2,basis_state)
    call LCMPUT(kentry(1),'SPOT-X-RHO',1,4,rho)
    call LCMPUT(kentry(1),'SPOT-X-KEFF',1,4,keff64)
    call LCMPUT(kentry(1),'SPOT-X-L',ngrp*nsnap,4,leak)
    call LCMPUT(kentry(1),'SPOT-X-H',nsnap,4,height)
    call LCMPUT(kentry(1),'SPOT-X-NORM',1,4,norm)
    call LCMPUT(kentry(1),'SPOT-X-PERP',ngrp*nsnap,4,offspace)
    call LCMPUT(kentry(1),'SPOT-X-GERR',1,4,gram_error)
    call LCMPUT(kentry(1),'SPOT-X-FIXB',1,1,fixb)
    call LCMPTC(kentry(1),'SPOT-X-NID',12,'NUFISS-UNIT ')
    call LCMPTC(kentry(1),'SPOT-X-BTYP',12,basis_type)
  else
  if (.not.CHECK_I(kentry(1),'SPOT-X-DIMS',[version,ngrp,nsnap,total_coef])) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-RANK',rank)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-OFF',offset)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-GOFF',gram_offset)) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-BOFF',basis_offset)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-A',coordinates)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-GRAM',gram_flat)) return
  if (.not.CHECK_32(kentry(1),'SPOT-X-BASIS',basis_state)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-RHO',[rho])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-KEFF',[keff64])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-L',leak)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-H',height)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-NORM',[norm])) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-PERP',offspace)) return
  if (.not.CHECK_64(kentry(1),'SPOT-X-GERR',[gram_error])) return
  if (.not.CHECK_I(kentry(1),'SPOT-X-FIXB',[fixb])) return
  if (.not.CHARACTER_RECORD_MATCHES(kentry(1),'SPOT-X-NID',3,12,'NUFISS-UNIT')) return
  if (.not.CHARACTER_RECORD_MATCHES(kentry(1),'SPOT-X-BTYP',3,12,basis_type)) return
  endif
  ok=.true.

  deallocate(height,offspace,basis_state,gram_flat,coordinates)
  deallocate(basis_offset,gram_offset,offset,rank)
  deallocate(leak,den64,num64,leak64,current64,phi64,unknown64)
  deallocate(nufis,mirror32,volume,dz,area,mat1d,keyflx,mat)

contains


  subroutine solve_spd(matrix,vector,result,n,ok)
    integer, intent(in) :: n
    real(kind=dp), intent(in) :: matrix(n,n),vector(n)
    real(kind=dp), intent(out) :: result(n)
    real(kind=dp) :: lower(n,n),work(n),pivot
    integer :: row,col,k
    logical, intent(out) :: ok

    ok=.false.
    result=0.0_dp
    lower=0.0_dp
    do row=1,n
      do col=1,row
        pivot=matrix(row,col)
        do k=1,col-1
          pivot=pivot-lower(row,k)*lower(col,k)
        enddo
        if (row == col) then
          if ((.not.ieee_is_finite(pivot)).or.(pivot <= 0.0_dp)) &
            return
          lower(row,col)=sqrt(pivot)
        else
          lower(row,col)=pivot/lower(col,col)
        endif
      enddo
    enddo
    do row=1,n
      work(row)=vector(row)
      do k=1,row-1
        work(row)=work(row)-lower(row,k)*work(k)
      enddo
      work(row)=work(row)/lower(row,row)
    enddo
    do row=n,1,-1
      result(row)=work(row)
      do k=row+1,n
        result(row)=result(row)-lower(k,row)*result(k)
      enddo
      result(row)=result(row)/lower(row,row)
    enddo
    if (any(.not.ieee_is_finite(result))) &
      return
    ok=.true.
  end subroutine solve_spd

end subroutine CANONICAL_CORE

  logical function CHECK_I(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected(:)
    integer, allocatable :: actual(:)
    integer :: istat
    CHECK_I=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),1)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_I=all(actual == expected)
  end function CHECK_I

  logical function CHECK_32(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real32), intent(in) :: expected(:)
    real(real32), allocatable :: actual(:)
    integer :: istat
    CHECK_32=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),2)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_32=all(transfer(actual,0_int32,size(actual)) == &
                transfer(expected,0_int32,size(expected)))
  end function CHECK_32

  logical function CHECK_64(object,name,expected)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: expected(:)
    real(real64), allocatable :: actual(:)
    integer :: istat
    CHECK_64=.false.
    if (.not.RECORD_MATCHES(object,name,size(expected),4)) return
    allocate(actual(size(expected)),stat=istat)
    if (istat /= 0) return
    call LCMGET(object,name,actual)
    CHECK_64=all(transfer(actual,0_int64,size(actual)) == &
                transfer(expected,0_int64,size(expected)))
  end function CHECK_64
end module SPOR64_BOOT_CANONICAL64_V2
