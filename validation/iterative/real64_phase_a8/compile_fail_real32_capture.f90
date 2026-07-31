subroutine COMPILE_FAIL_REAL32_CAPTURE(ngeff, ngind, nun, qfr32, &
    eval32, source32, raw32, nconv, ok)
  use, intrinsic :: iso_fortran_env, only : real32
  use SPOR64_A8, only : SPOR64_A8_CAPTURE_PROBE
  implicit none
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff)
  real(real32), intent(in) :: qfr32(nun,ngeff)
  real(real32), intent(in) :: eval32(nun,ngeff)
  real(real32), intent(in) :: source32(nun,ngeff)
  real(real32), intent(in) :: raw32(nun,ngeff)
  logical, intent(in) :: nconv(ngeff)
  logical, intent(out) :: ok

  call SPOR64_A8_CAPTURE_PROBE(ngeff, ngind, nun, qfr32, eval32, &
      source32, raw32, nconv, ok)
end subroutine COMPILE_FAIL_REAL32_CAPTURE
