program CHECK_B2M_THREE_PLANE_COMMIT
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NSTATE=40
  integer, parameter :: NGRP=370
  integer, parameter :: NSNAP=3
  integer, parameter :: NREG=8
  integer, parameter :: NUNKNO=14
  integer, parameter :: NMAT=8
  integer(int32), parameter :: REAL32_MAGNITUDE_MASK = &
      int(z'7fffffff',int32)
  integer(int32), parameter :: FROZEN_TOL_BITS = &
      int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64 = &
      real(huge(0.0_real32),real64)
  character(len=12), parameter :: PROJECTED_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
       'TRACK','MICROLIB2','FLUX','SPOT-R64']
  character(len=12), parameter :: ASSEMBLED_ROOT_NAMES(8) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
       'TRACK','MICROLIB2','SYSTEM','FLUX','SPOT-R64']
  character(len=12), parameter :: ROOT_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
  character(len=12), parameter :: PLANE_ROOT_NAMES(12) = &
      [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
       'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
       'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D']
  character(len=12), parameter :: PLANE_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','FLUX','STATE','EPOCH']
  character(len=12), parameter :: SYSTEM_ROOT_NAMES(8) = &
      [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
       'STATE-VECTOR','SPOT-LEAK1D','SPOT-L1-SNAP','GROUP','SPOT-R64']
  character(len=12), parameter :: SYSTEM_AUTHORITY_NAMES(3) = &
      [character(len=12) :: 'RHO','STATE','EPOCH']
  character(len=12), parameter :: GROUP_NAMES(15) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
       'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG', &
       'DRAGON-TXSC','SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG']
  character(len=12), parameter :: RESPONSE_NAMES(12) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG', &
       'PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG', &
       'DIAGF$MCCG']
  integer, parameter :: RESPONSE_LENGTHS(12) = &
      [32,14,32,14,8,8,8,8,8,8,8,14]

  character(len=1024) :: projected_path, assembled_path
  integer :: copied_items, group_records, response_values
  integer :: tx_checks, sphys_checks, sused_checks, leakage_checks
  integer :: system_states, flux_states
  integer :: response_nonzero_by_plane(NSNAP)
  integer(int64) :: full_copy_records, full_copy_words
  real(real64) :: rho
  type(c_ptr) :: projected, assembled

  if (command_argument_count() /= 2) error stop &
      'expected PROJECTED and ASSEMBLED XSM paths'
  call get_command_argument(1,projected_path)
  call get_command_argument(2,assembled_path)

  call LCMOP(projected,trim(projected_path),2,2,0)
  call LCMOP(assembled,trim(assembled_path),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'persistent PROJECTED archive')
  call REQUIRE_ASSOCIATED(assembled,'persistent ASSEMBLED archive')
  if (c_associated(projected,assembled)) &
      error stop 'PROJECTED and ASSEMBLED archive handles alias'

  call VERIFY_ASSEMBLED_ARCHIVE(projected,assembled,rho)
  call VERIFY_PLANE_LIFECYCLES(projected,assembled,rho,flux_states)
  call VERIFY_COPIED_SUBTREES(projected,assembled,full_copy_records, &
      full_copy_words,copied_items)
  call VERIFY_ASSEMBLED_SYSTEMS(assembled,rho,tx_checks,sphys_checks, &
      sused_checks,leakage_checks,response_values, &
      response_nonzero_by_plane,group_records,system_states)

  call LCMCL(assembled,1)
  call LCMCL(projected,1)

  if (copied_items /= 3*NSNAP) &
      error stop 'copied-list item inventory differs'
  if (full_copy_records <= 0_int64 .or. full_copy_words <= 0_int64) &
      error stop 'recursive full-copy inventory is empty'
  if (group_records /= NSNAP*NGRP*size(GROUP_NAMES)) &
      error stop 'group-record inventory differs'
  if (response_values /= NSNAP*NGRP*sum(RESPONSE_LENGTHS)) &
      error stop 'response-value inventory differs'
  if (any(response_nonzero_by_plane <= 0)) &
      error stop 'one or more planes have an all-zero response payload'
  if (tx_checks /= NSNAP*NGRP*(NMAT+1)) &
      error stop 'TX bit-check inventory differs'
  if (sphys_checks /= NSNAP*NGRP*(NMAT+1)) &
      error stop 'S0 physical bit-check inventory differs'
  if (sused_checks /= NSNAP*NGRP*(NMAT+1)) &
      error stop 'S0 used bit-check inventory differs'
  if (leakage_checks /= NSNAP*NGRP) &
      error stop 'leakage bit-check inventory differs'
  if (system_states /= NSNAP .or. flux_states /= NSNAP) &
      error stop 'lifecycle inventory differs'

  write(*,'(A)') 'B2M THREE-PLANE COMMIT POSTERIOR PASS'
  write(*,'(A,I0,A,I0,A)') 'B2M ROOT-ENTRIES=', &
      size(ASSEMBLED_ROOT_NAMES),' SYSTEMS=',NSNAP, &
      ' ROOT-STATE=ASSEMBLED/1'
  write(*,'(A,I0,A,I0,A,I0)') 'B2M COPIED-LIST-ITEMS=',copied_items, &
      ' FULL-COPY-RECORDS=',full_copy_records, &
      ' FULL-COPY-32BIT-WORDS=',full_copy_words
  write(*,'(A,I0,A,I0)') 'B2M GROUPS=',NSNAP*NGRP, &
      ' EXACT-GROUP-RECORDS=',group_records
  write(*,'(A,I0,A,I0)') 'B2M RESPONSE-FINITE-VALUES=',response_values, &
      ' RESPONSE-NONZERO-VALUES=',sum(response_nonzero_by_plane)
  write(*,'(A,I0,A,I0,A,I0)') 'B2M PLANE1-NONZERO=', &
      response_nonzero_by_plane(1),' PLANE2-NONZERO=', &
      response_nonzero_by_plane(2),' PLANE3-NONZERO=', &
      response_nonzero_by_plane(3)
  write(*,'(A,I0,A,I0,A,I0,A,I0)') 'B2M LEAKAGE-BITS=',leakage_checks, &
      ' TXSC-BITS=',tx_checks,' S0PHYS-BITS=',sphys_checks, &
      ' S0USED-BITS=',sused_checks
  write(*,'(A,I0,A,I0)') 'B2M SYSTEM-STATES=ASSEMBLED/1x', &
      system_states,' FLUX-STATES=PROJECTED/1x',flux_states
  write(*,'(A)') &
      'B2M THREE-PLANE-B2K-POSTERIOR=COMPATIBLE EMPIRICAL-CONTROLS=0'
  write(*,'(A)') &
      'B2M RESPONSE-ACCURACY=NOT-EVALUATED CONVERGENCE=NOT-EVALUATED'

