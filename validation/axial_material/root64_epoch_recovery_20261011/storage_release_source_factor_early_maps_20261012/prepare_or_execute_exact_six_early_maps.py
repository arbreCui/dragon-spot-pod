"""Exact six superseded early-map raw files; no failed-run claim; default verify."""
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
PACKAGE = REC / 'storage_release_source_factor_early_maps_20261012'
PREVIOUS_SOURCE = REC / 'storage_release_failed_B_raw_20261012/prepare_or_execute_failed_B_release.py'
PREVIOUS_SHA = '917779a6d2520d4e3651909e5a98c66847568d040c0b61d1228b1e50f3a82050'
spec = importlib.util.spec_from_file_location('frozen_current_release_protection_helpers', PREVIOUS_SOURCE)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
c = b.c
BRANCH = ART / 'axial-material-production-qualified-AB-source-factor-20261006'
AAA3 = REC / 'aaa_three_plane_streaming_source_v1'
FORMAL_PLAN = AAA3 / 'PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json'
FORTRAN_FREEZE = AAA3 / 'COMPLETE_FORTRAN_SOURCE_FREEZE.json'
MANIFEST = PACKAGE / 'EXACT_6_SOURCE_FACTOR_EARLY_MAP_RAW_MANIFEST.json'
EXPECTED_BYTES = 1427734232

def candidates():
    return sorted([BRANCH / 'AAA' / name / file for name in ['map001', 'map002']
        for file in ['closed_snapshots.xsm', 'candidate_snapshots.xsm', 'candidate_radial.xsm']])

def sources():
    rows = [c.pin(Path(__file__)), c.pin(PREVIOUS_SOURCE), c.pin(b.LIBRARY)]
    if rows[1]['sha256'] != PREVIOUS_SHA or rows[2]['sha256'] != b.LIBRARY_SHA:
        raise RuntimeError('exact already-frozen readonly protection helper Sources required')
    return rows

def inventory():
    files, links, dirs = {}, {}, []
    stack = [BRANCH]
    while stack:
        p = stack.pop()
        c.ancestors(p)
        if not stat.S_ISDIR(p.lstat().st_mode):
            raise RuntimeError('ordinary source-factor branch directory required')
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
                        raise RuntimeError('unexpected special branch entry')
        finally:
            os.close(fd)
        c.guard()
    return dict(ordinary_file_identities=files, symlinks=links, directories=sorted(dirs))

def branch_proof():
    d, row = b.exact_json(BRANCH / 'AAA/run_status.json')
    if (d['classification'] != 'WAITING_REFERENCE' or d['completed_maps'] != 12
            or d['reference_qualification'] is not None or d['cases']['AAA']['classification'] != 'VALID_MET'
            or d['cases']['AAA']['final_directory'] != str(BRANCH / 'AAA/map012')):
        raise RuntimeError('exact completed12/WAITING_REFERENCE branch evidence required')
    proofs = [row]
    for name in ['map001', 'map002']:
        stage, stage_row = b.exact_json(BRANCH / 'AAA' / name / 'result.json')
        if stage['classification'] != 'SEALED_STAGE_OUTPUTS':
            raise RuntimeError('old early-map stage result metadata must remain sealed')
        proofs.append(stage_row)
    return dict(pins=proofs, branch_classification='WAITING_REFERENCE', completed_maps=12,
        final_numerical_map_classification='VALID_MET', selected_raw_are_failed_run_outputs=False,
        selection='Only superseded map001/map002 intermediate raw; map003 onward, map012, bootstrap and training retained.')

