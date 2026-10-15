"""UNREADY request constructors, explicit B role and complete latest prefix.

No main, writes, imports of candidate science modules, Source-generation or
admission. A separately reviewed Root host supplies already verified metadata
and pins; it preserves child extraction/construction exit2 as evidence-only.
"""
from copy import deepcopy
from pathlib import Path

B_SCOPE='ONE_CURRENT_ORIGINAL_B_MATERIAL_CONSTRUCTION_FULL_CONTEXT_NOT_A_RELABELLING'

def require(ok,message):
    if type(ok)is not bool or not ok:raise ValueError(message)

def unique(pins):
    table={}
    for p in pins:
        require(p['path']not in table or table[p['path']]==p,'conflicting fullPF role')
        table[p['path']]=p
    return list(table.values())

def extract_request(binding,binding_pin,manifest,manifest_pin,source_freeze_pin,
                    output_directory,complete_latest_roots,explicit_metadata_pins,
                    complete_fixed_pins):
    require(binding['state']=='B'and manifest['state_order']==['B']and
      set(manifest['states'])=={'B'}and manifest['observation_scope']==B_SCOPE and
      manifest['current_B_case_input_binding_pin']==binding_pin and
      manifest['current_case_spec_pin']==binding['current_case_spec_pin'],
      'same genuine current B input and whole observation, no A-to-B global substitution')
    state=manifest['states']['B']
    require(state['actual_observation_directory']==binding['actual_observation_directory']and
      state['actual_native_cwd']==binding['actual_native_cwd']and
      state['current_B_case_input_binding_pin']==binding_pin and
      len(state['complete_context_pins'])==55 and len(state['complete_state_snapshot_inputs'])==8,
      'complete actual B55context/8tree with separate native cwd/output directory')
    owning=Path(binding['actual_output_root']);prefix=binding['complete_latest_prefix_roots']
    require(len(prefix)>=64 and len(complete_latest_roots)==len(set(complete_latest_roots))and
      complete_latest_roots==prefix+[str(owning)]and owning.is_absolute()and
      str(owning)==binding['actual_output_root']and
      Path(output_directory)==owning/'evidence'/'extract'and str(Path(output_directory))==output_directory,
      'whole latest64 or later prefix plus exact next B root/evidence/extract; no reset')
    return dict(schema='CURRENT_B_MATERIAL_LINEAGE_EVIDENCE_REQUEST_V1',operation='extract',
      output_directory=output_directory,owning_host_output_directory=str(owning),current_case_spec_pin=binding['current_case_spec_pin'],
      current_B_case_input_binding_pin=binding_pin,actual_observation_manifest_pin=manifest_pin,
      complete_source_freeze_pin=source_freeze_pin,original_caps=binding['original_caps'],
      joint_archive_roots=list(complete_latest_roots),
      explicit_cumulative_metadata_file_pins=list(explicit_metadata_pins),
      complete_input_pins=unique(complete_fixed_pins+[binding_pin,manifest_pin,source_freeze_pin,
        binding['current_case_spec_pin'],binding['original_v10_seed_plan_pin']]),
      state_order=['B'],observation_scope=B_SCOPE,
      historical_B_context_claimed=False,complete_final_construction_qualified=False)

def aggregate_request(extract_request_value,binding,binding_pin,manifest,
                      extraction_report,extraction_report_pin,extraction_host_pin,
                      independent_review,independent_review_pin,coverage_pin,
                      output_directory,complete_fixed_pins):
    require(extract_request_value['current_B_case_input_binding_pin']==binding_pin and
      extraction_report['state_order']==['B']and set(extraction_report['states'])=={'B'}and
      extraction_report['observation_scope']==B_SCOPE and
      extraction_report['current_B_case_input_binding_pin']==binding_pin and
      extraction_report['actual_observation_manifest_pin']==extract_request_value['actual_observation_manifest_pin'],
      'actual complete B extraction, never retained A pool relabelling')
    owning=Path(binding['actual_output_root'])
    require(extract_request_value['owning_host_output_directory']==str(owning)and
      extract_request_value['joint_archive_roots']==binding['complete_latest_prefix_roots']+[str(owning)]and
      Path(output_directory)==owning/'evidence'/'aggregate'and str(Path(output_directory))==output_directory,
      'same complete B root and exact fresh evidence/aggregate sibling role')
    state=manifest['states']['B']
    pairs=[dict(event=r['event'],role=r['role'],root_prefix=r['root_prefix'],
      input_pin=r['input_pin'],sqlite_pin=r['paired_SQLite_pin'],
      native_pool_pin=r['paired_original_pool_pin'])for r in extraction_report['states']['B']]
    require(len(pairs)==8 and pairs[-1]['role']=='final-complete-micro'and
      independent_review['actual_extraction_report_pin']==extraction_report_pin and
      independent_review['actual_extraction_host_pin']==extraction_host_pin and
      independent_review['actual_observation_manifest_pin']==extract_request_value['actual_observation_manifest_pin']and
      independent_review['current_B_case_input_binding_pin']==binding_pin and
      independent_review['all_snapshot_pairs']==pairs and
      independent_review['complete_context_pins']==state['complete_context_pins']and
      independent_review['all_original_snapshot_and_context_pins_verified']is True,
      'separate actual original B tree/context saved-word review required')
    coverage=dict(schema='ROOT_ACTUAL_COMPLETE_OBSERVED_SNAPSHOT_COVERAGE_FOR_CONTEXT_V1',
      all_original_snapshot_pairs_saved=True,actual_extraction_report_pin=extraction_report_pin,
      actual_observation_manifest_pin=extract_request_value['actual_observation_manifest_pin'],
      current_B_case_input_binding_pin=binding_pin,
      actual_closed_extraction_receipt_independently_reviewed=True,
      independent_actual_review_pin=independent_review_pin,
      states={'B':dict(all_snapshot_pairs=pairs,complete_context_pins=state['complete_context_pins'])},
      new_qualification_sha256=None)
    final=pairs[-1];request=deepcopy(extract_request_value)
    request.update(operation='aggregate',output_directory=output_directory,
      actual_extraction_independent_review_pin=independent_review_pin,
      aggregation_binding=dict(state_order=['B'],current_B_case_input_binding_pin=binding_pin,
        Source_route=dict(ITSTMP=0,historical_call_proved=False),
        states={'B':dict(sqlite_pin=final['sqlite_pin'],native_pool_pin=final['native_pool_pin'])},
        actual_context_states={'B':dict(complete_context_pins=state['complete_context_pins'],
          all_snapshot_pairs=pairs,actual_extraction_report_pin=extraction_report_pin,
          actual_observation_manifest_pin=extract_request_value['actual_observation_manifest_pin'],
          selected_last_libmix_number=state['selected_last_libmix_number'],
          actual_extraction_coverage_contract_pin=coverage_pin)}))
    request['complete_input_pins']=unique(request['complete_input_pins']+complete_fixed_pins+
      [extraction_report_pin,extraction_host_pin,independent_review_pin,coverage_pin])
    return request,coverage
