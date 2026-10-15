"""Pure-stdlib after-terminal reader. Does not compile or launch any child."""
import argparse
import ast
import hashlib
import json
import math
import re
import struct
import time
from pathlib import Path

OUT = Path('/Users/wen/spot/validation/artifacts/axial-material-rank1-cross-group-key-delta-codec-checks-v11-resource-scoped-v4-20261009')
SRC = Path('/Users/wen/spot/validation/artifacts/axial-material-rank1-cross-group-key-delta-codec-check-source-v11-20261009')
TMP = Path('/private/tmp/axmat_v11_actual_keycodec_independent_raw_review_20261009')
WRAPPER = Path('/Users/wen/spot/validation/axial_material/identity_key_delta_source_v11_20261009/run_bounded_codec_checks_resource_scoped_v4.py')
FAMILY = 'IDENTITY_KEY_DELTA_CODEC_CHECKS_V11_RESOURCE_SCOPED_V4'
KERNEL_SHA = '0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'
CONTROL_SHA = '3f59d94d49c049b206419b49c3a3ac437aa3d980548ab8fb27632ba4dfd472f7'
CAP = 536870912
GROUPS = 12
DESCRIPTORS = GROUPS*4096
MESSAGE = 'SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.'
CAPS = dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_cap_mib=512,archive_reserve_bytes=2*2**30,history_cap_bytes=96*2**30,min_free_bytes=8*2**30,threads=1,numeric_children_at_once=1,retries=0)
MUTATIONS = ['unchanged_word','difference_word','stored_difference_word','base_word','input_length','load_length','ineligible_existing','corrupt_index_zero','corrupt_index_high','missing_anchor']
tracked = {}

def ident(p):
    s=p.lstat()
    return dict(dev=s.st_dev,ino=s.st_ino,mode=s.st_mode,nlink=s.st_nlink,size=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)

def read(p):
    p=Path(p)
    if str(p) not in tracked:tracked[str(p)]=ident(p)
    b=p.read_bytes()
    assert ident(p)==tracked[str(p)], ('changed during read',str(p))
    return b

def sha(b):return hashlib.sha256(b).hexdigest()
def jread(p):return json.loads(read(p))
def pin(p,expected=None):
    b=read(p); h=sha(b)
    if expected is not None:assert h==expected,(str(p),h,expected)
    return dict(path=str(p),sha256=h,bytes=len(b),identity=tracked[str(p)])
def s64(n):return n if n < 2**63 else n-2**64
BASE1=[s64(n) for n in [0,0x8000000000000000,0x7fffffffffffffff,0xffffffffffffffff,0x7ff8000000000123,0x7ff0000000000001]]
BASE2=[s64(n) for n in [0x7ff0000000000000,0xfff0000000000000,0xfff8000000000456,0x3ff0000000000000,0x8000000000000000,0]]
def mutated(base,d):return [s64((n & (2**64-1)) ^ (1 if i<d else 0)) for i,n in enumerate(base)]

