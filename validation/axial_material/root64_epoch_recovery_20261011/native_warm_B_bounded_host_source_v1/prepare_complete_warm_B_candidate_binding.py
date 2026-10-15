#!/usr/bin/env python3
"""Pure stdlib complete Source writer/fullEOF audit. Never compiles or runs hosts."""
import ast
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BASE=Path(__file__).resolve().parent
BUILD=ART/'axial-material-new-REAL64-native-B-complete57-route-build-only-20261012'
BCASE=REC/'native_warm_B_case_source_v1'
BDECL=REC/'native_warm_B_runtime_build_source_v1/CURRENT_B_COMPLETE57_BUILD_BINDING.json'
BDECL_SHA='81469aedf71439ecf83994cc2a45c39670bab3fdb869d551de4cdfd233e00904'

def pin(path):
    path=Path(path);s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(s.st_mode):raise RuntimeError('regular file only')
    with path.open('rb') as f:
        def current():
            v=os.fstat(f.fileno());return [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]
        if current()!=before:raise RuntimeError('opened7ID')
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        if current()!=before:raise RuntimeError('fullEOF7ID')
    v=path.lstat()
    if [v.st_dev,v.st_ino,v.st_mode,v.st_nlink,v.st_size,v.st_mtime_ns,v.st_ctime_ns]!=before:raise RuntimeError('after7ID')
    return dict(path=str(path),sha256=sha,size_bytes=s.st_size,identity=before)

def write(path,data):
    if path.exists()or path.is_symlink():raise RuntimeError('fresh binding once, no overwrite or review-history factory')
    if (BASE/'COMPLETE_WARM_B_CANDIDATE_SOURCE_FREEZE.json').exists():raise RuntimeError('frozen package immutable')
    with path.open('x') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def normalized(node):return ast.dump(node,include_attributes=False)

