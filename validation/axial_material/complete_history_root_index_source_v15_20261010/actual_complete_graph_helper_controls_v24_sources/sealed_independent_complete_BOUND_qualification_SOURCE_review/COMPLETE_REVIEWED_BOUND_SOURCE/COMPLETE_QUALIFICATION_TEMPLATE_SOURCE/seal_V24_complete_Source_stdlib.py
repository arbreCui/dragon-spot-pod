"""Seal complete unexecuted Source only, preserving all original bytes."""
from pathlib import Path
import ast
import hashlib
import json
import stat
import sys
ROOT=Path(__file__).resolve().parent
ROLES=('pure_helper_controls.UNREADY.py','pure_helper_controls_host.UNREADY.py','fresh_verifier_controls.UNREADY.py','fresh_verifier_host.UNREADY.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py')

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    before=identity(p);assert stat.S_ISREG(before[2]) and before[3]==1
    raw=p.read_bytes();assert len(raw)==before[4] and identity(p)==before
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=before)

def main():
    assert len(sys.argv)==1 and sys.dont_write_bytecode and not sys.flags.optimize
    r=json.loads((ROOT/'SOURCE_SELF_REVIEW.json').read_bytes())
    assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
    assert type(r['check_count']) is int and r['check_count']==len(r['checks'])==1670
    assert all(type(x['passed']) is bool and x['passed'] is True for x in r['checks'])
    receipt=json.loads((ROOT/'ACTUAL_V24_SOURCE_AUTHOR_TOOL_RETURN.json').read_bytes());tr=receipt['terminal_tool_return']
    assert receipt['source_only'] is True and receipt['closed'] is True and receipt['actual_tool_terminal_return_observed'] is True
    assert type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and tr['chunk_id']=='331a15'
    observed=json.loads(tr['output']);assert observed['review_pin']==pin(ROOT/'SOURCE_SELF_REVIEW.json')
    assert observed['module_pin']==pin(ROOT/ROLES[-1]) and observed['role_pins']=={name:pin(ROOT/name) for name in ROLES}
    inverse=json.loads((ROOT/'V24_COMPLETE_MODULE_CONTROLLER_BINDER_SOURCE_INVERSE.json').read_bytes())
    for name,item in inverse['all_complete_Source_finite_inverse'].items():
        s=(ROOT/name).read_text()
        for h in reversed(item['full_hunks']):
            assert s.count(h['new_utf8'])==1
            s=s.replace(h['new_utf8'],h['old_utf8'],1)
        old=Path(item['original_pin']['path']).read_bytes()
        assert s.encode()==old and ast.dump(ast.parse(s),include_attributes=False)==ast.dump(ast.parse(old),include_attributes=False)
        assert pin(ROOT/name)==item['new_pin'] and pin(Path(item['original_pin']['path']))==item['original_pin']
    manifest=ROOT/'MANIFEST.json';assert not manifest.exists();manifest.write_bytes(b'')
    rootid=identity(ROOT);paths=sorted(ROOT.rglob('*'));assert not any(p.is_symlink() for p in paths)
    members=[pin(p) for p in paths if p.is_file() and p!=manifest]
    dirs={p.relative_to(ROOT).as_posix():identity(p) for p in paths if p.is_dir()}
    py=[]
    for p in paths:
        if p.is_file() and p.suffix=='.py':ast.parse(p.read_bytes());py.append(p.relative_to(ROOT).as_posix())
    plan=json.loads((ROOT/'ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json').read_bytes())
    for kind in ('pure','fresh'):
        assert all('v24' in path for path in plan['namespaces'][kind].values())
    m=dict(schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_PURE_FRESH_SOURCE_PACKAGE_V1',source_only=True,status='SEALED_COMPLETE_V24_UNREADY_SOURCE_NO_EXECUTION_OR_QUALIFICATION',members=members,member_count=len(members),complete_member_bytes=sum(v['size_bytes'] for v in members),directories=dirs,package_root_identity=rootid,symlinks=[],templates_and_control_module={name:pin(ROOT/name) for name in ROLES},source_binding_generator_pin=pin(ROOT/'bind_complete_qualification_SOURCE_only.py'),full_original_Source_inverse_pin=pin(ROOT/'V24_COMPLETE_MODULE_CONTROLLER_BINDER_SOURCE_INVERSE.json'),complete_Source_self_review_pin=pin(ROOT/'SOURCE_SELF_REVIEW.json'),actual_Source_author_tool_receipt_pin=pin(ROOT/'ACTUAL_V24_SOURCE_AUTHOR_TOOL_RETURN.json'),complete_original_parent_manifest_pin=r['complete_original_parent_manifest_pin'],complete_original_parent_files=125,complete_original_pure_Source_files=61,complete_original_fresh_Source_files=13,new_complete_helper_Source_sha256='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',pure_added_controls=dict(positive=5,reject=13,failure=3),complete_fresh_public_return_fields=27,complete_fresh_canonical_files=37111,complete_fresh_actual_read_records=37112,complete_fresh_original_lossless_gzip_files=3,private_state_original_tuple_metadata_and_actual_object_identity_preserved=True,seven_private_state_module_comparisons_replaced=True,public_nine_fields_comparator_byteexact=True,full_fresh_subprocess_absence_precondition_preserved=True,original_actual_V23_helper_Source_install_schema_and_fact_reused=True,new_actual_helper_qualification=None,six_future_business_pins=[None]*6,Source_candidate_controller_helper_guard_reader_API_or_binding_executed=False,any_RSS_or_build_or_science_pass_prediction=None,parsed_python_files=py)
    manifest.write_text(json.dumps(m,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    assert identity(ROOT)==rootid
    assert [pin(Path(v['path'])) for v in members]==members
    assert {p.relative_to(ROOT).as_posix():identity(p) for p in ROOT.rglob('*') if p.is_dir()}==dirs
    print(json.dumps(dict(status=m['status'],source_only=True,manifest_pin=pin(manifest),member_count=len(members),complete_member_bytes=m['complete_member_bytes'],directory_count=len(dirs),module_pin=pin(ROOT/ROLES[-1]),Source_self_review_pin=pin(ROOT/'SOURCE_SELF_REVIEW.json'),check_count=1670),separators=(',',':')))

if __name__=='__main__':main()
