from pathlib import Path
import hashlib,json,os,stat
P=Path('/private/tmp/axmat_native_STRICT_SCOPE_complete_SOURCE_peer_l4us4hq0')
A=Path('/private/tmp/axmat_native_host_BINDER_STRICT_SCOPE_UNREADY_SOURCE_20261010_gs2tnzvo')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    s=p.lstat();assert stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with p.open('rb')as f:
        assert identity(os.fstat(f.fileno()))==identity(s);b=f.read();assert len(b)==s.st_size and f.read(1)==b'';assert identity(os.fstat(f.fileno()))==identity(s)
    assert identity(p.lstat())==identity(s)
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
r=json.loads((P/'REVIEW.json').read_bytes());assert r['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'and r['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and r['source_only']is True and r['all_checks_passed']is True and r['blockers']==[]
assert len(r['checks'])==r['check_count']==5741 and all(type(v)is dict and set(v)=={'check','passed'}and v['passed']is True for v in r['checks'])and len({v['check']for v in r['checks']})==5741
for k in('qualified_source_manifest','host_template','checker_template','binder'):assert pin(Path(r[k]['path']))==r[k]
tr=json.loads((P/'ACTUAL_SOURCE_REVIEW_TOOL_TERMINAL_RETURN.json').read_bytes());assert tr['closed']is True and tr['source_only']is True and tr['actual_tool_terminal_return_observed']is True and type(tr['terminal_tool_return']['exit_code'])is int and tr['terminal_tool_return']['exit_code']==0 and 'session_id'not in tr['terminal_tool_return']and tr['review_sha256']==pin(P/'REVIEW.json')['sha256']
am=json.loads((A/'MANIFEST.json').read_bytes());assert len(am['members'])==82
copies=[]
for v in am['members']:
    original=Path(v['path']);copied=P/'COMPLETE_FIXED_AUTHOR_SOURCE'/v['relative_path'];assert pin(original)=={k:v[k]for k in('path','sha256','size_bytes','identity')};assert original.read_bytes()==copied.read_bytes();copies.append(dict(original=v,peer_copy=pin(copied)))
assert(A/'MANIFEST.json').read_bytes()==(P/'COMPLETE_FIXED_AUTHOR_SOURCE/MANIFEST.json').read_bytes()
manifest=P/'MANIFEST.json';assert not manifest.exists();manifest.write_text('{}\n')
members=[dict(relative_path=p.relative_to(P).as_posix(),**pin(p))for p in sorted(P.rglob('*'))if p.is_file()and p!=manifest]
directories={str(p):identity(p.lstat())for p in [P,*sorted(p for p in P.rglob('*')if p.is_dir())]}
value=dict(schema='INDEPENDENT_NATIVE_COMPLETE_STRICT_SCOPE_SOURCE_PEER_SEAL_V1',source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',member_count=len(members),total_member_bytes=sum(v['size_bytes']for v in members),members=members,directories=directories,qualified_author_manifest=r['qualified_source_manifest'],independent_complete_review=pin(P/'REVIEW.json'),actual_Source_review_terminal=pin(P/'ACTUAL_SOURCE_REVIEW_TOOL_TERMINAL_RETURN.json'),all5741_complete_independent_checks_typed_true=True,complete82_author_members_plus_manifest_byte_copy=True,complete_author_Source_copies=copies,actual_build_or_native_run=None,actual_RSS_or_scientific_qualification=None)
manifest.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
for v in members:assert pin(Path(v['path']))=={k:v[k]for k in('path','sha256','size_bytes','identity')}
assert directories=={str(p):identity(p.lstat())for p in [P,*sorted(p for p in P.rglob('*')if p.is_dir())]}
assert sorted(p.relative_to(P).as_posix()for p in P.rglob('*')if p.is_file())==sorted([v['relative_path']for v in members]+['MANIFEST.json'])
print(json.dumps(dict(source_only=True,status=value['status'],manifest=pin(manifest),review=pin(P/'REVIEW.json'),member_count=len(members),all5741_complete_independent_checks_typed_true=True,all_frozen_files_and_directories_unchanged=True,no_reviewed_binder_checker_host_guard_API_or_payload_execution=True),indent=2))
