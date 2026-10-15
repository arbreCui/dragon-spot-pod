"""UNREADY complete B55 versus B2 typed comparison owning contract. Metadata admission only on import."""
import hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');ART=R/'validation/artifacts';BASE=Path(__file__).absolute().parent
OUT=ART/'axial-material-current-B55-nativeWarmB2-complete-typed-macro-compare-20261015-v1'
OUTPUT_BOUND=32*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(actual_lineage_qualified=False,original_RAM_bits_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,online_BOOT_qualified=False,reaction_multiplicity_qualified=False,scientific_accuracy_qualified=False)
def need(v,m):
 if v is not True:raise RuntimeError(m)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and not any(x.is_symlink()for x in(q,*q.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes'],'exact ordinary Source/control/input current7');return q
def pin(q):
 q=Path(q);s=q.lstat();h=hashlib.sha256()
 with q.open('rb')as f:
  need(identity(os.fstat(f.fileno()))==identity(s),'opened Source/control current7')
  while True:
   b=f.read(2**20)
   if not b:break
   h.update(b)
  need(identity(os.fstat(f.fileno()))==identity(s),'EOF Source/control current7')
 p=dict(path=str(q),sha256=h.hexdigest(),size_bytes=s.st_size,identity=identity(s));current(p);return p
def metadata(p):
 q=current(p);need(p['size_bytes']<8*2**20,'bounded metadata8MiB');raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'metadata complete SHA');v=json.loads(raw);current(p);return v
def source(p,name):
 need(pin(p['path'])==p,'whole frozen Source fullPF');spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def unique(rows):
 t={}
 for p in rows:
  if p['path']in t:need(t[p['path']]==p,'same path one fullPF')
  t[p['path']]=p
 return list(t.values())
def write(q,v):
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<6*2**20,'metadata report6MiB')
 if Path(q).is_relative_to(BASE):need(sum(x.stat().st_size for x in BASE.rglob('*')if x.is_file())+len(raw)<SOURCE_BOUND,'whole Source/metadata16MiB including new output')
 with Path(q).open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def genuine(v,key,p,outkey):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'genuine closed typed0')
 need(json.loads(t['output'].strip().splitlines()[-1])[outkey]==p,'genuine return exact artifact PF')
def read_with_budget(p,budget):
 budget();v=metadata(p);budget();return v

def own_bytes(root):
 total=0
 if Path(root).exists():
  for q in Path(root).rglob('*'):
   s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'no owning output/Source alias')
   if stat.S_ISREG(s.st_mode):total+=s.st_size
 return total

