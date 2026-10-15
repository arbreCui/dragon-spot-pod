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
out = A / 'axial-material-stable-wire-sort-original-pure-controls-root-closure-v27-20261011-v3'
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
PH = A / 'axial-material-stable-wire-sort-original-pure-controls-host-v27-20261011-odcl3yl4'
PO = A / 'axial-material-stable-wire-sort-original-pure-controls-v27-20261011-odcl3yl4'
resources = training.TrainingResources(out, [H, O, C])


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
    roots = [H, O, C, out]
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



import resource,signal,threading
resource.setrlimit(resource.RLIMIT_CPU,(600,600))
def budget(*args):
    assert time.monotonic()-started<600
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss<512*2**20
    assert threading.active_count()==1
signal.signal(signal.SIGALRM,budget)
signal.setitimer(signal.ITIMER_REAL,.1,.1)
def no_child(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.posix_spawn'):
        raise RuntimeError('Root pure evidence closeout only')
sys.addaudithook(no_child)
base=Path('/private/tmp/SPOT_stable_wire_v27_pure_protocol_odcl3yl4')
tools=Path('/private/tmp/Root_v27_pure_protocol_actual_tool_returns_20261011.json')
tp=pin(tools);actual=json.loads(tools.read_bytes())
assert actual['initial']['chunk_id']=='68ece3' and actual['initial']['session_id']==62042
assert actual['closed']['chunk_id']=='3a9510' and actual['closed']['exit_code']==0
real=json.loads(actual['closed']['output'])
assert real['status']=='ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED'
for field in ('actual_host_result','actual_admission_stdout'):
    want=real[field];got=pin(want['path'])
    assert got['identity']==want['identity'] and got['sha256']==want['sha256']
hp=pin(PH/'result.json');h=json.loads((PH/'result.json').read_bytes())
assert hp['sha256']=='0aaed12e13c6109345ab859305d0fbef73a73b8a056343a02e1b0ffd07e974f6'
assert h['status']==real['status'] and h['new_Q_created'] is False
assert h['whole_family_memory_pass'] is False
assert h['whole_seconds']<60
assert h['threads']==1 and h['children_at_once']==1 and h['retries']==0
watch=h['watchdog'];assert watch['returncode']==0 and watch['limit_failure'] is None
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert watch['sampled_peak_rss_mib']==395.890625 and watch['sampled_peak_rss_mib']<512
for item in h['input_sources']+[h['original_helper'],h['resource_factory']]:
    now=pin(item['path']);assert now['identity']==item['identity'] and now['sha256']==item['sha256']
cp=pin(h['actual_control_report']['path']);c=json.loads(Path(cp['path']).read_bytes())
assert cp['sha256']==h['actual_control_report']['sha256']
assert c['status']=='ACTUAL_PURE_HELPER_CONTROLS_PASS_NO_RUNTIME_OR_SCIENCE_ADMISSION'
for key in ('business_component_executed','fresh_runtime_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted'):
    assert c[key] is False
def fixture_entry(p):
    if p.is_symlink():
        before=p.lstat();target=os.readlink(p)
        assert stat.S_ISLNK(before.st_mode) and p.lstat()==before
        return dict(path=str(p),entry_type='retained_original_protocol_fixture_symlink',
                    link_identity=identity(before),literal_target=target)
    return pin(p)
files=[fixture_entry(p) for root in (PH,PO,base/'sources') for p in sorted(root.rglob('*')) if p.is_file() or p.is_symlink()]
# Original archive budget counts regular files and the followed file aliases.
actual_archive_bytes=sum(p.stat().st_size for root in (PH,PO,base/'sources') for p in root.rglob('*') if p.is_file())
assert actual_archive_bytes<64*2**20
before=account(64*2**20)
out.mkdir()
copies=[]
for p in (tools,Path('/private/tmp/Root_v27_independent_source_review_20261011.json'),Path('/private/tmp/Root_review_v27_pure_source_20261011.py'),Path(__file__)):
    original=pin(p);target=out/p.name
    with p.open('rb') as src,target.open('xb') as dst:
        while block:=src.read(2**20):dst.write(block)
    target_pin=pin(target)
    assert original['size_bytes']==target_pin['size_bytes'] and original['sha256']==target_pin['sha256']
    copies.append(dict(original=original,copied=target_pin))
after=account(2**20)
value=dict(schema='SPOT_ROOT_ACTUAL_V27_PURE_PROTOCOL_EXTERNAL_CLOSED_BINDING_V1',
 status='ROOT_BOUND_ACTUAL_PURE_PROTOCOL_PASS_NO_Q_OR_SCIENTIFIC_ADMISSION',
 actual_host_result=hp,actual_control_report=cp,actual_genuine_tool_returns=tp,
 retained_protocol_complete_file_pins=files,actual_protocol_archive_bytes=actual_archive_bytes,
 joint_scope='Original d19 H/O/C+D/E plus Root publication; pure H/O use original 64MiB protocol archive guard and remain in complete96GiB history',
 copied_Root_evidence=copies,resources_before=before,resources_after=after,
 actual_child_peak_rss_mib=watch['sampled_peak_rss_mib'],actual_host_protocol_seconds=h['whole_seconds'],
 new_Q_created=False,whole_522_to_512_memory_pass=False,Native_started=False,
 AAA_accuracy_qualified=False,ABA_admitted=False)
with (out/'ROOT_EXTERNAL_CLOSED_BINDING.json').open('x') as f:
    json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
text='SPOT 内存优化版本的实际完整协议检查\n\n新6a版本已执行原完整协议，唯一一次实际工具关闭EXIT0。原生产/codec/子类型/owner/审计快照/短索引控制及已保存67项完整wire字段核验通过。原60秒、512MiB、64MiB产物、单线程、单工作子进程与零重试限制保持。实际协议17.03秒，原监控器记录工作子进程峰值395.890625MiB。完整协议归档及Source合计低于64MiB。\n\n当前结果证明本版本原协议控制实际通过，外部Root工具返回、Source与所有产物全文件指纹已绑定。先前全量输入独立检查仍是315.15625MiB。两者均不证明此前522.359375MiB整段流程已满足512MiB，也不构成新Q、生产接入、Native内存、AAA物理精度或ABA准入。原失败证据保留，材料/温度/rank/验收门未改，清理暂缓。\n'
with (out/'REPORT.txt').open('x') as f:f.write(text)
final=account(0);budget()
for item in files:assert fixture_entry(Path(item['path']))==item
assert pin(tools)==tp and pin(PH/'result.json')==hp and pin(cp['path'])==cp
result_pin=pin(out/'ROOT_EXTERNAL_CLOSED_BINDING.json')
print(json.dumps(dict(status=value['status'],root_closure=result_pin,report=pin(out/'REPORT.txt'),
 actual_protocol_archive_bytes=actual_archive_bytes,full_retained_files=len(files),
 final_account=final,elapsed_seconds=time.monotonic()-started,own_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))
