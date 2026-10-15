from pathlib import Path
import hashlib,importlib.util,json,os,shlex,stat,sys
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
A=ROOT/'validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1';E=A.with_name(A.name+'-evidence');D=Path(__file__).parent
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def seven(p):
 q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode)and not q.is_symlink()and ids(s)==p['identity']and s.st_size==p['size_bytes']
def pin(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 assert s.st_size<=64*2**20 or p.is_relative_to(A)or p.is_relative_to(E)
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
  assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
 assert ids(p.lstat())==ids(s);return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
 if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
 return json.loads(Path(p).read_bytes())
def inventory(root):
 result=[]
 for cwd,dirs,files in os.walk(root,followlinks=False):
  assert not Path(cwd).is_symlink()
  for n in dirs:assert not(Path(cwd)/n).is_symlink()
  for n in files:
   p=Path(cwd)/n;s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink();result.append((str(p),s.st_size))
 return result
def module(p,name):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
assert not(D/'REVIEW.json').exists()and not(D/'TRUE_TOOL_RETURNS.json').exists()
hp=pin(A/'Root_actual_current_material_evidence_summary.json');h=load(hp);cp=h['actual_complete_child_receipt']['report'];c=load(cp)
ap=pin(R/'ROOT_EXACT_COMPARE_THREE_V7_ACTUAL30_ARGV_20261014.json');argv=load(ap);rp=argv['actual_request_pin'];request=load(rp)
tp=pin(R/'ROOT_ACTUAL_COMPARE_THREE_V7_ACTUAL30_TRUE_TOOL_RETURNS_20261014.json');raw=load(tp);z=raw['actual_terminal_return']
assert raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and raw['original_integer_exit_code']==1 and type(z['exit_code'])is int and z['exit_code']==1 and z.get('session_id')is None
assert raw['actual_initial_return']['chunk_id']=='fe1897'and raw['actual_initial_return']['session_id']==2767 and z['chunk_id']=='32a97f'and raw['exact_executed_command']==argv['shell_safe_command']and shlex.split(raw['exact_executed_command'])==argv['argv']and len(argv['argv'])==30
failure='ResourceFailure: FAIL_RESOURCE: experiment regular-file total exceeds declared artifact budget'
assert h['schema']=='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'and h['operation']=='compare-three'and h['status']=='ACTUAL_CURRENT_EVIDENCE_FAILED_NO_RETRY'and h['failure']==h['after_check_error']==failure
assert h['actual_intentional_exit2_normal_closure']is True and h['actual_complete_child_receipt']['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2'
assert c['schema']=='ACTUAL_CURRENT_OBSERVED_A_TO_THREE_NATIVE_RAW_MACRO_COMPARISON_V1'and c['observed_final_A_pair']==request['observed_final_A_pair']and c['whole_archive_producer_seals_not_relabelled']is True
sfpath=Path(argv['argv'][argv['argv'].index('--source-freeze-summary')+1]);hfpath=Path(argv['argv'][argv['argv'].index('--host-freeze-summary')+1]);sp=pin(sfpath);hfp=pin(hfpath);sf=load(sp);hf=load(hfp)
fixed=h['fixed_current_pins'];assert len(fixed)==len({p['path']for p in fixed})==6050 and {p['path']:p for p in fixed}=={p['path']:p for p in hf['dependencies']+[hfp,rp]}
for p in fixed:seven(p)
out=h['complete_output_pins'];assert len(out)==len({p['path']for p in out})==17
for p in out:assert pin(p['path'])==p
assert cp in out and h['actual_watchdog_full_pin']in out and h['actual_log_full_pin']in out
currentinventory=dict(inventory(A)+inventory(E));assert set(currentinventory)=={p['path']for p in out}|{hp['path']}and all(currentinventory[p['path']]==p['size_bytes']for p in out+[hp])
watch=load(h['actual_watchdog_full_pin']);assert type(watch['returncode'])is int and watch['returncode']==2 and watch['limit_failure']is None and watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['sampled_peak_rss_mib']<512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True
assert len(h['records'])==1 and h['records'][0]['status']=='FAILED'and h['records'][0]['label']=='evidence-stage/complete_evidence'and h['records'][0]['error']=='own-child stage failed; no retry'and h['records'][0]['command']==watch['command']
stage=load(next(p for p in out if p['path']==str(A/'evidence-stage/stages.json')));assert set(stage)=={'stages'}and stage['stages']==h['records']
assert type(h['SELF_peak_bytes'])is int and h['SELF_peak_bytes']<512*2**20 and 0<h['wall_seconds']<1800 and h['original_guard_class']=='OwnRSSSerialExecutor'and h['original_guard_MRO_unchanged']is True
receipt=json.loads(Path(h['actual_log_full_pin']['path']).read_bytes());assert receipt==h['actual_complete_child_receipt']
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2**31,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0);assert request['original_caps']==caps
for obj in [h,c,h['actual_complete_child_receipt'],request]:
 for k,v in obj.items():
  if k.endswith('_qualified')or k in ['historical_native_RAM_bits_verified','original_XSM_memory_bits_verified','historical_unsaved_context_recovered','ABA_admitted','goal_complete']:assert v is False
comparisons=c['comparisons'];assert len(comparisons)==3 and [x['plane']for x in comparisons]==[1,2,3]
rows=[]
for row,producer in zip(comparisons,request['actual_native_producers']):
 assert type(row['plane'])is int and row['plane']==producer['plane']and row['archive_pin']==producer['archive_pin'];seven(row['archive_pin'])
 assert row['compared_all_macro_records']==19620 and row['compared_original_payload_words']==3734983 and row['raw_word_mismatches']==3167229 and row['full_original_scope_retained']is True and len(row['all_output_pins'])==4 and all(p in out for p in row['all_output_pins'])
 sizes={Path(p['path']).name:p['size_bytes']for p in row['all_output_pins']};assert sizes=={'complete_macro_comparison.jsonl':20413399,'original_archive_index.sqlite':52441088,'original_words.bin':150267572,'physical.jsonl':34371817}
 rows.append(dict(plane=row['plane'],archive_pin=row['archive_pin'],original_report_compared_macro_records=row['compared_all_macro_records'],original_report_compared_payload_words=row['compared_original_payload_words'],original_report_positional_raw_word_mismatches=row['raw_word_mismatches'],all_new_output_pins=row['all_output_pins'],actual_new_output_bytes=sum(sizes.values()),actual_spool_bytes=sizes,full_original_scope_retained=True))
assert c['all_raw_word_mismatches']==sum(x['raw_word_mismatches']for x in comparisons)==9501687
roots=request['joint_archive_roots'];extra=request['explicit_cumulative_metadata_file_pins'];assert len(roots)==len(set(roots))==25 and len(extra)==4 and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)
assert extra==sf['retained_actual_GENDF_explicit_metadata_file_pins']and h['resources_after']['explicit_metadata_files']==extra and h['resources_after']['explicit_external_metadata_bytes']==22676
support=module(R/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/prepare_cli_host_v15.py','compare_actual_post_original_support');sys.path.insert(0,str(support.PARENT.parent));production,prodpf=support.load(support.PARENT,support.PARENT_SHA,'compare_actual_post_original_parent')
resource=production.DiskResources(ROOT/'validation',roots,8*2**30,2**31)
try:resource.check();raise AssertionError('original actual resource failure unexpectedly disappeared')
except production.ResourceFailure as e:
 snapshot=e.snapshot;assert str(e)=='FAIL_RESOURCE: experiment regular-file total exceeds declared artifact budget'and snapshot==resource.latest
assert snapshot['resource_roots']==roots and snapshot['artifact_budget_bytes']==2**31 and snapshot['min_free_bytes']==8*2**30 and snapshot['artifact_bytes']==2149687331 and snapshot['regular_files']==339
external=0
for p in extra:
 seven(p);assert pin(p['path'])==p
 if not any(Path(p['path']).is_relative_to(Path(root))for root in roots):external+=p['size_bytes']
assert external==22676
complete=snapshot['artifact_bytes']+external;assert complete==2149710007 and complete-2**31==2226359
saved=h['resources_after'];assert saved['complete_joint_five_root_fresh']['resource_roots']==roots and saved['complete_joint_roots_plus_metadata_bytes']==saved['complete_joint_five_root_fresh']['artifact_bytes']+external==2146515995
assert saved['complete_joint_roots_plus_metadata_bytes']+hp['size_bytes']==complete
diagp=pin(R/'ROOT_COMPARE_THREE_ACTUAL_SAVED_OUTPUT_TYPED_PATH_DIAGNOSIS_20261014.json');diag=load(diagp)
assert diag['schema']=='ROOT_COMPARE_THREE_ACTUAL_SAVED_OUTPUT_TYPED_PATH_DIAGNOSIS_V1'and diag['diagnosis']=='POSITIONAL_ZIP_COMPARISON_OF_DIFFERENT_NATIVE_RECORD_ORDERS'and diag['original_Root_exit_code_retained']==1 and diag['original_joint_resource_failure_retained']is True and diag['source_reports_not_modified']is True
assert diag['original_archive_not_redecoded']is True and diag['original_pool_payload_not_reopened']is True and diag['formal_corrected_raw_word_comparison_executed']is False
for row,comparison in zip(diag['results'],comparisons):
 assert row['plane']==comparison['plane']and row['typed_path_count']==19620 and row['path_sets_equal']is True and row['all_same_type_and_counts']is True and row['all_same_original_payload_SHA']is True and row['diagnostic_source_pin']in comparison['all_output_pins']
for p in fixed:seven(p)
for p in out+[hp,ap,tp,diagp]:seven(p)
result=dict(schema='INDEPENDENT_COMPARE_THREE_V7_ACTUAL_FAILURE_FACTS_POSTVERIFICATION_V1',status='PASS_ACTUAL_COMPARE_THREE_V7_FAILURE_FACTS_POSTVERIFICATION',failure=None,review_failure=None,business_pass=False,business_failure=h['failure'],source_only=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,actual_aggregate_host_pin=hp,actual_aggregate_report_pin=cp,actual_Root_true_tool_pin=tp,actual_Root_argv_pin=ap,actual_request_pin=rp,actual_Source_freeze_pin=sp,actual_Host_freeze_pin=hfp,actual_Root_integer_exit_code=1,original_Root_exit_code_retained=1,actual_original_Root_terminal_return=z,actual_host_status=h['status'],actual_host_failure=h['failure'],actual_host_after_check_error=h['after_check_error'],actual_child_status=h['actual_complete_child_receipt']['status'],actual_child_integer_exit_code=watch['returncode'],actual_original_failed_no_retry_record=h['records'][0],actual_intentional_child_exit2_closed=True,actual_watchdog_full_pin=h['actual_watchdog_full_pin'],actual_log_full_pin=h['actual_log_full_pin'],actual_watchdog_limit_failure=watch['limit_failure'],actual_watchdog_elapsed_seconds=watch['elapsed_seconds'],actual_watchdog_peak_rss_mib=watch['sampled_peak_rss_mib'],actual_SELF_peak_bytes=h['SELF_peak_bytes'],actual_wall_seconds=h['wall_seconds'],actual_fixed_current_pin_count=6050,all6050_fixed_current7_verified_twice=True,actual_complete_new_output_pins=out+[hp],actual_complete_new_output_count=18,actual_complete_new_output_bytes=sum(p['size_bytes']for p in out+[hp]),all18_new_outputs_full_EOF_SHA_and_current7_verified=True,actual_three_original_archive_inputs_metadata_only_no_second_EOF=True,actual_per_plane_reported_comparison_facts=rows,original_report_total_compared_payload_words=sum(x['compared_original_payload_words']for x in comparisons),original_report_total_positional_raw_word_mismatches=c['all_raw_word_mismatches'],original_caps=caps,actual_joint25_roots=roots,actual_explicit_external_metadata_file_pins=extra,actual_explicit_external_metadata_bytes=external,actual_original_DiskResources_failure_snapshot=snapshot,actual_current_original_joint_role_bytes=snapshot['artifact_bytes'],actual_original_joint_role_excess_bytes=snapshot['artifact_bytes']-2**31,actual_current_complete_joint_roots_plus_metadata_bytes=complete,actual_complete_joint_excess_bytes=complete-2**31,actual_saved_before_final_Host_joint_roots_plus_metadata_bytes=saved['complete_joint_roots_plus_metadata_bytes'],actual_final_Host_report_bytes=hp['size_bytes'],final_Host_report_addition_exactly_explains_resource_excess=True,actual_original_resource_failure_retained=True,actual_Root_saved_output_typed_path_diagnosis_pin=diagp,Root_diagnostic_evidence_scope='Root only read new saved comparison JSONL rows; this reviewer verifies the diagnosis metadata and source pins without repeating scientific analysis.',Root_diagnostic_saved_results=diag['results'],original_positional_word_mismatch_totals_not_valid_physical_disagreement=True,formal_corrected_raw_word_comparison_executed=False,original_reports_not_modified=True,business_or_scientific_execution_retried=False,old_scientific_payload_or_native_archive_decode_repeated=False,physics_qualified=False,three_plane_qualified=False,GLOBAL_qualified=False,rank_qualified=False,online_BOOT_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,reviewer_source_pin=pin(__file__))
p=D/'REVIEW.json'
with p.open('x')as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(p),actual_Root_integer_exit_code=1,actual_complete_new_output_count=18,actual_complete_joint_excess_bytes=2226359,original_report_total_positional_mismatches=9501687,physics_qualified=False)),flush=True)
