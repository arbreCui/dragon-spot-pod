"""Generate the full pure mother candidate and byte-derived 67-fixture Source."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import textwrap

ROOT = Path('/Users/wen/spot')
OUT = Path(__file__).resolve().parent
BASIS = OUT/'preserved_source_basis'
CANDIDATE = OUT/'candidate_source'
assert not CANDIDATE.exists()


def pin(path):
    path = Path(path)
    before = path.lstat()
    ids = [before.st_dev, before.st_ino, before.st_mode, before.st_nlink,
           before.st_size, before.st_mtime_ns, before.st_ctime_ns]
    assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1
    with path.open('rb') as f:
        a = os.fstat(f.fileno())
        assert ids == [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
        data = f.read()
        a = os.fstat(f.fileno())
        assert ids == [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
    a = path.lstat()
    assert ids == [a.st_dev,a.st_ino,a.st_mode,a.st_nlink,a.st_size,a.st_mtime_ns,a.st_ctime_ns]
    assert len(data) == before.st_size
    return dict(path=str(path), size_bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), identity=ids)


def put(path, data):
    with Path(path).open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def defs(data):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(data).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}


source = BASIS/'V25_PURE_MOTHER_NOT_RECOVERED_NEW6A_PURE.py'
source_pin = pin(source)
assert source_pin['sha256'] == '6ac338e3f54523210f81c1226c0954f86d047bad8e90af1ecaec539b796058cc'
before = source.read_text()
after = before
changes = []
for old, new in [
    ("SOURCE_STATUS = 'READY_SOURCE_BOUND_BY_ROOT'", "SOURCE_STATUS = 'UNREADY_CURRENT_ROOT_PURE_BINDING_REQUIRED'"),
    ("HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'", "HELPER_PATH = '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py'"),
    ("HELPER_SHA256 = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'", "HELPER_SHA256 = '6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'"),
    ('HELPER_SOURCE_BYTES = 150986', 'HELPER_SOURCE_BYTES = 152950'),
    ("AUDIT_CONTROL_PATH = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v25_sources/inactive_audit_snapshot_controls_SOURCE_ONLY.py'", 'AUDIT_CONTROL_PATH = '+repr(str(BASIS/'ORIGINAL_COMPLETE_INACTIVE_SNAPSHOT_CONTROLS.py'))),
]:
    assert after.count(old) == 1
    after = after.replace(old, new)
    changes.append(dict(exact_before=old, exact_after=new, count=1))
inverse = after
for change in reversed(changes):
    assert inverse.count(change['exact_after']) == 1
    inverse = inverse.replace(change['exact_after'], change['exact_before'])
assert inverse == before
assert defs(after) == defs(before)
ast.parse(after)
CANDIDATE.mkdir(mode=0o700)
mother = CANDIDATE/'pure_helper_controls_NEW_EPOCH_CANDIDATE.py'
put(mother, after.encode())

wire_source = BASIS/'ORIGINAL_BOUNDED_COMPLETE_WIRE67_CONTROLLER.py'
wire_pin = pin(wire_source)
assert wire_pin['sha256'] == '09cbab061de6c3c28f6268bf88a6f3e1fcd4f5ff428cf5fd3d955e1cac87e5b3'
wire = wire_source.read_text()
tree = ast.parse(wire)
selected = {'GuardViolation', 'typed', 'identities', 'TaggedStr', 'Reiterable',
            'RowList', 'RowTuple', 'state', 'attempt'}
segments = [ast.get_source_segment(wire, n) for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in selected]
assert len(segments) == len(selected)
start = wire.index("    base=('/pure/control/a'")
end = wire.index("    result['fixture_results']=fixture_results", start)
fixture_block = textwrap.dedent(wire[start:end]).rstrip()
new_wire = ('"""All original 67 tiny-data fixtures; full real-edge run is separate."""\n'
            'import inspect,json,struct\nfrom pathlib import PurePosixPath\nevents=[]\n\n'
            + '\n\n'.join(segments)
            + '\n\ndef wire_fixture_controls(old,new):\n'
            + textwrap.indent(fixture_block, '    ')
            + '\n    assert len(fixture_results)==67\n'
            + "    assert sum(r['original_complete_evidence']['outcome']['kind']=='return' for r in fixture_results)==14\n"
            + "    assert sum(r['original_complete_evidence']['outcome']['kind']=='raise' for r in fixture_results)==53\n"
            + '    return fixture_results\n')
ast.parse(new_wire)
new_tree = ast.parse(new_wire)
for node in new_tree.body:
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in selected:
        original = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == node.name)
        assert ast.dump(node, include_attributes=False) == ast.dump(original, include_attributes=False)
generated_wire = CANDIDATE/'wire67_original_fixture_definitions.py'
put(generated_wire, new_wire.encode())

index_source = OUT/'NEW_EPOCH_DATA_SUPPLEMENTS.py'
ast.parse(index_source.read_bytes())
fixed = [pin(source), pin(wire_source), pin(index_source), pin(__file__)]
report = dict(schema='SPOT_NEW_EPOCH_PURE_CANDIDATE_DERIVATION_ONLY_V1',
              status='FULL_PURE_MOTHER_CANDIDATE_AND_ALL67_TINY_WIRE_FIXTURES_GENERATED_NOT_Q',
              original_mother=source_pin, new_full_mother_candidate=pin(mother),
              exact_changes=changes, whole_source_inverse_bytes_equal=True,
              every_original_top_level_function_and_class_AST_equal=True,
              all_original_five_full_pure_stages_and_assertions_retained=True,
              original_60s_512MiB_64MiB_onechild_retry0_limits_retained=True,
              new67_fixture_source=pin(generated_wire), original67_fixture_source=wire_pin,
              all_selected_definitions_AST_equal=True,
              full_original67_fixture_construction_and_assertion_block_retained=True,
              new_synthetic_index_source=pin(index_source), fixed_current_Source_inputs=fixed,
              full_protocol_requires_current_Root_binding=True,
              remaining_original_added_control_gaps=[
                  'Original7ae399/c3a81/f133f lost Sources were not recovered byte exactly; new Source must be reviewed as new.',
                  'Full original saved graph and63379 trace roundtrip are preserved but not executed in the small-data run.',
                  'Original real Popen same-observation nine-field/private snapshot controls are preserved but not executed under no-process recovery authorization.',
                  'Original238780 whole wire rows/full wire EOF equality and current fresh-observation binding remain to be performed or explicitly historically bound.',
                  'Current whole input including all480 absence inputs and all27 fresh return fields needs actual new whole-input fresh verification.',
                  'Original OwnRSS host, complete current history/fresh/free ledger and genuine external Root/peer closure remain required before Q.',
              ],
              new_Q_created=False, protocol_executed=False, whole_INPUT_admitted=False,
              science_or_BOOT_admitted=False)
for wanted in fixed:
    assert pin(wanted['path']) == wanted
put(OUT/'NEW_EPOCH_CANDIDATE_DERIVATION.json',
    (json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False)+'\n').encode())
print(json.dumps(dict(status=report['status'], candidate=pin(mother),
                      wire67_source=pin(generated_wire),
                      proof=pin(OUT/'NEW_EPOCH_CANDIDATE_DERIVATION.json'),
                      every_original_definition_AST_equal=True,
                      protocol_executed=False, new_Q_created=False)), flush=True)
