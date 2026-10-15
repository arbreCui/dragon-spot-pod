#!/usr/bin/env python3
"""Exclusive Source-only final freeze after exact independently closed0 role review."""
import argparse
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat

REC=Path(__file__).resolve().parent
HERE=REC/'post_curated66_current_catalog_common_source_v2_20261013'
PREPARER=REC/'prepare_post_curated66_current_catalog_common_source_v2_20261013.py'
PREP_TOOL=REC/'ACTUAL_POST_CURATED66_CATALOG_COMMON_V2_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261013.json'

def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in ('path','sha256','size_bytes','identity')}
def pin(path):
 p=Path(path);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);parts=[]
 try:
  assert ids(os.fstat(fd))==ids(s)
  while True:
   b=os.read(fd,1048576)
   if not b:break
   parts.append(b)
  assert ids(os.fstat(fd))==ids(s)
 finally:os.close(fd)
 raw=b''.join(parts);assert len(raw)==s.st_size and ids(p.lstat())==ids(s)
 return raw,dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=ids(s))
def read(p):
 raw,pf=pin(p);return json.loads(raw),pf
def same(row):assert norm(pin(row['path'])[1])==norm(row)
def put(name,value):
 raw=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode();p=HERE/name
 fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
 try:assert os.write(fd,raw)==len(raw);os.fsync(fd)
 finally:os.close(fd)
 actual,pf=pin(p);assert actual==raw and pf['identity'][3]==1
 return pf
