subroutine SPOR64_A4_COMPILE_ANCHOR(anchor_status)
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use SPOR64_A4, only : SPOR64_A4_CONTEXT, &
      MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED
  implicit none

  integer, intent(out) :: anchor_status
  integer, parameter :: m = 1, n = 14, ngeff = 5, ng = 370
  integer, parameter :: nreg = 8, kpn = 14
  integer :: ibc(n-nreg), keycur(n-nreg), keyflx(nreg,1,1)
  integer :: ngind(ngeff), nzon(n)
  logical :: nconv(ngeff)
  real(real32) :: sc(0:m,1,ngeff), sigal(-6:m,ngeff)
  real(real64) :: fi(kpn,ngeff), qn(kpn,ngeff)
  real(real64) :: raw_response(kpn,ngeff), source(kpn,ngeff)
  type(SPOR64_A4_CONTEXT) :: context

  nzon = [0, 1, 0, 1, 0, 1, 0, 1, -1, -2, -3, -4, -5, -6]
  keyflx(:,1,1) = [1, 2, 3, 4, 5, 6, 7, 8]
  keycur = [9, 10, 11, 12, 13, 14]
  ibc = [1, 2, 3, 4, 5, 6]
  ngind = [366, 367, 368, 369, 370]
  nconv = .false.
  sc = 0.0_real32
  sigal = 0.0_real32
  fi = 0.0_real64
  qn = 0.0_real64
  source = 0.0_real64
  raw_response = 0.0_real64

  ! The context remains disabled and unallocated by design.
  call MCGFL1R64_A2_A3_HOST_CLOSURE_COMPILE_ONLY_LOCKED(n, 2, nzon, qn, &
      fi, m, 1, 1, 1, sc, source, kpn, nreg, keyflx, keycur, ibc, &
      sigal, 1, .false., .false., 0, ng, ngeff, ngind, nconv, context, &
      raw_response, anchor_status)
end subroutine SPOR64_A4_COMPILE_ANCHOR
