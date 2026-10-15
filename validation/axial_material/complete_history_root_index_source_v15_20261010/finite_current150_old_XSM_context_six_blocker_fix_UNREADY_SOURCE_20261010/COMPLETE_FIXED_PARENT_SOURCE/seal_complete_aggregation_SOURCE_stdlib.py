"""Seal only this fresh TMP complete Source/META package; never candidate run."""
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);s=path.lstat()
    assert path.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with path.open('rb')as stream:
        assert identity(os.fstat(stream.fileno()))==identity(s)
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        assert identity(os.fstat(stream.fileno()))==identity(s)
    assert identity(path.lstat())==identity(s)
    return dict(path=str(path),sha256=digest,size_bytes=s.st_size,identity=identity(s))

assert P.is_relative_to(Path('/private/tmp'))and not(P/'MANIFEST.json').exists()
rp=pin(P/'AUTHOR_COMPLETE_AGGREGATION_SOURCE_STATIC_REVIEW.json')
review=json.loads(Path(rp['path']).read_bytes())
assert review['schema']=='COMPLETE_AGGREGATION_ENGINE_OBSERVER_AUTHOR_SOURCE_STATIC_REVIEW_V1'
assert review['source_only']is True and review['all_checks_typed_true']is True
assert type(review['check_count'])is int and review['check_count']==len(review['checks'])>0
assert review['unique_check_label_count']==review['check_count']
assert len({x['check']for x in review['checks']})==review['check_count']
assert all(type(x)is dict and set(x)=={'check','passed'}and type(x['check'])is str and x['passed']is True for x in review['checks'])
assert review['complete_aggregation_executable_qualification_ready']is False
assert review['candidate_or_API_imported_or_executed']is False
assert review['numeric_or_large_material_payload_read']is False
assert review['compiled']is False
assert review['new_aggregation_qualification']is None and review['scientific_qualification']is None
assert review['complete_parent_members']==[26,82]
for value in review['source_candidate_pins'].values():assert pin(value['path'])==value
rows=[];directories=[]
for p in sorted(P.rglob('*')):
    s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
    if stat.S_ISDIR(s.st_mode):
        directories.append(dict(path=str(p),relative_path=str(p.relative_to(P)),identity=identity(s)))
    else:
        row=pin(p);row['relative_path']=str(p.relative_to(P));rows.append(row)
for row in rows:
    assert pin(row['path'])=={k:row[k]for k in('path','sha256','size_bytes','identity')}
value=dict(schema='COMPLETE_FINAL_AGGREGATION_ENGINE_GENUINE_HOST_OBSERVATION_UNREADY_SOURCE_MANIFEST_V1',
    source_only=True,status='SEALED_UNREADY_SOURCE_ONLY_NO_RUNTIME_OR_QUALIFICATION',
    member_count=len(rows),members=rows,full_member_bytes=sum(r['size_bytes']for r in rows),
    nested_directory_count=len(directories),nested_directory_identity_at_seal=directories,
    root_identity_before_manifest_append=identity(P.lstat()),root_directory_identity_not_claimed_stable_across_manifest_creation=True,
    author_complete_Source_static_review=rp,actual_author_Source_check_count=review['check_count'],
    full_parent_member_counts=[26,82],all_members_full_EOF_SHA7ID_checked=True,
    candidate_or_material_executed=False,compiled=False,actual_Source_installation=None,
    actual_genuine_host_run=None,complete_aggregation_executable_qualification_ready=False,
    new_aggregation_qualification=None,scientific_qualification=None)
with(P/'MANIFEST.json').open('x')as stream:
    json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
mp=pin(P/'MANIFEST.json')
print(json.dumps(dict(source_only=True,status=value['status'],manifest=mp,member_count=len(rows),
    full_member_bytes=value['full_member_bytes'],nested_directory_count=len(directories),report=rp,
    actual_author_Source_check_count=review['check_count'],candidate_or_material_executed=False),allow_nan=False),flush=True)
