subroutine COMPILE_FAIL_INT64_NGIND(ngeff, ngind64, nun, qfr64, eval64, &
    source64, raw64, nconv)
  use, intrinsic :: iso_fortran_env, only: int64, real64
  use SPOMOC_AUDIT, only: SPOMOC_CAPTURE64
  implicit none
  integer, intent(in) :: ngeff, nun
  integer(int64), intent(in) :: ngind64(ngeff)
  real(real64), intent(in) :: qfr64(nun, ngeff), eval64(nun, ngeff)
  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)
  logical, intent(in) :: nconv(ngeff)

  call SPOMOC_CAPTURE64(ngeff, ngind64, nun, qfr64, eval64, source64, &
      raw64, nconv)
end subroutine COMPILE_FAIL_INT64_NGIND
