"""Independent full-EOF readonly manifest/current-union audit; no cleanup imports."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import time

ROOT=Path('/Users/wen/spot');REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011';ART=ROOT/'validation/artifacts'
PKG=Path(__file__).absolute().parent.parent;OUT=Path(__file__).absolute().parent
HELPER=REC/'storage_release_closed_v7_v8_project_pair_20261013/independent_postverify_20261013/verify_exact_two_postrelease_v2.py'
spec=importlib.util.spec_from_file_location('independent_readonly_full_EOF_primitive',HELPER);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
NAMES=['initial_pack.xsm','axial_macro.xsm','axial_track.xsm','basis.xsm']
BRANCHES=[ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+v) for v in ('v5','v6')]
PATHS=[str(p/'AAA'/name) for p in BRANCHES for name in NAMES]
START=time.monotonic()

def old_inventory():
    import stat
    files={};links={};dirs={};stack=list(BRANCHES)
    while stack:
        p=stack.pop();st=p.lstat();s.check(stat.S_ISDIR(st.st_mode),'old ordinary directory')
        dirs[str(p)]=s.seven(st);fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try:
            with os.scandir(fd) as entries:
                for e in entries:
                    q=p/e.name;st=e.stat(follow_symlinks=False)
                    if stat.S_ISDIR(st.st_mode):stack.append(q)
                    elif stat.S_ISREG(st.st_mode):files[str(q)]=s.seven(st)
                    elif stat.S_ISLNK(st.st_mode):links[str(q)]=dict(identity=s.seven(st),target=os.readlink(q))
                    else:raise RuntimeError('old special entry')
        finally:os.close(fd)
    return dict(ordinary_file_identities=files,symlinks=links,directory_identities=dirs)

def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest-sha256',required=True);p.add_argument('--manifest-seven-id',required=True);a=p.parse_args()
    mp=s.pin(PKG/'EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_MANIFEST.json');s.check(mp['sha256']==a.manifest_sha256 and mp['identity']==json.loads(a.manifest_seven_id),'externally selected final manifest SHA/all7ID')
    m=s.exact_json(mp);s.check(m['schema']=='ROOT_EXACT_EIGHT_CLOSED_FAILED_V5_V6_PRIVATE_COPY_RELEASE_MANIFEST_V1' and m['action_executed'] is False and m['target_count']==8 and m['total_target_logical_bytes']==998909696,'exact unexecuted finite eight manifest')
    sfp=m['selected_complete_Source_only_freeze_pin'];s.check(sfp['sha256']=='f6d1442e3fda4718bfda0d6dcd94e5ab577b5af2b286e13745d69d6407dcf74b' and sfp['identity']==[16777229,50012360,33188,1,5648,1791869633301732784,1791869633301732784],'externally selected unchanged Source-only freeze')
    sf=s.exact_json(sfp)
    for row in sf['Source_pins']+[sf['external_readonly_helper_pin'],sf['readonly_candidate_survey_pin'],sf['required_interface_source_only_pin'],sf['actual_Source_only_protection_preflight_tool_pin']]:s.same(row)
    s.check(sf['Source_pins']==m['Source_pins'] and sf['v9_terminal_prefilled'] is False and sf['final_manifest_created'] is False,'original Source freeze historical statement not promoted to current execution')
    protected=m['current_protected_full_EOF_pins'];table={r['path']:r for r in protected}
    s.check(len(table)==len(protected),'protected list deduplicated')
    for row in protected+m['retained_ordinary_full_EOF_pins']+m['target_full_EOF_pins']:s.same(row)
    targets=m['target_full_EOF_pins'];inodes={tuple(r['identity'][:2]) for r in protected}
    s.check([r['path'] for r in targets]==PATHS and sum(r['size_bytes'] for r in targets)==998909696,'literal exact eight current PFs and byte sum')
    for row in targets:s.check(row['identity'][3]==1 and row['path'] not in table and tuple(row['identity'][:2]) not in inodes,'owned single link candidate disjoint current union')
    s.check(old_inventory()==m['complete_before_inventory'],'all closed old branch directory/file/link seven-identities current unchanged')
    expected=set(m['complete_before_inventory']['ordinary_file_identities'])-set(PATHS)
    s.check({r['path'] for r in m['retained_ordinary_full_EOF_pins']}==expected,'all old entries besides exact eight retained')
    for b in BRANCHES:
        for name in ['global.xsm','ax_current.xsm','initial_system.xsm']:
            s.check(str(b/'AAA'/name) in expected,'failed global causal raw retained')
    catalog=s.exact_json(table[str(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json')])
    common=s.exact_json(table[str(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json')])
    science=s.exact_json(table[str(REC/'saved_full370_terminal_audit_host_source_v2/CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json')])
    hf=s.exact_json(table[str(REC/'aaa_three_plane_streaming_pipeline_source_v9/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')])
    for rows,count in [([r['current_pin'] for r in catalog['rows']],3040),(common['fixed_current_pins'],2012),(science['fixed_current_pins'],3315),(science['science_original_input_pins'],1129),(hf['dependencies'],257)]:
        s.check(len(rows)==count,'all original row cardinality')
        for row in rows:s.check(table[row['path']]==row,'each complete current row exactly represented')
    tool=s.exact_json(m['selected_actual_v9_true_tool_receipt_pin']);v9=s.exact_json(m['selected_actual_v9_summary_pin'])
    s.check(tool['observed_closed'] is True and tool['original_integer_exit_code']==1 and tool['terminal']['exit_code']==1 and v9['status']=='FAILED_UNQUALIFIED_NO_RETRY' and v9['engineering_three_plane_closed0'] is False and v9['after_check_error'] is None and len(v9['records'])==42,'actual v9 unqualified genuine closed exit1 retained')
    records={r['label']:r for r in v9['records']}
    s.check(records['AAA/global_positive']['status']=='PASS' and records['AAA/project_positive']['status']=='PASS' and records['AAA/view_missing_operand']['status']=='FAILED' and v9['records'][-1]['label']=='AAA/view_memory_output','genuine v9 individual successes and failed lexical card scope')
    for row in v9['output_pins']:s.check(table[row['path']]==row,'every actual v9 output fullpin protected unchanged')
    closure=m['Source_DAG_provenance']['actual_closed_v9_protection']
    s.check(closure['Root_true_terminal_exit_code']==1 and closure['engineering_status_preserved'] is False and len(closure['all_actual_v9_stage_closures'])==42,'future-v9 placeholders replaced by actual unqualified closure')
    for row in closure['all_actual_v9_stage_closures']:
        w=s.exact_json(row['watchdog_pin']);s.same(row['log_pin']);s.check(w['liveness_group_cleanup'] is True and w['own_child_only'] is True and w['command']==records[row['label']]['command'],'all42 true owned child closed metadata')
        s.check(table[row['watchdog_pin']['path']]==row['watchdog_pin'] and table[row['log_pin']['path']]==row['log_pin'],'entire actual v9 logs/watchdogs protected')
    namespaces=m['Source_DAG_provenance']['additional_exact_current_source_namespaces'];protected_namespaces={r['namespace'] for r in namespaces}
    for required in ['current_formal_material_authority_exact_cache70_source_v5','current_eleven_saved_gendf_current_mount_host_source_v4','reaction_genDF_current_mount_stream_source_v2']:
        s.check(str(REC/required) in protected_namespaces,'mandatory current final material/GENDF Source namespace included')
    for entry in namespaces:
        path=Path(entry['namespace']);wanted=entry['all_current_Source_and_metadata_full_EOF_pins']
        actual=sorted(str(q) for q in path.rglob('*') if q.is_file())
        s.check(actual==sorted(r['path'] for r in wanted),'entire current Source directory entries unchanged')
        for row in wanted:s.check(table[row['path']]==row,'every Source file fullpin protected')
    for proof in m['closed_failed_overall_v5_v6_run_proofs']:
        d=s.exact_json(proof['failed_overall_summary_pin']);t=s.exact_json(proof['Root_true_closed_exit1_tool_pin'])
        terminal=t['final'] if proof['version']=='v5' else t['terminal']
        s.check(terminal['exit_code']==1 and d['status']=='FAILED_UNQUALIFIED_NO_RETRY' and d['engineering_three_plane_closed0'] is False and len(d['records'])==33,'actual old failed aggregates retained')
        selected={r['label']:r for r in d['records']};s.check(selected['AAA/pack']['status']=='PASS' and selected['AAA/initial_positive']['status']=='PASS','old PACK INITIAL individual pass retained')
        for row in proof['all33_actual_child_closure_and_log_pins']:
            w=s.exact_json(row['watchdog_pin']);s.same(row['log_pin']);s.check(w['returncode']==row['actual_returncode'] and w['limit_failure']==row['limit_failure'] and w['liveness_group_cleanup'] is True and w['own_child_only'] is True,'all66 old ownchild closure and actual limit stops preserved')
    # If v10 is already frozen, check it separately without mutating the old
    # exact8 frozen helper or promoting an unrun v10 to runtime success.
    extra_v10=[];v10hf=REC/'aaa_three_plane_streaming_pipeline_source_v10/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
    if v10hf.exists():
        row=s.pin(v10hf);d=s.exact_json(row);extra_v10.append(row)
        for wanted in [d['host_source']]+d['dependencies']:
            actual=s.pin(wanted['path']);s.check(actual==wanted,'actual current v10 full Source dependency pin')
            s.check(actual['path'] not in PATHS and tuple(actual['identity'][:2]) not in {tuple(p['identity'][:2]) for p in targets},'actual v10 Source/input not any candidate path or inode')
            s.same(actual);extra_v10.append(actual)
    for row in s.VERIFIED.values():s.check(s.seven(Path(row['path']).lstat())==row['identity'],'all verified EOF files still exact at end')
    s.check(not (PKG/'ACTUAL_EXACT_EIGHT_RELEASE_RECEIPT.json').exists(),'no actual release performed by prepare/review')
    result=dict(schema='INDEPENDENT_READONLY_EXACT_EIGHT_FINAL_MANIFEST_CURRENT_UNION_REVIEW_V1',status='ALL_CURRENT_FULL_EOF_EXACT_EIGHT_FUTURE_RELEASE_MANIFEST_PASS_NO_DELETION',manifest_pin=mp,Source_freeze_pin=sfp,protected_count=len(protected),retained_count=len(expected),candidate_count=8,candidate_logical_bytes=998909696,all3040_current_catalog_rows_verified=True,all2012_Common_rows_verified=True,all3315_science_current_and1129_inputs_verified=True,all257_v9_HF_deps_verified=True,all_actual_v9_outputs_unchanged_and_protected=True,v9_actual_unqualified_exit1_preserved=True,all_old_PACK_INITIAL_individual_PASS_preserved=True,current_material_v5_and_GENDF_v4_parser_v2_protected=True,additional_actual_v10_Source_HF_dependency_pins=extra_v10,v10_runtime_or_science_success_claimed=False,deletion_executed=False,compiler_or_numerical_business_executed=False,goal_complete=False,full_EOF_unique_verified_files=len(s.VERIFIED),full_EOF_unique_verified_bytes=sum(r['size_bytes'] for r in s.VERIFIED.values()),checks=s.CHECKS,elapsed_seconds=time.monotonic()-START,reviewer_Source_pin=s.pin(Path(__file__).absolute()))
    raw=(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode();path=OUT/'INDEPENDENT_FULL_EOF_FINAL_MANIFEST_REVIEW.json'
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644)
    with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=result['status'],review_pin=s.pin(path),protected_count=len(protected),retained_count=len(expected),full_EOF_files=result['full_EOF_unique_verified_files'],full_EOF_bytes=result['full_EOF_unique_verified_bytes'],checks=result['checks'],v10_extra_fullEOF_pins=len(extra_v10),deletion_executed=False)))

if __name__=='__main__':main()
