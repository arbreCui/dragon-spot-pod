import ast
import hashlib
import json
import stat
import sys
from pathlib import Path

D=Path('/private/tmp/axmat_complete_graph_canonical_file_table_owned_consume_source_draft_20261009')
B=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
N='combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def identity(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
terminal_chunk=sys.argv[1]
assert sha(D/N)=='b607c5e5ff9614d48a17e32df9605f7d29d3c7d685228caf5af01530319ef5d9'
frozen=[(N,'abb5aef91e6a2032c708c87a14fddf3a89e9798cf37d3e153233d8062c41920f'),('PURE_CODEC_REPORT.json','2cdfbca11901ae89ecbe88ea952bff86a3da5a39f56f47243138aee6f61d538a'),('source_inverse_proof.json','758590b04de09db506f70d80bc76c99b9e0e6bad5b165c9609ee44868ebb0a6a'),('actual_source_and_pure_codec_tool_return.json','edaf221ace316c8a6b4e90f5684470078800ae87cd4353a7399e725da8cae7bf')]
oldpins=[]
for name,digest in frozen:
 p=B/name;ident=identity(p);assert sha(p)==digest and identity(p)==ident
 oldpins.append(dict(path=str(p),sha256=digest,identity=ident))
report=json.loads((D/'PURE_CODEC_REPORT.json').read_text())
assert report['control_count']==59 and report['owned_consume_control_count']==18
assert report['source']['sha256']==sha(D/N)
assert report['original_stored_bytes']==67624825 and report['diagnostic_stored_bytes']==66558451 and report['headroom_bytes']==550413
assert report['full_decoded_original_graph_equal'] and report['source_and_data_seven_identity_before_after_equal']
assert report['whole_typed_order_and_IEEE_float_bits']==report['decoded_whole_typed_order_and_IEEE_float_bits']
assert report['complete_original_graph_json_measure']==report['complete_decoded_graph_json_measure']
assert len(report['two_real_strict_wrapper_calls_observed'])==3
assert report['two_real_strict_wrapper_calls_observed'][-1]==dict(private_consume=True,rows_before=36776,rows_after=0)
assert (D/'pure_codec.stderr').read_bytes()==b'' and (D/'source_generation.stderr').read_bytes()==b''
pure_stdout=[json.loads(line) for line in (D/'pure_codec.stdout').read_text().splitlines()]
assert len(pure_stdout)==2 and pure_stdout[-1]['report_sha256']==sha(D/'PURE_CODEC_REPORT.json')
parent=Path(report['parent']['path']);source=parent.read_text();candidate=(D/N).read_text()
edits=json.loads((D/'complete_5_plus_3_source_region_edits.json').read_text());assert len(edits)==8
inverse=candidate
for edit in reversed(edits):assert inverse.count(edit['new'])==1;inverse=inverse.replace(edit['new'],edit['old'],1)
assert inverse==source
trees=[ast.parse(s) for s in (source,candidate)]
defs=[{n.name:ast.get_source_segment(s,n) for n in t.body if isinstance(n,ast.FunctionDef)} for s,t in zip((source,candidate),trees)]
same=[name for name in defs[0] if defs[0][name]==defs[1][name]]
assert len(defs[0])==69 and len(defs[1])==72 and len(same)==67
receipt=dict(schema='AXMAT_CANONICAL_FILE_TABLE_OWNED_CONSUME_ACTUAL_SOURCE_AND_PURE_CODEC_TOOL_RETURN_V1',status='CLOSED_SOURCE_AND_PURE_CODEC_ONLY',source_generation=dict(initial_chunk_id='0acd35',exit_code=0,closed=True,session_id=None),pure_codec=dict(initial_chunk_id='4a21ea',session_id=5005,terminal_chunk_id=terminal_chunk,exit_code=0,closed=True),failed_pure_reviewers=[dict(path=str(D/'failed_fixture_reader_before_MAX_JSON_BYTES_binding'/'actual_tool_return.json'),sha256=sha(D/'failed_fixture_reader_before_MAX_JSON_BYTES_binding'/'actual_tool_return.json'),exit_code=1,closed=True),dict(path=str(D/'failed_fixture_reader_before_sorted_parse_boundary'/'actual_tool_return.json'),sha256=sha(D/'failed_fixture_reader_before_sorted_parse_boundary'/'actual_tool_return.json'),exit_code=1,closed=True)],source_sha256=sha(D/N),report_sha256=sha(D/'PURE_CODEC_REPORT.json'),inverse_proof_sha256=sha(D/'source_inverse_proof.json'),stdout_sha256=sha(D/'pure_codec.stdout'),stderr_size=0,business_executed=False,project_written=False,actual_business_RSS_qualified=False)
(D/'actual_source_and_pure_codec_tool_return.json').write_text(json.dumps(receipt,indent=2)+'\n')
final=dict(schema='AXMAT_COMPLETE_GRAPH_CANONICAL_FILE_TABLE_OWNED_CONSUME_SOURCE_ONLY_FINAL_REVIEW_V1',status='PASS_SOURCE_AND_PURE_CODEC_ONLY_UNREADY',candidate=dict(path=str(D/N),sha256=sha(D/N),identity=identity(D/N)),pure_codec_report=dict(path=str(D/'PURE_CODEC_REPORT.json'),sha256=sha(D/'PURE_CODEC_REPORT.json')),true_actual_tool_receipt=dict(path=str(D/'actual_source_and_pure_codec_tool_return.json'),sha256=sha(D/'actual_source_and_pure_codec_tool_return.json')),frozen_abb5_and_original_41_control_evidence_fresh_pins=oldpins,full_eight_region_inverse_to_1d7=True,three_regions_to_abb5=True,unchanged_original_functions_count=len(same),public_default_decoder_nonmutating=True,encoder_byteexact_to_abb5=True,two_wrappers_consume_only_owned_new_parse=True,rows_release_observed_primitive_only=True,original_max_json_bytes=67108864,original_decoded_schema_columns_values_order_and_content_digest_preserved=True,original_failed_graph_roundtrip=dict(canonical_files=36776,original_bytes=67624825,diagnostic_bytes=66558451,headroom_bytes=550413),total_controls=59,original_controls=41,new_owned_consume_controls=18,formal_new_graph=None,actual_V12_PREP=None,actual_V12_RUN=None,native_or_science_credit=False,business_module_imported=False,business_API_executed=False,project_written=False,limitations=['Strict file wrapper executed only as isolated AST source using STDlib bounded TMP fixture reader adapters; original alias/stream/business gates not invoked.','Rows lifetime evidence is source and pure primitive observation only; no business process RSS measurement or512MiB qualification.','Diagnostic stored graph is TMP-only. Root must generate a unique formal complete V12 graph and independently run all unchanged original gates.'])
(D/'FINAL_REPORT.json').write_text(json.dumps(final,indent=2)+'\n')
(D/'REPORT.txt').write_text('新最小owned consume修订仅TMP SOURCE与pure codec通过，仍UNREADY。\n公开默认decode和encoder不改调用者输入；两个strict wrapper在原严格JSON解析后，仅消费自己新parse的行表。\n逐row完整scalar转freshdict后置None，全部完成clear；primitive实证content SHA前旧rows为空，不能据此声称业务RSS512MiB通过。\n完整8区域逆向1d7、3区域逆向冻结abb5；原67函数逐字、所有schema/values/limits/math/verify/phase/lineage不改。\n真实旧graph67624825B -> 诊断透明表66558451B，原64MiB余550413B；36776 canonical行、全decoded对象typed/order/IEEE floatbits/content摘要保持。\n41原控制＋18新增控制共59通过，两实际pure reviewer失败均原样保留，仅修测试namespace及原parser排序边界，无业务重试。\n未写项目或正式graph，未导入业务、调用API/phase/controller/native/compiler。Root另建unique V12正式图后仍须完整原gate准入。\n')
manifest=[]
for p in sorted(D.rglob('*')):
 if p.is_file() and p.name!='evidence_file_manifest.json':manifest.append(dict(path=str(p),sha256=sha(p),size=p.stat().st_size))
(D/'evidence_file_manifest.json').write_text(json.dumps(dict(schema='OWNED_CONSUME_SOURCE_AND_PURE_CODEC_EVIDENCE_MANIFEST_V1',files=manifest),indent=2)+'\n')
print(json.dumps(dict(status=final['status'],final_report_sha256=sha(D/'FINAL_REPORT.json'),pure_report_sha256=sha(D/'PURE_CODEC_REPORT.json'),actual_receipt_sha256=sha(D/'actual_source_and_pure_codec_tool_return.json'),evidence_manifest_sha256=sha(D/'evidence_file_manifest.json'),source_sha256=sha(D/N),controls=59)))
