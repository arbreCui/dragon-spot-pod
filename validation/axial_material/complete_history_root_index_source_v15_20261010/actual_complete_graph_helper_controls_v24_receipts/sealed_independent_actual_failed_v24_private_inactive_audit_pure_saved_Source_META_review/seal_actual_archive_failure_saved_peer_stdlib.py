from pathlib import Path
import hashlib, json, stat, sys, shutil

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(path):
    before = identity(path)
    assert stat.S_ISREG(before[2]) and before[3] == 1 and not path.is_symlink()
    raw = path.read_bytes()
    assert identity(path) == before and len(raw) == before[4]
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=before)

def main():
    assert len(sys.argv) == 2
    p = Path(sys.argv[1])
    assert p.is_relative_to(Path('/private/tmp')) and p.is_dir() and not (p / 'MANIFEST.json').exists()
    shutil.copyfile(__file__, p / 'seal_actual_archive_failure_saved_peer_stdlib.py')
    for src in ('/private/tmp/make_V24_saved_archive_failure_Source_META_auditor_stdlib.py', '/private/tmp/review_V24_actual_pure_archive_failure_saved_Source_META_INITIAL_FAILED.py'):
        path = Path(src)
        shutil.copyfile(path, p / 'SOURCE_AND_INDEPENDENT_AUDITOR' / path.name)
    r = json.loads((p / 'REVIEW.json').read_bytes())
    assert r['schema'] == 'INDEPENDENT_V24_ACTUAL_FAILED_PRIVATE_INACTIVE_AUDIT_PURE_SAVED_SOURCE_META_REVIEW_V1'
    assert r['status'] == 'PASS_SAVED_ACTUAL_PURE_CONTROLS_ARCHIVE_FAILURE_EVIDENCE_ONLY'
    assert r['source_only'] is True and r['all_checks_typed_true'] is True and r['blockers'] == []
    assert type(r['check_count']) is int and r['check_count'] == len(r['checks']) == 16447
    assert len({c['check'] for c in r['checks']}) == 16447
    assert all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
    assert r['actual_terminal_exit_code'] == 1 and r['actual_child_returncode'] == 0
    assert r['original_HOD_bytes'] == 80605706 > r['original_HOD_cap_bytes'] == 67108864
    assert r['current_HODE_bytes'] == 81918500 and r['large_graph_or_trace_payload_rehashed_or_decoded_by_reviewer'] is False
    assert r['frozen_D_files'] == 353 and r['frozen_D_directories'] == 30
    assert r['reviewer_candidate_helper_controller_guard_reader_API_or_business_executed'] is False
    assert r['no_numeric_replay_or_material_decode'] is True and r['no_repoll_or_retry_performed_by_reviewer'] is True
    for k in ('entire_pure_protocol_qualified', 'actual_pure_protocol_qualified', 'actual_full_current_graph_verifier_qualified', 'FreshV24_executed', 'whole_combined_build_qualified', 'whole_INPUT_admitted', 'native_RSS_qualified', 'AAA_accuracy_qualified', 'ABA_admitted', 'physical_balance_qualified'):
        assert r[k] is False
    assert r['new_actual_helper_qualification'] is None
    returns = json.loads((p / 'ACTUAL_INDEPENDENT_SAVED_REVIEW_TOOL_RETURNS.json').read_bytes())
    assert [a['actual_tool_return']['exit_code'] for a in returns['actual_tool_returns']] == [1, 0]
    assert all(type(a['actual_tool_return']['exit_code']) is int and 'session_id' not in a['actual_tool_return'] and a['closed'] is True and a['actual_observed_terminal'] is True for a in returns['actual_tool_returns'])
    assert returns['original_actual_terminal_output_preserved_exact'] is True
    manifest_path = p / 'MANIFEST.json'
    manifest_path.write_bytes(b'')
    assert not any(f.is_symlink() for f in p.rglob('*'))
    members = [pin(f) for f in sorted(p.rglob('*')) if f.is_file() and f != manifest_path]
    dirs = {f.relative_to(p).as_posix(): identity(f) for f in sorted(p.rglob('*')) if f.is_dir()}
    manifest = dict(schema='INDEPENDENT_V24_ACTUAL_PURE_ARCHIVE_FAILURE_SAVED_REVIEW_SEALED_NAMESPACE_V1', status=r['status'], source_only=True, member_count=len(members), complete_member_bytes=sum(f['size_bytes'] for f in members), members=members, directories=dirs, package_root_identity=identity(p), symlinks=[], review_pin=pin(p / 'REVIEW.json'), all_checks_typed_true=True, check_count=r['check_count'], blockers=[], actual_own_failure_return_preserved=True, actual_outer_failed=True, actual_child_controls_PASS=True, actual_protocol_qualified=False, new_actual_helper_qualification=None, large_payload_rehashed_or_decoded_by_reviewer=False, candidate_helper_guard_reader_API_or_business_executed=False)
    manifest_path.write_text(json.dumps(manifest, indent=2, allow_nan=False) + '\n')
    assert identity(p) == manifest['package_root_identity'] and all(pin(Path(f['path'])) == f for f in members)
    print(json.dumps(dict(status=r['status'], source_only=True, manifest_pin=pin(manifest_path), review_pin=pin(p / 'REVIEW.json'), member_count=len(members), full_file_count=len(members) + 1, directory_count=len(dirs), complete_member_bytes=manifest['complete_member_bytes'], check_count=r['check_count'], all_checks_typed_true=True, blockers=[], actual_child_controls_PASS=True, actual_outer_failed=True, actual_protocol_qualified=False, new_actual_helper_qualification=None), separators=(',', ':')))

if __name__ == '__main__':
    main()
