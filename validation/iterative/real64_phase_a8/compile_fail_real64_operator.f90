subroutine COMPILE_FAIL_REAL64_OPERATOR(sc64, sigal64, ok)
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A8, only : SPOR64_A8_OPERATOR_PROBE
  implicit none
  real(real64), intent(in) :: sc64(0:8,1)
  real(real64), intent(in) :: sigal64(-6:8)
  logical, intent(out) :: ok

  call SPOR64_A8_OPERATOR_PROBE(sc64, sigal64, ok)
end subroutine COMPILE_FAIL_REAL64_OPERATOR
