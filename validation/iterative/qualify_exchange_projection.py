#!/usr/bin/env python3
"""Same-operator fixed-space POD study for conservative S2 radial networks.

This standalone experiment never reads D4 states or writes production inputs.
"""
from dataclasses import dataclass
import json
from pathlib import Path
import sys

import numpy as np

from qualify_coupled_reference_extended import cases as previous_cases, direct_reference


@dataclass(frozen=True)
class ExchangeNetwork:
    name: str
    streaming: float
    weights: np.ndarray
    total: np.ndarray  # plane, region, group
    scatter: np.ndarray  # plane, region, destination, incident group
    nuf: np.ndarray
    chi: np.ndarray
    transfer: np.ndarray  # plane, group, destination region, incident region

    def __post_init__(self):
        n, r, g = self.total.shape
        if self.weights.shape != (r,) or np.any(self.weights <= 0):
            raise ValueError("positive radial weights required")
        if self.scatter.shape != (n, r, g, g) or self.nuf.shape != (n, r, g):
            raise ValueError("material dimensions disagree")
        if self.transfer.shape != (n, g, r, r) or self.chi.shape != (g,):
            raise ValueError("transfer/source dimensions disagree")
        arrays = (self.weights, self.total, self.scatter, self.nuf, self.chi, self.transfer)
        if any(not np.isfinite(a).all() for a in arrays) or self.streaming <= 0:
            raise ValueError("finite inputs and positive streaming required")
        if np.any(self.scatter < 0) or np.any(self.nuf < 0) or np.any(self.chi < 0):
            raise ValueError("nonnegative source coefficients required")
        if np.any(self.absorption <= 0) or not np.isclose(sum(self.chi), 1, atol=1e-14, rtol=0):
            raise ValueError("positive absorption and normalized chi required")
        for matrix in self.transfer.reshape(-1, r, r):
            if np.max(np.abs(self.weights @ matrix)) > 1e-13:
                raise ValueError("nonconservative radial transfer")
            weighted = self.weights[:, None]*matrix
            if not np.allclose(weighted, weighted.T, atol=1e-13, rtol=0):
                raise ValueError("declared graph exchange must have symmetric conductance")

    @property
    def cells(self):
        return self.total.shape[0]

    @property
    def regions(self):
        return self.total.shape[1]

    @property
    def groups(self):
        return self.total.shape[2]

    @property
    def size(self):
        return 2*self.total.size

    @property
    def absorption(self):
        return self.total-self.scatter.sum(axis=2)

    def fields(self, angular):
        raw = np.asarray(angular).reshape(self.regions, self.groups, 2, self.cells)
        zero = np.zeros((self.regions, self.groups, 1), dtype=raw.dtype)
        plus = np.concatenate((zero, raw[:, :, 0]), axis=2)
        minus = np.concatenate((raw[:, :, 1], zero), axis=2)
        phi = ((plus[:, :, :-1]+plus[:, :, 1:]+minus[:, :, :-1]+minus[:, :, 1:])/2).transpose(2, 0, 1)
        return plus, minus, phi

    def production(self, angular):
        return float(np.sum(self.weights[None, :, None]*self.nuf*self.fields(angular)[2]))

    def residual(self, angular, rho):
        plus, minus, phi = self.fields(angular)
        rows = []
        for r in range(self.regions):
            for g in range(self.groups):
                for z in range(self.cells):
                    transverse = self.transfer[z, g, r] @ phi[z, :, g]
                    source = self.scatter[z, r, g] @ phi[z, r]
                    source += rho*self.chi[g]*(self.nuf[z, r] @ phi[z, r])
                    for sign, face in ((1, plus), (-1, minus)):
                        left, right = face[r, g, z:z+2]
                        rows.append(sign*self.streaming*(right-left)
                                    + self.total[z, r, g]*(left+right)/2
                                    + transverse/2-source/2)
        return np.asarray(rows)

    def operators(self):
        loss = np.empty((self.size, self.size)); birth = np.empty_like(loss)
        for i in range(self.size):
            unit = np.zeros(self.size); unit[i] = 1
            loss[:, i] = self.residual(unit, 0)
            birth[:, i] = loss[:, i]-self.residual(unit, 1)
        return loss, birth

    def row_weights(self):
        return np.repeat(self.weights, self.groups*self.cells*2)

    def balance(self, angular, rho):
        plus, minus, phi = self.fields(angular)
        absorption = float(np.sum(self.weights[None, :, None]*self.absorption*phi))
        outflow = float(self.streaming*np.sum(self.weights[:, None]*(plus[:, :, -1]+minus[:, :, 0])))
        source = rho*self.production(angular)
        transfer = sum(self.weights @ (self.transfer[z, g] @ phi[z, :, g])
                       for z in range(self.cells) for g in range(self.groups))
        return dict(absorption=absorption, axial_boundary_outflow=outflow,
                    fission_source=source, net_radial_transfer=float(transfer),
                    physical_balance_defect=absorption+outflow-source,
                    relative_physical_balance_defect=(absorption+outflow-source)/source)


