"""Non-scientific fixture control only. Negative cases are absent from any future production launcher."""
import argparse,fcntl,hashlib,json,os,stat,sys
from pathlib import Path
FD_NUMBERS=(101,102,103)
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-readonly-FD-same-PID-exec-control-20261016-v1')
class FDRefusal(RuntimeError):pass
def need(v,code):
 if v is not True:raise FDRefusal(code)
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def metadata(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'METADATA_CURRENT7')
 raw=q.read_bytes();need(len(raw)<65536 and hashlib.sha256(raw).hexdigest()==p['sha256']and identity(q.lstat())==p['identity'],'METADATA_FULL_SHA');return json.loads(raw)
def prepare_readonly_fds(rows):
 need(len(rows)==3 and all(set(p)=={'path','sha256','size_bytes','identity'}for p in rows),'EXACT_THREE_FULL_PIN_ROLES');opened=[];proof=[];seen=set()
 for target in FD_NUMBERS:
  try:os.fstat(target)
  except OSError as e:need(e.errno==9,'FD_SLOT_INSPECTION_ERROR')
  else:raise FDRefusal('FD_SLOT_ALREADY_OCCUPIED')
 try:
  for p,target in zip(rows,FD_NUMBERS):
   q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and not any(x.is_symlink()for x in(q,*q.parents)),'EXACT_REAL_REGULAR_INPUT')
   need(identity(s)==p['identity']and s.st_size==p['size_bytes']and len(p['sha256'])==64,'CURRENT7_MISMATCH')
   fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW);opened.append(fd);st=os.fstat(fd);need(identity(st)==p['identity'],'OPENED_CURRENT7_MISMATCH')
   node=(st.st_dev,st.st_ino);need(node not in seen,'DUPLICATE_DEVICE_INODE');seen.add(node)
   need(fcntl.fcntl(fd,fcntl.F_GETFL)&os.O_ACCMODE==os.O_RDONLY,'OPEN_FD_NOT_READONLY');os.dup2(fd,target,inheritable=True)
   need(identity(os.fstat(target))==p['identity']and os.get_inheritable(target)is True and fcntl.fcntl(target,fcntl.F_GETFL)&os.O_ACCMODE==os.O_RDONLY,'FIXED_FD_NOT_SAME_READONLY_FILE')
   need(identity(q.lstat())==p['identity'],'AFTER_DUP_CURRENT7_MISMATCH');proof.append(dict(real_original_full_pin=p,readonly_fd=target,actual_fd_current7=identity(os.fstat(target)),inheritable=True,F_GETFL_access_mode=fcntl.fcntl(target,fcntl.F_GETFL)&os.O_ACCMODE,payload_body_SHA_repeated=False))
  return proof
 finally:
  for fd in opened:
   if fd not in FD_NUMBERS:os.close(fd)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--case-pin',required=True);ap.add_argument('--probe-pin',required=True);ap.add_argument('--case',choices=('positive','closed_fd','wrong7','duplicate_inode'),required=True);a=ap.parse_args()
 try:
  pp=json.loads(a.probe_pin);case=metadata(json.loads(a.case_pin));need(case['schema']=='NONSCIENTIFIC_READONLY_FD_EXEC_FIXTURE_CASE_V1'and case['case']==a.case and case['scientific_data']is False,'ONLY_NONSCIENTIFIC_CASES')
  rows=case['fixture_full_pins'];need(len(rows)==3 and all(Path(p['path']).parent==OUT/'fixtures'for p in rows),'ONLY_THREE_NEW_FIXTURE_PATHS')
  q=Path(pp['path']);need(q==OUT/'build/readonly_fd_native_startup_control'and q.is_file()and identity(q.lstat())==pp['identity']and hashlib.sha256(q.read_bytes()).hexdigest()==pp['sha256'],'EXACT_NEW_NONSCIENTIFIC_PROBE_BINARY')
  if a.case=='wrong7':rows=json.loads(json.dumps(rows));rows[0]['identity'][6]-=1
  if a.case=='duplicate_inode':rows=[rows[0],rows[0],rows[2]]
  proof=prepare_readonly_fds(rows);receipt=dict(schema='READONLY_FD_LAUNCHER_BEFORE_SAME_PID_EXEC_RECEIPT_V1',case=a.case,PID=os.getpid(),process_group=os.getpgrp(),fixed_fd_proofs=proof,scientific_payload_opened=False,new_child_spawned=False,exec_executable_pin=pp,original_path_identity_only_no_payload_SHA=True)
  if a.case=='closed_fd':os.close(FD_NUMBERS[-1]);receipt['intentionally_closed_fd_for_negative_control']=FD_NUMBERS[-1]
  native_argv=[str(q),str(os.getpid()),str(os.getpgrp())];receipt['exact_native_exec_argv']=native_argv
  path=OUT/a.case/'FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json'
  with path.open('x')as f:json.dump(receipt,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
  os.execv(str(q),native_argv)
 except FDRefusal as e:
  print(json.dumps(dict(schema='FD_CONTRACT_LAUNCHER_REFUSAL_V1',case=a.case,reason_code=str(e),PID=os.getpid(),process_group=os.getpgrp(),native_exec_reached=False,scientific_payload_opened=False)),flush=True);raise SystemExit(1)
if __name__=='__main__':main()
