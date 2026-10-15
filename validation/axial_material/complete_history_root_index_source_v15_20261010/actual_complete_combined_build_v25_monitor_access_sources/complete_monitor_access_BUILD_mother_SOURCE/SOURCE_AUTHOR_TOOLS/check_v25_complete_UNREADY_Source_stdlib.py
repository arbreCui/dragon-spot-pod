"""AST/text/stdlib metadata author checks only, no candidate execution."""
import ast
import hashlib
import json
from pathlib import Path
import shutil
import stat

P=Path('/private/tmp/axmat_v25_complete_canonical_TRUE_snapshot_jointQ_UNREADY_SOURCE_bwo0x_85')
R=Path('/Users/wen/spot');B=R/'validation/axial_material/complete_history_root_index_source_v15_20261010'
checks=[]
def check(v,label):
 assert type(v)is bool and v,label
 assert label not in [r['check']for r in checks],label
 checks.append(dict(check=label,passed=True))
def pin(p):
 s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];raw=p.read_bytes();t=p.lstat()
 check(i==[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns],'own_'+str(p.relative_to(P))+'_full_EOF_unchanged')if p.is_relative_to(P)else None
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=i)
def ds(text):return {n.name:ast.get_source_segment(text,n)for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def assignments(text):return {n.targets[0].id:n.value for n in ast.parse(text).body if isinstance(n,ast.Assign)and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
def inv(t,rows):
 for row in reversed(rows):
  assert t.count(row['new'])==row['count'];t=t.replace(row['new'],row['old'])
 return t
proof=json.loads((P/'COMPLETE_SOURCE_INVERSES.json').read_bytes());bproof=json.loads((P/'COMPLETE_SOURCE_BINDER_INVERSES.json').read_bytes())
canonical=(P/'canonical.V25.UNREADY.full.py').read_text();old=(P/'ORIGINAL_PARENT_SOURCE/canonical.full.py').read_text();original_definitions=ds(old);new_definitions=ds(canonical)
check(len(original_definitions)==70,'original_complete_canonical_70_definitions_retained')
check(set(original_definitions).issubset(new_definitions),'every_original_canonical_definition_name_retained')
check(len(new_definitions)==77,'only_seven_added_stdlib_joint_Q_contract_definitions')
for role,rows in proof['exact_finite_transforms'].items():
 target=P/('canonical.V25.UNREADY.full.py'if role=='canonical'else'host_and_postclose_templates/'+role+'.V25.UNREADY.full.py');text=target.read_text();parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();back=inv(text,rows)
 check(back==parent,role+'_whole_exact_byte_inverse_to_actual_V22_parent')
 check(ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False),role+'_whole_AST_inverse_to_actual_V22_parent')
 check(set(ds(parent)).issubset(ds(text)),role+'_all_original_definitions_retained')
 for name,segment in ds(parent).items():check(ds(back)[name]==segment,role+'_'+name+'_original_full_definition_byte_restored')
 changed=[name for name in ds(parent)if ds(text)[name]!=ds(parent)[name]]
 if role=='canonical':check(changed==['require_ready','record_actual_trim_component','prepare_build','create_complete_input_graph','complete_input_phase','current_new_owned_paths'],'canonical_only_six_disclosed_lastuse_Q_and_owner_functions_changed')
 for cap in ('1800','600','512','2*2**30','96*2**30','8*2**30'):check(cap in text,role+'_original_budget_token_'+cap)
 check('exec('not in text,'no_dynamic_exec_added_'+role)
 if role in ('prepare_host','build_host'):
  for literal in ('full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','runner.execute','retries=0','children_at_once=1','resource.history_roots'):check(literal in text,role+'_genuine_flow_'+literal)
 if role in ('prepare_writer','build_writer'):
  main_node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)and n.name=='main');check(isinstance(main_node.body[0],ast.If),'UNREADY_'+role+'_guard_is_first_main_statement')
  check('UNREADY SOURCE ONLY'in ast.get_docstring(ast.parse(text)),'honest_UNREADY_'+role+'_doc')
