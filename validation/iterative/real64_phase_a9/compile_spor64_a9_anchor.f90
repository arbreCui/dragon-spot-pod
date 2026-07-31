subroutine COMPILE_SPOR64_A9_ANCHOR(jpsys_group,iptrk,iftrak,impx,title, &
    keyflx_base1,matcod,vol32,xstrc32,xsdia0_32,keycur, &
    matalb_surface,albedo32,surfac32,njj_off,ijj_off,ipos_off, &
    nscat_off,scat_off32,fixed_source64,initial_flux64,xcsou64, &
    state64,history64,akeep64,epsinr64,epsunk64,epsout64, &
    eext64,eunk64,einr_last64,iinr_state,outer_iteration,requested)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int64, real32, real64
  use SPOR64_A9, only : FLU2AC64, FLU2DR64_CORE, FLUBAL64, &
      SPOR64_A9_COUNTER_PROBE, SPOR64_A9_OPERATOR_PROBE, &
      SPOR64_A9_STATE_PROBE, SPOR64_A9_TERMINAL64
  use SPOR64_A9_HOST, only : SPOR64_A9_DISPATCH, &
      SPOR64_A9_LEGACY_CALLBACK_IFACE, &
      SPOR64_A9_REAL64_CALLBACK_IFACE, SPOR64_A9_SELECTOR_PROBE
  implicit none

  type(c_ptr), intent(in) :: jpsys_group, iptrk
  integer, intent(in) :: iftrak, impx, iinr_state, outer_iteration
  integer, intent(in) :: keyflx_base1(8), matcod(8), keycur(6)
  integer, intent(in) :: matalb_surface(6)
  integer, intent(in) :: njj_off(8,370), ijj_off(8,370)
  integer, intent(in) :: ipos_off(8,370), nscat_off(370)
  character(len=72), intent(in) :: title
  logical, intent(in) :: requested
  real(real32), intent(in) :: vol32(8), xstrc32(0:8,370)
  real(real32), intent(in) :: xsdia0_32(0:8,370)
  real(real32), intent(in) :: albedo32(6), surfac32(6)
  real(real32), intent(in) :: scat_off32(8*370,370)
  real(real64), intent(in) :: fixed_source64(14,370)
  real(real64), intent(in) :: initial_flux64(14,370), xcsou64(370)
  real(real64), intent(in) :: epsinr64, epsunk64, epsout64
  real(real64), intent(in) :: eext64, eunk64, einr_last64
  real(real64), contiguous, intent(inout) :: state64(:,:,:)
  real(real64), contiguous, intent(inout) :: history64(:,:,:)
  real(real64), contiguous, intent(inout) :: akeep64(:)

  integer :: default_real32_kind, default_real64_kind
  integer(int64) :: cutoff_visit64
  logical :: accepted, balance_ok, counter_ok, default_selected
  logical :: dispatch_ok, operator_ok, selected_real64, state_ok
  real(real64) :: terminal_flux64(14,370)
  real(real64) :: terminal_source64(14,370), zmu64
  procedure(SPOR64_A9_LEGACY_CALLBACK_IFACE) :: &
      SPOR64_A9_ANCHOR_LEGACY_CALLBACK
  procedure(SPOR64_A9_REAL64_CALLBACK_IFACE) :: &
      SPOR64_A9_ANCHOR_REAL64_CALLBACK

  call FLU2DR64_CORE(jpsys_group,iptrk,iftrak,impx,title,keyflx_base1, &
      matcod,vol32,xstrc32,xsdia0_32,keycur,matalb_surface,albedo32, &
      surfac32,njj_off,ijj_off,ipos_off,nscat_off,scat_off32, &
      fixed_source64,initial_flux64,epsinr64,epsunk64,epsout64, &
      terminal_flux64,terminal_source64,cutoff_visit64,accepted, &
      state_ok)
  call FLUBAL64(matcod,vol32,keyflx_base1,xstrc32,xsdia0_32,xcsou64, &
      1,keycur,matalb_surface,albedo32,surfac32,njj_off,ijj_off, &
      ipos_off,nscat_off,scat_off32,terminal_flux64,balance_ok)
  call FLU2AC64(370,14,1,history64,akeep64,zmu64,state_ok)
  call SPOR64_A9_TERMINAL64(eext64,eunk64,einr_last64,epsout64, &
      epsunk64,epsinr64,iinr_state,outer_iteration,accepted)
  call SPOR64_A9_STATE_PROBE(state64,state_ok)
  call SPOR64_A9_OPERATOR_PROBE(scat_off32,operator_ok)
  call SPOR64_A9_COUNTER_PROBE(cutoff_visit64,counter_ok)
  call SPOR64_A9_SELECTOR_PROBE(terminal_flux64(:,1),default_selected, &
      default_real32_kind,default_real64_kind)
  call SPOR64_A9_DISPATCH(requested,terminal_flux64(:,1), &
      SPOR64_A9_ANCHOR_LEGACY_CALLBACK, &
      SPOR64_A9_ANCHOR_REAL64_CALLBACK,selected_real64,dispatch_ok)

end subroutine COMPILE_SPOR64_A9_ANCHOR

subroutine SPOR64_A9_ANCHOR_LEGACY_CALLBACK(ok)
  implicit none
  logical, intent(inout) :: ok
  ok = .true.
end subroutine SPOR64_A9_ANCHOR_LEGACY_CALLBACK

subroutine SPOR64_A9_ANCHOR_REAL64_CALLBACK(values64,ok)
  use, intrinsic :: iso_fortran_env, only : real64
  implicit none
  real(real64), contiguous, intent(inout) :: values64(:)
  logical, intent(inout) :: ok
  ok = size(values64) > 0
end subroutine SPOR64_A9_ANCHOR_REAL64_CALLBACK
