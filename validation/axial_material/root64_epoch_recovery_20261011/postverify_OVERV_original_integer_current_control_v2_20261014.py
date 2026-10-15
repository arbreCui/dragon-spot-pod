"""Sole bounded postverification; only this control's fourteen new files are hashed."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shlex
import stat
import sys

sys.dont_write_bytecode = True
REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
PKG = REC / 'OVERV_original_guarded_integer_control_source_v3_20261014'
OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-new-OVERV-original-integer-current-control-20261014-v1')
DEST = REC / 'independent_OVERV_original_integer_current_control_actual_postverify_20261014'
CACHE = {}


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(p):
    q = Path(p['path'])
    require(q.is_absolute() and not any(a.is_symlink() for a in (q, *q.parents)), 'ordinary exact current path')
    s = q.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == p['identity'] and s.st_size == p['size_bytes'],
            'current exact seven fields ' + str(q))


def load(path):
    q = Path(path).absolute()
    if str(q) in CACHE:
        p, raw = CACHE[str(q)]
        current(p)
        return p, raw
    before = q.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_uid == os.getuid()
            and before.st_size < 64 * 2 ** 20, 'bounded ordinary metadata/new output')
    with os.fdopen(os.open(q, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        require(identity(os.fstat(f.fileno())) == identity(before), 'opened full7')
        raw = f.read()
        require(identity(os.fstat(f.fileno())) == identity(before), 'after complete EOF7')
    p = dict(path=str(q), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=identity(before))
    current(p)
    CACHE[str(q)] = (p, raw)
    return p, raw


def read(path):
    p, raw = load(path)
    return json.loads(raw), p


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
    return load(path)[0]


report, preport = read(OUT / 'Root_actual_OVERV_original_current_integer_control_summary.json')
sf, psf = read(PKG / 'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_SOURCE_ONLY_FREEZE.json')
hf, phf = read(PKG / 'COMPLETE_ORIGINAL_OVERV_INTEGER_CONTROL_HOST_SOURCE_ONLY_FREEZE.json')
cli, pcli = read(PKG / 'ROOT_REVIEWABLE_ORIGINAL_OVERV_INTEGER_CURRENT_CONTROL_ARGV.json')
root, proot = read(REC / 'ROOT_EXACT_OVERV_ORIGINAL_INTEGER_ACTUAL24_ARGV_20261014.json')
raw, praw = read(REC / 'ROOT_ACTUAL_OVERV_ORIGINAL_INTEGER_ACTUAL24_TRUE_TOOL_RETURNS_20261014.json')
plan, pplan = read(sf['control_plan_pin']['path'])
require(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and
        raw['original_integer_exit_code'] == 0, 'actual closed Root0')
terminal = raw['actual_terminal_return']
require(type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and terminal.get('session_id') is None,
        'genuine typed no-session terminal0')
require(json.loads(terminal['output'])['report_pin'] == preport and root['argv'] == cli['argv'] and
        len(root['argv']) == 24 and shlex.split(raw['exact_executed_command']) == root['argv'] and
        shlex.split(root['shell_safe_command']) == root['argv'], 'true terminal stdout and exact actual24')
require(report['schema'] == 'ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_GUARDED_REPORT_V1' and
        report['status'] == 'ACTUAL_CURRENT_OVERV_NATIVE_INTEGER_CONTROL_CLOSED0_ONLY' and
        report['failure'] is None and report['secondary_failures'] == [] and
        report['final_report_resource_check_passed'] is True, 'original success facts no changes to sealed report')
require(len(report['fixed_current_pins']) == 43 and len(hf['dependencies']) == 36 and
        len(report['output_pins']) == 13, 'actual fixed43/HF36/new13 counts')
table = {}
for p in report['fixed_current_pins'] + hf['dependencies']:
    require(p['path'] not in table or table[p['path']] == p, 'one canonical current PF')
    table[p['path']] = p
for p in table.values():
    current(p)
expected_outputs = {p['path']: p for p in report['output_pins']}
require(len(expected_outputs) == 13 and all(Path(path).is_relative_to(OUT) for path in expected_outputs),
        'exact thirteen new controlled output paths')
actual_paths = {str(p) for p in OUT.rglob('*') if p.is_file()}
require(actual_paths == set(expected_outputs) | {preport['path']} and len(actual_paths) == 14,
        'complete new scene fourteen files including original summary')
outputs = []
for path in sorted(expected_outputs):
    p, _ = load(path)
    require(p == expected_outputs[path], 'complete new output EOF/PF')
    outputs.append(p)
outputs.append(preport)
records = report['records']
require([r['label'] for r in records] == ['build/compile_control', 'build/link_control', 'control/run_current_control'] and
        all(r['status'] == 'PASS' and r['wall_cap_seconds'] == 600 for r in records), 'three original successful native stages')
require(records[0]['command'] == report['actual_compile_command'] and
        records[1]['command'] == report['actual_link_command'], 'actual compile/link commands retained')
require(records[0]['command'][:10] == [plan['original_compiler_pin']['path'], *plan['original_compile_flags']] and
        [q for q in records[0]['command'] if q.startswith('-I')] == plan['original_compile_include_arguments'] and
        [q for q in records[1]['command'] if q.endswith('.a')] == [p['path'] for p in plan['original_four_archive_pins']],
        'original compiler/nineflags/module roles/four archive order')
watch_results = []
for record in records:
    label = record['label']
    logpin, _ = load(OUT / (label + '.log'))
    require(logpin['sha256'] == record['log_sha256'], 'actual whole stage log')
    watch, watchpin = read(OUT / (label + '.watchdog.json'))
    declared = [p for p in report['actual_watchdog_checks'] if p['path'] == watchpin['path']]
    require(len(declared) == 1 and declared[0]['sha256'] == watchpin['sha256'], 'actual original watchdog declaration')
    require(type(watch['returncode']) is int and watch['returncode'] == 0 and watch['limit_failure'] is None and
            watch['command'] == record['command'] and watch['own_child_only'] is True and
            watch['liveness_group_cleanup'] is True and watch['rss_cap_mib'] == 512 and
            0 < watch['wall_cap_seconds'] <= 600 and 0 <= watch['sampled_peak_rss_mib'] < 512 and
            0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'], 'original child ownership exit0 and original wall/RSS bounds')
    watch_results.append(dict(actual_watchdog_pin=watchpin, returncode=0, limit_failure=None,
                              sampled_peak_rss_mib=watch['sampled_peak_rss_mib'], elapsed_seconds=watch['elapsed_seconds']))
require(len(watch_results) == len(report['actual_watchdog_checks']) == 3, 'all three true watches')
results = report['actual_control_results']
require(results['all_three_stages_PASS'] is True and results['all_constant64_and_overv370x8_current_words_match'] is True,
        'exact original current comparison completed')
native_pin, native_bytes = load(results['actual_native_log_pin']['path'])
require(native_pin == results['actual_native_log_pin'], 'actual native log fullPF')
native_rows = [json.loads(line) for line in native_bytes.decode().splitlines() if line.startswith('{') and line.endswith('}')]
oracle, poracle = read(results['actual_integer_oracle_output_pin']['path'])
require(poracle == results['actual_integer_oracle_output_pin'] and len(native_rows) == len(oracle['rows']) == 372,
        'current native/oracle row counts')
require(native_rows[-1] == dict(control_scope='ORIGINAL_OVERV_FALLBACK_ONLY', physics_qualified=False,
                              historical_machine_bit_replay=False), 'precise native footer no historical claim')
require(native_rows[:371] == oracle['rows'][:371] and set(native_rows[0]) ==
        {'EVJ64_hex', 'NMASS64_hex', 'SQFMAS64_hex'} and all(re.fullmatch('[0-9A-F]{16}', v)
        for v in native_rows[0].values()), 'all three exact current constant binary64 words')
native_words = []
for group, row in enumerate(native_rows[1:371], 1):
    require(set(row) == {'group', 'OVERV32_hex'} and type(row['group']) is int and row['group'] == group and
            len(row['OVERV32_hex']) == 8 and all(re.fullmatch('[0-9A-F]{8}', word) for word in row['OVERV32_hex']),
            'all370 groups and eight original current binary32 words')
    native_words += row['OVERV32_hex']
bounded = report['actual_bounded_input_evidence']
rows = bounded['actual_original_record_metadata']
require(len(rows) == 371 and bounded['actual_payload_bytes_read'] == 13324 and
        bounded['complete_SQLite_or_pool_body_EOF_repeated'] is False and bounded['original_XSM_opened'] is False,
        'bounded original current payload only, no native tree or old full bodies')
energy_pin, energy_bytes = load(bounded['energy_path'])
saved_pin, saved_bytes = load(bounded['expected_path'])
require(len(energy_bytes) == 1484 and len(saved_bytes) == 11840 and rows[0]['path'] == ['ENERGY'] and
        rows[0]['kind'] == 2 and rows[0]['declared_count'] == rows[0]['original_word_count'] == 371 and
        hashlib.sha256(energy_bytes).hexdigest() == rows[0]['native_payload_sha256'], 'new exact ENERGY copy from declared original hash')
for group, row in enumerate(rows[1:], 1):
    wordbytes = saved_bytes[(group - 1) * 32:group * 32]
    require(row['path'] == ['MACROLIB', 'GROUP', group, 'OVERV'] and row['kind'] == 2 and
            row['declared_count'] == row['original_word_count'] == 8 and
            hashlib.sha256(wordbytes).hexdigest() == row['native_payload_sha256'], 'complete tiny original saved word hash')
saved_words = [saved_bytes[i:i + 4][::-1].hex().upper() for i in range(0, len(saved_bytes), 4)]
require(native_words == saved_words and len(native_words) == 2960 and oracle['actual_energy_pin'] == energy_pin,
        'all2960 actual native words equal independent model and original saved current words')
falsekeys = ('physics_qualified', 'historical_machine_bit_replay', 'historical_native_RAM_bits_verified',
             'original_XSM_memory_bits_verified', 'complete_reaction_authority_qualified', 'AAA_qualified',
             'ABA_admitted', 'goal_complete')
require(all(report[k] is False and results[k] is False and oracle[k] is False for k in falsekeys) and
        results['original_whole_LIBDEN_procedure_executed'] is False and
        report['original_SOURCE_CONTEXT_NOT_SAVED_issue_not_deleted'] is True,
        'current formula only no historical LIBDEN process or physics qualification')
require(report['original_guard_MRO_unchanged'] is True and
        report['original_caps'] == sf['original_caps'] == hf['original_caps'] == plan['original_caps'],
        'original owning MRO and all caps unchanged')
resources = report['resources_after_including_summary_bytes']
require(0 < report['wall_seconds'] < 1800 and resources['host_SELF_peak_bytes'] < 512 * 2 ** 20 and
        resources['complete_joint']['artifact_bytes'] + resources['explicit_external_metadata_bytes'] < 2 * 2 ** 30 and
        resources['original_history']['artifact_bytes'] + 20971764748 + 64 * 2 ** 20 < 96 * 2 ** 30 and
        resources['complete_joint']['disk_free_bytes'] - 20971764748 - 2 * 2 ** 30 >= 8 * 2 ** 30,
        'actual summary-inclusive original wall/SELF/joint/history/cold/free resource guards')
require(len(plan['cumulative_joint_roots']) == 20 and len(plan['explicit_cumulative_metadata_file_pins']) == 2,
        'complete twenty roots and two explicit metadata resources')
budget_path = REC / 'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014/literal11_release_common.py'
spec = importlib.util.spec_from_file_location('original_current_factory_metadata_after_OVERV_only', budget_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
budget = module.budget()
for p in table.values():
    current(p)
for p in outputs + [psf, phf, pcli, proot, praw, pplan]:
    current(p)
DEST.mkdir()
result = dict(schema='INDEPENDENT_OVERV_ORIGINAL_MIXED_PRECISION_INTEGER_CONTROL_ACTUAL_POSTVERIFICATION_V1',
              status='PASS_ACTUAL_OVERV_ORIGINAL_MIXED_PRECISION_CURRENT_CONTROL_FACTS_POSTVERIFIED_NO_HISTORICAL_OR_PHYSICS_QUALIFICATION',
              failure=None, verification_failure=None, business_executed=False, compiler_executed=False,
              numerical_executed=False, files_deleted=False,
              actual_report_pin=preport, actual_Host_freeze_pin=phf, actual_CLI_pin=pcli,
              actual_Source_freeze_pin=psf, actual_Root_true_tool_return_pin=praw, actual_Root_argv_pin=proot,
              actual_Root_integer_exit_code=0, actual_original_report_status=report['status'],
              actual_fixed_current_count=43, actual_HF_dependency_count=36, actual_new_output_file_count=14,
              actual_new_output_full_EOF_pins=outputs, actual_watchdog_results=watch_results,
              fixed_and_HF_current_seven_fields_verified_twice=True,
              actual_control_native_object_pin=load(OUT / 'build/OVERV_control.o')[0],
              actual_control_native_executable_pin=load(OUT / 'runtime/OVERV_control_unqualified')[0],
              actual_native_control_log_pin=native_pin, actual_integer_oracle_output_pin=poracle,
              actual_owned_ENERGY_copy_pin=energy_pin, actual_owned_saved_OVERV_copy_pin=saved_pin,
              actual_current_constant64_words=native_rows[0], actual_current_overv_groups=370,
              actual_current_overv_mixtures=8, actual_current_overv_words_compared=2960,
              all_current_native_vs_independent_integer_model_vs_saved_words_equal=True,
              actual_original_guarded_payload_bytes=13324, actual_new_owned_payload_bytes_rechecked=13324,
              original_large_SQLite_or_pool_body_EOF_repeated_by_reviewer=False,
              original_XSM_opened_by_reviewer=False, original_whole_LIBDEN_procedure_executed=False,
              original_SOURCE_CONTEXT_NOT_SAVED_issue_removed=False,
              actual_original_guard_resources_after_including_summary=resources,
              actual_current_original_factory_metadata={k: budget[k] for k in
                ('artifact_bytes', 'regular_files', 'disk_free_bytes',
                 'remaining_after_original_initial_reserves_bytes', 'original_initial_reserve_admitted')},
              cumulative_joint_roots=plan['cumulative_joint_roots'],
              explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],
              original_caps=report['original_caps'], reviewer_source_pin=load(__file__)[0],
              **{k: False for k in falsekeys})
review = write(DEST / 'REVIEW.json', result)
print(json.dumps(dict(status=result['status'], review_pin=review), allow_nan=False), flush=True)
