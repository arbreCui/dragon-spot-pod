"""Isolated tiny filesystem and pure codec cases; no business input/constructor."""
from pathlib import Path
import ast,base64,copy,hashlib,json,os,sys,tempfile
BASE=Path('/private/tmp/axmat-requirements-varint-wire-compact-phase-source-draft-20261009')
PARENT=Path('/Users/wen/spot/validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_owned_phase_owner_lifetimes_20261009.py')
CANDIDATE=BASE/'combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py'
def selected(path):
 tree=ast.parse(path.read_bytes());permitted=(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign)
 space={'__name__':'isolated_tiny_'+path.stem}
 exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,permitted)],type_ignores=[]),str(path),'exec'),space)
 return space
OLD,NEW=selected(PARENT),selected(CANDIDATE)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
clone=lambda x:copy.deepcopy(x)
results=[]
active=None;opens={};owned=set()
def audit(event,args):
 if active is not None and event=='open' and type(args[0])is str and args[0]in owned:
  record=opens.setdefault(active,{});record[args[0]]=record.get(args[0],0)+1
sys.addaudithook(audit)
def case(name,**facts):results.append(dict(case=name,PASS=True,**facts))
def error(module,fn):
 try:fn()
 except module['InputGraphError'] as exc:return str(exc)
 raise AssertionError('negative accepted')
def refreeze(module,value):value['content_sha256']=module['_content_digest'](value);return value

