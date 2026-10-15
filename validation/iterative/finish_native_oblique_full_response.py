"""Run the six raw audits and final verifier with live own-child limits."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from calibrate_native_oblique_streaming import save
from run_native_oblique_streaming_calibration import digest
from run_native_oblique_full_audits import main as audit


def main(root, project, wait_for_replay=False, final_only=False):
    for path, sha in json.loads((root/'verification_runner_inputs.json').read_text()).items():
        assert digest(root/path) == sha
    if wait_for_replay:
        waiting = time.monotonic()
        while not (root/'replay/receipts/white_h20_n4.json').exists():
            if (root/'verification/abort_wait').exists():
                raise RuntimeError('continuation explicitly aborted; preserve all output')
            for file in (root/'replay/runs').glob('*_watchdog.json'):
                result = json.loads(file.read_text())
                if result['returncode'] or result['limit_failure']:
                    raise RuntimeError('replay failed; independent finish not started')
            if time.monotonic()-waiting > 7200:
                raise RuntimeError('replay wait exceeded two hours; no numerical audit started')
            time.sleep(1.)
        receipts = list((root/'replay/receipts').glob('*.json'))
        assert len(receipts) == 568
        assert all(json.loads(file.read_text())['all_byte_identical'] for file in receipts)
        save(root/'runs/final_wait.json', dict(waited_seconds=time.monotonic()-waiting,
             replay_receipts=568, audits_started_only_after_complete_replay=True))
    if not final_only: audit(root)
    env = os.environ.copy()
    env.update({k: '1' for k in ['PYTHONDONTWRITEBYTECODE', 'VECLIB_MAXIMUM_THREADS', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS']})
    command = [sys.executable, str(root/'build/verify_native_oblique_full_response.py'), str(root), str(project)]
    start = time.monotonic(); peak = 0.; failure = None
    with (root/'runs/final_verification.log').open('x') as log:
        child = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, env=env, cwd='/private/tmp')
        while child.poll() is None:
            p = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(child.pid)], capture_output=True, text=True)
            if p.returncode and child.poll() is None:
                child.terminate(); child.wait(timeout=10); raise RuntimeError('own-child RSS watchdog unavailable')
            if p.stdout.strip(): peak = max(peak, float(p.stdout.strip())/1024)
            if time.monotonic()-start > 600 or peak > 512:
                failure = 'time or RSS cap'; child.terminate(); child.wait(timeout=10); break
            time.sleep(.2)
    save(root/'runs/final_verification_watchdog.json', dict(command=command, returncode=child.returncode,
         elapsed_seconds=time.monotonic()-start, sampled_peak_rss_mib=peak, limit_failure=failure))
    if child.returncode or failure: raise RuntimeError('final verification failed; preserve all output')
    print('Six raw audits and final verification passed.', flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('artifact', type=Path); p.add_argument('project', type=Path)
    p.add_argument('--wait-for-replay', action='store_true')
    p.add_argument('--final-only', action='store_true', help='Reuse completed raw audits; the final verifier still checks every audit and watchdog.')
    a = p.parse_args(); main(a.artifact.resolve(), a.project.resolve(), a.wait_for_replay, a.final_only)
