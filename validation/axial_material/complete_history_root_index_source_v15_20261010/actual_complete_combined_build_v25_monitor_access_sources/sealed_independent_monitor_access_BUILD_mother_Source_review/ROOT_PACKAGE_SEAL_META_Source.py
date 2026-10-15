import hashlib
import json
import stat
from pathlib import Path
ROOT = Path(__file__).parent
def identity(p):
    s=p.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    before=identity(p)
    assert stat.S_ISREG(before[2]) and not p.is_symlink()
    b=p.read_bytes()
    assert identity(p)==before and len(b)==before[4]
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=before)
target=ROOT/'MANIFEST.json'
target.touch(exist_ok=False)
members={str(p.relative_to(ROOT)):pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=target}
directories={'.':identity(ROOT),**{str(p.relative_to(ROOT)):identity(p) for p in sorted(ROOT.rglob('*')) if p.is_dir()}}
value=dict(schema='ROOT_COMPLETE_INDEPENDENT_NAMESPACE_SOURCE_REVIEW_MANIFEST_V1',source_only=True,members=members,directories=directories,member_count=len(members),candidate_or_business_executed=False,science_qualification_created=False)
target.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
for k,v in members.items(): assert pin(ROOT/k)==v
for k,v in directories.items(): assert identity(ROOT if k=='.' else ROOT/k)==v
print(json.dumps(dict(source_only=True,review_pin=pin(ROOT/'REVIEW.json'),manifest_pin=pin(target),complete_files=len(members)+1,closed_only_not_execution_or_science=True)))
