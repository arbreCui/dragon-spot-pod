import ast
import copy
import gc
import hashlib
import json
import math
import os
import stat
import struct
from pathlib import Path

D=Path('/private/tmp/axmat_complete_graph_canonical_file_table_owned_consume_source_draft_20261009')
P=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py')
C=D/'combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
G=Path('/Users/wen/spot/validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-cross-group-identity-key-delta-live-resource-scopes-v11-20261009/input_graph.json')
CAP=67108864
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
before={str(p):identity(p) for p in (P,C,G)}
parent=P.read_text();candidate=C.read_text();assert sha(parent.encode())=='1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'
assert sha(candidate.encode())=='b607c5e5ff9614d48a17e32df9605f7d29d3c7d685228caf5af01530319ef5d9'
BASE_NAMES={'_require','_path','_sha','_content_digest','_unique_object','_invalid_constant','_finite_float','_unique_sorted_object','_parse_strict_json_text','_parse_strict_json_payload'}
NEW_NAMES={'_canonical_file_storage_values','encode_canonical_file_table_storage','decode_canonical_file_table_storage','strict_json'}
def pure_namespace(source,allow):
 tree=ast.parse(source)
 constants={}
 for n in tree.body:
  if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
   try:constants[n.targets[0].id]=ast.literal_eval(n.value)
   except (ValueError,TypeError):pass
 env={'json':json,'hashlib':hashlib,'os':os,'math':math,'MAX_JSON_BYTES':CAP,**constants}
 nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in allow or isinstance(n,ast.ClassDef) and n.name=='InputGraphError']
 assert {n.name for n in nodes if isinstance(n,ast.FunctionDef)}==allow
 code=compile(ast.Module(body=nodes,type_ignores=[]),'<isolated-pure-json-codec-only>','exec')
 exec(code,env)
 return env
old=pure_namespace(parent,BASE_NAMES);new=pure_namespace(candidate,BASE_NAMES|NEW_NAMES)
encode=new['encode_canonical_file_table_storage'];decode=new['decode_canonical_file_table_storage']
def whole_typed_order_signature(value):
 digest=hashlib.sha256();counts={};pending=[value]
 while pending:
  item=pending.pop();kind=type(item);tag=kind.__name__;counts[tag]=counts.get(tag,0)+1;digest.update(tag.encode()+b':')
  if kind is dict:
   digest.update(str(len(item)).encode()+b':')
   for k,v in reversed(list(item.items())):pending.append(v);pending.append(k)
  elif kind is list:
   digest.update(str(len(item)).encode()+b':');pending.extend(reversed(item))
  elif kind is str:
   raw=item.encode('utf-8');digest.update(str(len(raw)).encode()+b':'+raw)
  elif kind is float:digest.update(struct.pack('>d',item))
  elif kind is int:digest.update(str(item).encode())
  elif kind is bool:digest.update(b'1' if item else b'0')
  elif item is None:digest.update(b'null')
  else:raise TypeError(kind)
  digest.update(b';')
 return dict(sha256=digest.hexdigest(),counts=counts)
def measure(value):
 enc=json.JSONEncoder(separators=(',',':'),allow_nan=False);h=hashlib.sha256();size=0
 for piece in enc.iterencode(value):
  raw=piece.encode();h.update(raw);size+=len(raw)
 return dict(bytes=size,sha256=h.hexdigest())
raw=G.read_bytes();assert sha(raw)=='02c379cc436856ceeca047ef1d242a6ce6571ba61a687ab679ac6593e77d0594'
original=old['_parse_strict_json_payload'](raw,str(G));del raw;gc.collect()
original_sig=whole_typed_order_signature(original)
old_content=original['content_sha256'];assert old['_content_digest'](original)==old_content
keys={tuple(row) for row in original['canonical_files']};assert keys=={('path','sha256','size_bytes')}
count=len(original['canonical_files']);row_duplicates=count-len({(r['path'],r['sha256'],r['size_bytes']) for r in original['canonical_files']})
original_measure=measure(original)
stored=encode(original);assert whole_typed_order_signature(original)==original_sig
assert stored['graph']['content_sha256']==old_content
fixture=D/'diagnostic_actual_failed_graph_canonical_file_table_storage.json'
with fixture.open('x',encoding='utf-8') as f:
 json.dump(stored,f,separators=(',',':'),allow_nan=False);f.write('\n')
