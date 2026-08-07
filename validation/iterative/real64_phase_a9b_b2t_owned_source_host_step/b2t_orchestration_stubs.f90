module SPOR64_B2K
  use, intrinsic :: iso_c_binding, only : c_ptr
  use B2T_STUB_PROBES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2K_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2K_ARCHIVE_ASSEMBLED = 2

  public :: SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE

contains

  subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(ipout,ipprojected, &
      ipsystems,status)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(B2T_NSNAP)
    integer, intent(out) :: status
    integer :: plane

    status = SPOR64_B2K_ADMISSION_FAILED
    b2k_calls = b2k_calls + 1
    if (b2k_calls /= 1 .or. event_count /= 0) &
      error stop 'B2T stub B2K call order differs'
    call B2T_RECORD_EVENT(B2T_EVENT_K)
    call B2T_REQUIRE_SAME(ipprojected,expected_projected, &
        'B2K PROJECTED input')
    do plane = 1, B2T_NSNAP
      call B2T_REQUIRE_SAME(ipsystems(plane),expected_systems(plane), &
          'B2K SYSTEM input')
    end do
    call B2T_REQUIRE_FRESH(ipout,'B2K private ASSEMBLED output')
    call B2T_REQUIRE_DISTINCT(ipout,expected_output, &
        'private ASSEMBLED versus caller output')
    call B2T_REQUIRE_DISTINCT(ipout,expected_projected, &
        'private ASSEMBLED versus PROJECTED')
    call B2T_REQUIRE_DISTINCT(ipout,expected_track_file, &
        'private ASSEMBLED versus TRACK_f')
    do plane = 1, B2T_NSNAP
      call B2T_REQUIRE_DISTINCT(ipout,expected_systems(plane), &
          'private ASSEMBLED versus SYSTEM')
    end do
    call B2T_REQUIRE_DISTINCT(ipout,replay_assembled, &
        'private ASSEMBLED versus replay candidate')

    if (failure_mode == B2T_FAIL_K) return
    call B2T_PUT_MARKER(ipout,100)
    produced_assembled = ipout
    status = SPOR64_B2K_ARCHIVE_ASSEMBLED
  end subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE

end module SPOR64_B2K


module SPOR64_B2N
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use B2T_STUB_PROBES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2N_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2N_COMMITTED = 2

  public :: SPOR64_B2N_BUILD

contains

  subroutine SPOR64_B2N_BUILD(ipprojected,plane_index,ipmacro_out, &
      ipsource_out,status)
    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out
    integer, intent(in) :: plane_index
    integer, intent(out) :: status
    integer :: plane

    status = SPOR64_B2N_PREFLIGHT_FAILED
    b2n_calls = b2n_calls + 1
    if (b2k_calls /= 1 .or. .not. c_associated(produced_assembled)) &
      error stop 'B2T stub B2N called without committed B2K'
    if (plane_index /= b2n_calls) &
      error stop 'B2T stub B2N plane order differs'
    call B2T_RECORD_EVENT(B2T_EVENT_N_BASE+plane_index)
    call B2T_REQUIRE_SAME(ipprojected,expected_projected, &
        'B2N PROJECTED input')
    call B2T_REQUIRE_FRESH(ipmacro_out,'B2N private MACRO0 output')
    call B2T_REQUIRE_FRESH(ipsource_out,'B2N private FSOURCE output')
    call B2T_REQUIRE_DISTINCT(ipmacro_out,ipsource_out, &
        'same-plane private source pair')
    call B2T_REQUIRE_DISTINCT(ipmacro_out,expected_output, &
        'private MACRO0 versus caller output')
    call B2T_REQUIRE_DISTINCT(ipsource_out,expected_output, &
        'private FSOURCE versus caller output')
    call B2T_REQUIRE_DISTINCT(ipmacro_out,produced_assembled, &
        'private MACRO0 versus private ASSEMBLED')
    call B2T_REQUIRE_DISTINCT(ipsource_out,produced_assembled, &
        'private FSOURCE versus private ASSEMBLED')
    do plane = 1, B2T_NSNAP
      call B2T_REQUIRE_DISTINCT(ipmacro_out,expected_systems(plane), &
          'private MACRO0 versus SYSTEM')
      call B2T_REQUIRE_DISTINCT(ipsource_out,expected_systems(plane), &
          'private FSOURCE versus SYSTEM')
      if (c_associated(produced_macros(plane))) then
        call B2T_REQUIRE_DISTINCT(ipmacro_out,produced_macros(plane), &
            'private MACRO0 cross-plane uniqueness')
        call B2T_REQUIRE_DISTINCT(ipsource_out,produced_macros(plane), &
            'private FSOURCE versus prior MACRO0')
      end if
      if (c_associated(produced_sources(plane))) then
        call B2T_REQUIRE_DISTINCT(ipmacro_out,produced_sources(plane), &
            'private MACRO0 versus prior FSOURCE')
        call B2T_REQUIRE_DISTINCT(ipsource_out,produced_sources(plane), &
            'private FSOURCE cross-plane uniqueness')
      end if
    end do

    if (failure_mode == B2T_FAIL_N2 .and. plane_index == 2) return
    call B2T_PUT_MARKER(ipmacro_out,100+plane_index)
    call B2T_PUT_MARKER(ipsource_out,200+plane_index)
    produced_macros(plane_index) = ipmacro_out
    produced_sources(plane_index) = ipsource_out
    status = SPOR64_B2N_COMMITTED
  end subroutine SPOR64_B2N_BUILD

