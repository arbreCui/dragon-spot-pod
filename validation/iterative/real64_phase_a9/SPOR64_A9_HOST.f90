module SPOR64_A9_HOST
  use, intrinsic :: iso_fortran_env, only : real32, real64
  implicit none
  private

  logical, parameter, public :: DEFAULT_REAL64_ROUTE = .false.
  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  abstract interface
    subroutine SPOR64_A9_LEGACY_CALLBACK_IFACE(ok)
      logical, intent(inout) :: ok
    end subroutine SPOR64_A9_LEGACY_CALLBACK_IFACE

    subroutine SPOR64_A9_REAL64_CALLBACK_IFACE(state64, ok)
      import :: real64
      real(real64), intent(inout), contiguous :: state64(:)
      logical, intent(inout) :: ok
    end subroutine SPOR64_A9_REAL64_CALLBACK_IFACE
  end interface

  public :: SPOR64_A9_LEGACY_CALLBACK_IFACE
  public :: SPOR64_A9_REAL64_CALLBACK_IFACE
  public :: SPOR64_A9_DISPATCH
  public :: SPOR64_A9_SELECTOR_PROBE

contains

  subroutine SPOR64_A9_DISPATCH(requested, state64, legacy_callback, &
      real64_callback, selected_real64, route_ok)
    logical, intent(in) :: requested
    real(real64), intent(inout), contiguous :: state64(:)
    procedure(SPOR64_A9_LEGACY_CALLBACK_IFACE) :: legacy_callback
    procedure(SPOR64_A9_REAL64_CALLBACK_IFACE) :: real64_callback
    logical, intent(out) :: selected_real64, route_ok

    selected_real64 = DEFAULT_REAL64_ROUTE
    route_ok = .false.
    if (requested) selected_real64 = .true.

    if (selected_real64) then
      call real64_callback(state64, route_ok)
      return
    end if

    call legacy_callback(route_ok)
  end subroutine SPOR64_A9_DISPATCH


  subroutine SPOR64_A9_SELECTOR_PROBE(state64, default_selected, &
      real32_kind_value, real64_kind_value)
    real(real64), intent(in), contiguous :: state64(:)
    logical, intent(out) :: default_selected
    integer, intent(out) :: real32_kind_value, real64_kind_value

    default_selected = DEFAULT_REAL64_ROUTE
    real32_kind_value = kind(1.0) * kind_guard
    real64_kind_value = kind(state64) * kind_guard
  end subroutine SPOR64_A9_SELECTOR_PROBE

end module SPOR64_A9_HOST
