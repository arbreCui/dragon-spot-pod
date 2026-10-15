"""Small Source/metadata helpers; no transport, compilation or cleanup."""
import hashlib, importlib.util, json, os, stat, sys
from pathlib import Path
sys.dont_write_bytecode=True

R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
ART = R/'validation/artifacts'
BASE = Path(__file__).absolute().parent
TOP = BASE.parent
CORE = REC/'full370_unreduced_eigen_reference_source_v2'
V6 = REC/'one_actual_track_H150_NZ48_full370_component_source_v1_20261014/v6'
FINITE = REC/'current_eight_fuel_finite18_SCAT_producer_source_v1_20261015'
FINITE_ENTRY = FINITE/'v6'
FINITE_OUT = ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v2'
OUT = ART/'axial-material-current-full370-real-operator-control-20261015-v2'
CAPTURE = REC/'current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015'
CAPTURE_ENTRY = CAPTURE/'v2'
RETIREMENT_ENTRY = CAPTURE/'v3'
RETIRED_PATHS={str(ART/'axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence/A1'/n) for n in ('original_archive_index.sqlite','original_words.bin')}
CAPTURE_OUT = ART/'axial-material-current-A1-native-vector-capture-and-literal2-retirement-20261015-v1'
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
    fresh_bytes=2*2**30, history_bytes=96*2**30, cold_reserve_bytes=20971764748,
    metadata_reserve_bytes=64*2**20, free_floor_bytes=8*2**30,
    threads=1, children_at_once=1, retries=0)
FALSE = dict(physics_qualified=False, complete_reaction_authority_qualified=False,
    full_reference_qualified=False, formal_H150_NZ48_full_controls_qualified=False,
    historical_machine_bit_replay=False, historical_native_RAM_bits_verified=False,
    original_XSM_memory_bits_verified=False, scientific_accuracy_qualified=False,
    three_plane_qualified=False, GLOBAL_qualified=False, rank_qualified=False,
    online_BOOT_qualified=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False)
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def require(ok, message):
    if type(ok) is not bool or not ok:
        raise RuntimeError(message)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(p):
    q=Path(p['path']);require(str(q) not in RETIRED_PATHS,'retired A1 spools are historical only; no live reopen/current7'); s=q.lstat()
    require(q.is_absolute() and '..' not in q.parts and stat.S_ISREG(s.st_mode)
        and s.st_nlink==1 and not any(x.is_symlink() for x in (q,*q.parents))
        and identity(s)==p['identity'] and s.st_size==p['size_bytes'], 'exact current ordinary7 '+str(q))
    return q

def metadata_limit(path):
    # Match the exact upstream roles; Source/plans/tools/reviews keep8MiB.
    large={ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/Root_actual_all34_original_ASCII_infinite_SCAT_summary.json',ART/'axial-material-current-all34-original-ASCII-infinite-SCAT-producer-20261015-v1/inventories/ACTUAL_ALL34_ORIGINAL_ASCII_INFINITE_SCAT_EVIDENCE.json',FINITE_OUT/'Root_actual_eight_fuel_finite18_SCAT_summary.json',
           FINITE_OUT/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json',
           CAPTURE_OUT/'Root_actual_A1_native_vector_capture_summary.json'}
    return 64*2**20 if Path(path) in large else 8*2**20

def pin(path, maximum=None):
    q=Path(path);require(str(q) not in RETIRED_PATHS,'retired A1 spools are historical only; no hashing or regeneration'); s=q.lstat()
    require(q.is_absolute() and '..' not in q.parts and stat.S_ISREG(s.st_mode)
        and s.st_nlink==1 and not any(x.is_symlink() for x in (q,*q.parents)), 'literal ordinary pin')
    require(maximum is None or s.st_size<maximum, 'bounded Source/metadata')
    digest=hashlib.sha256(); count=0
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno()))==identity(s), 'opened7')
        while True:
            raw=f.read(2**20)
            if not raw: break
            count+=len(raw); digest.update(raw)
        require(identity(os.fstat(f.fileno()))==identity(s), 'fullEOF7')
    require(count==s.st_size and identity(q.lstat())==identity(s), 'after fullEOF7')
    return dict(path=str(q),sha256=digest.hexdigest(),size_bytes=count,identity=identity(s))

