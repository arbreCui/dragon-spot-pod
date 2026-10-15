#!/usr/bin/env python3
"""Read-only literal role survey; no deletion, imports or business execution."""
from pathlib import Path
import hashlib,json,os,stat

REC=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART=Path('/Users/wen/spot/validation/artifacts')
OLD=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261013-v14'
OUT=REC/'post_v15_failed_v14_private_storage_literal_role_readonly_survey_20261014'

def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
    p=Path(p);a=seven(p.lstat());assert stat.S_ISREG(a[2])and not p.is_symlink()
    h=hashlib.sha256();fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        assert seven(os.fstat(fd))==a
        with os.fdopen(fd,'rb')as f:
            fd=None
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
            assert seven(os.fstat(f.fileno()))==a
    finally:
        if fd is not None:os.close(fd)
    assert seven(p.lstat())==a
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=a[4],identity=a)
def read(p):
    pf=pin(p);d=json.loads(Path(p).read_text());assert seven(Path(p).lstat())==pf['identity'];return d,pf
def rows_by_paths(d,keys):return[row for key in keys for row in d.get(key,[])]
def nested_matches(d,path,pointer='$'):
    out=[]
    if isinstance(d,dict):
        if set(d)=={'path','sha256','size_bytes','identity'}and d.get('path')==path:out.append(dict(pointer=pointer,pin=d))
        else:
            for key,v in d.items():out.extend(nested_matches(v,path,pointer+'/'+key))
    elif isinstance(d,list):
        for i,v in enumerate(d):out.extend(nested_matches(v,path,pointer+'/'+str(i)))
    return out
