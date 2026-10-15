"""UNREADY genuine integrated monitor controls, one fresh case per Root run.

No native/material/physical input is opened. The same runtime factory and owner
adapter used by future production are called under the exact original runner.
Root must independently close each actual tool/group and qualify the complete
twelve-case set afterwards; this process cannot certify its parent or Q itself.
"""
import argparse
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import threading
import time

SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_CONTROLS_BINDING_REQUIRED'
SOURCE_BINDING_PATH = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v9_link_count_monitor_controls_sources/Root_actual_N8_monitor_controls_Source_binding.json'
SOURCE_BINDING_SHA256 = '4db8beb550fec97ba40291c29e485cb80f8ae00ce6e13071109f82c01451f040'
SUPPORT=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
CASE_IDS=('01_exact_environment_and_sole_wait_owner','02_actual_live_business_and_descendants','03_actual_closed_after_live_PS_census','04_actual_nonzero_exit_preserves_stage_failure','05_actual_closed_leader_and_reparented_group','06_unknown_owner_ECHILD_and_PID_reuse_refusals','07_actual_late_descendant_exit_strict_lsof_failure','08_actual_strict_stream_nonzero_timeout_oversize','09_original_resource_caps_and_frozen_Source','10_original_cleanup_exceptions_and_group_evidence','11_actual_watchdog_pipe_and_group_closure','12_actual_Root_and_independent_saved_control_closure')

def require(v,m):
    if type(v) is not bool or not v:raise ValueError(m)

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
        d={}
        for k,v in items:require(k not in d,'duplicate actual control key');d[k]=v
        return d
    return validate_saved_metadata_types(json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v))))

def fullpin(path):
    p=Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    require(p.is_absolute() and stat.S_ISREG(s.st_mode) and s.st_nlink==1 and all(not q.is_symlink()for q in(p,*p.parents)),'actual regular single-link Source/control META')
    with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    t=p.lstat();require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before,'actual Source/control EOF unchanged')
    return dict(path=str(p),sha256=d,size_bytes=s.st_size,identity=before)

def metadata(pin):
    require(type(pin) is dict and fullpin(pin['path'])==pin,'actual full META pin')
    return strict_json(Path(pin['path']).read_bytes())

def write_new(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())

def actual_zero(pin,schema):
    t=metadata(pin);a=t['terminal_tool_return']
    require(t['schema']==schema and t['closed'] is True and t['observed_terminal'] is True and t['session_repolled_after_close'] is False and type(a['exit_code']) is int and a['exit_code']==0 and 'session_id'not in a and a['chunk_id']==t['actual_terminal_chunk'],'actual observed typedzero Root Source tool')
    return strict_json(a['output'])

def wait_small_file(path,deadline):
    while not path.exists():
        require(time.monotonic()<deadline,'original stage/whole controls clock')
        time.sleep(.01)
    return strict_json(path.read_bytes())

