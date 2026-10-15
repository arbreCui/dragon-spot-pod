import sys
_PYTHON_PROCESS_ATTEMPTS=[]
def _forbid(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.exec','os.posix_spawn','os.spawn','os.startfile','os.startfile/2'):
        _PYTHON_PROCESS_ATTEMPTS.append(event);raise RuntimeError('pure metadata Root Q closure forbids Python process launches')
sys.addaudithook(_forbid)
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
out = A / 'axial-material-installed6a-Q-Root-closed-binding-v29-20261011'
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


EXPECTED_Q_WRITER={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py', 'size_bytes': 24385, 'sha256': '9095bf8902be3105b82f5097dfc867d2ca0efe2aa94a187297841235d49fdfa3', 'identity': [16777229, 49660046, 33188, 1, 24385, 1791704692801967693, 1791704692801967693]}
EXPECTED_CONTRACT={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/installed6a_closed_metadata_admission_contract.py', 'size_bytes': 33913, 'sha256': 'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1', 'identity': [16777229, 49656560, 33188, 1, 33913, 1791702643852949734, 1791702643852949734]}
EXPECTED_PEER_SOURCE={'path': '/private/tmp/SPOT_NEW6A_Q_INDEPENDENT_REVIEW_COMPLETE_FRESH_SOURCE_ONLY_t2n40h2x/REVIEW_ACTUAL_NEW6A_METADATA_Q_AFTER_REAL_WRITER_CLOSED0.py', 'size_bytes': 30266, 'sha256': '442d2c3b2b142bb7ea2245d8716a688070631319832280e3e6cabd5d67a2d938', 'identity': [16777229, 49661280, 33188, 1, 30266, 1791705164928328950, 1791705164928328950]}
EXPECTED_Q_MANIFEST={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json', 'size_bytes': 103587, 'sha256': 'd62b0cabc7be06eb47c29a826b7f500a3cb5e9ec6090773b61b672df6d8aae02', 'identity': [16777229, 49660049, 33188, 1, 103587, 1791704692926812011, 1791704692926812011]}
EXPECTED_PEER_MANIFEST={'path': '/private/tmp/SPOT_NEW6A_Q_INDEPENDENT_REVIEW_COMPLETE_FRESH_SOURCE_ONLY_t2n40h2x/FINAL_SOURCE_ONLY_MANIFEST.json', 'size_bytes': 13102, 'sha256': 'c214aeb4f6d31df4b5a3a7da441aab0323f8c23748f4c85b5d9ca1beb253015c', 'identity': [16777229, 49661281, 33188, 1, 13102, 1791705164929526412, 1791705164929526412]}
PREPARER_SOURCE={'path': '/private/tmp/prepare_new6a_Q_actual_Root_closure_Source_only_20261011.py', 'size_bytes': 19763, 'sha256': '5f21b379ea2dff098e26a9e5dae8d9323122604c29458b78dbdf86383ce3aea8', 'identity': [16777229, 49662147, 33188, 1, 19763, 1791705487433802669, 1791705487433802669]}
ORIGINAL_RESOURCE_PREFIX={'path': '/private/tmp/Root_v28_fullfresh_original_resource_precheck_v2_20261011.py', 'size_bytes': 4771, 'sha256': 'ded9bda107c0c2ac3aad8111b17efe8fee2f27908d86468ecbf8ddd0518abf66', 'identity': [16777229, 49653193, 33188, 1, 4771, 1791700396971599237, 1791700396971599237]}
WRITER_TOOLS='/private/tmp/Root_corrected_new6a_Q_v3_actual_tool_returns_20261011.json'
PEER_TOOLS='/private/tmp/Root_new6a_Q_independent_saved_review_actual_tool_returns_20261011.json'
QROOT=Path('/Users/wen/spot/validation/artifacts/axial-material-installed6a-helper-metadata-admission-v29-20261011')
PEEROUT=Path('/Users/wen/spot/validation/artifacts/axial-material-installed6a-Q-independent-saved-review-v29-20261011')
WRITER_COMMAND='env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B /private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py'
PEER_COMMAND='env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B /private/tmp/SPOT_NEW6A_Q_INDEPENDENT_REVIEW_COMPLETE_FRESH_SOURCE_ONLY_t2n40h2x/REVIEW_ACTUAL_NEW6A_METADATA_Q_AFTER_REAL_WRITER_CLOSED0.py'

import importlib.util,resource,signal,threading,math,struct,re,ast
CHECKS=[];INPUTS={};COPY_ROWS={}
def ck(v,m):
    if type(v) is not bool or not v:raise ValueError('actual Root new6a closure: '+m)
    CHECKS.append(dict(name=m,passed=True))
def verify(row):
    ck(type(row['identity']) is list and len(row['identity'])==7 and all(type(v) is int for v in row['identity']),'typed exact full7ID')
    got=pin(row['path']);ck(got=={k:row[k] for k in got},'whole EOF7ID '+row['path'])
    if got['path'] in INPUTS:ck(INPUTS[got['path']]==got,'repeat pin same')
    INPUTS[got['path']]=got;return got
def pairs(rows):
    d={}
    for k,v in rows:
        if k in d:raise ValueError('duplicate JSON key')
        d[k]=v
    return d
def nonfinite(v):raise ValueError('nonfinite actual metadata '+v)
def read(p,expected=None):
    before=pin(p)
    if expected is not None:verify(expected);ck(before==expected,'exact bound JSON pin')
    with Path(p).open('rt',encoding='utf8') as f:v=json.load(f,object_pairs_hook=pairs,parse_constant=nonfinite)
    ck(pin(p)==before,'full JSON input unchanged');INPUTS[before['path']]=before;return v
def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return list(a)==list(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    if type(a) is float:return math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
    return a==b
def closed0(tool):
    ck(type(tool['closed']['exit_code']) is int and tool['closed']['exit_code']==0 and 'session_id' not in tool['closed'],'genuine closed integer zero')
    ck(type(tool['closed']['chunk_id']) is str and re.fullmatch('[0-9a-f]{6}',tool['closed']['chunk_id']) is not None,'closed genuine tool chunk')
    if tool.get('terminal_in_initial_call') is True:ck(exact(tool['initial'],tool['closed']),'actual terminal-in-initial full object')
    else:ck(type(tool['initial']['session_id']) is int and 'exit_code' not in tool['initial'],'actual yielded initial retained')
    ck(not tool.get('closed_output_truncated_by_tool',False),'small actual stdout untruncated')
    return json.loads(tool['closed']['output'],object_pairs_hook=pairs,parse_constant=nonfinite)
def checkpoint():
    rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    ck(0<=rss<512*2**20 and threading.active_count()==1 and not _PYTHON_PROCESS_ATTEMPTS and time.monotonic()-started<600,'original600/512/thread1/no Python launches')
    return dict(seconds=time.monotonic()-started,own_peak_rss_bytes=rss,Python_process_attempts=list(_PYTHON_PROCESS_ATTEMPTS),Python_audit_scope='Named events after hook; native/C and pre-script children not observed')
def deadline(signum,frame):raise TimeoutError('original600s Root metadata closure cap')
signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,600)
ck(len(sys.argv)==1 and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12').resolve(),'canonical interpreter and no arguments')
for row in (EXPECTED_Q_WRITER,EXPECTED_CONTRACT,EXPECTED_PEER_SOURCE,EXPECTED_Q_MANIFEST,EXPECTED_PEER_MANIFEST):verify(row)
qm=read(EXPECTED_Q_MANIFEST['path'],EXPECTED_Q_MANIFEST);pm=read(EXPECTED_PEER_MANIFEST['path'],EXPECTED_PEER_MANIFEST)
wt=read(WRITER_TOOLS);pt=read(PEER_TOOLS);ws=closed0(wt);ps=closed0(pt)
ck(wt['initial']['chunk_id']=='c81bec' and wt['initial']['session_id']==24272 and wt['closed']['chunk_id']=='11666a','unique real writer launch and terminal')
ck(wt['actual_command']==WRITER_COMMAND and pt['actual_command']==PEER_COMMAND,'both actual canonical commands')
ck(ws['actual_Source_writer']==EXPECTED_Q_WRITER and ws['metadata_contract_Source']==EXPECTED_CONTRACT and ws['new_Q_created'] is True,'actual writer Source and contract coupling')
QPIN=ws['actual_metadata_Q'];QWIT=ws['actual_complete_resource_witness'];RPIN=ps['review_pin'];RWIT=ps['actual_peer_resource_witness']
for row in (QPIN,QWIT,RPIN,RWIT):verify(row)
ck(QPIN['path']==str(QROOT/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json') and QWIT['path']==str(QROOT/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json'),'actual Q endpoints')
ck(RPIN['path']==str(PEEROUT/'REVIEW.json') and RWIT['path']==str(PEEROUT/'ACTUAL_RESOURCE_WITNESS.json'),'actual peer endpoints')
ck(ps['status']=='PASS_ACTUAL_NEW6A_Q_METADATA_ONLY' and ps['actual_metadata_Q']==QPIN and ps['actual_independent_review_Source']==EXPECTED_PEER_SOURCE and ps['metadata_contract_Source']==EXPECTED_CONTRACT,'actual peer stdout bound to Q/source/contract')
q=read(QPIN['path'],QPIN);qw=read(QWIT['path'],QWIT);peer=read(RPIN['path'],RPIN);pw=read(RWIT['path'],RWIT)
ck(peer['status']=='PASS_ACTUAL_NEW6A_Q_METADATA_ONLY' and peer['actual_metadata_Q']==QPIN and peer['actual_Source_writer']==EXPECTED_Q_WRITER and peer['actual_independent_review_Source']==EXPECTED_PEER_SOURCE and peer['metadata_contract_Source']==EXPECTED_CONTRACT,'full actual peer review exact binding')
ck(type(peer['check_count']) is int and peer['check_count']>0 and peer['check_count']==len(peer['checks']) and peer['all_checks_typed_true'] is True and peer['blockers']==[] and all(type(r['passed']) is bool and r['passed'] is True for r in peer['checks']),'all actual peer checks typed and final count exact')
ck(ps['check_count']==peer['check_count'] and ps['all_checks_typed_true'] is True,'actual peer smallstdout complete counts')
for obj in (q,peer):
    for key in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','science_or_BOOT_admitted'):ck(obj[key] is False,'no physics/whole gate '+key)
for obj in (ws,ps,qw,pw):
    for key in ('whole_build_qualified','whole_INPUT_admitted','science_or_BOOT_admitted'):ck(obj[key] is False,'actual witnesses/stdout no '+key)
ck(qw['actual_metadata_Q']==QPIN and qw['actual_Source_writer']==EXPECTED_Q_WRITER and qw['metadata_contract_Source']==EXPECTED_CONTRACT,'writer resource witness Q and source binds')
ck(pw['schema']=='SPOT_ACTUAL_NEW6A_Q_INDEPENDENT_SAVED_REVIEW_RESOURCE_WITNESS_V1' and pw['actual_metadata_Q']==QPIN and pw['actual_saved_review']==RPIN and pw['actual_independent_review_Source']==EXPECTED_PEER_SOURCE,'actual peer resource witness binds review/Q/source')
spec=importlib.util.spec_from_file_location('Root_closed_new6a_pure_metadata_contract',EXPECTED_CONTRACT['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
module.validate_actual_new_Q(q)
ck(len(q['complete_Root_metadata_EOF7ID_inputs'])==235 and q['complete_Root_metadata_EOF7ID_inputs']==peer['complete_actual_Q_declared_EOF7ID_input_pins'],'all235 exact actual Q inputs fully reviewed, no original178 subset')
for row in q['complete_Root_metadata_EOF7ID_inputs']+peer['all_this_review_EOF7ID_input_pins']:verify(row)
for obj in (q,qw,peer,pw):module.full_refs(obj)
for row in tuple(module.INPUTS.values()):verify(row)
ck(peer['actual_genuine_writer_tool_returns']==pin(WRITER_TOOLS),'peer genuine writer-tool document full pin')
ck(peer['actual_resource_witness']==QWIT,'peer actual writer resource witness full pin')
# Only Source/metadata results are copied; large historical graph/trace inputs remain fully pinned.
def add_copy(row):
    verify(row)
    if row['path'] in COPY_ROWS:ck(COPY_ROWS[row['path']]==row,'copied original literal unique identity')
    COPY_ROWS[row['path']]=row
for row in [QPIN,QWIT,RPIN,RWIT,pin(WRITER_TOOLS),pin(PEER_TOOLS),EXPECTED_Q_WRITER,EXPECTED_CONTRACT,EXPECTED_PEER_SOURCE,EXPECTED_Q_MANIFEST,EXPECTED_PEER_MANIFEST,pin(__file__),PREPARER_SOURCE,ORIGINAL_RESOURCE_PREFIX]:add_copy(row)
for res in (qw['resources_before'],qw['resources_after_Q_before_witness']):
    for ns in res['complete_original_and_new_Source_namespaces']:
        for row in ns['files']:add_copy(row)
    for row in res['current_stage_fresh_explicit_file_pins']:add_copy(row)
for res in (peer['resources_before'],pw['resources_after_review_before_resource_witness']):
    ck(res['original_joint2_history96_free8_and_wholephysics_limits_unchanged'] is True,'actual peer original caps retained')
    for ns in res['complete_peer_Source_namespaces']:
        for row in ns['files']:add_copy(row)
    for row in res['explicit_current_peer_fresh_input_pins']:add_copy(row)
for name in ('old_immutable_Q','old_immutable_factory','old_Q_writer_Source'):add_copy(module.FIXED_ENDPOINTS[name])
for row in t['original_five_guard_pins']:add_copy(row)
for freeze in t['current_complete_D_E_freeze'].values():
    for row in freeze['files']:add_copy(row)
ck(sum(row['size_bytes'] for row in COPY_ROWS.values())<32*2**20,'complete selected Source/results preserve32MiB reserve, no historical payload duplication')
# Closed original helpers/controls still have no Native/transport qualification.
whole_roots=[row['path'] for row in qw['resources_after_Q_before_witness']['complete_joint_roots_inode_once']]+[str(PEEROUT),str(Path(__file__).parent),str(out)]+[row['path'] for row in pw['resources_before']['explicit_current_peer_fresh_input_pins']]+[row['root'] for row in pw['resources_before']['complete_peer_Source_namespaces']]+[PEER_TOOLS,WRITER_TOOLS,PREPARER_SOURCE['path']]
_SOURCE_FREEZE=None
def fulljoint():
    seen=set();total=0;records=[]
    for literal in whole_roots:
        p=Path(literal)
        if not p.exists():ck(not p.is_symlink(),'future closure no alias');continue
        s=p.lstat();ck(not stat.S_ISLNK(s.st_mode),'whole closure root/file no alias')
        members=sorted(p.rglob('*'),key=str) if stat.S_ISDIR(s.st_mode) else [p]
        for m in members:
            ms=m.lstat();ck(not stat.S_ISLNK(ms.st_mode),'closure joint member no alias')
            if stat.S_ISDIR(ms.st_mode):continue
            ck(stat.S_ISREG(ms.st_mode) and ms.st_nlink==1,'whole joint ordinary regular singlelink')
            key=(ms.st_dev,ms.st_ino)
            if key not in seen:seen.add(key);total+=ms.st_size;records.append(dict(path=str(m),size_bytes=ms.st_size,identity=identity(ms)))
    return total,records
def complete_account(reserve):
    original=account(reserve);total,rows=fulljoint();ck(total+reserve<2*2**30,'complete whole closure new/current stages joint2 reserved')
    frees={str(Path(p).parent):int(os.statvfs(Path(p).parent).f_bavail)*int(os.statvfs(Path(p).parent).f_frsize) for p in whole_roots}
    ck(min(frees.values())-reserve>=8*2**30,'all actual closure TMP inputs free8 reserved');checkpoint()
    for row in tuple(INPUTS.values()):verify(row)
    return dict(original_resource_return=original,complete_closure_joint_bytes=total,joint_full_regular_files=rows,reserved_bytes=reserve,all_actual_fresh_files_tmp_free_bytes=frees,original_caps_and_fiveguards_DE_unchanged=True)
before=complete_account(32*2**20)
for row in tuple(INPUTS.values()):verify(row)
checkpoint();out.mkdir(mode=0o700);saved=[]
for i,row in enumerate(COPY_ROWS.values()):
    target=out/'retained'/('input_'+str(i).zfill(4))/Path(row['path']).name;target.parent.mkdir(parents=True,exist_ok=True);verify(row)
    with Path(row['path']).open('rb') as src,target.open('xb') as dst:
        for block in iter(lambda:src.read(1048576),b''):dst.write(block)
        dst.flush();os.fsync(dst.fileno())
    cp=pin(target);ck(cp['sha256']==row['sha256'] and cp['size_bytes']==row['size_bytes'],'full copy bytes equal distinct saved identity');verify(row);saved.append(dict(original=row,saved=cp))
after_copies=complete_account(4*2**20)
for row in tuple(INPUTS.values()):verify(row)
finalcheckpoint=checkpoint();frozen_checks=list(CHECKS)
closure=dict(schema='SPOT_ROOT_ACTUAL_NEW6A_Q_WRITER_AND_INDEPENDENT_SAVED_REVIEW_CLOSED_BINDING_V1',status='ROOT_CLOSED_ACTUAL_NEW6A_METADATA_Q_ONLY',actual_metadata_Q=QPIN,actual_Source_writer=EXPECTED_Q_WRITER,metadata_contract_Source=EXPECTED_CONTRACT,actual_genuine_Q_writer_tool_returns=pin(WRITER_TOOLS),actual_independent_saved_Q_review=RPIN,actual_independent_saved_Q_review_tool_returns=pin(PEER_TOOLS),actual_independent_saved_Q_review_Source=EXPECTED_PEER_SOURCE,actual_Q_writer_resource_witness=QWIT,actual_independent_saved_Q_review_resource_witness=RWIT,actual_Root_closure_Source=pin(__file__),complete_Q_declared235_EOF7ID_input_pins=q['complete_Root_metadata_EOF7ID_inputs'],complete_Root_EOF7ID_inputs=list(INPUTS.values()),all_Source_and_current_peer_fresh_inputs_fully_owned=True,original_Q_and_old_writer_frozen_ancestry_not_authorization=True,retained_source_and_actual_result_copies=saved,resources_before=before,resources_after_copies_before_closure=after_copies,actual_checkpoint=finalcheckpoint,checks=frozen_checks,check_count=len(frozen_checks),all_checks_typed_true=all(type(r['passed']) is bool and r['passed'] is True for r in frozen_checks),blockers=[],whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,science_or_BOOT_admitted=False,canonical_wired=False,whole_522_to_512_memory_pass=False,legacy_Q_authorizes_new_helper=False)
ck(closure['check_count']==len(closure['checks']) and closure['all_checks_typed_true'] is True,'frozen final closure checks count exact')
with (out/'ROOT_CLOSED_BINDING.json').open('x') as f:json.dump(closure,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
cpin=pin(out/'ROOT_CLOSED_BINDING.json')
text='本记录只完成新6a数据读取合同Q的真实写入、独立审核与Root闭环。完整235输入、原完整控件与Source/失败记录均保留。\n尚未证明完整INPUT满足512MiB；尚未授予在线双精度、AAA精度、ABA或独立耦合参考资格。原物理输入、rank2、A/B/A顺序、阈值和有界执行保持。\n'
with (out/'REPORT.txt').open('x') as f:f.write(text);f.flush();os.fsync(f.fileno())
after=complete_account(1024*1024);final=checkpoint();ck(sum(p.lstat().st_size for p in out.rglob('*') if p.is_file())<64*2**20,'Root complete publication archive64MiB')
for row in tuple(INPUTS.values()):verify(row)
frozen();signal.setitimer(signal.ITIMER_REAL,0)
print(json.dumps(dict(status=closure['status'],actual_metadata_Q=QPIN,actual_closed_Root_binding=cpin,actual_independent_review=RPIN,copied_files=len(saved),actual_complete_joint_bytes=after['complete_closure_joint_bytes'],actual_history_including_external_DE_bytes=after['original_resource_return']['history_including_external_DE_bytes'],actual_final_checkpoint=final,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)