class Expected:
    """Independent full-input ledger; never derives expectation from actual encoding."""
    def __init__(self):self.clear();self.event=0;self.records=[]
    def clear(self):self.enabled=False;self.plan=False;self.entries={};self.owner={1:0,2:0};self.ready={};self.live=0;self.peak=0;self.hits=0
    def begin(self,enabled=True):
        self.clear();self.enabled=enabled;self.plan=enabled
        if enabled:self.live=self.peak=DESCRIPTORS
    def stats(self,name):
        self.event+=1
        self.records.append(dict(kind='stats_snapshot',name=name,file=name+'.stats.bin',event=self.event,header=[1,self.event,0,0,self.hits,self.live,self.peak,CAP,int(self.plan),GROUPS]))
    def acquire(self,ig,phase,key):
        if (ig,phase) in self.entries:
            assert self.entries[ig,phase]['full']==key
            if phase==2 and self.ready.get(ig,False):self.hits+=1
            return
        base=self.entries.get((self.owner[phase],phase))
        diffs=[] if base is None or len(base['full'])!=len(key) else [i for i,(a,b) in enumerate(zip(base['full'],key)) if a!=b]
        delta=base is not None and len(base['full'])==len(key) and 12*len(diffs)<8*len(key)
        bits=[key[i] for i in diffs] if delta else list(key)
        positions=[i+1 for i in diffs] if delta else None
        self.entries[ig,phase]=dict(full=list(key),bits=bits,positions=positions,count=len(key))
        if self.owner[phase]==0:self.owner[phase]=ig
        self.live+=12*len(diffs) if delta else 8*len(key)
        self.peak=max(self.peak,self.live)
    def snapshot(self,name,ig,phase,key,active,decode=True):
        self.event+=1
        hasmode=any(g==ig for g,p in self.entries)
        ent=self.entries.get((ig,phase));owner=self.owner[phase] if hasmode else 0
        base=self.entries.get((owner,phase))
        bits=ent['bits'] if ent else None
        pos=ent['positions'] if ent else None
        anchor=base['bits'] if base else None
        dec=list(ent['full']) if ent and decode else []
        h=[1,self.event,ig,phase,len(key),len(dec),ent['count'] if ent else 0,len(bits) if bits is not None else 0,len(pos) if pos is not None else 0,int(pos is not None),owner,len(bits) if bits is not None else 0,len(pos) if pos is not None else 0,len(anchor) if anchor is not None else 0,int(hasmode),int(self.ready.get(ig,False)),int(active),0,0,self.hits,self.live,self.peak,CAP,GROUPS,int(self.plan),int(pos is not None),int(bits is not None),int(base is not None and base['positions'] is not None),int(anchor is not None),int(decode),0,0]
        self.records.append(dict(kind='key_snapshot',name=name,file=name+'.bin',event=self.event,group=ig,phase=phase,header=h,input=list(key),payload=list(bits) if bits is not None else [],indices=list(pos) if pos is not None else [],anchor=list(anchor) if anchor is not None else [],decoded=dec))
    def guard(self,name,ig,phase,key,eligible=True):
        active=self.enabled and eligible
        if active:self.acquire(ig,phase,key)
        self.snapshot(name,ig,phase,key,active)

def positives():
    m=Expected();m.begin();m.stats('threshold_begin')
    for phase,base,owner in [(1,BASE1,5),(2,BASE2,2)]:
        m.guard(f'p{phase}_owner{owner}',owner,phase,base)
        m.guard(f'p{phase}_zero_delta',1 if phase==1 else 5,phase,base)
        m.guard(f'p{phase}_single_delta',2 if phase==1 else 1,phase,mutated(base,1))
        m.guard(f'p{phase}_strict_12d36_lt_8n48',3,phase,mutated(base,3))
        m.guard(f'p{phase}_equal_12d48_eq_8n48_full',4,phase,mutated(base,4))
        m.guard(f'p{phase}_over_12d60_gt_8n48_full',6,phase,mutated(base,5))
        m.guard(f'p{phase}_different_size_full',7,phase,base+[17 if phase==1 else 19])
    m.guard('p1_ineligible_fresh',11,1,BASE1,False);m.guard('p2_ineligible_fresh',11,2,BASE2,False)
    m.ready[5]=True
    m.guard('ready_phase1_no_hit',5,1,BASE1);m.guard('ready_phase2_first_hit',5,2,BASE2);m.guard('ready_phase2_second_hit',5,2,BASE2)
    m.ready[5]=False;m.guard('not_ready_phase2_no_hit',5,2,BASE2)
    m.clear();m.stats('threshold_clear');m.begin();m.stats('lifecycle_begin')
    m.guard('lifecycle_p1_owner9',9,1,BASE2);m.guard('lifecycle_p1_group3_zero',3,1,BASE2)
    m.guard('lifecycle_p2_owner3',3,2,BASE1);m.guard('lifecycle_p2_group9_delta',9,2,mutated(BASE1,1))
    m.ready[9]=True;m.guard('lifecycle_ready_hit',9,2,mutated(BASE1,1))
    m.clear();m.stats('lifecycle_clear');m.begin(False);m.stats('disabled_begin')
    m.guard('disabled_phase1',1,1,BASE1);m.guard('disabled_phase2',1,2,BASE2)
    m.clear();m.stats('disabled_clear')
    assert len(m.records)==33 and sum(x['kind']=='key_snapshot' for x in m.records)==27
    return m

