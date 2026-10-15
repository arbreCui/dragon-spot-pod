import collections
import gzip
import hashlib
import json
import os
import stat
import time
from pathlib import Path

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
R = ROOT / 'validation/storage_cleanup_ninth_20261009'
TMP = Path('/private/tmp/spot_ninth_actual_preflight_independent_review_20261009')
MANIFEST_SHA = 'e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8'
PREFLIGHT_SHA = '3b03b77dc51b84ff4b20241214c36b90018470bf40d5886e02ee4bb1c40c7358'
BASELINE = dict(sha256='87cb87e22df74a4a4155723b09d008e56b9b154b426e50b8c136007a22f16f6e', directories=7013, regular_files=175560, symlinks=687)
PINS = {}
BYTES = 0
START = time.monotonic()

def identity(p):
    s = Path(p).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(p):
    global BYTES
    p = Path(p)
    before = identity(p)
    assert stat.S_ISREG(before[2]) and p.parent.resolve(strict=True) == p.parent, str(p)
    if str(p) in PINS:
        assert PINS[str(p)]['identity'] == before, str(p)
        return PINS[str(p)]
    h = hashlib.sha256()
    with p.open('rb') as stream:
        s = os.fstat(stream.fileno())
        assert [s.st_dev, s.st_ino] == before[:2], str(p)
        while block := stream.read(4 * 1024**2):
            h.update(block)
            BYTES += len(block)
    assert identity(p) == before, str(p)
    result = dict(path=str(p), identity=before, size=before[3], sha256=h.hexdigest())
    PINS[str(p)] = result
    return result

def expected(row):
    fresh = pin(row['path'])
    size = row.get('size', row.get('size_bytes', row.get('bytes')))
    assert fresh['sha256'] == row['sha256'], row['path']
    if size is not None:
        assert fresh['size'] == size, row['path']
    if 'identity' in row:
        assert fresh['identity'] == row['identity'], row['path']
    return fresh

def read_json(p, sha=None):
    record = pin(p)
    if sha:
        assert record['sha256'] == sha, str(p)
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out, ('duplicate JSON key', str(p), key)
            out[key] = value
        return out
    value = json.loads(Path(p).read_text(), object_pairs_hook=pairs)
    assert identity(p) == record['identity']
    return value

