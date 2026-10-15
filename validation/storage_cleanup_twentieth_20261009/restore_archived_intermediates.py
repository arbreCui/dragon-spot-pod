"""Restore the 30 archived working files into a new, separate directory."""
from pathlib import Path
import argparse,json,gzip,hashlib,os

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--destination',required=True,help='New empty destination; existing directories are refused.')
 args=parser.parse_args()
 base=Path(__file__).resolve().parent
 manifest=json.loads((base/'Root/lossless_archive_manifest.json').read_bytes())
 rows=manifest['archives'];assert len(rows)==30
 assert len({r['original_relative_path'] for r in rows})==30
 assert len({r['saved_archive_relative_path'] for r in rows})==30
 requested=Path(args.destination).expanduser()
 if os.path.lexists(requested):raise SystemExit('Destination already exists; choose a new separate directory.')
 dest=requested.resolve()
 if os.path.lexists(dest):raise SystemExit('Destination already exists; choose a new separate directory.')
 for row in rows:
  rel=Path(row['original_relative_path']);assert not rel.is_absolute() and '..' not in rel.parts
  saved_rel=Path(row['saved_archive_relative_path']);assert not saved_rel.is_absolute() and '..' not in saved_rel.parts
  archive=base/saved_rel
  assert archive.stat().st_size==row['gzip_size_bytes'] and digest(archive)==row['gzip_sha256']
 dest.mkdir(parents=True)
 restored=[]
 for row in rows:
  target=dest/row['original_relative_path'];target.parent.mkdir(parents=True,exist_ok=True)
  temporary=target.with_name(target.name+'.restoring');h=hashlib.sha256();size=0;created=False
  try:
   with gzip.open(base/row['saved_archive_relative_path'],'rb') as source,temporary.open('xb') as output:
    created=True
    for b in iter(lambda:source.read(1024*1024),b''):output.write(b);h.update(b);size+=len(b)
   assert size==row['raw_size_bytes'] and h.hexdigest()==row['raw_sha256']
   os.chmod(temporary,0o600);os.link(temporary,target);temporary.unlink();restored.append(str(target))
  except BaseException:
   if created:temporary.unlink(missing_ok=True)
   raise
 print(json.dumps({'restored_files':len(restored),'destination':str(dest),'raw_content_verified':True,'original_project_files_overwritten':False},ensure_ascii=False))

if __name__=='__main__':main()
