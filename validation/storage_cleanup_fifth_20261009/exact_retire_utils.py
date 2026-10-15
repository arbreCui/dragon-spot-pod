from pathlib import Path
import hashlib, json, os, stat, subprocess, shutil
ROOT=Path('/Users/wen/spot')
OUT=ROOT/'validation/storage_cleanup_fifth_20261009'
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def digest(p):
 b=identity(p)
 if not stat.S_ISREG(b[2]):raise ValueError(f'not regular: {p}')
 h=hashlib.sha256()
 with p.open('rb') as f:
  st=os.fstat(f.fileno())
  if [st.st_dev,st.st_ino]!=b[:2]:raise ValueError('inode changed')
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 if identity(p)!=b:raise ValueError(f'changed reading {p}')
 return {'path':str(p),'identity':b,'sha256':h.hexdigest(),'bytes':b[3]}
def save(name,v):
 p=OUT/name
 if p.exists():raise ValueError(f'existing evidence {p}')
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def inventory(excluded):
 h=hashlib.sha256();counts={'regular_files':0,'symlinks':0,'directories':0}
 for parent,dirs,files in os.walk(ROOT,followlinks=False):
  dirs.sort();files.sort();dirs[:]=[n for n in dirs if Path(parent)/n!=OUT]
  for n in sorted(dirs+files):
   p=Path(parent)/n
   if str(p) in excluded:continue
   s=p.lstat();rel=str(p.relative_to(ROOT))
   if stat.S_ISLNK(s.st_mode):row=[rel,identity(p),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISDIR(s.st_mode):row=[rel,'directory'];counts['directories']+=1
   elif stat.S_ISREG(s.st_mode):row=[rel,identity(p)];counts['regular_files']+=1
   else:raise ValueError(f'unsupported {p}')
   h.update(json.dumps(row,ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),**counts)
def capacity():
 k=int(subprocess.check_output(['/usr/bin/du','-k','-s',str(ROOT)],text=True).split()[0])
 return {'project_allocated_bytes':k*1024,'disk_free_bytes':shutil.disk_usage(ROOT).free}
def symlink_check(selected):
 rows=[]
 for parent,dirs,files in os.walk(ROOT,followlinks=False):
  for n in dirs+files:
   p=Path(parent)/n
   if p.is_symlink():
    target=p.resolve()
    if str(target) in selected or any(Path(q).is_relative_to(target) for q in selected):raise ValueError(f'link enters candidate {p}')
    rows.append([str(p),os.readlink(p),str(target)])
 return {'count':len(rows),'sha256':hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()}
