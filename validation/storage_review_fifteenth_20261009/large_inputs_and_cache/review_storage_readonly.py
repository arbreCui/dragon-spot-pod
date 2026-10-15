import hashlib
import json
import os
import stat
from pathlib import Path

ROOT = Path('/Users/wen/spot')
O = Path('/private/tmp/spot_storage_fifteenth_large_holds_readonly_independent_review_20261009')
PINS = {}


def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]


def pin(p, expected=None):
    p = Path(p)
    before = identity(p)
    assert stat.S_ISREG(before[2]) and p.resolve() == p
    h = hashlib.sha256()
    with p.open('rb') as stream:
        while chunk := stream.read(1024 ** 2):
            h.update(chunk)
    assert identity(p) == before
    result = dict(path=str(p), sha256=h.hexdigest(), size_bytes=before[3], identity=before)
    if expected is not None:
        assert result['sha256'] == expected
    PINS[str(p)] = result
    return result


def read(p, expected=None):
    bound = pin(p, expected)
    result = json.loads(Path(p).read_text())
    assert identity(p) == bound['identity']
    return result


def metadata(p):
    p = Path(p)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
    return dict(path=str(p), logical_bytes=s.st_size, allocated_bytes=s.st_blocks * 512,
                identity=identity(p))


inventory_path = Path('/private/tmp/spot_fifteenth_storage_metadata_inventory_20261009.json')
inventory = read(inventory_path)
graph_path = ROOT / 'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
graph = read(graph_path, '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
assert len(graph['canonical_files']) == 35647 and len(graph['namespaces']) == 86 and len(graph['aliases']) == 186
canon = {row['path']: row for row in graph['canonical_files']}
ns_files = {str(Path(row['canonical_root']) / name) for row in graph['namespaces'] for name in row['files']}
roots = set(graph['live_resource_roots'])
assert len(roots) == 231
old_path = ROOT / 'validation/storage_review_more_20261008/current_protection_index.json'
old = read(old_path)
normalized_path = ROOT / 'validation/storage_review_more_20261008/normalized_protection_index.json'
normalized = read(normalized_path)
assert set(normalized['protected_files']) == set(old['canonical_protected_files'])
cold_path = ROOT / 'validation/storage_cleanup_eighth_20261009/cold_dynamic/current_cold_dynamic_protected_files.json'
cold = read(cold_path)
r9_manifest_path = ROOT / 'validation/storage_cleanup_ninth_20261009/manifest.json'
r9_manifest = read(r9_manifest_path)
cold_paths = set(r9_manifest['current_cold_extra_protected_files'])
assert len(cold_paths) == 6248
cold_paths |= {row['path'] for row in cold['current_cold_dynamic_protected_files']}
uncleared_material = set(cold['remaining_11_material_candidate_paths'])
restore_primaries = {row['path'] for row in r9_manifest['retained_primaries']}

cache_boundary_path = ROOT / 'validation/storage_cleanup_twelfth_20261009/current_protection_review/cache_64_current_canonical_source_boundary.json'
boundary = read(cache_boundary_path, '38e419a8c62e2790cccf67fbf04a64bc46d9d6e1b1b9a2e30e5a79353c381d23')
cache_base_path = Path('/private/tmp/spot_storage_twelfth_current_v9_graph_protection_boundary_20261009/cache_223_current_closure_intersection.json')
base = read(cache_base_path, '8189a99f7a5bb111a883d3953470f40618c3874100938ec4b73d551a206312c8')
held_cache = {row['path'] for row in base['resource_root_hits']} | {row['path'] for row in boundary['extra_current_canonical_source_cache_HOLD']}
assert len(base['resource_root_hits']) == 157 and len(boundary['extra_current_canonical_source_cache_HOLD']) == 2 and len(held_cache) == 159
current_cache = {str(ROOT / row['path']) for row in inventory['cache_like']}
assert len(current_cache) == inventory['cache_like_count'] == 159 and current_cache == held_cache
cache_metas = [metadata(path) for path in sorted(current_cache)]
cache_logical = sum(row['logical_bytes'] for row in cache_metas)
cache_allocated = sum({tuple(row['identity'][:2]): row['allocated_bytes'] for row in cache_metas}.values())
assert cache_logical == 4254785 and cache_allocated == 4534272
path_set_sha = hashlib.sha256(('\n'.join(sorted(current_cache)) + '\n').encode()).hexdigest()
assert path_set_sha == hashlib.sha256(('\n'.join(sorted(held_cache)) + '\n').encode()).hexdigest()

report_refs = []
round_dirs = ['storage_cleanup_20261008', 'storage_cleanup_more_20261008',
    'storage_cleanup_third_20261008', 'storage_cleanup_fourth_20261008',
    'storage_cleanup_fifth_20261008', 'storage_cleanup_sixth_20261009',
    'storage_cleanup_seventh_20261009', 'storage_cleanup_eighth_20261009',
    'storage_cleanup_ninth_20261009', 'storage_cleanup_tenth_20261009',
    'storage_cleanup_eleventh_20261009', 'storage_cleanup_twelfth_20261009',
    'storage_cleanup_thirteenth_20261009', 'storage_cleanup_fourteenth_20261009']
for dirname in round_dirs:
    p = ROOT / 'validation' / dirname / 'REPORT.txt'
    if p.is_file():
        report_refs.append(pin(p))
pin(ROOT / 'validation/storage_cleanup_fourteenth_20261009/compiled_and_native_retention_review/REPORT.txt')
test_path = ROOT / 'validation/iterative/test_d4a_picard_map_preflight.py'
probe_path = ROOT / 'validation/axial_material/probe_refined_AAA_white_odd_response.py'
pin(test_path)
pin(probe_path)
assert 'REPAIRED = ROOT / "validation/artifacts/d4a-scattering-bootstrap-run-20260924/Dragon"' in test_path.read_text()
assert "'build/libDragon.a','build/libTrivac.a','build/libUtilib.a','build/libGanlib.a'" in probe_path.read_text()

big_rows = []
for allocated_at_inventory, size_at_inventory, relative in inventory['large_files']:
    p = ROOT / relative
    fresh = metadata(p)
    assert fresh['logical_bytes'] == size_at_inventory
    absolute = str(p)
    fresh.update(current_canonical=absolute in canon, current_exhaustive_namespace_member=absolute in ns_files,
                 old_protection_index_member=absolute in old['canonical_protected_files'],
                 cold_dynamic_member=absolute in cold_paths, previous_restore_primary=absolute in restore_primaries)
    # expected seal SHA is provenance only; no content reread of main scientific arrays.
    fresh['expected_canonical_sha256_not_fresh_payload_hash'] = canon.get(absolute, {}).get('sha256')
    if any(fresh[k] for k in ('current_canonical', 'current_exhaustive_namespace_member', 'cold_dynamic_member', 'previous_restore_primary')):
        fresh['reason'] = 'HOLD: current full-byte/namespace/cold or previous restoration dependency.'
    elif absolute in uncleared_material:
        fresh['reason'] = 'HOLD: remaining material copy has no complete dynamic reader exclusion; previous HOLD unchanged.'
    elif '/packed_material_intermediates/' in absolute:
        fresh['reason'] = 'HOLD: sole lossless payload for previously retired raw intermediate and restoration chain.'
    elif fresh['old_protection_index_member']:
        fresh['reason'] = 'HOLD in this review: historical owner reference needs complete current readchain and restoration proof before retirement.'
    else:
        fresh['reason'] = 'HOLD in this review: scientific main result or archive; no new complete consumer exclusion plus exact restoration proof. Same name/size/date is insufficient.'
    big_rows.append(fresh)

root_observations = []
for relative, observed in inventory['large_roots'][:20]:
    path = str(ROOT / relative)
    owned = [row for row in graph['canonical_files'] if row['path'].startswith(path + '/')]
    root_observations.append(dict(path=path, observed_regular_count=observed[0],
        observed_logical_bytes=observed[1], observed_allocated_path_bytes=observed[2],
        current_canonical_members=len(owned), current_canonical_logical_bytes=sum(row['size_bytes'] for row in owned),
        declared_resource_root=path in roots, note='Root fresh metadata observation; not exclusive APFS free space or a new full payload SHA scan.'))

protected_r1 = ROOT / 'validation/storage_cleanup_20261008/preservation_baseline.json'
assert str(protected_r1) in old['canonical_protected_files']
pin(protected_r1, 'e311d296eff2b9c9b8fd3cb7fb28dc4976e26ebe4229d8198dc50e473254288b')
bootstrap = metadata(ROOT / 'validation/artifacts/d4a-scattering-bootstrap-run-20260924/Dragon')
bootstrap['reason'] = 'HOLD: test_d4a_picard_map_preflight.py:18/166/176/177 directly hashes and copies this original path.'
signed = metadata(ROOT / 'validation/artifacts/native-signed-axial-state-20260929/build/libDragon.a')
signed['reason'] = 'HOLD: probe_refined_AAA_white_odd_response.py:22/81-82 fixed old signed package; current full INPUT also owns this library.'
retired = []
for version in range(2, 9):
    date = '20261008' if version <= 6 else '20261009' if version == 8 else '20261008'
    p = ROOT / f'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{version}-{date}/runtime/Dragon'
    if version == 7:
        # The V7 family actually used Oct09; derive known retired path from R13 manifest instead of guessing.
        continue
    retired.append(dict(path=str(p), lexists=os.path.lexists(p)))
assert all(not row['lexists'] for row in retired)

for path, bound in PINS.items():
    assert identity(path) == bound['identity']
assert all(identity(row['path']) == row['identity'] for row in big_rows + cache_metas + [bootstrap, signed])
report = dict(
    schema='SPOT_FIFTEENTH_LARGE_STORAGE_AND_UNCHANGED_HELD_CACHE_READONLY_INDEPENDENT_REVIEW_V1',
    status='PASS', conclusion='本次审查范围内新增安全删除候选0；当前大项或恢复义务保持，未因最新INPUT通过释放历史引用。',
    approved_deletion_candidates=[], approved_logical_bytes=0, approved_allocated_bytes=0,
    fresh_inventory_pin=PINS[str(inventory_path)], current_graph_metadata_whole_SHA_pin=PINS[str(graph_path)],
    current_graph_scope=dict(canonical_files=35647, namespaces=86, aliases=186, declared_resource_roots=231),
    cache_set_check=dict(current_count=159, original_resource_HOLD_count=157, original_source_derivative_HOLD_count=2,
                         exact_R12_retained_set_equal=True, sorted_absolute_path_set_sha256=path_set_sha,
                         current_logical_bytes=cache_logical, current_unique_inode_allocated_bytes=cache_allocated,
                         new_paths=0, missing_held_paths=0, ordinary_dependency_clear_new_cache_candidates=0,
                         original_boundary_report=PINS[str(cache_boundary_path)], original_intersection_report=PINS[str(cache_base_path)],
                         observation='Path-set and fresh lstat only; cache contents were not rehashed. No copied159-path list.'),
    major_protected_categories=[
        dict(category='Two complete current A/B historical inputs', paths=[str(ROOT / 'validation/artifacts/axial-material-production-qualified-AB-source-factor-20261006'), str(ROOT / 'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005')], consumer='Current complete graph; pending bound cold factory producer_environment/declare original12-map parent and fulloffline receipt/material/layout contract.'),
        dict(category='Native full primary response arrays', paths=[str(ROOT / 'validation/artifacts/native-layered-full-20261001/primary'), str(ROOT / 'validation/artifacts/native-oblique-full-response-20260930/analysis')], consumer='Original full-range result.sha256 and replay/reference receipts require primitive/cell/face/trajectory raw main data. R14 compiled retention review; no exact replacement or full reader exclusion established.'),
        dict(category='Permanent restoration payloads', paths=[str(ROOT / 'validation/storage_cleanup_ninth_20261009/packed_material_intermediates'), str(ROOT / 'validation/storage_cleanup_fourteenth_20261009/metadata_archives'), str(ROOT / 'validation/artifacts/d4a-actual-temperature-library-run-20261003/merge/28-U238/tape30')], consumer='R9 89gzip restores originalraw then priorR2 work copies; R14 eightgzip reconstruct retiredmetadata; U238 originalmerge is retained restore master. Cannot discard the only lossless recovery source.'),
        dict(category='Protected historical baseline', paths=[str(protected_r1)], consumer='Old current_protection_index canonical owner; R14 restored original e311 bytes and retained this exact path.'),
        dict(category='Current typed specification and cold environment', paths=[str(ROOT / 'validation/axial_material/combined_runtime_reached_typed_inputs_measurement_evidence_20261007/typed_input_specs.json'), str(ROOT / 'validation/artifacts/axial-material-cold-cp314-scipy-dependency-20261008')], consumer='Complete graph/consumer phase owns entire typed requirements and SciPy manifest/package/wheel, not cache.'),
    ],
    direct_compiled_consumers=[bootstrap, signed],
    Root_fresh_largest20_directory_observations=root_observations,
    top50_actual_large_files_metadata_and_protection_intersections=big_rows,
    reviewed_R1_to_R14_reports=report_refs,
    original_reports_logs_seals_failed_facts_source_and_restore_rules_keep=True,
    future_cold_prep_or_native_declared_or_scientifically_qualified=False,
    no_candidate_pair_full_SHA_scan_needed_because_none_recommended=True,
    current_scientific_large_payloads_content_rehashed=False, full35GB_phase_or_business_reexecuted=False,
    allproject_full_walk_or_new_baseline_copy_created=False,
    project_formal_ART_written=False, files_deleted=0,
    native_RSS_or_AAA_or_ABA_credit=False, full_read_pins=list(PINS.values()),
    limits=['Uses Root fresh small inventory plus current pinned graph and earlier frozen dependency reviews.',
            'Top50 large-file identities and held159 cache paths freshly checked; does not claim all project scientific bytes rehashed.',
            'Outside graph/resource membership is not deletion permission. Full current consumers, historical owner and exact restoration proof still required.',
            'Allocated path bytes are observations, not exclusive APFS space; cache allocation deduplicated by inode.'])
with (O / 'REPORT.json').open('x') as stream:
    json.dump(report, stream, indent=2)
    stream.write('\n')
text = ('本轮只读复查：新增可安全删除候选0。\n'
        '159份缓存与R12保留集合完全相同：157资源目录内缓存+2当前源码衍生缓存；没有新增普通无依赖缓存。逻辑4,254,785B、去重分配4,534,272B。\n'
        '最大项仍为两套完整历史输入、native分层/斜向原始主数据、89材料gzip恢复档和主核数据；原结果与恢复依赖保留。\n'
        '旧bootstrap程序被测试直接读取，signed库被probe及当前图使用。R1保护快照已恢复原字节，继续保留；V2–V8已退役副本不重复计入候选。\n'
        '只鲜核小元数据/保护证据与50大文件身份，没有重读35GB科学输入、业务调用、删除或正式写入。\n')
with (O / 'REPORT.txt').open('x') as stream:
    stream.write(text)
print(json.dumps(dict(status='PASS', report=str(O / 'REPORT.json'), report_sha256=hashlib.sha256((O / 'REPORT.json').read_bytes()).hexdigest(),
                      safe_new_candidates=0, exact159_R12_cache_set_equal=True, cached_paths_set_sha256=path_set_sha,
                      current_cache_logical_bytes=cache_logical, current_cache_unique_allocated_bytes=cache_allocated)))
