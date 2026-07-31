subroutine COMPILE_FAIL_REAL32_MUTABLE_TAIL(values32, ok)
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A8, only : SPOR64_A8_MUTABLE_PROBE
  implicit none
  real(real32), contiguous, intent(inout) :: values32(:,:)
  logical, intent(out) :: ok

  call SPOR64_A8_MUTABLE_PROBE(values32, ok)
end subroutine COMPILE_FAIL_REAL32_MUTABLE_TAIL
