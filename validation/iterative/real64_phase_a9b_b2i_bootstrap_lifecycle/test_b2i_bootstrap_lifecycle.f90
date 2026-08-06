program TEST_B2I_BOOTSTRAP_LIFECYCLE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite, &
      ieee_quiet_nan, ieee_value
  use SPOR64_B2I, only : SPOR64_B2I_ADMISSION_FAILED, &
      SPOR64_B2I_BOOTSTRAP_COMMITTED, SPOR64_B2I_SEAL_BOOTSTRAP
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED, &
      SPOR64_B2C_PUBLISH
  implicit none

  integer, parameter :: NSTATE=40, NGRP=370, NREG=8
  integer, parameter :: NSNAP=3, NUNKNO=14, NMAT_LOCAL=8
  integer, parameter :: NREJECTION=12
  integer(int32), parameter :: B2C_TOL_BITS=int(z'348637bd',int32)
  character(len=1024) :: axial_path, archive_path, axial_track_path
  integer :: seal_calls, rejection_count, authority_bit_checks
  integer :: mirror_bit_checks, deep_copy_checks, history_exclusions
  integer :: b2c_publish_calls
  type(c_ptr) :: axial_base, archive_base, axial_track_base
  type(c_ptr) :: candidate_base

  if (command_argument_count() /= 3) error stop &
    'expected state1_axial.xsm, state1_snapshots.xsm, and axial track paths'
  call get_command_argument(1,axial_path)
  call get_command_argument(2,archive_path)
  call get_command_argument(3,axial_track_path)

  call LCMOP(axial_base,trim(axial_path),2,2,0)
  call LCMOP(archive_base,trim(archive_path),2,2,0)
  call LCMOP(axial_track_base,trim(axial_track_path),2,2,0)
  if (.not. c_associated(axial_base) .or. &
      .not. c_associated(archive_base) .or. &
      .not. c_associated(axial_track_base)) &
    error stop 'read-only real XSM open failed'

  seal_calls=0
  rejection_count=0
  authority_bit_checks=0
  mirror_bit_checks=0
  deep_copy_checks=0
  history_exclusions=0
  b2c_publish_calls=0

  call BUILD_LIGHTWEIGHT_CANDIDATE(candidate_base)
  call VERIFY_UNSEALED_INPUT(axial_base,candidate_base)
  call RUN_POSITIVE()
  call RUN_REJECTION(1)
  call RUN_REJECTION(2)
  call RUN_REJECTION(3)
  call RUN_REJECTION(4)
  call RUN_REJECTION(5)
  call RUN_REJECTION(6)
  call RUN_REJECTION(7)
  call RUN_REJECTION(8)
  call RUN_REJECTION(9)
  call RUN_REJECTION(10)
  call RUN_REJECTION(11)
  call RUN_REJECTION(12)

  if (seal_calls /= NREJECTION+1) &
    error stop 'seal-call inventory differs'
  if (rejection_count /= NREJECTION) &
    error stop 'rejection inventory differs'
  if (authority_bit_checks /= 2*NUNKNO*NGRP*NSNAP) &
    error stop 'REAL64 authority bit-check inventory differs'
  if (mirror_bit_checks /= 2*NUNKNO*NGRP*NSNAP) &
    error stop 'REAL32 mirror bit-check inventory differs'
  if (deep_copy_checks /= 4*NSNAP) &
    error stop 'four-list deep-copy inventory differs'
  if (history_exclusions /= 3) &
    error stop 'root history exclusion inventory differs'
  if (b2c_publish_calls /= NSNAP) &
    error stop 'B2C producer-call inventory differs'

  call LCMCL(candidate_base,2)
  call LCMCL(axial_track_base,1)
  call LCMCL(archive_base,1)
  call LCMCL(axial_base,1)

  write(*,'(A)') 'B2I BOOTSTRAP-LIFECYCLE PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2I SEAL-CALLS=',seal_calls, &
      ' COMMITS=1 REJECTIONS=',rejection_count
  write(*,'(A)') &
      'B2I FRESH-ZERO-WRITE-REJECTIONS=11 COLLISION-NO-NEW-WRITES=1'
  write(*,'(A,I0,A,I0)') 'B2I AUTHORITY64-BITS=',authority_bit_checks, &
      ' MIRROR32-BITS=',mirror_bit_checks
  write(*,'(A,I0,A,I0)') 'B2I FOUR-LIST-DEEP-COPIES=',deep_copy_checks, &
      ' ROOT-HISTORY-EXCLUSIONS=',history_exclusions
  write(*,'(A,I0)') 'B2I PRODUCTION-B2C-PUBLISH-CALLS=',b2c_publish_calls
  write(*,'(A)') &
      'B2I REAL-XSM-INPUTS=3 DRAGON-EXECUTIONS=0 TRANSPORT-SOLVES=0'

