"""Seal this finite Source/META package only; no candidate or material read."""
import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).resolve().parent
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with p.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==identity(s)
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        assert identity(os.fstat(f.fileno()))==identity(s)
    assert identity(p.lstat())==identity(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=identity(s))
report=json.loads((P/'AUTHOR_COMPLETE_OLD_XSM_CONTEXT_AWARE_SOURCE_STATIC_REVIEW.json').read_bytes())
assert report['source_only']is True and report['all_checks_typed_true']is True and report['check_count']==1296
assert all(row['passed']is True for row in report['checks'])and len({r['check']for r in report['checks']})==1296
target=P/'MANIFEST.json'
assert not os.path.lexists(target)
with target.open('xb')as f:f.write(b'')
members=[];directories=[]
for p in [P,*sorted(P.rglob('*'))]:
    s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
    if stat.S_ISDIR(s.st_mode):directories.append(dict(path=str(p),identity=identity(s)))
    else:
        assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
        if p!=target:members.append(dict(relative_path=str(p.relative_to(P)),**pin(p)))
value=dict(schema='COMPLETE_OLD_XSM_CONTEXT_AWARE_AGGREGATION_SOURCE_ONLY_MANIFEST_V2',source_only=True,
    status='UNREADY_COMPLETE_SOURCE_SEALED_NO_EXECUTION_OR_QUALIFICATION',member_count=len(members),
    total_member_bytes=sum(m['size_bytes']for m in members),members=members,directories=directories,
    original_parent162_and_manifest_complete=True,original_caps=report['exact_scope'],
    actual_native_extraction=None,actual_MAT_SPH_context=None,actual_aggregation=None,actual_independent_review=None,new_Q=None,
    material_DB_numeric_helper_API_guard_compile_not_executed=True)
value['original_caps']=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,
    history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
with target.open('wb')as f:f.write((json.dumps(value,indent=2,allow_nan=False)+'\n').encode())
for m in members:assert pin(Path(m['path']))=={k:m[k]for k in('path','sha256','size_bytes','identity')}
for d in directories:assert identity(Path(d['path']).lstat())==d['identity']
names=('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','complete_observed_old_post_final_XSM_extractor.UNREADY.py',
    'complete_context_aware_aggregation_and_oldXSM_genuine_host.UNREADY.py','bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py',
    'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','AUTHOR_COMPLETE_OLD_XSM_CONTEXT_AWARE_SOURCE_STATIC_REVIEW.json')
print(json.dumps(dict(source_only=True,status=value['status'],manifest=pin(target),member_count=len(members),total_member_bytes=value['total_member_bytes'],
    directory_count=len(directories),checks=1296,candidates={name:pin(P/name)for name in names},no_candidate_material_DB_API_guard_execution=True),allow_nan=False))