def main():
    cli=argparse.ArgumentParser();cli.add_argument('--case-id',required=True,choices=CASE_IDS);cli.add_argument('--actual-source-binding-terminal',required=True);cli.add_argument('--independent-bound-control-Source-prelaunch-review',required=True);a=cli.parse_args()
    started=time.monotonic()
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_CONTROLS_BINDING_REQUIRED' and type(SOURCE_BINDING_PATH) is str and type(SOURCE_BINDING_SHA256) is str,'UNREADY Source refuses all controls/APIs')
    binding_pin=fullpin(SOURCE_BINDING_PATH);require(binding_pin['sha256']==SOURCE_BINDING_SHA256,'actual controls Source binding SHA')
    b=metadata(binding_pin);author=b['actual_author_Source_contract']
    require(b['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1' and b['source_only'] is True and b['actual_control_execution'] is None and b['original_caps']==CAPS,'only actual Source-bound fresh monitor controls')
    for p in author.values():require(fullpin(p['path'])==p,'all actual controls Source owners unchanged')
    source_truth=fullpin(a.actual_source_binding_terminal);source_output=actual_zero(source_truth,'ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_TOOL_TERMINAL_RETURN_V1')
    require(source_output['actual_controls_Source_binding_pin']==binding_pin and source_output['bound_controls_driver_Source_pin']==fullpin(Path(__file__).resolve()),'actual Root Source-binding stdout couples driver and binding')
    preflight_pin=fullpin(a.independent_bound_control_Source_prelaunch_review);preflight=metadata(preflight_pin)
    require(preflight['schema']=='INDEPENDENT_ACTUAL_N8_BOUND_MONITOR_CONTROLS_SOURCE_PRELAUNCH_REVIEW_V1' and preflight['status']=='PASS_ACTUAL_BOUND_CONTROL_SOURCE_ONLY_NO_CONTROLS_EXECUTION' and preflight['source_only'] is True and preflight['all_checks_passed'] is True and preflight['blockers']==[] and preflight['actual_controls_Source_binding_pin']==binding_pin and preflight['actual_bound_controls_driver_Source_pin']==fullpin(Path(__file__).resolve()) and preflight['actual_Source_binding_tool_terminal_pin']==source_truth,'independent actual bound Source prelaunch mandatory')
    require(not sys.flags.optimize and sys.gettrace() is None and sys.getprofile() is None and all(os.environ.get(k)=='1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')),'exact original nonoptimized one-thread controls environment')
    require(hashlib.sha256(SUPPORT.read_bytes()).hexdigest()==SUPPORT_SHA,'original genuine support Source')
    spec=importlib.util.spec_from_file_location('axmat_N8_controls_original_support',SUPPORT);support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    require(Path(sys.executable).resolve()==support.PYTHON,'exact original Python')
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_N8_controls_original_helper')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_N8_controls_original_resource')
    full,production=helper.modules();helper.guard_admission(full)
    runtime,_=support.load(Path(author['runtime_template']['path']),author['runtime_template']['sha256'],'axmat_N8_controls_actual_complete_runtime')
    case_index=CASE_IDS.index(a.case_id);ns=b['case_namespaces'][a.case_id]
    roots=tuple(Path(ns[k])for k in('host','output','control','source','receipts'));host,out,control,source,receipts=roots
    require(len(set(roots))==5 and not any(p.is_relative_to(q)for p in roots for q in roots if p!=q),'actual disjoint complete control HOCDE')
    require(all(p.is_absolute() and p!=support.ART and p.is_relative_to(support.ART) and all(not q.is_symlink()for q in(p,*p.parents))for p in roots[:3]) and all(p.is_relative_to(support.BASE) and p!=support.BASE for p in roots[3:]),'Root fixed ART/base control roots')
    require(not any(os.path.lexists(p)for p in roots[:3]),'fresh case namespaces zero retry')
    dfreeze,efreeze=runtime.tree(source),runtime.tree(receipts)
    history=resource.history_roots([str(p)for p in(host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    resources,monitor=runtime.build_exact_owner_resources(support,roots,b['tool_pins'],started,dfreeze,efreeze,history,(resource,full,production))
    before=resources.check();require(before['artifact_bytes']+2*2**30<96*2**30 and before['disk_free_bytes']-2*2**30>=8*2**30,'original complete reserve')
    host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir();(host/'CONTROLS').mkdir();shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
    require(fullpin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original guard Source bytes')
    runner=full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'CONTROLS',resources)
    monitor.install_bounded_wrappers(runner);deadline=time.monotonic()+600;monitor.stage_deadline=deadline
    observer=runtime.attach_exact_owner_observer(runner,resources,monitor,b['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,author['owner_scope_helper'],support,control_mode=True)
    selected_case={1:'live_descendant',2:'closed_after_PS',3:'nonzero',4:'closed_leader_group',5:'external_reaper',6:'late_descendant_exit',7:'byte_producer',9:'late_descendant_exit',10:'closed_after_PS'}.get(case_index,'closed_after_PS')
    fixture=Path(author['monitor_control_child_Source']['path']);case_folder=host/'CONTROLS';gate_events=[];barrier_used=False;strict_lsof_refusal_target=None;expected_failure=case_index in(3,5,6,9)
    actual_scans=[]
    def scan_sink(joint,scan,state):
        require(observer.control_mode is True,'actual controls-only full raw sink')
        event=dict(schema='ACTUAL_N8_CONTROL_COMPLETE_SCAN_V1',joint=joint,complete_actual_raw_scan=scan,actual_owner_state=state)
        raw=(json.dumps(event,allow_nan=False)+'\n').encode();monitor.disk_account(len(raw))
        target=host/'runtime/ACTUAL_CONTROL_COMPLETE_SCANS.jsonl'
        with target.open('ab') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
        monitor.disk_account(0);actual_scans.append(dict(joint=joint,state=state))
        if selected_case=='live_descendant' and barrier_used and joint['open_unlinked_bytes']>0 and not(out/'leader_release').exists():
            (out/'leader_release').touch(exist_ok=False)
    resources._actual_control_scan_sink=scan_sink
    original_signal=signal.getsignal(signal.SIGCHLD);actual_error=None;after=None;command=[str(support.PYTHON),'-B',str(fixture),selected_case,str(out),repr(deadline)]
    def barrier(rows,selected):
        nonlocal barrier_used,strict_lsof_refusal_target
        if barrier_used:return
        business=[o for o in observer.owners.values()if o['role']=='business' and o['closed_wait'] is None]
        if not business or not(out/'leader_ready.json').exists():return
        owner=business[-1];pid=owner['pid'];row=rows.get(pid)
        if row is None or row['state'].startswith('Z'):return
        ready=strict_json((out/'leader_ready.json').read_bytes());require(ready['pid']==pid and ready['pgid']==pid,'real private child ready matches exact owner/group')
        if selected_case in('live_descendant','closed_leader_group','late_descendant_exit') and not(out/'descendant_ready.json').exists():return
        barrier_used=True
        gate_events.append(dict(event='actual_full_PS_before_control_transition',complete_rows=rows,selected_original_parentchain=sorted(selected),actual_owner_pid=pid,actual_ready=ready))
        if selected_case=='live_descendant':return
        if selected_case=='late_descendant_exit':
            descendant_ready=strict_json((out/'descendant_ready.json').read_bytes())
            require(all(type(descendant_ready[k])is int and descendant_ready[k]>0 for k in('pid','ppid','pgid')) and type(ready['descendant_pid'])is int and ready['descendant_pid']>0,'exact positive actual ready descendant identity')
            target=descendant_ready['pid'];descendant_row=rows.get(target)
            require(target==ready['descendant_pid'] and descendant_ready['ppid']==pid and descendant_ready['pgid']==owner['pgid'] and target in selected and descendant_row is not None and all(descendant_row[k]==descendant_ready[k]for k in('pid','ppid','pgid')) and not descendant_row['state'].startswith('Z'),'ready non-zombie descendant must be actually selected in saved fullPS before release')
            strict_lsof_refusal_target=dict(actual_ready=descendant_ready,actual_selected_full_PS_row=descendant_row)
            gate_events.append(dict(event='actual_non_zombie_descendant_selected_before_release',**strict_lsof_refusal_target))
            (out/'descendant_release').touch(exist_ok=False)
            closed=wait_small_file(out/'descendant_real_wait.json',min(deadline,time.monotonic()+2))
            require(type(closed['pid'])is int and closed['pid']==ready['descendant_pid'] and closed['exited'] is True and type(closed['exitcode'])is int and closed['exitcode']==0,'real compiler-descendant parent wait, never a fake closed row')
            gate_events.append(dict(event='actual_descendant_closed_by_its_own_parent',actual_wait=closed))
            return
        if selected_case=='external_reaper':
            try:observer.register(owner['process'],'business',owner['args'])
            except BaseException as error:gate_events.append(dict(event='actual_duplicate_exact_owner_refused',actual_error=runtime.monitor_error(error)))
            else:raise ValueError('duplicate actual owner accepted')
            (out/'leader_release').touch(exist_ok=False)
            # Deliberate real negative control, clearly outside the owning
            # instance waiter. Actual ECHILD must be rejected afterwards.
            wait_deadline=min(deadline,time.monotonic()+2)
            while True:
                waited=os.waitpid(pid,os.WNOHANG)
                if waited[0]==pid:break
                require(waited[0]==0 and time.monotonic()<wait_deadline,'actual bounded negative waiter only');time.sleep(.01)
            gate_events.append(dict(event='actual_external_control_waiter_reaped',actual_pid_status=list(waited)))
            return
        (out/'leader_release').touch(exist_ok=False)
        code=owner['process'].wait(timeout=min(2,max(.001,deadline-time.monotonic())))
        gate_events.append(dict(event='actual_original_Popen_wait_after_PS',actual_returncode=code,actual_owner_state=observer.summary()))
    resources._actual_control_barrier=barrier
    try:
        # These negative controls call the actual attached wrapper and exact
        # original objects. They do not replace PS/lsof/cleanup outcomes.
        if case_index in(0,5):
            rejected=[]
            try:observer.start_wrapper(-1,os.getpid(),runner.bounded.TERM_GRACE_SECONDS)
            except BaseException as error:rejected.append(dict(input='wrong_original_frame',actual_error=runtime.monitor_error(error)))
            require(len(rejected)==1,'wrong genuine frame actually refused')
            signal.signal(signal.SIGCHLD,signal.SIG_IGN)
            try:
                try:observer.environment()
                except BaseException as error:rejected.append(dict(input='actual_SIGCHLD_ignored',actual_error=runtime.monitor_error(error)))
            finally:signal.signal(signal.SIGCHLD,original_signal)
            require(len(rejected)==2,'actual ignored SIGCHLD refused, original disposition restored')
            gate_events.extend(rejected)
        try:runner.execute(case_folder,'actual_private_control',command,600)
        except BaseException as error:actual_error=runtime.monitor_error(error)
        require((actual_error is not None)==expected_failure,'actual case outcome must match required positive/refusal; no retry or nonzero whitelist')
        require(barrier_used,'actual ready pipe/file transition observed, no sleep-based guessed exit')
        if case_index==5:
            require(any(x.get('actual_errno')==errno.ECHILD for x in [o.get('last_wait') or {} for o in observer.owners.values()]),'actual ECHILD negative evidence required')
        if case_index==1:
            require(any(s['joint']['open_unlinked_bytes']>0 and any(o['role']=='business' and o['closed_wait'] is None for o in s['state']['owners']) for s in actual_scans),'actual live business/descendant/unlinked FD counted before release')
        if case_index==4:
            require(any(s['joint']['open_unlinked_bytes']>0 and any(o['role']=='business' and o['closed_wait'] is not None for o in s['state']['owners']) for s in actual_scans),'actual retained descendant FD and exact closed leader counted in complete scan')
        if case_index==3:
            require(any(o['closed_wait'] is not None and o['closed_wait']['actual_exit_code']==7 for o in observer.owners.values() if o['role']=='business'),'actual nonzero original exit tuple remains 7')
        if case_index in(6,9):
            require(strict_lsof_refusal_target is not None and monitor.events>0 and monitor.journal is not None and monitor.recording_errors==[] and monitor.unpersisted==[],'actual selected-descendant strict refusal requires complete persisted original failure evidence')
            journal_pin=fullpin(monitor.journal);failure_events=[strict_json(line)for line in monitor.journal.read_bytes().splitlines()]
            require(fullpin(monitor.journal)==journal_pin,'complete original failure journal unchanged across strict refusal check')
            target=strict_lsof_refusal_target['actual_ready']['pid'];specific_refusals=[]
            for event in failure_events:
                if event.get('event')!='original_joint_bytes_failure':continue
                ps=event['original_ps'];scan=event['original_lsof'];selected_pids=event['original_parent_chain_selected_PIDs']
                if target not in selected_pids:continue
                require(type(ps['actual_returncode'])is int and ps['actual_returncode']==0 and ps['streams_complete']is True and type(ps['actual_stdout'])is str,'specific refusal originates from a real complete strict fullPS')
                ps_target=[]
                for line in ps['actual_stdout'].splitlines():
                    words=line.split();require(len(words)==4 and all(w.isdigit()for w in words[:3]),'saved original strict refusal fullPS rows')
                    if int(words[0])==target:ps_target.append(dict(pid=int(words[0]),ppid=int(words[1]),pgid=int(words[2]),state=words[3]))
                require(ps_target==[strict_lsof_refusal_target['actual_selected_full_PS_row']],'strict refusal uses the saved selected non-zombie descendant census')
                expected_argv=[b['tool_pins']['lsof']['path'],'-nP','-F','pfnsiDtk','-a','-p',','.join(map(str,sorted(selected_pids)))]
                require(scan['source_argv_for_actual_selected_PIDs']==expected_argv and scan['actual_returned_argv']==expected_argv and scan['streams_complete']is True and type(scan['actual_returncode'])is int and type(scan['actual_stdout'])is str and type(scan['actual_stderr'])is str,'actual single canonical lsof invocation and complete raw refusal streams')
                returned_pids=[]
                for line in scan['actual_stdout'].splitlines():
                    if line.startswith('p'):require(line[1:].isdigit(),'saved actual lsof PID field');returned_pids.append(int(line[1:]))
                error=event['original_error'];nonzero=scan['actual_returncode']!=0 and error['type']=='builtins.ValueError' and error['repr']==repr(ValueError('full live own process file scan required'))
                missing_target=scan['actual_returncode']==0 and target not in returned_pids and error['type']=='builtins.ValueError' and error['repr']==repr(ValueError('single strict lsof0 complete selected PID coverage; no absent-PID acceptance'))
                if nonzero or missing_target:specific_refusals.append(dict(actual_failure_event_sequence=event['sequence'],actual_selected_descendant_PID=target,actual_canonical_lsof_returncode=scan['actual_returncode'],actual_lsof_returned_PIDs=returned_pids,canonical_nonzero_refused=nonzero,selected_descendant_coverage_missing_refused=missing_target))
            require(bool(specific_refusals),'complete passing lsof or unrelated later error cannot satisfy strict-refusal control')
            gate_events.append(dict(event='actual_specific_canonical_strict_lsof_refusal_verified',actual_failure_journal_pin=journal_pin,actual_refusals=specific_refusals))
        if case_index==7:
            require((case_folder/'actual_private_control.log').stat().st_size==8*2**20,'actual private 8MiB producer only; no canonical tool oversize claim')
        # An ECHILD negative leaves original Popen cache unknown by design.
        # Do not call it zero and do not force another original wait. Root's
        # separately saved current PS/group closure is mandatory for all cases.
        if not expected_failure:after=resources.check()
        if case_index==0:
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
        require(runtime.tree(source)==dfreeze and runtime.tree(receipts)==efreeze,'complete frozen D/E retained')
        monitor.disk_account(0)
        facts=dict(schema='ACTUAL_N8_GENUINE_MONITOR_CONTROL_CASE_FACTS_V1',case_id=a.case_id,source_only=False,actual_author_Source_contract=author,actual_controls_Source_binding_pin=binding_pin,actual_Source_binding_tool_terminal_pin=source_truth,actual_independent_bound_Source_prelaunch_review_pin=preflight_pin,actual_host_PID=os.getpid(),actual_case_command=command,actual_expected_refusal=expected_failure,actual_error=actual_error,actual_gate_events=gate_events,actual_all_stage_records=runner.records,actual_exact_owner_state=observer.summary(),actual_failure_only_monitor_evidence=monitor.summary(include_unpersisted=True),actual_original_caps=CAPS,actual_resources_before=before,actual_resources_after=after,actual_complete_Source_D_freeze=dfreeze,actual_complete_receipt_E_freeze=efreeze,actual_Source_D_and_receipt_E_frozen=True,actual_fixture_Source_pin=fullpin(fixture),actual_genuine_guard_Source_pins=[support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)],actual_original_helper_pin=hpin,actual_original_resource_pin=rpin,actual_original_guard_classes_MRO_modified=False,canonical_OS_nonzero_timeout_oversize_or_EPERM_manufactured=False,private_byte_producer_not_canonical_tool_evidence=True,Root_actual_control_tool_terminal=None,Root_actual_current_process_group_closure=None,actual_control_qualification=None,actual_native_build_or_AB_executed=False,native_transport_executed=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        path=host/'ACTUAL_CONTROL_CASE_FACTS.json';raw=(json.dumps(facts,indent=2,allow_nan=False)+'\n').encode();monitor.disk_account(len(raw));write_new(path,facts);monitor.disk_account(0)
        print(json.dumps(dict(status='ACTUAL_CONTROL_CASE_FACTS_ONLY_ROOT_CLOSURE_AND_INDEPENDENT_REVIEW_REQUIRED',actual_control_case_facts_pin=fullpin(path),actual_monitor_controls_qualification=None,actual_native_or_scientific_qualification_created=False),allow_nan=False),flush=True)
    finally:
        try:observer.restore_original_objects()
        finally:
            signal.signal(signal.SIGCHLD,original_signal);monitor.restore_bounded_objects()

if __name__=='__main__':main()
