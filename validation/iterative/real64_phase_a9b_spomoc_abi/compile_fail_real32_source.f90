subroutine COMPILE_FAIL_REAL32_SOURCE(ngeff, ngind, nun, qfr64, eval64, &
    source32, raw64, nconv)
  use, intrinsic :: iso_fortran_env, only: real32, real64
  use SPOMOC_AUDIT, only: SPOMOC_CAPTURE64
  implicit none
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff)
  real(real64), intent(in) :: qfr64(nun, ngeff), eval64(nun, ngeff)
  real(real32), intent(in) :: source32(nun, ngeff)
  real(real64), intent(in) :: raw64(nun, ngeff)
  logical, intent(in) :: nconv(ngeff)

  call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, eval64, source32, &
      raw64, nconv)
end subroutine COMPILE_FAIL_REAL32_SOURCE
