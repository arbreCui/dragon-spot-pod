"""UNREADY independent complete fresh-verifier controls SOURCE template.

No helper, guard, source namespace, graph or business API is loaded at import.
Root must bind a peer-qualified installed new helper and source-review a genuine
619/705/38de host before this template can become READY. Current bindings are
None. The old 60-second pure controls are separate and are never expanded here.
Future execution is metadata verification only, not component/native/science.
"""
from __future__ import annotations
import argparse
import copy
import gc
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import stat
import struct
import sys
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'
ACTUAL_SUCCESS_PINS = None
NEW_HELPER_PATH = None
NEW_HELPER_SHA256 = None
NEW_HELPER_SOURCE_BYTES = None
NEW_HELPER_IDENTITY = None
UNKNOWN_Q = None
UNKNOWN_BUSINESS_PINS = None
OUTPUT_PATH = None
OLD_HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'
OLD_HELPER_SHA256 = 'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'
OLD_HELPER_SOURCE_BYTES = 145715
GRAPH_PIN = {
 'path': '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010/input_graph.json',
 'sha256': 'dfaaaff743d8edf4c94b262c5ee8104f606eddecaf39260010167f0884c6d976',
 'identity': [16777229,49377441,33188,1,45530035,1791587709451819342,1791587709451819342]}
PHASE = 'helper_complete_fresh_verifier_control'
STAGE_SECONDS, WHOLE_HOST_SECONDS, RSS_MIB = 600, 1800, 512
JOINT_HOST_SOURCE_OUT_ARCHIVE_BYTES = 64*2**20
HISTORY_BYTES, MIN_FREE_BYTES = 96*2**30, 8*2**30
THREADS, CHILDREN, RETRIES = 1, 1, 0
MAX_JSON_BYTES = 64*2**20
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
ENCODER = json.JSONEncoder(ensure_ascii=True,sort_keys=False,separators=(',',':'),allow_nan=False)

def require(condition, message):
 if type(condition) is not bool or not condition:raise AssertionError(message)

def sha_text(value):
 return type(value) is str and len(value)==64 and all(c in '0123456789abcdef' for c in value)

def identity(path):
 s=Path(path).lstat()
 require(stat.S_ISREG(s.st_mode) and s.st_nlink==1,'normal single-link regular source/metadata input required')
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def full_pin(path, expected_sha256=None, expected_identity=None):
 path=Path(path);before=identity(path);h=hashlib.sha256();count=0
 with path.open('rb') as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   h.update(block);count+=len(block)
 after=identity(path)
 require(before==after and count==before[4],'full EOF/7identity source or graph changed')
 digest=h.hexdigest()
 if expected_sha256 is not None:require(digest==expected_sha256,'fixed source/graph SHA changed')
 if expected_identity is not None:require(before==expected_identity,'fixed source/graph 7identity changed')
 return dict(path=str(path),sha256=digest,identity=before,size_bytes=count)

def load_pinned(path, sha256, source_bytes, name):
 before=full_pin(path,sha256)
 require(before['size_bytes']==source_bytes,'exact source byte count required')
 spec=importlib.util.spec_from_file_location(name,path)
 require(spec is not None and spec.loader is not None,'normal installed helper loader required')
 module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
 require(Path(module.__file__).resolve()==Path(path).resolve(),'actual helper source path required')
 require(full_pin(path,sha256)==before,'helper source changed during import')
 return module,before

def value_snapshot(value):
 """Complete builtin types/order/value/float bits; mutable ids separately."""
 mutable=[]
 def visit(part):
  kind=type(part)
  if kind in (dict,list):mutable.append(id(part))
  if kind is dict:return ('dict',tuple((visit(k),visit(v)) for k,v in part.items()))
  if kind in (list,tuple):return (kind.__name__,tuple(visit(v) for v in part))
  if kind is float:return ('float',struct.pack('>d',part).hex())
  require(kind in (str,int,bool,type(None)),'builtin JSON/tuple fixture value required')
  return (kind.__name__,part)
 return visit(value),tuple(mutable)

