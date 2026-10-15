"""UNREADY independent new B engineering-context readback from the genuine A1/B2/A3 PACK.
Complete material blocks, geometry, basis and declarations; no GLOBAL/PROJECT stage.
"""
from pathlib import Path
import contextlib,hashlib,json,os,stat,struct,sys
PARSER=Path('/Users/wen/spot/validation/axial_material/snapshot_control_preflight.py')
sys.path.insert(0,str(PARSER.parent))
from snapshot_control_preflight import _XSM
MAX_READ_BYTES=1024*1024
READ_CHECK=None

def identity(st):
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]

class BoundedFDBytes:
    """Same-fd slices use pread; no mmap and no retained file-page mapping."""
    def __init__(self,fd,size):self.fd=fd;self.size=size;self.largest_read=0
    def __len__(self):return self.size
    def __getitem__(self,key):
        if READ_CHECK is None:raise RuntimeError('owning Root readback budget must be bound')
        READ_CHECK()
        if not isinstance(key,slice)or key.step not in (None,1):raise RuntimeError('only bounded byte slices')
        begin=0 if key.start is None else key.start;end=self.size if key.stop is None else key.stop
        if not 0<=begin<=end<=self.size or end-begin>MAX_READ_BYTES:
            raise RuntimeError('bounded same-fd XSM read extent')
        self.largest_read=max(self.largest_read,end-begin)
        result=os.pread(self.fd,end-begin,begin)
        if len(result)!=end-begin:raise RuntimeError('short same-fd XSM read')
        READ_CHECK()
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

def scalar(a,d,name,type_code):
    o,w,t=d[name]
    if t!=type_code:raise RuntimeError('scalar type '+name)
    if type_code==1 and w==1:return struct.unpack('<i',a.read(o,w))[0]
    if type_code==4 and w==2:return struct.unpack('<d',a.read(o,w))[0]
    raise RuntimeError('scalar length '+name)

def chars(a,d,name,expected):
    o,w,t=d[name]
    if t!=3 or a.read(o,w).decode('ascii').rstrip()!=expected:raise RuntimeError('exact character record '+name)


def verify_white_tracking_copy(original,marked):
    original,marked=Path(original),Path(marked)
    inherited=0
    with _open_xsm(original) as old,_open_xsm(marked) as new:
        active=set()
        def walk(previous,actual,root=False):
            nonlocal inherited
            additions={'AXMAT-WHITE','AXMAT-W-P'} if root else set()
            if set(actual)!=set(previous)|additions:
                raise ValueError('conditional receiver TRACK names changed')
            for name,p in previous.items():
                n=actual[name]
                if p[1:]!=n[1:]:raise ValueError('TRACK record kind/length changed: '+name)
                if p[2]==0:
                    pair=(p[0],n[0])
                    if pair in active:raise ValueError('cyclic TRACK object')
                    active.add(pair);walk(old.directory(p[0]),new.directory(n[0]));active.remove(pair)
                elif p[2]==10:
                    for a,b in zip(old.integers(p[0],p[1]),new.integers(n[0],n[1]),strict=True):
                        pair=(a,b)
                        if pair in active:raise ValueError('cyclic TRACK list')
                        active.add(pair);walk(old.directory(a),new.directory(b));active.remove(pair)
                else:
                    if old.read(p[0],p[1])!=new.read(n[0],n[1]):raise ValueError('TRACK inherited words changed: '+name)
                    inherited+=1
        walk(old.root,new.root,True)
        state=struct.unpack('<40i',old.record(old.root,'STATE-VECTOR',40,1))
        if (state[5],state[6],state[7],state[8],state[14],state[15])!=(8,48,3,1,32,3):
            raise ValueError('TRACK outside declared constant-diamond SN8 SCAT3 layout')
        if old.record(old.root,'NCODE',2,1)!=struct.pack('<2i',1,1) or old.record(old.root,'ZCODE',2,2)!=struct.pack('<2f',0,0):
            raise ValueError('original axial vacuum data differs')
        if new.record(new.root,'AXMAT-WHITE',4,1)!=struct.pack('<4i',1,1,8,3):
            raise ValueError('conditional white version/trace row differs')
        if new.record(new.root,'AXMAT-W-P',2,4)!=struct.pack('<d',6*.61776479):
            raise ValueError('conditional white physical perimeter differs')
    return dict(status='PASS_ONLY_TWO_WHITE_MARKERS_ADDED',inherited_records=inherited,new_records=2,
        physical_geometry_and_boundary_records_unchanged=True,model='conditional constant outer-sodium trace, uniform transverse azimuth',
        AAA_accuracy_qualified=False,ABA_admitted=False)


