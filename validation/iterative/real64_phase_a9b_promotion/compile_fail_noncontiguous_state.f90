subroutine COMPILE_FAIL_NONCONTIGUOUS_STATE(state64,ok)
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A9, only : SPOR64_A9_STATE_PROBE
  implicit none

  real(real64), contiguous, intent(in) :: state64(:,:,:)
  logical, intent(out) :: ok

  call SPOR64_A9_STATE_PROBE(state64(::2,:,:),ok)
end subroutine COMPILE_FAIL_NONCONTIGUOUS_STATE