def admit(packet,child=False):
 need(packet['schema']in('CURRENT_B55_B2_COMPLETE_COMPARISON_ADMISSION_PACKET_V1','CURRENT_B55_B2_COMPLETE_COMPARISON_SOURCE_ONLY_PLAN_V1')and packet['actual_business_preconditions_closed']is True and packet['source_role_pin_audit_complete']is True and packet['original_caps']==CAPS,'NULL extractionRoot/post/pair/latestbudget never admits comparison or GEN')
 need(packet['Source_only_stat_budget_fits']is True and packet['Root_original_classes_recheck_required']is True and packet['only_current_stage']=='complete_B55_B2_compare'and packet['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['B2_archive_not_redecoded']is True,'only full typed19620/all-original-word comparison32+Source16; no decode or reduced output reservation')
 extractplan=metadata(packet['actual_latest_complete_prefix_plan_pin']);old=source(packet['frozen_B2_extraction_contract_Source_pin'],'comparison_prior_B2_exact_lifecycle_admission')
 build,bm,archive,retirement,bridge=old.admit(extractplan,True)
 host=metadata(packet['actual_B2_extraction_Host_report_pin']);raw=metadata(packet['actual_B2_extraction_Root_tools_pin']);extraction=metadata(packet['actual_B2_complete_extraction_report_pin']);post=metadata(packet['actual_B2_complete_extraction_post_pin']);tools=metadata(packet['actual_B2_complete_extraction_post_tools_pin'])
 genuine(raw,'actual_terminal_return',packet['actual_B2_extraction_Host_report_pin'],'report_pin');genuine(tools,'actual_review_return',packet['actual_B2_complete_extraction_post_pin'],'review_pin')
 need(host['schema']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_GUARDED_ROOT_REPORT_V1'and host['status']=='ACTUAL_CURRENT_NATIVEWARM_B2_COMPLETE_EXTRACTION_EVIDENCE_CHILD2_CLOSED_ONLY'and host['failure']is None and host['complete_physical_tree_extraction_completed']is True and host['final_report_resource_check_passed']is True and type(host['actual_child_integer_exit_code'])is int and host['actual_child_integer_exit_code']==2 and host['actual_child_report_pin']==packet['actual_B2_complete_extraction_report_pin']and host['control_plan_pin']==packet['actual_latest_complete_prefix_plan_pin']and len(host['records'])==1 and host['records'][0]['status']=='FAILED'and host['records'][0]['error']==host['original_runner_error']=='own-child stage failed; no retry','genuine complete B2 extractRoot0 with original evidencechild2/FAILED/error preserved')
 need(post['schema']=='RECORDED_CURRENT_NATIVEWARM_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B2_COMPLETE_PHYSICAL_TREE_EXTRACTION_ROOT0_CHILD2_METADATA_ONLY'and post['failure']is None and post['metadata_only']is True and post['actual_Host_report_pin']==packet['actual_B2_extraction_Host_report_pin']and post['actual_Root_tools_pin']==packet['actual_B2_extraction_Root_tools_pin']and post['actual_child_report_pin']==packet['actual_B2_complete_extraction_report_pin']and type(post['actual_Root_integer_exit_code'])is int and post['actual_Root_integer_exit_code']==0 and type(post['actual_child_integer_exit_code'])is int and post['actual_child_integer_exit_code']==2,'same genuine independent complete B2 extraction metadata post0')
 need(extraction['schema']=='ACTUAL_COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_EXTRACTION_V1'and extraction['status']=='COMPLETE_NATIVEWARM_B2_PHYSICAL_TREE_READONLY_EVIDENCE_ONLY'and extraction['entire_original_physical_tree_walked']is True and extraction['all_original_types_counts_words_and_physical_API_orders_saved']is True and extraction['unrelated_original_containers_retained']is True and extraction['complete_MICROLIB2_list1_MACROLIB_records']==19620,'complete physical archive, not reconstructed19249 subset or macro-only re-decoding')
 need(post['control_plan_pin']==packet['actual_latest_complete_prefix_plan_pin']and post['complete_joint_roots']==extractplan['complete_joint_roots']and post['original_caps']==CAPS and post['complete_physical_tree_extraction_completed']is True and post['actual_full_physical_tree_counts']=={k:extraction[k]for k in('complete_physical_tree_records','complete_directories','complete_extents','complete_MICROLIB2_list1_MACROLIB_records')}and post['all_original_typed_metadata_original_words_and_physical_API_orders_saved']is True and post['unrelated_original_containers_preserved']is True and post['not_limited_to_constructed19249_fields']is True and post['new_output_blind_fullEOF_SHA_verified_twice']is True and post['original_FAILED_error_and_expected_child2_preserved']is True and post['comparison_stage_not_executed']is True,'actual independent full physical tree/counts/all3 byte-proof scope, no offline construction substituted')
 need(packet['actual_B2_lineage_metadata_audit_pin']==extractplan['actual_B2_lineage_metadata_audit_pin'],'same explicit known/unknown physical-input lineage audit; no qualification manufactured')
 pair=packet['native_B2_pair'];expected=dict(archive_pin=extractplan['actual_current_epoch_B2_archive_pin'],sqlite_pin=extraction['paired_SQLite_pin'],native_pool_pin=extraction['paired_original_pool_pin'])
 need(pair==expected and packet['actual_current_epoch_B2_archive_pin']==expected['archive_pin']==extraction['actual_current_epoch_B2_archive_pin']and post['paired_SQLite_pin']==expected['sqlite_pin']and post['paired_original_pool_pin']==expected['native_pool_pin']and post['complete_physical_directory_slots_pin']==extraction['complete_physical_directory_slots_pin'],'exact independently extracted full B2 SQL/pool/physical index, old savedAAA pair cannot substitute')
 observed=metadata(packet['actual_B_complete_context_snapshot_extraction_post_pin']);observedtools=metadata(packet['actual_B_complete_context_snapshot_extraction_post_tools_pin']);genuine(observedtools,'actual_review_return',packet['actual_B_complete_context_snapshot_extraction_post_pin'],'review_pin')
 need(observed['schema']=='ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1'and observed['status']=='PASS_ACTUAL_CURRENT_B_FULL55_CONTEXT8_SNAPSHOT_EXTRACTION_EVIDENCE_CHILD2_METADATA_ONLY'and observed['failure']is None and len(observed['all_snapshot_pairs'])==8 and len(observed['complete_context_pins'])==55 and packet['observed_B55_pair']==observed['all_snapshot_pairs'][-1]and packet['observed_B55_pair']['event']==55 and packet['observed_B55_pair']['role']=='final-complete-micro','actual full B55 final pair from all8 snapshots/all55 consecutive contexts, not A substitution')
 roots=packet['complete_joint_roots'];need(roots[:-1]==extractplan['complete_joint_roots']==host['complete_joint_roots']and len(roots)==78 and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(BASE.is_relative_to(Path(r))for r in roots[:-1]),'full original77 prefix plus exactly one fresh comparison78, FTOP counted')
 need(packet['planned_actual_output_root']==str(OUT)and(OUT.is_dir()if child else not os.path.lexists(OUT)),'fresh literal sole comparison owning root, no retry')
 need(packet['retained_B2_current_epoch_readonly_pins']==extractplan['retained_B2_current_epoch_readonly_pins']and packet['retained_current7_pins']==unique(extractplan['retained_current7_pins']+extraction['all_output_file_pins']),'all previous outputs/archived presence/B4/native and all three B2 extraction outputs retained')
 for p in packet['retained_current7_pins']+packet['retained_B2_current_epoch_readonly_pins']:current(p)
 for p in packet['explicit_cumulative_metadata_file_pins']:bm.current_metadata_role(p,build)
 return build,bm,extractplan,extraction,post

class Resources:
 def __init__(self,packet,build,bm,metadata_pins,started,stage_seconds):
  self.packet=packet;self.build=build;self.bm=bm;self.metadata_pins=unique(metadata_pins);self.started=started;self.stage_seconds=stage_seconds
  support=source(packet['original_support_Source_pin'],'B2_extract_resource_support');source(packet['original_production_inputs_Source_pin'],'production_inputs')
  helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B2_extract_resource_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'B2_extract_original_resource_factory');full,production=helper.modules();helper.guard_admission(full)
  self.history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure);self.joined=production.DiskResources(R/'validation',packet['complete_joint_roots'],8*2**30,2*2**30)
 def light(self):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-self.started<self.stage_seconds,'original SELF512 and stage/whole wall since initial claim')
  need(own_bytes(OUT)<OUTPUT_BOUND and own_bytes(BASE)<SOURCE_BOUND,'complete typed comparison output32MiB and all own Source16MiB hard boundaries')
  return peak
 def check(self):
  peak=self.light()
  command=['/bin/ps','-o','rss=','-p',str(os.getpid())];sample=subprocess.run(command,capture_output=True,text=True,timeout=2)
  need(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit()and int(sample.stdout.strip())*1024<512*2**20,'original same-PID PS RSS512 hard guard; private owning child guard unchanged')
  h=self.history.check();j=self.joined.check();extra=0
  for p in self.metadata_pins:
   self.bm.current_metadata_role(p,self.build)
   if not any(Path(p['path']).is_relative_to(Path(r))for r in self.packet['complete_joint_roots']):extra+=p['size_bytes']
  for p in self.packet['retained_B2_current_epoch_readonly_pins']:
   current(p);need(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'every nine-role B2 input already covered in original history, not fresh metadata or copied')
  unlinked={}
  for name in os.listdir('/dev/fd'):
   try:s=os.fstat(int(name))
   except(ValueError,OSError):continue
   if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[s.st_dev,s.st_ino]=s.st_size
  need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'unchanged complete joint2/history96/cold/meta/free8/external/open-unlinked')
  return dict(original_history=h,complete_joint=j,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),entire_comparison_output_bytes=own_bytes(OUT),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-self.started,actual_PS_return=dict(argv=command,returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr),current_PID=os.getpid(),current_parent_PID=os.getppid())

def admit_reservation(packet,before):
 existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']
 need(existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'actual full77 inherited prefix plus entire comparison32 and Source16 fits original2GiB before new output')
 return dict(complete_joint_roots=packet['complete_joint_roots'],original_caps=CAPS,only_current_stage='complete_B55_B2_compare',stage_output_reservation_bytes=OUTPUT_BOUND,new_Source_metadata_reservation_bytes=SOURCE_BOUND,existing_measured_total_bytes=existing,future_stages_not_reserved=True)
