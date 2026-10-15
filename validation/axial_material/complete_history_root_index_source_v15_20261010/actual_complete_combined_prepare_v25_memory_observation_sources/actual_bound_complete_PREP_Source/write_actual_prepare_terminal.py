'UNREADY SOURCE ONLY complete V25 Root PREP postclose metadata writer. Root must first bind actual Q/canonical and all required future Source values, freeze this writer in D, then record a genuine strict closed terminal before executing it. All original success and failure branches, complete streams/namespaces/inputs, caps and scientific boundaries remain required. Source supplies no actual result or qualification.'
import hashlib
import json
import os
from pathlib import Path
import stat
import time

FUTURE_V25_CANONICAL_SHA='47a3c90cb172ed20483c377851e770f58d7b0f6a75670e3c9f79008f9375e243'

BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
D=BASE/'actual_complete_combined_prepare_v25_memory_observation_sources'
E=BASE/'actual_complete_combined_prepare_v25_memory_observation_receipts'
H=ART/'axial-material-complete-combined-prepare-host-v25-memory-observation-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-memory-observation-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-memory-observation-20261010'
FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation.py')
FACTORY_SHA=FUTURE_V25_CANONICAL_SHA
SOURCE_BINDING_STATUS='READY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND'

BUILD_MEMORY_DIAGNOSTIC_CONTRACT = {'schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_OUTPUT_CONTRACT_V1', 'relative_path': 'build_memory_diagnostic.jsonl', 'row_schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_ROW_V1', 'phases': ['run_build', 'declaration_admission', 'before_build_link', 'before_metadata_objects', 'before_metadata_executable', 'before_metadata_dependencies', 'run_finally'], 'points': ['declaration_enter', 'declaration_return', 'commands_constructed', 'execute_enter', 'execute_return', 'environment_enter', 'environment_return', 'complete_input_enter', 'specs1_enter', 'specs1_return', 'owned1_enter', 'owned1_return', 'current_before_enter', 'current_before_return', 'verify_graph_enter', 'verify_graph_return', 'snapshot_enter', 'snapshot_return', 'trace_digest_enter', 'trace_digest_return', 'specs2_enter', 'specs2_return', 'current_after_enter', 'current_after_return', 'owned2_enter', 'owned2_return', 'graph2_enter', 'graph2_return', 'bindings_enter', 'bindings_return', 'lengths_enter', 'lengths_return', 'complete_input_return', 'archive_resources_return', 'normal_pre_inventory'], 'max_rows': 256, 'max_line_bytes_including_newline': 4096, 'max_bytes': 1048576, 'open_flags': 'O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW', 'mode_octal': '0600', 'one_parent_descriptor': True, 'write_only': True, 'read_during_active_input_audit': False, 'last_normal_marker': 'normal_pre_inventory', 'close_before_original_OUT_inventory': True, 'no_append_after_close': True, 'ru_maxrss_semantics': 'DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK', 'diagnostic_runtime_dependency_provenance': 'FUTURE_ROOT_SOURCE_BIND_AND_PRELAUNCH_ENVIRONMENT_WITNESS_REQUIRED', 'actual_runtime_pin': None, 'current_RSS_qualified': False, 'whole_INPUT_build_native_or_science_qualified': False}

def memory_diagnostic_declaration(d):
    expected=BUILD_MEMORY_DIAGNOSTIC_CONTRACT
    actual=d.get('build_memory_diagnostic_output_contract')
    if json.dumps(actual,sort_keys=True,allow_nan=False)!=json.dumps(expected,sort_keys=True,allow_nan=False):
        raise ValueError('exact declared write-only bounded output diagnostic contract required')
    forecast=d['complete_archive_forecast']
    fields=('copied_SOURCE_metadata_bound','trim_whole_component_metadata_and_trace_bound','full_graph_and_creation_trace_bound','combined_runtime_and_link_transient_bound','complete_raw_tools_and_closeout_bound','diagnostic_max_bytes','total_bound')
    if any(type(forecast[k]) is not int or forecast[k]<0 for k in fields):
        raise ValueError('exact integer complete forecast and diagnostic reservation required')
    if forecast['diagnostic_max_bytes']!=expected['max_bytes'] or forecast['total_bound']!=sum(forecast[k] for k in fields[:-1]) or forecast['total_bound']>=2*2**30:
        raise ValueError('all original complete forecast components plus diagnostic remain below original 2GiB')
    return actual

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    p=Path(p); before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular metadata file required')
    with p.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('full EOF source changed')
    return dict(path=str(p),sha256=digest,identity=before)

