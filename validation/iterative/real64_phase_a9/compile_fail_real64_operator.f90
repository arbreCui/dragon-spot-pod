subroutine COMPILE_FAIL_REAL64_OPERATOR()
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A9, only : SPOR64_A9_OPERATOR_PROBE
  implicit none

  logical :: ok
  real(real64) :: operator64(1,1)

  operator64 = +0.0_real64
  call SPOR64_A9_OPERATOR_PROBE(operator64,ok)
end subroutine COMPILE_FAIL_REAL64_OPERATOR
