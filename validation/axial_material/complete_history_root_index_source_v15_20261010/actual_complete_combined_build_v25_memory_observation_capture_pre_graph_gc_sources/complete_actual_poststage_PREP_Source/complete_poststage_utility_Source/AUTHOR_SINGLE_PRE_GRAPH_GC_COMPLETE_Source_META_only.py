import ast
import copy
import hashlib
import json
import os
import pathlib
import stat
import tempfile

P = pathlib.Path('/private/tmp/axmat_P4_BUILD_exact_declaration_reader_minimal_UNREADY_Source_66od7kgz')
EXPECTED_MF = 'cedc1311c69b4e09d589a145a0757288658585c8939186a5cfc29fa682b506fe'
PROPOSAL_PEER = pathlib.Path('/private/tmp/spot_independent_readonly_single_pre_graph_gc_proposal_review_20261011_0qgkav70.json')
PAIRS = [('v25_memory_observation_capture', 'v25_memory_observation_capture_pre_graph_gc'),
         ('v25-memory-observation-capture', 'v25-memory-observation-capture-pre-graph-gc')]
OLD = "    del specs,original_aliases\n    memory_diagnostic_point(phase,'verify_graph_enter')\n"
NEW = "    del specs,original_aliases\n    gc.collect()\n    memory_diagnostic_point(phase,'verify_graph_enter')\n"
CHECKS = []


def check(name, passed):
    assert type(passed) is bool
    assert name not in {r['name'] for r in CHECKS}
    CHECKS.append(dict(name=name, passed=passed))
    if not passed:
        raise ValueError(name)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def finite_json(raw):
    def pairs(items):
        value = {}
        for k, v in items:
            if k in value:
                raise ValueError('duplicate JSON key')
            value[k] = v
        return value
    def reject(value):
        raise ValueError('nonfinite JSON')
    return json.loads(raw.decode(), object_pairs_hook=pairs, parse_constant=reject)


def read(path):
    s = path.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and 0 <= s.st_size <= 1048576
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb', buffering=0) as f:
        assert identity(os.fstat(f.fileno())) == identity(s)
        raw = f.read(s.st_size + 1)
        assert len(raw) == s.st_size and identity(os.fstat(f.fileno())) == identity(s)
    assert identity(path.lstat()) == identity(s)
    return raw, dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=identity(s))


def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    return read(path)[1]


def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def retarget(text):
    for old, new in PAIRS:
        text = text.replace(old, new)
    return text


def reverse(text, rows):
    results = []
    for r in reversed(rows):
        actual = text.count(r['new'])
        assert actual == r['count'], (r['label'], actual, r['count'])
        results.append(dict(label=r['label'], expected=r['count'], actual=actual))
        text = text.replace(r['new'], r['old'])
    return text, results


def definition_metadata(original, current):
    kinds = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    old = [n for n in ast.parse(original).body if isinstance(n, kinds)]
    new = [n for n in ast.parse(current).body if isinstance(n, kinds)]
    seen = {}
    records = []
    for i, n in enumerate(old):
        occurrence = seen.get(n.name, 0)
        seen[n.name] = occurrence + 1
        candidates = [q for q in new if q.name == n.name]
        unchanged = occurrence < len(candidates) and ast.get_source_segment(original, n) == ast.get_source_segment(current, candidates[occurrence]) and ast.dump(n, include_attributes=False) == ast.dump(candidates[occurrence], include_attributes=False)
        records.append(dict(name=n.name, occurrence=i, whole_bytes_and_AST_unchanged=unchanged))
    return dict(original_count=len(old), new_count=len(new), unchanged_original_definition_occurrences=records)


MF_RAW, MF_PIN = read(P / 'MANIFEST.json')
M = finite_json(MF_RAW)
check('exact_sealed_A5_parent_manifest_SHA', MF_PIN['sha256'] == EXPECTED_MF)
check('parent_strict_UNREADY_Source_only', M['source_only'] is True and M['candidate_or_business_executed'] is False)
ROOT_FILES = {str(p.relative_to(P)) for p in P.rglob('*') if p.is_file()}
ROOT_DIRS = {'.', *[str(p.relative_to(P)) for p in P.rglob('*') if p.is_dir()]}
check('parent_complete_member_enumeration', ROOT_FILES == set(M['members']) | {'MANIFEST.json'})
check('parent_complete_directory_enumeration', ROOT_DIRS == set(M['directories']))
BASE = {}
BASE_PINS = {}
for rel, declared in M['members'].items():
    raw, pin = read(P / rel)
    check('parent_full_EOF_SHA_7ID_' + rel, pin == {k: declared[k] for k in ('path', 'sha256', 'size_bytes', 'identity')})
    BASE[rel] = raw
    BASE_PINS[rel] = pin
