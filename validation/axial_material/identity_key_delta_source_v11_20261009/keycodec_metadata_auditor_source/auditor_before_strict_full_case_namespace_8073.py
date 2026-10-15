"""Pure metadata RAW key-codec controls audit. No import-time I/O or child launch.

The caller owns fresh full component/build/seal/Root admission. This module
qualifies only the 21 actual primitive codec controls at the specified root.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import struct

SCHEMA = 'AXMAT_RANK1_CROSS_GROUP_IDENTITY_KEY_CODEC_CONTROLS_AUDIT_V1'
CAP = 536870912
GROUPS = 12
DESCRIPTORS = GROUPS*4096
MESSAGE = 'SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.'
MUTATIONS = ('unchanged_word','difference_word','stored_difference_word','base_word',
             'input_length','load_length','ineligible_existing','corrupt_index_zero',
             'corrupt_index_high','missing_anchor')
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
RAW_BINARY_BYTES = 70792
RAW_JSONL_BYTES = 26930
RAW_XABORT_BYTES = 1000
RAW_TOTAL_BYTES = 98722


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


def _identity(info):
    return (info.st_dev,info.st_ino,info.st_mode,info.st_nlink,
            info.st_size,info.st_mtime_ns,info.st_ctime_ns)


def _normal(path):
    p=Path(path)
    if not p.is_absolute() or '..' in p.parts:
        raise ValueError('ordinary absolute codec root required')
    for node in [*reversed(p.parents),p]:
        info=node.lstat()
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('codec path aliases forbidden: '+str(node))
        if node!=p and not stat.S_ISDIR(info.st_mode):
            raise ValueError('ordinary codec parent required')
    return p


def _json(raw):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate codec JSON key')
            d[k]=v
        return d
    def constant(value):raise ValueError('nonfinite codec JSON constant: '+value)
    return json.loads(raw,object_pairs_hook=unique,parse_constant=constant)


def _verify_records(folder,model,read):
    manifest=[_json(x) for x in read(folder/'keycodec_manifest.jsonl').splitlines()]
    expected=[];summaries=[];binary_bytes=0
    for event in model.records:
        expected.append({k:v for k,v in event.items()
                         if k not in ('header','input','payload','indices','anchor','decoded')})
        if event['kind']=='negative_expected':continue
        raw=read(folder/event['file']);h=event['header'];n=len(h)
        if len(raw)<8*n:raise ValueError('short raw codec header')
        actual=list(struct.unpack_from('<'+'q'*n,raw))
        if actual!=h:raise ValueError('complete raw codec header differs: '+event['name'])
        offset=8*n
        if event['kind']=='key_snapshot':
            for key,fmt in [('input','q'),('payload','q'),('indices','i'),('anchor','q'),('decoded','q')]:
                count=len(event[key]);amount=struct.calcsize(fmt)*count
                if len(raw)<offset+amount:raise ValueError('short complete raw codec '+key)
                actual=list(struct.unpack_from('<'+fmt*count,raw,offset))
                if actual!=event[key]:raise ValueError('complete raw codec '+key+' differs: '+event['name'])
                offset+=amount
        if offset!=len(raw):raise ValueError('raw codec exact EOF differs: '+event['name'])
        binary_bytes+=len(raw)
        summaries.append(dict(name=event['name'],event=event['event'],
                              bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),header=h))
    if manifest!=expected:raise ValueError('complete codec manifest event/schema/order differs')
    binary_names={x['file'] for x in model.records if 'file' in x}
    if {p.name for p in folder.glob('*.bin')}!=binary_names:
        raise ValueError('complete codec raw namespace differs')
    canonical_jsonl=b''.join((json.dumps(x,separators=(',',':'))+'\n').encode() for x in expected)
    if read(folder/'keycodec_manifest.jsonl')!=canonical_jsonl:
        raise ValueError('original codec JSONL bytes differ')
    return summaries,binary_bytes,len(canonical_jsonl)


def audit_keycodec_controls(controls_root):
    """Read all actual 21 controls; no old Root or old primitive PASS binding.

    Every read and accounting expectation is local to this call. The caller
    must separately verify its full component source/build/seal/Root contract.
    """
    if any(os.environ.get(k)!='1' for k in THREAD_KEYS):
        raise ValueError('original single-thread codec audit environment required')
    root=_normal(controls_root)
    if not stat.S_ISDIR(root.lstat().st_mode):
        raise ValueError('ordinary codec controls root required')
    observed={};pins={}
    def read(path):
        p=_normal(path);first=p.lstat()
        if not stat.S_ISREG(first.st_mode):raise ValueError('ordinary codec file required')
        signature=_identity(first)
        if str(p) in observed and observed[str(p)]!=signature:
            raise ValueError('codec endpoint changed between reads')
        fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
        try:
            if _identity(os.fstat(fd))!=signature:raise ValueError('codec open identity changed')
            chunks=[]
            while block:=os.read(fd,2**20):chunks.append(block)
            raw=b''.join(chunks)
            if len(raw)!=first.st_size or _identity(os.fstat(fd))!=signature:
                raise ValueError('codec endpoint changed during byte read')
        finally:os.close(fd)
        if _identity(_normal(p).lstat())!=signature:
            raise ValueError('codec pathname changed after byte read')
        observed[str(p)]=signature
        pins[str(p)]=dict(sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),
                         identity=list(signature))
        return raw
    cases=[('keycodec_positive',positives(),0)]
    cases.extend((f'keycodec_negative_{which}_p{phase}',negatives(which,phase),23)
                 for phase in (1,2) for which in MUTATIONS)
    executable=str(root.parent/'runtime/keycodec_controls')
    details=[];total_binary=0;total_jsonl=0;total_xabort=0
    for name,model,expected_code in cases:
        folder=_normal(root/name)
        namespace_before={p.name:_identity(p.lstat()) for p in folder.iterdir()}
        command=[executable,'positive'] if expected_code==0 else [executable,'negative',name[len('keycodec_negative_'):-3],name[-1]]
        watch=_json(read(folder/'execute.watchdog.json'))
        if (watch['command']!=command or type(watch['returncode']) is not int
            or watch['returncode']!=expected_code or type(watch['pid']) is not int or watch['pid']<=0
            or watch['limit_failure'] is not None or watch['rss_cap_mib']!=512
            or not 0<=watch['sampled_peak_rss_mib']<512
            or not 0<watch['wall_cap_seconds']<=600
            or not 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']
            or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True):
            raise ValueError('actual codec original own-child cap/exit/command differs: '+name)
        log=read(folder/'execute.log')
        summaries,binary_bytes,jsonl_bytes=_verify_records(folder,model,read)
        total_binary+=binary_bytes;total_jsonl+=jsonl_bytes
        if os.path.lexists(folder/'unexpected_return.txt'):
            raise ValueError('codec unexpected return archive exists')
        if expected_code==0:
            if log!=b'RAW_KEYCODEC_CONTROLS_COMPLETE\n' or os.path.lexists(folder/'actual_xabort.txt'):
                raise ValueError('actual positive codec completion differs')
        else:
            rejection=read(folder/'actual_xabort.txt')
            if rejection!=(MESSAGE+'\n').encode() or log.count(('ACTUAL_XABORT='+MESSAGE).encode())!=1 or b'STOP 23' not in log:
                raise ValueError('actual negative codec rejection differs')
            total_xabort+=len(rejection)
        if namespace_before!={p.name:_identity(p.lstat()) for p in folder.iterdir()}:
            raise ValueError('codec control namespace changed during full read')
        details.append(dict(control=name,expected_returncode=expected_code,
                            actual_returncode=watch['returncode'],pid=watch['pid'],
                            sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
                            elapsed_seconds=watch['elapsed_seconds'],raw_records=summaries,
                            raw_binary_bytes=binary_bytes,raw_jsonl_bytes=jsonl_bytes,
                            original_negative_supervisor_status_not_promoted=True))
    if (total_binary,total_jsonl,total_xabort)!=(RAW_BINARY_BYTES,RAW_JSONL_BYTES,RAW_XABORT_BYTES):
        raise ValueError('exact complete21 raw byte forecast differs')
    for path,signature in observed.items():
        if _identity(_normal(path).lstat())!=signature:
            raise ValueError('complete codec identity changed after audit')
    return dict(schema=SCHEMA,actual_codec_controls_passed=True,
                standalone_control_count=21,positive_key_count=27,positive_stats_count=6,
                expected_negative_actual_rejection_count=20,
                complete_input_encoded_positions_anchor_decoded_wordwise_equal=True,
                canonical_strict_cost_fallback_zero_delta_two_phase_lifecycle_and_hits_verified=True,
                exact_EOF_verified=True,raw_binary_bytes=total_binary,
                raw_manifest_jsonl_bytes=total_jsonl,raw_xabort_bytes=total_xabort,
                raw_total_bytes=total_binary+total_jsonl+total_xabort,
                fresh_file_pins=pins,actual_control_details=details,
                all_fresh_seven_identity_before_after_equal=True,
                original45_controls_completion_claimed=False,
                full_component_build_admission_claimed=False,
                actual_full_FLU_entry_executed=False,native_RSS_verified=False,
                AAA_accuracy_qualified=False,ABA_admitted=False)
