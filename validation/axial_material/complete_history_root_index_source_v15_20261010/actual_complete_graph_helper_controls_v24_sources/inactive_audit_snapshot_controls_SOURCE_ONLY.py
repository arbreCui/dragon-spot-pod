"""Future Root-run metadata controls only; SOURCE does not grant admission."""
from pathlib import Path
import copy
import gzip
import hashlib
import json
import math
import struct
import subprocess
import sys

SNAPSHOT_FIELDS = ['schema', 'coverage', 'records', 'subprocess_records',
                   'unique_records', 'actual_read_open_attempts', 'record_storage',
                   'success_of_open_attempt_is_not_observed',
                   'native_libc_HDF5_loader_and_directory_stat_are_not_traced']
POSITIVES = ['empty_owned_True', 'same_actual_read_duplicate_and_Popen_owned_True',
             'control_only_floatbits_strattrs_owned_True', 'default_Audit_subclass',
             'default_records_dict_subclass']
REJECTS = ['flag_None', 'flag_zero', 'flag_one', 'flag_string', 'flag_list', 'flag_dict',
           'Audit_subclass_True', 'records_dict_subclass_True', 'records_list_True',
           'recording_True', 'stale_active_registry_identity', 'active_True', 'active_False']
FAILURES = ['invalid_second_row_before_clear', 'missing_attempt_count_before_clear',
            'nonfinite_clone_after_clear']
ENCODER = json.JSONEncoder(ensure_ascii=True, sort_keys=False,
                          separators=(',', ':'), allow_nan=False)

def require(condition, message):
    if type(condition) is not bool or not condition:
        raise AssertionError(message)

def snapshot_order_type_bit_pin(value, *, include_identity=False):
    """Full stream of types/order/fields/values/floatbits, never selected rows.

    Bytes/tuple/subclass attributes are included for caller-state witnesses;
    normalized public snapshots are complete builtin finite JSON. No mutable
    witness tree or complete encoded buffer is allocated by this fingerprint.
    """
    require(type(include_identity) is bool, 'control witness identity flag exact bool')
    digest = hashlib.sha256()
    nodes = 0
    def emit(tag, payload=b''):
        digest.update(tag)
        digest.update(struct.pack('>Q', len(payload)))
        digest.update(payload)
    def visit(part):
        nonlocal nodes
        nodes += 1
        kind = type(part)
        typename = (kind.__module__ + '.' + kind.__qualname__).encode('utf8')
        emit(b'T', typename)
        if isinstance(part, (dict, list, tuple)):
            if include_identity:
                emit(b'I', str(id(part)).encode('ascii'))
            emit(b'N', str(len(part)).encode('ascii'))
            if isinstance(part, dict):
                for key, child in part.items():
                    visit(key)
                    visit(child)
            else:
                for child in part:
                    visit(child)
        elif isinstance(part, str):
            emit(b'S', str.encode(part, 'utf8', 'surrogatepass'))
            if kind is not str:
                if include_identity:
                    emit(b'I', str(id(part)).encode('ascii'))
                visit(getattr(part, '__dict__', None))
        elif kind is bytes:
            emit(b'B', part)
        elif kind is float:
            # Nonfinite bits remain visible in deliberately rejecting fixtures.
            emit(b'F', struct.pack('>d', part))
        elif kind is int:
            emit(b'J', str(part).encode('ascii'))
        elif kind is bool:
            emit(b'Z', b'1' if part else b'0')
        elif kind is type(None):
            emit(b'0')
        else:
            raise AssertionError('unsupported complete control witness type ' + typename.decode())
    visit(value)
    return dict(schema='FULL_STREAM_TYPE_ORDER_VALUE_ATTRS_FLOATBITS_CONTROL_PIN_V1',
                sha256=digest.hexdigest(), complete_node_count=nodes,
                mutable_identities_included=include_identity, no_fields_or_rows_selected=True)

