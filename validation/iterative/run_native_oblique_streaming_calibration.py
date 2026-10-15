"""Only calibration commands; live limits apply to this runner's own children."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from calibrate_native_oblique_streaming import save


def digest(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(root,primary=None):
    plan=json.loads((root/'calibration_plan.json').read_text());env=os.environ.copy()
    settings={k:'1' for k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']};env.update(settings)
    commands=[('tests',[sys.executable,str(root/'build/test_native_oblique_streaming.py'),str(root)])]
    commands += [(c['id'],[sys.executable,str(root/'build/calibrate_native_oblique_streaming.py'),str(root),c['id']]) for c in plan['cases']]
    save(root/'runs/commands.json',dict(commands=commands,environment=settings,cwd='/private/tmp'))
    for name,command in commands:
        if shutil.disk_usage(root).free<1024**3+plan['maximum_process_output_bound_bytes']:raise RuntimeError('storage reserve reached')
        start=time.monotonic();peak=0.;failure=None
        with (root/'runs'/(name+'.log')).open('x') as log:
            child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,cwd='/private/tmp')
            while child.poll() is None:
                p=subprocess.run(['/bin/ps','-o','rss=','-p',str(child.pid)],capture_output=True,text=True)
                if p.returncode and child.poll() is None:
                    child.terminate();child.wait(timeout=10);raise RuntimeError('own-child RSS watchdog unavailable')
                if p.stdout.strip():peak=max(peak,float(p.stdout.strip())/1024)
                if time.monotonic()-start>600 or peak>512:
                    failure='time or RSS limit';child.terminate();child.wait(timeout=10);break
                time.sleep(.2)
        save(root/'runs'/(name+'_watchdog.json'),dict(returncode=child.returncode,elapsed_seconds=time.monotonic()-start,sampled_peak_rss_mib=peak,limit_failure=failure))
        print(name,child.returncode,round(time.monotonic()-start,2),flush=True)
        if child.returncode or failure:raise RuntimeError('bounded calibration failed; retain completed outputs')
        if primary and name!='tests':
            folder=root/'calibration'/name;ref=primary/'calibration'/name;names=sorted(p.name for p in folder.iterdir())
            assert names==sorted(p.name for p in ref.iterdir())
            receipt={n:dict(sha256=digest(folder/n),bytes=(folder/n).stat().st_size) for n in names}
            for n in names:assert receipt[n]['sha256']==digest(ref/n),(name,n)
            save(root/'receipts'/(name+'.json'),dict(files=receipt,all_byte_identical=True))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--compare-primary',type=Path)
    a=p.parse_args();main(a.artifact.resolve(),a.compare_primary.resolve() if a.compare_primary else None)
