module SPOR64_B2C
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : CHARACTER_RECORD_MATCHES, EMPTY_MEMORY_ROOT, &
      EXACT_INVENTORY, RECORD_MATCHES
  use SPOR64_SCHEMA, only : SCHEMA_PLANE_SEED_AUTHORITY
  implicit none
  private

  integer, parameter, public :: SPOR64_B2C_PREFLIGHT_FAILED = 5
  integer, parameter, public :: SPOR64_B2C_CHILD_PUBLISHED = 6
  integer, parameter, public :: SPOR64_B2C_DRIVER_COMMITTED = 7
  integer, parameter, public :: SPOR64_B2C_HOST_COMMITTED = 8

  integer, parameter :: ACCEPTED_UNPUBLISHED = 4
  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NMAT = 8
  integer, parameter :: NUNKNO = 14
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: kind_guard = 1 / merge(1, 0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2C_PUBLISH
  public :: SPOR64_B2C_PUBLISH_CONT

contains

  subroutine SPOR64_B2C_PUBLISH(ipflux,accepted_token,terminal_flux64, &
      terminal_source64,keyflx_base1,nmerg_input,imerge_input, &
      leak1d_input32,epsout32, &
      epsunk32,epsinr32,coptio,macro_name,track_name,system_name,status)
    type(c_ptr), intent(in) :: ipflux
    integer, intent(in) :: accepted_token
    real(real64), intent(in) :: terminal_flux64(:,:), terminal_source64(:,:)
    integer, intent(in) :: keyflx_base1(:)
    integer, intent(in) :: nmerg_input, imerge_input(:)
    real(real32), intent(in) :: leak1d_input32(:)
    real(real32), intent(in) :: epsout32, epsunk32, epsinr32
    character(len=4), intent(in) :: coptio
    character(len=12), intent(in) :: macro_name, track_name, system_name
    integer, intent(out) :: status

    call SPOR64_B2C_PUBLISH_IMPL(ipflux,accepted_token,terminal_flux64, &
        terminal_source64,keyflx_base1,nmerg_input,imerge_input, &
        leak1d_input32,epsout32,epsunk32,epsinr32,coptio,macro_name, &
        track_name,system_name,status)
  end subroutine SPOR64_B2C_PUBLISH


  subroutine SPOR64_B2C_PUBLISH_CONT(ipflux,ipseed_lifecycle, &
      accepted_token,terminal_flux64,terminal_source64,keyflx_base1, &
      nmerg_input,imerge_input,leak1d_input32,epsout32,epsunk32, &
      epsinr32,coptio,macro_name,track_name,system_name,status)
    type(c_ptr), intent(in) :: ipflux, ipseed_lifecycle
    integer, intent(in) :: accepted_token
    real(real64), intent(in) :: terminal_flux64(:,:), terminal_source64(:,:)
    integer, intent(in) :: keyflx_base1(:)
    integer, intent(in) :: nmerg_input, imerge_input(:)
    real(real32), intent(in) :: leak1d_input32(:)
    real(real32), intent(in) :: epsout32, epsunk32, epsinr32
    character(len=4), intent(in) :: coptio
    character(len=12), intent(in) :: macro_name, track_name, system_name
    integer, intent(out) :: status

    call SPOR64_B2C_PUBLISH_IMPL(ipflux,accepted_token,terminal_flux64, &
        terminal_source64,keyflx_base1,nmerg_input,imerge_input, &
        leak1d_input32,epsout32,epsunk32,epsinr32,coptio,macro_name, &
        track_name,system_name,status,ipseed_lifecycle)
  end subroutine SPOR64_B2C_PUBLISH_CONT


  subroutine SPOR64_B2C_PUBLISH_IMPL(ipflux,accepted_token, &
      terminal_flux64,terminal_source64,keyflx_base1,nmerg_input, &
      imerge_input,leak1d_input32,epsout32,epsunk32,epsinr32,coptio, &
      macro_name,track_name,system_name,status,ipseed_lifecycle)
    type(c_ptr), intent(in) :: ipflux
    integer, intent(in) :: accepted_token
    real(real64), intent(in) :: terminal_flux64(:,:), terminal_source64(:,:)
    integer, intent(in) :: keyflx_base1(:)
    integer, intent(in) :: nmerg_input, imerge_input(:)
    real(real32), intent(in) :: leak1d_input32(:)
    real(real32), intent(in) :: epsout32, epsunk32, epsinr32
    character(len=4), intent(in) :: coptio
    character(len=12), intent(in) :: macro_name, track_name, system_name
    integer, intent(out) :: status
    type(c_ptr), intent(in), optional :: ipseed_lifecycle

    integer :: state_vector(NSTATE)
    integer :: ig, ir, allocation_status
    integer :: lifecycle_plane, lifecycle_epoch
    logical :: seen_unknown(NUNKNO), publish_solved
    real(real32) :: eps_converge(5)
    real(real64) :: lifecycle_rho64
    real(real32), allocatable :: flux_stage32(:,:), source_stage32(:,:)
    type(c_ptr) :: authority, authority_flux, authority_source
    type(c_ptr) :: lifecycle_authority
    type(c_ptr) :: legacy_flux, legacy_source
    character(len=12) :: signature, authority_state

    status = SPOR64_B2C_PREFLIGHT_FAILED
    publish_solved = present(ipseed_lifecycle)

    ! The complete no-write preflight is deliberately ahead of LCMDID/LCMLID.
    if (accepted_token /= ACCEPTED_UNPUBLISHED) return
    if (.not. c_associated(ipflux)) return
    if (size(terminal_flux64,1) /= NUNKNO .or. &
        size(terminal_flux64,2) /= NGRP) return
    if (size(terminal_source64,1) /= NUNKNO .or. &
        size(terminal_source64,2) /= NGRP) return
    if (size(keyflx_base1) /= NREG) return
    if (nmerg_input /= 1 .or. size(imerge_input) /= NMAT) return
    if (any(imerge_input /= 1)) return
    if (size(leak1d_input32) /= NGRP) return
    if (.not. all(ieee_is_finite(terminal_flux64))) return
    if (.not. all(ieee_is_finite(terminal_source64))) return
    if (any(abs(terminal_flux64) > REAL32_MAX64)) return
    if (any(abs(terminal_source64) > REAL32_MAX64)) return
    if (.not. all(ieee_is_finite(leak1d_input32))) return
    if (transfer(epsout32,0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(epsunk32,0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(epsinr32,0_int32) /= FROZEN_TOL_BITS) return
    if (coptio /= 'B0  ') return
    if (macro_name /= 'MACRO0') return
    if (track_name /= 'TRACK') return
    if (system_name /= 'SYSTEM') return

    ! CONT alone may publish a lifecycle-bearing SOLVED state.  Its identity
    ! is inherited from the already sealed PROJECTED seed object, never from
    ! independent caller scalars.  All reads remain in the no-write preflight.
    if (publish_solved) then
      if (.not. c_associated(ipseed_lifecycle)) return
      if (c_associated(ipflux,ipseed_lifecycle)) return
      if (.not. RECORD_MATCHES(ipseed_lifecycle,'SPOT-R64',-1,0)) return
      lifecycle_authority = LCMGID(ipseed_lifecycle,'SPOT-R64')
      if (.not. c_associated(lifecycle_authority)) return
      if (.not. PROJECTED_AUTHORITY_IS_EXACT(lifecycle_authority)) return
      if (.not. RECORD_MATCHES(lifecycle_authority,'RHO',1,4)) return
      if (.not. RECORD_MATCHES(lifecycle_authority,'PLANE',1,1)) return
      if (.not. RECORD_MATCHES(lifecycle_authority,'FLUX',NGRP,10)) return
      if (.not. REAL64_FLUX_IS_VALID(lifecycle_authority)) return
      if (.not. CHARACTER_RECORD_MATCHES(lifecycle_authority,'STATE',3, &
          12,'PROJECTED')) return
      if (.not. RECORD_MATCHES(lifecycle_authority,'EPOCH',1,1)) return
      call LCMGET(lifecycle_authority,'RHO',lifecycle_rho64)
      call LCMGET(lifecycle_authority,'PLANE',lifecycle_plane)
      call LCMGET(lifecycle_authority,'EPOCH',lifecycle_epoch)
      if (.not. ieee_is_finite(lifecycle_rho64)) return
      if (lifecycle_rho64 <= +0.0_real64) return
      if (lifecycle_plane < 1 .or. lifecycle_plane > 3) return
      if (lifecycle_epoch < 0 .or. &
          lifecycle_epoch == huge(lifecycle_epoch)) return
    end if

    seen_unknown = .false.
    do ir = 1, NREG
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > NUNKNO) return
      if (seen_unknown(keyflx_base1(ir))) return
      seen_unknown(keyflx_base1(ir)) = .true.
    end do

    if (.not. EMPTY_MEMORY_ROOT(ipflux)) return

    allocate(flux_stage32(NUNKNO,NGRP), &
        source_stage32(NUNKNO,NGRP),stat=allocation_status)
    if (allocation_status /= 0) then
      if (allocated(flux_stage32)) deallocate(flux_stage32)
      if (allocated(source_stage32)) deallocate(source_stage32)
      return
    end if
    flux_stage32 = real(terminal_flux64,real32)
    source_stage32 = real(terminal_source64,real32)
    ! Repeat freshness immediately before the first caller-visible mutation.
    if (.not. EMPTY_MEMORY_ROOT(ipflux)) return

    ! Authoritative REAL64 child publication precedes every compatibility write.
    authority = LCMDID(ipflux,'SPOT-R64')
    if (.not. c_associated(authority)) &
        call XABORT('SPOR64_B2C: SPOT-R64 DIRECTORY CREATION FAILED.')
    if (publish_solved) then
      call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)
      call LCMPUT(authority,'PLANE',1,1,lifecycle_plane)
    end if
    authority_flux = LCMLID(authority,'FLUX',NGRP)
    if (.not. c_associated(authority_flux)) &
        call XABORT('SPOR64_B2C: TYPE-4 FLUX LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(authority_flux,ig,NUNKNO,4,terminal_flux64(:,ig))
    end do
    authority_source = LCMLID(authority,'SOUR',NGRP)
    if (.not. c_associated(authority_source)) &
        call XABORT('SPOR64_B2C: TYPE-4 SOUR LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(authority_source,ig,NUNKNO,4,terminal_source64(:,ig))
    end do

    ! Compatibility publication follows type-4 authority; its REAL32 arrays
    ! were fully staged during the no-write preflight above.
    legacy_flux = LCMLID(ipflux,'FLUX',NGRP)
    if (.not. c_associated(legacy_flux)) &
        call XABORT('SPOR64_B2C: TYPE-2 FLUX LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(legacy_flux,ig,NUNKNO,2,flux_stage32(:,ig))
    end do
    legacy_source = LCMLID(ipflux,'SOUR',NGRP)
    if (.not. c_associated(legacy_source)) &
        call XABORT('SPOR64_B2C: TYPE-2 SOUR LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(legacy_source,ig,NUNKNO,2,source_stage32(:,ig))
    end do
    status = SPOR64_B2C_CHILD_PUBLISHED

    state_vector = 0
    state_vector(1) = NGRP
    state_vector(2) = NUNKNO
    state_vector(3) = 1
    state_vector(6) = 0
    state_vector(7) = 0
    state_vector(8) = 3
    state_vector(9) = 3
    state_vector(10) = 1
    state_vector(11) = 740
    state_vector(12) = 500
    state_vector(17) = NMAT
    state_vector(18) = nmerg_input
    eps_converge = [epsinr32,epsunk32,epsout32, &
        0.0_real32,0.0_real32]
    signature = 'L_FLUX'
    call LCMPTC(ipflux,'SIGNATURE',12,signature)
    call LCMPUT(ipflux,'STATE-VECTOR',NSTATE,1,state_vector)
    call LCMPUT(ipflux,'EPS-CONVERGE',5,2,eps_converge)
    call LCMPUT(ipflux,'IMERGE-LEAK',NMAT,1,imerge_input)
    call LCMPUT(ipflux,'KEYFLX',NREG,1,keyflx_base1)
    call LCMPTC(ipflux,'OPTION',4,coptio)
    status = SPOR64_B2C_DRIVER_COMMITTED

    call LCMPTC(ipflux,'LINK.MACRO',12,macro_name)
    call LCMPTC(ipflux,'LINK.TRACK',12,track_name)
    call LCMPTC(ipflux,'LINK.SYSTEM',12,system_name)
    call LCMPUT(ipflux,'SPOT-LEAK1D',NGRP,2,leak1d_input32)
    if (publish_solved) then
      authority_state = 'SOLVED'
      call LCMPTC(authority,'STATE',12,authority_state)
      ! EPOCH is the final mutation and commits this accepted local state.
      call LCMPUT(authority,'EPOCH',1,1,lifecycle_epoch)
    end if
    status = SPOR64_B2C_HOST_COMMITTED

    deallocate(flux_stage32,source_stage32)
  end subroutine SPOR64_B2C_PUBLISH_IMPL
  logical function PROJECTED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    PROJECTED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_PLANE_SEED_AUTHORITY)
  end function PROJECTED_AUTHORITY_IS_EXACT


  logical function REAL64_FLUX_IS_VALID(ipauthority)
    type(c_ptr), intent(in) :: ipauthority
    integer :: ig, actual_length, actual_type
    real(real64) :: stage64(NUNKNO)
    type(c_ptr) :: ipflux

    REAL64_FLUX_IS_VALID = .false.
    if (.not. c_associated(ipauthority)) return
    ipflux = LCMGID(ipauthority,'FLUX')
    if (.not. c_associated(ipflux)) return
    do ig = 1, NGRP
      call LCMLEL(ipflux,ig,actual_length,actual_type)
      if (actual_length /= NUNKNO .or. actual_type /= 4) return
      call LCMGDL(ipflux,ig,stage64)
      if (.not. all(ieee_is_finite(stage64))) return
    end do
    REAL64_FLUX_IS_VALID = .true.
  end function REAL64_FLUX_IS_VALID
end module SPOR64_B2C
