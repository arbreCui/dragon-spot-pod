program TEST_B2H_PROJECTION_AUTHORITY
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite, &
      ieee_quiet_nan, ieee_value
  use SPOR64_B2H, only : SPOR64_B2H_ADMISSION_FAILED, &
      SPOR64_B2H_PROJECTED_COMMITTED, SPOR64_B2H_PROJECT, &
      SPOR64_B2H_RECONSTRUCT
  implicit none

  integer, parameter :: NSTATE=40, NGRP=370, NREG=8
  integer, parameter :: NMAT=8, NUNKNO=14
  integer, parameter :: SEED_EPOCH=41
  character(len=1024) :: seed_path, track_path
  integer :: keyflx(NREG)
  integer :: reconstruct_calls, reconstruct_rejections
  integer :: project_calls, project_rejections
  integer :: region_bit_checks, nonregion_bit_checks, mirror_bit_checks
  real(real64) :: seed_rho64, projected_rho64
  real(real64) :: projected_region64(NREG,NGRP)
  real(real64) :: expected_seed_flux64(NUNKNO,NGRP)
  real(real32) :: poisoned_root_flux32(NUNKNO,NGRP)
  type(c_ptr) :: seed_base, track_base

  if (command_argument_count() /= 2) &
    error stop 'expected restart_cap.xsm and restart_track.xsm paths'
  call get_command_argument(1,seed_path)
  call get_command_argument(2,track_path)

  call LCMOP(seed_base,trim(seed_path),2,2,0)
  call LCMOP(track_base,trim(track_path),2,2,0)
  if (.not. c_associated(seed_base) .or. &
      .not. c_associated(track_base)) error stop 'read-only XSM open failed'

  call REQUIRE_RECORD(track_base,'KEYFLX$ANIS',NREG,1)
  call LCMGET(track_base,'KEYFLX$ANIS',keyflx)
  call REQUIRE_VALID_KEY_MAP(keyflx)

  seed_rho64=1.0_real64+spacing(1.0_real64)
  projected_rho64=1.125_real64+spacing(1.125_real64)
  call BUILD_PROJECTED_REGIONS(projected_region64)
  reconstruct_calls=0
  reconstruct_rejections=0
  project_calls=0
  project_rejections=0
  region_bit_checks=0
  nonregion_bit_checks=0
  mirror_bit_checks=0

  call TEST_RECONSTRUCT_CONTRACT()
  call RUN_POSITIVE_PROJECTION()
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
  call RUN_REJECTION(13)

  if (reconstruct_calls /= 6 .or. reconstruct_rejections /= 5) &
    error stop 'reconstruction call inventory differs'
  if (project_calls /= 14 .or. project_rejections /= 13) &
    error stop 'projection call inventory differs'
  if (region_bit_checks /= NREG*NGRP) &
    error stop 'region bit-check inventory differs'
  if (nonregion_bit_checks /= (NUNKNO-NREG)*NGRP) &
    error stop 'non-region bit-check inventory differs'
  if (mirror_bit_checks /= NUNKNO*NGRP) &
    error stop 'mirror bit-check inventory differs'

  call LCMCL(track_base,1)
  call LCMCL(seed_base,1)
  write(*,'(A)') 'B2H PROJECTION-AUTHORITY PASS'
  write(*,'(A,I0,A,I0)') 'B2H RECONSTRUCT-CALLS=',reconstruct_calls, &
      ' REJECTIONS=',reconstruct_rejections
  write(*,'(A,I0,A,I0)') 'B2H PROJECT-CALLS=',project_calls, &
      ' REJECTIONS=',project_rejections
  write(*,'(A,I0,A,I0,A,I0)') 'B2H REGION-BITS=',region_bit_checks, &
      ' NONREGION-BITS=',nonregion_bit_checks,' MIRROR-BITS=',mirror_bit_checks
  write(*,'(A)') &
      'B2H RHO-TYPE4-BITS=2 SOURCE-CARRYOVERS=0 ARTIFACT-WRITES=0'

