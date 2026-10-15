import ast
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
DEST=Path('/private/tmp/axmat_v12_graph_table_owned_consume_independent_final_review_20261009')
OLD=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
NEW=Path('/private/tmp/axmat_complete_graph_canonical_file_table_owned_consume_source_draft_20261009')
NAME='combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
MOTHER=ROOT/'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
RD=ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/canonical_file_table_storage_Root_source_admission'
READY=RD/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.READY_REVIEW_CANDIDATE.py'
PROD=Path('/private/tmp/axmat_v12_owned_specs_identity_key_delta_graph_table_combined_source_only_20261009/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.UNREADY.py')
PM=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.py'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def funcs(t):return {n.name:ast.get_source_segment(t,n)for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)}
def inv(t,edits):
 for e in reversed(edits):
  assert t.count(e['new'])==1,e.get('name',e.get('region'))
  t=t.replace(e['new'],e['old'],1)
 return t

nt=(NEW/NAME).read_text();ot=(OLD/NAME).read_text();mt=MOTHER.read_text();rt=READY.read_text()
assert sha(NEW/NAME)=='b607c5e5ff9614d48a17e32df9605f7d29d3c7d685228caf5af01530319ef5d9'
assert sha(OLD/NAME)=='abb5aef91e6a2032c708c87a14fddf3a89e9798cf37d3e153233d8062c41920f'
assert sha(READY)=='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
assert inv(nt,read(NEW/'owned_consume_region_edits.json'))==ot
assert len(read(NEW/'owned_consume_region_edits.json'))==3
assert inv(nt,read(NEW/'complete_5_plus_3_source_region_edits.json'))==mt
assert len(read(NEW/'complete_5_plus_3_source_region_edits.json'))==8
n=funcs(nt);o=funcs(ot);m=funcs(mt);rf=funcs(rt)
assert len(n)==len(o)==72 and len(m)==69 and n==rf
assert [k for k in o if n[k]!=o[k]]==['decode_canonical_file_table_storage','strict_json','_parse_strict_json_payload']
assert [k for k in m if n[k]!=m[k]]==['strict_json','_parse_strict_json_payload']
assert 'MAX_JSON_BYTES = 64 * 1024 * 1024' in nt
assert n['encode_canonical_file_table_storage']==o['encode_canonical_file_table_storage']
assert 'tuple(pin) == CANONICAL_FILE_TABLE_STORAGE_COLUMNS' in n['encode_canonical_file_table_storage']
assert 'CANONICAL_FILE_TABLE_STORAGE_COLUMNS = ("path", "sha256", "size_bytes")' in nt
assert 'result = {"path": canonical, "sha256": digest.hexdigest(), "size_bytes": length}' in m['_stream']
assert 'actual[canonical] = pin' in m['_phase']
assert '"canonical_files": [actual[path] for path in sorted(actual)]' in m['create_graph']
assert 'return {key: value[key] for key in sorted(value)}' in m['_unique_sorted_object']
assert sorted(('path','sha256','size_bytes'))==['path','sha256','size_bytes']
assert n['_json_clone']==m['_json_clone']
assert n['_parse_strict_json_text']==m['_parse_strict_json_text']
decoder=n['decode_canonical_file_table_storage']
assert 'storage, *, _consume=False' in decoder
assert 'type(_consume) is bool' in decoder
assert decoder.index('pins.append({key: value')<decoder.index('rows[index] = None')<decoder.index('rows.clear()')<decoder.index('del rows')<decoder.index('_content_digest(restored)')
assert 'if pins:\n        del row, values' in decoder
assert 'copy.deepcopy' not in decoder and '_json_clone' not in decoder
assert 'if _consume:\n            rows[index] = None' in decoder and 'if _consume:\n        rows.clear()' in decoder
for k in ('strict_json','_parse_strict_json_payload'):
 f=n[k]
 assert f.index('result = _parse_strict_json_text(decoded, path)')<f.index('del decoded')<f.index('decode_canonical_file_table_storage(result, _consume=True)')
 assert 'if type(result) is dict and result.get("schema") == CANONICAL_FILE_TABLE_STORAGE_SCHEMA:' in f
 assert f.endswith('return result')
rootproof=read(RD/'Root_READY_candidate_inverse_proof.json')
assert len(rootproof['ready_regions'])==2 and inv(rt,rootproof['ready_regions'])==nt
assert inv(inv(rt,rootproof['ready_regions']),read(NEW/'complete_5_plus_3_source_region_edits.json'))==mt
assert 'GRAPH_STORAGE_SOURCE_STATUS = "READY_ROOT_REVIEWED_COMPLETE_INPUT_STORAGE_CODEC"' in rt
assert sha(NEW/'PURE_CODEC_REPORT.json')=='afb8afd67c8581ba8a90f245554fc31707c9810f704703ee8813db86a0336b52'
assert sha(NEW/'FINAL_REPORT.json')=='10caa6044a4e870bd9970b86e3906a3f5ffd6a9f13d5e4d96d214adea8e0a8d9'
assert sha(NEW/'actual_source_and_pure_codec_tool_return.json')=='6bf226ac6984ed0729cb992dad036bccd5070d234a197b736b464a188353202e'
pure=read(NEW/'PURE_CODEC_REPORT.json');actual=read(NEW/'actual_source_and_pure_codec_tool_return.json')
assert actual['source_sha256']==sha(NEW/NAME) and actual['pure_codec']['closed'] is True
assert type(actual['pure_codec']['exit_code'])is int and actual['pure_codec']['exit_code']==0
assert (actual['pure_codec']['initial_chunk_id'],actual['pure_codec']['session_id'],actual['pure_codec']['terminal_chunk_id'])==('4a21ea',5005,'bb2d72')
assert pure['source']['sha256']==sha(NEW/NAME) and len(pure['controls'])==59 and pure['owned_consume_control_count']==18
for k in ('full_decoded_original_graph_equal','every_row_value_type_order_and_duplicate_preserved','all_original_noncanonical_graph_values_preserved','source_and_data_seven_identity_before_after_equal','encoder_and_public_default_decoder_do_not_mutate_inputs','private_owned_consume_clears_parsed_rows_only','restored_canonical_pin_dicts_are_independent'):
 assert pure[k] is True,k
