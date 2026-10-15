"""Readonly default, literal --execute only, no retry; sequential same-dirfd unlink3."""
import argparse,json,os,time,sys
from pathlib import Path
import literal11_release_common as s

def main():
    p=argparse.ArgumentParser(allow_abbrev=False);p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    if sys.argv[1:].count('--execute')!=(1 if a.execute else 0):raise RuntimeError('execution requires exactly one literal --execute token')
    mp=s.external(s.FINAL,a.manifest_sha256,a.manifest_seven_id);m=s.read(mp)
    if m['schema']!='ROOT_EXACT_LITERAL_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_MANIFEST_V1'or m['draft_only']is not False or m['action_executed']is not False or m['target_count']!=3 or m['target_logical_bytes']!=s.BYTES or m['target_full_EOF_pins']!=s.TARGET_SELECTED_PINS:raise RuntimeError('exact actual66 manifest only')
    sf=m['selected_Source_freeze_pin'];f=s.source_gate(sf);reviews=m['selected_literal11_Source_reviews'];protected,dag,retained,inventory=s.current_protection(sf,reviews)
    if protected!=m['current_protected_full_EOF_pins']or dag!=m['Source_DAG_provenance']or retained!=m['retained_all_other_v15_files_full_EOF_pins']or inventory!=m['complete_before_inventory']or s.closed_proofs()!=m['actual_closed_failed_v14_v15_v16_owner_proofs']or f['Source_pins']!=m['Source_pins']:raise RuntimeError('unchanged full current Source/DAG/owner/inventory proof')
    s.disjoint(protected);s.writer_gate(protected);before=s.budget();s.RECEIPTS.mkdir(exist_ok=True);s.b.ancestors(s.RECEIPTS)
    if s.RECEIPTS.is_symlink()or s.RECEIPTS.lstat().st_uid!=os.getuid():raise RuntimeError('owned ordinary receipt directory')
    rp_path=s.RECEIPTS/('ACTUAL_EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_RECEIPT.json'if a.execute else'READONLY_EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_VERIFICATION_RECEIPT.json')
    if os.path.lexists(rp_path)or os.path.lexists(rp_path.with_suffix('.pending')):raise RuntimeError('no receipt overwrite or automatic retry')
    value=dict(schema='ACTUAL_EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_RECEIPT_V1',status='EXECUTING_NO_DELETION_YET'if a.execute else'READONLY_LITERAL2_ALL_CURRENT_EOF_VERIFIED',manifest_pin=mp,execute_requested=a.execute,original_budget_before=before,deletion_records=[],next_target_intent=None,compiler_or_business_executed=False,started_unix=time.time())
    s.write_new(rp_path,value);rp=s.receipt_pin(rp_path)
    if not a.execute:print(json.dumps(dict(status=value['status'],receipt_pin=rp,deletion_executed=False)));return
    expected=dict(inventory['directory_identities']);counts={};changes=[]
    try:
        for target,row in zip(s.TARGETS,s.TARGET_SELECTED_PINS):
            s.same(row);s.writer_gate(protected);s.b.ancestors(target)
            value['next_target_intent']=dict(fullpin=row,fsynced_before_unlink=True,unlink_return_not_yet_observed=True);rp=s.update_owned(rp_path,value,rp)
            fd=os.open(target.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            first_fd_error=None;first_fd_tb=None
            try:
                previous=expected[str(target.parent)]
                if s.identity(os.fstat(fd))!=previous or s.identity(target.parent.lstat())!=previous:raise RuntimeError('exact current parent sameFD all7 immediately before unlink')
                actual=os.stat(target.name,dir_fd=fd,follow_symlinks=False)
                if s.identity(actual)!=row['identity']or actual.st_uid!=os.getuid()or actual.st_nlink!=1:raise RuntimeError('literal whitelist current UID/nlink/all7 immediately before unlink')
                os.unlink(target.name,dir_fd=fd)
                # Record actual syscall first; later failures retain this exact partial action.
                value['deletion_records'].append(dict(original_fullpin=row,actual_unlink_returned=True));value['next_target_intent']=None;rp=s.update_owned(rp_path,value,rp)
                value['deletion_records'][-1]['target_directory_fsync_attempted']=True;rp=s.update_owned(rp_path,value,rp)
                os.fsync(fd)
                value['deletion_records'][-1]['target_directory_fsync_returned']=True;rp=s.update_owned(rp_path,value,rp)
                now=s.identity(os.fstat(fd))
                if now!=s.identity(target.parent.lstat())or now[:3]!=previous[:3]or now[3]!=previous[3]-1 or now[4]!=previous[4]-32 or now[5]<previous[5]or now[6]<previous[6]:raise RuntimeError('same-device APFS exact one-entry delta')
                if os.path.lexists(target):raise RuntimeError('released literal private target reappeared')
                expected[str(target.parent)]=now;counts[str(target.parent)]=counts.get(str(target.parent),0)+1
                value['deletion_records'][-1].update(confirmed_absent=True,parent_before_seven_id=previous,parent_after_seven_id=now);rp=s.update_owned(rp_path,value,rp)
            except BaseException as error:
                first_fd_error=error;first_fd_tb=error.__traceback__;raise
            finally:
                try:os.close(fd)
                except BaseException:
                    if first_fd_error is not None:raise first_fd_error.with_traceback(first_fd_tb)
                    raise
        for r in protected+f['Source_pins']+[sf,mp]:s.same(r)
        new=s.inventory()
        if new['ordinary_file_identities']!={p:i for p,i in inventory['ordinary_file_identities'].items()if p not in s.TARGET_PATHS}or new['symlinks']!=inventory['symlinks']or set(new['directory_identities'])!=set(inventory['directory_identities']):raise RuntimeError('v15 difference beyond exact3')
        for path,old in inventory['directory_identities'].items():
            now=new['directory_identities'][path]
            if path in counts:
                n=counts[path]
                if now!=expected[path]or now[:3]!=old[:3]or now[3]!=old[3]-n or now[4]!=old[4]-32*n or now[5]<old[5]or now[6]<old[6]:raise RuntimeError('exact affected parent aggregate delta')
                changes.append(dict(path=path,before=old,after=now,removed_children=n,nlink_delta=-n,size_delta=-32*n))
            elif now!=old:raise RuntimeError('unaffected directory all7 changed')
        if s.inventory([s.V12_OUT])!=dag['current_v12_complete_inventory']:raise RuntimeError('allv12 inventory changed')
        s.writer_gate(protected);after=s.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=3 or after['original_initial_reserve_admitted']is not True:raise RuntimeError('exact original family5 bytes/file delta and full original reserve')
        value.update(status='EXACT_LITERAL3_BEFORE_SAVED370_OLD_PACK_AND_MACRO_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',deleted_files=3,logical_bytes_released=s.BYTES,original_budget_after=after,affected_parent_changes=changes,all_other_v15_science_and_current_success_failed_public_outputs_retained=True,only_old_private_exact_path_replay_lost=True,completed_unix=time.time());rp=s.update_owned(rp_path,value,rp);s.guard()
    except BaseException as error:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',first_error=repr(error))
        try:s.update_owned(rp_path,value,rp)
        except BaseException as later:print(json.dumps(dict(primary_error=repr(error),receipt_publication_error=repr(later),actual_deletion_records=value['deletion_records'],pending_intent=value['next_target_intent'])),flush=True)
        raise
    print(json.dumps(dict(status=value['status'],receipt_pin=rp,deleted_files=3,logical_bytes_released=s.BYTES,original_initial_reserve_admitted=after['original_initial_reserve_admitted'])))
if __name__=='__main__':main()
