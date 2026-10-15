"""Prepare/verify exact five old failed-B raw paths; --execute is explicit."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE = REC / 'storage_release_failed_B_raw_20261012'
LIBRARY = REC / 'storage_release_20261012/storage_release_common.py'
LIBRARY_SHA = '7c8b7c4f1b1d16b84e0bd3fc257ac4dc24a8bd71fa025857794fc382b5b59262'
spec = importlib.util.spec_from_file_location('frozen_exact_release_audit_helpers', LIBRARY)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
OLD1 = ART / 'axial-material-new-REAL64-native-warm-B-20261012-v1'
OLD2 = ART / 'axial-material-new-REAL64-native-warm-B-20261012-v2-initial-storage-reserve'
GROUPS = [OLD1, OLD2]
CURRENT_B = ART / 'axial-material-new-REAL64-native-warm-B-20261012-v3-process-monitor-access/Root_actual_single_plane_warm_B_summary.json'
CURRENT_61 = ART / 'axial-material-new-REAL64-native-A2-A3-complete61-route-build-only-20261012/Root_actual_build_only_summary.json'
B_FREEZE = REC / 'native_warm_B_process_monitor_host_source_v3/COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json'
A23_BIND = REC / 'native_warm_A2_A3_bounded_host_source_v2/CURRENT_A23_COMPLETE_HOST_SOURCE_BINDING.json'
A23_FREEZE = REC / 'native_warm_A2_A3_bounded_host_source_v2/COMPLETE_A23_BOUNDED_HOST_SOURCE_FREEZE.json'
AAA_PLAN = Path('/private/tmp/SPOT_AAA_full370_terminal_source_UNRUN_20261012/ACTUAL_INPUT_PIN_PLAN_UNRUN.json')
MANIFEST = PACKAGE / 'EXACT_5_OLD_FAILED_B_RAW_RELEASE_MANIFEST.json'
EXPECTED_BYTES = 467550984

def candidates():
    return sorted([OLD1 / 'B' / n for n in ['new_native_B.xsm', 'snapshot_B.xsm', 'material.xsm']]
                  + [OLD2 / 'B' / n for n in ['snapshot_B.xsm', 'material.xsm']])

def exact_json(path):
    row = c.pin(path)
    return c.read_pinned_json(row), row

def inventory():
    files, links, dirs = {}, {}, []
    stack = list(GROUPS)
    while stack:
        p = stack.pop()
        c.ancestors(p)
        if not stat.S_ISDIR(p.lstat().st_mode):
            raise RuntimeError('ordinary failed-B directory required')
        dirs.append(str(p))
        fd = os.open(p, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for entry in entries:
                    q = p / entry.name
                    s = entry.stat(follow_symlinks=False)
                    if stat.S_ISDIR(s.st_mode):
                        stack.append(q)
                    elif stat.S_ISREG(s.st_mode):
                        files[str(q)] = c.identity(s)
                    elif stat.S_ISLNK(s.st_mode):
                        links[str(q)] = dict(identity=c.identity(s), target=os.readlink(q))
                    else:
                        raise RuntimeError('special entry in failed-B directory')
        finally:
            os.close(fd)
        c.guard()
    return dict(ordinary_file_identities=files, symlinks=links, directories=sorted(dirs))

def failed_proofs():
    out = []
    for root, failure, transported in [
        (OLD1, "RuntimeError('history96GiB original cold reserve')", True),
        (OLD2, "PermissionError(1, 'Operation not permitted')", False),
    ]:
        d, row = exact_json(root / 'Root_actual_single_plane_warm_B_summary.json')
        if (d['status'] != 'FAILED_WARM_B_NATIVE_PRODUCER_NO_RETRY' or d['failure'] != failure
                or d['transport_executed'] is not transported or d['single_plane_native_producer_closed'] is not False):
            raise RuntimeError('exact old B failure proof required')
        out.append(dict(pin=row, status=d['status'], failure=d['failure'],
                        transport_executed=d['transport_executed'], single_plane_native_producer_closed=False))
    return out

def protection():
    old_rows, old_coverage = c.current_protection()
    table = {r['path']:r for r in old_rows}
    docs = []
    for p in [CURRENT_B, CURRENT_61]:
        d, row = exact_json(p)
        if p == CURRENT_B:
            if (d['status'] != 'ACTUAL_SINGLE_PLANE2_E0_WARM_B_NATIVE_PRODUCER_CLOSED0_ONLY'
                    or d['failure'] is not None or d['single_plane_native_producer_closed'] is not True
                    or d['transport_executed'] is not True or len(d['records']) != 4
                    or any(x['status'] != 'PASS' for x in d['records'])):
                raise RuntimeError('current Bv3 actual four-stage closure required')
        elif (d['status'] != 'ACTUAL_A23_FIVE_COMPILE_AND_COMPLETE61_DRAGON_LINK_CLOSED0_ONLY'
              or d['failure'] is not None or d['after_check_error'] is not None
              or len(d['records']) != 6 or any(x['status'] != 'PASS' for x in d['records'])):
            raise RuntimeError('current actual A23 full61 six-stage closure required')
        for key in ['fixed_current_pins', 'owned_runtime_pins', 'output_pins']:
            c.add_nested_pins(d.get(key, []), table)
        table[row['path']] = row
        docs.append(row)
    for p in [B_FREEZE, A23_BIND, A23_FREEZE]:
        d, row = exact_json(p)
        if p == A23_BIND and len(d['fixed_current_pins']) != 2163:
            raise RuntimeError('exact warm A23 v2 2163 fixed input binding required')
        c.add_nested_pins(d, table)
        table[row['path']] = row
        docs.append(row)
    plan, plan_row = exact_json(AAA_PLAN)
    if (plan['schema'] != 'AAA_TERMINAL_SOURCE_READONLY_ACTUAL_INPUT_PLAN_V1'
            or len(plan['inputs']) != 1129 or plan['candidate_executed'] is not False
            or plan['candidate_imported'] is not False):
        raise RuntimeError('exact saved-data AAA unexecuted input plan required')
    for p, sha in plan['inputs'].items():
        row = c.pin(p)
        if row['sha256'] != sha:
            raise RuntimeError('saved-data AAA planned SHA changed: ' + p)
        old = table.get(p)
        if old is not None and old != row:
            raise RuntimeError('AAA planned input conflicts with current full pin')
        table[p] = row
    for key in ['source', 'source_predecessor_UNRUN']:
        # The predecessor's former path now holds the revised Source; its
        # explicitly retained copy carries the predecessor hash.
        source_path = plan[key].get('retained_as', plan[key]['path'])
        row = c.pin(source_path)
        if row['sha256'] != plan[key]['sha256']:
            raise RuntimeError('AAA saved-data Source hash changed')
        table[row['path']] = row
    table[plan_row['path']] = plan_row
    docs.append(plan_row)
    rows = sorted(table.values(), key=lambda x:x['path'])
    for row in rows:
        c.same(row)
    return rows, dict(prior_current_protection=old_coverage,
        current_Bv3_four_stages_and_A23_full61_six_stages_actual_PASS_required=True,
        warm_A23_v2_direct_fixed_pins=2163, AAA_saved_data_UNRUN_input_SHA_entries=1129,
        AAA_plan_SHA_entries_upgraded_to_full_EOF_SHA_and_7ID=True,
        total_extended_full_EOF_pins=len(rows), selected_current_documents=docs,
        current_reports_use_fixed_owned_output_pins_only=True)

def disjoint(targets, protected):
    names = {r['path'] for r in protected}
    ids = set()
    for row in protected:
        s = Path(row['path']).lstat()
        if c.identity(s) != row['identity']:
            raise RuntimeError('protected full 7ID changed')
        ids.add((s.st_dev, s.st_ino))
    for row in targets:
        p = Path(row['path'])
        if p not in candidates():
            raise RuntimeError('target outside literal exact five path list')
        s = p.lstat()
        if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or c.identity(s) != row['identity']:
            raise RuntimeError('exact ordinary nlink1/stable failed-B raw required')
        if str(p) in names or (s.st_dev, s.st_ino) in ids:
            raise RuntimeError('old raw remains a current or planned mandatory dependency: ' + str(p))

def source_pins():
    library = c.pin(LIBRARY)
    if library['sha256'] != LIBRARY_SHA or Path(c.__file__) != LIBRARY:
        raise RuntimeError('exact already-frozen streaming audit helper Source required')
    return [c.pin(Path(__file__)), library]

def prepare():
    if MANIFEST.exists():
        raise RuntimeError('immutable exact-five manifest already exists')
    sources = source_pins()
    proofs = failed_proofs()
    protected, coverage = protection()
    before = inventory()
    targets = [c.pin(p) for p in candidates()]
    if len(targets) != 5 or sum(x['size_bytes'] for x in targets) != EXPECTED_BYTES:
        raise RuntimeError('exact five failed-B raw total bytes required')
    disjoint(targets, protected)
    names = {r['path'] for r in targets}
    kept = [c.pin(p) for p in sorted(before['ordinary_file_identities']) if p not in names]
    if inventory() != before:
        raise RuntimeError('old failed directories changed during streaming audit')
    for row in sources + targets + kept + protected:
        if c.identity(Path(row['path']).lstat()) != row['identity']:
            raise RuntimeError('full observed 7ID changed before manifest creation')
    d = dict(schema='SPOT_EXACT_FIVE_OLD_FAILED_B_RAW_RELEASE_MANIFEST_V1', created_unix=time.time(),
        action_executed=False, target_count=5, total_target_logical_bytes=EXPECTED_BYTES,
        target_full_EOF_pins=targets, source_pins=sources, closed_failure_proofs=proofs,
        current_and_planned_mandatory_full_EOF_pins=protected, protection_coverage=coverage,
        retained_ordinary_file_full_EOF_pins=kept, complete_before_inventory=before,
        preparation_after_inventory_equals_before=True, original_budget_before=c.budget(),
        consequence='Only five superseded old failed-B raw files are lost for historical raw replay. All other reports, logs, bindings, source, proof, runtime and directory entries remain. The qualified current Bv3 raw, A1, A23 and saved-data AAA plan remain protected.',
        scientific_computation_started=False, numerical_thresholds_or_budgets_changed=False, goal_complete=False)
    c.write_new(MANIFEST, d)
    print(json.dumps(dict(status='EXACT_FIVE_MANIFEST_PREPARED_NO_DELETE', manifest=c.pin(MANIFEST),
        target_count=5, target_bytes=EXPECTED_BYTES, retained_regular_files=len(kept),
        retained_symlinks=len(before['symlinks']), protected_full_EOF_pins=len(protected))))

def verify_or_execute(args):
    row = c.pin(MANIFEST)
    if row['sha256'] != args.manifest_sha256 or row['identity'] != json.loads(args.manifest_seven_id):
        raise RuntimeError('explicit Root-selected exact manifest SHA/7ID required')
    m = c.read_pinned_json(row)
    if (m['schema'] != 'SPOT_EXACT_FIVE_OLD_FAILED_B_RAW_RELEASE_MANIFEST_V1' or m['action_executed']
            or m['target_count'] != 5 or m['total_target_logical_bytes'] != EXPECTED_BYTES
            or [r['path'] for r in m['target_full_EOF_pins']] != [str(p) for p in candidates()]
            or sum(r['size_bytes'] for r in m['target_full_EOF_pins']) != EXPECTED_BYTES):
        raise RuntimeError('hard-coded exact-five frozen manifest required')
    receipt = PACKAGE / ('ACTUAL_EXACT_FIVE_RELEASE_EXECUTION_RECEIPT.json' if args.execute else 'ACTUAL_READONLY_EXACT_FIVE_VERIFICATION_RECEIPT.json')
    if receipt.exists() or receipt.with_suffix('.pending').exists():
        raise RuntimeError('no receipt overwrite or automatic execution retry')
    if source_pins() != m['source_pins'] or failed_proofs() != m['closed_failure_proofs']:
        raise RuntimeError('Source or saved closed failure proofs changed')
    protected, coverage = protection()
    if protected != m['current_and_planned_mandatory_full_EOF_pins'] or coverage != m['protection_coverage']:
        raise RuntimeError('current or planned mandatory protection scope changed')
    targets = m['target_full_EOF_pins']
    kept = m['retained_ordinary_file_full_EOF_pins']
    for item in targets + kept:
        c.same(item)
    if inventory() != m['complete_before_inventory']:
        raise RuntimeError('exact two old failed-B directory inventories changed')
    disjoint(targets, protected)
    before = c.budget()
    r = dict(schema='SPOT_EXACT_FIVE_OLD_FAILED_B_RAW_ACTUAL_RECEIPT_V1', started_unix=time.time(),
        manifest_pin=row, execute_requested=args.execute, all_full_EOF_preflight_verified=True,
        original_budget_before=before, deletion_records=[], retention_records=[],
        status='READONLY_EXACT_FIVE_VERIFIED' if not args.execute else 'EXECUTING',
        scientific_computation_started=False, budgets_or_thresholds_changed=False, goal_complete=False)
    c.write_new(receipt, r)
    if not args.execute:
        print(json.dumps(dict(status=r['status'], receipt=c.pin(receipt), deletion_executed=False)))
        return
    try:
        for item in targets:
            c.same(item)
            disjoint([item], protected)
            p = Path(item['path'])
            fd = os.open(p.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                if c.identity(os.stat(p.name, dir_fd=fd, follow_symlinks=False)) != item['identity']:
                    raise RuntimeError('single target changed immediately before unlink')
                os.unlink(p.name, dir_fd=fd)
            finally:
                os.close(fd)
            if os.path.lexists(p):
                raise RuntimeError('unlinked target reappeared')
            r['deletion_records'].append(dict(path=item['path'], original_full_EOF_pin=item,
                action='UNLINK_EXACT_FROZEN_ORDINARY_FILE', confirmed_absent=True, unix=time.time()))
            c.update_owned_receipt(receipt, r)
        for item in kept:
            c.same(item)
            r['retention_records'].append(dict(path=item['path'], full_EOF_SHA_and_7ID_unchanged=True))
        for item in protected + m['source_pins'] + [row]:
            c.same(item)
        expected = dict(m['complete_before_inventory'])
        expected['ordinary_file_identities'] = {p:i for p,i in expected['ordinary_file_identities'].items()
                                                if p not in {x['path'] for x in targets}}
        if inventory() != expected:
            raise RuntimeError('unexpected retained entry change after exact release')
        after = c.budget()
        if before['artifact_bytes'] - after['artifact_bytes'] != EXPECTED_BYTES or before['regular_files'] - after['regular_files'] != 5:
            raise RuntimeError('history changed beyond exact five raw paths; check concurrent artifact writers')
        r.update(status='EXACT_FIVE_OLD_FAILED_B_RELEASE_AND_RETENTION_VERIFIED',
            original_budget_after=after, logical_bytes_released=EXPECTED_BYTES, deleted_file_count=5,
            all_other_old_failed_directory_entries_verified_unchanged=True,
            current_and_planned_dependency_closure_full_EOF_verified_unchanged=True, completed_unix=time.time())
    except BaseException as e:
        r.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY', error=repr(e), completed_unix=time.time())
        c.update_owned_receipt(receipt, r)
        raise
    c.update_owned_receipt(receipt, r)
    print(json.dumps(dict(status=r['status'], receipt=c.pin(receipt), deleted_file_count=5,
        logical_bytes_released=EXPECTED_BYTES, original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))

def main():
    ap = argparse.ArgumentParser()
    actions = ap.add_mutually_exclusive_group()
    actions.add_argument('--prepare', action='store_true')
    actions.add_argument('--execute', action='store_true')
    ap.add_argument('--manifest-sha256')
    ap.add_argument('--manifest-seven-id')
    args = ap.parse_args()
    if args.prepare:
        if args.manifest_sha256 or args.manifest_seven_id:
            raise RuntimeError('prepare does not accept manifest authority arguments')
        prepare()
    else:
        if not args.manifest_sha256 or not args.manifest_seven_id:
            raise RuntimeError('verification/execution requires external exact manifest SHA/7ID')
        verify_or_execute(args)

if __name__ == '__main__':
    main()
