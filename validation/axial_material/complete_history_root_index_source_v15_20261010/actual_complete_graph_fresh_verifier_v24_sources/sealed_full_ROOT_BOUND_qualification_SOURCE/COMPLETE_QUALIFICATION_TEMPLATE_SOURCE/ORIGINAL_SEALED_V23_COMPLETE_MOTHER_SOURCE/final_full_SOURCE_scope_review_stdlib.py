"""SOURCE AST/byteproof only. Never import/execute any reviewed Source."""
from pathlib import Path
import ast
import hashlib
import json

P = Path(__file__).parent
checks = []

def check(label, passed, evidence=None):
    assert type(passed) is bool
    checks.append(dict(check=label, passed=passed, evidence=evidence))
    assert passed, label

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def full_pin(path):
    before = identity(path)
    raw = path.read_bytes()
    assert before == identity(path) and len(raw) == before[4]
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=before)

def segment(source, node):
    return ''.join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])

def globals_of(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result

inverse = json.loads((P / 'ALL_FOUR_COMPLETE_QUALIFICATION_TEMPLATE_INVERSES.json').read_bytes())
for name, proof in inverse['all_four_complete_source_inverse'].items():
    template = Path(proof['template_pin']['path'])
    raw = template.read_text()
    check(name + '/actual_complete_template_full_pin', full_pin(template) == proof['template_pin'])
    restored = raw
    for hunk in reversed(proof['full_hunks']):
        check(name + '/unique_inverse_' + hunk['label'], restored.count(hunk['new_utf8']) == 1)
        restored = restored.replace(hunk['new_utf8'], hunk['old_utf8'], 1)
    original = Path(proof['original_Source_pin']['path'])
    check(name + '/original_full_Source_current_pin', full_pin(original) == proof['original_Source_pin'])
    check(name + '/full_original_bytes_AST', restored == original.read_text()
          and ast.dump(ast.parse(restored), include_attributes=False)
          == ast.dump(ast.parse(original.read_text()), include_attributes=False))
    old_source = original.read_text()
    old_defs = {node.name: node for node in ast.parse(old_source).body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    new_defs = {node.name: node for node in ast.parse(raw).body
                if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
    check(name + '/complete_original_definitions_order',
          [key for key in new_defs if key in old_defs] == list(old_defs))
    for label, node in old_defs.items():
        if label not in proof['actually_changed_original_definitions']:
            check(name + '/whole_unchanged_definition/' + label,
                  segment(old_source, node) == segment(raw, new_defs[label])
                  and ast.dump(node, include_attributes=False) == ast.dump(new_defs[label], include_attributes=False))
    for guard_text in ('guard_admission(full)', 'full.OwnRSSSerialExecutor.__bases__',
                       'resource.DynamicHistoryResources', 'resources.check()', 'runner.execute('):
        if guard_text in old_source:
            check(name + '/all_original_genuine_guard_count/' + guard_text,
                  raw.count(guard_text) == old_source.count(guard_text))
    literals = globals_of(ast.parse(raw))
    check(name + '/UNREADY_Source_status', literals['SOURCE_STATUS'].startswith('UNREADY'))
    for key in ('ACTUAL_SUCCESS_PINS', 'UNKNOWN_Q', 'UNKNOWN_BUSINESS_PINS', 'BOUND_HELPER_PIN',
                'INSTALL_WITNESS_PIN', 'SOURCE_INSTALL_RECORD_PIN', 'TARGET_SHA', 'NEW_HELPER_IDENTITY',
                'NEW_HELPER_PATH', 'HELPER_PATH', 'AUDIT_CONTROL_PATH'):
        if key in literals:
            check(name + '/unknown_actual_binding_None/' + key, literals[key] is None)
    check(name + '/complete_new_module_sha_bytes',
          literals['AUDIT_CONTROL_SHA256'] == full_pin(P / 'inactive_audit_snapshot_controls_SOURCE_ONLY.py')['sha256']
          and literals['AUDIT_CONTROL_SOURCE_BYTES'] == (P / 'inactive_audit_snapshot_controls_SOURCE_ONLY.py').stat().st_size)

module = (P / 'inactive_audit_snapshot_controls_SOURCE_ONLY.py').read_text()
mt = ast.parse(module)
mg = globals_of(mt)
check('complete_snapshot_nine_fields', mg['SNAPSHOT_FIELDS'] == ['schema', 'coverage', 'records', 'subprocess_records',
      'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed',
      'native_libc_HDF5_loader_and_directory_stat_are_not_traced'])
check('new_complete_control_counts5positive13reject3failure',
      len(mg['POSITIVES']) == 5 and len(mg['REJECTS']) == 13 and len(mg['FAILURES']) == 3)
check('new_control_labels_unique', len(set(mg['POSITIVES'] + mg['REJECTS'] + mg['FAILURES'])) == 21)
check('actual_same_Popen_source_observation_not_cross_run_identity_normalization',
      module.count('process = subprocess.Popen(') == 1
      and 'audit._popen_objects = dict(observed._popen_objects)' in module
      and 'records = copy.deepcopy(observed._records)' in module
      and 'no_cross_process_PID_FD_inode_normalization=True' in module)
check('complete_type_order_floatbits_strattrs_witness', all(text in module for text in
      ("struct.pack('>d', part)", "str.encode(part, 'utf8', 'surrogatepass')",
       "visit(getattr(part, '__dict__', None))", 'for key, child in part.items():', 'for child in part:')))
state = next(node for node in mt.body if isinstance(node, ast.FunctionDef) and node.name == 'audit_state_pin')
check('ephemeral_witness_wrapper_id_not_counted_as_caller', 'rows' not in {node.id for node in ast.walk(state) if isinstance(node, ast.Name)}
      and 'snapshot_order_type_bit_pin(audit._records, include_identity=True)' in ast.get_source_segment(module, state))
check('private_failure_error_scope_and_nontransactional_after_clear_honest', all(text in module for text in
      ('original_error_class_and_message_retained=True', 'private_clone_failure_after_clear_consumption_observed=',
       "expected_after_clear = case['case'] == 'nonfinite_clone_after_clear'", 'no_transactional_private_mode_promise=True')))
check('entire_wire_and_full_gzip_EOF_no_selected_rows', all(text in module for text in
      ('for piece in ENCODER.iterencode(trace):', "stream.read(len(block)) == block",
       "stream.read(1) == b'\\n' and stream.read(1) == b''", 'no_fields_or_records_selected=True')))
pure = (P / 'pure_helper_controls.UNREADY.py').read_text()
phost = (P / 'pure_helper_controls_host.UNREADY.py').read_text()
fresh = (P / 'fresh_verifier_controls.UNREADY.py').read_text()
fhost = (P / 'fresh_verifier_host.UNREADY.py').read_text()
check('pure_original_report_sort_encoding_preserved_and_private_complete_order_artifact_added',
      'report_pin = artifacts.write_json("ACTUAL_REPORT.json", report)' in pure
      and 'encoder=ORDER_PRESERVING_JSON_ENCODER)' in pure
      and 'ACTUAL_PRIVATE_INACTIVE_AUDIT_SNAPSHOT_CONTROLS.json' in phost
      and 'audit_controls.validate_small_control_report(private_report)' in phost)
check('pure_new_loader_has_global_hashlib_dependency',
      any(isinstance(n, ast.Import) and any(a.name == 'hashlib' for a in n.names) for n in ast.parse(phost).body))
check('fresh_complete_original37111files37112reads',
      'all37111 canonical files plus1 fixed externalgraph must be really opened once' in fresh
      and "len(trace['records'])!=37112" in fhost
      and 'canonical_files=37111' in fhost)
check('fresh_all_original27_return_fields_order', len(globals_of(ast.parse(fhost))['RETURN_FIELDS']) == 27)
for filename in ('EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz', 'ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz',
                 'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'):
    check('fresh_three_original_lossless_gzip/' + filename, filename in fresh and filename in fhost)
check('fresh_original_trace_snapshot_default_then_private_last_use_source_order',
      fresh.index('trace=audit.snapshot()') < fresh.index("lossless_json_gzip(output,'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'")
      < fresh.index('del trace') < fresh.index('trace=audit.snapshot(_consume=True)')
      < fresh.index("report['actual_complete_trace_counts']"))
check('fresh_full_default_record_identity_nonmutation_and_True_complete_contract', all(text in fresh for text in
      ('audit_records_before=', 'include_identity=True', 'all_nine_fields_full_type_order_value_floatbits_and_counts_equal=True',
       'all37112_actual_reads_from_same_genuine_phase=True', 'no_cross_phase_hash_or_stat_cache=True')))
check('fresh_no_second_graph_phase_added', fresh.count('verified=new.verify_graph(') == 1)
check('fresh_all_original_four_positive_three_reject_trace_controls',
      "len(positive)!=4" in fhost and "len(negative)!=3" in fhost)
binder = (P / 'bind_complete_qualification_SOURCE_only.py').read_text()
check('Source_binder_exact_SCHEMA_int0_closed_stdout_7ID_coupling', all(text in binder for text in
      ('ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1',
       "type(terminal['exit_code']) is int and terminal['exit_code'] == 0",
       "('session_id' not in terminal or terminal['session_id'] is None)",
       "observed['installed_helper'] == witness['installed_helper']", "all(type(item) is int for item in pin['identity'])")))
check('Source_binder_complete_parent_inventory_and_no_Controller_import_execution',
      'shutil.copytree(HERE, out /' in binder and 'original_members, original_directories' in binder
      and 'importlib' not in binder and 'subprocess' not in binder and 'exec(' not in binder)
check('Source_binder_actual_qualification_none_and_oldQ_no_credit',
      'new_actual_helper_qualification=None' in binder and "record['actual_new_helper_qualification_sha256'] is None" in binder
      and 'PROTECTED_PARENT_SHA' in binder)
for file in sorted(P.rglob('*.py')):
    ast.parse(file.read_bytes())
    check('full_Source_AST_parse_only/' + file.relative_to(P).as_posix(), True)
plan = json.loads((P / 'ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json').read_bytes())
check('all_future_qualification_and_six_business_pins_None',
      plan['new_joint_Helper_Q'] is None and plan['all_business_science_pins'] == [None] * 6
      and plan['new_pure_terminal'] is None and plan['new_fresh_terminal'] is None)
for kind in ('pure', 'fresh'):
    for key in ('host', 'output'):
        path = Path(plan['namespaces'][kind][key])
        check('five_history_ART_contract_new_path/' + kind + '/' + key,
              path.is_relative_to(Path('/Users/wen/spot/validation/artifacts'))
              and path != Path('/Users/wen/spot/validation/artifacts'))
report = dict(schema='COMPLETE_PRIVATE_INACTIVE_AUDIT_FULL_QUALIFICATION_FINAL_SOURCE_REVIEW_V1',
              status='PASS_SOURCE_ONLY_UNREADY_NO_CONTROLLER_OR_BINDER_EXECUTION', source_only=True,
              checks=checks, check_count=len(checks), all_checks_typed_true=all(c['passed'] is True for c in checks),
              blockers=[], qualified_template_Source_pins={name: full_pin(P/name) for name in
              ('pure_helper_controls.UNREADY.py','pure_helper_controls_host.UNREADY.py','fresh_verifier_controls.UNREADY.py',
               'fresh_verifier_host.UNREADY.py','inactive_audit_snapshot_controls_SOURCE_ONLY.py')},
              new_actual_helper_qualification=None, six_future_business_pins=[None]*6,
              helper_candidate_guard_reader_API_or_controller_or_Source_binding_executed=False)
(P / 'FINAL_FULL_SOURCE_SCOPE_REVIEW.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
print(json.dumps(dict(source_only=True, check_count=len(checks), all_checks_typed_true=True,
                     report_pin=full_pin(P / 'FINAL_FULL_SOURCE_SCOPE_REVIEW.json'), actual_newQ=None,
                     candidate_or_binding_executed=False), separators=(',', ':')))
