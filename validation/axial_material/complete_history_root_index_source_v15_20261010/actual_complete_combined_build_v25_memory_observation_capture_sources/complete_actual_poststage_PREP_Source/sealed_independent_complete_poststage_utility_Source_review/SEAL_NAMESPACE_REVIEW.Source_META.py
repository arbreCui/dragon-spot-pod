"""Seal the finite namespace-only verdict, no candidate/module/API execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

F=Path('/private/tmp/axmat_INDEPENDENT_V25_capture_namespace_Source_f8j_l6gn')
S=Path(str(F)+'_seal_receipt')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    s=ident(path.lstat());assert stat.S_ISREG(s[2])and s[3]==1 and all(not q.is_symlink()for q in(path,*path.parents))
    with path.open('rb')as f:assert ident(os.fstat(f.fileno()))==s;raw=f.read();assert len(raw)==s[4]and f.read(1)==b'' and ident(os.fstat(f.fileno()))==s
    assert ident(path.lstat())==s
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=s)
def main():
    review=json.loads((F/'REVIEW.json').read_bytes());truth=json.loads((F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json').read_bytes());t=truth['terminal_tool_return'];stdout=json.loads(t['output'])
    assert review['status']=='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION'and review['source_only']is True and review['all_checks_typed_true']is True and review['blockers']==[]
    assert review['check_count']==len(review['checks'])==206 and len({r['name']for r in review['checks']})==206 and all(type(r['passed'])is bool and r['passed']is True for r in review['checks'])
    assert truth['closed']is True and truth['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==truth['actual_terminal_chunk']=='cff257'
    assert stdout['review_pin']==pin(F/'REVIEW.json')and stdout['qualified_complete_Source_manifest_pin']==review['qualified_complete_Source_manifest_pin']
    mp=F/'MANIFEST.json';assert not mp.exists();mp.touch()
    files={};dirs={'.':ident(F.lstat())};py=0
    for p in sorted(F.rglob('*')):
        assert not p.is_symlink()
        if p.is_dir():dirs[str(p.relative_to(F))]=ident(p.lstat())
        elif p!=mp:
            files[str(p.relative_to(F))]=pin(p)
            if p.suffix=='.py':ast.parse(p.read_bytes());py+=1
    value=dict(schema='INDEPENDENT_V25_CAPTURE_NAMESPACE_ONLY_SOURCE_REVIEW_PACKAGE_V1',source_only=True,status=review['status'],members=files,directories=dirs,member_count=len(files),qualification_scope=review['qualification_scope'],memory_implementation_reassessment_performed=False,actual_Source_review_exit_int=0,Source_verdict_qualification_granted=True,candidate_or_business_executed=False)
    mp.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n');assert dirs=={'.':ident(F.lstat()),**{str(p.relative_to(F)):ident(p.lstat())for p in F.rglob('*')if p.is_dir()}}
    assert all(pin(F/rel)==p for rel,p in files.items());S.mkdir()
    print(json.dumps(dict(status='SEALED_SOURCE_ONLY_PASS_NO_RUNTIME_OR_SCIENCE_CREDIT',source_only=True,qualification_scope=review['qualification_scope'],manifest_pin=pin(mp),review_pin=pin(F/'REVIEW.json'),candidate_manifest_pin=review['qualified_complete_Source_manifest_pin'],actual_Source_review_tool_return_pin=pin(F/'ACTUAL_SOURCE_REVIEW_TOOL_RETURN.json'),members=len(files),files=len(files)+1,directories=len(dirs),Source_AST_count=py,blockers=[],actual_candidate_execution=False,scientific_qualification_created=False),allow_nan=False))

if __name__=='__main__':main()
