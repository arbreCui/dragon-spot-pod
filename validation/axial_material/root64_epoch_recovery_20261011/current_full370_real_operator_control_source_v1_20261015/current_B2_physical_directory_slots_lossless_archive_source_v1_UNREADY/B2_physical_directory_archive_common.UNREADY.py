"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=8*2**20
ARCHIVE_CAP=4*2**20
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
 q=Path(q)
 if q.is_relative_to(BASE):require(own_bytes(BASE)+len(raw)<SOURCE_CAP,'entire Source16MiB before metadata write')
 else:
  owners=[a for a in q.parents if a.parent==ART]
  require(len(owners)==1 and own_bytes(owners[0])+len(raw)<OUT_CAP,'entire sole archive output8MiB before metadata write')
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

def unique(rows):
 out={}
 for p in rows:require(p['path']not in out or out[p['path']]==p,'same path same wholePF');out[p['path']]=p
 return list(out.values())
def current_failed_v1(p,binding):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in binding['retained_failed_v1_current7_only_pins'],'only exact failed-v1 current7-only role; no SHA/fullPF claimed')
 q=Path(p['path']);s=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int for x in p['identity'])and identity(s)==p['identity']and s.st_size==p['size_bytes'],'entire exact failed-v1 file stable current7, no partial body open/hash or generic missing skip')
 return s

def current_all_retained(binding):
 for p in binding['all1_plain_pins']+binding['retained_current7_pins']:current7(p)
 for p in binding['retained_failed_v1_current7_only_pins']:current_failed_v1(p,binding)
