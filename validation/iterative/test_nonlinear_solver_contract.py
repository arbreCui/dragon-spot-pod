#!/usr/bin/env python3
"""Algebra and publication tests for the no-transport solver contract."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import struct
import sys
import unittest


Q = Fraction
Vector = tuple[Q, ...]
Matrix = tuple[tuple[Q, ...], ...]


class SingularNewtonSystem(ValueError):
    """The exact Newton equation has no unique step."""


class InvalidMap(RuntimeError):
    """The strict physical map was not evaluated."""


@dataclass(frozen=True)
class ProposalEvaluation:
    classification: str
    published: Vector
    returned: Vector
    defects: tuple[Q, Q, Q]
    accepted: Vector | None


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    if len(matrix) != len(vector) or any(len(row) != len(vector) for row in matrix):
        raise ValueError("inconsistent matrix dimensions")
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def exact_solve(matrix: Matrix, rhs: Vector) -> Vector:
    """Solve a square rational system, rejecting an exactly singular one."""

    n = len(rhs)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("inconsistent Newton-system dimensions")
    work = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for column in range(n):
        pivot = next(
            (row for row in range(column, n) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            raise SingularNewtonSystem("singular exact Newton system")
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            scale = work[row][column]
            work[row] = [
                left - scale * right
                for left, right in zip(work[row], work[column], strict=True)
            ]
    return tuple(work[row][-1] for row in range(n))


def affine_map(matrix: Matrix, offset: Vector, state: Vector) -> Vector:
    return tuple(
        value + offset[i]
        for i, value in enumerate(matvec(matrix, state))
    )


def residual_jacobian(map_jacobian: Matrix) -> Matrix:
    return tuple(
        tuple(
            value - (Q(1) if row == column else Q(0))
            for column, value in enumerate(values)
        )
        for row, values in enumerate(map_jacobian)
    )


def exact_newton_oracle(base, map_function, jacobian_function):
    """Return one full exact-Newton proposal after one valid map call."""

    returned = map_function(base)
    if len(returned) != len(base):
        raise InvalidMap("map returned the wrong state dimension")
    residual = tuple(left - right for left, right in zip(returned, base, strict=True))
    jacobian = jacobian_function(base)
    step = exact_solve(jacobian, tuple(-value for value in residual))
    candidate = tuple(left + right for left, right in zip(base, step, strict=True))
    return candidate


def block_defects(candidate: Vector, returned: Vector) -> tuple[Q, Q, Q]:
    """One manufactured scalar for each physical SPOT state block."""

    if len(candidate) != 3 or len(returned) != 3:
        raise ValueError("manufactured state must contain rho, leakage and modal blocks")
    rho = abs(returned[0] - candidate[0])
    leakage_scale = max(abs(returned[1]), abs(candidate[1]))
    leakage_delta = abs(returned[1] - candidate[1])
    leakage = Q(0) if leakage_scale == 0 else leakage_delta / leakage_scale
    if returned[2] == 0:
        raise ValueError("nonpositive manufactured modal norm")
    modal = abs(returned[2] - candidate[2]) / abs(returned[2])
    return rho, leakage, modal


def three_component_gate(defects: tuple[Q, Q, Q], tolerance: Q) -> bool:
    if tolerance < 0 or any(value < 0 for value in defects):
        raise ValueError("invalid stopping data")
    return all(value <= tolerance for value in defects)


def evaluate_proposal(
    proposal: Vector,
    materialize,
    map_function,
    tolerance: Q,
) -> ProposalEvaluation:
    """Publish, evaluate and classify one proposal without a retry."""

    published = materialize(proposal)
    returned = map_function(published)
    defects = block_defects(published, returned)
    passed = three_component_gate(defects, tolerance)
    classification = "TOLERANCE_MET" if passed else "VALID_NOT_MET"
    return ProposalEvaluation(
        classification=classification,
        published=published,
        returned=returned,
        defects=defects,
        accepted=published if passed else None,
    )


def f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def scalar_directional_quotient(residual, publish, x, direction, step):
    base = publish(x)
    perturbed = publish(x + step * direction)
    return base, perturbed, (residual(perturbed) - residual(base)) / step


class NonlinearSolverContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.map_jacobian = (
            (Q(0), Q(1, 2), Q(0)),
            (Q(1, 3), Q(0), Q(1, 4)),
            (Q(0), Q(1, 5), Q(0)),
        )
        self.root = (Q(2), Q(3), Q(5))
        image = matvec(self.map_jacobian, self.root)
        self.offset = tuple(
            self.root[i] - image[i] for i in range(len(self.root))
        )

    def test_coupled_affine_root_requires_fresh_candidate_map(self) -> None:
        calls: list[Vector] = []

        def map_function(state: Vector) -> Vector:
            calls.append(state)
            return affine_map(self.map_jacobian, self.offset, state)

        base = (Q(1), Q(1), Q(1))
        candidate = exact_newton_oracle(
            base,
            map_function,
            lambda _: residual_jacobian(self.map_jacobian),
        )
        self.assertEqual(candidate, self.root)
        self.assertEqual(calls, [base])

        evaluation = evaluate_proposal(candidate, lambda state: state, map_function, Q(0))
        self.assertEqual(calls, [base, candidate])
        self.assertEqual(evaluation.classification, "TOLERANCE_MET")
        self.assertEqual(evaluation.published, candidate)
        self.assertEqual(evaluation.returned, candidate)
        self.assertEqual(evaluation.accepted, candidate)

    def test_linear_prediction_cannot_accept_nonlinear_candidate(self) -> None:
        calls: list[Vector] = []

        def nonlinear_map(state: Vector) -> Vector:
            calls.append(state)
            return (state[0] * state[0], (state[1] + 1) / 2, (state[2] + 1) / 2)

        base = (Q(2), Q(1), Q(1))
        jacobian = ((Q(3), Q(0), Q(0)), (Q(0), Q(-1, 2), Q(0)), (Q(0), Q(0), Q(-1, 2)))
        candidate = exact_newton_oracle(base, nonlinear_map, lambda _: jacobian)
        self.assertEqual(candidate, (Q(4, 3), Q(1), Q(1)))

        evaluation = evaluate_proposal(
            candidate,
            lambda state: state,
            nonlinear_map,
            Q(0),
        )
        self.assertEqual(evaluation.classification, "VALID_NOT_MET")
        self.assertEqual(evaluation.published, candidate)
        self.assertIsNone(evaluation.accepted)
        self.assertEqual(evaluation.defects, (Q(4, 9), Q(0), Q(0)))
        self.assertEqual(calls, [base, candidate])

    def test_materialized_state_is_the_certified_root_candidate(self) -> None:
        events: list[tuple[str, Vector]] = []
        proposal = (Q(2), Q(301, 100), Q(5))

        def materialize(state: Vector) -> Vector:
            events.append(("materialize", state))
            return self.root

        def map_function(state: Vector) -> Vector:
            events.append(("map", state))
            return affine_map(self.map_jacobian, self.offset, state)

        evaluation = evaluate_proposal(proposal, materialize, map_function, Q(0))
        self.assertEqual(
            events,
            [("materialize", proposal), ("map", self.root)],
        )
        self.assertEqual(evaluation.classification, "TOLERANCE_MET")
        self.assertEqual(evaluation.published, self.root)
        self.assertEqual(evaluation.returned, self.root)
        self.assertEqual(evaluation.accepted, self.root)

    def test_gate_is_three_separate_inclusive_conditions(self) -> None:
        epsilon = Q(1, 10)
        self.assertTrue(three_component_gate((epsilon, epsilon, epsilon), epsilon))
        for failed in range(3):
            defects = [epsilon, epsilon, epsilon]
            defects[failed] += Q(1, 100)
            self.assertFalse(three_component_gate(tuple(defects), epsilon))

    def test_consistent_leakage_unit_change_preserves_newton_step(self) -> None:
        scale = (Q(1), Q(100), Q(1))
        inverse = tuple(Q(1, 1) / value for value in scale)
        scaled_jacobian = tuple(
            tuple(
                scale[i] * self.map_jacobian[i][j] * inverse[j]
                for j in range(3)
            )
            for i in range(3)
        )
        scaled_offset = tuple(scale[i] * self.offset[i] for i in range(3))
        base = (Q(1), Q(1), Q(1))
        scaled_base = tuple(scale[i] * base[i] for i in range(3))

        candidate = exact_newton_oracle(
            base,
            lambda state: affine_map(self.map_jacobian, self.offset, state),
            lambda _: residual_jacobian(self.map_jacobian),
        )
        scaled_candidate = exact_newton_oracle(
            scaled_base,
            lambda state: affine_map(scaled_jacobian, scaled_offset, state),
            lambda _: residual_jacobian(scaled_jacobian),
        )
        self.assertEqual(
            scaled_candidate,
            tuple(scale[i] * candidate[i] for i in range(3)),
        )

    def test_invalid_map_and_singular_system_fail_closed(self) -> None:
        derivative_called = False

        def invalid_map(_: Vector) -> Vector:
            raise InvalidMap("strict inner terminal not met")

        def derivative(_: Vector) -> Matrix:
            nonlocal derivative_called
            derivative_called = True
            return ((Q(1),),)

        with self.assertRaises(InvalidMap):
            exact_newton_oracle((Q(1),), invalid_map, derivative)
        self.assertFalse(derivative_called)

        with self.assertRaises(SingularNewtonSystem):
            exact_newton_oracle(
                (Q(1),),
                lambda _: (Q(2),),
                lambda _: ((Q(0),),),
            )

        candidate_calls = 0

        def invalid_candidate_map(_: Vector) -> Vector:
            nonlocal candidate_calls
            candidate_calls += 1
            raise InvalidMap("candidate radial terminal not met")

        with self.assertRaises(InvalidMap):
            evaluate_proposal(
                (Q(1), Q(1), Q(1)),
                lambda state: state,
                invalid_candidate_map,
                Q(0),
            )
        self.assertEqual(candidate_calls, 1)

    def test_fd_secant_depends_on_binary32_publication_step(self) -> None:
        self.assertEqual(sys.float_info.radix, 2)
        self.assertEqual(sys.float_info.mant_dig, 53)
        self.assertEqual(sys.float_info.rounds, 1)
        self.assertEqual(struct.calcsize(">f"), 4)

        # F(x)=x corresponds to the smooth manufactured map G(x)=2x.
        residual = lambda value: value
        identity = lambda value: value
        x = 1.0
        direction = 1.0
        hidden = 2.0**-25
        one_ulp = 2.0**-23
        tie_to_even = 3.0 * 2.0**-24

        _, smooth, smooth_jv = scalar_directional_quotient(
            residual, identity, x, direction, hidden
        )
        self.assertNotEqual(smooth, x)
        self.assertEqual(smooth_jv, 1.0)

        base, collapsed, zero_jv = scalar_directional_quotient(
            residual, f32, x, direction, hidden
        )
        self.assertEqual(collapsed, base)
        self.assertEqual(zero_jv, 0.0)
        self.assertEqual(
            scalar_directional_quotient(
                residual, f32, x, direction, one_ulp
            )[2],
            1.0,
        )
        self.assertEqual(
            scalar_directional_quotient(
                residual, f32, x, direction, tie_to_even
            )[2],
            4.0 / 3.0,
        )


if __name__ == "__main__":
    unittest.main()
