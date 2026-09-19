program test_full_rank_picard_cycle
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : error_unit, int32, int64, &
      real32, real64
  use GANLIB
  use SPOR64_B2I, only : SPOR64_B2I_ADMISSION_FAILED, &
      SPOR64_B2I_BOOTSTRAP_COMMITTED, &
      SPOR64_B2I_SEAL_BOOTSTRAP
  use SPOR64_B2J, only : SPOR64_B2J_ADMISSION_FAILED, &
      SPOR64_B2J_ARCHIVE_PROJECTED, &
      SPOR64_B2J_PROJECT_ARCHIVE
  use SPOR64_B2W, only : SPOR64_B2W_CLOSED, &
      SPOR64_B2W_PREFLIGHT_FAILED, SPOR64_B2W_CLOSE
  use SPOR64_VERIFY, only : EMPTY_ROOT
  implicit none

  integer, parameter :: NSTATE = 40
  integer, parameter :: NGRP = 370
  integer, parameter :: NSNAP = 3
  integer, parameter :: NREG2D = 4
  integer, parameter :: NMODE_OLD = 3
  integer, parameter :: NMODE_FULL = 4
  integer, parameter :: NFLOOR = 3
  integer, parameter :: NAXREG = NREG2D*NFLOOR
  integer, parameter :: LL4 = NAXREG
  integer, parameter :: LL5 = NREG2D*(NFLOOR+1)
  integer, parameter :: NAXUNK = LL4+LL5
  integer, parameter :: NMAT = 1
  integer, parameter :: NSURF = 1
  integer, parameter :: NUNK = NREG2D+NSURF
  integer, parameter :: NIFIS = 32
  integer, parameter :: MAXMIX = 3
  integer(int32), parameter :: FROZEN_TOL_BITS = int(z'348637bd',int32)
  real(real64), parameter :: KEFF64 = 1.2500000001_real64
  real(real64), parameter :: BAD_KEFF64 = 1.2500000002_real64
  real(real32), parameter :: KEFF32 = real(KEFF64,real32)

  integer :: status, dims(4), rank(NGRP), ilong, itylcm
  integer :: ientry2(2), jentry2(2), ientry4(4), jentry4(4)
  character(len=12) :: hentry2(2), hentry4(4)
  type(c_ptr) :: pod_system, physical_system, bad_fluxes, bad_plane
  type(c_ptr) :: route_contract, tampered_contract
  type(c_ptr) :: axial_track, axial_macro, axial_flux
  type(c_ptr) :: bootstrap, sealed_ax0, closed_archive0
  type(c_ptr) :: projected_archive1, feedback1, axial_candidate1
  type(c_ptr) :: closed_ax1, closed_archive1, projected_archive2
  type(c_ptr) :: bad_archive, bad_feedback, bad_output1, bad_output2
  type(c_ptr) :: kentry2(2), kentry4(4)
  real(real32) :: b2i_bad_leakage32(NGRP)
  real(real64) :: b2i_bad_leakage64(NGRP*NSNAP)

  call open_root(pod_system,'PC-POD')
  call open_root(physical_system,'PC-PHYS')
  call open_root(axial_track,'PC-AXTRK')
  call open_root(axial_macro,'PC-AXMAC')
  call open_root(axial_flux,'PC-AXFLX')
  call open_root(bootstrap,'PC-BOOT')
  call open_root(sealed_ax0,'PC-AX0')
  call open_root(closed_archive0,'PC-ARC0')
  call open_root(projected_archive1,'PC-PROJ1')
  call open_root(feedback1,'PC-RET1')
  call open_root(axial_candidate1,'PC-AXC1')
  call open_root(closed_ax1,'PC-AX1')
  call open_root(closed_archive1,'PC-ARC1')
  call open_root(projected_archive2,'PC-PROJ2')

  call build_pod_system(pod_system)
  hentry2(1) = 'PHYSICAL'
  hentry2(2) = 'POD-SYSTEM'
  ientry2 = [1,1]
  jentry2 = [0,2]
  kentry2 = [physical_system,pod_system]
  call SPOPHYS(2,hentry2,ientry2,jentry2,kentry2)
  call LCMGET(physical_system,'POD-RANK-G',rank)
  call assert_true(all(rank == NMODE_FULL), &
      'SPOPHYS DID NOT PRODUCE FULL PHYSICAL RANK')

  call build_axial_track(axial_track)
  call build_axial_macro(axial_macro)
  call build_axial_flux(axial_flux)
  hentry4(1) = 'AXIAL-FLUX'
  hentry4(2) = 'AXIAL-TRACK'
  hentry4(3) = 'PHYSICAL'
  hentry4(4) = 'AXIAL-MACRO'
  ientry4 = [1,1,1,1]
  jentry4 = [1,2,2,2]
  kentry4 = [axial_flux,axial_track,physical_system,axial_macro]
  call SPOSTATE(4,hentry4,ientry4,jentry4,kentry4)
  call LCMGET(axial_flux,'SPOT-X-DIMS',dims)
  call assert_true(all(dims == [1,NGRP,NSNAP, &
      NGRP*NSNAP*NMODE_FULL]),'SPOSTATE FULL-RANK DIMENSIONS')
  call LCMGET(axial_flux,'SPOT-X-RANK',rank)
  call assert_true(all(rank == NMODE_FULL),'SPOSTATE LOST FULL RANK')
  call LCMLEN(axial_flux,'SPOT-X-KEFF',ilong,itylcm)
  call assert_true(ilong == 1 .and. itylcm == 4, &
      'SPOSTATE DID NOT RETAIN REAL64 KEFF')
  call check_real64_keff(axial_flux)

  call build_route_contract(route_contract,FROZEN_TOL_BITS)

  call build_bootstrap_archive(bootstrap)
  ! Exercise the genesis boundary explicitly: retain a nonzero REAL64
  ! value that projects to the archive's zero REAL32 mirror.
  call LCMGET(axial_flux,'SPOT-X-L',b2i_bad_leakage64)
  b2i_bad_leakage64(1) = tiny(0.0_real64)
  call LCMPUT(axial_flux,'SPOT-X-L',NGRP*NSNAP,4,b2i_bad_leakage64)
  ! A one-ULP change in that REAL32 mirror must still fail closed.
  call open_root(bad_archive,'PC-BADAR')
  call LCMEQU(bootstrap,bad_archive)
  bad_fluxes = LCMGID(bad_archive,'FLUX')
  bad_plane = LCMGIL(bad_fluxes,1)
  call LCMGET(bad_plane,'SPOT-LEAK1D',b2i_bad_leakage32)
  b2i_bad_leakage32(1) = transfer(1_int32,0.0_real32)
  call LCMPUT(bad_plane,'SPOT-LEAK1D',NGRP,2,b2i_bad_leakage32)
  call open_root(bad_output1,'PC-BADO1')
  call open_root(bad_output2,'PC-BADO2')
  call SPOR64_B2I_SEAL_BOOTSTRAP(bad_output1,bad_output2, &
      axial_flux,axial_track,bad_archive,route_contract,status)
  call assert_true(status == SPOR64_B2I_ADMISSION_FAILED .and. &
      EMPTY_ROOT(bad_output1) .and. EMPTY_ROOT(bad_output2), &
      'B2I ACCEPTED A ONE-ULP REAL32 LEAKAGE TAMPER')
  call LCMCL(bad_output2,2)
  call LCMCL(bad_output1,2)
  call LCMCL(bad_archive,2)
  call SPOR64_B2I_SEAL_BOOTSTRAP(sealed_ax0,closed_archive0, &
      axial_flux,axial_track,bootstrap,route_contract,status)
  call assert_true(status == SPOR64_B2I_BOOTSTRAP_COMMITTED, &
      'B2I REJECTED MANUFACTURED BOOTSTRAP')
  call LCMGET(sealed_ax0,'SPOT-X-L',b2i_bad_leakage64)
  call assert_true(transfer(b2i_bad_leakage64(1),0_int64) == &
      transfer(tiny(0.0_real64),0_int64), &
      'B2I QUANTIZED THE REAL64 AXIAL LEAKAGE AUTHORITY')
  call check_axial_state(sealed_ax0,'CLOSED',0)
  call check_real64_keff(sealed_ax0)
  call check_archive_state(closed_archive0,'CLOSED',0)

  call open_root(bad_archive,'PC-BADAR')
  call open_root(bad_output1,'PC-BADO1')
  call LCMEQU(closed_archive0,bad_archive)
  call LCMPUT(bad_archive,'SPOT-ITER-K',1,4,BAD_KEFF64)
  call SPOR64_B2J_PROJECT_ARCHIVE(bad_output1,sealed_ax0, &
      axial_track,bad_archive,route_contract,status)
  call assert_true(status == SPOR64_B2J_ADMISSION_FAILED .and. &
      EMPTY_ROOT(bad_output1),'B2J ACCEPTED SAME-REAL32 DIFFERENT-REAL64 K')
  call LCMCL(bad_output1,2)
  call LCMCL(bad_archive,2)

  call SPOR64_B2J_PROJECT_ARCHIVE(projected_archive1,sealed_ax0, &
      axial_track,closed_archive0,route_contract,status)
  call assert_true(status == SPOR64_B2J_ARCHIVE_PROJECTED, &
      'FIRST B2J PROJECTION FAILED')
  call check_archive_state(projected_archive1,'PROJECTED',1)

  call build_identity_feedback(projected_archive1,feedback1)
  call LCMEQU(sealed_ax0,axial_candidate1)
  call LCMDEL(axial_candidate1,'SPOT-X-STATE')
  call LCMDEL(axial_candidate1,'SPOT-X-EPOCH')
  call open_root(bad_feedback,'PC-BADFB')
  call open_root(bad_output1,'PC-BADO1')
  call open_root(bad_output2,'PC-BADO2')
  call LCMEQU(feedback1,bad_feedback)
  call LCMPUT(bad_feedback,'SPOT-ITER-K',1,4,BAD_KEFF64)
  call SPOR64_B2W_CLOSE(bad_output1,bad_output2,axial_candidate1, &
      bad_feedback,route_contract,status)
  call assert_true(status == SPOR64_B2W_PREFLIGHT_FAILED .and. &
      EMPTY_ROOT(bad_output1) .and. EMPTY_ROOT(bad_output2), &
      'B2W ACCEPTED SAME-REAL32 DIFFERENT-REAL64 K')
  call LCMCL(bad_output2,2)
  call LCMCL(bad_output1,2)
  call LCMCL(bad_feedback,2)
  call SPOR64_B2W_CLOSE(closed_ax1,closed_archive1,axial_candidate1, &
      feedback1,route_contract,status)
  call assert_true(status == SPOR64_B2W_CLOSED, &
      'B2W REJECTED STRICT IDENTITY FEEDBACK')

  ! NEGATIVE ROUTE-CONTRACT TEST: one flipped bit in the sealed radial
  ! terminal must make the same otherwise-valid close refuse with both
  ! outputs untouched.
  call build_route_contract(tampered_contract,FROZEN_TOL_BITS+1_int32)
  call open_root(bad_output1,'PC-BADO1')
  call open_root(bad_output2,'PC-BADO2')
  call SPOR64_B2W_CLOSE(bad_output1,bad_output2,axial_candidate1, &
      feedback1,tampered_contract,status)
  call assert_true(status == SPOR64_B2W_PREFLIGHT_FAILED .and. &
      EMPTY_ROOT(bad_output1) .and. EMPTY_ROOT(bad_output2), &
      'B2W ACCEPTED A TAMPERED ROUTE CONTRACT')
  call LCMCL(bad_output2,2)
  call LCMCL(bad_output1,2)
  call LCMCL(tampered_contract,2)
  call check_axial_state(closed_ax1,'CLOSED',1)
  call check_real64_keff(closed_ax1)
  call check_archive_state(closed_archive1,'CLOSED',1)

  call SPOR64_B2J_PROJECT_ARCHIVE(projected_archive2,closed_ax1, &
      axial_track,closed_archive1,route_contract,status)
  call assert_true(status == SPOR64_B2J_ARCHIVE_PROJECTED, &
      'SECOND B2J PROJECTION FAILED')
  call check_archive_state(projected_archive2,'PROJECTED',2)
  call LCMGET(closed_ax1,'SPOT-X-RANK',rank)
  call assert_true(all(rank == NMODE_FULL), &
      'FULL RANK CHANGED ACROSS PICARD EPOCH')

  call LCMCL(projected_archive2,2)
  call LCMCL(closed_archive1,2)
  call LCMCL(closed_ax1,2)
  call LCMCL(axial_candidate1,2)
  call LCMCL(feedback1,2)
  call LCMCL(projected_archive1,2)
  call LCMCL(closed_archive0,2)
  call LCMCL(sealed_ax0,2)
  call LCMCL(bootstrap,2)
  call LCMCL(axial_flux,2)
  call LCMCL(axial_macro,2)
  call LCMCL(axial_track,2)
  call LCMCL(physical_system,2)
  call LCMCL(pod_system,2)

  call LCMCL(route_contract,2)
  write(*,'(A)') &
      'B2I PROJECTION PASS: REAL64 AUTHORITY RETAINED; R32 1-ULP TAMPER REFUSED'
  write(*,'(A)') &
      'FULL-RANK REAL64 K CONTRACT PASS: B2J/B2W REJECT R64 DRIFT IN ONE R32 BIN'
  write(*,'(A)') &
      'ROUTE-CONTRACT NEGATIVE PASS: TAMPERED CONTRACT REFUSED'
  write(*,'(A)') &
      'FULL-RANK PICARD CYCLE PASS: NREG2D=4 NSNAP=3 RANK=4 EPOCH=0->1->2'

