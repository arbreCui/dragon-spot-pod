"""Current predicates for an explicitly new historical PREP INPUT reuse contract.

No original production admission or numerical control is replayed. Complete
fresh byte/namespace/alias verification remains a separate mandatory phase.
The callers supply the original complete spec and the pins actually verified
in that phase. Nothing here supplies a saved hash or stat cache.
"""
import os
from pathlib import Path
import stat


def check_member_and_directory_predicates(g, specs, aliases):
    directory_rows = []
    for row in specs['independent_directory_owners']:
        actual = g._scan_namespace(row['root'], aliases)
        assert actual['directories'] == set(row['directories'])
        directory_rows.append(dict(root=row['root'], directories=len(row['directories'])))
    member_rows = []
    for row in specs['remaining_source_owned_requirements']['negative_folder_exact_member_predicates']:
        folder = Path(row['root'])
        expected = row['expected_direct_regular_members']
        assert type(expected) is list and len(expected) == len(set(expected))
        assert set(p.name for p in folder.iterdir()) == set(expected)
        assert set(row['expected_SHA_by_member']) == set(expected)
        for name in expected:
            path = folder / name
            assert not path.is_symlink() and stat.S_ISREG(os.lstat(path).st_mode)
            assert str(path.resolve(strict=True)) == str(path)
        member_rows.append(dict(root=str(folder), direct_regular_members=len(expected)))
    assert len(directory_rows) == 3 and len(member_rows) == 79
    return dict(independent_source_directory_predicates=directory_rows,
                original_negative_exact_member_predicates=member_rows,
                original_controls_reexecuted=False)


def check_failed_lengths_and_owned_negative_bytes(g, specs, aliases, freshly_verified_pins):
    """Use only actual pins from this phase, never an earlier phase's sizes.

    A caller may supply graph canonical pins only immediately after the genuine
    verify_graph comparison of every freshly read pin with that exact table.
    """
    requirements = specs['remaining_source_owned_requirements']
    rows = requirements['failed_original_file_length_predicates']
    assert len(rows) == 4
    totals = {}
    observations = []
    for row in rows:
        total = 0
        for name, expected in row['relative_expected_sizes'].items():
            assert type(expected) is int and expected >= 0
            canonical = g._resolve(str(Path(row['root']) / name), aliases, kind='file')
            pin = freshly_verified_pins[canonical]
            assert type(pin['size_bytes']) is int and pin['size_bytes'] == expected
            total += pin['size_bytes']
        totals[row['root']] = total
        observations.append(dict(root=row['root'], files=len(row['relative_expected_sizes']), bytes=total))
    for row in rows:
        rule = row['sum_rule']
        assert type(rule['combined_source_out_bytes']) is int
        assert sum(totals[root] for root in rule['combined_sources']) == rule['combined_source_out_bytes']
    negative_edges = 0
    for row in requirements['negative_folder_exact_member_predicates']:
        for name, expected in row['expected_SHA_by_member'].items():
            canonical = g._resolve(str(Path(row['root']) / name), aliases, kind='file')
            assert freshly_verified_pins[canonical]['sha256'] == expected
            negative_edges += 1
    return dict(failed_original_length_maps=observations,
                failed_original_combined_SOURCE_OUT_sums_checked=True,
                original_negative_owned_byte_edges_checked=negative_edges,
                sizes_scope='JUST_COMPLETED_FRESH_PHASE_ONLY',
                original_controls_reexecuted=False, failed_run_success_credit=False)


def bind_namespaces(g, specs, aliases):
    namespaces = []
    for row in specs['namespace_specs']:
        links = {}
        for name, literal in row['symlinks'].items():
            actual = aliases[str(Path(row['root']) / name)]
            assert actual['text'] == literal
            links[name] = {key: value for key, value in actual.items() if key != 'path'}
        namespaces.append(g.explicit_sealed_namespace(row['root'], row['files'], links,
            owner=row['owner'], category=row['category'], directories=row['directories'],
            aliases=aliases.values()))
    assert len(namespaces) == 71
    return namespaces


def bind_aliases(g, specs, owners):
    paths = {path for owner in owners for path in owner['expected_files']}
    for row in specs['namespace_specs']:
        paths.add(row['root'])
        paths.update(str(Path(row['root']) / name) for name in row['symlinks'])
    paths.update(row['path'] for row in specs['aliases'])
    aliases = g._alias_map(g.capture_aliases(sorted(paths)))
    for row in specs['aliases']:
        actual = aliases[row['path']]
        for key, expected in row['binding'].items():
            if key == 'sha256':
                actual[key] = expected
            else:
                assert actual[key] == expected
    return aliases
