"""Readonly default; no retry. Root external manifest all7ID required for execute."""
import argparse
import json
import os
from pathlib import Path
import time
import exact_eight_release_common as s

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    mp=s.external(s.MANIFEST,a.manifest_sha256,a.manifest_seven_id);m=s.read(mp)
    if m['schema']!='ROOT_EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_RELEASE_MANIFEST_V1' or m['action_executed'] is not False or m['target_count']!=8 or m['total_target_logical_bytes']!=s.BYTES:raise RuntimeError('exact unexecuted eight manifest')
    sf=m['selected_complete_Source_only_freeze_pin'];freeze=s.Source_gate(sf)
    tp=m['selected_actual_v9_true_tool_receipt_pin'];sp=m['selected_actual_v9_summary_pin']
    protected,dag=s.protection(tp,sp);proofs,targets=s.closed_old_proofs()
    if protected!=m['current_protected_full_EOF_pins'] or dag!=m['Source_DAG_provenance'] or proofs!=m['closed_failed_overall_v5_v6_run_proofs'] or targets!=m['target_full_EOF_pins'] or freeze['Source_pins']!=m['Source_pins']:raise RuntimeError('current complete protected union or exact old closure changed')
    for row in targets+m['retained_ordinary_full_EOF_pins']+m['Source_pins']+[sf,mp]:s.same(row)
    if s.inventory()!=m['complete_before_inventory']:raise RuntimeError('old branch complete inventory changed')
    s.disjoint(targets,protected);s.writer_gate(tp,sp);before=s.budget()
    path=s.PKG/('ACTUAL_EXACT_EIGHT_RELEASE_RECEIPT.json' if a.execute else 'READONLY_EXACT_EIGHT_VERIFICATION_RECEIPT.json')
    if os.path.lexists(path) or os.path.lexists(path.with_suffix('.pending')):raise RuntimeError('no receipt overwrite or automatic deletion retry')
    value=dict(schema='ACTUAL_EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_RELEASE_RECEIPT_V1',status='EXECUTING_NO_DELETION_YET' if a.execute else 'READONLY_ALL_FULL_EOF_VERIFIED',manifest_pin=mp,execute_requested=a.execute,started_unix=time.time(),deletion_records=[],original_budget_before=before,compiler_or_numerical_business_executed=False,goal_complete=False)
    s.write_new(path,value);rp=s.pin(path)
    if not a.execute:print(json.dumps(dict(status=value['status'],receipt_pin=rp,deletion_executed=False)));return
    try:
        for row in targets:
            s.owned_disjoint(row,protected)
            candidate=Path(row['path']);fd=os.open(candidate.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if s.identity(os.stat(candidate.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:raise RuntimeError('candidate changed immediately before exact unlink')
                os.unlink(candidate.name,dir_fd=fd)
            finally:os.close(fd)
            if os.path.lexists(candidate):raise RuntimeError('released candidate reappeared')
            value['deletion_records'].append(dict(original_fullpin=row,confirmed_absent=True));rp=s.update_owned(path,value,rp)
        for row in m['retained_ordinary_full_EOF_pins']+protected+m['Source_pins']+[sf,mp]:s.same(row)
        old=m['complete_before_inventory'];new=s.inventory();removed={r['path'] for r in targets}
        if new['ordinary_file_identities']!={p:i for p,i in old['ordinary_file_identities'].items() if p not in removed} or new['symlinks']!=old['symlinks'] or set(new['directory_identities'])!=set(old['directory_identities']):raise RuntimeError('unexpected entry/file change beyond exact eight')
        parents={str(p.parent) for p in s.TARGETS};changes=[]
        for p,before_dir in old['directory_identities'].items():
            after_dir=new['directory_identities'][p]
            if p in parents:
                if after_dir[:3]!=before_dir[:3] or after_dir[3]<1 or after_dir[5]<before_dir[5] or after_dir[6]<before_dir[6]:raise RuntimeError('affected native directory stable owner/inode/mode changed')
                changes.append(dict(path=p,before_seven_id=before_dir,after_seven_id=after_dir,ordinary_entry_delta=-4,all_other_file_link_entries_exact=True,nlink_delta=after_dir[3]-before_dir[3],directory_size_delta=after_dir[4]-before_dir[4],interpretation='OBSERVED_NATIVE_DIRECTORY_METADATA_NO_ASSUMED_APFS_NLINK_RULE'))
            elif after_dir!=before_dir:raise RuntimeError('unaffected directory all7ID changed')
        s.writer_gate(tp,sp);after=s.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=8:raise RuntimeError('nonexact logical history release delta or concurrent artifact writer')
        value.update(status='EXACT_EIGHT_PRIVATE_COPY_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',deleted_files=8,logical_bytes_released=s.BYTES,original_budget_after=after,observed_parent_directory_changes=changes,all_other_result_logs_Source_current_science_and_v9_outputs_retained=True,individual_PACK_INITIAL_PASS_preserved=True,old_private_v5_v6_raw_replay_unavailable=True,original_physics_producers_inputs_caps_math_thresholds_unchanged=True,completed_unix=time.time())
    except BaseException as e:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(e));s.update_owned(path,value,rp);raise
    rp=s.update_owned(path,value,rp);s.guard()
    print(json.dumps(dict(status=value['status'],receipt_pin=rp,deleted_files=8,logical_bytes_released=s.BYTES,original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))

if __name__=='__main__':main()
