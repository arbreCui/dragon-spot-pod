"""Create final manifest only with Root's real selected v11HF and final SourceSF."""
import argparse
import time
import json
import single_project_release_common as s

def main():
    p=argparse.ArgumentParser()
    for role in ('source-freeze','v11-host-freeze'):
        p.add_argument('--'+role+'-sha256',required=True);p.add_argument('--'+role+'-seven-id',required=True)
    a=p.parse_args();sf=s.external(s.SF,a.source_freeze_sha256,a.source_freeze_seven_id);f=s.source_gate(sf)
    hf=s.external(s.V11_HF,a.v11_host_freeze_sha256,a.v11_host_freeze_seven_id)
    protected,dag,retained=s.current_protection(hf);s.owned_disjoint(s.TARGET_SELECTED_PIN,protected);s.writer_gate();before=s.inventory();budget=s.budget()
    value=dict(schema='ROOT_EXACT_SINGLE_OLD_V9_PROJECT_RELEASE_MANIFEST_V1',draft_only=False,action_executed=False,selected_complete_Source_freeze_pin=sf,selected_actual_v11_HF_pin=hf,selected_actual_v11_CLI_pin=s.V11_CLI_SELECTED_PIN,Source_pins=f['Source_pins'],target_full_EOF_pin=s.TARGET_SELECTED_PIN,target_count=1,target_logical_bytes=s.BYTES,current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,retained_oldv9_full_EOF_pins=retained,complete_before_inventory=before,original_budget_before_preparation=budget,compiler_or_business_executed=False,goal_complete=False,old_raw_replay_unavailable_after_future_release=True,GLOBAL_PROJECT_PASS_not_reclassified=True,created_unix=time.time())
    for row in protected+retained+f['Source_pins']+[sf,hf,s.TARGET_SELECTED_PIN]:s.same(row)
    s.writer_gate();s.write_new(s.FINAL,value)
    print(json.dumps(dict(status='ACTUAL_V11_HF_CURRENT_DAG_SINGLE_MANIFEST_PREPARED_NO_DELETION',manifest_pin=s.pin(s.FINAL),protected_count=len(protected),retained_count=242,target_bytes=s.BYTES,deletion_executed=False)))

if __name__=='__main__':main()
