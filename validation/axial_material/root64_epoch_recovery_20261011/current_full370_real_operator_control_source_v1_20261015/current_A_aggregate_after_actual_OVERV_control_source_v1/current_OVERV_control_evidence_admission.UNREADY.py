"""Metadata-only admission of the already closed current OVERV control.

No compiler, integer oracle or scientific decoder is invoked here. Root's
fresh full A aggregation still runs all original arithmetic and comparisons.
The earlier missing-control event remains an explicit retained fact.
"""
import json
import hashlib

SCHEMA = 'CURRENT_A_OVERV_PRIOR_ACTUAL_CONTROL_ADMISSION_V1'
ORIGINAL_ISSUE = dict(category='SOURCE_CONTEXT_NOT_SAVED', field='OVERV',
    reason='DOUBLE sqrt/libm rounded constants require independent model/runtime controls',
    original_all370x8_words_compared=True, historical_machine_bit_replay=False)
FALSE_KEYS = ('physics_qualified', 'historical_machine_bit_replay',
    'historical_native_RAM_bits_verified', 'original_XSM_memory_bits_verified',
    'complete_reaction_authority_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete')


def require(ok, message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)


def closed_return(value, key, chunk, payload_key, expected_pin):
    require(value['observed_closed'] is True and
        type(value['original_integer_exit_code']) is int and value['original_integer_exit_code'] == 0,
        'original genuine closed integer0')
    terminal = value[key]
    require(type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and
        terminal['chunk_id'] == chunk, 'exact original genuine terminal return')
    payload = json.loads(terminal['output'])
    require(payload[payload_key] == expected_pin, 'genuine terminal output binds full evidence PF')


def contains_pin(value, expected):
    if type(value) is dict:
        return value == expected or any(contains_pin(v, expected) for v in value.values())
    if type(value) is list:
        return any(contains_pin(v, expected) for v in value)
    return False


def admit_retired_guard_input_roles(request, read):
    """Exact historical PFs remain stored; only released ASCII guards are absent."""
    prior = read(request['historical_complete_input_request_pin'])
    history = prior['complete_input_pins']
    reference = request['historical_complete_input_pins']
    digest = hashlib.sha256(json.dumps(history,sort_keys=True,separators=(',', ':'),allow_nan=False).encode()).hexdigest()
    require(reference == dict(original_request_full_pin=request['historical_complete_input_request_pin'],
        original_member='complete_input_pins',ordered_fullPF_count=5937,
        ordered_fullPF_canonical_sha256=digest) and len(history) == 5937,
        'all immutable historical consumed PFs remain in exact original request and ordered digest')
    proof = request['retired_guard_input_admission_pins']
    receipt, tools, post, posttools = (read(proof[k]) for k in
        ('receipt', 'tools', 'post', 'post_tools'))
    closed_return(tools, 'actual_execution_return', 'ef0657', 'receipt_pin', proof['receipt'])
    closed_return(posttools, 'actual_review_return', '2e6e5f', 'review_pin', proof['post'])
    require(receipt['schema'] == 'LITERAL3_COMPLETED_A_ASCII_EXPORT_RETIREMENT_RECEIPT_V1' and
        receipt['mode'] == 'execute' and receipt['status'] == 'RETIRED_EXACT_LITERAL3_COMPLETED_A_ASCII_EXPORTS_ONLY' and
        receipt['failure'] is None and receipt['actual_released_bytes'] == 346861973 and
        receipt['actual_released_pins'] == receipt['exact_target_pins'] and
        post['schema'] == 'INDEPENDENT_ACTUAL_LITERAL3_A_ASCII_EXPORT_RETIREMENT_METADATA_POSTVERIFY_V1' and
        post['status'] == 'PASS_ACTUAL_EXACT_LITERAL3_A_ASCII_EXPORT_RETIREMENT_346861973B_METADATA_ONLY' and
        post['failure'] is None and post['actual_retirement_receipt_pin'] == proof['receipt'] and
        post['actual_Root_execution_tools_pin'] == proof['tools'] and
        post['all14_earlier_SQL_pool_files_still_live'] is True and post['all43_result_JSONL_preserved'] is True,
        'genuine exact retirement and separate post0, all mathematical operands retained')
    retired = request['exact_retired_input_pins']
    h = {p['path']: p for p in history}
    require(len(h) == 5937 and len(retired) == 3 and
        {p['path']: p for p in retired} == {p['path']: p for p in receipt['actual_released_pins']} and
        all(h[p['path']] == p for p in retired), 'only exact3 historical guards match released fullPFs')
    import os
    require(all(not os.path.lexists(p['path']) for p in retired), 'all exactly retired paths remain absent')
    retired_paths = {p['path'] for p in retired}
    live = {p['path']: p for p in request['complete_input_pins']}
    expected = {k: p for k, p in h.items() if k not in retired_paths}
    require(len(expected) == 5934 and all(live.get(k) == p for k, p in expected.items()) and
        not any(k in live for k in retired_paths) and
        request['current_live_historical_input_count'] == 5934,
        '5937 historical = 5934 unchanged live +3 genuinely retired export guards')
    return dict(historical_consumed_inputs=5937, current_live_historical_inputs=5934,
        exact_retired_guard_input_pins=retired, mathematical_input_scope_reduced=False)