contains

  subroutine TEST_RECONSTRUCT_CONTRACT()
    real(real32) :: basis32(5,3), bad_basis32(5,3)
    real(real64) :: coordinates64(3), bad_coordinates64(3)
    real(real64) :: short_coordinates64(2)
    real(real64) :: projected64(5), expected64(5), short_output64(4)
    logical :: ok
    integer :: i, a

    basis32=reshape([real(real32) :: &
        1.0_real32,2.0_real32,3.0_real32,4.0_real32,5.0_real32, &
        6.0_real32,7.0_real32,8.0_real32,9.0_real32,10.0_real32, &
        11.0_real32,12.0_real32,13.0_real32,14.0_real32, &
        15.0_real32],[5,3])/16.0_real32
    coordinates64=[0.5_real64+spacing(0.5_real64), &
        1.25_real64+spacing(1.25_real64), &
        0.25_real64+spacing(0.25_real64)]
    expected64=0.0_real64
    do i=1,size(expected64)
      do a=1,size(coordinates64)
        expected64(i)=expected64(i)+ &
            real(basis32(i,a),real64)*coordinates64(a)
      end do
    end do
    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(basis32,coordinates64,projected64,ok)
    if (.not. ok) error stop 'valid reconstruction rejected'
    do i=1,size(projected64)
      if (transfer(projected64(i),0_int64) /= &
          transfer(expected64(i),0_int64)) &
        error stop 'reconstruction loop-order bits differ'
    end do

    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(basis32,coordinates64,short_output64,ok)
    call REQUIRE_RECONSTRUCTION_REJECTED(ok)

    short_coordinates64=coordinates64(1:2)
    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(basis32,short_coordinates64,projected64,ok)
    call REQUIRE_RECONSTRUCTION_REJECTED(ok)

    bad_basis32=basis32
    bad_basis32(2,2)=ieee_value(0.0_real32,ieee_quiet_nan)
    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(bad_basis32,coordinates64,projected64,ok)
    call REQUIRE_RECONSTRUCTION_REJECTED(ok)

    bad_coordinates64=coordinates64
    bad_coordinates64(3)=ieee_value(0.0_real64,ieee_quiet_nan)
    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(basis32,bad_coordinates64,projected64,ok)
    call REQUIRE_RECONSTRUCTION_REJECTED(ok)

    bad_basis32=-1.0_real32
    reconstruct_calls=reconstruct_calls+1
    call SPOR64_B2H_RECONSTRUCT(bad_basis32,coordinates64,projected64,ok)
    call REQUIRE_RECONSTRUCTION_REJECTED(ok)
  end subroutine TEST_RECONSTRUCT_CONTRACT


  subroutine REQUIRE_RECONSTRUCTION_REJECTED(ok)
    logical, intent(in) :: ok

    if (ok) error stop 'invalid reconstruction accepted'
    reconstruct_rejections=reconstruct_rejections+1
  end subroutine REQUIRE_RECONSTRUCTION_REJECTED


  subroutine RUN_POSITIVE_PROJECTION()
    type(c_ptr) :: seed, output
    integer :: status

    call CLONE_OBJECT(seed_base,'B2H-P-SEED',seed)
    call ADD_SOLVED_AUTHORITY(seed,.true.,.true.)
    call LCMOP(output,'B2H-P-OUT',0,1,0)
    if (.not. c_associated(output)) error stop 'positive output open failed'
    call REQUIRE_PREPARED_INPUT(seed,track_base,output)
    project_calls=project_calls+1
    call SPOR64_B2H_PROJECT(output,seed,track_base,projected_region64, &
        projected_rho64,status)
    if (status /= SPOR64_B2H_PROJECTED_COMMITTED) &
      error stop 'valid projection did not commit'
    call VERIFY_PROJECTED_OUTPUT(output,seed)
    call LCMCL(output,2)
    call LCMCL(seed,2)
  end subroutine RUN_POSITIVE_PROJECTION


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    character(len=12) :: seed_name, track_name, output_name
    character(len=12) :: wrong_state
    integer :: status, marker, nonregion_unknown
    integer :: bad_keyflx(NREG)
    real(real32) :: wrong32(NUNKNO), wrong_epoch32
    real(real64) :: local_projected64(NREG,NGRP)
    real(real64) :: short_projected64(NREG-1,NGRP)
    real(real64) :: bad64(NUNKNO)
    type(c_ptr) :: seed, track, output, authority, payload

    write(seed_name,'("B2H-S",I2.2)') case_id
    write(track_name,'("B2H-T",I2.2)') case_id
    write(output_name,'("B2H-O",I2.2)') case_id
    call CLONE_OBJECT(seed_base,seed_name,seed)
    call CLONE_OBJECT(track_base,track_name,track)
    call LCMOP(output,output_name,0,1,0)
    if (.not. c_associated(output)) error stop 'negative output open failed'
    local_projected64=projected_region64
    short_projected64=projected_region64(1:NREG-1,:)

    if (case_id /= 1) call ADD_SOLVED_AUTHORITY(seed,.false.,.false.)
    select case(case_id)
    case(1)
      continue
    case(2)
      authority=LCMGID(seed,'SPOT-R64')
      wrong_state='PROJECTED'
      call LCMPTC(authority,'STATE',12,wrong_state)
    case(3)
      authority=LCMGID(seed,'SPOT-R64')
      wrong_epoch32=real(SEED_EPOCH,real32)
      call LCMPUT(authority,'EPOCH',1,2,wrong_epoch32)
    case(4)
      authority=LCMGID(seed,'SPOT-R64')
      payload=LCMGID(authority,'FLUX')
      wrong32=1.0_real32
      call LCMPDL(payload,1,NUNKNO,2,wrong32)
    case(5)
      authority=LCMGID(seed,'SPOT-R64')
      payload=LCMGID(authority,'SOUR')
      call LCMGDL(payload,1,bad64)
      bad64(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPDL(payload,1,NUNKNO,4,bad64)
    case(6)
      continue
    case(7)
      local_projected64(1,1)= &
          ieee_value(0.0_real64,ieee_quiet_nan)
    case(8)
      local_projected64(1,1)=0.0_real64
    case(9)
      continue
    case(10)
      call LCMGET(track,'KEYFLX$ANIS',bad_keyflx)
      bad_keyflx(2)=bad_keyflx(1)
      call LCMPUT(track,'KEYFLX$ANIS',NREG,1,bad_keyflx)
    case(11)
      marker=271811
      call LCMPUT(output,'SENTINEL',1,1,marker)
    case(12)
      authority=LCMGID(seed,'SPOT-R64')
      payload=LCMGID(authority,'FLUX')
      call LCMGDL(payload,1,bad64)
      nonregion_unknown=FIRST_NONREGION_UNKNOWN(keyflx)
      bad64(nonregion_unknown)=2.0_real64*real(huge(0.0_real32),real64)
      call LCMPDL(payload,1,NUNKNO,4,bad64)
    case(13)
      authority=LCMGID(seed,'SPOT-R64')
      bad64(1)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPUT(authority,'RHO',1,4,bad64(1))
    case default
      error stop 'unknown projection rejection case'
    end select

    project_calls=project_calls+1
    if (case_id == 6) then
      call SPOR64_B2H_PROJECT(output,seed,track,short_projected64, &
          projected_rho64,status)
    else if (case_id == 9) then
      call SPOR64_B2H_PROJECT(output,seed,track,local_projected64, &
          0.0_real64,status)
    else
      call SPOR64_B2H_PROJECT(output,seed,track,local_projected64, &
          projected_rho64,status)
    end if
    if (status /= SPOR64_B2H_ADMISSION_FAILED) &
      error stop 'invalid projection input was accepted'
    if (case_id == 11) then
      call REQUIRE_SENTINEL_UNCHANGED(output,271811)
    else
      call REQUIRE_EMPTY_ROOT(output)
    end if
    project_rejections=project_rejections+1
    call LCMCL(output,2)
    call LCMCL(track,2)
    call LCMCL(seed,2)
  end subroutine RUN_REJECTION


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
          error stop 'projected region lacks REAL64-only witness bit'
      end do
    end do
  end subroutine BUILD_PROJECTED_REGIONS


  subroutine ADD_SOLVED_AUTHORITY(seed,poison_root,capture_expected)
    type(c_ptr), intent(in) :: seed
    logical, intent(in) :: poison_root, capture_expected
    character(len=12) :: state
    integer :: ig, iu, epoch
    real(real32) :: root32(NUNKNO), poison32(NUNKNO)
    real(real64) :: flux64(NUNKNO), source64(NUNKNO), source_base64
    type(c_ptr) :: root_flux, authority, authority_flux, authority_source

    root_flux=LCMGID(seed,'FLUX')
    if (.not. c_associated(root_flux)) error stop 'seed root FLUX missing'
    authority=LCMDID(seed,'SPOT-R64')
    if (.not. c_associated(authority)) &
      error stop 'seed authority directory creation failed'
    state='SOLVED'
    epoch=SEED_EPOCH
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,epoch)
    call LCMPUT(authority,'RHO',1,4,seed_rho64)
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    authority_source=LCMLID(authority,'SOUR',NGRP)
    if (.not. c_associated(authority_flux) .or. &
        .not. c_associated(authority_source)) &
      error stop 'seed authority list creation failed'

    do ig=1,NGRP
      call LCMGDL(root_flux,ig,root32)
      flux64=real(root32,real64)
      do iu=1,NUNKNO
        if (flux64(iu) < 0.0_real64) then
          flux64(iu)=flux64(iu)-spacing(flux64(iu))
        else
          flux64(iu)=flux64(iu)+spacing(flux64(iu))
        end if
        source_base64=8192.0_real64+real(3*ig+iu,real64)/8.0_real64
        source64(iu)=source_base64+spacing(source_base64)
        poison32(iu)=30000.0_real32+real(17*ig+iu,real32)
      end do
      call LCMPDL(authority_flux,ig,NUNKNO,4,flux64)
      call LCMPDL(authority_source,ig,NUNKNO,4,source64)
      if (poison_root) call LCMPDL(root_flux,ig,NUNKNO,2,poison32)
      if (capture_expected) then
        expected_seed_flux64(:,ig)=flux64
        poisoned_root_flux32(:,ig)=poison32
      end if
    end do
  end subroutine ADD_SOLVED_AUTHORITY


  subroutine REQUIRE_PREPARED_INPUT(seed,track,output)
    type(c_ptr), intent(in) :: seed, track, output
    character(len=12) :: state
    integer :: state_vector(NSTATE), track_state(NSTATE)
    integer :: seed_key(NREG), track_key(NREG), imerge(NMAT)
    integer :: epoch, ig, length, record_type
    integer(int32), parameter :: TOL_BITS=int(z'348637bd',int32)
    real(real32) :: eps(5), leak(NGRP), staged32(NUNKNO)
    real(real64) :: rho, staged64(NUNKNO), assembled64(NUNKNO)
    type(c_ptr) :: authority, flux, source

    if (c_associated(seed,track) .or. c_associated(seed,output) .or. &
        c_associated(track,output)) error stop 'prepared objects alias'
    call REQUIRE_EMPTY_ROOT(output)
    call REQUIRE_CHARACTER(seed,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_RECORD(seed,'STATE-VECTOR',NSTATE,1)
    call LCMGET(seed,'STATE-VECTOR',state_vector)
    if (any(state_vector /= [NGRP,NUNKNO,1,0,0,0,0,3,3,1,740,500, &
        0,0,0,0,NMAT,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, &
        0,0,0,0])) error stop 'prepared seed state differs'
    call REQUIRE_RECORD(seed,'EPS-CONVERGE',5,2)
    call LCMGET(seed,'EPS-CONVERGE',eps)
    if (any(transfer(eps(1:3),[0_int32,0_int32,0_int32]) /= &
        TOL_BITS)) error stop 'prepared seed tolerance differs'
    if (any(transfer(eps(4:5),[0_int32,0_int32]) /= 0_int32)) &
      error stop 'prepared terminal tolerance differs'
    call REQUIRE_RECORD(seed,'IMERGE-LEAK',NMAT,1)
    call LCMGET(seed,'IMERGE-LEAK',imerge)
    if (any(imerge /= 1)) error stop 'prepared merge map differs'
    call REQUIRE_RECORD(seed,'KEYFLX',NREG,1)
    call LCMGET(seed,'KEYFLX',seed_key)
    call REQUIRE_CHARACTER(seed,'OPTION',4,'B0  ')
    call REQUIRE_CHARACTER(seed,'LINK.MACRO',12,'MACRO0')
    call REQUIRE_CHARACTER(seed,'LINK.TRACK',12,'TRACK')
    call REQUIRE_CHARACTER(seed,'LINK.SYSTEM',12,'SYSTEM')
    call REQUIRE_RECORD(seed,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(seed,'SPOT-LEAK1D',leak)
    if (.not. all(ieee_is_finite(leak))) &
      error stop 'prepared leakage is nonfinite'

    call REQUIRE_CHARACTER(track,'SIGNATURE',12,'L_TRACK')
    call REQUIRE_RECORD(track,'STATE-VECTOR',NSTATE,1)
    call LCMGET(track,'STATE-VECTOR',track_state)
    if (track_state(1) /= NREG .or. track_state(2) /= NUNKNO) &
      error stop 'prepared TRACK state differs'
    call REQUIRE_RECORD(track,'KEYFLX$ANIS',NREG,1)
    call LCMGET(track,'KEYFLX$ANIS',track_key)
    if (any(seed_key /= track_key)) error stop 'prepared key maps differ'
    call REQUIRE_VALID_KEY_MAP(track_key)

    call REQUIRE_RECORD(seed,'SPOT-R64',-1,0)
    authority=LCMGID(seed,'SPOT-R64')
    call REQUIRE_CHARACTER(authority,'STATE',12,'SOLVED')
    call LCMGTC(authority,'STATE',12,state)
    if (state /= 'SOLVED') error stop 'prepared authority state differs'
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= SEED_EPOCH) error stop 'prepared authority epoch differs'
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call LCMGET(authority,'RHO',rho)
    if (.not. ieee_is_finite(rho) .or. rho <= 0.0_real64) &
      error stop 'prepared authority RHO differs'
    if (transfer(rho,0_int64) /= transfer(seed_rho64,0_int64)) &
      error stop 'prepared authority RHO bits differ'
    if (transfer(rho,0_int64) == transfer( &
        real(real(rho,real32),real64),0_int64)) &
      error stop 'prepared authority RHO lacks REAL64-only bit'
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(authority,'SOUR',NGRP,10)
    flux=LCMGID(authority,'FLUX')
    source=LCMGID(authority,'SOUR')
    do ig=1,NGRP
      call LCMLEL(flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'prepared authority FLUX schema differs'
      call LCMGDL(flux,ig,staged64)
      if (.not. all(ieee_is_finite(staged64))) &
        error stop 'prepared authority FLUX nonfinite'
      assembled64=staged64
      assembled64(track_key)=projected_region64(:,ig)
      if (any(abs(assembled64) > real(huge(0.0_real32),real64))) &
        error stop 'prepared output is not REAL32-representable'
      staged32=real(assembled64,real32)
      if (.not. all(ieee_is_finite(staged32))) &
        error stop 'prepared downcast is nonfinite'
      call LCMLEL(source,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'prepared authority SOUR schema differs'
      call LCMGDL(source,ig,staged64)
      if (.not. all(ieee_is_finite(staged64))) &
        error stop 'prepared authority SOUR nonfinite'
    end do
  end subroutine REQUIRE_PREPARED_INPUT


  subroutine VERIFY_PROJECTED_OUTPUT(output,seed)
    type(c_ptr), intent(in) :: output, seed
    character(len=12) :: authority_state
    integer :: epoch, ig, iu, ir, mapped_region
    integer :: length, record_type
    integer(int64) :: expected_bits64, found_bits64, roundtrip_bits64
    integer(int32) :: expected_bits32, found_bits32
    real(real64) :: found64(NUNKNO), expected64
    real(real32) :: mirror32(NUNKNO)
    type(c_ptr) :: authority, authority_flux, legacy_flux

    call REQUIRE_CHARACTER(output,'SIGNATURE',12,'L_FLUX')
    call REQUIRE_RECORD(output,'SPOT-R64',-1,0)
    call REQUIRE_RECORD(output,'FLUX',NGRP,10)
    call REQUIRE_ABSENT(output,'SOUR')
    call REQUIRE_ABSENT(output,'QFISS')
    call REQUIRE_ABSENT(output,'SPOT-QFISS')
    call REQUIRE_ABSENT(output,'DSOUR')
    call REQUIRE_METADATA_COPY(output,seed)

    authority=LCMGID(output,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'output authority missing'
    call REQUIRE_CHARACTER(authority,'STATE',12,'PROJECTED')
    call LCMGTC(authority,'STATE',12,authority_state)
    if (authority_state /= 'PROJECTED') error stop 'authority state differs'
    call REQUIRE_RECORD(authority,'EPOCH',1,1)
    call LCMGET(authority,'EPOCH',epoch)
    if (epoch /= SEED_EPOCH+1) error stop 'projection epoch did not advance'
    call REQUIRE_RECORD(authority,'RHO',1,4)
    call LCMGET(authority,'RHO',expected64)
    if (transfer(expected64,0_int64) /= &
        transfer(projected_rho64,0_int64)) &
      error stop 'projected RHO bits differ'
    if (transfer(expected64,0_int64) == transfer(seed_rho64,0_int64)) &
      error stop 'projected RHO was confused with seed RHO'
    if (transfer(expected64,0_int64) == transfer( &
        real(real(expected64,real32),real64),0_int64)) &
      error stop 'projected RHO lost REAL64-only bit'
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_ABSENT(authority,'SOUR')
    call REQUIRE_ABSENT(authority,'QFISS')
    call REQUIRE_ABSENT(authority,'SPOT-QFISS')
    call REQUIRE_ABSENT(authority,'DSOUR')

    authority_flux=LCMGID(authority,'FLUX')
    legacy_flux=LCMGID(output,'FLUX')
    if (.not. c_associated(authority_flux) .or. &
        .not. c_associated(legacy_flux)) error stop 'output FLUX list missing'
    do ig=1,NGRP
      call LCMLEL(authority_flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'authority FLUX element schema differs'
      call LCMLEL(legacy_flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 2) &
        error stop 'legacy FLUX element schema differs'
      call LCMGDL(authority_flux,ig,found64)
      call LCMGDL(legacy_flux,ig,mirror32)
      do iu=1,NUNKNO
        mapped_region=0
        do ir=1,NREG
          if (keyflx(ir) == iu) mapped_region=ir
        end do
        if (mapped_region > 0) then
          expected64=projected_region64(mapped_region,ig)
          region_bit_checks=region_bit_checks+1
        else
          expected64=expected_seed_flux64(iu,ig)
          nonregion_bit_checks=nonregion_bit_checks+1
          if (transfer(found64(iu),0_int64) == transfer( &
              real(poisoned_root_flux32(iu,ig),real64),0_int64)) &
            error stop 'non-region value came from poisoned root FLUX'
        end if
        expected_bits64=transfer(expected64,0_int64)
        found_bits64=transfer(found64(iu),0_int64)
        if (found_bits64 /= expected_bits64) &
          error stop 'projected authority FLUX bits differ'
        roundtrip_bits64=transfer( &
            real(real(expected64,real32),real64),0_int64)
        if (found_bits64 == roundtrip_bits64) &
          error stop 'projected authority lost REAL64-only bit'
        expected_bits32=transfer(real(expected64,real32),0_int32)
        found_bits32=transfer(mirror32(iu),0_int32)
        if (found_bits32 /= expected_bits32) &
          error stop 'legacy mirror is not authority downcast'
        mirror_bit_checks=mirror_bit_checks+1
      end do
    end do
  end subroutine VERIFY_PROJECTED_OUTPUT


  subroutine REQUIRE_METADATA_COPY(output,seed)
    type(c_ptr), intent(in) :: output, seed
    integer :: output_state(NSTATE), seed_state(NSTATE)
    integer :: output_imerge(NMAT), seed_imerge(NMAT)
    integer :: output_keyflx(NREG), seed_keyflx(NREG)
    integer :: i
    real(real32) :: output_eps(5), seed_eps(5)
    real(real32) :: output_leak(NGRP), seed_leak(NGRP)

    call REQUIRE_RECORD(output,'STATE-VECTOR',NSTATE,1)
    call REQUIRE_RECORD(output,'EPS-CONVERGE',5,2)
    call REQUIRE_RECORD(output,'IMERGE-LEAK',NMAT,1)
    call REQUIRE_RECORD(output,'KEYFLX',NREG,1)
    call REQUIRE_RECORD(output,'SPOT-LEAK1D',NGRP,2)
    call LCMGET(output,'STATE-VECTOR',output_state)
    call LCMGET(seed,'STATE-VECTOR',seed_state)
    if (any(output_state /= seed_state)) error stop 'STATE-VECTOR not copied'
    call LCMGET(output,'EPS-CONVERGE',output_eps)
    call LCMGET(seed,'EPS-CONVERGE',seed_eps)
    do i=1,size(output_eps)
      if (transfer(output_eps(i),0_int32) /= &
          transfer(seed_eps(i),0_int32)) error stop 'EPS bits not copied'
    end do
    call LCMGET(output,'IMERGE-LEAK',output_imerge)
    call LCMGET(seed,'IMERGE-LEAK',seed_imerge)
    if (any(output_imerge /= seed_imerge)) error stop 'IMERGE not copied'
    call LCMGET(output,'KEYFLX',output_keyflx)
    call LCMGET(seed,'KEYFLX',seed_keyflx)
    if (any(output_keyflx /= seed_keyflx)) error stop 'KEYFLX not copied'
    call LCMGET(output,'SPOT-LEAK1D',output_leak)
    call LCMGET(seed,'SPOT-LEAK1D',seed_leak)
    do i=1,size(output_leak)
      if (transfer(output_leak(i),0_int32) /= &
          transfer(seed_leak(i),0_int32)) error stop 'leak bits not copied'
    end do
    call REQUIRE_CHARACTER(output,'OPTION',4,'B0  ')
    call REQUIRE_CHARACTER(output,'LINK.MACRO',12,'MACRO0')
    call REQUIRE_CHARACTER(output,'LINK.TRACK',12,'TRACK')
    call REQUIRE_CHARACTER(output,'LINK.SYSTEM',12,'SYSTEM')
  end subroutine REQUIRE_METADATA_COPY


  subroutine CLONE_OBJECT(source,name,target)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: target

    call LCMOP(target,name,0,1,0)
    if (.not. c_associated(target)) error stop 'LCM clone target failed'
    call LCMEQU(source,target)
  end subroutine CLONE_OBJECT


  subroutine REQUIRE_VALID_KEY_MAP(map)
    integer, intent(in) :: map(NREG)
    logical :: seen(NUNKNO)
    integer :: ir

    seen=.false.
    do ir=1,NREG
      if (map(ir) < 1 .or. map(ir) > NUNKNO) &
        error stop 'real TRACK key map is out of range'
      if (seen(map(ir))) error stop 'real TRACK key map is not unique'
      seen(map(ir))=.true.
    end do
  end subroutine REQUIRE_VALID_KEY_MAP


  integer function FIRST_NONREGION_UNKNOWN(map)
    integer, intent(in) :: map(NREG)
    logical :: active(NUNKNO)
    integer :: ir, iu

    active=.false.
    do ir=1,NREG
      active(map(ir))=.true.
    end do
    FIRST_NONREGION_UNKNOWN=0
    do iu=1,NUNKNO
      if (.not. active(iu)) then
        FIRST_NONREGION_UNKNOWN=iu
        return
      end if
    end do
    error stop 'real TRACK has no non-region unknown'
  end function FIRST_NONREGION_UNKNOWN


  subroutine REQUIRE_SENTINEL_UNCHANGED(root,expected)
    type(c_ptr), intent(in) :: root
    integer, intent(in) :: expected
    integer :: found

    call REQUIRE_RECORD(root,'SENTINEL',1,1)
    call LCMGET(root,'SENTINEL',found)
    if (found /= expected) error stop 'pre-existing output record changed'
    call REQUIRE_ABSENT(root,'SPOT-R64')
    call REQUIRE_ABSENT(root,'FLUX')
    call REQUIRE_ABSENT(root,'SIGNATURE')
  end subroutine REQUIRE_SENTINEL_UNCHANGED


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


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      error stop 'unexpected output record'
  end subroutine REQUIRE_ABSENT


  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= expected_length .or. record_type /= expected_type) &
      error stop 'record schema differs'
  end subroutine REQUIRE_RECORD


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
end program TEST_B2H_PROJECTION_AUTHORITY
