from pathlib import Path
import ast, difflib, hashlib, json, shutil, stat, tarfile, tempfile

PARENT=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
EXPECTED_MF='6b743dbb801efa359929b5c2bd409b337fdaf65d417a8e08debaeb917eba392f'

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not p.is_symlink()
    h=hashlib.sha256()
    with p.open('rb')as f:
        for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
    assert ident(p.lstat())==ident(s)
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ident(s))
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def replace_once(t,old,new):
    assert t.count(old)==1,(old[:100],t.count(old));return t.replace(old,new,1)
def definition(t,name):
    n=next(n for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name)
    return ''.join(t.splitlines(True)[n.lineno-1:n.end_lineno])
def namespace(t):
    return t.replace('REQUIRED_N6_FRESH_NAMESPACES','REQUIRED_N7_FRESH_NAMESPACES').replace('-AB-v6-','-AB-v7-').replace('_AB_v6_','_AB_v7_').replace('fixed v6','fixed v7').replace('new fixed v6','new fixed v7')

MONITOR_SOURCE=r'''
def monitor_error(error):
    return dict(type=type(error).__module__+'.'+type(error).__qualname__,repr=repr(error),
        complete_traceback=''.join(traceback.format_exception(type(error),error,error.__traceback__)))

def monitor_stream(value):
    # Preserve the exact object returned by the original text=True call. A
    # TimeoutExpired may instead carry partial bytes: never call those complete.
    if value is None or type(value)is str:return value
    if type(value)is bytes:return dict(original_type='bytes',base64=base64.b64encode(value).decode('ascii'))
    raise TypeError('unexpected actual subprocess stream type')

class FailureOnlyMonitorEvidence:
    """Failure evidence only; no accepted scan, cleanup, or new qualification.

    Every successful original monitor scan remains ephemeral. The original
    failed call is committed before any added PS query and is never rewritten.
    Disk checks refuse writes above the unchanged known byte caps. A failed
    original lsof leaves open-unlinked accounting unverified; a previous value
    is explicitly stale evidence, never a replacement passing observation.
    """
    def __init__(self,roots,tools,started,resources,base_history_check,dfreeze,efreeze):
        self.roots=tuple(map(Path,roots));self.host=self.roots[0];self.tools=tools
        self.started=started;self.resources=resources;self.base_history_check=base_history_check
        self.dfreeze=dfreeze;self.efreeze=efreeze;self.stage_deadline=None
        self.latest_joint=None;self.latest_failed_selection=[];self.events=0
        self.unpersisted=[];self.recording_errors=[];self.journal=None;self.originals=None
        self.host_created_only_for_failure=False
    def clock(self):
        now=time.monotonic();whole=CAPS['whole_seconds']-(now-self.started)
        stage=None if self.stage_deadline is None else self.stage_deadline-now
        return dict(whole_seconds_remaining=whole,stage_seconds_remaining=stage,
            whole_cap_satisfied=whole>0,stage_cap_satisfied=stage is None or stage>0,
            no_additional_time_budget=True)
    def disk_account(self,increment):
        require(type(increment)is int and increment>=0,'exact diagnostic byte increment')
        total=0;seen=set()
        for root in self.roots:
            if not root.exists():continue
            for p in root.rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'diagnostic whole namespace noalias')
                if stat.S_ISDIR(s.st_mode):continue
                require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'diagnostic regular singlelink only')
                key=(s.st_dev,s.st_ino);require(key not in seen,'diagnostic no hardlink duplicate');seen.add(key);total+=s.st_size
        require(tree(self.roots[3])==self.dfreeze and tree(self.roots[4])==self.efreeze,'diagnostic never changes frozen D/E')
        history=self.base_history_check(self.resources)
        external=sum(p['size_bytes']for p in self.dfreeze['files']+self.efreeze['files'])
        previous_unlinked=0 if self.latest_joint is None else self.latest_joint['open_unlinked_bytes']
        require(total+previous_unlinked+increment<CAPS['joint_archive_bytes'],'diagnostic bytes within original joint2GiB; no new allowance')
        require(history['artifact_bytes']+external+previous_unlinked+increment<=CAPS['history_bytes'],'diagnostic bytes within original history96GiB')
        require(history['disk_free_bytes']-increment>=CAPS['free_floor_bytes'],'diagnostic bytes within original free8GiB floor')
        return dict(actual_regular_joint_bytes=total,additional_record_bytes=increment,
            previous_complete_open_unlinked_bytes=previous_unlinked,
            current_open_unlinked_verified=False,failed_scan_never_replaced_by_this_account=True,
            actual_original_history_check=history,external_D_E_bytes=external,clock=self.clock())
    def record(self,event):
        self.events+=1
        event=dict(schema='ACTUAL_N7_FAILURE_ONLY_MONITOR_EVENT_V1',sequence=self.events,
            actual_host_PID=os.getpid(),clock=self.clock(),**event)
        try:
            if not self.host.exists():
                self.disk_account(0);self.host.mkdir();self.host_created_only_for_failure=True
            require(self.host.is_dir()and not self.host.is_symlink(),'failure evidence actual fresh H')
            folder=self.host/'runtime';folder.mkdir(exist_ok=True)
            require(folder.is_dir()and not folder.is_symlink(),'failure evidence actual H runtime directory')
            target=folder/'ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'
            if target.exists():
                s=target.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not target.is_symlink(),'failure journal noalias')
            else:require(not os.path.lexists(target),'failure journal fresh ordinary file')
            # Accounting precedes each real append; the journal itself belongs
            # to H and every later original/full postclose traversal counts it.
            raw=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
            account=self.disk_account(len(raw));event['actual_diagnostic_write_byte_account_before']=account
            raw=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
            self.disk_account(len(raw))
            with target.open('ab')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            self.journal=target;self.disk_account(0)
        except BaseException as error:
            # Recording errors never swallow/replace the original guard or
            # cleanup exception. Unwritten raw is retained for the bounded
            # failure result, if the same original disk caps permit it.
            self.unpersisted.append(event);self.recording_errors.append(monitor_error(error))
    def failure_ps(self,phase,business_pid=None):
        event=dict(event='additional_postfailure_PS_liveness',phase=phase,
            original_failed_selection=list(self.latest_failed_selection),business_child_PID=business_pid,
            original_selection_not_changed=True,used_to_accept_original_failure=False,
            observed=False,actual_argv=None,actual_returncode=None,actual_stdout=None,actual_stderr=None)
        try:
            timing=self.clock();remaining=timing['whole_seconds_remaining']
            if timing['stage_seconds_remaining']is not None:remaining=min(remaining,timing['stage_seconds_remaining'])
            require(remaining>0,'no additional diagnostic query after original whole/stage deadline')
            self.disk_account(0)
            argv=[self.tools['ps']['path'],'-axo','pid=,ppid=,pgid=']
            event['actual_argv']=argv
            observed=subprocess.run(argv,capture_output=True,text=True,timeout=min(2,remaining))
            event.update(observed=True,actual_returncode=observed.returncode,
                actual_stdout=observed.stdout,actual_stderr=observed.stderr,streams_complete=True)
            # This additional query is evidence only. Nonzero never qualifies
            # or repairs a failed scan; parsing cannot change any selected PID.
            if type(observed.returncode)is int and observed.returncode==0:
                rows=[]
                for line in observed.stdout.splitlines():
                    words=line.split();require(len(words)==3 and all(w.isdigit()for w in words),'complete actual failure-only PS three-column output')
                    rows.append(dict(pid=int(words[0]),ppid=int(words[1]),pgid=int(words[2])))
                targets=set(self.latest_failed_selection)
                if type(business_pid)is int and business_pid>0:targets.add(business_pid)
                event['actual_selected_or_child_rows']=[r for r in rows if r['pid']in targets]
                event['actual_child_process_group_rows']=[r for r in rows if type(business_pid)is int and r['pgid']==business_pid]
        except BaseException as error:
            event['observation_error']=monitor_error(error)
            if isinstance(error,(subprocess.TimeoutExpired,subprocess.CalledProcessError)):
                event.update(actual_stdout=monitor_stream(error.output),actual_stderr=monitor_stream(error.stderr),
                    streams_complete=False,actual_returncode=error.returncode if isinstance(error,subprocess.CalledProcessError)else None)
        self.record(event)
    def joint_failure(self,frame,error):
        observed=frame.get('observed');ps_process=frame.get('ps_process')
        selected=frame.get('selected');self.latest_failed_selection=[]if selected is None else sorted(selected)
        ps_complete='ps_stdout'in frame and 'ps_stderr'in frame
        ps_stdout=frame.get('ps_stdout');ps_stderr=frame.get('ps_stderr')
        lsof_stdout=None if observed is None else observed.stdout;lsof_stderr=None if observed is None else observed.stderr
        if isinstance(error,(subprocess.TimeoutExpired,subprocess.CalledProcessError)):
            command=error.cmd
            if command==frame.get('ps_argv') and not ps_complete:ps_stdout=error.output;ps_stderr=error.stderr
            elif observed is None:lsof_stdout=error.output;lsof_stderr=error.stderr
        original_lsof_argv=None if selected is None else [self.tools['lsof']['path'],'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))]
        self.record(dict(event='original_joint_bytes_failure',original_error=monitor_error(error),
            original_ps=dict(actual_argv=frame.get('ps_argv'),actual_diagnostic_PID=frame.get('ps_diagnostic_pid'),
                actual_returncode=frame.get('ps_returncode'),actual_stdout=monitor_stream(ps_stdout),actual_stderr=monitor_stream(ps_stderr),
                streams_complete=ps_complete,closed_returncode_cached=None if ps_process is None else ps_process.returncode),
            original_parent_chain_selected_PIDs=list(self.latest_failed_selection),
            original_lsof=dict(source_argv_for_actual_selected_PIDs=original_lsof_argv,
                actual_returned_argv=None if observed is None else observed.args,
                actual_returncode=None if observed is None else observed.returncode,
                actual_stdout=monitor_stream(lsof_stdout),actual_stderr=monitor_stream(lsof_stderr),streams_complete=observed is not None),
            original_text_mode_unchanged=True,no_strip_or_stream_truncation=True,
            N6_original_failed_lsof_raw_remains_unknown=True,
            original_scan_failure_still_raises=True))
        self.failure_ps('after_original_failed_joint_scan')
    def install_bounded_wrappers(self,runner):
        bounded=runner.bounded
        original_terminate_group=bounded.terminate_group
        original_finish_liveness_watchdog=bounded.finish_liveness_watchdog
        self.originals=(bounded,original_terminate_group,original_finish_liveness_watchdog)
        def terminate_group(process):
            active=sys.exc_info()[1];cleanup_error=None
            if active is not None:
                self.record(dict(event='before_original_terminate_group',original_active_exception=monitor_error(active),
                    actual_business_PID=process.pid,cached_business_returncode=process.returncode,
                    original_object_captured_before_wrapping=True,cleanup_success_not_inferred=True))
                self.failure_ps('before_original_terminate_group',process.pid)
            try:return original_terminate_group(process)
            except BaseException as error:
                cleanup_error=error
                self.record(dict(event='original_terminate_group_exception',original_active_exception=None if active is None else monitor_error(active),
                    actual_cleanup_exception=monitor_error(error),actual_business_PID=process.pid,
                    cached_business_returncode=process.returncode,cleanup_success_not_inferred=True))
                raise
            finally:
                if active is not None or cleanup_error is not None:
                    self.record(dict(event='after_original_terminate_group',actual_business_PID=process.pid,
                        cached_business_returncode=process.returncode,original_delegate_returned=cleanup_error is None,
                        cleanup_success_not_inferred=True))
                    self.failure_ps('after_original_terminate_group',process.pid)
        def finish_liveness_watchdog(write_fd,watchdog):
            active=sys.exc_info()[1];cleanup_error=None
            if active is not None:
                self.record(dict(event='before_original_finish_liveness_watchdog',original_active_exception=monitor_error(active),
                    actual_watchdog_PID=watchdog.pid,actual_original_write_fd=write_fd,
                    cached_watchdog_returncode=watchdog.returncode,cleanup_success_not_inferred=True))
                self.failure_ps('before_original_finish_liveness_watchdog',watchdog.pid)
            try:return original_finish_liveness_watchdog(write_fd,watchdog)
            except BaseException as error:
                cleanup_error=error
                self.record(dict(event='original_finish_liveness_watchdog_exception',original_active_exception=None if active is None else monitor_error(active),
                    actual_cleanup_exception=monitor_error(error),actual_watchdog_PID=watchdog.pid,
                    cached_watchdog_returncode=watchdog.returncode,cleanup_success_not_inferred=True))
                raise
            finally:
                if active is not None or cleanup_error is not None:
                    self.record(dict(event='after_original_finish_liveness_watchdog',actual_watchdog_PID=watchdog.pid,
                        cached_watchdog_returncode=watchdog.returncode,original_delegate_returned=cleanup_error is None,
                        cleanup_success_not_inferred=True))
                    self.failure_ps('after_original_finish_liveness_watchdog',watchdog.pid)
        bounded.terminate_group=terminate_group
        bounded.finish_liveness_watchdog=finish_liveness_watchdog
    def restore_bounded_objects(self):
        if self.originals is not None:
            bounded,original_terminate_group,original_finish_liveness_watchdog=self.originals
            bounded.terminate_group=original_terminate_group
            bounded.finish_liveness_watchdog=original_finish_liveness_watchdog
    def summary(self,include_unpersisted=False):
        return dict(schema='ACTUAL_N7_FAILURE_ONLY_MONITOR_SUMMARY_V1',failure_event_count=self.events,
            journal_pin=None if self.journal is None else fullpin(self.journal),
            additional_recording_errors=list(self.recording_errors),
            unpersisted_complete_events=list(self.unpersisted)if include_unpersisted else [],
            original_successful_scan_raw_history_not_persisted=True,
            original_PS_lsof_argv_timeout_and_PID_parent_chain_unchanged=True,
            only_two_bounded_callable_objects_wrapped_for_failure_evidence=True,
            original_bounded_Source_bytes_and_supervisor_classes_unchanged=True,
            original_guard_and_cleanup_exceptions_both_retained_without_acceptance=True,
            original_watchdog_cleanup_flag_not_actual_cleanup_proof=True,
            host_created_only_for_failure_evidence=self.host_created_only_for_failure,
            original_caps=CAPS,actual_clock=self.clock(),
            diagnostic_source_contract_is_not_runtime_qualification=True,
            new_instrumented_runtime_controls_actual=None,new_native_runtime_qualification=None,
            N6_original_failed_lsof_raw_remains_unknown=True)
'''

