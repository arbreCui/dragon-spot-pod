"""Independent readonly postrelease audit. Never imports or calls deletion hosts."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
PKG = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011/storage_release_closed_v7_v8_project_pair_20261013'
OUT = Path(__file__).absolute().parent
START = time.monotonic()
CHECKS = 0
VERIFIED = {}
BYTES = 1498711904
TARGETS = [str(ART / ('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-' + v) / 'AAA/projected_boot.xsm') for v in ('v7', 'v8')]

def check(v, message):
    global CHECKS
    CHECKS += 1
    if not v:
        raise RuntimeError(message)
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 512 * 2**20 or time.monotonic() - START >= 1800:
        raise RuntimeError('original SELF512MiB/whole1800s audit bounds exceeded')

def seven(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(p):
    p = Path(p)
    check(p.is_absolute() and '..' not in p.parts, 'canonical absolute path')
    for parent in reversed(p.parents):
        check(stat.S_ISDIR(parent.lstat().st_mode), 'non-directory or symlink ancestor')
    before = p.lstat()
    check(stat.S_ISREG(before.st_mode), 'regular nonsymlink file')
    h = hashlib.sha256()
    count = 0
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        check(seven(os.fstat(fd)) == seven(before), 'identity changed at open')
        while True:
            chunk = os.read(fd, 2**20)
            if not chunk:
                break
            h.update(chunk)
            count += len(chunk)
            check(True, 'streaming bounds')
        check(seven(os.fstat(fd)) == seven(before), 'identity changed while reading EOF')
    finally:
        os.close(fd)
    check(seven(p.lstat()) == seven(before) and count == before.st_size, 'identity or size changed after EOF')
    return dict(path=str(p), sha256=h.hexdigest(), size_bytes=count, identity=seven(before))

def same(row):
    actual = pin(row['path'])
    check(actual == row, 'full EOF SHA/all7ID mismatch: ' + row['path'])
    old = VERIFIED.get(row['path'])
    check(old is None or old == actual, 'conflicting or changed repeated fullpin')
    VERIFIED[row['path']] = actual
    return actual

def exact_json(row):
    same(row)
    raw = Path(row['path']).read_bytes()
    check(len(raw) == row['size_bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'] and seven(Path(row['path']).lstat()) == row['identity'], 'JSON changed after EOF')
    return json.loads(raw)

def inventory():
    files, links, dirs = {}, {}, {}
    stack = [Path(t).parent.parent for t in TARGETS]
    while stack:
        directory = stack.pop()
        s = directory.lstat()
        check(stat.S_ISDIR(s.st_mode), 'ordinary closed branch directory')
        dirs[str(directory)] = seven(s)
        fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    p = directory / e.name
                    s = e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):
                        stack.append(p)
                    elif stat.S_ISREG(s.st_mode):
                        files[str(p)] = seven(s)
                    elif stat.S_ISLNK(s.st_mode):
                        links[str(p)] = dict(identity=seven(s), target=os.readlink(p))
                    else:
                        raise RuntimeError('special closed-branch entry')
        finally:
            os.close(fd)
        check(True, 'inventory bounds')
    return dict(ordinary_file_identities=files, symlinks=links, directory_identities=dirs)

def budget_snapshot():
    # Same apparent regular-file scope: every current direct axial-material-* root.
    roots = sorted(str(p) for p in ART.glob('axial-material-*'))
    total, count, stack = 0, 0, list(roots)
    while stack:
        p = Path(stack.pop())
        if not p.exists():
            continue
        check(stat.S_ISDIR(p.lstat().st_mode), 'history root/descendant must be nonsymlink directory')
        fd = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    try:
                        s = e.stat(follow_symlinks=False)
                    except FileNotFoundError:
                        continue
                    if stat.S_ISDIR(s.st_mode):
                        stack.append(str(p / e.name))
                    elif stat.S_ISREG(s.st_mode):
                        total += s.st_size
                        count += 1
        finally:
            os.close(fd)
        check(True, 'history bounds')
    end_roots = sorted(str(p) for p in ART.glob('axial-material-*'))
    return dict(artifact_bytes=total, regular_files=count, disk_free_bytes=shutil.disk_usage(ART).free,
                root_set_stable_during_observation=roots == end_roots, root_count=len(roots),
                observation_started_after_cleanup=True, concurrent_v9_output_exists=os.path.lexists(ART / 'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'),
                interpretation='CURRENT_CONCURRENT_OUTPUT_OBSERVATION_NOT_AN_EXACT_CLEANUP_DELTA_AUTHORITY')

def main():
    mp = dict(path=str(PKG / 'EXACT_TWO_CLOSED_FAILED_RUN_PROJECT_PRIVATE_COPY_MANIFEST.json'), sha256='cd9959328b0f12ff88f5b858a9ffb41ae6221ca0da760e2b293a3b999b4d6c19', size_bytes=3861469, identity=[16777229,49980346,33188,1,3861469,1791847142031341032,1791847142031341032])
    fp = dict(path=str(PKG / 'COMPLETE_EXACT_TWO_PROJECT_RELEASE_SOURCE_FREEZE.json'), sha256='506c02b59a9b18bc9e9d1045d2cd2878a1b9348a03d2a84215f1bbd5477671fe', size_bytes=3383, identity=[16777229,49980480,33188,1,3383,1791847182418256949,1791847182418256949])
    manifest, freeze = exact_json(mp), exact_json(fp)
    check(freeze['manifest_pin'] == mp and freeze['exact_target_count'] == 2 and freeze['frozen_manifest_protected_count'] == 4390, 'exact frozen manifest selection')
    check(manifest['target_count'] == 2 and manifest['total_target_logical_bytes'] == BYTES and manifest['action_executed'] is False, 'unmodified original preparation Source')
    for row in freeze['Source_pins'] + [freeze['selected_exact_execution_CLI_pin']]:
        same(row)
    check(freeze['Source_pins'] == manifest['Source_pins'], 'frozen Source identity equality')
    tp = pin(PKG / 'ROOT_ACTUAL_EXACT_TWO_RELEASE_TRUE_TOOL_RETURNS.json')
    true = exact_json(tp)
    check(true['observed_closed'] is True and true['original_integer_exit_code'] == 0 and true['terminal']['exit_code'] == 0 and true['terminal']['chunk_id'] == '16fdee' and true['initial']['chunk_id'] == '7a746b' and true['initial']['session_id'] == 82301, 'true Root actual closed0 tool returns')
    terminal_output = json.loads(true['terminal']['output'])
    receipt_pin = terminal_output['receipt_pin']
    check(receipt_pin['path'] == str(PKG / 'ACTUAL_EXACT_TWO_PROJECT_PRIVATE_COPY_RELEASE_RECEIPT.json') and receipt_pin['sha256'] == '9294696fc115befeb919f70995cc0b5f0c8da8ae0a7bfd7b32e3ffca492e1638' and receipt_pin['identity'] == [16777229,50010663,33188,1,359503,1791868911294485386,1791868911294917471], 'Root terminal externally selected actual receipt fullPF')
    receipt = exact_json(receipt_pin)
    check(receipt['status'] == 'EXACT_TWO_PRIVATE_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED' and receipt['manifest_pin'] == mp and receipt['execute_requested'] is True and receipt['deleted_files'] == 2 and receipt['logical_bytes_released'] == BYTES, 'actual complete exacttwo release receipt')
    check(receipt['compiler_or_numerical_business_executed'] is False and receipt['goal_complete'] is False and true['numerical_business_executed'] is False, 'cleanup carries no science/goal success')
    candidates = manifest['target_full_EOF_pins']
    check([p['path'] for p in candidates] == TARGETS and sum(p['size_bytes'] for p in candidates) == BYTES and all(p['identity'][3] == 1 and stat.S_ISREG(p['identity'][2]) for p in candidates), 'literal two owned candidate definitions')
    check(receipt['deletion_records'] == [dict(original_fullpin=p, confirmed_absent=True) for p in candidates], 'exact two real deletion records')
    for target in TARGETS:
        check(not os.path.lexists(target), 'released exact target must remain absent')
    protected = manifest['current_protected_full_EOF_pins']
    retained = manifest['retained_ordinary_full_EOF_pins']
    check(len(protected) == 4390 and len(retained) == 472 and len({p['path'] for p in protected}) == 4390 and len({p['path'] for p in retained}) == 472, 'complete deduplicated protected and retained scope')
    paths = {p['path'] for p in protected}
    inodes = {tuple(p['identity'][:2]) for p in protected}
    check(all(p['path'] not in paths and tuple(p['identity'][:2]) not in inodes for p in candidates), 'targets disjoint from every current protected path and inode')
    for row in protected + retained + manifest['Source_pins']:
        same(row)
    dag = manifest['Source_DAG_provenance']
    roles = dag['roles']
    protected_table = {p['path']:p for p in protected}
    catalog_path = str(ROOT / 'validation/axial_material/root64_epoch_recovery_20261011/current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')
    binding_path = str(ROOT / 'validation/axial_material/root64_epoch_recovery_20261011/current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')
    catalog = exact_json(protected_table[catalog_path])
    binding = exact_json(protected_table[binding_path])
    catalog_rows = [r['current_pin'] for r in catalog['rows']]
    common_rows = binding['fixed_current_pins']
    check(len(catalog_rows) == 3040 and len(common_rows) == 2012 and len(roles['saved_full370_current3315']) == 3315, 'entire original row counts, not a false unique-path count')
    for role, rows in [('catalog_all3040_current_rows',catalog_rows), ('current_Common_BIND2012',common_rows)]:
        check(set(roles[role]) == {r['path'] for r in rows}, 'exact role dedup path union includes every row')
        for row in rows:
            check(protected_table[row['path']] == row, 'every full input row has exact verified current protected pin')
    check(dag['all257_v9_dependencies_included'] is True and dag['all_business_and_physics_qualification_flags_unchanged'] is True, 'full v9 and original nonqualification scope preserved')
    old, new = manifest['complete_before_inventory'], inventory()
    expected = {p:i for p,i in old['ordinary_file_identities'].items() if p not in TARGETS}
    check(len(old['ordinary_file_identities']) == 474 and new['ordinary_file_identities'] == expected and len(expected) == 472, 'complete inventory removes exactly two ordinary files')
    check(new['symlinks'] == old['symlinks'] and set(new['directory_identities']) == set(old['directory_identities']), 'all links and all60 directories unchanged in presence')
    changes = {p['path']:p for p in receipt['observed_parent_directory_changes']}
    parents = {str(Path(t).parent) for t in TARGETS}
    check(set(changes) == parents, 'exact two affected directories')
    for p,before in old['directory_identities'].items():
        after = new['directory_identities'][p]
        if p in parents:
            row = changes[p]
            check(before == row['before_seven_id'] and after == row['after_seven_id'] and after[:3] == before[:3] and row['ordinary_entry_delta'] == -1 and row['exact_other_file_and_link_inventory_unchanged'] is True, 'actual parent native filesystem metadata exact receipt equality')
        else:
            check(after == before, 'unaffected directory all7ID exact')
    for proof in manifest['closed_failed_overall_run_proofs']:
        summary = exact_json(proof['failed_overall_summary_pin'])
        closed = exact_json(proof['Root_true_closed_exit1_tool_receipt_pin'])
        same(proof['actual_owning_pipeline_Source_pin'])
        check(summary['status'] == 'FAILED_UNQUALIFIED_NO_RETRY' and summary['engineering_three_plane_closed0'] is False and len(summary['records']) == 41 and summary['after_check_error'] is None, 'historical failed aggregate scope unchanged')
        check(closed['observed_closed'] is True and closed['original_integer_exit_code'] == 1 and closed['terminal']['exit_code'] == 1, 'old trueRoot closure unchanged')
        selected = {r['label']:r for r in summary['records']}
        check(selected['AAA/global_positive']['status'] == 'PASS' and selected['AAA/project_positive']['status'] == 'PASS' and summary['records'][-1]['label'] == 'AAA/view_missing_operand', 'preserve actual individual GLOBAL PROJECT PASS vs failedBOOT prefix')
        check(len(proof['all41_actual_child_closures']) == 41, 'all41 historical watchdogs included')
        for row in proof['all41_actual_child_closures']:
            watchdog = exact_json(row['watchdog_pin'])
            same(row['log_pin'])
            record = selected[row['label']]
            check(watchdog['returncode'] == (0 if record['status'] == 'PASS' else 1) and watchdog['command'] == record['command'] and watchdog['liveness_group_cleanup'] is True and watchdog['own_child_only'] is True and watchdog['limit_failure'] is None and watchdog['rss_cap_mib'] == 512 and 0 < watchdog['elapsed_seconds'] < watchdog['wall_cap_seconds'] <= 600 and 0 <= watchdog['sampled_peak_rss_mib'] < 512, 'all original child closures and bounds retain true evidence')
    before, after = receipt['original_budget_before'], receipt['original_budget_after']
    check(before['artifact_bytes'] - after['artifact_bytes'] == BYTES and before['regular_files'] - after['regular_files'] == 2, 'actual execution exact logical bytes/two files delta')
    for value in (before, after):
        remainder = 96 * 2**30 - value['artifact_bytes'] - 20971764748 - 64 * 2**20 - 2 * 2**30
        check(value['artifact_budget_bytes'] == 96 * 2**30 and value['min_free_bytes'] == 8 * 2**30 and value['disk_free_bytes'] >= 8 * 2**30 and value['remaining_after_original_initial_reserves_bytes'] == remainder and value['original_initial_reserve_admitted'] == (remainder > 0), 'unchanged original history/fresh/cold/metadata/free budget arithmetic')
    check(before['remaining_after_original_initial_reserves_bytes'] == -246785547 and after['remaining_after_original_initial_reserves_bytes'] == 1251926357 and after['original_initial_reserve_admitted'] is True, 'actual reserve refusal cleared under original constants')
    current = budget_snapshot()
    for row in VERIFIED.values():
        check(seven(Path(row['path']).lstat()) == row['identity'], 'full EOF validated file remained stable through audit')
    report = dict(schema='INDEPENDENT_READONLY_EXACT_TWO_PROJECT_RELEASE_POSTCHECK_V1', status='ALL_PROTECTED_RETAINED_FULL_EOF_EXACT_TWO_ABSENT_CLOSED0_POSTCHECK',
                  manifest_pin=mp, source_freeze_pin=fp, Root_true_actual_tool_returns_pin=tp, actual_release_receipt_pin=receipt_pin,
                  target_count=2, targets_confirmed_absent=TARGETS, deleted_logical_bytes=BYTES, protected_count=4390, retained_count=472,
                  complete_before_regular_files=474, complete_after_regular_files=472, directory_count=len(new['directory_identities']),
                  exact_all_other_file_link_directory_entries_preserved=True, parent_native_metadata_exact_actual_receipt_match=True,
                  full_EOF_unique_verified_files=len(VERIFIED), full_EOF_unique_verified_bytes=sum(p['size_bytes'] for p in VERIFIED.values()),
                  full_EOF_verified_pins=sorted(VERIFIED.values(),key=lambda p:p['path']), checks=CHECKS,
                  original_execution_artifact_bytes_before=before['artifact_bytes'], original_execution_artifact_bytes_after=after['artifact_bytes'],
                  exact_original_execution_regular_file_delta=2, original_initial_reserve_after_execution_bytes=1251926357,
                  original_initial_reserve_after_execution_admitted=True, current_concurrent_history_observation=current,
                  old_GLOBAL_and_PROJECT_individual_PASS_preserved=True, old_failed_aggregate_and_BOOT_nonqualification_preserved=True,
                  old_private_PROJECT_raw_replay_unavailable=True, deletion_or_preparation_host_called=False, compiler_or_numerical_business_executed=False,
                  original_physics_inputs_caps_thresholds_unchanged=True, goal_complete=False,
                  audit_elapsed_seconds=time.monotonic()-START, audit_SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  reviewer_Source_pin=pin(Path(__file__).absolute()))
    path = OUT / 'INDEPENDENT_POSTRELEASE_FULL_EOF_REVIEW.json'
    raw = (json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd,'wb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    print(json.dumps(dict(status=report['status'],review_pin=pin(path),full_EOF_files=report['full_EOF_unique_verified_files'],full_EOF_bytes=report['full_EOF_unique_verified_bytes'],checks=report['checks'],original_reserve_after_execution_bytes=1251926357,concurrent_output_present=current['concurrent_v9_output_exists'],deletion_executed_by_review=False)))

if __name__ == '__main__':
    main()
