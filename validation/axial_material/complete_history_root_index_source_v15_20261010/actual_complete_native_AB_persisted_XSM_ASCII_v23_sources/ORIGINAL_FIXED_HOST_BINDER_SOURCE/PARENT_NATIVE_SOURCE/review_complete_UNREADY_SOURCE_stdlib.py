"""SOURCE-only review. Never imports or executes a reviewed candidate."""
import ast
import difflib
import hashlib
import json
import stat
from pathlib import Path

P = Path(__file__).resolve().parent
CHECKS = []


def check(name, truth, detail=None):
    if type(truth) is not bool or not truth:
        raise AssertionError(name)
    CHECKS.append(dict(check=name, passed=True, detail=detail))


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    before = path.lstat()
    check('ordinary SOURCE member '+str(path), stat.S_ISREG(before.st_mode) and before.st_nlink == 1)
    raw = path.read_bytes()
    check('SOURCE full EOF stable '+str(path), identity(before) == identity(path.lstat()) and len(raw) == before.st_size)
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
                size_bytes=len(raw), identity=identity(before)), raw


def funcs(tree):
    return {n.name:ast.dump(n, include_attributes=False) for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


def assignment(tree, name):
    found = [n.value for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    check('one global '+name, len(found) == 1)
    return found[0]


def literal(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp):
        left, right = literal(node.left), literal(node.right)
        if isinstance(node.op, ast.Mult):
            return left*right
        if isinstance(node.op, ast.Pow):
            return left**right
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'dict' and not node.args:
        return {k.arg:literal(k.value) for k in node.keywords}
    raise AssertionError('unexpected Source constant form')


pins = json.loads((P/'ORIGINAL_SOURCE_PROVENANCE_PINS.json').read_bytes())['pins']
check('all35 complete original SOURCE ownership', len(pins) == 35)
for p in pins:
    original, raw = pin(Path(p['path']))
    check('original SHA/7ID unchanged '+p['path'], original == {k:p[k] for k in original})
    saved, copy = pin(Path(p['saved_source_path']))
    check('complete saved Source bytes '+p['path'], raw == copy and original['sha256'] == saved['sha256'])

versions = []
for name, sha in [('complete_native_XSM_ASCII_checker.UNREADY.py', 'e2a3879dfd9b86827177ed344527d1cb3503645166a8c4c115a9dca1722ba6be'),
                  ('complete_native_XSM_ASCII_checker_v2.UNREADY.py', '390d461a2f70d5a502731de9457e502a3211fdf7649248670467f43d48fb46fb'),
                  ('complete_native_XSM_ASCII_checker_v3.UNREADY.py', None)]:
    p, raw = pin(P/name)
    if sha is not None:
        check('preserved prior unexecuted Source SHA '+name, p['sha256'] == sha)
    tree = ast.parse(raw, filename=str(P/name))
    versions.append((p, raw, tree))
    check('UNREADY literal '+name, literal(assignment(tree, 'SOURCE_STATUS')) == 'UNREADY_SOURCE_ONLY')
    check('actual binding absent '+name, literal(assignment(tree, 'ROOT_BOUND_BINDING_SHA256')) is None)
    check('original caps '+name, literal(assignment(tree, 'CAPS')) == dict(whole_seconds=1800, stage_seconds=600,
          rss_mib=512, joint_archive_bytes=2*2**30, history_bytes=96*2**30,
          free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0))
    check('all science/RAM flags false '+name, all(v is False for v in literal(assignment(tree, 'FALSE')).values()))

prior_pin, prior_raw, prior_tree = versions[1]
current_pin, current_raw, current_tree = versions[2]
prior_lines, current_lines = prior_raw.decode().splitlines(keepends=True), current_raw.decode().splitlines(keepends=True)
hunks = []
for kind, a, b, c, d in difflib.SequenceMatcher(None, prior_lines, current_lines, autojunk=False).get_opcodes():
    if kind != 'equal':
        hunks.append(dict(old_begin_line=a, old_end_exclusive_line=b, new_begin_line=c, new_end_exclusive_line=d,
                          old_full_lines=prior_lines[a:b], new_full_lines=current_lines[c:d]))
back = current_lines[:]
for h in reversed(hunks):
    check('full new hunk exactly recorded '+str(h['new_begin_line']), back[h['new_begin_line']:h['new_end_exclusive_line']] == h['new_full_lines'])
    back[h['new_begin_line']:h['new_end_exclusive_line']] = h['old_full_lines']
check('complete v3 reverse restores unchanged v2 bytes', ''.join(back).encode() == prior_raw)
old, new = funcs(prior_tree), funcs(current_tree)
check('all16 prior functions/classes retained', len(old) == 16 and set(old) <= set(new))
unchanged = [name for name in old if old[name] == new[name]]
changed = [name for name in old if old[name] != new[name]]
check('four corrected functions changed; all12 other function AST byte-equivalent', changed == ['exact_pin', 'compare_ascii', 'evidence', 'main'] and len(unchanged) == 12)
check('only new typed pin validator', set(new)-set(old) == {'pin_shape'})

text = current_raw.decode()
imports = sorted({n.module if isinstance(n, ast.ImportFrom) else a.name for n in ast.walk(current_tree)
                  if isinstance(n, (ast.Import, ast.ImportFrom))
                  for a in ([None] if isinstance(n, ast.ImportFrom) else n.names)})
check('only stdlib imports; no business/native/guard import', imports == sorted(['argparse', 'contextlib', 'hashlib', 'itertools', 'json', 'math', 'os', 'pathlib', 're', 'sqlite3', 'stat', 'struct', 'time']))
for name, fragment in {
    'SQLite bounded8MiB cache': 'PRAGMA cache_size=-8192',
    'SQLite no mmap': 'PRAGMA mmap_size=0',
    'SQLite on disk temp': 'PRAGMA temp_store=FILE',
    'native bounded pread': 'os.pread(self.fd, min(2**20, self.size-begin), begin)',
    'ASCII bounded complete line iterator': "src.readline(2**20+1)",
    'all macro19619 records': "macro['records'] == 19619",
    'all macro19990 header-close spans': "macro['physical_headers_including_all_closes'] == 19990",
    'all macro2264113 numeric values': "macro['numeric_components'] == 2264113",
    'all370 groups': 'range(1, 371)',
    'all3 moments': 'range(3)',
    'all32fission components': '(2, 4), 8*32, read_value=False',
    'complete old fission contract256 retained': 'unchanged_old_contract_expected_fission_index_count=256',
    'REAL32 rounded+parser64 separate': "struct.pack('<fd', value, value)",
    'REAL64 complete parser bits': "struct.pack('<d', value)",
    'physical/API order separate': 'native_API_export_record_index=ordinal',
    'leading name bytes preserved': ".rstrip(b' ').decode('ascii')",
    'A then B serial': "for name in ('A', 'B'):",
    'Root genuine guard explicitly required': "binding['unchanged_genuine_host_guard_required'] is True",
    'all actual input pins fullbeforeafter': 'for p in inputs:\n        exact_pin(p)',
    'equalfloat/bool7ID rejected': 'all(type(v) is int and v >= 0 for v in expected[\'identity\'])',
    'equalfloat/bool caps rejected': "all(type(value) is int for value in binding['original_caps'].values())",
    'Source/binary linkage explicitly unqualified': 'original_native_build_binary_Source_linkage_qualified=False',
    'all long CHAR projection streamed via disk': "char_spool.read(2**20)",
    'all long projection bits bounded without new field limit': 'for begin in range(0, len(projection), 2**20):',
    'original table close consumes exact open table': "close_level in containers and containers[close_level]['kind'] == 0",
    'complete sequential list range': "index == parent['list_last_index']+1",
}.items():
    check(name, fragment in text)
check('current native source imports no mmap', 'import mmap' not in text and 'mmap.mmap' not in text)
check('no reviewed Source executed by reviewer', not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
      and n.func.id in ('exec', 'eval', 'compile', '__import__') for n in ast.walk(current_tree)))

blueprint = json.loads((P/'ROOT_BINDING_BLUEPRINT.UNREADY.json').read_bytes())
parent = json.loads((P/'SAVED_RAW_TRANSFER_PARENT_META.json').read_bytes())['rawrecord_binding']
check('all original90 parent inputs preserved in original ordered prefix', len(parent['input_pins']) == 90
      and blueprint['complete_input_pins'][:90] == parent['input_pins'])
check('all129 unique declared binding inputs retained', len(blueprint['complete_input_pins']) == 129
      and len({x['path'] for x in blueprint['complete_input_pins']}) == 129)
check('all35 complete Source pins retained in format evidence', len(blueprint['source_runtime_format_evidence']['complete_original_format_Source_pins']) == 35)
check('all original execution/admission None', all(blueprint[k] is None for k in
      ('actual_source_admission', 'actual_Root_bound_checker', 'actual_genuine_host', 'actual_run', 'actual_success')))
check('both full seven-member prior raw contracts retained', all(len(blueprint['states'][state]['saved_complete_macro']) == 7 for state in ('A','B')))

reverse = dict(schema='COMPLETE_UNEXECUTED_V3_FROM_V2_SOURCE_REVERSE_AND_AST_PROOF_V1', source_only=True,
    prior_unexecuted_checker=prior_pin, current_unexecuted_checker=current_pin,
    full_line_hunks=hunks, full_reverse_restores_prior_bytes=True,
    complete_unchanged_function_AST=unchanged, complete_changed_functions=changed,
    complete_added_functions=['pin_shape'], no_checker_execution=True,
    no_native_numeric_or_ASCII_material_payload_read=True, no_original_project_ART_or_frozen_D_E_write=True)
(P/'COMPLETE_V3_SOURCE_REVERSE_AND_AST_PROOF.json').write_text(json.dumps(reverse, indent=2)+'\n')
report = dict(schema='COMPLETE_NATIVE_XSM_ASCII_UNREADY_STDLIB_SOURCE_REVIEW_V1', source_only=True,
    candidate=current_pin, checks=CHECKS, check_count=len(CHECKS), all_checks_passed=True,
    no_candidate_import_execution=True, no_native_API_guard_transport_execution=True,
    no_native_or_numeric_material_payload_read=True, no_original_Source_R_ART_or_frozen_D_E_write=True,
    Source_review_is_not_runtime_qualification=True, RSS_qualification=None,
    actual_native_persisted_byte_comparison=None, actual_native_RAM_bits_qualification=None,
    original_native_build_binary_Source_linkage_qualified=False,
    science_qualification=False,
    remaining_actual_work=['independent complete Source review', 'Root-only separately bound checker and unchanged genuine supervisor',
        'Root actual full A/B bounded persisted native-byte comparison with all original caps',
        'truthful REAL64/CHAR/LOGICAL loss evidence if present; no repair or tolerance',
        'actual native original build/Source linkage; original RAM remains separate',
        'full isotope/region/fission/NESP and TRANC reaction semantics qualification',
        'finite150cm fully coupled370group reference and AAA8/8 before ABA'])
(P/'STATIC_SOURCE_REVIEW.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(dict(source_only=True, candidate=current_pin, checks=len(CHECKS), original_Source_count=35,
                     v3_hunks=len(hunks), unchanged_function_AST=len(unchanged), changed_function_AST=changed,
                     candidate_never_run=True, numeric_payload_never_read=True), indent=2))
