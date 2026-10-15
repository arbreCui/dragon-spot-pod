"""Finite, independent stdlib SOURCE reads/AST/hash only. Never execute reviewed source."""
from pathlib import Path
import ast
import hashlib
import json
import stat

PACKAGE = Path('/private/tmp/axmat_current150_AB_rawrecord_wrapper_UNREADY_SOURCE_20261010_angular_v3q9')
OUT = Path(__file__).parent
EXPECTED_MANIFEST_SHA = 'f862d822da445bb7674e246c985dc1c8e4caed1f5fcc68e7ace4e791a955d97c'
EXPECTED_WRAPPER_SHA = '098b2a463877767254441ad49dd61076c0adb3320adf2d6c521e7abebac44116'
checks = []
observed = {}

def check(name, condition):
    if type(condition) is not bool or not condition:
        raise ValueError(name)
    checks.append({'name': name, 'value': True})

def pin_source(path):
    for component in [*reversed(path.parents), path]:
        check('not symlink: ' + str(component), not stat.S_ISLNK(component.lstat().st_mode))
    before_stat = path.lstat()
    before = [before_stat.st_dev, before_stat.st_ino, before_stat.st_mode, before_stat.st_nlink, before_stat.st_size, before_stat.st_mtime_ns, before_stat.st_ctime_ns]
    check('ordinary bounded singlelink SOURCE: ' + str(path), stat.S_ISREG(before_stat.st_mode) and before_stat.st_nlink == 1 and before_stat.st_size <= 2 * 2**20)
    with path.open('rb') as stream:
        raw = stream.read()
        check('SOURCE full EOF: ' + str(path), stream.read(1) == b'')
    after_stat = path.lstat()
    after = [after_stat.st_dev, after_stat.st_ino, after_stat.st_mode, after_stat.st_nlink, after_stat.st_size, after_stat.st_mtime_ns, after_stat.st_ctime_ns]
    check('SOURCE full EOF stable exact7ID: ' + str(path), before == after and len(raw) == before[4])
    return raw, {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'size_bytes': len(raw), 'identity': before}

manifest_raw, manifest_pin = pin_source(PACKAGE / 'sealed_SOURCE_manifest.json')
check('expected manifest SHA', manifest_pin['sha256'] == EXPECTED_MANIFEST_SHA)
manifest = json.loads(manifest_raw)
check('exactly13 SOURCE members plus manifest', manifest['members_excluding_manifest'] == 13 and len(manifest['files']) == 13 and sorted(p.name for p in PACKAGE.iterdir()) == sorted([*manifest['files'], 'sealed_SOURCE_manifest.json']))
sources = {}
trees = {}
for name, declared in manifest['files'].items():
    raw, actual = pin_source(PACKAGE / name)
    check('full member SHA/size/exact7ID matches manifest: ' + name, actual == declared)
    sources[name] = raw
    observed[name] = actual
    if name.endswith('.py') or name == 'wrapper_before_reader_pin_SOURCE.txt':
        tree = ast.parse(raw, filename=name)
        trees[name] = tree
        check('full SOURCE AST parsed: ' + name, isinstance(tree, ast.Module))
    elif name.endswith('.json'):
        check('full small META JSON parsed: ' + name, type(json.loads(raw)) is dict)
check('complete13 member total bytes', sum(p['size_bytes'] for p in observed.values()) == manifest['bytes_excluding_manifest'] == 132004)
check('expected wrapper SHA', observed['transfer_full_AB_rawrecord_UNREADY.py']['sha256'] == EXPECTED_WRAPPER_SHA)

for name, declared in manifest['complete_original_default_reader_sources'].items():
    raw, actual = pin_source(Path(declared['path']))
    check('original reader SOURCE exact fullEOF/SHA7ID: ' + name, actual == declared)
    check('original reader complete bytes equal SOURCE copy: ' + name, raw == sources['original_' + name + '_full.SOURCE.py'])
    ast.parse(raw, filename=name + '.py')
    observed['original_' + name] = actual

