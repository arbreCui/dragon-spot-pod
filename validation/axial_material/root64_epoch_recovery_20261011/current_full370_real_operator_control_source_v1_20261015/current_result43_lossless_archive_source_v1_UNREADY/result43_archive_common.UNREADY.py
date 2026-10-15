"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=192*2**20
ARCHIVE_CAP=184*2**20
SOURCE_CAP=16*2**20
CHUNK=2**20
PYTHON=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FALSE=dict(physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
 scientific_accuracy_qualified=False,full_reference_qualified=False,
 result_values_decoded=False,numerical_executed=False,compiler_executed=False,
 native_executed=False,files_deleted=False,plain_retirement_authorized=False)

def require(ok,message):
 if type(ok)is not bool or not ok:raise RuntimeError(message)

def identity(s):
 return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current7(p):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int
  and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity']),'complete integer fullPF')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)
  and s.st_nlink==1 and s.st_uid==os.getuid() and identity(s)==p['identity']and p['size_bytes']==s.st_size,
  'literal regular private file current7')
 return s

def pin(q):
 q=Path(q);s=q.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'own regular single-link file')
 before=identity(s);h=hashlib.sha256();n=0
 with q.open('rb')as f:
  while b:=f.read(CHUNK):h.update(b);n+=len(b)
 require(identity(q.lstat())==before and n==before[4],'whole EOF identity stable')
 return dict(path=str(q.absolute()),sha256=h.hexdigest(),size_bytes=n,identity=before)

def metadata(p):
 current7(p);require(p['size_bytes']<8*2**20,'metadata role below8MiB')
 raw=Path(p['path']).read_bytes();require(len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata fullEOF SHA')
 value=json.loads(raw);current7(p);return value

def source_module(p,name):
 current7(p);require(pin(p['path'])==p,'whole selected Source')
 cached=sys.modules.get(name)
 if cached is not None:
  require(Path(cached.__file__).absolute()==Path(p['path']),'cached original Source exact module origin, no replacement')
  current7(p);return cached
 spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec)
 sys.modules[name]=m;spec.loader.exec_module(m);current7(p);return m