def audit_state_pin(audit, *, include_records=True):
    """All original data identities; temporary witness containers have no id.

    Real Popen references are the same actual objects from one observation.
    Each original mutable root is fingerprinted separately so a newly built
    report list cannot be mistaken for caller-owned audit state.
    """
    require(type(include_records) is bool, 'complete state witness flag exact bool')
    data = dict(subprocess_records=snapshot_order_type_bit_pin(audit._subprocess_records, include_identity=True),
                popen_commands=snapshot_order_type_bit_pin(audit._popen_commands, include_identity=True),
                active=snapshot_order_type_bit_pin(audit._active),
                recording=snapshot_order_type_bit_pin(audit._recording))
    if include_records:
        data['records'] = snapshot_order_type_bit_pin(audit._records, include_identity=True)
    objects = [(key, type(value).__module__ + '.' + type(value).__qualname__, id(value), value)
               for key, value in audit._popen_objects.items()]
    return dict(data=data, exact_Popen_object_map_identity=id(audit._popen_objects),
                exact_actual_Popen_object_references=objects)

def disjoint_owned_audit(g, observed, *, audit_class=None, record_class=None):
    """Copy one genuine observation into a fresh builtin owned record state.

    Real PID/FD/inode/command IDs are unchanged. Popen object references are
    retained exactly in an independent map; they are never synthesized or
    normalized across different processes. Only _records is transferable.
    """
    audit = (g.ReadOpenAudit if audit_class is None else audit_class)()
    records = copy.deepcopy(observed._records)
    audit._records = records if record_class is None else record_class(records)
    audit._subprocess_records = copy.deepcopy(observed._subprocess_records)
    audit._popen_commands = copy.deepcopy(observed._popen_commands)
    audit._popen_objects = dict(observed._popen_objects)
    require(audit._records is not observed._records
            and not any(isinstance(observed._records[key], (dict, list))
                        and audit._records[key] is observed._records[key] for key in audit._records),
            'new private records map and every record dict must be independently owned')
    return audit

def complete_audit_state_equal(left, right, exact_value, label):
    """All private state; original metadata plus exact same observed objects.

    State witnesses stay local and never enter JSON reports. Tuple metadata
    retains original key/type/id values; no PID/FD/inode is normalized.
    """
    fields = ['data', 'exact_Popen_object_map_identity',
              'exact_actual_Popen_object_references']
    require(type(left) is dict and type(right) is dict
            and list(left) == list(right) == fields,
            label + ': complete audit state type/fields/order')
    for field in fields[:2]:
        exact_value(left[field], right[field], label + '/' + field)
    lrefs = left[fields[2]]
    rrefs = right[fields[2]]
    require(type(lrefs) is list and type(rrefs) is list and len(lrefs) == len(rrefs),
            label + ': exact complete Popen reference list type/count/order')
    for index, (lrow, rrow) in enumerate(zip(lrefs, rrefs)):
        where = label + '/' + fields[2] + '/' + str(index)
        require(type(lrow) is tuple and type(rrow) is tuple
                and len(lrow) == len(rrow) == 4,
                where + ': complete original metadata tuple and actual object')
        exact_value(list(lrow[:3]), list(rrow[:3]), where + '/original_key_type_id')
        require(type(lrow[3]) is type(rrow[3]) and lrow[3] is rrow[3],
                where + ': exact actual observed object type and identity')

def complete_snapshot_equal(left, right, exact_value, label):
    require(list(left) == list(right) == SNAPSHOT_FIELDS,
            label + ': all nine original snapshot fields and order')
    exact_value(left, right, label)
    require(snapshot_order_type_bit_pin(left) == snapshot_order_type_bit_pin(right),
            label + ': every nested type/order/field/float bit')