a=assignments(canonical)
check(ast.literal_eval(a['DRAFT_STATUS'])=='UNREADY_V25_COMPLETE_INACTIVE_AUDIT_ACTUAL_Q_UNBOUND','canonical_UNREADY_status')
for k in ('FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA',*('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')):check(isinstance(a[k],ast.Constant)and a[k].value is None,k+'_truly_None_not_success')
check(canonical.count('trace=audit.snapshot(_consume=True)')==3 and canonical.count('trace=audit.snapshot()')==0,'exact_three_last_owned_snapshot_calls_and_no_other_snapshot_edits')
for name in ('record_actual_trim_component','create_complete_input_graph','complete_input_phase'):
 oldnode=ast.parse(original_definitions[name]).body[0];newnode=ast.parse(new_definitions[name]).body[0]
 calls=[n for n in ast.walk(newnode)if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and isinstance(n.func.value,ast.Name)and n.func.value.id=='audit'and n.func.attr=='snapshot']
 check(len(calls)==1 and len(calls[0].keywords)==1 and calls[0].keywords[0].arg=='_consume'and isinstance(calls[0].keywords[0].value,ast.Constant)and calls[0].keywords[0].value.value is True,name+'_one_private_True_snapshot')
 refs=[n.ctx.__class__.__name__ for n in ast.walk(newnode)if isinstance(n,ast.Name)and n.id=='audit'];check(refs.count('Load')==1 and refs.count('Store')==1 and refs.count('Del')==1,name+'_audit_no_other_alias_or_load_after_snapshot')
for key in ('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN'):
 check(isinstance(a[key],ast.Constant)and a[key].value is None,'UNREADY_'+key+'_unknown_actual_root_binding')
for token in ('ROOT_V25_ACTUAL_JOINT_HELPER_META_ADMISSION_WRITER_TOOL_TERMINAL_RETURN_V1','INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1','PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY',"'94520a'","'17e611'","'821784'","peer['check_count']==len(peer['checks'])==48","complete_original_member_count","helper_Q_collect_refs(value,external)","complete[p]=row"):
 check(token in new_definitions['helper_Q_admission'],'new_external_Q_exact_actual_proof_gate_'+token)
check('strict_json_bytes(qt[\'terminal_tool_return\'][\'output\'].encode(\'utf-8\'))'in new_definitions['helper_Q_admission'],'real_Root_Q_terminal_stdout_exact_integer_JSON_only')
check(old.count('gc.collect()')==canonical.count('gc.collect()'),'no_gc_added_or_moved_by_lastuse_Q_contract')
check('**helper_Q_admission()}'in new_definitions['prepare_build'],'all_actual_Q_and_proof_endpoints_explicit_typed_expected_file_owners')
check('*helper_Q_admission()]'in new_definitions['current_new_owned_paths'],'all_actual_Q_and_proof_endpoints_original_ordinary_scope')
check('helper_Q_admission()'in new_definitions['require_ready'],'actually_read_new_Q_not_only_nonzero_SHA')
for token in ('ACTUAL_HELPER_Q_SCHEMA','ACTUAL_HELPER_Q_STATUS','actual_root_terminal','independent_actual_review','actual_SOURCE_install_record','actual_SOURCE_install_tool_return','Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs','private_inactive_audit_snapshot_controls_order_preserved_artifact','complete_gzip_pins'):
 check(token in new_definitions['helper_Q_admission'],'new_actual_Q_complete_contract_'+token)
for forbidden in ('compile(','importlib','ReadOpenAudit(','verify_graph(','create_fresh_complete_wire_graph('):check(forbidden not in ''.join(new_definitions[k]for k in new_definitions if k.startswith('helper_Q_')),'joint_Q_reader_no_'+forbidden)
for role,row in bproof['roles'].items():
 text=Path(row['candidate_path']).read_text();parent=(P/'ORIGINAL_PARENT_SOURCE'/(role+'.full.py')).read_text();edit=row['whole_exact_inverse']
 check(edit['old']==parent and edit['new']==text and text.replace(edit['new'],edit['old'],1)==parent,role+'_whole_explicit_byte_inverse')
 check(ast.dump(ast.parse(edit['old']),include_attributes=False)==ast.dump(ast.parse(parent),include_attributes=False),role+'_whole_AST_inverse')
 check(all(ds(text)[k]==ds(parent)[k]for k in row['original_legacy_definition_bytes_exact']),role+'_all_declared_retained_legacy_helpers_exact')
 tree=ast.parse(text);check(len([n for n in tree.body if isinstance(n,ast.If)and isinstance(n.test,ast.Compare)and isinstance(n.test.left,ast.Name)and n.test.left.id=='__name__'])==1,role+'_main_only_dispatch_no_import_time_io')
 check('compile('not in text,role+'_no_Source_compilation_in_future_binder')
 check('helper_Q_admission()'in ds(text)['main'],role+'_actual_new_Q_and_core_proof_validation')
 for key in ('FUTURE_ACTUAL_NEW_Q_WRITER_TERMINAL_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_PIN','FUTURE_ACTUAL_NEW_Q_SAVED_PEER_RETENTION_PIN'):
  ba=assignments(text);check(isinstance(ba[key],ast.Constant)and ba[key].value is None,role+'_'+key+'_UNREADY_None')
 for token in ('--actual-new-Q-writer-terminal','--actual-new-Q-writer-terminal-sha256','--actual-Q-saved-peer','--actual-Q-saved-peer-sha256','--actual-Q-saved-peer-retention','--actual-Q-saved-peer-retention-sha256'):
  check(token in ds(text)['main'],role+'_requires_actual_Root_CLI_'+token)
 if role=='BUILD_binder':
  for token in ('all_complete_scope_verified','actual_PREP_metadata_only','actual_Root_PREP_summary_pin','actual_Root_PREP_terminal_pin','actual_complete_namespace_manifest_pin','actual_output_fullpins','all_original_full_five_stages_retained','ROOT_V25_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1'):check(token in ds(text)['main'],'BUILD_binder_preserves_'+token)

