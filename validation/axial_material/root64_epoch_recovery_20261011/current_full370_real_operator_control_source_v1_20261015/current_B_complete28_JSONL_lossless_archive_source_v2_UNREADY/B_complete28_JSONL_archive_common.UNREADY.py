"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=264*2**20
ARCHIVE_CAP=256*2**20
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
  require(len(owners)==1 and own_bytes(owners[0])+len(raw)<OUT_CAP,'entire sole archive output264MiB before metadata write')
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

def current_failed_pool(p,binding):
 require(type(p)is dict and set(p)=={'path','size_bytes','identity'}and p in binding['retained_failed_pool_archive_current7_only_pins'],
  'only exact retained failed-pool7rows stat3, never partial SHA/fullPF or generic missing exception')
 q=Path(p['path']);st=q.lstat()
 require(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(st.st_mode)
  and st.st_uid==os.getuid()and st.st_nlink==1 and identity(st)==p['identity']and st.st_size==p['size_bytes'],
  'entire retained failed-pool metadata/runtime row current7 only')

def current_exact16_historical_absence(binding):
 targets=binding['exact16_retired_temporary_target_pins']
 require(type(targets)is list and len(targets)==16 and len({p['path']for p in targets})==16
  and all(set(p)=={'path','sha256','size_bytes','identity'}for p in targets[:15])
  and set(targets[-1])=={'path','size_bytes','identity'}and targets[-1]['size_bytes']==67099371,
  'exact15 completed fullPF temporaries and sole failed partialstat3 history, not generic absent path skip')
 for p in targets:
  require(not os.path.lexists(p['path'])and not any(x.is_symlink()for x in Path(p['path']).parents),
   'only precisely proved temporary16 absent, never current-stat/hash retired SQL/pool or partial')

