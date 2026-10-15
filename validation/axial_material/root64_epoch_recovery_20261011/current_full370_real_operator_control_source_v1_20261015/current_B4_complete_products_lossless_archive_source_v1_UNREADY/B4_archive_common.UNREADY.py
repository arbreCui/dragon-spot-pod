"""Draft byte-preserving archive support. Source only; no admission is minted here."""
import hashlib, importlib.util, json, os, resource, stat, sys, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
BASE=Path(__file__).absolute().parent
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,
 history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,
 free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
OUT_CAP=64*2**20
ARCHIVE_CAP=56*2**20
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
  require(len(owners)==1 and own_bytes(owners[0])+len(raw)<OUT_CAP,'entire sole archive output64MiB before metadata write')
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
 require(binding['schema']=='CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_BINDING_V1'and binding['prerequisite_binding_complete']is True and binding['draft_unready']is False and binding['Source_admission_ready']is False and binding['original_caps']==CAPS,'new B4 binding; future NULL B55/current-prefix roles remain UNREADY')
 capture=metadata(binding['actual_B_capture_Host_report_pin']);manifest=metadata(binding['actual_B_manifest_pin']);input_binding=metadata(binding['actual_B_input_binding_pin'])
 true0(binding['actual_B_capture_Root_tools_pin'],'actual_terminal_return','report_pin',binding['actual_B_capture_Host_report_pin']);true0(binding['actual_B_capture_post_tools_pin'],'actual_review_return','review_pin',binding['actual_B_capture_post_pin'])
 cp=metadata(binding['actual_B_capture_post_pin']);state=capture['actual_B_state']
 require(capture['schema']=='ACTUAL_CURRENT_B_COMPLETE_NATIVE_CAPTURE_ROOT_REPORT_V1'and capture['status']=='ACTUAL_CURRENT_B_FULL55_CONTEXT_8TREE_4PRODUCT_CAPTURE_CLOSED0_ONLY'and capture['failure']is None and capture['final_report_resource_check_passed']is True and capture['original_caps']==CAPS,'actual full B capture closed0, not warm A/B reuse')
 require(cp['schema']=='RECORDED_CURRENT_B_COMPLETE_CAPTURE_METADATA_POSTVERIFY_V1'and cp['status']=='PASS_ACTUAL_CURRENT_B_FULL4PRODUCT_55CONTEXT_8TREE_CAPTURE_CHILD0_METADATA_ONLY'and cp['failure']is None and cp['actual_Host_report_pin']==binding['actual_B_capture_Host_report_pin']and cp['actual_Root_tools_pin']==binding['actual_B_capture_Root_tools_pin'],'same real independent capture metadata post0')
 require(manifest['state_order']==['B']and manifest['states']['B']['actual_owning_report_pin']==binding['actual_B_capture_Host_report_pin']and manifest['current_B_case_input_binding_pin']==binding['actual_B_input_binding_pin']and len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8,'complete current B capture/manifest; no product omission')
 products=state['actual_material_product_pins']
 require(binding['all4_product_pins']==products and len(products)==len({p['path']for p in products})==4 and{Path(p['path']).name for p in products}=={'m.xsm','u.asc','a.asc','t.asc'}and all(Path(p['path']).parent==Path(input_binding['actual_output_root'])for p in products),'exact four complete actual B products in producer order, including complete original m.xsm bytes; no JSONL or ASCII-only relabelling')
 require(binding['original4_product_total_bytes']==sum(p['size_bytes']for p in products),'original byte total derived from exact current B fullPFs')
 extract=metadata(binding['actual_B_extraction_Host_report_pin']);ep=metadata(binding['actual_B_extraction_post_pin']);er=metadata(binding['actual_B_extraction_child_report_pin'])
 true0(binding['actual_B_extraction_Root_tools_pin'],'actual_terminal_return','report_pin',binding['actual_B_extraction_Host_report_pin']);true0(binding['actual_B_extraction_post_tools_pin'],'actual_review_return','review_pin',binding['actual_B_extraction_post_pin'])
 require(extract['status']=='ACTUAL_CURRENT_B_COMPLETE_EXTRACT_EVIDENCE_CHILD2_CLOSED_ONLY'and extract['failure']is None and extract['actual_child_integer_exit_code']==2 and type(extract['actual_child_integer_exit_code'])is int and extract['records'][0]['status']=='FAILED'and extract['records'][0]['error']=='own-child stage failed; no retry'and extract['actual_child_report_pin']==binding['actual_B_extraction_child_report_pin'],'actual complete B extraction Root0/original child2 and FAILED preserved')
 require(ep['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and ep['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and ep['failure']is None and ep['actual_extraction_report_pin']==binding['actual_B_extraction_child_report_pin']and ep['actual_extraction_host_pin']==binding['actual_B_extraction_Host_report_pin']and ep['current_B_case_input_binding_pin']==binding['actual_B_input_binding_pin']and er['state_order']==['B']and len(er['states']['B'])==8 and len(er['context_states']['B'])==55,'actual independent full B extraction metadata proof')
 require(binding['actual_B55_control_and_post_role_keys_audited']is True,'execution order requires real B55 control/post0 before archive; no future successful control assumed')
 control=metadata(binding['actual_B55_control_Host_report_pin']);post=metadata(binding['actual_B55_control_post_pin'])
 true0(binding['actual_B55_control_Root_tools_pin'],'actual_terminal_return','report_pin',binding['actual_B55_control_Host_report_pin']);true0(binding['actual_B55_control_post_tools_pin'],'actual_review_return','review_pin',binding['actual_B55_control_post_pin'])
 require(control['schema']=='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1'and control['status']=='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'and control['failure']is None and control['final_report_resource_check_passed']is True and control['original_caps']==CAPS and control['actual_B_manifest_pin']==binding['actual_B_manifest_pin']and control['actual_B_extraction_report_pin']==binding['actual_B_extraction_child_report_pin'],'actual fresh B55 native/integer control closed0, never prior A runtime evidence')
 require(len(control['records'])==len(control['actual_watchdog_checks'])==3 and all(r['status']=='PASS'for r in control['records'])and all(type(w['actual_watchdog']['returncode'])is int and w['actual_watchdog']['returncode']==0 and w['actual_watchdog']['limit_failure']is None for w in control['actual_watchdog_checks']),'all three original guarded current B55 native stages child0')
 results=control['actual_control_results'];require(results['all_constant64_and_overv370x8_current_words_match']is True and type(results['actual_native_vs_integer_model_and_saved_word_mismatches'])is int and results['actual_native_vs_integer_model_and_saved_word_mismatches']==0 and results['actual_current_overv_words_compared']==2960,'actual B55 all native/integer/saved words matched; no archive numerical replay')
 roles=binding['actual_B55_control_post_role_projection'];require(post['schema']==roles['schema']and post['status']==roles['status']and post['failure']is None and post[roles['actual_Host_report_pin_field']]==binding['actual_B55_control_Host_report_pin']and post[roles['actual_Root_tools_pin_field']]==binding['actual_B55_control_Root_tools_pin']and type(post[roles['actual_Root_integer_exit_code_field']])is int and post[roles['actual_Root_integer_exit_code_field']]==0,'exact actual audited B55 post role projection')
 retained=state['complete_context_pins']+[r['input_pin']for r in state['complete_state_snapshot_inputs']]+[p for row in er['states']['B']for p in(row['paired_SQLite_pin'],row['paired_original_pool_pin'])]
 require(binding['retained_native_current7_pins']==retained and len(retained)==79 and not{p['path']for p in products}&{p['path']for p in retained},'all55contexts/eight XSM/sixteen saved SQL-pool files retained separately from the four archive products')
 latest=metadata(binding['latest_complete_plan_pin']);out=Path(binding['planned_actual_output_root']);prefix=binding['inherited_latest_complete_joint_roots'];capture_prefix=input_binding['complete_latest_prefix_roots']+[input_binding['actual_output_root']]
 require(latest['complete_joint_roots']==prefix and prefix[:len(capture_prefix)]==capture_prefix and binding['complete_joint_roots']==prefix+[str(out)]and out.parent==ART and len(binding['complete_joint_roots'])==len(set(binding['complete_joint_roots']))and not any(Path(a).is_relative_to(Path(b))for a in binding['complete_joint_roots']for b in binding['complete_joint_roots']if a!=b),'entire dynamic then-latest prefix including failed stages plus one counted B4 archive root')
 require(binding['bounded_total_output_bytes']==OUT_CAP and binding['bounded_archive_payload_bytes']==ARCHIVE_CAP and binding['bounded_Source_metadata_bytes']==SOURCE_CAP,'64MiB total/56MiB gzip payload/8MiB runtime-metadata headroom/16MiB Source')
 for p in products+retained+binding['original_B_native_and_readonly_input_current7_pins']:current7(p)
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
  require(own_bytes(self.out)<OUT_CAP,'whole archive output64MiB hard cap')
  require(own_bytes(BASE)<SOURCE_CAP,'entire own Source/metadata16MiB component')
  return peak
 def check(self):
  peak=self.light();h=self.history.check();f=self.joined.check();extra=0
  roots=self.binding['complete_joint_roots']
  for p in self.binding['explicit_cumulative_metadata_file_pins']:
   current_metadata(p,self.binding,self.metadata_context)
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