def exact(p):
    q=current(p); require(p['size_bytes']<metadata_limit(q), 'exact-role bounded Source/metadata read')
    raw=q.read_bytes(); require(hashlib.sha256(raw).hexdigest()==p['sha256'], 'Source/metadata SHA')
    current(p); return raw

def read(p):
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result, 'duplicate JSON key'); result[k]=v
        return result
    return json.loads(exact(p),object_pairs_hook=pairs,parse_constant=lambda x:
        (_ for _ in ()).throw(RuntimeError('nonfinite JSON '+x)))

def load(p,name):
    exact(p); require(name not in sys.modules, 'fresh pinned module '+name)
    spec=importlib.util.spec_from_file_location(name,p['path'])
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    require(Path(module.__file__).absolute()==Path(p['path']), 'module origin'); exact(p)
    return module

def write(path,value):
    with Path(path).open('x',encoding='utf-8') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    return pin(Path(path),64*2**20)

def unique(rows):
    result={}
    for p in rows:
        require(p['path'] not in result or result[p['path']]==p, 'one complete current pin per path')
        result[p['path']]=p
    return list(result.values())

def contains(value,wanted):
    return value==wanted or (type(value) is dict and any(contains(x,wanted) for x in value.values())) or (
        type(value) is list and any(contains(x,wanted) for x in value))

def closed0(tools,key,result_pin,result_key):
    r=tools[key]
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int
        and tools['original_integer_exit_code']==0 and type(r['exit_code']) is int
        and r['exit_code']==0 and r.get('session_id') is None, 'actual typed closed0, not a running cell')
    require(json.loads(r['output'].strip().splitlines()[-1])[result_key]==result_pin,
        'actual terminal stdout exact pin')