def write_new(q,value,bound):
 raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
 require(len(raw)<bound,'own metadata hard bound')
 fd=os.open(q,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
 with os.fdopen(fd,'wb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 dfd=os.open(Path(q).parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(dfd)
 finally:os.close(dfd)
 return pin(q)

def true0(p,key,stdout_role,expected):
 d=metadata(p);r=d[key]
 require(d['observed_closed']is True and type(d['original_integer_exit_code'])is int
  and d['original_integer_exit_code']==0 and type(r['exit_code'])is int and r['exit_code']==0
  and 'session_id'not in r,'genuine typed original closed0; no live session')
 lines=r['output'].splitlines();require(bool(lines),'actual terminal stdout')
 require(json.loads(lines[-1])[stdout_role]==expected,'actual terminal complete PF')
 return d

def contains(value,p):
 return value==p or type(value)is dict and any(contains(v,p)for v in value.values())or type(value)is list and any(contains(v,p)for v in value)

def admit(binding):
 """Final Source preparation must supply actual keys, never future status/PF guesses."""
 require(binding['schema']=='RESULT43_LOSSLESS_ARCHIVE_EXECUTION_BINDING_V1'
  and binding['Source_admission_ready']is True and binding['draft_unready']is False
  and binding['original_caps']==CAPS,'new independently admitted binding; original caps')
 registry=metadata(binding['original_result43_registry_pin'])
 require(binding['saved_registry_selected_pins']==registry['selected_pins']
  and len(registry['selected_pins'])==43
  and sum(p['size_bytes']for p in registry['selected_pins'])==583122866,
  'immutable saved43 registry, no result omission')
 require(binding['all48_plain_pins']==registry['selected_pins']+binding['completed_A2_new5_JSONL_pins']
  and len(binding['all48_plain_pins'])==48
  and sum(p['size_bytes']for p in binding['all48_plain_pins'])==805236925
  and len({p['path']for p in binding['all48_plain_pins']})==48,'exact saved43 plus A2 new5; literal48 unique inputs')
 a=metadata(binding['completed_A2_host_pin']);post=metadata(binding['completed_A2_post_pin'])
 require(binding['completed_A2_new5_JSONL_pins']==[p for p in a['complete_output_pins']if Path(p['path']).suffix=='.jsonl']
  and len(binding['completed_A2_new5_JSONL_pins'])==5
  and sum(p['size_bytes']for p in binding['completed_A2_new5_JSONL_pins'])==222114059,'all5 JSONL members in actual A2 manifest')
 require(a['status']=='ACTUAL_CURRENT_A_FULL_MATH_CONTROL_EVIDENCE_EXIT2_CLOSED_ONLY'
  and a['failure']is None and a['current_source_gap_resolved']is True
  and a['actual_child_evidence_only_integer_exit_code']==2
  and a['final_report_resource_check_passed']is True,'actual current A2 gap0, original child2')
 true0(binding['completed_A2_Root_tools_pin'],'actual_terminal_return','report_pin',binding['completed_A2_host_pin'])
 require(post['schema']=='INDEPENDENT_ACTUAL_CURRENT_A_FULL_AGGREGATE_AFTER_OVERV_METADATA_POSTVERIFY_V1'
  and post['status']=='PASS_RECORDED_CURRENT_A_FULL_AGGREGATE_SOURCE_GAP0_METADATA_ONLY_CHILD2_PRESERVED'
  and post['actual_Host_report_pin']==binding['completed_A2_host_pin']
  and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_code']==2,
  'actual independent A2 post scope, no child0 laundering')
 true0(binding['completed_A2_post_tools_pin'],'actual_review_return','review_pin',binding['completed_A2_post_pin'])
 # No schema/status of the future early14 post is asserted by this draft.
 # Its exact actual-key projection must be reviewed and fixed before final Source admission.
 require(binding['early14_actual_key_projection_Source_reviewed']is True
  and binding['early14_actual_retirement_and_post0_verified']is True
  and len(binding['actual_retired_early14_pins'])==14
  and sum(p['size_bytes']for p in binding['actual_retired_early14_pins'])==149659264,
  'actual early14 receipt/Root0/independent post0 required, future NULL is unready')
 ep=binding['early14_closure_pins'];retirement=metadata(ep['receipt']);earlypost=metadata(ep['post'])
 require(retirement['schema']=='LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOL_RETIREMENT_RECEIPT_V1'
  and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOLS_ONLY'
  and retirement['failure']is None and retirement['files_deleted']is True
  and retirement['actual_released_pins']==retirement['exact_target_pins']==binding['historical_early14_original_pins']
  and retirement['actual_released_pins']==binding['actual_retired_early14_pins']
  and retirement['actual_released_bytes']==149659264,'exact genuine completed early14 receipt, no historical reclassification')
 true0(ep['Root_tools'],'actual_execution_return','receipt_pin',ep['receipt'])
 projection=binding['early14_post_actual_role_projection']
 require(earlypost['schema']==projection['schema']and earlypost['status']==projection['status']
  and earlypost['failure']is None and earlypost[projection['receipt_pin_field']]==ep['receipt']
  and earlypost[projection['Root_tools_pin_field']]==ep['Root_tools'],'future post actual-key projection; no guessed field alias')
 true0(ep['post_tools'],'actual_review_return','review_pin',ep['post'])
 for p in binding['actual_retired_early14_pins']:
  require(not os.path.lexists(p['path']),'exact retired early14 absent, historical PF only')
 require(binding['historical_completed_guard_role_paths']==binding['old30_intersection_paths']
  and len(binding['historical_completed_guard_role_paths'])==30
  and set(binding['historical_completed_guard_role_paths'])<=set(p['path']for p in binding['all48_plain_pins']),
  'all30 completed historical input guards retained in archive lookup')
 intersection=metadata(binding['original_result43_old_input_intersection_pin'])
 require(binding['old30_intersection_paths']==[p['path']for p in intersection['exact_original_input_intersection_pins']]
  and intersection['exact_input_intersection_count']==30,'unchanged exact old30 historical guard metadata')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots']
 require(binding['complete_joint_roots']==prefix+[str(out)]
  and prefix[:64]==binding['completed_A2_complete64_roots']and len(prefix)>=64
  and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))
  and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),
  'latest complete prefix plus exactly one whole owning archive output; no reset/overlap')
 require(retirement['complete_joint_roots']==binding['completed_A2_complete64_roots'],
  'actual early14 receipt uses complete A2 64 prefix; archival stage inherits latest full prefix')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP
  and binding['bounded_Source_metadata_bytes']==SOURCE_CAP,'192MiB total/184MiB payload/8MiB metadata headroom/16MiB Source')
 for p in binding['retained_native_current7_pins']+binding['all48_plain_pins']:current7(p)
 require(len(binding['retained_native_current7_pins'])==66,'all66 remaining native contexts/XSM/final55 pair preserved')
 return out

