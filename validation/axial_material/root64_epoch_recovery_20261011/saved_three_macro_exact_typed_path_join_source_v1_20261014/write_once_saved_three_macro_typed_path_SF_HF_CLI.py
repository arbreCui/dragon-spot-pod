"""Publish exact reviewed Source metadata once; no scientific execution."""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def require(v,t):
 if type(v)is not bool or not v:raise RuntimeError(t)
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(x.is_symlink()for x in(p,*p.parents))and s.st_size<64*2**20,'ordinary bounded metadata');raw=p.read_bytes();require(ids(p.lstat())==ids(s),'metadata beforeafter7');return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=s.st_size,identity=ids(s))
def read(p):require(pin(p['path'])==p,'full exact metadata PF');return json.loads(Path(p['path']).read_bytes())
def has(v,p):return v==p or isinstance(v,dict)and any(has(x,p)for x in v.values())or isinstance(v,list)and any(has(x,p)for x in v)
def write(p,d):
 with p.open('xb')as f:f.write((json.dumps(d,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();proof={}
 for role in('peer-review','peer-tools'):
  k=role.replace('-','_');p=pin(getattr(a,k+'_summary'));require(p['sha256']==getattr(a,k+'_sha256')and p['identity']==json.loads(getattr(a,k+'_seven_id')),'exact peer triple');proof[role]=p
 peer=read(proof['peer-review']);tool=read(proof['peer-tools']);z=tool['actual_review_return'];require(peer['source_only']is True and peer['failure']is None and peer['status'].startswith('PASS')and all(peer[k]is False for k in('business_executed','compiler_executed','numerical_executed','files_deleted')),'same round Source only');require(tool['observed_closed']is True and type(tool['original_integer_exit_code'])is int and tool['original_integer_exit_code']==0 and type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==proof['peer-review'],'genuine Source review0')
 rp=pin(BASE/'SOURCE_REVIEW_READY.json');ready=read(rp);selected=[ready[k]for k in('host_source_pin','child_source_pin','original_admission_Source_pin','original_adapter_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin')]+[rp];require(all(has(peer,p)for p in selected),'same round nine exact selected Source fullPF');plan=read(ready['plan_pin'])
 table={}
 for p in selected+list(proof.values())+plan['source_dependency_pins']:
  require(p['path']not in table or table[p['path']]==p,'one exact current fullPF per path');table[p['path']]=p
 deps=list(table.values())
 for p in deps:
  q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and ids(s)==p['identity']and not any(x.is_symlink()for x in(q,*q.parents)),'current dependency exact7')
 code=[ready[k]for k in('host_source_pin','child_source_pin','original_admission_Source_pin','original_adapter_Source_pin')];sp=write(BASE/'COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_SOURCE_ONLY_FREEZE.json',dict(schema='COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_SOURCE_ONLY_FREEZE_V1',source_only=True,control_plan_pin=ready['plan_pin'],child_source_pin=ready['child_source_pin'],complete_source_file_pins=code,same_round_review_pin=proof['peer-review'],same_round_tools_pin=proof['peer-tools'],actual_comparison_report_pin=None,physics_qualified=False))
 hp=write(BASE/'COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_HOST_SOURCE_ONLY_FREEZE.json',dict(schema='COMPLETE_SAVED_THREE_MACRO_TYPED_PATH_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sp,dependencies=deps+[sp],actual_duplicate_physical_release_proof_pin=plan['actual_duplicate_physical_release_proof_pin'],actual_duplicate_physical_release_Root_tool_pin=plan['actual_duplicate_physical_release_Root_tool_pin'],actual_duplicate_release_schema='EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_RECEIPT_V1',physics_qualified=False))
 old=read(plan['original_recipe_pin']);argv=old['argv'][:11]+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',sp),('host-freeze',hp)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 require(len(argv)==24,'original env11 and host plus two actual triples');cp=write(BASE/'ROOT_REVIEWABLE_SAVED_THREE_MACRO_TYPED_PATH_ACTUAL24_ARGV.json',dict(schema='ROOT_REVIEWABLE_SAVED_THREE_MACRO_TYPED_PATH_ACTUAL_ARGV_V1',argv=argv,shell_safe_command=shlex.join(argv),source_freeze_pin=sp,host_freeze_pin=hp,physics_qualified=False));fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='SAVED_TYPED_PATH_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY',Source_freeze_pin=sp,Host_freeze_pin=hp,CLI_pin=cp,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