def short(p):
    q=pin(p); return dict(path=q['path'],sha256=q['sha256'])

def write(p,v):
    with Path(p).open('x') as f: json.dump(v,f,indent=2,allow_nan=False);f.write('\n')

def inventory(root):
    files={};directories=[]
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs:
            p=Path(folder)/name
            if p.is_symlink() or not p.is_dir(): raise ValueError('regular SOURCE directory required')
            directories.append(str(p.relative_to(root)))
        for name in names:
            p=Path(folder)/name; files[str(p.relative_to(root))]=pin(p)['sha256']
    return dict(files=files,symlinks={},directories=sorted(directories))

def complete_namespace(root):
    files={};directories=[];symlinks={}
    for folder,dirs,names in os.walk(root,followlinks=False):
        for name in dirs:
            p=Path(folder)/name
            if p.is_symlink(): symlinks[str(p.relative_to(root))]=dict(identity=identity(p),literal_target=os.readlink(p))
            else: directories.append(dict(path=str(p.relative_to(root)),identity=identity(p)))
        for name in names:
            p=Path(folder)/name
            if p.is_symlink(): symlinks[str(p.relative_to(root))]=dict(identity=identity(p),literal_target=os.readlink(p))
            else: files[str(p.relative_to(root))]=pin(p)
    return dict(root=str(root),files=files,directories=directories,symlinks=symlinks)

