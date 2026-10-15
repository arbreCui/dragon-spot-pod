"""Independently sum saved REAL64 axial P0 terms; no transport or fitting.

The ratio transverse term is retained and then separately reported. White outer
radial boundaries imply zero physical net radial escape. A small residual of
the equation containing that term does not by itself establish physical balance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from snapshot_control_preflight import _open_xsm
from qualified_snapshot_ingestion import list_handles

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'validation/artifacts'
PROD=ART/'axial-material-production-qualified-AB-compensated-20261004'
OUT=ART/'axial-material-AAA-global-transverse-balance-20261004'
FINAL=PROD/'AAA/map004'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value,stream,indent=2)
        stream.write('\n')


def data(archive,directory,name,dtype,count=None):
    entry=directory[name]
    kind={'<i4':1,'<f4':2,'<f8':4}[dtype]
    if entry[2]!=kind or entry[1]<=0:
        raise ValueError('invalid scalar record: '+name)
    result=np.frombuffer(archive.read(entry[0],entry[1]),dtype).copy()
    if count is not None and len(result)!=count:
        raise ValueError('unexpected scalar record length: '+name)
    if not np.all(np.isfinite(result)):
        raise ValueError('nonfinite scalar record: '+name)
    return result


def directories(archive,name,count):
    handles=list_handles(archive,archive.root,name,count)
    if any(handle[1:]!=(-1,0) for handle in handles):
        raise ValueError('directory list required: '+name)
    return [archive.directory(handle[0]) for handle in handles]


def prepare():
    OUT.mkdir(exist_ok=False)
    paths=[PROD/'AAA/bootstrap/initial_axial_track.xsm', PROD/'AAA/bootstrap/initial_axial_macrolib.xsm',
        FINAL/'closed_axial.xsm',FINAL/'candidate_system.xsm',FINAL/'result.json',PROD/'AAA/run_status.json',
        Path(__file__).resolve(),Path(sys.modules['snapshot_control_preflight'].__file__),Path(sys.modules['qualified_snapshot_ingestion'].__file__)]
    write_new(OUT/'declaration.json',dict(schema='AXMAT_SAVED_R64_GLOBAL_P0_TRANSVERSE_DIAGNOSTIC_V1',declared_unix=time.time(),
        files={str(p.resolve()):digest(p) for p in paths},
        equation='sum V*((TX-selfscatter)*phi-offgroup_scatter-fission_source)+axial_out+sum V*radial_ratio*phi=0',
        physical_scope='Whole-domain net transverse escape is zero for the declared isotropic unit-albedo outer radial boundary. Report the sum of the closure term without deleting, clipping, fitting or changing it.',
        interpretation='Saved 370-group P0 coefficient/accounting diagnostic only. Includes original transfer multiplicities and transport correction; not an independent CE absorption measurement or a complete regional physical balance qualification.',
        acceptance='Report actual numbers and exact subtraction identity. No new cross-method accuracy threshold or claimed error attribution.',
        wall_seconds=60,threads=1,retries=0,transport_launched=False))
    print(json.dumps(dict(declaration=str(OUT/'declaration.json'),sha256=digest(OUT/'declaration.json'))))


def run(expected):
    if digest(OUT/'declaration.json')!=expected:
        raise ValueError('diagnostic declaration changed')
    decl=json.loads((OUT/'declaration.json').read_text())
    for name,wanted in decl['files'].items():
        if digest(name)!=wanted:raise ValueError('frozen input changed: '+name)
    if (OUT/'run_claim.json').exists():raise ValueError('no retry')
    write_new(OUT/'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    started=time.monotonic()
    with _open_xsm(PROD/'AAA/bootstrap/initial_axial_track.xsm') as track, \
            _open_xsm(PROD/'AAA/bootstrap/initial_axial_macrolib.xsm') as macro, \
            _open_xsm(FINAL/'closed_axial.xsm') as axial, \
            _open_xsm(FINAL/'candidate_system.xsm') as system:
        st=data(track,track.root,'STATE-VECTOR','<i4',40)
        ms=data(macro,macro.root,'STATE-VECTOR','<i4',40)
        nr,nz,ns,nunk,ll4=int(st[5]),int(st[6]),int(st[7]),int(st[1]),int(st[10])
        ng,nm,nfis=int(ms[0]),int(ms[1]),int(ms[3])
        if (nr,nz,ns,ng)!=(8,12,3,370):raise ValueError('wrong saved AAA dimensions')
        key=data(track,track.root,'KEYFLX','<i4',nr*nz)-1
        mat=data(track,track.root,'MATCOD','<i4',nr*nz)-1
        zone=data(track,track.root,'MAT1D','<i4',nz)-1
        volume=data(track,track.root,'VOLUME','<f4',nr*nz).astype(float)
        area=data(track,track.root,'AREA2D','<f4',nr).astype(float)
        k=float(data(axial,axial.root,'SPOT-KEFF64','<f8',1)[0])
        handles=list_handles(axial,axial.root,'FLUX64',ng)
        if any(h[1:]!=(2*nunk,4) for h in handles):raise ValueError('not authoritative REAL64 flux')
        unknown=np.array([np.frombuffer(axial.read(h[0],h[1]),'<f8') for h in handles])
        phi=unknown[:,key]
        if np.any(phi<=0) or not np.all(np.isfinite(unknown)) or k<=0:
            raise ValueError('invalid authoritative saved field')
        mg=directories(macro,'GROUP',ng); sg=directories(system,'GROUP',ng)
        nuf=np.stack([data(macro,g,'NUSIGF','<f4',nm*nfis).reshape(nfis,nm) for g in mg]).astype(float)
        component=np.einsum('gfi,gi->fi',nuf[:,:,mat],phi)
        nuf_total=float(np.sum(component*volume[None,:]))
        reaction=[]; fission=[]; transverse=[]; outward=[]
        for g in range(ng):
            chi=data(macro,mg[g],'CHI','<f4',nm*nfis).reshape(nfis,nm).astype(float)
            source=(chi[:,mat]*component).sum(axis=0)/k
            source_off=np.zeros(nr*nz)
            nj=data(macro,mg[g],'NJJS00','<i4',nm)
            ij=data(macro,mg[g],'IJJS00','<i4',nm)-1
            ip=data(macro,mg[g],'IPOS00','<i4',nm)-1
            scat=data(macro,mg[g],'SCAT00','<f4').astype(float)
            for index,material in enumerate(mat):
                for j in range(nj[material]):
                    source_group=ij[material]-j; offset=ip[material]+j
                    if not 0<=source_group<ng or not 0<=offset<len(scat):raise ValueError('invalid compressed transfer')
                    if source_group!=g:source_off[index]+=scat[offset]*phi[source_group,index]
            tx=data(system,sg[g],'DRAGON-TXSC','<f4',nm+1).astype(float)[1:]
            sx=data(system,sg[g],'DRAGON-S0XSC','<f4').astype(float).reshape(-1,nm+1)[0,1:]
            delta=data(system,sg[g],'RADIAL-OP64','<f8',nr*ns).reshape(ns,nr)
            coefficient=np.array([delta[zone[z],r] for r in range(nr) for z in range(nz)])
            reaction.append(float(np.dot(volume,(tx[mat]-sx[mat])*phi[g]-source_off)))
            fission.append(float(np.dot(volume,source)))
            transverse.append(float(np.dot(volume,coefficient*phi[g])))
            cour=unknown[g,ll4:ll4+nr*(nz+1)].reshape(nr,nz+1)
            outward.append(float(np.dot(area,cour[:,-1]-cour[:,0])))
    source=sum(fission); net_reaction=sum(reaction); net_transverse=sum(transverse); escape=sum(outward)
    if source<=0 or not np.isfinite(source):raise ValueError('nonpositive total fission source')
    closed=(net_reaction+escape+net_transverse-source)/source
    physical=(net_reaction+escape-source)/source
    result=dict(classification='COMPLETE_SAVED_R64_GLOBAL_TRANSVERSE_DIAGNOSTIC_ONLY',case='AAA',k64=k,
        global_nufission=nuf_total,global_chi_weighted_fission_source=source,
        terms=dict(net_total_minus_allgroup_transfer=net_reaction,axial_outward=escape,transverse_ratio_term=net_transverse,fission_source=source),
        normalized_by_fission_source=dict(closed_P0_residual=closed,without_transverse_P0_residual=physical,
            transverse_ratio_term=net_transverse/source,axial_outward=escape/source),
        subtraction_identity_error=physical-(closed-net_transverse/source),
        expected_physical_net_radial_escape=0.0,
        per_group=dict(net_reaction=reaction,fission_source=fission,transverse_term=transverse,axial_outward=outward),
        input_identities=decl['files'],scientific_accuracy_qualified=False,
        caveat=decl['interpretation'],elapsed_seconds=time.monotonic()-started)
    for name,wanted in decl['files'].items():
        if digest(name)!=wanted:raise ValueError('input changed during audit')
    if result['elapsed_seconds']>60:raise TimeoutError('declared host limit exceeded')
    write_new(OUT/'result.json',result)
    print(json.dumps({key:value for key,value in result.items() if key not in ('per_group','input_identities')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else run(args.sha256)
