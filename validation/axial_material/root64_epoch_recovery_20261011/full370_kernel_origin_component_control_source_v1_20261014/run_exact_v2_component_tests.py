"""Select exact v2 imports explicitly, then execute unchanged six-test Source bytes."""
import argparse,hashlib,importlib.util,json,os,runpy,stat,sys
from pathlib import Path
sys.dont_write_bytecode=True
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def exact(p):
 q=Path(p['path']);s=q.lstat()
 if not q.is_absolute()or any(a.is_symlink()for a in(q,*q.parents))or not stat.S_ISREG(s.st_mode)or s.st_nlink!=1 or identity(s)!=p['identity']:raise RuntimeError('exact component ordinary current7')
 raw=q.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=p['sha256']or identity(q.lstat())!=p['identity']:raise RuntimeError('exact component full Source bytes')
 return raw
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--plan',required=True);ap.add_argument('--test',required=True);a,remaining=ap.parse_known_args()
 plan=json.loads(Path(a.plan).read_bytes());bindings=plan['explicit_component_import_bindings'];tests=[plan['angular_test_Source_pin'],plan['multigroup_test_Source_pin']]
 test=next(p for p in tests if p['path']==a.test)
 for row in bindings:
  name=row['module'];p=row['pin'];exact(p)
  if name in sys.modules:raise RuntimeError('component module already imported '+name)
  spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
  if Path(m.__file__).absolute()!=Path(p['path']):raise RuntimeError('actual component module binding '+name)
 exact(test);sys.argv=[a.test,*remaining]
 try:runpy.run_path(a.test,run_name='__main__')
 finally:
  exact(test)
  for row in bindings:
   exact(row['pin'])
   if Path(sys.modules[row['module']].__file__).absolute()!=Path(row['pin']['path']):raise RuntimeError('component module changed '+row['module'])
if __name__=='__main__':main()