def small_private_snapshot_controls(g, fixture_path, exact_value, wall_seconds):
    """Full default/True/private rejects; original protocol remains separate."""
    require(type(wall_seconds) is int and wall_seconds == 60,
            'same original full pure60 deadline, no new resource allowance')
    path = Path(fixture_path)
    # One real metadata capture, including the actual repeated file opens and
    # real Popen stdio audit. It reads only an existing original tiny fixture.
    with g.ReadOpenAudit() as observed:
        for _ in range(2):
            with path.open('rb') as stream:
                stream.read()
        process = subprocess.Popen(
            [sys.executable, '-B', '-c',
             "import sys;sys.stdout.write('inactive audit metadata protocol\\n')"],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            actual_stdout, actual_stderr = process.communicate(timeout=wall_seconds)
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
    require(process.returncode == 0 and actual_stdout == b'inactive audit metadata protocol\n'
            and actual_stderr == b'', 'actual metadata Popen result required')
    require(observed._active is False and observed._recording is False
            and all(audit is not observed for audit in g._ACTIVE_TRACES),
            'real capture must be inactive and absent from actual hook registry')
    origin = observed.snapshot()
    duplicate = [row for row in origin['records'] if row.get('path') == str(path)]
    require(len(duplicate) == 1 and duplicate[0]['attempt_count'] == 2,
            'real duplicate attempts must survive complete actual capture')
    require(len(origin['subprocess_records']) == 1,
            'one actual Popen audit command and complete stdio descriptors required')
    actual_roles = [row for row in origin['records'] if 'subprocess_stdio_roles' in row]
    require(len(actual_roles) > 0 and any('devnull' in row['subprocess_stdio_roles'] for row in actual_roles),
            'actual original descriptor/Popen role association must be observed')

    class AcceptedStr(str):
        def __str__(self):
            return 'OVERRIDE_MUST_NOT_REPLACE_UNDERLYING_SNAPSHOT_TEXT'
    class AuditSubclass(g.ReadOpenAudit):
        pass
    class RecordsSubclass(dict):
        pass

    empty = g.ReadOpenAudit()
    real = disjoint_owned_audit(g, observed)
    augmented = disjoint_owned_audit(g, observed)
    text = AcceptedStr('actual underlying control text')
    text.caller_attributes = {'floatbits': [-0.0, 1e-300, 1.25],
                              'types': [None, True, False, 0, '0']}
    first_key = next(iter(augmented._records))
    augmented._records[first_key]['control_only_snapshot_extra'] = {
        'signed_zero': [-0.0, 0.0], 'finite_bits': [1e-300, 1.25],
        'ordered_scalars': [True, 0, None, 'text'], 'accepted_str': text}
    positive = []
    for label, source in [('empty_owned_True', empty),
                          ('same_actual_read_duplicate_and_Popen_owned_True', real),
                          ('control_only_floatbits_strattrs_owned_True', augmented)]:
        baseline_audit = disjoint_owned_audit(g, source)
        before = audit_state_pin(baseline_audit)
        baseline = baseline_audit.snapshot()
        complete_audit_state_equal(before, audit_state_pin(baseline_audit), exact_value, label + '/default original complete state')
        explicit = baseline_audit.snapshot(_consume=False)
        complete_snapshot_equal(baseline, explicit, exact_value, label + '/explicitFalse')
        complete_audit_state_equal(before, audit_state_pin(baseline_audit), exact_value, label + '/explicitFalse full state')
        owned = disjoint_owned_audit(g, source)
        map_identity = id(owned._records)
        remaining_before = audit_state_pin(owned, include_records=False)
        value = owned.snapshot(_consume=True)
        require(type(owned._records) is dict and id(owned._records) == map_identity
                and owned._records == {}, label + ': same owned builtin map is cleared')
        complete_audit_state_equal(remaining_before, audit_state_pin(owned, include_records=False), exact_value, label + '/all other data and actual Popen references retained')
        complete_snapshot_equal(baseline, value, exact_value, label + '/True complete descriptor')
        positive.append(dict(case=label, default_and_explicitFalse_complete_state_unchanged=True,
            owned_same_builtin_records_map_completely_cleared=True,
            all_other_audit_state_and_actual_Popen_references_unchanged=True,
            all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default=True,
            actual_full_expected_snapshot=baseline, actual_full_consumed_snapshot=value,
            comparison_origin='same actual observation; disjoint record maps; no PID/FD/inode normalization',
            augmented_control_fields_not_claimed_as_actual_open_trace=(label == 'control_only_floatbits_strattrs_owned_True')))
    for label, audit in [('default_Audit_subclass', disjoint_owned_audit(g, observed, audit_class=AuditSubclass)),
                         ('default_records_dict_subclass', disjoint_owned_audit(g, observed, record_class=RecordsSubclass))]:
        before = audit_state_pin(audit)
        result = audit.snapshot()
        explicit = audit.snapshot(_consume=False)
        complete_snapshot_equal(origin, result, exact_value, label + '/default original public behavior')
        complete_snapshot_equal(origin, explicit, exact_value, label + '/explicitFalse original behavior')
        complete_audit_state_equal(before, audit_state_pin(audit), exact_value, label + '/default full state')
        positive.append(dict(case=label, default_and_explicitFalse_complete_state_unchanged=True,
            all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default=True,
            actual_full_expected_snapshot=origin, actual_full_default_snapshot=result,
            private_True_not_permitted_for_subclass=True))

    rejected = []
    def reject(label, audit, flag, expected_message):
        before = audit_state_pin(audit)
        try:
            audit.snapshot(_consume=flag)
        except Exception as error:
            require(type(error) is g.InputGraphError and str(error) == expected_message,
                    label + ': exact private rejection class/message')
            complete_audit_state_equal(before, audit_state_pin(audit), exact_value, label + '/reject complete caller unchanged')
            rejected.append(dict(case=label, class_name=type(error).__name__, message=str(error),
                rejected=True, complete_audit_state_identity_type_order_value_bits_unchanged=True))
        else:
            raise AssertionError('private control accepted ' + label)
    flag_error = 'private read-open snapshot consume flag must be an exact bool'
    owner_error = 'private read-open snapshot consume requires an owned inactive builtin audit'
    active_error = 'end the read-open audit phase before freezing its trace'
    for label, flag in [('flag_None', None), ('flag_zero', 0), ('flag_one', 1),
                        ('flag_string', 'True'), ('flag_list', []), ('flag_dict', {})]:
        reject(label, disjoint_owned_audit(g, observed), flag, flag_error)
    reject('Audit_subclass_True', disjoint_owned_audit(g, observed, audit_class=AuditSubclass), True, owner_error)
    reject('records_dict_subclass_True', disjoint_owned_audit(g, observed, record_class=RecordsSubclass), True, owner_error)
    bad_list = g.ReadOpenAudit()
    bad_list._records = []
    reject('records_list_True', bad_list, True, owner_error)
    recording = disjoint_owned_audit(g, observed)
    recording._recording = True
    reject('recording_True', recording, True, owner_error)
    stale = disjoint_owned_audit(g, observed)
    g._ACTIVE_TRACES.append(stale)
    try:
        reject('stale_active_registry_identity', stale, True, owner_error)
    finally:
        g._ACTIVE_TRACES.remove(stale)
    with g.ReadOpenAudit() as active:
        reject('active_True', active, True, active_error)
        reject('active_False', active, False, active_error)

    failures = []
    for label in FAILURES:
        source = disjoint_owned_audit(g, observed)
        keys = list(source._records)
        if label == 'invalid_second_row_before_clear':
            source._records = {keys[0]: source._records[keys[0]], b'control_only_invalid_second': None}
        elif label == 'missing_attempt_count_before_clear':
            source._records[keys[0]].pop('attempt_count')
        else:
            source._records[keys[0]]['control_only_nonfinite'] = float('inf')
        errors = []
        for consume in (False, True):
            audit = disjoint_owned_audit(g, source)
            before = audit_state_pin(audit)
            remaining = audit_state_pin(audit, include_records=False)
            try:
                audit.snapshot(_consume=consume)
            except Exception as error:
                errors.append((type(error).__name__, str(error)))
                if consume and label == 'nonfinite_clone_after_clear':
                    require(audit._records == {}, 'private clone error may follow complete map consumption')
                    complete_audit_state_equal(remaining, audit_state_pin(audit, include_records=False), exact_value, label + '/other state')
                else:
                    complete_audit_state_equal(before, audit_state_pin(audit), exact_value, label + '/failure before clear or default')
            else:
                raise AssertionError('invalid snapshot fixture accepted ' + label)
        require(errors[0] == errors[1], label + ': original rejection class and message unchanged')
        failures.append(dict(case=label, actual_default_error=dict(class_name=errors[0][0], message=errors[0][1]),
            actual_private_error=dict(class_name=errors[1][0], message=errors[1][1]),
            original_error_class_and_message_retained=True,
            both_callers_unchanged_before_clear_or_default=(label != 'nonfinite_clone_after_clear'),
            private_clone_failure_after_clear_consumption_observed=(label == 'nonfinite_clone_after_clear'),
            no_transactional_private_mode_promise=True))
    require([c['case'] for c in positive] == POSITIVES
            and [c['case'] for c in rejected] == REJECTS
            and [c['case'] for c in failures] == FAILURES,
            'complete added private snapshot control set and order')
    return dict(schema='PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1',
        status='ACTUAL_PRIVATE_SNAPSHOT_CONTROLS_RETURNED_METADATA_ONLY',
        positive_controls=positive, private_guard_rejections=rejected, last_use_failure_controls=failures,
        actual_single_Popen_observation=origin, actual_same_observation_full_record_role_comparison=True,
        actual_stdout_hex=actual_stdout.hex(), actual_stderr_hex=actual_stderr.hex(), actual_child_returncode=process.returncode,
        no_cross_process_PID_FD_inode_normalization=True, default_original_complete_protocol_preserved=True,
        no_new_fixture_or_material_file_created=True, native_or_numeric_component_executed=False,
        helper_qualification_created=False, business_or_science_qualification_created=False)

def validate_small_control_report(report):
    require(type(report) is dict and report['schema'] == 'PRIVATE_INACTIVE_READ_OPEN_AUDIT_COMPLETE_SNAPSHOT_CONTROLS_V1'
            and report['status'] == 'ACTUAL_PRIVATE_SNAPSHOT_CONTROLS_RETURNED_METADATA_ONLY',
            'actual complete private audit control report required')
    require([c['case'] for c in report['positive_controls']] == POSITIVES
            and [c['case'] for c in report['private_guard_rejections']] == REJECTS
            and [c['case'] for c in report['last_use_failure_controls']] == FAILURES,
            'complete all added control labels and order required')
    for case in report['positive_controls']:
        require(case['default_and_explicitFalse_complete_state_unchanged'] is True
                and case['all_nine_fields_nested_types_order_values_attrs_floatbits_equal_default'] is True,
                'actual positive full state and descriptor witnesses required')
        right = case.get('actual_full_consumed_snapshot', case.get('actual_full_default_snapshot'))
        require(snapshot_order_type_bit_pin(case['actual_full_expected_snapshot']) == snapshot_order_type_bit_pin(right)
                and list(right) == SNAPSHOT_FIELDS, 'saved complete positive snapshots differ')
        if case['case'] in POSITIVES[:3]:
            require(case['owned_same_builtin_records_map_completely_cleared'] is True
                    and case['all_other_audit_state_and_actual_Popen_references_unchanged'] is True,
                    'actual successful private map-only consumption required')
    for case in report['private_guard_rejections']:
        require(case['rejected'] is True and case['class_name'] == 'InputGraphError'
                and case['complete_audit_state_identity_type_order_value_bits_unchanged'] is True,
                'all actual private reject witnesses required')
    for case in report['last_use_failure_controls']:
        expected_after_clear = case['case'] == 'nonfinite_clone_after_clear'
        require(case['both_callers_unchanged_before_clear_or_default'] is (not expected_after_clear)
                and case['private_clone_failure_after_clear_consumption_observed'] is expected_after_clear,
                'actual before-clear vs nontransactional after-clear failure scope required')
        require(case['original_error_class_and_message_retained'] is True
                and case['actual_default_error'] == case['actual_private_error']
                and case['no_transactional_private_mode_promise'] is True,
                'original full failure/last-use contract required')
    require(type(report['actual_child_returncode']) is int and report['actual_child_returncode'] == 0
            and report['actual_stdout_hex'] == b'inactive audit metadata protocol\n'.hex()
            and report['actual_stderr_hex'] == b''.hex(), 'actual observed metadata Popen streams required')
    require(report['actual_same_observation_full_record_role_comparison'] is True
            and report['no_cross_process_PID_FD_inode_normalization'] is True
            and report['default_original_complete_protocol_preserved'] is True
            and report['helper_qualification_created'] is False
            and report['business_or_science_qualification_created'] is False
            and report['native_or_numeric_component_executed'] is False,
            'honest original metadata-only scope required')

def full_consumed_snapshot_wire_compare(trace, gzip_path):
    """Compare every ordered JSON wire byte to the saved complete default.

    Existing caller checks and all three original lossless gzip artifacts stay
    whole. This does not decode another complete graph or select trace rows.
    """
    digest = hashlib.sha256()
    byte_count = 0
    with gzip.open(gzip_path, 'rb') as stream:
        for piece in ENCODER.iterencode(trace):
            block = piece.encode('ascii')
            require(stream.read(len(block)) == block,
                    'complete consumed/default snapshot wire/type/order mismatch')
            digest.update(block)
            byte_count += len(block)
        require(stream.read(1) == b'\n' and stream.read(1) == b'',
                'full default trace gzip terminal newline and EOF required')
        digest.update(b'\n')
        byte_count += 1
    return dict(uncompressed_JSON_bytes=byte_count, uncompressed_JSON_sha256=digest.hexdigest(),
                every_default_and_consumed_wire_byte_compared=True, full_gzip_EOF_verified=True,
                no_fields_or_records_selected=True, complete_nine_snapshot_fields=list(trace))
