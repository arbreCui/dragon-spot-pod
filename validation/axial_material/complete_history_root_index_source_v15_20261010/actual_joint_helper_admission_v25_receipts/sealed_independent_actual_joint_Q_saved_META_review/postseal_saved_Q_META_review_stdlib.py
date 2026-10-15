"""Complete finite peer bytes/namespace postseal; no qualification rerun."""
import hashlib,json,stat
from pathlib import Path
P=Path(__file__).parent
def identity(p):
    s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p)
    if not stat.S_ISREG(before[2]):raise ValueError('regular finite Source/META')
    h=hashlib.sha256()
    with p.open('rb')as f:
        while b:=f.read(1024*1024):h.update(b)
    if identity(p)!=before:raise ValueError('changed input')
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
m=json.loads((P/'MANIFEST.json').read_bytes());r=json.loads((P/'REVIEW.json').read_bytes())
names={str(p.relative_to(P))for p in P.rglob('*')if p.is_file()and p.name!='MANIFEST.json'};dirs={'.'}|{str(p.relative_to(P))for p in P.rglob('*')if p.is_dir()}
if names!=set(m['complete_members'])or dirs!=set(m['complete_directories']):raise ValueError('complete finite peer scope mismatch')
if any(pin(P/rel)!=v for rel,v in m['complete_members'].items())or any(identity(P if rel=='.'else P/rel)!=v for rel,v in m['complete_directories'].items()):raise ValueError('full finite peer EOF SHA7ID changed')
for name in ['Root_actual_Q_pin','Root_actual_Q_writer_terminal_pin','Root_actual_Q_writer_Source_pin']:
    if pin(Path(r[name]['path']))!=r[name]:raise ValueError('Root actual source/Q/proof changed')
if r['check_count']!=48 or r['source_only']is not True or r['blockers']!=[]:raise ValueError('saved helper-only metadata review contract')
print(json.dumps(dict(status='POSTSEAL_PASS_COMPLETE_SAVED_JOINT_HELPER_Q_META_ONLY',source_only=True,manifest_pin=pin(P/'MANIFEST.json'),review_pin=pin(P/'REVIEW.json'),check_count=48,member_count=len(names),complete_member_bytes=m['complete_member_bytes'],directory_count=len(dirs),Root_actual_Q_pin=r['Root_actual_Q_pin'],candidate_helper_writer_guard_API_or_numeric_executed=False)))