def protection_and_source_review():
    old, old_coverage = b.protection()
    table = {r['path']:r for r in old}
    reports = []
    for name, plane in [('A2',2), ('A3',3)]:
        for dirname, filename in [
            (f'axial-material-new-REAL64-native-warm-{name}-20261012-v1', f'Root_actual_single_plane_warm_{name}_summary.json'),
            (f'axial-material-current-warm-{name}-CLE-entry-controls-20261012-v1', 'Root_actual_entry_controls_summary.json')]:
            d, row = b.exact_json(ART / dirname / filename)
            if d['failure'] is not None or not d['records']:
                raise RuntimeError('actual A2/A3 current report must be closed without failure')
            if filename.startswith('Root_actual_single_plane'):
                if (d['status'] != f'ACTUAL_SINGLE_PLANE{plane}_E0_WARM_{name}_NATIVE_PRODUCER_CLOSED0_ONLY'
                        or len(d['records']) != 4 or any(r['status'] != 'PASS' for r in d['records'])
                        or d['transport_executed'] is not True or d['single_plane_native_producer_closed'] is not True):
                    raise RuntimeError('actual independent A2/A3 producer four-stage PASS required')
            for key in ['fixed_current_pins', 'owned_runtime_pins', 'output_pins']:
                c.add_nested_pins(d.get(key, []), table)
            table[row['path']] = row
            reports.append(row)
    plan, plan_row = b.exact_json(FORMAL_PLAN)
    if (plan_row['sha256'] != '3948281d4f69755af3b1ab2ee8d14fa6ab444e2450db17adc51e21be7aedffab'
            or plan['formal_source_root'] != str(ART / 'axial-material-production-qualified-AB-rank1-factor-cache-20261007')
            or plan['source_factor_20261006_intermediate_raw_used'] is not False
            or plan['new_source_uses_rank2'] is not False or len(plan['formal_inputs']) != 13
            or len(plan['producers']) != 3):
        raise RuntimeError('exact new formal rank1 and independent producer plan required')
    c.add_nested_pins(plan, table)
    table[plan_row['path']] = plan_row
    freeze, freeze_row = b.exact_json(FORTRAN_FREEZE)
    if (freeze_row['sha256'] != '5bb9e5c9cd8f41a6985a3b61b23ee56db61aa94af0f1d0d1ff8fb906d0aa426b'
            or len(freeze['files']) != 9 or freeze['compiler_executed'] is not False
            or freeze['transport_executed'] is not False or freeze['whole_host_not_implemented_here'] is not True):
        raise RuntimeError('exact nine Source-only Fortran freeze required')
    c.add_nested_pins(freeze, table)
    table[freeze_row['path']] = freeze_row
    for origin in freeze['original_sources_still_unchanged']:
        row = c.pin(origin['path'])
        if row['sha256'] != origin['sha256']:
            raise RuntimeError('original Fortran Source hash changed')
        table[row['path']] = row
    # Read actual Fortran Source, including relative private-file construction.
    texts = {}
    for row in freeze['files']:
        c.same(row)
        text = Path(row['path']).read_text()
        if c.identity(Path(row['path']).lstat()) != row['identity']:
            raise RuntimeError('Fortran Source changed during reference review')
        if str(BRANCH) in text or any(x in text for x in ['closed_snapshots.xsm','candidate_snapshots.xsm','candidate_radial.xsm']):
            raise RuntimeError('new Fortran Source refers to selected old branch raw')
        texts[Path(row['path']).name] = text
    pack = texts['APACKX64.f90']
    boot = texts['SPOBOOX64.f90']
    if not all(x in pack for x in ['if(nentry/=7)', 'jentry(5:7)/=2', 'SPOR64_BOOT64_READ_NATIVE',
        'if(n/=1)', 'if(pl/=p.or.ep/=0)', 'shape(admitted)/=[14,370]', 'call LCMEQU(inputs(k,p),item)']):
        raise RuntimeError('actual three independent producer-copy Source anchors changed')
    if not all(x in boot for x in ["archive_file='BOOT-SOLVED-STAGE.xsm'", "'BOOT-MAC-',p,'.xsm'",
        "'BOOT-Q-',p,'.xsm'", 'if(exists)call XABORT', 'call LCMOP(archive_stage,archive_file,0,2,0)']):
        raise RuntimeError('actual relative fresh-private-file Source anchors changed')
    rows = sorted(table.values(), key=lambda x:x['path'])
    for row in rows:
        c.same(row)
    review = dict(prior_full_protection=old_coverage, prior_protected_count=len(old),
        actual_A2_A3_report_pins=reports, formal_and_producer_input_plan=plan_row,
        complete_new_Fortran_Source_freeze=freeze_row, total_protected_full_EOF_pins=len(rows),
        Source_input_and_copy_observed='APACKX64 takes four fresh output XSMs plus three independent readonly original A1/A2/A3 archives; validates own case, plane/e0, LISTDIM1 and full370x14 NativeREAD before any write; whole-tree copies six lists.',
        relative_file_construction_observed='SPOBOOX64 only creates BOOT-SOLVED-STAGE.xsm and BOOT-MAC-1..3.xsm/BOOT-Q-1..3.xsm after refusing existing files. Context and system inputs arrive through readonly kentry operands.',
        new_Source_contains_no_selected_raw_filename_or_old_branch_absolute_path=True,
        formal_rank1_bootstrap_and_training_paths_explicitly_pinned=True,
        new_complete_host_not_yet_implemented_or_executed=True,
        exclusion_scope='Current qualified route and explicitly frozen next Fortran/input plan; no claim about all future unimplemented hosts or historical replays.')
    return rows, review

