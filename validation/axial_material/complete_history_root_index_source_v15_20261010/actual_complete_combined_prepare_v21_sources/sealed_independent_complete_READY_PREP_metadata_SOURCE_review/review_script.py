"""Finite independent SOURCE/META review. No reviewed module is imported/executed.

Reads only the fixed TMP SOURCE package and its explicitly pinned SOURCE/META
references. ART references are recorded without being opened. No compile,
helper, guard, native, business or physical calculation occurs here.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat

OUT = Path(__file__).parent
PACKAGE = Path('/private/tmp/axmat_v21_COMPLETE_READY_runtime_genuine_PREP_closed_metadata_SOURCE_20261010_syx41')
ART = Path('/Users/wen/spot/validation/artifacts')
MANIFEST_SHA = 'ccb00e949582078a6a9e1f73c788a6a21d6b7dca9a02460e7fd1f8889cdaf6a8'
RUNTIME_SHA = '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
HOST_SHA = '776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405'
WRITER_SHA = '9dc8823bb3c5433d5cac464720e3f8d8da3d631ac0b4eaaef2d6f3bb83ba866d'
Q_SHA = '29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'
HELPER_SHA = 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
FUTURE = ['FUTURE_ACTUAL_COMBINED_DECLARATION_SHA', 'FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA', 'FUTURE_ACTUAL_COMBINED_SEAL_SHA', 'FUTURE_ACTUAL_COMBINED_TERMINAL_SHA', 'FUTURE_ACTUAL_COMBINED_RUNTIME_SHA', 'FUTURE_ACTUAL_NATIVE_TERMINAL_SHA']
checks = []
inputs = {}
raws = {}

def check(name, value):
    if type(value) is not bool or not value:
        raise ValueError(name)
    checks.append({'name': name, 'value': True})

def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def read(p, expected=None):
    p = Path(p)
    check('SOURCE/META only, never ART payload: ' + str(p), p.is_absolute() and not p.is_relative_to(ART) and '..' not in p.parts)
    for parent in [*reversed(p.parents), p]:
        s = parent.lstat()
        check('ordinary nonalias SOURCE/META path component: ' + str(parent), not stat.S_ISLNK(s.st_mode))
    before = identity(p)
    check('bounded regular singlelink SOURCE/META: ' + str(p), stat.S_ISREG(before[2]) and before[3] == 1 and before[4] <= 10 * 2**20)
    with p.open('rb') as f:
        raw = f.read()
        check('actual EOF: ' + str(p), f.read(1) == b'')
    check('whole SOURCE/META EOF stable 7ID: ' + str(p), identity(p) == before and len(raw) == before[4])
    pin = {'path': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw), 'identity': before}
    if expected is not None:
        check('exact SHA/bytes pin: ' + str(p), pin['sha256'] == expected['sha256'] and pin['size_bytes'] == expected['size_bytes'])
        if 'identity' in expected:
            check('exact typed7 source identity: ' + str(p), type(expected['identity']) is list and len(expected['identity']) == 7 and all(type(x) is int for x in expected['identity']) and pin['identity'] == expected['identity'])
        if 'path' in expected:
            check('exact path pin: ' + str(p), expected['path'] == str(p))
    if str(p) in inputs:
        check('repeated whole read unchanged: ' + str(p), inputs[str(p)] == pin)
    inputs[str(p)] = pin
    raws[str(p)] = raw
    return raw, pin

def pairs(items):
    d = {}
    for k, v in items:
        if k in d:
            raise ValueError('duplicate META key: ' + k)
        d[k] = v
    return d

def reject_constant(value):
    raise ValueError('nonfinite META constant: ' + value)

def meta(raw):
    v = json.loads(raw, object_pairs_hook=pairs, parse_constant=reject_constant)
    def finite(x):
        if isinstance(x, dict):
            return all(finite(q) for q in x.values())
        if isinstance(x, list):
            return all(finite(q) for q in x)
        return type(x) is not float or math.isfinite(x)
    check('all parsed META numbers finite', finite(v))
    return v

def definitions(text):
    return [(n.name, ast.get_source_segment(text, n)) for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]

def globals_ast(text):
    return {n.targets[0].id: n.value for n in ast.parse(text).body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}

def inverse(candidate, parent, hunks, old_key, new_key, count, label):
    check(label + ' exact hunk count', len(hunks) == count)
    generated = parent
    for h in hunks:
        check(label + ' unique forward full anchor', generated.count(h[old_key]) == 1)
        generated = generated.replace(h[old_key], h[new_key], 1)
    check(label + ' entire forward bytes', generated == candidate)
    restored = candidate
    for h in reversed(hunks):
        check(label + ' unique inverse full anchor', restored.count(h[new_key]) == 1)
        restored = restored.replace(h[new_key], h[old_key], 1)
    check(label + ' entire byte inverse', restored == parent)
    check(label + ' entire AST inverse', ast.dump(ast.parse(restored), include_attributes=False) == ast.dump(ast.parse(parent), include_attributes=False))
    return restored

def all_files(root):
    files = []
    directories = ['.']
    for folder, dirs, names in os.walk(root, followlinks=False):
        for n in dirs:
            p = Path(folder) / n
            check('sealed source directory ordinary: ' + str(p), not p.is_symlink() and p.is_dir())
            directories.append(str(p.relative_to(root)))
        for n in names:
            p = Path(folder) / n
            check('sealed source member ordinary: ' + str(p), not p.is_symlink() and p.is_file())
            files.append(str(p.relative_to(root)))
    return sorted(files), sorted(directories)

def typed_zero(tr, chunk):
    check('actual typed closed EXIT0 terminal: ' + chunk, type(tr) is dict and tr.get('chunk_id') == chunk and type(tr.get('exit_code')) is int and tr['exit_code'] == 0 and 'session_id' not in tr)

def main():
    manifest_raw, manifest_pin = read(PACKAGE / 'sealed_complete_SOURCE_manifest.json', {'sha256': MANIFEST_SHA, 'size_bytes': 15134})
    manifest = meta(manifest_raw)
    check('outer SOURCE-only status', manifest['schema'] == 'AXMAT_V21_COMPLETE_READY_RUNTIME_GENUINE_PREP_POSTCLOSE_METADATA_SOURCE_SEAL_V1' and manifest['status'] == 'SEALED_COMPLETE_SOURCE_READY_UNINSTALLED_NO_ACTUAL_PREP_OR_BUILD_CREDIT')
    names, dirs = all_files(PACKAGE)
    records = manifest['full_file_inventory']
    check('all25 files and all directories covered exactly', names == sorted([*records, 'sealed_complete_SOURCE_manifest.json']) and dirs == sorted(manifest['full_directory_relative_paths']) and len(names) == 25)
    check('outer declared 24 members/1054375 bytes', type(manifest['members_excluding_this_manifest']) is int and manifest['members_excluding_this_manifest'] == len(records) == 24 and manifest['bytes_excluding_this_manifest'] == sum(q['size_bytes'] for q in records.values()) == 1054375)
    for name, pin in records.items():
        read(PACKAGE / name, pin)
    check('outer has no runtime/science credit', all(manifest[k] is False for k in ('API_guard_business_executed', 'metadata_writer_executed', 'ART_graph_numeric_payload_read', 'canonical_or_frozen_namespace_written', 'installed', 'actual_PREP_build_INPUT_native_AAA_ABA_success_claimed')))

    copied = PACKAGE / 'sealed_READY_runtime_and_PREP_binding'
    bound = copied / 'BOUND_READY_SOURCE'
    old_manifest = meta(raws[str(copied / 'sealed_SOURCE_manifest.json')])
    original = Path(old_manifest['package_path'])
    original_names, original_dirs = all_files(original)
    inner_names, inner_dirs = all_files(copied)
    check('copied original whole16 files/dirs retained', original_names == inner_names == sorted([*old_manifest['full_member_inventory'], 'sealed_SOURCE_manifest.json']) and original_dirs == inner_dirs == sorted(old_manifest['complete_directory_relative_paths']) and len(inner_names) == 16)
    for name in inner_names:
        q = old_manifest['full_member_inventory'].get(name)
        original_raw, original_pin = read(original / name, q)
        check('all16 original SOURCE files byteexact copy: ' + name, original_raw == raws[str(copied / name)])
    check('first original manifest preserved SHA', hashlib.sha256(raws[str(copied / 'sealed_SOURCE_manifest.json')]).hexdigest() == '5b8653db81265f06eddbe6e9fb9e66c59dacbb8608537a69b4ca58244cbf30d3')
    generated = meta(raws[str(bound / 'generated_SOURCE_manifest.json')])
    check('generated source complete8 members', generated['member_count'] == len(generated['members']) == 8 and sorted(q['relative'] for q in generated['members']) == sorted(Path(n).name for n in inner_names if n.startswith('BOUND_READY_SOURCE/') and not n.endswith('generated_SOURCE_manifest.json')))
    for q in generated['members']:
        check('inner member source SHA/bytes unchanged: ' + q['relative'], hashlib.sha256(raws[str(bound / q['relative'])]).hexdigest() == q['sha256'] and len(raws[str(bound / q['relative'])]) == q['size_bytes'])

    proof = meta(raws[str(bound / 'full_READY_runtime_and_genuine_PREP_SOURCE_inverse.json')])
    runtime = raws[str(bound / 'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')].decode()
    host = raws[str(bound / 'combined_prepare_host.py')].decode()
    unready = raws[str(bound / 'UNREADY_parent_exact_source.txt')].decode()
    host_parent = raws[str(bound / 'genuine_PREP_parent_exact_source.txt')].decode()
    check('fixed actual runtime host pins', hashlib.sha256(runtime.encode()).hexdigest() == RUNTIME_SHA and hashlib.sha256(host.encode()).hexdigest() == HOST_SHA)
    inverse(runtime, unready, proof['runtime_ordered_hunks'], 'before', 'after', 4, 'complete READY runtime')
    inverse(host, host_parent, proof['host_ordered_hunks'], 'before', 'after', 11, 'complete genuine PREP host')
    check('70 runtime definitions original byteexact/order', definitions(runtime) == definitions(unready) and len(definitions(runtime)) == 70)
    original_globals, ready_globals = globals_ast(unready), globals_ast(runtime)
    check('all runtime global names unchanged', list(original_globals) == list(ready_globals))
    changed = [k for k in original_globals if ast.dump(original_globals[k], include_attributes=False) != ast.dump(ready_globals[k], include_attributes=False)]
    check('only3 runtime binding globals changed', changed == ['DRAFT_STATUS', 'INPUT_HELPERS', 'FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA'])
    check('six future business success pins stay None', all(ast.literal_eval(ready_globals[k]) is None for k in FUTURE) and proof['future_business_six_pins'] == {k: None for k in FUTURE})
    check('same full graph helper and real Q source bound', ast.literal_eval(ready_globals['FUTURE_ACTUAL_COMPLETE_GRAPH_HELPER_CONTROLS_ADMISSION_SHA']) == Q_SHA and HELPER_SHA in ast.get_source_segment(runtime, ready_globals['INPUT_HELPERS']))
    check('host original guard class API MRO and full pins retained by complete inverse', len(definitions(host)) == len(definitions(host_parent)) == 1)
    for anchor in ('full,production=helper.modules()', 'helper.guard_admission(full)', 'resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)', 'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30', "for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()", "[str(support.PYTHON),str(TARGET),'prepare-build']"):
        check('genuine host original scope anchor ' + anchor, anchor in host and anchor in host_parent)

    writer_dir = PACKAGE / 'metadata_writer_SOURCE_binding'
    writer_proof = meta(raws[str(writer_dir / 'full_metadata_writer_SOURCE_inverse.json')])
    writer = raws[str(writer_dir / 'write_actual_prepare_terminal.py')].decode()
    writer_parent = raws[str(writer_dir / 'original_metadata_writer_full_SOURCE.txt')].decode()
    check('fixed V21 writer9dc and originalaf0c', hashlib.sha256(writer.encode()).hexdigest() == WRITER_SHA and len(writer.encode()) == 9989 and hashlib.sha256(writer_parent.encode()).hexdigest() == 'af0c633fa31f29517fa5b8d8dbebdd16d7d255a1c3203047ecd79ef02722b539')
    inverse(writer, writer_parent, writer_proof['complete_forward_hunks'], 'old', 'new', 12, 'complete postclose metadata writer')
    old_defs, new_defs = definitions(writer_parent), definitions(writer)
    check('all7 writer definitions in original order', [k for k, _ in old_defs] == [k for k, _ in new_defs] == ['identity', 'pin', 'short', 'write', 'inventory', 'complete_namespace', 'main'])
    for (name, old), (_, new) in zip(old_defs, new_defs):
        restored = new
        for h in reversed(writer_proof['complete_forward_hunks']):
            restored = restored.replace(h['new'], h['old'])
        check('full writer definition inverse: ' + name, restored == old)
        if name != 'main':
            check('unchanged writer primitive source: ' + name, new == old)
        old_ast, new_ast = ast.parse(old), ast.parse(new)
        for cls in (ast.If, ast.Assert, ast.Raise, ast.Return):
            check('writer original ' + cls.__name__ + ' count: ' + name, sum(isinstance(n, cls) for n in ast.walk(old_ast)) == sum(isinstance(n, cls) for n in ast.walk(new_ast)))
        check('writer full callee order unchanged: ' + name, [ast.dump(n.func, include_attributes=False) for n in ast.walk(old_ast) if isinstance(n, ast.Call)] == [ast.dump(n.func, include_attributes=False) for n in ast.walk(new_ast) if isinstance(n, ast.Call)])
    for anchor in ("actual=json.loads((E/'Root_actual_prepare_tool_terminal_return.json').read_text())", "actual['closed'] is not True", "type(observed.get('exit_code')) is not int", "'session_id' in observed", "w['limit_failure'] is not None", "w['own_child_only'] is not True", "w['liveness_group_cleanup'] is not True", '(1800,600,512,2*2**30,1,1,0)', "h['input_sources']+[h['original_helper'],h['resource_factory']]", "if source_inventory!=d['source_inventory']", 'for root in (H,S,O,T,D)', 'for root in (H,S,O,T,D,E)', 'FACTORY.stat().st_size', "full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR'", "full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR'", 'separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False', "for key in cp['false_fields']: value[key]=False", "summary['original_five_build_stages_executed']=False", "summary['native_RSS_qualified']=False", "summary['cleanup_performed']=False"):
        check('postclose writer unchanged scope anchor: ' + anchor, anchor in writer and anchor in writer_parent)
    wg = globals_ast(writer)
    check('writer pins same canonical READY runtime', ast.literal_eval(wg['FACTORY_SHA']) == RUNTIME_SHA)
    prep_schema = ready_globals['PREP_TERMINAL_SCHEMA']
    check('runtime complete original PREP schema construction', isinstance(prep_schema, ast.BinOp) and isinstance(prep_schema.op, ast.Add) and isinstance(prep_schema.left, ast.Name) and prep_schema.left.id == 'PREFIX' and type(prep_schema.right.value) is str)
    full_prep_schema = ast.literal_eval(ready_globals['PREFIX']) + prep_schema.right.value
    check('writer original schema fully matches V21 runtime', full_prep_schema == 'AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_ACTUAL_EXTERNAL_PREP_RETURN_V1' and full_prep_schema in writer)

    check('exactly30 explicit source/META bindings and9 ART references', len(proof['all_SOURCE_Q_meta_references_full_EOF_SHA7ID_before_after']) == 30 and len(proof['ART_references_bound_by_actual_Q_only_never_read']) == 9)
    for q in proof['all_SOURCE_Q_meta_references_full_EOF_SHA7ID_before_after']:
        read(q['path'], q)
    for q in proof['ART_references_bound_by_actual_Q_only_never_read']:
        check('ART pin deliberately unopened: ' + q['path'], Path(q['path']).is_relative_to(ART) and q['path'] not in inputs)
    read(writer_proof['parent']['path'], writer_proof['parent'])
    qraw = raws[proof['actual_joint_Q']['path']]
    q = meta(qraw)
    check('actual Q29ac and full stored copy byteexact', hashlib.sha256(qraw).hexdigest() == Q_SHA and qraw == raws[str(bound / 'actual_joint_Q_exact_METADATA_copy.json')])
    check('actual qualified helper-only joint status', q['schema'] == 'AXMAT_ROOT_COMPLETE_GRAPH_PRIVATE_VERIFIER_HELPER_ACTUAL_JOINT_ADMISSION_V21' and q['status'] == 'QUALIFIED_ORIGINAL_FULL_PROTOCOL_AND_COMPLETE_CURRENT_GRAPH_METADATA_VERIFIER_ONLY_V21')
    check('Q no inherited business/physical qualification', all(q[k] is False for k in ('supervisor_class_or_MRO_modified', 'profile_used', 'fresh_production_graph_created', 'fresh_runtime_INPUT_qualified', 'new_combined_prepared', 'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted', 'whole_build_qualified', 'whole_INPUT_admitted', 'physical_balance_qualified')))
    check('actual helper same pin and size147870', q['helper']['sha256'] == HELPER_SHA and q['helper']['size_bytes'] == 147870 and q['helper'] == proof['actual_helper'])
    fresh = q['complete_current_graph_fresh_verifier']
    pure_terminal = meta(raws[q['actual_root_terminal']['path']])
    fresh_terminal = meta(raws[fresh['actual_root_terminal']['path']])
    typed_zero(pure_terminal['terminal_tool_return'], '5e1034')
    typed_zero(fresh_terminal['terminal_tool_return'], '59fbf2')
    check('new pure terminal exact schema/session closure', pure_terminal['schema'] == 'ROOT_V21_ACTUAL_PURE_PROTOCOL_TOOL_TERMINAL_RETURN_V1' and pure_terminal['closed'] is True and pure_terminal['initial_tool_return']['session_id'] == 49247 and pure_terminal['initial_tool_return']['chunk_id'] == 'ea406f' and pure_terminal['session_repolled_after_close'] is False)
    check('new fresh terminal exact schema/session closure', fresh_terminal['schema'] == 'AXMAT_V21B_ROOT_ACTUAL_COMPLETE_FRESH_VERIFIER_TOOL_TERMINAL_V1' and fresh_terminal['closed'] is True and fresh_terminal['initial_tool_return']['session_id'] == 38770 and fresh_terminal['initial_tool_return']['chunk_id'] == '45eca8' and fresh_terminal['no_closed_session_repoll'] is True and fresh_terminal['actual_tool_terminal_return_observed'] is True and fresh_terminal['retries'] == 0)
    pure_peer = meta(raws[q['independent_actual_review']['path']])
    fresh_peer = meta(raws[fresh['independent_actual_review']['path']])
    check('new original protocol independent saved review exact scope', pure_peer['schema'] == 'FINITE_V21_ACTUAL_60S_PROTOCOL_SAVED_META_REVIEW_V1' and pure_peer['status'] == 'ACTUAL_ORIGINAL_FULL_60S_PROTOCOL_PASS_VERIFIED_NOT_FULL_FRESH_VERIFIER' and pure_peer['blockers'] == [] and all(pure_peer[k] is True for k in ('all_explicit_input_SHA7ID_before_after_exact', 'full_report_original_metadata_and_both_strict_entrances_equal', 'full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified')))
    check('new complete verifier independent saved review exact scope', fresh_peer['schema'] == 'AXMAT_V21B_ACTUAL_COMPLETE_FRESH_VERIFIER_FINITE_SAVED_META_INDEPENDENT_REVIEW_V1' and fresh_peer['status'] == 'SAVED_ACTUAL_FULL_FRESH_VERIFIER_EVIDENCE_PASS_ROOT_ADMISSION_STILL_REQUIRED' and all(fresh_peer[k] is True for k in ('all_enumerated_and_explicit_input_pins_fresh_full_EOF_SHA256_and_7ID_before_after_equal', 'all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal', 'complete_expected_actual_JSON_wire_bytes_equal', 'one_genuine_stage_PASS', 'liveness_group_cleanup')) and fresh_peer['limit_failure'] is None and fresh_peer['retries'] == 0 and fresh_peer['private_positive_controls'] == 4 and fresh_peer['private_rejections'] == 3)
    pure_peer_tools = meta(raws[q['independent_actual_review_tool_return']['path']])
    fresh_peer_tools = meta(raws[fresh['independent_actual_review_tool_return']['path']])
    typed_zero(pure_peer_tools['actual_review_tool_result'], '2eb342')
    typed_zero(fresh_peer_tools['actual_review_terminal_return'], '45cf76')
    check('actual complete saved peer closed', fresh_peer_tools['actual_review_closed'] is True)
    protocol = q['full_protocol']
    check('original protocol all complete predicates retained', all(protocol[k] is True for k in ('original_and_fresh_small_producer_values_types_order_floatbits_exact', 'all_caller_mutable_identity_and_subtype_attributes_unchanged', 'complete_old_graph_two_normal_strict_entrances_exact', 'new_creation_trace_not_substituted_into_old_graph', 'full_json_types_order_floatbits_and_values_retained', 'default_source_nonmutation')))
    full_old_counts = {'absence_inputs': 449, 'absence_observations': 449, 'aliases': 186, 'canonical_files': 36776, 'category_requirement_rows': {'capture': 63535, 'code_environment': 34, 'component_ancestry': 90808, 'component_terminals': 43, 'dedup_build': 38154, 'memory_build': 25143, 'original92_build': 12362, 'physical_build': 7638, 'source_namespace': 50}, 'namespace_directories': 1119, 'namespace_files': 109886, 'namespace_symlinks': 1335, 'namespaces': 86, 'new_paths': 0, 'new_pins': 0, 'owners': 4471, 'read_trace_attempts': 181554, 'read_trace_records': 62332, 'requirement_owners': 4549, 'requirement_paths': 36778, 'requirements': 237767, 'role_requirement_rows': {'EXPECTED_INPUT_BYTES': 127881, 'NEWLY_DECLARED_INPUT_ONLY': 0, 'OWNED_EXHAUSTIVE_NAMESPACE_ALIAS_TARGET_BYTES': 0, 'OWNED_EXHAUSTIVE_NAMESPACE_BYTES': 109886}, 'subprocess_records': 0, 'top_fields': 31}
    check('original subtype2/reject61 and full trace counts', type(protocol['accepted_str_subtype_groups']) is int and protocol['accepted_str_subtype_groups'] == 2 and type(protocol['small_codec_rejections']) is int and protocol['small_codec_rejections'] == 61 and protocol['complete_original_graph_counts'] == full_old_counts and protocol['complete_new_creation_trace_records'] == 63379 and protocol['complete_new_creation_trace_actual_attempts'] == 175886)
    pure_caps = {'whole_seconds': 60, 'stage_seconds': 60, 'rss_mib': 512, 'archive_bytes': 64*2**20, 'history_bytes': 96*2**30, 'free_bytes': 8*2**30, 'threads': 1, 'children': 1, 'retries': 0}
    fresh_caps = {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_HOST_OUT_SOURCE_E_archive_bytes': 64*2**20, 'history_bytes': 96*2**30, 'free_bytes': 8*2**30, 'threads': 1, 'children': 1, 'retries': 0}
    check('distinct original pure and fresh caps intact', q['original_caps'] == pure_caps and fresh['original_caps'] == fresh_caps and all(type(v) is int for v in q['original_caps'].values()) and all(type(v) is int for v in fresh['original_caps'].values()))
    for label, scope, whole, stage in (('pure', q, 60, 60), ('fresh', fresh, 1800, 600)):
        for k, limit in (('whole_seconds', whole), ('child_seconds', stage), ('sampled_peak_rss_mib', 512)):
            v = scope['actual_measurement'][k]
            check('new actual ' + label + ' bounded measure ' + k, type(v) in (int, float) and math.isfinite(v) and 0 <= v < limit)
    fresh_summary = meta(raws[fresh['actual_controls_summary']['path']])
    check('fresh actual input45 is typedint not bool; no fixture false assumption', type(fresh_summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged']) is int and fresh_summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged'] == 45 and fresh_summary['complete_Source33_full_EOF_SHA7ID_before_after_unchanged'] is True and fresh_summary['complete_current_graph_full_EOF_SHA7ID_before_after_unchanged'] is True and fresh_summary['complete_27_fields_and_nested_type_order_value_floatbits_wire_equal'] is True)
    check('full27/37112/4positive3reject/3completegzip preserved', len(fresh['full_public_return_field_order']) == 27 and fresh['all_27_fields_nested_type_order_value_floatbits_and_wire_bytes_equal'] is True and fresh['complete_actual_unfiltered_read_trace_counts'] == {'records': 37112, 'attempts': 37112, 'canonical_files': 37111, 'external_graph_reads': 1, 'no_subprocess_reexecuted': True} and fresh['private_positive_controls'] == 4 and fresh['private_reject_controls'] == 3 and set(fresh['complete_gzips']) == {'expected_complete_return_contract', 'actual_complete_verifier_return', 'actual_complete_ReadOpenAudit_trace'})
    creator = meta(raws[proof['actual_joint_Q_creator_tool_record']['path']])
    typed_zero(creator['terminal_tool_return'], '7b37a2')
    observed_q = meta(creator['terminal_tool_return']['output'])
    check('actual Qcreator original JSON exact typed7 binding', creator['closed'] is True and creator['Root_META_only'] is True and creator['whole_build_INPUT_native_AAA_ABA_physics_qualified'] is False and observed_q['qualification'] == proof['actual_joint_Q'] and observed_q['pure_Root_terminal'] == '5e1034' and observed_q['fresh_Root_terminal'] == '59fbf2')

    binder_text = raws[str(copied / 'generate_READY_runtime_and_PREP_SOURCE_ONLY.py')].decode()
    check('binder public SOURCE funcs only standard library imports', all(isinstance(n, (ast.Import, ast.ImportFrom)) and (not isinstance(n, ast.ImportFrom) or n.module == 'pathlib') and (not isinstance(n, ast.Import) or all(a.name in ('argparse', 'ast', 'hashlib', 'json', 'math', 'os', 'stat') for a in n.names)) for n in ast.parse(binder_text).body if isinstance(n, (ast.Import, ast.ImportFrom))))
    for anchor in ("require(not path.is_relative_to(ART),'SOURCE binder never reads ART payload')", "typed_zero(last,final_chunk)", "pure_peer['full_counts_types_order_floatbits_and_default_nonmutation_receipts_verified']is True", "fresh_peer['all_27_public_return_fields_and_all_nested_types_order_values_floatbits_equal']is True", "typed_zero(pure_tools['actual_review_tool_result'],'2eb342')", "typed_zero(fresh_tools['actual_review_terminal_return'],'45cf76')", "fresh_summary['host_fixed_input_entries_full_EOF_SHA7ID_before_after_unchanged'])is int", "meta(creator['terminal_tool_return']['output'])", "definitions(runtime)==definitions(unready)"):
        check('binder full actual SOURCE/META predicate retained: ' + anchor, anchor in binder_text)
    old_tools = meta(raws[str(copied / 'actual_SOURCE_tool_returns.json')])
    writer_tools = meta(raws[str(PACKAGE / 'actual_complete_SOURCE_tool_returns.json')])
    check('actual author SOURCE failure/correction preserved', old_tools['first_binding_failure_chunk_id'] == 'a89890' and type(old_tools['first_binding_failure_typed_integer_exit_code']) is int and old_tools['first_binding_failure_typed_integer_exit_code'] == 1 and old_tools['corrected_binding_chunk_id'] == '3594d1' and type(old_tools['corrected_binding_typed_integer_exit_code']) is int and old_tools['corrected_binding_typed_integer_exit_code'] == 0 and writer_tools['first_writer_source_failure']['chunk_id'] == 'bdce7f' and writer_tools['first_writer_source_failure']['exit_code'] == 1 and writer_tools['corrected_writer_source_generation']['chunk_id'] == 'edd798' and writer_tools['corrected_writer_source_generation']['exit_code'] == 0)
    steps = meta(raws[str(PACKAGE / 'ROOT_COMPLETE_INSTALL_STEPS.json')])
    check('whole source writer archived before Dfreeze', steps['Source_package_must_be_archived_complete_before_D_freeze_and_PREP'] is True and steps['complete_postclose_metadata_writer']['sha256'] == WRITER_SHA and steps['runtime']['sha256'] == RUNTIME_SHA and steps['genuine_normal_PREP_host']['sha256'] == HOST_SHA and steps['Root_metadata_writer_argv_assumes_the_full_package_layout_preserved_in_D'] is True and steps['metadata_writer_executed'] is False and steps['new_PREP_executed'] is False and steps['new_build_executed'] is False)
    seal_raw, seal_pin = read(Path(str(PACKAGE) + '_seal_receipt') / 'actual_seal_tool_return.json')
    seal = meta(seal_raw)
    typed_zero(seal['terminal_tool_return'], 'd9391c')
    actual_seal = meta(seal['terminal_tool_return']['output'])
    check('actual outer seal source typed0 closed exact pin', seal['closed'] is True and seal['Root_installation_or_business_executed_by_this_agent'] is False and actual_seal['manifest'] == manifest_pin and actual_seal['members'] == 24 and actual_seal['member_bytes'] == 1054375)

    # One bounded end check of already enumerated SOURCE/META identities; no scans.
    for path, pin in inputs.items():
        check('all explicitly read SOURCE/META final exact7ID: ' + path, identity(Path(path)) == pin['identity'])
    result = {
        'schema': 'FINITE_V21_COMPLETE_READY_RUNTIME_GENUINE_PREP_METADATA_INDEPENDENT_SOURCE_REVIEW_V1',
        'status': 'SOURCE_PASS_COMPLETE_READY_UNINSTALLED_NO_ACTUAL_PREP_BUILD_INPUT_NATIVE_SCIENCE_CREDIT',
        'reviewed_outer_manifest': manifest_pin,
        'complete_package_files_including_manifest': 25,
        'complete_package_member_bytes_excluding_manifest': 1054375,
        'original_whole_sealed_package_byteexact_copied_files': 16,
        'full_forward_and_byte_AST_inverse_hunks': {'runtime': 4, 'genuine_PREP_host': 11, 'postclose_metadata_writer': 12},
        'runtime_all70_definitions_byteexact': True,
        'postclose_writer_all7_original_definition_inverses': True,
        'postclose_writer_original_control_flow_full_inverse_and_callee_sequence': True,
        'actual_Q': proof['actual_joint_Q'],
        'same_actual_helper': proof['actual_helper'],
        'actual_pure_terminal': q['actual_root_terminal'],
        'actual_complete_fresh_terminal': fresh['actual_root_terminal'],
        'actual_saved_independent_pure_review': q['independent_actual_review'],
        'actual_saved_independent_complete_fresh_review': fresh['independent_actual_review'],
        'explicit_SOURCE_META_whole_EOF_SHA_exact7ID_inputs': list(inputs.values()),
        'ART_references_stored_only_never_opened': proof['ART_references_bound_by_actual_Q_only_never_read'],
        'actual151pins_root_claim_not_reaudited': True,
        'six_future_business_success_pins': {k: None for k in FUTURE},
        'caps': {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_H_S_O_T_D_E_FACTORY_archive_bytes': 2*2**30, 'history_bytes': 96*2**30, 'free_floor_bytes': 8*2**30, 'threads': 1, 'children': 1, 'retries': 0},
        'author_SOURCE_failures_and_true_corrections_preserved': {'binder_failed': 'a89890:1', 'binder_corrected': '3594d1:0', 'writer_failed': 'bdce7f:1', 'writer_corrected': 'edd798:0'},
        'require_before_next_action': ['Root freshly install/pin canonical SOURCE and freeze complete D including writer', 'Root alone performs new one-use genuine bounded PREP', 'Only actual typed EXIT0 closed genuine PASS permits postclose metadata writer'],
        'checks': checks,
        'all_checks_typed_true': True,
        'blockers': [],
        'scope': {'standard_library_SOURCE_AST_hash_META_only': True, 'reviewed_module_imported_or_executed': False, 'helper_or_guard_API_called': False, 'compile_or_business_or_numeric_executed': False, 'ART_graph_material_numeric_payload_read': False, 'canonical_or_frozen_namespace_written': False, 'source_installation_performed': False, 'actual_PREP_qualified_by_this_review': False, 'whole_build_INPUT_native_AAA_ABA_physics_qualified': False, 'RSS_improvement_predicted': False},
    }
    with (OUT / 'REVIEW.json').open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    report = '\n'.join([
        result['status'],
        'Full25 SOURCE files: EOF/SHA/exact7ID verified; copied original16 SOURCE files byteexact.',
        'Full byte+AST inverse: runtime4 / genuine normal PREP host11 / postclose writer12. Runtime70 definitions exact; writer7 complete definition inverses.',
        'Actual helper Q29ac/dc01 binds new pure5e1034 and fullfresh59fbf2 closed typed0 terminals and both complete saved independent reviews. No ART payload opened.',
        'Original guards/MRO, whole1800/stage600/RSS512/2GiB joint H/S/O/T/D/E+FACTORY, history96GiB/free8GiB/threads1/child1/retry0 retained.',
        'Complete SOURCE writer must be included before Dfreeze; run only after Root future actual typed EXIT0 CLOSED genuine PREP.',
        'Actual SOURCE failures a89890 and bdce7f plus true corrections3594d1 and edd798 preserved.',
        'No candidate imports/APIs/compile/native/business/numerical run, numeric payload, canonical write or scientific qualification.',
        'Blockers: none. All six future business success pins remain None.',
        'Independent typedtrue checks: ' + str(len(checks)),
    ]) + '\n'
    with (OUT / 'REPORT.txt').open('x') as f:
        f.write(report)
    print(json.dumps({'status': result['status'], 'review_package': str(OUT), 'checks': len(checks), 'files': 25, 'full_inverse_hunks': result['full_forward_and_byte_AST_inverse_hunks'], 'REVIEW_sha256': hashlib.sha256((OUT / 'REVIEW.json').read_bytes()).hexdigest(), 'blockers': [], 'business_API_guard_numeric_executed': False}))

if __name__ == '__main__':
    main()