def main():
    leaves=['projected_boot.xsm','BOOT-Q-1.xsm','BOOT-MAC-1.xsm','radial1.bin','radial2.bin','radial3.bin',
      'axial_macro.xsm','ax_current.xsm','initial_system.xsm','basis.xsm','axial_track.xsm']
    targets=[pin(OLD/'AAA'/leaf)for leaf in leaves]
    assert all(x['identity'][3]==1 for x in targets)
    target_paths={x['path']:x for x in targets};physical={tuple(x['identity'][:2]):x for x in targets}
    examined=[];live=[];docs=[]
    def check(role,path,selector):
        d,pf=read(path);rows=selector(d);assert isinstance(rows,list)
        matches=[]
        for i,row in enumerate(rows):
            assert isinstance(row,dict)and all(k in row for k in ('path','sha256','size_bytes','identity'))
            if row['path']in target_paths or tuple(row['identity'][:2])in physical:
                matches.append(dict(index=i,pin=row,path_match=row['path']in target_paths,
                  physical_alias_match=tuple(row['identity'][:2])in physical))
            live.append(row)
        examined.append(dict(role=role,metadata_pin=pf,current_row_count=len(rows),target_current_matches=matches))
        docs.append((role,d,pf));return d
    v15=check('final_v15_HF2802',REC/'aaa_three_plane_compact_expected_pipeline_source_v15_20261014/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json',lambda d:d['dependencies'])
    selected=v15
    for role,hkey,rkey in [('newbuild4','selected_new_build_Host_freeze_pin','selected_actual_new_build70_report_pin'),
      ('fresh17v2','selected_fresh17_Host_freeze_pin','selected_actual_fresh17_report_pin'),
      ('modelv5','selected_private_model_Host_freeze_pin','selected_actual_private_model_report_pin'),
      ('public7','selected_public7_Host_freeze_pin','selected_actual_public7_report_pin')]:
        check(role+'_SourceHF',selected[hkey]['path'],lambda d:d['dependencies'])
        check(role+'_actual_current_fixed_output_owned',selected[rkey]['path'],lambda d:rows_by_paths(d,['fixed_current_pins','output_pins','owned_runtime_pins']))
    check('current_catalog3030',v15['selected_post_release_current_catalog_pin']['path'],lambda d:[x['current_pin']for x in d['rows']])
    check('current_BIND2012',v15['selected_post_release_current_binding_pin']['path'],lambda d:d['fixed_current_pins'])
    check('material_origin33',REC/'current_formal_material_authority_exact_cache70_source_v7/EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json',lambda d:[x['current_pin']for x in d['rows']])
    check('material_build_SourceHF39',REC/'current_formal_material_authority_exact_cache70_source_v7/COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json',lambda d:d['dependencies'])
    check('GENDF_origin51',REC/'current_eleven_saved_gendf_current_mount_host_source_v4/COMPLETE_CURRENT_GENDF_INPUT_METADATA_REATTESTATION_SOURCE_ONLY.json',lambda d:[x['current_pin']for x in d['rows']])
    check('GENDF_SourceHF67',REC/'current_eleven_saved_gendf_current_mount_host_source_v4/COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json',lambda d:d['dependencies'])
    sf=read(selected['selected_new_Fortran_Source_freeze_pin']['path'])[0]
    check('production_compact_FortranSF',selected['selected_new_Fortran_Source_freeze_pin']['path'],lambda d:d['files']+d['original_source_pins']+[d['complete_byte_inverse_pin'],d['control_plan_pin']])
    public_own=read(selected['selected_public7_Host_freeze_pin']['path'])[0]
    check('public_control_FortranSF',public_own['selected_control_Source_freeze_pin']['path'],lambda d:d['files']+d['original_source_pins']+d.get('dependencies',[]))
    assert not any(x['target_current_matches']for x in examined)
    # Current whole-dependency identity checks reuse frozen EOF provenance and
    # reobserve seven fields. No unrelated scientific payload is reread.
    seen={}
    for row in live:
        if row['path']in seen:assert seen[row['path']]==row
        seen[row['path']]=row
    for row in seen.values():
        path=Path(row['path']);assert not path.is_symlink()and seven(path.lstat())==row['identity']
    mf,mfp=read(REC/'storage_release_literal2_old_v14_BQ_source_v2_20261014/EXACT_LITERAL2_OLD_V14_PRIVATE_BQ_RELEASE_MANIFEST.json')
    cur66,cur66pf=read(REC/'storage_release_curated66_old_private_copies_source_v3_20261013/EXACT_CURATED66_OLD_PRIVATE_RELEASE_MANIFEST.json')
    old_summary,old_summary_pin=read(OLD/'Root_actual_three_plane_engineering_summary.json')
    old_raw,old_raw_pin=read(OLD/'Root_actual_complete_execution_record_before_final_publication.json')
    protection=[]
    for target in targets:
        roles={name:paths.count(target['path'])for name,paths in mf['Source_DAG_provenance']['roles'].items()if target['path']in paths}
        rows=[dict(index=i,pin=x)for i,x in enumerate(mf['current_protected_full_EOF_pins'])if x['path']==target['path']]
        original=[dict(index=i,pin=x)for i,x in enumerate(cur66['current_protected_full_EOF_pins'])if x['path']==target['path']]
        v14rows=[dict(index=i,pin=x)for i,x in enumerate(mf['retained_all_other_v14_files_full_EOF_pins'])if x['path']==target['path']]
        assert len(rows)==len(v14rows)==1 and rows[0]['pin']==v14rows[0]['pin']==target
        assert len(original)==1 and original[0]['pin']==target
        protection.append(dict(target_pin=target,current_literal2_protected_matches=rows,original_curated66_protected_matches=original,
          latest_literal2_current_v14_297_matches=v14rows,current_role_names_and_occurrence_counts=roles,
          failed_v14_summary_nested_matches=nested_matches(old_summary,target['path']),
          failed_v14_raw_nested_matches=nested_matches(old_raw,target['path']),
          nested_PF_do_not_become_new_business_DAG_edges=True,release_not_yet_authorized_or_prepared=True))
    # Largest earlier remaining failed private file, for a separate scope choice.
    earlier=[]
    for root in sorted(ART.iterdir()):
        if not root.is_dir()or not root.name.startswith('axial-material-new-AAA3-streaming')or root==OLD or '20261014-v15'in root.name:continue
        for p in root.rglob('*'):
            if not p.is_file()or p.is_symlink()or p.suffix not in ('.xsm','.bin'):continue
            s=p.lstat()
            if s.st_size<100000000:continue
            matching=[x for x in live if x['path']==str(p)or x['identity'][:2]==[s.st_dev,s.st_ino]]
            oldroles={name:paths.count(str(p))for name,paths in mf['Source_DAG_provenance']['roles'].items()if str(p)in paths}
            earlier.append(dict(path=str(p),size_bytes=s.st_size,current_identity=seven(s),
              direct_current_business_matches=matching,prior_literal2_protection_roles=oldroles,
              explicit_previous_preservation_requires_new_scope_decision=True,whole_EOF_reread=False,not_selected_for_release=True))
    earlier.sort(key=lambda x:x['size_bytes'],reverse=True)
    principal=targets[:3];alias=targets[3:]
    report=dict(schema='POST_V15_FAILED_V14_PRIVATE_STORAGE_EXACT_ROLE_READONLY_SURVEY_V1',
      status='PASS_READONLY_ROLE_SURVEY_FUTURE_RELEASE_GATED',failure=None,readonly=True,source_only=True,
      principal_exact3_pins=principal,principal_exact3_bytes=sum(x['size_bytes']for x in principal),
      consumed_private_alias_candidate_pins=alias,alias_candidate_count=len(alias),alias_candidate_bytes=sum(x['size_bytes']for x in alias),
      all_v14_candidate_count=len(targets),all_v14_candidate_bytes=sum(x['size_bytes']for x in targets),
      direct_current_closure_checks=examined,current_unique_pin_count=len(seen),all_current_seven_fields_reobserved=True,
      candidate_fullEOF_SHA_all7_observed=True,candidate_protection_and_failed_history_roles=protection,
      previous_literal2_manifest_pin=mfp,previous_curated66_manifest_pin=cur66pf,
      failed_v14_summary_pin=old_summary_pin,failed_v14_raw_pin=old_raw_pin,
      earlier_large_stat_only_private_files=earlier,
      proposed_exact_transition=dict(only_selected_fullpins_may_be_removed_from_new_current_protection=True,
        old_literal2_7251_and_old_v14_297_attestations_remain_immutable_historical=True,
        no_rewrite_old_results_or_Source_or_nested_scientific_facts=True,
        current_v15_newbuild_fresh_model_public7_and_material_GENDF_closures_are_protected=True,
        no_catalog_or_BIND_changes_for_these_literal_targets=True,no_generic_missing_or_restore=True),
      pending_gates=dict(actual_v15_successful_report_pin=None,actual_v15_Root_terminal_tool_pin=None,
        actual_v15_independent_post_review_pin=None,actual_next_stage_original_fullfresh2_budget_pin=None,
        Root_exact_future_release_scope_authorization=None),
      original_budget_unchanged=dict(fresh_bytes=2*2**30,history_bytes=96*2**30,cold_bytes=20971764748,
        meta_bytes=64*2**20,free_floor_bytes=8*2**30,self_child_bytes=512*2**20,stage_seconds=600,whole_seconds=1800),
      mathematical_or_scientific_qualification_granted=False,manifest_prepared=False,cleanup_Source_created=False,
      business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,
      unrelated_scientific_EOF_reread=False,new_v15_outputs_opened=False,all_file_descriptors_closed=True)
    OUT.mkdir();path=OUT/'REVIEW.json'
    with path.open('x')as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    pf=pin(path)
    print(json.dumps(dict(status=report['status'],review_pin=pf,principal_exact3_bytes=report['principal_exact3_bytes'],
      alias_candidate_bytes=report['alias_candidate_bytes'],all_v14_candidate_bytes=report['all_v14_candidate_bytes'],
      direct_current_closure_count=len(examined),current_unique_pin_count=len(seen),manifest_prepared=False,deletion_executed=False)))

if __name__=='__main__':main()
