subroutine compile_fail_wrong_context_type()
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A4, only : &
      MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED
  implicit none

  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: context, ibc(n-nreg), keycur(n-nreg)
  integer :: keyflx(nreg,1,1), ngind(ngeff), nzon(n), status
  logical :: nconv(ngeff)
  real(real32) :: sc(0:m,1,ngeff), sigal(-6:m,ngeff)
  real(real64) :: fi(kpn,ngeff), qn(kpn,ngeff)
  real(real64) :: raw_response(kpn,ngeff), source(kpn,ngeff)

  call MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED(n, 2, nzon, qn, &
      fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, context, &
      raw_response, status)
end subroutine compile_fail_wrong_context_type
