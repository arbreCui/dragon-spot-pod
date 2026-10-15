#!/usr/bin/env python3
"""Bounded heterogeneous/multigroup closure qualification, without transport runs."""
from dataclasses import dataclass, replace
from fractions import Fraction as Q
import json
from pathlib import Path
import sys

import numpy as np

from qualify_coupled_reference import Dual, rank_and_nullspace, rref


@dataclass(frozen=True)
class Network:
    name: str
    streaming: object
    total: np.ndarray  # plane, radial region, group
    scatter: np.ndarray  # plane, radial region, destination group, incident group
    nuf: np.ndarray
    chi: np.ndarray
    exchange: np.ndarray  # plane, group; symmetric conservative radial exchange

    def __post_init__(self):
        n, r, g = self.total.shape
        if r != 2 or n not in (1, 2) or g not in (1, 2):
            raise ValueError("only the declared small networks")
        if self.scatter.shape != (n, r, g, g) or self.nuf.shape != (n, r, g):
            raise ValueError("inconsistent material dimensions")
        if self.chi.shape != (g,) or self.exchange.shape != (n, g):
            raise ValueError("inconsistent source/exchange dimensions")
        arrays = (self.total, self.scatter, self.nuf, self.chi, self.exchange)
        if any(not np.isfinite(np.asarray(a, dtype=float)).all() for a in arrays):
            raise ValueError("nonfinite coefficients")
        if self.streaming <= 0 or np.any(self.exchange <= 0):
            raise ValueError("positive streaming and exchange required")
        if np.any(self.scatter < 0) or np.any(self.nuf < 0) or np.any(self.chi < 0):
            raise ValueError("negative source coefficient")
        if np.any(self.absorption <= 0) or sum(self.chi) != 1:
            raise ValueError("positive absorption and unit fission spectrum required")

    @property
    def cells(self):
        return self.total.shape[0]

    @property
    def groups(self):
        return self.total.shape[2]

    @property
    def radial_size(self):
        return self.total.size

    @property
    def unknowns(self):
        return 3*self.radial_size + 1

    @property
    def absorption(self):
        return self.total - self.scatter.sum(axis=2)

    def fields(self, x, with_leakage=True):
        x = np.asarray(x)
        if x.size != self.unknowns:
            raise ValueError("wrong state dimension")
        n, g, m = self.cells, self.groups, self.radial_size
        u = x[:m].reshape(n, 2, g)
        raw = x[m:-1].reshape(2, g, 2, n)
        zeros = np.zeros((2, g, 1), dtype=x.dtype)
        plus = np.concatenate((zeros, raw[:, :, 0, :]), axis=2)
        minus = np.concatenate((raw[:, :, 1, :], zeros), axis=2)
        phi = ((plus[:, :, :-1] + plus[:, :, 1:] + minus[:, :, :-1]
                + minus[:, :, 1:])/2).transpose(2, 0, 1)
        divergence = self.streaming*(plus[:, :, 1:]-minus[:, :, 1:]
                                     -plus[:, :, :-1]+minus[:, :, :-1])
        leakage = divergence.sum(axis=0).T / phi.sum(axis=1) if with_leakage else None
        return u, plus, minus, phi, leakage, x[-1]

    def radial_residual(self, u, phi, leakage, rho):
        rows = []
        for z in range(self.cells):
            for r in range(2):
                for g in range(self.groups):
                    source = rho*self.chi[g]*sum(self.nuf[z, r]*phi[z, r])
                    rows.append((self.total[z, r, g]+leakage[z, g])*u[z, r, g]
                                + self.exchange[z, g]*(u[z, r, g]-u[z, 1-r, g])
                                - sum(self.scatter[z, r, g]*u[z, r]) - source)
        return np.asarray(rows)

    def transverse(self, u, phi, leakage, rho, z, r, g, model):
        if model == "explicit_exchange":
            return self.exchange[z, g]*(phi[z, r, g]-phi[z, 1-r, g])
        if model != "ratio":
            raise ValueError("unknown closure")
        q = sum(self.scatter[z, r, g, h]*u[z, r, h]
                for h in range(self.groups) if h != g)
        q += rho*self.chi[g]*sum(self.nuf[z, r]*phi[z, r])
        d = (-self.total[z, r, g]+self.scatter[z, r, g, g]
             + q/u[z, r, g]-leakage[z, g])
        return d*phi[z, r, g]

    def angular_residual(self, x, model):
        u, plus, minus, phi, leakage, rho = self.fields(x, model == "ratio")
        rows = []
        for r in range(2):
            for g in range(self.groups):
                for z in range(self.cells):
                    transverse = self.transverse(u, phi, leakage, rho, z, r, g, model)
                    source = (sum(self.scatter[z, r, g]*phi[z, r])
                              + rho*self.chi[g]*sum(self.nuf[z, r]*phi[z, r]))
                    for sign, faces in ((1, plus), (-1, minus)):
                        left, right = faces[r, g, z:z+2]
                        rows.append(sign*self.streaming*(right-left)
                                    + self.total[z, r, g]*(right+left)/2
                                    + transverse/2-source/2)
        return np.asarray(rows)

    def residual(self, x, model="ratio"):
        u, _, _, phi, leakage, rho = self.fields(x)
        return np.concatenate((self.radial_residual(u, phi, leakage, rho),
                               self.angular_residual(x, model),
                               [sum((self.nuf*phi).flat)-1]))

    def balance(self, x, model):
        u, plus, minus, phi, leakage, rho = self.fields(x)
        absorption = sum((self.absorption*phi).flat)
        outflow = self.streaming*sum((plus[:, :, -1]+minus[:, :, 0]).flat)
        source = rho*sum((self.nuf*phi).flat)
        transverse = sum(self.transverse(u, phi, leakage, rho, z, r, g, model)
                         for z in range(self.cells) for r in range(2) for g in range(self.groups))
        defect = absorption+outflow-source
        return dict(absorption=absorption, axial_boundary_outflow=outflow,
                    fission_source=source, net_transverse_term=transverse,
                    physical_balance_defect=defect, relative_physical_balance_defect=defect/source,
                    closed_equation_balance_defect=defect+transverse)

    def positive(self, x):
        # Trial restriction, never clipping. Failure is not a nonexistence proof.
        return bool(np.all(np.asarray(x) > 0) and np.all(self.fields(x)[3] > 0))

    def exact_copy(self):
        def exact(a):
            return np.vectorize(lambda x: Q(str(x)), otypes=[object])(a)
        return replace(self, streaming=Q(str(self.streaming)),
                       **{key: exact(getattr(self, key))
                          for key in ("total", "scatter", "nuf", "chi", "exchange")})


