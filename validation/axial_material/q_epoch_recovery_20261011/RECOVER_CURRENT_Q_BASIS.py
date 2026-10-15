"""Recover durable Q Source bytes only; no helper import or protocol execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys
import threading
import time

START = time.monotonic()
ROOT = Path('/Users/wen/spot')
OUT = Path(__file__).resolve().parent
TARGETS = {
    72784: ('pure_helper_controls.py', '7ae39903114ec50ab77b203edd7cf88f16690c0519af3e2e8877dbe28d8700a8'),
    14682: ('read_open_short_index_state_controls.py', 'c3a81b4cfd93f40e458e999305e6917227ad3fbb08d4b6116ed6cddf281d6f95'),
    43643: ('wire67_saved_evidence_review.py', 'f133f92b39c5376dd719eb3942ac7049c34a850c500afd79028b63f12b9a207c'),
    152950: ('combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py', '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'),
}
ATTEMPTS = []


def forbid(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.exec',
                 'os.posix_spawn', 'os.spawn', 'os.startfile', 'os.startfile/2'):
        ATTEMPTS.append(event)
        raise RuntimeError('Source recovery forbids process creation')


sys.addaudithook(forbid)


def deadline(signum, frame):
    raise TimeoutError('600 second Source recovery cap')


signal.signal(signal.SIGALRM, deadline)
signal.setitimer(signal.ITIMER_REAL, 600)


def checkpoint():
    elapsed = time.monotonic() - START
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if sys.platform != 'darwin':
        rss *= 1024
    assert elapsed < 600 and rss < 512 * 2**20
    assert threading.active_count() == 1 and not ATTEMPTS
    return dict(elapsed_seconds=elapsed, own_peak_rss_bytes=rss,
                Python_process_creation_attempts=list(ATTEMPTS),
                scope='Python named process events after hook; no native process claim')


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def source_bytes(path, expected=None):
    path = Path(path).absolute()
    for ancestor in (path, *path.parents):
        assert not ancestor.is_symlink(), str(ancestor)
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1, str(path)
    before = identity(s)
    with path.open('rb') as stream:
        assert identity(os.fstat(stream.fileno())) == before
        data = stream.read()
        assert identity(os.fstat(stream.fileno())) == before
    assert identity(path.lstat()) == before and len(data) == s.st_size
    digest = hashlib.sha256(data).hexdigest()
    if expected is not None:
        assert digest == expected, str(path)
    return data, dict(path=str(path), size_bytes=len(data), sha256=digest,
                      identity=before)


def put_bytes(path, data):
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def put_json(path, value):
    put_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2,
                               allow_nan=False) + '\n').encode())


def pairs(rows):
    out = {}
    for key, value in rows:
        assert key not in out
        out[key] = value
    return out


def nonfinite(value):
    raise ValueError('nonfinite preserved metadata ' + value)


def read_json(path):
    data, pin = source_bytes(path)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=nonfinite), pin


assert sys.flags.optimize == 0 and sys.dont_write_bytecode
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    assert os.environ.get(name) == '1', name
assert set(p.name for p in OUT.iterdir()) == {'RECOVER_CURRENT_Q_BASIS.py'}
self_data, self_pin = source_bytes(__file__)
ast.parse(self_data)
scan = []
matches = {name: [] for name, digest in TARGETS.values()}
files_checked = 0
symlink_entries_not_followed = []
for scope in (ROOT/'validation/axial_material', ROOT/'validation/artifacts'):
    for directory, dirs, names in os.walk(scope, followlinks=False):
        kept = []
        for name in dirs:
            p = Path(directory)/name
            if p.is_symlink():
                symlink_entries_not_followed.append(str(p))
            else:
                kept.append(name)
        dirs[:] = kept
        for name in names:
            p = Path(directory)/name
            s = p.lstat()
            files_checked += 1
            if not stat.S_ISREG(s.st_mode) or s.st_size not in TARGETS:
                continue
            data, pin = source_bytes(p)
            target_name, digest = TARGETS[s.st_size]
            row = dict(current_pin=pin, sought_name=target_name,
                       whole_bytes_match=pin['sha256'] == digest)
            scan.append(row)
            if row['whole_bytes_match']:
                ast.parse(data)
                matches[target_name].append(pin)
        checkpoint()

helper_name, helper_sha = TARGETS[152950]
helper_matches = matches[helper_name]
assert len(helper_matches) >= 5
helper_path = ROOT/'validation/axial_material'/helper_name
helper_data, helper_pin = source_bytes(helper_path, helper_sha)
recovered = OUT/'recovered_exact_source'
recovered.mkdir(mode=0o700)
put_bytes(recovered/helper_name, helper_data)
copied_data, copied_pin = source_bytes(recovered/helper_name, helper_sha)
assert copied_data == helper_data
ast.parse(copied_data)

ART = ROOT/'validation/artifacts'
BASE = ROOT/'validation/axial_material/complete_history_root_index_source_v15_20261010'
source_basis = [
    (BASE/'actual_complete_graph_helper_controls_v25_sources/pure_helper_controls.py',
     '6ac338e3f54523210f81c1226c0954f86d047bad8e90af1ecaec539b796058cc',
     'V25_PURE_MOTHER_NOT_RECOVERED_NEW6A_PURE.py'),
    (ART/'axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011/actual_closed_S/inactive_audit_snapshot_controls_SOURCE_ONLY.py',
     'd439eb9641f45e09c17814a38a16dc7e2cbb6120fc09119df901e415daf28483',
     'ORIGINAL_COMPLETE_INACTIVE_SNAPSHOT_CONTROLS.py'),
    (ART/'axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011/actual_closed_S/fresh_verifier_controls.py',
     'b77f3530253d2fe7a70001cb23cf28482fd6e671e544f74f531fb22e70ae02a9',
     'HISTORICAL_FULLFRESH_COMPLETE_CONTROLLER.py'),
    (ART/'axial-material-stable-wire-sort-fullfresh-root-closure-v28-20261011/actual_closed_S/fresh_verifier_host.py',
     'cbcebb9b625ac27189d38ef260458ffdf540df2c50bcef07b7b036480dbd02c6',
     'HISTORICAL_FULLFRESH_ORIGINAL_HOST.py'),
    (ART/'axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/BOUNDED_COMPLETE_WIRE_SORT_CONTROL.py',
     '09cbab061de6c3c28f6268bf88a6f3e1fcd4f5ff428cf5fd3d955e1cac87e5b3',
     'ORIGINAL_BOUNDED_COMPLETE_WIRE67_CONTROLLER.py'),
    (ART/'axial-material-installed6a-Q-Root-closed-binding-v29-20261011/retained/input_0007/installed6a_closed_metadata_admission_contract.py',
     'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1',
     'HISTORICAL_EXACT_Q_CONTRACT.py'),
]
basis = OUT/'preserved_source_basis'
basis.mkdir(mode=0o700)
copies = []
for path, expected, name in source_basis:
    data, before = source_bytes(path, expected)
    ast.parse(data)
    put_bytes(basis/name, data)
    after_data, after = source_bytes(basis/name, expected)
    ast.parse(after_data)
    assert after_data == data and source_bytes(path, expected)[1] == before
    copies.append(dict(original_current_pin=before, new_copy_pin=after,
                       byte_exact_forward_and_inverse_equal=True,
                       syntax_parse_passed=True,
                       protocol_or_helper_import_executed=False))
    checkpoint()

index, index_pin = read_json(ART/'axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_READ_OPEN_SHORT_INDEX_STATE_CONTROLS.json')
wire, wire_pin = read_json(ART/'axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4/ACTUAL_SAVED_WIRE67_COMPLETE_FIELDS_REVIEW.json')
inverse, inverse_pin = read_json(ART/'axial-material-stable-wire-sort-source-install-20261011/pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json')
assert len(index['all_original_guards_with_nonempty_markers']) == 13
assert len(index['original_last_use_failure_with_nonempty_markers']) == 3
assert (index['actual_attempts'], index['unique_records'],
        index['exception_count_bearing_markers']) == (35, 9, 2)
assert (wire['fixture_count'], wire['returns'], wire['raises']) == (67, 14, 53)
assert len(wire['complete_saved_wire_control_result']['fixture_results']) == 67
assert source_bytes(__file__)[1] == self_pin
for row in scan:
    assert source_bytes(row['current_pin']['path'])[1] == row['current_pin']
for row in copies:
    assert source_bytes(row['original_current_pin']['path'])[1] == row['original_current_pin']
assert source_bytes(helper_path, helper_sha)[1] == helper_pin

report = dict(
    schema='SPOT_CURRENT_Q_DURABLE_SOURCE_RECOVERY_ONLY_V1',
    status='EXACT_INSTALLED6A_SOURCE_RECOVERED_THREE_NEW_PURE_CONTROLLERS_NOT_FOUND_AS_REGULAR_PROJECT_FILES',
    scope='Source bytes and syntax only; no current Q, PREP, BUILD, Native, ROOT64, or science admission',
    old_historical_OS_identities_reused_as_current=False,
    new_copy_OS_identity_is_distinct_and_recorded=True,
    ignored_paths_included=True,
    scanned_roots=[str(ROOT/'validation/axial_material'), str(ROOT/'validation/artifacts')],
    directory_regular_file_size_search_count=files_checked,
    symlink_entries_not_followed=symlink_entries_not_followed,
    exact_size_candidate_whole_EOF_results=scan,
    exact_current_source_matches=matches,
    recovered_installed6a=dict(source=helper_pin, new_copy=copied_pin,
                              whole_forward_inverse_byte_equal=True,
                              pure_syntax_parse_passed=True),
    preserved_Source_basis=copies,
    durable_complete_historical_control_logic_evidence=[index_pin, wire_pin, inverse_pin],
    historical_control_results_are_not_new_current_pass_results=True,
    minimum_remaining_control_logic=dict(
        new6a_pure='Rebind the entire V25 pure mother to unchanged6a; preserve all five stages, producer/reject/subtype/owner/codec/full graph/full trace/snapshot controls; add complete index and saved wire67 supplements.',
        index='Use actual6a ReadOpenAudit plus all original snapshot-control fixtures; preserve 35 synthetic attempts, nine unique records, two markers, standard/forced collision full nine-field comparison, default/False/True behavior, all13 guards and all3 last-use failures, original canonical key-byte oracle.',
        wire67='The preserved wire67 controller has all67 real fixtures and full original/candidate wire functions; the saved review binds every original field, full wire EOF equality and historical fresh observation. A current observation must be real; never relabel the historical observation as current.',
        fresh='Preserved complete controller retains all27 public fields, all9 snapshot fields, complete same-phase reads, unfiltered gzip wires and private four-positive/three-rejection controls. Rebind to newly verified whole current input and retain every absence input, including current480 when supplied by Root.',
        resources='Keep original60s pure,1800s whole/600s fresh stage,512MiB RSS,64MiB protocol archive,one thread,one business child,retries0; retain2GiB fresh,96GiB history,8GiB free and full current resource scope.'),
    recovery_Source=self_pin,
    final_checkpoint=checkpoint(),
    metadata_sources_imported=False,
    helper_or_protocol_executed=False,
    numerical_or_PS_or_native_subprocesses_started=False,
    new_Q_created=False,
    whole_INPUT_admitted=False,
    science_or_BOOT_admitted=False,
)
put_json(OUT/'SOURCE_RECOVERY_AUDIT.json', report)
report_pin = source_bytes(OUT/'SOURCE_RECOVERY_AUDIT.json')[1]
signal.setitimer(signal.ITIMER_REAL, 0)
print(json.dumps(dict(status=report['status'], recovered_helper=copied_pin,
                      source_basis_files=len(copies), source_scan_files=files_checked,
                      missing_three_new_pure_Source_names=[n for n in matches if not matches[n]],
                      report=report_pin, helper_or_protocol_executed=False,
                      new_Q_created=False), ensure_ascii=False), flush=True)
