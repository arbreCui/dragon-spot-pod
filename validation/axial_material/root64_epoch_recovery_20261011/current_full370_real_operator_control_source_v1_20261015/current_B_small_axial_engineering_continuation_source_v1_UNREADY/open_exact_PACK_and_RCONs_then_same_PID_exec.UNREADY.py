"""Positive-only current PACK+two plane-RCON readonly FD entry; no test modes."""
import argparse,fcntl,hashlib,json,os,stat
from pathlib import Path
class FDRefusal(RuntimeError):pass
FD_NUMBERS=(101,102,103)
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-B-small-axial-engineering-continuation-20261016-v1')
EXPECTED_RUNTIME_PIN={'path': '/Users/wen/spot/validation/artifacts/axial-material-current-B-plane2-minimal-runtime-complete71-build-only-20261016-v1/sources/runtime/Dragon', 'sha256': 'ec53b2aa6686a532c5663b6aea24011dd56c759ca5ede24a3f93832d86c5d9be', 'size_bytes': 11010040, 'identity': [16777229, 50955628, 33261, 1, 11010040, 1792082077672239123, 1792082077672239123]}
EXPECTED_ORDERED_FD_PINS=[{'path': '/Users/wen/spot/validation/artifacts/axial-material-current-A1-B2-A3-complete18-PACK-readonly-FD-20261016-v1/pack/initial_pack.xsm', 'sha256': 'e2ec2a195f680d630f21aa521c142732dd178249fc32358d72d3563e80f33d09', 'size_bytes': 470641008, 'identity': [16777229, 50959929, 33152, 1, 470641008, 1792084082533840782, 1792084082533840782]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-A1-B2-A3-complete18-PACK-readonly-FD-20261016-v1/pack/plane1_rcon.xsm', 'sha256': '641f1a32e6a9478ceb6001112bc4c08d9a6fca8d7e5a82331b6d2ebe8daba0b3', 'size_bytes': 820, 'identity': [16777229, 50959930, 33152, 1, 820, 1792084082557629409, 1792084082557629409]}, {'path': '/Users/wen/spot/validation/artifacts/axial-material-current-A1-B2-A3-complete18-PACK-readonly-FD-20261016-v1/pack/plane2_rcon.xsm', 'sha256': 'bf1a75c186f15fce0c3346c0167f13d3e947c9ec3763bcaea5fcaab8519f7cfa', 'size_bytes': 820, 'identity': [16777229, 50959931, 33152, 1, 820, 1792084082557653035, 1792084082557653035]}]
def need(v,code):
 if v is not True:raise FDRefusal(code)


def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


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


def metadata(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes']and s.st_size<65536 and not any(x.is_symlink()for x in(q,*q.parents)),'MANIFEST_CURRENT7')
 raw=q.read_bytes();need(hashlib.sha256(raw).hexdigest()==p['sha256']and identity(q.lstat())==p['identity'],'MANIFEST_FULL_SHA');return json.loads(raw)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest-pin',required=True);a=ap.parse_args();pm=json.loads(a.manifest_pin);v=metadata(pm);label=v['stage_label']
 need(label in('initial','axial')and Path(pm['path'])==OUT/'context'/(label+'.FD_manifest.json')and v['schema']=='CURRENT_B_ENGINEERING_PACK_RCON_FD_MANIFEST_V1'and v['PACK_Root0_and_independent_post0_closed']is True,'EXACT_POSITIVE_CONTEXT_MANIFEST')
 need(v['ordered_exact_PACK_RCON1_RCON2_full_pins']==EXPECTED_ORDERED_FD_PINS and v['runtime_pin']==EXPECTED_RUNTIME_PIN and len(v['actual_PACK_four_closure_pins'])==4 and all(p is not None for p in v['actual_PACK_four_closure_pins']),'EXACT_ALREADY_PROVED_CURRENT_PACK_RCON_ROLES')
 proof=prepare_readonly_fds(EXPECTED_ORDERED_FD_PINS);rp=EXPECTED_RUNTIME_PIN;q=Path(rp['path']);s=q.lstat();need(identity(s)==rp['identity']and s.st_size==rp['size_bytes']and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and bool(s.st_mode&0o111)and not any(x.is_symlink()for x in(q,*q.parents)),'EXACT_CURRENT_ALREADY_BUILT_RUNTIME')
 receipt=dict(schema='CURRENT_B_ENGINEERING_BEFORE_SAME_PID_EXEC_READONLY_FD_RECEIPT_V1',stage_label=label,manifest_pin=pm,runtime_pin=rp,PID=os.getpid(),process_group=os.getpgrp(),fixed_fd_proofs=proof,exact_native_exec_argv=[str(q)],new_child_spawned=False,negative_control_modes_available=False,scientific_large_input_copies_written=False,symlinks_or_hardlinks_created=False)
 with(OUT/'context'/(label+'.FD_before_exec.json')).open('x')as f:json.dump(receipt,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.execv(str(q),[str(q)])
if __name__=='__main__':main()