def cases():
    result = []
    for name in ("one_group_uniform", "one_group_axial_material", "one_group_radial_total_contrast"):
        t = np.full((2, 2, 1), 2.0)
        a = np.ones_like(t)
        if name != "one_group_uniform":
            t[1, :, 0] = 2.5
            a[1, :, 0] = [1.2, 0.9]
        if name == "one_group_radial_total_contrast":
            t[:, 1, 0] += 0.25
        nuf = np.zeros_like(t); nuf[:, 0, :] = 1
        result.append(Network(name, 2.0, t, (t-a)[:, :, :, None], nuf, np.ones(1), np.ones((2, 1))))
    for name in ("two_group_one_cell", "two_group_axial_material", "two_group_radial_total_contrast"):
        n = 1 if name == "two_group_one_cell" else 2
        t = np.empty((n, 2, 2)); scatter = np.zeros((n, 2, 2, 2))
        for z in range(n):
            t[z, :, :] = [2+z/4, 2.5+z/4]
            scatter[z, :, 0, 0] = 0.5
            scatter[z, :, 1, 1] = 0.5 if n == 1 else 0.75
            scatter[z, :, 1, 0] = [0.3, 0.4][z]
            scatter[z, :, 0, 1] = [0.1, 0.15][z]
        if name != "two_group_axial_material":
            t[:, 1, :] += 0.25
        nuf = np.zeros_like(t); nuf[:, 0, :] = [1, 0.5]
        result.append(Network(name, 0.5 if n == 1 else 2.0, t, scatter, nuf,
                              np.array([0.75, 0.25]), np.tile([1, 0.75], (n, 1))))
    return result


def complex_jacobian(network, x, model="ratio"):
    x = np.asarray(x, dtype=complex)
    j = np.empty((network.unknowns, network.unknowns))
    for i in range(network.unknowns):
        trial = x.copy(); trial[i] += 1j*1e-30
        j[:, i] = np.imag(network.residual(trial, model))/1e-30
    return j


