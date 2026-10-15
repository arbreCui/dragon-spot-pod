"""Two-hunk SOURCE append only; no business imports/API or payload reads."""
import ast,hashlib,json,time
from pathlib import Path
S=time.monotonic();OUT=Path(__file__).parent
D=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_saved_source_phase_diagnostic_sources')
OLD=Path('/private/tmp/axmat_saved_source_phase_normal_host_SOURCE_candidate_20261010_rohryp7y/saved_source_phase_diagnostic_host.CANDIDATE.py')
E=Path('/Users/wen/spot/validation/axial_material/refined_AAA_full_group_saved_source_phase_consistency_diagnostic_20261010.py')
PRIOR=Path('/private/tmp/axmat_saved_source_phase_host_independent_SOURCE_review_20261010_angular/REVIEW.json')
checks={};pins={}
def check(k,v):
 checks[k]=bool(v)
 if not v:raise ValueError(k)
def read(p,want=None):
 p=Path(p);a=p.stat();raw=p.read_bytes();b=p.stat();digest=hashlib.sha256(raw).hexdigest();keys=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
 check('stable:'+str(p),all(getattr(a,k)==getattr(b,k) for k in keys) and len(raw)==a.st_size)
 if want:check('sha:'+str(p),digest==want)
 pins[str(p)]={'sha256':digest,'bytes':len(raw)};return raw
