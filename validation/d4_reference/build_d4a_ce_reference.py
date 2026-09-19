#!/usr/bin/env python3
"""Build the corrected three-floor D4-A continuous-energy reference model.

The default-safe route is ``--no-run``: it exports and independently checks
the OpenMC inputs but never starts particle transport.  A production run is
possible only with ``--run`` and an explicit statistical protocol.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

import openmc


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASE = Path(__file__).with_name("audited_rnr_assembly_base.py")
# Exact 461-line freeze of this audited source; the frozen file itself remains
# byte-for-byte identical so that the reviewed SHA-256 stays meaningful.
AUDITED_BASE_ORIGIN = (
    "/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/assembly/"
    "results_new_materials_20260527/openmc/white/rnr_assembly.py"
)
DEFAULT_CROSS_SECTIONS = Path(
    os.environ.get(
        "OPENMC_CROSS_SECTIONS",
        "/Users/wen/openmc-workspace/data/endfb-viii.1-hdf5/"
        "cross_sections.xml",
    )
)

AUDITED_BASE_SHA256 = (
    "81eba865f5c8da02650ec1ed31480ced8ee07fef9b4f19c3b102d043e3287e0d"
)
CORRECTED_SOURCE_SHA256 = {
    "data/rnr_0burn_spot_proc/rnr_cc.c2m":
        "594e9e58aae950b003bd410440928c97b59cf67f70844033c69c05b78e8565b5",
    "data/rnr_0burn_spot_proc/rnr_interpol.c2m":
        "255ddfc61a61026e0f36aefe5ad4cee0b41871fdbd25e2b77c540bd9bccb8ed2",
    "data/rnr_0burn_spot_proc/irena_assembly_tiso_1_12_1ring.dat":
        "ca46ef77ea769059ddc612f1a78e4b565c32990401b21652c822bf2e11497a3e",
}

FUEL_TEMPERATURES_C = (650.0, 750.0, 850.0)
CLAD_TEMPERATURE_C = 620.0
SODIUM_TEMPERATURE_C = 475.0
Z_EDGES_CM = (0.0, 50.0, 100.0, 150.0)
PIN_PITCH_CM = 1.07
PIN_RINGS = 8
R_HOLE_CM = 0.11
R_FUEL_CM = 0.4225
R_GAP_CM = 0.435
R_CLAD_CM = 0.485
WRAPPER_INNER_SIDE_CM = 9.2155980
WRAPPER_OUTER_SIDE_CM = 9.7352133
ASSEMBLY_OUTER_SIDE_CM = 9.9950209
N_PINS = 217
N_FLOORS = 3
N_TALLY_BINS = N_PINS * N_FLOORS
MODEL_NUCLIDES = (
    "Am241", "C12", "Cr50", "Cr52", "Cr53", "Cr54", "Fe54", "Fe56",
    "Fe57", "Fe58", "He4", "Mn55", "Mo100", "Mo92", "Mo94", "Mo95",
    "Mo96", "Mo97", "Mo98", "Na23", "Ni58", "Ni60", "Ni61", "Ni62",
    "Ni64", "O16", "Pu238", "Pu239", "Pu240", "Pu241", "Pu242", "Si28",
    "Ti48", "U235", "U238",
)
OPENMC_PYTHON_CRITICAL_FILES = (
    "__init__.py",
    "executor.py",
    "statepoint.py",
    "tallies.py",
    "model/model.py",
)


class BuildFailure(RuntimeError):
    """A fail-closed model-construction error."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_python_tree(root: Path) -> str:
    """Hash Python sources independently of the package installation path."""
    digest = hashlib.sha256()
    files = sorted(path for path in root.rglob("*.py") if path.is_file())
    if not files:
        raise BuildFailure(f"OpenMC Python package contains no sources: {root}")
    for path in files:
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_openmc_executable(identifier: str) -> Path:
    located = shutil.which(identifier)
    if located is None:
        raise BuildFailure(f"cannot resolve OpenMC executable: {identifier}")
    path = Path(located).resolve(strict=True)
    if not path.is_file() or not os.access(path, os.X_OK):
        raise BuildFailure(f"OpenMC executable is not an executable file: {path}")
    return path


