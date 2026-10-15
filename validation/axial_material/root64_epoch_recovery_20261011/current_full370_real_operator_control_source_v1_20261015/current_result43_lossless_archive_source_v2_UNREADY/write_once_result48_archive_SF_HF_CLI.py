"""Source-only Root oncepublisher. Never launches archive or reads plain result bytes."""
import argparse,hashlib,importlib.util,json,os,stat,sys,time
from pathlib import Path

BASE=Path(__file__).absolute().parent

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def bootstrap(q):
 s=q.lstat();raw=q.read_bytes()
 if not(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()
  and s.st_size<8*2**20 and identity(q.lstat())==identity(s)
  and not any(x.is_symlink()for x in(q,*q.parents))):raise RuntimeError('bounded private bootstrap metadata')
 return json.loads(raw),dict(path=str(q),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools','generation'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();started=time.monotonic()
 with(BASE/'ROOT_PUBLICATION_CLAIM.json').open('x')as f:
  json.dump(dict(schema='RESULT48_ARCHIVE_ROOT_ONCE_PUBLICATION_CLAIM_V1',PID=os.getpid(),argv=__import__('sys').argv,started=started,business_executed=False,retries=0),f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 ready,pReady=bootstrap(BASE/'SOURCE_REVIEW_READY.json');pc=ready['common_source_pin'];q=Path(pc['path']);s=q.lstat();raw=q.read_bytes()
 if identity(s)!=pc['identity']or hashlib.sha256(raw).hexdigest()!=pc['sha256']:raise RuntimeError('whole prepared common Source')
 spec=importlib.util.spec_from_file_location('result48_archive_oncepublisher_common',q);c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);c.current7(pc)
 c.require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
  and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==c.PYTHON,
  'original Source publication interpreter/env/thread1')
 def argument(role):
  n=role.replace('-','_');ids=json.loads(getattr(a,n+'_seven_id'))
  return dict(path=getattr(a,n+'_summary'),sha256=getattr(a,n+'_sha256'),size_bytes=ids[4],identity=ids)
 pp=argument('peer-review');pt=argument('peer-tools');pg=argument('generation')
 c.require(ready['schema']=='RESULT48_LOSSLESS_ARCHIVE_SOURCE_REVIEW_READY_V1'
  and ready['source_only']is True and ready['actual_business_started']is False
  and ready['Root_final_publication_executed']is False
  and c.pin(Path(__file__).absolute())==ready['final_publisher_Source_pin'],'same exact prepared Source-only publisher')
 peer=c.metadata(pp);generation=c.true0(pg,'actual_Source_preparation_return','ready_pin',pReady)
 gd=json.loads(generation['actual_Source_preparation_return']['output'].splitlines()[-1])
 c.require(gd['status']=='RESULT48_LOSSLESS_ARCHIVE_SOURCE_PREPARATION_ONLY'
  and gd['plan_pin']==ready['execution_binding_pin']and all(gd[k]is False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')),'actual original Sourcegen0 only')
 c.true0(pt,'actual_review_return','review_pin',pp)
 selected=ready['selected_Source_pins']+[pReady,pg]
 c.require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')
  and peer['binding_pin']==ready['execution_binding_pin']and all(c.contains(peer,p)for p in selected)
  and all(peer[k]is False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')),
  'same-round independent genuine Source review covers complete selected metadata and Rootgen0')
 for p in selected:c.require(c.pin(p['path'])==p,'Root fullEOF selected Source/metadata; no old plain bodies')
 for p in ready['old48_plain_and_retained66_current7_only_pins']:c.current7(p)
 plan=c.metadata(ready['execution_binding_pin']);out=c.admit(plan)
 resources=c.Resources(plan,started,600);resources.check()
 c.require(not os.path.lexists(out)and not any(os.path.lexists(BASE/n)for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json','ROOT_ARCHIVE_EXECUTION_CLAIM.json')),'once publication; fresh business root, never overwrite/retry')
 proof=dict(selected_ready_pin=pReady,Source_generation_true_tools_pin=pg,peer_review_pin=pp,peer_true_tools_pin=pt,
  selected_Source_scope_only=True,Root_same_round_Source_publication_only=True)
 def write(name,value):
  raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();c.require(len(raw)<8*2**20 and c.own_bytes(BASE)+len(raw)<c.SOURCE_CAP,'whole Source each8MiB/combined16MiB')
  return c.write_new(BASE/name,value,8*2**20)
 sf=dict(schema='RESULT43_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1',source_only=True,candidate_executed=False,
  execution_binding_pin=ready['execution_binding_pin'],complete_source_file_pins=ready['complete_source_file_pins'],
  original_caps=c.CAPS,Root_same_round_peer_and_generation_proof=proof,**c.FALSE)
 psf=write('FINAL_SOURCE_FREEZE.json',sf)
 hf=dict(schema='RESULT43_LOSSLESS_ARCHIVE_HOST_FREEZE_V1',source_only=True,candidate_executed=False,
  selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],common_source_pin=pc,
  independent_Source_review_pin=pp,independent_Source_review_tools_pin=pt,original_caps=c.CAPS,
  Source_generation_true_tools_pin=pg,selected_Source_pins=selected,Root_same_round_peer_and_generation_proof=proof,**c.FALSE)
 phf=write('FINAL_HOST_FREEZE.json',hf)
 prefix=ready['original_complete_ENV_Python_B_prefix'];c.require(len(prefix)==11,'whole original ENV/Python/-B prefix')
 argv=prefix+[ready['host_source_pin']['path'],'--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],
  '--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':')),'--host-freeze-summary',phf['path'],
  '--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))]
 c.require(len(argv)==24,'exact original24 argv structural contract')
 pcli=write('FINAL_ROOT_REVIEWABLE_CLI.json',dict(schema='RESULT48_ARCHIVE_REVIEWABLE_CLI_SOURCE_ONLY_V1',argv=argv,
  source_freeze_pin=psf,host_freeze_pin=phf,planned_actual_output_root=str(out),complete_joint_roots=plan['complete_joint_roots'],
  exec_command_sandbox_permissions='require_escalated',permission_reason='Preserve unchanged original owning child PS/liveness/RSS guard',
  Root_same_round_peer_and_generation_proof=proof,**c.FALSE))
 for p in selected+[pp,pt]:c.require(c.pin(p['path'])==p,'same selected Source/metadata after publication')
 resources.check()
 receipt=dict(schema='ROOT_ONCE_RESULT48_ARCHIVE_SOURCE_PUBLICATION_ONLY_V1',source_only=True,
  final_source_freeze_pin=psf,final_host_freeze_pin=phf,final_CLI_pin=pcli,selected_Source_pins=selected,
  Root_same_round_peer_and_generation_proof=proof,Source_published_without_business=True,**c.FALSE)
 pr=write('FINAL_PUBLICATION_RECEIPT.json',receipt);resources.check()
 print(json.dumps(dict(status='ROOT_ONCE_RESULT48_ARCHIVE_SOURCE_PUBLICATION_ONLY',receipt_pin=pr,
  business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)

if __name__=='__main__':main()
