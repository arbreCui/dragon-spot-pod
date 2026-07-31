subroutine COMPILE_FAIL_NONCONTIGUOUS_MUTABLE(values64, ok)
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A8, only : SPOR64_A8_MUTABLE_PROBE
  implicit none
  real(real64), contiguous, intent(inout) :: values64(:,:)
  logical, intent(out) :: ok

  call SPOR64_A8_MUTABLE_PROBE(values64(:,::2), ok)
end subroutine COMPILE_FAIL_NONCONTIGUOUS_MUTABLE