def executable_version(path: Path) -> tuple[str, list[int], str | None]:
    try:
        completed = subprocess.run(
            [str(path), "--version"],
            text=True,
            capture_output=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BuildFailure(f"cannot query OpenMC executable version: {exc}") from exc
    text = completed.stdout
    if completed.returncode != 0 or not text.strip():
        detail = completed.stderr.strip() or "no version text"
        raise BuildFailure(f"OpenMC --version failed: {detail}")
    match = re.search(
        r"^OpenMC version (\d+)\.(\d+)\.(\d+)(?:-dev\d+)?$",
        text,
        re.MULTILINE,
    )
    if match is None:
        raise BuildFailure("OpenMC --version text has no recognized version")
    commit = re.search(r"^Commit hash: ([0-9a-fA-F]{7,64})$", text, re.MULTILINE)
    return (
        text,
        [int(value) for value in match.groups()],
        commit.group(1).lower() if commit is not None else None,
    )


def runtime_provenance(executable_identifier: str) -> dict:
    """Capture the executable and Python reader identities before transport."""
    executable = resolve_openmc_executable(executable_identifier)
    version_text, version, git_sha1 = executable_version(executable)
    module_file = getattr(openmc, "__file__", None)
    package_version = getattr(openmc, "__version__", None)
    if not isinstance(module_file, str) or not isinstance(package_version, str):
        raise BuildFailure("OpenMC Python package identity is unavailable")
    package_root = Path(module_file).resolve(strict=True).parent
    critical = {}
    for relative in OPENMC_PYTHON_CRITICAL_FILES:
        path = package_root / relative
        if not path.is_file():
            raise BuildFailure(f"missing critical OpenMC Python file: {path}")
        critical[relative] = sha256_file(path)
    return {
        "schema": "D4A_OPENMC_RUNTIME_PROVENANCE_V1",
        "executable": {
            "requested_identifier": executable_identifier,
            "resolved_path": str(executable),
            "sha256": sha256_file(executable),
            "version_text": version_text,
            "version_text_sha256": hashlib.sha256(
                version_text.encode("utf-8")
            ).hexdigest(),
            "openmc_version": version,
            "git_sha1": git_sha1,
        },
        "python_package": {
            "version": package_version,
            "root_identifier": str(package_root),
            "critical_files": critical,
            "stable_python_tree_sha256": sha256_python_tree(package_root),
            "stable_hash_rule": "sorted *.py: relative-posix NUL content NUL",
        },
    }


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise BuildFailure(f"missing {label}: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise BuildFailure(
            f"{label} hash changed: expected {expected}, found {actual}"
        )


def load_audited_base(path: Path):
    require_hash(path, AUDITED_BASE_SHA256, "audited CE assembly source")
    spec = importlib.util.spec_from_file_location("d4a_audited_ce_base", path)
    if spec is None or spec.loader is None:
        raise BuildFailure(f"cannot load audited CE source: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, expected in {
        "R_HOLE": R_HOLE_CM,
        "R_FUEL_4": R_FUEL_CM,
        "R_GAP": R_GAP_CM,
        "R_CLAD": R_CLAD_CM,
        "PIN_RINGS": PIN_RINGS,
        "O_M_MOX": 1.98,
        "fuel_compaction": 0.955,
        "p_Fe_EM10": 0.8908,
    }.items():
        if getattr(module, name) != expected:
            raise BuildFailure(f"audited CE source changed {name}")
    return module


def material_numbers(base, fuel_temperature_c: float) -> dict[str, float]:
    """Re-evaluate the reviewed rnr_interpol/rnr_cc formulas at one floor."""
    a_comb = base._interp(fuel_temperature_c, base._TABLE_comb)
    a_aim1 = base._interp(CLAD_TEMPERATURE_C, base._TABLE_AIM1)
    a_em10 = base._interp(SODIUM_TEMPERATURE_C, base._TABLE_EM10)
    a_na = base._interp(SODIUM_TEMPERATURE_C, base._TABLE_na)

    coeff_1 = 1.0 + a_comb * (fuel_temperature_c - 20.0)
    coeff_3 = 1.0 + a_aim1 * (CLAD_TEMPERATURE_C - 20.0)
    coeff_7 = 1.0 + a_em10 * (SODIUM_TEMPERATURE_C - 20.0)
    coeff_11 = 1.0 + a_na * (SODIUM_TEMPERATURE_C - 20.0)
    coeff_13 = 1.0 - a_comb * (fuel_temperature_c - 20.0)
    coeff_14 = 1.0 - a_aim1 * (CLAD_TEMPERATURE_C - 20.0)

    rho_mox = base.rho0_MOX / coeff_1**3
    rho_aim1 = base.rho0_AIM1 / coeff_3**3
    rho_em10 = base.rho0_EM10 / coeff_7**3
    rho_na = base.rho0_Na / coeff_11**3
    rho_he_1 = base.rho0_He / (coeff_1 * coeff_13**2)
    rho_he_2 = base.rho0_He / (coeff_1**3 * coeff_14**2)

    ox_corr = 1.0 + base.O_M_MOX * 15.9949 * (
        base.p_U / base.M_U_HM + base.p_Pu / base.M_Pu_HM
    )
    rho_hm = rho_mox / ox_corr
    n_mox = rho_hm * base.p_Pu * base.A_AVOGADRO / base.M_Pu_HM
    n_u = rho_hm * base.p_U * base.A_AVOGADRO / base.M_U_HM

    values = {
        "a_comb": a_comb,
        "a_AIM1": a_aim1,
        "a_EM10": a_em10,
        "a_na": a_na,
        "rho_MOX": rho_mox,
        "rho_AIM1": rho_aim1,
        "rho_EM10": rho_em10,
        "rho_Na": rho_na,
        "N_U5": base.p_U5 * n_u,
        "N_U8": base.p_U8 * n_u,
        "N_Pu38": base.p_Pu38 * n_mox,
        "N_Pu39": base.p_Pu39 * n_mox,
        "N_Pu40": base.p_Pu40 * n_mox,
        "N_Pu41": base.p_Pu41 * n_mox,
        "N_Pu42": base.p_Pu42 * n_mox,
        "N_Am": base.p_Am * n_mox,
        "N_O": base.O_M_MOX * (n_u + n_mox),
        "N_Na": rho_na * base.A_AVOGADRO / 22.98976928,
        "N_He_1": rho_he_1 * base.A_AVOGADRO / 4.002602,
        "N_He_2": rho_he_2 * base.A_AVOGADRO / 4.002602,
    }

    def element_density(fraction: float, rho: float, molar_mass: float) -> float:
        return fraction * rho * base.A_AVOGADRO / molar_mass

    for suffix, fraction, mass in (
        ("Fe_AIM1", base.p_Fe_AIM1, base.M_Fe),
        ("Cr_AIM1", base.p_Cr_AIM1, base.M_Cr),
        ("Ni_AIM1", base.p_Ni_AIM1, base.M_Ni),
        ("Mn_AIM1", base.p_Mn_AIM1, base.M_Mn),
        ("Mo_AIM1", base.p_Mo_AIM1, base.M_Mo),
        ("Si_AIM1", base.p_Si_AIM1, base.M_Si),
        ("Ti_AIM1", base.p_Ti_AIM1, base.M_Ti),
    ):
        values[f"N_{suffix}"] = element_density(fraction, rho_aim1, mass)
    for suffix, fraction, mass in (
        ("Fe_EM10", base.p_Fe_EM10, base.M_Fe),
        ("Cr_EM10", base.p_Cr_EM10, base.M_Cr),
        ("Ni_EM10", base.p_Ni_EM10, base.M_Ni),
        ("Mn_EM10", base.p_Mn_EM10, base.M_Mn),
        ("Mo_EM10", base.p_Mo_EM10, base.M_Mo),
        ("C_EM10", base.p_C_EM10, base.M_C),
        ("Si_EM10", base.p_Si_EM10, base.M_Si),
        ("Ti_EM10", base.p_Ti_EM10, base.M_Ti),
    ):
        values[f"N_{suffix}"] = element_density(fraction, rho_em10, mass)
    return values


def add_isotopes(material, total_density: float, isotope_fractions) -> None:
    for nuclide, fraction in isotope_fractions:
        material.add_nuclide(nuclide, total_density * fraction)


def make_floor_materials(base, floor: int, fuel_temperature_c: float):
    values = material_numbers(base, fuel_temperature_c)
    prefix = f"F{floor}"

    fuel = openmc.Material(name=f"{prefix}_FUEL_MOX")
    for nuclide, key in (
        ("U235", "N_U5"), ("U238", "N_U8"),
        ("Pu238", "N_Pu38"), ("Pu239", "N_Pu39"),
        ("Pu240", "N_Pu40"), ("Pu241", "N_Pu41"),
        ("Pu242", "N_Pu42"), ("Am241", "N_Am"), ("O16", "N_O"),
    ):
        fuel.add_nuclide(nuclide, values[key])
    fuel.set_density("sum")
    fuel.temperature = fuel_temperature_c + 273.15

    he_hole = openmc.Material(name=f"{prefix}_He_HOLE")
    he_hole.add_nuclide("He4", values["N_He_1"])
    he_hole.set_density("sum")
    he_hole.temperature = fuel_temperature_c + 273.15

    he_gap = openmc.Material(name=f"{prefix}_He_GAP")
    he_gap.add_nuclide("He4", values["N_He_2"])
    he_gap.set_density("sum")
    he_gap.temperature = CLAD_TEMPERATURE_C + 273.15

    clad = openmc.Material(name=f"{prefix}_CLAD_AIM1")
    add_isotopes(clad, values["N_Fe_AIM1"], (
        ("Fe54", base.p_Fe54), ("Fe56", base.p_Fe56),
        ("Fe57", base.p_Fe57), ("Fe58", base.p_Fe58),
    ))
    add_isotopes(clad, values["N_Cr_AIM1"], (
        ("Cr50", base.p_Cr50), ("Cr52", base.p_Cr52),
        ("Cr53", base.p_Cr53), ("Cr54", base.p_Cr54),
    ))
    add_isotopes(clad, values["N_Ni_AIM1"], (
        ("Ni58", base.p_Ni58), ("Ni60", base.p_Ni60),
        ("Ni61", base.p_Ni61), ("Ni62", base.p_Ni62),
        ("Ni64", base.p_Ni64),
    ))
    add_isotopes(clad, values["N_Mo_AIM1"], (
        ("Mo92", base.p_Mo92), ("Mo94", base.p_Mo94),
        ("Mo95", base.p_Mo95), ("Mo96", base.p_Mo96),
        ("Mo97", base.p_Mo97), ("Mo98", base.p_Mo98),
        ("Mo100", base.p_Mo100),
    ))
    clad.add_nuclide("Mn55", values["N_Mn_AIM1"])
    clad.add_nuclide("Si28", values["N_Si_AIM1"])
    clad.add_nuclide("Ti48", values["N_Ti_AIM1"])
    clad.set_density("sum")
    clad.temperature = CLAD_TEMPERATURE_C + 273.15

    em10 = openmc.Material(name=f"{prefix}_BOX_EM10")
    add_isotopes(em10, values["N_Fe_EM10"], (
        ("Fe54", base.p_Fe54), ("Fe56", base.p_Fe56),
        ("Fe57", base.p_Fe57), ("Fe58", base.p_Fe58),
    ))
    add_isotopes(em10, values["N_Cr_EM10"], (
        ("Cr50", base.p_Cr50), ("Cr52", base.p_Cr52),
        ("Cr53", base.p_Cr53), ("Cr54", base.p_Cr54),
    ))
    add_isotopes(em10, values["N_Ni_EM10"], (
        ("Ni58", base.p_Ni58), ("Ni60", base.p_Ni60),
        ("Ni61", base.p_Ni61), ("Ni62", base.p_Ni62),
        ("Ni64", base.p_Ni64),
    ))
    add_isotopes(em10, values["N_Mo_EM10"], (
        ("Mo92", base.p_Mo92), ("Mo94", base.p_Mo94),
        ("Mo95", base.p_Mo95), ("Mo96", base.p_Mo96),
        ("Mo97", base.p_Mo97), ("Mo98", base.p_Mo98),
        ("Mo100", base.p_Mo100),
    ))
    em10.add_nuclide("Mn55", values["N_Mn_EM10"])
    em10.add_nuclide("C12", values["N_C_EM10"])
    em10.add_nuclide("Si28", values["N_Si_EM10"])
    em10.add_nuclide("Ti48", values["N_Ti_EM10"])
    em10.set_density("sum")
    em10.temperature = SODIUM_TEMPERATURE_C + 273.15

    coolant = openmc.Material(name=f"{prefix}_COOLANT_Na")
    coolant.add_nuclide("Na23", values["N_Na"])
    coolant.set_density("sum")
    coolant.temperature = SODIUM_TEMPERATURE_C + 273.15

    materials = [fuel, he_hole, he_gap, clad, em10, coolant]
    mapping = {
        "fuel": fuel,
        "he_hole": he_hole,
        "he_gap": he_gap,
        "clad": clad,
        "em10": em10,
        "coolant": coolant,
    }
    anchors = {
        key: values[key]
        for key in (
            "N_Na", "N_U8", "N_Pu39", "N_O", "N_He_1", "N_He_2"
        )
    }
    anchors["N_Fe56_AIM1"] = values["N_Fe_AIM1"] * base.p_Fe56
    return materials, mapping, anchors


def lattice_index_map(num_rings: int):
    mapping = {}
    max_g = num_rings - 1
    for alpha in range(-max_g, max_g + 1):
        for x_index in range(-max_g, max_g + 1):
            z_index = -alpha - x_index
            ring = max(abs(x_index), abs(alpha), abs(z_index))
            if ring >= num_rings:
                continue
            openmc_ring = num_rings - 1 - ring
            if x_index >= 0:
                if alpha >= 0:
                    within = x_index
                else:
                    within = 2 * ring + z_index
            elif alpha <= 0:
                within = 3 * ring - x_index
            else:
                within = 5 * ring - z_index
            mapping[(openmc_ring, within)] = (x_index, alpha, ring)
    return mapping


def make_pin_universe(materials, floor: int, pin: int):
    hole = openmc.ZCylinder(r=R_HOLE_CM)
    fuel = openmc.ZCylinder(r=R_FUEL_CM)
    gap = openmc.ZCylinder(r=R_GAP_CM)
    clad = openmc.ZCylinder(r=R_CLAD_CM)
    prefix = f"floor_{floor}_pin_{pin:03d}"
    hole_cell = openmc.Cell(
        fill=materials["he_hole"], region=-hole, name=f"{prefix}_hole"
    )
    fuel_cell = openmc.Cell(
        fill=materials["fuel"], region=+hole & -fuel, name=f"{prefix}_fuel"
    )
    gap_cell = openmc.Cell(
        fill=materials["he_gap"], region=+fuel & -gap, name=f"{prefix}_gap"
    )
    clad_cell = openmc.Cell(
        fill=materials["clad"], region=+gap & -clad, name=f"{prefix}_clad"
    )
    coolant_cell = openmc.Cell(
        fill=materials["coolant"], region=+clad, name=f"{prefix}_coolant"
    )
    universe = openmc.Universe(
        cells=[hole_cell, fuel_cell, gap_cell, clad_cell, coolant_cell]
    )
    return universe, fuel_cell


def build_floor_lattice(materials, floor: int, fuel_temperature_c: float):
    num_rings = PIN_RINGS + 1
    indices = lattice_index_map(num_rings)
    lattice = openmc.HexLattice(name=f"floor_{floor}_217_pin_lattice")
    lattice.center = (0.0, 0.0)
    lattice.pitch = (PIN_PITCH_CM,)
    lattice.orientation = "y"

    records = []
    fuel_cells = []
    rings = []
    pin = 0
    for openmc_ring in range(num_rings):
        ring_from_center = num_rings - 1 - openmc_ring
        count = max(6 * ring_from_center, 1)
        universes = []
        for within in range(count):
            x_index, alpha_index, ring = indices[(openmc_ring, within)]
            x_cm = math.sqrt(0.75) * PIN_PITCH_CM * x_index
            y_cm = (0.5 * x_index + alpha_index) * PIN_PITCH_CM
            universe, fuel_cell = make_pin_universe(materials, floor, pin)
            universes.append(universe)
            fuel_cells.append(fuel_cell)
            records.append({
                "floor": floor,
                "fuel_temperature_c": f"{fuel_temperature_c:.1f}",
                "pin_index": pin,
                "openmc_ring_index": openmc_ring,
                "openmc_i_within": within,
                "ring_from_center": ring,
                "x_index": x_index,
                "alpha_index": alpha_index,
                "x_cm": f"{x_cm:.10f}",
                "y_cm": f"{y_cm:.10f}",
                "fuel_cell_id": fuel_cell.id,
            })
            pin += 1
        rings.append(universes)
    if pin != N_PINS:
        raise BuildFailure(f"floor {floor} built {pin} pins, expected {N_PINS}")
    lattice.universes = rings
    lattice.outer = openmc.Universe(cells=[
        openmc.Cell(fill=materials["coolant"], name=f"floor_{floor}_outer_na")
    ])
    return lattice, fuel_cells, records


def build_model(
    base,
    cross_sections: Path,
    execution: dict,
    runtime: dict | None = None,
):
    all_materials = []
    floor_materials = []
    material_anchors = []
    for floor, fuel_temperature in enumerate(FUEL_TEMPERATURES_C, start=1):
        materials, mapping, anchors = make_floor_materials(
            base, floor, fuel_temperature
        )
        all_materials.extend(materials)
        floor_materials.append(mapping)
        material_anchors.append({
            "floor": floor,
            "fuel_temperature_c": fuel_temperature,
            "fuel_temperature_k": fuel_temperature + 273.15,
            "clad_temperature_c": CLAD_TEMPERATURE_C,
            "sodium_temperature_c": SODIUM_TEMPERATURE_C,
            **anchors,
        })

    lattices = []
    fuel_cells = []
    pin_records = []
    for floor, (fuel_temperature, mapping) in enumerate(
        zip(FUEL_TEMPERATURES_C, floor_materials), start=1
    ):
        lattice, cells, records = build_floor_lattice(
            mapping, floor, fuel_temperature
        )
        lattices.append(lattice)
        fuel_cells.extend(cells)
        pin_records.extend(records)
    if len(fuel_cells) != N_TALLY_BINS:
        raise BuildFailure("the model does not contain exactly 651 fuel cells")

    wrap_inner = openmc.model.HexagonalPrism(
        edge_length=WRAPPER_INNER_SIDE_CM, orientation="y"
    )
    wrap_outer = openmc.model.HexagonalPrism(
        edge_length=WRAPPER_OUTER_SIDE_CM, orientation="y"
    )
    assembly_outer = openmc.model.HexagonalPrism(
        edge_length=ASSEMBLY_OUTER_SIDE_CM,
        orientation="y",
        boundary_type="white",
    )
    z_planes = []
    for index, value in enumerate(Z_EDGES_CM):
        if index in (0, N_FLOORS):
            z_planes.append(openmc.ZPlane(z0=value, boundary_type="vacuum"))
        else:
            z_planes.append(openmc.ZPlane(z0=value))

    root_cells = []
    for index in range(N_FLOORS):
        floor = index + 1
        axial = +z_planes[index] & -z_planes[index + 1]
        mapping = floor_materials[index]
        root_cells.extend([
            openmc.Cell(
                fill=lattices[index],
                region=-wrap_inner & axial,
                name=f"floor_{floor}_lattice_region",
            ),
            openmc.Cell(
                fill=mapping["em10"],
                region=+wrap_inner & -wrap_outer & axial,
                name=f"floor_{floor}_wrapper_EM10",
            ),
            openmc.Cell(
                fill=mapping["coolant"],
                region=+wrap_outer & -assembly_outer & axial,
                name=f"floor_{floor}_outer_Na",
            ),
        ])

    materials_xml = openmc.Materials(all_materials)
    materials_xml.cross_sections = str(cross_sections.resolve())
    geometry = openmc.Geometry(root_cells)

    settings = openmc.Settings()
    settings.run_mode = "eigenvalue"
    settings.energy_mode = "continuous-energy"
    settings.temperature = {"method": "interpolation"}
    settings.particles = execution["particles"]
    settings.batches = execution["batches"]
    settings.inactive = execution["inactive"]
    settings.seed = execution["seed"]
    settings.source = openmc.IndependentSource(
        space=openmc.stats.Box(
            (-ASSEMBLY_OUTER_SIDE_CM, -ASSEMBLY_OUTER_SIDE_CM, Z_EDGES_CM[0]),
            (+ASSEMBLY_OUTER_SIDE_CM, +ASSEMBLY_OUTER_SIDE_CM, Z_EDGES_CM[-1]),
        ),
        constraints={"fissionable": True},
    )

    tally = openmc.Tally(name="d4a_floor_pin_nu_fission")
    tally.filters = [openmc.CellFilter(fuel_cells)]
    tally.estimator = "tracklength"
    tally.nuclides = ["total"]
    tally.scores = ["nu-fission"]
    tallies = openmc.Tallies([tally])

    contract = {
        "schema": "D4A_CORRECTED_CE_REFERENCE_V1",
        "result_role": (
            "STATIC_INPUT_ONLY" if execution["mode"] == "NO_RUN"
            else "PRODUCTION_INPUT"
        ),
        "physics": {
            "fuel_temperatures_c": list(FUEL_TEMPERATURES_C),
            "clad_temperature_c": CLAD_TEMPERATURE_C,
            "sodium_temperature_c": SODIUM_TEMPERATURE_C,
            "temperature_method": "interpolation",
            "temperature_tolerance": None,
            "fitted_parameters": [],
        },
        "geometry": {
            "pins_per_floor": N_PINS,
            "floors": N_FLOORS,
            "pin_pitch_cm": PIN_PITCH_CM,
            "pin_radii_cm": [R_HOLE_CM, R_FUEL_CM, R_GAP_CM, R_CLAD_CM],
            "wrapper_and_outer_side_cm": [
                WRAPPER_INNER_SIDE_CM,
                WRAPPER_OUTER_SIDE_CM,
                ASSEMBLY_OUTER_SIDE_CM,
            ],
            "z_edges_cm": list(Z_EDGES_CM),
            "radial_boundary": "white",
            "axial_end_boundaries": "vacuum",
        },
        "observables": {
            "eigenvalue": "statepoint.keff",
            "tally_name": tally.name,
            "score": "nu-fission",
            "estimator": "tracklength",
            "nuclides": ["total"],
            "cell_filter_bins": N_TALLY_BINS,
            "normalization": "one global sum over all 651 bins",
        },
        "material_anchors": material_anchors,
        "execution": execution,
        "runtime_provenance": runtime,
        "cross_sections_xml": str(cross_sections.resolve()),
    }
    return openmc.Model(geometry, materials_xml, settings, tallies), pin_records, contract


def write_csv(path: Path, records) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def write_manifest(output: Path, base_source: Path, cross_sections: Path) -> None:
    checker = Path(__file__).with_name("check_d4a_ce_static.py")
    sources = {
        "driver": (
            "validation/d4_reference/build_d4a_ce_reference.py",
            Path(__file__).resolve(),
        ),
        "checker": (
            "validation/d4_reference/check_d4a_ce_static.py",
            checker.resolve(),
        ),
        "audited_ce_base": (
            "validation/d4_reference/audited_rnr_assembly_base.py",
            base_source.resolve(),
        ),
    }
    for relative in CORRECTED_SOURCE_SHA256:
        sources[f"spot:{relative}"] = (relative, (ROOT / relative).resolve())
    generated = {
        name: output / name
        for name in (
            "materials.xml",
            "geometry.xml",
            "settings.xml",
            "tallies.xml",
            "pin_map.csv",
            "model_contract.json",
        )
    }
    library_paths = {}
    for entry in ET.parse(cross_sections).getroot().findall("library"):
        if entry.get("type") != "neutron":
            continue
        material = entry.get("materials")
        if material in MODEL_NUCLIDES:
            if material in library_paths:
                raise BuildFailure(f"duplicate neutron library for {material}")
            logical_path = entry.get("path")
            if not logical_path:
                raise BuildFailure(f"neutron library path is missing for {material}")
            library_paths[material] = (
                logical_path,
                (cross_sections.parent / logical_path).resolve(),
            )
    if set(library_paths) != set(MODEL_NUCLIDES):
        missing = sorted(set(MODEL_NUCLIDES) - set(library_paths))
        raise BuildFailure(f"cross_sections.xml lacks neutron libraries: {missing}")
    for nuclide, (_logical_path, path) in library_paths.items():
        if not path.is_file():
            raise BuildFailure(f"missing neutron library for {nuclide}: {path}")
    manifest = {
        "schema": "D4A_CORRECTED_CE_INPUT_MANIFEST_V1",
        "audited_base_provenance": {
            "upstream_origin": AUDITED_BASE_ORIGIN,
            "frozen_path": "validation/d4_reference/audited_rnr_assembly_base.py",
            "line_count": 461,
            "sha256": AUDITED_BASE_SHA256,
        },
        "sources": {
            key: {"path": logical, "sha256": sha256_file(path)}
            for key, (logical, path) in sources.items()
        },
        "cross_sections_xml": {
            "path": str(cross_sections.resolve()),
            "sha256": sha256_file(cross_sections),
        },
        "nuclear_data": {
            nuclide: {"path": logical, "sha256": sha256_file(path)}
            for nuclide, (logical, path) in sorted(library_paths.items())
        },
        "generated": {
            key: {"path": key, "sha256": sha256_file(path)}
            for key, path in generated.items()
        },
    }
    manifest_path = output / "source_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    (output / "source_manifest.sha256").write_text(
        f"{sha256_file(manifest_path)}  source_manifest.json\n"
    )


