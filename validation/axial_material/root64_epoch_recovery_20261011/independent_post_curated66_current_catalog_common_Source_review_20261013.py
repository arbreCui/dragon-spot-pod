import os, stat, json, hashlib, ast
from pathlib import Path

R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
D=R/'post_curated66_current_catalog_common_source_v2_20261013'
O=R/'independent_post_curated66_current_catalog_common_Source_review_20261013'
cache={};checks=[];attested={}
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return {k:p[k]for k in ('path','sha256','size_bytes','identity')}
def check(ok,name):
    if not ok:raise AssertionError(name)
    checks.append(name)
def pin(path):
    p=Path(path);before=identity(p.lstat())
    if not stat.S_ISREG(before[2]):raise AssertionError('regular '+str(p))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb')as f:
        if identity(os.fstat(f.fileno()))!=before:raise AssertionError('open7 '+str(p))
        digest=hashlib.file_digest(f,'sha256').hexdigest()
        if identity(os.fstat(f.fileno()))!=before:raise AssertionError('EOF7 '+str(p))
    if identity(p.lstat())!=before:raise AssertionError('after7 '+str(p))
    out=dict(path=str(p),sha256=digest,size_bytes=before[4],identity=before);cache[str(p)]=out;return out
def same(p):
    p=norm(p)
    if p['path']not in cache and p['path']in attested:
        if attested[p['path']]!=p or identity(Path(p['path']).lstat())!=p['identity']:raise AssertionError('inherited actual fullEOF PF current7 '+p['path'])
        return
    actual=cache.get(p['path'])or pin(p['path'])
    if actual!=p:raise AssertionError('fullPF '+p['path'])
def read(path):
    p=pin(path);raw=Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=p['sha256']or identity(Path(path).lstat())!=p['identity']:raise AssertionError('metadata read7')
    return json.loads(raw),p,raw

