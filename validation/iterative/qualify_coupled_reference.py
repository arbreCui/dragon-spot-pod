#!/usr/bin/env python3
"""Exact small-model qualification of the full-coordinate ratio closure.

Two radial regions, one energy group, S2 vacuum boundaries and one or two
axial cells. All arithmetic, derivatives and rank decisions are rational.
This is a manufactured model, never a D4 solver or production-state writer.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path
import sys


@dataclass(frozen=True)
class Dual:
    value: Q
    derivative: tuple

    def lift(self, other):
        if isinstance(other, Dual):
            if len(other.derivative) != len(self.derivative):
                raise ValueError("different derivative dimensions")
            return other
        return Dual(Q(other), (Q(0),) * len(self.derivative))

    def __add__(self, other):
        other = self.lift(other)
        return Dual(self.value + other.value,
                    tuple(a + b for a, b in zip(self.derivative, other.derivative)))

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, tuple(-x for x in self.derivative))

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        other = self.lift(other)
        return Dual(self.value * other.value,
                    tuple(a * other.value + self.value * b
                          for a, b in zip(self.derivative, other.derivative)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.lift(other)
        if not other.value:
            raise ZeroDivisionError("undefined ratio in manufactured residual")
        return Dual(self.value / other.value,
                    tuple((a * other.value - self.value * b) / (other.value * other.value)
                          for a, b in zip(self.derivative, other.derivative)))

    def __rtruediv__(self, other):
        return self.lift(other) / self


@dataclass(frozen=True)
class Slab:
    cells: int
    streaming: Q  # mu / h, with the usual S2 mu=1/sqrt(3).
    total: Q = Q(2)
    absorption: Q = Q(1)
    exchange: Q = Q(1)

    def __post_init__(self):
        if self.cells not in (1, 2):
            raise ValueError("only the two declared manufactured meshes")
        if min(self.streaming, self.absorption, self.exchange) <= 0:
            raise ValueError("positive streaming, absorption and exchange required")
        if self.total < self.absorption:
            raise ValueError("negative scattering")

    @property
    def unknowns(self):
        return 6 * self.cells + 1

    def fields(self, x):
        """u is plane-major; vacuum incoming faces are fixed exact zeros."""
        n = self.cells
        if len(x) != self.unknowns:
            raise ValueError("wrong unknown count")
        u = [[x[2*z+r] for r in range(2)] for z in range(n)]
        faces = []
        for r in range(2):
            start = 2*n + 2*n*r
            plus = [Q(0), *x[start:start+n]]
            minus = [*x[start+n:start+2*n], Q(0)]
            faces.append((plus, minus))
        phi = [[sum(faces[r][angle][z] + faces[r][angle][z+1]
                    for angle in range(2)) / 2 for r in range(2)] for z in range(n)]
        leakage = []
        for z in range(n):
            divergence = sum(self.streaming * (plus[z+1]-minus[z+1]-plus[z]+minus[z])
                             for plus, minus in faces)
            leakage.append(divergence / sum(phi[z]))
        return u, faces, phi, leakage, x[-1]

    def residual(self, x, model="ratio", matching=False):
        if model not in ("ratio", "explicit_exchange"):
            raise ValueError("unknown manufactured operator")
        u, faces, phi, leakage, rho = self.fields(x)
        residual = []
        a, c, t, s = self.absorption, self.exchange, self.total, self.streaming
        # Radial transport is refreshed simultaneously, not frozen at a seed.
        for z in range(self.cells):
            for r in range(2):
                f = Q(r == 0)
                residual.append((a+c+leakage[z])*u[z][r] - c*u[z][1-r]
                                - rho*f*phi[z][r])
        # S2 diamond differencing, isotropic scattering and fission.
        for r in range(2):
            plus, minus = faces[r]
            f = Q(r == 0)
            for z in range(self.cells):
                if model == "ratio":
                    d = -a + rho*f*phi[z][r]/u[z][r] - leakage[z]
                    transverse = d * phi[z][r]
                else:
                    transverse = c * (phi[z][r] - phi[z][1-r])
                for sign, face in ((1, plus), (-1, minus)):
                    residual.append(sign*s*(face[z+1]-face[z])
                                    + t*(face[z]+face[z+1])/2
                                    + transverse/2 - (t-a)*phi[z][r]/2
                                    - rho*f*phi[z][r]/2)
        # Unit cell volumes; nu-fission=1 in region 0 and exactly 0 in region 1.
        residual.append(sum(row[0] for row in phi) - 1)
        if matching:
            # Diagnostic control only. These constraints are NOT in production.
            residual.extend(phi[z][1] - u[z][1] for z in range(self.cells))
        return residual

    def positive_family(self, alpha):
        """Exact candidate family; the residual equations independently test it."""
        alpha = Q(alpha)
        if alpha <= 0:
            raise ValueError("positive non-fission/fission amplitude ratio required")
        n, s, t = self.cells, self.streaming, self.total
        fuel_phi = Q(1, n)
        if n == 1:
            fuel_faces = [fuel_phi, fuel_phi]
            leakage = 2*s
        else:
            outgoing = fuel_phi / (1+t/(4*s))
            middle = outgoing * (Q(1, 2)+t/(4*s))
            fuel_faces = [middle, outgoing, outgoing, middle]
            leakage = s / (1+t/(4*s))
        diagonal = self.absorption + self.exchange + leakage
        radial_ratio = self.exchange / diagonal
        rho = diagonal - self.exchange * radial_ratio
        x = [value for _ in range(n) for value in (fuel_phi, radial_ratio*fuel_phi)]
        x += fuel_faces + [alpha*f for f in fuel_faces] + [rho]
        return x

    def explicit_reference(self):
        candidate = self.positive_family(Q(1))
        u, _, _, _, _ = self.fields(candidate)
        return self.positive_family(u[0][1] / u[0][0])

    def balance(self, x, model="ratio"):
        """Unit-volume global neutron balance; radial exchange has no exterior loss."""
        if model not in ("ratio", "explicit_exchange"):
            raise ValueError("unknown manufactured operator")
        u, faces, phi, leakage, rho = self.fields(x)
        absorption = self.absorption * sum(sum(row) for row in phi)
        axial_outflow = self.streaming * sum(plus[-1] + minus[0] for plus, minus in faces)
        fission_source = rho * sum(row[0] for row in phi)
        transverse = Q(0)
        for z in range(self.cells):
            for r in range(2):
                if model == "ratio":
                    d = -self.absorption + rho*Q(r == 0)*phi[z][r]/u[z][r] - leakage[z]
                    transverse += d * phi[z][r]
                else:
                    transverse += self.exchange * (phi[z][r] - phi[z][1-r])
        defect = absorption + axial_outflow - fission_source
        return {"absorption": absorption, "axial_boundary_outflow": axial_outflow,
                "fission_source": fission_source, "net_transverse_term": transverse,
                "physical_balance_defect": defect,
                "closed_equation_balance_defect": defect + transverse}


def jacobian(slab, x, model="ratio", matching=False):
    n = len(x)
    variables = [Dual(Q(value), tuple(Q(i == j) for j in range(n)))
                 for i, value in enumerate(x)]
    rows = slab.residual(variables, model, matching)
    return [row.value for row in rows], [list(row.derivative) for row in rows]


def rref(matrix):
    a = [[Q(value) for value in row] for row in matrix]
    if not a or not a[0] or any(len(row) != len(a[0]) for row in a):
        raise ValueError("nonempty rectangular matrix required")
    pivot_row = 0
    pivots = []
    for col in range(len(a[0])):
        candidates = [i for i in range(pivot_row, len(a)) if a[i][col]]
        if not candidates:
            continue
        i = candidates[0]
        a[pivot_row], a[i] = a[i], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v / scale for v in a[pivot_row]]
        for j in range(len(a)):
            if j == pivot_row:
                continue
            scale = a[j][col]
            a[j] = [v - scale*p for v, p in zip(a[j], a[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(a):
            break
    return a, pivots


def rank_and_nullspace(matrix):
    reduced, pivots = rref(matrix)
    n = len(matrix[0])
    nullspace = []
    for free in (i for i in range(n) if i not in pivots):
        v = [Q(0)] * n
        v[free] = Q(1)
        for row, pivot in enumerate(pivots):
            v[pivot] = -reduced[row][free]
        assert all(sum(a*b for a, b in zip(row, v)) == 0 for row in matrix)
        nullspace.append(v)
    return len(pivots), nullspace


def record_case(slab):
    ref = slab.explicit_reference()
    _, _, ref_phi, leakage, rho = slab.fields(ref)
    records = []
    for alpha in (Q(1, 4), Q(1, 2), Q(1)):
        x = slab.positive_family(alpha)
        residual, j = jacobian(slab, x)
        assert all(v == 0 for v in residual)
        _, _, phi, observed_leakage, observed_rho = slab.fields(x)
        assert all(v > 0 for row in phi for v in row)
        assert observed_leakage == leakage and observed_rho == rho
        rank, nullspace = rank_and_nullspace(j)
        assert rank == slab.unknowns - 1 and len(nullspace) == 1
        direct_defect = slab.residual(x, "explicit_exchange")
        assert any(direct_defect)
        records.append({"alpha": str(alpha), "state": list(map(str, x)),
                        "scalar_flux": [[str(v) for v in row] for row in phi],
                        "global_balance": {key: str(value) for key, value in slab.balance(x).items()},
                        "residual": list(map(str, residual)), "jacobian_rank": rank,
                        "jacobian": [[str(v) for v in row] for row in j],
                        "nullspace": [[str(v) for v in row] for row in nullspace],
                        "explicit_exchange_max_residual": str(max(map(abs, direct_defect)))})
    direct_residual, direct_j = jacobian(slab, ref, "explicit_exchange")
    augmented_residual, augmented_j = jacobian(slab, ref, matching=True)
    assert not any(direct_residual) and not any(augmented_residual)
    direct_rank, direct_null = rank_and_nullspace(direct_j)
    augmented_rank, augmented_null = rank_and_nullspace(augmented_j)
    assert direct_rank == augmented_rank == slab.unknowns
    assert not direct_null and not augmented_null
    return {"axial_cells": slab.cells, "mu_over_h": str(slab.streaming),
            "unknowns": slab.unknowns, "k": str(1/rho), "inverse_k": str(rho),
            "leakage_by_plane": list(map(str, leakage)), "positive_ratio_family": records,
            "explicit_exchange_reference": {
                "alpha": str(ref_phi[0][1]/ref_phi[0][0]), "state": list(map(str, ref)),
                "scalar_flux": [[str(v) for v in row] for row in ref_phi],
                "global_balance": {key: str(value) for key, value in slab.balance(ref, "explicit_exchange").items()},
                "jacobian_rank": direct_rank, "residual": list(map(str, direct_residual)),
                "jacobian": [[str(v) for v in row] for row in direct_j]},
            "additional_mean_matching_diagnostic_only": {
                "equations": len(augmented_residual), "jacobian_rank": augmented_rank,
                "residual": list(map(str, augmented_residual)),
                "production_change": False}}


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: qualify_coupled_reference.py NEW_OUTPUT_DIRECTORY")
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    result = {"classification": "EXACT_MANUFACTURED_COUPLED_CLOSURE_COUNTEREXAMPLE",
              "arithmetic": "rational values, rational forward derivatives, exact row reduction",
              "cases": [record_case(Slab(1, Q(1, 2))), record_case(Slab(2, Q(1)))],
              "limits": ["Not D4 data, a D4 Jacobian or a CE-error attribution.",
                         "Two S2 vacuum manufactured cases; no universal degeneracy claim.",
                         "Explicit radial exchange is a small reference control, not a 3D transport validation.",
                         "Extra mean-matching equations are a diagnostic control, not a production modification.",
                         "Full reference Jacobian rank proves local regularity at these solutions, not global uniqueness for arbitrary inputs."]}
    (out / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    for case in result["cases"]:
        n = case["unknowns"]
        print(f"{case['axial_cells']} cells: k={case['k']}, ratio rank={n-1}/{n}, "
              f"explicit-exchange rank={n}/{n}; exact positive one-parameter family")


if __name__ == "__main__":
    main()
