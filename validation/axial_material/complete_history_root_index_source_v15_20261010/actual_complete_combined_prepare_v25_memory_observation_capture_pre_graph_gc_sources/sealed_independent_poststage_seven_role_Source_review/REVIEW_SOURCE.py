import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import tempfile
import traceback

ROOT = Path('/private/tmp/axmat_single_pre_graph_gc_complete_UNREADY_Source_82j4vp0_')
SIBLING = Path(str(ROOT) + '_seal_receipt')
EXPECTED = '8ddab63da54f05828a93728b50a7c2cff680973409022725e64e5b083cbdf854'
PARENT = Path('/private/tmp/axmat_P4_BUILD_exact_declaration_reader_minimal_UNREADY_Source_66od7kgz')
PARENT_SHA = 'cedc1311c69b4e09d589a145a0757288658585c8939186a5cfc29fa682b506fe'
PAIRS = [('v25_memory_observation_capture', 'v25_memory_observation_capture_pre_graph_gc'), ('v25-memory-observation-capture', 'v25-memory-observation-capture-pre-graph-gc')]
OLD = "    del specs,original_aliases\n    memory_diagnostic_point(phase,'verify_graph_enter')\n"
NEW = "    del specs,original_aliases\n    gc.collect()\n    memory_diagnostic_point(phase,'verify_graph_enter')\n"
CAPS = dict(whole_wall_seconds=1800, stage_wall_seconds=600, rss_mib=512, joint_archive_bytes=2**31, history_bytes=96*2**30, free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)
CHECKS = []
BLOCKERS = []
READS = {}
OUT = Path(tempfile.mkdtemp(prefix='axmat_single_pre_graph_gc_complete_Source_INDEPENDENT_', dir='/private/tmp'))

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def strict(raw):
    def pairs(items):
        d = {}
        for k, v in items:
            if k in d:
                raise ValueError('duplicate JSON key: ' + k)
            d[k] = v
        return d
    def reject(v):
        raise ValueError('nonfinite JSON: ' + v)
    return json.loads(raw.decode('utf-8'), object_pairs_hook=pairs, parse_constant=reject)

def read(path):
    path = Path(path)
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1 or not 0 <= s.st_size <= 4*2**20:
        raise ValueError('bounded regular single-link Source/small META required: ' + str(path))
    before = identity(s)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb', buffering=0) as f:
        if identity(os.fstat(f.fileno())) != before:
            raise ValueError('opened descriptor differs: ' + str(path))
        raw = f.read(s.st_size + 1)
        if len(raw) != s.st_size or f.read(1) != b'' or identity(os.fstat(f.fileno())) != before:
            raise ValueError('full EOF/descriptor stability failure: ' + str(path))
    if identity(path.lstat()) != before:
        raise ValueError('path changed across full EOF: ' + str(path))
    pin = dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), size_bytes=len(raw), identity=before)
    if str(path) in READS and READS[str(path)] != pin:
        raise ValueError('repeated Source/META changed: ' + str(path))
    READS[str(path)] = pin
    return raw, pin

def exact(pin):
    if type(pin) is not dict or set(pin) != {'path', 'sha256', 'size_bytes', 'identity'} or type(pin['size_bytes']) is not int or type(pin['identity']) is not list or len(pin['identity']) != 7 or any(type(n) is not int for n in pin['identity']):
        raise ValueError('strict four-field fullpin required')
    raw, actual = read(pin['path'])
    if actual != pin:
        raise ValueError('declared fullpin mismatch: ' + str(pin['path']))
    return raw

def check(name, passed, evidence=None):
    if type(passed) is not bool or name in {x['check'] for x in CHECKS}:
        raise ValueError('review check must be unique typed bool: ' + name)
    row = dict(check=name, passed=passed)
    if evidence is not None:
        row['evidence'] = evidence
    CHECKS.append(row)
    if not passed:
        BLOCKERS.append(name)

