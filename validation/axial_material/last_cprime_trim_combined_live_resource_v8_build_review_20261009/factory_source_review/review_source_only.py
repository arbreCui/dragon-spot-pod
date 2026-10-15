from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import stat

OUT = Path('/private/tmp/spot_f8_final_factory_source_independent_review_20261009')
OUT.mkdir(exist_ok=True)
ROOT = Path('/Users/wen/spot')
A = ROOT / 'validation/axial_material'
ART = ROOT / 'validation/artifacts'
BASENAME = 'prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py'
DRAFT = Path('/private/tmp/axmat-trim-v8-wire-private-predicate-factory-source-draft-20261009')
READY = Path('/private/tmp/axmat-trim-v8-ready-source-admission-20261009')
PARENT = A / BASENAME.replace('_v8.py', '_v7.py')
HELPER_DRAFT = Path('/private/tmp/axmat-requirements-varint-wire-compact-phase-source-draft-20261009/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py')
HELPER = A / HELPER_DRAFT.name
PRIVATE = A / 'combined_runtime_current_predicates_private_declaration_lifetimes_20261009.py'
HELPER_REVIEW = Path('/private/tmp/axmat_requirements_varint_wire_final_independent_review_20261009/independent_final_source_and_tiny_review.json')
PINS = {}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def read_pin(path, expected=None):
    path = Path(path)
    assert path.is_absolute() and '..' not in path.parts
    for item in [*reversed(path.parents), path]:
        s = item.lstat()
        assert not stat.S_ISLNK(s.st_mode), str(item)
    first = path.lstat()
    assert stat.S_ISREG(first.st_mode), str(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        assert identity(os.fstat(fd)) == identity(first)
        blocks = []
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block:
                break
            blocks.append(block)
        raw = b''.join(blocks)
        assert identity(os.fstat(fd)) == identity(first)
    finally:
        os.close(fd)
    assert identity(path.lstat()) == identity(first)
    actual = sha(raw)
    if expected is not None:
        assert actual == expected, (str(path), actual, expected)
    PINS[str(path)] = dict(path=str(path), bytes=len(raw), sha256=actual, identity=identity(first),
                          full_fresh_SHA=True, stable_identity_before_after=True)
    return raw

def json_pin(path, expected=None):
    return json.loads(read_pin(path, expected))

def parse(raw):
    source = raw.decode('utf-8')
    return source, ast.parse(source)

def source_segment(source, node):
    return ast.get_source_segment(source, node)

def assignments(tree):
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            names = [n.id for n in ast.walk(node.targets[0]) if isinstance(n, ast.Name)]
            result[','.join(names)] = node
    return result

def functions(source, tree):
    return {n.name: dict(start=n.lineno, end=n.end_lineno, source=source_segment(source, n))
            for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

def replacement(label, old, new, current):
    assert old != new
    assert current.count(new) == 1, (label, 'new occurrences', current.count(new))
    return dict(label=label, old=old, new=new, old_sha256=sha(old.encode()), new_sha256=sha(new.encode()))

parent_raw = read_pin(PARENT, '45783d9920a53ca517f28abbff9071e81cd29b0ef87336f45216aa86d8e4bc5a')
draft_raw = read_pin(DRAFT / BASENAME, '82ee0e5721edfcc8d524b6b0773b992eeddfdc5f008fee10ac80b1bc6734ed09')
ready_raw = read_pin(READY / BASENAME, '4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4')
assert read_pin(READY / 'initial_source_only_mother.py.txt') == draft_raw
ps, pt = parse(parent_raw)
ds, dt = parse(draft_raw)
rs, rt = parse(ready_raw)
pa, da, ra = assignments(pt), assignments(dt), assignments(rt)
pf, df, rf = functions(ps, pt), functions(ds, dt), functions(rs, rt)
assert list(pf) == list(df) == list(rf) and len(pf) == 65
changed = [name for name in pf if pf[name]['source'] != df[name]['source']]
assert changed == ['graph_input_bindings', 'create_complete_input_graph']
assert all(df[name]['source'] == rf[name]['source'] for name in df)

# Build independent replacement regions from the actual AST and explicit
# allowed transitions, without executing or importing either factory.
patches = [replacement('module_docstring', source_segment(ps, pt.body[0]),
                       source_segment(ds, dt.body[0]), ds)]
for name in ['SOURCE', 'OUT', 'TERMINAL', 'FAMILY', 'DRAFT_STATUS', 'PREFIX', 'FORMAL_FACTORY']:
    old = source_segment(ps, pa[name]); new = source_segment(ds, da[name])
    if name in ['SOURCE', 'OUT', 'TERMINAL']:
        assert new == old.replace('-v7-', '-v8-')
    elif name == 'FAMILY':
        assert new == old.replace('_V7', '_V8')
    elif name == 'DRAFT_STATUS':
        assert ast.literal_eval(da[name].value) == 'UNREADY_V8_SOURCE_ONLY_HELPER_AND_FACTORY_REVIEWS_PENDING'
        assert ast.literal_eval(pa[name].value) == 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY'
    elif name == 'PREFIX':
        assert new == old.replace('_V7', '_V8')
    elif name == 'FORMAL_FACTORY':
        assert new == old.replace('_v7.py', '_v8.py')
    patches.append(replacement('assignment:' + name, old, new, ds))

old_helper_rows = source_segment(ps, pa['INPUT_HELPERS']).splitlines()
new_helper_rows = source_segment(ds, da['INPUT_HELPERS']).splitlines()
assert len(old_helper_rows) == len(new_helper_rows)
helper_rows = []
for label, filename, expected_sha in [
    ('graph', HELPER.name, '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'),
    ('current', PRIVATE.name, '2d9bf60b5a27d8cc32de5cc231e20b6caf65fa85f8c66d770124e0a0f1809b8f')]:
    old = next(row for row in old_helper_rows if row.lstrip().startswith(repr(label) + ':'))
    new = next(row for row in new_helper_rows if row.lstrip().startswith(repr(label) + ':'))
    assert new == " '" + label + "': (ROOT/'validation/axial_material/" + filename + "','" + expected_sha + "'),"
    patches.append(replacement('helper_binding:' + label, old, new, ds))
    helper_rows.append(dict(name=label, old=old, new=new))
assert [i for i, pair in enumerate(zip(old_helper_rows, new_helper_rows)) if pair[0] != pair[1]] == [1, 3]

for label, old, new in [
    ('full_saved_requirement_gate_to_strict_accessor', "table=graph['requirements'];g._validate_requirement_table(table)", "table=graph['requirements']"),
    ('full_saved_rows_to_full_strict_decoded_rows', "for row in table['rows']:", "for row in g.iter_graph_requirement_rows(graph):"),
    ('full_graph_creator_to_lossless_wire_creator', "graph=g.create_graph(typed_snapshot=", "graph=g.create_wire_graph(typed_snapshot=")]:
    patches.append(replacement(label, old, new, ds))
assert len(patches) == 13
inverse = ds
for patch in reversed(patches):
    assert inverse.count(patch['new']) == 1, patch['label']
    inverse = inverse.replace(patch['new'], patch['old'], 1)
assert inverse.encode() == parent_raw
forward = ps
for patch in patches:
    assert forward.count(patch['old']) == 1, patch['label']
    forward = forward.replace(patch['old'], patch['new'], 1)
assert forward.encode() == draft_raw

ready_patches = [
    replacement('module_source_admission_explanation', source_segment(ds, dt.body[0]), source_segment(rs, rt.body[0]), rs),
    replacement('reviewed_source_execution_status_only', source_segment(ds, da['DRAFT_STATUS']), source_segment(rs, ra['DRAFT_STATUS']), rs)]
assert source_segment(rs, ra['DRAFT_STATUS']) == source_segment(ps, pa['DRAFT_STATUS'])
ready_inverse = rs
for patch in reversed(ready_patches):
    assert ready_inverse.count(patch['new']) == 1
    ready_inverse = ready_inverse.replace(patch['new'], patch['old'], 1)
assert ready_inverse.encode() == draft_raw
ready_forward = ds
for patch in ready_patches:
    assert ready_forward.count(patch['old']) == 1
    ready_forward = ready_forward.replace(patch['old'], patch['new'], 1)
assert ready_forward.encode() == ready_raw

# All executable differences to F7 consist of six family identities, two
# helper pins, and the three checked statements; final status equals F7.
final_patches = [dict(p) for p in patches if p['label'] != 'assignment:DRAFT_STATUS']
final_patches[0] = replacement('module_docstring', source_segment(ps, pt.body[0]), source_segment(rs, rt.body[0]), rs)
final_inverse = rs
for patch in reversed(final_patches):
    assert final_inverse.count(patch['new']) == 1
    final_inverse = final_inverse.replace(patch['new'], patch['old'], 1)
assert final_inverse.encode() == parent_raw and len(final_patches) == 12

assert [ast.dump(n, include_attributes=False) for n in pt.body if isinstance(n, (ast.Import, ast.ImportFrom))] == [ast.dump(n, include_attributes=False) for n in rt.body if isinstance(n, (ast.Import, ast.ImportFrom))]
numeric = lambda tree: [(type(n.value).__name__, repr(n.value)) for n in ast.walk(tree) if isinstance(n, ast.Constant) and type(n.value) in (int, float, complex)]
assert numeric(pt) == numeric(dt) == numeric(rt)
assert pf['require_ready']['source'] == df['require_ready']['source'] == rf['require_ready']['source']
assert "if DRAFT_STATUS != 'READY_REVIEWED_TRIM_COMPONENT_INPUT_REUSE_FORMAL_FACTORY':" in rf['require_ready']['source']
assert "if Path(__file__).absolute()!=FORMAL_FACTORY:" in rf['require_ready']['source']
assert "if __name__=='__main__':\n    require_ready()" in rs
assert rs[rs.index("if __name__=='__main__':"):] == ps[ps.index("if __name__=='__main__':"):]

helper_raw = read_pin(HELPER_DRAFT, '1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643')
assert read_pin(HELPER, sha(helper_raw)) == helper_raw
private_raw = read_pin(PRIVATE, '2d9bf60b5a27d8cc32de5cc231e20b6caf65fa85f8c66d770124e0a0f1809b8f')
hs, ht = parse(helper_raw); hf = functions(hs, ht)
final_helper_review = json_pin(HELPER_REVIEW, '32d678d60900aa274a92f24abac1fc0529fa114f48df54eee8cafe2fd602154b')
assert final_helper_review['status'] == 'PASS'
assert final_helper_review['candidate']['sha256'] == sha(helper_raw)
for flag in ['AAA_accuracy_qualified', 'ABA_admitted', 'actual_512_native_RSS_proved', 'ART_or_formal_source_written', 'business_API_constructor_current_big_graph_large_union_PREP_RUN_native_executed']:
    assert final_helper_review[flag] is False
for group, expected_cases in [('independent_actual_tiny', 56), ('independent_codec_boundary_tiny', 24)]:
    info = final_helper_review[group]
    assert info['actual_exit_code'] == 0 and info['actual_session_closed'] is True and info['case_count'] == expected_cases
    case_report = json_pin(info['report']['path'], info['report']['sha256'])
    assert case_report['case_count'] == len(case_report['results']) == expected_cases
    assert all(row['PASS'] is True for row in case_report['results'])
    receipt = json_pin(info['tool_receipt']['path'], info['tool_receipt']['sha256'])
    assert receipt['actual_tool_return']['exit_code'] == 0 and receipt['session_closed'] is True and receipt['actual_terminal_return_observed'] is True
    stdout = json.loads(receipt['actual_tool_return']['output'])
    assert stdout['sha256'] == info['report']['sha256'] and stdout['case_count'] == expected_cases
    for field in ['copied_56_suite', 'suite', 'suite_inverse']:
        if field in info:
            read_pin(info[field]['path'], info[field]['sha256'])

handoff = json_pin(DRAFT / 'STOPPED_handoff.json', '329622bedc0d5c7870c0e10270e79d139f7940bac2612cb6d8f4dcef5fe6edd8')
assert len(handoff['future_actual_bindings']) == 17 and all(v is None for v in handoff['future_actual_bindings'].values())
transition = json_pin(READY / 'source_admission_transition.json', 'e4b59c5e13bc5c7fa212466a57f7c5f777e68407b7508451bf7e66004638118b')
assert transition['candidate_sha256'] == sha(ready_raw) and transition['source_only_mother_sha256'] == sha(draft_raw)
for name in ['actual_PREP', 'actual_RUN', 'actual_runtime_seal', 'actual_standard_INPUT_return', 'AAA', 'ABA']:
    assert transition[name] is None
author_audit = json_pin(DRAFT / 'source_audit.json', 'a3fa3c0e6febba94a960330b4b428df8c378bb32c8264d6afedee47da380e6e8')
author_inverse = json_pin(DRAFT / 'source_inverse.json', 'c203b0af4563fd569b275729745ad6e1675cde2b9d94c7bc425e6dcb149c1625')
assert author_audit['changed_function_count'] == 2 and author_audit['unchanged_function_count'] == 63
read_pin(DRAFT / 'REPORT.txt', 'f7faddcfe4dceb55224809379baf97a50282354a6c684154a9ddb5093891dd2f')
read_pin(READY / 'FINAL_READY_TRANSITION.diff', 'a2251408398698dcf0eb225192833eb86c3dc8ca0acb6479886b22020a753875')

original_specs = json_pin(A / 'combined_runtime_complete_historical_input_specs_20261007.json', '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
bodies = original_specs['metadata']['historical_actual_components']
assert set(bodies) == {'capture', 'capture_scope_is_original_operator_only', 'combined_runtime_RSS_not_proved', 'dedup', 'mathematical_controls_inherited_not_newly_executed', 'original92', 'physical'}
body_digest = sha(json.dumps(bodies, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode())
assert body_digest == 'a0b0445e79f91f5d3767ee57719937a5188608f6a22f77d62b17c5036950e130'
trim_original = json_pin(A / 'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json', 'fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
v7_source = ART / 'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009'
trim_v7 = json_pin(v7_source / 'trim_component_admission_INPUT.json', 'a4662b853831357c299de0c28d1d19e2a869f81c6308081f6fa1d7833fd797bb')
assert trim_original == trim_v7
assert source_segment(ps, pa['BODY_BINDING']) == source_segment(rs, ra['BODY_BINDING'])
assert source_segment(ps, pa['INPUT_SPECS']) == source_segment(rs, ra['INPUT_SPECS'])
assert source_segment(ps, pa['INPUT_SPECS_SHA']) == source_segment(rs, ra['INPUT_SPECS_SHA'])
assert "if bodies!=expected:raise ValueError('entire historical seven-key body differs; no field filtering')" in rf['actual_components']['source']
assert "value=trim_factory().production_admission(TRIM_SEAL_SHA,str(TRIM_TERMINAL/'terminal_return.json'),TRIM_TERMINAL_SHA)" in rf['record_actual_trim_component']['source']

hist = json_pin(ART / 'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json', 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
v7_out = ART / 'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009'
v7 = json_pin(v7_out / 'declaration.json', 'df56e805ff04d9ec5cffc3b877f6054d9d68de849407c7ebee45fdc1175d7e52')
prediction = json_pin(DRAFT / 'dynamic_resource_root_source_prediction.json', '3a875b656a3d3c984fe19c092395a9fb8572f14e79827cc98f5cd843cc601ef8')
current_roots = sorted(str(p) for p in ART.glob('axial-material-*'))
assert len(current_roots) == 225 and current_roots == prediction['actual_current_direct_glob']
assert current_roots == sorted(v7['resource_roots'])
assert set(hist['resource_roots']) <= set(current_roots) and len(hist['resource_roots']) == 170
new_roots = handoff['new_ART_roots']
assert len(new_roots) == 3 and new_roots == prediction['three_new_roots']
assert sorted(set(current_roots) | set(new_roots)) == prediction['known_direct_glob_plus_new_roots']
assert len(prediction['known_direct_glob_plus_new_roots']) == 228
assert not any(os.path.lexists(p) for p in new_roots)
assert prediction['directory_or_trace_filter_added'] is False
assert prediction['complete_effective_declared_roots'] is None
assert all(prediction[field] is None for field in ['actual_live_resource_bytes', 'actual_wire_graph_bytes', 'actual_wire_graph_within_original_64MiB_cap'])
root_identities = []
for p in current_roots:
    st = Path(p).lstat()
    assert stat.S_ISDIR(st.st_mode) and not stat.S_ISLNK(st.st_mode)
    root_identities.append(dict(path=p, identity=identity(st)))
assert "declared=set(historical_roots)|{str(SOURCE),str(OUT),str(TERMINAL)}" in rf['prepare_build']['source']
assert "b.history_roots(sorted(declared),ART)" in rf['prepare_build']['source']
assert "live_resource_roots=roots" in rf['create_complete_input_graph']['source']
assert "graph['live_resource_roots']!=sorted(d['resource_roots'])" in rf['complete_input_phase']['source']

read_pin(A / 'prepare_qualified_AB_rank1_cache_production.py', '92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a')
read_pin(A / 'qualify_refined_AAA_layered_full.py', '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6')
read_pin(ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py', '38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128')
read_pin(v7_out / 'runtime/run_bounded_dragon.py', 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
failed_v7 = json_pin(A / 'last_cprime_trim_combined_live_resource_v7_build_review_20261009/independent_actual_failure_review.json', '33bc79cf6c604c1f51efa60eb79e138fac718ec6bb1903dd944d65fe8995da00')
assert failed_v7['actual_tool_terminal']['exit_code'] == 1
assert failed_v7['combined_runtime_native_RSS_proved'] is False and failed_v7['AAA_accuracy_qualified'] is False and failed_v7['ABA_admitted'] is False
assert failed_v7['original_cap_MiB'] == 512
read_pin(failed_v7['actual_failed_Root_receipt']['path'], failed_v7['actual_failed_Root_receipt']['sha256'])

# Explicit source assertions supplement the full inverse for cross-schema
# wiring and external-byte/content/decoded-semantic SHA separation.
checks = {
    'explicit_wire_producer': 'graph=g.create_wire_graph(typed_snapshot=' in rf['create_complete_input_graph']['source'],
    'full_graph_creation_still_retained': 'return encode_graph_wire(create_graph(**kwargs))' in hf['create_wire_graph']['source'],
    'producer_full_JSON_clone_retained': 'graph = _json_clone(graph)' in hf['encode_graph_wire']['source'],
    'all_saved_rows_strict_accessor': 'for row in g.iter_graph_requirement_rows(graph):' in rf['graph_input_bindings']['source'],
    'accessor_full_wire_table_validation': '_validate_wire_requirement_table(table)' in hf['iter_graph_requirement_rows']['source'],
    'accessor_wire_content_digest': '_sha(graph.get("content_sha256")) == _content_digest(graph)' in hf['iter_graph_requirement_rows']['source'],
    'accessor_decoded_semantic_digest': '_wire_semantic_content_digest(graph) == encoding["decoded_content_sha256"]' in hf['iter_graph_requirement_rows']['source'],
    'accessor_full_five_column_decoding': 'yield from _decoded_requirement_rows(table["rows"], limits)' in hf['iter_graph_requirement_rows']['source'],
    'factory_raw_external_byte_SHA': "binding=dict(path=str(OUT/GRAPH_NAME),sha256=digest(OUT/GRAPH_NAME),content_sha256=graph['content_sha256'],scope='COMPLETE_HISTORICAL_INPUT_ONLY')" in rf['create_complete_input_graph']['source'],
    'fresh_verify_with_external_stored_SHA': "verified=g.verify_graph(d['input_graph']['path'],expected_sha256=d['input_graph']['sha256'],phase=phase)" in rf['complete_input_phase']['source'],
    'fresh_verify_encoded_content_matches_declaration': "verified['graph_content_sha256']!=d['input_graph']['content_sha256']" in rf['complete_input_phase']['source'],
    'Root_PREP_complete_binding_equal': "e['input_graph']!=d['input_graph']" in rf['prepare_terminal_admission']['source'],
    'API_complete_binding_unchanged': "historical_input_graph=d['input_graph']" in rf['production_admission']['source'],
    'API_owns_external_stored_graph_SHA': "own(d['input_graph']['path'],d['input_graph']['sha256'])" in rf['production_admission']['source'],
    'full_expected_SHA_union_enforced': "or files!=actual:" in rf['graph_input_bindings']['source'],
    'full_literal_alias_union_enforced': "if len(aliases)!=len(graph['aliases'])" in rf['graph_input_bindings']['source'],
    'full_declaration_SHA_alias_actual_path_union_enforced': "if d['files']!=files or d['complete_input_aliases']!=complete_aliases or paths!=set(files):" in rf['complete_input_phase']['source'],
    'consumer_scope_none_creation_and_verification': "if graph['consumer_scope']is not None:" in rf['create_complete_input_graph']['source'] and "if verified['consumer_scope']is not None" in rf['complete_input_phase']['source'],
    'strict_JSON_64MiB_original_cap': 'MAX_JSON_BYTES = 64 * 1024 * 1024' in hs,
    'full_raw_every_input_fresh_once': "or any(x['attempt_count']!=1 for x in regular)" in rf['complete_input_phase']['source'],
    'genuine_MRO_guard': 'full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)' in rf['modules']['source'],
    'four_original_tail_fields': ast.literal_eval(ra['TAIL_FIELDS'].value) == ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources'),
    'five_stages_still_exact': "return ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']" in rf['stage_labels']['source'],
    'one_true_trim_3arg_API_call_only_in_PREP_source': rs.count("value=trim_factory().production_admission(TRIM_SEAL_SHA,str(TRIM_TERMINAL/'terminal_return.json'),TRIM_TERMINAL_SHA)") == 1,
    'legacy_failed_V7_not_rerun_or_recredited': 'v7 without retrying its failed actual input-audit RUN' in ast.get_docstring(rt),
}
assert all(checks.values()), [k for k, v in checks.items() if not v]

# Freeze complete inverse witnesses and all full declaration/function source
# excerpts in TMP only; no candidate code is evaluated.
(OUT / 'reconstructed_F7_from_initial.py.txt').write_bytes(inverse.encode())
(OUT / 'reconstructed_initial_from_ready.py.txt').write_bytes(ready_inverse.encode())
(OUT / 'reconstructed_F7_from_ready.py.txt').write_bytes(final_inverse.encode())
source_evidence = dict(
    independent_13_initial_replacements=patches,
    independent_2_ready_transition_replacements=ready_patches,
    independent_12_final_to_F7_replacements=final_patches,
    all65_function_sources={name: dict(parent=pf[name], initial=df[name], ready=rf[name]) for name in pf},
    wire_helper_full_functions={name: hf[name] for name in ['_validate_wire_requirement_table', '_wire_semantic_content_digest', 'encode_graph_wire', 'create_wire_graph', 'iter_graph_requirement_rows', 'verify_graph']})
source_raw = (json.dumps(source_evidence, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
(OUT / 'complete_source_inverse_evidence.json').write_bytes(source_raw)

formal_target = A / BASENAME
assert not os.path.lexists(formal_target), 'review source candidate before any formal factory installation'
for path, info in PINS.items():
    assert identity(Path(path).lstat()) == info['identity'], ('end-of-review identity changed', path)
assert current_roots == sorted(str(p) for p in ART.glob('axial-material-*'))

report = dict(
    schema='AXMAT_F8_FACTORY_FINAL_INDEPENDENT_WHOLE_SOURCE_AND_READY_TRANSITION_REVIEW_V1',
    status='PASS', scope='SOURCE_CONTRACT_ONLY_READY_CANDIDATE_FOR_EXACT_FORMAL_COPY_AND_FUTURE_ACTUAL_PREP',
    reviewed_candidate=PINS[str(READY / BASENAME)], initial_STOPPED_candidate=PINS[str(DRAFT / BASENAME)], parent_F7=PINS[str(PARENT)],
    initial_to_parent_inverse=dict(regions=13, whole_source_bytes_equal=True, independently_constructed=True),
    ready_to_initial_inverse=dict(regions=2, whole_source_bytes_equal=True, all65_function_sources_exact=True),
    ready_to_parent_inverse=dict(regions=12, whole_source_bytes_equal=True, final_DRAFT_STATUS_equal_parent=True),
    functions=dict(count=65, unchanged_vs_parent=63, changed_vs_parent=changed,
                   changed_functions_only_three_allowed_statements=True, all65_ready_equal_initial=True,
                   catalog=[dict(name=name, parent_sha256=sha(pf[name]['source'].encode()), ready_sha256=sha(rf[name]['source'].encode()),
                                 exact_parent=pf[name]['source']==rf[name]['source']) for name in pf]),
    all_original_imports_CLI_math_numeric_constants_and_other_source_bytes_preserved=True,
    source_gate=dict(initial_UNREADY_actually_blocks_CLI=True, final_READY_equals_original_source_gate=True,
                     TMP_file_still_refused_by_unchanged_formal_path_gate=True, single_thread_and_nonoptimized_guards_unchanged=True,
                     prepare_build_run_build_and_main_require_ready=True,
                     correction='Initial suggestion that DRAFT_STATUS was merely an unused marker was wrong. require_ready checks it; this final reviewed transition restores only the original formal-only source execution flag.',
                     formal_factory_absent_at_review_end=True, source_READY_does_not_mean_business_RUNTIME_success=True),
    helper_final_review=PINS[str(HELPER_REVIEW)], graph_formal_exact_copy=PINS[str(HELPER)],
    private_formal_exact_source=PINS[str(PRIVATE)],
    helper_tiny_evidence=dict(previous_independent_cases=56, previous_independent_codec_boundary_cases=24,
                              full_reports_receipts_and_case_success_fresh_checked=True, rerun_in_this_review=False,
                              tiny_has_no_RSS_native_scientific_or_actual_production_graph_credit=True),
    helper_generation_metadata_note='Author initial handoff/source-audit still say helper final review pending because they predate the unchanged-SHA final PASS. Their bytes are preserved; this review freshly pins the later independent PASS and formal exact copy.',
    integration_checks=checks,
    three_digests=dict(external_actual_stored_wire_JSON_SHA='declaration.input_graph.sha256; exact fresh verify/Root PREP/seal inventory/API descriptor binding',
                       encoded_wire_content_SHA='graph.content_sha256 == declaration.input_graph.content_sha256 == verify_graph result graph_content_sha256',
                       decoded_full_semantic_SHA='graph.wire_encoding.decoded_content_sha256; internally checked by strict accessor and fresh verifier, protected by externally pinned stored graph bytes',
                       decoded_semantic_SHA_not_substituted_for_external_SHA=True,
                       no_new_actual_digest_or_graph_size_measured=True,
                       new_F8_semantic_SHA_need_not_equal_frozen_V7_graph_SHA='F8 genuinely changes source/helper identities and retains all old owners/roots; old graph SHA remains frozen, never rewritten.'),
    whole_INPUT=dict(original_specs=PINS[str(A / 'combined_runtime_complete_historical_input_specs_20261007.json')],
                     original_seven_key_names=sorted(bodies), whole_seven_body_canonical_digest=body_digest,
                     seven_key_full_dict_and_original_component_contract_sources_unchanged=True,
                     original_complete_trim_admission=PINS[str(A / 'last_cprime_trim_build_review_20261008/actual_complete_production_admission.json')],
                     frozen_V7_complete_trim_return=PINS[str(v7_source / 'trim_component_admission_INPUT.json')],
                     full_ordinary_JSON_dict_equal=True, original_raw_files_not_rewritten=True,
                     new_trim_3arg_PREP_API_still_required_not_executed=True,
                     material_seed_or_cold_dependencies_not_removed_or_INPUT_scope_pruned_by_review=True),
    resource_roots=dict(original_historical_declared_roots=170, current_unfiltered_axial_material_glob_count=225,
                        frozen_V7_roots_equal_current225=True, all225_ordinary_directories_present=True,
                        new3_roots_absent=True, known_direct_glob_plus_new3_prediction=228,
                        every_old_V7_family_root_including_old3_preserved=True,
                        source_unchanged_historical_declared_set_union_and_dynamic_history_roots=True,
                        scope_is_directory_contract_not_execution_trace=True,
                        actual_PREP_complete_effective_roots_graph_bytes_resource_bytes=None,
                        current_root_identity_records=root_identities),
    original_budgets=dict(total_wall_seconds=1800, stage_wall_seconds=600, own_RSS_MiB=512,
                         SOURCE_OUT_reserve_bytes=2*2**30, artifact_history_cap_bytes=96*2**30,
                         filesystem_free_floor_bytes=8*2**30, threads=1, numeric_children_at_once=1, retries=0,
                         stored_graph_JSON_cap_bytes=64*1024**2, genuine_MRO_705_38de_bc4_pins_fresh=True,
                         producer_original_full_create_and_clone_retained_no_memory_saving_claim=True),
    frozen_V7_failure=dict(review=PINS[str(A / 'last_cprime_trim_combined_live_resource_v7_build_review_20261009/independent_actual_failure_review.json')],
                           actual_Root_receipt=failed_v7['actual_failed_Root_receipt'], true_actual_exit_code=1,
                           failed_watch=failed_v7['failed_final_watch'], original_cap_MiB=512,
                           no_new_source_or_tiny_cause_line_RSS_native_or_science_credit=True),
    future_actual_bindings=handoff['future_actual_bindings'], all17_future_actual_bindings_still_None=True,
    current_source_transition_actual_PREP_RUN_seal_API_AAA_ABA_fields_None=True,
    actual_PREP_RUN_API_constructor_native_execution=False, actual_graph_creation_or_large_union_business_verification=False,
    formal_or_ART_written=False, project_source_imported_or_executed=False, scientific_qualification=False,
    combined_runtime_native_RSS_proved=False, AAA_accuracy_qualified=False, ABA_admitted=False,
    requirement_after_this_source_PASS='Root may exact-copy only final 4fc0dc source to its declared formal path, preserving reviewed helper pins. Actual new fresh complete PREP and immutable Root exit receipt, then original five-stage/four-tail RUN and full bounded standard INPUT/API plus namespace receipts remain separate required evidence; no F8 actual credit is granted here.',
    limits=['This independent review parses source AST and original data documents only; it does not execute/import business source, any API, constructor, PREP/RUN, helper verification, native program, or full production graph.',
            'Complete original historical specs/trim documents and selected small source/receipt metadata receive fresh full SHA. The old 64MiB graph and the entire multi-GiB canonical byte union were not reread or converted here; unchanged source/inverse and frozen prior actual evidence are not substituted for new fresh PREP.',
            '225+3=228 is a source-time unfiltered direct-root prediction. Actual new PREP must use complete original declared extras plus dynamic roots and measure actual stored wire JSON under the unchanged 64MiB cap.',
            'Final READY is exclusively a source admission flag. New PREP, build seal, full API/Root namespace, native own RSS, AAA/ABA and scientific completion remain unproved.'],
    complete_source_inverse_evidence=dict(path=str(OUT / 'complete_source_inverse_evidence.json'), bytes=len(source_raw), sha256=sha(source_raw)),
    fresh_pins=list(PINS.values()), completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
raw = (json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()
(OUT / 'REPORT.json').write_bytes(raw)
print(json.dumps(dict(status=report['status'], scope=report['scope'], report=str(OUT / 'REPORT.json'), report_bytes=len(raw),
                      report_sha256=sha(raw), reviewed_candidate_sha256=sha(ready_raw), fresh_pins=len(PINS),
                      initial_inverse_regions=13, ready_inverse_regions=2, final_to_F7_inverse_regions=12,
                      all65_ready_function_sources_exact_initial=True, source_evidence_sha256=sha(source_raw)), allow_nan=False))
