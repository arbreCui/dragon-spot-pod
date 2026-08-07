module B2S_STUB_PROBES
  use, intrinsic :: iso_fortran_env, only : int64, real64
  implicit none
  private

  integer, parameter, public :: B2S_NUNKNO=14, B2S_NGRP=370
  integer, save, public :: xdrta2_calls=0, core_calls=0, event_count=0
  integer, save, public :: events(16)=0, fail_plane=0
  integer, save, public :: core_plane(3)=0
  real(real64), save, public :: captured_flux64(B2S_NUNKNO,B2S_NGRP,3)=0.0_real64
  real(real64), save, public :: captured_qfiss64(B2S_NUNKNO,B2S_NGRP,3)=0.0_real64

  public :: B2S_RESET_PROBES, B2S_RECORD_EVENT
  public :: B2S_TERMINAL_FLUX, B2S_TERMINAL_SOURCE
  public :: B2S_QFISS_VALUE, B2S_CUTOFF_VALUE

contains

  subroutine B2S_RESET_PROBES(failing_plane)
    integer, intent(in), optional :: failing_plane

    xdrta2_calls=0
    core_calls=0
    event_count=0
    events=0
    fail_plane=0
    if (present(failing_plane)) fail_plane=failing_plane
    core_plane=0
    captured_flux64=0.0_real64
    captured_qfiss64=0.0_real64
  end subroutine B2S_RESET_PROBES


  subroutine B2S_RECORD_EVENT(code)
    integer, intent(in) :: code

    event_count=event_count+1
    if (event_count <= size(events)) events(event_count)=code
  end subroutine B2S_RECORD_EVENT


  pure real(real64) function B2S_TERMINAL_FLUX(plane,group,unknown)
    integer, intent(in) :: plane, group, unknown
    real(real64) :: base

    base=16384.0_real64+1024.0_real64*real(plane,real64)+ &
        real(31*group+unknown,real64)/16.0_real64
    B2S_TERMINAL_FLUX=base+real(plane,real64)*spacing(base)
  end function B2S_TERMINAL_FLUX


  pure real(real64) function B2S_TERMINAL_SOURCE(plane,group,unknown)
    integer, intent(in) :: plane, group, unknown
    real(real64) :: base

    base=32768.0_real64+2048.0_real64*real(plane,real64)+ &
        real(37*group+3*unknown,real64)/16.0_real64
    B2S_TERMINAL_SOURCE=base+real(plane,real64)*spacing(base)
  end function B2S_TERMINAL_SOURCE


  pure real(real64) function B2S_QFISS_VALUE(plane,group,unknown)
    integer, intent(in) :: plane, group, unknown
    real(real64) :: base

    base=4096.0_real64+256.0_real64*real(plane,real64)+ &
        2.0_real64*real(group,real64)+real(unknown,real64)/16.0_real64
    B2S_QFISS_VALUE=base+real(plane,real64)*spacing(base)
  end function B2S_QFISS_VALUE


  pure integer(int64) function B2S_CUTOFF_VALUE(plane)
    integer, intent(in) :: plane

    B2S_CUTOFF_VALUE=4294967300_int64+17_int64*int(plane,int64)
  end function B2S_CUTOFF_VALUE

end module B2S_STUB_PROBES


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
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use B2S_STUB_PROBES
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
    integer :: group, unknown, plane, record_length, record_type

    core_calls=core_calls+1
    plane=0
    call LCMLEN(iptrk,'B2S-PLANE',record_length,record_type)
    if (record_length == 1 .and. record_type == 1) &
      call LCMGET(iptrk,'B2S-PLANE',plane)
    call B2S_RECORD_EVENT(plane)
    if (core_calls <= size(core_plane)) core_plane(core_calls)=plane

    terminal_flux64=0.0_real64
    terminal_source64=0.0_real64
    cutoff_visit64=0_int64
    accepted=.false.
    ok=.false.
    if (plane < 1 .or. plane > 3) return

    captured_flux64(:,:,plane)=initial_flux64
    captured_qfiss64(:,:,plane)=fixed_source64
    do group=1,NGRP
      do unknown=1,NUNKNO
        terminal_flux64(unknown,group)= &
            B2S_TERMINAL_FLUX(plane,group,unknown)
        terminal_source64(unknown,group)= &
            B2S_TERMINAL_SOURCE(plane,group,unknown)
      end do
    end do
    cutoff_visit64=B2S_CUTOFF_VALUE(plane)
    accepted=.true.
    ok=plane /= fail_plane
  end subroutine FLU2DR64_CORE
end module SPOR64_A9


subroutine XDRTA2()
  use B2S_STUB_PROBES, only : xdrta2_calls, B2S_RECORD_EVENT
  implicit none

  xdrta2_calls=xdrta2_calls+1
  call B2S_RECORD_EVENT(0)
end subroutine XDRTA2
