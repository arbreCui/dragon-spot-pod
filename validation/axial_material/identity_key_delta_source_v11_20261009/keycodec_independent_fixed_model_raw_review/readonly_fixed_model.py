import hashlib,json,os,stat,struct
from collections import Counter
from pathlib import Path
B=Path('/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009')
R=B/'controls';CAP=536870912;NG=12;FEE=NG*4096
MESSAGE='SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.'
MUTATIONS=('unchanged_word','difference_word','stored_difference_word','base_word','input_length','load_length','ineligible_existing','corrupt_index_zero','corrupt_index_high','missing_anchor')
def check(v,msg):
    if not v:raise ValueError(msg)
def signed(x):
    x=x%(1<<64)
    return x-(1<<64) if x>=(1<<63) else x
def flip(x,mask):return signed((x%(1<<64))^mask)
D1=[signed(x) for x in (0,0x8000000000000000,0x7fffffffffffffff,0xffffffffffffffff,0x7ff8000000000123,0x7ff0000000000001)]
D2=[signed(x) for x in (0x7ff0000000000000,0xfff0000000000000,0xfff8000000000456,0x3ff0000000000000,0x8000000000000000,0)]
def change(k,n):return [flip(v,1) if i<n else v for i,v in enumerate(k)]
def encode(k,base):
    if base is None or len(k)!=len(base):return list(k),None
    positions=[i+1 for i,(x,y) in enumerate(zip(k,base)) if x!=y]
    if 12*len(positions)>=8*len(k):return list(k),None
    return [k[p-1] for p in positions],positions
class Ledger:
    def __init__(self):self.event=0;self.events=[];self.reset(False)
    def reset(self,enabled):
        self.enabled=enabled;self.allocated=enabled;self.entries={};self.owners={1:0,2:0};self.ready=set();self.live=FEE if enabled else 0;self.peak=self.live;self.hits=0
    def stats(self,name):
        self.event+=1
        meta=dict(kind='stats_snapshot',name=name,file=name+'.stats.bin',event=self.event)
        body=struct.pack('<10q',1,self.event,0,0,self.hits,self.live,self.peak,CAP,int(self.allocated),NG)
        self.events.append((meta,body))
    def snap(self,name,g,p,k,active,decode=True):
        self.event+=1
        e=self.entries.get((g,p));hasmode=any(i==g for i,j in self.entries)
        owner=self.owners[p] if hasmode else 0;base=self.entries.get((owner,p))
        payload=e['data'] if e else None;indices=e['positions'] if e else None
        anchor=base['data'] if base else None
        decoded=list(k) if e and decode else []
        if e and decode:
            check(self.decode(e,base)==list(k),'independent decoded positive key mismatch')
        a=[] if payload is None else payload;ix=[] if indices is None else indices;ref=[] if anchor is None else anchor
        h=[1,self.event,g,p,len(k),len(decoded),e['length'] if e else 0,len(a),len(ix),int(indices is not None),owner,len(a),len(ix),len(ref),int(hasmode),int(g in self.ready),int(active),0,0,self.hits,self.live,self.peak,CAP,NG,int(self.allocated),int(indices is not None),int(payload is not None),int(base is not None and base['positions'] is not None),int(anchor is not None),int(decode),0,0]
        body=struct.pack('<32q',*h)
        for seq,fmt in ((k,'q'),(a,'q'),(ix,'i'),(ref,'q'),(decoded,'q')):
            body+=struct.pack('<'+fmt*len(seq),*seq)
        meta=dict(kind='key_snapshot',name=name,file=name+'.bin',event=self.event,group=g,phase=p)
        self.events.append((meta,body))
    def decode(self,e,base):
        if e['data'] is None:raise ValueError('missing key payload')
        if e['positions'] is None:
            if len(e['data'])!=e['length']:raise ValueError('full size mismatch')
            return list(e['data'])
        if base is None or base['data'] is None or base['positions'] is not None or len(base['data'])!=e['length']:raise ValueError('missing same-size full anchor')
        pos=e['positions'];data=e['data']
        if len(pos)!=len(data) or pos!=sorted(set(pos)) or any(i<1 or i>e['length'] for i in pos):raise ValueError('noncanonical position')
        out=list(base['data'])
        for i,v in zip(pos,data):
            if out[i-1]==v:raise ValueError('stored value must differ from anchor')
            out[i-1]=v
        return out
    def guard(self,name,g,p,k,eligible=True):
        active=self.enabled and eligible
        if active:
            e=self.entries.get((g,p))
            if e is None:
                owner=self.owners[p];base=self.entries.get((owner,p))
                data,pos=encode(k,None if base is None else base['original'])
                self.entries[g,p]=dict(original=list(k),data=data,positions=pos,length=len(k))
                if owner==0:self.owners[p]=g
                self.live+=8*len(data)+(0 if pos is None else 4*len(pos));self.peak=max(self.peak,self.live)
            else:
                check(self.decode(e,self.entries.get((self.owners[p],p)))==list(k),'unexpected altered positive input')
                if p==2 and g in self.ready:self.hits+=1
        self.snap(name,g,p,k,active)
