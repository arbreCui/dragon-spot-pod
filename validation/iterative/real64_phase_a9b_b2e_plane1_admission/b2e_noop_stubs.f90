module B2E_NOOP_PROBES
  implicit none
  integer, save :: spomoc_calls = 0
  integer, save :: xdrta2_calls = 0
  integer, save :: core_calls = 0
  integer, save :: publisher_calls = 0
contains
  subroutine B2E_RESET_PROBES()
    spomoc_calls = 0
    xdrta2_calls = 0
    core_calls = 0
    publisher_calls = 0
  end subroutine B2E_RESET_PROBES
end module B2E_NOOP_PROBES


module SPOMOC_AUDIT
  use B2E_NOOP_PROBES, only : spomoc_calls
  implicit none
  private
  public :: SPOMOC_ACTIVE
contains
  logical function SPOMOC_ACTIVE()
    spomoc_calls = spomoc_calls + 1
    SPOMOC_ACTIVE = .false.
  end function SPOMOC_ACTIVE
end module SPOMOC_AUDIT


module SPOR64_A9
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use B2E_NOOP_PROBES, only : core_calls
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

    core_calls = core_calls + 1
    terminal_flux64 = 0.0_real64
    terminal_source64 = 0.0_real64
    cutoff_visit64 = 0_int64
    accepted = .false.
    ok = .true.
  end subroutine FLU2DR64_CORE
end module SPOR64_A9


module SPOR64_B2C
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : real32, real64
  use B2E_NOOP_PROBES, only : publisher_calls
  implicit none
  private
  public :: SPOR64_B2C_PUBLISH
contains
  subroutine SPOR64_B2C_PUBLISH(ipflux,accepted_token,terminal_flux64, &
      terminal_source64,keyflx_base1,leak1d_input32,epsout32, &
      epsunk32,epsinr32,coptio,macro_name,track_name,system_name,status)
    type(c_ptr), intent(in) :: ipflux
    integer, intent(in) :: accepted_token
    real(real64), intent(in) :: terminal_flux64(:,:), terminal_source64(:,:)
    integer, intent(in) :: keyflx_base1(:)
    real(real32), intent(in) :: leak1d_input32(:)
    real(real32), intent(in) :: epsout32, epsunk32, epsinr32
    character(len=4), intent(in) :: coptio
    character(len=12), intent(in) :: macro_name, track_name, system_name
    integer, intent(out) :: status

    publisher_calls = publisher_calls + 1
    status = -777
  end subroutine SPOR64_B2C_PUBLISH
end module SPOR64_B2C


subroutine XDRTA2()
  use B2E_NOOP_PROBES, only : xdrta2_calls
  implicit none
  xdrta2_calls = xdrta2_calls + 1
end subroutine XDRTA2
