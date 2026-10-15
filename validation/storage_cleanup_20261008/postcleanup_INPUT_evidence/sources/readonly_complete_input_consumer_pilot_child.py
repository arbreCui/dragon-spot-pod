"""Reviewed standalone private consumer pilot; no cold/controller or child launch.

Root must separately review this stopped source before a new, explicitly
bound performance-only version may run. The complete reviewed input graph and
all additional success/intake inputs are freshly checked; no owner is filtered.
The callback is invoked once with runtime_context=None and explicit initial
INPUT-only permission. It does not call any production/diagnostic API.
"""
import sys, os, time
STARTED=time.monotonic()
STATUS='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT'
if STATUS!='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT':raise ValueError('UNREADY: source review required; do not execute')
if sys.flags.optimize!=0 or 'PYTHONOPTIMIZE'in os.environ:raise ValueError('nonoptimized source predicates required')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
if any(os.environ.get(k)!='1'for k in THREADS):raise ValueError('single-thread environment required')
sys.dont_write_bytecode=True
import argparse, gc, hashlib, importlib, json, re, stat
from pathlib import Path
PYTHON='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
SCHEMA='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_BINDING_V1'
if str(Path(sys.executable).resolve())!=PYTHON:raise ValueError('actual original Python3.12 required')
def read_owned(path,expected):
 p=Path(path)
 if not p.is_absolute()or'..'in p.parts:raise ValueError('absolute ordinary input required')
 for ancestor in[*reversed(p.parents),p]:
  s=ancestor.lstat()
  if stat.S_ISLNK(s.st_mode)or(ancestor!=p and not stat.S_ISDIR(s.st_mode)):raise ValueError('ordinary input ancestry required')
 pre=p.lstat();keys=('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink');sig=lambda s:tuple(getattr(s,k)for k in keys)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  first=os.fstat(fd)
  if not stat.S_ISREG(first.st_mode)or sig(pre)!=sig(first):raise ValueError('input changed before opened read')
  chunks=[];h=hashlib.sha256();size=0
  while raw:=os.read(fd,8*2**20):chunks.append(raw);h.update(raw);size+=len(raw)
  last=os.fstat(fd);post=p.lstat()
  if sig(first)!=sig(last)or sig(last)!=sig(post)or size!=first.st_size:raise ValueError('input pathname changed')
  if re.fullmatch('[0-9a-f]{64}',expected)is None or expected=='0'*64 or h.hexdigest()!=expected:raise ValueError('independently pinned input differs')
  return b''.join(chunks)
 finally:os.close(fd)
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
p=argparse.ArgumentParser();p.add_argument('--binding',required=True);p.add_argument('--binding-sha256',required=True);a=p.parse_args()
binding=json.loads(read_owned(a.binding,a.binding_sha256),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite JSON')))
if binding['pilot_schema']!=SCHEMA or binding['draft_status']!='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT':raise ValueError('reviewed INPUT-only pilot contract required')
if'binding_descriptor'in binding:raise ValueError('external binding descriptor must not make a self-pin cycle')
if binding['pilot_context']['runtime_context']is not None or binding['pilot_context']['allow_unbound_initial_INPUT_declaration']is not True:raise ValueError('standalone initial INPUT-only context required')
if'production_runner'in sys.modules:raise ValueError('pilot child must not inherit a producer/cold controller module')
self_path=Path(__file__).absolute();expected=binding['pilot_context']['additional_expected_files'].get(str(self_path))
if expected is None:raise ValueError('actual child source owner missing')
read_owned(self_path,expected)
source=binding['binding_source'];read_owned(source['path'],source['sha256']);path=Path(source['path'])
if path.stem in sys.modules:raise ValueError('fresh ordinary private consumer module required')
sys.path.insert(0,str(path.parent));consumer=importlib.import_module(path.stem)
if consumer.__file__!=str(path)or consumer.__spec__.origin!=str(path):raise ValueError('actual private consumer path differs')
binding['binding_descriptor']=dict(path=a.binding,sha256=a.binding_sha256)
components,evidence=consumer.consume_completed_inputs(binding,binding['pilot_context'],phase='standalone_readonly_pilot')
if(evidence['consumer_scope_used']is not False or evidence['original_component_APIs_executed_in_this_process']is not False
 or evidence['new_binding_fixture_pass_claimed']is not False or evidence['science_qualification']is not False
 or any(evidence[k]['cold_binding']['current_cold_MRO_established']is not False for k in('current_before','current_after'))
 or any(evidence[k]['cold_binding']['new_binding_fixture_pass_claimed']is not False for k in('current_before','current_after'))
 or set(components)!=set(('original92','memory438','physical','dedup','capture','combined'))
 or'production_runner'in sys.modules):raise ValueError('standalone complete INPUT-only scope differs')
component_keys=list(components);del components;gc.collect()
elapsed=time.monotonic()-STARTED
if not 0<=elapsed<600:raise ValueError('original stage wall cap exceeded')
result=dict(schema='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_ACTUAL_CHILD_V1',binding=dict(path=a.binding,sha256=a.binding_sha256),
 private_consumer=source,actual_child_source=dict(path=str(self_path),sha256=expected),whole_component_return_keys=component_keys,
 complete_INPUT_evidence=evidence,elapsed_seconds=elapsed,component_API_executed=False,consumer_scope_used=False,
 cold_controller_imported=False,cold_controller_bound=False,cold_prepared=False,cold_MRO_proved=False,cold_fixture_passed=False,
 physics_or_native_transport_executed=False,combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,
 AAA_accuracy_qualified=False,ABA_admitted=False,RSS_qualification_claimed=False)
output=Path(binding['pilot_work_base'])/'consumer/result.json'
with output.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print('AXMAT-PRIVATE-COMPLETE-INPUT-CONSUMER-PILOT-RETURNED',flush=True)
