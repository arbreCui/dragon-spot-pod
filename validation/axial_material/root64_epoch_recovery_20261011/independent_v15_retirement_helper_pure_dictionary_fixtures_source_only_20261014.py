"""Execute extracted helper defs with fake c/Path/os only, not a Host or science."""
import ast,copy,hashlib,json,stat
from pathlib import Path,PurePosixPath
from types import SimpleNamespace
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
HELPER=R/'v15_exact_completed_SRC_retirement_admission_source_v1_20261014.py'
raw=HELPER.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9e6864537985470f6ce9ed5679f375960bc23168e470efdd412a73ff2048efe5'
tree=ast.parse(raw);defs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
assert [n.name for n in defs]==['exact_public_pin','exact_public_live_pin','exact_public_nulls','admit_exact_public_stale_lifetimes']
current={};jsondata={};parents={};extra_existing=set();symlinks=set()
class FakePath(PurePosixPath):
 def exists(self):return str(self)in current or str(self)in parents or str(self)in extra_existing
 def is_symlink(self):return str(self)in symlinks
 def lstat(self):return SimpleNamespace(**parents[str(self)])
class FakeCommon:
 def same_pin(self,path,row):
  if current.get(str(path))!=row:raise RuntimeError('fake current PF mismatch')
 def read_bound_json_current(self,path,row):
  self.same_pin(path,row);return copy.deepcopy(jsondata[str(path)]),copy.deepcopy(row)
def selected_pin(hf,key):
 row=hf[key]
 if {x['path']:x for x in hf['dependencies']}.get(row['path'])!=row:raise RuntimeError('fake selected dependency mismatch')
 return row
ns=dict(stat=stat,Path=FakePath,c=FakeCommon(),os=SimpleNamespace(getuid=lambda:501),MI=2**20,selected_pin=selected_pin,current_pin_table=lambda rows:{x['path']:x for x in rows})
exec(compile(ast.Module(body=defs,type_ignores=[]),str(HELPER),'exec'),ns)
serial=0
def pf(path,size=256):
 global serial
 serial+=1;return dict(path=str(path),sha256='a'*64,size_bytes=size,identity=[123,1000+serial,stat.S_IFREG|0o644,1,size,100,100])
