module B2U_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  implicit none
  private

  integer, parameter, public :: B2U_NSNAP = 3
  integer, parameter, public :: B2U_REDGET_SEMICOLON = 0
  integer, parameter, public :: B2U_REDGET_BAD = 1
  integer, parameter, public :: B2U_B2T_SUCCESS = 0
  integer, parameter, public :: B2U_B2T_FAILURE = 1

  integer, save, public :: redget_mode = B2U_REDGET_SEMICOLON
  integer, save, public :: b2t_mode = B2U_B2T_SUCCESS
  integer, save, public :: redget_calls = 0
  integer, save, public :: b2t_calls = 0
  integer, save, public :: xabort_calls = 0
  integer, save, public :: system_identity_checks = 0
  integer, save, public :: track_identity_checks = 0
  character(len=72), save, public :: last_abort = ' '
  type(c_ptr), save, public :: expected_output = c_null_ptr
  type(c_ptr), save, public :: expected_projected = c_null_ptr
  type(c_ptr), save, public :: expected_systems(B2U_NSNAP) = c_null_ptr
  type(c_ptr), save, public :: expected_track = c_null_ptr

  public :: B2U_RESET, B2U_REGISTER_MEDIA, B2U_REQUIRE_SAME

contains

  subroutine B2U_RESET(requested_redget,requested_b2t)
    integer, intent(in), optional :: requested_redget, requested_b2t

    redget_mode = B2U_REDGET_SEMICOLON
    b2t_mode = B2U_B2T_SUCCESS
    if (present(requested_redget)) redget_mode = requested_redget
    if (present(requested_b2t)) b2t_mode = requested_b2t
    redget_calls = 0
    b2t_calls = 0
    xabort_calls = 0
    system_identity_checks = 0
    track_identity_checks = 0
    last_abort = ' '
    expected_output = c_null_ptr
    expected_projected = c_null_ptr
    expected_systems = c_null_ptr
    expected_track = c_null_ptr
  end subroutine B2U_RESET


  subroutine B2U_REGISTER_MEDIA(ipout,ipprojected,ipsystems,iptrack)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(B2U_NSNAP), iptrack

    expected_output = ipout
    expected_projected = ipprojected
    expected_systems = ipsystems
    expected_track = iptrack
  end subroutine B2U_REGISTER_MEDIA


  subroutine B2U_REQUIRE_SAME(found,expected,context)
    type(c_ptr), intent(in) :: found, expected
    character(len=*), intent(in) :: context

    if (.not. c_associated(found,expected)) then
      write(*,'(A)') 'B2U adapter identity mismatch: '//trim(context)
      error stop 'B2U adapter pointer identity mismatch'
    end if
  end subroutine B2U_REQUIRE_SAME

end module B2U_ADAPTER_PROBES
