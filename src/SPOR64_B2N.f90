module SPOR64_B2N
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use GANLIB
  use SPOR64_VERIFY, only : ABSENT_RECORD, CHARACTER_RECORD_MATCHES, &
      EMPTY_MEMORY_ROOT, EXACT_INVENTORY, LIST_ITEM_IS_DIRECTORY, &
      RECORD_MATCHES
  implicit none
  private

  integer, parameter, public :: SPOR64_B2N_PREFLIGHT_FAILED = 1
  integer, parameter, public :: SPOR64_B2N_COMMITTED = 2

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

  public :: SPOR64_B2N_BUILD

contains

  subroutine SPOR64_B2N_BUILD(ipprojected,plane_index,ipmacro_out,ipsource_out,status)
    type(c_ptr), intent(in) :: ipprojected, ipmacro_out, ipsource_out
    integer, intent(in) :: plane_index
    integer, intent(out) :: status

    integer :: root_planes, root_epoch, plane_epoch
    integer :: track_state(NSTATE), mccg_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: flux_state(NSTATE), source_state(NSTATE)
    integer :: matcod(NREG), nzon(NUNKNO)
    integer :: keyflx(NREG), keyanis(NREG), keycur(NSOUT)
    integer :: imerge(NMAT)
    integer :: ip, ir, ifis, h, g, im, iu, ilong, itylcm
    integer :: allocation_status
    integer(int32) :: volume_bits, track_volume_bits
    integer(int64) :: found64, expected64
    real(real32) :: volume32(NREG), track_volume32(NUNKNO)
    real(real32) :: real_param32(4), eps_converge32(5)
    real(real32) :: leakage32(NGRP)
    real(real32), allocatable :: nusigf32(:,:,:), chi32(:,:,:)
    real(real32) :: q32(NUNKNO,NGRP), qint32(NGRP)
    real(real32) :: zero_nusigf32(NMAT*NIFIS), keff32
    real(real64) :: iter_keff64, rho64, plane_rho64
    real(real64) :: phi64(NUNKNO,NGRP), q64(NUNKNO,NGRP)
    real(real64) :: qint64(NGRP), mirror_first_integral64
    real(real64) :: fis64, product64, contribution64
    logical :: seen_unknown(NUNKNO)
    character(len=12) :: signature, lifecycle_state
    type(c_ptr) :: tracks, libraries, fluxes
    type(c_ptr) :: input_track, input_library, input_flux
    type(c_ptr) :: input_macro, input_groups, input_group
    type(c_ptr) :: root_authority, plane_authority, authority_flux
    type(c_ptr) :: output_groups, output_group
    type(c_ptr) :: source_outer, source_inner
    type(c_ptr) :: source_authority, qfiss_list

    status = SPOR64_B2N_PREFLIGHT_FAILED

    ! Both products are new in-memory LCM objects.  They cannot alias each
    ! other or the immutable B2l PROJECTED/e archive.
    if (.not. c_associated(ipprojected)) return
    if (.not. c_associated(ipmacro_out)) return
    if (.not. c_associated(ipsource_out)) return
    if (c_associated(ipprojected,ipmacro_out)) return
    if (c_associated(ipprojected,ipsource_out)) return
    if (c_associated(ipmacro_out,ipsource_out)) return
    if (plane_index < 1 .or. plane_index > NSNAP) return
    if (.not. EMPTY_MEMORY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_MEMORY_ROOT(ipsource_out)) return

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
    if (.not. CHARACTER_RECORD_MATCHES(root_authority,'STATE',3,12, &
        'PROJECTED')) return
    if (.not. RECORD_MATCHES(root_authority,'EPOCH',1,1)) return
    call LCMGET(root_authority,'RHO',rho64)
    call LCMGET(root_authority,'NPLANE',root_planes)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(rho64)) return
    if (rho64 <= +0.0_real64) return
    if (root_planes /= NSNAP) return
    if (root_epoch <= 0) return
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
    do ip = 1, NSNAP
      if (.not. LIST_ITEM_IS_DIRECTORY(tracks,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(libraries,ip)) return
      if (.not. LIST_ITEM_IS_DIRECTORY(fluxes,ip)) return
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
    if (any(track_state /= TRACK_STATE_EXPECTED)) return
    if (.not. RECORD_MATCHES(input_track,'MCCG-STATE',NSTATE,1)) return
    call LCMGET(input_track,'MCCG-STATE',mccg_state)
    if (any(mccg_state /= MCCG_STATE_EXPECTED)) return
    if (.not. RECORD_MATCHES(input_track,'REAL-PARAM',4,2)) return
    call LCMGET(input_track,'REAL-PARAM',real_param32)
    if (.not. all(ieee_is_finite(real_param32))) return
    if (transfer(real_param32(1),0_int32) /= MCCG_EPSI_BITS) return
    if (any(transfer(real_param32(2:4),0_int32,3) /= 0_int32)) return
    if (.not. RECORD_MATCHES(input_track,'VOLUME',NREG,2)) return
    if (.not. RECORD_MATCHES(input_track,'V$MCCG',NUNKNO,2)) return
    if (.not. RECORD_MATCHES(input_track,'MATCOD',NREG,1)) return
    if (.not. RECORD_MATCHES(input_track,'NZON$MCCG',NUNKNO,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX',NREG,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYFLX$ANIS',NREG,1)) return
    if (.not. RECORD_MATCHES(input_track,'KEYCUR$MCCG',NSOUT,1)) return
    call LCMGET(input_track,'VOLUME',volume32)
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
    if (any(matcod < 1) .or. any(matcod > NMAT)) return
    if (any(nzon(1:NREG) /= matcod)) return
    if (any(nzon(NREG+1:NUNKNO) < -NSOUT)) return
    if (any(nzon(NREG+1:NUNKNO) > -1)) return
    do ir = 1, NREG
      volume_bits = transfer(volume32(ir),0_int32)
      track_volume_bits = transfer(track_volume32(ir),0_int32)
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

    ! The same-index MICROLIB2 supplies one L_MACROLIB.  All fission data
    ! are staged as binary32, checked, and promoted only at the arithmetic
    ! operation where they enter the REAL64 source definition.
    if (.not. CHARACTER_RECORD_MATCHES(input_library,'SIGNATURE',3,12, &
        'L_LIBRARY')) return
    if (.not. RECORD_MATCHES(input_library,'STATE-VECTOR',NSTATE,1)) return
    call LCMGET(input_library,'STATE-VECTOR',library_state)
    if (library_state(1) /= NMAT) return
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
    if (any(macro_state /= MACRO_STATE_EXPECTED)) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-FROZEN')) return
    if (.not. ABSENT_RECORD(input_macro,'SPOT-KEFF')) return
    if (.not. RECORD_MATCHES(input_macro,'GROUP',NGRP,10)) return
    input_groups = LCMGID(input_macro,'GROUP')
    if (.not. c_associated(input_groups)) return
    allocate(nusigf32(NMAT,NIFIS,NGRP),chi32(NMAT,NIFIS,NGRP), &
        stat=allocation_status)
    if (allocation_status /= 0) return
    do g = 1, NGRP
      if (.not. LIST_ITEM_IS_DIRECTORY(input_groups,g)) return
      input_group = LCMGIL(input_groups,g)
      if (.not. c_associated(input_group)) return
      if (.not. RECORD_MATCHES(input_group,'NUSIGF',NMAT*NIFIS,2)) return
      if (.not. RECORD_MATCHES(input_group,'CHI',NMAT*NIFIS,2)) return
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
    if (any(flux_state(1:18) /= &
        [NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500,0,0,0,0,NMAT,1])) return
    if (any(flux_state(19:NSTATE) /= 0)) return
    if (.not. RECORD_MATCHES(input_flux,'EPS-CONVERGE',5,2)) return
    call LCMGET(input_flux,'EPS-CONVERGE',eps_converge32)
    if (.not. all(ieee_is_finite(eps_converge32))) return
    do g = 1, 3
      if (transfer(eps_converge32(g),0_int32) /= FROZEN_TOL_BITS) return
    end do
    do g = 4, 5
      if (transfer(eps_converge32(g),0_int32) /= 0_int32) return
    end do
    if (.not. RECORD_MATCHES(input_flux,'IMERGE-LEAK',NMAT,1)) return
    call LCMGET(input_flux,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) return
    if (.not. RECORD_MATCHES(input_flux,'KEYFLX',NREG,1)) return
    call LCMGET(input_flux,'KEYFLX',keyanis)
    if (any(keyanis /= keyflx)) return
    if (.not. CHARACTER_RECORD_MATCHES(input_flux,'OPTION',1,4, &
        'B0  ')) return
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
    if (.not. CHARACTER_RECORD_MATCHES(plane_authority,'STATE',3,12, &
        'PROJECTED')) return
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
      if (ilong /= NUNKNO .or. itylcm /= 4) return
      call LCMGDL(authority_flux,h,phi64(:,h))
      if (.not. all(ieee_is_finite(phi64(:,h)))) return
    end do
    do ir = 1, NREG
      do h = 1, NGRP
        if (phi64(keyflx(ir),h) <= +0.0_real64) return
      end do
    end do

    ! This scalar loop nest is the numerical definition.  It deliberately
    ! separates multiplication from addition, and never assumes FMA,
    ! reassociation, a reduction intrinsic, clipping, or normalization.
    q64 = +0.0_real64
    do ir = 1, NREG
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
      do ir = 1, NREG
        product64 = real(volume32(ir),real64) * q64(keyflx(ir),g)
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
    do ir = 1, NREG
      product64 = real(volume32(ir),real64) * &
          real(q32(keyflx(ir),1),real64)
      mirror_first_integral64 = mirror_first_integral64 + product64
    end do
    if (.not. ieee_is_finite(mirror_first_integral64)) return
    if (mirror_first_integral64 <= +0.0_real64) return

    ! Complete preflight precedes the first output mutation.  Repeating both
    ! freshness checks closes the caller-visible time-of-check window.
    if (.not. EMPTY_MEMORY_ROOT(ipmacro_out)) return
    if (.not. EMPTY_MEMORY_ROOT(ipsource_out)) return

    ! MACRO0 is a recursive copy of the selected macrolib.  Its only changed
    ! physical records are all NUSIGF arrays, set to positive numerical zero
    ! so the fixed QFISS source cannot be counted a second time by FLU.
    call LCMEQU(input_macro,ipmacro_out)
    zero_nusigf32 = +0.0_real32
    output_groups = LCMGID(ipmacro_out,'GROUP')
    if (.not. c_associated(output_groups)) &
        call XABORT('SPOR64_B2N: OUTPUT MACRO GROUP LIST MISSING.')
    do g = 1, NGRP
      output_group = LCMGIL(output_groups,g)
      if (.not. c_associated(output_group)) &
          call XABORT('SPOR64_B2N: OUTPUT MACRO GROUP MISSING.')
      call LCMPUT(output_group,'NUSIGF',NMAT*NIFIS,2,zero_nusigf32)
    end do
    call LCMPUT(ipmacro_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipmacro_out,'SPOT-KEFF',1,2,keff32)

    signature = 'L_SOURCE'
    call LCMPTC(ipsource_out,'SIGNATURE',12,signature)
    source_state = 0
    source_state(1:3) = [NGRP,NUNKNO,1]
    call LCMPUT(ipsource_out,'STATE-VECTOR',NSTATE,1,source_state)
    call LCMPUT(ipsource_out,'SPOT-FROZEN',1,1,1)
    call LCMPUT(ipsource_out,'SPOT-KEFF',1,2,keff32)
    call LCMPUT(ipsource_out,'SPOT-QINT',NGRP,2,qint32)
    source_outer = LCMLID(ipsource_out,'DSOUR',1)
    if (.not. c_associated(source_outer)) &
        call XABORT('SPOR64_B2N: DSOUR OUTER LIST CREATION FAILED.')
    source_inner = LCMLIL(source_outer,1,NGRP)
    if (.not. c_associated(source_inner)) &
        call XABORT('SPOR64_B2N: DSOUR INNER LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(source_inner,g,NUNKNO,2,q32(:,g))
    end do

    source_authority = LCMDID(ipsource_out,'SPOT-R64')
    if (.not. c_associated(source_authority)) &
        call XABORT('SPOR64_B2N: SOURCE AUTHORITY CREATION FAILED.')
    call LCMPUT(source_authority,'RHO',1,4,rho64)
    call LCMPUT(source_authority,'PLANE',1,1,plane_index)
    lifecycle_state = 'FROZEN-QFIS'
    call LCMPTC(source_authority,'STATE',12,lifecycle_state)
    qfiss_list = LCMLID(source_authority,'QFISS',NGRP)
    if (.not. c_associated(qfiss_list)) &
        call XABORT('SPOR64_B2N: QFISS LIST CREATION FAILED.')
    do g = 1, NGRP
      call LCMPDL(qfiss_list,g,NUNKNO,4,q64(:,g))
    end do

    ! EPOCH is the source-wide commit and the final output mutation.
    call LCMPUT(source_authority,'EPOCH',1,1,root_epoch)
    status = SPOR64_B2N_COMMITTED
  end subroutine SPOR64_B2N_BUILD
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
end module SPOR64_B2N