def networks():
    result = []
    for old in previous_cases():
        c = np.empty((old.cells, old.groups, 2, 2))
        for z in range(old.cells):
            for g in range(old.groups):
                c[z, g] = old.exchange[z, g]*np.array([[1., -1.], [-1., 1.]])
        result.append(ExchangeNetwork(old.name, old.streaming, np.ones(2), old.total.copy(),
                                      old.scatter.copy(), old.nuf.copy(), old.chi.copy(), c))
    weights = np.array([1., 2., 1.5, 1.])
    graph = np.zeros((4, 4))
    for i, j, coefficient in ((0, 1, .8), (1, 2, .6), (2, 3, .4), (0, 2, .15)):
        graph[i, i] += coefficient; graph[j, j] += coefficient
        graph[i, j] -= coefficient; graph[j, i] -= coefficient
    for layered in (False, True):
        t = np.empty((2, 4, 2)); scatter = np.zeros((2, 4, 2, 2)); c = np.empty((2, 2, 4, 4))
        for z in range(2):
            t[z] = (np.array([[2., 2.5], [2.1, 2.6], [2.25, 2.75], [2.4, 2.9]])+z*.25
                    if layered else np.tile([2., 2.5], (4, 1)))
            scatter[z, :, 0, 0] = .5; scatter[z, :, 1, 1] = .75
            scatter[z, :, 1, 0] = [.3, .4][z] if layered else .3
            scatter[z, :, 0, 1] = [.1, .15][z] if layered else .1
            for g in range(2):
                c[z, g] = graph/weights[:, None]*[1., .7][g]*(1.+.1*z if layered else 1.)
        nuf = np.tile([[1., .5], [.8, .4], [0., 0.], [0., 0.]], (2, 1, 1))
        result.append(ExchangeNetwork("four_region_layered" if layered else "four_region_uniform",
                                      2., weights.copy(), t, scatter, nuf, np.array([.75, .25]), c))
    return result


def snapshots(net):
    """Prescribed radial fixed-source data only; no full axial solution is used."""
    columns = []; receipts = []
    r, g = net.regions, net.groups
    for z in range(net.cells):
        for leakage in (.5, 1.5, 3.):
            loss = np.zeros((r*g, r*g))
            for i in range(r):
                for h in range(g):
                    row = i*g+h
                    loss[row, row] += net.total[z, i, h]+leakage
                    for j in range(r):
                        loss[row, j*g+h] += net.transfer[z, h, i, j]
                    loss[row, i*g:(i+1)*g] -= net.scatter[z, i, h]
            for source_region in range(r):
                if not np.any(net.nuf[z, source_region] > 0):
                    continue
                source = np.zeros((r, g)); source[source_region] = net.chi/net.weights[source_region]
                raw = np.linalg.solve(loss, source.ravel()).reshape(r, g)
                norm = float(np.sum(net.weights[:, None]*net.nuf[z]*raw))
                if norm <= 0 or np.min(raw) <= 0:
                    raise ValueError("inadmissible radial training snapshot")
                columns.append(raw/norm)
                receipts.append(dict(plane=z, prescribed_leakage=leakage, source_region=source_region,
                                     source_integral=float(np.sum(net.weights[:, None]*source)),
                                     raw_fission_production=norm,
                                     max_fixed_source_residual=float(np.max(np.abs(loss@raw.ravel()-source.ravel())))))
    return np.stack(columns, axis=2), receipts  # region, group, snapshot


