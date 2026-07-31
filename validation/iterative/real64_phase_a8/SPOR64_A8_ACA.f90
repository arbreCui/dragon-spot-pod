module SPOR64_A8_ACA
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none
  private

  real(real32), parameter :: INHERITED_EPSMAX32 = 1.0e-7_real32
  real(real64), parameter :: INHERITED_EPSMAX64 = &
      real(INHERITED_EPSMAX32, real64)
  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(0.0) == real32 .and. kind(0.0d0) == real64)
  integer, parameter :: epsmax_bits_guard = 1 / merge(1, 0, &
      transfer(INHERITED_EPSMAX32, 0_int32) == &
      int(z'33d6bf95', int32))

  public :: MCGFCR64
  public :: MCGPRA64
  public :: MCGABG64
  public :: MCGFCA64
  public :: SPOR64_A8_ACA_SHAPE_PROBE

  interface
    subroutine MSRLUS1(lforw, n, lc, im, mcu, ju, iludf32, cf32, &
        xin64, xout64)
      import :: real32, real64
      logical, intent(in) :: lforw
      integer, intent(in) :: n, lc
      integer, intent(in) :: im(n+1), mcu(lc), ju(n)
      real(real32), intent(in) :: iludf32(n), cf32(lc)
      real(real64) :: xin64(n), xout64(n)
    end subroutine MSRLUS1

    function DDOT(n, x64, incx, y64, incy) result(value64)
      import :: real64
      integer, intent(in) :: n, incx, incy
      real(real64), intent(in) :: x64(*), y64(*)
      real(real64) :: value64
    end function DDOT
  end interface