end module SPOR64_B2N


module SPOR64_B2S
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  use B2T_STUB_PROBES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2S_DISABLED = 0
  integer, parameter, public :: SPOR64_B2S_FAILED = 1
  integer, parameter, public :: SPOR64_B2S_RETURNED = 2

  public :: SPOR64_B2S_HOST_BRIDGE

contains

  subroutine SPOR64_B2S_HOST_BRIDGE(ipout,ipassembled,ipmacros, &
      ipsources,iptrack_file,status,cutoff_by_plane,enable)
    type(c_ptr), intent(in) :: ipout, ipassembled
    type(c_ptr), intent(in) :: ipmacros(B2T_NSNAP)
    type(c_ptr), intent(in) :: ipsources(B2T_NSNAP), iptrack_file
    integer, intent(out) :: status
    integer(int64), intent(out) :: cutoff_by_plane(B2T_NSNAP)
    logical, intent(in), optional :: enable
    integer :: plane

    status = SPOR64_B2S_FAILED
    cutoff_by_plane = 0_int64
    b2s_calls = b2s_calls + 1
    if (b2s_calls /= 1 .or. b2k_calls /= 1 .or. &
        b2n_calls /= B2T_NSNAP) &
      error stop 'B2T stub B2S call inventory differs'
    if (.not. present(enable)) &
      error stop 'B2T stub B2S enable argument omitted'
    if (.not. enable) error stop 'B2T stub B2S was not enabled'
    call B2T_RECORD_EVENT(B2T_EVENT_S)
    call B2T_REQUIRE_SAME(ipout,expected_output,'B2S caller output')
    call B2T_REQUIRE_FRESH(ipout,'B2S fresh caller output')
    call B2T_REQUIRE_SAME(ipassembled,produced_assembled, &
        'B2S immediate B2K ASSEMBLED')
    private_identity_checks = private_identity_checks + 1
    call B2T_REQUIRE_DISTINCT(ipassembled,replay_assembled, &
        'B2S ASSEMBLED replay substitution')
    replay_identity_checks = replay_identity_checks + 1
    call B2T_REQUIRE_MARKER(ipassembled,100,'B2S ASSEMBLED marker')

    do plane = 1, B2T_NSNAP
      call B2T_REQUIRE_SAME(ipmacros(plane),produced_macros(plane), &
          'B2S immediate B2N MACRO0')
      private_identity_checks = private_identity_checks + 1
      call B2T_REQUIRE_SAME(ipsources(plane),produced_sources(plane), &
          'B2S immediate B2N FSOURCE')
      private_identity_checks = private_identity_checks + 1
      call B2T_REQUIRE_DISTINCT(ipmacros(plane),replay_macros(plane), &
          'B2S MACRO0 replay substitution')
      replay_identity_checks = replay_identity_checks + 1
      call B2T_REQUIRE_DISTINCT(ipsources(plane),replay_sources(plane), &
          'B2S FSOURCE replay substitution')
      replay_identity_checks = replay_identity_checks + 1
      call B2T_REQUIRE_MARKER(ipmacros(plane),100+plane, &
          'B2S MACRO0 marker')
      call B2T_REQUIRE_MARKER(ipsources(plane),200+plane, &
          'B2S FSOURCE marker')
    end do

    call B2T_REQUIRE_SAME(iptrack_file,expected_track_file, &
        'B2S TRACK_f descriptor')
    track_identity_checks = track_identity_checks + 1

    if (failure_mode == B2T_FAIL_S) then
      cutoff_by_plane(1) = B2T_FAIL_CUTOFF
      return
    end if
    cutoff_by_plane = B2T_SUCCESS_CUTOFF
    call B2T_PUT_MARKER(ipout,9001)
    status = SPOR64_B2S_RETURNED
  end subroutine SPOR64_B2S_HOST_BRIDGE

end module SPOR64_B2S
