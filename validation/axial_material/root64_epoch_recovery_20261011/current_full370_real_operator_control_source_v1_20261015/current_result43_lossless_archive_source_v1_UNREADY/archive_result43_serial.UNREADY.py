"""Root-owned serial byte archival draft; no JSONL decoding and no unlink code."""
import argparse,gzip,hashlib,importlib.util,json,os,platform,sys,time,zlib
from pathlib import Path

BASE=Path(__file__).absolute().parent

def load_common(p):
 before=Path(p['path']).lstat();ids=[before.st_dev,before.st_ino,before.st_mode,before.st_nlink,before.st_size,before.st_mtime_ns,before.st_ctime_ns]
 if ids!=p['identity']or hashlib.sha256(Path(p['path']).read_bytes()).hexdigest()!=p['sha256']:raise RuntimeError('whole frozen common Source')
 spec=importlib.util.spec_from_file_location('result43_archive_common',p['path']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.current7(p);return m

class BoundedArchiveSink:
 """Check before every compressed write; partial files stay counted after any failure."""
 def __init__(self,file,completed_bytes,c,resources):
  self.file=file;self.completed_bytes=completed_bytes;self.c=c;self.resources=resources;self.bytes=0
 def write(self,b):
  self.resources.light()
  self.c.require(self.completed_bytes+self.bytes+len(b)<self.c.ARCHIVE_CAP,'all48 gzip payload below184MiB; no compression assumption')
  self.c.require(self.c.own_bytes(self.resources.out)+len(b)<self.c.OUT_CAP-8*2**20,'retain8MiB metadata/runtime headroom within192MiB')
  n=self.file.write(b);self.c.require(n==len(b),'complete compressed write');self.bytes+=n;return n
 def flush(self):return self.file.flush()

def archive_one(c,p,q,completed_bytes,resources):
 c.current7(p);fd=os.open(p['path'],os.O_RDONLY|os.O_NOFOLLOW);oldsha=hashlib.sha256();n=0
 try:
  c.require(c.identity(os.fstat(fd))==p['identity'],'opened original plain7')
  newfd=os.open(q,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
  with os.fdopen(newfd,'wb')as target:
   sink=BoundedArchiveSink(target,completed_bytes,c,resources)
   with gzip.GzipFile(filename='',mode='wb',fileobj=sink,compresslevel=6,mtime=0)as gz:
    while b:=os.read(fd,c.CHUNK):
     resources.light();oldsha.update(b);n+=len(b);c.require(n<=p['size_bytes'],'oldplain length bounded by exactPF');gz.write(b)
   target.flush();os.fsync(target.fileno())
  dfd=os.open(q.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
  try:os.fsync(dfd)
  finally:os.close(dfd)
  c.require(c.identity(os.fstat(fd))==p['identity'],'original open7 stable through compression')
 finally:os.close(fd)
 c.current7(p);c.require(n==p['size_bytes']and oldsha.hexdigest()==p['sha256'],'original fullEOF SHA/length exact savedPF')
 pgz=c.pin(q);uncompressed_sha=hashlib.sha256();uncompressed_length=0
 with q.open('rb')as raw:
  header=raw.read(10)
 c.require(header[:3]==b'\x1f\x8b\x08'and header[3]==0 and header[4:8]==b'\0'*4,
  'fixed gzip format/no filename/no timestamp; same pinned runtime deterministic parameters')
 with gzip.open(q,'rb')as stream:
  while b:=stream.read(c.CHUNK):
   resources.light();uncompressed_length+=len(b)
   c.require(uncompressed_length<=p['size_bytes'],'streaming decompression bounded by original length')
   uncompressed_sha.update(b)
 c.require(c.pin(q)==pgz,'compressed fullEOF SHA/current7 unchanged during round trip')
 c.require(uncompressed_length==p['size_bytes']and uncompressed_sha.hexdigest()==p['sha256'],
  'streamed decompressed byte SHA/length equal exact original plainPF; no decoded value claim')
 c.current7(p)
 return dict(original_plain_full_pin=p,compressed_archive_full_pin=pgz,
  compression_input_SHA=oldsha.hexdigest(),compression_input_length=n,
  streamed_decompressed_SHA=uncompressed_sha.hexdigest(),streamed_decompressed_length=uncompressed_length,
  exact_original_plain_bytes_recoverable=True,original_plain_preserved=True,filename_field='',mtime=0,
  compresslevel=6,gzip_header_hex=header.hex(),result_values_decoded=False)

def main():
 ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--binding-pin',required=True);ap.add_argument('--common-source-pin',required=True);ap.add_argument('--expected-parent-pid',required=True,type=int)
 args=ap.parse_args();started=time.monotonic();c=load_common(json.loads(args.common_source_pin));pbind=json.loads(args.binding_pin)
 c.require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None
  and all(os.environ.get(k)=='1'for k in c.THREADS)and Path(sys.executable).resolve()==c.PYTHON,
  'original child interpreter/unoptimized/unprofiled/thread1')
 b=c.metadata(pbind);out=c.admit(b);c.require(os.getppid()==args.expected_parent_pid,'original owning parent PID')
 resources=c.Resources(b,started,600);resources.check()
 c.write_new(out/'CHILD_ARCHIVE_CLAIM.json',dict(schema='RESULT43_SERIAL_BYTE_ARCHIVE_CHILD_ONCE_CLAIM_V1',PID=os.getpid(),parent_PID=os.getppid(),original_started=started,retries=0),64*2**10)
 archives=out/'archives';archives.mkdir();entries=[];completed_bytes=0;phase='BEFORE_FIRST_ARCHIVE'
 runtime=dict(python_version=platform.python_version(),python_executable=str(Path(sys.executable).resolve()),zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,zlib_build=zlib.ZLIB_VERSION,gzip_source_path=gzip.__file__,chunk_bytes=c.CHUNK,compresslevel=6,filename_field='',mtime=0)
 try:
  for ordinal,p in enumerate(b['all48_plain_pins']):
   phase='ARCHIVE_'+str(ordinal);resources.check()
   q=archives/(str(ordinal).zfill(3)+'_'+Path(p['path']).name+'.gz')
   entry=archive_one(c,p,q,completed_bytes,resources);entry['ordinal']=ordinal
   entry['historical_completed_A_guard_role']=p['path']in b['historical_completed_guard_role_paths']
   entry['completed_A2_new_JSONL_role']=p in b['completed_A2_new5_JSONL_pins']
   pe=c.write_new(out/('archive_entry_'+str(ordinal).zfill(3)+'.json'),entry,32*2**10)
   entries.append(dict(entry_pin=pe,**entry));completed_bytes+=entry['compressed_archive_full_pin']['size_bytes'];resources.check()
  phase='COMPLETE_INDEX';c.require(len(entries)==48,'all48 results byte preserved, no omitted plain')
  for p in b['all48_plain_pins']+b['retained_native_current7_pins']:c.current7(p)
  index=dict(schema='RESULT43_LOSSLESS_ORIGINAL_PATH_ARCHIVE_LOOKUP_V1',status='ALL48_STREAMED_ROUNDTRIP_SHA_LENGTH_EXACT_PLAIN_PRESERVED',binding_pin=pbind,entries=entries,ordered_original_plain_count=48,ordered_original_plain_total_bytes=805236925,total_gzip_bytes=completed_bytes,historical_completed_A_guard_role_count=30,archive_lookup_key='exact original path plus original fullPF',runtime=runtime,compression_ratio_assumed=False,requires_independent_post0_before_separate_plain_retirement=True,old_consumer_must_not_open_absent_historical_plain_paths=True,**c.FALSE)
  pindex=c.write_new(out/'RESULT43_LOSSLESS_ARCHIVE_INDEX.json',index,2*2**20);after=resources.check()
  report=dict(schema='ACTUAL_RESULT43_SERIAL_LOSSLESS_ARCHIVE_REPORT_V1',status='ALL48_BYTE_SHA_LENGTH_ROUNDTRIP_CLOSED0_PLAIN_RETAINED',failure=None,index_pin=pindex,binding_pin=pbind,completed_count=48,total_gzip_bytes=completed_bytes,original_plain_total_bytes=805236925,resources_after=after,wall_seconds=time.monotonic()-started,all48_original_plain_current7_retained=True,all66_native_current7_retained=True,**c.FALSE)
  preport=c.write_new(out/'ACTUAL_RESULT43_LOSSLESS_ARCHIVE_REPORT.json',report,2*2**20);resources.check()
  print(json.dumps(dict(status=report['status'],report_pin=preport)),flush=True)
 except BaseException as error:
  # Preserve the original nonzero, partial archives, and all plain inputs. Never retry or roll back.
  try:c.write_new(out/'FIRST_ARCHIVE_FAILURE.json',dict(schema='RESULT43_LOSSLESS_ARCHIVE_FIRST_FAILURE_V1',failure=repr(error),phase=phase,completed_entry_pins=[e['entry_pin']for e in entries],partial_archive_paths=[str(p)for p in sorted(archives.glob('*.gz'))],original_plain_files_deleted=False,retry_performed=False,**c.FALSE),512*2**10)
  except BaseException:pass
  raise

if __name__=='__main__':main()
