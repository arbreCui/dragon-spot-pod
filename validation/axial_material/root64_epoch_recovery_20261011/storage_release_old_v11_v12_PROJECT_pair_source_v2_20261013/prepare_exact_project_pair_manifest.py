"""Prepare only after Root authorizes actual candidate reads and real v14 pins."""
import argparse
import json
import time
import project_pair_release_common as s

def main():
    parser=argparse.ArgumentParser()
    roles=('source-freeze','v14-host-freeze','v14-cli','root-source-review','root-source-tools','independent-source-review','independent-source-tools')
    for role in roles:
        for name in('summary','sha256','seven-id'):parser.add_argument('--'+role+'-'+name,required=True)
    args=parser.parse_args();selected={}
    for role in roles:
        prefix=role.replace('-','_');selected[role]=s.external(getattr(args,prefix+'_summary'),getattr(args,prefix+'_sha256'),getattr(args,prefix+'_seven_id'))
    sf=selected['source-freeze'];f=s.source_gate(sf);hf=selected['v14-host-freeze'];cli=selected['v14-cli']
    reviews=[(who,selected[who+'-source-review'],selected[who+'-source-tools'])for who in('root','independent')]
    protected,dag,retained,inventory=s.current_protection(sf,hf,cli,reviews);s.disjoint(protected);proofs=s.closed_proofs();s.writer_gate(hf,protected);budget=s.budget()
    value=dict(schema='ROOT_EXACT_OLD_V11_V12_PRIVATE_PROJECT_PAIR_RELEASE_MANIFEST_V1',draft_only=False,action_executed=False,selected_complete_Source_freeze_pin=sf,selected_actual_v14_HF_pin=hf,selected_actual_v14_CLI_pin=cli,selected_actual_v14_Source_reviews=reviews,Source_pins=f['Source_pins'],target_full_EOF_pins=s.TARGET_SELECTED_PINS,target_count=2,target_logical_bytes=s.BYTES,current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,retained_other_oldv11_v12_full_EOF_pins=retained,complete_before_inventory=inventory,all_old_actual_closed_failure_proofs=proofs,original_budget_before_preparation=budget,compiler_or_business_executed=False,goal_complete=False,exact_old_raw_replay_unavailable_after_future_release=True,GLOBAL_PROJECT_PASS_not_reclassified=True,created_unix=time.time())
    for row in protected+f['Source_pins']+[sf,hf,cli]+s.TARGET_SELECTED_PINS:s.same(row)
    if s.inventory()!=inventory:raise RuntimeError('old branch changed before manifest publication')
    s.writer_gate(hf,protected);s.write_new(s.FINAL,value)
    print(json.dumps(dict(status='ACTUAL_V14_HF_CLI_AND_TWO_SOURCE_TOOL0_REVIEWS_EXACT_PAIR_MANIFEST_PREPARED_NO_DELETION',manifest_pin=s.pin(s.FINAL),protected_count=len(protected),retained_other_old_branch_count=len(retained),target_bytes=s.BYTES,deletion_executed=False)))

if __name__=='__main__':main()
