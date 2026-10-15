import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

started = time.monotonic()
attempts = []
def block_process(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.exec', 'os.posix_spawn', 'os.spawn'):
        attempts.append(event)
        raise RuntimeError('read-only Source reviewer prohibits process launches')
sys.addaudithook(block_process)
assert sys.flags.optimize == 0 and sys.dont_write_bytecode
V = Path('/Users/wen/spot/validation/axial_material')
A = Path('/Users/wen/spot/validation/artifacts')
FACTORY = V/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v29_installed6a_20261011.py'
HELPER = V/'combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py'
S = A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v29-installed6a-20261011'
O = A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v29-installed6a-20261011'
CONTRACT = Path('/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/installed6a_closed_metadata_admission_contract.py')
REPORT = Path('/private/tmp/actual_failed_v29_new_Q_cache_Source_only_review_20261011.json')
inputs = {}
def ids(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
def pin(path):
    p = Path(path)
    for q in (p, *p.parents):
        assert not q.is_symlink()
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1
    h = hashlib.sha256()
    with p.open('rb') as f:
        assert ids(os.fstat(f.fileno())) == ids(s)
        for chunk in iter(lambda: f.read(2**20), b''):
            h.update(chunk)
        assert ids(os.fstat(f.fileno())) == ids(s)
    assert ids(p.lstat()) == ids(s)
    return dict(path=str(p), size_bytes=s.st_size, sha256=h.hexdigest(), identity=ids(s))
def hold(path):
    row = pin(path)
    if row['path'] in inputs:
        assert inputs[row['path']] == row
    inputs[row['path']] = row
    return row
def strict_pairs(rows):
    out = {}
    for key, value in rows:
        assert key not in out
        out[key] = value
    return out
def reject(value):
    raise ValueError('nonfinite JSON '+value)
def read(path):
    row = hold(path)
    value = json.loads(Path(path).read_bytes(), object_pairs_hook=strict_pairs, parse_constant=reject)
    assert pin(path) == row
    return value

factory_pin = hold(FACTORY)
helper_pin = hold(HELPER)
contract_pin = hold(CONTRACT)
assert factory_pin['sha256'] == '7383448b86d9a432a4704ddadbe6edb6d3c9779f8611eb2e72deae51d6bd34b9'
assert helper_pin['sha256'] == '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'
assert contract_pin['sha256'] == 'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1'
factory = FACTORY.read_text()
helper = HELPER.read_text()
contract = CONTRACT.read_text()
tree = ast.parse(contract)
imports = [ast.get_source_segment(contract, n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
assert imports == ['import hashlib,json,math,os,stat,struct', 'from pathlib import Path']
assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ('exec_module', 'import_module', 'spec_from_file_location') for n in ast.walk(tree))
ftree = ast.parse(factory)
helper_q = next(n for n in ftree.body if isinstance(n, ast.FunctionDef) and n.name == 'helper_Q_admission')
helper_q_text = ast.get_source_segment(factory, helper_q)
assert helper_q_text.count('spec.loader.exec_module(module)') == 1
assert "NEW6A_METADATA_CONTRACT_PIN['path']" in helper_q_text
negative = read(S/'trim_component_API_absence_INPUT.json')
trace = read(O/'input_creation_python_open_trace.json')
assert set(trace) == {'schema', 'coverage', 'records', 'subprocess_records'}
assert trace['coverage'] == 'PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY'
assert set(negative) == {'absence_inputs', 'aliases', 'observations'}
assert len(negative['absence_inputs']) == len(negative['observations']) == 479
assert set(negative['absence_inputs']) == set(negative['observations'])
assert len(trace['records']) == 65124
missing = [r for r in trace['records'] if r['kind'] == 'path' and r['access'] == 'read' and not os.path.lexists(r['path'])]
assert len(missing) == 14 and len({r['path'] for r in missing}) == 14
covered = [r for r in missing if r['path'] in negative['absence_inputs']]
uncovered = [r for r in missing if r['path'] not in negative['absence_inputs']]
candidate = importlib.util.cache_from_source(str(CONTRACT))
assert candidate == '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/__pycache__/installed6a_closed_metadata_admission_contract.cpython-312.pyc'
assert len(covered) == 13 and len(uncovered) == 1
assert uncovered[0]['path'] == candidate and uncovered[0]['literal_path'] == candidate
assert uncovered[0]['attempt_count'] == 1 and uncovered[0]['flags'] == 16777216 and uncovered[0]['mode'] == 'r'
assert not os.path.lexists(candidate) and not os.path.lexists(Path(candidate).parent)
assert CONTRACT.parent.is_dir() and not CONTRACT.parent.is_symlink()
module_cache_records = [r for r in trace['records'] if r['kind'] == 'path' and '__pycache__' in r['path'] and 'SPOT_INSTALLED6A_NEW_Q' in r['path']]
assert module_cache_records == uncovered
htree = ast.parse(helper)
helpers = {n.name: ast.get_source_segment(helper, n) for n in htree.body if isinstance(n, ast.FunctionDef)}
assert "('code_environment'" in helper or "'source_namespace'" in helper
assert 'ABSENCE_INPUT_ROLE' in helpers['_absence_inputs']
assert 'first_missing_component' in helpers['_absence_observation']
assert 'expected' in helpers['_absence_phase']
assert 'explicit_declared_absent_file_attempts' in helpers['_trace_coverage']
for row in tuple(inputs.values()):
    assert pin(row['path']) == row
assert not attempts and time.monotonic()-started < 600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 512*2**20
result = dict(schema='SPOT_ACTUAL_FAILED_V29_NEW_Q_SOURCE_DERIVED_CACHE_SCOPE_REVIEW_V1',
    status='SOURCE_ONLY_ACTUAL_FAILED_TRACE_SCOPE_REVIEW_NO_FUTURE_COLD_PASS_CLAIM',
    Source_only=True, actual_failed_v29_factory=factory_pin, unchanged_graph_helper=helper_pin,
    unchanged_Q_contract_Source=contract_pin, saved_trace_pin=inputs[str(O/'input_creation_python_open_trace.json')],
    saved_original_negative_pin=inputs[str(S/'trim_component_API_absence_INPUT.json')],
    all_actual_trace_records=65124, all_actual_cache_attempt_records=sum(1 for r in trace['records'] if r['kind']=='path' and '__pycache__' in r['path']),
    genuine_current_absent_read_records=missing, original_exact_absence_contract_count=479,
    genuine_absent_reads_already_declared=covered, genuinely_uncovered_absent_read_records=uncovered,
    fixed_pinned_contract_candidate=candidate,
    contract_stdlib_imports=imports, contract_additional_dynamic_module_imports=0,
    current_new_Q_contract_cache_attempts=module_cache_records,
    minimum_new_absence_input=dict(path=candidate,owner=str(CONTRACT)+'#OPTIONAL_CURRENT_INTERPRETER_CACHE',
        category='source_namespace',reason='Exact cache_from_source candidate of the unchanged explicitly pinned new6a metadata contract; genuine ENOENT is INPUT only'),
    preserve_original479_and_all_trace_records_required=True,
    no_trace_discovery_may_create_new_allowlist=True,
    declared_absence_never_regular_bytes_or_science_credit=True,
    original_absence_phase_parent_alias_ENOENT_before_after_required=True,
    original_live_resource_roots_ART_only_unchanged_required=True,
    held_EOF7ID_inputs=list(inputs.values()), review_Source=hold(__file__),
    project_modules_imported=False, factory_host_writer_Native_PS_or_numerical_executed=False,
    future_PREP_or_full_INPUT_closed0_proved=False,
    elapsed_seconds=time.monotonic()-started, own_max_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
with REPORT.open('x') as f:
    json.dump(result, f, ensure_ascii=False, indent=2, allow_nan=False)
    f.write('\n')
print(json.dumps(dict(status=result['status'], report_pin=pin(REPORT), all_trace_records=65124, actual_absent_reads=14, previously_covered_absent_reads=13, Source_derived_new_contract_candidates=1), allow_nan=False))
