#!/usr/bin/env python3
"""Root-selected B run, once, after restoration of the original storage budget.

The original failed B run remains preserved. This invokes the frozen V2 host,
which must admit the complete initial reserve before any runtime or child exists.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
PACKAGE = REC / 'native_warm_B_initial_storage_reserve_source_v2'
PYTHON = '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
PREREQUISITES = [
    ('seventeen', ROOT / 'validation/artifacts/axial-material-new-ROOT64-full-connected17-expected-planes-v4-20261012/Root_actual_compile_only_summary.json',
     '12702c844a5b76b15a6331d0059003ad945ef8695402c60c9dd00a182ed90dcc',
     [16777234, 49772671, 33188, 1, 7605333, 1791741987612469808, 1791741987612469808]),
    ('entry-controls', ROOT / 'validation/artifacts/axial-material-current-warm-B-CLE-entry-controls-20261012-v1/Root_actual_entry_controls_summary.json',
     'a0acac4ded2b78a9f24a78521a30a5a2213ef377d80a1f99ef2a14044584b5b4',
     [16777234, 49777307, 33188, 1, 7388028, 1791744814192388888, 1791744814192388888]),
    ('source-freeze', PACKAGE / 'COMPLETE_WARM_B_INITIAL_STORAGE_SOURCE_FREEZE.json',
     '7ab72f62a6d4669e8daae86eeeb05f4cbe9fef0ea297c01853429286c43678f5',
     [16777234, 49779732, 33188, 1, 4456, 1791746346374781738, 1791746346374781738]),
]

def identity(st):
    return [st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns]

def main():
    if Path(sys.executable).resolve() != Path(PYTHON).resolve():
        raise RuntimeError('Original Python required')
    command = [PYTHON, '-B', str(PACKAGE / 'run_current_native_warm_B.py')]
    for prefix, path, expected_sha, expected_identity in PREREQUISITES:
        before = identity(path.lstat())
        if before != expected_identity or not stat.S_ISREG(before[2]):
            raise RuntimeError('Owning selected prerequisite identity differs: ' + str(path))
        with path.open('rb') as stream:
            if identity(os.fstat(stream.fileno())) != before:
                raise RuntimeError('Opened prerequisite identity differs')
            actual_sha = hashlib.file_digest(stream, 'sha256').hexdigest()
            if identity(os.fstat(stream.fileno())) != before:
                raise RuntimeError('EOF prerequisite identity differs')
        if identity(path.lstat()) != before or actual_sha != expected_sha:
            raise RuntimeError('Whole prerequisite bytes or identity differ')
        command += ['--' + prefix + '-summary', str(path),
                    '--' + prefix + '-sha256', expected_sha,
                    '--' + prefix + '-seven-id', json.dumps(expected_identity)]
    task_env = dict(os.environ)
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
                 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        task_env[name] = '1'
    task_env['PYTHONDONTWRITEBYTECODE'] = '1'
    os.chdir(ROOT)
    os.execve(PYTHON, command, task_env)

if __name__ == '__main__':
    main()
