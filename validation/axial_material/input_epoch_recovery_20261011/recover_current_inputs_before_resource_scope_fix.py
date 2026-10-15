#!/usr/bin/env python3
"""Current byte-copy discovery; never qualify old identities or run business."""
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
V = ROOT / 'validation/axial_material'
ART = ROOT / 'validation/artifacts'
BASE = V / 'complete_history_root_index_source_v15_20261010'
sys.path.insert(0, str(V))
from run_real64_common_rank2_training import TrainingResources

OUT = ART / 'axial-material-input-epoch-recovery-20261011'
PRELAUNCH = BASE / 'actual_complete_combined_build_v31_installed6a_20261011_receipts/Root_final_prelaunch_source_input_and_reserve_check.json'
PROOF = BASE / 'actual_complete_combined_build_v31_installed6a_20261011_sources/FULL_ACTUAL_PREP_PEER_AND_ORIGINAL_SOURCE_INVERSE_PROOF.json'
FREEZE = BASE / 'actual_complete_combined_prepare_v31_installed6a_20261011_receipts/Root_actual_successful_PREP_namespace_and_streams_freeze.json'
DECL = ART / 'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v31-installed6a-20261011/declaration.json'
COLD_RESERVE = 20971764748
FRESH_RESERVE = 2 * 2**30
CAP = 600

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]

