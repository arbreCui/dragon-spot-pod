program CHECK_B2L_REAL_ASM
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NSTATE=40
  integer, parameter :: NGRP=370
  integer, parameter :: NSNAP=3
  integer, parameter :: NUNKNO=14
  integer, parameter :: NMAT=8
  integer(int32), parameter :: REAL32_MAGNITUDE_MASK = &
      int(z'7fffffff',int32)
  character(len=12), parameter :: SYSTEM_ROOT_NAMES(7) = &
      [character(len=12) :: 'SIGNATURE','LINK.MACRO','LINK.TRACK', &
       'STATE-VECTOR', &
       'SPOT-LEAK1D','SPOT-L1-SNAP','GROUP       ']
  character(len=12), parameter :: GROUP_NAMES(15) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG', &
       'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
       'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DRAGON-TXSC ', &
       'SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG  ']
  character(len=12), parameter :: RESPONSE_NAMES(12) = &
      [character(len=12) :: 'CF$MCCG','ILUDF$MCCG','CQ$MCCG', &
       'DIAGQ$MCCG', &
       'PJJ$MCCG    ','PJJX$MCCG   ','PJJY$MCCG   ','PJJZ$MCCG   ', &
       'PJJXI$MCCG  ','PJJYI$MCCG  ','PJJZI$MCCG  ','DIAGF$MCCG  ']
  integer, parameter :: RESPONSE_LENGTHS(12) = &
      [32,14,32,14,8,8,8,8,8,8,8,14]

  character(len=1024) :: projected_path, system_path, source_path
  integer :: formula_tx_bits, formula_sphys_bits, formula_sused_bits
  integer :: response_values, response_nonzero, group_records
  integer(int64) :: full_copy_records, full_copy_words
  type(c_ptr) :: projected, system, source

  if (command_argument_count() /= 3) error stop &
      'expected PROJECTED, SYSTEM1, and frozen source archive paths'
  call get_command_argument(1,projected_path)
  call get_command_argument(2,system_path)
  call get_command_argument(3,source_path)

  call LCMOP(projected,trim(projected_path),2,2,0)
  call LCMOP(system,trim(system_path),2,2,0)
  call LCMOP(source,trim(source_path),2,2,0)
  call REQUIRE_ASSOCIATED(projected,'persistent PROJECTED archive')
  call REQUIRE_ASSOCIATED(system,'real ASM SYSTEM output')
  call REQUIRE_ASSOCIATED(source,'frozen source archive')

  call VERIFY_PROJECTED_AND_FULL_COPIES(projected,source, &
      full_copy_records,full_copy_words)
  call VERIFY_REAL_SYSTEM(projected,system,formula_tx_bits, &
      formula_sphys_bits,formula_sused_bits,response_values, &
      response_nonzero,group_records)

  call LCMCL(source,1)
  call LCMCL(system,1)
  call LCMCL(projected,1)

  if (formula_tx_bits /= NGRP*(NMAT+1)) &
      error stop 'TX bit-check inventory differs'
  if (formula_sphys_bits /= NGRP*(NMAT+1)) &
      error stop 'S0 physical bit-check inventory differs'
  if (formula_sused_bits /= NGRP*(NMAT+1)) &
      error stop 'S0 used bit-check inventory differs'
  if (response_values /= NGRP*sum(RESPONSE_LENGTHS)) &
      error stop 'response-value inventory differs'
  if (response_nonzero <= 0) &
      error stop 'all real response values are exactly zero'
  if (group_records /= NGRP*size(GROUP_NAMES)) &
      error stop 'group-record inventory differs'
  if (full_copy_records <= 0_int64 .or. full_copy_words <= 0_int64) &
      error stop 'full-copy comparison inventory is empty'

  write(*,'(A)') 'B2L REAL ASM POSTERIOR PASS'
  write(*,'(A,I0,A,I0)') 'B2L FULL-COPY-RECORDS=',full_copy_records, &
      ' FULL-COPY-32BIT-WORDS=',full_copy_words
  write(*,'(A,I0,A,I0)') 'B2L GROUPS=',NGRP, &
      ' EXACT-GROUP-RECORDS=',group_records
  write(*,'(A,I0,A,I0)') 'B2L RESPONSE-FINITE-VALUES=',response_values, &
      ' RESPONSE-NONZERO-VALUES=',response_nonzero
  write(*,'(A,I0,A,I0,A,I0)') 'B2L TXSC-BITS=',formula_tx_bits, &
      ' S0PHYS-BITS=',formula_sphys_bits, &
      ' S0USED-BITS=',formula_sused_bits
  write(*,'(A)') &
      'B2L B2K-PLANE1-POSTERIOR=COMPATIBLE EMPIRICAL-CONTROLS=0'
  write(*,'(A)') &
      'B2L RESPONSE-ACCURACY=NOT-EVALUATED CONVERGENCE=NOT-EVALUATED'

