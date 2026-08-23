module SPOR64_B2J
  ! Projects a CLOSED archive, or a proposal, into the
  ! PROJECTED archive of the next epoch.
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_B2H, only : SPOR64_B2H_ADMISSION_FAILED, &
      SPOR64_B2H_PROJECTED_COMMITTED, SPOR64_B2H_PROJECT, &
      SPOR64_B2H_RECONSTRUCT
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, RECORD_MATCHES
  use SPOR64_SCHEMA, only : SCHEMA_ARCHIVE_ROOT_AUTHORITY, &
      SCHEMA_CLOSED_ARCHIVE_ROOT, SCHEMA_PROJECTED_AUTHORITY, &
      SCHEMA_PROJECTED_PLANE_ROOT, SCHEMA_PROJECTED_PLANE_ROOT_L64, &
      SCHEMA_SOLVED_AUTHORITY
  implicit none
  private

  integer, parameter, public :: SPOR64_B2J_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2J_ARCHIVE_PROJECTED = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NSNAP = 3
  integer, parameter :: NIFIS = 32
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2J_PROJECT_ARCHIVE, SPOR64_B2J_PROJECT_PROPOSAL

contains

  subroutine SPOR64_B2J_PROJECT_ARCHIVE(iparchiveout,ipax,ipaxtrack, &
      iparchive,status)
    type(c_ptr), intent(in) :: iparchiveout, ipax, ipaxtrack, iparchive
    integer, intent(out) :: status

    integer :: axial_state(NSTATE), axial_track_state(NSTATE)
    integer :: state_dims(4), rank(NGRP), offset(NGRP+1)
    integer :: basis_offset(NGRP+1), plane_track_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: system_state(NSTATE)
    integer :: archive_planes, root_planes, axial_epoch, archive_epoch
    integer :: plane_epoch, projected_epoch, ncoef, total_basis
    integer :: nreg, nsurf, nunkno, nmat
    integer :: ig, ip, ir, a, nmode, b2h_status, allocation_status
    integer :: system_snapshot
    integer, allocatable :: plane_key(:), anis_key(:), seed_key(:)
    integer(int32) :: found32, expected32
    integer(int64) :: found64, expected64
    real(real32) :: keff32
    real(real64) :: axkeff64
    integer :: k64len, k64typ
    real(real32) :: plane_leakage32(NGRP), system_leakage32(NGRP)
    real(real32), allocatable :: area32(:), plane_volume32(:)
    real(real64) :: rho64, root_rho64, plane_rho64, iter_keff64
    real(real32), allocatable :: basis32(:), basis_slice32(:,:)
    real(real64), allocatable :: coordinates64(:), leakage64(:)
    real(real64), allocatable :: projected_region64(:,:,:)
    real(real64) :: coordinate_slice64(NSNAP)
    logical :: reconstruction_ok
    logical, allocatable :: seen_unknown(:)
    character(len=12) :: lifecycle_state, signature
    character(len=12), parameter :: stage_name(NSNAP) = &
        ['B2J-STAGE-1','B2J-STAGE-2','B2J-STAGE-3']
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: output_tracks, output_libraries, output_fluxes
    type(c_ptr) :: input_track(NSNAP), input_library(NSNAP)
    type(c_ptr) :: input_system(NSNAP), input_flux(NSNAP)
    type(c_ptr) :: plane_authority, root_authority, output_authority
    type(c_ptr) :: library_macro, macro_groups, system_groups
    type(c_ptr) :: output_item
    type(c_ptr) :: staged_flux(NSNAP)

    status = SPOR64_B2J_ADMISSION_FAILED
    staged_flux = c_null_ptr

    ! The only caller-supplied target is a fresh archive.  AX, axial track,
    ! and CLOSED archive are immutable members of one preceding epoch.
    if (.not. c_associated(iparchiveout)) return
    if (.not. c_associated(ipax)) return
    if (.not. c_associated(ipaxtrack)) return
    if (.not. c_associated(iparchive)) return
    if (c_associated(iparchiveout,ipax)) return
    if (c_associated(iparchiveout,ipaxtrack)) return
    if (c_associated(iparchiveout,iparchive)) return
    if (c_associated(ipax,ipaxtrack)) return
    if (c_associated(ipax,iparchive)) return
    if (c_associated(ipaxtrack,iparchive)) return
    if (.not. EMPTY_ROOT(iparchiveout)) return

    ! The three immutable radial TRACK objects are the sole geometry
    ! authority for this transition.
    if (.not. ARCHIVE_TRACK_GEOMETRY_IS_VALID(iparchive,nreg,nunkno, &
        nmat,nsurf)) return

    ! Admit the fixed Synthesis-POD representation from the sealed AX root.
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipax,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipax,'STATE-VECTOR',axial_state)
    if (axial_state(1) /= NGRP .or. axial_state(2) <= 0) return
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SPOT-X-STATE',3,12, &
        'CLOSED')) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-EPOCH',1,1)) return
    call LCMGET(ipax,'SPOT-X-EPOCH',axial_epoch)
    if (axial_epoch < 0 .or. axial_epoch == huge(axial_epoch)) return
    projected_epoch = axial_epoch + 1
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-DIMS',4,1)) return
    call LCMGET(ipax,'SPOT-X-DIMS',state_dims)
    if (any(state_dims(1:3) /= [1,NGRP,NSNAP])) return
    if (state_dims(4) <= 0) return
    ncoef = state_dims(4)
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-FIXB',1,1)) return
    call LCMGET(ipax,'SPOT-X-FIXB',ir)
    if (ir /= 1) return
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SPOT-X-NID',3,12, &
        'NUFISS-UNIT')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SPOT-X-BTYP',3,12, &
        'POD-FIXED')) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-RANK',NGRP,1)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-OFF',NGRP+1,1)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-BOFF',NGRP+1,1)) return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    call LCMGET(ipax,'SPOT-X-OFF',offset)
    call LCMGET(ipax,'SPOT-X-BOFF',basis_offset)
    if (any(rank < 1) .or. any(rank > NSNAP)) return
    if (offset(1) /= 0 .or. basis_offset(1) /= 0) return
    if (offset(NGRP+1) /= ncoef) return
    do ig = 1, NGRP
      if (int(offset(ig+1),int64)-int(offset(ig),int64) /= &
          int(NSNAP,int64)*int(rank(ig),int64)) return
      if (int(basis_offset(ig+1),int64)- &
          int(basis_offset(ig),int64) /= &
          int(nreg,int64)*int(rank(ig),int64)) return
    end do
    total_basis = basis_offset(NGRP+1)
    if (total_basis <= 0) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-BASIS',total_basis,2)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-A',ncoef,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-RHO',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-L',NGRP*NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'K-EFFECTIVE',1,2)) return
    allocate(basis32(total_basis),coordinates64(ncoef), &
        leakage64(NGRP*NSNAP), &
        projected_region64(nreg,NGRP,NSNAP), &
        plane_key(nreg),anis_key(nreg),seed_key(nreg), &
        area32(nreg),plane_volume32(nreg), &
        basis_slice32(nreg,NSNAP),seen_unknown(nunkno), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(ipax,'SPOT-X-BASIS',basis32)
    call LCMGET(ipax,'SPOT-X-A',coordinates64)
    call LCMGET(ipax,'SPOT-X-RHO',rho64)
    call LCMGET(ipax,'SPOT-X-L',leakage64)
    call LCMGET(ipax,'K-EFFECTIVE',keff32)
    if (.not. all(ieee_is_finite(basis32))) return
    if (.not. all(ieee_is_finite(coordinates64))) return
    if (.not. all(ieee_is_finite(leakage64))) return
    if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64) return
    if (.not. ieee_is_finite(keff32) .or. keff32 <= +0.0_real32) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/real(keff32,real64),0_int64)
    if (found64 /= expected64) then
      call LCMLEN(ipax,'SPOT-X-KEFF',k64len,k64typ)
      if (k64len /= 1 .or. k64typ /= 4) return
      call LCMGET(ipax,'SPOT-X-KEFF',axkeff64)
      if (transfer(rho64,0_int64) /= &
          transfer(1.0_real64/axkeff64,0_int64)) return
      if (transfer(real(axkeff64,real32),0_int32) /= &
          transfer(keff32,0_int32)) return
    end if

    ! AREA2D fixes the row ordering used by every stored POD basis.
    if (.not. CHARACTER_RECORD_MATCHES(ipaxtrack,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipaxtrack,'TRACK-TYPE',3,12, &
        'SPOT')) return
    if (.not. RECORD_MATCHES(ipaxtrack,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipaxtrack,'STATE-VECTOR',axial_track_state)
    if (axial_track_state(6) /= nreg) return
    if (axial_track_state(7) <= 0) return
    if (axial_track_state(8) /= NSNAP) return
    if (int(axial_track_state(1),int64) /= &
        int(nreg,int64)*int(axial_track_state(7),int64)) return
    if (axial_track_state(11) < 0) return
    if (int(axial_track_state(12),int64) /= &
        int(nreg,int64)*(int(axial_track_state(7),int64)+1_int64)) return
    if (int(axial_track_state(11),int64)+ &
        int(axial_track_state(12),int64) > &
        int(axial_track_state(2),int64)) return
    if (axial_state(2) /= axial_track_state(2)) return
    if (.not. RECORD_MATCHES(ipaxtrack,'AREA2D',nreg,2)) return
    call LCMGET(ipaxtrack,'AREA2D',area32)
    if (.not. all(ieee_is_finite(area32))) return
    if (any(area32 <= +0.0_real32)) return

    ! The archive root and AX root must describe exactly the same CLOSED
    ! epoch and RHO.  This is the archive-level provenance missing in B2h.
    if (.not. CHARACTER_RECORD_MATCHES(iparchive,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. CLOSED_ARCHIVE_ROOT_IS_EXACT(iparchive)) return
    if (.not. RECORD_MATCHES(iparchive,'LISTDIM',1,1)) return
    call LCMGET(iparchive,'LISTDIM',archive_planes)
    if (archive_planes /= NSNAP) return
    if (.not. RECORD_MATCHES(iparchive,'SPOT-ITER-K',1,4)) return
    call LCMGET(iparchive,'SPOT-ITER-K',iter_keff64)
    if (.not. ieee_is_finite(iter_keff64) .or. &
        iter_keff64 <= +0.0_real64) return
    found64 = transfer(iter_keff64,0_int64)
    expected64 = transfer(real(keff32,real64),0_int64)
    if (found64 /= expected64) then
      if (transfer(real(iter_keff64,real32),0_int32) /= &
          transfer(keff32,0_int32)) return
    end if
    if (.not. RECORD_MATCHES(iparchive,'SPOT-R64',-1,0)) return
    root_authority = LCMGID(iparchive,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. CLOSED_ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'CLOSED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',root_rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',archive_epoch)
    if (root_planes /= NSNAP .or. archive_epoch /= axial_epoch) return
    if (.not. ieee_is_finite(root_rho64)) return
    if (transfer(root_rho64,0_int64) /= transfer(rho64,0_int64)) return

    if (.not. RECORD_MATCHES(iparchive,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'SYSTEM',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'FLUX',NSNAP,10)) return
    tracks = LCMGID(iparchive,'TRACK')
    libraries = LCMGID(iparchive,'MICROLIB2')
    systems = LCMGID(iparchive,'SYSTEM')
    fluxes = LCMGID(iparchive,'FLUX')
    if (.not. c_associated(tracks)) return
    if (.not. c_associated(libraries)) return
    if (.not. c_associated(systems)) return
    if (.not. c_associated(fluxes)) return

    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(systems,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
      input_track(ip) = LCMGIL(tracks,ip)
      input_library(ip) = LCMGIL(libraries,ip)
      input_system(ip) = LCMGIL(systems,ip)
      input_flux(ip) = LCMGIL(fluxes,ip)
      if (.not. c_associated(input_track(ip))) return
      if (.not. c_associated(input_library(ip))) return
      if (.not. c_associated(input_system(ip))) return
      if (.not. c_associated(input_flux(ip))) return

      ! Admit the same-index B2i tuple.  SYSTEM is checked here only as a
      ! provenance witness.  It contains lagged leakage and is intentionally
      ! absent from the PROJECTED output; a later lifecycle gate must rebuild
      ! it from the projected leakage before continuation is admissible.
      if (.not. CHARACTER_RECORD_MATCHES(input_library(ip),'SIGNATURE', &
          3,12,'L_LIBRARY')) return
      if (.not. RECORD_MATCHES(input_library(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_library(ip),'STATE-VECTOR',library_state)
      if (library_state(1) /= nmat .or. library_state(2) <= 0) return
      if (library_state(3) /= NGRP .or. library_state(4) /= 3) return
      if (.not. RECORD_MATCHES(input_library(ip),'MACROLIB',-1,0)) return
      library_macro = LCMGID(input_library(ip),'MACROLIB')
      if (.not. c_associated(library_macro)) return
      if (.not. CHARACTER_RECORD_MATCHES(library_macro,'SIGNATURE', &
          3,12,'L_MACROLIB')) return
      if (.not. RECORD_MATCHES(library_macro,'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(library_macro,'STATE-VECTOR',macro_state)
      if (macro_state(1) /= NGRP .or. macro_state(2) /= nmat) return
      if (macro_state(3) /= 3 .or. macro_state(4) /= NIFIS) return
      if (macro_state(6) /= 2 .or. macro_state(13) /= 0) return
      if (.not. RECORD_MATCHES(library_macro,'GROUP',NGRP,10)) return
      macro_groups = LCMGID(library_macro,'GROUP')
      if (.not. c_associated(macro_groups)) return
      do ig = 1, NGRP
        if (.not. LIST_ITEM_IS_DIRECTORY(macro_groups,ig)) return
      end do

      if (.not. CHARACTER_RECORD_MATCHES(input_system(ip),'SIGNATURE', &
          3,12,'L_PIJ')) return
      if (.not. RECORD_MATCHES(input_system(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_system(ip),'STATE-VECTOR',system_state)
      if (any(system_state(1:14) /= &
          [1,1,1,0,1,1,4,NGRP,nunkno,nmat,1,0,0,0])) return
      if (any(system_state(15:NSTATE) /= 0)) return
      if (.not. RECORD_MATCHES(input_system(ip),'GROUP',NGRP,10)) return
      system_groups = LCMGID(input_system(ip),'GROUP')
      if (.not. c_associated(system_groups)) return
      do ig = 1, NGRP
        if (.not. LIST_ITEM_IS_DIRECTORY(system_groups,ig)) return
      end do
      if (.not. CHARACTER_RECORD_MATCHES(input_system(ip),'LINK.MACRO', &
          3,12,'MACRO0')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_system(ip),'LINK.TRACK', &
          3,12,'TRACK')) return
      if (.not. RECORD_MATCHES(input_system(ip),'SPOT-LEAK1D', &
          NGRP,2)) return
      call LCMGET(input_system(ip),'SPOT-LEAK1D',system_leakage32)
      if (.not. all(ieee_is_finite(system_leakage32))) return
      if (.not. RECORD_MATCHES(input_system(ip),'SPOT-L1-SNAP',1,1)) &
          return
      call LCMGET(input_system(ip),'SPOT-L1-SNAP',system_snapshot)
      if (system_snapshot /= ip) return

      if (.not. RECORD_MATCHES(input_track(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_track(ip),'STATE-VECTOR',plane_track_state)
      if (plane_track_state(1) /= nreg .or. &
          plane_track_state(2) /= nunkno) return
      if (plane_track_state(4) /= nmat .or. &
          plane_track_state(5) /= nsurf) return
      if (plane_track_state(6) /= 1 .or. &
          plane_track_state(9) /= 0) return
      if (plane_track_state(14) /= 4) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'TRACK-TYPE', &
          3,12,'MCCG')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'LINK.FTRACK', &
          3,12,'TRACK_f')) return
      if (.not. RECORD_MATCHES(input_track(ip),'VOLUME',nreg,2)) return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX',nreg,1)) return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX$ANIS',nreg,1)) &
          return
      call LCMGET(input_track(ip),'VOLUME',plane_volume32)
      call LCMGET(input_track(ip),'KEYFLX',plane_key)
      call LCMGET(input_track(ip),'KEYFLX$ANIS',anis_key)
      if (.not. all(ieee_is_finite(plane_volume32))) return
      seen_unknown = .false.
      do ir = 1, nreg
        found32 = transfer(plane_volume32(ir),0_int32)
        expected32 = transfer(area32(ir),0_int32)
        if (found32 /= expected32) return
        if (plane_key(ir) /= anis_key(ir)) return
        if (anis_key(ir) < 1 .or. anis_key(ir) > nunkno) return
        if (seen_unknown(anis_key(ir))) return
        seen_unknown(anis_key(ir)) = .true.
      end do
      if (.not. RECORD_MATCHES(input_flux(ip),'KEYFLX',nreg,1)) return
      call LCMGET(input_flux(ip),'KEYFLX',seed_key)
      if (any(seed_key /= anis_key)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'SPOT-R64',-1,0)) return
      plane_authority = LCMGID(input_flux(ip),'SPOT-R64')
      if (.not. c_associated(plane_authority)) return
      if (.not. SOLVED_AUTHORITY_IS_EXACT(plane_authority)) return
      if (.not. RECORD_MATCHES(plane_authority,'RHO',1,4)) return
      if (.not. CHARACTER_RECORD_MATCHES(plane_authority,'STATE',3,12, &
          'SOLVED')) return
      if (.not. RECORD_MATCHES(plane_authority,'EPOCH',1,1)) return
      call LCMGET(plane_authority,'RHO',plane_rho64)
      call LCMGET(plane_authority,'EPOCH',plane_epoch)
      if (.not. ieee_is_finite(plane_rho64)) return
      if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return
      if (plane_epoch /= axial_epoch) return
      if (.not. RECORD_MATCHES(input_flux(ip),'SPOT-LEAK1D', &
          NGRP,2)) return
      call LCMGET(input_flux(ip),'SPOT-LEAK1D',plane_leakage32)
      do ig = 1, NGRP
        if (.not. ieee_is_finite(plane_leakage32(ig))) return
        found64 = transfer(leakage64((ip-1)*NGRP+ig),0_int64)
        expected64 = transfer(real(plane_leakage32(ig),real64),0_int64)
        if (found64 /= expected64) then
          found32 = transfer(real(leakage64((ip-1)*NGRP+ig), &
              real32),0_int32)
          expected32 = transfer(plane_leakage32(ig),0_int32)
          if (found32 /= expected32) return
        end if
      end do
    end do

    ! Evaluate every B_g*a_(g,p) before opening any output record.  The
    ! explicit group/plane/mode order is the numerical definition inherited
    ! from SPOSTATE and B2h; no fit threshold or empirical control appears.
    do ig = 1, NGRP
      nmode = rank(ig)
      basis_slice32 = +0.0_real32
      coordinate_slice64 = +0.0_real64
      do a = 1, nmode
        basis_slice32(:,a) = basis32( &
            basis_offset(ig)+(a-1)*nreg+1: &
            basis_offset(ig)+a*nreg)
      end do
      do ip = 1, NSNAP
        coordinate_slice64(1:nmode) = coordinates64( &
            offset(ig)+(ip-1)*nmode+1:offset(ig)+ip*nmode)
        call SPOR64_B2H_RECONSTRUCT(basis_slice32(:,1:nmode), &
            coordinate_slice64(1:nmode), &
            projected_region64(:,ig,ip),reconstruction_ok)
        if (.not. reconstruction_ok) return
      end do
    end do

    ! B2h stages each fresh plane privately.  A rejected plane is destroyed
    ! and the caller's archive remains empty.  Only three successful staged
    ! PROJECTED objects permit the archive commit below.
    do ip = 1, NSNAP
      call LCMOP(staged_flux(ip),stage_name(ip),0,1,0)
      call SPOR64_B2H_PROJECT(staged_flux(ip),input_flux(ip), &
          input_track(ip),projected_region64(:,:,ip),rho64,b2h_status)
      if (b2h_status == SPOR64_B2H_ADMISSION_FAILED) then
        call CLOSE_STAGES(staged_flux)
        return
      end if
      if (b2h_status /= SPOR64_B2H_PROJECTED_COMMITTED) &
          call XABORT('SPOR64_B2J: UNKNOWN B2H STATUS.')
      if (.not. STAGED_PROJECTED_OBJECT_IS_COMMITTED(staged_flux(ip), &
          rho64,projected_epoch,nunkno, &
          leakage64((ip-1)*NGRP+1:ip*NGRP))) then
        call CLOSE_STAGES(staged_flux)
        return
      end if
    end do

    ! This repeat is immediately before the first caller-visible mutation.
    if (.not. EMPTY_ROOT(iparchiveout)) then
      call CLOSE_STAGES(staged_flux)
      return
    end if

    signature = 'L_ARCHIVE'
    call LCMPTC(iparchiveout,'SIGNATURE',12,signature)
    call LCMPUT(iparchiveout,'LISTDIM',1,1,archive_planes)
    call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)
    output_tracks = LCMLID(iparchiveout,'TRACK',NSNAP)
    output_libraries = LCMLID(iparchiveout,'MICROLIB2',NSNAP)
    output_fluxes = LCMLID(iparchiveout,'FLUX',NSNAP)
    if (.not. c_associated(output_tracks)) &
        call XABORT('SPOR64_B2J: OUTPUT TRACK LIST CREATION FAILED.')
    if (.not. c_associated(output_libraries)) &
        call XABORT('SPOR64_B2J: OUTPUT LIBRARY LIST CREATION FAILED.')
    if (.not. c_associated(output_fluxes)) &
        call XABORT('SPOR64_B2J: OUTPUT FLUX LIST CREATION FAILED.')
    do ip = 1, NSNAP
      output_item = LCMDIL(output_tracks,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2J: OUTPUT TRACK ITEM CREATION FAILED.')
      call LCMEQU(input_track(ip),output_item)
      output_item = LCMDIL(output_libraries,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2J: OUTPUT LIBRARY ITEM CREATION FAILED.')
      call LCMEQU(input_library(ip),output_item)
      output_item = LCMDIL(output_fluxes,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2J: OUTPUT FLUX ITEM CREATION FAILED.')
      call LCMEQU(staged_flux(ip),output_item)
    end do

    ! The old SYSTEM is not propagated: its leakage belongs to the lagged
    ! radial solve.  Release private stages before declaring the output
    ! committed.  B2j itself does not build a replacement SYSTEM.
    call CLOSE_STAGES(staged_flux)

    ! Archive EPOCH is the final caller-visible LCM mutation and the sole
    ! archive-wide commit.  An object without it must be discarded.
    output_authority = LCMDID(iparchiveout,'SPOT-R64')
    if (.not. c_associated(output_authority)) &
        call XABORT('SPOR64_B2J: ROOT AUTHORITY CREATION FAILED.')
    lifecycle_state = 'PROJECTED'
    call LCMPUT(output_authority,'RHO',1,4,rho64)
    call LCMPUT(output_authority,'NPLANE',1,1,archive_planes)
    call LCMPTC(output_authority,'STATE',12,lifecycle_state)
    call LCMPUT(output_authority,'EPOCH',1,1,projected_epoch)
    status = SPOR64_B2J_ARCHIVE_PROJECTED
  end subroutine SPOR64_B2J_PROJECT_ARCHIVE


  subroutine SPOR64_B2J_PROJECT_PROPOSAL(iparchiveout,ipproposal, &
      ipaxtrack,iptemplate,status)
    type(c_ptr), intent(in) :: iparchiveout, ipproposal
    type(c_ptr), intent(in) :: ipaxtrack, iptemplate
    integer, intent(out) :: status

    integer :: ip, template_epoch, template_planes, plane_epoch
    integer :: rank(NGRP)
    integer(int64) :: found64, expected64
    real(real32) :: proposal_keff32, template_keff32
    real(real32) :: plane_leakage32(NGRP)
    real(real64) :: proposal_rho64, template_iter_keff64
    real(real64) :: template_rho64, plane_rho64
    real(real64) :: proposal_leakage64(NGRP*NSNAP)
    real(real64) :: proposal_iter_keff64
    character(len=12) :: lifecycle_state
    type(c_ptr) :: template_authority, template_fluxes
    type(c_ptr) :: template_plane, template_plane_authority
    type(c_ptr) :: staged_ax, staged_archive
    type(c_ptr) :: staged_authority, staged_fluxes
    type(c_ptr) :: staged_plane, staged_plane_authority
    integer :: projected_status

    status = SPOR64_B2J_ADMISSION_FAILED
    staged_ax = c_null_ptr
    staged_archive = c_null_ptr

    ! A proposal is a separate lifecycle boundary.  It is never admitted by
    ! weakening the CLOSED/e contract above, and none of its normalization
    ! records are written to a caller-owned root.
    if (.not. c_associated(iparchiveout)) return
    if (.not. c_associated(ipproposal)) return
    if (.not. c_associated(ipaxtrack)) return
    if (.not. c_associated(iptemplate)) return
    if (c_associated(iparchiveout,ipproposal)) return
    if (c_associated(iparchiveout,ipaxtrack)) return
    if (c_associated(iparchiveout,iptemplate)) return
    if (c_associated(ipproposal,ipaxtrack)) return
    if (c_associated(ipproposal,iptemplate)) return
    if (c_associated(ipaxtrack,iptemplate)) return
    if (.not. EMPTY_ROOT(iparchiveout)) return

    ! Accept only the published, fixed-rank AA(1) carrier selected for this
    ! branch.  Saved map defects and solver diagnostics belong to x4, not to
    ! the affine proposal, and therefore cannot cross this boundary.
    if (.not. CHARACTER_RECORD_MATCHES(ipproposal,'SPOT-X-STATE',3,12, &
        'PROPOSAL')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipproposal,'SPOT-X-CARR',3,12, &
        'X4-RAW-FLUX')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-R64')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-EPOCH')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-RRHO')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-RLEAK')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-DLEAK')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-RA')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-X-PERP')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-GBAL')) return
    if (.not. ABSENT_RECORD(ipproposal,'SPOT-GBAL-MA')) return
    if (.not. RECORD_MATCHES(ipproposal,'SPOT-X-RANK',NGRP,1)) return
    call LCMGET(ipproposal,'SPOT-X-RANK',rank)
    if (any(rank /= 2)) return
    if (.not. RECORD_MATCHES(ipproposal,'K-EFFECTIVE',1,2)) return
    if (.not. RECORD_MATCHES(ipproposal,'SPOT-X-RHO',1,4)) return
    if (.not. RECORD_MATCHES(ipproposal,'SPOT-X-L',NGRP*NSNAP,4)) return
    call LCMGET(ipproposal,'K-EFFECTIVE',proposal_keff32)
    call LCMGET(ipproposal,'SPOT-X-RHO',proposal_rho64)
    call LCMGET(ipproposal,'SPOT-X-L',proposal_leakage64)
    if (.not. ieee_is_finite(proposal_keff32) .or. &
        proposal_keff32 <= +0.0_real32) return
    if (.not. ieee_is_finite(proposal_rho64) .or. &
        proposal_rho64 <= +0.0_real64) return
    if (.not. all(ieee_is_finite(proposal_leakage64))) return
    found64 = transfer(proposal_rho64,0_int64)
    expected64 = transfer(1.0_real64/real(proposal_keff32,real64), &
        0_int64)
    if (found64 /= expected64) return
    ! The proposal's SPOT-X-L is the exact double-precision affine of
    ! its parents; the historical binary32 round-trip requirement is
    ! retired with the dp leakage channel (finiteness checked above).
    proposal_iter_keff64 = real(proposal_keff32,real64)

    ! The template supplies only the immutable plane structures and the
    ! lineage epoch.  Check its original CLOSED state before making the
    ! private copy, so normalization cannot conceal a malformed template.
    if (.not. CHARACTER_RECORD_MATCHES(iptemplate,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. CLOSED_ARCHIVE_ROOT_IS_EXACT(iptemplate)) return
    if (.not. RECORD_MATCHES(iptemplate,'LISTDIM',1,1)) return
    if (.not. RECORD_MATCHES(iptemplate,'SPOT-ITER-K',1,4)) return
    if (.not. RECORD_MATCHES(iptemplate,'SPOT-R64',-1,0)) return
    call LCMGET(iptemplate,'LISTDIM',template_planes)
    call LCMGET(iptemplate,'SPOT-ITER-K',template_iter_keff64)
    if (template_planes /= NSNAP) return
    if (.not. ieee_is_finite(template_iter_keff64) .or. &
        template_iter_keff64 <= +0.0_real64) return
    template_keff32 = real(template_iter_keff64,real32)
    template_authority = LCMGID(iptemplate,'SPOT-R64')
    if (.not. c_associated(template_authority)) return
    if (.not. CLOSED_ROOT_AUTHORITY_IS_EXACT(template_authority)) return
    if (.not. CHARACTER_RECORD_MATCHES(template_authority,'STATE',3,12, &
        'CLOSED')) return
    if (.not. RECORD_MATCHES(template_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(template_authority,'NPLANE',1,1)) return
    if (.not. RECORD_MATCHES(template_authority,'EPOCH',1,1)) return
    call LCMGET(template_authority,'RHO',template_rho64)
    call LCMGET(template_authority,'NPLANE',template_planes)
    call LCMGET(template_authority,'EPOCH',template_epoch)
    if (template_planes /= NSNAP) return
    ! A proposal branch exists only after at least one completed CONT epoch;
    ! epoch zero remains the one-time B2I/B2J bootstrap route.
    if (template_epoch <= 0 .or. template_epoch == huge(template_epoch)) &
      return
    if (.not. ieee_is_finite(template_rho64) .or. &
        template_rho64 <= +0.0_real64) return
    found64 = transfer(template_rho64,0_int64)
    expected64 = transfer(1.0_real64/real(template_keff32,real64), &
        0_int64)
    if (found64 /= expected64) then
      if (transfer(template_rho64,0_int64) /= &
          transfer(1.0_real64/template_iter_keff64,0_int64)) return
    end if
    if (.not. RECORD_MATCHES(iptemplate,'FLUX',NSNAP,10)) return
    template_fluxes = LCMGID(iptemplate,'FLUX')
    if (.not. c_associated(template_fluxes)) return
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(template_fluxes,ip)) return
      template_plane = LCMGIL(template_fluxes,ip)
      if (.not. c_associated(template_plane)) return
      if (.not. RECORD_MATCHES(template_plane,'SPOT-R64',-1,0)) return
      template_plane_authority = LCMGID(template_plane,'SPOT-R64')
      if (.not. c_associated(template_plane_authority)) return
      if (.not. SOLVED_AUTHORITY_IS_EXACT(template_plane_authority)) &
        return
      if (.not. CHARACTER_RECORD_MATCHES(template_plane_authority, &
          'STATE',3,12,'SOLVED')) return
      if (.not. RECORD_MATCHES(template_plane_authority,'RHO',1,4)) &
        return
      if (.not. RECORD_MATCHES(template_plane_authority,'EPOCH',1,1)) &
        return
      call LCMGET(template_plane_authority,'RHO',plane_rho64)
      call LCMGET(template_plane_authority,'EPOCH',plane_epoch)
      if (plane_epoch /= template_epoch) return
      if (.not. ieee_is_finite(plane_rho64)) return
      if (transfer(plane_rho64,0_int64) /= &
          transfer(template_rho64,0_int64)) return
      if (.not. RECORD_MATCHES(template_plane,'SPOT-LEAK1D',NGRP,2)) &
        return
      call LCMGET(template_plane,'SPOT-LEAK1D',plane_leakage32)
      if (.not. all(ieee_is_finite(plane_leakage32))) return
    end do

    ! Normalize only two private in-memory copies to the already proven B2J
    ! CLOSED/e contract.  The original proposal and template remain read-only,
    ! and no normalized CLOSED object is ever returned to the caller.
    call LCMOP(staged_ax,'B2J-PROP-AX',0,1,0)
    call LCMOP(staged_archive,'B2J-PROP-AR',0,1,0)
    call LCMEQU(ipproposal,staged_ax)
    call LCMEQU(iptemplate,staged_archive)

    call LCMDEL(staged_ax,'SPOT-X-CARR')
    lifecycle_state = 'CLOSED'
    call LCMPTC(staged_ax,'SPOT-X-STATE',12,lifecycle_state)
    call LCMPUT(staged_ax,'SPOT-X-EPOCH',1,1,template_epoch)
    call LCMPUT(staged_archive,'SPOT-ITER-K',1,4, &
        proposal_iter_keff64)
    staged_authority = LCMGID(staged_archive,'SPOT-R64')
    if (.not. c_associated(staged_authority)) &
      call XABORT('SPOR64_B2J: PRIVATE PROPOSAL ROOT AUTHORITY MISSING.')
    call LCMPUT(staged_authority,'RHO',1,4,proposal_rho64)
    staged_fluxes = LCMGID(staged_archive,'FLUX')
    if (.not. c_associated(staged_fluxes)) &
      call XABORT('SPOR64_B2J: PRIVATE PROPOSAL FLUX LIST MISSING.')
    do ip = 1, NSNAP
      staged_plane = LCMGIL(staged_fluxes,ip)
      if (.not. c_associated(staged_plane)) &
        call XABORT('SPOR64_B2J: PRIVATE PROPOSAL PLANE MISSING.')
      staged_plane_authority = LCMGID(staged_plane,'SPOT-R64')
      if (.not. c_associated(staged_plane_authority)) &
        call XABORT('SPOR64_B2J: PRIVATE PROPOSAL AUTHORITY MISSING.')
      call LCMPUT(staged_plane_authority,'RHO',1,4,proposal_rho64)
      plane_leakage32 = real(proposal_leakage64( &
          (ip-1)*NGRP+1:ip*NGRP),real32)
      call LCMPUT(staged_plane,'SPOT-LEAK1D',NGRP,2, &
          plane_leakage32)
      ! The REAL64 leakage authority; SPOT-LEAK1D above is its exact
      ! bitwise demote mirror by construction.
      call LCMPUT(staged_plane,'LEAK1D64',NGRP,4, &
          proposal_leakage64((ip-1)*NGRP+1:ip*NGRP))
    end do

    projected_status = SPOR64_B2J_ADMISSION_FAILED
    call SPOR64_B2J_PROJECT_ARCHIVE(iparchiveout,staged_ax,ipaxtrack, &
        staged_archive,projected_status)
    call LCMCL(staged_archive,2)
    staged_archive = c_null_ptr
    call LCMCL(staged_ax,2)
    staged_ax = c_null_ptr
    if (projected_status /= SPOR64_B2J_ARCHIVE_PROJECTED) return
    status = SPOR64_B2J_ARCHIVE_PROJECTED
  end subroutine SPOR64_B2J_PROJECT_PROPOSAL


  logical function ARCHIVE_TRACK_GEOMETRY_IS_VALID(iparchive,nreg, &
      nunkno,nmat,nsurf)
    type(c_ptr), intent(in) :: iparchive
    integer, intent(out) :: nreg, nunkno, nmat, nsurf

    integer :: state(NSTATE), ip
    type(c_ptr) :: tracks, track

    ARCHIVE_TRACK_GEOMETRY_IS_VALID = .false.
    nreg = 0
    nunkno = 0
    nmat = 0
    nsurf = 0
    if (.not. RECORD_MATCHES(iparchive,'TRACK',NSNAP,10)) return
    tracks = LCMGID(iparchive,'TRACK')
    if (.not. c_associated(tracks)) return
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      track = LCMGIL(tracks,ip)
      if (.not. c_associated(track)) return
      if (.not. CHARACTER_RECORD_MATCHES(track,'SIGNATURE',3,12, &
          'L_TRACK')) return
      if (.not. RECORD_MATCHES(track,'STATE-VECTOR',NSTATE,1)) return
      call LCMGET(track,'STATE-VECTOR',state)
      if (state(1) <= 0 .or. state(2) <= 0 .or. state(4) <= 0 .or. &
          state(5) <= 0) return
      if (int(state(2),int64) /= &
          int(state(1),int64)+int(state(5),int64)) return
      if (ip == 1) then
        nreg = state(1)
        nunkno = state(2)
        nmat = state(4)
        nsurf = state(5)
      else
        if (state(1) /= nreg .or. state(2) /= nunkno .or. &
            state(4) /= nmat .or. state(5) /= nsurf) return
      end if
      if (.not. RECORD_MATCHES(track,'V$MCCG',state(2),2)) return
      if (.not. RECORD_MATCHES(track,'NZON$MCCG',state(2),1)) return
      if (.not. RECORD_MATCHES(track,'KEYCUR$MCCG',state(5),1)) return
      if (.not. RECORD_MATCHES(track,'VOLUME',state(1),2)) return
      if (.not. RECORD_MATCHES(track,'KEYFLX',state(1),1)) return
      if (.not. RECORD_MATCHES(track,'KEYFLX$ANIS',state(1),1)) return
    end do
    ARCHIVE_TRACK_GEOMETRY_IS_VALID = .true.
  end function ARCHIVE_TRACK_GEOMETRY_IS_VALID


  subroutine CLOSE_STAGES(staged_flux)
    type(c_ptr), intent(inout) :: staged_flux(:)
    integer :: ip

    do ip = 1, size(staged_flux)
      if (c_associated(staged_flux(ip))) call LCMCL(staged_flux(ip),2)
      staged_flux(ip) = c_null_ptr
    end do
  end subroutine CLOSE_STAGES
  logical function CLOSED_ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CLOSED_ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_ARCHIVE_ROOT_AUTHORITY)
  end function CLOSED_ROOT_AUTHORITY_IS_EXACT


  logical function CLOSED_ARCHIVE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    CLOSED_ARCHIVE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_CLOSED_ARCHIVE_ROOT)
  end function CLOSED_ARCHIVE_ROOT_IS_EXACT


  logical function SOLVED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    SOLVED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SOLVED_AUTHORITY)
  end function SOLVED_AUTHORITY_IS_EXACT


  logical function PROJECTED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    PROJECTED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_AUTHORITY)
  end function PROJECTED_AUTHORITY_IS_EXACT


  logical function PROJECTED_PLANE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    logical :: l64_exact, legacy_exact

    l64_exact = EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_PLANE_ROOT_L64)
    legacy_exact = EXACT_INVENTORY(iplist,SCHEMA_PROJECTED_PLANE_ROOT)
    PROJECTED_PLANE_ROOT_IS_EXACT = l64_exact .or. legacy_exact
  end function PROJECTED_PLANE_ROOT_IS_EXACT
  logical function STAGED_PROJECTED_OBJECT_IS_COMMITTED(iplist,rho,epoch, &
      nunkno,expected_leakage)
    type(c_ptr), intent(in) :: iplist
    real(real64), intent(in) :: rho
    integer, intent(in) :: epoch, nunkno
    real(real64), intent(in) :: expected_leakage(:)
    type(c_ptr) :: authority, authority_flux, mirror_flux
    real(real64) :: found_rho
    real(real32) :: found_leakage(NGRP)
    real(real64), allocatable :: authority_flux64(:)
    real(real32), allocatable :: mirror_flux32(:)
    integer(int32) :: found32, expected32
    integer :: found_epoch, ig, iu, ilong, itylcm, allocation_status

    STAGED_PROJECTED_OBJECT_IS_COMMITTED = .false.
    if (nunkno <= 0) return
    allocate(authority_flux64(nunkno),mirror_flux32(nunkno), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    if (.not. PROJECTED_PLANE_ROOT_IS_EXACT(iplist)) return
    if (.not. RECORD_MATCHES(iplist,'SPOT-R64',-1,0)) return
    authority = LCMGID(iplist,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. PROJECTED_AUTHORITY_IS_EXACT(authority)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(iplist,'FLUX',NGRP,10)) return
    if (size(expected_leakage) /= NGRP) return
    if (.not. RECORD_MATCHES(iplist,'SPOT-LEAK1D',NGRP,2)) return
    authority_flux = LCMGID(authority,'FLUX')
    mirror_flux = LCMGID(iplist,'FLUX')
    if (.not. c_associated(authority_flux)) return
    if (.not. c_associated(mirror_flux)) return
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'EPOCH',found_epoch)
    call LCMGET(iplist,'SPOT-LEAK1D',found_leakage)
    if (transfer(found_rho,0_int64) /= transfer(rho,0_int64)) return
    if (found_epoch /= epoch) return
    do ig = 1, NGRP
      call LCMLEL(authority_flux,ig,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 4) return
      call LCMLEL(mirror_flux,ig,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 2) return
      call LCMGDL(authority_flux,ig,authority_flux64)
      call LCMGDL(mirror_flux,ig,mirror_flux32)
      if (.not. all(ieee_is_finite(authority_flux64))) return
      if (.not. all(ieee_is_finite(mirror_flux32))) return
      if (any(abs(authority_flux64) > REAL32_MAX64)) return
      do iu = 1, nunkno
        found32 = transfer(mirror_flux32(iu),0_int32)
        expected32 = transfer(real(authority_flux64(iu),real32),0_int32)
        if (found32 /= expected32) return
      end do
      if (.not. ieee_is_finite(found_leakage(ig))) return
      if (transfer(real(found_leakage(ig),real64),0_int64) /= &
          transfer(expected_leakage(ig),0_int64)) then
        if (transfer(found_leakage(ig),0_int32) /= &
            transfer(real(expected_leakage(ig),real32),0_int32)) return
      end if
    end do
    STAGED_PROJECTED_OBJECT_IS_COMMITTED = .true.
  end function STAGED_PROJECTED_OBJECT_IS_COMMITTED

end module SPOR64_B2J
