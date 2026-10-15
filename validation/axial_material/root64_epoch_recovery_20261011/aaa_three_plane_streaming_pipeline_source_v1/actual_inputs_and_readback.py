"""Complete streaming data checks; no subprocess, Native, training or solver.

All physical inputs are fixed by the previously frozen exact absolute input plan.
Directories/lists/types and every leaf byte enter the canonical tree digest.
Readonly nested views must compare to independent source files before any release.
"""
from pathlib import Path
import contextlib
import hashlib
import json
import math
import os
import stat
import struct
import sys

R=Path('/Users/wen/spot')
REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
PLAN=REC/'aaa_three_plane_streaming_source_v1/PROTECTED_FORMAL_AND_PRODUCER_INPUTS.json'
PARSER=R/'validation/axial_material/snapshot_control_preflight.py'
sys.path.insert(0,str(PARSER.parent))
from snapshot_control_preflight import _XSM

MAX_READ_BYTES=1024*1024
CONTEXT_NAMES={'AX','AXTRACK','AXSYSTEM','AXMACRO','ARCHIVE','RCON'}

def identity(st):
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]

class BoundedFDBytes:
    """Same-fd slices use pread; no mmap and no retained file-page mapping."""
    def __init__(self,fd,size):self.fd=fd;self.size=size;self.largest_read=0
    def __len__(self):return self.size
    def __getitem__(self,key):
        if not isinstance(key,slice)or key.step not in (None,1):raise RuntimeError('only bounded byte slices')
        begin=0 if key.start is None else key.start;end=self.size if key.stop is None else key.stop
        if not 0<=begin<=end<=self.size or end-begin>MAX_READ_BYTES:
            raise RuntimeError('bounded same-fd XSM read extent')
        self.largest_read=max(self.largest_read,end-begin)
        result=os.pread(self.fd,end-begin,begin)
        if len(result)!=end-begin:raise RuntimeError('short same-fd XSM read')
        return result

@contextlib.contextmanager
def _open_xsm(path):
    path=Path(path);before=identity(path.lstat())
    if not stat.S_ISREG(before[2])or before[3]!=1 or before[4]<12:
        raise RuntimeError('regular non-symlink single-link XSM file required')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('opened XSM fd/path full7ID differs')
        yield _XSM(BoundedFDBytes(fd,before[4]))
    finally:
        try:
            if identity(os.fstat(fd))!=before or identity(path.lstat())!=before:
                raise RuntimeError('XSM same-fd/path full7ID changed during read-only traversal')
        finally:os.close(fd)

def full_pin(path):
    path=Path(path);before=identity(path.lstat())
    if not stat.S_ISREG(before[2])or before[3]!=1:raise RuntimeError('regular single-link complete EOF file')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC)
    try:
        if identity(os.fstat(fd))!=before:raise RuntimeError('full EOF opened fd/path differs')
        h=hashlib.sha256();offset=0
        while offset<before[4]:
            raw=os.pread(fd,min(MAX_READ_BYTES,before[4]-offset),offset)
            if not raw:raise RuntimeError('short complete EOF file')
            h.update(raw);offset+=len(raw)
        if identity(os.fstat(fd))!=before or identity(path.lstat())!=before:
            raise RuntimeError('complete EOF fd/path full7ID changed')
        return dict(path=str(path),sha256=h.hexdigest(),size_bytes=before[4],identity=before)
    finally:os.close(fd)

def node(a,d,path):
    for part in path:
        if isinstance(part,int):
            o,w,t=d
            if t!=10 or not 1<=part<=w:raise RuntimeError('list item extent/type')
            ptr=struct.unpack('<i',a.read(o+part-1,1))[0]
            h=a.directory(ptr)
            if set(h)!={'***HANDLE***'}:raise RuntimeError('complete XSM list handle')
            d=h['***HANDLE***']
        else:
            if isinstance(d,tuple):
                if d[1:]!=(-1,0):raise RuntimeError('directory extent/type')
                d=a.directory(d[0])
            d=d[part]
    if isinstance(d,tuple):
        if d[1:]!=(-1,0):raise RuntimeError('directory required')
        d=a.directory(d[0])
    return d

