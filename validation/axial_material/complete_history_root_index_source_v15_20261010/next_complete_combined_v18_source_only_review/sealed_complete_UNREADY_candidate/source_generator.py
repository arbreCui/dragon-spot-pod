import ast
import hashlib
import json
import stat
from pathlib import Path

ROOT=Path('/Users/wen/spot')
P=ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py'
G=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'
Q=ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_helper_controls_admission_v17.json'
B=Path('/private/tmp/axmat_v17_complete_combined_fresh_wire_trace_table_source_only_FINAL_20261010')
U=B/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.UNREADY.py'
UIP=B/'source_inverse_proof.json'
RP=Path('/private/tmp/axmat_v17_complete_combined_READY_source_binding_20261010/source_binding_inverse_proof.json')
O=ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_table_combined_runtime_v15.py'
COLD=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py'
CONSUMER=ROOT/'validation/axial_material/cold_component_input_consumer_identity_key_delta_graph_table_own_pid_peak_v12.py'
HOST=ROOT/'validation/axial_material/combined_cold_own_rss_host_physical_basis_own_pid_peak_20261008.py'
BASE=ROOT/'validation/artifacts/axial-material-production-qualified-AB-rank1-factor-cache-20261007/runtime/production_runner.py'
CHECKS=ROOT/'validation/axial_material/combined_runtime_historical_input_checks.py'
CURRENT=ROOT/'validation/axial_material/combined_runtime_current_predicates_final_private_last_uses_20261009.py'
D=Path('/private/tmp/axmat_v18_complete_combined_full_phase_last_use_source_only_20261010')
D.mkdir()

def pin(path):
 s=path.lstat();assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
 raw=path.read_bytes();t=path.lstat();a=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns];b=[t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
 assert a==b and len(raw)==s.st_size
 return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity7=a)
def write(path,value):
 with path.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