contains

  subroutine VERIFY_PROJECTED_AND_FULL_COPIES(root,real_archive, &
      compared_records,compared_words)
    type(c_ptr), intent(in) :: root, real_archive
    integer(int64), intent(out) :: compared_records, compared_words

    character(len=12), parameter :: root_names(7) = &
        [character(len=12) :: 'SIGNATURE','LISTDIM','SPOT-ITER-K', &
         'TRACK', &
         'MICROLIB2   ','FLUX        ','SPOT-R64    ']
    character(len=12), parameter :: authority_names(4) = &
        [character(len=12) :: 'RHO','NPLANE','STATE','EPOCH']
    character(len=12), parameter :: plane_names(12) = &
        [character(len=12) :: 'SIGNATURE','STATE-VECTOR', &
         'EPS-CONVERGE','IMERGE-LEAK', &
         'KEYFLX      ','OPTION      ','LINK.MACRO  ','LINK.TRACK  ', &
         'LINK.SYSTEM','SPOT-LEAK1D','SPOT-R64    ','FLUX        ']
    character(len=12), parameter :: plane_authority_names(4) = &
        [character(len=12) :: 'RHO','STATE','EPOCH','FLUX']
    integer :: listdim, epoch, ip
    type(c_ptr) :: authority, tracks, libraries, fluxes, plane
    type(c_ptr) :: plane_authority, source_tracks, source_libraries
    type(c_ptr) :: left_item, right_item

    if (.not. EXACT_INVENTORY(root,root_names)) &
        error stop 'PROJECTED root inventory differs'
    call REQUIRE_CHARACTER(root,'SIGNATURE','L_ARCHIVE')
    call REQUIRE_RECORD(root,'LISTDIM',1,1)
    call LCMGET(root,'LISTDIM',listdim)
    if (listdim /= NSNAP) error stop 'PROJECTED plane count differs'
    call REQUIRE_ABSENT(root,'SYSTEM')
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'PROJECTED root authority')
    if (.not. EXACT_INVENTORY(authority,authority_names)) &
        error stop 'PROJECTED authority inventory differs'
    call REQUIRE_CHARACTER(authority,'STATE','PROJECTED')
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= 1) error stop 'PROJECTED root epoch differs'

    tracks=LCMGID(root,'TRACK')
    libraries=LCMGID(root,'MICROLIB2')
    fluxes=LCMGID(root,'FLUX')
    source_tracks=LCMGID(real_archive,'TRACK')
    source_libraries=LCMGID(real_archive,'MICROLIB2')
    call REQUIRE_ASSOCIATED(tracks,'PROJECTED TRACK list')
    call REQUIRE_ASSOCIATED(libraries,'PROJECTED MICROLIB2 list')
    call REQUIRE_ASSOCIATED(fluxes,'PROJECTED FLUX list')
    call REQUIRE_ASSOCIATED(source_tracks,'source TRACK list')
    call REQUIRE_ASSOCIATED(source_libraries,'source MICROLIB2 list')

    compared_records=0_int64
    compared_words=0_int64
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(tracks,ip)
      call REQUIRE_DIRECTORY_ITEM(source_tracks,ip)
      left_item=LCMGIL(tracks,ip)
      right_item=LCMGIL(source_tracks,ip)
      call COMPARE_DICTIONARY(left_item,right_item,compared_records, &
          compared_words)

      call REQUIRE_DIRECTORY_ITEM(libraries,ip)
      call REQUIRE_DIRECTORY_ITEM(source_libraries,ip)
      left_item=LCMGIL(libraries,ip)
      right_item=LCMGIL(source_libraries,ip)
      call COMPARE_DICTIONARY(left_item,right_item,compared_records, &
          compared_words)

      call REQUIRE_DIRECTORY_ITEM(fluxes,ip)
      plane=LCMGIL(fluxes,ip)
      if (.not. EXACT_INVENTORY(plane,plane_names)) &
          error stop 'PROJECTED plane inventory differs'
      call REQUIRE_CHARACTER(plane,'SIGNATURE','L_FLUX')
      plane_authority=LCMGID(plane,'SPOT-R64')
      call REQUIRE_ASSOCIATED(plane_authority,'plane authority')
      if (.not. EXACT_INVENTORY(plane_authority, &
          plane_authority_names)) &
          error stop 'PROJECTED plane authority inventory differs'
      call REQUIRE_CHARACTER(plane_authority,'STATE','PROJECTED')
      call REQUIRE_RECORD(plane_authority,'EPOCH',1,1)
      call LCMGET(plane_authority,'EPOCH',epoch)
      if (epoch /= 1) error stop 'PROJECTED plane epoch differs'
    end do
  end subroutine VERIFY_PROJECTED_AND_FULL_COPIES


  subroutine VERIFY_REAL_SYSTEM(root,system_root,tx_checks,sphys_checks, &
      sused_checks,response_count,nonzero_count,record_count)
    type(c_ptr), intent(in) :: root, system_root
    integer, intent(out) :: tx_checks, sphys_checks, sused_checks
    integer, intent(out) :: response_count, nonzero_count, record_count

    integer :: state(NSTATE), expected_state(NSTATE), snapshot
    integer :: ig, im, i
    real(real32) :: leakage(NGRP), system_leakage(NGRP)
    real(real32) :: ntot(NMAT), sigw(NMAT), tranc(NMAT)
    real(real32) :: tx(0:NMAT), sphys(0:NMAT), sused(0:NMAT)
    real(real32) :: expected_tx(0:NMAT), expected_sphys(0:NMAT)
    real(real32) :: expected_sused(0:NMAT)
    real(real32), allocatable :: response(:)
    type(c_ptr) :: fluxes, plane, libraries, library, macro
    type(c_ptr) :: macro_groups, macro_group, system_groups, system_group

    if (.not. EXACT_INVENTORY(system_root,SYSTEM_ROOT_NAMES)) &
        error stop 'real SYSTEM root inventory differs'
    call REQUIRE_CHARACTER(system_root,'SIGNATURE','L_PIJ')
    call REQUIRE_CHARACTER(system_root,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER(system_root,'LINK.TRACK','TRACK')
    call REQUIRE_RECORD(system_root,'STATE-VECTOR',NSTATE,1)
    call LCMGET(system_root,'STATE-VECTOR',state)
    expected_state=0
    expected_state([1,2,3,5,6,11])=1
    expected_state(7)=4
    expected_state(8)=NGRP
    expected_state(9)=NUNKNO
    expected_state(10)=NMAT
    if (any(state /= expected_state)) &
        error stop 'real SYSTEM state vector differs'
    call REQUIRE_RECORD(system_root,'SPOT-L1-SNAP',1,1)
    call LCMGET(system_root,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= 1) error stop 'real SYSTEM plane identity differs'
    call REQUIRE_RECORD(system_root,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(system_root,'SPOT-LEAK1D',system_leakage)
    if (.not. all(ieee_is_finite(system_leakage))) &
        error stop 'real SYSTEM leakage is nonfinite'

    fluxes=LCMGID(root,'FLUX')
    plane=LCMGIL(fluxes,1)
    call REQUIRE_RECORD(plane,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(plane,'SPOT-LEAK1D',leakage)
    if (any(transfer(system_leakage,0_int32,NGRP) /= &
        transfer(leakage,0_int32,NGRP))) &
        error stop 'real SYSTEM leakage bits differ from PROJECTED plane 1'

    libraries=LCMGID(root,'MICROLIB2')
    library=LCMGIL(libraries,1)
    macro=LCMGID(library,'MACROLIB')
    macro_groups=LCMGID(macro,'GROUP')
    system_groups=LCMGID(system_root,'GROUP')
    call REQUIRE_ASSOCIATED(macro_groups,'plane-1 MACROLIB groups')
    call REQUIRE_ASSOCIATED(system_groups,'real SYSTEM groups')

    tx_checks=0
    sphys_checks=0
    sused_checks=0
    response_count=0
    nonzero_count=0
    record_count=0
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(macro_groups,ig)
      call REQUIRE_DIRECTORY_ITEM(system_groups,ig)
      macro_group=LCMGIL(macro_groups,ig)
      system_group=LCMGIL(system_groups,ig)
      if (.not. EXACT_INVENTORY(system_group,GROUP_NAMES)) &
          error stop 'real SYSTEM group inventory differs'
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
          error stop 'real formula input is nonfinite'

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
      if (any(transfer(tx,0_int32,NMAT+1) /= &
          transfer(expected_tx,0_int32,NMAT+1))) &
          error stop 'real TX ordered binary32 formula differs'
      if (any(transfer(sphys,0_int32,NMAT+1) /= &
          transfer(expected_sphys,0_int32,NMAT+1))) &
          error stop 'real S0 physical ordered binary32 formula differs'
      if (any(transfer(sused,0_int32,NMAT+1) /= &
          transfer(expected_sused,0_int32,NMAT+1))) &
          error stop 'real S0 used ordered binary32 formula differs'
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
        ! Clear the IEEE sign bit so +0 and -0 are both zero.  All other
        ! finite binary32 values remain nonzero; no tolerance is used.
        nonzero_count=nonzero_count+count(iand( &
            transfer(response,0_int32,size(response)), &
            REAL32_MAGNITUDE_MASK) /= 0_int32)
        deallocate(response)
      end do
    end do
  end subroutine VERIFY_REAL_SYSTEM


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
        call COMPARE_DICTIONARY(left_child,right_child,record_count, &
            word_count)
      case(10)
        left_child=LCMGID(left,name)
        right_child=LCMGID(right,name)
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
        call COMPARE_DICTIONARY(left_child,right_child,record_count, &
            word_count)
      case(10)
        left_child=LCMGIL(left,index)
        right_child=LCMGIL(right,index)
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
          error stop 'full-copy integer/character bits differ'
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
          error stop 'full-copy list integer/character bits differ'
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


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
        error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_CHARACTER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    character(len=12) :: found

    call REQUIRE_RECORD(root,name,3,3)
    call LCMGTC(root,name,12,found)
    if (found /= expected) error stop 'character record differs'
  end subroutine REQUIRE_CHARACTER


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

end program CHECK_B2L_REAL_ASM
