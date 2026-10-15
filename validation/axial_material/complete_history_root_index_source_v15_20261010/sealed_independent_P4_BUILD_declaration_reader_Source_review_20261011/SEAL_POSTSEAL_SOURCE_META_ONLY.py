"""Finite own Source/META seal. No import or execution of candidate Source."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

MAX=16*2**20
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def ident(p):return ids(Path(p).lstat())
def pin(p):
    p=Path(p);i=ident(p)
    assert p.is_absolute()and p.resolve()==p and stat.S_ISREG(i[2])and i[3]==1 and 0<=i[4]<=MAX
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        assert ids(os.fstat(fd))==i
        parts=[];remaining=MAX+1
        while remaining:
            b=os.read(fd,min(65536,remaining))
            if not b:break
            parts.append(b);remaining-=len(b)
        b=b''.join(parts)
        assert len(b)<=MAX and len(b)==i[4]and ids(os.fstat(fd))==i and ident(p)==i
    finally:os.close(fd)
    return b,dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=i)
def jread(p):
    b,q=pin(p);return json.loads(b),q
def view(root):
    files={};dirs={'.':ident(root)};asts={}
    for p in sorted(root.rglob('*')):
        i=ident(p);rel=str(p.relative_to(root));assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):dirs[rel]=i
        else:
            b,q=pin(p);files[rel]=q
            if rel.endswith('.py'):asts[rel]=hashlib.sha256(ast.dump(ast.parse(b),include_attributes=False).encode()).hexdigest()
    for rel,i in dirs.items():assert ident(root/rel)==i
    return dict(root=str(root),files=files,directories=dirs,symlinks={},complete_python_AST_SHA256=asts)
def verify(root):
    r,rp=jread(root/'REVIEW.json')
    assert r['schema']=='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1'and r['status']=='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'and r['source_only']is True
    assert r['all_checks_typed_true']is True and r['blockers']==[]and type(r['check_count'])is int and r['check_count']==len(r['checks'])
    assert len({c['check']for c in r['checks']})==r['check_count']and all(type(c['passed'])is bool and c['passed']is True for c in r['checks'])
    assert r['candidate_BINDER_API_guard_resource_helper_material_numeric_or_business_executed']is False and r['actual_ART_declaration_graph_trace_gzip_material_payload_read']is False
    for q in r['all_independently_read_Source_small_META_input_pins'].values():assert pin(q['path'])[1]==q
    assert view(Path(r['qualified_complete_Source_manifest_pin']['path']).parent)==r['complete_current_candidate_Source_small_META_view']
    w,wp=jread(root/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json');t=w['terminal_tool_return']
    assert w['closed']is True and w['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and w['session_repolled_after_close']is False
    o=json.loads(t['output']);assert o['review_pin']==rp and o['qualified_complete_Source_manifest_pin']==r['qualified_complete_Source_manifest_pin']and o['blockers']==[]and o['check_count']==r['check_count']
    return r,rp,wp
def write(p,d):
    b=(json.dumps(d,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    try:
        off=0
        while off<len(b):
            n=os.write(fd,b[off:]);assert n>0;off+=n
        os.fsync(fd)
    finally:os.close(fd)
def package(root):
    m,mp=jread(root/'MANIFEST.json');v=view(root)
    assert m['source_only']is True and type(m['member_count'])is int and m['member_count']==len(m['members'])and set(v['files'])==set(m['members'])|{'MANIFEST.json'}and v['directories']==m['directories']
    assert all(q==v['files'][rel]and q['path']==str(root/rel)for rel,q in m['members'].items())
    return m,mp,v
def main():
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    root=Path(__file__).parent;assert root.parent==Path('/private/tmp')and root.name.startswith('axmat_P4_BUILD_DECLARATION_READER_INDEPENDENT_')
    r,rp,wp=verify(root);action=sys.argv[1];s=Path(str(root)+'_seal_receipt')
    if action=='seal':
        # Allocate first, then record directory7ID; no package member is added later.
        fd=os.open(root/'MANIFEST.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);os.close(fd)
        v=view(root);members={k:q for k,q in v['files'].items()if k!='MANIFEST.json'}
        m=dict(schema='INDEPENDENT_FINITE_SINGLE_DECLARATION_READER_SOURCE_META_REVIEW_MANIFEST_V1',source_only=True,member_count=len(members),members=members,directories=v['directories'])
        b=(json.dumps(m,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();fd=os.open(root/'MANIFEST.json',os.O_WRONLY|os.O_NOFOLLOW)
        try:
            assert os.fstat(fd).st_size==0
            off=0
            while off<len(b):
                n=os.write(fd,b[off:]);assert n>0;off+=n
            os.fsync(fd)
        finally:os.close(fd)
        m,mp,v=package(root);s.mkdir()
        d=dict(schema='INDEPENDENT_SINGLE_DECLARATION_READER_SOURCE_META_SEAL_V1',source_only=True,status='SOURCE_ONLY_PASS_SINGLE_READER_NO_EXECUTION_OR_SCIENCE',manifest_pin=mp,review_pin=rp,actual_review_tool_return_pin=wp,complete_review_package_view=v,qualified_complete_Source_manifest_pin=r['qualified_complete_Source_manifest_pin'],check_count=r['check_count'])
        write(s/'SEAL_REPORT.json',d);assert verify(root)==(r,rp,wp)and package(root)==(m,mp,v)
        print(json.dumps(dict(manifest_pin=mp,review_pin=rp,seal_report_pin=pin(s/'SEAL_REPORT.json')[1],source_only=True,check_count=r['check_count'],blockers=[],files=len(v['files']),directories=len(v['directories'])),sort_keys=True))
    elif action=='postseal':
        m,mp,v=package(root);d,dp=jread(s/'SEAL_REPORT.json');assert d['manifest_pin']==mp and d['review_pin']==rp and d['complete_review_package_view']==v
        w,sp=jread(s/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');t=w['terminal_tool_return'];assert w['closed']is True and w['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and w['session_repolled_after_close']is False
        o=json.loads(t['output']);assert o['manifest_pin']==mp and o['review_pin']==rp and o['seal_report_pin']==dp
        post=dict(schema='INDEPENDENT_SINGLE_DECLARATION_READER_FULL_SOURCE_META_POSTSEAL_V1',source_only=True,manifest_pin=mp,review_pin=rp,actual_review_tool_return_pin=wp,actual_seal_tool_return_pin=sp,seal_report_pin=dp,complete_review_package_view=v,qualified_complete_Source_manifest_pin=r['qualified_complete_Source_manifest_pin'],all_complete_current_candidate_and_review_Source_small_META_pins_unchanged=True,top_level_package_peer_terminal_interface_satisfied=True,candidate_API_or_business_executed=False)
        write(s/'POSTSEAL_REPORT.json',post);assert verify(root)==(r,rp,wp)and package(root)==(m,mp,v)
        print(json.dumps(dict(manifest_pin=mp,review_pin=rp,postseal_report_pin=pin(s/'POSTSEAL_REPORT.json')[1],actual_seal_tool_return_pin=sp,source_only=True,check_count=r['check_count'],blockers=[],files=len(v['files']),directories=len(v['directories'])),sort_keys=True))
    else:raise ValueError('finite own Source seal action')
if __name__=='__main__':main()
