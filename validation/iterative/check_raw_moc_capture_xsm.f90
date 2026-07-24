program check_raw_moc_capture_xsm
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use, intrinsic :: iso_c_binding, only: c_ptr, c_int32_t, c_f_pointer
  use, intrinsic :: iso_fortran_env, only: int32, int64, real32, real64
  implicit none

  integer, parameter :: ng = 370
  integer, parameter :: nr = 8
  integer, parameter :: ns = 6
  integer, parameter :: nu = 14
  integer, parameter :: nstate = 40
  integer, parameter :: nargs = 7
  integer, parameter :: max_path = 72
  integer, parameter :: max_records = 4096

  type :: track_layout
    integer :: keyflux(nr)
    integer :: keycur(ns)
    integer :: ibc(ns)
    integer :: nzon(nu)
    integer :: icode(ns)
    real(real32) :: volume(nr)
    real(real32) :: albedo(ns)
  end type track_layout

  type :: system_data
    integer :: nmix = 0
    integer :: nalbedo = 0
    real(real32), allocatable :: s0(:,:)
    real(real32), allocatable :: group_albedo(:,:)
  end type system_data

  character(len=1024) :: path(nargs), arm_text
  type(c_ptr) :: pre, frozen, off, on
  type(track_layout) :: layout
  type(system_data) :: system
  real(real64), allocatable :: delta(:,:), evaluated(:,:)
  integer :: arm, i, j
  real(real64) :: relative_norm, relative_max

  if (command_argument_count() /= nargs) &
       call fail('expected TRACK SYSTEM PRE FROZEN OFF ON ARM')
  do i = 1, nargs
    call get_command_argument(i, path(i))
    if (len_trim(path(i)) == 0) call fail('empty argument')
    if ((i < nargs) .and. (len_trim(path(i)) > max_path)) &
         call fail('XSM path exceeds Ganlib limit')
    do j = 1, i - 1
      if ((i < nargs) .and. (j < nargs)) then
        if (trim(path(i)) == trim(path(j))) &
             call fail('XSM paths must be distinct')
      end if
    end do
  end do
  read(path(nargs), *, iostat=i) arm
  if ((i /= 0) .or. (arm < 1) .or. (arm > 2)) &
       call fail('arm must be 1 or 2')
  if (arm == 1) then
    arm_text = 'NATIVE'
  else
    arm_text = 'STATIONARY'
  end if

  call load_track(trim(path(1)), layout)
  call load_system(trim(path(2)), layout, system)
  call LCMOP(pre, trim(path(3)), 2, 2, 0)
  call LCMOP(frozen, trim(path(4)), 2, 2, 0)
  call LCMOP(off, trim(path(5)), 2, 2, 0)
  call LCMOP(on, trim(path(6)), 2, 2, 0)
  call require_signature(pre, 'L_FLUX', 'PRE')
  call require_signature(frozen, 'L_FLUX', 'FROZEN')
  call require_signature(off, 'L_FLUX', 'OFF')
  call require_signature(on, 'L_FLUX', 'ON')
  call require_audit_absent(pre, 'PRE')
  call require_audit_absent(frozen, 'FROZEN')
  call require_audit_absent(off, 'OFF')
  call compare_table(frozen, off, 0, .false.)
  call compare_table(off, on, 0, .true.)

  allocate(delta(nu, ng), evaluated(nu, ng))
  call check_audit(on, pre, arm, layout, system, delta, evaluated, &
       relative_norm, relative_max)
  call print_result(trim(arm_text), delta, layout, &
       relative_norm, relative_max)

  call LCMCL(on, 1)
  call LCMCL(off, 1)
  call LCMCL(frozen, 1)
  call LCMCL(pre, 1)

