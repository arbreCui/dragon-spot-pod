"""Direct terminal A/B material and complete original native track input support.

This module reads saved mathematical inputs only. It does not run transport,
build a library, grant historical SPH/MASK/reaction evidence,
or replace the unchanged online BOOT. Its outputs are unqualified actual-data
candidates for the separately admitted independent full370 reference adapter.
"""
from pathlib import Path
import hashlib
import struct
import sys
import numpy as np
ROOT=Path('/Users/wen/spot')
sys.path.insert(0,str(Path(__file__).resolve().parent))
from snapshot_control_preflight import _open_xsm

NG=370;NM=8;NL=3;NF=32;NTRACK=11364;NAZI=96;NPOLAR=4
CASE_SHA='ac3e67ffdc25f5bfa45bca5170253de8e875c983550e5ee878ee30c5d1a4c2c4'


def list_handles(archive,directory,name,count):
    raw=archive.record(directory,name,count,10)
    return [archive.directory(offset)['***HANDLE***'] for offset in struct.unpack(f'<{count}i',raw)]


def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()


def pin(item):
    p=Path(item['path'])
    if not p.is_absolute() or sha(p)!=item['sha256']:
        raise ValueError('actual whole-input SHA mismatch: '+str(p))
    return p


def array(a,d,name,dtype,count):
    kind={'<i4':1,'<f4':2,'<f8':4}[dtype]
    raw=a.record(d,name,count*(2 if dtype=='<f8' else 1),kind)
    v=np.frombuffer(raw,dtype).copy()
    if not np.isfinite(v).all():raise ValueError('nonfinite original record '+name)
    return v,dict(offset_words=d[name][0],length_words=d[name][1],type=d[name][2],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def variable(a,d,name,dtype):
    e=d.get(name);kind={'<i4':1,'<f4':2,'<f8':4}[dtype]
    if e is None or e[2]!=kind or e[1]<0 or (kind==4 and e[1]%2):
        raise ValueError('unexpected stored variable record '+name)
    raw=a.read(e[0],e[1]);v=np.frombuffer(raw,dtype).copy()
    if not np.isfinite(v).all():raise ValueError('nonfinite original record '+name)
    return v,dict(offset_words=e[0],length_words=e[1],type=e[2],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def child(a,d,name):
    e=d.get(name)
    if e is None or e[1:]!=(-1,0):raise ValueError('directory required: '+name)
    return a.directory(e[0])


def terminal_material_from_snapshot(item):
    """Read only original final MACROLIB; preserve raw f4 before promotion.

    Source/destination mapping is original MGXEXP/MGX and LIBDEN convention.
    Higher moments remain signed. Full-P2 uses raw NTOT0/SCAT, with no TRANC
    subtraction in this declared raw full-P2 reference: FLU disables correction
    at NANI>1; ASM additionally requires ISTRM==1 for that branch. TRANC,
    SIGS and SIGW remain independently returned for context verification.
    This is NOT an upstream-SPH/MASK or physical-reaction proof.
    """
    path=pin(item);records={};coverage={}
    with _open_xsm(path) as a:
        micro=a.object('MICROLIB2');macro=child(a,micro,'MACROLIB')
        state,r=array(a,macro,'STATE-VECTOR','<i4',40);records['STATE-VECTOR']=r
        if state[:4].tolist()!=[NG,NM,NL,NF]:raise ValueError('original 370/8/3/32 dimensions required')
        energy,r=array(a,macro,'ENERGY','<f4',NG+1);records['ENERGY']=r
        if not np.all(np.diff(energy.astype('f8'))<0):raise ValueError('original descending group boundaries required')
        fission_flat,r=variable(a,macro,'FISSIONINDEX','<i4');records['FISSIONINDEX']=r
        # Source LIBDEN: STATE(4)=NFISSI*NESP, FISSIONINDEX=NM*NFISSI.
        # Current actual endpoint is 8*8=64 integers / 256 bytes, whereas
        # NUSIGF/CHI have 8*32=256 reals per destination group.
        if not len(fission_flat) or len(fission_flat)%NM:raise ValueError('invalid original FISSIONINDEX length')
        nfissi=len(fission_flat)//NM
        if NF%nfissi:raise ValueError('fission isotope/spectrum decomposition differs')
        nesp=NF//nfissi;fission_index=fission_flat.reshape(nfissi,NM).T.copy()
        # Stored CHI-LIMITS are 0-based prefix boundaries. LIBDEN837-843
        # uses group>lower and group<=upper; never reinterpret as 1..371.
        chi_limits,cr=variable(a,micro,'CHI-LIMITS','<i4')
        if (len(chi_limits)!=nesp+1 or chi_limits[0]!=0 or chi_limits[-1]!=NG or np.any(np.diff(chi_limits)<=0)):
            raise ValueError('original multi-spectrum energy windows differ')
        micro_records={'CHI-LIMITS':cr};micro_fields={}
        for key,dtype in [('ISOTOPESMIX','<i4'),('ISOTOPESDENS','<f4'),('ISOTOPESTEMP','<f4')]:
            micro_fields[key],micro_records[key]=array(a,micro,key,dtype,62)
        if np.any((fission_index<0)|(fission_index>62)):raise ValueError('original fission slot out of range')
        channel_fission_index=np.repeat(fission_index,nesp,axis=1)
        channel_window=np.tile(np.arange(nesp),nfissi)
        handles=list_handles(a,macro,'GROUP',NG)
        if any(e[1:]!=(-1,0) for e in handles):raise ValueError('all destination group directories required')
        total=np.empty((NM,NG),dtype='<f4');tranc=np.empty_like(total)
        scatter=np.zeros((NM,NL,NG,NG),dtype='<f4')
        sigs=np.empty((NM,NL,NG),dtype='<f4');sigw=np.empty_like(sigs)
        nuf=np.empty((NM,NF,NG),dtype='<f4');chi=np.empty_like(nuf)
        event_names=('NFTOT','NG','N2N','N3N','N4N','NA','NP','N2A','NNP','ND','NT','NX')
        events={name:np.empty_like(total) for name in event_names}
        for g,e in enumerate(handles):
            d=a.directory(e[0]);prefix=f'GROUP/{g+1}/'
            for name,target in [('NTOT0',total),('TRANC',tranc),*events.items()]:
                value,r=array(a,d,name,'<f4',NM);target[:,g]=value;records[prefix+name]=r
            for name,target in [('NUSIGF',nuf),('CHI',chi)]:
                value,r=array(a,d,name,'<f4',NM*NF)
                target[:,:,g]=value.reshape(NF,NM).T;records[prefix+name]=r
            for l in range(NL):
                suffix=f'{l:02d}'
                for label,target in [('SIGS',sigs),('SIGW',sigw)]:
                    value,r=array(a,d,label+suffix,'<f4',NM)
                    target[:,l,g]=value;records[prefix+label+suffix]=r
                ij,ri=array(a,d,'IJJS'+suffix,'<i4',NM)
                nj,rn=array(a,d,'NJJS'+suffix,'<i4',NM)
                ip,rp=array(a,d,'IPOS'+suffix,'<i4',NM)
                if 'SCAT'+suffix in d:
                    values,rv=variable(a,d,'SCAT'+suffix,'<f4')
                else:
                    # MGXEXP148-156 explicitly leaves a missing/zero-length
                    # SCAT group action zero. A nonzero sparse span would be
                    # inconsistent with a readable full reference input.
                    if np.any(nj):raise ValueError('missing SCAT with active original sparse spans')
                    values=np.empty(0,dtype='<f4')
                    rv={'record_absent':True,'meaning':'EXPLICIT_ZERO_BY_MGXEXP_LCMLEN_BRANCH','bytes':0}
                for name,r in [('IJJS',ri),('NJJS',rn),('IPOS',rp),('SCAT',rv)]:records[prefix+name+suffix]=r
                addressed=np.zeros(len(values),dtype=np.uint16)
                for m in range(NM):
                    count=int(nj[m]);first=int(ij[m])-1;offset=int(ip[m])-1
                    if not 0<=count<=NG:raise ValueError('compressed scattering count out of range')
                    if count==0:continue
                    sources=first-np.arange(count);positions=offset+np.arange(count)
                    if (np.any(sources<0) or np.any(sources>=NG) or np.any(positions<0) or np.any(positions>=len(values))):
                        raise ValueError('compressed scattering mapping out of range')
                    scatter[m,l,g,sources]=values[positions];addressed[positions]+=1
                # Unaddressed payload is retained explicitly for the authority;
                # no silent padding discard, no fabricated duplicate transfer.
                coverage[prefix+'SCAT'+suffix]=dict(count=addressed,
                    unaddressed_values=values[addressed==0].copy(),
                    multiply_addressed_values=values[addressed>1].copy())
        if np.any(total<0) or np.any(scatter[:,0]<0) or np.any(nuf<0) or np.any(chi<0):
            raise ValueError('original nonnegative total/P0/fission input violated')
        track=a.object('TRACK');track_fields={};track_records={}
        for name,dtype,count in [('STATE-VECTOR','<i4',40),('MCCG-STATE','<i4',40),
                ('MATCOD','<i4',NM),('KEYFLX','<i4',NM),('KEYCUR$MCCG','<i4',6),
                ('BC-REFL+TRAN','<i4',6),('ALBEDO','<f4',6),('V$MCCG','<f4',14),
                ('XMU$MCCG','<f4',NPOLAR),('ZMU$MCCG','<f4',NPOLAR),('WZMU$MCCG','<f4',NPOLAR)]:
            track_fields[name],track_records[name]=array(a,track,name,dtype,count)
    pin(item)
    return dict(total_f4=total,raw_scatter_f4=scatter,nusigf_f4=nuf,chi_f4=chi,
        tranc_f4=tranc,sigs_f4=sigs,sigw_f4=sigw,events_f4=events,
        energy_f4=energy,fission_index=fission_index,nfission_isotopes=nfissi,nenergy_spectra=nesp,
        channel_fission_index=channel_fission_index,channel_energy_window=channel_window,
        chi_limits=chi_limits,micro_context_fields=micro_fields,micro_record_identity=micro_records,track=track_fields,
        macro_record_identity=records,track_record_identity=track_records,
        compressed_payload_coverage=coverage,whole_snapshot=item,
        status='UNQUALIFIED_TERMINAL_MATHEMATICAL_INPUT_SUPPORT',actual_context_admitted=False,
        historical_SPH_MASK_qualified=False,reaction_balance_qualified=False,
        online_boot_changed=False,full_reference_qualified=False)


def native_track_inventory(item):
    """Read every current format1 record, retaining original 0-based index.

    The record angle selects one native azimuth; do not multiply each track by
    96 again. The 4x2x2 states per original track give exactly181824 actions.
    This parser does not infer original volume/surface/angle normalization.
    """
    path=pin(item);record_hashes=[]
    with path.open('rb') as f:
        def record():
            marker=f.read(4)
            if len(marker)!=4:raise ValueError('missing current ray record')
            n=struct.unpack('<i',marker)[0]
            if n<0 or n>1000000:raise ValueError('unsupported record size')
            raw=f.read(n)
            if len(raw)!=n or f.read(4)!=marker:raise ValueError('invalid current ray record')
            record_hashes.append(hashlib.sha256(raw).hexdigest());return raw
        magic,ncom,ntr,fmt=struct.unpack('<4siii',record())
        if (magic,ncom,ntr,fmt)!=(b'$TRK',5,NTRACK,1):raise ValueError('original current track header differs')
        comments=[record() for _ in range(ncom)];state=record()
        if np.frombuffer(state,'<i4').tolist()!=[2,0,8,6,6,1,96,1,17]:raise ValueError('current track state differs')
        metadata=[record() for _ in range(6)]
        if [len(v) for v in metadata]!=[60,60,24,24,1536,768]:raise ValueError('original angular metadata dimensions differ')
        azi=np.frombuffer(metadata[4],'<f8').reshape(NAZI,2).copy()
        if not np.isfinite(azi).all():raise ValueError('nonfinite azimuth metadata')
        tracks=[]
        for index in range(ntr):
            raw=record();nsub,nseg=struct.unpack_from('<ii',raw)
            weight=struct.unpack_from('<d',raw,8)[0];angle=struct.unpack_from('<i',raw,16)[0]-1
            if nsub!=1 or not 3<=nseg<=17 or len(raw)!=20+12*nseg+32:
                raise ValueError('current full ray layout differs')
            nom=np.frombuffer(raw,'<i4',nseg,20).copy()
            h2=np.frombuffer(raw,'<f8',nseg,20+4*nseg).copy()
            tags=struct.unpack_from('<4i2d',raw,20+12*nseg)
            entry=-int(nom[0])-1;exit=-int(nom[-1])-1
            if (not np.isfinite(weight) or weight<=0 or not 0<=angle<NAZI or
                not np.isfinite(h2).all() or np.any(h2[1:-1]<=0) or
                np.any((nom[1:-1]<1)|(nom[1:-1]>NM)) or
                not 0<=entry<6 or not 0<=exit<6 or entry==exit or
                not np.isfinite(tags).all()):raise ValueError('current ray geometry/weight/tags differ')
            tracks.append(dict(original_track=index,angle=angle,weight=weight,
                planar_widths=h2[1:-1].copy(),regions=nom[1:-1]-1,
                entry_surface=entry,exit_surface=exit,all_original_nom=nom,
                all_original_h2=h2,format1_tags=tags))
        if f.read(1):raise ValueError('extra current ray EOF bytes')
    pin(item)
    return dict(tracks=tracks,azimuth_xy=azi,raw_metadata=metadata,comments=comments,
        record_sha256=record_hashes,whole_track=item,
        status='UNQUALIFIED_FULL_ORIGINAL_TRACK_INPUT_SUPPORT',actual_context_admitted=False)


def actual_reference_binding(A,B,rays,evidence,authority):
    """No declaration-only or array-shape admission; genuine authority required.

    The separately implemented authority must actually check exact final
    macro/track/geometry/temperature/density/fission/angular identities and all
    compressed payload, original SPH/MASK context and independent event
    multiplicity coverage. It must bind these arrays and receipts themselves.
    Missing historical/physical evidence remains UNKNOWN, not true/zero.
    """
    if not callable(authority) or authority(A,B,rays,evidence) is not True:
        raise ValueError('actual full370 material/track/physical-context binding UNREADY')
    return dict(status='EXTERNALLY_VERIFIED_INPUT_BINDING_ONLY',
        full_reference_qualified=False,AAA_qualified=False,ABA_admitted=False)
