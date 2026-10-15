"""Source-only author correction of an added census gate; no candidate execution."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import shutil

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
M=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')

def pin(path):
    s=path.lstat()
    with path.open('rb')as stream:sha=hashlib.file_digest(stream,'sha256').hexdigest()
    return dict(path=str(path),sha256=sha,size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])

def replace_once(text,old,new):
    assert text.count(old)==1
    return text.replace(old,new,1)

def main():
    backup=P/'AUTHOR_DRAFT_ERRORS/before_removing_added_first_live_census_gate';backup.mkdir()
    names=('N8_exact_owner_scope_observer.UNREADY.py','N8_genuine_integrated_controls_driver.UNREADY.py','N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json','AUTHOR_N8_FINAL_SOURCE_CHECKER.py')
    for name in names:shutil.copy2(P/name,backup/name)
    path=P/names[0];text=path.read_text()
    text=replace_once(text,"    A process can leave a group before any census.  Such ownership cannot be\n    recovered from later PS output: a leader closed before its first observed\n    live census makes this observer refuse, even if its group is now empty.\n", "    The original contract uses the current host parent closure. An exact\n    owned leader may be excluded individually after its real wait proves\n    exit/reap, including before its first live census. Its original session\n    group and any captured/current descendants remain in the current union.\n")
    text=replace_once(text,"                if not owner['live_census_seen']:self.fail('leader closed before any live census: escaped descendants ownership remains unknown',proof)\n",'')
    text=replace_once(text,'atomic_or_continuous_ownership_claimed=False,escaped_before_first_census_proven=False)', 'atomic_or_continuous_ownership_claimed=False,first_live_census_is_not_a_new_admission_gate=True)')
    ast.parse(text);path.write_text(text)
    path=P/names[1];text=path.read_text()
    old="""        if case_index==0:
            def close_before_first_census(owner,watchdog):
                code=owner['process'].wait(timeout=min(2,max(.001,deadline-time.monotonic())))
                gate_events.append(dict(event='actual_original_wait_before_first_business_census',actual_returncode=code,actual_owner_state=observer.summary()))
            observer.control_after_original_start=close_before_first_census
            early_command=[str(support.PYTHON),'-B',str(fixture),'early_exit',str(out),repr(deadline)]
            try:runner.execute(case_folder,'actual_early_exit_before_census',early_command,600)
            except BaseException as error:gate_events.append(dict(event='actual_unobserved_lifecycle_refused',actual_error=runtime.monitor_error(error)))
            else:raise ValueError('unobserved early-exit ancestry accepted')
            finally:observer.control_after_original_start=None
            require(any(o['role']=='business' and o['closed_wait']is not None and o['live_census_seen']is False for o in observer.owners.values()),'actual early wait without census retained as unknown')
"""
    new="""        if case_index==0:
            early_owner_pid=None
            def close_before_first_census(owner,watchdog):
                nonlocal early_owner_pid
                early_owner_pid=owner['pid']
                code=owner['process'].wait(timeout=min(2,max(.001,deadline-time.monotonic())))
                require(type(code)is int and code==0 and owner['closed_wait']is not None and owner['closed_wait']['actual_exit_code']==0,'real original owned wait0 and reaped status before census')
                gate_events.append(dict(event='actual_original_wait_before_first_business_census',actual_owner_PID=early_owner_pid,actual_returncode=code,actual_owner_state=observer.summary()))
            observer.control_after_original_start=close_before_first_census
            early_command=[str(support.PYTHON),'-B',str(fixture),'early_exit',str(out),repr(deadline)]
            try:runner.execute(case_folder,'actual_early_exit_before_census',early_command,600)
            finally:observer.control_after_original_start=None
            owner=observer.owners[early_owner_pid]
            require(owner['closed_wait']is not None and owner['closed_wait']['actual_exit_code']==0 and owner['live_census_seen']is False,'real early owned closure has no first-live-census prerequisite')
            scope=observer.last_scope
            require(scope is not None and early_owner_pid not in scope['actual_selected_PIDs'] and any(e['pid']==early_owner_pid for e in scope['individually_proven_closed_exclusions']),'only actual reaped early leader PID excluded in complete current scope')
            require(observer.host_pid in scope['actual_selected_PIDs'] and all(int(p)in scope['actual_selected_PIDs'] for p,row in scope['current_full_PS_rows'].items()if row['pgid']==early_owner_pid and int(p)!=early_owner_pid),'current same-group and host scope fully retained after early wait0')
            gate_events.append(dict(event='actual_early_exit_wait0_current_union_positive',actual_owner_PID=early_owner_pid,actual_complete_scope=scope))
            after=resources.check()
