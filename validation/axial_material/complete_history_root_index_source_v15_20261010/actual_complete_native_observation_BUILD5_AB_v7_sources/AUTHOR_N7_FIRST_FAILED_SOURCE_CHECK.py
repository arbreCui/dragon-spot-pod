from pathlib import Path
import ast,hashlib,json,shutil,stat,tarfile
P=Path('/private/tmp/axmat_complete_native_observation_N7_failure_only_monitor_UNREADY_Source_piquf6v6')
N=Path('/private/tmp/axmat_complete_native_observation_N6_shared_original_libraries_UNREADY_Source_p8u1h6xc')
checks=[]
def check(label,value):
 assert type(value)is bool,(label,type(value));checks.append(dict(check=label,passed=value));assert value,label
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 s=p.lstat();check_local=stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not p.is_symlink();assert check_local
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 assert identity(s)==identity(p.lstat());return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s))
def dump(n):return ast.dump(n,include_attributes=False)
def defs(t):return {n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
def globals_(t):
 return {x.id:n.value for n in t.body if isinstance(n,ast.Assign)for x in n.targets if isinstance(x,ast.Name)}
def unnamespace(t):return t.replace('REQUIRED_N7_FRESH_NAMESPACES','REQUIRED_N6_FRESH_NAMESPACES').replace('-AB-v7-','-AB-v6-').replace('_AB_v7_','_AB_v6_').replace('fixed v7','fixed v6').replace('new fixed v7','new fixed v6')
mf=json.loads((N/'MANIFEST.json').read_bytes());oldpins={r['relative_path']:pin(N/r['relative_path'])for r in mf['members']};startmf=pin(N/'MANIFEST.json')
check('original N6 complete manifest expected SHA',startmf['sha256']=='6b743dbb801efa359929b5c2bd409b337fdaf65d417a8e08debaeb917eba392f')
check('all152 parent members full EOF7ID match original frozen manifest',all(oldpins[r['relative_path']]==r['fullpin']for r in mf['members']))
check('parent full member set has no omitted file',{str(p.relative_to(N))for p in N.rglob('*')if p.is_file()}==set(oldpins)|{'MANIFEST.json'})
ledger=json.loads((P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json').read_bytes());changed={r['role_basename']for r in ledger['roles']}
check('only four complete current role files differ from N6',changed=={'complete_observation_BUILD5_AB_runtime.UNREADY.py','Root_prepare_observation_REQUEST.Source_META_only.UNREADY.py','bind_complete_observation_SOURCE_only.UNREADY.py','Root_observation_postclose_META_writer.UNREADY.py'})
check('all148 other parent members exact complete bytes SHA size',all((P/fn).read_bytes()==(N/fn).read_bytes()for fn in oldpins if fn not in changed))
check('original N6 manifest complete byte copy preserved',(P/'PREVIOUS_SEALED_N6_SOURCE_PROVENANCE/MANIFEST.json').read_bytes()==(N/'MANIFEST.json').read_bytes())
allasts={}
for q in sorted(P.rglob('*.py')):allasts[str(q.relative_to(P))]=ast.parse(q.read_text())
check('all complete Python Source parse by AST only',len(allasts)>0)
for row in ledger['roles']:
 fn=row['role_basename'];old=(N/fn).read_text();new=(P/fn).read_text();lines=new.splitlines(True)
 check(fn+' new fullpin agrees with actual full EOF7ID',pin(P/fn)==row['new_complete_Source_pin'])
 for h in reversed(row['hunks']):
  assert ''.join(lines[h['new_start_line0']:h['new_end_line0']])==h['new_text']
  lines[h['new_start_line0']:h['new_end_line0']]=h['old_text'].splitlines(True)
 check(fn+' complete inverse recovers whole parent bytes',''.join(lines)==old)
 check(fn+' complete inverse recovers whole parent AST',dump(ast.parse(''.join(lines)))==dump(ast.parse(old)))
 check(fn+' full original role retained',(P/'PREVIOUS_SEALED_N6_SOURCE_PROVENANCE'/fn).read_bytes()==(N/fn).read_bytes())
 oldtree=ast.parse(old);newtree=ast.parse(new);og=globals_(oldtree);ng=globals_(newtree)
 check(fn+' exact original CAPS and FUTURE Source AST',all(dump(og[k])==dump(ng[k])for k in ['CAPS','FUTURE']))
 check(fn+' OS tool allowlist/pin helpers unchanged',all(dump(defs(oldtree)[k])==dump(defs(newtree)[k])for k in ['source_tool_nlink_allowed']if k in defs(oldtree)))
 if 'request'in fn or 'bind_'in fn:
  check(fn+' body changes only namespace literals',unnamespace(new)==old)
runtime=P/'complete_observation_BUILD5_AB_runtime.UNREADY.py';rt=runtime.read_text();oldrt=(N/runtime.name).read_text();at=ast.parse(rt);ot=ast.parse(oldrt);nd=defs(at);od=defs(ot)
check('runtime original noninstrumented definitions complete byte AST',all(dump(od[k])==dump(nd[k])for k in od if k not in ['joint_bytes','guarded','run','validate_request']))
check('runtime validate_request only fresh namespace literals',dump(defs(ast.parse(unnamespace(rt)))['validate_request'])==dump(od['validate_request']))
check('runtime remains UNREADY Source gate',ast.literal_eval(globals_(at)['SOURCE_STATUS'])=='UNREADY_SOURCE_ONLY')
check('genuine host full bytes unchanged',(P/'complete_observation_genuine_host.UNREADY.py').read_bytes()==(N/'complete_observation_genuine_host.UNREADY.py').read_bytes())
hostg=globals_(allasts['complete_observation_genuine_host.UNREADY.py'])
check('host target/binding/Source admission and namespaces still None',all(isinstance(hostg[k],ast.Constant)and hostg[k].value is None for k in ['SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA']))
jn=nd['joint_bytes'];jo=od['joint_bytes'];original=jn.body[1].body[:-2]
check('joint wrapper complete original body AST and return preserved',len(jn.body)==2 and isinstance(jn.body[1],ast.Try)and len(jn.body[1].handlers)==1 and dump(ast.Module(body=[*original,jn.body[1].body[-1]],type_ignores=[]))==dump(ast.Module(body=jo.body,type_ignores=[])))
check('joint wrapper exception path bare re-raises',isinstance(jn.body[1].handlers[0].body[-1],ast.Raise)and jn.body[1].handlers[0].body[-1].exc is None)
check('joint original PS two columns and lsof fullargv retained',"ps_argv=[ps_tool,'-axo','pid=,ppid=']"in rt and "subprocess.run([lsof_tool,'-nP','-F','pfnsiDt','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)"in rt)
check('joint original strict lsof0/8MiB gates intact',"require(observed.returncode==0,'full live own process file scan required')"in rt and "require(len(observed.stdout)<8*2**20,'finite complete lsof output; never truncated')"in rt)
check('joint parent-chain selected closure and only reaped diagnostic discard intact',"selected.discard(ps_diagnostic_pid)"in rt and "new={p for p,parent in parents.items()if parent in selected};expanded=selected|new"in rt)
gn=nd['guarded'];go=od['guarded']
check('guarded original full body/gates/order unchanged inside try',dump(ast.Module(body=gn.body[-1].body,type_ignores=[]))==dump(ast.Module(body=go.body,type_ignores=[])))
check('guarded restores prior original stage deadline in finally',bool(gn.body[-1].finalbody))
mon=nd['FailureOnlyMonitorEvidence'];methods={n.name:n for n in mon.body if isinstance(n,ast.FunctionDef)}
check('monitor only caches one successful raw scan in memory','self.latest_original_scan=dict('in rt and "not_new_liveness_at_cleanup_time=True"in rt and 'remember_successful_scan' in methods)
check('monitor event writing only failure paths and no raw success append',not any(isinstance(x,ast.Call)and isinstance(x.func,ast.Attribute)and x.func.attr=='record'for x in ast.walk(methods['remember_successful_scan'])))
install=methods['install_bounded_wrappers'];it=''.join(rt.splitlines(True)[install.lineno-1:install.end_lineno])
check('both bounded objects captured before assigning wrappers',it.index('original_terminate_group=bounded.terminate_group')<it.index('bounded.terminate_group=terminate_group')and it.index('original_finish_liveness_watchdog=bounded.finish_liveness_watchdog')<it.index('bounded.finish_liveness_watchdog=finish_liveness_watchdog'))
check('terminate delegates unchanged original single call args','try:return original_terminate_group(process)'in it)
check('finish delegates unchanged original single call args','try:return original_finish_liveness_watchdog(write_fd,watchdog)'in it)
check('cleanup wrappers both bare re-raise original exceptions',len([n for n in ast.walk(install)if isinstance(n,ast.Raise)and n.exc is None])==2)
check('cleanup observations do not poll or change process reaping',not any(isinstance(x,ast.Call)and isinstance(x.func,ast.Attribute)and x.func.attr in ['poll','wait','kill','terminate','send_signal']for x in ast.walk(install)))
check('normal successful finish/terminate emits no new diagnostic query','if active is not None:'in it and 'if active is not None or cleanup_error is not None:'in it)
check('original guard and cleanup exceptions both explicit separate fields','original_active_exception' in it and 'actual_cleanup_exception' in it)
check('additional PGID scan only failure method original selected unaffected',"argv=[self.tools['ps']['path'],'-axo','pid=,ppid=,pgid=']"in rt and 'used_to_accept_original_failure=False' in rt and 'original_selection_not_changed=True' in rt)
check('additional failure query original remaining clocks and <=2seconds','timeout=min(2,remaining)'in rt and "require(remaining>0,'no additional diagnostic query after original whole/stage deadline')"in rt)
check('original failed raw commits before added failure PS query',rt.index("self.record(dict(event='original_joint_bytes_failure'")<rt.index("self.failure_ps('after_original_failed_joint_scan')"))
check('complete original text strings retained without strip/truncate','actual_stdout=monitor_stream(lsof_stdout)'in rt and 'actual_stderr=monitor_stream(lsof_stderr)'in rt and 'streams_complete=observed is not None'in rt and 'no_strip_or_stream_truncation=True'in rt)
check('timeout actual partial bytes preserved by base64 original type','original_type=\'bytes\''in rt and 'base64.b64encode(value)'in rt and 'streams_complete=False'in rt)
check('all diagnostics H-only and no D/E append',"target=folder/'ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'"in rt and "tree(self.roots[3])==self.dfreeze and tree(self.roots[4])==self.efreeze"in rt)
check('diagnostic file counts original joint/history/free exactly','total+previous_unlinked+increment<CAPS[\'joint_archive_bytes\']'in rt and "history['artifact_bytes']+external+previous_unlinked+increment<=CAPS['history_bytes']"in rt and "history['disk_free_bytes']-increment>=CAPS['free_floor_bytes']"in rt)
check('failed lsof never regular-only or stale passing substitute','current_open_unlinked_verified=False'in rt and 'failed_scan_never_replaced_by_this_account=True'in rt)
check('complete augmented failure result same caps no truncation','raw=(json.dumps(value,indent=2,allow_nan=False)'in rt and 'self.disk_account(len(raw))'in rt and 'complete_original_failure_result_retained_in_memory_only=True'in rt)
check('original two bounded callable objects restored in run finally','monitor.restore_bounded_objects()'in rt and "bounded.terminate_group=original_terminate_group"in rt and "bounded.finish_liveness_watchdog=original_finish_liveness_watchdog"in rt)
check('original class/MRO admission checks remain full',"full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)"in rt and "type(runner)is full.OwnRSSSerialExecutor"in rt)
post=(P/'Root_observation_postclose_META_writer.UNREADY.py').read_text()
check('success postclose rejects hidden monitor or cleanup failures',"type(diagnostic['failure_event_count'])is int and diagnostic['failure_event_count']==0"in post and "diagnostic['journal_pin']is None"in post and "diagnostic['additional_recording_errors']==[]"in post and "diagnostic['unpersisted_complete_events']==[]"in post)
check('legacy cleanup flag not certified by new summary or postclose',"original_watchdog_cleanup_flag_not_actual_cleanup_proof=True"in rt and "diagnostic['original_watchdog_cleanup_flag_not_actual_cleanup_proof']is True"in post)
check('instrumented runtime controls/native qualification remain None',"new_instrumented_runtime_controls_actual=None,new_native_runtime_qualification=None"in rt)
check('old N6 raw remains unknown in new evidence',"N6_original_failed_lsof_raw_remains_unknown=True"in rt and json.loads((P/'N7_ACTUAL_N6_FAILED_MONITOR_AND_SOURCE_PROVENANCE.json').read_bytes())['original_N6_failed_lsof_raw']is None)
provenance=json.loads((P/'N7_ACTUAL_N6_FAILED_MONITOR_AND_SOURCE_PROVENANCE.json').read_bytes())
check('actual N6 failure smallMETA+bound Source copies all full EOF7ID beforeafter',all(pin(Path(r['actual_original_fullpin']['path']))==r['actual_original_fullpin']and pin(Path(r['complete_byte_copy_fullpin']['path']))==r['complete_byte_copy_fullpin']and Path(r['actual_original_fullpin']['path']).read_bytes()==Path(r['complete_byte_copy_fullpin']['path']).read_bytes()for r in provenance['actual_original_files']))
index=json.loads((P/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());byname={x['relative_path']:x for x in index['members']};archivebefore=pin(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz')
with tarfile.open(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as tar:
 members=tar.getmembers();complete=True
 assert len(members)==len(byname)==1365
 for m in members:
  assert m.isfile()and m.name in byname and not Path(m.name).is_absolute()and '..'not in Path(m.name).parts
  h=hashlib.sha256();size=0
  with tar.extractfile(m)as f:
   for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk);size+=len(chunk)
  ep=byname[m.name]['full_original_Source_pin'];complete=complete and size==m.size==ep['size_bytes']and h.hexdigest()==ep['sha256']
check('whole1365 four-library compile Source archive all members EOF SHA size',complete and {m.name for m in members}==set(byname))
check('complete archive full EOF7ID unchanged after Source-only tar read',archivebefore==pin(P/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz'))
check('all original physical14/host12 inverse and shared-library contracts byteexact',all((P/x).read_bytes()==(N/x).read_bytes()for x in ['COMPLETE_FOUR_ORIGINAL_PHYSICAL_ROUTINE_OBSERVER_INSERT_ONLY_INVERSE.json','COMPLETE_ORIGINAL_NATIVE_HOST_TO_OBSERVATION_HOST_FULL_INVERSE.json','COMPLETE_N6_FOUR_ROLE_WHOLE_BYTE_AST_SOURCE_INVERSE.json','ORIGINAL129_AND_MATERIAL_SEED_CONTRACT.Source_META.json']))
check('N6 all7 seed/shared/c2m Source paths unchanged full definitions',all(dump(od[k])==dump(nd[k])for k in ['original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_shared_library_procedure','copy_state_seeds','collect_state']))
check('future namespace metadata None and no new science claim',all(v is None for k,v in json.loads((P/'N7_FAILURE_ONLY_MONITOR_FUTURE_ROOT_INTERFACE.UNREADY.json').read_bytes()).items()if k.startswith('actual_')))
check('all check labels unique positive count and exact typed true',len(checks)>0 and len({c['check']for c in checks})==len(checks)and all(type(c['passed'])is bool and c['passed']for c in checks))
check('parent all Source members7ID unchanged after review',oldpins=={r['relative_path']:pin(N/r['relative_path'])for r in mf['members']}and startmf==pin(N/'MANIFEST.json'))
shutil.copy2(Path(__file__),P/'AUTHOR_EXECUTED_N7_COMPLETE_SOURCE_CHECK.py')
report=dict(schema='AUTHOR_COMPLETE_N7_FAILURE_ONLY_MONITOR_SOURCE_CHECK_V1',status='AUTHOR_SOURCE_ONLY_CHECKED_NOT_INDEPENDENT_OR_RUNTIME_QUALIFIED',source_only=True,check_count=len(checks),all_checks_typed_true=True,checks=checks,blockers=[],Python_AST_file_count=len(allasts),whole_original_native_Source_archive_members=1365,original_N6_complete_members=152,complete_N7_changed_role_pins={r['role_basename']:pin(P/r['role_basename'])for r in ledger['roles']},full_Source_inverse_pin=pin(P/'COMPLETE_N7_FOUR_ROLE_MONITOR_NAMESPACE_BYTE_AST_INVERSE.json'),original_N6_manifest_pin=startmf,original_caps_ast_unchanged=True,actual_instrumented_runtime_controls=None,actual_N7_runtime_terminal=None,actual_native_A_B_observations=None,actual_scientific_qualification=None,candidate_or_helper_or_guard_or_API_or_native_or_material_executed=False)
(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,status=report['status'],check_count=len(checks),all_checks_typed_true=True,blockers=[],report_pin=pin(P/'AUTHOR_N7_COMPLETE_SOURCE_ONLY_REPORT.json'),candidate_or_helper_or_guard_or_API_or_native_or_material_executed=False),allow_nan=False))
