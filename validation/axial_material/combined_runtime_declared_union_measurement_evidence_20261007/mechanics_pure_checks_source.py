"""Disposable real filesystem checks. No project API/native/artifact execution."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile

SOURCE = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
SOURCE_SHA = 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
spec = importlib.util.spec_from_file_location('actual_combined_graph_mechanics_pure_checks', SOURCE)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
positive = []
negative = []


def rejected(name, fn):
    try:
        fn()
    except (g.InputGraphError, ValueError, OSError):
        negative.append(name)
    else:
        raise AssertionError('negative input accepted: ' + name)


with tempfile.TemporaryDirectory(prefix='combined-graph-mechanics-pure-') as temporary:
    root = Path(temporary).resolve()
    data = root / 'owned'
    data.mkdir()
    (data / 'empty').mkdir()
    a = data / 'a.bin'
    b = data / 'b.bin'
    a.write_bytes(bytes.fromhex('00000000000000000000000000000080'))
    b.write_bytes(b'complete other input\n')
    sha_a = hashlib.sha256(a.read_bytes()).hexdigest()
    sha_b = hashlib.sha256(b.read_bytes()).hexdigest()
    alias = root / 'alias.bin'
    alias.symlink_to('owned/a.bin')
    aliases = g.capture_aliases([str(alias)])
    owners = [{'owner': 'actual disposable owner ' + category,
               'category': category, 'expected_files': {str(a): sha_a}}
              for category in g.CLOSURE_CATEGORIES]
    owners.append({'owner': 'disposable alias owner', 'category': 'code_environment',
                   'expected_files': {str(alias): sha_a}})
    namespace = g.explicit_sealed_namespace(
        str(data), {'a.bin': sha_a, 'b.bin': sha_b}, {},
        owner='actual disposable exhaustive namespace', category='source_namespace',
        directories=['empty'], aliases=aliases)
    with g.ReadOpenAudit() as read:
        a.read_bytes()
        b.read_bytes()
    trace = read.snapshot()
    graph = g.create_graph(typed_snapshot={'fixture_only': True, 'science_pass': False},
                          owners=owners, namespaces=[namespace], aliases=aliases,
                          read_trace=trace,
                          declared_new_source_roots=[str(root)])
    assert graph['consumer_scope'] is None
    assert len(graph['canonical_files']) == 2
    assert len(graph['requirements']['rows']) == 12
    assert graph['science_qualification_created'] is False
    assert graph['live_resources_verified'] is False
    assert graph['external_declaration_exit0_verified'] is False
    positive.append('all logical owners and exhaustive namespace edges retain two complete canonical files')

    for phase in ('disposable_entry', 'disposable_next_phase'):
        with g.ReadOpenAudit() as actual_reads:
            verified = g.verify_graph(graph, phase=phase)
        observed = actual_reads.snapshot()
        regular = [r for r in observed['records']
                   if r['kind'] == 'path' and r['path'] in (str(a), str(b))]
        assert sum(r['attempt_count'] for r in regular) == 2, regular
        assert {r['path'] for r in regular} == {str(a), str(b)}
        assert verified['canonical_files_read'] == 2
        assert verified['actual_bytes_read'] == a.stat().st_size + b.stat().st_size
        assert verified['logical_owner_requirements'] == 12
        positive.append(phase + ': each complete canonical input read again once despite duplicate owners')

    def verify(value=graph):
        return g.verify_graph(value, phase='disposable_negative')

    before = a.stat()
    original = a.read_bytes()
    a.write_bytes(b'x' * len(original))
    os.utime(a, ns=(before.st_atime_ns, before.st_mtime_ns))
    rejected('same-size same-mtime changed input bytes', verify)
    a.write_bytes(original)
    alias.unlink()
    alias.symlink_to('owned/b.bin')
    rejected('literal alias target changed', verify)
    alias.unlink()
    alias.symlink_to('owned/a.bin')
    extra = data / 'unknown.bin'
    extra.write_bytes(b'unknown')
    rejected('added regular namespace member', verify)
    extra.unlink()
    (data / 'empty').rmdir()
    rejected('removed empty namespace directory', verify)
    (data / 'empty').mkdir()
    (data / 'new-empty').mkdir()
    rejected('added empty namespace directory', verify)
    (data / 'new-empty').rmdir()
    for field, value, name in (
        ('science_qualification_created', True, 'invented science pass'),
        ('live_resources_verified', True, 'invented current resources'),
        ('external_declaration_exit0_verified', True, 'invented Root declaration exit'),
    ):
        changed = copy.deepcopy(graph)
        changed[field] = value
        changed['content_sha256'] = g._content_digest(changed)
        rejected(name, lambda changed=changed: verify(changed))
    changed = copy.deepcopy(graph)
    changed['requirements']['rows'].pop()
    changed['content_sha256'] = g._content_digest(changed)
    rejected('lost duplicate logical edge', lambda: verify(changed))
    changed = copy.deepcopy(graph)
    changed['canonical_files'].pop()
    changed['content_sha256'] = g._content_digest(changed)
    rejected('filtered canonical file', lambda: verify(changed))
    changed = copy.deepcopy(graph)
    changed['fresh_reader_contract']['no_input_scope_or_typed_edge_filtering'] = False
    changed['content_sha256'] = g._content_digest(changed)
    rejected('weakened complete input contract', lambda: verify(changed))
    changed = copy.deepcopy(graph)
    changed['read_trace']['coverage'] = 'CLAIMED_NATIVE_COMPLETE_TRACE'
    changed['content_sha256'] = g._content_digest(changed)
    rejected('Python audit relabelled as native complete trace', lambda: verify(changed))
    raw_json = root / 'strict.json'
    for payload, name in ((b'{"a":1,"a":2}', 'duplicate JSON key'),
                          (b'{"a":NaN}', 'JSON NaN'),
                          (b'{"a":1e999}', 'JSON overflow'),
                          (b'\xff', 'invalid UTF8 JSON')):
        raw_json.write_bytes(payload)
        rejected(name, lambda: g.strict_json(str(raw_json)))
    verify()
    positive.append('original full input graph remains valid after disposable negative fixtures restored')

proof = {'schema': 'AXMAT_COMBINED_RUNTIME_GRAPH_MECHANICS_DISPOSABLE_CHECKS_V1',
         'source': {'path': str(SOURCE), 'sha256': SOURCE_SHA},
         'positive_groups': positive, 'negative_cases': negative,
         'positive_count': len(positive), 'negative_count': len(negative),
         'actual_project_APIs_executed': False, 'actual_native_children_executed': False,
         'actual_artifact_families_created': False, 'production_performance_or_RSS_proved': False,
         'scientific_qualification_created': False}
out = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_pure_checks_result_20261007.json')
with out.open('x') as stream:
    json.dump(proof, stream, indent=2, allow_nan=False)
    stream.write('\n')
print(json.dumps(proof))
print('proof_sha256', hashlib.sha256(out.read_bytes()).hexdigest())
