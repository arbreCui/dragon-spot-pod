import hashlib
import json
import os
import stat
from pathlib import Path

ROOT = Path('/Users/wen/spot')
R = ROOT / 'validation/storage_cleanup_fourteenth_20261009'
O = Path('/private/tmp/spot_storage_fourteenth_exact5_actual_post_independent_review_20261009')
PRE = Path('/private/tmp/spot_storage_fourteenth_exact5_preexec_independent_review_20261009')
PINS = {}


def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]


def pin(path, expected=None):
    path = Path(path)
    before = identity(path)
    assert stat.S_ISREG(before[2]) and before[-1] == 1 and path.resolve() == path
    h = hashlib.sha256()
    with path.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink] == before
        while chunk := stream.read(1024 ** 2):
            h.update(chunk)
    assert identity(path) == before
    result = dict(path=str(path), sha256=h.hexdigest(), size_bytes=before[3], identity=before)
    if expected is not None:
        assert result['sha256'] == expected
    PINS[str(path)] = result
    return result


def pairs(items):
    result = {}
    for key, value in items:
        assert key not in result
        result[key] = value
    return result


def read(path, expected=None):
    bound = pin(path, expected)
    result = json.loads(Path(path).read_text(), object_pairs_hook=pairs)
    assert identity(path) == bound['identity']
    return result


def fingerprint(excluded):
    h = hashlib.sha256()
    files_count = links_count = dirs_count = 0
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        dirs.sort()
        files.sort()
        dirs[:] = [name for name in dirs if Path(base) / name not in (ROOT / '.git', R)]
        for name in dirs + files:
            path = Path(base) / name
            if str(path) in excluded:
                continue
            s = path.lstat()
            if stat.S_ISREG(s.st_mode):
                row = [str(path.relative_to(ROOT)), s.st_dev, s.st_ino, s.st_mode,
                       s.st_nlink, s.st_size, s.st_blocks, s.st_mtime_ns, s.st_ctime_ns]
                files_count += 1
            elif stat.S_ISLNK(s.st_mode):
                row = [str(path.relative_to(ROOT)), 'symlink', os.readlink(path)]
                links_count += 1
            elif stat.S_ISDIR(s.st_mode):
                row = [str(path.relative_to(ROOT)), 'directory_path']
                dirs_count += 1
            else:
                continue
            h.update(json.dumps(row, separators=(',', ':')).encode() + b'\n')
    return dict(sha256=h.hexdigest(), regular_files=files_count,
                symlinks=links_count, directory_paths=dirs_count)


assert __debug__
source = R / 'manage_old_runtime_copies.py'
helper = R / 'manage_audit_metadata.py'
plan_path = R / 'old_runtime_dependency_review/exact5_runtime_candidates.json'
manifest_path = R / 'runtime_retirement_manifest.json'
pin(source, '0ec862f16b566add1eea3ad6610237b34763dee45ea4862457ef22cdcd47f14f')
pin(helper, '886be02cde541acd00e922d5f67965250ca1b50dc8302e374904b3f0839d541d')
plan = read(plan_path, '02f7ffe3c5775e381c2326cc766dc3f9274590635fda8838338c30e55835d4ee')
manifest = read(manifest_path, '00b3ff33f045f825137763dca4dbaffa61d013c92e0e3c5e946d4e72eb1f1096')
pre = read(PRE / 'REPORT.json', 'b1b2c049d3b65f601cfb3d8ca398d0c0da77969083a04c5982350a3a0bd7c198')
pre_tool = read(PRE / 'actual_readonly_tool_return.json', 'dc89650ff16d69579d0b1459be198f08a55b445859cd269f71ce9d98637f64ab')
assert pre['status'] == 'PASS'
# Pin the sealed genuine pre-execution result without re-executing its reader.
assert pre_tool['report_pin']['sha256'] == PINS[str(PRE / 'REPORT.json')]['sha256']
assert pre_tool['actual_tool_result'] == dict(initial_chunk_id='6f2fc1', session_id=78561, terminal_chunk_id='a752d3', exit_code=0, closed=True)
assert type(pre_tool['actual_tool_result']['exit_code']) is int
pin(PRE / 'review_prepared_readonly.py', pre_tool['source_sha256'])
for stream_key in ('full_stdout', 'full_stderr'):
    stream_pin = pin(pre_tool[stream_key]['path'], pre_tool[stream_key]['sha256'])
    assert stream_pin['size_bytes'] == pre_tool[stream_key]['size_bytes']
