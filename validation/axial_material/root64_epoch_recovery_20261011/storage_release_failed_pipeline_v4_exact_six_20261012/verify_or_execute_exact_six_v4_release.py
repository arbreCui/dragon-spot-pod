"""Default readonly. Root alone selects exact manifest and explicit --execute."""
import argparse
import json
import os
from pathlib import Path
import time
import release_v4_source_common as s
c=s.c


def business_writer_gate():
    # The current v5 directory remains protected by existence, not a frozen
    # pin of its outputs. A real completed summary is required at execution;
    # Source preparation itself never reads or freezes active v5 outputs.
    p=s.ACTIVE/'Root_actual_three_plane_engineering_summary.json'
    if not p.is_file():raise RuntimeError('active v5 not yet terminal; no deletion')
    d=c.read_pinned_json(c.pin(p))
    if d['after_check_error']is not None or not d['records']:raise RuntimeError('actual current v5 closure required')
    for r in d['records']:
        w=c.read_pinned_json(c.pin(s.ACTIVE/(r['label']+'.watchdog.json')))
        if w['command']!=r['command']or w['liveness_group_cleanup']is not True or w['own_child_only']is not True or type(w['returncode'])is not int:
            raise RuntimeError('all current v5 owning children must be truly closed')


def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True)
    p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');args=p.parse_args()
    mp=c.pin(s.MANIFEST)
    if mp['sha256']!=args.manifest_sha256 or mp['identity']!=json.loads(args.manifest_seven_id):raise RuntimeError('Root-selected exact manifest authority')
    m=c.read_pinned_json(mp)
    if m['schema']!='ROOT_REVIEWABLE_EXACT_SIX_FAILED_V4_STORAGE_SOURCE_MANIFEST_V1'or m['action_executed']is not False or m['target_count']!=6 or m['total_target_logical_bytes']!=s.BYTES or [r['path']for r in m['target_full_EOF_pins']]!=[str(p)for p in s.TARGETS]:raise RuntimeError('literal exact6 unexecuted manifest only')
    protected,dag=s.protect()
    if protected!=m['current_protected_full_EOF_pins']or dag!=m['Source_DAG_provenance']or s.closed_proof()!=m['closed_failed_branch_proof']or s.owning_provenance(m['target_full_EOF_pins'])!=m['exact_owning_provenance']:raise RuntimeError('Source/current DAG/closure or ownership changed')
    for row in m['target_full_EOF_pins']+m['retained_ordinary_full_EOF_pins']+m['Source_pins']+[mp]:c.same(row)
    if s.inventory()!=m['complete_before_inventory']:raise RuntimeError('complete old failed branch changed')
    s.disjoint(m['target_full_EOF_pins'],protected)
    if args.execute:business_writer_gate()
    before=c.budget();receipt=s.PACKAGE/('ACTUAL_EXACT_SIX_FAILED_V4_RELEASE_RECEIPT.json'if args.execute else'READONLY_EXACT_SIX_FAILED_V4_VERIFICATION_RECEIPT.json')
    if receipt.exists()or receipt.with_suffix('.pending').exists():raise RuntimeError('no receipt overwrite/no automatic retry')
    value=dict(schema='ROOT_EXACT_SIX_FAILED_V4_ACTUAL_STORAGE_RECEIPT_V1',manifest_pin=mp,
      status='EXECUTING'if args.execute else'READONLY_FULL_EOF_VERIFIED',execute_requested=args.execute,
      original_budget_before=before,started_unix=time.time(),deletion_records=[],
      compiler_or_numerical_business_started=False,goal_complete=False)
    c.write_new(receipt,value)
    if not args.execute:
        print(json.dumps(dict(status=value['status'],receipt_pin=c.pin(receipt),deletion_executed=False)));return
    try:
        for row in m['target_full_EOF_pins']:
            c.same(row);s.disjoint([row],protected);path=Path(row['path'])
            fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            try:
                if c.identity(os.stat(path.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:raise RuntimeError('target changed just before unlink')
                os.unlink(path.name,dir_fd=fd)
            finally:os.close(fd)
            if os.path.lexists(path):raise RuntimeError('target reappeared')
            value['deletion_records'].append(dict(original_fullpin=row,confirmed_absent=True));c.update_owned_receipt(receipt,value)
        for row in m['retained_ordinary_full_EOF_pins']+protected+m['Source_pins']+[mp]:c.same(row)
        afteri=s.inventory();old=m['complete_before_inventory'];removed={r['path']for r in m['target_full_EOF_pins']}
        if afteri['ordinary_file_identities']!={p:i for p,i in old['ordinary_file_identities'].items()if p not in removed}or afteri['symlinks']!=old['symlinks']or set(afteri['directory_identities'])!=set(old['directory_identities']):raise RuntimeError('unexpected retained branch change')
        for path,identity in old['directory_identities'].items():
            actual=afteri['directory_identities'][path]
            if path==str(s.BRANCH/'AAA'):
                if actual[:3]!=identity[:3]or actual[3]!=identity[3]-6 or actual[4]!=identity[4]-6*32:raise RuntimeError('APFS natural6 ordinary entry changes only')
            elif actual!=identity:raise RuntimeError('untouched old directory metadata changed')
        after=c.budget()
        if before['artifact_bytes']-after['artifact_bytes']!=s.BYTES or before['regular_files']-after['regular_files']!=6:raise RuntimeError('artifact writer or non-exact logical budget delta; no automatic retry')
        value.update(status='EXACT_SIX_FAILED_V4_RELEASE_AND_ALL_RETENTION_VERIFIED',
          deleted_files=6,logical_bytes_released=s.BYTES,original_budget_after=after,
          all_other_reports_logs_Source_original_inputs_v3PACK_retained=True,completed_unix=time.time())
    except BaseException as error:
        value.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(error));c.update_owned_receipt(receipt,value);raise
    c.update_owned_receipt(receipt,value)
    print(json.dumps(dict(status=value['status'],receipt_pin=c.pin(receipt),deleted_files=6,logical_bytes_released=s.BYTES)))


if __name__=='__main__':main()