def exact_value(left,right,where='root'):
 require(type(left) is type(right),'complete return type changed at '+where)
 if type(left) is dict:
  require(len(left)==len(right),'complete return field count changed at '+where)
  # Return mapping key insertion order is the original public API contract.
  for (lk,lv),(rk,rv) in zip(left.items(),right.items()):
   require(type(lk) is str and lk==rk,'complete return key order changed at '+where)
   exact_value(lv,rv,where+'/'+lk)
 elif type(left) is list:
  require(len(left)==len(right),'complete return list count changed at '+where)
  for i,(lv,rv) in enumerate(zip(left,right)):exact_value(lv,rv,where+'/'+str(i))
 elif type(left) is float:require(struct.pack('>d',left)==struct.pack('>d',right),'floatbits changed at '+where)
 else:require(type(left) in (str,int,bool,type(None)) and left==right,'complete return scalar changed at '+where)

def checkpoint(started,output):
 require(time.monotonic()-started<STAGE_SECONDS,'original 600-second fresh-control stage exceeded')
 rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 rss=int(rss if sys.platform=='darwin' else rss*1024)
 require(0<=rss<RSS_MIB*2**20,'original 512MiB fresh-control RSS exceeded')
 # The genuine future host separately counts HOST+SOURCE+OUT, before/after/final.
 sizes=sum(p.stat().st_size for p in output.iterdir() if p.is_file())
 require(sizes<JOINT_HOST_SOURCE_OUT_ARCHIVE_BYTES,'OUT alone exceeds joint64MiB cap')
 return dict(elapsed_seconds=time.monotonic()-started,own_peak_rss_bytes=rss,OUT_regular_bytes=sizes)

def write_json(output,name,value):
 path=output/name
 with path.open('x') as stream:
  for piece in ENCODER.iterencode(value):stream.write(piece)
  stream.write('\n');stream.flush();os.fsync(stream.fileno())
 return full_pin(path)

def lossless_json_gzip(output,name,value,started):
 """All fields/records, insertion order, no selected rows or record limit."""
 path=output/name;wire_hash=hashlib.sha256();wire_bytes=0
 with path.open('xb') as raw:
  with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as zipped:
   for piece in ENCODER.iterencode(value):
    block=piece.encode('ascii');wire_hash.update(block);wire_bytes+=len(block);zipped.write(block)
   block=b'\n';wire_hash.update(block);wire_bytes+=1;zipped.write(block)
  raw.flush();os.fsync(raw.fileno())
 checkpoint(started,output)
 restored=hashlib.sha256();restored_bytes=0
 with gzip.open(path,'rb') as stream:
  while True:
   block=stream.read(2**20)
   if not block:break
   restored.update(block);restored_bytes+=len(block)
 require(restored_bytes==wire_bytes and restored.hexdigest()==wire_hash.hexdigest(),'complete gzip JSON wire decompression/EOF/SHA mismatch')
 result=full_pin(path)
 result.update(uncompressed_JSON_bytes=wire_bytes,uncompressed_JSON_sha256=wire_hash.hexdigest(),complete_JSON_wire_gzip_decompression_EOF_SHA_verified=True,no_fields_or_records_filtered=True)
 return result

