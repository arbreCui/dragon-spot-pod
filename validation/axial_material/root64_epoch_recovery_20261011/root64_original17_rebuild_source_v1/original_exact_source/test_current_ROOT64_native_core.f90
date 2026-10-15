program test_current_ROOT64_native_core
  ! NEW SOURCE: real GANLIB in-memory contract controls for the current module.
  ! Synthetic values exercise serialization, admission and output atomicity.
  ! They are not transport results, a strict native producer or old 17 controls.
  use, intrinsic :: iso_c_binding, only : c_ptr, c_associated, c_null_ptr
  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64, &
      output_unit, error_unit
  use, intrinsic :: ieee_arithmetic, only : ieee_value, ieee_quiet_nan
  use GANLIB
  use SPOR64_BOOT64, only : ROOT64_REFUSED, ROOT64_PUBLISHED, ROOT64_LOADED, &
      ROOT64_IMPORTED, SPOR64_BOOT64_PUBLISH_NATIVE, SPOR64_BOOT64_READ_NATIVE, &
      SPOR64_BOOT64_IMPORT_NATIVE, SPOR64_BOOT64_SAME_TREE
  use SPOR64_RCONTRACT, only : SPOR64_ROUTE_CONTRACT, SPOR64_RCONTRACT_LOAD
  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT, RECORD_MATCHES
  implicit none
  integer, parameter :: NG=370, NR=2, NU=3, NM=2, NS=1, NV=40
  integer, parameter :: BASE_PLANE=2, BASE_EPOCH=7, NPUB=28, NREAD=48
  real(real64), parameter :: K64=1.25_real64+2.0_real64**(-40)
  real(real32), parameter :: RADIAL=2.5e-7_real32
  real(real32), parameter :: EPS3(3)=[RADIAL,5.0e-8_real32,1.0e-5_real32]
  character(len=40), parameter :: PUB_NAMES(NPUB)=[character(len=40) :: &
      'publish_plane_zero','publish_plane_four','publish_negative_epoch', &
      'publish_terminal_369_groups','publish_terminal_nan', &
      'publish_terminal_negative_region','publish_nan_keff', &
      'publish_nonpositive_keff','publish_same32_different64_keff', &
      'publish_negative_residual','publish_nan_residual', &
      'publish_residual_at_strict_limit','publish_outer_below_two', &
      'publish_outer_above_contract','publish_inner_zero', &
      'publish_inner_above_contract','publish_inner_not_converged', &
      'publish_last_native_type2','publish_last_native_short', &
      'publish_last_native_one64_ulp','publish_last_mirror_one32_ulp', &
      'publish_existing_root_list','publish_existing_seal', &
      'publish_forbidden_legacy_seed','publish_bad_track_partition', &
      'publish_bad_system_group_count','publish_bad_macro_fission_count', &
      'publish_changed_route_tolerance']
  character(len=40), parameter :: READ_NAMES(NREAD)=[character(len=40) :: &
      'read_missing_seal','read_uncommitted_seal','read_wrong_role', &
      'read_wrong_version','read_extra_seal_record','read_missing_root', &
      'read_root_list_369_groups','read_last_root_group_absent', &
      'read_last_root_type2_disguised','read_last_root_fake_type4_words', &
      'read_last_root_one64_ulp','read_last_root_nan', &
      'read_last_root_negative_region','read_last_reference_one64_ulp', &
      'read_last_native_one64_ulp','read_last_mirror_one32_ulp', &
      'read_same32_different64_native_keff','read_keff_mirror_one32_ulp', &
      'read_seal_keff_one64_ulp','read_different_requested_plane', &
      'read_different_requested_epoch','read_changed_seal_plane', &
      'read_changed_seal_epoch','read_track_nested_one64_ulp', &
      'read_system_last_group_payload','read_material_last_group_payload', &
      'read_different_valid_route_name','read_route_tolerance_one32_ulp', &
      'read_route_extra_record','read_track_key_overlap', &
      'read_track_zero_volume','read_system_wrong_group_count', &
      'read_macro_wrong_fission_count','read_flux_wrong_option', &
      'read_flux_tolerance_one32_ulp','read_seal_key_changed', &
      'read_seal_material_changed','read_seal_volume_one64_ulp', &
      'read_seal_weight_one64_ulp','read_residual_at_strict_limit', &
      'read_changed_seal_limit','read_terminal_outer_below_two', &
      'read_forbidden_legacy_seed','read_seal_keff_type2_disguised', &
      'read_native_list_369_groups','read_track_negative_zero_changed', &
      'read_sealed_residual_nan','read_last_native_type2_disguised']
  type fixture
    type(c_ptr) :: flux=c_null_ptr, track=c_null_ptr, system=c_null_ptr
    type(c_ptr) :: material=c_null_ptr, route=c_null_ptr
    real(real64) :: image(NU,NG)
  end type fixture
  type(fixture) :: seed, published
  integer :: next_root=0, completed=0, publish_calls=0, read_calls=0, import_calls=0
  integer :: i, status
  real(real64) :: residual(3)

  if (command_argument_count()/=0) call fail('no arguments accepted')
  call make_fixture(seed)
  do i=1,3
    call positive_case(seed,i,7*i-7)
  end do
  call clone_fixture(seed,published)
  residual=real(RADIAL,real64)/4.0_real64
  call SPOR64_BOOT64_PUBLISH_NATIVE(published%flux,published%track, &
      published%system,published%material,published%route,BASE_PLANE,BASE_EPOCH, &
      published%image,K64,residual,2,1,1,status)
  publish_calls=publish_calls+1
  call insist(status==ROOT64_PUBLISHED,'baseline actual publish refused')
  do i=1,NPUB
    call publish_refusal(seed,i)
  end do
  do i=1,NREAD
    call read_import_refusal(published,i)
  end do
  call occupied_output_refusals(published)
  call coherent_rewrite_scope_control(published)
  call insist(completed==3+NPUB+NREAD+3+1,'complete case count')
  call close_fixture(published)
  call close_fixture(seed)
  write(output_unit,'(A,I0,A,I0,A,I0,A,I0,A)') &
      '{"schema":"ACTUAL_CURRENT_ROOT64_NATIVE_CORE_CONTROLS_V1",'// &
      '"control_count":',completed,',"explicit_publish_calls":',publish_calls, &
      ',"explicit_read_calls":',read_calls,',"explicit_import_calls":',import_calls, &
      ',"status":"ALL_CURRENT_CORE_ASSERTIONS_COMPLETED",'// &
      '"synthetic_fixture":true,"transport_executed":false,'// &
      '"original_seventeen_controls_qualified":false,'// &
      '"native_producer_qualified":false,"online_BOOT_qualified":false,'// &
      '"goal_complete":false}'
  flush(output_unit)

