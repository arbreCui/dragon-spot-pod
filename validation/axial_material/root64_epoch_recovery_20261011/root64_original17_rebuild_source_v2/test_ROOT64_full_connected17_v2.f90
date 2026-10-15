program test_ROOT64_full_connected17_v2
  ! NEW SOURCE: all seventeen connected controls on current complete modules.
  ! Old /tmp seventeen fixture bytes were lost; no old PASS is inherited.
  ! Synthetic protocol values are never a genuine solver or physics result.
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
  use SPOR64_BOOT_CANONICAL64_V2, only: SPOR64_BOOT_CANONICAL64_WRITE
  use SPOR64_BOOT_CONTEXT64_V2, only: SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK, &
      SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOT_PUBLISH64, only: SPOR64_BOOT_GLOBAL_PUBLISH, &
      SPOR64_BOOT_GLOBAL_PUBLISHED
  use SPOR64_BOOT_PROJECT64, only: SPOR64_BOOT_PROJECT_ARCHIVE, &
      SPOR64_BOOT_PROJECT_COMMITTED
  use SPOR64_BOOTQ64_V2, only: SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_READ, &
      SPOR64_BOOTQ64_COMMITTED,SPOR64_BOOTQ64_LOADED,SPOR64_BOOTQ64_PREFLIGHT_FAILED
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
  integer, parameter :: AX_NR=6,AX_NU=14,NP=3,CONNECTED_RANK=1
  real(real32), parameter :: CONNECT_EPS3(3)=[2.5e-7_real32,5.0e-8_real32,2.5e-8_real32]
  character(len=40), parameter :: CONNECTED_CASES(17)=[character(len=40) :: &
      'positive','global_wrong_scope','missing_producer_seal', &
      'root_flux32_disguised','wrong_root_mirror','missing_global64', &
      'bad_seed_epoch','fabricated_projected','uncommitted_source', &
      'wrong_source_epoch','wrong_source_dimensions','mutated_macro', &
      'mutated_track','mutated_system','different_route','qfiss32_disguised', &
      'coherent_source_tamper']
  type connected_fixture
    type(fixture) :: radial
    type(c_ptr) :: ax=c_null_ptr,axtrack=c_null_ptr,axsystem=c_null_ptr
    type(c_ptr) :: axmacro=c_null_ptr,archive=c_null_ptr,global=c_null_ptr
    type(c_ptr) :: projected=c_null_ptr,macros(NP)=c_null_ptr,sources(NP)=c_null_ptr
    real(real64) :: ax_image(AX_NU,NG),ax_source(AX_NU,NG)
  end type connected_fixture
  type(connected_fixture) :: connection
  character(len=40) :: selected_case,phase
  integer :: selected_index,narg,actual_native_read,actual_q_read
  integer :: actual_global_checks=0,actual_project_checks=0
  integer :: actual_q_build_calls=0,actual_q_read_calls=0
  integer :: actual_archive_native_read_calls=0,actual_archive_native_gate_calls=0
  integer :: actual_archive_native_last_status=0
  integer :: actual_connected_q_build_calls=0,actual_connected_q_read_calls=0
  logical :: internal_refused,coherent_rewrite
  type(fixture) :: seed, published
  integer :: next_root=0, completed=0, publish_calls=0, read_calls=0, import_calls=0
  integer :: i, status
  real(real64) :: residual(3)

  narg=command_argument_count()
  call insist(narg==1.or.narg==2,'one case and optional coherent phase')
  call get_command_argument(1,selected_case)
  selected_index=0
  do i=1,size(CONNECTED_CASES)
    if(selected_case==CONNECTED_CASES(i)) selected_index=i
  enddo
  call insist(selected_index>0,'one exact originally declared case name')
  phase='single'
  if(narg==2) then
    call get_command_argument(2,phase)
    call insist(selected_index==17,'phase only allowed for coherent external binding control')
    call insist(phase=='prepare'.or.phase=='rewrite','exact prepare or rewrite phase')
  else
    call insist(selected_index/=17,'coherent case requires external host phases')
  endif
  coherent_rewrite=phase=='rewrite'
  call build_connected(connection,coherent_rewrite)
  internal_refused=.false.;actual_native_read=0;actual_q_read=0
  call run_connected_case(connection,selected_index,phase)
  call close_connected(connection)
  write(output_unit,'(A)') &
      '{"case":"'//trim(selected_case)//'","phase":"'//trim(phase)// &
      '","schema":"CONNECTED_CURRENT_ROOT64_SEVENTEEN_COMPONENT_ASSERTIONS_V2",'// &
      '"all_actual_assertions_completed":true,"synthetic_fixture":true,'// &
      '"genuine_producer_qualified":false,"solver_executed":false,'// &
      '"physics_qualified":false,"old_seventeen_PASS_inherited":false}'
  write(output_unit,'(A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A)') &
      '{"case":"'//trim(selected_case)//'","phase":"'//trim(phase)// &
      '","actual_native_read_status":',actual_native_read, &
      ',"actual_q_read_status":',actual_q_read, &
      ',"actual_global_checks":',actual_global_checks, &
      ',"actual_project_checks":',actual_project_checks, &
      ',"explicit_q_build_calls":',actual_q_build_calls, &
      ',"explicit_q_read_calls":',actual_q_read_calls, &
      ',"explicit_native_publish_calls":',publish_calls, &
      ',"actual_archive_native_read_calls":',actual_archive_native_read_calls, &
      ',"actual_archive_native_gate_calls":',actual_archive_native_gate_calls, &
      ',"actual_archive_native_last_status":',actual_archive_native_last_status, &
      ',"actual_connected_q_build_calls":',actual_connected_q_build_calls, &
      ',"actual_connected_q_read_calls":',actual_connected_q_read_calls,'}' 
  flush(output_unit)