def private_trace_controls(old,new,output):
 """Additional small controls belong only to the new600s phase, not old60s."""
 fixture=output/'private_trace_fixture.txt'
 with fixture.open('xb') as stream:stream.write(b'pure helper metadata trace control\n')
 with old.ReadOpenAudit() as audit:
  with fixture.open('rb') as stream:require(stream.read()==b'pure helper metadata trace control\n','small actual metadata fixture read differs')
 observed=audit.snapshot()
 require(type(observed['records']) is list and len(observed['records'])==1,'one actual small read-open audit record required')
 # This deliberately augmented JSON witness is a codec control, never relabeled
 # as an actual verifier trace. The full verifier trace is separately untouched.
 records=copy.deepcopy(observed['records'])
 records[0]['control_only_builtin_json_witness']={'floatbits':[-0.0,1e-300,1.25],'ordered':[True,0,None,'text']}
 baseline=old._trace_records(records)
 positive=[]
 for label,caller,explicit in [('default_list',copy.deepcopy(records),False),('default_tuple',tuple(copy.deepcopy(records)),False),('explicit_False_list',copy.deepcopy(records),True)]:
  before=value_snapshot(caller)
  result=new._trace_records(caller,_consume=False) if explicit else new._trace_records(caller)
  require(value_snapshot(caller)==before,'default nonmutation including mutableids failed: '+label)
  require(value_snapshot(result)[0]==value_snapshot(baseline)[0],'full normalized output type/order/value/floatbits mismatch: '+label)
  require(''.join(ENCODER.iterencode(result)).encode('ascii')==''.join(ENCODER.iterencode(baseline)).encode('ascii'),'full normalized byte/order output mismatch: '+label)
  positive.append(dict(case=label,caller_full_identity_type_order_value_floatbits_unchanged=True,full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd=True))
 owned=copy.deepcopy(records)
 require(type(owned) is list,'private consume only probe-owned builtin list')
 result=new._trace_records(owned,_consume=True)
 require(owned==[],'probe-owned complete private list was not cleared')
 require(value_snapshot(result)[0]==value_snapshot(baseline)[0] and ''.join(ENCODER.iterencode(result)).encode('ascii')==''.join(ENCODER.iterencode(baseline)).encode('ascii'),'private full normalized return differs from old bcd default')
 positive.append(dict(case='probe_owned_builtin_list_True',owned_list_completely_cleared=True,full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd=True))
 class ListSubclass(list):pass
 negatives=[]
 for label,caller,consume in [('nonbool_consume',copy.deepcopy(records),1),('tuple_True',tuple(copy.deepcopy(records)),True),('list_subclass_True',ListSubclass(copy.deepcopy(records)),True)]:
  # Preserve the actual outer type/id, and all nested mutable ids/values even
  # for the deliberately rejected list subclass; no helper result is invoked.
  before=(type(caller),id(caller),value_snapshot(tuple(caller)))
  try:new._trace_records(caller,_consume=consume)
  except Exception as error:
   require(type(error) is new.InputGraphError,'wrong private trace rejection class: '+label)
   require((type(caller),id(caller),value_snapshot(tuple(caller)))==before,'rejected private trace caller was changed: '+label)
   negatives.append(dict(case=label,class_name=type(error).__name__,message=str(error),rejected=True,caller_type_identity_nested_value_order_floatbits_unchanged=True))
  else:raise AssertionError('malformed private trace control accepted: '+label)
 require(len(positive)==4 and len(negatives)==3,'all additional private trace controls required')
 return dict(actual_small_ReadOpenAudit=observed,control_only_augmented_records=records,augmented_records_are_not_claimed_as_actual_full_verifier_trace=True,positive_controls=positive,rejections=negatives,old60pure_control_functions_not_changed=True)

def _old_parent_complete_return_constructors(old,graph):
 """Original pinned bcd pure constructors, never the new helper as oracle.

 Stored graph dictionaries were normalized for storage. Original verify_graph
 returns a deepcopy of FRESH_READER_CONTRACT, regenerated _coverage dictionaries
 in CLOSURE_CATEGORIES order, and regenerated _trace_coverage counts in its
 literal constructor order. Preserve every field/value/type/list/float bit;
 only these known output constructors supply their original insertion order.
 """
 reader=copy.deepcopy(old.FRESH_READER_CONTRACT)
 require(reader==graph['fresh_reader_contract'],'entire stored reader contract differs from original parent constant')
 saved_coverage=graph['coverage']
 require(type(saved_coverage) is dict and set(saved_coverage)==set(old.CLOSURE_CATEGORIES),'entire original closure category set required')
 for descriptor in saved_coverage.values():
  require(type(descriptor) is dict and set(descriptor)=={'canonical_files','bytes','owners'},'all original coverage descriptor fields required')
 coverage={category:{'canonical_files':saved_coverage[category]['canonical_files'],
                     'bytes':saved_coverage[category]['bytes'],
                     'owners':copy.deepcopy(saved_coverage[category]['owners'])}
           for category in old.CLOSURE_CATEGORIES}
 saved_trace=graph['trace_coverage']
 trace={
  'owned_file_attempts':saved_trace['owned_file_attempts'],
  'owned_namespace_directory_attempts':saved_trace['owned_namespace_directory_attempts'],
  'explicit_live_resource_directory_attempts':saved_trace['explicit_live_resource_directory_attempts'],
  'owned_regular_descriptor_attempts':saved_trace['owned_regular_descriptor_attempts'],
  'explicit_subprocess_pipe_attempts':saved_trace['explicit_subprocess_pipe_attempts'],
  'explicit_subprocess_null_device_attempts':saved_trace['explicit_subprocess_null_device_attempts'],
  'explicit_declared_absent_file_attempts':saved_trace['explicit_declared_absent_file_attempts'],
  'actual_subprocess_audit_attempts':saved_trace['actual_subprocess_audit_attempts'],
  'unique_records':saved_trace['unique_records'],
  'actual_read_open_attempts':saved_trace['actual_read_open_attempts']}
 require(type(saved_trace) is dict and set(saved_trace)==set(trace),'all original trace coverage fields required')
 require(coverage==saved_coverage and trace==saved_trace,'entire original constructor values differ from complete stored coverage dictionaries')
 return reader,coverage,trace

