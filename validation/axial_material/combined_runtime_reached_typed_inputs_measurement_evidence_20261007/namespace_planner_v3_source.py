"""Read-only typed namespace planning. No API, graph admission or payload scan."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
DECL = ART / 'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
DECL_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
HELPER = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
assert hashlib.sha256(HELPER.read_bytes()).hexdigest() == 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
spec = importlib.util.spec_from_file_location('actual_namespace_plan_strict_metadata_reader', HELPER)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
d = g.strict_json(str(DECL), DECL_SHA)


def literal_expression(node, names):
    # Parse documented literal path assignments; never execute a project module
    # or guess a SOURCE directory by rewriting an OUT family name.
    if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, bool)):
        return node.value
    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left = literal_expression(node.left, names)
        right = literal_expression(node.right, names)
        if isinstance(left, Path) and isinstance(right, str):
            return left / right
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'Path' and len(node.args) == 1 and not node.keywords:
        value = literal_expression(node.args[0], names)
        if isinstance(value, str):
            return Path(value)
    raise ValueError('nonliteral path expression')


registry = {}
source_bindings = []
for path, wanted in d['files'].items():
    p = Path(path)
    if p.parent != ROOT / 'validation/axial_material' or not p.name.startswith('prepare_') or p.suffix != '.py':
        continue
    # Expected SHA comes from the actual immutable declaration, never this read.
    g.strict_pin(path, wanted)
    text = p.read_text()
    assert hashlib.sha256(text.encode()).hexdigest() == wanted
    tree = ast.parse(text)
    values = {'ROOT': ROOT, 'ART': ART}
    assignments = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        try:
            value = literal_expression(node.value, values)
        except ValueError:
            continue
        if name in ('ROOT', 'ART'):
            assert value == values[name]
        values[name] = value
        assignments[name] = ast.get_source_segment(text, node)
    if isinstance(values.get('OUT'), Path) and isinstance(values.get('SOURCE'), Path):
        key = str(values['OUT'])
        binding = {'source_file': path, 'source_sha256': wanted,
                   'OUT': str(values['OUT']), 'SOURCE': str(values['SOURCE']),
                   'source_OUT_assignment': assignments['OUT'],
                   'source_SOURCE_assignment': assignments['SOURCE'],
                   'project_module_executed': False}
        if key in registry:
            assert registry[key]['SOURCE'] == binding['SOURCE'], 'ambiguous literal SOURCE binding'
        registry[key] = binding
        source_bindings.append(binding)

requirements = []
unresolved = []
metadata_pins = []


def inventory_requirement(document, pointer, root, inventory, source_binding=None):
    assert isinstance(inventory, dict)
    assert set(inventory) <= {'files', 'symlinks', 'directories'}
    assert isinstance(inventory.get('files'), dict)
    assert isinstance(inventory.get('symlinks'), dict)
    root = Path(root)
    assert root.is_absolute() and '..' not in root.parts
    for relative, expected in inventory['files'].items():
        g._relative(relative)
        g._sha(expected)
    for relative, literal in inventory['symlinks'].items():
        g._relative(relative)
        assert isinstance(literal, str) and literal
    if 'directories' in inventory:
        assert isinstance(inventory['directories'], list)
        for relative in inventory['directories']:
            g._relative(relative)
    members = {str(root / relative): expected for relative, expected in inventory['files'].items()}
    conflicts = {path: (wanted, d['files'][path]) for path, wanted in members.items()
                 if path in d['files'] and d['files'][path] != wanted}
    assert not conflicts, 'conflicting typed namespace and baseline expected SHA'
    requirements.append(dict(owner=document + '#' + pointer, root=str(root), inventory=inventory,
        literal_SOURCE_binding=source_binding,
        current_namespace_scanned=False, current_regular_payloads_hashed=False,
        expected_regular_members=len(members),
        expected_members_already_in_baseline=sum(path in d['files'] for path in members),
        expected_regular_members_missing_from_baseline={path: sha for path, sha in members.items() if path not in d['files']},
        old_expected_empty_directory_contract_present='directories' in inventory,
        old_literal_alias_count=len(inventory['symlinks']),
        all_original_logical_owners_retained=True))


documents = [(str(DECL), d, DECL_SHA)]
for path, wanted in d['files'].items():
    p = Path(path)
    if p.is_relative_to(ART) and p.name == 'declaration.json':
        documents.append((path, g.strict_json(path, wanted), wanted))
for document, obj, wanted in documents:
    metadata_pins.append(dict(path=document, sha256=wanted))
    for field in ('preserved_predecessors', 'component_namespaces', 'memory_component_namespaces', 'dedup_component_namespaces'):
        if field not in obj:
            continue
        assert isinstance(obj[field], list)
        for index, entry in enumerate(obj[field]):
            assert isinstance(entry, dict) and 'root' in entry and 'inventory' in entry
            inventory_requirement(document, '/' + field + '/' + str(index), entry['root'], entry['inventory'])
    if 'source_inventory' in obj:
        root = obj.get('source_root')
        binding = None
        if root is None:
            binding = registry.get(str(Path(document).parent))
            root = None if binding is None else binding['SOURCE']
        if root is None:
            unresolved.append(dict(document=document, pointer='/source_inventory',
                reason='No explicit source_root or pinned literal factory OUT/SOURCE binding; never guess'))
        else:
            inventory_requirement(document, '/source_inventory', root, obj['source_inventory'], binding)

def inventory_conflicts(requirements):
    roots = {}
    first_field_owner = {}
    differences = []
    conflicts = []
    for entry in requirements:
        root, current = entry['root'], entry['inventory']
        if root not in roots:
            roots[root] = current
        elif roots[root] != current:
            differences.append(dict(root=root, owner=entry['owner'],
                earlier_fields=sorted(roots[root]), current_fields=sorted(current)))
        for key, value in current.items():
            token = (root, key)
            if token not in first_field_owner:
                first_field_owner[token] = (entry['owner'], value)
            else:
                earlier_owner, earlier_value = first_field_owner[token]
                if earlier_value != value:
                    conflicts.append(dict(root=root, field=key,
                        earlier_owner=earlier_owner, current_owner=entry['owner'],
                        original_snapshots_not_unioned=True))
    # first_field_owner is comparison provenance only. Every original inventory
    # and its absent/present field shape remains in the original requirements.
    return roots, differences, conflicts


roots, inventory_representation_differences, unresolved_inventory_conflicts = inventory_conflicts(requirements)
result = dict(schema='AXMAT_COMBINED_RUNTIME_SOURCE_BOUND_TYPED_NAMESPACE_METADATA_PLAN_V1',
    scope='METADATA_PLANNING_ONLY_NOT_COMPLETE_COMPONENT_PREDICATE_OR_INPUT_ADMISSION',
    declaration=dict(path=str(DECL), sha256=DECL_SHA),
    literal_factory_SOURCE_OUT_bindings=source_bindings, metadata_pins=metadata_pins,
    logical_namespace_requirements=requirements,
    logical_namespace_requirement_count=len(requirements), distinct_namespace_roots=len(roots),
    distinct_expected_regular_paths=len({str(Path(root) / p) for root, inv in roots.items() for p in inv['files']}),
    unresolved_SOURCE_bindings=unresolved,
    inventory_representation_differences=inventory_representation_differences,
    unresolved_inventory_conflicts=unresolved_inventory_conflicts,
    baseline_full_26784_file_map_must_remain_unfiltered=True,
    actual_API_call_graph_reachability_audited=False,
    raw_receipt_and_dynamic_glob_namespaces_not_enumerated=True,
    current_full_namespace_membership_and_payload_not_verified=True,
    original_component_APIs_executed=False, component_implicit_dependency_closure_proved=False,
    complete_parent_predicate_replacement_proved=False, scientific_qualification_created=False,
    combined_runtime_admitted=False, AAA_accuracy_qualified=False, ABA_admitted=False)
out = Path('/private/tmp/combined_runtime_declared_namespace_metadata_plan_v3_result_20261007.json')
with out.open('x') as f:
    json.dump(result, f, indent=2, allow_nan=False)
    f.write('\n')
print(json.dumps({key: result[key] for key in ('schema', 'logical_namespace_requirement_count',
    'distinct_namespace_roots', 'distinct_expected_regular_paths', 'unresolved_SOURCE_bindings', 'unresolved_inventory_conflicts')}))
print('result_sha256', hashlib.sha256(out.read_bytes()).hexdigest())