contains

  subroutine build_connected(f,rewrite)
    type(connected_fixture), intent(out) :: f
    logical, intent(in) :: rewrite
    type(c_ptr) :: macro,list,item,child,tracks,libraries,fluxes,systems,native,mirrors,sources64,sources32
    type(c_ptr) :: seed,seedtrack,seedsystem,seedmaterial
    integer :: sv(NV),mccg(NV),g,p,row,floor,region,qstat,ps
    real(real32) :: eps(5),nu(NM*32)
    real(real64) :: gates(3)
    logical :: ok

    call make_fixture(f%radial)
    ! Upgrade the complete retained native fixture with the exact current Q
    ! context records; the old factory is kept byte-identical in this Source.
    call LCMPUT(f%radial%route,'EPS-TERMINAL',3,2,CONNECT_EPS3)
    call LCMGET(f%radial%track,'STATE-VECTOR',sv)
    sv(16)=2;sv(22)=1
    call LCMPUT(f%radial%track,'STATE-VECTOR',NV,1,sv)
    mccg=0
    mccg(1:20)=[-1,4,10,0,1,1,80,0,0,4,0,0,20,1,1,1,0,0,1,1]
    call LCMPUT(f%radial%track,'MCCG-STATE',NV,1,mccg)
    call LCMPUT(f%radial%track,'MCU$MCCG',1,1,[1])
    call LCMPUT(f%radial%track,'REAL-PARAM',4,2,[CONNECT_EPS3(3),0.0_real32,0.0_real32,0.0_real32])
    macro=LCMGID(f%radial%material,'MACROLIB')
    sv=0;sv(1:7)=[NG,NM,3,32,18,2,6]
    call LCMPUT(macro,'STATE-VECTOR',NV,1,sv)
    list=LCMGID(macro,'GROUP')
    do g=1,NG
      item=LCMGIL(list,g)
      do row=1,NM*32
        nu(row)=real(row,real32)/65536.0_real32
      enddo
      call LCMPUT(item,'NUSIGF',NM*32,2,nu)
    enddo
    if(rewrite) then
      f%radial%image(1,NG)=bump64(f%radial%image(1,NG))
      list=LCMGID(f%radial%flux,'FLUX64')
      call LCMPDL(list,NG,NU,4,f%radial%image(:,NG))
      list=LCMGID(f%radial%flux,'FLUX')
      call LCMPDL(list,NG,NU,2,real(f%radial%image(:,NG),real32))
    endif

    call open_root(f%ax);call open_root(f%axtrack);call open_root(f%axsystem)
    call open_root(f%axmacro);call open_root(f%archive);call open_root(f%global)
    call open_root(f%projected)
    call LCMEQU(macro,f%axmacro)
    call LCMPTC(f%axtrack,'SIGNATURE',12,'L_TRACK     ')
    call LCMPTC(f%axtrack,'TRACK-TYPE',12,'SPOT        ')
    sv=0;sv(1)=AX_NR;sv(2)=AX_NU;sv(6)=NR;sv(7)=NP;sv(8)=NP;sv(11)=AX_NR;sv(12)=8
    call LCMPUT(f%axtrack,'STATE-VECTOR',NV,1,sv)
    call LCMPUT(f%axtrack,'KEYFLX',AX_NR,1,[1,2,3,4,5,6])
    call LCMPUT(f%axtrack,'MATCOD',AX_NR,1,[1,1,1,2,2,2])
    call LCMPUT(f%axtrack,'MAT1D',NP,1,[1,2,3])
    call LCMPUT(f%axtrack,'AREA2D',NR,2,[1.0_real32,3.0_real32])
    call LCMPUT(f%axtrack,'VOL1D',NP,2,[1.0_real32,2.0_real32,4.0_real32])
    call LCMPUT(f%axtrack,'VOLUME',AX_NR,2, &
        [1.0_real32,2.0_real32,4.0_real32,3.0_real32,6.0_real32,12.0_real32])
    child=LCMDID(f%axtrack,'TRACK-META')
    call LCMPUT(child,'RAW64',2,4, &
        [1.0_real64+2.0_real64**(-40),transfer(int(z'8000000000000000',int64),0.0_real64)])
    call LCMPTC(f%axsystem,'SIGNATURE',12,'L_PIJ       ')
    sv=0;sv(8)=NG;sv(9)=AX_NU
    call LCMPUT(f%axsystem,'STATE-VECTOR',NV,1,sv)
    call LCMPUT(f%axsystem,'SPOT-FIXB',1,1,1)
    call LCMPTC(f%axsystem,'SPOT-BTYPE',12,'POD-FIXED   ')
    list=LCMLID(f%axsystem,'GROUP',NG)
    do g=1,NG
      item=LCMDIL(list,g)
      call LCMPUT(item,'POD-NMODE',1,1,CONNECTED_RANK)
      call LCMPUT(item,'NREG2D',1,1,NR)
      call LCMPUT(item,'NSNAP',1,1,NP)
      call LCMPUT(item,'POD-BASIS',NR,2,[1.0_real32,1.0_real32])
      call LCMPUT(item,'VOL2D',NR,2,[1.0_real32,3.0_real32])
      call LCMPUT(item,'CORE-TAG64',1,4,real(g,real64)+2.0_real64**(-40))
    enddo
    call LCMPTC(f%archive,'SIGNATURE',12,'L_ARCHIVE   ')
    call LCMPUT(f%archive,'LISTDIM',1,1,NP)
    tracks=LCMLID(f%archive,'TRACK',NP)
    libraries=LCMLID(f%archive,'MICROLIB2',NP)
    fluxes=LCMLID(f%archive,'FLUX',NP)
    systems=LCMLID(f%archive,'SYSTEM',NP)
    gates=real(CONNECT_EPS3(1),real64)/4.0_real64
    do p=1,NP
      seedtrack=LCMDIL(tracks,p);call LCMEQU(f%radial%track,seedtrack)
      seedmaterial=LCMDIL(libraries,p);call LCMEQU(f%radial%material,seedmaterial)
      seedsystem=LCMDIL(systems,p);call LCMEQU(f%radial%system,seedsystem)
      seed=LCMDIL(fluxes,p);call LCMEQU(f%radial%flux,seed)
      ! Each actual consumed leaf receives its own plane-p/e0 seal. Never
      ! copy one plane's already-published identity to the other planes.
      call SPOR64_BOOT64_PUBLISH_NATIVE(seed,seedtrack,seedsystem,seedmaterial, &
          f%radial%route,p,0,f%radial%image,K64,gates,2,1,1,ps)
      publish_calls=publish_calls+1
      call insist(ps==ROOT64_PUBLISHED,'actual consumed archive plane Native PUBLISH')
    enddo

    call LCMPTC(f%ax,'SIGNATURE',12,'L_FLUX      ')
    sv=0;sv(1:3)=[NG,AX_NU,1];sv(6)=3;sv(7)=3;sv(8)=3;sv(9)=0
    sv(11)=740;sv(12)=500;sv(17)=NM;sv(18)=1
    call LCMPUT(f%ax,'STATE-VECTOR',NV,1,sv)
    eps=0.0_real32;eps(1:3)=CONNECT_EPS3(2)
    call LCMPUT(f%ax,'EPS-CONVERGE',5,2,eps)
    call LCMPTC(f%ax,'OPTION',4,'B1  ')
    call LCMPUT(f%ax,'SPOT-KEFF64',1,4,K64)
    call LCMPUT(f%ax,'K-EFFECTIVE',1,2,real(K64,real32))
    native=LCMLID(f%ax,'FLUX64',NG);mirrors=LCMLID(f%ax,'FLUX',NG)
    sources64=LCMLID(f%ax,'SOUR64',NG);sources32=LCMLID(f%ax,'SOUR',NG)
    do g=1,NG
      f%ax_image(:,g)=transfer(int(z'8000000000000000',int64),0.0_real64)
      do region=1,NR
        do floor=1,NP
          row=(region-1)*NP+floor
          f%ax_image(row,g)=1.0_real64+real(g,real64)/1024.0_real64+ &
              real(region,real64)/64.0_real64+real(floor,real64)/128.0_real64+2.0_real64**(-40)
        enddo
      enddo
      if(rewrite.and.g==NG) f%ax_image(1,g)=f%ax_image(1,g)+0.03125_real64
      do row=1,AX_NU
        f%ax_source(row,g)=real(row+g,real64)/8192.0_real64+2.0_real64**(-41)
      enddo
      call LCMPDL(native,g,AX_NU,4,f%ax_image(:,g))
      call LCMPDL(mirrors,g,AX_NU,2,real(f%ax_image(:,g),real32))
      call LCMPDL(sources64,g,AX_NU,4,f%ax_source(:,g))
      call LCMPDL(sources32,g,AX_NU,2,real(f%ax_source(:,g),real32))
    enddo
    call SPOR64_BOOT_CANONICAL64_WRITE(f%ax,f%axtrack,f%axsystem,f%axmacro,ok)
    call insist(ok,'actual full CANONICAL64 WRITE on all370 synthetic native fields')
    gates=real(CONNECT_EPS3(2),real64)/4.0_real64
    call archive_native_admission(f,ok)
    call insist(ok,'owning Native admission before actual GLOBAL publication')
    call SPOR64_BOOT_GLOBAL_PUBLISH(f%global,f%ax,f%axtrack,f%axsystem,f%axmacro, &
        f%archive,f%radial%route,f%ax_image,f%ax_source,K64,gates,[2,1],1,.true.,ps)
    call insist(ps==SPOR64_BOOT_GLOBAL_PUBLISHED,'actual full GLOBAL publisher')
    call archive_native_admission(f,ok)
    call insist(ok,'owning Native admission before actual PROJECT publication')
    call SPOR64_BOOT_PROJECT_ARCHIVE(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,CONNECTED_RANK,ps)
    call insist(ps==SPOR64_BOOT_PROJECT_COMMITTED,'actual full PROJECTED-BOOT/e0 publisher')
    do p=1,NP
      call open_root(f%macros(p));call open_root(f%sources(p))
      call connected_q_build(f,p,f%macros(p),f%sources(p),qstat)
      call insist(qstat==SPOR64_BOOTQ64_COMMITTED,'actual all370x32 QBUILD plane')
    enddo
    gates=real(CONNECT_EPS3(1),real64)/4.0_real64
    call SPOR64_BOOT64_PUBLISH_NATIVE(f%radial%flux,f%radial%track,f%radial%system, &
        f%radial%material,f%radial%route,1,0,f%radial%image,K64,gates,2,1,1,ps)
    publish_calls=publish_calls+1
    call insist(ps==ROOT64_PUBLISHED,'actual current Native seal PUBLISH, protocol only')
    call assert_connected(f)
  end subroutine build_connected

  subroutine assert_connected(f)
    type(connected_fixture), intent(in) :: f
    type(SPOR64_ROUTE_CONTRACT) :: contract
    type(c_ptr) :: out
    real(real64), allocatable :: q(:,:),native(:,:)
    real(real64) :: rho
    integer :: p,rs,is
    logical :: ok
    call archive_native_admission(f,ok)
    call insist(ok,'owning complete Native archive admission on every readback')
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,contract,ok)
    actual_global_checks=actual_global_checks+1
    call insist(ok,'actual GLOBAL full independent input check')
    call SPOR64_BOOT_CONTEXT64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,contract,ok)
    actual_project_checks=actual_project_checks+1
    call insist(ok,'actual PROJECTED full scalar/nonscalar/canonical/context check')
    do p=1,NP
      call read_q(f,p,q,rho,rs)
      call insist(rs==SPOR64_BOOTQ64_LOADED,'actual QREAD recomputation on full source/macros')
      call insist(allocated(q),'actual QREAD typed array exists')
      call insist(all(shape(q)==[NU,NG]),'actual QREAD full370 native shape')
      call insist(all(q(1:NR,:)>0.0_real64),'all370 fission source regional positivity')
      call insist(all(transfer(q(NU,:),0_int64,NG)==0_int64),'non-scalar QFISS is positive zero')
      deallocate(q)
    enddo
    call SPOR64_BOOT64_READ_NATIVE(f%radial%flux,f%radial%track,f%radial%system, &
        f%radial%material,f%radial%route,1,0,native,rs)
    read_calls=read_calls+1
    call insist(rs==ROOT64_LOADED,'actual Native producer seal READ')
    call insist(all(shape(native)==[NU,NG]),'native full370 shape')
    call insist(all(transfer(native(NU,:),0_int64,NG)==int(z'8000000000000000',int64)), &
        'all370 native non-scalar signed-zero storage bits preserved')
    call insist(all(transfer(native(1,:),0_int64,NG)/= &
        transfer(real(real(native(1,:),real32),real64),0_int64,NG)), &
        'all370 native scalar fields retain REAL64 low bits')
    call open_root(out)
    call SPOR64_BOOT64_IMPORT_NATIVE(out,f%radial%flux,f%radial%track,f%radial%system, &
        f%radial%material,f%radial%route,1,0,is)
    import_calls=import_calls+1
    call insist(is==ROOT64_IMPORTED,'actual Native seal IMPORT')
    call insist(equal_tree(out,f%radial%flux),'actual Native full imported physical tree')
    call LCMCL(out,2);deallocate(native)
  end subroutine assert_connected

  subroutine read_q(f,p,q,rho,rs)
    type(connected_fixture), intent(in) :: f
    integer, intent(in) :: p
    real(real64), allocatable, intent(out) :: q(:,:)
    real(real64), intent(out) :: rho
    integer, intent(out) :: rs
    logical :: ok
    actual_connected_q_read_calls=actual_connected_q_read_calls+1
    rs=SPOR64_BOOTQ64_PREFLIGHT_FAILED;rho=0.0_real64
    call archive_native_admission(f,ok)
    if(.not.ok) return
    call SPOR64_BOOTQ64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,p,f%macros(p),f%sources(p),q,rho,rs)
    actual_q_read_calls=actual_q_read_calls+1
  end subroutine read_q

  subroutine connected_q_build(f,p,macroout,sourceout,rs)
    type(connected_fixture), intent(in) :: f
    integer, intent(in) :: p
    type(c_ptr), intent(in) :: macroout,sourceout
    integer, intent(out) :: rs
    logical :: ok
    actual_connected_q_build_calls=actual_connected_q_build_calls+1
    rs=SPOR64_BOOTQ64_PREFLIGHT_FAILED
    call archive_native_admission(f,ok)
    if(.not.ok) return
    call SPOR64_BOOTQ64_BUILD(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,p,macroout,sourceout,rs)
    actual_q_build_calls=actual_q_build_calls+1
  end subroutine connected_q_build

  subroutine archive_native_admission(f,ok)
    type(connected_fixture), intent(in) :: f
    logical, intent(out) :: ok
    type(c_ptr) :: tracks,systems,libraries,fluxes,seed,track,system,material,list
    real(real64), allocatable :: native(:,:)
    real(real64) :: values(NU)
    integer :: p,g,rs
    ! Explicit owning entry gate; frozen Context/Q modules do not claim an
    ! internal Native seal or external full-file authentication contract.
    ok=.false.;actual_archive_native_gate_calls=actual_archive_native_gate_calls+1
    actual_archive_native_last_status=ROOT64_REFUSED
    if(.not.RECORD_MATCHES(f%archive,'TRACK',NP,10)) return
    if(.not.RECORD_MATCHES(f%archive,'SYSTEM',NP,10)) return
    if(.not.RECORD_MATCHES(f%archive,'MICROLIB2',NP,10)) return
    if(.not.RECORD_MATCHES(f%archive,'FLUX',NP,10)) return
    tracks=LCMGID(f%archive,'TRACK');systems=LCMGID(f%archive,'SYSTEM')
    libraries=LCMGID(f%archive,'MICROLIB2');fluxes=LCMGID(f%archive,'FLUX')
    do p=1,NP
      track=LCMGIL(tracks,p);system=LCMGIL(systems,p)
      material=LCMGIL(libraries,p);seed=LCMGIL(fluxes,p)
      call SPOR64_BOOT64_READ_NATIVE(seed,track,system,material, &
          f%radial%route,p,0,native,rs)
      read_calls=read_calls+1
      actual_archive_native_read_calls=actual_archive_native_read_calls+1
      actual_archive_native_last_status=rs
      if(rs/=ROOT64_LOADED) then
        call insist(.not.allocated(native),'failed Native owning admission returns no authority')
        return
      endif
      call insist(allocated(native),'actual archive Native READ allocates authority')
      call insist(all(shape(native)==[NU,NG]),'all archive Native reads retain full370 shape')
      list=LCMGID(seed,'FLUX64')
      do g=1,NG
        call LCMGDL(list,g,values)
        call insist(same64(native(:,g),values),'all consumed archive native raw words match')
      enddo
      call insist(all(transfer(native(NU,:),0_int64,NG)==int(z'8000000000000000',int64)), &
          'all archive non-scalar signed-zero bits survive Native admission')
      call insist(all(transfer(native(1,:),0_int64,NG)/= &
          transfer(real(real(native(1,:),real32),real64),0_int64,NG)), &
          'all archive scalar fields retain real64 low bits')
      deallocate(native)
    enddo
    ok=.true.
  end subroutine archive_native_admission

  subroutine run_connected_case(f,which,phase)
    type(connected_fixture), intent(inout) :: f
    integer, intent(in) :: which
    character(len=*), intent(in) :: phase
    type(c_ptr) :: child,list,item,plane,auth,roots,mirrors,outmacro,outsource
    type(SPOR64_ROUTE_CONTRACT) :: contract
    real(real64), allocatable :: result(:,:)
    real(real64) :: values(NU),raw(2),rho
    real(real32) :: small(NU),total(NM)
    integer :: sv(NV),rs,bs,p
    logical :: ok
    if(which==1) then
      call assert_connected(f)
      actual_native_read=ROOT64_LOADED;actual_q_read=SPOR64_BOOTQ64_LOADED
      return
    endif
    select case(which)
    case(2)
      call LCMPTC(f%global,'ROLE',12,'NATIVE-K64  ')
    case(3)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      call LCMDEL(plane,'ROOT64-SEAL')
    case(4)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      list=LCMGID(plane,'ROOT-FLUX64')
      call LCMGDL(list,NG,values);call LCMPDL(list,NG,NU,2,real(values,real32))
    case(5)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      list=LCMGID(plane,'FLUX')
      call LCMGDL(list,NG,small);small(1)=bump32(small(1))
      call LCMPDL(list,NG,NU,2,small)
    case(6)
      call LCMDEL(f%projected,'GLOBAL64')
    case(7)
      auth=LCMGID(f%projected,'SPOT-R64')
      call LCMPUT(auth,'EPOCH',1,1,1)
    case(8)
      list=LCMGID(f%projected,'FLUX');plane=LCMGIL(list,2)
      auth=LCMGID(plane,'SPOT-R64');list=LCMGID(auth,'FLUX')
      call LCMGDL(list,NG,values);values(1)=values(1)+0.03125_real64
      call LCMPDL(list,NG,NU,4,values)
      roots=LCMGID(plane,'ROOT-FLUX64');call LCMPDL(roots,NG,NU,4,values)
      mirrors=LCMGID(plane,'FLUX');call LCMPDL(mirrors,NG,NU,2,real(values,real32))
    case(9)
      auth=LCMGID(f%sources(1),'SPOT-R64');call LCMDEL(auth,'EPOCH')
    case(10)
      auth=LCMGID(f%sources(1),'SPOT-R64');call LCMPUT(auth,'EPOCH',1,1,1)
    case(11)
      call LCMGET(f%sources(1),'STATE-VECTOR',sv);sv(2)=NU+1
      call LCMPUT(f%sources(1),'STATE-VECTOR',NV,1,sv)
    case(12)
      list=LCMGID(f%macros(1),'GROUP');item=LCMGIL(list,NG)
      call LCMGET(item,'NTOT0',total);total(1)=bump32(total(1))
      call LCMPUT(item,'NTOT0',NM,2,total)
    case(13)
      child=LCMGID(f%axtrack,'TRACK-META');call LCMGET(child,'RAW64',raw)
      raw(1)=bump64(raw(1));call LCMPUT(child,'RAW64',2,4,raw)
    case(14)
      list=LCMGID(f%axsystem,'GROUP');item=LCMGIL(list,NG)
      call LCMGET(item,'CORE-TAG64',rho);rho=bump64(rho)
      call LCMPUT(item,'CORE-TAG64',1,4,rho)
    case(15)
      call LCMPTC(f%radial%route,'CASE-NAME',12,'CORE-OTHER  ')
    case(16)
      roots=LCMGID(f%sources(1),'ROOT-QFISS64')
      call LCMGDL(roots,NG,values);call LCMPDL(roots,NG,NU,2,real(values,real32))
      auth=LCMGID(f%sources(1),'SPOT-R64');list=LCMGID(auth,'QFISS')
      call LCMPDL(list,NG,NU,2,real(values,real32))
    case(17)
      ! Internal modules deliberately accept coherent current values. The
      ! independent host pins this complete XSM before rewrite and rejects
      ! the changed full EOF SHA/7ID after the actual rewrite process.
      call assert_connected(f)
      call export_and_readback(f,phase=='rewrite')
      actual_native_read=ROOT64_LOADED;actual_q_read=SPOR64_BOOTQ64_LOADED
      return
    end select
    if(which>=3.and.which<=5) then
      call open_root(outmacro);call open_root(outsource)
      call connected_q_build(f,1,outmacro,outsource,bs)
      actual_native_read=actual_archive_native_last_status
      call insist(actual_native_read==ROOT64_REFUSED,'actual bound archive Native READ refusal')
      call insist(bs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'owning connected BUILD refuses broken Native authority')
      call insist(EMPTY_MEMORY_ROOT(outmacro).and.EMPTY_MEMORY_ROOT(outsource),'owning BUILD refusal output atomicity')
      call LCMCL(outsource,2);call LCMCL(outmacro,2)
      call read_q(f,1,result,rho,rs);actual_q_read=rs
      call insist(rs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'owning connected READ refuses same broken Native authority')
      call insist(.not.allocated(result),'owning READ refusal has no partially loaded authority')
    else
      if(which==2.or.(which>=6.and.which<=8)) then
        call SPOR64_BOOT_CONTEXT64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
            f%axmacro,f%archive,f%radial%route,contract,ok)
        actual_project_checks=actual_project_checks+1
        call insist(.not.ok,'actual full context reader refuses wrong/fabricated projection')
        call open_root(outmacro);call open_root(outsource)
        call connected_q_build(f,1,outmacro,outsource,bs)
        call insist(bs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'actual QBUILD refuses invalid upstream context')
        call insist(EMPTY_MEMORY_ROOT(outmacro).and.EMPTY_MEMORY_ROOT(outsource),'refused QBUILD output atomicity')
        call LCMCL(outsource,2);call LCMCL(outmacro,2)
      endif
      call read_q(f,1,result,rho,rs);actual_q_read=rs
      call insist(rs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'actual QREAD refuses case mutation')
      call insist(.not.allocated(result),'Q refusal has no loaded REAL64 result')
    endif
    internal_refused=.true.
  end subroutine run_connected_case

  subroutine export_and_readback(f,rewrite)
    type(connected_fixture), intent(in) :: f
    logical, intent(in) :: rewrite
    type(c_ptr) :: bundle,child,list
    type(connected_fixture) :: saved
    character(len=72), parameter :: filename='coherent_complete_context.xsm'
    integer :: p,mode
    logical :: exists
    inquire(file=trim(filename),exist=exists)
    if(rewrite) then
      call insist(exists,'host baseline XSM must exist before coherent rewrite')
      mode=1
    else
      call insist(.not.exists,'coherent baseline XSM must be fresh')
      mode=0
    endif
    bundle=c_null_ptr;call LCMOP(bundle,filename,mode,2,0)
    child=LCMDID(bundle,'NATIVE');call LCMEQU(f%radial%flux,child)
    child=LCMDID(bundle,'TRACK');call LCMEQU(f%radial%track,child)
    child=LCMDID(bundle,'SYSTEM');call LCMEQU(f%radial%system,child)
    child=LCMDID(bundle,'MATERIAL');call LCMEQU(f%radial%material,child)
    child=LCMDID(bundle,'RCON');call LCMEQU(f%radial%route,child)
    child=LCMDID(bundle,'AX');call LCMEQU(f%ax,child)
    child=LCMDID(bundle,'AXTRACK');call LCMEQU(f%axtrack,child)
    child=LCMDID(bundle,'AXSYSTEM');call LCMEQU(f%axsystem,child)
    child=LCMDID(bundle,'AXMACRO');call LCMEQU(f%axmacro,child)
    child=LCMDID(bundle,'ARCHIVE');call LCMEQU(f%archive,child)
    child=LCMDID(bundle,'GLOBAL64');call LCMEQU(f%global,child)
    child=LCMDID(bundle,'PROJECTED');call LCMEQU(f%projected,child)
    list=LCMLID(bundle,'MACROS',NP)
    do p=1,NP
      child=LCMDIL(list,p);call LCMEQU(f%macros(p),child)
    enddo
    list=LCMLID(bundle,'SOURCES',NP)
    do p=1,NP
      child=LCMDIL(list,p);call LCMEQU(f%sources(p),child)
    enddo
    call LCMCL(bundle,1)
    ! Reopen the real persisted full object read-only. Assertions below
    ! operate on these actual file records, not the pre-serialization fixture.
    bundle=c_null_ptr;call LCMOP(bundle,filename,2,2,0)
    saved%radial%flux=LCMGID(bundle,'NATIVE')
    saved%radial%track=LCMGID(bundle,'TRACK')
    saved%radial%system=LCMGID(bundle,'SYSTEM')
    saved%radial%material=LCMGID(bundle,'MATERIAL')
    saved%radial%route=LCMGID(bundle,'RCON')
    saved%ax=LCMGID(bundle,'AX');saved%axtrack=LCMGID(bundle,'AXTRACK')
    saved%axsystem=LCMGID(bundle,'AXSYSTEM');saved%axmacro=LCMGID(bundle,'AXMACRO')
    saved%archive=LCMGID(bundle,'ARCHIVE');saved%global=LCMGID(bundle,'GLOBAL64')
    saved%projected=LCMGID(bundle,'PROJECTED')
    list=LCMGID(bundle,'MACROS')
    do p=1,NP
      saved%macros(p)=LCMGIL(list,p)
    enddo
    list=LCMGID(bundle,'SOURCES')
    do p=1,NP
      saved%sources(p)=LCMGIL(list,p)
    enddo
    call assert_connected(saved)
    call LCMCL(bundle,1)
  end subroutine export_and_readback

  subroutine close_connected(f)
    type(connected_fixture), intent(inout) :: f
    integer :: p
    do p=1,NP
      call LCMCL(f%sources(p),2);call LCMCL(f%macros(p),2)
    enddo
    call LCMCL(f%projected,2);call LCMCL(f%global,2);call LCMCL(f%archive,2)
    call LCMCL(f%axmacro,2);call LCMCL(f%axsystem,2)
    call LCMCL(f%axtrack,2);call LCMCL(f%ax,2)
    call close_fixture(f%radial)
  end subroutine close_connected


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

end program test_ROOT64_full_connected17_v2