def main():
    started = time.monotonic()
    if OUT.exists() or OUT.is_symlink():
        raise RuntimeError('permanent output exists; no retry or overwrite')
    guards = TrainingResources(OUT)
    guard_sources = [Path(__file__).resolve(), V/'run_real64_common_rank2_training.py',
        V/'production_runner.py', V/'moment_order_complete_history_resource_trie_20261010.py']
    checkpoints = []

    def budget():
        if time.monotonic() - started >= CAP:
            raise RuntimeError('600 second metadata stage cap')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 512 * 2**20:
            raise RuntimeError('512 MiB SELF historical high water cap')

    def pin(path):
        budget()
        path = Path(path)
        before = identity(path.stat())
        h = hashlib.sha256()
        with path.open('rb') as f:
            opened = identity(os.fstat(f.fileno()))
            while True:
                b = f.read(1024*1024)
                if not b: break
                h.update(b)
                budget()
            eof = identity(os.fstat(f.fileno()))
        after = identity(path.stat())
        if not before == opened == eof == after:
            raise RuntimeError('input changed while hashing: '+str(path))
        return dict(path=str(path), size_bytes=after[4], sha256=h.hexdigest(),
                    identity=after)

    meta_paths = [PRELAUNCH, PROOF, FREEZE, DECL]
    initial_meta = [pin(p) for p in meta_paths]
    documents = [json.loads(p.read_text()) for p in meta_paths]
    prelaunch, proof, freeze, declaration = documents
    pins = {}
    pin_conflicts = []

    def collect(value, label):
        if isinstance(value, dict):
            if (isinstance(value.get('path'), str)
                    and isinstance(value.get('sha256'), str)
                    and isinstance(value.get('identity'), list)
                    and len(value['identity']) == 7):
                p = value['path']
                entry = dict(path=p, sha256=value['sha256'],
                    identity=value['identity'],
                    size_bytes=value.get('size_bytes', value['identity'][4]))
                if p in pins and pins[p]['pin'] != entry:
                    pin_conflicts.append(dict(path=p, source=label))
                else:
                    pins.setdefault(p, dict(pin=entry, sources=[]))['sources'].append(label)
            for child in value.values(): collect(child, label)
        elif isinstance(value, list):
            for child in value: collect(child, label)

    for d, label in zip(documents, ('prelaunch', 'Source_inverse', 'PREP_freeze', 'declaration_META')):
        collect(d, label)
    all_sha = dict(declaration['files'])
    for p, record in pins.items():
        old = all_sha.get(p)
        if old is not None and old != record['pin']['sha256']:
            pin_conflicts.append(dict(path=p, source='declaration_vs_pin'))
        all_sha.setdefault(p, record['pin']['sha256'])

    # Apparent-byte accounting includes all inherited current fresh roots,
    # external formal inputs, and this durable Source. No inode is charged twice.
    fresh_roots = [Path(x) for x in prelaunch['complete_new_participating_fresh_roots']]
    fresh_roots.append(OUT)
    external = {Path(p) for p in pins if not Path(p).is_relative_to(ART)}
    external.update(guard_sources)
    external.update(meta_paths)

    def apparent(paths, extra):
        seen = set(); total = 0; count = 0
        stack = list(paths)
        for path in extra:
            try: s = path.lstat()
            except FileNotFoundError: continue
            key = (s.st_dev, s.st_ino)
            if stat.S_ISREG(s.st_mode) and key not in seen:
                seen.add(key); total += s.st_size; count += 1
        while stack:
            budget(); directory = stack.pop()
            try:
                fd = os.open(directory, os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
            except FileNotFoundError: continue
            try:
                with os.scandir(fd) as entries:
                    for entry in entries:
                        s = entry.stat(follow_symlinks=False)
                        path = directory/entry.name
                        if stat.S_ISDIR(s.st_mode): stack.append(path)
                        elif stat.S_ISREG(s.st_mode):
                            key = (s.st_dev, s.st_ino)
                            if key not in seen:
                                seen.add(key); total += s.st_size; count += 1
            finally: os.close(fd)
        return dict(bytes=total, inode_count=count)

    def resources(label):
        budget(); original = guards.check()
        joint = apparent(fresh_roots, external)
        history = apparent([ART], external)
        free = original['fresh_output']['disk_free_bytes']
        if joint['bytes'] + 64*2**20 > 2*2**30:
            raise RuntimeError('inherited joint fresh cap/reserve')
        if history['bytes'] + COLD_RESERVE + 64*2**20 > 96*2**30:
            raise RuntimeError('complete history plus original cold reserve cap')
        if free - FRESH_RESERVE - COLD_RESERVE < 8*2**30:
            raise RuntimeError('filesystem free floor plus original reserves')
        checkpoints.append(dict(label=label, joint=joint, history=history,
            free_bytes=free, cold_reserve_bytes=COLD_RESERVE,
            fresh_reserve_bytes=FRESH_RESERVE,
            original_guard_checks=original))

    resources('before_output')
    OUT.mkdir()
    missing = {}
    existing_pin_rows = []
    counts = {}
    row_count = 0
    with (OUT/'current_inputs.ndjson').open('x', encoding='utf-8') as rows:
        for p, expected_sha in sorted(all_sha.items()):
            budget(); path = Path(p); historic = pins.get(p)
            row = dict(path=p, expected_sha256=expected_sha,
                historical_pin=historic['pin'] if historic else None)
            if not path.is_file():
                row['status'] = 'MISSING_CURRENT_ENDPOINT'
                missing[p] = row
            elif historic:
                actual = pin(path); row['current_pin'] = actual
                row['status'] = ('CURRENT_BYTES_MATCH' if actual['sha256'] == expected_sha
                                 else 'CURRENT_BYTES_DIFFER')
                names = ['device','inode','mode','nlink','size','mtime_ns','ctime_ns']
                row['historical_identity_changed_fields'] = [name for i,name in enumerate(names)
                    if actual['identity'][i] != historic['pin']['identity'][i]]
                existing_pin_rows.append(actual)
            else:
                row['status'] = 'CURRENT_PATH_PRESENT_BYTES_NOT_AUDITED'
            counts[row['status']] = counts.get(row['status'],0)+1
            rows.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
            row_count += 1
            if row_count % 4096 == 0: resources('paths_'+str(row_count))
        rows.flush(); os.fsync(rows.fileno())

    wanted_sizes = {r['historical_pin']['size_bytes'] for r in missing.values()
                    if r['historical_pin'] is not None}
    wanted_basenames = {Path(p).name for p,r in missing.items() if r['historical_pin'] is None}
    wanted_sha = {r['expected_sha256'] for r in missing.values()}
    matches = {}; hashed_bytes = 0; hashed_count = 0; scanned_count = 0
    excluded = {'.git','.aws','.codex','.agents'}
    for parent, dirs, files in os.walk(ROOT, followlinks=False):
        budget()
        dirs[:] = sorted(n for n in dirs if n not in excluded and not (Path(parent)/n).is_symlink())
        for name in files:
            path = Path(parent)/name
            s = path.lstat(); scanned_count += 1
            if not stat.S_ISREG(s.st_mode): continue
            if s.st_size not in wanted_sizes and name not in wanted_basenames: continue
            actual = pin(path); hashed_count += 1; hashed_bytes += actual['size_bytes']
            if actual['sha256'] in wanted_sha:
                matches.setdefault(actual['sha256'],[]).append(actual)
        if scanned_count//20000 > (scanned_count-len(files))//20000:
            resources('candidate_scan_'+str(scanned_count))

    recovered = 0; unknown_size = 0
    with (OUT/'missing_endpoint_candidates.ndjson').open('x',encoding='utf-8') as rows:
        for p,row in sorted(missing.items()):
            candidates = matches.get(row['expected_sha256'],[])
            if candidates: recovered += 1
            if row['historical_pin'] is None: unknown_size += 1
            result = dict(row, matching_current_byte_copies=candidates,
                status='EXACT_SAME_BYTE_COPY_FOUND' if candidates else 'NO_COPY_FOUND_IN_DECLARED_SEARCH_SCOPE',
                search_scope='all_project_regular_files_matching_expected_size' if row['historical_pin']
                    else 'all_project_regular_files_matching_any_missing_size_or_unknown_size_basename',
                old_identity_requalified=False, replacement_installed=False)
            rows.write(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n')
        rows.flush(); os.fsync(rows.fileno())
    for before in initial_meta:
        if pin(before['path']) != before: raise RuntimeError('authority META changed')
    resources('after_complete_inventory')
    summary = dict(schema='AXMAT_CURRENT_INPUT_EPOCH_COPY_DISCOVERY_V1',
        status='COMPLETE_CURRENT_DISCOVERY_ONLY_NOT_BUSINESS_QUALIFICATION',
        authority_pins=initial_meta, guard_Source_pins=[pin(p) for p in guard_sources],
        historical_device_is_not_normalized=True, canonical_path_count=len(declaration['files']),
        combined_path_count=len(all_sha), strict_historical_pin_count=len(pins),
        status_counts=counts, pin_conflicts=pin_conflicts,
        missing_endpoint_count=len(missing), exact_byte_copy_found_count=recovered,
        no_copy_found_in_scope_count=len(missing)-recovered,
        missing_unknown_size_count=unknown_size,
        project_candidates_scanned=scanned_count, candidate_files_hashed=hashed_count,
        candidate_bytes_hashed=hashed_bytes,
        all_current_existing_canonical_bytes_audited=False,
        current_Q_qualified=False, PREP_requalified=False, BUILD_executed=False,
        Native_executed=False, online_BOOT_qualified=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, goal_complete=False,
        seconds=time.monotonic()-started,
        SELF_ru_maxrss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        resource_checkpoints=checkpoints)
    with (OUT/'summary.json').open('x',encoding='utf-8') as f:
        json.dump(summary,f,ensure_ascii=False,indent=2); f.write('\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps({k:v for k,v in summary.items() if k not in
        ('authority_pins','guard_Source_pins','resource_checkpoints','pin_conflicts')},ensure_ascii=False))

if __name__ == '__main__':
    main()
