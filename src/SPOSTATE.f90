!DECK SPOSTATE
subroutine SPOSTATE(nentry,hentry,ientry,jentry,kentry)
  ! Construct the canonical fixed-space outer state x=(a,1/k,L) from one
  ! completed axial SPOT solution.
  !
  !   AXFLUX := SPOSTATE: AXFLUX TRACK_AX SYSTEM_AX MACROLIB3 :: ;
  !
  ! A single global nu-fission-production normalization removes the arbitrary
  ! eigenvector scale. Plane coordinates are obtained by reproducing SPOPROJ's
  ! volume restriction and solving the stored-basis Gram system. Leakage is
  ! independently reconstructed from the same scalar flux and face currents.
  use GANLIB
  use SPOT_LEAKAGE, only : SPOLE1
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: nstate=40
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: iflux(nstate),itrack(nstate),isystem(nstate),imacro(nstate)
  integer :: ngrp,nreg,nunk,nreg2d,nfloor,nsnap,nmix,nfis,ll4,ll5
  integer :: igr,ireg,ibm,ifis,ifloor,isnap,i,a,b,nmode
  integer :: ilong,itylcm,indic,nitma,total_coef,total_gram,total_basis,index
  integer :: fixb,version
  integer, allocatable :: mat(:),keyflx(:),mat1d(:),rank(:)
  integer, allocatable :: offset(:),gram_offset(:),basis_offset(:)
  real :: flott,keff,projected_sp,weight_sp
  real, allocatable :: area(:),dz(:),volume(:),unknown(:,:)
  real, allocatable :: nufis(:),basis(:,:),vol2d(:)
  real, allocatable :: basis_state(:)
  real, allocatable :: phi(:,:),current(:,:),leak_sp(:)
  real, allocatable :: numerator(:),denominator(:)
  real(kind=dp) :: dflott,norm,production,weight_sum
  real(kind=dp) :: rho,gram_error,offspace2,reconstructed
  real(kind=dp), allocatable :: coordinates(:),leak(:),height(:)
  real(kind=dp), allocatable :: gram_flat(:),offspace(:)
  real(kind=dp), allocatable :: gram(:,:),rhs(:),solution(:),plane(:)
  character(len=4) :: text4
  character(len=12) :: signature,track_type,basis_type,norm_id
  type(c_ptr) :: jpflux,jpmacro,kpmacro,jpsystem,kpsystem

  if (nentry /= 4) call XABORT('SPOSTATE: FOUR ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOSTATE: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 1).or.any(jentry(2:4) /= 2)) &
    call XABORT('SPOSTATE: MODIFIABLE FLUX AND THREE INPUTS EXPECTED.')

  call require_record(kentry(1),'SIGNATURE',3,3,'AXIAL FLUX')
  call require_record(kentry(2),'SIGNATURE',3,3,'AXIAL TRACK')
  call require_record(kentry(2),'TRACK-TYPE',3,3,'AXIAL TRACK')
  call require_record(kentry(3),'SIGNATURE',3,3,'SPOD SYSTEM')
  call require_record(kentry(4),'SIGNATURE',3,3,'AXIAL MACROLIB')
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOSTATE: L_FLUX EXPECTED.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_TRACK') call XABORT('SPOSTATE: L_TRACK EXPECTED.')
  call LCMGTC(kentry(2),'TRACK-TYPE',12,track_type)
  if (track_type /= 'SPOT') call XABORT('SPOSTATE: SPOT TRACK EXPECTED.')
  call LCMGTC(kentry(3),'SIGNATURE',12,signature)
  if (signature /= 'L_PIJ') call XABORT('SPOSTATE: L_PIJ EXPECTED.')
  call LCMGTC(kentry(4),'SIGNATURE',12,signature)
  if (signature /= 'L_MACROLIB') &
    call XABORT('SPOSTATE: L_MACROLIB EXPECTED.')

  call require_record(kentry(1),'STATE-VECTOR',nstate,1,'AXIAL FLUX')
  call require_record(kentry(2),'STATE-VECTOR',nstate,1,'AXIAL TRACK')
  call require_record(kentry(3),'STATE-VECTOR',nstate,1,'SPOD SYSTEM')
  call require_record(kentry(4),'STATE-VECTOR',nstate,1,'AXIAL MACROLIB')
  call LCMGET(kentry(1),'STATE-VECTOR',iflux)
  call LCMGET(kentry(2),'STATE-VECTOR',itrack)
  call LCMGET(kentry(3),'STATE-VECTOR',isystem)
  call LCMGET(kentry(4),'STATE-VECTOR',imacro)
  ngrp=iflux(1)
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
    call XABORT('SPOSTATE: INVALID DIMENSIONS.')
  if ((nreg /= nreg2d*nfloor).or.(nunk /= itrack(2)).or. &
      (ngrp /= imacro(1)).or.(ngrp /= isystem(8)).or. &
      (nunk /= isystem(9)).or.(ll4 < 0).or. &
      (ll5 /= nreg2d*(nfloor+1)).or.(ll4+ll5 > nunk)) &
    call XABORT('SPOSTATE: INCONSISTENT OBJECT DIMENSIONS.')

  call LCMLEN(kentry(1),'K-EFFECTIVE',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 2)) &
    call XABORT('SPOSTATE: INVALID K-EFFECTIVE RECORD.')
  call LCMGET(kentry(1),'K-EFFECTIVE',keff)
  if ((.not.ieee_is_finite(keff)).or.(keff <= 0.0)) &
    call XABORT('SPOSTATE: NONPOSITIVE K-EFFECTIVE.')
  rho=1.0_dp/real(keff,dp)

  call LCMLEN(kentry(3),'SPOT-FIXB',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 1)) &
    call XABORT('SPOSTATE: MISSING BASIS-STATE MARKER.')
  call LCMGET(kentry(3),'SPOT-FIXB',fixb)
  if ((fixb /= 0).and.(fixb /= 1)) &
    call XABORT('SPOSTATE: INVALID BASIS-STATE MARKER.')
  call LCMLEN(kentry(3),'SPOT-BTYPE',ilong,itylcm)
  if ((ilong /= 3).or.(itylcm /= 3)) &
    call XABORT('SPOSTATE: MISSING BASIS-TYPE MARKER.')
  call LCMGTC(kentry(3),'SPOT-BTYPE',12,basis_type)
  if ((basis_type /= 'POD-BUILT').and.(basis_type /= 'POD-FIXED')) &
    call XABORT('SPOSTATE: UNKNOWN BASIS TYPE.')
  if ((fixb == 0).neqv.(basis_type == 'POD-BUILT')) &
    call XABORT('SPOSTATE: INCONSISTENT BASIS MARKERS.')

  allocate(mat(nreg),keyflx(nreg),mat1d(nfloor),rank(ngrp))
  allocate(area(nreg2d),dz(nfloor),volume(nreg))
  allocate(unknown(nunk,ngrp))
  call require_record(kentry(2),'MATCOD',nreg,1,'AXIAL TRACK')
  call require_record(kentry(2),'KEYFLX',nreg,1,'AXIAL TRACK')
  call require_record(kentry(2),'MAT1D',nfloor,1,'AXIAL TRACK')
  call require_record(kentry(2),'AREA2D',nreg2d,2,'AXIAL TRACK')
  call require_record(kentry(2),'VOL1D',nfloor,2,'AXIAL TRACK')
  call require_record(kentry(2),'VOLUME',nreg,2,'AXIAL TRACK')
  call LCMGET(kentry(2),'MATCOD',mat)
  call LCMGET(kentry(2),'KEYFLX',keyflx)
  call LCMGET(kentry(2),'MAT1D',mat1d)
  call LCMGET(kentry(2),'AREA2D',area)
  call LCMGET(kentry(2),'VOL1D',dz)
  call LCMGET(kentry(2),'VOLUME',volume)
  if (any((mat1d < 1).or.(mat1d > nsnap))) &
    call XABORT('SPOSTATE: INVALID FLOOR/SNAPSHOT MAP.')
  if (any(.not.ieee_is_finite(area)).or.any(area <= 0.0).or. &
      any(.not.ieee_is_finite(dz)).or.any(dz <= 0.0).or. &
      any(.not.ieee_is_finite(volume)).or.any(volume <= 0.0)) &
    call XABORT('SPOSTATE: INVALID GEOMETRY.')
  do i=1,nreg2d
    do ifloor=1,nfloor
      ireg=(i-1)*nfloor+ifloor
      if (abs(real(volume(ireg),dp)-real(area(i),dp)*real(dz(ifloor),dp)) &
          > 0.5_dp*real(spacing(volume(ireg)),dp)) &
        call XABORT('SPOSTATE: INCONSISTENT EXTRUDED VOLUME.')
    enddo
  enddo
  if (any(keyflx < 0).or.any(keyflx > nunk).or. &
      any(mat < 0).or.any(mat > nmix)) &
    call XABORT('SPOSTATE: INVALID REGION MAP.')

  jpflux=LCMGID(kentry(1),'FLUX')
  do igr=1,ngrp
    call LCMLEL(jpflux,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 2)) &
      call XABORT('SPOSTATE: INVALID AXIAL FLUX ITEM.')
    call LCMGDL(jpflux,igr,unknown(:,igr))
  enddo
  if (any(.not.ieee_is_finite(unknown))) &
    call XABORT('SPOSTATE: NON-FINITE AXIAL FIELD.')
  do ireg=1,nreg
    if ((mat(ireg) > 0).and.(keyflx(ireg) > 0)) then
      do igr=1,ngrp
        if (unknown(keyflx(ireg),igr) <= 0.0) &
          call XABORT('SPOSTATE: NONPOSITIVE ACTIVE SCALAR FLUX.')
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
    if (ilong == 0) cycle
    if ((ilong /= nmix*nfis).or.(itylcm /= 2)) &
      call XABORT('SPOSTATE: INVALID NUSIGF RECORD.')
    call LCMGET(kpmacro,'NUSIGF',nufis)
    if (any(.not.ieee_is_finite(nufis))) &
      call XABORT('SPOSTATE: NON-FINITE NUSIGF.')
    do ireg=1,nreg
      ibm=mat(ireg)
      if ((ibm <= 0).or.(keyflx(ireg) <= 0)) cycle
      production=0.0_dp
      do ifis=1,nfis
        production=production+ &
          real(nufis((ifis-1)*nmix+ibm),dp)
      enddo
      norm=norm+real(volume(ireg),dp)* &
        real(unknown(keyflx(ireg),igr),dp)*production
    enddo
  enddo
  if ((.not.ieee_is_finite(norm)).or.(norm <= 0.0_dp)) &
    call XABORT('SPOSTATE: NONPOSITIVE GLOBAL NU-FISSION NORMALIZATION.')

  ! Reconstruct the signed plane leakage from this same axial field.
  allocate(phi(nfloor,nreg2d),current(nfloor+1,nreg2d))
  allocate(leak_sp(nsnap),numerator(nsnap),denominator(nsnap))
  allocate(leak(ngrp*nsnap))
  do igr=1,ngrp
    do i=1,nreg2d
      do ifloor=1,nfloor
        ireg=(i-1)*nfloor+ifloor
        if (keyflx(ireg) > 0) then
          phi(ifloor,i)=unknown(keyflx(ireg),igr)
        else
          phi(ifloor,i)=0.0
        endif
      enddo
      do a=1,nfloor+1
        current(a,i)=unknown(ll4+(i-1)*(nfloor+1)+a,igr)
      enddo
    enddo
    call SPOLE1(nreg2d,nfloor,nsnap,mat1d,dz,area,phi,current, &
                leak_sp,numerator,denominator)
    do isnap=1,nsnap
      index=(isnap-1)*ngrp+igr
      leak(index)=real(leak_sp(isnap),dp)
    enddo
  enddo
  if (any(.not.ieee_is_finite(leak))) &
    call XABORT('SPOSTATE: NON-FINITE LEAKAGE STATE.')

  ! Recover the fixed radial basis layout.
  call LCMLEN(kentry(3),'GROUP',ilong,itylcm)
  if ((ilong /= ngrp).or.(itylcm /= 10)) &
    call XABORT('SPOSTATE: INVALID SYSTEM GROUP LIST.')
  jpsystem=LCMGID(kentry(3),'GROUP')
  allocate(offset(ngrp+1),gram_offset(ngrp+1),basis_offset(ngrp+1))
  offset(1)=0
  gram_offset(1)=0
  basis_offset(1)=0
  do igr=1,ngrp
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMLEN(kpsystem,'POD-NMODE',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      call XABORT('SPOSTATE: INVALID POD MODE RECORD.')
    call LCMGET(kpsystem,'POD-NMODE',rank(igr))
    if ((rank(igr) <= 0).or.(rank(igr) > nsnap)) &
      call XABORT('SPOSTATE: INVALID POD MODE COUNT.')
    offset(igr+1)=offset(igr)+nsnap*rank(igr)
    gram_offset(igr+1)=gram_offset(igr)+rank(igr)*rank(igr)
    basis_offset(igr+1)=basis_offset(igr)+nreg2d*rank(igr)
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
    call XABORT('SPOSTATE: EMPTY SNAPSHOT HEIGHT.')

  gram_error=0.0_dp
  do igr=1,ngrp
    nmode=rank(igr)
    kpsystem=LCMGIL(jpsystem,igr)
    call LCMLEN(kpsystem,'NREG2D',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      call XABORT('SPOSTATE: INVALID NREG2D RECORD.')
    call LCMGET(kpsystem,'NREG2D',i)
    if (i /= nreg2d) call XABORT('SPOSTATE: RADIAL DIMENSION MISMATCH.')
    call LCMLEN(kpsystem,'NSNAP',ilong,itylcm)
    if ((ilong /= 1).or.(itylcm /= 1)) &
      call XABORT('SPOSTATE: INVALID NSNAP RECORD.')
    call LCMGET(kpsystem,'NSNAP',i)
    if (i /= nsnap) call XABORT('SPOSTATE: SNAPSHOT DIMENSION MISMATCH.')
    allocate(basis(nreg2d,nmode),vol2d(nreg2d))
    call LCMLEN(kpsystem,'POD-BASIS',ilong,itylcm)
    if ((ilong /= nreg2d*nmode).or.(itylcm /= 2)) &
      call XABORT('SPOSTATE: INVALID POD BASIS.')
    call LCMGET(kpsystem,'POD-BASIS',basis)
    basis_state(basis_offset(igr)+1:basis_offset(igr+1))= &
      reshape(basis,(/nreg2d*nmode/))
    call LCMLEN(kpsystem,'VOL2D',ilong,itylcm)
    if ((ilong /= nreg2d).or.(itylcm /= 2)) &
      call XABORT('SPOSTATE: INVALID POD VOLUME.')
    call LCMGET(kpsystem,'VOL2D',vol2d)
    if (any(.not.ieee_is_finite(basis)).or. &
        any(.not.ieee_is_finite(vol2d)).or.any(vol2d <= 0.0)) &
      call XABORT('SPOSTATE: NON-FINITE POD DATA.')
    do i=1,nreg2d
      if (transfer(vol2d(i),0) /= transfer(area(i),0)) &
        call XABORT('SPOSTATE: POD/AXIAL RADIAL VOLUME MISMATCH.')
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
        ! Match SPOPROJ's production restriction exactly: each product,
        ! accumulation, and division is performed in stored binary32 before
        ! the single global normalization and Gram projection.
        projected_sp=0.0
        weight_sp=0.0
        do ifloor=1,nfloor
          if (mat1d(ifloor) /= isnap) cycle
          ireg=(i-1)*nfloor+ifloor
          if (keyflx(ireg) <= 0) cycle
          projected_sp=projected_sp+volume(ireg)* &
            unknown(keyflx(ireg),igr)
          weight_sp=weight_sp+volume(ireg)
        enddo
        if (weight_sp <= 0.0) &
          call XABORT('SPOSTATE: EMPTY PLANE RESTRICTION.')
        projected_sp=projected_sp/weight_sp
        if ((.not.ieee_is_finite(projected_sp)).or. &
            (projected_sp <= 0.0)) &
          call XABORT('SPOSTATE: INVALID PLANE RESTRICTION.')
        plane(i)=real(projected_sp,dp)/norm
      enddo
      rhs=0.0_dp
      do a=1,nmode
        do i=1,nreg2d
          rhs(a)=rhs(a)+real(vol2d(i),dp)/weight_sum* &
            real(basis(i,a),dp)*plane(i)
        enddo
      enddo
      call solve_spd(gram,rhs,solution,nmode)
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
    call XABORT('SPOSTATE: NON-FINITE CANONICAL STATE.')

  version=1
  call LCMPUT(kentry(1),'SPOT-X-DIMS',4,1, &
    (/version,ngrp,nsnap,total_coef/))
  call LCMPUT(kentry(1),'SPOT-X-RANK',ngrp,1,rank)
  call LCMPUT(kentry(1),'SPOT-X-OFF',ngrp+1,1,offset)
  call LCMPUT(kentry(1),'SPOT-X-GOFF',ngrp+1,1,gram_offset)
  call LCMPUT(kentry(1),'SPOT-X-BOFF',ngrp+1,1,basis_offset)
  call LCMPUT(kentry(1),'SPOT-X-A',total_coef,4,coordinates)
  call LCMPUT(kentry(1),'SPOT-X-GRAM',total_gram,4,gram_flat)
  call LCMPUT(kentry(1),'SPOT-X-BASIS',total_basis,2,basis_state)
  call LCMPUT(kentry(1),'SPOT-X-RHO',1,4,rho)
  call LCMPUT(kentry(1),'SPOT-X-L',ngrp*nsnap,4,leak)
  call LCMPUT(kentry(1),'SPOT-X-H',nsnap,4,height)
  call LCMPUT(kentry(1),'SPOT-X-NORM',1,4,norm)
  call LCMPUT(kentry(1),'SPOT-X-PERP',ngrp*nsnap,4,offspace)
  call LCMPUT(kentry(1),'SPOT-X-GERR',1,4,gram_error)
  call LCMPUT(kentry(1),'SPOT-X-FIXB',1,1,fixb)
  norm_id='NUFISS-UNIT'
  call LCMPTC(kentry(1),'SPOT-X-NID',12,norm_id)
  call LCMPTC(kentry(1),'SPOT-X-BTYP',12,basis_type)

  write(6,'(A,I8,1P,4E13.5)') &
    'SPOSTATE NCOEF/RHO/NORM/PERP/GERR ',total_coef,rho,norm, &
    maxval(offspace),gram_error

  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOSTATE: ; CHARACTER EXPECTED.')

  deallocate(height,offspace,basis_state,gram_flat,coordinates)
  deallocate(basis_offset,gram_offset,offset,rank)
  deallocate(leak,denominator,numerator,leak_sp,current,phi)
  deallocate(nufis,unknown,volume,dz,area,mat1d,keyflx,mat)

contains

  subroutine require_record(object,name,length,type_code,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type

    call LCMLEN(object,name,actual_length,actual_type)
    if ((actual_length /= length).or.(actual_type /= type_code)) &
      call XABORT('SPOSTATE: INVALID '//trim(name)//' IN '//trim(owner)//'.')
  end subroutine require_record

  subroutine solve_spd(matrix,vector,result,n)
    integer, intent(in) :: n
    real(kind=dp), intent(in) :: matrix(n,n),vector(n)
    real(kind=dp), intent(out) :: result(n)
    real(kind=dp) :: lower(n,n),work(n),pivot
    integer :: row,col,k

    lower=0.0_dp
    do row=1,n
      do col=1,row
        pivot=matrix(row,col)
        do k=1,col-1
          pivot=pivot-lower(row,k)*lower(col,k)
        enddo
        if (row == col) then
          if ((.not.ieee_is_finite(pivot)).or.(pivot <= 0.0_dp)) &
            call XABORT('SPOSTATE: SINGULAR POD GRAM MATRIX.')
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
      call XABORT('SPOSTATE: NON-FINITE POD COORDINATE.')
  end subroutine solve_spd

end subroutine SPOSTATE
