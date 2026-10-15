"""Run declared layered-calibration jobs serially with an own-child watchdog."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


def save(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False); f.write('\n')


def main(root, jobfile):
    jobs=json.loads(jobfile.read_text())
    env=os.environ.copy()
    env.update({k:'1' for k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']})
    for job in jobs:
        name=job['name']; script=(root/'build'/job['script']).resolve()
        assert script.parent==root/'build' and script.suffix=='.py'
        if shutil.disk_usage(root).free < 1024**3+job.get('output_bound_bytes',256*1024**2):
            raise RuntimeError('storage reserve reached')
        command=[sys.executable,str(script),str(root),*job.get('args',[])]
        start=time.monotonic();peak=0.;failure=None
        with (root/'runs'/f'{name}.log').open('x') as log:
            child=subprocess.Popen(command,cwd='/private/tmp',env=env,stdout=log,stderr=subprocess.STDOUT)
            while child.poll() is None:
                sample=subprocess.run(['/bin/ps','-o','rss=','-p',str(child.pid)],capture_output=True,text=True)
                if sample.returncode and child.poll() is None:failure='own-child RSS unavailable'
                if sample.stdout.strip():peak=max(peak,float(sample.stdout.strip())/1024)
                if time.monotonic()-start>600 or peak>512:failure='resource cap'
                if failure:
                    child.terminate()
                    try:child.wait(timeout=10)
                    except subprocess.TimeoutExpired:child.kill();child.wait()
                    break
                time.sleep(.2)
        save(root/'runs'/f'{name}_watchdog.json',dict(command=command,returncode=child.returncode,
            elapsed_seconds=time.monotonic()-start,sampled_peak_rss_mib=peak,limit_failure=failure))
        print(name,child.returncode,round(time.monotonic()-start,2),flush=True)
        if child.returncode or failure:raise RuntimeError('job failed; outputs preserved')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('jobs',type=Path)
    a=p.parse_args();main(a.root.resolve(),a.jobs.resolve())
