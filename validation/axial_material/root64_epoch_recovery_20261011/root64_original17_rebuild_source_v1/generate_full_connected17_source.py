from pathlib import Path
import hashlib
import json
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=Path(__file__).resolve().parent
MOTHER=REC/'native_core_controls_source/test_current_ROOT64_native_core.f90'


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path):
    p=Path(path); before=identity(p.stat()); data=p.read_bytes(); after=identity(p.stat())
    assert before==after and len(data)==before[4]
    return dict(path=str(p),size_bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),identity=before)


def put(name,data):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb')as f:f.write(data if isinstance(data,bytes)else data.encode())
    return pin(p)


start=time.monotonic()
mother_pin=pin(MOTHER)
assert mother_pin['sha256']=='94ab9ccc25d03d4affc5b54490e0aebd4e5fe618687aa68493557fbe99f212c6'
old=MOTHER.read_bytes().decode()
changes=[]


def splice(before,after):
    global text
    assert text.count(before)==1, before[:100]
    text=text.replace(before,after,1);changes.append([before,after])


text=old
splice('program test_current_ROOT64_native_core\n  ! NEW SOURCE:',
       'program test_ROOT64_full_connected17_v1\n  ! NEW SOURCE:')
splice('  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT, RECORD_MATCHES\n',
'''  use SPOR64_VERIFY, only : EMPTY_MEMORY_ROOT, RECORD_MATCHES
  use SPOR64_BOOT_CANONICAL64_V2, only: SPOR64_BOOT_CANONICAL64_WRITE
  use SPOR64_BOOT_CONTEXT64_V2, only: SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK, &
      SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_BOOT_PUBLISH64, only: SPOR64_BOOT_GLOBAL_PUBLISH, &
      SPOR64_BOOT_GLOBAL_PUBLISHED
  use SPOR64_BOOT_PROJECT64, only: SPOR64_BOOT_PROJECT_ARCHIVE, &
      SPOR64_BOOT_PROJECT_COMMITTED
  use SPOR64_BOOTQ64_V2, only: SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_READ, &
      SPOR64_BOOTQ64_COMMITTED,SPOR64_BOOTQ64_LOADED,SPOR64_BOOTQ64_PREFLIGHT_FAILED
''')
splice('  ! NEW SOURCE: real GANLIB in-memory contract controls for the current module.\n',
'''  ! NEW SOURCE: all seventeen connected controls on current complete modules.
  ! Old /tmp seventeen fixture bytes were lost; no old PASS is inherited.
  ! Synthetic protocol values are never a genuine solver or physics result.
''')
splice('  end type fixture\n', '''  end type fixture
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
  logical :: internal_refused,coherent_rewrite
''')
begin=text.index('  if (command_argument_count()/=0)')
end=text.index('\ncontains\n',begin)
original_main=text[begin:end]
new_main='''  narg=command_argument_count()
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
      '","schema":"CONNECTED_CURRENT_ROOT64_SEVENTEEN_COMPONENT_ASSERTIONS_V1",'// &
      '"all_actual_assertions_completed":true,"synthetic_fixture":true,'// &
      '"genuine_producer_qualified":false,"solver_executed":false,'// &
      '"physics_qualified":false,"old_seventeen_PASS_inherited":false}'
  write(output_unit,'(A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A)') &
      '{"case":"'//trim(selected_case)//'","phase":"'//trim(phase)// &
      '","actual_native_read_status":',actual_native_read, &
      ',"actual_q_read_status":',actual_q_read, &
      ',"actual_global_checks":',actual_global_checks, &
      ',"actual_project_checks":',actual_project_checks, &
      ',"explicit_q_build_calls":',actual_q_build_calls, &
      ',"explicit_q_read_calls":',actual_q_read_calls, &
      ',"explicit_native_publish_calls":',publish_calls,'}'
  flush(output_unit)
'''
splice(original_main,new_main)
extra='''
  subroutine build_connected(f,rewrite)
    type(connected_fixture), intent(out) :: f
    logical, intent(in) :: rewrite
    type(c_ptr) :: macro,list,item,child,tracks,libraries,fluxes,native,mirrors,sources64,sources32
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
    do p=1,NP
      child=LCMDIL(tracks,p);call LCMEQU(f%radial%track,child)
      child=LCMDIL(libraries,p);call LCMEQU(f%radial%material,child)
      child=LCMDIL(fluxes,p);call LCMEQU(f%radial%flux,child)
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
    call SPOR64_BOOT_GLOBAL_PUBLISH(f%global,f%ax,f%axtrack,f%axsystem,f%axmacro, &
        f%archive,f%radial%route,f%ax_image,f%ax_source,K64,gates,[2,1],1,.true.,ps)
    call insist(ps==SPOR64_BOOT_GLOBAL_PUBLISHED,'actual full GLOBAL publisher')
    call SPOR64_BOOT_PROJECT_ARCHIVE(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,CONNECTED_RANK,ps)
    call insist(ps==SPOR64_BOOT_PROJECT_COMMITTED,'actual full PROJECTED-BOOT/e0 publisher')
    do p=1,NP
      call open_root(f%macros(p));call open_root(f%sources(p))
      call SPOR64_BOOTQ64_BUILD(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
          f%axmacro,f%archive,f%radial%route,p,f%macros(p),f%sources(p),qstat)
      actual_q_build_calls=actual_q_build_calls+1
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
    call SPOR64_BOOTQ64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,p,f%macros(p),f%sources(p),q,rho,rs)
    actual_q_read_calls=actual_q_read_calls+1
  end subroutine read_q

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
      call LCMDEL(f%radial%flux,'ROOT64-SEAL')
    case(4)
      list=LCMGID(f%radial%flux,'ROOT-FLUX64')
      call LCMGDL(list,NG,values);call LCMPDL(list,NG,NU,2,real(values,real32))
    case(5)
      list=LCMGID(f%radial%flux,'FLUX')
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
      call SPOR64_BOOT64_READ_NATIVE(f%radial%flux,f%radial%track,f%radial%system, &
          f%radial%material,f%radial%route,1,0,result,rs)
      read_calls=read_calls+1;actual_native_read=rs
      call insist(rs==ROOT64_REFUSED,'actual Native READ refuses broken seal/root/mirror')
      call insist(.not.allocated(result),'Native refusal has no partially loaded authority')
    else
      if(which==2.or.(which>=6.and.which<=8)) then
        call SPOR64_BOOT_CONTEXT64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
            f%axmacro,f%archive,f%radial%route,contract,ok)
        actual_project_checks=actual_project_checks+1
        call insist(.not.ok,'actual full context reader refuses wrong/fabricated projection')
        call open_root(outmacro);call open_root(outsource)
        call SPOR64_BOOTQ64_BUILD(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
            f%axmacro,f%archive,f%radial%route,1,outmacro,outsource,bs)
        actual_q_build_calls=actual_q_build_calls+1
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

'''
splice('\n  subroutine fail(message)\n',extra+'\n  subroutine fail(message)\n')
splice('end program test_current_ROOT64_native_core\n','end program test_ROOT64_full_connected17_v1\n')
new=text.encode();inverse=text
for before,after in reversed(changes):
    assert inverse.count(after)==1
    inverse=inverse.replace(after,before,1)
