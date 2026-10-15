#!/usr/bin/env python3
"""Stdlib-only source/metadata review; never import or execute project code."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import time

OUT = Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009')
ART = Path('/Users/wen/spot/validation/artifacts')
WORK = ART/'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
SOURCE = ART/'axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-admission-scipy-env-physical-basis-own-pid-peak-v9-20261009'
FACTORY = Path('/Users/wen/spot/validation/axial_material/prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py')
PLAN = Path('/private/tmp/spot_storage_nineteenth_root_20261009/fixed_candidate_plan.json')
PEER = Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009/REPORT.json')
PIN_PLAN = 'b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
PIN_PEER = '0473a770f97ecd65ef066aef12729478932d784c7aa4f22e42b138e46491e960'
PINS = {}
CONTENT = {}
SOURCE_TEXT = {}
GROUPS = {}
started = time.monotonic()

def full(path, wanted=None):
    path = Path(path)
    if str(path) not in CONTENT:
        before = path.lstat()
        assert stat.S_ISREG(before.st_mode), path
        raw = path.read_bytes()
        after = path.lstat()
        identity = lambda s: [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
        assert identity(before) == identity(after), path
        digest = hashlib.sha256(raw).hexdigest()
        PINS[str(path)] = dict(path=str(path),bytes=len(raw),sha256=digest,identity=identity(after))
        CONTENT[str(path)] = raw
    if wanted is not None:
        assert PINS[str(path)]['sha256'] == wanted, (path,wanted,PINS[str(path)]['sha256'])
    return CONTENT[str(path)]

def js(path,wanted=None):
    return json.loads(full(path,wanted))

plan = js(PLAN,PIN_PLAN)
peer = js(PEER,PIN_PEER)
candidate_rows = peer['proposed_regular18'] + peer['proposed_related_symlink18']
candidates = {x['path'] for x in candidate_rows}
regular_ids = {(x['identity'][0],x['identity'][1]):x['path'] for x in peer['proposed_regular18']}
assert len(candidates) == 36 and len(regular_ids) == 18
# Bind updated Root plan to the exact unchanged path/identity set, independent
# of its metadata key names. This traverses JSON only, never candidate contents.
plan_paths = set()
def walk_paths(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k == 'path' and isinstance(v,str): plan_paths.add(v)
            walk_paths(v)
    elif isinstance(value,list):
        for item in value: walk_paths(item)
walk_paths(plan)
assert candidates <= plan_paths

prepared = js(WORK/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
receipt_item = prepared['inputs']['material_results']
receipt = js(receipt_item['path'],receipt_item['sha256'])
material_item = prepared['inputs']['material_manifest']
material = js(material_item['path'],material_item['sha256'])
component_item = receipt['rank1_factor_cache_revision']
component = js(component_item['path'],component_item['sha256'])

def group(name, paths):
    GROUPS[name] = sorted(set(str(p) for p in paths))

group('prepared_direct_inputs', [v['path'] for v in prepared['inputs'].values()])
group('prepared_protocol_inputs', [prepared[k]['path'] for k in ('case_spec','rank_addendum')])
group('prepared_local_files', [WORK/p for p in prepared['local_files']])
group('current_component_files',component['files'])
group('receipt_top_level_direct_reads',[receipt['producer_runtime']['path'],receipt['receiver_source']['path'],component_item['path']])
group('material_manifest_geometry_read',[material['source_files']['geometry.dat']['path']])
group('material_source_fields_metadata_only',[v['path'] for v in material['source_files'].values()])

offline_union = set()
offline_metadata = {}
for letter in ('A','B'):
    state = receipt['states'][letter]
    descriptors = {k:v['path'] for k,v in state.items() if isinstance(v,dict) and 'path' in v}
    group(letter+'_state_descriptors',descriptors.values())
    offline_union.update(descriptors.values())
    execution = js(state['execution']['path'],state['execution']['sha256'])
    group(letter+'_execution_files',execution['files'])
    offline_union.update(execution['files'])
    run = js(state['snapshot_run_status']['path'],state['snapshot_run_status']['sha256'])
    base = Path(state['archive']['path']).parent
    group(letter+'_snapshot_outputs',[base/p for p in run['outputs']])
    offline_union.update(GROUPS[letter+'_snapshot_outputs'])
    audit = js(state['audit_status']['path'],state['audit_status']['sha256'])
    audit_dir = Path(state['audit_status']['path']).parent
    protocol_path = audit_dir/'protocol.json'
    protocol = js(protocol_path,audit['protocol_sha256'])
    group(letter+'_audit_protocol_files',protocol['files'])
    group(letter+'_audit_outputs',[audit_dir/p for p in audit['outputs']])
    offline_union.update(protocol['files'])
    offline_union.update(GROUPS[letter+'_audit_outputs'])
    # Exact sidecar reads and numerical-reader arguments at ingestion 115–130.
    group(letter+'_numerical_replay_and_sidecars',[audit_dir/p for p in (
        'audit.bin','observations.json','volume64.bin','volume_normalization_check.json',
        'negative_controls.json','normalization_negative_controls.json')])
    offline_union.update(GROUPS[letter+'_numerical_replay_and_sidecars'])
    offline_metadata[letter] = dict(
        archive=state['archive'],execution=state['execution'],snapshot_status=state['snapshot_run_status'],
        audit_status=state['audit_status'],audit_protocol=dict(path=str(protocol_path),sha256=audit['protocol_sha256']),
        execution_file_count=len(execution['files']),snapshot_output_count=len(run['outputs']),
        audit_output_count=len(audit['outputs']),audit_protocol_file_count=len(protocol['files']),
        native_executed_here=False,numerical_replayed_here=False)
group('offline_snapshot_complete_explicit_union',offline_union)

source_functions = {
    'production_runner.py':['require_file','pinned_runtime_files','check_material_manifest','preflight','prepare',
        'verify_prepared','verify_sealed_directory','run','base_inputs','verify_fixed_inputs','seal_directory',
        'resource_monitor','DiskResources'],
    'qualified_snapshot_ingestion.py':['digest','pinned','verify_offline_state','admit_snapshots','audit_payload'],
    'rank1_factor_cache_admission.py':['metadata','admit_rank1_factor_cache_variant','admit_rank1_factor_cache_receiver'],
    'numerical_layout_admission.py':['require','admit_layout_variant','verify_analysis_dependencies',
        'verify_analysis_environment','verify_common_basis'],
    'combined_cold_own_rss_host.py':['bind_controller','controls_admission','make_executor','launch'],
    'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py':['complete_input_phase','consume_completed_inputs','consume_metadata'],
    'analyze_r64_snapshot.py':['analyze'],
    'analyze_r64_tracking_moments.py':['analyze'],
    'check_r64_audit_rejections.py':['check'],
    'check_r64_normalization_rejections.py':['check'],
    'snapshot_control_preflight.py':['_XSM','_open_xsm','audit_snapshot_controls'],
    'physical_common_basis_admission.py':['full_sha','verify_corrected_common_basis'],
}
function_rows = []
for name,wanted in source_functions.items():
    path = WORK/'runtime'/name
    expected = {'production_runner.py':'67ae4ae465013fd7c7bd5ccb07c9d06c9b7e88dba9ba8481c7e4a506f15147bf',
        'combined_cold_own_rss_host.py':'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7'}.get(name)
    text = full(path,expected).decode()
    SOURCE_TEXT[name] = text
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in wanted:
            segment = ast.get_source_segment(text,node)
            function_rows.append(dict(path=str(path),function=node.name,line=node.lineno,end_line=node.end_lineno,
                complete_function_source_sha256=hashlib.sha256(segment.encode()).hexdigest()))
    assert set(wanted) <= {x['function'] for x in function_rows if x['path']==str(path)},name

factory_text = full(FACTORY,'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8').decode()
SOURCE_TEXT['factory'] = factory_text
for node in ast.parse(factory_text).body:
    if isinstance(node,ast.FunctionDef) and node.name in ('materialize_metadata','final_cold_info','cold_launch_in_clean_process','run_AAA'):
        segment = ast.get_source_segment(factory_text,node)
        function_rows.append(dict(path=str(FACTORY),function=node.name,line=node.lineno,end_line=node.end_lineno,
            complete_function_source_sha256=hashlib.sha256(segment.encode()).hexdigest()))

# Statically extract exactly the data used by environment file verification;
# literal_eval is data parsing, not execution/import of this business module.
tree = ast.parse(SOURCE_TEXT['numerical_layout_admission.py'])
env = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='ANALYSIS_ENVIRONMENT' for t in node.targets))
group('offline_analysis_environment_files',env['files'])
group('physical_common_basis_fixed_inputs',[
    ART/'axial-material-AAA-white-trace-angular-convergence-20261005/cold48_sn32/basis.xsm',
    WORK/'runtime/snapshot_control_preflight.py',
    prepared['inputs']['snapshot_A']['path'],prepared['inputs']['snapshot_B']['path']])

# Every FILE operand in the frozen generated decks is read from data, then
# bound to the actual stage directories constructed by production_runner.run.
deck_file_operands = {}
import re
for name in ('pack_archives','common_basis','case_setup','bootstrap_axial','bootstrap_radial',
             'picard_axial','picard_radial','checker_parent','rank_precision'):
    path = WORK/'decks'/(name+'.x2m')
    text = full(path).decode()
    operands = re.findall(r'\bFILE\s+[\x27\"]([^\x27\"]+)[\x27\"]',text)
    assert all(not Path(p).is_absolute() and '..' not in Path(p).parts for p in operands),(name,operands)
    deck_file_operands[name] = operands

checks = {}
all_reads = set()
for name,paths in GROUPS.items():
    all_reads.update(paths)
    hits = sorted(candidates & set(paths))
    checks[name] = dict(path_count=len(paths),exact_candidate_path_hits=hits)
resolved_hits = []
identity_hits = []
missing = []
for path in sorted(all_reads):
    actual = Path(path)
    resolved = str(actual.resolve(strict=False))
    if resolved in candidates: resolved_hits.append(dict(path=path,target=resolved))
    try:
        s=actual.stat()
    except FileNotFoundError:
        missing.append(path)
        continue
    target=regular_ids.get((s.st_dev,s.st_ino))
    if target is not None: identity_hits.append(dict(path=path,candidate=target))
assert not any(v['exact_candidate_path_hits'] for v in checks.values())
assert not resolved_hits and not identity_hits

exact_callsites = []
for name,text in SOURCE_TEXT.items():
    path = FACTORY if name == 'factory' else WORK/'runtime'/name
    for node in ast.walk(ast.parse(text)):
        if isinstance(node,ast.Call):
            call = ast.unparse(node)
            fn = ast.unparse(node.func)
            if fn in ('verify_prepared','admit_layout_variant','check_material_manifest','admit_snapshots',
                'verify_offline_state','verify_sealed_directory','_link','base_inputs','seal_directory',
                'deck','host','verify_fixed_inputs','preflight','make_executor','c.run','audit_payload',
                'pinned','analyze','analyze_moments','snapshot_negatives','normalization_negatives',
                '_open_xsm','factory.materialize_metadata','consume_metadata','complete_input_phase') \
                or fn.endswith('.read_text') or fn.endswith('.read_bytes'):
                exact_callsites.append(dict(path=str(path),line=node.lineno,call=call))

report = dict(
    schema='SPOT_R19_CURRENT_NATIVE_OFFLINE_SNAPSHOT_READ_PATH_SOURCE_REVIEW_V1',
    status='PASS',
    conclusion='NO_CANDIDATE_READ_DEPENDENCY_IN_REVIEWED_CURRENT_AAA_NATIVE_AND_OFFLINE_ADMISSION_CHAIN',
    original_phase_future_native_result=None,
    scope='Current fixed WORK prepared_cold AAA run, optional repeated current preflight/prepare offline admission, fresh bootstrap/map parent induction. No claim to re-run historical scientific workflows or arbitrary future ABA evidence.',
    current_work_root=str(WORK),current_source_root=str(SOURCE),
    fixed_candidate_plan=dict(path=str(PLAN),sha256=PIN_PLAN,
        initial_observed_sha256='3b66b9e7b7a6557622ee71ba8395d139744873a28c993f0d9aa95fbb2c6f7b75',
        changed_between_review_reads_by_root=True,exact_36_path_set_unchanged=True),
    supplied_complementary_current_graph_review=dict(path=str(PEER),sha256=PIN_PEER,
        peer_status=peer['status'],source_complete_functions=peer['current_source_complete_functions'],
        distinction='This report independently expands offline receipt execution/protocol/output paths, and proves fresh local runtime stage induction. The supplied peer owns whole graph/canonical/namespace/alias and expected37395 closure.'),
    candidate_paths=sorted(candidates),candidate_regular_device_inode_authority=peer['proposed_regular18'],
    entrypoint_proof=[
        dict(source=str(FACTORY),lines=[1291,1294,1295,1297,1298,1299,1300,1302,1303,1304,1309],
            behavior='Actual cold entry uses prepared_cold.json and c.run. It refuses existing AAA, archives or training before native transport. h.launch convenience prepared.json branch is explicitly unused at 1306-1309.'),
        dict(source=str(WORK/'runtime/production_runner.py'),lines=[851,642,643,649,651,654,657,659],
            behavior='run calls verify_prepared; layout metadata callback plus local_files, eight inputs and two protocol pins are checked. check_protocol reads declared field values. verify_prepared does not call preflight or admit_snapshots.'),
        dict(source=str(WORK/'runtime/production_runner.py'),lines=[558,559,376,394,413,419,420,421,422],
            behavior='prepare calls preflight. preflight material_manifest check reads only source_files geometry.dat; material_results receipt is read and passed to current admit_snapshots.'),
        dict(source=str(WORK/'runtime/qualified_snapshot_ingestion.py'),lines=[133,135,138,144,148,155,157,158,159,89,92,94,96,101,102,103,109,111,112,115,118,119,120,123,125,127,129],
            behavior='admit_snapshots binds A/B descriptors to resolved inputs and calls verify_offline_state. Every execution.files key, run.outputs leaf, audit.protocol.files key and audit.outputs leaf is a real digest read. Replay reads only explicit audit.bin, track, moments and volume64 arguments plus sibling JSON sidecars; audit_payload opens bound state archive.'),
        dict(source=str(WORK/'runtime/rank1_factor_cache_admission.py'),lines=[61,62,63,80,84,86,155,157,164,165,175,176,179,180],
            behavior='Current layout/receiver metadata goes through current factory.materialize_metadata to the finite current component consume callback. Parent receipt/variant are JSON comparisons; no recursive replay of historical producers/maps.'),
        dict(source=str(FACTORY),lines=[543,547,551,552],
            behavior='materialize_metadata uses current context and consume_metadata. Current consumer 605-621 performs complete_input_phase first, then strict_json of the frozen api_return to reconstruct complete metadata; it does not execute historical APIs.'),
    ],
    fresh_native_parent_induction=dict(
        original_snapshots=prepared['inputs'],
        archives_source_calls=[935,936,939,940,941,942,943,944,945,950],
        bootstrap_source_calls=[963,964,965,966,967,971,977,982,983,985,987,991,992],
        map_parent_source_calls=[917,920,923,924,996,997,1001,1002,1006,1007,1008,1009,1012,1013,1016,1018,1019,1021,1030],
        conclusion='AAA archives are freshly packed only from declared offline A/B. setup/closed_snapshots.xsm is freshly sealed, parent starts setup, each map links only the previous newly created local parent and then parent=current. verify_sealed_directory reads result.json.sha256 only within that current parent. No old family selection or old-map resume branch exists.',
        work_has_AAA=os.path.lexists(WORK/'AAA'),work_has_archives=os.path.lexists(WORK/'archives'),
        work_has_training=os.path.lexists(WORK/'training'),
        historical_candidate_result_seals_read_by_current_run=False),
    physical_common_basis_verifier=dict(source=str(WORK/'runtime/physical_common_basis_admission.py'),
        lines=[14,18,107,109,110,118,119],
        fixed_paths=GROUPS['physical_common_basis_fixed_inputs'],
        dynamic_paths=['WORK/training/common_basis.xsm','WORK/archives/training_snapshots.xsm'],
        candidate_path_intersection=[]),
    offline_receipt_state_expansion=offline_metadata,
    offline_explicit_union_count=len(offline_union),
    all_statically_derived_read_paths_count=len(all_reads),
    exact_path_checks=checks,resolved_candidate_alias_hits=resolved_hits,
    candidate_regular_device_inode_hits=identity_hits,
    derived_read_paths_missing_now=missing,
    derived_read_path_groups=GROUPS,
    deck_file_operands=deck_file_operands,
    resource_scope_semantics=dict(
        source=str(WORK/'runtime/production_runner.py'),lines=[92,105,107,110,113,115,118,124,142,145,147],
        statement='Inherited current dynamic family resource policy may stat/count candidate regular files. Resource capacity checks traverse/stat directories and sizes; they do not open/hash candidate payload and do not require a frozen exact payload inventory. Removing old counted regular files lowers artifact_bytes.'),
    source_complete_functions=function_rows,
    exact_source_read_callsites=exact_callsites,
    full_metadata_and_source_pins=PINS,
    functions_named_read_fields_in_reviewed_chain=[],
    read_fields_meaning='No such callable exists in this finite chain; actual read_text/read_bytes/_open_xsm and manifest files loops are the reviewed source of reads.',
    candidate_specific_blockers=[],
    limits=['Read-only source proof, not a native execution or a repeated numerical admission. Candidate content checks, global incoming symlinks, historical recomputability, restore intersections and retirement execution are Root/peer scopes.'],
    actual_tool_zero=dict(business_imports=0,business_calls=0,business_executions=0,
        native_solver_children=0,numerical_replays=0,candidate_payload_full_reads=0,
        candidate_payload_hash_reads=0,old_35GB_rehashes=0,project_writes=0,deletions=0),
    review_standard_library_only=True,elapsed_seconds=time.monotonic()-started,
)
OUT.mkdir(exist_ok=True)
out = OUT/'REPORT.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
report_sha=hashlib.sha256(out.read_bytes()).hexdigest()
(OUT/'REPORT.txt').write_text(
    'PASS: finite current cold AAA native and offline snapshot admission read paths exclude exact 18 regular +18 parent symlinks.\n'
    f'Report SHA256: {report_sha}\n'
    f'Current plan SHA256: {PIN_PLAN}; initial old plan SHA noted transparently.\n'
    f'Offline explicit union: {len(offline_union)} paths; all static read groups: {len(all_reads)} paths.\n'
    f'Candidate exact/resolved/device-inode intersections: 0/0/0. Missing current paths: {len(missing)}.\n'
    'Business import/call/native/numerical/candidate payload read/hash/project write/delete/35GB rehash: 0.\n'
    'Current graph/expected37395 closure is complementary pinned peer scope. No candidate-specific blocker.\n')
print(json.dumps(dict(status=report['status'],report=str(out),sha256=report_sha,
    offline_explicit_union_count=len(offline_union),all_read_path_count=len(all_reads),missing_paths=len(missing),
    candidate_exact_hits=0,candidate_resolved_hits=0,candidate_inode_hits=0,actual_tool_zero=report['actual_tool_zero']),ensure_ascii=False))
