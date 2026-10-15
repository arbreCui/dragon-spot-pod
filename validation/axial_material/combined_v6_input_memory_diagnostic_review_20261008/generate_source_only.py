"""TMP-only source preparation. Never imports or executes any project module."""
from pathlib import Path
import ast
import difflib
import hashlib
import json

P = Path('/private/tmp/axmat-trim-v5-input-allocation-diagnostic-source-draft-20261008')
T = Path('/private/tmp/axmat-trim-v6-input-allocation-diagnostic-source-draft-20261008')
R = Path('/Users/wen/spot')
ART = R / 'validation/artifacts'
F5 = R / 'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v5.py'
F6 = R / 'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v6.py'
G5 = R / 'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_pooled_phase_paths_20261008.py'
G6 = R / 'validation/axial_material/combined_runtime_reviewed_metadata_historical_input_graph_same_literal_phase_identity_20261008.py'
BASE = ART / 'axial-material-trim-combined-v6-python-input-memory-diagnostic-20261008'
S6 = ART / 'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008'
O6 = ART / 'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008'
E6 = ART / 'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008'

def sha(payload):
    return hashlib.sha256(payload).hexdigest()

def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), sha256=sha(data))

def write(path, value):
    with path.open('x') as stream:
        json.dump(value, stream, allow_nan=False, sort_keys=True, indent=2)
        stream.write('\n')

def inverse(parent, candidate, name):
    regions = []
    for tag, a, b, c, d in difflib.SequenceMatcher(None, parent, candidate, autojunk=False).get_opcodes():
        if tag != 'equal':
            regions.append(dict(parent_start=a, parent_end=b, candidate_start=c, candidate_end=d,
                                parent_text=parent[a:b], candidate_text=candidate[c:d]))
    restored = candidate
    for region in reversed(regions):
        assert restored[region['candidate_start']:region['candidate_end']] == region['candidate_text']
        restored = restored[:region['candidate_start']] + region['parent_text'] + restored[region['candidate_end']:]
    assert restored == parent
    proof = dict(schema='AXMAT_V6_DIAGNOSTIC_DIRECT_PARENT_COMPLETE_SOURCE_INVERSE_V1',
                 parent_sha256=sha(parent.encode()), candidate_sha256=sha(candidate.encode()),
                 full_byte_inverse_exact=True, regions=regions)
    write(T / (name + '.source_inverse.json'), proof)
    with (T / (name + '.full.diff')).open('x') as stream:
        stream.writelines(difflib.unified_diff(parent.splitlines(True), candidate.splitlines(True),
                                             fromfile='frozen_V5/' + name, tofile='stopped_V6/' + name))
    return proof

assert not BASE.exists()
expected = {
    P/'host.py':'b2b3d746573be1c141100835d19cbf3b54a1ff86f43644f949e49839f372f481',
    P/'child.py':'9f01d08ac89b31c609c7d2607b4549b09f643fe7dfa7fb8fc62d54e6b981f04f',
    P/'config_v2.json':'36a4c3bfb1fe3e6ed7a1f13d9092289a6aae8e43dc09a6bb19f83726db09149b',
    P/'ROOT_READY_config.json':'c95542dfa95b54e888e1b4659f119929f76b5dfcd6162d2b2f3591251fa383f6',
    F6:'6bcef269814a120f0cf8a5e9d068a6de0b509017690b8ae646b50b2ef27d8921',
    G6:'07b22c9f2f4fba626fbe7f4faec5edd9cbbc15f0e0f4f4edf5858aac489be612',
    O6/'declaration.json':'da73dec778985527b751441c396750504316ccdb241b80ba1ccac89cb41b69fd',
    E6/'declaration_terminal_return.json':'684742fbb37dee634f22a8a3d00c4f400a7aafd85d1a2b3a66700855b70cbb5f',
    E6/'terminal_return.json':'49b675cc09124d1d9e1513719ab8d636ce033a8bc8d42d45cffaed6284d0ab32',
}
for path, digest in expected.items():
    assert not path.is_symlink() and path.resolve(strict=True) == path
    assert pin(path)['sha256'] == digest
