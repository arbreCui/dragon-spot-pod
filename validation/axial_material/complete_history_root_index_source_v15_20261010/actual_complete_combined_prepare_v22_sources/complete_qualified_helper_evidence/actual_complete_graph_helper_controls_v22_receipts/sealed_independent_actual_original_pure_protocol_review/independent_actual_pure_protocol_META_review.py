#!/usr/bin/env python3
"""Saved pure protocol Source/META audit; no helper/guard/driver execution."""
import ast
import hashlib
import json
import os
import pathlib
import stat
import struct
import sys

HERE=pathlib.Path(__file__).parent
B=pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
D=B/'actual_complete_graph_helper_controls_v22_sources'
E=B/'actual_complete_graph_helper_controls_v22_receipts'
H=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-host-v22-20261010')
O=pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-private-owner-namespace-helper-controls-v22-20261010')
CHECKS=[];READS=[]
def check(name,ok,details=None):
 row={'check':name,'PASS':bool(ok)}
 if details is not None:row['details']=details
 CHECKS.append(row)
def id7(p):
 s=pathlib.Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full_pin(path,expected=None,sha=None):
 p=pathlib.Path(path);before=id7(p);check('regular single-link finite Source/META '+str(p),stat.S_ISREG(before[2]) and before[3]==1)
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   h.update(chunk);n+=len(chunk)
  s=os.fstat(f.fileno());check('descriptor stable through full EOF '+str(p),[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before)
 actual={'path':str(p),'sha256':h.hexdigest(),'identity':id7(p),'size_bytes':n}
 check('full EOF byte count and7ID stable '+str(p),actual['identity']==before and n==before[4])
 if expected is not None:
  check('exact saved full SHA7ID '+str(p),all(actual[k]==expected[k] for k in ('path','sha256','identity')))
  if 'size_bytes'in expected:check('explicit saved full size '+str(p),actual['size_bytes']==expected['size_bytes'])
 if sha is not None:check('Root exact terminal/META SHA '+str(p),actual['sha256']==sha)
 READS.append(actual);return actual
def meta(p,limit=8*1024*1024):
 p=pathlib.Path(p);check('bounded explicit saved META decode '+str(p),p.stat().st_size<=limit)
 if p.stat().st_size>limit:raise ValueError('META too large for decoding')
 return json.loads(p.read_bytes())
def norm(p):return {k:p[k] for k in ('path','sha256','identity')}
def value_signature(v):
 t=type(v)
 if t is dict:return ['dict',[[value_signature(k),value_signature(x)] for k,x in v.items()]]
 if t is list:return ['list',[value_signature(x) for x in v]]
 if t is float:return ['float',struct.pack('>d',v).hex()]
 return [t.__name__,v]
def exact(a,b):return value_signature(a)==value_signature(b)
def tree(root):
 files={};dirs={};links={};root=pathlib.Path(root)
 for current,ds,fs in os.walk(root,followlinks=False):
  current=pathlib.Path(current);dirs[current.relative_to(root).as_posix()]=id7(current)
  for name in ds[:]:
   p=current/name
   if p.is_symlink():links[p.relative_to(root).as_posix()]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)};ds.remove(name)
  for name in fs:
   p=current/name;relative=p.relative_to(root).as_posix()
   if p.is_symlink():links[relative]={'path':str(p),'identity':id7(p),'target_text':os.readlink(p)}
   else:files[relative]=id7(p)
 return files,dirs,links

