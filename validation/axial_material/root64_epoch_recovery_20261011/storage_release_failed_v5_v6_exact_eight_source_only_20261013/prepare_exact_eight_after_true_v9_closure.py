"""Root alone selects future true v9 receipt/summary. Creates manifest after closure."""
import argparse
import time
import exact_eight_release_common as s

def main():
    p=argparse.ArgumentParser()
    for role in ('source-freeze','v9-tool-receipt','v9-summary'):
        p.add_argument('--'+role+'-sha256',required=True);p.add_argument('--'+role+'-seven-id',required=True)
    a=p.parse_args()
    sf=s.external(s.SF,a.source_freeze_sha256,a.source_freeze_seven_id);freeze=s.Source_gate(sf)
    tp=s.external(s.V9_TRUE_TOOL,a.v9_tool_receipt_sha256,a.v9_tool_receipt_seven_id)
    sp=s.external(s.V9_SUMMARY,a.v9_summary_sha256,a.v9_summary_seven_id)
    protected,dag=s.protection(tp,sp);proofs,targets=s.closed_old_proofs();s.disjoint(targets,protected)
    inventory=s.inventory();retained=[s.pin(path) for path in sorted(inventory['ordinary_file_identities']) if path not in {r['path'] for r in targets}]
    s.writer_gate(tp,sp)
    value=dict(schema='ROOT_EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_RELEASE_MANIFEST_V1',action_executed=False,compiler_or_numerical_business_executed=False,goal_complete=False,
      selected_complete_Source_only_freeze_pin=sf,Source_pins=freeze['Source_pins'],selected_actual_v9_true_tool_receipt_pin=tp,selected_actual_v9_summary_pin=sp,
      target_count=8,total_target_logical_bytes=s.BYTES,target_full_EOF_pins=targets,current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,
      closed_failed_overall_v5_v6_run_proofs=proofs,retained_ordinary_full_EOF_pins=retained,complete_before_inventory=inventory,original_budget_before_preparation=s.budget(),
      created_unix=time.time(),all_result_logs_Source_other_outputs_retained=True,individual_PACK_INITIAL_PASS_preserved=True,
      old_failed_global_causal_raws_preserved=True,only_old_private_replay_paths_unavailable_after_future_release=True,no_success_receipt_prefilled=True,
      original_physical_inputs_producers_caps_math_and_thresholds_unchanged=True)
    for row in protected+retained+targets+freeze['Source_pins']+[sf,tp,sp]:s.same(row)
    s.write_new(s.MANIFEST,value)
    print(__import__('json').dumps(dict(status='TRUE_V9_CLOSED_FUTURE_EXACT_EIGHT_MANIFEST_PREPARED_NO_DELETION',manifest_pin=s.pin(s.MANIFEST),target_count=8,total_candidate_logical_bytes=s.BYTES,protected_count=len(protected),deletion_executed=False)))

if __name__=='__main__':main()
