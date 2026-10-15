"""Publish only the continuation Source HF/CLI after factual A10 and same-round Source post0."""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
REC=BASE.parent
HF=BASE/'COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_FREEZE.json'
CLI=BASE/'ROOT_REVIEWABLE_EXACT_CLOSED_A10_CONTINUATION_ARGV_20261014.json'
OUTPUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-formal-material-short-FIL-A10-closed-capture-continuation-20261014-v1')
def require(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def pin(path):
 p=Path(path);s=p.lstat();ids=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 require(stat.S_ISREG(s.st_mode)and s.st_size<=64*2**20,'bounded metadata Source file')
 with p.open('rb')as f:raw=f.read()
 require(ids(p.lstat())==ids(s),'whole metadata stable7')
 return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(p):
 require(pin(p['path'])==p,'full Source metadata exactPF');return json.loads(Path(p['path']).read_bytes())
def same7(p):
 q=Path(p['path']);s=q.lstat();require(stat.S_ISREG(s.st_mode)and not any(x.is_symlink()for x in [q,*q.parents])and [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==p['identity'],'all original dependency current7')
def write(p,v):
 with p.open('xb')as f:f.write((json.dumps(v,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
 return pin(p)
def tool0(t,rp):
 require(t['observed_closed']is True and type(t['original_integer_exit_code'])is int and t['original_integer_exit_code']==0,'observed real closed0')
 z=t['actual_review_return'];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==rp,'genuine review tool0 canonical stdout')
def contains(obj,p):
 return obj==p or isinstance(obj,dict)and any(contains(v,p)for v in obj.values())or isinstance(obj,list)and any(contains(v,p)for v in obj)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);roles=['failed-post','failed-post-tools','peer-review','peer-tools']
 for role in roles:
  for suffix in ['summary','sha256','seven-id']:ap.add_argument('--'+role+'-'+suffix,required=True)
 args=ap.parse_args();pins={};d={}
 for role in roles:
  k=role.replace('-','_');p=pin(getattr(args,k+'_summary'));require(p['sha256']==getattr(args,k+'_sha256')and p['identity']==json.loads(getattr(args,k+'_seven_id')),'actual required fullpin '+role);pins[role]=p;d[role]=read(p)
 post=d['failed-post'];peer=d['peer-review'];tool0(d['failed-post-tools'],pins['failed-post']);tool0(d['peer-tools'],pins['peer-review'])
 require(post['schema']=='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'and post['status']=='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'and post['failure']is None and post['actual_material_stage_closed0']is True and post['actual_stage_statuses']==['PASS']and post['actual_context_collection_source_function_verified']is True,'actual A10 stage0 capture-blocked factual authority')
 require(peer['failure']is None and peer['status'].startswith('PASS')and all(post[k]is False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted']),'Source review and original readonly factual post')
 for k in ['actual_review_return','actual_postverification_return']:
  z=d['failed-post-tools'][k];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==pins['failed-post'],'same actual post0')
 ready=read(pin(BASE/'SOURCE_REVIEW_READY.json'));plan=read(ready['plan_pin']);source=ready['host_source_pin'];writer=pin(__file__)
 own=[source,ready['helper_source_pin'],ready['plan_pin'],ready['inverse_pin'],pin(BASE/'SOURCE_REVIEW_READY.json'),writer]
 require(all(contains(peer,p)for p in own),'same round six exact Source pins present in real review')
 original_phase=post['actual_report_pin'];phase=read(original_phase);oldhfpin=post['actual_Host_freeze_pin'];oldhf=read(oldhfpin);oldclipin=post['actual_CLI_pin'];oldcli=read(oldclipin)
 require(oldhfpin==plan['selected_original_Host_freeze_pin']and oldclipin==plan['selected_original_CLI_pin']and oldcli['Host_freeze_pin']==oldhfpin and phase['failure']=='RuntimeError: both real process metadata tools fully pinned'and len(phase['records'])==1 and phase['records'][0]['status']=='PASS','one exact original failure/closed child')
 state=post['actual_collected_A_observation_state']
 require(all(k in state for k in plan['required_cached_state_original_keys'])and state['actual_genuine_material_stage']==phase['records'][0],'actual cached state complete; no Source-time reconstruction')
 hist=post['actual_owned_library_copy_pins_current'];require(type(hist)is list and len(hist)==2 and sum(p['size_bytes']for p in hist)==979740136,'only exact future released private2')
 paths={p['path']:p for p in hist};table={}
 def add(p):
  if p['path']in paths:require(p==paths[p['path']],'exact historical private copy PF');return
  require(p['path']not in table or table[p['path']]==p,'one current canonicalPF per path');table[p['path']]=p
 for p in oldhf['dependencies']+phase['fixed_current_pins']+phase['output_pins']+own+list(pins.values())+[original_phase,oldhfpin,oldclipin,post['actual_Root_true_tool_return_pin'],post['actual_Root_argv_pin'],pin('/usr/sbin/lsof')]:add(p)
 deps=list(table.values())
 for p in deps:same7(p)
 require(not HF.exists()and not CLI.exists()and not OUTPUT.exists(),'one publication/fresh future continuation OUT')
 sf=write(HF,dict(schema='COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_ONLY_FREEZE_V1',host_source=source,dependencies=deps,selected_original_failed_phase_pin=original_phase,selected_original_failed_post_pin=pins['failed-post'],selected_original_failed_post_tools_pin=pins['failed-post-tools'],selected_original_Host_freeze_pin=oldhfpin,selected_original_CLI_pin=oldclipin,same_round_independent_Source_review_pin=pins['peer-review'],same_round_independent_Source_tools_pin=pins['peer-tools'],complete_byte_inverse_pin=ready['inverse_pin'],control_plan_pin=ready['plan_pin'],original_release_function_Source=dict(source_pin=oldhf['host_source'],function_name='release_closed_owned_library_copies',complete_bytes_unchanged=True),original_collect_function_Source=dict(source_pin=oldhf['host_source'],function_name='collect_state',complete_bytes_unchanged=True,not_called_by_continuation=True),future_exact_private_library2_historical_pins=hist,original_root_exit1_retained=True,Dragon_rerun_permitted=False,new_scientific_outputs_permitted=False,source_only=True,continuation_executed=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False))
 chosen={'original-phase':original_phase,'original-Root-tools':post['actual_Root_true_tool_return_pin'],'original-Root-argv':post['actual_Root_argv_pin'],'original-host-freeze':oldhfpin,'original-CLI':oldclipin,'failed-post':pins['failed-post'],'failed-post-tools':pins['failed-post-tools'],'continuation-host-freeze':sf}
 argv=oldcli['exact_argv'][:11]+[source['path']]
 for role,p in chosen.items():argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 argv+=['--output-dir',str(OUTPUT)]
 require(len(argv)==62,'actual parser eight fullpin roles plus output env12 =62')
 cp=write(CLI,dict(schema='ROOT_REVIEWABLE_EXACT_CLOSED_A10_CONTINUATION_SOURCE_ONLY_ARGV_V1',exact_argv=argv,exact_command=shlex.join(argv),Host_freeze_pin=sf,host_source_pin=source,output_root=str(OUTPUT),actual_original_authority_pins=chosen,original_material_child_not_rerun=True,actual_completion_report_pin=None,actual_observation_manifest_pin=None,actual_release_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False))
 for p in deps:same7(p)
 fd=os.open(BASE,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
 print(json.dumps(dict(status='CLOSED_A10_CONTINUATION_OWN_HF_CLI_SOURCE_ONLY_PUBLISHED',Host_freeze_pin=sf,CLI_pin=cp,actual_argv_count=len(argv),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
