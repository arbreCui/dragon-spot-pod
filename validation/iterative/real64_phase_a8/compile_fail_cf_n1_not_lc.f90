subroutine COMPILE_FAIL_CF_N1_NOT_LC(im, cf_n1, cutoff_delta64, ok)
  use, intrinsic :: iso_fortran_env, only : int64, real32
  use SPOR64_A8_ACA, only : SPOR64_A8_ACA_SHAPE_PROBE
  implicit none
  integer, intent(in) :: im(15)
  real(real32), intent(in) :: cf_n1(14)
  integer(int64), intent(out) :: cutoff_delta64
  logical, intent(out) :: ok

  call SPOR64_A8_ACA_SHAPE_PROBE(14, 32, im, cf_n1, cutoff_delta64, ok)
end subroutine COMPILE_FAIL_CF_N1_NOT_LC
