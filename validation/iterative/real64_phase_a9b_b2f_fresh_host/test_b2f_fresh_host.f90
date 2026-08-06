program TEST_B2F_FRESH_HOST
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_quiet_nan, ieee_value
  use B2F_STUB_PROBES
  use SPOR64_B2B, only : SPOR64_B2B_ADMISSION_FAILED, SPOR64_B2B_INGRESS
  use SPOR64_B2C, only : SPOR64_B2C_PREFLIGHT_FAILED, &
      SPOR64_B2C_HOST_COMMITTED, SPOR64_B2C_PUBLISH
  implicit none

  integer, parameter :: NENTRY=7, NSTATE=40, NGRP=370
  integer, parameter :: NREG=8, NMAT=8, NUNKNO=14
  character(len=12), parameter :: MACRO_NAME='MACRO0'
  character(len=12), parameter :: TRACK_NAME='TRACK'
  character(len=12), parameter :: SYSTEM_NAME='SYSTEM'
  character(len=12) :: hentry(NENTRY)
  character(len=1024) :: seed_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: ientry(NENTRY), jentry(NENTRY), imerg(NMAT)
  integer :: status, b2b_calls, publisher_calls
  integer(int64) :: cutoff_visit64
  real(real32) :: eps32
  type(c_ptr) :: seed, macro, track, system, source, output
  type(c_ptr) :: kentry(NENTRY)
  type(FIL_file), target :: fake_track

  if (command_argument_count() /= 5) &
    error stop 'expected FLUX_OLD MACRO0 TRACK SYSTEM FSOURCE paths'
  call get_command_argument(1,seed_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,system_path)
  call get_command_argument(5,source_path)

  call LCMOP(seed,trim(seed_path),2,2,0)
  call LCMOP(macro,trim(macro_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call LCMOP(system,trim(system_path),2,2,0)
  call LCMOP(source,trim(source_path),2,2,0)
  if (.not. all([c_associated(seed),c_associated(macro), &
      c_associated(track),c_associated(system),c_associated(source)])) &
    error stop 'read-only XSM open failed'

  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  hentry=[character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
      'SYSTEM','FSOURCE','FLUX_OLD']
  ientry=[1,2,2,3,2,2,2]
  jentry=[0,2,2,2,2,2,2]
  kentry=[c_null_ptr,macro,track,c_loc(fake_track),system,source,seed]
  imerg=1
  eps32=transfer(int(z'348637bd',int32),0.0_real32)
  b2b_calls=0
  publisher_calls=0
  call B2F_RESET_TOTALS()

  call LCMOP(output,'B2F-POSITIVE',0,1,0)
  kentry(1)=output
  call CALL_INGRESS(.false.,.true.,status,cutoff_visit64)
  if (status /= SPOR64_B2C_HOST_COMMITTED) &
    error stop 'fresh ingress did not reach host commit'
  publisher_calls=publisher_calls+1
  if (spomoc_calls /= 1 .or. xdrta2_calls /= 1 .or. core_calls /= 1) &
    error stop 'accepted path counter inventory differs'
  if (cutoff_visit64 /= 0_int64) error stop 'stub cutoff differs'
  call VERIFY_PUBLISHED_OUTPUT(output,seed,source,system)
  call VERIFY_SECOND_PUBLICATION_REJECTED(output)
  call LCMCL(output,2)

  call RUN_BLOCKED_CASE('B2F-LIMERG',1)
  call RUN_BLOCKED_CASE('B2F-NONEMPTY',2)
  call RUN_BLOCKED_CASE('B2F-ALIAS',3)
  call RUN_BLOCKED_CASE('B2F-NOSEED',4)
  call RUN_BLOCKED_CASE('B2F-ACCESS',5)
  call RUN_BLOCKED_DAUGHTER_CASE()
  call RUN_PUBLISHER_REJECTIONS()

  if (b2b_calls /= 7) error stop 'B2B call inventory differs'
  if (publisher_calls /= 8) error stop 'publisher call inventory differs'
  if (spomoc_total /= 1 .or. xdrta2_total /= 1 .or. core_total /= 1) &
    error stop 'total boundary inventory differs'

  call LCMCL(source,1)
  call LCMCL(system,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(seed,1)
  write(*,'(A)') 'B2F FRESH-HOST PASS'
  write(*,'(A,I0)') 'B2F REAL-B2B-CALLS=',b2b_calls
  write(*,'(A,I0,A,I0)') 'B2F STUB-XDRTA2-CALLS=',xdrta2_total, &
      ' STUB-CORE-CALLS=',core_total
  write(*,'(A,I0,A)') 'B2F PRODUCTION-PUBLISHER-CALLS=',publisher_calls, &
      ' COMMITS=1'

contains

  subroutine CALL_INGRESS(rec,limerg,status_out,cutoff_out)
    logical, intent(in) :: rec, limerg
    integer, intent(out) :: status_out
    integer(int64), intent(out) :: cutoff_out

    b2b_calls=b2b_calls+1
    call B2F_RESET_PROBES()
    call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
        0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
        rec,0,limerg,370,8,8,32,1,2,1,.false.,.true., &
        status_out,cutoff_out)
  end subroutine CALL_INGRESS


  subroutine RUN_BLOCKED_CASE(object_name,case_id)
    character(len=*), intent(in) :: object_name
    integer, intent(in) :: case_id
    integer :: marker(1), found(1), local_status
    integer(int64) :: local_cutoff
    type(c_ptr) :: local_output

    marker=1700+case_id
    ientry=[1,2,2,3,2,2,2]
    jentry=[0,2,2,2,2,2,2]
    kentry=[c_null_ptr,macro,track,c_loc(fake_track),system,source,seed]
    if (case_id == 3) then
      kentry(1)=seed
    else
      call LCMOP(local_output,object_name,0,1,0)
      kentry(1)=local_output
    end if
    if (case_id == 2) call LCMPUT(local_output,'B2F-KEEP',1,1,marker)
    if (case_id == 4) kentry(7)=c_null_ptr
    if (case_id == 5) jentry(1)=1

    call CALL_INGRESS(.false.,case_id /= 1,local_status,local_cutoff)
    if (local_status /= SPOR64_B2B_ADMISSION_FAILED) &
      error stop 'blocked ingress status differs'
    if (spomoc_calls /= 0 .or. xdrta2_calls /= 0 .or. core_calls /= 0) &
      error stop 'blocked ingress crossed a boundary'
    if (local_cutoff /= 0_int64) error stop 'blocked ingress visited cutoff'
    if (case_id /= 3) then
      if (case_id == 2) then
        call REQUIRE_RECORD(local_output,'B2F-KEEP',1,1)
        call LCMGET(local_output,'B2F-KEEP',found)
        if (any(found /= marker)) error stop 'nonempty sentinel mutated'
        call REQUIRE_RECORD_COUNT(local_output,1)
      else
        call REQUIRE_EMPTY_ROOT(local_output)
      end if
      call LCMCL(local_output,2)
    end if
  end subroutine RUN_BLOCKED_CASE


  subroutine RUN_BLOCKED_DAUGHTER_CASE()
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length, local_status
    integer(int64) :: local_cutoff
    logical :: empty, is_lcm
    type(c_ptr) :: owner, daughter

    ientry=[1,2,2,3,2,2,2]
    jentry=[0,2,2,2,2,2,2]
    kentry=[c_null_ptr,macro,track,c_loc(fake_track),system,source,seed]
    call LCMOP(owner,'B2F-SUBDIR',0,1,0)
    daughter=LCMDID(owner,'EMPTY')
    if (.not. c_associated(daughter)) error stop 'daughter creation failed'
    kentry(1)=daughter

    call CALL_INGRESS(.false.,.true.,local_status,local_cutoff)
    if (local_status /= SPOR64_B2B_ADMISSION_FAILED) &
      error stop 'daughter ingress was not rejected'
    if (spomoc_calls /= 0 .or. xdrta2_calls /= 0 .or. core_calls /= 0) &
      error stop 'daughter ingress crossed a boundary'
    if (local_cutoff /= 0_int64) error stop 'daughter ingress visited cutoff'
    call LCMINF(daughter,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= 'EMPTY') &
      error stop 'daughter ingress mutated its target'
    call REQUIRE_RECORD_COUNT(owner,1)
    call LCMCL(owner,2)
  end subroutine RUN_BLOCKED_DAUGHTER_CASE


  subroutine VERIFY_PUBLISHED_OUTPUT(root,seed_root,source_root,system_root)
    type(c_ptr), intent(in) :: root, seed_root, source_root, system_root
    type(c_ptr) :: authority, authority_flux, authority_source
    type(c_ptr) :: legacy_flux, legacy_source, seed_flux
    type(c_ptr) :: source_outer, source_inner
    integer :: expected_state(NSTATE), found_state(NSTATE)
    integer :: expected_key(NREG), found_key(NREG), found_merge(NMAT)
    integer :: ig, iu
    integer(int32) :: expected_bits32, found_bits32
    integer(int64) :: expected_bits64, found_bits64
    real(real32) :: seed32(NUNKNO), source32(NUNKNO), found32(NUNKNO)
    real(real32) :: expected_eps(5), found_eps(5)
    real(real32) :: expected_leak(NGRP), found_leak(NGRP)
    real(real64) :: found64(NUNKNO)

    call REQUIRE_RECORD_COUNT(root,13)
    call REQUIRE_CHARACTER(root,'SIGNATURE','L_FLUX')
    call REQUIRE_RECORD(root,'SPOT-R64',-1,0)
    authority=LCMGID(root,'SPOT-R64')
    call REQUIRE_RECORD_COUNT(authority,2)
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(authority,'SOUR',NGRP,10)
    authority_flux=LCMGID(authority,'FLUX')
    authority_source=LCMGID(authority,'SOUR')
    call REQUIRE_RECORD(root,'FLUX',NGRP,10)
    call REQUIRE_RECORD(root,'SOUR',NGRP,10)
    legacy_flux=LCMGID(root,'FLUX')
    legacy_source=LCMGID(root,'SOUR')
    seed_flux=LCMGID(seed_root,'FLUX')
    source_outer=LCMGID(source_root,'DSOUR')
    source_inner=LCMGIL(source_outer,1)
    if (.not. all([c_associated(authority_flux), &
        c_associated(authority_source),c_associated(legacy_flux), &
        c_associated(legacy_source),c_associated(seed_flux), &
        c_associated(source_inner)])) error stop 'published list lookup failed'

    do ig=1,NGRP
      call REQUIRE_ELEMENT(authority_flux,ig,NUNKNO,4)
      call REQUIRE_ELEMENT(authority_source,ig,NUNKNO,4)
      call REQUIRE_ELEMENT(legacy_flux,ig,NUNKNO,2)
      call REQUIRE_ELEMENT(legacy_source,ig,NUNKNO,2)
      call LCMGDL(seed_flux,ig,seed32)
      call LCMGDL(source_inner,ig,source32)
      call LCMGDL(authority_flux,ig,found64)
      do iu=1,NUNKNO
        expected_bits64=transfer(real(seed32(iu),real64),0_int64)
        found_bits64=transfer(found64(iu),0_int64)
        if (found_bits64 /= expected_bits64) &
          error stop 'authoritative FLUX promotion differs'
      end do
      call LCMGDL(authority_source,ig,found64)
      do iu=1,NUNKNO
        expected_bits64=transfer(real(source32(iu),real64),0_int64)
        found_bits64=transfer(found64(iu),0_int64)
        if (found_bits64 /= expected_bits64) &
          error stop 'authoritative SOUR promotion differs'
      end do
      call LCMGDL(legacy_flux,ig,found32)
      do iu=1,NUNKNO
        expected_bits32=transfer(seed32(iu),0_int32)
        found_bits32=transfer(found32(iu),0_int32)
        if (found_bits32 /= expected_bits32) &
          error stop 'compatibility FLUX differs'
      end do
      call LCMGDL(legacy_source,ig,found32)
      do iu=1,NUNKNO
        expected_bits32=transfer(source32(iu),0_int32)
        found_bits32=transfer(found32(iu),0_int32)
        if (found_bits32 /= expected_bits32) &
          error stop 'compatibility SOUR differs'
      end do
    end do

    expected_state=0
    expected_state(1)=NGRP
    expected_state(2)=NUNKNO
    expected_state(3)=1
    expected_state(8)=3
    expected_state(9)=3
    expected_state(10)=1
    expected_state(11)=740
    expected_state(12)=500
    expected_state(17)=NMAT
    expected_state(18)=1
    call REQUIRE_RECORD(root,'STATE-VECTOR',NSTATE,1)
    call LCMGET(root,'STATE-VECTOR',found_state)
    if (any(found_state /= expected_state)) error stop 'published state differs'
    expected_eps=[eps32,eps32,eps32,0.0_real32,0.0_real32]
    call REQUIRE_RECORD(root,'EPS-CONVERGE',5,2)
    call LCMGET(root,'EPS-CONVERGE',found_eps)
    if (any(transfer(found_eps,0_int32,5) /= &
        transfer(expected_eps,0_int32,5))) error stop 'published eps differs'
    call REQUIRE_RECORD(root,'IMERGE-LEAK',NMAT,1)
    call LCMGET(root,'IMERGE-LEAK',found_merge)
    if (any(found_merge /= 1)) error stop 'published merge map differs'
    call LCMGET(seed_root,'KEYFLX',expected_key)
    call REQUIRE_RECORD(root,'KEYFLX',NREG,1)
    call LCMGET(root,'KEYFLX',found_key)
    if (any(found_key /= expected_key)) error stop 'published KEYFLX differs'
    call REQUIRE_CHARACTER(root,'OPTION','B0  ')
    call REQUIRE_CHARACTER(root,'LINK.MACRO','MACRO0')
    call REQUIRE_CHARACTER(root,'LINK.TRACK','TRACK')
    call REQUIRE_CHARACTER(root,'LINK.SYSTEM','SYSTEM')
    call REQUIRE_RECORD(system_root,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(system_root,'SPOT-LEAK1D',expected_leak)
    call REQUIRE_RECORD(root,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(root,'SPOT-LEAK1D',found_leak)
    if (any(transfer(found_leak,0_int32,NGRP) /= &
        transfer(expected_leak,0_int32,NGRP))) &
      error stop 'published leakage cache differs'
  end subroutine VERIFY_PUBLISHED_OUTPUT


  subroutine VERIFY_SECOND_PUBLICATION_REJECTED(root)
    type(c_ptr), intent(in) :: root
    type(c_ptr) :: authority, authority_flux
    integer :: keyflx(NREG), merge_map(NMAT), local_status, ir
    real(real32) :: leak(NGRP)
    real(real64) :: flux64(NUNKNO,NGRP), source64(NUNKNO,NGRP)
    real(real64) :: before(NUNKNO), after(NUNKNO)

    authority=LCMGID(root,'SPOT-R64')
    authority_flux=LCMGID(authority,'FLUX')
    call LCMGDL(authority_flux,1,before)
    keyflx=[(ir,ir=1,NREG)]
    merge_map=1
    leak=0.0_real32
    flux64=-1.0_real64
    source64=-2.0_real64
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    if (local_status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'second publication was not rejected'
    call LCMGDL(authority_flux,1,after)
    if (any(transfer(after,0_int64,NUNKNO) /= &
        transfer(before,0_int64,NUNKNO))) &
      error stop 'second publication mutated authority'
  end subroutine VERIFY_SECOND_PUBLICATION_REJECTED


  subroutine RUN_PUBLISHER_REJECTIONS()
    type(c_ptr) :: root, daughter
    integer :: keyflx(NREG), merge_map(NMAT), marker(1), found(1)
    integer :: local_status, iu
    real(real32) :: leak(NGRP)
    real(real64) :: flux64(NUNKNO,NGRP), source64(NUNKNO,NGRP)

    keyflx=[(iu,iu=1,NREG)]
    merge_map=1
    leak=0.0_real32
    flux64=1.0_real64
    source64=2.0_real64

    call LCMOP(root,'B2F-PUB1',0,1,0)
    call SPOR64_B2C_PUBLISH(root,3,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    call REQUIRE_PUBLISHER_REJECTION(root,local_status)

    call LCMOP(root,'B2F-PUB2',0,1,0)
    flux64(1,1)=ieee_value(0.0_real64,ieee_quiet_nan)
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    call REQUIRE_PUBLISHER_REJECTION(root,local_status)
    flux64=1.0_real64

    call LCMOP(root,'B2F-PUB3',0,1,0)
    source64(1,1)=2.0_real64*real(huge(0.0_real32),real64)
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    call REQUIRE_PUBLISHER_REJECTION(root,local_status)
    source64=2.0_real64

    call LCMOP(root,'B2F-PUB4',0,1,0)
    merge_map(NMAT)=2
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    call REQUIRE_PUBLISHER_REJECTION(root,local_status)
    merge_map=1

    call LCMOP(root,'B2F-PUB5',0,1,0)
    marker=9917
    call LCMPUT(root,'B2F-KEEP',1,1,marker)
    call SPOR64_B2C_PUBLISH(root,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    if (local_status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'nonempty publisher target was not rejected'
    call REQUIRE_RECORD(root,'B2F-KEEP',1,1)
    call LCMGET(root,'B2F-KEEP',found)
    if (any(found /= marker)) error stop 'publisher sentinel mutated'
    call REQUIRE_RECORD_COUNT(root,1)
    call LCMCL(root,2)

    call LCMOP(root,'B2F-PUB6',0,1,0)
    daughter=LCMDID(root,'EMPTY')
    if (.not. c_associated(daughter)) error stop 'publisher daughter missing'
    call SPOR64_B2C_PUBLISH(daughter,4,flux64,source64,keyflx,1,merge_map, &
        leak,eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME, &
        local_status)
    publisher_calls=publisher_calls+1
    if (local_status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'daughter publisher target was not rejected'
    call REQUIRE_EMPTY_TABLE(daughter,'EMPTY')
    call REQUIRE_RECORD_COUNT(root,1)
    call LCMCL(root,2)
  end subroutine RUN_PUBLISHER_REJECTIONS


  subroutine REQUIRE_PUBLISHER_REJECTION(root,found_status)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: found_status
    if (found_status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'publisher rejection status differs'
    call REQUIRE_EMPTY_ROOT(root)
    call LCMCL(root,2)
  end subroutine REQUIRE_PUBLISHER_REJECTION


  subroutine REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    call REQUIRE_EMPTY_TABLE(root,'/')
  end subroutine REQUIRE_EMPTY_ROOT


  subroutine REQUIRE_EMPTY_TABLE(root,expected_name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: expected_name
    character(len=72) :: object_file
    character(len=12) :: object_name
    logical :: empty, is_lcm
    integer :: object_length
    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= expected_name) &
      error stop 'expected an empty named LCM table'
  end subroutine REQUIRE_EMPTY_TABLE


  subroutine REQUIRE_RECORD_COUNT(root,expected_count)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected_count
    character(len=72) :: object_file
    character(len=12) :: object_name, name, first
    logical :: empty, is_lcm
    integer :: object_length, found_count

    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. object_length /= -1 .or. empty) &
      error stop 'record count requires a nonempty LCM root'
    name=' '
    call LCMNXT(root,name)
    first=name
    found_count=1
    do
      call LCMNXT(root,name)
      if (name == first) exit
      found_count=found_count+1
      if (found_count > expected_count) exit
    end do
    if (found_count /= expected_count) error stop 'record count differs'
  end subroutine REQUIRE_RECORD_COUNT


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type
    call LCMLEN(root,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) &
      error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_ELEMENT(root,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: index, expected_length, expected_type
    integer :: found_length, found_type
    call LCMLEL(root,index,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) &
      error stop 'list element schema differs'
  end subroutine REQUIRE_ELEMENT


  subroutine REQUIRE_CHARACTER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    character(len=12) :: found
    integer :: expected_words
    expected_words=3
    if (name == 'OPTION') expected_words=1
    call REQUIRE_RECORD(root,name,expected_words,3)
    found=' '
    call LCMGTC(root,name,4*expected_words,found)
    if (expected_words == 1) then
      if (found(1:4) /= expected) error stop 'character record differs'
    else
      if (found /= expected) error stop 'character record differs'
    end if
  end subroutine REQUIRE_CHARACTER

end program TEST_B2F_FRESH_HOST
