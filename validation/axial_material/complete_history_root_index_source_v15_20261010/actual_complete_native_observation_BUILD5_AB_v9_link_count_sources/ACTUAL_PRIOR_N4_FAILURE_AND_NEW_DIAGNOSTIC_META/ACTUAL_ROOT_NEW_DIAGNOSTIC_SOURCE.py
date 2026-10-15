import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--output', required=True)
a = ap.parse_args()
out = Path(a.output)
assert out.is_absolute() and out.parent.is_dir() and not os.path.lexists(out)
assert not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile() is None

def pin(path):
    path = Path(path)
    s = path.lstat()
    before = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    assert path.resolve() == path and stat.S_ISREG(s.st_mode)
    with path.open('rb') as f:
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
    s = path.lstat()
    assert before == [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    return dict(path=str(path), sha256=digest, size_bytes=before[4], identity=before)

ps = '/bin/ps'
lsof = '/usr/sbin/lsof'
before = {path: pin(path) for path in (ps, lsof, str(Path(__file__).resolve()))}
ps_argv = [ps, '-axo', 'pid=,ppid=']
with subprocess.Popen(ps_argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
    ps_pid = process.pid
    try:
        ps_stdout, ps_stderr = process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        raise
    except BaseException:
        process.kill()
        raise
    ps_returncode = process.poll()
    if ps_returncode:
        raise subprocess.CalledProcessError(ps_returncode, ps_argv, output=ps_stdout, stderr=ps_stderr)
assert type(ps_pid) is int and type(ps_returncode) is int and ps_returncode == 0
parents = {int(pid): int(parent) for pid, parent in (line.split() for line in ps_stdout.splitlines())}
selected = {os.getpid()}
while True:
    expanded = selected | {pid for pid, parent in parents.items() if parent in selected}
    if expanded == selected:
        break
    selected = expanded
assert ps_pid in selected and parents[ps_pid] == os.getpid()
without_closed_ps = selected - {ps_pid}
assert os.getpid() in without_closed_ps and selected - without_closed_ps == {ps_pid}

def observe(pids):
    argv = [lsof, '-nP', '-F', 'pfnsiDt', '-a', '-p', ','.join(map(str, sorted(pids)))]
    result = subprocess.run(argv, capture_output=True, text=True, timeout=2)
    assert len(result.stdout.encode()) < 8 * 2**20 and len(result.stderr.encode()) < 8 * 2**20
    return dict(argv=argv, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)

original = observe(selected)
fixed_selection = observe(without_closed_ps)
assert {path: pin(path) for path in before} == before
assert type(fixed_selection['returncode']) is int and fixed_selection['returncode'] == 0
value = dict(
    schema='ROOT_ACTUAL_CLOSED_PS_PID_ONLY_LSOF_COMPARISON_DIAGNOSTIC_V1',
    status='ACTUAL_READONLY_DIAGNOSTIC_ONLY_NO_NATIVE_OBSERVATION_OR_SCIENCE',
    actual_diagnostic_PID=os.getpid(),
    tools_and_diagnostic_Source_before_and_after=before,
    captured_ps_pid=ps_pid,
    captured_PS_closed_EXIT0=True,
    ps=dict(argv=ps_argv, returncode=ps_returncode, stdout=ps_stdout, stderr=ps_stderr),
    original_selected_pids=sorted(selected),
    selected_pids_excluding_only_actual_closed_PS_diagnostic=sorted(without_closed_ps),
    all_other_selected_pids_preserved=True,
    original_selection_lsof=original,
    closed_PS_only_excluded_lsof=fixed_selection,
    same_original_lsof_flags_timeout_and_output_limit=True,
    original_failed_native_host_reexecuted=False,
    compiler_material_candidate_guard_or_business_executed=False,
    original_N4_failure_lsof_raw_returncode_not_recovered=True,
    scientific_qualification_created=False,
)
with out.open('x') as f:
    json.dump(value, f, indent=2, allow_nan=False)
    f.write('\n')
print(json.dumps(dict(
    status=value['status'], diagnostic=pin(out), captured_ps_pid=ps_pid,
    captured_PS_closed_EXIT0=True, original_selected_pids=sorted(selected),
    retained_pids=sorted(without_closed_ps), original_lsof_returncode=original['returncode'],
    closed_PS_only_excluded_lsof_returncode=fixed_selection['returncode'],
    original_stdout_bytes=len(original['stdout'].encode()),
    fixed_selection_stdout_bytes=len(fixed_selection['stdout'].encode()),
    scientific_qualification_created=False,
), allow_nan=False), flush=True)
