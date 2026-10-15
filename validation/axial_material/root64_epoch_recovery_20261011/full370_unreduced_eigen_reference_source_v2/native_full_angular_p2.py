"""Full angular source/moment support for a 150-cm, 370-group reference.

This module does not solve an eigenproblem or admit actual material data.
All states (polar, axial sign, planar orientation, original azimuth) survive
until the weighted volume-integral moment accumulation. No POD is involved.

Convention, with angular averages normalized so <1>=1:
  R=(1,y,z,x,sqrt(3)xy,sqrt(3)yz,(3z*z-1)/2,
     sqrt(3)xz,sqrt(3)(x*x-y*y)/2), in (l,m) order.
  phi_lm=<R_lm psi>; q=sum_lm (2l+1) Sigma_l phi_lm R_lm.
  Raw SCAT matrices are [material,l,destination,source].
Source evidence: src/MOCCHR.f:33-37,73-123,137-154 (normalization/full NDIM3);
src/MOCIK3.f:51-77 (parities); independent full physical P2 (2l+1).
FLUSOU.f90 NDIM3 uses rectangular3x3 indices and is not an equivalence proof;
src/MGXEXP.f90:148-168 (raw moments and source/destination).

The original export_native_directional.f90:64-65,72 exports only NDIM2 [1,y,x]
as REAL32. Here complete NDIM3 polynomials use independent REAL64 arithmetic
from saved XMU/azimuth inputs. That is an explicitly extended angular basis,
not a claim of a byte-exact native full-P2 export. Saved REAL32 in-plane values
are retained separately. Geometry uses saved ZMU; XMU is never inferred from
it. Native CPO values are negative half-range representatives, so each real
axial sign is explicitly restored. WEI*WZMU/2 is the extrusion ray measure:
run_native_layered_full_batch.py:62-78, native_layered_full_action.py:12-27.
Neither polar/azimuth weights nor scalar flux are fitted or renormalized.
"""
from dataclasses import dataclass
import re
import numpy as np

GROUPS = 370
FISSION_COMPONENTS = 32
DEGREES = np.array([0,1,1,1,2,2,2,2,2], dtype=int)
CASE_SPEC_SHA256 = 'ac3e67ffdc25f5bfa45bca5170253de8e875c983550e5ee878ee30c5d1a4c2c4'


def _finite(value, name):
    value = np.asarray(value, dtype=float)
    if not np.isfinite(value).all():
        raise ValueError(f'{name} must be finite')
    return value


def real_harmonics_p2(directions):
    """Independent Cartesian real harmonics; directions are not normalized here."""
    direction = _finite(directions, 'directions')
    if direction.ndim != 2 or direction.shape[1] != 3:
        raise ValueError('directions shape (states,3) required')
    norm2 = (direction*direction).sum(axis=1)
    if np.any((norm2 < 1-64*np.finfo(float).eps) | (norm2 > 1+64*np.finfo(float).eps)):
        raise ValueError('unit harmonic directions required; no implicit normalization')
    x,y,z = direction.T
    s = np.sqrt(3.)
    return np.stack([np.ones_like(x),y,z,x,s*x*y,s*y*z,
                     (3*z*z-1)/2,s*x*z,s*(x*x-y*y)/2], axis=1)