with tempfile.TemporaryDirectory(prefix='axmat-wire-compact-tiny-',dir='/private/tmp')as tmp:
 root=Path(tmp);regular=root/'regular';regular.mkdir();(regular/'empty').mkdir()
 a=regular/'α_燃料.dat';a.write_bytes(b'alpha\x00\xff')
 b=regular/'b.dat';b.write_bytes(b'beta\x01')
 parent=regular/'parent.json';parent.write_bytes(b'{"signed":-0.0,"v":[1,true,"same"]}')
 extra=root/'new.dat';extra.write_bytes(b'explicit-new')
 link=regular/'link.dat';link.symlink_to(a.name)
 da=root/'directory_alias';da.symlink_to(regular.name,target_is_directory=True)
 filemap={str(p):sha(p)for p in (a,b,parent)}
 aliases=OLD['capture_aliases']([str(link),str(da)]);amap=OLD['_alias_map'](aliases)
 amap[str(link)]['sha256']=sha(a);aliases=list(amap.values())
 owners=[dict(owner='owner-'+c,category=c,expected_files=dict(filemap))for c in OLD['CLOSURE_CATEGORIES']]
 owners += [dict(owner='duplicate-owner',category='code_environment',expected_files={str(a):sha(a)}),
            dict(owner='duplicate-owner',category='code_environment',expected_files={str(a):sha(a)}),
            dict(owner='alias-owner',category='code_environment',expected_files={str(link):sha(a)}),
            dict(owner='new-role',category='source_namespace',expected_files={},newly_declared_input_paths=[str(extra)]),
            dict(owner='empty-absent-newlist',category='source_namespace',expected_files={})]
 new={str(extra):dict(owner='explicit-new',category='source_namespace',reason='tiny explicit new')}
 ns=OLD['explicit_sealed_namespace'](str(regular),{p.name:sha(p)for p in (a,b,parent)},
      {'link.dat':dict(text=a.name,target=str(a),kind='file',sha256=sha(a))},owner='ns-one',category='source_namespace',directories=['empty'],aliases=aliases)
 ns2=clone(ns);ns2['owner']='ns-two'
 ns3=clone(ns);ns3['root']=str(da);ns3['owner']='ns-alias'
 namespaces=[ns,ns2,ns3]
 own=OLD['_owners'](owners);new_inputs=OLD['_new_inputs'](new)
 json_input=dict(path=str(parent),sha256=sha(parent));owned={str(p)for p in (a,b,parent,extra)}
 def phase(module,label,compact=False,owner_values=None,ns_values=None):
  global active
  active=label
  try:
   ov=own if owner_values is None else module['_owners'](owner_values)
   kw=dict(json_input=json_input)
   if compact:
    ov=module['_owned_phase_owner_stream'](ov);kw.update(release_owned_owners=True,compact_requirements=True)
   return module['_phase'](ov,namespaces if ns_values is None else ns_values,amap,new_inputs,**kw)
  finally:active=None
 old=phase(OLD,'phase-old');default=phase(NEW,'phase-default');compact=phase(NEW,'phase-compact',True)
 expanded=list(NEW['_compact_requirement_dicts'](compact[0]))
 assert old==default and old==(expanded,*compact[1:])
 assert OLD['_canonical_json'](old)==NEW['_canonical_json'](default)==NEW['_canonical_json']((expanded,*compact[1:]))
 assert all(type(r)is dict for r in default[0])and all(type(r)is tuple for r in compact[0])
 assert opens['phase-old']==opens['phase-default']==opens['phase-compact']=={p:1 for p in owned}
 before=OLD['_canonical_json'](owners);assert before==NEW['_canonical_json'](owners)
 case('ordinary-direct-phase-byteexact-and-private-full-tuples',logical_rows=len(old[0]),canonical_files=len(owned),parent_JSON_and_signed_zero_preserved=True,caller_containers_unchanged=True,full_fresh_read_once_each=True)
 assert NEW['_wire_requirement_table_compact'](compact[0])['rows']['row_count']==len(old[0])
 old_table=OLD['_requirement_table'](old[0]);wire_table=NEW['_wire_requirement_table_compact'](compact[0])
 limits=(len(old_table['paths']),len(old_table['paths']),len(old_table['owners']),9,4)
 assert [list(r)for r in NEW['_decoded_requirement_rows'](wire_table['rows'],limits)]==old_table['rows']
 case('complete-five-columns-order-duplicate-owner-roles-table-inverse',all_rows_and_symbols_retained=True,duplicate_edges_retained=True)
 with NEW['ReadOpenAudit']()as read_audit:
  a.read_bytes()
 trace=read_audit.snapshot()
 args=dict(typed_snapshot={'Unicode':'α燃料𐐀','signed':-0.0,'list':[True,None,1,1.25]},owners=owners,
    namespaces=namespaces,aliases=aliases,read_trace=trace,newly_declared_input_paths=new,
    absence_inputs={str(root/'missing.dat'):dict(owner='optional',category='code_environment',reason='known tiny optional')})
 old_graph=OLD['create_graph'](**args);new_graph=NEW['create_graph'](**args)
 assert old_graph==new_graph and OLD['_canonical_json'](old_graph)==NEW['_canonical_json'](new_graph)
 assert json.dumps(old_graph,allow_nan=False,separators=(',',':')).encode()==json.dumps(new_graph,allow_nan=False,separators=(',',':')).encode()
 case('ordinary-create-graph-original-full-json-bytes-unchanged',all_mutable_graph_containers_independent=True)
 wire=NEW['encode_graph_wire'](old_graph);decoded=NEW['decode_graph_wire'](wire)
 assert decoded==old_graph and OLD['_canonical_json'](decoded)==OLD['_canonical_json'](old_graph)
 assert NEW['encode_graph_wire'](decoded)==wire
 assert [list(row)for row in NEW['iter_graph_requirement_rows'](wire)]==old_graph['requirements']['rows']
 assert list(NEW['iter_graph_requirement_rows'](old_graph))==old_graph['requirements']['rows']
 assert NEW['_wire_semantic_content_digest'](wire)==old_graph['content_sha256']
 assert NEW['create_wire_graph'](**args)==wire
 case('full-valid-wire-graph-exact-complete-inverse-Unicode-signedzero',wire_new_schema_explicit=True,logical_row_count=len(old_table['rows']),old_graph_source_unmodified=True)
 def verified(module,graph,label):
  global active
  active=label
  try:return module['verify_graph'](graph,phase='tiny')
  finally:active=None
 left=verified(OLD,old_graph,'verify-old');normal=verified(NEW,old_graph,'verify-new-legacy');right=verified(NEW,wire,'verify-wire')
 assert left==normal
 adjusted=dict(right,graph_content_sha256=old_graph['content_sha256']);assert left==adjusted
 assert opens['verify-old']==opens['verify-new-legacy']==opens['verify-wire']=={p:1 for p in owned}
 case('legacy-and-new-wire-verifier-complete-result-equal-except-explicit-wire-digest',all_original_fresh_byte_namespace_alias_owner_trace_gates=True)
 graphpath=root/'wire.json';graphpath.write_bytes(NEW['_canonical_json'](wire)+b'\n')
 got=NEW['verify_graph'](str(graphpath),expected_sha256=sha(graphpath),phase='tiny');assert got==right
 case('actual-tiny-wire-byte-file-SHA-strict-parser-entry',original_MAX_JSON_BYTES=NEW['MAX_JSON_BYTES'])
 badsha='0'*64
 assert 'JSON' in error(NEW,lambda:NEW['verify_graph'](str(graphpath),expected_sha256=badsha,phase='tiny'))
 case('stored-wire-actual-byte-SHA-refusal')
 def reject_pair(name,legacy):
  refreeze(OLD,legacy);encoded=NEW['encode_graph_wire'](legacy)
  le=error(OLD,lambda:OLD['verify_graph'](legacy,phase='tiny'))
  ne=error(NEW,lambda:NEW['verify_graph'](encoded,phase='tiny'))
  assert le==ne,(name,le,ne)
  case(name,original_and_wire_same_error_and_priority=True,message=le)
 mutated=clone(old_graph);mutated['owners']['rows'][0][2].append(mutated['owners']['rows'][0][2][0]);reject_pair('duplicate-owner-pin-index-refused',mutated)
 mutated=clone(old_graph);mutated['owners']['rows'][0][1]=9;reject_pair('unknown-owner-category-index-refused',mutated)
 mutated=clone(old_graph);mutated['owners']['rows'][0][2][0]=10**9;reject_pair('missing-owner-pin-index-refused',mutated)
 mutated=clone(old_graph);mutated['coverage_requirements']={'code_environment':{'minimum_files':10**9}};reject_pair('missing-required-coverage-refused',mutated)
 mutated=clone(old_graph);mutated['read_trace']['records'][0]['path']=str(root/'unknown-unowned.dat');reject_pair('unknown-trace-input-refused',mutated)
 mutated=clone(old_graph);mutated['newly_declared_input_pins'][str(extra)]='0'*64;reject_pair('changed-new-input-pin-refused',mutated)
 a.write_bytes(b'changed')
 le=error(OLD,lambda:OLD['verify_graph'](old_graph,phase='tiny'));ne=error(NEW,lambda:NEW['verify_graph'](wire,phase='tiny'));assert le==ne
 case('fresh-later-phase-changed-bytes-refused',same_error=True);a.write_bytes(b'alpha\x00\xff')
 unknown=regular/'unknown.dat';unknown.write_bytes(b'unknown')
 bad_owners=owners+[dict(owner='unknown-new-role',category='source_namespace',expected_files={},newly_declared_input_paths=[str(root/'undeclared-new')])]
 le=error(OLD,lambda:phase(OLD,'priority-old',owner_values=bad_owners));ne=error(NEW,lambda:phase(NEW,'priority-new',True,owner_values=bad_owners));assert le==ne and 'namespace' in le
 case('namespace-unknown-member-before-later-owner-role-error',same_error_priority=True)
 unknown.unlink()
 le=error(OLD,lambda:phase(OLD,'later-role-old',owner_values=bad_owners));ne=error(NEW,lambda:phase(NEW,'later-role-new',True,owner_values=bad_owners));assert le==ne and 'explicit reason/role' in le
 case('missing-explicit-owner-new-role-refused-after-namespace-restored',same_error_priority=True)
 verified(NEW,wire,'verify-restored');assert opens['verify-restored']=={p:1 for p in owned};case('restored-later-phase-again-full-fresh-read-once-no-cache')
 # Strict saved symbol-table gates keep original order before owners or bytes.
 for name,mutator in [('duplicate-path-symbol',lambda t:t['paths'].append(t['paths'][-1])),('duplicate-owner-symbol',lambda t:t['owners'].append(t['owners'][-1])),('unknown-table-field',lambda t:t.update(unknown=True)),('missing-table-field',lambda t:t.pop('owners')),('changed-column-layout',lambda t:t['columns'].reverse()),('unknown-binding-role-symbol',lambda t:t['binding_roles'].append('UNKNOWN'))]:
  bad=clone(wire);mutator(bad['requirements']);refreeze(NEW,bad)
  msg=error(NEW,lambda:NEW['verify_graph'](bad,phase='tiny'));case('wire-'+name,message=msg)
 for name,mutator in [('missing-wire-metadata-field',lambda x:x['wire_encoding'].pop('source_graph_schema')),('unknown-wire-metadata-field',lambda x:x['wire_encoding'].update(unknown=True)),('changed-semantic-digest',lambda x:x['wire_encoding'].update(decoded_content_sha256='0'*64))]:
  bad=clone(wire);mutator(bad);refreeze(NEW,bad);msg=error(NEW,lambda:NEW['verify_graph'](bad,phase='tiny'));case(name,message=msg)