assert pin(PARENT/'MANIFEST.json')['sha256']==EXPECTED_MF
mf=json.loads((PARENT/'MANIFEST.json').read_bytes());before={r['relative_path']:pin(PARENT/r['relative_path'])for r in mf['members']}
assert all(before[r['relative_path']]==r['fullpin']for r in mf['members'])
assert {str(p.relative_to(PARENT))for p in PARENT.rglob('*')if p.is_file()}==set(before)|{'MANIFEST.json'}
P=Path(tempfile.mkdtemp(prefix='axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_',dir='/private/tmp'))
for p in PARENT.rglob('*'):
    if p.name=='MANIFEST.json'and p.parent==PARENT:continue
    target=P/p.relative_to(PARENT)
    if p.is_dir():target.mkdir(exist_ok=True)
    else:shutil.copy2(p,target)
provenance=P/'PREVIOUS_SEALED_N6_SOURCE_PROVENANCE';provenance.mkdir()
shutil.copy2(PARENT/'MANIFEST.json',provenance/'MANIFEST.json')
roles=['complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py']
for fn in roles:shutil.copy2(PARENT/fn,provenance/fn)

old=(PARENT/roles[0]).read_text();t=namespace(old)
t=replace_once(t,'import hashlib\n','import hashlib\nimport base64\nimport traceback\n')
t=replace_once(t,'def joint_bytes(roots,lsof_tool,ps_tool):','def joint_bytes(roots,lsof_tool,ps_tool,monitor=None):')
joint=definition(t,'joint_bytes');head,body=joint.split('\n',1)
joint_new=head+'\n    try:\n'+''.join('    '+line for line in body.splitlines(True))+'''    except BaseException as error:
        if monitor is not None:
            try:monitor.joint_failure(locals(),error)
            except BaseException as recording_error:monitor.recording_errors.append(monitor_error(recording_error))
        raise
'''
t=replace_once(t,joint,joint_new)
guarded=definition(t,'guarded');head,body=guarded.split('\n',1)
guarded_new=head+'''\n    monitor=getattr(resources,'_failure_only_monitor',None)
    previous_deadline=None if monitor is None else monitor.stage_deadline
    if monitor is not None:monitor.stage_deadline=deadline
    try:
'''+''.join('    '+line for line in body.splitlines(True))+'''    finally:
        if monitor is not None:monitor.stage_deadline=previous_deadline
'''
t=replace_once(t,guarded,guarded_new)
t=replace_once(t,'def run(host_module,support,b,author,started):',MONITOR_SOURCE+'\ndef run(host_module,support,b,author,started):')
t=replace_once(t,'    class JointHistoryResources(resource.DynamicHistoryResources):','    monitor=None\n    class JointHistoryResources(resource.DynamicHistoryResources):')
t=replace_once(t,"joint=joint_bytes(roots5,b['tool_pins']['lsof']['path'],b['tool_pins']['ps']['path']);", "joint=joint_bytes(roots5,b['tool_pins']['lsof']['path'],b['tool_pins']['ps']['path'],monitor);")
t=replace_once(t,'            value.update(joint);return value','            if monitor is not None:monitor.latest_joint=dict(joint)\n            value.update(joint);return value')
t=replace_once(t,';runner=None\n    def budget()', ';runner=None\n    monitor=FailureOnlyMonitorEvidence(roots5,b[\'tool_pins\'],started,resources,resource.DynamicHistoryResources.check,dfreeze,efreeze)\n    resources._failure_only_monitor=monitor\n    def budget()')
t=replace_once(t,"        require(all(runner.env.get(k)=='1'for k in THREAD_KEYS)","        monitor.install_bounded_wrappers(runner)\n        require(all(runner.env.get(k)=='1'for k in THREAD_KEYS)")
t=replace_once(t,"actual_Root_observed_terminal=None,**FUTURE)\n        write_new(host/'result.json'", "actual_Root_observed_terminal=None,actual_failure_only_monitor_evidence=monitor.summary(),**FUTURE)\n        write_new(host/'result.json'")
t=replace_once(t,"original_caps=CAPS,actual_Root_observed_terminal=None,**FUTURE))\n        raise", "original_caps=CAPS,actual_Root_observed_terminal=None,actual_failure_only_monitor_evidence=monitor.summary(include_unpersisted=True),**FUTURE))\n        raise\n    finally:\n        monitor.restore_bounded_objects()")
(P/roles[0]).write_text(t)
for fn in roles[1:]:
    t=namespace((PARENT/fn).read_text())
    if 'postclose' in fn:
        anchor="    require(t['exit_code']==0,'actual success coverage requires Root typed zero, nonzero is retained failure only')"
        addition="""    diagnostic=h['actual_failure_only_monitor_evidence']
    require(diagnostic['schema']=='ACTUAL_N7_FAILURE_ONLY_MONITOR_SUMMARY_V1'and type(diagnostic['failure_event_count'])is int and diagnostic['failure_event_count']==0 and diagnostic['journal_pin']is None and diagnostic['additional_recording_errors']==[] and diagnostic['unpersisted_complete_events']==[],'actual successful instrumented host has no hidden monitor/cleanup failure or recording error')
    require(diagnostic['original_PS_lsof_argv_timeout_and_PID_parent_chain_unchanged']is True and diagnostic['original_bounded_Source_bytes_and_supervisor_classes_unchanged']is True and diagnostic['original_watchdog_cleanup_flag_not_actual_cleanup_proof']is True and diagnostic['new_instrumented_runtime_controls_actual']is None and diagnostic['new_native_runtime_qualification']is None and diagnostic['original_caps']==CAPS,'failure-only diagnostic scope does not qualify guard/native/science or treat legacy cleanup flag as proof')
"""
        t=replace_once(t,anchor,addition+anchor)
    (P/fn).write_text(t)

