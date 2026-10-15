#!/usr/bin/env python3
"""Preserve exact recovered bytes at new durable paths, without old identity claims."""
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import sys
import time
sys.dont_write_bytecode=True
ROOT=Path('/Users/wen/spot')
V=ROOT/'validation/axial_material'
sys.path.insert(0,str(V))
from run_real64_common_rank2_training import TrainingResources
D=V/'input_epoch_recovery_20261011'
INVENTORY=ROOT/'validation/artifacts/axial-material-input-epoch-recovery-v2-20261011'
OUT=ROOT/'validation/artifacts/axial-material-input-epoch-exact-copy-preservation-20261011'
DEST=D/'recovered_exact_files'
COLD=20971764748

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def main():
    start=time.monotonic()
    if OUT.exists() or DEST.exists():raise RuntimeError('fresh output and destination required; no overwrite')
    guard=TrainingResources(OUT)
    prior=json.loads((INVENTORY/'summary.json').read_text())
    baseline=prior['resource_checkpoints'][-1]
    rows=[json.loads(line) for line in (INVENTORY/'missing_endpoint_candidates.ndjson').read_text().splitlines()]
    created=0;bytes_created=0;copies={};bindings=[]
    def budget():
        if time.monotonic()-start>=600:raise RuntimeError('original metadata stage600 deadline')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20:raise RuntimeError('original SELF512 MiB')
    def pin(p):
        budget();p=Path(p);before=identity(p.stat());h=hashlib.sha256()
        with p.open('rb')as f:
            opened=identity(os.fstat(f.fileno()))
            for b in iter(lambda:f.read(1024*1024),b''):h.update(b);budget()
            eof=identity(os.fstat(f.fileno()))
        after=identity(p.stat())
        if not before==opened==eof==after:raise RuntimeError('Source changed during full EOF')
        return dict(path=str(p),sha256=h.hexdigest(),size_bytes=after[4],identity=after)
    def check():
        budget();r=guard.check()
        # Prior complete inherited account already includes original externals;
        # add all newly preserved durable bytes and a bounded metadata allowance.
        allowance=8*2**20
        if baseline['joint']['bytes']+bytes_created+allowance>=2*2**30:raise RuntimeError('joint2GiB')
        extra_original=baseline['history']['bytes']-baseline['original_guard_checks']['complete_history']['artifact_bytes']
        if r['complete_history']['artifact_bytes']+extra_original+bytes_created+COLD+allowance>=96*2**30:raise RuntimeError('history96GiB plus original cold reserve')
        if r['fresh_output']['disk_free_bytes']-COLD-2*2**30<8*2**30:raise RuntimeError('filesystem8GiB floor plus reserves')
        return r
    before=check();authority=[pin(INVENTORY/'summary.json'),pin(INVENTORY/'missing_endpoint_candidates.ndjson')]
    OUT.mkdir();DEST.mkdir()
    for row in rows:
        if not row['matching_current_byte_copies']:continue
        sha=row['expected_sha256'];origin=row['matching_current_byte_copies'][0]
        if sha not in copies:
            if pin(origin['path'])!=origin:raise RuntimeError('candidate current pin changed')
            folder=DEST/sha;folder.mkdir();destination=folder/Path(row['path']).name
            if destination.exists():raise RuntimeError('no overwrite')
            shutil.copyfile(origin['path'],destination)
            with destination.open('rb')as f:os.fsync(f.fileno())
            current=pin(destination)
            if current['sha256']!=sha or current['size_bytes']!=origin['size_bytes']:raise RuntimeError('actual copy mismatch')
            if current['identity'][1]==origin['identity'][1] or current['identity'][3]!=1:raise RuntimeError('independent ordinary Source copy required')
            if pin(origin['path'])!=origin:raise RuntimeError('origin changed after copy')
            copies[sha]=dict(current_durable_pin=current,actual_origin_pin=origin)
            bytes_created+=current['size_bytes'];created+=1
            if created%25==0:check()
        bindings.append(dict(historical_missing_path=row['path'],historical_expected_sha256=sha,
            **copies[sha],historical_identity_restored=False,current_business_admission=False))
    for p in authority:
        if pin(p['path'])!=p:raise RuntimeError('discovery authority changed')
    after=check()
    report=dict(schema='AXMAT_CURRENT_EXACT_BYTE_COPY_PRESERVATION_V1',
        status='EXACT_BYTES_PRESERVED_AT_NEW_PATHS_NOT_RUNTIME_ADMISSION',
        discovery_authority=authority,bindings=bindings,
        recovered_endpoint_count=len(bindings),unique_bytes_copies=created,
        created_regular_bytes=bytes_created,missing_endpoints_not_preserved=len(rows)-len(bindings),
        old_paths_recreated=False,old_identities_normalized=False,old_qualification_inherited=False,
        original_sources_modified=False,business_started=False,Q_qualified=False,
        online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False,
        resources_before=before,resources_after=after,original_cold_reserve_bytes=COLD,
        original_joint_and_history_baseline=baseline,
        wall_seconds=time.monotonic()-start,
        SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    with (OUT/'EXACT_BYTE_COPY_PRESERVATION.json').open('x')as f:
        json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    print(json.dumps({k:report[k]for k in ('status','recovered_endpoint_count','unique_bytes_copies','created_regular_bytes','missing_endpoints_not_preserved','wall_seconds','SELF_peak_bytes','business_started')}))

if __name__=='__main__':main()