def direct_reference(network):
    """Linear explicit-exchange eigenproblem, followed by radial fixed-source solve."""
    m = network.radial_size; angular = 2*m
    loss = np.empty((angular, angular)); birth = np.empty_like(loss)
    for i in range(angular):
        x = np.zeros(network.unknowns); x[m+i] = 1
        loss[:, i] = network.angular_residual(x, "explicit_exchange")
        x[-1] = 1
        birth[:, i] = loss[:, i]-network.angular_residual(x, "explicit_exchange")
    eigenvalues, eigenvectors = np.linalg.eig(np.linalg.solve(loss, birth))
    i = int(np.argmax(eigenvalues.real))
    k = eigenvalues[i]
    if abs(k.imag) > 1e-12 or k.real <= 0 or np.max(np.abs(eigenvalues)) > k.real+1e-12:
        raise ValueError("no qualifying dominant real positive eigenvalue")
    x = np.zeros(network.unknowns); x[m:-1] = eigenvectors[:, i].real; x[-1] = 1/k.real
    phi = network.fields(x)[3]
    x[m:-1] /= sum((network.nuf*phi).flat)
    _, _, _, phi, leakage, rho = network.fields(x)
    zero = np.zeros_like(phi)
    offset = network.radial_residual(zero, phi, leakage, rho)
    radial = np.empty((m, m))
    for i in range(m):
        unit = zero.copy(); unit.flat[i] = 1
        radial[:, i] = network.radial_residual(unit, phi, leakage, rho)-offset
    x[:m] = np.linalg.solve(radial, -offset)
    if not network.positive(x) or np.max(np.abs(network.residual(x, "explicit_exchange"))) > 1e-11:
        raise ValueError("explicit reference failed residual/positivity qualification")
    return x, eigenvalues


def solve_ratio(network, seed):
    x = np.array(seed, dtype=float); history = []
    if not network.positive(x):
        raise ValueError("ratio iteration requires a positive seed")
    for iteration in range(61):
        residual = network.residual(x)
        norm = float(np.max(np.abs(residual)))
        history.append(norm)
        if norm <= 1e-11:
            return x, "RESIDUAL_MET", history
        if iteration == 60:
            return x, "ITERATION_CAP", history
        direction = np.linalg.lstsq(complex_jacobian(network, x), -residual, rcond=1e-12)[0]
        for halve in range(20):
            trial = x + (2.0**-halve)*direction
            if network.positive(trial) and np.linalg.norm(network.residual(trial)) < np.linalg.norm(residual):
                x = trial
                break
        else:
            return x, "NO_POSITIVE_DESCENT_STEP", history
    raise AssertionError("unreachable")


def describe(network, x, model):
    u, plus, minus, phi, leakage, rho = network.fields(x)
    j = complex_jacobian(network, x, model)
    singular = np.linalg.svd(j, compute_uv=False)
    return {"state": x.tolist(), "k": float(1/rho), "radial_field": u.tolist(),
            "scalar_flux": phi.tolist(), "leakage": leakage.tolist(),
            "residual": network.residual(x, model).tolist(),
            "max_abs_residual": float(np.max(np.abs(network.residual(x, model)))),
            "minimum_scalar_flux": float(np.min(phi)), "minimum_radial_flux": float(np.min(u)),
            "minimum_nonvacuum_angular_flux": float(np.min(x[network.radial_size:-1])),
            "jacobian": j.tolist(), "singular_values": singular.tolist(),
            "relative_smallest_singular_value": float(singular[-1]/singular[0]),
            "rank_at_relative_threshold": {str(t): int(np.sum(singular > t*singular[0]))
                                           for t in (1e-8, 1e-10, 1e-12)},
            "balance": {key: float(value) for key, value in network.balance(x, model).items()}}


def exact_one_cell(network):
    """Independent rational rank-one fission reference and full residual Jacobians."""
    net = network.exact_copy()
    if net.cells != 1:
        raise ValueError("one-cell exact control only")
    g = net.groups; m = net.radial_size
    loss = [[Q(0) for _ in range(m)] for _ in range(m)]
    for r in range(2):
        for h in range(g):
            i = r*g+h
            for k in range(g):
                loss[i][r*g+k] -= net.scatter[0, r, h, k]
            loss[i][i] += net.total[0, r, h]+2*net.streaming+net.exchange[0, h]
            loss[i][(1-r)*g+h] -= net.exchange[0, h]
    source = [net.chi[i] if i < g else Q(0) for i in range(m)]
    reduced, pivots = rref([row+[b] for row, b in zip(loss, source)])
    if pivots != list(range(m)):
        raise ValueError("singular exact loss operator")
    response = [row[-1] for row in reduced]
    k = sum(a*b for a, b in zip(net.nuf.flat, response))
    phi = [v/k for v in response]
    reference = phi + [v for p in phi for v in (p, p)] + [1/k]
    records = []
    for scale in (Q(1, 2), Q(1), Q(2)):
        x = reference.copy()
        x[2*m:-1] = [scale*v for v in x[2*m:-1]]
        variables = [Dual(v, tuple(Q(i == j) for j in range(net.unknowns))) for i, v in enumerate(x)]
        residual = net.residual(variables)
        j = [list(row.derivative) for row in residual]
        rank, null = rank_and_nullspace(j)
        if any(row.value for row in residual):
            raise AssertionError("exact multigroup family does not satisfy equations")
        records.append({"reflector_scale": str(scale), "state": list(map(str, x)),
                        "k": str(k), "residual": [str(row.value) for row in residual],
                        "jacobian_rank": rank, "nullspace": [[str(v) for v in row] for row in null],
                        "jacobian": [[str(v) for v in row] for row in j],
                        "balance": {key: str(value) for key, value in net.balance(x, "ratio").items()}})
    variables = [Dual(v, tuple(Q(i == j) for j in range(net.unknowns))) for i, v in enumerate(reference)]
    residual = net.residual(variables, "explicit_exchange")
    j = [list(row.derivative) for row in residual]
    if any(row.value for row in residual):
        raise AssertionError("nonzero exact explicit-reference residual")
    return {"family": records, "explicit_exchange_rank": rank_and_nullspace(j)[0],
            "explicit_exchange_state": list(map(str, reference)),
            "explicit_exchange_jacobian": [[str(v) for v in row] for row in j]}


