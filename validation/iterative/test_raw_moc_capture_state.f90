program test_raw_moc_capture_state
  use, intrinsic :: iso_c_binding, only: c_ptr, c_associated
  use, intrinsic :: iso_fortran_env, only: int32, int64, real32, real64
  use GANLIB
  use SPOMOC_AUDIT
  implicit none

  integer, parameter :: ng = 370
  integer, parameter :: nu = 14
  type(c_ptr) :: ipflux
  integer :: ngind(ng)
  logical :: nconv(ng)
  real(real32) :: qfr(nu, ng), eval(nu, ng), epsilon
  real(real64) :: source(nu, ng), raw(nu, ng)
  character(len=32) :: mode
  integer :: i, j

  mode = 'valid'
  if (command_argument_count() == 1) call get_command_argument(1, mode)
  if (command_argument_count() > 1) error stop 'one mode expected'

  epsilon = transfer(int(z'348637BD', int32), 0.0_real32)
  do i = 1, ng
    ngind(i) = i
    nconv(i) = .true.
    do j = 1, nu
      qfr(j, i) = real(1000 + 17*i + j, real32) * 2.0_real32**(-20)
      eval(j, i) = real(2000 + 19*i + j, real32) * 2.0_real32**(-19)
      source(j, i) = real(qfr(j, i), real64) + &
           0.25_real64 * real(eval(j, i), real64)
      raw(j, i) = source(j, i) + &
           real(31*i + j, real64) * 2.0_real64**(-42)
    end do
  end do

  call LCMOP(ipflux, 'SPOMOC-TEST', 0, 1, 0)
  if (.not. c_associated(ipflux)) error stop 'LCMOP failed'

  select case (trim(mode))
  case ('off')
    call begin_capture(ipflux, 0)
    call SPOMOC_FLU_PATH(.false.)
    call SPOMOC_FLU_CONTEXT(1, 1)
    call SPOMOC_DOOR_BEGIN()
    call SPOMOC_MCCGF_BEGIN(ng, ng, ngind, nu, 2, .false., nu, 8, 6, &
         1, 1, 1, 10, 1, 80, 0, 0, 4, 0)
    call SPOMOC_SET_ROLE(1, 1)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    call SPOMOC_PUBLISH()
    call SPOMOC_FINISH()
    call require_absent(ipflux)
    write(*, '(A)') 'RAW-MOC-STATE OFF PASS'
  case ('valid')
    call begin_capture(ipflux, 1)
    call enter_mccgf()
    call SPOMOC_SET_ROLE(2, 1)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    call require_empty_first_group(ipflux)
    call SPOMOC_SET_ROLE(3, 2)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    call require_empty_first_group(ipflux)
    call SPOMOC_SET_ROLE(1, 1)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    call SPOMOC_PUBLISH()
    call require_complete(ipflux, 1)
    call SPOMOC_SET_ROLE(1, 2)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, &
         source + 1.0_real64, raw + 1.0_real64, nconv)
    call SPOMOC_SET_ROLE(2, 2)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, &
         source + 2.0_real64, raw + 2.0_real64, nconv)
    call require_complete(ipflux, 1)
    call SPOMOC_FINISH()
    if (SPOMOC_ACTIVE()) error stop 'active after FINISH'
    write(*, '(A)') 'RAW-MOC-STATE VALID PASS'
  case ('duplicate')
    call begin_capture(ipflux, 1)
    call begin_capture(ipflux, 1)
    error stop 'duplicate BEGIN accepted'
  case ('wrong-path')
    call begin_capture(ipflux, 1)
    call SPOMOC_FLU_PATH(.true.)
    error stop 'scalar path accepted'
  case ('partial-publish')
    call begin_capture(ipflux, 1)
    call enter_mccgf()
    call SPOMOC_SET_ROLE(1, 1)
    call SPOMOC_PUBLISH()
    error stop 'partial publication accepted'
  case ('wrong-step')
    call begin_capture(ipflux, 1)
    call enter_mccgf()
    call SPOMOC_SET_ROLE(1, 2)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    error stop 'wrong primary step accepted'
  case ('overwrite')
    call begin_capture(ipflux, 1)
    call enter_mccgf()
    call SPOMOC_SET_ROLE(1, 1)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    call SPOMOC_CAPTURE(ng, ngind, nu, qfr, eval, source, raw, nconv)
    error stop 'primary overwrite accepted'
  case default
    error stop 'unknown mode'
  end select

  call LCMCL(ipflux, 2)

