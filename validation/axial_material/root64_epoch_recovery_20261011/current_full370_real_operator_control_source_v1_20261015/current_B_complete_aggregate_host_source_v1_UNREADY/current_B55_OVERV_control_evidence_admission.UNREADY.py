"""UNREADY metadata admission of genuine B55 controls; no science replay.

B has no earlier actual aggregate. ORIGINAL_ISSUE is the unchanged engine's
Source mechanism only. No prior B issue count, subtraction or historical replay
is invented. A's genuinely existing earlier reports remain separately retained.
"""
import json
SCHEMA='CURRENT_B55_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1'
STATUS='PRIOR_ACTUAL_CURRENT_B55_OVERV_CONTROL_PREADMITTED_METADATA_ONLY'
ORIGINAL_ISSUE=dict(category='SOURCE_CONTEXT_NOT_SAVED',field='OVERV',
 reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',
 original_all370x8_words_compared=True,historical_machine_bit_replay=False)
FALSE_KEYS=('physics_qualified','historical_machine_bit_replay','historical_native_RAM_bits_verified',
 'original_XSM_memory_bits_verified','complete_reaction_authority_qualified','AAA_qualified','ABA_admitted','goal_complete','A_control_reused')
def require(v,m):
 if type(v)is not bool or not v:raise ValueError(m)
def closed(value,key,chunk,payload_key,expected):
 terminal=value[key]
 require(value['observed_closed']is True and type(value['original_integer_exit_code'])is int and value['original_integer_exit_code']==0 and type(terminal['exit_code'])is int and terminal['exit_code']==0 and terminal.get('session_id')is None and terminal['chunk_id']==chunk,'genuine exact original closed typed0')
 require(json.loads(terminal['output'].strip().splitlines()[-1])[payload_key]==expected,'actual stdout binds exact fullPF')
