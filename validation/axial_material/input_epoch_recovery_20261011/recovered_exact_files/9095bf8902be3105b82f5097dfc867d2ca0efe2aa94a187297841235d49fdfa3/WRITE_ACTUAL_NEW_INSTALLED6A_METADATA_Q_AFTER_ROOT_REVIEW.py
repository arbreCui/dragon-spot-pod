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

OLD_SOURCE_ROOT='/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp'
_OLD_SOURCE_NAMES=['ACTUAL_SAVED_CLOSED_EVIDENCE_SCHEMA_REVIEW.json', 'FINAL_SOURCE_ONLY_MANIFEST.json', 'SOURCE_ONLY_SCOPE_AND_MINIMUM_WHOLE_INPUT_PATH.txt', 'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py', 'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py', 'installed6a_closed_metadata_admission_contract.py']
_NEW_SOURCE_NAMES=['WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py', 'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py', 'CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json', 'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json']
_AUDIT_EVIDENCE_PINS=[{'path': '/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.json', 'size_bytes': 878501, 'sha256': 'fb60701155f40e1c5ee443908dede50c762cedd572e4f173fae78d2eea7593c6', 'identity': [16777229, 49659606, 33188, 1, 878501, 1791704416075077205, 1791704416075077205]}, {'path': '/private/tmp/new_q_contract_independent_scope_supplement_v29_v2_countfinal_20261011.json', 'size_bytes': 8765, 'sha256': '8bb43ce15efc295455347938ee859291229af03de7146845a678b993c05fd6fb', 'identity': [16777229, 49659821, 33188, 1, 8765, 1791704615690627309, 1791704615690627309]}]


