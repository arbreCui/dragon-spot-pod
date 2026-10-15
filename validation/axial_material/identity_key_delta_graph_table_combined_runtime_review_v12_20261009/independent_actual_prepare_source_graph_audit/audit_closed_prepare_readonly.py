"""Run only after Root provides its genuine closed PREP witness; no business imports."""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import stat

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
SOURCE=ART/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009'
OUT=ART/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
FACTORY=ROOT/'validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_combined_runtime_v12.py'
HELPER=ROOT/'validation/axial_material/combined_runtime_complete_input_graph_canonical_file_table_storage_20261009.py'
FACTORY_SHA='5af1feebc7d40549750e1daec6148ae073a4c85c1eb3242485e6d9e80826861b'
HELPER_SHA='e8f142bef9dede08e9e43eba995203dea17e0e48b6f383502ed18b89808a5c28'
SPECS=ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
SPECS_SHA='2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
PREFIX='AXMAT_OWNED_SPECS_IDENTITY_KEY_DELTA_GRAPH_TABLE_COMBINED_RUNTIME_V12'
GRAPH_SCHEMA='AXMAT_COMBINED_RUNTIME_VERIFIED_INPUT_GRAPH_REQUIREMENTS_VARINT_WIRE_V1'
STORAGE_SCHEMA='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1'
INPUT_SCOPE='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION'
CAP=67108864
COLS=['path','sha256','size_bytes']
FULL_SOURCE_NAMES={'historical_input_combined_runtime_factory.py','input_specs.json','source_admission.json','trim_component_admission_INPUT.json','trim_component_API_python_open_trace.json','trim_component_API_absence_INPUT.json','runtime/graph.py','runtime/codec.py','runtime/current.py','runtime/checks.py','runtime/ordinary.py'}

def sig(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink)
def valid_sha(v):return type(v)is str and len(v)==64 and all(c in '0123456789abcdef'for c in v)
def normal(p):
 p=Path(p)
 assert p.is_absolute() and '..' not in p.parts
 for q in [*reversed(p.parents),p]:assert not q.is_symlink(),str(q)
 return p
def fresh(p,expected=None,collect=False,max_bytes=None):
 p=normal(p);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);parts=[] if collect else None;h=hashlib.sha256();n=0
 try:
  before=os.fstat(fd);assert stat.S_ISREG(before.st_mode)
  if max_bytes is not None:assert before.st_size<=max_bytes
  while True:
   b=os.read(fd,1048576)
   if not b:break
   n+=len(b)
   if max_bytes is not None:assert n<=max_bytes
   h.update(b)
   if collect:parts.append(b)
  after=os.fstat(fd);assert sig(before)==sig(after)==sig(p.stat()) and n==before.st_size
 finally:os.close(fd)
 digest=h.hexdigest()
 if expected is not None:assert valid_sha(expected) and digest==expected,str(p)
 return dict(path=str(p),sha256=digest,bytes=n,seven_identity=list(sig(after))),b''.join(parts)if collect else None
def bad_constant(v):raise ValueError('nonfinite JSON '+v)
def finite_float(v):
 v=float(v);assert math.isfinite(v);return v
def strict(p,expected=None,max_bytes=CAP):
 pin,raw=fresh(p,expected,True,max_bytes);text=raw.decode('utf-8');del raw
 strings={};integers={}
 def intern_values(v):
  if type(v)is str:return strings.setdefault(v,v)
  if type(v)is list:
   for i,x in enumerate(v):v[i]=intern_values(x)
  return v
 def pairs(items):
  value={}
  for k,v in items:
   assert k not in value,'duplicate JSON key'
   value[k]=v
  return {strings.setdefault(k,k):intern_values(value[k])for k in sorted(value)}
 def integer(s):
  v=int(s);return integers.setdefault(v,v)
 try:value=json.loads(text,object_pairs_hook=pairs,parse_int=integer,parse_float=finite_float,parse_constant=bad_constant)
 finally:strings.clear();integers.clear()
 del text
 return value,pin
