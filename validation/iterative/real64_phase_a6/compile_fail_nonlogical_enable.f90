subroutine SPOR64_A6_COMPILE_FAIL_NONLOGICAL_ENABLE(kpsys, status)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A6, only : &
      MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED
  implicit none

  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, nsout = 6
  integer :: ibc(nsout), keycur(nsout), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n), wrong_enabled
  integer, intent(out) :: status
  logical :: nconv(ngeff), route_selected
  type(c_ptr), intent(in) :: kpsys(ngeff)
  real(real32) :: sc_by_group(0:m,1,ngeff)
  real(real32) :: sigal(-6:m,ngeff), volume(n), wzmu(1), zmu(1)
  real(real64) :: caz1(1), caz2(1)
  real(real64) :: phiin64_host(n,ngeff), qfr64_host(n,ngeff)
  real(real64) :: raw_response64(n,ngeff), source64(n,ngeff)

  wrong_enabled = 0
  call MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED( &
      wrong_enabled, kpsys, 1, 1, 2, n, n, n, nzon, qfr64_host, &
      phiin64_host, m, 1, 1, 1, 1, nreg, nsout, ng, ngeff, ngind, 1, 1, &
      sc_by_group, source64, keyflx, keycur, ibc, sigal, nconv, 1, 1, &
      11, .false., .false., 0, 1, caz1, caz2, zmu, wzmu, volume, &
      raw_response64, route_selected, status)
end subroutine SPOR64_A6_COMPILE_FAIL_NONLOGICAL_ENABLE
