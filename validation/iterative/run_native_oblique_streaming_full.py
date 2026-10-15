"""Serial full-matrix runner; recovery precedes all common-white solves."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from calibrate_native_oblique_streaming import save
from run_native_oblique_streaming_calibration import digest


def main(root,primary=None):
    plan=json.loads((root/'plan.json').read_text());assert plan['execution_admitted']
    env=os.environ.copy();settings={k:'1' for k in ['PYTHONDONTWRITEBYTECODE','VECLIB_MAXIMUM_THREADS','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']};env.update(settings)
    commands=[('test_kernel',[sys.executable,str(root/'build/test_native_oblique_streaming.py'),str(root)]),
              ('test_action',[sys.executable,str(root/'build/test_native_oblique_full_action.py'),str(root)])]
    commands += [(f'reference_p{p}',[sys.executable,str(root/'build/qualify_native_oblique_streaming_full.py'),str(root),f'reference_p{p}']) for p in range(4)]
    commands += [(c['id'],[sys.executable,str(root/'build/qualify_native_oblique_streaming_full.py'),str(root),c['id']]) for c in plan['processes']]
    for phase in ['recover','white']:
        for H in [1.,20.]:
            for nz in [1,2,4]:commands.append((f'{phase}_h{int(H)}_n{nz}',[sys.executable,str(root/'build/recover_native_oblique_full_response.py'),str(root),phase,str(H),str(nz)]))
    save(root/'runs/commands.json',dict(commands=commands,environment=settings,cwd='/private/tmp',compare_primary=str(primary) if primary else None))
    for name,command in commands:
        if shutil.disk_usage(root).free<plan['reserve_bytes']+plan['maximum_process_output_bound_bytes']:raise RuntimeError('free-space reserve reached')
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
        save(root/'runs'/(name+'_watchdog.json'),dict(returncode=child.returncode,elapsed_seconds=time.monotonic()-start,sampled_peak_rss_mib=peak,limit_failure=failure,free_bytes_after=shutil.disk_usage(root).free))
        print(name,child.returncode,round(time.monotonic()-start,2),flush=True)
        if child.returncode or failure:raise RuntimeError('full matrix stopped; preserve completed and failed outputs')
        if primary and not name.startswith('test_'):
            if name.startswith('reference_'):paths=[Path('reference')/(name.removeprefix('reference_')+suffix) for suffix in ['.npz','.json']]
            else:
                if name.startswith('recover_'):folder=Path('recovery')/name.removeprefix('recover_')
                elif name.startswith('white_'):folder=Path('white')/name.removeprefix('white_')
                else:folder=Path('analysis')/name
                paths=sorted(p.relative_to(root) for p in (root/folder).rglob('*') if p.is_file())
                assert paths==sorted(p.relative_to(primary) for p in (primary/folder).rglob('*') if p.is_file())
            receipt={}
            for path in paths:
                h=digest(root/path);assert h==digest(primary/path),(name,str(path))
                receipt[str(path)]=dict(sha256=h,bytes=(root/path).stat().st_size)
            save(root/'receipts'/(name+'.json'),dict(files=receipt,all_byte_identical=True))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('artifact',type=Path);p.add_argument('--compare-primary',type=Path);a=p.parse_args();main(a.artifact.resolve(),a.compare_primary.resolve() if a.compare_primary else None)
