#!/usr/bin/env python3
"""Freeze the complete reviewed Source candidate. No child, import, or solver."""
import hashlib
import json
import os
from pathlib import Path
import stat
import ast

BASE=Path(__file__).resolve().parent
TARGET=BASE/'COMPLETE_WARM_A_CANDIDATE_SOURCE_FREEZE.json'

def pin(path):
    path=Path(path);s=path.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if not stat.S_ISREG(s.st_mode):raise RuntimeError('only regular complete package files')
    with path.open('rb') as stream:
        def opened():
            s=os.fstat(stream.fileno());return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        if opened()!=before:raise RuntimeError('opened7ID')
        sha=hashlib.file_digest(stream,'sha256').hexdigest()
        if opened()!=before:raise RuntimeError('completeEOF7ID')
    s=path.lstat()
    if [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=before:raise RuntimeError('after7ID')
    return dict(path=str(path),bytes=before[4],sha256=sha,seven_id=before)

def main():
    if TARGET.exists()or TARGET.is_symlink():raise RuntimeError('immutable freeze exists, no overwrite/retry')
    binding=json.loads((BASE/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json').read_text())
    for row in binding['fixed_current_pins']:
        actual=pin(row['path'])
        if (actual['bytes'],actual['sha256'],actual['seven_id'])!=(row['size_bytes'],row['sha256'],row['identity']):
            raise RuntimeError('actual current dependency changed before freeze')
    for path in BASE.glob('*.py'):ast.parse(path.read_text())
    review=json.loads((BASE/'INDEPENDENT_FINAL_WARM_A_SOURCE_REVIEW.json').read_text())
    if review['Source_only_can_freeze'] is not True or review['actual_controls_or_transport_executed'] is not False:
        raise RuntimeError('actual independent final Source review needed, never numeric PASS')
    files=[pin(p)for p in sorted(BASE.iterdir())if p.is_file()]
    value=dict(schema='COMPLETE_CURRENT_WARM_A_SOURCE_CANDIDATE_IMMUTABLE_FREEZE_V2',files=files,
      actual_dependency_full_EOF_pins=binding['fixed_current_pins'],
      current17_pending=binding['current17_pending'],current17_actual_status=binding['current17_actual_status'],
      current_CLE_entry_controls_executed=False,warm_A_transport_executed=False,
      fixed_Source_candidate_only=True,old_PASS_inherited=False,
      single_plane_native_producer_qualified=False,three_plane_qualified=False,GLOBAL_qualified=False,
      rank_qualified=False,online_BOOT_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    with TARGET.open('x') as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    print(json.dumps(dict(status='SOURCE_ONLY_FROZEN_ENTRY_CONTROLS_PENDING',freeze=pin(TARGET),files=len(files),dependency_pins=len(binding['fixed_current_pins']))))
if __name__=='__main__':main()