check('parent_complete_Python_Source_AST', sum(1 for rel, raw in BASE.items() if rel.endswith('.py') and ast.parse(raw.decode())) == M['complete_Python_Source_AST_count'])
PEER_RAW, PEER_PIN = read(PROPOSAL_PEER)
PEER = finite_json(PEER_RAW)
check('different_author_readonly_17B_proposal_PASS_only', PEER['status'] == 'PASS_MINIMAL_ONE_CALL_SOURCE_PROPOSAL_ONLY_NO_EXECUTION_OR_RSS_QUALIFICATION' and PEER['reviewer_is_proposal_author'] is False and PEER['actual_RSS_or_build_or_scientific_qualification_created'] is False)
PROOF = finite_json(BASE['COMPLETE_SOURCE_INVERSES.json'])
ROLE_PATHS = PROOF['role_current_paths']
check('all_original_14_production_roles_retained', len(ROLE_PATHS) == 14)
check('actual_consumed_canonical_transform_count31', len(PROOF['exact_finite_transforms']['canonical']) == 31)
check('actual_consumed_canonical_row17_exact_label', PROOF['exact_finite_transforms']['canonical'][17]['label'] == 'complete_input_atomic_boundary_2')
Q = pathlib.Path(tempfile.mkdtemp(prefix='axmat_single_pre_graph_gc_complete_UNREADY_Source_', dir='/private/tmp'))
UPDATED = {}
LAYER_ROWS = {}
for role, rel in ROLE_PATHS.items():
    original = BASE[rel].decode()
    current = retarget(original)
    rows = [dict(label='fresh_namespace_' + old, old=old, new=new, count=original.count(old)) for old, new in PAIRS if old in original]
    if role == 'canonical':
        check('canonical_unique_exact_gc_insertion_anchor', current.count(OLD) == 1)
        current = current.replace(OLD, NEW, 1)
        rows.append(dict(label='single_pre_graph_gc_after_original_last_use_before_inactive_audit', old=OLD, new=NEW, count=1))
    recovered, counts = reverse(current, rows)
    check('whole_current_to_A5_byte_inverse_' + role, recovered == original)
    check('whole_current_to_A5_AST_inverse_' + role, ast.dump(ast.parse(recovered), include_attributes=False) == ast.dump(ast.parse(original), include_attributes=False))
    normalized = current
    if role == 'canonical':
        normalized = normalized.replace(NEW, OLD, 1)
    for old, new in reversed(PAIRS):
        normalized = normalized.replace(new, old)
    check('only_namespace_and_allowed_17B_runtime_delta_' + role, normalized == original)
    UPDATED[rel] = current.encode()
    LAYER_ROWS[role] = dict(relative_path=rel, A5_parent_Source_pin=BASE_PINS[rel], finite_transforms=rows, inverse_counts=counts, complete_A5_byte_and_AST_inverse=True)

# The consumed proof still has exactly the original rows, order, old blocks and counts.
NEW_PROOF = copy.deepcopy(PROOF)
for role, rows in NEW_PROOF['exact_finite_transforms'].items():
    for r in rows:
        r['new'] = retarget(r['new'])
NEW_PROOF['exact_finite_transforms']['canonical'][17]['new'] = '    gc.collect()\n' + NEW_PROOF['exact_finite_transforms']['canonical'][17]['new']
JSON_EDITS = []
for role, rows in NEW_PROOF['exact_finite_transforms'].items():
    for i, r in enumerate(rows):
        old_r = PROOF['exact_finite_transforms'][role][i]
        if r != old_r:
            JSON_EDITS.append(dict(field=['exact_finite_transforms', role, i, 'new'], old=old_r['new'], new=r['new']))
    current = UPDATED[ROLE_PATHS[role]].decode()
    parent = BASE['ORIGINAL_PARENT_SOURCE/' + role + '.full.py'].decode()
    inverse, counts = reverse(current, rows)
    check('actual_consumer_all_counted_rows_to_original_parent_' + role, inverse == parent)
    check('actual_consumer_whole_AST_to_original_parent_' + role, ast.dump(ast.parse(inverse), include_attributes=False) == ast.dump(ast.parse(parent), include_attributes=False))
    recalculated = definition_metadata(parent, current)
    check('complete_definition_metadata_is_honest_' + role, recalculated == NEW_PROOF['definitions_by_role'][role])
    LAYER_ROWS[role]['current_to_original_parent_inverse_counts'] = counts
    LAYER_ROWS[role]['definitions'] = recalculated
    check('consumer_old_and_count_and_row_order_unchanged_' + role, len(rows) == len(PROOF['exact_finite_transforms'][role]) and all(r['old'] == o['old'] and r['count'] == o['count'] and r['label'] == o['label'] for r, o in zip(rows, PROOF['exact_finite_transforms'][role])))
