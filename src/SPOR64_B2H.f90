module SPOR64_B2H
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  implicit none
  private

  integer, parameter, public :: SPOR64_B2H_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2H_PROJECTED_COMMITTED = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NMAT = 8
  integer, parameter :: NUNKNO = 14
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2H_RECONSTRUCT
  public :: SPOR64_B2H_PROJECT

contains

  pure subroutine SPOR64_B2H_RECONSTRUCT(basis32,coordinates64, &
      projected64,ok)
    real(real32), intent(in) :: basis32(:,:)
    real(real64), intent(in) :: coordinates64(:)
    real(real64), intent(out) :: projected64(:)
    logical, intent(out) :: ok
    integer :: i, a

    ok = .false.
    projected64 = +0.0_real64
    if (size(basis32,1) /= size(projected64)) return
    if (size(basis32,2) /= size(coordinates64)) return
    if (size(projected64) <= 0 .or. size(coordinates64) <= 0) return
    if (.not. all(ieee_is_finite(basis32))) return
    if (.not. all(ieee_is_finite(coordinates64))) return

    ! This is the fixed-space SPOPROJ contraction before its legacy downcast.
    ! The loop order is part of the frozen numerical definition.
    do i = 1, size(projected64)
      do a = 1, size(coordinates64)
        projected64(i) = projected64(i) + &
            real(basis32(i,a),real64) * coordinates64(a)
      end do
    end do
    if (.not. all(ieee_is_finite(projected64))) return
    if (any(projected64 <= +0.0_real64)) return
    ok = .true.
  end subroutine SPOR64_B2H_RECONSTRUCT


  subroutine SPOR64_B2H_PROJECT(ipout,ipseed,iptrack,projected_region64, &
      rho64,status)
    type(c_ptr), intent(in) :: ipout, ipseed, iptrack
    real(real64), intent(in) :: projected_region64(:,:)
    real(real64), intent(in) :: rho64
    integer, intent(out) :: status

    integer :: state_vector(NSTATE), track_state(NSTATE)
    integer :: keyflx(NREG), seed_keyflx(NREG), imerge(NMAT)
    integer :: seed_epoch, output_epoch
    integer :: ig, ir, ilong, itylcm, allocation_status
    logical :: seen_unknown(NUNKNO)
    real(real32) :: eps_converge(5), leak1d(NGRP)
    real(real64) :: leak1d64(NGRP)
    logical :: have_leak1d64
    real(real64) :: seed_rho64
    real(real64), allocatable :: seed_flux64(:,:), seed_source64(:,:)
    real(real64), allocatable :: projected_flux64(:,:)
    real(real32), allocatable :: flux_stage32(:,:)
    character(len=4) :: option
    character(len=12) :: signature, macro_name, track_name, system_name
    character(len=12) :: authority_state
    type(c_ptr) :: seed_authority, seed_flux, seed_source
    type(c_ptr) :: output_authority, output_flux, legacy_flux

    status = SPOR64_B2H_ADMISSION_FAILED

    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipseed)) return
    if (.not. c_associated(iptrack)) return
    if (c_associated(ipout,ipseed)) return
    if (c_associated(ipout,iptrack)) return
    if (c_associated(ipseed,iptrack)) return
    if (.not. EMPTY_LCM_ROOT(ipout)) return
    if (size(projected_region64,1) /= NREG) return
    if (size(projected_region64,2) /= NGRP) return
    ! This boundary checks the scalar representation only.  A future host
    ! gate must prove that rho64 and projected_region64 came from the same
    ! canonical SPOSTATE object and archive epoch.
    if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64) return
    if (.not. all(ieee_is_finite(projected_region64))) return
    if (any(projected_region64 <= +0.0_real64)) return

    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipseed,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipseed,'STATE-VECTOR',state_vector)
    if (state_vector(1) /= NGRP .or. state_vector(2) /= NUNKNO) return
    if (state_vector(3) /= 1) return
    if (any(state_vector(4:7) /= 0)) return
    if (state_vector(8) /= 3 .or. state_vector(9) /= 3) return
    if (state_vector(10) /= 1 .or. state_vector(17) /= NMAT) return
    if (state_vector(11) /= 740 .or. state_vector(12) /= 500) return
    if (state_vector(18) /= 1) return
    if (any(state_vector(13:16) /= 0)) return
    if (any(state_vector(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(ipseed,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipseed,'EPS-CONVERGE',eps_converge)
    if (.not. all(ieee_is_finite(eps_converge))) return
    if (transfer(eps_converge(1),0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(eps_converge(2),0_int32) /= FROZEN_TOL_BITS) return
    if (transfer(eps_converge(3),0_int32) /= FROZEN_TOL_BITS) return
    if (any(abs(eps_converge(4:5)) > +0.0_real32)) return
    if (.not. RECORD_MATCHES(ipseed,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(ipseed,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(ipseed,'KEYFLX',NREG,1)) return
    call LCMGET(ipseed,'KEYFLX',seed_keyflx)
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'OPTION',1,4,'B0  ')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipseed,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(ipseed,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(ipseed,'SPOT-LEAK1D',leak1d)
    if (.not. all(ieee_is_finite(leak1d))) return
    ! Presence-gated REAL64 leakage authority; when present the REAL32
    ! record must be its exact bitwise demote mirror.
    call LCMLEN(ipseed,'LEAK1D64',ilong,itylcm)
    have_leak1d64 = (ilong == NGRP .and. itylcm == 4)
    if (ilong /= 0 .and. .not. have_leak1d64) return
    leak1d64 = 0.0_real64
    if (have_leak1d64) then
      call LCMGET(ipseed,'LEAK1D64',leak1d64)
      if (.not. all(ieee_is_finite(leak1d64))) return
      do ig = 1, NGRP
        if (transfer(leak1d(ig),0_int32) /= &
            transfer(real(leak1d64(ig),real32),0_int32)) return
      end do
    end if

    if (.not. CHARACTER_RECORD_MATCHES(iptrack,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. RECORD_MATCHES(iptrack,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(iptrack,'STATE-VECTOR',track_state)
    if (track_state(1) /= NREG .or. track_state(2) /= NUNKNO) return
    if (.not. RECORD_MATCHES(iptrack,'KEYFLX$ANIS',NREG,1)) return
    call LCMGET(iptrack,'KEYFLX$ANIS',keyflx)
    if (any(seed_keyflx /= keyflx)) return
    seen_unknown = .false.
    do ir = 1, NREG
      if (keyflx(ir) < 1 .or. keyflx(ir) > NUNKNO) return
      if (seen_unknown(keyflx(ir))) return
      seen_unknown(keyflx(ir)) = .true.
    end do

    if (.not. RECORD_MATCHES(ipseed,'SPOT-R64',-1,0)) return
    seed_authority = LCMGID(ipseed,'SPOT-R64')
    if (.not. c_associated(seed_authority)) return
    if (.not. CHARACTER_RECORD_MATCHES(seed_authority,'STATE',3,12, &
        'SOLVED')) return
    if (.not. RECORD_MATCHES(seed_authority,'EPOCH',1,1)) return
    call LCMGET(seed_authority,'EPOCH',seed_epoch)
    if (seed_epoch < 0 .or. seed_epoch == huge(seed_epoch)) return
    output_epoch = seed_epoch + 1
    if (.not. RECORD_MATCHES(seed_authority,'RHO',1,4)) return
    call LCMGET(seed_authority,'RHO',seed_rho64)
    if (.not. ieee_is_finite(seed_rho64) .or. &
        seed_rho64 <= +0.0_real64) return
    if (.not. RECORD_MATCHES(seed_authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(seed_authority,'SOUR',NGRP,10)) return
    seed_flux = LCMGID(seed_authority,'FLUX')
    seed_source = LCMGID(seed_authority,'SOUR')
    if (.not. c_associated(seed_flux)) return
    if (.not. c_associated(seed_source)) return

    allocate(seed_flux64(NUNKNO,NGRP),seed_source64(NUNKNO,NGRP), &
        projected_flux64(NUNKNO,NGRP),flux_stage32(NUNKNO,NGRP), &
        stat=allocation_status)
    if (allocation_status /= 0) then
      if (allocated(seed_flux64)) deallocate(seed_flux64)
      if (allocated(seed_source64)) deallocate(seed_source64)
      if (allocated(projected_flux64)) deallocate(projected_flux64)
      if (allocated(flux_stage32)) deallocate(flux_stage32)
      return
    end if
    do ig = 1, NGRP
      call LCMLEL(seed_flux,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 4) return
      call LCMGDL(seed_flux,ig,seed_flux64(:,ig))
      if (.not. all(ieee_is_finite(seed_flux64(:,ig)))) return
      call LCMLEL(seed_source,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 4) return
      call LCMGDL(seed_source,ig,seed_source64(:,ig))
      if (.not. all(ieee_is_finite(seed_source64(:,ig)))) return
    end do

    projected_flux64 = seed_flux64
    do ig = 1, NGRP
      do ir = 1, NREG
        projected_flux64(keyflx(ir),ig) = projected_region64(ir,ig)
      end do
    end do
    if (.not. all(ieee_is_finite(projected_flux64))) return
    if (any(abs(projected_flux64) > REAL32_MAX64)) return
    flux_stage32 = real(projected_flux64,real32)
    if (.not. all(ieee_is_finite(flux_stage32))) return
    if (.not. EMPTY_LCM_ROOT(ipout)) return

    ! Publish the REAL64 payload first.  STATE and EPOCH are withheld until
    ! every authoritative and compatibility payload has been written, so a
    ! projected state is never inferred from directory presence alone.
    output_authority = LCMDID(ipout,'SPOT-R64')
    if (.not. c_associated(output_authority)) &
        call XABORT('SPOR64_B2H: AUTHORITY DIRECTORY CREATION FAILED.')
    authority_state = 'PROJECTED'
    call LCMPUT(output_authority,'RHO',1,4,rho64)
    output_flux = LCMLID(output_authority,'FLUX',NGRP)
    if (.not. c_associated(output_flux)) &
        call XABORT('SPOR64_B2H: TYPE-4 FLUX LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(output_flux,ig,NUNKNO,4,projected_flux64(:,ig))
    end do

    ! The root FLUX is a write-only compatibility mirror derived from the
    ! authority.  No SOUR or frozen-source diagnostic is copied forward.
    legacy_flux = LCMLID(ipout,'FLUX',NGRP)
    if (.not. c_associated(legacy_flux)) &
        call XABORT('SPOR64_B2H: TYPE-2 FLUX LIST CREATION FAILED.')
    do ig = 1, NGRP
      call LCMPDL(legacy_flux,ig,NUNKNO,2,flux_stage32(:,ig))
    end do
    signature = 'L_FLUX'
    macro_name = 'MACRO0'
    track_name = 'TRACK'
    system_name = 'SYSTEM'
    option = 'B0  '
    call LCMPTC(ipout,'SIGNATURE',12,signature)
    call LCMPUT(ipout,'STATE-VECTOR',NSTATE,1,state_vector)
    call LCMPUT(ipout,'EPS-CONVERGE',5,2,eps_converge)
    call LCMPUT(ipout,'IMERGE-LEAK',NMAT,1,imerge)
    call LCMPUT(ipout,'KEYFLX',NREG,1,keyflx)
    call LCMPTC(ipout,'OPTION',4,option)
    call LCMPTC(ipout,'LINK.MACRO',12,macro_name)
    call LCMPTC(ipout,'LINK.TRACK',12,track_name)
    call LCMPTC(ipout,'LINK.SYSTEM',12,system_name)
    call LCMPUT(ipout,'SPOT-LEAK1D',NGRP,2,leak1d)
    if (have_leak1d64) call LCMPUT(ipout,'LEAK1D64',NGRP,4,leak1d64)
    call LCMPTC(output_authority,'STATE',12,authority_state)
    call LCMPUT(output_authority,'EPOCH',1,1,output_epoch)
    status = SPOR64_B2H_PROJECTED_COMMITTED

    deallocate(flux_stage32,projected_flux64,seed_source64,seed_flux64)
  end subroutine SPOR64_B2H_PROJECT


  logical function EMPTY_LCM_ROOT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    EMPTY_LCM_ROOT = .false.
    if (.not. c_associated(iplist)) return
    call LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)
    EMPTY_LCM_ROOT = is_lcm .and. empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_LCM_ROOT


  logical function RECORD_MATCHES(iplist,name,expected_length,expected_type)
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


  logical function CHARACTER_RECORD_MATCHES(iplist,name,expected_length, &
      character_count,expected)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: expected_length, character_count
    character(len=:), allocatable :: found

    CHARACTER_RECORD_MATCHES = .false.
    if (.not. RECORD_MATCHES(iplist,name,expected_length,3)) return
    allocate(character(len=character_count) :: found)
    found(:) = ' '
    call LCMGTC(iplist,name,character_count,found)
    CHARACTER_RECORD_MATCHES = found == expected
    deallocate(found)
  end function CHARACTER_RECORD_MATCHES

end module SPOR64_B2H
