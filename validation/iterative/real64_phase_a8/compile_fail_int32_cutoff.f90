subroutine COMPILE_FAIL_INT32_CUTOFF(im, cf32, cutoff_delta32, ok)
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A8_ACA, only : SPOR64_A8_ACA_SHAPE_PROBE
  implicit none
  integer, intent(in) :: im(15)
  real(real32), intent(in) :: cf32(32)
  integer, intent(out) :: cutoff_delta32
  logical, intent(out) :: ok

  call SPOR64_A8_ACA_SHAPE_PROBE(14, 32, im, cf32, cutoff_delta32, ok)
end subroutine COMPILE_FAIL_INT32_CUTOFF