def expected_return_from_old(old):
 """Old bcd strict parser reads the entire fixed stored graph independently."""
 graph=old.strict_json(GRAPH_PIN['path'],GRAPH_PIN['sha256'],max_bytes=MAX_JSON_BYTES)
 require(type(graph) is dict and graph['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' and graph['consumer_scope'] is None,'complete fixed V20 input-only graph required')
 canonical=graph['canonical_files']
 require(type(canonical) is list and len(canonical)==37111,'complete37k canonical union required')
 paths={entry['path'] for entry in canonical}
 require(len(paths)==len(canonical),'canonical union must not contain duplicate paths')
 require(type(graph['requirements']['rows']) is dict and graph['requirements']['rows']['column_count']==5 and type(graph['requirements']['rows']['row_count']) is int,'complete five-column encoded requirement rows required')
 require(type(graph['owners']['rows']) is list and len(graph['owners']['rows'])==4473,'all fixed V20 logical owners required')
 require(type(graph['read_trace']['records']) is list and len(graph['read_trace']['records'])==63469 and graph['read_trace']['subprocess_records']==[],'complete fixed V20 saved trace required')
 require(graph['science_qualification_created'] is False and graph['live_resources_verified'] is False and graph['external_declaration_exit0_verified'] is False,'saved graph cannot create live or science qualification')
 metadata=dict(requirement_row_count=graph['requirements']['rows']['row_count'],requirement_column_count=5,canonical_files=len(canonical),owners=len(graph['owners']['rows']),namespaces=len(graph['namespaces']),aliases=len(graph['aliases']),saved_trace_records=len(graph['read_trace']['records']),saved_trace_actual_attempts=sum(record['attempt_count'] for record in graph['read_trace']['records']),absence_inputs=len(graph['absence_inputs']),closure_categories=len(graph['closure_categories']),complete_coverage_fields=list(graph['coverage']),complete_tracecoverage_fields=list(graph['trace_coverage']),scope=graph['scope'],consumer_scope=graph['consumer_scope'],newly_declared_input_paths=graph['newly_declared_input_paths'],newly_declared_input_pins=graph['newly_declared_input_pins'])
 oracle_reader,oracle_coverage,oracle_trace=_old_parent_complete_return_constructors(old,graph)
 expected={
  'schema':'AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2',
  'classification':'FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY',
  'consumer_scope':None,'consumer_selected_literal_and_canonical_paths':None,
  'consumer_complete_namespace_root_sequence':None,
  'scope':'INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION','phase':PHASE,
  'graph_content_sha256':graph['content_sha256'],
  'fresh_reader_contract':oracle_reader,
  'canonical_files_read':len(canonical),'actual_bytes_read':sum(entry['size_bytes'] for entry in canonical),
  'byte_count_scope':'CANONICAL_INPUT_UNION_ONLY_EXCLUDES_STORED_GRAPH_JSON',
  'logical_owner_requirements':graph['requirements']['rows']['row_count'],
  'exhaustive_namespaces_checked':len(graph['namespaces']),
  'explicit_aliases_checked':len(graph['aliases']),
  'coverage':oracle_coverage,'trace_coverage':oracle_trace,
  'live_io_scope':graph['live_io_scope'],'live_subprocesses_reexecuted':False,
  'declared_absence_inputs_checked_before_and_after_bytes':len(graph['absence_inputs']),
  'absence_inputs_are_not_regular_bytes_or_science':True,
  'caller_must_recheck_current_OS_identity_and_live_probe_results':True,
  'typed_snapshot':graph['typed_snapshot'],'science_qualification_created':False,
  'live_resources_verified':False,'external_declaration_exit0_verified':False,
  'caller_must_verify_live_environment_modules_PID_time_and_resources':True}
 require(expected['logical_owner_requirements']==238441 and expected['exhaustive_namespaces_checked']==86 and expected['explicit_aliases_checked']==186 and expected['declared_absence_inputs_checked_before_and_after_bytes']==479,'complete fixed V20 graph counts changed')
 require(graph['newly_declared_input_paths']=={} and graph['newly_declared_input_pins']=={} and len(graph['closure_categories'])==9 and len(graph['coverage'])==9,'complete fixed V20 scope/declaration changed')
 # Borrowed complete expected public fields survive; the full graph/trace/owner
 # and canonical pin tables are released before the new fresh verifier starts.
 del canonical,graph
 gc.collect()
 return expected,paths,metadata

def run(output_dir,driver_sha256):
 # Root actual pins and a READY source review are necessary before any I/O/API.
 require(SOURCE_STATUS=='READY_SOURCE_BOUND_BY_ROOT','UNREADY template cannot execute')
 require(type(NEW_HELPER_PATH) is str and NEW_HELPER_PATH.startswith('/Users/wen/spot/') and sha_text(NEW_HELPER_SHA256) and type(NEW_HELPER_SOURCE_BYTES) is int and NEW_HELPER_SOURCE_BYTES>0,'unknown helper path/SHA/bytes are not bindings')
 require(type(OUTPUT_PATH) is str and output_dir==OUTPUT_PATH and sha_text(driver_sha256),'Root exact output and actual driver SHA CLI binding required')
 require(sys.dont_write_bytecode and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None,'normal -B nonoptimized unprofiled process required')
 require(all(os.environ.get(key)=='1' for key in THREAD_KEYS),'original single-thread environment required')
 started=time.monotonic()
 def deadline(signum,frame):raise TimeoutError('unchanged600s fresh verifier control deadline')
 signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,STAGE_SECONDS)
 output=Path(output_dir);require(output.is_absolute() and not os.path.lexists(output),'one fresh exclusive output, no retry')
 output.mkdir(mode=0o700)
 report=dict(schema='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1',status='RUNNING_NO_METADATA_OR_SCIENCE_QUALIFICATION',actual_success_pins=None,PID=os.getpid(),parent_PID=os.getppid(),whole_host_seconds=WHOLE_HOST_SECONDS,stage_seconds=STAGE_SECONDS,rss_mib=RSS_MIB,joint_HOST_SOURCE_OUT_archive_bytes=JOINT_HOST_SOURCE_OUT_ARCHIVE_BYTES,history_bytes=HISTORY_BYTES,min_free_bytes=MIN_FREE_BYTES,threads=THREADS,children=CHILDREN,retries=RETRIES,business_component_executed=False,numeric_or_native_executed=False,whole_business_INPUT_qualified=False,native_RSS_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,helper_metadata_qualified=False,actual_external_genuine_host_and_Root_closed_exit0_required=True)
 try:
  self_before=full_pin(Path(__file__).resolve(),driver_sha256)
  graph_before=full_pin(GRAPH_PIN['path'],GRAPH_PIN['sha256'],GRAPH_PIN['identity'])
  old,old_before=load_pinned(OLD_HELPER_PATH,OLD_HELPER_SHA256,OLD_HELPER_SOURCE_BYTES,'axmat_fresh_control_independent_parent_bcd')
  new,new_before=load_pinned(NEW_HELPER_PATH,NEW_HELPER_SHA256,NEW_HELPER_SOURCE_BYTES,'axmat_fresh_control_actual_new_helper')
  require(type(NEW_HELPER_IDENTITY) is list and len(NEW_HELPER_IDENTITY)==7 and all(type(v) is int for v in NEW_HELPER_IDENTITY) and new_before['identity']==NEW_HELPER_IDENTITY,'Root actual installed helper exact seven-integer identity required')
  write_json(output,'ACTUAL_RUN_CLAIM.json',dict(PID=os.getpid(),parent_PID=os.getppid(),driver=self_before,helper=new_before,graph=graph_before,phase=PHASE,threads=THREADS,children=CHILDREN,retries=RETRIES))
  report['private_trace_controls']=private_trace_controls(old,new,output)
  checkpoint(started,output)
  expected,paths,expected_metadata=expected_return_from_old(old)
  report['independent_full_saved_graph_metadata']=expected_metadata
  with new.ReadOpenAudit() as audit:
   verified=new.verify_graph(GRAPH_PIN['path'],expected_sha256=GRAPH_PIN['sha256'],phase=PHASE)
  trace=audit.snapshot()
  exact_value(expected,verified,'complete_actual_fresh_verifier_return')
  require(trace['schema']=='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' and trace['coverage']=='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' and type(trace['records']) is list and trace['subprocess_records']==[],'actual full verifier read-open trace contract required')
  actual_paths=[]
  for record in trace['records']:
   require(type(record) is dict and record['event']=='open' and record['kind']=='path' and record['access']=='read' and record['observation']=='OPEN_ATTEMPT' and type(record['attempt_count']) is int and record['attempt_count']==1,'every actual verifier graph/input must open once as read-only path')
   actual_paths.append(record['path'])
  require(len(actual_paths)==len(set(actual_paths))==37112 and set(actual_paths)==paths|{GRAPH_PIN['path']},'all37111 canonical files plus1 fixed externalgraph must be really opened once')
  require(type(trace['unique_records']) is int and trace['unique_records']==len(trace['records']) and type(trace['actual_read_open_attempts']) is int and trace['actual_read_open_attempts']==sum(record['attempt_count'] for record in trace['records'])==37112,'complete actual open counts/attempts differ')
  require(trace['record_storage']=='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' and trace['success_of_open_attempt_is_not_observed'] is True and trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is True,'audit limited observation scope must remain honest')
  report['expected_complete_return_contract']=lossless_json_gzip(output,'EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz',expected,started)
  report['actual_complete_verifier_return']=lossless_json_gzip(output,'ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz',verified,started)
  report['actual_complete_ReadOpenAudit_trace']=lossless_json_gzip(output,'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz',trace,started)
  report['actual_complete_trace_counts']=dict(records=len(trace['records']),attempts=trace['actual_read_open_attempts'],canonical_files=verified['canonical_files_read'],external_graph_reads=1,no_subprocess_reexecuted=True)
  report['complete_return_fields_retained']=list(verified)
  report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal']=True
  del expected,paths,verified,trace,audit,actual_paths
  gc.collect()
  report['fixed_inputs_before']=dict(driver=self_before,old_parent=old_before,new_helper=new_before,stored_graph=graph_before)
  after=dict(driver=full_pin(Path(__file__).resolve(),driver_sha256),old_parent=full_pin(OLD_HELPER_PATH,OLD_HELPER_SHA256),new_helper=full_pin(NEW_HELPER_PATH,NEW_HELPER_SHA256),stored_graph=full_pin(GRAPH_PIN['path'],GRAPH_PIN['sha256'],GRAPH_PIN['identity']))
  require(after==report['fixed_inputs_before'],'actual fixed source/graph fullSHA7identity changed across completefresh control')
  report['fixed_inputs_after']=after
  report['caps_checkpoint']=checkpoint(started,output)
  report['status']='ACTUAL_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_RETURNED_PENDING_EXTERNAL_ROOT'
  report['actual_success_pins']=dict(helper=new_before,graph=graph_before,full_return=report['actual_complete_verifier_return'],full_trace=report['actual_complete_ReadOpenAudit_trace'])
  report_pin=write_json(output,'ACTUAL_REPORT.json',report)
  final_checkpoint=checkpoint(started,output)
  print(json.dumps(dict(status=report['status'],report=report_pin,PID=os.getpid(),parent_PID=os.getppid(),actual_external_genuine_host_and_Root_closed_exit0_required=True,final_checkpoint=final_checkpoint),allow_nan=False),flush=True)
 except BaseException as error:
  report.update(status='FAILED_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_NO_RETRY',error=dict(class_name=type(error).__name__,message=str(error)),actual_success_pins=None,helper_metadata_qualified=False)
  write_json(output,'FAILED_REPORT.json',report)
  raise
 finally:signal.setitimer(signal.ITIMER_REAL,0)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output-dir',required=True)
 parser.add_argument('--driver-sha256',required=True,help='actual Root pinned READY driver SHA, supplied by the future genuine host; no self-hash literal')
 args=parser.parse_args();run(args.output_dir,args.driver_sha256)

if __name__=='__main__':main()
