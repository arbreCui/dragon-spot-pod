"""Readonly by default. Root explicitly executes exact two literal private raws only."""
import argparse
import json
import os
from pathlib import Path
import time
import project_pair_release_common as s

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    mp=s.pin(s.MANIFEST)
    if mp['sha256']!=a.manifest_sha256 or mp['identity']!=json.loads(a.manifest_seven_id):raise RuntimeError('externally selected exact manifest SHA/all7ID required')
    m=s.read(mp)
    if m['schema']!='ROOT_REVIEWABLE_EXACT_TWO_CLOSED_FAILED_RUN_PROJECT_COPY_RELEASE_SOURCE_MANIFEST_V1' or m['action_executed'] is not False or m['target_count']!=2 or m['total_target_logical_bytes']!=s.BYTES:raise RuntimeError('exact unexecuted two-target Source manifest required')
    protected,dag=s.protection()
    if protected!=m['current_protected_full_EOF_pins'] or dag!=m['Source_DAG_provenance'] or s.closed_proofs(m['target_full_EOF_pins'])!=m['closed_failed_overall_run_proofs']:raise RuntimeError('current reachable DAG or true failed overall closures changed')
    for row in m['target_full_EOF_pins']+m['retained_ordinary_full_EOF_pins']+m['Source_pins']+[mp]:s.same(row)
    if s.inventory()!=m['complete_before_inventory']:raise RuntimeError('closed branch complete before inventory changed')
    s.disjoint(m['target_full_EOF_pins'],protected);s.writer_gate();before=s.budget()
    receipt=s.PKG/('ACTUAL_EXACT_TWO_PROJECT_PRIVATE_COPY_RELEASE_RECEIPT.json' if a.execute else 'READONLY_EXACT_TWO_PROJECT_PRIVATE_COPY_VERIFICATION_RECEIPT.json')
    if receipt.exists() or receipt.with_suffix('.pending').exists():raise RuntimeError('no automatic deletion retry/receipt overwrite')
    value=dict(schema='ACTUAL_EXACT_TWO_CLOSED_FAILED_RUN_PRIVATE_PROJECT_RELEASE_RECEIPT_V1',status='EXECUTING_NO_DELETION_YET' if a.execute else 'READONLY_FULL_EOF_VERIFIED',manifest_pin=mp,execute_requested=a.execute,started_unix=time.time(),deletion_records=[],original_budget_before=before,compiler_or_numerical_business_executed=False,goal_complete=False)
    s.write_new(receipt,value);rp=s.pin(receipt)
    if not a.execute:print(json.dumps(dict(status=value['status'],receipt_pin=rp,deletion_executed=False)));return
    try:
        for row in m['target_full_EOF_pins']:
            s.owned_disjoint(row,protected);path=Path(row['path']);fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if s.identity(os.stat(path.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:raise RuntimeError('exact target changed just before unlink')
                os.unlink(path.name,dir_fd=fd)
            finally:os.close(fd)
            if os.path.lexists(path):raise RuntimeError('released target reappeared')
            value['deletion_records'].append(dict(original_fullpin=row,confirmed_absent=True));rp=s.update_owned(receipt,value,rp)
        for row in m['retained_ordinary_full_EOF_pins']+protected+m['Source_pins']+[mp]:s.same(row)
        old=m['complete_before_inventory'];new=s.inventory();removed={r['path'] for r in m['target_full_EOF_pins']}
        if new['ordinary_file_identities']!={p:i for p,i in old['ordinary_file_identities'].items() if p not in removed} or new['symlinks']!=old['symlinks'] or set(new['directory_identities'])!=set(old['directory_identities']):raise RuntimeError('unexpected additional retained branch entry/file change')
        parents={str(p.parent) for p in s.TARGETS};directory_changes=[]
        for p,b in old['directory_identities'].items():
            after=new['directory_identities'][p]
            if p in parents:
                if after[:3]!=b[:3] or after[3]<1 or after[5]<b[5] or after[6]<b[6]:raise RuntimeError('affected directory changed beyond stable owner inode/mode')
                directory_changes.append(dict(path=p,before_seven_id=b,after_seven_id=after,ordinary_entry_delta=-1,exact_other_file_and_link_inventory_unchanged=True,nlink_delta=after[3]-b[3],directory_size_delta=after[4]-b[4],interpretation='OBSERVED_NATIVE_FILESYSTEM_DIRECTORY_METADATA_AFTER_EXACT_ONE_UNLINK_NO_ASSUMED_PARENT_NLINK_RULE'))
            elif after!=b:raise RuntimeError('unaffected directory metadata changed')
        after=s.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=2:raise RuntimeError('non-exact logical ART release delta or concurrent artifact writer')
        value.update(status='EXACT_TWO_PRIVATE_PROJECT_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',deleted_files=2,logical_bytes_released=s.BYTES,original_budget_after=after,observed_parent_directory_changes=directory_changes,all_other_result_documents_logs_Source_current_inputs_retained=True,individual_GLOBAL_and_PROJECT_PASS_preserved=True,old_v7_v8_private_PROJECT_raw_replay_unavailable=True,original_physics_producers_inputs_caps_math_and_thresholds_unchanged=True,completed_unix=time.time())
        s.guard()
    except BaseException as e:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(e));rp=s.update_owned(receipt,value,rp);raise
    rp=s.update_owned(receipt,value,rp);s.guard()
    print(json.dumps(dict(status=value['status'],receipt_pin=rp,deleted_files=2,logical_bytes_released=s.BYTES,original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))

if __name__=='__main__':main()
