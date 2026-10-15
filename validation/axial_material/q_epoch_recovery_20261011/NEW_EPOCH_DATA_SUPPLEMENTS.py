"""New synthetic index controls; not recovered old Source or live I/O evidence."""
import copy
import json
import struct

SNAPSHOT_FIELDS = ['schema', 'coverage', 'records', 'subprocess_records',
                   'unique_records', 'actual_read_open_attempts', 'record_storage',
                   'success_of_open_attempt_is_not_observed',
                   'native_libc_HDF5_loader_and_directory_stat_are_not_traced']


def typed(v, identities=False):
    kind = type(v)
    if kind is float:
        return ('float', struct.pack('>d', v).hex())
    if kind in (dict, list, tuple, set):
        prefix = (kind.__name__, id(v)) if identities else (kind.__name__,)
        if kind is dict:
            return prefix + (tuple((typed(k, identities), typed(x, identities)) for k, x in v.items()),)
        if kind is set:
            return prefix + (frozenset(typed(x, identities) for x in v),)
        return prefix + (tuple(typed(x, identities) for x in v),)
    if isinstance(v, (dict, list, tuple, set)):
        return (kind.__module__, kind.__qualname__, id(v), repr(v))
    return (kind.__module__, kind.__qualname__, v)


def state(a):
    return typed({k: v for k, v in a.__dict__.items()}, identities=True)[-1]


def other_state(a):
    return tuple((k, typed(v, identities=True)) for k, v in a.__dict__.items()
                 if k not in ('_records', '_read_open_key_count_included'))


def clone(g, a, cls=None, records_cls=None):
    b = (g.ReadOpenAudit if cls is None else cls)()
    b._records = copy.deepcopy(a._records)
    if records_cls is not None:
        b._records = records_cls(b._records)
    b._read_open_key_count_included = copy.deepcopy(a._read_open_key_count_included)
    b._subprocess_records = copy.deepcopy(a._subprocess_records)
    b._popen_objects = dict(a._popen_objects)
    b._popen_commands = copy.deepcopy(a._popen_commands)
    b._active = a._active
    b._recording = a._recording
    return b


def snapshot_oracle(g, records):
    return dict(schema=g.TRACE_SCHEMA, coverage='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY',
                records=g._json_clone(list(records.values())), subprocess_records=[],
                unique_records=len(records),
                actual_read_open_attempts=sum(row['attempt_count'] for row in records.values()),
                record_storage='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS',
                success_of_open_attempt_is_not_observed=True,
                native_libc_HDF5_loader_and_directory_stat_are_not_traced=True)