contains

  subroutine build_route_contract(root,eps_radial_bits)
    type(c_ptr), intent(out) :: root
    integer(int32), intent(in) :: eps_radial_bits
    real(real32) :: eps32(3)
    character(len=12) :: sig12, name12
    character(len=4) :: option4
    call open_root(root,'PC-RCONTR')
    sig12 = 'L_RCONTRACT'
    name12 = 'PC-SMOKE'
    option4 = 'B0  '
    eps32(1) = transfer(eps_radial_bits,0.0_real32)
    eps32(2) = transfer(eps_radial_bits,0.0_real32)
    eps32(3) = transfer(eps_radial_bits,0.0_real32)
    call LCMPTC(root,'SIGNATURE',12,sig12)
    call LCMPTC(root,'CASE-NAME',12,name12)
    call LCMPUT(root,'EPS-TERMINAL',3,2,eps32)
    call LCMPUT(root,'FLU-CAPS',2,1,[500,740])
    call LCMPUT(root,'FLU-ACCE',2,1,[3,3])
    call LCMPTC(root,'FLU-OPTION',4,option4)
  end subroutine build_route_contract

  subroutine open_root(root,name)
    type(c_ptr), intent(out) :: root
    character(len=*), intent(in) :: name

    call LCMOP(root,name,0,1,0)
    call assert_true(c_associated(root),'LCM ROOT CREATE '//trim(name))
  end subroutine open_root


  subroutine build_pod_system(root)
    type(c_ptr), intent(in) :: root
    integer :: state(NSTATE), rank_old(NGRP), ig, is
    real(real32) :: volume(NREG2D), basis(NREG2D,NMODE_OLD)
    real(real32) :: coefficient(NMODE_OLD,NSNAP)
    real(real32) :: radial(NREG2D*NSNAP), tx(MAXMIX+1)
    real(real32) :: scatter(MAXMIX+1)
    real(real64) :: sigma_root(NGRP*NSNAP), sigma(NSNAP)
    character(len=12) :: text12
    type(c_ptr) :: groups, group

    text12 = 'L_PIJ'
    call LCMPTC(root,'SIGNATURE',12,text12)
    state = 0
    state(1) = 1
    state(2) = 1
    state(3) = 1
    state(5) = 1
    state(6) = 1
    state(8) = NGRP
    state(9) = NAXUNK
    state(10) = MAXMIX
    state(11) = 1
    state(14) = 1
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    rank_old = NMODE_OLD
    call LCMPUT(root,'POD-RANK-G',NGRP,1,rank_old)
    call LCMPUT(root,'SPOT-FIXB',1,1,0)
    text12 = 'POD-BUILT'
    call LCMPTC(root,'SPOT-BTYPE',12,text12)

    do ig = 1, NGRP
      do is = 1, NSNAP
        sigma_root((ig-1)*NSNAP+is) = real(NSNAP-is+1,real64)
      end do
    end do
    call LCMPUT(root,'POD-SIGMA-G',NGRP*NSNAP,4,sigma_root)

    volume = 1.0_real32
    basis = 0.0_real32
    basis(1,1) = 2.0_real32
    basis(2,2) = 2.0_real32
    basis(3,3) = 2.0_real32
    coefficient = 0.25_real32
    radial = 0.0_real32
    tx = 1.0_real32
    scatter = 0.0_real32
    groups = LCMLID(root,'GROUP',NGRP)
    call assert_true(c_associated(groups),'POD GROUP LIST CREATE')
    do ig = 1, NGRP
      group = LCMDIL(groups,ig)
      call assert_true(c_associated(group),'POD GROUP CREATE')
      call LCMPUT(group,'NREG2D',1,1,NREG2D)
      call LCMPUT(group,'NSNAP',1,1,NSNAP)
      call LCMPUT(group,'POD-NMODE',1,1,NMODE_OLD)
      call LCMPUT(group,'VOL2D',NREG2D,2,volume)
      call LCMPUT(group,'POD-BASIS',NREG2D*NMODE_OLD,2,basis)
      call LCMPUT(group,'POD-COEFF',NMODE_OLD*NSNAP,2,coefficient)
      sigma = sigma_root((ig-1)*NSNAP+1:ig*NSNAP)
      call LCMPUT(group,'POD-SIGMA',NSNAP,4,sigma)
      call LCMPUT(group,'POD-REC-ERR',1,4,0.0_real64)
      call LCMPUT(group,'POD-ORTHO',1,4,0.0_real64)
      call LCMPUT(group,'RADIAL-OP',NREG2D*NSNAP,2,radial)
      call LCMPUT(group,'DRAGON-TXSC',MAXMIX+1,2,tx)
      call LCMPUT(group,'DRAGON-S0XSC',MAXMIX+1,2,scatter)
    end do
  end subroutine build_pod_system


  subroutine build_axial_track(root)
    type(c_ptr), intent(in) :: root
    integer :: state(NSTATE), mat(NAXREG), key(NAXREG), i
    integer :: floor_map(NFLOOR)
    real(real32) :: area(NREG2D), height(NFLOOR), volume(NAXREG)
    character(len=12) :: text12

    text12 = 'L_TRACK'
    call LCMPTC(root,'SIGNATURE',12,text12)
    text12 = 'SPOT'
    call LCMPTC(root,'TRACK-TYPE',12,text12)
    state = 0
    state(1) = NAXREG
    state(2) = NAXUNK
    state(6) = NREG2D
    state(7) = NFLOOR
    state(8) = NSNAP
    state(11) = LL4
    state(12) = LL5
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    mat = 1
    do i = 1, NAXREG
      key(i) = i
    end do
    floor_map = [1,2,3]
    area = 1.0_real32
    height = 1.0_real32
    volume = 1.0_real32
    call LCMPUT(root,'MATCOD',NAXREG,1,mat)
    call LCMPUT(root,'KEYFLX',NAXREG,1,key)
    call LCMPUT(root,'MAT1D',NFLOOR,1,floor_map)
    call LCMPUT(root,'AREA2D',NREG2D,2,area)
    call LCMPUT(root,'VOL1D',NFLOOR,2,height)
    call LCMPUT(root,'VOLUME',NAXREG,2,volume)
  end subroutine build_axial_track


  subroutine build_axial_macro(root)
    type(c_ptr), intent(in) :: root
    integer :: state(NSTATE), ig
    real(real32) :: nufission(NMAT)
    character(len=12) :: text12
    type(c_ptr) :: groups, group

    text12 = 'L_MACROLIB'
    call LCMPTC(root,'SIGNATURE',12,text12)
    state = 0
    state(1) = NGRP
    state(2) = NMAT
    state(4) = 1
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    nufission = 1.0_real32
    groups = LCMLID(root,'GROUP',NGRP)
    call assert_true(c_associated(groups),'AXIAL MACRO GROUP LIST')
    do ig = 1, NGRP
      group = LCMDIL(groups,ig)
      call LCMPUT(group,'NUSIGF',NMAT,2,nufission)
    end do
  end subroutine build_axial_macro


  subroutine build_axial_flux(root)
    type(c_ptr), intent(in) :: root
    integer :: state(NSTATE), ig
    real(real32) :: field32(NAXUNK)
    real(real64) :: field64(NAXUNK)
    character(len=12) :: text12
    type(c_ptr) :: flux32, flux64

    text12 = 'L_FLUX'
    call LCMPTC(root,'SIGNATURE',12,text12)
    state = 0
    state(1) = NGRP
    state(2) = NAXUNK
    call LCMPUT(root,'STATE-VECTOR',NSTATE,1,state)
    call LCMPUT(root,'K-EFFECTIVE',1,2,KEFF32)
    call LCMPUT(root,'SPOT-KEFF64',1,4,KEFF64)
    field32 = 0.0_real32
    field32(1:NAXREG) = 1.0_real32
    field64 = real(field32,real64)
    flux32 = LCMLID(root,'FLUX',NGRP)
    flux64 = LCMLID(root,'FLUX64',NGRP)
    call assert_true(c_associated(flux32) .and. c_associated(flux64), &
        'AXIAL FLUX LIST CREATE')
    do ig = 1, NGRP
      call LCMPDL(flux32,ig,NAXUNK,2,field32)
      call LCMPDL(flux64,ig,NAXUNK,4,field64)
    end do
  end subroutine build_axial_flux


  subroutine build_bootstrap_archive(root)
    type(c_ptr), intent(in) :: root
    integer :: ip, ig, state(NSTATE), key(NREG2D), anis(NREG2D)
    integer :: zones(NUNK), surface_key(NSURF), imerge(NMAT)
    real(real32) :: area(NREG2D), metric(NUNK), leakage(NGRP)
    real(real32) :: eps(5), flux_mirror(NUNK), source_mirror(NUNK)
    real(real64) :: flux_authority(NUNK), source_authority(NUNK)
    character(len=4) :: option
    character(len=12) :: text12
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: item, macro, groups, group, mirror_flux, mirror_source
    type(c_ptr) :: authority, authority_flux, authority_source

    text12 = 'L_ARCHIVE'
    call LCMPTC(root,'SIGNATURE',12,text12)
    call LCMPUT(root,'LISTDIM',1,1,NSNAP)
    call LCMPUT(root,'SPOT-ITER-K',1,4,KEFF64)
    tracks = LCMLID(root,'TRACK',NSNAP)
    libraries = LCMLID(root,'MICROLIB2',NSNAP)
    systems = LCMLID(root,'SYSTEM',NSNAP)
    fluxes = LCMLID(root,'FLUX',NSNAP)
    call assert_true(c_associated(tracks) .and. c_associated(libraries) &
        .and. c_associated(systems) .and. c_associated(fluxes), &
        'BOOTSTRAP ARCHIVE LIST CREATE')

    key = [1,2,3,4]
    anis = key
    zones = [1,1,1,1,0]
    surface_key = [NUNK]
    imerge = 1
    area = 1.0_real32
    metric = 1.0_real32
    leakage = 0.0_real32
    eps = 0.0_real32
    eps(1:3) = transfer(FROZEN_TOL_BITS,0.0_real32)
    flux_authority = [1.0_real64,1.0_real64,1.0_real64, &
        1.0_real64,0.5_real64]
    source_authority = 0.0_real64
    flux_mirror = real(flux_authority,real32)
    source_mirror = real(source_authority,real32)

    do ip = 1, NSNAP
      item = LCMDIL(tracks,ip)
      text12 = 'L_TRACK'
      call LCMPTC(item,'SIGNATURE',12,text12)
      text12 = 'MCCG'
      call LCMPTC(item,'TRACK-TYPE',12,text12)
      text12 = 'TRACK_f'
      call LCMPTC(item,'LINK.FTRACK',12,text12)
      state = 0
      state(1) = NREG2D
      state(2) = NUNK
      state(3) = 1
      state(4) = NMAT
      state(5) = NSURF
      state(6) = 1
      state(9) = 0
      state(14) = 4
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'VOLUME',NREG2D,2,area)
      call LCMPUT(item,'KEYFLX',NREG2D,1,key)
      call LCMPUT(item,'KEYFLX$ANIS',NREG2D,1,anis)
      call LCMPUT(item,'V$MCCG',NUNK,2,metric)
      call LCMPUT(item,'NZON$MCCG',NUNK,1,zones)
      call LCMPUT(item,'KEYCUR$MCCG',NSURF,1,surface_key)

      item = LCMDIL(libraries,ip)
      text12 = 'L_LIBRARY'
      call LCMPTC(item,'SIGNATURE',12,text12)
      state = 0
      state(1) = NMAT
      state(2) = 1
      state(3) = NGRP
      state(4) = 3
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      macro = LCMDID(item,'MACROLIB')
      text12 = 'L_MACROLIB'
      call LCMPTC(macro,'SIGNATURE',12,text12)
      state = 0
      state(1) = NGRP
      state(2) = NMAT
      state(3) = 3
      state(4) = NIFIS
      state(6) = 2
      state(13) = 0
      call LCMPUT(macro,'STATE-VECTOR',NSTATE,1,state)
      groups = LCMLID(macro,'GROUP',NGRP)
      do ig = 1, NGRP
        group = LCMDIL(groups,ig)
      end do

      item = LCMDIL(systems,ip)
      text12 = 'L_PIJ'
      call LCMPTC(item,'SIGNATURE',12,text12)
      text12 = 'MACRO0'
      call LCMPTC(item,'LINK.MACRO',12,text12)
      text12 = 'TRACK'
      call LCMPTC(item,'LINK.TRACK',12,text12)
      state = 0
      state(1:14) = [1,1,1,0,1,1,4,NGRP,NUNK,NMAT,1,0,0,0]
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage)
      call LCMPUT(item,'SPOT-L1-SNAP',1,1,ip)
      groups = LCMLID(item,'GROUP',NGRP)
      do ig = 1, NGRP
        group = LCMDIL(groups,ig)
      end do

      item = LCMDIL(fluxes,ip)
      text12 = 'L_FLUX'
      call LCMPTC(item,'SIGNATURE',12,text12)
      state = 0
      state(1:18) = [NGRP,NUNK,1,0,0,0,0,3,3,1,740,500, &
          0,0,0,0,NMAT,1]
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'EPS-CONVERGE',5,2,eps)
      call LCMPUT(item,'IMERGE-LEAK',NMAT,1,imerge)
      call LCMPUT(item,'KEYFLX',NREG2D,1,key)
      option = 'B0  '
      call LCMPTC(item,'OPTION',4,option)
      text12 = 'MACRO0'
      call LCMPTC(item,'LINK.MACRO',12,text12)
      text12 = 'TRACK'
      call LCMPTC(item,'LINK.TRACK',12,text12)
      text12 = 'SYSTEM'
      call LCMPTC(item,'LINK.SYSTEM',12,text12)
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage)
      mirror_flux = LCMLID(item,'FLUX',NGRP)
      mirror_source = LCMLID(item,'SOUR',NGRP)
      authority = LCMDID(item,'SPOT-R64')
      authority_flux = LCMLID(authority,'FLUX',NGRP)
      authority_source = LCMLID(authority,'SOUR',NGRP)
      do ig = 1, NGRP
        call LCMPDL(mirror_flux,ig,NUNK,2,flux_mirror)
        call LCMPDL(mirror_source,ig,NUNK,2,source_mirror)
        call LCMPDL(authority_flux,ig,NUNK,4,flux_authority)
        call LCMPDL(authority_source,ig,NUNK,4,source_authority)
      end do
    end do
  end subroutine build_bootstrap_archive


  subroutine build_identity_feedback(projected,feedback)
    type(c_ptr), intent(in) :: projected, feedback
    integer :: ip, ig, state(NSTATE), epoch, nplane
    real(real32) :: leakage32(NGRP), zero32(NUNK), fs_keff32
    real(real64) :: leakage64(NGRP), zero64(NUNK), rho64, iter_keff64
    character(len=12) :: text12
    type(c_ptr) :: source_tracks, source_libraries, source_fluxes
    type(c_ptr) :: tracks, libraries, systems, fluxes
    type(c_ptr) :: source_item, item, groups, group, authority
    type(c_ptr) :: source_list, authority_source, authority_qfiss
    type(c_ptr) :: legacy_outer, legacy_inner, root_authority

    leakage32 = 0.0_real32
    leakage64 = 0.0_real64
    zero32 = 0.0_real32
    zero64 = 0.0_real64
    fs_keff32 = KEFF32
    call LCMGET(projected,'SPOT-ITER-K',iter_keff64)
    root_authority = LCMGID(projected,'SPOT-R64')
    call LCMGET(root_authority,'RHO',rho64)
    call LCMGET(root_authority,'NPLANE',nplane)
    call LCMGET(root_authority,'EPOCH',epoch)
    call assert_true(nplane == NSNAP .and. epoch == 1, &
        'PROJECTED TEMPLATE EPOCH')

    text12 = 'L_ARCHIVE'
    call LCMPTC(feedback,'SIGNATURE',12,text12)
    call LCMPUT(feedback,'LISTDIM',1,1,NSNAP)
    call LCMPUT(feedback,'SPOT-ITER-K',1,4,iter_keff64)
    call LCMPUT(feedback,'SPOT-L1-ERR',1,2,0.0_real32)
    tracks = LCMLID(feedback,'TRACK',NSNAP)
    libraries = LCMLID(feedback,'MICROLIB2',NSNAP)
    systems = LCMLID(feedback,'SYSTEM',NSNAP)
    fluxes = LCMLID(feedback,'FLUX',NSNAP)
    source_tracks = LCMGID(projected,'TRACK')
    source_libraries = LCMGID(projected,'MICROLIB2')
    source_fluxes = LCMGID(projected,'FLUX')

    do ip = 1, NSNAP
      source_item = LCMGIL(source_tracks,ip)
      item = LCMDIL(tracks,ip)
      call LCMEQU(source_item,item)
      source_item = LCMGIL(source_libraries,ip)
      item = LCMDIL(libraries,ip)
      call LCMEQU(source_item,item)

      item = LCMDIL(systems,ip)
      text12 = 'L_PIJ'
      call LCMPTC(item,'SIGNATURE',12,text12)
      text12 = 'MACRO0'
      call LCMPTC(item,'LINK.MACRO',12,text12)
      text12 = 'TRACK'
      call LCMPTC(item,'LINK.TRACK',12,text12)
      state = 0
      state(1:14) = [1,1,1,0,1,1,4,NGRP,NUNK,NMAT,1,0,0,0]
      call LCMPUT(item,'STATE-VECTOR',NSTATE,1,state)
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage32)
      call LCMPUT(item,'SPOT-L1-SNAP',1,1,ip)
      groups = LCMLID(item,'GROUP',NGRP)
      do ig = 1, NGRP
        group = LCMDIL(groups,ig)
      end do
      authority = LCMDID(item,'SPOT-R64')
      call LCMPUT(authority,'RHO',1,4,rho64)
      text12 = 'ASSEMBLED'
      call LCMPTC(authority,'STATE',12,text12)
      call LCMPUT(authority,'EPOCH',1,1,epoch)

      source_item = LCMGIL(source_fluxes,ip)
      item = LCMDIL(fluxes,ip)
      call LCMEQU(source_item,item)
      call LCMPUT(item,'LEAK1D64',NGRP,4,leakage64)
      source_list = LCMLID(item,'SOUR',NGRP)
      legacy_outer = LCMLID(item,'SPOT-QFISS',1)
      legacy_inner = LCMLIL(legacy_outer,1,NGRP)
      call LCMPUT(item,'SPOT-FS-EQN',1,1,1)
      call LCMPUT(item,'SPOT-FS-K',1,2,fs_keff32)
      authority = LCMGID(item,'SPOT-R64')
      authority_source = LCMLID(authority,'SOUR',NGRP)
      authority_qfiss = LCMLID(authority,'QFISS',NGRP)
      text12 = 'SOLVED'
      call LCMPTC(authority,'STATE',12,text12)
      do ig = 1, NGRP
        call LCMPDL(source_list,ig,NUNK,2,zero32)
        call LCMPDL(legacy_inner,ig,NUNK,2,zero32)
        call LCMPDL(authority_source,ig,NUNK,4,zero64)
        call LCMPDL(authority_qfiss,ig,NUNK,4,zero64)
      end do
    end do

    root_authority = LCMDID(feedback,'SPOT-R64')
    call LCMPUT(root_authority,'NPLANE',1,1,NSNAP)
    text12 = 'RETURNED'
    call LCMPTC(root_authority,'STATE',12,text12)
    call LCMPUT(root_authority,'EPOCH',1,1,epoch)
  end subroutine build_identity_feedback


  subroutine check_axial_state(root,expected_state,expected_epoch)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: expected_state
    integer, intent(in) :: expected_epoch
    integer :: epoch_found
    integer :: rank_found(NGRP)
    character(len=12) :: state_found

    call LCMGTC(root,'SPOT-X-STATE',12,state_found)
    call LCMGET(root,'SPOT-X-EPOCH',epoch_found)
    call LCMGET(root,'SPOT-X-RANK',rank_found)
    call assert_true(state_found == expected_state, &
        'AXIAL LIFECYCLE STATE')
    call assert_true(epoch_found == expected_epoch,'AXIAL EPOCH')
    call assert_true(all(rank_found == NMODE_FULL),'AXIAL FULL RANK')
  end subroutine check_axial_state


  subroutine check_archive_state(root,expected_state,expected_epoch)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: expected_state
    integer, intent(in) :: expected_epoch
    integer :: epoch_found
    real(real64) :: iter_keff_found, rho_found
    character(len=12) :: state_found
    type(c_ptr) :: authority

    authority = LCMGID(root,'SPOT-R64')
    call assert_true(c_associated(authority),'ARCHIVE AUTHORITY EXISTS')
    call LCMGTC(authority,'STATE',12,state_found)
    call LCMGET(authority,'EPOCH',epoch_found)
    call LCMGET(authority,'RHO',rho_found)
    call LCMGET(root,'SPOT-ITER-K',iter_keff_found)
    call assert_true(state_found == expected_state, &
        'ARCHIVE LIFECYCLE STATE')
    call assert_true(epoch_found == expected_epoch,'ARCHIVE EPOCH')
    call assert_true(transfer(iter_keff_found,0_int64) == &
        transfer(KEFF64,0_int64),'ARCHIVE REAL64 KEFF BITS CHANGED')
    call assert_true(transfer(rho_found,0_int64) == &
        transfer(1.0_real64/KEFF64,0_int64), &
        'ARCHIVE REAL64 RHO BITS CHANGED')
  end subroutine check_archive_state


  subroutine check_real64_keff(root)
    type(c_ptr), intent(in) :: root
    real(real64) :: keff_found, rho_found

    call LCMGET(root,'SPOT-X-KEFF',keff_found)
    call LCMGET(root,'SPOT-X-RHO',rho_found)
    call assert_true(transfer(KEFF64,0_int64) /= &
        transfer(real(KEFF32,real64),0_int64), &
        'TEST KEFF DOES NOT EXERCISE REAL64 AUTHORITY')
    call assert_true(transfer(BAD_KEFF64,0_int64) /= &
        transfer(KEFF64,0_int64) .and. &
        transfer(real(BAD_KEFF64,real32),0_int32) == &
        transfer(KEFF32,0_int32), &
        'NEGATIVE KEFF IS NOT IN THE SAME REAL32 BIN')
    call assert_true(transfer(keff_found,0_int64) == &
        transfer(KEFF64,0_int64),'REAL64 KEFF BITS CHANGED')
    call assert_true(transfer(rho_found,0_int64) == &
        transfer(1.0_real64/KEFF64,0_int64),'REAL64 RHO BITS CHANGED')
  end subroutine check_real64_keff


  subroutine assert_true(condition,message)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: message

    if (.not. condition) then
      write(error_unit,'(A)') 'FULL-RANK PICARD CYCLE FAIL: '//trim(message)
      error stop 1
    end if
  end subroutine assert_true

end program test_full_rank_picard_cycle


subroutine REDGET(indic,nitma,flott,text4,dflott)
  implicit none
  integer :: indic, nitma
  real :: flott
  character(len=*) :: text4
  double precision :: dflott

  indic = 3
  nitma = 0
  flott = 0.0
  text4 = ';'
  dflott = 0.0d0
end subroutine REDGET
