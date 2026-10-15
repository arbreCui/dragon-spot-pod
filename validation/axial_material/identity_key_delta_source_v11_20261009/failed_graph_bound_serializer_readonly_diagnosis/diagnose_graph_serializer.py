import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path

D=Path('/private/tmp/axmat_v11_failed_graph_bound_serializer_readonly_diagnosis_20261009')
ROOT=Path('/Users/wen/spot')
AM=ROOT/'validation/axial_material'
OUT=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-cross-group-identity-key-delta-live-resource-scopes-v11-20261009'
F=AM/'prepare_historical_input_owned_specs_cross_group_identity_key_delta_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v11.py'
H=AM/'combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
G=OUT/'input_graph.json'
STDERR=AM/'identity_key_delta_combined_runtime_review_v11_20261009/run_build.stderr'
CAP=64*1024*1024
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
paths=(F,H,G,STDERR)
before={str(p):identity(p) for p in paths}
factory=F.read_text();helper=H.read_text();failure=STDERR.read_text()
assert sha(helper.encode())=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
ft=ast.parse(factory);ht=ast.parse(helper)
fa={n.name:n for n in ft.body if isinstance(n,ast.FunctionDef)}
ha={n.name:n for n in ht.body if isinstance(n,ast.FunctionDef)}
writer=ast.get_source_segment(factory,fa['create_complete_input_graph'])
assert "json.dump(graph,f,separators=(',',':'),allow_nan=False);f.write('\\n')" in writer
assert 'write_graph' not in ha
reader=ast.get_source_segment(helper,ha['strict_json']);stream=ast.get_source_segment(helper,ha['_stream'])
assert any(isinstance(n.value,ast.BinOp) and ast.literal_eval(n.value.left)==64 and ast.literal_eval(n.value.right)==1024*1024 for n in []) is False
maxnode=next(n.value for n in ht.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='MAX_JSON_BYTES')
assert ast.dump(maxnode)==ast.dump(ast.parse('64 * 1024 * 1024',mode='eval').body)
assert isinstance(ha['strict_json'].args.kw_defaults[-1],ast.Name) and ha['strict_json'].args.kw_defaults[-1].id=='MAX_JSON_BYTES'
assert '_require(before.st_size <= max_bytes' in stream and '_stream(canonical, collect=True, max_bytes=max_bytes)' in reader
assert 'input exceeds read bound' in failure and str(G) in failure
raw_hash=hashlib.sha256();body_hash=hashlib.sha256();size=0;nonascii=0
in_string=False;escaped=False;format_whitespace=0;unicode_escape_count=0
fd=os.open(G,os.O_RDONLY|os.O_NOFOLLOW)
try:
 assert identity(G)==before[str(G)]
 while chunk:=os.read(fd,1024*1024):
  raw_hash.update(chunk);size+=len(chunk)
  for byte in chunk:
   nonascii+=byte>=128
   if in_string:
    if escaped:
     unicode_escape_count+=byte==117;escaped=False
    elif byte==92:escaped=True
    elif byte==34:in_string=False
   elif byte==34:in_string=True
   elif byte in (9,10,13,32):format_whitespace+=1
 assert not in_string and not escaped and size==before[str(G)]['size']
finally:os.close(fd)
assert size==67624825 and format_whitespace==1 and nonascii==unicode_escape_count==0
assert size>CAP
# The producer wrote exactly one trailing newline; no alternative whitespace exists.
with G.open('rb') as f:
 remain=size-1
 while remain:
  chunk=f.read(min(1024*1024,remain));assert chunk;body_hash.update(chunk);remain-=len(chunk)
 assert f.read()==b'\n'
def pairs(items):
 d={}
 for key,value in items:
  if key in d:raise ValueError('duplicate JSON key')
  d[key]=value
 return d
def reject(value):raise ValueError('nonfinite JSON: '+value)
with G.open('r',encoding='utf-8') as f:graph=json.load(f,object_pairs_hook=pairs,parse_constant=reject)
counts={name:0 for name in ('dict','list','str','int','float','bool','null')}
stack=[graph]
while stack:
 item=stack.pop();kind=type(item)
 if kind is dict:counts['dict']+=1;stack.extend(item.values());assert all(type(k)is str for k in item)
 elif kind is list:counts['list']+=1;stack.extend(item)
 elif kind is str:counts['str']+=1
 elif kind is int:counts['int']+=1
 elif kind is float:counts['float']+=1;assert math.isfinite(item)
 elif kind is bool:counts['bool']+=1
 elif item is None:counts['null']+=1
 else:raise TypeError(kind)
def encoded_measure(value,*,ensure_ascii,sort_keys):
 encoder=json.JSONEncoder(ensure_ascii=ensure_ascii,sort_keys=sort_keys,separators=(',',':'),allow_nan=False)
 h=hashlib.sha256();total=0
 for piece in encoder.iterencode(value):
  b=piece.encode('utf-8');h.update(b);total+=len(b)
 return dict(bytes=total,sha256=h.hexdigest())
