"""Fresh reached typed-input measurement; not parent-API replacement/admission."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
STARTED = time.monotonic()
HELPER = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
HELPER_SHA = 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
SPECS = Path('/private/tmp/combined_runtime_source_owned_typed_input_specs_draft_20261007.json')
SPECS_SHA = 'c9c7414f71ac6f857d8f8dcf959cd558ea2bd26b6fb137ed28870f95473da2d6'
ADAPTER = Path('/private/tmp/combined_runtime_source_owned_typed_input_adapter_draft_20261007.py')
ADAPTER_SHA = '29429fe5318d4525bbbe3e55ce1880d895cbe3cda702962bb780871b95de1714'
BASE = Path('/private/tmp/combined-runtime-reached-typed-inputs-readonly-measurement-20261007')
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == HELPER_SHA
assert hashlib.sha256(ADAPTER.read_bytes()).hexdigest() == ADAPTER_SHA
spec = importlib.util.spec_from_file_location('actual_reached_inputs_readonly_mechanics', HELPER)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
s = g.strict_json(str(SPECS), SPECS_SHA)
assert s['new_business_contract_READY'] is False
assert s['baseline_file_count'] == 26784 and s['original_baseline_file_map_unchanged'] is True
owners = g._owners(s['owners'] + [dict(owner='actual externally observed typed metadata output',
    category='code_environment', expected_files={str(SPECS): SPECS_SHA, str(HELPER): HELPER_SHA,
                                               str(ADAPTER): ADAPTER_SHA})])
alias_paths = set()
for owner in owners:
    alias_paths.update(owner['expected_files'])
for n in s['namespace_specs']:
    alias_paths.add(n['root'])
    alias_paths.update(str(Path(n['root']) / name) for name in n['symlinks'])
alias_paths.update(v['path'] for v in s['aliases'])
aliases = g.capture_aliases(sorted(alias_paths))
alias_map = g._alias_map(aliases)
for owner in s['aliases']:
    binding = alias_map[owner['path']]
    for key, value in owner['binding'].items():
        if key != 'sha256':
            assert binding[key] == value, 'original literal alias expectation changed'
        else:
            # Expected target bytes remain part of this fresh phase's owners.
            alias_map[owner['path']]['sha256'] = value
namespaces = []
for n in s['namespace_specs']:
    links = {}
    for name, value in n['symlinks'].items():
        actual = alias_map[str(Path(n['root']) / name)]
        assert actual['text'] == value, 'old original namespace alias literal changed'
        links[name] = {key: v for key, v in actual.items() if key != 'path'}
    namespaces.append(g.explicit_sealed_namespace(n['root'], n['files'], links,
        owner=n['owner'], category=n['category'], directories=n['directories'], aliases=alias_map.values()))
for requirement in s['independent_directory_owners']:
    actual = g._scan_namespace(requirement['root'], alias_map)
    assert actual['directories'] == set(requirement['directories']), 'independent original SOURCE exact-dir predicate changed'
phase_started = time.monotonic()
with g.ReadOpenAudit() as observed_reads:
    requirements, actual, new_pins, fresh_specs = g._phase(owners, namespaces, alias_map, {},
        json_input=dict(path=str(SPECS), sha256=SPECS_SHA))
phase_elapsed = time.monotonic() - phase_started
observed = observed_reads.snapshot()
assert new_pins == {} and fresh_specs['parsed'] == s
regular_reads = [v for v in observed['records'] if v['kind'] == 'path' and v['path'] in actual]
assert {v['path'] for v in regular_reads} == set(actual)
assert all(v['attempt_count'] == 1 for v in regular_reads)
assert sum(v['attempt_count'] for v in regular_reads) == len(actual)
for requirement in s['independent_directory_owners']:
    after = g._scan_namespace(requirement['root'], alias_map)
    assert after['directories'] == set(requirement['directories']), 'independent SOURCE directory gate changed after phase'
trace_path = BASE / 'measurement/actual_phase_python_open_trace.json'
with trace_path.open('x') as stream:
    json.dump(observed, stream, separators=(',', ':'), allow_nan=False)
    stream.write('\n')
table = g._requirement_table(requirements)
result = dict(schema='AXMAT_COMBINED_RUNTIME_REACHED_TYPED_INPUTS_ACTUAL_READONLY_MEASUREMENT_V1',
    classification='FRESH_TYPED_BYTES_NAMESPACE_AND_ALIAS_MEASUREMENT_ONLY',
    typed_specs=dict(path=str(SPECS), sha256=SPECS_SHA),
    adapter=dict(path=str(ADAPTER), sha256=ADAPTER_SHA),
    helper=dict(path=str(HELPER), sha256=HELPER_SHA),
    full_original_baseline_file_count=26784, baseline_omitted_or_filtered=False,
    reached_component_count=len(s['reached_component_records']),
    original_namespace_logical_requirement_count=len(namespaces),
    distinct_namespace_roots=len({n['root'] for n in namespaces}),
    independent_source_directory_predicate_count=len(s['independent_directory_owners']),
    literal_alias_logical_requirement_count=len(s['aliases']), actual_alias_count=len(alias_map),
    canonical_files_read=len(actual), actual_bytes_read=sum(v['size_bytes'] for v in actual.values()),
    logical_owner_edges=len(requirements), namespace_regular_edges=sum(len(n['files']) for n in namespaces),
    namespace_directory_edges=sum(len(n['directories']) for n in namespaces),
    all_selected_expected_SHAs_and_namespace_requirements_passed=True,
    each_selected_canonical_file_freshly_opened_once_in_phase=True,
    fresh_specs_parsed_from_same_phase_owned_bytes=True,
    actual_phase_open_trace=dict(path=str(trace_path), sha256=hashlib.sha256(trace_path.read_bytes()).hexdigest()),
    actual_phase_python_open_attempt_count=sum(v['attempt_count'] for v in regular_reads),
    requirement_table_sha256=hashlib.sha256(g._canonical_json(table)).hexdigest(),
    phase_elapsed_seconds=phase_elapsed, child_whole_elapsed_seconds=time.monotonic()-STARTED,
    historical_component_semantics_only=True,
    trace_scope='PYTHON_OPEN_ATTEMPTS_OF_SELECTED_PHASE_ONLY_NOT_LIBC_NATIVE_OR_DYLD_TRACE',
    all_original_parent_predicate_edges_complete=False, current_independent_live_predicates_all_checked=False,
    original_component_APIs_executed=False, complete_parent_predicate_replacement_proved=False,
    new_business_contract_READY=False, original_failed_combined_runtime_admitted=False,
    science_qualification_created=False, native_transport_executed=False,
    combined_runtime_RSS_proved=False, AAA_accuracy_qualified=False, ABA_admitted=False)
out = BASE / 'measurement/result.json'
with out.open('x') as stream:
    json.dump(result, stream, indent=2, allow_nan=False)
    stream.write('\n')
print(json.dumps(result, allow_nan=False), flush=True)
print('AXMAT-COMBINED-REACHED-TYPED-INPUTS-READ-ONLY-MEASURED', flush=True)
