"""Record a source-level boundary/coupling distinction, not error attribution."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
NATIVE=Path('/Users/wen/openmc-workspace/src')


def main():
    paths=[NATIVE/'src/boundary_condition.cpp',NATIVE/'src/surface.cpp',ROOT/'src/SPOT1P64.f90',
        ROOT/'validation/iterative/native_layered_full_result.md',ROOT/'validation/iterative/native_oblique_physical_boundary_contract.md',Path(__file__).resolve()]
    commit=subprocess.check_output(['git','-C',str(NATIVE),'rev-parse','HEAD'],text=True).strip()
    if commit!='e542b2f035e397a647cc3ad0ae39946b1ad81e7b':raise ValueError('native source identity changed')
    if subprocess.check_output(['git','-C',str(NATIVE),'diff','HEAD','--','src/boundary_condition.cpp','src/surface.cpp'],text=True):
        raise ValueError('native boundary source changed')
    axial=(ROOT/'src/SPOT1P64.f90').read_text()
    if 'kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)' not in axial:
        raise ValueError('axial transverse P0 source anchor changed')
    review=dict(schema='AXMAT_AAA_WHITE_AXIAL_SOURCE_SCOPE_REVIEW_V1',status='SOURCE_DISTINCTION_RECORDED',native_commit=commit,
        files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        CE_boundary='WhiteBC calls diffuse_reflect; that method samples cosine-weighted normal direction and uniform azimuth, including axial direction for a vertical hexagonal side.',
        axial_transverse='The axial discrete matrix adds the saved radial coefficient through mn(in,1)*radial_m*dn(1,jn), a P0 scalar coupling. It does not explicitly include the same surface/layer/angular white-return operator.',
        previous_native_reference='The separately qualified layered fixed-source reference explicitly mixes polar and axial signs at each surface/layer. Its frozen scope is groups 51/61/98 and small axial grids; it does not qualify a 370-group scattering/fission eigenproblem or this AAA control.',
        hypothesis='An explicit white-return angular operator is a justified next controlled comparison after source adequacy and the independent one-factor axial diagnostics. Do not infer that this distinction quantitatively explains the observed gap.',
        confirmed_cause=False,physical_error_attribution_available=False,new_transport_started=False,
        shared_runtime_changed=False,original_boundary_changed=False,threshold_changed=False)
    out=ROOT/'validation/artifacts/axial-material-ce-qualified-AAA-ufs-20261004/white_axial_source_scope_review.json'
    with out.open('x') as stream:json.dump(review,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest())))


if __name__=='__main__':main()