ready,sp,_=read(D/'POST_CURATED66_CATALOG_COMMON_SOURCE_REVIEW_READY.json')
check(sp['sha256']=='a5810680884ff22f131bb5db9962c5be6af38360ccbd85e01aa8352474244d44','exact completed v2 Source review READY pin')
check(ready['source_only']is True and ready['compiler_executed']is False and ready['numerical_executed']is False and ready['Host_imported']is False,'READY actual Source-only unimpor ted/no compile/numeric')
check(ready['independent_source_role_review_pin']is None and ready['final_Source_freeze_pin']is None and ready['future_actual_build_report_pin']is None,'pre-freeze review scope; future freeze/build actual pins remain None')
eof,ep,_=read(ready['retained_fullEOF_all7_report_pin']['path']);same(ready['retained_fullEOF_all7_report_pin'])
check(eof['status']=='PASS_RETAINED3030_ROWS_UNIQUE2979_CURRENT_COMPLETE_EOF_ALL7'and eof['row_count']==3030 and eof['unique_file_count']==2979 and eof['unique_fullEOF_bytes']==3052255693 and eof['released_targets_not_opened']is True and eof['all_file_descriptors_closed']is True,'actual parent complete3030 unique2979 EOF report exact scope')
attested={p['path']:norm(p)for p in eof['actual_full_EOF_pins']}
check(len(attested)==2979,'actual completeEOF unique2979 declaration set')
prep,prep_pf,_=read(R/'ACTUAL_POST_CURATED66_CATALOG_COMMON_V2_SOURCE_PREPARATION_TRUE_TOOL_RETURNS_20261013.json')
terminal=prep['actual_v2']['actual_terminal_tool_return']
check(terminal['exit_code']==0 and terminal['chunk_id']=='d9a1ca','genuine v2 preparer terminal original tool EXIT0')
prep_output=json.loads(terminal['output'].strip().splitlines()[-1])
check(norm(prep_output['source_review_ready_pin'])==sp and norm(prep_output['retained_fullEOF_report_pin'])==ep,'real preparer raw output binds exact READY and retainedEOF pins')
check(prep['failed_v1']['actual_terminal_tool_return']['exit_code']==1,'original failed v1 real tool1 preserved')
new,np,_=read(D/'CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json')
old,op,_=read(R/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')
receipt,ap,_=read(R/'storage_release_curated66_old_private_copies_actual_receipts_20261013/ACTUAL_EXACT_CURATED66_OLD_PRIVATE_RELEASE_RECEIPT.json')
check(ap['sha256']=='114d2fd0f13c1af1396823cbba0c4b693130361092ed83ad4ecb6ca2849aadda','genuine actual66 release receipt current exactpin')
released={x['original_fullpin']['path']:norm(x['original_fullpin'])for x in receipt['deletion_records']}
indices=[i for i,x in enumerate(old['rows'])if x['current_pin']['path']in released]
check(len(old['rows'])==3040 and len(indices)==10 and len(new['rows'])==3030,'exact original3040 intersect actual66 is10 retained3030')
removed=[old['rows'][i]for i in indices]
for row in removed:
    check(norm(row['current_pin'])==released[row['current_pin']['path']],'migrated actualreleased exactPF')
    check(row['mandatory']is False and all(x.startswith('recursive_full_PF_from_current_JSON:')for x in row['roles']),'migrated only nonmandatory recursive failed historical JSON declaration')
    check(not Path(row['current_pin']['path']).exists()and not Path(row['current_pin']['path']).is_symlink(),'migrated released path absent without opening')
check(new['rows']==[row for i,row in enumerate(old['rows'])if i not in indices],'all3030 complete row data/order identical')
history=new['historical_non_live_declarations']
check(len(history)==177 and history[:167]==old['historical_non_live_declarations'],'original167 historical entire data retained plus10')
for entry,row,i in zip(history[167:],removed,indices):
    check('current_pin'not in entry and entry['historical_pin']==row['historical_pin']and entry['roles']==row['roles']and entry['mandatory']is False,'historical migration no topcurrent alias preserves historical identity/roles')
    check(norm(entry['actual_released_original_pin'])==norm(row['current_pin'])and entry['original_catalog_row_index']==i and entry['observed_current_pin']is None and entry['historical_only_not_rebound']is True,'migration preserves actual lastPF only as archival released evidence')
    same(entry['actual_release_receipt_pin']);same(entry['actual_independent_postrelease_review_pin'])
check({k:v for k,v in new.items()if k not in ('rows','historical_non_live_declarations','post_release_role_reconciliation')}=={k:v for k,v in old.items()if k not in ('rows','historical_non_live_declarations')},'all original top metadata preserved explicitly as predecessor attestation')
role=new['post_release_role_reconciliation']
check(norm(role['predecessor_catalog_pin'])==op and role['original_top_non_rows_accounting_is_predecessor_historical_attestation']is True,'selected original catalog top accounting remains historical source attestation')
for k in ('actual_release_receipt_pin','actual_release_true_tool_pin','actual_independent_postrelease_review_pin','actual_independent_postrelease_true_tool_pin'):same(role[k])
check(role['exact_retired_row_count']==10 and role['original_retired_indices']==indices and role['retained_row_count']==3030,'role exact counts/indices')
check(role['Source_only']is True and all(role[k]is False for k in ('compiler_executed','numerical_executed','deletion_executed_by_this_step','missing_mandatory_or_other_unreleased_rows_skipped','mathematical_or_physics_qualification_promoted')),'no missing mandatory/unreleased skip or execution/qualification')
unique={}
for row in new['rows']:
    p=norm(row['current_pin']);oldpf=norm(row['historical_pin'])
    if not(oldpf['path']==p['path']and oldpf['sha256']==p['sha256']and oldpf['size_bytes']==p['size_bytes']and oldpf['identity'][1:]==p['identity'][1:]and p['identity'][0]==16777229):raise AssertionError('retained exact historical to actual device-only PF view')
    if p['path']in unique and unique[p['path']]!=p:raise AssertionError('inconsistent retained completePF')
    unique[p['path']]=p
    same(p)
check(len(unique)==role['actual_retained_current_full_EOF_unique_regular_files']==2979 and sum(p['size_bytes']for p in unique.values())==role['actual_retained_current_full_EOF_unique_bytes']==3052255693,'actual retained3030 unique2979 fullEOF/7 and byte accounting')
newbind,bp,_=read(D/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json')
oldbind,obp,_=read(R/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')
oldcatalog=norm(oldbind['current_mount_full_identity_catalog_pin'])
check(oldcatalog==op and norm(newbind['current_mount_full_identity_catalog_pin'])==np,'BIND currentcatalog exact old/new PF')
replaced=dict(oldbind);replaced['current_mount_full_identity_catalog_pin']=np
replaced['fixed_current_pins']=[np if norm(x)==op else x for x in oldbind['fixed_current_pins']]
check(newbind==replaced and len(newbind['fixed_current_pins'])==len(oldbind['fixed_current_pins'])==2012,'BIND whole data only catalogPF replacements;2012 order unchanged')
check([i for i,p in enumerate(oldbind['fixed_current_pins'])if norm(p)==op]==[2006]and norm(newbind['fixed_current_pins'][2006])==np,'actual original unique catalogPF fixedindex2006 replaced only')
for p in newbind['fixed_current_pins']:same(p)
oldcommon=R/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/guarded_warm_A_common.py'
common=D/'guarded_warm_A_common.py';cp=pin(common);ocp=pin(oldcommon);cb=common.read_bytes();ocb=oldcommon.read_bytes()
replacement=[(b"BASE = REC/'post_curated66_current_catalog_common_source_v2_20261013'",b"BASE = REC/'current_mount_full_identity_common_source_v1'"),(b"BIND = BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json'",b"BIND = BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'")]
restored=cb
for after,before in replacement:
    check(restored.count(after)==1,'one exact Common namespace literal');restored=restored.replace(after,before,1)
check(restored==ocb,'Common wholeEOF inverse only BASE/BIND two literals; all methods/math/serializers unchanged')
ast.parse(cb)
inverse,ip,_=read(ready['complete_byte_data_inverse_pin']['path']);same(ready['complete_byte_data_inverse_pin'])
check(inverse['exact_binding_replacement_index']==2006 and inverse['whole_catalog_canonical_data_inverse_observed']is True and inverse['whole_binding_canonical_data_inverse_observed']is True and inverse['Common_whole_byte_inverse_observed']is True,'author wholeinverse exact2006 and complete three-file inverse contract')
check([r['original_catalog_index']for r in inverse['exact_removed_original_rows']]==indices and [r['original_row']for r in inverse['exact_removed_original_rows']]==removed,'inverse contains all exact10 entire original rows in index order')
check(norm(ready['new_catalog_pin'])==np and norm(ready['new_binding_pin'])==bp and norm(ready['new_Common_Source_pin'])==cp,'READY exact current three Source pins')
for p in ready['files']+ready['original_source_metadata_pins']:same(p)
for p in attested.values():
    if identity(Path(p['path']).lstat())!=p['identity']:raise AssertionError('final inherited2979 actualEOF/current7 '+p['path'])
for p in cache.values():
    if identity(Path(p['path']).lstat())!=p['identity']:raise AssertionError('final Source/dependency7 '+p['path'])
report=dict(schema='INDEPENDENT_POST_CURATED66_CURRENT_CATALOG_COMMON_SOURCE_ONLY_REVIEW_V1',status='PASS_SOURCE_ONLY_EXACT10_ROLE_MIGRATION',failure=None,Source_freeze_pin=None,Source_review_ready_pin=sp,catalog_pin=np,binding_pin=bp,common_source_pin=cp,original_catalog_pin=op,original_binding_pin=obp,original_Common_pin=ocp,actual_release_receipt_pin=ap,actual_retained_fullEOF_report_pin=ep,actual_preparer_true_tool_return_pin=prep_pf,source_only=True,Host_imported=False,Host_main_executed=False,compiler_executed=False,compiled=False,numerical_executed=False,numeric=False,business_executed=False,deletion_executed_by_this_reviewer=False,released_targets_opened=False,science_EOF_repeated=False,actual_retained_row_count=3030,actual_retained_unique_file_count=2979,inherited_actual_fullEOF2979_all_current7_independently_reverified=True,exact_retired_row_count=10,all_file_descriptors_closed=True,checks=checks,checked_full_EOF_Source_metadata_pin_count=len(cache),checked_exact_Source_metadata_pins=[sp,np,bp,cp,op,obp,ocp,ap,ep,prep_pf,ip])
report['status']='PASS_POST_CURATED66_CATALOG_BINDING_COMMON_SOURCE_ONLY'
report.update(actual_common_source_pin=cp,actual_catalog_pin=np,actual_binding_pin=bp,actual_source_review_ready_pin=sp)
O.mkdir(exist_ok=True);p=O/'FINAL_REVIEW.json';p.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n');rp=pin(p)
print(json.dumps(dict(status=report['status'],failure=None,review_pin=rp,Source_review_ready_pin=sp,catalog_pin=np,binding_pin=bp,common_source_pin=cp,actual_retained_row_count=3030,all_file_descriptors_closed=True),ensure_ascii=False))