def canonical_columns(matrix):
    result = matrix.copy()
    for j in range(result.shape[1]):
        if result[np.argmax(np.abs(result[:, j])), j] < 0:
            result[:, j] *= -1
    return result


def spaces(net, training):
    plain = []; enriched = []; spectra = []
    root_w = np.sqrt(net.weights)
    constant = root_w/np.linalg.norm(root_w)
    for g in range(net.groups):
        weighted = root_w[:, None]*training[:, g]
        u, s, _ = np.linalg.svd(weighted, full_matrices=True)
        residual = weighted-constant[:, None]*(constant @ weighted)[None, :]
        uc, sc, _ = np.linalg.svd(residual, full_matrices=True)
        plain.append(canonical_columns(u)/root_w[:, None])
        enriched.append(np.column_stack((constant, canonical_columns(uc[:, :net.regions-1])))/root_w[:, None])
        spectra.append(dict(plain=s.tolist(), constant_removed=sc.tolist()))
    return dict(plain_pod=plain, constant_enriched_pod=enriched), spectra


def lifts(net, basis):
    """Face trial lift and cell/angle test lift deliberately have different row order."""
    if len(basis) != net.groups:
        raise ValueError("one radial basis per group is required")
    ranks = [b.shape[1] for b in basis]
    if any(b.shape[0] != net.regions or k < 1 or np.linalg.matrix_rank(b) != k
           for b, k in zip(basis, ranks)):
        raise ValueError("independent radial trial vectors required")
    size = 2*net.cells*sum(ranks)
    p = np.zeros((net.size, size)); q = np.zeros_like(p)
    col = 0
    for g, b in enumerate(basis):
        for mode in range(b.shape[1]):
            for angle in range(2):
                for z in range(net.cells):
                    for r in range(net.regions):
                        row = np.ravel_multi_index((r, g, angle, z), (net.regions, net.groups, 2, net.cells))
                        p[row, col] = b[r, mode]
                    col += 1
    col = 0
    for g, b in enumerate(basis):
        for mode in range(b.shape[1]):
            for z in range(net.cells):
                for angle in range(2):
                    for r in range(net.regions):
                        row = np.ravel_multi_index((r, g, z, angle), (net.regions, net.groups, net.cells, 2))
                        q[row, col] = b[r, mode]
                    col += 1
    return p, q


def projected_eigenpair(net, loss, birth, basis):
    p, q = lifts(net, basis)
    test = q.T*net.row_weights()[None, :]
    lr, fr = test@loss@p, test@birth@p
    eigenvalues, vectors = np.linalg.eig(np.linalg.solve(lr, fr))
    index = int(np.argmax(eigenvalues.real))
    k = eigenvalues[index]
    if abs(k.imag) > 1e-11 or k.real <= 0 or np.max(np.abs(eigenvalues)) > k.real+1e-11:
        raise ValueError("no declared dominant real positive eigenpair")
    if np.max(np.abs(vectors[:, index].imag)) > 1e-11:
        raise ValueError("complex dominant mode")
    modal = vectors[:, index].real
    production = net.production(p@modal)
    if abs(production) <= 1e-14:
        raise ValueError("vanishing fission normalization")
    modal /= production
    angular = p@modal
    return angular, float(k.real), modal, lr, fr, test


def weighted_norm(net, phi):
    return float(np.sqrt(np.sum(net.weights[None, :, None]*phi*phi)))


