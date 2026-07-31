subroutine COMPILE_FAIL_NONCONTIGUOUS_STATE()
  use, intrinsic :: iso_fortran_env, only : real64
  use SPOR64_A9, only : SPOR64_A9_STATE_PROBE
  implicit none

  logical :: ok
  real(real64) :: state64(2,2,2)

  state64 = +0.0_real64
  call SPOR64_A9_STATE_PROBE(state64(::2,:,:),ok)
end subroutine COMPILE_FAIL_NONCONTIGUOUS_STATE
