module SPOR64_B2I
  ! The exactly-once bootstrap seal that starts a chain.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_MEMORY_ROOT, LIST_ITEM_IS_DIRECTORY, RECORD_MATCHES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2I_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2I_BOOTSTRAP_COMMITTED = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NSNAP = 3
  integer, parameter :: NUNKNO = 14
  integer, parameter :: NMAT = 8
  integer, parameter :: NIFIS = 32
  integer, parameter :: BOOTSTRAP_EPOCH = 0
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2I_SEAL_BOOTSTRAP

contains

  subroutine SPOR64_B2I_SEAL_BOOTSTRAP(ipaxout,iparchiveout,ipax, &
      ipaxtrack,iparchive,status)
    type(c_ptr), intent(in) :: ipaxout, iparchiveout
    type(c_ptr), intent(in) :: ipax, ipaxtrack, iparchive
    integer, intent(out) :: status

    integer :: axial_state(NSTATE), axial_track_state(NSTATE)
    integer :: plane_state(NSTATE), plane_track_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: system_state(NSTATE)
    integer :: state_dims(4), plane_key(NREG), anis_key(NREG)
    integer :: seed_key(NREG), imerge(NMAT)
    integer :: archive_planes, system_snapshot, fixb, ncoef
    integer :: total_basis, total_gram
    integer :: nfloor, ig, ip, ir, iu, a, b, nmode
    integer :: index_a, index_b, index_g, ilong, itylcm
    integer :: allocation_status
    integer, allocatable :: rank(:), offset(:), gram_offset(:)
    integer, allocatable :: basis_offset(:), mat1d(:)
    integer(int32) :: found32, expected32
    integer(int64) :: found64, expected64
    logical :: seen_unknown(NUNKNO)
    real(real32) :: keff32
    real(real32) :: eps_converge(5), area32(NREG), volume32(NREG)
    real(real32) :: plane_leak32(NGRP)
    real(real32) :: system_leak32(NGRP)
    real(real32) :: mirror_flux32(NUNKNO), mirror_source32(NUNKNO)
    real(real32), allocatable :: dz32(:), basis32(:)
    real(real64) :: rho64, norm64, gram_error64, gram_error_check64
    real(real64) :: iter_keff64
    real(real64) :: weight_sum, gram_value
    real(real64) :: authority_flux64(NUNKNO), authority_source64(NUNKNO)
    real(real64), allocatable :: coordinates64(:), gram64(:)
    real(real64), allocatable :: leakage64(:), height64(:)
    real(real64), allocatable :: offspace64(:)
    real(real64), allocatable :: height_check64(:)
    character(len=12) :: lifecycle_state, signature
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes
    type(c_ptr) :: input_track(NSNAP), input_library(NSNAP)
    type(c_ptr) :: input_system(NSNAP), input_flux(NSNAP)
    type(c_ptr) :: plane_authority(NSNAP)
    type(c_ptr) :: authority_flux, authority_source
    type(c_ptr) :: mirror_flux, mirror_source
    type(c_ptr) :: library_macro, macro_groups, system_groups
    type(c_ptr) :: output_item, output_authority

    status = SPOR64_B2I_ADMISSION_FAILED

    ! This is an exactly-once bootstrap seal.  It accepts no loose RHO,
    ! basis, epoch, or plane pointer: every value is recovered from the two
    ! input roots and their same-index children.
    if (.not. c_associated(ipaxout)) return
    if (.not. c_associated(iparchiveout)) return
    if (.not. c_associated(ipax)) return
    if (.not. c_associated(ipaxtrack)) return
    if (.not. c_associated(iparchive)) return
    if (c_associated(ipaxout,iparchiveout)) return
    if (c_associated(ipaxout,ipax)) return
    if (c_associated(ipaxout,ipaxtrack)) return
    if (c_associated(ipaxout,iparchive)) return
    if (c_associated(iparchiveout,ipax)) return
    if (c_associated(iparchiveout,ipaxtrack)) return
    if (c_associated(iparchiveout,iparchive)) return
    if (c_associated(ipax,ipaxtrack)) return
    if (c_associated(ipax,iparchive)) return
    if (c_associated(ipaxtrack,iparchive)) return
    if (.not. EMPTY_MEMORY_ROOT(ipaxout)) return
    if (.not. EMPTY_MEMORY_ROOT(iparchiveout)) return

    ! Canonical B/A/RHO/L are admitted only from one SPOSTATE-owned AX root.
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipax,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipax,'STATE-VECTOR',axial_state)
    if (axial_state(1) /= NGRP .or. axial_state(2) <= 0) return
    if (.not. ABSENT_RECORD(ipax,'SPOT-X-STATE')) return
    if (.not. ABSENT_RECORD(ipax,'SPOT-X-EPOCH')) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-DIMS',4,1)) return
    call LCMGET(ipax,'SPOT-X-DIMS',state_dims)
    if (state_dims(1) /= 1 .or. state_dims(2) /= NGRP) return
    if (state_dims(3) /= NSNAP .or. state_dims(4) <= 0) return
    ncoef = state_dims(4)
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-FIXB',1,1)) return
    call LCMGET(ipax,'SPOT-X-FIXB',fixb)
    if (fixb /= 1) return
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SPOT-X-NID',3,12, &
        'NUFISS-UNIT')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SPOT-X-BTYP',3,12, &
        'POD-FIXED')) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-RANK',NGRP,1)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-OFF',NGRP+1,1)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-GOFF',NGRP+1,1)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-BOFF',NGRP+1,1)) return
    allocate(rank(NGRP),offset(NGRP+1),gram_offset(NGRP+1), &
        basis_offset(NGRP+1),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    call LCMGET(ipax,'SPOT-X-OFF',offset)
    call LCMGET(ipax,'SPOT-X-GOFF',gram_offset)
    call LCMGET(ipax,'SPOT-X-BOFF',basis_offset)
    if (any(rank < 1) .or. any(rank > NSNAP)) return
    if (offset(1) /= 0 .or. gram_offset(1) /= 0) return
    if (basis_offset(1) /= 0 .or. offset(NGRP+1) /= ncoef) return
    do ig = 1, NGRP
      if (offset(ig+1)-offset(ig) /= NSNAP*rank(ig)) return
      if (gram_offset(ig+1)-gram_offset(ig) /= rank(ig)*rank(ig)) return
      if (basis_offset(ig+1)-basis_offset(ig) /= NREG*rank(ig)) return
    end do
    total_basis = basis_offset(NGRP+1)
    total_gram = gram_offset(NGRP+1)
    if (total_basis <= 0 .or. total_gram <= 0) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-BASIS',total_basis,2)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-A',ncoef,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-GRAM',total_gram,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-RHO',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-L',NGRP*NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-H',NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-NORM',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-PERP',NGRP*NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-GERR',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'K-EFFECTIVE',1,2)) return
    allocate(basis32(total_basis),coordinates64(ncoef), &
        gram64(total_gram),leakage64(NGRP*NSNAP),height64(NSNAP), &
        height_check64(NSNAP),offspace64(NGRP*NSNAP), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(ipax,'SPOT-X-BASIS',basis32)
    call LCMGET(ipax,'SPOT-X-A',coordinates64)
    call LCMGET(ipax,'SPOT-X-GRAM',gram64)
    call LCMGET(ipax,'SPOT-X-RHO',rho64)
    call LCMGET(ipax,'SPOT-X-L',leakage64)
    call LCMGET(ipax,'SPOT-X-H',height64)
    call LCMGET(ipax,'SPOT-X-NORM',norm64)
    call LCMGET(ipax,'SPOT-X-PERP',offspace64)
    call LCMGET(ipax,'SPOT-X-GERR',gram_error64)
    call LCMGET(ipax,'K-EFFECTIVE',keff32)
    if (.not. all(ieee_is_finite(basis32))) return
    if (.not. all(ieee_is_finite(coordinates64))) return
    if (.not. all(ieee_is_finite(gram64))) return
    if (.not. all(ieee_is_finite(leakage64))) return
    if (.not. all(ieee_is_finite(height64))) return
    if (.not. all(ieee_is_finite(offspace64))) return
    if (any(height64 <= +0.0_real64)) return
    if (any(offspace64 < +0.0_real64)) return
    if (.not. ieee_is_finite(norm64) .or. norm64 <= +0.0_real64) return
    if (.not. ieee_is_finite(gram_error64) .or. &
        gram_error64 < +0.0_real64) return
    if (.not. ieee_is_finite(keff32) .or. keff32 <= +0.0_real32) return
    if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/real(keff32,real64),0_int64)
    if (found64 /= expected64) return

    ! Bind the stored POD bundle to the derived geometry identities retained
    ! by SPOSTATE.  These identities are not a hash of every axial-track row.
    if (.not. CHARACTER_RECORD_MATCHES(ipaxtrack,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipaxtrack,'TRACK-TYPE',3,12, &
        'SPOT')) return
    if (.not. RECORD_MATCHES(ipaxtrack,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipaxtrack,'STATE-VECTOR',axial_track_state)
    if (axial_track_state(1) /= NREG*axial_track_state(7)) return
    if (axial_state(2) /= axial_track_state(2)) return
    if (axial_track_state(6) /= NREG) return
    if (axial_track_state(7) <= 0 .or. axial_track_state(8) /= NSNAP) return
    if (axial_track_state(11) < 0) return
    if (axial_track_state(12) /= &
        NREG*(axial_track_state(7)+1)) return
    if (axial_track_state(11)+axial_track_state(12) > &
        axial_track_state(2)) return
    nfloor = axial_track_state(7)
    if (.not. RECORD_MATCHES(ipaxtrack,'AREA2D',NREG,2)) return
    if (.not. RECORD_MATCHES(ipaxtrack,'MAT1D',nfloor,1)) return
    if (.not. RECORD_MATCHES(ipaxtrack,'VOL1D',nfloor,2)) return
    allocate(mat1d(nfloor),dz32(nfloor),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(ipaxtrack,'AREA2D',area32)
    call LCMGET(ipaxtrack,'MAT1D',mat1d)
    call LCMGET(ipaxtrack,'VOL1D',dz32)
    if (.not. all(ieee_is_finite(area32))) return
    if (.not. all(ieee_is_finite(dz32))) return
    if (any(area32 <= +0.0_real32) .or. any(dz32 <= +0.0_real32)) return
    if (any(mat1d < 1) .or. any(mat1d > NSNAP)) return
    height_check64 = +0.0_real64
    do ir = 1, nfloor
      height_check64(mat1d(ir)) = height_check64(mat1d(ir)) + &
          real(dz32(ir),real64)
    end do
    do ip = 1, NSNAP
      if (transfer(height_check64(ip),0_int64) /= &
          transfer(height64(ip),0_int64)) return
    end do

    ! Replay SPOSTATE's frozen-toolchain Gram arithmetic exactly.  This is
    ! an identity check, never an orthogonality tolerance or fit criterion.
    weight_sum = sum(real(area32,real64))
    if (.not. ieee_is_finite(weight_sum) .or. &
        weight_sum <= +0.0_real64) return
    gram_error_check64 = +0.0_real64
    do ig = 1, NGRP
      nmode = rank(ig)
      do a = 1, nmode
        do b = 1, nmode
          gram_value = +0.0_real64
          do ir = 1, NREG
            index_a = basis_offset(ig)+(a-1)*NREG+ir
            index_b = basis_offset(ig)+(b-1)*NREG+ir
            gram_value = gram_value + real(area32(ir),real64)/ &
                weight_sum*real(basis32(index_a),real64)* &
                real(basis32(index_b),real64)
          end do
          index_g = gram_offset(ig)+(b-1)*nmode+a
          if (transfer(gram_value,0_int64) /= &
              transfer(gram64(index_g),0_int64)) return
          if (a == b) then
            gram_error_check64 = max(gram_error_check64, &
                abs(gram_value-1.0_real64))
          else
            gram_error_check64 = max(gram_error_check64,abs(gram_value))
          end if
        end do
      end do
    end do
    if (transfer(gram_error_check64,0_int64) /= &
        transfer(gram_error64,0_int64)) return

    ! The archive is an unsealed bootstrap candidate.  Its four same-index
    ! plane lists must be complete, while every lifecycle marker is absent.
    if (.not. CHARACTER_RECORD_MATCHES(iparchive,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(iparchive,'LISTDIM',1,1)) return
    call LCMGET(iparchive,'LISTDIM',archive_planes)
    if (archive_planes /= NSNAP) return
    if (.not. ABSENT_RECORD(iparchive,'SPOT-R64')) return
    if (.not. RECORD_MATCHES(iparchive,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'SYSTEM',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'FLUX',NSNAP,10)) return
    if (.not. RECORD_MATCHES(iparchive,'SPOT-ITER-K',1,4)) return
    call LCMGET(iparchive,'SPOT-ITER-K',iter_keff64)
    if (.not. ieee_is_finite(iter_keff64) .or. &
        iter_keff64 <= +0.0_real64) return
    if (transfer(iter_keff64,0_int64) /= &
        transfer(real(keff32,real64),0_int64)) return
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
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'SIGNATURE', &
          3,12,'L_TRACK')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_library(ip),'SIGNATURE', &
          3,12,'L_LIBRARY')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_system(ip),'SIGNATURE', &
          3,12,'L_PIJ')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_flux(ip),'SIGNATURE', &
          3,12,'L_FLUX')) return

      if (.not. RECORD_MATCHES(input_library(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_library(ip),'STATE-VECTOR',library_state)
      if (library_state(1) /= NMAT .or. library_state(2) <= 0) return
      if (library_state(3) /= NGRP .or. library_state(4) /= 3) return
      if (.not. RECORD_MATCHES(input_library(ip),'MACROLIB',-1,0)) return
      library_macro = LCMGID(input_library(ip),'MACROLIB')
      if (.not. c_associated(library_macro)) return
      if (.not. CHARACTER_RECORD_MATCHES(library_macro,'SIGNATURE', &
          3,12,'L_MACROLIB')) return
      if (.not. RECORD_MATCHES(library_macro,'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(library_macro,'STATE-VECTOR',macro_state)
      if (macro_state(1) /= NGRP .or. macro_state(2) /= NMAT) return
      if (macro_state(3) /= 3 .or. macro_state(4) /= NIFIS) return
      if (macro_state(6) /= 2 .or. macro_state(13) /= 0) return
      if (.not. RECORD_MATCHES(library_macro,'GROUP',NGRP,10)) return
      macro_groups = LCMGID(library_macro,'GROUP')
      if (.not. c_associated(macro_groups)) return
      do ig = 1, NGRP
        if (.not. LIST_ITEM_IS_DIRECTORY(macro_groups,ig)) return
      end do

      if (.not. RECORD_MATCHES(input_system(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_system(ip),'STATE-VECTOR',system_state)
      if (any(system_state(1:14) /= &
          [1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0])) return
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
      call LCMGET(input_system(ip),'SPOT-LEAK1D',system_leak32)
      ! SYSTEM retains the leakage used by the completed radial solve; the
      ! closing SPOLEAK updates FLUX to the returned state.  The next SYSTEM
      ! is rebuilt, so these records belong to different Picard stages and
      ! are not required to be equal.
      if (.not. all(ieee_is_finite(system_leak32))) return
      if (.not. RECORD_MATCHES(input_system(ip),'SPOT-L1-SNAP',1,1)) return
      call LCMGET(input_system(ip),'SPOT-L1-SNAP',system_snapshot)
      if (system_snapshot /= ip) return

      if (.not. RECORD_MATCHES(input_track(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_track(ip),'STATE-VECTOR',plane_track_state)
      if (plane_track_state(1) /= NREG .or. &
          plane_track_state(2) /= NUNKNO) return
      if (plane_track_state(4) /= NMAT .or. &
          plane_track_state(5) /= 6) return
      if (plane_track_state(6) /= 1 .or. &
          plane_track_state(9) /= 0) return
      if (plane_track_state(14) /= 4) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'TRACK-TYPE', &
          3,12,'MCCG')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'LINK.FTRACK', &
          3,12,'TRACK_f')) return
      if (.not. RECORD_MATCHES(input_track(ip),'VOLUME',NREG,2)) return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX',NREG,1)) return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX$ANIS', &
          NREG,1)) return
      call LCMGET(input_track(ip),'VOLUME',volume32)
      call LCMGET(input_track(ip),'KEYFLX',plane_key)
      call LCMGET(input_track(ip),'KEYFLX$ANIS',anis_key)
      if (.not. all(ieee_is_finite(volume32))) return
      if (any(volume32 <= +0.0_real32)) return
      seen_unknown = .false.
      do ir = 1, NREG
        if (transfer(volume32(ir),0_int32) /= &
            transfer(area32(ir),0_int32)) return
        if (plane_key(ir) /= anis_key(ir)) return
        if (anis_key(ir) < 1 .or. anis_key(ir) > NUNKNO) return
        if (seen_unknown(anis_key(ir))) return
        seen_unknown(anis_key(ir)) = .true.
      end do

      if (.not. RECORD_MATCHES(input_flux(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_flux(ip),'STATE-VECTOR',plane_state)
      if (plane_state(1) /= NGRP .or. plane_state(2) /= NUNKNO) return
      if (plane_state(3) /= 1 .or. any(plane_state(4:7) /= 0)) return
      if (plane_state(8) /= 3 .or. plane_state(9) /= 3) return
      if (plane_state(10) /= 1 .or. plane_state(17) /= NMAT) return
      if (plane_state(11) /= 740 .or. plane_state(12) /= 500) return
      if (any(plane_state(13:16) /= 0)) return
      if (plane_state(18) /= 1 .or. &
          any(plane_state(19:NSTATE) /= 0)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'EPS-CONVERGE',5,2)) return
      call LCMGET(input_flux(ip),'EPS-CONVERGE',eps_converge)
      if (.not. all(ieee_is_finite(eps_converge))) return
      if (transfer(eps_converge(1),0_int32) /= FROZEN_TOL_BITS) return
      if (transfer(eps_converge(2),0_int32) /= FROZEN_TOL_BITS) return
      if (transfer(eps_converge(3),0_int32) /= FROZEN_TOL_BITS) return
      if (any(abs(eps_converge(4:5)) > +0.0_real32)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'IMERGE-LEAK',NMAT,1)) return
      call LCMGET(input_flux(ip),'IMERGE-LEAK',imerge)
      if (any(imerge /= 1)) return
      if (.not. CHARACTER_RECORD_MATCHES(input_flux(ip),'OPTION', &
          1,4,'B0  ')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_flux(ip),'LINK.MACRO', &
          3,12,'MACRO0')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_flux(ip),'LINK.TRACK', &
          3,12,'TRACK')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_flux(ip),'LINK.SYSTEM', &
          3,12,'SYSTEM')) return
      if (.not. RECORD_MATCHES(input_flux(ip),'KEYFLX',NREG,1)) return
      call LCMGET(input_flux(ip),'KEYFLX',seed_key)
      if (any(seed_key /= anis_key)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'SPOT-LEAK1D', &
          NGRP,2)) return
      call LCMGET(input_flux(ip),'SPOT-LEAK1D',plane_leak32)
      do ig = 1, NGRP
        if (.not. ieee_is_finite(plane_leak32(ig))) return
        found64 = transfer(leakage64((ip-1)*NGRP+ig),0_int64)
        expected64 = transfer(real(plane_leak32(ig),real64),0_int64)
        if (found64 /= expected64) return
      end do

      if (.not. RECORD_MATCHES(input_flux(ip),'SPOT-R64',-1,0)) return
      plane_authority(ip) = LCMGID(input_flux(ip),'SPOT-R64')
      if (.not. c_associated(plane_authority(ip))) return
      if (.not. AUTHORITY_HAS_EXACT_PAYLOAD(plane_authority(ip))) return
      if (.not. ABSENT_RECORD(plane_authority(ip),'RHO')) return
      if (.not. ABSENT_RECORD(plane_authority(ip),'STATE')) return
      if (.not. ABSENT_RECORD(plane_authority(ip),'EPOCH')) return
      if (.not. ABSENT_RECORD(plane_authority(ip),'QFISS')) return
      if (.not. RECORD_MATCHES(plane_authority(ip),'FLUX', &
          NGRP,10)) return
      if (.not. RECORD_MATCHES(plane_authority(ip),'SOUR', &
          NGRP,10)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'FLUX',NGRP,10)) return
      if (.not. RECORD_MATCHES(input_flux(ip),'SOUR',NGRP,10)) return
      authority_flux = LCMGID(plane_authority(ip),'FLUX')
      authority_source = LCMGID(plane_authority(ip),'SOUR')
      mirror_flux = LCMGID(input_flux(ip),'FLUX')
      mirror_source = LCMGID(input_flux(ip),'SOUR')
      if (.not. c_associated(authority_flux)) return
      if (.not. c_associated(authority_source)) return
      if (.not. c_associated(mirror_flux)) return
      if (.not. c_associated(mirror_source)) return
      do ig = 1, NGRP
        call LCMLEL(authority_flux,ig,ilong,itylcm)
        if (ilong /= NUNKNO .or. itylcm /= 4) return
        call LCMLEL(authority_source,ig,ilong,itylcm)
        if (ilong /= NUNKNO .or. itylcm /= 4) return
        call LCMLEL(mirror_flux,ig,ilong,itylcm)
        if (ilong /= NUNKNO .or. itylcm /= 2) return
        call LCMLEL(mirror_source,ig,ilong,itylcm)
        if (ilong /= NUNKNO .or. itylcm /= 2) return
        call LCMGDL(authority_flux,ig,authority_flux64)
        call LCMGDL(authority_source,ig,authority_source64)
        call LCMGDL(mirror_flux,ig,mirror_flux32)
        call LCMGDL(mirror_source,ig,mirror_source32)
        if (.not. all(ieee_is_finite(authority_flux64))) return
        if (.not. all(ieee_is_finite(authority_source64))) return
        if (.not. all(ieee_is_finite(mirror_flux32))) return
        if (.not. all(ieee_is_finite(mirror_source32))) return
        if (any(abs(authority_flux64) > REAL32_MAX64)) return
        if (any(abs(authority_source64) > REAL32_MAX64)) return
        do iu = 1, NUNKNO
          found32 = transfer(mirror_flux32(iu),0_int32)
          expected32 = transfer(real(authority_flux64(iu),real32),0_int32)
          if (found32 /= expected32) return
          found32 = transfer(mirror_source32(iu),0_int32)
          expected32 = transfer(real(authority_source64(iu),real32),0_int32)
          if (found32 /= expected32) return
        end do
        do ir = 1, NREG
          if (authority_flux64(anis_key(ir)) <= +0.0_real64) return
        end do
      end do
    end do

    ! Repeat the two freshness checks immediately before the first write.
    if (.not. EMPTY_MEMORY_ROOT(ipaxout)) return
    if (.not. EMPTY_MEMORY_ROOT(iparchiveout)) return

    ! Fresh-target copies are deliberate: LCMEQU is never applied to an old
    ! archive or plane.  The read-only inputs remain untouched on all paths.
    call LCMEQU(ipax,ipaxout)
    signature = 'L_ARCHIVE'
    call LCMPTC(iparchiveout,'SIGNATURE',12,signature)
    call LCMPUT(iparchiveout,'LISTDIM',1,1,archive_planes)
    call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)
    output_tracks = LCMLID(iparchiveout,'TRACK',NSNAP)
    output_libraries = LCMLID(iparchiveout,'MICROLIB2',NSNAP)
    output_systems = LCMLID(iparchiveout,'SYSTEM',NSNAP)
    output_fluxes = LCMLID(iparchiveout,'FLUX',NSNAP)
    if (.not. c_associated(output_tracks)) &
        call XABORT('SPOR64_B2I: OUTPUT TRACK LIST CREATION FAILED.')
    if (.not. c_associated(output_libraries)) &
        call XABORT('SPOR64_B2I: OUTPUT LIBRARY LIST CREATION FAILED.')
    if (.not. c_associated(output_systems)) &
        call XABORT('SPOR64_B2I: OUTPUT SYSTEM LIST CREATION FAILED.')
    if (.not. c_associated(output_fluxes)) &
        call XABORT('SPOR64_B2I: OUTPUT FLUX LIST CREATION FAILED.')
    lifecycle_state = 'SOLVED'
    do ip = 1, NSNAP
      output_item = LCMDIL(output_tracks,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2I: OUTPUT TRACK ITEM CREATION FAILED.')
      call LCMEQU(input_track(ip),output_item)
      output_item = LCMDIL(output_libraries,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2I: OUTPUT LIBRARY ITEM CREATION FAILED.')
      call LCMEQU(input_library(ip),output_item)
      output_item = LCMDIL(output_systems,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2I: OUTPUT SYSTEM ITEM CREATION FAILED.')
      call LCMEQU(input_system(ip),output_item)
      output_item = LCMDIL(output_fluxes,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2I: OUTPUT FLUX ITEM CREATION FAILED.')
      call LCMEQU(input_flux(ip),output_item)
      output_authority = LCMGID(output_item,'SPOT-R64')
      if (.not. c_associated(output_authority)) &
          call XABORT('SPOR64_B2I: OUTPUT PLANE AUTHORITY MISSING.')
      ! RHO labels the completed outer state; it is not asserted to be the
      ! eigenvalue used by the preceding (lagged) radial equation.
      call LCMPUT(output_authority,'RHO',1,4,rho64)
      call LCMPTC(output_authority,'STATE',12,lifecycle_state)
      call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)
    end do

    ! The archive root is the sole global commit.  A partial fresh pair has
    ! no CLOSED root and must be discarded; no LCM mutation follows EPOCH.
    lifecycle_state = 'CLOSED'
    call LCMPTC(ipaxout,'SPOT-X-STATE',12,lifecycle_state)
    call LCMPUT(ipaxout,'SPOT-X-EPOCH',1,1,BOOTSTRAP_EPOCH)
    output_authority = LCMDID(iparchiveout,'SPOT-R64')
    if (.not. c_associated(output_authority)) &
        call XABORT('SPOR64_B2I: OUTPUT ROOT AUTHORITY CREATION FAILED.')
    call LCMPUT(output_authority,'RHO',1,4,rho64)
    call LCMPUT(output_authority,'NPLANE',1,1,archive_planes)
    call LCMPTC(output_authority,'STATE',12,lifecycle_state)
    call LCMPUT(output_authority,'EPOCH',1,1,BOOTSTRAP_EPOCH)
    status = SPOR64_B2I_BOOTSTRAP_COMMITTED
  end subroutine SPOR64_B2I_SEAL_BOOTSTRAP
  logical function AUTHORITY_HAS_EXACT_PAYLOAD(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12) :: first_name, item_name
    integer :: item_count
    logical :: saw_flux, saw_source

    AUTHORITY_HAS_EXACT_PAYLOAD = .false.
    if (.not. c_associated(iplist)) return
    item_name = ' '
    call LCMNXT(iplist,item_name)
    if (item_name == ' ') return
    first_name = item_name
    item_count = 0
    saw_flux = .false.
    saw_source = .false.
    do
      item_count = item_count+1
      if (item_count > 2) return
      select case(item_name)
      case('FLUX')
        if (saw_flux) return
        saw_flux = .true.
      case('SOUR')
        if (saw_source) return
        saw_source = .true.
      case default
        return
      end select
      call LCMNXT(iplist,item_name)
      if (item_name == first_name) exit
    end do
    AUTHORITY_HAS_EXACT_PAYLOAD = item_count == 2 .and. &
        saw_flux .and. saw_source
  end function AUTHORITY_HAS_EXACT_PAYLOAD
end module SPOR64_B2I
