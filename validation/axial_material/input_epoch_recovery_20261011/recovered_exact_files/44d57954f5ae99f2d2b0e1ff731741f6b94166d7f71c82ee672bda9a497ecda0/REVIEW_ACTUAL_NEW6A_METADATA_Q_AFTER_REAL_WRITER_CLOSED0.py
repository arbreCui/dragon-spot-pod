import sys
_PYTHON_PROCESS_ATTEMPTS=[]
def _forbid(event,args):
    if event in ('subprocess.Popen','os.system','os.fork','os.forkpty','os.exec','os.posix_spawn','os.spawn','os.startfile','os.startfile/2'):
        _PYTHON_PROCESS_ATTEMPTS.append(event);raise RuntimeError('independent pure metadata Q review forbids Python process launches')
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
out = A / 'axial-material-installed6a-Q-independent-saved-review-v29-20261011'
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


EXPECTED_WRITER={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py', 'size_bytes': 24385, 'sha256': '9095bf8902be3105b82f5097dfc867d2ca0efe2aa94a187297841235d49fdfa3', 'identity': [16777229, 49660046, 33188, 1, 24385, 1791704692801967693, 1791704692801967693]}
EXPECTED_CONTRACT={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/installed6a_closed_metadata_admission_contract.py', 'size_bytes': 33913, 'sha256': 'f574c3d985847417bb906028177fdf50f85081bec506640abadfaa3547b6f4d1', 'identity': [16777229, 49656560, 33188, 1, 33913, 1791702643852949734, 1791702643852949734]}
EXPECTED_MANIFEST={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json', 'size_bytes': 103587, 'sha256': 'd62b0cabc7be06eb47c29a826b7f500a3cb5e9ec6090773b61b672df6d8aae02', 'identity': [16777229, 49660049, 33188, 1, 103587, 1791704692926812011, 1791704692926812011]}
EXPECTED_FACTORY={'path': '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py', 'size_bytes': 199668, 'sha256': 'e40972672c752de6bddc905525e1dfef389fd41fd6451cdac4a5c3dc5ecaa308', 'identity': [16777229, 49660047, 33188, 1, 199668, 1791704692802579236, 1791704692802579236]}
ACTUAL_WRITER_TOOL_FILE='/private/tmp/Root_corrected_new6a_Q_v3_actual_tool_returns_20261011.json'
EXPECTED_COMMAND='env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B /private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_V3_COUNTFINAL_unkdz2l9/WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py'
QROOT=Path('/Users/wen/spot/validation/artifacts/axial-material-installed6a-helper-metadata-admission-v29-20261011')

import importlib.util,math,resource,signal,struct,threading,re
CHECKS=[];INPUTS={}
def ck(value,message):
    if type(value) is not bool or not value:raise ValueError('independent saved Q review: '+message)
    CHECKS.append(dict(name=message,passed=True))
def verify(wanted):
    ck(type(wanted) is dict and type(wanted['path']) is str and type(wanted['identity']) is list and len(wanted['identity'])==7 and all(type(v) is int for v in wanted['identity']),'typed full7ID input')
    actual=pin(wanted['path']);ck(actual=={k:wanted[k] for k in actual},'whole EOF7ID '+wanted['path'])
    if actual['path'] in INPUTS:ck(INPUTS[actual['path']]==actual,'same repeated EOF input')
    INPUTS[actual['path']]=actual;return actual
def pairs(rows):
    d={}
    for k,v in rows:
        if k in d:raise ValueError('duplicate saved JSON key')
        d[k]=v
    return d
def nonfinite(value):raise ValueError('nonfinite saved JSON '+value)
def read(p,expected=None):
    before=pin(p)
    if expected is not None:verify(expected);ck(before==expected,'bound complete saved JSON')
    with Path(p).open('rt',encoding='utf8') as f:value=json.load(f,object_pairs_hook=pairs,parse_constant=nonfinite)
    ck(pin(p)==before,'saved JSON unchanged after load');INPUTS[before['path']]=before;return value
def exact(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return list(a)==list(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    if type(a) is float:return math.isfinite(a) and math.isfinite(b) and struct.pack('>d',a)==struct.pack('>d',b)
    return a==b
def unique_rows(rows):
    ck(type(rows) is list and len(rows)>0,'nonempty full declared input list');d={}
    for row in rows:
        verify(row);ck(row['path'] not in d,'declared input path unique');d[row['path']]=row
    return d
def collect_rows(rows):
    d={}
    for row in rows:
        verify(row)
        if row['path'] in d:ck(d[row['path']]==row,'mandatory duplicate matches full pin')
        d[row['path']]=row
    return d
def checkpoint():
    rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    ck(0<=rss<512*2**20 and threading.active_count()==1 and not _PYTHON_PROCESS_ATTEMPTS and time.monotonic()-started<600,'original own512/600/thread1/no Python launch observed')
    return dict(seconds=time.monotonic()-started,own_peak_rss_bytes=rss,Python_process_attempts=list(_PYTHON_PROCESS_ATTEMPTS),Python_audit_scope='Named events after hook; native/C and pre-script children not observed')
def deadline(signum,frame):raise TimeoutError('original600s independent metadata review cap')
signal.signal(signal.SIGALRM,deadline);signal.setitimer(signal.ITIMER_REAL,600)
ck(len(sys.argv)==1 and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12').resolve(),'canonical interpreter no extra arguments')
verify(EXPECTED_WRITER);verify(EXPECTED_CONTRACT);verify(EXPECTED_MANIFEST);verify(EXPECTED_FACTORY)
manifest=read(EXPECTED_MANIFEST['path'],EXPECTED_MANIFEST);ck(manifest['corrected_writer_Source']==EXPECTED_WRITER and manifest['corrected_UNREADY_factory_Source']==EXPECTED_FACTORY and manifest['metadata_contract_Source']==EXPECTED_CONTRACT,'actual Source manifest bindings')
# No candidate writer, factory or helper numerical function is invoked.
spec=importlib.util.spec_from_file_location('saved_new6a_pure_metadata_contract_independent_review',EXPECTED_CONTRACT['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
tools=read(ACTUAL_WRITER_TOOL_FILE);initial,closed=tools['initial'],tools['closed']
ck(type(closed['exit_code']) is int and closed['exit_code']==0 and 'session_id' not in closed and closed['chunk_id']=='11666a','actual genuine closed integer0 writer')
ck(initial['chunk_id']=='c81bec' and initial['session_id']==24272,'actual initial writer launch bound to this unique saved process')
if tools.get('terminal_in_initial_call') is True:ck(exact(initial,closed),'genuine terminal in initial API call full object retained')
else:ck(type(initial['session_id']) is int and 'exit_code' not in initial and type(initial['chunk_id']) is str,'actual yielded initial session retained')
ck(tools['actual_command']==EXPECTED_COMMAND,'actual canonical no-profile writer command exact')
ck(type(closed['output']) is str and not tools.get('closed_output_truncated_by_tool',False),'small actual writer stdout complete')
stdout=json.loads(closed['output'],object_pairs_hook=pairs,parse_constant=nonfinite)
ck(stdout['status']=='QUALIFIED_INSTALLED6A_ORIGINAL_PURE_FULL_CURRENT_GRAPH_METADATA_ONLY' and stdout['new_Q_created'] is True,'actual new Q created metadata only')
for key in ('whole_build_qualified','whole_INPUT_admitted','science_or_BOOT_admitted'):ck(stdout[key] is False,'writer stdout no '+key)
ck(stdout['actual_Source_writer']==EXPECTED_WRITER and stdout['metadata_contract_Source']==EXPECTED_CONTRACT,'actual stdout writer and contract fullpins')
QPIN=stdout['actual_metadata_Q'];WPIN=stdout['actual_complete_resource_witness'];verify(QPIN);verify(WPIN)
ck(QPIN['path']==str(QROOT/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json') and WPIN['path']==str(QROOT/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json'),'actual two distinct Q/witness endpoints')
q=read(QPIN['path'],QPIN);witness=read(WPIN['path'],WPIN)
ck(q['schema']=='SPOT_INSTALLED6A_ACTUAL_ORIGINAL_PURE_AND_FULLFRESH_HELPER_METADATA_Q_V29' and q['status']==stdout['status'],'actual new distinct Q schema/status')
ck(q['scope']=='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE','helper metadata-only scope')
for key in ('whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','canonical_wired','science_or_BOOT_admitted','legacy_Q_authorizes_new_helper'):ck(q[key] is False,'Q no '+key)
ck(q['actual_Source_writer']==EXPECTED_WRITER and q['metadata_contract_Source']==EXPECTED_CONTRACT,'Q actual full Source pins')
closed_evidence,fixed=module.validate_closed_evidence();ck(exact(q['complete_actual_new6a_closed_evidence'],closed_evidence),'all actual v27/v28 full contracts revalidated unchanged')
module.validate_actual_new_Q(q);verify(EXPECTED_CONTRACT)
ck(witness['schema']=='SPOT_V29_ACTUAL_NEW6A_METADATA_Q_WRITER_COMPLETE_RESOURCE_WITNESS_V1' and witness['actual_metadata_Q']==QPIN and witness['actual_Source_writer']==EXPECTED_WRITER and witness['metadata_contract_Source']==EXPECTED_CONTRACT,'actual witness full Q/writer/contract binding')
for key in ('whole_build_qualified','whole_INPUT_admitted','science_or_BOOT_admitted'):ck(witness[key] is False,'witness no '+key)
ck(witness['writer_does_not_PIN_its_future_self_receipt'] is True,'no Q/witness selfpin cycle')
ck(exact(q['resources_before'],witness['resources_before']),'actual before resource record copied complete')
ck(exact(q['complete_Root_metadata_EOF7ID_inputs'],witness['complete_Root_metadata_EOF7ID_inputs']),'witness full declared current/historical inputs copied complete')
declared=unique_rows(q['complete_Root_metadata_EOF7ID_inputs'])
actualaudit=read(manifest['new_actual_audit_and_precise_scope_supplement'][0]['path'],manifest['new_actual_audit_and_precise_scope_supplement'][0]);ck(actualaudit['check_count']==len(actualaudit['checks'])==5400 and all(type(c['passed']) is bool and c['passed'] is True for c in actualaudit['checks']),'actual original5400checks count strict, old209 inputs complete')
ck(len(actualaudit['all_verified_inputs'])==209,'all actual original209 EOF input rows')
def source_namespace(saved):
    root=Path(saved['root']);ck(root.is_dir() and not root.is_symlink(),'ordinary complete Source root');paths=sorted(root.rglob('*'),key=str);dirs=[];files=[]
    for p in [root,*paths]:
        s=p.lstat();ck(not stat.S_ISLNK(s.st_mode),'Source no aliases')
        if stat.S_ISDIR(s.st_mode):dirs.append(dict(path=str(p),identity=identity(s)))
        else:files.append(pin(p));verify(files[-1])
    actual=dict(root=str(root),directories=dirs,files=files,regular_bytes=sum(r['size_bytes'] for r in files));ck(actual==saved,'Source entire names/directories/files/fullEOF7ID preserved');return files
before=q['resources_before'];after=witness['resources_after_Q_before_witness'];sourcefiles=[]
ck(len(before['complete_original_and_new_Source_namespaces'])==3,'all original/failed-v2/new-v3 Source families counted')
for ns in before['complete_original_and_new_Source_namespaces']:sourcefiles+=source_namespace(ns)
ck(before['complete_original_and_new_Source_namespaces']==after['complete_original_and_new_Source_namespaces'],'actual whole Source roots beforeafter unchanged')
ck([r['root'] for r in before['complete_original_and_new_Source_namespaces']]==manifest['three_complete_Q_Source_family_roots'],'all three exact Source roots in declared order')
external=before['current_stage_fresh_explicit_file_pins'];ck(external==after['current_stage_fresh_explicit_file_pins'],'complete actual current fresh files beforeafter same')
ck(external[:len(manifest['explicit_current_stage_fresh_inputs'])]==manifest['explicit_current_stage_fresh_inputs'],'all actual participating14 fresh Source/audit/scope/failure file pins')
ck(len(external)==len(manifest['explicit_current_stage_fresh_inputs'])+2,'two actual Root prelaunch review files added')
review_source=pin(manifest['prelaunch_Root_review_contract']['Source_path']);review_pin=pin(manifest['prelaunch_Root_review_contract']['report_path']);ck(external[-2:]==[review_source,review_pin],'actual prelaunch Root reviewSource/result bound dynamically')
rr=read(review_pin['path'],review_pin);ck(rr['status']==manifest['prelaunch_Root_review_contract']['required_status'] and rr['writer']==EXPECTED_WRITER and rr['manifest']==EXPECTED_MANIFEST and rr['metadata_contract']==EXPECTED_CONTRACT,'genuine actual prelaunch Root report binds this writer and manifest')
for key in manifest['prelaunch_Root_review_contract']['required_true_fields']:ck(rr[key] is True,'actual Root strict Source check '+key)
mandatory=collect_rows(fixed+[EXPECTED_WRITER,EXPECTED_CONTRACT]+actualaudit['all_verified_inputs']+manifest['new_actual_audit_and_precise_scope_supplement']+external+sourcefiles)
ck(declared==mandatory and len(declared)==235,'complete current Q235 inputs exactly include all209/current fresh Source and audit pins, no old178-only subset')
ck(QPIN['path'] not in declared and WPIN['path'] not in declared,'no circular future Q/witness input qualification')
for r in declared.values():verify(r)
def saved_resource(res,reserve):
    ck(type(res['reserved_bytes']) is int and res['reserved_bytes']==reserve and res['complete_joint_cap_bytes']==2*2**30 and res['min_free_bytes']==8*2**30,'saved original joint2/free8/reservation')
    orig=res['original_resource_return'];ck(orig['reserved_bytes']==reserve,'actual original reservation retained');h=orig['original_resource_checks']['complete_history'];f=orig['original_resource_checks']['fresh_output']
    ck(h['artifact_budget_bytes']==96*2**30 and f['artifact_budget_bytes']==2*2**30 and h['min_free_bytes']==f['min_free_bytes']==8*2**30,'actual original96/fresh2/free8 check returns')
    ck(orig['history_including_external_DE_bytes']==h['artifact_bytes']+t['current_external_DE_bytes'] and orig['history_including_external_DE_bytes']+reserve<=96*2**30,'actual wholehistory + DE once bound')
    ck(min(h['disk_free_bytes'],f['disk_free_bytes'],*res['tmp_disk_free_bytes'].values())-reserve>=8*2**30,'actual original and TMP free8 reserved')
    ck(res['complete_new_Q_joint_bytes']==orig['joint_bytes']+res['additional_unique_Source_bytes'] and res['complete_new_Q_joint_bytes']+reserve<2*2**30 and res['original_five_guards_and_DE_preserved'] is True,'complete supplemental joint original bytes + exact additions bounded')
    ck(sum(r['new_unique_regular_bytes'] for r in res['complete_joint_roots_inode_once'])==res['complete_new_Q_joint_bytes'],'saved complete per-root/file inode-once sum exact')
saved_resource(before,64*2**20);saved_resource(after,1024*1024)
ck(after['complete_new_Q_joint_bytes']-before['complete_new_Q_joint_bytes']==QPIN['size_bytes'],'actual wholejoint grew by full Q bytes only before witness')
# Recount all actual current complete stage roots/files independently, never all37k history into fresh.
seen_inodes=set();current_joint=0
for row in after['complete_joint_roots_inode_once']:
    p=Path(row['path']);s=p.lstat();ck(not stat.S_ISLNK(s.st_mode),'current joint no alias')
    members=sorted(p.rglob('*'),key=str) if stat.S_ISDIR(s.st_mode) else [p]
    for member in members:
        ms=member.lstat();ck(not stat.S_ISLNK(ms.st_mode),'joint member no alias')
        if stat.S_ISDIR(ms.st_mode):continue
        ck(stat.S_ISREG(ms.st_mode) and ms.st_nlink==1,'joint ordinary singlelink current file');key=(ms.st_dev,ms.st_ino)
        if key not in seen_inodes:seen_inodes.add(key);current_joint+=ms.st_size
ck(current_joint==stdout['actual_final_complete_joint_bytes']==after['complete_new_Q_joint_bytes']+WPIN['size_bytes'],'actual afterwitness complete joint equals independently recounted full current family')
ck(type(stdout['actual_final_history_including_external_DE_bytes']) is int and stdout['actual_final_history_including_external_DE_bytes']<=96*2**30 and stdout['actual_final_history_including_external_DE_bytes']>=after['original_resource_return']['history_including_external_DE_bytes']+WPIN['size_bytes'],'actual final96 history tool observation bounded including witness')
def writer_checkpoint(row):
    ck(type(row['seconds']) is float and math.isfinite(row['seconds']) and 0<row['seconds']<600 and type(row['own_peak_rss_bytes']) is int and 0<=row['own_peak_rss_bytes']<512*2**20 and row['Python_process_attempts']==[] and row['Python_audit_scope']=='Named events after hook; native/C and pre-script children not observed','actual writer own512/600/Python audit-scope checkpoint')
for row in (q['external_writer_checkpoint'],witness['checkpoint_after_Q_before_witness'],stdout['actual_final_checkpoint']):writer_checkpoint(row)
ck(q['external_writer_checkpoint']['seconds']<=witness['checkpoint_after_Q_before_witness']['seconds']<=stdout['actual_final_checkpoint']['seconds'],'actual checkpoint monotonic whole writer sequence')
ck(sorted(p.name for p in QROOT.iterdir())==['ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json','ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json'] and QPIN['size_bytes']+WPIN['size_bytes']<64*2**20,'actual complete unique Q output namespace / original archive64')
# Actual reviewer resources use the original fiveguards/D_E/96/free8/joint2 too.
selfpin=pin(__file__);reviewSource=Path(__file__).parent
original_before=account(4*2**20);checkpoint()
allreviewfresh=collect_rows(list(declared.values())+[pin(ACTUAL_WRITER_TOOL_FILE),QPIN,WPIN,selfpin])
for r in allreviewfresh.values():verify(r)
ck(current_joint+sum(p.lstat().st_size for p in reviewSource.rglob('*') if p.is_file())+4*2**20<2*2**30,'original complete Qfamily + reviewer Source + metadata reserve2GiB')
ck(int(os.statvfs(reviewSource).f_bavail)*int(os.statvfs(reviewSource).f_frsize)-4*2**20>=8*2**30,'actual reviewer TMP free8 reserved')
for p in tuple(INPUTS.values()):verify(p)
verify(EXPECTED_CONTRACT);frozen();own_checkpoint=checkpoint()
# Complete checks are frozen only after every recorded input check is finished.
frozen_checks=list(CHECKS);report=dict(status='PASS_ACTUAL_NEW6A_Q_METADATA_ONLY',actual_metadata_Q=QPIN,actual_Source_writer=EXPECTED_WRITER,metadata_contract_Source=EXPECTED_CONTRACT,actual_resource_witness=WPIN,actual_genuine_writer_tool_returns=pin(ACTUAL_WRITER_TOOL_FILE),actual_independent_review_Source=selfpin,checks=frozen_checks,check_count=len(frozen_checks),all_checks_typed_true=all(type(c['passed']) is bool and c['passed'] is True for c in frozen_checks),blockers=[],complete_actual_Q_declared_EOF7ID_input_pins=list(declared.values()),all_this_review_EOF7ID_input_pins=list(INPUTS.values()),actual_complete_final_Q_joint_bytes=current_joint,resources_before=original_before,own_checkpoint=own_checkpoint,Source_only=False,metadata_only=True,writer_factory_Native_or_PS_executed=False,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,science_or_BOOT_admitted=False)
ck(report['check_count']==len(report['checks']) and report['check_count']>0 and report['all_checks_typed_true'] is True,'final frozen report count and bools exact')
out.mkdir(mode=0o700)
with (out/'REVIEW.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
reviewpin=pin(out/'REVIEW.json');original_after=account(1024*1024);finalcheck=checkpoint()
ck(current_joint+sum(p.lstat().st_size for p in reviewSource.rglob('*') if p.is_file())+reviewpin['size_bytes']+1024*1024<2*2**30,'review final complete current family and Source/output2GiB')
ck(reviewpin['size_bytes']<4*2**20,'review complete output reserved4MiB')
for p in allreviewfresh.values():verify(p)
frozen();signal.setitimer(signal.ITIMER_REAL,0)
print(json.dumps(dict(status=report['status'],actual_metadata_Q=QPIN,review_pin=reviewpin,actual_independent_review_Source=selfpin,metadata_contract_Source=EXPECTED_CONTRACT,check_count=report['check_count'],all_checks_typed_true=True,actual_original_after_resource_summary=dict(joint_bytes=original_after['joint_bytes'],history_including_external_DE_bytes=original_after['history_including_external_DE_bytes'],reserved_bytes=original_after['reserved_bytes']),actual_final_checkpoint=finalcheck,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)
