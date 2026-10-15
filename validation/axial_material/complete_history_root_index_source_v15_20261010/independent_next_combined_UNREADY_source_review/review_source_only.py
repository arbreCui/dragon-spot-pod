"""Pure whole-source and fixed-document review; never imports project code."""
import ast, hashlib, json, os, stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');BASE=Path('/private/tmp/axmat_v15_sender_window_root_index_graph_table_combined_source_only_20261010');HERE=Path(__file__).parent
CAND=BASE/'prepare_sender_window_root_index_graph_table_combined_runtime_v15.UNREADY.py'
COMP=ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
pins={};sources={};checks={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def rd(p,w=None,ident=None):
 p=Path(p);a=identity(p);assert stat.S_ISREG(a[2]);b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
 assert identity(p)==a and len(b)==a[4] and (w is None or sha==w) and (ident is None or ident==a),str(p)
 pin=dict(path=str(p),sha256=sha,size_bytes=len(b),identity=a)
 if str(p) in pins:assert pins[str(p)]==pin
 pins[str(p)]=pin;sources[str(p)]=b;return b.decode()
def chk(n,b):checks[n]=bool(b);assert b,n
def segments(t):
 out={}
 def walk(n,parents):
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
   key='/'.join([*parents,n.name]);assert key not in out;out[key]=ast.get_source_segment(t,n);parents=[*parents,n.name]
  for c in ast.iter_child_nodes(n):walk(c,parents)
 walk(ast.parse(t),[]);return out
def consts(t):
 out={}
 for n in ast.parse(t).body:
  if isinstance(n,ast.Assign):
   for key in n.targets:
    if isinstance(key,ast.Name):
     try:out[key.id]=ast.literal_eval(n.value)
     except (ValueError,TypeError):pass
 return out
def replay(text,regions,old='before',new='after'):
 inv=text
 for x in reversed(regions):
  assert type(x['count']) is int and x['count']>0 and inv.count(x[new])==x['count'],x['name']
  inv=inv.replace(x[new],x[old],x['count'])
 return inv
t=rd(CAND,'0e4d1e4cbc3daf55b605665e9693a3afa7910b29f4df578d6dcaab812b2026d9');pr=json.loads(rd(BASE/'source_complete_inverse_proof.json','65365088ca669bebd39b0b9eca916f4cca0a3e8fe6cee21c1cc02d60e128ada1'))
report=json.loads(rd(BASE/'REPORT.json'));parent=rd(pr['parent']['path'],pr['parent']['sha256'],pr['parent']['identity']);ancestor=rd(pr['ancestor_V12']['path'],pr['ancestor_V12']['sha256'],pr['ancestor_V12']['identity'])
op=json.loads(rd(pr['c064_to_V12_proof']['path'],pr['c064_to_V12_proof']['sha256']));comp=rd(COMP,'cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447')
chk('28_regions_whole_byte_inverse_restores_c064',len(pr['regions'])==28 and replay(t,pr['regions'])==parent)
chk('32_parent_regions_whole_byte_inverse_restores_5af',len(op['regions'])==32 and replay(parent,op['regions'])==ancestor)
forward=parent
for x in pr['regions']:
 assert forward.count(x['before'])==x['count'];forward=forward.replace(x['before'],x['after'],x['count'])
chk('whole_forward_candidate_byteexact',forward==t)
s=segments(t);ps=segments(parent);cs=segments(comp);acs=segments(ancestor)
exact=[k for k,v in ps.items() if s.get(k)==v];modified=[k for k,v in ps.items() if k in s and s[k]!=v];added=sorted(set(s)-set(ps))
chk('original76_segments64_byteexact12_wiring9_additions',len(ps)==76 and len(exact)==64 and len(modified)==12 and len(added)==9 and set(ps)<=set(s))
chk('reported_exact_scope_matches_independent_AST',sorted(modified)==sorted(pr['modified_original_segments']) and added==pr['added_segments'])
for n in pr['all_protected_math_input_stage_and_supervisor_definitions_byteexact']:chk('protected_byteexact_'+n,s[n]==ps[n])
chk('component_two_complete_admission_gates_copied_byteexact',all(s[n]==cs[n] for n in ['stream_environment_helper_source_admission','root_index_resource_source_admission']))
cv=consts(t);pv=consts(parent);av=consts(ancestor)
future=['TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','SENDER_OBJECT_SHA','FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
chk('seven_component_and_six_future_success_pins_None',all(n in cv and cv[n] is None for n in future))
chk('draft_blocks_all_business_before_pins_formal_path_and_single_thread',cv['DRAFT_STATUS'].startswith('UNREADY_') and 'TMP draft cannot perform a business action' in s['require_ready'] and 'for value in (TRIM_DECL_SHA' in s['require_ready'] and 'single-thread environment required before project import' in s['require_ready'])
chk('original_constant_wall_RSS_archive_history_free_caps_byteexact',all(ast.get_source_segment(t,n) in parent for n in ast.parse(t).body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id in {'TOTAL_WALL','RESERVE','HISTORY_POLICY','THREAD_KEYS','TAIL_FIELDS'} for a in n.targets)))
chk('original_stage5_and_complete_run_unchanged',s['stage_labels']==ps['stage_labels'] and s['stage_commands']==ps['stage_commands'] and s['run_build']==ps['run_build'] and s['stage_labels'].count("'")==10)
chk('production_three_objects_whole_original92_inverse_and_index2',s['combined_link_command']==ps['combined_link_command'] and "sole_object_changes=['SPOT1P64.o','SPOASM.o','FLU2DR64.o']" in s['combined_link_command'] and "d['production_link_command']!=d['build_commands'][2]" in s['trim_component_contract'])
chk('normal_V15_true_three_argument_API_and_full_return',s['record_actual_trim_component']==ps['record_actual_trim_component'] and "trim_factory().production_admission(TRIM_SEAL_SHA,str(TRIM_TERMINAL/'terminal_return.json'),TRIM_TERMINAL_SHA)" in s['record_actual_trim_component'] and 'trim_component_contract(value,d,admission)' in s['record_actual_trim_component'] and 'write_new(SOURCE/TRIM_INPUT_NAME,value)' in s['record_actual_trim_component'])
chk('whole_seven_input_and_local_strict_reader_ancestor_unchanged',s['actual_components']==ps['actual_components'] and s['actual_components'].count("bodies!=expected")==1 and s['strict_json_bytes']==ps['strict_json_bytes']==acs['strict_json_bytes'] and s['read']==ps['read']==acs['read'])
graph=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py';gt=rd(graph,'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28');gs=segments(gt)
chk('e8_helper_pinned_unchanged_and_original64MiB_two_strict_readers','MAX_JSON_BYTES = 64 * 1024 * 1024' in gt and 'MAX_JSON_BYTES' in gs['strict_json'] and 'strict_json_bytes' in s['read'] and graph.name in t and 'e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28' in t)
chk('complete_input_phase_full_scope_fresh_each_phase_and_no_consumer_scope',s['complete_input_phase']==ps['complete_input_phase'] and 'current_new_owned_paths(d)' in s['complete_input_phase'] and 'g.verify_graph' in s['complete_input_phase'] and "verified['consumer_scope']is not None" in s['complete_input_phase'] and "any(x['attempt_count']!=1" in s['complete_input_phase'])
chk('current_phase_support_gate_rechecks_before_after_graph',s['complete_input_phase'].count('current_new_owned_paths(d)')==2 and 'support=component_support_contract(tv,td,ta)' in s['current_new_owned_paths'])
chk('all_regular_helper_resource_files_have_complete_component_owner_then_graph_owner',"d['files'].get(path) != wanted" in s['component_support_contract'] and "merge_expected(files,support['files'])" in s['trim_component_input'] and "*trim['support_owners']" in s['create_complete_input_graph'] and "expected_files=dict(stream['source_inputs'])" in s['component_support_contract'] and "expected_files=dict(resource['source_inputs'])" in s['component_support_contract'] and s['graph_input_bindings']==ps['graph_input_bindings'])
chk('two_independent_owner_roles_present','ACTUAL_COMPLETE_HELPER_PROTOCOL_AND_ALL_SOURCE_ANCESTORS_V15' in s['component_support_contract'] and 'ACTUAL_COMPLETE_ROOT_INDEX_RESOURCE_AND_ALL_SOURCE_ANCESTORS_V15' in s['component_support_contract'])
chk('bad_cycle_fixture_aliases_retained_in_original_whole_namespace_gate','controls[key] != observed' in s['stream_environment_helper_source_admission'] and "observed_links[relative] = os.readlink(path)" in s['stream_environment_helper_source_admission'] and "controls['control_root']" in s['stream_environment_helper_source_admission'] and 'stream = stream_environment_helper_source_admission()' in s['component_support_contract'])
chk('helper_fixture_aliases_not_native_aliases_or_graph_capture_alias_scope',"native_library_aliases" not in s['component_support_contract']+s['current_new_owned_paths'] and "support" not in '\n'.join(line for line in s['create_complete_input_graph'].splitlines() if 'capture_aliases' in line or 'trim_alias_paths' in line) and s['current_trim_predicates']==ps['current_trim_predicates'])
qpath=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_resource_module_admission.json';q=json.loads(rd(qpath,'5a0b2c1870ba1f0cced713bb3528fb9c13928aaf436859763c97edb19afd7676'))
qp={x['path']:x['sha256'] for x in q['full_input_pins']};chk('resource42_unique_regular_full_pins_plus_independent_qualification_owner43',len(q['full_input_pins'])==len(qp)==42 and str(qpath) not in qp and "expected[admission_pin['path']] = admission_pin['sha256']" in s['root_index_resource_source_admission'])
for x in q['full_input_pins']:rd(x['path'],x['sha256'],x['identity'])
chk('all42_resource_pins_fresh_complete_SHA_and_identity',True)
chk('resource_two_full_namespace_gates_rechecked_twice_with_all_links',len(q['complete_actual_namespace_inventories'])==2 and "namespace_snapshot(namespace['root']) != before_namespace" in s['root_index_resource_source_admission'] and "expected[str(path)]" in s['root_index_resource_source_admission'] and 'target=os.readlink(path)' in s['root_index_resource_source_admission'])
chk('true_current_resource_module_and_original_ancestry_distinct','new genuine resource factory and old ancestry descriptors must remain distinct' in s['component_support_contract'] and "return load(ROOT_INDEX_RESOURCE_MODULE" in s['root_index_resource_factory'] and "root_index_resource_factory().DynamicHistoryResources" in s['DynamicHistoryResources'] and 'ROOT_INDEX_RESOURCE_SOURCE_PARENT' in s['root_index_resource_source_admission'])
helperqpath=ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/Root_actual_helper_controls_admission.json';hq=json.loads(rd(helperqpath,'16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568'))
helperproof=ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/source_patch_proof.json';rd(helperproof,'1809278680379d2ef6ee5c76218d4614abbbc1c9cbcf379674e7540485db86f2');rd(ROOT/'validation/axial_material/complete_environment_streaming_sha_helper_v14b.py','7d740b177f5e1c728f0729df031248fbb396f6978b9a3d5c8776a0c270db48d3')
chk('fixed_original_H7d_1809_16d_full_gate_and_no_cross_stage_SHA_cache',s['stream_environment_helper_source_admission']==cs['stream_environment_helper_source_admission'] and "cross_stage_SHA_reuse=False" in s['stream_environment_helper_source_admission'] and "for literal, wanted in files.items():" in s['stream_environment_helper_source_admission'])
links={k:v for name in ['control_inventory','host_inventory'] for k,v in hq[name]['symlinks'].items()};chk('actual_helper_qualification_retains_deliberately_invalid_and_cycle_symlink_map',bool(links) and any('cycle' in k or 'loop' in k or 'bad' in k for k in links))
sender=next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef) and n.name=='sender_component_contract');assign=next(n for n in sender.body if isinstance(n,ast.Assign) and any(isinstance(a,ast.Name) and a.id=='original68' for a in n.targets));counts={k.arg:ast.literal_eval(k.value) for k in assign.value.keywords}
chk('original68_complete30_count_fields_and_only86_total_override',len(counts)==30 and counts['total_declared_stages']==68 and counts['actual_total_unit_kernel_invocations']==2710 and counts['bitwise_compared_output_scalars']==2042712 and counts['compared_actual_field_and_source_bytes']==53816832 and 'expected86 = dict(original68, total_declared_stages=86)' in s['sender_component_contract'])
chk('sender14_separate70raw_288241824_48stub_zero_kernel_credit',all(x in s['sender_component_contract'] for x in ['positive_cases=10','expected_guard_rejection_cases=4','reference_wrapper_calls=24','candidate_wrapper_calls=24','wrapper_calls_total=48','observer_calls_total=34','raw_file_count=70','raw_bytes=288241824',"len(raw_sender['cases']) != 14",'real_SPOT_receiver_calls_in_this_observer_executable',"sum(row['status'] == 'FAILED' for row in stages) != 24"]))
chk('exact_original12_build59old14sender_final_audit_and_expected_negative_guards',all(x in s['sender_component_contract'] for x in ["len(d['build_commands']) != 12",'len(old_labels) != 59','len(labels) != 86','len(negative23) != 20','len(negative1) != 4',"watch['rss_cap_mib'] != 512"]))
chk('no_old_failed_component_or_combined_or_native_credit_transfer',"failed_historical_combined_RUN_promoted=False" in s['create_complete_input_graph'] and "old_capture_RSS_transferred=False" in s['trim_component_input'] and "native_RSS_proof_obtained=False" in s['sender_component_contract'] and report['actual_component_execution_success_claimed'] is False)
for path in [report['proposed_formal_factory'],*report['new_roots']]:chk('new_namespace_absent_'+Path(path).name,not os.path.lexists(path))
for p in list(pins.values()):rd(p['path'],p['sha256'],p['identity'])
compile(t,str(CAND),'exec')
result=dict(schema='AXMAT_V15_COMBINED_UNREADY_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS_COMPLETE_SOURCE_ONLY_UNREADY_NO_BUSINESS_PERMISSION_GRANTED',checks=checks,all_checks_passed=True,
    candidate=pins[str(CAND)],source_input_pins=list(pins.values()),whole_inverse_regions=28,parent_inverse_regions=32,original_segments=76,byteexact_segments=64,wiring_segments=12,added_segments=9,
    full_protected_segments=pr['all_protected_math_input_stage_and_supervisor_definitions_byteexact'],original68_counts=counts,
    seven_component_pins_and_six_future_pins_None=True,resource_pins42_plus_qualification43=True,full_invalid_helper_alias_maps_retained=links,
    mathematical_source_or_stage_or_threshold_changes=False,business_import_or_execution=False,API_or_fixture_or_resource_scan=False,Root_session_polled=False,
    project_files_written=False,full86_component_credit=False,new_combined_credit=False,native_RSS_credit=False,AAA_accuracy_qualified=False,ABA_admitted=False,
    review_scope='Pure full byte inverse/AST protected-source checks and fixed canonical qualification files only. Copied complete helper/resource namespace gates are inspected as source, never invoked. No live OUT inventory or runtime observation.')
with (HERE/'REPORT.json').open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
print(json.dumps(dict(status=result['status'],checks=len(checks),input_pins=len(pins),report_sha256=hashlib.sha256((HERE/'REPORT.json').read_bytes()).hexdigest()),allow_nan=False))
