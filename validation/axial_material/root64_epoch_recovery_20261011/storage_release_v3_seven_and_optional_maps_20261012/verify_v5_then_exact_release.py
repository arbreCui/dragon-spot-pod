"""Root selected exact cleanup; add immutable current v5 protection in-process.
Default remains readonly. No numerical child, compiler, retry or threshold change.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
import time
import release_source_common as s
c=s.c

def no_target_overlap(targets,protected):
 paths={p['path']for p in protected};inodes={tuple(p['identity'][:2])for p in protected}
 for p in targets:
  if p['path']in paths or tuple(p['identity'][:2])in inodes:raise RuntimeError('exact target intersects additional current v5 Source/input')

def main():
 parser=argparse.ArgumentParser(add_help=False)
 parser.add_argument('--additional-v5-proof-sha256',required=True)
 parser.add_argument('--additional-v5-proof-seven-id',required=True)
 args,original_arguments=parser.parse_known_args()
 pp=c.pin(s.PACKAGE/'ADDITIONAL_CURRENT_V5_SOURCE_DAG_DISJOINT_PROOF.json')
 if pp['sha256']!=args.additional_v5_proof_sha256 or pp['identity']!=json.loads(args.additional_v5_proof_seven_id):raise RuntimeError('Root exact additional v5 proof full pin required')
 proof=c.read_pinned_json(pp)
 if proof['schema']!='ADDITIONAL_CURRENT_V5_FINITE_SOURCE_DAG_EXACT_RELEASE_PROOF_V1' or proof['deletion_executed']is not False:raise RuntimeError('exact readonly additional Source proof')
 bp=argparse.ArgumentParser(add_help=False);bp.add_argument('--batch',choices=list(s.BATCHES),required=True);batch,_=bp.parse_known_args(original_arguments)
 expected=next(p for p in proof['two_unchanged_manifest_pins']if p['path']==str(s.PACKAGE/s.BATCHES[batch.batch]['manifest']))
 c.same(expected);manifest=c.read_pinned_json(expected)
 if proof['current_pipeline5_freeze_pin']['sha256']!='09950ab3e9ac8d626d30d9020639b4653e5a391164355316f9f8c33f5c87025c':raise RuntimeError('exact current frozen pipeline5')
 sources=proof['additional_v5_current_full_EOF_pins']+proof['guard_wrapper_and_unchanged_original_Source_pins']+[pp]
 for p in sources:c.same(p)
 no_target_overlap(manifest['target_full_EOF_pins'],proof['additional_v5_current_full_EOF_pins'])
 receipt=s.PACKAGE/(batch.batch+('_V5_GUARD_ACTUAL_RECEIPT.json'if '--execute'in original_arguments else'_V5_GUARD_READONLY_RECEIPT.json'))
 if receipt.exists():raise RuntimeError('no guard receipt overwrite or automatic retry')
 r=dict(schema='SAMEPROCESS_CURRENT_V5_EXACT_RELEASE_GUARD_V1',proof_pin=pp,selected_manifest_pin=expected,own_Source_pin=proof['guard_wrapper_and_unchanged_original_Source_pins'][0],batch=batch.batch,original_arguments=original_arguments,status='V5_BEFORE_COMPLETE',before_full_EOF_verified=True,before_full_EOF_count=len(sources),numerical_or_compiler_child_started=False,started_unix=time.time())
 c.write_new(receipt,r)
 try:
  spec=importlib.util.spec_from_file_location('unchanged_exact_cleanup_executor',s.PACKAGE/'verify_or_execute_exact_release.py');executor=importlib.util.module_from_spec(spec);spec.loader.exec_module(executor)
  old_argv=sys.argv;sys.argv=[str(s.PACKAGE/'verify_or_execute_exact_release.py')]+original_arguments
  try:executor.main()
  finally:sys.argv=old_argv
  r['original_executor_completed']=True
 except BaseException as error:
  r.update(status='ORIGINAL_EXACT_EXECUTOR_FAILED_NO_RETRY',original_executor_error=repr(error));raise
 finally:
  try:
   for p in sources:c.same(p)
   c.same(expected)
   r.update(after_full_EOF_verified=True,after_full_EOF_count=len(sources),completed_unix=time.time())
   if r.get('original_executor_completed')is True:r['status']='V5_GUARD_BEFORE_AND_AFTER_COMPLETE_ORIGINAL_EXACT_EXECUTOR_COMPLETED'
  except BaseException as error:
   r.update(status='V5_POSTGUARD_FAILED_NO_RETRY',after_error=repr(error));raise
  finally:c.update_owned_receipt(receipt,r)
 print(json.dumps(dict(status=r['status'],v5_guard_receipt_pin=c.pin(receipt))))
if __name__=='__main__':main()