FAILED_WRITER_SOURCE_ROOT='/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_CORRECTED_SOURCE_ONLY_V29_m_27vcch'
_FAILED_SOURCE_NAMES=['CORRECTED_SOURCE_WHOLE_INVERSE_AND_SCHEMA_PROOF.json', 'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json', 'UNREADY_NEW_INSTALLED6A_ORIGINAL_COMBINED_FACTORY.py', 'WRITE_ACTUAL_NEW_INSTALLED6A_METADATA_Q_AFTER_ROOT_REVIEW.py']
_CURRENT_FRESH_EXPLICIT_PINS=[{'path': '/private/tmp/new_q_contract_independent_audit_v29_20261011.py', 'size_bytes': 12120, 'sha256': '7616febccf3718cb1c935545b44ab6fcd80f1b754a9d925c15e412c931646f81', 'identity': [16777229, 49657098, 33188, 1, 12120, 1791702965894771656, 1791702965894771656]}, {'path': '/private/tmp/new_q_contract_independent_audit_v29_20261011.json', 'size_bytes': 878501, 'sha256': '8edd36ad15198cb7075e9ad51c1ed7775bcd41dc6dfed8bd656fccada784e897', 'identity': [16777229, 49657100, 33188, 1, 878501, 1791702966247218874, 1791702966247218874]}, {'path': '/private/tmp/new_q_contract_independent_scope_supplement_v29_20261011.json', 'size_bytes': 7016, 'sha256': 'be370d190a958e9b0026f315cd93a601d27cc38d6c2992d9eb4305d4d5a77ee8', 'identity': [16777229, 49657182, 33188, 1, 7016, 1791703078736709870, 1791703078736709870]}, {'path': '/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.py', 'size_bytes': 12227, 'sha256': '56e42fa4cff2e780849b66d53b5c2c4850d8a8170321d8ca6929e099955fa94d', 'identity': [16777229, 49659604, 33188, 1, 12227, 1791704415745460880, 1791704415745460880]}, {'path': '/private/tmp/new_q_contract_independent_audit_v29_v2_countfinal_20261011.json', 'size_bytes': 878501, 'sha256': 'fb60701155f40e1c5ee443908dede50c762cedd572e4f173fae78d2eea7593c6', 'identity': [16777229, 49659606, 33188, 1, 878501, 1791704416075077205, 1791704416075077205]}, {'path': '/private/tmp/new_q_contract_independent_scope_supplement_v29_v2_countfinal_20261011.json', 'size_bytes': 8765, 'sha256': '8bb43ce15efc295455347938ee859291229af03de7146845a678b993c05fd6fb', 'identity': [16777229, 49659821, 33188, 1, 8765, 1791704615690627309, 1791704615690627309]}, {'path': '/private/tmp/new_q_independent_audit_v2_countfinal_Source_inverse_20261011.json', 'size_bytes': 1736, 'sha256': '1d288a2305e30ac5d2ed3cc0de8f238de8a06543cb6149643673344d330ec2df', 'identity': [16777229, 49659605, 33188, 1, 1736, 1791704415745741798, 1791704415745741798]}, {'path': '/private/tmp/new_q_contract_independent_audit_v2_actual_tool_return_20261011.json', 'size_bytes': 1585, 'sha256': '95ce911cb865e3e347cf52b4b7c16358851e3b1ae5d34baa58a86ff46f04198f', 'identity': [16777229, 49659739, 33188, 1, 1585, 1791704533929672856, 1791704533929672856]}, {'path': '/private/tmp/new_q_corrected_source_prepare_v29_20261011.py', 'size_bytes': 16675, 'sha256': '6d2c9418e7d43c6f5bf83b5754b6c36cea7b9b7e5d53004e36e5ac11d7d3db3e', 'identity': [16777229, 49657328, 33188, 1, 16675, 1791703252675724494, 1791703252675724494]}, {'path': '/private/tmp/new_q_corrected_source_prepare_v29_v2_20261011.py', 'size_bytes': 16713, 'sha256': '6f90d312d4c37d186075eeb79e491d6ea87b8681cde9280cd1471e1b6ca7a972', 'identity': [16777229, 49657378, 33188, 1, 16713, 1791703293605264638, 1791703293605264638]}, {'path': '/private/tmp/new_q_corrected_source_prepare_v1_actual_failed_tool_return_20261011.json', 'size_bytes': 1613, 'sha256': '7137688899253b62d838a457c37f4e66254732811430c001351732213cc91304', 'identity': [16777229, 49657379, 33188, 1, 1613, 1791703293606979769, 1791703293606979769]}, {'path': '/private/tmp/new_q_corrected_source_v2_final_schema_review_20261011.json', 'size_bytes': 2029, 'sha256': '34d7df91ecd112211bec824d71d4592c88fec43244b0c853f73911bd54b693fe', 'identity': [16777229, 49657427, 33188, 1, 2029, 1791703336677850118, 1791703336677850118]}, {'path': '/private/tmp/Root_corrected_new6a_Q_actual_tool_returns_20261011.json', 'size_bytes': 2459, 'sha256': 'f3c957bf6481a608d30cf63455811dc1c9e1876d48738da18b865bdcaac05d7c', 'identity': [16777229, 49659370, 33188, 1, 2459, 1791704327539225644, 1791704327539225644]}, {'path': '/private/tmp/new_q_corrected_source_prepare_v29_v3_actual_countfinal_20261011.py', 'size_bytes': 14410, 'sha256': '8e3847afc318ca01e86846fab1cfc7e92cfbd8e70467f74b93f421bd0b5535b6', 'identity': [16777229, 49660043, 33188, 1, 14410, 1791704692662905792, 1791704692662905792]}]
_FAILED_WRITER_ACTUAL_TOOLS_PIN={'path': '/private/tmp/Root_corrected_new6a_Q_actual_tool_returns_20261011.json', 'size_bytes': 2459, 'sha256': 'f3c957bf6481a608d30cf63455811dc1c9e1876d48738da18b865bdcaac05d7c', 'identity': [16777229, 49659370, 33188, 1, 2459, 1791704327539225644, 1791704327539225644]}
_ROOT_REVIEW_SOURCE_PATH='/private/tmp/Root_review_corrected_new6a_Q_Source_v3_20261011.py'
_ROOT_REVIEW_REPORT_PATH='/private/tmp/Root_corrected_new6a_Q_independent_Source_review_v3_20261011.json'
_CURRENT_FRESH_RUNTIME_PINS=[]

