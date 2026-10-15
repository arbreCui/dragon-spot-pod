"""Independent all-group saved-state source/reaction diagnostics, source draft.

No production solver, SPOT, Ganlib, old audit, or resource module is imported.
Root must source-admit/bind READY, pin this script, and use the genuine bounded
OwnRSS supervisor before one fresh execution. A complete diagnostic never grants
AAA, ABA, reaction-transfer equivalence, or full physical-balance qualification.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import struct
import sys
import time

SOURCE_STATUS = 'UNREADY'
ROOT = Path('/Users/wen/spot')
PROD = ROOT/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
OBS = ROOT/'validation/artifacts/axial-material-qualified-AAA-white-trace-refined-observables-20261005'
DEFAULT_OUTPUT = ROOT/'validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-20261010'
WALL_SECONDS = 60.0
RSS_LIMIT_MIB = 512.0
ARCHIVE_LIMIT_BYTES = 64*2**20
THREADS = 1
CHILDREN = 1
RETRIES = 0
NG, NM, NF, NR, NZ, NS, NU, LL4, LL5 = 370, 24, 32, 8, 48, 3, 1800, 1152, 392
NC = NR*NZ
CHANNELS = ('NFTOT','NG','N2N','N3N','N4N','NA','NP','N2A','NNP','ND','NT','NX')
INPUTS = {
    'track': (PROD/'AAA/bootstrap/initial_axial_track.xsm','b8302889d66f37947b3060f5caef2be43c7da5dfd6673daaa1ffb66fd81997d6'),
    'macro': (PROD/'AAA/bootstrap/initial_axial_macrolib.xsm','bca18875dbde9b5ae14f916f3df902ab071c173adff02c1b09ef647116282510'),
    'closed_axial': (PROD/'AAA/map012/closed_axial.xsm','fcb6e4144a05d943f5a54637c0124ec59498b7176ca077db295f0878ef60e01a'),
    'system': (PROD/'AAA/map012/candidate_system.xsm','994bacfea61f3145d0ba73f7889494215bca77fb5a341152fdd652e8f168c5e4'),
    'run_status': (PROD/'AAA/run_status.json','1acb16adc59f91e66599f74d11993d300bae73647dc870d148936935d199012f'),
    'final_seal': (PROD/'AAA/map012/result.json','f3716289ced3716fa89747ecb99b01757cd8d0f85ed202548f2fb68d5518606c'),
    'prepared': (PROD/'prepared.json','024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53'),
    'protocol': (OBS/'protocol.json','3f5c23d7d79c8d26162229d1cda51d3ee2218645222c8aec27b428280a93cadf'),
    'regions': (OBS/'observables.regions.csv','2fd4096bf31098cc8323fd7eae791a5c1bedb10bf01daf8a637a3c238b256327'),
    'faces': (OBS/'observables.faces.csv','02f9d68c41f2bd0be79f691094db862fa6cfaee371071c094e3ad1b0322057b9'),
    'summary': (OBS/'observables.summary.txt','7b430da7fc916ee54abefba63e4ad21e0c490826bbf8170e9d176995e9171612'),
}
np = None  # Imported normally only by admitted main(), not at source-review time.


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
            if set(item)!={'***HANDLE***'}:raise ValueError('list handle directory has unexpected members')
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


class Output:
    def __init__(self,path,start):
        if not path.is_absolute():raise ValueError('absolute fresh output required')
        path.mkdir(exist_ok=False);self.path=path;self.start=start;self.files={};self.bytes=0
    def bytes_file(self,name,raw):
        check_time(self.start)
        if '/' in name or name in self.files:raise ValueError('invalid output name')
        if self.bytes+len(raw)>ARCHIVE_LIMIT_BYTES:raise ValueError('64 MiB compact output cap exceeded')
        p=self.path/name
        with p.open('xb') as f:f.write(raw)
        self.files[name]={'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw)};self.bytes+=len(raw)
        return self.files[name]
    def json_file(self,name,value):
        raw=(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n').encode('utf8')
        return self.bytes_file(name,raw)
    def array(self,name,value,dtype='<f8'):
        arr=np.ascontiguousarray(value,dtype=dtype)
        raw=arr.tobytes(order='C');info=self.bytes_file(name+'.bin',raw)
        return {'file':name+'.bin','dtype':arr.dtype.str,'shape':list(arr.shape),'order':'C','axes':'documented in array key/name and layout.json','bytes':info['size_bytes'],'sha256':info['sha256']}


def finite_summary(value):
    v=np.asarray(value,dtype=np.float64)
    if not np.isfinite(v).all():raise ValueError('nonfinite diagnostic')
    flat=v.ravel(order='C');idx=int(np.argmax(np.abs(flat)))
    return {'shape':list(v.shape),'signed_sum':math.fsum(float(x) for x in flat),'absolute_sum':math.fsum(abs(float(x)) for x in flat),'minimum':float(np.min(v)),'maximum':float(np.max(v)),'max_abs':float(abs(flat[idx])),'max_abs_zero_based_index':list(np.unravel_index(idx,v.shape))}


def compare_export(path,keys,values,nonnegative,start):
    """Independent ordered sums with an operation-count roundoff screen only."""
    seen=set();worst={};eps=np.finfo(np.float64).eps
    # More operations than either native export or independent ordered replay;
    # this is an arithmetic identity bound, never an AAA accuracy threshold.
    op_count=NG*(NF+8)+128;gamma=(op_count*eps)/(1-op_count*eps)
    with path.open(newline='') as f:
        for row in csv.DictReader(f):
            check_time(start);key=tuple(int(row[k]) for k in keys)
            if key in seen or key not in values:raise ValueError('missing/duplicate/export observation key')
            seen.add(key)
            for field,expected in values[key].items():
                got=float(row[field])
                if not math.isfinite(got):raise ValueError('nonfinite saved export')
                # For signed current sums, callers supply sum-absolute scale.
                scale=nonnegative[key][field]
                bound=gamma*scale+8*math.ulp(got)+8*math.ulp(expected)
                delta=abs(got-expected)
                if delta>bound:raise ValueError('independent export replay disagrees: '+field)
                old=worst.get(field,{'max_abs_delta':-1})
                if delta>old['max_abs_delta']:worst[field]={'max_abs_delta':delta,'bound_at_worst':bound,'key':list(key)}
    if seen!=set(values):raise ValueError('incomplete exported observations')
    return {'rows':len(seen),'original_physics_accuracy_gate_changed':False,'arithmetic_operation_count':op_count,'gamma64':gamma,'fields':worst}


def evaluate(out,input_before,start):
    readers={role:XSM(INPUTS[role][0],input_before[role],start) for role in ('track','macro','closed_axial','system')}
    try:
        t,m,a,s=(readers[n] for n in ('track','macro','closed_axial','system'))
        ts=t.array(t.root,'STATE-VECTOR','<i4',40,'ROOT');ms=m.array(m.root,'STATE-VECTOR','<i4',40,'ROOT')
        fs=a.array(a.root,'STATE-VECTOR','<i4',40,'ROOT');ss=s.array(s.root,'STATE-VECTOR','<i4',40,'ROOT')
        if tuple(ts[[0,1,5,6,7,10,11]])!=(NC,NU,NR,NZ,NS,LL4,LL5):raise ValueError('original refined track dimensions differ')
        if tuple(ms[[0,1,3]])!=(NG,NM,NF) or tuple(fs[:2])!=(NG,NU) or tuple(ss[[7,8,9,10]])!=(NG,NU,NM,NS):raise ValueError('saved owners incompatible')
        if a.text(a.root,'SPOT-X-STATE','ROOT')!='CLOSED':raise ValueError('closed final AX required')
        epoch=a.array(a.root,'SPOT-X-EPOCH','<i4',1,'ROOT')
        if int(epoch[0])!=12:raise ValueError('wrong final epoch')
        key=t.array(t.root,'KEYFLX','<i4',NC,'ROOT')-1;mat=t.array(t.root,'MATCOD','<i4',NC,'ROOT')-1
        zone=t.array(t.root,'MAT1D','<i4',NZ,'ROOT')-1
        vol=t.array(t.root,'VOLUME','<f4',NC,'ROOT').astype(np.float64)
        area=t.array(t.root,'AREA2D','<f4',NR,'ROOT').astype(np.float64);height=t.array(t.root,'VOL1D','<f4',NZ,'ROOT').astype(np.float64)
        if len(np.unique(key))!=NC or np.any(key<0) or np.any(key>=LL4) or np.any(mat<0) or np.any(mat>=NM) or np.any(zone<0) or np.any(zone>=NS):raise ValueError('invalid original material/scalar/snapshot map')
        if np.any(vol<=0) or np.any(area<=0) or np.any(height<=0):raise ValueError('invalid original positive geometry')
        volume_expected=np.repeat(area,NZ)*np.tile(height,NR)
        volume_bound=0.5*np.spacing(vol.astype(np.float32)).astype(np.float64)
        if np.any(np.abs(vol-volume_expected)>volume_bound):raise ValueError('extruded volume exceeds original half-ULP geometry bound')
        energy=m.array(m.root,'ENERGY','<f4',NG+1,'ROOT')
        # Monotonic/units are reported with actual sequence; no eV/MeV conversion.
        de=np.diff(energy.astype(np.float64))
        energy_monotonic=bool(np.all(de<0) or np.all(de>0))
        if not energy_monotonic:raise ValueError('energy boundaries not strictly ordered')
        fission_index=m.array(m.root,'FISSIONINDEX','<i4',2*NF,'ROOT')
        k64=float(a.array(a.root,'SPOT-KEFF64','<f8',1,'ROOT')[0]);k32=float(a.array(a.root,'K-EFFECTIVE','<f4',1,'ROOT')[0])
        if k64<=0 or k32<=0 or struct.pack('<f',k64)!=struct.pack('<f',k32):raise ValueError('invalid original keff mirror')
        flux_entries=a.list(a.root,'FLUX64',NG,'ROOT');mirror_entries=a.list(a.root,'FLUX',NG,'ROOT');source_entries=a.list(a.root,'SOUR',NG,'ROOT')
        unknown=np.empty((NG,NU),dtype='<f8');saved_source=np.empty((NG,NU),dtype='<f4')
        for g,(ef,em,eq) in enumerate(zip(flux_entries,mirror_entries,source_entries)):
            if ef[1:]!=(2*NU,4) or em[1:]!=(NU,2) or eq[1:]!=(NU,2):raise ValueError('authoritative flux/source layout differs')
            raw=a.read(ef[0],ef[1]);v=np.frombuffer(raw,dtype='<f8')
            legacy=a.read(em[0],em[1]);qraw=a.read(eq[0],eq[1]);q=np.frombuffer(qraw,dtype='<f4')
            if not np.isfinite(v).all() or not np.isfinite(q).all() or v.astype('<f4').tobytes()!=legacy:raise ValueError('invalid R64 authority/REAL32 mirror/source')
            unknown[g]=v;saved_source[g]=q
            for label,e,b in [('FLUX64',ef,raw),('FLUX',em,legacy),('SOUR',eq,qraw)]:a.records[f'{label}/{g+1}']={'offset_words':e[0],'length_words':e[1],'type':e[2],'sha256':hashlib.sha256(b).hexdigest()}
        if 'SOUR64' in a.root or 'SPOT-R64' in a.root:raise ValueError('changed axial authoritative-source schema: review separately')
        phi=unknown[:,key];current=unknown[:,LL4:LL4+LL5].reshape(NG,NR,NZ+1)
        if np.any(phi<=0):raise ValueError('original nonpositive scalar flux gate')
        source_scalar=saved_source[:,key].astype(np.float64)
        groups=m.groups();sysgroups=s.groups();m.audit_group_payloads(groups);s.audit_group_payloads(sysgroups)
        nus=np.empty((NG,NF,NM));chi=np.empty_like(nus);tx=np.empty((NG,NM));self_corr=np.empty_like(tx);radial=np.empty((NG,NS,NR))
        total=np.empty_like(tx);tranc=np.empty_like(tx);channels={name:np.empty_like(tx) for name in CHANNELS}
        for g in range(NG):
            owner=f'GROUP/{g+1}';mg=groups[g];sg=sysgroups[g]
            nus[g]=m.array(mg,'NUSIGF','<f4',NF*NM,owner).reshape(NF,NM);chi[g]=m.array(mg,'CHI','<f4',NF*NM,owner).reshape(NF,NM)
            if np.any(nus[g]<0):raise ValueError('original negative NUSIGF gate')
            tx[g]=s.array(sg,'DRAGON-TXSC','<f4',NM+1,owner)[1:]
            sx=s.variable(sg,'DRAGON-S0XSC','<f4',owner)
            if sx.size%(NM+1) or sx.size<(NM+1):raise ValueError('invalid corrected selfscatter layout')
            self_corr[g]=sx.reshape(-1,NM+1)[0,1:]
            radial[g]=s.array(sg,'RADIAL-OP64','<f8',NR*NS,owner).reshape(NS,NR)
            total[g]=m.array(mg,'NTOT0','<f4',NM,owner);tranc[g]=m.array(mg,'TRANC','<f4',NM,owner)
            for name in CHANNELS:channels[name][g]=m.array(mg,name,'<f4',NM,owner)
        prod=np.zeros((NC,NF));nu_coeff=np.zeros((NG,NM));flux_integr=np.zeros(NC);rate_integr=np.zeros(NC)
        for g in range(NG):
            check_time(start);prod+=phi[g,:,None]*nus[g,:,mat].reshape(NC,NF)
            for f in range(NF):nu_coeff[g]+=nus[g,f]
            flux_integr+=vol*phi[g];rate_integr+=vol*phi[g]*nu_coeff[g,mat]
        qf=np.zeros((NG,NC))
        for f in range(NF):qf+=chi[:,f,mat]*prod[None,:,f]/k64
        qoff=np.zeros_like(qf);qall=np.zeros_like(qf);macro_self=np.zeros((NG,NM));transfer_out=np.zeros((NG,NM))
        scatter_coverage=[]
        for g in range(NG):
            check_time(start);mg=groups[g];owner=f'GROUP/{g+1}'
            nj=m.array(mg,'NJJS00','<i4',NM,owner);ij=m.array(mg,'IJJS00','<i4',NM,owner)-1;ip=m.array(mg,'IPOS00','<i4',NM,owner)-1
            scat=m.variable(mg,'SCAT00','<f4',owner).astype(np.float64)
            covered=np.zeros(len(scat),dtype=np.int32)
            for mix in range(NM):
                count=int(nj[mix]);first=int(ij[mix]);offset=int(ip[mix])
                if count<0 or count>NG:raise ValueError('invalid compressed scatter count')
                if count==0:continue  # Zero row is preserved, never silently excluded.
                src=first-np.arange(count);pos=offset+np.arange(count)
                if np.any(src<0) or np.any(src>=NG) or np.any(pos<0) or np.any(pos>=len(scat)):raise ValueError('compressed scatter map overflow')
                weights=scat[pos];covered[pos]+=1;np.add.at(transfer_out[:,mix],src,weights)
                same=np.flatnonzero(src==g)
                if len(same)>1:raise ValueError('duplicate compressed selfscatter')
                if len(same):macro_self[g,mix]=weights[int(same[0])]
                cells=np.flatnonzero(mat==mix)
                if len(cells):
                    field=phi[src[:,None],cells[None,:]]
                    qall[g,cells]=np.sum(weights[:,None]*field,axis=0)
                    mask=src!=g;qoff[g,cells]=np.sum(weights[mask,None]*field[mask],axis=0)
            # Do not silently discard stored padding/unaddressed entries. Report
            # every coverage value and actual unused payload; no guessed formula.
            scatter_coverage.append({'group':g+1,'stored_values':len(scat),'referenced_values':int(np.count_nonzero(covered)),'unreferenced_indices_1based':(np.flatnonzero(covered==0)+1).tolist(),'multiply_referenced_indices_1based':(np.flatnonzero(covered>1)+1).tolist(),'unreferenced_signed_sum':math.fsum(float(v) for v in scat[covered==0])})
        qtotal=qf+qoff
        axial=area[None,:,None]*(current[:,:,1:]-current[:,:,:-1]);axial=axial.reshape(NG,NC)
        rcoef=radial[:,zone,:].transpose(0,2,1).reshape(NG,NC)
        closure=vol[None,:]*rcoef*phi
        corr_collision=vol[None,:]*((tx[:,mat]-self_corr[:,mat])*phi-qoff-qf)
        C=corr_collision+axial;Rclosed=C+closure
        raw_collision=vol[None,:]*(total[:,mat]*phi-qall-qf);raw_balance=raw_collision+axial
        correction=vol[None,:]*((tx[:,mat]-total[:,mat])-(self_corr[:,mat]-macro_self[:,mat]))*phi
        correction_identity=C-raw_balance-correction
        subtraction_identity=C-(Rclosed-closure)
        # All channels are independently retained; no invented absorption
        # sum or multiplicity weighting, particularly for NX/NNP/N2A.
        channel_rates={name:vol[None,:]*phi*value[:,mat] for name,value in channels.items()}
        norm=math.fsum(float(v) for v in rate_integr)
        if norm<=0 or not math.isfinite(norm):raise ValueError('original nonpositive global nufission')
        cur_integr=np.sum(current*area[None,:,None],axis=0);cur_abs=np.sum(np.abs(current)*area[None,:,None],axis=0)
        vals={};scales={}
        for r in range(NR):
            for z in range(NZ):
                i=r*NZ+z;k=(r+1,z+1)
                vals[k]={'volume_cm3':float(vol[i]),'integrated_flux':float(flux_integr[i]),'integrated_nufission':float(rate_integr[i]),'flux_per_global_nufission':float(flux_integr[i]/norm),'nufission_fraction':float(rate_integr[i]/norm)}
                scales[k]={f:abs(v) for f,v in vals[k].items()}
        export_cells=compare_export(INPUTS['regions'][0],('radial_region','axial_cell'),vals,scales,start)
        vals={};scales={}
        for r in range(NR):
            for z in range(NZ+1):
                k=(r+1,z+1);vals[k]={'integrated_net_current_plus_z':float(cur_integr[r,z]),'current_per_global_nufission':float(cur_integr[r,z]/norm)}
                scales[k]={'integrated_net_current_plus_z':float(cur_abs[r,z]),'current_per_global_nufission':float(cur_abs[r,z]/norm)}
        export_faces=compare_export(INPUTS['faces'][0],('radial_region','face'),vals,scales,start)
        coarse_flux=flux_integr.reshape(NR,12,4).sum(axis=2);coarse_rate=rate_integr.reshape(NR,12,4).sum(axis=2)
        # Source phase differs: report signed/absolute/relative discrepancy,
        # never impose an unsupported equality or a physical success threshold.
        source_delta=source_scalar-qtotal
        source_scale=np.maximum(np.abs(source_scalar),np.abs(qtotal))
        source_relative=np.zeros_like(qtotal);mask=source_scale>0;source_relative[mask]=source_delta[mask]/source_scale[mask]
        arrays={'full_flux64':unknown,'full_saved_source32':saved_source,'scalar_flux64':phi,'face_current64':current,'material_indices_1based':mat+1,'scalar_keys_1based':key+1,'snapshot_zones_1based':zone+1,'volumes':vol,'areas':area,'heights':height,'energy_boundaries_stored_units':energy,'fission_component_indices':fission_index,'nusigf_g_f_m':nus,'chi_g_f_m':chi,'fission_production_i_f':prod,'fission_source_g_i':qf,'offgroup_scatter_source_g_i':qoff,'allgroup_scatter_source_g_i':qall,'saved_source_scalar32_promoted_g_i':source_scalar,'saved_vs_final_source_delta_g_i':source_delta,'saved_vs_final_source_relative_g_i':source_relative,'axial_outflow_g_i':axial,'transverse_closure_g_i':closure,'corrected_collision_g_i':corr_collision,'without_closure_g_i':C,'with_closure_g_i':Rclosed,'uncorrected_collision_g_i':raw_collision,'uncorrected_net_collision_plus_axial_g_i':raw_balance,'transport_correction_balance_g_i':correction,'correction_subtraction_identity_g_i':correction_identity,'closure_subtraction_identity_g_i':subtraction_identity,'ntot0_g_m':total,'tranc_g_m':tranc,'system_total_g_m':tx,'system_selfscatter_g_m':self_corr,'macro_selfscatter_g_m':macro_self,'alltarget_transfer_per_source_group_material':transfer_out,'tx_minus_ntot0_plus_tranc_g_m':tx-total+tranc,'selfcorr_minus_macroself_plus_tranc_g_m':self_corr-macro_self+tranc,'original_coarse_integrated_flux':coarse_flux,'original_coarse_integrated_nufission':coarse_rate,'original_13plane_current':cur_integr[:,::4]}
        for name,value in channel_rates.items():arrays['reaction_'+name+'_rate_g_i']=value
        for name,value in channels.items():arrays['reaction_'+name+'_coefficient_g_m']=value
        layouts={}
        for name,value in arrays.items():
            check_time(start)
            if not np.isfinite(value).all():raise ValueError('nonfinite raw output '+name)
            dtype='<i4' if name in ('material_indices_1based','scalar_keys_1based','snapshot_zones_1based','fission_component_indices') else ('<f4' if name in ('full_saved_source32','energy_boundaries_stored_units') else '<f8')
            layouts[name]=out.array(name,value,dtype)
        summary={name:finite_summary(value) for name,value in {'fission_source':vol[None,:]*qf,'offgroup_source':vol[None,:]*qoff,'saved_source_difference':source_delta,'saved_source_relative':source_relative,'corrected_collision':corr_collision,'axial_outflow':axial,'transverse_closure':closure,'with_closure':Rclosed,'without_closure':C,'uncorrected_net_collision_plus_axial':raw_balance,'transport_correction':correction,'correction_identity':correction_identity,'closure_identity':subtraction_identity}.items()}
        summary['channels_unweighted_by_neutron_multiplicity']={name:finite_summary(value) for name,value in channel_rates.items()}
        summary['per_group']={name:np.sum(value,axis=1).tolist() for name,value in {'fission_source':vol[None,:]*qf,'collision':corr_collision,'axial':axial,'closure':closure,'with_closure':Rclosed,'without_closure':C,'raw_net_collision_plus_axial':raw_balance,'correction':correction}.items()}
        summary['per_cell']={name:np.sum(value,axis=0).tolist() for name,value in {'fission_source':vol[None,:]*qf,'axial':axial,'closure':closure,'with_closure':Rclosed,'without_closure':C}.items()}
        guards={}
        for name in ('B2  B1HOM','OPTION','IMERGE-LEAK'):
            e=a.root.get(name)
            if e is None:guards[name]={'present':False};continue
            b=a.raw(a.root,name,e[1],e[2],'ROOT')
            guards[name]={'present':True,'type':e[2],'length_words':e[1],'sha256':hashlib.sha256(b).hexdigest()}
            if e[2]==2:guards[name]['stored_REAL32_values']=np.frombuffer(b,'<f4').astype(float).tolist()
            elif e[2]==1:guards[name]['stored_INT32_values']=np.frombuffer(b,'<i4').tolist()
            elif e[2]==3:guards[name]['stored_text']=b.decode('ascii').rstrip(' \0')
        result={'classification':'ALL_370_GROUP_SAVED_SOURCE_REACTION_FLUX_DIAGNOSTICS_COMPLETE_NOT_PHYSICAL_BALANCE_QUALIFIED','dimensions':{'groups':NG,'mixtures':NM,'fission_components':NF,'cells':NC,'faces':LL5,'radial_regions':NR,'axial_cells':NZ,'unknowns_per_group':NU},'full_group_fine_cell_coverage':True,'global_nufission_replayed':norm,'chi_sum_by_component_material':np.sum(chi,axis=0).tolist(),'energy_monotonic':energy_monotonic,'energy_units':'stored units, not inferred/converted','scatter_coverage':scatter_coverage,'export_replay':{'cells':export_cells,'faces':export_faces},'summary':summary,'saved_guard_records':guards,'source_scope':{'saved_work_source_type':'REAL32 last-buffer projection','final_state_source_reconstructed':True,'saved_work_source_equals_final_state_source_assessed':False,'axial_R64_work_source_present':False,'S2_guarded_SIGS_source_not_reconstructed':True,'radial_source_not_substituted':True,'historical_executable_current_source_equivalence_assumed':False},'reaction_scope':{'all_present_named_channels_retained':list(CHANNELS),'neutron_multiplicity_contract_supplied':False,'NX_semantics_assessed':False,'physical_absorption_formula_assumed':False,'net_total_minus_transfer_is_not_absorption':True,'transport_correction_zero_hypothesis_accepted':False},'scientific_accuracy_qualified':False,'AAA_qualified':False,'ABA_admitted':False,'same_MG_unreduced_reference_qualified':False,'reaction_raw_transfer_equivalence_qualified':False,'full_physical_neutron_balance_qualified':False,'original_scientific_thresholds_unchanged':True,'transport_launched':False,'basis_rank_or_white_coefficients_modified':False,'no_clipping_renormalization_or_dropped_bin':True}
        out.json_file('layout.json',{'arrays':layouts,'cell_order':'radial region outer, axial cell inner, zero-based raw array; stored maps included','group_order':'exact stored370-group order; ENERGY sequence preserved','face_current_sign':'positive-z, all49 axial planes and8regions','fission_axes':'group,fission_component,material','original_observation':'exact4finecells to1 originalcell, single global denominator; original13planes only after complete392fineface retained'})
        out.json_file('record_inventory.json',{name:{'root_directory':reader.root,'records':reader.records,'bytes_read':reader.bytes_read} for name,reader in readers.items()})
        return result
    finally:
        for reader in readers.values():
            if not reader.stream.closed:reader.close()


def main():
    global np
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evaluator-sha256',required=True)
    parser.add_argument('--out-root',default=str(DEFAULT_OUTPUT))
    args=parser.parse_args()
    if SOURCE_STATUS!='READY':raise RuntimeError('source-only UNREADY evaluator: Root source admission required')
    for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
        if os.environ.get(name)!='1':raise ValueError('original single-thread environment required: '+name)
    import numpy as numpy
    np=numpy
    start=time.monotonic();selfpath=Path(__file__).absolute();self_before=fresh_hash(selfpath,start)
    if self_before['sha256']!=args.evaluator_sha256:raise ValueError('evaluator source pin differs')
    # A fresh exclusive namespace is the irreversible run claim. Never retry it.
    out=Output(Path(args.out_root),start)
    out.json_file('execution_claim.json',{'schema':'REFINED_AAA_ALL_GROUP_READ_ONLY_DIAGNOSTIC_RUN_CLAIM_V1','evaluator':self_before,'declared_limits':{'wall_seconds':WALL_SECONDS,'own_rss_mib':RSS_LIMIT_MIB,'archive_bytes':ARCHIVE_LIMIT_BYTES,'threads':THREADS,'children':CHILDREN,'retries':RETRIES},'parent_PID':os.getppid(),'PID':os.getpid(),'started_unix':time.time(),'normal_genuine_OwnRSS_supervision_required':True})
    before={}
    for role,(path,expected) in INPUTS.items():
        item=fresh_hash(path,start)
        if item['sha256']!=expected:raise ValueError('immutable input pin differs: '+role)
        before[role]=item
    status=json.loads(INPUTS['run_status'][0].read_text());seal=json.loads(INPUTS['final_seal'][0].read_text());protocol=json.loads(INPUTS['protocol'][0].read_text())
    if status['cases']['AAA']['classification']!='VALID_MET' or status['cases']['AAA']['completed_maps']!=12 or status['cases']['AAA']['final_directory']!=str(PROD/'AAA/map012'):raise ValueError('original final MET pointer changed')
    if seal['classification']!='SEALED_STAGE_OUTPUTS' or seal['sha256']['closed_axial.xsm']!=INPUTS['closed_axial'][1] or seal['sha256']['candidate_system.xsm']!=INPUTS['system'][1]:raise ValueError('original final seal binding differs')
    if protocol['production_prepared']['sha256']!=INPUTS['prepared'][1] or protocol['final_stage_seal']['sha256']!=INPUTS['final_seal'][1]:raise ValueError('old exporter preparation/seal binding differs')
    for role in ('track','macro','closed_axial'):
        if protocol['source_inputs'][str(INPUTS[role][0])]!=INPUTS[role][1]:raise ValueError('old exporter frozen input differs')
    result=evaluate(out,before,start)
    after={}
    for role,(path,expected) in INPUTS.items():
        item=fresh_hash(path,start)
        if item['sha256']!=expected or item['literal_7id_before']!=before[role]['literal_7id_before'] or item['target_7id_before']!=before[role]['target_7id_before'] or item['literal_symlink_text']!=before[role]['literal_symlink_text']:raise ValueError('input changed across complete diagnostic: '+role)
        after[role]=item
    self_after=fresh_hash(selfpath,start)
    if self_after['sha256']!=self_before['sha256'] or self_after['literal_7id_before']!=self_before['literal_7id_before'] or self_after['target_7id_before']!=self_before['target_7id_before']:raise ValueError('evaluator source changed')
    out.json_file('input_identities.json',{'before':before,'after':after,'evaluator_before':self_before,'evaluator_after':self_after})
    result['elapsed_seconds_before_final_report']=time.monotonic()-start
    out.json_file('result.json',result)
    members=dict(out.files)
    out.json_file('payload_manifest.json',{'schema':'REFINED_AAA_INDEPENDENT_ALL_GROUP_DIAGNOSTIC_PAYLOAD_MANIFEST_V1','files':members,'payload_bytes_before_manifest':out.bytes,'scientific_accuracy_qualified':False,'requires_Root_actual_terminal_and_OwnRSS_receipts':True})
    check_time(start)
    print(json.dumps({'classification':result['classification'],'result':str(out.path/'result.json'),'sha256':out.files['result.json']['sha256'],'payload_manifest':str(out.path/'payload_manifest.json'),'manifest_sha256':out.files['payload_manifest.json']['sha256'],'archive_bytes':out.bytes,'elapsed_seconds':time.monotonic()-start,'scientific_accuracy_qualified':False},indent=2,allow_nan=False))


if __name__=='__main__':main()
