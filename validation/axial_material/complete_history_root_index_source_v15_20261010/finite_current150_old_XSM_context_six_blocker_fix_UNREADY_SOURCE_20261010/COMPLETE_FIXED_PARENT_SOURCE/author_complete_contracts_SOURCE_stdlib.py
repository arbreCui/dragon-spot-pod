"""Only finite Source/small META copies and candidate contracts; no payload/API."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

P=Path(__file__).resolve().parent
def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(path):
    path=Path(path);s=path.lstat()
    assert path.is_absolute()and stat.S_ISREG(s.st_mode)and s.st_nlink==1
    with path.open('rb')as stream:
        assert identity(os.fstat(stream.fileno()))==identity(s)
        raw=stream.read();assert identity(os.fstat(stream.fileno()))==identity(s)
    assert identity(path.lstat())==identity(s)
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity=identity(s))
def write(name,value):
    (P/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,
    history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
base=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
native_source=base/'actual_complete_native_AB_persisted_XSM_ASCII_v23_sources/Root_bound_complete_native_checker.py'
native_META=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-native-AB-persisted-XSM-ASCII-output-v23-20261010/ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json')
copies=P/'FINITE_ACTUAL_NATIVE_V23_SOURCE_META';copies.mkdir(exist_ok=True)
copied=[]
for path in (native_source,native_META):
    before=pin(path);raw=path.read_bytes();assert pin(path)==before
    assert len(raw)<100000
    (copies/path.name).write_bytes(raw)
    copied.append(dict(original=before,copy=pin(copies/path.name)))
native_tree=ast.parse((copies/native_source.name).read_bytes())
native=json.loads((copies/native_META.name).read_bytes())
assert native['native_persisted_XSM_value_bits_verified']is True
assert native['all_complete_state_scope_retained']is True
assert [s['state']for s in native['states']]==['A','B']
for s in native['states']:
    for key,counts in(('complete_MACROLIB',(19619,19990,2264113)),('complete_MICROLIB',(23895,24842,18670730))):
        row=s[key]
        assert (row['records'],row['physical_headers_including_all_closes'],row['numeric_components'])==counts
        assert row['all_persisted_native_value_bits_equal_ASCII']is True
        assert row['native_physical_preorder_equal_original_ASCII']is True
        assert row['native_XSM_API_export_preorder_equal_original_ASCII']is False
        assert row['original_ASCII_export_omitted_native_zero_length_records']==0
write('ACTUAL_FINITE_V23_NATIVE_LAYOUT_SOURCE_META.json',dict(schema='FINITE_ACTUAL_SAVED_NATIVE_V23_LAYOUT_SOURCE_META_ONLY_V1',source_only=True,
    complete_original_copies=copied,Source_fields=dict(SQL_columns=['key','ordinal','api_key','row','micro_ordinal','macro_ordinal'],
    pool='complete_native_original_value_bytes.bin',sqlite='complete_native_original_path_index.sqlite',
    state_folder_order=['A','B'],paired_pin_capture_required_from_Root=True,
    physical_slots='complete_native_physical_directory_slots.jsonl',logical_inventory='complete_native_logical_record_inventory.jsonl',
    API_order='complete_native_xsmnxt_export_record_order.jsonl'),
    actual_saved_metadata_scope_only=True,actual_closed_terminal_or_RSS_verified_here=False,
    actual_native_independent_review_pin=None,actual_native_terminal_pin=None,
    Source_binary_linkage_qualified=False,historical_RAM_bits_verified=False,aggregate_or_science_qualified=False))

request=dict(schema='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_BINDING_REQUEST_V1',source_only=True,
    source_admission_pin=None,actual_Root_Source_admission_tool_return_pin=None,
    independent_host_binder_Source_review_pin=None,prior_actual_V22_build_tool_return_pin=None,
    actual_native_terminal_pin=None,actual_native_saved_coverage_contract_pin=None,
    original129_input_pins=None,additional_actual_evidence_input_pins=None,
    states={'A':{'sqlite_pin':None,'native_pool_pin':None},'B':{'sqlite_pin':None,'native_pool_pin':None}},
    namespaces={k:None for k in('host','output','control','source','receipts')},
    new_complete_aggregation_controls_actual_run=None,new_aggregation_qualification_sha256=None,
    actual_scientific_qualification_sha256=None)
write('ROOT_SOURCE_REQUEST_TEMPLATE.UNREADY.json',request)
write('EXACT_SOURCE_ADMISSION_AND_PEER_CONTRACT.json',dict(schema='COMPLETE_FINAL_AGGREGATION_SOURCE_SCOPE_CONTRACT_V1',source_only=True,
    peer_schema='INDEPENDENT_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_REVIEW_V1',
    peer_status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',peer_required=dict(source_only=True,all_checks_passed=True,blockers=[],
        checks='unique nonempty check labels, each passed exact bool true',check_count='exact integer equals full checks length'),
    five_fullpin_fields=['qualified_source_manifest','host_template','engine_template','adapter','binder'],
    fullpin_shape={'path':'absolute str','sha256':'lowercase64 str','size_bytes':'nonnegative exactint','identity':'7 nonnegative exactints, nlink1, size matches'},
    Root_admission_schema='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V1',
    Root_admission_status='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE',
    actual_admission_tool_schema='ROOT_ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1',
    actual_admission_output_status='ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
    actual_tool_required={'observed_terminal':True,'closed':True,'session_repolled_after_close':False,
        'actual_terminal_chunk':'equals original terminal chunk_id','terminal_tool_return':'untouched actual dict; exit exactint; no session_id'},
    source_admission_tool_exit=0,prior_BUILD_schema='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1',
    prior_BUILD_exit='any honest exactint; PREP cannot substitute',
    normalized_native_terminal_schema='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVED_TERMINAL_FOR_AGGREGATION_V1',
    normalized_native_coverage_schema='ROOT_ACTUAL_COMPLETE_NATIVE_SAVED_POOL_COVERAGE_FOR_AGGREGATION_V1',
    normalized_native_wrapper_preserves_original_receipt_and_output=True,normalized_native_terminal_exit='honest exactint, no Source-binlink invented data gate',
    original129_preserved_in_order=True,additional_actual_paired_pool_and_SQlite_pins_required=True,
    all_future_actual_source_install_engine_host_controls_qualification=None,
    actual_construction_error_or_mismatch_not_promoted_to_PASS=True))

families=[
    dict(family='ALL_ORIGINAL_RECORDS',scope='all original23895 root micro rows including19619 macro rows; all headers/orders remain original inputs',
        known='full adapter inventory iter_raw EOF SHA plus kind/count/path key type/physical/API/micro/macro ordinal',
        unproved='ROOT original RAM and compilation ownership; final Producer unknown never filtered'),
    dict(family='BINDING62',scope='all62 isotope slots and original12byte aliases, own ISOTOPESMIX/DENS',
        known='existing saved native row/pool and unchanged LIBIPS adapter',unproved='historical caller state/masking'),
    dict(family='SCAT_SIGS_SIGW_CHECK',scope='all370x370x8x3 mathematical cells and actual compressed SCAT/NJJS/IJJS/IPOS, SIGS, diagonalSIGW and CHECK',
        known='separate REAL32 per multiplication/addition with all isotope/destination/source order',
        unproved='MASKK/MASK/MASKL/LALL actual old macro inheritance, original compiled FMA/reassociation'),
    dict(family='SCALARS_EXTRAS',scope='NTOT0/1 STRD→DIFF H/C factors OVERV TRANC plus all18 declared original8byte names',
        known='actual field presence; density own-order, ordinary extra final overwrite, OVERV fallback final dominates extras',
        unproved='old STATE9 LDIFF, old EXIST/presence, actual masks/times; special BST/CST/NW/H retained with own producer'),
    dict(family='FISSION_PROMPT_DELAYED',scope='all64 FISSIONINDEX slots binding,32 components,all256/group; prompt and all6 NUSIGFxx plus6 CHIxx',
        known='final original64 checked as input consistency, mapped prompt/first-spectrum delayed model with full known masks',
        unproved='old NFISS0/NFISSI/INDFIS and initial ZNUS/ZCHI; literal KFIS.GT.NFISS0*NESP; other-spectrum delayed retained unknown'),
    dict(family='LAMBDA',scope='all48=6delayed x8slots',known='slot-wise original mix loop last present micro LAMBDA write',
        unproved='old decay table/LSAME context and absent values; no density average, no invented0'),
    dict(family='VOLUMES_AND_FLUX',scope='all62 ISOTOPESVOL,8 MIXTURESVOL/VOLUME,370x8 FLUX-INTG/P1 NWT0/1',
        known='last isotope mix assignment and last present correct-length NWT write times actual modeled volume; non370 NWT Source skip retained',
        unproved='MIXTURESVOL-only values are inputs, cannot self-prove volume producer'),
    dict(family='METADATA_SPHand_STATE',scope='all40 state words, SHIBA STATE/EPS/TCEPS, ENERGY371/TIMESTAMP/SPH/particle words and every other original macro record',
        known='original words/types/presence fully retained; explicit fresh signature/energy and direct extra/particle numeric copy models',
        unproved='old maxima/TMPDAY/trackingMAT/actual SPH, char1 projection padding and Source-binlink; no final self-prove')]
write('COMPLETE_ENGINE_SCOPE_AND_UNVERIFIED_COMPONENTS.json',dict(schema='COMPLETE_FINAL_MICRO_MACRO_ENGINE_CONSERVATIVE_SCOPE_V1',source_only=True,
    original_caps=caps,states=['A','B'],Source_fact_parents=[319,253,359],families=families,
    no_reaction_selection=True,no_missing_zero_fill=True,no_SPH_one=True,no_forced_actual_MASK=True,
    actual_fixed_native_success_is_not_aggregation_qualification=True,
    final_constructive_model_is_not_historical_LIBDEN_bit_replay=True,
    normal_completed_diagnostic_exit=2,unexpected_failure_exit=1,success_qualification_exit_available=False,
    new_pure_full_fresh_controls_actual_run=None,aggregate_or_science_qualification=None))

hooks=json.loads((P/'COMPLETE_OBSERVATION_FORTRAN_SOURCE_INVERSE.json').read_bytes())
insertions=[]
for derivative in hooks['complete_derivatives']:
    for h in derivative['complete_zero_based_hunks']:
        insertions.append(dict(source=derivative['original'],candidate=derivative['candidate'],
            original_one_based_insert_before=h['old_start0']+1,full_new_lines=h['new_full_lines']))
write('EXACT_READONLY_OBSERVATION_PRODUCTION_EXTENSION_CONTRACT.json',dict(schema='ROOT_FUTURE_COMPLETE_OLD_STATE_AND_MAT_SPH_OBSERVATION_EXTENSION_V1',source_only=True,
    observation_module=pin(P/'AXMAT_OBSERVATION_MOD.UNREADY.f90'),context_extractor=pin(P/'extract_actual_observation_context.UNREADY.py'),
    exact_original_source_insertion_points=insertions,original_numeric_and_control_statements_bytes_unchanged=True,
    original_material_A_B_decks_and_same_physical_inputs_required=True,
    event_order='all event numbers per actual state process, no omitted call, no sorting/renumbering',
    events=['LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER',
        'TONDRV_AFTER_REAL_MAT_ELIMINATION','TONDRV_ACTUAL_FINAL_LIBMIX_MASK','TONSPH_BEFORE_ACTUAL_TONCMI','TONDRV_FINAL_AFTER_SHIBA'],
    oldmacro_snapshots='fresh LCMEQU disk-backedXSM before LIBMIX and after LIBDEN old-state reads; full type/length/word tree, not final substitute',
    fission_actual='defined pre-mutation old NFISS0/NFISSI and8 x actualoldslots INDFIS',
    flags_actual='NBMIX/NGROUP/NBISO/NL/NDEL/NESP/NED/ITRANC/MAXNFI/NPART/LSAME/ITSTMP/TMPDAY/STERN/MASKK/LALL/LDIFF/MASK/MASKL',
    tracking_actual='all actual MAT NREG cells after elimination,62 MIX/LSHI/DEN, KSPH/ITRANZ/IPROB/IGRMIN/MAX',
    SPH_actual='every actual INRS TONCMI call,62 MASKI and all8x370 REAL32 factors, no1 assumption',
    post_actual='complete post-LIBMIX macro plus complete final TONDRV micro including SHIBA state',
    byte_format='AXOBSCTX then version/event/libmix/labelsize little INTEGER32, label ASCII, exact argument words; REAL32 saved bits not converted JSON floats',
    LOGICAL_encoding='explicit observer MERGE1/0, not a claim of original LOGICAL storage bits',
    snapshot_character_storage='LCMEQU originalword copy; LCMEXP binary strncpy not accepted as arbitrary character evidence',
    absence_rule='old macro absent when actualMASKKfalse; observe actualdirectory length/type, never invent snapshot',
    full_XSM_extraction_extension_required='reuse exact frozen XSM/ReadOnlyFileBytes/DiskRecords complete walk path in a fresh Source-only derivative; prefix macro root explicitly, no ASCII or invented root node; yet unimplemented here',
    missing_implementation=['complete old-XSM extraction entry/independent controls/genuine binding','context-aware engine old-inheritance and initial fission replay','same-input instrumented fresh production genuinehost/build linkage'],
    no_prediction_actual_resource_PASS=True,original_caps=caps,Root_sequential_only=True,
    observation_compile_or_run=None,oldstate_actual_capture=None,Source_binary_linkage_qualified=False,
    actual_material_outputs_byte_unchanged_verified=False,scientific_qualification_created=False))

write('REQUIRED_NEW_ROOT_ACTUAL_CONTROLS_BEFORE_AGGREGATION_Q.json',dict(schema='COMPLETE_AGGREGATION_FUTURE_ACTUAL_CONTROL_CONTRACT_V1',source_only=True,
    arithmetic=['all RN-even ties including subnormal/normal carry/overflow; signed zeros; sqrt exact midpoint; exact Source constants; no FMA assumption'],
    full_scope=['62aliases/ownmixdensity including empty aliases','370x8x3 complete sparse SCAT including diagonal and CHECK order',
        '18names including duplicate/presence/last overwrites','64 index/32component/all256 prompt and12 delayed records and48lambda',
        'allVolumes/lastNWT/energy fallback/40state/SHIBA/TIMESTAMP/SPH'],
    rejects=['bool/equalfloat pins andcaps','changed or truncated full paired SQL/pool','missing mandatory operand','unknown type/count/key kind',
        'duplicate or out-of-order actual event','missingoldmacro/MAT/SPH/flags cannotbePASS','malformed sparse ranges/fullcounts',
        'all nonfinite/overflow preserved as actualfailure','foreign/aliased output/parents','guard MRO/ownchild/command/PID/cap override'],
    actual_failure_paths=['all mismatches disk-retained nonzero','partial phase keepsfulloriginalscope classifiedunknown',
        'per-state handlesclosed before next state','timeout/RSS/archive/free/history cleanup withzero retry'],
    inherited_raw5positive10reject='saved separate software scope only',actual_controls_run=None,new_qualification=None,
    every_new_control_requires_original_genuine_watch_and_complete_saved_review=True))
print(json.dumps(dict(source_only=True,finite_native_Source_META_copies=copied,
    complete_family_contracts=len(families),future_root_pins_unknown=True,material_or_candidate_API_executed=False)))
