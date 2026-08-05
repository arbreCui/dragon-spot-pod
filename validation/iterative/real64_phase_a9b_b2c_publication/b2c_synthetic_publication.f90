module B2C_SYNTHETIC_PUBLICATION
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  private

  integer, parameter, public :: B2C_SYNTHETIC_PREFLIGHT_FAILED = 5
  integer, parameter, public :: B2C_SYNTHETIC_CHILD_PUBLISHED = 6
  integer, parameter, public :: B2C_SYNTHETIC_DRIVER_COMMITTED = 7
  integer, parameter, public :: B2C_SYNTHETIC_HOST_COMMITTED = 8
  integer, parameter, public :: B2C_SYNTHETIC_ACCEPTED_TOKEN = 4
  integer, parameter, public :: B2C_NUNKNO = 14
  integer, parameter, public :: B2C_NGRP = 370
  integer, parameter, public :: B2C_COLLISIONS = 5
  integer, parameter, public :: B2C_LEDGER_SIZE = 13

  integer, parameter, public :: B2C_EVENT_AUTHORITY_DIRECTORY = 1
  integer, parameter, public :: B2C_EVENT_AUTHORITY_FLUX = 2
  integer, parameter, public :: B2C_EVENT_AUTHORITY_SOURCE = 3
  integer, parameter, public :: B2C_EVENT_LEGACY_FLUX = 4
  integer, parameter, public :: B2C_EVENT_LEGACY_SOURCE = 5
  integer, parameter, public :: B2C_EVENT_STATE_VECTOR = 6
  integer, parameter, public :: B2C_EVENT_EPS_CONVERGE = 7
  integer, parameter, public :: B2C_EVENT_KEYFLX = 8
  integer, parameter, public :: B2C_EVENT_OPTION = 9
  integer, parameter, public :: B2C_EVENT_LINK_MACRO = 10
  integer, parameter, public :: B2C_EVENT_LINK_TRACK = 11
  integer, parameter, public :: B2C_EVENT_LINK_SYSTEM = 12
  integer, parameter, public :: B2C_EVENT_LEAK1D = 13

  public :: B2C_SYNTHETIC_PUBLISH

contains

  subroutine B2C_SYNTHETIC_PUBLISH(accepted_token,collisions, &
      terminal_flux64,terminal_source64,status,ledger,ledger_length, &
      status_trace,status_trace_length,conversion_count, &
      authority_flux64,authority_source64,legacy_flux32,legacy_source32)
    integer, intent(in) :: accepted_token
    logical, intent(in) :: collisions(B2C_COLLISIONS)
    real(real64), intent(in) :: terminal_flux64(B2C_NUNKNO,B2C_NGRP)
    real(real64), intent(in) :: terminal_source64(B2C_NUNKNO,B2C_NGRP)
    integer, intent(out) :: status
    integer, intent(inout) :: ledger(B2C_LEDGER_SIZE)
    integer, intent(out) :: ledger_length
    integer, intent(inout) :: status_trace(3)
    integer, intent(out) :: status_trace_length
    integer(int64), intent(out) :: conversion_count
    real(real64), intent(inout) :: authority_flux64(B2C_NUNKNO,B2C_NGRP)
    real(real64), intent(inout) :: authority_source64(B2C_NUNKNO,B2C_NGRP)
    real(real32), intent(inout) :: legacy_flux32(B2C_NUNKNO,B2C_NGRP)
    real(real32), intent(inout) :: legacy_source32(B2C_NUNKNO,B2C_NGRP)

    integer :: ig, iu
    real(real64), parameter :: real32_max64 = &
        real(huge(0.0_real32),real64)
    real(real32) :: flux_stage32(B2C_NUNKNO,B2C_NGRP)
    real(real32) :: source_stage32(B2C_NUNKNO,B2C_NGRP)

    status = B2C_SYNTHETIC_PREFLIGHT_FAILED
    ledger_length = 0
    status_trace_length = 0
    conversion_count = 0_int64

    ! This validation-owned state machine models only the publication ledger.
    ! Every rejection occurs before touching any caller-owned payload.
    if (accepted_token /= B2C_SYNTHETIC_ACCEPTED_TOKEN) return
    if (any(collisions)) return
    if (.not. all(ieee_is_finite(terminal_flux64))) return
    if (.not. all(ieee_is_finite(terminal_source64))) return
    if (any(abs(terminal_flux64) > real32_max64)) return
    if (any(abs(terminal_source64) > real32_max64)) return

    call append_event(B2C_EVENT_AUTHORITY_DIRECTORY)
    authority_flux64 = terminal_flux64
    call append_event(B2C_EVENT_AUTHORITY_FLUX)
    authority_source64 = terminal_source64
    call append_event(B2C_EVENT_AUTHORITY_SOURCE)

    ! One scalar conversion per terminal value, in one forward-only pass.
    do ig = 1, B2C_NGRP
      do iu = 1, B2C_NUNKNO
        flux_stage32(iu,ig) = real(terminal_flux64(iu,ig),real32)
        conversion_count = conversion_count + 1_int64
        source_stage32(iu,ig) = real(terminal_source64(iu,ig),real32)
        conversion_count = conversion_count + 1_int64
      end do
    end do
    legacy_flux32 = flux_stage32
    call append_event(B2C_EVENT_LEGACY_FLUX)
    legacy_source32 = source_stage32
    call append_event(B2C_EVENT_LEGACY_SOURCE)
    call append_status(B2C_SYNTHETIC_CHILD_PUBLISHED)

    call append_event(B2C_EVENT_STATE_VECTOR)
    call append_event(B2C_EVENT_EPS_CONVERGE)
    call append_event(B2C_EVENT_KEYFLX)
    call append_event(B2C_EVENT_OPTION)
    call append_status(B2C_SYNTHETIC_DRIVER_COMMITTED)

    call append_event(B2C_EVENT_LINK_MACRO)
    call append_event(B2C_EVENT_LINK_TRACK)
    call append_event(B2C_EVENT_LINK_SYSTEM)
    call append_event(B2C_EVENT_LEAK1D)
    call append_status(B2C_SYNTHETIC_HOST_COMMITTED)

  contains

    subroutine append_event(event)
      integer, intent(in) :: event

      ledger_length = ledger_length + 1
      ledger(ledger_length) = event
    end subroutine append_event


    subroutine append_status(next_status)
      integer, intent(in) :: next_status

      status = next_status
      status_trace_length = status_trace_length + 1
      status_trace(status_trace_length) = next_status
    end subroutine append_status

  end subroutine B2C_SYNTHETIC_PUBLISH

end module B2C_SYNTHETIC_PUBLICATION