# Read only the new small authoritative Q as Source-contract context, never
# call any function from the new canonical/validator/binder/controller.
qp=B/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json';qraw=qp.read_bytes();q=json.loads(qraw)
qcontext_pin=pin(qp);check(qcontext_pin['sha256']=='c6efd7accfdc897642853a286bd0c0fa7caac91879a02aaf34dae2d3e2162d9b','actual_Root_Q_context_full_SHA_unbound')
check(q['schema']=='AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_INACTIVE_AUDIT_HELPER_ACTUAL_JOINT_ADMISSION_V25'and q['status']=='QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V25','Source_Q_schema_status_context_matches_actual_constructor')
check(q['helper']['sha256']=='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092','same_actual_installed_3b_Source_context')
for scope in (q,q['complete_current_graph_fresh_verifier']):
 for k in ('actual_root_terminal','actual_controls_summary','actual_host_result','actual_control_report','complete_namespace_manifest','independent_actual_review','independent_actual_review_tool_return','source_manifest','independent_review_retention_record','independent_review_actual_seal','actual_measurement'):check(k in scope,'actual_Q_'+('pure'if scope is q else'fresh')+'_core_endpoint_'+k)
check(len(q['full_protocol'])==13,'actual_Q_all_thirteen_original_protocol_fields_retained')
check(len(q['complete_current_graph_fresh_verifier']['all27_return_fields'])==27,'actual_Q_all27_complete_current_graph_return_fields_retained')
check(q['complete_current_graph_fresh_verifier']['complete_actual_read_counts']==dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True),'actual_Q_full_unfiltered_read_scope_context')
check([len(q['private_inactive_audit_snapshot_controls'][k])for k in ('positive_controls','private_guard_rejections','last_use_failure_controls')]==[5,13,3],'actual_Q_full_snapshot_controls_context')
for field in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','whole_build_qualified','whole_INPUT_admitted','physical_balance_qualified','canonical_wired'):check(q[field]is False,'actual_Q_context_'+field+'_false')
declared=q['Root_finite_joint_META_full_EOF_SHA7ID_verified_unique_inputs'];check(len(declared)==310,'actual_Q_complete_310_unique_input_pins_preserved_no_old173_assumption')
refs={}
def collect(v):
 if type(v)is dict:
  if'path'in v and'sha256'in v and('identity'in v or'identity7'in v):
   ids=v.get('identity',v.get('identity7'));row=dict(path=v['path'],sha256=v['sha256'],size_bytes=ids[4],identity=ids);assert row['path']not in refs or refs[row['path']]==row;refs[row['path']]=row
  for x in v.values():collect(x)
 elif type(v)is list:
  for x in v:collect(x)
collect(q);declared_map={v['path']:dict(path=v['path'],sha256=v['sha256'],size_bytes=v['identity'][4],identity=v['identity'])for v in declared}
check(len(declared_map)==310 and all(p in declared_map and declared_map[p]==r for p,r in refs.items()),'all_Q_core_refs_in_actual_complete_unique_input_scope')

