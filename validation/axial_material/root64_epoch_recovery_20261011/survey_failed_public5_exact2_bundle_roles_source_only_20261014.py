"""Read exactly2 old failedpublic5 bodies + necessary metadata, no cleanup/business."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011');P=Path('/Users/wen/spot/validation/artifacts/axial-material-new-BQ64-genuine-public-READ-seven-controls-20261013-v5');OUT=R/'independent_failed_public5_literal2_bundle_storage_role_survey_20261014';seen={}
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,payload=False):
 p=Path(p);s=p.lstat();i=ids(s);assert stat.S_ISREG(s.st_mode);fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as f:
  assert ids(os.fstat(f.fileno()))==i
  if payload:raw=None;sha=hashlib.file_digest(f,'sha256').hexdigest()
  else:raw=f.read();sha=hashlib.sha256(raw).hexdigest()
  assert ids(os.fstat(f.fileno()))==i
 assert ids(p.lstat())==i;pf=dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=i);seen[str(p)]=(pf,raw);return pf,raw
def read(p):pf,raw=pin(p);return json.loads(raw),pf
def hits(value,paths,prefix=''):
 rows=[]
 if isinstance(value,dict):
  if value.get('path')in paths and {'path','sha256','size_bytes','identity'}<=set(value):rows.append(dict(JSON_pointer=prefix,pin={k:value[k]for k in('path','sha256','size_bytes','identity')}))
  for k,v in value.items():rows.extend(hits(v,paths,prefix+'/'+k))
 elif isinstance(value,list):
  for i,v in enumerate(value):rows.extend(hits(v,paths,prefix+'/'+str(i)))
 return rows
assert not OUT.exists();owner,opf=read(P/'Root_actual_control_summary.json');target=[x for x in owner['output_pins']if Path(x['path']).name=='coherent_complete_context.xsm'];paths={x['path']for x in target};assert len(paths)==2
for row in target:
 p=Path(row['path']);assert p.lstat().st_uid==os.getuid()and p.lstat().st_nlink==1 and all(not q.is_symlink()for q in(p,*p.parents));actual,raw=pin(p,payload=True);assert actual==row
assert sum(x['size_bytes']for x in target)==200327056 and len({tuple(x['identity'][:2])for x in target})==2
matrix=[]
for role,name,n in [('v15','aaa_three_plane_compact_expected_pipeline_source_v15_20261014/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',2802),('build4','bq64_compact_expected_build_host_source_v4_20261013/COMPLETE_BQ64_COMPACT_EXPECTED_BUILD_HOST_SOURCE_FREEZE.json',2565),('fresh17','bq64_compact_expected_connected17_host_source_v2_20261013/COMPLETE_FRESH17_NEW_BOOTQ_HOST_SOURCE_FREEZE.json',2586),('model5','bq64_private_GANLIB_model_control_host_source_v5_20261013/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json',2597),('public7','public_read_compact_bq_admission_control_host_source_v7_20261014/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json',2629),('oldpublic5','public_read_compact_bq_admission_control_host_source_v5_20261013/COMPLETE_CONTROL_HOST_SOURCE_FREEZE.json',2609)]:
 d,pf=read(R/name);assert len(d['dependencies'])==n and hits(d,paths)==[];matrix.append(dict(role=role,pin=pf,dependency_count=n,direct_or_nested_bodyPF_refs=[]))
for role,dirname,name in [('build4','axial-material-new-BQ64-compact-expected-composed-complete70-build-only-20261013-v4','Root_actual_build_only_summary.json'),('fresh17','axial-material-new-BQ64-compact-expected-fresh-connected17-20261013-v2','Root_actual_connected17_summary.json'),('model5','axial-material-new-BQ64-private-GANLIB-model-controls-20261013-v5','Root_actual_control_summary.json'),('public7','axial-material-new-BQ64-genuine-public-READ-seven-controls-20261014-v7','Root_actual_control_summary.json')]:
 d,pf=read(R.parent.parent/'artifacts'/dirname/name);assert hits(d,paths)==[];matrix.append(dict(role=role+'_actual_report',pin=pf,fixed_count=len(d['fixed_current_pins']),output_count=len(d['output_pins']),direct_or_nested_bodyPF_refs=[]))
for role,name,n in [('CAT3030','post_curated66_current_catalog_common_source_v2_20261013/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG_POST_CURATED66.json',3030),('BIND2012','post_curated66_current_catalog_common_source_v2_20261013/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING_POST_CURATED66.json',2012),('material33','current_formal_material_authority_exact_cache70_source_v7/EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json',33),('GENDF51','current_eleven_saved_gendf_current_mount_host_source_v4/COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json',51)]:
 d,pf=read(R/name);assert not hits(d,paths)and all(x.encode()not in seen[pf['path']][1]for x in paths);matrix.append(dict(role=role,pin=pf,role_count=n,exact_body_path_or_PF_refs=[]))
mf,mpf=read(R/'storage_release_literal2_old_v14_BQ_source_v2_20261014/EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json');rows=mf['current_protected_full_EOF_pins'];indices=[dict(index=i,pin=x)for i,x in enumerate(rows)if x['path']in paths];assert len(rows)==7251 and [x['index']for x in indices]==[4607,4612]and [x['pin']for x in indices]==target
roles={k:[x for x in v if x in paths]for k,v in mf['Source_DAG_provenance']['roles'].items()if any(x in paths for x in v)};assert set(roles)=={'current_public5_failed_entire_HF_ownHost_actual_fixed_output_summary_retained'}
r,rpf=read(R/'storage_release_literal2_old_v14_BQ_actual_receipts_20261014/ACTUAL_EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_OLD_PRIVATE_RELEASE_RECEIPT.json');assert r['manifest_pin']==mpf and r['deleted_files']==2 and r['logical_bytes_released']==528482632
old66,old66pf=read(R/'storage_release_curated66_old_private_copies_source_v3_20261013/EXACT_CURATED66_OLD_PRIVATE_RELEASE_MANIFEST.json');assert not hits(old66,paths)
commonpf,craw=pin(R/'storage_release_literal2_old_v14_BQ_source_v2_20261014/literal2_release_common.py');a=ast.parse(craw);bundles=ast.literal_eval(next(n.value for n in a.body if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='PUBLIC5_FAILED_BUNDLES'for t in n.targets)));assert bundles==target
f=next(n for n in a.body if isinstance(n,ast.FunctionDef)and n.name=='current_protection');code=ast.get_source_segment(craw.decode(),f);assert 'for p in PUBLIC5_FAILED_BUNDLES:'in code and "hf['dependencies']+a['fixed_current_pins']+a['output_pins']"in code
historical=[]
for role,name in [('failed_public5_post','independent_compact_BQ_public_v5_auxiliary128_failure_postverify_20261014/REVIEW.json'),('public7_Source0','independent_public7_completed_SRC_bundle_lifecycle_Source_review_20261014/REVIEW.json')]:
 d,pf=read(R/name);historical.append(dict(role=role,pin=pf,body_references=hits(d,paths),meaning='immutable completed original time-fact observation, not direct current runtime dependencies'))
last=owner['records'][-1];w,wpf=read(P/(last['label']+'.watchdog.json'));assert type(w['returncode'])is int and w['returncode']==0 and w['own_child_only']is True and w['liveness_group_cleanup']is True and '128MiB'in w['limit_failure']and last['command'][-2:]==['public_read_stale_BQ_MAC','prepare'];assert owner['status']=='ACTUAL_CONTROL_FAILED_UNQUALIFIED'and len(owner['records'])==10 and owner['actual_seven_genuine_public_READ_controls_passed']is False
files={};directories={}
for p in sorted(P.rglob('*')):
 s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
 if stat.S_ISREG(s.st_mode):files[str(p)]=ids(s)
 elif stat.S_ISDIR(s.st_mode):directories[str(p)]=ids(s)
 else:raise AssertionError('special failedowner file')
assert len(files)==31 and set(files)=={x['path']for x in owner['output_pins']}|{opf['path']}
for x in owner['output_pins']:assert ids(Path(x['path']).lstat())==x['identity']
parents=[dict(path=str(Path(x['path']).parent),identity=ids(Path(x['path']).parent.lstat()),UID=Path(x['path']).parent.lstat().st_uid,expected_future_exact_one_entry_APFS_nlink_delta=-1,expected_future_exact_one_entry_APFS_size_delta=-32)for x in target]
for pf,raw in seen.values():assert ids(Path(pf['path']).lstat())==pf['identity']
OUT.mkdir();d=dict(schema='INDEPENDENT_FAILED_PUBLIC5_EXACT2_BUNDLE_STORAGE_ROLE_SURVEY_V1',status='PASS_READONLY_EXACT_FAILED_PUBLIC5_LITERAL2_ROLE_SURVEY_NO_CLEANUP_ADMISSION',failure=None,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,exact_target_full_EOF_pins=target,target_UID=os.getuid(),target_count=2,total_logical_bytes=200327056,all7_fullEOF_actual_observed=True,independent_physical_inodes=True,live_and_nested_dependency_matrix=matrix,original_failed_public5_report_pin=opf,original_failed_public5_status=owner['status'],original_failed_public5_failure=owner['failure'],old_public5_output_target_indices=[dict(index=i,pin=x)for i,x in enumerate(owner['output_pins'])if x['path']in paths],old_public5_owned_target_indices=[dict(index=i,pin=x)for i,x in enumerate(owner['owned_runtime_pins'])if x['path']in paths],MAC_before_manifest_not_claimed=True,last_actual_failed_prepare_watch_pin=wpf,last_actual_child_returncode=0,last_actual_watch_limit_failure=w['limit_failure'],normal_resource_closed0_not_claimed=True,previous_literal2_manifest_pin=mpf,previous_literal2_completed_release_receipt_pin=rpf,previous_literal2_protected_count=7251,exact_two_previous_current_protected_indices=indices,exact_previous_protected_roles=roles,original_curated66_manifest_pin=old66pf,original7030_not_containing_public5_bodies=True,old_literal2_common_Source_pin=commonpf,old_literal2_current_protection_function_requires_exact_both_bodies_current=True,historical_nested_time_fact_sources=historical,failed_public5_current31_file_inventory=files,failed_public5_directory_inventory=directories,exact2_parent_current_identity=parents,future_minimal_migration=dict(previous7251_activeprotected_to7249=True,only_exact_original_indices4607_4612_to_historical=True,old_public5_current_scene31_files_to29=True,old_failed_report_output_owned_PFs_remain_immutable_history=True,old_MF_SF_release_receipt_and_postreview_unchanged=True,all_other_raw_logs_watch_sentinel_MF_summaries_Source_science_current_preserved=True,only_old_failed_public5_two_exact_path_replay_lost=True,new_SourceHF_catalog_BIND_changes_required=False,no_generic_missing_PF_skip=True,new_unique_cleanup_Source_explicit_role_migration_required=True),public7_current_MAC_bundle_preserved=True,public7_retirement_SRC_context_not_this_target=True,no_other_scientific_payload_fullEOF_read=True,v15_active_outputs_not_opened=True,future_v15_terminal_gate_pin=None,future_v15_independent_post_gate_pin=None,future_no_active_writer_PS_lsof_gate=None,future_cleanup_Source_freeze_pin=None,future_cleanup_manifest_pin=None,cleanup_execution_authorized=False,AAA_qualified=False,ABA_admitted=False)
p=OUT/'REVIEW.json';fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
with os.fdopen(fd,'wb')as f:f.write((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode());f.flush();os.fsync(f.fileno())
rpf,raw=pin(p);print(json.dumps(dict(status=d['status'],failure=None,review_pin=rpf,target_count=2,total_logical_bytes=200327056,previous_protected_count=7251,exact_protected_indices=[4607,4612],old_public5_scene_file_count=31,future_cleanup_manifest_pin=None,source_only=True,numerical_executed=False,deletion_executed=False)))
