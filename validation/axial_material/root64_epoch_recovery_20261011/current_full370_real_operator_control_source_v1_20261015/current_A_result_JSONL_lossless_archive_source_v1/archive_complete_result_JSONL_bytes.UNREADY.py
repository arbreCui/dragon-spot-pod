"""UNREADY: Root-only byte-preserving archive; no JSONL decoding or plaintext deletion."""
import argparse,gzip,hashlib,importlib.util,json,os,resource,stat,sys,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
OUT=BASE/'archive_output_v1'
ART=Path('/Users/wen/spot/validation/artifacts')
BLOCK=2**20
OUTPUT_BOUND=192*2**20
RECEIPT_RESERVE=8*2**20
def need(v,m):
 if v is not True:raise RuntimeError(m)
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def current(p):
 need(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}and type(p['size_bytes'])is int and type(p['identity'])is list and len(p['identity'])==7 and all(type(v)is int for v in p['identity']),'complete integer fullPF')
 q=Path(p['path']);s=q.lstat();need(q.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1 and s.st_uid==os.getuid()and ident(s)==p['identity']and s.st_size==p['size_bytes']and not any(a.is_symlink()for a in(q,*q.parents)),'ordinary owned exact current7')
 return q
def full(p,budget,parse=False):
 q=current(p);need(not parse or p['size_bytes']<8*2**20,'bounded metadata8MiB')
 h=hashlib.sha256();parts=[];n=0;fd=os.open(q,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  need(ident(os.fstat(fd))==p['identity'],'opened7')
  while True:
   b=os.read(fd,BLOCK)
   if not b:break
   h.update(b);n+=len(b)
   if parse:parts.append(b)
   budget()
  need(ident(os.fstat(fd))==p['identity'],'EOF7')
 finally:os.close(fd)
 current(p);need(n==p['size_bytes']and h.hexdigest()==p['sha256'],'whole byte-stream SHA')
 return json.loads(b''.join(parts))if parse else None
def pin_new(q,budget):
 s=q.lstat();need(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'new archive regular single-link file')
 p=dict(path=str(q),sha256='',size_bytes=s.st_size,identity=ident(s));h=hashlib.sha256()
 with q.open('rb')as f:
  need(ident(os.fstat(f.fileno()))==p['identity'],'new archive opened7')
  while True:
   b=f.read(BLOCK)
   if not b:break
   h.update(b);budget()
  need(ident(os.fstat(f.fileno()))==p['identity'],'new archive EOF7')
 p['sha256']=h.hexdigest();current(p);return p
def module(p,name,budget):
 full(p,budget);spec=importlib.util.spec_from_file_location(name,p['path']);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);current(p);return m
def save(f,v):
 b=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode();need(len(b)<RECEIPT_RESERVE,'runtime receipt8MiB inside whole192MiB')
 f.seek(0);f.write(b);f.truncate();f.flush();os.fsync(f.fileno())
