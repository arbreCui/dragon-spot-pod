program B2B_SYNTHETIC_DISPATCH_DRIVER
  use B2B_SYNTHETIC_DISPATCH, only : B2B_DISPATCH
  implicit none

  integer :: event_count, events(4), ingress_count, legacy_count
  logical :: ok, returned, selected
  character(len=24) :: scenario

  event_count = 0
  events = 0
  ingress_count = 0
  legacy_count = 0
  scenario = ''
  call get_command_argument(1, scenario)

  select case (trim(scenario))
  case ('off')
    call B2B_DISPATCH(.false., INGRESS_STUB, LEGACY_STUB, selected, &
        returned, ok)
    if (selected .or. .not. returned .or. .not. ok) error stop 11
    if (ingress_count /= 0 .or. legacy_count /= 1) error stop 12
    if (event_count /= 1 .or. any(events(1:1) /= [9])) error stop 13
  case ('selected')
    call B2B_DISPATCH(.true., INGRESS_STUB, LEGACY_STUB, selected, &
        returned, ok)
    if (.not. selected .or. .not. returned .or. .not. ok) error stop 21
    if (ingress_count /= 1 .or. legacy_count /= 0) error stop 22
    if (event_count /= 3 .or. any(events(1:3) /= [1,2,3])) error stop 23
  case ('admission-fail')
    call B2B_DISPATCH(.true., INGRESS_STUB, LEGACY_STUB, selected, &
        returned, ok)
    if (.not. selected .or. .not. returned .or. ok) error stop 31
    if (ingress_count /= 1 .or. legacy_count /= 0) error stop 32
    if (event_count /= 1 .or. any(events(1:1) /= [4])) error stop 33
  case ('core-fail')
    call B2B_DISPATCH(.true., INGRESS_STUB, LEGACY_STUB, selected, &
        returned, ok)
    if (.not. selected .or. .not. returned .or. ok) error stop 41
    if (ingress_count /= 1 .or. legacy_count /= 0) error stop 42
    if (event_count /= 3 .or. any(events(1:3) /= [1,2,3])) error stop 43
  case default
    error stop 90
  end select

  write(*,'(A,1X,A)') 'B2B-DISPATCH-PASS', trim(scenario)

contains

  subroutine APPEND_EVENT(value)
    integer, intent(in) :: value
    event_count = event_count + 1
    if (event_count > size(events)) error stop 91
    events(event_count) = value
  end subroutine APPEND_EVENT

  subroutine INGRESS_STUB(callback_ok)
    logical, intent(out) :: callback_ok
    ingress_count = ingress_count + 1
    select case (trim(scenario))
    case ('admission-fail')
      call APPEND_EVENT(4)
      callback_ok = .false.
      return
    case ('selected')
      call APPEND_EVENT(1)
      call APPEND_EVENT(2)
      call APPEND_EVENT(3)
      callback_ok = .true.
    case ('core-fail')
      call APPEND_EVENT(1)
      call APPEND_EVENT(2)
      call APPEND_EVENT(3)
      callback_ok = .false.
    case default
      error stop 92
    end select
  end subroutine INGRESS_STUB

  subroutine LEGACY_STUB(callback_ok)
    logical, intent(out) :: callback_ok
    legacy_count = legacy_count + 1
    call APPEND_EVENT(9)
    callback_ok = .true.
  end subroutine LEGACY_STUB

end program B2B_SYNTHETIC_DISPATCH_DRIVER
