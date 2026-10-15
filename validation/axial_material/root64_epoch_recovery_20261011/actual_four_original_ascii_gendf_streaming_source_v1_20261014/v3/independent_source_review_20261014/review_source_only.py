"""Independent fullEOF metadata and static Source review; never decode gzip."""
import ast
import hashlib
import json
import os
import stat
from pathlib import Path

BASE = Path(__file__).absolute().parents[1]
REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ROOT = Path('/Users/wen/spot')
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
            fresh_bytes=2147483648, history_bytes=103079215104,
            cold_reserve_bytes=20971764748, metadata_reserve_bytes=67108864,
            free_floor_bytes=8589934592, threads=1, children_at_once=1, retries=0)
FLAGS = dict(business_executed=False, numerical_executed=False, compiler_executed=False,
             files_deleted=False, physics_qualified=False, scientific_accuracy_qualified=False,
             complete_reaction_authority_qualified=False, physical_neutron_balance_qualified=False,
             AAA_qualified=False, ABA_admitted=False, goal_complete=False)
PIN_KEYS = {'path', 'sha256', 'size_bytes', 'identity'}


def require(ok, message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(p):
    require(type(p) is dict and set(p) == PIN_KEYS and type(p['path']) is str
            and type(p['sha256']) is str and len(p['sha256']) == 64
            and all(c in '0123456789abcdef' for c in p['sha256'])
            and type(p['size_bytes']) is int and p['size_bytes'] >= 0
            and type(p['identity']) is list and len(p['identity']) == 7
            and all(type(i) is int for i in p['identity'])
            and p['identity'][4] == p['size_bytes'], 'complete strict PF type')
    q = Path(p['path'])
    s = q.lstat()
    require(q.is_absolute() and not any(x.is_symlink() for x in (q, *q.parents))
            and stat.S_ISREG(s.st_mode) and s.st_nlink == 1
            and identity(s) == p['identity'], 'exact literal single-link current7: ' + str(q))
    return s


def pin(q):
    q = Path(q)
    s = q.lstat()
    require(q.is_absolute() and not any(x.is_symlink() for x in (q, *q.parents))
            and stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'literal ordinary file')
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno())) == identity(s), 'opened current7')
        sha = hashlib.file_digest(f, 'sha256').hexdigest()
        require(identity(os.fstat(f.fileno())) == identity(s), 'EOF current7')
    p = dict(path=str(q), sha256=sha, size_bytes=s.st_size, identity=identity(s))
    current(p)
    return p


def full(p):
    current(p)
    require(pin(p['path']) == p, 'same wholeEOF SHA/current7: ' + p['path'])
    return p


def read(p):
    full(p)
    require(p['size_bytes'] < 8 * 2**20, 'bounded metadata')
    raw = Path(p['path']).read_bytes()
    require(len(raw) == p['size_bytes'] and hashlib.sha256(raw).hexdigest() == p['sha256'], 'whole read exact')
    current(p)
    return json.loads(raw)


def new(q, value):
    with Path(q).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def class_text(q, name):
    text = Path(q).read_text()
    return next(ast.get_source_segment(text, n) for n in ast.parse(text).body
                if isinstance(n, ast.ClassDef) and n.name == name)


