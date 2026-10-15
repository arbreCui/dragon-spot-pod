import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat

R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = R / 'validation/artifacts'
D = B / 'actual_complete_combined_build_v21_sources'
E = B / 'actual_complete_combined_build_v21_receipts'
P = Path('/private/tmp/axmat_v21_complete_build_host_actual_SOURCE_binding_20261010_9l6eaiab')
PEER = Path('/private/tmp/axmat_v21_actual_bound_complete_build_HOST_independent_SOURCE_review_20261010_f5v2c')
DESIGN_PEER = Path('/private/tmp/axmat_v21_complete_build_generator_independent_SOURCE_review_20261010_y84cv')
PREP_E = B / 'actual_complete_combined_prepare_v21_receipts'
HOST = ART / 'axial-material-complete-combined-build-host-v21-20261010'
OUT = ART / 'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'

def identity(p):
    s = p.stat(follow_symlinks=False)
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(p):
    p = Path(p)
    before = identity(p)
    assert stat.S_ISREG(before[2]) and before[3] == 1 and not p.is_symlink(), str(p)
    h = hashlib.sha256()
    with p.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    assert identity(p) == before
    return dict(path=str(p), sha256=h.hexdigest(), size_bytes=before[4], identity=before)

def exact(q):
    current = pin(q['path'])
    assert current['sha256'] == q['sha256'] and current['identity'] == q['identity'], q['path']
    if 'size_bytes' in q:
        assert current['size_bytes'] == q['size_bytes']
    return current

def load(p, expected=None):
    q = pin(p)
    if expected:
        assert q['sha256'] == expected, str(p)
    return json.loads(Path(p).read_text()), q

def complete_package(root, manifest_name, expected_sha):
    m, mp = load(root / manifest_name, expected_sha)
    members = m['members']
    assert isinstance(members, dict) and len(members) == m['member_count']
    assert set(f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()) == set(members) | {manifest_name}
    assert not any(f.is_symlink() for f in root.rglob('*'))
    pins = {name: exact(q) for name, q in members.items()}
    pins[manifest_name] = mp
    return m, pins

def save_new(path, value):
    assert not os.path.lexists(path)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

