"""Production PACK positive-only FD entry. No negative/test mode or input-copy facility."""
import argparse,fcntl,hashlib,json,os,stat,sys
from pathlib import Path
FD_NUMBERS=(101,102,103)
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-current-A1-B2-A3-complete18-PACK-readonly-FD-20261016-v1')
EXPECTED_CATALOG_PIN={'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_full370_real_operator_control_source_v1_20261015/current_selected_A1_B2_A3_readonly_producer_catalog_v1_20261016/CURRENT_SELECTED_A1_B2_A3_READONLY_BYTE_CATALOG.json', 'sha256': '6cd317c560230c57cff60c06da96df96cc690195ef12843579828ed66e16b917', 'size_bytes': 73816, 'identity': [16777229, 50953321, 33188, 1, 73816, 1792081036832338117, 1792081036832338117]}
EXPECTED_RUNTIME_PIN={'path': '/Users/wen/spot/validation/artifacts/axial-material-current-B-plane2-minimal-runtime-complete71-build-only-20261016-v1/sources/runtime/Dragon', 'sha256': 'ec53b2aa6686a532c5663b6aea24011dd56c759ca5ede24a3f93832d86c5d9be', 'size_bytes': 11010040, 'identity': [16777229, 50955628, 33261, 1, 11010040, 1792082077672239123, 1792082077672239123]}
class FDRefusal(RuntimeError):pass

def need(v,code):
 if v is not True:raise FDRefusal(code)

def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def metadata(p):
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_uid==os.getuid()and s.st_nlink==1 and identity(s)==p['identity']and s.st_size==p['size_bytes']and not any(x.is_symlink()for x in(q,*q.parents)),'METADATA_CURRENT7')
 raw=q.read_bytes();catalog_role=p==EXPECTED_CATALOG_PIN
 need(((catalog_role and len(raw)==73816)or(not catalog_role and len(raw)<65536))and hashlib.sha256(raw).hexdigest()==p['sha256']and identity(q.lstat())==p['identity'],'METADATA_FULL_SHA');return json.loads(raw)

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
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest-pin',required=True);a=ap.parse_args();pm=json.loads(a.manifest_pin);manifest=metadata(pm)
 need(Path(pm['path'])==OUT/'pack/READONLY_FD_MANIFEST.json'and manifest['schema']=='CURRENT_A1_B2_A3_PRODUCTION_PACK_READONLY_FD_MANIFEST_V1'and manifest['FD_control_Root0_and_post0_closed']is True,'EXACT_POSITIVE_PACK_MANIFEST')
 need(manifest['catalog_pin']==EXPECTED_CATALOG_PIN and manifest['runtime_pin']==EXPECTED_RUNTIME_PIN,'EXACT_APPROVED_CATALOG_AND_CURRENT_BUILT_RUNTIME')
 catalog=metadata(EXPECTED_CATALOG_PIN);producers=catalog['producers'];expected=[(1,'A','R64WARM-A-V1 '),(2,'B','R64WARM-B-V1 '),(3,'A','R64-A3-WARM1 ')]
 need([(x['plane'],x['material'],x['expected_case'])for x in producers]==expected,'EXACT_A1_B2_A3_ORDER_CASES')
 rows=[x['archive']for x in producers];need(rows==manifest['ordered_three_real_archive_full_pins']and all(p is not None for p in manifest['actual_FD_control_four_closure_pins']),'THREE_EXACT_CURRENT_COLD_ARCHIVES_AND_REAL_CONTROL_CLOSURE')
 proof=prepare_readonly_fds(rows);rp=EXPECTED_RUNTIME_PIN;q=Path(rp['path']);st=q.lstat();need(q.is_absolute()and stat.S_ISREG(st.st_mode)and st.st_uid==os.getuid()and st.st_nlink==1 and bool(st.st_mode&0o111)and identity(st)==rp['identity']and st.st_size==rp['size_bytes']and not any(p.is_symlink()for p in(q,*q.parents)),'CURRENT_EXACT_ALREADY_BUILT_DRAGON_NO_COMPILE')
 receipt=dict(schema='PRODUCTION_A1_B2_A3_PACK_READONLY_FD_BEFORE_EXEC_RECEIPT_V1',manifest_pin=pm,catalog_pin=EXPECTED_CATALOG_PIN,runtime_pin=rp,PID=os.getpid(),process_group=os.getpgrp(),fixed_fd_proofs=proof,exact_native_exec_argv=[str(q)],new_child_spawned=False,symlinks_or_hardlinks_created=False,scientific_archive_copies_written=False,negative_control_modes_available=False,scientific_archive_body_SHA_repeated_by_launcher=False)
 with(OUT/'pack/PRODUCTION_FD_LAUNCHER_BEFORE_EXEC_RECEIPT.json').open('x')as f:json.dump(receipt,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 os.execv(str(q),[str(q)])
if __name__=='__main__':main()
