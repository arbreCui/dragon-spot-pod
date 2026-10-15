from pathlib import Path
import hashlib,json,stat,sys,shutil

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    a=identity(p);assert stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink()
    raw=p.read_bytes();assert identity(p)==a and len(raw)==a[4]
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)

def main():
    assert len(sys.argv)==2;p=Path(sys.argv[1]);assert p.is_relative_to(Path('/private/tmp')) and p.is_dir() and not (p/'MANIFEST.json').exists()
    shutil.copyfile(__file__,p/'seal_V25_actual_complete_pure_saved_peer_stdlib.py')
    r=json.loads((p/'REVIEW.json').read_bytes())
    assert r['schema']=='INDEPENDENT_V25_ACTUAL_SUCCESS_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1' and r['status']=='PASS_SAVED_ACTUAL_PURE_CONTROLS_SOURCE_META_ONLY'
    assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers']==[]
    assert type(r['check_count']) is int and r['check_count']==len(r['checks'])==55 and len({c['check'] for c in r['checks']})==55 and all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
    assert r['actual_outer_exit_code']==r['actual_child_returncode']==0 and r['full_frozen_D_files']==9 and r['full_original_E_files']==3
    assert r['complete_bound_Source_archive_files']==184 and r['complete_bound_Source_peer_archive_files']==199 and r['full_Source_streamed_bytes_hash_verified'] is True and r['all_five_direct_Source_original_bytes_verified'] is True
    assert r['original_HOD_bytes']==62499039<r['original_cap_bytes']==67108864 and r['current_HODE_bytes']==63392917<r['original_cap_bytes']
    assert r['new_actual_helper_qualification'] is None and r['large_graph_trace_payload_rehashed_or_decoded'] is False and r['reviewer_candidate_helper_controller_guard_reader_API_or_business_executed'] is False
    assert all(r[k] is False for k in ('actual_full_current_graph_fresh_verifier_qualified','whole_combined_build_qualified','whole_INPUT_admitted','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified'))
    receipts=json.loads((p/'ACTUAL_INDEPENDENT_SOURCE_META_INSPECTION_AND_REVIEW_TOOL_RETURNS.json').read_bytes());actual=receipts['records'][-1]['actual_tool_return']
    assert type(actual['exit_code']) is int and actual['exit_code']==0 and 'session_id' not in actual and actual['chunk_id']=='6fa312'
    actual_stdout=json.loads(actual['output']);assert actual_stdout['review_dir']==str(p) and actual_stdout['review_sha256']==pin(p/'REVIEW.json')['sha256'] and actual_stdout['check_count']==55
    supplemental=json.loads((p/'DELEGATED_SAVED_CONTROLS_ACTUAL_EVIDENCE.json').read_bytes())
    assert supplemental['all_checks_typed_true'] is True and supplemental['check_count']==136 and supplemental['source_only'] is True
    assert supplemental['helper_candidate_guard_API_or_numeric_executed'] is False
    assert type(supplemental['actual_success_tool_return']['exit_code']) is int and supplemental['actual_success_tool_return']['exit_code']==0 and supplemental['actual_success_tool_return']['chunk_id']=='2276a3' and 'session_id' not in supplemental['actual_success_tool_return']
    mf=p/'MANIFEST.json';mf.write_bytes(b'')
    assert not any(f.is_symlink() for f in p.rglob('*'))
    members=[pin(f) for f in sorted(p.rglob('*')) if f.is_file() and f!=mf]
    dirs={f.relative_to(p).as_posix():identity(f) for f in sorted(p.rglob('*')) if f.is_dir()}
    m=dict(schema='INDEPENDENT_V25_ACTUAL_COMPLETE_PURE_SAVED_SOURCE_META_REVIEW_SEALED_NAMESPACE_V1',status=r['status'],source_only=True,members=members,member_count=len(members),complete_member_bytes=sum(v['size_bytes'] for v in members),directories=dirs,package_root_identity=identity(p),symlinks=[],review_pin=pin(p/'REVIEW.json'),actual_Root_pure_summary_pin=r['actual_Root_pure_summary_pin'],actual_Root_terminal_receipt_pin=r['actual_Root_terminal_receipt_pin'],actual_complete_HODE_namespace_manifest_pin=r['actual_complete_HODE_namespace_manifest_pin'],all_checks_typed_true=True,aggregate_main_check_count=55,supplemental_complete_small_control_check_count=136,blockers=[],actual_pure_outer_and_child_EXIT0_evidence_verified=True,original_caps_unchanged=True,new_actual_helper_qualification=None,large_graph_trace_payload_rehashed_or_decoded=False,reviewer_candidate_helper_guard_API_or_business_executed=False,actual_own_finite_inspection_failures_preserved=True)
    mf.write_text(json.dumps(m,indent=2,allow_nan=False)+'\n')
    assert identity(p)==m['package_root_identity'] and all(pin(Path(v['path']))==v for v in members)
    print(json.dumps(dict(status=r['status'],source_only=True,manifest_pin=pin(mf),review_pin=pin(p/'REVIEW.json'),member_count=len(members),full_file_count=len(members)+1,directory_count=len(dirs),complete_member_bytes=m['complete_member_bytes'],aggregate_main_check_count=55,supplemental_complete_small_control_check_count=136,all_checks_typed_true=True,blockers=[],new_actual_helper_qualification=None),separators=(',',':')))

if __name__=='__main__':main()
