program TEST_B2P_SOLVED_LIFECYCLE
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_positive_inf, &
      ieee_quiet_nan, ieee_value
  use B2P_STUB_PROBES
  use SPOR64_B2B, only : SPOR64_B2B_CONT, SPOR64_B2B_CORE_FAILED, &
      SPOR64_B2B_INGRESS, SPOR64_B2B_NOT_ACCEPTED
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED, &
      SPOR64_B2C_PREFLIGHT_FAILED, SPOR64_B2C_PUBLISH, &
      SPOR64_B2C_PUBLISH_CONT
  use SPOR64_B2H, only : SPOR64_B2H_PROJECT, &
      SPOR64_B2H_PROJECTED_COMMITTED
  use SPOR64_B2O, only : SPOR64_B2O_SEALED, &
      SPOR64_B2O_SEAL_CONT_PAIR
  implicit none

  integer, parameter :: NENTRY=7, NSTATE=40, NGRP=370
  integer, parameter :: NREG=8, NMAT=8, NUNKNO=14
  integer, parameter :: METADATA_REJECTIONS=16
  character(len=12), parameter :: MACRO_NAME='MACRO0'
  character(len=12), parameter :: TRACK_NAME='TRACK'
  character(len=12), parameter :: SYSTEM_NAME='SYSTEM'
  character(len=12) :: hentry(NENTRY)
  character(len=1024) :: seed_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: ientry(NENTRY), jentry(NENTRY), imerg(NMAT), keyflx(NREG)
  integer :: solved_bit_checks, solved_mirror_checks
  integer :: projected_bit_checks, projected_mirror_checks
  integer :: metadata_rejections_seen, alias_rejections_seen
  integer :: token_rejections_seen, core_rejections_seen
  integer :: seed_verifications, legacy_commits
  real(real32) :: eps32, leakage32(NGRP)
  real(real64) :: expected_terminal_flux64(NUNKNO,NGRP)
  real(real64) :: expected_terminal_source64(NUNKNO,NGRP)
  real(real64) :: projected_region64(NREG,NGRP), projected_rho64
  real(real64) :: lifecycle_keff64, lifecycle_rho64
  type(c_ptr) :: seed_base, macro, track, system_base, source_base
  type(c_ptr) :: assembled, source, sealed_seed, sealed_system
  type(c_ptr) :: kentry(NENTRY)
  type(FIL_file), target :: fake_track

  if (command_argument_count() /= 5) &
    error stop 'expected FLUX_OLD MACRO0 TRACK SYSTEM FSOURCE paths'
  call get_command_argument(1,seed_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,system_path)
  call get_command_argument(5,source_path)

  call LCMOP(seed_base,trim(seed_path),2,2,0)
  call LCMOP(macro,trim(macro_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call LCMOP(system_base,trim(system_path),2,2,0)
  call LCMOP(source_base,trim(source_path),2,2,0)
  if (.not. all([c_associated(seed_base),c_associated(macro), &
      c_associated(track),c_associated(system_base), &
      c_associated(source_base)])) error stop 'read-only XSM open failed'

  call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
  call LCMGET(track,'KEYFLX$ANIS',keyflx)
  call REQUIRE_RECORD(system_base,'SPOT-LEAK1D',NGRP,2)
  call LCMGET(system_base,'SPOT-LEAK1D',leakage32)
  imerg=1
  eps32=transfer(int(z'348637bd',int32),0.0_real32)
  call B2P_BUILD_TERMINALS(expected_terminal_flux64, &
      expected_terminal_source64)
  call BUILD_PROJECTED_REGIONS(projected_region64)
  lifecycle_keff64=nearest(1.0_real64,-1.0_real64)
  lifecycle_rho64=1.0_real64/lifecycle_keff64
  if (transfer(lifecycle_rho64,0_int64) == &
      transfer(1.0_real64,0_int64)) &
    error stop 'lifecycle RHO witness collapsed to unity'
  if (transfer(lifecycle_rho64,0_int64) == transfer( &
      real(real(lifecycle_rho64,real32),real64),0_int64)) &
    error stop 'lifecycle RHO lacks REAL64-only low bits'
  projected_rho64=lifecycle_rho64

  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  hentry=[character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
      'SYSTEM','FSOURCE','FLUX_OLD']
  ientry=[1,2,2,3,2,2,2]
  jentry=[0,2,2,2,2,2,2]
  kentry=[c_null_ptr,macro,track,c_loc(fake_track),c_null_ptr, &
      c_null_ptr,c_null_ptr]

  solved_bit_checks=0
  solved_mirror_checks=0
  projected_bit_checks=0
  projected_mirror_checks=0
  metadata_rejections_seen=0
  alias_rejections_seen=0
  token_rejections_seen=0
  core_rejections_seen=0
  seed_verifications=0
  legacy_commits=0
  call B2P_RESET_PROBES()

  call BUILD_SYNTHETIC_ASSEMBLED(assembled)
  call CLONE_OBJECT(source_base,'B2P-SOURCE',source)
  call ADD_SOURCE_AUTHORITY(source,2)
  call LCMOP(sealed_seed,'B2P-SEED',0,1,0)
  call LCMOP(sealed_system,'B2P-SYSTEM',0,1,0)
  call SEAL_CONT_INPUTS()
  call VERIFY_SEALED_SEED()

  call RUN_LEGACY_PUBLICATION()
  call RUN_METADATA_REJECTION_SET()
  call RUN_ALIAS_REJECTION()
  call RUN_TOKEN_REJECTION()
  call RUN_CORE_REJECTION_SET()
  call RUN_INTEGRATED_CHAIN()

  if (legacy_commits /= 1) error stop 'legacy commit inventory differs'
  if (metadata_rejections_seen /= METADATA_REJECTIONS) &
    error stop 'metadata rejection inventory differs'
  if (alias_rejections_seen /= 1 .or. token_rejections_seen /= 1 .or. &
      core_rejections_seen /= 2) &
    error stop 'publisher/core rejection inventory differs'
  if (seed_verifications /= 5) &
    error stop 'sealed seed verification inventory differs'
  if (xdrta2_calls /= 3 .or. core_calls /= 3) &
    error stop 'stub call inventory differs'
  if (.not. capture_valid .or. .not. terminals_distinct) &
    error stop 'stub terminal distinction was not observed'
  if (solved_bit_checks /= 2*NUNKNO*NGRP) &
    error stop 'SOLVED type-4 bit inventory differs'
  if (solved_mirror_checks /= 2*NUNKNO*NGRP) &
    error stop 'SOLVED mirror bit inventory differs'
  if (projected_bit_checks /= NUNKNO*NGRP) &
    error stop 'PROJECTED type-4 bit inventory differs'
  if (projected_mirror_checks /= NUNKNO*NGRP) &
    error stop 'PROJECTED mirror bit inventory differs'

  call LCMCL(sealed_system,2)
  call LCMCL(sealed_seed,2)
  call LCMCL(source,2)
  call LCMCL(assembled,2)
  call LCMCL(source_base,1)
  call LCMCL(system_base,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(seed_base,1)

  write(*,'(A)') 'B2P SOLVED-LIFECYCLE PASS'
  write(*,'(A,I0,A,I0,A,I0)') 'B2P REAL-B2B-CONT=',3, &
      ' STUB-CORE=',core_calls,' STUB-XDRTA2=',xdrta2_calls
  write(*,'(A,I0,A,I0)') 'B2P SOLVED-TYPE4-BITS=',solved_bit_checks, &
      ' SOLVED-MIRROR-BITS=',solved_mirror_checks
  write(*,'(A,I0,A,I0)') 'B2P PROJECTED-TYPE4-BITS=', &
      projected_bit_checks,' PROJECTED-MIRROR-BITS=', &
      projected_mirror_checks
  write(*,'(A,I0,A,I0,A,I0,A,I0,A,I0)') &
      'B2P LEGACY-COMMITS=',legacy_commits, &
      ' METADATA-REJECTIONS=',metadata_rejections_seen, &
      ' ALIAS-REJECTIONS=',alias_rejections_seen, &
      ' TOKEN-REJECTIONS=',token_rejections_seen, &
      ' CORE-REJECTIONS=',core_rejections_seen
  write(*,'(A)') 'B2P EPOCH=1->2 B2H-PLANE-CARRYOVER=NOT-PRESENT'

contains

  subroutine SEAL_CONT_INPUTS()
    integer :: status
    type(c_ptr) :: authority

    call SPOR64_B2O_SEAL_CONT_PAIR(assembled,source,sealed_seed, &
        sealed_system,status)
    if (status /= SPOR64_B2O_SEALED) error stop 'CONT pair was not sealed'
    authority=LCMGID(sealed_seed,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'sealed authority missing'
    if (.not. EXACT_INVENTORY(authority,[character(len=12) :: &
        'RHO','PLANE','FLUX','STATE','EPOCH'])) &
      error stop 'sealed authority inventory differs'
    call REQUIRE_INTEGER_VALUE(authority,'PLANE',2)
    call REQUIRE_INTEGER_VALUE(authority,'EPOCH',1)
    call REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
  end subroutine SEAL_CONT_INPUTS


  subroutine VERIFY_SEALED_SEED()
    integer :: ig, found_plane, found_epoch
    integer(int64) :: found_rho_bits
    real(real32) :: found32(NUNKNO), expected32(NUNKNO)
    real(real64) :: found64(NUNKNO), expected64(NUNKNO), found_rho64
    type(c_ptr) :: archive_fluxes, archive_seed, expected_authority
    type(c_ptr) :: found_authority, expected_flux, found_flux
    type(c_ptr) :: expected_root_flux, found_root_flux

    if (.not. EXACT_INVENTORY(sealed_seed,[character(len=12) :: &
        'SPOT-R64','FLUX','SIGNATURE','STATE-VECTOR','EPS-CONVERGE', &
        'IMERGE-LEAK','KEYFLX','OPTION','LINK.MACRO','LINK.TRACK', &
        'LINK.SYSTEM','SPOT-LEAK1D'])) &
      error stop 'sealed seed root inventory changed'
    found_authority=LCMGID(sealed_seed,'SPOT-R64')
    if (.not. c_associated(found_authority)) &
      error stop 'sealed seed authority missing'
    if (.not. EXACT_INVENTORY(found_authority,[character(len=12) :: &
        'RHO','PLANE','FLUX','STATE','EPOCH'])) &
      error stop 'sealed seed authority inventory changed'
    call REQUIRE_CHARACTER(found_authority,'STATE',12,'PROJECTED')
    call LCMGET(found_authority,'RHO',found_rho64)
    call LCMGET(found_authority,'PLANE',found_plane)
    call LCMGET(found_authority,'EPOCH',found_epoch)
    found_rho_bits=transfer(found_rho64,0_int64)
    if (found_rho_bits /= transfer(lifecycle_rho64,0_int64) .or. &
        found_plane /= 2 .or. found_epoch /= 1) &
      error stop 'sealed seed metadata changed'

    archive_fluxes=LCMGID(assembled,'FLUX')
    archive_seed=LCMGIL(archive_fluxes,2)
    expected_authority=LCMGID(archive_seed,'SPOT-R64')
    expected_flux=LCMGID(expected_authority,'FLUX')
    found_flux=LCMGID(found_authority,'FLUX')
    expected_root_flux=LCMGID(archive_seed,'FLUX')
    found_root_flux=LCMGID(sealed_seed,'FLUX')
    if (.not. all([c_associated(archive_fluxes), &
        c_associated(archive_seed),c_associated(expected_authority), &
        c_associated(expected_flux),c_associated(found_flux), &
        c_associated(expected_root_flux),c_associated(found_root_flux)])) &
      error stop 'sealed seed comparison payload missing'
    do ig=1,NGRP
      call REQUIRE_LIST_ELEMENT(found_flux,ig,NUNKNO,4)
      call REQUIRE_LIST_ELEMENT(found_root_flux,ig,NUNKNO,2)
      call LCMGDL(expected_flux,ig,expected64)
      call LCMGDL(found_flux,ig,found64)
      if (any(transfer(found64,0_int64,NUNKNO) /= &
          transfer(expected64,0_int64,NUNKNO))) &
        error stop 'sealed seed type-4 FLUX changed'
      call LCMGDL(expected_root_flux,ig,expected32)
      call LCMGDL(found_root_flux,ig,found32)
      if (any(transfer(found32,0_int32,NUNKNO) /= &
          transfer(expected32,0_int32,NUNKNO))) &
        error stop 'sealed seed root FLUX changed'
    end do
    seed_verifications=seed_verifications+1
  end subroutine VERIFY_SEALED_SEED


  subroutine RUN_LEGACY_PUBLICATION()
    integer :: status
    type(c_ptr) :: output, authority

    call LCMOP(output,'B2P-LEGACY',0,1,0)
    call SPOR64_B2C_PUBLISH(output,4,expected_terminal_flux64, &
        expected_terminal_source64,keyflx,1,imerg,leakage32, &
        eps32,eps32,eps32,'B0  ',MACRO_NAME,TRACK_NAME,SYSTEM_NAME,status)
    if (status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'legacy publisher did not commit'
    call REQUIRE_RECORD(output,'SPOT-R64',-1,0)
    authority=LCMGID(output,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'legacy authority missing'
    if (.not. EXACT_INVENTORY(authority,[character(len=12) :: &
        'FLUX','SOUR'])) error stop 'legacy authority acquired lifecycle data'
    call REQUIRE_ABSENT(authority,'RHO')
    call REQUIRE_ABSENT(authority,'PLANE')
    call REQUIRE_ABSENT(authority,'STATE')
    call REQUIRE_ABSENT(authority,'EPOCH')
    legacy_commits=legacy_commits+1
    call LCMCL(output,2)
  end subroutine RUN_LEGACY_PUBLICATION


  subroutine RUN_METADATA_REJECTION_SET()
    integer :: case_id, status, marker
    real(real32) :: wrong_real32, bad_flux32(NUNKNO)
    real(real64) :: bad_rho64, bad_flux64(NUNKNO)
    character(len=12) :: seed_name, output_name, wrong_state
    type(c_ptr) :: bad_seed, output, authority, authority_flux

    do case_id=1,METADATA_REJECTIONS
      write(seed_name,'("B2P-BS",I2.2)') case_id
      write(output_name,'("B2P-BO",I2.2)') case_id
      call CLONE_OBJECT(sealed_seed,seed_name,bad_seed)
      authority=LCMGID(bad_seed,'SPOT-R64')
      if (.not. c_associated(authority)) error stop 'bad seed authority missing'
      select case(case_id)
      case(1)
        wrong_state='SOLVED'
        call LCMPTC(authority,'STATE',12,wrong_state)
      case(2)
        call LCMPUT(authority,'PLANE',1,1,0)
      case(3)
        call LCMPUT(authority,'PLANE',1,1,4)
      case(4)
        wrong_real32=2.0_real32
        call LCMPUT(authority,'PLANE',1,2,wrong_real32)
      case(5)
        marker=31003
        call LCMPUT(authority,'EXTRA',1,1,marker)
      case(6)
        bad_rho64=ieee_value(0.0_real64,ieee_quiet_nan)
        call LCMPUT(authority,'RHO',1,4,bad_rho64)
      case(7)
        bad_rho64=0.0_real64
        call LCMPUT(authority,'RHO',1,4,bad_rho64)
      case(8)
        bad_rho64=-1.0_real64
        call LCMPUT(authority,'RHO',1,4,bad_rho64)
      case(9)
        bad_rho64=ieee_value(0.0_real64,ieee_positive_inf)
        call LCMPUT(authority,'RHO',1,4,bad_rho64)
      case(10)
        wrong_real32=real(lifecycle_rho64,real32)
        call LCMPUT(authority,'RHO',1,2,wrong_real32)
      case(11)
        wrong_real32=1.0_real32
        call LCMPUT(authority,'EPOCH',1,2,wrong_real32)
      case(12)
        call LCMPUT(authority,'EPOCH',1,1,-1)
      case(13)
        call LCMPUT(authority,'EPOCH',1,1,huge(0))
      case(14)
        authority_flux=LCMGID(authority,'FLUX')
        if (.not. c_associated(authority_flux)) &
          error stop 'bad seed FLUX authority missing'
        bad_flux32=1.0_real32
        call LCMPDL(authority_flux,1,NUNKNO,2,bad_flux32)
      case(15)
        continue
      case(16)
        authority_flux=LCMGID(authority,'FLUX')
        if (.not. c_associated(authority_flux)) &
          error stop 'bad seed FLUX authority missing'
        call LCMGDL(authority_flux,NGRP,bad_flux64)
        bad_flux64(NUNKNO)=ieee_value(0.0_real64,ieee_quiet_nan)
        call LCMPDL(authority_flux,NGRP,NUNKNO,4,bad_flux64)
      case default
        error stop 'unknown metadata rejection case'
      end select
      call LCMOP(output,output_name,0,1,0)
      if (case_id == 15) then
        marker=31515
        call LCMPUT(output,'B2P-KEEP',1,1,marker)
      end if
      call SPOR64_B2C_PUBLISH_CONT(output,bad_seed,4, &
          expected_terminal_flux64,expected_terminal_source64,keyflx, &
          1,imerg,leakage32,eps32,eps32,eps32,'B0  ',MACRO_NAME, &
          TRACK_NAME,SYSTEM_NAME,status)
      if (status /= SPOR64_B2C_PREFLIGHT_FAILED) &
        error stop 'invalid lifecycle metadata was accepted'
      if (case_id == 15) then
        call REQUIRE_INTEGER_VALUE(output,'B2P-KEEP',marker)
        if (.not. EXACT_INVENTORY(output,[character(len=12) :: &
            'B2P-KEEP'])) error stop 'nonempty output sentinel changed'
      else
        call REQUIRE_EMPTY_ROOT(output)
      end if
      metadata_rejections_seen=metadata_rejections_seen+1
      call LCMCL(output,2)
      call LCMCL(bad_seed,2)
    end do
  end subroutine RUN_METADATA_REJECTION_SET


  subroutine RUN_ALIAS_REJECTION()
    integer :: status

    call SPOR64_B2C_PUBLISH_CONT(sealed_seed,sealed_seed,4, &
        expected_terminal_flux64,expected_terminal_source64,keyflx, &
        1,imerg,leakage32,eps32,eps32,eps32,'B0  ',MACRO_NAME, &
        TRACK_NAME,SYSTEM_NAME,status)
    if (status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'output/seed alias was accepted'
    alias_rejections_seen=alias_rejections_seen+1
    call VERIFY_SEALED_SEED()
  end subroutine RUN_ALIAS_REJECTION


  subroutine RUN_TOKEN_REJECTION()
    integer :: status
    type(c_ptr) :: output

    call LCMOP(output,'B2P-TOKEN',0,1,0)
    call SPOR64_B2C_PUBLISH_CONT(output,sealed_seed,3, &
        expected_terminal_flux64,expected_terminal_source64,keyflx, &
        1,imerg,leakage32,eps32,eps32,eps32,'B0  ',MACRO_NAME, &
        TRACK_NAME,SYSTEM_NAME,status)
    if (status /= SPOR64_B2C_PREFLIGHT_FAILED) &
      error stop 'nonaccepted token was accepted'
    call REQUIRE_EMPTY_ROOT(output)
    token_rejections_seen=token_rejections_seen+1
    call LCMCL(output,2)
    call VERIFY_SEALED_SEED()
  end subroutine RUN_TOKEN_REJECTION


  subroutine RUN_CORE_REJECTION_SET()
    integer :: case_id, expected_status, status
    integer(int64) :: cutoff
    character(len=12) :: output_name
    type(c_ptr) :: output

    do case_id=1,2
      select case(case_id)
      case(1)
        stub_core_ok=.false.
        stub_accepted=.true.
        expected_status=SPOR64_B2B_CORE_FAILED
      case(2)
        stub_core_ok=.true.
        stub_accepted=.false.
        expected_status=SPOR64_B2B_NOT_ACCEPTED
      case default
        error stop 'unknown core rejection case'
      end select
      write(output_name,'("B2P-CR",I2.2)') case_id
      call LCMOP(output,output_name,0,1,0)
      kentry(1)=output
      kentry(5)=sealed_system
      kentry(6)=source
      kentry(7)=sealed_seed
      call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
          0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
          .false.,0,.true.,370,8,8,32,1,2,1,.false.,.true., &
          SPOR64_B2B_CONT,status,cutoff)
      if (status /= expected_status) &
        error stop 'core rejection status differs'
      call REQUIRE_EMPTY_ROOT(output)
      core_rejections_seen=core_rejections_seen+1
      call LCMCL(output,2)
    end do
    stub_core_ok=.true.
    stub_accepted=.true.
    call VERIFY_SEALED_SEED()
  end subroutine RUN_CORE_REJECTION_SET


  subroutine RUN_INTEGRATED_CHAIN()
    integer :: status
    integer(int64) :: cutoff
    type(c_ptr) :: solved, projected

    call LCMOP(solved,'B2P-SOLVED',0,1,0)
    kentry(1)=solved
    kentry(5)=sealed_system
    kentry(6)=source
    kentry(7)=sealed_seed
    call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
        0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
        .false.,0,.true.,370,8,8,32,1,2,1,.false.,.true., &
        SPOR64_B2B_CONT,status,cutoff)
    if (status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'real B2B CONT did not reach B2C host commit'
    if (cutoff /= B2P_CUTOFF_SENTINEL) &
      error stop 'cutoff sentinel differs'
    if (xdrta2_calls /= 3 .or. core_calls /= 3 .or. &
        .not. capture_valid .or. .not. terminals_distinct) &
      error stop 'real B2B did not execute the distinct-terminal stub once'
    call VERIFY_TERMINAL_DISTINCTION()
    call VERIFY_SOLVED_OUTPUT(solved)
    call VERIFY_SEALED_SEED()

    call LCMOP(projected,'B2P-PROJECT',0,1,0)
    call SPOR64_B2H_PROJECT(projected,solved,track,projected_region64, &
        projected_rho64,status)
    if (status /= SPOR64_B2H_PROJECTED_COMMITTED) &
      error stop 'B2H did not consume production SOLVED/1'
    call VERIFY_PROJECTED_OUTPUT(projected)
    call LCMCL(projected,2)
    call LCMCL(solved,2)
  end subroutine RUN_INTEGRATED_CHAIN


  subroutine VERIFY_TERMINAL_DISTINCTION()
    integer :: ig, iu
    integer(int64) :: input_bits, returned_bits, roundtrip_bits

    do ig=1,NGRP
      do iu=1,NUNKNO
        returned_bits=transfer(returned_flux64(iu,ig),0_int64)
        input_bits=transfer(captured_flux64(iu,ig),0_int64)
        if (returned_bits == input_bits) &
          error stop 'stub terminal FLUX equals B2B input FLUX'
        roundtrip_bits=transfer(real(real(returned_flux64(iu,ig), &
            real32),real64),0_int64)
        if (returned_bits == roundtrip_bits) &
          error stop 'stub terminal FLUX lacks REAL64-only low bit'
        returned_bits=transfer(returned_source64(iu,ig),0_int64)
        input_bits=transfer(captured_qfiss64(iu,ig),0_int64)
        if (returned_bits == input_bits) &
          error stop 'stub terminal SOUR equals B2B fixed source'
        roundtrip_bits=transfer(real(real(returned_source64(iu,ig), &
            real32),real64),0_int64)
        if (returned_bits == roundtrip_bits) &
          error stop 'stub terminal SOUR lacks REAL64-only low bit'
      end do
    end do
  end subroutine VERIFY_TERMINAL_DISTINCTION


  subroutine VERIFY_SOLVED_OUTPUT(solved)
    type(c_ptr), intent(in) :: solved
    integer :: ig, iu, found_plane, found_epoch
    integer(int64) :: found_bits, expected_bits, mirror_bits
    real(real32) :: mirror32(NUNKNO)
    real(real64) :: found64(NUNKNO), found_rho64, seed_rho64
    type(c_ptr) :: authority, authority_flux, authority_source
    type(c_ptr) :: root_flux, root_source, seed_authority

    call REQUIRE_RECORD(solved,'SPOT-R64',-1,0)
    authority=LCMGID(solved,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'SOLVED authority missing'
    if (.not. EXACT_INVENTORY(authority,[character(len=12) :: &
        'RHO','PLANE','FLUX','SOUR','STATE','EPOCH'])) &
      error stop 'SOLVED authority inventory is not exact'
    call REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
    call LCMGET(authority,'PLANE',found_plane)
    call LCMGET(authority,'EPOCH',found_epoch)
    if (found_plane /= 2 .or. found_epoch /= 1) &
      error stop 'SOLVED lifecycle plane/epoch differs'
    call LCMGET(authority,'RHO',found_rho64)
    seed_authority=LCMGID(sealed_seed,'SPOT-R64')
    call LCMGET(seed_authority,'RHO',seed_rho64)
    if (transfer(found_rho64,0_int64) /= transfer(seed_rho64,0_int64)) &
      error stop 'SOLVED RHO was not inherited bit-exactly'

    authority_flux=LCMGID(authority,'FLUX')
    authority_source=LCMGID(authority,'SOUR')
    root_flux=LCMGID(solved,'FLUX')
    root_source=LCMGID(solved,'SOUR')
    if (.not. all([c_associated(authority_flux), &
        c_associated(authority_source),c_associated(root_flux), &
        c_associated(root_source)])) error stop 'SOLVED payload missing'
    do ig=1,NGRP
      call REQUIRE_LIST_ELEMENT(authority_flux,ig,NUNKNO,4)
      call REQUIRE_LIST_ELEMENT(authority_source,ig,NUNKNO,4)
      call REQUIRE_LIST_ELEMENT(root_flux,ig,NUNKNO,2)
      call REQUIRE_LIST_ELEMENT(root_source,ig,NUNKNO,2)
      call LCMGDL(authority_flux,ig,found64)
      call LCMGDL(root_flux,ig,mirror32)
      do iu=1,NUNKNO
        found_bits=transfer(found64(iu),0_int64)
        expected_bits=transfer(returned_flux64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'SOLVED FLUX is not the stub terminal FLUX'
        mirror_bits=transfer(mirror32(iu),0_int32)
        if (mirror_bits /= transfer(real(returned_flux64(iu,ig), &
            real32),0_int32)) error stop 'SOLVED root FLUX downcast differs'
        solved_bit_checks=solved_bit_checks+1
        solved_mirror_checks=solved_mirror_checks+1
      end do
      call LCMGDL(authority_source,ig,found64)
      call LCMGDL(root_source,ig,mirror32)
      do iu=1,NUNKNO
        found_bits=transfer(found64(iu),0_int64)
        expected_bits=transfer(returned_source64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'SOLVED SOUR is not the stub terminal SOUR'
        mirror_bits=transfer(mirror32(iu),0_int32)
        if (mirror_bits /= transfer(real(returned_source64(iu,ig), &
            real32),0_int32)) error stop 'SOLVED root SOUR downcast differs'
        solved_bit_checks=solved_bit_checks+1
        solved_mirror_checks=solved_mirror_checks+1
      end do
    end do
  end subroutine VERIFY_SOLVED_OUTPUT


  subroutine VERIFY_PROJECTED_OUTPUT(projected)
    type(c_ptr), intent(in) :: projected
    integer :: ig, iu, ir, mapped_region, found_epoch
    integer(int64) :: found_bits, expected_bits, mirror_bits
    real(real32) :: mirror32(NUNKNO)
    real(real64) :: found64(NUNKNO), expected64, found_rho64
    type(c_ptr) :: authority, authority_flux, root_flux

    call REQUIRE_RECORD(projected,'SPOT-R64',-1,0)
    authority=LCMGID(projected,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'PROJECTED authority missing'
    if (.not. EXACT_INVENTORY(authority,[character(len=12) :: &
        'RHO','FLUX','STATE','EPOCH'])) &
      error stop 'PROJECTED authority inventory differs'
    call REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMGET(authority,'EPOCH',found_epoch)
    if (found_epoch /= 2) error stop 'B2H did not advance epoch 1 to 2'
    call LCMGET(authority,'RHO',found_rho64)
    if (transfer(found_rho64,0_int64) /= &
        transfer(projected_rho64,0_int64)) &
      error stop 'PROJECTED RHO bits differ'
    call REQUIRE_ABSENT(authority,'PLANE')
    call REQUIRE_ABSENT(authority,'SOUR')
    call REQUIRE_ABSENT(projected,'SOUR')

    authority_flux=LCMGID(authority,'FLUX')
    root_flux=LCMGID(projected,'FLUX')
    if (.not. c_associated(authority_flux) .or. &
        .not. c_associated(root_flux)) error stop 'PROJECTED FLUX missing'
    do ig=1,NGRP
      call REQUIRE_LIST_ELEMENT(authority_flux,ig,NUNKNO,4)
      call REQUIRE_LIST_ELEMENT(root_flux,ig,NUNKNO,2)
      call LCMGDL(authority_flux,ig,found64)
      call LCMGDL(root_flux,ig,mirror32)
      do iu=1,NUNKNO
        mapped_region=0
        do ir=1,NREG
          if (keyflx(ir) == iu) mapped_region=ir
        end do
        if (mapped_region > 0) then
          expected64=projected_region64(mapped_region,ig)
        else
          expected64=returned_flux64(iu,ig)
        end if
        found_bits=transfer(found64(iu),0_int64)
        expected_bits=transfer(expected64,0_int64)
        if (found_bits /= expected_bits) &
          error stop 'B2H PROJECTED payload rule differs'
        mirror_bits=transfer(mirror32(iu),0_int32)
        if (mirror_bits /= transfer(real(expected64,real32),0_int32)) &
          error stop 'B2H PROJECTED root downcast differs'
        projected_bit_checks=projected_bit_checks+1
        projected_mirror_checks=projected_mirror_checks+1
      end do
    end do
  end subroutine VERIFY_PROJECTED_OUTPUT


  subroutine BUILD_PROJECTED_REGIONS(projected)
    real(real64), intent(out) :: projected(NREG,NGRP)
    real(real64) :: base
    integer :: ig, ir

    do ig=1,NGRP
      do ir=1,NREG
        base=4096.0_real64+real(2*ig,real64)+ &
            real(ir,real64)/16.0_real64
        projected(ir,ig)=base+spacing(base)
        if (transfer(projected(ir,ig),0_int64) == transfer( &
            real(real(projected(ir,ig),real32),real64),0_int64)) &
          error stop 'projected region lacks REAL64-only low bit'
      end do
    end do
  end subroutine BUILD_PROJECTED_REGIONS


  subroutine BUILD_SYNTHETIC_ASSEMBLED(root)
    type(c_ptr), intent(out) :: root
    integer :: ip
    character(len=12) :: name, signature, state
    type(c_ptr) :: tracks, libraries, systems, fluxes, item
    type(c_ptr) :: seed, system, authority

    call LCMOP(root,'B2P-ASSEMB',0,1,0)
    signature='L_ARCHIVE'
    call LCMPTC(root,'SIGNATURE',12,signature)
    call LCMPUT(root,'LISTDIM',1,1,3)
    call LCMPUT(root,'SPOT-ITER-K',1,4,lifecycle_keff64)
    tracks=LCMLID(root,'TRACK',3)
    libraries=LCMLID(root,'MICROLIB2',3)
    systems=LCMLID(root,'SYSTEM',3)
    fluxes=LCMLID(root,'FLUX',3)
    if (.not. all([c_associated(tracks),c_associated(libraries), &
        c_associated(systems),c_associated(fluxes)])) &
      error stop 'archive list creation failed'
    do ip=1,3
      item=LCMDIL(tracks,ip)
      item=LCMDIL(libraries,ip)
      write(name,'("B2P-Y",I2.2)') ip
      call CLONE_OBJECT(system_base,name,system)
      call ADD_SYSTEM_AUTHORITY(system,ip)
      write(name,'("B2P-F",I2.2)') ip
      call BUILD_PROJECTED_SEED(name,ip,system,seed)
      item=LCMDIL(fluxes,ip)
      call LCMEQU(seed,item)
      item=LCMDIL(systems,ip)
      call LCMEQU(system,item)
      call LCMCL(seed,2)
      call LCMCL(system,2)
    end do
    authority=LCMDID(root,'SPOT-R64')
    call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)
    call LCMPUT(authority,'NPLANE',1,1,3)
    state='ASSEMBLED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_SYNTHETIC_ASSEMBLED


  subroutine BUILD_PROJECTED_SEED(name,plane,system,seed)
    character(len=*), intent(in) :: name
    integer, intent(in) :: plane
    type(c_ptr), intent(in) :: system
    type(c_ptr), intent(out) :: seed
    integer :: state_vector(NSTATE), imerge_leak(NMAT), seed_keyflx(NREG)
    integer :: ig, iu
    real(real32) :: eps_converge(5), seed_leakage32(NGRP)
    real(real32) :: stage32(NUNKNO)
    real(real64) :: stage64(NUNKNO)
    character(len=4) :: option
    character(len=12) :: signature, link_macro, link_track, link_system
    character(len=12) :: state
    type(c_ptr) :: input_flux, root_flux, authority, authority_flux

    call LCMOP(seed,name,0,1,0)
    input_flux=LCMGID(seed_base,'FLUX')
    root_flux=LCMLID(seed,'FLUX',NGRP)
    authority=LCMDID(seed,'SPOT-R64')
    call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    do ig=1,NGRP
      call LCMGDL(input_flux,ig,stage32)
      call LCMPDL(root_flux,ig,NUNKNO,2,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        if (stage64(iu) < +0.0_real64) then
          stage64(iu)=stage64(iu)- &
              real(plane,real64)*spacing(stage64(iu))
        else
          stage64(iu)=stage64(iu)+ &
              real(plane,real64)*spacing(stage64(iu))
        end if
      end do
      call LCMPDL(authority_flux,ig,NUNKNO,4,stage64)
    end do
    state='PROJECTED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)

    call LCMGTC(seed_base,'SIGNATURE',12,signature)
    call LCMGET(seed_base,'STATE-VECTOR',state_vector)
    call LCMGET(seed_base,'EPS-CONVERGE',eps_converge)
    call LCMGET(seed_base,'IMERGE-LEAK',imerge_leak)
    call LCMGET(seed_base,'KEYFLX',seed_keyflx)
    call LCMGTC(seed_base,'OPTION',4,option)
    call LCMGTC(seed_base,'LINK.MACRO',12,link_macro)
    call LCMGTC(seed_base,'LINK.TRACK',12,link_track)
    call LCMGTC(seed_base,'LINK.SYSTEM',12,link_system)
    call LCMGET(system,'SPOT-LEAK1D',seed_leakage32)
    call LCMPTC(seed,'SIGNATURE',12,signature)
    call LCMPUT(seed,'STATE-VECTOR',NSTATE,1,state_vector)
    call LCMPUT(seed,'EPS-CONVERGE',5,2,eps_converge)
    call LCMPUT(seed,'IMERGE-LEAK',NMAT,1,imerge_leak)
    call LCMPUT(seed,'KEYFLX',NREG,1,seed_keyflx)
    call LCMPTC(seed,'OPTION',4,option)
    call LCMPTC(seed,'LINK.MACRO',12,link_macro)
    call LCMPTC(seed,'LINK.TRACK',12,link_track)
    call LCMPTC(seed,'LINK.SYSTEM',12,link_system)
    call LCMPUT(seed,'SPOT-LEAK1D',NGRP,2,seed_leakage32)
  end subroutine BUILD_PROJECTED_SEED


  subroutine ADD_SOURCE_AUTHORITY(source_object,plane)
    type(c_ptr), intent(in) :: source_object
    integer, intent(in) :: plane
    integer :: ig, iu
    real(real32) :: stage32(NUNKNO)
    real(real64) :: stage64(NUNKNO)
    character(len=12) :: state
    type(c_ptr) :: root_outer, root_source, authority, qfiss

    root_outer=LCMGID(source_object,'DSOUR')
    root_source=LCMGIL(root_outer,1)
    authority=LCMDID(source_object,'SPOT-R64')
    call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)
    call LCMPUT(authority,'PLANE',1,1,plane)
    state='FROZEN-QFIS'
    call LCMPTC(authority,'STATE',12,state)
    qfiss=LCMLID(authority,'QFISS',NGRP)
    do ig=1,NGRP
      call LCMGDL(root_source,ig,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        stage64(iu)=stage64(iu)+spacing(stage64(iu))
      end do
      call LCMPDL(qfiss,ig,NUNKNO,4,stage64)
    end do
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine ADD_SOURCE_AUTHORITY


  subroutine ADD_SYSTEM_AUTHORITY(system,plane)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane
    character(len=12) :: state
    type(c_ptr) :: authority

    call LCMPUT(system,'SPOT-L1-SNAP',1,1,plane)
    authority=LCMDID(system,'SPOT-R64')
    call LCMPUT(authority,'RHO',1,4,lifecycle_rho64)
    state='ASSEMBLED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine ADD_SYSTEM_AUTHORITY


  subroutine CLONE_OBJECT(input,name,output)
    type(c_ptr), intent(in) :: input
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: output

    call LCMOP(output,name,0,1,0)
    if (.not. c_associated(output)) error stop 'LCM clone target failed'
    call LCMEQU(input,output)
  end subroutine CLONE_OBJECT


  subroutine REQUIRE_RECORD(owner,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEN(owner,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) &
      error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


  subroutine REQUIRE_LIST_ELEMENT(owner,index,expected_length,expected_type)
    type(c_ptr), intent(in) :: owner
    integer, intent(in) :: index, expected_length, expected_type
    integer :: found_length, found_type

    call LCMLEL(owner,index,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) &
      error stop 'list element schema differs'
  end subroutine REQUIRE_LIST_ELEMENT


  subroutine REQUIRE_ABSENT(owner,name)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name

    call REQUIRE_RECORD(owner,name,0,99)
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_CHARACTER(owner,name,character_count,expected)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name, expected
    integer, intent(in) :: character_count
    character(len=72) :: found
    integer :: word_count

    word_count=(character_count+3)/4
    call REQUIRE_RECORD(owner,name,word_count,3)
    found=' '
    call LCMGTC(owner,name,character_count,found)
    if (found(1:character_count) /= expected) &
      error stop 'character record differs'
  end subroutine REQUIRE_CHARACTER


  subroutine REQUIRE_INTEGER_VALUE(owner,name,expected)
    type(c_ptr), intent(in) :: owner
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected
    integer :: found

    call REQUIRE_RECORD(owner,name,1,1)
    call LCMGET(owner,name,found)
    if (found /= expected) error stop 'integer record value differs'
  end subroutine REQUIRE_INTEGER_VALUE


  subroutine REQUIRE_EMPTY_ROOT(root)
    type(c_ptr), intent(in) :: root
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    call LCMINF(root,object_file,object_name,empty,object_length,is_lcm)
    if (.not. is_lcm .or. .not. empty .or. object_length /= -1 .or. &
        trim(object_name) /= '/') error stop 'rejected output mutated'
  end subroutine REQUIRE_EMPTY_ROOT


  logical function EXACT_INVENTORY(owner,expected_names)
    type(c_ptr), intent(in) :: owner
    character(len=12), intent(in) :: expected_names(:)
    character(len=12) :: first_name, item_name
    integer :: count, i
    logical :: found(size(expected_names))

    EXACT_INVENTORY=.false.
    found=.false.
    item_name=' '
    call LCMNXT(owner,item_name)
    if (item_name == ' ') return
    first_name=item_name
    count=0
    do
      count=count+1
      if (count > size(expected_names)) return
      do i=1,size(expected_names)
        if (item_name == expected_names(i)) exit
      end do
      if (i > size(expected_names) .or. found(i)) return
      found(i)=.true.
      call LCMNXT(owner,item_name)
      if (item_name == first_name) exit
    end do
    EXACT_INVENTORY=count == size(expected_names) .and. all(found)
  end function EXACT_INVENTORY
end program TEST_B2P_SOLVED_LIFECYCLE
