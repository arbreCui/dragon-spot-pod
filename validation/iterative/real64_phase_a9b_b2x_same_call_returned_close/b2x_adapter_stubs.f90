module SPOR64_B2W
  use B2X_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_ptr
  implicit none
  private

  integer, parameter, public :: SPOR64_B2W_PREFLIGHT_FAILED=1
  integer, parameter, public :: SPOR64_B2W_CLOSED=2
  integer, parameter, public :: SPOR64_B2W_RETURNED_ADMITTED=3
  public :: SPOR64_B2W_ADMIT_RETURNED, SPOR64_B2W_CLOSE

contains

  subroutine SPOR64_B2W_ADMIT_RETURNED(ipfeedback,status)
    type(c_ptr), intent(in) :: ipfeedback
    integer, intent(out) :: status

    admit_calls=admit_calls+1
    if (admit_calls /= 1) error stop 'B2X admission stub count differs'
    call B2X_REQUIRE_SAME(ipfeedback,expected_media(4), &
        'returned admission FEEDBACK')
    if (admit_mode == B2X_ADMIT_FAILURE) then
      status=SPOR64_B2W_PREFLIGHT_FAILED
    else
      status=SPOR64_B2W_RETURNED_ADMITTED
    end if
  end subroutine SPOR64_B2W_ADMIT_RETURNED

  subroutine SPOR64_B2W_CLOSE(ipaxout,iparchiveout,ipax,ipfeedback,status)
    type(c_ptr), intent(in) :: ipaxout, iparchiveout, ipax, ipfeedback
    integer, intent(out) :: status
    type(c_ptr) :: actual(4)
    integer :: index

    b2w_calls=b2w_calls+1
    if (b2w_calls /= 1) error stop 'B2X B2W stub call count differs'
    actual=[ipaxout,iparchiveout,ipax,ipfeedback]
    do index=1,4
      call B2X_REQUIRE_SAME(actual(index),expected_media(index), &
          'ordered B2W medium')
    end do
    if (b2w_mode == B2X_B2W_FAILURE) then
      status=SPOR64_B2W_PREFLIGHT_FAILED
    else
      status=SPOR64_B2W_CLOSED
    end if
  end subroutine SPOR64_B2W_CLOSE

end module SPOR64_B2W


subroutine REDGET(indic,nitma,flott,text,dflott)
  use B2X_ADAPTER_PROBES
  implicit none
  integer :: indic, nitma
  real :: flott
  character(len=*) :: text
  double precision :: dflott

  redget_calls=redget_calls+1
  if (redget_calls /= 1) error stop 'B2X adapter REDGET count differs'
  nitma=0
  flott=0.0
  dflott=0.0d0
  indic=3
  if (redget_mode == B2X_REDGET_BAD) then
    text='EDIT'
  else
    text=';'
  end if
end subroutine REDGET


subroutine XABORT(message)
  use B2X_ADAPTER_PROBES
  implicit none
  character(len=*) :: message

  xabort_calls=xabort_calls+1
  last_abort=trim(message)
end subroutine XABORT