assert pre_tool['full_stderr']['size_bytes'] == 0
rows = plan['candidates']
assert len(rows) == 5 and [row['version'] for row in rows] == [2, 3, 4, 5, 6]
assert manifest['candidates'] == rows and manifest['kind'] == 'FIVE_EXACT_OLD_FAILED_RUNTIME_COPIES_ONLY'
assert manifest['source_sha256'] == PINS[str(source)]['sha256']
assert manifest['helper_sha256'] == PINS[str(helper)]['sha256']
assert manifest['plan_sha256'] == PINS[str(plan_path)]['sha256']
assert manifest['scientific_credit'] is False
expected_paths = [str(ROOT / 'validation/artifacts' / (
    f'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-'
    f'last-cprime-trim-live-resource-scopes-v{version}-20261008/runtime/Dragon'
)) for version in range(2, 7)]
assert [row['path'] for row in rows] == expected_paths
assert all(not os.path.lexists(path) for path in expected_paths)
primary = rows[0]['retained_primary']
assert all(row['retained_primary'] == primary for row in rows)
assert primary['path'] == str(ROOT / 'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/runtime/Dragon')
assert primary['sha256'] == '77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba'
master = pin(primary['path'], primary['sha256'])
assert master['identity'] == primary['identity'] and master['size_bytes'] == primary['size_bytes'] == 9225720
assert Path(primary['path']).stat().st_blocks * 512 == primary['allocated_bytes'] == 9228288

result_path = R / 'runtime_retirement_result.json'
result = read(result_path, '20060a888dac5e9a21b6d4e1250579833a40e0dd16dd97347ae064d3eaf8c9c2')
observation_path = R / 'Root_actual_runtime_retirement_observation.json'
observation = read(observation_path, '658c5c026381c26e0cc61a5d39ccc30cee9e2fd3fafb7dae0015544058dae283')
assert result['status'] == 'FIVE_RETIRED' and result['deleted_paths'] == expected_paths
assert result['manifest_sha256'] == PINS[str(manifest_path)]['sha256']
assert result['allocated_bytes'] == sum(row['allocated_bytes'] for row in rows) == 46141440
assert result['old_failure_promoted'] is False and result['scientific_credit'] is False
assert observation['kind'] == 'ROOT_ACTUAL_FIXED_FIVE_RUNTIME_RETIREMENT'
assert observation['manifest_sha256'] == PINS[str(manifest_path)]['sha256']
assert observation['source_sha256'] == PINS[str(source)]['sha256']
assert observation['result_sha256'] == PINS[str(result_path)]['sha256']
assert observation['deleted_paths'] == expected_paths and observation['retained_primary'] == primary
assert observation['allocated_bytes'] == result['allocated_bytes']
tool = observation['actual_tool']
assert tool == dict(initial_chunk='c1cb49', session_id=89290, terminal_chunk='51643e', actual_exit_code=0, closed=True)
assert type(tool['actual_exit_code']) is int and tool['closed'] is True
assert observation['old_failures_preserved'] is True and observation['scientific_credit'] is False
prepared = read(R / 'Root_runtime_preparation_observation.json')
assert prepared['prepare_tool'] == dict(initial_chunk='32f85f', session_id=26895, terminal_chunk='4d2d92', actual_exit_code=0, closed=True)
assert type(prepared['prepare_tool']['actual_exit_code']) is int
assert prepared['manifest_sha256'] == PINS[str(manifest_path)]['sha256']
assert prepared['source_sha256'] == PINS[str(source)]['sha256']
assert prepared['first_prepare_failed_before_mutation']['actual_exit_code'] == 1
pin(R / prepared['first_prepare_failed_before_mutation']['preserved_source'])

