import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import stat
import sys

sys.dont_write_bytecode = True
REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
PKG = REC / 'current_material_evidence_empty_root_cumulative_twelve_roots_source_v4_20261014'
DEST = REC / 'independent_empty_root_cumulative12_aggregate_final_SF_HF_request_ROOT30_metadata_review_20261014'


def require(value, label):
    if not value:
        raise RuntimeError(label)


def ident(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(p):
    q = Path(p['path'])
    for a in (q, *q.parents):
        require(not a.is_symlink(), 'ordinary exact path, no ancestor alias')
    s = q.lstat()
    require(stat.S_ISREG(s.st_mode) and ident(s) == p['identity'] and s.st_size == p['size_bytes'], 'current exact regular seven fields ' + str(q))
    require(all(type(v) is int for v in p['identity']), 'strict integer seven fields')


def pin(q):
    q = Path(q).absolute()
    s = q.lstat()
    require(stat.S_ISREG(s.st_mode), 'regular metadata file')
    fd = os.open(q, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        require(ident(os.fstat(f.fileno())) == ident(s), 'metadata open identity')
        sha = hashlib.file_digest(f, 'sha256').hexdigest()
        require(ident(os.fstat(f.fileno())) == ident(s), 'metadata EOF identity')
    require(ident(q.lstat()) == ident(s), 'metadata path after EOF')
    p = dict(path=str(q), sha256=sha, size_bytes=s.st_size, identity=ident(s))
    current(p)
    return p


def read(q):
    p = pin(q)
    value = json.loads(Path(p['path']).read_bytes())
    current(p)
    return value, p


def write(q, value):
    fd = os.open(q, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    with os.fdopen(fd, 'wb') as f:
        f.write((json.dumps(value, indent=2, allow_nan=False) + '\n').encode())
        f.flush()
        os.fsync(f.fileno())
    d = os.open(q.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(d)
    finally:
        os.close(d)
    return pin(q)


sf, psf = read(PKG / 'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')
hf, phf = read(PKG / 'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json')
dyn, pdyn = read(PKG / 'ROOT_REVIEWABLE_MATERIAL_EVIDENCE_DYNAMIC_INTERFACE_SOURCE_ONLY.json')
cli, pcli = read(REC / 'ROOT_EXACT_EMPTY_ROOT_CUMULATIVE12_AGGREGATE_REQUEST_PREPARATION_ARGV_20261014.json')
argv, pargv = read(REC / 'ROOT_EXACT_EMPTY_ROOT_CUMULATIVE12_FIRST_A_COMPLETE_AGGREGATE_ACTUAL_ARGV_20261014.json')
raw, praw = read(REC / 'ROOT_ACTUAL_EMPTY_ROOT_CUMULATIVE12_AGGREGATE_REQUEST_PREPARATION_TRUE_TOOL_RETURNS_20261014.json')
request, preq = read(REC / 'first_A_empty_root_cumulative12_aggregate_request_20261014_v1/CURRENT_ACTUAL_MATERIAL_EVIDENCE_REQUEST.json')
post, ppost = read(REC / 'independent_literal2_old_map005006_before_aggregate_actual_exact_release_postverify_20261014/REVIEW.json')
posttools, pposttools = read(REC / 'independent_literal2_old_map005006_before_aggregate_actual_exact_release_postverify_20261014/TRUE_TOOL_RETURNS.json')
receipt, preceipt = read(post['actual_release_receipt_pin']['path'])

require(len(sf['complete_source_file_pins']) == 13 and len(hf['dependencies']) == 5955 and len(request['complete_input_pins']) == 5937, 'real complete Source/HF/request counts')
require(sf['candidate_executed'] is False and hf['candidate_executed'] is False, 'Source-only frozen package')
table = {}
for p in sf['complete_source_file_pins'] + hf['dependencies'] + request['complete_input_pins']:
    require(p['path'] not in table or table[p['path']] == p, 'one exact full identity per path')
    table[p['path']] = p
for p in table.values():
    current(p)
source_pins = []
for p in sf['complete_source_file_pins']:
    require(pin(p['path']) == p, 'full exact small Source bytes')
    source_pins.append(p)

require(len(cli['exact_argv']) == 25 and shlex.split(cli['exact_command']) == cli['exact_argv'], 'actual exact request preparation 25')
require(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and raw['original_integer_exit_code'] == 0, 'request preparation real closed zero')
t = raw['actual_terminal_return']
require(type(t['exit_code']) is int and t['exit_code'] == 0 and t.get('session_id') is None, 'real terminal zero no live session')
require(shlex.split(raw['exact_executed_command']) == cli['exact_argv'], 'exact actually executed request command')
observed = json.loads(t['output'].strip())
require(observed['request'] == preq and observed['status'] == 'CURRENT_ACTUAL_EVIDENCE_REQUEST_PREPARED_NO_BUSINESS_EXECUTION', 'actual request receipt exact PF')
require(len(dyn['known_argv_prefix']) == 24 and dyn['required_actual_prefix'] == 'request', 'published original dynamic interface')
expected = dyn['known_argv_prefix'] + ['--request-summary', preq['path'], '--request-sha256', preq['sha256'], '--request-seven-id', json.dumps(preq['identity'], separators=(',', ':'))]
require(argv['argv'] == expected and len(expected) == 30 and shlex.split(argv['exact_command']) == expected, 'exact published 24 plus genuine request six')
require(argv['request_pin'] == preq and argv['published_dynamic_interface_pin'] == pdyn and argv['actual_executed'] is False, 'real Root command binding not future execution')
require(request['operation'] == 'aggregate' and request['complete_source_freeze_pin'] == psf and request['actual_stage_executed'] is False, 'request only same immutable aggregation package')
roots = request['joint_archive_roots']
require(len(roots) == 12 and len(set(roots)) == 12 and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b), 'twelve complete disjoint cumulative roots')
require(roots[:5] == request['original_five_role_roots'] and roots[2] == request['exact_retained_original_observed_root'] and roots[5] == request['exact_retained_completion_metadata_root'], 'original physical A owner and separate closure preserved')
require(not os.path.lexists(roots[0]) and not os.path.lexists(roots[1]), 'fresh aggregate output pair absent')
require(Path(roots[3]) == PKG and Path(roots[4]) == Path(preq['path']).parent, 'own Source and request complete roots')
capsnode = next(n for n in ast.parse((PKG / 'current_material_lineage_evidence.py').read_bytes()).body if isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'CAPS' for x in n.targets))
ns = {}
exec(compile(ast.Module(body=[capsnode], type_ignores=[]), '<original literal CAPS only>', 'exec'), {}, ns)
require(request['original_caps'] == ns['CAPS'], 'exact original unchanged caps')
binding = request['aggregation_binding']
require(binding['state_order'] == ['A'] and binding['Source_route'] == dict(ITSTMP=0, historical_call_proved=False), 'same physical A only original route')
state = binding['actual_context_states']['A']
require(len(state['all_snapshot_pairs']) == 8 and len(state['complete_context_pins']) == 55, 'complete original pairs and contexts')
coverage, pcoverage = read(request['actual_extraction_independent_review_pin']['path'])
require(pcoverage == request['actual_extraction_independent_review_pin'] and coverage['schema'] == 'ROOT_ACTUAL_CURRENT_MATERIAL_EXTRACTION_REVIEW_V1' and coverage['all_original_snapshot_and_context_pins_verified'] is True, 'genuine dedicated same actual independent extraction coverage')
require(coverage['all_snapshot_pairs'] == state['all_snapshot_pairs'] and coverage['complete_context_pins'] == state['complete_context_pins'] and coverage['actual_extraction_report_pin'] == state['actual_extraction_report_pin'] and coverage['actual_observation_manifest_pin'] == request['actual_observation_manifest_pin'], 'complete actual coverage relationships')
require(post['failure'] is None and post['actual_release_receipt_pin'] == preceipt and receipt['deleted_files'] == 2 and receipt['logical_bytes_released'] == 463397752, 'actual exact two obsolete map release')
for k in ('actual_review_return', 'actual_postverification_return'):
    v = posttools[k]
    require(type(v['exit_code']) is int and v['exit_code'] == 0 and v.get('session_id') is None, 'genuine release independent post tools ' + k)
    require(json.loads(v['output'].strip().splitlines()[-1])['review_pin'] == ppost, 'actual post stdout PF')
require(posttools['observed_closed'] is True and type(posttools['original_integer_exit_code']) is int and posttools['original_integer_exit_code'] == 0, 'actual release post closed zero')
before_snapshot = receipt['original_budget_after']
require(before_snapshot['original_initial_reserve_admitted'] is True and before_snapshot['remaining_after_original_initial_reserves_bytes'] == 149537172, 'actual original factory after release full reserve')
common = REC / 'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014/literal11_release_common.py'
spec = importlib.util.spec_from_file_location('exact_original_budget_metadata_for_aggregate_review', common)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
budget = module.budget()
require(budget['original_initial_reserve_admitted'] is True and budget['remaining_after_original_initial_reserves_bytes'] > 0, 'current genuine original full fresh2/cold/meta/free factory')
for p in table.values():
    current(p)
for p in (psf, phf, pdyn, pcli, pargv, praw, preq, ppost, pposttools, preceipt, pcoverage):
    current(p)
DEST.mkdir()
result = dict(schema='INDEPENDENT_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_FINAL_METADATA_INTEGRATION_REVIEW_V1', status='PASS_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_FINAL_METADATA_READY_FOR_UNIQUE_RUNTIME', failure=None,
    source_only=True, business_executed=False, compiler_executed=False, numerical_executed=False, files_deleted=False,
    actual_Source_freeze_pin=psf, actual_Host_freeze_pin=phf, actual_dynamic_interface_pin=pdyn, actual_request_preparation_CLI_pin=pcli,
    actual_request_pin=preq, actual_Root_argv_pin=pargv, actual_request_preparation_true_tool_pin=praw,
    actual_cleanup_post_pin=ppost, actual_cleanup_post_tools_pin=pposttools, actual_cleanup_release_receipt_pin=preceipt,
    actual_extraction_review_pin=pcoverage, reviewer_source_pin=pin(__file__),
    complete_source_count=13, current_HF_dependency_count=5955, current_request_input_count=5937, complete_distinct_current_pin_count=len(table),
    all_declared_current_pins_seven_fields_verified_twice=True, complete_small_Source_file_bytes_verified=True,
    no_scientific_payload_EOF_or_native_tree_read_by_reviewer=True, original_caps=request['original_caps'], cumulative_joint_roots=roots,
    actual_original_factory_after_release_snapshot={k: before_snapshot[k] for k in ('artifact_bytes', 'regular_files', 'disk_free_bytes', 'remaining_after_original_initial_reserves_bytes', 'original_initial_reserve_admitted')},
    actual_current_original_factory_metadata={k: budget[k] for k in ('artifact_bytes', 'regular_files', 'disk_free_bytes', 'remaining_after_original_initial_reserves_bytes', 'original_initial_reserve_admitted')},
    actual_aggregate_runtime_return=None, actual_aggregate_report_pin=None, actual_GENDF_report_pin=None, physics_qualified=False, goal_complete=False)
review = write(DEST / 'REVIEW.json', result)
print(json.dumps(dict(status=result['status'], review_pin=review), allow_nan=False))