r={'schema':'AXMAT_SAVED_SOURCE_PHASE_TWO_PID_HUNKS_INDEPENDENT_SOURCE_APPEND_V1','status':'SOURCE_ONLY_NOT_EXECUTED','business_imported':False,'business_API_called':False,'numeric_payload_read':False,'canonical_candidate_written':False,'diagnostic_executed':False,'future_actual_host_pin':None,'future_actual_terminal_pin':None,'future_actual_output_pins':None}
try:
 prior=json.loads(read(PRIOR,'e715c1170aae24eb44e017956cbd1bf6f8eac7a929d5ab2cee2f22aaaf921faa'))
 check('prior131_reference_only',prior['status']=='SOURCE_INTERFACE_NO_DETERMINISTIC_BLOCKER_FOUND' and len(prior['checks'])==131 and all(prior['checks'].values()))
 p=json.loads(read(D/'Root_finite_additional_PID_binding_source_inverse.json'))
 old=read(OLD,'230cfe009d989253d49bb18afc04a1fe64cafea53941e61100c6cd19d953634c').decode()
 new=read(D/'saved_source_phase_diagnostic_host.py','2b0e919aca6ac4e59a438ffe7d49fccc318bcc5821192a537472c06cbe0a3186').decode()
 check('host30676B',len(new.encode())==30676)
 check('exactly_two_hunks',p['finite_change_count']==len(p['changes'])==2 and p['parent_host_sha256']==hashlib.sha256(old.encode()).hexdigest() and p['host_sha256']==hashlib.sha256(new.encode()).hexdigest())
 restored=new
 for i,h in reversed(list(enumerate(p['changes']))):
  check('unique_inverse_hunk'+str(i),restored.count(h['after'])==1)
  restored=restored.replace(h['after'],h['before'],1)
 check('full_byte_inverse_to230',restored==old)
 nt=ast.parse(new);ot=ast.parse(old)
 unchanged=lambda t:[ast.dump(n,include_attributes=False) for n in t.body if not(isinstance(n,ast.FunctionDef) and n.name=='main')]
 check('all_globals_and_other_functions_unchanged',unchanged(nt)==unchanged(ot))
 evaluator=read(E,'e4eed9d520499cf15dae35c56adb1b7a3dea54e67e73046dd828ee47a1225fcf').decode();et=ast.parse(evaluator)
 claimcall=next(n for n in ast.walk(et) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='json_file' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value=='execution_claim.json')
 claim={ast.literal_eval(k):v for k,v in zip(claimcall.args[1].keys,claimcall.args[1].values)}
 check('producer_PID_osgetpid',ast.unparse(claim['PID'])=='os.getpid()')
 check('producer_parentPID_osgetppid',ast.unparse(claim['parent_PID'])=='os.getppid()')
 check('new_binding_typed_real_fields',"type(claim['PID']) is int and type(claim['parent_PID']) is int and claim['PID']==watch['pid'] and claim['parent_PID']==os.getpid()" in new)
 check('host_actual_claim_pin_and_PID_fields',all(s in new for s in ("actual_host_pid=os.getpid()","actual_child_claim=support.pin(OUTPUT/'execution_claim.json')","actual_child_claim_PID=claim['PID']","actual_child_claim_parent_PID=claim['parent_PID']","actual_claim_watchdog_host_PID_binding_verified=True")))
 check('claim_check_after_successful_execute_before_payload_accept',new.index("runner.execute(HOST/'run','admit',command,STAGE_CAP)")<new.index("claim['PID']==watch['pid']")<new.index('phase_validation=validate_phase_payload'))
 r.update(status='TWO_HUNK_SOURCE_APPEND_NO_BLOCKER_FOUND',checks=checks,source_pins=pins,root_final_host_SOURCE_qualified_sha256='2b0e919aca6ac4e59a438ffe7d49fccc318bcc5821192a537472c06cbe0a3186',root_final_host_SOURCE_bytes=30676,reviewed_parent_sha256='230cfe009d989253d49bb18afc04a1fe64cafea53941e61100c6cd19d953634c',prior131_review_path=str(PRIOR),prior131_review_sha256='e715c1170aae24eb44e017956cbd1bf6f8eac7a929d5ab2cee2f22aaaf921faa',prior131_full_survey_rerun=False,full_inverse_to230=True,original_genuine61970538de_bc_eb_chain_classes_methods_MRO_unchanged=True,original_caps_and_fullscope_unchanged=True,limits={'whole_seconds':60,'stage_seconds':60,'own_rss_mib':512,'joint_archive_bytes':67108864,'history_bytes':103079215104,'min_free_bytes':8589934592,'five_thread_environment_variables_each':'1','children':1,'retries':0},claim_fields_match_actual_fixed_producer=True,interpretation='The unchanged genuine executor directly Popen launches the evaluator; its claim PID is the actual evaluator getpid and parent_PID is the launching host getpid. New host rejects a mismatch before accepting the phase payload and preserves actual claim pin/PID fields in its own result.',remaining_actual_requirements=['Freeze complete D after original131 and this append package are copied.','Use ordinary E for actual Root receipts; never write into frozen D during/after business run.','One actual strict integer0/genuine PASS/normal threads1/RSS<512/whole<60 run remains required.','After all final Root receipts stdout stderr and terminal exist recheck HOST+OUT+D+E+canonical<64MiB and unchanged dynamic96GiB/free8GiB.'],qualification={'native_RSS_verified':False,'full_physical_neutron_balance_qualified':False,'source_partition_qualified':False,'multiplicity_qualified':False,'scientific_accuracy_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'same_MG_unreduced_reference_qualified':False})
except BaseException as e:r.update(status='TWO_HUNK_SOURCE_APPEND_FAILED',error=repr(e),checks=checks,source_pins=pins)
r['source_only_review_seconds']=time.monotonic()-S
path=OUT/'REVIEW.json'
with path.open('x') as f:json.dump(r,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
raw=path.read_bytes();print(json.dumps({'status':r['status'],'review_path':str(path),'review_sha256':hashlib.sha256(raw).hexdigest(),'review_bytes':len(raw),'checks':len(checks),'SOURCE_final_host_sha256':r.get('root_final_host_SOURCE_qualified_sha256'),'business_import_execute':False,'numeric_payload_read':False},indent=2))
if r['status']=='TWO_HUNK_SOURCE_APPEND_FAILED':raise SystemExit(1)