RECOVER_PROOF = copy.deepcopy(NEW_PROOF)
for edit in reversed(JSON_EDITS):
    value = RECOVER_PROOF
    for key in edit['field'][:-1]:
        value = value[key]
    assert value[edit['field'][-1]] == edit['new']
    value[edit['field'][-1]] = edit['old']
check('whole_consumed_proof_JSON_inverse_equals_exact_A5_object', RECOVER_PROOF == PROOF)
UPDATED['COMPLETE_SOURCE_INVERSES.json'] = dump(NEW_PROOF)
FIXED_REL = 'utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json'
UPDATED[FIXED_REL] = retarget(BASE[FIXED_REL].decode()).encode()
fixed = finite_json(UPDATED[FIXED_REL])
fixed_parent = finite_json(BASE[FIXED_REL])
check('fixed_contract_only_10_fresh_namespace_literal_changes', sum(BASE[FIXED_REL].decode().count(old) for old, new in PAIRS) == 10)
fixed_inverse = UPDATED[FIXED_REL].decode()
for old, new in reversed(PAIRS):
    fixed_inverse = fixed_inverse.replace(new, old)
check('fixed_complete_contract_whole_byte_inverse_A5', fixed_inverse.encode() == BASE[FIXED_REL])
for key in ['seven_author_role_Source_pins', 'author_manifest', 'author_peer_manifest', 'actual_new_PREP_bound_Source_manifest', 'actual_new_PREP_business_pins', 'actual_new_BUILD_business_pins', 'future_actual_diagnostic_resource_environment_witness']:
    check('fixed_future_unknown_remains_None_' + key, fixed[key] is None)
check('all_10_fresh_runtime_namespaces_absent_no_old_output_reuse', len(fixed['namespaces']) == 10 and all(not os.path.lexists(value) for value in fixed['namespaces'].values()))
for rel, raw in BASE.items():
    write(Q / rel, UPDATED.get(rel, raw))
write(Q / 'SINGLE_PRE_GRAPH_GC_PROVENANCE/ORIGINAL_A5_MANIFEST.byte_exact.json', MF_RAW)
write(Q / 'SINGLE_PRE_GRAPH_GC_PROVENANCE/DIFFERENT_AUTHOR_17B_PROPOSAL_REVIEW.byte_exact.json', PEER_RAW)
METHOD_RAW, METHOD_PIN = read(pathlib.Path(__file__))
write(Q / 'AUTHOR_SINGLE_PRE_GRAPH_GC_COMPLETE_Source_META_only.py', METHOD_RAW)

ROLES = {role: read(Q / rel)[1] for role, rel in ROLE_PATHS.items()}
for role in LAYER_ROWS:
    LAYER_ROWS[role]['current_Source_pin'] = ROLES[role]