def definitions(source):return {n.name:ast.get_source_segment(source,n)for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
inputs=[P,G,Q,U,UIP,RP,O,COLD,CONSUMER,HOST,BASE,CHECKS,CURRENT]
before=[pin(path)for path in inputs]
assert before[0]['sha256']=='feebcbb5894797d9f748a7b43e817b30da90e64068f17f141135121462ef234c'
assert before[1]['sha256']=='bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
assert before[2]['sha256']=='d49036e0a0fd396dd9550e81fd310b74442a867e7a4cc36ff2b16bf70a9c6bf8'
assert before[6]['sha256']=='0ea1e6295d8efb34bdccf1dcbde9e56654a5fcd6a190c372f181c5611564d382'
q=json.loads(Q.read_text())
assert q['helper']['sha256']==before[1]['sha256'] and q['status']=='QUALIFIED_PURE_COMPLETE_GRAPH_HELPER_METADATA_PROTOCOL_ONLY_V17'
assert all(q[name]is False for name in ('fresh_production_graph_created','fresh_runtime_INPUT_qualified','new_combined_prepared','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
src=P.read_text();original=src;edits=[]
def replace(old,new):
 global src
 assert src.count(old)==1,(old[:80],src.count(old))
 src=src.replace(old,new);edits.append(dict(old=old,new=new,occurrences=1))
replace(src.splitlines()[0],repr('UNREADY source-only V18 complete sender/root-index whole-phase caller last-use revision. Root-qualified bcd order-preserved full metadata helper and d490 pure-helper admission remain exact INPUT-only prerequisites. Every original whole historical body, full fresh EOF phase, graph trace, namespace, alias, current predicate, failure-length comparison, five build stages, physics and budget remains required. Additional whole pinned specs re-read replaces no original phase; completed private caller views are released after their real last use. V17 build exceeded original512 MiB after two inner stages and grants no build, native or science qualification. No actual V18 prepare/build/whole INPUT/native/AAA/ABA has run; all future business success pins remain None.'))
for old,new in (
("SOURCE = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v17-20261010'","SOURCE = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010'"),
("OUT = ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v17-20261010'","OUT = ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010'"),
("TERMINAL = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v17-20261010'","TERMINAL = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010'"),
("FAMILY = 'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V17'","FAMILY = 'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V18'"),
("PREFIX = 'AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V17'","PREFIX = 'AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V18'"),
("FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v17.py'","FORMAL_FACTORY = ROOT/'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py'"),
("DRAFT_STATUS = 'READY_REVIEWED_V17_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'","DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V18_FULL_PHASE_CALLER_LAST_USE_REVIEW_REQUIRED'"),
("if DRAFT_STATUS != 'READY_REVIEWED_V17_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':","if DRAFT_STATUS != 'READY_REVIEWED_V18_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY':"),
):replace(old,new)
oldfunc=definitions(original)['complete_input_phase'];newfunc=oldfunc
anchor="    before=current_input_predicates(helpers,specs,require_build_interpreter)\n    with g.ReadOpenAudit()as audit:"
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"    before=current_input_predicates(helpers,specs,require_build_interpreter)\n    # All current-before and two-literal-alias checks above have completed.\n    # Re-read the whole fixed specs only when current-after actually needs them.\n    del specs,original_aliases\n    with g.ReadOpenAudit()as audit:")
anchor="    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()\n    after=current_input_predicates(helpers,specs,require_build_interpreter)"
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()\n    # This is this phase's real verifier return; only its four used scalar counts\n    # survive. No public verifier result or graph is filtered or modified.\n    fresh_counts=(verified['canonical_files_read'],verified['actual_bytes_read'],\n        verified['logical_owner_requirements'],verified['exhaustive_namespaces_checked'])\n    del verified\n    # Full fresh EOF/SHA/identity/strict parsing occurs again, without a cache.\n    encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA);specs=minimal_live_specs(encoded);del encoded\n    after=current_input_predicates(helpers,specs,require_build_interpreter)")
anchor="    after=current_input_predicates(helpers,specs,require_build_interpreter)\n    current_new_owned_paths(d)\n    graph=g.strict_json"
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"    after=current_input_predicates(helpers,specs,require_build_interpreter)\n    current_new_owned_paths(d)\n    # Original current-after predicates consume all four fields. The remaining\n    # original length/negative-byte checker reads this complete field alone.\n    length_specs={'remaining_source_owned_requirements':specs['remaining_source_owned_requirements']}\n    del specs\n    graph=g.strict_json")
anchor="    pins={row['path']:row for row in graph['canonical_files']}\n    lengths=checks.check_failed_lengths_and_owned_negative_bytes(g,specs,g._alias_map(graph['aliases']),pins)"
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"    # Full canonical union/alias comparisons above have completed.\n    del files,complete_aliases,paths,expected_snapshot\n    pins={row['path']:row for row in graph['canonical_files']}\n    lengths=checks.check_failed_lengths_and_owned_negative_bytes(g,length_specs,g._alias_map(graph['aliases']),pins)")
anchor="    del graph,pins,specs,files,complete_aliases,paths;gc.collect()\n    return dict(phase=phase,canonical_files=verified['canonical_files_read'],bytes=verified['actual_bytes_read'],\n        logical_edges=verified['logical_owner_requirements'],namespaces=verified['exhaustive_namespaces_checked'],"
assert newfunc.count(anchor)==1
newfunc=newfunc.replace(anchor,"    del graph,pins,length_specs;gc.collect()\n    return dict(phase=phase,canonical_files=fresh_counts[0],bytes=fresh_counts[1],\n        logical_edges=fresh_counts[2],namespaces=fresh_counts[3],")
replace(oldfunc,newfunc)
compile(src,'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py','exec')
rev=src
for e in reversed(edits):
 assert rev.count(e['new'])==1
 rev=rev.replace(e['new'],e['old'])
