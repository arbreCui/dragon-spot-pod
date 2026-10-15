"""Only checks this fixed Source review metadata and complete member bytes."""
import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p)
    if not stat.S_ISREG(before[2]):raise ValueError('ordinary Source/META only')
    h=hashlib.sha256()
    with p.open('rb')as f:
        while b:=f.read(1024*1024):h.update(b)
    if identity(p)!=before:raise ValueError('changed file')
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
m=json.loads((P/'MANIFEST.json').read_bytes());r=json.loads((P/'REVIEW.json').read_bytes())
files={str(p.relative_to(P))for p in P.rglob('*')if p.is_file()and p.name!='MANIFEST.json'}
dirs={'.'}|{str(p.relative_to(P))for p in P.rglob('*')if p.is_dir()}
if files!=set(m['complete_members'])or dirs!=set(m['complete_directories']):raise ValueError('complete review namespace differs')
for rel,v in m['complete_members'].items():
    if pin(P/rel)!=v:raise ValueError('full member EOF SHA7ID changed')
for rel,v in m['complete_directories'].items():
    if identity(P if rel=='.'else P/rel)!=v:raise ValueError('review directory changed')
if pin(Path(r['qualified_Root_writer_Source_pin']['path']))!=r['qualified_Root_writer_Source_pin']:raise ValueError('reviewed Root writer changed')
if m['source_only']is not True or m['check_count']!=65 or r['blockers']!=[]:raise ValueError('Source-only report contract')
print(json.dumps(dict(status='POSTSEAL_COMPLETE_EOF_SHA7ID_SOURCE_ONLY_PASS',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'REVIEW.json'),check_count=65,member_count=len(files),whole_member_bytes=m['complete_member_bytes'],directory_count=len(dirs),writer_pin=r['qualified_Root_writer_Source_pin'],candidate_or_writer_API_or_numeric_executed=False)))
