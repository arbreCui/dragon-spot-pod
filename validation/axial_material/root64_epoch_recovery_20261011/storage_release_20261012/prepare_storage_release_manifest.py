"""Prepare reviewable evidence only; never delete files or launch calculations."""
import json
from pathlib import Path
import time
import storage_release_common as c

def main():
    manifest = c.PACKAGE / 'EXACT_24_FAILED_RAW_RELEASE_MANIFEST.json'
    if manifest.exists():
        raise RuntimeError('immutable candidate manifest already exists')
    source_paths = [Path(__file__), c.PACKAGE / 'storage_release_common.py', c.PACKAGE / 'execute_exact_storage_release.py']
    sources = [c.pin(p) for p in source_paths]
    failures = c.failure_documents()
    protected, coverage = c.current_protection()
    before = c.inventory()
    target_paths = c.candidates()
    targets = [c.pin(p) for p in target_paths]
    if sum(r['size_bytes'] for r in targets) != c.EXPECTED_BYTES:
        raise RuntimeError('exact declared release byte sum changed')
    c.protected_disjoint(targets, protected)
    target_names = {str(p) for p in target_paths}
    retained = [c.pin(p) for p in sorted(before['ordinary_file_identities']) if p not in target_names]
    after = c.inventory()
    if before != after:
        raise RuntimeError('six old attempt directories changed during complete streaming audit')
    for row in targets + retained + protected + sources:
        if c.identity(Path(row['path']).lstat()) != row['identity']:
            raise RuntimeError('file identity changed during candidate preparation')
    snapshot = c.budget()
    d = dict(schema='SPOT_EXACT_24_CLOSED_FAILED_RAW_RELEASE_MANIFEST_V1',
        created_unix=time.time(), action_executed=False, target_count=24,
        total_target_logical_bytes=c.EXPECTED_BYTES, target_full_EOF_pins=targets,
        source_pins=sources, closed_failure_proofs=failures,
        current_mandatory_protected_full_EOF_pins=protected, protection_coverage=coverage,
        retained_ordinary_file_full_EOF_pins=retained, retained_symlinks=before['symlinks'],
        retained_directories=before['directories'], complete_before_inventory=before,
        candidate_preparation_after_inventory_equals_before=True,
        original_budget_observation_before=snapshot,
        expected_budget_after_logical_bytes=snapshot['artifact_bytes']-c.EXPECTED_BYTES,
        retention='Every other entry in the six old directories remains, including reports, logs, source, objects, libraries, controls and all remaining raw files.',
        consequence='The selected old failed attempts lose these raw stage replay inputs; saved failure, stage and numerical records remain. Successful science maps and baselines are outside the exact list.',
        no_scientific_calculation_started=True, physical_inputs_changed=False,
        numerical_thresholds_changed=False, budgets_changed=False, goal_complete=False)
    c.write_new(manifest, d)
    print(json.dumps(dict(manifest=c.pin(manifest), target_count=24,
        target_bytes=c.EXPECTED_BYTES, retained_regular_files=len(retained),
        retained_symlinks=len(before['symlinks']), protection_coverage=coverage,
        deletion_executed=False), ensure_ascii=False))

if __name__ == '__main__':
    main()

