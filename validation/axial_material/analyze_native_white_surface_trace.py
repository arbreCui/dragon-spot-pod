"""Read-only, bounded surface-trace analysis of sealed H20/N4 native fields.

No transport, linear solve, coefficient fitting or production replacement.
The explicit local-trace hypothesis is evaluated on the native volume field;
its discrepancy is reported without defining an accuracy acceptance gate.
"""

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation/axial_material"))
import qualify_refined_AAA_layered_full as full
from probe_refined_AAA_white_odd_response import (
    ART, DiskResources, digest, read, require_file, verify, write_new,
)

OUT = ART / "axial-material-AAA-native-white-surface-trace-analysis-20261006"
NATIVE = full.OUT
ANGULAR = ART / "axial-material-AAA-white-trace-refined-native-angular-response-20261005"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
PRODUCTION = ART / "axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
COMPILED = ART / "axial-material-AAA-white-trace-angular-convergence-20261005/build"
NATIVE_SEAL = "67a1e9e18e180c07f7316181966ed12793f0979c2bdb32b58adcc5407bdd1de0"
ANGULAR_SEAL = "8862154f1fb3458676460f8a4074a1a52070322332dd08e66c2773b0e4345540"
CAUSAL_DECLARATION = "f4a9ecd37a8b224a22869f2d8e670c26d7e8d2cb7af28ba63ecfaeb802dd04b2"
GROUPS = (51, 61, 98)
PERMUTATION = (1, 3, 5, 7, 0, 2, 4, 6)
LIMIT = 5e-12


def _sealed_files(root, seal_sha):
    require_file(root / "seal.json", seal_sha)
    manifest = read(root / "seal.json")["files"]
    # Only the read subset is admitted below, with identities from this seal.
    return {str(root / name): sha for name, sha in manifest.items()}


def _verify_inputs(declaration):
    verify(declaration["files"])
    for path, target in declaration["native_library_aliases"].items():
        if str(Path(path).resolve()) != target:
            raise ValueError("declared numerical library alias changed")
    expected = declaration["numerical_loader_environment"]
    observed = {k: v for k, v in os.environ.items()
                if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}
    if observed != {k: v for k, v in expected.items()
                     if k.startswith("DYLD_") or k == "OPENBLAS_CORETYPE"}:
        raise ValueError("declared numerical loader/dispatch environment changed")