def tree_digest(a,d):
    h=hashlib.sha256();counts={'leaves':0,'bytes':0,'directories':0,'list_items':0}
    def directory(v,depth):
        if depth>64:raise RuntimeError('XSM hierarchy depth bound')
        counts['directories']+=1;h.update(b'D'+struct.pack('<I',len(v)))
        for k in sorted(v):
            kb=k.encode('ascii');h.update(struct.pack('<I',len(kb))+kb);entry(v[k],depth+1)
    def entry(e,depth):
        o,w,t=e;h.update(struct.pack('<ii',w,t))
        if t==0 and w==-1:directory(a.directory(o),depth)
        elif t==10:
            if w<=0:raise RuntimeError('nonpositive list extent')
            counts['list_items']+=w
            for begin in range(0,w,4096):
                for ptr in struct.unpack('<'+str(min(4096,w-begin))+'i',a.read(o+begin,min(4096,w-begin))):
                    wrapper=a.directory(ptr)
                    if not wrapper:h.update(b'EMPTY');continue
                    if set(wrapper)!={'***HANDLE***'}:raise RuntimeError('XSM list wrapper')
                    entry(wrapper['***HANDLE***'],depth+1)
        else:
            if w<=0 or t not in range(1,7):raise RuntimeError('XSM scalar extent/type')
            counts['leaves']+=1;counts['bytes']+=4*w
            # Bound memory independently of the largest future scalar record.
            for begin in range(0,w,262144):h.update(a.read(o+begin,min(262144,w-begin)))
        if counts['leaves']+counts['directories']+counts['list_items']>2000000:
            raise RuntimeError('complete tree traversal node bound')
    directory(d,0)
    return dict(sha256=h.hexdigest(),**counts)

def exact_tree(a,da,b,db):
    left=tree_digest(a,da);right=tree_digest(b,db)
    if left!=right:raise RuntimeError('independent complete logical tree differs')
    return left

def validate_actual_producers(c,args):
    plan=json.loads(PLAN.read_text());fixed=[];reports=[]
    if plan['formal_configuration']['rank']!=1 or plan['formal_configuration']['sn']!=32 or \
       plan['formal_configuration']['cells_per_zone']!=16 or plan['training_slots']!=['A','B','A']:
        raise RuntimeError('formal independent rank1/48/SN32 training contract')
    c.verify_rows(plan['formal_inputs'])
    for i,row in enumerate(plan['producers'],1):
        d,p=c.load_json_exact(getattr(args,'a'+str(i)+'_summary'),getattr(args,'a'+str(i)+'_sha256'),getattr(args,'a'+str(i)+'_seven_id'))
        if p!=row['report'] or d['actual_output_pin']!=row['archive'] or d['actual_SALT_binary_track_pin']!=row['radial_binary_track']:
            raise RuntimeError('external actual producer report differs from frozen independent plane authority')
        c.same_pin(row['archive']['path'],row['archive']);c.same_pin(row['radial_binary_track']['path'],row['radial_binary_track'])
        terminal=d['actual_native_terminal']
        if terminal!=row['native_readback']:raise RuntimeError('actual complete producer terminal differs from frozen authority')
        if d['failure'] is not None or d['single_plane_native_producer_closed'] is not True or \
           len(d['records'])!=4 or any(x['status']!='PASS'for x in d['records']) or \
           (terminal['status'],terminal['plane'],terminal['epoch'],terminal['groups'],terminal['unknowns'],terminal['full_native_read_status'])!=('PASS',i,0,370,14,3) or \
           terminal['all370_ROOT_FLUX64_FLUX64_REF_bits_equal'] is not True or \
           terminal['full_source64_type4_finite_and_exact_mirror'] is not True or \
           terminal['strict_terminal_gate_passed'] is not True:
            raise RuntimeError('complete actual independent native producer scope')
        c.verify_rows(d['fixed_current_pins']);c.verify_rows(d['owned_runtime_pins']);c.verify_rows(d['output_pins'])
        if d['original_guard_MRO_unchanged'] is not True or d['original_guard_class']!='OwnRSSSerialExecutor' or \
           not 0<=d['SELF_peak_bytes']<512*2**20 or not 0<d['wall_seconds']<1800:
            raise RuntimeError('actual producer original host limits')
        fixed+=[p,row['archive'],row['radial_binary_track']]+d['fixed_current_pins']+d['owned_runtime_pins']+d['output_pins']
        reports.append(d)
    if len({tuple(x['archive']['identity'][:2])for x in plan['producers']})!=3:
        raise RuntimeError('three genuinely independent original files')
    fixed+=plan['formal_inputs']+[c.pin(PLAN),c.pin(PARSER)]
    return plan,fixed,reports

def packed_readback(pack,plan):
    fields=['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND']
    proof=[]
    with _open_xsm(pack)as a:
        if set(a.root)!=set(fields+['SIGNATURE','LISTDIM']):raise RuntimeError('packed root exact inventory')
        chars(a,a.root,'SIGNATURE','L_ARCHIVE')
        if scalar(a,a.root,'LISTDIM',1)!=3:raise RuntimeError('packed true three plane count')
        if any(a.root[name][1:]!=(3,10)for name in fields):raise RuntimeError('packed exactly three typed items in every full field')
        for p,row in enumerate(plan['producers'],1):
            with _open_xsm(Path(row['archive']['path']))as b:
                for name in fields:
                    digest=exact_tree(a,node(a,a.root,[name,p]),b,node(b,b.root,[name,1]))
                    proof.append(dict(plane=p,field=name,complete_tree=digest))
    return proof

