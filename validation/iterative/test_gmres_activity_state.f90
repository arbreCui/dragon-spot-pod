program test_gmres_activity_state
  use, intrinsic :: iso_c_binding, only: c_ptr, c_associated
  use, intrinsic :: iso_fortran_env, only: int32, real32
  use GANLIB
  use SPOMGMR_AUDIT
  implicit none

  integer, parameter :: ng = 370
  integer, parameter :: nu = 14
  integer(int32), parameter :: flu_bits = int(z'348637BD', int32)
  integer(int32), parameter :: err_bits = int(z'3727C5AC', int32)
  type(c_ptr) :: owner, track, extra
  integer :: ngind(ng), kmax(ng)
  logical :: active(ng)
  character(len=48) :: mode
  integer :: i

  mode = 'valid'
  if (command_argument_count() == 1) call get_command_argument(1, mode)
  if (command_argument_count() > 1) error stop 'one mode expected'

  do i = 1, ng
    ngind(i) = i
  end do
  active = .true.
  kmax = 0

  call LCMOP(owner, 'GMR-ACT-TEST', 0, 1, 0)
  call LCMOP(track, 'GMR-TRK-TEST', 0, 1, 0)
  if ((.not. c_associated(owner)) .or. (.not. c_associated(track))) &
       error stop 'LCMOP failed'
  call write_track(track, trim(mode))

  select case (trim(mode))
  case ('off')
    call SPOMGMR_FLU_RESET()
    call begin_locked(owner, track)
    call enter_locked()
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_MCGMRE_EXIT(1)
    call SPOMGMR_FINISH()
    call require_absent(owner, 'SPOT-GMR-AUD')
    write(*, '(A)') 'GMRES-ACTIVITY STATE OFF PASS'

  case ('valid')
    call arm_and_begin(owner, track)
    call require_initial(owner)
    call enter_locked()

    active = .true.
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_BLOCK_BEGIN(1, ng, active)
    call SPOMGMR_ROLE(2, 1, ng, active)
    call SPOMGMR_ROLE(3, 2, ng, active)
    active(201:ng) = .false.
    call SPOMGMR_ROLE(3, 3, ng, active)
    kmax(1:200) = 2
    kmax(201:ng) = 1
    call SPOMGMR_BLOCK_END(3, ng, kmax)

    active = .false.
    active(1:100) = .true.
    call SPOMGMR_ROLE(1, 4, ng, active)
    call SPOMGMR_BLOCK_BEGIN(4, ng, active)
    call SPOMGMR_ROLE(3, 5, ng, active)
    kmax = 0
    kmax(1:100) = 1
    call SPOMGMR_BLOCK_END(5, ng, kmax)
    call SPOMGMR_MCGMRE_EXIT(5)
    call SPOMGMR_FINISH()
    call require_mixed_complete(owner)
    write(*, '(A)') 'GMRES-ACTIVITY STATE VALID PASS'

  case ('zero-block')
    call arm_and_begin(owner, track)
    call enter_locked()
    active = .true.
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_MCGMRE_EXIT(1)
    call SPOMGMR_FINISH()
    call require_zero_block_complete(owner)
    write(*, '(A)') 'GMRES-ACTIVITY STATE ZERO-BLOCK PASS'

  case ('zero-k')
    call arm_and_begin(owner, track)
    call enter_locked()
    active = .true.
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_BLOCK_BEGIN(1, ng, active)
    call SPOMGMR_ROLE(2, 1, ng, active)
    do i = 2, 11
      call SPOMGMR_ROLE(3, i, ng, active)
    end do
    kmax = 10
    call SPOMGMR_BLOCK_END(11, ng, kmax)

    active = .false.
    active(1:200) = .true.
    call SPOMGMR_ROLE(1, 12, ng, active)
    call SPOMGMR_BLOCK_BEGIN(12, ng, active)
    do i = 13, 18
      call SPOMGMR_ROLE(3, i, ng, active)
    end do
    kmax = 0
    kmax(1:200) = 6
    call SPOMGMR_BLOCK_END(18, ng, kmax)

    active = .false.
    active(1:50) = .true.
    call SPOMGMR_ROLE(1, 19, ng, active)
    call SPOMGMR_BLOCK_BEGIN(19, ng, active)
    kmax = 0
    call SPOMGMR_BLOCK_END(19, ng, kmax)
    call SPOMGMR_MCGMRE_EXIT(19)
    call SPOMGMR_FINISH()
    call require_zero_k_complete(owner)
    write(*, '(A)') 'GMRES-ACTIVITY STATE ZERO-K PASS'

  case ('duplicate')
    call SPOMGMR_FLU_RESET()
    call SPOMGMR_PARSE_GMRA()
    call SPOMGMR_PARSE_GMRA()
    error stop 'duplicate GMRA accepted'

  case ('no-moca')
    call SPOMGMR_FLU_RESET()
    call SPOMGMR_PARSE_GMRA()
    call SPOMGMR_REQUIRE_MOCA(1)
    error stop 'GMRA without MOCA 2 accepted'

  case ('preexisting-sink')
    extra = LCMDID(owner, 'SPOT-GMR-AUD')
    if (.not. c_associated(extra)) error stop 'cannot create sentinel'
    call arm_and_begin(owner, track)
    error stop 'preexisting audit sink accepted'

  case ('partial-finish')
    call arm_and_begin(owner, track)
    call SPOMGMR_FINISH()
    error stop 'partial audit publication accepted'

  case ('second-entry')
    call arm_and_begin(owner, track)
    call enter_locked()
    call enter_locked()
    error stop 'second MCGMRE entry accepted'

  case ('open-block-exit')
    call arm_and_begin(owner, track)
    call enter_locked()
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_BLOCK_BEGIN(1, ng, active)
    call SPOMGMR_MCGMRE_EXIT(1)
    error stop 'MCGMRE exit with open block accepted'

  case ('mask-rise')
    call arm_and_begin(owner, track)
    call enter_locked()
    active = .true.
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_BLOCK_BEGIN(1, ng, active)
    call SPOMGMR_ROLE(3, 2, ng, active)
    active(101) = .false.
    call SPOMGMR_ROLE(3, 3, ng, active)
    active(101) = .true.
    call SPOMGMR_ROLE(3, 4, ng, active)
    kmax = 3
    kmax(101) = 2
    call SPOMGMR_BLOCK_END(4, ng, kmax)
    error stop 'Krylov mask 0-to-1 transition accepted'

  case ('kmax-mismatch')
    call arm_and_begin(owner, track)
    call enter_locked()
    active = .true.
    call SPOMGMR_ROLE(1, 1, ng, active)
    call SPOMGMR_BLOCK_BEGIN(1, ng, active)
    call SPOMGMR_ROLE(3, 2, ng, active)
    kmax = 1
    kmax(1) = 0
    call SPOMGMR_BLOCK_END(2, ng, kmax)
    error stop 'KMAX mismatch accepted'

  case ('wrong-door', 'wrong-type', 'wrong-ngrp', 'wrong-nun', &
        'wrong-nreg', 'wrong-maxout', 'wrong-maxinr', &
        'wrong-epsout', 'wrong-epsunk', 'wrong-epsinr', &
        'wrong-forward', 'wrong-ileak', 'wrong-rebalance', &
        'wrong-init', 'wrong-acce-left', 'wrong-acce-right', &
        'wrong-track-kryl', 'wrong-track-idifc', 'wrong-track-iaac', &
        'wrong-track-iscr', 'wrong-track-paca', 'wrong-track-maxi', &
        'wrong-track-stis', 'wrong-track-direct', &
        'wrong-track-errtol')
    call SPOMGMR_FLU_RESET()
    call SPOMGMR_PARSE_GMRA()
    call SPOMGMR_REQUIRE_MOCA(2)
    call begin_variant(owner, track, trim(mode))
    error stop 'unlocked FLU/TRACK context accepted'

  case ('actual-maxi', 'actual-errtol', 'actual-nstart', &
        'actual-ngroup', 'actual-ngeff', 'actual-nun', 'actual-ndim', &
        'actual-nlong', 'actual-nreg', 'actual-nsout', 'actual-nani', &
        'actual-nlin', 'actual-nfunl', 'actual-iaac', 'actual-iscr', &
        'actual-paca', 'actual-stis', 'actual-idir', 'actual-cyclic', &
        'actual-reverse', 'actual-ngind')
    call arm_and_begin(owner, track)
    call enter_variant(trim(mode))
    error stop 'unlocked MCGMRE arguments accepted'

  case default
    error stop 'unknown mode'
  end select

  call LCMCL(track, 2)
  call LCMCL(owner, 2)

