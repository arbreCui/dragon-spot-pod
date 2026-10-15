from pathlib import Path
import hashlib,json,stat,sys

def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(p):
    a=identity(p);assert stat.S_ISREG(a[2]) and a[3]==1 and not p.is_symlink()
    raw=p.read_bytes();assert identity(p)==a and len(raw)==a[4]
    return dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=a)

def main():
    assert len(sys.argv)==2;p=Path(sys.argv[1]);s=Path(str(p)+'_seal_receipt');assert p.is_relative_to(Path('/private/tmp')) and s.is_dir()
    mp=pin(p/'MANIFEST.json');m=json.loads((p/'MANIFEST.json').read_bytes())
    receiptpin=pin(s/'ACTUAL_INDEPENDENT_V25_SAVED_PURE_REVIEW_SEAL_TOOL_RETURN.json');receipt=json.loads(Path(receiptpin['path']).read_bytes());t=receipt['actual_tool_return']
    assert receipt['closed'] is True and receipt['actual_observed_terminal'] is True and receipt['original_actual_stdout_preserved_exact'] is True
    assert type(t['exit_code']) is int and t['exit_code']==0 and 'session_id' not in t
    actual=json.loads(t['output']);assert actual['manifest_pin']==mp and actual['review_pin']==pin(p/'REVIEW.json') and actual['aggregate_main_check_count']==55 and actual['supplemental_complete_small_control_check_count']==136
    assert m['status']=='PASS_SAVED_ACTUAL_PURE_CONTROLS_SOURCE_META_ONLY' and m['all_checks_typed_true'] is True and m['blockers']==[] and m['new_actual_helper_qualification'] is None
    assert identity(p)==m['package_root_identity'] and not any(f.is_symlink() for f in p.rglob('*'))
    current=[pin(f) for f in sorted(p.rglob('*')) if f.is_file() and f!=p/'MANIFEST.json'];dirs={f.relative_to(p).as_posix():identity(f) for f in sorted(p.rglob('*')) if f.is_dir()}
    assert current==m['members'] and dirs==m['directories'] and len(current)==m['member_count'] and sum(v['size_bytes'] for v in current)==m['complete_member_bytes']
    dest=s/'FULL_INDEPENDENT_V25_SAVED_PURE_REVIEW_POSTSEAL_VERIFICATION.json';assert not dest.exists()
    r=dict(schema='INDEPENDENT_V25_SAVED_ACTUAL_COMPLETE_PURE_REVIEW_FULL_POSTSEAL_VERIFICATION_V1',status=m['status'],source_only=True,complete_all_declared_members_fullEOF_SHA7ID_verified=True,complete_all_declared_directories_root_exact=True,actual_independent_seal_stdout_exact_Python_integer_pins_verified=True,strict_actual_seal_EXIT0_no_session=True,manifest_pin=mp,review_pin=pin(p/'REVIEW.json'),actual_seal_tool_receipt_pin=receiptpin,member_count=len(current),full_file_count=len(current)+1,directory_count=len(dirs),complete_member_bytes=m['complete_member_bytes'],aggregate_main_check_count=55,supplemental_complete_small_control_check_count=136,all_checks_typed_true=True,blockers=[],actual_pure_outer_child_EXIT0_evidence_verified=True,new_actual_helper_qualification=None,large_original_graph_trace_payload_rehashed_or_decoded=False,reviewer_helper_candidate_guard_API_or_business_executed=False)
    dest.write_text(json.dumps(r,indent=2,allow_nan=False)+'\n')
    assert pin(p/'MANIFEST.json')==mp and identity(p)==m['package_root_identity'] and current==[pin(Path(v['path'])) for v in current] and dirs=={f.relative_to(p).as_posix():identity(f) for f in sorted(p.rglob('*')) if f.is_dir()}
    print(json.dumps(dict(status=m['status'],source_only=True,manifest_pin=mp,review_pin=pin(p/'REVIEW.json'),postseal_verification_pin=pin(dest),actual_seal_tool_receipt_pin=receiptpin,full_file_count=len(current)+1,aggregate_main_check_count=55,supplemental_complete_small_control_check_count=136,all_checks_typed_true=True,blockers=[],new_actual_helper_qualification=None),separators=(',',':')))

if __name__=='__main__':main()