fixture_pin=dict(path=str(fixture),sha256=sha(fixture.read_bytes()),identity=identity(fixture))
actual_storage_bytes=fixture.stat().st_size
assert actual_storage_bytes<CAP and CAP-actual_storage_bytes>256*1024
print(json.dumps(dict(stage='DIAGNOSTIC_FIXTURE_CLOSED_NOT_QUALIFICATION',canonical_rows=count,storage_bytes=actual_storage_bytes,original_bytes=before[str(G)]['size'],headroom=CAP-actual_storage_bytes,source_sha256=sha(candidate.encode()))),flush=True)
logical_rows=original['requirements']['rows']['row_count'];scope_counts=dict(canonical_files=count,requirement_rows=logical_rows,namespaces=len(original['namespaces']),aliases=len(original['aliases']),absence_inputs=len(original['absence_inputs']),live_resource_roots=len(original['live_resource_roots']))
del original,stored;gc.collect()
raw=fixture.read_bytes();assert len(raw)==actual_storage_bytes and len(raw)<CAP
# Only the pure UTF-8/JSON wrapper and new pure codec execute; no file/API/phase helper.
decoded=new['_parse_strict_json_payload'](raw,str(fixture));del raw;gc.collect()
decoded_sig=whole_typed_order_signature(decoded);assert decoded_sig==original_sig
assert decoded['content_sha256']==old_content and new['_content_digest'](decoded)==old_content
decoded_measure=measure(decoded);assert decoded_measure==original_measure
assert type(decoded['canonical_files'])is list and len(decoded['canonical_files'])==count
assert all(tuple(row)==('path','sha256','size_bytes') for row in decoded['canonical_files'])
del decoded;gc.collect()
def model():
 graph=dict(schema=new['WIRE_GRAPH_SCHEMA'],scope=new['INPUT_SCOPE'],canonical_files=[dict(path='/tmp/same',sha256='1'*64,size_bytes=0),dict(path='/tmp/same',sha256='1'*64,size_bytes=0),dict(path='/tmp/other',sha256='2'*64,size_bytes=2**70)],extra=dict(negative_zero=-0.0,positive_zero=0.0,value=0.1,unicode='燃料α',literal='\\u4e00',flag=True,nothing=None,rows=[[1,1],[1,1]],shape={'x':{'s':'same'},'y':{'s':'same'}}))
 graph['content_sha256']=new['_content_digest'](graph);return graph
results=[]
for case in ('duplicate_rows','unicode_literal_strings','float_bits_int_bool_null','new_mutable_containers'):
 m=model();snapshot=copy.deepcopy(m);storage=encode(m);stored_snapshot=copy.deepcopy(storage);decoded=decode(storage)
 assert whole_typed_order_signature(decoded)==whole_typed_order_signature(m) and decoded==m
 assert m==snapshot and storage==stored_snapshot
 assert decoded['canonical_files']is not m['canonical_files'] and decoded['canonical_files'][0]is not m['canonical_files'][0]
 assert decoded['canonical_files'][0]is not decoded['canonical_files'][1]
 assert len(decoded['canonical_files'])==3
 results.append(dict(case=case,expected='ROUNDTRIP',observed='ROUNDTRIP'))
def bad(name,mutate,which='decode'):
 m=model();storage=encode(m)
 value=storage if which=='decode' else m
 mutate(value)
 try:(decode if which=='decode' else encode)(value)
 except new['InputGraphError'] as e:results.append(dict(case=name,expected='REJECT',observed='REJECT',message=str(e)))
 else:raise AssertionError(name)
