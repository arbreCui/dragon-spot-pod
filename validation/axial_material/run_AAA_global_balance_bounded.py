"""Bound the declared read-only P0 diagnostic through the existing watchdog."""
import json
from pathlib import Path
import shutil
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
PROD=ROOT/'validation/artifacts/axial-material-production-qualified-AB-compensated-20261004'
sys.path.insert(0,str(PROD/'runtime'))
from production_runner import DiskResources,SerialExecutor,require_file,sha256


def main():
    art=ROOT/'validation/artifacts'
    out=art/'axial-material-AAA-global-transverse-balance-20261004'
    require_file(out/'declaration.json','c9df8a30cc7e3e86a26cf180eb59a5708ecc1604cce924e339baab401b7d802b')
    ce=json.loads((art/'axial-material-ce-qualified-AAA-ufs-20261004/AAA/native_result.json').read_text())
    if ce['returncode'] is None:raise ValueError('CE child must have ended')
    if (out/'driver_claim.json').exists():raise ValueError('no repeat or retry')
    (out/'AAA').mkdir();(out/'runtime').mkdir()
    shutil.copy2(PROD/'runtime/run_bounded_dragon.py',out/'runtime/run_bounded_dragon.py')
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())
    source=ROOT/'validation/axial_material/audit_AAA_global_transverse_balance.py'
    files=[Path(__file__).resolve(),source,out/'declaration.json',out/'runtime/run_bounded_dragon.py',Path(sys.executable).resolve()]
    with (out/'driver_claim.json').open('x') as stream:
        json.dump(dict(started_unix=time.time(),wall_seconds=60,threads=1,retries=0,
            files={str(p):sha256(p) for p in files},resource_roots=roots),stream,indent=2)
    resources=DiskResources(art,roots,8*2**30,24*2**30)
    executor=SerialExecutor(out,60,'AAA',resources)
    executor.execute(out/'AAA','audit',[sys.executable,str(source),'run','--sha256',sha256(out/'declaration.json')],60)
    print((out/'AAA/audit.log').read_text())


if __name__=='__main__':main()
