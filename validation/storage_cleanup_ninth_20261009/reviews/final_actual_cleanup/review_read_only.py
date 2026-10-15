import collections
import hashlib
import json
import os
import stat
import time
import traceback
import zlib
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path('/Users/wen/spot')
R = ROOT / 'validation/storage_cleanup_ninth_20261009'
OUT = Path('/private/tmp/spot_ninth_actual_cleanup_independent_review_20261009')
START = time.monotonic()
PINS = {}
READ_BYTES = 0

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def fullpin(p, expected=None):
    global READ_BYTES
    p = Path(p)
    a = identity(p)
    assert stat.S_ISREG(a[2]), ('not regular', str(p))
    if str(p) in PINS:
        rec = PINS[str(p)]
        assert a == rec['identity'], ('changed cached pin', str(p))
    else:
        h = hashlib.sha256()
        with p.open('rb') as f:
            fs = os.fstat(f.fileno())
            assert [fs.st_dev, fs.st_ino] == a[:2]
            while b := f.read(4 * 1024**2):
                h.update(b)
                READ_BYTES += len(b)
        assert identity(p) == a, ('changed during read', str(p))
        rec = dict(path=str(p), identity=a, size=a[3], sha256=h.hexdigest())
        PINS[str(p)] = rec
    if expected:
        for k in ['sha256', 'identity']:
            if k in expected:
                assert rec[k] == expected[k], ('pin mismatch', k, str(p))
        size = expected.get('size', expected.get('bytes', expected.get('size_bytes')))
        if size is not None:
            assert rec['size'] == size, ('size mismatch', str(p))
    return rec

def load(p, sha=None):
    rec = fullpin(p, {'sha256': sha} if sha else None)
    b = Path(p).read_bytes()
    assert hashlib.sha256(b).hexdigest() == rec['sha256'] and identity(p) == rec['identity']
    return json.loads(b)

