from pathlib import Path
import os, json, hashlib, stat

ROOT = Path('/Users/wen/spot')
OUT = Path('/private/tmp/spot_storage_twentieth_root_20261009')
NAMES = ('projected_proposal.xsm', 'candidate_radial.xsm', 'candidate_snapshots.xsm',
         'candidate_axial.xsm', 'candidate_system.xsm', 'parent_for_checker.xsm')
DATES = ('20260925', '20260926', '20260926', '20260927', '20260927')
protected = set(json.loads((OUT/'graph_protected_paths.json').read_bytes()))

def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def parse_manifest(p):
    result = {}
    for line in p.read_text().splitlines():
        if not line.strip():
            continue
        sha, name = line.split(None, 1)
        name = name.strip().lstrip('*')
        assert len(sha) == 64
        result[name.removeprefix('./')] = sha
    return result

rows = []
manifests = []
for index, day in enumerate(DATES, 1):
    directory = ROOT/'validation/artifacts'/f'd4a-scattering-mesh12-picard-map{index}-{day}'
    pins = {}
    for name in ('result.sha256', 'input_manifest.sha256', 'output_manifest.sha256'):
        path = directory/name
        pins[name] = parse_manifest(path)
        manifests.append({'path': str(path), 'sha256': digest(path), 'identity': identity(path)})
    for name in NAMES:
        path = directory/name
        before = identity(path)
        assert stat.S_ISREG(before[2]) and before[6] == 1, str(path)
        assert str(path) not in protected and str(path.resolve()) not in protected
        source_pins = {m: values[name] for m, values in pins.items() if name in values}
        assert source_pins, str(path)
        sha = digest(path)
        assert set(source_pins.values()) == {sha}, (str(path), source_pins, sha)
        assert identity(path) == before
        rows.append({'path': str(path), 'identity': before, 'size_bytes': before[3],
                     'allocated_bytes': path.stat().st_blocks*512, 'sha256': sha,
                     'original_manifest_sha256s': source_pins,
                     'category': 'early_map_recomputable_working_intermediate',
                     'not_a_closed_state': True})

chosen = {x['path'] for x in rows}
chosen_inodes = {(x['identity'][0], x['identity'][1]) for x in rows}
links = []
other_hardlinks = []
for base, dirs, files in os.walk(ROOT, followlinks=False):
    if base == str(ROOT):
        dirs[:] = [d for d in dirs if d != '.git']
    for name in files + [d for d in dirs if (Path(base)/d).is_symlink()]:
        path = Path(base)/name
        s = path.lstat()
        if stat.S_ISLNK(s.st_mode):
            if str(path.resolve()) in chosen:
                links.append({'path': str(path), 'text': os.readlink(path), 'target': str(path.resolve())})
        elif stat.S_ISREG(s.st_mode) and (s.st_dev, s.st_ino) in chosen_inodes and str(path) not in chosen:
            other_hardlinks.append(str(path))
assert not links and not other_hardlinks, (links, other_hardlinks)

result = {'schema': 'SPOT_R20_ROOT_PROPOSED_30_INTERMEDIATES_FULL_BYTE_PROOF_V1',
          'status': 'PROVEN_BYTES_AND_PREFILTER_ONLY_PENDING_INDEPENDENT_DEPENDENCY_RESULTS_REVIEW',
          'candidates': rows, 'original_manifests': manifests,
          'total_size_bytes': sum(x['size_bytes'] for x in rows),
          'total_allocated_bytes': sum(x['allocated_bytes'] for x in rows),
          'no_project_symlinks_or_other_hardlinks_to_candidates': True,
          'all_bootstrap_and_closed_states_and_maps6_to9_kept': True,
          'requires_isolated_recomputation_for_early_whole_stage_revalidation': True,
          'science_business_executed': False, 'deletions_performed': 0}
(OUT/'proposed_candidates_full_byte_proof.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'candidate_count': len(rows), 'logical_bytes': result['total_size_bytes'],
                  'allocated_bytes': result['total_allocated_bytes'], 'symlink_dependents': len(links),
                  'all_original_manifest_pins_match': True}))
