program compile_fail_real32_actual
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A1, only : MCGFCS64_LOCKED
  implicit none

  integer, parameter :: m = 0, nreg = 1, n = 2, kpn = 2
  integer :: ibc(1), keycur(1), keyflx(1,1,1), nzon(n), status
  real(real32) :: fi(kpn), qn(kpn), s(kpn), sc(0:m,1), sigal(-6:m)

  ibc = 1
  keycur = 2
  keyflx = 1
  nzon = [0, -1]
  fi = 1.0_real32
  qn = 1.0_real32
  s = 0.0_real32
  sc = 1.0_real32
  sigal = 1.0_real32

  ! This call must not compile: mutable QN/FI/S are required to be REAL64.
  call MCGFCS64_LOCKED(n, 2, nzon, qn, fi, m, 1, 1, 1, sc, s, kpn, &
      nreg, keyflx, keycur, ibc, sigal, 1, status)
end program compile_fail_real32_actual
