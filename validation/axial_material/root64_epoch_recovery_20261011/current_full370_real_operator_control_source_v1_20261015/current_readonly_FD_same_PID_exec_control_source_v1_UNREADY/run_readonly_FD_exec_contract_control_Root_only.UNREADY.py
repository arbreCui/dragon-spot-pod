"""Root-only original-guard control of three tiny non-scientific fixtures. No production data IO."""
import argparse,fcntl,hashlib,importlib.util,json,os,resource,shutil,stat,subprocess,sys,time
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
 with(BASE/'ROOT_CONTROL_EXECUTION_CLAIM.json').open('x')as f:json.dump(dict(schema='ROOT_EXCLUSIVE_NONSCIENTIFIC_FD_CONTROL_CLAIM_V1',PID=os.getpid(),monotonic_start=start,argv=sys.argv,claim_before_bound_metadata_or_helper_import=True),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 ps=json.loads(a.source_pin);pb=json.loads(a.plan_pin);pr=json.loads(a.Source_review_pin);pt=json.loads(a.Source_review_tools_pin);initial(ps);plan=initial(pb);peer=initial(pr);tools=initial(pt)
 need(ps['path']==str(Path(__file__).absolute())and plan['host_source_pin']==ps,'exact current owning Host')
 cp=plan['contract_Source_pin'];initial(cp);need(Path(cp['path'])==BASE/'readonly_FD_exec_control_contract.UNREADY.py','literal local frozen contract Source')
 spec=importlib.util.spec_from_file_location('Root_readonly_FD_control_contract',cp['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 m.genuine(tools,'actual_review_return',pr,'review_pin');need(peer['schema']=='INDEPENDENT_SOURCE_ONLY_NONSCIENTIFIC_FD_EXEC_CONTRACT_CONTROL_REVIEW_V1'and peer['status']=='PASS_SOURCE_ONLY_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTROL'and peer['source_only']is True and peer['failure']is None and peer['source_pin']==ps and peer['plan_pin']==pb and peer['complete_source_file_pins']==plan['complete_source_file_pins'],'genuine same4Source/PLAN independent Source0')
 m.admit(plan)
 for p in plan['complete_source_file_pins']:need(m.pin_source(p['path'])==p,'whole four Source bytes frozen')
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
   own=sum(p.lstat().st_size for p in m.OUT.rglob('*')if p.is_file())if m.OUT.exists()else 0;local=sum(p.lstat().st_size for p in BASE.rglob('*')if p.is_file());need(own<m.OUTPUT_BOUND and local<m.SOURCE_BOUND,'complete own control32MiB/Source8MiB')
   unlinked={}
   for name in os.listdir('/dev/fd'):
    try:st=os.fstat(int(name))
    except(ValueError,OSError):continue
    if stat.S_ISREG(st.st_mode)and st.st_nlink==0:unlinked[st.st_dev,st.st_ino]=st.st_size
   need(j['artifact_bytes']+extra+sum(unlinked.values())<2*2**30 and h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original fresh2/history96/cold/meta64reserve/free8 with all external/open-unlinked')
   return dict(complete_joint_bytes=j['artifact_bytes'],explicit_external_metadata_bytes=extra,open_unlinked_bytes=sum(unlinked.values()),history_artifact_bytes=h['artifact_bytes'],history_root_count=len(h['resource_roots']),disk_free_bytes=j['disk_free_bytes'],own_output_bytes=own,own_Source_bytes=local,SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-start,Root_same_PID_PS=dict(returncode=sample.returncode,stdout=sample.stdout,stderr=sample.stderr))
 resources=Resources();before=resources.check();need(before['complete_joint_bytes']+before['explicit_external_metadata_bytes']+before['open_unlinked_bytes']+m.OUTPUT_BOUND+m.SOURCE_BOUND<2*2**30,'fresh whole85 plus control32/Source8 reserve')
 fixed=m.unique(plan['complete_source_file_pins']+[ps,pb,pr,pt,plan['Fortran_compiler_pin']]+[c.pin(p)for p in guard_files])
 def check():
  for p in fixed:m.current_metadata_role(p,plan);c.same_pin(p['path'],p)
  for p in owned:m.current(p);c.same_pin(p['path'],p)
  return resources.check()
 check();m.OUT.mkdir()
 for name in('runtime','sources','build','fixtures','positive','closed_fd','wrong7','duplicate_inode','FD_control'):(m.OUT/name).mkdir()
 shutil.copy2(support.BOUNDED,m.OUT/'runtime/run_bounded_dragon.py');need(c.pin(m.OUT/'runtime/run_bounded_dragon.py')['sha256']==plan['original_bounded_Source_pin']['sha256'],'whole original bounded Source');owned.append(c.pin(m.OUT/'runtime/run_bounded_dragon.py'))
 for role in('launcher_Source_pin','Fortran_probe_Source_pin'):
  p=plan[role];q=m.OUT/'sources'/Path(p['path']).name;shutil.copy2(p['path'],q);new=c.pin(q);need(new['sha256']==p['sha256']and new['size_bytes']==p['size_bytes'],'whole small control Sources only');owned.append(new)
 fixtures=[]
 for i,n in enumerate((257,521,1031),1):
  q=m.OUT/'fixtures'/('fixture'+str(i)+'.bin');data=bytes(65+(i*19+j*7)%26 for j in range(n))
  with q.open('xb')as f:f.write(data);f.flush();os.fsync(f.fileno())
  fixtures.append(c.pin(q));owned.append(fixtures[-1])
 casepins={}
 for name in('positive','closed_fd','wrong7','duplicate_inode'):
  q=m.OUT/name/'CASE.json';c.write(q,dict(schema='NONSCIENTIFIC_READONLY_FD_EXEC_FIXTURE_CASE_V1',case=name,fixture_full_pins=fixtures,scientific_data=False));casepins[name]=c.pin(q);owned.append(casepins[name])
 runner=full.OwnRSSSerialExecutor(m.OUT,1800-(time.monotonic()-start),'FD_control',resources);need(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==m.OUT/'runtime/run_bounded_dragon.py','same original single-child executor, no override/retry')
 compiler=plan['Fortran_compiler_pin']['path'];probe=m.OUT/'build/readonly_fd_native_startup_control';compile_cmd=[compiler,*plan['original_Fortran_flags'],'-J'+str(m.OUT/'build'),'-c',str(m.OUT/'sources/readonly_fd_native_startup_control.UNREADY.f90'),'-o',str(m.OUT/'build/readonly_fd_native_startup_control.o')]
 # One compiler invocation compiles and links the standalone libc/ISO_C_BINDING probe.
 compile_cmd=[x for x in compile_cmd if x!='-c'];compile_cmd[-1]=str(probe)
 actual=[];first=None;secondary=[];after=None;good=False;native_positive=None;receipts=[];binary=None
 def execute_case(directory,label,cmd,expected):
  check();err=None
  try:runner.execute(directory,label,cmd,600)
  except BaseException as e:err=e
  need(bool(runner.records),'real original runner record required');record=runner.records[-1];wp=m.OUT/(record['label']+'.watchdog.json');lp=m.OUT/(record['label']+'.log');w=m.metadata(c.pin(wp));log=lp.read_text();code=w['returncode']
  need(type(code)is int and code==expected and w['command']==cmd==record['command']and w['limit_failure']is None and w['own_child_only']is True and w['liveness_group_cleanup']is True and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and(expected!=0 or c.pin(lp)['sha256']==record['log_sha256']),'actual original monitor/record.label/raw code/limits/command closure')
  need((expected==0 and err is None and record['status']=='PASS')or(expected!=0 and err is not None and record['status']=='FAILED'),'negative original FAILED status preserved, never relabelled PASS')
  actual.append(dict(label=label,expected_integer_exit_code=expected,actual_integer_exit_code=code,actual_original_record_status=record['status'],actual_watchdog_pin=c.pin(wp),actual_watchdog=w,actual_log_pin=c.pin(lp),negative_refusal_expected=expected!=0,actual_error=None if err is None else repr(err)));check();return log,w
 try:
  execute_case(m.OUT/'build','compile_and_link_non_scientific_probe',compile_cmd,0);binary=c.pin(probe);owned.append(binary)
  for name,code in(('positive',0),('closed_fd',71),('wrong7',1),('duplicate_inode',1)):
   cmd=[str(support.PYTHON),'-B',str(m.OUT/'sources/open_fixture_FDs_then_same_PID_exec.UNREADY.py'),'--case-pin',json.dumps(casepins[name],separators=(',',':')),'--probe-pin',json.dumps(binary,separators=(',',':')),'--case',name];log,w=execute_case(m.OUT/name,name,cmd,code)
   if name in('positive','closed_fd'):
    rp=c.pin(m.OUT/name/'FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json');receipt=m.metadata(rp);need(receipt['PID']==w['pid']==receipt['process_group']and receipt['new_child_spawned']is False and [x['readonly_fd']for x in receipt['fixed_fd_proofs']]==[101,102,103]and [x['real_original_full_pin']for x in receipt['fixed_fd_proofs']]==fixtures,'actual wrapper PID/group equals original monitor child and exact fixture→FD mapping');receipts.append(dict(receipt_pin=rp,receipt=receipt))
    if name=='positive':
     lines=[x.split()for x in log.splitlines()if x.startswith('FD_NATIVE_PID_GROUP_BYTES ')];need('FD_READONLY_EXEC_NATIVE_POSITIVE_V1'in log.splitlines()and len(lines)==1 and list(map(int,lines[0][1:]))==[w['pid'],w['pid'],1809,3],'actual GNU startup samePID/group/complete3 fixture bytes/read-only positive marker');native_positive=dict(PID=w['pid'],process_group=w['pid'],complete_fixture_bytes=1809,fixture_count=3,full_reads_seeks_EOF_and_readonly_EBADF_verified=True)
    else:need('FD_CONTRACT_REFUSAL 71 INHERITED_FD_PRESENT'in log,'closedFD third inherited descriptor actually refused after preceding fixture checks')
   else:
    lines=[json.loads(x)for x in log.splitlines()if x.startswith('{')];need(len(lines)==1 and lines[0]['schema']=='FD_CONTRACT_LAUNCHER_REFUSAL_V1'and lines[0]['PID']==w['pid']and lines[0]['process_group']==w['pid']and lines[0]['native_exec_reached']is False and lines[0]['reason_code']==('CURRENT7_MISMATCH'if name=='wrong7'else'DUPLICATE_DEVICE_INODE'),'exact wrong7/duplicateinode pre-exec refusal only')
  need(len(actual)==len(runner.records)==5 and [x['actual_integer_exit_code']for x in actual]==[0,0,71,1,1],'one compile plus four independent controls once')
  after=check();good=True
 except BaseException as e:first=e
 finally:
  try:after=check()
  except BaseException as e:
   if first is None:first=e
   else:secondary.append(repr(e))
  report=dict(schema='ROOT_NONSCIENTIFIC_READONLY_FD_SAME_PID_EXEC_CONTRACT_CONTROL_REPORT_V1',status='PASS_NONSCIENTIFIC_GNU_STARTUP_READONLY_FD_EXEC_CONTRACT_CONTROLS_ONLY'if good and first is None else'FAILED_NONSCIENTIFIC_FD_CONTROL_NO_RETRY',failure=None if first is None else repr(first),secondary_failures=secondary,source_pin=ps,plan_pin=pb,independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,complete_source_file_pins=plan['complete_source_file_pins'],actual_fixture_full_pins=fixtures,actual_new_probe_binary_pin=binary,actual_stage_checks=actual,original_stage_records=runner.records,actual_native_positive_proof=native_positive,actual_launcher_before_exec_receipts=receipts,actual_child_integer_exit_codes=[x['actual_integer_exit_code']for x in actual],negative_original_FAILED_records_preserved=(len(actual)==5 and all(x['actual_original_record_status']=='FAILED'for x in actual if x['negative_refusal_expected'])),expected_negative_refusals_do_not_qualify_production_launcher=True,original_guard_class='OwnRSSSerialExecutor',original_guard_MRO_unchanged=True,complete_joint_roots=roots,original_caps=m.CAPS,bounded_new_output_reservation_bytes=m.OUTPUT_BOUND,bounded_own_Source_metadata_receipts_bytes=m.SOURCE_BOUND,resources_before=before,resources_after=after,whole_new_output_pins=[c.pin(q)for q in sorted(m.OUT.rglob('*'))if q.is_file()],all_three_tiny_fixture_fullpins_unchanged=(good and first is None),final_report_resource_check_passed=False,**m.FALSE)
  q=m.OUT/'Root_actual_non_scientific_readonly_FD_exec_control_summary.json';need(len((json.dumps(report,indent=2)+'\n').encode())<2*2**20,'control summary2MiB within32');c.write(q,report)
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
