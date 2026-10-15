"""Unique final metadata check; no scientific input or native tree is read."""
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
PKG = REC / 'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014'
DEST = REC / 'independent_GENDF_cumulative17_final_SF_HF_recipe_ROOT32_metadata_review_20261014'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(expected):
    p = Path(expected['path'])
    require(p.is_absolute() and not any(q.is_symlink() for q in (p, *p.parents)), 'ordinary absolute current path')
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == expected['identity'] and
            s.st_size == expected['size_bytes'] and all(type(v) is int for v in expected['identity']),
            'exact current seven fields ' + str(p))


def pin(path):
    p = Path(path).absolute()
    s = p.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_size < 64 * 2 ** 20, 'bounded metadata or Source')
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        require(identity(os.fstat(f.fileno())) == identity(s), 'opened metadata7')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        require(identity(os.fstat(f.fileno())) == identity(s), 'metadata EOF7')
    expected = dict(path=str(p), sha256=digest, size_bytes=s.st_size, identity=identity(s))
    current(expected)
    return expected


def read(path):
    expected = pin(path)
    value = json.loads(Path(path).read_bytes())
    current(expected)
    return value, expected


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


def genuine(raw):
    require(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and
            raw['original_integer_exit_code'] == 0, 'genuine original closed0')
    terminal = raw['actual_terminal_return']
    require(type(terminal['exit_code']) is int and terminal['exit_code'] == 0 and
            terminal.get('session_id') is None and type(terminal['output']) is str, 'typed terminal0')
    return json.loads(terminal['output'].strip().splitlines()[-1])


sf, psf = read(PKG / 'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json')
hf, phf = read(PKG / 'COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_HOST_SOURCE_ONLY_FREEZE.json')
recipe, precipe = read(PKG / 'ROOT_REVIEWABLE_CURRENT_GENDF_V4_CLI_SOURCE_ONLY.json')
argv, pargv = read(REC / 'ROOT_EXACT_GENDF_CUMULATIVE17_ACTUAL32_ARGV_20261014.json')
publication, ppublication = read(REC / 'ROOT_ACTUAL_GENDF_CUMULATIVE17_SOURCE_ONCE_PUBLICATION_TRUE_TOOL_RETURNS_20261014.json')
metadata, pmetadata = read(REC / 'ROOT_ACTUAL_GENDF_CUMULATIVE17_METADATA18_BINDER_TRUE_TOOL_RETURNS_20261014.json')
ready, pready = read(PKG / 'SOURCE_REVIEW_READY_v2.json')
plan, pplan = read(ready['plan_pin']['path'])
require(pplan == ready['plan_pin'] and sf['current_plan_pin'] == pplan, 'actual final READY_v2 plan')
require(len(sf['complete_source_file_pins']) == 5 and len(hf['dependencies']) == 6000,
        'actual Source5 and HF6000 complete counts')
require(sf['candidate_executed'] is False and hf['candidate_executed'] is False and
        sf['GENDF_executed'] is False and hf['GENDF_executed'] is False, 'unexecuted Source package')
require(hf['selected_source_freeze_pin'] == psf and hf['host_source'] == plan['candidate_host_source_pin'] and
        recipe['selected_source_freeze_pin'] == psf and recipe['selected_host_freeze_pin'] == phf and
        recipe['host_source_pin'] == hf['host_source'], 'exact published SF/HF/recipe host binding')
table = {}
for row in sf['complete_source_file_pins'] + hf['dependencies']:
    require(row['path'] not in table or table[row['path']] == row, 'unambiguous complete fullPF')
    table[row['path']] = row
for row in table.values():
    current(row)
for row in sf['complete_source_file_pins']:
    require(pin(row['path']) == row, 'complete bounded Source SHA/EOF7')
for row in plan['publication_source_mapping']:
    require(row['candidate_pin'] in sf['complete_source_file_pins'] and
            row['candidate_pin'] in hf['dependencies'], 'three correctly published candidate Source paths')
require(sf['complete_source_file_pins'] == plan['complete_source_file_pins'], 'actual loaded SF all current source pointers')
pubout = genuine(publication)
require(pubout['source_freeze_pin'] == psf and pubout['host_freeze_pin'] == phf and
        pubout['recipe_pin'] == precipe and len(shlex.split(publication['exact_executed_command'])) == 60,
        'actual unique publication60 exact PFs')
metaout = genuine(metadata)
require(metaout == argv and len(shlex.split(metadata['exact_executed_command'])) == 18,
        'actual metadata18 produced exact Root argv record')
observed_pin = argv['actual_material_observation_report_pin']
observed, observed_current = read(observed_pin['path'])
require(observed_current == observed_pin and observed['completion_only_existing_closed_stage'] is True and
        observed['Dragon_or_compiler_or_material_child_launched_by_continuation'] is False,
        'original successful bounded closure metadata')
require(str(Path(observed['actual_prior_A_cwd']).parent) == sf['retained_actual_capture_owner_root'] and
        Path(observed['original_failed_phase_pin']['path']).parent == Path(sf['retained_actual_capture_owner_root']),
        'explicit retained actual physical capture owner, never guessed index')
expected = recipe['argv_prefix'] + ['--material-observation-report-summary', observed_pin['path'],
        '--material-observation-report-sha256', observed_pin['sha256'], '--material-observation-report-seven-id',
        json.dumps(observed_pin['identity'], separators=(',', ':'))] + recipe['final_output_option']
