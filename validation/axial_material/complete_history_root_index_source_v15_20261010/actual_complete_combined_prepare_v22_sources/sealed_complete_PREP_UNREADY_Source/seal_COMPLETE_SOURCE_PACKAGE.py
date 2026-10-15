"""Standard-library finite SOURCE package seal; no binding or project execution."""
import hashlib
import json
from pathlib import Path
import stat

P=Path(__file__).resolve().parent

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    i=identity(p);assert stat.S_ISREG(i[2]) and not p.is_symlink()
    with p.open('rb') as f:d=hashlib.file_digest(f,'sha256').hexdigest()
    assert identity(p)==i
    return dict(path=str(p),sha256=d,size_bytes=i[4],identity=i)

def main():
    assert not (P/'MANIFEST.json').exists()
    members={str(p.relative_to(P)):pin(p) for p in sorted(P.rglob('*')) if p.is_file()}
    assert not any(p.is_symlink() for p in P.rglob('*'))
    report=json.loads((P/'FINAL_COMPLETE_SOURCE_SELF_REVIEW.json').read_bytes())
    assert report['all_checks_passed'] is True and report['blockers']==[] and report['check_count']==292
    assert report['actual_new_Q_sha256'] is None and report['actual_Q_or_ART_payload_read'] is False
    for rel,q in members.items():assert pin(P/rel)==q
    with (P/'MANIFEST.json').open('x') as f:
        json.dump(dict(schema='V22_COMPLETE_CANONICAL_GENUINE_PREP_UNREADY_SOURCE_MANIFEST_V1',source_only=True,status='SEALED_UNREADY_AWAITING_TRUE_NEW_HELPER_Q_AND_INDEPENDENT_SOURCE_REVIEW',members=members,member_count=len(members),member_bytes=sum(q['size_bytes'] for q in members.values()),all_members_complete_EOF_SHA7ID_before_after_exact=True,canonical70defs=True,genuine_normal_host_full=True,complete_metadata_writer_full=True,new_Q_path=None,new_Q_sha256=None,six_future_business_pins={k:None for k in report['all_six_future_business_pins']},original_genuine_caps=report['all_original_caps_preserved'],binder_or_helper_or_guard_or_API_or_business_executed=False,ART_payload_read=False,original_D_E_canonical_or_ART_written=False),f,indent=2,allow_nan=False);f.write('\n')
    for rel,q in members.items():assert pin(P/rel)==q
    assert sorted(str(p.relative_to(P)) for p in P.rglob('*') if p.is_file())==sorted(list(members)+['MANIFEST.json'])
    print(json.dumps(dict(source_only=True,closed_Source_seal=True,new_Q=None,member_count=len(members),member_bytes=sum(q['size_bytes'] for q in members.values()),manifest=pin(P/'MANIFEST.json'),final_review=pin(P/'FINAL_COMPLETE_SOURCE_SELF_REVIEW.json'),binder=pin(P/'bind_actual_Q_to_complete_PREP_SOURCE.py'),package_root_identity7=identity(P),project_or_binder_executed=False)))

if __name__=='__main__':main()
