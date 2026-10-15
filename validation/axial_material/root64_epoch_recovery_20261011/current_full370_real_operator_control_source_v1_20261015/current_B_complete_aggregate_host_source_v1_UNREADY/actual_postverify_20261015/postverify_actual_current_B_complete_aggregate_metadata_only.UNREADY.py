"""UNREADY independent metadata post for actual complete current B six-phase aggregate.

No candidate/helper import, no scientific decoder, no SQL/native tree or numeric
JSONL parsing. Original Root0 / evidence child2 / FAILED are distinct facts.
The exact separate author core freeze is bound below; actual execution is still NULL.
"""
import argparse,hashlib,json,os,resource,shlex,shutil,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent;PACKAGE=BASE.parent
ROOT=Path('/Users/wen/spot')
AUTHOR='/root/b_capture_actual_post_source';EXECUTOR='/root/b2_build_source_peer'
EXPECTED_CORE_AUTHOR_FREEZE={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_B_complete_aggregate_host_source_v1_UNREADY/AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json', 'sha256': '310365e21a80af9a244bcb2c87c830fbe8a2b07f5a6b6aef5f9f63acb7bb4dc5', 'size_bytes': 21400, 'identity': [16777229, 50876614, 33188, 1, 21400, 1792063231881745025, 1792063231881745025]}
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(historical_native_RAM_bits_verified=False,original_XSM_memory_bits_verified=False,historical_unsaved_context_recovered=False,reaction_multiplicity_qualified=False,TRANC_semantics_qualified=False,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,AAA_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,physics_qualified=False)
START=time.monotonic()
def need(v,m):
 if type(v)is not bool or not v:raise RuntimeError(m)
def budget():
 need(time.monotonic()-START<600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<512*2**20,'metadata post stage600/SELF512')
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'exact ordinary owned current7')
 return q
def full(p):
 q=current(p);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==p['identity'],'opened7')
  while b:=f.read(2**20):h.update(b);n+=len(b);budget()
  need(ids(os.fstat(f.fileno()))==p['identity'],'EOF7')
 need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'blind whole-file SHA/length');current(p);return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(ids(os.fstat(f.fileno()))==ids(s),'opened new file7')
  while b:=f.read(2**20):h.update(b);budget()
  need(ids(os.fstat(f.fileno()))==ids(s),'new file EOF7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s));current(p);return p
def meta(p):
 need(p['size_bytes']<8*2**20,'only bounded control metadata8MiB is decoded')
 q=full(p);v=json.loads(q.read_bytes());full(p);return v
def genuine(v,key,p,field):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and json.loads(t['output'].strip().splitlines()[-1])[field]==p,'genuine closed typed0 and exact output artifact PF')
def current_role(p,build):
 budget();q=Path(p['path']);s=q.lstat()
 need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'same exact inherited current7 without old payload read')
 if p in build['readonly_system_SDK_header_pins']:
  root=Path(build['readonly_system_SDK_root']);rs=root.lstat()
  need(str(root)=='/Library/Developer/CommandLineTools/SDKs/MacOSX27.0.sdk'and stat.S_ISDIR(rs.st_mode)and rs.st_uid==0 and ids(rs)==build['readonly_system_SDK_root_identity']and not any(x.is_symlink()for x in(root,*root.parents))and str(q)in{str(root/'usr/include'/n)for n in('stdio.h','stdlib.h','stdint.h')}and s.st_uid==0 and s.st_nlink==1,'only frozen selected readonly SDK headers current7')
 elif p in build['readonly_system_tool_metadata_pins']:
  need(str(q)in('/bin/ps','/usr/sbin/lsof')and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicitly frozen readonly PS/lsof roles')
 elif p==build['C_compiler_pin']:
  need(str(q)=='/Library/Developer/CommandLineTools/usr/bin/clang'and s.st_uid==0 and s.st_nlink==1 and bool(s.st_mode&0o111),'only explicit frozen current readonly clang role')
 elif str(q)=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15':
  need(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and s.st_uid==os.getuid()and s.st_nlink==p['identity'][3]==2,'only original frozen gfortran link exception')
 else:need(s.st_uid==os.getuid()and s.st_nlink==1,'same owned ordinary inherited role')
def all_output_pins(out):
 rows=[]
 if not os.path.lexists(out):return rows
 need(out.is_dir()and not any(x.is_symlink()for x in(out,*out.parents)),'literal fresh aggregate output')
 for q in sorted(out.rglob('*')):
  s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no new output alias')
  if stat.S_ISREG(s.st_mode):p=pin(q);full(p);rows.append(p)
  else:need(stat.S_ISDIR(s.st_mode),'ordinary new output files/directories only')
 return rows
def counted_bytes(roots):
 total=0
 for value in roots:
  root=Path(value);need(root.is_absolute()and not any(x.is_symlink()for x in(root,*root.parents)),'literal counted root')
  if not os.path.lexists(root):continue
  need(root.is_dir(),'counted root directory')
  for q in root.rglob('*'):
   budget();s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no alias in full counted scope')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total
def unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
def saved_resources(v,roots,limit):
 h=v['original_history'];j=v['complete_joint']
 need(v['host_SELF_peak_bytes']<512*2**20 and 0<=v['whole_elapsed_seconds']<1800 and v['entire_aggregate_output_bytes']<limit and j['resource_roots']==roots,'actual original SELF/wall/own-stage bound and whole current root scope')
 need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['artifact_bytes']+v['explicit_external_metadata_bytes']+v['host_open_unlinked_bytes']<2*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'actual original history/cumulative/cold/metadata/free caps')
