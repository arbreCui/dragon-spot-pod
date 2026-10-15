"""Prepare a bounded conditional side-white angular-model audit after CE ends.

No native solver or physical input is changed. Algebraic success cannot certify
the heterogeneous boundary trace, a coupled eigenproblem or AAA/ABA accuracy.
"""
import argparse
import json
from pathlib import Path
import sys
import time

sys.dont_write_bytecode=True
import white_side_trace_kernel as kernel
from prepare_qualified_AAA_ce_long_generations import ART, ROOT, OUT as CE, PRODUCTION, digest, pin, verify, write_new

OUT=ART / 'axial-material-AAA-white-trace-angular-model-20261004'
sys.path.insert(0,str(PRODUCTION / 'runtime'))
from snapshot_control_preflight import _open_xsm
from qualified_snapshot_ingestion import list_handles
from production_runner import DiskResources,SerialExecutor


def vector(archive,directory,name,dtype):
    import numpy as np
    item=directory[name]
    if item[2]!={'<f4':2,'<i4':1}[dtype] or item[1]<=0:
        raise ValueError('unexpected native input type: '+name)
    return np.frombuffer(archive.read(item[0],item[1]),dtype).copy()


def prepare():
    OUT.mkdir(exist_ok=False);(OUT / 'runtime').mkdir();(OUT / 'AAA').mkdir()
    import shutil
    shutil.copy2(PRODUCTION / 'runtime/run_bounded_dragon.py',OUT / 'runtime/run_bounded_dragon.py')
    original_spec=Path(json.loads((PRODUCTION / 'prepared.json').read_text())['case_spec']['path'])
    sources=[Path(__file__).resolve(),Path(kernel.__file__).resolve(),
        Path(__import__('prepare_qualified_AAA_ce_long_generations').__file__).resolve(),
        Path(__import__('prepare_qualified_AAA_ce_ufs').__file__).resolve(),
        *[Path(__import__(m).__file__).resolve() for m in ('production_runner','snapshot_control_preflight','qualified_snapshot_ingestion')],
        OUT / 'runtime/run_bounded_dragon.py',Path(sys.executable).resolve(),ROOT / 'src/SPOT1P64.f90',
        Path('/Users/wen/openmc-workspace/src/src/surface.cpp'),Path('/Users/wen/openmc-workspace/src/src/boundary_condition.cpp'),
        ROOT / 'validation/iterative/native_layered_full_action.py',ROOT / 'validation/iterative/native_layered_full_result.md',
        PRODUCTION / 'AAA/bootstrap/initial_axial_track.xsm',PRODUCTION / 'AAA/bootstrap/basis_reference.xsm',
        original_spec,CE / 'AAA/execution.json',CE / 'AAA/run_claim.json']
    write_new(OUT / 'declaration.json',dict(schema='AXMAT_WHITE_SIDE_CONDITIONAL_TRACE_ALGEBRA_V1',declared_unix=time.time(),
        files={str(p.resolve()):digest(p) for p in sources},case_spec=pin(original_spec),
        current_reference_manifest=pin(CE / 'AAA/execution.json'),current_reference_claim=pin(CE / 'AAA/run_claim.json'),
        source_gate='Do not launch this algebra child while the declared CE child is live. Its native_result must bind the same claim and contain a terminal return code.',
        model='Azimuth averaged outgoing side-wall angular flux; regionwise constant trace supplied explicitly from the declared basis. Side perimeter is physical hexagon geometry. Finite quadrature uses the same incoming/outgoing current measure, so its P0 net contribution vanishes.',
        exact_local_return='For any vertical wall normal, cosine-law reflected source particles have axial-cosine density 2*sqrt(1-mu^2)/pi; axial mean 0, second moment 1/4, P2 mean -1/8.',
        conditional_continuum_moment_coefficients={'P0':0,'P1':'3*perimeter/(16*area)','P2':'45*perimeter/(256*area)'},
        restrictions='This is a chosen angular boundary-trace approximation. No measured heterogeneous side trace is available. Do not treat the volume operator or its coefficients as a qualified native 3D transport law or as an explanation of the CE discrepancy.',
        success='On actual saved SN8 quadrature: isotropic null, weighted scalar conservation, weighted symmetry/positive semidefiniteness, nonpositive off-diagonal entries, positive implicit response. At independently fixed 256-point Gauss-Legendre quadrature: first three continuum projected coefficients agree to 1e-6 relative scale. Four malformed-grid/geometry controls must reject.',
        roundoff_multiplier=128,continuum_check_order=256,continuum_relative_tolerance=1e-6,
        source_law_check='High-order normalized return density has mean zero, second moment 1/4 and P2 mean -1/8 within the same 1e-6 screen.',
        actual_group_basis_policy='All 370 stored common-basis groups; outer sodium row 1 is an explicitly proposed constant trace. Preserve native scalar data and report the range of projected boundary coefficients; no CE-fitted multiplier.',
        wall_seconds=60,threads=1,retries=0,artifact_budget_bytes=24*2**30,min_free_bytes=8*2**30,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        native_transport_launched=False,engineering_thresholds_changed=False,AAA_accuracy_qualified=False))
    print(json.dumps(dict(status='WHITE_TRACE_ALGEBRA_PREDECLARED_PENDING_CE_TERMINAL',declaration=pin(OUT / 'declaration.json')),indent=2))