def read_record(a,d,name):
 o,w,t=d[name]
 if w<=0 or t not in range(1,7):raise RuntimeError('exact typed scientific leaf')
 return b''.join(a.read(o+j,min(262144,w-j))for j in range(0,w,262144))

def verify_macro_blocks(pack,macro):
 proof={'planes':3,'groups':370,'all_directory_leaf_records':0,'all_compared_raw_words':0}
 with _open_xsm(pack)as p,_open_xsm(macro)as m:
  sources=[node(p,p.root,['MICROLIB2',i,'MACROLIB'])for i in(1,2,3)];states=[struct.unpack('<40i',read_record(p,x,'STATE-VECTOR'))for x in sources];ng,nmix,nfis=states[0][0],states[0][1],states[0][3]
  if ng!=370 or nmix<=0 or any((x[0],x[1],x[2],x[3])!=(ng,nmix,states[0][2],nfis)for x in states):raise RuntimeError('SPOLIB full source states')
  def shallow(src,dst,root=False):
   if set(src[0])!=set(dst):raise RuntimeError('complete SPOLIB directory inventory')
   for name,e in src[0].items():
    o,w,t=e;de=dst[name]
    if root and name=='GROUP':
     if e[1:]!=(370,10)or de[1:]!=(370,10):raise RuntimeError('complete370 macro group list')
     for g in range(1,371):shallow([node(p,s,['GROUP',g])for s in sources],node(m,dst,['GROUP',g]))
     continue
    if t==0 and w==-1:
     if tree_digest(p,{name:e})!=tree_digest(m,{name:de}):raise RuntimeError('SPOLIB unchanged nested metadata tree')
     continue
    if t==10:
     if tree_digest(p,{name:e})!=tree_digest(m,{name:de}):raise RuntimeError('SPOLIB unchanged complete list')
     continue
    expected=read_record(p,src[0],name);outwords=w
    if t in(1,2):
     if name.startswith('SCAT')and t==2:
      expected=b'';outwords=0
      for s in src:
       if s[name][2]!=2:raise RuntimeError('original SPOOL SCAT type')
       expected+=read_record(p,s,name);outwords+=s[name][1]
     elif name.startswith('IPOS')and t==1 and w==nmix:
      values=[];offset=0;scatname='SCAT'+name[4:]
      for s in src:
       values.extend(x+offset if x>0 else x for x in struct.unpack('<'+str(nmix)+'i',read_record(p,s,name)));offset+=s.get(scatname,(None,0,None))[1]
      expected=struct.pack('<'+str(3*nmix)+'i',*values);outwords=3*nmix
     elif w==nmix:expected=b''.join(read_record(p,s,name)for s in src);outwords=3*nmix
     elif nfis>0 and w==nmix*nfis:
      raw=[read_record(p,s,name)for s in src];expected=b''.join(x[j*nmix*4:(j+1)*nmix*4]for j in range(nfis)for x in raw);outwords=3*w
    if root and name=='STATE-VECTOR':values=list(states[0]);values[1]=nmix*3;expected=struct.pack('<40i',*values);outwords=40
    if de[1:]!=(outwords,t)or read_record(m,dst,name)!=expected:raise RuntimeError('complete current3 SPOLIB block byte/type/extent mismatch: '+name)
    proof['all_directory_leaf_records']+=1;proof['all_compared_raw_words']+=outwords
  shallow(sources,m.root,True);proof['source_mixtures_per_plane']=nmix
 return proof

