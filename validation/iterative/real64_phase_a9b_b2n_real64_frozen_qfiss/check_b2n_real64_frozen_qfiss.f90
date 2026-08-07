program CHECK_B2N_REAL64_FROZEN_QFISS
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
  integer, parameter :: NIFIS=32
  integer(int32), parameter :: FROZEN_TOL_BITS=int(z'348637bd',int32)
  real(real64), parameter :: REAL32_MAX64= &
      real(huge(0.0_real32),real64)
  character(len=12), parameter :: PROJECTED_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
       'TRACK','MICROLIB2','FLUX','SPOT-R64']
  character(len=12), parameter :: ROOT_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
  character(len=12), parameter :: PLANE_ROOT_NAMES(12) = &
      [character(len=12) :: 'SPOT-R64','FLUX','SIGNATURE', &
       'STATE-VECTOR','EPS-CONVERGE','IMERGE-LEAK','KEYFLX','OPTION', &
       'LINK.MACRO','LINK.TRACK','LINK.SYSTEM','SPOT-LEAK1D']
  character(len=12), parameter :: PLANE_AUTHORITY_NAMES(4) = &
      [character(len=12) :: 'RHO','FLUX','STATE','EPOCH']
  character(len=12), parameter :: SOURCE_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','STATE-VECTOR','SPOT-FROZEN', &
       'SPOT-KEFF','SPOT-QINT','DSOUR','SPOT-R64']
  character(len=12), parameter :: SOURCE_AUTHORITY_NAMES(5) = &
      [character(len=12) :: 'RHO','PLANE','STATE','QFISS','EPOCH']

  character(len=1024) :: projected_path, macro_path, source_path
  integer :: mat(NREG), keyflx(NREG), epoch
  integer :: phi_positive, qfiss_checks, dsour_checks, qint_checks
  integer :: nusigf_zero_checks, nonregion_zero_checks
  integer(int64) :: unchanged_records, unchanged_words
  real(real32) :: volume32(NREG)
  real(real64) :: rho64, keff64
  real(real64) :: phi64(NUNKNO,NGRP), qfiss64(NUNKNO,NGRP)
  real(real64) :: qint64(NGRP)
  type(c_ptr) :: projected, macro_output, source_output, input_macro

  if (command_argument_count() /= 3) error stop &
      'expected PROJECTED, MACRO_OUT, and SOURCE_OUT paths'
  call get_command_argument(1,projected_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,source_path)
  if (len_trim(projected_path) == 0 .or. len_trim(macro_path) == 0 .or. &
      len_trim(source_path) == 0) error stop 'empty path is forbidden'

  call LCMOP(projected,trim(projected_path),2,2,0)
  call LCMOP(macro_output,trim(macro_path),2,2,0)
  call LCMOP(source_output,trim(source_path),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'persistent PROJECTED input')
  call REQUIRE_ASSOCIATED(macro_output,'persistent MACRO output')
  call REQUIRE_ASSOCIATED(source_output,'persistent SOURCE output')
  if (c_associated(projected,macro_output) .or. &
      c_associated(projected,source_output) .or. &
      c_associated(macro_output,source_output)) &
      error stop 'posterior object handles alias'

  call VERIFY_PROJECTED_PLANE1(projected,input_macro,rho64,keff64,epoch, &
      mat,keyflx,volume32,phi64,phi_positive)
  call VERIFY_MACRO_OUTPUT(input_macro,macro_output,keff64, &
      nusigf_zero_checks,unchanged_records,unchanged_words)
  call RECOMPUTE_QFISS(input_macro,rho64,mat,keyflx,volume32,phi64, &
      qfiss64,qint64,nonregion_zero_checks)
  call VERIFY_SOURCE_OUTPUT(source_output,rho64,keff64,epoch,qfiss64, &
      qint64,qfiss_checks,dsour_checks,qint_checks)

  call LCMCL(source_output,1)
  call LCMCL(macro_output,1)
  call LCMCL(projected,1)

  if (phi_positive /= NREG*NGRP) &
      error stop 'positive region-flux inventory differs'
  if (qfiss_checks /= NUNKNO*NGRP) &
      error stop 'REAL64 QFISS bit inventory differs'
  if (dsour_checks /= NUNKNO*NGRP) &
      error stop 'REAL32 DSOUR bit inventory differs'
  if (qint_checks /= NGRP) &
      error stop 'REAL32 QINT bit inventory differs'
  if (nusigf_zero_checks /= NGRP*NMAT*NIFIS) &
      error stop 'positive-zero NUSIGF inventory differs'
  if (nonregion_zero_checks /= (NUNKNO-NREG)*NGRP) &
      error stop 'non-region positive-zero QFISS inventory differs'
  if (unchanged_records <= 0_int64 .or. unchanged_words <= 0_int64) &
      error stop 'recursive unchanged-macrolib inventory is empty'

  write(*,'(A)') 'B2N REAL64 FROZEN-QFISS POSTERIOR PASS'
  write(*,'(A)') &
      'B2N QFISS-R64-BITS=5180 DSOUR-R32-PROJECTIONS=5180 QINT-R32-PROJECTIONS=370'
  write(*,'(A)') &
      'B2N POSITIVE-REGION-FLUX=2960 NONREGION-POSITIVE-ZERO-QFISS=2220'
  write(*,'(A)') &
      'B2N NUSIGF-POSITIVE-ZERO=94720 MACRO-OTHER-RECORDS=BIT-IDENTICAL'
  write(*,'(A)') &
      'B2N STATE=FROZEN-QFIS/1 PLANE=1 SAME-RHO=BIT-IDENTICAL'
  write(*,'(A)') 'B2N FIRST-GROUP-INTEGRAL=POSITIVE'
  write(*,'(A)') &
      'B2N DRAGON=0 ASM=0 FLU=0 CONVERGENCE=NOT-EVALUATED'
  write(*,'(A)') 'B2N EMPIRICAL-CONTROLS=0 CONT=0'

