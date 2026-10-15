"""Typed immutable-input assembly for the reviewed readonly component chain.

This is metadata assembly, not a business factory or admission API. Historical
Root PREP anchors INPUT provenance only. Every original baseline file remains
owned. Reached declarations retain their complete literal file maps; an older
declaration outside the readonly chain is never recursively promoted.
Current namespaces, payloads, live predicates and the remaining gate closure
must be checked independently before a caller can replace any original API.
"""
import hashlib
import json
from pathlib import Path


ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
DECLARATION = ART / 'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
DECLARATION_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
ROOT_PREP = ART / 'axial-material-qualified-AB-physical-dedup-combined-runtime-build-terminal-20261007/declaration_terminal_return.json'
ROOT_PREP_SHA = '1b2956eafedde4a4fec61cd40c3f55af484678ac82abaf0db2797c05d387a280'
PLAN = Path('/private/tmp/combined_runtime_declared_namespace_metadata_plan_v3_result_20261007.json')
PLAN_SHA = '8ccd5fa775dacf4a8217596a7285bc05bfafb351e87c5ec48f01cae3c593acfe'
GATES = Path('/private/tmp/axmat_combined_runtime_source_owned_input_reuse_plan_corrected_20261007.json')
GATES_SHA = '25c62393fd026ba16ca10e8fc18aa614d3a8099a6fae9b17d17c33ef5099da90'

# Source-reviewed API reachability, not a directory prefix or filename heuristic.
REACHED = (
    ('source_factor', 'axial-material-source-factor-build-20261006', 'component_ancestry', 'AXMAT_SOURCEFACTOR_BUILD_SEAL_V1'),
    ('moment_order', 'axial-material-moment-order-build-20261006', 'component_ancestry', 'AXMAT_MOMENT_ORDER_BUILD_SEAL_V1'),
    ('original92', 'axial-material-rank1-factor-cache-build-20261007', 'original92_build', 'AXMAT_RANK1_FACTOR_CACHE_BUILD_SEAL_V1'),
    ('memory', 'axial-material-rank1-factor-cache-memory-build-20261007', 'memory_build', 'AXMAT_RANK1_FACTOR_CACHE_MEMORY_BUILD_SEAL_V1'),
    ('dedup', 'axial-material-rank1-factor-cache-memory-dedup-build-20261007', 'dedup_build', 'AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_SEAL_V1'),
    ('physical', 'axial-material-spoasm-physical-abi-serial-guarded-build-20261007', 'physical_build', 'AXMAT_SPOASM_PHYSICAL_BUILD_SEAL_V1'),
    ('capture', 'axial-material-rank1-cache-memory-dedup-file-snapshot-native-angular-capture-20261007', 'capture', 'AXMAT_RANK1_MEMORY_DEDUP_FILE_SNAPSHOT_NATIVE_ANGULAR_CAPTURE_SEAL_V1'),
    ('original_capture16f', 'axial-material-AAA-production-angular-capture-20261006', 'capture', 'AXMAT_PRODUCTION_ANGULAR_CAPTURE_SEAL_V1'),
)


def pointer_escape(value):
    return value.replace('~', '~0').replace('/', '~1')


def file_owner(g, document, pointer, category, files):
    assert isinstance(files, dict)
    return dict(owner=str(document) + '#' + pointer, category=category,
                expected_files={g._path(p): g._sha(s) for p, s in files.items()})


def descriptor_owners(g, document, value, pointer, category):
    """The exact path+sha256 descriptor form used by the original assembler.

    Never reinterpret opaque strings, bare maps, absent paths or failure flags.
    This traversal adds byte ownership only; it cannot manufacture an API body.
    """
    result = []
    if isinstance(value, dict):
        if 'path' in value and 'sha256' in value:
            result.append(file_owner(g, document, pointer, category,
                                     {value['path']: value['sha256']}))
        for key, item in value.items():
            result.extend(descriptor_owners(g, document, item,
                pointer + '/' + pointer_escape(key), category))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            result.extend(descriptor_owners(g, document, item,
                pointer + '/' + str(index), category))
    return result