def verify_current_fresh_inputs_and_actual_Root_prelaunch_review():
    global _CURRENT_FRESH_RUNTIME_PINS
    for r in _CURRENT_FRESH_EXPLICIT_PINS:assert pin(r['path'])==r
    failed=_read_pinned_audit(_FAILED_WRITER_ACTUAL_TOOLS_PIN)
    assert failed['initial']==failed['closed'] and failed['closed']['chunk_id']=='7ed0a8' and type(failed['closed']['exit_code']) is int and failed['closed']['exit_code']==1 and 'session_id' not in failed['closed']
    assert 'verify_preserved_independent_audit_inputs' in failed['closed']['output'] and 'AssertionError' in failed['closed']['output']
    root_Source_pin=pin(_ROOT_REVIEW_SOURCE_PATH);root_report_pin=pin(_ROOT_REVIEW_REPORT_PATH)
    root_report=_read_pinned_audit(root_report_pin)
    assert root_report['status']=='ROOT_SOURCE_REVIEW_PASS_AUTHORIZE_ONE_ACTUAL_NEW6A_METADATA_Q_WRITER'
    assert root_report['writer']==pin(__file__) and root_report['metadata_contract']==CONTRACT_PIN
    assert root_report['manifest']==pin(Path(__file__).parent/'FINAL_CORRECTED_SOURCE_ONLY_MANIFEST.json')
    for key in ('whole_writer_inverse_and_original_function_AST_equal','whole_factory_inverse_to_117ec099_equal','original_resource_prefix_preserved','original_scientific_and_complete_build_gates_not_granted'):assert root_report[key] is True
    _CURRENT_FRESH_RUNTIME_PINS=_CURRENT_FRESH_EXPLICIT_PINS+[root_Source_pin,root_report_pin]

# A new Source family is added without altering the original resource prefix.
_SOURCE_ROOTS = [Path(OLD_SOURCE_ROOT), Path(FAILED_WRITER_SOURCE_ROOT), Path(__file__).parent]
_SOURCE_NAMESPACE_BEFORE = None
_PRESERVED_AUDIT_INPUTS = []

def _audit_json_pairs(rows):
    d={}
    for k,v in rows:
        assert k not in d,'duplicate audit JSON key'
        d[k]=v
    return d

def _audit_json_nonfinite(value):
    raise ValueError('nonfinite saved independent review metadata')

def _read_pinned_audit(wanted):
    assert pin(wanted['path'])==wanted
    with Path(wanted['path']).open('rt',encoding='utf8') as f:
        value=json.load(f,object_pairs_hook=_audit_json_pairs,parse_constant=_audit_json_nonfinite)
    assert pin(wanted['path'])==wanted
    return value

def verify_preserved_independent_audit_inputs():
    global _PRESERVED_AUDIT_INPUTS
    first,scope=(_read_pinned_audit(p) for p in _AUDIT_EVIDENCE_PINS)
    assert first['schema']=='SPOT_V29_NEW6A_Q_CONTRACT_INDEPENDENT_SOURCE_ONLY_AUDIT_V1'
    assert first['Source_only'] is True and first['writer_factory_helper_production_Native_or_PS_executed'] is False and first['all_checks_typed_true'] is True
    assert type(first['check_count']) is int and first['check_count']==len(first['checks']) and all(type(c['passed']) is bool and c['passed'] is True for c in first['checks'])
    assert scope['schema']=='SPOT_V29_NEW6A_Q_INDEPENDENT_RESOURCE_SCOPE_SUPPLEMENT_V1' and scope['Source_only'] is True and scope['writer_factory_Native_or_PS_executed'] is False
    assert scope['initial_readonly_audit']==_AUDIT_EVIDENCE_PINS[0]
    assert scope['actual_original_pure_joint_scope']=='Original d19 H/O/C+D/E plus Root publication; pure H/O use original 64MiB protocol archive guard and remain in complete96GiB history'
    rows=first['all_verified_inputs'];assert type(rows) is list and len(rows)==209 and len({r['path'] for r in rows})==209
    for r in rows:
        assert type(r['identity']) is list and len(r['identity'])==7 and all(type(v) is int for v in r['identity'])
        assert pin(r['path'])==r
    old=scope['new_Q_Source_package_complete_root'];assert old['path']==OLD_SOURCE_ROOT and sorted(old['names'])==_OLD_SOURCE_NAMES and len(old['files'])==6 and old['complete_regular_bytes']==459468
    assert ids_old_root()==old['identity']
    for r in old['files']:assert pin(r['path'])==r
    _PRESERVED_AUDIT_INPUTS=rows+_AUDIT_EVIDENCE_PINS

def ids_old_root():
    return identity(Path(OLD_SOURCE_ROOT).lstat())

