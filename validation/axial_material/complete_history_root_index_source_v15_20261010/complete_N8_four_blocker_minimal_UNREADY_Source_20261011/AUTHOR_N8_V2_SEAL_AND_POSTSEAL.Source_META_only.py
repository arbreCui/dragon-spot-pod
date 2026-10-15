"""Finite own Source package seal/postseal. Never imports candidates."""
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
    before=ident(p.lstat());assert p.is_absolute()and stat.S_ISREG(before[2])and before[3]==1 and all(not q.is_symlink()for q in(p,*p.parents))
    with p.open('rb')as f:assert ident(os.fstat(f.fileno()))==before;sha=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==before
    assert ident(p.lstat())==before
    return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def directories():return {str(p):ident(p.lstat())for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}
def write(p,v):
    with p.open('x')as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def terminal(path):
    w=json.loads(path.read_bytes());t=w['terminal_tool_return'];assert w['closed']is True and w['observed_terminal']is True and w['actual_terminal_chunk']==t['chunk_id']and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t
    return w,json.loads(t['output'])
def seal():
    rpath=P/'AUTHOR_COMPLETE_N8_V2_FINAL_SOURCE_ONLY_REPORT.json';r=json.loads(rpath.read_bytes());checks=r['checks']
    assert r['source_only']is True and r['all_checks_passed']is True and r['blockers']==[] and type(r['check_count'])is int and r['check_count']==len(checks)>0 and len({c['check']for c in checks})==len(checks)and all(type(c['passed'])is bool and c['passed']is True for c in checks)
    tool,out=terminal(P/'ACTUAL_AUTHOR_N8_V2_FINAL_SOURCE_CHECK_TOOL_RETURN.json');assert out['actual_report_pin']==pin(rpath)and out['blockers']==[]
    files=[p for p in sorted(P.rglob('*'))if p.is_file()];assert not(P/'MANIFEST.json').exists();members=[];py=0
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_bytes());py+=1
        members.append(dict(relative_path=str(p.relative_to(P)),fullpin=pin(p)))
    mf=P/'MANIFEST.json';mf.write_text('{}\n');dirs=directories();contract=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes())
    # This is the original schema consumed by the unchanged business binder.
    data=dict(schema='COMPLETE_NATIVE_OBSERVATION_BUILD5_AB_UNREADY_SOURCE_MANIFEST_V1',revision_schema='COMPLETE_N8_V2_FOUR_BLOCKER_MINIMAL_SOURCE_MANIFEST_V1',status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,members=members,directories=dirs,member_count=len(members),files_including_manifest=len(members)+1,directory_count=len(dirs),complete_Python_Source_AST_count=py,required_author_Source_roles=contract['required_author_Source_roles'],original_N8_parent_member_count=239,original_N7_source_member_count=181,original_native_Source_member_count=1365,actual_author_report_pin=pin(rpath),actual_author_Source_check_tool_return_pin=pin(P/'ACTUAL_AUTHOR_N8_V2_FINAL_SOURCE_CHECK_TOOL_RETURN.json'),actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_monitor_controls_qualification=None,actual_native_AB_execution=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    mf.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n');assert dirs==directories()and all(pin(P/row['relative_path'])==row['fullpin']for row in members)
    roles={k:pin(P/v)for k,v in contract['required_author_Source_roles'].items()};assert len(roles)==21
    print(json.dumps(dict(status='SEALED_AUTHOR_UNREADY_SOURCE_ONLY_NOT_ROOT_ADMITTED_OR_EXECUTED',source_only=True,manifest_pin=pin(mf),review_pin=pin(rpath),members=len(members),files=len(members)+1,directories=len(dirs),Source_AST_count=py,actual_author_Source_contract=roles,blockers=[],actual_candidate_execution=False,scientific_qualification_created=False),allow_nan=False),flush=True)
def postseal():
    truth,out=terminal(S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json');mfpin=pin(P/'MANIFEST.json');assert out['manifest_pin']==mfpin
    d=json.loads((P/'MANIFEST.json').read_bytes());checks=[]
    def check(n,v):assert type(v)is bool and n not in{c['check']for c in checks};checks.append(dict(check=n,passed=v))
    files={str(p.relative_to(P)):p for p in P.rglob('*')if p.is_file()};check('complete_full_Source_member_set',set(files)=={r['relative_path']for r in d['members']}|{'MANIFEST.json'});check('complete_actual_directory_freeze',directories()==d['directories'])
    py=0
    for row in d['members']:
        p=P/row['relative_path'];check('fullEOF_SHA_size_7ID:'+row['relative_path'],pin(p)==row['fullpin'])
        if p.suffix=='.py':ast.parse(p.read_bytes());py+=1
    check('Source_only_no_new_controls_native_science',d['actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution']is False and d['actual_monitor_controls_qualification']is None and d['actual_native_AB_execution']is None and d['scientific_qualification_created']is False)
    check('actual_author_report_coupling',out['review_pin']==pin(P/'AUTHOR_COMPLETE_N8_V2_FINAL_SOURCE_ONLY_REPORT.json'));check('exact_complete_counts',len(files)==d['files_including_manifest']and len(d['directories'])==d['directory_count']and py==d['complete_Python_Source_AST_count'])
    blockers=[c['check']for c in checks if c['passed']is not True];assert blockers==[];t,_=terminal(P/'ACTUAL_AUTHOR_N8_V2_FINAL_SOURCE_CHECK_TOOL_RETURN.json')
    result=dict(schema='AUTHOR_COMPLETE_N8_V2_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mfpin,review_pin=out['review_pin'],files=len(files),directories=len(d['directories']),complete_Python_Source_AST_count=py,check_count=len(checks),checks=checks,all_checks_passed=True,blockers=[],actual_review_terminal_chunk=t['actual_terminal_chunk'],actual_seal_terminal_chunk=truth['actual_terminal_chunk'],actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
    path=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json';write(path,result)
    print(json.dumps(dict(status=result['status'],source_only=True,manifest_pin=mfpin,postseal_verification_pin=pin(path),files=len(files),directories=len(d['directories']),blockers=[],actual_candidate_execution=False),allow_nan=False),flush=True)
if __name__=='__main__':
    cli=argparse.ArgumentParser();cli.add_argument('--mode',choices=('seal','postseal'),required=True);a=cli.parse_args();{'seal':seal,'postseal':postseal}[a.mode]()