def content_digest(value):
 data=dict(value);data.pop('content_sha256',None);h=hashlib.sha256()
 for part in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(data):h.update(part.encode('utf-8'))
 return h.hexdigest()
def restore(storage):
 assert type(storage)is dict and set(storage)=={'schema','graph'} and storage['schema']==STORAGE_SCHEMA
 graph=storage['graph'];assert type(graph)is dict and graph['schema']==GRAPH_SCHEMA and graph['scope']==INPUT_SCOPE and graph['consumer_scope']is None
 table=graph['canonical_files'];assert type(table)is dict and set(table)=={'columns','rows'} and table['columns']==COLS and type(table['columns'])is list and type(table['rows'])is list
 rows=table['rows'];pins=[]
 for i,row in enumerate(rows):
  assert type(row)is list and len(row)==3 and type(row[0])is str and type(row[1])is str and valid_sha(row[1]) and type(row[2])is int and row[2]>=0
  assert os.path.isabs(row[0]) and os.path.normpath(row[0])==row[0] and '\0'not in row[0]
  pins.append(dict(zip(COLS,row)));rows[i]=None
 rows.clear();del rows
 if pins:del row
 restored=dict(graph);restored['canonical_files']=pins
 assert valid_sha(restored['content_sha256'])and content_digest(restored)==restored['content_sha256']
 return restored
def requirements(graph):
 t=graph['requirements'];assert t['schema']=='AXMAT_COMBINED_RUNTIME_COMPLETE_TYPED_REQUIREMENT_TABLE_VARINT_WIRE_V1' and t['columns']==['path','canonical_path','owner','category','binding_role'] and t['scope']==INPUT_SCOPE and t['duplicate_edges_retained']is True
 paths=t['paths'];assert paths==sorted(set(paths)) and t['owners']==sorted(set(t['owners']))
 c=t['rows'];assert set(c)=={'schema','encoding','row_count','column_count','data'} and c['schema']=='AXMAT_COMPLETE_FIVE_COLUMN_REQUIREMENT_ROWS_V1' and c['encoding']=='CANONICAL_UNSIGNED_LEB128_BASE64' and type(c['column_count'])is int and c['column_count']==5 and type(c['row_count'])is int and c['row_count']>=0
 data=base64.b64decode(c['data'].encode('ascii'),validate=True);assert base64.b64encode(data).decode('ascii')==c['data'];limits=[len(paths),len(paths),len(t['owners']),len(t['categories']),len(t['binding_roles'])];position=0;literal={};canon=set()
 for _ in range(c['row_count']):
  row=[]
  for limit in limits:
   value=0;shift=0;groups=0
   while True:
    assert position<len(data);b=data[position];position+=1;groups+=1;value|=(b&127)<<shift;assert value<limit
    if b<128:
     assert groups==1 or b!=0;break
    shift+=7;assert shift<max(1,limit.bit_length())
   row.append(value)
  p,q=paths[row[0]],paths[row[1]]
  assert p not in literal or literal[p]==q;literal[p]=q;canon.add(q)
 assert position==len(data)
 return t,dict(literal),canon,c['row_count']
def expected_union(graph,t,literal):
 result={}
 def add(p,h):
  assert valid_sha(h) and p in literal;q=literal[p]
  assert q not in result or result[q]==h;result[q]=h
 o=graph['owners'];assert o['duplicate_descriptors_retained']is True and o['expected_hashes_come_from_typed_owners_not_observed_files']is True
 for p,h in o['expected_file_pins']:
  assert type(p)is int and type(h)is int and 0<=p<len(t['paths']) and 0<=h<len(o['expected_sha256s']);add(t['paths'][p],o['expected_sha256s'][h])
 for ns in graph['namespaces']:
  for rel,h in ns['files'].items():add(os.path.join(ns['root'],rel),h)
  for rel,link in ns['symlinks'].items():
   if link['kind']=='file'and 'sha256'in link:add(os.path.join(ns['root'],rel),link['sha256'])
 return result
