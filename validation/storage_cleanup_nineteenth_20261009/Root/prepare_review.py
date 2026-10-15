from pathlib import Path
import os, stat, json, hashlib, subprocess, collections

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
OUT = Path('/private/tmp/spot_storage_nineteenth_root_20261009')
REPORT = ROOT / 'validation/storage_cleanup_nineteenth_20261009'
WORK = ART / 'axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
GRAPH = ART / 'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
FAMILIES = {
    'axial-material-production-qualified-AB-white-trace-20261004': (8, 11),
    'axial-material-production-qualified-AB-rank1-factor-cache-20261007': (9, 12),
    'axial-material-production-qualified-AB-compensated-20261004': (1, 4),
}

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def inventory(exclude):
    files, links, dirs = [], [], []
    for base, children, names in os.walk(ROOT, followlinks=False):
        bp = Path(base)
        if bp == REPORT or bp.is_relative_to(REPORT):
            children[:] = []
            continue
        for name in list(children):
            p = bp / name
            if bp == ROOT and name in {'.git', '.agents', '.codex', '.aws'}:
                children.remove(name)
                continue
            if p == REPORT:
                children.remove(name)
                continue
            if p.is_symlink():
                if str(p) not in exclude:
                    links.append([str(p), identity(p), os.readlink(p)])
                children.remove(name)
            else:
                dirs.append(str(p))
        for name in names:
            p = bp / name
            if str(p) in exclude:
                continue
            s = p.lstat()
            if stat.S_ISLNK(s.st_mode):
                links.append([str(p), identity(p), os.readlink(p)])
            elif stat.S_ISREG(s.st_mode):
                files.append([str(p), identity(p)])
            else:
                raise AssertionError(('unusual file', str(p)))
    rows = {'files': sorted(files), 'links': sorted(links), 'directories': sorted(dirs)}
    fingerprints = {key: hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest() for key, value in rows.items()}
    return {'counts': {key: len(value) for key, value in rows.items()}, 'fingerprints': fingerprints}

