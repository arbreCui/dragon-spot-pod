subroutine COMPILE_FAIL_NONLOGICAL_SELECTOR()
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A9_HOST, only : SPOR64_A9_DISPATCH
  implicit none

  integer :: requested
  logical :: route_ok, selected_real64
  real(real64) :: state64(1)

  requested = 1
  state64 = +0.0_real64
  call SPOR64_A9_DISPATCH(requested, state64, LEGACY_CALLBACK, &
      REAL64_CALLBACK, selected_real64, route_ok)

contains

  subroutine LEGACY_CALLBACK(ok)
    logical, intent(inout) :: ok
    ok = .true.
  end subroutine LEGACY_CALLBACK

  subroutine REAL64_CALLBACK(state, ok)
    real(real64), intent(inout), contiguous :: state(:)
    logical, intent(inout) :: ok
    state = state + 1.0_real64
    ok = .true.
  end subroutine REAL64_CALLBACK

end subroutine COMPILE_FAIL_NONLOGICAL_SELECTOR
