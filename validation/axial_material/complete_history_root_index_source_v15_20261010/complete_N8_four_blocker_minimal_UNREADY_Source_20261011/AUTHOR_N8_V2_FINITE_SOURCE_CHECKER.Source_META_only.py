"""Finite Source/AST/full EOF checker. No candidate import or execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
OLD=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
MOTHER=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
FAILED=Path('/private/tmp/axmat_N8_COMPLETE_INDEPENDENT_Source_review_36g28ueh')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    p=Path(path);before=ident(p.lstat());assert p.is_absolute()and stat.S_ISREG(before[2])and before[3]==1 and all(not q.is_symlink()for q in(p,*p.parents))
    with p.open('rb')as f:
        assert ident(os.fstat(f.fileno()))==before;sha=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==before
    assert ident(p.lstat())==before
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def funcs(s):return {n.name:n for n in ast.parse(s).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def astvalue(n):return ast.dump(n,include_attributes=False)
def restore(text,hs):
    lines=text.splitlines(keepends=True)
    for h in reversed(hs):
        assert ''.join(lines[h['new_start_line0']:h['new_end_line0']])==h['new_text'];lines[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
    return ''.join(lines)
def main():
    checks=[];evidence={}
    def check(name,v,e=None):
        assert type(v)is bool and name not in {c['check']for c in checks};checks.append(dict(check=name,passed=v))
        if e is not None:evidence[name]=e
    oldmf=json.loads((OLD/'MANIFEST.json').read_bytes());revision=json.loads((P/'CURRENT_N8_V2_SOURCE_REVISION_CONTRACT.UNREADY.json').read_bytes())
    changed=revision['changed_complete_Source_roles'];assert len(changed)==8
    check('exact_four_failure_blocker_minimal_changed_role_set',set(changed)=={'Root_observation_postclose_META_writer.UNREADY.py','N8_genuine_integrated_controls_driver.UNREADY.py','N8_Root_controls_postclose_META.UNREADY.py','N8_actual_controls_qualification_gate.Source_META_only.py','complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json'})
    check('whole_actual_original_N8_manifest_pin',pin(OLD/'MANIFEST.json')==revision['parent_manifest_pin'])
    parentdirs={str(q):ident(q.lstat())for q in [OLD,*sorted(OLD.rglob('*'))]if q.is_dir()};check('sealed_parent_complete_directory_freeze_unchanged',parentdirs==oldmf['directories'])
    for row in oldmf['members']:
        name=row['relative_path'];check('parent_fullEOF_7ID:'+name,pin(OLD/name)==row['fullpin'])
        a,b=pin(OLD/name),pin(P/name)
        if name not in changed:check('complete_parent_member_byteexact:'+name,(a['sha256'],a['size_bytes'])==(b['sha256'],b['size_bytes']))
    inverse=json.loads((P/'COMPLETE_N8_V2_ALL_CHANGED_ROLE_BYTE_AST_INVERSE.json').read_bytes());check('complete_eight_changed_role_inverse_set',{r['role_basename']for r in inverse['roles']}==set(changed))
    for r in inverse['roles']:
        name=r['role_basename'];original=(OLD/name).read_text();new=(P/name).read_text();restored=restore(new,r['hunks'])
        check('full_current_to_N8_byte_inverse:'+name,restored==original)
        check('full_current_inverse_current_parent_backup_pins:'+name,pin(P/name)==r['new_complete_Source_pin']and pin(OLD/name)==r['parent_original_fullpin']and pin(r['retained_original_fullpin']['path'])==r['retained_original_fullpin']and Path(r['retained_original_fullpin']['path']).read_text()==original)
        if name.endswith('.py'):check('full_current_to_N8_AST_inverse:'+name,astvalue(ast.parse(restored))==astvalue(ast.parse(original)))
    current_n7=json.loads((P/'COMPLETE_N8_V2_CURRENT_FOUR_ROLE_TO_N7_BYTE_AST_INVERSE.json').read_bytes())
    for r in current_n7['roles']:
        name=r['role_basename'];old=Path(r['parent_original_fullpin']['path']).read_text();recovered=restore((P/name).read_text(),r['hunks']);check('complete_current_four_role_to_N7_byte_AST:'+name,recovered==old and astvalue(ast.parse(recovered))==astvalue(ast.parse(old))and pin(P/name)==r['new_complete_Source_pin'])
    scope=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes());roles=scope['required_author_Source_roles'];check('complete_original_twentyone_role_relative_contract',len(roles)==21 and roles==json.loads((OLD/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())['required_author_Source_roles'])
    rolepins={k:pin(P/v)for k,v in roles.items()if v!='MANIFEST.json'}
    check('all_twenty_complete_current_role_Source_pins_match_revision',rolepins==revision['current_role_Source_pins_before_manifest'])
    allowed={'Root_observation_postclose_META_writer.UNREADY.py':{'main'},'N8_genuine_integrated_controls_driver.UNREADY.py':{'main'},'N8_Root_controls_postclose_META.UNREADY.py':{'validate_saved_metadata_types','case_mode','manifest_mode','qualification_mode'},'N8_actual_controls_qualification_gate.Source_META_only.py':{'validate_actual_N8_monitor_controls'},'complete_observation_BUILD5_AB_runtime.UNREADY.py':{'validate_actual_N8_monitor_controls'},'Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py':{'validate_actual_N8_monitor_controls'},'bind_complete_observation_SOURCE_only.UNREADY.py':{'validate_actual_N8_monitor_controls'}}
    for name,mutable in allowed.items():
        a,b=funcs((OLD/name).read_text()),funcs((P/name).read_text())
        new=set(b)-set(a);expected={'recheck_saved_regular_file_pins','recheck_complete_saved_case'}if name in('N8_Root_controls_postclose_META.UNREADY.py','N8_actual_controls_qualification_gate.Source_META_only.py')else({'n8_recheck_saved_regular_file_pins','n8_recheck_complete_saved_case'}if name in('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py')else set())
        check('only_declared_full_raw_recheck_helper_definitions_added:'+name,new==expected and set(a)<=set(b))
        for key in set(a)-mutable:check('original_entire_def_AST_unchanged:'+name+':'+key,astvalue(a[key])==astvalue(b[key]))
        atop=[n for n in ast.parse((OLD/name).read_text()).body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))];btop=[n for n in ast.parse((P/name).read_text()).body if not isinstance(n,(ast.FunctionDef,ast.ClassDef))]
        check('all_original_imports_globals_caps_future_None_AST_unchanged:'+name,[astvalue(n)for n in atop]==[astvalue(n)for n in btop])
    runtime=(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py').read_text();writer=(P/'Root_observation_postclose_META_writer.UNREADY.py').read_text();summary=next(n for n in ast.walk(ast.parse(runtime))if isinstance(n,ast.FunctionDef)and n.name=='summary'and isinstance(n.args.args[0],ast.arg)and n.args.args[0].arg=='self')
    produced={k.arg for n in ast.walk(summary)if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id=='dict'for k in n.keywords}
    consumed={n.slice.value for n in ast.walk(ast.parse(writer))if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='diagnostic'and isinstance(n.slice,ast.Constant)}
    check('B1_all_actual_success_monitor_summary_writer_keys_exist',consumed<=produced,dict(produced=sorted(produced),consumed=sorted(consumed),missing=sorted(consumed-produced)))
    check('B1_removed_false_unchanged_PS_and_old_actual_controls_keys_not_read','original_PS_lsof_argv_timeout_and_PID_parent_chain_unchanged'not in consumed and 'new_instrumented_runtime_controls_actual'not in consumed)
    check('B1_truthful_new_PS_single_closed_PID_and_nonqualification_consumed',{'full_PS_pid_ppid_pgid_state_and_captured_union_explicitly_new','original_parent_chain_never_reduced_except_individually_proven_closed_owned_PIDs','diagnostic_source_contract_is_not_runtime_qualification','new_native_runtime_qualification'}<=consumed)
    driver=(P/'N8_genuine_integrated_controls_driver.UNREADY.py').read_text();dmain=funcs(driver)['main'];barrier=next(n for n in ast.walk(dmain)if isinstance(n,ast.FunctionDef)and n.name=='barrier');btext=ast.get_source_segment(driver,barrier)
    check('B2_before_release_exact_ready_nonZ_descendant_in_actual_PS_and_selection',all(x in btext for x in("type(descendant_ready[k])is int","target in selected","descendant_row['state'].startswith('Z')","descendant_row[k]==descendant_ready[k]","strict_lsof_refusal_target=dict"))and btext.index('strict_lsof_refusal_target=dict')<btext.index("(out/'descendant_release').touch"))
    check('B2_exact_saved_original_failure_canonical_argv_and_selected_descendant','original_joint_bytes_failure'in driver and "ps_target==[strict_lsof_refusal_target['actual_selected_full_PS_row']]"in driver and "scan['actual_returned_argv']==expected_argv"in driver)
    check('B2_original_error_current_type_repr_keys_no_fictitious_message',"error['type']=='builtins.ValueError'"in driver and "error['repr']==repr(ValueError("in driver and "error['message']"not in driver)
    check('B2_canonical_nonzero_or_exact_selected_descendant_missing_only',"scan['actual_returncode']!=0"in driver and "scan['actual_returncode']==0 and target not in returned_pids"in driver and "require(bool(specific_refusals),'complete passing lsof or unrelated later error cannot satisfy strict-refusal control')"in driver)
    check('B2_complete_actual_failure_journal_fullpin_and_no_recording_error',"fullpin(monitor.journal)==journal_pin"in driver and "monitor.recording_errors==[] and monitor.unpersisted==[]"in driver)
    protocol=json.loads((P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes());oldprotocol=json.loads((OLD/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes());copy=json.loads(json.dumps(protocol))
    for idx in(6,9):copy['cases'][idx]['source_required_behavior']=oldprotocol['cases'][idx]['source_required_behavior']
    check('B2_only_two_existing_protocol_case_descriptions_clarified',copy==oldprotocol)
    check('original_twelve_cases_and_all_actual_execution_None_unchanged',len(protocol['case_ids'])==12 and protocol['case_ids']==oldprotocol['case_ids']and all(c['actual_execution']is None and c['actual_root_closed_terminal']is None for c in protocol['cases']))
    post=(P/'N8_Root_controls_postclose_META.UNREADY.py').read_text()
    check('B3_actual_caps_exact_original_nine_keys_ints_values',"k in('original_caps','actual_original_caps')"in post and "set(v)==set(CAPS)and all(type(x)is int for x in v.values())and v==CAPS"in post)
    check('B3_actual_positive_host_owner_PID_PGID_exact_int',all(x in post for x in("type(f['actual_host_PID'])is int","type(o['pid'])is int","type(o['pgid'])is int","type(ready['descendant_pid'])is int and ready['descendant_pid']>0")))
    check('B3_actual_target_lists_exact_positive_int_unique',"all(type(p)is int and p>0 for p in g[k])"in post and "len(g[k])==len(set(g[k]))"in post)
    check('B4_case_and_manifest_and_qualification_existing_complete_rawpins_rechecked',"for view in views.values():recheck_saved_regular_file_pins(view['files'],allow_empty=True)"in post and "recheck_complete_saved_case(c)"in post and "for case in m['cases']:recheck_complete_saved_case(case)"in post and "recheck_saved_regular_file_pins(m['actual_complete_controls_regular_file_pins_before_own_append'])"in post)
    gate=(P/'N8_actual_controls_qualification_gate.Source_META_only.py').read_text();gatefs=funcs(gate)
    class Normalize(ast.NodeTransformer):
        def visit_Constant(self,node):
            if type(node.value)is str:node.value=node.value.replace('actual controls exact n8_fullpin required; None refused','actual controls exact fullpin required; None refused')
            return node
        def visit_Name(self,node):
            if node.id.startswith('n8_'):node.id=node.id[3:]
            if node.id=='N8_CASE_IDS':node.id='CASE_IDS'
            return node
        def visit_FunctionDef(self,node):
            if node.name.startswith('n8_'):node.name=node.name[3:]
            return self.generic_visit(node)
    for name in ('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py'):
        currentfs=funcs((P/name).read_text())
        for k in gatefs:
            counterpart=k if k=='validate_actual_N8_monitor_controls'else'n8_'+k
            norm=Normalize().visit(ast.parse(ast.get_source_segment((P/name).read_text(),currentfs[counterpart])).body[0])
            check('B4_all_full_Q_consumer_blocks_entire_normalized_AST_same:'+name+':'+k,astvalue(norm)==astvalue(gatefs[k]))
    for name in ('N8_actual_controls_qualification_gate.Source_META_only.py','complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py'):
        s=(P/name).read_text();check('B4_all_current_Q_and_manifest_full_regular_rawpins_rechecked:'+name,"q['actual_complete_controls_regular_file_pins_before_own_append']"in s and "manifest['actual_complete_controls_regular_file_pins_before_own_append']"in s and "['actual_complete_postclose_namespace_views']"in s and "view['files'],allow_empty=True"in s)
    check('B4_complete_empty_namespace_lists_accepted_but_missing_fullpins_refused','allow_empty=False'in gate and "type(pins)is list and (allow_empty is True or bool(pins))"in gate)
    for name in ('N8_exact_owner_scope_observer.UNREADY.py','N8_bind_monitor_controls_SOURCE_META_only.UNREADY.py','N8_private_control_child.UNREADY.py','complete_observation_genuine_host.UNREADY.py','COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz'):
        check('complete_original_owner_and_guard_entry_Source_not_changed:'+name,(P/name).read_bytes()==(OLD/name).read_bytes())
    check('no_first_live_census_or_hypothetical_escape_new_gate',revision['first_live_census_prerequisite_added']is False and revision['new_hypothetical_escaped_group_scope_gate_added']is False and (P/'N8_exact_owner_scope_observer.UNREADY.py').read_bytes()==(OLD/'N8_exact_owner_scope_observer.UNREADY.py').read_bytes())
    check('old_failure_Source_review_preserved_actual_int1_not_pass',json.loads((FAILED/'ACTUAL_INDEPENDENT_SOURCE_VERDICT_TOOL_RETURN.json').read_bytes())['terminal_tool_return']['exit_code']==1 and review_failure_preserved(P,FAILED))
    fullrecords=[];py=[]
    for q in sorted(P.rglob('*')):
        assert not q.is_symlink()
        if q.is_file():
            r=pin(q);fullrecords.append(r)
            if q.suffix=='.py':ast.parse(q.read_bytes());py.append(str(q))
    check('all_current_complete_Source_files_fullEOF_and_Python_AST',len(fullrecords)>239 and len(py)>96)
    check('all_future_actual_monitor_Q_control_native_science_Nonefalse',all(revision[k]is None for k in('actual_independent_Source_review','actual_Root_Source_admission','actual_controls_Source_binding','actual_monitor_controls_qualification','actual_native_AB_execution'))and revision['scientific_qualification_created']is False)
    blockers=[c['check']for c in checks if c['passed']is not True]
    result=dict(schema='AUTHOR_COMPLETE_N8_V2_FOUR_BLOCKER_MINIMAL_SOURCE_REPORT_V1',status='AUTHOR_SOURCE_ONLY_PASS_UNREADY_REQUIRES_DIFFERENT_AUTHOR_REVIEW'if not blockers else'AUTHOR_SOURCE_ONLY_FAIL_BLOCKED',source_only=True,parent_manifest_pin=pin(OLD/'MANIFEST.json'),actual_failed_independent_manifest_pin=pin(FAILED/'MANIFEST.json'),actual_failed_independent_report_pin=pin(FAILED/'REVIEW.json'),required_complete_author_Source_roles=roles,current_complete_role_Source_pins_before_manifest=rolepins,check_count=len(checks),checks=checks,check_evidence=evidence,all_checks_passed=not blockers,all_checks_typed_boolean=True,blockers=blockers,all_current_Source_and_small_META_fullpin_records_before_own_report_append=fullrecords,complete_Python_Source_AST_count_before_own_report_append=len(py),complete_original_native_Source_member_count=1365,complete_native_Source_archive_byteexact_transitive_parent_fullEOF=True,changed_complete_role_basenames=changed,original_caps=CAPS,actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_monitor_controls_qualification=None,actual_root_Source_admission=None,actual_bound_control_Source=None,actual_native_AB_execution=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limits=['Finite Source/AST and existing small META only; no candidate or OS/control/API/business execution.','Original author reports, old inverse/MFs and absolute path pins retained byteexact as parent history; this report and the new two complete inverses are current.','Actual Root controls, saved independent review and immutable Q still required before any business request or runtime.'])
    path=P/'AUTHOR_COMPLETE_N8_V2_FINAL_SOURCE_ONLY_REPORT.json'
    with path.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],source_only=True,check_count=len(checks),passed_checks=sum(c['passed']is True for c in checks),blockers=blockers,actual_report_pin=pin(path),complete_Python_Source_AST_count=len(py),actual_candidate_or_API_execution=False),allow_nan=False),flush=True)
    return 0 if not blockers else 1
def review_failure_preserved(p,f):
    folder=p/'PREVIOUS_SEALED_N8_FOUR_BLOCKER_FAILURE_PROVENANCE/INDEPENDENT_FAILED_REVIEW'
    return all((folder/q.relative_to(f)).read_bytes()==q.read_bytes()for q in f.rglob('*')if q.is_file())
if __name__=='__main__':raise SystemExit(main())
