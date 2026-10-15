"""List retired copies by default; restore an explicitly selected copy from its retained master."""
import argparse,hashlib,json,os,shutil,stat
from pathlib import Path
REPORT=Path('/Users/wen/spot/validation/storage_cleanup_thirteenth_20261009')
ROOT=Path('/Users/wen/spot')
PRIMARY=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/runtime/Dragon'
ALLOWED={str(ROOT/f'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{v}-20261009/runtime/Dragon') for v in (7,8)}
PRIMARY_SHA='77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba'
PRIMARY_SIZE=9225720

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifest-sha');choice=ap.add_mutually_exclusive_group();choice.add_argument('--restore-one');choice.add_argument('--restore-all',action='store_true');args=ap.parse_args()
 manifest=REPORT/'manifest.json'
 if REPORT.resolve(strict=True)!=REPORT or manifest.resolve(strict=True)!=manifest or not stat.S_ISREG(manifest.lstat().st_mode):raise ValueError('Nonordinary report/manifest')
 m=json.loads(manifest.read_text());rows=m['candidates']
 if len(rows)!=2 or {r['path'] for r in rows}!=ALLOWED or len(m['retained_primaries'])!=1 or sha(Path(__file__))!=m['restore_source_sha256']:raise ValueError('Unexpected recovery manifest/source')
 master=Path(m['retained_primaries'][0]['path'])
 if master!=PRIMARY or m['retained_primaries'][0]['sha256']!=PRIMARY_SHA or any(r['sha256']!=PRIMARY_SHA or r['size']!=PRIMARY_SIZE for r in rows):raise ValueError('Not the fixed original byte copies')
 if args.restore_one is None and not args.restore_all:
  print(json.dumps({'action':'LIST_ONLY_NO_WRITE','copies':[{'path':r['path'],'sha256':r['sha256'],'primary':str(master)} for r in rows],'old_inode_and_ctime_not_restored':True},ensure_ascii=False,indent=2));return
 selected=rows if args.restore_all else [r for r in rows if r['path']==args.restore_one]
 if not selected:raise ValueError('Select an exact manifest path')
 if not args.manifest_sha or sha(manifest)!=args.manifest_sha:raise ValueError('Actual recovery requires the recorded manifest SHA')
 if not stat.S_ISREG(master.lstat().st_mode) or master.resolve(strict=True)!=master or master.stat().st_size!=PRIMARY_SIZE or sha(master)!=PRIMARY_SHA:raise ValueError('Retained primary changed')
 for row in selected:
  p=Path(row['path'])
  if p.parent.resolve(strict=True)!=p.parent or os.path.lexists(p):raise ValueError('Destination must be an absent ordinary path')
  if row['sha256']!=m['retained_primaries'][0]['sha256'] or row['size']!=master.stat().st_size:raise ValueError('Recovery bytes differ')
  with master.open('rb') as src,p.open('xb') as dst:shutil.copyfileobj(src,dst,1024*1024);dst.flush();os.fsync(dst.fileno())
  if sha(p)!=row['sha256'] or p.stat().st_size!=row['size']:raise ValueError('Restored bytes differ')
  os.chmod(p,stat.S_IMODE(row['identity'][2]));os.utime(p,ns=(row['identity'][4],row['identity'][4]))
  print(json.dumps({'restored':str(p),'sha256':row['sha256'],'old_inode_and_ctime_not_restored':True},ensure_ascii=False))

if __name__=='__main__':main()
