"""Finite complete Source/META seal and postseal; no candidate execution."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
P=Path(__file__).resolve().parent
S=Path(str(P)+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    ids=ident(p.lstat());assert p.is_absolute()and stat.S_ISREG(ids[2])and ids[3]==1 and all(not q.is_symlink()for q in(p,*p.parents))
    with p.open('rb')as f:assert ident(os.fstat(f.fileno()))==ids;sha=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==ids
    assert ident(p.lstat())==ids
    return dict(path=str(p),sha256=sha,size_bytes=ids[4],identity=ids)
def dirs():return {'.':ident(P.lstat()),**{str(q.relative_to(P)):ident(q.lstat())for q in sorted(P.rglob('*'))if q.is_dir()}}
def write(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def terminal(p):
    w=json.loads(p.read_bytes());t=w['terminal_tool_return'];assert w['closed']is True and w['observed_terminal']is True and w['actual_terminal_chunk']==t['chunk_id']and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    return w,json.loads(t['output'])
def seal():
    report=P/'AUTHOR_P4_BUILD_DECLARATION_READER_SINGLE_FUNCTION_SOURCE_REPORT.json';r=json.loads(report.read_bytes());checks=r['checks']
    assert r['source_only']is True and r['all_checks_typed_true']is True and r['blockers']==[]and type(r['check_count'])is int and r['check_count']==len(checks)>0 and len({c['check']for c in checks})==len(checks)and all(type(c['passed'])is bool and c['passed']is True for c in checks)
    tool,out=terminal(P/'ACTUAL_AUTHOR_DECLARATION_READER_SOURCE_TOOL_RETURN.json');assert out['report_pin']==pin(report)
    files=[q for q in sorted(P.rglob('*'))if q.is_file()];target=P/'MANIFEST.json';assert not target.exists();members={};py=0
    for q in files:
        members[str(q.relative_to(P))]=pin(q)
        if q.suffix=='.py':ast.parse(q.read_bytes());py+=1
    target.write_text('{}\n');directories=dirs();value=dict(schema='V25_COMPLETE_BUILD_MEMORY_OBSERVATION_CAPTURE_NAMESPACE_UNREADY_SOURCE_MANIFEST_V1',revision_schema='P4_SINGLE_DECLARATION_META_READER_FIX_UNREADY_SOURCE_MANIFEST_V1',source_only=True,status='UNREADY_SOURCE_ONLY_REQUIRES_DIFFERENT_AUTHOR_REVIEW',member_count=len(members),members=members,directories=directories,total_member_bytes=sum(v['size_bytes']for v in members.values()),current_author_report=report.name,actual_consumed_complete_inverse='COMPLETE_SOURCE_INVERSES.json',whole_namespace_inverses='COMPLETE_P4_DECLARATION_READER_SINGLE_FUNCTION_14_ROLE_BYTE_AST_INVERSES.json',current_Source_role_count=14,typed_author_check_count=len(checks),only_runtime_change_single_BUILD_binder_read_function=True,all_original_other13role_Source_bytes_unchanged=True,original_P4_namespace_and_saved_PREP_not_replaced=True,added_exact_declaration_META_max_bytes=16*2**20,all_actual_future_environment_business_or_Source_qualification_pins=None,candidate_or_business_executed=False,complete_Python_Source_AST_count=py,files_including_manifest=len(members)+1,directory_count=len(directories),actual_author_report_pin=pin(report),actual_author_Source_check_tool_pin=pin(P/'ACTUAL_AUTHOR_DECLARATION_READER_SOURCE_TOOL_RETURN.json'))
    target.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');assert dirs()==directories and all(pin(P/rel)==wanted for rel,wanted in members.items())
    print(json.dumps(dict(status='SEALED_SOURCE_ONLY_UNREADY_NO_CANDIDATE_OR_BUSINESS',source_only=True,manifest_pin=pin(target),review_pin=pin(report),members=len(members),files=len(members)+1,directories=len(directories),complete_Python_Source_AST_count=py,blockers=[],actual_candidate_execution=False,scientific_qualification_created=False),allow_nan=False),flush=True)
def postseal():
    w,out=terminal(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');mp=pin(P/'MANIFEST.json');assert out['manifest_pin']==mp
    m=json.loads((P/'MANIFEST.json').read_bytes());checks=[]
    def check(n,v):assert type(v)is bool and n not in{r['check']for r in checks};checks.append(dict(check=n,passed=v))
    files={str(q.relative_to(P))for q in P.rglob('*')if q.is_file()};check('complete_Source_member_set',files==set(m['members'])|{'MANIFEST.json'});check('complete_frozen_directory_7IDs',dirs()==m['directories']);py=0
    for rel,wanted in m['members'].items():
        check('actual_fullEOF_SHA_size_7ID:'+rel,pin(P/rel)==wanted)
        if Path(rel).suffix=='.py':ast.parse((P/rel).read_bytes());py+=1
    check('exact_complete_counts',len(files)==m['files_including_manifest']and len(dirs())==m['directory_count']and py==m['complete_Python_Source_AST_count']);check('real_source_author_report_coupling',out['review_pin']==pin(P/m['current_author_report']));check('no_business_or_science_qualification',m['candidate_or_business_executed']is False and m['all_actual_future_environment_business_or_Source_qualification_pins']is None)
    blockers=[r['check']for r in checks if r['passed']is not True];assert not blockers;t,_=terminal(P/'ACTUAL_AUTHOR_DECLARATION_READER_SOURCE_TOOL_RETURN.json')
    v=dict(schema='P4_SINGLE_DECLARATION_READER_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mp,review_pin=out['review_pin'],files=len(files),directories=len(dirs()),complete_Python_Source_AST_count=py,check_count=len(checks),checks=checks,all_checks_typed_true=True,blockers=[],actual_review_terminal_chunk=t['actual_terminal_chunk'],actual_seal_terminal_chunk=w['actual_terminal_chunk'],actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
    vp=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json';write(vp,v);print(json.dumps(dict(status=v['status'],source_only=True,manifest_pin=mp,postseal_verification_pin=pin(vp),files=len(files),directories=len(dirs()),blockers=[],actual_candidate_execution=False),allow_nan=False),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mode',required=True,choices=('seal','postseal'));a=p.parse_args();{'seal':seal,'postseal':postseal}[a.mode]()