def run_static_checker(output: Path, cross_sections: Path) -> None:
    checker = Path(__file__).with_name("check_d4a_ce_static.py")
    try:
        subprocess.run(
            [
                sys.executable,
                str(checker),
                str(output),
                "--cross-sections",
                str(cross_sections.resolve()),
            ],
            check=True,
            timeout=30,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise BuildFailure(f"static CE checker failed: {exc}") from exc


def extract_result(output: Path, batches: int) -> None:
    import numpy as np

    statepoint = output / f"statepoint.{batches}.h5"
    if not statepoint.is_file():
        raise BuildFailure(f"missing final statepoint: {statepoint}")
    with openmc.StatePoint(statepoint) as sp:
        keff = float(sp.keff.nominal_value)
        keff_std = float(sp.keff.std_dev)
        tally = sp.get_tally(name="d4a_floor_pin_nu_fission")
        means = tally.get_values(scores=["nu-fission"], value="mean").reshape(-1)
        standard_deviations = tally.get_values(
            scores=["nu-fission"], value="std_dev"
        ).reshape(-1)
        cell_bins = [int(value) for value in np.ravel(tally.filters[0].bins)]
    if len(means) != N_TALLY_BINS or len(cell_bins) != N_TALLY_BINS:
        raise BuildFailure("final nu-fission tally does not contain 651 bins")
    rows = list(csv.DictReader((output / "pin_map.csv").open()))
    by_cell = {int(row["fuel_cell_id"]): row for row in rows}
    numeric_means = [float(value) for value in means]
    numeric_std = [float(value) for value in standard_deviations]
    total = math.fsum(numeric_means)
    if (not math.isfinite(keff) or not math.isfinite(keff_std) or
            not all(math.isfinite(value) and value >= 0.0
                    for value in numeric_means) or
            not all(math.isfinite(value) and value >= 0.0
                    for value in numeric_std) or
            total <= 0.0):
        raise BuildFailure("non-finite or non-positive CE result")
    if len(by_cell) != N_TALLY_BINS or set(cell_bins) != set(by_cell):
        raise BuildFailure("pin map and final CellFilter bins differ")
    floor_rates = [
        math.fsum(
            mean for cell_id, mean in zip(cell_bins, numeric_means)
            if int(by_cell[cell_id]["floor"]) == floor
        )
        for floor in range(1, N_FLOORS + 1)
    ]
    result_bins = []
    for cell_id, mean, std in zip(cell_bins, numeric_means, numeric_std):
        row = by_cell[cell_id]
        floor = int(row["floor"])
        result_bins.append({
            "floor": floor,
            "pin_index": int(row["pin_index"]),
            "ring_from_center": int(row["ring_from_center"]),
            "fuel_cell_id": cell_id,
            "nu_fission": mean,
            "nu_fission_std_dev": std,
            "global_fraction": mean / total,
        })
    result = {
        "schema": "D4A_CORRECTED_CE_RESULT_V1",
        "keff": keff,
        "keff_standard_deviation": keff_std,
        "global_nu_fission": total,
        "floor_nu_fission_fractions": [value / total for value in floor_rates],
        "bins": result_bins,
    }
    result_path = output / "reference_result.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    (output / "result_receipt.sha256").write_text(
        f"{sha256_file(statepoint)}  {statepoint.name}\n"
        f"{sha256_file(result_path)}  {result_path.name}\n"
    )


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--cross-sections", type=Path, default=DEFAULT_CROSS_SECTIONS
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--no-run", action="store_true")
    mode.add_argument("--run", action="store_true")
    parser.add_argument("--particles", type=int)
    parser.add_argument("--batches", type=int)
    parser.add_argument("--inactive", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument(
        "--openmc-exec",
        default="/Users/wen/miniforge3/envs/openmc-dev/bin/openmc",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = args.output.resolve()
    if output.exists():
        raise BuildFailure(f"output path must be fresh: {output}")
    if not args.cross_sections.is_file():
        raise BuildFailure(f"missing cross_sections.xml: {args.cross_sections}")
    require_hash(DEFAULT_BASE, AUDITED_BASE_SHA256, "repo-local audited CE source")
    for relative, expected in CORRECTED_SOURCE_SHA256.items():
        require_hash(ROOT / relative, expected, f"corrected SPOT input {relative}")
    checker = Path(__file__).with_name("check_d4a_ce_static.py")
    if not checker.is_file():
        raise BuildFailure(f"missing independent static checker: {checker}")

    if args.no_run:
        if any(value is not None for value in (
            args.particles, args.batches, args.inactive, args.seed
        )):
            raise BuildFailure("--no-run accepts no statistical protocol")
        execution = {
            "mode": "NO_RUN",
            "particles": 1,
            "batches": 2,
            "inactive": 1,
            "seed": 1,
            "note": "placeholder settings; not an accuracy calculation",
        }
    else:
        values = (args.particles, args.batches, args.inactive, args.seed)
        if any(value is None for value in values):
            raise BuildFailure(
                "--run requires explicit --particles, --batches, --inactive, and --seed"
            )
        if args.particles <= 0 or args.batches <= 1 or args.inactive <= 0:
            raise BuildFailure("invalid explicit statistical protocol")
        if args.inactive >= args.batches or args.seed <= 0 or args.threads <= 0:
            raise BuildFailure("invalid explicit run controls")
        execution = {
            "mode": "RUN",
            "particles": args.particles,
            "batches": args.batches,
            "inactive": args.inactive,
            "seed": args.seed,
            "threads": args.threads,
        }

    runtime = None
    if args.run:
        runtime = runtime_provenance(args.openmc_exec)

    output.mkdir(parents=True)
    base = load_audited_base(DEFAULT_BASE.resolve())
    model, pin_records, contract = build_model(
        base, args.cross_sections.resolve(), execution, runtime
    )
    model.export_to_xml(directory=output)
    write_csv(output / "pin_map.csv", pin_records)
    (output / "model_contract.json").write_text(
        json.dumps(contract, indent=2, sort_keys=True) + "\n"
    )
    write_manifest(output, DEFAULT_BASE.resolve(), args.cross_sections.resolve())
    run_static_checker(output, args.cross_sections)

    if args.no_run:
        print(
            "D4A CE NO-RUN PASS: 217 pins x 3 floors; 651 nu-fission bins; "
            "white radial; vacuum axial"
        )
        return

    openmc.run(
        cwd=str(output),
        openmc_exec=runtime["executable"]["resolved_path"],
        threads=args.threads,
    )
    extract_result(output, args.batches)
    print(f"D4A CE RESULT WRITTEN: {output / 'reference_result.json'}")


if __name__ == "__main__":
    try:
        main()
    except (BuildFailure, OSError, ValueError) as exc:
        print(f"D4A CE BUILD FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
