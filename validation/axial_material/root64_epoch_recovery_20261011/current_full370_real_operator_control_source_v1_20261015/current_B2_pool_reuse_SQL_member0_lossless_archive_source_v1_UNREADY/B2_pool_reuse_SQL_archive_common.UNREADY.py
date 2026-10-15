"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=72*2**20
ARCHIVE_CAP=64*2**20
SOURCE_CAP=8*2**20
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
 if q.is_relative_to(BASE):require(own_bytes(BASE)+len(raw)<SOURCE_CAP,'entire Source8MiB before metadata write')
 else:
  owners=[a for a in q.parents if a.parent==ART]
  require(len(owners)==1 and own_bytes(owners[0])+len(raw)<OUT_CAP,'entire sole archive output72MiB before metadata write')
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

def current_retired_SQL_and_discarded_partial(binding):
 rows=binding['exact_historical_SQL_and_discarded_partial_target_pins']
 require(type(rows)is list and len(rows)==2 and rows[0]==binding['historical_SQL_full_pin']
  and rows[1]==binding['discarded_partial_pool_current7_only_pin']and set(rows[1])=={'path','size_bytes','identity'},
  'exact historical SQL fullPF and discarded incomplete pool gzip stat3, never generalized missing skip')
 for p in rows:
  require(not os.path.lexists(p['path'])and not any(q.is_symlink()for q in Path(p['path']).parents),
   'only proved retired SQL and discarded exact incomplete pool gzip absent; never current-stat historical deleted targets')

def current_all_retained(binding):
 for p in binding['all1_plain_pins']+binding['retained_current7_pins']:current7(p)
 for p in binding['retained_failed_v1_current7_only_pins']:current_failed_v1(p,binding)
 current_retired_SQL_and_discarded_partial(binding)
 current7(binding['reused_SQL_member0_gzip_pin']);current7(binding['reused_SQL_member0_entry_pin'])