actual_dir=P/'ACTUAL_N6_FAILED_MONITOR_SMALL_META_PROVENANCE';actual_dir.mkdir()
summary=BASE/'Root_actual_N6_failed_native_observation_current_summary.json';j=json.loads(summary.read_bytes())
actual_paths=[summary]+[Path(j[k]['path'])for k in ['actual_failed_host_result_pin','actual_Root_tool_terminal_pin','actual_first_compiler_watchdog_pin','later_actual_liveness_diagnostic_pin','later_actual_liveness_tool_terminal_pin']]
actual_paths += [BASE/'actual_complete_native_observation_BUILD5_AB_v6_sources'/x for x in ['Root_bound_complete_observation_runtime.py','Root_bound_complete_observation_genuine_host.py','Root_actual_observation_SOURCE_binding.json','Root_actual_observation_bound_Source_full_inverse.json']]
actual_provenance=[]
for q in actual_paths:
    assert q.stat().st_size<1000000
    source=pin(q);dest=actual_dir/q.name;shutil.copy2(q,dest);assert dest.read_bytes()==q.read_bytes()
    actual_provenance.append(dict(actual_original_fullpin=source,complete_byte_copy_fullpin=pin(dest)))
write(P/'N7_ACTUAL_N6_FAILED_MONITOR_AND_SOURCE_PROVENANCE.json',dict(source_only=True,actual_original_files=actual_provenance,
    original_N6_failed_lsof_raw=None,old_failure_not_repaired=True,actual_N6_compile_return_zero_not_guard_qualified=True,
    actual_N6_cleanup_success_unproved=True,later_absence_is_a_different_actual_observation=True))

