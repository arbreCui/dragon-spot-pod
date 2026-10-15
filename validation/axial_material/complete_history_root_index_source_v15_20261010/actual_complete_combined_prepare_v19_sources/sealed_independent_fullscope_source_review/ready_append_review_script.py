"""Finite READY SOURCE binding audit. No project imports, APIs, or numeric reads."""
import ast
import copy
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).parent
OLD_DIR = Path('/private/tmp/axmat_v19_complete_prepare_caller_last_use_source_only_20261010')
READY_DIR = Path('/private/tmp/axmat_v19_complete_combined_READY_source_binding_20261010')
OLD = OLD_DIR / 'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.UNREADY.py'
READY = READY_DIR / 'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py'
BASE = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')
checks = {}
pins = {}

def check(name, condition):
    if type(condition) is not bool:
        raise TypeError(name)
    checks[name] = condition
    if not condition:
        raise ValueError(name)

def source_read(path, expected_sha=None, expected_bytes=None):
    path = Path(path)
    check('allowed_SOURCE_path:' + str(path), str(path).startswith('/private/tmp/') or path == BASE)
    before = path.stat()
    raw = path.read_bytes()
    after = path.stat()
    keys = ('st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
    before_id = [getattr(before, k) for k in keys]
    after_id = [getattr(after, k) for k in keys]
    check('full_SOURCE_EOF_7ID:' + str(path), before_id == after_id and len(raw) == before.st_size)
    sha = hashlib.sha256(raw).hexdigest()
    if expected_sha is not None:
        check('fixed_SOURCE_SHA:' + str(path), sha == expected_sha)
    if expected_bytes is not None:
        check('fixed_SOURCE_bytes:' + str(path), len(raw) == expected_bytes)
    pins[str(path)] = dict(path=str(path), sha256=sha, size_bytes=len(raw), before7ID=before_id, after7ID=after_id)
    return raw.decode('utf-8')

def obj(path, expected_sha=None, expected_bytes=None):
    return json.loads(source_read(path, expected_sha, expected_bytes))

def definitions(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

def assignments(tree):
    return {t.id: n for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}

def dump(node):
    return ast.dump(node, include_attributes=False)

result = dict(
    schema='AXMAT_V19_INDEPENDENT_READY_APPEND_SOURCE_REVIEW_V1',
    scope='TWO_READY_SOURCE_BINDINGS_TO_INDEPENDENTLY_REVIEWED_COMPLETE_585E_ONLY',
    project_module_imported=False, project_API_or_helper_called=False,
    business_executed=False, numeric_payload_read=False, ART_read_or_written=False,
    canonical_or_project_written=False, resource_helper_called=False,
    actual_RSS_pass_proved=False, source_line_RSS_cause_observed=False,
    future_PASS_predicted=False, blocking_findings=[])

try:
    original = source_read(OLD, '585e450c5eb5d8748ff7dedfab28ddcf6163d89ca90f3cdeb5c9095ac93eed50', 180475)
    ready = source_read(READY, '34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b', 180593)
    base = source_read(BASE, '5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240', 180102)
    first_proof = obj(OLD_DIR / 'source_inverse_proof.json', 'c3927b04791aa00115f1ad661f6113de6992d5a93f165a3c8ea58586dccd6595', 26128)
    proof = obj(READY_DIR / 'source_binding_inverse_proof.json', '87d8e493b207b6d21705a785dc4aa021845eb54c0b6b757ca0b47c52cf0156dc', 16847)
    old_manifest = obj(OLD_DIR / 'sealed_manifest.json', '29ebeca8b6f3cac996418f16525e17a4ee7e2adbb56b0647e496e9f5ac1b08ac')
    ready_manifest = obj(READY_DIR / 'sealed_manifest.json', '82b59edb22ac6255c6e869f3c05376af53a1dd981758b0983196f81d344a5848', 6109)
    for label, manifest, expected_count, directory in (
        ('585e', old_manifest, 5, OLD_DIR), ('34ef', ready_manifest, 7, READY_DIR)):
        check(label + '_sealed_member_count', manifest['member_count'] == len(manifest['members']) == expected_count)
        check(label + '_sealed_unique_members', len({m['path'] for m in manifest['members']}) == expected_count)
        for member in manifest['members']:
            check(label + '_sealed_member_in_own_source_package:' + member['path'], Path(member['path']).parent == directory)
            source_read(member['path'], member['sha256'], member['size_bytes'])
    prior = obj(OUT / 'REVIEW.json', 'ddd09a20482fd407e7ba0b245a5414a46929fadd0bf1f054e051f30c5aa1ea9d', 30182)
    check('actual_independent_complete_V19_body_review_163_all_typed_true', prior['status'] == 'SOURCE_PASS_COMPLETE_V19_UNREADY_LAST_USE_ONLY_NO_RUNTIME_CREDIT' and len(prior['checks']) == 163 and all(type(v) is bool and v is True for v in prior['checks'].values()))
    check('prior_complete_585e_to_5c4b_pins_exact', prior['candidate_sha256'] == pins[str(OLD)]['sha256'] and prior['parent_sha256'] == pins[str(BASE)]['sha256'] and prior['source_inverse_proof_sha256'] == pins[str(OLD_DIR / 'source_inverse_proof.json')]['sha256'])
    check('prior_complete_review_no_science_runtime_credit', all(type(v) is bool and v is False for v in prior['qualification'].values()) and prior['actual_RSS_pass_proved'] is False and prior['future_PASS_predicted'] is False)
    check('exactly_two_READY_source_binding_edits', len(proof['edits']) == 2 and all(e['occurrences'] == 1 for e in proof['edits']))
    check('READY_edit_kinds_doc_and_status_only', proof['edits'][0]['old'] == repr(ast.get_docstring(ast.parse(original))) and proof['edits'][1]['old'] == "DRAFT_STATUS = 'UNREADY_SOURCE_ONLY_V19_PREP_CALLER_LAST_USE_REVIEW_REQUIRED'" and proof['edits'][1]['new'] == "DRAFT_STATUS = 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'")
    restored = ready
    for i, edit in reversed(list(enumerate(proof['edits']))):
        check('READY_unique_inverse_hunk:' + str(i), restored.count(edit['new']) == 1)
        restored = restored.replace(edit['new'], edit['old'], 1)
    check('READY_full_text_inverse_to_reviewed_585e', restored == original)
    restored_base = restored
    for i, edit in reversed(list(enumerate(first_proof['edits']))):
        check('inherited_unique_inverse_hunk:' + str(i), restored_base.count(edit['new']) == edit['occurrences'])
        restored_base = restored_base.replace(edit['new'], edit['old'], edit['occurrences'])
    check('READY_full_text_inverse_to_actual_V18_5c4b', restored_base == base)
    ot, rt = ast.parse(original), ast.parse(ready)
    od, rd = definitions(ot), definitions(rt)
    check('all_70_definition_names_and_order_exact', list(od) == list(rd) and len(od) == 70)
    for name in od:
        check('definition_byteexact:' + name, ast.get_source_segment(original, od[name]) == ast.get_source_segment(ready, rd[name]))
    oa, ra = assignments(ot), assignments(rt)
    check('all_global_assignment_names_order_exact', list(oa) == list(ra))
    for name in oa:
        if name != 'DRAFT_STATUS':
            check('other_global_assignment_byteexact:' + name, ast.get_source_segment(original, oa[name]) == ast.get_source_segment(ready, ra[name]))
    normalized = copy.deepcopy(rt)
    check('first_statement_literal_docstring_only', isinstance(normalized.body[0], ast.Expr) and isinstance(normalized.body[0].value, ast.Constant) and isinstance(normalized.body[0].value.value, str))
    normalized.body[0] = copy.deepcopy(ot.body[0])
    for i, node in enumerate(normalized.body):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'DRAFT_STATUS' for t in node.targets):
            normalized.body[i] = copy.deepcopy(oa['DRAFT_STATUS'])
    check('entire_module_AST_exact_after_only_doc_status_normalization', dump(normalized) == dump(ot))
    future = ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA', 'FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA', 'FUTURE_ACTUAL_COMBINED_SEAL_SHA', 'FUTURE_ACTUAL_COMBINED_TERMINAL_SHA', 'FUTURE_ACTUAL_COMBINED_RUNTIME_SHA', 'FUTURE_ACTUAL_NATIVE_TERMINAL_SHA')
    check('all_six_future_business_native_pins_None', all(ast.literal_eval(ra[k].value) is None for k in future))
    require = rd['require_ready']
    expected = 'READY_REVIEWED_V19_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'
    status = ast.literal_eval(ra['DRAFT_STATUS'].value)
    check('exact_READY_literal_matches_unchanged_require_ready_guard', status == expected and any(isinstance(n, ast.Constant) and n.value == expected for n in ast.walk(require)))
    factory = ra['FORMAL_FACTORY'].value
    check('uninstalled_TMP_candidate_retains_FORMAL_FACTORY_identity_guard', '__file__' in ast.get_source_segment(ready, require) and 'FORMAL_FACTORY' in ast.get_source_segment(ready, require) and isinstance(factory, ast.BinOp) and isinstance(factory.left, ast.Name) and factory.left.id == 'ROOT' and isinstance(factory.op, ast.Div) and isinstance(factory.right, ast.Constant) and factory.right.value == 'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v19.py' and str(READY) != '/Users/wen/spot/' + factory.right.value)
    check('bcd_d490_pure_metadata_bindings_unchanged', dump(oa['INPUT_HELPERS']) == dump(ra['INPUT_HELPERS']) and dump(oa['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']) == dump(ra['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']))
    check('author_does_not_borrow_V18_as_independent_V19_review', proof['independent_V19_source_review'] is None and proof['independent_V19_source_review_completed'] is False and ready_manifest['final_independent_V19_review_complete'] is False)
    doc = ast.get_docstring(rt)
    check('truthful_READY_doc_scope_requires_review_before_installation', 'final independent SOURCE review before installation' in doc and 'Actual V18 PREP failed above512 MiB' in doc and 'has not executed any business or scientific validation' in doc and 'all six future combined/native success pins remain None' in doc)
    check('READY_proof_runtime_science_credit_false', proof['new_combined_prepare_or_build_or_whole_INPUT_or_native_or_AAA_or_ABA_credit'] is False and ready_manifest['new_RSS_or_native_or_AAA_or_ABA_credit'] is False)
    for path, pin in list(pins.items()):
        source_read(path, pin['sha256'], pin['size_bytes'])
    result.update(status='SOURCE_PASS_COMPLETE_V19_READY_BINDING_ONLY_NO_RUNTIME_CREDIT', checks=checks, source_pins=pins, candidate_sha256=pins[str(READY)]['sha256'], candidate_bytes=180593, independent_complete_body_review_sha256=pins[str(OUT / 'REVIEW.json')]['sha256'], candidate_to_585e_inverse_exact=True, candidate_to_5c4b_inverse_exact=True, all_70_definitions_byteexact_to_independently_reviewed_585e=True, all_other_module_globals_and_AST_exact=True, six_future_business_native_success_pins_None=True, all_original_scope_caps_two_phases_fullEOF_closure_trace_aliases_predicates_kept=True, qualification=dict(complete_PREP_pass_obtained=False, complete_build_pass_obtained=False, whole_INPUT_admitted=False, native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False, physical_balance_qualified=False, goal_complete=False), remaining_requirements=['Independent PREP-host retarget review remains separate.', 'Fresh actual complete PREP under original caps required; no observed V19 RSS success or source-line V18 failure attribution.'])
except BaseException as error:
    result.update(status='SOURCE_REVIEW_BLOCKED_BY_DEFINITE_PROOF_FAILURE', error=repr(error), blocking_findings=[repr(error)], checks=checks, source_pins=pins)

path = OUT / 'READY_APPEND_REVIEW.json'
with path.open('x') as f:
    json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
    f.write('\n')
report = '完整 V19 SOURCE 独立复核附加 READY 绑定：' + result['status'] + '\n'
report += '585e 完整调用方 last-use 的163项独立源码检查已完成；READY34ef /180593B仅改 docstring 与 DRAFT_STATUS，两处逆变换逐字回585e，再逐字回V18实际5c4b。全部70定义、其他模块全局和AST保持；现有完整输入相位修正、全部原两阶段fullEOF/closure/trace/alias/条件及原512/600等上限、bcd/d490和6futureNone保持。\n'
report += '仅 SOURCE_PASS，无安装、project/helper/API/业务/数值执行、numeric payload或ART读取/写入、资源检查。独立PREP host retarget仍由另一审查负责；未证明V19 RSS通过，未观测V18失败的具体源码行原因。AAA/ABA/native/物理平衡及目标完成资格均false。\n'
if result['blocking_findings']:
    report += '明确阻碍：' + repr(result['blocking_findings']) + '\n'
with (OUT / 'READY_APPEND_REPORT.txt').open('x') as f:
    f.write(report)
raw = path.read_bytes()
print(json.dumps(dict(status=result['status'], directory=str(OUT), ready_append_review_sha256=hashlib.sha256(raw).hexdigest(), ready_append_review_bytes=len(raw), source_checks=len(checks), candidate_sha256='34efcc340b87257929e9d4cb06631455549327436d2bbdc5561639b6535e140b', business_helper_API_called=False, numeric_payload_read=False, ART_read_or_written=False, RSS_pass_claimed=False), indent=2))
if result['blocking_findings']:
    raise SystemExit(1)