def inventory(excluded):
    digest = hashlib.sha256()
    counts = collections.Counter()
    for dp, dn, fn in os.walk(ROOT, followlinks=False):
        dn[:] = sorted(n for n in dn if Path(dp) / n != R)
        for name in sorted(dn + fn):
            p = Path(dp) / name
            if str(p) in excluded:
                continue
            s = p.lstat()
            relative = str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):
                row = [relative, identity(p), os.readlink(p)]
                counts['symlinks'] += 1
            elif stat.S_ISDIR(s.st_mode):
                row = [relative, 'directory']
                counts['directories'] += 1
            else:
                assert stat.S_ISREG(s.st_mode), str(p)
                row = [relative, identity(p)]
                counts['regular_files'] += 1
            digest.update(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n')
    return dict(sha256=digest.hexdigest(), **counts)

def all_absolute(value, out):
    if isinstance(value, dict):
        for key, item in value.items():
            all_absolute(key, out)
            all_absolute(item, out)
    elif isinstance(value, list):
        for item in value:
            all_absolute(item, out)
    elif isinstance(value, str) and value.startswith('/'):
        out.add(value)

def manifest_entries(p):
    entries = {}
    for line in Path(p).read_text().splitlines():
        if not line:
            continue
        sha, name = line.split('  ', 1)
        assert name not in entries and len(sha) == 64, str(p)
        entries[name] = sha
    return entries

def main():
    m = read_json(R / 'manifest.json', MANIFEST_SHA)
    pf = read_json(R / 'preflight.json', PREFLIGHT_SHA)
    assert pf['status'] == 'PASS' and pf['manifest_sha256'] == MANIFEST_SHA
    assert pf['files_deleted'] == 0 and pf['solver_or_API_executed'] is False
    assert pf['preservation_baseline'] == BASELINE
    obs = read_json(R / 'preflight_terminal_observation.json')
    assert type(obs['exit_code']) is int and obs['exit_code'] == 0 and obs['closed'] is True
    assert (obs['initial_chunk_id'], obs['session_id'], obs['terminal_chunk_id']) == ('ea0f23', 85957, '390621')
    assert obs['report_sha256'] == PREFLIGHT_SHA and obs['manifest_sha256'] == MANIFEST_SHA
    assert obs['files_deleted'] == 0 and obs['candidates'] == 265 and obs['preservation_baseline'] == BASELINE
    assert not (R / 'cleanup_result.json').exists() and not (R / 'retirement_ledger.jsonl').exists()
    candidates = m['candidates']
    selected = {row['path'] for row in candidates}
    assert len(selected) == len(candidates) == m['exact_count'] == 265
    counts = dict(collections.Counter(row['category'] for row in candidates))
    assert counts == dict(EXACT_DUPLICATE_OLD_WORK_COPY=167, TERMINAL_OLD_INTERMEDIATE_PAYLOAD=9, GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE=89)
    assert m['logical_bytes'] == sum(row['size'] for row in candidates) == 12914344895
    assert m['allocated_bytes'] == sum(row['allocated_bytes'] for row in candidates) == 12914892800
    assert m['new_scientific_credit'] is False and m['old_global_manifest_and_results_not_rewritten'] is True
    assert not selected.intersection(row['path'] for row in m['retained_primaries'])
    assert not selected.intersection(row['path'] for row in m['source_and_review_pins'])
    before = inventory(selected)
    assert before == BASELINE, ('initial full inventory', before)
    print('INDEPENDENT inventory before: matched actual Root baseline', flush=True)

    expected_sources = {
        'cleanup_exact_files.py': '323a011638b5261419fed84ef6e85854a001bbe22b3a7067faca0a70d5f9e3ab',
        'pack_old_material_intermediates.py': '6125b048be62d76041cdcc3f0b307aff74115172d7cb0b1a10bd4e07a6d53e4a',
        'restore_archived_material_intermediates.py': '26a4c2616f6df2662a0ff69659eb9e0b05b5d98e8dfd6a67e37f4eec13f8adf1',
        'restore_retired_work_copies.py': '53a51f0f70c5194b13328d01b356d33260cd1b310753fda743b8ad6af6a687bd',
    }
    for name, sha in expected_sources.items():
        assert pin(R / name)['sha256'] == sha
    assert m['cleanup_source_sha256'] == expected_sources['cleanup_exact_files.py']
    source_audit = read_json(R / 'reviews/final_lossless_source/independent_lossless_archive_source_review.json', '60e6df52166215d44cfa0cbe68cd7cbe3524b0469847547172806d13b2f944e6')
    assert source_audit['status'].startswith('PASS')
    assert len(m['source_and_review_pins']) == len({row['path'] for row in m['source_and_review_pins']}) == 4980
    for row in m['source_and_review_pins']:
        expected(row)
    print('INDEPENDENT full fresh source/review pins: 4980 verified', flush=True)
    assert len(m['retained_primaries']) == len({row['path'] for row in m['retained_primaries']}) == 336
    kept = [expected(row) for row in m['retained_primaries']]
    assert kept == pf['verified_primaries']
    retained = {row['path']: row for row in kept}
    print('INDEPENDENT full fresh retained primary pins: 336 verified', flush=True)

    graph = read_json(m['graph_pin']['path'], '242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
    expected(m['graph_pin'])
    index = read_json(m['old_index_pin']['path'], '30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
    expected(m['old_index_pin'])
    assert pin(m['graph_pin']['path'])['size'] == 64639433
    assert graph['requirements']['rows']['row_count'] == 235528
    absolute = set()
    all_absolute(graph, absolute)
    directories = {x['canonical_root'] for x in graph['namespaces']}
    directories |= {x['target'] for x in graph['aliases'] if x['kind'] in ('directory', 'dir')}
    directories |= set(index['protected_directories']) | set(m['critical_roots'])
    protected = absolute | set(index['protected_files']) | set(index['inbound_alias_targets']) | set(m['current_cold_extra_protected_files'])
    intersections = [p for p in selected if p in protected or any(p == d or p.startswith(d + '/') for d in directories)]
    assert not intersections, intersections
    close = dict(canonical_files=len(graph['canonical_files']), namespaces=len(graph['namespaces']), aliases=len(graph['aliases']), live_resource_roots=len(graph['live_resource_roots']), old_protected_files=len(index['protected_files']), critical_roots=len(m['critical_roots']), candidate_intersections=[])
    assert close == pf['current_closure']
    assert (close['canonical_files'], close['namespaces'], close['aliases'], close['live_resource_roots'], close['critical_roots']) == (35647, 86, 186, 228, 92)
    assert len(m['current_cold_extra_protected_files']) == len(set(m['current_cold_extra_protected_files'])) == 6248
    cold = read_json(m['current_cold_dynamic_proof']['report']['path'], '11f9f07e92ca6c11ccb90ed4bf58b9d98a0e726bf2893a40e457c32edbc9e161')
    dynamic = {row['path'] for row in cold['current_cold_dynamic_protected_files']}
    assert len(dynamic) == 6194 and dynamic.issubset(set(m['current_cold_extra_protected_files']))
    extra = read_json(m['current_cold_dynamic_proof']['extra_holds_report']['path'], 'd5b251e0242ba4d8a71f1f9d1a2983b3cea96b5114147b38a589541afbbe806a')
    holdpaths = {row['path'] for row in extra['selected'] + extra['holds'] + extra['archive_holds']}
    assert len(holdpaths) == 85 and dynamic | holdpaths == set(m['current_cold_extra_protected_files'])
    assert len(cold['explicit_dynamic_candidate_intersection']) == 31
    assert len(cold['remaining_11_material_candidate_paths']) == 11
    assert not selected.intersection(cold['explicit_dynamic_candidate_intersection'] + cold['remaining_11_material_candidate_paths'])
    boundary = read_json(R / 'historical_descriptor_pin_boundary.json', '3f058fadb4933ae835dae9f2a10110436dded6dd0ea733b853a817263798c223')
    assert boundary['status'] == 'DESCRIPTOR_ONLY_NOT_CURRENT_PIN' and len(boundary['records']) == 13
    assert not {row['path'] for row in boundary['records']}.intersection(row['path'] for row in m['source_and_review_pins'])
    linkrows = []
    for dp, dn, fn in os.walk(ROOT, followlinks=False):
        for name in dn + fn:
            p = Path(dp) / name
            if p.is_symlink():
                target = p.resolve(strict=False)
                assert not any(Path(q) == target or Path(q).is_relative_to(target) for q in selected)
                linkrows.append([str(p), os.readlink(p), str(target)])
    link = dict(count=len(linkrows), sha256=hashlib.sha256(json.dumps(sorted(linkrows)).encode()).hexdigest())
    assert link == pf['symlink_screen'] and link['count'] == 687
    print('INDEPENDENT graph/old index/cold6248/critical92/link687 exclusion: matched', flush=True)

    npz = read_json(R / 'reviews/npz/exact_replay_npz_source_proof.json', 'db3e8bc3bebc453be977516a28bc4b96b1482159157301cd0a0bfe5cc12f0df2')
    npzrows = {row['path']: row for row in npz['selected']}
    actual_npz = {row['path'] for row in candidates if row['category'] == 'EXACT_DUPLICATE_OLD_WORK_COPY' and row['path'].endswith('.npz')}
    assert actual_npz == set(npzrows) and len(actual_npz) == 159
    for p in actual_npz:
        row = npzrows[p]
        seal = expected(row['original_result_manifest'])
        entries = manifest_entries(seal['path'])
        familyroot = Path(seal['path']).parent
        primary = row['retained_primary']
        assert primary['path'] in retained
        assert entries[str(Path(p).relative_to(familyroot))] == entries[str(Path(primary['path']).relative_to(familyroot))] == row['sha256']
        verification = read_json(row['original_replay_verification']['path'], row['original_replay_verification']['sha256'])
        assert verification['all_verification_checks_passed'] is True
    for row in npz['original_producer_and_verifier_source_pins'] + npz['next_current_cold_and_V8_source_static_pins']:
        expected(row)
    assert not npz['current_axial_source_directory_family_or_exact_path_literal_hits']
    maps = read_json(R / 'root_old_compensated_intermediate_proposal.json', '120c4e0fc45fc97dc042907a64f461298c29adc5b4bad9529d46e24112233eb3')
    mapset = {str(ART / 'axial-material-production-qualified-AB-compensated-20261004/AAA' / stage / name) for stage in ('map001', 'map002', 'map003') for name in ('candidate_radial.xsm', 'candidate_snapshots.xsm', 'projected_proposal.xsm')}
    assert {row['path'] for row in candidates if row['category'] == 'TERMINAL_OLD_INTERMEDIATE_PAYLOAD'} == mapset == {row['path'] for row in maps['candidates']}
    assert maps['completed_maps'] == 4 and maps['original_case_classification'] == 'VALID_MET' and maps['original_run_classification'] == 'WAITING_REFERENCE'
    assert not maps['current_cold_required_intersection'] and maps['original_results_immutable'] is True and maps['scientific_credit'] is False
    for row in maps['retained_closed_anchors_and_stage_documents']:
        assert row['path'] in retained or row['path'] in {x['path'] for x in m['source_and_review_pins']}
        expected(row)

    inputrows = read_json(R / 'material_archive_input.json', 'dfb4c46ab3b9add27c4430dfadf932285841f5bcede40958c20c52203740702b')
    inputs = {row['path']: row for row in inputrows}
    pack = read_json(R / 'packed_material_intermediate_backups.json', 'd5834da3209265f9d0f4ad571f4da0c8a570558cfe39b7120750f5dad156aec9')
    assert pack['status'] == 'PASS' and pack['originals_removed'] == 0 and pack['input_sha256'] == 'dfb4c46ab3b9add27c4430dfadf932285841f5bcede40958c20c52203740702b'
    packed = {row['original']['path']: row for row in pack['records']}
    gzrows = {row['path']: row for row in candidates if row['category'] == 'GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'}
    assert len(inputrows) == len(inputs) == len(pack['records']) == len(packed) == len(gzrows) == 89 and set(inputs) == set(packed) == set(gzrows)
    ledger = [json.loads(line) for line in (R / 'backup_creation_ledger.jsonl').read_text().splitlines()]
    assert ledger == pack['records']
    backupobs = read_json(R / 'backup_terminal_observation.json', '67a59baa8aa87be670e84c30c58c316c478aa4dfabb4955573be2e00f28849cb')
    assert type(backupobs['exit_code']) is int and backupobs['exit_code'] == 0 and backupobs['closed'] is True
    assert backupobs['backup_report_sha256'] == pin(R / 'packed_material_intermediate_backups.json')['sha256']
    assert backupobs['files_deleted'] == 0 and backupobs['scientific_credit'] is False and backupobs['stderr_bytes'] == pin(R / 'backup.stderr')['size'] == 0
    assert pin(backupobs['stdout_path'])['sha256'] == backupobs['stdout_sha256']
    backupstdout_rows = [json.loads(line) for line in (R / 'backup.stdout').read_text().splitlines()]
    assert backupstdout_rows[:-1] == [dict(backups_completed=i, total=89) for i in range(1, 90)]
    backupstdout = backupstdout_rows[-1]
    assert backupstdout['backups'] == 89 and backupstdout['originals_removed'] == 0
    gzproofs = []
    actual = []
    for i, row in enumerate(candidates):
        p = Path(row['path'])
        assert p.is_absolute() and str(p) == row['path'] and '..' not in p.parts and p.is_relative_to(ART)
        fresh = expected(row)
        assert fresh['identity'][-1] == 1 and p.stat().st_blocks * 512 == row['allocated_bytes']
        category = row['category']
        if category == 'EXACT_DUPLICATE_OLD_WORK_COPY':
            primary = retained[row['retained_primary']]
            assert primary['path'] != fresh['path'] and primary['identity'][:2] != fresh['identity'][:2]
            assert (primary['size'], primary['sha256']) == (fresh['size'], fresh['sha256'])
        elif category == 'TERMINAL_OLD_INTERMEDIATE_PAYLOAD':
            proof = row['historical_payload_proof']
            assert proof['format'] == 'JSON_SHA256_MAP' and proof['path'] == str(p.parent / 'result.json') and proof['key'] == p.name
            record = read_json(proof['path'], proof['sha256'])
            assert record['classification'] == 'SEALED_STAGE_OUTPUTS' and record['sha256'][p.name] == fresh['sha256']
        else:
            relative = p.relative_to(ART)
            assert relative.parts[0] in ('d4a-final-four-fuel-temperature-run-20261002', 'd4a-remaining-fuel-temperature-run-20261001', 'd4a-remaining-temperature-run-20261001') and relative.name == 'tape30' and relative.parent.name in ('pendf', 'groupr')
            original = dict(row)
            for key in ('category', 'compressed_backup', 'restoration'):
                original.pop(key)
            assert original == inputs[str(p)] == packed[str(p)]['original']
            backup = row['compressed_backup']
            gp = Path(backup['path'])
            assert gp == R / 'packed_material_intermediates' / (str(relative) + '.gz')
            saved = expected(backup)
            assert gp.stat().st_blocks * 512 == packed[str(p)]['backup']['allocated_bytes']
            assert {key: packed[str(p)]['backup'][key] for key in ('path', 'identity', 'size', 'sha256')} == backup
            assert backup['path'] in retained
            proof = row['historical_payload_proof']
            assert proof['format'] == 'NJOY_RECEIPT_OUTPUT' and proof['path'] == str(p.parent / 'receipt.json')
            receipt = read_json(proof['path'], proof['sha256'])
            assert type(receipt['returncode']) is int and receipt['returncode'] == 0 and receipt['output_sha256'] == fresh['sha256']
            seal = pin(proof['result_manifest_path'])
            assert seal['sha256'] == proof['result_manifest_sha256'] and Path(seal['path']).parent == ART / relative.parts[0]
            assert manifest_entries(seal['path'])[str(p.relative_to(Path(seal['path']).parent))] == fresh['sha256']
            h = hashlib.sha256()
            length = 0
            with gzip.open(gp, 'rb') as stream:
                while block := stream.read(4 * 1024**2):
                    length += len(block)
                    assert length <= fresh['size'], str(gp)
                    h.update(block)
            assert (length, h.hexdigest()) == (fresh['size'], fresh['sha256'])
            assert identity(gp) == saved['identity']
            assert packed[str(p)]['verified_decompressed'] == dict(size=length, sha256=h.hexdigest())
            gzproofs.append(dict(original=fresh, compressed=saved, independently_decompressed=dict(size=length, sha256=h.hexdigest())))
            if len(gzproofs) % 15 == 0:
                print('INDEPENDENT complete gzip raw-byte verification:', len(gzproofs), 'of89', flush=True)
        actual.append(fresh)
    assert actual == pf['verified_candidates'] and len(gzproofs) == 89
    assert sum(packed[p]['backup']['allocated_bytes'] for p in packed) == pack['compressed_allocated_bytes'] == m['compressed_allocated_bytes'] == 2640285696
    assert m['expected_nominal_net_removed_allocated_bytes'] == m['allocated_bytes'] - m['compressed_allocated_bytes'] == 10274607104
    assert sum(row['allocated_bytes'] for row in inputs.values()) == pack['raw_allocated_bytes'] == 8454860800
    print('INDEPENDENT selected265 full raw-byte and compressed89 verification: matched', flush=True)

    priorpaths = sorted(ROOT.joinpath('validation').glob('storage_cleanup*/manifest.json'))
    priorpaths = [p for p in priorpaths if p != R / 'manifest.json']
    priorpaths.append(ROOT / 'validation/storage_review_more_20261008/exact_retirement_manifest.json')
    old_primary_edges = []
    selected_by_path = {row['path']: row for row in candidates}
    for oldp in priorpaths:
        old = read_json(oldp)
        def walk(value, role=''):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in ('duplicate_primary', 'retained_primary', 'primary'):
                        path = item['path'] if isinstance(item, dict) and 'path' in item else item if isinstance(item, str) else None
                        if path in selected:
                            assert selected_by_path[path]['category'] == 'GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE', (str(oldp), key, path)
                            if isinstance(item, dict):
                                assert item.get('expected_sha256', item.get('sha256')) == selected_by_path[path]['sha256']
                            old_primary_edges.append(dict(manifest=str(oldp), key=key, primary=path, required_restore_first=selected_by_path[path]['compressed_backup']['path']))
                    walk(item, key)
            elif isinstance(value, list):
                for item in value:
                    walk(item, role)
        walk(old)
    assert len({edge['primary'] for edge in old_primary_edges}) == 89
    for p, record in PINS.items():
        assert identity(p) == record['identity'], p
    after = inventory(selected)
    assert after == before == BASELINE, ('final full inventory', after)
    assert not (R / 'cleanup_result.json').exists() and not (R / 'retirement_ledger.jsonl').exists()
    report = dict(
        schema='SPOT_NINTH_INDEPENDENT_ACTUAL_FULL_PREFLIGHT_REVIEW_V1', status='PASS',
        manifest_sha256=MANIFEST_SHA, preflight_sha256=PREFLIGHT_SHA,
        expectedwholebaseline=BASELINE, expected_whole_baseline=BASELINE,
        preservation_baseline=BASELINE, nonselected_before=before, nonselected_after=after,
        cleanup_source_sha256=m['cleanup_source_sha256'], source_review_sha256=pin(R / 'reviews/final_lossless_source/independent_lossless_archive_source_review.json')['sha256'],
        source_and_review_full_fresh_pins=4980, retained_primaries_full_fresh_pins=336,
        selected_count=265, categories=counts, verified_candidates_match_actual_root_preflight=True,
        all_265_originals_present=True, all_89_gzip_backups_full_compressed_SHA_and_independently_decompressed_size_SHA_verified=True,
        independent_gzip_records=gzproofs, independently_decompressed_total_bytes=sum(x['independently_decompressed']['size'] for x in gzproofs),
        actual_backup_report_sha256=pin(R / 'packed_material_intermediate_backups.json')['sha256'],
        actual_backup_tool_receipt=backupobs, actual_preflight_tool_receipt=obs,
        old_restore_primary_dependency_edges=old_primary_edges,
        old_restore_primary_unique_count=89, old_restore_order='Restore the 89 raw paths losslessly from the retained gzip primaries before running previous rounds exact-duplicate restorers; no gzip restoration depends on deleted raw data.',
        current_closure=close, current_graph_full_static_parse=True, current_graph_requirement_rows=235528,
        current_cold_protected_paths=6248, original_42_material_seed_candidates_held=True,
        symlink_screen=link, historical_descriptor_rows_not_claimed_current_fresh_pins=13,
        removed_allocated_bytes=m['allocated_bytes'], preserved_compressed_allocated_bytes=m['compressed_allocated_bytes'], nominal_net_allocated_bytes=m['expected_nominal_net_removed_allocated_bytes'],
        retained_original_classifications=dict(compensated_case='VALID_MET', compensated_run='WAITING_REFERENCE', map_candidate_output='SEALED_STAGE_OUTPUTS', historical_only=True),
        limitations=['Nine old compensated proposal payloads have no promised lossless restoration; their original closed parent/final states, results, source and reproduction records remain retained. Any historical full-stage replay requiring retired payload paths must be restored or rebuilt before execution.', 'Five iterative working copies have no original candidate manifest; they are supported by fresh byte equality plus retained original recipes/logs. Three other legacy copies have manifest-bound retained primaries. No missing historic manifest or failed whole-run classification is converted to a fresh PASS.', 'Whole nonselected evidence is a full pathname/inode/mode/size/mtime/ctime/linkcount inventory, not a full content SHA of every unselected project file. All 4980 source/review files, 336 kept primaries and 265 selected files are independently fully hashed. Cold6194 metadata references are static protection, not scientific/API admission.'],
        files_deleted=0, restore_or_pack_or_root_preflight_or_apply_executed=False,
        scientific_API_imported=False, PREP_or_RUN_executed=False, formal_or_ART_writes=False,
        new_scientific_credit=False, project_write_scope='None; independent script and reports are in TMP only.',
        independent_hash_read_unique_files=len(PINS), independent_hash_read_bytes=BYTES,
        audit_source_sha256=pin(Path(__file__))['sha256'], elapsed_seconds=time.monotonic()-START)
    TMP.mkdir(parents=True, exist_ok=True)
    details = TMP / 'independent_fresh_full_pins.json'
    with details.open('x') as stream:
        json.dump(dict(status='PASS', manifest_sha256=MANIFEST_SHA, preflight_sha256=PREFLIGHT_SHA, records=list(PINS.values())), stream, indent=2)
        stream.write('\n')
    report['independent_fresh_full_pins_sha256'] = hashlib.sha256(details.read_bytes()).hexdigest()
    output = TMP / 'independent_preflight_review.json'
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status='PASS', report=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest(), candidates=265, sourcepins=4980, kept=336, gzip=89, whole_baseline=after, elapsed_seconds=report['elapsed_seconds'])), flush=True)

if __name__ == '__main__':
    main()
