"""Six physical white-transfer component controls; Source only until owner runs.

No compiler is invoked here. Three saved provider arguments make the exported
old ABIs and unchanged multigroup action directly reviewable.
"""
import argparse
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path
import sys
import time
import unittest
import numpy as np
from numpy.polynomial.legendre import leggauss
from native_layered_white_transfer import white_radial_transfer
from native_layered_multigroup import transport_multigroup
from native_layered_zonal import transport_zonal
from native_layered_transport import transport

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument('--library', type=Path, required=True)
PARSER.add_argument('--multigroup-library', type=Path, required=True)
PARSER.add_argument('--old-library', type=Path, required=True)
PARSER.add_argument('--report', type=Path, required=True)
ARGS, REMAINING = PARSER.parse_known_args()
sys.argv = [sys.argv[0], *REMAINING]
LIB = ARGS.library.resolve(); MULTI = ARGS.multigroup_library.resolve()
OLD = ARGS.old_library.resolve(); OBSERVATIONS = []


def fixture(nz=3, k=370, profile='AAA'):
    region, group = np.arange(8)[:, None], np.arange(k)[None, :]
    total = np.repeat((.002+(region+1)*.0003+group*.000001)[:, None, :], nz, axis=1)
    if profile == 'ABA':
        total[:, nz//3:2*nz//3] = (.006+(region+1)*.0002+group*.000002)[:, None, :]
    total[:, :, 0] = 0.
    if k > 1: total[:, :, 1] = 1e-12
    return total


def surfaces(orientation):
    return (1, 4) if orientation == 1 else (4, 1)


class DecimalWhiteReference:
    """Independent rectangle intersections and literal exp of optical length.

    No native geometry, native characteristic coefficients or saved matrix is
    used. All original binary64 coordinates are accumulated at decimal50.
    """
    def __init__(self, widths, regions, total, entry, exit_surface, H, nz, mu, orientation):
        self.total, self.regions = total, regions
        self.entry, self.exit = entry, exit_surface
        self.nz, self.mu, self.k = nz, mu, total.shape[-1]
        with localcontext() as ctx:
            ctx.prec = 50; D = Decimal.from_float
            x = [Decimal(0)]
            for width in widths: x.append(x[-1]+D(float(width)))
            z = [D(float(H))*j/nz for j in range(nz+1)]
            self.dm = D(float(mu)); self.rectangles = []
            for i, r in enumerate(regions):
                lo, hi = (x[i], x[i+1]) if orientation == 1 else (x[-1]-x[i+1], x[-1]-x[i])
                for j in range(nz): self.rectangles.append((lo, hi, z[j], z[j+1], int(r), j))
            self.breaks = sorted({zz-self.dm*xx for lo, hi, _, _, _, _ in self.rectangles
                                  for zz in z for xx in (lo, hi)})

    def path(self, offset):
        with localcontext() as ctx:
            ctx.prec = 50
            u = offset if isinstance(offset, Decimal) else Decimal.from_float(float(offset))
            cuts = []
            for lo, hi, za, zb, r, j in self.rectangles:
                va, vb = (za-u)/self.dm, (zb-u)/self.dm
                start, end = max(lo, min(va, vb)), min(hi, max(va, vb))
                if end > start: cuts.append((start, end, r, j, start == lo, end == hi))
            return sorted(cuts)

    def ray(self, offset):
        n = 6*self.nz
        t = np.zeros((n, n, self.k)); leak = np.zeros((2, 8, n, self.k)); d = np.zeros(n)
        path = self.path(offset)
        if not path or not path[0][4]: return t, leak, d
        column = self.entry*self.nz+path[0][3]; d[column] = 1.
        with localcontext() as ctx:
            ctx.prec = 50
            atten = np.array([math.exp(-math.fsum(float(b-a)*self.total[r, j, c]
                               for a, b, r, j, _, _ in path)) for c in range(self.k)])
        _, _, r, j, _, radial = path[-1]
        if radial: t[self.exit*self.nz+j, column] = atten
        else: leak[1 if self.mu > 0 else 0, r, column] = atten
        return t, leak, d

    def fixed(self, order):
        gn, gw = leggauss(order)
        n = 6*self.nz
        result = [np.zeros((n, n, self.k)), np.zeros((2, 8, n, self.k)), np.zeros(n)]
        with localcontext() as ctx:
            ctx.prec = 50
            for a, b in zip(self.breaks[:-1], self.breaks[1:]):
                for node, weight in zip(gn, gw):
                    offset = (a+b)/2+(b-a)*Decimal.from_float(float(node))/2
                    scalar = float((b-a)*Decimal.from_float(float(weight))/2)
                    for out, value in zip(result, self.ray(offset)): out += scalar*value
        return result


def boundary_currents(result, regions, nz, mu, orientation, exit_surface):
    cells = result['fields'].reshape(len(regions), nz, 9, -1); k = cells.shape[-1]
    radial = np.zeros((6*nz, k)); leak = np.zeros((2, 8, k))
    outer, face = (len(regions)-1, 6) if orientation == 1 else (0, 5)
    radial[exit_surface*nz:(exit_surface+1)*nz] = cells[outer, :, face]
    side, layer, field = (1, nz-1, 8) if mu > 0 else (0, 0, 7)
    for i, region in enumerate(regions): leak[side, region] += cells[i, layer, field]
    return radial, leak


class WhiteTransferTests(unittest.TestCase):
    def assert_arrays(self, actual, expected, rtol=5e-12, atol=1e-14):
        for name, value in zip(('transfer', 'leakage', 'incoming'), expected):
            np.testing.assert_allclose(actual[name], value, rtol=rtol, atol=atol)

    def test_independent_literal_optical_path_and_full_integrals(self):
        H, nz = 150., 3; widths, regions = [170., 230.], [0, 7]
        total = np.zeros((8, nz, 3))
        total[0] = [[.007, .014, .021], [0., .003, 0.], [.023, .011, .004]]
        total[7] = [[.005, .008, .015], [.017, 0., .007], [.006, .019, .01]]
        maximum = 0.
        for orientation in (1, -1):
            entry, exit_surface = surfaces(orientation)
            for mu in (.5, -.5):
                out = white_radial_transfer(LIB, widths, regions, total, entry,
                    exit_surface, H, nz, mu, orientation, 32)
                ref = DecimalWhiteReference(widths, regions, total, entry, exit_surface,
                                            H, nz, mu, orientation)
                offset = 25. if mu > 0 else 125.
                _, literal_leak, _ = ref.ray(offset)
                first, last = (0, 7) if orientation == 1 else (7, 0)
                first_layer, last_layer = (0, 2) if mu > 0 else (2, 0)
                split = 170. if orientation == 1 else 230.
                optical = (50*total[first, first_layer]+100*total[first, 1]+
                    (split-150)*total[first, last_layer]+(250-split)*total[last, last_layer])
                expected = np.array([math.exp(-float(value)) for value in optical])
                np.testing.assert_allclose(literal_leak[1 if mu > 0 else 0, last,
                    entry*nz+first_layer], expected, rtol=5e-12, atol=1e-14)
                exact = ref.fixed(64); self.assert_arrays(out, exact)
                maximum = max(maximum, *(float(abs(out[name]-value).max()/max(float(abs(value).max()), 1e-100))
                    for name, value in zip(('transfer', 'leakage', 'incoming'), exact)))
        OBSERVATIONS.append(dict(control='independent_decimal_clipping_literal_exp',
            H=H, zone_edges_cm=[0, 50, 100, 150], groups=3, relative=maximum))

    def test_all370_radial_basis_AAA_ABA_H150_both_orientation_and_mu_signs(self):
        H, nz, k = 150., 3, 370
        widths = np.array([55., 43., 61., 37., 44., 69., 40., 51.]); regions = np.arange(8)
        q, axial = np.zeros((8*nz, k)), np.zeros((8, k)); worst = 0.
        for profile in ('AAA', 'ABA'):
            total = fixture(nz, k, profile)
            for orientation in (1, -1):
                entry, exit_surface = surfaces(orientation)
                for mu in (.37, -.37):
                    out = white_radial_transfer(LIB, widths, regions, total, entry,
                        exit_surface, H, nz, mu, orientation, 32)
                    active = np.zeros(6*nz, dtype=bool); active[entry*nz:(entry+1)*nz] = True
                    np.testing.assert_array_equal(out['transfer'][:, ~active], np.zeros_like(out['transfer'][:, ~active]))
                    np.testing.assert_array_equal(out['leakage'][:, :, ~active], np.zeros_like(out['leakage'][:, :, ~active]))
                    for layer in range(nz):
                        column = entry*nz+layer; radial = np.zeros((6*nz, k)); radial[column] = 1.
                        action = transport_multigroup(MULTI, widths, regions, total, entry,
                            H, nz, mu, orientation, 32, q, radial, axial)
                        expected_t, expected_l = boundary_currents(action, regions, nz, mu, orientation, exit_surface)
                        np.testing.assert_allclose(out['transfer'][:, column], expected_t, rtol=5e-12, atol=1e-14)
                        np.testing.assert_allclose(out['leakage'][:, :, column], expected_l, rtol=5e-12, atol=1e-14)
                        outer, face = (0, 1) if orientation == 1 else (len(widths)-1, 2)
                        incoming = action['fields'].reshape(len(widths), nz, 9, k)[outer, layer, face]
                        np.testing.assert_array_equal(incoming, np.full(k, out['incoming'][column]))
                        worst = max(worst, float(abs(out['transfer'][:, column]-expected_t).max()),
                                    float(abs(out['leakage'][:, :, column]-expected_l).max()))
                    for name in ('transfer', 'leakage', 'incoming'): self.assertGreaterEqual(float(out[name].min()), 0.)
                    for flag in ('full_reference_qualified', 'white_closure_qualified', 'actual_A_B_input_qualified',
                                 'physical_balance_qualified', 'AAA_qualified', 'ABA_admitted'):
                        self.assertFalse(out[flag])
        OBSERVATIONS.append(dict(control='all370_radial_basis_vs_saved_multigroup',
            synthetic_profiles=['AAA', 'ABA'], H=H, nz=nz, regions=8,
            orientations=2, mu_signs=2, columns=370, absolute=worst))

    def test_void_conservation_independent_incoming_and_vacuum_ends(self):
        H, nz, k = 150., 3, 370; widths, regions = [170., 230.], [0, 7]
        total = np.zeros((8, nz, k)); worst = 0.; analytic_totals = []
        for orientation in (1, -1):
            entry, exit_surface = surfaces(orientation)
            for mu in (.5, -.5, .2, -.2):
                out = white_radial_transfer(LIB, widths, regions, total, entry,
                    exit_surface, H, nz, mu, orientation, 32)
                expected_d = np.zeros(6*nz); expected_d[entry*nz:(entry+1)*nz] = H/nz
                np.testing.assert_allclose(out['incoming'], expected_d, rtol=5e-12, atol=1e-14)
                accounted = out['transfer'].sum(axis=0)+out['leakage'].sum(axis=(0, 1))
                np.testing.assert_allclose(accounted, np.repeat(expected_d[:, None], k, axis=1), rtol=5e-12, atol=1e-14)
                # Independent radial-entry z interval: length H - abs(mu)*W.
                radial_expected = max(0., H-abs(mu)*math.fsum(widths))
                end_expected = min(H, abs(mu)*math.fsum(widths))
                radial_actual = out['transfer'].sum(axis=(0, 1))
                end_actual = out['leakage'].sum(axis=(0, 1, 2))
                np.testing.assert_allclose(radial_actual, np.full(k, radial_expected), rtol=5e-12, atol=1e-14)
                np.testing.assert_allclose(end_actual, np.full(k, end_expected), rtol=5e-12, atol=1e-14)
                if radial_expected == 0.:
                    np.testing.assert_array_equal(radial_actual, np.zeros(k))
                else:
                    self.assertGreater(float(radial_actual.min()), 0.)
                self.assertGreater(float(end_actual.min()), 0.)
                analytic_totals.append(dict(orientation=orientation, mu=mu,
                    radial_expected_per_group=radial_expected, end_expected_per_group=end_expected,
                    radial_absolute=float(abs(radial_actual-radial_expected).max()),
                    end_absolute=float(abs(end_actual-end_expected).max())))
                self.assertGreater(out['geometry'][4], 0.)
                self.assertEqual(out['geometry'][1], out['geometry'][3]+out['geometry'][4])
                np.testing.assert_array_equal(out['leakage'][0 if mu > 0 else 1], np.zeros_like(out['leakage'][0]))
                worst = max(worst, float(abs(accounted-expected_d[:, None]).max()))
        OBSERVATIONS.append(dict(control='void_radial_plus_axial_leakage_conservation',
            H=H, nz=nz, columns=k, absolute=worst, axial_inflow=0.,
            analytic_boundary_totals=analytic_totals))

    def test_preserved_old_two_ABIs_and_multigroup_action(self):
        H, nz = 150., 3; widths, regions = [.13, .7, .29], [0, 7, 0]
        total = fixture(nz, 3, 'ABA'); q = np.full((8*nz, 3), .003)
        radial, axial = np.full((6*nz, 3), .2), np.zeros((8, 3))
        for column in range(3):
            arguments = [widths, regions, total[:, :, column], 1, H, nz, -.61, -1, 16,
                         q[:, column:column+1], radial[:, column:column+1], axial[:, column:column+1]]
            old, new = transport_zonal(OLD, *arguments), transport_zonal(LIB, *arguments)
            for name in ('fields', 'geometry', 'metrics'): np.testing.assert_array_equal(old[name], new[name])
        constant_args = [widths, regions, total[:, 0, 2], 1, H, nz, -.61, -1, 16,
                         q[:, 2:3], radial[:, 2:3], axial[:, 2:3]]
        old, new = transport(OLD, *constant_args), transport(LIB, *constant_args)
        for name in ('fields', 'geometry', 'metrics'): np.testing.assert_array_equal(old[name], new[name])
        arguments = [widths, regions, total, 1, H, nz, -.61, -1, 16, -q, -radial, axial]
        old, new = transport_multigroup(MULTI, *arguments), transport_multigroup(LIB, *arguments)
        for name in ('fields', 'geometry', 'metrics'): np.testing.assert_array_equal(old[name], new[name])
        self.assertLess(float(new['fields'].min()), 0.)
        OBSERVATIONS.append(dict(control='preserved_two_old_ABIs_and_signed_multigroup',
            zonal_columns=[0, 1, 2], constant_column=2, multigroup_columns=3,
            absolute=0., independent_physical_reference=False))

    def test_all370_column_order_void_thin_and_large_optical_length(self):
        H, nz = 150., 3; widths, regions = [170., 230.], [0, 7]
        total = fixture(nz, 370, 'ABA'); total[:, :, -1] = 10.
        base = white_radial_transfer(LIB, widths, regions, total, 1, 4, H, nz, .5, 1, 32)
        reversed_groups = white_radial_transfer(LIB, widths, regions, total[:, :, ::-1], 1, 4, H, nz, .5, 1, 32)
        for name in ('transfer', 'leakage'):
            np.testing.assert_array_equal(base[name][:, :, ::-1] if name == 'transfer' else base[name][:, :, :, ::-1], reversed_groups[name])
        for column in (0, 1, 184, 369):
            single = white_radial_transfer(LIB, widths, regions, total[:, :, column:column+1], 1, 4, H, nz, .5, 1, 32)
            np.testing.assert_array_equal(base['transfer'][:, :, column:column+1], single['transfer'])
            np.testing.assert_array_equal(base['leakage'][:, :, :, column:column+1], single['leakage'])
            np.testing.assert_array_equal(base['incoming'], single['incoming'])
            np.testing.assert_array_equal(base['geometry'], single['geometry'])
        for name in ('transfer', 'leakage'):
            self.assertTrue(np.all(base[name][..., 0] >= base[name][..., 1]))
            self.assertTrue(np.all(base[name][..., 1] >= base[name][..., -1]))
        self.assertEqual(float(base['transfer'][:, :, -1].max()), 0.)
        self.assertGreater(float(base['leakage'][:, :, :, -1].max()), 0.)
        OBSERVATIONS.append(dict(control='all370_order_single_column_and_unclipped_optical_depth',
            columns=370, compared_columns=[0, 1, 184, 369], field_absolute=0.,
            high_sigma=10., high_sigma_radial_maximum=0.,
            high_sigma_short_chord_leakage=float(base['leakage'][:, :, :, -1].max())))

    def test_input_contract_rejection(self):
        total = fixture(3, 3, 'ABA')
        arguments = [LIB, [170., 230.], [0, 7], total, 1, 4, 150., 3, .5, 1, 16]
        invalid = [(3, np.zeros((8, 3))), (3, total.transpose(2, 1, 0)),
            (3, np.zeros((8, 3, 0))), (3, np.zeros((8, 3, 371))),
            (3, -np.ones_like(total)), (3, np.full_like(total, np.inf)),
            (3, np.full_like(total, np.nan)), (1, [170., 0.]), (1, []),
            (2, [0]), (2, [0, 8]), (2, [0, .5]), (4, 4), (5, 6),
            (4, -1), (6, 0.), (7, 2.5), (8, 0.), (8, 1.), (9, 0), (10, 1)]
        for index, value in invalid:
            trial = arguments.copy(); trial[index] = value
            with self.assertRaises(ValueError): white_radial_transfer(*trial)
        with self.assertRaises(TypeError): white_radial_transfer(*arguments, q=np.ones((24, 3)))
        OBSERVATIONS.append(dict(control='complete_white_input_rejection', invalid_cases=len(invalid)+1))


if __name__ == '__main__':
    started = time.perf_counter(); result = unittest.main(exit=False).result
    with ARGS.report.open('x') as stream:
        json.dump(dict(schema='LAYERED_WHITE_RADIAL_TRANSFER_COMPONENT_V1',
            component_only=True, synthetic_fixtures_only=True,
            white_closure_qualified=False, whole_inventory_qualified=False,
            full_reference_qualified=False, actual_A_B_input_qualified=False,
            physical_balance_qualified=False, scientific_accuracy_qualified=False,
            AAA_qualified=False, ABA_admitted=False, tests_run=result.testsRun,
            passed=result.wasSuccessful(), failures=[str(name) for name, _ in result.failures],
            errors=[str(name) for name, _ in result.errors], observations=OBSERVATIONS,
            elapsed_seconds=time.perf_counter()-started), stream,
            sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')
    sys.exit(0 if result.wasSuccessful() else 1)
