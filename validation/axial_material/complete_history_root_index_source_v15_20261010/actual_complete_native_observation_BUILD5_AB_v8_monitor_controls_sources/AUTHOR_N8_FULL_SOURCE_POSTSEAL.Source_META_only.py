"""Finite full EOF/AST/postseal Source validation; no candidate imports/actions."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')
SIBLING=Path(str(P)+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    before=ident(path.lstat());assert stat.S_ISREG(before[2])and before[3]==1 and all(not q.is_symlink()for q in(path,*path.parents))
    with path.open('rb')as f:
        assert ident(os.fstat(f.fileno()))==before;sha=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==before
    assert ident(path.lstat())==before
    return dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)

def main():
    cli=argparse.ArgumentParser();cli.add_argument('--actual-seal-receipt-sha256',required=True);a=cli.parse_args()
    truth=SIBLING/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json';assert pin(truth)['sha256']==a.actual_seal_receipt_sha256
    receipt=json.loads(truth.read_bytes());terminal=receipt['terminal_tool_return'];assert receipt['closed']is True and receipt['observed_terminal']is True and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and receipt['actual_terminal_chunk']==terminal['chunk_id']
    stdout=json.loads(terminal['output']);mf=pin(P/'MANIFEST.json');assert stdout['manifest_pin']==mf
    data=json.loads((P/'MANIFEST.json').read_bytes());checks=[];py=[]
    def check(name,value):
        assert type(value)is bool and name not in {r['check']for r in checks};checks.append(dict(check=name,passed=value))
    files={str(p.relative_to(P)):p for p in P.rglob('*')if p.is_file()};check('complete_actual_file_set',set(files)=={r['relative_path']for r in data['members']}|{'MANIFEST.json'})
    dirs={str(p):ident(p.lstat())for p in [P,*sorted(P.rglob('*'))]if p.is_dir()};check('complete_actual_directory_freeze',dirs==data['directories'])
    for row in data['members']:
        path=P/row['relative_path'];check('full_Source_META_EOF_7ID:'+row['relative_path'],pin(path)==row['fullpin'])
        if path.suffix=='.py':ast.parse(path.read_bytes());py.append(str(path))
    check('manifest_and_actual_author_review_tool_coupling',stdout['review_pin']==pin(P/'AUTHOR_COMPLETE_N8_FINAL_SOURCE_ONLY_REPORT.json'))
    check('no_candidate_guard_API_native_or_numeric_qualification',data['actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution']is False and data['actual_monitor_controls_qualification']is None and data['actual_native_AB_execution']is None and data['scientific_qualification_created']is False)
    check('all_exact_counts',len(files)==data['files_including_manifest']and len(dirs)==data['directory_count']and len(py)==data['complete_Python_Source_AST_count'])
    blockers=[c['check']for c in checks if not c['passed']];assert blockers==[]
    author_tool=json.loads((P/'ACTUAL_AUTHOR_FINAL_SOURCE_CHECK_TOOL_RETURN.json').read_bytes())
    result=dict(schema='AUTHOR_COMPLETE_N8_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,manifest_pin=mf,review_pin=stdout['review_pin'],actual_review_terminal_chunk=author_tool['actual_terminal_chunk'],actual_seal_terminal_chunk=receipt['actual_terminal_chunk'],files=len(files),directories=len(dirs),complete_Python_Source_AST_count=len(py),check_count=len(checks),checks=checks,all_checks_passed=True,blockers=[],actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
    target=SIBLING/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
    with target.open('x')as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=result['status'],source_only=True,manifest_pin=mf,actual_candidate_execution=False,postseal_verification_pin=pin(target),files=len(files),directories=len(dirs),blockers=[]),allow_nan=False))

if __name__=='__main__':main()
