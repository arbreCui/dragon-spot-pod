program TEST_B2O_CONT_BINDING_CUTOFF
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_loc, c_null_ptr, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64
  use, intrinsic :: ieee_arithmetic, only : ieee_positive_inf, &
      ieee_quiet_nan, ieee_value
  use B2O_STUB_PROBES
  use SPOR64_B2B, only : SPOR64_B2B_ADMISSION_FAILED, &
      SPOR64_B2B_CONT, SPOR64_B2B_INGRESS
  use SPOR64_B2C, only : SPOR64_B2C_HOST_COMMITTED
  use SPOR64_B2O, only : SPOR64_B2O_PREFLIGHT_FAILED, SPOR64_B2O_SEALED, &
      SPOR64_B2O_SEAL_CONT_PAIR
  implicit none

  integer, parameter :: NENTRY=7, NGRP=370, NMAT=8, NUNKNO=14
  integer, parameter :: NEGATIVE_CASES=32
  character(len=12) :: hentry(NENTRY)
  character(len=1024) :: seed_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: ientry(NENTRY), jentry(NENTRY), imerg(NMAT)
  integer :: ingress_calls, rejected_calls
  integer :: sealer_calls, sealer_positives, sealer_rejections
  real(real32) :: eps32
  real(real64) :: expected_flux64(NUNKNO,NGRP)
  real(real64) :: expected_qfiss64(NUNKNO,NGRP)
  type(c_ptr) :: seed_base, macro, track, system_base, source_base
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

  fake_track%unit=77
  fake_track%kdi_file=c_null_ptr
  hentry=[character(len=12) :: 'FLUX','MACRO0','TRACK','TRACK_f', &
      'SYSTEM','FSOURCE','FLUX_OLD']
  ientry=[1,2,2,3,2,2,2]
  jentry=[0,2,2,2,2,2,2]
  kentry=[c_null_ptr,macro,track,c_loc(fake_track),system_base, &
      source_base,seed_base]
  imerg=1
  eps32=transfer(int(z'348637bd',int32),0.0_real32)
  ingress_calls=0
  rejected_calls=0
  sealer_calls=0
  sealer_positives=0
  sealer_rejections=0
  call B2O_RESET_TOTALS()

  call RUN_POSITIVE()
  call RUN_SEALER_CASES()
  call RUN_REJECTION_SET()

  if (ingress_calls /= NEGATIVE_CASES+1) &
    error stop 'ingress call inventory differs'
  if (rejected_calls /= NEGATIVE_CASES) &
    error stop 'rejection inventory differs'
  if (xdrta2_total /= 1 .or. core_total /= 1) &
    error stop 'a rejected lifecycle crossed the core boundary'
  if (sealer_calls /= 7 .or. sealer_positives /= 2 .or. &
      sealer_rejections /= 5) error stop 'sealer inventory differs'

  call LCMCL(source_base,1)
  call LCMCL(system_base,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(seed_base,1)
  write(*,'(A)') 'B2O CONT-BINDING-CUTOFF PASS'
  write(*,'(A,I0,A,I0)') 'B2O REAL-B2B-CALLS=',ingress_calls, &
      ' REJECTIONS=',rejected_calls
  write(*,'(A,I0,A,I0)') 'B2O STUB-XDRTA2-CALLS=',xdrta2_total, &
      ' STUB-CORE-CALLS=',core_total
  write(*,'(A,I0,A,I0,A,I0)') 'B2O SEALER-CALLS=',sealer_calls, &
      ' POSITIVES=',sealer_positives,' REJECTIONS=',sealer_rejections
  write(*,'(A,I0)') 'B2O INT64-CUTOFF-SENTINEL=', &
      B2O_CUTOFF_SENTINEL

contains

  subroutine RUN_POSITIVE()
    type(c_ptr) :: assembled, seed, source, system, output
    integer :: local_status, seal_status
    integer(int64) :: local_cutoff

    call CLONE_OBJECT(source_base,'B2O-P-SOUR',source)
    call ADD_SOURCE_AUTHORITY(source)
    call BUILD_SYNTHETIC_ASSEMBLED(assembled)
    call LCMOP(seed,'B2O-P-SEED',0,1,0)
    call LCMOP(system,'B2O-P-SYS',0,1,0)
    call SPOR64_B2O_SEAL_CONT_PAIR(assembled,source,seed,system, &
        seal_status)
    sealer_calls=sealer_calls+1
    if (seal_status /= SPOR64_B2O_SEALED) &
      error stop 'same-index CONT pair was not sealed'
    sealer_positives=sealer_positives+1
    call REQUIRE_SEALED_PLANE(seed,1)
    call LCMOP(output,'B2O-P-OUT',0,1,0)
    kentry(1)=output
    kentry(5)=system
    kentry(6)=source
    kentry(7)=seed
    call CALL_INGRESS(local_status,local_cutoff)
    if (local_status /= SPOR64_B2C_HOST_COMMITTED) &
      error stop 'predicate-bound CONT did not reach host commit'
    if (local_cutoff /= B2O_CUTOFF_SENTINEL) &
      error stop 'INT64 cutoff sentinel did not return bit-exactly'
    if (xdrta2_calls /= 1 .or. core_calls /= 1 .or. &
        .not. capture_valid) error stop 'positive boundary inventory differs'
    call REQUIRE_CAPTURE_BITS()
    call LCMCL(output,2)
    call LCMCL(system,2)
    call LCMCL(seed,2)
    call LCMCL(assembled,2)
    call LCMCL(source,2)
  end subroutine RUN_POSITIVE


  subroutine RUN_SEALER_CASES()
    integer :: case_id, seal_status
    real(real64) :: wrong_rho64
    character(len=12) :: source_name, seed_name, system_name, wrong_state
    type(c_ptr) :: assembled, source, seed, system
    type(c_ptr) :: source_authority, root_authority

    do case_id=1,6
      write(source_name,'(A,I2.2)') 'B2O-EQ',case_id
      write(seed_name,'(A,I2.2)') 'B2O-ES',case_id
      write(system_name,'(A,I2.2)') 'B2O-EY',case_id
      call CLONE_OBJECT(source_base,source_name,source)
      call ADD_SOURCE_AUTHORITY(source)
      call BUILD_SYNTHETIC_ASSEMBLED(assembled)
      source_authority=LCMGID(source,'SPOT-R64')
      root_authority=LCMGID(assembled,'SPOT-R64')
      if (.not. all([c_associated(source_authority), &
          c_associated(root_authority)])) error stop 'sealer case authority'
      select case(case_id)
      case(1)
        call LCMPUT(source_authority,'PLANE',1,1,2)
      case(2)
        call LCMPUT(source_authority,'PLANE',1,1,0)
      case(3)
        wrong_rho64=nearest(1.0_real64,1.0_real64)
        call LCMPUT(source_authority,'RHO',1,4,wrong_rho64)
      case(4)
        wrong_state='PROJECTED'
        call LCMPTC(source_authority,'STATE',12,wrong_state)
      case(5)
        wrong_rho64=nearest(1.0_real64,-1.0_real64)
        call LCMPUT(root_authority,'RHO',1,4,wrong_rho64)
      case(6)
        call LCMPUT(source_authority,'EPOCH',1,1,2)
      end select
      call LCMOP(seed,seed_name,0,1,0)
      call LCMOP(system,system_name,0,1,0)
      call SPOR64_B2O_SEAL_CONT_PAIR(assembled,source,seed,system, &
          seal_status)
      sealer_calls=sealer_calls+1
      if (case_id == 1) then
        if (seal_status /= SPOR64_B2O_SEALED) &
          error stop 'source-selected plane 2 was not sealed'
        call REQUIRE_SEALED_PLANE(seed,2)
        sealer_positives=sealer_positives+1
      else
        if (seal_status /= SPOR64_B2O_PREFLIGHT_FAILED) &
          error stop 'invalid same-index sealer input was accepted'
        call REQUIRE_EMPTY_ROOT(seed)
        call REQUIRE_EMPTY_ROOT(system)
        sealer_rejections=sealer_rejections+1
      end if
      call LCMCL(system,2)
      call LCMCL(seed,2)
      call LCMCL(assembled,2)
      call LCMCL(source,2)
    end do
  end subroutine RUN_SEALER_CASES


  subroutine RUN_REJECTION_SET()
    integer :: case_id

    do case_id=1,NEGATIVE_CASES
      call RUN_REJECTION(case_id)
    end do
  end subroutine RUN_REJECTION_SET


  subroutine RUN_REJECTION(case_id)
    integer, intent(in) :: case_id
    character(len=12) :: seed_name, source_name, system_name, output_name
    character(len=12) :: wrong_state
    integer :: local_status, marker
    integer(int64) :: local_cutoff
    real(real32) :: leak32(NGRP), wrong_real32
    real(real64) :: rho64
    type(c_ptr) :: seed, source, system, output
    type(c_ptr) :: seed_authority, source_authority, system_authority

    write(seed_name,'(A,I2.2)') 'B2O-S',case_id
    write(source_name,'(A,I2.2)') 'B2O-Q',case_id
    write(system_name,'(A,I2.2)') 'B2O-Y',case_id
    write(output_name,'(A,I2.2)') 'B2O-O',case_id
    call PREPARE_CONT_OBJECTS(seed_name,source_name,system_name, &
        case_id == 1,seed,source,system)
    seed_authority=LCMGID(seed,'SPOT-R64')
    source_authority=LCMGID(source,'SPOT-R64')
    system_authority=LCMGID(system,'SPOT-R64')
    if (.not. c_associated(seed_authority)) error stop 'seed authority missing'
    if (.not. c_associated(source_authority)) error stop 'source authority missing'
    if (.not. c_associated(system_authority)) error stop 'system authority missing'
    marker=8000+case_id

    select case(case_id)
    case(1)
      continue
    case(2)
      call LCMPUT(seed_authority,'RHO',1,1,marker)
    case(3)
      rho64=nearest(1.0_real64,1.0_real64)
      call LCMPUT(source_authority,'RHO',1,4,rho64)
    case(4)
      rho64=nearest(1.0_real64,-1.0_real64)
      call LCMPUT(system_authority,'RHO',1,4,rho64)
    case(5)
      wrong_state='SOLVED'
      call LCMPTC(seed_authority,'STATE',12,wrong_state)
    case(6)
      wrong_state='PROJECTED'
      call LCMPTC(source_authority,'STATE',12,wrong_state)
    case(7)
      wrong_state='PROJECTED'
      call LCMPTC(system_authority,'STATE',12,wrong_state)
    case(8)
      call LCMPUT(seed_authority,'EPOCH',1,1,2)
    case(9)
      call LCMPUT(source_authority,'EPOCH',1,1,2)
    case(10)
      call LCMPUT(system_authority,'EPOCH',1,1,2)
    case(11)
      call LCMPUT(source_authority,'PLANE',1,1,2)
    case(12)
      call LCMPUT(source_authority,'PLANE',1,1,0)
      call LCMPUT(system,'SPOT-L1-SNAP',1,1,0)
    case(13)
      call LCMGET(seed,'SPOT-LEAK1D',leak32)
      leak32(1)=nearest(leak32(1),1.0_real32)
      call LCMPUT(seed,'SPOT-LEAK1D',NGRP,2,leak32)
    case(14)
      call LCMPUT(seed_authority,'EXTRA',1,1,marker)
    case(15)
      call LCMPUT(source_authority,'EXTRA',1,1,marker)
    case(16)
      call LCMPUT(system_authority,'EXTRA',1,1,marker)
    case(17)
      wrong_real32=1.0_real32
      call LCMPUT(source_authority,'PLANE',1,2,wrong_real32)
    case(18)
      wrong_real32=1.0_real32
      call LCMPUT(system,'SPOT-L1-SNAP',1,2,wrong_real32)
    case(19)
      rho64=+0.0_real64
      call LCMPUT(seed_authority,'RHO',1,4,rho64)
    case(20)
      rho64=+0.0_real64
      call LCMPUT(source_authority,'RHO',1,4,rho64)
    case(21)
      rho64=+0.0_real64
      call LCMPUT(system_authority,'RHO',1,4,rho64)
    case(22)
      rho64=-1.0_real64
      call LCMPUT(seed_authority,'RHO',1,4,rho64)
    case(23)
      rho64=-1.0_real64
      call LCMPUT(source_authority,'RHO',1,4,rho64)
    case(24)
      rho64=-1.0_real64
      call LCMPUT(system_authority,'RHO',1,4,rho64)
    case(25)
      rho64=ieee_value(0.0_real64,ieee_positive_inf)
      call LCMPUT(seed_authority,'RHO',1,4,rho64)
    case(26)
      rho64=ieee_value(0.0_real64,ieee_positive_inf)
      call LCMPUT(source_authority,'RHO',1,4,rho64)
    case(27)
      rho64=ieee_value(0.0_real64,ieee_positive_inf)
      call LCMPUT(system_authority,'RHO',1,4,rho64)
    case(28)
      rho64=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPUT(seed_authority,'RHO',1,4,rho64)
    case(29)
      rho64=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPUT(source_authority,'RHO',1,4,rho64)
    case(30)
      rho64=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPUT(system_authority,'RHO',1,4,rho64)
    case(31)
      call LCMPUT(seed_authority,'PLANE',1,1,2)
    case(32)
      wrong_real32=1.0_real32
      call LCMPUT(seed_authority,'PLANE',1,2,wrong_real32)
    case default
      error stop 'unknown negative case'
    end select

    call LCMOP(output,output_name,0,1,0)
    kentry(1)=output
    kentry(5)=system
    kentry(6)=source
    kentry(7)=seed
    call CALL_INGRESS(local_status,local_cutoff)
    if (local_status /= SPOR64_B2B_ADMISSION_FAILED) &
      error stop 'invalid lifecycle was not rejected'
    if (local_cutoff /= 0_int64) &
      error stop 'rejected lifecycle returned a cutoff count'
    if (xdrta2_calls /= 0 .or. core_calls /= 0 .or. capture_valid) &
      error stop 'rejected lifecycle crossed the core boundary'
    call REQUIRE_EMPTY_ROOT(output)
    rejected_calls=rejected_calls+1
    call LCMCL(output,2)
    call LCMCL(system,2)
    call LCMCL(source,2)
    call LCMCL(seed,2)
  end subroutine RUN_REJECTION


  subroutine PREPARE_CONT_OBJECTS(seed_name,source_name,system_name, &
      omit_seed_rho,seed,source,system)
    character(len=*), intent(in) :: seed_name, source_name, system_name
    logical, intent(in) :: omit_seed_rho
    type(c_ptr), intent(out) :: seed, source, system

    call CLONE_OBJECT(seed_base,seed_name,seed)
    call CLONE_OBJECT(source_base,source_name,source)
    call CLONE_OBJECT(system_base,system_name,system)
    call SYNC_SEED_LEAKAGE(seed,system)
    call ADD_SEED_AUTHORITY(seed,omit_seed_rho,.true.)
    call ADD_SOURCE_AUTHORITY(source)
    call ADD_SYSTEM_AUTHORITY(system,1)
  end subroutine PREPARE_CONT_OBJECTS


  subroutine BUILD_PROJECTED_SEED(name,plane,system,seed)
    character(len=*), intent(in) :: name
    integer, intent(in) :: plane
    type(c_ptr), intent(in) :: system
    type(c_ptr), intent(out) :: seed
    integer :: state_vector(40), imerge_leak(NMAT), keyflx(8)
    integer :: ig, iu
    real(real32) :: eps_converge(5), leakage32(NGRP)
    real(real32) :: stage32(NUNKNO)
    real(real64) :: rho64, stage64(NUNKNO)
    character(len=4) :: option
    character(len=12) :: signature, link_macro, link_track, link_system
    character(len=12) :: state
    type(c_ptr) :: input_flux, root_flux, authority, authority_flux

    if (plane < 1 .or. plane > 3) &
      error stop 'projected seed plane is out of range'
    call LCMOP(seed,name,0,1,0)
    if (.not. c_associated(seed)) error stop 'projected seed creation failed'
    input_flux=LCMGID(seed_base,'FLUX')
    if (.not. c_associated(input_flux)) error stop 'base FLUX missing'
    root_flux=LCMLID(seed,'FLUX',NGRP)
    authority=LCMDID(seed,'SPOT-R64')
    if (.not. all([c_associated(root_flux),c_associated(authority)])) &
      error stop 'projected flux authority creation failed'
    rho64=1.0_real64
    call LCMPUT(authority,'RHO',1,4,rho64)
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    if (.not. c_associated(authority_flux)) &
      error stop 'projected type-4 FLUX creation failed'
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
    call LCMGET(seed_base,'KEYFLX',keyflx)
    call LCMGTC(seed_base,'OPTION',4,option)
    call LCMGTC(seed_base,'LINK.MACRO',12,link_macro)
    call LCMGTC(seed_base,'LINK.TRACK',12,link_track)
    call LCMGTC(seed_base,'LINK.SYSTEM',12,link_system)
    call LCMGET(system,'SPOT-LEAK1D',leakage32)
    call LCMPTC(seed,'SIGNATURE',12,signature)
    call LCMPUT(seed,'STATE-VECTOR',40,1,state_vector)
    call LCMPUT(seed,'EPS-CONVERGE',5,2,eps_converge)
    call LCMPUT(seed,'IMERGE-LEAK',NMAT,1,imerge_leak)
    call LCMPUT(seed,'KEYFLX',8,1,keyflx)
    call LCMPTC(seed,'OPTION',4,option)
    call LCMPTC(seed,'LINK.MACRO',12,link_macro)
    call LCMPTC(seed,'LINK.TRACK',12,link_track)
    call LCMPTC(seed,'LINK.SYSTEM',12,link_system)
    call LCMPUT(seed,'SPOT-LEAK1D',NGRP,2,leakage32)
  end subroutine BUILD_PROJECTED_SEED


  subroutine BUILD_SYNTHETIC_ASSEMBLED(assembled)
    type(c_ptr), intent(out) :: assembled
    integer :: ip
    real(real64) :: one64
    character(len=12) :: name, signature, state
    type(c_ptr) :: tracks, libraries, systems, fluxes, item
    type(c_ptr) :: seed, system, authority

    call LCMOP(assembled,'B2O-ASSEMB',0,1,0)
    if (.not. c_associated(assembled)) error stop 'archive creation failed'
    signature='L_ARCHIVE'
    call LCMPTC(assembled,'SIGNATURE',12,signature)
    call LCMPUT(assembled,'LISTDIM',1,1,3)
    one64=1.0_real64
    call LCMPUT(assembled,'SPOT-ITER-K',1,4,one64)
    tracks=LCMLID(assembled,'TRACK',3)
    libraries=LCMLID(assembled,'MICROLIB2',3)
    systems=LCMLID(assembled,'SYSTEM',3)
    fluxes=LCMLID(assembled,'FLUX',3)
    if (.not. all([c_associated(tracks),c_associated(libraries), &
        c_associated(systems),c_associated(fluxes)])) &
      error stop 'archive list creation failed'
    do ip=1,3
      item=LCMDIL(tracks,ip)
      if (.not. c_associated(item)) error stop 'TRACK item creation failed'
      item=LCMDIL(libraries,ip)
      if (.not. c_associated(item)) error stop 'library item creation failed'

      write(name,'(A,I2.2)') 'B2O-AY',ip
      call CLONE_OBJECT(system_base,name,system)
      call ADD_SYSTEM_AUTHORITY(system,ip)
      write(name,'(A,I2.2)') 'B2O-AS',ip
      call BUILD_PROJECTED_SEED(name,ip,system,seed)
      item=LCMDIL(fluxes,ip)
      if (.not. c_associated(item)) error stop 'FLUX item creation failed'
      call LCMEQU(seed,item)
      item=LCMDIL(systems,ip)
      if (.not. c_associated(item)) error stop 'SYSTEM item creation failed'
      call LCMEQU(system,item)
      call LCMCL(system,2)
      call LCMCL(seed,2)
    end do

    authority=LCMDID(assembled,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'root authority failed'
    call LCMPUT(authority,'RHO',1,4,one64)
    call LCMPUT(authority,'NPLANE',1,1,3)
    state='ASSEMBLED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine BUILD_SYNTHETIC_ASSEMBLED


  subroutine REQUIRE_SEALED_PLANE(seed,expected_plane)
    type(c_ptr), intent(in) :: seed
    integer, intent(in) :: expected_plane
    integer :: found_plane, ig, iu
    integer(int64) :: expected_bits, found_bits
    real(real32) :: stage32(NUNKNO)
    real(real64) :: base64, expected64, stage64(NUNKNO)
    type(c_ptr) :: authority, root_flux, authority_flux

    authority=LCMGID(seed,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'sealed authority missing'
    call LCMGET(authority,'PLANE',found_plane)
    if (found_plane /= expected_plane) error stop 'sealed plane differs'
    root_flux=LCMGID(seed,'FLUX')
    authority_flux=LCMGID(authority,'FLUX')
    if (.not. all([c_associated(root_flux), &
        c_associated(authority_flux)])) &
      error stop 'sealed FLUX payload missing'
    do ig=1,NGRP
      call LCMGDL(root_flux,ig,stage32)
      call LCMGDL(authority_flux,ig,stage64)
      do iu=1,NUNKNO
        base64=real(stage32(iu),real64)
        if (base64 < +0.0_real64) then
          expected64=base64- &
              real(expected_plane,real64)*spacing(base64)
        else
          expected64=base64+ &
              real(expected_plane,real64)*spacing(base64)
        end if
        expected_bits=transfer(expected64,0_int64)
        found_bits=transfer(stage64(iu),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'sealed seed payload is not source-selected index'
      end do
      expected_flux64(:,ig)=stage64
    end do
  end subroutine REQUIRE_SEALED_PLANE


  subroutine CALL_INGRESS(local_status,local_cutoff)
    integer, intent(out) :: local_status
    integer(int64), intent(out) :: local_cutoff

    ingress_calls=ingress_calls+1
    call B2O_RESET_PROBES()
    call SPOR64_B2B_INGRESS(NENTRY,hentry,ientry,jentry,kentry, &
        0,500,740,eps32,eps32,eps32,1,3,3,'B0  ',0,1,1,imerg,0, &
        .false.,0,.true.,370,8,8,32,1,2,1,.false.,.true., &
        SPOR64_B2B_CONT,local_status,local_cutoff)
  end subroutine CALL_INGRESS


  subroutine CLONE_OBJECT(source,name,target)
    type(c_ptr), intent(in) :: source
    character(len=*), intent(in) :: name
    type(c_ptr), intent(out) :: target

    call LCMOP(target,name,0,1,0)
    if (.not. c_associated(target)) error stop 'LCM clone target failed'
    call LCMEQU(source,target)
  end subroutine CLONE_OBJECT


  subroutine SYNC_SEED_LEAKAGE(seed,system)
    type(c_ptr), intent(in) :: seed, system
    real(real32) :: leakage32(NGRP)

    call LCMGET(system,'SPOT-LEAK1D',leakage32)
    call LCMPUT(seed,'SPOT-LEAK1D',NGRP,2,leakage32)
  end subroutine SYNC_SEED_LEAKAGE


  subroutine ADD_SEED_AUTHORITY(seed,omit_rho,include_plane)
    type(c_ptr), intent(in) :: seed
    logical, intent(in) :: omit_rho, include_plane
    integer :: ig, iu
    real(real32) :: stage32(NUNKNO)
    real(real64) :: rho64, stage64(NUNKNO)
    character(len=12) :: state
    type(c_ptr) :: root_flux, authority, authority_flux

    root_flux=LCMGID(seed,'FLUX')
    if (.not. c_associated(root_flux)) error stop 'root FLUX missing'
    authority=LCMDID(seed,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'seed authority failed'
    rho64=1.0_real64
    if (.not. omit_rho) call LCMPUT(authority,'RHO',1,4,rho64)
    if (include_plane) call LCMPUT(authority,'PLANE',1,1,1)
    authority_flux=LCMLID(authority,'FLUX',NGRP)
    if (.not. c_associated(authority_flux)) error stop 'authority FLUX failed'
    do ig=1,NGRP
      call LCMGDL(root_flux,ig,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        if (stage64(iu) < +0.0_real64) then
          stage64(iu)=stage64(iu)-spacing(stage64(iu))
        else
          stage64(iu)=stage64(iu)+spacing(stage64(iu))
        end if
      end do
      call LCMPDL(authority_flux,ig,NUNKNO,4,stage64)
      expected_flux64(:,ig)=stage64
    end do
    state='PROJECTED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine ADD_SEED_AUTHORITY


  subroutine ADD_SOURCE_AUTHORITY(source)
    type(c_ptr), intent(in) :: source
    integer :: ig, iu
    real(real32) :: stage32(NUNKNO)
    real(real64) :: rho64, stage64(NUNKNO)
    character(len=12) :: state
    type(c_ptr) :: root_outer, root_source, authority, qfiss

    root_outer=LCMGID(source,'DSOUR')
    if (.not. c_associated(root_outer)) error stop 'root DSOUR missing'
    root_source=LCMGIL(root_outer,1)
    if (.not. c_associated(root_source)) error stop 'DSOUR child missing'
    authority=LCMDID(source,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'source authority failed'
    rho64=1.0_real64
    call LCMPUT(authority,'RHO',1,4,rho64)
    call LCMPUT(authority,'PLANE',1,1,1)
    state='FROZEN-QFIS'
    call LCMPTC(authority,'STATE',12,state)
    qfiss=LCMLID(authority,'QFISS',NGRP)
    if (.not. c_associated(qfiss)) error stop 'QFISS list failed'
    do ig=1,NGRP
      call LCMGDL(root_source,ig,stage32)
      stage64=real(stage32,real64)
      do iu=1,NUNKNO
        stage64(iu)=stage64(iu)+spacing(stage64(iu))
      end do
      call LCMPDL(qfiss,ig,NUNKNO,4,stage64)
      expected_qfiss64(:,ig)=stage64
    end do
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine ADD_SOURCE_AUTHORITY


  subroutine ADD_SYSTEM_AUTHORITY(system,plane)
    type(c_ptr), intent(in) :: system
    integer, intent(in) :: plane
    real(real64) :: rho64
    character(len=12) :: state
    type(c_ptr) :: authority

    call LCMPUT(system,'SPOT-L1-SNAP',1,1,plane)
    authority=LCMDID(system,'SPOT-R64')
    if (.not. c_associated(authority)) error stop 'system authority failed'
    rho64=1.0_real64
    call LCMPUT(authority,'RHO',1,4,rho64)
    state='ASSEMBLED'
    call LCMPTC(authority,'STATE',12,state)
    call LCMPUT(authority,'EPOCH',1,1,1)
  end subroutine ADD_SYSTEM_AUTHORITY


  subroutine REQUIRE_CAPTURE_BITS()
    integer :: ig, iu
    integer(int64) :: expected_bits, found_bits, roundtrip_bits

    do ig=1,NGRP
      do iu=1,NUNKNO
        expected_bits=transfer(expected_flux64(iu,ig),0_int64)
        found_bits=transfer(captured_flux64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'core FLUX differs from type-4 authority'
        roundtrip_bits=transfer(real(real(expected_flux64(iu,ig), &
            real32),real64),0_int64)
        if (found_bits == roundtrip_bits) &
          error stop 'core FLUX lost its REAL64-only low bits'
        expected_bits=transfer(expected_qfiss64(iu,ig),0_int64)
        found_bits=transfer(captured_qfiss64(iu,ig),0_int64)
        if (found_bits /= expected_bits) &
          error stop 'core QFISS differs from type-4 authority'
        roundtrip_bits=transfer(real(real(expected_qfiss64(iu,ig), &
            real32),real64),0_int64)
        if (found_bits == roundtrip_bits) &
          error stop 'core QFISS lost its REAL64-only low bits'
      end do
    end do
  end subroutine REQUIRE_CAPTURE_BITS


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
end program TEST_B2O_CONT_BINDING_CUTOFF