def inventory(root,expected):
 files={};dirs=[];links={}
 for current,folders,names in os.walk(normal(root),followlinks=False):
  rel=Path(current).relative_to(root)
  if rel.parts:dirs.append(str(rel))
  for name in folders+names:
   p=Path(current)/name
   if p.is_symlink():links[str(p.relative_to(root))]=os.readlink(p)
  for name in names:
   p=Path(current)/name
   if not p.is_symlink():files[str(p.relative_to(root))]=fresh(p)[0]['sha256']
 actual=dict(files=files,symlinks=links,directories=sorted(dirs));assert actual==expected
 return actual
def main():
 a=argparse.ArgumentParser();a.add_argument('--closed-root-prepare-receipt',required=True);a.add_argument('--receipt-sha256',required=True);a.add_argument('--report',required=True);args=a.parse_args()
 report_path=Path(args.report);assert report_path.is_absolute()and str(report_path).startswith('/private/tmp/')and not report_path.exists()
 root,rootpin=strict(args.closed_root_prepare_receipt,args.receipt_sha256)
 assert root['record_producer']=='root'and root['actual_tool_terminal_return_observed']is True and root['record_written_after_actual_terminal_return']is True and type(root['returncode'])is int and root['returncode']==0 and type(root['actual_tool_result']['exit_code'])is int and root['actual_tool_result']['exit_code']==0
 terminal,terminalpin=strict(root['terminal_evidence']['path'],root['terminal_evidence']['sha256'])
 assert terminal['schema']==PREFIX+'_ACTUAL_EXTERNAL_PREP_RETURN_V1'and terminal['successful_declaration_input_observed']is True and terminal['record_producer']=='root'and terminal['actual_tool_terminal_return_observed']is True and terminal['record_written_after_actual_terminal_return']is True and type(terminal['returncode'])is int and terminal['returncode']==0
 assert type(terminal['actual_tool_result']['exit_code'])is int and terminal['actual_tool_result']['exit_code']==0
 declaration,declpin=strict(root['declaration']['path'],root['declaration']['sha256']);assert root['declaration']['path']==str(OUT/'declaration.json')and terminal['declaration']==root['declaration']
 d=declaration;assert d['schema']==PREFIX+'_DECLARATION_V1'and d['stages']==['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
 assert (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['threads'],d['numeric_children_at_once'],d['retries'])==(1800,600,512,1,1,0)
 assert (d['archive_reserve_bytes'],d['artifact_budget_bytes'],d['min_free_bytes'])==(2*2**30,96*2**30,8*2**30)
 assert root['input_graph']==terminal['input_graph']==d['input_graph']and root['source']==terminal['source']==dict(path=str(FACTORY),sha256=FACTORY_SHA)
 for key in ('successful_new_runtime_build_observed','original_component_APIs_executed_now','native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'):assert terminal[key]is False
 factorypin,_=fresh(FACTORY,FACTORY_SHA);helperpin,_=fresh(HELPER,HELPER_SHA)
 snapshot,sp=strict(terminal['source_inventory']['path'],terminal['source_inventory']['sha256']);assert snapshot==d['source_inventory']and set(snapshot['files'])==FULL_SOURCE_NAMES and snapshot['symlinks']=={}
 actual_source=inventory(SOURCE,snapshot)
 assert actual_source['files']['historical_input_combined_runtime_factory.py']==FACTORY_SHA and actual_source['files']['runtime/graph.py']==HELPER_SHA and actual_source['files']['input_specs.json']==SPECS_SHA
 fresh(SPECS,SPECS_SHA)
 source_admission,_=strict(SOURCE/'source_admission.json',actual_source['files']['source_admission.json']);assert source_admission['schema']==PREFIX+'_SOURCE_ADMISSION_V1'
 assert source_admission['historical_whole_component_body']==d['historical_whole_component_body']==terminal['historical_whole_component_body']and d['historical_whole_component_body']['sha256']==SPECS_SHA and d['historical_whole_component_body']['whole_seven_key_body_retained']is True
 trim,_=strict(SOURCE/'trim_component_admission_INPUT.json',actual_source['files']['trim_component_admission_INPUT.json'])
 admitted,_=strict(ROOT/'validation/axial_material/identity_key_delta_full_component_review_v11_20261009/admit.stdout');assert trim==admitted
 assert trim['compiled_kernel_source']['sha256']=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'and trim['cache_unit_control_counts']['total_declared_stages']==68
 for key in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed','production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted'):assert trim[key]is False
 graphpin=d['input_graph'];assert graphpin['path']==str(OUT/'input_graph.json')and graphpin['scope']=='COMPLETE_HISTORICAL_INPUT_ONLY'
 storage,gp=strict(graphpin['path'],graphpin['sha256']);assert gp['bytes']<CAP
 graph=restore(storage);del storage;assert graph['content_sha256']==graphpin['content_sha256']
 table,literal,canonical,edges=requirements(graph);expected=expected_union(graph,table,literal)
 pins=graph['canonical_files'];paths=[r['path']for r in pins];assert paths==sorted(set(paths))and set(paths)==canonical
 observed={r['path']:r['sha256']for r in pins};assert observed==expected==d['files']and graphpin['path']not in observed
 assert observed[str(FACTORY)]==FACTORY_SHA and observed[str(HELPER)]==HELPER_SHA and observed[str(SOURCE/'runtime/graph.py')]==HELPER_SHA
 aliases={r['path']:{k:v for k,v in r.items()if k!='path'}for r in graph['aliases']};assert len(aliases)==len(graph['aliases'])and aliases==d['complete_input_aliases']
 assert graph['live_resource_roots']==sorted(d['resource_roots'])and graph['typed_snapshot']['historical_whole_component_body']==d['historical_whole_component_body']and graph['typed_snapshot']['actual_last_cprime_trim_component_INPUT']==d['actual_last_cprime_trim_component_INPUT']
 for key in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified'):assert graph[key]is False
 stdout,_=strict(terminal['full_stdout']['path'],terminal['full_stdout']['sha256']);assert stdout==dict(declaration=str(OUT/'declaration.json'),declaration_sha256=declpin['sha256']);stderrpin,_=fresh(terminal['full_stderr']['path'],terminal['full_stderr']['sha256']);assert stderrpin['bytes']==0
 result=dict(schema='AXMAT_V12_ACTUAL_CLOSED_PREPARE_SOURCE_GRAPH_INDEPENDENT_AUDIT_V1',status='PASS_ACTUAL_SOURCE_COPY_AND_COMPLETE_GRAPH_METADATA_ONLY',actual_root_PREP=rootpin,actual_external_PREP=terminalpin,declaration=declpin,source_inventory=sp,source_file_count=len(actual_source['files']),source_exact_inventory=actual_source,actual_factory=factorypin,actual_helper=helperpin,actual_stored_graph=gp,original_read_bound_bytes=CAP,actual_headroom_bytes=CAP-gp['bytes'],fresh_computed_decoded_content_sha256=graph['content_sha256'],actual_canonical_row_count=len(pins),actual_logical_edge_count=edges,actual_alias_count=len(aliases),actual_namespace_count=len(graph['namespaces']),actual_descriptor_count=len(expected),all_declared_EXPECTED_union_and_canonical_pins_equal=True,all_original_seven_BODY_bytes_retained=True,actual_full68_component_API_INPUT_equal_to_genuine_admitted_return=True,both_strict_reader_identity_and_original_methods_bound_by_reviewed_e8_source=True,all_caps_unchanged=True,all_SOURCE_files_freshly_hashed=True,all_historical_canonical_files_rehashed_by_this_audit=False,business_imports_or_calls=False,project_files_written=False,new_runtime_build_success_claimed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
 report_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(report=str(report_path),sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),status=result['status'],graph_bytes=gp['bytes'],canonical_rows=len(pins),logical_edges=edges)))
if __name__=='__main__':main()