contains

  subroutine BUILD_LIGHTWEIGHT_CANDIDATE(candidate)
    type(c_ptr), intent(out) :: candidate
    character(len=12) :: signature
    integer :: listdim, ip, history_project
    real(real32) :: history_l1
    real(real64) :: iter_keff, history_perp
    type(c_ptr) :: real_tracks, real_libraries, real_systems, real_fluxes
    type(c_ptr) :: out_tracks, out_libraries, out_systems, out_fluxes
    type(c_ptr) :: source_item, output_item

    call REQUIRE_CHARACTER(archive_base,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_RECORD(archive_base,'LISTDIM',1,1)
    call REQUIRE_RECORD(archive_base,'SPOT-ITER-K',1,4)
    call REQUIRE_RECORD(archive_base,'SPOT-L1-ERR',1,2)
    call REQUIRE_RECORD(archive_base,'SPOT-PJ-PERP',1,4)
    call REQUIRE_RECORD(archive_base,'SPOT-PROJECT',1,1)
    call LCMGET(archive_base,'LISTDIM',listdim)
    call LCMGET(archive_base,'SPOT-ITER-K',iter_keff)
    call LCMGET(archive_base,'SPOT-L1-ERR',history_l1)
    call LCMGET(archive_base,'SPOT-PJ-PERP',history_perp)
    call LCMGET(archive_base,'SPOT-PROJECT',history_project)
    if (listdim /= NSNAP) error stop 'real archive plane count differs'
    if (.not. ieee_is_finite(iter_keff) .or. &
        .not. ieee_is_finite(history_l1) .or. &
        .not. ieee_is_finite(history_perp)) &
      error stop 'real archive root diagnostic is nonfinite'

    real_tracks=LCMGID(archive_base,'TRACK')
    real_libraries=LCMGID(archive_base,'MICROLIB2')
    real_systems=LCMGID(archive_base,'SYSTEM')
    real_fluxes=LCMGID(archive_base,'FLUX')
    if (.not. c_associated(real_tracks) .or. &
        .not. c_associated(real_libraries) .or. &
        .not. c_associated(real_systems) .or. &
        .not. c_associated(real_fluxes)) &
      error stop 'real archive four-list lookup failed'

    call LCMOP(candidate,'B2I-BASE',0,1,0)
    if (.not. c_associated(candidate)) error stop 'candidate open failed'
    signature='L_ARCHIVE'
    call LCMPTC(candidate,'SIGNATURE',12,signature)
    call LCMPUT(candidate,'LISTDIM',1,1,listdim)
    call LCMPUT(candidate,'SPOT-ITER-K',1,4,iter_keff)
    call LCMPUT(candidate,'SPOT-L1-ERR',1,2,history_l1)
    call LCMPUT(candidate,'SPOT-PJ-PERP',1,4,history_perp)
    call LCMPUT(candidate,'SPOT-PROJECT',1,1,history_project)
    out_tracks=LCMLID(candidate,'TRACK',NSNAP)
    out_libraries=LCMLID(candidate,'MICROLIB2',NSNAP)
    out_systems=LCMLID(candidate,'SYSTEM',NSNAP)
    out_fluxes=LCMLID(candidate,'FLUX',NSNAP)
    if (.not. c_associated(out_tracks) .or. &
        .not. c_associated(out_libraries) .or. &
        .not. c_associated(out_systems) .or. &
        .not. c_associated(out_fluxes)) &
      error stop 'candidate four-list creation failed'

    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(real_tracks,ip)
      call REQUIRE_DIRECTORY_ITEM(real_libraries,ip)
      call REQUIRE_DIRECTORY_ITEM(real_systems,ip)
      call REQUIRE_DIRECTORY_ITEM(real_fluxes,ip)

      source_item=LCMGIL(real_tracks,ip)
      output_item=LCMDIL(out_tracks,ip)
      call REQUIRE_ASSOCIATED(output_item,'candidate TRACK item')
      call LCMEQU(source_item,output_item)
      call ADD_DEEP_SENTINEL(output_item,1000+ip)

      source_item=LCMGIL(real_libraries,ip)
      output_item=LCMDIL(out_libraries,ip)
      call REQUIRE_ASSOCIATED(output_item,'candidate MICROLIB2 item')
      call BUILD_MINIMAL_LIBRARY(source_item,output_item,2000+ip)

      source_item=LCMGIL(real_systems,ip)
      output_item=LCMDIL(out_systems,ip)
      call REQUIRE_ASSOCIATED(output_item,'candidate SYSTEM item')
      call BUILD_MINIMAL_SYSTEM(source_item,output_item,3000+ip)

      source_item=LCMGIL(real_fluxes,ip)
      output_item=LCMDIL(out_fluxes,ip)
      call REQUIRE_ASSOCIATED(output_item,'candidate FLUX item')
      call PUBLISH_B2C_CANDIDATE(source_item,output_item)
      call ADD_DEEP_SENTINEL(output_item,4000+ip)
    end do
  end subroutine BUILD_LIGHTWEIGHT_CANDIDATE


  subroutine BUILD_MINIMAL_LIBRARY(source,target,sentinel)
    type(c_ptr), intent(in) :: source, target
    integer, intent(in) :: sentinel
    character(len=12) :: signature
    integer :: state(NSTATE), macro_state(NSTATE), ig
    type(c_ptr) :: source_macro, target_macro, target_groups, group_item

    call REQUIRE_CHARACTER(source,'SIGNATURE',12,'L_LIBRARY')
    call REQUIRE_RECORD(source,'STATE-VECTOR',NSTATE,1)
    call LCMGTC(source,'SIGNATURE',12,signature)
    call LCMGET(source,'STATE-VECTOR',state)
    source_macro=LCMGID(source,'MACROLIB')
    call REQUIRE_ASSOCIATED(source_macro,'real MACROLIB')
    call REQUIRE_CHARACTER(source_macro,'SIGNATURE',12,'L_MACROLIB')
    call REQUIRE_RECORD(source_macro,'STATE-VECTOR',NSTATE,1)
    call LCMGET(source_macro,'STATE-VECTOR',macro_state)

    call LCMPTC(target,'SIGNATURE',12,signature)
    call LCMPUT(target,'STATE-VECTOR',NSTATE,1,state)
    target_macro=LCMDID(target,'MACROLIB')
    call REQUIRE_ASSOCIATED(target_macro,'minimal MACROLIB')
    signature='L_MACROLIB'
    call LCMPTC(target_macro,'SIGNATURE',12,signature)
    call LCMPUT(target_macro,'STATE-VECTOR',NSTATE,1,macro_state)
    target_groups=LCMLID(target_macro,'GROUP',NGRP)
    call REQUIRE_ASSOCIATED(target_groups,'minimal MACROLIB GROUP')
    do ig=1,NGRP
      group_item=LCMDIL(target_groups,ig)
      call REQUIRE_ASSOCIATED(group_item,'minimal MACROLIB group item')
    end do
    call ADD_DEEP_SENTINEL(target,sentinel)
  end subroutine BUILD_MINIMAL_LIBRARY


  subroutine BUILD_MINIMAL_SYSTEM(source,target,sentinel)
    type(c_ptr), intent(in) :: source, target
    integer, intent(in) :: sentinel
    character(len=12) :: signature, link_macro, link_track
    integer :: state(NSTATE), ig, snapshot
    real(real32) :: leakage(NGRP)
    type(c_ptr) :: target_groups, group_item

    call REQUIRE_CHARACTER(source,'SIGNATURE',12,'L_PIJ')
    call REQUIRE_RECORD(source,'STATE-VECTOR',NSTATE,1)
    call REQUIRE_CHARACTER(source,'LINK.MACRO',12,'MACRO0')
    call REQUIRE_CHARACTER(source,'LINK.TRACK',12,'TRACK')
    call REQUIRE_RECORD(source,'SPOT-LEAK1D',NGRP,2)
    call REQUIRE_RECORD(source,'SPOT-L1-SNAP',1,1)
    call LCMGTC(source,'SIGNATURE',12,signature)
    call LCMGTC(source,'LINK.MACRO',12,link_macro)
    call LCMGTC(source,'LINK.TRACK',12,link_track)
    call LCMGET(source,'STATE-VECTOR',state)
    call LCMGET(source,'SPOT-LEAK1D',leakage)
    call LCMGET(source,'SPOT-L1-SNAP',snapshot)
    if (snapshot /= sentinel-3000) &
      error stop 'real SYSTEM plane identity differs'
    if (.not. all(ieee_is_finite(leakage))) &
      error stop 'real SYSTEM leakage is nonfinite'

    call LCMPTC(target,'SIGNATURE',12,signature)
    call LCMPUT(target,'STATE-VECTOR',NSTATE,1,state)
    call LCMPTC(target,'LINK.MACRO',12,link_macro)
    call LCMPTC(target,'LINK.TRACK',12,link_track)
    call LCMPUT(target,'SPOT-LEAK1D',NGRP,2,leakage)
    call LCMPUT(target,'SPOT-L1-SNAP',1,1,snapshot)
    target_groups=LCMLID(target,'GROUP',NGRP)
    call REQUIRE_ASSOCIATED(target_groups,'minimal SYSTEM GROUP')
    do ig=1,NGRP
      group_item=LCMDIL(target_groups,ig)
      call REQUIRE_ASSOCIATED(group_item,'minimal SYSTEM group item')
    end do
    call ADD_DEEP_SENTINEL(target,sentinel)
  end subroutine BUILD_MINIMAL_SYSTEM


  subroutine ADD_DEEP_SENTINEL(root,sentinel)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: sentinel
    type(c_ptr) :: deep

    call LCMPUT(root,'B2I-SENT',1,1,sentinel)
    deep=LCMDID(root,'B2I-DEEP')
    call REQUIRE_ASSOCIATED(deep,'deep-copy sentinel directory')
    call LCMPUT(deep,'VALUE',1,1,sentinel)
  end subroutine ADD_DEEP_SENTINEL


  subroutine PUBLISH_B2C_CANDIDATE(history,target)
    type(c_ptr), intent(in) :: history, target
    character(len=4), parameter :: option='B0  '
    character(len=12), parameter :: macro_name='MACRO0'
    character(len=12), parameter :: track_name='TRACK'
    character(len=12), parameter :: system_name='SYSTEM'
    character(len=12) :: published_name
    integer :: ig, iu, length, record_type, status
    integer :: keyflx(NREG), imerge(NMAT_LOCAL)
    integer(int32) :: original_bits, mirror_bits
    real(real32) :: flux32(NUNKNO), source32(NUNKNO)
    real(real32) :: leakage32(NGRP), eps32
    real(real64) :: flux64(NUNKNO,NGRP), source64(NUNKNO,NGRP)
    type(c_ptr) :: history_flux, history_source, authority, published

    call REQUIRE_ASSOCIATED(target,'candidate FLUX list item')
    call REQUIRE_RECORD(history,'FLUX',NGRP,10)
    call REQUIRE_RECORD(history,'SOUR',NGRP,10)
    call REQUIRE_RECORD(history,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(history,'IMERGE-LEAK',NMAT_LOCAL,1)
    call REQUIRE_RECORD(history,'SPOT-LEAK1D',NGRP,2)
    history_flux=LCMGID(history,'FLUX')
    history_source=LCMGID(history,'SOUR')
    call REQUIRE_ASSOCIATED(history_flux,'historical root FLUX')
    call REQUIRE_ASSOCIATED(history_source,'historical root SOUR')
    call LCMGET(history,'KEYFLX',keyflx)
    call LCMGET(history,'IMERGE-LEAK',imerge)
    call LCMGET(history,'SPOT-LEAK1D',leakage32)
    if (any(imerge /= 1)) error stop 'historical merge map differs'
    if (.not. all(ieee_is_finite(leakage32))) &
      error stop 'historical leakage is nonfinite'

    do ig=1,NGRP
      call LCMLEL(history_flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 2) &
        error stop 'historical FLUX list schema differs'
      call LCMLEL(history_source,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 2) &
        error stop 'historical SOUR list schema differs'
      call LCMGDL(history_flux,ig,flux32)
      call LCMGDL(history_source,ig,source32)
      if (.not. all(ieee_is_finite(flux32)) .or. &
          .not. all(ieee_is_finite(source32))) &
        error stop 'historical terminal payload is nonfinite'
      flux64(:,ig)=real(flux32,real64)
      source64(:,ig)=real(source32,real64)
      do iu=1,NUNKNO
        if (flux64(iu,ig) < 0.0_real64) then
          flux64(iu,ig)=flux64(iu,ig)-spacing(flux64(iu,ig))
        else
          flux64(iu,ig)=flux64(iu,ig)+spacing(flux64(iu,ig))
        end if
        if (source64(iu,ig) < 0.0_real64) then
          source64(iu,ig)=source64(iu,ig)-spacing(source64(iu,ig))
        else
          source64(iu,ig)=source64(iu,ig)+spacing(source64(iu,ig))
        end if
        original_bits=transfer(flux32(iu),0_int32)
        mirror_bits=transfer(real(flux64(iu,ig),real32),0_int32)
        if (mirror_bits /= original_bits) &
          error stop 'FLUX REAL64 witness changes its REAL32 mirror'
        original_bits=transfer(source32(iu),0_int32)
        mirror_bits=transfer(real(source64(iu,ig),real32),0_int32)
        if (mirror_bits /= original_bits) &
          error stop 'SOUR REAL64 witness changes its REAL32 mirror'
      end do
    end do
    eps32=transfer(B2C_TOL_BITS,0.0_real32)
    write(published_name,'("B2I-B2C",I2.2)') b2c_publish_calls+1
    call LCMOP(published,published_name,0,1,0)
    call REQUIRE_EMPTY_ROOT(published)
    b2c_publish_calls=b2c_publish_calls+1
    call SPOR64_B2C_PUBLISH(published,4,flux64,source64,keyflx,1,imerge, &
        leakage32,eps32,eps32,eps32,option,macro_name,track_name, &
        system_name,status)
    if (status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'production B2C publisher rejected real payload'
    call LCMEQU(published,target)
    call LCMCL(published,2)
    authority=LCMGID(target,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'published candidate authority')
    call REQUIRE_INPUT_AUTHORITY_INVENTORY(authority)
  end subroutine PUBLISH_B2C_CANDIDATE


  subroutine RUN_POSITIVE()
    integer :: status
    type(c_ptr) :: axial_output, archive_output

    call LCMOP(axial_output,'B2I-AX-P',0,1,0)
    call LCMOP(archive_output,'B2I-AR-P',0,1,0)
    call REQUIRE_EMPTY_ROOT(axial_output)
    call REQUIRE_EMPTY_ROOT(archive_output)
    seal_calls=seal_calls+1
    call SPOR64_B2I_SEAL_BOOTSTRAP(axial_output,archive_output, &
        axial_base,axial_track_base,candidate_base,status)
    if (status /= SPOR64_B2I_BOOTSTRAP_COMMITTED) &
      error stop 'valid bootstrap candidate did not commit'
    call VERIFY_AXIAL_OUTPUT(axial_output)
    call VERIFY_ARCHIVE_OUTPUT(archive_output)
    call VERIFY_UNSEALED_INPUT(axial_base,candidate_base)
    call LCMCL(archive_output,2)
    call LCMCL(axial_output,2)
  end subroutine RUN_POSITIVE


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    character(len=12) :: axial_name, archive_name
    character(len=12) :: axial_output_name, archive_output_name
    integer :: status, marker
    logical :: owns_axial, owns_archive
    type(c_ptr) :: axial_input, archive_input
    type(c_ptr) :: axial_output, archive_output

    axial_input=axial_base
    archive_input=candidate_base
    owns_axial=.false.
    owns_archive=.false.
    write(axial_name,'("B2I-X",I2.2)') case_id
    write(archive_name,'("B2I-C",I2.2)') case_id
    write(axial_output_name,'("B2I-AO",I2.2)') case_id
    write(archive_output_name,'("B2I-RO",I2.2)') case_id

    select case(case_id)
    case(1)
      call CLONE_OBJECT(axial_base,axial_name,axial_input)
      owns_axial=.true.
      call PERTURB_REAL64_RECORD(axial_input,'SPOT-X-RHO')
    case(2)
      call CLONE_OBJECT(axial_base,axial_name,axial_input)
      owns_axial=.true.
      call PERTURB_REAL64_RECORD(axial_input,'SPOT-X-GRAM')
    case(3)
      call CLONE_OBJECT(axial_base,axial_name,axial_input)
      owns_axial=.true.
      call PERTURB_REAL64_RECORD(axial_input,'SPOT-X-H')
    case(4:11)
      call CLONE_OBJECT(candidate_base,archive_name,archive_input)
      owns_archive=.true.
      call MUTATE_ARCHIVE_REJECTION(archive_input,case_id)
    case(12)
      continue
    case default
      error stop 'unknown B2i rejection case'
    end select

    call LCMOP(axial_output,axial_output_name,0,1,0)
    call LCMOP(archive_output,archive_output_name,0,1,0)
    call REQUIRE_EMPTY_ROOT(axial_output)
    call REQUIRE_EMPTY_ROOT(archive_output)
    if (case_id == 12) then
      marker=271828
      call LCMPUT(axial_output,'SENTINEL',1,1,marker)
    end if

    seal_calls=seal_calls+1
    call SPOR64_B2I_SEAL_BOOTSTRAP(axial_output,archive_output, &
        axial_input,axial_track_base,archive_input,status)
    if (status /= SPOR64_B2I_ADMISSION_FAILED) &
      error stop 'invalid bootstrap candidate was accepted'
    if (case_id == 12) then
      call REQUIRE_ONLY_SENTINEL(axial_output,271828)
      call REQUIRE_EMPTY_ROOT(archive_output)
    else
      call REQUIRE_EMPTY_ROOT(axial_output)
      call REQUIRE_EMPTY_ROOT(archive_output)
    end if
    call VERIFY_UNSEALED_INPUT(axial_input,archive_input)
    rejection_count=rejection_count+1

    call LCMCL(archive_output,2)
    call LCMCL(axial_output,2)
    if (owns_archive) call LCMCL(archive_input,2)
    if (owns_axial) call LCMCL(axial_input,2)
  end subroutine RUN_REJECTION


  subroutine MUTATE_ARCHIVE_REJECTION(archive,case_id)
    type(c_ptr), intent(in) :: archive
    integer, intent(in) :: case_id
    integer :: marker, key(NREG)
    real(real32) :: values32(NUNKNO), leakage32(NGRP), volume32(NREG)
    real(real64) :: iter_keff, values64(NUNKNO)
    type(c_ptr) :: list, item, authority, payload

    select case(case_id)
    case(4)
      call LCMGET(archive,'SPOT-ITER-K',iter_keff)
      iter_keff=nearest(iter_keff,1.0_real64)
      call LCMPUT(archive,'SPOT-ITER-K',1,4,iter_keff)
    case(5)
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,1)
      call LCMGET(item,'SPOT-LEAK1D',leakage32)
      leakage32(1)=nearest(leakage32(1),1.0_real32)
      call LCMPUT(item,'SPOT-LEAK1D',NGRP,2,leakage32)
    case(6)
      list=LCMGID(archive,'TRACK')
      item=LCMGIL(list,2)
      call LCMGET(item,'VOLUME',volume32)
      volume32(1)=nearest(volume32(1),1.0_real32)
      call LCMPUT(item,'VOLUME',NREG,2,volume32)
    case(7)
      list=LCMGID(archive,'TRACK')
      item=LCMGIL(list,3)
      call LCMGET(item,'KEYFLX$ANIS',key)
      key(2)=key(1)
      call LCMPUT(item,'KEYFLX$ANIS',NREG,1,key)
    case(8)
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,1)
      payload=LCMGID(item,'SOUR')
      call LCMGDL(payload,1,values32)
      values32(1)=nearest(values32(1),1.0_real32)
      call LCMPDL(payload,1,NUNKNO,2,values32)
    case(9)
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,2)
      authority=LCMGID(item,'SPOT-R64')
      payload=LCMGID(authority,'SOUR')
      call LCMGDL(payload,1,values64)
      values64(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPDL(payload,1,NUNKNO,4,values64)
    case(10)
      list=LCMGID(archive,'FLUX')
      item=LCMGIL(list,3)
      authority=LCMGID(item,'SPOT-R64')
      marker=314159
      call LCMPUT(authority,'EXTRA',1,1,marker)
    case(11)
      call LCMDEL(archive,'SYSTEM')
    case default
      error stop 'unknown archive mutation case'
    end select
  end subroutine MUTATE_ARCHIVE_REJECTION


  subroutine PERTURB_REAL64_RECORD(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type
    real(real64), allocatable :: values(:)

    call LCMLEN(root,name,length,record_type)
    if (length < 1 .or. record_type /= 4) &
      error stop 'REAL64 mutation target schema differs'
    allocate(values(length))
    call LCMGET(root,name,values)
    values(1)=nearest(values(1),1.0_real64)
    call LCMPUT(root,name,length,4,values)
    deallocate(values)
  end subroutine PERTURB_REAL64_RECORD


  subroutine VERIFY_UNSEALED_INPUT(axial,archive)
    type(c_ptr), intent(in) :: axial, archive
    integer :: ip
    type(c_ptr) :: fluxes, plane, authority

    call REQUIRE_ABSENT(axial,'SPOT-X-STATE')
    call REQUIRE_ABSENT(axial,'SPOT-X-EPOCH')
    call REQUIRE_ABSENT(archive,'SPOT-R64')
    call REQUIRE_RECORD(archive,'FLUX',NSNAP,10)
    fluxes=LCMGID(archive,'FLUX')
    do ip=1,NSNAP
      call REQUIRE_DIRECTORY_ITEM(fluxes,ip)
      plane=LCMGIL(fluxes,ip)
      call REQUIRE_RECORD(plane,'SPOT-R64',-1,0)
      authority=LCMGID(plane,'SPOT-R64')
      call REQUIRE_ABSENT(authority,'RHO')
      call REQUIRE_ABSENT(authority,'STATE')
      call REQUIRE_ABSENT(authority,'EPOCH')
      call REQUIRE_ABSENT(authority,'QFISS')
    end do
  end subroutine VERIFY_UNSEALED_INPUT


  subroutine VERIFY_AXIAL_OUTPUT(output)
    type(c_ptr), intent(in) :: output
    integer :: epoch

    if (c_associated(output,axial_base)) &
      error stop 'fresh axial output aliases its input'
    call COMPARE_AXIAL_CANONICAL(axial_base,output)
    call REQUIRE_CHARACTER(output,'SPOT-X-STATE',12,'CLOSED')
    call REQUIRE_RECORD(output,'SPOT-X-EPOCH',1,1)
    call LCMGET(output,'SPOT-X-EPOCH',epoch)
    if (epoch /= 0) error stop 'fresh axial epoch differs'
  end subroutine VERIFY_AXIAL_OUTPUT


  subroutine COMPARE_AXIAL_CANONICAL(input,output)
    type(c_ptr), intent(in) :: input, output

    call COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call COMPARE_CHARACTER_RECORD(input,output,'SPOT-X-NID',12)
    call COMPARE_CHARACTER_RECORD(input,output,'SPOT-X-BTYP',12)
    call COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-DIMS')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-FIXB')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-RANK')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-OFF')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-GOFF')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-X-BOFF')
    call COMPARE_REAL32_RECORD(input,output,'SPOT-X-BASIS')
    call COMPARE_REAL32_RECORD(input,output,'K-EFFECTIVE')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-A')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-GRAM')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-RHO')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-L')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-H')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-NORM')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-PERP')
    call COMPARE_REAL64_RECORD(input,output,'SPOT-X-GERR')
  end subroutine COMPARE_AXIAL_CANONICAL


  subroutine VERIFY_ARCHIVE_OUTPUT(output)
    type(c_ptr), intent(in) :: output
    integer :: listdim, epoch, nplane, ip
    real(real64) :: input_keff, output_keff, axial_rho, output_rho
    type(c_ptr) :: input_tracks, input_libraries, input_systems
    type(c_ptr) :: input_fluxes, output_tracks, output_libraries
    type(c_ptr) :: output_systems, output_fluxes, authority
    type(c_ptr) :: input_item, output_item

    if (c_associated(output,candidate_base)) &
      error stop 'fresh archive output aliases its input'
    call REQUIRE_OUTPUT_ARCHIVE_INVENTORY(output)
    call REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_ARCHIVE')
    call REQUIRE_RECORD(output,'LISTDIM',1,1)
    call LCMGET(output,'LISTDIM',listdim)
    if (listdim /= NSNAP) error stop 'fresh archive plane count differs'
    call LCMGET(candidate_base,'SPOT-ITER-K',input_keff)
    call LCMGET(output,'SPOT-ITER-K',output_keff)
    if (BITS64(input_keff) /= BITS64(output_keff)) &
      error stop 'fresh archive K bits differ'

    call REQUIRE_ABSENT(output,'SPOT-L1-ERR')
    history_exclusions=history_exclusions+1
    call REQUIRE_ABSENT(output,'SPOT-PJ-PERP')
    history_exclusions=history_exclusions+1
    call REQUIRE_ABSENT(output,'SPOT-PROJECT')
    history_exclusions=history_exclusions+1

    authority=LCMGID(output,'SPOT-R64')
    call REQUIRE_ASSOCIATED(authority,'fresh archive authority')
    call REQUIRE_ROOT_AUTHORITY_INVENTORY(authority)
    call REQUIRE_CHARACTER(authority,'STATE',12,'CLOSED')
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call REQUIRE_RECORD(authority,'NPLANE',1,1)
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call LCMGET(authority,'EPOCH',epoch)
    call LCMGET(authority,'NPLANE',nplane)
    call LCMGET(authority,'RHO',output_rho)
    call LCMGET(axial_base,'SPOT-X-RHO',axial_rho)
    if (epoch /= 0 .or. nplane /= NSNAP) &
      error stop 'fresh archive root lifecycle differs'
    if (BITS64(output_rho) /= BITS64(axial_rho)) &
      error stop 'fresh archive root RHO bits differ'

    input_tracks=LCMGID(candidate_base,'TRACK')
    input_libraries=LCMGID(candidate_base,'MICROLIB2')
    input_systems=LCMGID(candidate_base,'SYSTEM')
    input_fluxes=LCMGID(candidate_base,'FLUX')
    output_tracks=LCMGID(output,'TRACK')
    output_libraries=LCMGID(output,'MICROLIB2')
    output_systems=LCMGID(output,'SYSTEM')
    output_fluxes=LCMGID(output,'FLUX')
    call REQUIRE_ASSOCIATED(output_tracks,'fresh TRACK list')
    call REQUIRE_ASSOCIATED(output_libraries,'fresh MICROLIB2 list')
    call REQUIRE_ASSOCIATED(output_systems,'fresh SYSTEM list')
    call REQUIRE_ASSOCIATED(output_fluxes,'fresh FLUX list')

    do ip=1,NSNAP
      input_item=LCMGIL(input_tracks,ip)
      output_item=LCMGIL(output_tracks,ip)
      call VERIFY_TRACK_COPY(input_item,output_item,1000+ip)
      deep_copy_checks=deep_copy_checks+1

      input_item=LCMGIL(input_libraries,ip)
      output_item=LCMGIL(output_libraries,ip)
      call VERIFY_LIBRARY_COPY(input_item,output_item,2000+ip)
      deep_copy_checks=deep_copy_checks+1

      input_item=LCMGIL(input_systems,ip)
      output_item=LCMGIL(output_systems,ip)
      call VERIFY_SYSTEM_COPY(input_item,output_item,3000+ip)
      deep_copy_checks=deep_copy_checks+1

      input_item=LCMGIL(input_fluxes,ip)
      output_item=LCMGIL(output_fluxes,ip)
      call VERIFY_FLUX_COPY(input_item,output_item,4000+ip,axial_rho)
      deep_copy_checks=deep_copy_checks+1
    end do
  end subroutine VERIFY_ARCHIVE_OUTPUT


  subroutine VERIFY_TRACK_COPY(input,output,sentinel)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel

    call REQUIRE_DISTINCT(input,output,'TRACK item')
    call COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call COMPARE_CHARACTER_RECORD(input,output,'TRACK-TYPE',12)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.FTRACK',12)
    call COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call COMPARE_INTEGER_RECORD(input,output,'KEYFLX')
    call COMPARE_INTEGER_RECORD(input,output,'KEYFLX$ANIS')
    call COMPARE_REAL32_RECORD(input,output,'VOLUME')
    call VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_TRACK_COPY


  subroutine VERIFY_LIBRARY_COPY(input,output,sentinel)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel
    integer :: ig
    type(c_ptr) :: input_macro, output_macro
    type(c_ptr) :: input_groups, output_groups

    call REQUIRE_DISTINCT(input,output,'MICROLIB2 item')
    call COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    input_macro=LCMGID(input,'MACROLIB')
    output_macro=LCMGID(output,'MACROLIB')
    call REQUIRE_DISTINCT(input_macro,output_macro,'MACROLIB directory')
    call COMPARE_CHARACTER_RECORD(input_macro,output_macro,'SIGNATURE',12)
    call COMPARE_INTEGER_RECORD(input_macro,output_macro,'STATE-VECTOR')
    call REQUIRE_RECORD(input_macro,'GROUP',NGRP,10)
    call REQUIRE_RECORD(output_macro,'GROUP',NGRP,10)
    input_groups=LCMGID(input_macro,'GROUP')
    output_groups=LCMGID(output_macro,'GROUP')
    call REQUIRE_DISTINCT(input_groups,output_groups,'MACROLIB GROUP list')
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(input_groups,ig)
      call REQUIRE_DIRECTORY_ITEM(output_groups,ig)
    end do
    call VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_LIBRARY_COPY


  subroutine VERIFY_SYSTEM_COPY(input,output,sentinel)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel
    integer :: ig
    type(c_ptr) :: input_groups, output_groups

    call REQUIRE_DISTINCT(input,output,'SYSTEM item')
    call COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.MACRO',12)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.TRACK',12)
    call COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call COMPARE_INTEGER_RECORD(input,output,'SPOT-L1-SNAP')
    call COMPARE_REAL32_RECORD(input,output,'SPOT-LEAK1D')
    call REQUIRE_RECORD(input,'GROUP',NGRP,10)
    call REQUIRE_RECORD(output,'GROUP',NGRP,10)
    input_groups=LCMGID(input,'GROUP')
    output_groups=LCMGID(output,'GROUP')
    call REQUIRE_DISTINCT(input_groups,output_groups,'SYSTEM GROUP list')
    do ig=1,NGRP
      call REQUIRE_DIRECTORY_ITEM(input_groups,ig)
      call REQUIRE_DIRECTORY_ITEM(output_groups,ig)
    end do
    call VERIFY_DEEP_SENTINEL(input,output,sentinel)
  end subroutine VERIFY_SYSTEM_COPY


  subroutine VERIFY_FLUX_COPY(input,output,sentinel,expected_rho)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: sentinel
    real(real64), intent(in) :: expected_rho
    character(len=12) :: state
    integer :: epoch, ig, iu, length, record_type
    integer(int64) :: promoted_bits
    real(real32) :: output_flux32(NUNKNO), output_source32(NUNKNO)
    real(real64) :: input_flux64(NUNKNO), input_source64(NUNKNO)
    real(real64) :: output_flux64(NUNKNO), output_source64(NUNKNO), rho
    type(c_ptr) :: input_authority, output_authority
    type(c_ptr) :: input_authority_flux, input_authority_source
    type(c_ptr) :: output_authority_flux, output_authority_source
    type(c_ptr) :: output_root_flux, output_root_source

    call REQUIRE_DISTINCT(input,output,'FLUX item')
    call COMPARE_CHARACTER_RECORD(input,output,'SIGNATURE',12)
    call COMPARE_CHARACTER_RECORD(input,output,'OPTION',4)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.MACRO',12)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.TRACK',12)
    call COMPARE_CHARACTER_RECORD(input,output,'LINK.SYSTEM',12)
    call COMPARE_INTEGER_RECORD(input,output,'STATE-VECTOR')
    call COMPARE_INTEGER_RECORD(input,output,'IMERGE-LEAK')
    call COMPARE_INTEGER_RECORD(input,output,'KEYFLX')
    call COMPARE_REAL32_RECORD(input,output,'EPS-CONVERGE')
    call COMPARE_REAL32_RECORD(input,output,'SPOT-LEAK1D')
    call VERIFY_DEEP_SENTINEL(input,output,sentinel)

    input_authority=LCMGID(input,'SPOT-R64')
    output_authority=LCMGID(output,'SPOT-R64')
    call REQUIRE_ASSOCIATED(input_authority,'input plane authority')
    call REQUIRE_DISTINCT(input_authority,output_authority, &
        'output plane authority')
    call REQUIRE_INPUT_AUTHORITY_INVENTORY(input_authority)
    call REQUIRE_OUTPUT_PLANE_AUTHORITY_INVENTORY(output_authority)
    call REQUIRE_CHARACTER(output_authority,'STATE',12,'SOLVED')
    call LCMGTC(output_authority,'STATE',12,state)
    if (state /= 'SOLVED') error stop 'output plane state differs'
    call LCMGET(output_authority,'EPOCH',epoch)
    call LCMGET(output_authority,'RHO',rho)
    if (epoch /= 0) error stop 'output plane epoch differs'
    if (BITS64(rho) /= BITS64(expected_rho)) &
      error stop 'output plane RHO bits differ'
    call REQUIRE_ABSENT(output_authority,'QFISS')

    input_authority_flux=LCMGID(input_authority,'FLUX')
    input_authority_source=LCMGID(input_authority,'SOUR')
    output_authority_flux=LCMGID(output_authority,'FLUX')
    output_authority_source=LCMGID(output_authority,'SOUR')
    output_root_flux=LCMGID(output,'FLUX')
    output_root_source=LCMGID(output,'SOUR')
    call REQUIRE_ASSOCIATED(output_authority_flux,'output authority FLUX')
    call REQUIRE_ASSOCIATED(output_authority_source,'output authority SOUR')
    call REQUIRE_ASSOCIATED(output_root_flux,'output root FLUX')
    call REQUIRE_ASSOCIATED(output_root_source,'output root SOUR')

    do ig=1,NGRP
      call LCMLEL(output_authority_flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'output authority FLUX schema differs'
      call LCMLEL(output_authority_source,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'output authority SOUR schema differs'
      call LCMLEL(output_root_flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 2) &
        error stop 'output root FLUX schema differs'
      call LCMLEL(output_root_source,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 2) &
        error stop 'output root SOUR schema differs'
      call LCMGDL(input_authority_flux,ig,input_flux64)
      call LCMGDL(input_authority_source,ig,input_source64)
      call LCMGDL(output_authority_flux,ig,output_flux64)
      call LCMGDL(output_authority_source,ig,output_source64)
      call LCMGDL(output_root_flux,ig,output_flux32)
      call LCMGDL(output_root_source,ig,output_source32)
      do iu=1,NUNKNO
        if (BITS64(output_flux64(iu)) /= BITS64(input_flux64(iu))) &
          error stop 'output authority FLUX bits differ'
        authority_bit_checks=authority_bit_checks+1
        if (BITS64(output_source64(iu)) /= BITS64(input_source64(iu))) &
          error stop 'output authority SOUR bits differ'
        authority_bit_checks=authority_bit_checks+1

        promoted_bits=BITS64(real(output_flux32(iu),real64))
        if (BITS64(output_flux64(iu)) == promoted_bits) &
          error stop 'output authority FLUX lacks REAL64-only witness'
        if (BITS32(output_flux32(iu)) /= &
            BITS32(real(output_flux64(iu),real32))) &
          error stop 'output root FLUX is not the exact authority downcast'
        mirror_bit_checks=mirror_bit_checks+1

        promoted_bits=BITS64(real(output_source32(iu),real64))
        if (BITS64(output_source64(iu)) == promoted_bits) &
          error stop 'output authority SOUR lacks REAL64-only witness'
        if (BITS32(output_source32(iu)) /= &
            BITS32(real(output_source64(iu),real32))) &
          error stop 'output root SOUR is not the exact authority downcast'
        mirror_bit_checks=mirror_bit_checks+1
      end do
    end do
  end subroutine VERIFY_FLUX_COPY


  subroutine VERIFY_DEEP_SENTINEL(input,output,expected)
    type(c_ptr), intent(in) :: input, output
    integer, intent(in) :: expected
    integer :: input_root, output_root, input_deep, output_deep
    type(c_ptr) :: input_directory, output_directory

    call REQUIRE_RECORD(input,'B2I-SENT',1,1)
    call REQUIRE_RECORD(output,'B2I-SENT',1,1)
    call LCMGET(input,'B2I-SENT',input_root)
    call LCMGET(output,'B2I-SENT',output_root)
    if (input_root /= expected .or. output_root /= expected) &
      error stop 'deep-copy root sentinel differs'
    input_directory=LCMGID(input,'B2I-DEEP')
    output_directory=LCMGID(output,'B2I-DEEP')
    call REQUIRE_DISTINCT(input_directory,output_directory, &
        'deep-copy sentinel directory')
    call REQUIRE_RECORD(input_directory,'VALUE',1,1)
    call REQUIRE_RECORD(output_directory,'VALUE',1,1)
    call LCMGET(input_directory,'VALUE',input_deep)
    call LCMGET(output_directory,'VALUE',output_deep)
    if (input_deep /= expected .or. output_deep /= expected) &
      error stop 'deep-copy nested sentinel differs'
  end subroutine VERIFY_DEEP_SENTINEL


  subroutine COMPARE_CHARACTER_RECORD(input,output,name,character_count)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer, intent(in) :: character_count
    character(len=:), allocatable :: input_value, output_value
    integer :: word_count

    word_count=(character_count+3)/4
    call REQUIRE_RECORD(input,name,word_count,3)
    call REQUIRE_RECORD(output,name,word_count,3)
    allocate(character(len=character_count) :: input_value,output_value)
    input_value(:)=' '
    output_value(:)=' '
    call LCMGTC(input,name,character_count,input_value)
    call LCMGTC(output,name,character_count,output_value)
    if (input_value /= output_value) &
      error stop 'copied character record differs'
    deallocate(input_value,output_value)
  end subroutine COMPARE_CHARACTER_RECORD


  subroutine COMPARE_INTEGER_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: input_length, input_type, output_length, output_type
    integer, allocatable :: input_value(:), output_value(:)

    call LCMLEN(input,name,input_length,input_type)
    call LCMLEN(output,name,output_length,output_type)
    if (input_length < 1 .or. input_type /= 1 .or. &
        output_length /= input_length .or. output_type /= input_type) &
      error stop 'copied integer record schema differs'
    allocate(input_value(input_length),output_value(input_length))
    call LCMGET(input,name,input_value)
    call LCMGET(output,name,output_value)
    if (any(input_value /= output_value)) &
      error stop 'copied integer record differs'
    deallocate(input_value,output_value)
  end subroutine COMPARE_INTEGER_RECORD


  subroutine COMPARE_REAL32_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: input_length, input_type, output_length, output_type
    real(real32), allocatable :: input_value(:), output_value(:)

    call LCMLEN(input,name,input_length,input_type)
    call LCMLEN(output,name,output_length,output_type)
    if (input_length < 1 .or. input_type /= 2 .or. &
        output_length /= input_length .or. output_type /= input_type) &
      error stop 'copied REAL32 record schema differs'
    allocate(input_value(input_length),output_value(input_length))
    call LCMGET(input,name,input_value)
    call LCMGET(output,name,output_value)
    if (any(BITS32(input_value) /= BITS32(output_value))) &
      error stop 'copied REAL32 record bits differ'
    deallocate(input_value,output_value)
  end subroutine COMPARE_REAL32_RECORD


  subroutine COMPARE_REAL64_RECORD(input,output,name)
    type(c_ptr), intent(in) :: input, output
    character(len=*), intent(in) :: name
    integer :: input_length, input_type, output_length, output_type
    real(real64), allocatable :: input_value(:), output_value(:)

    call LCMLEN(input,name,input_length,input_type)
    call LCMLEN(output,name,output_length,output_type)
    if (input_length < 1 .or. input_type /= 4 .or. &
        output_length /= input_length .or. output_type /= input_type) &
      error stop 'copied REAL64 record schema differs'
    allocate(input_value(input_length),output_value(input_length))
    call LCMGET(input,name,input_value)
    call LCMGET(output,name,output_value)
    if (any(BITS64(input_value) /= BITS64(output_value))) &
      error stop 'copied REAL64 record bits differ'
    deallocate(input_value,output_value)
  end subroutine COMPARE_REAL64_RECORD


  subroutine REQUIRE_OUTPUT_ARCHIVE_INVENTORY(root)
    type(c_ptr), intent(in) :: root
    character(len=12) :: first_name, item_name
    logical :: signature, listdim, iter_k, tracks, libraries
    logical :: systems, fluxes, authority
    integer :: count

    signature=.false.
    listdim=.false.
    iter_k=.false.
    tracks=.false.
    libraries=.false.
    systems=.false.
    fluxes=.false.
    authority=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'empty output archive'
    first_name=item_name
    count=0
    do
      count=count+1
      select case(item_name)
      case('SIGNATURE')
        if (signature) error stop 'duplicate archive signature'
        signature=.true.
      case('LISTDIM')
        if (listdim) error stop 'duplicate archive plane count'
        listdim=.true.
      case('SPOT-ITER-K')
        if (iter_k) error stop 'duplicate archive K'
        iter_k=.true.
      case('TRACK')
        if (tracks) error stop 'duplicate archive TRACK list'
        tracks=.true.
      case('MICROLIB2')
        if (libraries) error stop 'duplicate archive MICROLIB2 list'
        libraries=.true.
      case('SYSTEM')
        if (systems) error stop 'duplicate archive SYSTEM list'
        systems=.true.
      case('FLUX')
        if (fluxes) error stop 'duplicate archive FLUX list'
        fluxes=.true.
      case('SPOT-R64')
        if (authority) error stop 'duplicate archive authority'
        authority=.true.
      case default
        error stop 'unexpected fresh archive root record'
      end select
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 8 .or. .not. signature .or. .not. listdim .or. &
        .not. iter_k .or. .not. tracks .or. .not. libraries .or. &
        .not. systems .or. .not. fluxes .or. .not. authority) &
      error stop 'fresh archive root inventory differs'
  end subroutine REQUIRE_OUTPUT_ARCHIVE_INVENTORY


  subroutine REQUIRE_INPUT_AUTHORITY_INVENTORY(root)
    type(c_ptr), intent(in) :: root
    character(len=12) :: first_name, item_name
    logical :: flux, source
    integer :: count

    flux=.false.
    source=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'empty input authority'
    first_name=item_name
    count=0
    do
      count=count+1
      select case(item_name)
      case('FLUX')
        if (flux) error stop 'duplicate input authority FLUX'
        flux=.true.
      case('SOUR')
        if (source) error stop 'duplicate input authority SOUR'
        source=.true.
      case default
        error stop 'unexpected input authority record'
      end select
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 2 .or. .not. flux .or. .not. source) &
      error stop 'input authority inventory differs'
  end subroutine REQUIRE_INPUT_AUTHORITY_INVENTORY


  subroutine REQUIRE_OUTPUT_PLANE_AUTHORITY_INVENTORY(root)
    type(c_ptr), intent(in) :: root
    character(len=12) :: first_name, item_name
    logical :: flux, source, rho, state, epoch
    integer :: count

    flux=.false.
    source=.false.
    rho=.false.
    state=.false.
    epoch=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'empty output plane authority'
    first_name=item_name
    count=0
    do
      count=count+1
      select case(item_name)
      case('FLUX')
        if (flux) error stop 'duplicate output authority FLUX'
        flux=.true.
      case('SOUR')
        if (source) error stop 'duplicate output authority SOUR'
        source=.true.
      case('RHO')
        if (rho) error stop 'duplicate output authority RHO'
        rho=.true.
      case('STATE')
        if (state) error stop 'duplicate output authority STATE'
        state=.true.
      case('EPOCH')
        if (epoch) error stop 'duplicate output authority EPOCH'
        epoch=.true.
      case default
        error stop 'unexpected output plane authority record'
      end select
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 5 .or. .not. flux .or. .not. source .or. &
        .not. rho .or. .not. state .or. .not. epoch) &
      error stop 'output plane authority inventory differs'
  end subroutine REQUIRE_OUTPUT_PLANE_AUTHORITY_INVENTORY


  subroutine REQUIRE_ROOT_AUTHORITY_INVENTORY(root)
    type(c_ptr), intent(in) :: root
    character(len=12) :: first_name, item_name
    logical :: rho, nplane, state, epoch
    integer :: count

    rho=.false.
    nplane=.false.
    state=.false.
    epoch=.false.
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name == ' ') error stop 'empty output root authority'
    first_name=item_name
    count=0
    do
      count=count+1
      select case(item_name)
      case('RHO')
        if (rho) error stop 'duplicate root authority RHO'
        rho=.true.
      case('NPLANE')
        if (nplane) error stop 'duplicate root authority NPLANE'
        nplane=.true.
      case('STATE')
        if (state) error stop 'duplicate root authority STATE'
        state=.true.
      case('EPOCH')
        if (epoch) error stop 'duplicate root authority EPOCH'
        epoch=.true.
      case default
        error stop 'unexpected root authority record'
      end select
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 4 .or. .not. rho .or. .not. nplane .or. &
        .not. state .or. .not. epoch) &
      error stop 'root authority inventory differs'
  end subroutine REQUIRE_ROOT_AUTHORITY_INVENTORY


  subroutine REQUIRE_CHARACTER(root,name,character_count,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: character_count
    character(len=:), allocatable :: found
    integer :: word_count

    word_count=(character_count+3)/4
    call REQUIRE_RECORD(root,name,word_count,3)
    allocate(character(len=character_count) :: found)
    found(:)=' '
    call LCMGTC(root,name,character_count,found)
    if (found /= expected) then
      write(*,'(A,1X,A,1X,A,1X,A)') 'CHARACTER-MISMATCH',trim(name), &
          trim(found),trim(expected)
      error stop 'character record differs'
    end if
    deallocate(found)
  end subroutine REQUIRE_CHARACTER


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
      error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      error stop 'unexpected record is present'
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_DIRECTORY_ITEM(list,index)
    type(c_ptr), intent(in) :: list
    integer, intent(in) :: index
    integer :: length, record_type

    call LCMLEL(list,index,length,record_type)
    if (length /= -1 .or. record_type /= 0) &
      error stop 'list item is not a directory'
  end subroutine REQUIRE_DIRECTORY_ITEM


  subroutine REQUIRE_ASSOCIATED(pointer,owner)
    type(c_ptr), intent(in) :: pointer
    character(len=*), intent(in) :: owner

    if (.not. c_associated(pointer)) then
      write(*,'(A,1X,A)') 'UNASSOCIATED',trim(owner)
      error stop 'required GANLIB pointer is unassociated'
    end if
  end subroutine REQUIRE_ASSOCIATED


  subroutine REQUIRE_DISTINCT(left,right,owner)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: owner

    call REQUIRE_ASSOCIATED(left,trim(owner)//' input')
    call REQUIRE_ASSOCIATED(right,trim(owner)//' output')
    if (c_associated(left,right)) then
      write(*,'(A,1X,A)') 'ALIASED',trim(owner)
      error stop 'deep-copy pointer aliases its input'
    end if
  end subroutine REQUIRE_DISTINCT


  subroutine REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'rejected output was mutated'
  end subroutine REQUIRE_EMPTY_ROOT


  subroutine REQUIRE_ONLY_SENTINEL(root,expected)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected
    character(len=12) :: first_name, item_name
    integer :: found, count

    call REQUIRE_RECORD(root,'SENTINEL',1,1)
    call LCMGET(root,'SENTINEL',found)
    if (found /= expected) error stop 'collision sentinel changed'
    item_name=' '
    call LCMNXT(root,item_name)
    if (item_name /= 'SENTINEL') &
      error stop 'collision output gained an unexpected record'
    first_name=item_name
    count=0
    do
      count=count+1
      call LCMNXT(root,item_name)
      if (item_name == first_name) exit
    end do
    if (count /= 1) error stop 'collision output gained a new record'
  end subroutine REQUIRE_ONLY_SENTINEL


  subroutine CLONE_OBJECT(source,name,target)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: target

    call LCMOP(target,name,0,1,0)
    call REQUIRE_ASSOCIATED(target,'clone target')
    call REQUIRE_EMPTY_ROOT(target)
    call LCMEQU(source,target)
  end subroutine CLONE_OBJECT


  elemental integer(int32) function BITS32(value)
    real(real32), intent(in) :: value

    BITS32=transfer(value,0_int32)
  end function BITS32


  elemental integer(int64) function BITS64(value)
    real(real64), intent(in) :: value

    BITS64=transfer(value,0_int64)
  end function BITS64

end program TEST_B2I_BOOTSTRAP_LIFECYCLE
