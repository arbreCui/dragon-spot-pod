"""Default read-only verification. --execute removes only the frozen 24 paths."""
import argparse
import json
import os
from pathlib import Path
import time
import storage_release_common as c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-sha256', required=True)
    ap.add_argument('--manifest-seven-id', required=True)
    ap.add_argument('--execute', action='store_true')
    args = ap.parse_args()
    manifest = c.PACKAGE / 'EXACT_24_FAILED_RAW_RELEASE_MANIFEST.json'
    mrow = c.pin(manifest)
    if mrow['sha256'] != args.manifest_sha256 or mrow['identity'] != json.loads(args.manifest_seven_id):
        raise RuntimeError('external Root-selected manifest SHA and exact 7ID required')
    m = c.read_pinned_json(mrow)
    if m['schema'] != 'SPOT_EXACT_24_CLOSED_FAILED_RAW_RELEASE_MANIFEST_V1' or m['action_executed']:
        raise RuntimeError('exact unexecuted release manifest required')
    targets = m['target_full_EOF_pins']
    if ([r['path'] for r in targets] != [str(p) for p in c.candidates()]
            or len(targets) != 24 or sum(r['size_bytes'] for r in targets) != c.EXPECTED_BYTES
            or m['total_target_logical_bytes'] != c.EXPECTED_BYTES):
        raise RuntimeError('exact hard-coded 24 path and byte list required')
    receipt = c.PACKAGE / ('ACTUAL_EXACT_RELEASE_EXECUTION_RECEIPT.json' if args.execute else 'ACTUAL_READONLY_RELEASE_VERIFICATION_RECEIPT.json')
    if receipt.exists() or receipt.with_suffix('.pending').exists():
        raise RuntimeError('no execution retry or receipt overwrite')
    for row in m['source_pins']:
        c.same(row)
    if str(Path(__file__)) not in {r['path'] for r in m['source_pins']}:
        raise RuntimeError('current executor Source not bound')
    if c.failure_documents() != m['closed_failure_proofs']:
        raise RuntimeError('actual closed failure proofs changed')
    protected, coverage = c.current_protection()
    if protected != m['current_mandatory_protected_full_EOF_pins'] or coverage != m['protection_coverage']:
        raise RuntimeError('current immediate mandatory dependency closure changed')
    for row in targets + m['retained_ordinary_file_full_EOF_pins']:
        c.same(row)
    if c.inventory() != m['complete_before_inventory']:
        raise RuntimeError('exact retained file, symlink and directory inventory changed')
    c.protected_disjoint(targets, protected)
    before = c.budget()
    r = dict(schema='SPOT_EXACT_FAILED_RAW_RELEASE_ACTUAL_RECEIPT_V1', started_unix=time.time(),
        manifest_pin=mrow, execute_requested=args.execute, preflight_complete=True,
        all_target_retained_and_protected_full_EOF_pins_verified=True,
        exact_inventory_before_verified=True, original_budget_before=before,
        deletion_records=[], retention_records=[], status='READONLY_VERIFIED' if not args.execute else 'EXECUTING',
        scientific_calculation_started=False, budgets_or_thresholds_changed=False, goal_complete=False)
    c.write_new(receipt, r)
    if not args.execute:
        print(json.dumps(dict(status=r['status'], receipt=c.pin(receipt), target_count=24,
                              target_bytes=c.EXPECTED_BYTES, deletion_executed=False)))
        return
    try:
        for row in targets:
            c.guard()
            # Repeat full file and parent checks immediately before this one unlink.
            c.same(row)
            c.protected_disjoint([row], protected)
            p = Path(row['path'])
            parent_fd = os.open(p.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                s = os.stat(p.name, dir_fd=parent_fd, follow_symlinks=False)
                if c.identity(s) != row['identity']:
                    raise RuntimeError('target identity changed immediately before unlink')
                os.unlink(p.name, dir_fd=parent_fd)
            finally:
                os.close(parent_fd)
            if os.path.lexists(p):
                raise RuntimeError('unlinked target path reappeared')
            r['deletion_records'].append(dict(path=row['path'], original_full_EOF_pin=row,
                action='UNLINK_EXACT_FROZEN_ORDINARY_FILE', confirmed_absent=True, unix=time.time()))
            c.update_owned_receipt(receipt, r)
        for row in m['retained_ordinary_file_full_EOF_pins']:
            c.same(row)
            r['retention_records'].append(dict(path=row['path'], full_EOF_SHA_and_7ID_unchanged=True))
        for row in protected + m['source_pins'] + [mrow]:
            c.same(row)
        after_inventory = c.inventory()
        expected = dict(m['complete_before_inventory'])
        expected['ordinary_file_identities'] = {p:i for p,i in expected['ordinary_file_identities'].items()
                                                if p not in {x['path'] for x in targets}}
        if after_inventory != expected:
            raise RuntimeError('unexpected retained inventory change after exact release')
        after = c.budget()
        if before['artifact_bytes'] - after['artifact_bytes'] != c.EXPECTED_BYTES:
            raise RuntimeError('complete history logical byte reduction differs from exact target sum')
        if before['regular_files'] - after['regular_files'] != 24:
            raise RuntimeError('complete history ordinary file count reduction differs from 24')
        if not after['original_initial_reserve_admitted']:
            raise RuntimeError('original cold/metadata/fresh initial reserve still not admitted')
        r.update(status='EXACT_24_RELEASE_AND_RETENTION_VERIFIED', original_budget_after=after,
            logical_bytes_released=c.EXPECTED_BYTES, deleted_file_count=24,
            all_other_group_entries_full_EOF_or_symlink_identity_unchanged=True,
            current_mandatory_dependency_closure_full_EOF_unchanged=True,
            after_inventory_equals_before_minus_exact_targets=True, completed_unix=time.time())
    except BaseException as e:
        r.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY', error=repr(e), completed_unix=time.time())
        c.update_owned_receipt(receipt, r)
        raise
    c.update_owned_receipt(receipt, r)
    print(json.dumps(dict(status=r['status'], receipt=c.pin(receipt), deleted_file_count=24,
                          logical_bytes_released=c.EXPECTED_BYTES,
                          original_initial_reserve_admitted=True)))

if __name__ == '__main__':
    main()
