#!/usr/bin/env python3
"""Finite standard-library SOURCE seal; no project import, business execution or ART read."""
import ast
import hashlib
import json
import stat
from pathlib import Path

D = Path('/private/tmp/axmat_v18_complete_combined_READY_source_binding_20261010')
def pin(p):
    p = Path(p)
    s0 = p.lstat()
    assert stat.S_ISREG(s0.st_mode) and s0.st_nlink == 1
    assert not p.is_symlink()
    assert p.resolve() == p
    b = p.read_bytes()
    s1 = p.lstat()
    fields = lambda s: [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    assert fields(s0) == fields(s1) and len(b) == s1.st_size
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'size_bytes': len(b), 'identity7': fields(s1)}
def exact(want):
    assert pin(want['path']) == want, want['path']
def reverse(t, edits):
    for e in reversed(edits):
        assert t.count(e['new']) == e['occurrences']
        t = t.replace(e['new'], e['old'])
    return t
def write_new(p, b):
    with Path(p).open('xb') as f:
        f.write(b)

proof = json.loads((D / 'source_binding_inverse_proof.json').read_bytes())
report_pin = pin(D / 'REPORT.json')
assert report_pin['sha256'] == 'a2049d14127c95cc59ebcb1fce51f9004324cfbe1b134f7ec2129e783e9101db'
assert pin(D / 'source_binding_inverse_proof.json')['sha256'] == '36bac8dcf1a640be03fe2e851d231cedfef0f7b06dc65afb8a0fb1bc6a4ae0ad'
for entry in proof['inputs']:
    assert '/validation/artifacts/' not in entry['path']
    exact(entry)
fresh_refs = []
bound_only_refs = []
for record in proof['source_qualification_references']:
    if 'actual' in record:
        entry = record['actual']
        assert '/validation/artifacts/' not in entry['path']
        exact(entry)
        fresh_refs.append(entry)
    else:
        assert record['freshly_read_in_this_source_task'] is False
        assert '/validation/artifacts/' in record['bound_by_actual_Q']['path']
        bound_only_refs.append(record)
exact(proof['candidate'])
candidate_path = Path(proof['candidate']['path'])
candidate_text = candidate_path.read_text()
assert proof['candidate']['sha256'] == '5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240'
assert len(proof['edits']) == 2
unready_text = reverse(candidate_text, proof['edits'])
unready_bytes = Path(proof['inputs'][0]['path']).read_bytes()
assert unready_text.encode() == unready_bytes
assert hashlib.sha256(unready_bytes).hexdigest() == 'ecfdff36d99aa7ea6be8fdf592e3d9ff5018b8c6aeb7604f1ef00dda1ddc3583'
def definitions(text):
    parsed = ast.parse(text)
    lines = text.splitlines(keepends=True)
    return {n.name: ''.join(lines[n.lineno - 1:n.end_lineno]) for n in parsed.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
assert definitions(candidate_text) == definitions(unready_text)
assert len(definitions(candidate_text)) == 70
compile(candidate_text, str(candidate_path), 'exec')
assert proof['future_combined_native_six_success_pins_None'] is True
actual = json.loads((D / 'actual_source_binding_tool_return.json').read_bytes())
ret = actual['actual_tool_return']
assert type(ret['exit_code']) is int and ret['exit_code'] == 0
assert ret.get('session_id') is None and ret['chunk_id'] == 'a05efa'
assert actual['source_only'] is True and actual['installed'] is False
copies = [
('/private/tmp/axmat_v18_complete_combined_READY_source_binding_generator_20261010.py', 'source_binding_generator.py', '4d54cc988d47918017bdabcf082918bf528cf0ef2a94000a7a082cec68989f0f'),
('/private/tmp/axmat_v18_ready_generator_finite_adaptation_proof_20261010.json', 'generator_source_inverse_proof.json', 'd0858cb5f72ea6d33ba5eee1921b0247a2342837e09dd76bbd42db64cdf5557e'),
('/private/tmp/axmat_v18_ready_generator_finite_adaptation_20261010.py', 'generator_source_adaptation.py', None)
]
copy_receipts = []
for src, name, expected in copies:
    before = pin(src)
    if expected is not None:
        assert before['sha256'] == expected
    b = Path(src).read_bytes()
    dst = D / name
    write_new(dst, b)
    assert pin(src) == before
    dst_pin = pin(dst)
    assert dst_pin['sha256'] == before['sha256']
    copy_receipts.append({'source': before, 'sealed_copy': dst_pin})
generator_proof = json.loads((D / 'generator_source_inverse_proof.json').read_bytes())
parent = Path(generator_proof['parent_path'])
parent_pin = pin(parent)
assert parent_pin['sha256'] == generator_proof['parent_sha256']
generator_text = (D / 'source_binding_generator.py').read_text()
assert reverse(generator_text, generator_proof['edits']).encode() == parent.read_bytes()
assert generator_proof['full_inverse_exact'] is True
for entry in proof['inputs']:
    exact(entry)
for entry in fresh_refs:
    exact(entry)
exact(proof['candidate'])
assert pin(D / 'REPORT.json') == report_pin
members = [pin(p) for p in sorted(D.iterdir())]
assert all(Path(x['path']).is_file() for x in members)
manifest = {
'schema': 'AXMAT_V18_READY_COMPLETE_COMBINED_SOURCE_BINDING_SEALED_MANIFEST_V1',
'status': 'SEALED_READY_SOURCE_BOUND_UNINSTALLED_NOT_EXECUTED',
'members': members, 'member_count': len(members),
'copy_receipts': copy_receipts, 'generator_parent_fresh_pin': parent_pin,
'source_inputs_and_SOURCE_qualification_references_fresh_full_EOF_before_after_exact': True,
'ART_qualification_references_bound_only_by_actual_Q_not_reread': bound_only_refs,
'candidate_two_edits_only': True, 'all_70_function_class_definitions_byteexact_to_ecfd': True,
'full_READY_inverse_to_ecfd_and_verified_ancestry_to_feeb_82_0ea': True,
'generator_full_inverse_to_original_V17_generator': True,
'actual_source_tool_return_integer_EXIT0_closed': True,
'future_combined_native_six_success_pins_None': True,
'installed': False, 'project_written': False, 'ART_read_or_written': False,
'project_module_imported_or_executed': False, 'numeric_payload_read': False, 'resource_check_called': False,
'new_combined_prepare_or_build_or_whole_INPUT_or_native_or_AAA_or_ABA_credit': False
}
manifest_path = D / 'sealed_manifest.json'
write_new(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode())
for entry in members:
    exact(entry)
print(json.dumps({'source_only_seal': True, 'installed': False, 'member_count': len(members),
'candidate': pin(candidate_path), 'manifest': pin(manifest_path),
'actual_source_binding_tool_return': pin(D / 'actual_source_binding_tool_return.json'),
'all_70_definitions_exact': True, 'two_candidate_edits_only': True,
'no_ART_read_or_write': True, 'business_executed': False}))
