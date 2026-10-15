module SPOR64_BOOTQ64_V2
  ! Builds the frozen fission source each plane is solved
  ! against.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT
  use SPOR64_BOOT_CONTEXT64_V2, only : SPOR64_BOOT_CONTEXT64_READ, &
      BOOT_ARCHIVE_NAMES, BOOT_PLANE_NAMES, BOOT_PLANE_AUTH_NAMES
  use SPOR64_BOOT64, only : SPOR64_BOOT64_SAME_TREE
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, &
      RECORD_MATCHES
  use SPOR64_SCHEMA, only : SCHEMA_ARCHIVE_ROOT_AUTHORITY, &
      SCHEMA_PROJECTED_ARCHIVE_ROOT, SCHEMA_PROJECTED_AUTHORITY, &
      SCHEMA_PROJECTED_PLANE_ROOT, SCHEMA_PROJECTED_PLANE_ROOT_L64
  implicit none
  private

  integer, parameter, public :: SPOR64_BOOTQ64_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_BOOTQ64_COMMITTED = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NSNAP = 3
  integer, parameter :: NCODE = 6
  integer, parameter :: NIFIS = 32
  integer, parameter :: TRACK_ACTIVE_COMPONENTS = 1
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: MCCG_STATE_EXPECTED(NSTATE) = &
      [-1,4,10,0,0,0,80,0,0,0,0,0,20,1,1,1,0,0,1,1, &
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_BOOTQ64_BUILD, SPOR64_BOOTQ64_READ
  integer, parameter, public :: SPOR64_BOOTQ64_LOADED=3

  ! Private composed comparison retains the original BOOT64 limits.
  integer, parameter :: MAX_DEPTH = 64, MAX_NODES = 2000000
  integer, parameter :: MAX_RECORD_WORDS = 16777216
  integer, parameter :: composed_integer_kind_guard = &
      1 / merge(1,0,kind(1) == int32)
  integer, parameter :: VIEW_NONE = -1, VIEW_ROOT = 0, VIEW_AUTH = 1
  integer, parameter :: VIEW_GLOBAL = 2, VIEW_SEED = 3
  integer(int64), parameter :: COMPACT_FIXED_BYTES = 844632_int64
  integer(int64), parameter :: COMPACT_BYTES_PER_UNKNOWN = 7400_int64
  integer(int64), parameter :: COMPACT_STORAGE_CAP = 32_int64*1024_int64*1024_int64

contains

  subroutine SPOR64_BOOTQ64_BUILD(ipprojected,ipglobal,ipax,ipaxtrack, &
      ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
      ipmacro_out,ipsource_out,status)
    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out
    type(c_ptr), intent(in) :: ipglobal,ipax,ipaxtrack,ipaxsystem
    type(c_ptr), intent(in) :: ipaxmacro,iparchive,ipcontract
    type(SPOR64_ROUTE_CONTRACT) :: contract
    logical :: context_ok
    type(c_ptr) :: input_roots(8), child
    integer :: alias_index
    real(real64) :: norm64
    real(real64), allocatable :: volume64(:)
    integer, intent(in) :: plane_index
    integer, intent(out) :: status

    integer :: root_planes, root_epoch, plane_epoch
    integer :: track_state(NSTATE), mccg_state(NSTATE)
    integer :: archive_track_state(NSTATE), probe_track_state(NSTATE)
    integer :: archive_mccg_state(NSTATE), probe_mccg_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: macro_state_expected(NSTATE)
    integer :: flux_state(NSTATE), source_state(NSTATE)
    integer, allocatable :: matcod(:), nzon(:)
    integer, allocatable :: keyflx(:), keyanis(:), keycur(:)
    integer, allocatable :: imerge(:)
    integer :: ip, ir, ifis, h, g, im, iu, ilong, itylcm
    integer :: allocation_status, nreg, nunkno, nmat, nsurf, probe_nsurf
    integer(int32) :: volume_bits, track_volume_bits
    integer(int64) :: found64, expected64
    real(real32), allocatable :: volume32(:), track_volume32(:)
    real(real32) :: real_param32(4), eps_converge32(5)
    real(real32) :: leakage32(NGRP)
    real(real32), allocatable :: nusigf32(:,:,:), chi32(:,:,:)
    real(real32), allocatable :: q32(:,:), zero_nusigf32(:)
    real(real32) :: qint32(NGRP), keff32
    real(real64) :: iter_keff64, rho64, plane_rho64
    real(real64), allocatable :: phi64(:,:), q64(:,:)
    real(real64) :: qint64(NGRP), mirror_first_integral64
    real(real64) :: fis64, product64, contribution64
    logical, allocatable :: seen_unknown(:)
    character(len=12) :: signature, lifecycle_state
    type(c_ptr) :: tracks, libraries, fluxes
    type(c_ptr) :: probe_track
    type(c_ptr) :: input_track, input_library, input_flux
    type(c_ptr) :: input_macro, input_groups, input_group
    type(c_ptr) :: root_authority, plane_authority, authority_flux
    type(c_ptr) :: output_groups, output_group
    type(c_ptr) :: source_outer, source_inner
    type(c_ptr) :: source_authority, qfiss_list

    status = SPOR64_BOOTQ64_PREFLIGHT_FAILED
    input_roots=[ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem, &
                 ipaxmacro,iparchive,ipcontract]
    do alias_index=1,size(input_roots)
      if (c_associated(ipmacro_out,input_roots(alias_index))) return
      if (c_associated(ipsource_out,input_roots(alias_index))) return
    enddo
    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax, &
        ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract, &
        contract,context_ok)
    if (.not.context_ok) return
    call LCMGET(ipglobal,'NORM64',norm64)

    ! Both products are new in-memory LCM objects.  They cannot alias each
    ! other or the immutable B2l PROJECTED/e archive.
    if (.not. c_associated(ipprojected)) return
    if (.not. c_associated(ipmacro_out)) return
    if (.not. c_associated(ipsource_out)) return
    if (c_associated(ipprojected,ipmacro_out)) return
    if (c_associated(ipprojected,ipsource_out)) return
    if (c_associated(ipmacro_out,ipsource_out)) return
    if (plane_index < 1 .or. plane_index > NSNAP) return
    if (.not. EMPTY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_ROOT(ipsource_out)) return

    ! Admit exactly one B2l PROJECTED/e root.  RHO is authoritative and must
    ! be the bitwise result of the stated reciprocal, not an independent
    ! caller parameter.
    if (.not. PROJECTED_ARCHIVE_ROOT_IS_EXACT(ipprojected)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipprojected,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipprojected,'LISTDIM',1,1)) return
    call LCMGET(ipprojected,'LISTDIM',root_planes)
    if (root_planes /= NSNAP) return
    if (.not. RECORD_MATCHES(ipprojected,'SPOT-ITER-K',1,4)) return
    call LCMGET(ipprojected,'SPOT-ITER-K',iter_keff64)
    if (.not. ieee_is_finite(iter_keff64)) return
    if (iter_keff64 <= +0.0_real64) return
    if (iter_keff64 > REAL32_MAX64) return
    keff32 = real(iter_keff64,real32)
    if (.not. ieee_is_finite(keff32)) return
    if (keff32 <= +0.0_real32) return

    if (.not. RECORD_MATCHES(ipprojected,'SPOT-R64',-1,0)) return
    root_authority = LCMGID(ipprojected,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',4,16, &
        'PROJECTED-BOOT')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(rho64)) return
    if (rho64 <= +0.0_real64) return
    if (root_planes /= NSNAP) return
    if (root_epoch /= 0) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/iter_keff64,0_int64)
    if (found64 /= expected64) return

    if (.not. RECORD_MATCHES(ipprojected,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipprojected,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipprojected,'FLUX',NSNAP,10)) return
    tracks = LCMGID(ipprojected,'TRACK')
    libraries = LCMGID(ipprojected,'MICROLIB2')
    fluxes = LCMGID(ipprojected,'FLUX')
    if (.not. c_associated(tracks)) return
    if (.not. c_associated(libraries)) return
    if (.not. c_associated(fluxes)) return
    archive_track_state = 0
    archive_mccg_state = 0
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
      probe_track = LCMGIL(tracks,ip)
      if (.not. c_associated(probe_track)) return
      if (.not. RECORD_MATCHES(probe_track,'STATE-VECTOR',NSTATE,1)) &
          return
      call LCMGET(probe_track,'STATE-VECTOR',probe_track_state)
      probe_nsurf = probe_track_state(5)
      if (probe_track_state(1) <= 0 .or. probe_track_state(2) <= 0 .or. &
          probe_track_state(4) <= 0 .or. probe_nsurf <= 0) return
      if (probe_track_state(3) /= 1 .or. &
          probe_track_state(6) /= TRACK_ACTIVE_COMPONENTS) return
      if (int(probe_track_state(2),int64) /= &
          int(probe_track_state(1),int64)+int(probe_nsurf,int64)) return
      if (ip == 1) then
        archive_track_state = probe_track_state
        nsurf = probe_nsurf
      else
        if (probe_track_state(1) /= archive_track_state(1) .or. &
            probe_track_state(2) /= archive_track_state(2) .or. &
            probe_track_state(4) /= archive_track_state(4) .or. &
            probe_nsurf /= nsurf) return
      end if
      if (.not. RECORD_MATCHES(probe_track,'V$MCCG', &
          probe_track_state(2),2)) return
      if (.not. RECORD_MATCHES(probe_track,'NZON$MCCG', &
          probe_track_state(2),1)) return
      if (.not. RECORD_MATCHES(probe_track,'KEYCUR$MCCG',nsurf,1)) return
      if (.not. RECORD_MATCHES(probe_track,'MCCG-STATE',NSTATE,1)) return
      call LCMGET(probe_track,'MCCG-STATE',probe_mccg_state)
      if (probe_mccg_state(5) <= 0 .or. probe_mccg_state(6) <= 0) return
      if (probe_mccg_state(10) /= 3 .and. &
          probe_mccg_state(10) /= 4) return
      if (probe_mccg_state(10) == 3) then
        if (probe_mccg_state(17) <= 0) return
        if (.not. RECORD_MATCHES(probe_track,'IM0$MCCG', &
            probe_track_state(2)+1,1)) return
        if (.not. RECORD_MATCHES(probe_track,'MCU0$MCCG', &
            probe_mccg_state(17),1)) return
      else
        if (probe_mccg_state(17) /= 0) return
        if (.not. ABSENT_RECORD(probe_track,'IM0$MCCG')) return
        if (.not. ABSENT_RECORD(probe_track,'MCU0$MCCG')) return
      end if
      if (ip == 1) then
        archive_mccg_state = probe_mccg_state
      else
        if (any(probe_mccg_state([5,6,10,17]) /= &
            archive_mccg_state([5,6,10,17]))) return
      end if
      if (.not. RECORD_MATCHES(probe_track,'MCU$MCCG', &
          probe_mccg_state(6),1)) return
    end do
    input_track = LCMGIL(tracks,plane_index)
    input_library = LCMGIL(libraries,plane_index)
    input_flux = LCMGIL(fluxes,plane_index)
    if (.not. c_associated(input_track)) return
    if (.not. c_associated(input_library)) return
    if (.not. c_associated(input_flux)) return

    ! Fix the selected radial material/unknown map before reading either
    ! microscopic fission data or the plane flux authority.
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'TRACK-TYPE',3,12, &
        'MCCG')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'LINK.FTRACK',3,12, &
        'TRACK_f')) return
    if (.not. RECORD_MATCHES(input_track,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_track,'STATE-VECTOR',track_state)
    nreg = track_state(1)
    nunkno = track_state(2)
    nmat = track_state(4)
    if (nreg /= archive_track_state(1) .or. &
        nunkno /= archive_track_state(2) .or. &
        nmat /= archive_track_state(4)) return
    if (nreg <= 0 .or. nunkno <= 0 .or. nmat <= 0) return
    if (track_state(3) /= 1) return
    if (track_state(5) /= nsurf .or. &
        track_state(6) /= TRACK_ACTIVE_COMPONENTS) return
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) return
    if (int(nmat,int64)*int(NIFIS,int64) > &
        int(huge(nmat),int64)) return
    if (track_state(9) /= 0 .or. track_state(14) /= 4) return
    if (track_state(16) /= 2 .or. track_state(22) /= 1) return
    if (track_state(27) < 0 .or. track_state(39) /= 0) return
    if (track_state(40) /= 0) return
    if (.not. RECORD_MATCHES(input_track,'MCCG-STATE',NSTATE,1)) return
    call LCMGET(input_track,'MCCG-STATE',mccg_state)
    if (mccg_state(5) <= 0 .or. mccg_state(6) <= 0) return
    if (any(mccg_state(5:6) /= archive_mccg_state(5:6))) return
    if (any(mccg_state(1:4) /= MCCG_STATE_EXPECTED(1:4))) return
    if (any(mccg_state(7:9) /= MCCG_STATE_EXPECTED(7:9))) return
    if (any(mccg_state(11:16) /= MCCG_STATE_EXPECTED(11:16))) return
    if (any(mccg_state(18:NSTATE) /= &
        MCCG_STATE_EXPECTED(18:NSTATE))) return
    if (mccg_state(10) /= archive_mccg_state(10) .or. &
        mccg_state(17) /= archive_mccg_state(17)) return
    if (.not. RECORD_MATCHES(input_track,'REAL-PARAM',4,2)) return
    call LCMGET(input_track,'REAL-PARAM',real_param32)
    if (.not. all(ieee_is_finite(real_param32))) return
    if (transfer(real_param32(1),0_int32) /= &
        contract%eps_mccg_bits) return
    if (any(transfer(real_param32(2:4),0_int32,3) /= 0_int32)) return
    if (.not. RECORD_MATCHES(input_track,'VOLUME',nreg,2)) return
    if (.not. RECORD_MATCHES(input_track,'V$MCCG',nunkno,2)) return
    if (.not. RECORD_MATCHES(input_track,'MATCOD',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'NZON$MCCG',nunkno,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX$ANIS',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYCUR$MCCG',nsurf,1)) return
    allocate(matcod(nreg),nzon(nunkno),keyflx(nreg),keyanis(nreg), &
        keycur(nsurf),imerge(nmat),volume32(nreg), &
        track_volume32(nunkno),seen_unknown(nunkno), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(input_track,'VOLUME',volume32)
    allocate(volume64(nreg),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(input_flux,'VOLUME64',volume64)
    call LCMGET(input_track,'V$MCCG',track_volume32)
    call LCMGET(input_track,'MATCOD',matcod)
    call LCMGET(input_track,'NZON$MCCG',nzon)
    call LCMGET(input_track,'KEYFLX',keyflx)
    call LCMGET(input_track,'KEYFLX$ANIS',keyanis)
    call LCMGET(input_track,'KEYCUR$MCCG',keycur)
    if (.not. all(ieee_is_finite(volume32))) return
    if (.not. all(ieee_is_finite(track_volume32))) return
    if (any(volume32 <= +0.0_real32)) return
    if (any(track_volume32 <= +0.0_real32)) return
    if (any(matcod < 1) .or. any(matcod > nmat)) return
    if (any(nzon(1:nreg) /= matcod)) return
    if (any(nzon(nreg+1:nunkno) < -NCODE)) return
    if (any(nzon(nreg+1:nunkno) > -1)) return
    do ir = 1, nreg
      volume_bits = transfer(volume32(ir),0_int32)
      track_volume_bits = transfer(track_volume32(ir),0_int32)
      if (volume_bits /= track_volume_bits) return
    end do
    if (any(keyflx /= keyanis)) return
    if (any(keyflx < 1) .or. any(keyflx > nunkno)) return
    if (any(keycur < 1) .or. any(keycur > nunkno)) return
    seen_unknown = .false.
    do ir = 1, nreg
      if (seen_unknown(keyflx(ir))) return
      seen_unknown(keyflx(ir)) = .true.
    end do
    do ir = 1, nsurf
      if (seen_unknown(keycur(ir))) return
      seen_unknown(keycur(ir)) = .true.
    end do
    if (.not. all(seen_unknown)) return

    ! The same-index MICROLIB2 supplies one L_MACROLIB.  All fission data
    ! are staged as binary32, checked, and promoted only at the arithmetic
    ! operation where they enter the REAL64 source definition.
    if (.not. CHARACTER_RECORD_MATCHES(input_library,'SIGNATURE',3,12, &
        'L_LIBRARY')) return
    if (.not. RECORD_MATCHES(input_library,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_library,'STATE-VECTOR',library_state)
    if (library_state(1) /= nmat) return
    if (library_state(2) <= 0) return
    if (library_state(3) /= NGRP) return
    if (library_state(4) /= 3) return
    if (.not. RECORD_MATCHES(input_library,'MACROLIB',-1,0)) return
    input_macro = LCMGID(input_library,'MACROLIB')
    if (.not. c_associated(input_macro)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_macro,'SIGNATURE',3,12, &
        'L_MACROLIB')) return
    if (.not. RECORD_MATCHES(input_macro,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_macro,'STATE-VECTOR',macro_state)
    macro_state_expected = 0
    macro_state_expected(1:7) = [NGRP,nmat,3,NIFIS,18,2,6]
    if (any(macro_state /= macro_state_expected)) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-FROZEN')) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-KEFF')) return
    if (.not. RECORD_MATCHES(input_macro,'GROUP',NGRP,10)) return
    input_groups = LCMGID(input_macro,'GROUP')
    if (.not. c_associated(input_groups)) return
    allocate(nusigf32(nmat,NIFIS,NGRP),chi32(nmat,NIFIS,NGRP), &
        q32(nunkno,NGRP),zero_nusigf32(nmat*NIFIS), &
        phi64(nunkno,NGRP),q64(nunkno,NGRP), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    do g = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(input_groups,g)) return
      input_group = LCMGIL(input_groups,g)
      if (.not. c_associated(input_group)) return
      if (.not. RECORD_MATCHES(input_group,'NUSIGF',nmat*NIFIS,2)) return
      if (.not. RECORD_MATCHES(input_group,'CHI',nmat*NIFIS,2)) return
      call LCMGET(input_group,'NUSIGF',nusigf32(:,:,g))
      call LCMGET(input_group,'CHI',chi32(:,:,g))
      if (.not. all(ieee_is_finite(nusigf32(:,:,g)))) return
      if (.not. all(ieee_is_finite(chi32(:,:,g)))) return
      if (any(nusigf32(:,:,g) < +0.0_real32)) return
      if (any(chi32(:,:,g) < +0.0_real32)) return
    end do

    ! The plane root is PROJECTED/e and contains no source.  Its root FLUX
    ! is only a legacy mirror: no value is read from that binary32 list.
    if (.not. PROJECTED_PLANE_ROOT_IS_EXACT(input_flux)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(input_flux,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_flux,'STATE-VECTOR',flux_state)
    if (any(flux_state(1:7) /= [NGRP,nunkno,1,0,0,0,0])) return
    if (flux_state(8) /= contract%flu_acce_free .or. &
        flux_state(9) /= contract%flu_acce_accel) return
    if (flux_state(10) /= 1) return
    if (flux_state(11) /= contract%flu_maxinr .or. &
        flux_state(12) /= contract%flu_maxout) return
    if (any(flux_state(13:16) /= 0)) return
    if (flux_state(17) /= nmat .or. flux_state(18) /= 1) return
    if (any(flux_state(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(input_flux,'EPS-CONVERGE',5,2)) return
    call LCMGET(input_flux,'EPS-CONVERGE',eps_converge32)
    if (.not. all(ieee_is_finite(eps_converge32))) return
    do g = 1, 3
      if (transfer(eps_converge32(g),0_int32) /= &
          contract%eps_radial_bits) return
    end do
    do g = 4, 5
      if (transfer(eps_converge32(g),0_int32) /= 0_int32) return
    end do
    if (.not. RECORD_MATCHES(input_flux,'IMERGE-LEAK',nmat,1)) return
    call LCMGET(input_flux,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(input_flux,'KEYFLX',nreg,1)) return
    call LCMGET(input_flux,'KEYFLX',keyanis)
    if (any(keyanis /= keyflx)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'OPTION',1,4, &
        contract%flu_option)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(input_flux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(input_flux,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(input_flux,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) return

    if (.not. RECORD_MATCHES(input_flux,'SPOT-R64',-1,0)) return
    plane_authority = LCMGID(input_flux,'SPOT-R64')
    if (.not. c_associated(plane_authority)) return
    if (.not. PROJECTED_AUTHORITY_IS_EXACT(plane_authority)) return
    if (.not. RECORD_MATCHES(plane_authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(plane_authority,'STATE',4,16, &
        'PROJECTED-BOOT')) return
    if (.not. RECORD_MATCHES(plane_authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(plane_authority,'FLUX',NGRP,10)) return
    call LCMGET(plane_authority,'RHO',plane_rho64)
    call LCMGET(plane_authority,'EPOCH',plane_epoch)
    if (.not. ieee_is_finite(plane_rho64)) return
    if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return
    if (plane_epoch /= root_epoch) return
    authority_flux = LCMGID(plane_authority,'FLUX')
    if (.not. c_associated(authority_flux)) return
    do h = 1, NGRP
      call LCMLEL(authority_flux,h,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 4) return
      call LCMGDL(authority_flux,h,phi64(:,h))
      if (.not. all(ieee_is_finite(phi64(:,h)))) return
    end do
    do ir = 1, nreg
      do h = 1, NGRP
        if (phi64(keyflx(ir),h) <= +0.0_real64) return
      end do
    end do

    ! This scalar loop nest is the numerical definition.  It deliberately
    ! separates multiplication from addition, and never assumes FMA,
    ! reassociation, a reduction intrinsic, clipping, or normalization.
    q64 = +0.0_real64
    do ir = 1, nreg
      im = matcod(ir)
      iu = keyflx(ir)
      do ifis = 1, NIFIS
        fis64 = +0.0_real64
        do h = 1, NGRP
          product64 = real(nusigf32(im,ifis,h),real64) * phi64(iu,h)
          fis64 = fis64 + product64
        end do
        if (.not. ieee_is_finite(fis64)) return
        do g = 1, NGRP
          contribution64 = real(chi32(im,ifis,g),real64) * fis64
          contribution64 = contribution64 * rho64
          if (.not. ieee_is_finite(contribution64)) return
          q64(iu,g) = q64(iu,g) + contribution64
          if (.not. ieee_is_finite(q64(iu,g))) return
        end do
      end do
    end do
    if (.not. all(ieee_is_finite(q64))) return
    if (any(q64 < +0.0_real64)) return
    if (any(q64 > REAL32_MAX64)) return

    qint64 = +0.0_real64
    do g = 1, NGRP
      do ir = 1, nreg
        product64 = volume64(ir) * q64(keyflx(ir),g)
        qint64(g) = qint64(g) + product64
      end do
    end do
    if (.not. all(ieee_is_finite(qint64))) return
    if (any(qint64 < +0.0_real64)) return
    if (qint64(1) <= +0.0_real64) return
    if (any(qint64 > REAL32_MAX64)) return

    ! These are the only compatibility conversions.  The type-4 QFISS
    ! authority remains q64; DSOUR and SPOT-QINT are one-time mirrors.
    q32 = real(q64,real32)
    qint32 = real(qint64,real32)
    if (.not. all(ieee_is_finite(q32))) return
    if (.not. all(ieee_is_finite(qint32))) return
    if (any(q32 < +0.0_real32)) return
    if (any(qint32 < +0.0_real32)) return
    if (qint32(1) <= +0.0_real32) return
    mirror_first_integral64 = +0.0_real64
    do ir = 1, nreg
      product64 = volume64(ir) * &
          real(q32(keyflx(ir),1),real64)
      mirror_first_integral64 = mirror_first_integral64 + product64
    end do
    if (.not. ieee_is_finite(mirror_first_integral64)) return
    if (mirror_first_integral64 <= +0.0_real64) return

    ! Complete preflight precedes the first output mutation.  Repeating both
    ! freshness checks closes the caller-visible time-of-check window.
    if (.not. EMPTY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_ROOT(ipsource_out)) return

    ! MACRO0 is a recursive copy of the selected macrolib.  Its only changed
    ! physical records are all NUSIGF arrays, set to positive numerical zero
    ! so the fixed QFISS source cannot be counted a second time by FLU.
    call LCMEQU(input_macro,ipmacro_out)
    zero_nusigf32 = +0.0_real32
    output_groups = LCMGID(ipmacro_out,'GROUP')
    if (.not. c_associated(output_groups)) &
        call XABORT('SPOR64_BOOTQ64: OUTPUT MACRO GROUP LIST MISSING.')
    do g = 1, NGRP
      output_group = LCMGIL(output_groups,g)
      if (.not. c_associated(output_group)) &
          call XABORT('SPOR64_BOOTQ64: OUTPUT MACRO GROUP MISSING.')
      call LCMPUT(output_group,'NUSIGF',nmat*NIFIS,2,zero_nusigf32)
    end do
    call LCMPUT(ipmacro_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipmacro_out,'SPOT-KEFF',1,2,keff32)

    signature = 'L_SOURCE'
    call LCMPTC(ipsource_out,'SIGNATURE',12,signature)
    source_state = 0
    source_state(1:3) = [NGRP,nunkno,1]
    call LCMPUT(ipsource_out,'STATE-VECTOR',NSTATE,1,source_state)
    call LCMPUT(ipsource_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipsource_out,'SPOT-KEFF',1,2,keff32)
    call LCMPUT(ipsource_out,'SPOT-QINT',NGRP,2,qint32)
    source_outer = LCMLID(ipsource_out,'DSOUR',1)
    if (.not. c_associated(source_outer)) &
        call XABORT('SPOR64_BOOTQ64: DSOUR OUTER LIST CREATION FAILED.')
    source_inner = LCMLIL(source_outer,1,NGRP)
    if (.not. c_associated(source_inner)) &
        call XABORT('SPOR64_BOOTQ64: DSOUR INNER LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(source_inner,g,nunkno,2,q32(:,g))
    end do

    source_authority = LCMDID(ipsource_out,'SPOT-R64')
    if (.not. c_associated(source_authority)) &
        call XABORT('SPOR64_BOOTQ64: SOURCE AUTHORITY CREATION FAILED.')
    call LCMPUT(source_authority,'RHO',1,4,rho64)
    call LCMPUT(source_authority,'PLANE',1,1,plane_index)
    lifecycle_state = 'FROZEN-QFIS'
    call LCMPTC(source_authority,'STATE',12,lifecycle_state)
    call LCMPUT(source_authority,'NORM',1,4,norm64)
    child=LCMDID(source_authority,'GLOBAL64')
    call LCMEQU(ipglobal,child)
    child=LCMDID(source_authority,'SEED')
    call LCMEQU(input_flux,child)
    qfiss_list = LCMLID(source_authority,'QFISS',NGRP)
    if (.not. c_associated(qfiss_list)) &
        call XABORT('SPOR64_BOOTQ64: QFISS LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(qfiss_list,g,nunkno,4,q64(:,g))
    end do

    child=LCMLID(ipsource_out,'ROOT-QFISS64',NGRP)
    do g=1,NGRP
      call LCMPDL(child,g,nunkno,4,q64(:,g))
    enddo

    ! EPOCH is the source-wide commit and the final output mutation.
    call LCMPUT(source_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_BOOTQ64_COMMITTED
  end subroutine SPOR64_BOOTQ64_BUILD
  logical function PROJECTED_ARCHIVE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    PROJECTED_ARCHIVE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,BOOT_ARCHIVE_NAMES)
  end function PROJECTED_ARCHIVE_ROOT_IS_EXACT


  logical function ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,SCHEMA_ARCHIVE_ROOT_AUTHORITY)
  end function ROOT_AUTHORITY_IS_EXACT


  logical function PROJECTED_PLANE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    PROJECTED_PLANE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,BOOT_PLANE_NAMES)
  end function PROJECTED_PLANE_ROOT_IS_EXACT


  logical function PROJECTED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist

    PROJECTED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,BOOT_PLANE_AUTH_NAMES)
  end function PROJECTED_AUTHORITY_IS_EXACT

  ! Independent read-back recomputes the entire physical source from the supplied
  ! global/canonical/seed inputs. Internal copies alone cannot authorize inputs.
  subroutine SPOR64_BOOTQ64_READ(ipprojected,ipglobal,ipax,ipaxtrack, &
      ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index,ipmacro, &
      ipsource,q64,rho64,status)
    type(c_ptr), intent(in) :: ipprojected,ipglobal,ipax,ipaxtrack
    type(c_ptr), intent(in) :: ipaxsystem,ipaxmacro,iparchive,ipcontract
    type(c_ptr), intent(in) :: ipmacro,ipsource
    integer, intent(in) :: plane_index
    real(real64), allocatable, intent(out) :: q64(:,:)
    real(real64), intent(out) :: rho64
    integer, intent(out) :: status
    type(c_ptr) :: staged_macro,staged_source,source_auth,typed_source
    type(c_ptr) :: original_fluxes,original_seed
    integer :: build_status,state(NSTATE),g,ilong,itylcm,istat
    logical :: same_macro,same_source,stage_exists
    status=SPOR64_BOOTQ64_PREFLIGHT_FAILED
    rho64=0.0_real64
    if (.not.c_associated(ipmacro).or..not.c_associated(ipsource)) return
    ! Private disk-backed expected records use two immutable context views.
    ! The host owns a fresh exclusive cwd; existing files are always refused.
    inquire(file='BQ64-MAC-ST',exist=stage_exists)
    if (stage_exists) return
    inquire(file='BQ64-SRC-ST',exist=stage_exists)
    if (stage_exists) return
    call LCMOP(staged_macro,'BQ64-MAC-ST',0,2,0)
    call LCMOP(staged_source,'BQ64-SRC-ST',0,2,0)
    call BQ64_BUILD_COMPACT_EXPECTED(ipprojected,ipglobal,ipax,ipaxtrack, &
        ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
        staged_macro,staged_source,build_status)
    same_macro=.false.
    same_source=.false.
    if (build_status == SPOR64_BOOTQ64_COMMITTED) then
      same_macro=SPOR64_BOOT64_SAME_TREE(staged_macro,ipmacro)
      original_fluxes=LCMGID(ipprojected,'FLUX')
      original_seed=LCMGIL(original_fluxes,plane_index)
      same_source=BQ64_SAME_COMPOSED_SOURCE(staged_source,ipsource, &
          ipglobal,original_seed)
    endif
    call LCMCL(staged_source,2)
    call LCMCL(staged_macro,2)
    if (.not.same_macro.or..not.same_source) return
    call LCMGET(ipsource,'STATE-VECTOR',state)
    allocate(q64(state(2),NGRP),stat=istat)
    if (istat /= 0) return
    typed_source=LCMGID(ipsource,'ROOT-QFISS64')
    do g=1,NGRP
      call LCMLEL(typed_source,g,ilong,itylcm)
      if (ilong /= state(2).or.itylcm /= 4) then
        deallocate(q64)
        return
      endif
      call LCMGDL(typed_source,g,q64(:,g))
    enddo
    source_auth=LCMGID(ipsource,'SPOT-R64')
    call LCMGET(source_auth,'RHO',rho64)
    status=SPOR64_BOOTQ64_LOADED
  end subroutine SPOR64_BOOTQ64_READ

  subroutine BQ64_BUILD_COMPACT_EXPECTED(ipprojected,ipglobal,ipax,ipaxtrack, &
      ipaxsystem,ipaxmacro,iparchive,ipcontract,plane_index, &
      ipmacro_out,ipsource_out,status)
    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out
    type(c_ptr), intent(in) :: ipglobal,ipax,ipaxtrack,ipaxsystem
    type(c_ptr), intent(in) :: ipaxmacro,iparchive,ipcontract
    type(SPOR64_ROUTE_CONTRACT) :: contract
    logical :: context_ok
    type(c_ptr) :: input_roots(8), child
    integer :: alias_index
    real(real64) :: norm64
    real(real64), allocatable :: volume64(:)
    integer, intent(in) :: plane_index
    integer, intent(out) :: status

    integer :: root_planes, root_epoch, plane_epoch
    integer :: track_state(NSTATE), mccg_state(NSTATE)
    integer :: archive_track_state(NSTATE), probe_track_state(NSTATE)
    integer :: archive_mccg_state(NSTATE), probe_mccg_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: macro_state_expected(NSTATE)
    integer :: flux_state(NSTATE), source_state(NSTATE)
    integer, allocatable :: matcod(:), nzon(:)
    integer, allocatable :: keyflx(:), keyanis(:), keycur(:)
    integer, allocatable :: imerge(:)
    integer :: ip, ir, ifis, h, g, im, iu, ilong, itylcm
    integer :: allocation_status, nreg, nunkno, nmat, nsurf, probe_nsurf
    integer(int32) :: volume_bits, track_volume_bits
    integer(int64) :: found64, expected64
    real(real32), allocatable :: volume32(:), track_volume32(:)
    real(real32) :: real_param32(4), eps_converge32(5)
    real(real32) :: leakage32(NGRP)
    real(real32), allocatable :: nusigf32(:,:,:), chi32(:,:,:)
    real(real32), allocatable :: q32(:,:), zero_nusigf32(:)
    real(real32) :: qint32(NGRP), keff32
    real(real64) :: iter_keff64, rho64, plane_rho64
    real(real64), allocatable :: phi64(:,:), q64(:,:)
    real(real64) :: qint64(NGRP), mirror_first_integral64
    real(real64) :: fis64, product64, contribution64
    logical, allocatable :: seen_unknown(:)
    character(len=12) :: signature, lifecycle_state
    type(c_ptr) :: tracks, libraries, fluxes
    type(c_ptr) :: probe_track
    type(c_ptr) :: input_track, input_library, input_flux
    type(c_ptr) :: input_macro, input_groups, input_group
    type(c_ptr) :: root_authority, plane_authority, authority_flux
    type(c_ptr) :: output_groups, output_group
    type(c_ptr) :: source_outer, source_inner
    type(c_ptr) :: source_authority, qfiss_list

    status = SPOR64_BOOTQ64_PREFLIGHT_FAILED
    input_roots=[ipprojected,ipglobal,ipax,ipaxtrack,ipaxsystem, &
                 ipaxmacro,iparchive,ipcontract]
    do alias_index=1,size(input_roots)
      if (c_associated(ipmacro_out,input_roots(alias_index))) return
      if (c_associated(ipsource_out,input_roots(alias_index))) return
    enddo
    call SPOR64_BOOT_CONTEXT64_READ(ipprojected,ipglobal,ipax, &
        ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract, &
        contract,context_ok)
    if (.not.context_ok) return
    call LCMGET(ipglobal,'NORM64',norm64)

    ! Both products are new in-memory LCM objects.  They cannot alias each
    ! other or the immutable B2l PROJECTED/e archive.
    if (.not. c_associated(ipprojected)) return
    if (.not. c_associated(ipmacro_out)) return
    if (.not. c_associated(ipsource_out)) return
    if (c_associated(ipprojected,ipmacro_out)) return
    if (c_associated(ipprojected,ipsource_out)) return
    if (c_associated(ipmacro_out,ipsource_out)) return
    if (plane_index < 1 .or. plane_index > NSNAP) return
    if (.not. EMPTY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_ROOT(ipsource_out)) return

    ! Admit exactly one B2l PROJECTED/e root.  RHO is authoritative and must
    ! be the bitwise result of the stated reciprocal, not an independent
    ! caller parameter.
    if (.not. PROJECTED_ARCHIVE_ROOT_IS_EXACT(ipprojected)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipprojected,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipprojected,'LISTDIM',1,1)) return
    call LCMGET(ipprojected,'LISTDIM',root_planes)
    if (root_planes /= NSNAP) return
    if (.not. RECORD_MATCHES(ipprojected,'SPOT-ITER-K',1,4)) return
    call LCMGET(ipprojected,'SPOT-ITER-K',iter_keff64)
    if (.not. ieee_is_finite(iter_keff64)) return
    if (iter_keff64 <= +0.0_real64) return
    if (iter_keff64 > REAL32_MAX64) return
    keff32 = real(iter_keff64,real32)
    if (.not. ieee_is_finite(keff32)) return
    if (keff32 <= +0.0_real32) return

    if (.not. RECORD_MATCHES(ipprojected,'SPOT-R64',-1,0)) return
    root_authority = LCMGID(ipprojected,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',4,16, &
        'PROJECTED-BOOT')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(rho64)) return
    if (rho64 <= +0.0_real64) return
    if (root_planes /= NSNAP) return
    if (root_epoch /= 0) return
    found64 = transfer(rho64,0_int64)
    expected64 = transfer(1.0_real64/iter_keff64,0_int64)
    if (found64 /= expected64) return

    if (.not. RECORD_MATCHES(ipprojected,'TRACK',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipprojected,'MICROLIB2',NSNAP,10)) return
    if (.not. RECORD_MATCHES(ipprojected,'FLUX',NSNAP,10)) return
    tracks = LCMGID(ipprojected,'TRACK')
    libraries = LCMGID(ipprojected,'MICROLIB2')
    fluxes = LCMGID(ipprojected,'FLUX')
    if (.not. c_associated(tracks)) return
    if (.not. c_associated(libraries)) return
    if (.not. c_associated(fluxes)) return
    archive_track_state = 0
    archive_mccg_state = 0
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
      probe_track = LCMGIL(tracks,ip)
      if (.not. c_associated(probe_track)) return
      if (.not. RECORD_MATCHES(probe_track,'STATE-VECTOR',NSTATE,1)) &
          return
      call LCMGET(probe_track,'STATE-VECTOR',probe_track_state)
      probe_nsurf = probe_track_state(5)
      if (probe_track_state(1) <= 0 .or. probe_track_state(2) <= 0 .or. &
          probe_track_state(4) <= 0 .or. probe_nsurf <= 0) return
      if (probe_track_state(3) /= 1 .or. &
          probe_track_state(6) /= TRACK_ACTIVE_COMPONENTS) return
      if (int(probe_track_state(2),int64) /= &
          int(probe_track_state(1),int64)+int(probe_nsurf,int64)) return
      if (ip == 1) then
        archive_track_state = probe_track_state
        nsurf = probe_nsurf
      else
        if (probe_track_state(1) /= archive_track_state(1) .or. &
            probe_track_state(2) /= archive_track_state(2) .or. &
            probe_track_state(4) /= archive_track_state(4) .or. &
            probe_nsurf /= nsurf) return
      end if
      if (.not. RECORD_MATCHES(probe_track,'V$MCCG', &
          probe_track_state(2),2)) return
      if (.not. RECORD_MATCHES(probe_track,'NZON$MCCG', &
          probe_track_state(2),1)) return
      if (.not. RECORD_MATCHES(probe_track,'KEYCUR$MCCG',nsurf,1)) return
      if (.not. RECORD_MATCHES(probe_track,'MCCG-STATE',NSTATE,1)) return
      call LCMGET(probe_track,'MCCG-STATE',probe_mccg_state)
      if (probe_mccg_state(5) <= 0 .or. probe_mccg_state(6) <= 0) return
      if (probe_mccg_state(10) /= 3 .and. &
          probe_mccg_state(10) /= 4) return
      if (probe_mccg_state(10) == 3) then
        if (probe_mccg_state(17) <= 0) return
        if (.not. RECORD_MATCHES(probe_track,'IM0$MCCG', &
            probe_track_state(2)+1,1)) return
        if (.not. RECORD_MATCHES(probe_track,'MCU0$MCCG', &
            probe_mccg_state(17),1)) return
      else
        if (probe_mccg_state(17) /= 0) return
        if (.not. ABSENT_RECORD(probe_track,'IM0$MCCG')) return
        if (.not. ABSENT_RECORD(probe_track,'MCU0$MCCG')) return
      end if
      if (ip == 1) then
        archive_mccg_state = probe_mccg_state
      else
        if (any(probe_mccg_state([5,6,10,17]) /= &
            archive_mccg_state([5,6,10,17]))) return
      end if
      if (.not. RECORD_MATCHES(probe_track,'MCU$MCCG', &
          probe_mccg_state(6),1)) return
    end do
    input_track = LCMGIL(tracks,plane_index)
    input_library = LCMGIL(libraries,plane_index)
    input_flux = LCMGIL(fluxes,plane_index)
    if (.not. c_associated(input_track)) return
    if (.not. c_associated(input_library)) return
    if (.not. c_associated(input_flux)) return

    ! Fix the selected radial material/unknown map before reading either
    ! microscopic fission data or the plane flux authority.
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'SIGNATURE',3,12, &
        'L_TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'TRACK-TYPE',3,12, &
        'MCCG')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_track,'LINK.FTRACK',3,12, &
        'TRACK_f')) return
    if (.not. RECORD_MATCHES(input_track,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_track,'STATE-VECTOR',track_state)
    nreg = track_state(1)
    nunkno = track_state(2)
    nmat = track_state(4)
    if (nreg /= archive_track_state(1) .or. &
        nunkno /= archive_track_state(2) .or. &
        nmat /= archive_track_state(4)) return
    if (nreg <= 0 .or. nunkno <= 0 .or. nmat <= 0) return
    if (track_state(3) /= 1) return
    if (track_state(5) /= nsurf .or. &
        track_state(6) /= TRACK_ACTIVE_COMPONENTS) return
    if (int(nunkno,int64) /= int(nreg,int64)+int(nsurf,int64)) return
    if (int(nmat,int64)*int(NIFIS,int64) > &
        int(huge(nmat),int64)) return
    if (track_state(9) /= 0 .or. track_state(14) /= 4) return
    if (track_state(16) /= 2 .or. track_state(22) /= 1) return
    if (track_state(27) < 0 .or. track_state(39) /= 0) return
    if (track_state(40) /= 0) return
    if (.not. RECORD_MATCHES(input_track,'MCCG-STATE',NSTATE,1)) return
    call LCMGET(input_track,'MCCG-STATE',mccg_state)
    if (mccg_state(5) <= 0 .or. mccg_state(6) <= 0) return
    if (any(mccg_state(5:6) /= archive_mccg_state(5:6))) return
    if (any(mccg_state(1:4) /= MCCG_STATE_EXPECTED(1:4))) return
    if (any(mccg_state(7:9) /= MCCG_STATE_EXPECTED(7:9))) return
    if (any(mccg_state(11:16) /= MCCG_STATE_EXPECTED(11:16))) return
    if (any(mccg_state(18:NSTATE) /= &
        MCCG_STATE_EXPECTED(18:NSTATE))) return
    if (mccg_state(10) /= archive_mccg_state(10) .or. &
        mccg_state(17) /= archive_mccg_state(17)) return
    if (.not. RECORD_MATCHES(input_track,'REAL-PARAM',4,2)) return
    call LCMGET(input_track,'REAL-PARAM',real_param32)
    if (.not. all(ieee_is_finite(real_param32))) return
    if (transfer(real_param32(1),0_int32) /= &
        contract%eps_mccg_bits) return
    if (any(transfer(real_param32(2:4),0_int32,3) /= 0_int32)) return
    if (.not. RECORD_MATCHES(input_track,'VOLUME',nreg,2)) return
    if (.not. RECORD_MATCHES(input_track,'V$MCCG',nunkno,2)) return
    if (.not. RECORD_MATCHES(input_track,'MATCOD',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'NZON$MCCG',nunkno,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX$ANIS',nreg,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYCUR$MCCG',nsurf,1)) return
    allocate(matcod(nreg),nzon(nunkno),keyflx(nreg),keyanis(nreg), &
        keycur(nsurf),imerge(nmat),volume32(nreg), &
        track_volume32(nunkno),seen_unknown(nunkno), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(input_track,'VOLUME',volume32)
    allocate(volume64(nreg),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(input_flux,'VOLUME64',volume64)
    call LCMGET(input_track,'V$MCCG',track_volume32)
    call LCMGET(input_track,'MATCOD',matcod)
    call LCMGET(input_track,'NZON$MCCG',nzon)
    call LCMGET(input_track,'KEYFLX',keyflx)
    call LCMGET(input_track,'KEYFLX$ANIS',keyanis)
    call LCMGET(input_track,'KEYCUR$MCCG',keycur)
    if (.not. all(ieee_is_finite(volume32))) return
    if (.not. all(ieee_is_finite(track_volume32))) return
    if (any(volume32 <= +0.0_real32)) return
    if (any(track_volume32 <= +0.0_real32)) return
    if (any(matcod < 1) .or. any(matcod > nmat)) return
    if (any(nzon(1:nreg) /= matcod)) return
    if (any(nzon(nreg+1:nunkno) < -NCODE)) return
    if (any(nzon(nreg+1:nunkno) > -1)) return
    do ir = 1, nreg
      volume_bits = transfer(volume32(ir),0_int32)
      track_volume_bits = transfer(track_volume32(ir),0_int32)
      if (volume_bits /= track_volume_bits) return
    end do
    if (any(keyflx /= keyanis)) return
    if (any(keyflx < 1) .or. any(keyflx > nunkno)) return
    if (any(keycur < 1) .or. any(keycur > nunkno)) return
    seen_unknown = .false.
    do ir = 1, nreg
      if (seen_unknown(keyflx(ir))) return
      seen_unknown(keyflx(ir)) = .true.
    end do
    do ir = 1, nsurf
      if (seen_unknown(keycur(ir))) return
      seen_unknown(keycur(ir)) = .true.
    end do
    if (.not. all(seen_unknown)) return

    ! The same-index MICROLIB2 supplies one L_MACROLIB.  All fission data
    ! are staged as binary32, checked, and promoted only at the arithmetic
    ! operation where they enter the REAL64 source definition.
    if (.not. CHARACTER_RECORD_MATCHES(input_library,'SIGNATURE',3,12, &
        'L_LIBRARY')) return
    if (.not. RECORD_MATCHES(input_library,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_library,'STATE-VECTOR',library_state)
    if (library_state(1) /= nmat) return
    if (library_state(2) <= 0) return
    if (library_state(3) /= NGRP) return
    if (library_state(4) /= 3) return
    if (.not. RECORD_MATCHES(input_library,'MACROLIB',-1,0)) return
    input_macro = LCMGID(input_library,'MACROLIB')
    if (.not. c_associated(input_macro)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_macro,'SIGNATURE',3,12, &
        'L_MACROLIB')) return
    if (.not. RECORD_MATCHES(input_macro,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_macro,'STATE-VECTOR',macro_state)
    macro_state_expected = 0
    macro_state_expected(1:7) = [NGRP,nmat,3,NIFIS,18,2,6]
    if (any(macro_state /= macro_state_expected)) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-FROZEN')) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-KEFF')) return
    if (.not. RECORD_MATCHES(input_macro,'GROUP',NGRP,10)) return
    input_groups = LCMGID(input_macro,'GROUP')
    if (.not. c_associated(input_groups)) return
    allocate(nusigf32(nmat,NIFIS,NGRP),chi32(nmat,NIFIS,NGRP), &
        q32(nunkno,NGRP),zero_nusigf32(nmat*NIFIS), &
        phi64(nunkno,NGRP),q64(nunkno,NGRP), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    do g = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(input_groups,g)) return
      input_group = LCMGIL(input_groups,g)
      if (.not. c_associated(input_group)) return
      if (.not. RECORD_MATCHES(input_group,'NUSIGF',nmat*NIFIS,2)) return
      if (.not. RECORD_MATCHES(input_group,'CHI',nmat*NIFIS,2)) return
      call LCMGET(input_group,'NUSIGF',nusigf32(:,:,g))
      call LCMGET(input_group,'CHI',chi32(:,:,g))
      if (.not. all(ieee_is_finite(nusigf32(:,:,g)))) return
      if (.not. all(ieee_is_finite(chi32(:,:,g)))) return
      if (any(nusigf32(:,:,g) < +0.0_real32)) return
      if (any(chi32(:,:,g) < +0.0_real32)) return
    end do

    ! The plane root is PROJECTED/e and contains no source.  Its root FLUX
    ! is only a legacy mirror: no value is read from that binary32 list.
    if (.not. PROJECTED_PLANE_ROOT_IS_EXACT(input_flux)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(input_flux,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_flux,'STATE-VECTOR',flux_state)
    if (any(flux_state(1:7) /= [NGRP,nunkno,1,0,0,0,0])) return
    if (flux_state(8) /= contract%flu_acce_free .or. &
        flux_state(9) /= contract%flu_acce_accel) return
    if (flux_state(10) /= 1) return
    if (flux_state(11) /= contract%flu_maxinr .or. &
        flux_state(12) /= contract%flu_maxout) return
    if (any(flux_state(13:16) /= 0)) return
    if (flux_state(17) /= nmat .or. flux_state(18) /= 1) return
    if (any(flux_state(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(input_flux,'EPS-CONVERGE',5,2)) return
    call LCMGET(input_flux,'EPS-CONVERGE',eps_converge32)
    if (.not. all(ieee_is_finite(eps_converge32))) return
    do g = 1, 3
      if (transfer(eps_converge32(g),0_int32) /= &
          contract%eps_radial_bits) return
    end do
    do g = 4, 5
      if (transfer(eps_converge32(g),0_int32) /= 0_int32) return
    end do
    if (.not. RECORD_MATCHES(input_flux,'IMERGE-LEAK',nmat,1)) return
    call LCMGET(input_flux,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(input_flux,'KEYFLX',nreg,1)) return
    call LCMGET(input_flux,'KEYFLX',keyanis)
    if (any(keyanis /= keyflx)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'OPTION',1,4, &
        contract%flu_option)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(input_flux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(input_flux,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(input_flux,'SPOT-LEAK1D',leakage32)
    if (.not. all(ieee_is_finite(leakage32))) return

    if (.not. RECORD_MATCHES(input_flux,'SPOT-R64',-1,0)) return
    plane_authority = LCMGID(input_flux,'SPOT-R64')
    if (.not. c_associated(plane_authority)) return
    if (.not. PROJECTED_AUTHORITY_IS_EXACT(plane_authority)) return
    if (.not. RECORD_MATCHES(plane_authority,'RHO',1,4)) return
    if (.not. CHARACTER_RECORD_MATCHES(plane_authority,'STATE',4,16, &
        'PROJECTED-BOOT')) return
    if (.not. RECORD_MATCHES(plane_authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(plane_authority,'FLUX',NGRP,10)) return
    call LCMGET(plane_authority,'RHO',plane_rho64)
    call LCMGET(plane_authority,'EPOCH',plane_epoch)
    if (.not. ieee_is_finite(plane_rho64)) return
    if (transfer(plane_rho64,0_int64) /= transfer(rho64,0_int64)) return
    if (plane_epoch /= root_epoch) return
    authority_flux = LCMGID(plane_authority,'FLUX')
    if (.not. c_associated(authority_flux)) return
    do h = 1, NGRP
      call LCMLEL(authority_flux,h,ilong,itylcm)
      if (ilong /= nunkno .or. itylcm /= 4) return
      call LCMGDL(authority_flux,h,phi64(:,h))
      if (.not. all(ieee_is_finite(phi64(:,h)))) return
    end do
    do ir = 1, nreg
      do h = 1, NGRP
        if (phi64(keyflx(ir),h) <= +0.0_real64) return
      end do
    end do

    ! This scalar loop nest is the numerical definition.  It deliberately
    ! separates multiplication from addition, and never assumes FMA,
    ! reassociation, a reduction intrinsic, clipping, or normalization.
    q64 = +0.0_real64
    do ir = 1, nreg
      im = matcod(ir)
      iu = keyflx(ir)
      do ifis = 1, NIFIS
        fis64 = +0.0_real64
        do h = 1, NGRP
          product64 = real(nusigf32(im,ifis,h),real64) * phi64(iu,h)
          fis64 = fis64 + product64
        end do
        if (.not. ieee_is_finite(fis64)) return
        do g = 1, NGRP
          contribution64 = real(chi32(im,ifis,g),real64) * fis64
          contribution64 = contribution64 * rho64
          if (.not. ieee_is_finite(contribution64)) return
          q64(iu,g) = q64(iu,g) + contribution64
          if (.not. ieee_is_finite(q64(iu,g))) return
        end do
      end do
    end do
    if (.not. all(ieee_is_finite(q64))) return
    if (any(q64 < +0.0_real64)) return
    if (any(q64 > REAL32_MAX64)) return

    qint64 = +0.0_real64
    do g = 1, NGRP
      do ir = 1, nreg
        product64 = volume64(ir) * q64(keyflx(ir),g)
        qint64(g) = qint64(g) + product64
      end do
    end do
    if (.not. all(ieee_is_finite(qint64))) return
    if (any(qint64 < +0.0_real64)) return
    if (qint64(1) <= +0.0_real64) return
    if (any(qint64 > REAL32_MAX64)) return

    ! These are the only compatibility conversions.  The type-4 QFISS
    ! authority remains q64; DSOUR and SPOT-QINT are one-time mirrors.
    q32 = real(q64,real32)
    qint32 = real(qint64,real32)
    if (.not. all(ieee_is_finite(q32))) return
    if (.not. all(ieee_is_finite(qint32))) return
    if (any(q32 < +0.0_real32)) return
    if (any(qint32 < +0.0_real32)) return
    if (qint32(1) <= +0.0_real32) return
    mirror_first_integral64 = +0.0_real64
    do ir = 1, nreg
      product64 = volume64(ir) * &
          real(q32(keyflx(ir),1),real64)
      mirror_first_integral64 = mirror_first_integral64 + product64
    end do
    if (.not. ieee_is_finite(mirror_first_integral64)) return
    if (mirror_first_integral64 <= +0.0_real64) return

    ! Complete preflight precedes the first output mutation.  Repeating both
    ! freshness checks closes the caller-visible time-of-check window.
    if (.not. EMPTY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_ROOT(ipsource_out)) return

    ! Only a fresh compact expected tree receives this storage-bound gate.
    if (.not.COMPACT_EXPECTED_STORAGE_FITS(nunkno)) return

    ! MACRO0 is a recursive copy of the selected macrolib.  Its only changed
    ! physical records are all NUSIGF arrays, set to positive numerical zero
    ! so the fixed QFISS source cannot be counted a second time by FLU.
    call LCMEQU(input_macro,ipmacro_out)
    zero_nusigf32 = +0.0_real32
    output_groups = LCMGID(ipmacro_out,'GROUP')
    if (.not. c_associated(output_groups)) &
        call XABORT('SPOR64_BOOTQ64: OUTPUT MACRO GROUP LIST MISSING.')
    do g = 1, NGRP
      output_group = LCMGIL(output_groups,g)
      if (.not. c_associated(output_group)) &
          call XABORT('SPOR64_BOOTQ64: OUTPUT MACRO GROUP MISSING.')
      call LCMPUT(output_group,'NUSIGF',nmat*NIFIS,2,zero_nusigf32)
    end do
    call LCMPUT(ipmacro_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipmacro_out,'SPOT-KEFF',1,2,keff32)

    signature = 'L_SOURCE'
    call LCMPTC(ipsource_out,'SIGNATURE',12,signature)
    source_state = 0
    source_state(1:3) = [NGRP,nunkno,1]
    call LCMPUT(ipsource_out,'STATE-VECTOR',NSTATE,1,source_state)
    call LCMPUT(ipsource_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipsource_out,'SPOT-KEFF',1,2,keff32)
    call LCMPUT(ipsource_out,'SPOT-QINT',NGRP,2,qint32)
    source_outer = LCMLID(ipsource_out,'DSOUR',1)
    if (.not. c_associated(source_outer)) &
        call XABORT('SPOR64_BOOTQ64: DSOUR OUTER LIST CREATION FAILED.')
    source_inner = LCMLIL(source_outer,1,NGRP)
    if (.not. c_associated(source_inner)) &
        call XABORT('SPOR64_BOOTQ64: DSOUR INNER LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(source_inner,g,nunkno,2,q32(:,g))
    end do

    source_authority = LCMDID(ipsource_out,'SPOT-R64')
    if (.not. c_associated(source_authority)) &
        call XABORT('SPOR64_BOOTQ64: SOURCE AUTHORITY CREATION FAILED.')
    call LCMPUT(source_authority,'RHO',1,4,rho64)
    call LCMPUT(source_authority,'PLANE',1,1,plane_index)
    lifecycle_state = 'FROZEN-QFIS'
    call LCMPTC(source_authority,'STATE',12,lifecycle_state)
    call LCMPUT(source_authority,'NORM',1,4,norm64)
    child=LCMDID(source_authority,'GLOBAL64')
    child=LCMDID(source_authority,'SEED')
    qfiss_list = LCMLID(source_authority,'QFISS',NGRP)
    if (.not. c_associated(qfiss_list)) &
        call XABORT('SPOR64_BOOTQ64: QFISS LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(qfiss_list,g,nunkno,4,q64(:,g))
    end do

    child=LCMLID(ipsource_out,'ROOT-QFISS64',NGRP)
    do g=1,NGRP
      call LCMPDL(child,g,nunkno,4,q64(:,g))
    enddo

    ! EPOCH is the source-wide commit and the final output mutation.
    call LCMPUT(source_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_BOOTQ64_COMMITTED
  end subroutine BQ64_BUILD_COMPACT_EXPECTED

  logical function COMPACT_EXPECTED_STORAGE_FITS(nunkno)
    integer, intent(in) :: nunkno
    integer(int64) :: required_bytes
    COMPACT_EXPECTED_STORAGE_FITS = .false.
    if (nunkno <= 0) return
    required_bytes = COMPACT_FIXED_BYTES + &
        COMPACT_BYTES_PER_UNKNOWN*int(nunkno,int64)
    COMPACT_EXPECTED_STORAGE_FITS = required_bytes <= COMPACT_STORAGE_CAP
  end function COMPACT_EXPECTED_STORAGE_FITS

  ! Exactly two empty expected placeholders are resolved to immutable inputs.
  ! Every resolved subtree then uses the original full raw tree comparison.
  logical function BQ64_SAME_COMPOSED_SOURCE(left,right,ipglobal,ipseed)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer :: nodes, visited(2)
    logical :: equal
    nodes = 0
    visited = 0
    BQ64_SAME_COMPOSED_SOURCE = .false.
    if (.not.c_associated(left).or..not.c_associated(right)) return
    if (.not.c_associated(ipglobal).or..not.c_associated(ipseed)) return
    equal = BQ64_COMPOSED_NODE(left,right,0,nodes,VIEW_ROOT, &
        ipglobal,ipseed,visited)
    BQ64_SAME_COMPOSED_SOURCE = equal.and.all(visited == 1)
  end function BQ64_SAME_COMPOSED_SOURCE

  recursive logical function BQ64_COMPOSED_NODE(left,right,depth,nodes, &
      view,ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: depth,view
    integer, intent(inout) :: nodes,visited(2)
    type(c_ptr) :: resolved_left
    character(len=72) :: file_name
    character(len=12) :: object_name
    integer :: slot,extent,next_view
    logical :: empty,medium
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not.c_associated(left).or..not.c_associated(right)) return
    resolved_left = left
    next_view = view
    if (view == VIEW_GLOBAL.or.view == VIEW_SEED) then
      if (depth /= 2) return
      slot = view-1
      if (visited(slot) /= 0) return
      ! The parent has already compared both directory type/length metadata.
      call LCMINF(left,file_name,object_name,empty,extent,medium)
      if (.not.empty.or.extent /= -1) return
      if (view == VIEW_GLOBAL) then
        resolved_left = ipglobal
      else
        resolved_left = ipseed
      endif
      if (.not.c_associated(resolved_left)) return
      visited(slot) = 1
      next_view = VIEW_NONE
    else if (view == VIEW_ROOT) then
      if (depth /= 0) return
    else if (view == VIEW_AUTH) then
      if (depth /= 1) return
    else if (view /= VIEW_NONE) then
      return
    endif
    ! This call compares empty flags, inventories, extents and all raw words
    ! after resolution, with the original cumulative depth and shared nodes.
    equal = BQ64_SAME_DIRECTORY(resolved_left,right,depth,nodes,next_view, &
        ipglobal,ipseed,visited)
  end function BQ64_COMPOSED_NODE

  recursive logical function BQ64_SAME_DIRECTORY(left,right,depth,nodes, &
      view,ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: depth,view
    integer, intent(inout) :: nodes,visited(2)
    integer :: child_view
    character(len=72) :: file_name
    character(len=12) :: object_name, item_name, first_name
    integer :: left_extent, right_extent, count_left, count_right
    integer :: length_left, type_left, length_right, type_right
    logical :: left_empty, right_empty, medium
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    call LCMINF(left,file_name,object_name,left_empty,left_extent,medium)
    call LCMINF(right,file_name,object_name,right_empty,right_extent,medium)
    if (left_extent /= -1 .or. right_extent /= -1) return
    if (left_empty .neqv. right_empty) return
    if (left_empty) then
      equal = .true.
      return
    end if
    item_name = ' '
    call LCMNXT(left,item_name)
    first_name = item_name
    count_left = 0
    do
      nodes = nodes+1
      count_left = count_left+1
      if (nodes > MAX_NODES .or. item_name == ' ') return
      call LCMLEN(left,item_name,length_left,type_left)
      call LCMLEN(right,item_name,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        child_view = VIEW_NONE
        if (view == VIEW_ROOT.and.depth == 0.and.item_name == 'SPOT-R64') then
          child_view = VIEW_AUTH
        else if (view == VIEW_AUTH.and.depth == 1) then
          if (item_name == 'GLOBAL64') child_view = VIEW_GLOBAL
          if (item_name == 'SEED') child_view = VIEW_SEED
        endif
        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &
            child_view,ipglobal,ipseed,visited)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &
            ipglobal,ipseed,visited)) return
      else
        if (.not. BQ64_SAME_RECORD(left,right,item_name,0,length_left,type_left)) return
      end if
      call LCMNXT(left,item_name)
      if (item_name == first_name) exit
    end do
    item_name = ' '
    call LCMNXT(right,item_name)
    first_name = item_name
    count_right = 0
    do
      count_right = count_right+1
      if (count_right > MAX_NODES .or. item_name == ' ') return
      call LCMNXT(right,item_name)
      if (item_name == first_name) exit
    end do
    equal = count_left == count_right
  end function BQ64_SAME_DIRECTORY

  recursive logical function BQ64_SAME_LIST(left,right,extent,depth,nodes, &
      ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: extent, depth
    integer, intent(inout) :: nodes,visited(2)
    integer :: index, length_left, type_left, length_right, type_right
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH .or. extent <= 0) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    do index = 1, extent
      nodes = nodes+1
      if (nodes > MAX_NODES) return
      call LCMLEL(left,index,length_left,type_left)
      call LCMLEL(right,index,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 99 .and. length_left == 0) cycle
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &
            VIEW_NONE,ipglobal,ipseed,visited)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &
            ipglobal,ipseed,visited)) return
      else
        if (.not. BQ64_SAME_RECORD(left,right,' ',index,length_left,type_left)) return
      end if
    end do
    equal = .true.
  end function BQ64_SAME_LIST

  logical function BQ64_SAME_RECORD(left,right,name,index,length,type_code)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: index, length, type_code
    integer(int64) :: words64
    integer :: words, allocation_status
    integer, allocatable :: left_bits(:), right_bits(:)
    BQ64_SAME_RECORD = .false.
    if (length <= 0 .or. type_code < 1 .or. type_code > 6) return
    words64 = int(length,int64)
    if (type_code == 4 .or. type_code == 6) words64 = 2_int64*words64
    if (words64 > int(MAX_RECORD_WORDS,int64)) return
    words = int(words64)
    allocate(left_bits(words),right_bits(words),stat=allocation_status)
    if (allocation_status /= 0) return
    ! GANLIB's GET wrappers copy raw words without coercion. The allocated
    ! buffer is two int32 words per REAL64/complex value, one for other types.
    if (index == 0) then
      call LCMGET(left,name,left_bits)
      call LCMGET(right,name,right_bits)
    else
      call LCMGDL(left,index,left_bits)
      call LCMGDL(right,index,right_bits)
    end if
    BQ64_SAME_RECORD = all(left_bits == right_bits)
  end function BQ64_SAME_RECORD

end module SPOR64_BOOTQ64_V2
