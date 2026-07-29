subroutine SPOR64_A3_COMPILE_ANCHOR(anchor_status)
  use, intrinsic :: iso_c_binding, only : c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A3, only : MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED
  implicit none

  integer, intent(out) :: anchor_status
  integer, parameter :: k = 14, kpn = 14, m = 1, nangl = 1
  integer, parameter :: ngeff = 5, nmod = 4, nmu = 1, npjjm = 1
  integer, parameter :: nreg = 8, nsout = 6
  integer :: isgnr(nmod,1), keycur(nsout), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(k), pjjind(npjjm,2)
  logical :: nconv(ngeff)
  type(c_ptr) :: kpsys(ngeff)
  real(real32) :: cpo(nmu), sigal(-6:m,ngeff)
  real(real32) :: volume(k), wzmu(nmu), zmu(nmu)
  real(real64) :: caz0(nangl), caz1(nangl), caz2(nangl)
  real(real64) :: raw_response(kpn,ngeff), source(kpn,ngeff), xsi(nsout)

  kpsys = c_null_ptr
  nconv = .false.
  ngind = [366, 367, 368, 369, 370]
  nzon = [0, 1, 0, 1, 0, 1, 0, 1, -1, -2, -3, -4, -5, -6]
  keyflx(:,1,1) = [1, 2, 3, 4, 5, 6, 7, 8]
  keycur = [9, 10, 11, 12, 13, 14]
  pjjind = 1
  isgnr = 1
  cpo = 1.0_real32
  zmu = 1.0_real32
  wzmu = 1.0_real32
  sigal = 1.0_real32
  volume = 1.0_real32
  caz0 = 1.0_real64
  caz1 = 1.0_real64
  caz2 = 1.0_real64
  source = 0.0_real64
  raw_response = 0.0_real64
  xsi = 0.0_real64

  ! NCONV is deliberately empty: this call is safe-failing if invoked.
  call MCGFCF_MCGFST_R64_COMPILE_ONLY_LOCKED(99, 1, 4, 2, kpn, k, &
      nreg, m, ngeff, nangl, nmu, 1, 1, nmod, 1, 1, 1, keyflx, keycur, &
      nzon, nconv, caz0, caz1, caz2, cpo, zmu, wzmu, source, sigal, &
      isgnr, 0, nsout, 1, xsi, raw_response, kpsys, 1, npjjm, pjjind, &
      volume, 370, ngind, .false., .false., 1, anchor_status)
end subroutine SPOR64_A3_COMPILE_ANCHOR