old_ready = json.loads((P/'ROOT_READY_config.json').read_text())
old_stopped = json.loads((P/'config_v2.json').read_text())
assert old_ready.pop('status') == 'READY_ROOT_REVIEWED_INPUT_DIAGNOSTIC_ONLY'
old_without_status = dict(old_stopped)
assert old_without_status.pop('status') == 'UNREADY_STOPPED_SOURCE_ONLY_ROOT_REVIEW_REQUIRED'
assert old_ready == old_without_status
failure = json.loads((E6/'terminal_return.json').read_text())
assert failure['returncode'] == 1
assert failure['actual_tool_terminal_return_observed'] is True
assert failure['successful_combined_link_completion_observed'] is False

proofs = {}
for name, count in [('host.py',4),('child.py',2)]:
    parent = (P/name).read_text()
    assert parent.count('TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC') == count
    candidate = parent.replace('TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC','TRIM_V6_INPUT_ALLOCATION_DIAGNOSTIC')
    ast.parse(candidate)
    with (T/name).open('x') as stream:
        stream.write(candidate)
    proofs[name] = inverse(parent,candidate,name)
    assert len(proofs[name]['regions']) == count
    assert ast.dump(ast.parse(candidate.replace('TRIM_V6_INPUT_ALLOCATION_DIAGNOSTIC','TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC'))) == ast.dump(ast.parse(parent))

config = json.loads((P/'config_v2.json').read_text())
config['V5_function_interval_evidence_transferred_to_V6'] = config.pop('V4_function_interval_evidence_transferred_to_V5')
config['actual_PREP'] = pin(E6/'declaration_terminal_return.json')
config['base'] = str(BASE)
config['child_source'] = pin(T/'child.py')
config['declaration'] = pin(O6/'declaration.json')
config['factory'] = pin(F6)
config['failed_RUN_provenance_INPUT_only'] = pin(E6/'terminal_return.json')
config['family'] = 'TRIM_V6_INPUT_ALLOCATION_DIAGNOSTIC'
config['host_source'] = pin(T/'host.py')
config['result_path'] = str(BASE/'diagnostic/result.json')
config['schema'] = 'AXMAT_TRIM_V6_INPUT_ALLOCATION_DIAGNOSTIC_CONFIG_V1'
for marker in config['profile_markers']:
    if marker['path'] == str(F5): marker['path'] = str(F6)
    elif marker['path'] == str(G5): marker['path'] = str(G6)
config['profile_source_files']['factory'] = pin(F6)
config['profile_source_files']['graph'] = pin(G6)
write(T/'config.json',config)
proofs['config.json'] = inverse((P/'config_v2.json').read_text(),(T/'config.json').read_text(),'config.json')