def main():
    p_ready = pin(BASE / 'SOURCE_REVIEW_READY.json')
    p_generation = pin(BASE / 'ACTUAL_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json')
    ready = read(p_ready)
    generation = read(p_generation)
    require(ready['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_SOURCE_REVIEW_READY_V1'
            and ready['source_only'] is True and ready['actual_business_started'] is False
            and ready['Root_final_publication_executed'] is False
            and all(ready[k] is False for k in FLAGS), 'same Source-only ready and false flags')
    gt = generation['actual_Source_preparation_return']
    require(generation['observed_closed'] is True
            and type(generation['original_integer_exit_code']) is int
            and generation['original_integer_exit_code'] == 0
            and type(gt['exit_code']) is int and gt['exit_code'] == 0
            and gt.get('session_id') is None and type(gt['output']) is str, 'actual generation typed closed0')
    stdout = json.loads(gt['output'].strip().splitlines()[-1])
    require(stdout['status'] == 'FOUR_ORIGINAL_ASCII_SOURCE_PREPARATION_ONLY'
            and stdout['ready_pin'] == p_ready and all(stdout[k] is False for k in FLAGS), 'generation stdout same full readyPF')
    selected = ready['selected_Source_pins'] + [p_ready, p_generation]
    require(len(ready['selected_Source_pins']) == 149
            and len({p['path'] for p in ready['selected_Source_pins']}) == 149
            and ready['selected_Source_pins'] == ready['dependencies'], 'all149 precise unique selected metadata/Source')
    for p in selected:
        full(p)
    parsed = []
    for p in selected:
        if p['path'].endswith('.py'):
            ast.parse(Path(p['path']).read_text(), filename=p['path'])
            parsed.append(p)
    plan = read(ready['control_plan_pin'])
    proof = read(plan['original_whole_source_proof_pin'])
    old = read(plan['selected_prior_original38_plan_pin'])
    require(plan['schema'] == 'FOUR_ORIGINAL_ASCII_GENDF_STREAM_SOURCE_ONLY_PLAN_V1'
            and plan['source_only'] is True and plan['extractor_executed'] is False
            and all(plan[k] is False for k in FLAGS)
            and ready['original_caps'] == plan['original_caps'] == old['original_caps'] == CAPS,
            'unchanged original caps and Source-only plan')
    roots = plan['complete_joint_roots']
    expected_delta = [str(REC / 'literal4_completed_compare_spool_retirement_20261014_v1'),
                      str(REC / 'one_actual_track_H150_NZ48_full370_component_source_v1_20261014'),
                      str(ROOT / 'validation/artifacts/axial-material-one-actual-track-H150-NZ48-full370-component-20261014-v1'),
                      str(BASE.parent), plan['planned_actual_output_root']]
    require(len(old['complete_joint_roots']) == 38 and len(roots) == len(set(roots)) == 43
            and roots == old['complete_joint_roots'] + expected_delta
            and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b),
            'exact retained original38 plus declared five disjoint roots')
    require(len(old['explicit_cumulative_metadata_file_pins']) == 4
            and all(p in plan['explicit_cumulative_metadata_file_pins'] for p in old['explicit_cumulative_metadata_file_pins'])
            and len(plan['explicit_cumulative_metadata_file_pins']) == 138
            and all(p in ready['dependencies'] for p in plan['explicit_cumulative_metadata_file_pins']),
            'prior4 plus exact full138 explicit metadata retained')
    require(not os.path.lexists(plan['planned_actual_output_root'])
            and not any(os.path.lexists(BASE / n) for n in ('FINAL_SOURCE_FREEZE.json', 'FINAL_HOST_FREEZE.json',
                                                          'FINAL_ROOT_REVIEWABLE_CLI.json', 'FINAL_PUBLICATION_RECEIPT.json')),
            'business namespace and Root once publication still fresh')
    retirement = read(plan['actual_precise_retirement_receipt_pin'])
    retirement_tools = read(plan['actual_Root_retirement_true_tools_pin'])
    rt = retirement_tools['actual_execution_return']
    require(retirement['schema'] == 'LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'
            and retirement['mode'] == 'execute'
            and retirement['status'] == 'RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'
            and retirement['failure'] is None and retirement['actual_released_bytes'] == 405417320
            and retirement['actual_released_pins'] == retirement['exact_target_pins']
            and len(retirement['actual_released_pins']) == 4
            and plan['actual_precise_retirement_receipt_pin']['path'] == plan['precise_required_actual_retirement_receipt_path']
            and type(rt['exit_code']) is int and rt['exit_code'] == 0 and rt.get('session_id') is None
            and json.loads(rt['output'].strip().splitlines()[-1])['receipt_pin'] == plan['actual_precise_retirement_receipt_pin'],
            'actual precise Root retirement and genuine stdoutPF')
    require(all(not os.path.lexists(p['path']) for p in retirement['actual_released_pins']), 'only four exact retired paths absent')
    require(proof['inputs'] == plan['inputs'] and proof['legacy_identity_order'] == ['dev', 'ino', 'mode', 'size', 'mtime_ns', 'ctime_ns', 'nlink']
            and proof['current_identity_order'] == ['dev', 'ino', 'mode', 'nlink', 'size', 'mtime_ns', 'ctime_ns']
            and proof['original_a11_already_applied_to_input'] is True
            and proof['second_quantization_performed'] is False and proof['original_ascii_payload_read'] is False,
            'explicit legacy7 normalization and no second formatter')
    full(proof['whole_original_scalar_helper_pin'])
    full(proof['whole_unchanged_scalar_helper_copy_pin'])
    require(Path(proof['whole_original_scalar_helper_pin']['path']).read_bytes()
            == Path(proof['whole_unchanged_scalar_helper_copy_pin']['path']).read_bytes(), 'whole unchanged scalar helper bytes')
    require(len(proof['whole_original_guard_source_copies']) == 4, 'four original whole guard Source copies')
    for row in proof['whole_original_guard_source_copies']:
        full(row['original_full_pin'])
        full(row['whole_unchanged_copy_full_pin'])
        require(Path(row['original_full_pin']['path']).read_bytes() == Path(row['whole_unchanged_copy_full_pin']['path']).read_bytes(),
                'whole unchanged guard/writer Source copy')
    require([r['nuclide'] for r in plan['inputs']] == ['Am241', 'Pu238', 'Pu239', 'Pu240']
            and [r['mat'] for r in plan['inputs']] == [9543, 9434, 9437, 9440]
            and [r['historical_proof']['round9_candidate_index'] for r in plan['inputs']] == [201, 208, 215, 222], 'exact four originals')
    gzip_pins = []
    for row in plan['inputs']:
        hp = row['historical_proof']
        manifest = read(hp['round9_manifest_pin'])
        backups = read(hp['round9_backups_pin'])
        m = manifest['candidates'][hp['round9_candidate_index']]
        matching = [r for r in backups['records'] if r['original']['path'] == m['path']]
        require(len(matching) == 1 and backups['status'] == 'PASS', 'one exact round9 backup row')
        b = matching[0]
        oldgz = m['compressed_backup']
        legacy = oldgz['identity']
        normal = dict(path=oldgz['path'], sha256=oldgz['sha256'], size_bytes=oldgz['size'],
                      identity=[legacy[0], legacy[1], legacy[2], legacy[6], legacy[3], legacy[4], legacy[5]])
        require(row['gzip_primary_current_full_pin'] == normal
                and all(b['backup'][k] == oldgz[k] for k in ('path', 'identity', 'size', 'sha256'))
                and all(b['original'][k] == m[k] for k in ('path', 'identity', 'size', 'sha256'))
                and b['verified_decompressed'] == dict(size=row['historical_original_ASCII_size_bytes'],
                                                       sha256=row['historical_original_ASCII_sha256'])
                and m['path'] == row['historical_original_ASCII_path']
                and m['size'] == row['historical_original_ASCII_size_bytes']
                and m['sha256'] == row['historical_original_ASCII_sha256'], 'historical original/gzip crossbinding')
        current(normal)  # Deliberately no gzip payload read in this Source-only review.
        gzip_pins.append(normal)
        require(not os.path.lexists(row['historical_original_ASCII_path'])
                and hp['current_original_file_present'] is False and hp['current_original_PF_not_invented'] is True,
                'absent historical ASCII is not declared current')
        groupr = read(hp['actual_GROUPR_receipt_pin'])
        dragr = read(hp['actual_DRAGR_receipt_pin'])
        hashes = read(hp['actual_DRAGR_input_hashes_pin'])
        folder = Path(row['historical_original_ASCII_path']).parents[1]
        binary = folder / 'dragr/tape24'
        require(type(groupr['returncode']) is int and groupr['returncode'] == 0
                and groupr['output_sha256'] == row['historical_original_ASCII_sha256']
                and type(dragr['returncode']) is int and dragr['returncode'] == 0
                and hashes[str(binary)] == row['historical_original_ASCII_sha256']
                and not os.path.lexists(binary)
                and m['historical_payload_proof']['sha256'] == hp['actual_GROUPR_receipt_pin']['sha256']
                and m['historical_payload_proof']['result_manifest_sha256'] == hp['actual_result_sha256_manifest_pin']['sha256'],
                'closed original producer/consumer receipts and missing binary context precise')
        full(hp['actual_GROUPR_deck_pin'])
        full(hp['actual_DRAGR_deck_pin'])
        gtext = Path(hp['actual_GROUPR_deck_pin']['path']).read_text()
        dtext = Path(hp['actual_DRAGR_deck_pin']['path']).read_text()
        require('moder' in gtext and '-27 30' in gtext and '24 -25' in dtext and '-21 -23 -25' in dtext
                and all(str(t) in gtext for t in row['original_source_deck_temperatures_K'][3:6]),
                'original format1 ASCII decks and precise input temperature grid')
    require(sum(r['historical_original_ASCII_size_bytes'] for r in plan['inputs']) == 284814387
            and plan['original_decompressed_payload_expected_bytes'] == 284814387
            and plan['original_ascii_output_files_planned'] == 0, 'whole expected original four payload bytes, no unpackfiles')
    stream = (BASE / 'stream_four_original_ascii_gendf.py').read_text()
    v2stream = (BASE.parent / 'v2/stream_four_original_ascii_gendf.py').read_text()
    require(v2stream.count("require(sections,'actual MF3 and MF6 inventories present')") == 1
            and stream == v2stream.replace("require(sections,'actual MF3 and MF6 inventories present')",
                                          "require(bool(sections),'actual MF3 and MF6 inventories present')"),
            'v3 exact single strict-boolean fix')
    required_child = ["gzip.GzipFile(fileobj=compressed,mode='rb')", "hashlib.sha256()", "self.stream.readline(83)",
                      "compressed.read(1)==b''", "compressed.bytes==p['size_bytes']", "compressed.digest.hexdigest()==p['sha256']",
                      "reader.bytes==row['historical_original_ASCII_size_bytes']", "reader.digest.hexdigest()==row['historical_original_ASCII_sha256']",
                      "ng==370 and ngg==0 and npl==383", "len(grids)==8", "nz==10", "energy=payload[11:382]",
                      "1<=nl<=8", "nz in(1,10)", "0<=npl<=88800", "npl==ng2*active['nl']*active['nz']",
                      "len([g for g in grids if g['temperature_K']==section['temperature_K']])==1",
                      "require(bool(sections)", "second_quantization_performed=False", "SCAT_constructed=False"]
    require(all(s in stream for s in required_child), 'whole actual stream/hash/grid/dimension Source gates inspected')
    host = (BASE / 'run_guarded_four_original_ascii_gendf.py').read_text()
    publisher = (BASE / 'write_once_Root_four_original_ascii_SF_HF_CLI.py').read_text()
    require(host.count('runner.execute(') == 1 and 'runner.execute(stage,\'four_original_ASCII_fullEOF_inventory\',cmd,600)' in host
            and '1800-(time.monotonic()-start)' in host and '512*2**20' in host
            and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)' in host
            and 'type(runner)is full.OwnRSSSerialExecutor' in host
            and 'hf[\'explicit_cumulative_metadata_file_pins\']' in host
            and 'sum(unlinked.values())<2*2**30' in host and "len(runner.records)==1" in host,
            'original guard class/MRO, one child, exact caps, cumulative metadata and open-unlinked retained')
    require('subprocess' not in publisher and 'runner.execute' not in publisher
            and "with Path(p).open('x')" in publisher
            and "type(t['exit_code'])is int and t['exit_code']==0" in publisher
            and "json.loads(t['output'].strip().splitlines()[-1])['review_pin']==pp" in publisher
            and 'all(contains(peer,p)for p in selected)' in publisher,
            'Root publisher once, peer/generation exactPF closed0, no sciencebody')
    require(ready['original_complete_ENV_Python_B_prefix'] == ['/usr/bin/env', '-u', 'PYTHONOPTIMIZE',
            'PYTHONDONTWRITEBYTECODE=1', 'OMP_NUM_THREADS=1', 'OPENBLAS_NUM_THREADS=1', 'MKL_NUM_THREADS=1',
            'VECLIB_MAXIMUM_THREADS=1', 'NUMEXPR_NUM_THREADS=1', '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '-B'],
            'original complete interpreter environment prefix')
    support_root = REC / 'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'
    guard_sources = [(support_root / 'prepare_qualified_AB_source_factor_production.py', '16e4b6f213689a01e6b957f93370c39692526f56fd1e613c4541e4b17e676e8d'),
                     (ROOT / 'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py', 'ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022'),
                     (ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py', '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
                     (support_root / 'runtime/production_runner.py', 'b8418e994a3765540dd6e0f36970c80a166813d4d75c39943c7b7dbfb359176d')]
    guard_pins = []
    for q, wanted in guard_sources:
        p = pin(q)
        require(p['sha256'] == wanted, 'whole original Source closure hash')
        ast.parse(q.read_text(), filename=str(q))
        guard_pins.append(p)
    guard_folder = ROOT / 'validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard'
    pg = pin(guard_folder / 'guard_controls.json')
    require(pg['sha256'] == 'ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454', 'original guard actual admission fullEOF')
    guard = read(pg)
    tested = pin(guard_folder / 'tested_driver_source.py')
    require(tested['sha256'] == guard['source_sha256']
            and class_text(guard_sources[2][0], 'OwnRSSSerialExecutor') == class_text(tested['path'], 'OwnRSSSerialExecutor')
            and guard['positive_child_completed'] is True and guard['actual_oversize_child_rejected'] is True
            and guard['terminated_own_child_not_live'] is True and guard['rss_cap_mib'] == 512,
            'whole unchanged original OwnRSS class and retained live proof')
    admission = [pg, tested]
    for name, wanted in guard['control_files'].items():
        p = pin(guard_folder / name)
        require(p['sha256'] == wanted, 'original declared live guard control hash')
        admission.append(p)
    for p in selected:
        current(p)
    for p in gzip_pins:
        current(p)
    report = dict(schema='INDEPENDENT_FOUR_ORIGINAL_ASCII_STREAM_SOURCE_ONLY_REVIEW_V3',
                  status='PASS_FOUR_ORIGINAL_ASCII_STREAM_V3_SOURCE_ONLY_FULL_EOF_CURRENT7_REVIEW',
                  source_only=True, failure=None, selected_Source_pins=selected,
                  complete_AST_parsed_Source_pins=parsed, original_dynamic_guard_Source_pins=guard_pins,
                  original_live_guard_admission_full_pins=admission,
                  current_gzip_primary_pins_checked_without_payload_read=gzip_pins,
                  exact_retired_pins=retirement['actual_released_pins'],
                  original38_retained=True, complete_joint_roots=roots,
                  complete_explicit_metadata_count=138, selected_Source_pin_count=149,
                  original_caps=CAPS, whole_original_helper_and_four_guard_copies_equal=True,
                  original_archive_lineage_full_metadata_EOF_verified=True,
                  explicit_legacy7_to_current7_mapping_verified=True,
                  static_child_dual_hash_streaming_and_original_grid_validation_reviewed=True,
                  original_ASCII_decoded_temperatures_preserved=True, second_quantization_performed=False,
                  v2_unchanged_frozen_bool_failure_retained=True, v3_exact_single_bool_fix_reviewed=True,
                  actual_generation_closed0_verified=True, Root_final_publication_executed=False,
                  gzip_payload_read=False, original_ascii_payload_read=False,
                  sciencebody_imported_or_executed=False, native_engines_started=0, **FLAGS)
    target = BASE / 'independent_source_review_20261014/REVIEW.json'
    new(target, report)
    print(json.dumps(dict(status=report['status'], review_pin=pin(target), **FLAGS)), flush=True)


if __name__ == '__main__':
    main()
