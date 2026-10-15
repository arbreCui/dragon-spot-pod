"""Readonly default, exact one literal target only, no overwrite or retry."""
import argparse
import os
import json
import time
import single_project_release_common as s

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    mp=s.external(s.FINAL,a.manifest_sha256,a.manifest_seven_id);m=s.read(mp)
    if m['schema']!='ROOT_EXACT_SINGLE_OLD_V9_PROJECT_RELEASE_MANIFEST_V1' or m['draft_only'] is not False or m['action_executed'] is not False or m['target_count']!=1 or m['target_logical_bytes']!=s.BYTES or m['target_full_EOF_pin']!=s.TARGET_SELECTED_PIN or m['selected_actual_v11_CLI_pin']!=s.V11_CLI_SELECTED_PIN:raise RuntimeError('strict real final exact1 manifest, never draft')
    sf=m['selected_complete_Source_freeze_pin'];f=s.source_gate(sf);hf=m['selected_actual_v11_HF_pin']
    protected,dag,retained=s.current_protection(hf)
    if protected!=m['current_protected_full_EOF_pins'] or dag!=m['Source_DAG_provenance'] or retained!=m['retained_oldv9_full_EOF_pins'] or f['Source_pins']!=m['Source_pins'] or s.inventory()!=m['complete_before_inventory']:raise RuntimeError('real current dependency/Source/retained entry change')
    s.owned_disjoint(s.TARGET_SELECTED_PIN,protected);s.writer_gate();before=s.budget()
    receipt=s.PKG/('ACTUAL_SINGLE_OLD_V9_PROJECT_RELEASE_RECEIPT.json' if a.execute else 'READONLY_SINGLE_OLD_V9_PROJECT_VERIFICATION_RECEIPT.json')
    if os.path.lexists(receipt) or os.path.lexists(receipt.with_suffix('.pending')):raise RuntimeError('no receipt overwrite or automatic deletion retry')
    value=dict(schema='ACTUAL_SINGLE_OLD_V9_PRIVATE_PROJECT_RELEASE_RECEIPT_V1',status='EXECUTING_NO_DELETION_YET' if a.execute else 'READONLY_EXACT_SINGLE_CURRENT_DAG_VERIFIED',manifest_pin=mp,execute_requested=a.execute,original_budget_before=before,deletion_records=[],compiler_or_business_executed=False,goal_complete=False,started_unix=time.time())
    s.write_new(receipt,value);rp=s.pin(receipt)
    if not a.execute:print(json.dumps(dict(status=value['status'],receipt_pin=rp,deletion_executed=False)));return
    try:
        row=s.TARGET_SELECTED_PIN;s.owned_disjoint(row,protected);fd=os.open(s.TARGET.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            if s.identity(os.fstat(fd))!=m['complete_before_inventory']['directory_identities'][str(s.TARGET.parent)]:raise RuntimeError('original parent directory changed at exact unlink open')
            if s.identity(os.stat(s.TARGET.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:raise RuntimeError('target changed immediately before exact one unlink')
            os.unlink(s.TARGET.name,dir_fd=fd)
        finally:os.close(fd)
        if os.path.lexists(s.TARGET):raise RuntimeError('released oldv9 raw reappeared')
        value['deletion_records'].append(dict(original_fullpin=row,confirmed_absent=True));rp=s.update_owned(receipt,value,rp)
        for p in protected+retained+f['Source_pins']+[sf,hf,mp]:s.same(p)
        old=m['complete_before_inventory'];new=s.inventory()
        if new['ordinary_file_identities']!={p:i for p,i in old['ordinary_file_identities'].items() if p!=str(s.TARGET)} or new['symlinks']!=old['symlinks'] or set(new['directory_identities'])!=set(old['directory_identities']):raise RuntimeError('unexpected oldv9 entry/file difference beyond one')
        directory_changes=[]
        for path,before_dir in old['directory_identities'].items():
            after_dir=new['directory_identities'][path]
            if path==str(s.TARGET.parent):
                if after_dir[:3]!=before_dir[:3] or after_dir[3]<1 or after_dir[5]<before_dir[5] or after_dir[6]<before_dir[6]:raise RuntimeError('parent stable owner/inode/mode changed')
                directory_changes.append(dict(path=path,before_seven_id=before_dir,after_seven_id=after_dir,ordinary_entry_delta=-1,all_other_file_link_entries_exact=True,nlink_delta=after_dir[3]-before_dir[3],directory_size_delta=after_dir[4]-before_dir[4],interpretation='REAL_NATIVE_PARENT_METADATA_NO_ASSUMED_APFS_NLINK_RULE'))
            elif after_dir!=before_dir:raise RuntimeError('unaffected directory all7ID changed')
        s.writer_gate();after=s.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=1:raise RuntimeError('nonexact true logical one-file release delta/concurrent ART writer')
        value.update(status='EXACT_SINGLE_OLD_V9_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',deleted_files=1,logical_bytes_released=s.BYTES,original_budget_after=after,observed_parent_directory_changes=directory_changes,all242_other_oldv9_files_and_all_current_science_Source_inputs_retained=True,GLOBAL_PROJECT_individual_PASS_preserved=True,only_old_v9_full_PROJECT_GLOBAL_raw_replay_unavailable=True,original_physics_math_producers_thresholds_caps_unchanged=True,completed_unix=time.time())
    except BaseException as e:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(e));s.update_owned(receipt,value,rp);raise
    rp=s.update_owned(receipt,value,rp);s.guard();print(json.dumps(dict(status=value['status'],receipt_pin=rp,deleted_files=1,logical_bytes_released=s.BYTES,original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))

if __name__=='__main__':main()
