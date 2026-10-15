"""Prepare the minimum Boolean fix in a new Source namespace only.

Does not create SF/HF/CLI, invoke a compiler, launch a control, read SCI or
rewrite any v1 evidence. Root alone publishes once after the same-round peer.
"""
import ast,hashlib,json,os,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent;REC=BASE.parent;OLD=REC/'saved_MT5_NX_raw32_yield_source_v1_20261014';ART=REC.parents[1]/'artifacts'
OUT=ART/'axial-material-saved-MT5-NX-raw32-producer-yield-diagnostic-20261014-v2'
FALSE=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
def require(ok,msg):
 if type(ok)is not bool or not ok:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();require(p.is_absolute()and not any(a.is_symlink()for a in(p,*p.parents))and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'exact ordinary Source/metadata')
 with p.open('rb')as f:
  require(identity(os.fstat(f.fileno()))==identity(s),'opened7')
  h=hashlib.file_digest(f,'sha256').hexdigest();require(identity(os.fstat(f.fileno()))==identity(s),'EOF7')
 require(identity(p.lstat())==identity(s),'path7');return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=identity(s))
def read(p):
 p=pin(p);require(p['size_bytes']<8*2**20,'small bounded metadata');v=json.loads(Path(p['path']).read_bytes());require(pin(p['path'])==p,'same exact metadata');return v,p
def current(p):
 q=Path(p['path']);s=q.lstat();require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and q.is_absolute()and identity(s)==p['identity']and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(a.is_symlink()for a in(q,*q.parents)),'declared complete current7, SCI payload not read')
def write(p,v):
 with Path(p).open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def unique(rows):
 d={}
 for p in rows:
  if p['path']in d:require(d[p['path']]==p,'same path inconsistent PF')
  d[p['path']]=p
 return list(d.values())
def exact_change(raw,before,after):
 require(raw.count(before)==1,'one exact Source statement substitution')
 new=raw.replace(before,after);require(new.replace(after,before)==raw,'whole Source inverse recovers original bytes exactly');return new
