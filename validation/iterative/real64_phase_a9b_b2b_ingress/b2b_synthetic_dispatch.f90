module B2B_SYNTHETIC_DISPATCH
  implicit none
  private

  abstract interface
    subroutine B2B_SYNTHETIC_CALLBACK(ok)
      logical, intent(out) :: ok
    end subroutine B2B_SYNTHETIC_CALLBACK
  end interface

  public :: B2B_DISPATCH
  public :: B2B_SYNTHETIC_CALLBACK

contains

  subroutine B2B_DISPATCH(requested, ingress_callback, legacy_callback, &
      selected, returned, ok)
    logical, intent(in) :: requested
    procedure(B2B_SYNTHETIC_CALLBACK) :: ingress_callback
    procedure(B2B_SYNTHETIC_CALLBACK) :: legacy_callback
    logical, intent(out) :: selected, returned, ok

    selected = .false.
    returned = .false.
    ok = .false.
    if (requested) then
      selected = .true.
      call ingress_callback(ok)
      returned = .true.
      return
    end if
    call legacy_callback(ok)
    returned = .true.
  end subroutine B2B_DISPATCH

end module B2B_SYNTHETIC_DISPATCH