terminal_pin=full_pin(E/'Root_actual_pure_protocol_tool_terminal_return.json',sha='12d8bbdef3cd59c2f9889d507cf8e5e646f37f4d7e0df1649381373c82100e78')
summary_pin=full_pin(E/'Root_actual_pure_protocol_summary.json',sha='f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4')
manifest_pin=full_pin(E/'Root_actual_pure_protocol_namespace_manifest.json',sha='9d8453f1aefcc25ae029d5d0d7a8e1622ccac0c322556528326d79c06871123c')
terminal=meta(terminal_pin['path']);summary=meta(summary_pin['path']);manifest=meta(manifest_pin['path'])
t=terminal['terminal_tool_return']
check('genuine Root pure6f6847 strict integer0 closed no session',terminal['schema']=='ROOT_V22_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1' and type(t['exit_code'])is int and t['exit_code']==0 and t['chunk_id']=='6f6847' and 'session_id'not in t and terminal['closed']is True and terminal['actual_tool_terminal_return_observed']is True and terminal['initial_tool_return']['session_id']==74949 and terminal['subsequent_actual_tool_observations'][-1]==t and terminal['session_repolled_after_close']is False)
check('summary exact actual closed terminal and Source metadata scope',summary['schema']=='ROOT_V22_ACTUAL_COMPLETE_QUALIFICATION_SUMMARY_V1' and summary['status']=='ACTUAL_EXIT0_CLOSED_COMPLETE_PURE_CONTROLS_SAVED_REVIEW_REQUIRED' and summary['terminal_chunk_id']=='6f6847' and type(summary['actual_Root_exit_code'])is int and summary['actual_Root_exit_code']==0 and summary['closed']is True and norm(summary['actual_external_Root_terminal'])==norm(terminal_pin) and norm(summary['complete_namespace_manifest'])==norm(manifest_pin))
check('manifest finite inventory complete four roots',manifest['schema']=='ROOT_V22_COMPLETE_QUALIFICATION_FINITE_NAMESPACE_V1' and set(manifest['complete_namespaces'])=={'D','H','O','E_pre_summary'})
snapshots=[];regular_DHO=0;link_DHO=0
later_E={'Root_actual_pure_protocol_summary.json','Root_actual_pure_protocol_namespace_manifest.json'}
for label,ns in manifest['complete_namespaces'].items():
 root=pathlib.Path(ns['root']);files,dirs,links=tree(root)
 check(label+' literal correct root',root=={'D':D,'H':H,'O':O,'E_pre_summary':E}[label])
 expected_files=set(ns['files'])|(later_E if label=='E_pre_summary' else set())
 check(label+' all original entries and no cropped hidden files',set(files)==expected_files and set(dirs)==set(ns['directories']) and links==ns['symlinks'])
 check(label+' full saved entry counts',ns['file_count']==len(ns['files']) and ns['directory_count']==len(ns['directories']) and ns['symlink_count']==len(ns['symlinks']))
 for rel,pin in ns['files'].items():
  check(label+' root-relative saved path '+rel,pathlib.Path(pin['path'])==root/rel);full_pin(pin['path'],pin)
 for rel,identity in ns['directories'].items():
  if label=='E_pre_summary' and rel=='.':check('E directory honest append boundary not immutable forever',dirs[rel]!=identity and dirs[rel][:3]==identity[:3],{'before_summary_manifest':identity,'current_after_append':dirs[rel]})
  else:check(label+' entire directory7ID unchanged '+rel,dirs[rel]==identity)
 if label!='E_pre_summary':regular_DHO+=sum(x[4] for x in files.values());link_DHO+=sum(x['identity'][4] for x in links.values())
 snapshots.append({'label':label,'root':str(root),'regular_files':{r:ns['files'].get(r) for r in files},'directories':dirs,'symlinks':links,'regular_file_count':len(files),'directory_count':len(dirs)})
