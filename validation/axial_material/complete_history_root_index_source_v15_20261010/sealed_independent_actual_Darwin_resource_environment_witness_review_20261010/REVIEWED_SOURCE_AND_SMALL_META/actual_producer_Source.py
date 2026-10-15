import hashlib,json,os,stat,sys,resource,time
from pathlib import Path

PY=Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
MOD=Path('/Users/wen/miniforge3/envs/openmc-dev/lib/python3.12/lib-dynload/resource.cpython-312-darwin.so')
SHA='cbd0358d5dfb6a5271a7e645118a36d0537b49e84452a2bcd7d26a73eb131164'
SEMANTICS='DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')

def identity(p):
 s=p.lstat()
 return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
 p=Path(p)
 assert p.is_absolute() and '..' not in p.parts
 for q in [*reversed(p.parents),p]:
  st=q.lstat()
  assert not stat.S_ISLNK(st.st_mode)
  assert q==p or stat.S_ISDIR(st.st_mode)
 before=identity(p)
 assert stat.S_ISREG(before[2]) and type(before[3]) is int and before[3]>0
 with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==before
 return {'path':str(p),'sha256':sha,'size_bytes':before[4],'identity':before}

assert __debug__ and sys.flags.optimize==0
assert sys.platform=='darwin' and sys.executable==str(PY)
assert resource.__file__==str(MOD)
assert all(os.environ.get(k)=='1' for k in THREADS)
start=time.monotonic()
producer=pin(Path(__file__))
py_before=pin(PY);mod_before=pin(MOD)
assert mod_before['sha256']==SHA and mod_before['size_bytes']==53552
raw=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
assert type(raw) is int and raw>=0
assert pin(PY)==py_before and pin(MOD)==mod_before and pin(Path(__file__))==producer
assert time.monotonic()-start<30
body={'schema':'ROOT_ACTUAL_DARWIN_RESOURCE_SELF_RUSAGE_DIAGNOSTIC_ENVIRONMENT_QUERY_V1','source_only':True,'platform':sys.platform,'diagnostic_dependency_verified':True,'actual_python_fullpin':py_before,'actual_resource_module_fullpin':mod_before,'actual_environment_producer_Source_fullpin':producer,'actual_python_version':sys.version,'actual_python_optimization':sys.flags.optimize,'actual_thread_environment':{k:os.environ[k] for k in THREADS},'self_ru_maxrss_native_bytes_observed':raw,'ru_maxrss_semantics':SEMANTICS,'query_count':1,'whole_BUILD_qualified':False,'whole_INPUT_qualified':False,'native_or_science_qualified':False,'candidate_guard_helper_compile_material_or_numeric_executed':False,'elapsed_seconds':time.monotonic()-start}
print(json.dumps(body,ensure_ascii=False,allow_nan=False))