def transfer_readback(project,global_file,pack,roots,plan):
    if len(roots)!=6 or set(roots)!=CONTEXT_NAMES:raise RuntimeError('exact six independent GLOBAL contexts')
    if full_pin(roots['ARCHIVE'])!=full_pin(pack):raise RuntimeError('ARCHIVE context is not the exact independent PACK complete pin')
    with contextlib.ExitStack()as stack:
        a=stack.enter_context(_open_xsm(project));g=stack.enter_context(_open_xsm(global_file));b=stack.enter_context(_open_xsm(pack))
        pg=node(a,a.root,['GLOBAL64']);ga=node(g,g.root,['ARCHIVE'])
        pga=node(a,a.root,['GLOBAL64','ARCHIVE'])
        proof={'complete_global':exact_tree(a,pg,g,g.root),'complete_archive':exact_tree(g,ga,b,b.root),
               'retained_complete_archive':exact_tree(a,pga,b,b.root),'independent_six_contexts':[dict(field='ARCHIVE',complete_tree=exact_tree(a,pga,b,b.root))],'original_three_planes':[]}
        for name,path in roots.items():
            if name=='ARCHIVE':continue
            c=stack.enter_context(_open_xsm(path))
            proof['independent_six_contexts'].append(dict(field=name,complete_tree=exact_tree(a,node(a,a.root,['GLOBAL64',name]),c,c.root)))
        for p,row in enumerate(plan['producers'],1):
            c=stack.enter_context(_open_xsm(Path(row['archive']['path'])))
            for name in ['TRACK','MICROLIB2','SYSTEM','FLUX','RCONTRACT','BOOT_BIND']:
                proof['original_three_planes'].append(dict(plane=p,field=name,
                  complete_tree=exact_tree(a,node(a,pga,[name,p]),c,node(c,c.root,[name,1]))))
    return proof

def scalar(a,d,name,type_code):
    o,w,t=d[name]
    if t!=type_code:raise RuntimeError('scalar type '+name)
    if type_code==1 and w==1:return struct.unpack('<i',a.read(o,w))[0]
    if type_code==4 and w==2:return struct.unpack('<d',a.read(o,w))[0]
    raise RuntimeError('scalar length '+name)

def chars(a,d,name,expected):
    o,w,t=d[name]
    if t!=3 or a.read(o,w).decode('ascii').rstrip()!=expected:raise RuntimeError('exact character record '+name)

def array(a,d,name,type_code,count):
    o,w,t=d[name]
    multiplier=2 if type_code==4 else 1
    if t!=type_code or w!=multiplier*count:raise RuntimeError('array type/extent '+name)
    return struct.unpack('<'+str(count)+('d'if type_code==4 else 'i'if type_code==1 else 'f'),a.read(o,w))