bad('wrong_storage_schema',lambda s:s.update(schema='wrong'))
bad('extra_outer_field',lambda s:s.update(extra=True))
bad('missing_outer_graph',lambda s:s.pop('graph'))
bad('wrong_decoded_schema',lambda s:s['graph'].update(schema='wrong'))
bad('wrong_scope',lambda s:s['graph'].update(scope='wrong'))
bad('extra_table_field',lambda s:s['graph']['canonical_files'].update(extra=0))
bad('bad_column_order',lambda s:s['graph']['canonical_files']['columns'].reverse())
bad('duplicate_columns',lambda s:s['graph']['canonical_files'].update(columns=['path','path','size_bytes']))
bad('missing_column',lambda s:s['graph']['canonical_files'].update(columns=['path','sha256']))
bad('row_short',lambda s:s['graph']['canonical_files']['rows'][0].pop())
bad('row_long',lambda s:s['graph']['canonical_files']['rows'][0].append(0))
bad('row_not_list',lambda s:s['graph']['canonical_files']['rows'].__setitem__(0,tuple(s['graph']['canonical_files']['rows'][0])))
bad('bool_size',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(2,False))
bad('negative_size',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(2,-1))
bad('path_not_string',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(0,123))
bad('path_not_absolute',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(0,'relative'))
bad('bad_sha',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(1,'F'*64))
bad('changed_value',lambda s:s['graph']['canonical_files']['rows'][0].__setitem__(2,1))
bad('omitted_row',lambda s:s['graph']['canonical_files']['rows'].pop())
bad('extra_duplicate_row',lambda s:s['graph']['canonical_files']['rows'].append(list(s['graph']['canonical_files']['rows'][0])))
bad('changed_other_graph_field',lambda s:s['graph']['extra'].update(flag=False))
bad('wrong_content_digest',lambda s:s['graph'].update(content_sha256='f'*64))
bad('encoder_extra_pin_field',lambda g:g['canonical_files'][0].update(unexpected=True),'encode')
bad('encoder_missing_pin_field',lambda g:g['canonical_files'][0].pop('sha256'),'encode')
bad('encoder_bool_size',lambda g:g['canonical_files'][0].update(size_bytes=True),'encode')
# Original ordinary JSON remains identical, including rejection class/message.
ordinary=[b'null',b'true',b'[1,-0.0,0.0,0.1,"same","\\\\u1234",{"b":1,"a":2}]',b'{"schema":"ordinary","nested":{"b":true,"a":null}}',b'{"dup":1,"dup":2}',b'NaN',b'{"x":1e9999}',b'\xff',b'{"broken":',b'{"x":'+b'9'*4301+b'}']
for index,payload in enumerate(ordinary):
 observations=[]
 for ns in (old,new):
  try:v=ns['_parse_strict_json_payload'](payload,'/pure/model');observations.append(('RETURN',whole_typed_order_signature(v)))
  except Exception as e:observations.append((type(e).__name__,str(e)))
 assert observations[0]==observations[1],(index,observations)
 results.append(dict(case='ordinary_'+str(index),observed=observations[1][0],equal_to_parent=True))
for name,payload in (('truncated_storage_EOF',json.dumps(encode(model())).encode()[:-1]),('duplicate_storage_header',b'{"schema":"one","schema":"two"}')):
 try:new['_parse_strict_json_payload'](payload,'/pure/bad')
 except new['InputGraphError'] as e:results.append(dict(case=name,expected='REJECT',observed='REJECT',message=str(e)))
 else:raise AssertionError(name)

# Additional tests execute only selected pure functions and strict_json's source
# wrapper with independently bounded STDlib fixture-reader adapters. No original
# business filesystem/alias resolver, graph verifier, phase or API is loaded.
initial_count=len(results);assert initial_count==41
owned_results=[]
def positive(name):
 owned_results.append(dict(case=name,expected='PASS',observed='PASS'))
for rows_count in (0,3):
 m=model()
 if rows_count==0:
  m['canonical_files']=[];m['content_sha256']=new['_content_digest'](m)
 storage=encode(m);snapshot=copy.deepcopy(storage)
 default=decode(storage)
 assert storage==snapshot and whole_typed_order_signature(default)==whole_typed_order_signature(m)
 positive('default_nonmutation_rows_'+str(rows_count))
 rows=storage['graph']['canonical_files']['rows'];original_values=copy.deepcopy(rows)
 check_calls=[];digest_calls=[]
 real_values=new['_canonical_file_storage_values'];real_digest=new['_content_digest']
 def progressive_values(row):
  index=len(check_calls)
  assert rows[:index]==[None]*index and row==original_values[index]
  assert rows[index:]==original_values[index:]
  check_calls.append(index)
  return real_values(row)
 def digest_after_release(value):
  assert rows==[]
  assert value['canonical_files']==m['canonical_files']
  digest_calls.append(True)
  return real_digest(value)
 new['_canonical_file_storage_values']=progressive_values
 new['_content_digest']=digest_after_release
 try:restored=decode(storage,_consume=True)
 finally:new['_canonical_file_storage_values']=real_values;new['_content_digest']=real_digest
 assert len(check_calls)==rows_count and digest_calls==[True] and rows==[]
 assert whole_typed_order_signature(restored)==whole_typed_order_signature(m)
 assert all(type(pin)is dict for pin in restored['canonical_files'])
 positive('owned_progressive_release_before_content_digest_rows_'+str(rows_count))
