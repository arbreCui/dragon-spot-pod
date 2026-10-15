"""Prepare a new Source namespace only; never import or execute candidate code."""
import ast, copy, hashlib, json, os, resource, stat, time
from pathlib import Path

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD = REC / 'aaa_three_plane_streaming_pipeline_source_v10'
NEW = Path(__file__).resolve().parent.parent
OLD_CLI = REC / 'ROOT_EXACT_ACTUAL_PIPELINE_V10_ARGV_20261013.json'
NEW_CLI = REC / 'ROOT_EXACT_ACTUAL_PIPELINE_V11_ARGV_20261013.json'
CAUSE = REC / 'ACTUAL_PIPELINE_V10_PARENT_SELF_MEMORY_REFUSAL_CAUSE_20261013.json'
RETURNS = REC / 'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json'
MEASURE = REC / 'independent_v10_parent_memory_lifetime_review_20261013/REVIEW.json'
READER = REC / 'independent_v10_bounded_reader_memory_review_20261013/REVIEW.json'
READER_RETURNS = READER.parent / 'TRUE_READONLY_TOOL_RETURNS.json'
COMPILER = Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
START = time.monotonic()
checks = []
hashed = {}

def need(ok, name):
    if not ok:
        raise RuntimeError(name)
    checks.append(name)

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def pin(p):
    p = Path(p)
    before = identity(p)
    need(stat.S_ISREG(before[2]) and not any(v.is_symlink() for v in (p, *p.parents)),
         'regular literal no-alias Source/provenance:' + str(p))
    need(before[3] == 1 or (p == COMPILER and before[3] == 2),
         'single link except exact existing immutable compiler role:' + str(p))
    with p.open('rb') as f:
        s = os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before,
             'opened exact all7ID:' + str(p))
        sha = hashlib.file_digest(f, 'sha256').hexdigest()
        s = os.fstat(f.fileno())
        need([s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns] == before == identity(p),
             'full EOF stable all7ID:' + str(p))
    result = dict(path=str(p), sha256=sha, size_bytes=before[4], identity=before)
    need(str(p) not in hashed or hashed[str(p)] == result, 'no changed immutable PF:' + str(p))
    hashed[str(p)] = result
    return result

def verify(p):
    need(pin(p['path']) == p, 'actual exact SHA/size/all7ID:' + p['path'])

def save(p, raw):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    need(not p.exists() and not p.is_symlink(), 'write new Source exactly once:' + str(p))
    with p.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

def write(p, value):
    save(p, (json.dumps(value, indent=2, allow_nan=False) + '\n').encode())

oldhf = json.loads((OLD / 'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json').read_text())
oldcli = json.loads(OLD_CLI.read_text())
need(len(oldhf['dependencies']) == 278, 'derive all original current v10 278 dependencies')
for p in oldhf['dependencies'] + [oldhf['host_source']] + list(oldcli['mandatory_external_bindings'].values()):
    verify(p)
original = (OLD / 'run_actual_three_plane_pipeline.py').read_text()
closed_block = """    c.verify_rows(fixed)
    # Admission and full EOF checks are complete. Keep their immutable full pins,
    # the original ordered link command and the plan; close only unused JSONs.
    exe=dict(next(x for x in build['output_pins']if Path(x['path']).name=='Dragon'))
    compiler=build['records'][0]['command'][0]
    includes=tuple(x for x in build['records'][0]['command']if x.startswith('-I'))
    archives=tuple(x for x in build['records'][-1]['command']if x.endswith('.a'))
    bounded_sha256=binding['original_bounded']['sha256']
    del build,current69,original69,seventeen,producer_reports,row,producer_fixed,sf,binding,native_sf
    del native_sf_rows,actual_new_sources,old9,original69_link,current69_link,current70_link,stripped70,module_positions
    gc.collect()
    resources=PhaseResources(base_resources)
"""
changes = [
    ('fresh_output_namespace', "-20261012-v10'", "-20261012-v11'"),
    ('exact_host_freeze_schema', 'COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V10',
     'COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11'),
    ('import_standard_cyclic_gc', 'import argparse\n', 'import argparse\nimport gc\n'),
    ('close_metadata_only_after_complete_fixed_EOF',
     '    c.verify_rows(fixed)\n    resources=PhaseResources(base_resources)\n', closed_block),
    ('use_previously_cached_exact_executable_pin',
     "    exe=next(x for x in build['output_pins']if Path(x['path']).name=='Dragon')\n    shutil.copy2(exe['path'],OUT/'runtime/Dragon')",
     "    shutil.copy2(exe['path'],OUT/'runtime/Dragon')"),
    ('use_previously_cached_original_bounded_SHA',
     "owned[1]['sha256']!=binding['original_bounded']['sha256']", "owned[1]['sha256']!=bounded_sha256"),
    ('direct_compile_uses_exact_cached_compiler_and_includes',
     "        compiler=build['records'][0]['command'][0]\n        includes=[x for x in build['records'][0]['command']if x.startswith('-I')]\n        probe_obj=",
     '        probe_obj='),
    ('mutator_compile_uses_exact_cached_compiler_and_includes',
     "        cmd=build['records'][0]['command'];compiler=cmd[0]\n        includes=[x for x in cmd if x.startswith('-I')]\n        obj=",
     '        obj='),
    ('mutator_link_uses_exact_cached_archive_order',
     "        archives=[x for x in build['records'][-1]['command']if x.endswith('.a')]\n        for i,command in enumerate([compile_cmd,",
     '        for i,command in enumerate([compile_cmd,'),
]
candidate = original
for label, before, after in changes:
    need(candidate.count(before) == 1, 'one exact old Source block:' + label)
    candidate = candidate.replace(before, after, 1)