contains

  subroutine VERIFY_PROJECTED_PLANE1(root,macro,rho,keff,plane_epoch, &
      material,key,volume,flux,positive_count)
    type(c_ptr), intent(in) :: root
    type(c_ptr), intent(out) :: macro
    real(real64), intent(out) :: rho, keff
    integer, intent(out) :: plane_epoch
    integer, intent(out) :: material(NREG), key(NREG)
    real(real32), intent(out) :: volume(NREG)
    real(real64), intent(out) :: flux(NUNKNO,NGRP)
    integer, intent(out) :: positive_count

    integer :: ip, ig, ir, listdim, nplane, root_epoch
    integer :: state(NSTATE), expected_state(NSTATE), track_state(NSTATE)
    integer :: library_state(NSTATE), macro_state(NSTATE)
    integer :: plane_key(NREG), imerge(NMAT)
    integer(int32) :: eps_bits(5)
    logical :: seen(NUNKNO)
    real(real32) :: eps(5), leakage(NGRP), mirror(NUNKNO)
    real(real64) :: root_rho, plane_rho
    type(c_ptr) :: root_authority, tracks, libraries, planes
    type(c_ptr) :: track, library, plane, plane_authority
    type(c_ptr) :: authority_flux, mirror_flux, macro_groups

    if (.not. EXACT_INVENTORY(root,PROJECTED_ROOT_NAMES)) &
        error stop 'PROJECTED root inventory differs'
    call REQUIRE_CHARACTER12(root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_RECORD(root,'LISTDIM',1,1)
    call REQUIRE_RECORD(root,'SPOT-ITER-K',1,4)
    call REQUIRE_RECORD(root,'TRACK',NSNAP,10)
    call REQUIRE_RECORD(root,'MICROLIB2',NSNAP,10)
    call REQUIRE_RECORD(root,'FLUX',NSNAP,10)
    call REQUIRE_RECORD(root,'SPOT-R64',-1,0)
    call LCMGET(root,'LISTDIM',listdim)
    call LCMGET(root,'SPOT-ITER-K',keff)
    if (listdim /= NSNAP) error stop 'PROJECTED plane count differs'
    if (.not. ieee_is_finite(keff) .or. keff <= +0.0_real64) &
        error stop 'PROJECTED eigenvalue is invalid'

    root_authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(root_authority,'PROJECTED root authority')
    if (.not. EXACT_INVENTORY(root_authority,ROOT_AUTHORITY_NAMES)) &
        error stop 'PROJECTED root authority inventory differs'
    call REQUIRE_RECORD(root_authority,'RHO',1,4)
    call REQUIRE_RECORD(root_authority,'NPLANE',1,1)
    call REQUIRE_CHARACTER12(root_authority,'STATE','PROJECTED')
    call REQUIRE_RECORD(root_authority,'EPOCH',1,1)
    call LCMGET(root_authority,'RHO',root_rho)
    call LCMGET(root_authority,'NPLANE',nplane)
    call LCMGET(root_authority,'EPOCH',root_epoch)
    if (.not. ieee_is_finite(root_rho) .or. root_rho <= +0.0_real64) &
        error stop 'PROJECTED root RHO is invalid'
    if (transfer(root_rho,0_int64) /= &
        transfer(1.0_real64/keff,0_int64)) &
        error stop 'PROJECTED RHO is not the bitwise reciprocal of K'
    if (nplane /= NSNAP .or. root_epoch /= 1) &
        error stop 'PROJECTED root lifecycle differs'

    tracks=LCMGID(root,'TRACK')
    libraries=LCMGID(root,'MICROLIB2')
    planes=LCMGID(root,'FLUX')
    call REQUIRE_ASSOCIATED(tracks,'PROJECTED TRACK list')
    call REQUIRE_ASSOCIATED(libraries,'PROJECTED MICROLIB2 list')
    call REQUIRE_ASSOCIATED(planes,'PROJECTED FLUX list')
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(tracks,ip)
      call REQUIRE_DIRECTORY_ITEM(libraries,ip)
      call REQUIRE_DIRECTORY_ITEM(planes,ip)
    end do

    track=LCMGIL(tracks,1)
    library=LCMGIL(libraries,1)
    plane=LCMGIL(planes,1)
    call REQUIRE_CHARACTER12(track,'SIGNATURE','L_TRACK')
    call REQUIRE_RECORD(track,'STATE-VECTOR',NSTATE,1)
    call LCMGET(track,'STATE-VECTOR',track_state)
    if (track_state(1) /= NREG .or. track_state(2) /= NUNKNO .or. &
        track_state(4) /= NMAT .or. track_state(5) /= 6 .or. &
        track_state(6) /= 1 .or. track_state(9) /= 0 .or. &
        track_state(14) /= 4) error stop 'plane-1 TRACK state differs'
    call REQUIRE_RECORD(track,'MATCOD',NREG,1)
    call REQUIRE_RECORD(track,'VOLUME',NREG,2)
    call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
    call LCMGET(track,'MATCOD',material)
    call LCMGET(track,'VOLUME',volume)
    call LCMGET(track,'KEYFLX$ANIS',key)
    if (any(material < 1) .or. any(material > NMAT)) &
        error stop 'plane-1 material map is invalid'
    if (.not. all(ieee_is_finite(volume)) .or. &
        any(volume <= +0.0_real32)) &
        error stop 'plane-1 region volume is invalid'
    seen=.false.
    do ir=1,NREG
      if (key(ir) < 1 .or. key(ir) > NUNKNO) &
          error stop 'plane-1 region key is out of range'
      if (seen(key(ir))) error stop 'plane-1 region key is repeated'
      seen(key(ir))=.true.
    end do

    call REQUIRE_CHARACTER12(library,'SIGNATURE','L_LIBRARY')
    call REQUIRE_RECORD(library,'STATE-VECTOR',NSTATE,1)
    call LCMGET(library,'STATE-VECTOR',library_state)
    if (library_state(1) /= NMAT .or. library_state(2) <= 0 .or. &
        library_state(3) /= NGRP .or. library_state(4) /= 3) &
        error stop 'plane-1 library state differs'
    call REQUIRE_RECORD(library,'MACROLIB',-1,0)
    macro=LCMGID(library,'MACROLIB')
    call REQUIRE_ASSOCIATED(macro,'plane-1 physical MACROLIB')
    call REQUIRE_CHARACTER12(macro,'SIGNATURE','L_MACROLIB')
    call REQUIRE_RECORD(macro,'STATE-VECTOR',NSTATE,1)
    call LCMGET(macro,'STATE-VECTOR',macro_state)
    if (macro_state(1) /= NGRP .or. macro_state(2) /= NMAT .or. &
        macro_state(3) /= 3 .or. macro_state(4) /= NIFIS .or. &
        macro_state(6) /= 2 .or. macro_state(13) /= 0) &
        error stop 'plane-1 MACROLIB state differs'
    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
    macro_groups=LCMGID(macro,'GROUP')
    call REQUIRE_ASSOCIATED(macro_groups,'plane-1 MACROLIB GROUP list')
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(macro_groups,ig)
    end do

    if (.not. EXACT_INVENTORY(plane,PLANE_ROOT_NAMES)) &
        error stop 'PROJECTED plane-1 root inventory differs'
    call REQUIRE_CHARACTER12(plane,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(plane,'STATE-VECTOR',NSTATE,1)
    call LCMGET(plane,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:18)=[NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1]
    if (any(state /= expected_state)) &
        error stop 'PROJECTED plane-1 state vector differs'
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
    call LCMGET(plane,'KEYFLX',plane_key)
    if (any(plane_key /= key)) &
        error stop 'PROJECTED KEYFLX differs from TRACK'
    call REQUIRE_CHARACTER_N(plane,'OPTION',1,4,'B0  ')
    call REQUIRE_CHARACTER12(plane,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER12(plane,'LINK.TRACK','TRACK')
    call REQUIRE_CHARACTER12(plane,'LINK.SYSTEM','SYSTEM')
    call REQUIRE_RECORD(plane,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(plane,'SPOT-LEAK1D',leakage)
    if (.not. all(ieee_is_finite(leakage))) &
        error stop 'PROJECTED plane-1 leakage is nonfinite'

    call REQUIRE_RECORD(plane,'SPOT-R64',-1,0)
    plane_authority=LCMGID(plane,'SPOT-R64')
    call REQUIRE_ASSOCIATED(plane_authority,'PROJECTED plane-1 authority')
    if (.not. EXACT_INVENTORY(plane_authority,PLANE_AUTHORITY_NAMES)) &
        error stop 'PROJECTED plane-1 authority inventory differs'
    call REQUIRE_RECORD(plane_authority,'RHO',1,4)
    call REQUIRE_CHARACTER12(plane_authority,'STATE','PROJECTED')
    call REQUIRE_RECORD(plane_authority,'EPOCH',1,1)
    call REQUIRE_RECORD(plane_authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(plane,'FLUX',NGRP,10)
    call LCMGET(plane_authority,'RHO',plane_rho)
    call LCMGET(plane_authority,'EPOCH',plane_epoch)
    if (.not. ieee_is_finite(plane_rho)) &
        error stop 'PROJECTED plane-1 RHO is nonfinite'
    if (transfer(plane_rho,0_int64) /= transfer(root_rho,0_int64)) &
        error stop 'PROJECTED plane-1 RHO differs from root'
    if (plane_epoch /= root_epoch) &
        error stop 'PROJECTED plane-1 epoch differs from root'
    rho=plane_rho
    authority_flux=LCMGID(plane_authority,'FLUX')
    mirror_flux=LCMGID(plane,'FLUX')
    call REQUIRE_ASSOCIATED(authority_flux,'plane-1 REAL64 FLUX list')
    call REQUIRE_ASSOCIATED(mirror_flux,'plane-1 REAL32 FLUX list')
    positive_count=0
    do ig=1,NGRP
      call REQUIRE_LIST_RECORD(authority_flux,ig,NUNKNO,4)
      call REQUIRE_LIST_RECORD(mirror_flux,ig,NUNKNO,2)
      call LCMGDL(authority_flux,ig,flux(:,ig))
      call LCMGDL(mirror_flux,ig,mirror)
      if (.not. all(ieee_is_finite(flux(:,ig))) .or. &
          .not. all(ieee_is_finite(mirror))) &
          error stop 'PROJECTED plane-1 flux is nonfinite'
      if (any(abs(flux(:,ig)) > REAL32_MAX64)) &
          error stop 'PROJECTED plane-1 flux exceeds REAL32 range'
      if (any(transfer(mirror,0_int32,NUNKNO) /= &
          transfer(real(flux(:,ig),real32),0_int32,NUNKNO))) &
          error stop 'PROJECTED plane-1 compatibility flux differs'
      do ir=1,NREG
        if (flux(key(ir),ig) <= +0.0_real64) &
            error stop 'PROJECTED region flux is not strictly positive'
        positive_count=positive_count+1
      end do
    end do
  end subroutine VERIFY_PROJECTED_PLANE1


  subroutine VERIFY_MACRO_OUTPUT(input,output,expected_keff,zero_count, &
      record_count,word_count)
    type(c_ptr), intent(in) :: input, output
    real(real64), intent(in) :: expected_keff
    integer, intent(out) :: zero_count
    integer(int64), intent(out) :: record_count, word_count

    character(len=12) :: first_name, name
    integer :: input_count, output_count, length, record_type
    integer :: marker
    real(real32) :: found_keff, expected_keff32
    type(c_ptr) :: input_groups, output_groups

    call COUNT_DICTIONARY_NAMES(input,input_count)
    call COUNT_DICTIONARY_NAMES(output,output_count)
    if (input_count <= 0 .or. output_count /= input_count+2) &
        error stop 'zero-fission MACRO root inventory count differs'
    call REQUIRE_ABSENT(input,'SPOT-FROZEN')
    call REQUIRE_ABSENT(input,'SPOT-KEFF')
    call REQUIRE_RECORD(output,'SPOT-FROZEN',1,1)
    call REQUIRE_RECORD(output,'SPOT-KEFF',1,2)
    call LCMGET(output,'SPOT-FROZEN',marker)
    call LCMGET(output,'SPOT-KEFF',found_keff)
    expected_keff32=real(expected_keff,real32)
    if (marker /= 1) error stop 'zero-fission MACRO marker differs'
    if (.not. ieee_is_finite(found_keff) .or. &
        transfer(found_keff,0_int32) /= &
        transfer(expected_keff32,0_int32)) &
        error stop 'zero-fission MACRO eigenvalue mirror differs'

    zero_count=0
    record_count=0_int64
    word_count=0_int64
    name=' '
    call LCMNXT(input,name)
    if (name == ' ') error stop 'input MACROLIB is empty'
    first_name=name
    do
      call LCMLEN(input,name,length,record_type)
      if (name == 'GROUP') then
        call REQUIRE_RECORD(output,name,NGRP,10)
        if (length /= NGRP .or. record_type /= 10) &
            error stop 'input MACROLIB GROUP schema differs'
        input_groups=LCMGID(input,name)
        output_groups=LCMGID(output,name)
        call REQUIRE_ASSOCIATED(input_groups,'input MACROLIB groups')
        call REQUIRE_ASSOCIATED(output_groups,'output MACROLIB groups')
        call COMPARE_MACRO_GROUPS(input_groups,output_groups,zero_count, &
            record_count,word_count)
      else
        call COMPARE_NAMED_ENTRY(input,output,name,record_count,word_count)
      end if
      call LCMNXT(input,name)
      if (name == first_name) exit
    end do
    if (zero_count /= NGRP*NMAT*NIFIS) &
        error stop 'zero-fission MACRO NUSIGF inventory differs'
  end subroutine VERIFY_MACRO_OUTPUT


  subroutine COMPARE_MACRO_GROUPS(left,right,zero_count,record_count, &
      word_count)
    type(c_ptr), intent(in) :: left, right
    integer, intent(inout) :: zero_count
    integer(int64), intent(inout) :: record_count, word_count

    character(len=12) :: first_name, name
    integer :: ig, left_count, right_count
    real(real32) :: input_nusigf(NMAT*NIFIS)
    real(real32) :: output_nusigf(NMAT*NIFIS)
    type(c_ptr) :: left_group, right_group

    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(left,ig)
      call REQUIRE_DIRECTORY_ITEM(right,ig)
      left_group=LCMGIL(left,ig)
      right_group=LCMGIL(right,ig)
      call REQUIRE_ASSOCIATED(left_group,'input MACROLIB group')
      call REQUIRE_ASSOCIATED(right_group,'output MACROLIB group')
      call COUNT_DICTIONARY_NAMES(left_group,left_count)
      call COUNT_DICTIONARY_NAMES(right_group,right_count)
      if (left_count <= 0 .or. right_count /= left_count) &
          error stop 'zero-fission MACRO group inventory differs'
      name=' '
      call LCMNXT(left_group,name)
      if (name == ' ') error stop 'input MACROLIB group is empty'
      first_name=name
      do
        if (name == 'NUSIGF') then
          call REQUIRE_RECORD(left_group,name,NMAT*NIFIS,2)
          call REQUIRE_RECORD(right_group,name,NMAT*NIFIS,2)
          call LCMGET(left_group,name,input_nusigf)
          call LCMGET(right_group,name,output_nusigf)
          if (.not. all(ieee_is_finite(input_nusigf)) .or. &
              any(input_nusigf < +0.0_real32)) &
              error stop 'physical NUSIGF is invalid'
          if (any(transfer(output_nusigf,0_int32,NMAT*NIFIS) /= &
              0_int32)) error stop 'output NUSIGF is not positive zero'
          zero_count=zero_count+NMAT*NIFIS
        else
          call COMPARE_NAMED_ENTRY(left_group,right_group,name, &
              record_count,word_count)
        end if
        call LCMNXT(left_group,name)
        if (name == first_name) exit
      end do
    end do
  end subroutine COMPARE_MACRO_GROUPS


  subroutine RECOMPUTE_QFISS(macro,rho,material,key,volume,flux,qfiss, &
      qint,nonregion_count)
    type(c_ptr), intent(in) :: macro
    real(real64), intent(in) :: rho
    integer, intent(in) :: material(NREG), key(NREG)
    real(real32), intent(in) :: volume(NREG)
    real(real64), intent(in) :: flux(NUNKNO,NGRP)
    real(real64), intent(out) :: qfiss(NUNKNO,NGRP), qint(NGRP)
    integer, intent(out) :: nonregion_count

    integer :: ir, ifis, h, g, ibm, iunk, iu
    logical :: mapped(NUNKNO)
    real(real32) :: group_chi(NMAT,NIFIS)
    real(real32) :: group_nusigf(NMAT,NIFIS)
    real(real32), allocatable :: chi32(:,:,:), nusigf32(:,:,:)
    real(real64) :: product, fission_rate, contribution
    type(c_ptr) :: groups, group

    call REQUIRE_RECORD(macro,'GROUP',NGRP,10)
    groups=LCMGID(macro,'GROUP')
    call REQUIRE_ASSOCIATED(groups,'physical MACROLIB groups')
    allocate(chi32(NMAT,NIFIS,NGRP),nusigf32(NMAT,NIFIS,NGRP))
    do g=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(groups,g)
      group=LCMGIL(groups,g)
      call REQUIRE_RECORD(group,'CHI',NMAT*NIFIS,2)
      call REQUIRE_RECORD(group,'NUSIGF',NMAT*NIFIS,2)
      call LCMGET(group,'CHI',group_chi)
      call LCMGET(group,'NUSIGF',group_nusigf)
      if (.not. all(ieee_is_finite(group_chi)) .or. &
          any(group_chi < +0.0_real32)) &
          error stop 'physical CHI is invalid'
      if (.not. all(ieee_is_finite(group_nusigf)) .or. &
          any(group_nusigf < +0.0_real32)) &
          error stop 'physical NUSIGF is invalid'
      chi32(:,:,g)=group_chi
      nusigf32(:,:,g)=group_nusigf
    end do

    ! Independent ordered oracle.  Each multiply and each add is assigned to
    ! a REAL64 scalar before the next operation.  The four loop levels are
    ! the frozen numerical definition: ir -> ifis -> h -> g.
    qfiss=+0.0_real64
    do ir=1,NREG
      ibm=material(ir)
      iunk=key(ir)
      do ifis=1,NIFIS
        fission_rate=+0.0_real64
        do h=1,NGRP
          product=real(nusigf32(ibm,ifis,h),real64)*flux(iunk,h)
          if (.not. ieee_is_finite(product) .or. &
              product < +0.0_real64) &
              error stop 'ordered fission product is invalid'
          fission_rate=fission_rate+product
          if (.not. ieee_is_finite(fission_rate) .or. &
              fission_rate < +0.0_real64) &
              error stop 'ordered fission rate is invalid'
        end do
        do g=1,NGRP
          contribution=real(chi32(ibm,ifis,g),real64)*fission_rate
          if (.not. ieee_is_finite(contribution) .or. &
              contribution < +0.0_real64) &
              error stop 'ordered CHI contribution is invalid'
          contribution=contribution*rho
          if (.not. ieee_is_finite(contribution) .or. &
              contribution < +0.0_real64) &
              error stop 'ordered rho contribution is invalid'
          qfiss(iunk,g)=qfiss(iunk,g)+contribution
          if (.not. ieee_is_finite(qfiss(iunk,g)) .or. &
              qfiss(iunk,g) < +0.0_real64) &
              error stop 'ordered QFISS accumulation is invalid'
        end do
      end do
    end do

    mapped=.false.
    mapped(key)=.true.
    nonregion_count=0
    do g=1,NGRP
      do iu=1,NUNKNO
        if (.not. mapped(iu)) then
          if (transfer(qfiss(iu,g),0_int64) /= 0_int64) &
              error stop 'non-region QFISS is not positive zero'
          nonregion_count=nonregion_count+1
        end if
      end do
    end do
    if (.not. all(ieee_is_finite(qfiss)) .or. &
        any(qfiss < +0.0_real64)) &
        error stop 'independent QFISS is invalid'

    qint=+0.0_real64
    do g=1,NGRP
      do ir=1,NREG
        product=real(volume(ir),real64)*qfiss(key(ir),g)
        if (.not. ieee_is_finite(product) .or. &
            product < +0.0_real64) &
            error stop 'ordered QINT product is invalid'
        qint(g)=qint(g)+product
        if (.not. ieee_is_finite(qint(g)) .or. &
            qint(g) < +0.0_real64) &
            error stop 'ordered QINT accumulation is invalid'
      end do
    end do
    if (qint(1) <= +0.0_real64) &
        error stop 'first-group source integral is not positive'
  end subroutine RECOMPUTE_QFISS


  subroutine VERIFY_SOURCE_OUTPUT(source,rho,keff,expected_epoch,qfiss, &
      qint,qfiss_count,dsour_count,qint_count)
    type(c_ptr), intent(in) :: source
    real(real64), intent(in) :: rho, keff
    integer, intent(in) :: expected_epoch
    real(real64), intent(in) :: qfiss(NUNKNO,NGRP), qint(NGRP)
    integer, intent(out) :: qfiss_count, dsour_count, qint_count

    integer :: state(NSTATE), expected_state(NSTATE)
    integer :: marker, plane, epoch, g
    integer(int32) :: qfiss32_bits(NUNKNO), expected32_bits(NUNKNO)
    integer(int64) :: qfiss64_bits(NUNKNO), expected64_bits(NUNKNO)
    real(real32) :: source_keff, expected_keff32
    real(real32) :: qint32(NGRP), expected_qint32(NGRP)
    real(real32) :: dsour32(NUNKNO)
    real(real64) :: source_rho, authority_qfiss(NUNKNO)
    type(c_ptr) :: authority, qfiss_list, dsour_outer, dsour_inner

    if (.not. EXACT_INVENTORY(source,SOURCE_ROOT_NAMES)) &
        error stop 'SOURCE root inventory differs'
    call REQUIRE_CHARACTER12(source,'SIGNATURE','L_SOURCE')
    call REQUIRE_RECORD(source,'STATE-VECTOR',NSTATE,1)
    call LCMGET(source,'STATE-VECTOR',state)
    expected_state=0
    expected_state(1:3)=[NGRP,NUNKNO,1]
    if (any(state /= expected_state)) &
        error stop 'SOURCE state vector differs'
    call REQUIRE_RECORD(source,'SPOT-FROZEN',1,1)
    call LCMGET(source,'SPOT-FROZEN',marker)
    if (marker /= 1) error stop 'SOURCE frozen marker differs'
    call REQUIRE_RECORD(source,'SPOT-KEFF',1,2)
    call LCMGET(source,'SPOT-KEFF',source_keff)
    expected_keff32=real(keff,real32)
    if (.not. ieee_is_finite(source_keff) .or. &
        transfer(source_keff,0_int32) /= &
        transfer(expected_keff32,0_int32)) &
        error stop 'SOURCE eigenvalue mirror differs'

    call REQUIRE_RECORD(source,'SPOT-QINT',NGRP,2)
    call LCMGET(source,'SPOT-QINT',qint32)
    expected_qint32=real(qint,real32)
    if (.not. all(ieee_is_finite(qint32)) .or. &
        any(qint32 < +0.0_real32)) &
        error stop 'SOURCE QINT is invalid'
    if (any(transfer(qint32,0_int32,NGRP) /= &
        transfer(expected_qint32,0_int32,NGRP))) &
        error stop 'SOURCE QINT one-time downcast differs'
    if (qint32(1) <= +0.0_real32) &
        error stop 'SOURCE first-group QINT is not positive'
    qint_count=NGRP

    call REQUIRE_RECORD(source,'SPOT-R64',-1,0)
    authority=LCMGID(source,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'SOURCE REAL64 authority')
    if (.not. EXACT_INVENTORY(authority,SOURCE_AUTHORITY_NAMES)) &
        error stop 'SOURCE authority inventory differs'
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call REQUIRE_RECORD(authority,'PLANE',1,1)
    call REQUIRE_CHARACTER12(authority,'STATE','FROZEN-QFIS')
    call REQUIRE_RECORD(authority,'QFISS',NGRP,10)
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call LCMGET(authority,'RHO',source_rho)
    call LCMGET(authority,'PLANE',plane)
    call LCMGET(authority,'EPOCH',epoch)
    if (.not. ieee_is_finite(source_rho) .or. &
        transfer(source_rho,0_int64) /= transfer(rho,0_int64)) &
        error stop 'SOURCE authority RHO differs from plane'
    if (plane /= 1) error stop 'SOURCE authority plane differs'
    if (epoch /= expected_epoch) &
        error stop 'SOURCE authority epoch differs from plane'

    qfiss_list=LCMGID(authority,'QFISS')
    call REQUIRE_ASSOCIATED(qfiss_list,'SOURCE type-4 QFISS list')
    qfiss_count=0
    do g=1,NGRP
      call REQUIRE_LIST_RECORD(qfiss_list,g,NUNKNO,4)
      call LCMGDL(qfiss_list,g,authority_qfiss)
      if (.not. all(ieee_is_finite(authority_qfiss)) .or. &
          any(authority_qfiss < +0.0_real64)) &
          error stop 'SOURCE type-4 QFISS is invalid'
      qfiss64_bits=transfer(authority_qfiss,0_int64,NUNKNO)
      expected64_bits=transfer(qfiss(:,g),0_int64,NUNKNO)
      if (any(qfiss64_bits /= expected64_bits)) &
          error stop 'SOURCE type-4 QFISS formula bits differ'
      qfiss_count=qfiss_count+NUNKNO
    end do

    call REQUIRE_RECORD(source,'DSOUR',1,10)
    dsour_outer=LCMGID(source,'DSOUR')
    call REQUIRE_ASSOCIATED(dsour_outer,'SOURCE DSOUR outer list')
    call REQUIRE_LIST_RECORD(dsour_outer,1,NGRP,10)
    dsour_inner=LCMGIL(dsour_outer,1)
    call REQUIRE_ASSOCIATED(dsour_inner,'SOURCE DSOUR group list')
    dsour_count=0
    do g=1,NGRP
      call REQUIRE_LIST_RECORD(dsour_inner,g,NUNKNO,2)
      call LCMGDL(dsour_inner,g,dsour32)
      if (.not. all(ieee_is_finite(dsour32)) .or. &
          any(dsour32 < +0.0_real32)) &
          error stop 'SOURCE DSOUR is invalid'
      qfiss32_bits=transfer(dsour32,0_int32,NUNKNO)
      expected32_bits=transfer(real(qfiss(:,g),real32),0_int32,NUNKNO)
      if (any(qfiss32_bits /= expected32_bits)) &
          error stop 'SOURCE DSOUR one-time downcast differs'
      dsour_count=dsour_count+NUNKNO
    end do
  end subroutine VERIFY_SOURCE_OUTPUT


  recursive subroutine COMPARE_DICTIONARY(left,right,record_count, &
      word_count)
    type(c_ptr), intent(in) :: left, right
    integer(int64), intent(inout) :: record_count, word_count
    character(len=12) :: first_name, name
    integer :: left_count, right_count

    call COUNT_DICTIONARY_NAMES(left,left_count)
    call COUNT_DICTIONARY_NAMES(right,right_count)
    if (left_count /= right_count) &
        error stop 'recursive dictionary inventory differs'
    if (left_count == 0) return
    name=' '
    call LCMNXT(left,name)
    first_name=name
    do
      call COMPARE_NAMED_ENTRY(left,right,name,record_count,word_count)
      call LCMNXT(left,name)
      if (name == first_name) exit
    end do
  end subroutine COMPARE_DICTIONARY


  subroutine COMPARE_NAMED_ENTRY(left,right,name,record_count,word_count)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer(int64), intent(inout) :: record_count, word_count
    integer :: left_length, right_length, left_type, right_type
    type(c_ptr) :: left_child, right_child

    call LCMLEN(left,name,left_length,left_type)
    call LCMLEN(right,name,right_length,right_type)
    if (left_length /= right_length .or. left_type /= right_type) &
        error stop 'recursive named-entry schema differs'
    select case(left_type)
    case(0)
      left_child=LCMGID(left,name)
      right_child=LCMGID(right,name)
      call REQUIRE_ASSOCIATED(left_child,'left recursive directory')
      call REQUIRE_ASSOCIATED(right_child,'right recursive directory')
      call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
    case(10)
      left_child=LCMGID(left,name)
      right_child=LCMGID(right,name)
      call REQUIRE_ASSOCIATED(left_child,'left recursive list')
      call REQUIRE_ASSOCIATED(right_child,'right recursive list')
      call COMPARE_LIST(left_child,right_child,left_length,record_count, &
          word_count)
    case default
      call COMPARE_NAMED_PAYLOAD(left,right,name,left_length,left_type, &
          record_count,word_count)
    end select
  end subroutine COMPARE_NAMED_ENTRY


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
          error stop 'recursive list-item schema differs'
      select case(left_type)
      case(0)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left list directory')
        call REQUIRE_ASSOCIATED(right_child,'right list directory')
        call COMPARE_DICTIONARY(left_child,right_child,record_count,word_count)
      case(10)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
        call REQUIRE_ASSOCIATED(left_child,'left nested list')
        call REQUIRE_ASSOCIATED(right_child,'right nested list')
        call COMPARE_LIST(left_child,right_child,left_length,record_count, &
            word_count)
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
          error stop 'recursive integer or character bits differ'
      word_count=word_count+length
    case(2)
      allocate(real_left(length),real_right(length))
      call LCMGET(left,name,real_left)
      call LCMGET(right,name,real_right)
      if (any(transfer(real_left,0_int32,length) /= &
          transfer(real_right,0_int32,length))) &
          error stop 'recursive REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(double_left(length),double_right(length))
      call LCMGET(left,name,double_left)
      call LCMGET(right,name,double_right)
      if (any(transfer(double_left,0_int64,length) /= &
          transfer(double_right,0_int64,length))) &
          error stop 'recursive REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(logical_left(length),logical_right(length))
      call LCMGET(left,name,logical_left)
      call LCMGET(right,name,logical_right)
      if (any(transfer(logical_left,0_int32,length) /= &
          transfer(logical_right,0_int32,length))) &
          error stop 'recursive logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(complex_left(length),complex_right(length))
      call LCMGET(left,name,complex_left)
      call LCMGET(right,name,complex_right)
      if (any(transfer(complex_left,0_int32,2*length) /= &
          transfer(complex_right,0_int32,2*length))) &
          error stop 'recursive complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported recursive GANLIB record type'
    end select
    record_count=record_count+1_int64
  end subroutine COMPARE_NAMED_PAYLOAD


  subroutine COMPARE_LIST_PAYLOAD(left,right,index,length,record_type, &
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
          error stop 'recursive list integer or character bits differ'
      word_count=word_count+length
    case(2)
      allocate(real_left(length),real_right(length))
      call LCMGDL(left,index,real_left)
      call LCMGDL(right,index,real_right)
      if (any(transfer(real_left,0_int32,length) /= &
          transfer(real_right,0_int32,length))) &
          error stop 'recursive list REAL32 bits differ'
      word_count=word_count+length
    case(4)
      allocate(double_left(length),double_right(length))
      call LCMGDL(left,index,double_left)
      call LCMGDL(right,index,double_right)
      if (any(transfer(double_left,0_int64,length) /= &
          transfer(double_right,0_int64,length))) &
          error stop 'recursive list REAL64 bits differ'
      word_count=word_count+2_int64*length
    case(5)
      allocate(logical_left(length),logical_right(length))
      call LCMGDL(left,index,logical_left)
      call LCMGDL(right,index,logical_right)
      if (any(transfer(logical_left,0_int32,length) /= &
          transfer(logical_right,0_int32,length))) &
          error stop 'recursive list logical bits differ'
      word_count=word_count+length
    case(6)
      allocate(complex_left(length),complex_right(length))
      call LCMGDL(left,index,complex_left)
      call LCMGDL(right,index,complex_right)
      if (any(transfer(complex_left,0_int32,2*length) /= &
          transfer(complex_right,0_int32,2*length))) &
          error stop 'recursive list complex bits differ'
      word_count=word_count+2_int64*length
    case default
      error stop 'unsupported recursive GANLIB list-item type'
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

end program CHECK_B2N_REAL64_FROZEN_QFISS
