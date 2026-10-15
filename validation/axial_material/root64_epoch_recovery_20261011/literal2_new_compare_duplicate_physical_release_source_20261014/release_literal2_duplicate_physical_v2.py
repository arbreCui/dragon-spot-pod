"""Release exactly two independently verified duplicate private physical streams."""
import argparse,hashlib,json,os,stat,subprocess,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
R=Path('/Users/wen/spot')
PREFIX=R/'validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence'
EXPECTED_SHA='b9b72ad2f281ca6b4c881fc3734412f68debcdd80ff03ceec4372b02786b4c60'
def require(v,msg):
 if type(v)is not bool or not v:raise RuntimeError(msg)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 q=Path(p['path']);s=q.lstat();require(q.is_absolute()and stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in(q,*q.parents))and identity(s)==p['identity'],'exact ordinary current7 '+str(q));return q

def full(p):
 q=current(p);require(p['identity'][3]==1 and q.lstat().st_uid==os.getuid(),'single-link owned release data and authority');h=hashlib.sha256();fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  require(identity(os.fstat(fd))==p['identity'],'opened full7')
  with os.fdopen(fd,'rb',closefd=False)as f:
   while True:
    b=f.read(1024*1024)
    if not b:break
    h.update(b)
  require(identity(os.fstat(fd))==p['identity'],'closed full7')
 finally:os.close(fd)
 current(p);require(h.hexdigest()==p['sha256'],'full EOF SHA');return json.loads(q.read_bytes())if q.suffix=='.json'else None

def write(p,d):
 with p.open('xb')as f:f.write((json.dumps(d,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
 s=p.lstat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s))
def no_open(files):
 for p in files:
  z=subprocess.run(['/usr/sbin/lsof','-nP','-F','pfn','--',p['path']],capture_output=True,text=True,timeout=30)
  require(z.returncode==1 and not z.stdout and not z.stderr,'exact duplicate/owner not open '+p['path'])
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--plan-sha256',required=True);ap.add_argument('--plan-seven-id',required=True);ap.add_argument('--mode',choices=['check','execute'],required=True);a=ap.parse_args();p=BASE/'PLAN.json';s=p.lstat();planpf=dict(path=str(p),sha256=a.plan_sha256,size_bytes=s.st_size,identity=json.loads(a.plan_seven_id));plan=full(planpf);post=full(plan['post_review_pin']);tools=full(plan['post_tools_pin'])
 require(post['status']=='PASS_ACTUAL_COMPARE_THREE_V7_FAILURE_FACTS_POSTVERIFICATION'and post['failure']is None and post['actual_Root_integer_exit_code']==1,'original genuine Root1 evidence retained')
 for role in('actual_review_return','actual_postverification_return'):
  z=tools[role];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==plan['post_review_pin'],'genuine solepost closed0')
 owner=plan['retained_complete_owner_pin'];targets=plan['target_pins'];require(owner['path']==str(PREFIX/'A1/physical.jsonl')and [p['path']for p in targets]==[str(PREFIX/'A2/physical.jsonl'),str(PREFIX/'A3/physical.jsonl')],'only three fixed literal paths')
 require(all(p['sha256']==EXPECTED_SHA and p['size_bytes']==34371817 for p in[owner,*targets])and sum(p['size_bytes']for p in targets)==68743634,'exact two duplicate byte totals')
 for p in[owner,*targets]:require(p in post['actual_complete_new_output_pins'],'independent fullEOF authority');full(p)
 for p in plan['fixed_current_pins']+plan['retained_new_output_pins']:current(p)
 no_open([owner,*targets]);receipt=BASE/('ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_RECEIPT.json'if a.mode=='execute'else'EXACT_LITERAL2_DUPLICATE_PHYSICAL_READONLY_RECEIPT.json');require(not receipt.exists(),'once unique receipt')
 deleted=[]
 try:
  if a.mode=='execute':
   for p in targets:
    no_open([p]);current(p);fd=os.open(Path(p['path']).parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:
     require(identity(os.stat('physical.jsonl',dir_fd=fd,follow_symlinks=False))==p['identity'],'immediate target exact7');os.unlink('physical.jsonl',dir_fd=fd);os.fsync(fd)
    finally:os.close(fd)
    deleted.append(p)
   for p in plan['fixed_current_pins']+plan['retained_new_output_pins']:current(p)
   full(owner);require(all(not os.path.lexists(p['path'])for p in targets),'exact two absent')
  result=dict(schema='EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_RECEIPT_V1',status='ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASED_ONLY'if a.mode=='execute'else'EXACT_LITERAL2_READONLY_READY',plan_pin=planpf,post_review_pin=plan['post_review_pin'],retained_complete_owner_pin=owner,exact_target_pins=targets,actual_released_pins=deleted,actual_released_bytes=sum(p['size_bytes']for p in deleted),retained_new_output_pins=plan['retained_new_output_pins'],all_original_archives_SQLite_pools_reports_logs_retained=True,original_Root_exit_code_retained=1,original_resource_failure_retained=True,physics_qualified=False,goal_complete=False,failure=None)
  rp=write(receipt,result)
 except BaseException as e:
  write(BASE/'ACTUAL_EXACT_LITERAL2_DUPLICATE_PHYSICAL_RELEASE_FAILED_RECEIPT.json',dict(failure=repr(e),actual_released_pins=deleted,original_Root_exit_code_retained=1,physics_qualified=False));raise
 print(json.dumps(dict(status=result['status'],receipt_pin=rp,actual_released_bytes=result['actual_released_bytes'],physics_qualified=False)),flush=True)
if __name__=='__main__':main()
