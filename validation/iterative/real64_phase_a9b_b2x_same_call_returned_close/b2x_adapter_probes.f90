module B2X_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  implicit none
  private

  integer, parameter, public :: B2X_REDGET_SEMICOLON=1
  integer, parameter, public :: B2X_REDGET_BAD=2
  integer, parameter, public :: B2X_B2W_SUCCESS=1
  integer, parameter, public :: B2X_B2W_FAILURE=2
  integer, parameter, public :: B2X_ADMIT_SUCCESS=1
  integer, parameter, public :: B2X_ADMIT_FAILURE=2

  integer, public :: redget_calls=0
  integer, public :: b2w_calls=0
  integer, public :: admit_calls=0
  integer, public :: xabort_calls=0
  integer, public :: identity_checks=0
  integer, public :: redget_mode=B2X_REDGET_SEMICOLON
  integer, public :: b2w_mode=B2X_B2W_SUCCESS
  integer, public :: admit_mode=B2X_ADMIT_SUCCESS
  character(len=131), public :: last_abort=' '
  type(c_ptr), public :: expected_media(4)=c_null_ptr

  public :: B2X_RESET, B2X_REGISTER, B2X_REQUIRE_SAME

contains

  subroutine B2X_RESET(parser_mode,close_mode,admission_mode)
    integer, intent(in), optional :: parser_mode, close_mode, admission_mode

    redget_calls=0
    b2w_calls=0
    admit_calls=0
    xabort_calls=0
    identity_checks=0
    last_abort=' '
    expected_media=c_null_ptr
    redget_mode=B2X_REDGET_SEMICOLON
    b2w_mode=B2X_B2W_SUCCESS
    admit_mode=B2X_ADMIT_SUCCESS
    if (present(parser_mode)) redget_mode=parser_mode
    if (present(close_mode)) b2w_mode=close_mode
    if (present(admission_mode)) admit_mode=admission_mode
  end subroutine B2X_RESET


  subroutine B2X_REGISTER(media)
    type(c_ptr), intent(in) :: media(4)
    expected_media=media
  end subroutine B2X_REGISTER


  subroutine B2X_REQUIRE_SAME(found,expected,label)
    type(c_ptr), intent(in) :: found, expected
    character(len=*), intent(in) :: label

    if (.not. c_associated(found,expected)) then
      write(*,'(A)') 'B2X adapter pointer mismatch: '//trim(label)
      error stop 'B2X adapter pointer mismatch'
    end if
    identity_checks=identity_checks+1
  end subroutine B2X_REQUIRE_SAME

end module B2X_ADAPTER_PROBES