contains

  subroutine begin_capture(owner, arm)
    type(c_ptr), intent(in) :: owner
    integer, intent(in) :: arm

    call SPOMOC_BEGIN(owner, arm, 'MCCG', 0, ng, nu, 8, 1, 740, &
         epsilon, epsilon, epsilon, .true., 0, .true., 1, 1, 0)
  end subroutine begin_capture


  subroutine enter_mccgf()
    call SPOMOC_FLU_PATH(.false.)
    call SPOMOC_FLU_CONTEXT(1, 1)
    call SPOMOC_DOOR_BEGIN()
    call SPOMOC_MCCGF_BEGIN(ng, ng, ngind, nu, 2, .false., nu, 8, 6, &
         1, 1, 1, 10, 1, 80, 0, 0, 4, 0)
  end subroutine enter_mccgf


  subroutine require_absent(owner)
    type(c_ptr), intent(in) :: owner
    integer :: ilong, itype

    call LCMLEN(owner, 'SPOT-MOC-AUD', ilong, itype)
    if (ilong /= 0) error stop 'OFF created audit directory'
  end subroutine require_absent


  subroutine require_empty_first_group(owner)
    type(c_ptr), intent(in) :: owner
    type(c_ptr) :: audit, groups
    integer :: ilong, itype

    audit = LCMGID(owner, 'SPOT-MOC-AUD')
    groups = LCMGID(audit, 'GROUP')
    call LCMLEL(groups, 1, ilong, itype)
    if ((ilong == -1) .and. (itype == 0)) &
         error stop 'excluded role wrote a group tuple'
  end subroutine require_empty_first_group


  subroutine require_complete(owner, arm)
    type(c_ptr), intent(in) :: owner
    type(c_ptr) :: audit, groups, group_dir
    integer, intent(in) :: arm
    integer :: state(24), expected(24), ordered(ng)
    integer :: ilong, itype, group_id(1), role(1), step(1)
    real(real64) :: values(nu)
    integer :: ig

    audit = LCMGID(owner, 'SPOT-MOC-AUD')
    call LCMGET(audit, 'STATE-VECTOR', state)
    expected = [1, 1, arm, 1, 1, 1, 1, 1, 1, 1, 1, 1, &
         10, 1, 80, 0, 0, 4, 0, ng, ng, nu, 8, ng]
    if (any(state /= expected)) error stop 'STATE-VECTOR differs'
    call LCMGET(audit, 'NGIND', ordered)
    if (any(ordered /= ngind)) error stop 'NGIND differs'
    call LCMLEN(audit, 'GROUP', ilong, itype)
    if ((ilong /= ng) .or. (itype /= 10)) &
         error stop 'GROUP metadata differs'
    groups = LCMGID(audit, 'GROUP')
    do ig = 1, ng
      call LCMLEL(groups, ig, ilong, itype)
      if ((ilong /= -1) .or. (itype /= 0)) &
           error stop 'group item differs'
      group_dir = LCMGIL(groups, ig)
      call require_record(group_dir, 'SPOT-M-QFR', nu, 4)
      call require_record(group_dir, 'SPOT-M-EVAL', nu, 4)
      call require_record(group_dir, 'SPOT-M-SRC', nu, 4)
      call require_record(group_dir, 'SPOT-M-RAW', nu, 4)
      call require_record(group_dir, 'SPOT-M-STEP', 1, 1)
      call require_record(group_dir, 'SPOT-M-ROLE', 1, 1)
      call require_record(group_dir, 'SPOT-M-GROUP', 1, 1)
      call LCMGET(group_dir, 'SPOT-M-QFR', values)
      if (any(transfer(values, 0_int64, nu) /= &
           transfer(real(qfr(:, ig), real64), 0_int64, nu))) &
           error stop 'QFR promotion differs'
      call LCMGET(group_dir, 'SPOT-M-EVAL', values)
      if (any(transfer(values, 0_int64, nu) /= &
           transfer(real(eval(:, ig), real64), 0_int64, nu))) &
           error stop 'EVAL promotion differs'
      call LCMGET(group_dir, 'SPOT-M-SRC', values)
      if (any(transfer(values, 0_int64, nu) /= &
           transfer(source(:, ig), 0_int64, nu))) error stop 'SRC differs'
      call LCMGET(group_dir, 'SPOT-M-RAW', values)
      if (any(transfer(values, 0_int64, nu) /= &
           transfer(raw(:, ig), 0_int64, nu))) error stop 'RAW overwritten'
      call LCMGET(group_dir, 'SPOT-M-STEP', step)
      call LCMGET(group_dir, 'SPOT-M-ROLE', role)
      call LCMGET(group_dir, 'SPOT-M-GROUP', group_id)
      if ((step(1) /= 1) .or. (role(1) /= 1) .or. &
           (group_id(1) /= ig)) error stop 'group identity differs'
    end do
  end subroutine require_complete


  subroutine require_record(directory, name, expected_length, &
       expected_type)
    type(c_ptr), intent(in) :: directory
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: ilong, itype

    call LCMLEN(directory, name, ilong, itype)
    if ((ilong /= expected_length) .or. (itype /= expected_type)) &
         error stop 'record metadata differs'
  end subroutine require_record

end program test_raw_moc_capture_state
