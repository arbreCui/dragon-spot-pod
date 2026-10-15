"""Plot saved convergence and globally normalized AAA comparison evidence."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"


def main():
    production = ART / "axial-material-production-qualified-AB-compensated-20261004"
    ce = ART / "axial-material-ce-qualified-AB-compensated-20261004/AAA"
    obs = ART / "axial-material-qualified-AAA-observables-20261004"
    status = json.loads((production / "AAA/run_status.json").read_text())
    stats = json.loads((ce / "statistics.json").read_text())
    current = json.loads((ce / "currents_balance_symmetry.json").read_text())
    assessment = json.loads((ce / "reference_assessment.json").read_text())
    contract = json.loads((ce / "reference_contract.json").read_text())
    rows = list(csv.DictReader((obs / "observables.regions.csv").open()))
    bins = contract["region_layer_bins"]
    lookup = {(int(row["radial_region"]), int(row["axial_cell"])): row for row in rows}
    z_edges = np.array(contract["tally_z_edges_cm"])
    z_centers = (z_edges[:-1] + z_edges[1:]) / 2
    p_flux, c_flux, p_nuf, c_nuf = [], [], [], []
    for layer in range(1, len(z_centers) + 1):
        indices = [i for i, row in enumerate(bins) if row["layer"] == layer and row["region"] in (4, 5, 6, 7)]
        volumes = np.array([bins[i]["volume_cm3"] for i in indices])
        p_rows = [lookup[(bins[i]["region"], layer)] for i in indices]
        p_flux.append(sum(float(row["flux_per_global_nufission"]) for row in p_rows) / sum(float(row["volume_cm3"]) for row in p_rows))
        c_flux.append(float(np.dot(volumes, np.array(stats["reference_flux"])[indices]) / volumes.sum()))
        p_nuf.append(sum(float(row["nufission_fraction"]) for row in p_rows))
        c_nuf.append(float(np.array(stats["reference_nufission_fraction"])[indices].sum()))
    out = ART / "axial-material-AAA-compensated-closeout-20261004"
    out.mkdir(exist_ok=True)
    for name in ("comparison.png", "comparison.svg"):
        if (out / name).exists():
            raise ValueError("comparison plot already exists: no overwrite")
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "white", "savefig.facecolor": "white"})
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.2))
    ax = axes[0, 0]
    maps = status["cases"]["AAA"]["maps"]
    for key, color in (("RRHO", "#4178a8"), ("RLEAK", "#a24981"), ("RA", "#36896c")):
        ax.semilogy([row["epoch"] for row in maps], [row["defects"][key] for row in maps], "o-", color=color, label=key)
    ax.axhline(status["outer_gate"], color="#555555", linestyle="--", label="Original gate: 5e-7")
    ax.set(xticks=[row["epoch"] for row in maps], xlabel="Completed coupled map", ylabel="Iteration defect", title="Iteration converged in four maps")
    ax.legend(fontsize=9)
    for ax, p, c, title, ylabel in ((axes[0, 1], p_flux, c_flux, "Fuel scalar flux", "Volume-averaged scalar flux / global nu-fission"),
            (axes[1, 0], p_nuf, c_nuf, "Fuel nu-fission by axial cell", "Cell nu-fission / global nu-fission")):
        ax.plot(z_centers, p, "o-", color="#246aab", label="SPOT saved REAL64")
        ax.plot(z_centers, c, "s--", color="#cc7627", label="CE sample mean")
        ax.set(xlabel="z (cm)", ylabel=ylabel, title=title)
        ax.legend(fontsize=9)
    ax = axes[1, 1]
    comparison = current["comparison"]
    ax.plot(comparison["z_cm"], comparison["production_net_plus_z"], "o-", color="#246aab", label="SPOT saved REAL64")
    ax.plot(comparison["z_cm"], comparison["ce_net_plus_z"], "s--", color="#cc7627", label="CE sample mean")
    ax.axhline(0, color="#777777", linewidth=.8)
    ax.set(xlabel="z (cm)", ylabel="Net +z current / global nu-fission", title="Signed full-section axial current")
    ax.legend(fontsize=9)
    for ax in axes.ravel():
        ax.grid(axis="y", alpha=.18)
    k = stats["k"]
    title = "AAA control: " + assessment["classification"].replace("_", " ")
    fig.suptitle(title, x=.07, ha="left", fontsize=15)
    footnote = (f"k: SPOT {k['production']:.8f}; CE {k['reference']:.8f} +/- {k['sigma_k']:.8f}. "
        f"Source screen: {stats['checks']['source_convergence_screen']}; statistics: {stats['status']}.\n"
        "One global nu-fission normalization per method; no per-layer scaling. Profile lines have no pointwise confidence bands.\n"
        "Current differences have no declared cross-method accuracy gate. Telescoping is an accounting identity, not full neutron balance.")
    fig.text(.07, .018, footnote, fontsize=8.2, va="bottom", color="#444444")
    fig.tight_layout(rect=(.02, .095, 1, .95))
    fig.savefig(out / "comparison.png", dpi=180)
    fig.savefig(out / "comparison.svg")
    plt.close(fig)
    print(str(out / "comparison.png"))


if __name__ == "__main__":
    main()