def main():
    assert not os.path.lexists(D) and not os.path.lexists(E) and not os.path.lexists(HOST)
    author, source = complete_package(P, 'Root_complete_bound_SOURCE_manifest.json', '4005ae585a6c0a3bcd6f94f6ecc92a7dbca6fe75d23a562b9f54cc2a403bc088')
    peer, peer_source = complete_package(PEER, 'sealed_manifest.json', '95c35345385761c7acd654ca30c0584f959a140a98e5845a99d80456d3ec6f3b')
    design_peer, design_source = complete_package(DESIGN_PEER, 'sealed_manifest.json', 'b9b4c223ce31d23358105ee2754a6d5d218ed65db5d79265ca78f64ade489c8a')
    assert author['member_count'] == 19 and source['combined_build_host.py']['sha256'] == 'ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196'
    assert author['actual_Source_render_chunk_id'] == '9f0b06' and type(author['actual_Source_render_exit_code']) is int and author['actual_Source_render_exit_code'] == 0 and author['actual_Source_render_closed'] is True
    for sealed, count in [(peer, 148), (design_peer, 182)]:
        assert type(sealed['actual_review_typed_integer_exit_code']) is int and sealed['actual_review_typed_integer_exit_code'] == 0 and sealed['actual_review_closed'] is True
        assert sealed['review_checks'] == count and not sealed['blockers'] and sealed['full_EOF_SHA7ID_before_after_unchanged'] is True
    review, _ = load(PEER / 'REVIEW.json', '6f3b47380ec4670974ceac189e8e2a864f34b539bf6f2ba997c6055c6948f1d0')
    assert review['all_checks_typed_true'] is True and len(review['checks']) == 148
    assert all(type(c['value']) is bool and c['value'] is True for c in review['checks'])
    for q in review['all_bounded_Source_and_small_Root_META_pins_beforeafter'].values():
        exact(q)
    seal_path = PEER.parent / (PEER.name + '_seal_receipt') / 'actual_seal_tool_return.json'
    seal, seal_pin = load(seal_path)
    terminal = seal['terminal_tool_return']
    assert seal['closed'] is True and terminal['chunk_id'] == '27dd8f' and type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and 'session_id' not in terminal
    assert json.loads(terminal['output'])['manifest'] == peer_source['sealed_manifest.json']
    peer_source['actual_seal_tool_return.json'] = seal_pin
    summary, summary_pin = load(PREP_E / 'Root_actual_complete_combined_prepare_summary.json', '21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344')
    root_terminal, _ = load(summary['actual_root_terminal']['path'], summary['actual_root_terminal']['sha256'])
    assert root_terminal['closed'] is True and type(root_terminal['exit_code']) is int and root_terminal['exit_code'] == 0
    assert root_terminal['terminal_tool_return']['chunk_id'] == 'e0647a' and 'session_id' not in root_terminal['terminal_tool_return']
    prep_peer, _ = load(PREP_E / 'sealed_independent_actual_complete_PREP_saved_META_review/REVIEW.json', '553cf0dc4212fd72c27598010a85daef2e839e27ada6da8ca389fb32a045410c')
    assert prep_peer['all_checks_typed_true'] is True and not prep_peer['blockers'] and len(prep_peer['checks']) == 517
    namespaces, _ = load(summary['namespace_manifest']['path'], summary['namespace_manifest']['sha256'])
    all_prepared = {}
    for ns in namespaces['namespaces']:
        root = Path(ns['root'])
        actual_files = {f.relative_to(root).as_posix() for f in root.rglob('*') if f.is_file()}
        assert actual_files == set(ns['files']) and not any(f.is_symlink() for f in root.rglob('*'))
        for name, q in ns['files'].items():
            assert q['path'] == str(root / name)
            all_prepared[q['path']] = exact(q)
        for directory in ns['directories']:
            assert identity(root / directory['path']) == directory['identity']
    prep_host, _ = load(summary['actual_host_result']['path'], summary['actual_host_result']['sha256'])
    fixed = [exact(q) for q in prep_host['input_sources'] + [prep_host['original_helper'], prep_host['resource_factory']]]
    assert len(fixed) == 67
    canonical = pin(R / 'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')
    assert canonical['sha256'] == '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
    ast.parse((P / 'combined_build_host.py').read_text())
    for relative in ('execution_claim.json', 'seal.json', 'driver_result.json', 'closeout_failure.json', 'raw_metadata_receipt.json', 'audit/binary_identity.json', 'audit/result.json', 'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V21/stages.json', 'runtime/Dragon'):
        assert not os.path.lexists(OUT / relative), relative
    assert shutil.disk_usage(R).free - 2 * 2**30 >= 8 * 2**30
    E.mkdir(); D.mkdir()
    copied = {}
    for relative_root, pool in [('', source), ('sealed_independent_actual_bound_build_SOURCE_review', peer_source), ('sealed_independent_generator_design_SOURCE_review', design_source)]:
        for relative, q in pool.items():
            destination = D / relative_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(q['path'], destination)
            current = pin(destination)
            assert current['sha256'] == q['sha256'] and current['size_bytes'] == q['size_bytes']
            copied[destination.relative_to(D).as_posix()] = current
    assert pin(D / 'combined_build_host.py')['sha256'] == source['combined_build_host.py']['sha256']
    save_new(D / 'Root_actual_complete_build_SOURCE_install_record.json', dict(schema='ROOT_V21_COMPLETE_ACTUAL_BUILD_SOURCE_INSTALL_V1', status='SOURCE_READY_REAL_ROOT_COMPLETE_BUILD_REQUIRED', original_author_source_pins=source, original_bound_peer_source_pins=peer_source, original_generator_design_peer_source_pins=design_source, complete_copied_source_pins=copied, genuine_PREP_summary=summary_pin, all_prepared_saved_namespace_files=all_prepared, all67_actual_PREP_fixed_inputs_unchanged=fixed, actual_canonical_source=canonical, all_original_source_packages_unchanged=True, no_business_build_or_numeric_executed=True, no_SOURCE_append_after_freeze=True, whole_build_qualified=False, whole_INPUT_admitted=False, native_RSS_qualified=False, AAA_accuracy_qualified=False, ABA_admitted=False))
    frozen = {f.relative_to(D).as_posix(): pin(f) for f in sorted(D.rglob('*')) if f.is_file()}
    directories = {'.': identity(D)}
    directories.update({f.relative_to(D).as_posix(): identity(f) for f in sorted(D.rglob('*')) if f.is_dir()})
    assert len(frozen) == 30
    for pool in [source, peer_source, design_source]:
        for q in pool.values(): exact(q)
    for q in all_prepared.values(): exact(q)
    for q in fixed: exact(q)
    save_new(E / 'Root_prelaunch_complete_build_source_freeze.json', dict(schema='ROOT_V21_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1', source_root=str(D), complete_files=frozen, complete_directories=directories, symlinks={}, no_SOURCE_append_after_freeze=True, actual_complete_SOURCE_file_count=len(frozen)))
    print(json.dumps(dict(status='COMPLETE_SOURCE_INSTALLED_FROZEN_NO_BUILD_YET', full_Source_files=len(frozen), complete_Source_directories=len(directories), all67_PREP_fixed_inputs_unchanged=True, all_prepared_namespaces_unchanged=True, host=pin(D / 'combined_build_host.py'), frozen=pin(E / 'Root_prelaunch_complete_build_source_freeze.json'), free_bytes=shutil.disk_usage(R).free, business_or_numeric_executed=False), ensure_ascii=False))

if __name__ == '__main__':
    main()