def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--peer-review-json',required=True);ap.add_argument('--peer-review-sha256',required=True)
 ap.add_argument('--peer-review-seven-id',required=True);ap.add_argument('--peer-true-tool-json',required=True)
 a=ap.parse_args();peer,peerpf=read(a.peer_review_json);true,toolpf=read(a.peer_true_tool_json)
 assert peerpf['sha256']==a.peer_review_sha256 and peerpf['identity']==json.loads(a.peer_review_seven_id)
 assert peer['status']=='PASS_POST_CURATED66_CATALOG_BINDING_COMMON_SOURCE_ONLY'and peer['failure']is None
 actual=true['actual_review_return'];assert isinstance(actual,dict)and actual['exit_code']==0 and not actual.get('session_id')
 line=next(x for x in reversed(actual['output'].splitlines())if x.strip().startswith('{'))
 assert norm(json.loads(line)['review_pin'])==peerpf
 ready,readypf=read(HERE/'POST_CURATED66_CATALOG_COMMON_SOURCE_REVIEW_READY.json')
 assert ready['source_only']is True and ready['compiler_executed']is False and ready['numerical_executed']is False and ready['Host_imported']is False
 for key,pfkey in [('actual_common_source_pin','new_Common_Source_pin'),('actual_catalog_pin','new_catalog_pin'),('actual_binding_pin','new_binding_pin')]:
  assert norm(peer[key])==ready[pfkey]
 assert norm(peer['actual_source_review_ready_pin'])==readypf
 for row in ready['files']+ready['original_source_metadata_pins']:same(row)
 prep,preptoolpf=read(PREP_TOOL);terminal=prep['actual_v2']['actual_terminal_tool_return']
 assert terminal['exit_code']==0 and not terminal.get('session_id')
 prepared=json.loads(next(x for x in reversed(terminal['output'].splitlines())if x.strip().startswith('{')))
 assert prepared['source_review_ready_pin']==readypf and prepared['compiler_executed']is False and prepared['numerical_executed']is False
 assert prep['failed_v1']['actual_terminal_tool_return']['exit_code']==1
 inv,invpf=read(ready['complete_byte_data_inverse_pin']['path']);oldcat,_=read(inv['original_catalog_pin']['path'])
 cat,_=read(ready['new_catalog_pin']['path']);back=copy.deepcopy(cat);back.pop('post_release_role_reconciliation')
 assert len(cat['rows'])==3030 and len(cat['historical_non_live_declarations'])==inv['original_historical_declaration_count']+10
 back['historical_non_live_declarations']=back['historical_non_live_declarations'][:-10]
 for item in inv['exact_removed_original_rows']:back['rows'].insert(item['original_catalog_index'],item['original_row'])
 assert back==oldcat and all('current_pin'not in x for x in cat['historical_non_live_declarations'])
 oldbind,_=read(inv['original_binding_pin']['path']);bind,_=read(ready['new_binding_pin']['path']);back=copy.deepcopy(bind)
 assert inv['exact_binding_replacement_index']==2006 and len(bind['fixed_current_pins'])==2012
 back['current_mount_full_identity_catalog_pin']=inv['original_catalog_pin'];back['fixed_current_pins'][2006]=inv['original_catalog_pin']
 assert back==oldbind and bind['current_mount_full_identity_catalog_pin']==ready['new_catalog_pin']==bind['fixed_current_pins'][2006]
 common,commonpf=pin(ready['new_Common_Source_pin']['path']);oldcommon,_=pin(inv['original_Common_pin']['path'])
 back=common.decode()
 for splice in reversed(inv['Common_literal_splices']):
  assert back.count(splice['after'])==1;back=back.replace(splice['after'],splice['before'],1)
 assert back.encode()==oldcommon;ast.parse(common)
 eof,eofpf=read(ready['retained_fullEOF_all7_report_pin']['path'])
 assert eof['status']=='PASS_RETAINED3030_ROWS_UNIQUE2979_CURRENT_COMPLETE_EOF_ALL7'and eof['row_count']==3030 and eof['unique_file_count']==2979
 table={row['path']:row for row in eof['actual_full_EOF_pins']};assert len(table)==2979
 assert eof['all_file_descriptors_closed']is True and eof['SELF_peak_bytes']<512*2**20 and 0<eof['wall_seconds']<1800
 for row in cat['rows']:
  assert table[row['current_pin']['path']]==row['current_pin']and ids(Path(row['current_pin']['path']).lstat())==row['current_pin']['identity']
 # Full EOF was actually performed by the closed Source preparer; no fake new scientific re-read claim.
 ownpreparer=pin(PREPARER)[1];ownfreezer=pin(__file__)[1]
 files=ready['files']+[readypf,ownpreparer,ownfreezer,preptoolpf,peerpf,toolpf]
 assert len({x['path']for x in files})==len(files)
 freeze=dict(schema='COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_ONLY_FREEZE_V1',
  source_only=True,compiled=False,compiler_executed=False,numerical_executed=False,business_executed=False,
  Host_imported=False,deletion_executed=False,files=files,original_source_metadata_pins=ready['original_source_metadata_pins'],
  new_Common_Source_pin=ready['new_Common_Source_pin'],new_catalog_pin=ready['new_catalog_pin'],new_binding_pin=ready['new_binding_pin'],
  complete_byte_data_inverse_pin=invpf,retained_fullEOF_all7_report_pin=eofpf,
  actual_source_preparation_true_tool_return_pin=preptoolpf,actual_independent_source_role_review_pin=peerpf,
  actual_independent_source_role_true_tool_return_pin=toolpf,
  actual_release_receipt_pin=ready['actual_release_receipt_pin'],actual_release_true_tool_return_pin=ready['actual_release_true_tool_return_pin'],
  actual_independent_postrelease_review_pin=ready['actual_independent_postrelease_review_pin'],
  actual_independent_postrelease_true_tool_return_pin=ready['actual_independent_postrelease_true_tool_return_pin'],
  exact_retired_row_count=10,retained_catalog_row_count=3030,retained_current_unique_paths=2979,
  old_catalog_top_non_rows_statistics_are_predecessor_historical_attestation=True,
  new_current_accounting_key='post_release_role_reconciliation',all_other_3030_rows_order_and_data_unchanged=True,
  original2012_binding_only_catalogPF_two_references_replaced_at_index2006=True,
  Common_only_two_BASE_BIND_literal_changes=True,all_original_guard_math_serializer_method_bytes_unchanged=True,
  no_generic_missing_pin_skip=True,no_top_level_current_pin_in_historical_declarations=True,
  future_actual_build_object_pin=None,future_actual_build_report_pin=None,future_actual_control_report_pin=None,
  compiler_qualified=False,reader_qualified=False,AAA_qualified=False,ABA_admitted=False)
 for row in files+ready['original_source_metadata_pins']:same(row)
 sf=put('COMPLETE_POST_CURATED66_CURRENT_CATALOG_BINDING_COMMON_SOURCE_FREEZE.json',freeze)
 print(json.dumps({'status':'SOURCE_ONLY_POST_CURATED66_CATALOG_BINDING_COMMON_FROZEN_UNIMPORTED_UNQUALIFIED','source_freeze_pin':sf,
  'new_Common_Source_pin':commonpf,'new_catalog_pin':ready['new_catalog_pin'],'new_binding_pin':ready['new_binding_pin'],
  'actual_independent_source_role_review_pin':peerpf,'compiler_executed':False,'numerical_executed':False,'business_executed':False,'deletion_executed':False}))
if __name__=='__main__':main()
