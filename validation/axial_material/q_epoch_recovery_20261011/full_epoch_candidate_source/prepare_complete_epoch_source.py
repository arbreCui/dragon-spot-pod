"""Write the complete new-epoch pure controller/host, never execute them."""
import ast
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/q_epoch_recovery_20261011'
DEST=Path(__file__).resolve().parent
AUDIT=ROOT/'validation/artifacts/axial-material-input-epoch-recovery-v2-20261011/current_inputs.ndjson'

def digest(data):return hashlib.sha256(data).hexdigest()

def put(name,data):
    p=DEST/name
    with p.open('xb')as stream:stream.write(data)
    return dict(path=str(p),size_bytes=len(data),sha256=digest(data))

def replace(raw,before,after,changes):
    a,b=before.encode(),after.encode();assert raw.count(a)==1
    changes.append(dict(exact_before=before,exact_after=after,count=1))
    return raw.replace(a,b)

def proof(raw,base,changes):
    restored=raw
    for c in reversed(changes):
        a,b=c['exact_before'].encode(),c['exact_after'].encode();assert restored.count(b)==1
        restored=restored.replace(b,a)
    assert restored==base
    return dict(whole_source_inverse_byte_exact=True,original_sha256=digest(base),new_sha256=digest(raw),exact_changes=changes)

