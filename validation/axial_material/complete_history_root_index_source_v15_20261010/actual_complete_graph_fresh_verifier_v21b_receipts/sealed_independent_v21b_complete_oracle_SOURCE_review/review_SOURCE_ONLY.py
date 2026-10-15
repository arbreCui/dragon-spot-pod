"""Independent full-EOF SOURCE/AST review; no candidate/helper execution."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

PACKAGE = Path('/private/tmp/axmat_v21b_complete_fresh_verifier_old_constructor_oracle_SOURCE_ONLY_20261010_angular_qhs7_kjb')
OUT = Path(__file__).parent
MANIFEST_SHA = '6a2495ae42e0cbabdb257a92347de7391451e7e93a9fc1530dbcc7badd787483'
OLD_PACKAGE = Path('/private/tmp/axmat_v21_complete_fresh_verifier_ART_roots_SOURCE_fix_20261010_angular_ws815t4g')
OLD_HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py')
NEW_HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
checks = []
source_pins = []

def check(name, condition):
    if type(condition) is not bool or not condition:
        raise AssertionError(name)
    checks.append({'name': name, 'value': condition, 'value_type': 'bool'})

def ident(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def read(path, expected_sha=None, expected_identity=None):
    before = ident(path)
    check('regular private nonsymlink SOURCE/META: ' + str(path), stat.S_ISREG(before[2]) and before[3] == 1 and not path.is_symlink())
    h = hashlib.sha256()
    blocks = []
    count = 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(2**20)
            if not block:
                break
            h.update(block)
            blocks.append(block)
            count += len(block)
    after = ident(path)
    check('full EOF stable SHA7ID: ' + str(path), before == after and count == before[4] and all(type(v) is int for v in before))
    digest = h.hexdigest()
    if expected_sha is not None:
        check('exact pinned SOURCE SHA: ' + str(path), digest == expected_sha)
    if expected_identity is not None:
        check('exact pinned SOURCE 7ID: ' + str(path), before == expected_identity)
    pin = {'path': str(path), 'sha256': digest, 'identity': before, 'size_bytes': count}
    source_pins.append(pin)
    return b''.join(blocks), pin

def pairs(entries):
    result = {}
    for k, v in entries:
        if k in result:
            raise ValueError('duplicate SOURCE META key: ' + k)
        result[k] = v
    return result

def constant(value):
    raise ValueError('nonfinite SOURCE META: ' + value)

def metadata(raw):
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)

def parse(raw):
    return ast.parse(raw)

def dump(node):
    return ast.dump(node, include_attributes=False)

def functions(tree):
    return {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

def globals_ast(tree):
    return {n.targets[0].id: n.value for n in tree.body if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}

def assigned(node, name):
    matches = [n.value for n in ast.walk(node) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    check('single independent AST assignment: ' + name, len(matches) == 1)
    return matches[0]

def source(raw, node):
    return ast.get_source_segment(raw.decode('utf-8'), node)

def dict_keys(node):
    check('complete literal dict AST shape', isinstance(node, ast.Dict) and all(isinstance(k, ast.Constant) and type(k.value) is str for k in node.keys))
    return [k.value for k in node.keys]

def inverse(raw, hunks, expected, label):
    result = raw.decode('utf-8')
    check(label + ' typed finite inverse list', type(hunks) is list and all(type(h) is dict and set(h) == {'before', 'after'} and all(type(v) is str for v in h.values()) for h in hunks))
    for i, hunk in reversed(list(enumerate(hunks))):
        check(label + ' unique complete reverse hunk ' + str(i), result.count(hunk['after']) == 1)
        result = result.replace(hunk['after'], hunk['before'], 1)
    restored = result.encode('utf-8')
    check(label + ' entire byte inverse', restored == expected)
    check(label + ' entire AST inverse', dump(parse(restored)) == dump(parse(expected)))
    return {'hunk_count': len(hunks), 'full_bytes_exact': True, 'full_AST_exact': True, 'restored_sha256': hashlib.sha256(restored).hexdigest(), 'restored_bytes': len(restored), 'ordered_hunks': hunks}

def typed_literal_pin(value):
    return type(value) is dict and set(value) == {'path', 'sha256', 'identity'} and type(value['path']) is str and type(value['sha256']) is str and len(value['sha256']) == 64 and type(value['identity']) is list and len(value['identity']) == 7 and all(type(v) is int for v in value['identity'])

manifest_raw, manifest_pin = read(PACKAGE / 'MANIFEST.json', MANIFEST_SHA)
manifest = metadata(manifest_raw)
check('manifest actual sealed Source-only schema', manifest['schema'] == 'AXMAT_V21_FRESH_VERIFIER_BINDING_SOURCE_PACKAGE_MANIFEST_V1' and manifest['source_only'] is True and manifest['runtime_executed'] is False)
check('sealed manifest full27 member371881 byte inventory', len(manifest['members']) == manifest['member_count'] == 27 and sum(x['size_bytes'] for x in manifest['members']) == manifest['total_member_bytes'] == 371881)
package_before = ident(PACKAGE)
names_before = sorted(p.name for p in PACKAGE.iterdir())
check('complete final flat package namespace', names_before == sorted([x['name'] for x in manifest['members']] + ['MANIFEST.json']) and len(set(names_before)) == 28)
members = {}
member_pins = {}
all_metadata = {}
for entry in manifest['members']:
    check('flat exact manifest member name ' + entry['name'], type(entry['name']) is str and Path(entry['name']).name == entry['name'] and entry['path'] == str(PACKAGE / entry['name']) and type(entry['identity']) is list and len(entry['identity']) == 7 and all(type(v) is int for v in entry['identity']))
    raw, pin = read(PACKAGE / entry['name'], entry['sha256'], entry['identity'])
    check('manifest exact member bytes ' + entry['name'], pin['size_bytes'] == entry['size_bytes'])
    members[entry['name']] = raw
    member_pins[entry['name']] = pin
    if entry['name'].endswith('.json'):
        all_metadata[entry['name']] = metadata(raw)
    if entry['name'].endswith('.py'):
        compile(raw, entry['name'], 'exec')  # Compile only, never execute/import.
        check('SOURCE syntax compiles without execution ' + entry['name'], True)

draw = members['fresh_verifier_controls.v21b.READY_SOURCE.py']
hraw = members['fresh_verifier_host.v21b.READY_SOURCE.py']
braw = members['bind_fresh_verifier_sources.py']
pdraw = members['fresh_verifier_controls.py.previous_READY_SOURCE.txt']
phraw = members['fresh_verifier_host.py.previous_READY_SOURCE.txt']
check('fixed current driver 895c full26061 bytes', hashlib.sha256(draw).hexdigest() == '895c889569507f2b5e28ee1da6efc6c91bbdd30cd05338dd6e039d9591e72f84' and len(draw) == 26061)
check('fixed current host bb232 full24654 bytes', hashlib.sha256(hraw).hexdigest() == 'bb232eb13187013fde74e909aac8d316648a83a63115758ad2f0db200ab2322f' and len(hraw) == 24654)
check('fixed v21b binder52c4 bytes', hashlib.sha256(braw).hexdigest() == '52c42fcf871e0b01d1a4373f35a3a740e344458282868a3765f5fa5f2e2bcd0e')
check('fixed prior ee552 full23482 SOURCE bytes', hashlib.sha256(pdraw).hexdigest() == 'ee552f1458957281a695f84c8cd74fb8c25450228eaa6aec4bbd48601d29395a' and len(pdraw) == 23482)
check('fixed prior3633 full24650 SOURCE bytes', hashlib.sha256(phraw).hexdigest() == '3633e8ea03992293b6a481f49baa0c783a28446fbca2e37325177cd6c9e3fba2' and len(phraw) == 24650)
dt, ht, pdt, pht, bt = map(parse, (draw, hraw, pdraw, phraw, braw))
dd, hd, pdd, phd = map(functions, (dt, ht, pdt, pht))
dg, hg, pdg, phg = map(globals_ast, (dt, ht, pdt, pht))
proof = all_metadata['V21B_COMPLETE_SOURCE_INVERSE_PROOF.json']
inverses = {}
inverses['ready_driver_to_ee552'] = inverse(draw, proof['ready_driver_ordered_hunks'], pdraw, 'complete driver→ee552')
inverses['ready_host_to_3633'] = inverse(hraw, proof['ready_host_ordered_hunks'], phraw, 'complete host→3633')
check('only5 driver and5 host finite hunks', len(proof['ready_driver_ordered_hunks']) == 5 and len(proof['ready_host_ordered_hunks']) == 5)
check('all previous driver definitions in order plus only one constructor', set(dd) == set(pdd) | {'_old_parent_complete_return_constructors'} and [name for name in dd if name != '_old_parent_complete_return_constructors'] == list(pdd))
unchanged_driver = []
for name, node in pdd.items():
    if name == 'expected_return_from_old':
        continue
    check('original complete driver function bytes unchanged: ' + name, source(pdraw, node) == source(draw, dd[name]))
    unchanged_driver.append(name)
check('all previous host definitions exact set', set(hd) == set(phd))
for name, node in phd.items():
    check('original complete host function bytes unchanged: ' + name, source(phraw, node) == source(hraw, hd[name]))
check('only OUTPUT_PATH driver global changed', set(dg) == set(pdg) and [name for name in dg if dump(dg[name]) != dump(pdg[name])] == ['OUTPUT_PATH'])
check('only four namespace+TARGET_SHA host globals changed', set(hg) == set(phg) and [name for name in hg if dump(hg[name]) != dump(phg[name])] == ['HOST', 'OUT', 'SOURCE_ARCHIVE', 'RECEIPTS', 'TARGET_SHA'])

oldraw, oldpin = read(OLD_HELPER, 'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6')
newraw, newpin = read(NEW_HELPER, 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7')
check('fixed old145715/new147870 complete SOURCE bytes', len(oldraw) == 145715 and len(newraw) == 147870)
od, nd = functions(parse(oldraw)), functions(parse(newraw))
og, ng = globals_ast(parse(oldraw)), globals_ast(parse(newraw))
old_return = [n.value for n in od['verify_graph'].body if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict)]
new_return = [n.value for n in nd['verify_graph'].body if isinstance(n, ast.Return) and isinstance(n.value, ast.Dict)]
check('single full public old/new verify return dict', len(old_return) == len(new_return) == 1)
old_return, new_return = old_return[0], new_return[0]
check('entire old/new public return AST unchanged', dump(old_return) == dump(new_return))
check('original entire reader constant AST preserved in installed helper', dump(og['FRESH_READER_CONTRACT']) == dump(ng['FRESH_READER_CONTRACT']))
check('original entire closure category AST preserved in installed helper', dump(og['CLOSURE_CATEGORIES']) == dump(ng['CLOSURE_CATEGORIES']))
expected = assigned(dd['expected_return_from_old'], 'expected')
previous_expected = assigned(pdd['expected_return_from_old'], 'expected')
public_fields = dict_keys(old_return)
check('full27 original public top order retained', len(public_fields) == 27 and public_fields == dict_keys(new_return) == dict_keys(expected) == dict_keys(previous_expected) == ast.literal_eval(hg['RETURN_FIELDS']))
for key, val, prev in zip(public_fields, expected.values, previous_expected.values):
    if key not in ('fresh_reader_contract', 'coverage', 'trace_coverage'):
        check('complete original expected AST retained: ' + key, dump(val) == dump(prev))
old_values = dict(zip(public_fields, old_return.values))
check('old reader API derives full deepcopy original constant', ast.unparse(old_values['fresh_reader_contract']) == 'copy.deepcopy(FRESH_READER_CONTRACT)')
check('old coverage/trace API uses freshly generated full fields', ast.unparse(old_values['coverage']) == 'coverage' and ast.unparse(old_values['trace_coverage']) == 'trace_coverage')
check('other nested typed_snapshot only original full deepcopy', ast.unparse(old_values['typed_snapshot']) == "copy.deepcopy(graph['typed_snapshot'])" and ast.unparse(dict(zip(public_fields, expected.values))['typed_snapshot']) == "graph['typed_snapshot']")
constructor = dd['_old_parent_complete_return_constructors']
ctor_text = ast.unparse(constructor)
reader = assigned(constructor, 'reader')
coverage = assigned(constructor, 'coverage')
trace = assigned(constructor, 'trace')
old_counts = assigned(od['_trace_coverage'], 'counts')
check('oracle reader original bcd constant only full deepcopy', ast.unparse(reader) == 'copy.deepcopy(old.FRESH_READER_CONTRACT)')
reader_keys = dict_keys(og['FRESH_READER_CONTRACT'])
check('complete original ten reader fields', len(reader_keys) == 10)
check('reader full mapping equality gate retained', "reader == graph['fresh_reader_contract']" in ctor_text)
categories = ast.literal_eval(og['CLOSURE_CATEGORIES'])
check('all9 coverage original sequence', categories == ('code_environment', 'original92_build', 'memory_build', 'dedup_build', 'physical_build', 'capture', 'component_ancestry', 'component_terminals', 'source_namespace'))
check('oracle complete coverage dict original category sequence no filtering', isinstance(coverage, ast.DictComp) and ast.unparse(coverage.key) == 'category' and len(coverage.generators) == 1 and ast.unparse(coverage.generators[0].iter) == 'old.CLOSURE_CATEGORIES' and not coverage.generators[0].ifs)
old_inner = [n for n in ast.walk(od['_coverage']) if isinstance(n, ast.Dict) and len(n.keys) == 3 and all(isinstance(k, ast.Constant) for k in n.keys) and [k.value for k in n.keys] == ['canonical_files', 'bytes', 'owners']]
check('one original full3-field coverage inner constructor', len(old_inner) == 1)
check('all coverage nested keyorder original', dict_keys(coverage.value) == dict_keys(old_inner[0]) == ['canonical_files', 'bytes', 'owners'])
check('old coverage owners originally complete sorted names list', ast.unparse(old_inner[0].values[2]) == 'sorted(names)')
for key, value in zip(dict_keys(coverage.value), coverage.value.values):
    wanted = "copy.deepcopy(saved_coverage[category]['owners'])" if key == 'owners' else "saved_coverage[category][" + repr(key) + ']'
    check('complete stored coverage value unconverted: ' + key, ast.unparse(value) == wanted)
trace_keys = dict_keys(old_counts)
check('all10 trace counters original nested keyorder', len(trace_keys) == 10 and dict_keys(trace) == trace_keys)
for key, value in zip(trace_keys, trace.values):
    check('all saved trace counts unconverted: ' + key, ast.unparse(value) == 'saved_trace[' + repr(key) + ']')
for fragment in ("set(saved_coverage) == set(old.CLOSURE_CATEGORIES)", "set(descriptor) == {'canonical_files', 'bytes', 'owners'}", 'set(saved_trace) == set(trace)', 'coverage == saved_coverage and trace == saved_trace'):
    check('complete keyset/value gate: ' + fragment, fragment in ctor_text)
check('oracle no new helper, sort, filtering, old API calls', not any(isinstance(n, ast.Call) and (ast.unparse(n.func).startswith('new.') or ast.unparse(n.func) in ('sorted', 'filter', 'old.verify_graph', 'old._coverage', 'old._trace_coverage')) for n in ast.walk(constructor)))
check('old actual full helper compares regenerated coverage/trace to saved graph', "coverage == graph['coverage']" in ast.unparse(od['verify_graph']) and "trace_coverage == graph['trace_coverage']" in ast.unparse(od['verify_graph']))
check('new actual full helper still complete coverage/trace equality gates', "coverage == graph['coverage']" in ast.unparse(nd['verify_graph']) and "trace_coverage == graph['trace_coverage']" in ast.unparse(nd['verify_graph']))
check('original coverage constructor unchanged old/new', source(oldraw, od['_coverage']) == source(newraw, nd['_coverage']))
check('original tracecoverage constructor unchanged old/new', source(oldraw, od['_trace_coverage']) == source(newraw, nd['_trace_coverage']))
check('expected only one added pure oracle call', sum(isinstance(n, ast.Call) and ast.unparse(n.func) == '_old_parent_complete_return_constructors' for n in ast.walk(dd['expected_return_from_old'])) == 1)

for name in ('ACTUAL_SUCCESS_PINS', 'UNKNOWN_Q', 'UNKNOWN_BUSINESS_PINS'):
    check('driver no false runtime future pin: ' + name, ast.literal_eval(dg[name]) is None)
for name in ('UNKNOWN_Q', 'UNKNOWN_BUSINESS_PINS'):
    check('host no false runtime future pin: ' + name, ast.literal_eval(hg[name]) is None)
check('driver actual fixed dc01 path/SHA/bytes/7ints unchanged', all(dump(dg[name]) == dump(pdg[name]) for name in ('NEW_HELPER_PATH', 'NEW_HELPER_SHA256', 'NEW_HELPER_SOURCE_BYTES', 'NEW_HELPER_IDENTITY')))
check('helper SOURCE exact7ID literal still current installed Source', ast.literal_eval(dg['NEW_HELPER_IDENTITY']) == newpin['identity'])
for name, sha in (('BOUND_HELPER_PIN', 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'), ('INSTALL_WITNESS_PIN', 'f8e83e8ca68397f30657ed5a8fc5b0f2fdcb0e4bd8071a006cca75ba570a68b9'), ('SOURCE_INSTALL_RECORD_PIN', '7f5a98632ac8210de1ae0926bebcd51a43359ec9f17e89b7e81ecf931879fc37')):
    value = ast.literal_eval(hg[name])
    check('exact literal fixed actual Source pin, no witness read: ' + name, typed_literal_pin(value) and value['sha256'] == sha and dump(hg[name]) == dump(phg[name]))
check('actual required driverSHA exact current Source bytes', ast.literal_eval(hg['TARGET_SHA']) == hashlib.sha256(draw).hexdigest())
check('normal source READY status only, not business qualification', ast.literal_eval(dg['SOURCE_STATUS']) == ast.literal_eval(hg['SOURCE_STATUS']) == 'READY_SOURCE_BOUND_BY_ROOT')
check('new one-use v21b OUT exact driver literal', ast.literal_eval(dg['OUTPUT_PATH']) == '/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21b-20261010')
for name in ('HOST', 'OUT', 'SOURCE_ARCHIVE', 'RECEIPTS'):
    check('only fresh v21b namespace literal: ' + name, 'v21b' in ast.unparse(hg[name]) and dump(hg[name]) != dump(phg[name]))
check('frozen fixed V20 graphpin literal unchanged driver and host', dump(dg['GRAPH_PIN']) == dump(pdg['GRAPH_PIN']) and all(dump(hg[name]) == dump(phg[name]) for name in ('GRAPH_PATH', 'GRAPH_SHA', 'GRAPH_IDENTITY')))

oldbinder, oldbinderpin = read(OLD_PACKAGE / 'bind_fresh_verifier_sources.py', '76c516aa1965ce6316062df6806a9616e4dccff1bc239d37b52c542234c491c4')
oldunreadydriver, oldudpin = read(OLD_PACKAGE / 'fresh_verifier_controls.UNREADY.py')
oldunreadyhost, olduhpin = read(OLD_PACKAGE / 'fresh_verifier_host.UNREADY.py')
inverses['binder_to_76c516'] = inverse(braw, proof['binder_ordered_hunks'], oldbinder, 'complete namespace binder→76c516')
inverses['unready_driver_to_a459'] = inverse(members['fresh_verifier_controls.UNREADY.py'], proof['unready_driver_ordered_hunks'], oldunreadydriver, 'complete UNREADY driver→a459')
inverses['unready_host_to_a459'] = inverse(members['fresh_verifier_host.UNREADY.py'], proof['unready_host_ordered_hunks'], oldunreadyhost, 'complete UNREADY host→a459')
hostproof = all_metadata['host_template_complete_source_inverse.json']
originalhost = members['pure_helper_controls_host.original.txt']
check('full genuine original de72 9406-byte parent Source', hashlib.sha256(originalhost).hexdigest() == 'de72db68baa9b91fee8aad1965605ab25c9cb11ed2ea3013c3a1f04d52a41fb2' and len(originalhost) == 9406)
inverses['unready_host_to_de72'] = inverse(members['fresh_verifier_host.UNREADY.py'], hostproof['ordered_hunks'], originalhost, 'complete inherited genuine23 host→de72')
check('exact inherited23 genuine host inverse full', len(hostproof['ordered_hunks']) == 23)
render_driver = members['fresh_verifier_controls.UNREADY.py'].decode()
for before, after in [("SOURCE_STATUS = 'UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'", "SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'")] + [(name + ' = None', name + ' = ' + repr(ast.literal_eval(dg[name]))) for name in ('NEW_HELPER_PATH', 'NEW_HELPER_SHA256', 'NEW_HELPER_SOURCE_BYTES', 'NEW_HELPER_IDENTITY', 'OUTPUT_PATH')]:
    check('literal-only noexecution future driver binding anchor ' + before.split('=')[0], render_driver.count(before) == 1)
    render_driver = render_driver.replace(before, after, 1)
check('future6globs Root literal render exact final driver', render_driver.encode() == draw)
render_host = members['fresh_verifier_host.UNREADY.py'].decode()
for before, after in [("SOURCE_STATUS='UNREADY_SOURCE_ONLY_NO_ACTUAL_SUCCESS'", "SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'")] + [(name + '=None', name + '=' + repr(ast.literal_eval(hg[name]))) for name in ('TARGET_SHA', 'BOUND_HELPER_PIN', 'INSTALL_WITNESS_PIN', 'SOURCE_INSTALL_RECORD_PIN')]:
    check('literal-only noexecution future host binding anchor ' + before.split('=')[0], render_host.count(before) == 1)
    render_host = render_host.replace(before, after, 1)
check('future5globs Root literal render exact final host', render_host.encode() == hraw)

run_text = ast.unparse(dd['run'])
exact_text = ast.unparse(dd['exact_value'])
host_main = ast.unparse(hd['main'])
host_controls = ast.unparse(hd['_full_controls'])
for fragment in ('type(left) is type(right)', 'zip(left.items(), right.items())', "struct.pack('>d', left) == struct.pack('>d', right)"):
    check('full actual nested type/order/floatbits strict compare unchanged: ' + fragment, fragment in exact_text)
check('no sorted/ignoreorder in strict actual return comparison', not any(isinstance(n, ast.Call) and ast.unparse(n.func) in ('sorted', 'set') for n in ast.walk(dd['exact_value'])))
check('exact one full newverify public call no consumer filter', sum(isinstance(n, ast.Call) and ast.unparse(n.func) == 'new.verify_graph' and [kw.arg for kw in n.keywords] == ['expected_sha256', 'phase'] for n in ast.walk(dd['run'])) == 1)
for fragment in ("set(actual_paths) == paths | {GRAPH_PIN['path']}", '== 37112', "trace['subprocess_records'] == []", "trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is True"):
    check('all37111+1 reads full honest audit unchanged: ' + fragment, fragment in run_text)
check('all three unfiltered fullgzip writes unchanged', sum(isinstance(n, ast.Call) and ast.unparse(n.func) == 'lossless_json_gzip' for n in ast.walk(dd['run'])) == 3 and source(draw, dd['lossless_json_gzip']) == source(pdraw, pdd['lossless_json_gzip']))
check('all4 positives3rejects exact source unchanged', source(draw, dd['private_trace_controls']) == source(pdraw, pdd['private_trace_controls']) and 'len(positive) == 4 and len(negatives) == 3' in ast.unparse(dd['private_trace_controls']))
check('fixed input fullEOF Source7ID before/after unchanged', source(draw, dd['full_pin']) == source(pdraw, pdd['full_pin']) and "after == report['fixed_inputs_before']" in run_text)
for fragment in ('full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)', 'helper.guard_admission(full)', 'Path(full.__file__).resolve() != support.FULL', 'Path(production.__file__).resolve() != support.PARENT', 'type(runner) is not full.OwnRSSSerialExecutor', 'runner.resources is not resources'):
    check('genuine guard/MRO/path/executor call unchanged: ' + fragment, fragment in host_main)
for fragment in ('declared_history_roots = (HOST, OUT, support.SOURCE, support.OUT, support.TERMINAL)', 'not path.is_relative_to(support.ART)', 'resource.history_roots([str(path) for path in declared_history_roots], support.ART)', 'resource.DynamicHistoryResources(support.ART, roots, 8 * 2 ** 30, 96 * 2 ** 30, production.ResourceFailure)'):
    check('full dynamic ART scope resource Source unchanged: ' + fragment, fragment in host_main)
check('joint HOST OUT D E archive both original checks unchanged', host_main.count('support.archive_bytes((HOST, OUT, SOURCE_ARCHIVE, RECEIPTS))') == 2)
check('no invented separate before joint64 measurement', 'archive_before_result_bytes=archived' in host_main and host_main.count('support.archive_bytes(') == 2)
check('unchanged1800/600/512/64MiB exact host assignment', ast.unparse(next(n.value for n in ht.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Tuple) and [x.id for x in t.elts] == ['WHOLE_CAP', 'STAGE_CAP', 'RSS_CAP', 'ARCHIVE_CAP'] for t in n.targets))) == '(1800, 600, 512, 64 * 2 ** 20)')
check('all original resources threads child retry report contract', '(1800, 600, 512, 64 * 2 ** 20, 96 * 2 ** 30, 8 * 2 ** 30, 1, 1, 0)' in host_controls)
check('normal host zeroextraargv retained', 'len(sys.argv) != 1' in host_main)
check('actual merged streams honest unchanged false separatecaptures', 'independent_child_stdout_captured=False' in host_main and 'independent_child_stderr_captured=False' in host_main)
check('complete Source namespace before/after full equality retained', 'source_after != source_before' in host_main and source(hraw, hd['_source_namespace']) == source(phraw, phd['_source_namespace']))
for field in ('actual_success_pins', 'UNKNOWN_Q', 'UNKNOWN_BUSINESS_PINS'):
    check('manifest unknown future pin None: ' + field, manifest[field] is None)
for field in ('runtime_executed', 'old_v21_namespaces_modified', 'old_0057_a459_packages_modified', 'helper_guard_business_API_called', 'current_graph_payload_read', 'install_witness_read', 'ART_directory_read', 'helper_metadata_qualified', 'whole_business_INPUT', 'native', 'AAA', 'ABA', 'physics_balance', 'actual_RSS_compliance_proven'):
    check('manifest honest Source-only false: ' + field, manifest[field] is False)
author_review = all_metadata['ORACLE_SOURCE_REVIEW.json']
check('author148checks typedtrue only Source', len(author_review['checks']) == 148 and all(type(x['value']) is bool and x['value'] is True for x in author_review['checks']) and author_review['source_only'] is True and author_review['UNKNOWN_Q'] is None and author_review['actual_success_pins'] is None)

# Re-read every reviewed member to full EOF after all AST/proof work. No ART glob.
for pin in list(source_pins):
    _, afterpin = read(Path(pin['path']), pin['sha256'], pin['identity'])
    check('complete reviewed SOURCE/META before-after stable: ' + pin['path'], afterpin == pin)
check('sealed full inventory and package directory7ID unchanged', sorted(p.name for p in PACKAGE.iterdir()) == names_before and ident(PACKAGE) == package_before)

def count_definitions(tree):
    return {'top_functions': sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in tree.body), 'all_function_nodes': sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(tree)), 'top_classes': sum(isinstance(n, ast.ClassDef) for n in tree.body), 'all_class_nodes': sum(isinstance(n, ast.ClassDef) for n in ast.walk(tree))}

report = {
    'schema': 'AXMAT_V21B_INDEPENDENT_FULL_OLD_CONSTRUCTOR_ORACLE_SOURCE_REVIEW_V1',
    'status': 'SOURCE_PASS_FOR_ROOT_METADATA_BINDING_ONLY_NOT_RUNTIME_QUALIFICATION',
    'source_only': True, 'checks': checks, 'all_checks_typed_true': True, 'blockers': [],
    'author_sealed_manifest': manifest_pin, 'author_package_directory_identity_before_after': package_before,
    'complete_author_member_count': 27, 'complete_author_member_bytes': 371881,
    'complete_author_member_pins_before_after': member_pins,
    'all_reviewed_Source_META_pins_before_after': source_pins[:len(source_pins)//2],
    'driver': member_pins['fresh_verifier_controls.v21b.READY_SOURCE.py'],
    'host': member_pins['fresh_verifier_host.v21b.READY_SOURCE.py'],
    'binder': member_pins['bind_fresh_verifier_sources.py'],
    'full_inverse_evidence': inverses,
    'actual_definition_inventory': {'previous_driver': count_definitions(pdt), 'candidate_driver': count_definitions(dt), 'previous_host': count_definitions(pht), 'candidate_host': count_definitions(ht), 'binder': count_definitions(bt), 'old_helper_Source': count_definitions(parse(oldraw)), 'new_helper_Source': count_definitions(parse(newraw))},
    'unchanged_driver_function_names': unchanged_driver, 'unchanged_host_function_names': list(hd),
    'entire_public27field_order': public_fields, 'original_reader10key_order': reader_keys,
    'original_coverage9category_order': list(categories), 'original_coverage3nested_key_order': dict_keys(old_inner[0]), 'original_trace10key_order': trace_keys,
    'complete_old_public_return_AST': dump(old_return), 'complete_new_public_return_AST': dump(new_return),
    'complete_original_reader_constant_AST': dump(og['FRESH_READER_CONTRACT']),
    'complete_original_coverage_inner_constructor_AST': dump(old_inner[0]),
    'complete_original_trace_counts_constructor_AST': dump(old_counts),
    'complete_candidate_oracle_constructor_SOURCE': source(draw, constructor),
    'value_type_order_review': 'Only original three public constructors restore their original insertion order. Every stored coverage/trace value is carried unconverted with complete keyset/equality gates. The unchanged exact_value then checks every actual nested builtin type, mapping insertion order, list length/order, scalar and IEEE754 float bits. Complete typed_snapshot is retained with its original stored nested order. No new helper is used as oracle; no helper constructor was executed during this review.',
    'qualification_limits': ['SOURCE pass permits Root metadata binding and finite actual Source mechanical review only.', 'No real 600-second complete verifier result, 60-second pure protocol qualification, new Q, business INPUT/build/native/AAA/ABA/physics qualification is created.', 'Host has original after and final joint HOST+OUT+D+E64MiB checks, not a separate before joint archive measurement; Root must preserve actual external prelaunch fullD+E count and H/OUT absence.', 'The failed v21 run is frozen and contributes no qualification or successful future pins.', 'No line-level RSS cause or future pass is inferred.'],
    'helper_or_guard_API_executed': False, 'candidate_driver_host_binder_executed': False,
    'graph_ART_numeric_payload_read': False, 'install_witness_payload_read': False,
    'canonical_project_D_E_or_results_written': False, 'ART_directory_globbed': False,
    'actual_success_pins': None, 'UNKNOWN_Q': None, 'UNKNOWN_BUSINESS_PINS': None,
    'helper_metadata_qualified': False, 'whole_business_INPUT_qualified': False,
    'native_RSS_qualified': False, 'AAA_accuracy_qualified': False, 'ABA_admitted': False, 'physical_balance_qualified': False,
}
with (OUT / 'INDEPENDENT_REVIEW.json').open('x') as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write('\n')
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps({'status': report['status'], 'checks': len(checks), 'blockers': [], 'author_manifest_sha256': MANIFEST_SHA, 'complete_members': 27, 'member_bytes': 371881, 'driver_sha256': hashlib.sha256(draw).hexdigest(), 'host_sha256': hashlib.sha256(hraw).hexdigest(), 'report_path': str(OUT / 'INDEPENDENT_REVIEW.json'), 'report_sha256': hashlib.sha256((OUT / 'INDEPENDENT_REVIEW.json').read_bytes()).hexdigest(), 'source_only': True, 'API_executed': False, 'UNKNOWN_Q': None}, allow_nan=False))
