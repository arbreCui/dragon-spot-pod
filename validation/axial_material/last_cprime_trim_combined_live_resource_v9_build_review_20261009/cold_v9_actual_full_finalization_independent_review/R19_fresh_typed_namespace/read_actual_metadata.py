"""Finite, stdlib-only metadata reader; no business imports or execution."""
from pathlib import Path
import hashlib, json, math, os, stat, struct

OUT = Path('/private/tmp/axmat_v9_finalization_after_R19_typed_readback_20261009')
OLD = Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009')
R18 = Path('/private/tmp/axmat_v9_finalization_after_R18_fresh_readback_20261009')
FULL = Path('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009')
FIELDS = ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
PINS = []

def require(v, msg):
    if not v: raise ValueError(msg)

def identity(p):
    s = p.lstat()
    return [getattr(s, 'st_'+k) for k in FIELDS]

def read(p, sha=None):
    p = Path(p)
    require(p.is_absolute() and '..' not in p.parts, 'absolute path required')
    for q in (p, *p.parents):
        s = q.lstat()
        require(not stat.S_ISLNK(s.st_mode), 'alias source forbidden')
        require(stat.S_ISREG(s.st_mode) if q == p else stat.S_ISDIR(s.st_mode), 'source type')
    before = identity(p); b = p.read_bytes(); h = hashlib.sha256(b).hexdigest()
    require(identity(p) == before, 'identity changed during read')
    require(sha is None or h == sha, 'pin changed '+str(p))
    PINS.append({'path':str(p),'sha256':h,'bytes':len(b),'identity':before})
    return b

def pairs(items):
    d = {}
    for k, v in items:
        require(k not in d, 'duplicate JSON key'); d[k] = v
    return d

def finite(s):
    v = float(s); require(math.isfinite(v), 'nonfinite JSON'); return v

def parse(b):
    def reject(s): raise ValueError('nonfinite JSON '+s)
    return json.loads(b, object_pairs_hook=pairs, parse_float=finite, parse_constant=reject)

def load(p, sha=None): return parse(read(p, sha))

def typed(v):
    if v is None: return ['None']
    if type(v) is bool: return ['bool',v]
    if type(v) is int: return ['int',str(v)]
    if type(v) is float: return ['float64',struct.pack('!d',v).hex()]
    if type(v) is str: return ['str',v]
    if type(v) is list: return ['list',[typed(x) for x in v]]
    if type(v) is dict: return ['dict_ordered',[[typed(k),typed(x)] for k,x in v.items()]]
    raise TypeError(type(v))

def namespace(root):
    files={}; dirs=[]; links={}; root=Path(root)
    for folder, ds, ns in os.walk(root, followlinks=False):
        for name in ds+ns:
            p=Path(folder)/name; r=str(p.relative_to(root)); s=p.lstat()
            if stat.S_ISLNK(s.st_mode): links[r]=os.readlink(p)
            elif stat.S_ISREG(s.st_mode): files[r]=identity(p)
            elif stat.S_ISDIR(s.st_mode): dirs.append(r)
            else: raise ValueError('unsupported namespace '+str(p))
    return {'files':files,'directories':sorted(dirs),'symlinks':links}

