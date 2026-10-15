"""Exact, externally pinned retirement; no directory, link or document deletion."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
REVIEW = ROOT / 'validation/storage_review_more_20261008'
OUT = ROOT / 'validation/storage_cleanup_more_20261008'
MANIFEST = REVIEW / 'exact_retirement_manifest.json'
HELPER = ROOT / 'validation/storage_cleanup_20261008/cleanup_exact_batches_apply.py'
HELPER_SHA = 'ca3aa6d669f9712b6121e5174706bdbf797da43dadc57679a6473758ffc3e5dc'
if hashlib.sha256(HELPER.read_bytes()).hexdigest() != HELPER_SHA:
    raise ValueError('reviewed ordinary-file helper changed')
old = runpy.run_path(str(HELPER))
fresh, sig, unlink_exact, write_new = [old[k] for k in ('fresh', 'sig', 'unlink_exact', 'write_new')]


def inventory():
    files, links, directories = {}, {}, []
    stack = [ROOT]
    while stack:
        base = stack.pop()
        with os.scandir(base) as entries:
            for entry in entries:
                p = Path(entry.path)
                if p in (OUT, REVIEW):
                    continue
                relative = str(p.relative_to(ROOT))
                s = entry.stat(follow_symlinks=False)
                if stat.S_ISREG(s.st_mode):
                    files[relative] = sig(s)
                elif stat.S_ISLNK(s.st_mode):
                    links[relative] = [sig(s), os.readlink(p)]
                elif stat.S_ISDIR(s.st_mode):
                    directories.append(relative)
                    stack.append(p)
                else:
                    raise ValueError('unexpected special entry: ' + relative)
    return dict(files=files, symlinks=links, directories=sorted(directories))


def identity(record):
    p = Path(record['path'])
    old['ordinary_ancestors'](p)
    s = p.lstat()
    if not stat.S_ISREG(s.st_mode) or sig(s) != record['identity']:
        raise ValueError('reviewed ordinary-file identity changed: ' + str(p))
    if 'allocated_bytes' in record and s.st_blocks * 512 != record['allocated_bytes']:
        raise ValueError('reviewed allocated bytes changed: ' + str(p))


def validate_manifest(expected):
    descriptor = fresh(MANIFEST, expected)
    m = json.loads(MANIFEST.read_text())
    rows = m['files']
    paths = {r['path'] for r in rows}
    if not rows or len(paths) != len(rows) or len(rows) != m['file_count']:
        raise ValueError('exact unique file count required')
    if sum(r['identity'][3] for r in rows) != m['logical_bytes']:
        raise ValueError('exact logical bytes required')
    if sum(r['allocated_bytes'] for r in rows) != m['allocated_bytes']:
        raise ValueError('exact allocated bytes required')
    retained = set()
    for r in rows:
        p = Path(r['path'])
        if not p.is_absolute() or '..' in p.parts or not p.is_relative_to(ART) or r['identity'][-1] != 1:
            raise ValueError('ordinary nlink1 artifact leaf required')
        if r['category'] == 'material_duplicate':
            if not re.fullmatch(r'tape[0-9]{2}', p.name) or not r.get('duplicate_primary'):
                raise ValueError('only reviewed material tape copies allowed')
            retained.add(r['duplicate_primary']['path'])
        elif r['category'] == 'old_intermediate':
            if p.name not in ('projected_proposal.xsm', 'candidate_radial.xsm', 'candidate_snapshots.xsm'):
                raise ValueError('only three reviewed intermediate XSM names allowed')
            if not r['retained_anchors']:
                raise ValueError('retained final-state anchors required')
        else:
            raise ValueError('unexpected retirement category')
        retained.update(a['path'] for a in r['retained_anchors'])
        if not re.fullmatch(r'[0-9a-f]{64}', r['expected_sha256']):
            raise ValueError('historical expected SHA required')
    if paths & retained:
        raise ValueError('candidate intersects retained state/primary')
    p = m['protection_index']
    fresh(Path(p['path']), p['sha256'])
    protection = json.loads(Path(p['path']).read_text())
    protected = set(protection['protected_files']) | set(protection['inbound_alias_targets'])
    prefixes = [Path(p) for p in protection['protected_directories']]
    for r in rows:
        candidate = Path(r['path'])
        if r['path'] in protected or any(candidate.is_relative_to(p) for p in prefixes):
            raise ValueError('candidate intersects current protected contract')
        identity(r)
    for d in m['metadata_pins']:
        fresh(Path(d['path']), d['sha256'])
    return m, descriptor


def no_inbound_aliases(paths, baseline):
    for relative in baseline['symlinks']:
        if os.path.realpath(ROOT / relative) in paths:
            raise ValueError('project alias points to selected leaf')


def preflight(expected):
    started = time.monotonic()
    if os.path.lexists(OUT):
        raise ValueError('exclusive observation directory already exists')
    m, descriptor = validate_manifest(expected)
    baseline = inventory()
    selected = {r['path'] for r in m['files']}
    no_inbound_aliases(selected, baseline)
    OUT.mkdir()
    write_new(OUT / 'preservation_baseline.json', baseline)
    baseline_owner = fresh(OUT / 'preservation_baseline.json')
    retained, records = {}, []
    for n, r in enumerate(m['files'], 1):
        identity(r)
        candidate = fresh(Path(r['path']), r['expected_sha256'])
        if candidate['identity'] != r['identity'] or candidate['identity'] != baseline['files'][str(Path(r['path']).relative_to(ROOT))]:
            raise ValueError('candidate changed during preflight')
        for anchor in r['retained_anchors'] + ([r['duplicate_primary']] if r.get('duplicate_primary') else []):
            identity(anchor)
            if anchor['path'] not in retained:
                actual = fresh(Path(anchor['path']), anchor['expected_sha256'])
                if actual['identity'] != anchor['identity']:
                    raise ValueError('retained anchor changed during preflight')
                retained[anchor['path']] = actual
            actual = retained[anchor['path']]
            if actual['sha256'] != anchor['expected_sha256'] or actual['identity'] != anchor['identity']:
                raise ValueError('inconsistent retained anchor owner')
        if r.get('duplicate_primary'):
            primary = retained[r['duplicate_primary']['path']]
            if primary['sha256'] != candidate['sha256'] or primary['bytes'] != candidate['bytes']:
                raise ValueError('material copy and retained primary differ')
        records.append(dict(candidate=candidate, category=r['category'], historical_proofs=r['historical_proofs'],
                            duplicate_primary=r.get('duplicate_primary'), retained_anchors=r['retained_anchors']))
        if n % 50 == 0 or n == len(m['files']):
            print(json.dumps(dict(preflight_checked=n, total=len(m['files']), elapsed_seconds=time.monotonic() - started)), flush=True)
    for d in m['metadata_pins']:
        fresh(Path(d['path']), d['sha256'])
    if inventory() != baseline:
        raise ValueError('retained workspace changed during preflight; no deletions performed')
    write_new(OUT / 'preflight.json', dict(schema='SPOT_MORE_EXACT_RETIREMENT_PREFLIGHT_V1', status='PASS',
        manifest=descriptor, candidates=records, retained_fresh_contents=retained, baseline=baseline_owner,
        file_count=len(records), logical_bytes=m['logical_bytes'], allocated_bytes=m['allocated_bytes'],
        material_duplicate_files=sum(r['category'] == 'material_duplicate' for r in records),
        intermediate_files=sum(r['category'] == 'old_intermediate' for r in records),
        all_selected_and_retained_contents_freshly_hashed=True, deleted_files=0, elapsed_seconds=time.monotonic() - started))
    print(json.dumps(dict(status='PREFLIGHT_PASS_NO_DELETIONS', preflight=fresh(OUT / 'preflight.json'))), flush=True)


def apply(expected, preflight_sha):
    started = time.monotonic()
    m, manifest = validate_manifest(expected)
    fresh(OUT / 'preflight.json', preflight_sha)
    pre = json.loads((OUT / 'preflight.json').read_text())
    if pre['status'] != 'PASS' or pre['deleted_files'] != 0 or pre['manifest']['sha256'] != expected:
        raise ValueError('complete externally observed preflight required')
    if [r['path'] for r in m['files']] != [r['candidate']['path'] for r in pre['candidates']]:
        raise ValueError('preflight exact deletion set/order differs')
    for r in pre['candidates']:
        identity(r['candidate'])
    for r in pre['retained_fresh_contents'].values():
        identity(r)
    fresh(OUT / 'preservation_baseline.json', pre['baseline']['sha256'])
    baseline = json.loads((OUT / 'preservation_baseline.json').read_text())
    if inventory() != baseline:
        raise ValueError('workspace changed since preflight; no deletion started')
    no_inbound_aliases({r['path'] for r in m['files']}, baseline)
    with (OUT / 'retirement_ledger.jsonl').open('x') as ledger:
        for n, r in enumerate(pre['candidates'], 1):
            unlink_exact(r['candidate'])
            ledger.write(json.dumps(dict(sequence=n, action='ordinary_leaf_unlinked', absent_after_unlink=True, **r), allow_nan=False) + '\n')
            ledger.flush()
            os.fsync(ledger.fileno())
            if n % 50 == 0 or n == len(pre['candidates']):
                print(json.dumps(dict(deleted_files=n, total=len(pre['candidates']))), flush=True)
    for r in pre['candidates']:
        del baseline['files'][str(Path(r['candidate']['path']).relative_to(ROOT))]
    after = inventory()
    if after != baseline:
        changed = [p for p in set(after['files']) | set(baseline['files']) if after['files'].get(p) != baseline['files'].get(p)]
        write_new(OUT / 'preservation_failure.json', dict(changed_retained_paths=changed,
            symlinks_unchanged=after['symlinks'] == baseline['symlinks'], directory_paths_unchanged=after['directories'] == baseline['directories']))
        raise ValueError('postcleanup preservation mismatch; inspect recorded facts')
    for d in m['metadata_pins']:
        fresh(Path(d['path']), d['sha256'])
    result = dict(schema='SPOT_MORE_EXACT_RETIREMENT_ACTUAL_V1', status='PASS', manifest_sha256=expected,
        preflight_sha256=preflight_sha, deleted_files=pre['file_count'],
        material_duplicate_files=pre['material_duplicate_files'], intermediate_files=pre['intermediate_files'],
        removed_logical_bytes=pre['logical_bytes'], removed_allocated_bytes=pre['allocated_bytes'],
        retained_regular_paths=len(after['files']), retained_symlinks=len(after['symlinks']),
        retained_directory_paths=len(after['directories']), all_nonselected_file_identities_unchanged=True,
        all_symlink_entries_unchanged=True, directory_paths_unchanged=True,
        historical_seals_and_results_unchanged=True, old_full_intermediate_replay_retired=True,
        physics_execution=False, current_INPUT_revalidation_still_required=True,
        elapsed_seconds=time.monotonic() - started)
    write_new(OUT / 'cleanup_result.json', result)
    print(json.dumps(result), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=('preflight', 'apply'))
    p.add_argument('--manifest-sha256', required=True)
    p.add_argument('--preflight-sha256')
    a = p.parse_args()
    if not re.fullmatch(r'[0-9a-f]{64}', a.manifest_sha256):
        raise ValueError('root-observed manifest SHA required')
    if a.mode == 'preflight':
        preflight(a.manifest_sha256)
    else:
        if not a.preflight_sha256 or not re.fullmatch(r'[0-9a-f]{64}', a.preflight_sha256):
            raise ValueError('root-observed preflight SHA required')
        apply(a.manifest_sha256, a.preflight_sha256)
