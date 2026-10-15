"""TMP-only pure function differential fixtures; no business module import.

Extract just the original validator AST and compare with the two-region
candidate on a real exclusive temporary tree. No resource class is loaded.
"""
from pathlib import Path
from itertools import product
import ast
import difflib
import hashlib
import json
import os
import random
import stat
import tempfile
import time

D = Path(__file__).parent
SOURCE = Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_moment_order_production.py')
SOURCE_SHA = 'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'

def pin(path):
    path = Path(path)
    before = path.lstat()
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    after = path.lstat()
    names = ['st_dev', 'st_ino', 'st_mode', 'st_nlink', 'st_size', 'st_mtime_ns', 'st_ctime_ns']
    identity = [getattr(before, name) for name in names]
    assert identity == [getattr(after, name) for name in names]
    return dict(path=str(path), sha256=digest, identity=identity, size_bytes=before.st_size)

def save(name, value):
    with (D/name).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')

before = pin(SOURCE)
assert before['sha256'] == SOURCE_SHA
source = SOURCE.read_text()
tree = ast.parse(source)
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'validate_history_roots')
original = ast.get_source_segment(source, node)
edits = [
    dict(old='    roots = []\n', new='    roots = []\n    overlap_trie = {}\n'),
    dict(old='        if any(path == old or path.is_relative_to(old) or old.is_relative_to(path) for old in roots):\n            raise ValueError("resource roots overlap or repeat")\n',
         new='        branch = overlap_trie\n        for part in path.parts:\n            if None in branch:\n                raise ValueError("resource roots overlap or repeat")\n            branch = branch.setdefault(part, {})\n        if branch:\n            raise ValueError("resource roots overlap or repeat")\n        branch[None] = None\n'),
]
candidate = original
for edit in edits:
    assert candidate.count(edit['old']) == 1
    candidate = candidate.replace(edit['old'], edit['new'], 1)
inverse = candidate
for edit in reversed(edits):
    assert inverse.count(edit['new']) == 1
    inverse = inverse.replace(edit['new'], edit['old'], 1)
assert inverse == original
candidate_file = D/'validate_history_roots_incremental_trie_candidate.py'
with candidate_file.open('x') as stream:
    stream.write('"""UNREADY source-only function candidate; not installed or a production resource admission."""\nfrom pathlib import Path\n\n'+candidate+'\n')
with (D/'original_validate_history_roots.py.txt').open('x') as stream:
    stream.write(original+'\n')
full_reconstructed = source.replace(original, candidate, 1)
assert full_reconstructed.replace(candidate, original, 1) == source
with (D/'minimal_original_source.patch').open('x') as stream:
    stream.write(''.join(difflib.unified_diff(source.splitlines(True), full_reconstructed.splitlines(True), fromfile=str(SOURCE), tofile='SOURCE_ONLY_NEW_NORMAL_MODULE_NOT_INSTALLED')))
