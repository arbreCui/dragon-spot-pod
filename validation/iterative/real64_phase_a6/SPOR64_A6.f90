module SPOR64_A6
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A5, only : &
      MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED, &
      SPOR64_A5_INVALID, SPOR64_A5_OK, SPOR64_A5_RESPONSE_FAILED, &
      SPOR64_A5_UNSUPPORTED
  implicit none
  private

  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(1.0d0) == real64)

  logical, parameter, public :: SPOR64_A6_DEFAULT_ENABLED = .false.
  integer, parameter, public :: SPOR64_A6_OK = SPOR64_A5_OK
  integer, parameter, public :: SPOR64_A6_UNSUPPORTED = &
      SPOR64_A5_UNSUPPORTED
  integer, parameter, public :: SPOR64_A6_INVALID = SPOR64_A5_INVALID
  integer, parameter, public :: SPOR64_A6_RESPONSE_FAILED = &
      SPOR64_A5_RESPONSE_FAILED

  public :: MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED

contains

  subroutine MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED( &
      enabled, kpsys, iftrak, nbtr, ndim, k, kpn, nlong, nzon, &
      qfr64_host, phiin64_host, m, nani, nmu, n2max, nangl, nreg, &
      nsout, ng, ngeff, ngind, nlin, nfunl, sc_by_group, source64, &
      keyflx, keycur, ibc, sigal, nconv, stis, npjjm, isch, cyclic, &
      lprism, idir, nbatch, caz1, caz2, zmu, wzmu, volume, &
      raw_response64, route_selected, status)
    logical, intent(in) :: enabled
    type(c_ptr), contiguous, intent(in) :: kpsys(:)
    integer, intent(in) :: iftrak, nbtr, ndim, k, kpn, nlong
    integer, contiguous, intent(in) :: nzon(:)
    real(real64), contiguous, intent(in) :: qfr64_host(:,:)
    real(real64), contiguous, intent(in) :: phiin64_host(:,:)
    integer, intent(in) :: m, nani, nmu, n2max, nangl, nreg, nsout
    integer, intent(in) :: ng, ngeff
    integer, contiguous, intent(in) :: ngind(:)
    integer, intent(in) :: nlin, nfunl
    real(real32), contiguous, intent(in) :: sc_by_group(0:,:,:)
    real(real64), contiguous, intent(inout) :: source64(:,:)
    integer, contiguous, target, intent(in) :: keyflx(:,:,:)
    integer, contiguous, intent(in) :: keycur(:), ibc(:)
    real(real32), contiguous, intent(in) :: sigal(-6:,:)
    logical, contiguous, intent(in) :: nconv(:)
    integer, intent(in) :: stis, npjjm, isch
    logical, intent(in) :: cyclic, lprism
    integer, intent(in) :: idir, nbatch
    real(real64), contiguous, intent(in) :: caz1(:), caz2(:)
    real(real32), contiguous, intent(in) :: zmu(:), wzmu(:), volume(:)
    real(real64), contiguous, intent(inout) :: raw_response64(:,:)
    logical, intent(out) :: route_selected
    integer, intent(out) :: status

    route_selected = .false.
    status = SPOR64_A6_UNSUPPORTED
    if (.not. enabled) return
    route_selected = .true.
    status = SPOR64_A6_INVALID
    if (isch /= 11 .or. npjjm /= 1) return
    if (ndim /= 2 .or. cyclic .or. lprism) return
    if (stis /= 1 .or. idir /= 0) return
    if (k /= nlong .or. kpn /= nlong) return
    if (nsout /= nlong-nreg) return
    if (nlong /= 14 .or. nreg /= 8 .or. nsout /= 6) return
    if (ng /= 370 .or. nani /= 1 .or. nlin /= 1 .or. nfunl /= 1) return

    if (nangl <= 0 .or. nmu <= 0) return
    if (iftrak <= 0 .or. nbtr <= 0 .or. n2max <= 0 .or. nbatch <= 0) &
        return
    if (m < 0 .or. ngeff <= 0 .or. ngeff > ng) return
    if (size(kpsys) /= ngeff) return
    if (size(nzon) /= nlong) return
    if (size(qfr64_host,1) /= kpn .or. &
        size(qfr64_host,2) /= ngeff) return
    if (size(phiin64_host,1) /= kpn .or. &
        size(phiin64_host,2) /= ngeff) return
    if (size(sc_by_group,1) /= m+1 .or. &
        size(sc_by_group,2) /= 1 .or. &
        size(sc_by_group,3) /= ngeff) return
    if (size(source64,1) /= kpn .or. &
        size(source64,2) /= ngeff) return
    if (size(keyflx,1) /= nreg .or. &
        size(keyflx,2) /= nlin .or. &
        size(keyflx,3) /= nfunl) return
    if (size(keycur) /= nsout .or. size(ibc) /= nsout) return
    if (size(sigal,1) /= m+7 .or. size(sigal,2) /= ngeff) return
    if (size(ngind) /= ngeff .or. size(nconv) /= ngeff) return
    if (size(caz1) /= nangl .or. size(caz2) /= nangl) return
    if (size(zmu) /= nmu .or. size(wzmu) /= nmu) return
    if (size(volume) /= nlong) return
    if (size(raw_response64,1) /= kpn .or. &
        size(raw_response64,2) /= ngeff) return

    call MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(nlong, &
        ndim, nzon, qfr64_host, phiin64_host, m, nani, nlin, nfunl, &
        sc_by_group, source64, kpn, nreg, keyflx, keycur, ibc, sigal, &
        stis, cyclic, lprism, idir, ng, ngeff, ngind, nconv, iftrak, &
        nbtr, n2max, nbatch, kpsys, caz1, caz2, zmu, wzmu, volume, &
        raw_response64, status)
  end subroutine MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED

end module SPOR64_A6