def negatives(which,phase):
    m=Expected();m.begin();m.stats('negative_begin')
    for name,g,p,k in [('negative_p1_owner5',5,1,BASE1),('negative_p1_owner7_prerequisite',7,1,BASE1),('negative_p1_target2',2,1,mutated(BASE1,1)),('negative_p2_owner7',7,2,BASE2),('negative_p2_group5_zero',5,2,BASE2),('negative_p2_target2',2,2,mutated(BASE2,1))]:m.guard(name,g,p,k)
    attempted=mutated(BASE1 if phase==1 else BASE2,1);owner=5 if phase==1 else 7
    operation='guard';output_words=6
    if which=='unchanged_word':attempted[1]=s64((attempted[1] & (2**64-1)) ^ 1)
    elif which=='difference_word':attempted[0]=s64((attempted[0] & (2**64-1)) ^ 2)
    elif which=='stored_difference_word':m.entries[2,phase]['bits'][0]=s64((m.entries[2,phase]['bits'][0] & (2**64-1)) ^ 2)
    elif which=='base_word':m.entries[owner,phase]['bits'][1]=s64((m.entries[owner,phase]['bits'][1] & (2**64-1)) ^ 1)
    elif which=='input_length':attempted=attempted+[17]
    elif which=='load_length':operation='load';output_words=7
    elif which=='ineligible_existing':pass
    elif which=='corrupt_index_zero':m.entries[2,phase]['positions'][0]=0;operation='load'
    elif which=='corrupt_index_high':m.entries[2,phase]['positions'][0]=7;operation='load'
    elif which=='missing_anchor':m.entries[owner,phase]['bits']=None;operation='load'
    else:raise AssertionError(which)
    label=f'negative_{which}_p{phase}'
    m.snapshot(label+'_attempt',2,phase,attempted,False,False)
    m.records.append(dict(kind='negative_expected',case=label,expected_XABORT=MESSAGE,expected_exit=23,operation=operation,output_words=output_words))
    return m

def verify_records(folder,model):
    manifest=[json.loads(x) for x in read(folder/'keycodec_manifest.jsonl').splitlines()]
    expected=[];summaries=[]
    for e in model.records:
        expected.append({k:v for k,v in e.items() if k not in ['header','input','payload','indices','anchor','decoded']})
        if e['kind']=='negative_expected':continue
        b=read(folder/e['file']);h=e['header'];n=len(h)
        assert len(b)>=8*n,(str(folder),e['name'],'short header')
        actual=list(struct.unpack_from('<'+'q'*n,b));assert actual==h,(e['name'],'header',actual,h)
        offset=8*n
        if e['kind']=='key_snapshot':
            for field,fmt in [('input','q'),('payload','q'),('indices','i'),('anchor','q'),('decoded','q')]:
                count=len(e[field]);size=struct.calcsize(fmt)*count
                assert len(b)>=offset+size,(e['name'],field,'short payload')
                got=list(struct.unpack_from('<'+fmt*count,b,offset));assert got==e[field],(e['name'],field,got,e[field])
                offset+=size
        assert offset==len(b),(e['name'],'trailing bytes')
        summaries.append(dict(name=e['name'],event=e['event'],sha256=sha(b),bytes=len(b),header=h))
    assert manifest==expected,(str(folder),'manifest order/schema differs')
    assert {p.name for p in folder.glob('*.bin')}=={e['file'] for e in model.records if 'file' in e}
    return summaries