metadata_manifest_path = R / 'audit_metadata_manifest.json'
metadata_manifest = read(metadata_manifest_path, '90f6851e4fb4d40f795467ae06bb8669d8311d282b8c49253a9a1d805e582035')
metadata_observation_path = R / 'Root_actual_metadata_retirement_and_protected_restore.json'
metadata_observation = read(metadata_observation_path, '661dc862299e32e813ee2ce94883cf5417f7003e71769e03f538774f2d66b4b6')
peer_path = R / 'independent_metadata_actual_review/independent_actual_metadata_review.json'
peer = read(peer_path, '06f741aaa0ece315a7525654fd2c96edcc592bcdeb9a378a5784938b254da8b9')
peer_receipt_path = R / 'independent_metadata_actual_review/actual_readonly_tool_return.json'
peer_receipt = read(peer_receipt_path, '9f8ad5f50dd95b36d5cacc16778df14ceb311d76823d0a38b2fc78f390fda7c9')
assert peer['status'] == 'PASS' and peer['manifest_sha256'] == PINS[str(metadata_manifest_path)]['sha256']
assert peer['Root_actual_two_window_observation_sha256'] == PINS[str(metadata_observation_path)]['sha256']
assert peer_receipt['report_sha256'] == PINS[str(peer_path)]['sha256']
assert peer_receipt['actual_tool_result'] == dict(initial_chunk_id='91c96a', session_id=11342, terminal_chunk_id='fdc8eb', exit_code=0, closed=True)
assert type(peer_receipt['actual_tool_result']['exit_code']) is int
read(R / 'audit_metadata_retirement_result.json', peer['result_sha256'])
metadata_rows = metadata_manifest['records']
assert len(metadata_rows) == 10
held = str(ROOT / 'validation/storage_cleanup_20261008/preservation_baseline.json')
absent = metadata_observation['final_retired_metadata_paths']
assert len(absent) == len(set(absent)) == metadata_observation['final_retired_metadata_count'] == 9
assert set(absent) == {row['path'] for row in metadata_rows} - {held}
assert set(peer['final_absent_paths']) == set(absent) and peer['final_retired_count'] == 9
assert all(not os.path.lexists(path) for path in absent)
assert metadata_observation['held_original_path'] == peer['restored_historical_canonical_protected_path'] == held
assert metadata_observation['original_inode_and_ctime_restored'] is False
held_pin = pin(held, 'e311d296eff2b9c9b8fd3cb7fb28dc4976e26ebe4229d8198dc50e473254288b')
held_stat = Path(held).lstat()
held_identity = dict(size=held_stat.st_size, allocated=held_stat.st_blocks * 512,
                     dev=held_stat.st_dev, ino=held_stat.st_ino, nlink=held_stat.st_nlink,
                     mode=held_stat.st_mode, mtime_ns=held_stat.st_mtime_ns, ctime_ns=held_stat.st_ctime_ns)
assert held_identity == peer['restored_current_identity']
held_original = next(row for row in metadata_rows if row['path'] == held)
assert all(held_identity[key] == held_original[key] for key in ('size', 'mode', 'mtime_ns'))
assert metadata_observation['retire_tool']['actual_exit_code'] == 0 and type(metadata_observation['retire_tool']['actual_exit_code']) is int
assert metadata_observation['retire_tool']['closed'] is True and metadata_observation['retire_tool']['original_JSON_paths_retired_at_that_window'] == 10
assert metadata_observation['restore_tool']['actual_exit_code'] == 0 and type(metadata_observation['restore_tool']['actual_exit_code']) is int
assert metadata_observation['restore_tool']['closed'] is True and metadata_observation['restore_tool']['path'] == held
assert peer['all_unique_archives_compressed_fullSHA_AND_complete_decompressed_SHA_size_again_verified'] is True
unique_archives = {row['archive_path']: row for row in metadata_rows}
assert len(unique_archives) == len(peer['archives']) == 8
archive_fresh = []
for decoded_proof in peer['archives']:
    row = unique_archives[decoded_proof['path']]
    assert row['archive_sha256'] == decoded_proof['compressed_sha256']
    assert row['archive_size'] == decoded_proof['compressed_bytes']
    assert row['sha256'] == decoded_proof['decoded_sha256'] and row['size'] == decoded_proof['decoded_bytes']
    archive = pin(row['archive_path'], row['archive_sha256'])
    assert archive['size_bytes'] == row['archive_size']
    assert row['archive_allocated'] == decoded_proof['allocated_bytes']
    previous_pin = next(bound for bound in peer['all_fullread_pins'] if bound['path'] == row['archive_path'])
    assert archive['identity'] == [previous_pin['dev'], previous_pin['ino'], previous_pin['mode'],
                                   previous_pin['size'], previous_pin['mtime_ns'], previous_pin['ctime_ns'], previous_pin['nlink']]
    current_allocated = Path(row['archive_path']).stat().st_blocks * 512
    archive_fresh.append(dict(**archive, fresh_allocated_bytes=current_allocated,
                             earlier_allocated_bytes=decoded_proof['allocated_bytes'],
                             allocated_delta_bytes=current_allocated-decoded_proof['allocated_bytes'],
                             earlier_actual_full_decompression_evidence=decoded_proof))