def delta(a,b,prefix=''):
    if isinstance(a,dict) and isinstance(b,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            name=prefix+'/'+key
            if key not in a: out.append(dict(field=name,parent_missing=True,candidate=b[key]))
            elif key not in b: out.append(dict(field=name,parent=a[key],candidate_missing=True))
            else: out.extend(delta(a[key],b[key],name))
        return out
    if isinstance(a,list) and isinstance(b,list):
        assert len(a)==len(b)
        return [change for i,(x,y) in enumerate(zip(a,b)) for change in delta(x,y,prefix+'/'+str(i))]
    return [] if a==b else [dict(field=prefix,parent=a,candidate=b)]

changes = delta(old_stopped,config)
assert len(changes) == 24
assert config['caps'] == old_stopped['caps']
assert config['maximum_boundary_events'] == 1024
assert config['status'] == old_stopped['status'] == 'UNREADY_STOPPED_SOURCE_ONLY_ROOT_REVIEW_REQUIRED'
assert sum(len(marker['functions']) for marker in config['profile_markers']) == 25
assert [marker['functions'] for marker in config['profile_markers']] == [marker['functions'] for marker in old_stopped['profile_markers']]
assert all(config[k] is None for k in ('build_seal','production_admission'))
assert config['failed_RUN_provenance_is_not_an_admission_dependency_or_success'] is True
assert config['failed_RUN_is_not_success_input'] is True
assert config['V5_function_interval_evidence_transferred_to_V6'] is False

path_observations=[]
def paths(value,field=''):
    if isinstance(value,dict):
        for key,item in value.items(): paths(item,field+'/'+key)
    elif isinstance(value,list):
        for i,item in enumerate(value): paths(item,field+'/'+str(i))
    elif isinstance(value,str) and value.startswith('/'):
        path=Path(value)
        assert 'scopes-v5-' not in value and 'scopes-v4-' not in value
        assert 'trim-v5-input-allocation' not in value and 'trim-v4-input-allocation' not in value
        assert 'combined-v5-python-input' not in value and 'combined-v4-python-input' not in value
        expected_absent = value in (str(BASE),str(BASE/'diagnostic/result.json'))
        if expected_absent: assert not path.exists()
        else: assert path.exists()
        path_observations.append(dict(field=field,path=value,exists=path.exists(),planned_output_only=expected_absent))
paths(config)
for name,descriptor in config['profile_source_files'].items():
    assert pin(Path(descriptor['path'])) == descriptor
for marker in config['profile_markers']:
    tree=ast.parse(Path(marker['path']).read_text())
    found={node.name for node in ast.walk(tree) if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
    assert set(marker['functions']) <= found
assert BASE.parent == ART
assert Path(config['result_path']).parent == BASE/'diagnostic'
assert not BASE.exists()

write(T/'source_only_observation.json',dict(
    schema='AXMAT_V6_INPUT_ALLOCATION_DIAGNOSTIC_SOURCE_ONLY_OBSERVATION_V1',
    frozen_parent_hashes_verified=[dict(path=str(path),sha256=digest) for path,digest in expected.items()],
    config_deep_field_changes=changes,config_changed_field_count=len(changes),
    every_config_path_observation=path_observations,
    all_named_profile_functions_source_AST_confirmed=True,selected_whole_function_count=25,
    exact_parent_profile_marker_function_lists=True,exact_original_caps=True,
    host_wrapper_identity_region_count=len(proofs['host.py']['regions']),
    child_wrapper_identity_region_count=len(proofs['child.py']['regions']),
    config_whole_byte_inverse_to_corrected_stopped_V5=True,
    V5_ready_config_differs_from_corrected_stopped_config_only_in_status=True,
    wrapper_profile_callback_byte_exact_to_V5=True,ART_BASE_not_created=True,
    project_modules_imported=False,API_or_constructor_or_native_or_numerical_execution=False,
    build_or_input_admission_or_diagnostic_execution=False,
    runtime_or_physics_or_AAA_or_ABA_credit=False))

write(T/'STOPPED_handoff.json',dict(
    schema='AXMAT_TRIM_V6_INPUT_ALLOCATION_DIAGNOSTIC_STOPPED_SOURCE_HANDOFF_V1',
    status='UNREADY_STOPPED_SOURCE_ONLY_ROOT_REVIEW_REQUIRED',
    source_files={name:pin(T/name) for name in ('host.py','child.py','config.json')},
    source_inverse_files={name:pin(T/(name+'.source_inverse.json')) for name in ('host.py','child.py','config.json')},
    source_observation=pin(T/'source_only_observation.json'),
    parent_wrapper_source_files={name:pin(P/name) for name in ('host.py','child.py','config_v2.json','ROOT_READY_config.json')},
    actual_V6_factory=pin(F6),actual_V6_graph_helper=pin(G6),
    actual_V6_declaration=pin(O6/'declaration.json'),actual_V6_PREP=pin(E6/'declaration_terminal_return.json'),
    failed_V6_RUN_context_ONLY=pin(E6/'terminal_return.json'),
    failed_V6_RUN_is_not_admission_dependency_or_success=True,
    direct_wrapper_delta='Only six TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC identity tokens become V6. The whole profile callback, genuine call, MRO, imports, budgets and archive logic remain byte exact.',
    config_delta='Only V6 identities, exact current producer/helper/DECL/PREP/failed-context pins, exclusive V6 BASE/result paths and diagnostic wrapper paths/SHAs; marker function lists and caps are exact corrected V5.',
    new_exclusive_ART_BASE_planned_only=str(BASE),ART_BASE_not_created=True,
    actual_call='declaration_admission(DECLSHA, True, prep_sha256=PREPSHA)',
    original_budget=config['caps'],maximum_boundary_events=1024,selected_whole_function_count=25,
    profile_callback_byte_exact=True,old_supervisor_parent_bounded_helper_unchanged=True,
    no_V5_function_intervals_transferred_to_V6=True,no_actual_V6_diagnostic_executed=True,
    original_python='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',
    environment={'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'},
    unset_environment=['PYTHONPATH','PYTHONOPTIMIZE'],
    future_ready_config_change='Root may create a new config differing only in status to READY_ROOT_REVIEWED_INPUT_DIAGNOSTIC_ONLY after independent review; compute its new complete SHA. No ready config was authored here.',
    future_ready_config_path_planned_only=str(T/'ROOT_READY_config.json'),
    planned_ROOT_launch_after_ready_review=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(T/'host.py'),'--config',str(T/'ROOT_READY_config.json'),'--config-sha256','ROOT_MUST_COMPUTE_FRESH_READY_CONFIG_SHA'],
    complete_archive_scope='Root must include BASE, all wrapper/config source and review copies, full actual host stdout/stderr, child merged log and observed terminal receipt in the original 2GiB scope. Host BASE alone is insufficient.',
    ROOT_actual_exit_and_postterminal_receipt_required=True,complete_merged_child_log_plus_external_host_stdout_stderr_required=True,
    diagnostic_hook_overhead_is_inside_original_limits=True,
    RUSAGE_SELF_is_high_water_not_live_RSS_or_cause=True,no_single_JSON_API_log_contract=True,
    failure_does_not_create_success_result=True,science_or_cold_or_AAA_or_ABA_credit=False,
    build_or_native_or_API_execution=False))

with (T/'REPORT.txt').open('x') as stream:
    stream.write('V6 INPUT memory interval diagnostic: STOPPED, TMP source only.\n'
                 'No project import, API call, constructor, numerical child, build or diagnostic was executed.\n'
                 'Host/child change only 4+2 identity regions; complete byte inverses reconstruct frozen V5 sources.\n'
                 'Config reconstructs corrected frozen V5 config_v2.json byte exactly via its source inverse.\n'
                 'All config path fields checked individually; exclusive V6 BASE and result path remain absent.\n'
                 'All 25 selected function names confirmed by source AST; marker lists, max 1024, and all caps unchanged.\n'
                 'Actual V6 DECL/PREP pins verified; actual failed RUN returncode 1 is context only.\n'
                 'The V5 function interval is not a V6 observation. Fresh Root execution remains required.\n'
                 'Only Root may create READY config after independent source review; no READY file was created.\n'
                 'Own child caps remain 1800 total / 600 stage seconds / 512 MiB / 2 GiB archive / 96 GiB history / 8 GiB free / 1 thread / 1 child / 0 retries.\n'
                 '705/38de/bc4 genuine supervisor chain, canonical import, real three-argument declaration admission and producer preflight remain unchanged.\n'
                 'RUSAGE_SELF is cumulative high water; it does not establish live RSS or line-level cause.\n'
                 'No build, native RSS, coupled physical accuracy, cold, AAA or ABA qualification is claimed.\n')
print(json.dumps(dict(status='STOPPED_SOURCE_ONLY',source_files={name:pin(T/name) for name in ('host.py','child.py','config.json')},handoff=pin(T/'STOPPED_handoff.json'),config_changed_field_count=len(changes),planned_BASE_absent=not BASE.exists()),indent=2))
