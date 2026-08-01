subroutine COMPILE_FAIL_ACA_IM_EXTENT(im14,cf32,cutoff_delta64,ok)
  use, intrinsic :: iso_fortran_env, only : int64, real32
  use SPOR64_A8_ACA, only : SPOR64_A8_ACA_SHAPE_PROBE
  implicit none

  integer, intent(in) :: im14(14)
  real(real32), intent(in) :: cf32(32)
  integer(int64), intent(out) :: cutoff_delta64
  logical, intent(out) :: ok

  call SPOR64_A8_ACA_SHAPE_PROBE(14,32,im14,cf32,cutoff_delta64,ok)
end subroutine COMPILE_FAIL_ACA_IM_EXTENT
