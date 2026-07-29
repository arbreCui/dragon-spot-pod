module SPOR64_A2
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite, &
      ieee_quiet_nan, ieee_value
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use SPOR64_A1, only : MCGFCS64_LOCKED, SPOR64_INVALID, SPOR64_OK, &
      SPOR64_UNSUPPORTED
  implicit none
  private

  integer, parameter, public :: SPOR64_A2_OK = SPOR64_OK
  integer, parameter, public :: SPOR64_A2_UNSUPPORTED = SPOR64_UNSUPPORTED
  integer, parameter, public :: SPOR64_A2_INVALID = SPOR64_INVALID
  integer, parameter, public :: SPOR64_A2_RESPONSE_FAILED = 4

  public :: SPOR64_POST_STIS_RAW_RESPONSE_IFACE
  public :: MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED

  abstract interface
    subroutine SPOR64_POST_STIS_RAW_RESPONSE_IFACE(ngeff, ngind, nconv, kpn, &
        source, raw_response, status)
      import :: real64
      integer, intent(in) :: ngeff, kpn
      integer, intent(in) :: ngind(:)
      logical, intent(in) :: nconv(:)
      real(real64), intent(in) :: source(:,:)
      real(real64), intent(inout) :: raw_response(:,:)
      integer, intent(out) :: status
    end subroutine SPOR64_POST_STIS_RAW_RESPONSE_IFACE
  end interface

contains

  subroutine MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED(n, ndim, nzon, qn, fi, &
      m, &
      nani, nlin, nfunl, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, stis, cyclic, lprism, idir, ng, ngeff, ngind, nconv, &
      primary_response, raw_response, status)
    integer, intent(in) :: n, ndim, m, nani, nlin, nfunl
    integer, intent(in) :: kpn, nreg, stis, idir, ng, ngeff
    integer, intent(in) :: nzon(:), ngind(:)
    integer, intent(in) :: keyflx(:,:,:), keycur(:), ibc(:)
    logical, intent(in) :: cyclic, lprism, nconv(:)
    real(real64), intent(in) :: qn(:,:), fi(:,:)
    real(real32), intent(in) :: sc(0:,:,:), sigal(-6:,:)
    real(real64), intent(inout) :: source(:,:), raw_response(:,:)
    procedure(SPOR64_POST_STIS_RAW_RESPONSE_IFACE) :: primary_response
    integer, intent(out) :: status

    integer :: group, response_status, source_status
    real(real64), allocatable :: raw_work(:,:), source_work(:,:)

    status = SPOR64_A2_UNSUPPORTED
    if (ndim /= 2) return
    if (nani /= 1) return
    if (nlin /= 1) return
    if (nfunl /= 1) return
    if (stis /= 1) return
    if (cyclic .or. lprism) return
    if (idir /= 0) return

    status = SPOR64_A2_INVALID
    if (ng <= 0 .or. ngeff <= 0 .or. ngeff > ng) return
    if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return
    if (.not. any(nconv)) return
    if (ngind(1) < 1 .or. ngind(ngeff) /= ng) return
    do group = 2, ngeff
      if (ngind(group) /= ngind(group - 1) + 1) return
    end do

    if (size(qn, 1) /= kpn .or. size(qn, 2) /= ngeff) return
    if (size(fi, 1) /= kpn .or. size(fi, 2) /= ngeff) return
    if (size(source, 1) /= kpn .or. size(source, 2) /= ngeff) return
    if (size(raw_response, 1) /= kpn .or. &
        size(raw_response, 2) /= ngeff) return
    if (size(sc, 1) /= m + 1 .or. size(sc, 2) /= 1 .or. &
        size(sc, 3) /= ngeff) return
    if (size(sigal, 1) /= m + 7 .or. size(sigal, 2) /= ngeff) return

    allocate(source_work(kpn, ngeff), raw_work(kpn, ngeff))
    source_work = source
    raw_work = 0.0_real64

    do group = 1, ngeff
      if (.not. nconv(group)) cycle
      call MCGFCS64_LOCKED(n, ndim, nzon, qn(:,group), fi(:,group), m, &
          nani, nlin, nfunl, sc(:,:,group), source_work(:,group), kpn, &
          nreg, keyflx, keycur, ibc, sigal(:,group), stis, source_status)
      if (source_status /= SPOR64_OK) then
        status = source_status
        return
      end if
    end do

    do group = 1, ngeff
      if (nconv(group)) then
        raw_work(:,group) = ieee_value(0.0_real64, ieee_quiet_nan)
      end if
    end do

    call primary_response(ngeff, ngind, nconv, kpn, source_work, &
        raw_work, response_status)
    if (response_status /= 0) then
      status = SPOR64_A2_RESPONSE_FAILED
      return
    end if

    status = SPOR64_A2_RESPONSE_FAILED
    do group = 1, ngeff
      if (nconv(group)) then
        if (.not. all(ieee_is_finite(raw_work(:,group)))) return
      else
        if (.not. all_positive_zero(raw_work(:,group))) return
      end if
    end do

    raw_response = 0.0_real64
    do group = 1, ngeff
      if (.not. nconv(group)) cycle
      source(:,group) = source_work(:,group)
      raw_response(:,group) = raw_work(:,group)
    end do
    status = SPOR64_A2_OK
  end subroutine MCGFL1R64_POST_STIS_RAW_FACADE_LOCKED


  pure logical function all_positive_zero(values)
    real(real64), intent(in) :: values(:)
    integer(int64) :: bits(size(values))

    bits = transfer(values, bits)
    all_positive_zero = all(bits == 0_int64)
  end function all_positive_zero

end module SPOR64_A2