def assemble_typed_input_specs(g):
    # Strict readers bind each metadata document to a prior expected SHA.
    d = g.strict_json(str(DECLARATION), DECLARATION_SHA)
    assert len(d['files']) == 26784
    prep = g.strict_json(str(ROOT_PREP), ROOT_PREP_SHA)
    assert (prep['record_producer'] == 'root'
            and prep['actual_tool_terminal_return_observed'] is True
            and prep['record_written_after_actual_terminal_return'] is True
            and type(prep['returncode']) is int and prep['returncode'] == 0
            and prep['declaration'] == dict(path=str(DECLARATION), sha256=DECLARATION_SHA)
            and prep['successful_declaration_input_observed'] is True
            and prep['successful_combined_link_completion_observed'] is False
            and prep['production_admission_observed'] is False)
    stdout = g.strict_json(prep['full_stdout']['path'], prep['full_stdout']['sha256'])
    assert stdout == dict(declaration=str(DECLARATION), declaration_sha256=DECLARATION_SHA)
    assert g.strict_pin(prep['full_stderr']['path'], prep['full_stderr']['sha256'])['size_bytes'] == 0
    plan = g.strict_json(str(PLAN), PLAN_SHA)
    gates = g.strict_json(str(GATES), GATES_SHA)
    assert not plan['unresolved_SOURCE_bindings'] and not plan['unresolved_inventory_conflicts']
    assert plan['component_implicit_dependency_closure_proved'] is False
    assert gates['scope']['new_contract_READY'] is False
    registry = {v['OUT']: v for v in plan['literal_factory_SOURCE_OUT_bindings']}
    documents = {str(DECLARATION): d}
    categories = {str(DECLARATION): 'component_ancestry'}
    owners = [file_owner(g, DECLARATION, '/files', 'component_ancestry', d['files']),
              file_owner(g, ROOT_PREP, '', 'component_terminals', {str(ROOT_PREP): ROOT_PREP_SHA}),
              file_owner(g, DECLARATION, '', 'component_ancestry', {str(DECLARATION): DECLARATION_SHA}),
              file_owner(g, PLAN, '', 'code_environment', {str(PLAN): PLAN_SHA}),
              file_owner(g, GATES, '', 'code_environment', {str(GATES): GATES_SHA})]
    owners.extend(descriptor_owners(g, ROOT_PREP, prep, '', 'component_terminals'))
    source_bindings = []
    for binding in gates['sources'].values():
        source_bindings.append(dict(path=binding['path'], sha256=binding['sha256']))
    for binding in source_bindings:
        assert d['files'][binding['path']] == binding['sha256']
    owners.append(file_owner(g, GATES, '/sources', 'code_environment',
                            {v['path']: v['sha256'] for v in source_bindings}))
    namespace_specs = []
    independent_directory_owners = []
    reached_records = []
    for label, family, category, seal_schema in REACHED:
        root = ART / family
        doc = root / 'declaration.json'
        seal_path = root / 'seal.json'
        if label == 'original_capture16f':
            # The genuine 619 inline admission supplies this literal expected
            # pin. Its declaration is NOT present in aa3e.files, so it cannot
            # acquire authority from a newly computed current digest.
            import ast
            source = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
            source_sha = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
            assert d['files'][str(source)] == source_sha
            g.strict_pin(str(source), source_sha)
            tree = ast.parse(source.read_text())
            literals = {node.targets[0].id: node.value.value for node in tree.body
                        if isinstance(node, ast.Assign) and len(node.targets) == 1
                        and isinstance(node.targets[0], ast.Name)
                        and isinstance(node.value, ast.Constant)}
            expected_doc = literals['CAPTURE_DECL_SHA']
            assert expected_doc == '6ed345f39f4ddab3299b2845877f10903f38fe89d9f9a5ebf875acadd3d3ce2b'
            assert literals['CAPTURE_SEAL_SHA'] == d['files'][str(seal_path)]
            owners.append(file_owner(g, source, '/CAPTURE_DECL_SHA', category,
                                     {str(doc): expected_doc}))
        else:
            expected_doc = d['files'][str(doc)]
        expected_seal = d['files'][str(seal_path)]
        obj = g.strict_json(str(doc), expected_doc)
        seal = g.strict_json(str(seal_path), expected_seal)
        assert seal['schema'] == seal_schema
        documents[str(doc)] = obj
        categories[str(doc)] = category
        owners.append(file_owner(g, doc, '/files', category, obj['files']))
        owners.append(file_owner(g, seal_path, '/files', category,
            {str(root / g._relative(name)): sha for name, sha in seal['files'].items()}))
        complete_files = dict(seal['files'])
        assert 'seal.json' not in complete_files
        complete_files['seal.json'] = expected_seal
        # Old file-only contracts acquire a separately identified NEW directory
        # binding when materialized; this never invents an old empty-dir PASS.
        directory_field = ('namespace_directories' if 'namespace_directories' in seal
                           else 'directories' if 'directories' in seal else None)
        namespace_specs.append(dict(owner=str(seal_path) + '#/files', root=str(root),
            category=category, expected_metadata=dict(path=str(seal_path), sha256=expected_seal),
            files=complete_files, symlinks=seal.get('symlinks', {}),
            directories=None if directory_field is None else seal[directory_field],
            old_expected_directory_field=directory_field,
            old_sealed_file_namespace_owner=True))
        for field in ('source_directories', 'source_namespace_directories'):
            if field in obj:
                source_root = obj['source_root']
                assert registry[str(root)]['SOURCE'] == source_root
                assert isinstance(obj[field], list)
                independent_directory_owners.append(dict(owner=str(doc) + '#/' + field,
                    root=source_root, directories=obj[field], expected_metadata=dict(path=str(doc), sha256=expected_doc),
                    source_inventory_shape_not_modified=True))
        reached_records.append(dict(label=label, root=str(root), category=category,
            declaration=dict(path=str(doc), sha256=expected_doc),
            seal=dict(path=str(seal_path), sha256=expected_seal),
            full_declared_file_owner_count=len(obj['files']),
            full_seal_regular_owner_count=len(seal['files'])))
    # Retain ONLY inventories read by the selected declaration chain. The V3
    # survey contains other historical declarations, which are not promoted.
    selected_requirements = [r for r in plan['logical_namespace_requirements']
                             if r['owner'].split('#', 1)[0] in documents]
    for entry in selected_requirements:
        category = ('source_namespace' if entry['owner'].endswith('#/source_inventory')
                    else categories[entry['owner'].split('#', 1)[0]])
        inv = entry['inventory']
        namespace_specs.append(dict(owner=entry['owner'], root=entry['root'], category=category,
            expected_metadata=dict(path=entry['owner'].split('#', 1)[0],
                sha256=DECLARATION_SHA if entry['owner'].split('#', 1)[0] == str(DECLARATION)
                else d['files'][entry['owner'].split('#', 1)[0]]),
            files=inv['files'], symlinks=inv['symlinks'], directories=inv.get('directories'),
            old_expected_directory_field='directories' if 'directories' in inv else None,
            literal_SOURCE_binding=entry['literal_SOURCE_binding'],
            old_logical_inventory_unchanged=True))
    aliases = []
    for doc, obj in documents.items():
        for field in ('aliases', 'input_aliases', 'native_dependency_alias_bindings'):
            for path, value in obj.get(field, {}).items():
                assert isinstance(value, dict) and set(value) <= {'text', 'target', 'sha256'}
                aliases.append(dict(owner=doc + '#/' + field + '/' + pointer_escape(path),
                    path=g._path(path), binding=value, expected_metadata=dict(path=doc,
                    sha256=DECLARATION_SHA if doc == str(DECLARATION) else d['files'][doc])))
    # Exact descriptors from the whole seven-key body are input pins; scientific
    # and failure flags remain in their unchanged historical JSON body.
    owners.extend(descriptor_owners(g, DECLARATION, d['actual_components'],
                                   '/actual_components', 'component_ancestry'))
    normalized = g._owners(owners)
    expected = {}
    conflicts = []
    for owner in normalized:
        for path, sha in owner['expected_files'].items():
            if path in expected and expected[path] != sha:
                conflicts.append(dict(path=path, earlier_sha256=expected[path], current_sha256=sha,
                                      owner=owner['owner']))
            else:
                expected[path] = sha
    assert not conflicts, 'different old expected file SHA owners cannot be merged'
    return dict(schema='AXMAT_COMBINED_RUNTIME_SOURCE_OWNED_TYPED_INPUT_SPECS_DRAFT_V1',
        classification='TYPED_REACHED_IMMUTABLE_INPUT_ASSEMBLY_NOT_API_REPLACEMENT',
        historical_prepare=dict(path=str(ROOT_PREP), sha256=ROOT_PREP_SHA),
        declaration=dict(path=str(DECLARATION), sha256=DECLARATION_SHA),
        reached_component_records=reached_records, owners=normalized,
        namespace_specs=namespace_specs, independent_directory_owners=independent_directory_owners,
        aliases=aliases, literal_factory_source_bindings=source_bindings,
        historical_actual_components=d['actual_components'],
        original_whole_seven_key_body_retained=True, baseline_file_count=len(d['files']),
        original_baseline_file_map_unchanged=True, literal_unique_expected_paths=len(expected),
        additional_literal_expected_paths={p: sha for p, sha in expected.items() if p not in d['files']},
        selected_original_inventory_count=len(selected_requirements),
        unrelated_historical_inventory_requirements_not_promoted=len(plan['logical_namespace_requirements'])-len(selected_requirements),
        unresolved_expected_SHA_conflicts=conflicts,
        source_owned_gate_contract=dict(path=str(GATES), sha256=GATES_SHA),
        unresolved_before_API_replacement=['Complete remaining raw/terminal/failure source-owned edges',
            'Fresh full byte/namespace/alias verification and retained actual read trace',
            'All independent current-only predicates and genuine bounded host handoff',
            'Independent full adapter source closure review'],
        all_original_API_predicates_accounted=False, current_bytes_and_namespaces_verified=False,
        current_live_predicates_verified=False, original_component_APIs_executed=False,
        complete_parent_predicate_replacement_proved=False, new_business_contract_READY=False,
        combined_runtime_admitted=False, combined_runtime_native_RSS_proved=False,
        scientific_qualification_created=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def main():
    import importlib.util
    helper = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
    assert hashlib.sha256(helper.read_bytes()).hexdigest() == 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
    spec = importlib.util.spec_from_file_location('readonly_typed_input_metadata_mechanics', helper)
    g = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(g)
    result = assemble_typed_input_specs(g)
    out = Path('/private/tmp/combined_runtime_source_owned_typed_input_specs_draft_20261007.json')
    with out.open('x') as stream:
        json.dump(result, stream, separators=(',', ':'), allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(owners=len(result['owners']), namespaces=len(result['namespace_specs']),
        source_directory_owners=len(result['independent_directory_owners']),
        aliases=len(result['aliases']), reached_components=len(result['reached_component_records']),
        literal_unique_expected_paths=result['literal_unique_expected_paths'],
        additional_literal_expected_paths=len(result['additional_literal_expected_paths']),
        READY=result['new_business_contract_READY'], output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())))


if __name__ == '__main__':
    main()