for flag in (0,1,None,'yes'):
 storage=encode(model());snapshot=copy.deepcopy(storage)
 try:decode(storage,_consume=flag)
 except new['InputGraphError'] as e:
  assert str(e)=='invalid private canonical-file storage consume flag'
  assert storage==snapshot
  owned_results.append(dict(case='invalid_private_consume_flag_'+repr(flag),expected='REJECT',observed='REJECT',message=str(e)))
 else:raise AssertionError(flag)
for name,mutation in (
 ('owned_invalid_header_before_rows',lambda x:x.update(schema='wrong')),
 ('owned_bad_column_order',lambda x:x['graph']['canonical_files']['columns'].reverse()),
 ('owned_second_row_bool_size',lambda x:x['graph']['canonical_files']['rows'][1].__setitem__(2,False)),
 ('owned_content_digest_after_release',lambda x:x['graph'].update(content_sha256='f'*64))):
 storage=encode(model());mutation(storage);rows=storage['graph']['canonical_files']['rows']
 try:decode(storage,_consume=True)
 except new['InputGraphError'] as e:
  if name=='owned_second_row_bool_size':assert rows[0]is None and rows[1][2]is False and type(rows[2])is list
  elif name=='owned_content_digest_after_release':assert rows==[]
  else:assert len(rows)==3 and all(type(row)is list for row in rows)
  owned_results.append(dict(case=name,expected='REJECT',observed='REJECT',message=str(e)))
 else:raise AssertionError(name)
# The two real wrappers both call the private consume branch on their newly
# parsed container; these hooks observe release rather than mimic that branch.
real_decode=new['decode_canonical_file_table_storage'];wrapper_calls=[]
def spy_decode(storage,*,_consume=False):
 assert _consume is True
 rows=storage['graph']['canonical_files']['rows'];old_rows=copy.deepcopy(rows)
 value=real_decode(storage,_consume=_consume)
 assert rows==[] and value['canonical_files']==[dict(zip(new['CANONICAL_FILE_TABLE_STORAGE_COLUMNS'],row)) for row in old_rows]
 wrapper_calls.append(dict(private_consume=_consume,rows_before=len(old_rows),rows_after=len(rows)))
 return value
new['decode_canonical_file_table_storage']=spy_decode
fixture_reads=[]
def empty_aliases_fixture(aliases):
 assert aliases==();return {}
def direct_fixture_resolve(path,declared,*,kind):
 assert declared=={} and kind=='file' and Path(path).parent==D
 return path
def bounded_fixture_stream(path,*,collect,max_bytes):
 assert collect is True and type(max_bytes)is int and max_bytes>0
 path=Path(path);pre=identity(path)
 new['_require'](pre['size']<=max_bytes,'fixture JSON input exceeds read bound')
 fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb') as f:payload=f.read(max_bytes+1)
 new['_require'](len(payload)<=max_bytes,'fixture JSON input exceeds read bound')
 assert identity(path)==pre and len(payload)==pre['size']
 fixture_reads.append(dict(path=str(path),sha256=sha(payload),identity_before_after_equal=True,max_bytes=max_bytes))
 return dict(path=str(path),sha256=sha(payload),size_bytes=len(payload)),payload
