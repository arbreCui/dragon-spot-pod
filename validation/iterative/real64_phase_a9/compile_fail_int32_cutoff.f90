subroutine COMPILE_FAIL_INT32_CUTOFF()
  use, intrinsic :: iso_fortran_env, only : int32
  use SPOR64_A9, only : SPOR64_A9_COUNTER_PROBE
  implicit none

  integer(int32) :: counter32
  logical :: ok

  counter32 = 0_int32
  call SPOR64_A9_COUNTER_PROBE(counter32,ok)
end subroutine COMPILE_FAIL_INT32_CUTOFF