inverse=[]
for fn in roles:
    a=(PARENT/fn).read_text();b=(P/fn).read_text();ops=[]
    for tag,i,j,k,l in difflib.SequenceMatcher(None,a.splitlines(True),b.splitlines(True),autojunk=False).get_opcodes():
        if tag!='equal':ops.append(dict(old_start_line0=i,old_end_line0=j,new_start_line0=k,new_end_line0=l,old_text=''.join(a.splitlines(True)[i:j]),new_text=''.join(b.splitlines(True)[k:l])))
    restored=b.splitlines(True)
    for row in reversed(ops):
        assert ''.join(restored[row['new_start_line0']:row['new_end_line0']])==row['new_text']
        restored[row['new_start_line0']:row['new_end_line0']]=row['old_text'].splitlines(True)
    assert ''.join(restored)==a
    assert ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(a),include_attributes=False)
    inverse.append(dict(role_basename=fn,parent_original_fullpin=pin(PARENT/fn),new_complete_Source_pin=pin(P/fn),hunks=ops,whole_byte_inverse_equals_parent=True,whole_AST_inverse_equals_parent=True))
write(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json',dict(schema='COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_SOURCE_INVERSE_V1',source_only=True,coordinates='zero_based_half_open_lines',roles=inverse,new_physics_or_business_child=False,new_original_PS_or_lsof_command=False,no_accepted_lsof_failure=True))

namespaces=next(ast.literal_eval(n.value)for n in ast.parse((P/roles[0]).read_text()).body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id=='REQUIRED_N7_FRESH_NAMESPACES'for x in n.targets))
write(P/'N7_FAILURE_ONLY_MONITOR_FUTURE_ROOT_INTERFACE.UNREADY.json',dict(schema='N7_FAILURE_ONLY_MONITOR_FUTURE_ROOT_SOURCE_INTERFACE_V1',source_only=True,
    namespaces=namespaces,complete_scope='original129 + complete actual additional inputs; all14 author roles;1365 Source,4 libraries+link,A then B',
    actual_Source_independent_review=None,actual_Root_N7_Source_admission=None,actual_Root_N7_Source_admission_tool_terminal=None,
    actual_request=None,actual_bound_Source=None,actual_bound_Source_independent_review=None,actual_HOCDE_frozen_Source=None,
    actual_N7_runtime_terminal=None,actual_instrumented_guard_controls=None,actual_N7_native_Source_binary_linkage=None,
    actual_N7_A_B_observations=None,actual_N7_storage_and_ownchild_RSS=None,actual_N7_scientific_qualification=None,
    original_N6_lsof_raw=None,original_N6_failure_cause_unknown=True,Root_alone_executes_business=True,
    no_business_retry=True,no_blanket_nonzero_lsof_acceptance=True,no_live_business_PID_exclusion=True,
    no_diagnostic_budget_extension=True,no_successful_scan_raw_history=True,
    diagnostic_failure_raw_liveness_and_cleanup_evidence_only=True,old_N6_admission_cannot_admit_N7=True))