new['_alias_map']=empty_aliases_fixture;new['_resolve']=direct_fixture_resolve;new['_stream']=bounded_fixture_stream
m=model();payload=(json.dumps(encode(m),separators=(',',':'),allow_nan=False)+'\n').encode()
unchanged_payload=bytes(payload)
value=new['_parse_strict_json_payload'](payload,'/pure/owned-payload')
assert payload==unchanged_payload and whole_typed_order_signature(value)==whole_typed_order_signature(m)
positive('payload_wrapper_new_owned_parse_complete_release')
smallfixture=D/'owned_wrapper_small_fixture.json'
with smallfixture.open('xb') as f:f.write(payload)
pin=sha(payload);value=new['strict_json'](str(smallfixture),pin)
assert whole_typed_order_signature(value)==whole_typed_order_signature(m)
assert len(wrapper_calls)==2 and all(call['private_consume']is True and call['rows_before']==3 and call['rows_after']==0 for call in wrapper_calls)
positive('strict_json_wrapper_new_owned_parse_complete_release')
try:new['strict_json'](str(smallfixture),'f'*64)
except new['InputGraphError'] as e:
 assert str(e)=='JSON digest changed: '+str(smallfixture)
 assert len(wrapper_calls)==2
 owned_results.append(dict(case='strict_fixture_wrong_digest_before_decoder',expected='REJECT',observed='REJECT',message=str(e)))
else:raise AssertionError('wrong digest')
try:new['strict_json'](str(smallfixture),pin,max_bytes=len(payload)-1)
except new['InputGraphError'] as e:
 assert str(e)=='fixture JSON input exceeds read bound' and len(wrapper_calls)==2
 owned_results.append(dict(case='strict_fixture_read_bound_before_decoder',expected='REJECT',observed='REJECT',message=str(e)))
else:raise AssertionError('read bound')
ordinary_payload=b'{"schema":"ordinary","nested":{"b":1,"a":-0.0}}'
ordinaryfixture=D/'owned_wrapper_ordinary_fixture.json'
with ordinaryfixture.open('xb') as f:f.write(ordinary_payload)
ordinary_parsed=new['strict_json'](str(ordinaryfixture),sha(ordinary_payload))
assert whole_typed_order_signature(ordinary_parsed)==whole_typed_order_signature(old['_parse_strict_json_payload'](ordinary_payload,str(ordinaryfixture)))
assert len(wrapper_calls)==2
positive('strict_json_ordinary_schema_does_not_enter_decoder')
# Full failed-graph fixture through actual strict_json source wrapper as well as
# the actual owned payload wrapper exercised above. Reader adapters are scoped
# isolated TMP fresh pin/bound I/O, not original business admission helpers.
large_decoded=new['strict_json'](str(fixture),fixture_pin['sha256'])
assert whole_typed_order_signature(large_decoded)==original_sig
assert new['_content_digest'](large_decoded)==old_content
assert measure(large_decoded)==original_measure
assert wrapper_calls[-1]==dict(private_consume=True,rows_before=count,rows_after=0)
del large_decoded;gc.collect()
positive('strict_json_wrapper_full_old_graph_roundtrip_owned_release')
new['decode_canonical_file_table_storage']=real_decode
results.extend(owned_results)