assert rev==original
rp=json.loads(RP.read_text());u=rev
for e in reversed(rp['edits']):u=u.replace(e['new'],e['old'])
assert u==U.read_text()
up=json.loads(UIP.read_text());o=u
for e in reversed(up['edits']):o=o.replace(e['new'],e['old'])
assert o==O.read_text()
a,b=definitions(original),definitions(src)
assert a.keys()==b.keys();changed=[n for n in a if a[n]!=b[n]]
assert changed==['require_ready','complete_input_phase'],changed
unchanged=[n for n in a if a[n]==b[n]]
# The same original checker consumes the identical complete negative-byte field.
cs=CHECKS.read_text();cn=definitions(cs)['check_failed_lengths_and_owned_negative_bytes']
cs_node=ast.parse(cn).body[0]
fields=[n.slice.value for n in ast.walk(cs_node)if isinstance(n,ast.Subscript)and isinstance(n.value,ast.Name)and n.value.id=='specs'and isinstance(n.slice,ast.Constant)]
assert fields==['remaining_source_owned_requirements']
assert oldfunc.count('current_input_predicates(')==newfunc.count('current_input_predicates(')==2
assert oldfunc.count('current_new_owned_paths(')==newfunc.count('current_new_owned_paths(')==2
assert oldfunc.count('g.verify_graph(')==newfunc.count('g.verify_graph(')==1
assert oldfunc.count("g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])")==newfunc.count("g.strict_json(d['input_graph']['path'],d['input_graph']['sha256'])")==1
assert oldfunc.count('failed_prepare_input(g)')==newfunc.count('failed_prepare_input(g)')==2
assert oldfunc.count('gc.collect()')==newfunc.count('gc.collect()')==3
assert newfunc.count('encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA)')==2 and oldfunc.count('encoded=g.strict_json(str(INPUT_SPECS),INPUT_SPECS_SHA)')==1
oldgates=[ast.dump(n,include_attributes=False)for n in ast.walk(ast.parse(oldfunc))if isinstance(n,(ast.Assert,ast.If,ast.Raise))]
newgates=[ast.dump(n,include_attributes=False)for n in ast.walk(ast.parse(newfunc))if isinstance(n,(ast.Assert,ast.If,ast.Raise))]
assert oldgates==newgates
for v in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):assert src.count(v+' = None')==1
for lit in ('TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512','RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30',"def stage_labels():return ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']"):
 assert original.count(lit)==src.count(lit)==1