root=FakePath('/pure_memory/public7');exe=str(root/'runtime/control_unqualified')
life=json.loads((R/'public_read_compact_bq_admission_control_host_source_v7_20261014/EXACT_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN.json').read_bytes())
source=pf('/pure_memory/control.f90');sf=pf('/pure_memory/control_SF.json');lpf=pf('/pure_memory/lifetimePLAN.json')
life['unchanged_Fortran_Source_pin']=source;life['unchanged_public_Fortran_Source_freeze_pin']=sf
hf=dict(dependencies=[lpf],selected_completed_first_SRC_bundle_lifetime_Source_plan_pin=lpf)
own=dict(dependencies=[lpf],selected_completed_first_SRC_bundle_lifetime_Source_plan_pin=lpf,exact_completed_first_SRC_bundle_retirement_scope_only=True,retired_bundle_is_historical_not_current_no_generic_missing_skip=True,original_Fortran_math_7controls_9phases_11commands_unchanged=True)
plan=dict(completed_first_SRC_bundle_lifetime_Source_plan_pin=lpf)
report=dict(actual_control_Source_pin=source,actual_Source_freeze_pin=sf,fixed_current_pins=[lpf],output_pins=[],owned_runtime_pins=[],records=[],actual_control_results=[],actual_stale_host_evidence=[],actual_completed_bundle_retirements=[])
current[lpf['path']]=lpf;jsondata[lpf['path']]=life
for name in ('public_read_stale_BQ_SRC','public_read_stale_BQ_MAC'):
 cwd=root/name;selected='BQ64-SRC-ST'if name.endswith('SRC')else'BQ64-MAC-ST'
 bundle=pf(cwd/'coherent_complete_context.xsm',100163528);sentinel=pf(cwd/selected);mf=pf(cwd/'Host_independent_stale_before_full_EOF_SHA_all7.json')
 prepare=dict(command=[exe,name,'prepare'],status='PASS');read=dict(command=[exe,name,'read'],status='PASS')
 oracle=dict(case=name,phase='read',actual_terminal=dict(actual_public_read_status=1,actual_control_public_read_calls=1,actual_baseline_public_read_calls=0),actual_log_pin=pf(root/(name+'.log')))
 report['records'].extend([prepare,read]);report['actual_control_results'].append(oracle)
 evidence=dict(case=name,actual_before_manifest_pin=mf,actual_bundle_before_pin=bundle,actual_bundle_after_pin=bundle,actual_stale_before_pin=sentinel,actual_stale_after_pin=sentinel,actual_two_files_full_EOF_SHA_all7_unchanged=True,actual_other_BQ_absent=True,genuine_read_child_closed0=True,actual_read_record=read)
 for row in (mf,sentinel):current[row['path']]=row;report['output_pins'].append(row);report['owned_runtime_pins'].append(row)
 jsondata[mf['path']]=dict(schema='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1',case=name,actual_bundle_pin=bundle,actual_stale_pin=sentinel,other_BQ_absent=True,genuine_prepare_child_closed0=True,actual_prepare_record=prepare)
 if name.endswith('MAC'):
  current[bundle['path']]=bundle;report['output_pins'].append(bundle);report['owned_runtime_pins'].append(bundle)
  evidence.update(bundle_lifetime_status='CURRENT_RETAINED_AFTER_COMPLETED_READ',current_bundle_pin=bundle)
 else:
  before=[123,9,stat.S_IFDIR|0o755,4,128,10,10];before_unlink=[123,9,stat.S_IFDIR|0o755,5,160,20,20];after=[123,9,stat.S_IFDIR|0o755,4,128,30,30]
  parents[str(cwd)]=dict(st_dev=123,st_ino=9,st_mode=stat.S_IFDIR|0o755,st_nlink=5,st_size=160,st_mtime_ns=40,st_ctime_ns=40,st_uid=501)
  intentpf=pf(cwd/'Host_completed_SRC_bundle_retirement_intent.json');receiptpf=pf(cwd/'Host_completed_SRC_bundle_retirement_receipt.json')
  for row in (intentpf,receiptpf):current[row['path']]=row;report['output_pins'].append(row);report['owned_runtime_pins'].append(row)
  common=dict(case=name,actual_before_manifest_pin=mf,actual_stale_before_fullpin=sentinel,actual_stale_after_fullpin=sentinel,actual_prepare_record=prepare,actual_completed_read_record=read,actual_read_oracle=oracle,other_BQ_absent=True,actual_before_equals_after_full_SHA_all7=True,target_uid=501,no_retry=True,no_old_v5_file_targeted=True,physics_qualified=False)
  intent=dict(common,schema='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_INTENT_V1',exact_bundle_fullpin=bundle,actual_bundle_after_completed_READ_fullpin=bundle,target_single_link_required=True,parent_before_intent_identity=before,current_owned_target_count=1,only_this_exact_bundle_may_be_unlinked=True)
  receipt=dict(common,schema='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_RECEIPT_V1',actual_intent_pin=intentpf,exact_retired_bundle_fullpin=bundle,historical_completed_read_after_fullpin=bundle,parent_before_identity=before_unlink,parent_before_intent_identity=before,parent_after_identity=after,current_bundle_pin=None,primary_operation_failure=None,secondary_operation_failures=[],actual_retired_count=1)
  for key in ('intent_parent_fsync_attempted','intent_parent_fsync_returned','unlink_attempted','unlink_returned','parent_fsync_attempted','parent_fsync_returned','target_absent_observed','removed_current_owned_fullpin','retirement_completed','retired_bundle_historical_only','receipt_written_before_directory_close_and_any_later_check','directory_close_not_claimed_by_receipt'):receipt[key]=True
  jsondata[intentpf['path']]=intent;jsondata[receiptpf['path']]=receipt
  event=dict(case=name,intent_pin=intentpf,receipt_pin=receiptpf,historical_bundle_before_pin=bundle,historical_bundle_after_completed_read_pin=bundle,operation=receipt,retirement_completed=True,current_bundle_pin=None,post_receipt_failure=None,secondary_operation_failures=[])
  evidence.update(bundle_lifetime_status='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE',current_bundle_pin=None,actual_completed_bundle_retirement=event);report['actual_completed_bundle_retirements']=[event]
 report['actual_stale_host_evidence'].append(evidence)
