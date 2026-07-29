subroutine SPOR64_A5_COMPILE_ANCHOR(kpsys, anchor_status)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A5, only : &
      MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED
  implicit none

  integer, intent(out) :: anchor_status
  integer, parameter :: m = 1, n = 14, ngeff = 5, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: ibc(n-nreg), keycur(n-nreg), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n)
  logical :: nconv(ngeff)
  type(c_ptr), intent(in) :: kpsys(ngeff)
  real(real32) :: sc(0:m,1,ngeff), sigal(-6:m,ngeff)
  real(real32) :: volume(n), wzmu(1), zmu(1)
  real(real64) :: caz1(1), caz2(1), fi(kpn,ngeff), qn(kpn,ngeff)
  real(real64) :: raw_response(kpn,ngeff), source(kpn,ngeff)

  nzon = [0, 1, 0, 1, 0, 1, 0, 1, -1, -2, -3, -4, -5, -6]
  keyflx(:,1,1) = [1, 2, 3, 4, 5, 6, 7, 8]
  keycur = [9, 10, 11, 12, 13, 14]
  ibc = [1, 2, 3, 4, 5, 6]
  ngind = [366, 367, 368, 369, 370]
  nconv = .true.
  sc = 0.0_real32
  sigal = 0.0_real32
  zmu = 0.0_real32
  wzmu = 0.0_real32
  volume = 0.0_real32
  caz1 = 0.0_real64
  caz2 = 0.0_real64
  fi = 0.0_real64
  qn = 0.0_real64
  source = 0.0_real64
  raw_response = 0.0_real64

  call MCGFL1R64_HOST_SHAPED_POPULATION_COMPILE_ONLY_LOCKED(n, 2, nzon, &
      qn, fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, 1, 1, 1, &
      1, kpsys, caz1, caz2, zmu, wzmu, volume, raw_response, &
      anchor_status)
end subroutine SPOR64_A5_COMPILE_ANCHOR