original_class = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'DynamicHistoryResources')
reconstructed_tree = ast.parse(full_reconstructed)
assert ast.get_source_segment(source, original_class) == ast.get_source_segment(full_reconstructed, next(n for n in reconstructed_tree.body if isinstance(n, ast.ClassDef) and n.name == original_class.name))
old_segments = [ast.get_source_segment(source, n) for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != 'validate_history_roots']
new_segments = [ast.get_source_segment(full_reconstructed, n) for n in ast.walk(reconstructed_tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name != 'validate_history_roots']
assert old_segments == new_segments
save('source_inverse_proof.json', dict(schema='AXMAT_HISTORY_ROOTS_TWO_REGION_FUNCTION_SOURCE_INVERSE_V1', status='SOURCE_ONLY_UNREADY',
    original_source=before, original_function_lines=[node.lineno, node.end_lineno], edits=edits,
    original_function_sha256=hashlib.sha256(original.encode()).hexdigest(), candidate=pin(candidate_file),
    complete_function_inverse_exact=True, hypothetical_complete_source_inverse_exact=True,
    all_other_function_class_segments_exact=True, untouched_segment_count=len(old_segments),
    DynamicHistoryResources_and_check_body_exact=True, original_imports_globals_caps_MRO_unchanged=True,
    candidate_installed=False))

def load_function(text):
    # Sole isolated function execution explicitly authorized for TMP fixtures.
    globals_map = {'Path': Path}
    exec(compile(text, '<isolated-validator-only>', 'exec'), globals_map)
    return globals_map['validate_history_roots']

old = load_function(original)
new = load_function(candidate)

def outcome(function, values, base):
    try:
        result = function(values, base)
        assert type(result) is list and all(type(p) is type(Path('/')) for p in result)
        return dict(kind='return', value=[str(p) for p in result])
    except Exception as error:
        return dict(kind='exception', type=type(error).__module__+'.'+type(error).__qualname__,
            message=str(error), errno=getattr(error, 'errno', None), filename=getattr(error, 'filename', None),
            filename2=getattr(error, 'filename2', None))

rows = []
def check(name, values, base, message=None, expected_paths=None, exception_type=None):
    a = outcome(old, values, base)
    b = outcome(new, values, base)
    assert a == b, (name, a, b)
    if message is not None:
        assert a['kind'] == 'exception' and a['type'] == 'builtins.ValueError' and a['message'] == message, (name, a)
    if exception_type is not None:
        assert a['kind'] == 'exception' and a['type'] == exception_type, (name, a)
    if expected_paths is not None:
        assert a == dict(kind='return', value=[str(p) for p in expected_paths]), (name, a)
    rows.append(dict(name=name, outcome=a))

E = 'explicit complete-history resource roots required'
T = 'resource roots must be absolute directory paths'
P = 'resource roots must be strict validation/artifacts descendants'
S = 'resource root or ancestor is a symlink/non-directory'
O = 'resource roots overlap or repeat'
started = time.monotonic()
with tempfile.TemporaryDirectory(prefix='real_tree_', dir=D) as temporary:
    root = Path(temporary)
    base = root/'artifacts'
    base.mkdir()
    for name in ['a', 'a/inner', 'a/inner/deeper', 'b', 'c', 'other', 'other/nested']:
        (base/name).mkdir(exist_ok=True)
    (base/'file').write_bytes(b'fixture\x00finite file bytes\n')
    os.link(base/'file', base/'hardlink_file')
    assert (base/'file').stat().st_nlink == 2
    (base/'dirlink').symlink_to(base/'a', target_is_directory=True)
    (base/'dangling').symlink_to(base/'not_created', target_is_directory=True)
    (base/'self_loop').symlink_to('self_loop')
    (base/'mutual_a').symlink_to('mutual_b')
    (base/'mutual_b').symlink_to('mutual_a')
    base_alias = root/'artifacts_alias'
    base_alias.symlink_to(base, target_is_directory=True)
    outside = root/'outside'; outside.mkdir()
    class StringSubclass(str):
        pass
    core = [
        ('original_order', [str(base/'c'), str(base/'a'), str(base/'b')], base, None, [base/'c', base/'a', base/'b']),
        ('future_root', [str(base/'future/deep')], base, None, [base/'future/deep']),
        ('valid_siblings_same_text_prefix', [str(base/'a'), str(base/'ab')], base, None, [base/'a', base/'ab']),
        ('unicode_and_whitespace', [str(base/'空间'), str(base/' space ')], base, None, [base/'空间', base/' space ']),
        ('string_subclass', [StringSubclass(str(base/'b'))], base, None, [base/'b']),
        ('trailing_slash_and_dot', [str(base/'b')+'///./'], base, None, [base/'b']),
        ('resolved_base_symlink', [str(base/'b')], base_alias, None, [base/'b']),
        ('empty', [], base, E, None),
        ('not_list_none', None, base, E, None),
        ('not_list_string', str(base/'a'), base, E, None),
        ('not_list_tuple', (str(base/'a'),), base, E, None),
        ('non_string_Path', [base/'a'], base, T, None),
        ('non_string_bytes', [os.fsencode(base/'a')], base, T, None),
        ('non_string_int', [1], base, T, None),
        ('relative', ['a'], base, P, None),
        ('empty_path_string', [''], base, P, None),
        ('dotdot_inside', [str(base/'a/../b')], base, P, None),
        ('dotdot_after_future', [str(base/'future/../b')], base, P, None),
        ('equal_base', [str(base)], base, P, None),
        ('outside', [str(outside)], base, P, None),
        ('base_text_prefix_not_descendant', [str(base)+'2/a'], base, P, None),
        ('literal_base_alias_not_resolved_root', [str(base_alias/'b')], base_alias, P, None),
        ('symlink_root', [str(base/'dirlink')], base, S, None),
        ('symlink_ancestor', [str(base/'dirlink/inner/future')], base, S, None),
        ('dangling_symlink', [str(base/'dangling')], base, S, None),
        ('dangling_ancestor', [str(base/'dangling/future')], base, S, None),
        ('self_loop_root', [str(base/'self_loop')], base, S, None),
        ('mutual_loop_root', [str(base/'mutual_a')], base, S, None),
        ('file_root', [str(base/'file')], base, S, None),
        ('hardlink_file_root', [str(base/'hardlink_file')], base, S, None),
        ('file_ancestor', [str(base/'file/child')], base, S, None),
        ('duplicate', [str(base/'a'), str(base/'a')], base, O, None),
        ('duplicate_after_Path_normalization', [str(base/'a'), str(base/'a')+'/./'], base, O, None),
        ('old_ancestor', [str(base/'a'), str(base/'a/inner')], base, O, None),
        ('new_ancestor', [str(base/'a/inner'), str(base/'a')], base, O, None),
        ('overlap_precedes_later_nonstring', [str(base/'a'), str(base/'a/inner'), 1], base, O, None),
        ('nonstring_precedes_later_overlap', [str(base/'a'), 1, str(base/'a/inner')], base, T, None),
        ('bad_ancestor_precedes_overlap', [str(base/'a'), str(base/'a/inner/../../dirlink')], base, P, None),
        ('symlink_validation_precedes_overlap', [str(base/'a'), str(base/'a/inner/link')], base, None, None),
        ('non_directory_precedes_duplicate', [str(base/'file'), str(base/'file')], base, S, None),
    ]
    (base/'a/inner/link').symlink_to(base/'b', target_is_directory=True)
    for name, values, case_base, message, expected in core:
        if name == 'symlink_validation_precedes_overlap': message = S
        check(name, values, case_base, message, expected)
    check('missing_base_precedes_invalid_values', [], root/'missing_base', exception_type='builtins.FileNotFoundError')
    # Original resolves base but does not independently require it to be a
    # directory; preserve this existing behavior rather than add a new guard.
    check('original_file_base_future_descendant', [str(base/'file/future')], base/'file', expected_paths=[base/'file/future'])
    check('double_slash_anchor_original_behavior', ['/'+str(base/'a')], base)
    check('embedded_NUL_original_behavior', [str(base/'nul')+'\x00'], base)
    pool = [str(base/p) for p in ['a', 'a/inner', 'a/inner/deeper', 'ab', 'b', 'future', 'future/child', 'dirlink', 'file', 'dangling']]
    for i, values in enumerate(product(pool, repeat=2)):
        check('ordered_pair_%03d'%i, list(values), base)
    rng = random.Random(20261010)
    priority_pool = pool + [1, '', str(base), str(base/'b/..'), str(outside)]
    for i in range(256):
        check('ordered_priority_triple_%03d'%i, [rng.choice(priority_pool) for _ in range(3)], base)
    future_roots = [str(base/('future_sibling_%03d'%i)/'a'/'b') for i in range(300)]
    rng.shuffle(future_roots)
    check('300_unique_future_siblings_original_return_order', future_roots, base, expected_paths=[Path(x) for x in future_roots])
    tree_summary = dict(hardlink_nlink=2, real_existing_directories=True, real_symlinks=True,
        legal_missing_future_roots=True, separate_source_only_TEMP_tree=True, fixture_tree_removed_after_scope=True)
assert pin(SOURCE) == before
save('fixture_results.json', dict(schema='AXMAT_HISTORY_ROOTS_ISOLATED_REAL_TREE_DIFFERENTIAL_V1', status='PASS_PURE_FUNCTION_FIXTURES_ONLY',
    original_source=before, candidate=pin(candidate_file), case_count=len(rows),
    core_declared_expected_outcomes=len(core)+2, ordered_pair_count=100, deterministic_priority_triples=256,
    large_valid_future_set_count=300, fixtures=rows, real_tree=tree_summary,
    errors_exact_class_message_errno_and_filenames=True, returns_original_order_and_Path_types=True,
    elapsed_seconds=time.monotonic()-started, project_script_imported_or_executed=False,
    original_resource_class_or_check_instantiated=False, business_API_called=False,
    performance_or_whole_prepare_speedup_credit=False, native_AAA_ABA_credit=False))
print(json.dumps(dict(status='PASS_PURE_FUNCTION_FIXTURES_ONLY', cases=len(rows), candidate=pin(candidate_file),
    proof=pin(D/'source_inverse_proof.json'), fixture_report=pin(D/'fixture_results.json')), indent=2))
