subroutine COMPILE_SPOR64_A8_ANCHOR(ipsys, npsys, iptrk, iftrak, impx, &
    ngrp, nun, keyflx_base1, title, full_source64, full_flux64, &
    cutoff_delta64, ok)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real64
  use SPOR64_A8, only : DOORFV64
  implicit none

  type(c_ptr), intent(in) :: ipsys, iptrk
  integer, intent(in) :: iftrak, impx, ngrp, nun
  integer, intent(in) :: npsys(ngrp), keyflx_base1(8)
  character(len=72), intent(in) :: title
  real(real64), intent(in) :: full_source64(nun,ngrp)
  real(real64), intent(inout) :: full_flux64(nun,ngrp)
  integer(int64), intent(out) :: cutoff_delta64
  logical, intent(out) :: ok

  call DOORFV64(ipsys, npsys, iptrk, iftrak, impx, ngrp, nun, &
      keyflx_base1, title, full_source64, full_flux64, cutoff_delta64, &
      ok)
end subroutine COMPILE_SPOR64_A8_ANCHOR
