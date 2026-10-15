"""Serial resource/storage watchdog and complete streaming independent replay."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import numpy as np
import scipy


def save(path,data):
    with path.open('x') as f:json.dump(data,f,indent=2);f.write('\n')


def digest(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def main(a,primary=None):
    plan=json.loads((a/'plan.json').read_text());env=os.environ.copy()
    limits={k:'1' for k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']};env.update(limits)
    tests=['test_native_oblique_track_pilot.py','test_oblique_strip_geometry.py','test_axial_cell_characteristic.py']
    commands=[([sys.executable,str(a/'build'/test)],test.removesuffix('.py')) for test in tests]
    commands += [([sys.executable,str(a/'build/qualify_native_oblique_track_pilot.py'),str(a),c['id']],c['id']) for c in plan['process_cases']]
    commands.append(([sys.executable,str(a/'build/qualify_native_oblique_track_pilot.py'),str(a),'summary'],'summary'))
    save(a/'runs/command.json',dict(commands=commands,environment=limits,cwd='/private/tmp',primary_compare=str(primary) if primary else None))
    save(a/'runs/versions.json',dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()))
    if primary:(a/'receipts').mkdir()
    for command,name in commands:
        reserve=plan['storage']['free_space_reserve_bytes'];casebound=plan['storage']['maximum_replay_case_bound_bytes']
        if shutil.disk_usage(a).free<reserve+casebound:raise RuntimeError('free-space reserve reached before next process; keep completed files')
        start=time.monotonic();peak=0.;failure=None
        with (a/'runs'/(name+'.log')).open('x') as log:
            child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,env=env,cwd='/private/tmp')
            while child.poll() is None:
                p=subprocess.run(['/bin/ps','-o','rss=','-p',str(child.pid)],capture_output=True,text=True)
                if p.returncode==0 and p.stdout.strip():peak=max(peak,float(p.stdout.strip())/1024)
                if time.monotonic()-start>600 or peak>512:
                    failure='wall time or memory cap exceeded';child.terminate();child.wait(timeout=10);break
                time.sleep(.2)
        save(a/'runs'/(name+'_watchdog.json'),dict(returncode=child.returncode,elapsed_seconds=time.monotonic()-start,
            sampled_peak_rss_mib=peak,limit_failure=failure,free_bytes_after=shutil.disk_usage(a).free))
        print(name,child.returncode,round(time.monotonic()-start,2),flush=True)
        if child.returncode or failure:raise RuntimeError(name+': bounded process failed; existing outputs preserved')
        if primary and name.startswith('t') and not name.startswith('test_'):
            folder=a/'analysis'/name;ref=primary/'analysis'/name
            files=sorted(p.name for p in folder.iterdir() if p.is_file())
            assert files==sorted(p.name for p in ref.iterdir() if p.is_file())
            receipt={}
            for file in files:
                p=folder/file;h=digest(p);assert h==digest(ref/file),(name,file)
                receipt[file]=dict(sha256=h,bytes=p.stat().st_size)
            save(a/'receipts'/(name+'.json'),dict(files=receipt,all_files_byte_identical=True,
                duplicate_npz_disposal='Only these fresh replay NPZ files are discarded after complete comparison; primary files and replay result JSON remain.'))
            for file in files:
                if file.endswith('.npz'):(folder/file).unlink()
        if primary and name=='summary':assert digest(a/'analysis/result.json')==digest(primary/'analysis/result.json')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--compare-primary',type=Path)
    args=p.parse_args();main(args.artifact.resolve(),args.compare_primary.resolve() if args.compare_primary else None)