def disjoint(targets, protected):
    paths = {r['path'] for r in protected}
    ids = set()
    for row in protected:
        s = Path(row['path']).lstat()
        if c.identity(s) != row['identity']:
            raise RuntimeError('current or next-Source protected 7ID changed')
        ids.add((s.st_dev,s.st_ino))
    for row in targets:
        p = Path(row['path']);s = p.lstat()
        if (p not in candidates() or not stat.S_ISREG(s.st_mode) or s.st_nlink != 1
                or c.identity(s) != row['identity']):
            raise RuntimeError('exact ordinary nlink1 early-map target required')
        if str(p) in paths or (s.st_dev,s.st_ino) in ids:
            raise RuntimeError('early raw remains a current or next-Source dependency: '+str(p))

def prepare():
    if MANIFEST.exists():
        raise RuntimeError('immutable six-target manifest already exists')
    src = sources();proof = branch_proof()
    protected, review = protection_and_source_review()
    before = inventory()
    targets = [c.pin(p) for p in candidates()]
    if len(targets)!=6 or sum(r['size_bytes'] for r in targets)!=EXPECTED_BYTES:
        raise RuntimeError('exact six-target size changed')
    disjoint(targets,protected)
    names = {r['path'] for r in targets}
    kept = [c.pin(p) for p in sorted(before['ordinary_file_identities']) if p not in names]
    if inventory()!=before:
        raise RuntimeError('old source-factor branch changed during readonly streaming audit')
    for row in src+targets+kept+protected:
        if c.identity(Path(row['path']).lstat())!=row['identity']:
            raise RuntimeError('full observed 7ID changed before manifest freeze')
    d = dict(schema='SPOT_EXACT_SIX_SUPERSEDED_EARLY_MAP_RAW_RELEASE_MANIFEST_V1',created_unix=time.time(),
        action_executed=False,target_count=6,total_target_logical_bytes=EXPECTED_BYTES,target_full_EOF_pins=targets,
        source_pins=src,completed_branch_and_stage_proof=proof,current_and_next_Source_protected_full_EOF_pins=protected,
        actual_Source_reference_review=review,retained_ordinary_file_full_EOF_pins=kept,complete_before_inventory=before,
        preparation_after_inventory_equals_before=True,original_budget_before=c.budget(),
        retention='Every other branch entry, including map003 onward, map012, bootstrap, training, all numerical/accuracy/performance records, reports/logs/source/runtime and remaining raw, retained.',
        consequence='Six superseded early-map raw inputs are lost for historical replay. This is a completed12/WAITING_REFERENCE branch, not a failed-run cleanup. Saved results and final raw stay. Current and next explicitly frozen inputs remain protected.',
        scientific_computation_started=False,numerical_thresholds_or_budgets_changed=False,goal_complete=False)
    c.write_new(MANIFEST,d)
    print(json.dumps(dict(status='EXACT_SIX_MANIFEST_PREPARED_NO_DELETE',manifest=c.pin(MANIFEST),target_count=6,
        target_bytes=EXPECTED_BYTES,retained_regular_files=len(kept),retained_symlinks=len(before['symlinks']),protected_full_EOF_pins=len(protected))))

