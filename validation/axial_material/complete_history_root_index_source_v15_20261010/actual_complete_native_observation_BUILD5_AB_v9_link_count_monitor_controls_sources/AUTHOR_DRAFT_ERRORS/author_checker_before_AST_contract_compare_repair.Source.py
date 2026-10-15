"""Finite author Source/AST/full EOF checker. Does not import any candidate."""
import ast
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
import tarfile

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
M=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')

def pin(path):
    s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not path.is_symlink()
    with path.open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
    t=path.lstat();assert [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before
    return dict(path=str(path),sha256=sha,size_bytes=s.st_size,identity=before)

def main():
    checks=[];evidence={}
    def check(name,value):
        assert type(value)is bool and name not in {r['check']for r in checks}
        checks.append(dict(check=name,passed=value))
    mf=json.loads((M/'MANIFEST.json').read_bytes());check('actual_complete_N7_mother_manifest_181',len(mf['members'])==181 and pin(M/'MANIFEST.json')['sha256']=='178b885f37bf7c65cdd3375f9be29bd53c7b7e408aa61011894d25bb23cee928')
    changed={'complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py','EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json'}
    retained=[]
    for row in mf['members']:
        name=row['relative_path'];current=M/name;assert pin(current)==row['fullpin']
        target=P/('PREVIOUS_SEALED_N7_SOURCE_PROVENANCE/'+name if name in changed else name)
        check('original_N7_full_byte_retention:'+name,target.read_bytes()==current.read_bytes())
        retained.append(dict(relative_path=name,mother_original_fullpin=row['fullpin'],actual_complete_retained_original_fullpin=pin(target),actual_current_derivative_fullpin=pin(P/name)if name in changed else None))
    (P/'COMPLETE_ORIGINAL_N7_MEMBER_RETENTION.Source_META.json').write_text(json.dumps(dict(schema='COMPLETE_N8_ORIGINAL_N7_MEMBER_RETENTION_V1',source_only=True,mother_manifest_pin=pin(M/'MANIFEST.json'),members=retained,changed_relative_paths=sorted(changed),all181_complete_original_bytes_retained=True,original_source_owner_scope_not_reduced=True,actual_candidate_or_API_execution=False),indent=2)+'\n')
    inv=json.loads((P/'COMPLETE_N8_FOUR_ROLE_BYTE_AST_INVERSE.json').read_bytes())
    for row in inv['roles']:
        name=row['role_basename'];text=(P/name).read_text();lines=text.splitlines(keepends=True)
        check('actual_derivative_pin:'+name,pin(P/name)==row['new_complete_Source_pin'])
        for h in reversed(row['hunks']):
            assert ''.join(lines[h['new_start_line0']:h['new_end_line0']])==h['new_text']
            lines[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(keepends=True)
        restored=''.join(lines);original=(M/name).read_text()
        check('whole_byte_and_AST_inverse:'+name,restored==original and ast.dump(ast.parse(restored),include_attributes=False)==ast.dump(ast.parse(original),include_attributes=False))
    j=json.loads((P/'COMPLETE_REQUIRED_SCOPE_JSON_BYTE_INVERSE.json').read_bytes());check('whole_original_required_scope_JSON_inverse',base64.b64decode(j['complete_original_bytes_base64'])==(M/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes()and base64.b64decode(j['complete_new_bytes_base64'])==(P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())
    py=[];allpins=[]
    for path in sorted(P.rglob('*')):
        if path.is_file():
            allpins.append(pin(path))
            if path.suffix=='.py':ast.parse(path.read_bytes());py.append(pin(path))
    check('all_current_complete_Python_Source_AST_without_execution',len(py)>50)
    archive=P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz';index=json.loads((P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());expected={r['relative_path']:r['full_original_Source_pin']for r in index['members']};native=[]
    with tarfile.open(archive,'r:gz')as t:
        members=t.getmembers();check('complete_original_native_Source_archive_1365_unique',len(members)==len(expected)==1365 and {m.name for m in members}==set(expected))
        for member in members:
            assert member.isfile()and not Path(member.name).is_absolute()and '..'not in Path(member.name).parts
            with t.extractfile(member)as f:
                d=hashlib.sha256();size=0
                while True:
                    raw=f.read(2**20)
                    if not raw:break
                    d.update(raw);size+=len(raw)
            wanted=expected[member.name];check('native_Source_full_member_EOF:'+member.name,d.hexdigest()==wanted['sha256']and size==wanted['size_bytes'])
            native.append(dict(relative_path=member.name,sha256=d.hexdigest(),size_bytes=size))
    with gzip.open(archive,'rb')as stream:
        while stream.read(2**20):pass
    check('complete_original_Source_gzip_CRC_and_EOF',True)
    runtime=(P/'complete_observation_BUILD5_AB_runtime.UNREADY.py').read_text();rt=ast.parse(runtime);mother=ast.parse((M/'complete_observation_BUILD5_AB_runtime.UNREADY.py').read_bytes())
    defs={n.name:n for n in rt.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};olddefs={n.name:n for n in mother.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    for name in ('compile_all','guarded','original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_original_procedure','copy_state_seeds','collect_state','frozen_sources','source_tool_nlink_allowed'):
        check('original_complete_physics_build_guard_shared_seed_AST:'+name,ast.dump(defs[name],include_attributes=False)==ast.dump(olddefs[name],include_attributes=False))
    assigns={n.targets[0].id:ast.literal_eval(n.value)for n in rt.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in('CAPS','FUTURE','ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES','SHARED_INPUT_LIBRARY_LAYOUT')}
    oldassign={n.targets[0].id:ast.literal_eval(n.value)for n in mother.body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)and n.targets[0].id in assigns}
    for key in assigns:check('complete_original_literal_contract:'+key,assigns[key]==oldassign[key])
    contract=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes());roles=contract['required_author_Source_roles'];oldroles=json.loads((M/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())['required_author_Source_roles']
    check('all14_original_roles_plus_exact7_declared_new_owners',len(roles)==21 and all(roles[k]==v for k,v in oldroles.items())and all((P/v).is_file()for v in roles.values()if v!='MANIFEST.json'))
    helper=(P/'N8_exact_owner_scope_observer.UNREADY.py').read_text();ht=ast.parse(helper);cls=next(n for n in ht.body if isinstance(n,ast.ClassDef)and n.name=='ExactOwnerScopeObserver');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)}
    check('original_genuine_start_readFD_childPGID_grace_single_watchdog',"watchdog=original(read_fd,child_pgid,grace)"in helper and 'return watchdog'in helper and 'guard_source,child_pgid'not in helper)
    check('owner_capture_exact_genuine_frame_code_runner_process',"frame.f_code is self.original_process_code"in helper and "frame.f_locals.get('self') is self.runner"in helper and 'del frame'in helper)
    check('only_exact_original_Popen_per_instance_private_wait_overrides',"type(process) is self.original_Popen"in helper and 'process._internal_poll=tracked_poll;process._try_wait=tracked_try_wait'in helper and 'del process._internal_poll;del process._try_wait'in helper)
    check('real_wait_tuple_ECHILD_unknown_non_OSError_no_synthetic_zero', 'class OwnershipUnknown(RuntimeError)'in helper and 'self.original_waitpid(process.pid,flags)'in helper and 'os.WIFEXITED(status) or os.WIFSIGNALED(status)'in helper and 'actual owned waitpid failed; no ECHILD-zero fallback'in helper)
    check('actual_main_thread_default_SIGCHLD_original_lock_required',"len(threading.enumerate())==1"in helper and 'signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL'in helper and 'process._waitpid_lock.locked()'in helper)
    check('no_new_first_census_gate_and_actual_later_PID_reappearance_refused', 'leader closed before any live census' not in helper and 'closed exact PID reappeared in a later census'in helper and 'first_live_census_is_not_a_new_admission_gate=True'in helper)
    check('full_original_parentchain_captured_descendant_PGID_union', "selected=set(original_parent_closure)"in helper and "r['pgid'] in groups"in helper and "self.captured_descendants if p in rows"in helper)
    check('production_optional_controls_hooks_none_and_mode_refusal', 'self.control_after_original_start=None'in helper and 'no post-start controls transition in production'in helper and 'resources._actual_control_barrier=None;resources._actual_control_scan_sink=None'in runtime and 'control_mode=False)'in runtime)
    check('single_strict_complete_lsof_0_2second_8MiB_and_PID_scope',runtime.count("observed=subprocess.run([lsof_tool,")==1 and "timeout=2)"in runtime and "observed.returncode==0"in runtime and "set(returned_pids)==selected"in runtime and '8*2**20'in runtime)
    check('new_PS_full_PPID_PGID_state_explicit',"ps_argv=[ps_tool,'-axo','pid=,ppid=,pgid=,stat=']"in runtime)
    check('same_resources_factory_called_by_business_and_controls',"resources,monitor=build_exact_owner_resources("in runtime and 'runtime.build_exact_owner_resources('in(P/'N8_genuine_integrated_controls_driver.UNREADY.py').read_text())
    gate=ast.parse((P/'N8_actual_controls_qualification_gate.Source_META_only.py').read_bytes());gate_defs={n.name:ast.dump(n,include_attributes=False)for n in gate.body if isinstance(n,ast.FunctionDef)}
    for name in ('complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py'):
        text=(P/name).read_text();tree=ast.parse(text);d={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
        check('Q_function_full_AST_exact:'+name,ast.dump(d['validate_actual_N8_monitor_controls'],include_attributes=False)==gate_defs['validate_actual_N8_monitor_controls'].replace("Name(id='require'","Name(id='n8_require'").replace("Name(id='read_pinned'","Name(id='n8_read_pinned'").replace("Name(id='actual_closed_zero'","Name(id='n8_actual_closed_zero'").replace("Name(id='CASE_IDS'","Name(id='N8_CASE_IDS'").replace("Name(id='recheck_pinned'","Name(id='n8_recheck_pinned'"))
        check('required_actual_Q_and_terminal_None_refusal_before_business:'+name,'actual_monitor_controls_qualification_pin'in text and 'actual_monitor_controls_qualification_terminal_pin'in text and 'validate_actual_N8_monitor_controls('in text)
    protocol=json.loads((P/'N8_TWELVE_GENUINE_CONTROL_PROTOCOL.UNREADY.json').read_bytes());driver=(P/'N8_genuine_integrated_controls_driver.UNREADY.py').read_text()
    check('all12_actual_control_categories_no_future_pass',len(protocol['cases'])==12 and [c['case_id']for c in protocol['cases']]==protocol['case_ids'] and all(c['actual_execution']is None for c in protocol['cases'])and protocol['actual_monitor_controls_qualification']is None)
    check('real_control_barriers_wait_reaper_fork_FD_Source_no_mock_scans',"os.waitpid(pid,os.WNOHANG)"in driver and "owner['process'].wait("in driver and "resources._actual_control_barrier=barrier"in driver and 'os.fork()'in(P/'N8_private_control_child.UNREADY.py').read_text())
    check('real_early_exit_control_before_first_census',"observer.control_after_original_start=close_before_first_census"in driver and 'actual_early_exit_before_census'in driver and 'actual_early_exit_wait0_current_union_positive'in driver and 'actual_unobserved_lifecycle_refused'not in driver)
    check('Root_current_groups_and_frozen_D_E_postclose_required',"actual_current_process_groups_absent"in(P/'N8_Root_controls_postclose_META.UNREADY.py').read_text() and "views['source']==f['actual_complete_Source_D_freeze']"in(P/'N8_Root_controls_postclose_META.UNREADY.py').read_text())
    check('Q_requires_complete12_Root_terminals_and_independent_saved_review','INDEPENDENT_ACTUAL_N8_SAVED_GENUINE_MONITOR_CONTROLS_REVIEW_V1'in(P/'N8_actual_controls_qualification_gate.Source_META_only.py').read_text() and 'ROOT_ACTUAL_N8_MONITOR_CONTROLS_QUALIFICATION_TOOL_TERMINAL_RETURN_V1'in(P/'N8_actual_controls_qualification_gate.Source_META_only.py').read_text())
    check('no_waitid_ctypes_or_new_platform_API_route_in_new_helper','waitid('not in helper and 'ctypes'not in helper)
    check('stdlib_original_Source_link_exception_exact_single_role',"EXPECTED_STDLIB_PATH = '/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/subprocess.py'"in helper and "before==expected['identity'] and before[3]>=1"in helper)
    blockers=[c['check']for c in checks if not c['passed']]
    report=dict(schema='AUTHOR_COMPLETE_N8_EXACT_OWNER_MONITOR_AND_INTEGRATED_CONTROLS_SOURCE_CHECK_V1',status='AUTHOR_SOURCE_CHECK_COMPLETE_UNREADY_NOT_INDEPENDENT_OR_RUNTIME'if not blockers else'AUTHOR_SOURCE_CHECK_BLOCKED_UNREADY',source_only=True,mother_manifest_pin=pin(M/'MANIFEST.json'),actual_complete_changed_role_Source_pins={r['role_basename']:pin(P/r['role_basename'])for r in inv['roles']},required_complete_author_Source_roles=roles,actual_new_role_Source_pins={k:pin(P/v)for k,v in roles.items()if k not in oldroles},check_count=len(checks),checks=checks,all_checks_passed=not blockers,blockers=blockers,complete_Python_Source_AST_count=len(py),complete_original_native_Source_member_count=len(native),complete_native_Source_member_EOF_records=native,all_current_Source_and_small_META_fullpin_records=allpins,actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_monitor_controls_qualification=None,actual_root_Source_admission=None,actual_bound_control_Source=None,actual_native_AB_execution=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,limits=protocol['accurate_remaining_limits'])
    with (P/'AUTHOR_COMPLETE_N8_SOURCE_ONLY_REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=report['status'],source_only=True,check_count=len(checks),all_checks_passed=not blockers,blockers=blockers,actual_report_pin=pin(P/'AUTHOR_COMPLETE_N8_SOURCE_ONLY_REPORT.json'),actual_candidate_or_API_execution=False),allow_nan=False))
    if blockers:raise SystemExit(1)

if __name__=='__main__':main()
