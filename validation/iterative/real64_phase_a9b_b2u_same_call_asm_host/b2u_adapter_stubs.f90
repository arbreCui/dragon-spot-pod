module SPOR64_B2T
  use B2U_ADAPTER_PROBES
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  implicit none
  private

  integer, parameter, public :: SPOR64_B2T_DISABLED = 0
  integer, parameter, public :: SPOR64_B2T_FAILED = 1
  integer, parameter, public :: SPOR64_B2T_RETURNED = 2
  public :: SPOR64_B2T_HOST_STEP

contains

  subroutine SPOR64_B2T_HOST_STEP(ipout,ipprojected,ipsystems, &
      iptrack_file,status,cutoff_by_plane,enable)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(B2U_NSNAP), iptrack_file
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_by_plane(B2U_NSNAP)
    logical, intent(in), optional :: enable
    integer :: plane

    b2t_calls = b2t_calls+1
    if (b2t_calls /= 1) error stop 'B2U B2T stub call inventory differs'
    if (.not. present(enable)) error stop 'B2U B2T enable omitted'
    if (.not. enable) error stop 'B2U B2T enable is false'
    call B2U_REQUIRE_SAME(ipout,expected_output,'RETURNED output')
    call B2U_REQUIRE_SAME(ipprojected,expected_projected, &
        'PROJECTED input')
    do plane = 1, B2U_NSNAP
      call B2U_REQUIRE_SAME(ipsystems(plane),expected_systems(plane), &
          'ordered same-call SYSTEM')
      system_identity_checks = system_identity_checks+1
    end do
    call B2U_REQUIRE_SAME(iptrack_file,expected_track, &
        'current SPOR64T TRACK_f handle')
    track_identity_checks = track_identity_checks+1

    cutoff_by_plane = [4294967401_int64,4294967402_int64, &
        4294967403_int64]
    if (b2t_mode == B2U_B2T_FAILURE) then
      status = SPOR64_B2T_FAILED
    else
      status = SPOR64_B2T_RETURNED
    end if
  end subroutine SPOR64_B2T_HOST_STEP

end module SPOR64_B2T


subroutine REDGET(indic,nitma,flott,text,dflott)
  use B2U_ADAPTER_PROBES
  implicit none
  integer :: indic, nitma
  real :: flott
  character(len=*) :: text
  double precision :: dflott

  redget_calls = redget_calls+1
  if (redget_calls /= 1) error stop 'B2U REDGET call inventory differs'
  nitma = 0
  flott = 0.0
  dflott = 0.0d0
  indic = 3
  if (redget_mode == B2U_REDGET_BAD) then
    text = 'EDIT'
  else
    text = ';'
  end if
end subroutine REDGET


subroutine XABORT(message)
  use B2U_ADAPTER_PROBES
  implicit none
  character(len=*) :: message

  xabort_calls = xabort_calls+1
  last_abort = trim(message)
end subroutine XABORT