assert inverse==old
assert max(map(len,text.splitlines()))<=132
source_pin=put('test_ROOT64_full_connected17_v1.f90',new)
retained_pin=put('original_exact_source/test_current_ROOT64_native_core.f90',old)
proof=put('COMPLETE_FORTRAN_MOTHER_EXACT_BYTE_INVERSE.json',json.dumps({
    'schema':'FULL_CORE83_MOTHER_TO_NEW_CONNECTED17_EXACT_SOURCE_INVERSE_V1',
    'original':mother_pin,'retained_complete_original':retained_pin,'new':source_pin,
    'literal_changes':changes,'full_byte_inverse_matches':inverse==old,
    'native_factory_and_all_complete_old_helpers_byte_unchanged':True,
    'unused_old83_control_routines_retained_not_executed_as17':True,
    'old_lost17_fixture_source_bytes_recovered':False,
    'old17_PASS_or_original_qualification_inherited':False},ensure_ascii=False,indent=2)+'\n')
assert pin(MOTHER)==mother_pin
put('SOURCE_GENERATION_ACTUAL_SELF_RESULT.json',json.dumps({
    'Source_writer_completed':True,'source_pin':source_pin,'mother_unchanged':True,
    'full_byte_inverse_matches':True,'proof':proof,'elapsed_seconds':time.monotonic()-start,
    'compiler_CLE_parser_native_or_transport_executed':False},indent=2)+'\n')
print(json.dumps({'source_pin':source_pin,'proof_pin':proof,'mother_unchanged':True,
                  'elapsed_seconds':time.monotonic()-start,'no_compiler_or_solver':True}))