def complete_Source_namespace(root,expected_names):
    root=Path(root);assert root.is_dir() and not root.is_symlink()
    for p in root.parents:assert not p.is_symlink()
    before=identity(root.lstat());paths=sorted(root.rglob('*'),key=str)
    assert sorted(p.name for p in root.iterdir())==sorted(expected_names)
    directories=[dict(path=str(root),identity=before)];files=[]
    for p in paths:
        s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
        if stat.S_ISDIR(s.st_mode):directories.append(dict(path=str(p),identity=identity(s)))
        else:assert stat.S_ISREG(s.st_mode) and s.st_nlink==1;files.append(pin(p))
    assert paths==sorted(root.rglob('*'),key=str) and identity(root.lstat())==before
    for r in directories:assert identity(Path(r['path']).lstat())==r['identity']
    return dict(root=str(root),directories=directories,files=files,regular_bytes=sum(r['size_bytes'] for r in files))

def _complete_new_Q_joint_inode_once():
    roots=[H,O,C,out,AH,AO,AS,*_SOURCE_ROOTS]
    roots += [Path(min(record['directories'],key=lambda p:len(Path(p).parts))) for record in t['current_complete_D_E_freeze'].values()]
    seen=set();total=0;root_records=[]
    for root in roots:
        if not root.exists():assert not root.is_symlink();continue
        assert root.is_dir() and not root.is_symlink()
        paths=sorted(root.rglob('*'),key=str);before=identity(root.lstat());root_bytes=0
        for p in paths:
            s=p.lstat();assert not stat.S_ISLNK(s.st_mode)
            if stat.S_ISDIR(s.st_mode):continue
            assert stat.S_ISREG(s.st_mode) and s.st_nlink==1
            key=(s.st_dev,s.st_ino)
            if key not in seen:seen.add(key);total+=s.st_size;root_bytes+=s.st_size
        assert paths==sorted(root.rglob('*'),key=str) and identity(root.lstat())==before
        root_records.append(dict(path=str(root),identity=before,new_unique_regular_bytes=root_bytes))
    for r in _CURRENT_FRESH_RUNTIME_PINS:
        assert pin(r['path'])==r
        key=(r['identity'][0],r['identity'][1]);added=0
        if key not in seen:seen.add(key);total+=r['size_bytes'];added=r['size_bytes']
        root_records.append(dict(path=r['path'],identity=r['identity'],new_unique_regular_bytes=added,kind='current_stage_fresh_explicit_regular_file'))
    return total,root_records

def account_complete_new_Q(reserve):
    global _SOURCE_NAMESPACE_BEFORE
    assert type(reserve) is int and reserve>=0
    original=account(reserve)
    namespaces=[complete_Source_namespace(_SOURCE_ROOTS[0],_OLD_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[1],_FAILED_SOURCE_NAMES),complete_Source_namespace(_SOURCE_ROOTS[2],_NEW_SOURCE_NAMES)]
    if _SOURCE_NAMESPACE_BEFORE is None:_SOURCE_NAMESPACE_BEFORE=namespaces
    else:assert namespaces==_SOURCE_NAMESPACE_BEFORE,'whole original and new Source namespace changed'
    complete,roots=_complete_new_Q_joint_inode_once()
    assert complete>=original['joint_bytes'] and complete+reserve<2*2**30
    frees={str(root):int(os.statvfs(root).f_bavail)*int(os.statvfs(root).f_frsize) for root in _SOURCE_ROOTS}
    assert min([*frees.values(),*(int(os.statvfs(Path(r['path']).parent).f_bavail)*int(os.statvfs(Path(r['path']).parent).f_frsize) for r in _CURRENT_FRESH_RUNTIME_PINS)])-reserve>=8*2**30
    assert time.monotonic()-started<600
    for r in _PRESERVED_AUDIT_INPUTS+_CURRENT_FRESH_RUNTIME_PINS:assert pin(r['path'])==r
    return dict(original_resource_return=original,complete_new_Q_joint_bytes=complete,additional_unique_Source_bytes=complete-original['joint_bytes'],reserved_bytes=reserve,complete_joint_cap_bytes=2*2**30,complete_joint_roots_inode_once=roots,complete_original_and_new_Source_namespaces=namespaces,tmp_disk_free_bytes=frees,current_stage_fresh_explicit_file_pins=_CURRENT_FRESH_RUNTIME_PINS,min_free_bytes=8*2**30,reused_closed_protocol_scope='Original v27 and v28 protocol64MiB controls remain complete historical inputs under original96GiB history; no37k-canonical fresh2GiB substitution',original_five_guards_and_DE_preserved=True)

