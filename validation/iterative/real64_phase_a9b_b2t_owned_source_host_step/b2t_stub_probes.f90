module B2T_STUB_PROBES
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int64
  implicit none
  private

  integer, parameter, public :: B2T_NSNAP = 3
  integer, parameter, public :: B2T_EVENT_K = 10
  integer, parameter, public :: B2T_EVENT_N_BASE = 20
  integer, parameter, public :: B2T_EVENT_S = 30
  integer, parameter, public :: B2T_FAIL_NONE = 0
  integer, parameter, public :: B2T_FAIL_K = 1
  integer, parameter, public :: B2T_FAIL_N2 = 2
  integer, parameter, public :: B2T_FAIL_S = 3
  integer(int64), parameter, public :: B2T_FAIL_CUTOFF = &
      4294967297_int64
  integer(int64), parameter, public :: B2T_SUCCESS_CUTOFF(B2T_NSNAP) = &
      [4294967301_int64,4294967302_int64,4294967303_int64]

  integer, save, public :: failure_mode = B2T_FAIL_NONE
  integer, save, public :: event_count = 0
  integer, save, public :: events(8) = 0
  integer, save, public :: b2k_calls = 0
  integer, save, public :: b2n_calls = 0
  integer, save, public :: b2s_calls = 0
  integer, save, public :: private_identity_checks = 0
  integer, save, public :: replay_identity_checks = 0
  integer, save, public :: track_identity_checks = 0

  type(c_ptr), save, public :: expected_output = c_null_ptr
  type(c_ptr), save, public :: expected_projected = c_null_ptr
  type(c_ptr), save, public :: expected_systems(B2T_NSNAP) = c_null_ptr
  type(c_ptr), save, public :: expected_track_file = c_null_ptr
  type(c_ptr), save, public :: produced_assembled = c_null_ptr
  type(c_ptr), save, public :: produced_macros(B2T_NSNAP) = c_null_ptr
  type(c_ptr), save, public :: produced_sources(B2T_NSNAP) = c_null_ptr
  type(c_ptr), save, public :: replay_assembled = c_null_ptr
  type(c_ptr), save, public :: replay_macros(B2T_NSNAP) = c_null_ptr
  type(c_ptr), save, public :: replay_sources(B2T_NSNAP) = c_null_ptr

  public :: B2T_RESET_PROBES, B2T_REGISTER_CALL, B2T_REGISTER_REPLAYS
  public :: B2T_RECORD_EVENT, B2T_REQUIRE_SAME, B2T_REQUIRE_DISTINCT
  public :: B2T_REQUIRE_FRESH, B2T_PUT_MARKER, B2T_REQUIRE_MARKER

contains

  subroutine B2T_RESET_PROBES(requested_failure)
    integer, intent(in), optional :: requested_failure

    failure_mode = B2T_FAIL_NONE
    if (present(requested_failure)) failure_mode = requested_failure
    event_count = 0
    events = 0
    b2k_calls = 0
    b2n_calls = 0
    b2s_calls = 0
    private_identity_checks = 0
    replay_identity_checks = 0
    track_identity_checks = 0
    expected_output = c_null_ptr
    expected_projected = c_null_ptr
    expected_systems = c_null_ptr
    expected_track_file = c_null_ptr
    produced_assembled = c_null_ptr
    produced_macros = c_null_ptr
    produced_sources = c_null_ptr
    replay_assembled = c_null_ptr
    replay_macros = c_null_ptr
    replay_sources = c_null_ptr
  end subroutine B2T_RESET_PROBES


  subroutine B2T_REGISTER_CALL(ipout,ipprojected,ipsystems,iptrack_file)
    type(c_ptr), intent(in) :: ipout, ipprojected
    type(c_ptr), intent(in) :: ipsystems(B2T_NSNAP), iptrack_file

    expected_output = ipout
    expected_projected = ipprojected
    expected_systems = ipsystems
    expected_track_file = iptrack_file
  end subroutine B2T_REGISTER_CALL


  subroutine B2T_REGISTER_REPLAYS(assembled,macros,sources)
    type(c_ptr), intent(in) :: assembled
    type(c_ptr), intent(in) :: macros(B2T_NSNAP), sources(B2T_NSNAP)

    replay_assembled = assembled
    replay_macros = macros
    replay_sources = sources
  end subroutine B2T_REGISTER_REPLAYS


  subroutine B2T_RECORD_EVENT(code)
    integer, intent(in) :: code

    if (event_count >= size(events)) &
      error stop 'B2T stub event inventory overflow'
    event_count = event_count + 1
    events(event_count) = code
  end subroutine B2T_RECORD_EVENT


  subroutine B2T_REQUIRE_SAME(found,expected,context)
    type(c_ptr), intent(in) :: found, expected
    character(len=*), intent(in) :: context

    if (.not. c_associated(found,expected)) then
      write(*,'(A)') 'B2T stub identity mismatch: '//trim(context)
      error stop 'B2T stub identity mismatch'
    end if
  end subroutine B2T_REQUIRE_SAME


  subroutine B2T_REQUIRE_DISTINCT(left,right,context)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: context

    if (c_associated(left,right)) then
      write(*,'(A)') 'B2T stub unexpected alias: '//trim(context)
      error stop 'B2T stub unexpected alias'
    end if
  end subroutine B2T_REQUIRE_DISTINCT


  subroutine B2T_REQUIRE_FRESH(root,context)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: context
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    if (.not. c_associated(root)) then
      write(*,'(A)') 'B2T stub missing root: '//trim(context)
      error stop 'B2T stub missing root'
    end if
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') then
      write(*,'(A)') 'B2T stub nonfresh root: '//trim(context)
      error stop 'B2T stub nonfresh root'
    end if
  end subroutine B2T_REQUIRE_FRESH


  subroutine B2T_PUT_MARKER(root,value)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: value

    call LCMPUT(root,'B2T-MARK',1,1,value)
  end subroutine B2T_PUT_MARKER


  subroutine B2T_REQUIRE_MARKER(root,expected,context)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected
    character(len=*), intent(in) :: context
    integer :: found, length, record_type

    call LCMLEN(root,'B2T-MARK',length,record_type)
    if (length /= 1 .or. record_type /= 1) then
      write(*,'(A)') 'B2T stub marker schema mismatch: '//trim(context)
      error stop 'B2T stub marker schema mismatch'
    end if
    call LCMGET(root,'B2T-MARK',found)
    if (found /= expected) then
      write(*,'(A)') 'B2T stub marker value mismatch: '//trim(context)
      error stop 'B2T stub marker value mismatch'
    end if
  end subroutine B2T_REQUIRE_MARKER

end module B2T_STUB_PROBES
