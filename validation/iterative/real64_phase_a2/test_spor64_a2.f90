program test_spor64_a2
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use SPOR64_A2, only : MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED, &
      SPOR64_A2_INVALID, SPOR64_A2_OK, SPOR64_A2_RESPONSE_FAILED, &
      SPOR64_A2_UNSUPPORTED
  implicit none

  integer, parameter :: m = 1, nreg = 2, nsur = 2, n = nreg + nsur
  integer, parameter :: kpn = 6, ng = 370, ngeff = 5
  integer :: callback_calls, callback_mode, calls_before
  integer :: group, i, mask, status
  integer :: ibc(nsur), keycur(nsur), keyflx(nreg,1,1)
  integer :: ngind(ngeff), ngind_before(ngeff), nzon(n)
  integer(int32) :: sc_bits_before((m+1)*ngeff)
  integer(int32) :: sigal_bits_before((m+7)*ngeff)
  integer(int64) :: fi_bits_before(kpn*ngeff)
  integer(int64) :: qn_bits_before(kpn*ngeff)
  logical :: nconv(ngeff), nconv_before(ngeff)
  real(real32) :: sc(0:m,1,ngeff), sigal(-6:m,ngeff)
  real(real64) :: expected_raw(kpn,ngeff)
  real(real64) :: expected_source(kpn,ngeff)
  real(real64) :: fi(kpn,ngeff), qn(kpn,ngeff)
  real(real64) :: raw_response(kpn,ngeff), raw_before(kpn,ngeff)
  real(real64) :: source(kpn,ngeff), source_before(kpn,ngeff)

  callback_calls = 0
  callback_mode = 0
  nzon = [0, 1, -1, -2]
  keyflx(:,1,1) = [2, 1]
  keycur = [4, 3]
  ibc = [2, 1]
  ngind = [366, 367, 368, 369, 370]
  nconv = [.true., .false., .true., .false., .true.]

  sc = 0.0_real32
  sigal = 0.0_real32
  qn = 0.0_real64
  fi = 0.0_real64
  do group = 1, ngeff
    sc(0,1,group) = 1.0_real32
    sc(1,1,group) = transfer(int(z'3EAAAAAB', int32), 0.0_real32)
    sigal(-1,group) = 1.0_real32
    sigal(-2,group) = 0.5_real32
    qn(1,group) = 0.25_real64 * real(group, real64) + &
        2.0_real64**(-30)
    fi(1,group) = 0.5_real64 + real(group, real64) * &
        2.0_real64**(-31)
    qn(2,group) = real(group - 1, real64) + 2.0_real64**(-40)
    fi(2,group) = 1.0_real64 + real(group, real64) * &
        2.0_real64**(-30)
    fi(3,group) = 2.0_real64 + real(group, real64) * &
        2.0_real64**(-31)
    fi(4,group) = 0.5_real64 + real(group, real64) * &
        2.0_real64**(-32)
    source(:,group) = -10.0_real64 - real(group, real64)
    raw_response(:,group) = 20.0_real64 + real(group, real64)
  end do

  source_before = source
  raw_before = raw_response
  call form_expected

  qn_bits_before = transfer(qn, qn_bits_before)
  fi_bits_before = transfer(fi, fi_bits_before)
  sc_bits_before = transfer(sc, sc_bits_before)
  sigal_bits_before = transfer(sigal, sigal_bits_before)
  ngind_before = ngind
  nconv_before = nconv

  call invoke(2, status)
  call require(status == SPOR64_A2_OK, 'active-mask status')
  call require(callback_calls == 1, 'callback count')
  call require(same64(source, expected_source), 'source matrix')
  call require(same64(raw_response, expected_raw), 'raw response matrix')
  call require(transfer(raw_response(5,1), 0_int64) /= &
      transfer(real(real(raw_response(5,1), real32), real64), 0_int64), &
      'raw response has no real32 round trip')
  call require(same64(source(:,2:2), source_before(:,2:2)) .and. &
      same64(source(:,4:4), source_before(:,4:4)), &
      'inactive source columns')
  call require(all(bits64(raw_response(:,2)) == 0_int64) .and. &
      all(bits64(raw_response(:,4)) == 0_int64), &
      'inactive raw columns are positive zero')
  call require(all(qn_bits_before == transfer(qn, qn_bits_before)), &
      'qn input unchanged')
  call require(all(fi_bits_before == transfer(fi, fi_bits_before)), &
      'fi input unchanged')
  call require(all(sc_bits_before == transfer(sc, sc_bits_before)), &
      'sc input unchanged')
  call require(all(sigal_bits_before == transfer(sigal, &
      sigal_bits_before)), 'sigal input unchanged')
  call require(all(ngind_before == ngind), 'ngind input unchanged')
  call require(all(nconv_before .eqv. nconv), 'nconv input unchanged')
  print '(A)', 'SPOR64-A2 ACTIVE-MASK SOURCE-PRIMARY PASS'

  do mask = 1, 2**ngeff - 1
    do group = 1, ngeff
      nconv(group) = btest(mask, group - 1)
    end do
    source = source_before
    raw_response = raw_before
    call form_expected
    calls_before = callback_calls
    call invoke(2, status)
    call require(status == SPOR64_A2_OK, 'exhaustive mask status')
    call require(callback_calls == calls_before + 1, &
        'exhaustive mask callback count')
    call require(same64(source, expected_source), &
        'exhaustive mask source')
    call require(same64(raw_response, expected_raw), &
        'exhaustive mask response')
  end do
  nconv = nconv_before
  source = source_before
  raw_response = raw_before
  print '(A)', 'SPOR64-A2 ALL-NONEMPTY-MASKS PASS'

  source = source_before
  raw_response = raw_before
  do callback_mode = 1, 4
    source = source_before
    raw_response = raw_before
    call invoke(2, status)
    call require(status == SPOR64_A2_RESPONSE_FAILED, &
        'callback contract failure status')
    call require(same64(source, source_before), &
        'callback contract failure changed source')
    call require(same64(raw_response, raw_before), &
        'callback contract failure changed raw response')
  end do
  callback_mode = 0
  print '(A)', 'SPOR64-A2 TRANSACTIONAL FAILURE PASS'

  source = source_before
  raw_response = raw_before
  ibc(nsur) = nsur + 1
  call invoke(2, status)
  call require(status == SPOR64_A2_INVALID, 'late invalid status')
  call require(same64(source, source_before), 'late invalid source')
  call require(same64(raw_response, raw_before), 'late invalid response')
  ibc(nsur) = 1

  ngind(3) = ngind(2) + 2
  call invoke(2, status)
  call require(status == SPOR64_A2_INVALID, 'group map status')
  call require(same64(source, source_before), 'group map source')
  call require(same64(raw_response, raw_before), 'group map response')
  ngind = ngind_before

  call invoke(3, status)
  call require(status == SPOR64_A2_UNSUPPORTED, 'unsupported status')
  call require(same64(source, source_before), 'unsupported source')
  call require(same64(raw_response, raw_before), 'unsupported response')

  nconv = .false.
  call invoke(2, status)
  call require(status == SPOR64_A2_INVALID, 'empty active set status')
  call require(same64(source, source_before), 'empty active source')
  call require(same64(raw_response, raw_before), 'empty active response')
  call require(callback_calls == 36, 'callback called after preflight fail')
  nconv = nconv_before
  print '(A)', 'SPOR64-A2 FAIL-CLOSED PASS'

  print '(A)', 'SPOR64-A2 SYNTHETIC-OPERATOR-ONLY'
  print '(A)', 'SPOR64-A2 PARTIAL-SLICE-ONLY'
  print '(A)', 'SPOR64-A2 DRAGON-RUNS=0'

