subroutine COMPILE_FAIL_IM_N_NOT_NPLUS1(im_n, cf32, cutoff_delta64, ok)
  use, intrinsic :: iso_fortran_env, only : int64, real32
  use SPOR64_A8_ACA, only : SPOR64_A8_ACA_SHAPE_PROBE
  implicit none
  integer, intent(in) :: im_n(14)
  real(real32), intent(in) :: cf32(32)
  integer(int64), intent(out) :: cutoff_delta64
  logical, intent(out) :: ok

  call SPOR64_A8_ACA_SHAPE_PROBE(14, 32, im_n, cf32, cutoff_delta64, ok)
end subroutine COMPILE_FAIL_IM_N_NOT_NPLUS1