def verify_complete_three_plane_material_mapping(pack,track,macro_out):
 with _open_xsm(pack)as p,_open_xsm(track)as t,_open_xsm(macro_out)as m:
  radial=[node(p,p.root,['TRACK',i])for i in(1,2,3)];macro=[node(p,p.root,['MICROLIB2',i,'MACROLIB'])for i in(1,2,3)]
  state=[struct.unpack('<40i',read_record(p,s,'STATE-VECTOR'))for s in radial];mstate=[struct.unpack('<40i',read_record(p,s,'STATE-VECTOR'))for s in macro];nreg=state[0][0];nmix=max(x[3]for x in state)
  if nreg<=0 or nmix<=0 or any(x[0]!=nreg or x[3]!=nmix for x in state)or any(x[1]!=nmix for x in mstate):raise RuntimeError('complete TRACK/SPOLIB source mixture block dimensions must agree')
  outtrack=struct.unpack('<40i',read_record(t,t.root,'STATE-VECTOR'));outmacro=struct.unpack('<40i',read_record(m,m.root,'STATE-VECTOR'))
  if outtrack[3]!=3*nmix or outmacro[1]!=3*nmix:raise RuntimeError('actual TRACK and SPOLIB macro NMIX must both equal all three complete source blocks')
  planes=[struct.unpack('<'+str(nreg)+'i',read_record(p,s,'MATCOD'))for s in radial];floors=struct.unpack('<48i',read_record(t,t.root,'MAT1D'));actual=struct.unpack('<'+str(nreg*48)+'i',read_record(t,t.root,'MATCOD'));expected=[];middle=0
  if floors!=(1,)*16+(2,)*16+(3,)*16:raise RuntimeError('geometry MIX selects exact native snapshot slots1/2/3')
  for region in range(nreg):
   for floor in range(48):
    slot=floors[floor];original=planes[slot-1][region]
    if not 0<=original<=nmix:raise RuntimeError('original radial mixture index extent')
    value=0 if original==0 else original+(slot-1)*nmix;expected.append(value)
    if slot==2 and value!=0:
     if not nmix<value<=2*nmix:raise RuntimeError('middle16 floors must use exact B material block')
     middle+=1
  if tuple(expected)!=actual or middle==0:raise RuntimeError('all region/floor material IDs must implement original SPOT snapshot-block mapping, including nonempty B block')
  return dict(source_mixtures_per_plane=nmix,actual_TRACK_total_mixtures=outtrack[3],actual_SPOLIB_total_mixtures=outmacro[1],radial_regions=nreg,axial_cells=48,all_region_floor_material_ids_compared=len(actual),middle_B_block_nonvoid_ids_compared=middle,geometry_MIX_means_snapshot_slot=True,full_SPOT_original_MATCOD_mapping_equal=True)

def verify_engineering_outputs(root,plan):
 root=Path(root);proof={};counts={}
 with _open_xsm(root/'basis.xsm')as b:
  chars(b,b.root,'SIGNATURE','L_PIJ');r=b.root['POD-RANK-G'];s=b.root['POD-SIGMA-G']
  if r[1:]!=(370,1)or s[1:]!=(2220,4):raise RuntimeError('complete370 rank1/three-double spectra')
  ranks=struct.unpack('<370i',read_record(b,b.root,'POD-RANK-G'));sigmas=struct.unpack('<1110d',read_record(b,b.root,'POD-SIGMA-G'))
  for g in range(370):
   x=sigmas[3*g:3*g+3]
   if ranks[g]!=1 or not(x[0]>=x[1]>=x[2]>=0 and x[0]>0 and all(v==v and abs(v)<float('inf')for v in x)and x[0]>9.5367431640625e-7*x[0]):raise RuntimeError('unchanged independent rank precision floor')
  proof['common_basis_370_group_rank1_and_complete_three_spectra']=True
 for file,signature in(('axial_track.xsm','L_TRACK'),('axial_macro.xsm','L_MACROLIB'),('initial_system.xsm','L_PIJ'),('ax_current.xsm','L_FLUX')):
  with _open_xsm(root/file)as a:chars(a,a.root,'SIGNATURE',signature);counts[file]=tree_digest(a,a.root)
 with _open_xsm(root/'axial_track.xsm')as a:
  st=struct.unpack('<40i',read_record(a,a.root,'STATE-VECTOR'));mix=struct.unpack('<48i',read_record(a,a.root,'MAT1D'))
  if(st[5],st[6],st[7],st[8],st[14],st[15])!=(8,48,3,1,32,3)or mix!=(1,)*16+(2,)*16+(3,)*16:raise RuntimeError('exact48cell new A1/B2/A3 geometry mapping')
 proof['exact_new48cell_SN32_SCAT3_plane_MIX_mapping']=True
 with _open_xsm(root/'global_rcon.xsm')as a:
  chars(a,a.root,'SIGNATURE','L_RCONTRACT');chars(a,a.root,'CASE-NAME','PIN-ABA');chars(a,a.root,'FLU-OPTION','B0')
  if read_record(a,a.root,'EPS-TERMINAL')!=struct.pack('<3f',2.5e-7,5e-8,2.5e-8)or read_record(a,a.root,'FLU-CAPS')!=struct.pack('<2i',500,740)or read_record(a,a.root,'FLU-ACCE')!=struct.pack('<2i',3,3):raise RuntimeError('unchanged complete terminal declaration')
 proof['new_global_PIN_ABA_RCON_exact_declared_parameters']=True;proof['whole_output_logical_tree_digests']=counts
 proof['only_original_two_white_markers_added']=verify_white_tracking_copy(root/'axial_track_unmarked.xsm',root/'axial_track.xsm')
 proof['complete_current_PACK_three_material_macrolib_copy']=verify_macro_blocks(plan['PACK_full_pin']['path'],root/'axial_macro.xsm')
 proof['complete_current_three_plane_axial_material_block_mapping']=verify_complete_three_plane_material_mapping(plan['PACK_full_pin']['path'],root/'axial_track.xsm',root/'axial_macro.xsm')
 return proof
