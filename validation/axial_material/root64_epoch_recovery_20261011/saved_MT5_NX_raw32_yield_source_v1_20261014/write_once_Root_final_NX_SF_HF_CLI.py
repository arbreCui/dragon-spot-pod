"""Root-only final Source publication after peer and true generation review.

Never launches the host/child. All preliminary Source files remain unchanged.
Three required complete PF triples identify peer review, its original typed
tool return, and the retained actual Source-generation tool returns.
"""
import argparse,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
FALSE=('business_executed','compiler_executed','numerical_executed','files_deleted')
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'literal regular single-link metadata')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'opened metadata7')
  digest=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF metadata7')
 require(identity(p.lstat())==identity(s),'metadata path7')
 return dict(path=str(p),sha256=digest,size_bytes=s.st_size,identity=identity(s))
def current(p):
 require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['path'])is str
  and type(p['sha256'])is str and len(p['sha256'])==64 and all(c in '0123456789abcdef'for c in p['sha256'])
  and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7
  and all(type(v)is int for v in p['identity'])and p['identity'][3]==1 and p['identity'][4]==p['size_bytes'],'complete strict PF')
 q=Path(p['path']);require(q.is_absolute()and not any(a.is_symlink()for a in(q,*q.parents))
  and identity(q.lstat())==p['identity']and stat.S_ISREG(q.lstat().st_mode),'exact current7, no data payload read')
def read(p):
 current(p);require(p['size_bytes']<8*2**20 and pin(p['path'])==p,'bounded wholemetadata SHA/current7')
 v=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same final metadata fullPF');return v
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def unique(rows):
 table={}
 for p in rows:
  if p['path']in table:require(table[p['path']]==p,'same path inconsistent fullPF')
  table[p['path']]=p
 return list(table.values())
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools','generation'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args()
 def arg(role):
  n=role.replace('-','_');q=Path(getattr(a,n+'_summary'));p=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=q.stat().st_size,identity=json.loads(getattr(a,n+'_seven_id')));return read(p),p
 peer,pp=arg('peer-review');tools,pt=arg('peer-tools');generation,pg=arg('generation')
 targets=[BASE/n for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')]
 require(not any(os.path.lexists(q)for q in targets),'Root final once only, no overwrite/republish')
 ready2,pready2=read(pin(BASE/'SOURCE_REVIEW_READY_v2.json')),pin(BASE/'SOURCE_REVIEW_READY_v2.json')
 require(ready2['source_only']is True and ready2['actual_business_started']is False and ready2['final_publisher_Source_pin']==pin(Path(__file__).absolute()),'same reviewed final publisher Source')
 selected=ready2['selected_Source_pins']+[pready2];require(ready2['actual_Source_generation_tool_returns_pin']==pg,'exact original actual Source generation evidence')
 for p in selected:current(p)
 require(peer['source_only']is True and type(peer['status'])is str and peer['status'].startswith('PASS')and peer['failure']is None
  and all(peer[k]is False for k in FALSE)and all(contains(peer,p)for p in selected),'same Source-only passing peer, exact complete selected PF scope')
 t=tools['actual_review_return'];require(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int
  and tools['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None
  and type(t['output'])is str and json.loads(t['output'].strip().splitlines()[-1])['review_pin']==pp,'genuine peer original typed closed0/stdout exact PF')
 require(generation['schema']=='ACTUAL_SAVED_NX_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_V1'and generation['source_only']is True
  and all(generation[k]is False for k in FALSE)and generation['root_same_round_publication_performed']is False,'original preparation evidence only')
 success=generation['second_corrected_actual_source_generation_return'];failure=generation['first_failed_actual_source_generation_return']
 require(type(success['exit_code'])is int and success['exit_code']==0 and success.get('session_id')is None and type(success['output'])is str
  and type(failure['exit_code'])is int and failure['exit_code']==1 and failure.get('session_id')is None and type(failure['output'])is str,'actual first failure1 and corrected preparation0 retained')
 original_ready=ready2['selected_original_READY_pin'];require(json.loads(success['output'].strip().splitlines()[-1])['ready_pin']==original_ready,'true generation stdout exact original ready PF')
 prelim_sf=ready2['preliminary_source_freeze_pin'];prelim_hf=ready2['preliminary_host_freeze_pin'];prelim_cli=ready2['preliminary_CLI_pin']
 sf=read(prelim_sf);hf=read(prelim_hf);cli=read(prelim_cli)
 require(hf['selected_source_freeze_pin']==prelim_sf and cli['source_freeze_pin']==prelim_sf and cli['host_freeze_pin']==prelim_hf,'original preliminary Source bindings')
 for p in hf['dependencies']:current(p)
 proof=dict(peer_review_pin=pp,peer_true_tools_pin=pt,Source_generation_true_tools_pin=pg,selected_final_publisher_ready_pin=pready2,selected_original_READY_pin=original_ready,preliminary_SF_HF_CLI_pins=[prelim_sf,prelim_hf,prelim_cli],root_same_round_Source_only_publication=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)
 sf['Root_same_round_peer_and_generation_proof']=proof
 sf['complete_source_file_pins']=unique(sf['complete_source_file_pins']+[ready2['final_publisher_Source_pin'],pready2])
 write(targets[0],sf);psf=pin(targets[0])
 hf['selected_source_freeze_pin']=psf;hf['Root_same_round_peer_and_generation_proof']=proof
 hf['dependencies']=unique(hf['dependencies']+[ready2['final_publisher_Source_pin'],pready2,pp,pt,pg,original_ready,prelim_sf,prelim_hf,prelim_cli]);write(targets[1],hf);phf=pin(targets[1])
 argv=cli['argv'];host=hf['host_source_pin']['path'];require(len(argv)>11 and argv[11]==host,'original complete env/Python/-B argv prefix')
 cli['argv']=argv[:11]+[host,'--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],'--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':')),'--host-freeze-summary',phf['path'],'--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))]
 cli['source_freeze_pin']=psf;cli['host_freeze_pin']=phf;cli['Root_same_round_peer_and_generation_proof']=proof;write(targets[2],cli)
 for p in selected:current(p)
 for p in(pp,pt,pg):require(pin(p['path'])==p,'same closed review/generation metadata after Source publication')
 receipt=dict(schema='ROOT_ONCE_FINAL_SAVED_NX_SOURCE_PUBLICATION_ONLY_V1',source_only=True,selected_Source_pins=selected,peer_and_generation_proof=proof,final_source_freeze_pin=psf,final_host_freeze_pin=phf,final_CLI_pin=pin(targets[2]),preliminary_files_not_modified=True,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,goal_complete=False);write(targets[3],receipt)
 print(json.dumps(dict(status='ROOT_FINAL_NX_SOURCE_PUBLICATION_ONLY',receipt_pin=pin(targets[3]),business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,goal_complete=False)))
if __name__=='__main__':main()
