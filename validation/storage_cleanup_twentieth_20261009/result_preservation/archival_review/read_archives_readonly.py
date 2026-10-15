import pathlib,json,hashlib,gzip,stat,os,time
D=pathlib.Path(__file__).parent;RD=pathlib.Path('/private/tmp/spot_storage_twentieth_root_20261009');t=time.monotonic()
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
M=RD/'lossless_archive_manifest.json';P=RD/'proposed_candidates_full_byte_proof.json'
mi=ident(M);pi=ident(P)
assert digest(M)=='9a82a37b0c19fbd011e6ecfc289a18fef83bc41f5301114aeb30e911f8602836'
assert digest(P)=='517ef094a4cfb8163ef12db9fdc8d58c0d12584f891c09f2e90fd7af3ef6632e'
m=json.loads(M.read_bytes());p=json.loads(P.read_bytes());old={x['path']:x for x in p['candidates']};rows=m['archives'];assert len(rows)==len(old)==30
assert {r['original_path'] for r in rows}==set(old) and len({r['temporary_archive_path'] for r in rows})==30
root=pathlib.Path('/Users/wen/spot');pins=[];parsed={}
for x in p['original_manifests']:
 path=pathlib.Path(x['path']);assert ident(path)==x['identity'] and digest(path)==x['sha256']
 d={}
 for line in path.read_text().splitlines():
  h,n=line.split(None,1);n=n.strip();assert n not in d;d[n]=h
 parsed[str(path)]=d;pins.append(x)
results=[]
for r in rows:
 orig=pathlib.Path(r['original_path']);c=old[str(orig)];assert ident(orig)==c['identity']
 assert r['raw_sha256']==c['sha256'] and r['raw_size_bytes']==c['size_bytes']
 assert r['original_relative_path']==str(orig.relative_to(root))
 for mn,want in c['original_manifest_sha256s'].items():assert parsed[str(orig.parent/mn)][orig.name]==want==r['raw_sha256']
 a=pathlib.Path(r['temporary_archive_path']);ai=ident(a);assert stat.S_ISREG(ai[2]) and ai[6]==1 and str(a.resolve())==str(a)
 assert ai[3]==r['gzip_size_bytes'];compressed=digest(a);assert compressed==r['gzip_sha256']
 total=0;h=hashlib.sha256()
 with gzip.open(a,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):
   total+=len(b);assert total<=r['raw_size_bytes'];h.update(b)
 assert total==r['raw_size_bytes'] and h.hexdigest()==r['raw_sha256']
 assert ident(a)==ai and ident(orig)==c['identity']
 results.append({'original_path':str(orig),'archive_path':str(a),'archive_identity':ai,'compressed_sha256':compressed,'compressed_size_bytes':ai[3],'decompressed_sha256':h.hexdigest(),'decompressed_size_bytes':total,'original_identity_stable':True,'matches_original_result_input_or_output_manifests':True})
assert sum(r['decompressed_size_bytes'] for r in results)==m['raw_bytes']==2580841168
assert sum(r['compressed_size_bytes'] for r in results)==m['gzip_bytes']==1155035285
assert ident(M)==mi and ident(P)==pi
for x in pins:assert ident(pathlib.Path(x['path']))==x['identity']
for c in old.values():assert ident(pathlib.Path(c['path']))==c['identity']
out={'schema':'SPOT_R20_INDEPENDENT_ALL_30_LOSSLESS_GZIP_FULL_INVERSE_CONTENT_REVIEW_V1','status':'PASS_LOSSLESS_ARCHIVE_CONTENT','project_written':False,'files_deleted':0,'business_executed':False,'archives_count':30,'archive_manifest_path':str(M),'archive_manifest_sha256':digest(M),'raw_proof_path':str(P),'raw_proof_sha256':digest(P),'raw_total_bytes':m['raw_bytes'],'gzip_total_bytes':m['gzip_bytes'],'full_raw_bytes_decoded_and_hashed_here':sum(r['decompressed_size_bytes'] for r in results),'compressed_bytes_full_hashed_here':sum(r['compressed_size_bytes'] for r in results),'all_archives_and_original_identity_before_after_stable':True,'all_original_manifests_fresh_fullSHA':pins,'archive_results':results,'restore_source_status':'PENDING_FINAL_SMALL_SOURCE_REVIEW_AFTER_NOOVERWRITE_BOUNDARY_CORRECTION','restoration_boundary':{'exact_content_size_SHA_recoverable_without_scientific_recomputation':True,'restores_original_inode_or_ctime':False,'restores_original_mtime':False,'old_scientific_outcomes_unchanged':True,'archives_become_required_unique_lossless_restore_primary_after_original_retirement':True,'existing_97_restore_packs_not_in_scope':True,'future_actual_restore_not_executed_or_claimed':True},'elapsed_readonly_seconds':time.monotonic()-t}
for name,v in [('CONTENT_REPORT.json',json.dumps(out,ensure_ascii=False,indent=2)+'\n'),('CONTENT_REPORT.txt','R20 无损压缩内容独审\n\n30份原工作文件合计2,580,841,168字节，无损gzip合计1,155,035,285字节。已独立完整读取每个gzip、全量解压并累计大小/SHA，与Root原文件全文证明和原result/input/output清单逐项一致；前后原文件及归档身份保持。\n\n可以按原内容恢复而无需约20.86小时科学重算；不恢复原inode/ctime/mtime，不改变旧通过或失败事实。原文件退役后30份gzip必须作为唯一无损恢复主本保留。未执行恢复、删除或业务，输出仅TMP。恢复工具最终no-overwrite边界源审另列。\n')]:
 with (D/name).open('x') as f:f.write(v);f.flush();os.fsync(f.fileno())
print(json.dumps({'status':out['status'],'report':str(D/'CONTENT_REPORT.json'),'sha256':digest(D/'CONTENT_REPORT.json'),'decoded_bytes':out['full_raw_bytes_decoded_and_hashed_here'],'archive_count':30,'seconds':out['elapsed_readonly_seconds']}))