def prepare():
    native_files = _sealed_files(NATIVE, NATIVE_SEAL)
    angular_files = _sealed_files(ANGULAR, ANGULAR_SEAL)
    selected = [NATIVE / n for n in (
        "declaration.json", "result.json", "driver_result.json", "AAA/stages.json",
        "inputs/inventory.npz", "white/h20_n4/geometry.npz")]
    selected += [NATIVE / f"verification/p{p}_h20_n4/operators.npz" for p in range(4)]
    selected += [NATIVE / f"white/h20_n4/g{g}_q32.npz" for g in GROUPS]
    selected += [ANGULAR / f"angular_response_g{g}.npz" for g in GROUPS]
    identities = {**native_files, **angular_files}
    files = {str(p): identities[str(p)] for p in selected}
    verify(files)
    native_result, driver = read(NATIVE / "result.json"), read(NATIVE / "driver_result.json")
    stages = read(NATIVE / "AAA/stages.json")["stages"]
    if (native_result["classification"] != "COMPLETE_CURRENT_DATA_H20_N4_FULL_FIXED_SOURCE_WHITE_ONLY"
            or not native_result["full_current_discrete_fixed_source_qualified"]
            or not native_result["full_current_geometric_white_qualified"]
            or driver["classification"] != "COMPLETE_BOUNDED_CURRENT_FULL_FIXED_SOURCE_WHITE_ONLY"
            or driver["error"] is not None or len(stages) != 368
            or any(s["status"] != "PASS" for s in stages)):
        raise ValueError("terminal sealed native completion required")
    require_file(CAUSAL / "declaration.json", CAUSAL_DECLARATION)
    if (read(CAUSAL / "driver_result.json")["classification"] != "FAILED_CURRENT_LAYERED_COMPARISON_NO_RETRY"
            or (CAUSAL / "seal.json").exists()):
        raise ValueError("retain original terminal comparison failure")
    # Keep the existing environment and execution dependencies pinned.
    causal_declaration = read(CAUSAL / "declaration.json")
    files.update(causal_declaration["files"])
    files.update(read(NATIVE / "declaration.json")["files"])
    files.update(read(ANGULAR / "declaration.json")["files"])
    candidate = ROOT / "validation/axial_material/angular_collision_slab_candidate.py"
    files[str(candidate)] = read(CAUSAL / "declaration.json")["files"][str(candidate)]
    variant = PRODUCTION / "runtime/conditional_white_receiver_variant.json"
    require_file(variant, "1801fe8378d328e110d4d8b0e55107265cf44edde0ec5ac7a2a19a8d2300ed42")
    production_files = read(variant)["files"]
    for name in ("SPOT1P64.f90", "axmat_white_trace_model.f90"):
        path = str(COMPILED / name)
        files[path] = production_files[path]
    extras = [Path(__file__).resolve(), Path(sys.executable).resolve(), Path("/bin/ps"),
        NATIVE / "seal.json", ANGULAR / "seal.json", CAUSAL / "declaration.json",
        CAUSAL / "driver_result.json", CAUSAL / "AAA/stages.json",
        COMPILED / "SPOT1P64.f90", COMPILED / "axmat_white_trace_model.f90",
        PRODUCTION / "runtime/conditional_white_receiver_variant.json",
        ROOT / "validation/axial_material/angular_collision_slab_candidate.py",
        ROOT / "validation/axial_material/white_side_trace_kernel.py"]
    for path in extras:
        files.setdefault(str(path), digest(require_file(path)))
    _verify_inputs(dict(files=files, native_library_aliases=causal_declaration["native_library_aliases"],
        numerical_loader_environment=causal_declaration["numerical_loader_environment"]))
    OUT.mkdir(exist_ok=False)
    for name in ("runtime", "AAA", "runs", "analysis"):
        (OUT / name).mkdir()
    shutil.copy2(NATIVE / "runtime/run_bounded_dragon.py", OUT / "runtime/run_bounded_dragon.py")
    files[str(OUT / "runtime/run_bounded_dragon.py")] = digest(OUT / "runtime/run_bounded_dragon.py")
    roots = sorted(set(read(NATIVE / "declaration.json")["resource_roots"])
        | {str(p.resolve()) for p in ART.glob("axial-material-*") if p.is_dir()} | {str(OUT)})
    resources = DiskResources(ART, roots, 8 * 2**30, 96 * 2**30).check()
    reserve = 32 * 2**20
    if (resources["artifact_bytes"] + reserve >= 96 * 2**30
            or resources["disk_free_bytes"] - reserve < 8 * 2**30):
        raise ValueError("complete offline-analysis storage admission failed")
    write_new(OUT / "declaration.json", dict(
        schema="AXMAT_OFFLINE_NATIVE_SURFACE_TRACE_ANALYSIS_V1", files=files,
        resource_roots=roots, resources_before=resources, archive_reserve_bytes=reserve,
        numeric_environment=read(NATIVE / "declaration.json")["numeric_environment"],
        native_library_aliases=causal_declaration["native_library_aliases"],
        native_library_linkage=causal_declaration["native_library_linkage"],
        numerical_loader_environment=causal_declaration["numerical_loader_environment"],
        native_seal_sha256=NATIVE_SEAL, angular_seal_sha256=ANGULAR_SEAL,
        predecessor_comparison_remains_failed=True, groups=list(GROUPS),
        total_wall_seconds=300, stage_wall_seconds=120, rss_cap_mib=512,
        numeric_children_at_once=1, threads=1, retries=0, fresh_transport_flights=0,
        fresh_linear_solves=0, height_cm=20, coarse_layers=4, native_angular_states=8,
        primitive="E_sfz = angular outgoing current / geometric incoming measure M_sfz",
        hypothesis="Ehat_sfz = b_Na * projected native volume angular mean a_sz",
        weak_wall="b_Na*sum_f(out_sfz-M_sfz*whiteamp_fz)/(omega_s*A_stored*dz)",
        measure_discrepancy_reported_separately=True, model_discrepancy_acceptance_gate=None,
        original_accuracy_thresholds_changed=False, legacy_comparison_failure_waived=False,
        production_equation_changed=False, AAA_accuracy_qualified=False, ABA_admitted=False))
    print(json.dumps({"declaration_sha256": digest(OUT / "declaration.json")}))


def _relative(actual, expected):
    diff = abs(actual - expected).reshape(-1, expected.shape[-1]).max(axis=0)
    scale = abs(expected).reshape(-1, expected.shape[-1]).max(axis=0)
    if ((scale == 0) & (diff != 0)).any():
        raise ValueError("nonzero discrepancy at exactly zero archived field")
    import numpy as np
    return np.divide(diff, scale, out=np.zeros_like(diff), where=scale > 0)