def positive():
    s=Ledger();s.reset(True);s.stats('threshold_begin')
    for p,k,owner,zero,single in ((1,D1,5,1,2),(2,D2,2,5,1)):
        s.guard('p%d_owner%d'%(p,owner),owner,p,k)
        s.guard('p%d_zero_delta'%p,zero,p,k)
        s.guard('p%d_single_delta'%p,single,p,change(k,1))
        s.guard('p%d_strict_12d36_lt_8n48'%p,3,p,change(k,3))
        s.guard('p%d_equal_12d48_eq_8n48_full'%p,4,p,change(k,4))
        s.guard('p%d_over_12d60_gt_8n48_full'%p,6,p,change(k,5))
        s.guard('p%d_different_size_full'%p,7,p,k+[17 if p==1 else 19])
    s.guard('p1_ineligible_fresh',11,1,D1,False);s.guard('p2_ineligible_fresh',11,2,D2,False)
    s.ready.add(5);s.guard('ready_phase1_no_hit',5,1,D1);s.guard('ready_phase2_first_hit',5,2,D2);s.guard('ready_phase2_second_hit',5,2,D2)
    s.ready.remove(5);s.guard('not_ready_phase2_no_hit',5,2,D2)
    s.reset(False);s.stats('threshold_clear');s.reset(True);s.stats('lifecycle_begin')
    s.guard('lifecycle_p1_owner9',9,1,D2);s.guard('lifecycle_p1_group3_zero',3,1,D2);s.guard('lifecycle_p2_owner3',3,2,D1);s.guard('lifecycle_p2_group9_delta',9,2,change(D1,1))
    s.ready.add(9);s.guard('lifecycle_ready_hit',9,2,change(D1,1));s.reset(False);s.stats('lifecycle_clear')
    s.reset(False);s.stats('disabled_begin');s.guard('disabled_phase1',1,1,D1);s.guard('disabled_phase2',1,2,D2);s.reset(False);s.stats('disabled_clear')
    return s
reasons=Counter()
def negative(mutation,p):
    s=Ledger();s.reset(True);s.stats('negative_begin')
    for name,g,phase,k in (('negative_p1_owner5',5,1,D1),('negative_p1_owner7_prerequisite',7,1,D1),('negative_p1_target2',2,1,change(D1,1)),('negative_p2_owner7',7,2,D2),('negative_p2_group5_zero',5,2,D2),('negative_p2_target2',2,2,change(D2,1))):s.guard(name,g,phase,k)
    inp=change(D1 if p==1 else D2,1);owner=5 if p==1 else 7;e=s.entries[2,p];base=s.entries[owner,p]
    operation='guard';nout=6
    if mutation=='unchanged_word':inp[1]=flip(inp[1],1)
    elif mutation=='difference_word':inp[0]=flip(inp[0],2)
    elif mutation=='stored_difference_word':e['data'][0]=flip(e['data'][0],2)
    elif mutation=='base_word':base['data'][1]=flip(base['data'][1],1)
    elif mutation=='input_length':inp.append(17)
    elif mutation=='load_length':operation='load';nout=7
    elif mutation=='ineligible_existing':pass
    elif mutation=='corrupt_index_zero':e['positions'][0]=0;operation='load'
    elif mutation=='corrupt_index_high':e['positions'][0]=7;operation='load'
    elif mutation=='missing_anchor':base['data']=None;operation='load'
    label='negative_%s_p%d'%(mutation,p);s.snap(label+'_attempt',2,p,inp,False,False)
    rejected=False
    try:
        decoded=s.decode(e,base)
        if operation=='load' and nout!=e['length']:rejected=True;reason='output length'
        elif operation=='guard' and mutation=='ineligible_existing':rejected=True;reason='ineligible existing key'
        elif operation=='guard' and decoded!=inp:rejected=True;reason='dense input identity unequal'
    except ValueError as err:rejected=True;reason=str(err)
    check(rejected,'independent model did not reject '+label);reasons[reason]+=1
    s.events.append((dict(kind='negative_expected',case=label,expected_XABORT=MESSAGE,expected_exit=23,operation=operation,output_words=nout),None))
    return s