contains

  subroutine VERIFY_ASSEMBLED_ARCHIVE(input_root,output_root,root_rho)
    type(c_ptr), intent(in) :: input_root, output_root
    real(real64), intent(out) :: root_rho

    integer :: input_planes, output_planes, input_epoch, output_epoch
    integer(int64) :: input_bits, output_bits, expected_bits
    real(real64) :: input_keff, output_keff, output_rho
    type(c_ptr) :: input_authority, output_authority

    if (.not. EXACT_INVENTORY(input_root,PROJECTED_ROOT_NAMES)) &
        error stop 'PROJECTED root inventory differs'
    if (.not. EXACT_INVENTORY(output_root,ASSEMBLED_ROOT_NAMES)) &
        error stop 'ASSEMBLED root inventory differs'
    call REQUIRE_CHARACTER12(input_root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_CHARACTER12(output_root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_RECORD(input_root,'LISTDIM',1,1)
    call REQUIRE_RECORD(output_root,'LISTDIM',1,1)
    call LCMGET(input_root,'LISTDIM',input_planes)
    call LCMGET(output_root,'LISTDIM',output_planes)
    if (input_planes /= NSNAP .or. output_planes /= NSNAP) &
        error stop 'archive plane count differs'
    call REQUIRE_RECORD(input_root,'SPOT-ITER-K',1,4)
    call REQUIRE_RECORD(output_root,'SPOT-ITER-K',1,4)
    call LCMGET(input_root,'SPOT-ITER-K',input_keff)
    call LCMGET(output_root,'SPOT-ITER-K',output_keff)
    if (.not. ieee_is_finite(input_keff) .or. input_keff <= 0.0_real64) &
        error stop 'PROJECTED iteration eigenvalue is invalid'
    input_bits=transfer(input_keff,0_int64)
    output_bits=transfer(output_keff,0_int64)
    if (output_bits /= input_bits) &
        error stop 'iteration eigenvalue bits changed at commit'

    call REQUIRE_RECORD(input_root,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(input_root,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(input_root,'FLUX',NSNAP,10)
    call REQUIRE_ABSENT(input_root,'SYSTEM')
    call REQUIRE_RECORD(output_root,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(output_root,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(output_root,'SYSTEM',NSNAP,10)
    call REQUIRE_RECORD(output_root,'FLUX',NSNAP,10)

    call REQUIRE_RECORD(input_root,'SPOT-R64',-1,0)
    call REQUIRE_RECORD(output_root,'SPOT-R64',-1,0)
    input_authority=LCMGID(input_root,'SPOT-R64')
    output_authority=LCMGID(output_root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(input_authority,'PROJECTED root authority')
    call REQUIRE_ASSOCIATED(output_authority,'ASSEMBLED root authority')
    if (.not. EXACT_INVENTORY(input_authority,ROOT_AUTHORITY_NAMES)) &
        error stop 'PROJECTED root authority inventory differs'
    if (.not. EXACT_INVENTORY(output_authority,ROOT_AUTHORITY_NAMES)) &
        error stop 'ASSEMBLED root authority inventory differs'
    call REQUIRE_RECORD(input_authority,'RHO',1,4)
    call REQUIRE_RECORD(output_authority,'RHO',1,4)
    call REQUIRE_RECORD(input_authority,'NPLANE',1,1)
    call REQUIRE_RECORD(output_authority,'NPLANE',1,1)
    call REQUIRE_CHARACTER12(input_authority,'STATE','PROJECTED')
    call REQUIRE_CHARACTER12(output_authority,'STATE','ASSEMBLED')
    call REQUIRE_RECORD(input_authority,'EPOCH',1,1)
    call REQUIRE_RECORD(output_authority,'EPOCH',1,1)
    call LCMGET(input_authority,'RHO',root_rho)
    call LCMGET(output_authority,'RHO',output_rho)
    call LCMGET(input_authority,'NPLANE',input_planes)
    call LCMGET(output_authority,'NPLANE',output_planes)
    call LCMGET(input_authority,'EPOCH',input_epoch)
    call LCMGET(output_authority,'EPOCH',output_epoch)
    if (.not. ieee_is_finite(root_rho) .or. root_rho <= 0.0_real64) &
        error stop 'PROJECTED root RHO is invalid'
    if (transfer(output_rho,0_int64) /= transfer(root_rho,0_int64)) &
        error stop 'root RHO bits changed at commit'
    expected_bits=transfer(1.0_real64/input_keff,0_int64)
    if (transfer(root_rho,0_int64) /= expected_bits) &
        error stop 'root RHO is not bitwise reciprocal of eigenvalue'
    if (input_planes /= NSNAP .or. output_planes /= NSNAP) &
        error stop 'root authority plane count differs'
    if (input_epoch /= 1 .or. output_epoch /= 1) &
        error stop 'root lifecycle epoch differs'
  end subroutine VERIFY_ASSEMBLED_ARCHIVE


  subroutine VERIFY_PLANE_LIFECYCLES(input_root,output_root,root_rho, &
      state_count)
    type(c_ptr), intent(in) :: input_root, output_root
    real(real64), intent(in) :: root_rho
    integer, intent(out) :: state_count

    integer :: ip, keyflx(NREG)
    type(c_ptr) :: input_fluxes, output_fluxes, tracks
    type(c_ptr) :: input_plane, output_plane, track

    input_fluxes=LCMGID(input_root,'FLUX')
    output_fluxes=LCMGID(output_root,'FLUX')
    tracks=LCMGID(input_root,'TRACK')
    call REQUIRE_ASSOCIATED(input_fluxes,'PROJECTED FLUX list')
    call REQUIRE_ASSOCIATED(output_fluxes,'ASSEMBLED FLUX list')
    call REQUIRE_ASSOCIATED(tracks,'PROJECTED TRACK list')
    state_count=0
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(tracks,ip)
      track=LCMGIL(tracks,ip)
      call REQUIRE_RECORD(track,'KEYFLX',NREG,1)
      call LCMGET(track,'KEYFLX',keyflx)
      call REQUIRE_DIRECTORY_ITEM(input_fluxes,ip)
      call REQUIRE_DIRECTORY_ITEM(output_fluxes,ip)
      input_plane=LCMGIL(input_fluxes,ip)
      output_plane=LCMGIL(output_fluxes,ip)
      call VERIFY_PROJECTED_PLANE(input_plane,root_rho,keyflx)
      call VERIFY_PROJECTED_PLANE(output_plane,root_rho,keyflx)
      state_count=state_count+1
    end do
  end subroutine VERIFY_PLANE_LIFECYCLES


  subroutine VERIFY_PROJECTED_PLANE(plane,root_rho,expected_keyflx)
    type(c_ptr), intent(in) :: plane
    real(real64), intent(in) :: root_rho
    integer, intent(in) :: expected_keyflx(NREG)

    integer :: state(NSTATE), expected_state(NSTATE)
    integer :: imerge(NMAT), keyflx(NREG), epoch, ig
    integer(int32) :: eps_bits(5)
    real(real32) :: eps(5), leakage(NGRP), mirror(NUNKNO)
    real(real64) :: plane_rho, authority_flux(NUNKNO)
    type(c_ptr) :: authority, mirror_fluxes, authority_fluxes

    if (.not. EXACT_INVENTORY(plane,PLANE_ROOT_NAMES)) &
        error stop 'PROJECTED plane root inventory differs'
    call REQUIRE_CHARACTER12(plane,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(plane,'STATE-VECTOR',NSTATE,1)
    call LCMGET(plane,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:18)=[NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1]
    if (any(state /= expected_state)) &
        error stop 'PROJECTED plane state vector differs'
    call REQUIRE_RECORD(plane,'EPS-CONVERGE',5,2)
    call LCMGET(plane,'EPS-CONVERGE',eps)
    if (.not. all(ieee_is_finite(eps))) &
        error stop 'PROJECTED convergence metadata is nonfinite'
    eps_bits=transfer(eps,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS) .or. &
        any(eps_bits(4:5) /= 0_int32)) &
        error stop 'PROJECTED convergence metadata bits differ'
    call REQUIRE_RECORD(plane,'IMERGE-LEAK',NMAT,1)
    call LCMGET(plane,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) error stop 'PROJECTED leakage merge differs'
    call REQUIRE_RECORD(plane,'KEYFLX',NREG,1)
    call LCMGET(plane,'KEYFLX',keyflx)
    if (any(keyflx /= expected_keyflx)) &
        error stop 'PROJECTED KEYFLX differs from TRACK'
    call REQUIRE_CHARACTER_N(plane,'OPTION',1,4,'B0  ')
    call REQUIRE_CHARACTER12(plane,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(plane,'LINK.TRACK','TRACK')
    call REQUIRE_CHARACTER12(plane,'LINK.SYSTEM','SYSTEM')
    call REQUIRE_RECORD(plane,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(plane,'SPOT-LEAK1D',leakage)
    if (.not. all(ieee_is_finite(leakage))) &
        error stop 'PROJECTED leakage is nonfinite'

    call REQUIRE_RECORD(plane,'SPOT-R64',-1,0)
    authority=LCMGID(plane,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'PROJECTED plane authority')
    if (.not. EXACT_INVENTORY(authority,PLANE_AUTHORITY_NAMES)) &
        error stop 'PROJECTED plane authority inventory differs'
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','PROJECTED')
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(plane,'FLUX',NGRP,10)
    call LCMGET(authority,'RHO',plane_rho)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(plane_rho)) &
        error stop 'PROJECTED plane RHO is nonfinite'
    if (transfer(plane_rho,0_int64) /= transfer(root_rho,0_int64)) &
        error stop 'PROJECTED plane RHO bits differ from root'
    if (epoch /= 1) error stop 'PROJECTED plane epoch differs'
    authority_fluxes=LCMGID(authority,'FLUX')
    mirror_fluxes=LCMGID(plane,'FLUX')
    call REQUIRE_ASSOCIATED(authority_fluxes,'REAL64 projected FLUX list')
    call REQUIRE_ASSOCIATED(mirror_fluxes,'REAL32 projected FLUX list')
    do ig=1,NGRP
      call REQUIRE_LIST_RECORD(authority_fluxes,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(mirror_fluxes,ig,NUNKNO,2)
      call LCMGDL(authority_fluxes,ig,authority_flux)
      call LCMGDL(mirror_fluxes,ig,mirror)
      if (.not. all(ieee_is_finite(authority_flux)) .or. &
          .not. all(ieee_is_finite(mirror))) &
          error stop 'PROJECTED flux payload is nonfinite'
      if (any(abs(authority_flux) > REAL32_MAX64)) &
          error stop 'PROJECTED REAL64 flux is outside REAL32 range'
      if (any(transfer(mirror,0_int32,NUNKNO) /= &
          transfer(real(authority_flux,real32),0_int32,NUNKNO))) &
          error stop 'PROJECTED REAL32 mirror bits differ'
    end do
  end subroutine VERIFY_PROJECTED_PLANE


  subroutine VERIFY_COPIED_SUBTREES(input_root,output_root,record_count, &
      word_count,item_count)
    type(c_ptr), intent(in) :: input_root, output_root
    integer(int64), intent(out) :: record_count, word_count
    integer, intent(out) :: item_count

    character(len=12), parameter :: names(3) = &
        [character(len=12) :: 'TRACK','MICROLIB2','FLUX']
    integer :: i
    type(c_ptr) :: input_list, output_list

    record_count=0_int64
    word_count=0_int64
    item_count=0
    do i=1,size(names)
      call REQUIRE_RECORD(input_root,names(i),NSNAP,10)
      call REQUIRE_RECORD(output_root,names(i),NSNAP,10)
      input_list=LCMGID(input_root,names(i))
      output_list=LCMGID(output_root,names(i))
      call REQUIRE_ASSOCIATED(input_list,'PROJECTED copied list')
      call REQUIRE_ASSOCIATED(output_list,'ASSEMBLED copied list')
      call COMPARE_LIST(input_list,output_list,NSNAP,record_count, &
          word_count)
      item_count=item_count+NSNAP
    end do
  end subroutine VERIFY_COPIED_SUBTREES


  subroutine VERIFY_ASSEMBLED_SYSTEMS(root,root_rho,tx_checks, &
      sphys_checks,sused_checks,leakage_checks,response_count, &
      nonzero_count,record_count,state_count)
    type(c_ptr), intent(in) :: root
    real(real64), intent(in) :: root_rho
    integer, intent(out) :: tx_checks, sphys_checks, sused_checks
    integer, intent(out) :: leakage_checks
    integer, intent(out) :: response_count, nonzero_count(NSNAP)
    integer, intent(out) :: record_count, state_count

    integer :: ip, ig, im, i, epoch, snapshot
    integer :: state(NSTATE), expected_state(NSTATE)
    real(real64) :: system_rho
    real(real32) :: leakage(NGRP), system_leakage(NGRP)
    real(real32) :: ntot(NMAT), sigw(NMAT), tranc(NMAT)
    real(real32) :: tx(0:NMAT), sphys(0:NMAT), sused(0:NMAT)
    real(real32) :: expected_tx(0:NMAT), expected_sphys(0:NMAT)
    real(real32) :: expected_sused(0:NMAT)
    real(real32), allocatable :: response(:)
    type(c_ptr) :: systems, fluxes, libraries
    type(c_ptr) :: system_root, authority, plane, library, macro
    type(c_ptr) :: system_groups, macro_groups, system_group, macro_group

    systems=LCMGID(root,'SYSTEM')
    fluxes=LCMGID(root,'FLUX')
    libraries=LCMGID(root,'MICROLIB2')
    call REQUIRE_ASSOCIATED(systems,'ASSEMBLED SYSTEM list')
    call REQUIRE_ASSOCIATED(fluxes,'ASSEMBLED FLUX list')
    call REQUIRE_ASSOCIATED(libraries,'ASSEMBLED MICROLIB2 list')
    tx_checks=0
    sphys_checks=0
    sused_checks=0
    leakage_checks=0
    response_count=0
    nonzero_count=0
    record_count=0
    state_count=0
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(systems,ip)
      call REQUIRE_DIRECTORY_ITEM(fluxes,ip)
      call REQUIRE_DIRECTORY_ITEM(libraries,ip)
      system_root=LCMGIL(systems,ip)
      plane=LCMGIL(fluxes,ip)
      library=LCMGIL(libraries,ip)
      if (.not. EXACT_INVENTORY(system_root,SYSTEM_ROOT_NAMES)) &
          error stop 'ASSEMBLED SYSTEM root inventory differs'
      call REQUIRE_CHARACTER12(system_root,'SIGNATURE','L_PIJ')
      call REQUIRE_CHARACTER12(system_root,'LINK.MACRO','MACRO0')
      call REQUIRE_CHARACTER12(system_root,'LINK.TRACK','TRACK')
      call REQUIRE_RECORD(system_root,'STATE-VECTOR',NSTATE,1)
      call LCMGET(system_root,'STATE-VECTOR',state)
      expected_state=0
      expected_state([1,2,3,5,6,11])=1
      expected_state(7)=4
      expected_state(8)=NGRP
      expected_state(9)=NUNKNO
      expected_state(10)=NMAT
      if (any(state /= expected_state)) &
          error stop 'ASSEMBLED SYSTEM state vector differs'
      call REQUIRE_RECORD(system_root,'SPOT-L1-SNAP',1,1)
      call LCMGET(system_root,'SPOT-L1-SNAP',snapshot)
      if (snapshot /= ip) error stop 'ASSEMBLED SYSTEM plane differs'
      call REQUIRE_RECORD(system_root,'SPOT-LEAK1D',NGRP,2)
      call REQUIRE_RECORD(plane,'SPOT-LEAK1D',NGRP,2)
      call LCMGET(system_root,'SPOT-LEAK1D',system_leakage)
      call LCMGET(plane,'SPOT-LEAK1D',leakage)
      if (.not. all(ieee_is_finite(system_leakage))) &
          error stop 'ASSEMBLED SYSTEM leakage is nonfinite'
      if (any(transfer(system_leakage,0_int32,NGRP) /= &
          transfer(leakage,0_int32,NGRP))) &
          error stop 'SYSTEM leakage bits differ from same-index FLUX'
      leakage_checks=leakage_checks+NGRP

      call REQUIRE_RECORD(system_root,'SPOT-R64',-1,0)
      authority=LCMGID(system_root,'SPOT-R64')
      call REQUIRE_ASSOCIATED(authority,'ASSEMBLED SYSTEM authority')
      if (.not. EXACT_INVENTORY(authority,SYSTEM_AUTHORITY_NAMES)) &
          error stop 'ASSEMBLED SYSTEM authority inventory differs'
      call REQUIRE_RECORD(authority,'RHO',1,4)
      call REQUIRE_CHARACTER12(authority,'STATE','ASSEMBLED')
      call REQUIRE_RECORD(authority,'EPOCH',1,1)
      call LCMGET(authority,'RHO',system_rho)
      call LCMGET(authority,'EPOCH',epoch)
      if (.not. ieee_is_finite(system_rho)) &
          error stop 'ASSEMBLED SYSTEM RHO is nonfinite'
      if (transfer(system_rho,0_int64) /= transfer(root_rho,0_int64)) &
          error stop 'ASSEMBLED SYSTEM RHO bits differ from root'
      if (epoch /= 1) error stop 'ASSEMBLED SYSTEM epoch differs'
      state_count=state_count+1

      call REQUIRE_RECORD(system_root,'GROUP',NGRP,10)
      call REQUIRE_RECORD(library,'MACROLIB',-1,0)
      macro=LCMGID(library,'MACROLIB')
      call REQUIRE_ASSOCIATED(macro,'same-index MACROLIB')
      call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
      system_groups=LCMGID(system_root,'GROUP')
      macro_groups=LCMGID(macro,'GROUP')
      call REQUIRE_ASSOCIATED(system_groups,'ASSEMBLED SYSTEM groups')
      call REQUIRE_ASSOCIATED(macro_groups,'same-index MACROLIB groups')
      do ig=1,NGRP
        call REQUIRE_DIRECTORY_ITEM(system_groups,ig)
        call REQUIRE_DIRECTORY_ITEM(macro_groups,ig)
        system_group=LCMGIL(system_groups,ig)
        macro_group=LCMGIL(macro_groups,ig)
        if (.not. EXACT_INVENTORY(system_group,GROUP_NAMES)) &
            error stop 'ASSEMBLED SYSTEM group inventory differs'
        call REQUIRE_ABSENT(system_group,'FUNKNO$USS')
        record_count=record_count+size(GROUP_NAMES)

        call REQUIRE_RECORD(macro_group,'NTOT0',NMAT,2)
        call REQUIRE_RECORD(macro_group,'SIGW00',NMAT,2)
        call REQUIRE_RECORD(macro_group,'TRANC',NMAT,2)
        call LCMGET(macro_group,'NTOT0',ntot)
        call LCMGET(macro_group,'SIGW00',sigw)
        call LCMGET(macro_group,'TRANC',tranc)
        if (.not. all(ieee_is_finite(ntot)) .or. &
            .not. all(ieee_is_finite(sigw)) .or. &
            .not. all(ieee_is_finite(tranc))) &
            error stop 'same-index formula input is nonfinite'

        call REQUIRE_RECORD(system_group,'DRAGON-TXSC',NMAT+1,2)
        call REQUIRE_RECORD(system_group,'SPOT-S0-PHYS',NMAT+1,2)
        call REQUIRE_RECORD(system_group,'DRAGON-S0XSC',NMAT+1,2)
        call LCMGET(system_group,'DRAGON-TXSC',tx)
        call LCMGET(system_group,'SPOT-S0-PHYS',sphys)
        call LCMGET(system_group,'DRAGON-S0XSC',sused)
        expected_tx=+0.0_real32
        expected_sphys=+0.0_real32
        expected_sused=+0.0_real32
        expected_sused(0)=expected_sphys(0)-leakage(ig)
        do im=1,NMAT
          expected_tx(im)=ntot(im)
          expected_sphys(im)=sigw(im)
          expected_tx(im)=expected_tx(im)-tranc(im)
          expected_sphys(im)=expected_sphys(im)-tranc(im)
          expected_sused(im)=expected_sphys(im)-leakage(ig)
        end do
        if (.not. all(ieee_is_finite(expected_tx)) .or. &
            .not. all(ieee_is_finite(expected_sphys)) .or. &
            .not. all(ieee_is_finite(expected_sused))) &
            error stop 'ordered binary32 formula result is nonfinite'
        if (any(transfer(tx,0_int32,NMAT+1) /= &
            transfer(expected_tx,0_int32,NMAT+1))) &
            error stop 'TX ordered binary32 formula differs'
        if (any(transfer(sphys,0_int32,NMAT+1) /= &
            transfer(expected_sphys,0_int32,NMAT+1))) &
            error stop 'S0 physical ordered binary32 formula differs'
        if (any(transfer(sused,0_int32,NMAT+1) /= &
            transfer(expected_sused,0_int32,NMAT+1))) &
            error stop 'S0 used ordered binary32 formula differs'
        tx_checks=tx_checks+NMAT+1
        sphys_checks=sphys_checks+NMAT+1
        sused_checks=sused_checks+NMAT+1

        do i=1,size(RESPONSE_NAMES)
          call REQUIRE_RECORD(system_group,RESPONSE_NAMES(i), &
              RESPONSE_LENGTHS(i),2)
          allocate(response(RESPONSE_LENGTHS(i)))
          call LCMGET(system_group,RESPONSE_NAMES(i),response)
          if (.not. all(ieee_is_finite(response))) &
              error stop 'real response payload is nonfinite'
          response_count=response_count+size(response)
          ! Clear only the IEEE sign bit.  Both signed zeros then count as
          ! zero, while every other finite binary32 value remains nonzero.
          nonzero_count(ip)=nonzero_count(ip)+count(iand( &
              transfer(response,0_int32,size(response)), &
              REAL32_MAGNITUDE_MASK) /= 0_int32)
          deallocate(response)
        end do
      end do
    end do
  end subroutine VERIFY_ASSEMBLED_SYSTEMS


  recursive subroutine COMPARE_DICTIONARY(left,right,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer(int64), intent(inout) :: record_count, word_count
    character(len=12) :: first_name, name
    integer :: left_count, right_count, left_length, right_length
    integer :: left_type, right_type
    type(c_ptr) :: left_child, right_child

    call COUNT_DICTIONARY_NAMES(left,left_count)
    call COUNT_DICTIONARY_NAMES(right,right_count)
    if (left_count /= right_count) &
        error stop 'full-copy directory count differs'
    if (left_count == 0) return
    name=' '
    call LCMNXT(left,name)
    first_name=name
    do
      call LCMLEN(left,name,left_length,left_type)
      call LCMLEN(right,name,right_length,right_type)
      if (left_length /= right_length .or. left_type /= right_type) &
          error stop 'full-copy named schema differs'
      select case(left_type)
      case(0)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied directory')
        call REQUIRE_ASSOCIATED(right_child,'right copied directory')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied list')
        call REQUIRE_ASSOCIATED(right_child,'right copied list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count, &
            word_count)
      case default
        call COMPARE_NAMED_RECORD(left,right,name,left_length,left_type, &
            record_count,word_count)
      end select
      call LCMNXT(left,name)
      if (name == first_name) exit
    end do
  end subroutine COMPARE_DICTIONARY


  recursive subroutine COMPARE_LIST(left,right,length,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: length
    integer(int64), intent(inout) :: record_count, word_count
    integer :: index, left_length, right_length, left_type, right_type
    type(c_ptr) :: left_child, right_child

    do index=1,length
      call LCMLEL(left,index,left_length,left_type)
      call LCMLEL(right,index,right_length,right_type)
      if (left_length /= right_length .or. left_type /= right_type) &
          error stop 'full-copy list-item schema differs'
      select case(left_type)
      case(0)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left copied list directory')
        call REQUIRE_ASSOCIATED(right_child,'right copied list directory')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left copied nested list')
        call REQUIRE_ASSOCIATED(right_child,'right copied nested list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count, &
            word_count)
      case default
        call COMPARE_LIST_RECORD(left,right,index,left_length,left_type, &
            record_count,word_count)
      end select
    end do
  end subroutine COMPARE_LIST


  subroutine COMPARE_NAMED_RECORD(left,right,name,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: length, record_type
    integer(int64), intent(inout) :: record_count, word_count

    integer, allocatable :: integer_left(:), integer_right(:)
    real(real32), allocatable :: real_left(:), real_right(:)
    real(real64), allocatable :: double_left(:), double_right(:)
    logical, allocatable :: logical_left(:), logical_right(:)
    complex(real32), allocatable :: complex_left(:), complex_right(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(integer_left(length),integer_right(length))
      call LCMGET(left,name,integer_left)
      call LCMGET(right,name,integer_right)
      if (any(integer_left /= integer_right)) &
          error stop 'full-copy integer or character bits differ'
      word_count=word_count+length
    case(2)
      allocate(real_left(length),real_right(length))
      call LCMGET(left,name,real_left)
      call LCMGET(right,name,real_right)
      if (any(transfer(real_left,0_int32,length) /= &
          transfer(real_right,0_int32,length))) &
          error stop 'full-copy REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(double_left(length),double_right(length))
      call LCMGET(left,name,double_left)
      call LCMGET(right,name,double_right)
      if (any(transfer(double_left,0_int64,length) /= &
          transfer(double_right,0_int64,length))) &
          error stop 'full-copy REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(logical_left(length),logical_right(length))
      call LCMGET(left,name,logical_left)
      call LCMGET(right,name,logical_right)
      if (any(transfer(logical_left,0_int32,length) /= &
          transfer(logical_right,0_int32,length))) &
          error stop 'full-copy logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(complex_left(length),complex_right(length))
      call LCMGET(left,name,complex_left)
      call LCMGET(right,name,complex_right)
      if (any(transfer(complex_left,0_int32,2*length) /= &
          transfer(complex_right,0_int32,2*length))) &
          error stop 'full-copy complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported full-copy GANLIB record type'
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_NAMED_RECORD


  subroutine COMPARE_LIST_RECORD(left,right,index,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: index, length, record_type
    integer(int64), intent(inout) :: record_count, word_count

    integer, allocatable :: integer_left(:), integer_right(:)
    real(real32), allocatable :: real_left(:), real_right(:)
    real(real64), allocatable :: double_left(:), double_right(:)
    logical, allocatable :: logical_left(:), logical_right(:)
    complex(real32), allocatable :: complex_left(:), complex_right(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(integer_left(length),integer_right(length))
      call LCMGDL(left,index,integer_left)
      call LCMGDL(right,index,integer_right)
      if (any(integer_left /= integer_right)) &
          error stop 'full-copy list integer or character bits differ'
      word_count=word_count+length
    case(2)
      allocate(real_left(length),real_right(length))
      call LCMGDL(left,index,real_left)
      call LCMGDL(right,index,real_right)
      if (any(transfer(real_left,0_int32,length) /= &
          transfer(real_right,0_int32,length))) &
          error stop 'full-copy list REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(double_left(length),double_right(length))
      call LCMGDL(left,index,double_left)
      call LCMGDL(right,index,double_right)
      if (any(transfer(double_left,0_int64,length) /= &
          transfer(double_right,0_int64,length))) &
          error stop 'full-copy list REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(logical_left(length),logical_right(length))
      call LCMGDL(left,index,logical_left)
      call LCMGDL(right,index,logical_right)
      if (any(transfer(logical_left,0_int32,length) /= &
          transfer(logical_right,0_int32,length))) &
          error stop 'full-copy list logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(complex_left(length),complex_right(length))
      call LCMGDL(left,index,complex_left)
      call LCMGDL(right,index,complex_right)
      if (any(transfer(complex_left,0_int32,2*length) /= &
          transfer(complex_right,0_int32,2*length))) &
          error stop 'full-copy list complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported full-copy GANLIB list-item type'
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_LIST_RECORD


  subroutine COUNT_DICTIONARY_NAMES(root,result_count)
    type(c_ptr), intent(in) :: root
    integer, intent(out) :: result_count
    character(len=12) :: first_name, name

    result_count=0
    name=' '
    call LCMNXT(root,name)
    if (name == ' ') return
    first_name=name
    do
      result_count=result_count+1
      call LCMNXT(root,name)
      if (name == first_name) exit
    end do
  end subroutine COUNT_DICTIONARY_NAMES


  logical function EXACT_INVENTORY(root,expected_names)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, name
    logical, allocatable :: found(:)
    integer :: count_names, index

    EXACT_INVENTORY=.false.
    if (.not. c_associated(root)) return
    allocate(found(size(expected_names)))
    found=.false.
    name=' '
    call LCMNXT(root,name)
    if (name == ' ') return
    first_name=name
    count_names=0
    do
      count_names=count_names+1
      if (count_names > size(expected_names)) return
      do index=1,size(expected_names)
        if (name == expected_names(index)) exit
      end do
      if (index > size(expected_names) .or. found(index)) return
      found(index)=.true.
      call LCMNXT(root,name)
      if (name == first_name) exit
    end do
    EXACT_INVENTORY=count_names == size(expected_names) .and. all(found)
  end function EXACT_INVENTORY


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    integer :: length, record_type

    call LCMLEL(list,index,length,record_type)
    if (length /= -1 .or. record_type /= 0) &
        error stop 'expected directory list item'
  end subroutine REQUIRE_DIRECTORY_ITEM


  subroutine REQUIRE_LIST_RECORD(list,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index, expected_length, expected_type
    integer :: length, record_type

    call LCMLEL(list,index,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        error stop 'list record schema differs'
  end subroutine REQUIRE_LIST_RECORD


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_CHARACTER12(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected

    call REQUIRE_CHARACTER_N(root,name,3,12,expected)
  end subroutine REQUIRE_CHARACTER12


  subroutine REQUIRE_CHARACTER_N(root,name,expected_words,character_count, &
      expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: expected_words, character_count
    character(len=72) :: found, padded

    if (character_count < 1 .or. character_count > len(found)) &
        error stop 'invalid character comparison length'
    call REQUIRE_RECORD(root,name,expected_words,3)
    found=' '
    padded=' '
    padded=expected
    call LCMGTC(root,name,character_count,found)
    if (found(1:character_count) /= padded(1:character_count)) &
        error stop 'character record differs'
  end subroutine REQUIRE_CHARACTER_N


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
        error stop 'forbidden record is present'
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A)') trim(owner)
      error stop 'required GANLIB pointer is absent'
    end if
  end subroutine REQUIRE_ASSOCIATED

end program CHECK_B2M_THREE_PLANE_COMMIT