def write_source(p,raw):
 ast.parse(raw,filename=str(p))
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
def main():
 require(not os.path.lexists(OUT),'fresh corrected validation namespace')
 targets=['check_saved_MT5_NX_raw32_and_yield.py','run_saved_MT5_NX_raw32_yield_original_guard.py','write_once_Root_final_NX_SF_HF_CLI.py','PLAN.json','WHOLE_SOURCE_BYTE_INVERSE.json','REQUIRE_ARGUMENT_SOURCE_TYPE_AUDIT.json','SOURCE_REVIEW_READY.json']
 require(not any(os.path.lexists(BASE/n)for n in targets),'Source preparation once, no prior files overwritten')
 plan,pplan=read(OLD/'PLAN.json');tool,ptool=read(OLD/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')
 failed,pfailed=read(ART/'axial-material-saved-MT5-NX-raw32-producer-yield-diagnostic-20261014-v1/Root_actual_saved_MT5_NX_raw32_yield_summary.json')
 require(len(plan['complete_joint_roots'])==34 and plan['source_only']is True and plan['goal_complete']is False,'same latest prior34 exact plan')
 require(tool['observed_closed']is True and type(tool['original_integer_exit_code'])is int and tool['original_integer_exit_code']==1 and type(tool['actual_terminal_return']['exit_code'])is int and tool['actual_terminal_return']['exit_code']==1 and tool['actual_terminal_return'].get('session_id')is None,'original actual failed validation1, preserved')
 require(failed['status']=='ACTUAL_SAVED_MT5_NX_PRODUCER_FAILED_NO_RETRY'and failed['failure']=="RuntimeError('own-child stage failed; no retry')"and failed['goal_complete']is False,'original failure, no mathematical result relabeled')
 watchdog=failed['actual_watchdog_full_pin'];log=failed['actual_log_full_pin']
 if watchdog is None or log is None:
  for p in failed['complete_output_pins']:
   if p['path'].endswith('.watchdog.json'):watchdog=p
   if p['path'].endswith('.log'):log=p
 require(type(watchdog)is dict and type(log)is dict,'original failed child watchdog/log preserved')
 watch,pwatch=read(watchdog['path']);require(pwatch==watchdog and type(watch['returncode'])is int and watch['returncode']==1 and watch['limit_failure']is None,'actual child1/no resource-limit failure')
 require(pin(log['path'])==log,'whole original failure log');lograw=Path(log['path']).read_text();require("require(nonzero,'original DRAGR would omit all-zero NX')"in lograw and 'ValueError: original DRAGR would omit all-zero NX'in lograw,'actual strict Boolean guard rejected list before any report')
 oldchild=OLD/'check_saved_MT5_NX_raw32_and_yield.py';oldhost=OLD/'run_saved_MT5_NX_raw32_yield_original_guard.py'
 c0=oldchild.read_bytes();c1=exact_change(c0,b"require(nonzero,'original DRAGR would omit all-zero NX')",b"require(bool(nonzero),'original DRAGR would omit all-zero NX')")
 c2=exact_change(c1,b"len(roots)==34 and len(set(roots))==34,'bound kernel complete32 plus NX Source/output, no cumulative reset'",b"len(roots)==36 and len(set(roots))==36,'bound prior34 plus corrected NX Source/output, no cumulative reset'")
 h0=oldhost.read_bytes();h1=exact_change(h0,b"len(plan['complete_joint_roots'])==34,'complete kernel32 plus NX Source/owning output, no reset'",b"len(plan['complete_joint_roots'])==36,'complete prior34 plus corrected NX Source/owning output, no reset'")
 child=BASE/oldchild.name;host=BASE/oldhost.name;write_source(child,c2);write_source(host,h1)
 pub_old=OLD/'write_once_Root_final_NX_SF_HF_CLI.py';prefix=pub_old.read_text().split('def main():',1)[0]
 body=Path(__file__).read_text().split('# ROOT_FINAL_PUBLISHER_BODY\n',1)[1].split('# END_ROOT_FINAL_PUBLISHER_BODY',1)[0]
 body=body[body.index("PUBLISHER_BODY = r'''")+len("PUBLISHER_BODY = r'''"):body.rindex("'''")]
 publisher=BASE/pub_old.name;write_source(publisher,(prefix+body).encode())
 audit=[]
 for p in(child,host,publisher,Path(__file__).absolute()):
  source=p.read_text();tree=ast.parse(source,filename=str(p))
  for node in ast.walk(tree):
   if isinstance(node,ast.Call)and isinstance(node.func,ast.Name)and node.func.id=='require':
    arg=node.args[0];audit.append(dict(source_file=p.name,line=node.lineno,expression=ast.get_source_segment(source,arg),AST_type=type(arg).__name__))
    if isinstance(arg,ast.Name):require(arg.id in ('all_exact','good'),'no bare list/string guard argument; only proven Boolean all_exact/good')
 write(BASE/'REQUIRE_ARGUMENT_SOURCE_TYPE_AUDIT.json',dict(schema='NX_CORRECTED_REQUIRE_ARGUMENT_SOURCE_TYPE_AUDIT_V2',source_only=True,require_calls=audit,bare_all_exact_proof='initialized True; exact=(replay==original_raw) is bool; all_exact=all_exact and exact remains bool',bare_good_proof='verified initialized False then set True; good=verified and first.error is None remains bool',name_short_circuit_proof="name and name not in names returns bool for a valid nonempty name; empty name returns empty string and correctly remains a rejection path",nonzero_guard_proof='bool(nonzero) accepts every nonempty selected list and still rejects an actual all-zero vector',**FALSE))
 inverse=dict(schema='NX_MINIMUM_BOOL_FIX_AND_CUMULATIVE_DIMENSION_WHOLE_SOURCE_INVERSE_V2',source_only=True,original_child_pin=pin(oldchild),new_child_pin=pin(child),original_host_pin=pin(oldhost),new_host_pin=pin(host),original_scientific_statement_proof_pin=plan['original_statement_byte_proof_pin'],child_changes=[dict(before="require(nonzero,'original DRAGR would omit all-zero NX')",after="require(bool(nonzero),'original DRAGR would omit all-zero NX')",role='strict Boolean condition only'),dict(before="len(roots)==34 and len(set(roots))==34,'bound kernel complete32 plus NX Source/output, no cumulative reset'",after="len(roots)==36 and len(set(roots))==36,'bound prior34 plus corrected NX Source/output, no cumulative reset'",role='metadata cumulative dimensions only')],host_changes=[dict(before="len(plan['complete_joint_roots'])==34,'complete kernel32 plus NX Source/owning output, no reset'",after="len(plan['complete_joint_roots'])==36,'complete prior34 plus corrected NX Source/owning output, no reset'",role='metadata cumulative dimensions only')],whole_inverse_verified=True,original_producer_formulas_math_masks_cutoffs_unchanged=True,original_guard_helpers_and_preamble_exact_bytes_unchanged=True,**FALSE)
 write(BASE/'WHOLE_SOURCE_BYTE_INVERSE.json',inverse)
 newplan=dict(plan);newplan['planned_actual_output_root']=str(OUT);newplan['complete_joint_roots']=plan['complete_joint_roots']+[str(BASE),str(OUT)]
 require(len(newplan['complete_joint_roots'])==36 and len(set(newplan['complete_joint_roots']))==36,'retain every prior34 plus corrected Source/output')
 newplan.update(selected_prior_failed_NX34_plan_pin=pplan,selected_prior_original_failure_Root_tool_pin=ptool,selected_prior_failed_guarded_summary_pin=pfailed,selected_prior_failed_watchdog_pin=watchdog,selected_prior_failed_child_log_pin=log,minimum_bool_fix_whole_inverse_pin=pin(BASE/'WHOLE_SOURCE_BYTE_INVERSE.json'),corrected_new_namespace_validation_entry=True,original_no_retry_per_validation_entry_unchanged=True)
 write(BASE/'PLAN.json',newplan);pnewplan=pin(BASE/'PLAN.json')
 oldsf,psf=read(OLD/'FINAL_SOURCE_FREEZE.json');oldhf,phf=read(OLD/'FINAL_HOST_FREEZE.json');oldcli,pcli=read(OLD/'FINAL_ROOT_REVIEWABLE_CLI.json')
 sources=unique([pin(child),pin(host),pin(publisher),pin(Path(__file__).absolute()),pin(BASE/'WHOLE_SOURCE_BYTE_INVERSE.json'),pin(BASE/'REQUIRE_ARGUMENT_SOURCE_TYPE_AUDIT.json')]+[p for p in oldsf['complete_source_file_pins']if '/saved_MT5_NX_raw32_yield_source_v1_20261014/'not in p['path']])
 failure_peer_pins=[pin(OLD/'actual_failure_postverify_20261014'/n)for n in ('REVIEW.json','TRUE_TOOL_RETURNS.json')]
 deps=unique([p for p in oldhf['dependencies']if '/saved_MT5_NX_raw32_yield_source_v1_20261014/'not in p['path']]+sources+[pnewplan,pplan,ptool,pfailed,watchdog,log,psf,phf,pcli]+failure_peer_pins)
 for p in deps:current(p)
 ready=dict(schema='SAVED_MT5_NX_BOOL_FIX_SOURCE_REVIEW_READY_V2',source_only=True,control_plan_pin=pnewplan,child_source_pin=pin(child),host_source_pin=pin(host),final_publisher_Source_pin=pin(publisher),complete_source_file_pins=sources,dependencies=deps,selected_Source_pins=unique(sources+deps),original_caps=plan['original_caps'],original_complete_ENV_Python_B_prefix=oldcli['argv'][:11],whole_inverse_AST_type_audit_passed=True,actual_business_started=False,Root_final_publication_executed=False,original_failed_guarded_entry_retained=True,**FALSE)
 write(BASE/'SOURCE_REVIEW_READY.json',ready);print(json.dumps(dict(status='NX_BOOL_FIX_SOURCE_PREPARATION_ONLY',ready_pin=pin(BASE/'SOURCE_REVIEW_READY.json'),**FALSE)))
if __name__=='__main__':main()

# ROOT_FINAL_PUBLISHER_BODY
PUBLISHER_BODY = r'''def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('peer-review','peer-tools','generation'):
  for suffix in('summary','sha256','seven-id'):ap.add_argument('--'+role+'-'+suffix,required=True)
 a=ap.parse_args()
 def arg(role):
  n=role.replace('-','_');q=Path(getattr(a,n+'_summary'));p=dict(path=str(q),sha256=getattr(a,n+'_sha256'),size_bytes=q.stat().st_size,identity=json.loads(getattr(a,n+'_seven_id')));return read(p),p
 peer,pp=arg('peer-review');tools,pt=arg('peer-tools');generation,pg=arg('generation')
 targets=[BASE/n for n in('FINAL_SOURCE_FREEZE.json','FINAL_HOST_FREEZE.json','FINAL_ROOT_REVIEWABLE_CLI.json','FINAL_PUBLICATION_RECEIPT.json')]
 require(not any(os.path.lexists(q)for q in targets),'Root final once only, no overwrite/republish')
 pready=pin(BASE/'SOURCE_REVIEW_READY.json');ready=read(pready)
 require(ready['source_only']is True and ready['actual_business_started']is False and ready['Root_final_publication_executed']is False and ready['final_publisher_Source_pin']==pin(Path(__file__).absolute()),'same reviewed corrected Source-only publisher')
 selected=ready['selected_Source_pins']+[pready,pg]
 for p in selected:current(p)
 require(peer['source_only']is True and type(peer['status'])is str and peer['status'].startswith('PASS')and peer['failure']is None and all(peer[k]is False for k in FALSE)and all(contains(peer,p)for p in selected),'same passing Source-only review and full corrected Source/generation PF scope')
 t=tools['actual_review_return'];require(tools['observed_closed']is True and type(tools['original_integer_exit_code'])is int and tools['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None and type(t['output'])is str and json.loads(t['output'].strip().splitlines()[-1])['review_pin']==pp,'genuine original peer closed0/stdout exact PF')
 gt=generation['actual_Source_preparation_return'];require(generation['observed_closed']is True and type(generation['original_integer_exit_code'])is int and generation['original_integer_exit_code']==0 and type(gt['exit_code'])is int and gt['exit_code']==0 and gt.get('session_id')is None and type(gt['output'])is str,'genuine corrected Source-generation closed0')
 gd=json.loads(gt['output'].strip().splitlines()[-1]);require(gd['ready_pin']==pready and gd['status']=='NX_BOOL_FIX_SOURCE_PREPARATION_ONLY'and all(gd[k]is False for k in FALSE),'exact new corrected ready true generation stdout; no business')
 plan=read(ready['control_plan_pin']);require(len(plan['complete_joint_roots'])==36 and plan['original_caps']==ready['original_caps'],'same complete prior34 plus corrected Source/output, original caps')
 for p in ready['dependencies']:current(p)
 proof=dict(peer_review_pin=pp,peer_true_tools_pin=pt,Source_generation_true_tools_pin=pg,selected_Source_only_ready_pin=pready,root_same_round_Source_only_publication=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)
 flags=dict(business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,complete_reaction_authority_qualified=False,physical_neutron_balance_qualified=False,unreduced_reference_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 sf=dict(schema='SAVED_MT5_NX_RAW32_YIELD_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,control_plan_pin=ready['control_plan_pin'],child_source_pin=ready['child_source_pin'],complete_source_file_pins=ready['complete_source_file_pins']+[pready],original_caps=ready['original_caps'],Root_same_round_peer_and_generation_proof=proof,**flags)
 write(targets[0],sf);psf=pin(targets[0])
 hf=dict(schema='SAVED_MT5_NX_RAW32_YIELD_HOST_SOURCE_ONLY_FREEZE_V1',candidate_executed=False,source_only=True,selected_source_freeze_pin=psf,host_source_pin=ready['host_source_pin'],dependencies=unique(ready['dependencies']+[pready,pp,pt,pg]),original_caps=ready['original_caps'],Root_same_round_peer_and_generation_proof=proof,**flags)
 write(targets[1],hf);phf=pin(targets[1])
 prefix=ready['original_complete_ENV_Python_B_prefix'];require(type(prefix)is list and len(prefix)==11,'exact original env/Python/-B prefix')
 argv=prefix+[ready['host_source_pin']['path'],'--source-freeze-summary',psf['path'],'--source-freeze-sha256',psf['sha256'],'--source-freeze-seven-id',json.dumps(psf['identity'],separators=(',',':')),'--host-freeze-summary',phf['path'],'--host-freeze-sha256',phf['sha256'],'--host-freeze-seven-id',json.dumps(phf['identity'],separators=(',',':'))]
 cli=dict(schema='SAVED_MT5_NX_RAW32_YIELD_REVIEWABLE_CLI_SOURCE_ONLY_V1',argv=argv,source_freeze_pin=psf,host_freeze_pin=phf,planned_actual_output_root=plan['planned_actual_output_root'],Root_same_round_peer_and_generation_proof=proof,**flags);write(targets[2],cli)
 for p in selected:current(p)
 for p in(pp,pt,pg):require(pin(p['path'])==p,'same exact peer/generation metadata after Root Source-only publication')
 receipt=dict(schema='ROOT_ONCE_FINAL_CORRECTED_NX_SOURCE_PUBLICATION_ONLY_V2',source_only=True,selected_Source_pins=selected,peer_and_generation_proof=proof,final_source_freeze_pin=psf,final_host_freeze_pin=phf,final_CLI_pin=pin(targets[2]),original_failed_entry_unchanged=True,**flags);write(targets[3],receipt)
 print(json.dumps(dict(status='ROOT_FINAL_CORRECTED_NX_SOURCE_PUBLICATION_ONLY',receipt_pin=pin(targets[3]),**flags)))
if __name__=='__main__':main()
'''
# END_ROOT_FINAL_PUBLISHER_BODY
