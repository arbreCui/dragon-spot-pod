"""Root future request META producer; no native/controller/candidate import.
Read complete actual Source/small receipts/tool/library bytes solely for pins.
Only Root executes this after independent observer Source admission. UNREADY
inputs are not guessed; all actual runtime/observations/science remain unknown.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

P=Path(__file__).resolve().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
ROLES={'qualified_source_manifest': 'MANIFEST.json', 'host_template': 'complete_observation_genuine_host.UNREADY.py', 'runtime_template': 'complete_observation_BUILD5_AB_runtime.UNREADY.py', 'binder': 'bind_complete_observation_SOURCE_only.UNREADY.py', 'postclose_writer': 'Root_observation_postclose_META_writer.UNREADY.py', 'native_Source_archive': 'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz', 'native_Source_index': 'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json', 'observer_module': 'OBSERVATION_SOURCE/AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90', 'context_extractor': 'OBSERVATION_SOURCE/extract_actual_complete_context_with_SPH_decisions.UNREADY.py', 'original_complete_native_walker': 'PARENT_SOURCE/Root_bound_complete_native_checker.py', 'original_material_seed_contract': 'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json', 'material_blueprint_Source': 'GUARD_SOURCE/material_inputs.py', 'request_preparer': 'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py', 'legacy_context_old_XSM_extractor': 'COMPLETE_LEGACY_CONTEXT_HANDOFF_SOURCE/complete_observed_old_post_final_XSM_extractor.UNREADY.py', 'owner_scope_helper': 'N8_exact_owner_scope_observer.UNREADY.py', 'monitor_controls_gate': 'N8_actual_controls_qualification_gate.Source_META_only.py', 'monitor_controls_protocol': 'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json', 'monitor_control_driver': 'N8_genuine_integrated_controls_driver.UNREADY.py', 'monitor_control_child_Source': 'N8_private_control_child.UNREADY.py', 'monitor_control_Source_binder': 'N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py', 'monitor_controls_postclose_qualifier': 'N8_Root_controls_postclose_META.UNREADY.py'}

CANONICAL_OS_TOOL_PATHS = {'fortran': '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', 'c': '/usr/bin/gcc', 'cpp': '/usr/bin/cpp', 'ar': '/usr/bin/ar', 'lsof': '/usr/sbin/lsof', 'ps': '/bin/ps'}

def source_tool_nlink_allowed(path,nlink,tool_role=None):
    # Default stays the original single-link contract. Only an explicit one of
    # these six original OS tool roles may preserve a positive real hardlink
    # count. Paths, bytes, all seven identity integers and caller order stay real.
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1

def require(v,m):
    if type(v)is not bool or not v:raise ValueError(m)

def pin(path,deadline,tool_role=None):
    p=Path(path);s=p.lstat();identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];require(p.is_absolute()and all(not q.is_symlink()for q in(p,*p.parents))and stat.S_ISREG(s.st_mode)and source_tool_nlink_allowed(p,s.st_nlink,tool_role),'actual Root full regular pin; only declared canonical OS tools may have real positive hardlinks')
    d=hashlib.sha256()
    with p.open('rb')as f:
        while True:
            require(time.monotonic()<deadline,'actual Root request preparation600 cap');raw=f.read(2**20)
            if not raw:break
            d.update(raw)
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==identity,'full requestSource/META/library/tool EOF unchanged')
    return dict(path=str(p),sha256=d.hexdigest(),size_bytes=s.st_size,identity=identity)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate actual Root metadata key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

SHARED_INPUT_LIBRARY_LAYOUT = {'schema': 'COMPLETE_AB_SINGLE_COPY_ORIGINAL_SHARED_LIBRARIES_AND_EXACT_PROCEDURE_FILE_LITERALS_V1', 'shared_directory': 'shared_input_libraries', 'state_order': ['A', 'B'], 'seed_destination_order': ['material.x2m', 'AxMatTone.c2m', 'geometry.dat', 'rnr_cc.c2m', 'rnr_interpol.c2m', 'DLIB_ACTUAL', 'DLIB8R1_370'], 'original_procedure_copy_name': 'AxMatTone.c2m.original', 'literal_replacements': [{'original': "FIL: 'DLIB_ACTUAL'", 'derived': "FIL: '../shared_input_libraries/DLIB_ACTUAL'", 'count': 2}, {'original': "FIL: 'DLIB8R1_370'", 'derived': "FIL: '../shared_input_libraries/DLIB8R1_370'", 'count': 1}]}
REQUIRED_N8_FRESH_NAMESPACES = {'host': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v8-host-20261010', 'output': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v8-runtime-20261010', 'control': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v8-control-20261010', 'source': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v8_sources', 'receipts': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v8_receipts'}

N8_CASE_IDS=('01_exact_environment_and_sole_wait_owner','02_actual_live_business_and_descendants','03_actual_closed_after_live_PS_census','04_actual_nonzero_exit_preserves_stage_failure','05_actual_closed_leader_and_reparented_group','06_unknown_owner_ECHILD_and_PID_reuse_refusals','07_actual_late_descendant_exit_strict_lsof_failure','08_actual_strict_stream_nonzero_timeout_oversize','09_original_resource_caps_and_frozen_Source','10_original_cleanup_exceptions_and_group_evidence','11_actual_watchdog_pipe_and_group_closure','12_actual_Root_and_independent_saved_control_closure')

def n8_require(value,message):
    if type(value) is not bool or not value:raise ValueError(message)

def n8_strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            n8_require(key not in result,'duplicate controls metadata key');result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def n8_fullpin(path):
    p=Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    n8_require(p.is_absolute() and all(not q.is_symlink() for q in (p,*p.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==1,'complete Source/META nonalias singlelink')
    with p.open('rb') as stream:
        n8_require(list((lambda t:(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns))(os.fstat(stream.fileno())))==before,'opened Source/META identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    t=p.lstat();n8_require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before,'complete Source/META EOF unchanged')
    return dict(path=str(p),sha256=digest,size_bytes=s.st_size,identity=before)

def n8_recheck_pinned(pin):
    n8_require(type(pin) is dict and set(pin)=={'path','sha256','size_bytes','identity'} and type(pin['path']) is str and Path(pin['path']).is_absolute() and type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}',pin['sha256']) is not None,'actual controls exact n8_fullpin required; None refused')
    n8_require(type(pin['size_bytes']) is int and pin['size_bytes']>=0 and type(pin['identity']) is list and len(pin['identity'])==7 and all(type(x) is int and x>=0 for x in pin['identity']) and pin['identity'][3]==1 and pin['identity'][4]==pin['size_bytes'],'controls typed integer7ID/size')
    n8_require(n8_fullpin(pin['path'])==pin,'actual controls Source/META full EOF pin unchanged')
    return pin

def n8_read_pinned(pin):
    n8_recheck_pinned(pin)
    return n8_strict_json(Path(pin['path']).read_bytes())

def n8_actual_closed_zero(pin,expected_schema):
    wrapper=n8_read_pinned(pin);terminal=wrapper['terminal_tool_return']
    n8_require(wrapper['schema']==expected_schema and wrapper['closed'] is True and wrapper['observed_terminal'] is True and wrapper['session_repolled_after_close'] is False,'actual observed CLOSED controls terminal')
    n8_require(type(terminal) is dict and type(terminal['exit_code']) is int and terminal['exit_code']==0 and 'session_id' not in terminal and type(terminal['chunk_id']) is str and bool(terminal['chunk_id']) and wrapper['actual_terminal_chunk']==terminal['chunk_id'],'actual typed zero, exact terminal chunk and no live session')
    return wrapper,n8_strict_json(terminal['output'])

def validate_actual_N8_monitor_controls(qualification_pin,qualification_terminal_pin,author):
    q=n8_read_pinned(qualification_pin)
    n8_require(q['schema']=='ROOT_ACTUAL_N8_EXACT_OWNER_MONITOR_CONTROLS_QUALIFICATION_V1' and q['status']=='ACTUAL_TWELVE_GENUINE_MONITOR_CONTROLS_QUALIFIED_NO_NATIVE_OR_SCIENCE' and q['source_only'] is False and q['actual_monitor_controls_qualified'] is True,'actual Root monitor controls qualification required')
    n8_require(q['actual_author_Source_contract']==author and q['original_caps']==CAPS and all(type(x) is int for x in q['original_caps'].values()),'complete actual controls Source owner contract and original caps')
    for key in ('actual_native_build_or_AB_executed','native_transport_executed','scientific_qualification_created','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):
        n8_require(q[key] is False,'control qualification cannot create native/science fact: '+key)
    binding=n8_read_pinned(q['actual_controls_Source_binding_pin'])
    n8_require(binding['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1' and binding['source_only'] is True and binding['actual_author_Source_contract']==author and binding['actual_control_execution'] is None,'actual Source-bound monitor controls roles, not guessed execution')
    manifest=n8_read_pinned(q['actual_controls_manifest_pin'])
    n8_require(manifest['schema']=='ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST_V1' and manifest['actual_author_Source_contract']==author and manifest['source_only'] is False and manifest['all_required_controls_passed'] is True and manifest['blockers']==[],'complete actual controls manifest, not a Source protocol')
    n8_require(manifest['actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and manifest['original_caps']==CAPS,'controls Source binding and unchanged limits')
    cases=manifest['cases']
    n8_require(type(cases) is list and len(cases)==len(N8_CASE_IDS) and [c['case_id'] for c in cases]==list(N8_CASE_IDS),'all twelve genuine controls; no filtering unknown cases')
    for case in cases:
        n8_require(case['passed'] is True and case['actual_genuine_runner_used'] is True and case['actual_shared_resource_factory_used'] is True and case['actual_exact_owner_observer_used'] is True and case['synthetic_PS_or_lsof_or_cleanup_error_used_for_qualification'] is False,'actual same monitoring implementation, no mock qualification')
        n8_require(case['actual_complete_raw_evidence_saved'] is True and case['actual_Source_D_and_receipt_E_frozen'] is True and case['actual_original_caps_verified'] is True and case['actual_remaining_owned_groups_absent_after_Root_closure'] is True,'complete raw, frozen Source, original caps and actual residual-group closure')
        n8_actual_closed_zero(case['actual_Root_case_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_TOOL_TERMINAL_RETURN_V1')
        n8_require(type(case['actual_complete_evidence_pins']) is list and bool(case['actual_complete_evidence_pins']),'actual complete Source/small-META raw evidence, no empty case')
        for p in case['actual_complete_evidence_pins']:n8_recheck_pinned(p)
    _,controls_output=n8_actual_closed_zero(q['actual_Root_controls_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROLS_TOOL_TERMINAL_RETURN_V1')
    n8_require(controls_output['actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and controls_output['all_required_controls_passed'] is True,'actual Root complete controls zero output coupling')
    peer=n8_read_pinned(q['actual_independent_saved_controls_review_pin'])
    n8_require(peer['schema']=='INDEPENDENT_ACTUAL_N8_SAVED_GENUINE_MONITOR_CONTROLS_REVIEW_V1' and peer['status']=='PASS_ACTUAL_SAVED_TWELVE_GENUINE_MONITOR_CONTROLS_NO_NATIVE_OR_SCIENCE' and peer['actual_author_Source_contract']==author and peer['qualified_actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and peer['qualified_actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and peer['qualified_actual_Root_controls_tool_terminal_return_pin']==q['actual_Root_controls_tool_terminal_return_pin'] and peer['all_checks_passed'] is True and peer['blockers']==[],'independent review of these actual saved controls required')
    checks=peer['checks']
    n8_require(type(checks) is list and type(peer['check_count']) is int and peer['check_count']==len(checks)>0 and len({c['check'] for c in checks})==len(checks) and all(type(c) is dict and set(c)=={'check','passed'} and type(c['check']) is str and bool(c['check']) and c['passed'] is True for c in checks),'unique typed independent actual controls checks')
    _,q_output=n8_actual_closed_zero(qualification_terminal_pin,'ROOT_ACTUAL_N8_MONITOR_CONTROLS_QUALIFICATION_TOOL_TERMINAL_RETURN_V1')
    n8_require(q_output['actual_monitor_controls_qualification_pin']==qualification_pin and q_output['actual_monitor_controls_qualified'] is True and q_output['native_or_scientific_qualification_created'] is False,'actual Root qualification output coupled to this immutable Q')
    return dict(schema='ACTUAL_N8_REQUIRED_MONITOR_CONTROLS_SCOPE_COUPLING_V1',actual_monitor_controls_qualification_pin=qualification_pin,actual_Root_qualification_tool_terminal_return_pin=qualification_terminal_pin,actual_complete_controls_manifest_pin=q['actual_controls_manifest_pin'],actual_independent_saved_controls_review_pin=q['actual_independent_saved_controls_review_pin'],actual_stdlib_subprocess_Source_pin=q['actual_stdlib_subprocess_Source_pin'],all_twelve_actual_controls_required=True,native_or_scientific_qualification_created=False)

def main():
    ap=argparse.ArgumentParser()
    for name in('independent-review','Source-admission','actual-admission-terminal','fortran','c','cpp','ar','lsof','ps','host','output','control','source','receipts','request-output','monitor-controls-qualification','monitor-controls-qualification-terminal'):ap.add_argument('--'+name,required=True)
    a=ap.parse_args();require({k:getattr(a,k)for k in REQUIRED_N8_FRESH_NAMESPACES}==REQUIRED_N8_FRESH_NAMESPACES,'new fixed v8 Rootrequest namespaces only');deadline=time.monotonic()+600;require(not sys_optimized(),'unprofiled nonoptimized Root metadata pin preparation')
    seed=strict_json((P/'ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json').read_bytes());review=pin(a.independent_review,deadline);admission=pin(a.Source_admission,deadline);terminal=pin(a.actual_admission_terminal,deadline);author={k:pin(P/v,deadline)for k,v in ROLES.items()};ad=strict_json(Path(a.Source_admission).read_bytes());peer=strict_json(Path(a.independent_review).read_bytes())
    require(ad['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and ad['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and ad['source_only']is True and ad['actual_author_Source_contract']==author and ad['independent_Source_review_pin']==review,'actual independently admitted complete observer Source required before input hashing')
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['actual_author_Source_contract']==author and peer['all_checks_passed']is True and peer['blockers']==[],'real whole Source peer pass exact source')
    for k,v in FUTURE.items():require(ad[k]is v,'actual future still unknown/false')
    monitor_q=pin(a.monitor_controls_qualification,deadline);monitor_q_terminal=pin(a.monitor_controls_qualification_terminal,deadline)
    monitor_scope=validate_actual_N8_monitor_controls(monitor_q,monitor_q_terminal,author)
    require(all(getattr(a,k)==v for k,v in CANONICAL_OS_TOOL_PATHS.items()),'all six original canonical OS tool CLI paths unchanged')
    tools={k:pin(getattr(a,k),deadline,tool_role=k)for k in('fortran','c','cpp','ar','lsof','ps')};libraries={}
    for name,value in seed['libraries'].items():
        actual=pin(value['path'],deadline);require(actual['sha256']==value['generation_sha256'],'actual immutable original library generation hash');libraries[name]=actual
    states={}
    for state in('A','B'):
        rows=[dict(destination=name,input_pin=seed['states'][state][name])for name in('material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m')]+[dict(destination=name,input_pin=libraries[name])for name in('DLIB_ACTUAL','DLIB8R1_370')]
        states[state]=dict(original_material_deck_pin=seed['states'][state]['material.x2m'],native_stage_inputs=rows)
    original=seed['original129_input_pins'];extra=[];seen={r['path']for r in original}
    for p in[review,admission,terminal,monitor_q,monitor_q_terminal,*tools.values(),*libraries.values()]:
        require(p['path']not in seen,'all additional actual Source/tool/library pins disjoint from original129');seen.add(p['path']);extra.append(p)
    request=dict(schema='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_REQUEST_V1',source_only=True,Root_only_actual_execution=True,scientific_qualification_created=False,original_caps=CAPS,state_order=['A','B'],build_stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],SPOT_AXMAT_OBSERVATION='ADMITTED_SOURCE_ONLY',actual_author_Source_contract=author,actual_monitor_controls_qualification_pin=monitor_q,actual_monitor_controls_qualification_terminal_pin=monitor_q_terminal,actual_required_monitor_controls_scope=monitor_scope,independent_observation_Source_review_pin=review,independent_observation_Source_admission_pin=admission,actual_Root_observation_Source_admission_tool_return_pin=terminal,original129_input_pins=original,additional_actual_evidence_input_pins=extra,tool_pins=tools,states=states,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,namespaces={k:getattr(a,k)for k in('host','output','control','source','receipts')},actual_observation_manifest=None,actual_Root_observed_runtime_terminal=None,actual_runtime_observer_executable=None,**FUTURE)
    output=Path(a.request_output);require(output.is_absolute()and output.parent.is_dir()and not os.path.lexists(output),'fresh Rootrequest file')
    with output.open('x')as f:json.dump(request,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status='ACTUAL_ROOT_OBSERVATION_REQUEST_META_ONLY_NO_BUILD_OR_MATERIAL_RUN',source_only=True,actual_request_pin=pin(output,deadline),native_build_or_API_or_material_execution=False,all_runtime_and_observations_unknown=True,**FUTURE),allow_nan=False),flush=True)

def sys_optimized():
    import sys
    return bool(sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE')or sys.getprofile()is not None)
if __name__=='__main__':main()
