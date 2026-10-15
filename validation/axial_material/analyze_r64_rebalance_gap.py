"""Explain the saved-state/bare-image gap with an independent balance matrix."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from analyze_r64_snapshot import analyze


def diagnose(path):
    original=analyze(path)
    data=path.read_bytes();offset=0
    def take(dtype,shape):
        nonlocal offset
        out=np.frombuffer(data,dtype=dtype,count=int(np.prod(shape)),offset=offset).reshape(shape,order='F').copy()
        offset+=out.nbytes
        return out
    if take('<i4',(5,)).tolist()!=[370,8,14,8,32]:
        raise ValueError('unexpected export')
    k=take('<f8',(1,))[0];v=take('<f4',(8,)).astype('f8')
    mat=take('<i4',(8,));key=take('<i4',(8,))-1
    phi=take('<f8',(14,370));take('<f4',(14,370));take('<f8',(14,370))
    nuf=take('<f4',(8,32,370)).astype('f8');chi=take('<f4',(8,32,370)).astype('f8')
    total=take('<f4',(9,370)).astype('f8');within=take('<f4',(9,370)).astype('f8')
    scatter=take('<f4',(8,370,370)).astype('f8');take('<f8',(14,370));fresh=take('<f8',(14,370))
    if offset!=len(data) or mat.tolist()!=list(range(1,9)):
        raise ValueError('bad export')
    production=np.einsum('msj,mj->ms',nuf,phi[key],optimize=False)
    qfis=np.einsum('msi,ms->mi',chi,production,optimize=False)/k
    indices=np.arange(370);scatter[:,indices,indices]=0
    matrix=-np.einsum('mij,mj,m->ij',scatter,fresh[key],v,optimize=False)
    matrix[indices,indices]=np.sum((total[1:]-within[1:])*fresh[key]*v[:,None],axis=0)
    rhs=np.sum(qfis*v[:,None],axis=0)
    factors=np.linalg.solve(matrix,rhs)
    balanced=fresh*factors[None,:]
    if not np.isfinite(balanced).all() or np.any(factors<=0):
        raise ValueError('invalid independent balance factors')
    error=np.max(np.abs(balanced-phi),axis=0)/np.max(np.abs(balanced),axis=0)
    matrix_error=float(np.linalg.norm(matrix@factors-rhs)/np.linalg.norm(rhs))
    # Best scalar per group distinguishes a spatial-shape error from scaling.
    best=np.sum(fresh*phi,axis=0)/np.sum(fresh*fresh,axis=0)
    shape_error=np.max(np.abs(fresh*best[None,:]-phi),axis=0)/np.max(np.abs(phi),axis=0)
    return dict(classification='REBALANCE_GAP_DIAGNOSTIC',
        original_audit_classification=original['classification'],original_audit_still_passes=False,
        bare_image_defect=original['maximum_full_image_defect'],
        independently_rebalanced_image_defect=float(np.max(error)),
        maximum_spatial_shape_defect_after_group_scale=float(np.max(shape_error)),
        maximum_balance_factor_change=float(np.max(np.abs(factors-1))),
        independent_balance_matrix_relative_residual=matrix_error,
        rebalanced_image_below_original_threshold=bool(np.max(error)<original['terminal_threshold']),
        bare_failing_groups=[g['group'] for g in original['groups'] if g['full_image_defect']>=original['terminal_threshold']],
        snapshot_qualified=False,production_qualified=False,
        scope='Post-audit diagnostic only. Reconstruct the complete all-group rebalancing matrix from frozen coefficients and the exported bare transport image; do not replace or relax the preregistered bare-image gate.',
        export_sha256=hashlib.sha256(data).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();result=diagnose(args.export)
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
