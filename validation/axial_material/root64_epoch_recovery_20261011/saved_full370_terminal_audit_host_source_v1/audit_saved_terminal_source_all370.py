"""UNRUN saved-data audit of all 370 terminal axial P0/P1/P2 sources.

This does not solve transport or an eigenproblem, import project APIs, qualify
AAA, or fabricate the six unobserved NDIM3 transverse/mixed harmonics. The full
nine-harmonic reference is explicitly UNREADY. No parent Source is modified.
The independent streaming XSM reader is exact Source extracted from the pinned
previous complete P0 auditor; all new mathematics is independent below.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os
from pathlib import Path
import resource, signal, struct, sys, threading, time
WALL_SECONDS=600.0
RSS_BYTES=512*2**20
ARCHIVE_BYTES=64*2**20
NG,NUN,NZ,NA,NR,NL,NMAT,NF=370,1800,48,32,8,3,24,32
LL4=NL*NZ*NR
np=None
START=0.0
LAUNCH_ATTEMPTS=[]

def identity(s):
    return {k:getattr(s,k) for k in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}

def check_time(start):
    if time.monotonic()-start >= WALL_SECONDS:
        raise TimeoutError('original saved-state diagnostic wall limit exceeded')

def fresh_hash(path,start):
    """Full EOF SHA; no memo, each literal input freshly read before and after."""
    check_time(start)
    literal_before=identity(path.lstat());target_before=identity(path.stat())
    alias=os.readlink(path) if path.is_symlink() else None
    h=hashlib.sha256();count=0
    with path.open('rb') as stream:
        fd_before=identity(os.fstat(stream.fileno()))
        if fd_before!=target_before:raise ValueError('input path/fd identity mismatch')
        block=bytearray(2**20)
        while True:
            check_time(start);n=stream.readinto(block)
            if type(n) is not int or n<0 or n>len(block):raise ValueError('invalid input read count')
            if n==0:break
            h.update(memoryview(block)[:n]);count+=n
        fd_after=identity(os.fstat(stream.fileno()))
    literal_after=identity(path.lstat());target_after=identity(path.stat())
    alias_after=os.readlink(path) if path.is_symlink() else None
    if count!=fd_before['st_size'] or fd_before!=fd_after or target_before!=target_after or literal_before!=literal_after or alias!=alias_after:
        raise ValueError('input changed across full EOF hash')
    return {'path':str(path),'sha256':h.hexdigest(),'size_bytes':count,'literal_7id_before':literal_before,'literal_7id_after':literal_after,'target_7id_before':target_before,'target_7id_after':target_after,'fd_7id_before':fd_before,'fd_7id_after':fd_after,'literal_symlink_text':alias}

class XSM:
    """Independent read-only little-endian Ganlib directory/record reader."""
    def __init__(self,path,pinned,start):
        self.path=path;self.pinned=pinned;self.start=start;self.stream=path.open('rb');self.records={};self.bytes_read=0
        if identity(os.fstat(self.stream.fileno()))!=pinned['fd_7id_before']:raise ValueError('XSM owner changed before parsing')
        if self.read(0,3)[:4]!=b'$XSM':raise ValueError('wrong little-endian XSM format')
        self.root=self.directory(self.ints(2,1)[0])
    def read(self,offset,words):
        check_time(self.start)
        if type(offset) is not int or type(words) is not int or offset<0 or words<0 or (offset+words)*4>self.pinned['size_bytes']:
            raise ValueError('XSM out-of-file range')
        self.stream.seek(offset*4);raw=self.stream.read(words*4);self.bytes_read+=len(raw)
        if len(raw)!=words*4:raise ValueError('short XSM record')
        return raw
    def ints(self,offset,count):return struct.unpack(f'<{count}i',self.read(offset,count))
    def directory(self,start):
        result={};seen=set();offset=start
        while offset not in seen:
            seen.add(offset)
            magic,cap,count,following,_=struct.unpack_from('<4s4i',self.read(offset,8))
            if magic!=b'$$$$' or not 0<=count<=cap<=30:raise ValueError('invalid XSM directory')
            raw=self.read(offset+8,6*cap)
            for i in range(count):
                entry=tuple(struct.unpack_from('<i',raw,4*(k*cap+i))[0] for k in range(3))
                name=raw[12*(cap+i):12*(cap+i+1)].decode('ascii').rstrip(' \0')
                if not name or name in result:raise ValueError('invalid/duplicate XSM name')
                result[name]=entry
            offset=following
        if offset!=start:raise ValueError('invalid XSM extent cycle')
        return result
    def raw(self,directory,name,words,kind,owner):
        e=directory.get(name)
        if e is None or e[1:]!=(words,kind):raise ValueError('wrong record '+owner+'/'+name+': '+repr(e))
        raw=self.read(e[0],words)
        desc={'offset_words':e[0],'length_words':words,'type':kind,'sha256':hashlib.sha256(raw).hexdigest()}
        key=owner+'/'+name
        if key in self.records and self.records[key]!=desc:raise ValueError('record identity drift')
        self.records[key]=desc
        return raw
    def array(self,directory,name,dtype,count,owner):
        d=np.dtype(dtype);k={'i':1,'f':2 if d.itemsize==4 else 4}[d.kind]
        raw=self.raw(directory,name,count*(d.itemsize//4),k,owner)
        arr=np.frombuffer(raw,dtype=d).copy()
        if arr.size!=count or (d.kind=='f' and not np.isfinite(arr).all()):raise ValueError('invalid typed field '+owner+'/'+name)
        return arr
    def variable(self,directory,name,dtype,owner):
        e=directory.get(name)
        if e is None or e[1]<=0:raise ValueError('missing variable field '+name)
        d=np.dtype(dtype)
        if (e[1]*4)%d.itemsize:raise ValueError('invalid typed length')
        return self.array(directory,name,dtype,e[1]*4//d.itemsize,owner)
    def text(self,directory,name,owner):
        e=directory.get(name)
        if e is None or e[2]!=3 or e[1]<=0:raise ValueError('invalid character record '+name)
        return self.raw(directory,name,e[1],3,owner).decode('ascii').rstrip(' \0')
    def list(self,directory,name,count,owner):
        offsets=struct.unpack(f'<{count}i',self.raw(directory,name,count,10,owner))
        result=[]
        for offset in offsets:
            item=self.directory(offset)
            if '***HANDLE***' not in item:raise ValueError('missing list handle')
            self.records[f'{owner}/{name}/HANDLE/{len(result)+1}']={'directory_offset_words':offset,'directory':item}
            result.append(item['***HANDLE***'])
        return result
    def groups(self):
        entries=self.list(self.root,'GROUP',NG,'ROOT')
        if any(e[1:]!=(-1,0) for e in entries):raise ValueError('group must be a directory')
        return [self.directory(e[0]) for e in entries]
    def audit_group_payloads(self,groups):
        # Preserve every stored group field identity, including delayed-fission
        # records and higher moments not used by the P0 formula; omit nothing.
        for g,directory in enumerate(groups,1):
            for name,e in directory.items():
                if e[1]>0 and e[2] in (1,2,3,4):self.raw(directory,name,e[1],e[2],f'GROUP/{g}')
                else:raise ValueError('unexpected nested/unsupported group field '+name)
    def close(self):
        fd=identity(os.fstat(self.stream.fileno()));self.stream.close()
        if fd!=self.pinned['fd_7id_before'] or identity(self.path.stat())!=self.pinned['target_7id_before']:
            raise ValueError('XSM changed during parse')

def checkpoint(*_):
    check_time(START)
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=RSS_BYTES:
        raise MemoryError('own observed peak reaches unchanged 512 MiB cap')
    if threading.active_count()!=1:raise RuntimeError('single Python main thread required')


def no_launch(event,args):
    if event.startswith(('subprocess.','os.posix_spawn','os.spawn','os.fork','os.exec')):
        LAUNCH_ATTEMPTS.append(event);raise RuntimeError('saved-data audit forbids child launch')


def read_words(f,dtype,count):
    checkpoint();size=np.dtype(dtype).itemsize*count;raw=f.read(size)
    if len(raw)!=size:raise ValueError('incomplete actual raw capture payload')
    v=np.frombuffer(raw,dtype).copy()
    if not np.isfinite(v).all():raise ValueError('nonfinite actual capture values')
    return v


def unpack_field(path,context,dims):
    with path.open('rb') as f:
        if f.read(8)!=b'AXCFD001':raise ValueError('actual field magic differs')
        h=read_words(f,'<i4',8)
        stable_count=1+NR*3+NR+1+2*NZ+NL*NZ+2*NA*NL+NA*NA+1
        if h[:4].tolist()!=context[:4].tolist() or h[4:7].tolist()!=dims[8:].tolist() or h[7]!=stable_count:
            raise ValueError('field chronology/complete layout differs')
        raw=[read_words(f,dtype,int(n)) for dtype,n in zip(('<i4','<f4','<f8'),dims[8:])]
        if f.read(1):raise ValueError('extra field bytes')
    fields={}
    layouts=[ [('mat1d',(NZ,)),('mat',(NZ,NR)),('ncode',(2,)),('opposite',(NA,)),('white_row',(1,)),('ischm',(1,)),('lfixup',(1,))],
        [('vol1d',(NZ,)),('total',(NMAT+1,)),('sgas',(NMAT+1,NL)),('basis',(NR,1)),('vol2d',(NR,)),('zcode',(2,)),('mu',(NA,)),('w',(NA,)),('pl',(NL,NA))],
        [('white_perimeter',(1,)),('radial2d',(NR,3)),('weight',(NR,)),('mass',(1,1)),('total_projected',(1,1,NZ)),('radial_projected',(1,1,NZ)),('scat_projected',(1,1,NL,NZ)),('mn',(NA,NL)),('dn',(NL,NA)),('white_angle',(NA,NA)),('white_mode',(1,1)),('qext',(1,NL,NZ,NR)),('source_projected',(NL,NZ,1)),('cell',(NA,1,NZ)),('face',(NA,1,NZ+1)),('modal_flux',(NL,NZ,1)),('modal_current',(NZ+1,1)),('flux',(1,NL,NZ,NR)),('current',(NZ+1,NR)),('xnei',(NA,NR))] ]
    for values,layout in zip(raw,layouts):
        first=0
        for name,shape in layout:
            count=math.prod(shape);fields[name]=values[first:first+count].reshape(shape,order='F');first+=count
        if first!=values.size:raise ValueError('complete field unpack count differs')
    return fields


def raw_vector(path,magic,context):
    with path.open('rb') as f:
        if f.read(8)!=magic:raise ValueError('source/return magic differs')
        h=read_words(f,'<i4',5)
        if h[:4].tolist()!=context[:4].tolist() or h[4]!=NUN:raise ValueError('source/return chronology differs')
        v=read_words(f,'<f8',NUN)
        if f.read(1):raise ValueError('extra source/return bytes')
    return v


def summary(v):
    v=np.asarray(v);flat=v.ravel();index=int(np.argmax(abs(flat)))
    return dict(shape=list(v.shape),maximum_absolute=float(abs(flat[index])),signed_value_at_maximum=float(flat[index]),zero_based_index=[int(x) for x in np.unravel_index(index,v.shape)],minimum=float(v.min()),maximum=float(v.max()),nonzero_count=int(np.count_nonzero(v)))


def relative(defect,scale):
    zero=(scale==0)&(defect!=0)
    return np.divide(abs(defect),scale,out=np.zeros_like(defect),where=scale>0),zero


def save_array(out,name,v):
    checkpoint();v=np.ascontiguousarray(v)
    if not np.isfinite(v).all():raise ValueError('nonfinite derived array '+name)
    p=out/(name+'.bin');raw=v.tobytes()
    if sum(x.stat().st_size for x in out.iterdir() if x.is_file())+len(raw)>=ARCHIVE_BYTES:
        raise RuntimeError('complete saved-data output reaches unchanged 64 MiB cap')
    with p.open('xb') as f:f.write(raw)
    return dict(path=p.name,shape=list(v.shape),dtype=v.dtype.str,order='C',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def run(manifest,before,out):
    roles=manifest['roles'];capture=Path(roles['capture'])
    c=json.loads(Path(roles['capture_audit']).read_text())
    if not all(c[k] is True for k in ('complete_production_370_groups','original_map012_scientific_records_word_exact','original_terminal_passed','all_three_moments_and_currents_byte_exact','raw_fields_and_sources_unmodified')):
        raise ValueError('genuine complete successful original capture required')
    if c['chronological_inventory']['all_370_groups_last_context']!=[3,1]:raise ValueError('last-context differs')
    with Path(roles['capture_stream']).open('rb') as f:
        if f.read(8)!=b'AXCAP002':raise ValueError('only actual corrected rank1 capture schema accepted')
        dims=read_words(f,'<i4',11)
        if dims[:8].tolist()!=[NG,NUN,NZ,NA,NR,NL,NMAT,3]:raise ValueError('actual complete original dimensions differ')
        terminal=read_words(f,'<i4',9);terminal_real=read_words(f,'<f8',7)
        b2=read_words(f,'<f4',4);norm=read_words(f,'<f8',2);cache_stats=read_words(f,'<i8',6)
        if terminal[:7].tolist()!=[3,1,371,1,1,500,740] or terminal[8]!=NG or b2[3]!=0:
            raise ValueError('complete strict terminal and zero SIGS leakage correction required')
        if not all(terminal_real[i]<terminal_real[i+1] for i in (0,2,4)) or min(norm)<=0 or terminal_real[6]!=norm[0]:raise ValueError('native strict gates/normalization differ')
        contexts=[];published=np.empty((NG,NUN));published_source=np.empty_like(published)
        for g in range(NG):
            ctx=read_words(f,'<i4',9)
            if ctx[0]!=g+1 or ctx[2:4].tolist()!=[3,1] or ctx[1]!=ctx[4] or ctx[6]!=1 or ctx[8]!=1:raise ValueError('all370 contexts in original order required')
            contexts.append(ctx);published[g]=read_words(f,'<f8',NUN);published_source[g]=read_words(f,'<f8',NUN)
        if f.read(1):raise ValueError('extra publication stream bytes')
    factor=float(norm[0]/norm[1]);k=float(norm[0])
    readers={role:XSM(Path(roles[role]),before[roles[role]],START) for role in ('track','macro','closed_axial')}
    try:
        t,m,a=[readers[x] for x in ('track','macro','closed_axial')]
        ts=t.array(t.root,'STATE-VECTOR','<i4',40,'ROOT');ms=m.array(m.root,'STATE-VECTOR','<i4',40,'ROOT')
        if ts[[0,1,5,6,7,10,11]].tolist()!=[NR*NZ,NUN,NR,NZ,3,LL4,NR*(NZ+1)] or ms[:4].tolist()!=[NG,NMAT,NL,NF]:raise ValueError('actual track/macro shape differs')
        mat=t.array(t.root,'MATCOD','<i4',NR*NZ,'ROOT').reshape(NR,NZ)-1
        keys=t.array(t.root,'KEYFLX','<i4',NR*NZ,'ROOT')-1
        expected_keys=np.arange(LL4).reshape(NL,NZ,NR,order='F')[0].T.ravel()
        if not np.array_equal(keys,expected_keys) or np.any((mat<0)|(mat>=NMAT)):raise ValueError('explicit physical scalar key or material map differs')
        volume=t.array(t.root,'VOLUME','<f4',NR*NZ,'ROOT').reshape(NR,NZ).astype('f8')
        if np.any(volume<=0):raise ValueError('positive full physical volume required')
        if a.array(a.root,'SPOT-KEFF64','<f8',1,'ROOT').tobytes()!=norm[:1].tobytes():raise ValueError('native keff publication differs')
        handles=a.list(a.root,'FLUX64',NG,'ROOT')
        for g,h in enumerate(handles):
            if h[1:]!=(2*NUN,4) or a.read(h[0],h[1])!=published[g].tobytes():raise ValueError('complete actual FLUX64 publication differs')
        phi=np.stack([v[:LL4].reshape(NL,NZ,NR,order='F').transpose(0,2,1) for v in published])
        groups=m.groups();nus=np.empty((NG,NMAT,NF));chi=np.empty_like(nus)
        total=np.empty((NG,NMAT));selfraw=np.zeros((NG,NL,NMAT));sigw=np.empty_like(selfraw)
        off=np.zeros_like(phi);all_scatter=np.zeros_like(phi);abs_off=np.zeros_like(phi);coverage=[]
        for g,d in enumerate(groups):
            checkpoint();owner=f'GROUP/{g+1}'
            nus[g]=m.array(d,'NUSIGF','<f4',NF*NMAT,owner).reshape(NF,NMAT).T
            chi[g]=m.array(d,'CHI','<f4',NF*NMAT,owner).reshape(NF,NMAT).T
            total[g]=m.array(d,'NTOT0','<f4',NMAT,owner)
            for l in range(NL):
                suffix=f'{l:02d}';sigw[g,l]=m.array(d,'SIGW'+suffix,'<f4',NMAT,owner)
                nj=m.array(d,'NJJS'+suffix,'<i4',NMAT,owner);ij=m.array(d,'IJJS'+suffix,'<i4',NMAT,owner)-1;ip=m.array(d,'IPOS'+suffix,'<i4',NMAT,owner)-1
                entry=d.get('SCAT'+suffix)
                if entry is None or entry[1]==0:
                    if np.any(nj):raise ValueError('missing raw scatter with nonzero spans')
                    values=np.empty(0)
                else:values=m.variable(d,'SCAT'+suffix,'<f4',owner).astype('f8')
                addressed=np.zeros(len(values),dtype='<i4')
                for mix in range(NMAT):
                    n=int(nj[mix]);src=int(ij[mix])-np.arange(n);pos=int(ip[mix])+np.arange(n)
                    if not 0<=n<=NG or np.any((src<0)|(src>=NG)) or np.any((pos<0)|(pos>=len(values))):raise ValueError('original sparse transfer index outside full domain')
                    addressed[pos]+=1;weights=values[pos];cells=np.flatnonzero(mat.ravel()==mix)
                    same=np.flatnonzero(src==g)
                    if len(same)>1:raise ValueError('duplicate raw diagonal')
                    if len(same):selfraw[g,l,mix]=weights[int(same[0])]
                    if not len(cells):continue
                    field=phi[src,l].reshape(len(src),NR*NZ)[:,cells] if n else np.empty((0,len(cells)))
                    all_scatter[g,l].ravel()[cells]=np.sum(weights[:,None]*field,axis=0)
                    mask=src!=g
                    off[g,l].ravel()[cells]=np.sum(weights[mask,None]*field[mask],axis=0)
                    abs_off[g,l].ravel()[cells]=np.sum(abs(weights[mask,None]*field[mask]),axis=0)
                # Refuse malformed current payload; no dropping padding or duplicate mapping.
                if np.any(addressed!=1):raise ValueError('actual current sparse payload not mapped exactly once')
                coverage.append(dict(group=g+1,moment=l,stored_values=len(values),all_payload_once=True))
        if np.any(nus<0) or np.any(chi<0):raise ValueError('nonnegative actual fission coefficients required')
        production=np.zeros((NR,NZ,NF));production_abs=np.zeros_like(production)
        for g in range(NG):
            term=phi[g,0,:,:,None]*nus[g,mat];production+=term;production_abs+=abs(term)
        fission=np.zeros((NG,NR,NZ));fission_abs=np.zeros_like(fission)
        for g in range(NG):
            term=chi[g,mat]*production/k;fission[g]=np.sum(term,axis=2)
            fission_abs[g]=np.sum(abs(chi[g,mat])*production_abs/k,axis=2)
        qfinal=off.copy();qfinal[:,0]+=fission
        abs_final=abs_off.copy();abs_final[:,0]+=fission_abs
        # This screen bounds only this reconstruction from saved binary64 phi,
        # binary32 coefficients and final k. It cannot bound rounding in an
        # unobserved historical source phase, nor qualify a physical tolerance.
        nops=4*NG*NF+4*NG+8*NR+128;eps=np.finfo('f8').eps;gamma=nops*eps/(1-nops*eps)
        round_bound=gamma*abs_final/(1-gamma)+8*np.spacing(abs(qfinal))
        qsaved=np.empty_like(phi);dd_native=np.empty((NG,NA,NZ));dd_final=np.empty_like(dd_native);dd_scale=np.empty_like(dd_native)
        total_delta=np.empty((NG,NMAT));self_delta=np.empty((NG,NL,NMAT));native_source_consistency=[]
        for g,ctx in enumerate(contexts):
            checkpoint();folder=capture/'AAA'
            field=unpack_field(folder/f'angular_field_g{g+1:03d}.bin',ctx,dims)
            s2=raw_vector(folder/f'angular_source_g{g+1:03d}.bin',b'AXCS2001',ctx)
            returned=raw_vector(folder/f'angular_return_g{g+1:03d}.bin',b'AXCRT001',ctx)
            if (returned*factor).tobytes()!=published[g].tobytes() or (s2*factor).tobytes()!=published_source[g].tobytes():raise ValueError('original single global normalization not exact')
            if s2[:LL4].tobytes()!=field['qext'].ravel(order='F').tobytes() or returned[:LL4].tobytes()!=field['flux'].ravel(order='F').tobytes():raise ValueError('actual qext/return layout differs')
            if not np.array_equal(field['mat'].T-1,mat) or field['ncode'].tolist()!=[1,1] or np.any(field['zcode']!=0) or field['lfixup'][0]!=0:raise ValueError('original complete material/vacuum/NoFixup contract differs')
            qsaved[g]=(s2[:LL4]*factor).reshape(NL,NZ,NR,order='F').transpose(0,2,1)
            total_delta[g]=field['total'][1:].astype('f8')-total[g]
            self_delta[g]=field['sgas'][1:].T.astype('f8')-sigw[g]
            qproject=np.zeros((NL,NZ));qsproject=np.zeros_like(qproject)
            for z in range(NZ):
                for r in range(NR):
                    wb=float(field['weight'][r])*float(field['basis'][r,0])
                    qproject[:,z]+=wb*qfinal[g,:,r,z];qsproject[:,z]+=wb*qsaved[g,:,r,z]
            original_project=field['source_projected'][:,:,0]*factor
            project_delta=float(abs(original_project-qsproject).max())
            native_source_consistency.append(dict(group=g+1,maximum_absolute_saved_source_projection_difference=project_delta))
            cell=field['cell'][:,0]*factor;face=field['face'][:,0]*factor
            for z in range(NZ):
                C=np.eye(NA)*float(field['total_projected'][0,0,z])
                for l in range(NL):C-=field['mn'][:,l,None]*float(field['scat_projected'][0,0,l,z])*field['dn'][l,None,:]
                C+=field['mn'][:,0,None]*float(field['radial_projected'][0,0,z])*field['dn'][0,None,:]
                C+=float(field['white_mode'][0,0])*field['white_angle']
                h=float(field['vol1d'][z]);mu=field['mu'].astype('f8');mass=float(field['mass'][0,0])
                stream=mu*mass*(face[:,z+1]-face[:,z]);collision=h*(C@cell[:,z])
                native_rhs=h*(field['mn']@original_project[:,z]);final_rhs=h*(field['mn']@qproject[:,z])
                dd_native[g,:,z]=stream+collision-native_rhs;dd_final[g,:,z]=stream+collision-final_rhs
                dd_scale[g,:,z]=abs(mu)*mass*(abs(face[:,z+1])+abs(face[:,z]))+h*(abs(C)@abs(cell[:,z]))+abs(final_rhs)
        delta=qsaved-qfinal;source_scale=abs(qsaved)+abs_final
        source_ratio,source_zero=relative(delta,source_scale);dd_ratio,dd_zero=relative(dd_final,dd_scale)
        arrays=dict(actual_all370_publication_contexts=np.stack(contexts),final_flux_axial_P0_P1_P2=phi,raw_offgroup_source=off,raw_allgroup_scatter_source=all_scatter,all32_fission_source=fission,saved_terminal_source=qsaved,reconstructed_final_source=qfinal,saved_minus_final_source=delta,final_reconstruction_roundoff_screen=round_bound,source_relative_defect=source_ratio,source_zero_scale_nonzero=source_zero.astype('<i4'),native_DD_saved_source_defect=dd_native,native_DD_final_source_defect=dd_final,native_DD_final_source_scale=dd_scale,native_DD_final_source_relative=dd_ratio,native_DD_zero_scale_nonzero=dd_zero.astype('<i4'),actual_total_minus_NTOT0=total_delta,actual_SGAS_minus_SIGW=self_delta,raw_diagonal_minus_SIGW=selfraw-sigw,material_indices_1based=mat+1,physical_volume=volume)
        layout={name:save_array(out,name,v) for name,v in arrays.items()}
        by_moment=[]
        for l in range(NL):
            num=math.sqrt(float(np.sum(volume[None]*delta[:,l]**2)))
            scale=math.sqrt(float(np.sum(volume[None]*source_scale[:,l]**2)))
            by_moment.append(dict(axial_moment=l,complete_group_region_layer_delta=summary(delta[:,l]),weighted_L2_absolute=num,weighted_L2_scale=scale,relative_weighted_L2=None if scale==0 else num/scale,final_reconstruction_roundoff_screen=summary(round_bound[:,l]),maximum_positive_absolute_defect_minus_final_reconstruction_screen=float(np.maximum(abs(delta[:,l])-round_bound[:,l],0).max()),saved_historical_source_arithmetic_bound='UNKNOWN; saved-minus-final difference is not thereby a bug proof'))
        return dict(classification='COMPLETE_SAVED_TERMINAL_THREE_AXIAL_MOMENT_SOURCE_DIAGNOSTIC_ONLY_NDIM3_NINE_MOMENTS_UNREADY',groups=NG,regions=NR,axial_cells=NZ,shared_faces=NZ+1,actual_publication_header=dict(terminal_integer=terminal.tolist(),terminal_real=terminal_real.tolist(),B2=b2.tolist(),keff_fisour_operands=norm.tolist(),normalization_factor=factor,cache_stats=cache_stats.tolist()),source_comparison=by_moment,native_DD_final_source=summary(dd_ratio),native_DD_saved_source=summary(dd_native),actual_total_minus_NTOT0=summary(total_delta),actual_SGAS_minus_SIGW=summary(self_delta),raw_diagonal_minus_SIGW=summary(selfraw-sigw),native_source_projection_consistency=native_source_consistency,scatter_coverage=coverage,array_layout=layout,axes={'three_moment_arrays':['group','axial_Legendre_P0_P1_P2','radial_region','axial_cell'],'DD_arrays':['group','actual_axial_cosine','axial_cell'],'known_NDIM3_R_indices_0based':[0,2,6],'unknown_NDIM3_R_indices_0based':[1,3,4,5,7,8]},nine_moment_status='UNKNOWN_SIX_TRANSVERSE_OR_MIXED_MOMENTS_NOT_OBSERVED; no zero completion, no fitted/angular reconstruction',resource_scope='bounded pure saved data, canonical single-thread environment and one Python main thread, child launches rejected; native thread census external, no kernel hard RSS cap claim',physical_interpretation='Same captured native axial operator and declared raw final-state cross-group source. Source discrepancy includes native iterative source phase and arithmetic; actual-total/self differences are directly reported, not automatically a bug or a CE error cause. No complete reaction multiplicity/SPH history or actual fulltrack white closure.',roundoff_screen_operation_upper_count=nops,original_physics_thresholds_changed=False,no_clip_no_drop_no_local_renormalization=True,full_neutron_balance_qualified=False,full_eigen_reference_qualified=False,AAA_qualified=False,ABA_admitted=False)
    finally:
        for reader in readers.values():
            if not reader.stream.closed:reader.close()


def main():
    global START,np
    START=time.monotonic()
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest',required=True);parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--source-sha256',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args()
    if sys.platform!='darwin':raise ValueError('actual macOS own-RSS byte semantics required')
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
        if os.environ.get(name)!='1':raise ValueError('canonical one-thread environment required: '+name)
    if sys.version_info[:2]!=(3,12) or sys.flags.optimize!=0:raise ValueError('canonical unoptimized Python3.12 required')
    resource.setrlimit(resource.RLIMIT_CPU,(600,resource.getrlimit(resource.RLIMIT_CPU)[1]))
    sys.addaudithook(no_launch)
    signal.signal(signal.SIGALRM,checkpoint);signal.setitimer(signal.ITIMER_REAL,.1,.1)
    source=fresh_hash(Path(__file__).absolute(),START)
    manifest_pin=fresh_hash(Path(args.manifest),START)
    if source['sha256']!=args.source_sha256 or manifest_pin['sha256']!=args.manifest_sha256:raise ValueError('explicit Source/manifest pins differ')
    manifest=json.loads(Path(args.manifest).read_text())
    if manifest['schema']!='AAA_TERMINAL_SOURCE_READONLY_ACTUAL_INPUT_PLAN_V1' or manifest['candidate_executed'] is not False:raise ValueError('fixed Source-only plan required')
    if manifest['source']!={'path':str(Path(__file__).absolute()),'sha256':args.source_sha256}:raise ValueError('manifest must bind this exact Source and namespace')
    out=Path(args.out)
    if not out.is_absolute() or not str(out).startswith('/private/tmp/') or out.exists():raise ValueError('fresh exclusive TMP result directory required')
    out.mkdir();(out/'CLAIM.json').write_text(json.dumps(dict(actual_started_unix=time.time(),source=source,manifest=manifest_pin,declared_wall=600,observed_own_peak_limit=RSS_BYTES,threads=1,children=0,no_retry=True),indent=2)+'\n')
    try:
        import numpy as numpy
        np=numpy;checkpoint()
        before={}
        for p,wanted in manifest['inputs'].items():
            got=fresh_hash(Path(p),START)
            if got['sha256']!=wanted:raise ValueError('complete original input pin differs: '+p)
            before[p]=got
        result=run(manifest,before,out)
        after={}
        for p,wanted in manifest['inputs'].items():
            got=fresh_hash(Path(p),START)
            if got['sha256']!=wanted or got['literal_7id_before']!=before[p]['literal_7id_before'] or got['target_7id_before']!=before[p]['target_7id_before'] or got['literal_symlink_text']!=before[p]['literal_symlink_text']:raise ValueError('original input identity changed: '+p)
            after[p]=got
        if fresh_hash(Path(__file__).absolute(),START)['sha256']!=args.source_sha256 or fresh_hash(Path(args.manifest),START)['sha256']!=args.manifest_sha256:raise ValueError('Source/manifest changed during execution')
        checkpoint();result['actual_elapsed_seconds']=time.monotonic()-START;result['actual_own_peak_bytes_macOS']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;result['child_launch_attempts']=LAUNCH_ATTEMPTS
        (out/'INPUT_PINS_BEFORE_AFTER.json').write_text(json.dumps(dict(before=before,after=after),indent=2)+'\n')
        (out/'RESULT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        if sum(p.stat().st_size for p in out.iterdir() if p.is_file())>=ARCHIVE_BYTES:raise RuntimeError('complete final archive cap exceeded')
        checkpoint();print(json.dumps({k:v for k,v in result.items() if k in ('classification','actual_elapsed_seconds','actual_own_peak_bytes_macOS','nine_moment_status','AAA_qualified','full_eigen_reference_qualified')},indent=2,allow_nan=False))
    except BaseException as error:
        (out/'FAILED.json').write_text(json.dumps(dict(error=repr(error),actual_elapsed_seconds=time.monotonic()-START,actual_own_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,AAA_qualified=False,full_eigen_reference_qualified=False),indent=2)+'\n')
        raise
    finally:signal.setitimer(signal.ITIMER_REAL,0)

if __name__=='__main__':main()
