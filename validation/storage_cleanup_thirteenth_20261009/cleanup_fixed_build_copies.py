"""Retire only two independently reviewed, byte-identical failed-build copies."""
import argparse, hashlib, json, os, stat, time
from pathlib import Path

ROOT=Path('/Users/wen/spot')
REPORT=ROOT/'validation/storage_cleanup_thirteenth_20261009'
PRIMARY=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/runtime/Dragon'
ALLOWED={str(ROOT/f'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{v}-20261009/runtime/Dragon') for v in (7,8)}

def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def check(row):
 p=Path(row['path']);before=identity(p)
 if p.resolve(strict=True)!=p or not stat.S_ISREG(before[2]) or before!=row['identity'] or sha(p)!=row['sha256'] or identity(p)!=before:
  raise ValueError('Reviewed file changed: '+str(p))
 return p

def other_paths_digest(excluded):
 h=hashlib.sha256();counts={'regular_files':0,'symlinks':0,'directories':0}
 for cur,sub,names in os.walk(ROOT,followlinks=False):
  base=Path(cur);sub[:]=sorted(n for n in sub if base/n not in {ROOT/'.git',REPORT})
  h.update(json.dumps(['directory',str(base.relative_to(ROOT))],separators=(',',':')).encode()+b'\n');counts['directories']+=1
  for name in sorted(sub+names):
   p=base/name
   if str(p) in excluded:continue
   s=p.lstat()
   if stat.S_ISLNK(s.st_mode):value=['link',str(p.relative_to(ROOT)),identity(p),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISREG(s.st_mode):value=['file',str(p.relative_to(ROOT)),identity(p)];counts['regular_files']+=1
   else:continue
   h.update(json.dumps(value,separators=(',',':')).encode()+b'\n')
 return {'sha256':h.hexdigest(),**counts}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifest-sha',required=True);ap.add_argument('--independent-review-sha');ap.add_argument('--execute',action='store_true');args=ap.parse_args()
 manifest=REPORT/'manifest.json'
 if REPORT.resolve(strict=True)!=REPORT or sha(manifest)!=args.manifest_sha:raise ValueError('Manifest/report changed')
 m=json.loads(manifest.read_text());rows=m['candidates'];paths={r['path'] for r in rows}
 if sha(Path(__file__))!=m['cleanup_source_sha256'] or len(rows)!=2 or paths!=ALLOWED or len(m['retained_primaries'])!=1:raise ValueError('Not the reviewed fixed two-file action')
 master=m['retained_primaries'][0]
 if master['path']!=str(PRIMARY):raise ValueError('Wrong retained primary')
 check(master)
 for row in rows:
  if row['identity'][6]!=1 or row['sha256']!=master['sha256'] or row['identity'][3]!=master['identity'][3]:raise ValueError('Copy is not independently recoverable')
  check(row)
 for row in m['retained_control_pins']:check(row)
 before=other_paths_digest(paths)
 result={'schema':'SPOT_THIRTEENTH_EXACT_TWO_BUILD_COPY_RETIREMENT_V1','status':'PASS_FIXED_TWO_COPY_PREFLIGHT','manifest_sha256':args.manifest_sha,'executed':False,'count':2,'allocated_bytes':sum(x['allocated_bytes'] for x in rows),'logical_bytes':sum(x['size'] for x in rows),'other_paths_before':before,'timestamp':time.time(),'science_or_API_executed':False,'scientific_credit':False}
 if args.execute:
  pre=json.loads((REPORT/'independent_preflight_review.json').read_text())
  if not args.independent_review_sha or sha(REPORT/'independent_preflight_review.json')!=args.independent_review_sha or pre['status']!='PASS' or pre['manifest_sha256']!=args.manifest_sha or pre['cleanup_source_sha256']!=m['cleanup_source_sha256'] or pre['fixed_paths']!=sorted(paths):raise ValueError('Independent review missing or differs')
  if os.path.lexists(REPORT/'retirement_ledger.jsonl') or os.path.lexists(REPORT/'cleanup_result.json'):raise ValueError('Already attempted; no overwrite or retry')
  with (REPORT/'retirement_ledger.jsonl').open('x') as f:
   for row in rows:
    check(master);check(row).unlink();f.write(json.dumps({'path':row['path'],'sha256':row['sha256'],'retained_primary':str(PRIMARY),'removed_at':time.time()})+'\n');f.flush();os.fsync(f.fileno())
  if any(os.path.lexists(p) for p in paths):raise ValueError('Deleted path unexpectedly exists')
  after=other_paths_digest(paths)
  if after!=before:raise ValueError('Unselected project files/links/directory paths changed')
  check(master)
  for row in m['retained_control_pins']:check(row)
  result.update(status='PASS_ACTUAL_FIXED_TWO_BUILD_COPY_RETIREMENT',executed=True,other_paths_after=after)
  with (REPORT/'cleanup_result.json').open('x') as f:f.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
