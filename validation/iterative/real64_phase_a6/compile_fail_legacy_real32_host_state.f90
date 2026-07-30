subroutine SPOR64_A6_COMPILE_FAIL_LEGACY_REAL32_HOST_STATE(kpsys, status)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A6, only : &
      MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED, &
      SPOR64_A6_DEFAULT_ENABLED
  implicit none

  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, nsout = 6
  integer :: ibc(nsout), keycur(nsout), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n)
  integer, intent(out) :: status
  logical :: nconv(ngeff), route_selected
  type(c_ptr), intent(in) :: kpsys(ngeff)
  real(real32) :: legacy_phiin(n,ngeff), legacy_qfr(n,ngeff)
  real(real32) :: legacy_raw_response(n,ngeff), legacy_source(n,ngeff)
  real(real32) :: sc_by_group(0:m,1,ngeff)
  real(real32) :: sigal(-6:m,ngeff), volume(n), wzmu(1), zmu(1)
  real(real64) :: caz1(1), caz2(1)

  call MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED( &
      SPOR64_A6_DEFAULT_ENABLED, kpsys, 1, 1, 2, n, n, n, nzon, &
      legacy_qfr, legacy_phiin, m, 1, 1, 1, 1, nreg, nsout, ng, ngeff, &
      ngind, 1, 1, sc_by_group, legacy_source, keyflx, keycur, ibc, &
      sigal, nconv, 1, 1, 11, .false., .false., 0, 1, caz1, caz2, zmu, &
      wzmu, volume, legacy_raw_response, route_selected, status)
end subroutine SPOR64_A6_COMPILE_FAIL_LEGACY_REAL32_HOST_STATE
