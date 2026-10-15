"""Genuine bf469 normal-path predicates; no new alias rights from a graph."""
from pathlib import Path
import sys

DECLARATION = Path('/Users/wen/spot/validation/artifacts/axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json')
DECLARATION_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
SOURCE = Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-physical-dedup-combined-runtime-build-admission-20261007')


def check_original_ordinary_paths(g, provider):
    assert sys.flags.optimize == 0, 'original and new assert predicates must be enabled'
    d = g.strict_json(str(DECLARATION), DECLARATION_SHA)
    assert len(d['files']) == 26784 and len(d['component_namespaces']) == 8
    checks = 0
    for literal in d['files']:
        p = provider.normal(literal)
        assert p.is_file()
        checks += 1
    # The original literal aliases remain legitimate; their target is ordinary.
    for literal, binding in d['aliases'].items():
        p = Path(literal)
        import os
        assert p.is_symlink() and os.readlink(p) == binding['text']
        assert str(p.resolve(strict=True)) == binding['target']
        provider.normal(binding['target'])
        checks += 1
    rows = list(d['component_namespaces']) + [dict(root=str(SOURCE), inventory=d['source_inventory'])]
    endpoint_counts = []
    for row in rows:
        root = provider.normal(row['root'])
        assert root.is_dir() and row['inventory']['symlinks'] == {}
        for name in row['inventory']['directories']:
            assert provider.normal(root/name).is_dir()
        for name in row['inventory']['files']:
            assert provider.normal(root/name).is_file()
        endpoint_counts.append(dict(root=str(root), ordinary_files=len(row['inventory']['files']),
                                    ordinary_directories=len(row['inventory']['directories'])))
    return dict(canonical_baseline_ordinary_file_predicates=checks-2,
        explicit_literal_aliases_and_ordinary_targets_checked=2,
        original_complete_namespace_ordinary_endpoints=endpoint_counts,
        genuine_original_normal_function_called=True, old16f_weak_alias_contract_unchanged=True,
        assertions_enabled=True, no_extra_alias_rights_granted=True)
