"""UNREADY complete B2 extraction owning contract. Metadata admission only on import."""
import hashlib,importlib.util,json,os,resource,stat,subprocess,sys,time
from pathlib import Path
R=Path('/Users/wen/spot');ART=R/'validation/artifacts';BASE=Path(__file__).absolute().parent
OUT=ART/'axial-material-current-nativeWarmB2-complete-physical-tree-extract-20261015-v1'
OUTPUT_BOUND=256*2**20;SOURCE_BOUND=16*2**20
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,fresh_bytes=2*2**30,history_bytes=96*2**30,cold_reserve_bytes=20971764748,metadata_reserve_bytes=64*2**20,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
FALSE=dict(original_RAM_bits_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,online_BOOT_qualified=False,reaction_multiplicity_qualified=False,scientific_accuracy_qualified=False)
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
 need(packet['schema']in('CURRENT_B2_COMPLETE_EXTRACTION_ADMISSION_PACKET_V1','CURRENT_B2_COMPLETE_EXTRACTION_SOURCE_ONLY_PLAN_V1')and packet['actual_business_preconditions_closed']is True and packet['source_role_pin_audit_complete']is True and packet['original_caps']==CAPS,'UNREADY NULL bridge/archive/exact1/post/latest-budget is never admitted')
 need(packet['Source_only_stat_budget_fits']is True and packet['Root_original_classes_recheck_required']is True,'honest current full stat precheck required; Root remeasures original classes before admission')
 need(packet['only_current_stage']=='complete_B2_extract'and packet['bounded_new_output_reservation_bytes']==OUTPUT_BOUND and packet['bounded_new_Source_metadata_reservation_bytes']==SOURCE_BOUND and packet['comparison_stage_not_in_this_execution']is True,'complete physical-tree extraction only256MiB plus Source16, no scope reduction or combined future comparison')
 bridge=metadata(packet['actual_B2_current_epoch_bridge_report_pin']);bridgetools=metadata(packet['actual_B2_current_epoch_bridge_Root_tools_pin']);bridgepost=metadata(packet['actual_B2_current_epoch_bridge_post_pin']);bridgeposttools=metadata(packet['actual_B2_current_epoch_bridge_post_tools_pin'])
 genuine(bridgetools,'actual_terminal_return',packet['actual_B2_current_epoch_bridge_report_pin'],'report_pin');genuine(bridgeposttools,'actual_review_return',packet['actual_B2_current_epoch_bridge_post_pin'],'review_pin')
 need(bridge['schema']=='ROOT_NATIVE_WARM_B2_CURRENT_EPOCH_BLIND_FULLFILE_BINDING_REPORT_V1'and bridge['status']=='PASS_B2_SELECTED_READONLY_ROLES_CURRENT_EPOCH_BLIND_SHA_ONLY'and bridge['failure']is None and bridge['final_report_resource_check_passed']is True and len(bridge['ordered_role_pairs'])==9 and bridge['original_caps']==CAPS,'genuine selected nine-role blind bridge0, not recertification of all4790 or lineage PASS')
 bc=packet['bridge_post_contract'];need(bridgepost['schema']==bc['schema']and bridgepost['status']==bc['status']and bridgepost['failure']is None and bridgepost[bc['Root_report_pin_field']]==packet['actual_B2_current_epoch_bridge_report_pin']and bridgepost[bc['Root_tools_pin_field']]==packet['actual_B2_current_epoch_bridge_Root_tools_pin'],'same independent genuine bridge metadata post0')
 need(packet['actual_current_epoch_B2_archive_pin']==bridge['current_epoch_B2_archive_pin']and packet['retained_B2_current_epoch_readonly_pins']==[r['current_epoch_full_pin']for r in bridge['ordered_role_pairs']]and packet['historical_B2_archive_pin']==next(r['historical_full_pin']for r in bridge['ordered_role_pairs']if r['role']=='B2_archive'),'historical/current B2 archive separate exact roles')
 for r in bridge['ordered_role_pairs']:
  p=r['current_epoch_full_pin'];old=r['historical_full_pin'];need(r['blind_complete_SHA_and_length_equal']is True and r['before_open_EOF_after_current7_stable']is True and p['sha256']==old['sha256']and p['size_bytes']==old['size_bytes']and p['identity'][1:]==old['identity'][1:]and old['identity'][0]==16777234 and p['identity'][0]==16777229,'old historical PF unchanged, only explicit device epoch rebind');current(p)
 # Exact single-presence lifecycle, not a generic missing-path skip.
 retirement=metadata(packet['actual_latest_complete_prefix_plan_pin']);receipt=metadata(packet['actual_presence_retirement_receipt_pin']);rtools=metadata(packet['actual_presence_retirement_Root_tools_pin']);rpost=metadata(packet['actual_presence_retirement_post_pin']);rptools=metadata(packet['actual_presence_retirement_post_tools_pin'])
 genuine(rtools,'actual_terminal_return',packet['actual_presence_retirement_receipt_pin'],'receipt_pin');genuine(rptools,'actual_review_return',packet['actual_presence_retirement_post_pin'],'review_pin')
 target=retirement['exact_target_pins'];need(retirement['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_PLAN_V1'and retirement['Source_admission_ready']is True and retirement['draft_unready']is False and len(target)==1 and target[0]['size_bytes']==169615994 and target[0]['sha256']=='9ac74eebba95d541a6281d61e3be7ad527cf19d44de54078e8ffc7627660eda7','one exact retired presence169615994B, original native and other result paths cannot be skipped')
 need(receipt['schema']=='CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_RETIREMENT_RECEIPT_V1'and receipt['mode']=='execute'and receipt['status']=='RETIRED_CURRENT_BAGG_PRESENCE_EXACT1_ORIGINAL_COMPLETE_BYTES_IN_ARCHIVE'and receipt['failure']is None and receipt['plan_pin']==packet['actual_latest_complete_prefix_plan_pin']and receipt['actual_released_pins']==receipt['exact_target_pins']==target and receipt['actual_released_bytes']==169615994 and receipt['resources_after_original_classes_forced_fresh']is True and receipt['files_deleted']is True and all(not os.path.lexists(p['path'])for p in target),'genuine exact1 retirement0 and final forced-fresh original guards; no original plaintext reopening')
 rc=retirement['execute_post_report_contract'];need(rpost['schema']==rc['schema']and rpost['status']==rc['status']and rpost['failure']is None and rpost['metadata_only']is True and rpost['actual_execution_receipt_pin']==packet['actual_presence_retirement_receipt_pin']and rpost['actual_Root_tools_pin']==packet['actual_presence_retirement_Root_tools_pin']and rpost['plan_pin']==packet['actual_latest_complete_prefix_plan_pin']and rpost['actual_released_pins']==target and rpost['actual_released_bytes']==169615994 and type(rpost['actual_Root_integer_exit_code'])is int and rpost['actual_Root_integer_exit_code']==0,'genuine independent exact1 retirement metadata post0 exact identity and release scope')
 cp=retirement['actual_archive_closure_pins'];need(packet['actual_presence_archive_report_pin']==cp['Host']and packet['actual_presence_archive_Root_tools_pin']==cp['Root_tools']and packet['actual_presence_archive_post_pin']==cp['post']and packet['actual_presence_archive_post_tools_pin']==cp['post_tools'],'same complete presence archive0/post0 retained as exact retired-result mapping')
 archive=metadata(retirement['inherited_complete_archive_plan_pin']);apost=metadata(cp['post']);aptools=metadata(cp['post_tools']);genuine(aptools,'actual_review_return',cp['post'],'review_pin');genuine(metadata(cp['Root_tools']),'actual_terminal_return',cp['Host'],'report_pin')
 need(apost['schema']=='RECORDED_CURRENT_BAGG_SINGLE_PRESENCE_LOSSLESS_ARCHIVE_METADATA_POSTVERIFY_V1'and apost['status']=='PASS_ACTUAL_SINGLE_BAGG_PRESENCE_STREAMED_SHA_LENGTH_ARCHIVE_METADATA_ONLY_ORIGINAL_RETAINED'and apost['failure']is None and apost['actual_Host_report_pin']==cp['Host']and apost['actual_Root_tools_pin']==cp['Root_tools']and type(apost['actual_Root_integer_exit_code'])is int and apost['actual_Root_integer_exit_code']==0 and type(apost['actual_child_integer_exit_code'])is int and apost['actual_child_integer_exit_code']==0 and apost['original_presence_full_pin']==target[0]and apost['compressed_presence_archive_full_pin']==retirement['retained_presence_gzip_pins'][0]and apost['presence_entry_pin']==retirement['retained_presence_entry_pins'][0]and apost['Root_actual_streamed_decompression_proof_matched_original_fullPF']is True,'complete exact presence original/gzip/entry/index byte-proof metadata retained; creation-time original live remains historical')
 roots=packet['complete_joint_roots'];need(roots[:-1]==retirement['complete_joint_roots']==archive['complete_joint_roots']and len(roots)==77 and roots[-1]==str(OUT)and len(roots)==len(set(roots))and not any(Path(a).is_relative_to(Path(b))for a in roots for b in roots if a!=b)and any(BASE.is_relative_to(Path(r))for r in roots[:-1]),'full original75 plus presence76 plus fresh extraction77, including complete FTOP Source')
 need(packet['planned_actual_output_root']==str(OUT)and (OUT.is_dir()if child else not os.path.lexists(OUT)),'literal fresh owning extraction root; no retry')
 need(packet['retained_current7_pins']==retirement['retained_current7_pins']+retirement['retained_presence_gzip_pins']+retirement['retained_presence_entry_pins']+[cp['index']]and not{p['path']for p in target}&{p['path']for p in packet['retained_current7_pins']+packet['explicit_cumulative_metadata_file_pins']},'exact sole historical absent presence excluded, every other result/native/input/archive/entry/index remains current7')
 for p in packet['retained_current7_pins']:current(p)
 metadata(packet['actual_B2_lineage_metadata_audit_pin']) # Explicit known/unknown roles; no True lineage invented.
 build=metadata(packet['original_guard_build_plan_pin']);bm=source(packet['original_guard_build_contract_Source_pin'],'B2_extract_original_build_metadata_roles');bm.admit_lifecycle(build)
 for k in('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin'):need(packet[k]==build[k],'unchanged exact original owning guard dependency')
 for p in packet['explicit_cumulative_metadata_file_pins']:bm.current_metadata_role(p,build)
 for p in packet['child_ordinary_explicit_metadata_pins']:
  current(p);need(Path(p['path']).lstat().st_uid==os.getuid(),'child ordinary metadata only; system roles stay delegated exact table')
 return build,bm,archive,retirement,bridge

class Resources:
 def __init__(self,packet,build,bm,metadata_pins,started,stage_seconds):
  self.packet=packet;self.build=build;self.bm=bm;self.metadata_pins=unique(metadata_pins);self.started=started;self.stage_seconds=stage_seconds
  support=source(packet['original_support_Source_pin'],'B2_extract_resource_support');source(packet['original_production_inputs_Source_pin'],'production_inputs')
  helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B2_extract_resource_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'B2_extract_original_resource_factory');full,production=helper.modules();helper.guard_admission(full)
  self.history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure);self.joined=production.DiskResources(R/'validation',packet['complete_joint_roots'],8*2**30,2*2**30)
 def light(self):
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-self.started<self.stage_seconds,'original SELF512 and stage/whole wall since initial claim')
  need(own_bytes(OUT)<OUTPUT_BOUND and own_bytes(BASE)<SOURCE_BOUND,'complete extraction output256MiB and all own Source16MiB hard boundaries')
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
  return dict(original_history=h,complete_joint=j,explicit_external_metadata_bytes=extra,host_open_unlinked_bytes=sum(unlinked.values()),entire_extraction_output_bytes=own_bytes(OUT),host_SELF_peak_bytes=peak,whole_elapsed_seconds=time.monotonic()-self.started,actual_PS_return=dict(argv=command,returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr),current_PID=os.getpid(),current_parent_PID=os.getppid())

def admit_reservation(packet,before):
 existing=before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']+before['host_open_unlinked_bytes']
 need(existing+OUTPUT_BOUND+SOURCE_BOUND<2*2**30,'actual full76 prefix plus entire extraction256 and Source16 fits original2GiB before new output')
 return dict(complete_joint_roots=packet['complete_joint_roots'],original_caps=CAPS,only_current_stage='complete_B2_extract',stage_output_reservation_bytes=OUTPUT_BOUND,new_Source_metadata_reservation_bytes=SOURCE_BOUND,existing_measured_total_bytes=existing,comparison_stage_not_reserved=True)