def main():
    parser=argparse.ArgumentParser()
    for prefix in ('build-summary','build-binding'):
        parser.add_argument('--'+prefix,required=True)
        parser.add_argument('--'+prefix+'-sha256',required=True)
        parser.add_argument('--'+prefix+'-seven-id',required=True)
    args=parser.parse_args()
    summary_path=Path(args.build_summary);build_bind_path=Path(args.build_binding)
    if summary_path!=BUILD/'Root_actual_build_only_summary.json' or build_bind_path!=BUILD/'Root_current_compile_only_binding.json':
        raise RuntimeError('explicit independent B actual report and binding paths required')
    for path,sha,seven in [(summary_path,args.build_summary_sha256,args.build_summary_seven_id),(build_bind_path,args.build_binding_sha256,args.build_binding_seven_id)]:
        row=pin(path)
        if row['sha256']!=sha or row['identity']!=json.loads(seven):raise RuntimeError('external explicit B actual report fullEOF SHA/7ID')
    summary=json.loads(summary_path.read_text());build_bind=json.loads(build_bind_path.read_text())
    declaration_pin=pin(BDECL)
    if declaration_pin['sha256']!=BDECL_SHA:raise RuntimeError('exact frozen complete B build declaration')
    declaration=json.loads(BDECL.read_text())
    flags=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']
    if summary['schema']!='ACTUAL_COMPLETE_NATIVE_B_HANDLER_DISPATCHER57_BUILD_ONLY_V1' or summary['status']!='ACTUAL_B_TWO_COMPILE_AND_COMPLETE57_DRAGON_LINK_CLOSED0_ONLY' or summary['failure'] is not None or summary['after_check_error'] is not None or summary['Dragon_linked'] is not True or summary['transport_executed'] is not False:
        raise RuntimeError('actual independent B two-compile and complete57 Dragon link required')
    expected=declaration['compile_commands']+[declaration['complete_link_command']]
    if build_bind['complete_ordered_link_input_count']!=57 or len(summary['records'])!=3 or any(r['status']!='PASS'for r in summary['records']) or [r['command']for r in summary['records']]!=expected or build_bind['actual_commands']!=expected:
        raise RuntimeError('complete exact three current B build stages and57 ordered link inputs')
    if len(expected[-1][3:-2])!=57 or expected[-1][-6:-2]!=declaration['prior_actual_complete_link'][-6:-2] or declaration['original_compile_flags']!=flags or build_bind['original_flags']!=flags:
        raise RuntimeError('original nine flags and complete original archive order')
    if summary['original_guard_class']!='OwnRSSSerialExecutor' or summary['original_guard_MRO_unchanged'] is not True or not 0<=summary['SELF_peak_bytes']<512*2**20 or not 0<summary['wall_seconds']<1800:
        raise RuntimeError('actual B build original SELF and whole guard')
    if summary['fixed_current_pins']!=build_bind['fixed_current_pins'] or len(summary['actual_watchdog_checks'])!=3:
        raise RuntimeError('actual B build owning input and watchdog inventory')
    for record,receipt in zip(summary['records'],summary['actual_watchdog_checks']):
        watch=Path(receipt['path']);wanted=BUILD/(record['label']+'.watchdog.json')
        if watch!=wanted or pin(watch)['sha256']!=receipt['sha256']:raise RuntimeError('actual B build watchdog fullfile')
        w=json.loads(watch.read_text());log=BUILD/(record['label']+'.log')
        if w['returncode']!=0 or w['limit_failure'] is not None or w['command']!=record['command'] or w['rss_cap_mib']!=512 or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True:
            raise RuntimeError('actual B build true original zero-return own-child guard')
        if not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=record['wall_cap_seconds']<=600 or not 0<=w['sampled_peak_rss_mib']<512 or pin(log)['sha256']!=record['log_sha256']:
            raise RuntimeError('actual B build original resource limits and complete log')
    origins_B=summary['actual_new_Source_to_object_origins']
    if len(origins_B)!=2:raise RuntimeError('actual complete B handler and dispatcher Source/object origins')
    input_table={r['path']:r for r in summary['fixed_current_pins']};output_table={r['path']:r for r in summary['output_pins']}
    for index,row in enumerate(origins_B):
        command=expected[index];source_pin=row['source_pin'];object_pin=row['object_pin']
        if source_pin['path']!=str(BCASE/('AXNCASEB64.f90'if index==0 else 'KDRDRV.F')) or source_pin!=pin(source_pin['path']) or input_table.get(source_pin['path'])!=source_pin or object_pin!=pin(object_pin['path']) or output_table.get(object_pin['path'])!=object_pin:
            raise RuntimeError('actual full frozen B Source-to-object binding')
        if row['actual_compile_record']!=summary['records'][index] or row['actual_watchdog_check']!=summary['actual_watchdog_checks'][index] or row['original_nine_flags']!=flags or command[1:10]!=flags or command[command.index('-c')+1]!=source_pin['path'] or command[command.index('-o')+1]!=object_pin['path'] or object_pin['path']not in expected[-1]:
            raise RuntimeError('actual B Source compiler command and final runtime object provenance')
    source=build_bind['fixed_current_pins'];fixed={}
    for row in source:
        actual=pin(row['path'])
        if actual!=row:raise RuntimeError('actual current B57 fullpin differs: '+row['path'])
        if actual['path'] in fixed and fixed[actual['path']]!=actual:raise RuntimeError('duplicate inconsistent fullpin')
        fixed[actual['path']]=actual
    for row in summary['output_pins']+[pin(summary_path),pin(build_bind_path),declaration_pin]:
        if pin(row['path'])!=row:raise RuntimeError('actual current B build output/origin fullpin')
        fixed[row['path']]=row
    dragon=next(p for p in summary['output_pins']if p['path']==str(BUILD/'runtime/Dragon'))
    if pin(dragon['path'])!=dragon:raise RuntimeError('actual independent B runtime fullpin')
    addendum_path=BCASE/'COMPLETE_B_SOURCE_BYTE_INVERSE_AND_PHYSICAL_METADATA.json'
    add=json.loads(addendum_path.read_text());manifest_path=BASE/'COMPLETE_A_V3_TO_B_V1_SOURCE_BYTE_INVERSE.json'
    if add['schema']!='SOURCE_ONLY_INDEPENDENT_B_PLANE2_E0_MINIMAL_COMPLETE_CANDIDATE_V1' or add['new_case']['case_name']!='R64WARM-B-V1' or (add['new_case']['plane'],add['new_case']['epoch'])!=(2,0):
        raise RuntimeError('actual independent B complete physical Source declaration')
    for row in add['sources']:
        wanted={k:row['new_source'][k]for k in ('path','sha256','size_bytes','identity')}
        if pin(wanted['path'])!=wanted:raise RuntimeError('frozen complete B Source changed')
        fixed[wanted['path']]=wanted
    if pin(BASE/'verify_native_B_archive64.f90')['sha256']!=pin(BCASE/'verify_native_B_archive64.f90')['sha256']:
        raise RuntimeError('probe must reuse frozen complete B verifier bytes')
    physical=[]
    roles={'material':'readonly_material','geometry':'readonly_geometry','warm_type4_seed':'readonly_seed_archive','readonly_original_rays_reference':'readonly_rays_reference'}
    for row in add['B_physical_inputs']:
        wanted={k:row['current_full_EOF_pin'][k]for k in ('path','sha256','size_bytes','identity')}
        actual=pin(wanted['path'])
        if actual!=wanted:raise RuntimeError('original independent B full physical readonly pin')
        physical.append(dict(role=roles[row['role']],pin=actual,owned_runtime_relative_path=row['owned_future_runtime_relative_path']))
    if len(physical)!=4 or {r['role']for r in physical}!=set(roles.values()):raise RuntimeError('full four B inputs including readonly rays reference')
    if next(r for r in physical if r['role']=='readonly_rays_reference')['owned_runtime_relative_path'] is not None:
        raise RuntimeError('real SALT output must not be staged from original rays')
    core_path=ART/'axial-material-new-ROOT64-native-core-controls-20261011/Root_actual_compile_only_summary.json'
    ingress_path=ART/'axmat-native-real64-warm-ingress-20261011/Root_actual_compile_only_summary.json'
    applicability=[]
    for name,path,fragments in [('core83',core_path,['/new_source/SPOR64_BOOT64.f90','/new_source/SPOR64_VERIFY.f90','/new_source/SPOR64_RCONTRACT.f90','/axial-material-new-ROOT64-BOOT-compile-only-20261011/build/']),
       ('AB_ingress',ingress_path,['/native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90','/axial-material-new-REAL64-producer-compile-only-20261011/build/'])]:
        report=json.loads(path.read_text())
        matches=[r for r in report['fixed_current_pins']if any(f in r['path']for f in fragments) and r['path']in fixed]
        if not matches:raise RuntimeError('no actual covered Source/object applicability')
        for row in matches:
            if row!=fixed[row['path']]or pin(row['path'])!=row:raise RuntimeError('actual same Source/object applicability')
            applicability.append(dict(report=name,pin=row))
        for row in report['fixed_current_pins']+report['output_pins']:
            if pin(row['path'])!=row:raise RuntimeError('saved actual prerequisite complete pin')
            fixed[row['path']]=row
    origins=[]
    for origin_path,covered in [(ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/Root_actual_compile_only_summary.json',
          ['SPOR64_BOOT64.o','SPOR64_RCONTRACT.o','SPOR64_VERIFY.o']),
          (ART/'axial-material-new-REAL64-producer-compile-only-20261011/Root_actual_compile_only_summary.json',['AXMAT_NATIVE_PRODUCER_CHAIN.o'])]:
        origin=json.loads(origin_path.read_text())
        if origin['failure'] is not None or any(r['status']!='PASS'for r in origin['records']):raise RuntimeError('actual covered component compile origin')
        inputs={r['path']:r for r in origin['fixed_current_pins']};outputs={r['path']:r for r in origin['output_pins']}
        for record in origin['records']:
            cmd=record['command']
            if '-c'not in cmd or '-o'not in cmd:continue
            src=cmd[cmd.index('-c')+1];obj=cmd[cmd.index('-o')+1]
            if Path(obj).name not in covered:continue
            if inputs[src]!=pin(src) or outputs[obj]!=pin(obj) or fixed[obj]!=outputs[obj]:raise RuntimeError('actual complete Source-to-covered-object binding')
            if cmd[1:10]!=build_bind['original_flags']:raise RuntimeError('original covered compile complete9 flags')
            origins.append(dict(actual_compile_origin_report=pin(origin_path),source_pin=inputs[src],object_pin=outputs[obj],actual_compile_record=record))
        for row in origin['fixed_current_pins']+origin['output_pins']+[pin(origin_path)]:
            if pin(row['path'])!=row:raise RuntimeError('current complete actual covered compile inputs/outputs')
            fixed[row['path']]=row
    if len(origins)!=4:raise RuntimeError('all four actual covered Source/object compile origins')
    required17_names={'SPOR64_BOOT64.o','SPOR64_RCONTRACT.o','SPOR64_VERIFY.o',
       'SPOR64_BOOT_CANONICAL64.o','SPOR64_BOOT_CONTEXT64.o','SPOR64_BOOTQ64.o',
       'SPOR64_B2H.o','SPOR64_BOOT_PUBLISH64.o','SPOR64_BOOT_PROJECT64.o'}
    current_link=summary['records'][-1]['command']
    required17=[pin(p)for p in current_link if Path(p).name in required17_names]
    if len(required17)!=9 or {Path(p['path']).name for p in required17}!=required17_names:
        raise RuntimeError('all nine exact current production objects for17 applicability')
    actual17_path=ART/'axial-material-new-ROOT64-full-connected17-expected-planes-v4-20261012/Root_actual_compile_only_summary.json'
    actual17=json.loads(actual17_path.read_text())
    if actual17['schema']!='ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V2' or actual17['status']!='ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY' or actual17['failure'] is not None or actual17['after_check_error'] is not None:
        raise RuntimeError('Root explicitly selected genuinely complete current17 PASS required')
    if len(actual17['records'])!=20 or any(r['status']!='PASS'for r in actual17['records']) or actual17['actual_logical_control_count']!=17 or actual17['actual_run_phase_count']!=18 or actual17['all17_original_names_exercised']is not True:
        raise RuntimeError('complete actual20 PASS /17 logical/18 phases')
    authority_keys=('actual_current_control_binding_pin','actual_current_control_source_pin','actual_current_control_freeze_pin')
    baseline17=[pin(actual17_path)]+[actual17[k]for k in authority_keys]
    table17={row['path']:row for row in actual17['fixed_current_pins']}
    oracle=json.loads(Path(actual17['actual_current_control_binding_pin']['path']).read_text())
    if [row['command']for row in actual17['records']]!=[oracle['planned_compile_command'],oracle['planned_link_command']]+oracle['planned_run_commands'] or oracle['planned_output_root']!=str(actual17_path.parent):
        raise RuntimeError('true current owning17 exact20 command/oracle binding')
    if oracle['source_pin']!=actual17['actual_current_control_source_pin']:
        raise RuntimeError('actual control Source authority differs')
    for row in required17:
        if table17.get(row['path'])!=row or row['path']not in oracle['planned_link_command']:
            raise RuntimeError('all nine actual17 objects equal current B57 production objects')
    for row in baseline17[1:]:
        if table17.get(row['path'])!=row or pin(row['path'])!=row:raise RuntimeError('full exact actual17 authority pin')
    for row in actual17['fixed_current_pins']+actual17['output_pins']+baseline17:
        if pin(row['path'])!=row:raise RuntimeError('actual17 current complete dependency/output fullEOF pin')
        if row['path']in fixed and fixed[row['path']]!=row:raise RuntimeError('actual17 repeated dependency mismatch')
        fixed[row['path']]=row
    support=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py'
    original_host=REC/'run_current_ROOT64_native_core_controls.py'
    original=original_host.read_text();candidate=(BASE/'guarded_warm_B_common.py').read_text()
    def resource_class(text):return next(n for n in ast.walk(ast.parse(text))if isinstance(n,ast.ClassDef)and n.name=='Resources')
    if normalized(resource_class(original))!=normalized(resource_class(candidate)):
        raise RuntimeError('original full Resources body changed')
    if ast.get_source_segment(original,resource_class(original))!=ast.get_source_segment(candidate,resource_class(candidate)):
        raise RuntimeError('original complete Resources literal bytes changed')
    support_values={}
    for n in ast.parse(support.read_text()).body:
        if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and isinstance(n.value,ast.Constant):support_values[n.targets[0].id]=n.value.value
    bounded=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py'
    compiler=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
    for p in [summary_path,build_bind_path,addendum_path,manifest_path,core_path,ingress_path,support,original_host,dragon['path'],bounded,compiler,
      *[p for p in BASE.glob('*')if p.is_file() and p.suffix in ('.py','.f90')]]:
        row=pin(p);fixed[row['path']]=row
    for row in physical:fixed[row['pin']['path']]=row['pin']
    boot=ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build'
    producer=ART/'axial-material-new-REAL64-producer-compile-only-20261011/build'
    inc=[str(producer),str(boot),str(ROOT/'Ganlib/lib/Darwin_arm64/modules')]
    link_paths=[producer/'AXMAT_NATIVE_PRODUCER_CHAIN.o',boot/'SPOR64_BOOT64.o',boot/'SPOR64_RCONTRACT.o',boot/'SPOR64_VERIFY.o',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    for directory in inc:
        for p in sorted(Path(directory).glob('*.mod')):
            row=pin(p);fixed[row['path']]=row
    deps=[pin(p)for p in link_paths]
    for row in deps:fixed[row['path']]=row
    binding=dict(schema='CURRENT_COMPLETE_WARM_B_ENTRY_AND_BOUNDED_PRODUCER_HOST_SOURCE_BINDING_V1',
      original_stage_wall_cap_seconds=600,whole_wall_cap_seconds=1800,SELF_and_each_own_child_RSS_cap_bytes=512*2**20,
      threads=1,children_at_once=1,retries=0,fresh_output_cap_bytes=2*2**30,history_cap_bytes=96*2**30,
      filesystem_floor_bytes=8*2**30,original_cold_reserve_bytes=20971764748,
      current_B57_Dragon=dragon,actual_B57_build_summary=pin(summary_path),actual_B57_build_binding=pin(build_bind_path),
      actual_B57_build_declaration=declaration_pin,actual_new_B_runtime_Source_object_origins=origins_B,
      actual_core83_report=pin(core_path),actual_AB_ingress_report=pin(ingress_path),
      covered_existing_control_source_and_object_applicability=applicability,
      actual_covered_Source_object_compile_origins=origins,
      seventeen_required_same_production_object_pins=required17,
      current_exact_17_actual_PASS_Source_binding_freeze_and_report_pins=baseline17,selected_actual_current17_report=pin(actual17_path),
      current17_actual_status=actual17['status'],current17_actual_failure=actual17['failure'],
      current17_pending=False,eligibility_requires_external_explicit_Root_selected_actual_PASS_report_fullpin=True,
      mandatory_current17_summary_schema='ACTUAL_NEW_FULL_CONNECTED17_SYNTHETIC_COMPONENT_CONTROLS_ROOT_V2',
      mandatory_current17_status='ACTUAL_CURRENT17_CONNECTED_COMPONENT_CONTROLS_CLOSED0_ONLY',
      selected_current17_actual_PASS_output_root=str(actual17_path.parent),
      original_guard_Source=pin(ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py'),
      original_support=pin(support),original_bounded=pin(bounded),compiler=pin(compiler),original_nine_flags=build_bind['original_flags'],
      physical_inputs=physical,exact_warm_deck=pin(BCASE/'ROOT64_NEW_WARM_B_20261012.x2m'),
      corrected_staging_role_addendum=pin(addendum_path),probe_include_directories=inc,probe_link_dependencies=deps,
      Source_only=True,compiler_or_transport_executed=False,actual_current17_PASS_claimed=True,
      current_CLE_route_controls_executed=False,current_warm_B_native_producer_qualified=False,
      three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
      fixed_current_pins=[fixed[k]for k in sorted(fixed)])
    deck=binding['exact_warm_deck'];fixed[deck['path']]=deck;binding['fixed_current_pins']=[fixed[k]for k in sorted(fixed)]
    if binding['original_nine_flags']!=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']:
        raise RuntimeError('original complete9 numeric flags')
    write(BASE/'CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json',binding)
    # The one complete inverse manifest above carries all Source derivation evidence.
    print(json.dumps(dict(status='SOURCE_BINDING_WRITTEN_NO_CHILD',fixed_fullEOF_pins=len(fixed),binding=pin(BASE/'CURRENT_WARM_B_COMPLETE_HOST_SOURCE_BINDING.json'),controls_or_warm_executed=False)))
if __name__=='__main__':main()
