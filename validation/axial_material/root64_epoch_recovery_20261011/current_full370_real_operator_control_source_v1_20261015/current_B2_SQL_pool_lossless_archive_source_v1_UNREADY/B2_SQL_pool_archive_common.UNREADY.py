"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=32*2**20
ARCHIVE_CAP=24*2**20
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
  require(len(owners)==1 and own_bytes(owners[0])+len(raw)<OUT_CAP,'entire sole archive output32MiB before metadata write')
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
 for p in binding['all2_plain_pins']+binding['retained_current7_pins']:current7(p)
 for p in binding['retained_failed_v1_current7_only_pins']:current_failed_v1(p,binding)
def admit(binding):
 require(binding['schema']=='CURRENT_B2_PAIRED_SQL_POOL_LOSSLESS_ARCHIVE_BINDING_V1'and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False and binding['Source_admission_ready']is False and binding['original_caps']==CAPS and type(binding['actual_current_resource_stage_budget'])is dict,'NULL physical exact1 Root0/post0/latest budget never admits SQL-pool archive or GEN')
 previouspin=binding['actual_physical_directory_retirement_plan_pin'];previous=metadata(previouspin)
 receipt=metadata(binding['actual_physical_directory_retirement_receipt_pin']);post=metadata(binding['actual_physical_directory_retirement_post_pin'])
 true0(binding['actual_physical_directory_retirement_Root_tools_pin'],'actual_terminal_return','receipt_pin',binding['actual_physical_directory_retirement_receipt_pin'])
 true0(binding['actual_physical_directory_retirement_post_tools_pin'],'actual_review_return','review_pin',binding['actual_physical_directory_retirement_post_pin'])
 historical=binding['historical_retired_physical_directory_full_pin']
 require(previous['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and previous['Source_admission_ready']is True and previous['draft_unready']is False and previous['no_new_output_root']is True and previous['original_caps']==CAPS and previous['exact_target_pins']==[historical]and historical['size_bytes']==34371817 and historical['sha256']=='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60','only exact physical JSONL historical PF retired; no generic missing role skip')
 require(receipt['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['plan_pin']==previouspin and receipt['exact_target_pins']==receipt['actual_released_pins']==[historical]and type(receipt['actual_released_bytes'])is int and receipt['actual_released_bytes']==34371817 and receipt['files_deleted']is True and receipt['resources_after_original_classes_forced_fresh']is True and receipt['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and receipt['generic_missing_path_skip_authorized']is False,'genuine exact1 physical retirementRoot0 with forced fresh resources and permanent byte mapping')
 require(post['schema']=='CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_ACTUAL_EXECUTION_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B2_PHYSICAL_DIRECTORY_EXACT1_RETIRED_COMPLETE_RESULT_BYTES_IN_ARCHIVE_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_execution_receipt_pin']==binding['actual_physical_directory_retirement_receipt_pin']and post['actual_Root_tools_pin']==binding['actual_physical_directory_retirement_Root_tools_pin']and post['plan_pin']==previouspin and post['source_pin']==receipt['source_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and post['exact_target_pins']==post['actual_released_pins']==[historical]and type(post['actual_released_bytes'])is int and post['actual_released_bytes']==34371817 and post['files_deleted']is True and post['files_deleted_by_post']is False and post['historical_retired_physical_directory_full_pin']==historical and post['historical_deleted_fullPF_not_claimed_current']is True and post['exact_one_target_absent_verified_twice']is True and post['future_consumer_must_use_exact_single_B2_physical_directory_archive_mapping']is True and post['generic_missing_path_skip_authorized']is False,'genuine independent exact1 metadata post0 for the same Source/plan/receipt, not archive or readonly success substituted')
 require(not os.path.lexists(historical['path'])and not any(q.is_symlink()for q in Path(historical['path']).parents),'only proved retired physical original absent, never current-stat/hash it or skip other missing files')
 archivepin=previous['inherited_complete_archive_plan_pin'];archive=metadata(archivepin);cp=previous['actual_archive_closure_pins'];apost=metadata(cp['post']);index=metadata(cp['index'])
 true0(cp['Root_tools'],'actual_terminal_return','report_pin',cp['Host']);true0(cp['post_tools'],'actual_review_return','review_pin',cp['post'])
 projection=previous['actual_archive_post_key_projection'];gzip=previous['retained_physical_directory_gzip_pins'];entries=previous['retained_physical_directory_entry_pins']
 require(len(gzip)==len(entries)==len(index['entries'])==1 and archive['actual_physical_directory_original_pin']==historical and archive['all1_plain_pins']==[historical]and apost['schema']==projection['schema']and apost['status']==projection['status']and apost['failure']is None and apost[projection['original_full_pin_field']]==historical and apost[projection['compressed_archive_full_pin_field']]==gzip[0]and apost[projection['entry_pin_field']]==entries[0]and apost['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True and post['retained_physical_directory_gzip_pins']==gzip and post['retained_physical_directory_entry_pins']==entries and post['original_lookup_index_pin']==cp['index'],'retired physical original permanently recoverable via same complete gzip/entry/index, creation history preserved')
 row=index['entries'][0];entry=metadata(entries[0]);require(row['entry_pin']==entries[0]and entry=={k:v for k,v in row.items()if k!='entry_pin'}and row['original_plain_full_pin']==historical and row['compressed_archive_full_pin']==gzip[0]and row['compression_input_SHA']==row['streamed_decompressed_SHA']==historical['sha256']and row['compression_input_length']==row['streamed_decompressed_length']==34371817 and row['original_plain_preserved']is True,'exact physical entry creation-time preservation remains history, not a current original claim')
 compareplan=metadata(archive['latest_complete_plan_pin']);pair=compareplan['native_B2_pair'];ordered=[pair['sqlite_pin'],pair['native_pool_pin']]
 require(binding['all2_plain_pins']==ordered and binding['actual_B2_SQL_pool_original_pair']==dict(sqlite_pin=ordered[0],native_pool_pin=ordered[1])and [p['size_bytes']for p in ordered]==[52441088,150267572]and binding['original_plain_total_bytes']==202708660 and binding['compression_order']=='SQL_THEN_ORIGINAL_POOL','only complete actual paired SQL index then original pool; no numerical parsing or repeat native decoding')
 expected=unique(previous['retained_current7_pins']+previous['retained_archive_metadata_current7_pins']+gzip+entries+[cp['index']]+previous['retained_B2_current_epoch_readonly_pins'])
 require(all(p in expected for p in ordered)and binding['retained_current7_pins']==[p for p in expected if p not in ordered]and historical['path']not in{p['path']for p in expected}and binding['retained_physical_directory_gzip_pins']==gzip and binding['retained_physical_directory_entry_pins']==entries and binding['retained_physical_directory_index_pin']==cp['index'],'all other native/B4/current comparison detail/docs/physical archive bytes retained; only SQL/pool targets separated')
 require(binding['retained_failed_v1_current7_only_pins']==previous['retained_failed_v1_current7_only_pins']==post['retained_failed_v1_current7_only_pins']and post['prior_v1_Root1_child_minus15_unknown_counts_equality_preserved']is True and post['prior_v1_partial_payload_body_not_opened_or_hashed_by_post']is True and binding['retained_B2_current_epoch_readonly_pins']==previous['retained_B2_current_epoch_readonly_pins'],'all eight failed-v1 files current7-only and cold9 roles preserved without fullPF/SHA invention')
 proofs=[binding[k]for k in('actual_physical_directory_retirement_plan_pin','actual_physical_directory_retirement_receipt_pin','actual_physical_directory_retirement_Root_tools_pin','actual_physical_directory_retirement_post_pin','actual_physical_directory_retirement_post_tools_pin')]+[archivepin]+list(cp.values())
 require(binding['latest_complete_plan_pin']==previouspin and binding['base_explicit_cumulative_metadata_file_pins']==previous['explicit_cumulative_metadata_file_pins']and binding['explicit_cumulative_metadata_file_pins']==unique(previous['explicit_cumulative_metadata_file_pins']+proofs),'complete inherited80 metadata union plus exact retirement actual proofs, no dropped external roles or large cold payload in metadata')
 out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots'];require(prefix==previous['complete_joint_roots']==receipt['complete_joint_roots']==post['complete_joint_roots']==archive['complete_joint_roots']and len(prefix)==80 and binding['complete_joint_roots']==prefix+[str(out)]and out.parent==ART and len(binding['complete_joint_roots'])==81 and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),'entire inherited80 plus exactly one owning paired archive81 root, no scope reset')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP and binding['metadata_runtime_headroom_bytes']==8*2**20 and binding['bounded_Source_metadata_bytes']==SOURCE_CAP and binding['future_consumer_must_restore_exact_SQL_pool_pair_together']is True,'whole32MiB=24gzip+8runtime metadata plus Source16; failures retained without retry or assumed compression')
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
  require(own_bytes(self.out)<OUT_CAP,'whole archive output32MiB hard cap')
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
