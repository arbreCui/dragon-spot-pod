module SPOR64_B2W
  ! Admits a RETURNED archive and closes the epoch.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, RECORD_MATCHES
  use SPOR64_SCHEMA, only : SCHEMA_FEEDBACK_ROOT, &
      SCHEMA_RETURNED_CHILD_AUTHORITY, SCHEMA_RETURNED_CHILD_ROOT, &
      SCHEMA_RETURNED_FEEDBACK_ROOT, SCHEMA_RETURNED_ROOT_AUTHORITY, &
      SCHEMA_SYSTEM_AUTHORITY, SCHEMA_SYSTEM_ROOT, SCHEMA_SYSTEM_ROOT_L1RAW
  implicit none
  private

  integer, parameter, public :: SPOR64_B2W_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2W_CLOSED = 2
  integer, parameter, public :: SPOR64_B2W_RETURNED_ADMITTED = 3

  integer, parameter :: NSTATE = 40
  integer, parameter :: NSNAP = 3
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NUNKNO = 14
  integer, parameter :: NMAT = 8
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2W_ADMIT_RETURNED, SPOR64_B2W_CLOSE

contains

  subroutine SPOR64_B2W_ADMIT_RETURNED(ipfeedback,status)
    type(c_ptr), intent(in) :: ipfeedback
    integer, intent(out) :: status

    integer :: ip, ig, archive_planes, root_planes, root_epoch
    integer :: child_epoch(NSNAP), fs_marker(NSNAP)
    integer(int32) :: found32, expected32
    integer(int64) :: found64, expected64
    real(real32) :: fs_keff32(NSNAP)
    real(real32) :: child_leakage32(NGRP,NSNAP)
    real(real32) :: system_leakage32(NGRP,NSNAP)
    real(real64) :: child_rho64(NSNAP)
    type(c_ptr) :: root_authority
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: input_system, input_flux

    status = SPOR64_B2W_PREFLIGHT_FAILED
    if (.not. c_associated(ipfeedback)) return

    ! Admit the exact object returned by B2R before any fresh axial work.
    ! This routine is read-only: no LCM mutation is possible on either path.
    if (.not. RETURNED_FEEDBACK_ROOT_IS_EXACT(ipfeedback)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipfeedback,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipfeedback,'LISTDIM',1,1)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SPOT-R64',-1,0)) return
    call LCMGET(ipfeedback,'LISTDIM',archive_planes)
    if (archive_planes /= NSNAP) return

    root_authority = LCMGID(ipfeedback,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. RETURNED_ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'RETURNED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    if (.not. ABSENT_RECORD(root_authority,'RHO')) return
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (root_planes /= NSNAP .or. root_epoch <= 0) return

    if (.not. RECORD_MATCHES(ipfeedback,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SYSTEM',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'FLUX',NSNAP,10)) return
    tracks = LCMGID(ipfeedback,'TRACK')
    libraries = LCMGID(ipfeedback,'MICROLIB2')
    systems = LCMGID(ipfeedback,'SYSTEM')
    fluxes = LCMGID(ipfeedback,'FLUX')
    if (.not. c_associated(tracks)) return
    if (.not. c_associated(libraries)) return
    if (.not. c_associated(systems)) return
    if (.not. c_associated(fluxes)) return

    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(systems,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
      input_system = LCMGIL(systems,ip)
      input_flux = LCMGIL(fluxes,ip)
      if (.not. c_associated(input_system)) return
      if (.not. c_associated(input_flux)) return
      if (.not. RETURNED_CHILD_IS_VALID(input_flux,child_rho64(ip), &
          fs_keff32(ip),child_epoch(ip),fs_marker(ip), &
          child_leakage32(:,ip))) return
      if (child_epoch(ip) /= root_epoch) return
      if (.not. RETURNED_SYSTEM_IS_VALID(input_system,ip, &
          child_rho64(ip),child_epoch(ip),system_leakage32(:,ip))) return

      ! ASM consumes child L0.  Bind it element by element to the L0 retained
      ! by the same-index SYSTEM; a scalar norm cannot prove this identity.
      do ig = 1, NGRP
        found32 = transfer(child_leakage32(ig,ip),0_int32)
        expected32 = transfer(system_leakage32(ig,ip),0_int32)
        if (found32 /= expected32) return
      end do
    end do

    ! All three children solve the same frozen radial equation generation.
    do ip = 2, NSNAP
      found64 = transfer(child_rho64(ip),0_int64)
      expected64 = transfer(child_rho64(1),0_int64)
      if (found64 /= expected64) return
      found32 = transfer(fs_keff32(ip),0_int32)
      expected32 = transfer(fs_keff32(1),0_int32)
      if (found32 /= expected32) return
    end do

    status = SPOR64_B2W_RETURNED_ADMITTED
  end subroutine SPOR64_B2W_ADMIT_RETURNED

  subroutine SPOR64_B2W_CLOSE(ipaxout,iparchiveout,ipax,ipfeedback,status)
    type(c_ptr), intent(in) :: ipaxout, iparchiveout, ipax, ipfeedback
    integer, intent(out) :: status

    integer :: ip, ig, archive_planes, root_planes, root_epoch
    integer :: child_epoch(NSNAP), fs_marker(NSNAP)
    integer(int32) :: found32, expected32
    integer(int64) :: found64, expected64
    real(real32) :: keff32, l1_error32, fs_keff32(NSNAP)
    real(real32) :: child_leakage32(NGRP,NSNAP)
    real(real32) :: system_leakage32(NGRP,NSNAP), checked_l1_error32
    real(real64) :: rho1, iter_keff64, child_rho64(NSNAP)
    real(real64) :: axial_leakage64(NGRP*NSNAP)
    character(len=12) :: signature, lifecycle_state
    type(c_ptr) :: root_authority
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: input_track(NSNAP), input_library(NSNAP)
    type(c_ptr) :: input_system(NSNAP), input_flux(NSNAP)
    type(c_ptr) :: output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes
    type(c_ptr) :: output_item, output_authority

    status = SPOR64_B2W_PREFLIGHT_FAILED

    ! The two targets and two immutable inputs are four distinct roots.
    if (.not. c_associated(ipaxout)) return
    if (.not. c_associated(iparchiveout)) return
    if (.not. c_associated(ipax)) return
    if (.not. c_associated(ipfeedback)) return
    if (c_associated(ipaxout,iparchiveout)) return
    if (c_associated(ipaxout,ipax)) return
    if (c_associated(ipaxout,ipfeedback)) return
    if (c_associated(iparchiveout,ipax)) return
    if (c_associated(iparchiveout,ipfeedback)) return
    if (c_associated(ipax,ipfeedback)) return
    if (.not. EMPTY_ROOT(ipaxout)) return
    if (.not. EMPTY_ROOT(iparchiveout)) return

    ! Recover the complete canonical axial bundle.  The axial root also owns
    ! ordinary solver records, so only the canonical records are prescribed.
    if (.not. CANONICAL_AX_IS_VALID(ipax,keff32,rho1, &
        axial_leakage64)) return

    ! The feedback root has exactly the seven returned-archive records plus
    ! the two records produced by the direct leakage update.
    if (.not. FEEDBACK_ROOT_IS_EXACT(ipfeedback)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipfeedback,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipfeedback,'LISTDIM',1,1)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SPOT-ITER-K',1,4)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SPOT-L1-ERR',1,2)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SPOT-R64',-1,0)) return
    call LCMGET(ipfeedback,'LISTDIM',archive_planes)
    call LCMGET(ipfeedback,'SPOT-ITER-K',iter_keff64)
    call LCMGET(ipfeedback,'SPOT-L1-ERR',l1_error32)
    if (archive_planes /= NSNAP) return
    if (.not. ieee_is_finite(iter_keff64)) return
    if (iter_keff64 <= +0.0_real64) return
    found64 = transfer(iter_keff64,0_int64)
    expected64 = transfer(real(keff32,real64),0_int64)
    if (found64 /= expected64) then
      found32 = transfer(real(iter_keff64,real32),0_int32)
      expected32 = transfer(keff32,0_int32)
      if (found32 /= expected32) return
    end if
    if (.not. ieee_is_finite(l1_error32)) return
    if (l1_error32 < +0.0_real32) return

    root_authority = LCMGID(ipfeedback,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. RETURNED_ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'RETURNED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    if (.not. ABSENT_RECORD(root_authority,'RHO')) return
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (root_planes /= NSNAP .or. root_epoch <= 0) return

    if (.not. RECORD_MATCHES(ipfeedback,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'SYSTEM',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipfeedback,'FLUX',NSNAP,10)) return
    tracks = LCMGID(ipfeedback,'TRACK')
    libraries = LCMGID(ipfeedback,'MICROLIB2')
    systems = LCMGID(ipfeedback,'SYSTEM')
    fluxes = LCMGID(ipfeedback,'FLUX')
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
      if (.not. RETURNED_CHILD_IS_VALID(input_flux(ip), &
          child_rho64(ip),fs_keff32(ip),child_epoch(ip),fs_marker(ip), &
          child_leakage32(:,ip))) return
      if (child_epoch(ip) /= root_epoch) return
      if (.not. RETURNED_SYSTEM_IS_VALID(input_system(ip),ip, &
          child_rho64(ip),child_epoch(ip),system_leakage32(:,ip))) return
    end do

    ! The radial equation coefficient is plane-independent and is tied to
    ! its stored binary32 eigenvalue by the frozen reciprocal operation.
    do ip = 2, NSNAP
      found64 = transfer(child_rho64(ip),0_int64)
      expected64 = transfer(child_rho64(1),0_int64)
      if (found64 /= expected64) return
      found32 = transfer(fs_keff32(ip),0_int32)
      expected32 = transfer(fs_keff32(1),0_int32)
      if (found32 /= expected32) return
    end do

    ! SPOLEAK compares its fresh L1 against the returned radial-equation L0.
    ! The archived SYSTEM retains that L0, so the transition diagnostic is
    ! an exact reproducible identity, never an acceptance threshold.
    checked_l1_error32 = maxval(abs(child_leakage32-system_leakage32))
    found32 = transfer(l1_error32,0_int32)
    expected32 = transfer(checked_l1_error32,0_int32)
    if (found32 /= expected32) return

    ! The newly integrated plane leakage is the exact binary32-to-binary64
    ! promotion stored in the canonical axial state.  No error threshold is
    ! applied, and lagged SYSTEM L0 is not required to equal fresh L1.
    do ip = 1, NSNAP
      do ig = 1, NGRP
        found64 = transfer(axial_leakage64((ip-1)*NGRP+ig),0_int64)
        expected64 = transfer(real(child_leakage32(ig,ip),real64), &
            0_int64)
        if (found64 /= expected64) then
          found32 = transfer(real(axial_leakage64((ip-1)*NGRP+ig), &
              real32),0_int32)
          expected32 = transfer(child_leakage32(ig,ip),0_int32)
          if (found32 /= expected32) return
        end if
      end do
    end do

    ! Close the caller-visible time-of-check window before the first write.
    if (.not. EMPTY_ROOT(ipaxout)) return
    if (.not. EMPTY_ROOT(iparchiveout)) return

    call LCMEQU(ipax,ipaxout)
    lifecycle_state = 'CLOSED'
    call LCMPTC(ipaxout,'SPOT-X-STATE',12,lifecycle_state)
    call LCMPUT(ipaxout,'SPOT-X-EPOCH',1,1,root_epoch)

    ! Rebuild the archive root so the transition-only error diagnostic is
    ! not propagated.  All four indexed payloads are recursive copies.
    signature = 'L_ARCHIVE'
    call LCMPTC(iparchiveout,'SIGNATURE',12,signature)
    call LCMPUT(iparchiveout,'LISTDIM',1,1,archive_planes)
    call LCMPUT(iparchiveout,'SPOT-ITER-K',1,4,iter_keff64)
    output_tracks = LCMLID(iparchiveout,'TRACK',NSNAP)
    output_libraries = LCMLID(iparchiveout,'MICROLIB2',NSNAP)
    output_systems = LCMLID(iparchiveout,'SYSTEM',NSNAP)
    output_fluxes = LCMLID(iparchiveout,'FLUX',NSNAP)
    if (.not. c_associated(output_tracks)) &
        call XABORT('SPOR64_B2W: OUTPUT TRACK LIST CREATION FAILED.')
    if (.not. c_associated(output_libraries)) &
        call XABORT('SPOR64_B2W: OUTPUT LIBRARY LIST CREATION FAILED.')
    if (.not. c_associated(output_systems)) &
        call XABORT('SPOR64_B2W: OUTPUT SYSTEM LIST CREATION FAILED.')
    if (.not. c_associated(output_fluxes)) &
        call XABORT('SPOR64_B2W: OUTPUT FLUX LIST CREATION FAILED.')

    do ip = 1, NSNAP
      output_item = LCMDIL(output_tracks,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2W: OUTPUT TRACK ITEM CREATION FAILED.')
      call LCMEQU(input_track(ip),output_item)
      output_item = LCMDIL(output_libraries,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2W: OUTPUT LIBRARY ITEM CREATION FAILED.')
      call LCMEQU(input_library(ip),output_item)
      output_item = LCMDIL(output_systems,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2W: OUTPUT SYSTEM ITEM CREATION FAILED.')
      call LCMEQU(input_system(ip),output_item)
      output_item = LCMDIL(output_fluxes,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2W: OUTPUT FLUX ITEM CREATION FAILED.')
      call LCMEQU(input_flux(ip),output_item)
      output_authority = LCMGID(output_item,'SPOT-R64')
      if (.not. c_associated(output_authority)) &
          call XABORT('SPOR64_B2W: OUTPUT FLUX AUTHORITY MISSING.')
      ! QFISS belongs only to the RETURNED transition.  A CLOSED child has
      ! the same five-record authority consumed by B2j on the next epoch.
      call LCMDEL(output_authority,'QFISS')
      ! In a CLOSED archive, child RHO labels the completed outer state.
      ! SPOT-FS-K remains the immutable receipt of the preceding radial
      ! equation; B2j must not confuse that lagged equation coefficient with
      ! the state being projected next.
      call LCMPUT(output_authority,'RHO',1,4,rho1)
      ! Rewriting EPOCH commits the relabelled child after its RHO update.
      call LCMPUT(output_authority,'EPOCH',1,1,root_epoch)
    end do

    output_authority = LCMDID(iparchiveout,'SPOT-R64')
    if (.not. c_associated(output_authority)) &
        call XABORT('SPOR64_B2W: ROOT AUTHORITY CREATION FAILED.')
    call LCMPUT(output_authority,'RHO',1,4,rho1)
    call LCMPUT(output_authority,'NPLANE',1,1,archive_planes)
    call LCMPTC(output_authority,'STATE',12,lifecycle_state)
    ! This is the archive-wide commit and the final LCM mutation.
    call LCMPUT(output_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_B2W_CLOSED
  end subroutine SPOR64_B2W_CLOSE


  logical function CANONICAL_AX_IS_VALID(ipax,keff32,rho64,leakage64)
    type(c_ptr), intent(in) :: ipax
    real(real32), intent(out) :: keff32
    real(real64), intent(out) :: rho64, leakage64(NGRP*NSNAP)

    integer :: state(NSTATE), dims(4), fixb, ncoef
    integer :: rank(NGRP), offset(NGRP+1)
    integer :: gram_offset(NGRP+1), basis_offset(NGRP+1)
    integer :: ig, total_gram, total_basis, allocation_status
    integer(int64) :: found64, expected64
    real(real32), allocatable :: basis32(:)
    real(real64), allocatable :: coordinates64(:), gram64(:)
    real(real64) :: height64(NSNAP), norm64
    real(real64) :: keff64r
    integer :: lenk64, tylk64
    real(real64) :: offspace64(NGRP*NSNAP), gram_error64

    CANONICAL_AX_IS_VALID = .false.
    keff32 = +0.0_real32
    rho64 = +0.0_real64
    leakage64 = +0.0_real64

    if (.not. CHARACTER_RECORD_MATCHES(ipax,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipax,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipax,'STATE-VECTOR',state)
    if (state(1) /= NGRP .or. state(2) <= 0) return
    if (.not. RECORD_MATCHES(ipax,'K-EFFECTIVE',1,2)) return
    call LCMGET(ipax,'K-EFFECTIVE',keff32)
    if (.not. ieee_is_finite(keff32)) return
    if (keff32 <= +0.0_real32) return
    if (.not. ABSENT_RECORD(ipax,'SPOT-X-STATE')) return
    if (.not. ABSENT_RECORD(ipax,'SPOT-X-EPOCH')) return

    if (.not. RECORD_MATCHES(ipax,'SPOT-X-DIMS',4,1)) return
    call LCMGET(ipax,'SPOT-X-DIMS',dims)
    if (any(dims(1:3) /= [1,NGRP,NSNAP])) return
    if (dims(4) <= 0) return
    ncoef = dims(4)
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
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    call LCMGET(ipax,'SPOT-X-OFF',offset)
    call LCMGET(ipax,'SPOT-X-GOFF',gram_offset)
    call LCMGET(ipax,'SPOT-X-BOFF',basis_offset)
    if (any(rank < 1) .or. any(rank > NSNAP)) return
    if (offset(1) /= 0 .or. gram_offset(1) /= 0) return
    if (basis_offset(1) /= 0) return
    do ig = 1, NGRP
      if (offset(ig+1)-offset(ig) /= NSNAP*rank(ig)) return
      if (gram_offset(ig+1)-gram_offset(ig) /= &
          rank(ig)*rank(ig)) return
      if (basis_offset(ig+1)-basis_offset(ig) /= &
          NREG*rank(ig)) return
    end do
    if (offset(NGRP+1) /= ncoef) return
    total_gram = gram_offset(NGRP+1)
    total_basis = basis_offset(NGRP+1)
    if (total_gram <= 0 .or. total_basis <= 0) return

    if (.not. RECORD_MATCHES(ipax,'SPOT-X-A',ncoef,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-GRAM',total_gram,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-BASIS',total_basis,2)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-RHO',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-L',NGRP*NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-H',NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-NORM',1,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-PERP',NGRP*NSNAP,4)) return
    if (.not. RECORD_MATCHES(ipax,'SPOT-X-GERR',1,4)) return
    allocate(basis32(total_basis),coordinates64(ncoef), &
        gram64(total_gram),stat=allocation_status)
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
    if (.not. all(ieee_is_finite(basis32))) return
    if (.not. all(ieee_is_finite(coordinates64))) return
    if (.not. all(ieee_is_finite(gram64))) return
    if (.not. all(ieee_is_finite(leakage64))) return
    if (.not. all(ieee_is_finite(height64))) return
    if (.not. all(ieee_is_finite(offspace64))) return
    if (any(height64 <= +0.0_real64)) return
    if (any(offspace64 < +0.0_real64)) return
    if (.not. ieee_is_finite(norm64)) return
    if (norm64 <= +0.0_real64) return
    if (.not. ieee_is_finite(gram_error64)) return
    if (gram_error64 < +0.0_real64) return
    if (.not. ieee_is_finite(rho64)) return
    if (rho64 <= +0.0_real64) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/real(keff32,real64),0_int64)
    if (found64 /= expected64) then
      call LCMLEN(ipax,'SPOT-X-KEFF',lenk64,tylk64)
      if (lenk64 /= 1 .or. tylk64 /= 4) return
      call LCMGET(ipax,'SPOT-X-KEFF',keff64r)
      if (transfer(rho64,0_int64) /= &
          transfer(1.0_real64/keff64r,0_int64)) return
      if (transfer(real(keff64r,real32),0_int32) /= &
          transfer(keff32,0_int32)) return
    end if

    CANONICAL_AX_IS_VALID = .true.
  end function CANONICAL_AX_IS_VALID


  logical function RETURNED_SYSTEM_IS_VALID(system,plane,rho64,epoch, &
      leakage32)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane, epoch
    real(real64), intent(in) :: rho64
    real(real32), intent(out) :: leakage32(NGRP)

    integer :: state(NSTATE), found_plane, found_epoch
    integer(int64) :: found64, expected64
    real(real64) :: found_rho64
    type(c_ptr) :: authority

    RETURNED_SYSTEM_IS_VALID = .false.
    leakage32 = +0.0_real32
    if (.not. RETURNED_SYSTEM_ROOT_IS_EXACT(system)) return
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
    call LCMGET(system,'SPOT-LEAK1D',leakage32)
    call LCMGET(system,'SPOT-L1-SNAP',found_plane)
    if (.not. all(ieee_is_finite(leakage32))) return
    if (found_plane /= plane) return
    authority = LCMGID(system,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. RETURNED_SYSTEM_AUTHORITY_IS_EXACT(authority)) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'ASSEMBLED')) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    call LCMGET(authority,'RHO',found_rho64)
    call LCMGET(authority,'EPOCH',found_epoch)
    if (.not. ieee_is_finite(found_rho64)) return
    found64 = transfer(found_rho64,0_int64)
    expected64 = transfer(rho64,0_int64)
    if (found64 /= expected64) return
    if (found_epoch /= epoch) return
    RETURNED_SYSTEM_IS_VALID = .true.
  end function RETURNED_SYSTEM_IS_VALID


  logical function RETURNED_CHILD_IS_VALID(child,rho64,fs_keff32,epoch, &
      fs_marker,leakage32,iter_keff64_in)
    type(c_ptr), intent(in) :: child
    real(real64), intent(out) :: rho64
    real(real32), intent(out) :: fs_keff32, leakage32(NGRP)
    integer, intent(out) :: epoch, fs_marker
    real(real64), intent(in), optional :: iter_keff64_in

    integer :: state(NSTATE), imerge(NMAT), keyflx(NREG)
    integer :: ig, ir
    integer(int32) :: eps_bits(5)
    integer(int64) :: found64, expected64
    logical :: seen(NUNKNO)
    real(real32) :: eps32(5)
    real(real32) :: mirror_flux32(NUNKNO), mirror_source32(NUNKNO)
    real(real32) :: mirror_qfiss32(NUNKNO)
    real(real64) :: authority_flux64(NUNKNO)
    real(real64) :: authority_source64(NUNKNO)
    real(real64) :: authority_qfiss64(NUNKNO)
    type(c_ptr) :: authority
    type(c_ptr) :: mirror_flux, mirror_source
    type(c_ptr) :: authority_flux, authority_source, authority_qfiss
    type(c_ptr) :: legacy_outer, legacy_inner

    RETURNED_CHILD_IS_VALID = .false.
    rho64 = +0.0_real64
    fs_keff32 = +0.0_real32
    epoch = 0
    fs_marker = 0
    leakage32 = +0.0_real32

    if (.not. RETURNED_CHILD_ROOT_IS_EXACT(child)) return
    if (.not. CHARACTER_RECORD_MATCHES(child,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(child,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(child,'STATE-VECTOR',state)
    if (any(state(1:18) /= &
        [NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500,0,0,0,0,NMAT,1])) &
        return
    if (any(state(19:NSTATE) /= 0)) return

    ! These fixed records identify the admitted returned schema.  They are
    ! never used as a closure tolerance or numerical control in this gate.
    if (.not. RECORD_MATCHES(child,'EPS-CONVERGE',5,2)) return
    call LCMGET(child,'EPS-CONVERGE',eps32)
    if (.not. all(ieee_is_finite(eps32))) return
    eps_bits = transfer(eps32,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS)) return
    if (any(eps_bits(4:5) /= 0_int32)) return
    if (.not. RECORD_MATCHES(child,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(child,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(child,'KEYFLX',NREG,1)) return
    call LCMGET(child,'KEYFLX',keyflx)
    seen = .false.
    do ir = 1, NREG
      if (keyflx(ir) < 1 .or. keyflx(ir) > NUNKNO) return
      if (seen(keyflx(ir))) return
      seen(keyflx(ir)) = .true.
    end do
    if (.not. CHARACTER_RECORD_MATCHES(child,'OPTION',1,4,'B0  ')) &
        return
    if (.not. CHARACTER_RECORD_MATCHES(child,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(child,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(child,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return

    if (.not. RECORD_MATCHES(child,'SPOT-FS-EQN',1,1)) return
    if (.not. RECORD_MATCHES(child,'SPOT-FS-K',1,2)) return
    call LCMGET(child,'SPOT-FS-EQN',fs_marker)
    call LCMGET(child,'SPOT-FS-K',fs_keff32)
    if (fs_marker /= 1) return
    if (.not. ieee_is_finite(fs_keff32)) return
    if (fs_keff32 <= +0.0_real32) return
    if (.not. RECORD_MATCHES(child,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(child,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) return

    if (.not. RECORD_MATCHES(child,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(child,'SOUR',NGRP,10)) return
    if (.not. RECORD_MATCHES(child,'SPOT-QFISS',1,10)) return
    if (.not. RECORD_MATCHES(child,'SPOT-R64',-1,0)) return
    mirror_flux = LCMGID(child,'FLUX')
    mirror_source = LCMGID(child,'SOUR')
    legacy_outer = LCMGID(child,'SPOT-QFISS')
    authority = LCMGID(child,'SPOT-R64')
    if (.not. c_associated(mirror_flux)) return
    if (.not. c_associated(mirror_source)) return
    if (.not. c_associated(legacy_outer)) return
    if (.not. c_associated(authority)) return

    if (.not. RETURNED_CHILD_AUTHORITY_IS_EXACT(authority)) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(authority,'SOUR',NGRP,10)) return
    if (.not. RECORD_MATCHES(authority,'QFISS',NGRP,10)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'SOLVED')) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    if (.not. ABSENT_RECORD(authority,'PLANE')) return
    call LCMGET(authority,'RHO',rho64)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(rho64)) return
    if (rho64 <= +0.0_real64) return
    if (epoch <= 0) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/real(fs_keff32,real64),0_int64)
    if (found64 /= expected64) then
      if (present(iter_keff64_in)) then
        if (transfer(rho64,0_int64) /= &
            transfer(1.0_real64/iter_keff64_in,0_int64)) return
        if (transfer(fs_keff32,0_int32) /= &
            transfer(real(iter_keff64_in,real32),0_int32)) return
      else
        if (transfer(fs_keff32,0_int32) /= &
            transfer(real(1.0_real64/rho64,real32),0_int32)) return
      end if
    end if

    authority_flux = LCMGID(authority,'FLUX')
    authority_source = LCMGID(authority,'SOUR')
    authority_qfiss = LCMGID(authority,'QFISS')
    if (.not. c_associated(authority_flux)) return
    if (.not. c_associated(authority_source)) return
    if (.not. c_associated(authority_qfiss)) return
    if (.not. LIST_ITEM_MATCHES(legacy_outer,1,NGRP,10)) return
    legacy_inner = LCMGIL(legacy_outer,1)
    if (.not. c_associated(legacy_inner)) return

    do ig = 1, NGRP
      if (.not. LIST_ITEM_MATCHES(mirror_flux,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(mirror_source,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(legacy_inner,ig,NUNKNO,2)) return
      if (.not. LIST_ITEM_MATCHES(authority_flux,ig,NUNKNO,4)) return
      if (.not. LIST_ITEM_MATCHES(authority_source,ig,NUNKNO,4)) return
      if (.not. LIST_ITEM_MATCHES(authority_qfiss,ig,NUNKNO,4)) return
      call LCMGDL(mirror_flux,ig,mirror_flux32)
      call LCMGDL(mirror_source,ig,mirror_source32)
      call LCMGDL(legacy_inner,ig,mirror_qfiss32)
      call LCMGDL(authority_flux,ig,authority_flux64)
      call LCMGDL(authority_source,ig,authority_source64)
      call LCMGDL(authority_qfiss,ig,authority_qfiss64)
      if (.not. all(ieee_is_finite(mirror_flux32))) return
      if (.not. all(ieee_is_finite(mirror_source32))) return
      if (.not. all(ieee_is_finite(mirror_qfiss32))) return
      if (.not. all(ieee_is_finite(authority_flux64))) return
      if (.not. all(ieee_is_finite(authority_source64))) return
      if (.not. all(ieee_is_finite(authority_qfiss64))) return
      if (.not. REAL32_PROJECTION_MATCHES(mirror_flux32, &
          authority_flux64)) return
      if (.not. REAL32_PROJECTION_MATCHES(mirror_source32, &
          authority_source64)) return
      if (.not. REAL32_PROJECTION_MATCHES(mirror_qfiss32, &
          authority_qfiss64)) return
    end do

    RETURNED_CHILD_IS_VALID = .true.
  end function RETURNED_CHILD_IS_VALID


  logical function REAL32_PROJECTION_MATCHES(mirror,authority)
    real(real32), intent(in) :: mirror(:)
    real(real64), intent(in) :: authority(:)
    integer :: i

    REAL32_PROJECTION_MATCHES = .false.
    if (size(mirror) /= size(authority)) return
    if (.not. all(ieee_is_finite(mirror))) return
    if (.not. all(ieee_is_finite(authority))) return
    if (any(abs(authority) > REAL32_MAX64)) return
    do i = 1, size(mirror)
      if (transfer(mirror(i),0_int32) /= &
          transfer(real(authority(i),real32),0_int32)) return
    end do
    REAL32_PROJECTION_MATCHES = .true.
  end function REAL32_PROJECTION_MATCHES
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
  logical function FEEDBACK_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    FEEDBACK_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_FEEDBACK_ROOT)
  end function FEEDBACK_ROOT_IS_EXACT


  logical function RETURNED_FEEDBACK_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_FEEDBACK_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_RETURNED_FEEDBACK_ROOT)
  end function RETURNED_FEEDBACK_ROOT_IS_EXACT


  logical function RETURNED_ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_RETURNED_ROOT_AUTHORITY)
  end function RETURNED_ROOT_AUTHORITY_IS_EXACT


  logical function RETURNED_CHILD_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_CHILD_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_RETURNED_CHILD_ROOT)
  end function RETURNED_CHILD_ROOT_IS_EXACT


  logical function RETURNED_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_ROOT_L1RAW) &
        .or. EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_ROOT)
  end function RETURNED_SYSTEM_ROOT_IS_EXACT


  logical function RETURNED_SYSTEM_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_SYSTEM_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_SYSTEM_AUTHORITY)
  end function RETURNED_SYSTEM_AUTHORITY_IS_EXACT


  logical function RETURNED_CHILD_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    RETURNED_CHILD_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_RETURNED_CHILD_AUTHORITY)
  end function RETURNED_CHILD_AUTHORITY_IS_EXACT
end module SPOR64_B2W
