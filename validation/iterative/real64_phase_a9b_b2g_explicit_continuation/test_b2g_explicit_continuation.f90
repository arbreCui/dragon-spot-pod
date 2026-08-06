program TEST_B2G_EXPLICIT_CONTINUATION
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use B2G_STUB_PROBES
  use SPOR64_B2B, only : SPOR64_B2B_ADMISSION_FAILED, SPOR64_B2B_BOOT, &
      SPOR64_B2B_CONT, SPOR64_B2B_INGRESS
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED
  implicit none

  integer, parameter :: NENTRY=7, NGRP=370, NMAT=8, NUNKNO=14
  integer, parameter :: R64_OFF=0
  character(len=12) :: hentry(NENTRY)
  character(len=1024) :: seed_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: ientry(NENTRY), jentry(NENTRY), imerg(NMAT)
  integer :: ingress_calls, rejected_calls
  real(real32) :: eps32
  real(real64) :: expected_flux64(NUNKNO,NGRP)
  real(real64) :: expected_qfiss64(NUNKNO,NGRP)
  real(real64) :: expected_boot_flux64(NUNKNO,NGRP)
  real(real64) :: expected_boot_qfiss64(NUNKNO,NGRP)
  real(real64) :: roundtrip_flux64(NUNKNO,NGRP)
  real(real64) :: roundtrip_qfiss64(NUNKNO,NGRP)
  real(real64) :: poison_flux64(NUNKNO,NGRP)
  real(real64) :: poison_qfiss64(NUNKNO,NGRP)
  type(c_ptr) :: seed_base, macro, track, system, source_base
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
  call LCMOP(system,trim(system_path),2,2,0)
  call LCMOP(source_base,trim(source_path),2,2,0)
  if (.not. all([c_associated(seed_base),c_associated(macro), &
      c_associated(track),c_associated(system),c_associated(source_base)])) &
    error stop 'read-only XSM open failed'

  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  hentry=[character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
      'SYSTEM','FSOURCE','FLUX_OLD']
  ientry=[1,2,2,3,2,2,2]
  jentry=[0,2,2,2,2,2,2]
  kentry=[c_null_ptr,macro,track,c_loc(fake_track),system, &
      source_base,seed_base]
  imerg=1
  eps32=transfer(int(z'348637bd',int32),0.0_real32)
  ingress_calls=0
  rejected_calls=0
  if (SPOR64_B2B_BOOT /= 1 .or. SPOR64_B2B_CONT /= 2) &
    error stop 'production mode token values differ'
  call B2G_RESET_TOTALS()

  call RUN_BOOT_POSITIVE()
  call RUN_CONT_POSITIVE()
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

  if (ingress_calls /= 13) error stop 'ingress call inventory differs'
  if (rejected_calls /= 11) error stop 'rejection inventory differs'
  if (xdrta2_total /= 2 .or. core_total /= 2) &
    error stop 'rejection crossed XDRTA2/core boundary'

  call LCMCL(source_base,1)
  call LCMCL(system,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(seed_base,1)
  write(*,'(A)') 'B2G EXPLICIT-CONTINUATION PASS'
  write(*,'(A,I0,A,I0)') 'B2G REAL-B2B-CALLS=',ingress_calls, &
      ' REJECTIONS=',rejected_calls
  write(*,'(A,I0,A,I0)') 'B2G STUB-XDRTA2-CALLS=',xdrta2_total, &
      ' STUB-CORE-CALLS=',core_total
  write(*,'(A)') 'B2G TYPE4-POISON-PROOF=BITWISE'

contains

  subroutine RUN_BOOT_POSITIVE()
    type(c_ptr) :: seed, source, output
    integer :: local_status
    integer(int64) :: local_cutoff

    call CLONE_OBJECT(seed_base,'B2G-B-SEED',seed)
    call CLONE_OBJECT(source_base,'B2G-B-SOUR',source)
    call LOAD_BOOT_EXPECTATIONS(seed,source)
    call LCMOP(output,'B2G-B-OUT',0,1,0)
    kentry(1)=output
    kentry(6)=source
    kentry(7)=seed
    call CALL_INGRESS(SPOR64_B2B_BOOT,local_status,local_cutoff)
    if (local_status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'BOOT did not reach production host commit'
    if (local_cutoff /= 0_int64) error stop 'BOOT stub cutoff differs'
    if (xdrta2_calls /= 1 .or. core_calls /= 1 .or. .not. capture_valid) &
      error stop 'BOOT boundary inventory differs'
    call REQUIRE_BOOT_CAPTURE_BITS()
    call REQUIRE_RECORD(output,'SPOT-R64',-1,0)
    call REQUIRE_OUTPUT_AUTHORITY(output,expected_boot_qfiss64)
    call LCMCL(output,2)
    call LCMCL(source,2)
    call LCMCL(seed,2)
  end subroutine RUN_BOOT_POSITIVE


  subroutine RUN_CONT_POSITIVE()
    type(c_ptr) :: seed, source, output
    integer :: local_status
    integer(int64) :: local_cutoff

    call CLONE_OBJECT(seed_base,'B2G-P-SEED',seed)
    call CLONE_OBJECT(source_base,'B2G-P-SOUR',source)
    call ADD_SEED_AUTHORITY(seed,.true.)
    call ADD_SOURCE_AUTHORITY(source,.true.)
    call LCMOP(output,'B2G-P-OUT',0,1,0)
    kentry(1)=output
    kentry(6)=source
    kentry(7)=seed
    call CALL_INGRESS(SPOR64_B2B_CONT,local_status,local_cutoff)
    if (local_status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'CONT did not reach production host commit'
    if (local_cutoff /= 0_int64) error stop 'positive stub cutoff differs'
    if (xdrta2_calls /= 1 .or. core_calls /= 1 .or. .not. capture_valid) &
      error stop 'positive boundary inventory differs'
    call REQUIRE_CAPTURE_BITS()
    call REQUIRE_RECORD(output,'SPOT-R64',-1,0)
    call REQUIRE_OUTPUT_AUTHORITY(output,expected_qfiss64)
    call LCMCL(output,2)
    call LCMCL(source,2)
    call LCMCL(seed,2)
  end subroutine RUN_CONT_POSITIVE


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    integer :: local_status, marker(1)
    integer(int64) :: local_cutoff
    character(len=12) :: seed_name, source_name, output_name
    type(c_ptr) :: seed, source, output, authority, payload
    real(real32) :: wrong32(NUNKNO)

    write(seed_name,'(A,I2.2)') 'B2G-S',case_id
    write(source_name,'(A,I2.2)') 'B2G-Q',case_id
    write(output_name,'(A,I2.2)') 'B2G-O',case_id
    call CLONE_OBJECT(seed_base,seed_name,seed)
    call CLONE_OBJECT(source_base,source_name,source)
    marker=1900+case_id
    wrong32=real(marker(1),real32)

    select case(case_id)
    case(1)
      call ADD_SEED_AUTHORITY(seed,.false.)
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case(2)
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case(3)
      call LCMPUT(seed,'SPOT-R64',1,1,marker)
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case(4)
      authority=LCMDID(seed,'SPOT-R64')
      if (.not. c_associated(authority)) error stop 'seed directory failed'
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case(5)
      call ADD_SEED_AUTHORITY(seed,.false.)
      authority=LCMGID(seed,'SPOT-R64')
      payload=LCMGID(authority,'FLUX')
      call LCMPDL(payload,1,NUNKNO,2,wrong32)
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case(6)
      call ADD_SEED_AUTHORITY(seed,.false.)
    case(7)
      call ADD_SEED_AUTHORITY(seed,.false.)
      call LCMPUT(source,'SPOT-R64',1,1,marker)
    case(8)
      call ADD_SEED_AUTHORITY(seed,.false.)
      authority=LCMDID(source,'SPOT-R64')
      if (.not. c_associated(authority)) error stop 'source directory failed'
    case(9)
      call ADD_SEED_AUTHORITY(seed,.false.)
      call ADD_SOURCE_AUTHORITY(source,.false.)
      authority=LCMGID(source,'SPOT-R64')
      payload=LCMGID(authority,'QFISS')
      call LCMPDL(payload,1,NUNKNO,2,wrong32)
    case(10)
      call ADD_SEED_AUTHORITY(seed,.false.)
    case(11)
      call ADD_SOURCE_AUTHORITY(source,.false.)
    case default
      error stop 'unknown rejection case'
    end select

    call LCMOP(output,output_name,0,1,0)
    kentry(1)=output
    kentry(6)=source
    kentry(7)=seed
    if (case_id == 1) then
      call CALL_INGRESS(R64_OFF,local_status,local_cutoff)
    else if (case_id >= 10) then
      call CALL_INGRESS(SPOR64_B2B_BOOT,local_status,local_cutoff)
    else
      call CALL_INGRESS(SPOR64_B2B_CONT,local_status,local_cutoff)
    end if
    if (local_status /= SPOR64_B2B_ADMISSION_FAILED) &
      error stop 'invalid mode/authority was not rejected'
    if (local_cutoff /= 0_int64) error stop 'rejected call visited cutoff'
    if (xdrta2_calls /= 0 .or. core_calls /= 0 .or. capture_valid) &
      error stop 'rejected call crossed core boundary'
    call REQUIRE_EMPTY_ROOT(output)
    rejected_calls=rejected_calls+1
    call LCMCL(output,2)
    call LCMCL(source,2)
    call LCMCL(seed,2)
  end subroutine RUN_REJECTION


  subroutine CALL_INGRESS(r64_mode,local_status,local_cutoff)
    integer, intent(in) :: r64_mode
    integer, intent(out) :: local_status
    integer(int64), intent(out) :: local_cutoff

    ingress_calls=ingress_calls+1
    call B2G_RESET_PROBES()
    call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
        0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
        .false.,0,.true.,370,8,8,32,1,2,1,.false.,.true., &
        r64_mode,local_status,local_cutoff)
  end subroutine CALL_INGRESS


  subroutine CLONE_OBJECT(source,name,target)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: target

    call LCMOP(target,name,0,1,0)
    if (.not. c_associated(target)) error stop 'LCM clone target failed'
    call LCMEQU(source,target)
  end subroutine CLONE_OBJECT


  subroutine ADD_SEED_AUTHORITY(seed,poison_root)
    type(c_ptr), intent(in) :: seed
    logical, intent(in) :: poison_root
    integer :: ig, iu
    real(real32) :: stage32(NUNKNO), poison32(NUNKNO)
    real(real64) :: stage64(NUNKNO)
    type(c_ptr) :: root_flux, authority, authority_flux

    root_flux=LCMGID(seed,'FLUX')
    if (.not. c_associated(root_flux)) error stop 'root FLUX missing'
    authority=LCMDID(seed,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'seed authority failed'
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    if (.not. c_associated(authority_flux)) error stop 'authority FLUX failed'
    do ig=1,NGRP
      call LCMGDL(root_flux,ig,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        if (stage64(iu) < 0.0_real64) then
          stage64(iu)=stage64(iu)-spacing(stage64(iu))
        else
          stage64(iu)=stage64(iu)+spacing(stage64(iu))
        end if
      end do
      call LCMPDL(authority_flux,ig,NUNKNO,4,stage64)
      if (poison_root) then
        do iu=1,NUNKNO
          poison32(iu)=4096.0_real32+real(17*ig+iu,real32)
        end do
        call LCMPDL(root_flux,ig,NUNKNO,2,poison32)
        expected_flux64(:,ig)=stage64
        roundtrip_flux64(:,ig)=real(real(stage64,real32),real64)
        poison_flux64(:,ig)=real(poison32,real64)
      end if
    end do
  end subroutine ADD_SEED_AUTHORITY


  subroutine ADD_SOURCE_AUTHORITY(source,poison_root)
    type(c_ptr), intent(in) :: source
    logical, intent(in) :: poison_root
    integer :: ig, iu
    real(real32) :: stage32(NUNKNO), poison32(NUNKNO)
    real(real64) :: stage64(NUNKNO)
    type(c_ptr) :: root_outer, root_source, authority, authority_qfiss

    root_outer=LCMGID(source,'DSOUR')
    if (.not. c_associated(root_outer)) error stop 'root DSOUR missing'
    root_source=LCMGIL(root_outer,1)
    if (.not. c_associated(root_source)) error stop 'DSOUR child missing'
    authority=LCMDID(source,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'source authority failed'
    authority_qfiss=LCMLID(authority,'QFISS',NGRP)
    if (.not. c_associated(authority_qfiss)) error stop 'QFISS list failed'
    do ig=1,NGRP
      call LCMGDL(root_source,ig,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        stage64(iu)=stage64(iu)+spacing(stage64(iu))
      end do
      call LCMPDL(authority_qfiss,ig,NUNKNO,4,stage64)
      if (poison_root) then
        do iu=1,NUNKNO
          poison32(iu)=8192.0_real32+real(19*ig+iu,real32)
        end do
        call LCMPDL(root_source,ig,NUNKNO,2,poison32)
        expected_qfiss64(:,ig)=stage64
        roundtrip_qfiss64(:,ig)=real(real(stage64,real32),real64)
        poison_qfiss64(:,ig)=real(poison32,real64)
      end if
    end do
  end subroutine ADD_SOURCE_AUTHORITY


  subroutine LOAD_BOOT_EXPECTATIONS(seed,source)
    type(c_ptr), intent(in) :: seed, source
    integer :: ig
    real(real32) :: stage32(NUNKNO)
    type(c_ptr) :: root_flux, root_outer, root_source

    root_flux=LCMGID(seed,'FLUX')
    if (.not. c_associated(root_flux)) error stop 'BOOT root FLUX missing'
    root_outer=LCMGID(source,'DSOUR')
    if (.not. c_associated(root_outer)) error stop 'BOOT root DSOUR missing'
    root_source=LCMGIL(root_outer,1)
    if (.not. c_associated(root_source)) error stop 'BOOT DSOUR child missing'
    do ig=1,NGRP
      call LCMGDL(root_flux,ig,stage32)
      expected_boot_flux64(:,ig)=real(stage32,real64)
      call LCMGDL(root_source,ig,stage32)
      expected_boot_qfiss64(:,ig)=real(stage32,real64)
    end do
  end subroutine LOAD_BOOT_EXPECTATIONS


  subroutine REQUIRE_CAPTURE_BITS()
    integer :: ig, iu
    integer(int64) :: expected_bits, found_bits, poison_bits

    do ig=1,NGRP
      do iu=1,NUNKNO
        expected_bits=transfer(expected_flux64(iu,ig),0_int64)
        found_bits=transfer(captured_flux64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'core FLUX differs from type-4 authority'
        poison_bits=transfer(roundtrip_flux64(iu,ig),0_int64)
        if (found_bits == poison_bits) &
          error stop 'core FLUX lost REAL64-only authority bits'
        poison_bits=transfer(poison_flux64(iu,ig),0_int64)
        if (found_bits == poison_bits) &
          error stop 'core FLUX equals promoted root poison'
        expected_bits=transfer(expected_qfiss64(iu,ig),0_int64)
        found_bits=transfer(captured_qfiss64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'core source differs from type-4 QFISS authority'
        poison_bits=transfer(roundtrip_qfiss64(iu,ig),0_int64)
        if (found_bits == poison_bits) &
          error stop 'core QFISS lost REAL64-only authority bits'
        poison_bits=transfer(poison_qfiss64(iu,ig),0_int64)
        if (found_bits == poison_bits) &
          error stop 'core source equals promoted root poison'
      end do
    end do
  end subroutine REQUIRE_CAPTURE_BITS


  subroutine REQUIRE_BOOT_CAPTURE_BITS()
    integer :: ig, iu
    integer(int64) :: expected_bits, found_bits

    do ig=1,NGRP
      do iu=1,NUNKNO
        expected_bits=transfer(expected_boot_flux64(iu,ig),0_int64)
        found_bits=transfer(captured_flux64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'BOOT core FLUX is not exact type-2 promotion'
        expected_bits=transfer(expected_boot_qfiss64(iu,ig),0_int64)
        found_bits=transfer(captured_qfiss64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'BOOT core source is not exact type-2 promotion'
      end do
    end do
  end subroutine REQUIRE_BOOT_CAPTURE_BITS


  subroutine REQUIRE_OUTPUT_AUTHORITY(root,input_qfiss64)
    type(c_ptr), intent(in) :: root
    real(real64), intent(in) :: input_qfiss64(NUNKNO,NGRP)
    integer :: ig, iu, length, record_type
    integer(int64) :: expected_bits, found_bits, qfiss_bits
    real(real64) :: published_source64(NUNKNO)
    type(c_ptr) :: authority, flux, source

    authority=LCMGID(root,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'output authority missing'
    call REQUIRE_RECORD(authority,'FLUX',NGRP,10)
    call REQUIRE_RECORD(authority,'SOUR',NGRP,10)
    call REQUIRE_ABSENT(authority,'QFISS')
    flux=LCMGID(authority,'FLUX')
    source=LCMGID(authority,'SOUR')
    do ig=1,NGRP
      call LCMLEL(flux,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'published FLUX is not type 4'
      call LCMLEL(source,ig,length,record_type)
      if (length /= NUNKNO .or. record_type /= 4) &
        error stop 'published SOUR is not type 4'
      call LCMGDL(source,ig,published_source64)
      do iu=1,NUNKNO
        expected_bits=transfer( &
            real(1000*ig+iu,real64)/8.0_real64,0_int64)
        found_bits=transfer(published_source64(iu),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'published SOUR differs from core terminal source'
        qfiss_bits=transfer(input_qfiss64(iu,ig),0_int64)
        if (found_bits == qfiss_bits) &
          error stop 'published SOUR was confused with fixed QFISS'
      end do
    end do
  end subroutine REQUIRE_OUTPUT_AUTHORITY


  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: length, record_type

    call LCMLEN(root,name,length,record_type)
    if (length /= 0 .or. record_type /= 99) &
      error stop 'unexpected output authority record'
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
end program TEST_B2G_EXPLICIT_CONTINUATION
