"""Independent public7 Source review only. No candidate import/body execution/syscalls."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'public_read_compact_bq_admission_control_host_source_v7_20261014'
OUT=R/'independent_public7_completed_SRC_bundle_lifecycle_Source_review_20261014'
checks=[];observed={}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def check(name,condition):
 if not condition:raise AssertionError(name)
 checks.append(name)
def pin(path):
 p=Path(path);before=ids(p.lstat());check('ordinary metadata Source '+str(p),stat.S_ISREG(before[2]));fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:assert ids(os.fstat(f.fileno()))==before;raw=f.read();assert ids(os.fstat(f.fileno()))==before
 assert ids(p.lstat())==before;pf=dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before);observed[str(p)]=(pf,raw);return pf,raw
def read(p):pf,raw=pin(p);return json.loads(raw),pf
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def bound(p):pf,raw=pin(p['path']);check('exact declared PF '+p['path'],pf==norm(p));return raw
def write(name,d):
 p=OUT/name;raw=(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)[0]
check('unique independent review namespace absent',not OUT.exists())
ready,rpf=read(P/'HOST_SOURCE_REVIEW_READY.json');plan,ppf=read(P/'EXACT_CONTROL_HOST_SOURCE_ONLY_PLAN.json');life,lpf=read(P/'EXACT_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN.json')
hostpf,raw=pin(P/'run_guarded_public_controls.py');text=raw.decode();tree=ast.parse(text);functions={n.name:ast.get_source_segment(text,n)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
check('exact current public7 Host SHA/size',hostpf['sha256']=='b5585624107b4e6b8fc027621d52ba868295b9140cca0c7f943c616e3f41512a'and hostpf['size_bytes']==35510)
check('READY exact Host/PLAN/Lifetime pins',ready['host_source']==hostpf and ready['control_host_plan_pin']==ppf and ready['lifetime_Source_plan_pin']==lpf)
check('Source only no actual/compiler/numerics/deletion admission',all(ready[k]is False for k in ('compiler_executed','numerical_executed','Host_imported','files_deleted','reader_qualified','AAA_qualified'))and ready['future_Host_freeze_pin']is None and ready['future_actual_public7_report_pin']is None and ready['future_actual_retirement_receipt_pin']is None)
for name,key,changeskey,originalkey in [('COMPLETE_PUBLIC_HOST_V5_TO_V7_LIFETIME_WHOLE_BYTE_DATA_INVERSE.json','complete_Host_plan_inverse_pin','Host_exact_changes','original_Host_pin'),('COMPLETE_PUBLIC_HOST_V6_TO_V7_APFS_INTENT_SYNC_WHOLE_BYTE_INVERSE.json',None,'changes','original_Source_pin')]:
 inverse,ipf=read(P/name)
 if key:check('READY binds v5 whole inverse',ready[key]==ipf)
 orig=bound(inverse[originalkey]);back=text
 for block in reversed(inverse[changeskey]):check('inverse block exact singleton '+block['reason'],back.count(block['after'])==1);back=back.replace(block['after'],block['before'],1)
 check('whole source byte inverse '+name,back.encode()==orig)
 if changeskey=='Host_exact_changes':
  oldtree=ast.parse(orig);oldfunc={n.name:ast.get_source_segment(orig.decode(),n)for n in oldtree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
  check('all original 11 helpers/classes entire Source bytes unchanged',len(inverse['unchanged_11_functions_and_classes'])==11 and all(functions[n]==oldfunc[n]for n in inverse['unchanged_11_functions_and_classes']))
  oldplan=json.loads(bound(inverse['original_plan_pin']));restored=dict(plan)
  for k,v in inverse['exact_original_changed_plan_fields'].items():
   if k in oldplan:restored[k]=v
   else:restored.pop(k)
  check('full original PLAN canonical inverse',restored==oldplan)
  check('PLAN onlyownHost ownOUT exact lifecycle addition',set(inverse['exact_original_changed_plan_fields'])=={'host_source_pin','planned_output_root','completed_first_SRC_bundle_lifetime_Source_plan_pin'})
 else:check('public6 to7 only two corrections plus ownOUT',len(inverse['changes'])==3 and inverse['added_exact_lifecycle_correction_blocks']==2 and inverse['new_ownOUT_literal_changes']==1)
helper=bound(ready['private_retirement_helper_Source_pin']).decode();ast.parse(helper)
check('current exact helper inserted whole bytes in ownHost',helper.rstrip()in text)
check('Host AST only not loaded or functions invoked',True)
fn=functions['retire_completed_first_SRC_bundle'];main=functions['main']
check('exact onlySRC ownv7 oneattempt caller namespace',"cwd!=OUT/'public_read_stale_BQ_SRC' or retirements"in fn and "bundle=cwd/'coherent_complete_context.xsm';sentinel=cwd/'BQ64-SRC-ST';other=cwd/'BQ64-MAC-ST'"in fn)
check('actual prepare/read PASS and exact SRC command/phase eligibility',all(x in fn for x in ["prepare['status']!='PASS' or read_record['status']!='PASS'","prepare['command'][-2:]!=['public_read_stale_BQ_SRC','prepare']","read_record['command'][-2:]!=['public_read_stale_BQ_SRC','read']","('public_read_stale_BQ_SRC','read')"]))
check('strict actual integer read1/control1/baseline0',"[('actual_public_read_status',1),('actual_control_public_read_calls',1),('actual_baseline_public_read_calls',0)]"in fn and 'type(expected.get(key))is not int' in fn)
check('beforeMF actual closedprepare bound exactbundle sentinel and otherabsence',all(x in fn for x in ["c.verify_rows([mf,before,stale])","value['actual_bundle_pin']!=before","value['actual_stale_pin']!=stale","value.get('genuine_prepare_child_closed0')is not True","value['actual_prepare_record']!=prepare","other.exists() or other.is_symlink()"]))
check('full current bundle+sentinel before equals after allPF',"after=c.pin(bundle);after_stale=c.pin(sentinel)"in fn and 'after!=before or after_stale!=stale'in fn)
check('exclusive current owned exactPF1 inode disjoint fixed andotherowned',all(x in fn for x in ["before['identity'][3]!=1","sum(row==before for row in owned)!=1","any(row['identity'][:2]==before['identity'][:2]for row in fixed)","any(row['path']!=before['path']and row['identity'][:2]==before['identity'][:2]for row in owned)"]))
check('owned parent ordinary UID no symlink before write',"not stat.S_ISDIR(parent.st_mode) or cwd.is_symlink() or parent.st_uid!=os.getuid()"in fn)
check('strict APFS intent creation checks devino mode UID +1link +32bytes monotonic',all(x in fn for x in ["parent_before[:3]!=parent_before_intent[:3]","parent_now.st_uid!=uid","parent_before[3]!=parent_before_intent[3]+1","parent_before[4]!=parent_before_intent[4]+32","parent_before[5]<parent_before_intent[5]","parent_before[6]<parent_before_intent[6]"])and 'parent_before[:4]'not in fn)
check('intent file write+fullPF owned before attempt',fn.index('c.write(intent_path,intent)')<fn.index('retirements.append(event)')<fn.index('fd=os.open(cwd'))
check('intent entry sync attempted then returned before strict leaf',fn.index("attempted['intent_parent_fsync_attempted']=True")<fn.index("os.fsync(fd);attempted['intent_parent_fsync_returned']=True")<fn.index('leaf=os.stat(bundle.name'))
check('strict dirfd complete identity UID recheck after intent fsync',"if seven(os.fstat(fd))!=parent_before or os.fstat(fd).st_uid!=uid:"in fn and 'same exact directory after durable intent entry before single unlink'in fn)
check('leaf O_NOFOLLOW via dirfd complete all7 UID nlink and regular',"os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW"in fn and 'follow_symlinks=False'in fn and "seven(leaf)!=before['identity'] or leaf.st_uid!=uid or leaf.st_nlink!=1 or not stat.S_ISREG(leaf.st_mode)"in fn)
check('complete target EOF recheck+immediate leaf same identity before exact singleunlink',fn.count('os.unlink(')==1 and fn.index('c.same_pin(bundle,before)')<fn.index("attempted['unlink_attempted']=True")<fn.index('os.unlink(bundle.name,dir_fd=fd)'))
check('actual unlink return immediate currentPF removal before fsync/check/close',fn.index('os.unlink(bundle.name,dir_fd=fd)')<fn.index("attempted['unlink_returned']=True")<fn.index('owned.remove(before)')<fn.index("attempted['parent_fsync_attempted']=True")<fn.index("os.fsync(fd);attempted['parent_fsync_returned']=True"))
check('truthful absent retiredcount one+before/after historical only',all(x in fn for x in ["attempted['current_bundle_pin']=None;attempted['retired_bundle_historical_only']=True","event['current_bundle_pin']=None","attempted['removed_current_owned_fullpin']=True;attempted['actual_retired_count']=1","except FileNotFoundError:attempted['target_absent_observed']=True"]))
check('operation receipt publication close FirstFailure preservesfirst object+tb',all(x in fn for x in ["local=FirstFailure()","local.capture(error,'exact_retirement_operation')","local.capture(error,'retirement_receipt_publication')","local.capture(error,'retirement_directory_close')","local.reraise()"])and 'self.error=error;self.traceback=error.__traceback__'in functions['FirstFailure']and 'raise self.error.with_traceback(self.traceback)'in functions['FirstFailure'])
check('truthful flags receipt persisted before directoryclose or subsequent check',fn.index('c.write(receipt_path,attempted)')<fn.index('try:os.close(fd)')<fn.index('local.reraise()')<fn.index('c.verify_rows([mf,stale,intent_pin'))
check('receipt pin owned and required before nextMAC onlysuccess',"receipt_pin=c.pin(receipt_path);owned.append(receipt_pin);event['receipt_pin']=receipt_pin"in fn and "if not event['retirement_completed'] or event['receipt_pin']is None:"in fn)
check('old v5 path never unlinktarget and MAC always retained',"OUT=R/'validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7'"in text and "if name=='public_read_stale_BQ_SRC':"in main and "current_bundle_pin=proof['actual_bundle_after_pin']"in main)
check('MACprepare onlyone completeSRCretirement and exactabsence',all(x in main for x in ["if name=='public_read_stale_BQ_MAC'and phase=='prepare':","len(retirements)!=1 or retirements[0]['retirement_completed']is not True","exact first completed SRC bundle retirement before second MAC prepare"]))
check('stage directory exists before original ownrunner construction',main.index("(OUT/('compact-'+KIND+'-controls')).mkdir()")<main.index('runner=full.OwnRSSSerialExecutor'))
check('both stale MF+bundle+sentinel fullPF retained unchanged before read; onlyretired removed',"c.verify_rows([state['manifest_pin'],state['bundle_pin'],state['stale_pin']])"in main and "owned.extend([state['manifest_pin'],bundle_pin,stale_pin])"in main and fn.count('owned.remove(')==1)
check('11guarded commands 9phase 2stale exactly1SRC retirement success',"expected_count=3 if KIND=='model'else 11"in main and "len(actual)!=9 or len(stale)!=2 or len(retirements)!=1 or retirements[0]['retirement_completed']is not True"in main and plan['planned_total_guarded_stages']==11 and len(plan['planned_run_phases'])==9)
check('publication catches and retains firsterror throughconstruction checksrewrite',all(x in main for x in ["except BaseException as error:first.capture(error,'execute_or_oracle')","first.capture(error,'after_check')","summary=None","first.capture(error,'publication')","first.capture(late,'failed_report_publication')","first.reraise()","actual_seven_genuine_public_READ_controls_passed=False"]))
check('original 128MiB auxiliary +8MiB pending caps',"AUX_CAP=128*2**20"in text and "AUX_PENDING=8*2**20"in text and plan['direct_auxiliary_cap_bytes']==134217728 and plan['pending_metadata_bytes']==8388608)
check('ownHost separatelybound HF and inactualfixed not assumed HFdeps',"c.same_pin(__file__,hf['host_source'])"in main and "fixed=unique(fixed+[phf,hf['host_source'],plan_pin"in main)
check('future build/current object/report/output pins remain None',all(v is None for k,v in plan.items()if k.startswith('future_'))and all(v is None for k,v in life.items()if k.startswith('future_')))
check('lifeplan exact current Host/control SF and original caps',plan['host_source_pin']==hostpf and plan['completed_first_SRC_bundle_lifetime_Source_plan_pin']==lpf and life['unchanged_Fortran_Source_pin']==plan['control_Source_pin']and life['unchanged_public_Fortran_Source_freeze_pin']==plan['selected_control_Source_freeze_pin'])
for key in ('control_Source_pin','selected_control_Source_freeze_pin','production_Source_pin','selected_new_build_Host_freeze_pin','selected_new_Fortran_Source_freeze_pin','selected_post_release_Common_Source_freeze_pin','selected_post_release_Common_Source_pin'):bound(plan[key])
bhf=json.loads(observed[plan['selected_new_build_Host_freeze_pin']['path']][1]);check('exact build4 2565 originalclosed dependencies retained',len(bhf['dependencies'])==2565)
for row in bhf['dependencies']:
 check('inherited current7 '+row['path'],ids(Path(row['path']).lstat())==row['identity'])
for row in ready.values():
 if isinstance(row,dict)and{'path','sha256','size_bytes','identity'}<=row.keys():bound(row)
oldfailed=json.loads(observed[ready['actual_failed_public5_summary_pin']['path']][1]);check('failed public5 kept unqualified original128failure',oldfailed['status']=='ACTUAL_CONTROL_FAILED_UNQUALIFIED'and oldfailed['actual_seven_genuine_public_READ_controls_passed']is False and '128MiB'in oldfailed['failure'])
oldbundles=[x for x in oldfailed['output_pins']if Path(x['path']).name=='coherent_complete_context.xsm'];check('bothold public5 100MBbundles stillcurrent7 no deletion',len(oldbundles)==2 and all(x['size_bytes']==100163528 and ids(Path(x['path']).lstat())==x['identity']for x in oldbundles))
for name,key in [('ACTUAL_PUBLIC7_COMPLETED_FIRST_SRC_BUNDLE_LIFETIME_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261014.json','actual_Source_preparation_tool_return'),('ACTUAL_PUBLIC7_V6_TO_V7_APFS_INTENT_SYNC_SOURCE_INVERSE_TRUE_TOOL_RETURNS_20261014.json','actual_corrected_Source_inverse_tool_return')]:
 d,p=read(R/name);closed=d[key];check('genuine closed Source tool '+name,type(closed['exit_code'])is int and closed['exit_code']==0 and closed.get('session_id')is None)
 output=json.loads(closed['output']);declared=output.get('source_review_ready_pin',output.get('whole_inverse_pin',output.get('inverse_pin')))
 if declared:bound(declared)
check('new public7 business OUT absent',not Path(plan['planned_output_root']).exists())
check('no public7 HostHF or CLI freeze exists yet',not(P/'COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json').exists()and not(P/'ROOT_REVIEWABLE_EXACT_CONTROL_ARGV_SOURCE_TEMPLATE.json').exists())
for pf,raw in observed.values():check('all openedmetadata Source finalcurrent7 '+pf['path'],ids(Path(pf['path']).lstat())==pf['identity'])
OUT.mkdir()
report=dict(schema='INDEPENDENT_PUBLIC7_COMPLETED_FIRST_SRC_BUNDLE_LIFECYCLE_SOURCE_ONLY_REVIEW_V1',status='PASS_PUBLIC7_COMPLETED_FIRST_SRC_BUNDLE_LIFECYCLE_SOURCE_ONLY_REVIEW',failure=None,source_only=True,business_executed=False,Host_imported=False,compiled=False,numeric=False,deletion_executed=False,current_host_pin=hostpf,actual_Host_source_pin=hostpf,actual_control_host_plan_pin=ppf,actual_lifetime_Source_plan_pin=lpf,actual_source_review_ready_pin=rpf,checks_count=len(checks),checks=checks,selected_new_build_Host_freeze_pin=plan['selected_new_build_Host_freeze_pin'],selected_new_Fortran_Source_freeze_pin=plan['selected_new_Fortran_Source_freeze_pin'],selected_control_Source_freeze_pin=plan['selected_control_Source_freeze_pin'],unchanged_control_Source_pin=plan['control_Source_pin'],full_scientific_EOF_not_repeated=True,actual_candidate_helper_body_not_executed=True,old_public5_both_bundle_current7_observations=oldbundles,first_error_object_traceback_preserved=True,only_exact_completed_SRC_bundle_PF_may_become_historical=True,MAC_bundle_current_retained_contract=True,retirement_file_receipt_flags_do_not_claim_directory_close=True,downstream_v15_retirement_gate_implemented_or_tested=False,downstream_required_contract='Only successful public7 report bound to ownHF/Source0, exact SRC case/read counts/one retirement, complete current intent+receipt PFs, historical before/after samePF and MF+sentinel retained; actualunlink and both directoryfsync returned true, exact absence; MAC currentPF. No generic missing PF allowance.',future_actual_report_pin=None,future_actual_retirement_receipt_pin=None,reader_qualified=False,AAA_qualified=False)
review=write('REVIEW.json',report)
print(json.dumps(dict(status=report['status'],failure=None,review_pin=review,current_host_pin=hostpf,control_host_plan_pin=ppf,lifetime_Source_plan_pin=lpf,checks_count=len(checks),source_only=True,business_executed=False,compiled=False,numeric=False,deletion_executed=False)))
