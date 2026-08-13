program CHECK_B2Z_REAL_RETURNED
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NSTATE=40, NGRP=370, NSNAP=3
  integer, parameter :: NREG=8, NUNKNO=14, NMAT=8, NIFIS=32
  integer(int32), parameter :: FROZEN_TOL_BITS=int(z'348637bd',int32)
  integer(int32), parameter :: REAL32_MAGNITUDE_MASK=int(z'7fffffff',int32)
  real(real64), parameter :: REAL32_MAX64=real(huge(0.0_real32),real64)
  integer, parameter :: TRACK_STATE_EXPECTED(NSTATE) = &
      [NREG,NUNKNO,1,NMAT,6,1,4,0,0,0,48,1,-1,4,1,2, &
       165,100000,11364,96,96,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  integer, parameter :: MACRO_STATE_EXPECTED(NSTATE) = &
      [NGRP,NMAT,3,NIFIS,18,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0, &
       0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  character(len=12), parameter :: PROJECTED_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
       'TRACK','MICROLIB2','FLUX','SPOT-R64']
  character(len=12), parameter :: RETURNED_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','TRACK', &
       'MICROLIB2','SYSTEM','FLUX','SPOT-R64']
  character(len=12), parameter :: ROOT_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
  character(len=12), parameter :: RETURN_AUTHORITY_NAMES(3) = &
      [character(len=12) :: 'NPLANE','STATE','EPOCH']
  character(len=12), parameter :: PROJECTED_PLANE_NAMES(12) = &
      [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
       'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
       'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D']
  character(len=12), parameter :: PROJECTED_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','FLUX','STATE','EPOCH']
  character(len=12), parameter :: RETURNED_CHILD_NAMES(16) = &
      [character(len=12) :: 'SPOT-R64','FLUX','SOUR','SIGNATURE', &
       'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
       'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D', &
       'SPOT-FS-EQN','SPOT-FS-K','SPOT-QFISS']
  character(len=12), parameter :: RETURNED_AUTHORITY_NAMES(6) = &
      [character(len=12) :: 'RHO','FLUX','SOUR','QFISS','STATE','EPOCH']
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

  character(len=1024) :: projected_path, returned_path
  integer :: ip, r64_flux_values, r64_sour_values, r64_qfiss_values
  integer :: r32_flux_values, r32_sour_values, r32_qfiss_values
  integer :: leakage_checks, tx_checks, sphys_checks, sused_checks
  integer :: response_values, response_nonzero(NSNAP), qfiss_formula_values
  integer(int64) :: copied_records, copied_words
  real(real64) :: rho64, keff64
  real(real64) :: phi64(NUNKNO,NGRP), expected_qfiss(NUNKNO,NGRP)
  real(real32) :: leakage32(NGRP), volume32(NREG)
  integer :: matcod(NREG), keyflx(NREG)
  type(c_ptr) :: projected, returned
  type(c_ptr) :: ptracks, plibraries, pfluxes
  type(c_ptr) :: rtracks, rlibraries, rsystems, rfluxes
  type(c_ptr) :: track, library, plane, system, child, macro

  if (command_argument_count() /= 2) &
      error stop 'expected PROJECTED and RETURNED XSM paths'
  call get_command_argument(1,projected_path)
  call get_command_argument(2,returned_path)
  if (len_trim(projected_path) == 0 .or. len_trim(returned_path) == 0) &
      error stop 'empty XSM path is forbidden'

  call LCMOP(projected,trim(projected_path),2,2,0)
  call LCMOP(returned,trim(returned_path),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'PROJECTED archive')
  call REQUIRE_ASSOCIATED(returned,'RETURNED archive')
  if (c_associated(projected,returned)) error stop 'archive handles alias'

  call VERIFY_ROOTS(projected,returned,rho64,keff64)
  ptracks=LCMGID(projected,'TRACK')
  plibraries=LCMGID(projected,'MICROLIB2')
  pfluxes=LCMGID(projected,'FLUX')
  rtracks=LCMGID(returned,'TRACK')
  rlibraries=LCMGID(returned,'MICROLIB2')
  rsystems=LCMGID(returned,'SYSTEM')
  rfluxes=LCMGID(returned,'FLUX')
  call REQUIRE_ASSOCIATED(ptracks,'PROJECTED TRACK list')
  call REQUIRE_ASSOCIATED(plibraries,'PROJECTED MICROLIB2 list')
  call REQUIRE_ASSOCIATED(pfluxes,'PROJECTED FLUX list')
  call REQUIRE_ASSOCIATED(rtracks,'RETURNED TRACK list')
  call REQUIRE_ASSOCIATED(rlibraries,'RETURNED MICROLIB2 list')
  call REQUIRE_ASSOCIATED(rsystems,'RETURNED SYSTEM list')
  call REQUIRE_ASSOCIATED(rfluxes,'RETURNED FLUX list')

  copied_records=0_int64
  copied_words=0_int64
  call COMPARE_LIST(ptracks,rtracks,NSNAP,copied_records,copied_words)
  call COMPARE_LIST(plibraries,rlibraries,NSNAP,copied_records,copied_words)

  r64_flux_values=0
  r64_sour_values=0
  r64_qfiss_values=0
  r32_flux_values=0
  r32_sour_values=0
  r32_qfiss_values=0
  leakage_checks=0
  tx_checks=0
  sphys_checks=0
  sused_checks=0
  response_values=0
  response_nonzero=0
  qfiss_formula_values=0
  do ip=1,NSNAP
    call REQUIRE_DIRECTORY_ITEM(ptracks,ip)
    call REQUIRE_DIRECTORY_ITEM(plibraries,ip)
    call REQUIRE_DIRECTORY_ITEM(pfluxes,ip)
    call REQUIRE_DIRECTORY_ITEM(rsystems,ip)
    call REQUIRE_DIRECTORY_ITEM(rfluxes,ip)
    track=LCMGIL(ptracks,ip)
    library=LCMGIL(plibraries,ip)
    plane=LCMGIL(pfluxes,ip)
    system=LCMGIL(rsystems,ip)
    child=LCMGIL(rfluxes,ip)
    call VERIFY_PROJECTED_CONTEXT(track,library,plane,rho64,matcod, &
        keyflx,volume32,leakage32,phi64,macro)
    call VERIFY_SYSTEM(system,library,ip,rho64,leakage32, &
        leakage_checks,tx_checks,sphys_checks,sused_checks, &
        response_values,response_nonzero(ip))
    call RECOMPUTE_QFISS(macro,rho64,matcod,keyflx,phi64,expected_qfiss)
    call VERIFY_RETURNED_CHILD(child,ip,rho64,keff64,keyflx,leakage32, &
        expected_qfiss,r64_flux_values,r64_sour_values,r64_qfiss_values, &
        r32_flux_values,r32_sour_values,r32_qfiss_values, &
        qfiss_formula_values)
  end do

  call LCMCL(returned,1)
  call LCMCL(projected,1)

  if (r64_flux_values /= NSNAP*NGRP*NUNKNO .or. &
      r64_sour_values /= NSNAP*NGRP*NUNKNO .or. &
      r64_qfiss_values /= NSNAP*NGRP*NUNKNO) &
      error stop 'REAL64 census differs'
  if (r32_flux_values /= r64_flux_values .or. &
      r32_sour_values /= r64_sour_values .or. &
      r32_qfiss_values /= r64_qfiss_values) &
      error stop 'REAL32 mirror census differs'
  if (qfiss_formula_values /= NSNAP*NGRP*NUNKNO) &
      error stop 'QFISS formula census differs'
  if (leakage_checks /= NSNAP*NGRP) error stop 'leakage census differs'
  if (tx_checks /= NSNAP*NGRP*(NMAT+1) .or. &
      sphys_checks /= tx_checks .or. sused_checks /= tx_checks) &
      error stop 'SYSTEM formula census differs'
  if (response_values /= NSNAP*NGRP*sum(RESPONSE_LENGTHS)) &
      error stop 'SYSTEM response census differs'
  if (any(response_nonzero <= 0)) error stop 'all-zero SYSTEM response plane'
  if (copied_records <= 0_int64 .or. copied_words <= 0_int64) &
      error stop 'copied subtree census is empty'

  write(*,'(A)') 'B2Z REAL RETURNED POSTERIOR PASS'
  write(*,'(A)') 'B2Z ROOT=PROJECTED/1->RETURNED/1 PLANES=3 INDEX-OWNED=YES'
  write(*,'(A,I0,A,I0)') 'B2Z COPIED-RECORDS=',copied_records, &
      ' COPIED-32BIT-WORDS=',copied_words
  write(*,'(A,I0,A,I0,A,I0)') 'B2Z R64-FLUX=',r64_flux_values, &
      ' R64-SOUR=',r64_sour_values,' R64-QFISS=',r64_qfiss_values
  write(*,'(A,I0,A,I0,A,I0)') 'B2Z R32-FLUX=',r32_flux_values, &
      ' R32-SOUR=',r32_sour_values,' R32-QFISS=',r32_qfiss_values
  write(*,'(A,I0,A,I0)') 'B2Z QFISS-FORMULA-BITS=',qfiss_formula_values, &
      ' LEAKAGE-BITS=',leakage_checks
  write(*,'(A,I0,A,I0,A,I0)') 'B2Z SYSTEM-TX=',tx_checks, &
      ' SYSTEM-S0PHYS=',sphys_checks,' SYSTEM-S0USED=',sused_checks
  write(*,'(A,I0,A,3(I0,1X))') 'B2Z RESPONSE-FINITE=',response_values, &
      ' NONZERO-BY-PLANE=',response_nonzero
  write(*,'(A)') 'B2Z EMPIRICAL-CONTROLS=0 OUTER-CONVERGENCE=NOT-EVALUATED'