assert before==[pin(p)for p in inputs]
C=D/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.UNREADY.py'
with C.open('x')as f:f.write(src)
with(D/'complete_input_phase.V18.py.txt').open('x')as f:f.write(newfunc+'\n')
proof=dict(schema='AXMAT_V18_WHOLE_PHASE_CALLER_LAST_USE_SOURCE_INVERSE_V1',status='SOURCE_ONLY_UNREADY',inputs=before,source_inputs_before_after_equal=True,candidate=pin(C),edits=edits,full_inverse_to_feeb_exact=True,ancestry_inverse_to_82_exact=True,ancestry_inverse_to_0ea_exact=True,original_definition_names_exact=True,changed_definitions=changed,unchanged_definitions=unchanged,unchanged_definitions_count=len(unchanged),all_original_complete_phase_If_Assert_Raise_nodes_exact=True,all_original_current_predicate_calls_2_retained=True,all_original_current_owned_path_calls_2_retained=True,original_full_verify_1_and_second_strict_graph_1_retained=True,both_original_failed_prepare_reads_2_retained=True,original_gc_count_exact_no_extra_gc=True,extra_whole_pinned_specs_fresh_EOF_read_1=True,length_checker_complete_spec_field_source_exact=fields,actual_bcd_helper_and_d490_qualification_sources_unchanged=True,all_future_business_six_pins_None=True,no_memo_or_phase_hash_shortcut=True,no_graph_or_trace_or_historical_body_pruned=True,project_written=False,project_module_imported_or_API_called=False,resource_check_called=False,numeric_payload_read=False,actual_V18_control_or_prepare_or_build_or_INPUT_or_native_or_AAA_or_ABA_executed=False)
write(D/'source_inverse_proof.json',proof)
report=dict(schema='AXMAT_V18_COMPLETE_PHASE_CALLER_LAST_USE_SOURCE_REPORT_V1',status='SOURCE_ONLY_UNREADY_NOT_RUNTIME_QUALIFIED',candidate=pin(C),parent=before[0],helper=before[1],helper_Q=before[2],actual_V17_failure_Root_message_scope=dict(terminal_chunk='d03f21',actual_parent_exit_code=1,canonical_child_returncode=-15,child_seconds=166.138,sampled_peak_rss_mib=515.078125,original_rss_cap_mib=512,inner_stage_PASS=['build/link','metadata/objects'],remaining_three_stages_complete=False,successful_driver_result_or_seal=False,Root_failed_summary_sha256='21368d83dddde8aa85a712a5f8ebea4dfca3c2fd82c1d4c4979ec3bbcfa02df5',failure_line_observed=False,source_level_causality_proved=False),rejected_alternatives=['retry failed V17 namespace','remove fresh whole phases or traces','saved hash/stat caches or cross-phase reuse','weaken original RSS/accuracy/wall/history/free limits','add gc/malloc_trim/RSS sampling bypass','change kernel/sender/math/physical spec'],source_last_uses=[dict(object='specs four fields and original_aliases',last_use='current_input_predicates before; original two-alias equality already complete',change='delete before full verify_graph; full pinned specs re-read after actual verify/audit checks and before current-after'),dict(object='verified complete public return',last_use='consumer/content identity + audit canonical read count',change='retain same four fresh scalar counts only; original full return is not mutated'),dict(object='specs reached_component_records/independent_directory_owners/aliases',last_use='current-after and post current_new_owned_paths',change='delete private view; preserve the entire original remaining_source_owned_requirements object for exact original length/negative-byte checker'),dict(object='files/complete_aliases/paths/expected_snapshot',last_use='same whole canonical union and literal alias comparison',change='delete before constructing full canonical pins and failed namespace check')],remaining_risks=['V17 peak source line not observed; these last-use changes do not prove why515 MiB occurred or guarantee V18 PASS','bcd verify_graph still constructs full normalized namespaces, full private requirement tuples, full fresh byte pins and complete trace normalization; its qualification is protocol only, not full business phase RSS','declaration read() retains original independent JSON semantics and all declaration fields; environment/declaration_admission/run_build unchanged except V18 guard namespace constants','actual new prepare/build whole five-stage/INPUT/native evidence still required'],new_namespaces=dict(SOURCE='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010',OUT='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010',TERMINAL='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010',HOST='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-prepare-host-v18-20261010'),budgets=dict(whole=1800,stage=600,rss_mib=512,strict_JSON_bytes=67108864,source_out_reserve_bytes=2147483648,history_bytes=103079215104,free_bytes=8589934592,threads=1,children=1,retries=0),future_actual_combined_declaration_sha256=None,future_actual_combined_PREP_terminal_sha256=None,future_actual_combined_seal_sha256=None,future_actual_combined_run_terminal_sha256=None,future_actual_combined_runtime_sha256=None,future_actual_native_terminal_sha256=None,new_full_graph_or_whole_INPUT_or_native_or_science_qualification=False,project_written=False,helper_imported_or_executed=False,source_compile_only=True)
assert all(not Path(v).exists()for v in report['new_namespaces'].values())
write(D/'REPORT.json',report)
# Native SOURCE wiring map only. No new native candidate or false future pin.
def lineof(path,text):
 return next(i for i,l in enumerate(path.read_text().splitlines(),1)if text in l)
