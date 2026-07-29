subroutine compile_fail_real64_operator()
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A3, only : MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED
  implicit none

  integer, parameter :: k = 14, kpn = 14, m = 1, nangl = 1
  integer, parameter :: ngeff = 1, nmod = 4, nmu = 1, npjjm = 1
  integer, parameter :: nreg = 8, nsout = 6
  integer :: isgnr(nmod,1), keycur(nsout), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(k), pjjind(npjjm,2), status
  logical :: nconv(ngeff)
  type(c_ptr) :: kpsys(ngeff)
  real(real32) :: cpo(nmu), wzmu(nmu), zmu(nmu)
  real(real64) :: caz0(nangl), caz1(nangl), caz2(nangl)
  real(real64) :: raw_response(kpn,ngeff), sigal(-6:m,ngeff)
  real(real64) :: source(kpn,ngeff), volume(k), xsi(nsout)

  call MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(99, 1, 4, 2, kpn, k, &
      nreg, m, ngeff, nangl, nmu, 1, 1, nmod, 1, 1, 1, keyflx, keycur, &
      nzon, nconv, caz0, caz1, caz2, cpo, zmu, wzmu, source, sigal, &
      isgnr, 0, nsout, 1, xsi, raw_response, kpsys, 1, npjjm, pjjind, &
      volume, 370, ngind, .false., .false., 1, status)
end subroutine compile_fail_real64_operator
