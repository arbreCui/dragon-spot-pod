module B2G_STUB_PROBES
  use, intrinsic :: iso_fortran_env, only : real64
  implicit none
  integer, parameter :: B2G_NUNKNO=14, B2G_NGRP=370
  integer, save :: spomoc_calls=0, xdrta2_calls=0, core_calls=0
  integer, save :: spomoc_total=0, xdrta2_total=0, core_total=0
  logical, save :: capture_valid=.false.
  real(real64), save :: captured_flux64(B2G_NUNKNO,B2G_NGRP)=0.0_real64
  real(real64), save :: captured_qfiss64(B2G_NUNKNO,B2G_NGRP)=0.0_real64
contains
  subroutine B2G_RESET_TOTALS()
    spomoc_calls=0
    xdrta2_calls=0
    core_calls=0
    spomoc_total=0
    xdrta2_total=0
    core_total=0
    capture_valid=.false.
    captured_flux64=0.0_real64
    captured_qfiss64=0.0_real64
  end subroutine B2G_RESET_TOTALS

  subroutine B2G_RESET_PROBES()
    spomoc_calls=0
    xdrta2_calls=0
    core_calls=0
    capture_valid=.false.
    captured_flux64=0.0_real64
    captured_qfiss64=0.0_real64
  end subroutine B2G_RESET_PROBES
end module B2G_STUB_PROBES


module SPOMOC_AUDIT
  use B2G_STUB_PROBES, only : spomoc_calls, spomoc_total
  implicit none
  private
  public :: SPOMOC_ACTIVE
contains
  logical function SPOMOC_ACTIVE()
    spomoc_calls=spomoc_calls+1
    spomoc_total=spomoc_total+1
    SPOMOC_ACTIVE=.false.
  end function SPOMOC_ACTIVE
end module SPOMOC_AUDIT


module SPOR64_A9
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use B2G_STUB_PROBES, only : core_calls, core_total, capture_valid, &
      captured_flux64, captured_qfiss64
  implicit none
  private
  integer, parameter :: NGRP=370, NREG=8, NMAT=8, NUNKNO=14, NSOUT=6
  public :: FLU2DR64_CORE
contains
  subroutine FLU2DR64_CORE(jpsys_group,iptrk,iftrak,impx,title, &
      keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
      matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
      nscat_off,scat_off32,fixed_source64,initial_flux64, &
      epsinr64,epsunk64,epsout64,terminal_flux64, &
      terminal_source64,cutoff_visit64,accepted,ok)
    type(c_ptr), intent(in) :: jpsys_group, iptrk
    integer, intent(in) :: iftrak, impx
    character(len=72), intent(in) :: title
    integer, intent(in) :: keyflx_base1(NREG), matcod(NREG)
    integer, intent(in) :: keycur(NSOUT), matalb_surface(NSOUT)
    integer, intent(in) :: njj_off(NMAT,NGRP), ijj_off(NMAT,NGRP)
    integer, intent(in) :: ipos_off(NMAT,NGRP), nscat_off(NGRP)
    real(real32), intent(in) :: vol32(NREG)
    real(real32), intent(in) :: xstrc32(0:NMAT,NGRP)
    real(real32), intent(in) :: xsdia0_32(0:NMAT,NGRP)
    real(real32), intent(in) :: albedo32(NSOUT), surfac32(NSOUT)
    real(real32), intent(in) :: scat_off32(NMAT*NGRP,NGRP)
    real(real64), intent(in) :: fixed_source64(NUNKNO,NGRP)
    real(real64), intent(in) :: initial_flux64(NUNKNO,NGRP)
    real(real64), intent(in) :: epsinr64, epsunk64, epsout64
    real(real64), intent(out) :: terminal_flux64(NUNKNO,NGRP)
    real(real64), intent(out) :: terminal_source64(NUNKNO,NGRP)
    integer(int64), intent(out) :: cutoff_visit64
    logical, intent(out) :: accepted, ok
    integer :: ig, iu

    core_calls=core_calls+1
    core_total=core_total+1
    captured_flux64=initial_flux64
    captured_qfiss64=fixed_source64
    capture_valid=.true.
    terminal_flux64=initial_flux64
    ! Synthetic, exactly representable terminal sweep-source sentinel.  It is
    ! deliberately not QFISS: B2C must publish the core's SOUR result without
    ! turning it into the next outer iteration's frozen fission source.
    do ig=1,NGRP
      do iu=1,NUNKNO
        terminal_source64(iu,ig)=real(1000*ig+iu,real64)/8.0_real64
      end do
    end do
    cutoff_visit64=0_int64
    accepted=.true.
    ok=.true.
  end subroutine FLU2DR64_CORE
end module SPOR64_A9


subroutine XDRTA2()
  use B2G_STUB_PROBES, only : xdrta2_calls, xdrta2_total
  implicit none
  xdrta2_calls=xdrta2_calls+1
  xdrta2_total=xdrta2_total+1
end subroutine XDRTA2
