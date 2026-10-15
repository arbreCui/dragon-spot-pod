"""UNREADY Root-only PACK production; positive readonly FD entry, no compile/GLOBAL/PROJECT."""
import argparse,fcntl,hashlib,importlib.util,json,os,resource,shutil,stat,struct,subprocess,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def need(v,s):
 if v is not True:raise RuntimeError(s)
def initial(p):
 q=Path(p['path']);s=q.lstat();ids=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and ids==p['identity']and s.st_size==p['size_bytes']and s.st_size<6*2**20 and not any(x.is_symlink()for x in(q,*q.parents)),'initial Source/small metadata exact regular7')
 raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256'],'initial full Source/metadata SHA');return json.loads(raw)if q.suffix=='.json'else raw

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for name in('source-pin','plan-pin','Source-review-pin','Source-review-tools-pin'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();start=time.monotonic()
 with(BASE/'ROOT_CONTROL_EXECUTION_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_A1_B2_A3_COMPLETE18_PACK_FD_CLAIM_V1',PID=os.getpid(),monotonic_start=start,argv=sys.argv,claim_before_bound_metadata_or_helper_import=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 ps=json.loads(a.source_pin);pb=json.loads(a.plan_pin);pr=json.loads(a.Source_review_pin);pt=json.loads(a.Source_review_tools_pin);initial(ps);plan=initial(pb);peer=initial(pr);tools=initial(pt)
 need(ps['path']==str(Path(__file__).absolute())and plan['host_source_pin']==ps,'exact current owning Host')
 cp=plan['contract_Source_pin'];initial(cp);need(Path(cp['path'])==BASE/'production_PACK_FD_Source_contract.UNREADY.py','literal local frozen contract Source')
 spec=importlib.util.spec_from_file_location('Root_readonly_FD_control_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.genuine(tools,'actual_review_return',pr,'review_pin');need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_A1_B2_A3_PACK_ONLY_FD_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==ps and peer['plan_pin']==pb and peer['complete_source_file_pins']==plan['complete_source_file_pins'],'genuine same five Source files including deck and PLAN independent Source0')
 m.admit(plan)
 need(plan['complete_source_file_pins']==[plan[k]for k in('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','exact_PACK_deck_Source_pin')]and len(plan['complete_source_file_pins'])==5,'exact four Python Sources plus reviewed PACK deck')
 for p in plan['complete_source_file_pins']:need(m.pin_source(p['path'])==p,'whole five Source files including PACK deck frozen')
 need(sys.platform=='darwin'and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and fcntl.F_GETFL==3 and os.O_ACCMODE==3 and os.O_RDONLY==0 and os.SEEK_SET==0,'exact declared macOS libc constants and original unoptimized mode')
 m.source_module(plan['original_production_inputs_Source_pin'],'production_inputs');c=m.source_module(plan['original_Common_Source_pin'],'FD_control_original_common');support=m.source_module(plan['original_support_Source_pin'],'FD_control_original_support')
 need(Path(sys.executable).resolve()==support.PYTHON and all(os.environ.get(k)=='1'for k in c.THREADS),'exact original Python and one-thread environment')
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'FD_control_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'FD_control_original_history');full,production=helper.modules();guard_files=helper.guard_admission(full)
 need(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'unchanged original OwnRSS class/MRO/PID guard')
 roots=plan['complete_joint_roots'];joined=production.DiskResources(m.R/'validation',roots,8*2**30,2*2**30);history=factory.DynamicHistoryResources(c.ART,factory.history_roots([],c.ART),8*2**30,96*2**30,production.ResourceFailure);explicit=m.unique(plan['explicit_cumulative_metadata_file_pins']+[ps,pb,pr,pt]);owned=[]
 class Resources:
  def check(self):
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800,'original SELF512 and whole1800 from claim')
   sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(os.getpid())],capture_output=True,text=True,timeout=2);need(sample.returncode==0 and sample.stderr==''and len(sample.stdout)<1024 and sample.stdout.strip().isdigit()and int(sample.stdout.strip())*1024<512*2**20,'same-PID Root PS512')
   h=history.check();j=joined.check();extra=0
   for p in explicit:
    m.current_metadata_role(p,plan)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in roots):extra+=p['size_bytes']
   m.retained(plan)
   for p in plan['readonly_history_code_and_selected_native_pins']:need(any(Path(p['path']).is_relative_to(Path(r))for r in h['resource_roots']),'actual declared history-covered readonly roles, never project tools')
   for p in owned:m.current(p)
   own=sum(p.lstat().st_size for p in m.OUT.rglob('*')if p.is_file())if m.OUT.exists()else 0;local=sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file());need(own<m.OUTPUT_BOUND and local<m.SOURCE_BOUND,'complete own conditional PACK512MiB/Source8MiB')
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:st=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(st.st_mode)and st.st_nlink==0:unlinked[st.st_dev,st.st_ino]=st.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original fresh2/history96/cold/meta64reserve/free8 with all external/open-unlinked')
   return dict(complete_joint_bytes=j['artifact_bytes'],explicit_external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),history_artifact_bytes=h['artifact_bytes'],history_root_count=len(h['resource_roots']),disk_free_bytes=j['disk_free_bytes'],own_output_bytes=own,own_Source_bytes=local,SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-start,Root_same_PID_PS=dict(returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr))
 readback_started=None
 resources=Resources();before=resources.check();need(before['complete_joint_bytes']+before['explicit_external_metadata_bytes']+before['open_unlinked_bytes']+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'fresh whole86 plus conditional PACK512/Source8 reserve')
 fixed=m.unique(plan['complete_source_file_pins']+[ps,pb,pr,pt,plan['runtime_pin'],plan['original_XSM_parser_Source_pin']]+[c.pin(p)for p in guard_files])
 def check():
  for p in fixed:m.current_metadata_role(p,plan);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  return resources.check()

 check();m.OUT.mkdir()
 for name in('runtime','sources','pack','PACK_only'):(m.OUT/name).mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');need(c.pin(m.OUT/'runtime/run_bounded_dragon.py')['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source');owned.append(c.pin(m.OUT/'runtime/run_bounded_dragon.py'))
 for role in('launcher_Source_pin','readback_Source_pin'):
  p=plan[role];q=m.OUT/'sources'/Path(p['path']).name;shutil.copy2(p['path'],q);new=c.pin(q);need(new['sha256']==p['sha256']and new['size_bytes']==p['size_bytes'],'only reviewed small code Source copies');owned.append(new)
 for p in plan['ordered_three_real_archive_full_pins']:m.current_metadata_role(p,plan)
 deck=m.OUT/'pack/pack.x2m';shutil.copy2(plan['exact_PACK_deck_Source_pin']['path'],deck);dp=c.pin(deck);need(dp['sha256']==plan['exact_PACK_deck_Source_pin']['sha256'],'exact seven operands/four outputs/three readonly FD deck');owned.append(dp)
 four=[plan[k]for k in('FD_control_Root_report_pin','FD_control_Root_tools_pin','FD_control_actual_post_pin','FD_control_actual_post_tools_pin')]
 manifest=dict(schema='CURRENT_A1_B2_A3_PRODUCTION_PACK_READONLY_FD_MANIFEST_V1',catalog_pin=plan['selected27_catalog_pin'],runtime_pin=plan['runtime_pin'],ordered_three_real_archive_full_pins=plan['ordered_three_real_archive_full_pins'],actual_FD_control_four_closure_pins=four,FD_control_Root0_and_post0_closed=True)
 mp=m.OUT/'pack/READONLY_FD_MANIFEST.json';c.write(mp,manifest);pm=c.pin(mp);owned.append(pm)
 cmd=[str(support.PYTHON),'-B',str(m.OUT/'sources/open_exact_three_cold_archives_then_exec_Dragon.UNREADY.py'),'--manifest-pin',json.dumps(pm,separators=(',',':'))]
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'PACK_only',resources);need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','one unmodified original ownchild PID/group guard, no compiler or nested subprocess')
 first=None;secondary=[];after=None;good=False;watch=None;watchpin=None;logpin=None;receiptpin=None;receipt=None;packpin=None;rconpins=[];packed=None;rconproofs=None;strict=None;readback_elapsed=None
 try:
  check();err=None
  try:runner.execute(m.OUT/'pack','produce_complete18_PACK_only',cmd,600,marker=plan['executed_PACK_completion_marker'],deck='pack.x2m')
  except BaseException as e:err=e
  if runner.records:
   record=runner.records[-1];wp=m.OUT/(record['label']+'.watchdog.json');lp=m.OUT/(record['label']+'.log')
   if wp.exists():watchpin=c.pin(wp);watch=m.metadata(watchpin)
   if lp.exists():logpin=c.pin(lp)
  if err is not None:raise err
  need(len(runner.records)==1 and record['status']=='PASS'and watch is not None and watch['command']==cmd==record['command']and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and logpin['sha256']==record['log_sha256'],'actual positive-only native stage0/launcherargv/original monitor closure once')
  receiptpin=c.pin(m.OUT/'pack/PRODUCTION_FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json');receipt=m.metadata(receiptpin);need(receipt['PID']==receipt['process_group']==watch['pid']and receipt['new_child_spawned']is False and receipt['negative_control_modes_available']is False and receipt['symlinks_or_hardlinks_created']is False and receipt['scientific_archive_copies_written']is False and receipt['runtime_pin']==plan['runtime_pin']and receipt['catalog_pin']==plan['selected27_catalog_pin']and [x['real_original_full_pin']for x in receipt['fixed_fd_proofs']]==plan['ordered_three_real_archive_full_pins']and [x['readonly_fd']for x in receipt['fixed_fd_proofs']]==[101,102,103],'exact real archive→FD→samePID exec receipt, no alias/copy/general bypass')
  readback_started=time.monotonic();packpin=c.pin(m.OUT/'pack/initial_pack.xsm');rconpins=[c.pin(m.OUT/'pack'/('plane'+str(p)+'_rcon.xsm'))for p in(1,2,3)];owned.extend([packpin,*rconpins]);check()
  last_scan=0.0
  def checkpoint(force=False):
   nonlocal last_scan
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800 and time.monotonic()-readback_started<600,'every bounded read SELF512/whole1800/readback600')
   if force or time.monotonic()-last_scan>=5:resources.check();last_scan=time.monotonic()
  checkpoint(True);rb=m.source_module(plan['readback_Source_pin'],'PACK_independent_bounded_complete18_readback');rb.READ_CHECK=checkpoint
  packed=rb.packed_readback(packpin['path'],plan);need(len(packed)==18 and [(x['plane'],x['field'])for x in packed]==[(p,f)for p in(1,2,3)for f in('TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND')],'complete independent18 trees, no sampled or macro-only substitute')
  rconproofs=[];strict=[]
  with rb._open_xsm(packpin['path'])as a:
   for p,row in enumerate(plan['producers'],1):
    route=rb.node(a,a.root,['RCONTRACT',p]);bind=rb.node(a,a.root,['BOOT_BIND',p]);flux=rb.node(a,a.root,['FLUX',p]);seal=rb.node(a,flux,['ROOT64-SEAL']);expected=row['expected_case'].rstrip()
    need(route['CASE-NAME'][1:]==(3,3)and seal['CASE'][1:]==(3,3),'exact typed12-character native plane case records');rb.chars(a,route,'CASE-NAME',expected);rb.chars(a,seal,'CASE',expected)
    need(rb.scalar(a,bind,'PLANE',1)==rb.scalar(a,seal,'PLANE',1)==p and rb.scalar(a,bind,'EPOCH',1)==rb.scalar(a,seal,'EPOCH',1)==0,'strict plane/e0 in bind and native seal')
    dimsentry=seal['DIMS'];need(dimsentry[1:]==(4,1),'native exact4 typed dimensions');dims=struct.unpack('<4i',a.read(dimsentry[0],dimsentry[1]));need(dims[0]==370 and dims[1]==14,'full370×14 native extent unchanged')
    native=flux['SPOT-KEFF64'];saved=seal['KEFF64'];mirror=flux['K-EFFECTIVE'];need(native[1:]==saved[1:]==(2,4)and mirror[1:]==(1,2),'type4 double native and seal keff, type2 mirror')
    nb=a.read(native[0],native[1]);sb=a.read(saved[0],saved[1]);need(nb==sb,'all original64-bit keff words unchanged');keff=struct.unpack('<d',nb)[0];need(keff>0 and keff<float('inf')and struct.pack('<f',keff)==a.read(mirror[0],mirror[1]),'finite positive native64 and exact32 mirror, original predicate')
    typed=0
    for parent,name in((flux,'ROOT-FLUX64'),(flux,'FLUX64'),(seal,'ROOT-REF64')):
     entry=parent[name];need(entry[1:]==(370,10),'complete370 typed group list')
     for group in range(370):
      ptr=struct.unpack('<i',a.read(entry[0]+group,1))[0];wrapper=a.directory(ptr);need(set(wrapper)=={'***HANDLE***'}and wrapper['***HANDLE***'][1:]==(28,4),'every complete14-unknown group retains original type4 words');typed+=1
    with rb._open_xsm(rconpins[p-1]['path'])as b:rconproofs.append(dict(plane=p,complete_RCON_tree=rb.exact_tree(a,route,b,b.root)))
    strict.append(dict(plane=p,material=row['material'],expected_case=row['expected_case'],epoch=0,groups=370,unknowns=14,verified_full_type4_group_records=typed,native_keff64_raw_bytes=nb.hex(),native64_seal64_equal=True,native32_mirror_equal=True))
  checkpoint(True);readback_elapsed=time.monotonic()-readback_started;check();after=resources.check();good=True
 except BaseException as e:first=e
 finally:
  try:after=resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ROOT_CURRENT_A1_B2_A3_COMPLETE18_PACK_READONLY_FD_REPORT_V1',status='PASS_ACTUAL_A1_B2_A3_COMPLETE18_PACK_ONLY_NATIVE0_INDEPENDENT_READBACK0'if good and first is None else'FAILED_A1_B2_A3_PACK_ONLY_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,source_pin=ps,plan_pin=pb,complete_source_file_pins=plan['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,selected27_catalog_pin=plan['selected27_catalog_pin'],runtime_pin=plan['runtime_pin'],actual_FD_control_four_closure_pins=four,ordered_three_real_archive_full_pins=plan['ordered_three_real_archive_full_pins'],actual_stage_records=runner.records,actual_watchdog_pin=watchpin,actual_watchdog=watch,actual_log_pin=logpin,actual_production_FD_before_exec_receipt_pin=receiptpin,actual_production_FD_before_exec_receipt=receipt,actual_complete_PACK_pin=packpin,actual_ordered_three_RCON_pins=rconpins,actual_independent_complete18_tree_proofs=packed,actual_independent_three_RCON_tree_proofs=rconproofs,actual_independent_strict_plane_case_epoch_type4_keff_proofs=strict,actual_independent_readback_elapsed_seconds=readback_elapsed,whole_new_output_pins=[c.pin(q)for q in sorted(m.OUT.rglob('*'))if q.is_file()],original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,complete_joint_roots=roots,original_caps=m.CAPS,bounded_new_output_reservation_bytes=m.OUTPUT_BOUND,bounded_own_Source_metadata_receipts_bytes=m.SOURCE_BOUND,resources_before=before,resources_after=after,all27_real_cold_producer_roles_current7_retained=(good and first is None),actual_production_child_count=len(runner.records),scientific_archive_copies_written=False,symlinks_or_hardlinks_created=False,compiler_executed=False,build_reexecuted=False,APACK_negative_controls_executed=False,final_report_resource_check_passed=False,**m.FALSE)
  q=m.OUT/'Root_actual_A1_B2_A3_complete18_PACK_FD_summary.json';need(len((json.dumps(report,indent=2)+'\n').encode())<2*2**20,'PACK summary2MiB inside conditional512');c.write(q,report)
  try:
   resources.check();report['final_report_resource_check_passed']=True
   with q.open('w')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.truncate();f.flush();os.fsync(f.fileno())
   resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
 if first is not None:raise first
 print(json.dumps(dict(status=report['status'],report_pin=c.pin(q),**m.FALSE)),flush=True)
if __name__=='__main__':main()
