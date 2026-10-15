"""Root finite PREP/BUILD Source/META request writer. No candidate/API execution."""
import ast,hashlib,json,os,stat
from pathlib import Path
def pin(p):
 s=p.lstat()
 assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 data=p.read_bytes()
 t=p.lstat()
 identity=lambda x:[x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns]
 assert identity(s)==identity(t)
 return dict(path=str(p),sha256=hashlib.sha256(data).hexdigest(),size_bytes=len(data),identity=identity(t))

def write(p,v):
 with p.open("x") as f: json.dump(v,f,indent=2,allow_nan=False);f.write("\n")


import Root_poststage_Source_META_contract as scope
assert Path(scope.__file__).resolve()==Path(__file__).resolve().parent/'Root_poststage_Source_META_contract.py'
if __name__=='__main__':scope.request_main()
