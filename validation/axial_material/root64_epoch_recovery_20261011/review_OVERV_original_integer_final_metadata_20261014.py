"""Final metadata only; original data and all native programs remain untouched."""
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
PKG = REC / 'OVERV_original_guarded_integer_control_source_v3_20261014'
DEST = REC / 'independent_OVERV_original_integer_final_SF_HF_CLI_ROOT24_metadata_review_20261014'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(expected):
    p = Path(expected['path'])
    require(p.is_absolute() and not any(q.is_symlink() for q in (p, *p.parents)), 'ordinary exact path')
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == expected['identity'] and s.st_size == expected['size_bytes'],
            'current exact seven fields ' + str(p))


def pin(path):
    p = Path(path).absolute()
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_size < 64 * 2 ** 20, 'bounded Source/metadata')
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        require(identity(os.fstat(f.fileno())) == identity(s), 'opened7')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        require(identity(os.fstat(f.fileno())) == identity(s), 'EOF7')
    result = dict(path=str(p), sha256=digest, size_bytes=s.st_size, identity=identity(s))
    current(result)
    return result


def read(path):
    expected = pin(path)
    result = json.loads(Path(path).read_bytes())
    current(expected)
    return result, expected


def write(path, value):
    with path.open('xb') as f:
        f.write((json.dumps(value, indent=2, allow_nan=False) + '\n').encode())
        f.flush()
        os.fsync(f.fileno())
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return pin(path)


sf, psf = read(PKG / 'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE.json')
hf, phf = read(PKG / 'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE.json')
cli, pcli = read(PKG / 'ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json')
root, proot = read(REC / 'ROOT_EXACT_OVERV_ORIGINAL_INTEGER_ACTUAL24_ARGV_20261014.json')
publication, ppublication = read(REC / 'ROOT_ACTUAL_OVERV_ORIGINAL_INTEGER_SOURCE_ONCE_PUBLICATION_TRUE_TOOL_RETURNS_20261014.json')
plan, pplan = read(sf['control_plan_pin']['path'])
require(pplan == sf['control_plan_pin'] and len(sf['selected_Source_pins']) == 8 and len(hf['dependencies']) == 36,
        'actual Source8/HF36 counts')
require(sf['source_only'] is True and hf['source_only'] is True and sf['compiler_executed'] is False and
        hf['compiler_executed'] is False and sf['actual_current_control_report_pin'] is None and
        hf['actual_current_control_report_pin'] is None, 'source only no actual control filled')
require(hf['selected_source_freeze_pin'] == psf and cli['source_freeze_pin'] == psf and
        cli['host_freeze_pin'] == phf and cli['host_source_pin'] == hf['host_source_pin'],
        'exact actual published Source/Host/runtime wiring')
require(publication['observed_closed'] is True and type(publication['original_integer_exit_code']) is int and
        publication['original_integer_exit_code'] == 0, 'real publication closed0')
t = publication['actual_terminal_return']
require(type(t['exit_code']) is int and t['exit_code'] == 0 and t.get('session_id') is None, 'true typed terminal0')
stdout = json.loads(t['output'])
require(stdout['Source_freeze_pin'] == psf and stdout['Host_freeze_pin'] == phf and stdout['CLI_pin'] == pcli,
        'original publication stdout exact PFs')
published_args = shlex.split(publication['exact_executed_command'])
writer = next(p for p in sf['selected_Source_pins'] if Path(p['path']).name == 'write_once_original_OVERV_integer_control_Source_HF_CLI.py')
require(published_args[2] == writer['path'] and len(published_args) == 21,
        'actual Source-only direct Python publication3 plus eighteen authority arguments')
table = {}
for expected in sf['selected_Source_pins'] + hf['dependencies']:
    require(expected['path'] not in table or table[expected['path']] == expected, 'unique actual fullPF per path')
    table[expected['path']] = expected
for expected in table.values():
    current(expected)
for expected in sf['selected_Source_pins']:
    require(pin(expected['path']) == expected, 'bounded selected Source full SHA')
require(len(cli['argv']) == 24 and root['argv'] == cli['argv'] and
        shlex.split(root['shell_safe_command']) == cli['argv'], 'actual exact 24-token runtime')
require(cli['argv'][:3] == ['/usr/bin/env', '-u', 'PYTHONOPTIMIZE'] and
        all(value in cli['argv'][:11] for value in
        ['PYTHONDONTWRITEBYTECODE=1', 'OMP_NUM_THREADS=1', 'OPENBLAS_NUM_THREADS=1',
         'MKL_NUM_THREADS=1', 'VECLIB_MAXIMUM_THREADS=1', 'NUMEXPR_NUM_THREADS=1']) and
        cli['argv'][10] == '-B' and cli['argv'][11] == hf['host_source_pin']['path'],
        'unchanged original runtime Python/thread/no-bytecode interface')
