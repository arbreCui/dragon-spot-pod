"""Actual small-file os.open/replace/fstat fixtures; no fabricated stat values.
Only isolated AST definitions are executed. No project modules/API/native/ART.
"""
import ast,hashlib,json,os,stat,tempfile
from pathlib import Path
from types import SimpleNamespace
OLD=Path('/private/tmp/axmat-cold-owned-specs-input-intake-draft-20261007/cold_component_input_consumer.py')
NEW=Path('/private/tmp/axmat-cold-owned-specs-input-intake-path-stable-draft-20261007/cold_component_input_consumer.py')
D=NEW.parent
for p,w in [(OLD,'92a82b8dc214ebd9157e1fdac3fc78669e7fdc340f6d3a771334c4fbfdcbfc82'),
 (NEW,'81ceb9daac17747a35c8d874226f47ac5b459ea888df4e2948b229f9bd71bc76')]:
 assert hashlib.sha256(p.read_bytes()).hexdigest()==w
positive=[];negative=[];observations=[]
KEYS=('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink')
def info(s):return {k:getattr(s,k)for k in KEYS}
def extract(p,proxy):
 source=p.read_text();nodes=[n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)and n.name in ('normal','digest')]
 ns=dict(Path=Path,os=proxy,stat=stat,hashlib=hashlib)
 exec(compile(ast.Module(body=nodes,type_ignores=[]),'<isolated real-file byte reader>','exec'),ns)
 return ns['digest']
class RealOS:
 def __init__(self,path,swap,window=None,identical=False):
  self.path=path;self.swap=swap;self.window=window;self.identical=identical;self.calls=0;self.events=[];self.fds=[]
 def __getattr__(self,k):return getattr(os,k)
 def replace(self,where):
  before=self.path.lstat();os.replace(self.swap,self.path);after=self.path.lstat()
  self.events.append(dict(event='actual_os_replace',window=where,pathname_before=info(before),pathname_after=info(after),
   actual_path_bytes_sha256=hashlib.sha256(self.path.read_bytes()).hexdigest()))
 def open(self,path,flags):
  fd=os.open(path,flags);self.fds.append(fd)
  self.events.append(dict(event='actual_os_open',fd=fd,opened_fd=info(os.fstat(fd))))
  if self.window=='after_os_open_before_first_fstat':self.replace(self.window)
  return fd
 def fstat(self,fd):
  actual=os.fstat(fd);self.calls+=1;self.events.append(dict(event='actual_fstat',ordinal=self.calls,fd=fd,signature=info(actual)))
  if self.window=='after_final_fstat_before_post_pathname'and self.calls==2:self.replace(self.window)
  return actual
 def read(self,fd,n):
  raw=os.read(fd,n)
  if self.window=='inside_read_after_first_fstat'and raw:
   self.window=None;self.replace('inside_read_after_first_fstat')
  return raw
 def close(self,fd):os.close(fd)
def case(base,reader,window,identical=False):
 p=base/'input.bin';swap=base/'swap.bin';p.write_bytes(b'ORIGINAL\x00INPUT!')
 swap.write_bytes(p.read_bytes()if identical else b'CHANGED!\x00INPUT!')
 wanted=hashlib.sha256(p.read_bytes()).hexdigest();proxy=RealOS(p,swap,window,identical)
 fn=extract(reader,proxy)
 try:r=fn(p);accepted=True;error=None
 except (ValueError,FileNotFoundError)as e:r=None;accepted=False;error=dict(type=type(e).__name__,message=str(e))
 row=dict(reader_sha256=hashlib.sha256(reader.read_bytes()).hexdigest(),window=window,identical_replacement_bytes=identical,
  actual_acceptance=accepted,expected_original_sha256=wanted,returned=r,error=error,actual_events=proxy.events,
  final_path_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 observations.append(row)
 return row
with tempfile.TemporaryDirectory(prefix='axmat-real-pathname-stability-',dir='/private/tmp')as t:
 base=Path(t)
 for reader in (OLD,NEW):
  row=case(base,reader,None);assert row['actual_acceptance']and row['returned'][0]==row['expected_original_sha256']
  positive.append('normal byte read exact '+reader.name+row['reader_sha256'][:8])
 for window in ('after_os_open_before_first_fstat','after_final_fstat_before_post_pathname'):
  old=case(base,OLD,window);new=case(base,NEW,window)
  assert old['actual_acceptance']and old['returned'][0]==old['expected_original_sha256']and old['final_path_sha256']!=old['expected_original_sha256']
  assert not new['actual_acceptance']and new['error']['type']=='ValueError'
  positive.append('old reader actual replacement gap observed: '+window)
  negative.append('new reader rejects actual replacement: '+window)
 # Do not generalize that all mid-read swaps pass the old reader: observe its real FD ctime outcome.
 middle=case(base,OLD,'inside_read_after_first_fstat')
 if middle['actual_acceptance']:
  assert middle['returned'][0]==middle['expected_original_sha256']
  positive.append('this filesystem actual mid-read replacement accepted by old reader')
 else:
  assert middle['error']['message']=='input changed during fresh byte read'
  positive.append('this filesystem actual mid-read replacement caught by old FD ctime comparison')
 newmiddle=case(base,NEW,'inside_read_after_first_fstat');assert not newmiddle['actual_acceptance']
 negative.append('new reader also rejects observed actual mid-read replacement')
 identical=case(base,NEW,'after_final_fstat_before_post_pathname',True)
 assert not identical['actual_acceptance']and identical['final_path_sha256']==identical['expected_original_sha256']
 negative.append('same-byte replacement still fails actual pathname identity')
 for kind in ('symlink','directory','missing'):
  p=base/'bad';target=base/'target';target.write_bytes(b'x')
  if kind=='symlink':p.symlink_to(target)
  elif kind=='directory':p.mkdir()
  try:extract(NEW,os)(p)
  except (ValueError,FileNotFoundError):negative.append('new reader rejects '+kind)
  else:raise AssertionError('accepted '+kind)
  if kind=='symlink':p.unlink()
  elif kind=='directory':p.rmdir()
 # Real truncate during the read, after first fstat, must never be represented as original bytes.
 class TruncOS(RealOS):
  def read(self,fd,n):
   raw=os.read(fd,n)
   if raw:
    self.path.write_bytes(b'X');self.events.append(dict(event='actual_truncate',pathname=info(self.path.lstat())))
   return raw
 p=base/'truncate';p.write_bytes(b'original');proxy=TruncOS(p,base/'unused')
 try:extract(NEW,proxy)(p)
 except ValueError:negative.append('new reader rejects actual truncate')
 else:raise AssertionError('accepted truncated input')
report=dict(schema='AXMAT_PRIVATE_INPUT_PATHNAME_STABILITY_ACTUAL_TINY_FIXTURES_V1',
 old=dict(path=str(OLD),sha256=hashlib.sha256(OLD.read_bytes()).hexdigest()),new=dict(path=str(NEW),sha256=hashlib.sha256(NEW.read_bytes()).hexdigest()),
 positive=positive,negative=negative,actual_small_file_observations=observations,
 stat_results_fabricated=False,original_os_module_or_project_globals_overlaid=False,
 scope='Isolated synthetic function globals wrap real stdlib syscalls and return actual observed stat values; no live business modules altered',
 actual_business_or_API_or_constructor_or_child_or_native_or_ART=False,RSS_or_cold_or_scientific_credit=False)
p=D/'pathname_stability_tiny_report.json';p.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(positive=len(positive),negative=len(negative),actual_reader_replacement_observations=len(observations),report=dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))))
