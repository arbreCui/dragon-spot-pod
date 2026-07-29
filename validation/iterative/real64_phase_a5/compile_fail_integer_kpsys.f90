subroutine SPOR64_A5_COMPILE_FAIL_INTEGER_KPSYS(status)
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A5, only : &
      MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED
  implicit none

  integer, intent(out) :: status
  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: ibc(6), keycur(6), keyflx(8,1,1), ngind(1), nzon(14)
  integer :: wrong_kpsys(1)
  logical :: nconv(1)
  real(real32) :: sc(0:m,1,1), sigal(-6:m,1)
  real(real32) :: volume(14), wzmu(1), zmu(1)
  real(real64) :: caz1(1), caz2(1), fi(14,1), qn(14,1)
  real(real64) :: raw_response(14,1), source(14,1)

  call MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(n, 2, nzon, &
      qn, fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, 1, 1, 1, &
      1, wrong_kpsys, caz1, caz2, zmu, wzmu, volume, raw_response, status)
end subroutine SPOR64_A5_COMPILE_FAIL_INTEGER_KPSYS
