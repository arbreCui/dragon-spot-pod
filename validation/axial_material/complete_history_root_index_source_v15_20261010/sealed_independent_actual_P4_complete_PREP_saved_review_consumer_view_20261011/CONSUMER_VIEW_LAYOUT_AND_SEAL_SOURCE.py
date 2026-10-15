"""Finite byte-copy layout adapter; no candidate, utility, business or payload execution.

The top-level REVIEW is the exact already-executed 31-check report. This file
creates a consumer view and verifies its complete Source/small-META bytes.
It does not perform or claim a second saved-PREP audit.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

OLD = Path('/private/tmp/axmat_P4_ACTUAL_PREP_SAVED_Source_META_INDEPENDENT_56olj6zv')
OLD_MF_SHA = 'ef14996c8cb18bef78cdeaeedc427af7b8f62a799a18b80ea2a02165638731a7'
OLD_REPORT_SHA = 'a167790fca200ad486018b9d8199b3a8ddad531bb782cce16b650f9386681f63'
UTILITY = Path('/private/tmp/axmat_V25_memory_observation_capture_namespace_ONLY_UNREADY_Source_20261011_13_9k38l/utilities/Root_poststage_Source_META_contract.py')
LIMIT = 16 * 2**20
FIELDS = ('path', 'sha256', 'size_bytes', 'identity')
SCHEMA = 'INDEPENDENT_V25_ACTUAL_COMPLETE_PREP_SAVED_META_REVIEW_V1'
STATUS = 'PASS_ACTUAL_COMPLETE_PREP_ONLY'

def ident(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def sident(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def read(p):
    p = Path(p)
    before = ident(p)
    assert p.is_absolute() and p.resolve() == p
    assert stat.S_ISREG(before[2]) and before[3] == 1 and 0 <= before[4] <= LIMIT
    fd = os.open(p, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        assert sident(os.fstat(fd)) == before
        blocks = []
        remaining = LIMIT + 1
        while remaining:
            b = os.read(fd, min(65536, remaining))
            if not b:
                break
            blocks.append(b)
            remaining -= len(b)
        data = b''.join(blocks)
        assert len(data) <= LIMIT and len(data) == before[4]
        assert sident(os.fstat(fd)) == before and ident(p) == before
    finally:
        os.close(fd)
    return data, dict(path=str(p), sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data), identity=before)

def view(root):
    root = Path(root)
    assert root.is_absolute() and root.resolve() == root
    assert stat.S_ISDIR(ident(root)[2])
    files = {}
    dirs = {'.': ident(root)}
    asts = {}
    for p in sorted(root.rglob('*')):
        rel = str(p.relative_to(root))
        i = ident(p)
        assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):
            dirs[rel] = i
        else:
            data, q = read(p)
            files[rel] = q
            if rel.endswith('.py'):
                tree = ast.parse(data, filename=str(p))
                asts[rel] = hashlib.sha256(ast.dump(tree, include_attributes=False).encode()).hexdigest()
    for rel, q in files.items():
        assert read(root / rel)[1] == q
    for rel, i in dirs.items():
        assert ident(root / rel) == i
    return dict(root=str(root), files=files, directories=dirs, symlinks={}, complete_python_AST_SHA256=asts)

def package(root, expected_sha=None):
    data, mf = read(root / 'MANIFEST.json')
    if expected_sha is not None:
        assert mf['sha256'] == expected_sha
    m = json.loads(data)
    v = view(root)
    assert type(m['member_count']) is int and m['member_count'] == len(m['members'])
    assert m['source_only'] is True and type(m['members']) is dict
    assert set(v['files']) == set(m['members']) | {'MANIFEST.json'}
    assert m['directories'] == v['directories']
    for rel, q in m['members'].items():
        assert q == v['files'][rel] and q['path'] == str(root / rel)
    return m, mf, v

def closed_zero(data):
    d = json.loads(data)
    assert d['closed'] is True and d['observed_terminal'] is True
    t = d.get('terminal_tool_return', d.get('actual_tool_return', d.get('exec_command_result')))
    assert type(t) is dict and type(t['exit_code']) is int and t['exit_code'] == 0
    assert 'session_id' not in t and d.get('session_repolled_after_close', False) is False
    return d, t

def report_contract(data):
    r = json.loads(data)
    assert r['schema'] == SCHEMA and r['status'] == STATUS and r['source_only'] is True
    assert r['all_checks_typed_true'] is True and r['blockers'] == []
    assert type(r['checks']) is list and len(r['checks']) == 31
    assert all(type(c['passed']) is bool and c['passed'] is True for c in r['checks'])
    names = [c.get('check', c.get('name')) for c in r['checks']]
    assert len(set(names)) == 31
    return r

def write_bytes(p, data):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        off = 0
        while off < len(data):
            n = os.write(fd, data[off:])
            assert n > 0
            off += n
        os.fsync(fd)
    finally:
        os.close(fd)
    assert read(p)[0] == data

def write_json(p, data):
    write_bytes(p, (json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode())

def old_pins():
    m, mf, v = package(OLD, OLD_MF_SHA)
    assert len(v['files']) == 15 and len(v['directories']) == 3
    raw_report, rp = read(OLD / 'attempt2_output/REVIEW.json')
    assert rp['sha256'] == OLD_REPORT_SHA
    report_contract(raw_report)
    original_review_raw, original_review_pin = read(OLD / 'ACTUAL_ATTEMPT2_REVIEW_TOOL_RETURN.json')
    d, tr = closed_zero(original_review_raw)
    assert tr['chunk_id'] == 'faf1b5'
    receipt = Path(str(OLD) + '_seal_receipt')
    receipt_files = {}
    for name in ('SEAL_REPORT.json', 'POSTSEAL_REPORT.json', 'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json', 'ACTUAL_FULL_SOURCE_POSTSEAL_TOOL_RETURN.json'):
        data, q = read(receipt / name)
        receipt_files[name] = q
        if name.startswith('ACTUAL_'):
            closed_zero(data)
    return m, mf, v, raw_report, rp, original_review_pin, receipt_files

def assemble():
    m, mf, v, raw_report, rp, original_review_pin, receipts = old_pins()
    root = Path(tempfile.mkdtemp(prefix='axmat_P4_SAVED_PREP_REVIEW_CONSUMER_VIEW_', dir='/private/tmp'))
    copied = {}
    for rel, q in v['files'].items():
        data, actual = read(OLD / rel)
        assert actual == q
        dst = root / 'ORIGINAL_SEALED_REVIEW_LINEAGE' / rel
        write_bytes(dst, data)
        copied[rel] = dict(original_fullpin=q, copy_fullpin=read(dst)[1], content_byte_exact=True)
    for name, q in receipts.items():
        data, actual = read(q['path'])
        assert actual == q
        dst = root / 'ORIGINAL_TRUE_SIBLING_RECEIPT_LINEAGE' / name
        write_bytes(dst, data)
        copied['sibling/' + name] = dict(original_fullpin=q, copy_fullpin=read(dst)[1], content_byte_exact=True)
    write_bytes(root / 'REVIEW.json', raw_report)
    adapter_source, adapter_pin = read(Path(__file__))
    write_bytes(root / 'CONSUMER_VIEW_LAYOUT_AND_SEAL_SOURCE.py', adapter_source)
    utility_data, utility_pin = read(UTILITY)
    utility_tree = ast.parse(utility_data, filename=str(UTILITY))
    selected = {n.name: ast.get_source_segment(utility_data.decode(), n) for n in utility_tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in {'package', 'peer', 'terminal'}}
    assert set(selected) == {'package', 'peer', 'terminal'}
    top = read(root / 'REVIEW.json')[1]
    write_json(root / 'BYTE_EXACT_REPORT_CONSUMER_VIEW_PROVENANCE.json', dict(
        schema='P4_ACTUAL_SAVED_PREP_REVIEW_BYTE_EXACT_PATH_LAYOUT_CONSUMER_VIEW_V1',
        source_only=True,
        scope='Same actual faf1b5 31-check report copied to the fixed top-level consumer path; no new saved-PREP audit or qualification.',
        original_manifest_pin=mf,
        original_review_pin=rp,
        top_level_review_pin=top,
        original_actual_31_check_tool_return_pin=original_review_pin,
        original_true_seal_and_postseal_pins=receipts,
        complete_original_file_copy_relations=copied,
        original_complete_directories=v['directories'],
        original_file_count=15,
        same_actual_review_bytes=True,
        new_31_check_review_performed=False,
        business_candidate_utility_guard_resource_native_or_payload_executed=False,
        runtime_caps_or_scientific_gates_changed=False,
        actual_consumer_Source_pin=utility_pin,
        complete_consumer_functions=selected,
        layout_adapter_original_Source_pin=adapter_pin,
        original_pass_report_schema=SCHEMA,
        original_pass_report_status=STATUS))
    # Allocate MANIFEST first so writing its contents cannot change directory 7ID.
    write_bytes(root / 'MANIFEST.json', b'')
    current = view(root)
    members = {k: q for k, q in current['files'].items() if k != 'MANIFEST.json'}
    manifest = dict(schema='COMPLETE_SOURCE_META_BYTE_EXACT_CONSUMER_VIEW_MANIFEST_V1', source_only=True,
                    scope='Fixed path layout for the same actual saved-PREP independent report; copies are explicit lineage, not new review.',
                    member_count=len(members), members=members, directories=current['directories'])
    data = (json.dumps(manifest, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    fd = os.open(root / 'MANIFEST.json', os.O_WRONLY | os.O_NOFOLLOW)
    try:
        assert os.fstat(fd).st_size == 0
        off = 0
        while off < len(data):
            n = os.write(fd, data[off:])
            assert n > 0
            off += n
        os.fsync(fd)
    finally:
        os.close(fd)
    checked, mp, cv = package(root)
    assert old_pins()[1:3] == (mf, v)
    print(json.dumps(dict(source_only=True, root=str(root), manifest_pin=mp, review_pin=top,
                         file_count=len(cv['files']), directory_count=len(cv['directories']),
                         new_31_check_review_performed=False), sort_keys=True, allow_nan=False))

def verify_view(root):
    m, mp, v = package(root)
    data, rp = read(root / 'REVIEW.json')
    report_contract(data)
    pbytes, pp = read(root / 'BYTE_EXACT_REPORT_CONSUMER_VIEW_PROVENANCE.json')
    p = json.loads(pbytes)
    old = old_pins()
    assert old[1] == p['original_manifest_pin'] and old[2]['directories'] == p['original_complete_directories']
    assert old[4] == p['original_review_pin'] and old[5] == p['original_actual_31_check_tool_return_pin']
    assert old[6] == p['original_true_seal_and_postseal_pins']
    assert data == old[3] and rp == p['top_level_review_pin']
    assert p['new_31_check_review_performed'] is False and p['runtime_caps_or_scientific_gates_changed'] is False
    assert p['business_candidate_utility_guard_resource_native_or_payload_executed'] is False
    assert len(p['complete_original_file_copy_relations']) == 19
    for rel, c in p['complete_original_file_copy_relations'].items():
        a, aq = read(c['original_fullpin']['path'])
        b, bq = read(c['copy_fullpin']['path'])
        assert aq == c['original_fullpin'] and bq == c['copy_fullpin'] and a == b and c['content_byte_exact'] is True
    assert read(UTILITY)[1] == p['actual_consumer_Source_pin']
    return mp, rp, pp, v

def seal(root):
    mp, rp, pp, v = verify_view(root)
    sibling = Path(str(root) + '_seal_receipt')
    sibling.mkdir()
    result = dict(schema='P4_BYTE_EXACT_ACTUAL_SAVED_PREP_REVIEW_CONSUMER_VIEW_SEAL_V1', source_only=True,
                  status='SAME_ACTUAL_31_CHECK_REPORT_PATH_LAYOUT_VIEW_ONLY',
                  manifest_pin=mp, review_pin=rp, provenance_pin=pp,
                  file_count=len(v['files']), directory_count=len(v['directories']),
                  complete_current_Source_small_META_view=v,
                  new_31_check_review_performed=False,
                  candidate_API_native_or_payload_executed=False,
                  caps_or_scientific_gates_changed=False)
    write_json(sibling / 'SEAL_REPORT.json', result)
    assert verify_view(root) == (mp, rp, pp, v)
    print(json.dumps(dict(manifest_pin=mp, review_pin=rp, seal_report_pin=read(sibling / 'SEAL_REPORT.json')[1],
                         source_only=True, same_original_actual_review=True, new_31_check_review_performed=False,
                         file_count=len(v['files']), directory_count=len(v['directories'])), sort_keys=True, allow_nan=False))

def postseal(root):
    mp, rp, pp, v = verify_view(root)
    sibling = Path(str(root) + '_seal_receipt')
    sealbytes, sp = read(sibling / 'SEAL_REPORT.json')
    saved = json.loads(sealbytes)
    assert saved['manifest_pin'] == mp and saved['review_pin'] == rp and saved['complete_current_Source_small_META_view'] == v
    raw, tp = read(sibling / 'ACTUAL_SOURCE_SEAL_TOOL_RETURN.json')
    wrapper, terminal = closed_zero(raw)
    observed = json.loads(terminal['output'])
    assert observed['manifest_pin'] == mp and observed['review_pin'] == rp and observed['seal_report_pin'] == sp
    result = dict(schema='P4_BYTE_EXACT_ACTUAL_SAVED_PREP_REVIEW_CONSUMER_VIEW_POSTSEAL_V1', source_only=True,
                  status='COMPLETE_CONSUMER_VIEW_BYTES_AND_REAL_CLOSED_INT0_SEAL_RECHECKED_SAME_ACTUAL_REPORT',
                  manifest_pin=mp, review_pin=rp, provenance_pin=pp, actual_seal_tool_return_pin=tp,
                  seal_report_pin=sp, complete_current_Source_small_META_view=v,
                  fixed_top_level_peer_consumer_contract_satisfied=True,
                  original_sealed_review_and_true_sibling_bytes_unchanged=True,
                  new_31_check_review_performed=False,
                  candidate_API_native_or_payload_executed=False, caps_or_scientific_gates_changed=False)
    write_json(sibling / 'POSTSEAL_REPORT.json', result)
    assert verify_view(root) == (mp, rp, pp, v)
    print(json.dumps(dict(manifest_pin=mp, review_pin=rp, postseal_report_pin=read(sibling / 'POSTSEAL_REPORT.json')[1],
                         actual_seal_tool_return_pin=tp, source_only=True,
                         fixed_top_level_peer_consumer_contract_satisfied=True,
                         new_31_check_review_performed=False, file_count=len(v['files']),
                         directory_count=len(v['directories'])), sort_keys=True, allow_nan=False))

if __name__ == '__main__':
    assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
    action = sys.argv[1]
    if action == 'assemble':
        assert len(sys.argv) == 2
        assemble()
    else:
        assert len(sys.argv) == 3
        root = Path(sys.argv[2])
        assert root.parent == Path('/private/tmp') and root.name.startswith('axmat_P4_SAVED_PREP_REVIEW_CONSUMER_VIEW_')
        if action == 'seal':
            seal(root)
        elif action == 'postseal':
            postseal(root)
        else:
            raise ValueError('finite layout adapter action')
