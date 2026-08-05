module SPOR64_B2C
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
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

    integer :: state_vector(NSTATE)
    integer :: ig, ir, ilong, itylcm, allocation_status
    logical :: seen_unknown(NUNKNO)
    real(real32) :: eps_converge(5)
    real(real32), allocatable :: flux_stage32(:,:), source_stage32(:,:)
    type(c_ptr) :: authority, authority_flux, authority_source
    type(c_ptr) :: legacy_flux, legacy_source

    status = SPOR64_B2C_PREFLIGHT_FAILED

    ! The complete no-write preflight is deliberately ahead of LCMDID/LCMLID.
    if (accepted_token /= ACCEPTED_UNPUBLISHED) return
    if (.not. c_associated(ipflux)) return
    if (size(terminal_flux64,1) /= NUNKNO .or. &
        size(terminal_flux64,2) /= NGRP) return
    if (size(terminal_source64,1) /= NUNKNO .or. &
        size(terminal_source64,2) /= NGRP) return
    if (size(keyflx_base1) /= NREG) return
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

    seen_unknown = .false.
    do ir = 1, NREG
      if (keyflx_base1(ir) < 1 .or. keyflx_base1(ir) > NUNKNO) return
      if (seen_unknown(keyflx_base1(ir))) return
      seen_unknown(keyflx_base1(ir)) = .true.
    end do

    if (.not. ABSENT_RECORD(ipflux,'SPOT-R64')) return
    if (.not. ABSENT_RECORD(ipflux,'SOUR')) return
    if (.not. ABSENT_RECORD(ipflux,'AFLUX')) return
    if (.not. ABSENT_RECORD(ipflux,'DFLUX')) return
    if (.not. ABSENT_RECORD(ipflux,'ADFLUX')) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'STATE-VECTOR',NSTATE,1)) return
    if (.not. RECORD_MATCHES(ipflux,'EPS-CONVERGE',5,2)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'KEYFLX',NREG,1)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'OPTION',1,3)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'LINK.MACRO',3,3)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'LINK.TRACK',3,3)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'LINK.SYSTEM',3,3)) return
    if (.not. ABSENT_OR_MATCHES(ipflux,'SPOT-LEAK1D',NGRP,2)) return
    legacy_flux = LCMGID(ipflux,'FLUX')
    if (.not. c_associated(legacy_flux)) return
    do ig = 1, NGRP
      call LCMLEL(legacy_flux,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 2) return
    end do

    allocate(flux_stage32(NUNKNO,NGRP), &
        source_stage32(NUNKNO,NGRP),stat=allocation_status)
    if (allocation_status /= 0) then
      if (allocated(flux_stage32)) deallocate(flux_stage32)
      if (allocated(source_stage32)) deallocate(source_stage32)
      return
    end if

    ! Authoritative REAL64 child publication precedes every compatibility write.
    authority = LCMDID(ipflux,'SPOT-R64')
    if (.not. c_associated(authority)) &
        call XABORT('SPOR64_B2C: SPOT-R64 DIRECTORY CREATION FAILED.')
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

    ! Exactly one write-only REAL32 staging pass follows type-4 authority.
    flux_stage32 = real(terminal_flux64,real32)
    source_stage32 = real(terminal_source64,real32)
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
    state_vector(18) = 1
    eps_converge = [epsinr32,epsunk32,epsout32, &
        0.0_real32,0.0_real32]
    call LCMPUT(ipflux,'STATE-VECTOR',NSTATE,1,state_vector)
    call LCMPUT(ipflux,'EPS-CONVERGE',5,2,eps_converge)
    call LCMPUT(ipflux,'KEYFLX',NREG,1,keyflx_base1)
    call LCMPTC(ipflux,'OPTION',4,coptio)
    status = SPOR64_B2C_DRIVER_COMMITTED

    call LCMPTC(ipflux,'LINK.MACRO',12,macro_name)
    call LCMPTC(ipflux,'LINK.TRACK',12,track_name)
    call LCMPTC(ipflux,'LINK.SYSTEM',12,system_name)
    call LCMPUT(ipflux,'SPOT-LEAK1D',NGRP,2,leak1d_input32)
    status = SPOR64_B2C_HOST_COMMITTED

    deallocate(flux_stage32,source_stage32)
  end subroutine SPOR64_B2C_PUBLISH


  logical function RECORD_MATCHES(iplist,name,expected_length, &
      expected_type)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type

    RECORD_MATCHES = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    RECORD_MATCHES = actual_length == expected_length .and. &
        actual_type == expected_type
  end function RECORD_MATCHES


  logical function ABSENT_RECORD(iplist,name)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type

    ABSENT_RECORD = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    ABSENT_RECORD = actual_length == 0 .and. actual_type == 99
  end function ABSENT_RECORD


  logical function ABSENT_OR_MATCHES(iplist,name,expected_length, &
      expected_type)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type

    ABSENT_OR_MATCHES = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    ABSENT_OR_MATCHES = &
        (actual_length == 0 .and. actual_type == 99) .or. &
        (actual_length == expected_length .and. &
         actual_type == expected_type)
  end function ABSENT_OR_MATCHES

end module SPOR64_B2C
