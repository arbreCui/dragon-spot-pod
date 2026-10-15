"""UNREADY archive host draft, using the unchanged actual OwnRSS serial guard."""
import argparse,hashlib,importlib.util,json,os,shutil,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent

def bootstrap(p):
 q=Path(p['path']);s=q.lstat();ids=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if ids!=p['identity']or hashlib.sha256(q.read_bytes()).hexdigest()!=p['sha256']:raise RuntimeError('whole frozen common Source')
 spec=importlib.util.spec_from_file_location('single_B2_physical_directory_archive_common',q);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);m.current7(p);return m

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source-freeze','host-freeze'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();started=time.monotonic()
 claim=BASE/'ROOT_ARCHIVE_EXECUTION_CLAIM.json'
 with claim.open('x')as f:
  json.dump(dict(schema='ROOT_SINGLE_B2_PHYSICAL_DIRECTORY_ARCHIVE_EXCLUSIVE_ONCE_CLAIM_V1',PID=os.getpid(),original_started=started,argv=sys.argv,claim_before_metadata_or_result_body_IO=True,required_permission='require_escalated',retries=0),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 def argument(role):
  name=role.replace('-','_');ids=json.loads(getattr(a,name+'_seven_id'))
  return dict(path=getattr(a,name+'_summary'),sha256=getattr(a,name+'_sha256'),size_bytes=ids[4],identity=ids)
 # This draft has no final freezes. Root cannot enter result-byte IO until Source admission exists.
 psf=argument('source-freeze');phf=argument('host-freeze')
 # Bootstrap pin is carried in independently reviewed HF; the final publisher must bind it exactly.
 q=Path(phf['path']);s=q.lstat();ids=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
 if ids!=phf['identity']or q.stat().st_size>=8*2**20 or hashlib.sha256(q.read_bytes()).hexdigest()!=phf['sha256']:raise RuntimeError('whole HF metadata')
 initial_hf=json.loads(q.read_bytes());c=bootstrap(initial_hf['common_source_pin']);sf=c.metadata(psf);hf=c.metadata(phf)
 c.require(sf['schema']=='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1'
  and hf['schema']=='CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_HOST_FREEZE_V1'
  and hf['selected_source_freeze_pin']==psf and sf['source_only']is True
  and sf['candidate_executed']is False and hf['host_source_pin']['path']==str(Path(__file__).absolute())
  and hf['original_caps']==c.CAPS
  and c.pin(hf['host_source_pin']['path'])==hf['host_source_pin'],'final reviewed Source/host identities')
 pbind=sf['execution_binding_pin'];b=c.metadata(pbind);out=c.admit(b)
 peer=c.metadata(hf['independent_Source_review_pin'])
 c.require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
  and peer['binding_pin']==pbind and all(c.contains(peer,p)for p in sf['complete_source_file_pins']),
  'actual independent Source review covers whole frozen Source and exact binding')
 c.true0(hf['independent_Source_review_tools_pin'],'actual_review_return','review_pin',hf['independent_Source_review_pin'])
 c.require(out.parent==c.ART and not os.path.lexists(out),'fresh sole owning archive root, no retry')
 support=c.source_module(b['original_support_Source_pin'],'B4_products_original_support')
 c.require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
  and all(os.environ.get(k)=='1'for k in support.THREAD_KEYS)
  and Path(sys.executable).resolve()==support.PYTHON,'original unoptimized unprofiled interpreter/thread1')
 # Preload the original import spine; original classes and guard controls remain whole unchanged.
 c.original_resource_modules(b)
 helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'B4_products_original_guard_helper')
 full,production=helper.modules();guard_files=helper.guard_admission(full)
 c.require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)
  and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,
  'unchanged actual OwnRSS class/MRO/origin')
 resources=c.Resources(b,started,1800);before=resources.check()
 c.require(before['complete_joint']['artifact_bytes']+before['explicit_external_metadata_bytes']
  +before['own_open_unlinked_bytes']+c.OUT_CAP+c.SOURCE_CAP<2*2**30,
  'coexisting complete original B2 physical directory ledger plus worst8MiB archive and16MiB Source fit original joint2GiB; no compression assumption')
 sourcepins=sf['complete_source_file_pins']+[hf['host_source_pin'],hf['common_source_pin']]
 for p in sourcepins:c.require(c.pin(p['path'])==p,'whole admitted Source before launch')
 for p in b['all1_plain_pins']+b['retained_current7_pins']:c.current7(p)
 out.mkdir(mode=0o700);runtime=out/'runtime';runtime.mkdir();stage=out/'archive-stage';stage.mkdir()
 shutil.copy2(support.BOUNDED,runtime/'run_bounded_dragon.py')
 c.require(c.pin(runtime/'run_bounded_dragon.py')['sha256']==b['original_bounded_Source_pin']['sha256'],'whole original bounded Source copy')
 runner=full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-started),'archive-stage',resources)
 c.require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources
  and Path(runner.bounded.__file__).resolve()==runtime/'run_bounded_dragon.py','genuine original one-child owning executor')
 failure=None;original_error=None;receipt=None;watch=None;secondary=[];after=None;originals_retained_after=False
 def capture(error,phase):
  nonlocal failure,original_error
  if original_error is None:failure=repr(error);original_error=error
  else:secondary.append(dict(phase=phase,error=repr(error)))
 command=[str(support.PYTHON),'-B',str(BASE/'archive_single_B2_physical_directory_slots.UNREADY.py'),
  '--binding-pin',json.dumps(pbind,separators=(',',':')),'--common-source-pin',json.dumps(hf['common_source_pin'],separators=(',',':')),
  '--expected-parent-pid',str(os.getpid())]
 try:
  runner.execute(stage,'serial_single_B2_physical_directory_byte_archive',command,600)
  c.require(len(runner.records)==1 and runner.records[0]['status']=='PASS','one original guarded child0; no retry')
  watchpath=out/(runner.records[0]['label']+'.watchdog.json');watch=c.metadata(c.pin(watchpath))
  c.require(type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']is None
   and watch['command']==command and watch['rss_cap_mib']==512 and watch['own_child_only']is True
   and watch['liveness_group_cleanup']is True and 0<=watch['sampled_peak_rss_mib']<512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600,
   'genuine original wall/RSS/liveness completion')
  log=out/(runner.records[0]['label']+'.log');lines=log.read_text().splitlines();c.require(len(lines)==1,'one actual complete child receipt')
  receipt=json.loads(lines[0]);child=c.metadata(receipt['report_pin'])
  c.require(child['schema']=='ACTUAL_CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1'
   and child['status']=='SINGLE_B2_PHYSICAL_DIRECTORY_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'
   and child['failure']is None and child['completed_count']==1 and child['binding_pin']==pbind
   and child['all1_original_plain_current7_retained']is True,'complete one-ledger byte archival only, no original plain retirement')
 except BaseException as error:capture(error,'original_guard_or_child_report')
 try:
  for p in b['all1_plain_pins']+b['retained_current7_pins']:c.current7(p)
  originals_retained_after=True
  for p in sourcepins:c.require(c.pin(p['path'])==p,'whole admitted Source after launch')
  after=resources.check()
 except BaseException as error:capture(error,'post_guard_current7_or_resources')
 summary=dict(schema='ACTUAL_CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1',
  status='ACTUAL_CURRENT_B2_SINGLE_PHYSICAL_DIRECTORY_ARCHIVED_ROUNDTRIP_CLOSED0_ORIGINAL_RETAINED'if failure is None else'FAILED_B2_SINGLE_PHYSICAL_DIRECTORY_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED',
  failure=failure,secondary_failures=secondary,original_caps=c.CAPS,source_freeze_pin=psf,host_freeze_pin=phf,binding_pin=pbind,
  actual_child_receipt=receipt,actual_watchdog=watch,records=runner.records,resources_before=before,resources_after=after,
  original_guard_class_and_MRO_unchanged=True,retries=0,all1_original_plain_current7_retained=originals_retained_after,
  archive_complete=failure is None,plain_retirement_allowed=False,independent_archive_post0_required=True,
  complete_joint_roots=b['complete_joint_roots'],wall_seconds=time.monotonic()-started,
  final_report_resource_check_passed=False,**c.FALSE)
 target=out/'Root_actual_single_B2_physical_directory_lossless_archive_summary.json'
 psummary=None
 try:
  psummary=c.write_new(target,summary,2*2**20)
  fresh=resources.check();summary['resources_after_including_summary_bytes']=fresh;summary['final_report_resource_check_passed']=True
  raw=(json.dumps(summary,indent=2,allow_nan=False)+'\n').encode();c.require(len(raw)<2*2**20
   and c.own_bytes(out)-psummary['size_bytes']+len(raw)<c.OUT_CAP,'own host report2MiB and total8MiB before rewrite')
  c.current7(psummary);fd=os.open(target,os.O_WRONLY|os.O_NOFOLLOW)
  with os.fdopen(fd,'wb')as f:
   c.require(c.identity(os.fstat(f.fileno()))==psummary['identity'],'own summary opened exact7 before rewrite')
   f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())
  c.require(c.identity(target.lstat())[:4]==psummary['identity'][:4],'same owning summary inode/link role')
  psummary=c.pin(target);resources.check()
 except BaseException as error:
  capture(error,'owned_report_publication')
  if psummary is not None:
   try:
    summary.update(status='FAILED_B2_SINGLE_PHYSICAL_DIRECTORY_ARCHIVE_NO_RETRY_ORIGINAL_RETAINED',archive_complete=False,
     failure=failure,secondary_failures=secondary,final_report_resource_check_passed=False)
    raw=(json.dumps(summary,indent=2,allow_nan=False)+'\n').encode()
    c.require(len(raw)<2*2**20 and c.own_bytes(out)-psummary['size_bytes']+len(raw)<c.OUT_CAP,'bounded owning failure report')
    c.current7(psummary);fd=os.open(target,os.O_WRONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'wb')as f:
     c.require(c.identity(os.fstat(f.fileno()))==psummary['identity'],'same own report7 for failure facts')
     f.seek(0);f.truncate(0);f.write(raw);f.flush();os.fsync(f.fileno())
   except BaseException as late:secondary.append(dict(phase='failure_report_publication',error=repr(late)))
 if original_error is not None:raise original_error
 print(json.dumps(dict(status=summary['status'],report_pin=psummary,files_deleted=False)),flush=True)

if __name__=='__main__':main()