def main():
    if SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_Q_AND_CANONICAL_SOURCE_BOUND' or FACTORY_SHA is None:
        raise ValueError('UNREADY Source template: no Root PREP result metadata reads before actual Q and canonical Source binding')
    actual=json.loads((E/'Root_actual_prepare_tool_terminal_return.json').read_text())
    observed=actual['terminal_tool_return']
    if actual['closed'] is not True or type(observed.get('exit_code')) is not int or observed['exit_code']!=0 or 'session_id' in observed:
        raise ValueError('Root actual typed EXIT0 closed tool return required')
    h=json.loads((H/'result.json').read_text())
    w=json.loads((H/'run/prepare.watchdog.json').read_text())
    d=json.loads((O/'declaration.json').read_text());memory_diagnostic_declaration(d)
    if os.path.lexists(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']):raise ValueError('BUILD-only diagnostic absent after PREP')
    cp=d['actual_external_prepare_terminal_contract']
    if pin(FACTORY)['sha256']!=FACTORY_SHA or cp['root']!=str(T) or cp['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25_ACTUAL_EXTERNAL_PREP_RETURN_V1':
        raise ValueError('fixed new formal source required')
    if type(w['returncode']) is not int or w['returncode']!=0 or w['limit_failure'] is not None or w['command']!=cp['command'] or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True:
        raise ValueError('genuine actual whole PREP PASS required')
    if len(h['stage_records'])!=1 or h['stage_records'][0]['status']!='PASS' or not (0<=w['sampled_peak_rss_mib']<512 and h['whole_seconds']<1800 and w['elapsed_seconds']<=600):
        raise ValueError('original caps required')
    if (h['whole_wall_cap_seconds'],h['stage_wall_cap_seconds'],h['rss_cap_mib'],h['archive_cap_bytes'],h['threads'],h['children_at_once'],h['retries'])!=(1800,600,512,2*2**30,1,1,0):
        raise ValueError('original complete PREP caps unchanged')
    for q in h['input_sources']+[h['original_helper'],h['resource_factory']]:
        if pin(q['path'])!=q: raise ValueError('all original full EOF inputs unchanged')
    source_inventory=inventory(S)
    if source_inventory!=d['source_inventory']: raise ValueError('all SOURCE files/dirs identical')
    declaration=short(O/'declaration.json')
    if json.loads((H/'run/prepare.log').read_text())!=dict(declaration=declaration['path'],declaration_sha256=declaration['sha256']):
        raise ValueError('complete actual child merged stream required')
    if (E/'parent_stderr.log').stat().st_size!=0 or os.path.lexists(T) or (O/'seal.json').exists():
        raise ValueError('fresh terminal and INPUT-only PREP boundary required')
    T.mkdir()
    copies=[(H/'run/prepare.log','actual_child_merged_stdout_stderr.json'),(E/'parent_stderr.log','actual_external_host_stderr.txt'),(E/'parent_stdout.log','actual_external_host_stdout.json'),(E/'Root_actual_prepare_tool_terminal_return.json','actual_external_Root_tool_terminal.json')]
    for src,name in copies:
        with (T/name).open('xb') as f: f.write(src.read_bytes())
        if pin(src)['sha256']!=pin(T/name)['sha256']: raise ValueError('byte-exact original stream required')
    write(T/'Root_actual_SOURCE_inventory.json',source_inventory)
    value=dict(schema=cp['schema'],record_producer='root',successful_declaration_input_observed=True,actual_tool_terminal_return_observed=True,record_written_after_actual_terminal_return=True,returncode=observed['exit_code'],actual_tool_result=observed,source=short(FACTORY),command=cp['command'],declaration=declaration,input_graph=d['input_graph'],historical_whole_component_body=d['historical_whole_component_body'],historical_PREP=d['historical_PREP'],actual_last_cprime_trim_component_INPUT=d['actual_last_cprime_trim_component_INPUT'],trim_component_API_executed_in_this_PREP=d['trim_component_API_executed_in_this_PREP'],source_inventory=short(T/'Root_actual_SOURCE_inventory.json'),full_stdout=short(T/'actual_child_merged_stdout_stderr.json'),full_stderr=short(T/'actual_external_host_stderr.txt'),full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR',full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR',separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False,actual_child_watchdog=pin(H/'run/prepare.watchdog.json'),actual_root_host_terminal_tool_return=pin(T/'actual_external_Root_tool_terminal.json'),actual_root_host_launchargs=actual['actual_launch_arguments'],actual_root_host_stdout=pin(T/'actual_external_host_stdout.json'),original_executor_merged_capture_source=pin('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py'),original_executor_capture_semantics='705 source subprocess.Popen stderr=subprocess.STDOUT; full actual merged child stream and separate real external host stderr preserved',observed_at_unix=time.time())
    for key in cp['false_fields']: value[key]=False
    write(T/'declaration_terminal_return.json',value)
    namespaces=[complete_namespace(root) for root in (H,S,O,T,D)]
    write(E/'Root_actual_complete_prepare_namespace_manifest.json',dict(schema='ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1',namespaces=namespaces,all_original_inputs_fresh_full_EOF_SHA7ID_unchanged=h['input_sources']+[h['original_helper'],h['resource_factory']],canonical_factory=pin(FACTORY),no_build_or_native_credit=True))
    total=sum(p.stat().st_size for root in (H,S,O,T,D,E) for p in root.rglob('*') if p.is_file() and not p.is_symlink())+FACTORY.stat().st_size
    if not total<2*2**30: raise ValueError('joint original 2GiB archive cap exceeded')
    summary=dict(schema='ROOT_V25_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1',status='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD',actual_root_terminal=pin(E/'Root_actual_prepare_tool_terminal_return.json'),actual_host_result=pin(H/'result.json'),formal_PREP_terminal=pin(T/'declaration_terminal_return.json'),actual_declaration=pin(O/'declaration.json'),actual_input_graph=pin(O/'input_graph.json'),all_source_files_verified_count=len(source_inventory['files']),all_original_pinned_inputs_unchanged_count=len(h['input_sources'])+2,whole_seconds=h['whole_seconds'],child_seconds=w['elapsed_seconds'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],whole_wall_cap_seconds=1800,stage_wall_cap_seconds=600,rss_mib=512,joint_archive_bytes=total,joint_archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children=1,retries=0,new_five_stage_build_executed=False,whole_combined_INPUT_admitted=False,new_native_transport_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False)
    summary['Root_actual_terminal']=summary['actual_root_terminal']
    summary['actual_complete_input_graph']=summary['actual_input_graph']
    summary['actual_complete_creation_trace']=pin(O/'input_creation_python_open_trace.json')
    summary['namespace_manifest']=pin(E/'Root_actual_complete_prepare_namespace_manifest.json')
    summary['original_caps_preserved']=True
    summary['original_five_build_stages_executed']=False
    summary['native_RSS_qualified']=False
    summary['cleanup_performed']=False
    write(E/'Root_actual_complete_combined_prepare_summary.json',summary)
    print(json.dumps({k:summary[k] for k in ('status','whole_seconds','child_seconds','sampled_peak_rss_mib','joint_archive_bytes','all_source_files_verified_count')}))

if __name__=='__main__':main()
