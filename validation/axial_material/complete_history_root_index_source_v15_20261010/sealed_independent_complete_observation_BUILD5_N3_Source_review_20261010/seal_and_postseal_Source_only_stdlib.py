import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

R=Path(__file__).parent
P=Path('/private/tmp/axmat_complete_native_observation_BUILD5_AB_E_fullpin_same_sort_finite_UNREADY_Source_fix_pb5gkdac')
S=Path(str(R)+'_seal_receipt')
def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    a=ident(p.lstat());assert p.is_absolute()and stat.S_ISREG(a[2])and a[3]==1 and not p.is_symlink()
    with p.open('rb')as f:
        assert ident(os.fstat(f.fileno()))==a
        h=hashlib.file_digest(f,'sha256').hexdigest()
        assert ident(os.fstat(f.fileno()))==a
    assert ident(p.lstat())==a
    return dict(path=str(p),sha256=h,size_bytes=a[4],identity=a)
def write(p,j):
    with p.open('x')as f:json.dump(j,f,indent=2,allow_nan=False);f.write('\n')
def inventory(r):
    return dict(files={str(p.relative_to(r)):pin(p)for p in sorted(r.rglob('*'))if p.is_file()},directories={'.'if p==r else str(p.relative_to(r)):ident(p.lstat())for p in[r,*sorted(r.rglob('*'))]if p.is_dir()})
def validate():
    report=json.loads((R/'REVIEW.json').read_bytes());checks=report['checks']
    assert report['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and report['source_only']is True and report['all_checks_passed']is True
    assert type(report['check_count'])is int and report['check_count']==len(checks)==66 and len({c['check']for c in checks})==66
    assert all(set(c)=={'check','passed'}and type(c['check'])is str and type(c['passed'])is bool for c in checks)
    assert sum(not c['passed']for c in checks)==len(report['blockers'])==0
    truth=json.loads((R/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json').read_bytes());t=truth['terminal_tool_return']
    assert truth['closed']is True and truth['observed_terminal']is True and truth['actual_terminal_chunk']==t['chunk_id']=='c21dff'and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    stdout=json.loads(t['output']);assert stdout['review_pin']==pin(R/'REVIEW.json')and stdout['blocker_count']==0 and stdout['failed_checks']==0
    assert inventory(P)==report['complete_reviewed_source_namespace_before']==report['complete_reviewed_source_namespace_after']
    assert report['helper_candidate_guard_API_native_material_compile_or_numeric_executed']is False
    return report
if sys.argv[1:] == ['seal']:
    report=validate();m=R/'MANIFEST.json';assert not m.exists();m.touch()
    before=inventory(R)
    for p in R.rglob('*.py'):ast.parse(p.read_bytes())
    rows=[dict(relative_path=k,fullpin=v)for k,v in before['files'].items()if k!='MANIFEST.json']
    result=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_REVIEW_MANIFEST_V1',status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT',source_only=True,members=rows,member_count=len(rows),file_count_including_manifest=len(rows)+1,directory_count=len(before['directories']),complete_directory_identity=before['directories'],review_pin=pin(R/'REVIEW.json'),actual_review_tool_truth_pin=pin(R/'ACTUAL_INDEPENDENT_REVIEW_TOOL_RETURNS.json'),actual_original_Source_manifest_pin=report['complete_reviewed_source_manifest_pin'],whole_original_native_Source_archive_members=1365,independent_aggregate_Source_checks=66,blocker_count=0,qualified_source_manifest=report['complete_reviewed_source_manifest_pin'],actual_Root_Source_admission=None,actual_native_execution=None,scientific_qualification_created=False)
    m.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    actual=inventory(R);assert actual['directories']==before['directories']and all(actual['files'][r['relative_path']]==r['fullpin']for r in rows)
    print(json.dumps(dict(status=result['status'],source_only=True,manifest_pin=pin(m),review_pin=pin(R/'REVIEW.json'),members=len(rows),files=len(rows)+1,directories=len(before['directories']),blockers=0,actual_candidate_execution=False),allow_nan=False))
elif sys.argv[1:] == ['postseal']:
    report=validate();mf=json.loads((R/'MANIFEST.json').read_bytes());before=inventory(R)
    assert len(before['files'])==mf['file_count_including_manifest']and before['directories']==mf['complete_directory_identity']
    assert set(before['files'])=={x['relative_path']for x in mf['members']}|{'MANIFEST.json'}
    assert all(before['files'][r['relative_path']]==r['fullpin']for r in mf['members'])
    for p in R.rglob('*.py'):ast.parse(p.read_bytes())
    seal=json.loads((S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json').read_bytes());t=seal['terminal_tool_return'];assert seal['closed']is True and seal['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    assert json.loads(t['output'])['manifest_pin']==pin(R/'MANIFEST.json')
    value=dict(schema='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=pin(R/'MANIFEST.json'),review_pin=pin(R/'REVIEW.json'),all_review_package_members_full_EOF_SHA7ID_verified=True,all_original_author_members_full_EOF_SHA7ID_and_directories_unchanged=True,complete_review_package_file_count=len(before['files']),complete_review_package_directory_count=len(before['directories']),actual_review_terminal_chunk='c21dff',actual_seal_terminal_chunk=t['chunk_id'],independent_aggregate_Source_checks=66,blockers=0,actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
    q=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json';write(q,value);assert inventory(R)==before
    print(json.dumps(dict(status=value['status'],source_only=True,manifest_pin=pin(R/'MANIFEST.json'),postseal_verification_pin=pin(q),actual_candidate_execution=False),allow_nan=False))
else:raise SystemExit('seal or postseal only')