inverse = json.loads(sources['full_reader_SOURCE_pin_inverse.json'])
restored = sources['transfer_full_AB_rawrecord_UNREADY.py'].decode()
for hunk in reversed(inverse['hunks']):
    check('one known reader pin replacement', restored.count(hunk['new']) == 1)
    restored = restored.replace(hunk['new'], hunk['old'], 1)
before = sources['wrapper_before_reader_pin_SOURCE.txt']
check('complete reader pin two-hunk byte inverse', restored.encode() == before)
check('complete reader pin two-hunk AST inverse', ast.dump(ast.parse(restored), include_attributes=False) == ast.dump(trees['wrapper_before_reader_pin_SOURCE.txt'], include_attributes=False))

wrapper_tree = trees['transfer_full_AB_rawrecord_UNREADY.py']
wrapper_text = sources['transfer_full_AB_rawrecord_UNREADY.py'].decode()
globals_ast = {n.targets[0].id: n.value for n in wrapper_tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
future = ('SOURCE_QUALIFICATION_SHA256', 'ACTUAL_ROOT_BINDING_RECEIPT_SHA256', 'ACTUAL_TRANSFER_QUALIFICATION_SHA256', 'REACTION_MULTIPLICITY_QUALIFICATION_SHA256', 'ACTUAL_SCIENTIFIC_REFERENCE_SHA256')
check('all five actual qualification/binding/runtime/science pins None', all(ast.literal_eval(globals_ast[name]) is None for name in future))
check('still exact UNREADY source status', ast.literal_eval(globals_ast['SOURCE_STATUS']) == 'UNREADY_SOURCE_ONLY_ROOT_TRUE_BINDING_AND_GENUINE_SUPERVISOR_REQUIRED')
check('complete dimensions370/8/3/32', ast.literal_eval(globals_ast['EXPECTED_DIMENSIONS']) == (370, 8, 3, 32))
caps = {'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_archive_bytes': 2147483648, 'history_bytes': 103079215104, 'free_floor_bytes': 8589934592, 'threads': 1, 'children_at_once': 1, 'retries': 0}
expected_caps_ast = ast.parse("{'whole_seconds': 1800, 'stage_seconds': 600, 'rss_mib': 512, 'joint_archive_bytes': 2*2**30, 'history_bytes': 96*2**30, 'free_floor_bytes': 8*2**30, 'threads': 1, 'children_at_once': 1, 'retries': 0}", mode='eval').body
check('wrapper exact original caps SOURCE AST', ast.dump(globals_ast['CAPS'], include_attributes=False) == ast.dump(expected_caps_ast, include_attributes=False))
check('manifest original caps', manifest['original_caps'] == caps and all(type(v) is int for v in manifest['original_caps'].values()))
binding = json.loads(sources['ROOT_BINDING_TEMPLATE.UNREADY.json'])
check('binding original caps', binding['original_caps'] == caps)
check('binding true input/Python pins all unknown', all(item[k] is None for item in [*binding['inputs'].values(), binding['python']] for k in ('sha256', 'size_bytes', 'identity')))
check('binding actual source qualification unknown', binding['source_qualification_sha256'] is None)
check('no circular READY wrapper SHA in binding', binding['final_READY_wrapper_SHA_in_this_binding'] is None and binding['final_READY_wrapper_SHA_must_be_pinned_externally_by_real_genuine_host'] is True)
check('all scientific flags typedFalse', all(type(v) is bool and v is False for v in ast.literal_eval(globals_ast['FALSE_SCIENCE']).values()))

functions = {n.name: n for n in wrapper_tree.body if isinstance(n, ast.FunctionDef)}
calls = [n for n in ast.walk(wrapper_tree) if isinstance(n, ast.Call)]
native_calls = [n for n in calls if isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'first_reader' and n.func.attr == 'decode']
stream_calls = [n for n in calls if isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'second_reader' and n.func.attr == 'decode_stream']
check('one default native_records.decode(raw) with no keywords', len(native_calls) == 1 and len(native_calls[0].args) == 1 and isinstance(native_calls[0].args[0], ast.Name) and native_calls[0].args[0].id == 'raw' and not native_calls[0].keywords)
check('one default stream_records.decode_stream(binary iterator) with no keywords', len(stream_calls) == 1 and len(stream_calls[0].args) == 1 and isinstance(stream_calls[0].args[0], ast.Name) and stream_calls[0].args[0].id == 'binary_lines' and not stream_calls[0].keywords)
check('no wrapper reaction_selection reference', all(not (isinstance(n, ast.Name) and n.id == 'reaction_selection') and not (isinstance(n, ast.Attribute) and n.attr == 'reaction_selection') for n in ast.walk(wrapper_tree)))
stream_definition = next(n for n in trees['original_stream_records_full.SOURCE.py'].body if isinstance(n, ast.FunctionDef) and n.name == 'decode_stream')
check('stream original default keeps every record', len(stream_definition.args.defaults) == 1 and isinstance(stream_definition.args.defaults[0], ast.Lambda) and isinstance(stream_definition.args.defaults[0].body, ast.Constant) and stream_definition.args.defaults[0].body.value is True)
for name in ('spool_first_reader', 'compare_second_reader'):
    check('full record insertion-order .items() path: ' + name, any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name) and n.func.value.id == 'records' and n.func.attr == 'items' for n in ast.walk(functions[name])))