native=dict(schema='AXMAT_V18_FINITE_NEXT_NATIVE_SOURCE_WIRING_MAP_ONLY_V1',status='SOURCE_MAP_ONLY_NO_NEW_NATIVE_CANDIDATE_OR_QUALIFICATION',sources=before[7:11],fixed_physics_source=dict(path=str(BASE),function='production_config_from_spec / check_case_spec',line=lineof(BASE,'geometry, basis, production =')),fixed_physical_contracts=dict(groups=370,fission_components=32,scat=3,geometry_radial_regions=8,radial_radii_cm=[.11,.308712,.381084,.412536,.4225,.435,.485],hex_edge_cm=.61776479,radial_boundary='white isotropic albedo one, NOT specular reflection',axial_boundary='vacuum at both ends',case_order=['AAA','ABA'],training_slots=list('ABA'),rank_and_48cells_SN32_come_from_pinned_case_spec_not_new_choice=True,picard_alpha=1,outer_gate_each=5e-7,axial_spatial='constant diamond',no_new_material_temperature_or_geometry_change=True),cold_budget_source=dict(path=str(COLD),line=lineof(COLD,'BUDGETS = dict'),budgets=dict(setup_seconds=120,bootstrap_axial_seconds=4200,bootstrap_radial_seconds=600,radial_seconds=300,axial_seconds=4200,host_seconds=120,max_maps=100,total_seconds=43200),rss_cap_mib=512,original_cold_reservation_bytes=20971764748,original_snapshot_bytes=237955708,history_bytes=103079215104,free_bytes=8589934592,threads=1,children=1,retries=0),native_guard_source=dict(path=str(HOST),line=lineof(HOST,'CAPS = dict'),own_pid_source='cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py',own_pid_source_sha256='ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b',genuine_normal_class_or_MRO_no_overlay=True),required_finite_binding_points=[dict(file=str(COLD),functions=['require_input_ready','component_intake','completed_components','component_return_admission','last_cprime_trim_return_admission','complete_history_resources','source_contract','declare','render_controller','prepare_binding_in_clean_process','finalize_cold_in_clean_process','cold_launch_in_clean_process','cold_terminal_admission'],changes='fresh factory/SOURCE/OUTPUT/TERM/controls namespaces, new actual combined factory/source/seal/terminal/runtime/prep pins only after observed new success; complete actual V15 component/sender support contract; keep all original physics, metadata inverse, full producer P14/analysis P12 environment, deck inverse, 512 own-PID bounds, case order and closeout gates'),dict(file=str(CONSUMER),functions=['input_guard','consume_completed_inputs','consume_metadata'],changes='new actual whole standalone intake Root terminal and all full descriptor values; bcd graph SHA/dispatch, actual canonical schema and complete observed counts only after new intake success; keep full seven historical INPUT bodies, fresh all bytes, namespace and aliases; no API replay in cold controller'),dict(file=str(HOST),functions=['binding_admission','resource_provenance','source_mro_proof','controls_admission','make_executor'],changes='current native resource constructor/source descriptor must name actual ebbb DynamicHistoryResources; preserve original92/fe811 ancestor INPUT contracts as ancestors and exact genuine OwnRSS/own-PID guard; fresh bounded source/binding controls required; no class/global/cache overlay')],required_additional_artifacts=['normal whole combined admit host with full raw stdout descriptor under original1800/600/512/64MiB; actual Root exit0 and sealed evidence','new immutable cold intake descriptor, consumer, cold factory, postterminal recorder and true resource-bound native host SOURCE pins','new declare + prepare + binding + controls + finalize actual evidence before cold AAA','actual AAA full bounded convergence and eight original independent precision checks before ABA'],old_V12_native_failure_is_not_success=True,V17_failed_build_cannot_supply_intake_or_native_success=True,all_future_native_decl_prepare_binding_controls_terminal_closeout_pins_None=True,scientific_or_native_RSS_qualification=False,source_only=True)
write(D/'next_native_source_wiring_map.json',native)
print(json.dumps(dict(source_only=True,output_dir=str(D),candidate=pin(C),proof=pin(D/'source_inverse_proof.json'),report=pin(D/'REPORT.json'),native_map=pin(D/'next_native_source_wiring_map.json'),changed_definitions=changed,unchanged_definitions_count=len(unchanged),inverse_feeb_82_0ea_exact=True,no_new_gc=True,actual_business_executed=False),allow_nan=False))
