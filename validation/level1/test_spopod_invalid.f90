program test_spopod_invalid
  use, intrinsic :: iso_fortran_env, only : error_unit
  use, intrinsic :: ieee_arithmetic, only : ieee_value, &
    ieee_quiet_nan,ieee_positive_inf
  implicit none
  integer, parameter :: dp=kind(1.0d0)
  integer :: nreg2d,nsnap,rank_req,nmode
  character(32) :: case_name,entry_name
  real(dp), allocatable :: phi(:,:),vol(:),sigma(:)
  real, allocatable :: basis(:,:),coeff(:,:)
  real(dp) :: rec_err,ortho_err

  call get_command_argument(1,case_name)
  call get_command_argument(2,entry_name)
  nreg2d=3
  nsnap=2
  rank_req=0
  if (case_name=='dimensions') nreg2d=0
  if (case_name=='snapshot_shape') nsnap=4
  allocate(phi(nreg2d,nsnap),vol(nreg2d),sigma(nsnap))
  allocate(basis(nreg2d,nsnap),coeff(nsnap,nsnap))
  phi=1.0_dp
  vol=1.0_dp
  select case(case_name)
  case('nan_phi')
    phi(1,1)=ieee_value(1.0_dp,ieee_quiet_nan)
  case('inf_phi')
    phi(1,1)=ieee_value(1.0_dp,ieee_positive_inf)
  case('nan_vol')
    vol(1)=ieee_value(1.0_dp,ieee_quiet_nan)
  case('inf_vol')
    vol(1)=ieee_value(1.0_dp,ieee_positive_inf)
  case('zero_vol')
    vol(1)=0.0_dp
  case('negative_vol')
    vol(1)=-1.0_dp
  case('zero_flux')
    phi(:,1)=0.0_dp
  case('negative_rank')
    rank_req=-1
  case('dimensions','snapshot_shape')
    ! Rejected before normalization or the SVD.
  case default
    write(error_unit,'(a)') 'Unknown invalid-input test.'
    error stop 1
  end select
  if (entry_name=='legacy') then
    call SPOPOD(nreg2d,nsnap,real(phi),real(vol),rank_req,nmode, &
                basis,coeff,sigma,rec_err,ortho_err,0,1)
  else if (entry_name=='real64') then
    call SPOPOD64(nreg2d,nsnap,phi,vol,rank_req,nmode, &
                  basis,coeff,sigma,rec_err,ortho_err,0,1)
  else
    write(error_unit,'(a)') 'Unknown POD entry.'
    error stop 1
  endif
  write(error_unit,'(a)') 'Invalid input was unexpectedly accepted.'
  error stop 1
end program test_spopod_invalid

subroutine XABORT(message)
  character(*), intent(in) :: message
  write(*,'(a)') 'XABORT: '//message
  error stop 2
end subroutine XABORT
