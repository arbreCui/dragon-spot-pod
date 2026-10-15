import ast
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
DEST=Path('/private/tmp/axmat_v12_standalone_intake_independent_source_review_20261009')
D=Path('/private/tmp/axmat_v12_graph_table_standalone_bounded_whole_input_intake_source_only_20261009')
FACTORY=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
HELPER=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
V10_FACTORY=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_factor_diagonal_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v10.py'
V10_HELPER=ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def inv(t,edits):
 for e in reversed(edits):
  assert t.count(e['new'])==1,e['region']
  t=t.replace(e['new'],e['old'],1)
 return t
def funcs(t):return {n.name:ast.get_source_segment(t,n)for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
proof=read(D/'source_complete_inverse_proof.json');report=read(D/'REPORT.json');receipt=read(D/'actual_source_generation_tool_receipt.json')
results={}
for filename,count,total,digest in [('host.UNREADY.py',7,18,'11f4b4dd268228fa00a11c07868d36ecb69f451fe8f30b10ab9593efaa45161f'),('postterminal_recorder.UNREADY.py',8,22,'034630d8e8c8518081314ce846b13c485fdb9640c52f282e7507a7becd932049')]:
 p=proof['proofs'][filename];text=(D/filename).read_text();ast.parse(text)
 assert sha(D/filename)==digest==p['candidate']['sha256']
 assert len(p['new_identity_edits'])==count and len(p['prior_V10_to_V11_edits'])+count==total
 mother=Path(p['mother_V11']['path']);genuine=Path(p['mother_genuine_V10']['path'])
 assert sha(mother)==p['mother_V11']['sha256']and sha(genuine)==p['mother_genuine_V10']['sha256']
 old=inv(text,p['new_identity_edits']);assert old==mother.read_text();assert inv(old,p['prior_V10_to_V11_edits'])==genuine.read_text()
 results[filename]=dict(path=str(D/filename),sha256=digest,new_identity_regions=count,complete_genuine_V10_inverse_regions=total,all_code_outside_identity_regions_original_byteexact=True)
assert sha(FACTORY)=='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
assert sha(HELPER)=='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
f=funcs(FACTORY.read_text());v=funcs(V10_FACTORY.read_text())
protected=['production_admission','complete_input_phase','actual_components','input_modules','current_input_predicates','graph_input_bindings','modules']
assert all(f[k]==v[k]for k in protected)
g=funcs(HELPER.read_text());oldg=funcs(V10_HELPER.read_text())
assert all(g[k]==oldg[k]for k in ('verify_graph','_phase','_consumer_lineage','_parse_strict_json_text'))
assert 'MAX_JSON_BYTES = 64 * 1024 * 1024' in HELPER.read_text()
host=(D/'host.UNREADY.py').read_text();rec=(D/'postterminal_recorder.UNREADY.py').read_text()
for key in ('SEAL_SHA','RUN_SHA','PREP_SHA','DECL_SHA'):assert key+'=None' in host
for key in ('HOST_SHA','DECL_SHA','SEAL_SHA','RUN_SHA','PREP_SHA','API_RETURN_SHA'):assert key+'=None' in rec
assert "DRAFT_STATUS='UNREADY_SOURCE_ONLY_GRAPH_TABLE_V12_STANDALONE_WHOLE_INPUT_DRAFT'" in host
assert host.index('if DRAFT_STATUS!=')<host.index('spec=importlib.util.spec_from_file_location')
assert "DRAFT_STATUS='UNREADY_SOURCE_ONLY_GRAPH_TABLE_V12_POSTTERMINAL_RECORDER_DRAFT'" in rec
assert rec.index('if DRAFT_STATUS!=')<rec.index('s=importlib.util.spec_from_file_location')
assert len(report['future_actual'])==30 and all(value is None for value in report['future_actual'].values())
assert report['child_API_token_count']==9 and report['interpreter']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
assert report['standard_three_keyword_arguments']==['seal_sha','terminal_evidence','terminal_evidence_sha256']
assert report['actual_caps_retained']==dict(total_wall_seconds=1800,stage_wall_seconds=600,RSS_MiB=512,threads=1,children_at_once=1,retries=0)
for token in ('full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)','type(runner)is not full.OwnRSSSerialExecutor','runner.resources is not resources','runner.execute(BASE/\'intake\',\'admit\',command,600)','runner=full.OwnRSSSerialExecutor(BASE,1800-(time.monotonic()-STARTED),FAMILY,resources)'):
 assert token in host,token
assert "not 0<=watch['sampled_peak_rss_mib']<512" in host
assert "not 0<w['sampled_peak_rss_mib']<512" in rec
assert "r.strict(BASE/'intake/admit.log')" in rec and "API_RETURN_SHA=None" in rec
assert "for key in ('producer','declaration','build_seal','actual_run','actual_PREP','actual_API_whole_merged_stream','actual_API_whole_return','supervisor_source','parent_source','bounded_helper')" in rec
assert "type(w['returncode'])is not int or w['returncode']!=0" in rec
assert report['installed_formal_V12_factory_source']['sha256']==sha(FACTORY)and report['installed_graph_helper_source']['sha256']==sha(HELPER)
assert report['no_consumer_scope_or_input_filtering']is True and report['all_original_seven_INPUT_bodies_preserved']is True
out=dict(schema='AXMAT_V12_STANDALONE_WHOLE_INPUT_INTAKE_INDEPENDENT_STATIC_SOURCE_REVIEW_V1',status='PASS_SOURCE_ONLY_UNREADY_NO_NEW_INTAKE_SUCCESS',reviewed_sources=results,source_inverse_proof=dict(path=str(D/'source_complete_inverse_proof.json'),sha256=sha(D/'source_complete_inverse_proof.json')),source_generation_report=dict(path=str(D/'REPORT.json'),sha256=sha(D/'REPORT.json')),source_generation_receipt=dict(path=str(D/'actual_source_generation_tool_receipt.json'),sha256=sha(D/'actual_source_generation_tool_receipt.json')),installed_factory=dict(path=str(FACTORY),sha256=sha(FACTORY)),installed_graph_helper=dict(path=str(HELPER),sha256=sha(HELPER)),full7_production_input_functions_byteexact_toV10=protected,fresh_full_graph_reader_phase_parser_lineage_unchanged=True,original64MiB_reader_cap_unchanged=True,actual_host_MRO_constructor_resource_object_and_supervisor_sources_guarded=True,original1800_600_512_thread1_child1_retry0_unchanged=True,all_host4_and_recorder6_actual_pins_None=True,all30_future_success_fields_None=True,UNREADY_gates_before_any_business_import=True,full_original_API_stream_return_scope_and_postterminal_bindings_preserved=True,new_stored_graph_read_uses_exact_reviewed_e8_helper_via_factory_not_legacy_cold_scope=True,ready_conversion_requirements=['After actual new run-build typed0 + fixed seal/terminal, fill host DECL/SEAL/RUN/PREP actual pins and READY status; independently inverse-review only those five assignments.','Recorder must remain UNREADY until actual host tool0 + complete API stream are available; then fill its six actual pins and READY status with postterminal facts, never before observed success.','Root records canonical application argv separately from any actual interpreter options; no separate child stderr is claimed because original guarded stream is merged.','Keep all fresh complete INPUT byte checks, source/helper MRO identity and original caps. No former V10 success, old failed V11 graph or purecodec result qualifies new intake.'],findings=[],existing59_controls_reexecuted=False,business_imports_or_calls=False,project_files_written=False,Root_live_or_closed_jobs_polled=False,new_intake_success_observed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
DEST.mkdir(exist_ok=True);p=DEST/'REPORT.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(status=out['status'],report=str(p),sha256=sha(p)),ensure_ascii=False))
