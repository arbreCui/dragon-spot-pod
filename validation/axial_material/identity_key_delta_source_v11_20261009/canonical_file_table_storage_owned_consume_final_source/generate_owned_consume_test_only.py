from pathlib import Path

D=Path('/private/tmp/axmat_complete_graph_canonical_file_table_owned_consume_source_draft_20261009')
BASE=Path('/private/tmp/axmat_complete_graph_canonical_file_table_storage_source_draft_20261009')
s=(BASE/'test_pure_storage_codec.py').read_text()
s=s.replace(str(BASE),str(D))
s=s.replace('abb5aef91e6a2032c708c87a14fddf3a89e9798cf37d3e153233d8062c41920f','b607c5e5ff9614d48a17e32df9605f7d29d3c7d685228caf5af01530319ef5d9')
s=s.replace("env={'json':json,'hashlib':hashlib,'os':os,'math':math,**constants}","env={'json':json,'hashlib':hashlib,'os':os,'math':math,'MAX_JSON_BYTES':CAP,**constants}")
s=s.replace("NEW_NAMES={'_canonical_file_storage_values','encode_canonical_file_table_storage','decode_canonical_file_table_storage'}","NEW_NAMES={'_canonical_file_storage_values','encode_canonical_file_table_storage','decode_canonical_file_table_storage','strict_json'}")
marker='assert before=={str(p):identity(p) for p in (P,C,G)}'
extra=r'''
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
wrapper_expected=old['_parse_strict_json_payload'](json.dumps(m,separators=(',',':'),allow_nan=False).encode(),'/pure/original-model-parser-boundary')
value=new['_parse_strict_json_payload'](payload,'/pure/owned-payload')
assert payload==unchanged_payload and whole_typed_order_signature(value)==whole_typed_order_signature(wrapper_expected)
positive('payload_wrapper_new_owned_parse_complete_release')
smallfixture=D/'owned_wrapper_small_fixture.json'
with smallfixture.open('xb') as f:f.write(payload)
pin=sha(payload);value=new['strict_json'](str(smallfixture),pin)
assert whole_typed_order_signature(value)==whole_typed_order_signature(wrapper_expected)
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
'''
assert s.count(marker)==1;s=s.replace(marker,extra+'\n'+marker)
s=s.replace("encoder_and_decoder_do_not_mutate_inputs=True", "encoder_and_public_default_decoder_do_not_mutate_inputs=True,private_owned_consume_clears_parsed_rows_only=True,owned_consume_controls=owned_results,owned_consume_control_count=len(owned_results),two_real_strict_wrapper_calls_observed=wrapper_calls,isolated_stdlib_fixture_reader_adapters=fixture_reads,strict_wrapper_adapter_scope='Actual source wrapper with isolated fixture I/O adapters; original business resolver/stream/phase/API not executed',rows_lifetime_evidence='Source plus primitive observation of rows[i]=None and empty rows before content digest; no actual business RSS measurement'")
s=s.replace("both_strict_wrappers_schema_gated_after_original_parser=True", "both_strict_wrappers_schema_gated_after_original_parser=True,complete_eight_region_inverse_to_1d7=True,additional_three_region_inverse_to_frozen_abb5=True")
s=s.replace('Only isolated pure AST metadata codec/UTF8 JSON wrapper tests and the old failed graph diagnostic fixture.', 'Only isolated pure AST metadata codec/UTF8 JSON wrapper tests, strict_json source wrapper with STDlib TMP fixture reader adapters, and the old failed graph diagnostic fixture.')
s=s.replace('encode新浅storage view不改producer的原graph；decode保留完整其他data且新canonical pin dict独立。', 'encode新浅storage view和公开decode默认不改原输入；两个strict wrapper仅对自己新parse容器逐row置None，全部转移后clear，内容SHA前释放；其证据限源码和primitive，不是业务RSS测量。')
(D/'test_owned_consume_pure_storage_codec.py').write_text(s)
print('generated isolated owned-consume fixture harness; not executed')