def admit(spec, binding, read):
    require(type(spec) is dict and spec['schema'] == SCHEMA and
        binding['state_order'] == ['A'] and set(binding['states']) == {'A'},
        'explicit current A prior actual control admission')
    values = {key: read(pin) for key, pin in spec['metadata_pins'].items()}
    plan, control, post = (values[k] for k in ('control_plan', 'control_report', 'control_post'))
    closed_return(values['control_returns'], 'actual_terminal_return', 'fa62fd', 'report_pin',
        spec['metadata_pins']['control_report'])
    closed_return(values['control_post_returns'], 'actual_postverification_return', '93f79f', 'review_pin',
        spec['metadata_pins']['control_post'])
    require(control['schema'] == 'ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_GUARDED_REPORT_V1' and
        control['status'] == 'ACTUAL_CURRENT_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY' and
        control['failure'] is None and control['secondary_failures'] == [] and
        control['final_report_resource_check_passed'] is True and
        control['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted'] is True,
        'actual control preserves original missing-control issue and genuine resource closure')
    require(post['schema'] == 'INDEPENDENT_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_ACTUAL_POSTVERIFICATION_V1' and
        post['status'] == 'PASS_ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_CURRENT_CONTROL_FACTS_POSTVERIFIED_NO_HISTORICAL_OR_PHYSICS_QUALIFICATION' and
        post['failure'] is None and post['verification_failure'] is None and
        post['actual_report_pin'] == spec['metadata_pins']['control_report'] and
        post['actual_Root_true_tool_return_pin'] == spec['metadata_pins']['control_returns'] and
        post['actual_Source_freeze_pin'] == spec['metadata_pins']['control_source_freeze'] and
        values['control_source_freeze']['control_plan_pin'] == spec['metadata_pins']['control_plan'] and
        post['original_SOURCE_CONTEXT_NOT_SAVED_issue_removed'] is False and
        post['all_current_native_vs_independent_integer_model_vs_saved_words_equal'] is True and
        post['actual_current_overv_groups'] == 370 and post['actual_current_overv_mixtures'] == 8 and
        post['actual_current_overv_words_compared'] == 2960 and
        post['actual_original_guarded_payload_bytes'] == 13324 and
        post['fixed_and_HF_current_seven_fields_verified_twice'] is True,
        'independent actual current control post, all371+2960 words bound')
    for document in (control, post, control['actual_control_results']):
        require(all(document[key] is False for key in FALSE_KEYS), 'no historical or physics qualification')
    result = control['actual_control_results']
    require(result['all_three_stages_PASS'] is True and
        result['all_constant64_and_overv370x8_current_words_match'] is True and
        result['original_whole_LIBDEN_procedure_executed'] is False and
        len(control['records']) == 3 and all(row['status'] == 'PASS' for row in control['records']),
        'already completed guarded control and integer model, no native rerun')
    prior = values['prior_aggregate_post']
    require(prior['actual_context_or_operand_issues'] == 1 and
        prior['actual_event_category_counts']['SOURCE_CONTEXT_NOT_SAVED'] == 1 and
        prior['actual_numeric_mismatch_rows'] == 0 and prior['actual_unknown_macro_producers'] == 0 and
        prior['actual_comparison_file_rows'] == 19249 and
        prior['actual_aggregate_report_pin'] == spec['metadata_pins']['prior_aggregate_report'] and
        prior['actual_request_pin'] == spec['metadata_pins']['prior_aggregate_request'] and
        values['prior_aggregate_request']['aggregation_binding'] == binding,
        'same actual full A input binding and retained earlier issue1, never a count subtraction')
    previous = values['prior_aggregate_report']
    require(previous == prior['actual_complete_mathematical_report'] and
        previous['state_order'] == ['A'] and previous['states'][0]['all_context_or_operand_issues'] == 1 and
        all(row['computation_finished'] is True for row in previous['states'][0]['phase_results']),
        'immutable old report remains issue1 with all six phases completed')
    actual = binding['actual_context_states']['A']
    pairs = actual['all_snapshot_pairs']
    require(len(pairs) == 8 and len(actual['complete_context_pins']) == 55,
        'all8trees/55events from original complete A inputs')
    descriptor = plan['selected_final_snapshot_descriptor']
    wanted = dict(event=descriptor['event'], role=descriptor['role'], root_prefix=descriptor['root_prefix'],
        input_pin=descriptor['input_pin'], sqlite_pin=descriptor['paired_SQLite_pin'],
        native_pool_pin=descriptor['paired_original_pool_pin'])
    require(wanted == pairs[-1] and wanted['event'] == 55 and
        wanted['role'] == 'final-complete-micro' and wanted['root_prefix'] == [] and
        binding['states']['A'] == dict(sqlite_pin=wanted['sqlite_pin'], native_pool_pin=wanted['native_pool_pin']) and
        plan['actual_extraction_child_report_pin'] == actual['actual_extraction_report_pin'],
        'control and fresh aggregate share exact original final55 descriptor/SQL/pool/extraction')
    original = control['actual_bounded_input_evidence']
    rows = original['actual_original_record_metadata']
    expected = [(('ENERGY',), 371)] + [(('MACROLIB', 'GROUP', g, 'OVERV'), 8) for g in range(1, 371)]
    require(len(rows) == len(expected) == 371 and original['actual_payload_bytes_read'] == 13324 and
        original['original_XSM_opened'] is False, 'exact original control record metadata scope')
    for row, (path, count) in zip(rows, expected):
        require(row['path'] == list(path) and row['kind'] == 2 and
            row['declared_count'] == row['original_word_count'] == count and
            row['native_payload_end_byte'] - row['native_payload_begin_byte'] == count*4,
            'same whole original ENERGY/OVERV record identities and shapes')
    arithmetic = values['original_arithmetic_binding']
    require(arithmetic['schema'] == 'ORIGINAL_OVERV_MIXED_PRECISION_ARITHMETIC_SOURCE_BINDING_V1' and
        arithmetic['each_original_arithmetic_statement_once_in_control'] is True and
        arithmetic['original_material_Source_not_modified'] is True and
        arithmetic['original_LCMPUT_publication_replaced_only_by_control_word_observation'] is True and
        arithmetic['not_an_original_whole_LIBDEN_invocation'] is True and
        contains_pin(plan, spec['metadata_pins']['original_arithmetic_binding']) and
        arithmetic['control_Source_pin']['sha256'] == values['control_source_freeze']['control_Fortran_Source_pin']['sha256'],
        'actual original constants and fallback Source statements, intact current control lineage')
    for key in ('EVJ64_hex', 'NMASS64_hex', 'SQFMAS64_hex'):
        require(type(post['actual_current_constant64_words'][key]) is str and
            len(post['actual_current_constant64_words'][key]) == 16, 'all original constant64 metadata')
    return dict(schema=SCHEMA, status='PRIOR_ACTUAL_CURRENT_OVERV_CONTROL_PREADMITTED_METADATA_ONLY',
        original_issue_fact=ORIGINAL_ISSUE, same_original_final_pair=wanted,
        original_energy_and_overv_record_metadata=rows, control_metadata_pins=spec['metadata_pins'],
        current_constant64_words=post['actual_current_constant64_words'],
        original_prior_issue_count=1, issue_count_adjustment_performed=False,
        physics_qualified=False, historical_machine_bit_replay=False)

