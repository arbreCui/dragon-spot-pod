subroutine SPOR64_A5_COMPILE_FAIL_NONCONTIGUOUS_POPULATION_ACTUAL(kpsys, &
    caz_storage, status)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A5, only : &
      MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED
  implicit none

  integer, intent(out) :: status
  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: ibc(6), keycur(6), keyflx(8,1,1), ngind(1), nzon(14)
  logical :: nconv(1)
  type(c_ptr), intent(in) :: kpsys(1)
  real(real32) :: sc(0:m,1,1), sigal(-6:m,1)
  real(real32) :: volume(14), wzmu(1), zmu(1)
  real(real64), intent(in) :: caz_storage(2,2)
  real(real64) :: caz2(2), fi(14,1), qn(14,1)
  real(real64) :: raw_response(14,1), source(14,1)

  call MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(n, 2, nzon, &
      qn, fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, 1, 1, 1, &
      1, kpsys, caz_storage(1,:), caz2, zmu, wzmu, volume, raw_response, &
      status)
end subroutine SPOR64_A5_COMPILE_FAIL_NONCONTIGUOUS_POPULATION_ACTUAL
