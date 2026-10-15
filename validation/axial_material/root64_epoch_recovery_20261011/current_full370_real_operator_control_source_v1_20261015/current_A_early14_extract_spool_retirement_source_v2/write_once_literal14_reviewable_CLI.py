"""Root-only metadata publisher; it never checks, reads, or deletes target bodies."""
import argparse,hashlib,json,os,shlex,stat
from pathlib import Path
BASE=Path(__file__).absolute().parent
WORKER=BASE/'retire_completed_A_early14_SQL_pool_spools.UNREADY.py'
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(q):
 q=Path(q);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not any(p.is_symlink()for p in(q,*q.parents)),'ordinary Source/metadata file')
 with q.open('rb')as f:
  need(ident(os.fstat(f.fileno()))==ident(s),'metadata opened7');h=hashlib.file_digest(f,'sha256').hexdigest();need(ident(os.fstat(f.fileno()))==ident(s),'metadata EOF7')
 need(ident(q.lstat())==ident(s),'metadata current7');return dict(path=str(q),sha256=h,size_bytes=s.st_size,identity=ident(s))
def read(p):
 need(pin(p['path'])==p and p['size_bytes']<8*2**20,'exact supplied metadata PF bounded8MiB');v=json.loads(Path(p['path']).read_bytes());need(pin(p['path'])==p,'same metadata fullPF');return v
def genuine(v,key,p,output_key):
 t=v[key];need(v['observed_closed']is True and type(v['original_integer_exit_code'])is int and v['original_integer_exit_code']==0 and type(t['exit_code'])is int and t['exit_code']==0 and t.get('session_id')is None,'actual closed typed0')
 need(json.loads(t['output'].strip().splitlines()[-1])[output_key]==p,'actual original stdout binds exact role PF')
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--mode',choices=['check','execute'],required=True);ap.add_argument('--review-pin',required=True);ap.add_argument('--review-tools-pin',required=True);ap.add_argument('--readonly-pin');ap.add_argument('--readonly-tools-pin');a=ap.parse_args()
 author=read(pin(BASE/'AUTHOR_SOURCE_FREEZE.json'));plan=read(author['whole_plan_pin'])
 for p in author['whole_Source_file_pins']:need(pin(p['path'])==p,'all frozen Source intact')
 source=next(p for p in author['whole_Source_file_pins']if p['path']==str(WORKER));pp=author['whole_plan_pin'];pr=json.loads(a.review_pin);pt=json.loads(a.review_tools_pin);review=read(pr);tools=read(pt)
 genuine(tools,'actual_review_return',pr,'review_pin')
 need(review['status'].startswith('PASS')and review['failure']is None and review['source_only']is True and review['source_pin']==source and review['plan_pin']==pp,'same actual independent Source-only review0; no business PASS invented')
 need(plan['actual_new_A_business_completed']is True and plan['actual_new_A_post_complete']is True and len(plan['complete_joint_roots'])==64,'genuine completed A2 binding and full64 prefix')
 argv=plan['original_complete_ENV_Python_B_prefix']+[str(WORKER),'--mode',a.mode]
 for role,p in(('source',source),('plan',pp),('review',pr)):
  argv+=['--'+role+'-summary',p['path'],'--'+role+'-sha256',p['sha256'],'--'+role+'-seven-id',json.dumps(p['identity'],separators=(',',':'))]
 checkpin=None;checktoolspin=None
 if a.mode=='execute':
  need(a.readonly_pin is not None and a.readonly_tools_pin is not None,'actual separate readonly check0 required')
  checkpin=json.loads(a.readonly_pin);checktoolspin=json.loads(a.readonly_tools_pin);check=read(checkpin);ct=read(checktoolspin)
  need(checkpin['path']==str(BASE/'READONLY_RECEIPT.json')and check['status']=='READONLY_READY_EXACT_LITERAL14_COMPLETED_A_DERIVED_SQL_POOLS'and check['failure']is None and check['source_pin']==source and check['plan_pin']==pp and check['peer_review_pin']==pr and check['actual_released_pins']==[]and check['resources_after_original_classes_forced_fresh']is True,'same exact readonly success0, no unlink, fresh original resources')
  genuine(ct,'actual_readonly_return',checkpin,'receipt_pin');need(ct['actual_readonly_permission_mode']=='require_escalated','original actual readonly permission route')
  argv+=['--readonly-receipt-pin',json.dumps(checkpin,separators=(',',':'))]
 outfile=BASE/('ROOT_READONLY_REVIEWABLE_CLI.json'if a.mode=='check'else'ROOT_EXECUTE_REVIEWABLE_CLI.json');need(not os.path.lexists(outfile),'each mode publication once without overwrite')
 v=dict(schema='LITERAL14_ORIGINAL_GUARDED_REVIEWABLE_CLI_V1',mode=a.mode,argv=argv,command=shlex.join(argv),source_pin=source,plan_pin=pp,independent_Source_review_pin=pr,independent_Source_review_tools_pin=pt,actual_readonly_receipt_pin=checkpin,actual_readonly_tools_pin=checktoolspin,Root_actual_exec_command_sandbox_permissions_required='require_escalated',original_caps=plan['original_caps'],business_executed=False,readonly_check_executed=False,retirement_executed=False,numerical_executed=False,files_deleted=False,physics_qualified=False,goal_complete=False)
 raw=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(raw)<8*2**20 and sum(q.stat().st_size for q in BASE.rglob('*')if q.is_file())+len(raw)<16*2**20,'whole retirement Source/metadata16MiB')
 with outfile.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 print(json.dumps(dict(status='LITERAL14_REVIEWABLE_'+a.mode.upper()+'_CLI_PUBLISHED_ONLY',CLI_pin=pin(outfile),checks_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