"""
    text=replace_once(text,old,new);ast.parse(text);path.write_text(text)
    path=P/names[2];d=json.loads(path.read_bytes())
    d['exact_owned_wait_policy'].pop('closed_before_first_non_zombie_census_refused')
    d['exact_owned_wait_policy']['actual_owned_wait0_early_exit_is_positive_without_live_census_prerequisite']=True
    d['exact_owned_wait_policy']['closed_leader_exclusion_is_single_PID_only']=True
    d['cases'][0]['source_required_behavior']=d['cases'][0]['source_required_behavior'].replace('A second real early-exit child is reaped by its exact original Popen wait before any business census and is explicitly refused as unknown ancestry.','A second real early-exit child is reaped by its exact original Popen wait0 before any business census and must pass the unchanged genuine runner. A full current PS retains host/watchdog, current original groups and all captured/current descendants; only this proven closed leader PID is excluded.')
    d['accurate_remaining_limits'][1]='Current fullPS parent closure plus captured descendants/groups is a finite observation, not continuous or atomic ownership. Historical unobserved group migration is not inferred and does not introduce a first-live-census acceptance prerequisite beyond the original current-scope contract.'
    d['original_contract_and_added_gate_correction']=dict(original_N7_current_parentchain_Source_pin=pin(M/'complete_observation_BUILD5_AB_runtime.UNREADY.py'),original_genuine_guard_Source_pin=pin(P/'GUARD_SOURCE/qualify_refined_AAA_layered_full.py'),original_current_scope_parentchain_lines=[205,206,207,208,209,210,211,212],added_first_live_census_gate_was_author_design_not_original_guard_or_user_requirement=True,added_gate_removed=True,original_genuine_guard_allows_first_poll_already_closed_then_final_resource_check=True,Root_confirmed_early_exact_wait0_positive=True,original_caps_and_strict_lsof_zero_unchanged=True,current_same_PGID_and_captured_descendants_never_removed_with_leader=True,ECHILD_wrong_object_and_actual_later_closed_PID_reappearance_refused=True,actual_controls_execution=None)
    path.write_text(json.dumps(d,indent=2,allow_nan=False)+'\n')
    path=P/names[3];text=path.read_text()
    text=replace_once(text,"check('unknown_early_exit_and_later_PID_reappearance_refuse', 'leader closed before any live census' in helper and 'closed exact PID reappeared in a later census'in helper)","check('no_new_first_census_gate_and_actual_later_PID_reappearance_refused', 'leader closed before any live census' not in helper and 'closed exact PID reappeared in a later census'in helper and 'first_live_census_is_not_a_new_admission_gate=True'in helper)")
    text=replace_once(text,"'actual_unobserved_lifecycle_refused'in driver)","'actual_early_exit_wait0_current_union_positive'in driver and 'actual_unobserved_lifecycle_refused'not in driver)")
    ast.parse(text);path.write_text(text)
    inv=json.loads((P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json').read_bytes())
    for row in inv['roles']:
        old=(M/row['role_basename']).read_text();new=(P/row['role_basename']).read_text();oldlines=old.splitlines(keepends=True);newlines=new.splitlines(keepends=True);hunks=[]
        for tag,a,b,c,e in difflib.SequenceMatcher(a=oldlines,b=newlines,autojunk=False).get_opcodes():
            if tag!='equal':hunks.append(dict(old_start_line0=a,old_end_line0=b,new_start_line0=c,new_end_line0=e,old_text=''.join(oldlines[a:b]),new_text=''.join(newlines[c:e])))
        restored=newlines[:]
        for h in reversed(hunks):assert ''.join(restored[h['new_start_line0']:h['new_end_line0']])==h['new_text'];restored[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
        assert ''.join(restored)==old and ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
        row['hunks']=hunks;row['new_complete_Source_pin']=pin(P/row['role_basename'])
    (P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json').write_text(json.dumps(inv,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status='AUTHOR_ORIGINAL_CURRENT_SCOPE_CONTRACT_CORRECTION_SOURCE_ONLY',source_only=True,first_live_census_gate_removed=True,early_exact_Popen_wait0_control_is_positive=True,actual_candidate_or_controls_or_API_execution=False),allow_nan=False))

if __name__=='__main__':main()