prototype=copy.deepcopy(dict(hf=hf,own=own,plan=plan,report=report,current=current,jsondata=jsondata,parents=parents,extra_existing=extra_existing,symlinks=symlinks))
results=[]
def run(name,edit=None,expect_pass=False):
 global current,jsondata,parents,extra_existing,symlinks
 x=copy.deepcopy(prototype)
 if edit:edit(x)
 current=x['current'];jsondata=x['jsondata'];parents=x['parents'];extra_existing=x['extra_existing'];symlinks=x['symlinks']
 try:
  result=ns['admit_exact_public_stale_lifetimes'](x['hf'],x['own'],x['plan'],x['report'],root,exe)
  assert result['sole_completed_SRC_bundle_retirement_admitted']is True and result['MAC_bundle_retained_current']is True
  accepted=True;error=None
 except (RuntimeError,KeyError,StopIteration)as e:accepted=False;error=str(e)
 assert accepted is expect_pass,(name,accepted,error)
 results.append(dict(name=name,expected_admitted=expect_pass,actual_admitted=accepted,error=error))
def event(x):return x['report']['actual_completed_bundle_retirements'][0]
def src(x):return next(e for e in x['report']['actual_stale_host_evidence']if e['case'].endswith('SRC'))
def mac(x):return next(e for e in x['report']['actual_stale_host_evidence']if e['case'].endswith('MAC'))
def receipt(x):return event(x)['operation']
def intent(x):return x['jsondata'][event(x)['intent_pin']['path']]
run('legal_exact_SRC_retirement_plus_retained_current_MAC',expect_pass=True)
run('missing_SRC_current_bundle_pin',lambda x:src(x).pop('current_bundle_pin'))
run('missing_event_current_bundle_pin',lambda x:event(x).pop('current_bundle_pin'))
run('missing_event_post_receipt_failure',lambda x:event(x).pop('post_receipt_failure'))
run('missing_receipt_current_bundle_pin',lambda x:receipt(x).pop('current_bundle_pin'))
run('missing_receipt_primary_operation_failure',lambda x:receipt(x).pop('primary_operation_failure'))
run('missing_lifetime_future_report_field',lambda x:x['jsondata'][lpf['path']].pop('future_actual_public7_report_pin'))
run('duplicate_retirement_event',lambda x:x['report']['actual_completed_bundle_retirements'].append(event(x)))
run('zero_retirement_events',lambda x:x['report'].update(actual_completed_bundle_retirements=[]))
run('SRC_bundle_still_current_on_disk',lambda x:x['extra_existing'].add(src(x)['actual_bundle_before_pin']['path']))
run('SRC_bundle_dangling_symlink',lambda x:x['symlinks'].add(src(x)['actual_bundle_before_pin']['path']))
run('historical_SRC_bundle_in_liveoutput',lambda x:x['report']['output_pins'].append(src(x)['actual_bundle_before_pin']))
run('historical_SRC_bundle_alias_in_fixed',lambda x:x['report']['fixed_current_pins'].append(dict(src(x)['actual_bundle_before_pin'],path='/pure_memory/alias')))
run('MAC_bundle_missingcurrent',lambda x:x['current'].pop(mac(x)['actual_bundle_before_pin']['path']))
run('MAC_bundle_retired',lambda x:mac(x).update(bundle_lifetime_status='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE'))
run('receipt_loaded_vs_operation_mismatch',lambda x:x['jsondata'].__setitem__(event(x)['receipt_pin']['path'],dict(receipt(x),unexpected='forged')))
for key in ('intent_parent_fsync_attempted','intent_parent_fsync_returned','unlink_attempted','unlink_returned','parent_fsync_attempted','parent_fsync_returned','removed_current_owned_fullpin','retirement_completed'):
 run('false_'+key,lambda x,key=key:receipt(x).__setitem__(key,False))