def write(name, obj):
    p = OUT / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    return sha(p)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not REPORT.exists(), 'fresh report destination required'
    binding_path = WORK / 'own_rss_binding.json'
    assert sha(binding_path) == '4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930'
    assert sha(GRAPH) == '0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
    b, g = json.loads(binding_path.read_text()), json.loads(GRAPH.read_text())
    exact = set(b['files']) | {x['path'] for x in g['canonical_files']} | set(g['requirements']['paths'])
    assert len(b['files']) == 37395 and len(g['canonical_files']) == 35647
    alias_paths = {x['path'] for x in g['aliases']}
    alias_targets = {str(Path(x['target']).resolve()) for x in g['aliases']}
    ns_roots = [Path(x[k]) for x in g['namespaces'] for k in ['root', 'canonical_root']]
    def unlocked(p):
        s = str(p)
        assert s not in exact and s not in alias_paths and s not in alias_targets, ('current exact dependency', s)
        assert not any(p == x or p.is_relative_to(x) for x in ns_roots), ('current namespace', s)
    regular, links, evidence, kept = [], [], {}, []
    for family, (last_delete, last_map) in FAMILIES.items():
        aaa = ART / family / 'AAA'
        actual = sorted(x.name for x in aaa.glob('map[0-9][0-9][0-9]') if x.is_dir())
        assert actual == [f'map{i:03d}' for i in range(1, last_map + 1)], (family, actual)
        for i in range(1, last_delete + 1):
            p = aaa / f'map{i:03d}' / 'closed_snapshots.xsm'
            unlocked(p)
            before = identity(p)
            assert stat.S_ISREG(before[2]) and before[6] == 1
            seal = p.parent / 'result.json'
            j = json.loads(seal.read_text())
            assert j['classification'] == 'SEALED_STAGE_OUTPUTS'
            expected = j['sha256'][p.name]
            actual_sha = sha(p)
            assert actual_sha == expected and identity(p) == before, ('original full SHA mismatch', str(p))
            regular.append({'path': str(p), 'identity': before, 'sha256': actual_sha, 'allocated_bytes': p.lstat().st_blocks * 512, 'original_stage_seal': str(seal), 'original_stage_seal_sha256': sha(seal)})
            evidence[str(seal)] = sha(seal)
            q = aaa / f'map{i+1:03d}' / 'parent_snapshots_closed.xsm'
            unlocked(q)
            assert q.is_symlink() and q.resolve() == p
            links.append({'path': str(q), 'identity': identity(q), 'link_text': os.readlink(q), 'target': str(p)})
        for i in range(last_map - 2, last_map + 1):
            p = aaa / f'map{i:03d}' / 'closed_snapshots.xsm'
            assert p.is_file() and not p.is_symlink()
            seal = p.parent / 'result.json'
            actual_sha = sha(p)
            assert actual_sha == json.loads(seal.read_text())['sha256'][p.name]
            kept.append({'path': str(p), 'identity': identity(p), 'sha256': actual_sha, 'original_stage_seal': str(seal), 'original_stage_seal_sha256': sha(seal)})
        for i in range(last_map - 1, last_map + 1):
            q = aaa / f'map{i:03d}' / 'parent_snapshots_closed.xsm'
            assert q.is_symlink() and q.resolve().is_file()
            kept.append({'path': str(q), 'identity': identity(q), 'link_text': os.readlink(q), 'target': str(q.resolve())})
    assert len(regular) == len(links) == 18
    targets = {x['path'] for x in regular}
    expected_inbound = {x['path'] for x in links}
    inbound = []
    for base, children, names in os.walk(ROOT, followlinks=False):
        bp = Path(base)
        if bp == ROOT:
            children[:] = [x for x in children if x not in {'.git', '.agents', '.codex', '.aws'}]
        for name in children + names:
            p = bp / name
            if p.is_symlink() and str(p.resolve()) in targets:
                inbound.append(str(p))
        children[:] = [x for x in children if not (bp / x).is_symlink()]
    assert set(inbound) == expected_inbound, ('other incoming symlinks', set(inbound) ^ expected_inbound)
    selected = targets | expected_inbound
    plan = {'schema': 'SPOT_OLD_ITERATION_STATE_RETIREMENT_V1', 'scope': '18 early completed map closed states and their 18 dependent parent symlinks only', 'current_binding': {'path': str(binding_path), 'sha256': sha(binding_path), 'count': len(b['files'])}, 'current_graph': {'path': str(GRAPH), 'sha256': sha(GRAPH), 'canonical_count': len(g['canonical_files']), 'namespace_count': len(g['namespaces']), 'alias_count': len(g['aliases'])}, 'regular': regular, 'symlinks': links, 'kept_last_three_closed_and_last_two_parent_links': kept, 'stage_documents': evidence, 'incoming_symlinks_exact': sorted(inbound), 'logical_bytes': sum(x['identity'][3] for x in regular), 'allocated_bytes': sum(x['allocated_bytes'] for x in regular), 'all_existing_bootstrap_last_two_maps_and_other_results_kept': True, 'old_historical_seals_not_asserted_complete': True, 'project_written': False, 'business_executed': False}
    ps = write('fixed_candidate_plan.json', plan)
    baseline = inventory(selected)
    docs = [ROOT/'README.md', ROOT/'validation/README.md', ROOT/'validation/axial_material/last_cprime_trim_build_review_20261008/current_progress.json', ROOT/'validation/storage_review_eighteenth_20261009/REPORT.txt', ROOT/'validation/storage_review_eighteenth_20261009/Root_actual_storage_closeout.json']
    baseline['control_document_pins'] = {str(x): sha(x) for x in docs}
    baseline['candidate_plan_sha256'] = ps
    baseline['du_kib'] = int(subprocess.check_output(['du', '-sk', str(ROOT)], text=True).split()[0])
    write('protected_before.json', baseline)
    print(json.dumps({'status': 'CANDIDATE_FULL_SHA_AND_CURRENT_EXCLUSIONS_PASS_REQUIRES_INDEPENDENT_READONLY_REVIEWS', 'regular': len(regular), 'symlinks': len(links), 'allocated_gib': plan['allocated_bytes']/2**30, 'plan_sha256': ps, 'protected': baseline['counts'], 'du_kib': baseline['du_kib']}, ensure_ascii=False))

if __name__ == '__main__':
    main()
