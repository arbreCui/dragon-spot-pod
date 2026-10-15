import hashlib,json,stat
from pathlib import Path

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
T=B/'Root_actual_Darwin_resource_SELF_rusage_environment_tool_terminal_return.json'
OUT=B/'Root_actual_Darwin_resource_SELF_rusage_diagnostic_environment_witness.json'
SEMANTICS='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK'

def pin(p):
 p=Path(p);s=p.lstat();i=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 t=p.lstat();assert [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==i
 return {'path':str(p),'sha256':h,'size_bytes':i[4],'identity':i}

def strict(data):
 def pairs(rows):
  d={}
  for k,v in rows:
   assert k not in d;d[k]=v
  return d
 def reject(v):raise ValueError(v)
 return json.loads(data,object_pairs_hook=pairs,parse_constant=reject)

assert not OUT.exists()
tp=pin(T);t=strict(T.read_text());tr=t['terminal_tool_return']
assert t['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_ENVIRONMENT_TOOL_TERMINAL_RETURN_V1'
assert t['observed_terminal'] is True and t['closed'] is True and t['session_repolled_after_close'] is False
assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
assert tr['chunk_id']=='5ae744'
d=strict(tr['output'])
assert d['schema']=='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_QUERY_V1'
assert d['platform']=='darwin' and d['source_only'] is True and d['diagnostic_dependency_verified'] is True
assert d['query_count']==1 and type(d['query_count']) is int
assert d['actual_python_fullpin']['path']=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
assert d['actual_resource_module_fullpin']['path']=='/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so'
assert d['actual_resource_module_fullpin']['sha256']=='cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164' and d['actual_resource_module_fullpin']['size_bytes']==53552
assert d['actual_resource_module_fullpin']['identity'][3]==2
assert d['actual_python_optimization']==0 and all(v=='1' for v in d['actual_thread_environment'].values()) and len(d['actual_thread_environment'])==5
assert type(d['self_ru_maxrss_native_bytes_observed']) is int and d['self_ru_maxrss_native_bytes_observed']>=0 and d['ru_maxrss_semantics']==SEMANTICS
for k in ('actual_python_fullpin','actual_resource_module_fullpin','actual_environment_producer_Source_fullpin'):
 assert pin(d[k]['path'])==d[k]
for k in ('whole_BUILD_qualified','whole_INPUT_qualified','native_or_science_qualified','candidate_guard_helper_compile_material_or_numeric_executed'):assert d[k] is False
assert pin(T)==tp
body=dict(d)
body['schema']='ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_WITNESS_V1'
body['actual_environment_tool_terminal_fullpin']=tp
body['environment_witness_META_writer_Source_fullpin']=pin(Path(__file__))
body['diagnostic_dependency_scope']='ISOLATED_ACTUAL_RESOURCE_IMPORT_AND_ONE_SELF_QUERY_ONLY_NOT_CURRENT_RSS_OR_BUSINESS_GUARD'
with OUT.open('x') as f:json.dump(body,f,ensure_ascii=False,allow_nan=False,indent=2);f.write('\n')
print(json.dumps({'witness_pin':pin(OUT),'actual_query_terminal_chunk':tr['chunk_id'],'query_count':1,'whole_BUILD_qualified':False,'whole_INPUT_qualified':False,'native_or_science_qualified':False,'cleanup_performed':False}))
