program test_spor64_a1
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use SPOR64_A1, only : MCGFCS64_LOCKED, SPOR64_INVALID, &
      SPOR64_NOT_TERMINAL, SPOR64_OK, SPOR64_PROMOTE_MUTABLE, &
      SPOR64_TERMINAL_COPY, SPOR64_UNSUPPORTED
  implicit none

  integer, parameter :: m = 1, nreg = 2, nsur = 2, n = nreg + nsur
  integer, parameter :: kpn = 6
  integer :: empty(0), ibc(nsur), keycur(nsur)
  integer :: keyflx(nreg,1,1), nzon(n), nzon_volume(nreg)
  integer :: i, status
  integer(int32) :: sc_bits_before(m+1), sigal_bits_before(m+7)
  integer(int64) :: fi_bits_before(kpn), qn_bits_before(kpn)
  real(real32) :: fi32(kpn), qn32(kpn), sc(0:m,1), sigal(-6:m)
  real(real32) :: terminal32(kpn), terminal_before(kpn)
  real(real64) :: expected, fi64(kpn), legacy, qn64(kpn), s(kpn)
  real(real64) :: s_before(kpn), sentinel

  sentinel = -7.25_real64
  fi32 = 0.0_real32
  qn32 = 0.0_real32
  fi64 = sentinel
  qn64 = sentinel

  fi32(1) = 0.5_real32
  qn32(1) = 0.25_real32
  call SPOR64_PROMOTE_MUTABLE(qn32, fi32, qn64, fi64, status)
  call require(status == SPOR64_OK, 'entry promotion status')
  call require(same64(qn64, real(qn32, real64)), 'entry qn promotion')
  call require(same64(fi64, real(fi32, real64)), 'entry fi promotion')
  print '(A)', 'SPOR64-A1 ENTRY-PROMOTION PASS'

  nzon = [0, 1, -1, -2]
  keyflx(:,1,1) = [2, 1]
  keycur = [4, 3]
  ibc = [2, 1]
  sc = 0.0_real32
  sc(0,1) = 1.0_real32
  sc(1,1) = transfer(int(z'3EAAAAAB', int32), 0.0_real32)
  sigal = 0.0_real32
  sigal(-1) = 1.0_real32
  sigal(-2) = 0.5_real32

  qn64 = 0.0_real64
  fi64 = 0.0_real64
  qn64(2) = 2.0_real64**(-40)
  fi64(2) = 1.0_real64 + 2.0_real64**(-30)
  qn64(1) = 0.25_real64 + 2.0_real64**(-30)
  fi64(1) = 0.5_real64 + 2.0_real64**(-31)
  fi64(3) = 1.0_real64 + 2.0_real64**(-30)
  fi64(4) = 0.5_real64 + 2.0_real64**(-31)
  s = sentinel

  sc_bits_before = transfer(sc(:,1), sc_bits_before)
  sigal_bits_before = transfer(sigal, sigal_bits_before)
  qn_bits_before = transfer(qn64, qn_bits_before)
  fi_bits_before = transfer(fi64, fi_bits_before)

  call MCGFCS64_LOCKED(n, 2, nzon, qn64, fi64, m, 1, 1, 1, &
      sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, 1, status)
  call require(status == SPOR64_OK, 'locked source status')

  expected = 1.0_real64 + 2.0_real64**(-30) + 2.0_real64**(-40)
  call require(bits64(s(2)) == bits64(expected), 'volume real64 source')
  legacy = real(real(qn64(2), real32) + &
      sc(0,1) * real(fi64(2), real32), real64)
  call require(bits64(s(2)) /= bits64(legacy), 'volume no real32 round trip')
  expected = qn64(1) + real(sc(1,1), real64) * fi64(1)
  call require(bits64(s(1)) == bits64(expected), &
      'exact binary32 coefficient promotion')
  legacy = real(real(qn64(1), real32), real64) + &
      real(sc(1,1), real64) * fi64(1)
  call require(bits64(s(1)) /= bits64(legacy), &
      'qn has no real32 round trip')
  call require(bits64(s(4)) == bits64(fi64(3)), 'surface response one')
  call require(bits64(s(3)) == bits64(0.5_real64 * fi64(4)), &
      'surface response two')
  call require(bits64(s(5)) == bits64(sentinel) .and. &
      bits64(s(6)) == bits64(sentinel), &
      'unaddressed source entries')
  call require(all(sc_bits_before == transfer(sc(:,1), sc_bits_before)), &
      'sc input unchanged')
  call require(all(sigal_bits_before == transfer(sigal, sigal_bits_before)), &
      'sigal input unchanged')
  call require(all(qn_bits_before == transfer(qn64, qn_bits_before)), &
      'qn input unchanged')
  call require(all(fi_bits_before == transfer(fi64, fi_bits_before)), &
      'fi input unchanged')
  print '(A)', 'SPOR64-A1 LOCKED-SOURCE PASS'

  nzon_volume = nzon(:nreg)
  s = sentinel
  call MCGFCS64_LOCKED(nreg, 2, nzon_volume, qn64, fi64, m, 1, 1, 1, &
      sc, s, kpn, nreg, keyflx, empty, empty, sigal, 1, status)
  call require(status == SPOR64_OK, 'zero-surface layout status')
  call require(bits64(s(1)) == bits64(qn64(1) + &
      real(sc(1,1), real64) * fi64(1)), &
      'zero-surface volume one')
  call require(bits64(s(2)) == bits64(1.0_real64 + &
      2.0_real64**(-30) + 2.0_real64**(-40)), &
      'zero-surface volume two')
  call require(all([(bits64(s(i)) == bits64(sentinel), i = 3, kpn)]), &
      'zero-surface unmapped entries')

  s = sentinel
  s_before = s
  call MCGFCS64_LOCKED(n, 3, nzon, qn64, fi64, m, 1, 1, 1, &
      sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, 1, status)
  call require(status == SPOR64_UNSUPPORTED, 'unsupported branch status')
  call require(same64(s, s_before), 'unsupported branch mutated state')

  ibc(nsur) = nsur + 1
  call MCGFCS64_LOCKED(n, 2, nzon, qn64, fi64, m, 1, 1, 1, &
      sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, 1, status)
  call require(status == SPOR64_INVALID, 'invalid layout status')
  call require(same64(s, s_before), 'invalid layout mutated state')
  ibc(nsur) = 1

  keyflx(2,1,1) = 0
  s = sentinel
  call MCGFCS64_LOCKED(n, 2, nzon, qn64, fi64, m, 1, 1, 1, &
      sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, 1, status)
  call require(status == SPOR64_OK, 'zero-key status')
  call require(bits64(s(1)) == bits64(sentinel), &
      'zero key did not preserve source')
  print '(A)', 'SPOR64-A1 FAIL-CLOSED PASS'

  terminal32 = -3.0_real32
  terminal_before = terminal32
  call SPOR64_TERMINAL_COPY(s, .false., terminal32, status)
  call require(status == SPOR64_NOT_TERMINAL, 'preterminal copy status')
  call require(same32(terminal32, terminal_before), &
      'preterminal copy mutated output')

  call SPOR64_TERMINAL_COPY(s, .true., terminal32, status)
  call require(status == SPOR64_OK, 'terminal copy status')
  call require(same32(terminal32, real(s, real32)), 'terminal copy values')
  print '(A)', 'SPOR64-A1 TERMINAL-COPY PASS'
  print '(A)', 'SPOR64-A1 PARTIAL-SLICE-ONLY'
  print '(A)', 'SPOR64-A1 DRAGON-RUNS=0'

contains

  subroutine require(condition, label)
    logical, intent(in) :: condition
    character(*), intent(in) :: label

    if (.not. condition) then
      write(*, '(A,1X,A)') 'SPOR64-A1 TEST FAILURE:', trim(label)
      error stop 1
    end if
  end subroutine require


  pure integer(int64) function bits64(value)
    real(real64), intent(in) :: value

    bits64 = transfer(value, 0_int64)
  end function bits64


  pure logical function same32(left, right)
    real(real32), intent(in) :: left(:), right(:)
    integer(int32) :: left_bits(size(left)), right_bits(size(right))

    if (size(left) /= size(right)) then
      same32 = .false.
      return
    end if
    left_bits = transfer(left, left_bits)
    right_bits = transfer(right, right_bits)
    same32 = all(left_bits == right_bits)
  end function same32


  pure logical function same64(left, right)
    real(real64), intent(in) :: left(:), right(:)
    integer(int64) :: left_bits(size(left)), right_bits(size(right))

    if (size(left) /= size(right)) then
      same64 = .false.
      return
    end if
    left_bits = transfer(left, left_bits)
    right_bits = transfer(right, right_bits)
    same64 = all(left_bits == right_bits)
  end function same64

end program test_spor64_a1