contains

  subroutine VERIFY_ROOTS(input,output,rho,keff)
    type(c_ptr), intent(in) :: input, output
    real(real64), intent(out) :: rho, keff
    integer :: nplane, epoch
    real(real64) :: expected_rho
    type(c_ptr) :: authority

    call REQUIRE_EXACT(input,PROJECTED_ROOT_NAMES)
    call REQUIRE_CHARACTER12(input,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_INTEGER(input,'LISTDIM',NSNAP)
    call REQUIRE_RECORD(input,'SPOT-ITER-K',1,4)
    call LCMGET(input,'SPOT-ITER-K',keff)
    if (.not. ieee_is_finite(keff) .or. keff <= +0.0_real64 .or. &
        keff > REAL32_MAX64) error stop 'PROJECTED K is invalid'
    call REQUIRE_RECORD(input,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(input,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(input,'FLUX',NSNAP,10)
    call REQUIRE_RECORD(input,'SPOT-R64',-1,0)
    authority=LCMGID(input,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'PROJECTED root authority')
    call REQUIRE_EXACT(authority,ROOT_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER12(authority,'STATE','PROJECTED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',rho)
    expected_rho=1.0_real64/keff
    if (.not. ieee_is_finite(rho) .or. rho <= +0.0_real64 .or. &
        transfer(rho,0_int64) /= transfer(expected_rho,0_int64)) &
        error stop 'PROJECTED RHO/K authority differs'

    call REQUIRE_EXACT(output,RETURNED_ROOT_NAMES)
    call REQUIRE_CHARACTER12(output,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_INTEGER(output,'LISTDIM',NSNAP)
    call REQUIRE_RECORD(output,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(output,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(output,'SYSTEM',NSNAP,10)
    call REQUIRE_RECORD(output,'FLUX',NSNAP,10)
    call REQUIRE_RECORD(output,'SPOT-R64',-1,0)
    call REQUIRE_ABSENT(output,'RHO')
    call REQUIRE_ABSENT(output,'SPOT-ITER-K')
    call REQUIRE_ABSENT(output,'AX_NEXT')
    call REQUIRE_ABSENT(output,'AX-NEXT')
    call REQUIRE_ABSENT(output,'CLOSED')
    authority=LCMGID(output,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'RETURNED root authority')
    call REQUIRE_EXACT(authority,RETURN_AUTHORITY_NAMES)
    call REQUIRE_INTEGER(authority,'NPLANE',NSNAP)
    call REQUIRE_CHARACTER12(authority,'STATE','RETURNED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_ABSENT(authority,'RHO')
    call REQUIRE_ABSENT(authority,'SPOT-ITER-K')
    call LCMGET(authority,'NPLANE',nplane)
    call LCMGET(authority,'EPOCH',epoch)
    if (nplane /= NSNAP .or. epoch /= 1) error stop 'RETURNED lifecycle differs'
  end subroutine VERIFY_ROOTS


  subroutine VERIFY_PROJECTED_CONTEXT(track,library,plane,root_rho, &
      material,key,volume,leakage,flux,macro)
    type(c_ptr), intent(in) :: track, library, plane
    real(real64), intent(in) :: root_rho
    integer, intent(out) :: material(NREG), key(NREG)
    real(real32), intent(out) :: volume(NREG), leakage(NGRP)
    real(real64), intent(out) :: flux(NUNKNO,NGRP)
    type(c_ptr), intent(out) :: macro
    integer :: state(NSTATE), library_state(NSTATE), macro_state(NSTATE)
    integer :: expected_state(NSTATE), key2(NREG), imerge(NMAT), epoch
    integer :: ir, ig
    integer(int32) :: eps_bits(5)
    logical :: seen(NUNKNO)
    real(real32) :: eps(5), mirror(NUNKNO)
    real(real64) :: plane_rho
    type(c_ptr) :: authority, authority_flux, mirror_flux

    call REQUIRE_CHARACTER12(track,'SIGNATURE','L_TRACK')
    call REQUIRE_RECORD(track,'STATE-VECTOR',NSTATE,1)
    call LCMGET(track,'STATE-VECTOR',state)
    if (any(state /= TRACK_STATE_EXPECTED)) error stop 'TRACK state differs'
    call REQUIRE_RECORD(track,'MATCOD',NREG,1)
    call REQUIRE_RECORD(track,'VOLUME',NREG,2)
    call REQUIRE_RECORD(track,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
    call LCMGET(track,'MATCOD',material)
    call LCMGET(track,'VOLUME',volume)
    call LCMGET(track,'KEYFLX',key)
    call LCMGET(track,'KEYFLX$ANIS',key2)
    if (any(material < 1) .or. any(material > NMAT)) &
        error stop 'TRACK material map is invalid'
    if (.not. all(ieee_is_finite(volume)) .or. any(volume <= +0.0_real32)) &
        error stop 'TRACK volume is invalid'
    if (any(key /= key2)) error stop 'TRACK KEYFLX aliases differ'
    seen=.false.
    do ir=1,NREG
      if (key(ir) < 1 .or. key(ir) > NUNKNO .or. seen(key(ir))) &
          error stop 'TRACK KEYFLX map is invalid'
      seen(key(ir))=.true.
    end do

    call REQUIRE_CHARACTER12(library,'SIGNATURE','L_LIBRARY')
    call REQUIRE_RECORD(library,'STATE-VECTOR',NSTATE,1)
    call LCMGET(library,'STATE-VECTOR',library_state)
    if (library_state(1) /= NMAT .or. library_state(2) <= 0 .or. &
        library_state(3) /= NGRP .or. library_state(4) /= 3) &
        error stop 'MICROLIB2 state differs'
    call REQUIRE_RECORD(library,'MACROLIB',-1,0)
    macro=LCMGID(library,'MACROLIB')
    call REQUIRE_ASSOCIATED(macro,'same-index physical MACROLIB')
    call REQUIRE_CHARACTER12(macro,'SIGNATURE','L_MACROLIB')
    call REQUIRE_RECORD(macro,'STATE-VECTOR',NSTATE,1)
    call LCMGET(macro,'STATE-VECTOR',macro_state)
    if (any(macro_state /= MACRO_STATE_EXPECTED)) &
        error stop 'MACROLIB state differs'
    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)

    call REQUIRE_EXACT(plane,PROJECTED_PLANE_NAMES)
    call REQUIRE_CHARACTER12(plane,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(plane,'STATE-VECTOR',NSTATE,1)
    call LCMGET(plane,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:18)=[NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1]
    if (any(state /= expected_state)) error stop 'PROJECTED plane state differs'
    call REQUIRE_RECORD(plane,'EPS-CONVERGE',5,2)
    call LCMGET(plane,'EPS-CONVERGE',eps)
    if (.not. all(ieee_is_finite(eps))) error stop 'tolerance is nonfinite'
    eps_bits=transfer(eps,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS) .or. &
        any(eps_bits(4:5) /= 0_int32)) error stop 'frozen tolerance differs'
    call REQUIRE_RECORD(plane,'IMERGE-LEAK',NMAT,1)
    call LCMGET(plane,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) error stop 'IMERGE-LEAK differs'
    call REQUIRE_RECORD(plane,'KEYFLX',NREG,1)
    call LCMGET(plane,'KEYFLX',key2)
    if (any(key2 /= key)) error stop 'PROJECTED KEYFLX differs from TRACK'
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
    call REQUIRE_EXACT(authority,PROJECTED_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','PROJECTED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call LCMGET(authority,'RHO',plane_rho)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(plane_rho) .or. &
        transfer(plane_rho,0_int64) /= transfer(root_rho,0_int64) .or. &
        epoch /= 1) error stop 'PROJECTED plane authority differs'
    call REQUIRE_RECORD(plane,'FLUX',NGRP,10)
    authority_flux=LCMGID(authority,'FLUX')
    mirror_flux=LCMGID(plane,'FLUX')
    call REQUIRE_ASSOCIATED(authority_flux,'PROJECTED REAL64 FLUX')
    call REQUIRE_ASSOCIATED(mirror_flux,'PROJECTED REAL32 FLUX')
    do ig=1,NGRP
      call REQUIRE_LIST_RECORD(authority_flux,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(mirror_flux,ig,NUNKNO,2)
      call LCMGDL(authority_flux,ig,flux(:,ig))
      call LCMGDL(mirror_flux,ig,mirror)
      call VERIFY_REAL64_MIRROR(flux(:,ig),mirror,'PROJECTED FLUX')
      do ir=1,NREG
        if (flux(key(ir),ig) <= +0.0_real64) &
            error stop 'mapped PROJECTED flux is not positive'
      end do
    end do
  end subroutine VERIFY_PROJECTED_CONTEXT


  subroutine VERIFY_SYSTEM(system,library,plane,root_rho,leakage, &
      nleak,ntx,nsphys,nsused,nresponse,nnonzero)
    type(c_ptr), intent(in) :: system, library
    integer, intent(in) :: plane
    real(real64), intent(in) :: root_rho
    real(real32), intent(in) :: leakage(NGRP)
    integer, intent(inout) :: nleak, ntx, nsphys, nsused, nresponse, nnonzero
    integer :: state(NSTATE), expected_state(NSTATE), epoch, snapshot
    integer :: ig, im, i
    real(real64) :: system_rho
    real(real32) :: system_leakage(NGRP), ntot(NMAT), sigw(NMAT), tranc(NMAT)
    real(real32) :: tx(0:NMAT), sphys(0:NMAT), sused(0:NMAT)
    real(real32) :: expected_tx(0:NMAT), expected_sphys(0:NMAT)
    real(real32) :: expected_sused(0:NMAT)
    real(real32), allocatable :: response(:)
    type(c_ptr) :: authority, macro, groups, macro_groups, group, macro_group

    call REQUIRE_EXACT(system,SYSTEM_ROOT_NAMES)
    call REQUIRE_CHARACTER12(system,'SIGNATURE','L_PIJ')
    call REQUIRE_CHARACTER12(system,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(system,'LINK.TRACK','TRACK')
    call REQUIRE_RECORD(system,'STATE-VECTOR',NSTATE,1)
    call LCMGET(system,'STATE-VECTOR',state)
    expected_state=0
    expected_state([1,2,3,5,6,11])=1
    expected_state(7)=4
    expected_state(8)=NGRP
    expected_state(9)=NUNKNO
    expected_state(10)=NMAT
    if (any(state /= expected_state)) error stop 'SYSTEM state differs'
    call REQUIRE_INTEGER(system,'SPOT-L1-SNAP',plane)
    call LCMGET(system,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= plane) error stop 'SYSTEM plane/index differs'
    call REQUIRE_RECORD(system,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(system,'SPOT-LEAK1D',system_leakage)
    if (.not. all(ieee_is_finite(system_leakage)) .or. &
        any(transfer(system_leakage,0_int32,NGRP) /= &
        transfer(leakage,0_int32,NGRP))) &
        error stop 'SYSTEM same-index leakage differs'
    nleak=nleak+NGRP
    authority=LCMGID(system,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SYSTEM authority')
    call REQUIRE_EXACT(authority,SYSTEM_AUTHORITY_NAMES)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','ASSEMBLED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',system_rho)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(system_rho) .or. &
        transfer(system_rho,0_int64) /= transfer(root_rho,0_int64) .or. &
        epoch /= 1) error stop 'SYSTEM authority differs'

    macro=LCMGID(library,'MACROLIB')
    call REQUIRE_ASSOCIATED(macro,'SYSTEM same-index MACROLIB')
    call REQUIRE_RECORD(system,'GROUP',NGRP,10)
    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
    groups=LCMGID(system,'GROUP')
    macro_groups=LCMGID(macro,'GROUP')
    call REQUIRE_ASSOCIATED(groups,'SYSTEM GROUP list')
    call REQUIRE_ASSOCIATED(macro_groups,'MACROLIB GROUP list')
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(groups,ig)
      call REQUIRE_DIRECTORY_ITEM(macro_groups,ig)
      group=LCMGIL(groups,ig)
      macro_group=LCMGIL(macro_groups,ig)
      call REQUIRE_EXACT(group,GROUP_NAMES)
      call REQUIRE_ABSENT(group,'FUNKNO$USS')
      call REQUIRE_RECORD(macro_group,'NTOT0',NMAT,2)
      call REQUIRE_RECORD(macro_group,'SIGW00',NMAT,2)
      call REQUIRE_RECORD(macro_group,'TRANC',NMAT,2)
      call LCMGET(macro_group,'NTOT0',ntot)
      call LCMGET(macro_group,'SIGW00',sigw)
      call LCMGET(macro_group,'TRANC',tranc)
      if (.not. all(ieee_is_finite(ntot)) .or. &
          .not. all(ieee_is_finite(sigw)) .or. &
          .not. all(ieee_is_finite(tranc))) error stop 'SYSTEM inputs nonfinite'
      call REQUIRE_RECORD(group,'DRAGON-TXSC',NMAT+1,2)
      call REQUIRE_RECORD(group,'SPOT-S0-PHYS',NMAT+1,2)
      call REQUIRE_RECORD(group,'DRAGON-S0XSC',NMAT+1,2)
      call LCMGET(group,'DRAGON-TXSC',tx)
      call LCMGET(group,'SPOT-S0-PHYS',sphys)
      call LCMGET(group,'DRAGON-S0XSC',sused)
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
          error stop 'SYSTEM ordered formula is nonfinite'
      if (any(transfer(tx,0_int32,NMAT+1) /= &
          transfer(expected_tx,0_int32,NMAT+1))) &
          error stop 'SYSTEM TX formula differs'
      if (any(transfer(sphys,0_int32,NMAT+1) /= &
          transfer(expected_sphys,0_int32,NMAT+1))) &
          error stop 'SYSTEM S0 physical formula differs'
      if (any(transfer(sused,0_int32,NMAT+1) /= &
          transfer(expected_sused,0_int32,NMAT+1))) &
          error stop 'SYSTEM S0 used formula differs'
      ntx=ntx+NMAT+1
      nsphys=nsphys+NMAT+1
      nsused=nsused+NMAT+1
      do i=1,size(RESPONSE_NAMES)
        call REQUIRE_RECORD(group,RESPONSE_NAMES(i),RESPONSE_LENGTHS(i),2)
        allocate(response(RESPONSE_LENGTHS(i)))
        call LCMGET(group,RESPONSE_NAMES(i),response)
        if (.not. all(ieee_is_finite(response))) &
            error stop 'SYSTEM response is nonfinite'
        nresponse=nresponse+size(response)
        nnonzero=nnonzero+count(iand(transfer(response,0_int32,size(response)), &
            REAL32_MAGNITUDE_MASK) /= 0_int32)
        deallocate(response)
      end do
    end do
  end subroutine VERIFY_SYSTEM


  subroutine RECOMPUTE_QFISS(macro,rho,material,key,flux,qfiss)
    type(c_ptr), intent(in) :: macro
    real(real64), intent(in) :: rho
    integer, intent(in) :: material(NREG), key(NREG)
    real(real64), intent(in) :: flux(NUNKNO,NGRP)
    real(real64), intent(out) :: qfiss(NUNKNO,NGRP)
    integer :: ir, ifis, h, g, im, iu
    real(real32) :: group_chi(NMAT,NIFIS), group_nusigf(NMAT,NIFIS)
    real(real32), allocatable :: chi32(:,:,:), nusigf32(:,:,:)
    real(real64) :: product, fission_rate, contribution
    type(c_ptr) :: groups, group

    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
    groups=LCMGID(macro,'GROUP')
    call REQUIRE_ASSOCIATED(groups,'QFISS physical MACROLIB groups')
    allocate(chi32(NMAT,NIFIS,NGRP),nusigf32(NMAT,NIFIS,NGRP))
    do g=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(groups,g)
      group=LCMGIL(groups,g)
      call REQUIRE_RECORD(group,'CHI',NMAT*NIFIS,2)
      call REQUIRE_RECORD(group,'NUSIGF',NMAT*NIFIS,2)
      call LCMGET(group,'CHI',group_chi)
      call LCMGET(group,'NUSIGF',group_nusigf)
      if (.not. all(ieee_is_finite(group_chi)) .or. &
          .not. all(ieee_is_finite(group_nusigf)) .or. &
          any(group_chi < +0.0_real32) .or. &
          any(group_nusigf < +0.0_real32)) error stop 'fission data invalid'
      chi32(:,:,g)=group_chi
      nusigf32(:,:,g)=group_nusigf
    end do

    ! Independent B2N oracle.  The scalar assignments and the frozen loop
    ! order ir -> ifis -> h -> g are part of the numerical definition.
    qfiss=+0.0_real64
    do ir=1,NREG
      im=material(ir)
      iu=key(ir)
      do ifis=1,NIFIS
        fission_rate=+0.0_real64
        do h=1,NGRP
          product=real(nusigf32(im,ifis,h),real64)*flux(iu,h)
          if (.not. ieee_is_finite(product) .or. product < +0.0_real64) &
              error stop 'QFISS fission product is invalid'
          fission_rate=fission_rate+product
          if (.not. ieee_is_finite(fission_rate) .or. &
              fission_rate < +0.0_real64) &
              error stop 'QFISS fission rate is invalid'
        end do
        do g=1,NGRP
          contribution=real(chi32(im,ifis,g),real64)*fission_rate
          if (.not. ieee_is_finite(contribution) .or. &
              contribution < +0.0_real64) &
              error stop 'QFISS CHI contribution is invalid'
          contribution=contribution*rho
          if (.not. ieee_is_finite(contribution) .or. &
              contribution < +0.0_real64) &
              error stop 'QFISS RHO contribution is invalid'
          qfiss(iu,g)=qfiss(iu,g)+contribution
          if (.not. ieee_is_finite(qfiss(iu,g)) .or. &
              qfiss(iu,g) < +0.0_real64) &
              error stop 'QFISS accumulation is invalid'
        end do
      end do
    end do
  end subroutine RECOMPUTE_QFISS


  subroutine VERIFY_RETURNED_CHILD(child,plane,rho,keff,expected_key, &
      expected_leakage,expected_qfiss,nrf,nrs,nrq,nmf,nms,nmq,nformula)
    type(c_ptr), intent(in) :: child
    integer, intent(in) :: plane
    real(real64), intent(in) :: rho, keff
    integer, intent(in) :: expected_key(NREG)
    real(real32), intent(in) :: expected_leakage(NGRP)
    real(real64), intent(in) :: expected_qfiss(NUNKNO,NGRP)
    integer, intent(inout) :: nrf, nrs, nrq, nmf, nms, nmq, nformula
    integer :: state(NSTATE), expected_state(NSTATE), key(NREG), imerge(NMAT)
    integer :: ig, epoch, marker
    integer(int32) :: eps_bits(5)
    real(real32) :: eps(5), leakage(NGRP), k32, expected_k32
    real(real32) :: mirror_flux(NUNKNO), mirror_sour(NUNKNO)
    real(real32) :: mirror_qfiss(NUNKNO)
    real(real64) :: found_rho, auth_flux(NUNKNO), auth_sour(NUNKNO)
    real(real64) :: auth_qfiss(NUNKNO)
    type(c_ptr) :: authority, aflux, asour, aqfiss, mflux, msour
    type(c_ptr) :: qouter, qinner

    if (plane < 1 .or. plane > NSNAP) error stop 'SOLVED list index is invalid'
    call REQUIRE_EXACT(child,RETURNED_CHILD_NAMES)
    call REQUIRE_CHARACTER12(child,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(child,'STATE-VECTOR',NSTATE,1)
    call LCMGET(child,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:18)=[NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1]
    if (any(state /= expected_state)) error stop 'SOLVED state differs'
    call REQUIRE_RECORD(child,'EPS-CONVERGE',5,2)
    call LCMGET(child,'EPS-CONVERGE',eps)
    if (.not. all(ieee_is_finite(eps))) error stop 'SOLVED tolerance nonfinite'
    eps_bits=transfer(eps,0_int32,5)
    if (any(eps_bits(1:3) /= FROZEN_TOL_BITS) .or. &
        any(eps_bits(4:5) /= 0_int32)) error stop 'SOLVED tolerance differs'
    call REQUIRE_RECORD(child,'IMERGE-LEAK',NMAT,1)
    call LCMGET(child,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) error stop 'SOLVED IMERGE-LEAK differs'
    call REQUIRE_RECORD(child,'KEYFLX',NREG,1)
    call LCMGET(child,'KEYFLX',key)
    if (any(key /= expected_key)) error stop 'SOLVED plane/index KEYFLX differs'
    call REQUIRE_CHARACTER_N(child,'OPTION',1,4,'B0  ')
    call REQUIRE_CHARACTER12(child,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(child,'LINK.TRACK','TRACK')
    call REQUIRE_CHARACTER12(child,'LINK.SYSTEM','SYSTEM')
    call REQUIRE_RECORD(child,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(child,'SPOT-LEAK1D',leakage)
    if (.not. all(ieee_is_finite(leakage)) .or. &
        any(transfer(leakage,0_int32,NGRP) /= &
        transfer(expected_leakage,0_int32,NGRP))) &
        error stop 'SOLVED plane/index leakage differs'

    authority=LCMGID(child,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SOLVED REAL64 authority')
    call REQUIRE_EXACT(authority,RETURNED_AUTHORITY_NAMES)
    call REQUIRE_ABSENT(authority,'PLANE')
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(authority,'STATE','SOLVED')
    call REQUIRE_INTEGER(authority,'EPOCH',1)
    call LCMGET(authority,'RHO',found_rho)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(found_rho) .or. &
        transfer(found_rho,0_int64) /= transfer(rho,0_int64) .or. &
        epoch /= 1) error stop 'SOLVED authority differs'
    call REQUIRE_INTEGER(child,'SPOT-FS-EQN',1)
    call LCMGET(child,'SPOT-FS-EQN',marker)
    if (marker /= 1) error stop 'SOLVED fission-source marker differs'
    call REQUIRE_RECORD(child,'SPOT-FS-K',1,2)
    call LCMGET(child,'SPOT-FS-K',k32)
    expected_k32=real(keff,real32)
    if (.not. ieee_is_finite(k32) .or. &
        transfer(k32,0_int32) /= transfer(expected_k32,0_int32)) &
        error stop 'SOLVED K mirror differs'

    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(authority,'SOUR',NGRP,10)
    call REQUIRE_RECORD(authority,'QFISS',NGRP,10)
    call REQUIRE_RECORD(child,'FLUX',NGRP,10)
    call REQUIRE_RECORD(child,'SOUR',NGRP,10)
    call REQUIRE_RECORD(child,'SPOT-QFISS',1,10)
    aflux=LCMGID(authority,'FLUX')
    asour=LCMGID(authority,'SOUR')
    aqfiss=LCMGID(authority,'QFISS')
    mflux=LCMGID(child,'FLUX')
    msour=LCMGID(child,'SOUR')
    qouter=LCMGID(child,'SPOT-QFISS')
    call REQUIRE_ASSOCIATED(aflux,'SOLVED authority FLUX')
    call REQUIRE_ASSOCIATED(asour,'SOLVED authority SOUR')
    call REQUIRE_ASSOCIATED(aqfiss,'SOLVED authority QFISS')
    call REQUIRE_ASSOCIATED(mflux,'SOLVED mirror FLUX')
    call REQUIRE_ASSOCIATED(msour,'SOLVED mirror SOUR')
    call REQUIRE_ASSOCIATED(qouter,'SOLVED mirror QFISS outer')
    call REQUIRE_LIST_RECORD(qouter,1,NGRP,10)
    qinner=LCMGIL(qouter,1)
    call REQUIRE_ASSOCIATED(qinner,'SOLVED mirror QFISS inner')
    do ig=1,NGRP
      call REQUIRE_LIST_RECORD(aflux,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(asour,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(aqfiss,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(mflux,ig,NUNKNO,2)
      call REQUIRE_LIST_RECORD(msour,ig,NUNKNO,2)
      call REQUIRE_LIST_RECORD(qinner,ig,NUNKNO,2)
      call LCMGDL(aflux,ig,auth_flux)
      call LCMGDL(asour,ig,auth_sour)
      call LCMGDL(aqfiss,ig,auth_qfiss)
      call LCMGDL(mflux,ig,mirror_flux)
      call LCMGDL(msour,ig,mirror_sour)
      call LCMGDL(qinner,ig,mirror_qfiss)
      call VERIFY_REAL64_MIRROR(auth_flux,mirror_flux,'SOLVED FLUX')
      call VERIFY_REAL64_MIRROR(auth_sour,mirror_sour,'SOLVED SOUR')
      call VERIFY_REAL64_MIRROR(auth_qfiss,mirror_qfiss,'SOLVED QFISS')
      if (any(auth_qfiss < +0.0_real64)) &
          error stop 'SOLVED QFISS is negative'
      if (any(transfer(auth_qfiss,0_int64,NUNKNO) /= &
          transfer(expected_qfiss(:,ig),0_int64,NUNKNO))) &
          error stop 'SOLVED QFISS does not match frozen B2N formula'
      nrf=nrf+NUNKNO
      nrs=nrs+NUNKNO
      nrq=nrq+NUNKNO
      nmf=nmf+NUNKNO
      nms=nms+NUNKNO
      nmq=nmq+NUNKNO
      nformula=nformula+NUNKNO
    end do
  end subroutine VERIFY_RETURNED_CHILD


  subroutine VERIFY_REAL64_MIRROR(authority,mirror,label)
    real(real64), intent(in) :: authority(:)
    real(real32), intent(in) :: mirror(:)
    character(len=*), intent(in) :: label
    if (size(authority) /= size(mirror)) error stop 'mirror size differs'
    if (.not. all(ieee_is_finite(authority)) .or. &
        .not. all(ieee_is_finite(mirror))) then
      write(*,'(A)') trim(label)//' contains a nonfinite value'
      error stop 'REAL64/mirror finiteness failure'
    end if
    if (any(abs(authority) > REAL32_MAX64)) then
      write(*,'(A)') trim(label)//' exceeds REAL32 range'
      error stop 'REAL64/mirror range failure'
    end if
    if (any(transfer(mirror,0_int32,size(mirror)) /= &
        transfer(real(authority,real32),0_int32,size(mirror)))) then
      write(*,'(A)') trim(label)//' mirror bits differ'
      error stop 'REAL64/mirror projection failure'
    end if
  end subroutine VERIFY_REAL64_MIRROR


  recursive subroutine COMPARE_DICTIONARY(left,right,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer(int64), intent(inout) :: record_count, word_count
    character(len=12) :: first_name, name
    integer :: left_count, right_count, left_length, right_length
    integer :: left_type, right_type
    type(c_ptr) :: left_child, right_child

    call COUNT_DICTIONARY_NAMES(left,left_count)
    call COUNT_DICTIONARY_NAMES(right,right_count)
    if (left_count /= right_count) error stop 'copied directory count differs'
    if (left_count == 0) return
    name=' '
    call LCMNXT(left,name)
    first_name=name
    do
      call LCMLEN(left,name,left_length,left_type)
      call LCMLEN(right,name,right_length,right_type)
      if (left_length /= right_length .or. left_type /= right_type) &
          error stop 'copied named schema differs'
      select case(left_type)
      case(0)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied dictionary')
        call REQUIRE_ASSOCIATED(right_child,'right copied dictionary')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
        call REQUIRE_ASSOCIATED(left_child,'left copied list')
        call REQUIRE_ASSOCIATED(right_child,'right copied list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count,word_count)
      case default
        call COMPARE_NAMED_PAYLOAD(left,right,name,left_length,left_type, &
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
          error stop 'copied list schema differs'
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
        call REQUIRE_ASSOCIATED(left_child,'left nested list')
        call REQUIRE_ASSOCIATED(right_child,'right nested list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count,word_count)
      case default
        call COMPARE_LIST_PAYLOAD(left,right,index,left_length,left_type, &
            record_count,word_count)
      end select
    end do
  end subroutine COMPARE_LIST


  subroutine COMPARE_NAMED_PAYLOAD(left,right,name,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: length, record_type
    integer(int64), intent(inout) :: record_count, word_count
    integer, allocatable :: il(:), ir(:)
    real(real32), allocatable :: rl(:), rr(:)
    real(real64), allocatable :: dl(:), dr(:)
    logical, allocatable :: ll(:), lr(:)
    complex(real32), allocatable :: cl(:), cr(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(il(length),ir(length)); call LCMGET(left,name,il); call LCMGET(right,name,ir)
      if (any(il /= ir)) error stop 'copied integer/character bits differ'
      word_count=word_count+length
    case(2)
      allocate(rl(length),rr(length)); call LCMGET(left,name,rl); call LCMGET(right,name,rr)
      if (any(transfer(rl,0_int32,length) /= transfer(rr,0_int32,length))) &
          error stop 'copied REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(dl(length),dr(length)); call LCMGET(left,name,dl); call LCMGET(right,name,dr)
      if (any(transfer(dl,0_int64,length) /= transfer(dr,0_int64,length))) &
          error stop 'copied REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(ll(length),lr(length)); call LCMGET(left,name,ll); call LCMGET(right,name,lr)
      if (any(transfer(ll,0_int32,length) /= transfer(lr,0_int32,length))) &
          error stop 'copied logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(cl(length),cr(length)); call LCMGET(left,name,cl); call LCMGET(right,name,cr)
      if (any(transfer(cl,0_int32,2*length) /= transfer(cr,0_int32,2*length))) &
          error stop 'copied complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported copied GANLIB record type'
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_NAMED_PAYLOAD


  subroutine COMPARE_LIST_PAYLOAD(left,right,index,length,record_type, &
      record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(in) :: index, length, record_type
    integer(int64), intent(inout) :: record_count, word_count
    integer, allocatable :: il(:), ir(:)
    real(real32), allocatable :: rl(:), rr(:)
    real(real64), allocatable :: dl(:), dr(:)
    logical, allocatable :: ll(:), lr(:)
    complex(real32), allocatable :: cl(:), cr(:)

    if (length == 0) then
      record_count=record_count+1_int64
      return
    end if
    select case(record_type)
    case(1,3)
      allocate(il(length),ir(length)); call LCMGDL(left,index,il); call LCMGDL(right,index,ir)
      if (any(il /= ir)) error stop 'copied list integer/character bits differ'
      word_count=word_count+length
    case(2)
      allocate(rl(length),rr(length)); call LCMGDL(left,index,rl); call LCMGDL(right,index,rr)
      if (any(transfer(rl,0_int32,length) /= transfer(rr,0_int32,length))) &
          error stop 'copied list REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(dl(length),dr(length)); call LCMGDL(left,index,dl); call LCMGDL(right,index,dr)
      if (any(transfer(dl,0_int64,length) /= transfer(dr,0_int64,length))) &
          error stop 'copied list REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(ll(length),lr(length)); call LCMGDL(left,index,ll); call LCMGDL(right,index,lr)
      if (any(transfer(ll,0_int32,length) /= transfer(lr,0_int32,length))) &
          error stop 'copied list logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(cl(length),cr(length)); call LCMGDL(left,index,cl); call LCMGDL(right,index,cr)
      if (any(transfer(cl,0_int32,2*length) /= transfer(cr,0_int32,2*length))) &
          error stop 'copied list complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported copied GANLIB list record type'
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_LIST_PAYLOAD


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


  subroutine REQUIRE_EXACT(root,expected_names)
    type(c_ptr), intent(in) :: root
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, name
    logical :: found(size(expected_names))
    integer :: count_names, index

    call REQUIRE_ASSOCIATED(root,'exact-inventory owner')
    found=.false.
    name=' '
    call LCMNXT(root,name)
    if (name == ' ') error stop 'exact inventory is empty'
    first_name=name
    count_names=0
    do
      count_names=count_names+1
      if (count_names > size(expected_names)) error stop 'exact inventory has extras'
      do index=1,size(expected_names)
        if (name == expected_names(index)) exit
      end do
      if (index > size(expected_names) .or. found(index)) &
          error stop 'exact inventory contains unknown/duplicate entry'
      found(index)=.true.
      call LCMNXT(root,name)
      if (name == first_name) exit
    end do
    if (count_names /= size(expected_names) .or. .not. all(found)) &
        error stop 'exact inventory is incomplete'
  end subroutine REQUIRE_EXACT


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    call REQUIRE_LIST_RECORD(list,index,-1,0)
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
        error stop 'named record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_INTEGER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found
    call REQUIRE_RECORD(root,name,1,1)
    call LCMGET(root,name,found)
    if (found /= expected) error stop 'integer record value differs'
  end subroutine REQUIRE_INTEGER


  subroutine REQUIRE_CHARACTER12(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    call REQUIRE_CHARACTER_N(root,name,3,12,expected)
  end subroutine REQUIRE_CHARACTER12


  subroutine REQUIRE_CHARACTER_N(root,name,expected_words,count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: expected_words, count
    character(len=72) :: found, padded
    call REQUIRE_RECORD(root,name,expected_words,3)
    found=' '
    padded=' '
    padded=expected
    call LCMGTC(root,name,count,found)
    if (found(1:count) /= padded(1:count)) &
        error stop 'character record value differs'
  end subroutine REQUIRE_CHARACTER_N


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type
    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
        error stop 'forbidden record is present'
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_ASSOCIATED(pointer,label)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: label
    if (.not. c_associated(pointer)) then
      write(*,'(A)') trim(label)//' is absent'
      error stop 'required GANLIB pointer missing'
    end if
  end subroutine REQUIRE_ASSOCIATED

end program CHECK_B2Z_REAL_RETURNED