restored = candidate
for label, before, after in reversed(changes):
    need(restored.count(after) == 1, 'one exact new Source block:' + label)
    restored = restored.replace(after, before, 1)
need(restored.encode() == (OLD / 'run_actual_three_plane_pipeline.py').read_bytes(),
     'complete byte inverse recovers entire v10 source')
oldtree = ast.parse(original)
tree = ast.parse(candidate)
main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
oldmain = next(n for n in oldtree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
all_deleted = ['build','current69','original69','seventeen','producer_reports','row','producer_fixed','sf','binding','native_sf',
               'native_sf_rows','actual_new_sources','old9','original69_link','current69_link','current70_link','stripped70','module_positions']
del_nodes = [n for n in main.body if isinstance(n, ast.Delete)]
need(len(del_nodes) == 2, 'exactly two new metadata lifetime deletion statements')
deleted = [n.id for d in del_nodes for n in d.targets]
need(deleted == all_deleted, 'exact explicit complete deletion list')
end_del = del_nodes[-1].lineno
for name in all_deleted:
    if name != 'row':
        need(not any(isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) and n.lineno > end_del
                     for n in ast.walk(main)), 'no future deleted metadata load:' + name)
def main_scope_nodes(node):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
        return
    yield node
    for child in ast.iter_child_nodes(node):
        yield from main_scope_nodes(child)
row_future = sorted((n.lineno, isinstance(n.ctx, ast.Store))
                    for stmt in main.body for n in main_scope_nodes(stmt)
                    if isinstance(n, ast.Name) and n.id == 'row' and n.lineno > end_del)
need(row_future and row_future[0][1], 'main loop row is reassigned before any subsequent same-scope load')
need(all(ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)
         for a, b in zip([n for n in oldtree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != 'main'],
                         [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != 'main'])),
     'all other host functions/classes and guard code AST unchanged')
oldnumbers = [n.value for n in ast.walk(oldtree) if isinstance(n, ast.Constant) and type(n.value) in (int,float)]
numbers = [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and type(n.value) in (int,float)]
# The cached extraction repeats the existing 0/0 subscripts at an earlier point;
# the inverse proves no original numerical statement or cap changed.
need(not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ('setrlimit','setstate')
             for n in ast.walk(tree)), 'no resetting resource peaks or limits')
gc_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and isinstance(n.func.value, ast.Name) and n.func.value.id == 'gc']
need(len(gc_calls) == 1 and gc_calls[0].func.attr == 'collect' and not gc_calls[0].args,
     'single explicit gc.collect after admission, no per-stage GC')
need(candidate[candidate.index('    def stable():'):candidate.index('    def retain(')] ==
     original[original.index('    def stable():'):original.index('    def retain(')],
     'complete stable original SELF/fullPF/resources/whole1800 guard bytes retained')
need(candidate[candidate.index('    # Complete unmodified original execution records'): ] ==
     original[original.index('    # Complete unmodified original execution records'): ],
     'complete raw records/snapshot/compact/final publication source bytes unchanged')