run('boolean_retired_count',lambda x:receipt(x).__setitem__('actual_retired_count',True))
run('boolean_read_status',lambda x:receipt(x)['actual_read_oracle']['actual_terminal'].__setitem__('actual_public_read_status',True))
run('creation_nlink_wrong',lambda x:receipt(x)['parent_before_identity'].__setitem__(3,4))
run('creation_size_wrong',lambda x:receipt(x)['parent_before_identity'].__setitem__(4,128))
run('unlink_nlink_wrong',lambda x:receipt(x)['parent_after_identity'].__setitem__(3,5))
run('unlink_size_wrong',lambda x:receipt(x)['parent_after_identity'].__setitem__(4,160))
run('current_parent_has_unexpected_entry',lambda x:x['parents'][str(root/'public_read_stale_BQ_SRC')].__setitem__('st_nlink',6))
run('current_parent_UID_wrong',lambda x:x['parents'][str(root/'public_read_stale_BQ_SRC')].__setitem__('st_uid',502))
run('receipt_primary_operation_failure',lambda x:receipt(x).__setitem__('primary_operation_failure','fsync failed'))
run('event_close_failure',lambda x:event(x).__setitem__('post_receipt_failure','close failed'))
run('MF_current_file_missing',lambda x:x['current'].pop(src(x)['actual_before_manifest_pin']['path']))
run('sentinel_current_file_missing',lambda x:x['current'].pop(src(x)['actual_stale_after_pin']['path']))
run('intent_current_file_missing',lambda x:x['current'].pop(event(x)['intent_pin']['path']))
run('receipt_current_file_missing',lambda x:x['current'].pop(event(x)['receipt_pin']['path']))
run('duplicate_owned_receipt',lambda x:x['report']['owned_runtime_pins'].append(event(x)['receipt_pin']))
run('wrong_ownHF_selected_lifetime',lambda x:x['own'].__setitem__('selected_completed_first_SRC_bundle_lifetime_Source_plan_pin',sf))
run('lifetime_future_success_claim',lambda x:x['jsondata'][lpf['path']].__setitem__('future_actual_public7_report_pin',sf))
run('historical_bundle_noncanonical_extra_field',lambda x:src(x)['actual_bundle_before_pin'].__setitem__('forged',True))
run('lowercase_MF_schema_rejected',lambda x:x['jsondata'][src(x)['actual_before_manifest_pin']['path']].__setitem__('schema','ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_all7_V1'))
run('SRC_before_after_fullPF_mismatch',lambda x:src(x).__setitem__('actual_bundle_after_pin',dict(src(x)['actual_bundle_before_pin'],sha256='b'*64)))
run('actual_report_fixed_missing_lifetime_plan',lambda x:x['report'].__setitem__('fixed_current_pins',[]))
print(json.dumps(dict(status='PASS_EXTRACTED_REAL_RETIREMENT_HELPER_PURE_DICTIONARY_FIXTURES_ONLY',source_sha256=hashlib.sha256(raw).hexdigest(),cases=len(results),legal_count=sum(r['actual_admitted']for r in results),refusal_count=sum(not r['actual_admitted']for r in results),results=results,prototype_is_fake_memory_not_actual_PF_or_controls=True,Host_imported=False,retirement_operation_executed=False,compiler_executed=False,numerical_executed=False)))
