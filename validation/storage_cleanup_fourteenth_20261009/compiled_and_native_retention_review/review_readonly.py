"""Bounded metadata/old source review; TMP output only, no target import/call."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib
import json
import os
import stat

ROOT = Path('/Users/wen/spot')
OUT = Path('/private/tmp/spot_storage_fourteenth_binary_native_readonly_review_20261009')
KEYS = ('dev', 'ino', 'mode', 'size', 'mtime_ns', 'ctime_ns', 'nlink')
PINS = []


def read(path, as_json=True):
    before = [getattr(path.lstat(), 'st_' + key) for key in KEYS]
    raw = path.read_bytes()
    assert before == [getattr(path.lstat(), 'st_' + key) for key in KEYS]
    PINS.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'size': len(raw), 'identity': before})
    return json.loads(raw) if as_json else raw.decode()


def unique(rows):
    return {(row['dev'], row['ino']): row for row in rows}


def amount(rows):
    return sum(row['allocated'] for row in unique(rows).values())


def under(path, roots):
    return any(path == root or path.startswith(root + '/') for root in roots)


def main():
    assert not (OUT / 'REPORT.txt').exists()
    rows = read(Path('/private/tmp/spot_storage_recheck_20261009/current_regular_file_metadata.json'))
    metadata = {row['path']: row for row in rows}
    graph = read(ROOT / 'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json')
    assert PINS[-1]['sha256'] == '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
    canonical = {row['path'] for row in graph['canonical_files']}
    namespaces = {row[key] for row in graph['namespaces'] for key in ('root', 'canonical_root')}
    aliases = {row[key] for row in graph['aliases'] for key in ('path', 'target')}
    diraliases = {row[key] for row in graph['aliases'] if row['kind'] == 'directory' for key in ('path', 'target')}
    roots = set(graph['live_resource_roots'])
    def markers(path):
        return {'canonical': path in canonical, 'namespace': under(path, namespaces), 'alias': path in aliases or under(path, diraliases), 'history_resource_member': under(path, roots)}
    def current(row):
        info = Path(row['path']).lstat()
        assert stat.S_ISREG(info.st_mode) and [getattr(info, 'st_' + key) for key in KEYS] == [row[key] for key in KEYS]
    for number in ('eighth', 'ninth', 'tenth', 'eleventh', 'twelfth', 'thirteenth'):
        read(ROOT / ('validation/storage_cleanup_' + number + '_20261009/REPORT.txt'), False)
    sixth = read(ROOT / 'validation/storage_cleanup_sixth_20261009/duplicate_library_source_review.json')
    old51 = read(Path('/private/tmp/spot_storage_twelfth_old_bootstrap_native_readonly_review_20261009/fresh_compiled_51_candidate_and_peer_SHA_records.json'))
    source = read(ROOT / 'validation/iterative/test_d4a_picard_map_preflight.py', False)
    assert 'd4a-scattering-bootstrap-run-20260924/Dragon' in source
    for path in ('validation/iterative/native_layered_full_result.md', 'validation/iterative/native_oblique_full_response_result.md', 'validation/axial_material/probe_refined_AAA_white_odd_response.py'):
        read(ROOT / path, False)
    compiled = [row for row in rows if Path(row['path']).suffix in ('.o', '.a', '.mod', '.so', '.dylib') or Path(row['path']).name in ('Dragon', 'dragon', 'Trivac', 'Ganlib')]
    for row in compiled:
        current(row)
    classes = {}
    for label in sorted({Path(row['path']).suffix or Path(row['path']).name for row in compiled}):
        selected = [row for row in compiled if (Path(row['path']).suffix or Path(row['path']).name) == label]
        classes[label] = {'paths': len(selected), 'unique_inodes': len(unique(selected)), 'unique_inode_allocated_bytes': amount(selected)}
    groups = defaultdict(list)
    for row in rows:
        if row['path'].startswith(str(ROOT / 'validation/artifacts') + '/'):
            groups[Path(row['path']).relative_to(ROOT / 'validation/artifacts').parts[0]].append(row)
    native = [{'path': str(ROOT / 'validation/artifacts' / family), 'regular_paths': len(files), 'unique_inode_allocated_bytes': amount(files), 'build_only_allocated_bytes': amount([row for row in files if '/build/' in row['path']]), 'decision': 'HOLD_UNIQUE_PRIMARY_DATA_AND_ORIGINAL_VERIFICATION_REPLAY_CONTRACT'} for family, files in sorted(groups.items(), key=lambda item: amount(item[1]), reverse=True) if family.startswith('native-')]
    primary = []
    for relative in ('native-layered-full-20261001/primary', 'native-oblique-full-response-20260930/analysis', 'axial-material-production-qualified-AB-source-factor-20261006', 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'):
        path = ROOT / 'validation/artifacts' / relative
        selected = [row for row in rows if row['path'].startswith(str(path) + '/')]
        primary.append({'path': str(path), 'regular_paths': len(selected), 'unique_inode_allocated_bytes': amount(selected), 'decision': 'HOLD_FULL_INPUT_OR_PRIMARY_NUMERICAL_WITNESS'})
    preserved51 = []
    for item in old51:
        row = metadata[item['candidate']['path']]
        current(row)
        assert [row[key] for key in KEYS] == item['candidate']['identity']
        preserved51.append({'path': row['path'], 'size': row['size'], 'allocated': row['allocated'], 'prior_full_SHA': item['candidate']['sha256'], 'current_metadata_matches_prior_full_SHA_identity': True, 'current_markers': markers(row['path']), 'original_manifest_edges': item['original_manifest_edges'], 'decision': 'HOLD_PRIOR_SEAL_NO_NEW_DEPENDENCY_AND_RESTORE_ADMISSION'})
    signed = []
    for item in sixth['explicitly_preserved_signed_host_libraries']:
        row = metadata[item['path']]
        current(row)
        assert [row[key] for key in KEYS] == item['identity']
        signed.append({'path': row['path'], 'size': row['size'], 'allocated': row['allocated'], 'prior_full_SHA': item['sha256'], 'decision': 'HOLD_DIRECT_SOURCE_LIBRARY_VERIFICATION_AND_LINK_INPUT'})
    archives = [row for row in rows if row['path'].endswith(('.gz', '.whl', '.zip', '.tar', '.tgz', '.xz', '.bz2', '.7z'))]
    other_archives = [row for row in archives if '/packed_material_intermediates/' not in row['path']]
    r13 = read(ROOT / 'validation/storage_cleanup_thirteenth_20261009/manifest.json')
    assert all(not os.path.lexists(row['path']) for row in r13['candidates'])
    five = [row for row in compiled if any(('live-resource-scopes-v' + str(version) + '-20261008/runtime/Dragon') in row['path'] for version in range(2, 7))]
    assert len(five) == 5
    result = {'schema': 'SPOT_R14_BINARY_NATIVE_LIGHT_READONLY_REVIEW_V1', 'status': 'PASS_READONLY_HOLD_NO_DELETE_AUTHORITY', 'Root_inventory_actual_tool': {'initial_chunk_id': 'd13960', 'session_id': 51871, 'terminal_chunk_id': '593b95', 'exit_code': 0, 'closed': True}, 'Root_metadata_regular_rows_derived': len(rows), 'Root_unique_inodes_derived': len(unique(rows)), 'Root_unique_inode_allocated_bytes': amount(rows), 'compiled_filter': '.o/.a/.mod/.so/.dylib or exact basename Dragon/dragon/Trivac/Ganlib; no pycache; distinct scope from old4115', 'compiled_rows_derived': len(compiled), 'compiled_unique_inodes_derived': len(unique(compiled)), 'compiled_unique_inode_allocated_bytes': amount(compiled), 'compiled_class_breakdown': classes, 'all_selected_compiled_fresh_seven_fields_match_Root_metadata': True, 'nonexclusive_protection_counts': {key: sum(markers(row['path'])[key] for row in compiled) for key in ('canonical', 'namespace', 'alias', 'history_resource_member')}, 'largest_compiled_explicit_paths': [dict(row, protection=markers(row['path'])) for row in sorted(compiled, key=lambda row: row['size'], reverse=True)[:45]], 'largest_object_explicit_paths': sorted([row for row in compiled if Path(row['path']).suffix == '.o'], key=lambda row: row['size'], reverse=True)[:8], 'native_family_sizes': native, 'protected_primary_exact_directory_sizes': primary, 'old51_fresh_metadata_and_original_manifest_edges': preserved51, 'old51_fresh_full_SHA_not_repeated': True, 'signed_libraries': signed, 'signed_direct_dependency': sixth['explicit_signed_source_dependency'], 'bootstrap_direct_test_dependency': {'source': str(ROOT / 'validation/iterative/test_d4a_picard_map_preflight.py'), 'line': 18, 'path': str(ROOT / 'validation/artifacts/d4a-scattering-bootstrap-run-20260924/Dragon'), 'size': metadata[str(ROOT / 'validation/artifacts/d4a-scattering-bootstrap-run-20260924/Dragon')]['size'], 'required_SHA': '873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef'}, 'archives_count_derived': len(archives), 'permanent_R9_material_restore_archive_count_derived': len(archives) - len(other_archives), 'other_archive_rows': other_archives, 'R13_retired2_confirmed_absent': [row['path'] for row in r13['candidates']], 'V2_V6_exact5_other_agent_scope': {'paths': [row['path'] for row in five], 'logical_bytes': sum(row['size'] for row in five), 'allocated_bytes': amount(five), 'delete_or_same_SHA_not_approved_or_claimed_here': True}, 'this_audit_new_fixed_binary_deletion_candidates_approved': [], 'this_audit_new_approved_recovery_bytes': 0, 'current_graph_pin': next(pin for pin in PINS if pin['path'].endswith('/input_graph.json')), 'pins': PINS, 'Root_pure_metadata_compression_review_not_duplicated': True, 'Git_history_or_sensitive_files_scanned': False, 'project_formal_ART_or_Git_written': False, 'business_import_API_constructor_PREP_RUN_build_restore_native_or_cold_binding_executed': False, 'full35GB_science_hash_performed': False, 'files_deleted': 0, 'scientific_credit': False}
    with (OUT / 'binary_native_inventory_and_HOLD_evidence.json').open('x') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    lines = ['旧binary/native轻量只读审查：本人新增可直接删固定项0。V2–V6五条程序由另一代理完整审查；不在这里预批准或重复hash，R13已删两条不重复计算。', '', f'复用Root真d13960/51871→593b95 EXIT0 inventory，不再walk。筛选{len(compiled)}路径/{len(unique(compiled))}独有inode，unique allocated {amount(compiled)}B（{amount(compiled)/2**30:.6f}GiB）。筛选条件与旧4115完整native binary不同。', f'.o {classes[".o"]["paths"]}路径、{classes[".o"]["unique_inode_allocated_bytes"]}B（{classes[".o"]["unique_inode_allocated_bytes"]/2**20:.3f}MiB）；.a {classes[".a"]["paths"]}路径、{classes[".a"]["unique_inode_allocated_bytes"]}B（{classes[".a"]["unique_inode_allocated_bytes"]/2**20:.3f}MiB）。最大.o仅1,063,872B，最大.a24,626,264B。其余完整依赖/restore排除未成立，不能按后缀或旧日期清空。', '', '主要大占用是主输入/数值见证，HOLD：']
    lines += [row['path'] + '：' + str(row['unique_inode_allocated_bytes']) + ' allocated B（' + f'{row["unique_inode_allocated_bytes"]/2**30:.6f}GiB' + '）。' for row in primary]
    lines += [row['path'] + '全目录 ' + str(row['unique_inode_allocated_bytes']) + 'B，build仅 ' + str(row['build_only_allocated_bytes']) + 'B。' for row in native[:2]]
    lines += ['layered primary覆盖全部原轨迹与独立原坐标/witness；oblique analysis保存完整响应和primitive/cell/face见证，原result文档规定全范围审计/回放。不是可再生编译缓存。既有retired replay副本按R9恢复限制处理，不称所有旧全seal现在自动可重验。', '', '明确直接读取，HOLD：' + result['bootstrap_direct_test_dependency']['path'] + '，9,154,744B；test_d4a_picard_map_preflight.py:18和REPAIRED_SHA直接依赖。']
    lines += [row['path'] + '：' + str(row['size']) + 'B；原probe_refined_AAA_white_odd_response.py prepare校核四签名库并链接，HOLD。' for row in signed]
    lines += ['R12的51个old native/bootstrap同SHA筛选现identity保持，47个有原seal；同SHA并不解除测试/源码/恢复义务，完整路径见JSON。', '', f'压缩包实际{len(archives)}个：89份永久材料恢复gzip，另一个cp314 SciPy wheel。没有新普通下载压缩包批次；wheel与installed环境仍被cold manifest固定。U238 merge/28-U238/tape30 839,016,696B是R7明确恢复主本，继续HOLD，不压缩改原路径。', 'V2–V6五条各9,225,720B，共' + str(sum(row['size'] for row in five)) + ' logical/' + str(amount(five)) + ' allocated B；由graph代理另审新精确退役证明。R13旧V7/V8已缺席。', '', '保留最小结果文档：历轮REPORT/manifest/ledger/真实tool/独审/restore入口；native plan/frozen/prepared/execution inputs、result.sha256、source/compiler lineage、runs完整logs/watchdog、receipts、verification/results、resumption/retry。V7/V8真实失败及V9成功/INPUT/cold UNREADY源/inverse/独审亦保留。结果摘要不能替代仍依赖的primary/analysis原始数组。', 'Root另审旧puremetadata无损压缩与精确恢复，本人不重复；这不授权删除native主数据、源码、环境、alias/canonical/namespace/既有完整history目录或恢复主本。', '', '仅TMP报告，0项目写/删除/压缩/恢复，无cold绑定/业务import/API/constructor/PREP/RUN/native/build/测试，不读Git历史或敏感文件，不重hash35GB科学INPUT，无RSS或科学信用。allocated按inode去重，不等同APFS即时独占空闲。']
    (OUT / 'REPORT.txt').write_text('\n'.join(lines) + '\n')
    print(json.dumps({'status': result['status'], 'output': str(OUT), 'compiled': len(compiled), 'allocated': amount(compiled), 'objects': classes['.o'], 'archives': classes['.a'], 'report_sha256': hashlib.sha256((OUT / 'REPORT.txt').read_bytes()).hexdigest(), 'evidence_sha256': hashlib.sha256((OUT / 'binary_native_inventory_and_HOLD_evidence.json').read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