COMPLETE_PROOF_PIN = read(Q / 'COMPLETE_SOURCE_INVERSES.json')[1]
INVERSE = dict(schema='SINGLE_PRE_GRAPH_GC_FRESH_NAMESPACE_COMPLETE_14_ROLE_AND_CONSUMED_JSON_INVERSE_V1', source_only=True, status='AUTHOR_SOURCE_ONLY_UNREADY_NOT_RUNTIME_QUALIFICATION', namespace_pairs=PAIRS, parent_manifest_pin=MF_PIN, different_author_17B_proposal_review_pin=PEER_PIN, roles=LAYER_ROWS, actual_consumed_complete_inverse_pin=COMPLETE_PROOF_PIN, actual_consumed_complete_inverse_parent_pin=BASE_PINS['COMPLETE_SOURCE_INVERSES.json'], complete_consumed_proof_JSON_edits=JSON_EDITS, complete_consumed_proof_JSON_inverse_equals_parent=True, consumed_canonical_row_count=31, consumed_canonical_gc_row_index=17, consumed_canonical_gc_row_label='complete_input_atomic_boundary_2', fixed_contract_parent_pin=BASE_PINS[FIXED_REL], fixed_contract_current_pin=read(Q / FIXED_REL)[1], fixed_contract_namespace_pairs=PAIRS, fixed_contract_whole_byte_inverse_to_A5=True, runtime_behavior_delta_only_17_bytes=True, existing_A5_namespace_P4_V3_and_original_parent_inverse_proofs_are_lineage_and_preserved=True, candidate_binder_guard_resource_API_or_business_executed=False, runtime_RSS_or_science_qualified=False)
INVERSE_PIN = write(Q / 'SINGLE_PRE_GRAPH_GC_COMPLETE_14_ROLE_AND_ACTUAL_CONSUMED_PROOF_INVERSES.json', dump(INVERSE))
CANON = UPDATED[ROLE_PATHS['canonical']].decode()
ct = ast.parse(CANON)
check('gc_is_already_top_level_imported_no_import_added', any(isinstance(n, ast.Import) and any(a.name == 'gc' for a in n.names) for n in ct.body))
phase = next(n for n in ct.body if isinstance(n, ast.FunctionDef) and n.name == 'complete_input_phase')
for i, n in enumerate(phase.body):
    if isinstance(n, ast.Delete) and [ast.unparse(x) for x in n.targets] == ['specs', 'original_aliases']:
        check('one_gc_call_after_last_use_before_active_audit', ast.unparse(phase.body[i+1]) == 'gc.collect()' and ast.unparse(phase.body[i+2]) == "memory_diagnostic_point(phase, 'verify_graph_enter')" and isinstance(phase.body[i+3], ast.With))