assert pure['two_real_strict_wrapper_calls_observed']==[dict(private_consume=True,rows_before=3,rows_after=0),dict(private_consume=True,rows_before=3,rows_after=0),dict(private_consume=True,rows_before=36776,rows_after=0)]
assert pure['whole_typed_order_and_IEEE_float_bits']==pure['decoded_whole_typed_order_and_IEEE_float_bits']
assert pure['complete_original_graph_json_measure']==pure['complete_decoded_graph_json_measure']
assert pure['diagnostic_stored_bytes']==66558451 and pure['headroom_bytes']==550413
for k in ('business_module_imported','business_API_or_phase_executed','controller_or_compiler_executed','project_written','formal_new_graph_created','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted'):
 assert pure[k] is False,k
assert pure['actual_new_combined_build'] is None
for row in actual['failed_pure_reviewers']:
 assert sha(row['path'])==row['sha256'] and row['exit_code']==1 and row['closed'] is True
pt=PROD.read_text();pmt=PM.read_text();p=funcs(pt);pm=funcs(pmt)
assert sha(PROD)=='4dd133d341c457d1ffb9ecc9ebd7c543ff430c221310d4869fcdce750e295c4c'
assert len(p)==65 and [k for k in pm if p[k]!=pm[k]]==['create_complete_input_graph']
assert p['create_complete_input_graph'].replace('json.dump(g.encode_canonical_file_table_storage(graph),f,','json.dump(graph,f,',1)==pm['create_complete_input_graph']
assert "'graph': (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py',None)" in pt
for line in pmt.splitlines():
 if any(line.startswith(k+' =')for k in ('TRIM_DECL_SHA','TRIM_SEAL_SHA','TRIM_TERMINAL_SHA','TRIM_SOURCE_ADMISSION_SHA','TRIM_OBJECT_SHA','TRIM_RUNTIME_SHA','TOTAL_WALL, STAGE_WALL, RSS','RESERVE, HISTORY_CAP, FREE_FLOOR')):assert line in pt
report=dict(schema='AXMAT_GRAPH_TABLE_OWNED_CONSUME_FINAL_INDEPENDENT_SOURCE_REVIEW_V1',status='PASS_REVIEWED_SOURCE_AND_BOUND_EXISTING_PURE_CODEC_EVIDENCE_ONLY',source=dict(path=str(NEW/NAME),sha256=sha(NEW/NAME)),READY_candidate=dict(path=str(READY),sha256=sha(READY)),parent_abb5=dict(path=str(OLD/NAME),sha256=sha(OLD/NAME)),original_parent=dict(path=str(MOTHER),sha256=sha(MOTHER)),three_region_inverse_toabb5=True,eight_region_inverse_to1d7=True,READY_two_only_text_status_regions=True,READY_total10region_inverse_to1d7=True,all72_READY_function_bodies_byteexact_to_b607=True,all67_original_functions_fullbyte_limits_math_phase_lineage_parser_text_unchanged=True,private_consume_defaultFalse_exactbool_and_nonmutation=True,both_parse_entries_del_text_before_owned_consumeTrue=True,complete_scalar_transfer_before_row_clear=True,all_consumed_rows_and_last_locals_released_before_content_digest=True,encode_unchanged_nonmutating_view=True,pin_insertion_order_matches_real_stream_phase_create_and_sorted_parser=True,original_issue_M1_resolved_in_source=True,existing_59_pure_controls=dict(path=str(NEW/'PURE_CODEC_REPORT.json'),sha256=sha(NEW/'PURE_CODEC_REPORT.json'),actual_tool_receipt=dict(path=str(NEW/'actual_source_and_pure_codec_tool_return.json'),sha256=sha(NEW/'actual_source_and_pure_codec_tool_return.json')),actual_closed_tool=dict(initial_chunk='4a21ea',session_id=5005,terminal_chunk='bb2d72',returncode=0),not_reexecuted_by_this_reviewer=True,diagnostic_old_graph_stored_bytes=66558451,original_read_bound_bytes=67108864,diagnostic_headroom_bytes=550413),producer_source_only=dict(path=str(PROD),sha256=sha(PROD),all64_nonwriter_functions_byteexact=True,all6_actual_V11_component_pins_preserved=True,all_original_resource_budgets_preserved=True,graph_helper_pin_currently_None=True,required_final_graph_helper_sha=sha(READY),READY_source_status_conversion_still_unreviewed_for_producer=True),future_binding_scope='The producer must bind final Root READY e8 source rather than b607 primitive hash. SOURCE/runtime/graph.py copy and source_inventory, source-owner extra graph helper path, factory copy, real fresh graph/declaration/intake/cold bindings all need consistent new actual hashes. Complete original seven INPUT bodies and fresh full graph verification remain unchanged; no old failed graph or closed job gets success credit.',findings=[],business_imports_or_calls=False,project_files_written=False,new_formal_graph_executed=False,new_combined_build_admission_verified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
DEST.mkdir(exist_ok=True)
out=DEST/'REPORT.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],report=str(out),sha256=sha(out)),ensure_ascii=False))
