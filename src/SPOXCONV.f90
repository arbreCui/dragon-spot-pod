!DECK SPOXCONV
subroutine SPOXCONV(nentry,hentry,ientry,jentry,kentry)
  ! Evaluate the raw fixed-space map defect between two canonical SPOSTATE
  ! records. If CURRENT=G(PREVIOUS), these values are the defect at PREVIOUS.
  !
  !   CURRENT := SPOXCONV: CURRENT PREVIOUS :: ;
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_fortran_env, only : int32,int64
  implicit none

  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)

  integer :: dims_c(4),dims_p(4),ngrp,nsnap,ncoef
  integer :: igr,isnap,a,b,nmode,index_a,index_b,index_g
  integer :: indic,nitma
  integer, allocatable :: rank_c(:),rank_p(:),off_c(:),off_p(:)
  integer, allocatable :: goff_c(:),goff_p(:),boff_c(:),boff_p(:)
  real, allocatable :: basis_c(:),basis_p(:)
  real :: flott
  real(kind=dp) :: dflott,rho_c,rho_p,r_rho,r_leak,r_a,d_leak
  real(kind=dp) :: leak_scale_c,leak_scale_p,leak_scale
  real(kind=dp) :: numerator,denominator,delta
  real(kind=dp), allocatable :: a_c(:),a_p(:),leak_c(:),leak_p(:)
  real(kind=dp), allocatable :: gram_c(:),gram_p(:),height_c(:),height_p(:)
  character(len=4) :: text4
  character(len=12) :: signature,norm_c,norm_p

  if (nentry /= 2) call XABORT('SPOXCONV: TWO ENTRIES EXPECTED.')
  if (any((ientry /= 1).and.(ientry /= 2))) &
    call XABORT('SPOXCONV: LCM ENTRIES EXPECTED.')
  if ((jentry(1) /= 1).or.(jentry(2) /= 2)) &
    call XABORT('SPOXCONV: MODIFIABLE CURRENT AND READ-ONLY PREVIOUS EXPECTED.')
  call LCMGTC(kentry(1),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOXCONV: CURRENT L_FLUX EXPECTED.')
  call LCMGTC(kentry(2),'SIGNATURE',12,signature)
  if (signature /= 'L_FLUX') call XABORT('SPOXCONV: PREVIOUS L_FLUX EXPECTED.')

  call require_record(kentry(1),'SPOT-X-DIMS',4,1,'CURRENT')
  call require_record(kentry(2),'SPOT-X-DIMS',4,1,'PREVIOUS')
  call LCMGET(kentry(1),'SPOT-X-DIMS',dims_c)
  call LCMGET(kentry(2),'SPOT-X-DIMS',dims_p)
  if (any(dims_c /= dims_p).or.(dims_c(1) /= 1)) &
    call XABORT('SPOXCONV: CANONICAL STATE DIMENSION MISMATCH.')
  ngrp=dims_c(2)
  nsnap=dims_c(3)
  ncoef=dims_c(4)
  if ((ngrp <= 0).or.(nsnap <= 0).or.(ncoef <= 0)) &
    call XABORT('SPOXCONV: INVALID CANONICAL STATE DIMENSIONS.')

  allocate(rank_c(ngrp),rank_p(ngrp))
  allocate(off_c(ngrp+1),off_p(ngrp+1))
  allocate(goff_c(ngrp+1),goff_p(ngrp+1))
  allocate(boff_c(ngrp+1),boff_p(ngrp+1))
  call require_record(kentry(1),'SPOT-X-RANK',ngrp,1,'CURRENT')
  call require_record(kentry(2),'SPOT-X-RANK',ngrp,1,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-OFF',ngrp+1,1,'CURRENT')
  call require_record(kentry(2),'SPOT-X-OFF',ngrp+1,1,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-GOFF',ngrp+1,1,'CURRENT')
  call require_record(kentry(2),'SPOT-X-GOFF',ngrp+1,1,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-BOFF',ngrp+1,1,'CURRENT')
  call require_record(kentry(2),'SPOT-X-BOFF',ngrp+1,1,'PREVIOUS')
  call LCMGET(kentry(1),'SPOT-X-RANK',rank_c)
  call LCMGET(kentry(2),'SPOT-X-RANK',rank_p)
  call LCMGET(kentry(1),'SPOT-X-OFF',off_c)
  call LCMGET(kentry(2),'SPOT-X-OFF',off_p)
  call LCMGET(kentry(1),'SPOT-X-GOFF',goff_c)
  call LCMGET(kentry(2),'SPOT-X-GOFF',goff_p)
  call LCMGET(kentry(1),'SPOT-X-BOFF',boff_c)
  call LCMGET(kentry(2),'SPOT-X-BOFF',boff_p)
  if (any(rank_c /= rank_p).or.any(rank_c <= 0).or. &
      any(off_c /= off_p).or.any(goff_c /= goff_p).or. &
      any(boff_c /= boff_p).or. &
      (off_c(1) /= 0).or.(goff_c(1) /= 0).or.(boff_c(1) /= 0).or. &
      (off_c(ngrp+1) /= ncoef)) &
    call XABORT('SPOXCONV: FIXED POD LAYOUT MISMATCH.')
  do igr=1,ngrp
    if (off_c(igr+1)-off_c(igr) /= nsnap*rank_c(igr)) &
      call XABORT('SPOXCONV: INVALID COORDINATE OFFSETS.')
    if (goff_c(igr+1)-goff_c(igr) /= rank_c(igr)*rank_c(igr)) &
      call XABORT('SPOXCONV: INVALID GRAM OFFSETS.')
    if (boff_c(igr+1) <= boff_c(igr)) &
      call XABORT('SPOXCONV: INVALID BASIS OFFSETS.')
  enddo
  allocate(basis_c(boff_c(ngrp+1)),basis_p(boff_c(ngrp+1)))
  call require_record(kentry(1),'SPOT-X-BASIS',boff_c(ngrp+1),2,'CURRENT')
  call require_record(kentry(2),'SPOT-X-BASIS',boff_c(ngrp+1),2,'PREVIOUS')
  call LCMGET(kentry(1),'SPOT-X-BASIS',basis_c)
  call LCMGET(kentry(2),'SPOT-X-BASIS',basis_p)
  if (any(.not.ieee_is_finite(basis_c)).or. &
      any(real32_bits(basis_c) /= real32_bits(basis_p))) &
    call XABORT('SPOXCONV: FIXED POD BASIS CHANGED.')

  allocate(a_c(ncoef),a_p(ncoef))
  allocate(leak_c(ngrp*nsnap),leak_p(ngrp*nsnap))
  allocate(height_c(nsnap),height_p(nsnap))
  allocate(gram_c(goff_c(ngrp+1)),gram_p(goff_c(ngrp+1)))
  call require_record(kentry(1),'SPOT-X-A',ncoef,4,'CURRENT')
  call require_record(kentry(2),'SPOT-X-A',ncoef,4,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-L',ngrp*nsnap,4,'CURRENT')
  call require_record(kentry(2),'SPOT-X-L',ngrp*nsnap,4,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-H',nsnap,4,'CURRENT')
  call require_record(kentry(2),'SPOT-X-H',nsnap,4,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-GRAM',goff_c(ngrp+1),4,'CURRENT')
  call require_record(kentry(2),'SPOT-X-GRAM',goff_c(ngrp+1),4,'PREVIOUS')
  call require_record(kentry(1),'SPOT-X-RHO',1,4,'CURRENT')
  call require_record(kentry(2),'SPOT-X-RHO',1,4,'PREVIOUS')
  call LCMGET(kentry(1),'SPOT-X-A',a_c)
  call LCMGET(kentry(2),'SPOT-X-A',a_p)
  call LCMGET(kentry(1),'SPOT-X-L',leak_c)
  call LCMGET(kentry(2),'SPOT-X-L',leak_p)
  call LCMGET(kentry(1),'SPOT-X-H',height_c)
  call LCMGET(kentry(2),'SPOT-X-H',height_p)
  call LCMGET(kentry(1),'SPOT-X-GRAM',gram_c)
  call LCMGET(kentry(2),'SPOT-X-GRAM',gram_p)
  call LCMGET(kentry(1),'SPOT-X-RHO',rho_c)
  call LCMGET(kentry(2),'SPOT-X-RHO',rho_p)
  if (any(.not.ieee_is_finite(a_c)).or. &
      any(.not.ieee_is_finite(a_p)).or. &
      any(.not.ieee_is_finite(leak_c)).or. &
      any(.not.ieee_is_finite(leak_p)).or. &
      any(.not.ieee_is_finite(height_c)).or.any(height_c <= 0.0_dp).or. &
      any(.not.ieee_is_finite(gram_c)).or. &
      (.not.ieee_is_finite(rho_c)).or.(rho_c <= 0.0_dp).or. &
      (.not.ieee_is_finite(rho_p)).or.(rho_p <= 0.0_dp)) &
    call XABORT('SPOXCONV: NON-FINITE CANONICAL STATE.')
  if (any(real64_bits(height_c) /= real64_bits(height_p)).or. &
      any(real64_bits(gram_c) /= real64_bits(gram_p))) &
    call XABORT('SPOXCONV: FIXED SPACE OR AXIAL HEIGHT CHANGED.')

  call require_record(kentry(1),'SPOT-X-NID',3,3,'CURRENT')
  call require_record(kentry(2),'SPOT-X-NID',3,3,'PREVIOUS')
  call LCMGTC(kentry(1),'SPOT-X-NID',12,norm_c)
  call LCMGTC(kentry(2),'SPOT-X-NID',12,norm_p)
  if ((norm_c /= 'NUFISS-UNIT').or.(norm_p /= norm_c)) &
    call XABORT('SPOXCONV: CANONICAL NORMALIZATION MISMATCH.')

  r_rho=abs(rho_c-rho_p)
  d_leak=maxval(abs(leak_c-leak_p))
  leak_scale_c=maxval(abs(leak_c))
  leak_scale_p=maxval(abs(leak_p))
  leak_scale=max(leak_scale_c,leak_scale_p)
  if (leak_scale == 0.0_dp) then
    if (d_leak /= 0.0_dp) &
      call XABORT('SPOXCONV: INVALID ZERO-LEAKAGE BRANCH.')
    r_leak=0.0_dp
  else
    r_leak=d_leak/leak_scale
  endif

  numerator=0.0_dp
  denominator=0.0_dp
  do igr=1,ngrp
    nmode=rank_c(igr)
    do isnap=1,nsnap
      do a=1,nmode
        index_a=off_c(igr)+(isnap-1)*nmode+a
        delta=a_c(index_a)-a_p(index_a)
        do b=1,nmode
          index_b=off_c(igr)+(isnap-1)*nmode+b
          index_g=goff_c(igr)+(b-1)*nmode+a
          numerator=numerator+height_c(isnap)*delta* &
            gram_c(index_g)*(a_c(index_b)-a_p(index_b))
          denominator=denominator+height_c(isnap)*a_c(index_a)* &
            gram_c(index_g)*a_c(index_b)
        enddo
      enddo
    enddo
  enddo
  if ((.not.ieee_is_finite(numerator)).or.(numerator < 0.0_dp).or. &
      (.not.ieee_is_finite(denominator)).or.(denominator <= 0.0_dp)) &
    call XABORT('SPOXCONV: INVALID COORDINATE NORM.')
  r_a=sqrt(numerator/denominator)
  if ((.not.ieee_is_finite(r_rho)).or. &
      (.not.ieee_is_finite(r_leak)).or. &
      (.not.ieee_is_finite(r_a))) &
    call XABORT('SPOXCONV: NON-FINITE MAP DEFECT.')

  call LCMPUT(kentry(1),'SPOT-X-RRHO',1,4,r_rho)
  call LCMPUT(kentry(1),'SPOT-X-RLEAK',1,4,r_leak)
  call LCMPUT(kentry(1),'SPOT-X-DLEAK',1,4,d_leak)
  call LCMPUT(kentry(1),'SPOT-X-RA',1,4,r_a)
  write(6,'(A,1P,4E24.16)') &
    'SPOXCONV RRHO/RLEAK/DLEAK/RA ',r_rho,r_leak,d_leak,r_a

  call REDGET(indic,nitma,flott,text4,dflott)
  if ((indic /= 3).or.(text4 /= ';')) &
    call XABORT('SPOXCONV: ; CHARACTER EXPECTED.')

  deallocate(gram_p,gram_c,height_p,height_c)
  deallocate(leak_p,leak_c,a_p,a_c)
  deallocate(basis_p,basis_c)
  deallocate(boff_p,boff_c,goff_p,goff_c,off_p,off_c,rank_p,rank_c)

contains

  pure elemental integer(int32) function real32_bits(value)
    real, intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits

  pure elemental integer(int64) function real64_bits(value)
    real(kind=dp), intent(in) :: value

    real64_bits=transfer(value,0_int64)
  end function real64_bits

  subroutine require_record(object,name,length,type_code,owner)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type

    call LCMLEN(object,name,actual_length,actual_type)
    if ((actual_length /= length).or.(actual_type /= type_code)) &
      call XABORT('SPOXCONV: INVALID '//trim(name)//' IN '//trim(owner)//'.')
  end subroutine require_record

end subroutine SPOXCONV
