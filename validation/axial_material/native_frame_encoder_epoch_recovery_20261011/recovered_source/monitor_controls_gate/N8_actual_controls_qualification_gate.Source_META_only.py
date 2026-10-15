"""Source/small-META gate only. No candidate import, process, or material API.

Future Root qualification and its observed terminal must exist independently
of this Source. Twelve protocol categories, Source binding, actual controls,
closed groups, original caps and an independent saved review are mandatory.
This file cannot manufacture those receipts or promote protocol text to PASS.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import stat

CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CASE_IDS=('01_exact_environment_and_sole_wait_owner','02_actual_live_business_and_descendants','03_actual_closed_after_live_PS_census','04_actual_nonzero_exit_preserves_stage_failure','05_actual_closed_leader_and_reparented_group','06_unknown_owner_ECHILD_and_PID_reuse_refusals','07_actual_late_descendant_exit_strict_lsof_failure','08_actual_strict_stream_nonzero_timeout_oversize','09_original_resource_caps_and_frozen_Source','10_original_cleanup_exceptions_and_group_evidence','11_actual_watchdog_pipe_and_group_closure','12_actual_Root_and_independent_saved_control_closure')

def require(value,message):
    if type(value) is not bool or not value:raise ValueError(message)

def validate_saved_metadata_types(value):
    if type(value)is dict:
        if set(value) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'}):
            require(type(value['path'])is str and Path(value['path']).is_absolute()and '..'not in Path(value['path']).parts and type(value['sha256'])is str and len(value['sha256'])==64 and all(c in '0123456789abcdef'for c in value['sha256']),'typed complete metadata pin path/SHA')
            require(type(value['identity'])is list and len(value['identity'])==7 and all(type(x)is int and x>=0 for x in value['identity']),'typed complete metadata integer7ID')
            if 'size_bytes'in value:require(type(value['size_bytes'])is int and value['size_bytes']>=0 and value['size_bytes']==value['identity'][4],'typed complete metadata size')
        for k,v in value.items():
            if k=='original_caps':require(type(v)is dict and set(v)==set(CAPS)and all(type(x)is int for x in v.values())and v==CAPS,'typed unchanged original nine caps')
            if k=='directories':require(type(v)is dict and all(type(row)is list and len(row)==7 and all(type(x)is int and x>=0 for x in row)for row in v.values()),'typed complete directory7IDs')
            validate_saved_metadata_types(v)
    elif type(value)is list:
        for v in value:validate_saved_metadata_types(v)
    elif type(value)is float:require(value-value==0,'finite saved metadata float')
    return value

def strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'duplicate controls metadata key');result[key]=value
        return result
    return validate_saved_metadata_types(json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v))))

def fullpin(path):
    p=Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(p.is_absolute() and all(not q.is_symlink() for q in (p,*p.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==1,'complete Source/META nonalias singlelink')
    with p.open('rb') as stream:
        require(list((lambda t:(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns))(os.fstat(stream.fileno())))==before,'opened Source/META identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before,'complete Source/META EOF unchanged')
    return dict(path=str(p),sha256=digest,size_bytes=s.st_size,identity=before)

def recheck_pinned(pin):
    require(type(pin) is dict and set(pin)=={'path','sha256','size_bytes','identity'} and type(pin['path']) is str and Path(pin['path']).is_absolute() and type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}',pin['sha256']) is not None,'actual controls exact fullpin required; None refused')
    require(type(pin['size_bytes']) is int and pin['size_bytes']>=0 and type(pin['identity']) is list and len(pin['identity'])==7 and all(type(x) is int and x>=0 for x in pin['identity']) and pin['identity'][3]==1 and pin['identity'][4]==pin['size_bytes'],'controls typed integer7ID/size')
    require(fullpin(pin['path'])==pin,'actual controls Source/META full EOF pin unchanged')
    return pin

def read_pinned(pin):
    recheck_pinned(pin)
    return strict_json(Path(pin['path']).read_bytes())

def actual_closed_zero(pin,expected_schema):
    wrapper=read_pinned(pin);terminal=wrapper['terminal_tool_return']
    require(wrapper['schema']==expected_schema and wrapper['closed'] is True and wrapper['observed_terminal'] is True and wrapper['session_repolled_after_close'] is False,'actual observed CLOSED controls terminal')
    require(type(terminal) is dict and type(terminal['exit_code']) is int and terminal['exit_code']==0 and 'session_id' not in terminal and type(terminal['chunk_id']) is str and bool(terminal['chunk_id']) and wrapper['actual_terminal_chunk']==terminal['chunk_id'],'actual typed zero, exact terminal chunk and no live session')
    return wrapper,strict_json(terminal['output'])

def recheck_saved_regular_file_pins(pins,allow_empty=False):
    require(type(pins)is list and (allow_empty is True or bool(pins)) and all(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}for p in pins),'declared complete regular-file fullpins, no missing or filtered evidence')
    require(len({p['path']for p in pins})==len(pins),'unique declared complete regular-file paths')
    for p in pins:recheck_pinned(p)

def recheck_complete_saved_case(case):
    views=case['actual_complete_postclose_namespace_views']
    require(type(views)is dict and set(views)=={'host','output','control','source','receipts'},'all five declared postclose namespace views retained')
    for view in views.values():recheck_saved_regular_file_pins(view['files'],allow_empty=True)
    recheck_saved_regular_file_pins(case['actual_complete_evidence_pins'])

def validate_actual_N8_monitor_controls(qualification_pin,qualification_terminal_pin,author):
    q=read_pinned(qualification_pin)
    require(q['schema']=='ROOT_ACTUAL_N8_EXACT_OWNER_MONITOR_CONTROLS_QUALIFICATION_V1' and q['status']=='ACTUAL_TWELVE_GENUINE_MONITOR_CONTROLS_QUALIFIED_NO_NATIVE_OR_SCIENCE' and q['source_only'] is False and q['actual_monitor_controls_qualified'] is True,'actual Root monitor controls qualification required')
    require(q['actual_author_Source_contract']==author and q['original_caps']==CAPS and all(type(x) is int for x in q['original_caps'].values()),'complete actual controls Source owner contract and original caps')
    for key in ('actual_native_build_or_AB_executed','native_transport_executed','scientific_qualification_created','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):
        require(q[key] is False,'control qualification cannot create native/science fact: '+key)
    binding=read_pinned(q['actual_controls_Source_binding_pin'])
    require(binding['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1' and binding['source_only'] is True and binding['actual_author_Source_contract']==author and binding['actual_control_execution'] is None,'actual Source-bound monitor controls roles, not guessed execution')
    manifest=read_pinned(q['actual_controls_manifest_pin'])
    require(manifest['schema']=='ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST_V1' and manifest['actual_author_Source_contract']==author and manifest['source_only'] is False and manifest['all_required_controls_passed'] is True and manifest['blockers']==[],'complete actual controls manifest, not a Source protocol')
    require(manifest['actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and manifest['original_caps']==CAPS,'controls Source binding and unchanged limits')
    cases=manifest['cases']
    require(type(cases) is list and len(cases)==len(CASE_IDS) and [c['case_id'] for c in cases]==list(CASE_IDS),'all twelve genuine controls; no filtering unknown cases')
    for case in cases:
        require(case['passed'] is True and case['actual_genuine_runner_used'] is True and case['actual_shared_resource_factory_used'] is True and case['actual_exact_owner_observer_used'] is True and case['synthetic_PS_or_lsof_or_cleanup_error_used_for_qualification'] is False,'actual same monitoring implementation, no mock qualification')
        require(case['actual_complete_raw_evidence_saved'] is True and case['actual_Source_D_and_receipt_E_frozen'] is True and case['actual_original_caps_verified'] is True and case['actual_remaining_owned_groups_absent_after_Root_closure'] is True,'complete raw, frozen Source, original caps and actual residual-group closure')
        actual_closed_zero(case['actual_Root_case_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_TOOL_TERMINAL_RETURN_V1')
        require(type(case['actual_complete_evidence_pins']) is list and bool(case['actual_complete_evidence_pins']),'actual complete Source/small-META raw evidence, no empty case')
        recheck_complete_saved_case(case)
    recheck_saved_regular_file_pins(manifest['actual_complete_controls_regular_file_pins_before_own_append'])
    recheck_saved_regular_file_pins(q['actual_complete_controls_regular_file_pins_before_own_append'])
    _,controls_output=actual_closed_zero(q['actual_Root_controls_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROLS_TOOL_TERMINAL_RETURN_V1')
    require(controls_output['actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and controls_output['all_required_controls_passed'] is True,'actual Root complete controls zero output coupling')
    peer=read_pinned(q['actual_independent_saved_controls_review_pin'])
    require(peer['schema']=='INDEPENDENT_ACTUAL_N8_SAVED_GENUINE_MONITOR_CONTROLS_REVIEW_V1' and peer['status']=='PASS_ACTUAL_SAVED_TWELVE_GENUINE_MONITOR_CONTROLS_NO_NATIVE_OR_SCIENCE' and peer['actual_author_Source_contract']==author and peer['qualified_actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and peer['qualified_actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and peer['qualified_actual_Root_controls_tool_terminal_return_pin']==q['actual_Root_controls_tool_terminal_return_pin'] and peer['all_checks_passed'] is True and peer['blockers']==[],'independent review of these actual saved controls required')
    checks=peer['checks']
    require(type(checks) is list and type(peer['check_count']) is int and peer['check_count']==len(checks)>0 and len({c['check'] for c in checks})==len(checks) and all(type(c) is dict and set(c)=={'check','passed'} and type(c['check']) is str and bool(c['check']) and c['passed'] is True for c in checks),'unique typed independent actual controls checks')
    _,q_output=actual_closed_zero(qualification_terminal_pin,'ROOT_ACTUAL_N8_MONITOR_CONTROLS_QUALIFICATION_TOOL_TERMINAL_RETURN_V1')
    require(q_output['actual_monitor_controls_qualification_pin']==qualification_pin and q_output['actual_monitor_controls_qualified'] is True and q_output['native_or_scientific_qualification_created'] is False,'actual Root qualification output coupled to this immutable Q')
    return dict(schema='ACTUAL_N8_REQUIRED_MONITOR_CONTROLS_SCOPE_COUPLING_V1',actual_monitor_controls_qualification_pin=qualification_pin,actual_Root_qualification_tool_terminal_return_pin=qualification_terminal_pin,actual_complete_controls_manifest_pin=q['actual_controls_manifest_pin'],actual_independent_saved_controls_review_pin=q['actual_independent_saved_controls_review_pin'],actual_stdlib_subprocess_Source_pin=q['actual_stdlib_subprocess_Source_pin'],all_twelve_actual_controls_required=True,native_or_scientific_qualification_created=False)