contains

  subroutine write_track(root, selected_mode)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: selected_mode
    integer :: state(40)
    real(real32) :: values(4)

    state = 0
    state(3) = 10
    state(4) = 0
    state(7) = 80
    state(8) = 0
    state(10) = 4
    state(13) = 20
    state(15) = 1
    state(18) = 0
    values = 0.0_real32
    values(1) = transfer(err_bits, 0.0_real32)

    select case (selected_mode)
    case ('wrong-track-kryl')
      state(3) = 9
    case ('wrong-track-idifc')
      state(4) = 1
    case ('wrong-track-iaac')
      state(7) = 79
    case ('wrong-track-iscr')
      state(8) = 1
    case ('wrong-track-paca')
      state(10) = 3
    case ('wrong-track-maxi')
      state(13) = 19
    case ('wrong-track-stis')
      state(15) = 0
    case ('wrong-track-direct')
      state(18) = 1
    case ('wrong-track-errtol')
      values(1) = transfer(err_bits + 1_int32, 0.0_real32)
    end select

    call LCMPUT(root, 'MCCG-STATE', 40, 1, state)
    call LCMPUT(root, 'REAL-PARAM', 4, 2, values)
  end subroutine write_track


  subroutine arm_and_begin(flux, tracking)
    type(c_ptr), intent(in) :: flux, tracking

    call SPOMGMR_FLU_RESET()
    call SPOMGMR_PARSE_GMRA()
    call SPOMGMR_REQUIRE_MOCA(2)
    call begin_locked(flux, tracking)
  end subroutine arm_and_begin


  subroutine begin_locked(flux, tracking)
    type(c_ptr), intent(in) :: flux, tracking
    real(real32) :: epsilon

    epsilon = transfer(flu_bits, 0.0_real32)
    call SPOMGMR_BEGIN(flux, tracking, 2, 'MCCG', 0, ng, nu, 8, &
         1, 740, epsilon, epsilon, epsilon, .true., 0, .true., 1, 1, 0)
  end subroutine begin_locked


  subroutine begin_variant(flux, tracking, selected_mode)
    type(c_ptr), intent(in) :: flux, tracking
    character(len=*), intent(in) :: selected_mode
    integer :: arm, itypec, ngrp, nun, nreg, maxout, maxinr
    integer :: ileak, initfl, ncptl, ncpta
    real(real32) :: epsout, epsunk, epsinr
    logical :: lforw, lrebal
    character(len=6) :: door

    arm = 2
    door = 'MCCG'
    itypec = 0
    ngrp = ng
    nun = nu
    nreg = 8
    maxout = 1
    maxinr = 740
    epsout = transfer(flu_bits, 0.0_real32)
    epsunk = epsout
    epsinr = epsout
    lforw = .true.
    ileak = 0
    lrebal = .true.
    initfl = 1
    ncptl = 1
    ncpta = 0

    select case (selected_mode)
    case ('wrong-door')
      door = 'SYBIL'
    case ('wrong-type')
      itypec = 1
    case ('wrong-ngrp')
      ngrp = ng - 1
    case ('wrong-nun')
      nun = nu - 1
    case ('wrong-nreg')
      nreg = 7
    case ('wrong-maxout')
      maxout = 2
    case ('wrong-maxinr')
      maxinr = 739
    case ('wrong-epsout')
      epsout = transfer(flu_bits + 1_int32, 0.0_real32)
    case ('wrong-epsunk')
      epsunk = transfer(flu_bits + 1_int32, 0.0_real32)
    case ('wrong-epsinr')
      epsinr = transfer(flu_bits + 1_int32, 0.0_real32)
    case ('wrong-forward')
      lforw = .false.
    case ('wrong-ileak')
      ileak = 1
    case ('wrong-rebalance')
      lrebal = .false.
    case ('wrong-init')
      initfl = 0
    case ('wrong-acce-left')
      ncptl = 2
    case ('wrong-acce-right')
      ncpta = 1
    end select

    call SPOMGMR_BEGIN(flux, tracking, arm, door, itypec, ngrp, nun, &
         nreg, maxout, maxinr, epsout, epsunk, epsinr, lforw, ileak, &
         lrebal, initfl, ncptl, ncpta)
  end subroutine begin_variant


  subroutine enter_locked()
    real(real32) :: errtol

    errtol = transfer(err_bits, 0.0_real32)
    call SPOMGMR_MCGMRE_ENTER(20, errtol, 10, ng, ng, ngind, nu, 2, &
         nu, 8, 6, 1, 1, 1, 80, 0, 4, 1, 0, .false., .true.)
  end subroutine enter_locked


  subroutine enter_variant(selected_mode)
    character(len=*), intent(in) :: selected_mode
    integer :: maxi, nstart, ngroup, ngeff, nun, ndim, nlong, nreg
    integer :: nsout, nani, nlin, nfunl, iaac, iscr, paca, stis, idir
    integer :: ordered(ng)
    real(real32) :: errtol
    logical :: cyclic, lforw

    maxi = 20
    errtol = transfer(err_bits, 0.0_real32)
    nstart = 10
    ngroup = ng
    ngeff = ng
    ordered = ngind
    nun = nu
    ndim = 2
    nlong = nu
    nreg = 8
    nsout = 6
    nani = 1
    nlin = 1
    nfunl = 1
    iaac = 80
    iscr = 0
    paca = 4
    stis = 1
    idir = 0
    cyclic = .false.
    lforw = .true.

    select case (selected_mode)
    case ('actual-maxi')
      maxi = 19
    case ('actual-errtol')
      errtol = transfer(err_bits + 1_int32, 0.0_real32)
    case ('actual-nstart')
      nstart = 9
    case ('actual-ngroup')
      ngroup = ng - 1
    case ('actual-ngeff')
      ngeff = ng - 1
    case ('actual-nun')
      nun = nu - 1
    case ('actual-ndim')
      ndim = 3
    case ('actual-nlong')
      nlong = nu + 1
    case ('actual-nreg')
      nreg = 7
    case ('actual-nsout')
      nsout = 5
    case ('actual-nani')
      nani = 2
    case ('actual-nlin')
      nlin = 2
    case ('actual-nfunl')
      nfunl = 2
    case ('actual-iaac')
      iaac = 79
    case ('actual-iscr')
      iscr = 1
    case ('actual-paca')
      paca = 3
    case ('actual-stis')
      stis = 0
    case ('actual-idir')
      idir = 1
    case ('actual-cyclic')
      cyclic = .true.
    case ('actual-reverse')
      lforw = .false.
    case ('actual-ngind')
      ordered(ng) = 1
    end select

    call SPOMGMR_MCGMRE_ENTER(maxi, errtol, nstart, ngroup, ngeff, &
         ordered, nun, ndim, nlong, nreg, nsout, nani, nlin, nfunl, &
         iaac, iscr, paca, stis, idir, cyclic, lforw)
  end subroutine enter_variant


  subroutine require_initial(flux)
    type(c_ptr), intent(in) :: flux
    type(c_ptr) :: audit
    integer :: state(24), expected(24)

    audit = LCMGID(flux, 'SPOT-GMR-AUD')
    expected = 0
    expected(1:8) = [1, 0, 2, 1, ng, nu, 0, 10]
    expected(21) = 20
    expected(22) = int(err_bits, kind(expected))
    call LCMGET(audit, 'STATE-VECTOR', state)
    if (any(state /= expected)) error stop 'initial STATE-VECTOR differs'
    call require_absent(audit, 'NGIND')
    call require_absent(audit, 'CALL-META')
    call require_absent(audit, 'ROLE-CALLS')
    call require_absent(audit, 'ROLE-GROUPS')
    call require_absent(audit, 'ROLE-EVENTS')
    call require_absent(audit, 'ROLE-ACTIVE')
    call require_absent(audit, 'K-HISTOGRAM')
    call require_absent(audit, 'BLOCK-META')
    call require_absent(audit, 'BLOCK-ACTIVE')
    call require_absent(audit, 'BLOCK-KMAX')
  end subroutine require_initial


  subroutine require_mixed_complete(flux)
    type(c_ptr), intent(in) :: flux
    type(c_ptr) :: audit
    integer :: state(24), expected(24), ordered(ng)
    integer :: calls(3), groups(3), histogram(0:10)
    integer :: call_meta(5), events(6,6)
    integer :: masks(ng,6), metadata(4,2)
    integer :: block_masks(ng,2), block_values(ng,2)
    integer :: expected_events(6,6)

    audit = LCMGID(flux, 'SPOT-GMR-AUD')
    expected = 0
    expected(1:8) = [1, 1, 2, 1, ng, nu, ng, 10]
    expected(9:20) = [1, 1, 2, 1, 3, 470, 370, 670, 2, 470, 670, 2]
    expected(21) = 20
    expected(22) = int(err_bits, kind(expected))
    call LCMGET(audit, 'STATE-VECTOR', state)
    if (any(state /= expected)) error stop 'complete STATE-VECTOR differs'

    call LCMGET(audit, 'NGIND', ordered)
    if (any(ordered /= ngind)) error stop 'NGIND differs'
    call LCMGET(audit, 'CALL-META', call_meta)
    if (any(call_meta /= [1, 1, 6, 2, 5])) &
         error stop 'CALL-META differs'
    call LCMGET(audit, 'ROLE-CALLS', calls)
    if (any(calls /= [2, 1, 3])) error stop 'ROLE-CALLS differs'
    call LCMGET(audit, 'ROLE-GROUPS', groups)
    if (any(groups /= [470, 370, 670])) error stop 'ROLE-GROUPS differs'

    expected_events(:,1) = [1, 1, 1, 1, 0, 370]
    expected_events(:,2) = [1, 2, 2, 1, 1, 370]
    expected_events(:,3) = [1, 3, 3, 2, 1, 370]
    expected_events(:,4) = [1, 4, 3, 3, 1, 200]
    expected_events(:,5) = [1, 5, 1, 4, 0, 100]
    expected_events(:,6) = [1, 6, 3, 5, 2, 100]
    call LCMGET(audit, 'ROLE-EVENTS', events)
    if (any(events /= expected_events)) error stop 'ROLE-EVENTS differs'
    call LCMGET(audit, 'ROLE-ACTIVE', masks)
    if (any(masks(:,1) /= 1) .or. any(masks(:,2) /= 1) .or. &
         any(masks(:,3) /= 1)) error stop 'full role mask differs'
    if (any(masks(1:200,4) /= 1) .or. any(masks(201:ng,4) /= 0)) &
         error stop 'partial Krylov role mask differs'
    if (any(masks(1:100,5) /= 1) .or. any(masks(101:ng,5) /= 0) .or. &
        any(masks(1:100,6) /= 1) .or. any(masks(101:ng,6) /= 0)) &
         error stop 'second-block role mask differs'

    histogram = 0
    call LCMGET(audit, 'K-HISTOGRAM', histogram)
    if ((histogram(0) /= 270) .or. (histogram(1) /= 270) .or. &
        (histogram(2) /= 200) .or. any(histogram(3:10) /= 0)) &
         error stop 'K-HISTOGRAM differs'
    call LCMGET(audit, 'BLOCK-META', metadata)
    if (any(metadata(:,1) /= [1, 1, 3, 370]) .or. &
        any(metadata(:,2) /= [1, 2, 5, 100])) &
         error stop 'BLOCK-META differs'
    call LCMGET(audit, 'BLOCK-ACTIVE', block_masks)
    if (any(block_masks(:,1) /= 1) .or. &
        any(block_masks(1:100,2) /= 1) .or. &
        any(block_masks(101:ng,2) /= 0)) &
         error stop 'BLOCK-ACTIVE differs'
    call LCMGET(audit, 'BLOCK-KMAX', block_values)
    if (any(block_values(1:200,1) /= 2) .or. &
        any(block_values(201:ng,1) /= 1) .or. &
        any(block_values(1:100,2) /= 1) .or. &
        any(block_values(101:ng,2) /= 0)) &
         error stop 'BLOCK-KMAX differs'
  end subroutine require_mixed_complete


  subroutine require_zero_block_complete(flux)
    type(c_ptr), intent(in) :: flux
    type(c_ptr) :: audit
    integer :: state(24), expected(24), histogram(0:10)

    audit = LCMGID(flux, 'SPOT-GMR-AUD')
    expected = 0
    expected(1:8) = [1, 1, 2, 1, ng, nu, ng, 10]
    expected(9:20) = [1, 1, 1, 0, 0, ng, 0, 0, 0, 0, 0, 0]
    expected(21) = 20
    expected(22) = int(err_bits, kind(expected))
    call LCMGET(audit, 'STATE-VECTOR', state)
    if (any(state /= expected)) error stop 'zero-block state differs'
    histogram = -1
    call LCMGET(audit, 'K-HISTOGRAM', histogram)
    if (any(histogram /= 0)) error stop 'zero-block histogram differs'
    call require_absent(audit, 'BLOCK-META')
    call require_absent(audit, 'BLOCK-ACTIVE')
    call require_absent(audit, 'BLOCK-KMAX')
  end subroutine require_zero_block_complete


  subroutine require_zero_k_complete(flux)
    type(c_ptr), intent(in) :: flux
    type(c_ptr) :: audit
    integer :: state(24), expected(24), histogram(0:10)
    integer :: metadata(4,3), masks(ng,3), values(ng,3)

    audit = LCMGID(flux, 'SPOT-GMR-AUD')
    expected = 0
    expected(1:8) = [1, 1, 2, 1, ng, nu, ng, 10]
    expected(9:20) = [1, 1, 3, 1, 16, 620, 370, 4900, &
         3, 570, 4900, 10]
    expected(21) = 20
    expected(22) = int(err_bits, kind(expected))
    call LCMGET(audit, 'STATE-VECTOR', state)
    if (any(state /= expected)) error stop 'zero-K state differs'
    histogram = 0
    call LCMGET(audit, 'K-HISTOGRAM', histogram)
    if ((histogram(0) /= 540) .or. (histogram(6) /= 200) .or. &
        (histogram(10) /= 370) .or. &
        any(histogram(1:5) /= 0) .or. any(histogram(7:9) /= 0)) &
         error stop 'zero-K histogram differs'
    call LCMGET(audit, 'BLOCK-META', metadata)
    if (any(metadata(:,1) /= [1, 1, 11, ng]) .or. &
        any(metadata(:,2) /= [1, 2, 18, 200]) .or. &
        any(metadata(:,3) /= [1, 3, 19, 50])) &
         error stop 'zero-K BLOCK-META differs'
    call LCMGET(audit, 'BLOCK-ACTIVE', masks)
    call LCMGET(audit, 'BLOCK-KMAX', values)
    if (any(masks(:,1) /= 1) .or. any(values(:,1) /= 10) .or. &
        any(masks(1:200,2) /= 1) .or. &
        any(masks(201:ng,2) /= 0) .or. &
        any(values(1:200,2) /= 6) .or. &
        any(values(201:ng,2) /= 0) .or. &
        any(masks(1:50,3) /= 1) .or. &
        any(masks(51:ng,3) /= 0) .or. any(values(:,3) /= 0)) &
         error stop 'zero-K block rows differ'
  end subroutine require_zero_k_complete


  subroutine require_absent(root, name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: ilong, itype

    call LCMLEN(root, name, ilong, itype)
    if (ilong /= 0) then
      write(0, '(A)') trim(name)//' unexpectedly exists'
      error stop 'unexpected record'
    end if
  end subroutine require_absent

end program test_gmres_activity_state