def admit(binding):
 require(binding['schema']=='CURRENT_B2_POOL_REUSE_SQL_MEMBER0_LOSSLESS_ARCHIVE_BINDING_V1'
  and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False
  and binding['Source_admission_ready']is False and binding['original_caps']==CAPS
  and type(binding['actual_current_resource_stage_budget'])is dict,
  'future exact SQL-plus-partial Root0/post0 and complete81 latest72plus16 budget NULL hard reject')
 previouspin=binding['actual_SQL_partial_recovery_plan_pin'];previous=metadata(previouspin)
 receipt=metadata(binding['actual_SQL_partial_recovery_receipt_pin']);post=metadata(binding['actual_SQL_partial_recovery_post_pin'])
 true0(binding['actual_SQL_partial_recovery_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_SQL_partial_recovery_receipt_pin'])
 true0(binding['actual_SQL_partial_recovery_post_tools_pin'],'actual_review_return','review_pin',binding['actual_SQL_partial_recovery_post_pin'])
 sql=binding['historical_SQL_full_pin'];partial=binding['discarded_partial_pool_current7_only_pin'];targets=[sql,partial]
 require(previous['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_PLAN_V1'
  and previous['Source_admission_ready']is True and previous['draft_unready']is False and previous['no_new_output_root']is True
  and previous['original_caps']==CAPS and previous['exact_target_pins']==targets
  and previous['exact_original_SQL_full_pin']==sql and previous['exact_partial_pool_current7_only_pin']==partial
  and previous['target_role_kinds']==['RESTORABLE_SQL_FULLPF','INCOMPLETE_POOL_GZIP_CURRENT7_ONLY']
  and sql['size_bytes']==52441088 and set(partial)=={'path','size_bytes','identity'}and partial['size_bytes']==17639368,
  'only exact recovered SQL fullPF plus incomplete pool-gzip3 targets, never complete original pool retirement or wholepair success')
 require(receipt['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ORIGINAL_RETIREMENT_RECEIPT_V1'
  and receipt['mode']=='execute'and receipt['status']=='RECOVERED_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED'
  and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==targets
  and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==70080456 and receipt['files_deleted']is True
  and receipt['resources_after_original_classes_forced_fresh']is True and receipt['whole_pair_archive_complete']is False
  and receipt['partial_target_body_opened_or_hashed']is False and receipt['generic_missing_path_skip_authorized']is False,
  'genuine new exact2 recovery Root0, original pair Root1/child1 failure remains failure')
 contract=binding['actual_SQL_partial_recovery_post_contract']
 require(post['schema']==contract['schema']=='CURRENT_B2_SQL_PARTIAL_EXACT2_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'
  and post['status']==contract['status']=='PASS_ACTUAL_CURRENT_B2_SQL_PARTIAL_EXACT2_SQL_ARCHIVED_PARTIAL_DISCARDED_METADATA_ONLY'
  and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_SQL_partial_recovery_receipt_pin']
  and post['actual_Root_tools_pin']==binding['actual_SQL_partial_recovery_Root_tools_pin']and post['plan_pin']==previouspin
  and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0
  and post['exact_target_pins']==post['actual_released_pins']==targets and type(post['actual_released_bytes'])is int and post['actual_released_bytes']==70080456
  and post['files_deleted']is True and post['files_deleted_by_post']is False and post['exact_two_targets_absent_verified_twice']is True
  and post['resources_after_original_classes_forced_fresh']is True and post['partial_target_body_opened_or_hashed']is False
  and post['whole_pair_archive_complete']is False and post['all_complete_results_preserved']is True
  and post['historical_deleted_target_PFs_not_claimed_current']is True and post['future_consumer_must_restore_SQL_with_exact_original_pool']is True
  and post['generic_missing_path_skip_authorized']is False,'genuine independent exact2 recovery metadata post0; no prior pair-success gate bypass')
 originalpin=previous['original_pair_execution_binding_pin'];original=metadata(originalpin)
 pool=original['all2_plain_pins'][1];gzip=binding['reused_SQL_member0_gzip_pin'];ep=binding['reused_SQL_member0_entry_pin'];entry=metadata(ep)
 require(original['all2_plain_pins']==[sql,pool]and pool['size_bytes']==150267572
  and binding['all1_plain_pins']==[pool]and binding['all2_original_pair_pins']==[sql,pool]
  and binding['original_plain_total_bytes']==150267572 and binding['original_pair_total_bytes']==202708660
  and binding['compression_order']=='ONLY_LIVE_ORIGINAL_POOL_REUSE_COMPLETE_SQL_MEMBER0_IN_PLACE',
  'only pool150267572 compressed; original SQL is historical and its complete gzip reused at original path without copy or link')
 mp=previous['actual_SQL_member0_control_closure_pins'];member=metadata(mp['Root_report']);memberpost=metadata(mp['post'])
 true0(mp['Root_tools'],'actual_terminal_return','report_pin',mp['Root_report']);true0(mp['post_tools'],'actual_review_return','review_pin',mp['post'])
 require(member['schema']=='ROOT_CURRENT_B2_SQL_MEMBER0_INDEPENDENT_RESTORATION_BYTE_CONTROL_REPORT_V1'
  and member['status']=='PASS_CURRENT_B2_SQL_MEMBER0_COMPLETE_GZIP_RESTORABLE_ORIGINAL_BYTES_ONLY'and member['failure']is None
  and member['original_member0_saved_full_pin']==sql and member['complete_member0_gzip_pin']==gzip and member['retained_member0_entry_pin']==ep
  and member['streamed_complete_member0_verified']is True and member['streamed_decompressed_SHA']==sql['sha256']and member['streamed_decompressed_length']==52441088
  and member['paired_SQL_pool_archive_complete']is False and member['original_member0_body_opened']is False
  and memberpost['actual_member0_Root_report_pin']==mp['Root_report']and memberpost['actual_Root_tools_pin']==mp['Root_tools']
  and memberpost['failure']is None and memberpost['Root_actual_complete_member0_stream_verified']is True
  and memberpost['original_member0_saved_full_pin']==sql and memberpost['complete_member0_gzip_pin']==gzip,
  'independent SQL member0 Root-only byteproof0 plus separate metadata post0 before exact recovery')
 mapping=previous['SQL_with_exact_live_original_pool_recovery_map']
 require(receipt['SQL_with_exact_live_original_pool_recovery_map']==post['SQL_with_exact_live_original_pool_recovery_map']==binding['SQL_with_exact_live_original_pool_recovery_map']==mapping
  and mapping==dict(historical_SQL_full_pin=sql,complete_SQL_gzip_full_pin=gzip,SQL_member0_entry_pin=ep,exact_live_original_pool_full_pin=pool,
   SQL_member0_Root_control_pin=mp['Root_report'],SQL_member0_independent_post_pin=mp['post'],restore_SQL_and_use_exact_original_pool_together=True,
   whole_pair_archive_complete=False,generic_missing_path_skip_authorized=False)
  and previous['retained_SQL_member0_gzip_pin']==post['retained_SQL_member0_gzip_pin']==gzip
  and previous['retained_SQL_member0_entry_pin']==post['retained_SQL_member0_entry_pin']==ep,
  'exact historical SQL-to-live-original-pool restoration mapping retained, never inferred pair success')
 require(entry['ordinal']==0 and entry['actual_B2_output_role']=='PAIRED_SQLITE_INDEX'and entry['original_plain_full_pin']==sql
  and entry['compressed_archive_full_pin']==gzip and entry['compression_input_SHA']==entry['streamed_decompressed_SHA']==sql['sha256']
  and entry['compression_input_length']==entry['streamed_decompressed_length']==52441088 and entry['exact_original_plain_bytes_recoverable']is True
  and entry['original_plain_preserved']is True,'old SQL entry preserved whole; true original_plain_preserved means archive-creation history only')
 expected=unique(previous['retained_current7_pins']+previous['retained_archive_metadata_current7_pins']+[gzip,ep])
 require(pool in expected and binding['retained_current7_pins']==[p for p in expected if p!=pool]
  and binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']
  and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins']
  and not{p['path']for p in targets}&{p['path']for p in expected},'all complete results/native/comparison/physical permanent mapping/failed8/cold9 retained; missing exception exact SQL and discarded partial only')
 proofs=[binding[k]for k in('actual_SQL_partial_recovery_plan_pin','actual_SQL_partial_recovery_receipt_pin','actual_SQL_partial_recovery_Root_tools_pin','actual_SQL_partial_recovery_post_pin','actual_SQL_partial_recovery_post_tools_pin')]+[originalpin]+list(previous['actual_pair_failure_closure_pins'].values())+list(mp.values())+[ep]
 require(binding['latest_complete_plan_pin']==previouspin and binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']
  and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),
  'complete existing explicit metadata table plus exact recovery failure/member0 closures, no lost old Host or external bytes')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots']
 require(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']and len(prefix)==81
  and binding['complete_joint_roots']==prefix+[str(out)]and len(binding['complete_joint_roots'])==82 and out.parent==ART
  and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))
  and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),
  'entire real existing81 including all failed roots plus only one fresh pool owning82 root')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP
  and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP
  and binding['SQL_recompressed_copied_or_hardlinked']is False and binding['future_consumer_must_restore_exact_SQL_pool_pair_together']is True,
  'candidate whole72MiB=64newpoolgzip+8runtime metadata plus Source8 must fit actual fullscope2GiB; no compression or future budget assumption')
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
  require(own_bytes(self.out)<OUT_CAP,'whole archive output72MiB hard cap')
  require(own_bytes(BASE)<SOURCE_CAP,'entire own Source/metadata8MiB component')
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
  current_retired_SQL_and_discarded_partial(self.binding)
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
