from pathlib import Path
import hashlib
import json
import ast

HERE=Path(__file__).resolve().parent
OLD=HERE.with_name('root64_original17_rebuild_source_v1')

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=ident(p.stat());b=p.read_bytes();z=ident(p.stat());assert a==z
    return dict(path=str(p),size_bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),identity=a)
def save(name,data):
    p=HERE/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data.encode()if isinstance(data,str)else data)
    return pin(p)

original=OLD/'generate_full_connected17_source.py'
original_pin=pin(original);old=original.read_text();text=old;changes=[]
def splice(before,after):
    global text
    assert text.count(before)==1,(before[:100],text.count(before))
    text=text.replace(before,after,1);changes.append([before,after])

splice("test_ROOT64_full_connected17_v1", "test_ROOT64_full_connected17_v2") if False else None
# The complete generated program and proof retain an exact current83core mother.
before=text
text=text.replace('test_ROOT64_full_connected17_v1','test_ROOT64_full_connected17_v2')
text=text.replace('SEVENTEEN_COMPONENT_ASSERTIONS_V1','SEVENTEEN_COMPONENT_ASSERTIONS_V2')
changes.append([before,text])
splice('  integer :: actual_q_build_calls=0,actual_q_read_calls=0\n',
'''  integer :: actual_q_build_calls=0,actual_q_read_calls=0
  integer :: actual_archive_native_read_calls=0,actual_archive_native_gate_calls=0
  integer :: actual_archive_native_last_status=0
  integer :: actual_connected_q_build_calls=0,actual_connected_q_read_calls=0
''')
splice("  write(output_unit,'(A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A)') &", 
       "  write(output_unit,'(A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A,I0,A)') &")
splice("      ',\"explicit_native_publish_calls\":',publish_calls,'}'", 
'''      ',"explicit_native_publish_calls":',publish_calls, &
      ',"actual_archive_native_read_calls":',actual_archive_native_read_calls, &
      ',"actual_archive_native_gate_calls":',actual_archive_native_gate_calls, &
      ',"actual_archive_native_last_status":',actual_archive_native_last_status, &
      ',"actual_connected_q_build_calls":',actual_connected_q_build_calls, &
      ',"actual_connected_q_read_calls":',actual_connected_q_read_calls,'}' ''')
