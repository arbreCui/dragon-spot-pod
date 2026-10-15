"""Run actual stdlib small-data controls only; no PS, Popen, full graph or solver."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys
import threading
import time

ROOT = Path('/Users/wen/spot')
BASE = Path(__file__).resolve().parent
OWN = BASE/'small_data_actual'
START = time.monotonic()
ATTEMPTS = []
META = ROOT/'validation/artifacts/axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4'
ALLOWED_ART_READS = {str(META/'ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json'),
                     str(META/'ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json'),
                     str(ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json')}


def safety(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.exec',
                 'os.posix_spawn', 'os.spawn', 'os.startfile', 'os.startfile/2'):
        ATTEMPTS.append(event)
        raise RuntimeError('recovery small-data run forbids all process creation')
    if event == 'open' and isinstance(args[0], (str, bytes)):
        path = Path(os.fsdecode(args[0])).absolute()
        flags = args[2]
        write = isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        if write and not path.is_relative_to(OWN):
            raise RuntimeError('only new small-data output can be written')
        if path.is_relative_to(ROOT/'validation/artifacts') and str(path) not in ALLOWED_ART_READS:
            raise RuntimeError('whole graph and material artifact reads forbidden in this run')


sys.addaudithook(safety)


def deadline(signum, frame):
    raise TimeoutError('original60s pure-data deadline exceeded')


signal.signal(signal.SIGALRM, deadline)
signal.setitimer(signal.ITIMER_REAL, 60)


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path, expected=None):
    path = Path(path)
    for p in (path, *path.parents):
        assert not p.is_symlink()
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1
    with path.open('rb') as f:
        assert identity(os.fstat(f.fileno())) == identity(before)
        data = f.read()
        assert identity(os.fstat(f.fileno())) == identity(before)
    assert identity(path.lstat()) == identity(before) and len(data) == before.st_size
    sha = hashlib.sha256(data).hexdigest()
    if expected is not None:
        assert sha == expected
    return dict(path=str(path), size_bytes=len(data), sha256=sha, identity=identity(before))


def checkpoint():
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform != 'darwin':
        rss *= 1024
    assert time.monotonic() - START < 60 and rss < 512 * 2**20
    assert threading.active_count() == 1 and not ATTEMPTS
    total = sum(p.lstat().st_size for p in OWN.rglob('*') if p.is_file() and not p.is_symlink())
    assert total < 64 * 2**20
    return dict(elapsed_seconds=time.monotonic()-START, own_peak_rss_bytes=rss,
                owned_regular_bytes=total, children_started=0,
                process_creation_attempts=list(ATTEMPTS))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def put(path, value):
    with Path(path).open('x', encoding='utf8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


assert sys.flags.optimize == 0 and sys.dont_write_bytecode
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    assert os.environ.get(key) == '1'
assert not OWN.exists()
OWN.mkdir(mode=0o700)
sources = [
    (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_20261011.py', 'c6e617b25d1df6fd5e1f18f2bd54b648e0abdd892659e51e3693eccb7b57b477'),
    (ROOT/'validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py', '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'),
    (BASE/'candidate_source/pure_helper_controls_NEW_EPOCH_CANDIDATE.py', '975833790097bd4484e6a41911e51cb5ed35dc85c367f5aed39a809908d58441'),
    (BASE/'candidate_source/wire67_original_fixture_definitions.py', '7591022b9e85c5852624e61ddc2b21170b5d98f0a66beea02f095d2321c8c5f3'),
    (BASE/'NEW_EPOCH_DATA_SUPPLEMENTS.py', None),
    (BASE/'preserved_source_basis/HISTORICAL_EXACT_Q_CONTRACT.py', 'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1'),
    (BASE/'preserved_source_basis/HISTORICAL_FULLFRESH_COMPLETE_CONTROLLER.py', 'b77f3530253d2fe7a70001cb23cf28482fd6e671e544f74f531fb22e70ae02a9'),
    (Path(__file__), None),
]
inputs = [pin(p, sha) for p, sha in sources]
metadata = [pin(META/'ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json'),
            pin(META/'ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json'),
            pin(ROOT/'validation/artifacts/axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json')]
for p, sha in sources:
    ast.parse(p.read_bytes())
index_metadata = json.loads(Path(metadata[0]['path']).read_bytes())
wire_metadata = json.loads(Path(metadata[1]['path']).read_bytes())
inverse = json.loads(Path(metadata[2]['path']).read_bytes())
a = sources[0][0].read_bytes()
b = sources[1][0].read_bytes()
assert a.count(inverse['exact_before'].encode()) == 1
assert b == a.replace(inverse['exact_before'].encode(), inverse['exact_after'].encode())
assert a == b.replace(inverse['exact_after'].encode(), inverse['exact_before'].encode())
aa, bb = ast.parse(a), ast.parse(b)
assert len(aa.body) == len(bb.body)
changed = [getattr(x,'name',type(x).__name__) for x,y in zip(aa.body,bb.body)
           if ast.dump(x,include_attributes=False) != ast.dump(y,include_attributes=False)]
assert changed == ['_wire_requirement_table_compact']
del a,b,aa,bb
old = load(sources[0][0], 'current_epoch_actual_old_c6e_stdlib_helper')
new = load(sources[1][0], 'current_epoch_actual_new_6a_stdlib_helper')
mother = load(sources[2][0], 'current_epoch_actual_mother_small_controls')
wire = load(sources[3][0], 'current_epoch_actual_original67_fixture_source')
index = load(sources[4][0], 'current_epoch_actual_synthetic_index_source')
assert mother.SOURCE_STATUS == 'UNREADY_CURRENT_ROOT_PURE_BINDING_REQUIRED'
before = checkpoint()
index_result = index.index_controls(new, index_metadata)
put(OWN/'ACTUAL_SYNTHETIC_INDEX_CONTROLS.json', index_result)
wire_result = wire.wire_fixture_controls(old, new)
assert [r['case'] for r in wire_result] == [r['case'] for r in wire_metadata['complete_saved_wire_control_result']['fixture_results']]
put(OWN/'ACTUAL_ALL67_WIRE_TINY_FIXTURES.json', dict(schema='NEW_EPOCH_ACTUAL_ALL67_WIRE_TINY_FIXTURES_ONLY_V1',
    fixture_results=wire_result, fixture_count=67, returns=14, raises=53,
    current_full238780_wire_and_fresh_payload_phase_reexecuted=False, new_Q_created=False))
artifacts = mother.Artifacts(OWN/'original_small_fixture_and_codec')
graph, fixture = mother.fixture_controls(new, artifacts)
codec = mother.codec_controls(new, graph, artifacts)
owner = mother.private_owner_consume_controls(new, graph)
assert len(codec['rejections']) == 61
assert [len(owner[k]) for k in ('positive_controls','private_guard_rejections','accepted_str_subclass_equivalence_controls','partial_invalid_second_owner_rejections')] == [4,3,2,2]
put(OWN/'ACTUAL_ORIGINAL_SMALL_FIXTURE_CODEC_OWNER_CONTROLS.json',
    dict(fixture=fixture, codec=codec, owner=owner))
contract_tree = ast.parse(sources[5][0].read_bytes())
fields = {}
for node in contract_tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in ('RETURN_FIELDS','SNAPSHOT_FIELDS'):
                fields[target.id] = ast.literal_eval(node.value)
assert len(fields['RETURN_FIELDS']) == 27 and len(fields['SNAPSHOT_FIELDS']) == 9
assert fields['SNAPSHOT_FIELDS'] == index.SNAPSHOT_FIELDS
for wanted in inputs + metadata:
    assert pin(wanted['path']) == wanted
result = dict(schema='SPOT_NEW_EPOCH_ACTUAL_STDLIB_SMALL_DATA_RECOVERY_CONTROLS_V1',
              status='ACTUAL_SMALL_DATA_CONTROLS_PASS_ONLY_NOT_FULL_PURE_FRESH_OR_Q',
              Source_inputs_before_after=inputs, historical_fixture_definition_metadata_inputs=metadata,
              historical_PASS_booleans_not_used_as_actual_result=True,
              old_new_whole_Source_forward_inverse_and_AST_difference_exact=changed,
              index=dict(attempts=35,unique_records=9,markers=2,standard_and_forced_collision_pass=True,
                         private_guards=13,last_use_failures=3),
              wire67=dict(fixtures=67,returns=14,raises=53,all_complete_case_definitions_order_retained=True),
              original_small_fixture_producer_and_all_rejections_pass=True,
              original_small_codec_rejections=61,original_owner_control_counts=[4,3,2,2],
              original27_fresh_return_fields_and9_snapshot_fields_retained_in_Source=fields,
              before=before,after=checkpoint(),
              limitations=[
                  'No original real Popen observation controls executed.',
                  'No complete saved graph or63379 creation trace read.',
                  'No full238780 edge wire comparison or current complete fresh observation executed.',
                  'Current480 absence entries and whole current27-field fresh return have not been verified.',
                  'The complete original OwnRSS host and current full resource ledger have not executed for this candidate.',
                  'This is a new controller candidate; lost original7ae399/c3a81/f133f Sources were not recovered byte exactly.',
              ],
              PS_native_or_numeric_process_started=False,children_started=0,
              full_original_pure_protocol_qualified=False,current_complete_fresh_qualified=False,
              new_Q_created=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)
put(OWN/'ACTUAL_SMALL_DATA_RESULT.json', result)
checkpoint()
signal.setitimer(signal.ITIMER_REAL, 0)
print(json.dumps(dict(status=result['status'], result=pin(OWN/'ACTUAL_SMALL_DATA_RESULT.json'),
                      index=result['index'],wire67=result['wire67'],
                      codec_rejections=61,owner_counts=[4,3,2,2],
                      children_started=0,new_Q_created=False)), flush=True)
