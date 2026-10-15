"""Finite closed-run evidence review; no project imports or calculations."""
import hashlib,json,os,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';HERE=Path(__file__).parent
BASE=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
RECEIPTS=BASE/'actual_component_execution_receipts'
SOURCE=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'
OUT=ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'
TERM=ART/'axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'
FACTORY=ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
FAMILY='SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_V15'
pins={};checks={};started=time.monotonic()
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,w=None,capture=False):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]),str(p)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0;parts=[]
 try:
  first=os.fstat(fd);fid=[first.st_dev,first.st_ino,first.st_mode,first.st_nlink,first.st_size,first.st_mtime_ns,first.st_ctime_ns];assert fid==before
  while b:=os.read(fd,1024*1024):
   h.update(b);n+=len(b)
   if capture:parts.append(b)
  last=os.fstat(fd);assert [last.st_dev,last.st_ino,last.st_mode,last.st_nlink,last.st_size,last.st_mtime_ns,last.st_ctime_ns]==before
 finally:os.close(fd)
 sha=h.hexdigest();assert identity(p)==before and n==before[4] and (w is None or sha==w),str(p)
 record=dict(path=str(p),sha256=sha,size_bytes=n,identity=before)
 if str(p) in pins:assert pins[str(p)]==record
 pins[str(p)]=record
 return b''.join(parts) if capture else record
