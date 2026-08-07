module B2P_STUB_PROBES
  use, intrinsic :: iso_fortran_env, only : int64, real64
  implicit none
  integer, parameter :: B2P_NUNKNO=14, B2P_NGRP=370
  integer(int64), parameter :: B2P_CUTOFF_SENTINEL=4294967311_int64
  integer, save :: xdrta2_calls=0, core_calls=0
  logical, save :: capture_valid=.false., terminals_distinct=.false.
  logical, save :: stub_accepted=.true., stub_core_ok=.true.
  real(real64), save :: captured_flux64(B2P_NUNKNO,B2P_NGRP)=0.0_real64
  real(real64), save :: captured_qfiss64(B2P_NUNKNO,B2P_NGRP)=0.0_real64
  real(real64), save :: returned_flux64(B2P_NUNKNO,B2P_NGRP)=0.0_real64
  real(real64), save :: returned_source64(B2P_NUNKNO,B2P_NGRP)=0.0_real64
contains
  subroutine B2P_RESET_PROBES()
    xdrta2_calls=0
    core_calls=0
    capture_valid=.false.
    terminals_distinct=.false.
    stub_accepted=.true.
    stub_core_ok=.true.
    captured_flux64=0.0_real64
    captured_qfiss64=0.0_real64
    returned_flux64=0.0_real64
    returned_source64=0.0_real64
  end subroutine B2P_RESET_PROBES


  pure subroutine B2P_BUILD_TERMINALS(flux64,source64)
    real(real64), intent(out) :: flux64(B2P_NUNKNO,B2P_NGRP)
    real(real64), intent(out) :: source64(B2P_NUNKNO,B2P_NGRP)
    real(real64) :: base
    integer :: ig, iu

    do ig=1,B2P_NGRP
      do iu=1,B2P_NUNKNO
        base=16384.0_real64+real(31*ig+iu,real64)/16.0_real64
        flux64(iu,ig)=base+spacing(base)
        base=32768.0_real64+real(37*ig+3*iu,real64)/16.0_real64
        source64(iu,ig)=base+spacing(base)
      end do
    end do
  end subroutine B2P_BUILD_TERMINALS
end module B2P_STUB_PROBES


module SPOMOC_AUDIT
  implicit none
  private
  public :: SPOMOC_ACTIVE
contains
  logical function SPOMOC_ACTIVE()
    SPOMOC_ACTIVE=.false.
  end function SPOMOC_ACTIVE
end module SPOMOC_AUDIT


module SPOR64_A9
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use B2P_STUB_PROBES, only : B2P_CUTOFF_SENTINEL, core_calls, &
      capture_valid, terminals_distinct, captured_flux64, &
      captured_qfiss64, returned_flux64, returned_source64, &
      stub_accepted, stub_core_ok, B2P_BUILD_TERMINALS
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

    core_calls=core_calls+1
    captured_flux64=initial_flux64
    captured_qfiss64=fixed_source64
    capture_valid=.true.
    call B2P_BUILD_TERMINALS(terminal_flux64,terminal_source64)
    returned_flux64=terminal_flux64
    returned_source64=terminal_source64
    terminals_distinct=any(transfer(terminal_flux64,0_int64, &
        size(terminal_flux64)) /= transfer(initial_flux64,0_int64, &
        size(initial_flux64))) .and. any(transfer(terminal_source64, &
        0_int64,size(terminal_source64)) /= transfer(fixed_source64, &
        0_int64,size(fixed_source64)))
    cutoff_visit64=B2P_CUTOFF_SENTINEL
    accepted=stub_accepted
    ok=stub_core_ok
  end subroutine FLU2DR64_CORE
end module SPOR64_A9


subroutine XDRTA2()
  use B2P_STUB_PROBES, only : xdrta2_calls
  implicit none
  xdrta2_calls=xdrta2_calls+1
end subroutine XDRTA2
