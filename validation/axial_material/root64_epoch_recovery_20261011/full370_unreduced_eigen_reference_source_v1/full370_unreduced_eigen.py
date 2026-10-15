"""Complete, unqualified full-space eigeniteration candidate; never a POD solve.

No actual-data entry is admitted by array shapes or by a caller's status label.
The authoritative material/angular/geometry adapter remains a separate explicit
dependency. Six absent captured moments are not read or completed here: all nine
unknown moments evolve from independent full angular sweeps.
"""
from dataclasses import dataclass
import resource
import sys
import time
import numpy as np

NG, NR, NZ, NMOM, NF = 370, 8, 48, 9, 32
DEGREES = np.array([0, 1, 1, 1, 2, 2, 2, 2, 2], dtype=np.int32)
FORMAL_CASE_SHA = 'fbe3362e16c19c93b87de2ebf67607c5ac0a579daa1f7af5891aae9c9faa7b16'


class ReferenceUnready(RuntimeError):
    pass


class ReferenceFailure(RuntimeError):
    pass


class Budget:
    """In-child checkpoints supplement the original own-child RSS supervisor.

    These checks do not replace the owning host's whole1800, history96GiB,
    initial fresh2GiB, cold20971764748+64MiB, free8GiB and single-child checks.
    """
    def __init__(self):
        self.started = time.monotonic()

    def check(self):
        peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak_bytes = peak if sys.platform == 'darwin' else peak * 1024
        elapsed = time.monotonic() - self.started
        if elapsed >= 600 or peak_bytes >= 512 * 2**20:
            raise ReferenceFailure('original numerical child600s/512MiB cap')
        return dict(seconds=elapsed, peak_bytes=peak_bytes)


@dataclass(frozen=True)
class Controls:
    # All science tolerances/iteration caps are mandatory externally frozen
    # inputs. There is deliberately no new guessed default or relaxed fallback.
    max_outer: int
    max_inner: int
    inner_relative: float
    flux_relative: float
    keff_relative: float
    eigen_relative: float
    normalization_absolute: float

    def validate(self):
        for name in ('max_outer', 'max_inner'):
            if type(getattr(self, name)) is not int or getattr(self, name) < 1:
                raise ReferenceUnready('mandatory predeclared integer cap: ' + name)
        for name in ('inner_relative', 'flux_relative', 'keff_relative',
                     'eigen_relative', 'normalization_absolute'):
            value = getattr(self, name)
            if type(value) is not float or not np.isfinite(value) or value <= 0:
                raise ReferenceUnready('mandatory predeclared science tolerance: ' + name)


def finite(value, shape, name):
    value = np.asarray(value)
    if value.dtype != np.dtype('float64') or value.shape != shape or not np.isfinite(value).all():
        raise ReferenceFailure('complete finite REAL64 ' + name)
    return value


def fission_rates(phi, nuf, ids):
    """All 32 isotope/spectrum slots; no CHI sum assumed to equal one."""
    finite(phi, (NR, NZ, NG, NMOM), 'nine moments')
    flat = phi[..., 0].reshape(NR*NZ, NG)
    rates = np.zeros((NR*NZ, NF), dtype=np.float64)
    for material in np.unique(ids):
        locations = np.flatnonzero(ids.ravel() == material)
        rates[locations] = flat[locations] @ nuf[material].T
    if not np.isfinite(rates).all():
        raise ReferenceFailure('nonfinite independent component fission rates')
    return rates.reshape(NR, NZ, NF)


def production(phi, nuf, ids, volume):
    rates = fission_rates(phi, nuf, ids)
    total = float(np.sum(rates * volume[..., None], dtype=np.float64))
    if not np.isfinite(total) or total <= 0:
        raise ReferenceFailure('finite positive whole-domain nu-fission integral')
    return total, rates


def source_coefficients(phi, scatter, nuf, chi, ids, k, frozen_fission=None):
    """Signed raw full P0/P1/P2, including every within/off-group transfer.

    This is the NDIM3 nine-harmonic convention of MOCCHR/FLUSOU. It does
    not substitute SPOT NDIM1's different off-group angular normalization.
    """
    finite(phi, (NR, NZ, NG, NMOM), 'nine moments')
    if not np.isfinite(k) or k <= 0:
        raise ReferenceFailure('finite positive eigenvalue')
    flat = phi.reshape(NR*NZ, NG, NMOM)
    coefficients = np.zeros_like(flat)
    rates = fission_rates(phi, nuf, ids) if frozen_fission is None else finite(
        frozen_fission, (NR, NZ, NF), 'frozen outer fission source')
    rates = rates.reshape(NR*NZ, NF)
    for material in np.unique(ids):
        locations = np.flatnonzero(ids.ravel() == material)
        for moment, degree in enumerate(DEGREES):
            coefficients[locations, :, moment] = (2*int(degree)+1) * (
                flat[locations, :, moment] @ scatter[material, degree].T)
        coefficients[locations, :, 0] += rates[locations] @ chi[material] / k
    return finite(coefficients.reshape(phi.shape), phi.shape, 'signed full source')


def relative_by_group(defect, reference):
    """No denominator floor; exact zero has an explicit mathematical branch."""
    shape = (NR, NZ, NG, NMOM)
    finite(defect, shape, 'full residual')
    finite(reference, shape, 'full residual reference')
    numerator = np.max(np.abs(defect), axis=(0, 1, 3))
    denominator = np.max(np.abs(reference), axis=(0, 1, 3))
    out = np.zeros(NG, dtype=np.float64)
    np.divide(numerator, denominator, out=out, where=denominator != 0)
    out[(denominator == 0) & (numerator != 0)] = np.inf
    return out