def check_finite(plan):
    """Inherited worker entry now requires actual finite-backed capture+retire.

    Retired A1 pair PFs are historical evidence, never live current7 inputs.
    The actual capture plan/report retain the upstream finite closure.
    """
    proof=plan['compact_capture_prerequisite_pins'];host=read(proof['host']);child=read(proof['child'])
    require(host['schema']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_GUARDED_REPORT_V1'
        and host['status']=='ACTUAL_A1_NATIVE_VECTOR_CAPTURE_26R4_104B_CLOSED0_ONLY'
        and host['failure'] is None and host.get('after_check_error') is None and host['secondary_failures']==[] and host['actual_evidence']==child
        and host['final_report_resource_check_passed'] is True
        and len(host['records'])==1 and host['records'][0]['status']=='PASS'
        and host['original_caps']==CAPS,'actual one closed capture under original owning caps')
    require(child['schema']=='ACTUAL_A1_NATIVE_26_REAL32_VECTOR_CAPTURE_V1'
        and child['status']=='A1_NATIVE_26_REAL32_WORDS_104B_CAPTURE_CLOSED0_ONLY'
        and child['compact_vector_full_pin']==plan['compact_native_vector_pin']
        and child['compact_vector_full_pin']['size_bytes']==104 and child['captured_original_record_count']==4 and child['captured_REAL32_words']==26 and child['captured_bytes']==104 and child['original_small_vectors_called_unchanged'] is True,'actual original104B compact capture')
    rows=child['native_vector_record_descriptors']
    expected=[('XMU$MCCG',4,0),('ZMU$MCCG',4,16),('WZMU$MCCG',4,32),('V$MCCG',14,48)]
    require(type(rows) is list and len(rows)==4,'four original native vector descriptors')
    for row,(name,words,offset) in zip(rows,expected):
        require(row['name']==name and row['path']==['TRACK',1,name] and row['kind']==2
            and row['words']==words and row['offset_bytes']==offset and row['captured_bytes']==4*words
            and row['captured_word_encoding']=='little_endian_REAL32'
            and row['native_payload_sha256']==row['captured_payload_sha256']
            and row['original_native_row']['native_payload_sha256']==row['native_payload_sha256'],
            'exact original/current raw record SHA and native descriptor scope')
    require(contains(host,proof['child']),'actual capture host binds exact child report')
    closed0(read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin')
    post=read(proof['post'])
    require(post['schema']==plan['capture_post_schema'] and post['status']==plan['capture_post_status']
        and post['status'].startswith('PASS') and post.get('failure') is None
        and all(contains(post,proof[k]) for k in ('host','child','root_tools')),
        'actual completed capture independent postverification pending')
    closed0(read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')
    retire=plan['literal2_retirement_prerequisite_pins'];receipt=read(retire['receipt'])
    targets=[child['original_A1_SQLite_pin'],child['original_A1_pool_pin']]
    require(receipt['schema']=='LITERAL2_COMPLETED_A1_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1'
        and receipt['mode']=='execute' and receipt['status']=='RETIRED_EXACT_LITERAL2_COMPLETED_A1_COMPARE_SPOOLS_ONLY'
        and receipt['failure'] is None and receipt['exact_target_pins']==targets
        and receipt['actual_released_pins']==targets and receipt['actual_released_bytes']==202708660
        and receipt['files_deleted'] is True,'exact actual literal2 completed spool retirement')
    for key,wanted in [('capture_host_pin',proof['host']),('capture_child_pin',proof['child']),
        ('compact_vector_full_pin',plan['compact_native_vector_pin']),('capture_post_pin',proof['post']),
        ('capture_root_tools_pin',proof['root_tools']),('capture_post_tools_pin',proof['post_tools'])]:
        require(receipt[key]==wanted,'retirement binds exact new capture/proofs '+key)
    require(all(not os.path.lexists(p['path']) for p in targets),'only exact two retired paths absent')
    for p in receipt['preserved_current7_pins']+receipt['preserved_full_provenance_pins']:current(p)
    require(receipt['complete_joint_roots']==plan['inherited_complete_joint_roots'] and len(receipt['fresh_ps_lsof_pins'])==2 and receipt['fresh_ps_lsof_checks_passed'] is True,'same54 root ledger and actual fresh process/open-handle guards')
    for p in receipt['fresh_ps_lsof_pins']:current(p)
    current(plan['compact_native_vector_pin'])
    closed0(read(retire['root_tools']),'actual_terminal_return',retire['receipt'],'receipt_pin')
    rpost=read(retire['post'])
    require(rpost['schema']==plan['retirement_post_schema'] and rpost['status']==plan['retirement_post_status']
        and rpost['status'].startswith('PASS') and rpost.get('failure') is None
        and contains(rpost,retire['receipt']) and contains(rpost,retire['root_tools'])
        and contains(rpost,proof['post']) and contains(rpost,plan['compact_native_vector_pin']),'actual literal2 independent post binds closure and capture')
    closed0(read(retire['post_tools']),'actual_review_return',retire['post'],'review_pin')
    for value in (host,child,post,receipt,rpost):
        for k in ('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'):
            if k in value: require(value[k] is False,'capture/retirement never grant physics')
    require(all(p['path'] not in RETIRED_PATHS for p in plan.get('scientific_input_current7_pins',[])+plan.get('source_dependency_pins',[])),'retired pair excluded from all live science/dependency lists')
    if 'current_original_A1_native_archive_pin' in plan:current(plan['current_original_A1_native_archive_pin'])
    return dict(capture=proof,retirement=retire)


def snapshot(file,value):
    data=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();file.seek(0);file.write(data);file.truncate();file.flush();os.fsync(file.fileno())
