#!/usr/bin/env python3
"""Exact post-release metadata-role reconciliation; never compiles/runs/deletes."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import time

REC=Path(__file__).resolve().parent
OUT=REC/'post_curated66_current_catalog_common_source_v2_20261013'
OLD_BIND=REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'
OLD_COMMON=REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/guarded_warm_A_common.py'
RECEIPT=REC/'storage_release_curated66_old_private_copies_actual_receipts_20261013/ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT.json'
RELEASE_TOOL=REC/'ROOT_CURATED66_V3_ACTUAL_RELEASE_TRUE_TOOL_RETURNS_20261013.json'
POST=REC/'independent_curated66_actual_postrelease_review_20261013/REVIEW.json'
POST_TOOL=POST.parent/'TRUE_TOOL_RETURNS.json'
REFUSAL=REC/'ROOT_ACTUAL_COMPACT_BQ_BUILD_V3_PRECOMPILE_CATALOG_REFUSAL_TRUE_TOOL_RETURN_20261013.json'
EXACT_INDICES=[1833,1834,1835,1872,1873,1946,1947,1948,2035,2036]


def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def norm(p):return{k:p[k]for k in ('path','sha256','size_bytes','identity')}


def pin(path,metadata=False):
    p=Path(path);s=p.lstat();assert stat.S_ISREG(s.st_mode)and not p.is_symlink()
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();count=0;pieces=[]
    try:
        assert ids(os.fstat(fd))==ids(s)
        while True:
            data=os.read(fd,1048576)
            if not data:break
            h.update(data);count+=len(data)
            if metadata:pieces.append(data)
        assert count==s.st_size and ids(os.fstat(fd))==ids(s)
    finally:os.close(fd)
    assert ids(p.lstat())==ids(s)
    return b''.join(pieces)if metadata else None,dict(path=str(p),sha256=h.hexdigest(),size_bytes=count,identity=ids(s))


def read(path):
    raw,pf=pin(path,True);return json.loads(raw),pf,raw


def put(name,value):
    p=OUT/name;raw=value if isinstance(value,bytes)else (json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode()
    fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    try:assert os.write(fd,raw)==len(raw);os.fsync(fd)
    finally:os.close(fd)
    actual,pf=pin(p,True);assert actual==raw and pf['identity'][3]==1;return pf


def main():
    start=time.monotonic()
    binding,bindingpf,bindraw=read(OLD_BIND)
    oldcatpf=binding['current_mount_full_identity_catalog_pin'];catalog,actualcatpf,catraw=read(oldcatpf['path'])
    assert actualcatpf==oldcatpf and len(catalog['rows'])==3040 and len(binding['fixed_current_pins'])==2012
    assert oldcatpf['sha256']=='77d7e680863e87bcff590cfab4be023a306ca6b7981eb00290440ff8e24e1ab2'
    receipt,receiptpf,_=read(RECEIPT);release_tool,releasetoolpf,_=read(RELEASE_TOOL)
    post,postpf,_=read(POST);post_tool,posttoolpf,_=read(POST_TOOL)
    assert receiptpf['sha256']=='114d2fd0f13c1af1396823cbba0c4b693130361092ed83ad4ecb6ca2849aadda'
    assert postpf['sha256']=='ab1fcf77e4668111c4f596cde66e36fe5433500daeec535a4bddd6652ccdb62e'
    assert receipt['status']=='EXACT_CURATED66_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED'
    assert receipt['execute_requested']is True and receipt['deleted_files']==66 and receipt['next_target_intent']is None
    assert receipt['compiler_or_business_executed']is False
    terminal=release_tool['actual_terminal_tool_return'];assert terminal['exit_code']==0 and not terminal.get('session_id')
    assert post['status']=='PASS_ACTUAL_EXACT66_POSTRELEASE_READONLY'and post['failure']is None and post['actual_target_absent_count']==66
    assert post['actual_release_receipt_pin']==receiptpf and post['all_file_descriptors_closed']is True
    post_actual=post_tool['actual_review_return'];assert isinstance(post_actual,dict)and post_actual['exit_code']==0 and not post_actual.get('session_id')
    post_stdout=post_actual['output'];last=next(line for line in reversed(post_stdout.splitlines())if line.strip().startswith('{'))
    assert norm(json.loads(last)['review_pin'])==postpf
    manifest,mfpf,_=read(receipt['manifest_pin']['path']);assert mfpf==receipt['manifest_pin']==post['manifest_pin']
    assert manifest['target_count']==66 and manifest['target_full_EOF_pins']==[x['original_fullpin']for x in receipt['deletion_records']]
    released={x['original_fullpin']['path']:x for x in receipt['deletion_records']}
    assert len(released)==66
    for row in released.values():
        assert row['actual_unlink_returned']is True and row['confirmed_absent']is True
        p=Path(row['original_fullpin']['path']);assert not p.exists()and not p.is_symlink()
    fixedpaths={row['path']for row in binding['fixed_current_pins']}
    retired=[];remaining=[]
    for index,row in enumerate(catalog['rows']):
        p=row['current_pin']['path']
        if p in released:
            assert row['current_pin']==released[p]['original_fullpin']and row['mandatory']is False
            assert p not in fixedpaths and index in EXACT_INDICES
            version='v3'if'/20261012-v3/'in p else None
            if version is None:version='v3'if'-20261012-v3/'in p else'v4'if'-20261012-v4/'in p else None
            assert version in ('v3','v4')
            prefix='recursive_full_PF_from_current_JSON:/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+version+'/'
            allowed={prefix+n for n in ['Root_actual_complete_execution_record_before_final_publication.json',
                'Root_actual_three_plane_engineering_summary.json','Root_actual_private_release_008.json']}
            assert row['roles']and set(row['roles'])<=allowed
            retired.append(dict(original_catalog_index=index,original_row=copy.deepcopy(row),actual_release_record=copy.deepcopy(released[p])))
        else:remaining.append(copy.deepcopy(row))
    assert [x['original_catalog_index']for x in retired]==EXACT_INDICES and len(remaining)==3030
    assert len({x['current_pin']['path']for x in remaining})==2979
    # Every retained complete PF remains strict, including mandatory-false rows.
    # Stream large scientific inputs; never collect their bytes in memory.
    checked={};fullbytes=0
    for ordinal,row in enumerate(remaining,1):
        current=row['current_pin'];historical=row['historical_pin']
        assert norm(current)==current and len(current['identity'])==7
        assert historical['path']==current['path']and historical['sha256']==current['sha256']and historical['size_bytes']==current['size_bytes']
        assert historical['identity'][1:]==current['identity'][1:]and current['identity'][0]==16777229
        assert type(row['mandatory'])is bool and isinstance(row['roles'],list)
        p=current['path']
        if p not in checked:
            _,actual=pin(p);assert actual==current;checked[p]=actual;fullbytes+=actual['size_bytes']
        else:
            assert checked[p]==current and ids(Path(p).lstat())==current['identity']
        assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<512*2**20
        assert 0<time.monotonic()-start<1800
        if ordinal in (1,1000,2000,3030):print(json.dumps({'readonly_EOF_progress_retained_rows':ordinal,'unique_files_checked':len(checked)}),flush=True)
    oldcommon,commonpf=pin(OLD_COMMON,True);common=oldcommon.decode()
    oldbase="BASE = REC/'current_mount_full_identity_common_source_v1'"
    newbase="BASE = REC/'post_curated66_current_catalog_common_source_v2_20261013'"
    oldbind="BIND = BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'"
    newbind="BIND = BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json'"
    assert common.count(oldbase)==1 and common.count(oldbind)==1
    derived=common.replace(oldbase,newbase,1).replace(oldbind,newbind,1)
    assert derived.replace(newbind,oldbind,1).replace(newbase,oldbase,1).encode()==oldcommon
    ast.parse(derived)
    oldhist=copy.deepcopy(catalog['historical_non_live_declarations']);newcatalog=copy.deepcopy(catalog)
    newcatalog['rows']=remaining
    moved=[]
    for data in retired:
        row=data['original_row']
        declaration=dict(historical_pin=row['historical_pin'],mandatory=False,roles=row['roles'],
          declaration_occurrence_count=row['declaration_occurrence_count'],differences=['path_absent_after_actual_exact_curated66_release'],
          observed_current_pin=None,historical_only_not_rebound=True,
          actual_released_original_pin=row['current_pin'],actual_release_receipt_pin=receiptpf,
          actual_independent_postrelease_review_pin=postpf,original_catalog_row_index=data['original_catalog_index'])
        assert 'current_pin'not in declaration;moved.append(declaration)
    newcatalog['historical_non_live_declarations']=oldhist+moved
    newcatalog['post_release_role_reconciliation']=dict(schema='EXACT_CURATED66_POSTRELEASE_CATALOG_ROLE_RECONCILIATION_V1',
      Source_only=True,compiler_executed=False,numerical_executed=False,deletion_executed_by_this_step=False,
      predecessor_catalog_pin=oldcatpf,actual_release_receipt_pin=receiptpf,actual_release_true_tool_pin=releasetoolpf,
      actual_independent_postrelease_review_pin=postpf,actual_independent_postrelease_true_tool_pin=posttoolpf,
      original_top_non_rows_accounting_is_predecessor_historical_attestation=True,
      exact_retired_row_count=10,original_retired_indices=EXACT_INDICES,retained_row_count=3030,
      actual_retained_current_full_EOF_unique_regular_files=len(checked),actual_retained_current_full_EOF_unique_bytes=fullbytes,
      all3030_retained_rows_whole_data_and_order_unchanged=True,all_retained_PF_all7_SHA_fullEOF_reverified=True,
      historical_removed_rows_have_no_top_level_current_pin=True,missing_mandatory_or_other_unreleased_rows_skipped=False,
      historical_reports_sources_unmodified=True,mathematical_or_physics_qualification_promoted=False)
    restored=copy.deepcopy(newcatalog);restored.pop('post_release_role_reconciliation')
    restored['historical_non_live_declarations']=restored['historical_non_live_declarations'][:-10]
    for item in retired:restored['rows'].insert(item['original_catalog_index'],item['original_row'])
    assert restored==catalog
    OUT.mkdir(exist_ok=False)
    commonnewpf=put('guarded_warm_A_common.py',derived.encode())
    newcatpf=put('CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json',newcatalog)
    newbinding=copy.deepcopy(binding)
    assert [i for i,row in enumerate(binding['fixed_current_pins'])if row==oldcatpf]==[2006]
    newbinding['current_mount_full_identity_catalog_pin']=newcatpf
    newbinding['fixed_current_pins'][2006]=newcatpf
    back=copy.deepcopy(newbinding);back['current_mount_full_identity_catalog_pin']=oldcatpf;back['fixed_current_pins'][2006]=oldcatpf
    assert back==binding
    newbindpf=put('CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json',newbinding)
    inversepf=put('COMPLETE_POST_CURATED66_CATALOG_BINDING_COMMON_WHOLE_DATA_BYTE_INVERSE.json',dict(
      schema='COMPLETE_POST_CURATED66_CATALOG_BINDING_COMMON_WHOLE_DATA_BYTE_INVERSE_V1',
      original_catalog_pin=oldcatpf,new_catalog_pin=newcatpf,exact_removed_original_rows=retired,
      original_historical_declaration_count=len(oldhist),original_non_rows_metadata_values_unchanged=True,
      whole_catalog_canonical_data_inverse_observed=True,original_binding_pin=bindingpf,new_binding_pin=newbindpf,
      exact_binding_replacement_index=2006,binding_only_two_same_catalog_PF_references_changed=True,
      whole_binding_canonical_data_inverse_observed=True,original_Common_pin=commonpf,new_Common_pin=commonnewpf,
      Common_literal_splices=[dict(before=oldbase,after=newbase),dict(before=oldbind,after=newbind)],
      Common_whole_byte_inverse_observed=True,all_original_guard_math_serializer_method_bytes_unchanged=True,
      no_compiler_or_Host_import_or_business_or_deletion=True))
    inputs=[bindingpf,oldcatpf,commonpf,receiptpf,releasetoolpf,postpf,posttoolpf,mfpf]
    _,refusalpf=pin(REFUSAL,True);inputs.append(refusalpf)
    rolepf=put('EXACT_TEN_RELEASED_CATALOG_ROWS_TO_HISTORICAL_ROLE_PLAN.json',dict(
      schema='EXACT_TEN_ACTUAL_RELEASED_CURRENT_CATALOG_ROLE_SOURCE_PLAN_V1',source_only=True,
      compiler_executed=False,numerical_executed=False,deleted_by_this_step=False,
      original_metadata_inputs=inputs,exact_ten_retired_original_rows=retired,
      retained_row_count=3030,retained_unique_current_paths=len(checked),actual_retained_fullEOF_bytes=fullbytes,
      no_top_level_current_pin_in_new_historical_declarations=True,
      oldBIND2012_fixed_rows_other2011_unchanged=True,oldCommon_only_two_BASE_BIND_literals_changed=True,
      future_new_build_object_pin=None,future_new_build_report_pin=None,math_or_physics_admitted=False))
    eofpf=put('ACTUAL_RETAINED3030_UNIQUE2979_COMPLETE_EOF_ALL7_SOURCE_RECHECK.json',dict(
      schema='ACTUAL_POST_CURATED66_RETAINED3030_COMPLETE_EOF_ALL7_SOURCE_RECHECK_V1',
      status='PASS_RETAINED3030_ROWS_UNIQUE2979_CURRENT_COMPLETE_EOF_ALL7',
      row_count=3030,unique_file_count=len(checked),unique_fullEOF_bytes=fullbytes,
      actual_full_EOF_pins=list(checked.values()),all_retained_order_and_data_unchanged=True,
      released_targets_not_opened=True,all_file_descriptors_closed=True,
      SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,wall_seconds=time.monotonic()-start,
      compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
    readypf=put('POST_CURATED66_CATALOG_COMMON_SOURCE_REVIEW_READY.json',dict(
      schema='POST_CURATED66_CATALOG_BINDING_COMMON_SOURCE_ONLY_REVIEW_READY_V1',source_only=True,
      compiler_executed=False,numerical_executed=False,Host_imported=False,
      files=[commonnewpf,newcatpf,newbindpf,inversepf,rolepf,eofpf],original_source_metadata_pins=inputs,
      actual_release_receipt_pin=receiptpf,actual_release_true_tool_return_pin=releasetoolpf,
      actual_independent_postrelease_review_pin=postpf,actual_independent_postrelease_true_tool_return_pin=posttoolpf,
      new_catalog_pin=newcatpf,new_binding_pin=newbindpf,new_Common_Source_pin=commonnewpf,
      complete_byte_data_inverse_pin=inversepf,retained_fullEOF_all7_report_pin=eofpf,
      independent_source_role_review_pin=None,final_Source_freeze_pin=None,
      future_actual_build_report_pin=None,compiler_qualified=False,reader_qualified=False,
      AAA_qualified=False,ABA_admitted=False))
    for original in inputs:assert pin(original['path'])[1]==original
    for row in checked.values():assert ids(Path(row['path']).lstat())==row['identity']
    print(json.dumps({'status':'SOURCE_ONLY_POST_CURATED66_CATALOG_COMMON_PREPARED_UNIMPORTED_UNQUALIFIED',
      'source_review_ready_pin':readypf,'new_Common_Source_pin':commonnewpf,'new_catalog_pin':newcatpf,
      'new_binding_pin':newbindpf,'complete_byte_data_inverse_pin':inversepf,'retained_fullEOF_report_pin':eofpf,
      'retired_rows':10,'retained_rows':3030,'actual_unique_retained_fullEOF_files':len(checked),
      'actual_unique_retained_fullEOF_bytes':fullbytes,'SELF_peak_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
      'wall_seconds':time.monotonic()-start,'compiler_executed':False,'numerical_executed':False,'deleted':False}))


if __name__=='__main__':main()