def check_inputs(expected):
    if digest(OUT / 'declaration.json')!=expected:raise ValueError('declaration changed')
    declaration=json.loads((OUT / 'declaration.json').read_text());verify(declaration['files'])
    native=json.loads((CE / 'AAA/native_result.json').read_text())
    claim=json.loads((CE / 'AAA/run_claim.json').read_text())
    if claim['manifest_sha256']!=declaration['current_reference_manifest']['sha256'] or native['returncode'] is None:
        raise ValueError('current CE has not reached a verified terminal')
    return declaration


def child(expected):
    import numpy as np
    declaration=check_inputs(expected)
    spec=json.loads(Path(declaration['case_spec']['path']).read_text())
    edge=spec['geometry']['hex_edge_cm'];perimeter=6*edge;area=3*np.sqrt(3)/2*edge*edge
    with _open_xsm(PRODUCTION / 'AAA/bootstrap/initial_axial_track.xsm') as tracking:
        mu=vector(tracking,tracking.root,'U','<f4').astype(float)
        weights=vector(tracking,tracking.root,'W','<f4').astype(float)
        areas=vector(tracking,tracking.root,'AREA2D','<f4').astype(float)
        if len(mu)!=8 or len(areas)!=8 or abs(areas.sum()/area-1)>5e-6:
            raise ValueError('actual quadrature or physical area differs from declared AAA')
    matrix=kernel.trace_exchange(mu,weights,perimeter,area)
    symmetric=np.sqrt(weights)[:,None]*matrix/np.sqrt(weights)[None,:]
    norm=np.linalg.norm(matrix,np.inf);tol=declaration['roundoff_multiplier']*np.finfo(float).eps*norm
    null=float(np.max(abs(matrix@np.ones(len(mu)))))
    balance=float(np.max(abs(weights@matrix)))
    symmetry=float(np.max(abs(symmetric-symmetric.T)))
    spectrum=np.linalg.eigvalsh(symmetric)
    off=matrix.copy();np.fill_diagonal(off,0)
    response=np.linalg.solve(np.eye(8)+matrix,np.eye(8))
    if max(null,balance,symmetry)>tol or spectrum.min()<-tol or off.max()>0 or response.min()<-tol:
        raise ValueError('finite white exchange invariant failed')
    high_mu,high_weights=np.polynomial.legendre.leggauss(declaration['continuum_check_order'])
    projected=kernel.legendre_projection(kernel.trace_exchange(high_mu,high_weights,perimeter,area),high_mu,high_weights)
    expected_projection=np.diag([0,3*perimeter/(16*area),45*perimeter/(256*area)])
    error=float(np.max(abs(projected-expected_projection))/np.max(abs(expected_projection)))
    density=kernel.white_return_density(high_mu)
    density_norm=high_weights@density
    observed_return=np.array([high_weights@(density*high_mu),high_weights@(density*high_mu**2),high_weights@(density*(3*high_mu**2-1)/2)])/density_norm
    return_error=float(np.max(abs(observed_return-np.array([0,.25,-.125]))))
    if max(error,return_error)>declaration['continuum_relative_tolerance']:
        raise ValueError('continuum moment/white source-law check failed')
    rejected=0
    for bad_mu,bad_weights,p,a in [(mu,weights,0,area),(mu,weights,perimeter,-area),
        (np.ones(8),weights,perimeter,area),(mu,-weights,perimeter,area)]:
        try:kernel.trace_exchange(bad_mu,bad_weights,p,a)
        except ValueError:rejected+=1
        else:raise ValueError('malformed grid/geometry accepted')
    coefficients=[]
    with _open_xsm(PRODUCTION / 'AAA/bootstrap/basis_reference.xsm') as basis:
        for handle in list_handles(basis,basis.root,'GROUP',370):
            group=basis.directory(handle[0]);mode=vector(basis,group,'POD-NMODE','<i4')
            b=vector(basis,group,'POD-BASIS','<f4').astype(float)
            if mode.tolist()!=[1] or len(b)!=8:raise ValueError('unexpected common rank/region count')
            block=kernel.projected_boundary_block(matrix,b[:1])
            if block.shape!=(1,8,1,8) or not np.isfinite(block).all():raise ValueError('modal trace-block construction failed')
            coefficients.append(b[0]**2*perimeter/(np.pi*area))
    result=dict(classification='PASS_CONDITIONAL_WHITE_TRACE_ANGULAR_ALGEBRA_ONLY',
        finite_SN8=dict(isotropic_null=null,weighted_balance=balance,weighted_symmetry=symmetry,roundoff_bound=tol,
            minimum_weighted_eigenvalue=float(spectrum.min()),minimum_implicit_response=float(response.min()),
            legendre_projection=kernel.legendre_projection(matrix,mu,weights).tolist()),
        high_order_continuum_relative_error=error,observed_white_return_moments=observed_return.tolist(),
        negative_controls_rejected=rejected,groups=370,physical_perimeter_cm=perimeter,physical_area_cm2=area,
        proposed_boundary_trace_row=1,projected_group_prefactor_range=[min(coefficients),max(coefficients)],
        coefficients_fitted_to_CE=False,heterogeneous_boundary_trace_measured=False,native_solver_changed=False,
        AAA_accuracy_qualified=False,ABA_admitted=False,scope=declaration['restrictions'])
    write_new(OUT / 'result.json',result)
    print('AXMAT-WHITE-TRACE-ALGEBRA-COMPLETE')
    print(json.dumps(result,indent=2))


def run(expected):
    declaration=check_inputs(expected)
    if (OUT / 'run_claim.json').exists():raise ValueError('no repeat or retry')
    write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time()))
    resources=DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    runner=SerialExecutor(OUT,60,'AAA',resources)
    runner.execute(OUT / 'AAA','algebra',[sys.executable,str(Path(__file__).resolve()),'child','--sha256',expected],60,'AXMAT-WHITE-TRACE-ALGEBRA-COMPLETE')
    verify(declaration['files'])
    write_new(OUT / 'driver_result.json',dict(status='COMPLETE_BOUNDED_ALGEBRA_ONLY',result=pin(OUT / 'result.json'),
        declaration_sha256=expected,resources=resources.check(),new_native_transport=False,AAA_accuracy_qualified=False))
    print(json.dumps(dict(status='COMPLETE_BOUNDED_ALGEBRA_ONLY',result=pin(OUT / 'result.json')),indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run','child'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else (run(args.sha256) if args.action=='run' else child(args.sha256))
