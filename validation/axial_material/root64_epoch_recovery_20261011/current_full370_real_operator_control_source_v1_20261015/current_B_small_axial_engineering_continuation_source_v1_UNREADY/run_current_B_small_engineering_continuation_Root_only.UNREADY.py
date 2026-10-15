"""UNREADY Root-only small new B engineering contexts; no GLOBAL/PROJECT/coupled-reference qualification."""
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
 with(BASE/'ROOT_CONTROL_EXECUTION_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_CURRENT_B_SMALL_ENGINEERING_CONTINUATION_CLAIM_V1',PID=os.getpid(),monotonic_start=start,argv=sys.argv,claim_before_bound_metadata_or_helper_import=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 ps=json.loads(a.source_pin);pb=json.loads(a.plan_pin);pr=json.loads(a.Source_review_pin);pt=json.loads(a.Source_review_tools_pin);initial(ps);plan=initial(pb);peer=initial(pr);tools=initial(pt)
 need(ps['path']==str(Path(__file__).absolute())and plan['host_source_pin']==ps,'exact current owning Host')
 cp=plan['contract_Source_pin'];initial(cp);need(Path(cp['path'])==BASE/'small_B_engineering_continuation_contract.UNREADY.py','literal local frozen contract Source')
 spec=importlib.util.spec_from_file_location('Root_readonly_FD_control_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.genuine(tools,'actual_review_return',pr,'review_pin');need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_CURRENT_B_ENGINEERING_CONTINUATION_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_CURRENT_B_ENGINEERING_CONTINUATION'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==ps and peer['plan_pin']==pb and peer['complete_source_file_pins']==plan['complete_source_file_pins'],'genuine same five Source files including deck and PLAN independent Source0')
 prior_host,prior_failure_post=m.admit(plan)
 need(plan['complete_source_file_pins']==[plan[k]for k in('host_source_pin','contract_Source_pin','launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin')]and len(plan['complete_source_file_pins'])==5,'exact five Python Sources including complete original-math deck builder')
 for p in plan['complete_source_file_pins']:need(m.pin_source(p['path'])==p,'whole five current-context Source files frozen')
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
   own=sum(p.lstat().st_size for p in m.OUT.rglob('*')if p.is_file())if m.OUT.exists()else 0;local=sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file());need(own<m.OUTPUT_BOUND and local<m.SOURCE_BOUND,'complete own conditional context128MiB/Source8MiB')
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:st=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(st.st_mode)and st.st_nlink==0:unlinked[st.st_dev,st.st_ino]=st.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original fresh2/history96/cold/meta64reserve/free8 with all external/open-unlinked')
   return dict(complete_joint_bytes=j['artifact_bytes'],explicit_external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),history_artifact_bytes=h['artifact_bytes'],history_root_count=len(h['resource_roots']),disk_free_bytes=j['disk_free_bytes'],own_output_bytes=own,own_Source_bytes=local,SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-start,Root_same_PID_PS=dict(returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr))
 readback_started=None
 resources=Resources();before=resources.check();need(before['complete_joint_bytes']+before['explicit_external_metadata_bytes']+before['open_unlinked_bytes']+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'fresh whole88 plus conditional context128/Source8 reserve')
 fixed=m.unique(plan['complete_source_file_pins']+[ps,pb,pr,pt,plan['runtime_pin'],plan['original_XSM_parser_Source_pin']]+list(plan['small_tool_saved_SHA_and_current7_candidate_roles'].values())+[c.pin(p)for p in guard_files])
 def check():
  for p in fixed:m.current_metadata_role(p,plan);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  return resources.check()

 check();m.OUT.mkdir()
 for name in('runtime','sources','context','ENGINEERING_only'):(m.OUT/name).mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');need(c.pin(m.OUT/'runtime/run_bounded_dragon.py')['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole unchanged bounded supervisor Source');owned.append(c.pin(m.OUT/'runtime/run_bounded_dragon.py'))
 for role in('launcher_Source_pin','readback_Source_pin','deck_builder_Source_pin'):
  p=plan[role];q=m.OUT/'sources'/Path(p['path']).name;shutil.copy2(p['path'],q);new=c.pin(q);need(new['sha256']==p['sha256']and new['size_bytes']==p['size_bytes'],'reviewed whole Source copies');owned.append(new)
 build=m.source_module(plan['deck_builder_Source_pin'],'same_original_B_engineering_deck_math');all_decks=build.engineering_decks(plan);decks={k:all_decks[k]for k in('initial','axial')}
 for label,text in decks.items():
  q=m.OUT/'context'/(label+'.x2m')
  with q.open('x')as stream:stream.write(text);stream.flush();os.fsync(stream.fileno())
  owned.append(c.pin(q))
 four=[plan[k]for k in('PACK_Root_report_pin','PACK_Root_tools_pin','PACK_actual_post_pin','PACK_actual_post_tools_pin')];rows=[plan['PACK_full_pin'],*plan['ordered_three_plane_RCON_pins'][:2]];manifests={}
 for label in decks:
  value=dict(schema='CURRENT_B_ENGINEERING_PACK_RCON_FD_MANIFEST_V1',stage_label=label,runtime_pin=plan['runtime_pin'],ordered_exact_PACK_RCON1_RCON2_full_pins=rows,actual_PACK_four_closure_pins=four,PACK_Root0_and_independent_post0_closed=True);q=m.OUT/'context'/(label+'.FD_manifest.json');c.write(q,value);manifests[label]=c.pin(q);owned.append(manifests[label])
 # Independent Root blind fullEOF verification while copying exact nine reusable files.
 copy_started=time.monotonic();last_copy_scan=0.0
 def copy_light():
  nonlocal last_copy_scan
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800 and time.monotonic()-copy_started<600,'all nine complete copies bounded SELF512/stage600/whole1800')
  if time.monotonic()-last_copy_scan>=5:resources.check();last_copy_scan=time.monotonic()
 copied=[]
 for p in plan['ordered_reused_nine_complete_full_pins']:
  m.current(p);q=m.OUT/'context'/Path(p['path']).name;h=hashlib.sha256();total=0
  with Path(p['path']).open('rb')as src,q.open('xb')as dst:
   need(m.identity(os.fstat(src.fileno()))==p['identity'],'opened exact completed original file7')
   while True:
    copy_light();block=src.read(2**20)
    if not block:break
    h.update(block);total+=len(block);dst.write(block)
   dst.flush();os.fsync(dst.fileno());need(m.identity(os.fstat(src.fileno()))==p['identity'],'EOF unchanged original9 current7')
  m.current(p);new=c.pin(q);need(total==new['size_bytes']==p['size_bytes']and h.hexdigest()==new['sha256']==p['sha256'],'independent complete copy original/destination SHA+length equality');owned.append(new);copied.append(dict(original_saved_full_pin=p,new_owned_complete_copy_full_pin=new))
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'ENGINEERING_only',resources);need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','unchanged original single ownchild PID/group RSS guard')
 stages=[];first=None;secondary=[];after=None;good=False;rank_admission=prior_host['actual_fresh_complete370_rank_admission'];scientific=None;outputpins=[];readback_elapsed=None
 def stage(label,command,marker,deck=None,fdlabel=None):
  check();error=None
  try:runner.execute(m.OUT/'context',label,command,600,marker=marker,deck=deck)
  except BaseException as e:error=e
  record=runner.records[-1]if runner.records else None;wp=m.OUT/(record['label']+'.watchdog.json')if record else None;lp=m.OUT/(record['label']+'.log')if record else None
  wpin=c.pin(wp)if wp is not None and wp.exists()else None;lpin=c.pin(lp)if lp is not None and lp.exists()else None;watch=m.metadata(wpin)if wpin else None;entry=dict(stage_label=label,original_record=record,actual_watchdog_pin=wpin,actual_watchdog=watch,actual_log_pin=lpin,actual_before_exec_receipt_pin=None,actual_before_exec_receipt=None);stages.append(entry)
  if error is not None:raise error
  need(record['status']=='PASS'and watch['command']==command==record['command']and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True and watch['rss_cap_mib']==512 and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and lpin['sha256']==record['log_sha256'],'actual stage single-child0 genuine original guard closure')
  if fdlabel is not None:
   p=c.pin(m.OUT/'context'/(fdlabel+'.FD_before_exec.json'));v=m.metadata(p);need(v['stage_label']==fdlabel and v['manifest_pin']==manifests[fdlabel]and v['PID']==v['process_group']==watch['pid']and v['new_child_spawned']is False and v['negative_control_modes_available']is False and v['symlinks_or_hardlinks_created']is False and v['scientific_large_input_copies_written']is False and [x['real_original_full_pin']for x in v['fixed_fd_proofs']]==rows and [x['readonly_fd']for x in v['fixed_fd_proofs']]==[101,102,103],'actual exact PACK/RCON FD identities and same-PID exec');entry.update(actual_before_exec_receipt_pin=p,actual_before_exec_receipt=v)
  check();return lp
 def native(label,marker):
  cmd=[str(support.PYTHON),'-B',str(m.OUT/'sources/open_exact_PACK_and_RCONs_then_same_PID_exec.UNREADY.py'),'--manifest-pin',json.dumps(manifests[label],separators=(',',':'))]
  return stage(label,cmd,marker,deck=label+'.x2m',fdlabel=label)
 try:
  native('initial','CURRENT-B-CONTEXT-INITIAL-SYSTEM-COMPLETE');native('axial','CURRENT-B-CONTEXT-AXIAL-ENGINEERING-COMPLETE')
  need([x['stage_label']for x in stages]==['initial','axial']and len(runner.records)==2,'only two continuation native stages; prior four stages are never repeated')
  readback_started=time.monotonic();last_scan=0.0
  def checkpoint(force=False):
   nonlocal last_scan
   peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024);need(peak<512*2**20 and time.monotonic()-start<1800 and time.monotonic()-readback_started<600,'every bounded independent read SELF512/stage600/whole1800')
   if force or time.monotonic()-last_scan>=5:resources.check();last_scan=time.monotonic()
  checkpoint(True);rb=m.source_module(plan['readback_Source_pin'],'complete_current_B_engineering_readback');rb.READ_CHECK=checkpoint;scientific=rb.verify_engineering_outputs(m.OUT/'context',plan);checkpoint(True)
  outputpins=[c.pin(m.OUT/'context'/n)for n in('basis.xsm','axial_track_unmarked.xsm','axial_track.xsm','axial_macro.xsm','initial_system.xsm','ax_current.xsm','global_rcon.xsm','plane3_rcon.xsm','radial1.bin','radial2.bin','radial3.bin')];readback_elapsed=time.monotonic()-readback_started;check();after=resources.check();good=True
 except BaseException as e:first=e
 finally:
  try:after=resources.check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ROOT_CURRENT_B_SMALL_ENGINEERING_CONTINUATION_REPORT_V1',status='PASS_ACTUAL_CURRENT_B_ENGINEERING_CONTINUATION_ROOT0_TWO_CHILD0_COMPLETE_READBACK0'if good and first is None else'FAILED_CURRENT_B_ENGINEERING_CONTINUATION_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,source_pin=ps,plan_pin=pb,complete_source_file_pins=plan['complete_source_file_pins'],independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,actual_PACK_four_closure_pins=four,PACK_full_pin=plan['PACK_full_pin'],original_three_plane_RCON_pins=plan['ordered_three_plane_RCON_pins'],production_config=plan['production_config'],global_case_name='PIN-ABA',prior_failed_Root_report_pin=plan['prior_failed_Root_report_pin'],prior_failed_Root_tools_pin=plan['prior_failed_Root_tools_pin'],prior_failure_actual_post_pin=plan['prior_failure_actual_post_pin'],prior_failure_actual_post_tools_pin=plan['prior_failure_actual_post_tools_pin'],prior_original_Root_integer_exit_code=1,prior_actual_child_integer_exit_codes=prior_host['actual_child_integer_exit_codes'],prior_original_stage_records=prior_host['original_stage_records'],prior_original_marker_failed_record_preserved=True,common_basis_retrained=False,rank_native_stage_repeated=False,white_tracking_tool_repeated=False,make_route_contract_tool_repeated=False,existing_new_A1_B2_A3_common_basis_reused_from_failed_v1=True,old_allA_basis_or_context_reused=False,retained_prior_actual_tool_fullEOF_proof_pins=prior_host['actual_Root_small_tools_fullEOF_and_stable7_verified_pins'],reused_prior_genuine_complete370_rank_admission=rank_admission,actual_stage_checks=stages,original_stage_records=runner.records,actual_child_integer_exit_codes=[x['actual_watchdog']['returncode']if x['actual_watchdog']is not None else None for x in stages],actual_complete_engineering_scientific_readback=scientific,actual_independent_readback_elapsed_seconds=readback_elapsed,actual_complete_scientific_output_pins=outputpins,actual_independent_nine_fullEOF_copy_proofs=copied,actual_independent_nine_copy_bytes=sum(x['new_owned_complete_copy_full_pin']['size_bytes']for x in copied),whole_new_output_pins=[c.pin(q)for q in sorted(m.OUT.rglob('*'))if q.is_file()],complete_joint_roots=roots,original_caps=m.CAPS,bounded_new_output_reservation_bytes=m.OUTPUT_BOUND,bounded_own_Source_metadata_receipts_bytes=m.SOURCE_BOUND,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,resources_before=before,resources_after=after,final_report_resource_check_passed=False,compiler_executed=False,build_reexecuted=False,production_runner_run_ABA_or_qualify_ABA_called=False,coupled_reference_executed=False,**m.FALSE)
  q=m.OUT/'Root_actual_current_B_small_engineering_continuation_summary.json';need(len((json.dumps(report,indent=2)+'\n').encode())<2*2**20,'bounded complete engineering summary inside128');c.write(q,report)
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
