subroutine COMPILE_FAIL_INT32_COUNTER(counter32,ok)
  use, intrinsic :: iso_fortran_env, only : int32
  use SPOR64_A9, only : SPOR64_A9_COUNTER_PROBE
  implicit none

  integer(int32), intent(in) :: counter32
  logical, intent(out) :: ok

  call SPOR64_A9_COUNTER_PROBE(counter32,ok)
end subroutine COMPILE_FAIL_INT32_COUNTER
