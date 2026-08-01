subroutine COMPILE_FAIL_REAL32_BRIDGE(ngeff, ngind, nun, qfr32, eval64, &
    source64, raw64, nconv)
  use, intrinsic :: iso_fortran_env, only: real32, real64
  implicit none
  interface
    subroutine SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, eval64, &
        source64, raw64, nconv)
      import :: real64
      integer, intent(in) :: ngeff, nun
      integer, intent(in) :: ngind(ngeff)
      real(real64), intent(in) :: qfr64(nun, ngeff)
      real(real64), intent(in) :: eval64(nun, ngeff)
      real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)
      logical, intent(in) :: nconv(ngeff)
    end subroutine SPOMOC_CAPTURE64
  end interface
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff)
  real(real32), intent(in) :: qfr32(nun, ngeff)
  real(real64), intent(in) :: eval64(nun, ngeff)
  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)
  logical, intent(in) :: nconv(ngeff)

  call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr32, eval64, source64, &
      raw64, nconv)
end subroutine COMPILE_FAIL_REAL32_BRIDGE