contains

  subroutine SPOR64_A8_ACA_SHAPE_PROBE(n1, lc, im, cf32, &
      cutoff_delta64, ok)
    integer, intent(in) :: n1, lc
    integer, intent(in) :: im(15)
    real(real32), intent(in) :: cf32(32)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    cutoff_delta64 = 0_int64
    ok = .false.
    if (n1 /= 14 .or. lc /= 32) return
    if (size(im) /= n1+1 .or. size(cf32) /= lc) return
    ok = .true.
  end subroutine SPOR64_A8_ACA_SHAPE_PROBE


  subroutine MCGFCR64(kpn, n1, nreg, m, ngeff, ii, keyflx2, keycur, &
      nzon, iperm, fi64, fiold64, sc32, ar64, ok)
    integer, intent(in) :: kpn, n1, nreg, m, ngeff, ii
    integer, intent(in) :: keyflx2(nreg,1), keycur(n1-nreg)
    integer, intent(in) :: nzon(n1), iperm(n1)
    real(real64), intent(in) :: fi64(kpn,ngeff)
    real(real64), intent(in) :: fiold64(kpn,ngeff)
    real(real32), intent(in) :: sc32(0:m,1)
    real(real64), intent(out) :: ar64(n1)
    logical, intent(out) :: ok

    integer :: i, ibm, ind, j
    real(real64) :: sigc64

    ar64 = +0.0_real64
    ok = .false.
    if (kpn <= 0 .or. n1 <= 0 .or. nreg <= 0) return
    if (nreg > n1 .or. m < 0 .or. ngeff <= 0) return
    if (ii < 1 .or. ii > ngeff) return
    if (.not. all(ieee_is_finite(fi64(:,ii)))) return
    if (.not. all(ieee_is_finite(fiold64(:,ii)))) return
    if (.not. all(ieee_is_finite(sc32))) return

    ! This checked interface structurally locks MACFLG=.false.; the
    ! inactive NJJ/IJJ/IPOS/XSCAT arguments do not exist here.
    do i = 1, n1
      j = iperm(i)
      if (j < 1 .or. j > n1) return
      ibm = nzon(j)
      if (j <= nreg) then
        if (ibm < 0 .or. ibm > m) return
        ind = keyflx2(j,1)
      else
        if (ibm >= 0) return
        ind = keycur(j-nreg)
      end if
      if (ind < 1 .or. ind > kpn) return
    end do

    do i = 1, n1
      j = iperm(i)
      ibm = nzon(j)
      if (ibm >= 0) then
        sigc64 = real(sc32(ibm,1), real64)
        ind = keyflx2(j,1)
      else
        sigc64 = 0.5_real64
        ind = keycur(j-nreg)
      end if
      ar64(i) = (fi64(ind,ii) - fiold64(ind,ii)) * sigc64
    end do
    ok = all(ieee_is_finite(ar64))
  end subroutine MCGFCR64


  subroutine MCGPRA64(lforw, opt, paca, flout, nlong, lc, im, mcu, ju, &
      diagm32, cm32, iludf32, ilucf32, diagf32, xin64, xout64, lc0, &
      im0, mcu0, cf32, ok)
    logical, intent(in) :: lforw, flout
    integer, intent(in) :: opt, paca, nlong, lc, lc0
    integer, intent(in) :: im(nlong+1), mcu(lc), ju(nlong)
    integer, intent(in) :: im0(*), mcu0(*)
    real(real32), intent(in) :: diagm32(nlong), cm32(lc)
    real(real32), intent(in) :: iludf32(nlong), ilucf32(lc)
    real(real32), intent(in) :: diagf32(nlong), cf32(lc)
    real(real64), intent(inout) :: xin64(nlong), xout64(nlong)
    logical, intent(out) :: ok

    integer :: i, ij, j
    real(real64) :: ff64

    ok = .false.
    if (paca /= 4 .or. lc0 /= 0) return
    if (opt < 1 .or. opt > 3) return
    if (nlong <= 0 .or. lc <= 0) return
    ! Prove the inactive formals are conforming without reading a value.
    if (size(ilucf32) /= lc .or. size(diagf32) /= nlong) return
    if (lbound(im0,1) /= 1 .or. lbound(mcu0,1) /= 1) return
    if (im(1) /= 0) return
    do i = 1, nlong
      if (im(i) < 0 .or. im(i) > lc) return
      if (im(i+1) < im(i) .or. im(i+1) > lc) return
      if (ju(i) < im(i)+1 .or. ju(i) > im(i+1)+1) return
    end do
    if (.not. all(ieee_is_finite(xin64))) return
    if (mod(opt,2) == 0) then
      if (.not. all(ieee_is_finite(xout64))) return
    end if
    if (mod(opt,2) == 1) then
      if (.not. all(ieee_is_finite(diagm32))) return
      if (.not. all(ieee_is_finite(cm32))) return
    end if
    if (opt/2 == 1) then
      if (.not. all(ieee_is_finite(iludf32))) return
      if (.not. all(ieee_is_finite(cf32))) return
    end if

    if (mod(opt,2) == 1) then
      if (lforw) then
        ! Preserve the legacy direct row order exactly.
        do i = 1, nlong
          ff64 = real(diagm32(i), real64) * xin64(i)
          do ij = im(i)+1, im(i+1)
            j = mcu(ij)
            if (j > 0 .and. j <= nlong) then
              ff64 = ff64 + real(cm32(ij), real64) * xin64(j)
            end if
          end do
          xout64(i) = ff64
        end do
      else
        ! Preserve the legacy transpose accumulation order exactly.
        do i = 1, nlong
          xout64(i) = real(diagm32(i), real64) * xin64(i)
        end do
        do i = 1, nlong
          do ij = im(i)+1, im(i+1)
            j = mcu(ij)
            if (j > 0 .and. j <= nlong) then
              xout64(j) = xout64(j) + &
                  real(cm32(ij), real64) * xin64(i)
            end if
          end do
        end do
      end if
    end if

    if (opt/2 == 1) then
      ! PACA=4 is the only admitted preconditioner.  ILUCF32,
      ! DIAGF32, IM0 and MCU0 are conforming but intentionally unread.
      if (flout) then
        call MSRLUS1(lforw, nlong, lc, im, mcu, ju, iludf32, cf32, &
            xout64, xin64)
      else
        call MSRLUS1(lforw, nlong, lc, im, mcu, ju, iludf32, cf32, &
            xout64, xout64)
      end if
    else if (flout) then
      xin64 = xout64
    end if

    if (flout) then
      ok = all(ieee_is_finite(xin64))
    else
      ok = all(ieee_is_finite(xout64))
    end if
  end subroutine MCGPRA64


  subroutine MCGABG64(lforw, paca, n, lc, epsm64, maxm, im, mcu, ju, &
      diagf32, cf32, iludf32, ilucf32, rhs64, f64, fac64, lc0, im0, &
      mcu0, cutoff_delta64, ok)
    logical, intent(in) :: lforw
    integer, intent(in) :: paca, n, lc, maxm, lc0
    integer, intent(in) :: im(n+1), mcu(lc), ju(n), im0(*), mcu0(*)
    real(real64), intent(in) :: epsm64, rhs64(n), fac64
    real(real32), intent(in) :: diagf32(n), cf32(lc), iludf32(n)
    real(real32), intent(in) :: ilucf32(lc)
    real(real64), intent(out) :: f64(n)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: i, iter, j
    real(real64) :: asin64, asin2_64, asin_norm2_64
    real(real64) :: aux64(2), bi64, cn64, denom64
    real(real64) :: cutoff_threshold64, cutoff_zero64
    real(real64) :: eps64, eps2_64, eps2_zero64, epsinf64
    real(real64) :: epsinf_zero64, fnorm64, r64, rhsn64
    real(real64) :: rt1_64, sin64, sin_norm2_64, sq2_64, wi64
    logical :: child_ok, guard_live, guard_zero
    real(real64), allocatable :: api64(:), asi64(:), pi64(:), ri64(:)
    real(real64), allocatable :: rhs_work64(:), rot64(:), si64(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    f64 = +0.0_real64
    if (paca /= 4 .or. lc0 /= 0) return
    if (n <= 0 .or. lc <= 0 .or. maxm < 0) return
    if (.not. ieee_is_finite(epsm64) .or. epsm64 < 0.0_real64) return
    if (.not. ieee_is_finite(fac64) .or. fac64 < 0.0_real64) return
    if (.not. all(ieee_is_finite(rhs64))) return

    allocate(api64(n), asi64(n), pi64(n), ri64(n), rhs_work64(n), &
        rot64(n), si64(n))
    api64 = +0.0_real64
    asi64 = +0.0_real64
    pi64 = +0.0_real64
    ri64 = +0.0_real64
    rhs_work64 = rhs64
    rot64 = +0.0_real64
    si64 = +0.0_real64

    sq2_64 = 1.0_real64 / sqrt(2.0_real64)
    epsinf64 = INHERITED_EPSMAX64 * fac64
    epsinf_zero64 = 0.0_real64 * fac64
    if (.not. ieee_is_finite(epsinf64)) return

    rhsn64 = 0.0_real64
    do i = 1, n
      rhsn64 = max(rhsn64, abs(rhs64(i)))
    end do

    ! Inherited-cutoff site 1: RHSN < EPSINF.
    guard_live = rhsn64 < epsinf64
    guard_zero = rhsn64 < epsinf_zero64
    if (guard_live .neqv. guard_zero) then
      cutoff_delta64 = cutoff_delta64 + 1_int64
    end if
    if (guard_live) then
      ok = .true.
      return
    end if

    eps2_64 = INHERITED_EPSMAX64 * rhsn64
    eps2_zero64 = 0.0_real64 * rhsn64
    eps2_64 = eps2_64 * eps2_64
    eps2_zero64 = eps2_zero64 * eps2_zero64
    if (.not. ieee_is_finite(eps2_64)) return

    call MCGPRA64(lforw, 3, paca, .false., n, lc, im, mcu, ju, &
        diagf32, cf32, iludf32, ilucf32, diagf32, rhs_work64, ri64, &
        lc0, im0, mcu0, cf32, child_ok)
    if (.not. child_ok) return

    do i = 1, n
      f64(i) = rhs64(i)
      ri64(i) = rhs64(i) - ri64(i)
      pi64(i) = ri64(i)
      rot64(i) = ri64(i)
    end do
    r64 = DDOT(n, ri64, 1, ri64, 1)
    fnorm64 = DDOT(n, f64, 1, f64, 1)
    if (.not. ieee_is_finite(r64) .or. r64 < 0.0_real64) return
    if (.not. ieee_is_finite(fnorm64) .or. fnorm64 <= 0.0_real64) return
    eps64 = sqrt(r64/fnorm64)
    if (.not. ieee_is_finite(eps64)) return
    if (eps64 <= epsm64) then
      ok = .true.
      return
    end if
    aux64(1) = r64

    iter = 0
    do while (iter < maxm)
      iter = iter + 1
      api64 = +0.0_real64
      call MCGPRA64(lforw, 3, paca, .false., n, lc, im, mcu, ju, &
          diagf32, cf32, iludf32, ilucf32, diagf32, pi64, api64, lc0, &
          im0, mcu0, cf32, child_ok)
      if (.not. child_ok) return

      denom64 = DDOT(n, api64, 1, rot64, 1)
      if (.not. ieee_is_finite(denom64) .or. &
          abs(denom64) <= 0.0_real64) &
          return
      aux64(2) = aux64(1) / denom64
      if (.not. ieee_is_finite(aux64(2))) return
      do j = 1, n
        si64(j) = ri64(j) - aux64(2) * api64(j)
      end do

      iter = iter + 1
      asi64 = +0.0_real64
      call MCGPRA64(lforw, 3, paca, .false., n, lc, im, mcu, ju, &
          diagf32, cf32, iludf32, ilucf32, diagf32, si64, asi64, lc0, &
          im0, mcu0, cf32, child_ok)
      if (.not. child_ok) return

      asin2_64 = DDOT(n, asi64, 1, si64, 1)
      asin_norm2_64 = DDOT(n, asi64, 1, asi64, 1)
      sin_norm2_64 = DDOT(n, si64, 1, si64, 1)
      if (.not. ieee_is_finite(asin2_64)) return
      if (.not. ieee_is_finite(asin_norm2_64) .or. &
          asin_norm2_64 < 0.0_real64) return
      if (.not. ieee_is_finite(sin_norm2_64) .or. &
          sin_norm2_64 < 0.0_real64) return
      asin64 = sqrt(asin_norm2_64)
      sin64 = sqrt(sin_norm2_64)
      cn64 = asin64 * sin64
      if (.not. ieee_is_finite(cn64)) return

      ! Inherited-cutoff site 2: CN > EPSMAX*ASIN2.
      cutoff_threshold64 = INHERITED_EPSMAX64 * asin2_64
      cutoff_zero64 = 0.0_real64 * asin2_64
      if (.not. ieee_is_finite(cutoff_threshold64)) return
      guard_live = cn64 > cutoff_threshold64
      guard_zero = cn64 > cutoff_zero64
      if (guard_live .neqv. guard_zero) then
        cutoff_delta64 = cutoff_delta64 + 1_int64
      end if
      if (guard_live) then
        if (cn64 <= 0.0_real64 .or. asin64 <= 0.0_real64) return
        cn64 = asin2_64 / cn64
        wi64 = max(abs(cn64), sq2_64) * sin64 / asin64
        wi64 = sign(wi64, cn64)
      else
        wi64 = 1.0_real64
      end if
      if (.not. ieee_is_finite(wi64)) return

      do j = 1, n
        f64(j) = f64(j) + aux64(2) * pi64(j) + wi64 * si64(j)
        ri64(j) = si64(j) - wi64 * asi64(j)
      end do
      r64 = DDOT(n, ri64, 1, ri64, 1)
      fnorm64 = DDOT(n, f64, 1, f64, 1)
      if (.not. ieee_is_finite(r64) .or. r64 < 0.0_real64) return
      if (.not. ieee_is_finite(fnorm64) .or. fnorm64 < 0.0_real64) &
          return

      ! Inherited-cutoff site 3: the in-loop FNORM < EPS2.
      guard_live = fnorm64 < eps2_64
      guard_zero = fnorm64 < eps2_zero64
      if (guard_live .neqv. guard_zero) then
        cutoff_delta64 = cutoff_delta64 + 1_int64
      end if
      if (guard_live) then
        f64 = +0.0_real64
        ok = .true.
        return
      end if
      if (fnorm64 <= 0.0_real64) return
      eps64 = sqrt(r64/fnorm64)
      if (.not. ieee_is_finite(eps64)) return
      if (eps64 <= epsm64) exit

      rt1_64 = aux64(1)
      aux64(1) = DDOT(n, ri64, 1, rot64, 1)
      if (.not. ieee_is_finite(aux64(1))) return
      if (.not. ieee_is_finite(rt1_64) .or. &
          abs(rt1_64) <= 0.0_real64 .or. &
          abs(wi64) <= 0.0_real64) return
      bi64 = aux64(1) / rt1_64 * aux64(2) / wi64
      if (.not. ieee_is_finite(bi64)) return
      do j = 1, n
        pi64(j) = ri64(j) + bi64 * (pi64(j) - wi64 * api64(j))
      end do
    end do

    iter = iter + 1
    ri64 = +0.0_real64
    call MCGPRA64(lforw, 3, paca, .false., n, lc, im, mcu, ju, &
        diagf32, cf32, iludf32, ilucf32, diagf32, f64, ri64, lc0, &
        im0, mcu0, cf32, child_ok)
    if (.not. child_ok) return
    do i = 1, n
      ri64(i) = rhs64(i) - ri64(i)
    end do
    r64 = DDOT(n, ri64, 1, ri64, 1)
    fnorm64 = DDOT(n, f64, 1, f64, 1)
    if (.not. ieee_is_finite(r64) .or. r64 < 0.0_real64) return
    if (.not. ieee_is_finite(fnorm64) .or. fnorm64 < 0.0_real64) return

    ! Inherited-cutoff site 4: the final FNORM < EPS2.
    guard_live = fnorm64 < eps2_64
    guard_zero = fnorm64 < eps2_zero64
    if (guard_live .neqv. guard_zero) then
      cutoff_delta64 = cutoff_delta64 + 1_int64
    end if
    if (guard_live) f64 = +0.0_real64
    ok = .true.
  end subroutine MCGABG64


  subroutine MCGFCA64(n1, ngeff, kpn, nreg, m, lc, lforw, paca, &
      keyflx2, keycur, nzon, nconv, maxm, epsaca64, response64, &
      phiin64, sc_by_group32, im, mcu, iperm, ju, diagq32, cq32, &
      iludf32, cf32, diagf32, cutoff_delta64, ok)
    integer, intent(in) :: n1, ngeff, kpn, nreg, m, lc, paca, maxm
    logical, intent(in) :: lforw, nconv(ngeff)
    integer, intent(in) :: keyflx2(nreg,1), keycur(n1-nreg), nzon(n1)
    integer, intent(in) :: im(n1+1), mcu(lc), iperm(n1), ju(n1)
    real(real64), intent(in) :: epsaca64, phiin64(kpn,ngeff)
    real(real64), intent(inout) :: response64(kpn,ngeff)
    real(real32), intent(in) :: sc_by_group32(0:m,1,ngeff)
    real(real32), intent(in) :: diagq32(n1,ngeff), cq32(lc,ngeff)
    real(real32), intent(in) :: iludf32(n1,ngeff), cf32(lc,ngeff)
    real(real32), intent(in) :: diagf32(n1,ngeff)
    integer(int64), intent(out) :: cutoff_delta64
    logical, intent(out) :: ok

    integer :: i, ii, ind, j
    integer :: im0_inactive(1), mcu0_inactive(1)
    integer(int64) :: child_delta64
    logical :: child_ok
    logical, allocatable :: seen(:)
    real(real64) :: flxn64
    real(real64), allocatable :: ar64(:,:), psi64(:,:)
    real(real32), allocatable :: diagf_inactive32(:)
    real(real32), allocatable :: lucf_inactive32(:)

    cutoff_delta64 = 0_int64
    ok = .false.
    if (paca /= 4) return
    if (n1 <= 0 .or. ngeff <= 0 .or. kpn <= 0) return
    if (nreg <= 0 .or. nreg > n1 .or. m < 0 .or. lc <= 0) return
    if (maxm < 0) return
    if (.not. ieee_is_finite(epsaca64) .or. &
        epsaca64 < 0.0_real64) return
    if (.not. all(ieee_is_finite(response64))) return
    if (.not. all(ieee_is_finite(phiin64))) return
    if (.not. all(ieee_is_finite(sc_by_group32))) return
    if (.not. all(ieee_is_finite(diagq32))) return
    if (.not. all(ieee_is_finite(cq32))) return
    if (.not. all(ieee_is_finite(iludf32))) return
    if (.not. all(ieee_is_finite(cf32))) return
    if (.not. all(ieee_is_finite(diagf32))) return

    allocate(seen(n1))
    seen = .false.
    do i = 1, n1
      j = iperm(i)
      if (j < 1 .or. j > n1) return
      if (seen(j)) return
      seen(j) = .true.
    end do

    allocate(ar64(n1,ngeff), psi64(n1,ngeff))
    allocate(lucf_inactive32(lc), diagf_inactive32(n1))
    ar64 = +0.0_real64
    psi64 = +0.0_real64
    lucf_inactive32 = +0.0_real32
    diagf_inactive32 = +0.0_real32
    im0_inactive(1) = 0
    mcu0_inactive(1) = 0

    ! Preserve the legacy phase order: all residuals, all group solves,
    ! then all corrections.  The locked branch has no group coupling.
    do ii = 1, ngeff
      if (nconv(ii)) then
        call MCGFCR64(kpn, n1, nreg, m, ngeff, ii, keyflx2, keycur, &
            nzon, iperm, response64, phiin64, sc_by_group32(:,:,ii), &
            ar64(:,ii), child_ok)
        if (.not. child_ok) return
      end if
    end do

    do ii = 1, ngeff
      if (nconv(ii)) then
        flxn64 = 0.0_real64
        do i = 1, nreg
          ind = keyflx2(i,1)
          if (ind < 1 .or. ind > kpn) return
          flxn64 = max(flxn64, abs(response64(ind,ii)))
        end do

        ! DIAGF_INACTIVE32 is used only by this direct pre-MCGABG call.
        call MCGPRA64(lforw, 3, paca, .true., n1, lc, im, mcu, ju, &
            diagq32(:,ii), cq32(:,ii), iludf32(:,ii), &
            lucf_inactive32, diagf_inactive32, ar64(:,ii), &
            psi64(:,ii), 0, im0_inactive, mcu0_inactive, cf32(:,ii), &
            child_ok)
        if (.not. child_ok) return

        child_delta64 = 0_int64
        ! MCGABG64 receives the active DIAGF32 record, never the inactive
        ! direct-call placeholder.
        call MCGABG64(lforw, paca, n1, lc, epsaca64, maxm, im, mcu, &
            ju, diagf32(:,ii), cf32(:,ii), iludf32(:,ii), &
            lucf_inactive32, ar64(:,ii), psi64(:,ii), flxn64, 0, &
            im0_inactive, mcu0_inactive, child_delta64, child_ok)
        cutoff_delta64 = cutoff_delta64 + child_delta64
        if (.not. child_ok) return
      end if
    end do

    do ii = 1, ngeff
      if (nconv(ii)) then
        do i = 1, n1
          j = iperm(i)
          if (nzon(j) >= 0) then
            ind = keyflx2(j,1)
          else
            ind = keycur(j-nreg)
          end if
          response64(ind,ii) = response64(ind,ii) + psi64(i,ii)
        end do
      end if
    end do
    ok = .true.
  end subroutine MCGFCA64

end module SPOR64_A8_ACA
