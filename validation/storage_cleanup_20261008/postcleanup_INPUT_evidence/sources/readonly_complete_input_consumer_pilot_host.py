"""Reviewed original705/38de own-child host for one INPUT-only private callback.

No production API, producer.modules(), cold/controller preparation, transport,
fixture or solver runs here. The original supervisor and parent are normally
imported at their genuine paths in this isolated process. Root must observe
actual tool return before recording any performance witness.
"""
import sys,os,time
STARTED=time.monotonic()
STATUS='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT'
if STATUS!='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT':raise ValueError('UNREADY: source review required; do not execute')
if sys.flags.optimize!=0 or'PYTHONOPTIMIZE'in os.environ:raise ValueError('nonoptimized source predicates required')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
if any(os.environ.get(k)!='1'for k in THREADS):raise ValueError('single-thread environment required')
sys.dont_write_bytecode=True
import argparse,hashlib,importlib,json,re,shutil,stat
from pathlib import Path
PYTHON='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
ART=Path('/Users/wen/spot/validation/artifacts')
FAMILY='STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT'
FULL=Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py')
FULL_SHA='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
PARENT=ART/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py'
PARENT_SHA='38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'
GUARD=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_source_factor_production.py')
GUARD_SHA='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
BUILDER=Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_cache_production.py')
BUILDER_SHA='92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
if str(Path(sys.executable).resolve())!=PYTHON:raise ValueError('actual original Python3.12 required')
def ordinary(path,missing=False):
 p=Path(path)
 if not p.is_absolute()or'..'in p.parts:raise ValueError('absolute ordinary path required')
 for a in[*reversed(p.parents),p]:
  try:s=a.lstat()
  except FileNotFoundError:
   if missing:continue
   raise
  if stat.S_ISLNK(s.st_mode)or(a!=p and not stat.S_ISDIR(s.st_mode)):raise ValueError('ordinary ancestry required')
 return p
def digest(path):
 p=ordinary(path);pre=p.lstat();keys=('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink');sig=lambda s:tuple(getattr(s,k)for k in keys)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  first=os.fstat(fd)
  if not stat.S_ISREG(first.st_mode)or sig(pre)!=sig(first):raise ValueError('input changed before opened read')
  h=hashlib.sha256();size=0
  while raw:=os.read(fd,8*2**20):h.update(raw);size+=len(raw)
  last=os.fstat(fd);ordinary(p);post=p.lstat()
  if sig(first)!=sig(last)or sig(last)!=sig(post)or size!=first.st_size:raise ValueError('input pathname changed')
  return h.hexdigest()
 finally:os.close(fd)
def owned(path,sha):
 p=ordinary(path)
 if re.fullmatch('[0-9a-f]{64}',sha)is None or sha=='0'*64 or digest(p)!=sha:raise ValueError('independently pinned bytes required')
 return p
def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate JSON key')
  d[k]=v
 return d
def read(path):return json.loads(Path(path).read_text(),object_pairs_hook=unique,parse_constant=lambda x:(_ for _ in()).throw(ValueError('nonfinite JSON')))
def normal_import(path,sha):
 p=owned(path,sha);name=p.stem;old=sys.modules.get(name)
 if old is not None:
  if getattr(old,'__file__',None)!=str(p)or getattr(old,'__spec__',None)is None or old.__spec__.origin!=str(p):raise ValueError('foreign canonical module already loaded: '+name)
  return old
 sys.path.insert(0,str(p.parent));m=importlib.import_module(name)
 if m.__file__!=str(p)or m.__spec__.origin!=str(p):raise ValueError('genuine normal import path differs')
 return m
p=argparse.ArgumentParser();p.add_argument('--binding',required=True);p.add_argument('--binding-sha256',required=True);a=p.parse_args()
binding=read(owned(a.binding,a.binding_sha256))
if binding['pilot_schema']!='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_BINDING_V1'or binding['draft_status']!='REVIEWED_READONLY_PRIVATE_CONSUMER_PILOT':raise ValueError('reviewed INPUT-only pilot contract required')
if'binding_descriptor'in binding or binding['pilot_context']['runtime_context']is not None or binding['pilot_context']['allow_unbound_initial_INPUT_declaration']is not True:raise ValueError('standalone binding/no self-cycle required')
self_path=Path(__file__).absolute();owned(self_path,binding['pilot_context']['additional_expected_files'][str(self_path)])
if'production_runner'in sys.modules:raise ValueError('fresh isolated canonical parent import required')
for name in('production_inputs','snapshot_control_preflight','qualified_snapshot_ingestion','numerical_layout_admission','white_receiver_tracking'):
 path=PARENT.parent/(name+'.py');normal_import(path,binding['supervisor_expected_files'][str(path)])