check('all complete Source and pure result exact counts',[(len(manifest['complete_namespaces'][k]['files']),len(manifest['complete_namespaces'][k]['directories']),len(manifest['complete_namespaces'][k]['symlinks'])) for k in ('D','H','O','E_pre_summary')]==[(61,6,0),(5,4,0),(33,4,2),(7,1,0)])
check('two real fixture aliases exact link bytes and7ID',manifest['complete_namespaces']['O']['symlinks']=={'fixture/file_alias.txt':{'path':str(O/'fixture/file_alias.txt'),'identity':id7(O/'fixture/file_alias.txt'),'target_text':'0_code_environment.txt'},'fixture/sealed/alias.txt':{'path':str(O/'fixture/sealed/alias.txt'),'identity':id7(O/'fixture/sealed/alias.txt'),'target_text':'subdir/owned.txt'}})
freeze=meta(summary['source_namespace_freeze']['path']);full_pin(summary['source_namespace_freeze']['path'],summary['source_namespace_freeze'])
check('Source D61 files/6 full directory7ID freeze exact, no append',freeze['schema']=='ROOT_V22_FINAL_COMPLETE_QUALIFICATION_SOURCE_FREEZE_V1' and freeze['source_root']==str(D) and freeze['complete_files']==manifest['complete_namespaces']['D']['files'] and freeze['complete_directories']==manifest['complete_namespaces']['D']['directories'] and freeze['no_Source_append_after_freeze']is True and summary['source_file_count']==61 and summary['all_source_files_before_after_exact']is True)
host=meta(H/'result.json');watch=meta(H/'run/admit.watchdog.json');child_stdout=meta(H/'run/admit.log');parent_stdout=meta(E/'parent_stdout.log');report=meta(O/'ACTUAL_REPORT.json');stages=meta(H/'GRAPH_PROTOCOL_CONTROLS/stages.json')
for label in ('actual_host_result','actual_control_report','actual_watchdog','actual_control_child_merged_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr'):full_pin(summary[label]['path'],summary[label])
check('normal host actual result and exact pure schema/status',host['schema']=='AXMAT_V22_GENUINE_PURE_GRAPH_PROTOCOL_CONTROLS_HOST_V1' and host['status']=='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' and norm(parent_stdout['actual_host_result'])==norm(summary['actual_host_result']) and norm(parent_stdout['actual_admission_stdout'])==norm(summary['actual_control_child_merged_stdout_stderr']) and parent_stdout['actual_external_Root_terminal_required']is True)
check('actual pure report Source status label honest, no Q from UNREADY label',report['schema']=='AXMAT_ROOT_BOUNDED_PURE_HELPER_CONTROLS_V16' and report['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION' and report['source_status']=='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS' and type(report['actual_success_pins'])is dict and child_stdout['status']==report['status'] and norm(child_stdout['report'])==norm(host['actual_control_report'])==norm(summary['actual_control_report']))
check('real watchdog same full saved object, int0 own child390.875 no limit cleanup',host['watchdog']==watch and type(watch['returncode'])is int and watch['returncode']==0 and type(watch['pid'])is int and watch['pid']==14844 and watch['sampled_peak_rss_mib']==390.875 and watch['rss_cap_mib']==512 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['command']==host['actual_canonical_command']==[str(pathlib.Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')),'-B',str(D/'pure_helper_controls.py'),'--output-dir',str(O)])
check('one genuine monitored admit stage and complete record',host['stage_records']==stages['stages'] and len(stages['stages'])==1 and stages['stages'][0]['label']=='run/admit' and stages['stages'][0]['status']=='PASS' and stages['stages'][0]['command']==watch['command'])
check('strict actual caps and measured time/memory all under',host['whole_seconds']==summary['whole_seconds']==17.33875858306419 and watch['elapsed_seconds']==summary['child_seconds']==15.59681337501388 and summary['sampled_peak_rss_mib']==390.875 and report['peak_rss_bytes']==409862144 and report['peak_rss_bytes']/2**20==390.875 and 0<report['elapsed_seconds']<=child_stdout['elapsed_seconds']<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stages['stages'][0]['wall_cap_seconds']<=60 and host['whole_seconds']<60)
check('all original caps unchanged across host/report/summary',[(host['whole_wall_cap_seconds'],host['stage_wall_cap_seconds'],host['rss_cap_mib'],host['archive_cap_bytes'],host['threads'],host['children_at_once'],host['retries'])]==[(60,60,512,67108864,1,1,0)] and report['caps']=={'children':1,'json_read_bytes':67108864,'output_bytes':67108864,'retries':0,'rss_bytes':536870912,'wall_seconds':60} and [(summary[k]) for k in ('whole_seconds_cap','stage_seconds_cap','rss_mib_cap','archive_bytes_cap','history_bytes_cap','free_bytes_floor','threads','children','retries')]==[60,60,512,67108864,103079215104,8589934592,1,1,0])
check('independent complete archive ledgers match conservative links honest',regular_DHO==61013090 and link_DHO==38 and host['archive_before_result_bytes']+summary['actual_host_result']['identity'][4]==regular_DHO and manifest['joint_D_H_O_bytes']==summary['joint_source_host_out_bytes']==regular_DHO+link_DHO==61013128 and regular_DHO+link_DHO<67108864,{'original_guard_regular_files_only_bytes':regular_DHO,'Root_META_conservative_link_text_bytes':link_DHO,'Root_META_regular_plus_symlink_text_bytes':regular_DHO+link_DHO})
check('71 full pinned current inputs:69 ordered host pins +2 original Source resources',len(host['input_sources'])==69 and summary['host_input_sources_and_original_helper_resource_factory_post_close_exact']==71)
for i,pin in enumerate(host['input_sources']):full_pin(pin['path'],pin);check('host ordered pin '+str(i)+' exact integer identity',all(type(x)is int for x in pin['identity']) and len(pin['identity'])==7)
for pin in (host['original_helper'],host['resource_factory']):full_pin(pin['path'],pin)
check('complete D61 inputs included without fixed crop',set(x['path'] for x in host['input_sources'][8:])==set(x['path'] for x in freeze['complete_files'].values()) and len(host['input_sources'][8:])==61)
check('real Root launch uses pinned approved host and all1threads',str(D/'pure_helper_controls_host.py')in terminal['actual_arguments']['cmd'] and all(k+'=1'in terminal['actual_arguments']['cmd'] for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')))
driver_source=(D/'pure_helper_controls.py').read_bytes();host_source=(D/'pure_helper_controls_host.py').read_bytes();ast.parse(driver_source);ast.parse(host_source)
check('installed driver/host exactly Source-qualified SHA',hashlib.sha256(driver_source).hexdigest()=='9ea06c8f44c637bd9cff6849ee4a0d55af88a3cb82d6aa3beb7684a94a8decb9' and hashlib.sha256(host_source).hexdigest()=='2d7bf5cc70e8cd061bcac683d27f33aea12f524b80079f7f5f9936534ef84e62')
for snippet in ['full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)',"Path(full.__file__).resolve()!=support.FULL","Path(production.__file__).resolve()!=support.PARENT",'helper.guard_admission(full)','type(runner) is not full.OwnRSSSerialExecutor','resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)']:
 check('unchanged genuine guard/MRO/resource Source '+snippet,snippet in host_source.decode())
for name in ('resources_before','resources_after'):
 resource=host[name];check('saved genuine full history/free metadata cap '+name,resource['min_free_bytes']==8589934592 and resource['artifact_budget_bytes']==103079215104 and resource['artifact_bytes']<103079215104 and resource['disk_free_bytes']>=8589934592 and resource['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and all(str(p)in resource['declared_resource_roots'] for p in (H,O,pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-admission-v15-20261010'),pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010'),pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-contiguous-flux-window-root-index-build-terminal-v15-20261010'))))

owner=report['private_owner_consume_controls'];check('new actual owner schema and summary full exact',owner['schema']=='AXMAT_V22_PRIVATE_OWNER_CONSUME_ACTUAL_CONTROL_V1' and owner['status']=='ACTUAL_PRIVATE_OWNER_CONTROLS_RETURNED_METADATA_ONLY' and exact(owner,summary['private_owner_consume_controls']))
positive=owner['positive_controls'];negative=owner['private_guard_rejections'];subtypes=owner['accepted_str_subclass_equivalence_controls'];partial=owner['partial_invalid_second_owner_rejections']
check('all4positive3reject2subtypes2invalidsecond complete and ordered',[x['case'] for x in positive]==['default_list','default_tuple','explicit_False_list','owned_builtin_list_True'] and [x['case'] for x in negative]==['nonbool_consume','tuple_True','list_subclass_True'] and [x['case'] for x in subtypes]==['plain_accepted_str','accepted_str_with_str_override'] and [x['case'] for x in partial]==['invalid_second_owner_default','invalid_second_owner_owned_True'])
baseline=positive[0]['expected_complete_descriptor_signature']
for case in positive:
 check('complete normalized full typed ordered descriptor signatures '+case['case'],case['full_normalized_descriptor_types_order_values_attrs_floatbits_equal_default']is True and exact(case['expected_complete_descriptor_signature'],case['actual_complete_descriptor_signature']) and exact(case['expected_complete_descriptor_signature'],baseline))
 check('complete default caller or exclusively-owned success clearing '+case['case'],case.get('caller_full_identity_type_order_value_attrs_floatbits_unchanged')is True if case['case']!='owned_builtin_list_True' else case['owned_list_completely_cleared_after_success']is True)
for case in negative:check('actual private flag/list rejection class/message/caller unchanged '+case['case'],case['class']=='InputGraphError' and case['message']=='private owner consume needs a bool and an exclusively owned builtin list' and case['caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True)
for case in subtypes:
 check('all accepted subtype value/type/order/attributes/floatbits '+case['case'],case['default_caller_full_identity_type_order_value_attrs_floatbits_unchanged']is True and case['owned_list_completely_cleared_after_success']is True and case['complete_normalized_descriptor_types_order_value_strattrs_floatbits_equal_default']is True and exact(case['expected_complete_descriptor_signature'],case['actual_complete_descriptor_signature']))
 wire=json.dumps(case['actual_complete_descriptor_signature']);check('subtype markers preserve all threefloat IEEE bit strings '+case['case'],all(struct.pack('>d',v).hex()in wire for v in (-0.0,1e-300,1.25)))
for case in partial:check('original invalid-second exact rejection '+case['case'],case['class']=='InputGraphError' and case['message']=='missing file owner')
for key in ('first_valid_slot_None_after_original_validate_and_append','invalid_second_slot_original_identity_and_value_unchanged','default_partial_caller_unchanged','original_owner_rejection_class_order_message_preserved','original_protocol_controls_fixtures_and_caps_unchanged','no_new_fixture_file_or_IO_created'):check('complete actual owner sequencing '+key,owner[key]is True)
check('new owner metadata cannot create qualification',owner['new_helper_qualification_created']is False and owner['business_or_science_qualification_created']is False)

fixture=meta(O/'small_fixture_controls.json');codecs=meta(O/'small_codec_and_rejection_controls.json')
check('original smallfixture summary exact complete projection',all(exact(fixture[k],v) for k,v in report['small_fixture'].items()) and exact(report['small_fixture'],summary['small_fixture']) and fixture['canonical_files']==11 and fixture['requirement_rows']==18 and len(fixture['all_nine_closure_categories'])==9 and len(fixture['complete_rejected_arguments'])==18 and len(fixture['rejections'])==37)
for key in ('caller_full_value_and_mutable_identity_preserved','complete_requirement_iterator_order_values_and_duplicate_edges_equal','duplicate_owner_descriptors_edges_and_optional_new_lists_preserved','fresh_graph_has_no_caller_mutable_container','producer_full_exact_values_types_order_floatbits','real_trace_attempt_multiplicity_and_extra_fields_preserved'):check('original fixture full requirement '+key,fixture[key]is True)
for i in range(18):
 a,b=fixture['rejections'][2*i:2*i+2];check('all18 original/fresh complete paired rejection '+str(i),a['case'].endswith(':original') and b['case']==a['case'][:-len(':original')]+':fresh' and a['class']==b['class']=='InputGraphError' and a['message']==b['message'])
check('original extra fresh consumer guard rejection present',fixture['rejections'][-1]['case']=='fresh_consumer_scope' and fixture['rejections'][-1]['class']=='InputGraphError')
accepted=fixture['accepted_str_subclass_equivalence_controls'];check('both original accepted subclass full checks retained',[x['case'] for x in accepted]==['plain_accepted_str','accepted_str_with_str_override'] and all(x['complete_builtin_output_values_types_order_floatbits_equal']is True and x['complete_caller_identity_type_order_value_attrs_floatbits_unchanged']is True for x in accepted))
check('original codec61 rejections + full malformed control inventory',len(codecs['rejections'])==report['small_codecs']['rejections']==61 and len(codecs['all_malformed_serializable_tables'])==37 and len(codecs['non_json_rejected_input_descriptions'])==6 and len(codecs['complete_trace_fixture'])==report['small_codecs']['accepted_trace_rows']==5 and all(x['class']=='InputGraphError' for x in codecs['rejections']) and exact(report['small_codecs'],summary['small_codecs']))
for key in ('all_default_inputs_unmodified','all_lossless_missing_null_order_type_floatbit_duplicate_controls','fresh_parsed_consume_arrays_released','ordinary_and_both_storage_strict_dispatches'):check('original codec complete success '+key,codecs[key]is True)
driver_ast=ast.parse(driver_source);run=next(n for n in driver_ast.body if isinstance(n,ast.FunctionDef) and n.name=='run');checkpoint_labels=[n.args[0].value for n in ast.walk(run) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='checkpoint' and n.args and isinstance(n.args[0],ast.Constant)]
check('five original complete pure checkpoints all actual',checkpoint_labels==[x['stage'] for x in report['stages']] and len(report['stages'])==5 and all(0<=x['elapsed_seconds']<60 and x['peak_rss_bytes']<=536870912 and x['owned_output_bytes']<=67108864 for x in report['stages']))
trace=report['full_new_creation_trace'];oldgraph=report['full_old_saved_graph'];original_meta=oldgraph['complete_original_metadata']
check('full63379 creationtrace all rows/attempts/columns/layouts retained',trace['full_record_count']==trace['table_rows']==summary['full_new_creation_trace_records']==63379 and trace['actual_attempt_count']==175886 and trace['subprocess_record_count']==0 and trace['table_columns']==10 and trace['table_layouts']==2 and trace['table_strings']==39287 and trace['original_insertion_order_compact_source']['size_bytes']==35211756 and all(trace[k]is True for k in ('default_source_nonmutation','exact_full_roundtrip','persisted_full_trace_exact_order_type_floatbit_inverse')))
for label,pin in [('full saved encoded trace',trace['encoded_artifact']),('full saved encoded graph',oldgraph['stored_wholegraph']),('unchanged input creationtrace metadata',trace['input']),('unchanged input originalgraph metadata',oldgraph['input'])]:full_pin(pin['path'],pin)
check('all full originalgraph normal parser metadata equality',exact(original_meta,oldgraph['normal_strict_file_entrance_full_semantics_and_counts']) and exact(original_meta,oldgraph['normal_strict_payload_entrance_full_semantics_and_counts']) and all(oldgraph[k]is True for k in ('full_default_roundtrip_exact','no_two_complete_decoded_graphs_between_strict_stages','old_read_trace_not_replaced_by_new_trace','original_legacy_semantic_sha_preserved')))
counts=original_meta['complete_counts'];check('complete originalgraph real fixed scope/counts retained',counts['canonical_files']==36776 and counts['requirements']==237767 and counts['owners']==4471 and counts['namespaces']==86 and counts['aliases']==186 and counts['read_trace_records']==62332 and counts['read_trace_attempts']==181554 and counts['subprocess_records']==0 and counts['absence_inputs']==449 and counts['new_paths']==counts['new_pins']==0 and counts['top_fields']==31 and len(original_meta['complete_closure_coverage'])==9)
check('actual pure successful pins bind entire artifacts exact',norm(report['actual_success_pins']['helper'])==norm(report['helper']) and norm(report['actual_success_pins']['encoded_new_trace'])==norm(trace['encoded_artifact']) and norm(report['actual_success_pins']['encoded_wholegraph'])==norm(oldgraph['stored_wholegraph']) and exact(report['helper'],summary['installed_helper']) and report['helper']['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c')
check('two complete original metadata input identities unchanged',len(report['saved_input_identity_before'])==len(report['saved_input_bytes_identity_after'])==2 and all(norm(a)==norm(b) for a,b in zip(report['saved_input_identity_before'],report['saved_input_bytes_identity_after'])))
for pin in report['saved_input_bytes_identity_after']:full_pin(pin['path'],pin)
check('honest mergedchild and separately original parent stderr scope',summary['separate_child_stderr_capture_verified']is False and summary['child_stdout_stderr_merge_is_original_normal_guard']is True and pathlib.Path(summary['actual_control_child_merged_stdout_stderr']['path'])==H/'run/admit.log' and pathlib.Path(summary['actual_external_parent_stderr']['path'])==E/'parent_stderr.log' and (E/'parent_stderr.log').stat().st_size==0)
check('no host profile or supervisor modification',host['profile_used']is False and host['supervisor_class_or_MRO_modified']is False)
check('pure pass only, no fullcurrentgraph/Q/build/Input/native/physics/AAA/ABA',summary['actual_pure_controls_pass']is True and summary['independent_saved_actual_review_pass']is False and summary['actual_new_helper_qualification_sha256']is None and all(summary[k]is False for k in ('actual_full_current_V20_graph_fresh_verifier_qualified','whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified')) and terminal['actual_new_helper_qualification_sha256']is None and all(terminal[k]is False for k in ('full_current_graph_fresh_verifier_qualified','complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')) and all(report[k]is False for k in ('business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted')) and all(host[k]is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))
for ns in snapshots:
 files,dirs,links=tree(ns['root']);check('all current scoped directory/symlink identities stable during peer '+ns['label'],dirs==ns['directories'] and links==ns['symlinks'])
result={'schema':'INDEPENDENT_V22_ACTUAL_PURE_PROTOCOL_SAVED_META_PEER_REVIEW_V1','scope':'READ_ONLY_FINITE_CURRENT_PURE_ARTIFACT_SOURCE_META_EOF_SHA7ID_ONLY','PASS':all(x['PASS'] for x in CHECKS),'check_count':len(CHECKS),'hard_blockers':[x for x in CHECKS if not x['PASS']],'checks':CHECKS,'complete_full_EOF_reads':READS,'complete_namespace_snapshots':snapshots,'actual_Root_pure_tool_receipt':terminal,'Root_summary_pin':summary_pin,'Root_namespace_manifest_pin':manifest_pin,'actual_watchdog':watch,'actual_host_whole_seconds':host['whole_seconds'],'pure_driver_peak_rss_bytes':report['peak_rss_bytes'],'original_and_new_complete_controls':{'original_fixture_rejections':37,'original_paired_fixture_rejection_cases':18,'original_codec_rejections':61,'original_subtype_controls':2,'new_owner_positive_controls':positive,'new_owner_guard_rejections':negative,'new_owner_subtypes':subtypes,'new_owner_invalid_second_rejections':partial,'five_original_pure_checkpoints':report['stages'],'complete_old_graph_counts':counts,'full_new_trace_records':63379},'Source_status_label_scope':'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS remains the original report metadata label; real purePASS follows the actual fixed Source/helper pins, all completed controls, real watched child and external Root int0 closed. It is never used as fullcurrentgraph qualification or Q.','archive_ledger_scope':{'original_normal_guard_regular_file_bytes':regular_DHO,'conservative_META_extra_symlink_literal_bytes':link_DHO,'Root_saved_META_total_DHO_bytes':regular_DHO+link_DHO,'joint_scope':['D','H','O'],'cap_bytes':67108864,'E_meta_append_after_namespace_snapshot_7_to_9_files':sorted(later_E)},'resource_scope':'Saved genuine resource metadata and exact Source pins verified; this peer did not walk broad historical ART or reexecute a live resource guard.','all_original_large_metadata_artifacts_fully_stream_hashed_without_API_or_decoder':True,'material_or_actual_numerical_payload_read_or_decoded':False,'helper_protocol_host_guard_driver_API_compile_or_numeric_executed_by_peer':False,'Root_original_Project_D_E_ART_or_TMP_Source_packages_mutated_by_peer':False,'old_closed_session_repolled':False,'pure_protocol_saved_evidence_independently_reviewed':True,'full_current_graph_verifier_qualified':False,'new_Q':None,'whole_build_INPUT_native_physics_AAA_ABA_goal_credit':False,'conclusion':'Actual complete pure helper protocol passed under the unchanged genuine supervisor/caps, with all old and new controls and complete Source freeze saved. Proceed only to the original complete current-graph verifier qualification; do not grant Q or build/Input/native/science credit yet.'}
raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();p=HERE/'INDEPENDENT_ACTUAL_PURE_PROTOCOL_META_REVIEW.json';p.write_bytes(raw);print(json.dumps({'status':'ACTUAL_COMPLETE_PURE_PROTOCOL_SAVED_META_PEER_PASS' if result['PASS'] else 'ACTUAL_COMPLETE_PURE_PROTOCOL_SAVED_META_PEER_BLOCKED','check_count':len(CHECKS),'hard_blocker_count':len(result['hard_blockers']),'review':{'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)},'actual_Root_terminal':'6f6847_int0closed','actual_ownwatch_peak_rss_mib':390.875,'original_guard_regular_DHO_bytes':regular_DHO,'conservative_META_symlink_DHO_bytes':regular_DHO+link_DHO,'full_current_graph_qualified':False,'new_Q':None,'no_science_or_native_credit':True}))
sys.exit(0 if result['PASS'] else 1)