require(len(recipe['argv_prefix']) == 24 and len(expected) == 32 and argv['argv'] == expected and
        shlex.split(argv['shell_safe_command']) == expected and argv['host_or_parser_launched'] is False,
        'published exact recipe24 plus material6 and output2')
require(recipe['argv_prefix'][11] == hf['host_source']['path'], 'actual selected runtime Source')
art = sf['cumulative_artifact_root_paths']
sources = sf['cumulative_Source_root_paths']
roots = art[:3] + sources + art[3:]
require(len(art) == 10 and len(sources) == 7 and len(roots) == len(set(roots)) == 17 and
        not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b),
        'complete seventeen disjoint cumulative roots')
require(roots == plan['complete_cumulative_seventeen_role_roots'] and
        sf['complete_cumulative_joint_root_count'] == hf['complete_cumulative_joint_root_count'] == 17,
        'published Source/Host explicit cumulative roots')
require(art[:3] == [recipe['final_output_option'][1], recipe['final_output_option'][1] + '-evidence',
                    str(Path(observed_pin['path']).parent)] and Path(sources[0]) == PKG,
        'new own output pair and Source counted, old closure preserved')
require(not os.path.lexists(art[0]) and not os.path.lexists(art[1]), 'fresh real output pair absent')
explicit = sf['cumulative_explicit_metadata_file_pins']
require(explicit == plan['cumulative_explicit_metadata_file_pins'] == hf['cumulative_explicit_metadata_file_pins'] and
        [q['path'] for q in explicit] == [str(REC / name) for name in
        ('ROOT_EXACT_GENDF_CUMULATIVE16_ACTUAL32_ARGV_20261014.json',
         'ROOT_ACTUAL_GENDF_CUMULATIVE16_METADATA18_BINDER_TRUE_TOOL_RETURNS_20261014.json')],
        'two exact previous metadata publications are counted')
for row in explicit:
    require(pin(row['path']) == row, 'small explicit metadata current fullPF')
require(len({tuple(q['identity'][:2]) for q in explicit}) == 2 and
        not any(Path(q['path']).is_relative_to(Path(root)) for q in explicit for root in roots),
        'distinct extra metadata outside counted roots')
caps_node = next(node for node in ast.parse(Path(hf['host_source']['path']).read_bytes()).body
                 if isinstance(node, ast.Assign) and any(isinstance(x, ast.Name) and x.id == 'CAPS' for x in node.targets))
caps = {}
exec(compile(ast.Module(body=[caps_node], type_ignores=[]), '<unchanged literal GENDF caps>', 'exec'), {}, caps)
require(sf['original_caps'] == hf['original_caps'] == caps['CAPS'], 'original exact time/RSS/archive/free/cold caps')
budget_path = REC / 'storage_release_literal2_old_map005006_before_aggregate_source_v1_20261014/literal11_release_common.py'
spec = importlib.util.spec_from_file_location('existing_original_factory_metadata_only_gendf_final', budget_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
budget = module.budget()
require(budget['original_initial_reserve_admitted'] is True and
        budget['remaining_after_original_initial_reserves_bytes'] > 0, 'current original fullfresh2/cold/meta/free factory')
for row in table.values():
    current(row)
for row in (psf, phf, precipe, pargv, ppublication, pmetadata, pready, pplan, observed_pin, *explicit):
    current(row)
DEST.mkdir()
report = dict(schema='INDEPENDENT_GENDF_CUMULATIVE17_FINAL_SF_HF_RECIPE_ROOT32_METADATA_REVIEW_V1',
              status='PASS_GENDF_CUMULATIVE17_FINAL_METADATA_READY_FOR_UNIQUE_RUNTIME', failure=None,
              source_only=True, business_executed=False, compiler_executed=False, numerical_executed=False,
              files_deleted=False, physics_qualified=False, goal_complete=False,
              actual_Source_freeze_pin=psf, actual_Host_freeze_pin=phf, actual_recipe_pin=precipe,
              actual_Root_argv_pin=pargv, actual_publication_true_tool_pin=ppublication,
              actual_metadata18_true_tool_pin=pmetadata, actual_material_observation_report_pin=observed_pin,
              actual_READY_v2_pin=pready, actual_plan_pin=pplan, reviewer_source_pin=pin(__file__),
              complete_source_count=5, current_HF_dependency_count=6000,
              complete_distinct_current_pin_count=len(table), all_current_seven_fields_verified_twice=True,
              five_bounded_Source_files_verified_complete_SHA=True, exact_runtime_argv_count=32,
              exact_actual_publication_argv_count=60, exact_actual_metadata_argv_count=18,
              cumulative_joint_roots=roots, cumulative_explicit_metadata_file_pins=explicit,
              explicit_metadata_bytes=sum(q['size_bytes'] for q in explicit), original_caps=caps['CAPS'],
              actual_current_original_factory_metadata={key: budget[key] for key in
                 ('artifact_bytes', 'regular_files', 'disk_free_bytes',
                  'remaining_after_original_initial_reserves_bytes', 'original_initial_reserve_admitted')},
              no_scientific_payload_EOF_or_native_tree_read_by_reviewer=True,
              actual_GENDF_runtime_return=None, actual_GENDF_report_pin=None)
review = write(DEST / 'REVIEW.json', report)
print(json.dumps(dict(status=report['status'], review_pin=review), allow_nan=False), flush=True)
