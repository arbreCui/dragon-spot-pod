"""Same-round Source review of the new bounded control and once-only writer."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
PKG = REC / 'OVERV_original_guarded_integer_control_source_v3_20261014'
DEST = REC / 'independent_OVERV_original_guarded_integer_control_candidate_writer_Source_review_20261014'


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def current(expected):
    path = Path(expected['path'])
    require(path.is_absolute() and not any(p.is_symlink() for p in (path, *path.parents)), 'ordinary exact path')
    s = path.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == expected['identity'] and
            s.st_size == expected['size_bytes'], 'current full seven fields ' + str(path))


def pin(path):
    path = Path(path).absolute()
    s = path.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_size < 64 * 2 ** 20, 'bounded Source/metadata')
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        require(identity(os.fstat(f.fileno())) == identity(s), 'opened Source7')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        require(identity(os.fstat(f.fileno())) == identity(s), 'Source EOF7')
    result = dict(path=str(path), sha256=digest, size_bytes=s.st_size, identity=identity(s))
    current(result)
    return result


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


def definitions(source):
    return {n.name: ast.get_source_segment(source, n) for n in ast.parse(source).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


ready, pready = read(PKG / 'SOURCE_REVIEW_READY.json')
selected = [ready[k] for k in ('host_source_pin', 'control_Fortran_Source_pin', 'integer_oracle_Source_pin',
                             'plan_pin', 'inverse_pin', 'Source_author_pin', 'writer_source_pin')] + [pready]
for expected in selected:
    require(pin(expected['path']) == expected, 'all eight selected Source fullPFs')
plan, pplan = read(ready['plan_pin']['path'])
inverse, pinverse = read(ready['inverse_pin']['path'])
raw, praw = read(REC / 'ACTUAL_OVERV_GUARDED_INTEGER_CONTROL_SOURCE_PREPARATION_TRUE_TOOL_RETURN_20261014.json')
require(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and
        raw['original_integer_exit_code'] == 0, 'actual Source generation closed0')
term = raw['actual_Source_preparation_return']
require(type(term['exit_code']) is int and term['exit_code'] == 0 and term.get('session_id') is None and
        json.loads(term['output'].strip())['ready_pin'] == pready, 'genuine preparation0 exact READY')
require(ready['source_only'] is True and all(ready[k] is False for k in
        ('business_executed', 'compiler_executed', 'numerical_executed', 'files_deleted', 'physics_qualified')),
        'Source only no scientific execution')
require(all(plan[k] is None for k in ('actual_energy_input_pin', 'actual_current_control_report_pin',
        'actual_integer_oracle_output_pin', 'actual_control_object_pin', 'actual_control_executable_pin')),
        'actual controls genuinely future None')
host = Path(ready['host_source_pin']['path']).read_text()
writer = Path(ready['writer_source_pin']['path']).read_text()
oracle = Path(ready['integer_oracle_Source_pin']['path']).read_text()
ast.parse(host); ast.parse(writer); oracle_tree = ast.parse(oracle)
prototype_pin = inverse['original_guard_prototype_Source_pin']
require(pin(prototype_pin['path']) == prototype_pin, 'original borrowed guard Source')
prototype = Path(prototype_pin['path']).read_text()
olddefs, newdefs = definitions(prototype), definitions(host)
borrowed = inverse['borrowed_original_guard_methods']
require(len(borrowed) == 5 and {q['name'] for q in borrowed} ==
        {'rewrite_summary', 'unique', 'safe_repr', 'FirstFailure', 'log_rows'}, 'five precise original borrowed methods')
for item in borrowed:
    require(olddefs[item['name']] == newdefs[item['name']] == item['whole_bytes'], 'complete borrowed method bytes')
original_control = inverse['original_Fortran_Source_pin']
require(pin(original_control['path']) == original_control and
        Path(original_control['path']).read_bytes() == Path(ready['control_Fortran_Source_pin']['path']).read_bytes(),
        'whole original Fortran arithmetic/control Source')
require(inverse['integer_oracle_Source_pin'] == ready['integer_oracle_Source_pin'] == plan['integer_oracle_Source_pin'],
        'same independently prepared integer Source')
require(not any(isinstance(n, ast.Constant) and type(n.value) is float for n in ast.walk(oracle_tree)),
        'integer model contains no native Python float literals')
mathcalls = {ast.unparse(n.func) for n in ast.walk(oracle_tree) if isinstance(n, ast.Call) and
             isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'math'}
require(mathcalls == {'math.isqrt'}, 'integer sqrt only no libm model')
spec = importlib.util.spec_from_file_location('independently_reviewed_integer_boundary_only', ready['integer_oracle_Source_pin']['path'])
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
boundary = model.self_check()
require(boundary['actual_energy_read'] is False and boundary['compiler_executed'] is False and
        boundary['historical_machine_bit_replay'] is False, 'pure source boundary selfcheck only')
caps_assign = next(n for n in ast.parse(host).body if isinstance(n, ast.Assign) and
                   any(isinstance(t, ast.Name) and t.id == 'CAPS' for t in n.targets))
ns = {}
exec(compile(ast.Module(body=[caps_assign], type_ignores=[]), '<literal original caps>', 'exec'), {}, ns)
require(plan['original_caps'] == ns['CAPS'] and ns['CAPS'] == dict(whole_seconds=1800, stage_seconds=600,
        rss_mib=512, fresh_bytes=2 * 2 ** 30, history_bytes=96 * 2 ** 30, cold_reserve_bytes=20971764748,
        metadata_reserve_bytes=64 * 2 ** 20, free_floor_bytes=8 * 2 ** 30, threads=1, children_at_once=1, retries=0),
        'exact unchanged original caps')
for expected in plan['source_dependency_pins']:
    current(expected)
build, pbuild = read(plan['actual_build75_report_pin']['path'])
require(pbuild == plan['actual_build75_report_pin'] and len(build['records']) == 6 and
        all(r['status'] == 'PASS' for r in build['records']) and build['failure'] is None,
        'actual completed original75 compile/link metadata')
compile_cmd = build['records'][0]['command']
link_cmd = build['records'][-1]['command']
require(compile_cmd[0] == plan['original_compiler_pin']['path'] and
        compile_cmd[1:10] == plan['original_compile_flags'], 'actual selected compiler and all nine compile flags')
require([v for v in compile_cmd if v.startswith('-I')] == plan['original_compile_include_arguments'],
        'all actual original module/include roles')
require([v for v in link_cmd if v.endswith('.a')] == [p['path'] for p in plan['original_four_archive_pins']],
        'all four original archives exact actual link order')
extraction, pextraction = read(plan['actual_extraction_child_report_pin']['path'])
descriptor = plan['selected_final_snapshot_descriptor']
require(pextraction == plan['actual_extraction_child_report_pin'] and descriptor in extraction['states']['A'] and
        descriptor['event'] == 55 and descriptor['role'] == 'final-complete-micro' and descriptor['root_prefix'] == [],
        'exact already-extracted current final descriptor')
adapter_pin = plan['original_saved_input_adapter_Source_pin']
require(pin(adapter_pin['path']) == adapter_pin, 'complete original native saved adapter Source')
adapter = Path(adapter_pin['path']).read_text()
validate = definitions(adapter)['validate_row'] if 'validate_row' in definitions(adapter) else None
adapter_ast = ast.parse(adapter)
classnode = next(n for n in adapter_ast.body if isinstance(n, ast.ClassDef) and n.name == 'SavedNativeInput')
validnode = next(n for n in classnode.body if isinstance(n, ast.FunctionDef) and n.name == 'validate_row')
attributes = {n.attr for n in ast.walk(validnode) if isinstance(n, ast.Attribute) and
              isinstance(n.value, ast.Name) and n.value.id == 'self'}
require(attributes == {'pool_pin'}, 'bounded row validator initialized with all its original instance inputs')
require('sum(map(len,payloads))==1484+370*8*4' in host and "for g in range(1,371)" in host and
        "row['kind']==2" in host and "hashlib.sha256(raw).hexdigest()==row['native_payload_sha256']" in host,
        'exact 13324-byte complete current record hashes and shapes')
require('model=oracle.original_overv_model(energy.read_bytes())' in host and
        'rows[:371]==model[:371]' in host and 'native_words==expected_words' in host,
        'independent exact constants/370x8 comparison and all saved words, no tolerance')
require(host.count("run(out/'build'") == 2 and host.count("run(out/'control'") == 1 and
        'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)' in host,
        'three genuine original stages and unchanged owning MRO')
roots = plan['cumulative_joint_roots']
require(len(roots) == len(set(roots)) == 20 and not any(Path(a).is_relative_to(Path(b))
        for a in roots for b in roots if a != b), 'twenty complete disjoint cumulative roots')
require(roots[:3] == [plan['planned_actual_output_root'], str(PKG),
        str(REC / 'OVERV_original_guarded_integer_control_source_v2_20261014')],
        'new control and both candidate Source directories retained')
gensf, pgensf = read(REC / 'current_eleven_saved_gendf_actual_cumulative_seventeen_roots_host_source_v11_20261014/COMPLETE_CURRENT_ELEVEN_GENDF_EXTRACTION_SOURCE_ONLY_FREEZE.json')
genroots = gensf['cumulative_artifact_root_paths'][:3] + gensf['cumulative_Source_root_paths'] + gensf['cumulative_artifact_root_paths'][3:]
require(roots[3:] == genroots and plan['explicit_cumulative_metadata_file_pins'] ==
        gensf['cumulative_explicit_metadata_file_pins'], 'all seventeen prior GENDF and two metadata resources retained')
require(not os.path.lexists(plan['planned_actual_output_root']), 'actual control output absent')
require('len(argv)==24' in writer and "('peer-review','peer-tools','Source-generation-tools')" in writer and
        "'actual_review_return'" in writer and "'ready_pin'" in writer and "path.open('xb')" in writer,
        'strict one-publication30 and exact execution24 metadata interface')
for expected in selected + plan['source_dependency_pins'] + [praw, pgensf]:
    current(expected)
DEST.mkdir()
result = dict(schema='INDEPENDENT_OVERV_ORIGINAL_GUARDED_INTEGER_CONTROL_CANDIDATE_WRITER_SOURCE_REVIEW_V1',
              status='PASS_OVERV_ORIGINAL_GUARDED_INTEGER_CURRENT_CONTROL_SOURCE_ONLY_READY_FOR_PUBLICATION',
              source_only=True, failure=None, business_executed=False, compiler_executed=False,
              numerical_executed=False, files_deleted=False, physics_qualified=False,
              historical_machine_bit_replay=False, original_SOURCE_CONTEXT_NOT_SAVED_issue_removed=False,
              final_selected_Source_pins=selected, plan_pin=pplan, writer_source_pin=ready['writer_source_pin'],
              actual_Source_generation_true_tool_pin=praw, original_genDF_Source_freeze_pin=pgensf,
              reviewer_source_pin=pin(__file__), five_original_guard_methods_whole_bytes_equal=True,
              whole_original_Fortran_control_bytes_equal=True, integer_oracle_has_no_native_float_or_libm_math=True,
              pure_integer_rounding_boundary_selfcheck_only=boundary, exact_guarded_payload_bytes=13324,
              actual_selected_descriptor=descriptor, original_caps=ns['CAPS'], complete_cumulative_roots=roots,
              explicit_cumulative_metadata_file_pins=plan['explicit_cumulative_metadata_file_pins'],
              original_native_stage_count=3, once_publication_argv_count=30, runtime_argv_count=24,
              all_current_Source_and_dependency_seven_fields_verified_twice=True,
              no_actual_ENERGY_or_OVERV_payload_or_SQLite_rows_read_by_reviewer=True,
              no_compiler_or_native_control_launched_by_reviewer=True,
              actual_control_report_pin=None, actual_control_object_pin=None, actual_control_executable_pin=None)
review = write(DEST / 'REVIEW.json', result)
print(json.dumps(dict(status=result['status'], review_pin=review), allow_nan=False), flush=True)
