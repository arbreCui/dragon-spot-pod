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
  and all(type(v)is int for v in p['identity'])and (p['identity'][3]==1 or p['path']=='/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15'and p['sha256']=='0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492'and p['identity'][3]==2)and p['identity'][4]==p['size_bytes'],'complete strict PF')
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
 for role in('peer-review','peer-tools','generation','retirement'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args()
 def arg(role):
  n=role.replace('-','_');q=Path(getattr(a,n+'_summary'));p=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=q.stat().st_size,identity=json.loads(getattr(a,n+'_seven_id')));return read(p),p
 peer,pp=arg('peer-review');tools,pt=arg('peer-tools');generation,pg=arg('generation');retirement,pr=arg('retirement')
 targets=[BASE/n for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')]
 require(not any(os.path.lexists(q)for q in targets),'Root final once only, no overwrite/republish')
 pready=pin(BASE/'SOURCE_REVIEW_READY.json');ready=read(pready)
 require(ready['source_only']is True and ready['actual_business_started']is False and ready['Root_final_publication_executed']is False and ready['final_publisher_Source_pin']==pin(Path(__file__).absolute()),'same reviewed corrected Source-only publisher')
 selected=ready['selected_Source_pins']+[pready,pg]
 for p in selected:current(p)
 require(peer['source_only']is True and type(peer['status'])is str and peer['status'].startswith('PASS')and peer['failure']is None and all(peer[k]is False for k in FALSE)and all(contains(peer,p)for p in selected),'same passing Source-only review and full corrected Source/generation PF scope')
 t=tools['actual_review_return'];require(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and type(t['output'])is str and json.loads(t['output'].strip().splitlines()[-1])['review_pin']==pp,'genuine original peer closed0/stdout exact PF')
 gt=generation['actual_Source_preparation_return'];require(generation['observed_closed']is True and type(generation['original_integer_exit_code'])is int and generation['original_integer_exit_code']==0 and type(gt['exit_code'])is int and gt['exit_code']==0 and gt.get('session_id')is None and type(gt['output'])is str,'genuine corrected Source-generation closed0')
 gd=json.loads(gt['output'].strip().splitlines()[-1]);require(gd['ready_pin']==pready and gd['status']=='EIGHT_FUEL_FINITE18_SCAT_SOURCE_PREPARATION_ONLY'and all(gd[k]is False for k in FALSE),'exact new corrected ready true generation stdout; no business')
 plan=read(ready['control_plan_pin']);require(len(plan['complete_joint_roots'])==51 and plan['original_caps']==ready['original_caps'],'same prior49 exact prefix plus Source/output51, original caps')
 for p in ready['dependencies']:current(p)
 require(pr==plan['actual_precise_retirement_receipt_pin']and pr['path']==plan['precise_required_actual_retirement_receipt_path']and retirement['schema']=='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'and retirement['mode']=='execute'and retirement['status']=='RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'and retirement['failure']is None and retirement['actual_released_bytes']==405417320 and retirement['actual_released_pins']==retirement['exact_target_pins']and len(retirement['actual_released_pins'])==4,'precise actual Root retirement receipt, no source substitute')
 for retired in retirement['actual_released_pins']:require(not os.path.lexists(retired['path']),'exact retired spool paths absent')
 proof=dict(actual_precise_retirement_receipt_pin=pr,peer_review_pin=pp,peer_true_tools_pin=pt,Source_generation_true_tools_pin=pg,selected_Source_only_ready_pin=pready,root_same_round_Source_only_publication=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)
 flags=dict(finite18_replayed=False,temperature_interpolation_replayed=False,physics_qualified=False,scientific_accuracy_qualified=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 sf=dict(schema='EIGHT_FUEL_FINITE18_SCAT_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,control_plan_pin=ready['control_plan_pin'],complete_source_file_pins=ready['complete_source_file_pins']+[pready],original_caps=ready['original_caps'],Root_same_round_peer_and_generation_proof=proof,**flags)
 write(targets[0],sf);psf=pin(targets[0])
 hf=dict(schema='EIGHT_FUEL_FINITE18_SCAT_HOST_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],dependencies=unique(ready['dependencies']+[pready,pp,pt,pg,pr]),actual_precise_retirement_receipt_pin=pr,explicit_cumulative_metadata_file_pins=unique(plan['explicit_cumulative_metadata_file_pins']+[pready,pp,pt,pg,pr]),original_caps=ready['original_caps'],Root_same_round_peer_and_generation_proof=proof,**flags)
 write(targets[1],hf);phf=pin(targets[1])
 prefix=ready['original_complete_ENV_Python_B_prefix'];require(type(prefix)is list and len(prefix)==11,'exact original env/Python/-B prefix')
 argv=prefix+[ready['host_source_pin']['path'],'--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],'--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':')),'--host-freeze-summary',phf['path'],'--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))]
 cli=dict(schema='EIGHT_FUEL_FINITE18_SCAT_REVIEWABLE_CLI_SOURCE_ONLY_V1',argv=argv,source_freeze_pin=psf,host_freeze_pin=phf,planned_actual_output_root=plan['planned_actual_output_root'],Root_same_round_peer_and_generation_proof=proof,**flags);write(targets[2],cli)
 for p in selected:current(p)
 for p in(pp,pt,pg,pr):require(pin(p['path'])==p,'same exact peer/generation metadata after Root Source-only publication')
 receipt=dict(schema='ROOT_ONCE_EIGHT_FUEL_FINITE18_SCAT_SOURCE_PUBLICATION_ONLY_V1',source_only=True,selected_Source_pins=selected,peer_and_generation_proof=proof,final_source_freeze_pin=psf,final_host_freeze_pin=phf,final_CLI_pin=pin(targets[2]),original_failed_entry_unchanged=True,**flags);write(targets[3],receipt)
 print(json.dumps(dict(status='ROOT_FINAL_EIGHT_FUEL_FINITE18_SCAT_SOURCE_PUBLICATION_ONLY',receipt_pin=pin(targets[3]),**flags)))
if __name__=='__main__':main()
