subroutine compile_fail_real32_mutable()
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A4, only : SPOR64_A4_CONTEXT, &
      MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED
  implicit none

  integer, parameter :: m = 1, n = 14, ngeff = 1, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: ibc(n-nreg), keycur(n-nreg), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n), status
  logical :: nconv(ngeff)
  real(real32) :: fi(kpn,ngeff), qn(kpn,ngeff)
  real(real32) :: raw_response(kpn,ngeff), source(kpn,ngeff)
  real(real32) :: sc(0:m,1,ngeff), sigal(-6:m,ngeff)
  type(SPOR64_A4_CONTEXT) :: context

  call MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED(n, 2, nzon, qn, &
      fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, context, &
      raw_response, status)
end subroutine compile_fail_real32_mutable
