import ast
import hashlib
import json
import os
import stat
from pathlib import Path

BASE = Path('/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4')
OUT = Path('/private/tmp/Root_v27_independent_source_review_20261011.json')
seen = {}

def pin_check(pin):
    path = Path(pin['path'])
    s = path.lstat()
    identity = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1, str(path)
    if 'identity' in pin:
        assert identity == pin['identity'], str(path)
    if 'size_bytes' in pin:
        assert s.st_size == pin['size_bytes'], str(path)
    h = hashlib.sha256()
    count = 0
    with path.open('rb') as f:
        before = os.fstat(f.fileno())
        assert [before.st_dev,before.st_ino,before.st_mode,before.st_nlink,before.st_size,before.st_mtime_ns,before.st_ctime_ns] == identity
        while True:
            block = f.read(2**20)
            if not block:
                break
            h.update(block)
            count += len(block)
        after = os.fstat(f.fileno())
        assert [after.st_dev,after.st_ino,after.st_mode,after.st_nlink,after.st_size,after.st_mtime_ns,after.st_ctime_ns] == identity
    assert count == s.st_size and h.hexdigest() == pin['sha256'], str(path)
    final = path.lstat()
    assert [final.st_dev,final.st_ino,final.st_mode,final.st_nlink,final.st_size,final.st_mtime_ns,final.st_ctime_ns] == identity
    seen[str(path)] = dict(path=str(path), sha256=h.hexdigest(), size_bytes=count, identity=identity)

def walk(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('sha256'), str):
            pin_check(value)
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

def definitions(source):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(source).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

contract = json.loads((BASE/'SOURCE_ONLY_CONTRACT.json').read_text())
declaration = json.loads((BASE/'SOURCE_FAMILY_DECLARATION.json').read_text())
derivation = json.loads((BASE/'SOURCE_DERIVATION_FULL_INVERSE.json').read_text())
manifest = json.loads((BASE/'FINAL_REVIEW_EVIDENCE_MANIFEST.json').read_text())
for value in (contract, declaration, derivation, manifest):
    walk(value)
inverses = []
for name, record in derivation['files'].items():
    old = Path(record['original_source']['path']).read_bytes()
    new = Path(record['new_source']['path']).read_bytes()
    restored = new.decode()
    for change in reversed(record.get('changes', [])):
        assert restored.count(change['exact_after']) == change['count'], name
        restored = restored.replace(change['exact_after'], change['exact_before'])
    assert restored.encode() == old, name
    before, after = definitions(old), definitions(new)
    assert set(before) == set(after), name
    changed = [key for key in before if before[key] != after[key]]
    assert changed == record.get('changed_top_level_definitions', []), (name, changed)
    inverses.append(dict(file=name, byte_exact_original_reconstruction=True, changed_definitions=changed))
for source_pin in contract['new_sources'].values():
    ast.parse(Path(source_pin['path']).read_bytes())
assert contract['caps'] == dict(whole_seconds=60,stage_seconds=60,rss_bytes=512*2**20,output_archive_bytes=64*2**20,threads=1,children_at_once=1,retries=0)
assert contract['original_artifact_budget_bytes'] == 96*2**30
assert contract['original_min_free_bytes'] == 8*2**30
assert contract['execution_environment_requires_escalated_for_original_supervisor_own_worker_child_PS_only'] is True
for key in ('host_namespace','output_namespace'):
    assert not os.path.lexists(contract[key]), key
host = Path(declaration['host_source']['path']).read_text()
assert 'WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=60,60,512,64*2**20' in host
assert "runner=full.OwnRSSSerialExecutor(HOST,remaining,'GRAPH_PROTOCOL_CONTROLS',resources)" in host
assert "whole_family_memory_pass=False" in host and "new_Q_created=False" in host
expected_command = ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(BASE/'sources/pure_helper_controls_host.py')]
assert declaration['command'] == expected_command
for pin in list(seen.values()):
    pin_check(pin)
result = dict(status='ROOT_SOURCE_REVIEW_PASS_AUTHORIZE_ONE_PURE_PROTOCOL_EXECUTION',
              source_inverse_checks=inverses, full_EOF_pins_before_after=list(seen.values()),
              command=expected_command, host_and_output_absent=True, no_source_imported=True,
              no_host_executed=True, no_new_Q=True, whole_memory_pass=False, science_admitted=False)
with OUT.open('x') as f:
    json.dump(result, f, indent=2, allow_nan=False)
    f.write('\n')
print(json.dumps(dict(status=result['status'], pins=len(seen), inverse_files=len(inverses),
                      report=str(OUT), report_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest())))
