module SPOR64_A1
  use, intrinsic :: iso_fortran_env, only : real32, real64
  implicit none
  private

  integer, parameter, public :: SPOR64_OK = 0
  integer, parameter, public :: SPOR64_UNSUPPORTED = 1
  integer, parameter, public :: SPOR64_INVALID = 2
  integer, parameter, public :: SPOR64_NOT_TERMINAL = 3

  public :: SPOR64_PROMOTE_MUTABLE
  public :: MCGFCS64_LOCKED
  public :: SPOR64_TERMINAL_COPY

contains

  subroutine SPOR64_PROMOTE_MUTABLE(qn32, fi32, qn64, fi64, status)
    real(real32), intent(in) :: qn32(:), fi32(:)
    real(real64), intent(inout) :: qn64(:), fi64(:)
    integer, intent(out) :: status

    status = SPOR64_INVALID
    if (size(qn32) /= size(qn64)) return
    if (size(fi32) /= size(fi64)) return
    if (size(qn32) /= size(fi32)) return

    qn64 = real(qn32, real64)
    fi64 = real(fi32, real64)
    status = SPOR64_OK
  end subroutine SPOR64_PROMOTE_MUTABLE


  subroutine MCGFCS64_LOCKED(n, ndim, nzon, qn, fi, m, nani, nlin, &
      nfunl, sc, s, kpn, nreg, keyflx, keycur, ibc, sigal, stis, status)
    integer, intent(in) :: n, ndim, m, nani, nlin, nfunl
    integer, intent(in) :: kpn, nreg, stis
    integer, intent(in) :: nzon(:)
    integer, intent(in) :: keyflx(:,:,:), keycur(:), ibc(:)
    real(real64), intent(in) :: qn(:), fi(:)
    real(real32), intent(in) :: sc(0:,:), sigal(-6:)
    real(real64), intent(inout) :: s(:)
    integer, intent(out) :: status

    integer :: ibm, ind, ind2, ir, isur, isur2, nsur

    status = SPOR64_UNSUPPORTED
    if (ndim /= 2) return
    if (nani /= 1) return
    if (nlin /= 1) return
    if (nfunl /= 1) return
    if (stis /= 1) return

    status = SPOR64_INVALID
    if (nreg <= 0 .or. n < nreg) return
    if (m < 0 .or. kpn <= 0) return
    nsur = n - nreg
    if (size(nzon) /= n) return
    if (size(qn) /= kpn .or. size(fi) /= kpn) return
    if (size(s) /= kpn) return
    if (size(sc, 1) /= m + 1 .or. size(sc, 2) /= 1) return
    if (size(sigal) /= m + 7) return
    if (size(keyflx, 1) /= nreg) return
    if (size(keyflx, 2) /= 1 .or. size(keyflx, 3) /= 1) return
    if (size(keycur) /= nsur .or. size(ibc) /= nsur) return

    ! Validate the complete locked layout before changing S.
    do ir = 1, n
      ibm = nzon(ir)
      if (ibm < 0) then
        if (ir <= nreg) return
        if (ibm < -6) return
        isur = ir - nreg
        if (isur < 1 .or. isur > nsur) return
        isur2 = ibc(isur)
        if (isur2 < 1 .or. isur2 > nsur) return
        ind = keycur(isur)
        ind2 = keycur(isur2)
        if (ind < 0 .or. ind > kpn) return
        if (ind > 0 .and. (ind2 < 1 .or. ind2 > kpn)) return
      else
        if (ir > nreg) return
        if (ibm > m) return
        ind = keyflx(ir, 1, 1)
        if (ind < 0 .or. ind > kpn) return
      end if
    end do

    do ir = 1, n
      ibm = nzon(ir)
      if (ibm < 0) then
        isur = ir - nreg
        isur2 = ibc(isur)
        ind = keycur(isur)
        ind2 = keycur(isur2)
        if (ind > 0) then
          s(ind) = real(sigal(ibm), real64) * fi(ind2)
        end if
      else
        ind = keyflx(ir, 1, 1)
        if (ind > 0) then
          s(ind) = qn(ind) + real(sc(ibm, 1), real64) * fi(ind)
        end if
      end if
    end do
    status = SPOR64_OK
  end subroutine MCGFCS64_LOCKED


  subroutine SPOR64_TERMINAL_COPY(state64, terminal_accepted, state32, &
      status)
    real(real64), intent(in) :: state64(:)
    logical, intent(in) :: terminal_accepted
    real(real32), intent(inout) :: state32(:)
    integer, intent(out) :: status

    status = SPOR64_NOT_TERMINAL
    if (.not. terminal_accepted) return

    status = SPOR64_INVALID
    if (size(state64) /= size(state32)) return

    state32 = real(state64, real32)
    status = SPOR64_OK
  end subroutine SPOR64_TERMINAL_COPY

end module SPOR64_A1
