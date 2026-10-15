import ast
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
DEST=Path('/private/tmp/axmat_v12_graph_table_independent_static_review_20261009')
HD=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
HELPER=HD/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
MOTHER=ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
PD=Path('/private/tmp/axmat_v12_owned_specs_identity_key_delta_graph_table_combined_source_only_20261009')
PRODUCER=PD/'prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.UNREADY.py'
PM=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def funcs(t):return {n.name:ast.get_source_segment(t,n)for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
def inverse(t,edits):
 for e in reversed(edits):
  assert t.count(e['new'])==1,e.get('name',e.get('region'))
  t=t.replace(e['new'],e['old'],1)
 return t

ht=HELPER.read_text();mt=MOTHER.read_text();pt=PRODUCER.read_text();pmt=PM.read_text()
assert sha(HELPER)=='abb5aef91e6a2032c708c87a14fddf3a89e9798cf37d3e153233d8062c41920f'
assert sha(MOTHER)=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
assert sha(PRODUCER)=='4dd133d341c457d1ffb9ecc9ebd7c543ff430c221310d4869fcdce750e295c4c'
assert sha(PM)=='66d09b9c8a818e25c7c12acf10ba7551256d71f5fd60bde1c80da6d35d0d9481'
assert len(read(HD/'source_region_edits.json'))==5
assert inverse(ht,read(HD/'source_region_edits.json'))==mt
h=funcs(ht);m=funcs(mt);p=funcs(pt);pm=funcs(pmt)
assert len(m)==69 and len(h)==72
assert [n for n in m if h[n]!=m[n]]==['strict_json','_parse_strict_json_payload']
assert set(h)-set(m)=={'_canonical_file_storage_values','encode_canonical_file_table_storage','decode_canonical_file_table_storage'}
for n in ('_stream','_phase','_parse_strict_json_text','verify_graph','_content_digest','_unique_object','_finite_float','_invalid_constant','_consumer_lineage'):
 assert h[n]==m[n]
assert 'MAX_JSON_BYTES = 64 * 1024 * 1024' in ht
for n in ('strict_json','_parse_strict_json_payload'):
 assert h[n].index('result = _parse_strict_json_text(decoded, path)') < h[n].index('del decoded') < h[n].index('return decode_canonical_file_table_storage(result)')
 assert 'if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:' in h[n]
 assert h[n].endswith('return result')
assert 'type(values[2]) is int and values[2] >= 0' in h['_canonical_file_storage_values']
assert 'type(values[0]) is str and type(values[1]) is str' in h['_canonical_file_storage_values']
assert 'type(storage) is dict and set(storage) == {"schema", "graph"}' in h['decode_canonical_file_table_storage']
assert 'set(table) == {"columns", "rows"}' in h['decode_canonical_file_table_storage']
assert 'table["columns"] == list(CANONICAL_FILE_TABLE_STORAGE_COLUMNS)' in h['decode_canonical_file_table_storage']
assert '_sha(restored.get("content_sha256")) == _content_digest(restored)' in h['decode_canonical_file_table_storage']
assert 'view = dict(graph)' in h['encode_canonical_file_table_storage']
assert 'view["canonical_files"] =' in h['encode_canonical_file_table_storage']
assert 'graph["canonical_files"] =' not in h['encode_canonical_file_table_storage']
assert 'copy.deepcopy' not in h['encode_canonical_file_table_storage']+h['decode_canonical_file_table_storage']
edits=read(PD/'source_complete_inverse_proof.json')['edits']
assert len(edits)==10 and inverse(pt,edits)==pmt
assert len(p)==65 and set(p)==set(pm)
assert [n for n in pm if p[n]!=pm[n]]==['create_complete_input_graph']
assert p['create_complete_input_graph'].replace('json.dump(g.encode_canonical_file_table_storage(graph),f,','json.dump(graph,f,',1)==pm['create_complete_input_graph']
for n in ('trim_component_contract','trim_component_input','record_actual_trim_component','graph_input_bindings','complete_input_phase','build','production_admission','modules','classes'):
 if n in pm:assert p[n]==pm[n]
for line in pmt.splitlines():
 if any(line.startswith(k+' =')for k in ('TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','TOTAL_WALL, STAGE_WALL, RSS','RESERVE, HISTORY_CAP, FREE_FLOOR')):
  assert line in pt
assert "'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py',None)" in pt
assert "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_CANONICAL_FILE_TABLE_COMBINED_V12'" in pt
pure=read(HD/'PURE_CODEC_REPORT.json')
assert sha(HD/'PURE_CODEC_REPORT.json')=='2cdfbca11901ae89ecbe88ea952bff86a3da5a39f56f47243138aee6f61d538a'
assert pure['source']['sha256']==sha(HELPER) and pure['parent']['sha256']==sha(MOTHER)
assert pure['full_decoded_original_graph_equal'] is True
assert pure['whole_typed_order_and_IEEE_float_bits']==pure['decoded_whole_typed_order_and_IEEE_float_bits']
assert pure['complete_original_graph_json_measure']==pure['complete_decoded_graph_json_measure']
assert len(pure['controls'])==41
assert pure['diagnostic_stored_bytes']==66558451 and pure['headroom_bytes']==550413

finding=dict(id='M1',severity='source_memory_lifetime_requirement',file=str(HELPER),function='decode_canonical_file_table_storage',observed='The decoder holds table[rows] unchanged while cumulatively constructing all pins. It does not progressively release consumed row list containers. Both full rows and reconstructed pin dicts coexist until return; this is separate from del decoded text, which is correctly done.',meaning='This source does not meet the requested timely row-release constraint and does not prove512MiB. The non-mutating default pure decode API is useful and can remain.',minimum_fix='Add an explicit private consume flag or helper used only for newly parsed locally-owned storage in both wrappers, clear each consumed table row slot after constructing its pin and release the rows container. Keep default public decode non-mutating if required by pure controls, and retain original full values/order/content digest. Re-pin the changed source and run matching pure codec controls; do not rerun any old closed business job.')
report=dict(schema='AXMAT_V12_CANONICAL_FILE_TABLE_HELPER_AND_PRODUCER_INDEPENDENT_STATIC_REVIEW_V1',status='STATIC_FULL_FIDELITY_PASS_WITH_ROW_LIFETIME_REPAIR_REQUIRED',helper=dict(path=str(HELPER),sha256=sha(HELPER)),producer=dict(path=str(PRODUCER),sha256=sha(PRODUCER)),helper_complete5region_inverse=True,original_helper_top69_only2wrappers_changed=True,all67_other_helper_functions_byteexact=True,both_json_entries_release_text_before_explicit_schema_decode=True,original_limits_fullbyte_phase_lineage_and_validation_unchanged=True,strict_outer_table_columns_row_scalars_and_nonbool_size=True,encode_does_not_modify_caller_graph=True,decoded_content_digest_checked=True,decode_avoids_deepcopy=True,decode_progressive_row_release=False,producer_complete10region_inverse=True,producer_top65_only_writer_expression_changed=True,all64_other_producer_functions_byteexact=True,six_real_V11_component_pins_preserved=True,complete_seven_INPUT_graph_logic_and_genuine_classes_preserved=True,matching_pure_codec_report=dict(path=str(HD/'PURE_CODEC_REPORT.json'),sha256=sha(HD/'PURE_CODEC_REPORT.json'),controls=41,actual_old_graph_stored_bytes=66558451,old_graph_encoding_headroom_bytes=550413,new_real_PREP_headroom_not_yet_proved=True),findings=[finding],binding_requirements=['Fill producer new INPUT_HELPERS graph SHA only with final reviewed actual helper source hash; if helper READY/docstring change, bind resulting final hash.','Root producer READY/docstring conversion must be separately inverse-proved; all functional bodies and six actual component pins stay exact.','New ordinary helper path and SOURCE/runtime/graph.py copied bytes enter fresh source_inventory and whole code_environment expected owners automatically; factory itself and SOURCE factory copy SHA also fresh.','New stored graph externalbyte SHA and decoded old graph content SHA remain separate, whole graph freshly derived at new PREP. Old failed V11 graph and run preserve failure, cannot serve new declaration or cold success.'],business_imports_or_calls=False,project_files_written=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
DEST.mkdir(exist_ok=True)
f=DEST/'REPORT.json';f.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],report=str(f),sha256=sha(f),findings=1),ensure_ascii=False))
