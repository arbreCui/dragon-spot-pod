"""Finite stdlib saved-META verification; never imports reviewed writer/helper/guard."""
from pathlib import Path
import ast,hashlib,json,stat,struct
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
HERE=Path(__file__).parent
checks=[]; observed={}; admission_inputs={}
def ck(name, ok):
 assert type(ok) is bool,name
 checks.append({'name':name,'PASS':ok})
 assert ok,name
def id7(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def full(p,expected=None,capture=False):
 p=Path(p);before=id7(p);ck('regular nonsymlink '+str(p),stat.S_ISREG(before[2]) and not p.is_symlink())
 h=hashlib.sha256();data=bytearray() if capture else None
 with p.open('rb') as f:
  while part:=f.read(1024*1024):
   h.update(part)
   if capture:data.extend(part)
 ck('full EOF stable '+str(p),id7(p)==before)
 item={'path':str(p),'sha256':h.hexdigest(),'size_bytes':before[4],'identity':before}
 if expected is not None:ck('exact full pin '+str(p),item==expected)
 if str(p) in observed:ck('consistent observed pin '+str(p),observed[str(p)]==item)
 observed[str(p)]=item
 return (bytes(data) if capture else None),item
def read(p,expected=None):
 raw,pin=full(p,expected,True)
 def pairs(items):
  d={}
  for k,v in items:assert k not in d;d[k]=v
  return d
 def bad(v):raise ValueError(v)
 return json.loads(raw,object_pairs_hook=pairs,parse_constant=bad),pin
def normalize(p):
 return {'path':p['path'],'sha256':p['sha256'],'size_bytes':p.get('identity',p.get('identity7'))[4],'identity':p.get('identity',p.get('identity7'))}
def add(p):
 v=normalize(p)
 if v['path'] in admission_inputs:ck('identical admission route pin '+v['path'],admission_inputs[v['path']]==v)
 admission_inputs[v['path']]=v
def sig(v):
 if type(v) is dict:return ('dict',tuple((sig(k),sig(x)) for k,x in v.items()))
 if type(v) is list:return ('list',tuple(sig(x) for x in v))
 if type(v) is float:return ('float',struct.pack('!d',v).hex())
 return (type(v).__name__,v)
def equal(name,a,b):ck(name,sig(a)==sig(b))
Qpath=B/'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json'
Q,Qpin=read(Qpath)
ck('fixed actual Q pin',Qpin=={'path':str(Qpath),'sha256':'89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816','size_bytes':448851,'identity':[16777229,49407444,33188,1,448851,1791605464130734338,1791605464130734338]})
E22b=B/'actual_joint_helper_admission_v22b_receipts';D22b=B/'actual_joint_helper_admission_v22b_sources'
terminal,terminal_pin=read(E22b/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json')
ck('actual Root metadata writer schema',terminal['schema']=='ROOT_V22B_ACTUAL_JOINT_HELPER_META_ADMISSION_WRITER_TOOL_TERMINAL_RETURN_V1')
ck('actual Root metadata writer closed observed',terminal['closed'] is True and terminal['actual_tool_return_observed'] is True and terminal['metadata_only'] is True and terminal['actual_Q_created'] is True)
tr=terminal['actual_tool_return']
ck('actual Root writer strict0 no session',tr['chunk_id']=='1b6bd5' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr)
out=json.loads(tr['output'])
equal('actual terminal direct Q pin',out['qualification'],Qpin)
ck('actual terminal173 and actual pure fresh terminals',out['unique_fresh_explicit_inputs']==173 and out['pure_Root_terminal']=='6f6847' and out['fresh_Root_terminal']=='57a6f5')
ck('actual Root business science flags false',terminal['helper_guard_API_or_numeric_business_executed'] is False and terminal['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False and out['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False)
ck('actual environment unsets optimize and only actual a9f writer',terminal['actual_arguments']['cmd'].startswith('env -u PYTHONOPTIMIZE ') and str(D22b/'write_actual_joint_helper_admission_v22b.READY.py') in terminal['actual_arguments']['cmd'])
F=Q['complete_current_graph_fresh_verifier']
pure,_=read(Q['actual_controls_summary']['path'],Q['actual_controls_summary'])
fresh,_=read(F['actual_controls_summary']['path'],F['actual_controls_summary'])
pp,_=read(Q['independent_actual_review']['path'],Q['independent_actual_review'])
fp,_=read(F['independent_actual_review']['path'],F['independent_actual_review'])
ps,_=read(Q['sealed_independent_pure_actual_review_manifest']['path'],Q['sealed_independent_pure_actual_review_manifest'])
fs,_=read(F['sealed_independent_actual_review_manifest']['path'],F['sealed_independent_actual_review_manifest'])
pure_report,_=read(Q['actual_control_report']['path'],Q['actual_control_report'])
fresh_report,_=read(F['actual_control_report']['path'],F['actual_control_report'])
fixture,_=read(Q['full_protocol_additional_complete_fixture_artifact']['path'],Q['full_protocol_additional_complete_fixture_artifact'])
small,_=read(Q['full_protocol_additional_complete_codec_artifact']['path'],Q['full_protocol_additional_complete_codec_artifact'])
ck('pure1084 actual pass',pp['PASS'] is True and pp['hard_blockers']==[] and type(pp['check_count']) is int and pp['check_count']==len(pp['checks'])==1084 and all(type(x['PASS']) is bool and x['PASS'] is True for x in pp['checks']))
ck('fresh686 actual pass',fp['PASS'] is True and fp['hard_blockers']==[] and type(fp['check_count']) is int and fp['check_count']==len(fp['checks'])==686 and all(type(x['PASS']) is bool and x['PASS'] is True for x in fp['checks']))
resolution=[]
for kind,peer,key,root,names in [
 ('pure',pp,'regular_files',B/'actual_complete_graph_helper_controls_v22_receipts',{'Root_actual_pure_protocol_namespace_manifest.json':'Root_namespace_manifest_pin','Root_actual_pure_protocol_summary.json':'Root_summary_pin'}),
 ('fresh',fp,'complete_regular_files',B/'actual_complete_graph_fresh_verifier_v22_receipts',{'Root_actual_fresh_verifier_namespace_manifest.json':'Root_namespace_manifest_pin','Root_actual_fresh_verifier_summary.json':'Root_summary_pin'}),
]:
 ck('all four complete snapshots '+kind,[s['label'] for s in peer['complete_namespace_snapshots']]==['D','H','O','E_pre_summary'])
 for s in peer['complete_namespace_snapshots']:
  nulls={name for name,v in s[key].items() if v is None}
  ck('original snapshot count '+kind+'/'+s['label'],len(s[key])==s['regular_file_count'] and len(s['directories'])==s['directory_count'])
  if s['label']=='E_pre_summary':ck('exact selfcapture null names/root '+kind,s['root']==str(root) and nulls==set(names))
  else:ck('other snapshot no null '+kind,not nulls)
  for name,v in s[key].items():
   if v is None:
    v=peer[names[name]]
    ck('selfcapture exact peer root/name '+kind+'/'+name,Path(v['path'])==Path(s['root'])/name)
    resolution.append({'kind':kind,'name':name,'postcapture_fullpin':normalize(v)})
   add(v)
for x in pp['complete_full_EOF_reads']+fp['complete_full_EOF_reads']+fp['unique_complete_fresh_rechecked_input_pins']:add(x)
for x in ps['complete_fresh_TMP_files_before_this_seal_and_future_actual_seal_receipt'].values():add(x)
for x in fs['all_fresh_TMP_files_before_this_seal_and_future_actual_seal_tool_receipt'].values():add(x)
for item in list(Q.values())+list(F.values()):
 if type(item) is dict and {'path','sha256','identity'}.issubset(item):add(item)
for x in F['complete_gzips'].values():add(x)
for doc in [pure,fresh]:
 for key in ['actual_external_Root_terminal','source_namespace_freeze','complete_namespace_manifest','actual_host_result','actual_control_report','actual_watchdog','actual_control_child_merged_stdout_stderr','actual_external_parent_stdout','actual_external_parent_stderr']:add(doc[key])
ck('independently complete exact173 admission routes',len(admission_inputs)==173)
for v in admission_inputs.values():full(v['path'],v)
ck('fixed pure actual summary SHA',Q['actual_controls_summary']['sha256']=='f03a8f32091134c24dbf77da9ec82c0582f3b16c6eaa1841df5934b37064c1a4')
ck('fixed fresh actual summary SHA',F['actual_controls_summary']['sha256']=='fb4ff68bbe2abc319b2e217279e4676327aa0b66ead1cb28fb8bbcb0882b7b6e')
ck('fixed actual qualified helper Source cf0',Q['helper']['sha256']=='cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c' and Q['helper']['size_bytes']==148965)
equal('complete fresh report retained in Root summary',fresh_report,fresh['complete_actual_report'])
equal('complete owner controls Root/report/Q',Q['private_owner_consume_controls'],pure_report['private_owner_consume_controls'])
equal('complete owner controls summary/report',pure['private_owner_consume_controls'],pure_report['private_owner_consume_controls'])
ck('whole fixture exact values types order floatbits',fixture['producer_full_exact_values_types_order_floatbits'] is True)
ck('all original pure stages count/order',[x['stage'] for x in pure_report['stages']]==['real_small_fixture_producer_equivalence_and_rejections','all_new_codecs_and_both_strict_entrances_small_controls','full_63379_creation_trace_roundtrip_and_stored_size','full_old_saved_graph_codec_and_two_normal_strict_entrances','all_original_saved_metadata_bytes_identity_unchanged'])
ck('all original rejection/paired/subtype counts',len(fixture['rejections'])==37 and len(fixture['complete_rejected_arguments'])==18 and len(small['rejections'])==61 and len(pure_report['small_fixture']['accepted_str_subclass_equivalence_controls'])==2)
ck('new private owner4+3+2+2 complete',len(Q['private_owner_consume_controls']['positive_controls'])==4 and len(Q['private_owner_consume_controls']['private_guard_rejections'])==3 and len(Q['private_owner_consume_controls']['accepted_str_subclass_equivalence_controls'])==2 and len(Q['private_owner_consume_controls']['partial_invalid_second_owner_rejections'])==2)
for scope in [pure,fresh]:
 ck('actual summary original honest pending-review flags',scope['independent_saved_actual_review_pass'] is False and scope['actual_new_helper_qualification_sha256'] is None)
 for key in ['whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified']:ck('actual summary no science '+scope['status']+'/'+key,scope[key] is False)
ck('fresh27 complete fields/4positive3reject',len(F['full_public_return_field_order'])==27 and F['private_positive_controls']==4 and F['private_reject_controls']==3)
equal('fresh all27 original order',F['full_public_return_field_order'],fresh_report['complete_return_fields_retained'])
equal('fresh full current graph metadata unchanged',F['full_current_graph_metadata'],fresh_report['independent_full_saved_graph_metadata'])
equal('actual complete37112 trace counts',F['complete_actual_unfiltered_read_trace_counts'],{'records':37112,'attempts':37112,'canonical_files':37111,'external_graph_reads':1,'no_subprocess_reexecuted':True})
ck('fresh complete graph scope none no new declaration',F['full_current_graph_metadata']['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and F['full_current_graph_metadata']['consumer_scope'] is None and F['full_current_graph_metadata']['newly_declared_input_paths']=={} and F['full_current_graph_metadata']['newly_declared_input_pins']=={})
equal('fresh peer all27 exact original report',fp['all27_return_fields'],fresh_report['complete_return_fields_retained'])
for k,v in F['complete_gzips'].items():
 equal('full normalized gzip original saved pin '+k,v,normalize(fresh_report[k]))
 ck('gzip full no filtering preserved '+k,fp['all_three_complete_gzip_pins'][k]['complete_JSON_wire_gzip_decompression_EOF_SHA_verified'] is True and fp['all_three_complete_gzip_pins'][k]['no_fields_or_records_filtered'] is True)
ck('three full gzips retained',list(F['complete_gzips'])==['expected_complete_return_contract','actual_complete_verifier_return','actual_complete_ReadOpenAudit_trace'])
for pinvalue,initial,session,closed,kind in [(Q['actual_root_terminal'],'86ab9d',74949,'6f6847','pure'),(F['actual_root_terminal'],'55ef8e',29568,'57a6f5','fresh')]:
 t,_=read(pinvalue['path'],pinvalue)
 ck('actual distinct terminal '+kind,t['initial_tool_return']['chunk_id']==initial and type(t['initial_tool_return']['session_id']) is int and t['initial_tool_return']['session_id']==session and t['terminal_tool_return']['chunk_id']==closed and type(t['terminal_tool_return']['exit_code']) is int and t['terminal_tool_return']['exit_code']==0 and 'session_id' not in t['terminal_tool_return'] and t['closed'] is True)
ck('pure full ledger strict scope',pp['archive_ledger_scope']['joint_scope']==['D','H','O'] and pp['archive_ledger_scope']['Root_saved_META_total_DHO_bytes']==61013128 and pp['archive_ledger_scope']['original_normal_guard_regular_file_bytes']==61013090 and pp['archive_ledger_scope']['conservative_META_extra_symlink_literal_bytes']==38)
ck('fresh saved originalHODE ledger scope',fp['original_archive_full_HODE_scope']['original_normal_guard_scope']==['H','O','D','E'])
for doc in [pure,fresh]:
 ck('all original host threads/children/retries/history/free',doc['threads']==doc['children']==1 and doc['retries']==0 and doc['history_bytes_cap']==96*2**30 and doc.get('free_bytes_floor',doc.get('min_free_bytes'))==8*2**30)
old=pure_report['full_old_saved_graph'];meta=old['complete_original_metadata'];trace=pure_report['full_new_creation_trace']
equal('old complete two original strict entrances',meta,old['normal_strict_file_entrance_full_semantics_and_counts'])
equal('old complete payload strict entrance',meta,old['normal_strict_payload_entrance_full_semantics_and_counts'])
protocol={'original_and_fresh_small_producer_values_types_order_floatbits_exact':True,'all_caller_mutable_identity_and_subtype_attributes_unchanged':True,'accepted_str_subtype_groups':2,'small_codec_rejections':pure_report['small_codecs']['rejections'],'complete_original_graph_counts':meta['complete_counts'],'complete_old_graph_two_normal_strict_entrances_exact':True,'complete_old_legacy_semantic_sha256':meta['legacy_semantic_sha256'],'complete_old_wire_content_sha256':meta['wire_content_sha256'],'complete_new_creation_trace_records':trace['full_record_count'],'complete_new_creation_trace_actual_attempts':trace['actual_attempt_count'],'new_creation_trace_not_substituted_into_old_graph':True,'full_json_types_order_floatbits_and_values_retained':True,'default_source_nonmutation':True}
equal('whole full_protocol constructor',Q['full_protocol'],protocol)
ck('complete original graph not replaced',protocol['complete_original_graph_counts']['canonical_files']==36776 and protocol['complete_original_graph_counts']['requirements']==237767 and protocol['complete_original_graph_counts']['read_trace_records']==62332 and protocol['complete_new_creation_trace_records']==63379 and protocol['complete_new_creation_trace_actual_attempts']==175886)
expected_measure={'whole_seconds':pure['whole_seconds'],'child_seconds':pure['child_seconds'],'sampled_peak_rss_mib':pure['sampled_peak_rss_mib'],'actual_final_host_out_source_bytes':pure['joint_source_host_out_bytes'],'original_normal_guard_regular_file_bytes':pp['archive_ledger_scope']['original_normal_guard_regular_file_bytes'],'conservative_META_extra_symlink_literal_bytes':pp['archive_ledger_scope']['conservative_META_extra_symlink_literal_bytes'],'regular_and_symlink_literal_ledgers_are_distinct':True,'old_complete_graph_stored_bytes':old['stored_wholegraph']['size_bytes'],'new_complete_trace_original_compact_bytes':trace['original_insertion_order_compact_source']['size_bytes'],'new_complete_trace_stored_bytes':trace['encoded_artifact']['size_bytes']}
equal('whole pure actual measurement constructor',Q['actual_measurement'],expected_measure)
caps={'whole_seconds':60,'stage_seconds':60,'rss_mib':512,'archive_bytes':64*2**20,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
equal('complete original60 caps',Q['original_caps'],caps)
fcaps={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_HOST_OUT_SOURCE_E_archive_bytes':64*2**20,'history_bytes':96*2**30,'free_bytes':8*2**30,'threads':1,'children':1,'retries':0}
equal('complete original1800/600 caps',F['original_caps'],fcaps)
current_joint=0
for root in [B/'actual_complete_graph_fresh_verifier_v22_sources',B/'actual_complete_graph_fresh_verifier_v22_receipts',ART/'axial-material-complete-graph-fresh-verifier-host-v22-20261010',ART/'axial-material-complete-graph-fresh-verifier-v22-20261010']:
 for p in root.rglob('*'):
  s=p.lstat();ck('finite original joint regular or directory '+str(p),stat.S_ISREG(s.st_mode) or stat.S_ISDIR(s.st_mode))
  if stat.S_ISREG(s.st_mode):current_joint+=s.st_size
fm={'whole_seconds':fresh['whole_seconds'],'child_seconds':fresh['child_seconds'],'sampled_peak_rss_mib':fresh['sampled_peak_rss_mib'],'driver_reported_own_peak_rss_mib':fp['driver_own_peak_rss_mib'],'sample_and_self_peaks_are_distinct':True,'joint_snapshot_plus_manifest_bytes_at_original_closeout':fp['original_archive_full_HODE_scope']['original_business_post_result_HODE_bytes'],'Root_saved_DHO_ledger_bytes_not_HODE_scope':fp['original_archive_full_HODE_scope']['Root_saved_DHO_ledger_bytes'],'saved_peer_full_HODE_bytes':fp['original_archive_full_HODE_scope']['peer_current_full_HODE_bytes'],'full_original_HODE_scope_preserved':True,'current_joint_regular_bytes_after_saved_peer_and_copy_receipts':current_joint}
equal('whole fresh distinct measurement constructor',F['actual_measurement'],fm)
ck('both actual limits preserved',expected_measure['whole_seconds']<60 and expected_measure['child_seconds']<60 and expected_measure['sampled_peak_rss_mib']<512 and expected_measure['actual_final_host_out_source_bytes']<64*2**20 and fm['whole_seconds']<1800 and fm['child_seconds']<600 and fm['sampled_peak_rss_mib']<512 and fm['driver_reported_own_peak_rss_mib']<512 and current_joint<64*2**20)
freeze,freeze_pin=read(E22b/'Root_final_v22b_META_writer_Source_freeze.json')
for rel,item in freeze['complete_files'].items():full(D22b/rel,item)
for rel,item in freeze['complete_directories'].items():ck('new fixed Source directory unchanged '+rel,id7(D22b/rel)==item)
writer_pin=freeze['complete_files']['write_actual_joint_helper_admission_v22b.READY.py']
ck('actual qualified writer Source a9fefd',writer_pin['sha256']=='a9fefd704170ce12cb68f329e75e3b4a015f665f7e8637abf1bb697437aa1c35')
raw,_=full(writer_pin['path'],writer_pin,True);wt=ast.parse(raw)
ck('17 Source functions retained no execution',len([x for x in wt.body if isinstance(x,ast.FunctionDef)])==17)
retention,retention_pin=read(E22b/'Root_complete_v22b_self_capture_Source_review_retention.json')
ck('complete Source peer retention6+1',retention['complete_original_member_count']==6 and len(retention['complete_original_members'])==6)
for row in retention['complete_original_members'].values():
 _,saved_pin=full(row['saved']['path'],row['saved'])
 ck('whole retained source-review bytes original SHA',saved_pin['sha256']==row['original']['sha256'] and saved_pin['size_bytes']==row['original']['size_bytes'])
full(retention['saved_actual_peer_seal_receipt']['path'],retention['saved_actual_peer_seal_receipt'])
source_review,_=read(retention['complete_original_members']['REVIEW.json']['saved']['path'],retention['complete_original_members']['REVIEW.json']['saved'])
ck('retained actual571 SourcePASS',source_review['PASS'] is True and source_review['SOURCE_PASS'] is True and source_review['check_count']==len(source_review['checks'])==571 and all(x['PASS'] is True for x in source_review['checks']))
ck('actual source qualified pin exact',source_review['corrected_writer']==writer_pin)
oldQ,oldQpin=read(B/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json')
ck('old jointQ31 top fields all retained',len(oldQ)==31 and set(oldQ).issubset(Q))
for name in ['full_protocol','actual_measurement','original_caps','complete_current_graph_fresh_verifier']:
 ck('old complete dictionary contract retained '+name,set(oldQ[name]).issubset(Q[name]))
equal('all original protocol field order',list(oldQ['full_protocol']),list(Q['full_protocol']))
equal('all original pure caps',oldQ['original_caps'],Q['original_caps'])
equal('all original fresh caps',oldQ['complete_current_graph_fresh_verifier']['original_caps'],F['original_caps'])
flags=['supervisor_class_or_MRO_modified','profile_used','fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified']
for k in flags:ck('Q software scope false '+k,Q[k] is False)
ck('Q exact actual source counts and legacy alias honesty',Q['pure_source_member_count']==pure['source_file_count']==61 and F['complete_source_member_count']==fresh['source_file_count']==13 and F['legacy_SOURCE33_key_is_compatibility_alias_not_V22_source_count'] is True)
ck('Q exact173 and META only',Q['Root_finite_joint_META_fresh_explicit_full_EOF_SHA7ID_verified_unique_input_count']==173 and Q['Root_finite_joint_META_only_no_project_API_or_numeric'] is True)
ck('whole current graph-only and protocol-only statuses',Q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_OWNER_NAMESPACE_HELPER_ACTUAL_JOINT_ADMISSION_V22' and Q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V22')
main_node=next(x for x in wt.body if isinstance(x,ast.FunctionDef) and x.name=='main')
admission_node=next(x.value for x in ast.walk(main_node) if isinstance(x,ast.Assign) and any(isinstance(n,ast.Name) and n.id=='admission' for n in x.targets))
source_top_keys=[ast.literal_eval(k) for k in admission_node.keys]
source_fresh_node=next(v for k,v in zip(admission_node.keys,admission_node.values) if ast.literal_eval(k)=='complete_current_graph_fresh_verifier')
source_fresh_keys=[ast.literal_eval(k) for k in source_fresh_node.keys]
equal('Q complete key order from original whole Source constructor',list(Q),source_top_keys)
equal('fresh complete key order from original whole Source constructor',list(F),source_fresh_keys)
def literals(node,actual,label):
 if isinstance(node,ast.Dict):
  equal('all original nested constructor keys '+label,list(actual),[ast.literal_eval(k) for k in node.keys])
  for k,v in zip(node.keys,node.values):literals(v,actual[ast.literal_eval(k)],label+'/'+str(ast.literal_eval(k)))
 elif isinstance(node,ast.Constant):equal('exact original constructor literal '+label,actual,ast.literal_eval(node))
literals(admission_node,Q,'Q')
for v in list(observed.values()):full(v['path'],v)
review={'schema':'INDEPENDENT_V22_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1','PASS':True,'hard_blockers':[],'check_count':len(checks),'checks':checks,'actual_Q':Qpin,'actual_Root_writer_terminal':terminal_pin,'actual_writer_Source':writer_pin,'actual_Source_review_retained_571PASS':retention_pin,'all173admission_input_fullpins':admission_inputs,'all173admission_inputs_count':173,'all_explicit_review_inputs':observed,'all_explicit_review_input_count':len(observed),'whole_original_contract_fields_preserved':True,'complete_Q_and_fresh_key_counts_and_order_from_original_whole_Source_constructor':{'top':len(source_top_keys),'fresh':len(source_fresh_keys)},'nested_constructor_types_order_values_floatbits_exactly_checked_against_original_saved_META':True,'four_original_self_capture_nulls_resolved_by_same_peer_postcapture_fullpins':resolution,'pure1084_and_fresh686_actual_saved_peer_PASS':True,'all_original_caps_preserved':True,'actual_Root_writer_closed_typed_exit0_only_stdlib_META':True,'helper_metadata_protocol_and_fresh_graph_metadata_verifier_qualified':True,'actual_whole_build_INPUT_native_physics_AAA_ABA_or_goal_qualified':False,'reviewer_writer_helper_guard_API_business_native_or_numeric_executed':False,'material_or_graph_or_gzip_payload_decoded_or_numeric_computed':False,'project_canonical_D_E_ART_or_original_files_modified':False,'prior_failed_writer_receipt_preserved_in_Source_review':True,'priorQ_used_only_for_contract_no_old_measurement_or_terminal_credit':True,'initial_reviewer_incorrect_nested_constructor_count_int1_preserved':True}
(HERE/'REVIEW.json').write_text(json.dumps(review,indent=2)+'\n')
(HERE/'REPORT.txt').write_text('PASS: actual Q 89d2f03c, actual Root writer1b6bd5 typed0 closed.\nIndependently reconstructed exactly173 full input-pin routes; all full EOF/SHA7ID checked twice.\nAll original31 top fields and original13 protocol/9 caps/22 fresh fields retained, new Q37/fresh26 complete; 27 refers to full public verifier return fields, distinct from nested Q fields. Actual pure1084 and fresh686 saved reviews bind distinct trials; new measurements and caps remain honest.\nFour original pre-summary selfcapture nulls are resolved via same-peer exact root/name postcapture fullpins. No field is omitted.\nSoftware helper metadata protocol/fresh verifier qualification only. Whole build/INPUT/native/AAA/ABA/physical balance remain false. No reviewed API or business code was run, no graph/material/gzip decoded, no project original written.\n')
print(json.dumps({'review_package':str(HERE),'PASS':True,'check_count':len(checks),'all173admission_inputs':True,'review_input_count':len(observed),'REVIEW_sha256':hashlib.sha256((HERE/'REVIEW.json').read_bytes()).hexdigest(),'actual_Q_sha256':Qpin['sha256'],'science_qualified':False}))

