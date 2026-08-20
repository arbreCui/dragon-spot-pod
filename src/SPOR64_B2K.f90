module SPOR64_B2K
  use, intrinsic :: iso_c_binding, only : c_associated, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  implicit none
  private

  integer, parameter, public :: SPOR64_B2K_ADMISSION_FAILED = 1
  integer, parameter, public :: SPOR64_B2K_ARCHIVE_ASSEMBLED = 2

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NREG = 8
  integer, parameter :: NSNAP = 3
  integer, parameter :: NUNKNO = 14
  integer, parameter :: NMAT = 8
  integer, parameter :: NSOUT = 6
  integer, parameter :: NIFIS = 32
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  integer(int32), parameter :: MCCG_EPSI_BITS = int(z'3727c5ac',int32)
  real(real64), parameter :: REAL32_MAX64 = real(huge(0.0_real32),real64)
  integer, parameter :: TRACK_STATE_EXPECTED(NSTATE) = &
      [NREG,NUNKNO,1,NMAT,6,1,4,0,0,0,48,1,-1,4,1,2, &
       165,100000,11364,96, &
       96,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: MCCG_STATE_EXPECTED(NSTATE) = &
      [-1,4,10,0,17,32,80,0,0,4,0,0,20,1,1,1,0,0,1,1, &
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: MACRO_STATE_EXPECTED(NSTATE) = &
      [NGRP,NMAT,3,NIFIS,18,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0, &
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: kind_guard = 1 / merge(1,0, &
      kind(1.0) == real32 .and. kind(0.0d0) == real64)

  public :: SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE

contains

  subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(ipout,ipprojected, &
      ipsystems,status)
    type(c_ptr), intent(in) :: ipout, ipprojected, ipsystems(NSNAP)
    integer, intent(out) :: status

    integer :: root_planes, root_epoch, plane_epoch
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: track_state(NSTATE), mccg_state(NSTATE)
    integer :: keyflx(NREG), keyanis(NREG), keycur(NSOUT)
    integer :: matcod(NREG), nzon(NUNKNO)
    integer :: ip, ir
    integer(int64) :: found64, expected64
    integer(int32) :: volume_bits, track_volume_bits
    real(real32) :: volume32(NREG), volume_track32(NUNKNO)
    real(real32) :: leakage32(NGRP), real_param32(4)
    real(real64) :: rho64, plane_rho64, iter_keff64
    character(len=12) :: signature, lifecycle_state
    logical :: seen_unknown(NUNKNO)
    type(c_ptr) :: root_authority, plane_authority
    type(c_ptr) :: tracks, libraries, fluxes
    type(c_ptr) :: input_track(NSNAP), input_library(NSNAP)
    type(c_ptr) :: input_flux(NSNAP), input_macro(NSNAP)
    integer :: probe_ilong, probe_itylcm
    logical :: unreduced_mode
    type(c_ptr) :: output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes, output_item
    type(c_ptr) :: staged_system(NSNAP), staged_authority

    status = SPOR64_B2K_ADMISSION_FAILED
    staged_system = c_null_ptr

    ! This boundary has no loose leakage, RHO, epoch, or numerical control.
    ! Every physical value is recovered from one committed B2j
    ! archive, while every response matrix is supplied by a fresh host ASM.
    if (.not. c_associated(ipout)) return
    if (.not. c_associated(ipprojected)) return
    do ip = 1, NSNAP
      if (.not. c_associated(ipsystems(ip))) return
    end do
    if (c_associated(ipout,ipprojected)) return
    do ip = 1, NSNAP
      if (c_associated(ipout,ipsystems(ip))) return
      if (c_associated(ipprojected,ipsystems(ip))) return
    end do
    do ip = 1, NSNAP-1
      do ir = ip+1, NSNAP
        if (c_associated(ipsystems(ip),ipsystems(ir))) return
      end do
    end do
    if (.not. EMPTY_LCM_ROOT(ipout)) return

    ! Admit exactly the root published by B2j: PROJECTED/e has no SYSTEM.
    if (.not. PROJECTED_ARCHIVE_ROOT_IS_EXACT(ipprojected)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipprojected,'SIGNATURE',3,12, &
        'L_ARCHIVE')) return
    if (.not. RECORD_MATCHES(ipprojected,'LISTDIM',1,1)) return
    call LCMGET(ipprojected,'LISTDIM',root_planes)
    if (root_planes /= NSNAP) return
    if (.not. RECORD_MATCHES(ipprojected,'SPOT-ITER-K',1,4)) return
    call LCMGET(ipprojected,'SPOT-ITER-K',iter_keff64)
    if (.not. ieee_is_finite(iter_keff64) .or. &
        iter_keff64 <= +0.0_real64) return
    if (.not. RECORD_MATCHES(ipprojected,'SPOT-R64',-1,0)) return
    root_authority = LCMGID(ipprojected,'SPOT-R64')
    if (.not. c_associated(root_authority)) return
    if (.not. ROOT_AUTHORITY_IS_EXACT(root_authority)) return
    if (.not. RECORD_MATCHES(root_authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(root_authority,'NPLANE',1,1)) return
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(rho64) .or. rho64 <= +0.0_real64) return
    if (root_planes /= NSNAP .or. root_epoch <= 0) return
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

    ! Establish every same-index TRACK/MICROLIB2/FLUX/SYSTEM tuple before
    ! opening a private stage.  The SYSTEM checks are a strict posterior of
    ! the host ASM binary32 operation order, not a replacement builder.
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
      input_track(ip) = LCMGIL(tracks,ip)
      input_library(ip) = LCMGIL(libraries,ip)
      input_flux(ip) = LCMGIL(fluxes,ip)
      if (.not. c_associated(input_track(ip))) return
      if (.not. c_associated(input_library(ip))) return
      if (.not. c_associated(input_flux(ip))) return

      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'SIGNATURE', &
          3,12,'L_TRACK')) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip),'TRACK-TYPE', &
          3,12,'MCCG')) return
      if (.not. RECORD_MATCHES(input_track(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_track(ip),'STATE-VECTOR',track_state)
      if (any(track_state /= TRACK_STATE_EXPECTED)) return
      if (.not. RECORD_MATCHES(input_track(ip),'MCCG-STATE', &
          NSTATE,1)) return
      call LCMGET(input_track(ip),'MCCG-STATE',mccg_state)
      if (any(mccg_state /= MCCG_STATE_EXPECTED)) return
      if (.not. RECORD_MATCHES(input_track(ip),'REAL-PARAM',4,2)) return
      call LCMGET(input_track(ip),'REAL-PARAM',real_param32)
      if (.not. all(ieee_is_finite(real_param32))) return
      if (transfer(real_param32(1),0_int32) /= MCCG_EPSI_BITS) return
      if (any(transfer(real_param32(2:4),0_int32,3) /= 0_int32)) return
      if (.not. CHARACTER_RECORD_MATCHES(input_track(ip), &
          'LINK.FTRACK',3,12,'TRACK_f')) return
      if (.not. RECORD_MATCHES(input_track(ip),'VOLUME',NREG,2)) return
      if (.not. RECORD_MATCHES(input_track(ip),'V$MCCG',NUNKNO,2)) return
      if (.not. RECORD_MATCHES(input_track(ip),'MATCOD',NREG,1)) return
      if (.not. RECORD_MATCHES(input_track(ip),'NZON$MCCG',NUNKNO,1)) &
          return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX',NREG,1)) return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYFLX$ANIS',NREG,1)) &
          return
      if (.not. RECORD_MATCHES(input_track(ip),'KEYCUR$MCCG',NSOUT,1)) &
          return
      call LCMGET(input_track(ip),'VOLUME',volume32)
      call LCMGET(input_track(ip),'V$MCCG',volume_track32)
      call LCMGET(input_track(ip),'MATCOD',matcod)
      call LCMGET(input_track(ip),'NZON$MCCG',nzon)
      call LCMGET(input_track(ip),'KEYFLX',keyflx)
      call LCMGET(input_track(ip),'KEYFLX$ANIS',keyanis)
      call LCMGET(input_track(ip),'KEYCUR$MCCG',keycur)
      if (.not. all(ieee_is_finite(volume32))) return
      if (.not. all(ieee_is_finite(volume_track32))) return
      if (any(volume32 <= +0.0_real32)) return
      if (any(volume_track32 <= +0.0_real32)) return
      if (any(matcod < 1) .or. any(matcod > NMAT)) return
      if (any(nzon(1:NREG) /= matcod)) return
      if (any(nzon(NREG+1:NUNKNO) < -NSOUT)) return
      if (any(nzon(NREG+1:NUNKNO) > -1)) return
      do ir = 1, NREG
        volume_bits = transfer(volume32(ir),0_int32)
        track_volume_bits = transfer(volume_track32(ir),0_int32)
        if (volume_bits /= track_volume_bits) return
      end do
      if (any(keyflx /= keyanis)) return
      if (any(keyflx < 1) .or. any(keyflx > NUNKNO)) return
      if (any(keycur < 1) .or. any(keycur > NUNKNO)) return
      seen_unknown = .false.
      do ir = 1, NREG
        if (seen_unknown(keyflx(ir))) return
        seen_unknown(keyflx(ir)) = .true.
      end do
      do ir = 1, NSOUT
        if (seen_unknown(keycur(ir))) return
        seen_unknown(keycur(ir)) = .true.
      end do
      if (.not. all(seen_unknown)) return

      if (.not. CHARACTER_RECORD_MATCHES(input_library(ip), &
          'SIGNATURE',3,12,'L_LIBRARY')) return
      if (.not. RECORD_MATCHES(input_library(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_library(ip),'STATE-VECTOR',library_state)
      if (library_state(1) /= NMAT .or. library_state(2) <= 0) return
      if (library_state(3) /= NGRP .or. library_state(4) /= 3) return
      if (.not. RECORD_MATCHES(input_library(ip),'MACROLIB',-1,0)) &
          return
      input_macro(ip) = LCMGID(input_library(ip),'MACROLIB')
      if (.not. c_associated(input_macro(ip))) return
      if (.not. CHARACTER_RECORD_MATCHES(input_macro(ip),'SIGNATURE', &
          3,12,'L_MACROLIB')) return
      if (.not. RECORD_MATCHES(input_macro(ip),'STATE-VECTOR', &
          NSTATE,1)) return
      call LCMGET(input_macro(ip),'STATE-VECTOR',macro_state)
      if (any(macro_state /= MACRO_STATE_EXPECTED)) return
      if (.not. RECORD_MATCHES(input_macro(ip),'GROUP',NGRP,10)) return

      if (.not. PROJECTED_PLANE_IS_EXACT(input_flux(ip),rho64, &
          root_epoch,keyflx,leakage32)) return
      plane_authority = LCMGID(input_flux(ip),'SPOT-R64')
      call LCMGET(plane_authority,'RHO',plane_rho64)
      call LCMGET(plane_authority,'EPOCH',plane_epoch)
      if (transfer(plane_rho64,0_int64) /= &
          transfer(rho64,0_int64)) return
      if (plane_epoch /= root_epoch) return

      if (.not. ABSENT_RECORD(ipsystems(ip),'SPOT-R64')) return
      if (.not. ABSENT_RECORD(ipsystems(ip),'B2I-SENT')) return
      if (.not. ABSENT_RECORD(ipsystems(ip),'B2I-DEEP')) return
      if (.not. CANDIDATE_SYSTEM_ROOT_IS_EXACT(ipsystems(ip))) return
      call LCMLEN(input_flux(ip),'LEAK1D64',probe_ilong,probe_itylcm)
      unreduced_mode = (probe_ilong == NGRP .and. probe_itylcm == 4)
      if (probe_ilong /= 0 .and. .not. unreduced_mode) return
      if (.not. SYSTEM_PAYLOAD_IS_VALID(ipsystems(ip),input_macro(ip), &
          leakage32,ip,unreduced_mode)) return
    end do

    ! Preserve each complete host system in a private LCM stage.  Only the
    ! lifecycle directory is added; PJJ and ACA response records remain the
    ! exact recursive LCMEQU copy produced by the real host ASM call.
    do ip = 1, NSNAP
      call OPEN_STAGE(staged_system(ip),ip)
      call LCMEQU(ipsystems(ip),staged_system(ip))
      staged_authority = LCMDID(staged_system(ip),'SPOT-R64')
      if (.not. c_associated(staged_authority)) &
          call XABORT('SPOR64_B2K: SYSTEM AUTHORITY CREATION FAILED.')
      lifecycle_state = 'ASSEMBLED'
      call LCMPUT(staged_authority,'RHO',1,4,rho64)
      call LCMPTC(staged_authority,'STATE',12,lifecycle_state)
      call LCMPUT(staged_authority,'EPOCH',1,1,root_epoch)

      call LCMGET(input_flux(ip),'SPOT-LEAK1D',leakage32)
      if (.not. STAGED_SYSTEM_ROOT_IS_EXACT(staged_system(ip))) then
        call CLOSE_STAGES(staged_system)
        return
      end if
      call LCMLEN(input_flux(ip),'LEAK1D64',probe_ilong,probe_itylcm)
      unreduced_mode = (probe_ilong == NGRP .and. probe_itylcm == 4)
      if (probe_ilong /= 0 .and. .not. unreduced_mode) then
        call CLOSE_STAGES(staged_system)
        return
      end if
      if (.not. SYSTEM_PAYLOAD_IS_VALID(staged_system(ip), &
          input_macro(ip),leakage32,ip,unreduced_mode)) then
        call CLOSE_STAGES(staged_system)
        return
      end if
      if (.not. SYSTEM_AUTHORITY_IS_COMMITTED(staged_system(ip), &
          rho64,root_epoch)) then
        call CLOSE_STAGES(staged_system)
        return
      end if
    end do

    ! This repeat is immediately before the first caller-visible mutation.
    if (.not. EMPTY_LCM_ROOT(ipout)) then
      call CLOSE_STAGES(staged_system)
      return
    end if

    signature = 'L_ARCHIVE'
    call LCMPTC(ipout,'SIGNATURE',12,signature)
    call LCMPUT(ipout,'LISTDIM',1,1,root_planes)
    call LCMPUT(ipout,'SPOT-ITER-K',1,4,iter_keff64)
    output_tracks = LCMLID(ipout,'TRACK',NSNAP)
    output_libraries = LCMLID(ipout,'MICROLIB2',NSNAP)
    output_systems = LCMLID(ipout,'SYSTEM',NSNAP)
    output_fluxes = LCMLID(ipout,'FLUX',NSNAP)
    if (.not. c_associated(output_tracks)) &
        call XABORT('SPOR64_B2K: OUTPUT TRACK LIST CREATION FAILED.')
    if (.not. c_associated(output_libraries)) &
        call XABORT('SPOR64_B2K: OUTPUT LIBRARY LIST CREATION FAILED.')
    if (.not. c_associated(output_systems)) &
        call XABORT('SPOR64_B2K: OUTPUT SYSTEM LIST CREATION FAILED.')
    if (.not. c_associated(output_fluxes)) &
        call XABORT('SPOR64_B2K: OUTPUT FLUX LIST CREATION FAILED.')
    do ip = 1, NSNAP
      output_item = LCMDIL(output_tracks,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2K: OUTPUT TRACK ITEM CREATION FAILED.')
      call LCMEQU(input_track(ip),output_item)
      output_item = LCMDIL(output_libraries,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2K: OUTPUT LIBRARY ITEM CREATION FAILED.')
      call LCMEQU(input_library(ip),output_item)
      output_item = LCMDIL(output_systems,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2K: OUTPUT SYSTEM ITEM CREATION FAILED.')
      call LCMEQU(staged_system(ip),output_item)
      output_item = LCMDIL(output_fluxes,ip)
      if (.not. c_associated(output_item)) &
          call XABORT('SPOR64_B2K: OUTPUT FLUX ITEM CREATION FAILED.')
      call LCMEQU(input_flux(ip),output_item)
    end do
    call CLOSE_STAGES(staged_system)

    ! Root EPOCH is the archive-wide commit and the final output mutation.
    root_authority = LCMDID(ipout,'SPOT-R64')
    if (.not. c_associated(root_authority)) &
        call XABORT('SPOR64_B2K: ROOT AUTHORITY CREATION FAILED.')
    lifecycle_state = 'ASSEMBLED'
    call LCMPUT(root_authority,'RHO',1,4,rho64)
    call LCMPUT(root_authority,'NPLANE',1,1,root_planes)
    call LCMPTC(root_authority,'STATE',12,lifecycle_state)
    call LCMPUT(root_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_B2K_ARCHIVE_ASSEMBLED
  end subroutine SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE


  logical function PROJECTED_PLANE_IS_EXACT(ipflux,rho,epoch, &
      expected_keyflx,leakage)
    type(c_ptr), intent(in) :: ipflux
    real(real64), intent(in) :: rho
    integer, intent(in) :: epoch
    integer, intent(in) :: expected_keyflx(NREG)
    real(real32), intent(out) :: leakage(NGRP)

    integer :: ig, ilong, itylcm, found_epoch
    integer :: state(NSTATE), imerge(NMAT), keyflx(NREG)
    integer(int32) :: found32
    real(real32) :: eps_converge(5)
    real(real32) :: mirror32(NUNKNO)
    real(real64) :: authority64(NUNKNO), found_rho
    type(c_ptr) :: authority, authority_flux, mirror_flux

    PROJECTED_PLANE_IS_EXACT = .false.
    if (.not. PROJECTED_PLANE_ROOT_IS_EXACT(ipflux)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'SIGNATURE',3,12, &
        'L_FLUX')) return
    if (.not. RECORD_MATCHES(ipflux,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipflux,'STATE-VECTOR',state)
    if (any(state(1:18) /= &
        [NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500,0,0,0,0,NMAT,1])) return
    if (any(state(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(ipflux,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipflux,'EPS-CONVERGE',eps_converge)
    if (.not. all(ieee_is_finite(eps_converge))) return
    do ig = 1, 3
      found32 = transfer(eps_converge(ig),0_int32)
      if (found32 /= FROZEN_TOL_BITS) return
    end do
    do ig = 4, 5
      found32 = transfer(eps_converge(ig),0_int32)
      if (found32 /= 0_int32) return
    end do
    if (.not. RECORD_MATCHES(ipflux,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(ipflux,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(ipflux,'KEYFLX',NREG,1)) return
    call LCMGET(ipflux,'KEYFLX',keyflx)
    if (any(keyflx /= expected_keyflx)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'OPTION',1,4,'B0  ')) &
        return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipflux,'LINK.SYSTEM',3,12, &
        'SYSTEM')) return
    if (.not. RECORD_MATCHES(ipflux,'SPOT-R64',-1,0)) return
    authority = LCMGID(ipflux,'SPOT-R64')
    if (.not. c_associated(authority)) return
    if (.not. PROJECTED_AUTHORITY_IS_EXACT(authority)) return
    if (.not. CHARACTER_RECORD_MATCHES(authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(authority,'RHO',1,4)) return
    if (.not. RECORD_MATCHES(authority,'EPOCH',1,1)) return
    if (.not. RECORD_MATCHES(authority,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'FLUX',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipflux,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'EPOCH',found_epoch)
    call LCMGET(ipflux,'SPOT-LEAK1D',leakage)
    if (.not. ieee_is_finite(found_rho)) return
    if (transfer(found_rho,0_int64) /= transfer(rho,0_int64)) return
    if (found_epoch /= epoch) return
    if (.not. all(ieee_is_finite(leakage))) return
    authority_flux = LCMGID(authority,'FLUX')
    mirror_flux = LCMGID(ipflux,'FLUX')
    if (.not. c_associated(authority_flux)) return
    if (.not. c_associated(mirror_flux)) return
    do ig = 1, NGRP
      call LCMLEL(authority_flux,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 4) return
      call LCMLEL(mirror_flux,ig,ilong,itylcm)
      if (ilong /= NUNKNO .or. itylcm /= 2) return
      call LCMGDL(authority_flux,ig,authority64)
      call LCMGDL(mirror_flux,ig,mirror32)
      if (.not. all(ieee_is_finite(authority64))) return
      if (.not. all(ieee_is_finite(mirror32))) return
      if (any(abs(authority64) > REAL32_MAX64)) return
      if (.not. SAME_REAL32_BITS(mirror32,real(authority64,real32))) &
          return
    end do
    PROJECTED_PLANE_IS_EXACT = .true.
  end function PROJECTED_PLANE_IS_EXACT


  logical function SYSTEM_PAYLOAD_IS_VALID(ipsystem,ipmacro,leakage, &
      plane,unreduced)
    type(c_ptr), intent(in) :: ipsystem, ipmacro
    real(real32), intent(in) :: leakage(NGRP)
    integer, intent(in) :: plane
    logical, intent(in) :: unreduced

    integer :: state(NSTATE), snapshot, ig, im, ilong, itylcm
    real(real32) :: ntot32(NMAT), sigw32(NMAT), tranc32(NMAT)
    real(real32) :: candidate_leakage32(NGRP)
    real(real32) :: tx32(0:NMAT), sphys32(0:NMAT), sused32(0:NMAT)
    real(real32) :: expected_tx32(0:NMAT)
    real(real32) :: expected_sphys32(0:NMAT)
    real(real32) :: expected_sused32(0:NMAT)
    type(c_ptr) :: macro_groups, system_groups, macro_group, system_group

    SYSTEM_PAYLOAD_IS_VALID = .false.
    if (.not. c_associated(ipsystem)) return
    if (.not. c_associated(ipmacro)) return
    if (plane < 1 .or. plane > NSNAP) return
    if (.not. all(ieee_is_finite(leakage))) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'SIGNATURE',3,12, &
        'L_PIJ')) return
    if (.not. RECORD_MATCHES(ipsystem,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(ipsystem,'STATE-VECTOR',state)
    if (any(state(1:14) /= &
        [1,1,1,0,1,1,4,NGRP,NUNKNO,NMAT,1,0,0,0])) return
    if (any(state(15:NSTATE) /= 0)) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.MACRO',3,12, &
        'MACRO0')) return
    if (.not. CHARACTER_RECORD_MATCHES(ipsystem,'LINK.TRACK',3,12, &
        'TRACK')) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-L1-SNAP',1,1)) return
    call LCMGET(ipsystem,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= plane) return
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-LEAK1D',NGRP,2)) return
    call LCMGET(ipsystem,'SPOT-LEAK1D',candidate_leakage32)
    if (.not. all(ieee_is_finite(candidate_leakage32))) return
    if (.not. SAME_REAL32_BITS(candidate_leakage32,leakage)) return
    if (.not. RECORD_MATCHES(ipsystem,'GROUP',NGRP,10)) return
    if (.not. RECORD_MATCHES(ipmacro,'GROUP',NGRP,10)) return
    system_groups = LCMGID(ipsystem,'GROUP')
    macro_groups = LCMGID(ipmacro,'GROUP')
    if (.not. c_associated(system_groups)) return
    if (.not. c_associated(macro_groups)) return

    do ig = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(system_groups,ig)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(macro_groups,ig)) return
      system_group = LCMGIL(system_groups,ig)
      macro_group = LCMGIL(macro_groups,ig)
      if (.not. c_associated(system_group)) return
      if (.not. c_associated(macro_group)) return
      if (.not. RESPONSE_GROUP_IS_EXACT(system_group)) return
      if (.not. RECORD_MATCHES(macro_group,'NTOT0',NMAT,2)) return
      if (.not. RECORD_MATCHES(macro_group,'SIGW00',NMAT,2)) return
      call LCMGET(macro_group,'NTOT0',ntot32)
      call LCMGET(macro_group,'SIGW00',sigw32)
      if (.not. all(ieee_is_finite(ntot32))) return
      if (.not. all(ieee_is_finite(sigw32))) return
      call LCMLEN(macro_group,'TRANC',ilong,itylcm)
      if (ilong /= NMAT .or. itylcm /= 2) return
      call LCMGET(macro_group,'TRANC',tranc32)
      if (.not. all(ieee_is_finite(tranc32))) return

      call LCMGET(system_group,'DRAGON-TXSC',tx32)
      call LCMGET(system_group,'SPOT-S0-PHYS',sphys32)
      call LCMGET(system_group,'DRAGON-S0XSC',sused32)
      expected_tx32 = +0.0_real32
      expected_sphys32 = +0.0_real32
      expected_sused32 = +0.0_real32
      if (unreduced) then
        ! REAL64 leakage mode: the stored self-scattering is the
        ! physical one; the reduction is applied in the solver core.
        expected_sused32(0) = expected_sphys32(0)
      else
        expected_sused32(0) = expected_sphys32(0)-leakage(ig)
      end if
      do im = 1, NMAT
        expected_tx32(im) = ntot32(im)
        expected_sphys32(im) = sigw32(im)
        expected_tx32(im) = expected_tx32(im)-tranc32(im)
        expected_sphys32(im) = expected_sphys32(im)-tranc32(im)
        if (unreduced) then
          expected_sused32(im) = expected_sphys32(im)
        else
          expected_sused32(im) = expected_sphys32(im)-leakage(ig)
        end if
      end do
      if (.not. all(ieee_is_finite(expected_tx32))) return
      if (.not. all(ieee_is_finite(expected_sphys32))) return
      if (.not. all(ieee_is_finite(expected_sused32))) return
      if (.not. SAME_REAL32_BITS(tx32,expected_tx32)) return
      if (.not. SAME_REAL32_BITS(sphys32,expected_sphys32)) return
      if (.not. SAME_REAL32_BITS(sused32,expected_sused32)) return
    end do
    SYSTEM_PAYLOAD_IS_VALID = .true.
  end function SYSTEM_PAYLOAD_IS_VALID


  logical function RESPONSE_GROUP_IS_EXACT(group)
    type(c_ptr), intent(in) :: group
    character(len=12), parameter :: names(15) = &
        ['CF$MCCG     ','ILUDF$MCCG  ','CQ$MCCG     ','DIAGQ$MCCG  ', &
         'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
         'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DRAGON-TXSC ', &
         'SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG  ']
    character(len=12), parameter :: response_names(12) = &
        ['CF$MCCG     ','ILUDF$MCCG  ','CQ$MCCG     ','DIAGQ$MCCG  ', &
         'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
         'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DIAGF$MCCG  ']
    integer, parameter :: response_lengths(12) = &
        [32,14,32,14,8,8,8,8,8,8,8,14]
    integer :: i

    RESPONSE_GROUP_IS_EXACT = .false.
    if (.not. EXACT_INVENTORY(group,names)) return
    do i = 1, size(response_names)
      if (.not. FINITE_REAL32_RECORD(group,response_names(i), &
          response_lengths(i))) return
    end do
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-TXSC',NMAT+1)) return
    if (.not. FINITE_REAL32_RECORD(group,'SPOT-S0-PHYS',NMAT+1)) return
    if (.not. FINITE_REAL32_RECORD(group,'DRAGON-S0XSC',NMAT+1)) return
    if (.not. ABSENT_RECORD(group,'FUNKNO$USS')) return
    RESPONSE_GROUP_IS_EXACT = .true.
  end function RESPONSE_GROUP_IS_EXACT


  logical function FINITE_REAL32_RECORD(root,name,expected_length)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length
    real(real32), allocatable :: values(:)
    integer :: allocation_status

    FINITE_REAL32_RECORD = .false.
    if (.not. RECORD_MATCHES(root,name,expected_length,2)) return
    allocate(values(expected_length),stat=allocation_status)
    if (allocation_status /= 0) return
    call LCMGET(root,name,values)
    FINITE_REAL32_RECORD = all(ieee_is_finite(values))
  end function FINITE_REAL32_RECORD


  logical function SYSTEM_AUTHORITY_IS_COMMITTED(ipsystem,rho,epoch)
    type(c_ptr), intent(in) :: ipsystem
    real(real64), intent(in) :: rho
    integer, intent(in) :: epoch
    type(c_ptr) :: authority
    real(real64) :: found_rho
    integer :: found_epoch

    SYSTEM_AUTHORITY_IS_COMMITTED = .false.
    if (.not. RECORD_MATCHES(ipsystem,'SPOT-R64',-1,0)) return
    authority = LCMGID(ipsystem,'SPOT-R64')
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
    SYSTEM_AUTHORITY_IS_COMMITTED = .true.
  end function SYSTEM_AUTHORITY_IS_COMMITTED


  subroutine OPEN_STAGE(stage,index)
    type(c_ptr), intent(out) :: stage
    integer, intent(in) :: index
    character(len=12), parameter :: names(NSNAP) = &
        ['B2K-STAGE-1','B2K-STAGE-2','B2K-STAGE-3']

    stage = c_null_ptr
    if (index < 1 .or. index > NSNAP) &
        call XABORT('SPOR64_B2K: INVALID PRIVATE STAGE INDEX.')
    call LCMOP(stage,names(index),0,1,0)
    if (.not. c_associated(stage)) &
        call XABORT('SPOR64_B2K: PRIVATE STAGE CREATION FAILED.')
  end subroutine OPEN_STAGE


  subroutine CLOSE_STAGES(stages)
    type(c_ptr), intent(inout) :: stages(:)
    integer :: i

    do i = 1, size(stages)
      if (c_associated(stages(i))) call LCMCL(stages(i),2)
      stages(i) = c_null_ptr
    end do
  end subroutine CLOSE_STAGES


  logical function SAME_REAL32_BITS(left,right)
    real(real32), intent(in) :: left(:), right(:)

    SAME_REAL32_BITS = size(left) == size(right)
    if (SAME_REAL32_BITS) SAME_REAL32_BITS = all( &
        transfer(left,0_int32,size(left)) == &
        transfer(right,0_int32,size(right)))
  end function SAME_REAL32_BITS


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


  logical function ABSENT_RECORD(iplist,name)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type

    ABSENT_RECORD = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    ABSENT_RECORD = actual_length == 0 .and. actual_type == 99
  end function ABSENT_RECORD


  logical function LIST_ITEM_IS_DIRECTORY(iplist,index)
    type(c_ptr), intent(in) :: iplist
    integer, intent(in) :: index
    integer :: actual_length, actual_type

    LIST_ITEM_IS_DIRECTORY = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEL(iplist,index,actual_length,actual_type)
    LIST_ITEM_IS_DIRECTORY = actual_length == -1 .and. actual_type == 0
  end function LIST_ITEM_IS_DIRECTORY


  logical function CHARACTER_RECORD_MATCHES(iplist,name,expected_words, &
      character_count,expected_value)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name, expected_value
    integer, intent(in) :: expected_words, character_count
    character(len=72) :: value

    CHARACTER_RECORD_MATCHES = .false.
    if (character_count < 1 .or. character_count > len(value)) return
    if (.not. RECORD_MATCHES(iplist,name,expected_words,3)) return
    value = ' '
    call LCMGTC(iplist,name,character_count,value)
    CHARACTER_RECORD_MATCHES = value(1:character_count) == expected_value
  end function CHARACTER_RECORD_MATCHES


  logical function PROJECTED_ARCHIVE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(7) = &
        ['SIGNATURE   ','LISTDIM     ','SPOT-ITER-K ','TRACK       ', &
         'MICROLIB2   ','FLUX        ','SPOT-R64    ']

    PROJECTED_ARCHIVE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function PROJECTED_ARCHIVE_ROOT_IS_EXACT


  logical function ROOT_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(4) = &
        ['RHO         ','NPLANE      ','STATE       ','EPOCH       ']

    ROOT_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function ROOT_AUTHORITY_IS_EXACT


  logical function PROJECTED_PLANE_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(12) = &
        ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
         'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ']
    character(len=12), parameter :: names64(13) = &
        ['SPOT-R64    ','FLUX        ','SIGNATURE   ','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK ','KEYFLX      ','OPTION      ', &
         'LINK.MACRO  ','LINK.TRACK  ','LINK.SYSTEM ','SPOT-LEAK1D ', &
         'LEAK1D64    ']

    PROJECTED_PLANE_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,names64) &
        .or. EXACT_INVENTORY(iplist,names)
  end function PROJECTED_PLANE_ROOT_IS_EXACT


  logical function PROJECTED_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(4) = &
        ['RHO         ','FLUX        ','STATE       ','EPOCH       ']

    PROJECTED_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function PROJECTED_AUTHORITY_IS_EXACT


  logical function SYSTEM_AUTHORITY_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(3) = &
        ['RHO         ','STATE       ','EPOCH       ']

    SYSTEM_AUTHORITY_IS_EXACT = EXACT_INVENTORY(iplist,names)
  end function SYSTEM_AUTHORITY_IS_EXACT


  logical function CANDIDATE_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(7) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ']
    character(len=12), parameter :: raw(8) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-L1-RAW ']

    CANDIDATE_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,raw) &
        .or. EXACT_INVENTORY(iplist,names)
  end function CANDIDATE_SYSTEM_ROOT_IS_EXACT


  logical function STAGED_SYSTEM_ROOT_IS_EXACT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=12), parameter :: names(8) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-R64    ']
    character(len=12), parameter :: raw(9) = &
        ['SIGNATURE   ','LINK.MACRO  ','LINK.TRACK  ','STATE-VECTOR', &
         'SPOT-LEAK1D ','SPOT-L1-SNAP','GROUP       ','SPOT-R64    ', &
         'SPOT-L1-RAW ']

    STAGED_SYSTEM_ROOT_IS_EXACT = EXACT_INVENTORY(iplist,raw) &
        .or. EXACT_INVENTORY(iplist,names)
  end function STAGED_SYSTEM_ROOT_IS_EXACT


  logical function EXACT_INVENTORY(iplist,expected_names)
    type(c_ptr), intent(in) :: iplist
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, item_name
    integer :: count, i, allocation_status
    logical, allocatable :: found(:)

    EXACT_INVENTORY = .false.
    if (.not. c_associated(iplist)) return
    allocate(found(size(expected_names)),stat=allocation_status)
    if (allocation_status /= 0) return
    found = .false.
    item_name = ' '
    call LCMNXT(iplist,item_name)
    if (item_name == ' ') return
    first_name = item_name
    count = 0
    do
      count = count+1
      if (count > size(expected_names)) return
      do i = 1, size(expected_names)
        if (item_name == expected_names(i)) exit
      end do
      if (i > size(expected_names)) return
      if (found(i)) return
      found(i) = .true.
      call LCMNXT(iplist,item_name)
      if (item_name == first_name) exit
    end do
    EXACT_INVENTORY = count == size(expected_names) .and. all(found)
  end function EXACT_INVENTORY

end module SPOR64_B2K


subroutine SPOR64K(nentry,hentry,ientry,jentry,kentry)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB
  use SPOR64_B2K, only : SPOR64_B2K_ARCHIVE_ASSEMBLED, &
      SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE
  implicit none

  integer, intent(in) :: nentry, ientry(nentry), jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  integer :: indic, nitma, status
  real :: flott
  double precision :: dflott
  character(len=4) :: text4
  type(c_ptr) :: systems(3)

  if (nentry /= 5) call XABORT('SPOR64K: FIVE ENTRIES EXPECTED.')
  if (hentry(1) /= 'ASSEMBLED') &
      call XABORT('SPOR64K: ASSEMBLED OUTPUT EXPECTED.')
  if (hentry(2) /= 'PROJECTED') &
      call XABORT('SPOR64K: PROJECTED INPUT EXPECTED.')
  if (hentry(3) /= 'SYSTEM1' .or. hentry(4) /= 'SYSTEM2' .or. &
      hentry(5) /= 'SYSTEM3') &
      call XABORT('SPOR64K: SYSTEM1/2/3 INPUTS EXPECTED.')
  if (any((ientry /= 1) .and. (ientry /= 2))) &
      call XABORT('SPOR64K: LCM ENTRIES EXPECTED.')
  if (jentry(1) /= 0 .or. any(jentry(2:5) /= 2)) &
      call XABORT('SPOR64K: NEW OUTPUT AND READ-ONLY INPUTS EXPECTED.')

  ! Consume the empty option list before any caller-visible mutation.
  call REDGET(indic,nitma,flott,text4,dflott)
  if (indic /= 3 .or. text4 /= ';') &
      call XABORT('SPOR64K: ; CHARACTER EXPECTED.')

  systems = kentry(3:5)
  call SPOR64_B2K_COMMIT_SYSTEM_ARCHIVE(kentry(1),kentry(2), &
      systems,status)
  if (status /= SPOR64_B2K_ARCHIVE_ASSEMBLED) &
      call XABORT('SPOR64K: B2K ARCHIVE ADMISSION FAILED.')
end subroutine SPOR64K