def solve_full370(model, operator, controls, initial_moments, initial_k,
                  budget):
    """Nested exact-source iteration, whole nu-fission normalization and recheck.

    The fixed-source inner iteration solves Phi=T(S Phi+F Phi_old/k_old).
    The outer update k_new=k_old*N(Phi)/N(Phi_old) is followed by ONE global
    normalization of every moment. A fresh complete T(S Phi+F Phi/k) recheck
    gates the returned state. There is no clipping, damping, rank reduction,
    fitted return, selected alternative eigenmode or retry on failure.
    """
    controls.validate()
    from current_formal_input_authority import FormalBinding
    authority = model.get('binding')
    if type(authority) is not FormalBinding:
        raise ReferenceUnready('concrete full current files and material/context authority')
    authority.verify_model(model, controls)
    ids = np.asarray(model['material_ids'])
    scatter = np.asarray(model['scatter64']); nuf = np.asarray(model['nusigf64'])
    chi = np.asarray(model['chi64']); volume = np.asarray(model['volume64'])
    if (ids.dtype.kind not in 'iu' or ids.shape != (NR, NZ) or
        scatter.ndim != 4 or scatter.shape[1:] != (3, NG, NG) or
        np.any(ids < 0) or np.any(ids >= scatter.shape[0])):
        raise ReferenceUnready('complete original material/region/layer identities')
    finite(scatter, scatter.shape, 'raw scatter')
    finite(nuf, (scatter.shape[0], NF, NG), 'all nu-fission slots')
    finite(chi, nuf.shape, 'all original component spectra')
    finite(volume, (NR, NZ), 'stored physical cell volume')
    if (np.any(volume <= 0) or np.any(scatter[:, 0] < 0) or
        np.any(nuf < 0) or np.any(chi < 0)):
        raise ReferenceFailure('original nonnegative P0/fission/positive volume')
    phi = finite(initial_moments, (NR, NZ, NG, NMOM), 'independent initial full angular ansatz').copy()
    if np.any(phi[..., 0] <= 0) or not np.isfinite(initial_k) or initial_k <= 0:
        raise ReferenceFailure('positive starting scalar flux/eigenvalue')
    k = float(initial_k)
    norm, rates = production(phi, nuf, ids, volume)
    phi /= norm
    history = []
    for outer in range(1, controls.max_outer+1):
        budget.check()
        old = phi.copy(); old_k = k
        old_norm, frozen = production(old, nuf, ids, volume)
        for inner in range(1, controls.max_inner+1):
            coefficients = source_coefficients(phi, scatter, nuf, chi, ids, old_k, frozen)
            action = operator.apply(coefficients)
            new = finite(action['moments64'], old.shape, 'all actual full angular moments')
            inner_error = float(np.max(relative_by_group(new-phi, new)))
            phi = new
            budget.check()
            if inner_error <= controls.inner_relative:
                break
        else:
            raise ReferenceFailure('full fixed-fission solve exceeded original predeclared cap')
        norm, rates = production(phi, nuf, ids, volume)
        k = old_k * norm / old_norm
        if not np.isfinite(k) or k <= 0:
            raise ReferenceFailure('nonfinite/nonpositive eigenvalue update')
        phi = phi / norm
        coefficients = source_coefficients(phi, scatter, nuf, chi, ids, k)
        # Actual complete residual for THIS normalized Phi/k, not its next iterate.
        terminal = operator.apply(coefficients)
        mapped = finite(terminal['moments64'], phi.shape, 'fresh full residual sweep')
        by_group = relative_by_group(mapped-phi, phi)
        flux_error = float(np.max(relative_by_group(phi-old, phi)))
        k_error = abs(k-old_k)/k
        norm_now, terminal_rates = production(phi, nuf, ids, volume)
        normalization_error = abs(norm_now-1.0)
        row = dict(outer=outer, inner=inner, inner_relative=inner_error,
                   flux_relative=flux_error, keff_relative=k_error,
                   eigen_relative=float(np.max(by_group)),
                   normalization_absolute=normalization_error)
        history.append(row); budget.check()
        if (row['flux_relative'] <= controls.flux_relative and
            row['keff_relative'] <= controls.keff_relative and
            row['eigen_relative'] <= controls.eigen_relative and
            normalization_error <= controls.normalization_absolute):
            if (np.any(phi[..., 0] <= 0) or
                terminal['minimum_angular_flux64'] < 0 or
                terminal['minimum_angular_integral64'] < 0 or
                not terminal['complete_coverage']):
                raise ReferenceFailure('candidate failed strict full angular/scalar survival')
            authority.verify_model(model, controls)
            # Distinct isotope/spectrum rates and original CHI birth survive.
            return dict(classification='COMPLETE_UNQUALIFIED_FULL370_NDIM3_EIGEN_CANDIDATE',
                        flux_moments64=phi, source_coefficients64=coefficients,
                        nu_fission_component_rates64=terminal_rates,
                        nu_fission_integral64=norm_now, keff64=k,
                        full_residual_by_group64=by_group, history=history,
                        actual_terminal_transport=terminal,
                        inherited_rank=1, reference_POD_rank=None, reduction_used=False,
                        groups=NG, axial_cells=NZ, retained_moments=NMOM,
                        observed_six_missing_capture_moments_used=False,
                        dominant_mode_uniqueness_qualified=False,
                        angular_mesh_error_qualified=False,
                        physical_reaction_balance_qualified=False,
                        full_reference_qualified=False, AAA_qualified=False,
                        ABA_admitted=False, goal_complete=False)
    raise ReferenceFailure('full eigeniteration exceeded original predeclared outer cap')
