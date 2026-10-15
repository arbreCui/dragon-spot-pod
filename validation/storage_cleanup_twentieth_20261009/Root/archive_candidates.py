from pathlib import Path
import json,os,gzip,hashlib,time

TMP=Path('/private/tmp/spot_storage_twentieth_root_20261009')
ROOT=Path('/Users/wen/spot')
proof=json.loads((TMP/'proposed_candidates_full_byte_proof.json').read_bytes())
out=TMP/'lossless_archives'
assert not out.exists();out.mkdir()

def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

rows=[];start=time.monotonic()
for row in proof['candidates']:
 p=Path(row['path']);assert identity(p)==row['identity']
 rel=p.relative_to(ROOT/'validation/artifacts')
 z=out/rel.with_name(rel.name+'.gz');z.parent.mkdir(parents=True,exist_ok=True)
 h=hashlib.sha256();count=0
 with p.open('rb') as f,z.open('wb') as output,gzip.GzipFile(fileobj=output,mode='wb',compresslevel=6,mtime=0,filename='') as c:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b);count+=len(b);c.write(b)
 assert count==row['size_bytes'] and h.hexdigest()==row['sha256'] and identity(p)==row['identity']
 inverse=hashlib.sha256();inverse_n=0
 with gzip.open(z,'rb') as c:
  for b in iter(lambda:c.read(1024*1024),b''):inverse.update(b);inverse_n+=len(b)
 assert inverse_n==count and inverse.digest()==h.digest()
 rows.append({'original_path':str(p),'original_relative_path':str(p.relative_to(ROOT)),
              'temporary_archive_path':str(z),'saved_archive_relative_path':str(Path('archives')/rel.with_name(rel.name+'.gz')),
              'raw_size_bytes':count,'raw_sha256':h.hexdigest(),'gzip_size_bytes':z.stat().st_size,
              'gzip_sha256':digest(z),'full_inverse_size_and_sha_verified':True})
result={'schema':'SPOT_R20_EXACT_30_ROOT_LOSSLESS_ARCHIVES_V1','status':'ALL_30_FULL_GZIP_INVERSE_MATCH_ORIGINAL_FULL_MANIFEST_BYTES',
        'archives':rows,'raw_bytes':sum(x['raw_size_bytes'] for x in rows),
        'gzip_bytes':sum(x['gzip_size_bytes'] for x in rows),'elapsed_seconds':time.monotonic()-start,
        'project_written':False,'raw_deleted':False,'codec':'gzip','compression_level':6,
        'replaces_original_recomputation_only_retirement_plan':True}
(TMP/'lossless_archive_manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'archive_count':len(rows),'raw_bytes':result['raw_bytes'],
                  'gzip_bytes':result['gzip_bytes'],'elapsed_seconds':result['elapsed_seconds']}))
