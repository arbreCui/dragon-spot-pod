"""Root-only future bounded context extraction; Source never executed by author.

Preserve every context word's original bytes, signed integer and REAL32 bits.
No material library, project API or observer is imported. A separately admitted
genuine host must bind this Source and every actual event pin; no CLI override
can supply admission. Old XSM snapshots need a separately admitted complete
native walker extension; this context reader does not substitute for that step.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import sys
import time

SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
ROOT_BOUND_OBSERVATION_REQUEST_SHA256 = None
ROOT_BOUND_GENUINE_HOST_PIN = None
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512,
    joint_archive_bytes=2*2**30, history_bytes=96*2**30,
    free_floor_bytes=8*2**30, threads=1, children_at_once=1, retries=0)


def require(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate context request key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def check_pin(p, budget):
    require(type(p) is dict and set(p)=={'path','sha256','size_bytes','identity'}, 'full context pin')
    require(type(p['path']) is str and Path(p['path']).is_absolute() and
        type(p['sha256']) is str and len(p['sha256'])==64 and
        all(c in '0123456789abcdef'for c in p['sha256']) and
        type(p['size_bytes']) is int and p['size_bytes']>=0 and
        type(p['identity']) is list and len(p['identity'])==7 and
        all(type(x) is int and x>=0 for x in p['identity']) and
        p['identity'][3]==1 and p['identity'][4]==p['size_bytes'], 'strict typed context pin')
    path = Path(p['path'])
    require(all(not q.is_symlink()for q in (path,*path.parents)), 'no context aliases')
    s=path.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s)==p['identity'], 'context identity differs')
    digest=hashlib.sha256();total=0
    with path.open('rb')as stream:
        require(identity(os.fstat(stream.fileno()))==p['identity'], 'context open identity')
        while True:
            budget();raw=stream.read(2**20)
            if not raw:break
            digest.update(raw);total+=len(raw)
        require(identity(os.fstat(stream.fileno()))==p['identity'], 'context EOF identity')
    require(total==p['size_bytes']and digest.hexdigest()==p['sha256']and
        identity(path.lstat())==p['identity'], 'context full EOF differs')


def extract_event(expected, out, budget):
    check_pin(expected,budget)
    with Path(expected['path']).open('rb') as stream:
        def take(size):
            require(type(size)is int and 0<=size<=2**20,'bounded context read')
            budget();raw=stream.read(size)
            require(len(raw)==size,'truncated actual context')
            return raw
        require(take(8)==b'AXOBSCTX','actual observation stream magic')
        version,event,libmix,label_size=struct.unpack('<4i',take(16))
        require(version==1 and event>=1 and libmix>=0 and 1<=label_size<=256,'actual context header')
        label=take(label_size).decode('ascii')
        dimensions={}
        def field(name,count,kind='INTEGER32',dimension=False):
            require(type(count)is int and count>=0,'original field count')
            begin=stream.tell();digest=hashlib.sha256()
            values=[] if dimension else None
            for start in range(0,count,4096):
                raw=take(4*min(4096,count-start));digest.update(raw)
                integers=struct.unpack('<'+'i'*(len(raw)//4),raw)
                if dimension:values.extend(integers)
                out.write(json.dumps(dict(event=event,libmix=libmix,label=label,
                    field=name,original_kind=kind,original_count=count,
                    element_begin0=start,full_original_bytes_hex=raw.hex(),
                    integer32_values=list(integers)if kind=='INTEGER32'else None,
                    REAL32_bits_hex=[raw[j:j+4].hex()for j in range(0,len(raw),4)]if kind=='REAL32'else None),
                    separators=(',',':'),allow_nan=False)+'\n')
            out.write(json.dumps(dict(event=event,label=label,field=name,
                span_begin=begin,span_end=stream.tell(),original_count=count,
                original_kind=kind,complete_original_SHA256=digest.hexdigest()),separators=(',',':'))+'\n')
            if dimension:
                require(count<=16,'dimension vector is explicitly finite')
                dimensions.update(zip(name.split(','),values))
                return values
        if label=='LIBMIX_BEFORE':
            field('NBMIX,NGROUP,NBISO,ITSTMP',4,dimension=True)
            n,g,i=(dimensions[k]for k in('NBMIX','NGROUP','NBISO'))
            require((n,g,i)==(8,370,62),'same complete material scope')
            field('ROOT_STATE40',40);field('MIX',i);field('DEN',i,'REAL32')
            field('TMPDAY',3,'REAL32');field('MACRO_LENGTH,MACRO_KIND',2,dimension=True)
            field('MASK',n);field('MASKL',g)
        elif label=='LIBDEN_OLD_CONTEXT':
            field('NBMIX,NGROUP,NBISO,NL,NDEL,NESP,NED,ITRANC,MAXNFI,NPART,ITSTMP,STERN,NFISSI',13,dimension=True)
            require(tuple(dimensions[k]for k in('NBMIX','NGROUP','NBISO','NL','NDEL','NESP','NED'))==
                (8,370,62,3,6,4,18),'full declared old context dimensions')
            field('TMPDAY',3,'REAL32');field('LSAME,MASKK,LALL,LDIFF',4)
            field('MASK',8);field('MASKL',370)
        elif label=='LIBDEN_BEFORE_FISSION_SLOT_MUTATION':
            field('NBMIX,MAXNFI,NFISS0,NFISSI',4,dimension=True)
            require(dimensions['NBMIX']==8 and 0<=dimensions['NFISS0']==dimensions['NFISSI']<=dimensions['MAXNFI']<=62,
                'original defined pre-mutation slot extent, no final map substituted')
            field('INDFIS_DEFINED_PRE_MUTATION',8*dimensions['NFISSI'])
        elif label=='TONDRV_AFTER_REAL_MAT_ELIMINATION':
            field('NREG,NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPROB,IGRMIN,IGRMAX',9,dimension=True)
            require((dimensions['NBISO'],dimensions['NBMIX'],dimensions['NGRO'])==(62,8,370)and
                dimensions['NREG']>=1,'actual tracking dimensions')
            field('MAT',dimensions['NREG']);field('MIX',62);field('LSHI',62);field('DEN',62,'REAL32')
        elif label=='TONDRV_ACTUAL_FINAL_LIBMIX_MASK':
            field('NBISO,NBMIX,NGRO,KSPH,ITRANZ,IPHASE,NRES2,ITSTMP',8,dimension=True)
            require((dimensions['NBISO'],dimensions['NBMIX'],dimensions['NGRO'])==(62,8,370), 'complete actual masks')
            field('LSHI',62);field('LSHI2',62);field('TMPDAY',3,'REAL32');field('MASK',8);field('MASKL',370)
        elif label=='TONSPH_BEFORE_ACTUAL_TONCMI':
            field('NBM,NBISO,NGRO,INRS,ITRANC,IGRMIN,IGRMAX',7,dimension=True)
            require((dimensions['NBM'],dimensions['NBISO'],dimensions['NGRO'])==(8,62,370), 'complete actual SPH dimensions')
            field('MASKI',62);field('SPH',8*370,'REAL32')
        elif label in ('LIBMIX_AFTER','TONDRV_FINAL_AFTER_SHIBA'):
            pass
        else:
            raise ValueError('unknown original event label, never skipped: '+label)
        require(stream.read(1)==b'','full context EOF; extra words not dropped')
    check_pin(expected,budget)
    return dict(event=event,libmix=libmix,label=label,input=expected,dimensions=dimensions,
        all_original_words_preserved=True,old_XSM_extracted_here=False)


def main():
    require(SOURCE_STATUS=='READY_ROOT_BOUND_SOURCE_ONLY' and
        type(ROOT_BOUND_OBSERVATION_REQUEST_SHA256)is str and
        type(ROOT_BOUND_GENUINE_HOST_PIN)is dict,'UNREADY refuses read/write before actual admission')
    parser=argparse.ArgumentParser();parser.add_argument('--request',required=True)
    parser.add_argument('--expected-parent-pid',required=True,type=int)
    args=parser.parse_args();started=time.monotonic()
    require(type(args.expected_parent_pid)is int and os.getppid()==args.expected_parent_pid,
        'actual separately admitted genuine host PID, never guessed at Source time')
    require(not sys.flags.optimize and sys.getprofile()is None and
        all(os.environ.get(k)=='1'for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS',
            'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')),
        'same unprofiled single-thread child environment')
    def budget():
        require(time.monotonic()-started<600,'original600 stage')
    request_path=Path(args.request)
    check_pin(ROOT_BOUND_GENUINE_HOST_PIN,budget)
    raw=request_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==ROOT_BOUND_OBSERVATION_REQUEST_SHA256,'actual bound request bytes')
    request=strict_json(raw)
    require(request['schema']=='ROOT_ACTUAL_OBSERVATION_CONTEXT_EXTRACTION_REQUEST_V1'and
        request['source_only']is True and request['original_caps']==CAPS and
        all(type(v)is int for v in request['original_caps'].values()),'same original actual extraction caps')
    require(request['Root_genuine_host_protection_verified']is True and
        request['future_old_context_qualification_sha256']is None,'separate genuine protection and unknown qualification')
    require(type(request['joint_archive_roots'])is list and len(request['joint_archive_roots'])==5,
        'complete actual HOCDE budget roots')
    roots=[Path(x)for x in request['joint_archive_roots']]
    require(all(x.is_absolute()for x in roots)and len(set(roots))==5 and
        not any(a.is_relative_to(b)for a in roots for b in roots if a!=b), 'full disjoint joint archive')
    last=[0.0]
    def budget():
        require(time.monotonic()-started<600,'original600 stage')
        now=time.monotonic()
        if now-last[0]<0.25:return
        last[0]=now;total=0
        for root in roots:
            if not root.exists():continue
            for p in root.rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'joint namespace symlink forbidden')
                if stat.S_ISREG(s.st_mode):total+=s.st_size
        unlinked={}
        for name in os.listdir('/dev/fd'):
            try:s=os.fstat(int(name))
            except (ValueError,OSError):continue
            if stat.S_ISREG(s.st_mode)and s.st_nlink==0:unlinked[(s.st_dev,s.st_ino)]=s.st_size
        require(total+sum(unlinked.values())<CAPS['joint_archive_bytes'],'all context/spool/SQL/journal bytes')
    output=Path(request['output_directory'])
    require(output.is_absolute()and not os.path.lexists(output),'fresh output zero retry')
    require(any(output.is_relative_to(root)for root in roots),'actual output counted in joint archive')
    output.mkdir();states={}
    for state in ('A','B'):
        pins=request['complete_state_event_pins'][state]
        require(type(pins)is list and len(pins)>0 and len({p['path']for p in pins})==len(pins),'all actual events, no selection')
        previous=0;events=[]
        with(output/(state+'_all_context_words.jsonl')).open('x',encoding='ascii')as out:
            for p in pins:
                event=extract_event(p,out,budget)
                require(event['event']==previous+1,'complete physical event order, no holes or renumbering')
                previous=event['event'];events.append(event)
        states[state]=events
    value=dict(schema='ACTUAL_FULL_OBSERVATION_CONTEXT_EXTRACTION_EVIDENCE_ONLY_V1',
        source_only=False,states=states,old_native_XSM_snapshots_still_require_complete_walker=True,
        historical_context_qualified=False,aggregate_construction_qualified=False,
        future_old_context_qualification_sha256=None,scientific_accuracy_qualified=False,
        genuine_supervisor_watch_verified_here=False)
    with(output/'ACTUAL_FULL_CONTEXT_EXTRACTION_REPORT.json').open('x')as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write('\n')
    check_pin(ROOT_BOUND_GENUINE_HOST_PIN,budget)
    require(hashlib.sha256(request_path.read_bytes()).hexdigest()==ROOT_BOUND_OBSERVATION_REQUEST_SHA256,
        'actual bound request unchanged')
    budget()
    raise SystemExit(2)


if __name__=='__main__':main()
