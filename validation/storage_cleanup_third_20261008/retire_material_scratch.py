"""Retire only an explicit, checked list of old material-processing scratch files."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
OUT = Path(__file__).resolve().parent
PROTECT = ROOT / 'validation/storage_review_more_20261008/normalized_protection_index.json'
ROOT_NAMES = (
    'd4a-final-four-fuel-temperature-run-20261002',
    'd4a-remaining-temperature-run-20261001',
    'd4a-remaining-fuel-temperature-run-20261001',
    'd4a-actual-temperature-library-run-20261003',
)
STAGES = {'pendf', 'groupr', 'dragr'}
SCRATCH = {'tape22', 'tape23', 'tape24', 'tape25', 'tape26', 'tape35'}


def write(name, data):
    p = OUT / name
    if p.exists():
        raise ValueError(f'will not overwrite evidence: {p}')
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]


def digest(p):
    before = identity(p)
    if not stat.S_ISREG(before[2]):
        raise ValueError(f'not a regular file: {p}')
    h = hashlib.sha256()
    with p.open('rb') as f:
        if [os.fstat(f.fileno()).st_dev, os.fstat(f.fileno()).st_ino] != before[:2]:
            raise ValueError('opened a different inode')
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    if identity(p) != before:
        raise ValueError(f'changed while reading: {p}')
    return dict(path=str(p), identity=before, sha256=h.hexdigest(), bytes=before[3])


def inventory(excluded):
    """A compact fingerprint of every other file, link and directory path."""
    h = hashlib.sha256()
    counts = dict(regular_files=0, symlinks=0, directories=0)
    for parent, dirs, files in os.walk(ROOT, followlinks=False):
        dirs.sort(); files.sort()
        dirs[:] = [n for n in dirs if Path(parent) / n != OUT]
        for n in sorted(dirs + files):
            p = Path(parent) / n
            if str(p) in excluded:
                continue
            s = p.lstat()
            rel = str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):
                row = [rel, identity(p), os.readlink(p)]; counts['symlinks'] += 1
            elif stat.S_ISDIR(s.st_mode):
                row = [rel, 'directory']; counts['directories'] += 1
            elif stat.S_ISREG(s.st_mode):
                row = [rel, identity(p)]; counts['regular_files'] += 1
            else:
                raise ValueError(f'unsupported file type: {p}')
            h.update(json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode() + b'\n')
    return dict(sha256=h.hexdigest(), **counts)


def capacity():
    k = int(subprocess.check_output(['/usr/bin/du', '-k', '-s', str(ROOT)], text=True).split()[0])
    return dict(project_allocated_bytes=k * 1024, disk_free_bytes=__import__('shutil').disk_usage(ROOT).free)


def plan():
    protection = json.loads(PROTECT.read_text())
    protected = set(protection['protected_files']) | set(protection['inbound_alias_targets'])
    prefixes = [Path(p) for p in protection['protected_directories']]
    candidates = []
    for name in ROOT_NAMES:
        root = ART / name
        seals = {}
        for line in (root / 'result.sha256').read_text().splitlines():
            sha, member = line.split(maxsplit=1)
            seals[member.lstrip('*')] = sha
        for p in sorted(root.rglob('tape*')):
            category = None
            if p.parent.name in STAGES and p.name in SCRATCH:
                category = 'material_stage_scratch'
            elif name == ROOT_NAMES[-1] and p.name == 'tape30' and p.parent.parent.name == 'merge' and re.fullmatch(r'(0[1-9]|1[0-9]|2[0-7])-.+', p.parent.name):
                category = 'superseded_cumulative_merge'
            if category is None:
                continue
            ident = identity(p)
            if not stat.S_ISREG(ident[2]) or ident[6] != 1:
                raise ValueError('candidate is linked or not regular')
            if str(p) in protected or any(p.is_relative_to(q) for q in prefixes):
                raise ValueError(f'protected candidate: {p}')
            receipt = p.parent / 'receipt.json'
            if json.loads(receipt.read_text())['returncode'] != 0:
                raise ValueError('stage did not finish successfully')
            deck = p.parent / 'input.in'
            if category == 'material_stage_scratch' and (not deck.is_file() or not (p.parent / 'tape30').is_file()):
                raise ValueError('missing retained deck or stage output')
            candidates.append(dict(path=str(p), category=category, identity=ident,
                allocated_bytes=p.stat().st_blocks * 512,
                historical_sha256=seals.get(str(p.relative_to(root))),
                historical_seal=digest(root / 'result.sha256'),
                retained_stage_receipt=digest(receipt),
                retained_deck=digest(deck) if deck.is_file() else None))
    selected = {r['path'] for r in candidates}
    links = []
    for parent, dirs, files in os.walk(ROOT, followlinks=False):
        for n in dirs + files:
            p = Path(parent) / n
            if p.is_symlink():
                target = str(p.resolve())
                if target in selected or any(Path(q).is_relative_to(Path(target)) for q in selected):
                    raise ValueError(f'live symlink enters selected path: {p}')
                links.append([str(p), os.readlink(p), target])
    write('manifest.json', dict(schema='SPOT_THIRD_EXACT_MATERIAL_SCRATCH_RETIREMENT_V1',
        candidates=candidates, protection_index=digest(PROTECT),
        fresh_project_symlink_count=len(links), symlink_inventory_sha256=hashlib.sha256(json.dumps(sorted(links)).encode()).hexdigest(),
        all_axial_material_artifacts_excluded=True, old_full_stage_replay_retired=True,
        retained_tapes=[20, 21, 27, 30], final_merge_retained='merge/28-U238/tape30', files_deleted=0))
    print(json.dumps(dict(candidate_files=len(candidates), logical_bytes=sum(r['identity'][3] for r in candidates), allocated_bytes=sum(r['allocated_bytes'] for r in candidates))))


def preflight():
    m = json.loads((OUT / 'manifest.json').read_text())
    if digest(PROTECT) != m['protection_index']:
        raise ValueError('protection index changed')
    selected = {r['path'] for r in m['candidates']}
    before = inventory(selected)
    verified = []
    for i, r in enumerate(m['candidates'], 1):
        p = Path(r['path']); d = digest(p)
        if d['identity'] != r['identity'] or (r['historical_sha256'] and d['sha256'] != r['historical_sha256']):
            raise ValueError(f'candidate identity or historical digest mismatch: {p}')
        verified.append(d)
        if i % 100 == 0:
            print(json.dumps(dict(fresh_candidates_checked=i)), flush=True)
    retained = []
    for name in ROOT_NAMES:
        root = ART / name
        seals = dict(line.split(maxsplit=1)[::-1] for line in (root / 'result.sha256').read_text().splitlines())
        for p in sorted(root.rglob('tape30')):
            if str(p) in selected or not p.is_file():
                continue
            d = digest(p); expected = seals.get(str(p.relative_to(root)))
            if expected and expected != d['sha256']:
                raise ValueError(f'retained output does not match original seal: {p}')
            retained.append(d)
    prep = ART / 'd4a-actual-temperature-material-prepared-20261003/preparation.json'
    source_paths = []
    for r in json.loads(prep.read_text())['sources']:
        d = digest(Path(r['path']))
        if d['sha256'] != r['sha256']:
            raise ValueError('final material source changed')
        source_paths.append(d)
    if inventory(selected) != before:
        raise ValueError('noncandidate files changed during preflight')
    write('preflight.json', dict(status='PASS', manifest_sha256=digest(OUT / 'manifest.json')['sha256'],
        verified_candidates=verified, retained_stage_outputs=retained, retained_final_material_sources=source_paths,
        preservation_baseline=before, capacity_before=capacity(), files_deleted=0,
        current_INPUT_API_rerun=False, all_nonselected_file_identity_fingerprint_checked=True))
    print(json.dumps(dict(status='PREFLIGHT_PASS', candidate_files=len(verified), retained_stage_outputs=len(retained), final_material_sources=len(source_paths))))


def apply(manifest_sha, preflight_sha):
    start = time.monotonic()
    if digest(OUT / 'manifest.json')['sha256'] != manifest_sha or digest(OUT / 'preflight.json')['sha256'] != preflight_sha:
        raise ValueError('Root-observed preflight/manifest hashes required')
    m = json.loads((OUT / 'manifest.json').read_text()); pre = json.loads((OUT / 'preflight.json').read_text())
    selected = {r['path'] for r in m['candidates']}
    if pre['status'] != 'PASS' or pre['manifest_sha256'] != manifest_sha or inventory(selected) != pre['preservation_baseline']:
        raise ValueError('preservation baseline changed')
    if [r['path'] for r in pre['verified_candidates']] != [r['path'] for r in m['candidates']]:
        raise ValueError('candidate list changed')
    for r in pre['verified_candidates'] + pre['retained_stage_outputs'] + pre['retained_final_material_sources']:
        if identity(Path(r['path'])) != r['identity']:
            raise ValueError('file changed after fresh read')
    ledger = OUT / 'retirement_ledger.jsonl'
    with ledger.open('x') as f:
        for r in pre['verified_candidates']:
            p = Path(r['path'])
            if identity(p) != r['identity']:
                raise ValueError('candidate changed before unlink')
            p.unlink()
            f.write(json.dumps(dict(**r, deleted=True), ensure_ascii=False) + '\n')
            f.flush()
    after = inventory(selected)
    if after != pre['preservation_baseline'] or any(Path(p).exists() for p in selected):
        raise ValueError('post-deletion preservation check failed')
    result = dict(status='PASS', deleted_files=len(selected), removed_logical_bytes=sum(r['identity'][3] for r in m['candidates']),
        removed_allocated_bytes=sum(r['allocated_bytes'] for r in m['candidates']),
        preservation_before=pre['preservation_baseline'], preservation_after=after, capacity_before=pre['capacity_before'], capacity_after=capacity(),
        elapsed_seconds=time.monotonic()-start, original_seals_and_reports_unchanged=True,
        all_axial_material_artifacts_unchanged=True, current_INPUT_API_rerun=False, old_full_stage_replay_retired=True)
    write('cleanup_result.json', result)
    print(json.dumps(result))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('action', choices=['plan', 'preflight', 'apply'])
    p.add_argument('--manifest-sha256'); p.add_argument('--preflight-sha256'); a = p.parse_args()
    if a.action == 'plan': plan()
    elif a.action == 'preflight': preflight()
    else: apply(a.manifest_sha256, a.preflight_sha256)