def inventory(excluded):
    h = hashlib.sha256()
    counts = collections.Counter()
    for dp, dn, fn in os.walk(ROOT, followlinks=False):
        dn[:] = sorted(n for n in dn if Path(dp) / n != R)
        for n in sorted(dn + fn):
            p = Path(dp) / n
            if str(p) in excluded:
                continue
            s = p.lstat()
            rel = str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):
                row = [rel, identity(p), os.readlink(p)]
                counts['symlinks'] += 1
            elif stat.S_ISDIR(s.st_mode):
                row = [rel, 'directory']
                counts['directories'] += 1
            elif stat.S_ISREG(s.st_mode):
                row = [rel, identity(p)]
                counts['regular_files'] += 1
            else:
                raise ValueError(('unsupported file type', str(p)))
            h.update(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n')
    return dict(sha256=h.hexdigest(), **dict(counts))

def link_screen(selected):
    rows = []
    for dp, dn, fn in os.walk(ROOT, followlinks=False):
        for n in dn + fn:
            p = Path(dp) / n
            if p.is_symlink():
                target = p.resolve(strict=False)
                assert not any(Path(q) == target or Path(q).is_relative_to(target) for q in selected), ('inbound alias', str(p), str(target))
                rows.append([str(p), os.readlink(p), str(target)])
    return dict(count=len(rows), sha256=hashlib.sha256(json.dumps(sorted(rows)).encode()).hexdigest()), sorted(rows)

def strict_gzip(record):
    b = record['backup']
    orig = record['original']
    saved = fullpin(b['path'], b)
    d = zlib.decompressobj(16 + zlib.MAX_WBITS)
    h = hashlib.sha256()
    compressed_h = hashlib.sha256()
    size = 0
    physical = 0
    with Path(b['path']).open('rb') as f:
        s = os.fstat(f.fileno())
        assert [s.st_dev, s.st_ino] == saved['identity'][:2]
        while block := f.read(1024**2):
            physical += len(block)
            compressed_h.update(block)
            assert not d.eof, ('trailing gzip data', b['path'])
            pending = block
            while pending:
                out = d.decompress(pending, 4 * 1024**2)
                size += len(out)
                assert size <= orig['size'], ('decoded oversized', b['path'])
                h.update(out)
                assert not d.unused_data, ('extra gzip member or trailing data', b['path'])
                pending = d.unconsumed_tail
        assert d.eof and not d.unconsumed_tail and not d.unused_data, ('incomplete gzip', b['path'])
        last = d.flush()
        size += len(last)
        h.update(last)
    assert size == orig['size'] and h.hexdigest() == orig['sha256'], ('decoded mismatch', b['path'])
    assert physical == b['size'] and compressed_h.hexdigest() == b['sha256']
    assert identity(b['path']) == saved['identity']
    assert record['verified_decompressed'] == dict(size=size, sha256=h.hexdigest())
    return dict(original=orig, compressed=saved, independent_strict_single_member_decoded=dict(size=size, sha256=h.hexdigest()), decoded_bytes_saved=0)

def collect_abs(value, dest):
    if isinstance(value, dict):
        for k, v in value.items():
            collect_abs(k, dest)
            collect_abs(v, dest)
    elif isinstance(value, list):
        for v in value:
            collect_abs(v, dest)
    elif isinstance(value, str) and value.startswith('/'):
        dest.add(value)

def main():
    m = load(R / 'manifest.json', 'e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8')
    pf = load(R / 'preflight.json', '3b03b77dc51b84ff4b20241214c36b90018470bf40d5886e02ee4bb1c40c7358')
    result = load(R / 'cleanup_result.json', 'c9008a5b8080b1d8dcc54030cf53564a4e5fd2c5c23f418335dfe732678b1f33')
    terminal = load(R / 'cleanup_terminal_observation.json', 'b8e680e4ff5242a9a8e1a217f1a58b758b380cff1e5e0fa9dfcff53fa9421827')
    ipf = load(R / 'independent_preflight_review.json', '35655209c7722f7ea23b459c6f17581f1538af7c575f8994b819598510d25602')
    source_review = load(R / 'reviews/final_lossless_source/independent_lossless_archive_source_review.json', '60e6df52166215d44cfa0cbe68cd7cbe3524b0469847547172806d13b2f944e6')
    backup = load(R / 'packed_material_intermediate_backups.json', 'd5834da3209265f9d0f4ad571f4da0c8a570558cfe39b7120750f5dad156aec9')
    backup_review = load(R / 'reviews/actual_lossless_backup/independent_actual_lossless_backup_review.json', 'fe69abbd5dc40cb459509957a25bb6afccf77d50032b90ec5b89ece96b0346d0')
    backup_input = load(R / 'material_archive_input.json', 'dfb4c46ab3b9add27c4430dfadf932285841f5bcede40958c20c52203740702b')
    backup_terminal = load(R / 'backup_terminal_observation.json', '67a59baa8aa87be670e84c30c58c316c478aa4dfabb4955573be2e00f28849cb')
    preflight_terminal = load(R / 'preflight_terminal_observation.json')
    ledger_pin = fullpin(R / 'retirement_ledger.jsonl', {'sha256':'16c87e9c98d5a17f0be9634e1bfda52c5aa9273695f2923f4c5cba43031e6998'})
    ledger = [json.loads(line) for line in (R / 'retirement_ledger.jsonl').read_bytes().splitlines()]
    selected = {c['path'] for c in m['candidates']}
    categories = dict(collections.Counter(c['category'] for c in m['candidates']))
    assert categories == {'EXACT_DUPLICATE_OLD_WORK_COPY':167, 'TERMINAL_OLD_INTERMEDIATE_PAYLOAD':9, 'GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE':89}
    assert len(selected) == len(ledger) == m['exact_count'] == result['deleted_files'] == terminal['deleted_files'] == 265
    assert all(not os.path.lexists(p) for p in selected)
    assert result['status'] == pf['status'] == ipf['status'] == 'PASS'
    assert terminal['initial_chunk_id'] == '2c9f71' and terminal['session_id'] == 25842 and terminal['terminal_chunk_id'] == 'd14461'
    assert terminal['exit_code'] == 0 and terminal['closed'] is True
    assert terminal['result_sha256'] == PINS[str(R / 'cleanup_result.json')]['sha256']
    assert result['manifest_sha256'] == pf['manifest_sha256'] == ipf['manifest_sha256'] == PINS[str(R/'manifest.json')]['sha256']
    assert result['preflight_sha256'] == ipf['preflight_sha256'] == PINS[str(R/'preflight.json')]['sha256']
    assert result['independent_preflight_sha256'] == PINS[str(R/'independent_preflight_review.json')]['sha256']
    assert result['new_scientific_credit'] is False and result['solver_or_API_executed'] is False
    assert m['new_scientific_credit'] is False and m['old_global_manifest_and_results_not_rewritten'] is True
    assert result['all_retained_primaries_and_source_review_bytes_unchanged'] is True
    assert sum(c['size'] for c in m['candidates']) == m['logical_bytes'] == result['deleted_logical_bytes'] == 12914344895
    assert sum(c['allocated_bytes'] for c in m['candidates']) == m['allocated_bytes'] == result['deleted_allocated_bytes'] == 12914892800
    assert len(pf['verified_candidates']) == 265 and len(pf['verified_primaries']) == len(m['retained_primaries']) == 336
    for c, prior, deleted in zip(m['candidates'], pf['verified_candidates'], ledger):
        assert {k:c[k] for k in ['path','identity','size','sha256']} == prior
        assert deleted == dict(**prior, category=c['category'], deleted=True)
        p = Path(c['path'])
        assert str(p) == c['path'] and p.is_absolute() and '..' not in p.parts and p.is_relative_to(ROOT/'validation/artifacts')
        assert p.parent.resolve(strict=True) == p.parent
    assert not selected & {p['path'] for p in m['retained_primaries']}
    expected_baseline = pf['preservation_baseline']
    assert expected_baseline == result['nonselected_before'] == result['nonselected_after'] == ipf['preservation_baseline']
    before = inventory(selected)
    assert before == expected_baseline, ('nonselected baseline before mismatch', before)
    links_before, link_rows = link_screen(selected)
    assert links_before == pf['symlink_screen'] == result['symlink_check_after']
    print(json.dumps(dict(phase='actual baseline and exact ledger verified', baseline=before, symlinks=links_before)), flush=True)
    for group in ['retained_primaries', 'source_and_review_pins']:
        for p in m[group]:
            fullpin(p['path'], p)
        print(json.dumps(dict(phase=group, verified=len(m[group]), unique_full_read_files=len(PINS), full_read_bytes=READ_BYTES)), flush=True)
    for prior, p in zip(pf['verified_primaries'], m['retained_primaries']):
        assert prior == {k:p[k] for k in ['path','identity','size','sha256']}
    for k in ['cleanup_source','pack_source','archive_restore_source','duplicate_restore_source','fixed_pack_input']:
        fullpin(source_review[k]['path'], source_review[k])
    assert source_review['status'] == 'PASS_SOURCE_ONLY_LOSSLESS_MATERIAL_ARCHIVE_AND_RESTORE'
    assert PINS[str(R/'cleanup_exact_files.py')]['sha256'] == m['cleanup_source_sha256'] == ipf['cleanup_source_sha256']
    assert backup['status'] == 'PASS' and backup['records'] and len(backup['records']) == len(backup_input) == 89
    assert backup_terminal['exit_code'] == 0 and backup_terminal['closed'] is True
    assert backup_review['strict_complete_single_member_gzip_verified_count'] == 89
    assert backup_review['packed_material_intermediate_backups_sha256'] == PINS[str(R/'packed_material_intermediate_backups.json')]['sha256']
    fullpin(R/'backup_creation_ledger.jsonl', {'sha256':'e6960498d0d191793a77de08f5a804aeef0563c3bf7946054aa0771a9259246e'})
    assert fullpin(R/'backup.stdout')['sha256'] == backup_terminal['stdout_sha256']
    assert fullpin(R/'backup.stderr')['size'] == backup_terminal['stderr_bytes'] == 0
    originals = {x['path']:x for x in backup_input}
    archived = {c['path']:c for c in m['candidates'] if c['category']=='GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'}
    retained = {x['path']:x for x in m['retained_primaries']}
    decoded = []
    for row in backup['records']:
        orig = row['original']; b = row['backup']; c = archived[orig['path']]
        assert orig == originals[orig['path']]
        assert all(c[k] == orig[k] for k in ['path','identity','size','sha256','allocated_bytes','historical_payload_proof'])
        assert c['compressed_backup'] == {k:b[k] for k in ['path','identity','size','sha256']}
        assert b['path'] in retained and b['path'] not in selected and Path(b['path']).is_relative_to(R/'packed_material_intermediates')
        decoded.append(strict_gzip(row))
    assert sum(x['independent_strict_single_member_decoded']['size'] for x in decoded) == 8454673080
    print(json.dumps(dict(phase='89 gzip fresh compressed and independently strict decoded', decoded_bytes=8454673080)), flush=True)
    exact = [c for c in m['candidates'] if c['category']=='EXACT_DUPLICATE_OLD_WORK_COPY']
    for c in exact:
        p = retained[c['retained_primary']]
        assert p['path'] not in selected and p['sha256'] == c['sha256'] and p['size'] == c['size']
    for c in m['candidates']:
        proof = c.get('historical_payload_proof')
        if not proof:
            continue
        doc = load(proof['path'], proof['sha256'])
        if proof['format'] == 'JSON_SHA256_MAP':
            assert doc['classification'] == 'SEALED_STAGE_OUTPUTS' and doc['sha256'][proof['key']] == c['sha256']
        else:
            assert proof['format']=='NJOY_RECEIPT_OUTPUT' and type(doc['returncode']) is int and doc['returncode']==0 and doc['output_sha256']==c['sha256']
            seal = fullpin(proof['result_manifest_path'], {'sha256':proof['result_manifest_sha256']})
            entries = {line.split('  ',1)[1]:line.split('  ',1)[0] for line in Path(seal['path']).read_text().splitlines() if line}
            assert entries[str(Path(c['path']).relative_to(Path(seal['path']).parent))] == c['sha256']
    graph_pin = fullpin(m['graph_pin']['path'], m['graph_pin'])
    index_pin = fullpin(m['old_index_pin']['path'], m['old_index_pin'])
    graph = load(graph_pin['path']); index = load(index_pin['path'])
    absolute = set(); collect_abs(graph, absolute)
    directories = {x['canonical_root'] for x in graph['namespaces']} | {x['target'] for x in graph['aliases'] if x['kind'] in ('directory','dir')} | set(index['protected_directories']) | set(m['critical_roots'])
    protected = absolute | set(index['protected_files']) | set(index['inbound_alias_targets']) | set(m['current_cold_extra_protected_files'])
    assert not selected & protected
    assert all(not any(p==d or p.startswith(d+'/') for d in directories) for p in selected)
    closure = dict(canonical_files=len(graph['canonical_files']), namespaces=len(graph['namespaces']), aliases=len(graph['aliases']), live_resource_roots=len(graph['live_resource_roots']), old_protected_files=len(index['protected_files']), critical_roots=len(m['critical_roots']), candidate_intersections=[])
    assert closure == pf['current_closure'] == ipf['current_closure']
    assert len(m['current_cold_extra_protected_files']) == 6248 and len(graph['live_resource_roots']) == 228
    actualcold_path = ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/next_cold_input_readonly_integrity_review/derived_required_path_SHA_owners.json'
    actualcold = load(actualcold_path)
    assert len(actualcold)==1534 and not selected & {x['path'] for x in actualcold}
    edges = ipf['old_restore_primary_dependency_edges']
    assert len(edges)==120 and len({e['primary'] for e in edges})==89
    for e in edges:
        assert e['primary'] in archived and e['required_restore_first']==archived[e['primary']]['compressed_backup']['path']
        fullpin(e['manifest'])
    material_roles = load(R/'material/retained_original_nuclear_source_pin_roles.json')
    for row in material_roles:
        fullpin(row['pin']['path'], row['pin'])
    material_stages = load(R/'material/retained_final_and_stage_evidence_fresh_SHA_identity.json')
    for row in material_stages:
        fullpin(row['path'], row)
    dragr = {x['path'] for x in material_stages if 'all control/expanded low/high final DRAGR nuclear libraries' in x.get('roles',[])}
    material_sources = {x['path'] for x in material_stages if '28 accepted final nuclear-data source' in x.get('roles',[])}
    assert len(dragr)==53 and len(material_sources)==28, ('material preservation counts', len(dragr), len(material_sources))
    for p in PINS.values():
        assert identity(p['path']) == p['identity'], ('pin no longer stable', p['path'])
    after = inventory(selected)
    assert after == before == expected_baseline
    links_after, after_rows = link_screen(selected)
    assert links_after == links_before and after_rows == link_rows
    assert all(not os.path.lexists(p) for p in selected)
    records = sorted(PINS.values(), key=lambda x:x['path'])
    pinfile = OUT/'all_fresh_full_SHA_identity_records.json'
    pinfile.write_text(json.dumps(records, indent=2)+'\n')
    gzipfile = OUT/'independent_89_strict_gzip_decoded_proofs.json'
    gzipfile.write_text(json.dumps(decoded, indent=2)+'\n')
    report = dict(schema='SPOT_NINTH_ACTUAL_CLEANUP_INDEPENDENT_READONLY_REVIEW_V1', status='PASS', scope='Actual fixed 265-file retirement and retained evidence only; no business execution', completed_utc=datetime.now(timezone.utc).isoformat(), manifest_sha256=PINS[str(R/'manifest.json')]['sha256'], preflight_sha256=PINS[str(R/'preflight.json')]['sha256'], result_sha256=PINS[str(R/'cleanup_result.json')]['sha256'], cleanup_tool_terminal_sha256=PINS[str(R/'cleanup_terminal_observation.json')]['sha256'], cleanup_tool=terminal, cleanup_source_sha256=m['cleanup_source_sha256'], independent_preflight_sha256=PINS[str(R/'independent_preflight_review.json')]['sha256'], source_review_sha256=PINS[str(R/'reviews/final_lossless_source/independent_lossless_archive_source_review.json')]['sha256'], retirement_ledger=ledger_pin, exact_ledger_manifest_preflight_one_to_one=True, selected_count=265, selected_categories=categories, all_selected_absent_after_actual_cleanup=True, retained_primaries_full_fresh_SHA_identity_count=336, source_and_review_full_fresh_SHA_identity_count=4980, all_retained_and_source_pins_still_stable=True, independent_full_SHA_unique_files=len(records), independent_full_SHA_physical_bytes=READ_BYTES, fresh_pins_file_sha256=hashlib.sha256(pinfile.read_bytes()).hexdigest(), preservation_baseline=before, independent_nonselected_before=before, independent_nonselected_after=after, symlink_screen=links_after, current_closure=closure, graph_pin=graph_pin, old_index_pin=index_pin, current_cold_extra_protected_paths=6248, next_actual_cold_required_path_scope=1534, candidate_current_or_protected_hits=0, independent_strict_complete_single_member_gzip_verified_count=89, independently_decoded_size_SHA_bytes=8454673080, decompressed_payload_bytes_saved=0, gzip_proofs_file_sha256=hashlib.sha256(gzipfile.read_bytes()).hexdigest(), actual_backup_review_sha256=PINS[str(R/'reviews/actual_lossless_backup/independent_actual_lossless_backup_review.json')]['sha256'], compressed_backups_permanently_required=True, compressed_backup_allocated_bytes=2640285696, earlier_exact_restore_edges_requiring_original_raw_restoration_first=120, preserved_unique_final_DRAGR_outputs=53, preserved_unique_original_nuclear_sources=28, original_material_stage_result_receipt_seal_evidence_full_fresh_count=len(material_stages), original_closed_parent_map004_bootstrap_docs_preservation='Original full pinned evidence preserved by fresh 336 retained +4980 source/review SHA identity and exact whole nonselected baseline; early maps1-3 removed leaves only those9', deleted_logical_bytes=12914344895, deleted_allocated_bytes=12914892800, nominal_net_removed_allocated_after_backup_bytes=10274607104, root_actual_capacity_observations=dict(before=result['capacity_before'],after=result['capacity_after']), old_global_manifest_results_not_rewritten=True, historical_descriptor_rows_not_claimed_current_fresh_pins=ipf['historical_descriptor_rows_not_claimed_current_fresh_pins'], files_deleted_by_this_review=0, restore_pack_cleanup_preflight_apply_executed_by_this_review=False, project_formal_ART_writes=False, business_import_API_ctor_PREP_RUN_solver_executed=False, new_scientific_or_RSS_or_qualification_credit=False, limitations=['Whole-project preservation fingerprint covers lstat identity plus literal links and directory names, not content SHA of all175560 files. Explicit retained336/source4980 and additional retained original source/stage evidence received complete fresh SHA.', 'R9 itself is excluded from the whole baseline; its89 backup gzip files, manifest, sources, reviews, actual receipts and ledger were separately completely hashed.', '89 compressed backups are now the required lossless primary recovery representation. Restore raw originals first, then the120 previous exact-copy restore edges; original inode andctime cannot be recreated.', '9 unique old compensated map1-3 numerical leaves have no equal retained primary. Original sealed-stage documents remain true historical evidence, but replay/full old seal needs numerical rebuild and byte equality is not promised.', 'Backup and prior preflight reports describe their original pre-deletion moments. Their original raw-present/deletion0 fields are not asserted as current state.', 'Capacity figures are observed project block accounting and disk-free values at Root cleanup; they are not guaranteed instant physical APFS reclamation.'], audit_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), elapsed_seconds=time.monotonic()-START)
    (OUT/'REPORT.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS',report=str(OUT/'REPORT.json'),sha256=hashlib.sha256((OUT/'REPORT.json').read_bytes()).hexdigest(),baseline=before,verified_gzip=89,full_read_files=len(records),elapsed_seconds=report['elapsed_seconds'])), flush=True)

try:
    main()
except Exception:
    (OUT/'failure_observation.json').write_text(json.dumps(dict(status='BLOCKED',exception=traceback.format_exc(),elapsed_seconds=time.monotonic()-START,files_deleted=0,formal_or_ART_written=False),indent=2)+'\n')
    raise
