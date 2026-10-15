"""Seal only completed independent saved SOURCE/small META evidence."""
from pathlib import Path
import ast
import hashlib
import json
import stat
import sys
ROOT=Path(__file__).resolve().parent

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    before=identity(p);assert stat.S_ISREG(before[2]) and before[3]==1
    raw=p.read_bytes();assert identity(p)==before and len(raw)==before[4]
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def main():
    assert sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv)==1
    report=json.loads((ROOT/'REVIEW.json').read_bytes())
    assert report['schema']=='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_FRESH_SAVED_SOURCE_META_REVIEW_V1'
    assert report['status']=='PASS_SAVED_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_META_ONLY'
    assert report['source_only'] is True and report['all_checks_typed_true'] is True and report['blockers']==[]
    assert type(report['check_count']) is int and report['check_count']==len(report['checks'])==42
    assert all(type(c['passed']) is bool and c['passed'] is True for c in report['checks'])
    assert report['new_actual_helper_qualification'] is None and report['six_future_business_pins']==[None]*6
    assert report['gzip_payloads_or_material_arrays_opened_or_decoded'] is False
    assert all(report[k] is False for k in ['actual_complete_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','candidate_helper_guard_controller_API_or_solver_executed'])
    for k in ['actual_Root_fresh_summary_pin','actual_Root_fresh_terminal_pin','actual_complete_namespace_manifest_pin','actual_postclose_writer_tool_receipt_pin']:
        assert pin(Path(report[k]['path']))==report[k]
    actual=json.loads((ROOT/'ACTUAL_SAVED_SOURCE_META_REVIEW_TOOL_RETURN.json').read_bytes());tr=actual['terminal_tool_return']
    assert actual['source_only'] is True and actual['closed'] is True and actual['actual_tool_terminal_return_observed'] is True
    assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and tr['chunk_id']=='514729'
    assert json.loads(tr['output'])['review_pin']==pin(ROOT/'REVIEW.json') and actual['review_sha256']==pin(ROOT/'REVIEW.json')['sha256']
    target=ROOT/'MANIFEST.json';assert not target.exists();target.write_bytes(b'')
    rootid=identity(ROOT);paths=sorted(ROOT.rglob('*'));assert not any(p.is_symlink() for p in paths)
    members=[pin(p) for p in paths if p.is_file() and p!=target]
    directories={p.relative_to(ROOT).as_posix():identity(p) for p in paths if p.is_dir()}
    parsed=[]
    for p in paths:
        if p.suffix=='.py' and p.is_file():ast.parse(p.read_bytes());parsed.append(p.relative_to(ROOT).as_posix())
    value=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_FRESH_SAVED_SOURCE_META_REVIEW_SEAL_V1',source_only=True,status='SEALED_PASS_SAVED_ACTUAL_COMPLETE_FRESH_SOURCE_META_ONLY',members=members,member_count=len(members),complete_member_bytes=sum(v['size_bytes'] for v in members),directories=directories,package_root_identity=rootid,symlinks=[],review_pin=pin(ROOT/'REVIEW.json'),actual_Source_META_review_tool_receipt_pin=pin(ROOT/'ACTUAL_SAVED_SOURCE_META_REVIEW_TOOL_RETURN.json'),actual_Root_fresh_summary_pin=report['actual_Root_fresh_summary_pin'],actual_Root_fresh_terminal_pin=report['actual_Root_fresh_terminal_pin'],actual_complete_namespace_manifest_pin=report['actual_complete_namespace_manifest_pin'],check_count=report['check_count'],parsed_python_Source_files=parsed,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,candidate_helper_guard_or_API_executed=False,result_gzip_or_material_payload_redecode=False)
    target.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    assert identity(ROOT)==rootid and [pin(Path(v['path'])) for v in members]==members
    assert {p.relative_to(ROOT).as_posix():identity(p) for p in ROOT.rglob('*') if p.is_dir()}==directories
    print(json.dumps(dict(source_only=True,status=value['status'],manifest_pin=pin(target),review_pin=value['review_pin'],member_count=len(members),complete_member_bytes=value['complete_member_bytes'],directory_count=len(directories),check_count=report['check_count']),separators=(',',':')))

if __name__=='__main__':main()
