"""Once-only Source publication; no native control or scientific payload read."""
import argparse,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
def require(ok,text):
 if type(ok)is not bool or not ok:raise RuntimeError(text)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
 p=Path(path);s=p.lstat();require(p.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_size<64*2**20 and not any(a.is_symlink()for a in(p,*p.parents)),'ordinary bounded Source/metadata')
 with p.open('rb')as f:raw=f.read()
 require(identity(p.lstat())==identity(s),'current7');return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def exact(p):
 require(pin(p['path'])==p,'exact metadata fullPF');return json.loads(Path(p['path']).read_bytes())
def contains(v,p):return v==p or type(v)is dict and any(contains(x,p)for x in v.values())or type(v)is list and any(contains(x,p)for x in v)
def write(path,v):
 with path.open('xb')as f:f.write((json.dumps(v,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(path)
def terminal(t):
 require(type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and type(t['output'])is str,'genuine closed typed terminal0')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools','Source-generation-tools'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args();proof={}
 for role in('peer-review','peer-tools','Source-generation-tools'):
  n=role.replace('-','_');p=pin(getattr(a,n+'_summary'));require(p['sha256']==getattr(a,n+'_sha256')and p['identity']==json.loads(getattr(a,n+'_seven_id')),'exact explicit authority triple');proof[role]=p
 ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json');ready=exact(ready_pin);plan=exact(ready['plan_pin'])
 peer=exact(proof['peer-review']);tools=exact(proof['peer-tools']);terminal(tools['actual_review_return'])
 require(peer['source_only']is True and peer['failure']is None and all(peer[k]is False for k in('business_executed','compiler_executed','numerical_executed','files_deleted'))and tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and json.loads(tools['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']==proof['peer-review'],'same-round genuine Source review0')
 selected=[ready[k]for k in('host_source_pin','control_Fortran_Source_pin','integer_oracle_Source_pin','plan_pin','inverse_pin','Source_author_pin','writer_source_pin')]+[ready_pin]
 require(all(contains(peer,p)for p in selected),'same-round eight selected control Source fullPFs')
 generation=exact(proof['Source-generation-tools']);terminal(generation['actual_Source_preparation_return'])
 require(generation['observed_closed']is True and type(generation['original_integer_exit_code'])is int and generation['original_integer_exit_code']==0 and json.loads(generation['actual_Source_preparation_return']['output'].strip().splitlines()[-1])['ready_pin']==ready_pin,'genuine Source preparation exactready')
 for p in selected:require(pin(p['path'])==p,'selected Source unchanged')
 require(all(plan[k]is None for k in('actual_energy_input_pin','actual_current_control_report_pin','actual_integer_oracle_output_pin','actual_control_object_pin','actual_control_executable_pin')),'no actual controls prefilled')
 deps=selected+list(proof.values())+plan['source_dependency_pins']
 table={}
 for p in deps:
  require(p['path']not in table or table[p['path']]==p,'one canonical current fullPF per path');table[p['path']]=p
 deps=list(table.values())
 for p in deps:
  q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and identity(s)==p['identity']and not any(a.is_symlink()for a in(q,*q.parents)),'all actual dependency current7')
 sf=dict(schema='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,control_plan_pin=ready['plan_pin'],control_Fortran_Source_pin=ready['control_Fortran_Source_pin'],integer_oracle_Source_pin=ready['integer_oracle_Source_pin'],original_caps=plan['original_caps'],complete_byte_inverse_pin=ready['inverse_pin'],selected_Source_pins=selected,same_round_Source_review_pin=proof['peer-review'],same_round_Source_tools_pin=proof['peer-tools'],actual_Source_generation_tool_pin=proof['Source-generation-tools'],actual_current_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 sp=write(BASE/'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE.json',sf)
 hf=dict(schema='COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE_V1',source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,host_source_pin=ready['host_source_pin'],selected_source_freeze_pin=sp,original_caps=plan['original_caps'],dependencies=deps+[sp],actual_current_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 hp=write(BASE/'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE.json',hf)
 previous=exact(plan['original_recipe_pin']);argv=previous['argv_prefix'][:11]+[ready['host_source_pin']['path']]
 for role,p in(('source-freeze',sp),('host-freeze',hp)):argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 require(len(argv)==24,'exact original env11 plus host and two required fullPF triples')
 cli=dict(schema='ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV_V1',argv=argv,source_freeze_pin=sp,host_freeze_pin=hp,host_source_pin=ready['host_source_pin'],planned_actual_output_root=plan['planned_actual_output_root'],is_complete_executable_argv=True,actual_control_report_pin=None,historical_machine_bit_replay=False,physics_qualified=False)
 cp=write(BASE/'ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json',cli)
 fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_SOURCE_SF_HF_CLI24_PUBLISHED_ONLY',Source_freeze_pin=sp,Host_freeze_pin=hp,CLI_pin=cp,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False)),flush=True)
if __name__=='__main__':main()
