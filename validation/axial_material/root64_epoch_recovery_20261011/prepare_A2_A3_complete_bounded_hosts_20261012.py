#!/usr/bin/env python3
"""Pure stdlib complete host/command writer. Never imports or executes a host."""
from pathlib import Path
import ast
import hashlib
import json
import os
import re
import stat

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts'
BUILD_BASE=REC/'native_warm_A2_A3_runtime_build_source_v1'
WARM_BASE=REC/'native_warm_A2_A3_bounded_host_source_v1'
BUILD_OUT=ART/'axial-material-new-REAL64-native-A2-A3-complete61-route-build-only-20261012'
OLD_BUILD=REC/'native_warm_B_runtime_build_source_v1/build_complete_native_B_handler_dispatcher57_only.py'
OLD_DECL=REC/'native_warm_B_runtime_build_source_v1/CURRENT_B_COMPLETE57_BUILD_BINDING.json'
OLD_WARM=REC/'native_warm_B_initial_storage_reserve_source_v2'
OLD_BIND=REC/'native_warm_B_bounded_host_source_v1/CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'
B_OUT=ART/'axial-material-new-REAL64-native-B-complete57-route-build-only-20261012'
A1_OUT=ART/'axial-material-new-REAL64-native-warm-A-20261012-v3'
FLAGS=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);before=identity(p.lstat());assert stat.S_ISREG(before[2]),str(p)
    with p.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==before
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        assert identity(os.fstat(f.fileno()))==before
    assert identity(p.lstat())==before
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def normalized(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def write(p,content):
    if isinstance(content,dict):content=json.dumps(content,indent=2,allow_nan=False)+'\n'
    if Path(p).exists():
        assert Path(p).read_bytes()==content.encode(),str(p)
        return
    with Path(p).open('x')as f:f.write(content);f.flush();os.fsync(f.fileno())
def offsets(data,needle):
    result=[];start=0
    while True:
        at=data.find(needle,start)
        if at<0:return result
        result.append(at);start=at+len(needle)
class Change:
    def __init__(self,p):self.path=Path(p);self.raw=self.path.read_bytes();self.current=self.raw;self.rows=[];self.original=pin(p)
    def replace(self,old,new,count=1):
        old=old.encode();new=new.encode();before=offsets(self.current,old)
        assert len(before)==count,(str(self.path),old,len(before),count)
        after=self.current.replace(old,new)
        replaced_after=[at+i*(len(new)-len(old))for i,at in enumerate(before)]
        assert all(after[at:at+len(new)]==new for at in replaced_after)
        self.rows.append(dict(old=old.decode(),new=new.decode(),count=count,before_byte_offsets=before,after_byte_offsets=replaced_after,reverse_scope='only these explicit replaced byte spans'))
        self.current=after
    def all(self,old,new):self.replace(old,new,self.current.count(old.encode()))
    def save(self,p):
        inverse=self.current
        for r in reversed(self.rows):
            old=r['old'].encode();new=r['new'].encode()
            for at in reversed(r['after_byte_offsets']):
                assert inverse[at:at+len(new)]==new
                inverse=inverse[:at]+old+inverse[at+len(new):]
            assert offsets(inverse,r['old'].encode())==r['before_byte_offsets']
        assert inverse==self.raw
        ast.parse(self.current.decode())
        write(p,self.current.decode());return dict(original_source=self.original,literal_changes=self.rows,new_source=pin(p),full_byte_forward_and_inverse_equal=True)

# Complete actual runtime admission, before any directory or child is created.
ADMIT_BUILD='''
def admit_build(path,sha,seven,binding,helper):
    d,p=load_json_exact(path,sha,seven)
    plan_path=Path(binding['planned_A23_61_build_binding_pin']['path'])
    same_pin(plan_path,binding['planned_A23_61_build_binding_pin']);plan=json.loads(plan_path.read_text())
    root=Path(plan['fresh_output_root'])
    if Path(path)!=root/'Root_actual_build_only_summary.json':raise RuntimeError('explicit sole actual61 build report path')
    if d.get('schema')!='ACTUAL_COMPLETE_NATIVE_A23_FIVE_SOURCE_COMPLETE61_BUILD_ONLY_V1' or d.get('status')!='ACTUAL_A23_FIVE_COMPILE_AND_COMPLETE61_DRAGON_LINK_CLOSED0_ONLY' or d.get('Dragon_linked') is not True or d.get('transport_executed') is not False:
        raise RuntimeError('actual five Source compiles and complete61 runtime required')
    closed_report(d,helper,root,6)
    wanted=plan['compile_commands']+[plan['complete_link_command']]
    if [r['command']for r in d['records']]!=wanted:raise RuntimeError('actual61 complete ordered commands')
    actual_bind_path=root/'Root_current_compile_only_binding.json';actual_bind_pin=pin(actual_bind_path)
    actual_bind=json.loads(actual_bind_path.read_text())
    if actual_bind['actual_commands']!=wanted or actual_bind['complete_ordered_link_input_count']!=61 or actual_bind['original_flags']!=FLAGS or actual_bind['fixed_current_pins']!=d['fixed_current_pins']:
        raise RuntimeError('actual61 owning binding and exact flags/input table')
    if len(wanted[-1][3:-2])!=61 or wanted[-1][-6:-2]!=plan['prior_actual_complete_link'][-6:-2]:raise RuntimeError('all61 input and original4 archive order')
    table={r['path']:r for r in d['fixed_current_pins']};outputs={r['path']:r for r in d['output_pins']}
    origins=d['actual_new_Source_to_object_origins']
    if len(origins)!=5:raise RuntimeError('all five actual Source-object origins')
    for index,row in enumerate(origins):
        cmd=wanted[index];source=row['source_pin'];obj=row['object_pin']
        if source['path']!=plan['compile_sources'][index] or table.get(source['path'])!=source or outputs.get(obj['path'])!=obj or row['actual_compile_record']!=d['records'][index] or row['actual_watchdog_check']!=d['actual_watchdog_checks'][index] or row['original_nine_flags']!=FLAGS:
            raise RuntimeError('current actual61 complete Source-object origin')
        if cmd[cmd.index('-c')+1]!=source['path'] or cmd[-1]!=obj['path'] or obj['path']not in wanted[-1]:raise RuntimeError('actual61 exact Source/compiler/object/link association')
        same_pin(source['path'],source);same_pin(obj['path'],obj)
    for row in binding['seventeen_required_same_production_object_pins']:
        if row['path']not in wanted[-1] or table.get(row['path'])!=row:raise RuntimeError('original17 same9 production objects in actual61 runtime')
    dragon=outputs.get(str(root/'runtime/Dragon'))
    if dragon is None:raise RuntimeError('actual61 complete Dragon fullpin')
    same_pin(dragon['path'],dragon)
    return d,p,actual_bind_pin,dragon
'''

def main():
    assert not(WARM_BASE/'COMPLETE_A23_BOUNDED_HOST_SOURCE_FREEZE.json').exists()
    assert not(WARM_BASE/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json').exists()
    BUILD_BASE.mkdir(exist_ok=True);WARM_BASE.mkdir(exist_ok=True)
    old_decl=json.loads(OLD_DECL.read_text());old_bind=json.loads(OLD_BIND.read_text())
    b_report_path=B_OUT/'Root_actual_build_only_summary.json';b_report=json.loads(b_report_path.read_text())
    b_binding_path=B_OUT/'Root_current_compile_only_binding.json';b_binding=json.loads(b_binding_path.read_text())
    assert b_report['status']=='ACTUAL_B_TWO_COMPILE_AND_COMPLETE57_DRAGON_LINK_CLOSED0_ONLY'and b_report['failure']is None and b_report['after_check_error']is None
    assert len(b_report['records'])==3 and all(r['status']=='PASS'for r in b_report['records'])
    assert b_binding['actual_commands']==[r['command']for r in b_report['records']]
    prior=b_report['records'][-1]['command'];assert prior==old_decl['complete_link_command']and len(prior[3:-2])==57
    originals=prior[3:-2];assert len(originals[-4:])==4
    compiler=old_bind['compiler']['path']
    case_dirs={s:REC/f'native_warm_{s}_case_source_v1'for s in ('A2','A3')}
    route_dir=REC/'three_native_plane_contract_route_source_v1'
    sources=[case_dirs['A2']/'AXNCASEA264.f90',case_dirs['A3']/'AXNCASEA364.f90',route_dir/'SPOASMP64.f',route_dir/'SPOOPP64.f90',case_dirs['A2']/'KDRDRV.F']
    includes=old_decl['includes'];build=BUILD_OUT/'build'
    compile_commands=[[compiler,*FLAGS,'-I'+str(build),*['-I'+p for p in includes],'-J'+str(build),'-c',str(p),'-o',str(build/(p.stem+'.o'))]for p in sources]
    old_dispatcher=str(B_OUT/'build/KDRDRV.o');assert originals.count(old_dispatcher)==1 and originals.index(old_dispatcher)==14
    objects=[str(build/'KDRDRV.o')if p==old_dispatcher else p for p in originals[:-4]]
    added=[str(build/(p.stem+'.o'))for p in sources[:-1]]
    link=[compiler,'-O2','-ffp-contract=off',*objects,*added,*originals[-4:],'-o',str(BUILD_OUT/'runtime/Dragon')]
    assert len(link[3:-2])==61 and link[-6:-2]==prior[-6:-2]
    fixed={}
    def add(row):
        row=normalized(row);assert pin(row['path'])==row,row['path']
        if row['path']in fixed:assert fixed[row['path']]==row
        fixed[row['path']]=row
    for row in old_bind['fixed_current_pins']+b_report['fixed_current_pins']+b_report['output_pins']:add(row)
    for p in [OLD_BUILD,OLD_DECL,OLD_BIND,b_report_path,b_binding_path,Path(__file__).resolve(),OLD_WARM/'COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json',route_dir/'INDEPENDENT_SMALL_SOURCE_REVIEW_RECEIPT.json',route_dir/'COMPLETE_THREE_PLANE_CONTRACT_ROUTE_BYTE_INVERSE.json']:add(pin(p))
    cases={}
    for name,plane in [('A2',2),('A3',3)]:
        folder=case_dirs[name];meta=folder/f'COMPLETE_PLANE{plane}_SOURCE_BYTE_INVERSE_AND_PHYSICAL_METADATA.json';m=json.loads(meta.read_text());add(pin(meta))
        assert(m['plane'],m['epoch'],m['archive_listdim'],m['archive_item'])==(plane,0,1,1)
        for r in m['sources']:add(r['new_source']);add(r['original_source'])
        physical=[]
        for row in m['physical_inputs']:
            add(row['pin']);physical.append(dict(row,owned_runtime_relative_path=None if row['role']=='readonly_rays_reference'else name+'/'+Path(row['pin']['path']).name))
        cases[name]=dict(case=name,plane=plane,epoch=0,physical_inputs=physical,exact_warm_deck=pin(folder/f'ROOT64_NEW_WARM_{name}_20261012.x2m'),probe_source_pin=pin(folder/f'verify_native_{name}_archive64.f90'),case_name_json=f'R64-{name}-WARM1 ',case_name_lcm12=f'R64-{name}-WARM1',handler=f'AXNCASE{name}64',case_Source_metadata_pin=pin(meta))
    a1_report_path=A1_OUT/'Root_actual_single_plane_warm_A_summary.json';a1=json.loads(a1_report_path.read_text())
    assert a1['status']=='ACTUAL_SINGLE_PLANE1_E0_WARM_A_NATIVE_PRODUCER_CLOSED0_ONLY'and a1['failure']is None and len(a1['records'])==4 and all(r['status']=='PASS'for r in a1['records'])
    assert a1['single_plane_native_producer_closed']is True and a1['actual_native_terminal']['full_native_read_status']==3
    for r in a1['fixed_current_pins']+a1['output_pins']:add(r)
    add(pin(a1_report_path))
    proofs=[]
    # Exact B host derivation preserves every original guard and limit.
    t=Change(OLD_BUILD)
    t.replace('Compile full B case handler and dispatcher, then complete57-input Dragon link; no transport.','Compile full A2/A3 handlers, per-plane operator and dispatcher, then complete61 link; no transport.')
    t.replace("OUT=ART/'axial-material-new-REAL64-native-B-complete57-route-build-only-20261012'",f"OUT=ART/'{BUILD_OUT.name}'")
    # FREEZE is the immutable B Source proof retained as part of original
    # supervisor admission; the new cases/routes are all independently pinned.
    t.replace("DECLARATION=REC/'native_warm_B_runtime_build_source_v1/CURRENT_B_COMPLETE57_BUILD_BINDING.json'",f"DECLARATION=REC/'{BUILD_BASE.name}/CURRENT_A23_COMPLETE61_BUILD_BINDING.json'")
    t.replace("if len(sources)!=2:raise RuntimeError('exact B handler and full dispatcher compile Sources')","if len(sources)!=5:raise RuntimeError('exact A2/A3 handlers, two per-plane operator Sources and full dispatcher')")
    oldmap=re.search(r'    reviewed_new_sources=\{.*?\}\n',t.current.decode()).group(0)
    reviewed={str(p):pin(p)['sha256']for p in sources}
    t.replace(oldmap,'    reviewed_new_sources='+repr(reviewed)+'\n')
    t.replace("resources=Resources();before=resources.check()\n","resources=Resources();before=resources.check()\n    if before['artifact_bytes']+20971764748+64*2**20+2*2**30>=96*2**30:raise RuntimeError('history96GiB original cold reserve plus initial fresh2GiB')\n")
    t.replace("if len(commands)!=2:raise RuntimeError('exact two complete B compile commands')","if len(commands)!=5:raise RuntimeError('exact five complete A23 compile commands')")
    block=t.current.decode().split('    base=command_declaration[\'prior_actual_complete_link\']\n',1)[1].split('    for row in command_declaration[\'B_physical_inputs\']:\n',1)[0]
    newblock="""    original_inputs=list(base[3:-2])
    old_dispatcher=command_declaration['prior_dispatcher_object']
    new_dispatcher=str(build/'KDRDRV.o')
    if len(original_inputs)!=57 or original_inputs.count(old_dispatcher)!=1 or original_inputs.index(old_dispatcher)!=14:raise RuntimeError('exact actual57 unique dispatcher input')
    original_objects=original_inputs[:-4]
    repaired_objects=[new_dispatcher if p==old_dispatcher else p for p in original_objects]
    added_objects=[str(build/(p.stem+'.o'))for p in sources[:-1]]
    expected_link=[str(COMPILER),'-O2','-ffp-contract=off',*repaired_objects,*added_objects,*original_inputs[-4:],'-o',str(OUT/'runtime/Dragon')]
    link=command_declaration['complete_link_command']
    if link!=expected_link or len(link[3:-2])!=61 or sum(a!=b for a,b in zip(original_objects,repaired_objects))!=1 or link[-6:-2]!=original_inputs[-4:]:raise RuntimeError('complete61 same-order dispatcher replacement and four new objects; original4 archive order')
    origin=command_declaration['actual_current57_runtime_origin']
    actual_runtime=json.loads(Path(origin['actual_summary_pin']['path']).read_text())
    actual_binding=json.loads(Path(origin['actual_binding_pin']['path']).read_text())
    if actual_runtime['status']!='ACTUAL_B_TWO_COMPILE_AND_COMPLETE57_DRAGON_LINK_CLOSED0_ONLY' or actual_runtime['failure'] is not None or actual_runtime['after_check_error'] is not None or len(actual_runtime['records'])!=3 or any(r['status']!='PASS'for r in actual_runtime['records']) or actual_runtime['records'][-1]['command']!=base or actual_binding['actual_commands']!=[r['command']for r in actual_runtime['records']]:raise RuntimeError('genuine actual current complete57 runtime origin')
    for record in actual_runtime['records']:helper.check_watch(Path(origin['actual_summary_pin']['path']).parent,record)
    for row in origin.values():
        if current_by_path.get(row['path'])!=row:raise RuntimeError('actual current57 fullEOF origin pin')
"""
    t.replace(block,newblock)
    t.replace("command_declaration['B_physical_inputs']","command_declaration['A_physical_inputs']")
    t.all('index<2','index<5')
    t.replace("if len(actual_new_object_origins)!=2:raise RuntimeError('two actual Source-to-object origins required')","if len(actual_new_object_origins)!=5:raise RuntimeError('five actual Source-to-object origins required')")
    t.replace("complete_declared_reference_inputs=1936,complete_ordered_link_input_count=57","complete_declared_reference_inputs=len(declared),complete_ordered_link_input_count=61")
    t.replace("scope='two complete B handler/dispatcher Source compiles and complete57 ordered input Dragon link; unique old dispatcher replaced and one Bhandler object added, other original inputs and four archives preserved; B plane2/e0 Source build only, no transport, GLOBAL, online BOOT or physics qualification'","scope='five complete A2/A3 handler, per-plane operator and dispatcher compiles with complete61 ordered Dragon link; same-order unique KDR replacement, four new objects, all original archives; Source build only, no producer, three-plane, GLOBAL, online BOOT or physics qualification'")
    t.replace("schema='ACTUAL_COMPLETE_NATIVE_B_HANDLER_DISPATCHER57_BUILD_ONLY_V1'","schema='ACTUAL_COMPLETE_NATIVE_A23_FIVE_SOURCE_COMPLETE61_BUILD_ONLY_V1'")
    t.replace("status='ACTUAL_B_TWO_COMPILE_AND_COMPLETE57_DRAGON_LINK_CLOSED0_ONLY'if failure is None else 'FAILED_B_BUILD_ONLY_NO_RETRY'","status='ACTUAL_A23_FIVE_COMPILE_AND_COMPLETE61_DRAGON_LINK_CLOSED0_ONLY'if failure is None else 'FAILED_A23_BUILD_ONLY_NO_RETRY'")
    build_host=BUILD_BASE/'build_complete_native_A23_handlers_operator_dispatcher61_only.py';proofs.append(t.save(build_host));add(pin(build_host))
    for name in ('A2','A3'):
        common=Change(OLD_WARM/'guarded_warm_B_common.py')
        common.replace("BIND = REC/'native_warm_B_bounded_host_source_v1/CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'",f"BIND = REC/'{WARM_BASE.name}/CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json'")
        common.replace('binding=json.loads(BIND.read_text());verify_rows(binding[\'fixed_current_pins\'])',f"binding=json.loads(BIND.read_text());binding.update(binding['cases']['{name}']);verify_rows(binding['fixed_current_pins'])")
        common.all("binding['current_B57_Dragon']","binding['current_A23_61_Dragon']")
        common.replace("c=binding['compiler']['path'];src=str(BASE/'verify_native_B_archive64.f90')", "c=binding['compiler']['path'];src=binding['probe_source_pin']['path']")
        common.all('verify_native_B_archive64',f'verify_native_{name}_archive64')
        common.replace('\ndef check_full_current(fixed,owned):\n',ADMIT_BUILD+'\ndef check_full_current(fixed,owned):\n')
        common_path=WARM_BASE/f'guarded_warm_{name}_common.py';proofs.append(common.save(common_path));add(pin(common_path))
        entry=Change(OLD_WARM/'run_current_warm_B_entry_controls.py')
        entry.all('guarded_warm_B_common',f'guarded_warm_{name}_common')
        entry.all('AXNCASEB64',f'AXNCASE{name}64')
        entry.all('snapshot_B.xsm','snapshot_A.xsm')
        entry.all('verify_native_B_archive64',f'verify_native_{name}_archive64')
        entry.all('warm-B',f'warm-{name}');entry.all('warm_B',f'warm_{name}');entry.all('WARM_B',f'WARM_{name}');entry.all('WARM-B',f'WARM-{name}')
        entry.all('R64WARM-B-V1 ',f'R64-{name}-WARM1 ')
        entry.replace("    args=parser.parse_args();start=time.monotonic()\n", "    for prefix in ('build',):\n        parser.add_argument('--'+prefix+'-summary',required=True)\n        parser.add_argument('--'+prefix+'-sha256',required=True)\n        parser.add_argument('--'+prefix+'-seven-id',required=True)\n    args=parser.parse_args();start=time.monotonic()\n")
        entry.replace("    fixed+=[seventeen_pin]+seventeen['fixed_current_pins']+seventeen['output_pins']\n", "    runtime,pruntime,pruntime_bind,dragon=c.admit_build(args.build_summary,args.build_sha256,args.build_seven_id,binding,helper)\n    binding['current_A23_61_Dragon']=dragon\n    fixed+=[seventeen_pin,pruntime,pruntime_bind]+seventeen['fixed_current_pins']+seventeen['output_pins']+runtime['fixed_current_pins']+runtime['output_pins']\n")
        # Source-only applicability is additionally checked at actual entry;
        # no positive FLUNAT transport is introduced into these controls.
        entry_path=WARM_BASE/f'run_current_warm_{name}_entry_controls.py';proofs.append(entry.save(entry_path));add(pin(entry_path))
        warm=Change(OLD_WARM/'run_current_native_warm_B.py')
        warm.all('guarded_warm_B_common',f'guarded_warm_{name}_common');warm.all('run_current_warm_B_entry_controls',f'run_current_warm_{name}_entry_controls')
        warm.all('verify_native_B_archive64',f'verify_native_{name}_archive64');warm.all('R64WARM-B-V1 ',f'R64-{name}-WARM1 ')
        warm.all('warm_B',f'warm_{name}');warm.all('WARM_B',f'WARM_{name}');warm.all('warm-B',f'warm-{name}');warm.all('WARM-B',f'WARM-{name}')
        warm.all('new_native_B.xsm',f'new_native_{name}.xsm');warm.all('ROOT64_NEW_WARM_B_20261012',f'ROOT64_NEW_WARM_{name}_20261012')
        warm.all("OUT/'B",f"OUT/'{name}");warm.replace("binding,'B')",f"binding,'{name}')");warm.all("r['label']=='B/solve'",f"r['label']=='{name}/solve'")
        warm.replace(f"OUT=c.ART/'axial-material-new-REAL64-native-warm-{name}-20261012-v2-initial-storage-reserve'",f"OUT=c.ART/'axial-material-new-REAL64-native-warm-{name}-20261012-v1'")
        if name=='A3':warm.replace('One owned plane2/e0 actual warm solve','One owned plane3/e0 actual warm solve')
        warm.replace("for prefix in ('seventeen','entry-controls','source-freeze'):","for prefix in ('seventeen','entry-controls','source-freeze','build'):")
        warm.replace(f"freeze_path=c.BASE/'COMPLETE_WARM_{name}_INITIAL_STORAGE_SOURCE_FREEZE.json'","freeze_path=c.BASE/'COMPLETE_A23_BOUNDED_HOST_SOURCE_FREEZE.json'")
        warm.replace(f"source_freeze['schema']!='CURRENT_WARM_{name}_INITIAL_STORAGE_SOURCE_FREEZE_ONLY_V2'","source_freeze['schema']!='COMPLETE_CURRENT_A23_BOUNDED_HOST_SOURCE_FREEZE_ONLY_V1'")
        original_required=f"""    required={{'guarded_warm_{name}_common.py','run_current_native_warm_{name}.py',
              'run_current_warm_{name}_entry_controls.py','verify_native_{name}_archive64.f90',
              'COMPLETE_INITIAL_STORAGE_HOST_SOURCE_BYTE_INVERSE.json'}}
"""
        new_required="""    required={'guarded_warm_A2_common.py','run_current_native_warm_A2.py',
              'run_current_warm_A2_entry_controls.py','guarded_warm_A3_common.py',
              'run_current_native_warm_A3.py','run_current_warm_A3_entry_controls.py',
              'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json','COMPLETE_A23_HOST_SOURCE_BYTE_INVERSE.json'}
"""
        warm.replace(original_required,new_required)
        warm.replace("    c.verify_rows(source_rows)\n", "    c.verify_rows(source_rows)\n    external_source_rows=source_freeze['fixed_external_source_files']\n    c.verify_rows(external_source_rows)\n")
        warm.replace("    seventeen,p17=c.admit17", "    external_table={r['path']:r for r in external_source_rows}\n    expected_external=[binding['probe_source_pin'],binding['planned_A23_61_build_binding_pin'],binding['planned_A23_61_build_host_pin']]\n    if len(external_table)!=len(external_source_rows) or any(external_table.get(r['path'])!=r for r in expected_external):\n        raise RuntimeError('complete exact frozen original case probe and current build Source dependencies')\n    seventeen,p17=c.admit17")
        warm.replace("    route,proute=admit_entry", "    runtime,pruntime,pruntime_bind,dragon=c.admit_build(args.build_summary,args.build_sha256,args.build_seven_id,binding,helper)\n    binding['current_A23_61_Dragon']=dragon\n    route,proute=admit_entry")
        warm.replace("    fixed+=source_rows+[source_pin,p17,proute]+seventeen['fixed_current_pins']+seventeen['output_pins']+route['fixed_current_pins']+route['output_pins']", "    fixed+=source_rows+external_source_rows+[source_pin,p17,proute,pruntime,pruntime_bind]+seventeen['fixed_current_pins']+seventeen['output_pins']+route['fixed_current_pins']+route['output_pins']+runtime['fixed_current_pins']+runtime['output_pins']")
        warm.replace("    if d['transport_executed'] is not False or d['physical_producer_qualified'] is not False:","    dragon=binding['current_A23_61_Dragon']\n    if pins.get(dragon['path'])!=dragon:raise RuntimeError('entry controls exact actual61 runtime applicability')\n    if d['transport_executed'] is not False or d['physical_producer_qualified'] is not False:")
        warm.replace("(terminal['plane'],terminal['epoch'],terminal['groups'],terminal['unknowns'])!=(2,0,370,14)",f"(terminal['plane'],terminal['epoch'],terminal['groups'],terminal['unknowns'])!=({cases[name]['plane']},0,370,14)")
        warm.all('ACTUAL_SINGLE_PLANE2_E0_',f"ACTUAL_SINGLE_PLANE{cases[name]['plane']}_E0_")
        warm_path=WARM_BASE/f'run_current_native_warm_{name}.py';proofs.append(warm.save(warm_path));add(pin(warm_path))
    build_plan=dict(schema='CURRENT_A23_FIVE_SOURCE_COMPLETE61_BUILD_BINDING_V1',current_full_EOF_pins=[fixed[k]for k in sorted(fixed)],compile_sources=[str(p)for p in sources],compile_commands=compile_commands,includes=includes,complete_link_command=link,original_compile_flags=FLAGS,fresh_output_root=str(BUILD_OUT),working_directory=str(build),prior_actual_complete_link=prior,prior_dispatcher_object=old_dispatcher,actual_current57_runtime_origin={'actual_summary_pin':pin(b_report_path),'actual_binding_pin':pin(b_binding_path),'actual_Dragon_pin':pin(B_OUT/'runtime/Dragon')},A_physical_inputs=cases['A2']['physical_inputs'],planned_five_Source_to_object_bindings=[dict(source_pin=pin(p),future_object_path=str(build/(p.stem+'.o')),actual_origin_required=True)for p in sources],complete_ordered_link_input_count=61,unchanged57_uses_only_KDR_same_order_replacement=True,new_object_count=4,original_four_archive_order_retained=True,initial_full_fresh_2GiB_history_reserve=True,Source_only=True,compile_or_link_or_transport_executed=False,three_plane_qualified=False,GLOBAL_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    build_plan['requires_host_process_metadata_access']=True
    plan_path=BUILD_BASE/'CURRENT_A23_COMPLETE61_BUILD_BINDING.json';write(plan_path,build_plan);add(pin(plan_path))
    binding=dict(old_bind)
    for k in ['current_B57_Dragon','actual_B57_build_summary','actual_B57_build_binding','actual_B57_build_declaration','actual_new_B_runtime_Source_object_origins','exact_warm_deck','physical_inputs','corrected_staging_role_addendum','current_warm_B_native_producer_qualified']:binding.pop(k,None)
    binding.update(schema='CURRENT_COMPLETE_A23_ENTRY_AND_BOUNDED_PRODUCER_HOST_SOURCE_BINDING_V1',planned_A23_61_build_binding_pin=pin(plan_path),actual_A1_single_plane_report_pin=pin(a1_report_path),cases=cases,current_A23_61_Dragon=None,actual61_PASS_required_before_any_case_child=True,initial_fresh_2GiB_history_reserve_required=True,current_warm_A2_native_producer_qualified=False,current_warm_A3_native_producer_qualified=False,new_three_plane_operator_controls_pending=True,new_operator_is_not_called_by_single_plane_warm_cases=True,old17_covers_unchanged_nine_component_objects_only=True)
    binding.update(planned_A23_61_build_host_pin=pin(build_host),requires_host_process_metadata_access=True)
    binding['fixed_current_pins']=[fixed[k]for k in sorted(fixed)]
    bind_path=WARM_BASE/'CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json';write(bind_path,binding)
    proof=dict(schema='COMPLETE_A23_BOUNDED_HOST_SOURCE_DERIVATION_ONLY_V1',sources=proofs,planned_build_binding_pin=pin(plan_path),planned_case_binding_pin=pin(bind_path),actual_A1_source_and_inputs_only_not_case_qualification=pin(a1_report_path),all_resources_guards_flags_thresholds_preserved=True,new_initial_full_fresh2GiB_preflight=True,future_actual61_report_is_mandatory_explicit_CLI_not_directory_scan=True,cases=('A2','A3'),compiled_or_business_executed=False)
    proof_path=WARM_BASE/'COMPLETE_A23_HOST_SOURCE_BYTE_INVERSE.json';write(proof_path,proof)
    print(json.dumps(dict(status='COMPLETE_A23_SOURCE_HOSTS_WRITTEN_NO_CHILD',fixed_fullEOF_count=len(fixed),build_host=pin(build_host),build_plan=pin(plan_path),case_binding=pin(bind_path),proof=pin(proof_path),actual_numeric_or_compiler_child_executed=False)))
if __name__=='__main__':main()