qe=B/'actual_joint_helper_admission_v25_receipts'
qtpath=qe/'Root_actual_joint_helper_META_admission_writer_tool_terminal_return.json';qppeer=qe/'sealed_independent_actual_joint_Q_saved_META_review/REVIEW.json';qrpath=qe/'Root_actual_joint_Q_saved_META_peer_retention_record.json'
qt=json.loads(qtpath.read_bytes());qpeer=json.loads(qppeer.read_bytes());qrt=json.loads(qrpath.read_bytes());qout=json.loads(qt['terminal_tool_return']['output'])
check(qt['schema']=='ROOT_V25_ACTUAL_JOINT_HELPER_META_ADMISSION_WRITER_TOOL_TERMINAL_RETURN_V1'and qt['closed']is True and qt['actual_tool_terminal_return_observed']is True and type(qt['terminal_tool_return']['exit_code'])is int and qt['terminal_tool_return']['exit_code']==0 and qt['terminal_tool_return']['chunk_id']=='94520a'and'session_id'not in qt['terminal_tool_return'],'actual_new_Q_writer_context_real94520a_closed0')
check(qout['actual_metadata_Q']==qcontext_pin and qout['actual_Source_writer']==q['Root_actual_Source_writer'],'actual_Root_raw_stdout_exact_integer_Q_and_Source_fullpins')
check(qpeer['schema']=='INDEPENDENT_V25_ACTUAL_JOINT_HELPER_Q_SAVED_META_REVIEW_V1'and qpeer['status']=='PASS_ACTUAL_JOINT_HELPER_Q_METADATA_ONLY'and qpeer['source_only']is True and qpeer['all_checks_typed_true']is True and qpeer['blockers']==[] and type(qpeer['check_count'])is int and qpeer['check_count']==len(qpeer['checks'])==48 and all(type(r['passed'])is bool and r['passed']is True for r in qpeer['checks']),'actual_new_Q_saved48_fullschema_complete_typed_contract_context')
check(qpeer['Root_actual_Q_pin']==qcontext_pin and qpeer['Root_actual_Q_writer_terminal_pin']==pin(qtpath),'actual_new_Q_saved48_complete_4pin_coupling')
check(qrt['complete_original_member_count']==len(qrt['complete_original_members'])==10 and qrt['complete_original_members']['REVIEW.json']['saved']==pin(qppeer),'actual_new_Q_saved48_retention_full_context')
for field in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'):check(qpeer[field]is False,'actual_new_Q_saved48_'+field+'_false')
externalcontext=[pin(x)for x in (qtpath,qppeer,qrpath)]

# Preserve author sources and a compact observed-context witness. Observed Q
# is not inserted as a READY binding, and no future business SHA is invented.
authors=P/'SOURCE_AUTHOR_TOOLS';authors.mkdir(exist_ok=True)
for src in ('/private/tmp/author_v25_complete_UNREADY_Source_stdlib.py','/private/tmp/author_v25_complete_bindings_Source_stdlib.py','/private/tmp/refine_v25_unsealed_Q_caps_Source_stdlib.py','/private/tmp/finalize_v25_unsealed_Source_contract_stdlib.py','/private/tmp/complete_v25_new_Q_external_proof_Source_only.py',__file__):shutil.copy2(src,authors/Path(src).name)
context=dict(schema='V25_UNREADY_COMPLETE_SOURCE_OBSERVED_ACTUAL_Q_CONTEXT_ONLY_V1',source_only=True,observed_actual_Root_Q_pin=qcontext_pin,observed_complete_input_count=310,observed_external_new_Q_proof_pins=externalcontext,external_new_Q_proofs_bound_in_candidate=False,observed_helper=q['helper'],new_canonical_Q_binding_sha256=None,actual_Q_used_to_run_a_candidate=False,new_Q_created_by_this_author=False,future_PREP_BUILD_INPUT_native_science_qualifications=False)
(P/'ACTUAL_Q_CONSTRUCTOR_CONTEXT_ONLY.NOT_BOUND.json').write_text(json.dumps(context,indent=2,allow_nan=False)+'\n')
report=dict(schema='V25_COMPLETE_CANONICAL_THREE_TRUE_SNAPSHOT_JOINT_Q_PREP_BUILD_UNREADY_SOURCE_AUTHOR_CHECKS_V1',status='SOURCE_ONLY_UNREADY_FULL_FLOW_DESIGN_NO_CANDIDATE_EXECUTION',source_only=True,all_checks_typed_true=True,check_count=len(checks),checks=checks,blockers=[],complete_original_canonical_70_definitions=True,canonical_new_stdlib_Q_reader_definitions=7,only_three_actual_lastuse_snapshot_private_True_calls=True,all_Q_and_proof_inputs_added_as_explicit_typed_and_ordinary_endpoints=True,original_complete_PREP_and_five_stage_BUILD_scopes_and_caps_preserved=True,six_future_business_pins_None=True,new_actual_Q_binding_sha256=None,new_actual_Q_writer_terminal_and_saved48_and_retention_binding_pins_None=True,observed_external_Q_proof_context=externalcontext,observed_actual_Q_context=qcontext_pin,candidate_guard_API_compiler_or_numeric_executed=False,project_canonical_frozen_Source_ART_written=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,author_source_check_failures_are_not_candidate_or_business_retries=True)
(P/'SOURCE_AUTHOR_CHECKS.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(source_only=True,status=report['status'],all_checks_typed_true=True,check_count=len(checks),blockers=[],output=str(P),review=pin(P/'SOURCE_AUTHOR_CHECKS.json'))))