def admit(binding):
 require(binding['schema']=='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_BINDING_V1'and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False and binding['Source_admission_ready']is False and binding['original_caps']==CAPS,'NULL actual comparison/post/latest resource binding cannot admit archive')
 h=metadata(binding['actual_comparison_Host_report_pin']);post=metadata(binding['actual_comparison_post_pin']);child=metadata(binding['actual_comparison_child_report_pin']);prior=metadata(binding['latest_complete_plan_pin'])
 true0(binding['actual_comparison_Root_tools_pin'],'actual_terminal_return','report_pin',binding['actual_comparison_Host_report_pin']);true0(binding['actual_comparison_post_tools_pin'],'actual_review_return','review_pin',binding['actual_comparison_post_pin'])
 require(h['schema']=='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_GUARDED_ROOT_REPORT_V1'and h['status']=='ACTUAL_CURRENT_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_CHILD2_CLOSED_ONLY'and h['failure']is None and h['complete_typed_word_comparison_completed']is True and h['actual_child_report_pin']==binding['actual_comparison_child_report_pin']and h['control_plan_pin']==binding['latest_complete_plan_pin']and h['final_report_resource_check_passed']is True and h['original_caps']==CAPS and len(h['records'])==1 and h['records'][0]['status']=='FAILED'and h['records'][0]['error']==h['original_runner_error']=='own-child stage failed; no retry'and type(h['actual_child_integer_exit_code'])is int and h['actual_child_integer_exit_code']==2,'genuine complete comparisonRoot0/evidencechild2 FAILED and original error retained, no retry')
 require(child['schema']=='ACTUAL_B55_NATIVEWARM_B2_FULL_TYPED_PATH_RAW_WORD_COMPARISON_V1'and child['status']=='ACTUAL_B55_NATIVEWARM_B2_COMPLETE_COMPARISON_EVIDENCE_ONLY'and child['compared_all_macro_records']==19620 and child['path_sets_equal']is True and child['all_original_records_and_typed_root_preserved']is True and child['original_archive_not_redecoded']is True and child['constructed_19249_field_subset_used']is False,'complete actual19620 typed root/all original words comparison, no reduced scope')
 require(post['schema']=='RECORDED_CURRENT_B55_NATIVEWARM_B2_COMPLETE_TYPED_COMPARISON_METADATA_POSTVERIFY_V2'and post['status']=='PASS_ACTUAL_CURRENT_B55_B2_COMPLETE_TYPED_COMPARISON_V2_ROOT0_CHILD2_METADATA_ONLY_DIFFERENCES_RECORDED'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==binding['actual_comparison_Host_report_pin']and post['actual_Root_tools_pin']==binding['actual_comparison_Root_tools_pin']and post['actual_child_report_pin']==binding['actual_comparison_child_report_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2,'same genuine independent comparison metadata post0, completion does not manufacture word equality')
 require(binding['actual_comparison_counts']==post['actual_comparison_counts']=={k:child[k]for k in('compared_all_macro_records','compared_original_payload_words','raw_word_mismatches','metadata_mismatches')}and type(child['raw_word_mismatches'])is int and child['raw_word_mismatches']==0 and type(child['metadata_mismatches'])is int and child['metadata_mismatches']==0 and type(child['compared_original_payload_words'])is int and child['compared_original_payload_words']>0 and post['complete_typed_word_comparison_completed']is True and post['actual_exact_inventory_metadata_and_all_words_equal']is True,'genuine v2 complete19620/all words and both actual mismatch counts0; still no online or physics qualification manufactured')
 ep=prior['actual_B2_complete_extraction_post_pin'];et=prior['actual_B2_complete_extraction_post_tools_pin'];extractpost=metadata(ep);true0(et,'actual_review_return','review_pin',ep)
 p=binding['actual_physical_directory_original_pin'];out=Path(binding['planned_actual_output_root'])
 require(extractpost['schema']=='RECORDED_CURRENT_NATIVEWARM_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_METADATA_POSTVERIFY_V1'and extractpost['status']=='PASS_ACTUAL_CURRENT_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_ROOT0_CHILD2_METADATA_ONLY'and extractpost['failure']is None and p==extractpost['complete_physical_directory_slots_pin']and p['size_bytes']==34371817 and binding['all1_plain_pins']==[p]and binding['original_plain_total_bytes']==p['size_bytes'],'only exact genuine B2 complete physical directory slots original fullPF, no parse or subset')
 failed=prior['retained_failed_v1_current7_only_pins'];ordinary=[q for q in prior['retained_current7_pins']if set(q)=={'path','sha256','size_bytes','identity'}]
 require(failed and all(type(q)is dict and set(q)=={'path','size_bytes','identity'}for q in failed)and [q for q in prior['retained_current7_pins']if q not in ordinary]==failed and binding['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']==failed and post['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved']is True and post['prior_v1_partial_payload_body_not_opened_or_hashed_by_post']is True,'entire failed-v1 tree remains only exact current7 roles, never SHA/fullPF or completed equality evidence')
 require(binding['prior_failed_v1_closure_pins']==post['prior_failed_v1_closure_pins']=={k:prior[k]for k in('actual_failed_v1_plan_pin','actual_failed_v1_Host_report_pin','actual_failed_v1_Root_tools_pin','actual_failed_v1_post_pin','actual_failed_v1_post_tools_pin','actual_failed_v1_final_CLI_pin')},'same genuine priorRoot1/child-15/failurepost0 closure remains separate from actual v2 success')
 expected=unique(ordinary+prior['retained_B2_current_epoch_readonly_pins']+post['new_complete_output_full_pins'])
 require(p in expected and binding['retained_current7_pins']==[q for q in expected if q!=p]and binding['retained_B2_current_epoch_readonly_pins']==prior['retained_B2_current_epoch_readonly_pins'],'all comparison outputs, all SQL/pools, prior Bagg16/B4 archives/native/inputs and nine cold readonly B2 roles retained; only exact physical ledger separate target')
 hf=metadata(h['host_freeze_pin']);proofs=[binding[k]for k in('latest_complete_plan_pin','actual_comparison_Host_report_pin','actual_comparison_Root_tools_pin','actual_comparison_child_report_pin','actual_comparison_post_pin','actual_comparison_post_tools_pin')]+[h['host_freeze_pin'],h['source_freeze_pin'],ep,et]
 require(binding['base_explicit_cumulative_metadata_file_pins']==prior['explicit_cumulative_metadata_file_pins']and binding['explicit_cumulative_metadata_file_pins']==unique(binding['base_explicit_cumulative_metadata_file_pins']+hf['explicit_cumulative_metadata_file_pins']+proofs),'complete current comparison host and actual external metadata union, no dropped oldHost/SDK/tool roles or large cold body in fresh metadata')
 prefix=binding['inherited_latest_complete_joint_roots'];require(prefix==h['complete_joint_roots']==prior['complete_joint_roots']and len(prefix)==79 and binding['complete_joint_roots']==prefix+[str(out)]and out.parent==ART and len(binding['complete_joint_roots'])==80 and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),'entire latest79 including both comparison roots plus exactly one owning archive80 root, all FTOP Source counted')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP and binding['metadata_runtime_headroom_bytes']==4*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP and binding['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True,'strict total8MiB=4payload+4runtime metadata plus Source16, original caps unchanged; actual gzip can fail without retry')
 current_all_retained(binding)
 return out

def original_resource_modules(binding):
 # Keep the already-proven original import spine. No compiler or production main is invoked.
 source_module(binding['original_production_inputs_Source_pin'],'production_inputs')
 production=source_module(binding['original_production_resource_Source_pin'],'production_runner')
 factory=source_module(binding['original_history_resource_Source_pin'],'B4_original_history')
 return production,factory

def own_bytes(out):
 if not out.exists():return 0
 require(not any(q.is_symlink()for q in(out,*out.parents)),'own output ancestors have no aliases')
 total=0
 for q in out.rglob('*'):
  s=q.lstat();require(not stat.S_ISLNK(s.st_mode),'own namespace has no aliases')
  if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total

def metadata_role_context(binding):
 build=metadata(binding['original_guard_build_plan_pin'])
 bm=source_module(binding['original_guard_build_contract_Source_pin'],'B4_original_build_metadata_roles')
 return build,bm

def current_metadata(p,binding,context=None):
 current7(binding['original_guard_build_plan_pin']);current7(binding['original_guard_build_contract_Source_pin'])
 build,bm=metadata_role_context(binding)if context is None else context
 bm.current_metadata_role(p,build)


class Resources:
 def __init__(self,binding,started,seconds):
  self.binding=binding;self.started=started;self.seconds=seconds
  self.out=Path(binding['planned_actual_output_root']);self.metadata_context=metadata_role_context(binding)
  production,factory=original_resource_modules(binding)
  self.joined=production.DiskResources(ROOT/'validation',binding['complete_joint_roots'],8*2**30,2*2**30)
  self.history=factory.DynamicHistoryResources(ART,factory.history_roots([str(self.out)],ART),8*2**30,96*2**30,production.ResourceFailure)
  initial=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure).check()
  require(initial['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'original fullfresh2/cold/meta/history96 reservation')
 def light(self):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  require(peak<512*2**20 and time.monotonic()-self.started<self.seconds,'unchanged SELF512/original start wall cap')
  require(own_bytes(self.out)<OUT_CAP,'whole archive output8MiB hard cap')
  require(own_bytes(BASE)<SOURCE_CAP,'entire own Source/metadata16MiB component')
  return peak
 def check(self):
  peak=self.light();h=self.history.check();f=self.joined.check();extra=0
  roots=self.binding['complete_joint_roots']
  for p in self.binding['explicit_cumulative_metadata_file_pins']:
   current_metadata(p,self.binding,self.metadata_context)
   if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
  for p in self.binding['retained_B2_current_epoch_readonly_pins']:
   current7(p);require(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'all nine cold readonly inputs covered by original history, not promoted into fresh metadata')
  for p in self.binding['retained_failed_v1_current7_only_pins']:current_failed_v1(p,self.binding)
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