def describe(net, loss, birth, basis, training, reference):
    angular, k, modal, lr, fr, test = projected_eigenpair(net, loss, birth, basis)
    rho = 1/k
    phi = net.fields(angular)[2]
    rphi = net.fields(np.asarray(reference["angular"]))[2]
    residual = loss@angular-rho*(birth@angular)
    constant_defects = []; gram = []; snapshot_errors = []
    for g, b in enumerate(basis):
        mass = b.T@(net.weights[:, None]*b)
        gram.append(mass.tolist())
        constant_projection = b@np.linalg.solve(mass, b.T@net.weights)
        constant_defects.append(float(np.sqrt(np.sum(net.weights*(1-constant_projection)**2)/sum(net.weights))))
        snap = training[:, g]
        reconstructed = b@np.linalg.solve(mass, b.T@(net.weights[:, None]*snap))
        snapshot_errors.append(float(np.sqrt(np.sum(net.weights[:, None]*(snap-reconstructed)**2)
                                                   /np.sum(net.weights[:, None]*snap*snap))))
    balance = net.balance(angular, rho)
    return dict(k=k, inverse_k=rho, angular=angular.tolist(), scalar_flux=phi.tolist(),
                modal_coefficients=modal.tolist(), basis=[b.tolist() for b in basis], gram=gram,
                reduced_loss=lr.tolist(), reduced_fission=fr.tolist(),
                minimum_scalar_flux=float(phi.min()), minimum_nonvacuum_angular_flux=float(angular.min()),
                positive_scalar=bool(np.all(phi > 0)), positive_nonvacuum_angular=bool(np.all(angular > 0)),
                max_full_local_residual=float(np.max(np.abs(residual))),
                max_projected_residual=float(np.max(np.abs(test@residual))),
                normalized_weighted_flux_error=weighted_norm(net, phi-rphi)/weighted_norm(net, rphi),
                reactivity_difference_pcm=1e5*(1/reference["k"]-rho),
                constant_space_defect_by_group=constant_defects,
                snapshot_projection_error_by_group=snapshot_errors,
                balance=balance,
                weighted_residual_balance_identity_error=float(net.row_weights()@residual-balance["physical_balance_defect"]))


def run():
    reports = []
    old_cases = {case.name: case for case in previous_cases()}
    for net in networks():
        loss, birth = net.operators()
        identity = [np.eye(net.regions) for _ in range(net.groups)]
        angular, k, _, _, _, _ = projected_eigenpair(net, loss, birth, identity)
        reference = dict(angular=angular.tolist(), k=k)
        training, receipts = snapshots(net)
        families, spectra = spaces(net, training)
        record = dict(name=net.name, cells=net.cells, regions=net.regions, groups=net.groups,
                      streaming=net.streaming, weights=net.weights.tolist(),
                      coefficients={name: getattr(net, name).tolist() for name in ("total", "scatter", "nuf", "chi", "transfer")},
                      full_loss=loss.tolist(), full_fission=birth.tolist(),
                      training=training.tolist(), snapshot_receipts=receipts, snapshot_spectra=spectra,
                      reference=describe(net, loss, birth, identity, training, reference), approximations=[])
        if net.name in old_cases:
            old = old_cases[net.name]; old_state, _ = direct_reference(old)
            record["previous_reference_recovery"] = dict(absolute_k_error=abs(k-1/old_state[-1]),
                max_angular_error=float(np.max(np.abs(angular-old_state[old.radial_size:-1]))))
        for family, complete in families.items():
            for rank in range(1, net.regions+1):
                entry = describe(net, loss, birth, [b[:, :rank] for b in complete], training, reference)
                entry.update(family=family, radial_rank_per_group=rank)
                record["approximations"].append(entry)
        # Invertible nonorthogonal coordinates test retained Gram/mass terms.
        transform = np.diag(np.arange(1, net.regions+1, dtype=float))
        for j in range(net.regions-1):
            transform[j, j+1] = .2
        changed = [b@transform for b in families["plain_pod"]]
        record["nonorthogonal_full_control"] = describe(net, loss, birth, changed, training, reference)
        reports.append(record)
    return dict(classification="CONSERVATIVE_NETWORK_SAME_OPERATOR_POD_COMPARISON",
                numpy_version=np.__version__, cases=reports,
                limits=["Manufactured network projection, not D4 or native radial transport.",
                        "Explicit exchange differs from the production ratio closure.",
                        "Training uses declared fixed-source solves, never the reference eigenflux.",
                        "Conservation does not by itself establish accuracy or positivity.",
                        "Rank errors are not assumed to decrease monotonically."])


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: qualify_exchange_projection.py NEW_OUTPUT_DIRECTORY")
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=False)
    result = run()
    (out/"summary.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    for case in result["cases"]:
        print(case["name"], "reference k", case["reference"]["k"])
        for entry in case["approximations"]:
            print(" ", entry["family"], entry["radial_rank_per_group"],
                  "flux error", entry["normalized_weighted_flux_error"],
                  "pcm", entry["reactivity_difference_pcm"],
                  "balance", entry["balance"]["relative_physical_balance_defect"],
                  "positive", entry["positive_scalar"], entry["positive_nonvacuum_angular"])


if __name__ == "__main__":
    main()
