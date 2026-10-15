"""Evaluate real metadata gates and exact inverse/target contracts before MF."""
import ast
import hashlib
import importlib.util
import json
import os
import stat
import sys
from pathlib import Path


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(p):
    p = Path(p);s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_size <= 64 * 2**20
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        assert identity(os.fstat(f.fileno())) == identity(s)
        b = f.read()
        assert identity(os.fstat(f.fileno())) == identity(s)
    assert identity(p.lstat()) == identity(s)
    return dict(path=str(p), sha256=hashlib.sha256(b).hexdigest(), size_bytes=len(b), identity=identity(s))


def exact(p):
    assert pin(p['path']) == p
    return Path(p['path']).read_bytes()


def segment(b, name):
    text = b.decode();node = next(n for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    return ast.get_source_segment(text, node)


def main():
    sfpath, destination = map(Path, sys.argv[1:])
    assert not destination.exists()
    sfpin = pin(sfpath);sf = json.loads(exact(sfpin))
    assert sf['manifest_prepared'] is False and sf['deletion_executed'] is False
    inverse = json.loads(exact(sf['strict_low_level_Source_provenance_pin']))
    assert len(inverse['entries']) == 3
    methods = ['_base', 'external', 'inventory', 'receipt_pin', 'update_owned', 'budget', 'review_gate']
    assert inverse['seven_lowlevel_methods_wholebytes_equal'] == methods
    inverses = []
    for entry in inverse['entries']:
        old = exact(entry['predecessor_pin']);new = exact(entry['candidate_pin']);back = new.decode()
        for change in reversed(entry['changes']):
            assert back.count(change['after']) == 1
            back = back.replace(change['after'], change['before'], 1)
        assert back.encode() == old
        ast.parse(new)
        if Path(entry['candidate_pin']['path']).name == 'literal11_release_common.py':
            assert all(segment(old, n) == segment(new, n) for n in methods)
        inverses.append(dict(candidate=entry['candidate_pin'],whole_inverse=True,changes=len(entry['changes'])))
    common = sfpath.parent / 'literal11_release_common.py'
    spec = importlib.util.spec_from_file_location('Root_literal11_A8_real_Source_review', common)
    c = importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
    assert c.pin(sfpath) == sfpin
    c.source_gate(sfpin)
    c.disjoint([])
    facts = c.closed_proofs()
    assert len(c.TARGETS) == len(c.TARGET_PATHS) == len(c.TARGET_SELECTED_PINS) == 2
    assert sum(p['size_bytes'] for p in c.TARGET_SELECTED_PINS) == 463397752
    assert len(c.ROLE_KEEP_PINS) == 9
    text = common.read_text();fn = next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == 'disjoint')
    guard = next(n for n in fn.body if isinstance(n, ast.If)).test
    code = compile(ast.Expression(guard), str(common), 'eval')
    env = dict(c.__dict__)
    assert eval(code, env) is False
    negative = dict(env);negative['TARGETS'] = c.TARGETS[:-1];assert eval(code, negative) is True
    negative = dict(env);negative['TARGET_PATHS'] = set(list(c.TARGET_PATHS)[:-1]);assert eval(code, negative) is True
    for _ in range(2):
        nodes = []
        for p in c.TARGET_SELECTED_PINS + c.ROLE_KEEP_PINS:
            s = Path(p['path']).lstat()
            assert identity(s) == p['identity'] and stat.S_ISREG(s.st_mode) and s.st_uid == os.getuid() and s.st_nlink == 1
            nodes.append((s.st_dev, s.st_ino))
        assert len(nodes) == len(set(nodes)) == 11
    report = dict(schema='ROOT_LITERAL2_OLD_MAP005006_SOURCE_ONLY_REVIEW_V1',status='PASS_LITERAL2_OLD_MAP005006_SOURCE_ONLY_REVIEW',failure=None,Source_freeze_pin=sfpin,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False,whole_original_three_script_inverses=inverses,seven_low_level_methods_whole_bytes_equal=methods,actual_source_gate_and_closed_proofs_pure_readonly_passed=True,actual_closed_authority_count=len(facts),actual_disjoint_first_guard_AST_evaluated_with_current2_and_returned_false=True,actual_disjoint_missing_target_count_and_missing_path_count_negatives_rejected=True,actual_guard_Source=ast.unparse(guard),targets_and9_retained_current7_UID_singlelink_twice=True,target_count=2,target_logical_bytes=463397752,manifest_or_execute_not_run=True)
    with destination.open('x') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(review_pin=pin(destination),target_count=2,actual_closed_authority_count=len(facts),business_executed=False,deletion_executed=False)))


if __name__ == '__main__':
    main()