save(NEW / 'run_actual_three_plane_pipeline.py', candidate.encode())
local_names = []
for p in oldhf['dependencies']:
    path = Path(p['path'])
    if path.is_relative_to(OLD):
        rel = path.relative_to(OLD)
        if rel not in (Path('DIRECT_ALIAS_ENTRY_BINDING.json'), Path('DECLARED_EXECUTION_INTERFACE.json')):
            save(NEW / rel, path.read_bytes())
            need((NEW / rel).read_bytes() == path.read_bytes(), 'whole predecessor helper/proof bytes identical:' + str(rel))
        local_names.append(str(rel))
alias = json.loads((OLD / 'DIRECT_ALIAS_ENTRY_BINDING.json').read_text())
alias['new_probe_source'] = str(NEW / 'direct_alias_entry_controls.f90')
write(NEW / 'DIRECT_ALIAS_ENTRY_BINDING.json', alias)
interface = json.loads((OLD / 'DECLARED_EXECUTION_INTERFACE.json').read_text())
interface.update(schema='DECLARED_ACTUAL_AAA3_STREAMING_ONE_SERIAL_50_STAGE_INTERFACE_V11',
                 host_source=str(NEW / 'run_actual_three_plane_pipeline.py'),
                 output_root='/Users/wen/spot/validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v11',
                 closed_admission_metadata_lifetime_only=True,
                 original_raw_execution_records_and_resource_snapshots_unchanged=True,
                 readonly_memory_fixture_is_not_actual_50_stage_qualification=True)
write(NEW / 'DECLARED_EXECUTION_INTERFACE.json', interface)

cause = json.loads(CAUSE.read_text())
need(cause['actual_parent_peak_bytes'] == 541753344 and cause['original_parent_cap_bytes'] == 536870912 and
     cause['parent_cap_refusal_preserved'] is True and cause['engineering_three_plane_closed0'] is False,
     'real failed v10 SELF cause retained, no success or relaxed cap')
buildpin = oldcli['mandatory_external_bindings']['build70']
build = json.loads(Path(buildpin['path']).read_text())
compiler = build['records'][0]['command'][0]
includes = tuple(x for x in build['records'][0]['command'] if x.startswith('-I'))
archives = tuple(x for x in build['records'][-1]['command'] if x.endswith('.a'))
exe = dict(next(x for x in build['output_pins'] if Path(x['path']).name == 'Dragon'))
need(compiler == str(COMPILER), 'actual exact immutable compiler role used by unchanged commands')
need(list(includes) == [x for x in build['records'][0]['command'] if x.startswith('-I')],
     'tuple include expansion equals original ordered compile arguments')
need(list(archives) == [x for x in build['records'][-1]['command'] if x.endswith('.a')],
     'tuple archive expansion equals original ordered link arguments')
need(exe == next(x for x in build['output_pins'] if Path(x['path']).name == 'Dragon'),
     'copied exact executable PF equals original selected actual70 output')
commandproof = dict(actual_closed_build70_pin=buildpin, exact_compiler=compiler,
                    exact_ordered_includes=list(includes), exact_ordered_archives=list(archives), exact_runtime_executable_pin=exe,
                    original_full_compile_command=build['records'][0]['command'],
                    original_full_ordered70_link_command=build['records'][-1]['command'],
                    original_command_construction_bodies_unchanged=True, tuple_unpacked_argv_values_identical=True)
write(NEW / 'COMPLETE_V10_TO_V11_CLOSED_METADATA_LIFETIME_BYTE_INVERSE.json',
      dict(schema='COMPLETE_V10_TO_V11_CLOSED_METADATA_LIFETIME_SOURCE_BYTE_INVERSE_V1',
           old_host_source_pin=oldhf['host_source'], new_host_source_pin=pin(NEW / 'run_actual_three_plane_pipeline.py'),
           exact_ordered_changes=[dict(label=n, old_block=a, new_block=b, count=1) for n,a,b in changes],
           complete_inverse_equal=True, metadata_deleted_only_after_all_original_admission_and_fixed_EOF_checks=True,
           exact_deleted_names=all_deleted, actual_cached_command_authority=commandproof,
           all_other_host_functions_classes_guards_unchanged=True,
           original_unmodified_raw_records_resource_snapshots_and_final_publication_bytes_unchanged=True,
           all_three_helper_complete_bytes_identical=True,
           all50_17positive_33strictnegative_math_caps_oracles_BOOT_literals_and_native_binary_unchanged=True,
           one_gc_collect_only_before_first_stage=True, ru_maxrss_never_reset=True,
           candidate_imported_or_executed=False, compiler_CLE_or_physics_executed=False,
           Source_only=True, actual_50_stage_runtime_pass_claimed=False))