def verify_or_execute(args):
    row = c.pin(MANIFEST)
    if row['sha256']!=args.manifest_sha256 or row['identity']!=json.loads(args.manifest_seven_id):
        raise RuntimeError('Root-selected manifest exact SHA/7ID required')
    m=c.read_pinned_json(row)
    if (m['schema']!='SPOT_EXACT_SIX_SUPERSEDED_EARLY_MAP_RAW_RELEASE_MANIFEST_V1' or m['action_executed']
        or m['target_count']!=6 or m['total_target_logical_bytes']!=EXPECTED_BYTES
        or [r['path'] for r in m['target_full_EOF_pins']]!=[str(p) for p in candidates()]
        or sum(r['size_bytes'] for r in m['target_full_EOF_pins'])!=EXPECTED_BYTES):
        raise RuntimeError('hard-coded exact-six unexecuted manifest required')
    receipt=PACKAGE/('ACTUAL_EXACT_SIX_RELEASE_EXECUTION_RECEIPT.json' if args.execute else 'ACTUAL_READONLY_EXACT_SIX_VERIFICATION_RECEIPT.json')
    if receipt.exists() or receipt.with_suffix('.pending').exists():
        raise RuntimeError('no receipt overwrite or automatic execution retry')
    if sources()!=m['source_pins'] or branch_proof()!=m['completed_branch_and_stage_proof']:
        raise RuntimeError('audit Source or preserved completed branch records changed')
    protected,review=protection_and_source_review()
    if protected!=m['current_and_next_Source_protected_full_EOF_pins'] or review!=m['actual_Source_reference_review']:
        raise RuntimeError('current/next Source protection or actual reference evidence changed')
    targets=m['target_full_EOF_pins'];kept=m['retained_ordinary_file_full_EOF_pins']
    for item in targets+kept:c.same(item)
    if inventory()!=m['complete_before_inventory']:raise RuntimeError('complete old branch inventory changed')
    disjoint(targets,protected);before=c.budget()
    r=dict(schema='SPOT_EXACT_SIX_SUPERSEDED_EARLY_MAP_RAW_ACTUAL_RECEIPT_V1',started_unix=time.time(),manifest_pin=row,
        execute_requested=args.execute,all_full_EOF_preflight_verified=True,original_budget_before=before,deletion_records=[],
        retention_records=[],status='READONLY_EXACT_SIX_VERIFIED' if not args.execute else 'EXECUTING',
        scientific_computation_started=False,budgets_or_thresholds_changed=False,goal_complete=False)
    c.write_new(receipt,r)
    if not args.execute:
        print(json.dumps(dict(status=r['status'],receipt=c.pin(receipt),deletion_executed=False)));return
    try:
        for item in targets:
            c.same(item);disjoint([item],protected);p=Path(item['path'])
            fd=os.open(p.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if c.identity(os.stat(p.name,dir_fd=fd,follow_symlinks=False))!=item['identity']:
                    raise RuntimeError('single target changed immediately before unlink')
                os.unlink(p.name,dir_fd=fd)
            finally:os.close(fd)
            if os.path.lexists(p):raise RuntimeError('target reappeared after unlink')
            r['deletion_records'].append(dict(path=item['path'],original_full_EOF_pin=item,action='UNLINK_EXACT_FROZEN_ORDINARY_FILE',confirmed_absent=True,unix=time.time()))
            c.update_owned_receipt(receipt,r)
        for item in kept:
            c.same(item);r['retention_records'].append(dict(path=item['path'],full_EOF_SHA_and_7ID_unchanged=True))
        for item in protected+m['source_pins']+[row]:c.same(item)
        expected=dict(m['complete_before_inventory']);names={x['path'] for x in targets}
        expected['ordinary_file_identities']={p:i for p,i in expected['ordinary_file_identities'].items() if p not in names}
        if inventory()!=expected:raise RuntimeError('unexpected retained branch entry change')
        after=c.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=EXPECTED_BYTES or before['regular_files']-after['regular_files']!=6:
            raise RuntimeError('history changed beyond exact six raw paths; check concurrent artifact writers')
        r.update(status='EXACT_SIX_EARLY_MAP_RELEASE_AND_RETENTION_VERIFIED',original_budget_after=after,logical_bytes_released=EXPECTED_BYTES,
            deleted_file_count=6,all_other_old_branch_entries_full_EOF_or_symlink_identity_unchanged=True,
            current_and_next_Source_dependency_closure_full_EOF_unchanged=True,completed_unix=time.time())
    except BaseException as e:
        r.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(e),completed_unix=time.time())
        c.update_owned_receipt(receipt,r);raise
    c.update_owned_receipt(receipt,r)
    print(json.dumps(dict(status=r['status'],receipt=c.pin(receipt),deleted_file_count=6,logical_bytes_released=EXPECTED_BYTES)))

def main():
    ap=argparse.ArgumentParser();actions=ap.add_mutually_exclusive_group()
    actions.add_argument('--prepare',action='store_true');actions.add_argument('--execute',action='store_true')
    ap.add_argument('--manifest-sha256');ap.add_argument('--manifest-seven-id');args=ap.parse_args()
    if args.prepare:
        if args.manifest_sha256 or args.manifest_seven_id:raise RuntimeError('prepare does not accept manifest authority arguments')
        prepare()
    else:
        if not args.manifest_sha256 or not args.manifest_seven_id:raise RuntimeError('verification/execution requires manifest SHA/7ID')
        verify_or_execute(args)

if __name__=='__main__':main()
