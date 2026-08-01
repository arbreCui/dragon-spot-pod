subroutine COMPILE_FAIL_RANK1_CAPTURE(ngeff, ngind, nun, qfr1, eval64, &
    source64, raw64, nconv)
  use, intrinsic :: iso_fortran_env, only: real64
  use SPOMOC_AUDIT, only: SPOMOC_CAPTURE64
  implicit none
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff)
  real(real64), intent(in) :: qfr1(:)
  real(real64), intent(in) :: eval64(nun, ngeff)
  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)
  logical, intent(in) :: nconv(ngeff)

  call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr1, eval64, source64, &
      raw64, nconv)
end subroutine COMPILE_FAIL_RANK1_CAPTURE