contains

  subroutine fail(message)
    character(len=*), intent(in) :: message
    write(error_unit,'(A)') 'ACTUAL ROOT64 CORE ASSERTION FAILED: '//message
    flush(error_unit)
    error stop 1
  end subroutine fail

  subroutine insist(condition,message)
    logical, intent(in) :: condition
    character(len=*), intent(in) :: message
    if (.not. condition) call fail(message)
  end subroutine insist

  subroutine open_root(root)
    type(c_ptr), intent(out) :: root
    character(len=40) :: name
    next_root=next_root+1
    write(name,'(A,I0)') 'CURRENT-ROOT64-CORE-',next_root
    root=c_null_ptr
    call LCMOP(root,trim(name),0,1,0)
    call insist(EMPTY_MEMORY_ROOT(root),'fresh actual memory root')
  end subroutine open_root

  subroutine close_fixture(f)
    type(fixture), intent(inout) :: f
    call LCMCL(f%route,2)
    call LCMCL(f%material,2)
    call LCMCL(f%system,2)
    call LCMCL(f%track,2)
    call LCMCL(f%flux,2)
    f%route=c_null_ptr; f%material=c_null_ptr; f%system=c_null_ptr
    f%track=c_null_ptr; f%flux=c_null_ptr
  end subroutine close_fixture

  subroutine clone_fixture(source,destination)
    type(fixture), intent(in) :: source
    type(fixture), intent(out) :: destination
    call open_root(destination%flux)
    call open_root(destination%track)
    call open_root(destination%system)
    call open_root(destination%material)
    call open_root(destination%route)
    call LCMEQU(source%flux,destination%flux)
    call LCMEQU(source%track,destination%track)
    call LCMEQU(source%system,destination%system)
    call LCMEQU(source%material,destination%material)
    call LCMEQU(source%route,destination%route)
    destination%image=source%image
    call assert_fixture_same(source,destination,'GANLIB fixture deep copy')
  end subroutine clone_fixture

  subroutine make_fixture(f)
    type(fixture), intent(out) :: f
    type(SPOR64_ROUTE_CONTRACT) :: contract
    type(c_ptr) :: macro, groups, item, native, mirrors, meta
    integer :: state(NV), group, row, key(NR), keycur(NS), matcod(NR)
    real(real32) :: volume(NR), eps(5), total(NM), nu_fission(NM*32)
    real(real32) :: spectrum(NM*32), diffusion(NM), metric(NU)
    real(real64) :: tag64(2)
    logical :: loaded
    call open_root(f%flux); call open_root(f%track); call open_root(f%system)
    call open_root(f%material); call open_root(f%route)
    key=[1,2]; keycur=[3]; matcod=[1,2]; volume=[1.0_real32,3.0_real32]
    call LCMPTC(f%track,'SIGNATURE',12,'L_TRACK     ')
    call LCMPTC(f%track,'TRACK-TYPE',12,'MCCG        ')
    call LCMPTC(f%track,'LINK.FTRACK',12,'TRACK_f     ')
    state=0; state(1:6)=[NR,NU,1,NM,NS,1]; state(14)=4
    call LCMPUT(f%track,'STATE-VECTOR',NV,1,state)
    call LCMPUT(f%track,'KEYFLX$ANIS',NR,1,key)
    call LCMPUT(f%track,'KEYFLX',NR,1,key)
    call LCMPUT(f%track,'KEYCUR$MCCG',NS,1,keycur)
    call LCMPUT(f%track,'MATCOD',NR,1,matcod)
    call LCMPUT(f%track,'VOLUME',NR,2,volume)
    metric=[1.0_real32,3.0_real32,1.0_real32]
    call LCMPUT(f%track,'V$MCCG',NU,2,metric)
    call LCMPUT(f%track,'NZON$MCCG',NU,1,[1,2,-1])
    meta=LCMDID(f%track,'TRACK-META')
    tag64=[1.0_real64+2.0_real64**(-40),transfer(int(z'8000000000000000',int64),0.0_real64)]
    call LCMPUT(meta,'RAW64',2,4,tag64)
    call LCMPTC(f%system,'SIGNATURE',12,'L_PIJ       ')
    call LCMPTC(f%system,'LINK.TRACK',12,'TRACK       ')
    call LCMPTC(f%system,'LINK.MACRO',12,'MICROLIB2   ')
    state=0; state(1:14)=[1,1,1,0,1,1,4,NG,NU,NM,1,0,0,0]
    call LCMPUT(f%system,'STATE-VECTOR',NV,1,state)
    groups=LCMLID(f%system,'GROUP',NG)
    do group=1,NG
      item=LCMDIL(groups,group)
      call LCMPUT(item,'GROUP-ID',1,1,group)
      call LCMPUT(item,'CORE-TAG64',1,4,real(group,real64)+2.0_real64**(-40))
    end do
    call LCMPTC(f%material,'SIGNATURE',12,'L_LIBRARY   ')
    state=0; state(1:4)=[NM,1,NG,3]
    call LCMPUT(f%material,'STATE-VECTOR',NV,1,state)
    macro=LCMDID(f%material,'MACROLIB')
    call LCMPTC(macro,'SIGNATURE',12,'L_MACROLIB  ')
    state=0; state(1:4)=[NG,NM,3,32]; state(6)=2
    call LCMPUT(macro,'STATE-VECTOR',NV,1,state)
    groups=LCMLID(macro,'GROUP',NG)
    do group=1,NG
      item=LCMDIL(groups,group)
      total=[1.0_real32+real(group,real32)/1024.0_real32,2.0_real32]
      nu_fission=0.0_real32
      nu_fission(1:NM)=[0.01_real32,0.02_real32]
      diffusion=1.0_real32/(3.0_real32*total)
      spectrum=1.0_real32/real(NG,real32)
      call LCMPUT(item,'NTOT0',NM,2,total)
      call LCMPUT(item,'NUSIGF',NM*32,2,nu_fission)
      call LCMPUT(item,'CHI',NM*32,2,spectrum)
      call LCMPUT(item,'DIFF',NM,2,diffusion)
    end do
    call LCMPTC(f%route,'SIGNATURE',12,'L_RCONTRACT ')
    call LCMPTC(f%route,'CASE-NAME',12,'CORE-FIXTURE')
    call LCMPUT(f%route,'EPS-TERMINAL',3,2,EPS3)
    call LCMPUT(f%route,'FLU-CAPS',2,1,[500,740])
    call LCMPUT(f%route,'FLU-ACCE',2,1,[3,3])
    call LCMPTC(f%route,'FLU-OPTION',4,'B0  ')
    call SPOR64_RCONTRACT_LOAD(f%route,contract,loaded)
    call insist(loaded,'genuine original RCONTRACT_LOAD')
    call insist(contract%eps_radial_bits==transfer(RADIAL,0_int32), &
        'original exact radial tolerance bits')
    call LCMPTC(f%flux,'SIGNATURE',12,'L_FLUX      ')
    state=0; state(1:18)=[NG,NU,1,0,0,2,0,3,3,1,740,500,0,0,0,0,NM,1]
    call LCMPUT(f%flux,'STATE-VECTOR',NV,1,state)
    eps=0.0_real32; eps(1:3)=RADIAL
    call LCMPUT(f%flux,'EPS-CONVERGE',5,2,eps)
    call LCMPUT(f%flux,'KEYFLX',NR,1,key)
    call LCMPTC(f%flux,'OPTION',4,'B0  ')
    call LCMPTC(f%flux,'LINK.TRACK',12,'TRACK       ')
    call LCMPTC(f%flux,'LINK.SYSTEM',12,'SYSTEM      ')
    call LCMPTC(f%flux,'LINK.MACRO',12,'MICROLIB2   ')
    call LCMPUT(f%flux,'SPOT-KEFF64',1,4,K64)
    call LCMPUT(f%flux,'K-EFFECTIVE',1,2,real(K64,real32))
    native=LCMLID(f%flux,'FLUX64',NG); mirrors=LCMLID(f%flux,'FLUX',NG)
    do group=1,NG
      do row=1,NU
        f%image(row,group)=1.0_real64+real(group,real64)/1024.0_real64+ &
            real(row,real64)/64.0_real64+2.0_real64**(-40)
      end do
      ! Surface unknown signed zero checks storage bits without region positivity.
      f%image(NU,group)=transfer(int(z'8000000000000000',int64),0.0_real64)
      call LCMPDL(native,group,NU,4,f%image(:,group))
      call LCMPDL(mirrors,group,NU,2,real(f%image(:,group),real32))
    end do
    call insist(any(transfer(f%image(1,:),0_int64,NG)/= &
        transfer(real(real(f%image(1,:),real32),real64),0_int64,NG)), &
        'fixture retains non-REAL32 low bits')
  end subroutine make_fixture

  subroutine positive_case(base,plane,epoch)
    type(fixture), intent(in) :: base
    integer, intent(in) :: plane,epoch
    type(fixture) :: f, saved
    type(c_ptr) :: out
    real(real64), allocatable :: result(:,:)
    real(real64) :: gates(3)
    integer :: ps,rs,is
    character(len=40) :: label
    call clone_fixture(base,f)
    gates=real(RADIAL,real64)/4.0_real64
    call SPOR64_BOOT64_PUBLISH_NATIVE(f%flux,f%track,f%system,f%material, &
        f%route,plane,epoch,f%image,K64,gates,2,1,1,ps)
    publish_calls=publish_calls+1
    call insist(ps==ROOT64_PUBLISHED,'actual positive publish')
    call clone_fixture(f,saved)
    call SPOR64_BOOT64_READ_NATIVE(f%flux,f%track,f%system,f%material, &
        f%route,plane,epoch,result,rs)
    read_calls=read_calls+1
    call insist(rs==ROOT64_LOADED,'actual positive read')
    call assert_flux(result,f%image,'positive 370 groups read bit image')
    call open_root(out)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%flux,f%track,f%system,f%material, &
        f%route,plane,epoch,is)
    import_calls=import_calls+1
    call insist(is==ROOT64_IMPORTED,'actual positive import')
    call insist(equal_tree(out,f%flux),'positive imported full tree raw words')
    call insist(SPOR64_BOOT64_SAME_TREE(out,f%flux),'public full-tree comparator positive')
    call assert_fixture_same(f,saved,'read/import must not mutate inputs')
    write(label,'(A,I0)') 'positive_full_370_plane_',plane
    call emit(label,'publish_read_import',ps,rs,is)
    call LCMCL(out,2); call close_fixture(saved); call close_fixture(f)
  end subroutine positive_case

  subroutine publish_refusal(base,which)
    type(fixture), intent(in) :: base
    integer, intent(in) :: which
    type(fixture) :: f,saved
    type(c_ptr) :: list,child
    real(real64) :: gates(3),keff,column(NU)
    real(real32) :: mirror(NU),eps(3)
    integer :: plane,epoch,outer,inner,converged,status,state(NV)
    call clone_fixture(base,f)
    gates=real(RADIAL,real64)/4.0_real64; keff=K64
    plane=BASE_PLANE; epoch=BASE_EPOCH; outer=2; inner=1; converged=1
    select case(which)
    case(1); plane=0
    case(2); plane=4
    case(3); epoch=-1
    case(4) ! Short shape is passed in the call below.
    case(5); f%image(2,NG)=ieee_value(0.0_real64,ieee_quiet_nan)
    case(6); f%image(2,NG)=-1.0_real64
    case(7); keff=ieee_value(0.0_real64,ieee_quiet_nan)
    case(8); keff=0.0_real64
    case(9); keff=bump64(K64)
    case(10); gates(3)=-1.0_real64
    case(11); gates(3)=ieee_value(0.0_real64,ieee_quiet_nan)
    case(12); gates(3)=real(RADIAL,real64)
    case(13); outer=1
    case(14); outer=501
    case(15); inner=0
    case(16); inner=741
    case(17); converged=0
    case(18)
      list=LCMGID(f%flux,'FLUX64')
      call LCMPDL(list,NG,NU,2,real(f%image(:,NG),real32))
    case(19)
      list=LCMGID(f%flux,'FLUX64')
      call LCMPDL(list,NG,NU-1,4,f%image(1:NU-1,NG))
    case(20)
      list=LCMGID(f%flux,'FLUX64'); column=f%image(:,NG); column(2)=bump64(column(2))
      call LCMPDL(list,NG,NU,4,column)
    case(21)
      list=LCMGID(f%flux,'FLUX'); mirror=real(f%image(:,NG),real32)
      mirror(2)=bump32(mirror(2)); call LCMPDL(list,NG,NU,2,mirror)
    case(22); child=LCMLID(f%flux,'ROOT-FLUX64',NG)
    case(23); child=LCMDID(f%flux,'ROOT64-SEAL')
    case(24); call LCMPUT(f%flux,'SPOT-R64',1,1,1)
    case(25); call LCMPUT(f%track,'KEYCUR$MCCG',NS,1,[2])
    case(26)
      call LCMGET(f%system,'STATE-VECTOR',state); state(8)=NG-1
      call LCMPUT(f%system,'STATE-VECTOR',NV,1,state)
    case(27)
      child=LCMGID(f%material,'MACROLIB'); call LCMGET(child,'STATE-VECTOR',state)
      state(4)=31; call LCMPUT(child,'STATE-VECTOR',NV,1,state)
    case(28)
      eps=EPS3; eps(1)=bump32(eps(1)); call LCMPUT(f%route,'EPS-TERMINAL',3,2,eps)
    case default; call fail('unknown publish case')
    end select
    call clone_fixture(f,saved)
    if (which==4) then
      call SPOR64_BOOT64_PUBLISH_NATIVE(f%flux,f%track,f%system,f%material, &
          f%route,plane,epoch,f%image(:,1:NG-1),keff,gates,outer,inner,converged,status)
    else
      call SPOR64_BOOT64_PUBLISH_NATIVE(f%flux,f%track,f%system,f%material, &
          f%route,plane,epoch,f%image,keff,gates,outer,inner,converged,status)
    end if
    publish_calls=publish_calls+1
    call insist(status==ROOT64_REFUSED,trim(PUB_NAMES(which))//' actual refusal')
    call assert_fixture_same(f,saved,trim(PUB_NAMES(which))//' whole input atomicity')
    call emit(PUB_NAMES(which),'publish_only',status,0,0)
    call close_fixture(saved); call close_fixture(f)
  end subroutine publish_refusal

  subroutine read_import_refusal(base,which)
    type(fixture), intent(in) :: base
    integer, intent(in) :: which
    type(fixture) :: f,saved
    type(c_ptr) :: seal,list,child,groups,out
    real(real64), allocatable :: result(:,:)
    real(real64) :: column(NU),tag(2),values(NR),gates(3),scalar
    real(real32) :: mirror(NU),eps(3),eps5(5),total(NM)
    integer :: plane,epoch,rs,is,group,state(NV),raw(2*NU)
    call clone_fixture(base,f)
    plane=BASE_PLANE; epoch=BASE_EPOCH
    seal=LCMGID(f%flux,'ROOT64-SEAL')
    select case(which)
    case(1); call LCMDEL(f%flux,'ROOT64-SEAL')
    case(2); call LCMPTC(seal,'STATE',12,'UNCOMMITTED ')
    case(3); call LCMPTC(seal,'ROLE',12,'PROJECTED   ')
    case(4); call LCMPUT(seal,'VERSION',1,1,2)
    case(5); call LCMPUT(seal,'EXTRA',1,1,1)
    case(6); call LCMDEL(f%flux,'ROOT-FLUX64')
    case(7,8)
      call LCMDEL(f%flux,'ROOT-FLUX64')
      if (which==7) then
        list=LCMLID(f%flux,'ROOT-FLUX64',NG-1)
      else
        list=LCMLID(f%flux,'ROOT-FLUX64',NG)
      end if
      do group=1,NG-1
        call LCMPDL(list,group,NU,4,f%image(:,group))
      end do
    case(9)
      list=LCMGID(f%flux,'ROOT-FLUX64')
      call LCMPDL(list,NG,NU,2,real(f%image(:,NG),real32))
    case(10)
      ! Type code 4 with fabricated raw REAL32 word pairs is still not authority.
      list=LCMGID(f%flux,'ROOT-FLUX64'); raw=0
      raw(1:2*NU:2)=transfer(real(f%image(:,NG),real32),0_int32,NU)
      column=transfer(raw,column)
      call insist(.not. same64(column,f%image(:,NG)),'type4 disguise actually differs')
      call LCMPDL(list,NG,NU,4,column)
    case(11,12,13)
      list=LCMGID(f%flux,'ROOT-FLUX64'); column=f%image(:,NG)
      if (which==11) column(2)=bump64(column(2))
      if (which==12) column(2)=ieee_value(0.0_real64,ieee_quiet_nan)
      if (which==13) column(2)=-1.0_real64
      call LCMPDL(list,NG,NU,4,column)
    case(14)
      list=LCMGID(seal,'ROOT-REF64'); column=f%image(:,NG); column(2)=bump64(column(2))
      call LCMPDL(list,NG,NU,4,column)
    case(15)
      list=LCMGID(f%flux,'FLUX64'); column=f%image(:,NG); column(2)=bump64(column(2))
      call LCMPDL(list,NG,NU,4,column)
    case(16)
      list=LCMGID(f%flux,'FLUX'); mirror=real(f%image(:,NG),real32)
      mirror(2)=bump32(mirror(2)); call LCMPDL(list,NG,NU,2,mirror)
    case(17); call LCMPUT(f%flux,'SPOT-KEFF64',1,4,bump64(K64))
    case(18); call LCMPUT(f%flux,'K-EFFECTIVE',1,2,bump32(real(K64,real32)))
    case(19); call LCMPUT(seal,'KEFF64',1,4,bump64(K64))
    case(20); plane=1
    case(21); epoch=BASE_EPOCH+1
    case(22); call LCMPUT(seal,'PLANE',1,1,1)
    case(23); call LCMPUT(seal,'EPOCH',1,1,BASE_EPOCH+1)
    case(24,46)
      child=LCMGID(f%track,'TRACK-META'); call LCMGET(child,'RAW64',tag)
      if (which==24) tag(1)=bump64(tag(1))
      if (which==46) tag(2)=0.0_real64
      call LCMPUT(child,'RAW64',2,4,tag)
      call insist(.not. SPOR64_BOOT64_SAME_TREE(f%track,LCMGID(seal,'TRACK')), &
          'public comparator must reject changed context raw bits')
    case(25)
      groups=LCMGID(f%system,'GROUP'); child=LCMGIL(groups,NG)
      call LCMGET(child,'CORE-TAG64',scalar)
      call LCMPUT(child,'CORE-TAG64',1,4,bump64(scalar))
    case(26)
      child=LCMGID(f%material,'MACROLIB'); groups=LCMGID(child,'GROUP')
      child=LCMGIL(groups,NG); call LCMGET(child,'NTOT0',total)
      total(2)=bump32(total(2)); call LCMPUT(child,'NTOT0',NM,2,total)
    case(27); call LCMPTC(f%route,'CASE-NAME',12,'OTHER-ROUTE ')
    case(28)
      eps=EPS3; eps(1)=bump32(eps(1)); call LCMPUT(f%route,'EPS-TERMINAL',3,2,eps)
    case(29); call LCMPUT(f%route,'EXTRA',1,1,1)
    case(30); call LCMPUT(f%track,'KEYCUR$MCCG',NS,1,[2])
    case(31); call LCMPUT(f%track,'VOLUME',NR,2,[1.0_real32,0.0_real32])
    case(32)
      call LCMGET(f%system,'STATE-VECTOR',state); state(8)=NG-1
      call LCMPUT(f%system,'STATE-VECTOR',NV,1,state)
    case(33)
      child=LCMGID(f%material,'MACROLIB'); call LCMGET(child,'STATE-VECTOR',state)
      state(4)=31; call LCMPUT(child,'STATE-VECTOR',NV,1,state)
    case(34); call LCMPTC(f%flux,'OPTION',4,'K   ')
    case(35)
      call LCMGET(f%flux,'EPS-CONVERGE',eps5); eps5(3)=bump32(eps5(3))
      call LCMPUT(f%flux,'EPS-CONVERGE',5,2,eps5)
    case(36); call LCMPUT(seal,'KEYFLX',NR,1,[2,1])
    case(37); call LCMPUT(seal,'MATCOD',NR,1,[2,1])
    case(38)
      call LCMGET(seal,'VOLUME64',values); values(2)=bump64(values(2))
      call LCMPUT(seal,'VOLUME64',NR,4,values)
    case(39)
      call LCMGET(seal,'WEIGHT64',values); values(2)=bump64(values(2))
      call LCMPUT(seal,'WEIGHT64',NR,4,values)
    case(40)
      call LCMGET(seal,'GATE64',gates); gates(3)=real(RADIAL,real64)
      call LCMPUT(seal,'GATE64',3,4,gates)
    case(41)
      call LCMGET(seal,'LIMIT64',gates); gates(3)=bump64(gates(3))
      call LCMPUT(seal,'LIMIT64',3,4,gates)
    case(42); call LCMPUT(seal,'TERM-INT',3,1,[1,1,1])
    case(43); call LCMPUT(f%flux,'SPOT-R64',1,1,1)
    case(44); call LCMPUT(seal,'KEFF64',1,2,real(K64,real32))
    case(45)
      call LCMDEL(f%flux,'FLUX64'); list=LCMLID(f%flux,'FLUX64',NG-1)
      do group=1,NG-1
        call LCMPDL(list,group,NU,4,f%image(:,group))
      end do
    case(47)
      call LCMGET(seal,'GATE64',gates); gates(3)=ieee_value(0.0_real64,ieee_quiet_nan)
      call LCMPUT(seal,'GATE64',3,4,gates)
    case(48)
      list=LCMGID(f%flux,'FLUX64')
      call LCMPDL(list,NG,NU,2,real(f%image(:,NG),real32))
    case default; call fail('unknown read case')
    end select
    call clone_fixture(f,saved)
    ! INTENT(OUT) may deallocate an old allocation; rejection must not commit a new one.
    allocate(result(1,1)); result=-123.0_real64
    call SPOR64_BOOT64_READ_NATIVE(f%flux,f%track,f%system,f%material,f%route, &
        plane,epoch,result,rs)
    read_calls=read_calls+1
    call insist(rs==ROOT64_REFUSED,trim(READ_NAMES(which))//' actual read refusal')
    call insist(.not. allocated(result),trim(READ_NAMES(which))//' read no partial allocation')
    call open_root(out)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%flux,f%track,f%system,f%material, &
        f%route,plane,epoch,is)
    import_calls=import_calls+1
    call insist(is==ROOT64_REFUSED,trim(READ_NAMES(which))//' actual import refusal')
    call insist(EMPTY_MEMORY_ROOT(out),trim(READ_NAMES(which))//' import output stays empty')
    call assert_fixture_same(f,saved,trim(READ_NAMES(which))//' inputs stay byte exact')
    call emit(READ_NAMES(which),'read_import',ROOT64_PUBLISHED,rs,is)
    call LCMCL(out,2); call close_fixture(saved); call close_fixture(f)
  end subroutine read_import_refusal

  subroutine occupied_output_refusals(base)
    type(fixture), intent(in) :: base
    type(fixture) :: f,saved
    type(c_ptr) :: out,copy,parent
    integer :: status
    call clone_fixture(base,f); call clone_fixture(f,saved)
    call open_root(out); call LCMPUT(out,'SENTINEL',2,4,[3.0_real64,-0.0_real64])
    call open_root(copy); call LCMEQU(out,copy)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%flux,f%track,f%system,f%material, &
        f%route,BASE_PLANE,BASE_EPOCH,status)
    import_calls=import_calls+1
    call insist(status==ROOT64_REFUSED,'occupied output refusal')
    call insist(equal_tree(out,copy),'occupied output preserved exactly')
    call assert_fixture_same(f,saved,'occupied output input atomicity')
    call emit('import_occupied_output','import_only',ROOT64_PUBLISHED,0,status)
    call LCMCL(copy,2); call LCMCL(out,2)
    call SPOR64_BOOT64_IMPORT_NATIVE(f%flux,f%flux,f%track,f%system,f%material, &
        f%route,BASE_PLANE,BASE_EPOCH,status)
    import_calls=import_calls+1
    call insist(status==ROOT64_REFUSED,'aliased flux output refusal')
    call assert_fixture_same(f,saved,'aliased output full input atomicity')
    call emit('import_output_aliases_flux','import_only',ROOT64_PUBLISHED,0,status)
    call open_root(parent); out=LCMDID(parent,'EMPTY-CHILD')
    call open_root(copy); call LCMEQU(parent,copy)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%flux,f%track,f%system,f%material, &
        f%route,BASE_PLANE,BASE_EPOCH,status)
    import_calls=import_calls+1
    call insist(status==ROOT64_REFUSED,'empty daughter is not fresh memory root')
    call insist(equal_tree(parent,copy),'daughter and parent preserved on refusal')
    call assert_fixture_same(f,saved,'daughter output input atomicity')
    call emit('import_empty_daughter_not_root','import_only',ROOT64_PUBLISHED,0,status)
    call LCMCL(copy,2); call LCMCL(parent,2)
    call close_fixture(saved); call close_fixture(f)
  end subroutine occupied_output_refusals

  subroutine coherent_rewrite_scope_control(base)
    type(fixture), intent(in) :: base
    type(fixture) :: f,saved
    type(c_ptr) :: list,seal,out
    real(real64), allocatable :: result(:,:)
    integer :: rs,is
    call clone_fixture(base,f)
    f%image(2,NG)=bump64(f%image(2,NG))
    list=LCMGID(f%flux,'ROOT-FLUX64'); call LCMPDL(list,NG,NU,4,f%image(:,NG))
    list=LCMGID(f%flux,'FLUX64'); call LCMPDL(list,NG,NU,4,f%image(:,NG))
    list=LCMGID(f%flux,'FLUX'); call LCMPDL(list,NG,NU,2,real(f%image(:,NG),real32))
    seal=LCMGID(f%flux,'ROOT64-SEAL'); list=LCMGID(seal,'ROOT-REF64')
    call LCMPDL(list,NG,NU,4,f%image(:,NG))
    call clone_fixture(f,saved)
    call SPOR64_BOOT64_READ_NATIVE(f%flux,f%track,f%system,f%material,f%route, &
        BASE_PLANE,BASE_EPOCH,result,rs)
    read_calls=read_calls+1
    call insist(rs==ROOT64_LOADED,'coherent internal rewrite requires independent host SHA')
    call assert_flux(result,f%image,'coherent rewritten image exact')
    call open_root(out)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%flux,f%track,f%system,f%material, &
        f%route,BASE_PLANE,BASE_EPOCH,is)
    import_calls=import_calls+1
    call insist(is==ROOT64_IMPORTED,'coherent rewrite scope actual import')
    call insist(equal_tree(out,f%flux),'coherent scope imported actual full tree')
    call assert_fixture_same(f,saved,'coherent scope inputs unchanged')
    call emit('scope_coherent_rewrite_needs_host_SHA','expected_core_acceptance', &
        ROOT64_PUBLISHED,rs,is)
    call LCMCL(out,2); call close_fixture(saved); call close_fixture(f)
  end subroutine coherent_rewrite_scope_control

  subroutine assert_flux(actual,expected,message)
    real(real64), allocatable, intent(in) :: actual(:,:)
    real(real64), intent(in) :: expected(NU,NG)
    character(len=*), intent(in) :: message
    integer :: group
    call insist(allocated(actual),message//' allocation')
    call insist(all(shape(actual)==[NU,NG]),message//' shape')
    do group=1,NG
      call insist(same64(actual(:,group),expected(:,group)),message//' all raw words')
    end do
  end subroutine assert_flux

  logical function same64(left,right)
    real(real64), intent(in) :: left(:),right(:)
    same64=.false.
    if (size(left)/=size(right)) return
    same64=all(transfer(left,0_int64,size(left))==transfer(right,0_int64,size(right)))
  end function same64

  real(real64) function bump64(value)
    real(real64), intent(in) :: value
    bump64=transfer(transfer(value,0_int64)+1_int64,0.0_real64)
  end function bump64

  real(real32) function bump32(value)
    real(real32), intent(in) :: value
    bump32=transfer(transfer(value,0_int32)+1_int32,0.0_real32)
  end function bump32

  subroutine emit(name,phase,ps,rs,is)
    character(len=*), intent(in) :: name,phase
    integer, intent(in) :: ps,rs,is
    completed=completed+1
    write(output_unit,'(A,I0,A,I0,A,I0,A)') '{"case":"'//trim(name)// &
        '","phase":"'//trim(phase)//'","publish_status":',ps, &
        ',"read_status":',rs,',"import_status":',is, &
        ',"all_actual_assertions_completed":true}'
    flush(output_unit)
  end subroutine emit

  subroutine assert_fixture_same(left,right,message)
    type(fixture), intent(in) :: left,right
    character(len=*), intent(in) :: message
    call insist(equal_tree(left%flux,right%flux),message//' FLUX')
    call insist(equal_tree(left%track,right%track),message//' TRACK')
    call insist(equal_tree(left%system,right%system),message//' SYSTEM')
    call insist(equal_tree(left%material,right%material),message//' MATERIAL')
    call insist(equal_tree(left%route,right%route),message//' RCONTRACT')
  end subroutine assert_fixture_same

  ! Independent assertion oracle: compares actual GANLIB names/types/extents and
  ! every raw word. It does not call the admission module's tree comparator.
  logical function equal_tree(left,right)
    type(c_ptr), intent(in) :: left,right
    integer :: visited
    visited=0
    equal_tree=compare_node(left,right,0,visited)
  end function equal_tree

  recursive logical function compare_node(left,right,depth,visited) result(equal)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: depth
    integer, intent(inout) :: visited
    character(len=72) :: filename
    character(len=12) :: object,name,first,other
    integer :: extent1,extent2,length1,length2,type1,type2,count1,count2,index
    logical :: empty1,empty2,medium
    type(c_ptr) :: child1,child2
    equal=.false.
    if (depth>64 .or. .not. c_associated(left) .or. .not. c_associated(right)) return
    call LCMINF(left,filename,object,empty1,extent1,medium)
    call LCMINF(right,filename,object,empty2,extent2,medium)
    if (extent1/=extent2 .or. (empty1 .neqv. empty2)) return
    if (extent1>=0) then
      do index=1,extent1
        visited=visited+1
        if (visited>2000000) return
        call LCMLEL(left,index,length1,type1); call LCMLEL(right,index,length2,type2)
        if (length1/=length2 .or. type1/=type2) return
        if (type1==99 .and. length1==0) cycle
        if (type1==0 .or. type1==10) then
          child1=LCMGIL(left,index); child2=LCMGIL(right,index)
          if (.not. compare_node(child1,child2,depth+1,visited)) return
        else
          if (.not. compare_words(left,right,' ',index,length1,type1)) return
        end if
      end do
      equal=.true.; return
    end if
    if (extent1/=-1) return
    if (empty1) then
      equal=.true.; return
    end if
    name=' '; call LCMNXT(left,name); first=name; count1=0
    do
      count1=count1+1; visited=visited+1
      if (visited>2000000 .or. name==' ') return
      call LCMLEN(left,name,length1,type1); call LCMLEN(right,name,length2,type2)
      if (length1/=length2 .or. type1/=type2) return
      if (type1==0 .or. type1==10) then
        child1=LCMGID(left,name); child2=LCMGID(right,name)
        if (.not. compare_node(child1,child2,depth+1,visited)) return
      else
        if (.not. compare_words(left,right,name,0,length1,type1)) return
      end if
      call LCMNXT(left,name)
      if (name==first) exit
    end do
    other=' '; call LCMNXT(right,other); first=other; count2=0
    do
      count2=count2+1
      if (count2>2000000 .or. other==' ') return
      call LCMNXT(right,other)
      if (other==first) exit
    end do
    equal=count1==count2
  end function compare_node

  logical function compare_words(left,right,name,index,length,type_code)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: index,length,type_code
    integer, allocatable :: words1(:),words2(:)
    integer :: nwords,allocation_status
    compare_words=.false.
    if (length<=0 .or. type_code<1 .or. type_code>6) return
    if (length>8388608) return
    nwords=length
    if (type_code==4 .or. type_code==6) nwords=2*length
    allocate(words1(nwords),words2(nwords),stat=allocation_status)
    if (allocation_status/=0) return
    if (index==0) then
      call LCMGET(left,name,words1); call LCMGET(right,name,words2)
    else
      call LCMGDL(left,index,words1); call LCMGDL(right,index,words2)
    end if
    compare_words=all(words1==words2)
  end function compare_words

end program test_current_ROOT64_native_core