def index_controls(g, saved_fixture_metadata):
    """Perform all synthetic cases using current code; never reuse saved PASS booleans."""
    seed = saved_fixture_metadata['complete_default_snapshot']['records']
    assert len(seed) == 9
    assert [r['attempt_count'] for r in seed] == [7, 6, 5, 4, 4, 3, 3, 2, 1]
    assert sum(r['attempt_count'] for r in seed) == 35
    assert not saved_fixture_metadata['complete_default_snapshot']['subprocess_records']
    cases = []
    baseline = None
    for label, digest in [('standard_SHA256', None), ('forced_collision', lambda data: b'one forced collision')]:
        a = g.ReadOpenAudit()
        oracle = {}
        for row in seed:
            count = row['attempt_count']
            includes_count = 'observer_error' in row
            for repeat in range(count):
                value = copy.deepcopy(row)
                if includes_count:
                    value['attempt_count'] = 1
                else:
                    del value['attempt_count']
                original_key = g._canonical_json(value)
                if original_key not in oracle:
                    stored = copy.deepcopy(value)
                    stored['attempt_count'] = 1
                    oracle[original_key] = stored
                else:
                    oracle[original_key]['attempt_count'] += 1
                g._read_open_short_index_insert(a, value,
                    _key_includes_count=includes_count, _index_digest=digest)
        assert len(a._records) == 9 and len(a._read_open_key_count_included) == 2
        before = state(a)
        expected = snapshot_oracle(g, oracle)
        actual = a.snapshot()
        assert list(actual) == list(expected) == SNAPSHOT_FIELDS
        assert typed(actual) == typed(expected)
        assert before == state(a)
        explicit = a.snapshot(_consume=False)
        assert typed(explicit) == typed(expected) and state(a) == before
        owned = clone(g, a)
        map_id, set_id = id(owned._records), id(owned._read_open_key_count_included)
        rest = other_state(owned)
        consumed = owned.snapshot(_consume=True)
        assert typed(consumed) == typed(expected)
        assert id(owned._records) == map_id and owned._records == {}
        assert id(owned._read_open_key_count_included) == set_id and owned._read_open_key_count_included == set()
        assert other_state(owned) == rest
        if baseline is None:
            baseline = actual
            observed = a
        else:
            assert typed(baseline) == typed(actual)
        cases.append(dict(case=label, complete_actual_snapshot=actual,
                          default_and_explicitFalse_complete_state_unchanged=True,
                          owned_same_map_and_marker_set_cleared=True,
                          original_canonical_key_bytes_oracle_equal=True))

    class AuditSubclass(g.ReadOpenAudit):
        pass

    class RecordsSubclass(dict):
        pass

    rejections = []

    def reject(label, a, flag, message):
        before = state(a)
        try:
            a.snapshot(_consume=flag)
        except Exception as error:
            assert type(error) is g.InputGraphError and str(error) == message
            assert state(a) == before
            rejections.append(dict(case=label, class_name=type(error).__name__,
                                   message=str(error), caller_complete_state_unchanged=True))
        else:
            raise AssertionError('synthetic private guard accepted ' + label)

    flag_error = 'private read-open snapshot consume flag must be an exact bool'
    owner_error = 'private read-open snapshot consume requires an owned inactive builtin audit'
    active_error = 'end the read-open audit phase before freezing its trace'
    for label, flag in [('flag_None', None), ('flag_zero', 0), ('flag_one', 1),
                        ('flag_string', 'True'), ('flag_list', []), ('flag_dict', {})]:
        reject(label, clone(g, observed), flag, flag_error)
    reject('Audit_subclass_True', clone(g, observed, cls=AuditSubclass), True, owner_error)
    reject('records_dict_subclass_True', clone(g, observed, records_cls=RecordsSubclass), True, owner_error)
    a = clone(g, observed)
    a._records = []
    reject('records_list_True', a, True, owner_error)
    a = clone(g, observed)
    a._recording = True
    reject('recording_True', a, True, owner_error)
    a = clone(g, observed)
    g._ACTIVE_TRACES.append(a)
    try:
        reject('stale_active_registry_identity', a, True, owner_error)
    finally:
        g._ACTIVE_TRACES.remove(a)
    # Setting the state is synthetic control data, not a fake live audit phase.
    a = clone(g, observed)
    a._active = True
    reject('active_True', a, True, active_error)
    reject('active_False', a, False, active_error)
    assert [r['case'] for r in rejections] == [r['case'] for r in saved_fixture_metadata['all_original_guards_with_nonempty_markers']]
    for actual, saved in zip(rejections, saved_fixture_metadata['all_original_guards_with_nonempty_markers']):
        assert (actual['class_name'], actual['message']) == (saved['class_name'], saved['message'])

    failures = []
    for label in ['invalid_second_row_before_clear', 'missing_attempt_count_before_clear', 'nonfinite_clone_after_clear']:
        source = clone(g, observed)
        keys = list(source._records)
        if label == 'invalid_second_row_before_clear':
            source._records = {keys[0]: source._records[keys[0]], b'control_only_invalid_second': None}
        elif label == 'missing_attempt_count_before_clear':
            source._records[keys[0]].pop('attempt_count')
        else:
            source._records[keys[0]]['control_only_nonfinite'] = float('inf')
        errors = []
        for consume in (False, True):
            a = clone(g, source)
            before, rest = state(a), other_state(a)
            try:
                a.snapshot(_consume=consume)
            except Exception as error:
                errors.append((type(error).__name__, str(error)))
                if consume and label == 'nonfinite_clone_after_clear':
                    assert a._records == {} and a._read_open_key_count_included == set()
                    assert other_state(a) == rest
                else:
                    assert state(a) == before
            else:
                raise AssertionError('synthetic last-use failure accepted ' + label)
        assert errors[0] == errors[1]
        failures.append(dict(case=label, actual_default_error=errors[0],
                             actual_private_error=errors[1],
                             original_error_class_and_message_retained=True,
                             no_transactional_private_mode_promise=True))
    assert [r['case'] for r in failures] == [r['case'] for r in saved_fixture_metadata['original_last_use_failure_with_nonempty_markers']]
    return dict(schema='NEW_EPOCH_ACTUAL_SYNTHETIC_INDEX_CONTROLS_V1',
                status='ACTUAL_SYNTHETIC_DATA_CONTROLS_ONLY_NO_Q',
                positive_controls=cases, all_original_guards_with_nonempty_markers=rejections,
                original_last_use_failure_with_nonempty_markers=failures,
                complete_default_snapshot=baseline, actual_attempts=35, unique_records=9,
                exception_count_bearing_markers=2,
                control_data_not_real_open_PID_FD_or_Popen_evidence=True,
                no_saved_pass_boolean_used_as_actual_result=True,
                actual_original_new_controller_Source_recovered=False,
                helper_or_runtime_or_scientific_qualification=False)
