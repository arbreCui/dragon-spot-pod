"""Finite full Source-package EOF/AST manifest writer. No candidate execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path('/private/tmp/axmat_N8_exact_owner_complete_UNREADY_Source_mjczixe4')

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    before=ident(path.lstat());assert stat.S_ISREG(before[2])and before[3]==1 and all(not q.is_symlink()for q in(path,*path.parents))
    with path.open('rb')as f:
        assert ident(os.fstat(f.fileno()))==before;sha=hashlib.file_digest(f,'sha256').hexdigest();assert ident(os.fstat(f.fileno()))==before
    assert ident(path.lstat())==before
    return dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before)

def main():
    report=P/'AUTHOR_COMPLETE_N8_FINAL_SOURCE_ONLY_REPORT.json';review=json.loads(report.read_bytes())
    checks=review['checks'];assert review['source_only']is True and review['all_checks_passed']is True and review['blockers']==[] and type(review['check_count'])is int and review['check_count']==len(checks)and len({c['check']for c in checks})==len(checks)and all(type(c['passed'])is bool and c['passed']is True for c in checks)
    sourcecheck=json.loads((P/'ACTUAL_AUTHOR_FINAL_SOURCE_CHECK_TOOL_RETURN.json').read_bytes());tool=sourcecheck['terminal_tool_return']
    assert sourcecheck['closed']is True and sourcecheck['observed_terminal']is True and type(tool['exit_code'])is int and tool['exit_code']==0 and 'session_id'not in tool
    assert json.loads(tool['output'])['actual_report_pin']==pin(report)
    allfiles=[p for p in sorted(P.rglob('*'))if p.is_file()];assert not (P/'MANIFEST.json').exists()
    py=0;members=[]
    for path in allfiles:
        if path.suffix=='.py':ast.parse(path.read_bytes());py+=1
        members.append(dict(relative_path=str(path.relative_to(P)),fullpin=pin(path)))
    mf=P/'MANIFEST.json'
    with mf.open('x')as f:f.write('{}\n')
    directories={str(p):ident(p.lstat())for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}
    assert all(not p.is_symlink()for p in [P,*sorted(P.rglob('*'))])
    contract=json.loads((P/'EXPECTED_INDEPENDENT_REVIEW_SOURCE_SCOPE_CONTRACT.json').read_bytes());assert len(contract['required_author_Source_roles'])==21
    value=dict(schema='COMPLETE_N8_EXACT_OWNER_MONITOR_AND_CONTROLS_UNREADY_SOURCE_MANIFEST_V1',status='UNREADY_SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW',source_only=True,members=members,directories=directories,member_count=len(members),files_including_manifest=len(members)+1,directory_count=len(directories),complete_Python_Source_AST_count=py,required_author_Source_roles=contract['required_author_Source_roles'],original_N7_source_member_count=181,original_native_Source_member_count=1365,actual_author_report_pin=pin(report),actual_author_Source_check_tool_return_pin=pin(P/'ACTUAL_AUTHOR_FINAL_SOURCE_CHECK_TOOL_RETURN.json'),actual_candidate_or_controls_or_guard_or_API_or_PS_lsof_wait_poll_compile_material_numeric_execution=False,actual_independent_Source_review=None,actual_Root_Source_admission=None,actual_monitor_controls_qualification=None,actual_native_AB_execution=None,scientific_qualification_created=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    mf.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    assert directories=={str(p):ident(p.lstat())for p in [P,*sorted(P.rglob('*'))]if p.is_dir()}
    assert all(pin(P/r['relative_path'])==r['fullpin']for r in members)
    print(json.dumps(dict(status='SEALED_AUTHOR_UNREADY_SOURCE_ONLY_NOT_ROOT_ADMITTED_OR_EXECUTED',source_only=True,manifest_pin=pin(mf),review_pin=pin(report),members=len(members),files=len(members)+1,directories=len(directories),Source_AST_count=py,blockers=[],actual_candidate_execution=False,scientific_qualification_created=False),allow_nan=False))

if __name__=='__main__':main()
