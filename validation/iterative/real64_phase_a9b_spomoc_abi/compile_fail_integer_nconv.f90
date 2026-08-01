subroutine COMPILE_FAIL_INTEGER_NCONV(ngeff, ngind, nun, qfr64, eval64, &
    source64, raw64, nconv_integer)
  use, intrinsic :: iso_fortran_env, only: real64
  use SPOMOC_AUDIT, only: SPOMOC_CAPTURE64
  implicit none
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff), nconv_integer(ngeff)
  real(real64), intent(in) :: qfr64(nun, ngeff), eval64(nun, ngeff)
  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)

  call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, eval64, source64, &
      raw64, nconv_integer)
end subroutine COMPILE_FAIL_INTEGER_NCONV
