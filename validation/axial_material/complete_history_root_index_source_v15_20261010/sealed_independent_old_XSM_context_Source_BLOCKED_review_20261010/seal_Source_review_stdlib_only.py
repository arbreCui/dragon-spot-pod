import hashlib,json,os,stat
from pathlib import Path
P=Path(__file__).resolve().parent
S=P.with_name(P.name+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with p.open('rb')as f:
        assert ident(os.fstat(f.fileno()))==ident(s)
        h=hashlib.file_digest(f,'sha256').hexdigest()
        assert ident(os.fstat(f.fileno()))==ident(s)
    assert ident(p.lstat())==ident(s)
    return dict(path=str(p),sha256=h,size_bytes=s.st_size,identity=ident(s))
view=json.loads((P/'FULL_SOURCE_INVENTORY_AND_RETENTION_BEFORE_AFTER.json').read_bytes())
assert view['before']==view['after']
for k in ('original','retained'):
    v=view['after'][k];root=Path(v['root'])
    actual={str(x.relative_to(root)) for x in root.rglob('*')if x.is_file()}
    assert actual==set(v['files'])
    for rel,expected in v['files'].items():assert pin(root/rel)==expected
    for rel,i in v['directories'].items():assert ident((root/rel).lstat())==i
for k in ('retention_record','retention_tool'):assert pin(Path(view['after'][k]['path']))==view['after'][k]
review=json.loads((P/'REVIEW.json').read_bytes())
assert review['status']=='SOURCE_ONLY_BLOCKED_NO_EXECUTION_OR_SCIENCE'
assert review['source_only']is True and review['all_checks_passed']is False
assert len(review['checks'])==review['check_count']==40 and len(review['blockers'])==6
assert sum(c['passed']is True for c in review['checks'])==38
mp=P/'MANIFEST.json';assert not mp.exists();mp.touch()
members=[];dirs=[]
for x in [P,*sorted(P.rglob('*'))]:
    s=x.lstat();assert not stat.S_ISLNK(s.st_mode)
    if stat.S_ISDIR(s.st_mode):dirs.append(dict(path=str(x),relative_path=str(x.relative_to(P)),identity=ident(s)))
    elif x!=mp:members.append(dict(relative_path=str(x.relative_to(P)),**pin(x)))
manifest=dict(schema='INDEPENDENT_COMPLETE_OLD_XSM_CONTEXT_SOURCE_BLOCKED_REVIEW_SEAL_V1',source_only=True,status='SEALED_SOURCE_ONLY_BLOCKED_NO_EXECUTION_OR_SCIENCE',member_count=len(members),total_member_bytes=sum(x['size_bytes']for x in members),members=members,directories=dirs,review_pin=pin(P/'REVIEW.json'),original_sources_beforeafter_unchanged=True,new_Q=None,scientific_qualification_created=False)
mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for m in members:assert pin(Path(m['path']))=={k:m[k]for k in ('path','sha256','size_bytes','identity')}
for d in dirs:assert ident(Path(d['path']).lstat())==d['identity']
S.mkdir();seal=dict(schema='INDEPENDENT_COMPLETE_OLD_XSM_CONTEXT_SOURCE_BLOCKED_REVIEW_SEAL_RECEIPT_V1',source_only=True,manifest_pin=pin(mp),review_pin=pin(P/'REVIEW.json'),member_count=len(members),directory_count=len(dirs),all_full_Source_members_EOF_SHA7ID_rechecked=True,source_candidates_unchanged_and_not_executed=True,new_Q=None)
(S/'SOURCE_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps(seal),flush=True)