def original_resource_modules(binding):
 # Keep the already-proven original import spine. No compiler or production main is invoked.
 source_module(binding['original_production_inputs_Source_pin'],'production_inputs')
 production=source_module(binding['original_production_resource_Source_pin'],'production_runner')
 factory=source_module(binding['original_history_resource_Source_pin'],'result43_original_history')
 return production,factory

def own_bytes(out):
 if not out.exists():return 0
 require(not any(q.is_symlink()for q in(out,*out.parents)),'own output ancestors have no aliases')
 total=0
 for q in out.rglob('*'):
  s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'own namespace has no aliases')
  if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total

def current_metadata(p):
 q=Path(p['path'])
 if q==Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'):
  s=q.lstat();require(p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'
   and s.st_nlink==p['identity'][3]==2 and identity(s)==p['identity']and s.st_size==p['size_bytes']
   and stat.S_ISREG(s.st_mode)and not any(x.is_symlink()for x in(q,*q.parents)),'sole original compiler nlink2 metadata exception')
 else:current7(p)

class Resources:
 def __init__(self,binding,started,seconds):
  self.binding=binding;self.started=started;self.seconds=seconds
  self.out=Path(binding['planned_actual_output_root'])
  production,factory=original_resource_modules(binding)
  self.joined=production.DiskResources(ROOT/'validation',binding['complete_joint_roots'],8*2**30,2*2**30)
  self.history=factory.DynamicHistoryResources(ART,factory.history_roots([str(self.out)],ART),8*2**30,96*2**30,production.ResourceFailure)
  initial=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure).check()
  require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation')
 def light(self):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-self.started<self.seconds,'unchanged SELF512/original start wall cap')
  require(own_bytes(self.out)<OUT_CAP,'whole archive output192MiB hard cap')
  require(own_bytes(BASE)<SOURCE_CAP,'entire own Source/metadata16MiB component')
  return peak
 def check(self):
  peak=self.light();h=self.history.check();f=self.joined.check();extra=0
  roots=self.binding['complete_joint_roots']
  for p in self.binding['explicit_cumulative_metadata_file_pins']:
   current_metadata(p)
   if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
  unlinked={}
  for fd in os.listdir('/dev/fd'):
   try:s=os.fstat(int(fd))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  require(f['artifact_bytes']+extra+sum(unlinked.values())<2*2**30,'joint2GiB includes external metadata and open-unlinked')
  require(h['artifact_bytes']+20971764748+64*2**20<96*2**30
   and f['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/free8')
  return dict(original_history=h,complete_joint=f,explicit_external_metadata_bytes=extra,
   own_open_unlinked_bytes=sum(unlinked.values()),SELF_peak_bytes=peak,
   original_elapsed_seconds=time.monotonic()-self.started)
