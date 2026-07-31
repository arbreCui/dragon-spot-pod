subroutine COMPILE_FAIL_REAL32_STATE()
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A9, only : SPOR64_A9_STATE_PROBE
  implicit none

  logical :: ok
  real(real32) :: state32(1,1,1)

  state32 = +0.0_real32
  call SPOR64_A9_STATE_PROBE(state32,ok)
end subroutine COMPILE_FAIL_REAL32_STATE
