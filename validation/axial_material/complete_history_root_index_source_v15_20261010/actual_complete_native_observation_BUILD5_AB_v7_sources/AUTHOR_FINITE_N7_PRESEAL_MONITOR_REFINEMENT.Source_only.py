from pathlib import Path
import ast,difflib,hashlib,json,shutil,stat
P=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
N=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
def once(t,a,b):assert t.count(a)==1,(a,t.count(a));return t.replace(a,b,1)
def pin(p):
 s=p.lstat();b=p.read_bytes();a=p.lstat();assert(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==(a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns)
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
q=P/'complete_observation_BUILD5_AB_runtime.UNREADY.py';t=q.read_text()
t=once(t,'def joint_bytes(roots,lsof_tool,ps_tool,monitor=None):\n    try:', 'def joint_bytes(roots,lsof_tool,ps_tool,monitor=None):\n    monitor_scan_started=None if monitor is None else time.monotonic()\n    try:')
t=once(t,'        return dict(complete_joint_HOCDE_bytes=total,','        if monitor is not None:monitor.remember_successful_scan(locals())\n        return dict(complete_joint_HOCDE_bytes=total,')
t=once(t,'self.latest_joint=None;self.latest_failed_selection=[];self.events=0','self.latest_joint=None;self.latest_original_scan=None;self.latest_failed_selection=[];self.events=0')
t=once(t,'    def record(self,event):\n        self.events+=1','    def record(self,event):\n        appended=False\n        self.events+=1')
t=once(t,'            self.journal=target;self.disk_account(0)','            appended=True;self.journal=target;self.disk_account(0)')
t=once(t,'            self.unpersisted.append(event);self.recording_errors.append(monitor_error(error))','            if not appended:self.unpersisted.append(event)\n            self.recording_errors.append(dict(actual_record_appended=appended,recording_error=monitor_error(error)))')
new='''    def remember_successful_scan(self,frame):
        # One current observation in memory only. Replacement releases the
        # previous complete streams; no accumulated successful scan history.
        observed=frame['observed']
        self.latest_original_scan=dict(original_scan_started_monotonic=frame['monitor_scan_started'],
            original_scan_finished_monotonic=time.monotonic(),original_PS_argv=frame['ps_argv'],
            original_PS_PID=frame['ps_diagnostic_pid'],original_PS_returncode=frame['ps_returncode'],
            original_PS_stdout=frame['ps_stdout'],original_PS_stderr=frame['ps_stderr'],
            original_selected_PIDs=sorted(frame['selected']),original_lsof_argv=observed.args,
            original_lsof_returncode=observed.returncode,original_lsof_stdout=observed.stdout,
            original_lsof_stderr=observed.stderr,not_new_liveness_at_cleanup_time=True)
    def write_failure_result(self,path,value):
        # The complete original failure result and all added diagnostic bytes
        # are subject to the same disk caps. No partial result is substituted.
        raw=(json.dumps(value,indent=2,allow_nan=False)+'\\n').encode('utf-8')
        try:self.disk_account(len(raw))
        except BaseException as error:
            self.recording_errors.append(dict(failure_result_not_written=True,actual_recording_error=monitor_error(error)))
            print(json.dumps(dict(status='FAILED_DIAGNOSTIC_RESULT_NOT_WRITTEN_OR_QUALIFIED',
                actual_failure_result_write_error=monitor_error(error),complete_original_failure_result_retained_in_memory_only=True,
                new_instrumented_runtime_qualification=None),allow_nan=False),file=sys.stderr,flush=True)
            return
        try:
            write_new(path,value);self.disk_account(0)
        except BaseException as error:
            self.recording_errors.append(dict(actual_failure_result_write_error=monitor_error(error)))
            print(json.dumps(dict(status='FAILED_DIAGNOSTIC_RESULT_WRITE_OR_POSTWRITE_ACCOUNT_ERROR',
                actual_failure_result_write_error=monitor_error(error),new_instrumented_runtime_qualification=None),allow_nan=False),file=sys.stderr,flush=True)
        # Both cases leave the original exception pending in the caller.
'''
t=once(t,'    def joint_failure(self,frame,error):',new+'    def joint_failure(self,frame,error):')
t=once(t,"self.record(dict(event='original_joint_bytes_failure',original_error=monitor_error(error),", "self.record(dict(event='original_joint_bytes_failure',original_error=monitor_error(error),\n            original_scan_started_monotonic=frame.get('monitor_scan_started'),\n            latest_prior_successful_original_scan=self.latest_original_scan,")
t=once(t,'actual_business_PID=process.pid,cached_business_returncode=process.returncode,','actual_business_PID=process.pid,cached_business_returncode=process.returncode,\n                    latest_prior_successful_original_scan=self.latest_original_scan,')
t=once(t,'cached_watchdog_returncode=watchdog.returncode,cleanup_success_not_inferred=True))\n                self.failure_ps(\'before_', 'cached_watchdog_returncode=watchdog.returncode,latest_prior_successful_original_scan=self.latest_original_scan,cleanup_success_not_inferred=True))\n                self.failure_ps(\'before_')
t=once(t,"            write_new(host/'failed_host_result.json',dict(","            monitor.write_failure_result(host/'failed_host_result.json',dict(")
ast.parse(t);q.write_text(t)
shutil.copy2(Path(__file__),P/'AUTHOR_FINITE_N7_PRESEAL_MONITOR_REFINEMENT.Source_only.py')
ledger=json.loads((P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json').read_bytes())
for r in ledger['roles']:
 fn=r['role_basename'];a=(N/fn).read_text();b=(P/fn).read_text();h=[]
 for tag,i,j,k,l in difflib.SequenceMatcher(None,a.splitlines(True),b.splitlines(True),autojunk=False).get_opcodes():
  if tag!='equal':h.append(dict(old_start_line0=i,old_end_line0=j,new_start_line0=k,new_end_line0=l,old_text=''.join(a.splitlines(True)[i:j]),new_text=''.join(b.splitlines(True)[k:l])))
 restored=b.splitlines(True)
 for x in reversed(h):
  assert ''.join(restored[x['new_start_line0']:x['new_end_line0']])==x['new_text'];restored[x['new_start_line0']:x['new_end_line0']]=x['old_text'].splitlines(True)
 assert ''.join(restored)==a
 assert ast.dump(ast.parse(''.join(restored)),include_attributes=False)==ast.dump(ast.parse(a),include_attributes=False)
 r['hunks']=h;r['new_complete_Source_pin']=pin(P/fn)
(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json').write_text(json.dumps(ledger,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,full_Source_refinement_written=pin(q),whole_inverse_pin=pin(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json'),candidate_or_API_or_guard_or_material_executed=False),allow_nan=False))