observed={}
def signature(i):return (i.st_dev,i.st_ino,i.st_mode,i.st_nlink,i.st_size,i.st_mtime_ns,i.st_ctime_ns)
def read(p):
    check(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode),'ordinary endpoint '+str(p));before=signature(p.lstat());b=p.read_bytes();check(signature(p.lstat())==before and len(b)==before[4],'unchanged byte read');observed[str(p)]=(before,hashlib.sha256(b).hexdigest());return b
def parse(raw):
    def pairs(items):
        out={}
        for k,v in items:check(k not in out,'duplicate JSON member');out[k]=v
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
cases=[('keycodec_positive',positive(),0,None,None)]
for p in (1,2):
    for mutation in MUTATIONS:cases.append(('keycodec_negative_%s_p%d'%(mutation,p),negative(mutation,p),23,mutation,p))
binary_bytes=jsonl_bytes=xabort_bytes=0;records=Counter();details=[]
for name,s,code,mutation,p in cases:
    folder=R/name;namespace_before={x.name:signature(x.lstat()) for x in folder.iterdir()}
    check(all(stat.S_ISREG(x.lstat().st_mode) and not x.is_symlink() for x in folder.iterdir()),'ordinary case namespace')
    expected=[meta for meta,body in s.events];jraw=read(folder/'keycodec_manifest.jsonl');actual=[parse(line) for line in jraw.splitlines()]
    check(actual==expected,'complete independent manifest event mismatch '+name)
    canonical=b''.join((json.dumps(meta,separators=(',',':'))+'\n').encode() for meta in expected);check(jraw==canonical,'complete original manifest byte mismatch '+name)
    jsonl_bytes+=len(jraw);expected_names={'execute.log','execute.watchdog.json','keycodec_manifest.jsonl'}
    nbytes=0
    for meta,body in s.events:
        records[meta['kind']]+=1
        if body is None:continue
        expected_names.add(meta['file']);actual_raw=read(folder/meta['file']);check(actual_raw==body,'full independent header/input/stored/position/anchor/decode/EOF mismatch '+name+'/'+meta['file']);nbytes+=len(actual_raw)
    binary_bytes+=nbytes
    watch=parse(read(folder/'execute.watchdog.json'));command=[str(B/'runtime/keycodec_controls'),'positive'] if code==0 else [str(B/'runtime/keycodec_controls'),'negative',mutation,str(p)]
    check(watch['command']==command and type(watch['returncode'])is int and watch['returncode']==code,'exact actual command/rejection return')
    check(watch['rss_cap_mib']==512 and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'bounded actual archived watchdog scope')
    log=read(folder/'execute.log')
    if code==0:check(log==b'RAW_KEYCODEC_CONTROLS_COMPLETE\n','positive actual completion')
    else:
        expected_names.add('actual_xabort.txt');reject=read(folder/'actual_xabort.txt');check(reject==(MESSAGE+'\n').encode(),'exact actual XABORT bytes');check(log.count(('ACTUAL_XABORT='+MESSAGE).encode())==1 and b'STOP 23' in log,'exact actual negative log');xabort_bytes+=len(reject)
    check(set(namespace_before)==expected_names,'exact complete case namespace '+name)
    check(namespace_before=={x.name:signature(x.lstat()) for x in folder.iterdir()},'case namespace changed')
    details.append(dict(case=name,manifest_events=len(expected),raw_binary_bytes=nbytes,raw_manifest_bytes=len(jraw),actual_returncode=code))
for path,(sig,sha) in observed.items():check(signature(Path(path).lstat())==sig,'complete finite check endpoint changed')
check((binary_bytes,jsonl_bytes,xabort_bytes)==(70792,26930,1000),'fixed full primitive raw totals')
print(json.dumps(dict(status='PASS_INDEPENDENT_DENSE_INTEGER_FIXTURE_MODEL_AND_RAW_BYTES',controls=21,positive_key_records=27,positive_stats_records=6,negative_exact_expected_rejections=20,all_raw_key_records=records['key_snapshot'],all_raw_stats_records=records['stats_snapshot'],all_manifest_events=sum(len(s.events) for _,s,_,_,_ in cases),complete_input_stored_values_int32_positions_anchor_decoded_int64_header_stats_and_EOF_exact=True,independent_rejection_reasons=dict(reasons),raw_binary_bytes=binary_bytes,raw_manifest_jsonl_bytes=jsonl_bytes,raw_xabort_bytes=xabort_bytes,raw_total_bytes=binary_bytes+jsonl_bytes+xabort_bytes,ordinary_unique_files_read=len(observed),raw_checks_digest=hashlib.sha256(json.dumps(details,sort_keys=True,separators=(',',':')).encode()).hexdigest(),AAA_accuracy_qualified=False,native_RSS_verified=False,full_component_build_admission_claimed=False),sort_keys=True,indent=2))
