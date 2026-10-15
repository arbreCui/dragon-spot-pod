"""Inspect only closed prepare records, immutable sources and SOURCE inventory."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';HERE=Path(__file__).parent
BASE=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
RECEIPTS=BASE/'actual_prepare_receipts'
SOURCE=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'
OUT=ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'
HOST=ART/'axial-material-complete-prepare-host-v15-20261010'
EVIDENCE=ART/'axial-material-complete-prepare-evidence-v15-20261010'
DECL=OUT/'declaration.json'
OLD_SOURCE=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-admission-v14b-20261010'
OLD_OUT=ART/'axial-material-sender-contiguous-flux-window-streaming-sha-build-v14b-20261010'
pins={};raws={};checks={}

def identity(path):
    s=Path(path).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def load_pin(path,wanted=None,recorded_identity=None):
    path=Path(path);before=identity(path)
    assert stat.S_ISREG(before[2]),str(path)
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    assert before==identity(path) and len(raw)==before[4],str(path)
    assert wanted is None or sha==wanted,str(path)
    assert recorded_identity is None or before==recorded_identity,str(path)
    pin=dict(path=str(path),sha256=sha,size_bytes=len(raw),identity=before)
    if str(path) in pins:assert pins[str(path)]==pin
    pins[str(path)]=pin;raws[str(path)]=raw
    return raw

def obj(path,wanted=None,recorded_identity=None):return json.loads(load_pin(path,wanted,recorded_identity))
def ref(value):
    load_pin(value['path'],value['sha256'],value.get('identity'))
def check(name,condition):
    checks[name]=bool(condition);assert condition,name

summary=obj(RECEIPTS/'Root_actual_prepare_evidence_and_summary.json')
root=obj(summary['Root_actual_terminal']['path'],summary['Root_actual_terminal']['sha256'])
stdout=obj(summary['actual_root_stdout']['path'],summary['actual_root_stdout']['sha256'])
ref(summary['actual_root_stderr'])
host=obj(stdout['host_result']['path'],stdout['host_result']['sha256'],stdout['host_result']['identity'])
child=obj(host['actual_child_prepare_result']['path'],host['actual_child_prepare_result']['sha256'],host['actual_child_prepare_result']['identity'])
watch=obj(host['actual_watchdog']['path'],host['actual_watchdog']['sha256'],host['actual_watchdog']['identity'])
log=obj(host['actual_full_merged_stdout_stderr']['path'],host['actual_full_merged_stdout_stderr']['sha256'],host['actual_full_merged_stdout_stderr']['identity'])
d=obj(DECL,'6dee0b453ea519beeb85abd834c22939c0f5c49565bcd3c793c6b83bf7e092a7',host['actual_declaration']['identity'])
admission=obj(host['actual_source_admission']['path'],host['actual_source_admission']['sha256'],host['actual_source_admission']['identity'])
check('actual_Root704853_session36033_terminal_f24857_strict_exit0_closed',
    root['initial']['chunk_id']=='704853' and root['initial']['session_id']==36033
    and root['terminal']['chunk_id']=='f24857' and type(root['terminal']['exit_code']) is int
    and root['terminal']['exit_code']==0 and root['session_closed'] is True
    and root['record_written_after_actual_terminal_return'] is True and root['actual_tool_terminal_return_observed'] is True)
check('actual_complete_Root_stdout_and_empty_stderr_full_SHA',
    len(raws[summary['actual_root_stderr']['path']])==0 and stdout['host_result']['path']==str(HOST/'result.json')
    and host['status']=='ACTUAL_COMPLETE_PREPARE_CLOSED_EXTERNAL_ROOT_REQUIRED')
check('actual_canonical_prepare_completed_unprofiled_no_failure',
    host['canonical_prepare_completed'] is True and host['profile_used'] is False
    and child['status']=='PREPARE_RETURNED' and child['failure'] is None
    and child['canonical_cli_completed'] is True and child['profile_used'] is False)
original=obj(ROOT/'validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/actual_component_execution_receipts/Root_actual_prepare_tool_return.json',
    'd69437dc3f3df2fc8b36adb7c3077410e6d3052e153d4568ea7e0b52ac856f82')
expected=list(original['input']['argv']);expected[1]=str(ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py')
check('actual_ten_original_CLI_parameters_exact_order_values_only_target_changed',
    len(expected)==23 and expected[2]=='prepare-build' and child['actual_canonical_argv']==expected
    and type(original['terminal']['exit_code']) is int and original['terminal']['exit_code']==0 and original['session_closed'] is True)
check('actual_child_before_after_source_bindings_unchanged',child['input_source_pins']==child['input_source_pins_after'])
for value in host['input_sources']+[host['original_helper'],host['resource_factory']]+child['input_source_pins']:ref(value)
host_source=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
host_text=load_pin(host_source,'3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7').decode()
check('actual_genuine_single_child_closed_command_and_stage',
    len(host['stage_records'])==1 and host['stage_records'][0]['status']=='PASS'
    and host['stage_records'][0]['command']==host['actual_command']==watch['command']
    and type(watch['returncode']) is int and watch['returncode']==0
    and type(watch['pid']) is int and watch['pid']>0 and watch['limit_failure'] is None
    and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
check('actual_whole1800_stage600_RSS512_archive2GiB_caps',
    (host['whole_wall_cap_seconds'],host['stage_wall_cap_seconds'],host['rss_cap_mib'],host['archive_cap_bytes'])==(1800,600,512,2*2**30)
    and 0<child['actual_child_elapsed_seconds']<watch['elapsed_seconds']<watch['wall_cap_seconds']<=host['stage_records'][0]['wall_cap_seconds']<=600
    and 0<=watch['sampled_peak_rss_mib']<512 and watch['rss_cap_mib']==512
    and 0<host['whole_elapsed_seconds']<1800 and 0<host['whole_archive_bytes']<2*2**30
    and (host['threads'],host['children_at_once'],host['retries'])==(1,1,0))
check('summary_agrees_full_actual_host_watch_declaration',
    summary['whole_host_seconds']==host['whole_elapsed_seconds'] and summary['own_child_peak_rss_mib']==watch['sampled_peak_rss_mib']
    and summary['archive_before_host_result_bytes']==host['whole_archive_bytes']
    and summary['actual_declaration']['sha256']==host['actual_declaration']['sha256']==pins[str(DECL)]['sha256'])
resource_snapshots=[host['resources_before'],host['resources_after'],host['stage_records'][0]['resource_before'],host['stage_records'][0]['resource_after']]
check('all_saved_complete_dynamic_history96GiB_free8GiB_guards_hold',all(
    s['min_free_bytes']==8*2**30 and s['artifact_budget_bytes']==96*2**30
    and 0<=s['artifact_bytes']<=96*2**30 and s['disk_free_bytes']>=8*2**30
    and s['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
    and s['resource_scope_contract']['all_declared_extras_retained'] is True
    and s['resource_scope_contract']['artifact_budget_GiB']==96 and s['resource_scope_contract']['min_free_GiB']==8
    and len(s['resource_roots'])==len(set(s['resource_roots'])) and set(s['declared_resource_roots'])<=set(s['resource_roots'])
    for s in resource_snapshots))
check('resource_before_full_reserve_held',host['resources_before']['artifact_bytes']+2*2**30<96*2**30
    and host['resources_before']['disk_free_bytes']-2*2**30>=8*2**30)
for s in resource_snapshots:
    for p in [SOURCE,OUT,HOST,EVIDENCE]:assert str(p) in s['resource_roots']
check('actual_resource_snapshots_preserve_all_declared_new_namespace_roots',True)
qref=d['root_index_resource_source_admission']['actual_resource_module_admission']
q=obj(qref['path'],'5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676')
check('complete_formal_actual_resource_qualification_retained_exact_in_both_envelopes',
    d['root_index_resource_source_admission']==admission['root_index_resource_source_admission']
    and d['root_index_resource_source_admission']['complete_actual_resource_module_admission']==q
    and q['status']=='PASS_RESOURCE_MODULE_ONLY'
    and d['root_index_resource_source_admission']['actual_resource_class_factory']==dict(path=host['resource_factory']['path'],
        sha256=host['resource_factory']['sha256'],class_name='DynamicHistoryResources',genuine_class_not_overlay=True))
helper=d['stream_environment_helper_admission']
for key in ['helper','source_patch_proof','actual_helper_controls_admission','original_helper','component_factory_parent']:ref(helper[key])
check('qualified_H7d_helper_true_source_proof_and_actual_controls_retained',
    helper==admission['stream_environment_helper_admission']
    and helper['helper']['sha256']=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3'
    and helper['source_patch_proof']['sha256']=='1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2'
    and helper['actual_helper_controls_admission']['sha256']=='16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568'
    and helper['supervisor_class_and_MRO_unchanged'] is True
    and helper['original_cache_and_sender_math_and_raw_controls_unchanged'] is True)
full_text=raws[str(ROOT/'validation/axial_material/qualify_refined_AAA_layered_full.py')].decode()
class_node=next(n for n in ast.parse(full_text).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
check('genuine_original_supervisor_source_MRO_fixed512_no_monkeypatch',
    ast.unparse(class_node.bases[0])=='SerialExecutor'
    and 'if peak>=512:' in ast.get_source_segment(full_text,class_node)
    and 'full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)' in host_text
    and 'type(runner) is not full.OwnRSSSerialExecutor' in host_text
    and host['supervisor_class_or_MRO_modified'] is False)
ref(dict(path=str(HOST/'runtime/run_bounded_dragon.py'),sha256='bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'))

def source_inventory():
    files={};symlinks={};directories=[]
    for parent,ds,fs in os.walk(SOURCE,followlinks=False):
        for name in ds+fs:
            p=Path(parent)/name;rel=str(p.relative_to(SOURCE));mode=p.lstat().st_mode
            if stat.S_ISLNK(mode):symlinks[rel]=os.readlink(p)
            elif stat.S_ISDIR(mode):directories.append(rel)
            elif stat.S_ISREG(mode):load_pin(p);files[rel]=pins[str(p)]['sha256']
            else:raise ValueError('unexpected SOURCE entry '+rel)
    return dict(files=files,symlinks=symlinks),sorted(directories)

inv,dirs=source_inventory()
check('complete_SOURCE18regular_zero_links_zero_dirs_fresh_all_SHA',
    inv==d['source_inventory'] and dirs==d['source_directories'] and len(inv['files'])==18 and inv['symlinks']=={} and dirs==[])
check('SOURCE_every_regular_file_owned_in_complete_declaration_files_map',
    {str(SOURCE/k):v for k,v in inv['files'].items()}=={k:v for k,v in d['files'].items() if k.startswith(str(SOURCE)+'/')})
check('original_kernel_sender_controls_math_sources_exact',
    inv['files']['SPOT1P64.f90']=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'
    and inv['files']['FLU2DR64.f']=='cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1'
    and inv['files']['rank1_factor_cache_last_cprime_trim_controls.f90']=='eab3a7790e9f499282017cc37581be5acb07f8a4170e8fcaae95b0de47305d52')
check('complete_original86_plan12_build14_sender_original68_retained',
    d['complete_stage_count']==86 and d['original_stage_count']==68 and len(d['build_commands'])==12
    and len(d['sender_control_contract']['cases'])==14
    and d['sender_control_contract']['original_68_controls_must_remain_unmodified'] is True
    and len(d['preserved_predecessors'])==8)
check('declaration_all_original_limits1thread1child0retry_96GiB_free8',
    tuple(d[k] for k in ['total_wall_seconds','stage_wall_seconds','rss_cap_mib','archive_reserve_bytes','artifact_budget_bytes','min_free_bytes','threads','numeric_children_at_once','retries'])
    ==(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0))
olddecl=obj(OLD_OUT/'declaration.json','d0eab52ad5c938cb7acf1e5216475f5d72c5c0a785ec589effad0951a00ed117')
def normalized(commands,source,out):
    return [[s.replace(str(source),'SOURCE').replace(str(out),'OUT') for s in cmd] for cmd in commands]
check('all12_build_and_production_link_commands_equal_predecessor_except_paths',
    normalized(d['build_commands'],SOURCE,OUT)==normalized(olddecl['build_commands'],OLD_SOURCE,OLD_OUT)
    and normalized([d['production_link_command']],SOURCE,OUT)==normalized([olddecl['production_link_command']],OLD_SOURCE,OLD_OUT))
check('original_physics_angular_thresholds_arithmetic_unchanged_no_fitting',all(d[k] is True for k in
    ['white_closure_unchanged','physical_data_unchanged','radial_arithmetic_unchanged','angle_grid_unchanged'])
    and d['original_accuracy_thresholds_changed'] is False and d['coefficient_fitting'] is False)
check('every_actual_prepare_record_grants_zero_component_native_AAA_ABA_credit',all(x[k] is False for x in [root,summary,host,child]
    for k in ['full86_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'])
    and d['actual_full_FLU_entry_executed'] is False and d['transport_launched'] is False
    and d['native_RSS_proof_obtained'] is False and d['AAA_accuracy_qualified'] is False and d['ABA_admitted'] is False
    and admission['scientific_qualification'] is False)
check('new_resource_only_and_helper_only_envelopes_no_full_component_credit',
    d['root_index_resource_source_admission']['full86_component_qualified'] is False
    and d['root_index_resource_source_admission']['resource_module_only'] is True
    and helper['complete_helper_controls_only'] is True)
forecast=d['complete_archive_forecast']
check('archive_forecast_original_single1GiB_allowance_within2GiB',
    forecast['nonraw_binary_diff_watch_log_and_metadata_allowance_bytes']==2**30
    and forecast['original_single_nonraw_1GiB_allowance_retained'] is True
    and forecast['forecast_complete_with_sender_and_stream_helper_bytes']<2*2**30
    and forecast['original_archive_reserve_bytes']==2*2**30)
check('stable_SOURCE_second_complete_inventory_identical',source_inventory()==(inv,dirs))
for p in list(pins.values()):
    raw=load_pin(p['path'],p['sha256'],p['identity'])
value=dict(schema='AXMAT_V15_ACTUAL_COMPLETE_PREPARE_FINITE_READONLY_REVIEW_V1',status='PASS_ACTUAL_COMPLETE_PREPARE_ONLY',
    checks=checks,all_checks_passed=True,Root_actual_terminal=dict(initial_chunk='704853',session_id=36033,terminal_chunk='f24857',integer_exit_code=0,session_closed=True),
    actual_whole_host_seconds=host['whole_elapsed_seconds'],actual_own_child_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
    actual_archive_before_host_result_bytes=host['whole_archive_bytes'],actual_declaration_pin=pins[str(DECL)],
    complete_SOURCE_inventory=inv,complete_SOURCE_directories=dirs,all_fresh_fixed_file_pins=list(pins.values()),
    declared_complete_input_file_bindings=len(d['files']),declared_preserved_history_namespaces=len(d['preserved_predecessors']),
    independent_full_historical_input_content_scan_performed=False,resource_full_scan_performed=False,business_import_or_execution_performed=False,
    OUT_namespace_frozen_or_enumerated=False,OUT_may_grow_for_separate_full86_execution=True,
    new_full86_credit_granted=False,new_native_RSS_credit_granted=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    review_scope='Closed Root/host/child/guard prepare receipts, fixed immutable source and formal qualifications, stable full SOURCE inventory and declaration only. Saved complete resource snapshots are verified as records; no resource.check invocation. Separate full86 may concurrently add OUT build/control files.',
    canonical_files_modified=False)
with (HERE/'REPORT.json').open('x') as stream:json.dump(value,stream,indent=2,ensure_ascii=False,allow_nan=False);stream.write('\n')
print(json.dumps(dict(status=value['status'],checks=len(checks),source_regular_files=len(inv['files']),fresh_fixed_file_pins=len(pins),declaration_sha256=pins[str(DECL)]['sha256'],
    report_sha256=hashlib.sha256((HERE/'REPORT.json').read_bytes()).hexdigest(),business_executed=False,resource_scan=False,OUT_namespace_frozen=False),allow_nan=False))
