"""Source-only preparation after ACTUAL finite18 report and postreview exist."""
import argparse, json
from pathlib import Path
import control_source_common as c

def metadata_pin(path,wanted=None):
    p=c.pin(path,c.metadata_limit(path))
    c.require(wanted is None or p['sha256']==wanted,'preserved original metadata SHA')
    return p

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--finite-post-schema',required=True)
    ap.add_argument('--finite-post-status',required=True)
    args=ap.parse_args()
    # The actual postreview schema/status are supplied only after the sole
    # verifier creates them. No anticipated post status or PF is fabricated.
    c.require(args.finite_post_status.startswith('PASS'),'actual positive finite18 post status required')
    c.require(not any((c.BASE/n).exists() for n in ('PLAN.json','SOURCE_REVIEW_READY.json')),
        'fresh preparation only, no overwrite/retry')
    author_pin=metadata_pin(c.BASE/'AUTHOR_SOURCE_ONLY_FREEZE.json');author=c.read(author_pin)
    c.require(author['source_only'] is True and author['source_preparation_executed'] is False
        and author['compiler_executed'] is False and author['numerical_executed'] is False,
        'frozen unexecuted author package')
    for p in author['source_pins']:c.require(metadata_pin(p['path'])==p,'author Sources unchanged')
    finite_plan_pin=metadata_pin(c.FINITE_ENTRY/'PLAN.json');finite=c.read(finite_plan_pin)
    c.require(finite['original_caps']==c.CAPS and finite['planned_actual_output_root']==str(c.FINITE_OUT),
        'exact finite18 completed cohort and original caps')
    proof={k:metadata_pin(p) for k,p in dict(
        host=c.FINITE_OUT/'Root_actual_eight_fuel_finite18_SCAT_summary.json',
        child=c.FINITE_OUT/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json',
        root_tools=c.FINITE_ENTRY/'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json',
        post=c.FINITE_ENTRY/'actual_postverify_20261015/REVIEW.json',
        post_tools=c.FINITE_ENTRY/'actual_postverify_20261015/TRUE_TOOL_RETURNS.json').items()}
    prerequisite=dict(finite18_prerequisite_pins=proof,finite18_post_schema=args.finite_post_schema,
        finite18_post_status=args.finite_post_status)
    c.check_finite(prerequisite)
    mother_pin=metadata_pin(c.V6/'PLAN.json');mother=c.read(mother_pin)
    formal_plan_pin=metadata_pin(c.CORE/'CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json')
    formal=c.read(formal_plan_pin);attestations=[];selected={}
    for key in ('current_case_spec_pin','current_prepared_pin','protected_formal_and_producer_plan_pin'):
        old=formal[key];new=metadata_pin(old['path'],old['sha256']);selected[key]=new
        attestations.append(dict(role=key,original_saved_pin=old,current_fullEOF_metadata_pin=new,
            old_history_rewritten=False,scientific_payload_read=False))
    c.require(selected['current_case_spec_pin']['sha256']=='fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16',
        'actual current fbe336 formal case, not old ac3e')
    case=c.read(selected['current_case_spec_pin']);prepared=c.read(selected['current_prepared_pin'])
    cfg=prepared['production_config']
    c.require(case['cases']['AAA']==['A','A','A'] and cfg['cells_per_zone']==16 and cfg['sn']==32
        and cfg['zone_height_cm']==50. and cfg['rank']==1 and case['geometry']['physical_z_edges_cm']==[0,50,100,150],
        'unchanged actual H150/48/SN32/rank1/AAA formal metadata')
    # The small axial XSM is science: retain its original SHA as provenance,
    # attest ONLY current7 here, and demand the actual parent whole hash later.
    old=formal['current_axial_track_pin'];q=Path(old['path']);s=q.lstat();new=dict(old,identity=c.identity(s))
    c.require(new['identity'][1:]==old['identity'][1:] and new['size_bytes']==s.st_size,
        'only observed device epoch changes for the retained original axial track')
    c.current(new);selected['current_axial_track_pin']=new
    attestations.append(dict(role='current_axial_track_pin',original_saved_pin=old,
        current_metadata_attested_pin=new,whole_body_SHA_recomputed_here=False,
        original_SHA_retained_not_newly_proved=True,actual_parent_fullEOF_SHA_required=True,old_history_rewritten=False))
    science=[mother[k] for k in ('observed_final55_SQLite_pin','observed_final55_pool_pin',
        'native_A1_SQLite_pin','native_A1_pool_pin','current_original_radial_track_pin')]+[new]
    for p in science:c.current(p)
    imports=[r for r in mother['explicit_import_bindings'] if r['module'] not in ('native_layered_zonal','actual_track_white_transfer')]
    copied=metadata_pin(c.BASE/'current_formal_full370_ray_operator.py')
    original=metadata_pin(c.CORE/'current_formal_full370_ray_operator.py')
    c.require(copied['sha256']==original['sha256'] and copied['size_bytes']==original['size_bytes'],
        'whole unchanged WholeRayOperator Source copy')
    imports.append(dict(module='current_formal_full370_ray_operator',pin=copied))
    for row in imports:c.exact(row['pin'])
    kernel_origin=mother['actual_kernel_origin_pin'];origin=c.read(kernel_origin)
    c.require(origin['original_caps']==c.CAPS and origin['library_pin']==mother['actual_kernel_library_pin'],
        'existing actual kernel origin/library only')
    roots=list(finite['complete_joint_roots'])
    c.require(str(c.FINITE) in roots and str(c.FINITE_OUT) in roots,
        'upstream finite Source and completed output already in cumulative roots')
    roots+= [str(c.BASE),str(c.OUT)]
    c.require(len(roots)==len(set(roots)) and all(not Path(a).is_relative_to(Path(b))
        for a in roots for b in roots if a!=b),'append two disjoint roots without reset')
    worker=metadata_pin(c.BASE/'run_full370_real_operator_control.py')
    guard=metadata_pin(c.BASE/'run_guarded_full370_real_operator_control.py')
    helper=metadata_pin(c.V6/'run_one_actual_track_component.py')
    support_pin=mother['original_support_Source_pin']
    # These literal original Source hashes/path roles are already in V6's HF.
    mother_hf=c.read(metadata_pin(c.V6/'COMPLETE_ONE_ACTUAL_TRACK_COMPONENT_CONTROL_HOST_SOURCE_ONLY_FREEZE.json'))
    wanted={str(mother[k]['path']) for k in ('original_Common_Source_pin','original_support_Source_pin','original_bounded_Source_pin')}
    wanted.update(str(c.REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'/n)
        for n in ('prepare_qualified_AB_source_factor_production.py','runtime/production_runner.py'))
    wanted.update(str(p) for p in (c.R/'validation/axial_material/qualify_refined_AAA_layered_full.py',
        c.R/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py'))
    support_dependencies=[p for p in mother_hf['dependencies'] if p['path'] in wanted]
    c.require({p['path'] for p in support_dependencies}==wanted,'complete unchanged original guard support Source roles')
    for p in support_dependencies:c.exact(p)
    plan=dict(schema='FULL370_REAL_CURRENT_MATERIAL_OPERATOR_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,
        planned_actual_output_root=str(c.OUT),original_caps=c.CAPS,complete_joint_roots=roots,
        inherited_complete_joint_roots=finite['complete_joint_roots'],inherited_finite18_plan_pin=finite_plan_pin,
        explicit_cumulative_metadata_file_pins=c.unique(finite['explicit_cumulative_metadata_file_pins']
            +list(proof.values())+[author_pin,mother_pin,formal_plan_pin]),
        original_Common_Source_pin=mother['original_Common_Source_pin'],original_support_Source_pin=support_pin,
        original_bounded_Source_pin=mother['original_bounded_Source_pin'],original_v6_vector_helper_pin=helper,
        exact_v2_source_root=str(c.CORE),explicit_import_bindings=imports,
        actual_kernel_origin_pin=kernel_origin,actual_kernel_library_pin=origin['library_pin'],
        actual_kernel_build_report_pin=origin['actual_build_report_pin'],complete_kernel_source_pins=origin['complete_source_pins'],
        scientific_input_current7_pins=science,formal_metadata_current_attestations=attestations,
        worker_source_pin=worker,host_source_pin=guard,physical_checks=formal['physical_checks'],
        offset_order=32,working_group_chunk=1,boundary_model='GEOMETRIC_LAYER_LOCAL_WHITE',
        source_fixture_formula='a=1+(r+1)/32+(g+1)/2048;c0=a;cm=a*(m+1)/512;t=(2*j+1-48)/48 for m=2,5,7 else1;R order from native_full_angular_p2',
        new_control_reserved_bytes=260858880+22319392+8*2**20,whole_white_cache_payload_bytes=260858880,
        control_reservation_components=dict(white_cache_array_payload=260858880,
            complete_saved_array_payload=22319392,NPZ_headers_new_metadata_and_publication_reserve=8*2**20),
        signed_current_scope='TWO_END_FACES_ONLY_NO49FACE_PROFILE',formal_SN32_equivalence_claimed=False,
        mathematical_operator_Source_copy_pin=copied,original_mathematical_operator_Source_pin=original,
        actual_control_report_pin=None,**selected,**prerequisite,**c.FALSE)
    for k in ('observed_final55_SQLite_pin','observed_final55_pool_pin','native_A1_SQLite_pin',
        'native_A1_pool_pin','current_original_radial_track_pin'):plan[k]=mother[k]
    dependencies=c.unique(author['source_pins']+support_dependencies+[helper,origin['library_pin'],kernel_origin,
        origin['actual_build_report_pin']]+origin['complete_source_pins']+[r['pin'] for r in imports]
        +science+list(selected.values())+list(proof.values())+[author_pin,mother_pin,formal_plan_pin,finite_plan_pin,original])
    plan['source_dependency_pins']=dependencies
    pp=c.write(c.BASE/'PLAN.json',plan)
    ready=c.write(c.BASE/'SOURCE_REVIEW_READY.json',dict(schema='FULL370_REAL_OPERATOR_CONTROL_SOURCE_REVIEW_READY_V1',
        source_only=True,source_preparation_only=True,compiler_executed=False,numerical_executed=False,
        worker_source_pin=worker,host_source_pin=guard,plan_pin=pp,author_source_freeze_pin=author_pin,
        whole_operator_copy_equals_original=True,finite18_actual_completed_prerequisites=proof,**c.FALSE))
    print(json.dumps(dict(status='FULL370_REAL_OPERATOR_CONTROL_SOURCE_PREPARED_ONLY',ready_pin=ready,
        compiler_executed=False,numerical_executed=False,**c.FALSE)),flush=True)

if __name__=='__main__':main()