def dump(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()

def write(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    return read(path)[1]

def package(root, expected, label):
    raw, mp = read(root/'MANIFEST.json')
    check(label + '_manifest_full_EOF_SHA', mp['sha256'] == expected, mp)
    mf = strict(raw)
    members = mf['members']
    check(label + '_manifest_strict_member_count', type(mf['member_count']) is int and len(members) == mf['member_count'])
    files = {}
    dirs = {}
    for path in [root, *sorted(root.rglob('*'))]:
        rel = str(path.relative_to(root))
        s = path.lstat()
        if stat.S_ISREG(s.st_mode):
            files[rel] = path
        elif stat.S_ISDIR(s.st_mode):
            dirs[rel] = identity(s)
        else:
            raise ValueError('special member in Source package')
    check(label + '_complete_enumerable_member_domain', set(files) == set(members)|{'MANIFEST.json'})
    check(label + '_complete_directory_seven_identities', dirs == mf['directories'])
    data = {}
    pins = {}
    for rel, declared in members.items():
        raw, pin = read(root/rel)
        check(label + '_full_EOF_SHA_same_7ID:' + rel, pin == declared, pin)
        data[rel], pins[rel] = raw, pin
    py_count = 0
    for rel, raw in data.items():
        if rel.endswith('.py'):
            ast.parse(raw.decode('utf-8'), filename=rel)
            py_count += 1
    check(label + '_all_Python_Source_AST_parsed', py_count == mf['complete_Python_Source_AST_count'])
    return mf, mp, data, pins, dirs

def reverse(text, rows):
    results = []
    for row in reversed(rows):
        if type(row['count']) is not int or row['count'] < 1 or type(row['old']) is not str or type(row['new']) is not str:
            raise ValueError('strict counted inverse transform required')
        observed = text.count(row['new'])
        results.append(dict(label=row['label'], expected=row['count'], observed=observed))
        if observed != row['count']:
            raise ValueError('inverse occurrence count: ' + row['label'])
        text = text.replace(row['new'], row['old'])
    return text, results

def ast_equal(a, b):
    return ast.dump(ast.parse(a), include_attributes=False) == ast.dump(ast.parse(b), include_attributes=False)

def functions(text):
    return {n.name: ast.get_source_segment(text, n) for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

def metadata(original, current):
    kinds = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
    old = [n for n in ast.parse(original).body if isinstance(n, kinds)]
    new = [n for n in ast.parse(current).body if isinstance(n, kinds)]
    seen, results = {}, []
    for i, node in enumerate(old):
        occurrence = seen.get(node.name, 0)
        seen[node.name] = occurrence + 1
        candidates = [q for q in new if q.name == node.name]
        unchanged = occurrence < len(candidates) and ast.get_source_segment(original, node) == ast.get_source_segment(current, candidates[occurrence]) and ast.dump(node, include_attributes=False) == ast.dump(candidates[occurrence], include_attributes=False)
        results.append(dict(name=node.name, occurrence=i, whole_bytes_and_AST_unchanged=unchanged))
    return dict(original_count=len(old), new_count=len(new), unchanged_original_definition_occurrences=results)

def receipt(pin, chunk, label):
    raw = exact(pin)
    d = strict(raw)
    t = d['terminal_tool_return']
    check(label + '_genuine_closed_Source_terminal', d['source_only'] is True and d['closed'] is True and d['observed_terminal'] is True and d['session_repolled_after_close'] is False and type(t) is dict and type(t['exit_code']) is int and t['exit_code'] == 0 and t['chunk_id'] == chunk and 'session_id' not in t, pin)
    check(label + '_no_candidate_or_business_execution', d['candidate_binder_guard_helper_resource_API_PS_lsof_or_business_executed'] is False)
    return strict(t['output'].encode('utf-8'))

def run():
    mf, mp, data, pins, dirs = package(ROOT, EXPECTED, 'current')
    pm, pp, base, basepins, pdirs = package(PARENT, PARENT_SHA, 'A5_parent')
    delivery_raw, delivery_pin = read(SIBLING/'DELIVERY.json')
    delivery = strict(delivery_raw)
    check('current_manifest_matches_delivery_exact_fourpin', mp == delivery['manifest_pin'])
    check('current_expected_complete_counts_113files_11dirs_61AST', len(data)+1 == 113 and len(dirs) == 11 and mf['complete_Python_Source_AST_count'] == 61)
    check('current_source_only_UNREADY_and_no_Runtime_or_science_claim', mf['source_only'] is True and mf['status'] == 'UNREADY_COMPLETE_SOURCE_ONLY_PENDING_DIFFERENT_AUTHOR_REVIEW_NO_RSS_CREDIT' and mf['actual_future_environment_business_or_Source_qualification_pins'] is None and mf['candidate_BINDER_guard_helper_resource_API_PS_lsof_or_business_executed'] is False and mf['runtime_BUILD_RSS_native_or_science_qualified'] is False)
    check('A5_parent_pinned_exact_current_lineage', mf['parent_manifest_pin'] == pp)
    author_stdout = receipt(delivery['actual_author_tool_pin'], 'cf1acd', 'author')
    seal_stdout = receipt(delivery['actual_source_seal_tool_pin'], '3d5dbc', 'author_seal')
    post_stdout = receipt(delivery['actual_full_postseal_tool_pin'], 'e6560b', 'author_postseal')
    check('author_seal_stdout_fullpin_coupling', seal_stdout['manifest_pin'] == mp and seal_stdout['author_report_pin'] == pins[mf['current_author_report']] and seal_stdout['complete_whole_inverse_pin'] == pins[mf['whole_namespace_and_gc_inverse']] and seal_stdout['actual_consumed_complete_inverse_pin'] == pins['COMPLETE_SOURCE_INVERSES.json'])
    check('author_postseal_stdout_matches_current_complete_snapshot', post_stdout['manifest_pin'] == mp and post_stdout['author_report_pin'] == pins[mf['current_author_report']] and post_stdout['all_directory_7ID_equal'] is True and post_stdout['all_member_full_EOF_SHA_7ID_equal'] is True and post_stdout['files'] == 113 and post_stdout['directories'] == 11 and post_stdout['complete_Python_Source_AST_count'] == 61)
    exact(delivery['actual_postseal_report_pin'])
    check('author_and_delivery_no_runtime_credit', delivery['source_only'] is True and delivery['no_Runtime_RSS_BUILD_AAA_ABA_science_credit'] is True and delivery['no_candidate_guard_resource_API_native_or_business_execution'] is True)
    author = strict(data[mf['current_author_report']])
    check('author_249_static_checks_preserved_as_author_evidence_only', type(author['check_count']) is int and author['check_count'] == len(author['checks']) == 249 and all(type(c['passed']) is bool and c['passed'] is True for c in author['checks']) and len({c['name'] for c in author['checks']}) == 249 and author['blockers'] == [])
    check('unchanged_original_nine_caps_typed_exact', delivery['original_nine_caps'] == CAPS and author['original_caps'] == CAPS and all(type(v) is int for v in delivery['original_nine_caps'].values()) and all(type(v) is int for v in author['original_caps'].values()))
    inverse = strict(data[mf['whole_namespace_and_gc_inverse']])
    current_proof = strict(data['COMPLETE_SOURCE_INVERSES.json'])
    parent_proof = strict(base['COMPLETE_SOURCE_INVERSES.json'])
    role_paths = current_proof['role_current_paths']
    check('all_14_production_roles_and_order_retained', role_paths == parent_proof['role_current_paths'] and len(role_paths) == 14 and set(inverse['roles']) == set(role_paths))
    check('actual_consumed_canonical_has_original_31_rows', len(current_proof['exact_finite_transforms']['canonical']) == len(parent_proof['exact_finite_transforms']['canonical']) == 31)
    replay = {}
    for role, rel in role_paths.items():
        current = data[rel].decode()
        old = base[rel].decode()
        rows = inverse['roles'][role]['finite_transforms']
        expected_rows = [dict(label='fresh_namespace_' + a, old=a, new=b, count=old.count(a)) for a, b in PAIRS if a in old]
        if role == 'canonical':
            expected_rows.append(dict(label='single_pre_graph_gc_after_original_last_use_before_inactive_audit', old=OLD, new=NEW, count=1))
        check('only_approved_namespace_and_gc_transforms:' + role, rows == expected_rows)
        recovered, counts = reverse(current, rows)
        check('whole_current_to_A5_byte_inverse:' + role, recovered.encode() == base[rel])
        check('whole_current_to_A5_AST_inverse:' + role, ast_equal(recovered, old))
        check('current_and_A5_role_fullpins:' + role, inverse['roles'][role]['current_Source_pin'] == pins[rel] and inverse['roles'][role]['A5_parent_Source_pin'] == basepins[rel])
        original_rel = 'ORIGINAL_PARENT_SOURCE/' + role + '.full.py'
        original = data[original_rel].decode()
        original_actual = exact(current_proof['original_parent_fullpins'][role]).decode()
        check('original_parent_current_retained_and_actual_full_EOF_bytes:' + role, original == original_actual and base[original_rel] == data[original_rel])
        allrows = current_proof['exact_finite_transforms'][role]
        result, allcounts = reverse(current, allrows)
        check('actual_consumed_whole_byte_inverse_to_original_parent:' + role, result == original)
        check('actual_consumed_whole_AST_inverse_to_original_parent:' + role, ast_equal(result, original))
        prow = parent_proof['exact_finite_transforms'][role]
        check('all_consumed_old_blocks_labels_counts_and_order_unchanged:' + role, len(allrows) == len(prow) and all(c['old'] == p['old'] and c['count'] == p['count'] and c['label'] == p['label'] and type(c['count']) is int for c, p in zip(allrows, prow)))
        calc = metadata(original, current)
        check('complete_definition_occurrence_metadata_honest:' + role, calc == current_proof['definitions_by_role'][role] and calc == inverse['roles'][role]['definitions'])
        replay[role] = dict(relative_path=rel, current_Source_pin=pins[rel], A5_Source_pin=basepins[rel], current_to_A5_counted_replay=counts, current_to_original_parent_counted_replay=allcounts, whole_bytes_and_AST_verified=True, definitions=calc)
    expected_proof = copy.deepcopy(parent_proof)
    for rows in expected_proof['exact_finite_transforms'].values():
        for row in rows:
            for a, b in PAIRS:
                row['new'] = row['new'].replace(a, b)
    expected_proof['exact_finite_transforms']['canonical'][17]['new'] = '    gc.collect()\n' + expected_proof['exact_finite_transforms']['canonical'][17]['new']
    check('whole_actual_consumed_JSON_only_namespace_and_one_gc_row', current_proof == expected_proof)
    gc_row = current_proof['exact_finite_transforms']['canonical'][17]
    check('actual_consumed_canonical_row17_gc_anchored_original_boundary2', gc_row['label'] == 'complete_input_atomic_boundary_2' and gc_row['new'] == '    gc.collect()\n' + parent_proof['exact_finite_transforms']['canonical'][17]['new'])
    fixed_rel = 'utilities/FIXED_SOURCE_OWNER_AND_FUTURE_FACT_CONTRACT.UNREADY.json'
    fixed_raw = data[fixed_rel]
    oldfixed = base[fixed_rel].decode()
    retargeted = oldfixed
    for a, b in PAIRS:
        retargeted = retargeted.replace(a, b)
    check('fixed_complete_owner_contract_only_ten_namespace_literals', fixed_raw.decode() == retargeted and sum(oldfixed.count(a) for a, b in PAIRS) == 10)
    fixed = strict(fixed_raw)
    check('all_ten_new_runtime_namespaces_exact_and_currently_fresh', fixed['namespaces'] == mf['fresh_namespaces'] == delivery['fresh_namespaces'] and len(fixed['namespaces']) == 10 and all(not os.path.lexists(p) for p in fixed['namespaces'].values()))
    future_keys = [k for k, v in strict(base[fixed_rel]).items() if v is None]
    check('all_original_unknown_fixed_future_facts_remain_None', all(fixed[k] is None for k in future_keys))
    canonical = data[role_paths['canonical']].decode()
    old_canonical = base[role_paths['canonical']].decode()
    tree = ast.parse(canonical)
    phase = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'complete_input_phase')
    oldphase = functions(old_canonical)['complete_input_phase']
    newphase = ast.get_source_segment(canonical, phase)
    check('canonical_complete_input_phase_only_exact_17B_behavior_delta', len(newphase.encode()) - len(oldphase.encode()) == 17 and newphase.replace(NEW.strip('\n'), OLD.strip('\n'), 1) == oldphase)
    deletes = [i for i, n in enumerate(phase.body) if isinstance(n, ast.Delete) and [ast.unparse(t) for t in n.targets] == ['specs', 'original_aliases']]
    check('single_pre_graph_gc_at_last_use_and_before_audit', len(deletes) == 1 and ast.unparse(phase.body[deletes[0]+1]) == 'gc.collect()' and ast.unparse(phase.body[deletes[0]+2]) == "memory_diagnostic_point(phase, 'verify_graph_enter')" and isinstance(phase.body[deletes[0]+3], ast.With))
    check('gc_existing_import_no_added_runtime_import', any(isinstance(n, ast.Import) and any(a.name == 'gc' for a in n.names) for n in ast.parse(old_canonical).body) and [ast.dump(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))] == [ast.dump(n) for n in ast.parse(old_canonical).body if isinstance(n, (ast.Import, ast.ImportFrom))])
    funcs = functions(canonical)
    parent_funcs = functions(old_canonical)
    for name in ['helper_Q_admission', 'input_modules', 'current_input_predicates', 'graph_input_bindings', 'environment', 'run_build']:
        check('whole_Q_helper_environment_guard_resource_algorithm_body_unchanged:' + name, funcs[name] == parent_funcs[name])
    check('both_original_full_graph_calls_and_full_open_trace_gates_unchanged', newphase.replace(NEW.strip('\n'), OLD.strip('\n'), 1) == oldphase and newphase.count("g.verify_graph(d['input_graph']['path']") == 1 and newphase.count("g.strict_json(d['input_graph']['path']") == 1 and 'every canonical input and the external graph must be freshly opened once' in newphase and 'paths!=set(files)' in newphase)
    check('original_whole_owner_alias_FLOAT_signedzero_algorithms_preserved_by_all14_inverses', all(r['whole_bytes_and_AST_verified'] is True for r in replay.values()))
    for role, rel in role_paths.items():
        assigns = {n.targets[0].id: n.value for n in ast.parse(data[rel]).body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
        old_assigns = {n.targets[0].id: n.value for n in ast.parse(base[rel]).body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
        unknowns = [name for name, n in old_assigns.items() if isinstance(n, ast.Constant) and n.value is None]
        check('all_original_unknown_top_level_future_globals_None:' + role, all(isinstance(assigns[name], ast.Constant) and assigns[name].value is None for name in unknowns))
    changed = {rel for rel in base if rel in data and data[rel] != base[rel]}
    check('complete_inherited_packet_delta_domain_only_roles_consumedproof_contract', changed == {rel for role, rel in role_paths.items() if inverse['roles'][role]['finite_transforms']}|{'COMPLETE_SOURCE_INVERSES.json', fixed_rel})
    role_pins = {name: pins[role_paths[name]] for name in ['canonical','prepare_host','prepare_writer','build_host','build_writer','prepare_binder','build_binder']}
    utility_pins = {name: pins[role_paths[name]] for name in role_paths if name.endswith('.py')}
    check('common_consumer_required_7_role_fullpins_current', role_pins == delivery['qualified_role_Source_pins'] == author['qualified_role_Source_pins'] and len(role_pins) == 7)
    check('common_consumer_required_7_utility_fullpins_current', utility_pins == delivery['qualified_utility_Source_pins'] == author['qualified_utility_Source_pins'] and len(utility_pins) == 7)
    check('actual_author_stdout_all14_role_current_fullpins', author_stdout['role_Source_pins'] == {**role_pins, **utility_pins})
    check('runtime_journal_output_contract_unchanged_and_not_current_RSS', strict(data[fixed_rel])['build_memory_diagnostic_output_contract'] == strict(base[fixed_rel])['build_memory_diagnostic_output_contract'] and strict(data[fixed_rel])['build_memory_diagnostic_output_contract']['current_RSS_qualified'] is False)
    for rel, original_pin in pins.items():
        check('final_current_full_EOF_SHA_same7ID:' + rel, read(ROOT/rel)[1] == original_pin)
    check('final_current_manifest_and_directory7IDs_unchanged', read(ROOT/'MANIFEST.json')[1] == mp and {str(p.relative_to(ROOT)): identity(p.lstat()) for p in [ROOT, *sorted(ROOT.rglob('*'))] if stat.S_ISDIR(p.lstat().st_mode)} == dirs)
    check('final_ten_namespaces_still_fresh', all(not os.path.lexists(p) for p in fixed['namespaces'].values()))
    evidence = dict(schema='INDEPENDENT_SINGLE_PRE_GRAPH_GC_COMPLETE_SOURCE_REPLAY_EVIDENCE_V1', source_only=True, author_manifest_pin=mp, A5_parent_manifest_pin=pp, delivery_pin=delivery_pin, actual_author_seal_pin=delivery['actual_source_seal_tool_pin'], actual_author_postseal_pin=delivery['actual_full_postseal_tool_pin'], roles=replay, fixed_contract_pin=pins[fixed_rel], current_consumed_proof_pin=pins['COMPLETE_SOURCE_INVERSES.json'], all_actual_Source_and_small_META_full_EOF_pins=READS.copy(), canonical_pre_graph_gc_has_no_inactive_audit_or_numeric_argument_change=True, actual_runtime_RSS_build_or_science_proved=False)
    ep = write(OUT/'REPLAY_EVIDENCE.json', dump(evidence))
    report = dict(schema='INDEPENDENT_V25_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_REVIEW_V1', status='PASS_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION' if not BLOCKERS else 'FAIL_COMPLETE_BUILD_MEMORY_OBSERVATION_SOURCE_ONLY_UNREADY_NO_EXECUTION', source_only=True, reviewer_is_current_package_author=False, scope='Current sealed 113-file complete Source package only: independent full EOF/SHA/7ID, all 14-role counted complete byte/AST reversals to A5 and original parent, actual canonical consumed31 JSON proof, exact ten fresh namespaces and one17-byte pre-graph gc call. Earlier lineage reviews are not newly qualified.', check_count=len(CHECKS), checks=CHECKS, all_checks_typed_true=not BLOCKERS and all(type(x['passed']) is bool and x['passed'] is True for x in CHECKS), blockers=BLOCKERS, qualified_complete_Source_manifest_pin=mp, qualified_role_Source_pins=role_pins, qualified_utility_Source_pins=utility_pins, actual_consumed_complete_inverse_pin=pins['COMPLETE_SOURCE_INVERSES.json'], independent_replay_evidence_pin=ep, original_nine_caps=CAPS, source_packet_files=113, source_packet_directories=11, complete_Python_Source_AST_count=61, runtime_behavior_delta='One gc.collect() after original del specs,original_aliases and before verify_graph_enter and inactive audit; exact17 bytes', all_original_Q_helper3b_ENV_resource_guard_MRO_two_graph_EOF_owner_FLOAT_algorithms_retained=True, actual_candidate_binder_guard_helper_resource_API_PS_lsof_native_business_executed=False, actual_new_PREP_BUILD_whole_INPUT_native_or_science_qualification=None, actual_RSS_qualified=False, AAA_ABA_or_goal_qualified=False, project_old_frozen_D_E_or_result_modified=False)
    rp = write(OUT/'REVIEW.json', dump(report))
    write(OUT/'REVIEW_SOURCE.py', Path(__file__).read_bytes())
    for rel, path in [('EVIDENCE/current_author_manifest.byte_exact.json', ROOT/'MANIFEST.json'), ('EVIDENCE/current_author_DELIVERY.byte_exact.json', SIBLING/'DELIVERY.json'), ('EVIDENCE/current_author_seal.byte_exact.json', Path(delivery['actual_source_seal_tool_pin']['path'])), ('EVIDENCE/current_author_postseal.byte_exact.json', Path(delivery['actual_full_postseal_tool_pin']['path']))]:
        write(OUT/rel, read(path)[0])
    print(json.dumps(dict(package=str(OUT), review_pin=rp, replay_evidence_pin=ep, check_count=len(CHECKS), all_checks_typed_true=not BLOCKERS, blockers=BLOCKERS, source_only=True, actual_candidate_or_business_executed=False, no_Runtime_RSS_or_science_credit=True), sort_keys=True))
    return not BLOCKERS

if __name__ == '__main__':
    try:
        ok = run()
    except Exception as e:
        failure = dict(schema='INDEPENDENT_COMPLETE_SINGLE_PRE_GRAPH_GC_SOURCE_REVIEW_ACTUAL_FAILURE_V1', source_only=True, checks=CHECKS, blockers=BLOCKERS, error=repr(e), traceback=traceback.format_exc(), package=str(OUT), actual_candidate_or_business_executed=False)
        write(OUT/'ACTUAL_REVIEW_FAILURE.json', dump(failure))
        write(OUT/'FAILED_REVIEW_SOURCE.py', Path(__file__).read_bytes())
        print(json.dumps(dict(package=str(OUT), Source_review_failed=True, error=repr(e), source_only=True)))
        raise
    if not ok:
        raise SystemExit(1)