(P/'N7_ROOT_NEXT_STEPS_SOURCE_ONLY.txt').write_text('''N7 is UNREADY Source instrumentation only. N6 original lsof raw/cause remain unknown.
1. Independent Source review this whole new manifest and exact14 roles/full four-role inverse. Root retain actual Source review/seal/postseal; no new runtime qualification.
2. Root fresh N7 Source admission must bind this manifest/roles and new independent report, original nine CAPS/FUTURE. N6 admission cannot admit N7.
3. Root Source/META request uses Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py with actual peer/admission/typed CLOSED0 admission receipt, exact six original canonical tools, all five fixed v7 namespaces and fresh request output. Original129 and all added Source/tool/library evidence remain protected.
4. Root Source-only binder uses --source-manifest-sha256 <new MF> --request <new request> --request-sha256 <new SHA> --output-source-dir <fixed v7 D>. Independent actual bound Source review, then freeze complete D/E. No native action here.
5. Root alone runs bound genuine host once, serial after other numeric work, original env/monitor permission and all9 original caps. Full1365 four-library compile+link; shared two original libraries once; all7 seed roles, original/derived c2m and A closure before B remain.
Failure instrumentation saves original failed joint PS/lsof text=True strings exactly, actual returncodes/selected PID parent-chain, original guard exception and actual cleanup exception; extra PS pid/ppid/pgid only after failure. Original scans and all strict gates still raise. Wrappers capture original bounded callables before delegation; no class/MRO/guard Source modification. Successful scans never append their raw outputs. Every failure journal byte belongs to H and original full HOCDE/history/free caps; elapsed time is counted in original whole/stage caps. Failed lsof means current open-unlinked measurement unverified, never replaced by stale/regular-only passing evidence. Any recording/query limitation is explicit, never inferred zero/memory/cleanup. No additional time/disk budget or business retry.
6. After genuine Root CLOSED, save exact Root terminal first in H before E freeze. If EXIT1, Root saves actual complete failure namespace META and journal evidence, no success writer. If EXIT0, original complete postclose writer additionally requires diagnostic failure_event_count exact0/no journal/no recording errors; fullHOCDE byte views count all files. A zero result still does not qualify new instrumented guard/native bits/aggregation/science.
New instrumented original-controls execution is not yet performed and remains None. No Source check forecasts 2GiB,512MiB,material data or scientific PASS. Do not clean original files or reuse old H/O/C/D/E.
''')

shutil.copy2(Path(__file__),P/'AUTHOR_CREATE_N7_SOURCE_ONLY.py')
write(P/'AUTHOR_N7_SOURCE_CREATION_LOCATION.json',dict(source_only=True,private_TMP_output=str(P),original_sealed_N6_manifest_pin=pin(PARENT/'MANIFEST.json'),all_project_and_original_packages_read_only=True))
print(json.dumps(dict(source_only=True,created_private_TMP=str(P),original_parent_manifest_pin=pin(PARENT/'MANIFEST.json'),changed_role_Source_pins={fn:pin(P/fn)for fn in roles},all_other_parent_members_complete_copied=True,new_namespace=namespaces,candidate_or_helper_or_guard_or_API_or_native_executed=False),allow_nan=False))