transfer = functions['transfer_state']
deletes = {target.id: node.lineno for node in ast.walk(transfer) if isinstance(node, ast.Delete) for target in node.targets if isinstance(target, ast.Name)}
check('first raw+dict fully deleted before second dict and second dict deleted within state', native_calls[0].lineno < deletes['raw'] < deletes['records'] < stream_calls[0].lineno < deletes['second_records'])
state_loops = [n for n in ast.walk(functions['main']) if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'state']
check('main state transfer order A then B', len(state_loops) == 1 and ast.literal_eval(state_loops[0].iter) == ('A', 'B'))
check('neither reader dict returned/stored across states', all(not (isinstance(n, ast.Name) and n.id in ('records', 'second_records', 'raw')) for n in ast.walk(next(n for n in transfer.body if isinstance(n, ast.Return)).value)))

anchors = {
    'raw exact-byte archive': 'dst.write(block)',
    'every raw physical close emitted': "row = {'entry': 'close'",
    'physical span begin/end/SHA': 'row.update(raw_begin_byte=begin, raw_end_byte=src.tell(), raw_span_sha256=digest.hexdigest())',
    'original character width preserved': "row['original_character_width'] = 4",
    'REAL32 plus separate parser64 bits': "struct.pack('<fd', x, x)",
    'REAL64 bits': "struct.pack('<d', x)",
    'exact str/int key types': 'all(type(v) in (str, int) for v in key)',
    'complete streaming count': "stats['all_records_validated'] == stats['retained_records'] == len(records) == expected_records",
    'all typed bytes compared': 'payload.read(len(chunk)) == chunk',
    'no typed trailing payload': "payload.read(1) == b''",
    'missing is explicit real gap': 'missing_real_record_no_substitution',
    'root FISSIONINDEX full256': "outcome(c, ('FISSIONINDEX',), (1,), 8*32)",
    'pergroup NUSIGF/CHI full256': "for name in ('NUSIGF','CHI'):",
    'full370 groups': 'for destination in range(1,371):',
    'all3 moments': 'for moment in range(3):',
    'all8 sparse mixtures': 'enumerate(zip(counts,tops,offsets),1)',
    'TRANC required actual field': "('NTOT0','TRANC','SIGS00','SIGS01','SIGS02','SIGW00','SIGW01','SIGW02')",
    'unused SCAT padding retained': 'raw_unreferenced_padding_retained_without_interpretation',
    'no contiguous sparse packing assumed': "'contiguous_packing_required_or_assumed':False",
    'ASCII not native memory bit proof': 'ASCII alone does not independently certify the original XSM memory bits.',
    'reaction multiplicity remains unverified': "'true_physical_loss_reaction_multiplicity_verified':False",
    'transport semantics remain unverified': "'transport_correction_semantics_qualified':False",
    'genuine supervisor watcher remains external': "'genuine_supervisor_watch_verified_here':False",
    'retained failure/no retry': 'ACTUAL_FAILED_OR_PARTIAL_TRANSFER_NO_RETRY_NO_QUALIFICATION',
}
for name, anchor in anchors.items():
    check('SOURCE complete-scope anchor: ' + name, anchor in wrapper_text)