compact_ascii=encoded_measure(graph,ensure_ascii=True,sort_keys=False)
compact_utf8=encoded_measure(graph,ensure_ascii=False,sort_keys=False)
assert compact_ascii==compact_utf8 and compact_ascii['bytes']==size-1
assert compact_ascii['sha256']==body_hash.hexdigest()
original_content=graph['content_sha256'];content_view=dict(graph);content_view.pop('content_sha256')
content=encoded_measure(content_view,ensure_ascii=True,sort_keys=True);assert content['sha256']==original_content
for p in paths:assert identity(p)==before[str(p)]
absent=[OUT/name for name in ('execution_claim.json','driver_result.json','seal.json','HISTORICAL_INPUT_CROSS_GROUP_IDENTITY_KEY_DELTA_COMBINED_RUNTIME_LINK_V11/stages.json')]
assert all(not os.path.lexists(p) for p in absent)
wire=graph['requirements'];rows=wire.get('rows')
row_summary=dict(type=type(rows).__name__,schema=rows.get('schema') if isinstance(rows,dict) else None,row_count=rows.get('row_count') if isinstance(rows,dict) else len(rows))
report=dict(schema='AXMAT_V11_ACTUAL_FAILED_GRAPH_READ_BOUND_SERIALIZER_DIAGNOSIS_V1',status='PASS_READONLY_DIAGNOSIS_NO_WHITESPACE_FIX_AVAILABLE',
 graph=dict(path=str(G),sha256=raw_hash.hexdigest(),identity=before[str(G)],bytes=size,original_max_bytes=CAP,excess_bytes=size-CAP),
 actual_writer=dict(path=str(F),sha256=sha(factory.encode()),function='create_complete_input_graph',format='json.dump separators comma/colon, allow_nan false, default ensure_ascii true, no indent; one EOF newline',helper_has_write_graph_function=False),
 reader=dict(path=str(H),sha256=sha(helper.encode()),max_json_bytes=CAP,strict_json_default_bound_unchanged=True,stat_gate_rejects_before_JSON_parse=True),
 full_builtin_JSON_read=dict(duplicate_keys_rejected=True,nonfinite_rejected=True,all_builtin_plain_types=True,complete_type_counts=counts),
 whitespace=dict(outside_strings=format_whitespace,only_trailing_newline=True,nonASCII_bytes=nonascii,unicode_escapes=unicode_escape_count),
 compact_ASCII=compact_ascii,compact_UTF8=compact_utf8,
 all_three_compact_original_same_whole_JSON_order_type_float_and_literal_strings='Both builtin compact encoders reproduce the exact original bytes excluding one EOF newline; bytes identical, so every JSON field/order/type/floatbit/string/duplicate row and graph edge is unchanged.',
 compact_still_exceeds_original_cap_bytes=compact_ascii['bytes']-CAP,
 content_digest=dict(saved=original_content,recomputed_stdlib_sorted_canonical=content['sha256'],equal=True),
 complete_graph_metadata_counts=dict(canonical_files=len(graph['canonical_files']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),absence_inputs=len(graph['absence_inputs']),live_resource_roots=len(graph['live_resource_roots']),requirement_rows=row_summary),
 source_and_graph_metadata_before_after_equal=True,
 failed_run=dict(stderr=dict(path=str(STDERR),sha256=sha(failure.encode()),bytes=before[str(STDERR)]['size']),missing_before_compile=[str(p) for p in absent],success_promoted=False),
 source_fix_draft=None,source_fix_status='UNREADY_UNIMPLEMENTABLE_AS_WHITESPACE_ONLY',
 next_step_requires_Root_choice='A separately reviewed explicit lossless graph wire codec/schema could remove repeated representation while decoding every original field and edge. No codec is implemented or approved here.',
 formal_graph_rewritten=False,max_read_bound_raised=False,fields_filtered=False,owner_edges_pruned=False,
 business_imported=False,business_executed=False,compiled=False,project_written=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('真实V11 combined失败发生在全图读取前的64MiB stat门，尚无execution_claim/driver_result/stages/seal。\n'
 'graph原始67,624,825B，超过67,108,864B原门515,961B。真实writer在combined create_complete_input_graph，不在graph helper；已是无indent紧凑JSON。\n'
 '全图STDlib严格JSON读取并重编码：仅EOF换行1B；无unicode转义/非ASCII字符。ensure_ascii True/False都得67,624,824B，仍超门515,960B。\n'
 '两种compact字节全文SHA与原图去1B换行完全相同，全部值、顺序、类型、浮点、字面字符串、所有owner/rows/ns/alias不变；canonical content SHA重新计算完全等于原图。\n'
 '因此不能交付满足原门的whitespace-only修复；未伪造新helper/新图/READY。原图和1d7 helper不改，读取上限不改。\n'
 '后续若要压缩完整表示，须Root选择单独lossless wire codec/schema审查；本轮没有实现该codec，更没有business或科学资格。\n')
print(json.dumps(dict(status=report['status'],graph_sha256=raw_hash.hexdigest(),bytes=size,cap=CAP,compact_bytes=compact_ascii['bytes'],compact_excess=compact_ascii['bytes']-CAP,format_whitespace=1,unicode_escapes=0,saved_content_sha256=original_content,recomputed_content_sha256=content['sha256'],report_sha256=sha((D/'REPORT.json').read_bytes()))))
