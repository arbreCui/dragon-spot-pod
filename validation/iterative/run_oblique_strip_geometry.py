"""Serial, bounded execution of the archived strip experiment on macOS."""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import numpy as np
import scipy


def save(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2);f.write('\n')


def main(a):
    plan=json.loads((a/'plan.json').read_text());env=os.environ.copy()
    limits={key:'1' for key in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']};env.update(limits)
    commands=[([sys.executable,str(a/'build'/script)],name) for script,name in [
        ('test_oblique_strip_geometry.py','tests'),('test_axial_cell_characteristic.py','reference_tests')]]
    commands += [([sys.executable,str(a/'build/qualify_oblique_strip_geometry.py'),str(a),c['id']],c['id']) for c in plan['process_cases']]
    commands.append(([sys.executable,str(a/'build/qualify_oblique_strip_geometry.py'),str(a),'summary'],'summary'))
    save(a/'runs/command.json',dict(commands=commands,environment=limits,cwd='/private/tmp'))
    save(a/'runs/versions.json',dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()))
    for command,name in commands:
        start=time.monotonic();peak=0.;limit_failure=None
        with (a/'runs'/(name+'.log')).open('x') as log:
            process=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,cwd='/private/tmp')
            while process.poll() is None:
                ps=subprocess.run(['/bin/ps','-o','rss=','-p',str(process.pid)],capture_output=True,text=True)
                if ps.returncode==0 and ps.stdout.strip():peak=max(peak,float(ps.stdout.strip())/1024)
                if time.monotonic()-start>600 or peak>512:
                    limit_failure='wall time or RSS cap exceeded';process.terminate();process.wait(timeout=10);break
                time.sleep(.2)
        save(a/'runs'/(name+'_watchdog.json'),dict(returncode=process.returncode,elapsed_seconds=time.monotonic()-start,sampled_peak_rss_mib=peak,limit_failure=limit_failure))
        print(name,process.returncode,round(time.monotonic()-start,2),flush=True)
        if process.returncode or limit_failure:raise RuntimeError(f'{name}: process or resource failure; retained outputs must not be overwritten')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);args=p.parse_args();main(args.artifact.resolve())