def verify_resource(r):
    assert r['artifact_budget_bytes']==96*2**30 and r['min_free_bytes']==8*2**30
    assert r['artifact_bytes']<=96*2**30 and r['disk_free_bytes']>=8*2**30
    assert r['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
    assert str(SRC) in r['declared_resource_roots'] and str(OUT) in r['declared_resource_roots']

def main():
    started=time.monotonic();a=argparse.ArgumentParser();a.add_argument('--root-observation',required=True);a.add_argument('--root-observation-sha256',required=True);a.add_argument('--root-stdout',required=True);a.add_argument('--root-stderr',required=True);args=a.parse_args()
    rootpin=pin(Path(args.root_observation),args.root_observation_sha256);root=jread(Path(args.root_observation))
    assert root['schema']=='AXMAT_ROOT_ACTUAL_CODEC_V4_TOOL_TERMINAL_RETURN_V1'
    assert root['classification']=='ACTUAL_HOST_EXIT_ZERO_CLOSED_EXTERNAL_BYTE_AUDIT_PENDING'
    actual_tool=root['actual_tool_terminal_return']
    assert type(actual_tool['exit_code']) is int and actual_tool['exit_code']==0
    assert actual_tool['chunk_id']=='060d2c' and actual_tool.get('session_id') is None
    assert root['actual_host_session_id']==34865 and root['terminal_observed_by_Root'] is True and root['session_closed'] is True and root['retry_count']==0
    for name in ['full_redirected_stdout','full_redirected_stderr','actual_driver_result','actual_stages','declaration','frozen_host_source','candidate_source']:
        v=root[name];assert pin(Path(v['path']),v['sha256'])['bytes']==v['bytes']
    assert root['full_redirected_stdout']['path']==args.root_stdout and root['full_redirected_stderr']['path']==args.root_stderr
    assert root['actual_driver_result']['path']==str(OUT/'driver_result.json') and root['actual_stages']['path']==str(OUT/FAMILY/'stages.json') and root['declaration']['path']==str(OUT/'declaration.json')
    assert root['frozen_host_source']['path']==str(WRAPPER) and root['candidate_source']['sha256']==KERNEL_SHA
    for name in ['native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:assert root[name] is False
    d=jread(OUT/'declaration.json');result=jread(OUT/'driver_result.json')
    assert d['caps']==CAPS and d['classification']=='PRIMITIVE_CODEC_CHECKS_ONLY_NOT_ORIGINAL45_OR_TRANSPORT'
    assert result['classification']=='ACTUAL_CODEC_OPERATIONS_CLOSED_EXTERNAL_BYTE_AUDIT_REQUIRED'
    assert result['positive_count']==1 and result['expected_negative_rejection_count']==20
    assert result['all_declared_operations_executed'] is True and result['actual_tail_check'] is True
    for k in ['original45_controls_completed','actual_full_FLU_entry_executed','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:assert result[k] is False
    assert result['actual_elapsed_seconds']<1800 and result['actual_archive_bytes']<=2*2**30
    verify_resource(d['resources_before']);verify_resource(result['actual_resources'])
    assert d['resources_before']['artifact_bytes']+2*2**30<=96*2**30
    assert d['resources_before']['disk_free_bytes']-2*2**30>=8*2**30
    sourcepins=[]
    for p,v in d['inputs'].items():sourcepins.append(pin(Path(p),v['sha256']));assert sourcepins[-1]['bytes']==v['bytes']
    pin(SRC/'SPOT1P64.f90',KERNEL_SHA);pin(SRC/'keycodec_controls.f90',CONTROL_SHA)
    sourcepins.append(pin(WRAPPER));ast.parse(read(WRAPPER))
    sourcepins.append(pin(Path(d['descriptor_source']['path']),d['descriptor_source']['sha256']))
    for v in d['bounded_runtime_helper'].values():sourcepins.append(pin(Path(v['path']),v['sha256']))
    for v in d['genuine_guard_sources']:sourcepins.append(pin(Path(v['path']),v['sha256']))
    original=jread(Path(d['original_build_declaration']['path']));sourcepins.append(pin(Path(d['original_build_declaration']['path']),d['original_build_declaration']['sha256']))
    commands=d['commands'];assert len(commands)==26
    assert [x[0] for x in commands]==['build/kernel','build/driver','build/link','build/descriptor','descriptor/execute','positive/execute']+[f'negative_{n}_p{p}/execute' for p in (1,2) for n in MUTATIONS]
    expected_codes=[0]*6+[23]*20;assert [x[2] for x in commands]==expected_codes
    assert commands[0][1][commands[0][1].index('-c')+1]==str(SRC/'SPOT1P64.f90')
    assert commands[1][1][commands[1][1].index('-c')+1]==str(SRC/'keycodec_controls.f90')
    assert '-ffp-contract=off' in commands[0][1] and '-ffp-contract=off' in commands[2][1]
    link=commands[2][1];oldlink=original['build_commands'][5]
    assert link[-7:-2]==oldlink[-7:-2]
    for p in link[-7:-2]:sourcepins.append(pin(Path(p),original['files'][p]))
    compiler=Path(commands[0][1][0]);sourcepins.append(pin(compiler))
    assert all(x[1][0]==str(compiler) for x in commands[:4])
    stages=jread(OUT/FAMILY/'stages.json')['stages'];assert len(stages)==26 and len(result['completed'])==26
    watches=[]
    for i,(label,command,expected_code) in enumerate(commands):
        wpath=OUT/(label+'.watchdog.json');w=jread(wpath);stage=stages[i];done=result['completed'][i]
        assert w['command']==command and type(w['returncode']) is int and w['returncode']==expected_code
        assert type(w['pid']) is int and w['pid']>0 and w['limit_failure'] is None
        assert 0<=w['sampled_peak_rss_mib']<512 and w['rss_cap_mib']==512
        assert 0<w['wall_cap_seconds']<=600 and 0<=w['elapsed_seconds']<w['wall_cap_seconds']
        assert w['own_child_only'] is True and w['liveness_group_cleanup'] is True
        assert stage['label']==label and stage['command']==command and stage['wall_cap_seconds']==600.0
        assert stage['status']==('PASS' if expected_code==0 else 'FAILED')
        assert done['label']==label and done['expected_returncode']==expected_code and done['expected_rejection']==(expected_code==23)
        assert done['actual_watchdog']['path']==str(wpath) and done['actual_watchdog']['sha256']==sha(read(wpath))
        log=read(OUT/(label+'.log'))
        if expected_code==0:assert stage['log_sha256']==sha(log) and done['actual_supervisor_error'] is None
        else:assert isinstance(done['actual_supervisor_error'],str) and done['actual_supervisor_error']
        for key in ['resource_before','resource_after']:
            if key in stage:verify_resource(stage[key])
        watches.append(dict(label=label,watch_sha256=sha(read(wpath)),returncode=expected_code,pid=w['pid'],sampled_peak_rss_mib=w['sampled_peak_rss_mib'],elapsed_seconds=w['elapsed_seconds'],log_sha256=sha(log)))
    descriptor=read(OUT/'descriptor/execute.log').decode('ascii')
    matches=re.fullmatch(r'mode_bytes=(\d+)\ngroup_bytes=(\d+)\n',descriptor)
    assert matches and sum(map(int,matches.groups()))<=4096
    positive=verify_records(OUT/'positive',positives())
    assert read(OUT/'positive/execute.log')==b'RAW_KEYCODEC_CONTROLS_COMPLETE\n'
    assert not (OUT/'positive/actual_xabort.txt').exists() and not (OUT/'positive/unexpected_return.txt').exists()
    negative=[]
    for phase in (1,2):
        for mutation in MUTATIONS:
            folder=OUT/f'negative_{mutation}_p{phase}'
            records=verify_records(folder,negatives(mutation,phase))
            assert read(folder/'actual_xabort.txt')==(MESSAGE+'\n').encode()
            log=read(folder/'execute.log');assert log.count(('ACTUAL_XABORT='+MESSAGE).encode())==1 and b'STOP 23' in log
            assert not (folder/'unexpected_return.txt').exists()
            negative.append(dict(mutation=mutation,phase=phase,raw_records=records,actual_xabort_sha256=sha(read(folder/'actual_xabort.txt')),log_sha256=sha(log)))
    stdout=read(Path(args.root_stdout));stderr=read(Path(args.root_stderr))
    assert stderr==b''
    assert stdout.decode().splitlines()==[x[0]+' CLOSED expected_exit='+str(x[2]) for x in commands]
    namespace={str(p.relative_to(OUT)):ident(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()}
    binarypins=[pin(p) for folder in [OUT/'build',OUT/'runtime'] for p in sorted(folder.iterdir()) if p.is_file()]
    for p,id0 in tracked.items():assert ident(Path(p))==id0,('changed after complete read',p)
    assert namespace=={str(p.relative_to(OUT)):ident(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()}
    report=dict(schema='axmat_v11_actual_codec_independent_full_raw_audit_v1',status='PASS_PRIMITIVE_CODEC_ONLY',root_actual_tool_pin=rootpin,root_raw_stdout_sha256=sha(stdout),root_raw_stderr_sha256=sha(stderr),declaration_sha256=sha(read(OUT/'declaration.json')),driver_result_sha256=sha(read(OUT/'driver_result.json')),source_pins=sourcepins,binary_pins=binarypins,actual_descriptor_bytes=dict(zip(['mode','group'],map(int,matches.groups()))),positive_key_count=27,positive_stats_count=6,positive_records=positive,negative_count=20,negative_records=negative,watches=watches,all_exact_EOF=True,independent_complete_expected_inputs_and_decoded_and_encoded_and_anchor_equal=True,all_full_fallback_thresholds_zero_delta_phase_owners_ready_hits_clear_checked=True,all_raw_and_source_identity_before_after_equal=True,output_namespace_regular_file_count=len(namespace),output_namespace_identity_digest=sha(json.dumps(namespace,sort_keys=True,separators=(',',':')).encode()),scope_limits=['These controls exercise 6/7-word keys, zero differences and disabled state. Zero-word/single-word keys and additional malformed representation cases are not newly executed by this suite.','Raw archives are test instrumentation; no real transport/production ndiff measurement or process RSS reduction is proved.','Actual watchdog readings are for the original supervised direct child; no missing wait4/kernel value is synthesized.','This is neither completion of original45 physics controls nor native/AAA/ABA qualification.'],original45_controls_completed=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,project_written=False,business_executed=False,elapsed_seconds=time.monotonic()-started)
    with (TMP/'REPORT.json').open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    with (TMP/'REPORT.txt').open('x') as f:f.write('V11 实际键编码原始输出独审通过，仅限 primitive codec。\n27键+6统计、20实际拒绝、26原守护阶段及完整EOF/源码/对象绑定均核验。\n完整原输入、完整解码、基准与差异值逐word一致；原4096B每组描述符及512/600/1800门不放宽。\n不代表原45物理控制或native/AAA/ABA通过，也未证明实际生产RSS下降。\n')
    print(json.dumps(dict(status=report['status'],report_sha256=sha(read(TMP/'REPORT.json')),tracked_files=len(tracked),positive_keys=27,negative_cases=20)))

if __name__=='__main__':main()