assert before=={str(p):identity(p) for p in (P,C,G)}
report=dict(schema='AXMAT_COMPLETE_GRAPH_CANONICAL_FILE_TABLE_STORAGE_PURE_CODEC_DIAGNOSIS_V1',status='PASS_PURE_CODEC_SOURCE_ONLY_UNREADY',
 source=dict(path=str(C),sha256=sha(candidate.encode()),identity=before[str(C)]),parent=dict(path=str(P),sha256=sha(parent.encode()),identity=before[str(P)]),
 actual_failed_graph=dict(path=str(G),sha256='02c379cc436856ceeca047ef1d242a6ce6571ba61a687ab679ac6593e77d0594',identity=before[str(G)]),
 exact_canonical_pin_columns=['path','sha256','size_bytes'],actual_canonical_pin_row_count=count,actual_canonical_duplicate_rows=row_duplicates,
 scope_counts=scope_counts,diagnostic_fixture_only=fixture_pin,original_stored_bytes=before[str(G)]['size'],diagnostic_stored_bytes=actual_storage_bytes,
 savings_bytes=before[str(G)]['size']-actual_storage_bytes,unchanged_max_json_bytes=CAP,headroom_bytes=CAP-actual_storage_bytes,
 full_decoded_original_graph_equal=True,whole_typed_order_and_IEEE_float_bits=original_sig,decoded_whole_typed_order_and_IEEE_float_bits=decoded_sig,
 complete_original_graph_json_measure=original_measure,complete_decoded_graph_json_measure=decoded_measure,unchanged_original_content_sha256=old_content,
 every_row_value_type_order_and_duplicate_preserved=True,all_original_noncanonical_graph_values_preserved=True,source_and_data_seven_identity_before_after_equal=True,
 controls=results,control_count=len(results),encoder_and_public_default_decoder_do_not_mutate_inputs=True,private_owned_consume_clears_parsed_rows_only=True,owned_consume_controls=owned_results,owned_consume_control_count=len(owned_results),two_real_strict_wrapper_calls_observed=wrapper_calls,isolated_stdlib_fixture_reader_adapters=fixture_reads,strict_wrapper_adapter_scope='Actual source wrapper with isolated fixture I/O adapters; original business resolver/stream/phase/API not executed',rows_lifetime_evidence='Source plus primitive observation of rows[i]=None and empty rows before content digest; no actual business RSS measurement',restored_canonical_pin_dicts_are_independent=True,
 both_strict_wrappers_schema_gated_after_original_parser=True,complete_eight_region_inverse_to_1d7=True,additional_three_region_inverse_to_frozen_abb5=True,original_verify_graph_phase_lineage_parse_text_and_math_byteexact=True,
 new_helper_source_size_delta_bytes=len(candidate.encode())-len(parent.encode()),
 allowance_for_new_source_owner_bytes='Measured diagnostic headroom is over256KiB, much larger than the new helper source delta and ordinary path/hash/row metadata. Actual V12 newly generated full graph size/owners must still pass the original64MiB gate; this is not a claimed V12 graph.',
 business_module_imported=False,business_API_or_phase_executed=False,controller_or_compiler_executed=False,project_written=False,
 helper_status='UNREADY_SOURCE_ONLY_PENDING_ROOT_REVIEW',formal_new_graph_created=False,actual_new_combined_build=None,
 native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,
 limit='Only isolated pure AST metadata codec/UTF8 JSON wrapper tests, strict_json source wrapper with STDlib TMP fixture reader adapters, and the old failed graph diagnostic fixture. No source/env/module constructor or full fresh INPUT/API gates run; Root must create unique new source/OUT/TERM and perform separate full qualification.')
(D/'PURE_CODEC_REPORT.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('canonical_files显式三列无损存储已在TMP pure codec验证，helper仍UNREADY。\n'
 f'真实旧graph={before[str(G)]["size"]}B；透明诊断storage={actual_storage_bytes}B；节省{before[str(G)]["size"]-actual_storage_bytes}B，原64MiB门余{CAP-actual_storage_bytes}B。\n'
 f'实际{count}个canonical pin全部3字段/值/型/行序保持；整个decoded JSON typed-order/IEEE浮点位及content_sha逐项全遍历摘要相同。\n'
 '普通JSON保持原入口结果及异常；新strict_json和fresh parent payload wrapper都仅exact新storage schema decode，原parse_text/verify_graph/_phase/consumer_lineage/所有数学和原bound逐字不改。\n'
 f'{len(results)}项必要pure roundtrip/reject/ordinary兼容控制通过，坏列/坏行/bool尺寸/缺行/多行/坏header/content/truncatedEOF被拒绝。\n'
 'encode新浅storage view和公开decode默认不改原输入；两个strict wrapper仅对自己新parse容器逐row置None，全部转移后clear，内容SHA前释放；其证据限源码和primitive，不是业务RSS测量。不复制整graph，不维护globalcache。\n'
 '未写项目，未导入业务/调用phase/API/控制器/编译器；诊断fixture不作为正式V12图或成功凭据。新真实V12图仍须原限额内完整PREP与5stage独立审查。\n')
print(json.dumps(dict(status=report['status'],source_sha256=sha(candidate.encode()),canonical_rows=count,original_bytes=before[str(G)]['size'],storage_bytes=actual_storage_bytes,savings=report['savings_bytes'],headroom=report['headroom_bytes'],controls=len(results),report_sha256=sha((D/'PURE_CODEC_REPORT.json').read_bytes()))))