inversepin = pin(NEW / 'COMPLETE_V10_TO_V11_CLOSED_METADATA_LIFETIME_BYTE_INVERSE.json')
write(NEW / 'FINITE_CLOSED_METADATA_NAME_LIFETIME_AND_COMMAND_EQUIVALENCE_SOURCE_REVIEW.json',
      dict(schema='FINITE_V11_CLOSED_METADATA_NAME_LIFETIME_AND_COMMAND_EQUIVALENCE_SOURCE_REVIEW_ONLY',
           status='SOURCE_ONLY_COMPLETE_BYTE_INVERSE_AND_FUTURE_NAME_LIVENESS_PASSED',
           deletion_line_numbers=[d.lineno for d in del_nodes], exact_deleted_names=all_deleted,
           all_deleted_report_names_have_no_future_load=True,
           final_producer_row_deleted_and_same_scope_reassigned_before_next_load=True,
           admission_followed_by_original_fixed_full_EOF_before_deletion=True,
           original_link_command_direct_ordered_inputs_plan_fixed_hf_retained=True,
           actual_cached_command_authority=commandproof, gc_collect_count=1, no_per_stage_gc=True,
           whole_stable_guard_bytes_unchanged=True, whole_raw_record_and_final_publication_bytes_unchanged=True,
           original_current_Common_original_OwnRSSSerialExecutor_and_SerialExecutor_not_modified=True,
           original_ALL_50_stage_and_17positive_33strictnegative_guards_unchanged=True,
           original_6_DELETE_CLE_prefix_and_v10_viewops_and_positive_BOOT_whole_bytes_unchanged=True,
           original_SELF_and_child_512MiB_whole1800_stage600_and_storage_caps_unchanged=True,
           actual_v10_failure_cause_pin=pin(CAUSE), readonly_metadata_measurement_pin=pin(MEASURE),
           readonly_reader_measurement_pin=pin(READER),
           readonly_measurements_are_not_actual_full_pipeline_runtime_proof=True,
           actual_50_stages_not_executed=True, remaining_actual_full_guarded_closure_required=True,
           AAA_qualified=False, ABA_admitted=False, goal_complete=False))
reviewpin = pin(NEW / 'FINITE_CLOSED_METADATA_NAME_LIFETIME_AND_COMMAND_EQUIVALENCE_SOURCE_REVIEW.json')

deps = []
for p in oldhf['dependencies']:
    path = Path(p['path'])
    target = NEW / path.relative_to(OLD) if path.is_relative_to(OLD) else path
    newpin = pin(target)
    deps.append(newpin)
    need(newpin['sha256'] == p['sha256'] or target.name in ('DIRECT_ALIAS_ENTRY_BINDING.json','DECLARED_EXECUTION_INTERFACE.json'),
         'derive every old278 PF without omission; only two required namespace metadata changes:' + str(target))
derived_count = len(deps)
provenance = [pin(OLD / 'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'), pin(OLD_CLI), oldhf['host_source'],
              pin(CAUSE), pin(RETURNS), pin(MEASURE), pin(READER), pin(READER_RETURNS)]
for key, value in cause.items():
    if key.endswith('_pin'):
        verify(value)
        provenance.append(value)
measurement = json.loads(MEASURE.read_text())
for value in measurement['Source_pins'] + [measurement['stage_ledger_pin'], measurement['reader_evidence_pin']]:
    verify(value)
    provenance.append(value)
raw_v10 = Path(cause['actual_summary_pin']['path']).parent / 'Root_actual_complete_execution_record_before_final_publication.json'
provenance.append(pin(raw_v10))
deps += provenance + [inversepin, reviewpin, pin(__file__)] + [p for p in oldhf['dependencies'] if Path(p['path']).is_relative_to(OLD)]
table = {}
for p in deps:
    need(p['path'] not in table or table[p['path']] == p, 'no complete current PF dependency ambiguity')
    table[p['path']] = p
need(not any(Path(p).name in ('projected_boot.xsm','negative_project.xsm') for p in table),
     'no dependency on old private PROJECT or negative clones or cleanup candidates')
