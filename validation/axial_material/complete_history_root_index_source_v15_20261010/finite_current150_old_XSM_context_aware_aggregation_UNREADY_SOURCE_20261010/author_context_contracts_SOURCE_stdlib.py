"""Write only Source contracts in this fresh TMP. No payload/API execution."""
import ast,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
def write(name,value):(P/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,
    free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
family=['qualified_source_manifest','host_template','engine_template','adapter','binder','old_XSM_extractor','observer_module']
write('EXACT_NEW_CONTEXT_SOURCE_ADMISSION_AND_PEER_CONTRACT.json',dict(schema='EXACT_NEW_CONTEXT_SOURCE_ADMISSION_AND_PEER_CONTRACT_V2',source_only=True,
    independent_peer_schema='INDEPENDENT_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_REVIEW_V2',
    independent_peer_status='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE',peer_flags=dict(source_only=True,all_checks_passed=True,blockers=[]),
    checks_contract='all complete numbered unique check labels; passed exact bool true; exact integer check_count',
    fullpin_keys=family,fullpin_shape=dict(path='actual absolute path',sha256='actual lowercase64hex',size_bytes='exact int',identity='seven exact ints'),
    admission_schema='ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_ENGINE_HOST_BINDER_SOURCE_ADMISSION_V2',
    admission_status='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE',all_family_pins_must_equal_actual_manifest_and_candidates=True,
    admission_same_peer_report_fullpin_mandatory=True,
    actual_Root_Source_tool_schema='ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V2',
    actual_Root_Source_tool_stdout_status='ACTUAL_COMPLETE_FINAL_AGGREGATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
    actual_tool_truth=dict(observed_terminal=True,closed=True,session_repolled_after_close=False,actual_terminal_chunk='same real terminal chunk',
        terminal_tool_return='unaltered actual tool object, exact int EXIT0 and no session_id',source_admission_pin='same actual stdout/admission fullpin'),
    previous_BUILD_schema='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1',PREP_cannot_BUILD=True,
    prior_BUILD_honest_nonzero_allowed=True,old_Q_not_transplanted=True,all_future_actualpins=None))
write('ROOT_CONTEXT_SOURCE_REQUEST_TEMPLATE.UNREADY.json',dict(schema='ROOT_ACTUAL_COMPLETE_CONTEXT_AWARE_SOURCE_BINDING_REQUEST_V2',source_only=True,
    operation=None,source_admission_pin=None,actual_Root_Source_admission_tool_return_pin=None,independent_host_binder_Source_review_pin=None,
    prior_actual_V22_build_tool_return_pin=None,actual_native_terminal_pin=None,actual_native_saved_coverage_contract_pin=None,
    actual_observation_manifest_pin=None,independent_observation_Source_admission_pin=None,
    namespaces=dict(host=None,output=None,control=None,source=None,receipts=None),
    original129_input_pins=None,additional_actual_evidence_input_pins=None,states=dict(A=None,B=None),
    complete_state_snapshot_inputs=dict(A=None,B=None),actual_context_states=None,
    new_complete_aggregation_controls_actual_run=None,new_aggregation_qualification_sha256=None,actual_scientific_qualification_sha256=None,
    actual_engine_activation=None,original_caps=caps,
    note='All None values deliberately refuse binding. Root fills only genuinely observed fullpins and exact complete lists, extraction first then aggregation.'))
write('FULL_ACTUAL_CONTEXT_AND_SNAPSHOT_EXTENSION_CONTRACT.UNREADY.json',dict(schema='FULL_ACTUAL_CONTEXT_AND_SNAPSHOT_EXTENSION_CONTRACT_V2',source_only=True,
    observer_binary_magic='AXOBSCTX',observer_stream_version_exact=2,state_order=['A','B'],all_context_events_consecutive_original_numbers=True,
    all_events_without_any_branch_selection_or_sorting=True,all_context_words_and_spans_saved_to_disk=True,
    full_native_snapshots=['all oldmacro-pre-LIBMIX','all oldmacro-LIBDEN','all postmacro-LIBMIX','all final-complete-micro'],
    macro_only_native_root_prefix=['MACROLIB'],full_micro_root_prefix=[],no_fake_MACROLIB_root_row=True,
    native_walker_parent='full frozen Root_bound_complete_native_checker.py9d8494',
    walker_unchanged_classes=['XSM','ReadOnlyFileBytes','DiskRecords'],all_native_types=[0,1,2,3,4,5,6,10,99],
    all_original_payload_words_types_counts_empty_lists_and_physical_API_orders_preserved=True,
    Source_rule_API_export_rotation_order_never_normalized=True,ASCII_not_used_or_invented=True,
    sqlite_contract=dict(schema_columns=['key','ordinal','api_key','row','micro_ordinal','macro_ordinal'],cache_mib=8,mmap_size=0,temp_store='FILE',journal_mode='DELETE'),
    input_chunk_bytes=2**20,full_context_MAT_stream_no_whole_region_dictionary=True,
    actual_context_states_exact_keys=['complete_context_pins','all_snapshot_pairs','actual_extraction_report_pin','actual_observation_manifest_pin',
        'selected_last_libmix_number','actual_extraction_coverage_contract_pin'],
    every_snapshot_exact_keys=['event','role','root_prefix','input_pin','sqlite_pin','native_pool_pin'],
    last_final_micro_pool_must_equal_full_construction_input=True,
    Root_coverage_schema='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1',
    coverage_requires_same_complete_all_context_and_snapshot_lists=True,coverage_requires_actual_closed_extraction_and_independent_saved_review=True,
    actual_extraction_report_schema='ACTUAL_COMPLETE_OBSERVED_OLD_POST_FINAL_XSM_EXTRACTION_EVIDENCE_ONLY_V1',
    required_caps=caps,full_original129_plus_all_actual_snapshot_context_pool_meta_Source_inputs=True,
    SQLite_journal_all_spools_and_open_unlinked_regular_temp_files_count_in_joint_HOCDE=True,
    A_all_handles_closed_before_B=True,all_future_observation_extraction_pins_and_new_Q=None))
write('COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS.json',dict(schema='COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS_V2',source_only=True,
    original_scopes=dict(isotopes=62,groups=370,mixes=8,declared_edits=18,moments=3,components=32,
        component_mix_values=256,FISSIONINDEX_isotope_mix_values=64,NDEL=6,delayed_fields=12,LAMBDA_values=48),
    Source_context_implemented=['full alias/mix/density fixed context','actual old STATE9/LDIFF and old STATE40 maxima',
        'full original NFISS0 and defined INDFIS initialization from actual old map, every allocation step with no zero-density filter',
        'actual full MAT membership/LSHI to MASK, original selected370 group range to MASKL',
        'LOGL from new GAF before old sparse SCAT restoration','SIGS independent from SCAT sum; SIGW diagonal; CHECK destination write order',
        'old masked NTOT0/NTOT1/H/C/OVERV/TRANC; DIFF reciprocal round trip at separate REAL32 steps',
        'all eighteen original extras, duplicates/order/presence/goto720/special names/EXIST carry forward',
        'old full fission zero initialization, literal KFIS>NFISS0*NESP, all prompt32x8 and six delayed pairs',
        'LAMBDA-D missing old slot1-only Source initialization, new slots and per-mix last write',
        'all original pre/post macro physical path/type/count order and full raw byte coupling',
        'old ENERGY/SIGNATURE unchanged, old STATE maxima/new flags/TIMESTAMP exact actual old overwrite',
        'ISOTOPESVOL last isotope write or actual pre-call MIXTURESVOL; VOLUME and all NWT last-write integrated flux',
        'all genuinely unmodified old fields raw-bit inheritance, potential producers reserved on failure',
        'all KSPH1 INRS/NBNRS true/false branch decisions and actual full2960-word SPH factors'],
    remaining_specific_unqualified_components=['fresh SIGNATURE and present PARTICLE/PARTICLE-NAM LCMPTC machine character conversion need new controls',
        'OVERV fallback DOUBLE sqrt/libm/constant expression must receive model/runtime controls; no historical bit replay claim',
        'Source undefined old tails or slots remain UNKNOWN if not overwritten by original Source',
        'instrumented actual context is a new same-input construction observation, never recovered original unsaved historical context',
        'complete production Source-to-binary linkage and fresh observer/extractor/engine malformed/math/resource controls remain unrun'],
    exact_unknown_values_not_defaulted=True,SPH_one_never_assumed=True,all_MASK_true_never_assumed=True,
    no_synthetic_ABSORPTION_no_reaction_zero_fill=True,unknown_fields_or_any_mismatch_retained_with_EXIT2=True,
    no_qualification_created=True,actual_observation=None,actual_old_XSM_extraction=None,actual_aggregation=None,new_Q=None))
text='''This sealed Source candidate does not execute material, native data readers, helpers, APIs, guards or transport.
The complete fixed parent (162 members plus its original MANIFEST) is preserved under COMPLETE_FIXED_PARENT_SOURCE.
All new derivations have complete zero-based inverse hunks and full original-byte recovery.

Root execution order:
1. Finish the separately admitted complete build and memory controls. Keep prior nonzero receipts honest; PREP is not BUILD.
2. Independently review this entire Source family. Root records actual Source-only admission and its real typed0 CLOSED tool receipt.
3. Separately admit and build the observation extension on the original A/B material decks and identical physical input. The new stream is version2.
   The only added TONDRV numerical-routine statement is the read-only AXOBS_SPH_DECISION call immediately before the original IF(NBNRS.GT.1).
   AXOBS_LIBMIX_BEGIN additionally reads original root MIXTURESVOL into a private observation array and writes its exact type/count/words.
   The original arithmetic assignments are not replaced, reordered, normalized or replayed. Preserve every material deck/log/Source/binary pin.
   Genuine same-input production and Source-to-binary linkage are Root's future actual steps, all unknown here.
4. Save the complete ordered observer manifest, every actual context file, every old/pre/post XSM and every final full micro XSM.
   Preserve all calls/events; no last-call-only material capture. All native XSM reads below are Root-only actual reads.
5. Bind operation old_XSM_extraction using the new stdlib binder in a fresh TMP, independently review all bound Source, Root install actual Source.
   Execute only the bound genuine host once. It runs the unchanged full V23 walk on every observed XSM tree, including all prefixes.
   The child intentionally exits2 evidence-only until separately qualified; genuine failure/watch/report/input-freeze evidence must be saved.
   Do not call this failure a missing payload or retry the native stage. Independently review complete saved extraction, all contexts and true terminal.
6. Form the explicit small coverage META from actual saved extraction and its independent review; preserve underlying receipts/outputs without edits.
   Bind operation context_aggregation in a separate fresh Source/namespace family using all actual snapshot pairs and context pins.
   Final states must be the same actual observed final full micro pools. The last call old/pre/post pair is selected only after validating all events.
7. Root alone runs the genuine bound aggregation host, sequential A then B, after releasing all state handles.
   All original129 pins plus every actual observation/pool/SQL/Source/META input are protected before/after at complete EOF/SHA/7ID.
   All original1800/600/512MiB/2GiB HOCDE/96GiB history/8GiB free/1thread/1child/0retry apply unchanged.
   Every spool, SQLite/journal, linked temporary file and open unlinked regular temp file remains in the real archive accounting.
8. Preserve every mismatch, Source-undefined component and unproved producer. Current candidate always exits2 on completed diagnostic evidence.
   New complete controls, independently reviewed genuinely closed execution and all component evidence are required before any future construction Q.
   This package creates neither Q nor native RAM, historical float, reaction balance, reference, AAA, ABA or science PASS.

Root Source-only binder argv (future required values are never guessed):
python3.12 -B bind_complete_context_aware_and_oldXSM_SOURCE_only.UNREADY.py --source-manifest-sha256 <actual-this-manifest-SHA> --request <actual-Root-request-path> --request-sha256 <actual-request-SHA> --output-source-dir <fresh-TMP>
Only Root runs installed Root_bound_complete_final_aggregation_genuine_host.py; future binding record supplies exact installed paths and actual pins.
Parent pure/raw protocol qualification is not the new full-prefix walker/model qualification. This author has executed only standard-library Source authors/review/seal.
'''
(P/'ROOT_ACTUAL_EXECUTION_SEQUENCE_AND_SCOPE_LIMITS.txt').write_text(text)
for p in P.glob('*.py'):ast.parse(p.read_text())
print(json.dumps(dict(source_only=True,contracts_written=5,all_candidates_UNREADY=True,all_future_actual_context_pins_None=True,
    no_material_native_API_guard_execution=True)))
