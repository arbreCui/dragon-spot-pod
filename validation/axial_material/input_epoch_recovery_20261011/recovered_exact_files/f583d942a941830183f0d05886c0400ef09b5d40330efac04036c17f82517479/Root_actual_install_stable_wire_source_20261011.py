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
out = A / 'axial-material-stable-wire-sort-source-install-20261011'
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



import resource, signal, threading
children=[]
def no_child(event,args):
    if event in ('subprocess.Popen','os.system','os.posix_spawn','os.fork','os.forkpty'):
        children.append(event)
        raise RuntimeError('metadata publication cannot launch child')
sys.addaudithook(no_child)
resource.setrlimit(resource.RLIMIT_CPU,(600,resource.getrlimit(resource.RLIMIT_CPU)[1]))
def own_budget(*args):
    assert time.monotonic()-started < 600
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 512*2**20
signal.signal(signal.SIGALRM,own_budget)
signal.setitimer(signal.ITIMER_REAL,.1,.1)


import ast
D=Path('/private/tmp/SPOT_private_builtin_wire_stable_sort_bn9q4own')
install=V/'combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py'
assert not install.exists() and not install.is_symlink()
manifest=pin(D/'FINAL_EVIDENCE_MANIFEST.json')
saved=json.loads((D/'FINAL_EVIDENCE_MANIFEST.json').read_bytes())
evidence=[];payload={}
for item in saved['files']:
    current=pin(item['path']);assert current==item;evidence.append(current)
    name=Path(item['path']).name
    if name not in ('ACTUAL_ORIGINAL_COMPLETE_WIRE_TABLE.json','ACTUAL_CANDIDATE_COMPLETE_WIRE_TABLE.json'):
        payload['pure_wire_controls/'+name]=Path(item['path']).read_bytes()
payload['pure_wire_controls/FINAL_EVIDENCE_MANIFEST.json']=(D/'FINAL_EVIDENCE_MANIFEST.json').read_bytes()
old_wire=(D/'ACTUAL_ORIGINAL_COMPLETE_WIRE_TABLE.json').read_bytes()
new_wire=(D/'ACTUAL_CANDIDATE_COMPLETE_WIRE_TABLE.json').read_bytes()
assert len(old_wire)==9793135 and old_wire==new_wire
assert hashlib.sha256(old_wire).hexdigest()=='96b3c54bf5c240e929f1abbfa21104bdd1cf1dd283c4f6f6517da9be76d42e82'
del old_wire,new_wire
proof=json.loads(payload['pure_wire_controls/SOURCE_ONLY_INVERSE_PROOF_V3.json'])
ancestor=pin(proof['original']['path']);assert ancestor==proof['original']
old_bytes=Path(ancestor['path']).read_bytes()
source=payload['pure_wire_controls/candidate_graph_helper_builtin_stable_wire_sort_v3.py']
assert len(source)==152950
assert hashlib.sha256(source).hexdigest()=='6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'
assert old_bytes.decode().count(proof['exact_before'])==1
assert source.decode().count(proof['exact_after'])==1
assert old_bytes.decode().replace(proof['exact_before'],proof['exact_after']).encode()==source
assert source.decode().replace(proof['exact_after'],proof['exact_before']).encode()==old_bytes
ast.parse(source)
controls=json.loads(payload['pure_wire_controls/ACTUAL_BOUNDED_COMPLETE_WIRE_SORT_CONTROL_RESULT.json'])
assert controls['status']=='PASS_FULL_REAL_EDGE_WIRE_BYTES_AND_TYPED_FIXTURES_ONLY_UNADMITTED'
assert len(controls['fixture_results'])==67
assert all(c['old_equals_candidate_complete_return_or_exception'] for c in controls['fixture_results'])
for k in ('source_candidate_admitted','Q_created','Native_solver_train_PS_started','project_or_ART_mutated','full_payload_phase_reexecuted','whole_522_to_512_RSS_proved'):
    assert controls[k] is False