check('no synthesized array/scattering/reaction helper calls', all(not (isinstance(n.func, ast.Attribute) and n.func.attr in ('scatter', 'macro', 'field', 'cpo_scatter', 'zeros', 'ones', 'asarray', 'solve', 'normalize')) for n in calls))
check('no spawned child/process imports', all(not (isinstance(n, ast.Import) and any(a.name.split('.')[0] in ('subprocess', 'multiprocessing') for a in n.names)) for n in ast.walk(wrapper_tree)))

report = {
    'schema': 'INDEPENDENT_FULL_AB_RAWRECORD_SOURCE_ONLY_PEER_REVIEW_V1',
    'status': 'SOURCE_ONLY_STATIC_REVIEW_COMPLETE_NOT_RUNTIME_OR_SCIENCE_ADMISSION',
    'package': str(PACKAGE),
    'manifest_pin': manifest_pin,
    'member_and_original_reader_pins': observed,
    'read_all13_members_plus_manifest': True,
    'all_py_and_prior_wrapper_complete_AST_parsed': True,
    'all_checks': checks,
    'source_blockers_for_full_raw_transfer': [],
    'reviewed_wrapper_reader_or_generator_imported_compiled_or_run': False,
    'material_payload_or_ART_numeric_read': False,
    'existing_sources_or_project_DE_or_canonical_modified': False,
    'actual_transfer_success': None,
    'actual_protocol_control_success': None,
    'scientific_accuracy_or_neutron_balance_pass': None,
    'root_context_not_changed': {'AAA_physical_gates': '7/8', 'ABA_started': False},
    'source_scope_limits': [
        'Only complete ASCII raw bytes and both full ASCII decoder typed values/bits are covered; original LCM/XSM memory bits require producer evidence.',
        'The required field contract is a structural inventory; true physical reaction/multiplicity and transport-correction semantics remain explicitly unqualified.',
        'The wrapper declares caps and child stage wall checks; actual joint HOST+OUT+SOURCE+D/E/resource/RSS/watch/closure evidence must come from the genuine external supervisor.',
        'FUTURE_PROTOCOL_CONTROLS phrase nonrepresentable REAL32 should be read as overflow/nonfinite rejection; arbitrary finite decimals are rounded to IEEE float32 while exact parser64 bits and raw bytes remain preserved. It is not an exact-representability test.',
    ],
    'required_next_steps': [
        'Root closes its current business stage and pins actual original A/B/Python/reader/Source receipt under the unchanged genuine original supervisor and caps.',
        'Root creates immutable binding then separate three-global-line READY derivative; independent exact three-hunk byte/AST inverse review remains required.',
        'Future actual child controls, complete A then B transfer, genuine terminal/resource receipts and saved-evidence review remain required before software admission.',
    ],
}
for name, expected in observed.items():
    _, actual = pin_source(Path(expected['path']))
    check('final unchanged source pin: ' + name, actual == expected)
_, final_manifest = pin_source(PACKAGE / 'sealed_SOURCE_manifest.json')
check('final unchanged manifest fullEOF/SHA7ID', final_manifest == manifest_pin)
with (OUT / 'SOURCE_PEER_REVIEW.json').open('x') as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write('\n')
print(json.dumps({'status': report['status'], 'review_path': str(OUT / 'SOURCE_PEER_REVIEW.json'), 'manifest_sha256': manifest_pin['sha256'], 'wrapper_sha256': observed['transfer_full_AB_rawrecord_UNREADY.py']['sha256'], 'members': 13, 'source_blockers': [], 'static_checks': len(checks), 'reviewed_code_executed': False, 'material_payload_read': False, 'actual_transfer_success': None}, allow_nan=False))