c=normal_import(PARENT,PARENT_SHA);full=normal_import(FULL,FULL_SHA);h=normal_import(GUARD,GUARD_SHA);b=normal_import(BUILDER,BUILDER_SHA)
if(full.SerialExecutor is not c.SerialExecutor or full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)
 or full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__ or full.OwnRSSSerialExecutor.execute is not c.SerialExecutor.execute
 or full.OwnRSSSerialExecutor.__init__.__code__.co_filename!=str(PARENT)or full.OwnRSSSerialExecutor.execute.__code__.co_filename!=str(PARENT)
 or full.OwnRSSSerialExecutor._process.__code__.co_filename!=str(FULL)
 or full.OwnRSSSerialExecutor._process.__globals__ is not full.__dict__
 or c.SerialExecutor.__init__.__globals__ is not c.__dict__ or c.SerialExecutor.execute.__globals__ is not c.__dict__):raise ValueError('actual original source and direct supervisor MRO required')
h.guard_admission(full) # Original immutable tested supervision INPUT; no new fixture credit.
for m in tuple(sys.modules.values()):
 path=getattr(m,'__file__',None)
 if path and str(path).startswith('/Users/wen/spot/validation/'):
  expected=binding['supervisor_expected_files'].get(str(Path(path).absolute()))
  if expected is None:raise ValueError('loaded project supervisor dependency has no old expected byte owner: '+str(path))
  owned(path,expected)
roots=binding['pilot_context']['resource_roots'];roots=[str(p)for p in b.validate_history_roots(roots,ART)]
resources=b.DynamicHistoryResources(ART,roots,8*2**30,96*2**30,c.ResourceFailure);before=resources.check()
base=ordinary(binding['pilot_work_base'],missing=True)
if not str(base).startswith('/private/tmp/')or os.path.lexists(base):raise ValueError('exclusive TMP observation family required; no retry')
base.mkdir();(base/'runtime').mkdir();(base/'consumer').mkdir();(base/FAMILY).mkdir()
helper=binding['bounded_helper'];shutil.copy2(owned(helper['path'],helper['sha256']),base/'runtime/run_bounded_dragon.py')
owned(base/'runtime/run_bounded_dragon.py',helper['sha256'])
remaining=1800-(time.monotonic()-STARTED)
if remaining<=0:raise ValueError('whole1800 exhausted before original constructor')
runner=full.OwnRSSSerialExecutor(base,remaining,FAMILY,resources)
if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).absolute()!=base/'runtime/run_bounded_dragon.py'or runner.records!=[]:raise ValueError('genuine constructor/local helper required')
child=binding['pilot_child'];owned(child['path'],child['sha256'])
command=[PYTHON,child['path'],'--binding',a.binding,'--binding-sha256',a.binding_sha256]
runner.execute(base/'consumer','consume',command,600,'AXMAT-PRIVATE-COMPLETE-INPUT-CONSUMER-PILOT-RETURNED')
result=read(base/'consumer/result.json');watch=read(base/'consumer/consume.watchdog.json');after=resources.check();elapsed=time.monotonic()-STARTED
if(len(runner.records)!=1 or runner.records[0]['status']!='PASS'or runner.records[0]['command']!=command
 or watch['command']!=command or type(watch['returncode'])is not int or watch['returncode']!=0 or watch['limit_failure']is not None
 or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True
 or not 0<=watch['sampled_peak_rss_mib']<512 or not 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=600
 or not elapsed<1800 or result['binding']!=dict(path=a.binding,sha256=a.binding_sha256)
 or any(result[k]is not False for k in('component_API_executed','consumer_scope_used','cold_controller_imported','cold_controller_bound','cold_prepared',
 'cold_MRO_proved','cold_fixture_passed','physics_or_native_transport_executed','combined_runtime_native_RSS_proved',
 'actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','RSS_qualification_claimed'))):raise ValueError('complete genuinely guarded INPUT-only pilot required')
result=dict(schema='AXMAT_STANDALONE_PRIVATE_COMPLETE_INPUT_CONSUMER_PILOT_ACTUAL_HOST_V1',
 binding=dict(path=a.binding,sha256=a.binding_sha256),actual_command=command,child_result=dict(path=str(base/'consumer/result.json'),sha256=digest(base/'consumer/result.json')),
 supervisor_source=dict(path=str(FULL),sha256=FULL_SHA),parent_source=dict(path=str(PARENT),sha256=PARENT_SHA),
 local_bounded_helper=dict(path=str(base/'runtime/run_bounded_dragon.py'),sha256=helper['sha256']),stage_records=runner.records,watchdog=watch,
 resources_before=before,resources_after=after,whole_elapsed_seconds=elapsed,total_wall_cap_seconds=1800,stage_wall_cap_seconds=600,RSS_cap_mib=512,
 threads=1,children_at_once=1,retries=0,supervisor_original_MRO_used=True,cold_MRO_proved=False,cold_fixture_passed=False,
 component_API_executed=False,cold_controller_imported=False,cold_controller_bound=False,cold_prepared=False,
 physics_or_native_transport_executed=False,combined_runtime_native_RSS_proved=False,actual_full_FLU_entry_executed=False,AAA_accuracy_qualified=False,ABA_admitted=False)
with(base/'result.json').open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
print(json.dumps(result,allow_nan=False),flush=True)
