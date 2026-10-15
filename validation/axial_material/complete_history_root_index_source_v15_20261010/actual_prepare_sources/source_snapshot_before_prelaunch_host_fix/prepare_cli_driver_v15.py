"""One unprofiled normal canonical V15 prepare CLI under an external guard."""
import hashlib
import json
import os
from pathlib import Path
import runpy
import stat
import sys
import time
ROOT=Path('/Users/wen/spot')
ART=ROOT/'validation/artifacts'
TARGET=ROOT/'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_root_index_production_v15.py'
TARGET_SHA='cc4b0fda4ab63d11debee532fdfbc399f5f7a68f753e20d1cff928e607a47447'
OLD_RECEIPT=ROOT/'validation/axial_material/sender_contiguous_flux_window_source_v13_20261009/actual_component_execution_receipts/Root_actual_prepare_tool_return.json'
OLD_RECEIPT_SHA='d69437dc3f3df2fc8b36adb7c3077410e6d3052e153d4568ea7e0b52ac856f82'
PROFILE_OUT=ART/'axial-material-complete-prepare-evidence-v15-20261010'

def pin(path, wanted=None):
    path = Path(path)
    a = path.lstat()
    identity = [a.st_dev, a.st_ino, a.st_mode, a.st_nlink, a.st_size, a.st_mtime_ns, a.st_ctime_ns]
    if not stat.S_ISREG(a.st_mode):
        raise ValueError('regular pinned source required')
    with path.open('rb') as stream:
        value = hashlib.file_digest(stream, 'sha256').hexdigest()
    b = path.lstat()
    after = [b.st_dev, b.st_ino, b.st_mode, b.st_nlink, b.st_size, b.st_mtime_ns, b.st_ctime_ns]
    if identity != after or (wanted is not None and value != wanted):
        raise ValueError('pinned source changed: ' + str(path))
    return dict(path=str(path), sha256=value, identity=identity)

def main():
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed nonoptimized unprofiled prepare wrapper required')
    before=[pin(TARGET,TARGET_SHA),pin(OLD_RECEIPT,OLD_RECEIPT_SHA)]
    receipt=json.loads(OLD_RECEIPT.read_text());argv=list(receipt['input']['argv'])
    if type(receipt['terminal']['exit_code']) is not int or receipt['terminal']['exit_code']!=0 or receipt['session_closed'] is not True or len(argv)!=23 or argv[2]!='prepare-build':
        raise ValueError('actual original ten preparation arguments and closed receipt required')
    argv[1]=str(TARGET)
    if not PROFILE_OUT.is_dir() or list(PROFILE_OUT.iterdir()):
        raise ValueError('Root-created exclusive empty preparation evidence root required')
    original_argv=sys.argv;started=time.monotonic();failure=None
    try:
        sys.argv=argv[1:]
        runpy.run_path(str(TARGET),run_name='__main__')
    except BaseException as error:
        failure=repr(error);raise
    finally:
        sys.argv=original_argv
        after=[pin(TARGET,TARGET_SHA),pin(OLD_RECEIPT,OLD_RECEIPT_SHA)]
        if before!=after:raise ValueError('whole preparation sources changed')
        with (PROFILE_OUT/'child_prepare_result.json').open('x') as stream:
            json.dump(dict(schema='AXMAT_V15_NORMAL_CANONICAL_PREPARE_WRAPPER_V1',status='PREPARE_RETURNED' if failure is None else 'PREPARE_FAILED_NO_RETRY',
                actual_canonical_argv=argv,input_source_pins=before,input_source_pins_after=after,failure=failure,profile_used=False,
                actual_child_elapsed_seconds=time.monotonic()-started,canonical_cli_completed=failure is None,
                compilation_or_transport_launched=False,full86_executed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False),stream,indent=2,allow_nan=False);stream.write('\n')

if __name__=='__main__':main()
