"""Prepare exact6 failed-v4 raw only. No unlink, compiler or science child."""
import ast
import json
from pathlib import Path
import time
import release_v4_source_common as s
c=s.c


def main():
    if s.MANIFEST.exists():raise RuntimeError('no immutable manifest overwrite')
    for p in s.PACKAGE.glob('*.py'):ast.parse(p.read_bytes())
    sources=[c.pin(p)for p in sorted(s.PACKAGE.glob('*.py'))]+[c.pin(s.LIBRARY)]
    protected,dag=s.protect();proof=s.closed_proof();before=s.inventory()
    targets=[c.pin(p)for p in s.TARGETS]
    if len(targets)!=6 or sum(p['size_bytes']for p in targets)!=s.BYTES:raise RuntimeError('exact six current raw bytes')
    s.disjoint(targets,protected);ownership=s.owning_provenance(targets)
    names={p['path']for p in targets}
    retained=[c.pin(p)for p in sorted(before['ordinary_file_identities'])if p not in names]
    if s.inventory()!=before:raise RuntimeError('closed failed branch changed during fullEOF preparation')
    for row in targets+retained+protected+sources:c.same(row)
    manifest=dict(schema='ROOT_REVIEWABLE_EXACT_SIX_FAILED_V4_STORAGE_SOURCE_MANIFEST_V1',
      prepared_unix=time.time(),action_executed=False,unlink_executed=False,target_count=6,
      total_target_logical_bytes=s.BYTES,target_full_EOF_pins=targets,
      retained_ordinary_full_EOF_pins=retained,complete_before_inventory=before,
      current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,
      Source_pins=sources,closed_failed_branch_proof=proof,exact_owning_provenance=ownership,
      original_budget_at_readonly_preparation=c.budget(),
      execution_must_wait_all_ART_business_writers_closed=True,
      mutable_progress_and_active_v5_not_immutably_pinned=True,
      retained_every_report_log_deck_Source_runtime_negative_reason=True,
      invalid_v3_PACK_remains_exact_protected_causal_input=True,
      three_native_input_copies_already_released_not_counted_again=True,
      exact_negative_filename='negative_pack.xsm',not_existing_alias='negative_source32.xsm',
      original_SELF512_whole1800_history96_free8_cold_and_initialfresh2_unchanged=True,
      physical_block_release_not_inferred_from_logical_size=True,
      historical_replay_loss='Only these six exact old owned raw files if Root later explicitly executes. All closed failures/results/Source retained; v3 invalid PACK remains.',
      compiler_or_numerical_or_delete_child_started=False,physics_qualification_created=False,goal_complete=False)
    c.write_new(s.MANIFEST,manifest)
    print(json.dumps(dict(status='EXACT_SIX_FAILED_V4_SOURCE_MANIFEST_PREPARED_NO_DELETE',
      manifest_pin=c.pin(s.MANIFEST),target_count=6,target_logical_bytes=s.BYTES,
      retained_files=len(retained),protected_full_EOF_files=len(protected),delete_executed=False)))


if __name__=='__main__':main()