def obj(p,w=None):return json.loads(pin(p,w,True))
def check(n,b):checks[n]=bool(b);assert b,n
summary=obj(RECEIPTS/'Root_actual_complete86_evidence_and_summary.json')
root=obj(summary['Root_actual_terminal']['path'],'3a422572fe78d51ffc4938294d8207a72c059d456dccfe1d1356e57c7e2384a2')
term=obj(TERM/'terminal_return.json','ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e')
stdout=obj(term['full_stdout']['path'],term['full_stdout']['sha256']);pin(term['full_stderr']['path'],term['full_stderr']['sha256'])
seal=obj(OUT/'seal.json','b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206')
d=obj(OUT/'declaration.json','6dee0b453ea519beeb85abd834c22939c0f5c49565bcd3c793c6b83bf7e092a7')
result=obj(OUT/'driver_result.json',seal['files']['driver_result.json']);audit=obj(OUT/'audit/result.json',seal['files']['audit/result.json'])
controls=obj(OUT/'audit/controls.json',seal['files']['audit/controls.json']);source_admission=obj(SOURCE/'source_admission.json',d['source_inventory']['files']['source_admission.json'])
stages=obj(OUT/FAMILY/'stages.json',seal['files'][FAMILY+'/stages.json'])['stages']
check('genuine_Root1eccba_session22445_to767c5d_strict_exit0_closed',root['initial']['chunk_id']=='1eccba' and root['initial']['session_id']==22445 and root['terminal']['chunk_id']=='767c5d' and type(root['terminal']['exit_code']) is int and root['terminal']['exit_code']==0 and root['session_closed'] is True and root['record_written_after_actual_terminal_return'] is True and root['actual_tool_terminal_return_observed'] is True)
check('formal_external_terminal_bound_to_same_complete_Root_receipt',type(term['returncode']) is int and term['returncode']==0 and term['record_producer']=='root' and term['actual_tool_terminal_return_observed'] is True and term['record_written_after_actual_terminal_return'] is True and term['actual_tool_provenance']['Root_actual_raw_tool_terminal_receipt']==summary['Root_actual_terminal'] and term['actual_tool_provenance']['actual_terminal_return']==root['terminal'] and term['actual_tool_provenance']['no_restart'] is True)
pin(FACTORY,'cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447')
check('exact_real_canonical_run_command_and_current_factory_pin',term['command']==root['input']['argv']==[str(Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')),str(FACTORY),'run-build','--sha256',pins[str(OUT/'declaration.json')]['sha256']] and term['source']==dict(path=str(FACTORY),sha256=pins[str(FACTORY)]['sha256']))
check('complete_original_caps_in_declaration',tuple(d[k] for k in ['total_wall_seconds','stage_wall_seconds','rss_cap_mib','archive_reserve_bytes','artifact_budget_bytes','min_free_bytes','threads','numeric_children_at_once','retries'])==(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0))
check('genuine_complete_result_audit_and_raw_controls_PASS',result['classification']=='COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_CONTROLS_ONLY_V15' and result['error'] is None and audit['classification']=='PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_ROOT_INDEX_BUILD_CONTROLS_ONLY_V15' and audit['control_status']==audit['binary_status']=='PASS' and controls['status']=='PASS' and stdout['result']==result and audit['declaration_sha256']==pins[str(OUT/'declaration.json')]['sha256'])
original68=dict(fixtures=8,inherited_bitwise_source_pairs_reexecuted=1146,additional_permutation_source_pairs=6,dense_reference_kernel_calls=378,memory_module_negative_calls=6,dictionary_positive_primitives=3,dictionary_module_negative_calls=8,original_stages_retained=31,total_declared_stages=68,original_factor_diagonal_45_stages_retained=45,additional_keycodec_driver_build_stages=2,additional_keycodec_execute_stages=21,inherited_last_cprime_stages_retained=40,factor_codec_positive_fixtures=3,factor_codec_module_negative_calls=4,factor_codec_public_factor_calls=6,factor_codec_public_solve_calls=12,actual_returned_unit_kernel_calls=2696,actual_guard_rejected_unit_kernel_calls=14,actual_total_unit_kernel_invocations=2710,bitwise_source_pairs=1152,independent_pivot_rhs=3,negative_calls=14,cache_cap_negative_calls=2,production_groups=370,production_layers=48,production_angles=32,source_moments=3,bitwise_compared_output_scalars=2042712,compared_actual_field_and_source_bytes=53816832)
expected86=dict(original68,total_declared_stages=86)
check('all_original68_thirty_count_fields_and_all86_only_total_difference',len(original68)==30 and all(x['original_68_control_counts']==original68 for x in [result,audit,controls]) and result['control_counts']==audit['control_counts']==controls['counts']==summary['control_counts']==expected86)
contract=d['sender_control_contract'];positive=[c for c in contract['cases'] if not c['negative']];steps=[s for c in positive for s in c['steps']]
sender_counts=dict(positive_cases=10,expected_guard_rejection_cases=4,positive_steps=22,reference_wrapper_calls=24,candidate_wrapper_calls=24,wrapper_calls_total=48,observer_calls_total=34,direct_candidate_steps=sum(s['expected_route']==1 for s in steps),sparse_fallback_steps=sum(s['expected_route']==2 for s in steps),empty_steps=sum(s['expected_route']==0 for s in steps),raw_file_count=70,raw_bytes=288241824,independently_verified_active_output_scalars=sum(2*c['nun']*s['active_groups'] for c in positive for s in c['steps']))
sender=controls['sender_window_controls'];check('all14_sender_actual13_count_fields_separate_from2710_kernel_calls',len(contract['cases'])==14 and len(positive)==10 and len(steps)==22 and all(x['sender_window_control_counts']==sender_counts for x in [result,audit,controls,summary]) and sender['counts']==sender_counts and sender['real_SPOT_receiver_calls_in_this_observer_executable']==0 and sender['solver_math_credit'] is False and result['sender_wrapper_observer_real_SPOT_credit']==audit['sender_wrapper_observer_real_SPOT_credit']==0)
c=d['control_contract'];old_labels=['controls/positive/execute']+['controls/negative_'+x['name']+'/execute' for x in [*c['negative_cases'],*c['cap_negative_cases']]]+['controls/memory_positive/execute']+['controls/memory_negative_'+x['name']+'/execute' for x in c['memory_negative_cases']]+['controls/dedup_positive/execute']+['controls/dedup_negative_'+x['name']+'/execute' for x in c['dedup_negative_cases']]+['controls/factor_positive/execute']+['controls/factor_negative_'+x['name']+'/execute' for x in c['factor_negative_cases']]+['controls/keycodec_positive/execute']+['controls/keycodec_negative_'+x['name']+'/execute' for x in c['keycodec_negative_cases']]
labels=['build/build_'+str(i).zfill(2) for i in range(12)]+old_labels+['sender_controls/'+x['name']+'/execute' for x in contract['cases']]+['audit/audit']
negative23={'controls/keycodec_negative_'+x['name']+'/execute' for x in c['keycodec_negative_cases']};negative1={'sender_controls/'+x['name']+'/execute' for x in contract['cases'] if x['negative']}
check('86_exact_order12build59old14sender_full_final_audit',len(d['build_commands'])==12 and len(old_labels)==59 and len(labels)==86 and len(set(labels))==86 and [s['label'] for s in stages]==labels and len(negative23)==20 and len(negative1)==4)
watch_records=[]
for s in stages:
 relative=s['label']+'.watchdog.json';w=obj(OUT/relative,seal['files'][relative]);rc=23 if s['label'] in negative23 else 1 if s['label'] in negative1 else 0
 assert s['status']==('FAILED' if rc else 'PASS') and type(w['returncode']) is int and w['returncode']==rc
 assert type(w['pid']) is int and w['pid']>0 and w['command']==s['command'] and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True
 assert w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['wall_cap_seconds']<=s['wall_cap_seconds']<=600 and 0<=w['elapsed_seconds']<w['wall_cap_seconds']
 assert s['log_sha256']==seal['files'][s['label']+'.log']
 watch_records.append(dict(label=s['label'],expected_returncode=rc,status=s['status'],watchdog=w))
check('all86_watchdogs_actual_PIDs_RSS_wall_and_exact24_negative_returns',len(watch_records)==86 and sum(x['expected_returncode']==0 for x in watch_records)==62 and sum(x['expected_returncode']==23 for x in watch_records)==20 and sum(x['expected_returncode']==1 for x in watch_records)==4)
check('whole_summary_counts_peak_and_untruncated_independent_audit',summary['stages']==86 and summary['ordinary_PASS']==62 and summary['expected_rejections']==24 and summary['unexpected_failures']==0 and summary['guard_sampled_own_child_peak_rss_mib']==max(x['watchdog']['sampled_peak_rss_mib'] for x in watch_records) and stages[-1]['elapsed_seconds']==summary['independent_audit_seconds'] and stages[-1]['wall_cap_seconds']==summary['independent_audit_wall_budget_seconds'] and 0<summary['independent_audit_seconds']<summary['independent_audit_wall_budget_seconds']<=600)
for i,s in enumerate(stages[:12]):assert s['command']==d['build_commands'][i]
check('all12_actual_build_commands_match_exact_declaration',True)
def inventory(root,hash_files):
 files={};dirs={str(root):identity(root)}
 for parent,ds,fs in os.walk(root,followlinks=False):
  for name in ds:
   p=Path(parent)/name;assert stat.S_ISDIR(p.lstat().st_mode);dirs[str(p)]=identity(p)
  for name in fs:
   p=Path(parent)/name;assert stat.S_ISREG(p.lstat().st_mode)
   if hash_files:record=pin(p);files[str(p.relative_to(root))]=record['sha256']
   else:assert str(p) in pins and identity(p)==pins[str(p)]['identity'];files[str(p.relative_to(root))]=pins[str(p)]['sha256']
 return dict(files=files,symlinks={},directories=sorted(str(Path(p).relative_to(root)) for p in dirs if p!=str(root))),dirs
outi,outdirs=inventory(OUT,True);sourcei,sourcedirs=inventory(SOURCE,True)
check('every_OUT7737_sealed_file_plus_seal_fresh_SHA_full_namespace_exact',len(seal['files'])==7737 and outi['files']=={**seal['files'],'seal.json':pins[str(OUT/'seal.json')]['sha256']} and outi['directories']==seal['directories'] and len(outi['directories'])==79)
check('all_SOURCE18_full_inventory_fresh_SHA_no_links_or_directories',sourcei==dict(files=d['source_inventory']['files'],symlinks=d['source_inventory']['symlinks'],directories=d['source_directories']) and len(sourcei['files'])==18 and sourcei['symlinks']=={} and sourcei['directories']==[])
check('every_SOURCE_file_has_complete_declared_owner',all(d['files'].get(str(SOURCE/n))==sha for n,sha in sourcei['files'].items()))
check('kernel_sender_H7d_math_source_pins_original_exact',sourcei['files']['SPOT1P64.f90']=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5' and sourcei['files']['FLU2DR64.f']=='cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1' and sourcei['files']['complete_environment_streaming_sha_helper_v14b.py']=='7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3' and sourcei['files']['rank1_factor_cache_last_cprime_trim_controls.f90']=='eab3a7790e9f499282017cc37581be5acb07f8a4170e8fcaae95b0de47305d52')
check('actual_successful_runtime_pinned_by_driver_and_whole_seal',result['runtime_sha256']==pins[str(OUT/'runtime/Dragon')]['sha256']==seal['files']['runtime/Dragon'])
raw=obj(controls['complete_raw_receipt']['path'],controls['complete_raw_receipt']['sha256']);check('all_original_control_raw_receipt_members_owned_by_same_successful_seal',all(seal['files'].get(k)==v for k,v in raw['files'].items()) and raw['before_numeric_gates'] is True)
rawsender=obj(OUT/'raw_sender_controls_receipt.json',seal['files']['raw_sender_controls_receipt.json']);check('sender_complete112_file_preservation_receipt_and_contract_before_numeric_gates',rawsender['files']=={k:v for k,v in seal['files'].items() if k.startswith('sender_controls/')} and len(rawsender['files'])==112 and rawsender['before_numeric_gates'] is True and rawsender['declared_sender_control_contract']==contract and rawsender['raw_identity_before_after_equal'] is True)
senderids={str((OUT/'sender_controls').relative_to(OUT/'sender_controls')):identity(OUT/'sender_controls')}
for p,ids in outdirs.items():
 if Path(p).is_relative_to(OUT/'sender_controls'):senderids[str(Path(p).relative_to(OUT/'sender_controls'))]=ids
for p,record in pins.items():
 if Path(p).is_relative_to(OUT/'sender_controls'):senderids[str(Path(p).relative_to(OUT/'sender_controls'))]=record['identity']
check('all127_sender_raw_file_directory_identities_match_before_after_actual_receipt',senderids==rawsender['raw_identity_snapshot']==sender['raw_identity_snapshot'])
wantedraw={x['name']+'/'+row['name']:row for x in contract['cases'] for row in x['raw_files']}
check('all70_sender_raw_binary_files288241824_complete_exact_bytes_and_fresh_hash',len(wantedraw)==70 and sum(x['size_bytes'] for x in wantedraw.values())==288241824 and set(sender['all_raw_files'])==set(wantedraw) and all(row==dict(path=str(OUT/'sender_controls'/name),bytes=wantedraw[name]['size_bytes'],sha256=seal['files']['sender_controls/'+name]) and pins[str(OUT/'sender_controls'/name)]['size_bytes']==row['bytes'] for name,row in sender['all_raw_files'].items()))
check('all14_actual_sender_cases_return_exact_and_have_all_raw_descriptors',[x['name'] for x in sender['cases']]==[x['name'] for x in contract['cases']] and all(actual['status']==('EXPECTED_REJECTION' if expected['negative'] else 'PASS') and actual['actual_returncode']==expected['expected_returncode'] and set(actual['raw_files'])=={x['name'] for x in expected['raw_files']} for actual,expected in zip(sender['cases'],contract['cases'])))
for case in sender['cases']:
 for n,row in case['raw_files'].items():assert row==sender['all_raw_files'][case['name']+'/'+n]
 for key in ['actual_log','actual_watchdog','actual_manifest']:
  row=case[key];p=Path(row['path']);assert row['sha256']==pins[str(p)]['sha256'] and row['bytes']==pins[str(p)]['size_bytes']
check('all_sender_case_log_watch_manifest_descriptors_fresh_owned',True)
tails=['actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources']
check('all_four_whole_success_tails_exact_complete_raw_stdout_and_terminal',all(term[k]==stdout[k] for k in tails) and term['actual_tail_check']=='PASS' and 0<term['actual_elapsed_seconds']<1800 and term['actual_elapsed_seconds']==summary['whole_seconds'] and term['actual_archive_bytes']==summary['whole_archive_bytes'])
archive=sum(v['size_bytes'] for p,v in pins.items() if Path(p).is_relative_to(OUT) or Path(p).is_relative_to(SOURCE))
check('all_SOURCE_OUT_archive801695953_bytes_below_original2GiB',archive==term['actual_archive_bytes']==801695953 and archive<2*2**30)
r=term['actual_resources'];check('actual_full_dynamic_history_tail96GiB_free8GiB_declared_roots_preserved',r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30 and archive<=r['artifact_bytes']<=96*2**30 and r['disk_free_bytes']>=8*2**30 and r['declared_resource_roots']==d['resource_roots'] and set(d['resource_roots'])<=set(r['resource_roots']) and r['resource_scope_policy']==d['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and r['resource_scope_contract']==d['resource_scope_contract'])
qpath=BASE/'Root_actual_resource_module_admission.json';q=obj(qpath,'5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676');check('prior_immutable_resource_Q_unchanged_and_complete_envelope_retained',q['status']=='PASS_RESOURCE_MODULE_ONLY' and d['root_index_resource_source_admission']['complete_actual_resource_module_admission']==q and d['root_index_resource_source_admission']==source_admission['root_index_resource_source_admission'])
check('complete_H7d_admission_body_identical_every_actual_whole_record',all(x['stream_environment_helper_admission']==d['stream_environment_helper_admission'] for x in [source_admission,audit,result]))
check('all_original_math_bitwise_memory_dictionary_codec_audit_flags_PASS',all(audit[k] is True for k in ['rank1_factor_cache_math_and_rhs_order_unchanged','all_new_cache_outputs_bitwise_equal_to_uncached','operator_identity_guard_negative_controls_passed','cross_group_identity_controls_passed','factor_diagonal_codec_controls_passed','all_original_and_memory_controls_bitwise_passed','full_shape_MATMUL_and_RHS_order_unchanged','all_original_memory_and_dictionary_controls_bitwise_passed']) and all(controls[k] is True for k in ['all_actual_outputs_finite','all_flux_cour_xnei_bitwise_equal','all_sources_independently_reconstructed','all370_plans_retained_and_accounted','all_lifecycle_clears_zero','physical_dense_translation_outputs_bitwise_unchanged','actual_guard_rejections']))
check('all_component_actual_records_keep_native_full_transport_AAA_ABA_false',all(x[k] is False for x in [root,summary] for k in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']) and all(x[k] is False for x in [d,audit,result] for k in ['actual_full_FLU_entry_executed','transport_launched','AAA_accuracy_qualified','ABA_admitted']) and audit['native_RSS_proof_obtained'] is False and controls['actual_full_FLU_entry_executed'] is False and controls['scientific_accuracy_or_performance_qualified'] is False and source_admission['scientific_qualification'] is False and sender['native_RSS_verified'] is False)
check('complete_namespaces_and_every_identity_stable_after_whole_read',inventory(OUT,False)==(outi,outdirs) and inventory(SOURCE,False)==(sourcei,sourcedirs) and all(identity(p)==v['identity'] for p,v in pins.items()))
value=dict(schema='AXMAT_V15_ACTUAL_COMPLETE86_INDEPENDENT_FULL_RAW_READONLY_REVIEW_V1',status='PASS_ACTUAL_COMPLETE86_COMPONENT_ONLY_FORMAL_ADMISSION_SEPARATE',all_checks_passed=True,checks=checks,
 actual_Root=dict(initial_chunk='1eccba',session_id=22445,terminal_chunk='767c5d',strict_integer_exit=0,session_closed=True),whole_actual_seconds=term['actual_elapsed_seconds'],whole_archive_bytes=archive,maximum_actual_sampled_own_child_rss_mib=summary['guard_sampled_own_child_peak_rss_mib'],normal_PASS=62,exact_expected_exit23=20,exact_expected_exit1=4,
 original68_counts=original68,complete86_counts=expected86,sender_counts=sender_counts,all86_actual_watchdogs=watch_records,
 complete_SOURCE_inventory=sourcei,complete_OUT_inventory=outi,complete_namespace_directory_identities={**outdirs,**sourcedirs},all_fresh_full_file_pins=list(pins.values()),
 fresh_SOURCE_OUT_regular_file_count=len(outi['files'])+len(sourcei['files']),sealed_OUT_member_count=len(seal['files']),
 source_math_changes=False,original_threshold_changes=False,resource_qualification_modified=False,
 native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,formal_runtime_INPUT_admission_performed_by_this_review=False,
 business_import_or_execution_performed=False,resource_full_scan_performed=False,Root_session_polled=False,project_files_written=False,
 numerical_raw_reconstruction_rerun=False,review_scope='Fresh full SHA/EOF/7-identity and exhaustive frozen SOURCE/OUT namespace verification, all genuine Root/seal/raw/control/watchdog/audit/tail records. The original independent raw numerical audit is verified as an actually completed stage; it is not executed again. Entire 28GB historical external inputs are not rehashed by this reader.',review_seconds=time.monotonic()-started)
with (HERE/'REPORT.json').open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=value['status'],checks=len(checks),fresh_SOURCE_OUT_regular_files=value['fresh_SOURCE_OUT_regular_file_count'],fresh_regular_pins=len(pins),archive_bytes=archive,report_sha256=hashlib.sha256((HERE/'REPORT.json').read_bytes()).hexdigest(),review_seconds=value['review_seconds'],business_executed=False),allow_nan=False))