@dataclass(frozen=True)
class NativeAngularStates:
    keys: np.ndarray             # [polar, actual z sign, orientation, azimuth]
    directions: np.ndarray       # XMU-based full harmonic direction
    streaming_directions: np.ndarray  # distinct ZMU-based geometric direction
    harmonics: np.ndarray
    xmu: np.ndarray
    zmu: np.ndarray
    wzmu: np.ndarray
    native_in_plane: np.ndarray | None
    azimuth_count: int

    def indices(self, polar, axial_sign, orientation, azimuth):
        p,s,o,a = np.broadcast_arrays(polar, axial_sign, orientation, azimuth)
        for value in (p,s,o,a):
            if not np.isfinite(value).all() or np.any(value != np.floor(value)):
                raise ValueError('integer angular indices required')
        if (np.any((p < 0) | (p >= len(self.xmu))) or
                np.any((a < 0) | (a >= self.azimuth_count)) or
                np.any((s != -1) & (s != 1)) or np.any((o != -1) & (o != 1))):
            raise ValueError('original polar/azimuth and explicit signed directions required')
        return (((p.astype(int)*2+(s == 1))*2+(o == -1))*self.azimuth_count+a).astype(int)

    def ray_weights(self, state_indices, track_weights):
        indices = np.asarray(state_indices)
        weights = _finite(track_weights, 'track weights')
        if (indices.ndim != 1 or indices.dtype.kind not in 'iu' or
                np.any((indices < 0) | (indices >= len(self.keys))) or
                weights.shape != indices.shape or np.any(weights <= 0)):
            raise ValueError('one positive original track weight per retained state required')
        return weights*self.wzmu[self.keys[indices,0]]/2


def angular_states_from_native(xmu, zmu, wzmu, azx, azy, native_in_plane=None):
    """Retain all original angular bins; no material/angle identity admission."""
    xmu,zmu,wzmu,azx,azy = [_finite(v,n).copy() for v,n in
        zip((xmu,zmu,wzmu,azx,azy),('XMU','ZMU','WZMU','azx','azy'))]
    if (xmu.ndim != 1 or not len(xmu) or zmu.shape != xmu.shape or
            wzmu.shape != xmu.shape or azx.ndim != 1 or not len(azx) or azy.shape != azx.shape or
            np.any((xmu <= -1) | (xmu >= 0)) or np.any(zmu <= 1) or np.any(wzmu <= 0)):
        raise ValueError('saved negative half-range XMU, ZMU>1 and positive WZMU required')
    aznorm = azx*azx+azy*azy
    if np.any((aznorm < 1-64*np.finfo(float).eps) | (aznorm > 1+64*np.finfo(float).eps)):
        raise ValueError('saved unit azimuth pairs required; no renormalization')
    in_plane = None
    if native_in_plane is not None:
        in_plane = _finite(native_in_plane, 'native in-plane harmonics').copy()
        sine = np.sqrt(1-xmu*xmu)
        expected = np.stack([np.ones((len(xmu),len(azx))),
            sine[:,None]*azy[None,:],sine[:,None]*azx[None,:]], axis=1).astype('f4')
        if in_plane.shape != expected.shape or not np.array_equal(in_plane.astype('f4'), expected):
            raise ValueError('saved REAL32 [1,y,x] harmonics differ from native XMU/azimuth convention')
    p,s,o,a = np.meshgrid(np.arange(len(xmu)), [-1,1], [1,-1],
                          np.arange(len(azx)), indexing='ij')
    p,s,o,a = [v.ravel() for v in (p,s,o,a)]
    transverse = np.sqrt(1-xmu[p]*xmu[p])
    direction = np.stack([o*transverse*azx[a],o*transverse*azy[a],-s*xmu[p]], axis=1)
    streaming = np.stack([o*azx[a]/zmu[p],o*azy[a]/zmu[p],
                          s*np.sqrt(1-1/(zmu[p]*zmu[p]))], axis=1)
    return NativeAngularStates(np.stack([p,s,o,a],axis=1), direction, streaming,
        real_harmonics_p2(direction), xmu,zmu,wzmu,in_plane,len(azx))