def sync_dir(q):
 fd=os.open(q,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(fd)
 finally:os.close(fd)
def current_unlinked_bytes():
 rows={}
 for name in os.listdir('/dev/fd'):
  try:s=os.fstat(int(name))
  except(ValueError,OSError):continue
  if stat.S_ISREG(s.st_mode)and s.st_nlink==0:rows[s.st_dev,s.st_ino]=s.st_size
 return sum(rows.values())
class BoundedGzipSink:
 def __init__(self,f,previous,budget):self.f=f;self.previous=previous;self.budget=budget;self.written=0
 def write(self,b):
  need(self.previous+self.written+len(b)+RECEIPT_RESERVE<=OUTPUT_BOUND,'aggregate archive192MiB hard bound; no assumed compression ratio')
  n=self.f.write(b);need(n==len(b),'complete archive write');self.written+=n;self.budget();return n
 def flush(self):self.f.flush()
def archive_one(original,q,previous,budget):
 source=current(original);fd=os.open(source,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0
 try:
  need(ident(os.fstat(fd))==original['identity'],'original plaintext opened7')
  with q.open('xb')as f:
   sink=BoundedGzipSink(f,previous,budget)
   with gzip.GzipFile(filename='',mode='wb',compresslevel=6,fileobj=sink,mtime=0)as z:
    while True:
     b=os.read(fd,BLOCK)
     if not b:break
     h.update(b);n+=len(b);need(n<=original['size_bytes'],'bounded original plaintext stream');z.write(b);budget()
   f.flush();os.fsync(f.fileno())
  sync_dir(q.parent)
  need(ident(os.fstat(fd))==original['identity'],'original plaintext EOF7')
 finally:os.close(fd)
 current(original);need(n==original['size_bytes']and h.hexdigest()==original['sha256'],'compressed stream equals exact saved original fullPF')
 compressed=pin_new(q,budget);decoded=hashlib.sha256();dn=0
 with q.open('rb')as f:
  need(ident(os.fstat(f.fileno()))==compressed['identity'],'compressed operand opened7')
  with gzip.GzipFile(fileobj=f,mode='rb')as z:
   while True:
    b=z.read(BLOCK)
    if not b:break
    dn+=len(b);need(dn<=original['size_bytes'],'bounded full decompression');decoded.update(b);budget()
  need(ident(os.fstat(f.fileno()))==compressed['identity'],'compressed operand EOF7')
 current(compressed);current(original)
 need(dn==original['size_bytes']and decoded.hexdigest()==original['sha256'],'whole decompress SHA and exact byte length equal saved plaintext PF')
 return dict(original_plaintext_pin=original,archive_pin=compressed,original_stream_SHA256=h.hexdigest(),decompressed_SHA256=decoded.hexdigest(),decompressed_bytes=dn,whole_decompressed_bytes_equal_original_SHA_and_size=True,JSONL_parsed=False,plaintext_deleted=False)
def main():
 ap=argparse.ArgumentParser(allow_abbrev=False)
 for role in('source','plan','review'):ap.add_argument('--'+role+'-pin',required=True)
 a=ap.parse_args();started=time.monotonic();resources={};plan=None;helper=None
 def budget():
  peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
  need(peak<512*2**20 and time.monotonic()-started<600,'original SELF512/stage600 within whole1800')
  source_bytes=0
  for q in BASE.rglob('*'):
   s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'archive Source namespace has no aliases')
   if stat.S_ISREG(s.st_mode)and not q.is_relative_to(OUT):source_bytes+=s.st_size
  need(source_bytes<16*2**20,'archive Source/metadata16MiB component, unchanged cumulative2GiB')
  if OUT.exists():
   total=0
   for q in OUT.rglob('*'):
    s=q.lstat();need(not stat.S_ISLNK(s.st_mode),'fresh archive namespace no aliases')
    if stat.S_ISREG(s.st_mode):total+=s.st_size
   need(total<=OUTPUT_BOUND,'entire archive/logs/receipt192MiB hard bound')
  if resources and time.monotonic()-resources['last']>=0.25:
   h=resources['history'].check();j=resources['joint'].check();extra=0
   for p in plan['explicit_cumulative_metadata_file_pins']:
    helper.current_metadata(p)
    if not any(Path(p['path']).is_relative_to(Path(r))for r in plan['complete_joint_roots']):extra+=p['size_bytes']
   unlinked=current_unlinked_bytes()
   need(j['artifact_bytes']+extra+unlinked<2*2**30,'unchanged full cumulative2GiB, external metadata and open-unlinked included')
   need(h['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30 and j['disk_free_bytes']-20971764748-2*2**30>=8*2**30,'original history96/cold/meta/fresh2/free8')
   resources['last']=time.monotonic();resources['latest']=dict(history_bytes=h['artifact_bytes'],joint_bytes=j['artifact_bytes'],external_metadata_bytes=extra,open_unlinked_bytes=unlinked,disk_free_bytes=j['disk_free_bytes'],SELF_peak_bytes=peak,elapsed_seconds=time.monotonic()-started)
 ps=json.loads(a.source_pin);pp=json.loads(a.plan_pin);pr=json.loads(a.review_pin)
 need(ps['path']==str(Path(__file__).absolute())and pp['path']==str(BASE/'PLAN.json')and not os.path.lexists(OUT),'literal Source/plan and fresh once archive output, no retry')
 full(ps,budget);plan=full(pp,budget,True);review=full(pr,budget,True)
 need(plan['schema']=='COMPLETE_RESULT_JSONL_LOSSLESS_ARCHIVE_PLAN_V1'and plan['Source_final_admission_complete']is True and plan['actual_new_A_business_completed']is True and plan['actual_new_A_post_complete']is True and plan['actual_early14_retirement_completed']is True,'UNREADY until genuine A and retirement closure plus Source admission')
 need(review['status']=='PASS_SOURCE_ONLY_COMPLETE_RESULT_JSONL_ARCHIVE'and review['failure']is None and review['source_only']is True and review['source_pin']==ps and review['plan_pin']==pp,'exact Source-only independent review contract; no runtime or physics PASS')
 roots=plan['complete_joint_roots'];need(len(roots)==len(set(roots))==64 and str(BASE.parent)in roots and all(not Path(x).is_relative_to(Path(y))for x in roots for y in roots if x!=y),'full64 prefix retained, archive output already under counted FTOP')
 inputs=module(plan['original_production_inputs_Source_pin'],'production_inputs',budget)
 need(Path(inputs.__file__).absolute()==Path(plan['original_production_inputs_Source_pin']['path']),'original preloaded production_inputs exact path')
 production=module(plan['original_production_resource_Source_pin'],'result_archive_original_production',budget);factory=module(plan['original_history_resource_Source_pin'],'result_archive_original_history',budget)
 shared=plan['shared_completed_A_admission_Source_pin'];need(shared['path']==str(BASE.parent/'current_A_early14_extract_spool_retirement_source_v1/retire_completed_A_early14_SQL_pool_spools.UNREADY.py'),'literal separately frozen metadata closure helper')
 helper=module(shared,'result_archive_completed_A_admission',budget)
 resources.update(history=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30,production.ResourceFailure),joint=production.DiskResources(ART.parent,roots,8*2**30,2*2**30),last=0.0)
 budget();a_proof=helper.admit_completed_new_A(plan,budget)
 rp=plan['early14_closure_pins'];retired=full(rp['receipt'],budget,True);rt=full(rp['Root_tools'],budget,True);post=full(rp['post'],budget,True);pt=full(rp['post_tools'],budget,True)
 helper.genuine(rt,'actual_execution_return',rp['receipt'],'receipt_pin');helper.genuine(pt,'actual_review_return',rp['post'],'review_pin')
 need(retired['schema']=='LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOL_RETIREMENT_RECEIPT_V1'and retired['mode']=='execute'and retired['status']=='RETIRED_EXACT_LITERAL14_COMPLETED_A_EARLY_EXTRACT_SPOOLS_ONLY'and retired['failure']is None and retired['actual_released_pins']==helper.TARGETS and retired['actual_released_bytes']==149659264 and retired['complete_joint_roots']==roots,'genuine exact14 completed lifecycle receipt, no input-scope reset')
 need(plan['early14_post_key_projection_audited']is True and post['schema']==plan['early14_post_schema']and post['status']==plan['early14_post_status']and post['failure']is None and post[plan['early14_post_receipt_pin_field']]==rp['receipt']and post[plan['early14_post_Root_tools_pin_field']]==rp['Root_tools'],'exact audited actual retirement post roles, no guessed success fields')
 need(all(not os.path.lexists(p['path'])for p in helper.TARGETS),'exact14 old derived operands absent only after true receipt/post0')
 registry=full(plan['original_result43_registry_pin'],budget,True);originals=registry['selected_pins'];new=plan['completed_new_A_JSONL_pins'];targets=plan['archive_plaintext_pins']
 need(len(originals)==43 and len({p['path']for p in originals})==43 and targets==originals+new and len({p['path']for p in targets})==len(targets)and all(Path(p['path']).suffix=='.jsonl'for p in targets),'exact saved43 plus all completed new A JSONLs; no summary-only replacement')
 host=full(plan['closure_pins']['new_A_host'],budget,True);new_manifest=host['complete_output_pins']
 need(new==[p for p in new_manifest if Path(p['path']).suffix=='.jsonl'],'new A result set equals every JSONL in genuine complete output PF manifest')
 for p in targets:current(p)
 for p in plan['preserved_current7_pins']:current(p)
 for p in plan['preserved_identity_only_roles']:helper.current_identity(p)
 OUT.mkdir(mode=0o700);sync_dir(BASE);sync_dir(OUT)
 d=dict(schema='COMPLETE_RESULT_JSONL_LOSSLESS_ARCHIVE_RECEIPT_V1',status='STARTED',failure=None,source_pin=ps,plan_pin=pp,peer_review_pin=pr,complete_joint_roots=roots,actual_A_closure=a_proof,actual_early14_retirement_receipt_pin=rp['receipt'],original_plaintext_pins=targets,archive_rows=[],archive_total_bytes=0,plaintext_total_bytes=sum(p['size_bytes']for p in targets),all_plaintexts_retained=True,plaintexts_deleted=False,JSONL_parsed=False,scientific_arrays_decoded=False,Source16MiB_reservation_unchanged=True,whole_archive_output_bound_bytes=OUTPUT_BOUND,original_caps=plan['original_caps'],resources_before=resources['latest'],resources_after=None,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 receipt=OUT/'EXECUTION_RECEIPT.json'
 with receipt.open('xb')as f:
  try:
   save(f,d);sync_dir(OUT);total=0
   for index,p in enumerate(targets,1):
    q=OUT/('%04d.jsonl.gz'%index);row=archive_one(p,q,total,budget);d['archive_rows'].append(row);total+=row['archive_pin']['size_bytes'];d['archive_total_bytes']=total;save(f,d);budget()
   need(len(d['archive_rows'])==len(targets),'all selected complete plaintexts archived and full-stream verified')
   for p in targets:current(p)
   for p in plan['preserved_current7_pins']:current(p)
   for p in plan['preserved_identity_only_roles']:helper.current_identity(p)
   budget();d['status']='ARCHIVED_COMPLETE_RESULT_JSONL_BYTES_PLAINTEXTS_RETAINED';d['resources_after']=resources['latest'];save(f,d);sync_dir(OUT);budget()
  except BaseException as e:
   d['status']='FAILED_ARCHIVE_PARTIAL_OUTPUT_PLAINTEXTS_RETAINED';d['failure']=repr(e);save(f,d);raise
 print(json.dumps(dict(status=d['status'],receipt_pin=pin_new(receipt,budget),plaintexts_deleted=False,JSONL_parsed=False,physics_qualified=False)),flush=True)
if __name__=='__main__':main()
