subroutine SPOMOC_MCCGF_BEGIN(ngrp, ngeff, ngind, nun, ndim0, cyclic, &
    nlong, nreg0, nsou, nani0, nlin0, nfunl0, kryl0, stis0, iaac0, &
    iscr0, idifc0, paca0, idir0)
  use SPOMOC_AUDIT, only: SPOMOC_MCCGF_BEGIN_MODULE => &
      SPOMOC_MCCGF_BEGIN
  implicit none
  integer, intent(in) :: ngrp, ngeff, nun, ndim0, nlong, nreg0, nsou
  integer, intent(in) :: nani0, nlin0, nfunl0, kryl0, stis0, iaac0
  integer, intent(in) :: iscr0, idifc0, paca0, idir0
  integer, intent(in) :: ngind(ngeff)
  logical, intent(in) :: cyclic

  call SPOMOC_MCCGF_BEGIN_MODULE(ngrp, ngeff, ngind, nun, ndim0, cyclic, &
      nlong, nreg0, nsou, nani0, nlin0, nfunl0, kryl0, stis0, iaac0, &
      iscr0, idifc0, paca0, idir0)
end subroutine SPOMOC_MCCGF_BEGIN


subroutine SPOMOC_SET_ROLE(role, iteration)
  use SPOMOC_AUDIT, only: SPOMOC_SET_ROLE_MODULE => SPOMOC_SET_ROLE
  implicit none
  integer, intent(in) :: role, iteration

  call SPOMOC_SET_ROLE_MODULE(role, iteration)
end subroutine SPOMOC_SET_ROLE


subroutine SPOMOC_PUBLISH()
  use SPOMOC_AUDIT, only: SPOMOC_PUBLISH_MODULE => SPOMOC_PUBLISH
  implicit none

  call SPOMOC_PUBLISH_MODULE()
end subroutine SPOMOC_PUBLISH


subroutine SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, eval64, source64, &
    raw64, nconv)
  use, intrinsic :: iso_fortran_env, only: real64
  use SPOMOC_AUDIT, only: SPOMOC_CAPTURE64_MODULE => SPOMOC_CAPTURE64
  implicit none
  integer, intent(in) :: ngeff, nun
  integer, intent(in) :: ngind(ngeff)
  real(real64), intent(in) :: qfr64(nun, ngeff), eval64(nun, ngeff)
  real(real64), intent(in) :: source64(nun, ngeff), raw64(nun, ngeff)
  logical, intent(in) :: nconv(ngeff)

  call SPOMOC_CAPTURE64_MODULE(ngeff, ngind, nun, qfr64, eval64, source64, &
      raw64, nconv)
end subroutine SPOMOC_CAPTURE64
