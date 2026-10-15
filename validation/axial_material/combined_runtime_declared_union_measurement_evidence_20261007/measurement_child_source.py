"""One fresh full declared-input read. Not a component-API replacement proof."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
STARTED = time.monotonic()
ROOT = Path('/Users/wen/spot')
DECLARATION = ROOT / 'validation/artifacts/axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
DECLARATION_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
HELPER = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
HELPER_SHA = 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
SOURCE_ROOT = ROOT / 'validation/artifacts/axial-material-qualified-AB-physical-dedup-combined-runtime-build-admission-20261007'
for p, wanted in ((DECLARATION, DECLARATION_SHA), (HELPER, HELPER_SHA)):
    assert hashlib.sha256(p.read_bytes()).hexdigest() == wanted
assert Path(sys.executable).resolve() == Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
assert all(os.environ.get(k) == '1' for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS',
           'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'))
spec = importlib.util.spec_from_file_location('actual_combined_declared_union_measurement_helper', HELPER)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
d = g.strict_json(str(DECLARATION), DECLARATION_SHA)
assert d['complete_archive_scope_roots'][0] == str(SOURCE_ROOT)
assert len(d['files']) == 26784
aliases = []
for p, item in d['aliases'].items():
    aliases.append(dict(path=p, text=item['text'], target=item['target'], kind='file',
                        sha256=d['files'][item['target']]))
namespaces = []
for entry in [*d['component_namespaces'], dict(root=str(SOURCE_ROOT), inventory=d['source_inventory'])]:
    inv = entry['inventory']
    assert set(inv) == {'files', 'symlinks', 'directories'} and inv['symlinks'] == {}
    namespaces.append(dict(schema=g.NAMESPACE_SCHEMA, root=entry['root'], canonical_root=entry['root'],
        owner='complete declared namespace ' + entry['root'], category='component_ancestry',
        files=inv['files'], symlinks={}, directories=inv['directories'], namespace_exhaustive=True))
owners = [{'owner': 'whole original declaration files; no filtering',
           'category': 'component_ancestry', 'expected_files': d['files']}]
assert len(namespaces) == 9
phase_started = time.monotonic()
with g.ReadOpenAudit() as actual_reads:
    requirements, actual, new_pins, fresh_parent = g._phase(
        g._owners(owners), [g._namespace_descriptor(v) for v in namespaces],
        g._alias_map(aliases), {})
phase_elapsed = time.monotonic() - phase_started
observed = actual_reads.snapshot()
assert new_pins == {} and fresh_parent is None
assert set(actual) == set(d['files'])
assert all(actual[p]['sha256'] == sha for p, sha in d['files'].items())
assert len(requirements) == len(d['files']) + sum(len(v['files']) for v in namespaces)
assert all(g._resolve(v['path'], g._alias_map(aliases), kind='file') == v['canonical_path']
           for v in requirements)
regular_reads = [r for r in observed['records'] if r['kind'] == 'path' and r['path'] in actual]
assert {r['path'] for r in regular_reads} == set(actual)
assert sum(r['attempt_count'] for r in regular_reads) == len(actual)
assert all(r['attempt_count'] == 1 for r in regular_reads)
table = g._requirement_table(requirements)
result = dict(schema='AXMAT_COMBINED_RUNTIME_DECLARED_UNION_ACTUAL_READONLY_MEASUREMENT_V1',
    classification='COMPLETE_DECLARED_INPUT_BYTES_AND_NAMESPACES_READ_ONLY',
    declaration=dict(path=str(DECLARATION), sha256=DECLARATION_SHA),
    helper=dict(path=str(HELPER), sha256=HELPER_SHA),
    canonical_files_read=len(actual), actual_bytes_read=sum(v['size_bytes'] for v in actual.values()),
    logical_owner_edges=len(requirements), complete_namespace_roots=[v['root'] for v in namespaces],
    namespace_regular_edge_count=sum(len(v['files']) for v in namespaces),
    namespace_directory_edge_count=sum(len(v['directories']) for v in namespaces),
    aliases_checked_before_and_after=len(aliases),
    exact_original_declared_input_scope=True, all_declared_SHA_and_membership_checks_passed=True,
    actual_python_open_attempt_count=sum(r['attempt_count'] for r in regular_reads),
    each_declared_canonical_file_freshly_opened_once_in_this_phase=True,
    requirement_table_sha256=hashlib.sha256(g._canonical_json(table)).hexdigest(),
    phase_elapsed_seconds=phase_elapsed, child_whole_elapsed_seconds=time.monotonic()-STARTED,
    trace_scope='PYTHON_OPEN_ATTEMPTS_ONLY_NOT_LIBC_NATIVE_OR_DYNAMIC_LOADER_TRACE',
    component_implicit_dependency_closure_proved=False, original_component_APIs_executed=False,
    complete_parent_control_predicate_replacement_proved=False,
    original_failed_link_runtime_admitted=False, science_qualification_created=False,
    native_transport_executed=False, combined_runtime_RSS_proved=False,
    AAA_accuracy_qualified=False, ABA_admitted=False)
result_path = Path('/private/tmp/combined_runtime_declared_union_readonly_measurement_result_20261007.json')
with result_path.open('x') as stream:
    json.dump(result, stream, indent=2, allow_nan=False)
    stream.write('\n')
print(json.dumps(result, allow_nan=False), flush=True)
print('AXMAT-COMBINED-DECLARED-UNION-READ-ONLY-MEASURED', flush=True)