def admit(spec,binding,read):
 require(type(spec)is dict and spec['schema']==SCHEMA and binding['state_order']==['B']and set(binding['states'])==set(binding['actual_context_states'])=={'B'},'current original B only; no A control or earlier B aggregate fiction')
 pins=spec['metadata_pins'];v={key:read(p)for key,p in pins.items()}
 plan=v['control_plan'];host=v['control_report'];post=v['control_post'];sf=v['control_source_freeze']
 closed(v['control_returns'],'actual_terminal_return','02a5d8','report_pin',pins['control_report'])
 closed(v['control_post_returns'],'actual_review_return','f10181','review_pin',pins['control_post'])
 require(v['control_returns']['actual_execution_permission_mode']=='require_escalated'and v['control_returns']['actual_retried']is False,'genuine original bounded B55 control once')
 require(host['schema']=='ACTUAL_CURRENT_B55_OVERV_ORIGINAL_NATIVE_INTEGER_CONTROL_GUARDED_REPORT_V1'and host['status']=='ACTUAL_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY'and host['failure']is None and host['secondary_failures']==[]and host['final_report_resource_check_passed']is True and host['control_plan_pin']==pins['control_plan']and host['source_freeze_pin']==pins['control_source_freeze']and host['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted']is True,'actual B55 control closes original resources and retains Source issue history')
 require(post['schema']=='RECORDED_CURRENT_B55_OVERV_NATIVE_INTEGER_CONTROL_METADATA_POSTVERIFY_V1'and post['status']=='PASS_ACTUAL_CURRENT_B55_OVERV_THREE_STAGE0_2960_WORDS_MATCH_METADATA_ONLY_NO_PHYSICS_QUALIFICATION'and post['failure']is None and post['metadata_only']is True and post['actual_Root_tools_pin']==pins['control_returns']and post['actual_Host_report_pin']==pins['control_report']and post['Source_freeze_pin']==pins['control_source_freeze']and post['control_plan_pin']==pins['control_plan']and post['actual_Root_integer_exit_code']==0 and post['actual_child_integer_exit_codes']==[0,0,0],'genuine independent current B55 actual post0 with three child0')
 require(sf['schema']=='CURRENT_B55_OVERV_CONTROL_SOURCE_ONLY_FREEZE_V1'and sf['control_plan_pin']==pins['control_plan']and sf['compiler_executed']is False and sf['native_executed']is False,'same frozen original B55 Source control')
 result=host['actual_control_results'];counts=dict(actual_current_energy_words_observed=371,actual_current_overv_words_compared=2960,actual_current_overv_groups=370,actual_current_overv_mixtures=8,actual_native_vs_integer_model_and_saved_word_mismatches=0,actual_constant64_words_compared=3,actual_constant64_word_mismatches=0)
 require(result==post['actual_control_results_metadata']and result['all_three_stages_PASS']is True and result['all_constant64_and_overv370x8_current_words_match']is True and result['original_whole_LIBDEN_procedure_executed']is False and post['actual_current_control_word_comparison_counts']==counts and all(type(result[k])is int and result[k]==x for k,x in counts.items()),'actual complete371/2960/3 constants and zero differences; no recomputation here')
 require(len(host['records'])==len(host['actual_watchdog_checks'])==3 and all(r['status']=='PASS'for r in host['records'])and all(type(w['actual_watchdog']['returncode'])is int and w['actual_watchdog']['returncode']==0 and w['actual_watchdog']['limit_failure']is None for w in host['actual_watchdog_checks']),'all three actual original stages closed0')
 for document in(host,post,result):require(all(document[k]is False for k in FALSE_KEYS),'no historical/physics/A-reuse qualification')
 actual=binding['actual_context_states']['B'];pairs=actual['all_snapshot_pairs'];descriptor=plan['selected_actual_B55_snapshot_descriptor']
 wanted=dict(event=descriptor['event'],role=descriptor['role'],root_prefix=descriptor['root_prefix'],input_pin=descriptor['input_pin'],sqlite_pin=descriptor['paired_SQLite_pin'],native_pool_pin=descriptor['paired_original_pool_pin'])
 require(len(pairs)==8 and len(actual['complete_context_pins'])==55 and pairs[-1]==wanted and wanted['event']==55 and wanted['role']=='final-complete-micro'and wanted['root_prefix']==[]and descriptor['state']=='B'and binding['states']['B']==dict(sqlite_pin=wanted['sqlite_pin'],native_pool_pin=wanted['native_pool_pin']),'all8trees/55contexts and exact actual final B55 pair')
 require(host['selected_actual_B55_snapshot_descriptor']==post['selected_actual_B55_snapshot_descriptor']==descriptor and host['selected_actual_B55_SQL_pool_pair']==post['selected_actual_B55_SQL_pool_pair']==plan['selected_actual_B55_SQL_pool_pair']==binding['states']['B']and host['actual_B_extraction_report_pin']==post['actual_B_extraction_report_pin']==plan['actual_B_extraction_child_report_pin']==actual['actual_extraction_report_pin']and host['actual_B_manifest_pin']==post['actual_B_manifest_pin']==plan['actual_B_manifest_pin']==actual['actual_observation_manifest_pin']and host['actual_B_input_binding_pin']==post['actual_B_input_binding_pin']==plan['actual_B_input_binding_pin']==binding['current_B_case_input_binding_pin'],'control and aggregate consume this exact B input/extraction/manifest, not an A result')
 original=host['actual_bounded_input_evidence'];rows=original['actual_original_record_metadata'];expected=[(('ENERGY',),371)]+[(('MACROLIB','GROUP',g,'OVERV'),8)for g in range(1,371)]
 require(original==post['actual_bounded_input_evidence_metadata']and len(rows)==371 and original['actual_payload_bytes_read']==13324 and original['complete_SQLite_or_pool_body_EOF_repeated']is False and original['original_XSM_opened']is False,'actual bounded B55 input record metadata only')
 for row,(path,count)in zip(rows,expected):require(row['path']==list(path)and row['kind']==2 and row['declared_count']==row['original_word_count']==count and row['native_payload_end_byte']-row['native_payload_begin_byte']==count*4,'same whole original B ENERGY/OVERV metadata paths/types/shapes')
 arithmetic=v['original_arithmetic_Source_binding']
 require(arithmetic['schema']=='ORIGINAL_OVERV_MIXED_PRECISION_ARITHMETIC_SOURCE_BINDING_V1'and arithmetic['each_original_arithmetic_statement_once_in_control']is True and arithmetic['original_material_Source_not_modified']is True and arithmetic['original_LCMPUT_publication_replaced_only_by_control_word_observation']is True and arithmetic['not_an_original_whole_LIBDEN_invocation']is True and arithmetic['control_Source_pin']['sha256']==sf['control_Fortran_Source_pin']['sha256']==plan['control_Fortran_Source_pin']['sha256'],'original arithmetic Source reference only; no A actual control imported')
 return dict(schema=SCHEMA,status=STATUS,original_issue_fact=ORIGINAL_ISSUE,original_issue_fact_is_Source_mechanism_not_prior_B_measurement=True,prior_B_aggregate_executed=False,prior_B_issue_count=None,prior_B_issue_count_invented=False,issue_count_adjustment_performed=False,same_original_final_pair=wanted,original_energy_and_overv_record_metadata=rows,control_metadata_pins=pins,actual_current_control_word_comparison_counts=counts,A_control_reused=False,historical_machine_bit_replay=False,physics_qualified=False)