for row in metadata_rows:
    assert row['archive_sha256'] == unique_archives[row['archive_path']]['archive_sha256']
    assert row['sha256'] == unique_archives[row['archive_path']]['sha256']
    assert row['size'] == unique_archives[row['archive_path']]['size']

expected_baseline = dict(sha256='216bf83c47ef942497c7eb1a569790a39954612a3df6b38e6b1f7e671475ff97', regular_files=174175, symlinks=687, directory_paths=6991)
assert manifest['untouched_before'] == result['unchanged_other_files'] == observation['other_files_fingerprint'] == expected_baseline
assert pre['expectedwholebaseline'] == expected_baseline
before = fingerprint(set(expected_paths))
assert before == expected_baseline
after = fingerprint(set(expected_paths))
assert after == before
assert all(not os.path.lexists(path) for path in expected_paths + absent)
for path, bound in PINS.items():
    assert identity(path) == bound['identity']

report = dict(
    schema='SPOT_R14_FIXED5_RUNTIME_ACTUAL_POST_READONLY_INDEPENDENT_REVIEW_V1', status='PASS',
    manifest_sha256=PINS[str(manifest_path)]['sha256'], source_sha256=PINS[str(source)]['sha256'],
    helper_sha256=PINS[str(helper)]['sha256'], plan_sha256=PINS[str(plan_path)]['sha256'],
    cleanup_result_sha256=PINS[str(result_path)]['sha256'], Root_actual_observation_sha256=PINS[str(observation_path)]['sha256'],
    genuine_Root_retirement_tool=tool, exact5_deleted_paths=expected_paths, all5_lexists_absent=True,
    logical_bytes_retired=sum(row['size_bytes'] for row in rows), allocated_bytes_retired=result['allocated_bytes'],
    V9_retained_primary_fullSHA_original_identity_fresh=master, expectedwholebaseline=expected_baseline,
    independent_fingerprint_before=before, independent_fingerprint_after=after,
    metadata_final9_absent_paths=absent, protected_R1_original_fullSHA_present=held_pin,
    protected_R1_current_identity_matches_actual_restoration_postcheck=held_identity,
    protected_R1_original_inode_or_ctime_restored=False,
    metadata_initial10_retirement_and_one_protected_restoration_real_windows_retained=True,
    unique8_archives_compressed_fullSHA_and_identity_fresh=archive_fresh,
    previous_actual_complete_decompression_PASS_fresh_SHA_bound=True,
    previous_metadata_actual_review_sha256=PINS[str(peer_path)]['sha256'],
    previous_metadata_actual_tool_receipt_sha256=PINS[str(peer_receipt_path)]['sha256'],
    fresh_gzip_decompression_performed_by_this_reader=False,
    archive_allocation_observation='First archive has current allocated3301376 versus earlier3313664 (-12288), with unchanged fullSHA/size/identity. Others match earlier allocation. No cause attributed; archive byte and original identity gates retained.',
    prior_actual_reader_failure=dict(initial_chunk_id='eac6f8', exit_code=1, closed=True,
                                     preserved_directory=str(O / 'attempt01_allocation_equality_assertion_failed'),
                                     correction='Treat archive allocated bytes as an actual observation; require unchanged fullSHA, exact size, and original complete identity.'),
    metadata_window_scope='Nine original review snapshots absent; one old-index protected baseline restored and retained. All eight exact compressed recovery payloads freshly SHA-bound to genuine earlier full-decompression PASS.',
    whole_untouched_scope='Sorted regular identities, symlink path/target and directory paths; .git, R14 and exact5 excluded. This fingerprint is metadata integrity, not a fresh hash of every project file.',
    old_failed_scientific_facts_promoted=False, new_scientific_or_native_RSS_credit=False,
    management_helper_or_business_module_imported=False, prepare_retire_restore_list_or_business_called=False,
    project_formal_or_ART_written=False, files_deleted_by_reviewer=0,
    full_read_pins=list(PINS.values()), audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
with (O / 'REPORT.json').open('x') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
print(json.dumps(dict(status='PASS', report=str(O / 'REPORT.json'),
                      report_sha256=hashlib.sha256((O / 'REPORT.json').read_bytes()).hexdigest(),
                      manifest_sha256=report['manifest_sha256'], cleanup_result_sha256=report['cleanup_result_sha256'],
                      expectedwholebaseline=expected_baseline)))