def _weighted(actual, expected, weights):
    import numpy as np
    axes = tuple(range(weights.ndim))
    num = (((actual - expected)**2) * weights[..., None]).sum(axis=axes)
    den = ((expected**2) * weights[..., None]).sum(axis=axes)
    # No floor or acceptance decision; exactly zero norm is explicitly null.
    ratio = np.sqrt(np.divide(num, den, out=np.zeros_like(num), where=den > 0))
    return [float(v) if d > 0 else None for v, d in zip(ratio, den, strict=True)], num, den


def worker(expected_declaration):
    import numpy as np
    from angular_collision_slab_candidate import source_family
    from white_side_trace_kernel import trace_exchange
    tick = time.monotonic()
    require_file(OUT / "declaration.json", expected_declaration)
    declaration = read(OUT / "declaration.json")
    claim = read(OUT / "execution_claim.json")
    if claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected_declaration:
        raise ValueError("own bounded parent execution claim required")
    stages = read(OUT / "AAA/stages.json")["stages"]
    if (len(stages) != 1 or stages[0]["status"] != "RUNNING"
            or stages[0]["command"] != [sys.executable, *sys.argv]):
        raise ValueError("actual bounded analysis child admission required")
    actual_env = dict(python=sys.version.split()[0], numpy=np.__version__)
    if any(actual_env[k] != declaration["numeric_environment"][k] for k in actual_env):
        raise ValueError("unchanged declared numerical environment required")
    _verify_inputs(declaration)
    if any(os.environ.get(k) != "1" for k in (
            "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")):
        raise ValueError("actual analysis child must use one numerical thread")
    with np.load(NATIVE / "inputs/inventory.npz", allow_pickle=False) as z:
        volumes = z["weights"][:8].copy()
        zmu, wzmu = z["zmu"].copy(), z["wzmu"].copy()
    with np.load(NATIVE / "white/h20_n4/geometry.npz", allow_pickle=False) as z:
        radial_measure = z["radial"].copy()
    perm = np.array(PERMUTATION)
    measure = radial_measure[perm].reshape(8, 6, 4)
    if not np.isfinite(measure).all() or (measure <= 0).any():
        raise ValueError("strictly positive geometric incoming measures required")
    native_ops = []
    for p in range(4):
        with np.load(NATIVE / f"verification/p{p}_h20_n4/operators.npz", allow_pickle=False) as z:
            if not np.array_equal(z["coverage"], np.ones_like(z["coverage"])):
                raise ValueError("complete native record coverage required")
            native_ops.append(z["operators"][1].sum(axis=2))
    # Stored axes: order, group, axial sign, orientation, output, input.
    ops = np.concatenate(native_ops, axis=1)
    if ops.shape != (3, 8, 72, 66):
        raise ValueError("unchanged group/state/operator layout required")
    area = sum(float(v) for v in volumes)
    dz = 5.0
    summaries = []
    for gi, group in enumerate(GROUPS):
        with np.load(ANGULAR / f"angular_response_g{group}.npz", allow_pickle=False) as z:
            b = z["source_lifting"][:8, 0].copy()
            mu, omega, testing = z["native_mu"].copy(), z["omega"].copy(), z["testing"][:1, :8].ravel().copy()
            gram = float(z["gram"])
        if not np.isfinite(b).all() or (b <= 0).any():
            raise ValueError("fixed positive rank1 basis required")
        family = source_family(mu)
        sources = family["sources"]
        native_mu = np.array([sign * m for m in np.sqrt(1 - 1 / zmu**2) for sign in (-1, 1)])
        native_omega = np.repeat(wzmu * zmu / 2, 2)
        weights = volumes / area
        gram_check = 0.0
        for w, value in zip(weights, b, strict=True):
            gram_check += float(w) * float(value) * float(value)
        if (not np.array_equal(mu, native_mu[perm])
                or not np.array_equal(omega, native_omega[perm]) or gram != gram_check
                or not np.array_equal(testing, weights * b / gram)
                or sources.shape != (8, 4, 38) or len(family["labels"]) != 38
                or not np.array_equal(sources[:, :, :32].reshape(32, 32), np.eye(32))):
            raise ValueError("unchanged complete angular/basis/source convention required")
        coefficients = sources.reshape(32, 38)
        lift = np.zeros((256, 32))
        for angle, state in enumerate(PERMUTATION):
            for region in range(8):
                for layer in range(4):
                    lift[state * 32 + region * 4 + layer, angle * 4 + layer] = b[region]
        with np.load(NATIVE / f"white/h20_n4/g{group}_q32.npz", allow_pickle=False) as z:
            amplitudes = z["white_amplitudes"][:, :256] @ lift @ coefficients
            saved_phi = z["white_phi"][:, :256] @ lift @ coefficients
            saved_jz = z["white_jz"][:, :256] @ lift @ coefficients
        x = np.zeros((8, 66, 38))
        x[:, :32] = (lift @ coefficients).reshape(8, 32, 38)
        x[:, 32:56] = amplitudes[None]
        y = np.einsum("srk,skc->src", ops[gi], x, optimize=True)
        with (OUT / "analysis" / f"raw_g{group}.npz").open("xb") as handle:
            np.savez_compressed(handle, operator=ops[gi], inputs=x, outputs=y,
                angular_to_full=perm, source_lifting=lift, source_coefficients=coefficients,
                sources=sources, volume=volumes, mu=mu, omega=omega, basis=b,
                gram=gram, testing=testing, geometric_incoming_measure=measure,
                actual_white_amplitudes=amplitudes, saved_phi=saved_phi, saved_jz=saved_jz)
        if not np.isfinite(y).all() or (y < 0).any():
            raise ValueError("positive finite sealed response action required")
        complete = y[perm, :32].reshape(8, 8, 4, 38) / (omega[:, None, None, None] * volumes[None, :, None, None] * dz)
        projected = np.einsum("r,srzc->szc", testing, complete)
        outgoing = y[perm, 32:56].reshape(8, 6, 4, 38)
        amp = amplitudes.reshape(6, 4, 38)
        incoming = measure[..., None] * amp[None]
        trace = outgoing / measure[..., None]
        estimated_trace = np.broadcast_to(b[0] * projected[:, None], trace.shape).copy()
        estimated_amp = (measure[..., None] * estimated_trace).sum(axis=0) / measure.sum(axis=0)[..., None]
        reconstructed_amp = outgoing.sum(axis=0) / measure.sum(axis=0)[..., None]
        scalar = y[:, :32].sum(axis=0) / np.repeat(volumes * dz, 4)[:, None]
        full_mu = np.empty(8)
        full_mu[perm] = mu
        jz = np.einsum("s,src->rc", full_mu, y[:, :32]) / np.repeat(volumes * dz, 4)[:, None]
        checks = dict(white_closure=float(_relative(reconstructed_amp, amp).max()),
            scalar_reconstruction=float(_relative(scalar, saved_phi).max()),
            signed_jz_reconstruction=float(_relative(jz, saved_jz).max()))
        if max(checks.values()) >= LIMIT:
            raise ValueError("unchanged archived response/white closure reconstruction failed")
        native_wall = b[0] * (outgoing - incoming).sum(axis=1) / (omega[:, None, None] * area * dz)
        kernel = trace_exchange(mu, 2 * omega, 6 * .61776479, area)
        conditional_wall = b[0]**2 * np.einsum("st,tzc->szc", kernel, projected)
        geometric_prefactor = measure.sum(axis=1) / (omega[:, None] * area * dz)
        ideal_prefactor = (6 * .61776479 / (np.pi * area)) * np.sqrt(1 - mu**2)
        trace_error, tn, td = _weighted(estimated_trace, trace, measure)
        amplitude_error, an, ad = _weighted(estimated_amp, amp, measure.sum(axis=0))
        wall_error, wn, wd = _weighted(conditional_wall, native_wall, omega[:, None] * np.full((1, 4), dz))
        transfer = ops[gi, :, 32:56, 32:56].sum(axis=0) / radial_measure.sum(axis=0)[:, None]
        cross_layer = np.arange(24)[:, None] % 4 != np.arange(24)[None, :] % 4
        fraction = (transfer * cross_layer).sum(axis=0) / transfer.sum(axis=0)
        arrays = dict(mu=mu, omega=omega, basis=b, gram=gram, source_labels=np.array(family["labels"]),
            sources=sources, complete_volume_angular_means=complete, projected_volume_angular_means=projected,
            geometric_incoming_measure=measure, actual_radial_outgoing=outgoing, actual_radial_incoming=incoming,
            actual_surface_trace=trace, conditional_surface_trace=estimated_trace,
            actual_white_amplitude=amp, conditional_white_amplitude=estimated_amp,
            reconstructed_white_amplitude=reconstructed_amp, native_weak_wall=native_wall,
            conditional_weak_wall=conditional_wall, trace_numerator=tn, trace_denominator=td,
            amplitude_numerator=an, amplitude_denominator=ad, wall_numerator=wn, wall_denominator=wd,
            geometric_prefactor=geometric_prefactor, ideal_prefactor=ideal_prefactor,
            native_white_transfer=transfer, cross_layer_mask=cross_layer, cross_layer_transfer_fraction=fraction)
        if any(not np.isfinite(v).all() for k, v in arrays.items() if k != "source_labels"):
            raise ValueError("nonfinite offline diagnostic")
        path = OUT / "analysis" / f"g{group}.npz"
        with path.open("xb") as handle:
            np.savez_compressed(handle, **arrays)
        summaries.append(dict(group=group, archive_sha256=digest(path), original_reconstruction_checks=checks,
            trace_weighted_l2_by_source=trace_error, white_amplitude_weighted_l2_by_source=amplitude_error,
            weak_wall_weighted_l2_by_source=wall_error,
            geometric_vs_ideal_prefactor_relative=float(abs(geometric_prefactor - ideal_prefactor[:, None]).max() / abs(ideal_prefactor).max()),
            cross_layer_transfer_fraction_min=float(fraction.min()), cross_layer_transfer_fraction_max=float(fraction.max())))
    write_new(OUT / "analysis/result.json", dict(
        classification="COMPLETE_OFFLINE_SURFACE_TRACE_ANALYSIS_NOT_QUALIFICATION",
        groups=summaries, complete_source_columns_each_group=38, response_applications=3,
        fresh_transport_flights=0, fresh_linear_solves=0, elapsed_seconds=time.monotonic() - tick,
        original_reconstruction_gate=LIMIT, model_discrepancy_acceptance_gate=None,
        local_trace_hypothesis_only=True, production_equation_changed=False,
        predecessor_comparison_remains_failed=True, AAA_accuracy_qualified=False, ABA_admitted=False))
    print("AXMAT-OFFLINE-SURFACE-TRACE-COMPLETE", flush=True)