def layer_material_ids(material_A, material_B, case, nz):
    """Explicit 8-region A/B identities over physical [0,50,100,150] zones."""
    if not isinstance(nz, (int,np.integer)) or nz < 3 or nz % 3 or case not in ('AAA','ABA'):
        raise ValueError('AAA/ABA and a complete three-zone axial grid required')
    a,b = [np.asarray(v) for v in (material_A,material_B)]
    if any(v.shape != (8,) or v.dtype.kind not in 'iu' or np.any(v < 0) for v in (a,b)):
        raise ValueError('explicit eight actual material identities for both A and B required')
    result = np.repeat(a[:,None],nz,axis=1)
    if case == 'ABA': result[:,nz//3:2*nz//3] = b[:,None]
    return result


def build_source_coefficients(flux_moments, scatter, material_ids, nusigf, chi, eigenvalue):
    """Full370 support algebra, without asserting actual material qualification.

    flux=(8,nz,370,9), scatter=(materials,3,dest,source),
    nusigf/chi=(materials,32,370). Fission components remain separately returned.
    Self-scatter is included; all signed P1/P2 values and flux moments survive.
    """
    phi,sc,nuf,ch = [_finite(v,n) for v,n in zip(
        (flux_moments,scatter,nusigf,chi),('flux moments','raw scatter','NUSIGF','CHI'))]
    ids = np.asarray(material_ids)
    if (phi.ndim != 4 or phi.shape[0] != 8 or phi.shape[1] < 3 or phi.shape[1] % 3 or
            phi.shape[2:] != (GROUPS,9) or
            ids.shape != phi.shape[:2] or ids.dtype.kind not in 'iu' or
            sc.ndim != 4 or sc.shape[1:] != (3,GROUPS,GROUPS) or
            nuf.shape != (sc.shape[0],FISSION_COMPONENTS,GROUPS) or ch.shape != nuf.shape or
            np.any((ids < 0) | (ids >= sc.shape[0])) or
            not np.isfinite(eigenvalue) or eigenvalue <= 0):
        raise ValueError('complete 8-region/370-group/P2/32-component material contract required')
    flat = phi.reshape(-1,GROUPS,9); output = np.zeros_like(flat)
    rates = np.zeros((len(flat),FISSION_COMPONENTS))
    for material in np.unique(ids):
        locations = np.flatnonzero(ids.ravel() == material)
        for moment,degree in enumerate(DEGREES):
            output[locations,:,moment] = (2*degree+1)*(flat[locations,:,moment]@sc[material,degree].T)
        rates[locations] = flat[locations,:,0]@nuf[material].T
        output[locations,:,0] += rates[locations]@ch[material]/eigenvalue
    return dict(coefficients=output.reshape(phi.shape),
        fission_component_rates=rates.reshape(*phi.shape[:2],FISSION_COMPONENTS),
        status='FULL370_P2_32COMPONENT_SUPPORT_ONLY',full_reference_qualified=False)


def reconstruct_source(coefficients, harmonics):
    coefficient = _finite(coefficients, 'source coefficients')
    harmonic = _finite(harmonics, 'full angular harmonics')
    if (coefficient.ndim != 4 or coefficient.shape[0] != 8 or
            coefficient.shape[2:] != (GROUPS,9) or harmonic.ndim != 2 or harmonic.shape[1] != 9):
        raise ValueError('complete source (8,nz,370,9) and selected full nine-harmonic states required')
    return np.einsum('am,rzgm->arzg', harmonic, coefficient, optimize=True)


def iter_source_chunks(coefficients, states, max_states=8):
    """Bound angular allocation; retain original indices for each kernel call."""
    if not isinstance(max_states, int) or not 1 <= max_states <= 128:
        raise ValueError('explicit angular chunk size 1..128 required')
    for first in range(0,len(states.keys),max_states):
        indices = np.arange(first,min(first+max_states,len(states.keys)))
        yield indices,reconstruct_source(coefficients,states.harmonics[indices])


def source_for_zonal_group(coefficients, states, state_index, group):
    """Unweighted q:(8*nz,1) for transport_zonal, with a local group total.

    The caller retains the same state key when choosing geometric mu,
    orientation and entrance face. All 370 groups use this same interface;
    boundary closure and group-specific total transfer are separate work.
    """
    coefficient = _finite(coefficients, 'complete source coefficients')
    if (coefficient.ndim != 4 or coefficient.shape[0] != 8 or
            coefficient.shape[2:] != (GROUPS,9) or
            not isinstance(state_index,(int,np.integer)) or not 0 <= state_index < len(states.keys) or
            not isinstance(group,(int,np.integer)) or not 0 <= group < GROUPS):
        raise ValueError('complete full370 source and retained state/group index required')
    value = np.einsum('m,rzm->rz',states.harmonics[state_index],coefficient[:,:,group,:])
    return np.ascontiguousarray(value.reshape(8*coefficient.shape[1],1))


class P2MomentAccumulator:
    """Accumulate weighted ray volume integrals before angular states disappear."""
    def __init__(self, states, nz):
        if not isinstance(nz,int) or nz < 3 or nz % 3:
            raise ValueError('complete three-zone axial grid required')
        self.states = states
        self.integrals = np.zeros((8,nz,GROUPS,9))
        self.observed_states = np.zeros(len(states.keys), dtype=bool)

    def add(self, state_indices, regional_integrals, original_track_weights):
        indices = np.asarray(state_indices)
        values = _finite(regional_integrals, 'unweighted regional ray integrals')
        weights = self.states.ray_weights(indices,original_track_weights)
        if values.shape != (len(indices),*self.integrals.shape[:3]):
            raise ValueError('per-state ray integrals shape (states,8,nz,370) required')
        self.integrals += np.einsum('am,a,arzg->rzgm',self.states.harmonics[indices],weights,values,optimize=True)
        self.observed_states[indices] = True

    def flux_moments(self, stored_volume):
        volume = _finite(stored_volume, 'actual stored TRACK cell volumes')
        if volume.shape != self.integrals.shape[:2] or np.any(volume <= 0):
            raise ValueError('positive actual stored cell volumes (8,nz) required')
        if not self.observed_states.all():
            raise ValueError('full angular-bin coverage is incomplete; no scalar-only fallback')
        # This geometric normalization is applied once, with no angle rescaling.
        return self.integrals/volume[:,:,None,None]


class ReferenceInputUnready(ValueError):
    pass


def current150_material_status(evidence):
    """Require explicit external material/context admissions; never infer them."""
    required = ('actual_A_B_raw_transfer','TRANC_semantics','reaction_multiplicity',
                'SPH_MASK_context','complete_angular_input')
    missing = []
    evidence = evidence if isinstance(evidence,dict) else {}
    for name in required:
        item = evidence.get(name,{})
        item = item if isinstance(item,dict) else {}
        if (item.get('status') != 'ADMITTED_ACTUAL_CURRENT150_AB' or
                not isinstance(item.get('path'),str) or not item['path'].startswith('/') or
                not isinstance(item.get('sha256'),str) or
                re.fullmatch('[0-9a-f]{64}',item['sha256']) is None):
            missing.append(name)
    if (evidence.get('groups') != GROUPS or evidence.get('fission_components') != FISSION_COMPONENTS or
            evidence.get('physical_z_edges_cm') != [0,50,100,150] or
            evidence.get('case_spec_sha256') != CASE_SPEC_SHA256):
        missing.append('original_current150_case_contract')
    return dict(status='UNREADY',missing=[*missing,'authoritative_context_verification'],
        declared_admissions_complete=not missing,full_reference_qualified=False,
        evidence_verification='An authoritative adapter must verify receipts and bind these exact input arrays; this algebra does not certify receipts.')


def current150_source_coefficients(*args, evidence=None, verify_admissions=None, **kwargs):
    """Actual-data route requires an external authoritative array/context binder.

    verify_admissions(evidence, args, kwargs) must verify the named receipts,
    actual array identities and TRANC/reaction/SPH/MASK/angular semantics.
    No shape-only or caller-declared metadata can silently admit actual data.
    """
    status = current150_material_status(evidence)
    missing = [name for name in status['missing'] if name != 'authoritative_context_verification']
    if missing or not callable(verify_admissions):
        raise ReferenceInputUnready('UNREADY: '+', '.join(status['missing']))
    if verify_admissions(evidence,args,kwargs) is not True:
        raise ReferenceInputUnready('UNREADY: authoritative actual array/context verification failed')
    result = build_source_coefficients(*args,**kwargs)
    status.update(status='EXTERNALLY_VERIFIED_COMPONENT_INPUT_ONLY',missing=[])
    result['material_status'] = status
    return result
