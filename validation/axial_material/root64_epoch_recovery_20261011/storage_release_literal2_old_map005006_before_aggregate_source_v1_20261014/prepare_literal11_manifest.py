"""Manifest preparation only; Root supplies genuine current Source0 reviews."""
import argparse,json,time
import literal11_release_common as s

def main():
    p=argparse.ArgumentParser(allow_abbrev=False);roles=('source-freeze','root-source-review','root-source-tools','independent-source-review','independent-source-tools')
    for role in roles:
        for n in('summary','sha256','seven-id'):p.add_argument('--'+role+'-'+n,required=True)
    a=p.parse_args();chosen={}
    for role in roles:
        q=role.replace('-','_');chosen[role]=s.external(getattr(a,q+'_summary'),getattr(a,q+'_sha256'),getattr(a,q+'_seven_id'))
    sf=chosen['source-freeze'];f=s.source_gate(sf);reviews=[(who,chosen[who+'-source-review'],chosen[who+'-source-tools'])for who in('root','independent')]
    protected,dag,retained,before=s.current_protection(sf,reviews);s.disjoint(protected);owners=s.closed_proofs();s.writer_gate(protected);budget=s.budget()
    m=dict(schema='ROOT_EXACT_LITERAL_LITERAL2_OLD_MAP005006_BEFORE_AGGREGATE_OLD_PRIVATE_RELEASE_MANIFEST_V1',draft_only=False,action_executed=False,selected_Source_freeze_pin=sf,selected_literal11_Source_reviews=reviews,Source_pins=f['Source_pins'],target_full_EOF_pins=s.TARGET_SELECTED_PINS,target_count=2,target_logical_bytes=s.BYTES,current_protected_full_EOF_pins=protected,Source_DAG_provenance=dag,retained_all_other_v15_files_full_EOF_pins=retained,complete_before_inventory=before,actual_closed_failed_v14_v15_v16_owner_proofs=owners,original_budget_before_preparation=budget,compiler_or_business_executed=False,all_other_v15_science_and_current_success_failed_outputs_retained=True,exact_old_private_path_replay_unavailable_after_future_release=True,created_unix=time.time())
    for r in protected+f['Source_pins']+[sf]+s.TARGET_SELECTED_PINS:s.same(r)
    if s.inventory()!=before:raise RuntimeError('v15 inventory changed before MF publication')
    s.writer_gate(protected);s.write_new(s.FINAL,m)
    print(json.dumps(dict(status='ACTUAL_LITERAL2_MANIFEST_PREPARED_CURRENT_EOF_NO_DELETION',manifest_pin=s.pin(s.FINAL),protected_count=len(protected),retained_other_count=len(retained),target_bytes=s.BYTES,deletion_executed=False)))
if __name__=='__main__':main()
