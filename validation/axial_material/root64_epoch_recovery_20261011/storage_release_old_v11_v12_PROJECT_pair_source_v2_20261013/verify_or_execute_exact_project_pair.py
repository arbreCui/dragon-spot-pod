"""Readonly default; exact two literal candidates, no overwrite or retry."""
import argparse
import json
import os
import time
import project_pair_release_common as s

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    mp=s.external(s.FINAL,a.manifest_sha256,a.manifest_seven_id);m=s.read(mp)
    if m['schema']!='ROOT_EXACT_OLD_V11_V12_PRIVATE_PROJECT_PAIR_RELEASE_MANIFEST_V1'or m['draft_only']is not False or m['action_executed']is not False or m['target_count']!=2 or m['target_logical_bytes']!=s.BYTES or m['target_full_EOF_pins']!=s.TARGET_SELECTED_PINS:raise RuntimeError('exact real pair manifest, never draft')
    sf=m['selected_complete_Source_freeze_pin'];f=s.source_gate(sf);hf=m['selected_actual_v14_HF_pin'];cli=m['selected_actual_v14_CLI_pin'];reviews=m['selected_actual_v14_Source_reviews']
    protected,dag,retained,inventory=s.current_protection(sf,hf,cli,reviews)
    if protected!=m['current_protected_full_EOF_pins']or dag!=m['Source_DAG_provenance']or retained!=m['retained_other_oldv11_v12_full_EOF_pins']or inventory!=m['complete_before_inventory']or f['Source_pins']!=m['Source_pins']or s.closed_proofs()!=m['all_old_actual_closed_failure_proofs']:raise RuntimeError('exact actual current Source/DAG/retained inventory and old closure unchanged')
    s.disjoint(protected);s.writer_gate(hf,protected);before=s.budget();s.RECEIPTS.mkdir(exist_ok=True)
    if s.RECEIPTS.is_symlink()or s.RECEIPTS.lstat().st_uid!=os.getuid():raise RuntimeError('ordinary owned receipt namespace')
    receipt=s.RECEIPTS/('ACTUAL_EXACT_OLD_V11_V12_PROJECT_PAIR_RELEASE_RECEIPT.json'if a.execute else'READONLY_EXACT_OLD_V11_V12_PROJECT_PAIR_VERIFICATION_RECEIPT.json')
    if os.path.lexists(receipt)or os.path.lexists(receipt.with_suffix('.pending')):raise RuntimeError('no receipt overwrite or automatic release retry')
    value=dict(schema='ACTUAL_EXACT_OLD_V11_V12_PRIVATE_PROJECT_PAIR_RELEASE_RECEIPT_V1',status='EXECUTING_NO_DELETION_YET'if a.execute else'READONLY_EXACT_PAIR_CURRENT_FINAL_V14_DAG_VERIFIED',manifest_pin=mp,execute_requested=a.execute,original_budget_before=before,deletion_records=[],compiler_or_business_executed=False,goal_complete=False,started_unix=time.time())
    s.write_new(receipt,value);rp=s.pin(receipt)
    if not a.execute:print(json.dumps(dict(status=value['status'],receipt_pin=rp,deletion_executed=False)));return
    try:
        for target,row in zip(s.TARGETS,s.TARGET_SELECTED_PINS):
            s.same(row);s.writer_gate(hf,protected);fd=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if s.identity(os.fstat(fd))!=inventory['directory_identities'][str(target.parent)]:raise RuntimeError('exact candidate parent directory all7 at open')
                if s.identity(os.stat(target.name,dir_fd=fd,follow_symlinks=False))!=row['identity']or os.stat(target.name,dir_fd=fd,follow_symlinks=False).st_uid!=os.getuid():raise RuntimeError('exact current target all7/UID immediately before unlink')
                os.unlink(target.name,dir_fd=fd)
                value['deletion_records'].append(dict(original_fullpin=row,actual_unlink_returned=True,confirmed_absent=not os.path.lexists(target)));rp=s.update_owned(receipt,value,rp)
            finally:os.close(fd)
            if os.path.lexists(target):raise RuntimeError('released old PROJECT reappeared')
        for row in protected+f['Source_pins']+[sf,hf,cli,mp]:s.same(row)
        new=s.inventory();targets={str(p)for p in s.TARGETS}
        if new['ordinary_file_identities']!={p:i for p,i in inventory['ordinary_file_identities'].items()if p not in targets}or new['symlinks']!=inventory['symlinks']or set(new['directory_identities'])!=set(inventory['directory_identities']):raise RuntimeError('entry difference beyond exact two candidates')
        changes=[];parents={str(p.parent)for p in s.TARGETS}
        for path,old in inventory['directory_identities'].items():
            after=new['directory_identities'][path]
            if path in parents:
                if after[:3]!=old[:3]or after[3]!=old[3]-1 or after[4]!=old[4]-32 or after[5]<old[5]or after[6]<old[6]:raise RuntimeError('exact APFS candidate parent one-entry change')
                changes.append(dict(path=path,before_seven_id=old,after_seven_id=after,nlink_delta=-1,size_delta=-32))
            elif after!=old:raise RuntimeError('unaffected directory all7 changed')
        if s.inventory([s.V13_OUT])!=dag['current_v13_complete_before_inventory']:raise RuntimeError('actual v13 299 outputs or directories changed')
        s.writer_gate(hf,protected);after=s.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=2:raise RuntimeError('nonexact original axial-family logical byte/file delta')
        if after['original_initial_reserve_admitted']is not True:raise RuntimeError('full original fresh/cold/meta next-run reserve insufficient')
        value.update(status='EXACT_OLD_V11_V12_PROJECT_PAIR_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',deleted_files=2,logical_bytes_released=s.BYTES,original_budget_after=after,observed_two_parent_directory_changes=changes,all_other_old_branch_and_v13_299_result_log_curve_Source_science_files_retained=True,GLOBAL_PROJECT_individual_PASS_preserved=True,only_old_PROJECT_GLOBAL_and_exact_finite_fixture_raw_replay_unavailable=True,original_physics_math_producers_thresholds_caps_unchanged=True,completed_unix=time.time())
        rp=s.update_owned(receipt,value,rp);s.guard()
    except BaseException as error:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',first_error=repr(error))
        try:s.update_owned(receipt,value,rp)
        except BaseException as later:print(json.dumps(dict(primary_error=repr(error),receipt_publication_error=repr(later),actual_deleted_records=value['deletion_records'])),flush=True)
        raise
    print(json.dumps(dict(status=value['status'],receipt_pin=rp,deleted_files=2,logical_bytes_released=s.BYTES,original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))

if __name__=='__main__':main()
