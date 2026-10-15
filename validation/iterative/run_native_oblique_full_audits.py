"""Serial live watchdog for all six independent full-response audits."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
from calibrate_native_oblique_streaming import save


def main(root):
    env=os.environ.copy();env.update({k:'1' for k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']})
    for H in [1.,20.]:
        for nz in [1,2,4]:
            name=f'audit_h{int(H)}_n{nz}';command=[sys.executable,str(root/'build/audit_native_oblique_full_response.py'),str(root),str(H),str(nz)]
            start=time.monotonic();peak=0.;failure=None
            with (root/'runs'/(name+'.log')).open('x') as log:
                child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,cwd='/private/tmp')
                while child.poll() is None:
                    p=subprocess.run(['/bin/ps','-o','rss=','-p',str(child.pid)],capture_output=True,text=True)
                    if p.returncode and child.poll() is None:
                        child.terminate();child.wait(timeout=10);raise RuntimeError('own-child RSS watchdog unavailable')
                    if p.stdout.strip():peak=max(peak,float(p.stdout.strip())/1024)
                    if time.monotonic()-start>600 or peak>512:
                        failure='time or RSS cap';child.terminate();child.wait(timeout=10);break
                    time.sleep(.2)
            save(root/'runs'/(name+'_watchdog.json'),dict(command=command,returncode=child.returncode,elapsed_seconds=time.monotonic()-start,sampled_peak_rss_mib=peak,limit_failure=failure))
            print(name,child.returncode,round(time.monotonic()-start,2),flush=True)
            if child.returncode or failure:raise RuntimeError('independent audit failed; preserve all output')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);a=p.parse_args();main(a.artifact.resolve())
