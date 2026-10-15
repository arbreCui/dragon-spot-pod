"""Full EOF/hash/7ID SOURCE seal only; no reviewed Source is executed."""
from pathlib import Path
import hashlib
import json
import stat

P = Path(__file__).parent

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(path):
    before = identity(path)
    assert stat.S_ISREG(before[2]) and before[3] == 1
    raw = path.read_bytes()
    assert before == identity(path) and len(raw) == before[4]
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=before)

review = json.loads((P / 'FINAL_FULL_SOURCE_SCOPE_REVIEW.json').read_bytes())
assert review['source_only'] is True and review['all_checks_typed_true'] is True
assert review['blockers'] == [] and len(review['checks']) == review['check_count'] and review['check_count'] >= 218
assert all(type(item['passed']) is bool and item['passed'] is True for item in review['checks'])
first = json.loads((P / 'SOURCE_SELF_REVIEW.json').read_bytes())
assert first['all_checks_typed_true'] is True and first['check_count'] == 168
for path, original in first['complete_original_source_and_META_pins_before_after'].items():
    assert pin(Path(path)) == original
manifest = P / 'MANIFEST.json'
assert not manifest.exists()
manifest.write_bytes(b'')
root_before = identity(P)
members = [pin(path) for path in sorted(P.rglob('*')) if path.is_file() and path != manifest]
directories = {path.relative_to(P).as_posix(): identity(path) for path in sorted(P.rglob('*')) if path.is_dir()}
assert not any(path.is_symlink() for path in P.rglob('*'))
roles = review['qualified_template_Source_pins']
assert all(pin(Path(value['path'])) == value for value in roles.values())
value = dict(schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_PURE_FRESH_SOURCE_PACKAGE_V1',
             source_only=True, status='SEALED_COMPLETE_UNREADY_SOURCE_NO_EXECUTION_OR_QUALIFICATION',
             members=members, member_count=len(members), complete_member_bytes=sum(m['size_bytes'] for m in members),
             directories=directories, package_root_identity=root_before, symlinks=[],
             complete_original_pure_Source_files=61, complete_original_fresh_Source_files=13,
             full_new_helper_candidate_members_plus_manifest=22,
             original_helper_Source_peer_check_count=479, original_helper_Source_peer_unique_label_count=429,
             templates_and_control_module=roles, source_binding_generator_pin=pin(P/'bind_complete_qualification_SOURCE_only.py'),
             full_original_Source_inverse_pin=pin(P/'ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json'),
             complete_Source_self_review_pin=pin(P/'SOURCE_SELF_REVIEW.json'),
             complete_final_Source_scope_review_pin=pin(P/'FINAL_FULL_SOURCE_SCOPE_REVIEW.json'),
             new_complete_helper_Source_sha256='3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092',
             pure_added_controls=dict(positive=5, reject=13, last_use_failure=3),
             complete_fresh_public_return_fields=27, complete_fresh_canonical_files=37111,
             complete_fresh_actual_read_records=37112, complete_fresh_original_lossless_gzip_files=3,
             new_actual_helper_qualification=None, six_future_business_pins=[None]*6,
             Source_candidate_controller_helper_guard_reader_API_or_binding_executed=False,
             any_RSS_or_build_or_science_pass_prediction=None)
manifest.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')
assert identity(P) == root_before
assert {path.relative_to(P).as_posix(): identity(path) for path in P.rglob('*') if path.is_dir()} == directories
assert [pin(Path(m['path'])) for m in members] == members
assert len([path for path in P.rglob('*') if path.is_file()]) == len(members)+1
print(json.dumps(dict(source_only=True, status='FULL_SOURCE_PACKAGE_SEALED_NOT_EXECUTED',
                     manifest_pin=pin(manifest), member_count=len(members), full_file_count=len(members)+1,
                     complete_member_bytes=value['complete_member_bytes'], directory_count=len(directories),
                     package_root_identity=root_before, new_actual_helper_qualification=None,
                     six_future_business_pins=[None]*6),separators=(',',':')))
