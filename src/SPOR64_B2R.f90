module SPOR64_B2R
  ! Collects the three SOLVED planes into one RETURNED archive.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : CHARACTER_RECORD_MATCHES, EMPTY_MEMORY_ROOT, &
      EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, RECORD_MATCHES, &
      SAME_REAL32_BITS
  use SPOR64_SCHEMA, only : SCHEMA_ARCHIVE_ROOT_AUTHORITY, &
      SCHEMA_CLOSED_ARCHIVE_ROOT, SCHEMA_SOLVED_PLANE_AUTHORITY, &
      SCHEMA_SOLVED_ROOT, SCHEMA_SOURCE_AUTHORITY, SCHEMA_SOURCE_ROOT, &
      SCHEMA_SYSTEM_AUTHORITY, SCHEMA_SYSTEM_ROOT, SCHEMA_SYSTEM_ROOT_L1RAW
  implicit none
  private

  integer, parameter, public :: SPOR64_B2R_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2R_RETURNED = 2

  integer, parameter :: NSNAP = 3
  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NMAT = 8
  integer, parameter :: NUNKNO = 14
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2R_COLLECT

contains

  subroutine SPOR64_B2R_COLLECT(ipout,ipassembled,ipsolved,ipsources,status)
    type(c_ptr), intent(in) :: ipout, ipassembled
    type(c_ptr), intent(in) :: ipsolved(NSNAP), ipsources(NSNAP)
    integer, intent(out) :: status

    integer :: ip, jp, slot, plane, root_planes, root_epoch
    integer :: allocation_status
    integer :: solved_slot(NSNAP), source_slot(NSNAP)
    integer :: solved_plane(NSNAP), source_plane(NSNAP)
    integer :: track_key(NREG,NSNAP), solved_key(NREG,NSNAP)
    integer :: fs_marker
    integer(int64) :: expected64
    real(real32) :: system_leak(NGRP,NSNAP)
    real(real32) :: solved_leak(NGRP,NSNAP)
    real(real32) :: source_keff32(NSNAP)
    real(real64) :: solved_leak64(NGRP,NSNAP)
    real(real32), allocatable :: qmirror32(:,:,:)
    real(real64) :: iter_keff64, root_rho64
    real(real64), allocatable :: qfiss64(:,:,:)
    character(len=12) :: signature, lifecycle_state
    type(c_ptr) :: root_authority
    type(c_ptr) :: tracks, libraries, systems, projected_fluxes
    type(c_ptr) :: input_track(NSNAP), input_library(NSNAP)
    type(c_ptr) :: input_system(NSNAP)
    type(c_ptr) :: output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes, output_item
    type(c_ptr) :: output_authority, output_qfiss
    type(c_ptr) :: legacy_outer, legacy_inner

    status = SPOR64_B2R_PREFLIGHT_FAILED
    solved_slot = 0
    source_slot = 0

    ! The ABI owns no loose plane, RHO, k, epoch, tolerance, or relaxation.
    ! All supplied objects are immutable and every rejection precedes output.
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipassembled)) return
    if (c_associated(ipout,ipassembled)) return
    do ip = 1, NSNAP
      if (.not. c_associated(ipsolved(ip))) return
      if (.not. c_associated(ipsources(ip))) return
      if (c_associated(ipout,ipsolved(ip))) return
      if (c_associated(ipout,ipsources(ip))) return
      if (c_associated(ipassembled,ipsolved(ip))) return
      if (c_associated(ipassembled,ipsources(ip))) return
    end do
    do ip = 1, NSNAP
      do jp = 1, NSNAP
        if (c_associated(ipsolved(ip),ipsources(jp))) return
      end do
      do jp = ip+1, NSNAP
        if (c_associated(ipsolved(ip),ipsolved(jp))) return
        if (c_associated(ipsources(ip),ipsources(jp))) return
      end do
    end do
    if (.not. EMPTY_MEMORY_ROOT(ipout)) return

    ! Admit one B2k ASSEMBLED/e archive.  Its RHO is the bitwise reciprocal of
    ! the current outer-state eigenvalue used by the radial equation and is
    ! the common generation label.
    if (.not. ASSEMBLED_ROOT_IS_EXACT(ipassembled)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipassembled,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipassembled,'LISTDIM',1,1)) return
    if (.not. RECORD_MATCHES(ipassembled,'SPOT-ITER-K',1,4)) return
    if (.not. RECORD_MATCHES(ipassembled,'SPOT-R64',-1,0)) return
    call LCMGET(ipassembled,'LISTDIM',root_planes)
    call LCMGET(ipassembled,'SPOT-ITER-K',iter_keff64)
    if (root_planes /= NSNAP) return
    if (.not. ieee_is_finite(iter_keff64)) return
    if (iter_keff64 <= +0.0_real64) return
    root_authority = LCMGID(ipassembled,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',root_rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(root_rho64)) return
    if (root_rho64 <= +0.0_real64) return
    if (root_planes /= NSNAP .or. root_epoch <= 0) return
    expected64 = transfer(1.0_real64/iter_keff64,0_int64)
    if (transfer(root_rho64,0_int64) /= expected64) return

    if (.not. RECORD_MATCHES(ipassembled,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipassembled,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipassembled,'SYSTEM',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipassembled,'FLUX',NSNAP,10)) return
    tracks = LCMGID(ipassembled,'TRACK')
    libraries = LCMGID(ipassembled,'MICROLIB2')
    systems = LCMGID(ipassembled,'SYSTEM')
    projected_fluxes = LCMGID(ipassembled,'FLUX')
    if (.not. c_associated(tracks)) return
    if (.not. c_associated(libraries)) return
    if (.not. c_associated(systems)) return
    if (.not. c_associated(projected_fluxes)) return

    ! The archive list index is the owner of TRACK/MICROLIB2/SYSTEM identity.
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(systems,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(projected_fluxes,ip)) return
      input_track(ip) = LCMGIL(tracks,ip)
      input_library(ip) = LCMGIL(libraries,ip)
      input_system(ip) = LCMGIL(systems,ip)
      if (.not. c_associated(input_track(ip))) return
      if (.not. c_associated(input_library(ip))) return
      if (.not. c_associated(input_system(ip))) return
      if (.not. TRACK_IS_VALID(input_track(ip),track_key(:,ip))) return
      if (.not. LIBRARY_IS_VALID(input_library(ip))) return
      if (.not. SYSTEM_IS_VALID(input_system(ip),ip,root_rho64, &
          root_epoch,system_leak(:,ip))) return
    end do

    allocate(qfiss64(NUNKNO,NGRP,NSNAP), &
        qmirror32(NUNKNO,NGRP,NSNAP),stat=allocation_status)
    if (allocation_status /= 0) return

    ! Argument order has no meaning.  Each detached set must independently
    ! contain the exact label set {1,2,3}; duplicates imply an omission.
    do slot = 1, NSNAP
      if (.not. SOLVED_IS_VALID(ipsolved(slot),root_rho64,root_epoch, &
          solved_plane(slot),solved_key(:,slot),solved_leak(:,slot), &
          solved_leak64(:,slot))) return
      plane = solved_plane(slot)
      if (solved_slot(plane) /= 0) return
      solved_slot(plane) = slot

      if (.not. SOURCE_IS_VALID(ipsources(slot),root_rho64,root_epoch, &
          iter_keff64,source_plane(slot),source_keff32(slot), &
          qfiss64(:,:,slot),qmirror32(:,:,slot))) return
      plane = source_plane(slot)
      if (source_slot(plane) /= 0) return
      source_slot(plane) = slot
    end do
    if (any(solved_slot == 0) .or. any(source_slot == 0)) return

    ! Bind every detached label to the same archive index without tolerance.
    do plane = 1, NSNAP
      slot = solved_slot(plane)
      if (any(solved_key(:,slot) /= track_key(:,plane))) return
      if (.not. SAME_REAL32_BITS(solved_leak(:,slot), &
          system_leak(:,plane))) return
    end do

    ! Close the time-of-check window immediately before caller-visible writes.
    if (.not. EMPTY_MEMORY_ROOT(ipout)) return

    signature = 'L_ARCHIVE'
    call LCMPTC(ipout,'SIGNATURE',12,signature)
    call LCMPUT(ipout,'LISTDIM',1,1,root_planes)
    output_tracks = LCMLID(ipout,'TRACK',NSNAP)
    output_libraries = LCMLID(ipout,'MICROLIB2',NSNAP)
    output_systems = LCMLID(ipout,'SYSTEM',NSNAP)
    output_fluxes = LCMLID(ipout,'FLUX',NSNAP)
    if (.not. c_associated(output_tracks)) &
        call XABORT('SPOR64_B2R: OUTPUT TRACK LIST CREATION FAILED.')
    if (.not. c_associated(output_libraries)) &
        call XABORT('SPOR64_B2R: OUTPUT LIBRARY LIST CREATION FAILED.')
    if (.not. c_associated(output_systems)) &
        call XABORT('SPOR64_B2R: OUTPUT SYSTEM LIST CREATION FAILED.')
    if (.not. c_associated(output_fluxes)) &
        call XABORT('SPOR64_B2R: OUTPUT FLUX LIST CREATION FAILED.')

    do plane = 1, NSNAP
      output_item = LCMDIL(output_tracks,plane)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2R: OUTPUT TRACK ITEM CREATION FAILED.')
      call LCMEQU(input_track(plane),output_item)
      output_item = LCMDIL(output_libraries,plane)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2R: OUTPUT LIBRARY ITEM CREATION FAILED.')
      call LCMEQU(input_library(plane),output_item)
      output_item = LCMDIL(output_systems,plane)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2R: OUTPUT SYSTEM ITEM CREATION FAILED.')
      call LCMEQU(input_system(plane),output_item)

      slot = solved_slot(plane)
      output_item = LCMDIL(output_fluxes,plane)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2R: OUTPUT FLUX ITEM CREATION FAILED.')
      call LCMEQU(ipsolved(slot),output_item)
      output_authority = LCMGID(output_item,'SPOT-R64')
      if (.not. c_associated(output_authority)) &
          call XABORT('SPOR64_B2R: COPIED SOLVED AUTHORITY MISSING.')

      ! Inside an archive, list index is the sole plane owner.  QFISS remains
      ! type-4 authority and is never reconstructed from terminal SOUR.
      call LCMDEL(output_authority,'PLANE')
      output_qfiss = LCMLID(output_authority,'QFISS',NGRP)
      if (.not. c_associated(output_qfiss)) &
          call XABORT('SPOR64_B2R: OUTPUT QFISS AUTHORITY FAILED.')
      jp = source_slot(plane)
      do ip = 1, NGRP
        call LCMPDL(output_qfiss,ip,NUNKNO,4,qfiss64(:,ip,jp))
      end do

      fs_marker = 1
      call LCMPUT(output_item,'SPOT-FS-EQN',1,1,fs_marker)
      call LCMPUT(output_item,'SPOT-FS-K',1,2,source_keff32(jp))
      legacy_outer = LCMLID(output_item,'SPOT-QFISS',1)
      if (.not. c_associated(legacy_outer)) &
          call XABORT('SPOR64_B2R: LEGACY QFISS OUTER LIST FAILED.')
      legacy_inner = LCMLIL(legacy_outer,1,NGRP)
      if (.not. c_associated(legacy_inner)) &
          call XABORT('SPOR64_B2R: LEGACY QFISS INNER LIST FAILED.')
      do ip = 1, NGRP
        call LCMPDL(legacy_inner,ip,NUNKNO,2,qmirror32(:,ip,jp))
      end do
      ! This rewrite is the final mutation of the returned child authority.
      call LCMPUT(output_authority,'EPOCH',1,1,root_epoch)
    end do

    ! RETURNED is deliberately unclosed.  The aggregate owns neither RHO nor
    ! k; a later axial solve and close gate own the next-generation values.
    root_authority = LCMDID(ipout,'SPOT-R64')
    if (.not. c_associated(root_authority)) &
        call XABORT('SPOR64_B2R: ROOT AUTHORITY CREATION FAILED.')
    call LCMPUT(root_authority,'NPLANE',1,1,root_planes)
    lifecycle_state = 'RETURNED'
    call LCMPTC(root_authority,'STATE',12,lifecycle_state)
    ! Root EPOCH is the archive-wide commit and final output mutation.
    call LCMPUT(root_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_B2R_RETURNED
  end subroutine SPOR64_B2R_COLLECT


  logical function TRACK_IS_VALID(track,keyanis)
    type(c_ptr), intent(in) :: track
    integer, intent(out) :: keyanis(NREG)
    integer :: ir, keyflx(NREG)
    logical :: seen(NUNKNO)

    TRACK_IS_VALID = .false.
    if (.not. CHARACTER_RECORD_MATCHES(track,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. RECORD_MATCHES(track,'KEYFLX',NREG,1)) return
    if (.not. RECORD_MATCHES(track,'KEYFLX$ANIS',NREG,1)) return
    call LCMGET(track,'KEYFLX',keyflx)
    call LCMGET(track,'KEYFLX$ANIS',keyanis)
    if (any(keyflx /= keyanis)) return
    seen = .false.
    do ir = 1, NREG
      if (keyanis(ir) < 1 .or. keyanis(ir) > NUNKNO) return
      if (seen(keyanis(ir))) return
      seen(keyanis(ir)) = .true.
    end do
    TRACK_IS_VALID = .true.
  end function TRACK_IS_VALID


  logical function LIBRARY_IS_VALID(library)
    type(c_ptr), intent(in) :: library

    LIBRARY_IS_VALID = CHARACTER_RECORD_MATCHES(library,'SIGNATURE', &
        3,12,'L_LIBRARY')
  end function LIBRARY_IS_VALID


  logical function SYSTEM_IS_VALID(system,plane,rho,epoch,leakage)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane, epoch
    real(real64), intent(in) :: rho
    real(real32), intent(out) :: leakage(NGRP)

    integer :: state(NSTATE), found_plane, found_epoch
    real(real64) :: found_rho
    type(c_ptr) :: authority

    SYSTEM_IS_VALID = .false.
    if (.not. SYSTEM_ROOT_IS_EXACT(system)) return
    if (.not. CHARACTER_RECORD_MATCHES(system,'SIGNATURE',3,12, &
        'L_PIJ')) return
    if (.not. CHARACTER_RECORD_MATCHES(system,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(system,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. RECORD_MATCHES(system,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(system,'STATE-VECTOR',state)
    if (any(state(1:14) /= &
        [1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0])) return
    if (any(state(15:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(system,'SPOT-LEAK1D',NGRP,2)) return
    if (.not. RECORD_MATCHES(system,'SPOT-L1-SNAP',1,1)) return
    if (.not. RECORD_MATCHES(system,'GROUP',NGRP,10)) return
    if (.not. RECORD_MATCHES(system,'SPOT-R64',-1,0)) return
    call LCMGET(system,'SPOT-LEAK1D',leakage)
    call LCMGET(system,'SPOT-L1-SNAP',found_plane)
    if (.not. all(ieee_is_finite(leakage))) return
    if (found_plane /= plane) return
    authority = LCMGID(system,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. SYSTEM_AUTHORITY_IS_EXACT(authority)) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'EPOCH',found_epoch)
    if (.not. ieee_is_finite(found_rho)) return
    if (transfer(found_rho,0_int64) /= transfer(rho,0_int64)) return
    if (found_epoch /= epoch) return
    SYSTEM_IS_VALID = .true.
  end function SYSTEM_IS_VALID


  logical function SOLVED_IS_VALID(solved,rho,epoch,plane,keyflx, &
      leakage,leakage64)
    type(c_ptr), intent(in) :: solved
    real(real64), intent(in) :: rho
    integer, intent(in) :: epoch
    integer, intent(out) :: plane, keyflx(NREG)
    real(real32), intent(out) :: leakage(NGRP)
    real(real64), intent(out) :: leakage64(NGRP)

    integer :: state(NSTATE), imerge(NMAT), found_epoch
    integer :: ig, ir
    integer(int32) :: eps_bits(5)
    real(real32) :: eps(5), mirror_flux(NUNKNO), mirror_source(NUNKNO)
    real(real64) :: found_rho, auth_flux(NUNKNO), auth_source(NUNKNO)
    logical :: seen(NUNKNO)
    type(c_ptr) :: authority, root_flux, root_source
    type(c_ptr) :: authority_flux, authority_source

    SOLVED_IS_VALID = .false.
    if (.not. SOLVED_ROOT_IS_EXACT(solved)) return
    if (.not. CHARACTER_RECORD_MATCHES(solved,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(solved,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(solved,'STATE-VECTOR',state)
    if (any(state(1:18) /= &
        [NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500,0,0,0,0,NMAT,1])) return
    if (any(state(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(solved,'EPS-CONVERGE',5,2)) return
    call LCMGET(solved,'EPS-CONVERGE',eps)
    if (.not. all(ieee_is_finite(eps))) return
    eps_bits = transfer(eps,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS)) return
    if (any(eps_bits(4:5) /= 0_int32)) return
    if (.not. RECORD_MATCHES(solved,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(solved,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(solved,'KEYFLX',NREG,1)) return
    call LCMGET(solved,'KEYFLX',keyflx)
    seen = .false.
    do ir = 1, NREG
      if (keyflx(ir) < 1 .or. keyflx(ir) > NUNKNO) return
      if (seen(keyflx(ir))) return
      seen(keyflx(ir)) = .true.
    end do
    if (.not. CHARACTER_RECORD_MATCHES(solved,'OPTION',1,4,'B0  ')) return
    if (.not. CHARACTER_RECORD_MATCHES(solved,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(solved,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(solved,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(solved,'SPOT-LEAK1D',NGRP,2)) return
    if (.not. RECORD_MATCHES(solved,'LEAK1D64',NGRP,4)) return
    call LCMGET(solved,'SPOT-LEAK1D',leakage)
    call LCMGET(solved,'LEAK1D64',leakage64)
    if (.not. all(ieee_is_finite(leakage))) return
    if (.not. all(ieee_is_finite(leakage64))) return
    if (.not. SAME_REAL32_BITS(leakage,real(leakage64,real32))) return
    if (.not. RECORD_MATCHES(solved,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(solved,'SOUR',NGRP,10)) return
    if (.not. RECORD_MATCHES(solved,'SPOT-R64',-1,0)) return
    root_flux = LCMGID(solved,'FLUX')
    root_source = LCMGID(solved,'SOUR')
    authority = LCMGID(solved,'SPOT-R64')
    if (.not. c_associated(root_flux)) return
    if (.not. c_associated(root_source)) return
    if (.not. c_associated(authority)) return
    if (.not. SOLVED_AUTHORITY_IS_EXACT(authority)) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(authority,'PLANE',1,1)) return
    if (.not. RECORD_MATCHES(authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(authority,'SOUR',NGRP,10)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'SOLVED')) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'PLANE',plane)
    call LCMGET(authority,'EPOCH',found_epoch)
    if (.not. ieee_is_finite(found_rho)) return
    if (transfer(found_rho,0_int64) /= transfer(rho,0_int64)) return
    if (plane < 1 .or. plane > NSNAP) return
    if (found_epoch /= epoch) return
    authority_flux = LCMGID(authority,'FLUX')
    authority_source = LCMGID(authority,'SOUR')
    if (.not. c_associated(authority_flux)) return
    if (.not. c_associated(authority_source)) return
    do ig = 1, NGRP
      if (.not. LIST_ITEM_MATCHES(root_flux,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(root_source,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(authority_flux,ig,NUNKNO,4)) return
      if (.not. LIST_ITEM_MATCHES(authority_source,ig,NUNKNO,4)) return
      call LCMGDL(root_flux,ig,mirror_flux)
      call LCMGDL(root_source,ig,mirror_source)
      call LCMGDL(authority_flux,ig,auth_flux)
      call LCMGDL(authority_source,ig,auth_source)
      if (.not. all(ieee_is_finite(mirror_flux))) return
      if (.not. all(ieee_is_finite(mirror_source))) return
      if (.not. all(ieee_is_finite(auth_flux))) return
      if (.not. all(ieee_is_finite(auth_source))) return
      if (.not. MIRROR_MATCHES_REAL64(mirror_flux,auth_flux)) return
      if (.not. MIRROR_MATCHES_REAL64(mirror_source,auth_source)) return
    end do
    SOLVED_IS_VALID = .true.
  end function SOLVED_IS_VALID


  logical function SOURCE_IS_VALID(source,rho,epoch,iter_keff,plane, &
      source_keff,qfiss,qmirror)
    type(c_ptr), intent(in) :: source
    real(real64), intent(in) :: rho, iter_keff
    integer, intent(in) :: epoch
    integer, intent(out) :: plane
    real(real32), intent(out) :: source_keff
    real(real64), intent(out) :: qfiss(NUNKNO,NGRP)
    real(real32), intent(out) :: qmirror(NUNKNO,NGRP)

    integer :: state(NSTATE), frozen, found_epoch, ig
    real(real32) :: qint(NGRP)
    real(real64) :: found_rho
    type(c_ptr) :: authority, authority_qfiss
    type(c_ptr) :: source_outer, source_inner

    SOURCE_IS_VALID = .false.
    if (.not. SOURCE_ROOT_IS_EXACT(source)) return
    if (.not. CHARACTER_RECORD_MATCHES(source,'SIGNATURE',3,12, &
        'L_SOURCE')) return
    if (.not. RECORD_MATCHES(source,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(source,'STATE-VECTOR',state)
    if (any(state(1:3) /= [NGRP,NUNKNO,1])) return
    if (any(state(4:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(source,'SPOT-FROZEN',1,1)) return
    call LCMGET(source,'SPOT-FROZEN',frozen)
    if (frozen /= 1) return
    if (.not. RECORD_MATCHES(source,'SPOT-KEFF',1,2)) return
    call LCMGET(source,'SPOT-KEFF',source_keff)
    if (.not. ieee_is_finite(source_keff)) return
    if (source_keff <= +0.0_real32) return
    if (transfer(source_keff,0_int32) /= &
        transfer(real(iter_keff,real32),0_int32)) return
    if (.not. RECORD_MATCHES(source,'SPOT-QINT',NGRP,2)) return
    call LCMGET(source,'SPOT-QINT',qint)
    if (.not. all(ieee_is_finite(qint))) return
    if (any(qint < +0.0_real32) .or. qint(1) <= +0.0_real32) return
    if (.not. RECORD_MATCHES(source,'DSOUR',1,10)) return
    source_outer = LCMGID(source,'DSOUR')
    if (.not. c_associated(source_outer)) return
    if (.not. LIST_ITEM_MATCHES(source_outer,1,NGRP,10)) return
    source_inner = LCMGIL(source_outer,1)
    if (.not. c_associated(source_inner)) return

    if (.not. RECORD_MATCHES(source,'SPOT-R64',-1,0)) return
    authority = LCMGID(source,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. SOURCE_AUTHORITY_IS_EXACT(authority)) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(authority,'PLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'FROZEN-QFIS')) return
    if (.not. RECORD_MATCHES(authority,'QFISS',NGRP,10)) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'PLANE',plane)
    call LCMGET(authority,'EPOCH',found_epoch)
    if (.not. ieee_is_finite(found_rho)) return
    if (transfer(found_rho,0_int64) /= transfer(rho,0_int64)) return
    if (plane < 1 .or. plane > NSNAP) return
    if (found_epoch /= epoch) return
    authority_qfiss = LCMGID(authority,'QFISS')
    if (.not. c_associated(authority_qfiss)) return
    do ig = 1, NGRP
      if (.not. LIST_ITEM_MATCHES(source_inner,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(authority_qfiss,ig,NUNKNO,4)) return
      call LCMGDL(source_inner,ig,qmirror(:,ig))
      call LCMGDL(authority_qfiss,ig,qfiss(:,ig))
      if (.not. all(ieee_is_finite(qmirror(:,ig)))) return
      if (.not. all(ieee_is_finite(qfiss(:,ig)))) return
      if (any(qmirror(:,ig) < +0.0_real32)) return
      if (any(qfiss(:,ig) < +0.0_real64)) return
      if (.not. MIRROR_MATCHES_REAL64(qmirror(:,ig),qfiss(:,ig))) return
    end do
    SOURCE_IS_VALID = .true.
  end function SOURCE_IS_VALID


  logical function MIRROR_MATCHES_REAL64(mirror,authority)
    real(real32), intent(in) :: mirror(:)
    real(real64), intent(in) :: authority(:)
    integer(int32), allocatable :: mirror_bits(:), projected_bits(:)
    integer :: allocation_status

    MIRROR_MATCHES_REAL64 = .false.
    if (size(mirror) /= size(authority)) return
    allocate(mirror_bits(size(mirror)),projected_bits(size(mirror)), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    mirror_bits = transfer(mirror,0_int32,size(mirror))
    projected_bits = transfer(real(authority,real32),0_int32,size(mirror))
    MIRROR_MATCHES_REAL64 = all(mirror_bits == projected_bits)
  end function MIRROR_MATCHES_REAL64
  logical function LIST_ITEM_MATCHES(iplist,index,expected_length, &
      expected_type)
    type(c_ptr), intent(in) :: iplist
    integer, intent(in) :: index, expected_length, expected_type
    integer :: actual_length, actual_type

    LIST_ITEM_MATCHES = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEL(iplist,index,actual_length,actual_type)
    LIST_ITEM_MATCHES = actual_length == expected_length .and. &
        actual_type == expected_type
  end function LIST_ITEM_MATCHES
  logical function ASSEMBLED_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    ASSEMBLED_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_CLOSED_ARCHIVE_ROOT)
  end function ASSEMBLED_ROOT_IS_EXACT


  logical function ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_ARCHIVE_ROOT_AUTHORITY)
  end function ROOT_AUTHORITY_IS_EXACT


  logical function SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_ROOT_L1RAW) &
        .or. EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_ROOT)
  end function SYSTEM_ROOT_IS_EXACT


  logical function SYSTEM_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SYSTEM_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_AUTHORITY)
  end function SYSTEM_AUTHORITY_IS_EXACT


  logical function SOLVED_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SOLVED_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOLVED_ROOT)
  end function SOLVED_ROOT_IS_EXACT


  logical function SOLVED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SOLVED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOLVED_PLANE_AUTHORITY)
  end function SOLVED_AUTHORITY_IS_EXACT


  logical function SOURCE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SOURCE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOURCE_ROOT)
  end function SOURCE_ROOT_IS_EXACT


  logical function SOURCE_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SOURCE_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOURCE_AUTHORITY)
  end function SOURCE_AUTHORITY_IS_EXACT
end module SPOR64_B2R