def run(expected_declaration):
    require_file(OUT / "declaration.json", expected_declaration)
    declaration = read(OUT / "declaration.json")
    _verify_inputs(declaration)
    resource = DiskResources(ART, declaration["resource_roots"], 8 * 2**30, 96 * 2**30)
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected_declaration))
    runner = full.OwnRSSSerialExecutor(OUT, declaration["total_wall_seconds"], "AAA", resource)
    started = time.monotonic()
    error = None
    try:
        runner.execute(OUT / "runs", "surface_trace", [sys.executable, str(Path(__file__).resolve()),
            "worker", "--declaration-sha", expected_declaration], declaration["stage_wall_seconds"],
            marker="AXMAT-OFFLINE-SURFACE-TRACE-COMPLETE")
        _verify_inputs(declaration)
        stages = read(OUT / "AAA/stages.json")["stages"]
        watch = read(OUT / "runs/surface_trace.watchdog.json")
        result = read(OUT / "analysis/result.json")
        if (len(stages) != 1 or stages[0]["status"] != "PASS"
                or watch["returncode"] != 0 or watch["limit_failure"] is not None
                or not 0 <= watch["elapsed_seconds"] < 120
                or not 0 <= watch["sampled_peak_rss_mib"] < 512
                or watch["own_child_only"] is not True or watch["liveness_group_cleanup"] is not True
                or result["classification"] != "COMPLETE_OFFLINE_SURFACE_TRACE_ANALYSIS_NOT_QUALIFICATION"
                or [g["group"] for g in result["groups"]] != list(GROUPS)
                or result["complete_source_columns_each_group"] != 38
                or result["fresh_linear_solves"] != 0 or result["fresh_transport_flights"] != 0
                or result["AAA_accuracy_qualified"] is not False or result["ABA_admitted"] is not False
                or result["predecessor_comparison_remains_failed"] is not True):
            raise ValueError("actual terminal bounded offline scope required")
    except BaseException as exc:
        error = repr(exc)
        raise
    finally:
        write_new(OUT / "driver_result.json", dict(
            classification="COMPLETE_BOUNDED_OFFLINE_ANALYSIS_ONLY" if error is None else "FAILED_OFFLINE_ANALYSIS_NO_RETRY",
            error=error, elapsed_seconds=time.monotonic() - started,
            fresh_transport_flights=0, fresh_linear_solves=0, AAA_accuracy_qualified=False, ABA_admitted=False))
    outputs = {str(p.relative_to(OUT)): digest(require_file(p)) for p in OUT.rglob("*") if p.is_file()}
    if sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file()) >= declaration["archive_reserve_bytes"]:
        raise ValueError("declared complete offline archive reserve exceeded")
    write_new(OUT / "seal.json", dict(classification="SEALED_COMPLETE_OFFLINE_ANALYSIS_ONLY", files=outputs,
        predecessor_comparison_remains_failed=True, AAA_accuracy_qualified=False, ABA_admitted=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run", "worker"))
    parser.add_argument("--declaration-sha")
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    elif args.mode == "run":
        run(args.declaration_sha)
    else:
        worker(args.declaration_sha)