def final_readback(axpath,archive):
    with _open_xsm(axpath)as a,_open_xsm(archive)as b:
        chars(a,a.root,'SPOT-X-STATE','CLOSED')
        if scalar(a,a.root,'SPOT-X-EPOCH',1)!=0:raise RuntimeError('AX closed/e0')
        dims=array(a,a.root,'SPOT-X-DIMS',1,4)
        rank=array(a,a.root,'SPOT-X-RANK',1,370)
        if dims[:3]!=(1,370,3)or any(r!=1 for r in rank):raise RuntimeError('formal full370/three planes/rank1')
        k=scalar(a,a.root,'SPOT-X-KEFF',4);rho=scalar(a,a.root,'SPOT-X-RHO',4);norm=scalar(a,a.root,'SPOT-X-NORM',4)
        if any(not math.isfinite(v)or v<=0 for v in [k,rho,norm])or struct.pack('<d',rho)!=struct.pack('<d',1/k):
            raise RuntimeError('actual full native canonical eigenvalue/normalization')
        root=node(b,b.root,['SPOT-R64']);chars(b,root,'STATE','CLOSED')
        if scalar(b,root,'EPOCH',1)!=0 or scalar(b,root,'NPLANE',1)!=3 or \
           struct.pack('<d',scalar(b,root,'RHO',4))!=struct.pack('<d',rho):raise RuntimeError('archive full closed/e0 authority')
        chars(b,b.root,'SIGNATURE','L_ARCHIVE')
        if scalar(b,b.root,'LISTDIM',1)!=3 or b.root['FLUX'][1:]!=(3,10):raise RuntimeError('final archive exact three typed FLUX items')
        counts=[]
        for p in range(1,4):
            f=node(b,b.root,['FLUX',p]);auth=node(b,f,['SPOT-R64']);chars(b,auth,'STATE','SOLVED')
            if scalar(b,auth,'EPOCH',1)!=0 or struct.pack('<d',scalar(b,auth,'RHO',4))!=struct.pack('<d',rho):
                raise RuntimeError('actual solved plane/e0 authority')
            # Frozen BOOTC64_PUBLISH omits PLANE; B2IX only adds RHO/STATE/EPOCH.
            # Never manufacture an independent authority field from list position.
            plane_presence='PRESENT_TYPED_AND_MATCHES'if 'PLANE'in auth else 'ABSENT_NOT_EMITTED_BY_FROZEN_BOOT_SOURCE'
            if 'PLANE'in auth and scalar(b,auth,'PLANE',1)!=p:raise RuntimeError('present typed plane identity differs')
            system=node(b,b.root,['SYSTEM',p]);chars(b,system,'LINK.MACRO','MACRO0');chars(b,system,'LINK.TRACK','TRACK')
            if scalar(b,system,'SPOT-L1-SNAP',1)!=p or scalar(b,system,'SPOT-L1-RAW',1)!=1:
                raise RuntimeError('actual ASM PROJECT LK1D ordered plane/physical system binding')
            leak=array(b,system,'SPOT-LEAK1D',2,370)
            if any(not math.isfinite(v)for v in leak):raise RuntimeError('full370 actual system leakage finite')
            lib=node(b,b.root,['MICROLIB2',p]);macro=node(b,lib,['MACROLIB'])
            mstate=array(b,macro,'STATE-VECTOR',1,40);nmat=mstate[1]
            if mstate[0]!=370 or mstate[3]!=32 or nmat<=0 or macro['GROUP'][1:]!=(370,10):
                raise RuntimeError('actual full370/32 fission components complete macro')
            if system['GROUP'][1:]!=(370,10):raise RuntimeError('complete full370 system groups')
            for g in range(1,371):
                group=node(b,system,['GROUP',g]);physical=array(b,group,'SPOT-S0-PHYS',2,nmat+1)
                if any(not math.isfinite(v)for v in physical):raise RuntimeError('full actual physical S0 finite')
            state=array(b,f,'STATE-VECTOR',1,40);unknowns=state[1]
            if state[0]!=370 or unknowns!=14:raise RuntimeError('actual full non-scalar plane extent')
            row={'plane':p,'PLANE_record_status':plane_presence,'SYSTEM_SPOT_L1_SNAP':p,
                 'SYSTEM_SPOT_L1_RAW':1,'SYSTEM_full370_SPOT_S0_PHYS_checked':True,'fission_components':32,
                 'groups':370,'unknowns':unknowns,'flux_values':0,'source_values':0,'flux_non32':0,'source_non32':0}
            for n64,n32,label in [('FLUX','FLUX','flux'),('SOUR','SOUR','source')]:
                le=auth[n64];me=f[n32]
                if le[1:]!=(370,10)or me[1:]!=(370,10):raise RuntimeError('full370 typed lists')
                for g in range(1,371):
                    o,w,t=list_entry(b,le,g);o2,w2,t2=list_entry(b,me,g)
                    if (w,t,w2,t2)!=(unknowns*2,4,unknowns,2):raise RuntimeError('complete terminal list item type/extent')
                    vals=struct.unpack('<'+str(unknowns)+'d',b.read(o,w));mirror=b.read(o2,w2)
                    if any(not math.isfinite(v)for v in vals):raise RuntimeError('terminal finite actual native field')
                    rounded=b''.join(struct.pack('<f',v)for v in vals)
                    if rounded!=mirror:raise RuntimeError('every exact native-to32 mirror')
                    row[label+'_values']+=unknowns
                    row[label+'_non32']+=sum(struct.pack('<d',v)!=struct.pack('<d',struct.unpack('<f',rounded[4*i:4*i+4])[0])for i,v in enumerate(vals))
            counts.append(row)
        return dict(dimensions=dims,rank_values=370,rank1_all_groups=True,keff64=k,rho64=rho,norm64=norm,
                    planes=counts,complete_AX_tree=tree_digest(a,a.root),complete_ARCHIVE_tree=tree_digest(b,b.root),
                    angular_sixmoments_status='UNKNOWN_NOT_AVAILABLE_IN_SCALAR_NATIVE_READBACK',
                    independent_reference_physics_assessment=False)

def list_entry(a,e,index):
    o,w,t=e
    if t!=10 or not 1<=index<=w:raise RuntimeError('list bounds/type')
    ptr=struct.unpack('<i',a.read(o+index-1,1))[0]
    d=a.directory(ptr)
    if set(d)!={'***HANDLE***'}:raise RuntimeError('complete list entry')
    return d['***HANDLE***']