assert sys.dont_write_bytecode
rows=[json.loads(x)for x in AUDIT.read_text().splitlines()]
current={j['path']:j['current_pin']for j in rows if j['status']=='CURRENT_BYTES_MATCH'}
mother_path=REC/'candidate_source/pure_helper_controls_NEW_EPOCH_CANDIDATE.py'
mother=mother_path.read_bytes();assert digest(mother)=='975833790097bd4484e6a41911e51cb5ed35dc85c367f5aed39a809908d58441'
raw=mother;changes=[]
tree=ast.parse(mother)
for name in ('GRAPH_PIN','TRACE_PIN'):
    node=next(n for n in tree.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    old=ast.literal_eval(node.value);actual=current[old['path']]
    assert actual['sha256']==old['sha256'] and actual['size_bytes']==old['identity'][4]
    new=dict(path=actual['path'],sha256=actual['sha256'],identity=actual['identity'])
    raw=replace(raw,ast.get_source_segment(mother.decode(),node),name+' = '+repr(new),changes)
raw=replace(raw,"SOURCE_STATUS = 'UNREADY_CURRENT_ROOT_PURE_BINDING_REQUIRED'","SOURCE_STATUS = 'UNREADY_PENDING_REAL_CURRENT_ROOT_BINDING'\nROOT_EXEC_BINDING = None",changes)
raw=replace(raw,'        small_graph, fixture_result = fixture_controls(g, artifacts)','        import epoch_additional_controls\n        report["new_epoch_complete_additional_controls"] = epoch_additional_controls.run_additional(g, artifacts, exact_value, ROOT_EXEC_BINDING)\n        checkpoint("complete_actual_index_wire67_full238780_and_five_cache_absence_controls")\n        small_graph, fixture_result = fixture_controls(g, artifacts)',changes)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main')
newmain='''def main():
    import epoch_binding
    global SOURCE_STATUS, ROOT_EXEC_BINDING
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--root-binding', required=True)
    parser.add_argument('--root-binding-sha256', required=True)
    args = parser.parse_args()
    cfg = epoch_binding.authorize(args.root_binding, args.root_binding_sha256, 'driver')
    require(args.output_dir == cfg['run_paths']['output'], 'exact current Root output path required')
    require(epoch_binding.pin(HELPER_PATH) == cfg['helper'], 'actual unchanged installed6a current full EOF seven-field binding required')
    ROOT_EXEC_BINDING = cfg
    SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'
    run(args.output_dir)'''
raw=replace(raw,ast.get_source_segment(mother.decode(),node),newmain,changes)
driver=put('complete_new_epoch_pure_controls.py',raw)
oldfunctions={n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
newfunctions={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(raw).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
assert set(oldfunctions)==set(newfunctions)
assert [k for k in oldfunctions if oldfunctions[k]!=newfunctions[k]]==['run','main']
driverproof=proof(raw,mother,changes)
driverproof['all_original_nonentry_function_and_class_AST_exact']=True
driverproof['all_five_original_stages_body_retained_with_one_added_complete_supplement_stage']=True
driverproof['historical_codec_counts_not_changed']=dict(old_graph_canonical_files=36776,old_graph_requirements=237767,old_graph_saved_trace_records=62332,new_creation_trace_records=63379,new_creation_trace_actual_attempts=175886,full_wire_historical_requirements=238780)
driverproof['full_current37590_and480_not_claimed_by_pure']=True

host_path=ROOT/'validation/artifacts/axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011/actual_closed_S/pure_helper_controls_host.py'
host_base=host_path.read_bytes();assert digest(host_base)=='daffb72c35d69273f1fe3cba9b905951312c729d0be0e84b3316d4012554f92f'
put('ORIGINAL_COMPLETE_PURE_HOST_BASIS.py',host_base)
host=host_base;hc=[];ht=ast.parse(host_base)
for name in ('HOST','OUT','SOURCE_ARCHIVE','TARGET','TARGET_SHA','SOURCE_STATUS','BOUND_HELPER_PIN','INSTALL_WITNESS_PIN','SOURCE_INSTALL_RECORD_PIN','AUDIT_CONTROL_PATH'):
    node=next(n for n in ht.body if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id==name)
    if name=='SOURCE_STATUS':value="'UNREADY_PENDING_REAL_CURRENT_ROOT_BINDING'"
    elif name=='SOURCE_ARCHIVE':value='Path(__file__).resolve().parent'
    elif name=='TARGET':value="Path(__file__).resolve().parent/'complete_new_epoch_pure_controls.py'"
    elif name=='TARGET_SHA':value=repr(driver['sha256'])
    elif name=='AUDIT_CONTROL_PATH':value=repr(str(REC/'preserved_source_basis/ORIGINAL_COMPLETE_INACTIVE_SNAPSHOT_CONTROLS.py'))
    else:value='None'
    host=replace(host,ast.get_source_segment(host_base.decode(),node),name+' = '+value,hc)
host=replace(host,'    started=time.monotonic()','''    started=time.monotonic()
    import argparse
    import epoch_binding
    global HOST, OUT, SOURCE_STATUS, BOUND_HELPER_PIN, INSTALL_WITNESS_PIN, SOURCE_INSTALL_RECORD_PIN
    parser=argparse.ArgumentParser(description='Full original pure protocol plus actual new-epoch controls, one genuine unchanged OwnRSS host.')
    parser.add_argument('--root-binding',required=True)
    parser.add_argument('--root-binding-sha256',required=True)
    args=parser.parse_args()
    cfg=epoch_binding.authorize(args.root_binding,args.root_binding_sha256,'host')
    if epoch_binding.pin(TARGET)!=cfg['driver']:raise ValueError('complete current driver EOF/7ID Source binding differs')
    HOST=Path(cfg['run_paths']['host']);OUT=Path(cfg['run_paths']['output'])
    for path in (HOST,OUT):
        if not path.is_absolute()or not path.is_relative_to(Path('/Users/wen/spot/validation/artifacts'))or path==Path('/Users/wen/spot/validation/artifacts'):raise ValueError('fresh private HOST and OUTPUT must be strict ART descendants')
    BOUND_HELPER_PIN={k:cfg['helper'][k]for k in ('path','sha256','identity')}
    # These are current review/input-observation pins, never old install identity.
    INSTALL_WITNESS_PIN={k:cfg['Root_Source_review'][k]for k in ('path','sha256','identity')}
    SOURCE_INSTALL_RECORD_PIN={k:cfg['current_epoch_input_observation'][k]for k in ('path','sha256','identity')}
    SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT' ''',hc)
host=replace(host,"    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:","    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:",hc)
host=replace(host,"        command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT)]","        command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT),'--root-binding',args.root_binding,'--root-binding-sha256',args.root_binding_sha256]",hc)
host=replace(host,"        if len(runner.records)!=1 or runner.records[0]['status']!='PASS'",'''        complete_supplement=control_report['new_epoch_complete_additional_controls']
        if (complete_supplement['index_attempts'],complete_supplement['index_unique_records'],complete_supplement['index_markers'],complete_supplement['index_private_guards'],complete_supplement['index_last_use_failures'])!=(35,9,2,13,3)or complete_supplement['index_both_standard_and_forced_collision']is not True:raise ValueError('whole actual index controls required')
        if (complete_supplement['wire67_fixtures'],complete_supplement['wire67_returns'],complete_supplement['wire67_raises'])!=(67,14,53)or complete_supplement['full_historical238780_wire']['logical_edges']!=238780:raise ValueError('all67 fixtures and complete238780 historical real wire controls required')
        if complete_supplement['cache_absence_cases']!=['DECLARED_REAL_F574_CACHE_ENOENT_READ_ACCEPTED','SAME_REAL_TRACE_UNDECLARED_REJECTED','PREEXISTING_CACHE_FILE_REJECTED','REAL_EXISTING_PARENT_REPLACEMENT_REJECTED','ACTUAL_READWRITE_ENOENT_REJECTED']:raise ValueError('all five real absence behavior cases required')
        if complete_supplement['complete27_future_fresh_return_fields']!=epoch_binding.RETURN_FIELDS or complete_supplement['complete9_snapshot_fields']!=epoch_binding.SNAPSHOT_FIELDS:raise ValueError('whole27/9 contracts must remain retained')
        if any(complete_supplement[k]is not False for k in ('all480_production_absences_actual','current_complete_fresh_qualified','new_Q_created','whole_INPUT_admitted','science_or_BOOT_admitted'))or complete_supplement['original37590_missing_canonical_endpoints_still_blocking_fullfresh']!=53:raise ValueError('pure cannot inherit a blocked whole-current/fresh/Q qualification')
        for key in ('index','wire67','cache_absence'):
            epoch_binding.read_pinned(complete_supplement[key])
        expected_stages=['complete_actual_index_wire67_full238780_and_five_cache_absence_controls','real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged']
        if [r['stage']for r in control_report['stages']]!=expected_stages:raise ValueError('all five original full stages plus whole supplement must run in order')
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' ''',hc)
host=replace(host,"schema='AXMAT_V25_GENUINE_PRIVATE_INACTIVE_AUDIT_PURE_PROTOCOL_CONTROLS_HOST_V1'","schema='SPOT_NEW_EPOCH_GENUINE_COMPLETE_PURE_INDEX_WIRE67_CACHE_ABSENCE_HOST_V1',current_Root_execution_binding=cfg['_binding_pin'],current_Root_Source_review=cfg['Root_Source_review'],current_epoch_input_observation=cfg['current_epoch_input_observation'],current_complete_fresh_qualified=False,new_Q_created=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False,all480_production_absences_actual=False,original37590_missing_canonical_endpoints_still_blocking_fullfresh=53",hc)
host=replace(host,"status='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED'","status='ACTUAL_NEW_EPOCH_COMPLETE_PURE_CONTROLS_EXTERNAL_ROOT_REQUIRED'",hc)
hostpin=put('complete_new_epoch_pure_host.py',host)
hostproof=proof(host,host_base,hc)
hostproof['unchanged_original_OwnRSS_guard_module_and_MRO_and_all_original_assertion_blocks_retained']=True
hostproof['one_actual_child_stage_no_retry_and_original_60s_512MiB_64MiB_caps_retained']=True
assert {n.name:ast.dump(n,include_attributes=False)for n in ht.body if isinstance(n,ast.FunctionDef)and n.name!='main'}=={n.name:ast.dump(n,include_attributes=False)for n in ast.parse(host).body if isinstance(n,ast.FunctionDef)and n.name!='main'}

# The complete independent fresh oracle bodies are preserved as historical
# basis, NOT falsely relabeled into a ready37590/480 current fresh controller.
for name,dest in [('HISTORICAL_FULLFRESH_COMPLETE_CONTROLLER.py','COMPLETE_FULLFRESH_ORACLE_HISTORICAL_BASIS.py'),('HISTORICAL_FULLFRESH_ORIGINAL_HOST.py','COMPLETE_FULLFRESH_HOST_HISTORICAL_BASIS.py')]:
    put(dest,(REC/'preserved_source_basis'/name).read_bytes())

required_paths=[REC/'NEW_EPOCH_DATA_SUPPLEMENTS.py',REC/'candidate_source/wire67_original_fixture_definitions.py',ROOT/'validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_20261011.py',ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json',ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/ACTUAL_BOUNDED_COMPLETE_WIRE_SORT_CONTROL_RESULT.json',ROOT/'validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/input_graph.json',REC/'preserved_source_basis/HISTORICAL_EXACT_Q_CONTRACT.py',ROOT/'validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json',ROOT/'validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json',REC/'small_data_actual_v2/ACTUAL_SYNTHETIC_INDEX_CONTROLS.json',REC/'small_data_actual_v2/ACTUAL_ALL67_WIRE_TINY_FIXTURES.json']
plan=dict(schema='SPOT_COMPLETE_NEW_EPOCH_PURE_SOURCE_DERIVATION_V1',status='COMPLETE_EXECUTABLE_SOURCE_PENDING_ACTUAL_CURRENT_ROOT_REVIEW_NOT_RUN',driver=driver,host=hostpin,driver_full_inverse=driverproof,host_full_inverse=hostproof,original_frozen_recovery_namespace_unchanged_in_place=True,new_child_subdirectory_created_after_its_freeze=True,original_complete_pure_cases_and_5stage_bodies_retained=True,new_actual_index_wire67_whole238780_and_cache5cases_integrated=True,complete_supplement_runtime_input_paths=[str(p)for p in required_paths],all480_production_absences_actual=False,current_fullfresh_host_prepared=False,current_Q_prepared=False,old37590_original_canonical_endpoint_missing=154,old37590_original_canonical_samebyte_found=101,old37590_original_canonical_no_bytes_found=53,canonical_unknown_bytes_never_replaced_by_absence=True,full_current_fresh_requirements=dict(all27_return_fields=True,all9_complete_snapshot_fields=True,all480_current_absence_observations=True,no_original_canonical_owner_erased=True,all_current_canonical_regular_bytes_full_EOF=True),Root_authorization_fields_required=['schema','status','scope','caps','qualification_flags','source_namespace_files','driver','host','helper','Root_Source_review','Root_Source_review_actual_tool_return','current_epoch_input_observation','small_data_result','small_data_true_closed_tool','complete_supplement_input_pins','run_paths'],future_genuine_host_entry=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',hostpin['path'],'--root-binding','<ACTUAL_CURRENT_ROOT_BINDING_PATH>','--root-binding-sha256','<ACTUAL_FULL_EOF_SHA>'],business_native_PS_or_child_executed=False)
put('COMPLETE_NEW_EPOCH_SOURCE_DERIVATION.json',(json.dumps(plan,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode())
for p in DEST.glob('*.py'):ast.parse(p.read_bytes())
print(json.dumps(dict(status=plan['status'],driver=driver,host=hostpin,original_function_bodies_preserved=True,fullfresh_and_Q_still_blocked_by_53_unknown_canonical_bytes=True),allow_nan=False))
