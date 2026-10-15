"""Stream every original ray into a full NDIM3 moment action, without POD.

This candidate composes actual fixed-source C++ ABIs, complete layer-local
white closure and all nine moments. It is NOT an admitted formal-case kernel.
H150/Nz48/SN32/current material/angular authority, model equivalence and actual
cost remain explicit prerequisites. The offset quadrature order is separate
from formal SPOT's SN32, and must never be described as that SN32 quadrature.
"""
from pathlib import Path
from collections import OrderedDict
import ctypes
import numpy as np
from scipy.linalg import lu_factor, lu_solve
from native_layered_multigroup import transport_multigroup, _quadrature
from native_layered_transport import aggregate
from full370_unreduced_eigen import ReferenceFailure, ReferenceUnready, finite

NR, NZ, NG, NMOM, NTRACK = 8, 48, 370, 9, 11364
NWHITE, ACTIONS = 6*NZ, NTRACK*4*2*2


class WholeRayOperator:
    """Actual streaming implementation, with one <=4-group LU working block.

    No cached angular outputs or full dense multigroup inverse are retained.
    All370 groups share each actual geometry construction. One ray's full
    transport fields occupy at most720*9*370*8 bytes, not a full angular
    history. White preparation uses one full group transfer plus compact
    per-ray face buffers, and never allocates a second full transfer matrix.
    White matrices are isolated per group in fresh output storage, then a
    small block is loaded/factored at each action. Saved captures do
    not supply any angular unknown. No actual library is loaded until the
    concrete KernelBinding verifies its full Source/object origin.
    """
    def __init__(self, library, ray_inventory, angular_states, totals64,
                 volume64, cache_root, offset_order, group_chunk, checks,
                 boundary_model, stored_surface64, budget, kernel_binding):
        from current_formal_input_authority import KernelBinding
        if type(kernel_binding) is not KernelBinding:
            raise ReferenceUnready('concrete current full Source/object kernel binding')
        kernel_binding.verify(library)
        self.kernel_binding = kernel_binding
        if type(group_chunk) is not int or not 1 <= group_chunk <= 4:
            raise ReferenceUnready('explicit working group chunk1..4')
        if type(offset_order) is not int or offset_order not in (16, 32):
            raise ReferenceUnready('independently frozen offset order16/32, not SN32')
        for name, original_max in (
                ('primitive', 1e-10), ('cell', 1e-10), ('global', 1e-10),
                ('geometry', 5e-12), ('represented_width', 5e-12), ('white', 5e-12)):
            value = checks[name]
            if type(value) is not float or not np.isfinite(value) or not 0 < value <= original_max:
                raise ReferenceUnready('original strict physical check ceiling: ' + name)
        if boundary_model not in ('GEOMETRIC_LAYER_LOCAL_WHITE', 'STORED_NATIVE_LAYER_LOCAL_WHITE'):
            raise ReferenceUnready('mandatory declared boundary model, no fitted normalizer')
        self.library = Path(library); self.ray_inventory = ray_inventory
        self.rays = ray_inventory['tracks']
        self.states = angular_states; self.total = finite(totals64, (NR, NZ, NG), 'all group totals')
        self.volume = finite(volume64, (NR, NZ), 'stored physical cell volumes')
        self.cache = Path(cache_root); self.order = offset_order
        self.chunk = group_chunk; self.checks = checks; self.budget = budget
        self.boundary_model = boundary_model
        self.stored_surface = finite(stored_surface64, (6, NZ), 'stored native surface/layer measure')
        if (len(self.rays) != NTRACK or len(self.states.xmu) != 4 or
            self.states.azimuth_count != 96 or len(self.states.keys) != 4*2*2*96 or
            np.any(self.total < 0) or np.any(self.volume <= 0) or np.any(self.stored_surface <= 0)):
            raise ReferenceUnready('complete current original tracks/angular states/physical measures')
        if self.cache.exists() or self.cache.is_symlink():
            raise ReferenceFailure('fresh private reference cache, once, no retry')
        self.cache.mkdir()
        self.prepared = False; self.denominator = None
        self.operator_calls = 0

    def chunks(self):
        for first in range(0, NG, self.chunk):
            yield first, min(first+self.chunk, NG)

    def actions(self):
        # Each track's saved angle ALREADY selects its one original azimuth.
        # Never place an additional range(96) loop around these actions.
        count = 0
        observed = np.zeros(len(self.states.keys), dtype=np.int64)
        self.budget.white_observed(observed)
        for original, ray in enumerate(self.rays):
            if ray['original_track'] != original:
                raise ReferenceFailure('original ray indices/order altered')
            angle = ray['angle']
            for polar in range(4):
                widths = np.ascontiguousarray(ray['planar_widths'] * self.states.zmu[polar])
                for sign in (-1, 1):
                    mu = sign*np.sqrt(1-1/self.states.zmu[polar]**2)
                    for orientation in (1, -1):
                        state = int(self.states.indices(polar, sign, orientation, angle))
                        entry, exit_surface = ray['entry_surface'], ray['exit_surface']
                        if orientation == -1:
                            entry, exit_surface = exit_surface, entry
                        weight = float(ray['weight'] * self.states.wzmu[polar] / 2)
                        if not np.isfinite(weight) or weight <= 0:
                            raise ReferenceFailure('original positive unfitted WEI*WZMU/2')
                        count += 1; observed[state] += 1
                        self.budget.check()
                        yield ray, widths, mu, orientation, entry, exit_surface, weight, state
        if count != ACTIONS or np.any(observed == 0):
            raise ReferenceFailure('full181824 actual actions and every native angular bin')

    def prepare_white(self):
        if self.prepared:
            raise ReferenceFailure('white preparation is exactly once')
        self.budget.white_baseline()
        T = np.zeros((NWHITE, NWHITE, NG))
        L = np.zeros((2, NR, NWHITE, NG)); D = np.zeros(NWHITE)
        total = np.ascontiguousarray(self.total)
        nodes, weights = _quadrature(self.order)
        function = ctypes.CDLL(str(self.library)).layered_white_accumulate370
        pointer = ctypes.c_void_p
        function.argtypes = ([ctypes.c_int]*3 + [pointer]*3 + [ctypes.c_int]*2 +
            [ctypes.c_double]*2 + [ctypes.c_int]*2 + [pointer]*2 +
            [ctypes.c_double] + [pointer]*4)
        function.restype = ctypes.c_int
        self.budget.white_arrays(T, L, D, total, total is self.total, nodes, weights)
        count = 0
        for ray, widths, mu, orientation, entry, exit_surface, weight, state in self.actions():
            regions = np.ascontiguousarray(ray['regions'], dtype=np.int32)
            geometry = np.zeros(6)
            self.budget.white_native_before(count, ray, state, self.states.keys[state], widths, regions, geometry)
            rc = function(len(widths), NZ, NG, widths.ctypes.data,
                regions.ctypes.data, total.ctypes.data, entry, exit_surface,
                150.0, mu, orientation, self.order, nodes.ctypes.data,
                weights.ctypes.data, weight, geometry.ctypes.data,
                T.ctypes.data, L.ctypes.data, D.ctypes.data)
            self.budget.white_native_after(count, rc, geometry)
            if rc:
                raise ReferenceFailure('actual full370 white accumulator code '+str(rc))
            count += 1; self.budget.check()
        if (count != ACTIONS or np.any(D <= 0) or not np.isfinite(D).all() or
            not np.isfinite(T).all() or not np.isfinite(L).all() or
            np.any(T < 0) or np.any(L < 0)):
            raise ReferenceFailure('whole original nonzero incoming white measure/transfer')
        denominator = D if self.boundary_model == 'GEOMETRIC_LAYER_LOCAL_WHITE' else self.stored_surface.ravel()
        for group in range(NG):
            np.savez(self.cache/f'white_g{group+1:04d}.npz',
                     transfer=T[:, :, group], leakage=L[:, :, :, group],
                     denominator=denominator, geometric_incoming=D)
            self.budget.check()
        self.denominator = D.copy()
        del T, L, D
        self.prepared = True

    def _one_sweep(self, coefficients, first, stop, amplitudes):
        k = stop-first
        moments = np.zeros((NR, NZ, k, NMOM))
        outgoing = np.zeros((6, NZ, k)); axial = np.zeros((2, NR, k))
        totals = np.ascontiguousarray(self.total[:, :, first:stop])
        ledger = np.zeros((k, 6))
        minimum_angle = minimum_integral = np.inf
        calls = 0
        # Source coefficients are constant throughout this sweep. A bounded
        # 16-state LRU retains the exact same einsum result across same-angle
        # tracks, without reordering one ray or one accumulation. At full370
        # each entry is 384*370*8=1136640 bytes; all16 total18186240 bytes.
        # Every sweep gets a fresh cache; no prior iterate can be reused.
        source_cache = OrderedDict()
        zero_axial = np.zeros((NR, k))
        for ray, widths, mu, orientation, entry, exit_surface, weight, state in self.actions():
            harmonic = self.states.harmonics[state]
            q = source_cache.pop(state, None)
            if q is None:
                if len(source_cache) == 16:
                    source_cache.popitem(last=False)
                q = np.ascontiguousarray(np.einsum('m,rzgm->rzg', harmonic,
                    coefficients[:, :, first:stop, :]).reshape(NR*NZ, k))
            source_cache[state] = q
            if sum(value.nbytes for value in source_cache.values()) > 16*NR*NZ*k*8:
                raise ReferenceFailure('bounded exact source state cache')
            response = transport_multigroup(self.library, widths, ray['regions'],
                totals, entry, 150.0, NZ, mu, orientation, self.order,
                q, amplitudes, zero_axial)
            geometric, fields, metrics = response['geometry'], response['fields'], response['metrics']
            if (geometric[3] > self.checks['geometry'] or
                geometric[5] > self.checks['represented_width'] or
                np.max(metrics[:, 2]) > self.checks['primitive'] or
                np.max(metrics[:, 12]) > self.checks['cell'] or
                np.any(metrics[:, 26] != 0)):
                raise ReferenceFailure('original primitive/cell/geometry/shared-face gate')
            values = aggregate(fields, ray['regions'], NZ, orientation, exit_surface)
            moments += weight*values['volume'][..., None]*harmonic
            outgoing += weight*values['radial']; axial += weight*values['axial']
            ledger += weight*metrics[:, 20:26]
            minimum_angle = min(minimum_angle, float(np.min(metrics[:, 0])))
            minimum_integral = min(minimum_integral, float(np.min(metrics[:, 1])))
            calls += 1; self.budget.check()
        source_cache.clear()
        if calls != ACTIONS or not np.isfinite(moments).all():
            raise ReferenceFailure('complete actual angular sweep coverage/finite moments')
        return dict(moments=moments, outgoing=outgoing, axial=axial,
                    ledger=ledger, minimum_angle=minimum_angle,
                    minimum_integral=minimum_integral, calls=calls)

    def apply(self, coefficients):
        finite(coefficients, (NR, NZ, NG, NMOM), 'complete signed input source')
        if not self.prepared:
            raise ReferenceUnready('complete current white transfer not actually prepared')
        # Full370 volume actions share geometry; only LU/IO use small groups.
        vacuum_action = self._one_sweep(coefficients, 0, NG, np.zeros((NWHITE, NG)))
        amplitudes = np.empty((NWHITE, NG)); denominators = np.empty((NWHITE, NG))
        predicted_axial = np.empty((2, NR, NG)); all_white_residual = np.zeros(NG)
        for first, stop in self.chunks():
            for group in range(first, stop):
                with np.load(self.cache/f'white_g{group+1:04d}.npz', allow_pickle=False) as saved:
                    T = saved['transfer']; L = saved['leakage']; D = saved['denominator']
                matrix = np.diag(D)-T
                rhs = vacuum_action['outgoing'][:, :, group].ravel()
                lu, piv = lu_factor(matrix, check_finite=True)
                solution = lu_solve((lu, piv), rhs, check_finite=True)
                residual = matrix@solution-rhs
                scale = np.max(np.abs(rhs))
                if scale == 0:
                    error = 0.0 if np.all(residual == 0) else np.inf
                else:
                    error = float(np.max(np.abs(residual))/scale)
                if not np.isfinite(solution).all() or error > self.checks['white']:
                    raise ReferenceFailure('actual full layer-local white matrix solve')
                amplitudes[:, group] = solution; denominators[:, group] = D
                predicted_axial[:, :, group] = vacuum_action['axial'][:, :, group] + np.einsum('sri,i->sr', L, solution)
                all_white_residual[group] = error
            self.budget.check()
        closed = self._one_sweep(coefficients, 0, NG, amplitudes)
        closure = closed['outgoing'].reshape(NWHITE, NG)-denominators*amplitudes
        scale = np.max(np.abs(closed['outgoing']), axis=(0, 1))
        relative = np.zeros(NG)
        np.divide(np.max(np.abs(closure), axis=0), scale, out=relative, where=scale != 0)
        relative[(scale == 0) & np.any(closure != 0, axis=0)] = np.inf
        if np.any(relative > self.checks['white']):
            raise ReferenceFailure('actual full local surface/layer white closure')
        axial_defect = closed['axial']-predicted_axial
        scale = np.max(np.abs(closed['axial']), axis=(0, 1))
        axial_error = np.zeros(NG)
        np.divide(np.max(np.abs(axial_defect), axis=(0, 1)), scale,
                  out=axial_error, where=scale != 0)
        axial_error[(scale == 0) & np.any(axial_defect != 0, axis=(0, 1))] = np.inf
        if np.any(axial_error > self.checks['white']):
            raise ReferenceFailure('independent full axial source/return assembly')
        # Geometric and stored normalizers stay distinct; neither is fitted.
        scale = closed['ledger'][:, 5]
        relative = np.zeros(NG)
        np.divide(np.abs(closed['ledger'][:, 4]), scale, out=relative, where=scale != 0)
        relative[(scale == 0) & (closed['ledger'][:, 4] != 0)] = np.inf
        if np.any(relative > self.checks['global']):
            raise ReferenceFailure('actual raw whole-track signed conservation')
        calls = vacuum_action['calls']+closed['calls']; self.budget.check()
        self.operator_calls += 1
        self.kernel_binding.verify(self.library)
        # Whole-track conservation includes radial inflow/outflow. The physical
        # vacuum/white problem additionally requires zero radial net loss;
        # stored and geometric normalizers may disagree and are reported as
        # different models. No fitted factor hides that discrepancy.
        physical_defect = (closed['ledger'][:, 0]-closed['ledger'][:, 3]
                           -closed['axial'].sum(axis=(0, 1)))
        physical_scale = np.abs(closed['ledger'][:, 0])
        physical_relative = np.zeros(NG)
        np.divide(np.abs(physical_defect), physical_scale,
                  out=physical_relative, where=physical_scale != 0)
        physical_relative[(physical_scale == 0) & (physical_defect != 0)] = np.inf
        return dict(moments64=closed['moments']/self.volume[:, :, None, None],
                    radial_outgoing_current64=closed['outgoing'],
                    axial_outgoing_current64=closed['axial'], whole_track_ledger64=closed['ledger'],
                    unfitted_physical_white_defect64=physical_defect,
                    unfitted_physical_white_relative64=physical_relative,
                    white_matrix_residual_relative64=all_white_residual,
                    white_closure_defect64=closure.reshape(6, NZ, NG),
                    axial_source_return_assembly_relative64=axial_error,
                    minimum_angular_flux64=closed['minimum_angle'],
                    minimum_angular_integral64=closed['minimum_integral'],
                    complete_coverage=calls == 2*ACTIONS,
                    action_calls=calls, actions_per_complete_group_sweep=ACTIONS,
                    azimuth_already_in_original_track=True, extra_times96_factor=False,
                    boundary_model=self.boundary_model, groups=NG,
                    original_tracks=NTRACK, angular_states=len(self.states.keys),
                    full_reference_qualified=False, AAA_qualified=False, ABA_admitted=False)
