"""Only seal an already completed independent SOURCE review; no API execution."""
from pathlib import Path
import ast
import hashlib
import json
import stat
import sys

ROOT=Path(__file__).resolve().parent
BOUND=Path('/private/tmp/axmat_inactive_audit_v23_actual_COMPLETE_BOUND_SOURCE_ROOT_20261010_10a0e4')

def identity(path):
    s=path.lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    before=identity(path)
    assert stat.S_ISREG(before[2]) and before[3]==1
    raw=path.read_bytes()
    assert len(raw)==before[4] and identity(path)==before
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def main():
    assert len(sys.argv)==1 and sys.dont_write_bytecode and not sys.flags.optimize
    report=json.loads((ROOT/'REVIEW.json').read_bytes())
    assert report['schema']=='INDEPENDENT_V23_ACTUAL_COMPLETE_BOUND_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_REVIEW_V1'
    assert report['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'
    assert report['source_only'] is True and report['all_checks_typed_true'] is True and report['blockers']==[]
    assert type(report['check_count']) is int and report['check_count']==len(report['checks'])==6696
    assert all(type(c['passed']) is bool and c['passed'] is True for c in report['checks'])
    assert pin(Path(report['bound_manifest_pin']['path']))==report['bound_manifest_pin']
    assert report['new_actual_helper_qualification'] is None and report['six_future_business_pins']==[None]*6
    actual=json.loads((ROOT/'ACTUAL_COMPLETE_BOUND_SOURCE_REVIEW_TOOL_RETURN.json').read_bytes())
    assert actual['source_only'] is True and actual['closed'] is True and actual['actual_tool_terminal_return_observed'] is True
    tr=actual['terminal_tool_return']
    assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr
    assert tr['chunk_id']=='7fddd8' and json.loads(tr['output'])['review_pin']==pin(ROOT/'REVIEW.json')
    assert actual['review_sha256']==pin(ROOT/'REVIEW.json')['sha256']
    evidence=json.loads((ROOT/'FULL_SOURCE_AND_META_PINS_BEFORE_AFTER.json').read_bytes())
    before=evidence['bound_after']
    assert identity(BOUND)==before['root_identity']
    assert {p.relative_to(BOUND).as_posix():identity(p) for p in BOUND.rglob('*') if p.is_dir()}==before['directories']
    assert {p.relative_to(BOUND).as_posix():pin(p) for p in BOUND.rglob('*') if p.is_file()}==before['files']
    manifest=ROOT/'MANIFEST.json'
    assert not manifest.exists()
    manifest.write_bytes(b'')
    root_id=identity(ROOT)
    paths=sorted(ROOT.rglob('*'))
    assert not any(p.is_symlink() for p in paths)
    members=[pin(p) for p in paths if p.is_file() and p!=manifest]
    dirs={p.relative_to(ROOT).as_posix():identity(p) for p in paths if p.is_dir()}
    parsed=[]
    for p in paths:
        if p.is_file() and p.suffix=='.py':
            ast.parse(p.read_bytes());parsed.append(p.relative_to(ROOT).as_posix())
    value=dict(schema='INDEPENDENT_V23_ACTUAL_COMPLETE_BOUND_QUALIFICATION_SOURCE_REVIEW_SEAL_V1',source_only=True,status='SEALED_SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION',members=members,member_count=len(members),complete_member_bytes=sum(x['size_bytes'] for x in members),directories=dirs,package_root_identity=root_id,symlinks=[],review_pin=pin(ROOT/'REVIEW.json'),bound_manifest_pin=report['bound_manifest_pin'],actual_Source_review_tool_receipt_pin=pin(ROOT/'ACTUAL_COMPLETE_BOUND_SOURCE_REVIEW_TOOL_RETURN.json'),check_count=report['check_count'],parsed_python_files=parsed,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,helper_guard_or_controller_API_executed=False,any_numeric_or_material_decode=False)
    manifest.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    assert identity(ROOT)==root_id
    assert {p.relative_to(ROOT).as_posix():identity(p) for p in ROOT.rglob('*') if p.is_dir()}==dirs
    assert [pin(Path(v['path'])) for v in members]==members
    print(json.dumps(dict(status=value['status'],source_only=True,manifest_pin=pin(manifest),member_count=len(members),complete_member_bytes=value['complete_member_bytes'],directory_count=len(dirs),review_pin=value['review_pin'],actual_Source_review_tool_receipt_pin=value['actual_Source_review_tool_receipt_pin'],check_count=report['check_count']),separators=(',',':')))

if __name__=='__main__':
    main()