contains

  subroutine form_expected
    expected_source = source_before
    expected_raw = 0.0_real64
    do group = 1, ngeff
      if (.not. nconv(group)) cycle
      expected_source(2,group) = qn(2,group) + &
          real(sc(0,1,group), real64) * fi(2,group)
      expected_source(1,group) = qn(1,group) + &
          real(sc(1,1,group), real64) * fi(1,group)
      expected_source(4,group) = real(sigal(-1,group), real64) * &
          fi(3,group)
      expected_source(3,group) = real(sigal(-2,group), real64) * &
          fi(4,group)
      do i = 1, kpn
        if (mod(i, 2) == 0) then
          expected_raw(i,group) = expected_source(kpn + 1 - i,group)
        else
          expected_raw(i,group) = -expected_source(kpn + 1 - i,group)
        end if
      end do
    end do
  end subroutine form_expected


  subroutine invoke(ndim, returned_status)
    integer, intent(in) :: ndim
    integer, intent(out) :: returned_status

    call MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED(n, ndim, nzon, qn, fi, m, &
        1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, sigal, 1, &
        .false., .false., 0, ng, ngeff, ngind, nconv, &
        synthetic_primary, raw_response, returned_status)
  end subroutine invoke


  subroutine synthetic_primary(local_ngeff, local_ngind, local_nconv, &
      local_kpn, local_source, local_raw, returned_status)
    integer, intent(in) :: local_ngeff, local_kpn
    integer, intent(in) :: local_ngind(:)
    logical, intent(in) :: local_nconv(:)
    real(real64), intent(in) :: local_source(:,:)
    real(real64), intent(inout) :: local_raw(:,:)
    integer, intent(out) :: returned_status

    integer :: local_group, local_i

    callback_calls = callback_calls + 1
    call require(local_ngeff == ngeff, 'callback ngeff')
    call require(local_kpn == kpn, 'callback kpn')
    call require(all(local_ngind == ngind_before), 'callback ngind')
    call require(all(local_nconv .eqv. nconv), 'callback nconv')

    do local_group = 1, local_ngeff
      if (.not. local_nconv(local_group)) cycle
      do local_i = 1, local_kpn
        if (callback_mode == 2 .and. local_group == local_ngeff .and. &
            local_i == local_kpn) cycle
        if (mod(local_i, 2) == 0) then
          local_raw(local_i,local_group) = &
              local_source(local_kpn + 1 - local_i,local_group)
        else
          local_raw(local_i,local_group) = &
              -local_source(local_kpn + 1 - local_i,local_group)
        end if
      end do
    end do

    if (callback_mode == 3) local_raw(1,2) = 1.0_real64
    if (callback_mode == 4) then
      local_raw(1,1) = ieee_value(0.0_real64, ieee_quiet_nan)
    end if

    if (callback_mode == 1) then
      returned_status = 17
    else
      returned_status = 0
    end if
  end subroutine synthetic_primary


  subroutine require(condition, label)
    logical, intent(in) :: condition
    character(*), intent(in) :: label

    if (.not. condition) then
      write(*, '(A,1X,A)') 'SPOR64-A2 TEST FAILURE:', trim(label)
      error stop 1
    end if
  end subroutine require


  pure function bits64(values) result(bits)
    real(real64), intent(in) :: values(:)
    integer(int64) :: bits(size(values))

    bits = transfer(values, bits)
  end function bits64


  pure logical function same64(left, right)
    real(real64), intent(in) :: left(:,:), right(:,:)
    integer(int64) :: left_bits(size(left)), right_bits(size(right))

    if (any(shape(left) /= shape(right))) then
      same64 = .false.
      return
    end if
    left_bits = transfer(left, left_bits)
    right_bits = transfer(right, right_bits)
    same64 = all(left_bits == right_bits)
  end function same64

end program test_spor64_a2