hf = copy.deepcopy(oldhf)
hf.update(schema='COMPLETE_ACTUAL_AAA3_STREAMING_PIPELINE_HOST_SOURCE_FREEZE_V11',
          host_source=pin(NEW / 'run_actual_three_plane_pipeline.py'), dependencies=list(table.values()),
          predecessor_host_freeze=pin(OLD / 'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'),
          Source_revision_scope='V10 to V11 only: new namespace/schema; import standard gc; after all original complete admission and fixed full EOF checks cache exact actual70 compiler/includes/archives/executable and original bounded SHA, delete only unused admitted metadata JSONs including final producer row, perform one gc.collect; later command constructors consume the exact cached values. Original guards/classes/MRO/Common/helpers/math/native complete70/50 stages/17 positive/33 strict refusals/BOOT/oracles/caps/unmodified raw resource records and snapshots remain unchanged.',
          helper_byte_equality_predecessor='pipeline_source_v10',
          complete_V10_to_V11_byte_inverse_pin=inversepin,
          finite_closed_metadata_lifetime_and_command_equivalence_source_review_pin=reviewpin,
          actual_closed_v10_original_SELF_failure_cause_pin=pin(CAUSE),
          actual_closed_v10_true_tool_returns_pin=pin(RETURNS),
          readonly_parent_metadata_memory_measurement_pin=pin(MEASURE),
          readonly_production_scope_bounded_reader_memory_measurement_pin=pin(READER),
          complete_original_v10_dependency_rows_derived=derived_count,
          original_raw_records_and_all_resource_snapshot_values_unchanged=True,
          readonly_measurement_not_full_50_stage_runtime_proof=True,
          candidate_imported_by_this_prepare=False, compiler_executed_by_this_prepare=False,
          actual_pipeline_executed_by_this_prepare=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False)
write(NEW / 'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json', hf)
hfp = pin(NEW / 'COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json')
cli = copy.deepcopy(oldcli)
cli.update(schema='ROOT_REVIEWABLE_EXACT_ACTUAL_PIPELINE_V11_CLOSED_METADATA_LIFETIME_COMPLETE70_ARGV_V1',
           Source_revision_scope=hf['Source_revision_scope'], actual_v10_failure_cause_pin=pin(CAUSE),
           actual_v10_true_tool_returns_pin=pin(RETURNS), complete_v10_to_v11_byte_inverse_pin=inversepin,
           readonly_measurement_not_actual50_runtime_pass=True)
argv = cli['argv']
index = argv.index(str(OLD / 'run_actual_three_plane_pipeline.py'))
argv[index] = str(NEW / 'run_actual_three_plane_pipeline.py')
for suffix, value in (('summary',hfp['path']),('sha256',hfp['sha256']),('seven-id',json.dumps(hfp['identity'],separators=(',',':')))):
    argv[argv.index('--host-freeze-' + suffix) + 1] = value
cli['mandatory_external_bindings']['host-freeze'] = hfp
write(NEW_CLI, cli)
clip = pin(NEW_CLI)
for p in hf['dependencies'] + [hf['host_source'], hfp] + list(cli['mandatory_external_bindings'].values()):
    verify(p)
need(not Path(interface['output_root']).exists() and not Path(interface['output_root']).is_symlink(),
     'fresh actual v11 output namespace remains absent, no business started')
print(json.dumps(dict(status='V11_CLOSED_METADATA_LIFETIME_ONLY_SOURCE_FROZEN_NOT_EXECUTED',
                      source_namespace=str(NEW), host_Source_freeze_pin=hfp, actual_reviewable_CLI_pin=clip,
                      inverse_pin=inversepin, finite_name_lifetime_command_review_pin=reviewpin,
                      original_dependency_count=derived_count, current_frozen_dependency_count=len(hf['dependencies']),
                      successful_Source_checks=len(checks), unique_full_EOF_files=len(hashed),
                      unique_full_EOF_bytes=sum(p['size_bytes'] for p in hashed.values()),
                      candidate_or_CLE_or_compiler_or_physics_executed=False,
                      original_guard_classes_MRO_raw_records_snapshots_and_all_caps_unchanged=True,
                      readonly_fixture_not_actual_50_stage_proof=True,
                      SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      elapsed_seconds=time.monotonic()-START), allow_nan=False))
