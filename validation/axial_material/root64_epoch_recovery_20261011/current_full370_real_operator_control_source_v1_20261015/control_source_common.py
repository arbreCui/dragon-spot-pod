"""Small Source/metadata helpers; no transport, compilation or cleanup."""
import hashlib, importlib.util, json, os, stat, sys
from pathlib import Path
sys.dont_write_bytecode=True

R = Path('/Users/wen/spot')
REC = R/'validation/axial_material/root64_epoch_recovery_20261011'
ART = R/'validation/artifacts'
BASE = Path(__file__).absolute().parent
CORE = REC/'full370_unreduced_eigen_reference_source_v2'
V6 = REC/'one_actual_track_H150_NZ48_full370_component_source_v1_20261014/v6'
FINITE = REC/'current_eight_fuel_finite18_SCAT_producer_source_v1_20261015'
FINITE_ENTRY = FINITE/'v4'
FINITE_OUT = ART/'axial-material-current-eight-fuel-finite18-SCAT-producer-20261015-v1'
OUT = ART/'axial-material-current-full370-real-operator-control-20261015-v1'
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
    q=Path(p['path']); s=q.lstat()
    require(q.is_absolute() and '..' not in q.parts and stat.S_ISREG(s.st_mode)
        and s.st_nlink==1 and not any(x.is_symlink() for x in (q,*q.parents))
        and identity(s)==p['identity'] and s.st_size==p['size_bytes'], 'exact current ordinary7 '+str(q))
    return q

def metadata_limit(path):
    # Match the exact upstream roles; Source/plans/tools/reviews keep8MiB.
    large={FINITE_OUT/'Root_actual_eight_fuel_finite18_SCAT_summary.json',
           FINITE_OUT/'inventories/ACTUAL_EIGHT_FUEL_FINITE18_SCAT_EVIDENCE.json'}
    return 64*2**20 if Path(path) in large else 8*2**20

def pin(path, maximum=None):
    q=Path(path); s=q.lstat()
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
    proof=plan['finite18_prerequisite_pins']; host=read(proof['host']); child=read(proof['child'])
    require(host['schema']=='ACTUAL_EIGHT_FUEL_FINITE18_SCAT_GUARDED_REPORT_V1'
        and host['status']=='ACTUAL_EIGHT_FUEL_64T_FINITE18_P0_WORDS_CLOSED0_ONLY'
        and host['failure'] is None and host.get('after_check_error') is None
        and host['final_report_resource_check_passed'] is True
        and len(host['records'])==1 and host['records'][0]['status']=='PASS'
        and host['original_caps']==CAPS, 'actual complete finite18 owning host pending')
    require(child['schema']=='ACTUAL_EIGHT_FUEL_FINITE18_SCAT_PRODUCER_COMPARISON_V1'
        and child['status']=='EIGHT_FUEL_64T_FINITE18_P0_RAW_WORDS_EQUAL'
        and child['eight_fuel_finite18_P0_producer_raw_words_replayed'] is True
        and all(child[k]==n for k,n in dict(compared_original_archives=16,
            compared_unique_nuclides=8,compared_temperature_records=64,
            compared_archive_temperature_records=128,compared_finite_dilution_nodes=1152,
            compared_original_leaf_records=3456).items()), 'complete finite18 producer evidence pending')
    require(contains(host,proof['child']), 'finite18 host must bind exact child report')
    closed0(read(proof['root_tools']),'actual_terminal_return',proof['host'],'report_pin')
    post=read(proof['post'])
    require(post['schema']==plan['finite18_post_schema'] and post['status']==plan['finite18_post_status']
        and post['status'].startswith('PASS') and post.get('failure') is None
        and all(contains(post,proof[k]) for k in ('host','child','root_tools')),
        'actual completed finite18 independent postverification pending')
    closed0(read(proof['post_tools']),'actual_review_return',proof['post'],'review_pin')
    for value in (host,child,post):
        for k in ('physics_qualified','full_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'):
            if k in value: require(value[k] is False, 'finite producer proof never inherited physics')
    return proof