def complete_Q_input_pins(fixed,extra):
    rows={}
    for r in fixed+extra+_PRESERVED_AUDIT_INPUTS+_CURRENT_FRESH_RUNTIME_PINS+[r for ns in _SOURCE_NAMESPACE_BEFORE for r in ns['files']]:
        assert pin(r['path'])==r
        if r['path'] in rows:assert rows[r['path']]==r
        rows[r['path']]=r
    return list(rows.values())

verify_current_fresh_inputs_and_actual_Root_prelaunch_review()
verify_preserved_independent_audit_inputs()
assert len(sys.argv)==1 and Path(sys.executable).resolve()==Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12').resolve()
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN
spec=importlib.util.spec_from_file_location('new_installed6a_metadata_Q_actual_contract',CONTRACT_PIN['path']);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
evidence,fixed=module.validate_closed_evidence()
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN
selfpin=pin(__file__)
before=account_complete_new_Q(64*2**20);checkpoint()
out.mkdir(mode=0o700)
q=dict(schema='SPOT_INSTALLED6A_ACTUAL_ORIGINAL_PURE_AND_FULLFRESH_HELPER_METADATA_Q_V29',status='QUALIFIED_INSTALLED6A_ORIGINAL_PURE_FULL_CURRENT_GRAPH_METADATA_ONLY',scope='HELPER_METADATA_ORIGINAL_COMPLETE_PROTOCOL_AND_SAME_CURRENT_GRAPH_VERIFIER_ONLY_NO_WHOLE_INPUT_BUILD_NATIVE_OR_SCIENCE',complete_actual_new6a_closed_evidence=evidence,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,complete_Root_metadata_EOF7ID_inputs=complete_Q_input_pins(fixed,[selfpin,CONTRACT_PIN]),original_resource_prefix_Source=ORIGINAL_PREFIX_PIN,original_resource_prefix_full_inverse_sha256=ORIGINAL_PREFIX_SHA,resources_before=before,external_writer_checkpoint=checkpoint(),whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,canonical_wired=False,science_or_BOOT_admitted=False,legacy_Q_authorizes_new_helper=False)
for p in fixed:assert pin(p['path'])==p
assert pin(__file__)==selfpin
with (out/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json').open('x') as f:json.dump(q,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
qpin=pin(out/'ACTUAL_INSTALLED6A_HELPER_METADATA_Q.json')
after=account_complete_new_Q(1024*1024)
finalcheckpoint=checkpoint()
witness=dict(schema='SPOT_V29_ACTUAL_NEW6A_METADATA_Q_WRITER_COMPLETE_RESOURCE_WITNESS_V1',actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,resources_before=before,resources_after_Q_before_witness=after,checkpoint_after_Q_before_witness=finalcheckpoint,complete_Root_metadata_EOF7ID_inputs=q['complete_Root_metadata_EOF7ID_inputs'],writer_does_not_PIN_its_future_self_receipt=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)
with (out/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json').open('x') as f:json.dump(witness,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
witnesspin=pin(out/'ACTUAL_NEW6A_Q_COMPLETE_RESOURCE_WITNESS.json')
assert witnesspin['size_bytes']<1024*1024
final_after_witness=account_complete_new_Q(0)
final_after_witness_checkpoint=checkpoint()
assert sum(p.lstat().st_size for p in out.rglob('*') if p.is_file())<64*2**20
for p in fixed:assert pin(p['path'])==p
assert pin(CONTRACT_PIN['path'])==CONTRACT_PIN and pin(__file__)==selfpin
signal.setitimer(signal.ITIMER_REAL,0)
print(json.dumps(dict(status=q['status'],actual_metadata_Q=qpin,actual_Source_writer=selfpin,metadata_contract_Source=CONTRACT_PIN,actual_complete_resource_witness=witnesspin,actual_final_complete_joint_bytes=final_after_witness['complete_new_Q_joint_bytes'],actual_final_history_including_external_DE_bytes=final_after_witness['original_resource_return']['history_including_external_DE_bytes'],actual_final_checkpoint=final_after_witness_checkpoint,new_Q_created=True,whole_build_qualified=False,whole_INPUT_admitted=False,science_or_BOOT_admitted=False)),flush=True)
