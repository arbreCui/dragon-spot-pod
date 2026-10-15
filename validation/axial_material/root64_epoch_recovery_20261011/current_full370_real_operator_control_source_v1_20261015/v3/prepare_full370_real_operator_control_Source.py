"""Source-only preparation after actual capture/post0 and exact retirement/post0."""
import argparse, ast,hashlib,json,os
from pathlib import Path
import control_source_common as c

def metadata_pin(path,wanted=None):
    p=c.pin(path,c.metadata_limit(path))
    c.require(wanted is None or p['sha256']==wanted,'preserved original metadata SHA')
    return p

def inverse(original,candidate):
    a=Path(original).read_bytes();b=Path(candidate).read_bytes();i=0
    while i<min(len(a),len(b)) and a[i]==b[i]:i+=1
    j=0
    while j<min(len(a)-i,len(b)-i) and a[-1-j]==b[-1-j]:j+=1
    ae=len(a)-j;be=len(b)-j;rebuilt=b[:i]+a[i:ae]+b[be:];c.require(rebuilt==a,'whole original complete byte inverse')
    return dict(original_full_pin=c.pin(original),candidate_full_pin=c.pin(candidate),edit_map=[dict(original_begin_byte=i,original_end_byte=ae,candidate_begin_byte=i,candidate_end_byte=be,original_bytes_hex=a[i:ae].hex(),candidate_bytes_hex=b[i:be].hex())],whole_original_reconstructed_sha256=hashlib.sha256(rebuilt).hexdigest(),complete_inverse_reconstructed_original=True)

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    for name in ('capture-post-schema','capture-post-status','retirement-post-schema','retirement-post-status'):ap.add_argument('--'+name,required=True)
    for role,prefix in (('capture',c.CAPTURE_ENTRY/'actual_capture_postverify_20261015/corrected_process_access_v2'),('retirement',c.RETIREMENT_ENTRY/'actual_retirement_postverify_20261015')):
        ap.add_argument('--'+role+'-post-review-path',default=str(prefix/'REVIEW.json'))
        ap.add_argument('--'+role+'-post-tools-path',default=str(prefix/'TRUE_TOOL_RETURNS.json'))
    args=ap.parse_args()
    c.require(args.capture_post_status.startswith('PASS') and args.retirement_post_status.startswith('PASS'),'actual positive capture and exact retirement posts required')
    c.require(not os.path.lexists(c.OUT) and not any((c.BASE/n).exists() for n in ('PLAN.json','SOURCE_REVIEW_READY.json','ORIGINAL_OPERATOR_AND_WORKER_SOURCE_INVERSE.json')),'fresh preparation/output only, no overwrite/retry')
    author_pin=metadata_pin(c.BASE/'AUTHOR_SOURCE_ONLY_FREEZE.json');author=c.read(author_pin)
    c.require(author['source_only'] is True and author['source_preparation_executed'] is False and author['compiler_executed'] is False and author['numerical_executed'] is False,'frozen unexecuted author Source')
    for pp in author['source_pins']:c.require(metadata_pin(pp['path'])==pp,'author Sources unchanged')
    capture_plan_pin=metadata_pin(c.CAPTURE_ENTRY/'PLAN.json');capture_plan=c.read(capture_plan_pin)
    c.require(capture_plan['original_caps']==c.CAPS and capture_plan['planned_actual_output_root']==str(c.CAPTURE_OUT) and len(capture_plan['complete_joint_roots'])==54,'exact completed capture54 and original caps')
    for role in ('capture','retirement'):
        prefix=(c.CAPTURE_ENTRY if role=='capture' else c.RETIREMENT_ENTRY)/('actual_'+role+'_postverify_20261015')
        for suffix in ('review','tools'):
            q=Path(getattr(args,role+'_post_'+suffix+'_path'));c.require(q.is_absolute() and '..' not in q.parts and q.is_relative_to(prefix),'actual completed post in exact own prefix')
    capture={k:metadata_pin(q) for k,q in dict(host=c.CAPTURE_OUT/'Root_actual_A1_native_vector_capture_summary.json',child=c.CAPTURE_OUT/'inventories/ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE.json',root_tools=c.CAPTURE_ENTRY/'ROOT_CAPTURE_ACTUAL24_TRUE_TOOL_RETURNS.json',post=Path(args.capture_post_review_path),post_tools=Path(args.capture_post_tools_path)).items()}
    capture_child=c.read(capture['child']);compact=capture_child['compact_vector_full_pin'];c.current(compact)
    c.require(compact['path']==str(c.CAPTURE_OUT/'inventories/A1_native_track_vectors_f4.bin') and compact['size_bytes']==104,'only exact current104B, Source prep current7 only')
    retirement={k:metadata_pin(q) for k,q in dict(receipt=c.RETIREMENT_ENTRY/'EXECUTION_RETIREMENT_RECEIPT.json',root_tools=c.RETIREMENT_ENTRY/'ROOT_RETIREMENT_EXECUTION_TRUE_TOOL_RETURNS.json',post=Path(args.retirement_post_review_path),post_tools=Path(args.retirement_post_tools_path)).items()}
    prerequisite=dict(compact_capture_prerequisite_pins=capture,literal2_retirement_prerequisite_pins=retirement,compact_native_vector_pin=compact,actual_compact_capture_report_pin=capture['child'],capture_post_schema=args.capture_post_schema,capture_post_status=args.capture_post_status,retirement_post_schema=args.retirement_post_schema,retirement_post_status=args.retirement_post_status,inherited_complete_joint_roots=capture_plan['complete_joint_roots'])
    c.check_finite(prerequisite);retire=c.read(retirement['receipt'])
    retire_plan_pin=metadata_pin(c.RETIREMENT_ENTRY/'PLAN.json');retire_plan=c.read(retire_plan_pin);retire_sf_pin=metadata_pin(c.RETIREMENT_ENTRY/'RETIREMENT_SOURCE_ONLY_FREEZE.json');retire_sf=c.read(retire_sf_pin)
    c.require(retire['plan_pin']==retire_plan_pin and retire['source_pin']==retire_plan['retirement_source_pin'] and retire_plan['original_capture_plan_pin']==capture_plan_pin and retire_plan['complete_joint_roots']==capture_plan['complete_joint_roots'] and retire_sf['control_plan_pin']==retire_plan_pin and retire_sf['selected_retirement_source_pin']==retire['source_pin'],'exact actual retirement-only v3 Source/plan/SF closure of original capture v2')
    historical_targets=retire['actual_released_pins']
    c.require(historical_targets==capture_plan['target_pins'] and {p['path'] for p in historical_targets}==c.RETIRED_PATHS,'exact two old A1 producer pins historical only')
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
    case_C=case['materials']['temperature_C_in_every_zone'];case_offset=case['materials']['kelvin_offset'];c.require(case_C==dict(clad_and_gap=620,fuel_and_hole=750,sodium=475) and case_offset==273.15,'unchanged explicit formal Celsius and Kelvin offset')
    case_K={k:float(v+case_offset) for k,v in case_C.items()};c.require(case_K==dict(clad_and_gap=893.15,fuel_and_hole=1023.15,sodium=748.15),'explicit formal C to K mapping; no saved REAL32 selection inference')
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
    native_archive=capture_plan['original_native_pairs'][0]['archive_pin'];c.current(native_archive)
    c.require(native_archive['path']==str(c.ART/'axial-material-new-REAL64-native-warm-A-20261012-v3/A/new_native_A.xsm') and native_archive['sha256']=='172ff389a42e6f573143e2fd1650e04fcfc5e7fe30f36e5b29bf902255e46bcc' and native_archive['size_bytes']==156880856,'current preserved original A1 XSM, no decode here')
    selected['current_original_A1_native_archive_pin']=native_archive
    science=[mother[k] for k in ('observed_final55_SQLite_pin','observed_final55_pool_pin','current_original_radial_track_pin')]+[new,compact,native_archive]
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
    roots=list(capture_plan['complete_joint_roots'])+[str(c.TOP),str(c.OUT)]
    c.require(len(roots)==56 and len(set(roots))==56 and all(not Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a!=b),'inherit completed capture54 and append whole fullTOP/newOUT56 without reset')
    worker=metadata_pin(c.BASE/'run_full370_real_operator_control.py')
    guard=metadata_pin(c.BASE/'run_guarded_full370_real_operator_control.py')
    helper=capture_plan['original_v6_vector_helper_pin'];c.exact(helper)
    helper_original=capture_plan['original_v6_vector_helper_provenance_pin'];c.require(metadata_pin(helper_original['path'])==helper_original and helper['sha256']==helper_original['sha256'] and helper['size_bytes']==helper_original['size_bytes'],'whole unchanged original v6 helper provenance')
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
    proof_rows=[dict(original_full_pin=metadata_pin(c.TOP/n),candidate_full_pin=metadata_pin(c.BASE/n),complete_byte_inverse=inverse(c.TOP/n,c.BASE/n)) for n in ('control_source_common.py','run_full370_real_operator_control.py','prepare_full370_real_operator_control_Source.py','run_guarded_full370_real_operator_control.py','write_once_full370_real_operator_control_SF_HF_CLI.py')]
    original_worker=(c.TOP/'run_full370_real_operator_control.py').read_bytes();worker_bytes=Path(worker['path']).read_bytes();old_begin=original_worker.index(b'    angles,angle_rows=helpers.small_vectors(');old_end=original_worker.index(b'    support=sys.modules',old_begin);new_begin=worker_bytes.index(b'    # New actual capture preserves');new_end=worker_bytes.index(b'    support=sys.modules',new_begin)
    c.require(worker_bytes[:new_begin]+original_worker[old_begin:old_end]+worker_bytes[new_end:]==original_worker,'reverse only compact input block equals whole original v1 worker; all math unchanged')
    for pp in author['source_pins']:ast.parse(c.exact(pp),filename=pp['path'])
    pp_inverse=c.write(c.BASE/'ORIGINAL_OPERATOR_AND_WORKER_SOURCE_INVERSE.json',dict(schema='FULL370_COMPACT_NATIVE_INPUT_WHOLE_OPERATOR_AND_WORKER_INVERSE_V1',whole_operator_copy_full_pin=copied,whole_original_operator_Source_pin=original,whole_operator_copy_equals_original=True,whole_original_v6_helper_copy_pin=helper,whole_original_v6_helper_provenance_pin=helper_original,complete_source_inverses=proof_rows,compact_input_only_whole_worker_reverse_equals_original=True,mathematical_fixture_operator_calls_and_checks_unchanged=True,scientific_payload_read=False,business_executed=False,numerical_executed=False,compiler_executed=False,files_deleted=False,**c.FALSE))
    proof_values=list(capture.values())+list(retirement.values())+[retire_plan_pin,retire_sf_pin]
    inherited_metadata=c.unique(capture_plan['explicit_cumulative_metadata_file_pins']+proof_values+[author_pin,mother_pin,formal_plan_pin,capture_plan_pin,pp_inverse]+[selected[k] for k in ('current_case_spec_pin','current_prepared_pin','protected_formal_and_producer_plan_pin')]+retire_plan['retirement_only_selected_Source_and_metadata_pins'])
    for pp in inherited_metadata:c.current(pp)
    plan=dict(schema='FULL370_REAL_CURRENT_MATERIAL_OPERATOR_CONTROL_SOURCE_ONLY_PLAN_V1',source_only=True,
        planned_actual_output_root=str(c.OUT),original_caps=c.CAPS,complete_joint_roots=roots,
        inherited_capture_plan_pin=capture_plan_pin,
        explicit_cumulative_metadata_file_pins=inherited_metadata,
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
        actual_control_report_pin=None,historical_retired_A1_SQLite_pin=historical_targets[0],historical_retired_A1_pool_pin=historical_targets[1],current_saved_final55_total_scope='Exact current final55 NTOT0 words promoted and repeated over48 layers for one component control; no claimed temperature/physics remapping',current_case_temperature_C=case_C,current_case_kelvin_offset=case_offset,current_formal_parameter_temperature_K=case_K,formal_C_to_K_parameter_mapping_verified=True,stored_native_REAL32_temperature_selection_qualified=False,native_AxMatTone_temperature_mapping_qualified=False,current_SPH_MASK_context_applied=False,finite18_replayed=False,temperature_interpolation_replayed=False,protected_formal_case_or_inputs_rewritten=False,**selected,**prerequisite,**c.FALSE)
    for k in ('observed_final55_SQLite_pin','observed_final55_pool_pin','current_original_radial_track_pin'):plan[k]=mother[k]
    dependencies=c.unique(author['source_pins']+support_dependencies+[helper,origin['library_pin'],kernel_origin,
        origin['actual_build_report_pin']]+origin['complete_source_pins']+[r['pin'] for r in imports]
        +science+list(selected.values())+proof_values+[author_pin,mother_pin,formal_plan_pin,capture_plan_pin,original,pp_inverse,helper_original]+[pp for pp in capture_plan['source_dependency_pins'] if pp['path'] not in c.RETIRED_PATHS]+retire_plan['retirement_only_selected_Source_and_metadata_pins'])
    c.require(all(pp['path'] not in c.RETIRED_PATHS for pp in dependencies+science),'no retired A1 pair live dependency')
    plan['source_dependency_pins']=dependencies
    pp=c.write(c.BASE/'PLAN.json',plan)
    ready=c.write(c.BASE/'SOURCE_REVIEW_READY.json',dict(schema='FULL370_REAL_OPERATOR_CONTROL_SOURCE_REVIEW_READY_V1',
        source_only=True,source_preparation_only=True,compiler_executed=False,numerical_executed=False,
        worker_source_pin=worker,host_source_pin=guard,plan_pin=pp,author_source_freeze_pin=author_pin,
        whole_operator_copy_equals_original=True,selected_Source_and_metadata_pins=c.unique(author['source_pins']+inherited_metadata+[pp_inverse,formal_plan_pin,original,helper_original]+[pp for pp in capture_plan['source_dependency_pins'] if pp['path'] not in c.RETIRED_PATHS]+retire_plan['retirement_only_selected_Source_and_metadata_pins']),original_Source_inverse_proof_pin=pp_inverse,actual_completed_prerequisite_pins=dict(capture=capture,retirement=retirement),business_executed=False,files_deleted=False,**c.FALSE))
    print(json.dumps(dict(status='FULL370_REAL_OPERATOR_CONTROL_SOURCE_PREPARED_ONLY',ready_pin=ready,
        compiler_executed=False,numerical_executed=False,**c.FALSE)),flush=True)

if __name__=='__main__':main()