contains

  subroutine load_track(xsm_path, data)
    character(len=*), intent(in) :: xsm_path
    type(track_layout), intent(out) :: data
    type(c_ptr) :: root
    character(len=12) :: track_type
    integer :: state(nstate), all_keys(nu), i

    call LCMOP(root, xsm_path, 2, 2, 0)
    call require_signature(root, 'L_TRACK', 'TRACK')
    call require_record(root, 'TRACK-TYPE', 3, 3, 'TRACK')
    call LCMGTC(root, 'TRACK-TYPE', 12, track_type)
    if (trim(track_type) /= 'MCCG') call fail('TRACK is not MCCG')
    call require_record(root, 'STATE-VECTOR', nstate, 1, 'TRACK')
    call LCMGET(root, 'STATE-VECTOR', state)
    if ((state(1) /= nr) .or. (state(2) /= nu) .or. &
         (state(5) /= ns) .or. (state(6) /= 1) .or. &
         (state(9) == 1)) call fail('TRACK dimensions or branch differ')
    call require_record(root, 'KEYFLX$ANIS', nr, 1, 'TRACK')
    call require_record(root, 'KEYCUR$MCCG', ns, 1, 'TRACK')
    call require_record(root, 'BC-REFL+TRAN', ns, 1, 'TRACK')
    call require_record(root, 'NZON$MCCG', nu, 1, 'TRACK')
    call require_record(root, 'VOLUME', nr, 2, 'TRACK')
    call require_record(root, 'ICODE', ns, 1, 'TRACK')
    call require_record(root, 'ALBEDO', ns, 2, 'TRACK')
    call LCMGET(root, 'KEYFLX$ANIS', data%keyflux)
    call LCMGET(root, 'KEYCUR$MCCG', data%keycur)
    call LCMGET(root, 'BC-REFL+TRAN', data%ibc)
    call LCMGET(root, 'NZON$MCCG', data%nzon)
    call LCMGET(root, 'VOLUME', data%volume)
    call LCMGET(root, 'ICODE', data%icode)
    call LCMGET(root, 'ALBEDO', data%albedo)
    if (any(data%keyflux < 1) .or. any(data%keyflux > nu) .or. &
         has_duplicate(data%keyflux)) call fail('invalid KEYFLX layout')
    if (any(data%keycur < 1) .or. any(data%keycur > nu) .or. &
         has_duplicate(data%keycur)) call fail('invalid KEYCUR layout')
    all_keys = [data%keyflux, data%keycur]
    do i = 1, nu
      if (count(all_keys == i) /= 1) &
           call fail('scalar/current keys are not a permutation')
    end do
    if (any(data%ibc < 1) .or. any(data%ibc > ns)) &
         call fail('invalid boundary coupling')
    if (any(data%nzon(1:nr) < 0) .or. &
         any(data%nzon(nr+1:nu) > -1) .or. &
         any(data%nzon(nr+1:nu) < -ns)) &
         call fail('invalid MCCG zone map')
    if (any(.not. ieee_is_finite(data%volume)) .or. &
         any(data%volume <= 0.0_real32)) call fail('invalid VOLUME')
    if (any(.not. ieee_is_finite(data%albedo))) &
         call fail('nonfinite TRACK albedo')
    call LCMCL(root, 1)
  end subroutine load_track


  subroutine load_system(xsm_path, layout, data)
    character(len=*), intent(in) :: xsm_path
    type(track_layout), intent(in) :: layout
    type(system_data), intent(out) :: data
    type(c_ptr) :: root, groups, group_dir
    integer :: group, ilong, itype, mix_max
    real(real32), allocatable :: tx(:)

    call LCMOP(root, xsm_path, 2, 2, 0)
    call require_signature(root, 'L_PIJ', 'SYSTEM')
    call require_record(root, 'GROUP', ng, 10, 'SYSTEM')
    groups = LCMGID(root, 'GROUP')
    call require_list_item(groups, 1, -1, 0, 'SYSTEM GROUP')
    group_dir = LCMGIL(groups, 1)
    call LCMLEN(group_dir, 'DRAGON-S0XSC', ilong, itype)
    if ((ilong < 1) .or. (itype /= 2)) &
         call fail('invalid DRAGON-S0XSC')
    data%nmix = ilong - 1
    mix_max = maxval(layout%nzon(1:nr))
    if ((mix_max > data%nmix) .or. (minval(layout%nzon(1:nr)) < 0)) &
         call fail('SYSTEM mixture range differs')
    call LCMLEN(group_dir, 'ALBEDO', data%nalbedo, itype)
    if ((data%nalbedo > 0) .and. (itype /= 2)) &
         call fail('invalid group ALBEDO')
    if (any(layout%icode < 0) .or. &
         any(layout%icode > data%nalbedo)) &
         call fail('ICODE exceeds group ALBEDO')
    allocate(data%s0(0:data%nmix, ng))
    allocate(data%group_albedo(data%nalbedo, ng))
    allocate(tx(0:data%nmix))
    do group = 1, ng
      call require_list_item(groups, group, -1, 0, 'SYSTEM GROUP')
      group_dir = LCMGIL(groups, group)
      call require_record(group_dir, 'DRAGON-S0XSC', data%nmix + 1, &
           2, 'SYSTEM GROUP')
      call require_record(group_dir, 'DRAGON-TXSC', data%nmix + 1, &
           2, 'SYSTEM GROUP')
      call LCMGET(group_dir, 'DRAGON-S0XSC', data%s0(:, group))
      call LCMGET(group_dir, 'DRAGON-TXSC', tx)
      if (data%nalbedo > 0) then
        call require_record(group_dir, 'ALBEDO', data%nalbedo, 2, &
             'SYSTEM GROUP')
        call LCMGET(group_dir, 'ALBEDO', data%group_albedo(:, group))
      end if
      if (any(.not. ieee_is_finite(data%s0(:, group))) .or. &
           any(.not. ieee_is_finite(tx))) &
           call fail('nonfinite SYSTEM cross section')
      if ((data%nalbedo > 0) .and. &
           any(.not. ieee_is_finite(data%group_albedo(:, group)))) &
           call fail('nonfinite SYSTEM albedo')
    end do
    deallocate(tx)
    call LCMCL(root, 1)
  end subroutine load_system


  subroutine check_audit(root, pre_root, arm, layout, system, delta, &
       evaluated, relative_norm, relative_max)
    type(c_ptr), intent(in) :: root, pre_root
    integer, intent(in) :: arm
    type(track_layout), intent(in) :: layout
    type(system_data), intent(in) :: system
    real(real64), intent(out) :: delta(nu, ng), evaluated(nu, ng)
    real(real64), intent(out) :: relative_norm, relative_max
    type(c_ptr) :: audit, groups, group_dir, pre_groups
    integer :: state(24), expected(24), ordered(ng)
    integer :: group, unknown, region, surface, key, coupled
    integer :: step(1), role(1), group_id(1), mix
    real(real64) :: qfr(nu), source(nu), raw(nu), pre64(nu)
    real(real32) :: qfr32(nu), eval32(nu), pre32(nu)
    real(real32) :: product32, sum32, albedo32
    real(real64) :: expected_source
    real(real64) :: numerator2, denominator2, term, max_num, max_den

    call require_root_census(root, .true.)
    audit = LCMGID(root, 'SPOT-MOC-AUD')
    call require_table_names(audit, [character(len=12) :: &
         'GROUP', 'NGIND', 'STATE-VECTOR'], 'AUDIT ROOT')
    call require_record(audit, 'STATE-VECTOR', 24, 1, 'AUDIT ROOT')
    call require_record(audit, 'NGIND', ng, 1, 'AUDIT ROOT')
    call require_record(audit, 'GROUP', ng, 10, 'AUDIT ROOT')
    call LCMGET(audit, 'STATE-VECTOR', state)
    expected = [1, 1, arm, 1, 1, 1, 1, 1, 1, 1, 1, 1, &
         10, 1, 80, 0, 0, 4, 0, ng, ng, nu, nr, ng]
    if (any(state /= expected)) call fail('audit STATE-VECTOR differs')
    call LCMGET(audit, 'NGIND', ordered)
    do group = 1, ng
      if (ordered(group) /= group) call fail('audit NGIND differs')
    end do
    groups = LCMGID(audit, 'GROUP')
    call require_record(pre_root, 'FLUX', ng, 10, 'PRE')
    pre_groups = LCMGID(pre_root, 'FLUX')

    numerator2 = 0.0_real64
    denominator2 = 0.0_real64
    max_num = 0.0_real64
    max_den = 0.0_real64
    do group = 1, ng
      call require_list_item(groups, group, -1, 0, 'AUDIT GROUP')
      group_dir = LCMGIL(groups, group)
      call require_table_names(group_dir, [character(len=12) :: &
           'SPOT-M-EVAL', 'SPOT-M-GROUP', 'SPOT-M-QFR', &
           'SPOT-M-RAW', 'SPOT-M-ROLE', 'SPOT-M-SRC', &
           'SPOT-M-STEP'], 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-QFR', nu, 4, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-EVAL', nu, 4, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-SRC', nu, 4, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-RAW', nu, 4, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-STEP', 1, 1, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-ROLE', 1, 1, 'AUDIT GROUP')
      call require_record(group_dir, 'SPOT-M-GROUP', 1, 1, 'AUDIT GROUP')
      call LCMGET(group_dir, 'SPOT-M-QFR', qfr)
      call LCMGET(group_dir, 'SPOT-M-EVAL', evaluated(:, group))
      call LCMGET(group_dir, 'SPOT-M-SRC', source)
      call LCMGET(group_dir, 'SPOT-M-RAW', raw)
      call LCMGET(group_dir, 'SPOT-M-STEP', step)
      call LCMGET(group_dir, 'SPOT-M-ROLE', role)
      call LCMGET(group_dir, 'SPOT-M-GROUP', group_id)
      if ((step(1) /= 1) .or. (role(1) /= 1) .or. &
           (group_id(1) /= group)) call fail('group identity differs')
      if (any(.not. ieee_is_finite(qfr)) .or. &
           any(.not. ieee_is_finite(evaluated(:, group))) .or. &
           any(.not. ieee_is_finite(source)) .or. &
           any(.not. ieee_is_finite(raw))) call fail('nonfinite tuple')
      qfr32 = real(qfr, real32)
      eval32 = real(evaluated(:, group), real32)
      if (.not. same_bits64(qfr, real(qfr32, real64))) &
           call fail('QFR is not an exact binary32 promotion')
      if (.not. same_bits64(evaluated(:, group), &
           real(eval32, real64))) &
           call fail('EVAL is not an exact binary32 promotion')
      call require_list_item(pre_groups, group, nu, 2, 'PRE FLUX')
      call LCMGDL(pre_groups, group, pre32)
      pre64 = real(pre32, real64)
      if (.not. same_bits64(evaluated(:, group), pre64)) &
           call fail('EVAL differs from frozen PRE input')

      do region = 1, nr
        key = layout%keyflux(region)
        mix = layout%nzon(region)
        product32 = system%s0(mix, group) * eval32(key)
        sum32 = qfr32(key) + product32
        expected_source = real(sum32, real64)
        if (transfer(source(key), 0_int64) /= &
             transfer(expected_source, 0_int64)) &
             call fail('volume source replay differs')
      end do
      do surface = 1, ns
        key = layout%keycur(surface)
        coupled = layout%keycur(layout%ibc(surface))
        albedo32 = layout%albedo(surface)
        if (layout%icode(surface) > 0) &
             albedo32 = system%group_albedo( &
             layout%icode(surface), group)
        product32 = albedo32 * eval32(coupled)
        expected_source = real(product32, real64)
        if (transfer(source(key), 0_int64) /= &
             transfer(expected_source, 0_int64)) &
             call fail('boundary source replay differs')
      end do

      delta(:, group) = raw - evaluated(:, group)
      do unknown = 1, nu
        if (.not. ieee_is_finite(delta(unknown, group))) &
             call fail('nonfinite raw-minus-eval')
      end do
      do region = 1, nr
        key = layout%keyflux(region)
        if ((evaluated(key, group) <= 0.0_real64) .or. &
             (raw(key) <= 0.0_real64)) &
             call fail('nonpositive scalar flux')
        term = (real(layout%volume(region), real64) * &
             delta(key, group)) * delta(key, group)
        numerator2 = numerator2 + term
        term = (real(layout%volume(region), real64) * &
             evaluated(key, group)) * evaluated(key, group)
        denominator2 = denominator2 + term
        max_num = max(max_num, abs(delta(key, group)))
        max_den = max(max_den, abs(evaluated(key, group)))
      end do
    end do
    if ((denominator2 <= 0.0_real64) .or. &
         (max_den <= 0.0_real64)) call fail('zero normalization')
    relative_norm = sqrt(numerator2 / denominator2)
    relative_max = max_num / max_den
  end subroutine check_audit


  subroutine print_result(arm, delta, layout, relative_norm, &
       relative_max)
    character(len=*), intent(in) :: arm
    real(real64), intent(in) :: delta(nu, ng)
    type(track_layout), intent(in) :: layout
    real(real64), intent(in) :: relative_norm, relative_max
    integer :: group, unknown, region, surface, key
    real(real64) :: max_num, value
    character(len=7) :: category

    write(6, '(A,1X,A)') 'RAW-MOC-XSM ARM', trim(arm)
    write(6, '(A,3(1X,I0))') 'RAW-MOC-XSM DIMS', ng, nr, nu
    write(6, '(A)') 'RAW-MOC-XSM PHASE POST-STIS-PRE-ACA-SCR'
    do group = 1, ng
      do unknown = 1, nu
        category = 'UNKNOWN'
        do region = 1, nr
          if (layout%keyflux(region) == unknown) category = 'SCALAR'
        end do
        do surface = 1, ns
          if (layout%keycur(surface) == unknown) category = 'CURRENT'
        end do
        write(6, '(A,2(1X,I0),1X,A,1X,ES25.17E3,1X,Z16.16)') &
             'RAW-MOC-XSM LEDGER', group, unknown, trim(category), &
             delta(unknown, group), transfer(delta(unknown, group), &
             0_int64)
      end do
    end do
    write(6, '(A,1X,ES25.17E3,1X,Z16.16)') &
         'RAW-MOC-XSM SCALAR-RELATIVE-TWO-NORM', relative_norm, &
         transfer(relative_norm, 0_int64)
    write(6, '(A,1X,ES25.17E3,1X,Z16.16)') &
         'RAW-MOC-XSM SCALAR-INPUT-NORMALIZED-MAX', relative_max, &
         transfer(relative_max, 0_int64)
    max_num = 0.0_real64
    do group = 1, ng
      do region = 1, nr
        key = layout%keyflux(region)
        max_num = max(max_num, abs(delta(key, group)))
      end do
    end do
    do group = 1, ng
      do region = 1, nr
        key = layout%keyflux(region)
        value = abs(delta(key, group))
        if (transfer(value, 0_int64) == transfer(max_num, 0_int64)) then
          write(6, '(A,3(1X,I0),1X,Z16.16)') &
               'RAW-MOC-XSM MAX-TIE', group, region, key, &
               transfer(delta(key, group), 0_int64)
        end if
      end do
    end do
    do group = 1, ng
      do surface = 1, ns
        key = layout%keycur(surface)
        write(6, '(A,3(1X,I0),1X,ES25.17E3,1X,Z16.16)') &
             'RAW-MOC-XSM CURRENT', group, surface, key, &
             delta(key, group), transfer(delta(key, group), 0_int64)
      end do
    end do
    write(6, '(A)') 'RAW-MOC-XSM CAPTURE-VALID'
    write(6, '(A)') 'RAW-MOC-XSM OUTER-CONVERGENCE NOT-EVALUATED'
    write(6, '(A)') 'RAW-MOC-XSM STAGE4 NOT-AUTHORIZED'
    write(6, '(A)') 'RAW-MOC-XSM COMPLETE'
  end subroutine print_result


  recursive subroutine compare_table(left, right, depth, ignore_audit)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: depth
    logical, intent(in) :: ignore_audit
    character(len=12) :: left_names(max_records)
    character(len=12) :: right_names(max_records)
    type(c_ptr) :: left_child, right_child
    integer :: left_count, right_count, i, left_length, right_length
    integer :: left_type, right_type

    call collect_names(left, left_names, left_count, &
         ignore_audit .and. (depth == 0))
    call collect_names(right, right_names, right_count, &
         ignore_audit .and. (depth == 0))
    if (left_count /= right_count) call fail('table census differs')
    if (any(left_names(1:left_count) /= right_names(1:right_count))) &
         call fail('table record names differ')
    do i = 1, left_count
      call LCMLEN(left, left_names(i), left_length, left_type)
      call LCMLEN(right, right_names(i), right_length, right_type)
      if ((left_length /= right_length) .or. &
           (left_type /= right_type)) call fail('record metadata differs')
      select case (left_type)
      case (0)
        left_child = LCMGID(left, left_names(i))
        right_child = LCMGID(right, right_names(i))
        call compare_table(left_child, right_child, depth + 1, .false.)
      case (10)
        left_child = LCMGID(left, left_names(i))
        right_child = LCMGID(right, right_names(i))
        call compare_list(left_child, right_child, left_length, depth + 1)
      case (1:6)
        call compare_table_primitive(left, right, left_names(i), &
             left_length, left_type)
      case default
        call fail('unsupported LCM record type')
      end select
    end do
  end subroutine compare_table


  recursive subroutine compare_list(left, right, list_length, depth)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: list_length, depth
    type(c_ptr) :: left_child, right_child
    integer :: item, left_length, right_length, left_type, right_type

    do item = 1, list_length
      call LCMLEL(left, item, left_length, left_type)
      call LCMLEL(right, item, right_length, right_type)
      if ((left_length /= right_length) .or. &
           (left_type /= right_type)) call fail('list metadata differs')
      select case (left_type)
      case (0)
        left_child = LCMGIL(left, item)
        right_child = LCMGIL(right, item)
        call compare_table(left_child, right_child, depth + 1, .false.)
      case (10)
        left_child = LCMGIL(left, item)
        right_child = LCMGIL(right, item)
        call compare_list(left_child, right_child, left_length, depth + 1)
      case (1:6)
        call compare_list_primitive(left, right, item, left_length, &
             left_type)
      case (99)
        if (left_length /= 0) call fail('invalid empty list item')
      case default
        call fail('unsupported LCM list type')
      end select
    end do
  end subroutine compare_list


  subroutine collect_names(table, names, count, ignore_audit)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(out) :: names(max_records)
    integer, intent(out) :: count
    logical, intent(in) :: ignore_audit
    character(len=12) :: name, first

    names = ' '
    count = 0
    name = ' '
    call LCMNXT(table, name)
    if (name == ' ') return
    first = name
    do
      if (.not. (ignore_audit .and. &
           (trim(name) == 'SPOT-MOC-AUD'))) then
        count = count + 1
        if (count > max_records) call fail('too many table records')
        names(count) = name
      end if
      call LCMNXT(table, name)
      if (name == first) exit
    end do
    call sort_names(names, count)
  end subroutine collect_names


  subroutine sort_names(names, count)
    character(len=12), intent(inout) :: names(max_records)
    integer, intent(in) :: count
    character(len=12) :: held
    integer :: i, j

    do i = 2, count
      held = names(i)
      j = i - 1
      do while (j >= 1)
        if (names(j) <= held) exit
        names(j + 1) = names(j)
        j = j - 1
      end do
      names(j + 1) = held
    end do
  end subroutine sort_names


  subroutine compare_table_primitive(left, right, name, length, lcm_type)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: length, lcm_type
    type(c_ptr) :: left_data, right_data

    call LCMGPD(left, name, left_data)
    call LCMGPD(right, name, right_data)
    call compare_words(left_data, right_data, length, lcm_type)
  end subroutine compare_table_primitive


  subroutine compare_list_primitive(left, right, item, length, lcm_type)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: item, length, lcm_type
    type(c_ptr) :: left_data, right_data

    call LCMGPL(left, item, left_data)
    call LCMGPL(right, item, right_data)
    call compare_words(left_data, right_data, length, lcm_type)
  end subroutine compare_list_primitive


  subroutine compare_words(left_data, right_data, length, lcm_type)
    type(c_ptr), intent(in) :: left_data, right_data
    integer, intent(in) :: length, lcm_type
    integer(c_int32_t), pointer :: left_words(:), right_words(:)
    integer :: word_count

    word_count = length
    if ((lcm_type == 4) .or. (lcm_type == 6)) word_count = 2 * length
    call c_f_pointer(left_data, left_words, [word_count])
    call c_f_pointer(right_data, right_words, [word_count])
    if (any(left_words /= right_words)) &
         call fail('non-audit primitive value differs')
  end subroutine compare_words


  subroutine require_root_census(root, allow_audit)
    type(c_ptr), intent(in) :: root
    logical, intent(in) :: allow_audit
    character(len=12) :: names(max_records)
    integer :: count, i, audit_count

    call collect_names(root, names, count, .false.)
    audit_count = 0
    do i = 1, count
      if (trim(names(i)) == 'SPOT-MOC-AUD') audit_count = audit_count + 1
    end do
    if (allow_audit) then
      if (audit_count /= 1) call fail('audit directory census differs')
    else
      if (audit_count /= 0) call fail('unexpected audit directory')
    end if
  end subroutine require_root_census


  subroutine require_table_names(table, expected, owner)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(in) :: expected(:)
    character(len=*), intent(in) :: owner
    character(len=12) :: found(max_records), sorted_expected(size(expected))
    integer :: count

    call collect_names(table, found, count, .false.)
    sorted_expected = expected
    call sort_small(sorted_expected)
    if (count /= size(expected)) call fail(trim(owner)//' census differs')
    if (any(found(1:count) /= sorted_expected)) &
         call fail(trim(owner)//' names differ')
  end subroutine require_table_names


  subroutine sort_small(names)
    character(len=12), intent(inout) :: names(:)
    character(len=12) :: held
    integer :: i, j

    do i = 2, size(names)
      held = names(i)
      j = i - 1
      do while (j >= 1)
        if (names(j) <= held) exit
        names(j + 1) = names(j)
        j = j - 1
      end do
      names(j + 1) = held
    end do
  end subroutine sort_small


  subroutine require_audit_absent(root, owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: owner
    integer :: ilong, itype

    call LCMLEN(root, 'SPOT-MOC-AUD', ilong, itype)
    if (ilong /= 0) call fail(trim(owner)//' already has audit directory')
  end subroutine require_audit_absent


  subroutine require_signature(root, expected, owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: expected, owner
    character(len=12) :: signature

    call require_record(root, 'SIGNATURE', 3, 3, owner)
    call LCMGTC(root, 'SIGNATURE', 12, signature)
    if (signature /= expected) call fail(trim(owner)//' signature differs')
  end subroutine require_signature


  subroutine require_record(root, name, expected_length, expected_type, &
       owner)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, owner
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEN(root, name, found_length, found_type)
    if ((found_length /= expected_length) .or. &
         (found_type /= expected_type)) then
      write(0, '(A,1X,A,4(1X,I0))') trim(owner)//' RECORD', trim(name), &
           found_length, found_type, expected_length, expected_type
      call fail('record contract differs')
    end if
  end subroutine require_record


  subroutine require_list_item(list, item, expected_length, &
       expected_type, owner)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: item, expected_length, expected_type
    character(len=*), intent(in) :: owner
    integer :: found_length, found_type

    call LCMLEL(list, item, found_length, found_type)
    if ((found_length /= expected_length) .or. &
         (found_type /= expected_type)) then
      write(0, '(A,1X,I0,4(1X,I0))') trim(owner)//' ITEM', item, &
           found_length, found_type, expected_length, expected_type
      call fail('list contract differs')
    end if
  end subroutine require_list_item


  pure logical function same_bits64(left, right)
    real(real64), intent(in) :: left(:), right(:)

    same_bits64 = size(left) == size(right)
    if (same_bits64) same_bits64 = all( &
         transfer(left, 0_int64, size(left)) == &
         transfer(right, 0_int64, size(right)))
  end function same_bits64


  pure logical function has_duplicate(values)
    integer, intent(in) :: values(:)
    integer :: left, right

    has_duplicate = .false.
    do left = 1, size(values) - 1
      do right = left + 1, size(values)
        if (values(left) == values(right)) then
          has_duplicate = .true.
          return
        end if
      end do
    end do
  end function has_duplicate


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0, '(A)') 'RAW-MOC-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_raw_moc_capture_xsm