splice('    type(c_ptr) :: macro,list,item,child,tracks,libraries,fluxes,native,mirrors,sources64,sources32\n',
'''    type(c_ptr) :: macro,list,item,child,tracks,libraries,fluxes,systems,native,mirrors,sources64,sources32
    type(c_ptr) :: seed,seedtrack,seedsystem,seedmaterial
''')
splice('''    fluxes=LCMLID(f%archive,'FLUX',NP)
    do p=1,NP
      child=LCMDIL(tracks,p);call LCMEQU(f%radial%track,child)
      child=LCMDIL(libraries,p);call LCMEQU(f%radial%material,child)
      child=LCMDIL(fluxes,p);call LCMEQU(f%radial%flux,child)
    enddo
''','''    fluxes=LCMLID(f%archive,'FLUX',NP)
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
''')
splice('''    call SPOR64_BOOT_GLOBAL_PUBLISH(f%global,f%ax,f%axtrack,f%axsystem,f%axmacro, &
''','''    call archive_native_admission(f,ok)
    call insist(ok,'owning Native admission before actual GLOBAL publication')
    call SPOR64_BOOT_GLOBAL_PUBLISH(f%global,f%ax,f%axtrack,f%axsystem,f%axmacro, &
''')
splice('''    call SPOR64_BOOT_PROJECT_ARCHIVE(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,CONNECTED_RANK,ps)
''','''    call archive_native_admission(f,ok)
    call insist(ok,'owning Native admission before actual PROJECT publication')
    call SPOR64_BOOT_PROJECT_ARCHIVE(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,CONNECTED_RANK,ps)
''')
splice('''      call SPOR64_BOOTQ64_BUILD(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
          f%axmacro,f%archive,f%radial%route,p,f%macros(p),f%sources(p),qstat)
      actual_q_build_calls=actual_q_build_calls+1
''','''      call connected_q_build(f,p,f%macros(p),f%sources(p),qstat)
''')
splice('''    logical :: ok
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(f%global,f%ax,f%axtrack,f%axsystem, &
''','''    logical :: ok
    call archive_native_admission(f,ok)
    call insist(ok,'owning complete Native archive admission on every readback')
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(f%global,f%ax,f%axtrack,f%axsystem, &
''')
splice('''    call SPOR64_BOOTQ64_READ(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
        f%axmacro,f%archive,f%radial%route,p,f%macros(p),f%sources(p),q,rho,rs)
    actual_q_read_calls=actual_q_read_calls+1
  end subroutine read_q
''','''    logical :: ok
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
''')
splice('''    case(3)
      call LCMDEL(f%radial%flux,'ROOT64-SEAL')
    case(4)
      list=LCMGID(f%radial%flux,'ROOT-FLUX64')
      call LCMGDL(list,NG,values);call LCMPDL(list,NG,NU,2,real(values,real32))
    case(5)
      list=LCMGID(f%radial%flux,'FLUX')
''','''    case(3)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      call LCMDEL(plane,'ROOT64-SEAL')
    case(4)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      list=LCMGID(plane,'ROOT-FLUX64')
      call LCMGDL(list,NG,values);call LCMPDL(list,NG,NU,2,real(values,real32))
    case(5)
      list=LCMGID(f%archive,'FLUX');plane=LCMGIL(list,NP)
      list=LCMGID(plane,'FLUX')
''')
splice('''      call SPOR64_BOOT64_READ_NATIVE(f%radial%flux,f%radial%track,f%radial%system, &
          f%radial%material,f%radial%route,1,0,result,rs)
      read_calls=read_calls+1;actual_native_read=rs
      call insist(rs==ROOT64_REFUSED,'actual Native READ refuses broken seal/root/mirror')
      call insist(.not.allocated(result),'Native refusal has no partially loaded authority')
''','''      call open_root(outmacro);call open_root(outsource)
      call connected_q_build(f,1,outmacro,outsource,bs)
      actual_native_read=actual_archive_native_last_status
      call insist(actual_native_read==ROOT64_REFUSED,'actual bound archive Native READ refusal')
      call insist(bs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'owning connected BUILD refuses broken Native authority')
      call insist(EMPTY_MEMORY_ROOT(outmacro).and.EMPTY_MEMORY_ROOT(outsource),'owning BUILD refusal output atomicity')
      call LCMCL(outsource,2);call LCMCL(outmacro,2)
      call read_q(f,1,result,rho,rs);actual_q_read=rs
      call insist(rs==SPOR64_BOOTQ64_PREFLIGHT_FAILED,'owning connected READ refuses same broken Native authority')
      call insist(.not.allocated(result),'owning READ refusal has no partially loaded authority')
''')
splice('''        call SPOR64_BOOTQ64_BUILD(f%projected,f%global,f%ax,f%axtrack,f%axsystem, &
            f%axmacro,f%archive,f%radial%route,1,outmacro,outsource,bs)
        actual_q_build_calls=actual_q_build_calls+1
''','''        call connected_q_build(f,1,outmacro,outsource,bs)
''')
ast.parse(text)
inverse=text
for before,after in reversed(changes):
    assert inverse.count(after)==1
    inverse=inverse.replace(after,before,1)
assert inverse==old
newpin=save('generate_full_connected17_source.py',text)
retained=save('unqualified_v1_exact_writer/generate_full_connected17_source.py',old)
save('EXACT_UNFROZEN_V1_TO_V2_SOURCE_WRITER_DERIVATION.json',json.dumps(dict(
    original=original_pin,retained=retained,new=newpin,literal_changes=changes,
    complete_inverse_matches=True,old_v1_archive_lineage_incomplete=True,
    compiler_or_native_executed=False),indent=2)+'\n')
print(json.dumps(dict(new_source_writer=newpin,original_v1_writer_unchanged=pin(original)==original_pin,
    complete_inverse=True,compiler_or_native_executed=False)))
