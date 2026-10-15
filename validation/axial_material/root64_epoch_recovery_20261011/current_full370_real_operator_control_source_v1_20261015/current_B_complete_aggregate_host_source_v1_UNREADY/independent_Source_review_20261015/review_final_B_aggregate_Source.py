"""Independent Source/metadata/current7 review. No project imports or scientific IO."""
import ast,builtins,hashlib,json,os,stat,symtable
from pathlib import Path
D=Path(__file__).absolute().parent.parent
HERE=Path(__file__).absolute().parent
def need(v,m):
 if not v:raise RuntimeError(m)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p,owned=True):
 need(set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'typed complete PF')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'exact current7')
 if owned:need(s.st_uid==os.getuid()and s.st_nlink==1,'ordinary owned role')
def pin(q):
 q=Path(q);s=q.lstat();raw=q.read_bytes();need(ids(q.lstat())==ids(s),'stable own Source/metadata');return dict(path=str(q.absolute()),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(p):
 current(p);need(p['size_bytes']<8*2**20,'small metadata/Source only');raw=Path(p['path']).read_bytes();need(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata/Source complete SHA');current(p);return raw
def meta(p):return json.loads(read(p))
def truth(p,key,field,want,chunk=None):
 x=meta(p);r=x[key];need(x['observed_closed']is True and type(x['original_integer_exit_code'])is int and x['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0 and 'session_id'not in r and json.loads(r['output'].splitlines()[-1])[field]==want,'genuine closed typed0 exact PF')
 if chunk is not None:need(r['chunk_id']==chunk,'same recorded actual chunk')
 return x
def at(x,path):
 for k in path:x=x[k]
 return x
def main():
 need(not(HERE/'REVIEW.json').exists(),'review once')
 rp=pin(D/'SOURCE_REVIEW_READY.json');gp=pin(D/'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json');ap=pin(D/'AUTHOR_PRE_ROOT_GENERATION_SOURCE_FREEZE.json')
 need(rp['sha256']=='dc16fd2cfb60f36c9cd60049054f63bd44b2c6570920804953de43ef6e779b5c'and gp['sha256']=='b4ca2921d62518d223f8657d46a56bdfb0b04a04e01a79beb8d52c512d47db7c'and ap['sha256']=='310365e21a80af9a244bcb2c87c830fbe8a2b07f5a6b6aef5f9f63acb7bb4dc5','Root supplied final READY/GEN/author')
 ready=meta(rp);a=meta(ap);truth(gp,'actual_Source_preparation_return','ready_pin',rp,'71a908');pp=ready['control_plan_pin'];p=meta(pp);packet=meta(a['admission_packet_pin'])
 need(a['admission_packet_pin']['sha256']=='76fc51334c2bbfcfd963c75016c998a8e7ca0ee0abd69e720ccc10f497f331c0'and a['Source_only_frozen_before_Root_generation']is True and a['native_or_compiler_executed_by_author']is False and a['Source_preparer_or_publisher_executed_by_author']is False,'author frozen actual packet')
 need(all(p[k]==v for k,v in packet.items()if k!='schema'),'GEN only added Source facts; unchanged actual packet')
 sp=ready['complete_source_file_pins'];need(sp==a['whole_Source_file_pins']and len(sp)==15 and len({q['path']for q in sp})==15,'exact complete15 Source table');code={}
 for q in sp:
  text=read(q).decode();tree=ast.parse(text);t=symtable.symtable(text,q['path'],'exec');top=set(t.get_identifiers());unknown=set()
  def walk(s):
   for name in s.get_identifiers():
    y=s.lookup(name)
    if y.is_referenced()and y.is_global()and name not in top and name not in vars(builtins):unknown.add(name)
   for c in s.get_children():walk(c)
  walk(t);need(not unknown,'no unbound globals');code[Path(q['path']).name]=text
 inv=meta(a['previous_whole_Source_inverse_inventory_pin']);oldtable={Path(q['path']).name:q for q in inv['complete_current_Source_file_pins']}
 changed={'aggregate_Source_contract.UNREADY.py':'c5b31b083ab1ccd15f56a8100c84f2a42ede2042d20b03845591e2473e4622a0','current_B4_product_lifecycle_admission.UNREADY.py':'8b97e7b7123eebd6c47b13b955f36d4167fed6137fdcbadea2c0e42042fd6962','build_current_B_complete_aggregate_request.UNREADY.py':'371d2c334e59d2022855c62bd085ecf0d177a43eacabfe0a09e4af5e396f21b2'}
 for q in sp:need(q['sha256']==changed.get(Path(q['path']).name,oldtable.get(Path(q['path']).name,q)['sha256']),'unchanged pre-reviewed Source except exact3 metadata lifecycle changes')
 for kind,name,oldkey,editkey in [('engine','complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','original_engine_Source_pin','exact_engine_metadata_hook_edits'),('worker','current_B_material_lineage_evidence.UNREADY.py','original_B_extract_worker_Source_pin','exact_worker_metadata_control_lifecycle_edits')]:
  text=code[name]
  for row in reversed(inv[editkey]):need(text.count(row['after'])==1,'unique inverse metadata hook');text=text.replace(row['after'],row['before'],1)
  need(text.encode()==read(inv[oldkey]),'whole original engine/worker inverse')
 for row in inv['whole_original_decoder_adapter_and_B_binding_copy_pairs']:need(read(row['original_Source_pin'])==read(row['whole_copy_Source_pin']),'whole decoder/adapter/B-binding/capture Source unchanged')
 builder=ast.parse(code['build_current_B_complete_aggregate_request.UNREADY.py']);hosttree=ast.parse(code['run_guarded_current_B_complete_aggregate.UNREADY.py']);consumed={n.slice.value for n in ast.walk(builder)if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='inputs'and isinstance(n.slice,ast.Constant)};provided=set()
 for n in ast.walk(hosttree):
  if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='request_inputs'for t in n.targets):provided={k.arg for k in n.value.keywords}
 need(consumed==provided,'host complete builder inputs dict exactly matches actual signature')
 worker=code['current_B_material_lineage_evidence.UNREADY.py'];bt=ast.parse(worker);budget=next(n for n in bt.body if isinstance(n,ast.ClassDef)and n.name=='Budget');check=next(n for n in budget.body if isinstance(n,ast.FunctionDef)and n.name=='check');need(isinstance(check.body[-1],ast.Assign)and ast.unparse(check.body[-1])=='self.last = time.monotonic()','Budget last stamp after entire scan; SELF/time checked every call')
 engine=code['complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py'];host=code['run_guarded_current_B_complete_aggregate.UNREADY.py'];need("for phase in('scattering','scalar','fission','extras','overv_fallback','metadata')"in engine and "facts['original_context_event_count']==55"in host and "facts['all_original_snapshot_count']==8"in host and 'complete_source_field_comparisons' in engine and "prior_B_issue_count=None"in worker,'complete six phases/8pairs/55contexts/full fields and no invented B prior issue1')
 caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
 need(p['original_caps']==a['original_caps']==ready['original_caps']==caps and p['bounded_new_aggregate_output_reservation_bytes']==320*2**20 and p['bounded_new_Source_metadata_reservation_bytes']==16*2**20 and p['only_current_stage']=='aggregate'and p['future_stage_budget_added_to_this_stage']is False,'unchanged full original caps; aggregate320+Source16 only')
 need(p['actual_business_preconditions_closed']is p['source_role_pin_audit_complete']is p['B4_actual_role_projection_audited']is True,'all actual lifecycle/control roles closed')
 life=p['exact_B4_product_lifecycle_binding'];need(life['schema']=='CURRENT_B4_SPLIT1_PLUS3_EXACT_ARCHIVED_RETIRED_PRODUCT_ROLES_ADMISSION_V2','exact split1+3 lifecycle');original=meta(life['actual_B_capture_manifest_pin'])['states']['B']['actual_material_product_pins'];need(life['ordered_exact4_historical_product_pins']==original and life['first_retired_original_product_pins']==original[:1]and life['remaining3_original_product_pins']==original[1:]and len(original)==4 and not os.path.lexists(life['historical_incomplete_partial001_pin']['path']),'first1+remaining3 exactly original4; partial excluded')
 for q in original:need(not os.path.lexists(q['path']),'only proven historical4 absent')
 known=[('member0_restore','Root_report_pin','5826fd','9345ca','report_pin'),('exact2_recovery','receipt_pin','78ceda','7b7ebe','receipt_pin')]
 for stage,artifact,c1,c2,key in known:
  s=life[stage];truth(s['Root_tools_pin'],'actual_terminal_return',key,s[artifact],c1);truth(s['post_tools_pin'],'actual_review_return','review_pin',s['post_pin'],c2);need(meta(s[artifact])['failure']is None and meta(s['post_pin'])['failure']is None,'known real member0/exact2 closures')
 for stage,artifact in [('complete4_archive','Root_report_pin'),('remaining3_retirement','receipt_pin')]:
  s=life[stage];pr=s['actual_role_projection'];need(type(pr)is dict,'actual projection not NULL')
  for which,tool,field in [('Root_return','Root_tools_pin',artifact),('post_return','post_tools_pin','post_pin')]:
   r=pr[which];truth(s[tool],r['return_field'],r['output_artifact_field'],s[field],r['genuine_terminal_chunk_id'])
  need(meta(s[artifact])['failure']is None and meta(s['post_pin'])['failure']is None,'actual archive/remaining3 failureNone')
 arc=life['complete4_archive'];ret=life['remaining3_retirement'];index=meta(arc['index_pin']);receipt=meta(ret['receipt_pin']);post=meta(ret['post_pin']);projection=ret['actual_role_projection'];rproj=projection['receipt'];pproj=projection['post']
 need(at(receipt,rproj['released_pins_path'])==at(post,pproj['released_pins_path'])==original[1:]and at(receipt,rproj['released_bytes_path'])==at(post,pproj['released_bytes_path'])==346861973 and receipt['resources_after_original_classes_forced_fresh']is True,'actual remaining3 exact targets346861973 and final fresh closure')
 entries=life['ordered_exact4_current_entry_pins'];archives=life['ordered_exact4_current_archive_pins'];need(entries==[r['entry_pin']for r in index['entries']]and archives==[r['compressed_archive_full_pin']for r in index['entries']]and [r['original_plain_full_pin']for r in index['entries']]==original and len(entries)==len(archives)==4,'exact four entries and gzip in actual full4 index order')
 common=code['aggregate_Source_contract.UNREADY.py'];lh=code['current_B4_product_lifecycle_admission.UNREADY.py'];need("roles=[life['actual_B_capture_manifest_pin'],life['member0_complete_entry_pin']]+entries"in common and 'for v in compressed+entrypins+'in lh and 'compressed,entrypins=archived_original4' in lh,'correct explicit all4 entries proof union and current7 fix')
 live=p['prospective_worker_live_input_pins'];ordinary=p['child_ordinary_explicit_metadata_pins'];need(all(q in live for q in entries+archives+[arc['index_pin']])and all(q in ordinary for q in entries+[arc['index_pin']]),'all4 entries/index reach child live/current metadata; gzip live retainers')
 excluded={q['path']for q in original} | {life['historical_incomplete_partial001_pin']['path']}
 for key in ['prospective_worker_live_input_pins','explicit_cumulative_metadata_file_pins','inherited_metadata_current7_pins','child_ordinary_explicit_metadata_pins']:need(not excluded&{q['path']for q in p[key]},'only exact lifecycle historical roles removed; no missing live role')
 for q in live+ordinary:current(q)
 for q in p['explicit_cumulative_metadata_file_pins']+p['inherited_metadata_current7_pins']:current(q,False)
 for q in entries:meta(q)
 for q in archives:current(q)
 b55=p['current_B55_OVERV_control_binding'];v={k:meta(q)for k,q in b55['metadata_pins'].items()};truth(b55['metadata_pins']['control_returns'],'actual_terminal_return','report_pin',b55['metadata_pins']['control_report'],'02a5d8');truth(b55['metadata_pins']['control_post_returns'],'actual_review_return','review_pin',b55['metadata_pins']['control_post'],'f10181');counts=v['control_post']['actual_current_control_word_comparison_counts'];need(v['control_report']['actual_control_results']==v['control_post']['actual_control_results_metadata']and counts==dict(actual_current_energy_words_observed=371,actual_current_overv_words_compared=2960,actual_current_overv_groups=370,actual_current_overv_mixtures=8,actual_native_vs_integer_model_and_saved_word_mismatches=0,actual_constant64_words_compared=3,actual_constant64_word_mismatches=0),'real B55 371/2960/3constants/zero mismatches consumed')
 latest=meta(p['latest_complete_plan_pin']);roots=p['complete_joint_roots'];need(roots[:-1]==latest['complete_joint_roots']and len(roots)==75 and len(roots)==len(set(roots))and roots[-1]==p['planned_actual_output_root']and not os.path.lexists(roots[-1]),'full74 to fresh75 includes failed history; no new data yet')
 need(p['prior_B_aggregate_executed']is False and p['prior_B_issue_count']is None and p['issue_count_adjustment_performed']is False,'first actual B aggregate remains unexecuted at Source stage')
 for q in sp:read(q)
 report=dict(schema='INDEPENDENT_COMPLETE_CURRENT_B_AGGREGATE_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_CURRENT_B_COMPLETE_AGGREGATE',failure=None,source_only=True,control_plan_pin=pp,complete_source_file_pins=sp,Source_review_ready_pin=rp,author_source_freeze_pin=ap,admission_packet_pin=a['admission_packet_pin'],Root_Source_preparation_tools_pin=gp,all15_AST_and_unbound_global_checks_passed=True,host_builder_complete_inputs_exact=True,worker_engine_host_field_interfaces_match=True,original_engine_and_worker_whole_inverse_verified=True,original_decoder_adapter_B_binding_wholecopies_verified=True,Budget_full_scan_stamp_at_completion=True,complete_scope=dict(phases=['scattering','scalar','fission','extras','overv_fallback','metadata'],snapshot_pairs=8,contexts=55),real_B55_word_counts=counts,prior_B_aggregate_executed=False,prior_B_issue_count=None,issue_count_adjustment_performed=False,split1_plus3_original4_strict_union_and_partial_exclusion=True,actual_B4_lifecycle_binding=life,all4_entries_index_and_gzip_explicit_live=True,complete_joint_roots=roots,original_caps=caps,aggregate_only_output_bound_bytes=320*2**20,Source_metadata_bound_bytes=16*2**20,Root_must_refresh_original_resource_gate_before_actual=True,product_gzip_SQL_pool_or_scientific_body_opened=False,project_helpers_GEN_pub_worker_decoder_or_native_executed=False,files_deleted=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 q=HERE/'REVIEW.json'
 with q.open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status=report['status'],review_pin=pin(q),source_only=True)),flush=True)
if __name__=='__main__':main()