def main():
    c=load(OLD/'finalization_config_ROOT_OBSERVED.json','8f5936308ad6ee031fc4328423966b9f0db069d27b5c1ce932f41a72d8a87174')
    report=load(OLD/'actual_finalization_readonly_REPORT.json','d02e1b4659d3f21559fface13562ecec3699ef455f1c80d84561827947f3fbbc')
    receipt=load(OLD/'actual_finalization_readonly_postterminal_tool_receipt.json','1e88eb9a6fdfad77634fe2cd2f5e63d436edbcc89d8dbb28b5ceb07026c2df2b')
    read(OLD/'audit_actual_finalization_readonly.py','d069335c743ee7c70f02674d58d37f41ca2b0b72a3c0c29c76b2eb32ace14617')
    prior=load(R18/'REPORT.json')
    prior_receipt=load(R18/'actual_fresh_readonly_tool_receipt.json')
    full=load(FULL/'REPORT.json','ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')
    full_receipt=load(FULL/'actual_readonly_tool_return.json','d3cc2a2f16ac2737ae5b339103d28ec84c8321fb90870d89b02f4f0de75c264a')
    for r in (receipt, prior_receipt):
        a=r['actual_tool']; require(type(a['exit_code']) is int and a['exit_code']==0 and a['closed'] is True,'actual readonly closed zero')
    require(c['future_cold_RUN_tool'] is None,'future cold None preserved')
    a=c['future_actual']['actual_tool_result']
    require(a=={'initial_chunk_id':'a76002','session_id':47736,'terminal_chunk_id':'195dc5','exit_code':0} and type(a['exit_code']) is int,'actual finalization exact four-key witness')
    require(report['actual_Root_tool']==a and receipt['Root_business_actual_tool']==a,'same actual finalization witness')
    require(c['future_actual']['Root_actual_closed_EXIT0_observed'] is True,'Root closed finalization observation')
    for p,h in c['known_files'].items(): read(p,h)
    w=Path(c['roots']['work']); t=Path(c['roots']['terminal'])
    old_bytes=read(w/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    cold_bytes=read(w/'prepared_cold.json','1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
    old=parse(old_bytes); cold=parse(cold_bytes)
    require(set(cold)==set(old)|{'own_child_supervision'} and 'own_child_supervision' not in old,'only supervision added')
    inverse=dict(cold); supervision=inverse.pop('own_child_supervision')
    require(typed(inverse)==typed(old),'whole typed order list and float64-bit inverse')
    require((json.dumps(inverse,indent=2,allow_nan=False)+'\n').encode()==old_bytes,'whole original serialization inverse')
    require(typed(supervision)==typed(c['expected_supervision']),'all descriptors exact original typed order')
    require(supervision==report['supervision']==full['supervision_all3_real_descriptors_exact'],'reports same descriptor values')
    for d in (supervision['binding'],supervision['controls']['seal'],supervision['controls']['terminal_evidence']): read(d['path'],d['sha256'])
    term=load(t/'finalization_terminal_return.json','ea33c7159edf82ce4ac1ba3682cc013c013431961a7ef7ad2e6f4dc0efd5bdb4')
    require(term['actual_tool_result']==a and term['actual_tool_terminal_return_observed'] is True and term['record_written_after_actual_terminal_return'] is True,'actual terminal witness')
    require(type(term['returncode']) is int and term['returncode']==0 and term['transport_started'] is False,'actual finalization code and no transport')
    stdout=load(term['full_stdout']['path'],term['full_stdout']['sha256'])
    stderr=read(term['full_stderr']['path'],term['full_stderr']['sha256'])
    require(len(stderr)==0 and typed(stdout)==typed(full['actual_entire_stdout_expected_whole_typed_order_floatbits_and_result_keys_exact']),'whole actual finalization stdout exact; stderr empty')
    namespaces={}
    for key,root in c['roots'].items():
        current=namespace(root); before=c['original_namespaces'][key]
        added={'prepared_cold.json'} if key=='work' else {'finalization.stdout','finalization.stderr','finalization_terminal_return.json'} if key=='terminal' else set()
        require(set(current['files'])==set(before['files'])|added,'namespace exact file set '+key)
        require(all(current['files'][p]==i for p,i in before['files'].items()),'old namespace every seven identities '+key)
        require(current['directories']==before['directories'] and current['symlinks']==before['symlinks'],'namespace exact dirs and links '+key)
        namespaces[key]={'regular_files':len(current['files']),'old_files_all_seven_fields_exact':True,'only_added':sorted(added),'directory_paths_exact':True,'symlink_targets_exact':True}
    absent=('AAA','archives','training','cold_source_complete_result.json','cold_source_failure.json','complete_cold_closeout_seal.json','cold_closeout_seal.json')
    require(all(not os.path.lexists(w/x) for x in absent),'native business outputs must be absent')
    require(not os.path.lexists(t/'terminal_return.json'),'no native Root terminal receipt')
    close=load('/Users/wen/spot/validation/storage_cleanup_nineteenth_20261009/Root_actual_storage_closeout.json')
    require(close['whole_existing_protected_set_preserved_after_report_save'] is True and close['business_executed'] is False and close['scientific_goal_still_active_not_qualified_by_storage'] is True,'R19 retained scope and no scientific credit')
    require(close['protected_counts']=={'files':160404,'links':669,'directories':7064},'R19 actual protected scope')
    for k in ('cleanup_actual_tool','whole_remainder_actual_postcheck_tool','Root_pre_retirement_joint_actual_tool'):
        q=close['actual_tools'][k];require(type(q['exit_code']) is int and q['exit_code']==0 and q['closed'] is True,'R19 actual terminal '+k)
    require(all(identity(Path(p['path']))==p['identity'] for p in PINS),'all fresh pin identities stable after complete reader')
    result={'schema':'AXMAT_V9_POST_R19_FINALIZATION_TYPED_READBACK_NO_NATIVE_V1','status':'PASS_CURRENT_ACTUAL_FINALIZATION_TYPED_BYTES_NAMESPACE_ONLY','scope':'FINITE_STDLIB_METADATA_READBACK_ONLY_NO_BUSINESS_IMPORT_OR_CALL',
      'actual_original_finalization_tool_result':a,'original_finalization_closed_observed_by_Root':True,'original_reader_actual_closed_tool':receipt['actual_tool'],
      'whole_original_typed_order_float64bits_inverse_exact':True,'whole_original_serialized_byte_inverse_exact':True,'only_own_child_supervision_added':True,
      'supervision_exact_actual_descriptors':supervision,'supervision_type':'dict2_with_nested_controls_dict2',
      'entire_actual_finalization_stdout':stdout,'stdout_type':'dict6','namespaces':namespaces,'absent_native_business_paths':list(absent),
      'fresh_after_R18_report_status':prior['status'],'R19_storage_closeout_status':close['status'],'R19_protected_counts':close['protected_counts'],
      'full_reader_nested_field_types':{k:type(full[k]).__name__ for k in ('supervision_all3_real_descriptors_exact','actual_entire_stdout_expected_whole_typed_order_floatbits_and_result_keys_exact','original_caps_complete_unchanged','reference_policy_boundary','inherited_controls2079_fullSHA_and7field_identities_preserved')},
      'reference_policy_boundary':full['reference_policy_boundary'],'original_caps_complete_unchanged':full['original_caps_complete_unchanged'],
      'fresh_read_pins':PINS,'project_written':False,'business_import_callback_API_executed':False,'native_executed_by_reader':False,'scientific_qualification':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
    p=OUT/'REPORT.json'
    with p.open('x') as f:json.dump(result,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
    b=p.read_bytes()
    print(json.dumps({'status':result['status'],'report':{'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},'namespace':namespaces,'read_pins':len(PINS),'native_executed':False},ensure_ascii=False))

if __name__=='__main__': main()