limits=(512,512,512,9,4)
rows=[[0,127,128,0,0],[511,256,1,8,3],[511,256,1,8,3],[128,255,299,7,2]]
codec=NEW['_encode_requirement_rows'](rows,len(rows))
assert [list(r)for r in NEW['_decoded_requirement_rows'](codec,limits)]==rows
case('varint-boundaries-0-127-128-255-256-511-and-duplicate-row-inverse')
def codec_bad(name,mutator):
 bad=clone(codec);mutator(bad)
 message=error(NEW,lambda:list(NEW['_decoded_requirement_rows'](bad,limits)))
 case('codec-'+name,message=message)
for name,mutator in [('unknown-field',lambda x:x.update(extra=True)),('missing-field',lambda x:x.pop('data')),('unknown-schema',lambda x:x.update(schema='UNKNOWN')),('unknown-encoding',lambda x:x.update(encoding='OTHER')),('wrong-column-count',lambda x:x.update(column_count=6)),('bool-column-count',lambda x:x.update(column_count=True)),('bool-row-count',lambda x:x.update(row_count=True)),('negative-row-count',lambda x:x.update(row_count=-1)),('missing-row-count',lambda x:x.pop('row_count')),('too-few-row-count',lambda x:x.update(row_count=3)),('too-many-row-count',lambda x:x.update(row_count=5)),('padding-removed',lambda x:x.update(data=x['data'].rstrip('='))),('extra-padding',lambda x:x.update(data=x['data']+'=')),('non-ASCII-symbol',lambda x:x.update(data='燃AAA')),('invalid-alphabet-symbol',lambda x:x.update(data='!!!!')),('whitespace-symbol',lambda x:x.update(data='    ')),('truncated-row',lambda x:x.update(data=base64.b64encode(b'\x00').decode())),('truncated-continuation',lambda x:x.update(row_count=1,data=base64.b64encode(b'\x00\x00\x00\x00\x80').decode())),('overlong-varint',lambda x:x.update(row_count=1,data=base64.b64encode(b'\x80\x00\x00\x00\x00\x00').decode())),('overflow-index',lambda x:x.update(row_count=1,data=base64.b64encode(b'\xff'*20+b'\x00'*5).decode())),('out-of-range-role',lambda x:x.update(row_count=1,data=base64.b64encode(b'\x00\x00\x00\x00\x04').decode())),('extra-row-bytes',lambda x:x.update(row_count=1,data=base64.b64encode(b'\x00'*10).decode()))]:codec_bad(name,mutator)
zero=NEW['_encode_requirement_rows']([[0,0,0,0,0]],1)
bad=clone(zero);bad['data']=bad['data'][:-2]+'B=';assert base64.b64decode(bad['data'])==base64.b64decode(zero['data'])
msg=error(NEW,lambda:list(NEW['_decoded_requirement_rows'](bad,limits)));case('codec-nonzero-base64-pad-bits-rejected',message=msg)
assert list(NEW['_decoded_requirement_rows'](NEW['_encode_requirement_rows']([],0),(0,0,0,9,4)))==[];case('codec-empty-table-exact-inverse')
for rows_bad in ([[False,0,0,0,0]],[[-1,0,0,0,0]],[[0,0,0,0]],[[0.0,0,0,0,0]]):
 msg=error(NEW,lambda:NEW['_encode_requirement_rows'](rows_bad,1));case('codec-encode-invalid-integer-or-width-'+str(len(results)),message=msg)
