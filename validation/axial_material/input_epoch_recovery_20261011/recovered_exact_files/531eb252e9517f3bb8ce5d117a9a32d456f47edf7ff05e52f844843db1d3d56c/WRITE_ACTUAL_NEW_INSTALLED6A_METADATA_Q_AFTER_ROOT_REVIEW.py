import sys
_PYTHON_PROCESS_ATTEMPTS=[]
def _forbid_process(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.exec','os.posix_spawn','os.spawn','os.startfile','os.startfile/2'):
        _PYTHON_PROCESS_ATTEMPTS.append(event);raise RuntimeError('new6a metadata Q forbids Python process creation')
sys.addaudithook(_forbid_process)
import hashlib
import json
import os
import stat
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

started = time.monotonic()
R = Path('/Users/wen/spot')
A = R / 'validation/artifacts'
V = R / 'validation/axial_material'
out = A / 'axial-material-installed6a-helper-metadata-admission-v29-20261011'
assert not out.exists() and not out.is_symlink()
assert sys.flags.optimize == 0 and sys.dont_write_bytecode
for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
             'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    assert os.environ.get(name) == '1'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    for p in (path, *path.parents):
        assert not p.is_symlink(), str(p)
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1
    h = hashlib.sha256()
    with path.open('rb') as stream:
        assert identity(os.fstat(stream.fileno())) == identity(before)
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            h.update(block)
        assert identity(os.fstat(stream.fileno())) == identity(before)
    assert identity(path.lstat()) == identity(before)
    return dict(path=str(path), size_bytes=before.st_size,
                sha256=h.hexdigest(), identity=identity(before))


timing_path = Path('/private/tmp/Root_current_original_account_phase_timing_m9t382tr/CURRENT_ACCOUNT_TIMING.json')
timing_pin = pin(timing_path)
assert timing_pin['sha256'] == '4f07c5d192d6417ca3f989f1fec2e57a135eb4abfa7d4a91106374f3e8005da8'
t = json.loads(timing_path.read_bytes())
gp = t['original_five_guard_pins']
for item in gp:
    assert pin(item['path']) == item
sys.path.insert(0, str(V))
import run_real64_common_rank2_training as training
for item in gp:
    assert any(getattr(m, '__file__', None) == item['path']
               for m in tuple(sys.modules.values()))
    assert pin(item['path']) == item
H = A / 'axial-material-grouped-native-AB-d19-v2-20261011-host'
O = A / 'axial-material-grouped-native-AB-d19-v2-20261011-output'
C = A / 'axial-material-grouped-native-AB-d19-v2-20261011-control'
AH=A/'axial-material-stable-wire-sort-complete-fresh-host-v28-20261011-dwah5ubd'
AO=A/'axial-material-stable-wire-sort-complete-fresh-v28-20261011-dwah5ubd'
AS=Path('/private/tmp/SPOT_stable_wire_v28_fullfresh_source_only_dwah5ubd/sources')
resources = training.TrainingResources(out, [H, O, C, AH, AO])


def frozen():
    for record in t['current_complete_D_E_freeze'].values():
        for item in record['files']:
            assert pin(item['path']) == item
        for path, saved in record['directories'].items():
            p = Path(path)
            assert not p.is_symlink() and p.is_dir()
            assert identity(p.lstat()) == saved
        root = Path(min(record['directories'], key=lambda p: len(Path(p).parts)))
        expected = {item['path'] for item in record['files']} | set(record['directories'])
        assert expected == {str(root), *(str(p) for p in root.rglob('*'))}
    assert pin(t['original_failed_provenance_pin']['path']) == t['original_failed_provenance_pin']


def joint():
    roots = [H, O, C, out, AH, AO, AS]
    roots += [Path(min(record['directories'], key=lambda p: len(Path(p).parts)))
              for record in t['current_complete_D_E_freeze'].values()]
    seen = set()
    total = 0
    for root in roots:
        if not root.exists():
            continue
        assert not root.is_symlink() and root.is_dir()
        for p in root.rglob('*'):
            s = p.lstat()
            assert not stat.S_ISLNK(s.st_mode)
            if stat.S_ISDIR(s.st_mode):
                continue
            assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1
            key = (s.st_dev, s.st_ino)
            if key not in seen:
                seen.add(key)
                total += s.st_size
    return total


def account(reserve):
    checks = resources.check()
    jb = joint()
    history = checks['complete_history']['artifact_bytes'] + t['current_external_DE_bytes']
    assert jb + reserve < 2 * 2**30
    assert history + reserve <= 96 * 2**30
    assert min(checks['complete_history']['disk_free_bytes'],
               checks['fresh_output']['disk_free_bytes']) - reserve >= 8 * 2**30
    assert time.monotonic() - started < 600
    frozen()
    return dict(joint_bytes=jb, history_including_external_DE_bytes=history,
                reserved_bytes=reserve, original_resource_checks=checks)


CONTRACT_PIN={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/installed6a_closed_metadata_admission_contract.py', 'size_bytes': 33913, 'sha256': 'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1', 'identity': [16777229, 49656560, 33188, 1, 33913, 1791702643852949734, 1791702643852949734]}
ORIGINAL_PREFIX_PIN={'path': '/private/tmp/Root_v28_fullfresh_original_resource_precheck_v2_20261011.py', 'size_bytes': 4771, 'sha256': 'ded9bda107c0c2ac3aad8111b17efe8fee2f27908d86468ecbf8ddd0518abf66', 'identity': [16777229, 49653193, 33188, 1, 4771, 1791700396971599237, 1791700396971599237]}
ORIGINAL_PREFIX_SHA='ca8e0d25e4a5526ba64c81ddfd866e77e966520e02d82a8a633fabcbe76138aa'

import importlib.util,resource,signal,threading
def _deadline(signum,frame):raise TimeoutError('original600s metadata Q cap')
signal.signal(signal.SIGALRM,_deadline);signal.setitimer(signal.ITIMER_REAL,600)
def checkpoint():
    rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    assert 0<=rss<512*2**20 and threading.active_count()==1 and not _PYTHON_PROCESS_ATTEMPTS and time.monotonic()-started<600
    return dict(seconds=time.monotonic()-started,own_peak_rss_bytes=rss,Python_process_attempts=list(_PYTHON_PROCESS_ATTEMPTS),Python_audit_scope='Named events after hook; native/C and pre-script children not observed')
assert len(sys.argv)==1 and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12').resolve()
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN
spec=importlib.util.spec_from_file_location('new_installed6a_metadata_Q_actual_contract',CONTRACT_PIN['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
evidence,fixed=module.validate_closed_evidence()
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN
selfpin=pin(__file__)
before=account(64*2**20);checkpoint()
out.mkdir(mode=0o700)
q=dict(schema='SPOT_INSTALLED6A_ACTUAL_ORIGINAL_PURE_AND_FULLFRESH_HELPER_METADATA_Q_V29',status='QUALIFIED_INSTALLED6A_ORIGINAL_PURE_FULL_CURRENT_GRAPH_METADATA_ONLY',scope='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE',complete_actual_new6a_closed_evidence=evidence,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,complete_Root_metadata_EOF7ID_inputs=fixed+[selfpin,CONTRACT_PIN],original_resource_prefix_Source=ORIGINAL_PREFIX_PIN,original_resource_prefix_full_inverse_sha256=ORIGINAL_PREFIX_SHA,resources_before=before,external_writer_checkpoint=checkpoint(),whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,canonical_wired=False,science_or_BOOT_admitted=False,legacy_Q_authorizes_new_helper=False)
for p in fixed:assert pin(p['path'])==p
assert pin(__file__)==selfpin
with (out/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json').open('x') as f:json.dump(q,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
qpin=pin(out/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json')
after=account(1024*1024);checkpoint()
assert sum(p.lstat().st_size for p in out.rglob('*') if p.is_file())<64*2**20
for p in fixed:assert pin(p['path'])==p
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN and pin(__file__)==selfpin
signal.setitimer(signal.ITIMER_REAL,0)
print(json.dumps(dict(status=q['status'],actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,new_Q_created=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)