def current_all_retained(binding):
 for p in binding['all28_plain_pins']+binding['retained_current7_pins']:current7(p)
 for p in binding['retained_failed_v1_current7_only_pins']:current_failed_v1(p,binding)
 for p in binding['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,binding)
 current_exact16_historical_absence(binding)
 current7(binding['retained_empty_numeric_mismatch_JSONL_pin'])

def admit(binding):
 require(binding['schema']=='CURRENT_B_COMPLETE28_JSONL_LOSSLESS_ARCHIVE_BINDING_V1'
  and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False
  and binding['Source_admission_ready']is False and binding['original_caps']==CAPS
  and type(binding['actual_current_resource_stage_budget'])is dict,
  'future completed-spool exact16 genuine execute0/post0 and latest full82plus264plusSource8 budget NULL hard reject')
 previouspin=binding['actual_completed_spool_exact16_plan_pin'];previous=metadata(previouspin)
 receipt=metadata(binding['actual_completed_spool_exact16_receipt_pin']);post=metadata(binding['actual_completed_spool_exact16_post_pin'])
 true0(binding['actual_completed_spool_exact16_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_completed_spool_exact16_receipt_pin'])
 true0(binding['actual_completed_spool_exact16_post_tools_pin'],'actual_review_return','review_pin',binding['actual_completed_spool_exact16_post_pin'])
 historical=binding['exact16_retired_temporary_target_pins']
 require(previous['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_PLAN_V1'
  and previous['Source_admission_ready']is True and previous['draft_unready']is False
  and previous['actual_completed_consumers_and_native_epoch_closed0']is True and previous['no_new_output_root']is True
  and previous['exact_target_pins']==historical and previous['target_total_bytes']==367026207
  and previous['bounded_own_Source_metadata_receipts_bytes']==8*2**20 and previous['original_caps']==CAPS,
  'independent new completed-derived temporary lifecycle, never failed archive success gate weakened')
 require(receipt['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_LIFECYCLE_RECEIPT_V1'
  and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_B_COMPLETED_SPOOL_EXACT16_DERIVED_TEMPORARIES_AND_FAILED_FRAGMENT'
  and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==historical
  and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==367026207
  and receipt['files_deleted']is True and receipt['resources_after_original_classes_forced_fresh']is True
  and receipt['temporary_completed_derived_spool_lifecycle_only']is True
  and receipt['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False
  and receipt['future_use_requires_new_full_native_extraction_and_independent_admission']is True
  and receipt['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False
  and receipt['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False
  and receipt['complete_pair_archive_success']is False and receipt['generic_missing_path_skip_authorized']is False,
  'genuine exact16 temporary lifecycle receipt0, native/results retained; old SQL/pool file byte identity not promised')
 contract=binding['actual_completed_spool_exact16_post_contract'];projection=metadata(binding['actual_completed_spool_exact16_post_Source_projection_pin'])
 require(projection['schema']==contract['schema']and projection['status']==contract['status'],'same frozen exact16 actualpost Source projection; its NULL future PF fields are never execution evidence')
 require(post['schema']==contract['schema']=='CURRENT_B_COMPLETED_DERIVED_SPOOL_EXACT16_EXECUTION_METADATA_POSTVERIFY_V1'
  and post['status']==contract['status']=='PASS_ACTUAL_B_COMPLETED_DERIVED_SPOOL_EXACT16_TEMPORARIES_RETIRED_NATIVE_AND_RESULTS_PRESERVED_METADATA_ONLY'
  and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_completed_spool_exact16_receipt_pin']
  and post['actual_Root_tools_pin']==binding['actual_completed_spool_exact16_Root_tools_pin']and post['plan_pin']==previouspin
  and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0
  and post['exact_target_pins']==post['actual_released_pins']==historical and post['actual_released_bytes']==367026207
  and post['files_deleted']is True and post['files_deleted_by_post']is False
  and post['resources_after_original_classes_forced_fresh']is True and post['exact_sixteen_targets_absent_verified_twice']is True
  and post['temporary_completed_derived_spool_lifecycle_only']is True
  and post['all_authoritative_native_and_completed_result_documents_preserved']is True
  and post['retired_spool_file_bytes_archived_or_byte_reconstructable_claimed']is False
  and post['complete_pair_archive_success']is False
  and post['future_use_requires_new_full_native_extraction_and_independent_admission']is True
  and post['new_SQL_or_pool_byte_identity_with_retired_file_claimed']is False
  and post['old_SQLgzip_with_newly_extracted_pool_automatically_compatible_claimed']is False,
  'genuine independent exact16 actual metadata post0, no readonly or failed post substituted for execution')
 current_exact16_historical_absence(binding)
 audit=metadata(previous['actual_completed_spool_role_audit_pin']);e=audit['actual_B_extract_closure'];g=audit['actual_B_aggregate_closure']
 ep=metadata(e['post']);gp=metadata(g['post'])
 true0(e['Root_tools'],'actual_terminal_return','report_pin',e['Root_report']);true0(e['post_tools'],'actual_review_return','review_pin',e['post'])
 true0(g['Root_tools'],'actual_terminal_return','report_pin',g['Root_report']);true0(g['post_tools'],'actual_review_return','review_pin',g['post'])
 require(ep['schema']==e['post_schema']and ep['status']==e['post_status']and ep['failure']is None
  and ep['actual_Host_report_pin']==e['Root_report']and ep['actual_Root_tools_pin']==e['Root_tools']
  and gp['schema']==g['post_schema']and gp['status']==g['post_status']and gp['failure']is None
  and gp['actual_Host_report_pin']==g['Root_report']and gp['actual_Root_tools_pin']==g['Root_tools'],
  'both original complete B extract and aggregate actual Root0/post0 whole-output PF inventories')
 # Presence is already archived/retired by its separate genuine historical exact1 closure, not a missing-path filter.
 pc=binding['inherited_presence_exact1_closure_pins'];pres=metadata(pc['receipt']);ppost=metadata(pc['post'])
 true0(pc['Root_tools'],'actual_terminal_return','receipt_pin',pc['receipt']);true0(pc['post_tools'],'actual_review_return','review_pin',pc['post'])
 presence=binding['historical_retired_presence_full_pin']
 require(pres['mode']=='execute'and pres['failure']is None and pres['actual_released_pins']==[presence]
  and pres['actual_released_bytes']==169615994 and pres['files_deleted']is True
  and ppost['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'
  and ppost['status']=='PASS_ACTUAL_CURRENT_BAGG_PRESENCE_EXACT1_RETIRED_COMPLETE_RESULT_BYTES_IN_ARCHIVE_METADATA_ONLY'
  and ppost['failure']is None and ppost['actual_execution_receipt_pin']==pc['receipt']and ppost['actual_Root_tools_pin']==pc['Root_tools']
  and type(ppost['actual_Root_integer_exit_code'])is int and ppost['actual_Root_integer_exit_code']==0
  and ppost['historical_retired_presence_full_pin']==presence and ppost['exact_one_target_absent_verified_twice']is True
  and not os.path.lexists(presence['path']),'known exact169615994 presence already retired with permanent archive; never a new target or generic missing role')
 rows=ep['actual_complete_output_full_EOF_twice_pins']+gp['all_new_output_blind_fullEOF_SHA_current7_twice_pins']
 JSONL=[p for p in rows if p['path'].endswith('.jsonl')]
 require(len(JSONL)==30 and presence in JSONL,'complete recorded inventories include25extract plus5aggregate JSONL with exact historical presence')
 live=[p for p in JSONL if p!=presence];ordered=[p for p in live if p['size_bytes']>0];empty=[p for p in live if p['size_bytes']==0]
 require(len(live)==29 and len(ordered)==28 and sum(p['size_bytes']for p in ordered)==249929878
  and len(empty)==1 and empty[0]['path'].endswith('/all_numeric_mismatches.jsonl')and empty[0]==binding['retained_empty_numeric_mismatch_JSONL_pin']
  and binding['all28_plain_pins']==ordered and binding['original_plain_total_bytes']==249929878
  and all(p in rows and p not in historical for p in live),
  'all28 real nonempty full result JSONL exact original postPF order, no subset, values or compression assumption; empty mismatch remains at original path')
 current_all_retained(binding)
 require(binding['retained_current7_pins']==[p for p in previous['retained_current7_pins']if p not in ordered]
  and binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']
  and binding['retained_failed_pool_archive_current7_only_pins']==previous['retained_failed_pool_archive_current7_only_pins']
  and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins'],
  'all rawnative/final55pair/55contexts/oldgzip-entry-index/docs/comparison detail/failed histories retained and not archived away')
 proofs=[binding[k]for k in('actual_completed_spool_exact16_plan_pin','actual_completed_spool_exact16_receipt_pin','actual_completed_spool_exact16_Root_tools_pin','actual_completed_spool_exact16_post_pin','actual_completed_spool_exact16_post_tools_pin','actual_completed_spool_exact16_post_Source_projection_pin')]+[previous['actual_completed_spool_role_audit_pin']]+[c[k]for c in(e,g)for k in('Root_report','Root_tools','post','post_tools')]+list(pc.values())
 require(binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']
  and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),
  'complete cumulative metadata table plus actual16/consumer/presence proofs, no lost external/cold accounting')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots']
 require(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']and len(prefix)==82
  and binding['complete_joint_roots']==prefix+[str(out)]and len(binding['complete_joint_roots'])==83 and out.parent==ART
  and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))
  and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),
  'entire real82 prefix including all failed roots plus exactly one new owning83 archive root')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP
  and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP
  and binding['compression_order']=='ORIGINAL_POST_INVENTORY_ORDER_ALL28_NONEMPTY_JSONL'
  and binding['plain_retirement_authorized']is False,'new component264MiB=256gzip+8runtime plusSource8; originals retained, separate future retirement only after independent post0')
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
  require(own_bytes(self.out)<OUT_CAP,'whole archive output264MiB hard cap')
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
  for p in self.binding['retained_failed_pool_archive_current7_only_pins']:current_failed_pool(p,self.binding)
  current_exact16_historical_absence(self.binding)
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