def save(report,source_limit,joint_existing=None):
 report.update(metadata_only=True,Source_author_task=AUTHOR,actual_executor_task=EXECUTOR,actual_post_not_executed_by_Source_author=True,reviewer_Source_pin=pin(Path(__file__).absolute()),helper_or_candidate_module_imported=False,Source_GEN_or_publication_executed=False,native_or_compiler_or_worker_executed=False,scientific_values_or_SQLite_or_native_XSM_or_context_body_decoded=False,original_collect_or_snapshot_pair_readback_repeated=False,historical_issue_records_modified=False,wall_seconds=time.monotonic()-START,**FALSE)
 raw=(json.dumps(report,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'post control report6MiB')
 need(counted_bytes([str(PACKAGE)])+len(raw)<source_limit,'entire Source/metadata bound including new post')
 if joint_existing is not None:need(joint_existing+len(raw)<2*2**30,'entire current cumulative2GiB including post')
 q=BASE/'REVIEW.json'
 with q.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 budget();print(json.dumps(dict(status=report['status'],review_pin=pin(q))),flush=True)
B55_SCHEMA='CURRENT_B55_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1'
B55_STATUS='PRIOR_ACTUAL_CURRENT_B55_OVERV_CONTROL_PREADMITTED_METADATA_ONLY'
ORIGINAL_ISSUE=dict(category='SOURCE_CONTEXT_NOT_SAVED',field='OVERV',
 reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',
 original_all370x8_words_compared=True,historical_machine_bit_replay=False)
B55_FALSE_KEYS=('physics_qualified','historical_machine_bit_replay','historical_native_RAM_bits_verified',
 'original_XSM_memory_bits_verified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete','A_control_reused')
def B55_closed(value,key,chunk,payload_key,expected):
 terminal=value[key]
 need(value['observed_closed']is True and type(value['original_integer_exit_code'])is int and value['original_integer_exit_code']==0 and type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None and terminal['chunk_id']==chunk,'genuine exact original closed typed0')
 need(json.loads(terminal['output'].strip().splitlines()[-1])[payload_key]==expected,'actual stdout binds exact fullPF')
def B55_admit(spec,binding,read):
 need(type(spec)is dict and spec['schema']==B55_SCHEMA and binding['state_order']==['B']and set(binding['states'])==set(binding['actual_context_states'])=={'B'},'current original B only; no A control or earlier B aggregate fiction')
 pins=spec['metadata_pins'];v={key:read(p)for key,p in pins.items()}
 plan=v['control_plan'];host=v['control_report'];post=v['control_post'];sf=v['control_source_freeze']
 B55_closed(v['control_returns'],'actual_terminal_return','02a5d8','report_pin',pins['control_report'])
 B55_closed(v['control_post_returns'],'actual_review_return','f10181','review_pin',pins['control_post'])
 need(v['control_returns']['actual_execution_permission_mode']=='require_escalated'and v['control_returns']['actual_retried']is False,'genuine original bounded B55 control once')
 need(host['schema']=='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1'and host['status']=='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['control_plan_pin']==pins['control_plan']and host['source_freeze_pin']==pins['control_source_freeze']and host['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted']is True,'actual B55 control closes original resources and retains Source issue history')
 need(post['schema']=='RECORDED_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B55_OVERV_THREE_STAGE0_2960_WORDS_MATCH_METADATA_ONLY_NO_PHYSICS_QUALIFICATION'and post['failure']is None and post['metadata_only']is True and post['actual_Root_tools_pin']==pins['control_returns']and post['actual_Host_report_pin']==pins['control_report']and post['Source_freeze_pin']==pins['control_source_freeze']and post['control_plan_pin']==pins['control_plan']and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_codes']==[0,0,0],'genuine independent current B55 actual post0 with three child0')
 need(sf['schema']=='CURRENT_B55_OVERV_CONTROL_SOURCE_ONLY_FREEZE_V1'and sf['control_plan_pin']==pins['control_plan']and sf['compiler_executed']is False and sf['native_executed']is False,'same frozen original B55 Source control')
 result=host['actual_control_results'];counts=dict(actual_current_energy_words_observed=371,actual_current_overv_words_compared=2960,actual_current_overv_groups=370,actual_current_overv_mixtures=8,actual_native_vs_integer_model_and_saved_word_mismatches=0,actual_constant64_words_compared=3,actual_constant64_word_mismatches=0)
 need(result==post['actual_control_results_metadata']and result['all_three_stages_PASS']is True and result['all_constant64_and_overv370x8_current_words_match']is True and result['original_whole_LIBDEN_procedure_executed']is False and post['actual_current_control_word_comparison_counts']==counts and all(type(result[k])is int and result[k]==x for k,x in counts.items()),'actual complete371/2960/3 constants and zero differences; no recomputation here')
 need(len(host['records'])==len(host['actual_watchdog_checks'])==3 and all(r['status']=='PASS'for r in host['records'])and all(type(w['actual_watchdog']['returncode'])is int and w['actual_watchdog']['returncode']==0 and w['actual_watchdog']['limit_failure']is None for w in host['actual_watchdog_checks']),'all three actual original stages closed0')
 for document in(host,post,result):need(all(document[k]is False for k in B55_FALSE_KEYS),'no historical/physics/A-reuse qualification')
 actual=binding['actual_context_states']['B'];pairs=actual['all_snapshot_pairs'];descriptor=plan['selected_actual_B55_snapshot_descriptor']
 wanted=dict(event=descriptor['event'],role=descriptor['role'],root_prefix=descriptor['root_prefix'],input_pin=descriptor['input_pin'],sqlite_pin=descriptor['paired_SQLite_pin'],native_pool_pin=descriptor['paired_original_pool_pin'])
 need(len(pairs)==8 and len(actual['complete_context_pins'])==55 and pairs[-1]==wanted and wanted['event']==55 and wanted['role']=='final-complete-micro'and wanted['root_prefix']==[]and descriptor['state']=='B'and binding['states']['B']==dict(sqlite_pin=wanted['sqlite_pin'],native_pool_pin=wanted['native_pool_pin']),'all8trees/55contexts and exact actual final B55 pair')
 need(host['selected_actual_B55_snapshot_descriptor']==post['selected_actual_B55_snapshot_descriptor']==descriptor and host['selected_actual_B55_SQL_pool_pair']==post['selected_actual_B55_SQL_pool_pair']==plan['selected_actual_B55_SQL_pool_pair']==binding['states']['B']and host['actual_B_extraction_report_pin']==post['actual_B_extraction_report_pin']==plan['actual_B_extraction_child_report_pin']==actual['actual_extraction_report_pin']and host['actual_B_manifest_pin']==post['actual_B_manifest_pin']==plan['actual_B_manifest_pin']==actual['actual_observation_manifest_pin']and host['actual_B_input_binding_pin']==post['actual_B_input_binding_pin']==plan['actual_B_input_binding_pin']==binding['current_B_case_input_binding_pin'],'control and aggregate consume this exact B input/extraction/manifest, not an A result')
 original=host['actual_bounded_input_evidence'];rows=original['actual_original_record_metadata'];expected=[(('ENERGY',),371)]+[(('MACROLIB','GROUP',g,'OVERV'),8)for g in range(1,371)]
 need(original==post['actual_bounded_input_evidence_metadata']and len(rows)==371 and original['actual_payload_bytes_read']==13324 and original['complete_SQLite_or_pool_body_EOF_repeated']is False and original['original_XSM_opened']is False,'actual bounded B55 input record metadata only')
 for row,(path,count)in zip(rows,expected):need(row['path']==list(path)and row['kind']==2 and row['declared_count']==row['original_word_count']==count and row['native_payload_end_byte']-row['native_payload_begin_byte']==count*4,'same whole original B ENERGY/OVERV metadata paths/types/shapes')
 arithmetic=v['original_arithmetic_Source_binding']
 need(arithmetic['schema']=='ORIGINAL_OVERV_MIXED_PRECISION_ARITHMETIC_SOURCE_BINDING_V1'and arithmetic['each_original_arithmetic_statement_once_in_control']is True and arithmetic['original_material_Source_not_modified']is True and arithmetic['original_LCMPUT_publication_replaced_only_by_control_word_observation']is True and arithmetic['not_an_original_whole_LIBDEN_invocation']is True and arithmetic['control_Source_pin']['sha256']==sf['control_Fortran_Source_pin']['sha256']==plan['control_Fortran_Source_pin']['sha256'],'original arithmetic Source reference only; no A actual control imported')
 return dict(schema=B55_SCHEMA,status=B55_STATUS,original_issue_fact=ORIGINAL_ISSUE,original_issue_fact_is_Source_mechanism_not_prior_B_measurement=True,prior_B_aggregate_executed=False,prior_B_issue_count=None,prior_B_issue_count_invented=False,issue_count_adjustment_performed=False,same_original_final_pair=wanted,original_energy_and_overv_record_metadata=rows,control_metadata_pins=pins,actual_current_control_word_comparison_counts=counts,A_control_reused=False,historical_machine_bit_replay=False,physics_qualified=False)

SCHEMA='CURRENT_B4_SPLIT1_PLUS3_EXACT_ARCHIVED_RETIRED_PRODUCT_ROLES_ADMISSION_V2'
ROLE_KEYS={
 'member0_restore':('Root_report_pin','Root_tools_pin','post_pin','post_tools_pin'),
 'exact2_recovery':('receipt_pin','Root_tools_pin','post_pin','post_tools_pin','plan_pin','inherited_archive_binding_pin'),
 'complete4_archive':('Root_report_pin','Root_tools_pin','child_report_pin','index_pin','post_pin','post_tools_pin'),
 'remaining3_retirement':('receipt_pin','Root_tools_pin','post_pin','post_tools_pin')}
def document(v,schema,status):
 need(v['schema']==schema and v['status']==status and v['failure']is None,'exact actual schema/status/failure; no generic PASS')
def closed(v,key,chunk,field,expected):
 r=v[key]
 need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and r.get('session_id')is None and type(chunk)is str and r['chunk_id']==chunk,'exact genuine closed typed0 return')
 need(json.loads(r['output'].strip().splitlines()[-1])[field]==expected,'genuine stdout exact metadata PF')
def at(v,path):
 need(type(path)is list and len(path)>0 and all(type(k)in(str,int)for k in path),'explicit audited metadata key/index path')
 for k in path:v=v[k]
 return v
def metadata_pins(spec,require_complete=True):
 need(type(spec)is dict and spec['schema']==SCHEMA,'explicit split1+3 lifecycle')
 rows=[spec['actual_B_capture_manifest_pin'],spec['member0_complete_entry_pin']]
 entries=spec['ordered_exact4_current_entry_pins']
 if entries is None:need(require_complete is False,'future four durable entry PFs still NULL')
 else:need(type(entries)is list and len(entries)==4,'explicit complete4 entry PF list');rows+=entries
 for phase,keys in ROLE_KEYS.items():
  stage=spec[phase];need(type(stage)is dict,'explicit phase roles')
  for key in keys:
   p=stage[key]
   if p is None:need(require_complete is False,'future archive/remaining3 real PF still NULL')
   else:need(type(p)is dict,'exact metadata PF');rows.append(p)
 return rows
def known_first_original(spec,original,read):
 m=spec['member0_restore'];mr=read(m['Root_report_pin']);mt=read(m['Root_tools_pin']);mp=read(m['post_pin']);mpt=read(m['post_tools_pin'])
 closed(mt,'actual_terminal_return','5826fd','report_pin',m['Root_report_pin']);closed(mpt,'actual_review_return','9345ca','review_pin',m['post_pin'])
 document(mr,'ROOT_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1','PASS_CURRENT_B4_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY')
 document(mp,'RECORDED_CURRENT_B4_MEMBER0_INDEPENDENT_RESTORE_BYTE_CONTROL_METADATA_POSTVERIFY_V1','PASS_ACTUAL_ROOT_MEMBER0_STREAMED_ORIGINAL_SHA_LENGTH_CLOSED0_METADATA_ONLY_ALL4_REMAINS_FAILED')
 gz=spec['member0_complete_gzip_pin'];ep=spec['member0_complete_entry_pin']
 need(mp['actual_member0_Root_report_pin']==m['Root_report_pin']and mp['actual_Root_tools_pin']==m['Root_tools_pin']and mp['actual_child_integer_exit_code']is None and mp['actual_member0_children_started']==0,'same genuine Root-only member0 post0; no invented child0')
 need(mr['original_member0_saved_full_pin']==mp['original_member0_saved_full_pin']==original[0]and mr['complete_member0_gzip_pin']==mp['complete_member0_gzip_pin']==gz and mr['retained_member0_entry_pin']==mp['retained_member0_entry_pin']==ep,'same exact member0/gzip/entry')
 need(mr['streamed_complete_member0_verified']is True and mp['Root_actual_complete_member0_stream_verified']is True and mr['streamed_decompressed_SHA']==mp['actual_streamed_decompressed_SHA']==original[0]['sha256']and type(mr['streamed_decompressed_length'])is int and mr['streamed_decompressed_length']==mp['actual_streamed_decompressed_length']==original[0]['size_bytes'],'actual independent complete restoration SHA/length; never replayed here')
 need(mp['original_failed_Root_integer_exit_code']==1 and mp['original_failed_child_integer_exit_code']==1 and mp['original_limited_failure_post_recorded_child_codes']==[]and mp['all4_archive_complete']is False,'old all4 Root1/child1/post0[] preserved')
 e=spec['exact2_recovery'];rr=read(e['receipt_pin']);rt=read(e['Root_tools_pin']);rp=read(e['post_pin']);rpt=read(e['post_tools_pin'])
 closed(rt,'actual_terminal_return','78ceda','receipt_pin',e['receipt_pin']);closed(rpt,'actual_review_return','7b7ebe','review_pin',e['post_pin'])
 document(rr,'CURRENT_B4_EXACT2_PARTIAL_ARCHIVE_RECOVERY_RECEIPT_V1','RETIRED_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED')
 document(rp,'CURRENT_B4_EXACT2_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1','PASS_ACTUAL_CURRENT_B4_EXACT2_RECOVERY_COMPLETE_RESULT_BYTES_PRESERVED_METADATA_ONLY')
 need(rp['actual_execution_receipt_pin']==e['receipt_pin']and rp['actual_Root_tools_pin']==e['Root_tools_pin']and rp['metadata_only']is True and rp['actual_Root_integer_exit_code']==0 and rp['files_deleted']is True and rp['files_deleted_by_post']is False,'actual exact2 Root0 and independent post0')
 need(rr['plan_pin']==e['plan_pin'],'explicit same exact2 plan role');plan=read(e['plan_pin'])
 need(plan['inherited_complete_archive_plan_pin']==e['inherited_archive_binding_pin'],'explicit same inherited archive binding role');oldarchive=read(e['inherited_archive_binding_pin'])
 need(oldarchive['all4_product_pins']==original and plan['actual_single_member_verification_closure_pins']==dict(Root_report=m['Root_report_pin'],Root_tools=m['Root_tools_pin'],post=m['post_pin'],post_tools=m['post_tools_pin']),'same original4 and actual independent member0 proof')
 partial=spec['historical_incomplete_partial001_pin'];exact2=[original[0],partial]
 need(rr['actual_released_pins']==rp['actual_released_pins']==rr['exact_target_pins']==plan['exact_target_pins']==exact2 and type(rr['actual_released_bytes'])is int and rr['actual_released_bytes']==rp['actual_released_bytes']==sum(p['size_bytes']for p in exact2)==101693287,'exact2 is one original plus one fragment, not two original products')
 need(partial['path']==str(Path(oldarchive['planned_actual_output_root'])/'archives/001_u.asc.gz')and partial['size_bytes']==25099039 and partial['path']not in{p['path']for p in original},'fragment explicit role excluded from original4')
 need(rp['historical_original_member0_full_pin']==original[0]and rp['retained_complete_member0_gzip_pin']==gz and rp['retained_member0_entry_pin']==ep and rp['complete_result_member0_bytes_preserved']is True and rp['exact_two_targets_absent_verified_twice']is True and rp['all4_archive_complete']is False and rp['original_failure_post_recorded_child_codes']==[],'exact first original retired; complete saved member0 and historical failure retained')
 need(spec['first_retired_original_product_pins']==[original[0]]and spec['remaining3_original_product_pins']==original[1:]and not os.path.lexists(original[0]['path'])and not os.path.lexists(partial['path']),'only explicit proven first original and exact fragment absent')
 return dict(original1=[original[0]],fragment=partial,gzip0=gz,entry0=ep)
def archived_original4(spec,original,first,read):
 a=spec['complete4_archive'];p=a['actual_role_projection'];need(type(p)is dict,'archivev2 projection remains NULL until actual closure')
 h=read(a['Root_report_pin']);raw=read(a['Root_tools_pin']);child=read(a['child_report_pin']);index=read(a['index_pin']);post=read(a['post_pin']);pt=read(a['post_tools_pin'])
 for v,which,artifact in((raw,'Root_return','Root_report_pin'),(pt,'post_return','post_pin')):
  x=p[which];closed(v,x['return_field'],x['genuine_terminal_chunk_id'],x['output_artifact_field'],a[artifact])
 document(h,'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REUSE_MEMBER0_GUARDED_HOST_REPORT_V2','ACTUAL_CURRENT_B4_ALL_PRODUCTS_ARCHIVE_REUSE_MEMBER0_CLOSED0_ONE_RETIRED_THREE_LIVE')
 document(child,'ACTUAL_CURRENT_B4_SERIAL_LOSSLESS_ARCHIVE_REUSE_MEMBER0_REPORT_V2','ALL4_COMPLETE_B_PRODUCT_BYTE_PROOF_CLOSED0_ONE_RETIRED_THREE_LIVE')
 need(h['actual_child_receipt']['report_pin']==a['child_report_pin']and child['index_pin']==a['index_pin']and h['archive_complete']is True and h['final_report_resource_check_passed']is True and h['retired_original_product_pins']==child['retired_original_product_pins']==[original[0]]and h['live_original_product_pins']==child['live_original_product_pins']==original[1:],'actual Host/child explicitly one retired plus three live at archive time')
 need(child['completed_count']==4 and child['newly_archived_count']==3 and child['reused_complete_archive_count']==1 and index['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V2'and index['status']=='ALL4_COMPLETE_B_PRODUCTS_BYTE_PROOF_CLOSED_ONE_RETIRED_THREE_LIVE'and index['retired_original_product_pins']==[original[0]]and index['live_original_product_pins']==original[1:],'complete4 index is reused1 plus new3')
 entries=index['entries'];need(len(entries)==4 and [e['original_plain_full_pin']for e in entries]==original,'ordered original4 exact manifest index')
 compressed=[e['compressed_archive_full_pin']for e in entries];entrypins=[e['entry_pin']for e in entries]
 need(spec['ordered_exact4_current_entry_pins']==entrypins and len({v['path']for v in entrypins})==4 and entrypins[0]==first['entry0'],'all four durable entry files explicitly preserved in index order')
 need(len({v['path']for v in compressed})==4 and spec['ordered_exact4_current_archive_pins']==compressed and compressed[0]==first['gzip0']and index['reused_member0_gzip_pin']==first['gzip0']and index['reused_member0_entry_pin']==first['entry0'],'all four current gzip PFs and old gzip0/entry0 retained exactly')
 for e,o in zip(entries,original):
  need(e['compression_input_SHA']==e['streamed_decompressed_SHA']==o['sha256']and type(e['compression_input_length'])is int and e['compression_input_length']==e['streamed_decompressed_length']==o['size_bytes']and e['exact_original_plain_bytes_recoverable']is True,'all four recorded original whole-byte SHA/length proofs')
 need(entries[0]['reused_complete_archive_from_failed_v1']is True and entries[0]['original_plain_preserved']is False and entries[0]['entry_pin']==first['entry0']and entries[0]['actual_exact2_cleanup_execution_receipt_pin']==spec['exact2_recovery']['receipt_pin'],'entry0 explicit reused archive after original0 retirement')
 pp=p['post'];document(post,pp['schema'],pp['status'])
 need(post['metadata_only']is True and at(post,pp['Root_report_pin_path'])==a['Root_report_pin']and at(post,pp['Root_tools_pin_path'])==a['Root_tools_pin']and at(post,pp['child_report_pin_path'])==a['child_report_pin']and at(post,pp['index_pin_path'])==a['index_pin']and at(post,pp['all4_complete_byte_proofs_verified_path'])is True,'independent archive post0 same Host/child/index and full4 byte-proof facts')
 return compressed,entrypins
def remaining3_closed(spec,original,compressed,read):
 a=spec['remaining3_retirement'];p=a['actual_role_projection'];need(type(p)is dict,'remaining3 actual projection remains NULL until closure')
 r=read(a['receipt_pin']);rt=read(a['Root_tools_pin']);post=read(a['post_pin']);pt=read(a['post_tools_pin'])
 for v,which,artifact in((rt,'Root_return','receipt_pin'),(pt,'post_return','post_pin')):
  x=p[which];closed(v,x['return_field'],x['genuine_terminal_chunk_id'],x['output_artifact_field'],a[artifact])
 rp=p['receipt'];pp=p['post'];document(r,rp['schema'],rp['status']);document(post,pp['schema'],pp['status'])
 need(post['metadata_only']is True and at(post,pp['receipt_pin_path'])==a['receipt_pin']and at(post,pp['Root_tools_pin_path'])==a['Root_tools_pin'],'future independent post0 same remaining3 Root receipt/tools')
 released=at(r,rp['released_pins_path'])
 need(released==at(post,pp['released_pins_path'])==original[1:]and len(released)==len({v['path']for v in released})==3 and at(r,rp['released_bytes_path'])==at(post,pp['released_bytes_path'])==sum(v['size_bytes']for v in original[1:]),'only remaining3 exact original PFs actually retired')
 need(at(r,rp['archive_index_pin_path'])==at(post,pp['archive_index_pin_path'])==spec['complete4_archive']['index_pin']and at(r,rp['retained_archive_pins_path'])==at(post,pp['retained_archive_pins_path'])==compressed,'remaining3 retirement consumes same full4 index and preserves all four archives')
 return released
def B4_admit(request,read,current):
 spec=request['exact_B4_product_lifecycle_binding'];need(type(spec)is dict and spec['schema']==SCHEMA,'explicit split1+3 lifecycle binding required')
 metadata_pins(spec,True)
 m=read(spec['actual_B_capture_manifest_pin']);original=m['states']['B']['actual_material_product_pins']
 need(m['state_order']==['B']and set(m['states'])=={'B'}and m['actual_B_observation_executed']is True and m['actual_A_observation_executed']is False and spec['actual_B_capture_manifest_pin']==request['actual_observation_manifest_pin'],'same genuine B-only manifest')
 need(len(original)==len({p['path']for p in original})==4 and [Path(p['path']).name for p in original]==['m.xsm','u.asc','a.asc','t.asc']and spec['ordered_exact4_historical_product_pins']==original,'only original4 complete products; not context/snapshot/pool or fragment roles')
 first=known_first_original(spec,original,read);compressed,entrypins=archived_original4(spec,original,first,read);rest=remaining3_closed(spec,original,compressed,read)
 union=first['original1']+rest
 need(union==original and len({v['path']for v in union})==4 and first['fragment']['path']not in{v['path']for v in union},'strict original1+remaining3 fullPF union exactly original4; fragment never counted')
 retired={v['path']for v in union};need(all(not os.path.lexists(x)for x in retired),'only proven original4 historical names absent')
 need(not retired&{v['path']for v in request['complete_input_pins']+request['explicit_cumulative_metadata_file_pins']},'historical original4 never ordinary live pins')
 pairs=request['aggregation_binding']['actual_context_states']['B']['all_snapshot_pairs'];contexts=request['aggregation_binding']['actual_context_states']['B']['complete_context_pins']
 protected=[v for row in pairs for v in(row['input_pin'],row['sqlite_pin'],row['native_pool_pin'])]+contexts
 need(len(pairs)==8 and len(contexts)==55 and not(retired|{first['fragment']['path']})&{v['path']for v in protected},'complete8 native/SQL/pool pairs and55contexts remain live; no generic missing skip')
 for v in compressed+entrypins+[spec['complete4_archive']['index_pin']]+protected:current(v)
 return dict(schema=SCHEMA,exact_four_historical_fullPFs_preserved=original,exact_four_current_archive_pins=compressed,exact_four_current_entry_pins=entrypins,first_retired_original_product_pins=first['original1'],remaining3_retired_original_product_pins=rest,explicit1_plus3_union_exactly_original4=True,partial_fragment_excluded_from_original4=True,retired_paths_exactly_absent=True,all8_native_tree_SQL_pool_pairs_and55_contexts_retained=True,scientific_arrays_recomputed=False)

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for n in('Root-tools-pin','Host-pin','executor-task-name'):ap.add_argument('--'+n,required=True)
 a=ap.parse_args();need(a.executor_task_name==EXECUTOR and a.executor_task_name!=AUTHOR and not os.path.lexists(BASE/'REVIEW.json'),'independent exact executor and immutable once-only metadata post')
 pRoot=json.loads(a.Root_tools_pin);pHost=json.loads(a.Host_pin);raw=meta(pRoot);host=None if pHost is None else meta(pHost);actual=raw['actual_terminal_return']
 need(raw['observed_closed']is True and type(raw['original_integer_exit_code'])is int and type(actual['exit_code'])is int and actual['exit_code']==raw['original_integer_exit_code']and actual.get('session_id')is None and raw['actual_execution_permission_mode']=='require_escalated'and raw['actual_retried']is False,'genuine observed closed Root integer and original permission/no retry')
 code=raw['original_integer_exit_code'];plan_pin=pin(PACKAGE/'PLAN.json')if host is None else host['control_plan_pin'];plan=meta(plan_pin);out=Path(plan['planned_actual_output_root']);roots=plan['complete_joint_roots'];limit=plan['bounded_new_aggregate_output_reservation_bytes'];source_limit=plan['bounded_new_Source_metadata_reservation_bytes']
 need(plan['schema']=='CURRENT_B_COMPLETE_AGGREGATE_SOURCE_ONLY_PLAN_V1'and plan['only_current_stage']=='aggregate'and type(limit)is int and limit==320*2**20 and source_limit==16*2**20 and plan['original_caps']==CAPS and plan['future_stage_budget_added_to_this_stage']is False,'actual aggregate-only320MiB/Source16 and original full caps from real plan')
 need(roots[-1]==str(out)and out.is_absolute(),'literal new owning aggregate root')
 if pHost is not None:need(pHost['path']==str(out/'Root_actual_current_B_complete_aggregate_summary.json')and host['schema']=='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_GUARDED_ROOT_REPORT_V1','actual emitted owning aggregate Host role')
 newpins=all_output_pins(out);table={p['path']:p for p in newpins};ownbytes=sum(p['size_bytes']for p in newpins)
 if code!=0:
  codes=[];observed_report=None
  if host is not None and host['actual_watchdog_full_pin']is not None:
   w=meta(host['actual_watchdog_full_pin']);need(w==host['actual_watchdog']and type(w['returncode'])is int,'only genuinely saved child code; no Root-to-child inference');codes.append(w['returncode'])
  if host is not None and host['actual_child_report_pin']is not None:observed_report=meta(host['actual_child_report_pin'])
  report=dict(schema='CURRENT_B_COMPLETE_AGGREGATE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1',status='PASS_FAILURE_FACTS_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_Host_status=None if host is None else host['status'],actual_Host_failure=None if host is None else host['failure'],actual_stage_records=None if host is None else host['records'],actual_original_runner_error=None if host is None else host['original_runner_error'],actual_recorded_child_integer_exit_codes=codes,actual_saved_child_evidence_metadata=observed_report,absent_child_code_invented=False,child_code_inferred_from_Root_return=False,new_partial_output_blind_fullEOF_twice_pins=newpins,complete_aggregate_or_source_gap0_inferred=False,control_plan_pin=plan_pin)
  save(report,source_limit);return
 need(host is not None,'Root0 requires genuine emitted Host report PF');genuine(raw,'actual_terminal_return',pHost,'report_pin');stdout=json.loads(actual['output'].strip().splitlines()[-1])
 need(type(stdout['actual_child_evidence_only_integer_exit_code'])is int and stdout['actual_child_evidence_only_integer_exit_code']==2 and stdout['original_runner_FAILED_record_preserved']is True,'actual Root stdout intentionally preserves evidence child2/FAILED')
 need(host['status']=='ACTUAL_CURRENT_B_COMPLETE_AGGREGATE_EVIDENCE_CHILD2_CLOSED_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['operation']=='aggregate'and type(host['actual_child_integer_exit_code'])is int and host['actual_child_integer_exit_code']==2 and host['actual_intentional_exit2_normal_closure']is True and host['final_report_resource_check_passed']is True and host['original_caps']==CAPS and host['original_guard_class']=='OwnRSSSerialExecutor'and host['original_guard_MRO_unchanged']is True and host['current_source_control_bound']is True and host['B_six_phase_construction_completed']is True,'actual original Root0 closure only with original engineering child2 and unchanged owning guard')
 sf=meta(host['source_freeze_pin']);hf=meta(host['host_freeze_pin']);core=meta(EXPECTED_CORE_AUTHOR_FREEZE);ready_pin=pin(PACKAGE/'SOURCE_REVIEW_READY.json');ready=meta(ready_pin);cli_pin=pin(PACKAGE/'FINAL_ROOT_REVIEWABLE_CLI.json');cli=meta(cli_pin)
 need(core['Source_only_frozen_before_Root_generation']is True and core['whole_Source_file_pins']==sf['complete_source_file_pins']and core['native_or_compiler_executed_by_author']is False and core['Source_preparer_or_publisher_executed_by_author']is False and len(sf['complete_source_file_pins'])==15,'exact final complete15 Source author freeze, no author business execution')
 need(sf['schema']=='COMPLETE_CURRENT_B_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1'and sf['source_only']is True and sf['candidate_executed']is False and hf['schema']=='CURRENT_B_COMPLETE_AGGREGATE_HOST_FREEZE_V1'and hf['selected_source_freeze_pin']==host['source_freeze_pin']and hf['source_only']is True and hf['decoder_executed']is False and ready['schema']=='CURRENT_B_COMPLETE_AGGREGATE_SOURCE_REVIEW_READY_V1'and ready['source_only']is True and sf['control_plan_pin']==plan_pin==ready['control_plan_pin']and sf['complete_source_file_pins']==ready['complete_source_file_pins']and hf['host_source_pin']==ready['host_source_pin']and hf['contract_Source_pin']==ready['contract_Source_pin']and hf['original_caps']==CAPS,'same exact complete Source/host/contract/plan publication')
 peer=meta(sf['independent_Source_review_pin']);pt=meta(sf['independent_Source_review_tools_pin']);gt=meta(sf['Root_Source_generation_true_tools_pin']);genuine(pt,'actual_review_return',sf['independent_Source_review_pin'],'review_pin');genuine(gt,'actual_Source_preparation_return',ready_pin,'ready_pin')
 need(peer['source_only']is True and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_AGGREGATE'and peer['failure']is None and peer['control_plan_pin']==plan_pin and peer['complete_source_file_pins']==sf['complete_source_file_pins'],'genuine same-round independent complete aggregate Source review0')
 for p in sf['complete_source_file_pins']:full(p);full(p)
 need(cli['schema']=='CURRENT_B_COMPLETE_AGGREGATE_FINAL_REVIEWABLE_ROOT_CLI_V1'and raw['exact_executed_command']==cli['command']and shlex.split(cli['command'])==cli['argv']and len(cli['argv'])==24 and cli['source_freeze_pin']==host['source_freeze_pin']and cli['host_freeze_pin']==host['host_freeze_pin']and cli['Root_actual_exec_command_sandbox_permissions_required']==hf['Root_actual_exec_command_sandbox_permissions_required']=='require_escalated','exact original published Root CLI command string and24argv, no reconstructed environment alias')
 latest=meta(plan['latest_complete_plan_pin']);need(host['complete_joint_roots']==roots==latest['complete_joint_roots']+[str(out)]and len(roots)==len(set(roots))and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y)and any(PACKAGE.is_relative_to(Path(x))for x in roots[:-1]),'entire dynamic then-latest74 prefix plus one counted aggregate root, no root count substitution')
 requestpin=host['actual_execution_request_pin'];request=meta(requestpin);manifest=meta(host['actual_observation_manifest_pin']);binding=meta(host['current_B_case_input_binding_pin']);state=manifest['states']['B'];build=meta(plan['original_guard_build_plan_pin']);capture=meta(plan['actual_capture_Host_report_pin']);ep=meta(plan['actual_B_extraction_post_pin']);extract=meta(plan['actual_B_extraction_report_pin'])
 need(request['schema']=='CURRENT_B_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1'and request['operation']=='aggregate'and request['state_order']==['B']and request['original_caps']==CAPS and request['complete_source_freeze_pin']==host['source_freeze_pin']and request['joint_archive_roots']==roots and request['output_directory']==str(out/'evidence/aggregate')and request['owning_host_output_directory']==str(out)and request['actual_observation_manifest_pin']==host['actual_observation_manifest_pin']==plan['actual_observation_manifest_pin']and request['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']==plan['current_B_case_input_binding_pin']and request['actual_extraction_independent_review_pin']==plan['actual_B_extraction_post_pin']==host['actual_B_extraction_post_pin']and host['actual_B_extraction_report_pin']==plan['actual_B_extraction_report_pin'],'exact actual aggregate request/current B input/extraction/manifest/owning root')
 need(manifest['state_order']==['B']and set(manifest['states'])=={'B'}and manifest['actual_B_observation_executed']is True and manifest['actual_A_observation_executed']is False and manifest['library_copy_created']is False and state==dict(capture['actual_B_state'],actual_owning_report_pin=plan['actual_capture_Host_report_pin']),'complete genuine current B capture, not an A relabelling')
 actual_binding=request['aggregation_binding'];ctx=actual_binding['actual_context_states']['B'];contexts=ctx['complete_context_pins'];pairs=ctx['all_snapshot_pairs'];final=pairs[-1]
 need(actual_binding['state_order']==['B']and actual_binding['Source_route']==dict(ITSTMP=0,historical_call_proved=False)and actual_binding['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']and contexts==ep['complete_context_pins']==state['complete_context_pins']and pairs==ep['all_snapshot_pairs']and len(contexts)==55 and len(pairs)==8 and len(extract['context_states']['B'])==55 and len(extract['states']['B'])==8 and ep['actual_Root_integer_exit_code']==0 and ep['actual_child_integer_exit_code']==2 and ep['actual_extraction_report_pin']==plan['actual_B_extraction_report_pin']and ep['all_original_snapshot_and_context_pins_verified']is True and final['event']==55 and final['role']=='final-complete-micro'and actual_binding['states']['B']==dict(sqlite_pin=final['sqlite_pin'],native_pool_pin=final['native_pool_pin']),'all actual55 contexts/eight saved input SQL-pool pairs and exact final B55, no scope reduction')
 coveragepin=host['actual_coverage_contract_pin'];coverage=meta(coveragepin);need(ctx['actual_extraction_coverage_contract_pin']==coveragepin and coverage['schema']=='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1'and coverage['all_original_snapshot_pairs_saved']is True and coverage['states']['B']==dict(all_snapshot_pairs=pairs,complete_context_pins=contexts)and coverage['actual_extraction_report_pin']==plan['actual_B_extraction_report_pin']and coverage['actual_observation_manifest_pin']==host['actual_observation_manifest_pin']and coverage['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']and coverage['independent_actual_review_pin']==plan['actual_B_extraction_post_pin']and coverage['actual_closed_extraction_receipt_independently_reviewed']is True and coverage['new_qualification_sha256']is None,'same actual immutable Root-reviewed complete extraction coverage')
 need(len(host['records'])==1,'one actual aggregate child, no retry');record=host['records'][0];w=host['actual_watchdog']
 need(record['status']=='FAILED'and record['error']==host['original_runner_error']=='own-child stage failed; no retry'and 'resource_after'not in record and type(w['returncode'])is int and w['returncode']==2 and w['command']==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600,'genuine original evidence child2/FAILED/error and absent resource_after/RSS/wall/liveness preserved')
 need(host['actual_watchdog_full_pin']['path']==str(out/(record['label']+'.watchdog.json'))and host['actual_log_full_pin']['path']==str(out/(record['label']+'.log'))and meta(host['actual_watchdog_full_pin'])==w,'record.label exact watchdog/log and saved watchdog bytes')
 command=record['command'];claim=meta(pin(PACKAGE/'ROOT_EXECUTION_CLAIM_RECEIPT.json'));need(len(command)==10 and command[1:4]==['-B',str(PACKAGE/'current_B_material_lineage_evidence.UNREADY.py'),'aggregate']and command[4]=='--request-pin'and json.loads(command[5])==requestpin and command[6:9]==['--output-dir',request['output_directory'],'--expected-parent-pid']and command[9]==str(claim['Root_PID']),'exact actual aggregate child command/request and sole owning Root PID')
 logpath=full(host['actual_log_full_pin']);need(logpath.stat().st_size<8*2**20,'bounded metadata child receipt log');lines=logpath.read_text().splitlines();need(len(lines)==1,'one complete actual child receipt without omitted warnings');receipt=json.loads(lines[0]);need(receipt==host['actual_complete_child_receipt']and receipt['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2'and receipt['report']==host['actual_child_report_pin'],'exact actual child receipt/report chain')
 reportpin=host['actual_child_report_pin'];child=meta(reportpin);need(reportpin['path']==str(out/'evidence/aggregate/ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json')and child['schema']=='ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'and child['status']=='ACTUAL_CURRENT_COMPLETE_ORIGINAL_MATH_CONSTRUCTION_EVIDENCE_ONLY_EXIT2'and child['error']is None and child['state_order']==['B']and len(child['states'])==1 and child['states'][0]['state']=='B'and child['current_case_spec_pin']==binding['current_case_spec_pin']and child['current_B_case_input_binding_pin']==host['current_B_case_input_binding_pin']and child['complete_source_freeze_pin']==host['source_freeze_pin']and child['actual_extraction_independent_review_pin']==plan['actual_B_extraction_post_pin']and child['original_caps']==CAPS and child['all_complete_state_scope_retained']is True,'complete current B original-math engineering evidence, no copied prior A counts')
 facts=child['states'][0];phases=facts['phase_results'];counters={k:facts[k]for k in('all_original_records','complete_MACROLIB_records','complete_source_field_comparisons','compared_known_elements','all_mismatching_elements','all_context_or_operand_issues','unknown_macro_producers','original_context_event_count','all_original_snapshot_count')}
 need(all(type(v)is int and v>=0 for v in counters.values())and facts['complete_source_field_comparisons']>0 and facts['compared_known_elements']>0 and facts['original_context_event_count']==len(contexts)and facts['all_original_snapshot_count']==len(pairs)and facts['all_mismatching_elements']==facts['all_context_or_operand_issues']==facts['unknown_macro_producers']==0,'actual complete positive field/known-element counts and zero mismatch/issues/unknown required by genuine Root success; no count prefill')
 need([p['phase']for p in phases]==['scattering','scalar','fission','extras','overv_fallback','metadata']and all(p['computation_finished']is True for p in phases)and facts['all_original_native_records_and_bytes_preserved']is True and facts['all_complete_orders_preserved']is True and facts['all_missing_fields_not_zero_filled']is True and facts['full_output_scope_retained_even_on_failure']is True and facts['all_state_databases_and_pool_closed_before_next_state']is True,'all six original phases and complete original record/type/order/byte scope retained')
 state_report_pin=table[str(out/'evidence/aggregate/B/ACTUAL_COMPLETE_STATE_CONSTRUCTION_REPORT.json')];need(meta(state_report_pin)==facts,'same durable state report and child states[0] metadata')
 for p in facts['complete_output_file_pins']:need(table[p['path']]==p and Path(p['path']).parent==out/'evidence/aggregate/B','all complete per-state new artifacts match independent blindSHA2 and exact owning scope')
 need(request['current_B55_OVERV_control_binding']==plan['current_B55_OVERV_control_binding']==host['actual_B55_control_binding']and request['exact_B4_product_lifecycle_binding']==plan['exact_B4_product_lifecycle_binding']==host['actual_B4_lifecycle_binding'],'same actual B55 and strictsplit1+3 B4 metadata gates consumed by Host and child')
 b55=B55_admit(request['current_B55_OVERV_control_binding'],actual_binding,meta);need(child['current_OVERV_control_admission']==facts['current_OVERV_control_admission']==b55 and b55['actual_current_control_word_comparison_counts']['actual_current_overv_words_compared']==2960,'same genuine prior B55 word controls consumed at exact final B55 pair, no repeated arithmetic')
 life=B4_admit(request,meta,current);need(life['explicit1_plus3_union_exactly_original4']is True and life['partial_fragment_excluded_from_original4']is True and life['all8_native_tree_SQL_pool_pairs_and55_contexts_retained']is True and life['retired_paths_exactly_absent']is True,'strict original1 plus remaining3 equals original4, partial is not a product; four gzip/entry/index retained')
 for item in(host,request,child,b55):need(item['prior_B_aggregate_executed']is False and item['prior_B_issue_count']is None and item['issue_count_adjustment_performed']is False,'first B aggregate, no invented prior B issue1 or counter subtraction')
 for _ in range(2):
  for p in host['fixed_current_pins']+request['complete_input_pins']:current_role(p,build)
  for p in hf['explicit_cumulative_metadata_file_pins']+plan['inherited_metadata_current7_pins']:current_role(p,build)
  for p in plan['existing_actual_A_prior_issue_reports_current7_only_pins']:current(p)
 need(ownbytes<limit,'entire actual aggregate output below full planned320MiB cap')
 saved_resources(host['resources_before'],roots,limit);saved_resources(host['resources_after'],roots,limit)
 before=host['resources_before'];existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes'];reservation=host['actual_aggregate_only_stage_reservation'];need(existing+limit+source_limit<2*2**30 and reservation==request['stage_reservation_binding']and reservation['complete_joint_roots']==roots and reservation['original_caps']==CAPS and reservation['stage_output_reservations']==dict(aggregate=limit)and reservation['new_Source_metadata_reservation_bytes']==source_limit and reservation['existing_measured_total_bytes']==existing and reservation['only_current_stage']=='aggregate'and reservation['other_stages_not_reserved_or_reduced']is True,'actual complete aggregate-only stage reservation fits whole original ledger, no scope shrink or budget reset')
 joint=counted_bytes(roots);extra=sum(p['size_bytes']for p in hf['explicit_cumulative_metadata_file_pins']if not any(Path(p['path']).is_relative_to(Path(r))for r in roots));unlinked=unlinked_bytes();need(joint+extra+unlinked<2*2**30 and shutil.disk_usage(ROOT).free-20971764748-2*2**30>=8*2**30,'current full original cumulative/free/cold reserve includes final Host/report and post metadata')
 for item in(host,child,receipt,facts):
  for k in FALSE:
   if k in item:need(item[k]is False,'engineering construction evidence cannot mint physical/reaction/historical/AAA/ABA/goal qualification')
 need(child['complete_final_construction_qualified']is False and child['new_aggregation_qualification_sha256']is None and child['actual_scientific_qualification_sha256']is None,'engineering source construction evidence only, no scientific qualification')
 for p in [pHost,reportpin,requestpin,coveragepin,host['actual_watchdog_full_pin'],host['actual_log_full_pin'],state_report_pin]:need(table[p['path']]==p,'all actual aggregate metadata and output artifacts blind matched')
 report=dict(schema='RECORDED_CURRENT_B_COMPLETE_SIXPHASE_AGGREGATE_METADATA_POSTVERIFY_V1',status='PASS_ACTUAL_CURRENT_B_FULL8_SNAPSHOT55_CONTEXT_SIXPHASE_CONSTRUCTION_EVIDENCE_CHILD2_METADATA_ONLY',failure=None,actual_Root_tools_pin=pRoot,actual_Host_report_pin=pHost,actual_Root_integer_exit_code=code,actual_child_integer_exit_code=w['returncode'],actual_child_report_pin=reportpin,actual_state_report_pin=state_report_pin,actual_original_runner_record=record,actual_original_runner_error=host['original_runner_error'],original_FAILED_error2_record_retained=True,actual_record_resource_after_absent_preserved=True,actual_intentional_exit2_normal_closure=True,actual_stage_watchdog_pin=host['actual_watchdog_full_pin'],actual_stage_log_pin=host['actual_log_full_pin'],actual_stage_watchdog=w,actual_six_phase_results=phases,actual_engine_reported_counters=counters,actual_compared_source_fields=facts['complete_source_field_comparisons'],actual_compared_known_elements=facts['compared_known_elements'],actual_context_or_operand_issues=facts['all_context_or_operand_issues'],actual_all_mismatch_elements=facts['all_mismatching_elements'],actual_unknown_macro_producers=facts['unknown_macro_producers'],actual_snapshot_pair_count=len(pairs),actual_context_event_count=len(contexts),all_snapshot_pairs=pairs,complete_context_pins=contexts,actual_B55_current_control_admission_metadata=b55,actual_B4_split1_plus3_exact4_lifecycle_metadata=life,prior_B_aggregate_executed=False,prior_B_issue_count=None,issue_count_adjustment_performed=False,prior_B_issue_count_invented=False,actual_B_six_phase_engine_evidence_completed=True,old_A_issue_history_current7_only_retained_pins=plan['existing_actual_A_prior_issue_reports_current7_only_pins'],all_new_output_blind_fullEOF_SHA_current7_twice_pins=newpins,actual_new_output_logical_bytes=ownbytes,actual_stage_hard_output_bound_from_plan_bytes=limit,actual_Source_metadata_bound_from_plan_bytes=source_limit,old_scientific_payload_current7_only=True,old_scientific_payload_body_opened=False,old_scientific_payload_SHA_recomputed=False,new_JSONL_values_decoded=False,new_numerical_values_recomputed=False,known_producer_count_field_absent_not_fabricated=True,complete_joint_roots=roots,current_joint_bytes=joint,current_external_metadata_bytes=extra,current_post_open_unlinked_bytes=unlinked,original_caps=CAPS,original_host_resources_before=host['resources_before'],original_host_resources_after=host['resources_after'],actual_Host_final_report_resource_check_passed=host['final_report_resource_check_passed'],control_plan_pin=plan_pin,Source_freeze_pin=host['source_freeze_pin'],Host_freeze_pin=host['host_freeze_pin'],actual_execution_request_pin=requestpin,actual_published_CLI_pin=cli_pin,actual_Source_peer_pin=sf['independent_Source_review_pin'],actual_Source_peer_tools_pin=sf['independent_Source_review_tools_pin'],actual_Root_Source_generation_tools_pin=sf['Root_Source_generation_true_tools_pin'],core_Source_author_freeze_pin=EXPECTED_CORE_AUTHOR_FREEZE)
 save(report,source_limit,joint+extra+unlinked)
if __name__=='__main__':main()