expected_tail = []
for role, p in [('source-freeze', psf), ('host-freeze', phf)]:
    expected_tail += ['--' + role + '-summary', p['path'], '--' + role + '-sha256', p['sha256'],
                     '--' + role + '-seven-id', json.dumps(p['identity'], separators=(',', ':'))]
require(cli['argv'][12:] == expected_tail and cli['planned_actual_output_root'] == plan['planned_actual_output_root'],
        'exact current Source/Host argument triples')
peer, ppeer = read(sf['same_round_Source_review_pin']['path'])
peertools, ppeertools = read(sf['same_round_Source_tools_pin']['path'])
require(ppeer == sf['same_round_Source_review_pin'] and ppeertools == sf['same_round_Source_tools_pin'] and
        peer['source_only'] is True and peer['failure'] is None, 'actual same-round Source review')
review_return = peertools['actual_review_return']
require(type(review_return['exit_code']) is int and review_return['exit_code'] == 0 and
        review_return.get('session_id') is None and json.loads(review_return['output'])['review_pin'] == ppeer,
        'genuine original independent Source0 exactstdoutPF')
roots = plan['cumulative_joint_roots']
require(roots == peer['complete_cumulative_roots'] and len(roots) == len(set(roots)) == 20 and
        not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b), 'twenty disjoint retained roots')
explicit = plan['explicit_cumulative_metadata_file_pins']
require(explicit == peer['explicit_cumulative_metadata_file_pins'] and len(explicit) == 2,
        'two exact extra metadata resources retained')
for p in explicit:
    require(pin(p['path']) == p, 'actual bounded explicit metadata PF')
require(sf['original_caps'] == hf['original_caps'] == plan['original_caps'] == peer['original_caps'],
        'exact original caps persist through publication')
require(not os.path.lexists(plan['planned_actual_output_root']), 'fresh control output absent')
budget_path = REC / 'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014/literal11_release_common.py'
spec = importlib.util.spec_from_file_location('original_current_factory_metadata_for_OVERV_final', budget_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
budget = module.budget()
require(budget['original_initial_reserve_admitted'] is True and
        budget['remaining_after_original_initial_reserves_bytes'] > 0, 'real complete-family fullfresh2/cold/meta/free reserve')
for expected in table.values():
    current(expected)
for expected in (psf, phf, pcli, proot, ppublication, pplan, ppeer, ppeertools, *explicit):
    current(expected)
DEST.mkdir()
result = dict(schema='INDEPENDENT_OVERV_ORIGINAL_INTEGER_FINAL_SF_HF_CLI_ROOT24_METADATA_REVIEW_V1',
              status='PASS_OVERV_ORIGINAL_INTEGER_FINAL_METADATA_READY_FOR_UNIQUE_THREE_STAGE_RUNTIME',
              source_only=True, failure=None, business_executed=False, compiler_executed=False,
              numerical_executed=False, files_deleted=False, physics_qualified=False,
              historical_machine_bit_replay=False, original_SOURCE_CONTEXT_NOT_SAVED_issue_removed=False,
              actual_Source_freeze_pin=psf, actual_Host_freeze_pin=phf, actual_CLI_pin=pcli,
              actual_Root_argv_pin=proot, actual_publication_true_tool_pin=ppublication,
              actual_same_round_Source_review_pin=ppeer, actual_same_round_Source_tools_pin=ppeertools,
              reviewer_source_pin=pin(__file__), actual_selected_Source_count=8,
              actual_HF_dependency_count=36, complete_distinct_current_pin_count=len(table),
              all_current_seven_fields_verified_twice=True, selected_small_Source_complete_SHA_verified=True,
              exact_runtime_argv_count=24, exact_actual_direct_Source_publication_argv_count=21,
              original_reviewable_env_Source_publication_argv_count=30,
              cumulative_joint_roots=roots, explicit_cumulative_metadata_file_pins=explicit,
              original_caps=plan['original_caps'],
              actual_current_original_factory_metadata={key: budget[key] for key in
                ('artifact_bytes', 'regular_files', 'disk_free_bytes',
                 'remaining_after_original_initial_reserves_bytes', 'original_initial_reserve_admitted')},
              no_actual_ENERGY_or_OVERV_payload_or_SQLite_rows_read_by_reviewer=True,
              no_scientific_archive_EOF_or_native_tree_read_by_reviewer=True,
              actual_control_report_pin=None, actual_control_object_pin=None, actual_control_executable_pin=None)
review = write(DEST / 'REVIEW.json', result)
print(json.dumps(dict(status=result['status'], review_pin=review), allow_nan=False), flush=True)
