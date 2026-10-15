"""Pure saved metadata size diagnostic. No component API, fresh input admission or numeric solve."""
import hashlib,json,os,stat,sys
from pathlib import Path
OLD=Path('/Users/wen/spot/validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009/input_graph.json')
NEW=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-table-combined-runtime-v15-20261010/input_creation_python_open_trace.json')
def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 before=identity(p)
 if not stat.S_ISREG(before[2]):raise ValueError('regular metadata required')
 with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
 if identity(p)!=before:raise ValueError('metadata identity changed')
 return dict(path=str(p),sha256=h,identity=before)
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def no_constant(s):raise ValueError('nonfinite JSON')
def measure(value):
 n=0;h=hashlib.sha256();e=json.JSONEncoder(separators=(',',':'),allow_nan=False)
 for s in e.iterencode(value):
  raw=s.encode('utf-8');n+=len(raw);h.update(raw)
 return dict(bytes=n,sha256=h.hexdigest())
def main():
 if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:raise ValueError('normal fixed diagnostic required')
 inputs=[pin(OLD),pin(NEW)]
 with OLD.open() as f:old=json.load(f,object_pairs_hook=unique,parse_constant=no_constant)
 if old['schema']!='AXMAT_COMPLETE_INPUT_GRAPH_CANONICAL_FILE_TABLE_STORAGE_V1':raise ValueError('exact old saved storage schema required')
 graph=old['graph'];old_trace=graph['read_trace'];old_measure=measure(old);old_trace_measure=measure(old_trace)
 if old_measure['bytes']+1!=inputs[0]['identity'][4]:raise ValueError('exact old compact file length differs')
 with NEW.open() as f:new=json.load(f,object_pairs_hook=unique,parse_constant=no_constant)
 if set(new)!=set(old_trace) or new['schema']!=old_trace['schema'] or new['coverage']!=old_trace['coverage']:raise ValueError('complete original trace shape required')
 if any(type(new[k]) is not list for k in ['records','subprocess_records']):raise ValueError('complete trace lists required')
 new_measure=measure(new)
 for expected,p in zip(inputs,[OLD,NEW]):
  if pin(p)!=expected:raise ValueError('saved metadata changed')
 print(json.dumps(dict(status='ACTUAL_SAVED_METADATA_SIZE_ONLY',inputs=inputs,old_complete_storage=old_measure,old_complete_trace=old_trace_measure,new_complete_creation_trace=new_measure,old_trace_records=len(old_trace['records']),new_trace_records=len(new['records']),old_subprocess_records=len(old_trace['subprocess_records']),new_subprocess_records=len(new['subprocess_records']),trace_only_replacement_size_model_bytes=old_measure['bytes']-old_trace_measure['bytes']+new_measure['bytes']+1,original_max_json_bytes=64*2**20,model_scope='Only replace old read_trace in old saved graph. This is not an actual V15 graph forecast or proof; all other V15 owners/namespaces/edges and metadata may differ.',component_API_executed=False,new_graph_created=False,fresh_input_bytes_qualified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False),allow_nan=False),flush=True)
if __name__=='__main__':main()
