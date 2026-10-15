"""Root exact-list cleanup proposal; default readonly. No implicit execution."""
import argparse,json,os
from pathlib import Path
import time
import release_source_common as s
c=s.c

def main():
 p=argparse.ArgumentParser();p.add_argument('--batch',choices=list(s.BATCHES),required=True);p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);p.add_argument('--execute',action='store_true');args=p.parse_args()
 b=s.BATCHES[args.batch];mp=c.pin(s.PACKAGE/b['manifest'])
 if mp['sha256']!=args.manifest_sha256 or mp['identity']!=json.loads(args.manifest_seven_id):raise RuntimeError('Root explicit complete selected manifest')
 m=c.read_pinned_json(mp)
 if m['batch']!=args.batch or m['action_executed']is not False or m['target_count']!=b['count']or m['total_target_logical_bytes']!=b['bytes']or [r['path']for r in m['target_full_EOF_pins']]!=[str(p)for p in b['targets']]:raise RuntimeError('literal independent finite target batch only')
 protected,pr=s.protect()
 if protected!=m['current_protected_full_EOF_pins']or pr!=m['Source_DAG_provenance']or s.proof(args.batch)!=m['closed_branch_proof']:raise RuntimeError('current/proposed Source DAG or actual closure changed')
 for r in m['target_full_EOF_pins']+m['retained_ordinary_full_EOF_pins']+m['Source_pins']+[mp]:c.same(r)
 if s.inventory(b['branch'])!=m['complete_before_inventory']:raise RuntimeError('complete closed branch inventory changed')
 s.disjoint(m['target_full_EOF_pins'],protected);before=c.budget()
 receipt=s.PACKAGE/(args.batch+('_ACTUAL_RELEASE_RECEIPT.json'if args.execute else'_READONLY_VERIFICATION_RECEIPT.json'))
 if receipt.exists()or receipt.with_suffix('.pending').exists():raise RuntimeError('no receipt overwrite or automatic retry')
 r=dict(schema='ROOT_SELECTED_INDEPENDENT_EXACT_STORAGE_BATCH_ACTUAL_V1',manifest_pin=mp,batch=args.batch,status='EXECUTING'if args.execute else'READONLY_FULL_EOF_VERIFIED',execute_requested=args.execute,original_budget_before=before,started_unix=time.time(),deletion_records=[],scientific_or_numerical_business_started=False,goal_complete=False)
 c.write_new(receipt,r)
 if not args.execute:print(json.dumps(dict(status=r['status'],receipt_pin=c.pin(receipt),deletion_executed=False)));return
 try:
  for row in m['target_full_EOF_pins']:
   c.same(row);s.disjoint([row],protected);path=Path(row['path']);fd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
   try:
    if c.identity(os.stat(path.name,dir_fd=fd,follow_symlinks=False))!=row['identity']:raise RuntimeError('single target changed immediately before unlink')
    os.unlink(path.name,dir_fd=fd)
   finally:os.close(fd)
   if os.path.lexists(path):raise RuntimeError('released target reappeared')
   r['deletion_records'].append(dict(original_full_pin=row,confirmed_absent=True));c.update_owned_receipt(receipt,r)
  for row in m['retained_ordinary_full_EOF_pins']+protected+m['Source_pins']+[mp]:c.same(row)
  afteri=s.inventory(b['branch']);old=m['complete_before_inventory'];removed={r['path']for r in m['target_full_EOF_pins']}
  if afteri['ordinary_file_identities']!={p:i for p,i in old['ordinary_file_identities'].items()if p not in removed}or afteri['symlinks']!=old['symlinks']or set(afteri['directory_identities'])!=set(old['directory_identities']):raise RuntimeError('unexpected retained branch entry change')
  counts={}
  for row in m['target_full_EOF_pins']:
   parent=str(Path(row['path']).parent);counts[parent]=counts.get(parent,0)+1
  for path,identity in old['directory_identities'].items():
   observed=afteri['directory_identities'][path]
   if path in counts:
    n=counts[path]
    if observed[:3]!=identity[:3]or observed[3]!=identity[3]-n or observed[4]!=identity[4]-32*n:raise RuntimeError('APFS parent directory must change only natural entry nlink/size/timestamps')
   elif observed!=identity:raise RuntimeError('untouched directory metadata changed')
  after=c.budget()
  if before['artifact_bytes']-after['artifact_bytes']!=b['bytes']or before['regular_files']-after['regular_files']!=b['count']:raise RuntimeError('history delta differs from exact finite files; no concurrent artifact writer permitted')
  r.update(status='EXACT_SELECTED_BATCH_RELEASE_AND_RETENTION_VERIFIED',deleted_files=b['count'],logical_bytes_released=b['bytes'],original_budget_after=after,all_other_raw_results_logs_Source_producers_retained=True,parent_APFS_nlink_size_natural_entry_changes_verified=True,completed_unix=time.time())
 except BaseException as error:
  r.update(status='STOPPED_PARTIAL_OR_POSTCHECK_FAILURE_NO_AUTOMATIC_RETRY',error=repr(error));c.update_owned_receipt(receipt,r);raise
 c.update_owned_receipt(receipt,r);print(json.dumps(dict(status=r['status'],receipt_pin=c.pin(receipt),deleted_files=b['count'],logical_bytes_released=b['bytes'])))
if __name__=='__main__':main()