closed=json.loads(payload['pure_wire_controls/ACTUAL_CLOSED_TOOL_RETURN.json'])
assert closed['exit_code']==0
asof=datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
report=f"""保存时间：{asof}

完整输入排序的第二项内存优化已完成真实纯数据对照：全部238,780条逻辑边的编码表与原表逐字节一致；67项正常、重复、类型、异常和自定义迭代控制全部一致。新程序仅在字段为原生字符串的私有记录上使用稳定排序，保留完整输入和原逐行检查。其函数分配测量峰值降低10,474,299字节；该量不是整段构建的RSS，也不能和此前7.09MiB简单相加后宣称512MiB达标。

本次另名安装152,950字节的新Source-only候选，保留前一候选和所有旧记录。没有生成准入Q、改生产factory或执行物理/Native求解。下一步是一次完整fresh输入核验与真实内存测量，随后仍需完整接入与整段构建验证。

证据边界补充：此前原完整fresh profile保存了完整27返回，但真实审计snapshot仅保存其canonical摘要和覆盖/计数见证；没有保留旧完整字节buffer。因此旧新snapshot证据可表述摘要、计数及实现/控制一致，不可声称旧buffer已逐字节比较。下一次将保存新的完整真实snapshot，原Source/result均不改。

科学目标和原阈值不变；AAA与ABA尚未准入。未清理文件。
"""
payload['REPORT.txt']=report.encode()
payload['ROOT_INSTALL_SOURCE.py']=Path(__file__).read_bytes()
payload['ROOT_SAVED_EVIDENCE_REVIEW.json']=(json.dumps(dict(
    schema='SPOT_STABLE_WIRE_SORT_SOURCE_ONLY_INSTALL_INPUTS_V1',
    evidence_original_pins=evidence,manifest_pin=manifest,ancestor_source=ancestor,
    full_actual_saved_wire_table_bytes_equal=True,complete_inverse_bytes_equal=True,
    original_five_guards=gp,new_qualification=False),ensure_ascii=False,indent=2)+'\n').encode()
total=sum(map(len,payload.values()));assert total<2*2**20
extra_source_bytes=ancestor['size_bytes']+len(source)
pre=account(total+extra_source_bytes+4*2**20)
out.mkdir()
for name,data in payload.items():
    p=out/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(data)
    assert p.read_bytes()==data
with install.open('xb') as f:f.write(source)
installed=pin(install)
assert install.read_bytes()==source
for item in evidence+[manifest,ancestor]+gp:assert pin(item['path'])==item
assert pin(timing_path)==timing_pin
post=account(extra_source_bytes+4*2**20)
own_budget();assert threading.active_count()==1 and not children
result=dict(schema='SPOT_STABLE_WIRE_SORT_SOURCE_ONLY_INSTALL_WITNESS_V1',
    classification='SOURCE_ONLY_COMBINED_INDEX_AND_SORT_HELPER_INSTALLED_NO_ADMISSION',
    asof=asof,installed_source=installed,report=pin(out/'REPORT.txt'),
    installer_source=pin(__file__),copied_files=len(payload),copied_bytes=total,
    actual_seconds=time.monotonic()-started,
    own_peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    resource_pre=pre,resource_post=post,all_old_input_and_source_pins_held=True,
    full_actual_saved_wire_bytes_equal=True,Source_inverse_byte_exact=True,
    Q_created=False,production_factory_changed=False,whole_RSS_512_proved=False,
    Native_or_science_started=False,cleanup_performed=False,
    child_launch_attempts=children,actual_python_thread_count=threading.active_count())
data=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();assert len(data)<2**20
with (out/'ACTUAL_SOURCE_INSTALL_WITNESS.json').open('xb') as f:f.write(data)
final=account(extra_source_bytes+2**20);own_budget()
signal.setitimer(signal.ITIMER_REAL,0,0)
Path('/private/tmp/Root_actual_stable_wire_source_install_witness_20261011.json').write_bytes(data)
print(json.dumps({k:result[k] for k in ('classification','installed_source','report','actual_seconds','own_peak_rss_bytes','Q_created','production_factory_changed','whole_RSS_512_proved','cleanup_performed')},ensure_ascii=False))
