"""Verify fixed namespace-only report/MF complete bytes after real Source seal."""
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
    before=ident(path.lstat());assert stat.S_ISREG(before[2])and before[3]==1
    with path.open('rb')as f:assert ident(os.fstat(f.fileno()))==before;raw=f.read();assert len(raw)==before[4]and f.read(1)==b''and ident(os.fstat(f.fileno()))==before
    assert ident(path.lstat())==before
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)
def main():
    seal_path=S/'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json';seal=json.loads(seal_path.read_bytes());t=seal['terminal_tool_return']
    assert seal['closed']is True and seal['observed_terminal']is True and type(t['exit_code'])is int and t['exit_code']==0 and 'session_id'not in t and t['chunk_id']==seal['actual_terminal_chunk']
    out=json.loads(t['output']);mp=F/'MANIFEST.json';m=json.loads(mp.read_bytes());assert pin(mp)==out['manifest_pin']
    assert {str(p.relative_to(F))for p in F.rglob('*')if p.is_file()}==set(m['members'])|{'MANIFEST.json'}
    assert {'.':ident(F.lstat()),**{str(p.relative_to(F)):ident(p.lstat())for p in F.rglob('*')if p.is_dir()}}==m['directories']
    py=0
    for rel,expected in m['members'].items():
        assert pin(F/rel)==expected
        if rel.endswith('.py'):ast.parse((F/rel).read_bytes());py+=1
    r=json.loads((F/'REVIEW.json').read_bytes());assert pin(F/'REVIEW.json')==out['review_pin']and r['all_checks_typed_true']is True and r['blockers']==[]
    results=json.loads((F/'COMPLETE_NAMESPACE_SOURCE_EOF_AND_INVERSE_RESULTS.json').read_bytes())
    for key in ('candidate_members','qualified_base_members'):
        for p in results[key].values():assert pin(Path(p['path']))==p
    assert pin(Path(r['qualified_complete_Source_manifest_pin']['path']))==r['qualified_complete_Source_manifest_pin']
    value=dict(schema='INDEPENDENT_V25_CAPTURE_NAMESPACE_ONLY_SOURCE_FULL_POSTSEAL_V1',status='FULL_SOURCE_POSTSEAL_VERIFIED_SOURCE_ONLY_NOT_ROOT_ADMITTED',source_only=True,qualification_scope=r['qualification_scope'],manifest_pin=pin(mp),review_pin=out['review_pin'],files=len(m['members'])+1,directories=len(m['directories']),complete_Source_AST_count=py,actual_review_terminal_chunk='cff257',actual_seal_terminal_chunk=seal['actual_terminal_chunk'],blockers=[],actual_candidate_guard_API_compile_native_or_numeric_executed=False,scientific_qualification_created=False)
    target=S/'FULL_SOURCE_POSTSEAL_VERIFICATION.json'
    with target.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    print(json.dumps(dict(status=value['status'],source_only=True,manifest_pin=pin(mp),review_pin=out['review_pin'],postseal_verification_pin=pin(target),files=value['files'],directories=value['directories'],blockers=[],actual_candidate_execution=False),allow_nan=False))

if __name__=='__main__':main()
