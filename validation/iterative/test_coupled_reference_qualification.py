"""Exact manufactured admissibility tests; no transport or production changes."""
from fractions import Fraction as Q
import unittest

from qualify_coupled_reference import Dual, Slab, jacobian, rank_and_nullspace


class CoupledReferenceQualification(unittest.TestCase):
    def test_exact_derivatives_of_ratio(self):
        x, y = Dual(Q(2), (Q(1), Q(0))), Dual(Q(1), (Q(0), Q(1)))
        value = (x*x + 3*y)/(x-y)
        self.assertEqual(value.value, 7)
        self.assertEqual(value.derivative, (-3, 10))

    def test_positive_family_survives_radial_and_leakage_feedback(self):
        for slab, k, leak in ((Slab(1, Q(1, 2)), Q(3, 8), Q(1)),
                              (Slab(2, Q(1)), Q(24, 55), Q(2, 3))):
            for alpha in (Q(1, 10), Q(1, 4), Q(1, 2), Q(2)):
                x = slab.positive_family(alpha)
                self.assertEqual(slab.residual(x), [0]*slab.unknowns)
                _, faces, phi, leakage, rho = slab.fields(x)
                self.assertEqual(1/rho, k)
                self.assertEqual(leakage, [leak]*slab.cells)
                self.assertEqual(sum(row[0] for row in phi), 1)
                self.assertTrue(all(v > 0 for row in phi for v in row))
                self.assertTrue(all(plus[0] == minus[-1] == 0 for plus, minus in faces))

    def test_exact_null_direction_changes_only_nonfission_angular_amplitude(self):
        for slab in (Slab(1, Q(1, 2)), Slab(2, Q(1))):
            x = slab.positive_family(Q(1, 4))
            _, j = jacobian(slab, x)
            rank, null = rank_and_nullspace(j)
            self.assertEqual(rank, slab.unknowns-1)
            self.assertEqual(len(null), 1)
            v = null[0]
            self.assertEqual(v[:4*slab.cells], [0]*(4*slab.cells))
            self.assertEqual(v[-1], 0)
            family_tangent = [b-a for a, b in zip(x, slab.positive_family(Q(1, 2)))]
            self.assertTrue(all(sum(a*b for a, b in zip(row, family_tangent)) == 0 for row in j))

    def test_explicit_exchange_reference_is_locally_regular(self):
        for slab, alpha in ((Slab(1, Q(1, 2)), Q(1, 3)), (Slab(2, Q(1)), Q(3, 8))):
            ref = slab.explicit_reference()
            residual, j = jacobian(slab, ref, "explicit_exchange")
            self.assertFalse(any(residual))
            self.assertEqual(rank_and_nullspace(j), (slab.unknowns, []))
            _, _, phi, _, _ = slab.fields(ref)
            self.assertEqual(phi[0][1]/phi[0][0], alpha)
            self.assertTrue(any(slab.residual(slab.positive_family(Q(1, 2)), "explicit_exchange")))

    def test_mean_matching_removes_this_null_direction_only_as_a_control(self):
        for slab in (Slab(1, Q(1, 2)), Slab(2, Q(1))):
            residual, j = jacobian(slab, slab.explicit_reference(), matching=True)
            self.assertFalse(any(residual))
            self.assertEqual(rank_and_nullspace(j), (slab.unknowns, []))
            self.assertTrue(any(slab.residual(slab.positive_family(Q(1, 2)), matching=True)))

    def test_physical_balance_distinguishes_equal_k_positive_solutions(self):
        for slab, defect in ((Slab(1, Q(1, 2)), Q(1, 3)),
                             (Slab(2, Q(1)), Q(5, 24))):
            balance = slab.balance(slab.positive_family(Q(1, 2)))
            self.assertEqual(balance["physical_balance_defect"], defect)
            self.assertEqual(balance["net_transverse_term"], -defect)
            self.assertEqual(balance["closed_equation_balance_defect"], 0)
            for model in ("ratio", "explicit_exchange"):
                reference = slab.balance(slab.explicit_reference(), model)
                self.assertEqual(reference["physical_balance_defect"], 0)
                self.assertEqual(reference["net_transverse_term"], 0)

    def test_complete_residual_jacobian_against_independent_central_difference(self):
        slab = Slab(2, Q(1))
        x = slab.positive_family(Q(1, 2))
        step = Q(1, 10**6)
        for model in ("ratio", "explicit_exchange"):
            _, j = jacobian(slab, x, model)
            for col in range(len(x)):
                plus, minus = x.copy(), x.copy()
                plus[col] += step
                minus[col] -= step
                a, b = slab.residual(plus, model), slab.residual(minus, model)
                for row in range(len(j)):
                    self.assertLess(abs((a[row]-b[row])/(2*step)-j[row][col]), Q(1, 10**8))


if __name__ == "__main__":
    unittest.main(verbosity=2)