# A bounded synthetic table measures only representation/container sizes. No
# production graph, owner union, factory import or actual RSS is sampled.
synthetic=[[i%40000,(i*3)%40000,i%4000,i%9,i%4]for i in range(4096)]
packed=NEW['_encode_requirement_rows'](synthetic,len(synthetic))
assert [list(r)for r in NEW['_decoded_requirement_rows'](packed,(40000,40000,4000,9,4))]==synthetic
old_rows_bytes=len(json.dumps(synthetic,separators=(',',':')).encode())
new_rows_bytes=len(json.dumps(packed,separators=(',',':')).encode())
assert new_rows_bytes<old_rows_bytes
dictionary=dict(zip(NEW['REQUIREMENT_COLUMNS'],('p','p','o','c','r')));tuple_row=tuple(dictionary.values())
measure=dict(synthetic_rows=4096,old_rows_JSON_bytes=old_rows_bytes,new_rows_codec_JSON_bytes=new_rows_bytes,
 reduction_bytes=old_rows_bytes-new_rows_bytes,dict_shallow_bytes=sys.getsizeof(dictionary),tuple_shallow_bytes=sys.getsizeof(tuple_row),
 production_row_count_from_prior_evidence_not_remeasured=235528,container_only_projected_saving_bytes=235528*(sys.getsizeof(dictionary)-sys.getsizeof(tuple_row)),not_actual_RSS_or_actual_production_graph_size=True)
case('bounded-synthetic-4096-row-wire-size-and-container-estimate',**measure)
assert all(r['PASS']for r in results)
report=dict(schema='AXMAT_REQUIREMENTS_VARINT_WIRE_COMPACT_PHASE_TINY_DIFFERENTIAL_V1',status='PASS_ISOLATED_TINY_ONLY',
 parent_source=dict(path=str(PARENT),sha256=sha(PARENT)),candidate_source=dict(path=str(CANDIDATE),sha256=sha(CANDIDATE)),
 case_count=len(results),results=results,representation_measurement=measure,
 real_business_union_or_producer_import_or_constructor_or_PREP_RUN=False,ART_or_formal_source_written=False,
 actual_512_native_RSS_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False)
path=BASE/'tiny_differential_report.json';assert not path.exists();path.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(report=str(path),sha256=sha(path),case_count=len(results),status=report['status'],representation_measurement=measure)))
