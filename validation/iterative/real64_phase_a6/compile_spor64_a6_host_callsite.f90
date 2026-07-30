subroutine SPOR64_A6_HOST_CALLSITE_COMPILE_ANCHOR(kpsys, route_selected, &
    anchor_status)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A6, only : &
      MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED, &
      SPOR64_A6_DEFAULT_ENABLED
  implicit none

  integer, parameter :: m = 1, n = 14, ngeff = 5, ng = 370
  integer, parameter :: nreg = 8, nsout = 6
  integer, parameter :: nangl = 2, nmu = 2
  type(c_ptr), intent(in) :: kpsys(ngeff)
  logical, intent(out) :: route_selected
  integer, intent(out) :: anchor_status
  integer :: ibc(nsout), keycur(nsout), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n)
  logical :: nconv(ngeff)
  real(real32) :: sc_by_group(0:m,1,ngeff)
  real(real32) :: sigal(-6:m,ngeff)
  real(real32) :: volume(n), wzmu(nmu), zmu(nmu)
  real(real64) :: caz1(nangl), caz2(nangl)
  real(real64) :: phiin64_host(n,ngeff), qfr64_host(n,ngeff)
  real(real64) :: raw_response64(n,ngeff), source64(n,ngeff)

  nzon = [0, 1, 0, 1, 0, 1, 0, 1, -1, -2, -3, -4, -5, -6]
  keyflx(:,1,1) = [1, 2, 3, 4, 5, 6, 7, 8]
  keycur = [9, 10, 11, 12, 13, 14]
  ibc = [1, 2, 3, 4, 5, 6]
  ngind = [366, 367, 368, 369, 370]
  nconv = .true.
  sc_by_group = 0.0_real32
  sigal = 0.0_real32
  volume = 0.0_real32
  zmu = 0.0_real32
  wzmu = 0.0_real32
  caz1 = 0.0_real64
  caz2 = 0.0_real64
  qfr64_host = 0.0_real64
  phiin64_host = 0.0_real64
  source64 = 0.0_real64
  raw_response64 = 0.0_real64

  call MCGFL1R64_DEFAULT_OFF_HOST_ADAPTER_COMPILE_ONLY_LOCKED( &
      SPOR64_A6_DEFAULT_ENABLED, kpsys, 1, 1, 2, n, n, n, nzon, &
      qfr64_host, phiin64_host, m, 1, nmu, 1, nangl, nreg, nsout, ng, &
      ngeff, ngind, 1, 1, sc_by_group, source64, keyflx, keycur, ibc, &
      sigal, nconv, 1, 1, 11, .false., .false., 0, 1, caz1, caz2, zmu, &
      wzmu, volume, raw_response64, route_selected, anchor_status)
end subroutine SPOR64_A6_HOST_CALLSITE_COMPILE_ANCHOR
