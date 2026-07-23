#!/usr/bin/env python3
"""Independent manufactured tests for the canonical SPOT state algebra."""

from __future__ import annotations

import math
import struct
import unittest


def cholesky_solve(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    n = len(rhs)
    lower = [[0.0] * n for _ in range(n)]
    for row in range(n):
        for col in range(row + 1):
            pivot = matrix[row][col]
            for k in range(col):
                pivot -= lower[row][k] * lower[col][k]
            if row == col:
                if not math.isfinite(pivot) or pivot <= 0.0:
                    raise ValueError("singular Gram matrix")
                lower[row][col] = math.sqrt(pivot)
            else:
                lower[row][col] = pivot / lower[col][col]
    work = [0.0] * n
    for row in range(n):
        work[row] = (
            rhs[row]
            - sum(lower[row][k] * work[k] for k in range(row))
        ) / lower[row][row]
    result = [0.0] * n
    for row in range(n - 1, -1, -1):
        result[row] = (
            work[row]
            - sum(lower[k][row] * result[k] for k in range(row + 1, n))
        ) / lower[row][row]
    return result


def gram_coordinates(
    basis: list[list[float]], volumes: list[float], field: list[float]
) -> tuple[list[float], list[list[float]]]:
    total = sum(volumes)
    weights = [value / total for value in volumes]
    modes = len(basis[0])
    gram = [
        [
            sum(weights[i] * basis[i][a] * basis[i][b] for i in range(len(field)))
            for b in range(modes)
        ]
        for a in range(modes)
    ]
    rhs = [
        sum(weights[i] * basis[i][a] * field[i] for i in range(len(field)))
        for a in range(modes)
    ]
    return cholesky_solve(gram, rhs), gram


def leakage(
    area: list[float],
    dz: list[float],
    plane_of_floor: list[int],
    phi: list[list[float]],
    current: list[list[float]],
    planes: int,
) -> list[float]:
    numerator = [0.0] * planes
    denominator = [0.0] * planes
    for floor, plane in enumerate(plane_of_floor):
        for region, radial_area in enumerate(area):
            numerator[plane] += radial_area * (
                current[floor + 1][region] - current[floor][region]
            )
            denominator[plane] += (
                radial_area * dz[floor] * phi[floor][region]
            )
    if any(value <= 0.0 for value in denominator):
        raise ValueError("nonpositive leakage denominator")
    return [
        numerator[plane] / denominator[plane]
        for plane in range(planes)
    ]


def defects(
    current_a: list[float],
    previous_a: list[float],
    gram: list[list[float]],
    current_rho: float,
    previous_rho: float,
    current_l: list[float],
    previous_l: list[float],
) -> tuple[float, float, float, float]:
    delta = [a - b for a, b in zip(current_a, previous_a, strict=True)]
    num = sum(
        delta[i] * gram[i][j] * delta[j]
        for i in range(len(delta))
        for j in range(len(delta))
    )
    den = sum(
        current_a[i] * gram[i][j] * current_a[j]
        for i in range(len(delta))
        for j in range(len(delta))
    )
    dl = max(abs(a - b) for a, b in zip(current_l, previous_l, strict=True))
    scale = max(max(map(abs, current_l)), max(map(abs, previous_l)))
    rleak = 0.0 if scale == 0.0 and dl == 0.0 else dl / scale
    return abs(current_rho - previous_rho), rleak, dl, math.sqrt(num / den)


def f32(value: float) -> float:
    return struct.unpack(">f", struct.pack(">f", value))[0]


def production_restriction(volumes: list[float], values: list[float]) -> float:
    projected = f32(0.0)
    weight = f32(0.0)
    for volume, value in zip(volumes, values, strict=True):
        projected = f32(projected + f32(f32(volume) * f32(value)))
        weight = f32(weight + f32(volume))
    if weight <= 0.0:
        raise ValueError("empty restriction")
    return f32(projected / weight)


def layout_coordinate_defect(
    current: list[float],
    previous: list[float],
    ranks: list[int],
    offsets: list[int],
    gram_offsets: list[int],
    gram_flat: list[float],
    heights: list[float],
) -> float:
    planes = len(heights)
    numerator = 0.0
    denominator = 0.0
    for group, modes in enumerate(ranks):
        for plane in range(planes):
            for a in range(modes):
                ia = offsets[group] + plane * modes + a
                da = current[ia] - previous[ia]
                for b in range(modes):
                    ib = offsets[group] + plane * modes + b
                    ig = gram_offsets[group] + b * modes + a
                    numerator += heights[plane] * da * gram_flat[ig] * (
                        current[ib] - previous[ib]
                    )
                    denominator += (
                        heights[plane]
                        * current[ia]
                        * gram_flat[ig]
                        * current[ib]
                    )
    return math.sqrt(numerator / denominator)


class StateMathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.area = [1.0, 2.0, 4.0]
        self.dz = [0.5, 1.5, 2.0, 1.0]
        self.plane_of_floor = [0, 0, 1, 1]
        self.basis = [
            [1.0, 0.2],
            [0.9, -0.4],
            [1.2, 0.3],
        ]

    def test_gram_coordinates_reconstruct_in_space_field(self) -> None:
        expected = [2.0, -0.75]
        field = [
            sum(row[j] * expected[j] for j in range(2))
            for row in self.basis
        ]
        coordinate, _ = gram_coordinates(self.basis, self.area, field)
        for actual, target in zip(coordinate, expected, strict=True):
            self.assertAlmostEqual(actual, target, places=13)

    def test_stored_basis_need_not_be_exactly_orthonormal(self) -> None:
        coordinate, gram = gram_coordinates(
            self.basis, self.area, [1.1, 0.8, 1.4]
        )
        naive = [
            sum(
                self.area[i] / sum(self.area) * self.basis[i][a] * [1.1, 0.8, 1.4][i]
                for i in range(3)
            )
            for a in range(2)
        ]
        self.assertGreater(max(abs(a - b) for a, b in zip(coordinate, naive)), 1e-2)
        self.assertNotAlmostEqual(gram[0][0], 1.0, places=6)

    def test_global_scaling_cancels_but_local_scaling_does_not(self) -> None:
        raw = [3.0, 5.0, 7.0]
        norm = 11.0
        state1, _ = gram_coordinates(
            self.basis, self.area, [value / norm for value in raw]
        )
        factor = 9.0
        state2, _ = gram_coordinates(
            self.basis,
            self.area,
            [factor * value / (factor * norm) for value in raw],
        )
        self.assertEqual(state1, state2)
        local, _ = gram_coordinates(
            self.basis,
            self.area,
            [factor * raw[0] / (factor * norm), raw[1] / (factor * norm), raw[2] / (factor * norm)],
        )
        self.assertGreater(max(abs(a - b) for a, b in zip(state1, local)), 1e-3)

    def test_signed_leakage_and_zero_branch(self) -> None:
        phi = [[1.0, 2.0, 1.5] for _ in self.dz]
        current = [
            [0.0, 0.0, 0.0],
            [0.1, 0.2, 0.4],
            [0.3, 0.5, 0.8],
            [0.2, 0.4, 0.7],
            [0.1, 0.2, 0.3],
        ]
        value = leakage(
            self.area,self.dz,self.plane_of_floor,phi,current,2
        )
        self.assertGreater(value[0], 0.0)
        self.assertLess(value[1], 0.0)
        zero = leakage(
            self.area,
            self.dz,
            self.plane_of_floor,
            phi,
            [[0.0, 0.0, 0.0] for _ in range(5)],
            2,
        )
        self.assertEqual(zero, [0.0, 0.0])

    def test_separate_defects(self) -> None:
        _, gram = gram_coordinates(self.basis,self.area,[1.0,1.0,1.0])
        zero = defects([1.0,2.0],[1.0,2.0],gram,0.8,0.8,[0.0,0.0],[0.0,0.0])
        self.assertEqual(zero, (0.0,0.0,0.0,0.0))
        changed = defects(
            [1.1,2.0],[1.0,2.0],gram,0.81,0.8,[0.2,-0.1],[0.1,-0.1]
        )
        self.assertAlmostEqual(changed[0],0.01,places=14)
        self.assertAlmostEqual(changed[1],0.5,places=14)
        self.assertAlmostEqual(changed[2],0.1,places=14)
        self.assertGreater(changed[3],0.0)

    def test_binary32_restriction_precedes_global_normalization(self) -> None:
        volumes = [0.1, 0.2, 0.3, 0.4]
        values = [1.0000001, 3.0, 2.0, 7.0]
        restricted = production_restriction(volumes, values)
        direct = sum(v * x for v, x in zip(volumes, values, strict=True)) / sum(volumes)
        self.assertNotEqual(restricted, direct)
        norm = 13.0
        self.assertEqual(restricted / norm, float(restricted) / norm)

    def test_multigroup_multiplane_height_and_flattening(self) -> None:
        ranks = [1, 2]
        offsets = [0, 2, 6]
        gram_offsets = [0, 1, 5]
        # Column-major flattened Gram blocks: [2] and [[3,1],[1,4]].
        gram_flat = [2.0, 3.0, 1.0, 1.0, 4.0]
        heights = [1.0, 3.0]
        previous = [1.0, 2.0, 0.5, 1.5, 2.0, -0.5]
        current = [1.2, 1.8, 0.7, 1.4, 2.2, -0.2]
        actual = layout_coordinate_defect(
            current,previous,ranks,offsets,gram_offsets,gram_flat,heights
        )
        # Independent block-matrix calculation.
        numerator = (
            1.0 * 2.0 * 0.2**2
            + 3.0 * 2.0 * (-0.2)**2
            + 1.0 * (3.0 * 0.2**2 + 2.0 * 0.2 * (-0.1) + 4.0 * (-0.1)**2)
            + 3.0 * (3.0 * 0.2**2 + 2.0 * 0.2 * 0.3 + 4.0 * 0.3**2)
        )
        denominator = (
            1.0 * 2.0 * 1.2**2
            + 3.0 * 2.0 * 1.8**2
            + 1.0 * (3.0 * 0.7**2 + 2.0 * 0.7 * 1.4 + 4.0 * 1.4**2)
            + 3.0 * (3.0 * 2.2**2 + 2.0 * 2.2 * (-0.2) + 4.0 * (-0.2)**2)
        )
        self.assertAlmostEqual(actual,math.sqrt(numerator/denominator),places=15)

    def test_singular_gram_fails_closed(self) -> None:
        singular = [[1.0,2.0],[2.0,4.0],[3.0,6.0]]
        with self.assertRaises(ValueError):
            gram_coordinates(singular,self.area,[1.0,1.0,1.0])


if __name__ == "__main__":
    unittest.main()
