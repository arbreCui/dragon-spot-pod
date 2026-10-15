"""UNREADY complete18-tree/6-context readback, explicit NEW A1/B2/A3 plan only.
No old global PLAN or validate_actual_producers is retained. Future Root only.
"""
from pathlib import Path
import contextlib,hashlib,json,os,stat,struct,sys
PARSER=Path('/Users/wen/spot/validation/axial_material/snapshot_control_preflight.py')
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