def boundary_root_diagnostic(network, candidate):
    """Solve an explicitly inadmissible zero-reflector problem; never repair a state."""
    m = network.radial_size
    x = np.array(candidate, dtype=float)
    x[2*m:-1] = 0.0
    # Residual order is radial, fuel angular, reflector angular, normalization.
    keep = list(range(2*m)) + [network.unknowns-1]
    history = []
    for iteration in range(11):
        residual = network.residual(x)
        norm = float(np.max(np.abs(residual)))
        history.append(norm)
        if norm <= 1e-13:
            break
        if iteration == 10:
            raise ValueError("boundary diagnostic reached its declared iteration cap")
        j = complex_jacobian(network, x)
        x[keep] += np.linalg.solve(j[np.ix_(keep, keep)], -residual[keep])
    result = describe(network, x, "ratio")
    result.update(classification="INADMISSIBLE_ZERO_REFLECTOR_BOUNDARY_ROOT",
                  admissible_active_domain=False, history=history)
    return result


def run():
    reports = []
    for network in cases():
        ref, eig = direct_reference(network)
        record = {"name": network.name, "cells": network.cells, "groups": network.groups,
                  "unknowns": network.unknowns, "streaming": float(network.streaming),
                  "coefficients": {key: getattr(network, key).tolist()
                                   for key in ("total", "scatter", "nuf", "chi", "exchange")},
                  "explicit_exchange": describe(network, ref, "explicit_exchange"),
                  "linear_reference_eigenvalues": [[float(v.real), float(v.imag)] for v in eig],
                  "ratio_attempts": []}
        for scale in (0.5, 1.0, 2.0):
            seed = ref.copy(); seed[2*network.radial_size:-1] *= scale
            solved, status, history = solve_ratio(network, seed)
            attempt = describe(network, solved, "ratio")
            attempt.update(reflector_seed_scale=scale, status=status, history=history)
            record["ratio_attempts"].append(attempt)
        if network.name == "two_group_one_cell":
            record["exact_rational_control"] = exact_one_cell(network)
        reports.append(record)
    return {"classification": "MANUFACTURED_HETEROGENEOUS_MULTIGROUP_QUALIFICATION",
            "numpy_version": np.__version__, "cases": reports,
            "limits": ["No D4 Jacobian or CE/POD error attribution.",
                       "Bounded solver failures do not prove absence of positive solutions.",
                       "Only the one-cell two-group control has exact rational rank decisions.",
                       "Explicit exchange changes the transverse closure and is not a 3D transport reference."]}


def boundary_run(summary):
    networks = cases()
    if [c["name"] for c in summary["cases"]] != [n.name for n in networks]:
        raise ValueError("boundary follow-up requires the complete declared case matrix")
    return {"scope": "Separately declared inadmissible-boundary diagnostic; original attempts preserved.",
            "cases": [{"name": n.name, **boundary_root_diagnostic(n, c["ratio_attempts"][1]["state"])}
                      for n, c in zip(networks, summary["cases"])]}


def main():
    if len(sys.argv) == 4 and sys.argv[1] == "--boundary":
        out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=False)
        result = boundary_run(json.loads(Path(sys.argv[2]).read_text()))
        (out/"boundary_roots.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
        print("Six explicitly inadmissible zero-reflector boundary diagnostics written.")
        return
    if len(sys.argv) != 2:
        raise SystemExit("usage: qualify_coupled_reference_extended.py [--boundary SUMMARY_JSON] NEW_OUTPUT_DIRECTORY")
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=False)
    result = run()
    (out/"summary.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    for case in result["cases"]:
        print(case["name"], "reference k", case["explicit_exchange"]["k"])
        for attempt in case["ratio_attempts"]:
            print(" ", attempt["reflector_seed_scale"], attempt["status"],
                  "residual", attempt["max_abs_residual"],
                  "rank", attempt["rank_at_relative_threshold"],
                  "balance", attempt["balance"]["relative_physical_balance_defect"])


if __name__ == "__main__":
    main()