check('original_helper3b_and_Q_admission_functions_whole_Source_unmodified', all(ast.get_source_segment(CANON, next(n for n in ct.body if isinstance(n, ast.FunctionDef) and n.name == name)) == ast.get_source_segment(BASE[ROLE_PATHS['canonical']].decode(), next(n for n in ast.parse(BASE[ROLE_PATHS['canonical']].decode()).body if isinstance(n, ast.FunctionDef) and n.name == name)) for name in ['helper_Q_admission', 'input_modules', 'current_input_predicates', 'environment', 'run_build']))
check('two_complete_graph_calls_all_original_body_byteexact_after_gc_inverse', CANON.replace(NEW, OLD, 1) == retarget(BASE[ROLE_PATHS['canonical']].decode()))
check('reader16MiB_minimal_fix_function_only_namespace_retargeted', ast.get_source_segment(UPDATED[ROLE_PATHS['build_binder']].decode(), next(n for n in ast.parse(UPDATED[ROLE_PATHS['build_binder']].decode()).body if isinstance(n, ast.FunctionDef) and n.name == 'read')) == retarget(ast.get_source_segment(BASE[ROLE_PATHS['build_binder']].decode(), next(n for n in ast.parse(BASE[ROLE_PATHS['build_binder']].decode()).body if isinstance(n, ast.FunctionDef) and n.name == 'read'))))
for role, rel in ROLE_PATHS.items():
    text = UPDATED[rel].decode()
    assignments = {n.targets[0].id: n.value for n in ast.parse(text).body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    old_assignments = {n.targets[0].id: n.value for n in ast.parse(BASE[rel].decode()).body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    none_names = [k for k, n in old_assignments.items() if isinstance(n, ast.Constant) and n.value is None and (k.startswith('FUTURE') or k in ['AUTHOR', 'AUTHOR_SHA', 'AUTHOR_PEER', 'AUTHOR_PEER_SHA', 'AUTHOR_SEAL', 'AUTHOR_SEAL_SHA', 'PREP_BOUND', 'PREP_BOUND_SHA', 'PREP_BINDING', 'PREP_BINDING_SHA', 'AUTHOR_SEAL', 'AUTHOR_SEAL_SHA'])]
    check('all_original_unknown_future_globals_None_' + role, all(isinstance(assignments[k], ast.Constant) and assignments[k].value is None for k in none_names))
    LAYER_ROWS[role]['all_original_unknown_future_None_globals'] = none_names
# Full binder consumer functions are Source-read and retained; nothing is invoked.
for role in ['prepare_binder', 'build_binder']:
    check('actual_binder_consumer_uses_fixed_current_proof_filename_' + role, "proof=read(HERE/'COMPLETE_SOURCE_INVERSES.json')" in UPDATED[ROLE_PATHS[role]].decode())
SOURCE_AST_COUNT = 0
ALL_PINS = {}
for p in sorted(Q.rglob('*')):
    if p.is_file():
        raw, pin = read(p)
        ALL_PINS[str(p.relative_to(Q))] = pin
        if p.suffix == '.py':
            ast.parse(raw.decode())
            SOURCE_AST_COUNT += 1
check('new_complete_Source_smallMETA_all_members_EOF_SHA_7ID', len(ALL_PINS) == len(BASE) + 4)
check('all_unmodified_A5_members_literal_preserved', all(read(Q / rel)[0] == raw for rel, raw in BASE.items() if rel not in UPDATED))
check('all_parent_Source_fullpins_unchanged_after_derivation', all(read(P / rel)[1] == pin for rel, pin in BASE_PINS.items()) and read(P / 'MANIFEST.json')[1] == MF_PIN)
REPORT = dict(schema='AUTHOR_COMPLETE_SINGLE_PRE_GRAPH_GC_FRESH_NAMESPACE_SOURCE_REPORT_V1', status='UNREADY_COMPLETE_SOURCE_ONLY_PENDING_DIFFERENT_AUTHOR_REVIEW_NO_RSS_CREDIT', source_only=True, check_count=len(CHECKS), checks=CHECKS, all_checks_typed_true=all(r['passed'] is True for r in CHECKS), blockers=[], qualified_role_Source_pins={k: p for k, p in ROLES.items() if k in ['canonical', 'prepare_binder', 'build_binder', 'prepare_host', 'prepare_writer', 'build_host', 'build_writer']}, qualified_utility_Source_pins={k: p for k, p in ROLES.items() if k not in ['canonical', 'prepare_binder', 'build_binder', 'prepare_host', 'prepare_writer', 'build_host', 'build_writer']}, actual_consumed_complete_inverse_pin=COMPLETE_PROOF_PIN, complete_14_role_fresh_namespace_and_17B_inverse_pin=INVERSE_PIN, parent_manifest_pin=MF_PIN, different_author_prior_17B_proposal_review_pin=PEER_PIN, actual_future_environment_business_or_Source_qualification_pins=None, no_Runtime_RSS_BUILD_native_AAA_ABA_or_science_qualification=True, project_C_old_frozen_D_E_or_results_modified=False, candidate_binder_helper_guard_PS_lsof_resource_API_material_or_business_executed=False, original_full_graph_owners_EOF_SHA_identity_float_signedzero_algorithms_inputs_guard_MRO_nine_caps_retained=True, original_caps=dict(whole_wall_seconds=1800, stage_wall_seconds=600, rss_mib=512, joint_archive_bytes=2*2**30, history_bytes=96*2**30, free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0), fresh_namespaces=fixed['namespaces'], canonical_function_behavior_change='exact17B gc.collect() after del specs,original_aliases before ReadOpenAudit activation', complete_Python_Source_AST_count_before_author_report=SOURCE_AST_COUNT, all_current_member_fullpins_before_author_report=ALL_PINS, old_reports_and_proofs_are_complete_byte_exact_lineage_not_current_qualification=True, future_independent_consumer_contract=dict(report_schema='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1', report_status='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION', required_fields=['source_only','all_checks_typed_true','blockers','check_count','checks','qualified_complete_Source_manifest_pin','qualified_role_Source_pins','qualified_utility_Source_pins'], peer_top_level_review='REVIEW.json', MF_members_and_directories='current complete enumerable file fourpins and directory seven-identities', genuine_peer_seal_stdout='manifest_pin/review_pin', one_same_genuine_independent_peer_can_supply_author_and_utility=True))
REPORT_PIN = write(Q / 'AUTHOR_COMPLETE_SINGLE_PRE_GRAPH_GC_FRESH_NAMESPACE_SOURCE_REPORT.json', dump(REPORT))
print(json.dumps(dict(package=str(Q), source_only=True, status=REPORT['status'], strict_all_author_Source_checks_true=True, check_count=len(CHECKS), author_report_pin=REPORT_PIN, actual_consumed_complete_inverse_pin=COMPLETE_PROOF_PIN, complete_14_role_inverse_pin=INVERSE_PIN, role_Source_pins=ROLES, candidate_or_business_executed=False), ensure_ascii=False, sort_keys=True))
