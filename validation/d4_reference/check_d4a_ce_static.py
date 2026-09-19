#!/usr/bin/env python3
"""Fail-closed static audit for the corrected D4-A OpenMC input deck."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import signal
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]
LOCAL_AUDITED_BASE = Path(__file__).with_name("audited_rnr_assembly_base.py")
AUDITED_BASE_ORIGIN = (
    "/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin/assembly/"
    "results_new_materials_20260527/openmc/white/rnr_assembly.py"
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
PIN_RADII_CM = (0.11, 0.4225, 0.435, 0.485)
HEX_SIDES_CM = (9.2155980, 9.7352133, 9.9950209)
N_PINS = 217
N_FLOORS = 3
N_BINS = 651
OPENMC_PYTHON_CRITICAL_FILES = {
    "__init__.py",
    "executor.py",
    "statepoint.py",
    "tallies.py",
    "model/model.py",
}
MODEL_NUCLIDES = {
    "Am241", "C12", "Cr50", "Cr52", "Cr53", "Cr54", "Fe54", "Fe56",
    "Fe57", "Fe58", "He4", "Mn55", "Mo100", "Mo92", "Mo94", "Mo95",
    "Mo96", "Mo97", "Mo98", "Na23", "Ni58", "Ni60", "Ni61", "Ni62",
    "Ni64", "O16", "Pu238", "Pu239", "Pu240", "Pu241", "Pu242", "Si28",
    "Ti48", "U235", "U238",
}
REQUIRED_OUTPUTS = {
    "materials.xml", "geometry.xml", "settings.xml", "tallies.xml",
    "pin_map.csv", "model_contract.json", "source_manifest.json",
    "source_manifest.sha256",
}


class AuditFailure(RuntimeError):
    pass


def fail(message: str) -> None:
    raise AuditFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_float(actual, expected, label: str) -> None:
    try:
        actual_float = float(actual)
        expected_float = float(expected)
    except (TypeError, ValueError) as exc:
        fail(f"{label} is not a float: {exc}")
    if actual_float.hex() != expected_float.hex():
        fail(
            f"{label} differs: {actual_float.hex()} != {expected_float.hex()}"
        )


def exact_sequence(actual, expected, label: str) -> None:
    if len(actual) != len(expected):
        fail(f"{label} length differs: {len(actual)} != {len(expected)}")
    for index, (left, right) in enumerate(zip(actual, expected)):
        exact_float(left, right, f"{label}[{index}]")


def check_runtime_provenance(runtime) -> None:
    if not isinstance(runtime, dict) or set(runtime) != {
        "schema", "executable", "python_package"
    }:
        fail("OpenMC runtime provenance field set differs")
    if runtime.get("schema") != "D4A_OPENMC_RUNTIME_PROVENANCE_V1":
        fail("OpenMC runtime provenance schema differs")
    executable = runtime.get("executable")
    executable_fields = {
        "requested_identifier", "resolved_path", "sha256", "version_text",
        "version_text_sha256", "openmc_version", "git_sha1",
    }
    if not isinstance(executable, dict) or set(executable) != executable_fields:
        fail("OpenMC executable provenance field set differs")
    if (not isinstance(executable["requested_identifier"], str) or
            not executable["requested_identifier"] or
            not isinstance(executable["resolved_path"], str) or
            not Path(executable["resolved_path"]).is_absolute() or
            re.fullmatch(r"[0-9a-f]{64}", executable["sha256"]) is None or
            not isinstance(executable["version_text"], str) or
            not executable["version_text"] or
            hashlib.sha256(executable["version_text"].encode("utf-8")).hexdigest()
            != executable["version_text_sha256"]):
        fail("OpenMC executable provenance is malformed")
    version = executable["openmc_version"]
    if (not isinstance(version, list) or len(version) != 3 or
            any(type(value) is not int or value < 0 for value in version)):
        fail("OpenMC executable version provenance is malformed")
    git_sha1 = executable["git_sha1"]
    if (git_sha1 is not None and
            (not isinstance(git_sha1, str) or
             re.fullmatch(r"[0-9a-f]{7,64}", git_sha1) is None)):
        fail("OpenMC executable git provenance is malformed")

    package = runtime.get("python_package")
    package_fields = {
        "version", "root_identifier", "critical_files",
        "stable_python_tree_sha256", "stable_hash_rule",
    }
    if not isinstance(package, dict) or set(package) != package_fields:
        fail("OpenMC Python package provenance field set differs")
    critical = package.get("critical_files")
    if (not isinstance(package["version"], str) or not package["version"] or
            not isinstance(package["root_identifier"], str) or
            not Path(package["root_identifier"]).is_absolute() or
            not isinstance(critical, dict) or
            set(critical) != OPENMC_PYTHON_CRITICAL_FILES or
            any(re.fullmatch(r"[0-9a-f]{64}", value) is None
                for value in critical.values()) or
            re.fullmatch(r"[0-9a-f]{64}", package["stable_python_tree_sha256"])
            is None or
            package["stable_hash_rule"] !=
            "sorted *.py: relative-posix NUL content NUL"):
        fail("OpenMC Python package provenance is malformed")


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read {path.name}: {exc}")


def load_base(path: Path):
    if path.resolve() != LOCAL_AUDITED_BASE.resolve():
        fail("audited CE base is not the repo-local frozen source")
    if sha256_file(path) != AUDITED_BASE_SHA256:
        fail("audited CE base source hash differs")
    spec = importlib.util.spec_from_file_location("d4a_ce_checker_base", path)
    if spec is None or spec.loader is None:
        fail("cannot load audited CE base source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_manifest(output: Path, relocated_cross_sections: Path | None):
    manifest_path = output / "source_manifest.json"
    expected_seal = f"{sha256_file(manifest_path)}  source_manifest.json\n"
    if (output / "source_manifest.sha256").read_text() != expected_seal:
        fail("source manifest seal differs")
    manifest = load_json(manifest_path)
    if manifest.get("schema") != "D4A_CORRECTED_CE_INPUT_MANIFEST_V1":
        fail("manifest schema differs")
    if manifest.get("audited_base_provenance") != {
        "upstream_origin": AUDITED_BASE_ORIGIN,
        "frozen_path": "validation/d4_reference/audited_rnr_assembly_base.py",
        "line_count": 461,
        "sha256": AUDITED_BASE_SHA256,
    }:
        fail("audited base provenance differs")

    local_sources = {
        "driver": (
            "validation/d4_reference/build_d4a_ce_reference.py",
            Path(__file__).with_name("build_d4a_ce_reference.py").resolve(),
        ),
        "checker": (
            "validation/d4_reference/check_d4a_ce_static.py",
            Path(__file__).resolve(),
        ),
        "audited_ce_base": (
            "validation/d4_reference/audited_rnr_assembly_base.py",
            LOCAL_AUDITED_BASE.resolve(),
        ),
    }
    for relative in CORRECTED_SOURCE_SHA256:
        local_sources[f"spot:{relative}"] = (relative, (ROOT / relative).resolve())
    sources = manifest.get("sources", {})
    if set(sources) != set(local_sources):
        fail("manifest source set differs")
    for key, (logical_path, local_path) in local_sources.items():
        record = sources.get(key)
        if (not isinstance(record, dict) or set(record) != {"path", "sha256"} or
                record.get("path") != logical_path):
            fail(f"source record differs: {key}")
        if not local_path.is_file() or sha256_file(local_path) != record.get("sha256"):
            fail(f"source hash differs: {key}")
    if sources["audited_ce_base"]["sha256"] != AUDITED_BASE_SHA256:
        fail("manifest audited CE base hash differs")
    for relative, expected in CORRECTED_SOURCE_SHA256.items():
        key = f"spot:{relative}"
        if sources[key]["sha256"] != expected:
            fail(f"manifest corrected source hash differs: {relative}")

    generated = manifest.get("generated", {})
    expected_generated = {
        name for name in REQUIRED_OUTPUTS
        if name not in {"source_manifest.json", "source_manifest.sha256"}
    }
    if set(generated) != expected_generated:
        fail("manifest generated-file set differs")
    for name, record in generated.items():
        if record.get("path") != name:
            fail(f"manifest generated path differs: {name}")
        if sha256_file(output / name) != record.get("sha256"):
            fail(f"generated input hash differs: {name}")

    xs_record = manifest.get("cross_sections_xml", {})
    if not isinstance(xs_record, dict) or set(xs_record) != {"path", "sha256"}:
        fail("cross_sections.xml record differs")
    declared_xs_path = xs_record.get("path")
    if not isinstance(declared_xs_path, str) or not declared_xs_path:
        fail("cross_sections.xml declared path differs")
    if relocated_cross_sections is None:
        xs_path = Path(declared_xs_path)
    else:
        xs_path = relocated_cross_sections.resolve()
    if not xs_path.is_file() or sha256_file(xs_path) != xs_record.get("sha256"):
        fail("cross_sections.xml content hash differs")
    libraries = manifest.get("nuclear_data", {})
    if set(libraries) != MODEL_NUCLIDES:
        fail("sealed neutron-library set differs")
    xs_libraries = {}
    xs_library_records = {}
    for entry in ET.parse(xs_path).getroot().findall("library"):
        if entry.get("type") == "neutron" and entry.get("materials") in MODEL_NUCLIDES:
            nuclide = entry.get("materials")
            if nuclide in xs_libraries:
                fail(f"duplicate cross-section library: {nuclide}")
            logical_path = entry.get("path")
            if not logical_path:
                fail(f"cross-section library path is missing: {nuclide}")
            xs_library_records[nuclide] = logical_path
            xs_libraries[nuclide] = (xs_path.parent / logical_path).resolve()
    if set(xs_libraries) != MODEL_NUCLIDES:
        fail("cross_sections.xml does not resolve all model nuclides")
    for nuclide, record in libraries.items():
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            fail(f"neutron-library record differs: {nuclide}")
        if record.get("path") != xs_library_records[nuclide]:
            fail(f"neutron-library logical path differs: {nuclide}")
        path = xs_libraries[nuclide]
        if not path.is_file() or sha256_file(path) != record.get("sha256"):
            fail(f"neutron-library hash differs: {nuclide}")
    return (
        manifest,
        xs_path,
        LOCAL_AUDITED_BASE.resolve(),
        declared_xs_path,
        xs_libraries,
    )


def independent_expected_materials(base, fuel_temperature_c: float):
    """Independent transcription of the frozen rnr material equations."""
    alpha_fuel = base._interp(fuel_temperature_c, base._TABLE_comb)
    alpha_clad = base._interp(CLAD_TEMPERATURE_C, base._TABLE_AIM1)
    alpha_em10 = base._interp(SODIUM_TEMPERATURE_C, base._TABLE_EM10)
    alpha_na = base._interp(SODIUM_TEMPERATURE_C, base._TABLE_na)
    f_fuel = 1.0 + alpha_fuel * (fuel_temperature_c - 20.0)
    f_clad = 1.0 + alpha_clad * (CLAD_TEMPERATURE_C - 20.0)
    f_em10 = 1.0 + alpha_em10 * (SODIUM_TEMPERATURE_C - 20.0)
    f_na = 1.0 + alpha_na * (SODIUM_TEMPERATURE_C - 20.0)
    inv_fuel = 1.0 - alpha_fuel * (fuel_temperature_c - 20.0)
    inv_clad = 1.0 - alpha_clad * (CLAD_TEMPERATURE_C - 20.0)

    rho_mox = base.rho0_MOX / f_fuel**3
    rho_clad = base.rho0_AIM1 / f_clad**3
    rho_em10 = base.rho0_EM10 / f_em10**3
    rho_na = base.rho0_Na / f_na**3
    correction = 1.0 + base.O_M_MOX * 15.9949 * (
        base.p_U / base.M_U_HM + base.p_Pu / base.M_Pu_HM
    )
    rho_hm = rho_mox / correction
    n_pu = rho_hm * base.p_Pu * base.A_AVOGADRO / base.M_Pu_HM
    n_u = rho_hm * base.p_U * base.A_AVOGADRO / base.M_U_HM

    fuel = {
        "U235": base.p_U5 * n_u,
        "U238": base.p_U8 * n_u,
        "Pu238": base.p_Pu38 * n_pu,
        "Pu239": base.p_Pu39 * n_pu,
        "Pu240": base.p_Pu40 * n_pu,
        "Pu241": base.p_Pu41 * n_pu,
        "Pu242": base.p_Pu42 * n_pu,
        "Am241": base.p_Am * n_pu,
        "O16": base.O_M_MOX * (n_u + n_pu),
    }

    def element(fraction, density, mass):
        return fraction * density * base.A_AVOGADRO / mass

    def isotope_split(total, pairs):
        return {name: total * fraction for name, fraction in pairs}

    clad = {}
    for total, pairs in (
        (element(base.p_Fe_AIM1, rho_clad, base.M_Fe), (
            ("Fe54", base.p_Fe54), ("Fe56", base.p_Fe56),
            ("Fe57", base.p_Fe57), ("Fe58", base.p_Fe58))),
        (element(base.p_Cr_AIM1, rho_clad, base.M_Cr), (
            ("Cr50", base.p_Cr50), ("Cr52", base.p_Cr52),
            ("Cr53", base.p_Cr53), ("Cr54", base.p_Cr54))),
        (element(base.p_Ni_AIM1, rho_clad, base.M_Ni), (
            ("Ni58", base.p_Ni58), ("Ni60", base.p_Ni60),
            ("Ni61", base.p_Ni61), ("Ni62", base.p_Ni62),
            ("Ni64", base.p_Ni64))),
        (element(base.p_Mo_AIM1, rho_clad, base.M_Mo), (
            ("Mo92", base.p_Mo92), ("Mo94", base.p_Mo94),
            ("Mo95", base.p_Mo95), ("Mo96", base.p_Mo96),
            ("Mo97", base.p_Mo97), ("Mo98", base.p_Mo98),
            ("Mo100", base.p_Mo100))),
    ):
        clad.update(isotope_split(total, pairs))
    clad.update({
        "Mn55": element(base.p_Mn_AIM1, rho_clad, base.M_Mn),
        "Si28": element(base.p_Si_AIM1, rho_clad, base.M_Si),
        "Ti48": element(base.p_Ti_AIM1, rho_clad, base.M_Ti),
    })

    em10 = {}
    for total, pairs in (
        (element(base.p_Fe_EM10, rho_em10, base.M_Fe), (
            ("Fe54", base.p_Fe54), ("Fe56", base.p_Fe56),
            ("Fe57", base.p_Fe57), ("Fe58", base.p_Fe58))),
        (element(base.p_Cr_EM10, rho_em10, base.M_Cr), (
            ("Cr50", base.p_Cr50), ("Cr52", base.p_Cr52),
            ("Cr53", base.p_Cr53), ("Cr54", base.p_Cr54))),
        (element(base.p_Ni_EM10, rho_em10, base.M_Ni), (
            ("Ni58", base.p_Ni58), ("Ni60", base.p_Ni60),
            ("Ni61", base.p_Ni61), ("Ni62", base.p_Ni62),
            ("Ni64", base.p_Ni64))),
        (element(base.p_Mo_EM10, rho_em10, base.M_Mo), (
            ("Mo92", base.p_Mo92), ("Mo94", base.p_Mo94),
            ("Mo95", base.p_Mo95), ("Mo96", base.p_Mo96),
            ("Mo97", base.p_Mo97), ("Mo98", base.p_Mo98),
            ("Mo100", base.p_Mo100))),
    ):
        em10.update(isotope_split(total, pairs))
    em10.update({
        "Mn55": element(base.p_Mn_EM10, rho_em10, base.M_Mn),
        "C12": element(base.p_C_EM10, rho_em10, base.M_C),
        "Si28": element(base.p_Si_EM10, rho_em10, base.M_Si),
        "Ti48": element(base.p_Ti_EM10, rho_em10, base.M_Ti),
    })
    he_hole = base.rho0_He / (f_fuel * inv_fuel**2)
    he_gap = base.rho0_He / (f_fuel**3 * inv_clad**2)
    expected = {
        "FUEL_MOX": (fuel_temperature_c + 273.15, fuel),
        "He_HOLE": (fuel_temperature_c + 273.15, {
            "He4": he_hole * base.A_AVOGADRO / 4.002602}),
        "He_GAP": (CLAD_TEMPERATURE_C + 273.15, {
            "He4": he_gap * base.A_AVOGADRO / 4.002602}),
        "CLAD_AIM1": (CLAD_TEMPERATURE_C + 273.15, clad),
        "BOX_EM10": (SODIUM_TEMPERATURE_C + 273.15, em10),
        "COOLANT_Na": (SODIUM_TEMPERATURE_C + 273.15, {
            "Na23": rho_na * base.A_AVOGADRO / 22.98976928}),
    }
    anchors = {
        "N_Na": expected["COOLANT_Na"][1]["Na23"],
        "N_U8": fuel["U238"],
        "N_Pu39": fuel["Pu239"],
        "N_O": fuel["O16"],
        "N_He_1": expected["He_HOLE"][1]["He4"],
        "N_He_2": expected["He_GAP"][1]["He4"],
        "N_Fe56_AIM1": clad["Fe56"],
    }
    return expected, anchors


def check_contract(contract, declared_xs_path: str, base):
    if contract.get("schema") != "D4A_CORRECTED_CE_REFERENCE_V1":
        fail("contract schema differs")
    if contract.get("result_role") not in {"STATIC_INPUT_ONLY", "PRODUCTION_INPUT"}:
        fail("contract result role differs")
    physics = contract.get("physics", {})
    exact_sequence(physics.get("fuel_temperatures_c", []), FUEL_TEMPERATURES_C,
                   "fuel temperatures")
    exact_float(physics.get("clad_temperature_c"), CLAD_TEMPERATURE_C,
                "clad temperature")
    exact_float(physics.get("sodium_temperature_c"), SODIUM_TEMPERATURE_C,
                "sodium temperature")
    if physics.get("temperature_method") != "interpolation":
        fail("temperature method is not interpolation")
    if physics.get("temperature_tolerance") is not None:
        fail("temperature tolerance is present")
    if physics.get("fitted_parameters") != []:
        fail("fitted or empirical parameters are present")

    geometry = contract.get("geometry", {})
    if geometry.get("pins_per_floor") != N_PINS or geometry.get("floors") != N_FLOORS:
        fail("contract pin/floor count differs")
    exact_float(geometry.get("pin_pitch_cm"), PIN_PITCH_CM, "pin pitch")
    exact_sequence(geometry.get("pin_radii_cm", []), PIN_RADII_CM, "pin radii")
    exact_sequence(geometry.get("wrapper_and_outer_side_cm", []), HEX_SIDES_CM,
                   "hex sides")
    exact_sequence(geometry.get("z_edges_cm", []), Z_EDGES_CM, "z edges")
    if geometry.get("radial_boundary") != "white":
        fail("radial boundary is not white")
    if geometry.get("axial_end_boundaries") != "vacuum":
        fail("axial end boundaries are not vacuum")

    observables = contract.get("observables", {})
    if observables != {
        "eigenvalue": "statepoint.keff",
        "tally_name": "d4a_floor_pin_nu_fission",
        "score": "nu-fission",
        "estimator": "tracklength",
        "nuclides": ["total"],
        "cell_filter_bins": N_BINS,
        "normalization": "one global sum over all 651 bins",
    }:
        fail("observable contract differs")
    if contract.get("cross_sections_xml") != declared_xs_path:
        fail("contract cross_sections.xml path differs")

    execution = contract.get("execution", {})
    if contract["result_role"] == "STATIC_INPUT_ONLY":
        if execution != {
            "mode": "NO_RUN", "particles": 1, "batches": 2,
            "inactive": 1, "seed": 1,
            "note": "placeholder settings; not an accuracy calculation",
        }:
            fail("no-run execution contract differs")
        if contract.get("runtime_provenance") is not None:
            fail("no-run contract contains runtime provenance")
    else:
        if execution.get("mode") != "RUN":
            fail("production execution mode differs")
        for key in ("particles", "batches", "inactive", "seed", "threads"):
            if type(execution.get(key)) is not int or execution[key] <= 0:
                fail(f"invalid production execution value: {key}")
        if execution["batches"] <= 1 or execution["inactive"] >= execution["batches"]:
            fail("invalid production batch protocol")
        check_runtime_provenance(contract.get("runtime_provenance"))

    anchors = contract.get("material_anchors", [])
    if len(anchors) != N_FLOORS:
        fail("material anchor count differs")
    expected_by_floor = {}
    for floor, fuel_temperature in enumerate(FUEL_TEMPERATURES_C, start=1):
        expected, expected_anchors = independent_expected_materials(
            base, fuel_temperature
        )
        expected_by_floor[floor] = expected
        anchor = anchors[floor - 1]
        expected_header = {
            "floor": floor,
            "fuel_temperature_c": fuel_temperature,
            "fuel_temperature_k": fuel_temperature + 273.15,
            "clad_temperature_c": CLAD_TEMPERATURE_C,
            "sodium_temperature_c": SODIUM_TEMPERATURE_C,
        }
        if set(anchor) != set(expected_header) | set(expected_anchors):
            fail(f"material anchor field set differs on floor {floor}")
        if anchor.get("floor") != floor:
            fail(f"material anchor floor differs on floor {floor}")
        for key, value in expected_header.items():
            if key != "floor":
                exact_float(anchor.get(key), value, f"anchor floor {floor} {key}")
        for key, value in expected_anchors.items():
            exact_float(anchor.get(key), value, f"anchor floor {floor} {key}")
    return execution, expected_by_floor


def check_materials(output: Path, declared_xs_path: str, expected_by_floor):
    root = ET.parse(output / "materials.xml").getroot()
    xs_node = root.find("cross_sections")
    if xs_node is None or xs_node.text != declared_xs_path:
        fail("materials.xml cross_sections path differs")
    materials = root.findall("material")
    expected_names = {
        f"F{floor}_{suffix}"
        for floor in range(1, N_FLOORS + 1)
        for suffix in (
            "FUEL_MOX", "He_HOLE", "He_GAP", "CLAD_AIM1", "BOX_EM10",
            "COOLANT_Na",
        )
    }
    by_name = {entry.get("name"): entry for entry in materials}
    if len(by_name) != 18 or set(by_name) != expected_names:
        fail("materials.xml material set differs")
    for floor, expected_materials in expected_by_floor.items():
        for suffix, (temperature, expected_nuclides) in expected_materials.items():
            name = f"F{floor}_{suffix}"
            entry = by_name[name]
            exact_float(entry.get("temperature"), temperature, f"{name} temperature")
            density = entry.find("density")
            if density is None or density.get("units") != "sum":
                fail(f"{name} does not use sum density")
            nuclides = entry.findall("nuclide")
            actual = {nuclide.get("name"): nuclide.get("ao") for nuclide in nuclides}
            if len(actual) != len(nuclides) or set(actual) != set(expected_nuclides):
                fail(f"{name} nuclide set differs")
            for nuclide, expected in expected_nuclides.items():
                exact_float(actual[nuclide], expected, f"{name} {nuclide}")


def check_pin_map(output: Path):
    with (output / "pin_map.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != N_BINS:
        fail(f"pin_map.csv has {len(rows)} rows, expected {N_BINS}")
    expected_fields = {
        "floor", "fuel_temperature_c", "pin_index", "openmc_ring_index",
        "openmc_i_within", "ring_from_center", "x_index", "alpha_index",
        "x_cm", "y_cm", "fuel_cell_id",
    }
    if set(rows[0]) != expected_fields:
        fail("pin_map.csv field set differs")
    cell_ids = []
    expected_ring_counts = {ring: max(6 * ring, 1) for ring in range(9)}
    for floor, fuel_temperature in enumerate(FUEL_TEMPERATURES_C, start=1):
        floor_rows = [row for row in rows if int(row["floor"]) == floor]
        if len(floor_rows) != N_PINS:
            fail(f"floor {floor} pin count differs")
        if {int(row["pin_index"]) for row in floor_rows} != set(range(N_PINS)):
            fail(f"floor {floor} pin indices differ")
        if Counter(int(row["ring_from_center"]) for row in floor_rows) != expected_ring_counts:
            fail(f"floor {floor} radial ring counts differ")
        expected_lattice_slots = {
            (openmc_ring, within)
            for openmc_ring in range(9)
            for within in range(max(6 * (8 - openmc_ring), 1))
        }
        actual_lattice_slots = {
            (int(row["openmc_ring_index"]), int(row["openmc_i_within"]))
            for row in floor_rows
        }
        if actual_lattice_slots != expected_lattice_slots:
            fail(f"floor {floor} lattice slots differ")
        for row in floor_rows:
            exact_float(row["fuel_temperature_c"], fuel_temperature,
                        f"floor {floor} pin temperature")
            x_index = int(row["x_index"])
            alpha_index = int(row["alpha_index"])
            ring = max(abs(x_index), abs(alpha_index), abs(-alpha_index - x_index))
            if int(row["ring_from_center"]) != ring:
                fail(f"floor {floor} pin ring coordinate differs")
            expected_x = f"{math.sqrt(0.75) * PIN_PITCH_CM * x_index:.10f}"
            expected_y = f"{(0.5 * x_index + alpha_index) * PIN_PITCH_CM:.10f}"
            if row["x_cm"] != expected_x or row["y_cm"] != expected_y:
                fail(f"floor {floor} pin coordinate differs")
            cell_ids.append(int(row["fuel_cell_id"]))
    if len(set(cell_ids)) != N_BINS:
        fail("fuel cell IDs are not 651-way unique")
    return set(cell_ids)


def check_tally(output: Path, fuel_cell_ids):
    root = ET.parse(output / "tallies.xml").getroot()
    filters = root.findall("filter")
    tallies = root.findall("tally")
    if len(filters) != 1 or len(tallies) != 1:
        fail("tally/filter count differs")
    filter_node = filters[0]
    if filter_node.get("type") != "cell":
        fail("nu-fission filter is not a CellFilter")
    bins = {int(value) for value in filter_node.findtext("bins", "").split()}
    if len(bins) != N_BINS or bins != fuel_cell_ids:
        fail("CellFilter bins do not match the 651 fuel cells")
    tally = tallies[0]
    if tally.get("name") != "d4a_floor_pin_nu_fission":
        fail("tally name differs")
    if tally.findtext("scores", "").split() != ["nu-fission"]:
        fail("tally score differs")
    if tally.findtext("estimator", "") != "tracklength":
        fail("tally estimator differs")
    if tally.findtext("nuclides", "").split() != ["total"]:
        fail("tally nuclides differ")
    if tally.findtext("filters", "").split() != [filter_node.get("id")]:
        fail("tally does not reference the unique CellFilter")


def surface_coefficients(surface):
    return tuple(float(value) for value in surface.get("coeffs", "").split())


def check_geometry(output: Path, fuel_cell_ids):
    root = ET.parse(output / "geometry.xml").getroot()
    cells = root.findall("cell")
    fuel_cells = [cell for cell in cells if cell.get("name", "").endswith("_fuel")]
    actual_fuel_ids = {int(cell.get("id")) for cell in fuel_cells}
    if len(fuel_cells) != N_BINS or actual_fuel_ids != fuel_cell_ids:
        fail("geometry fuel cells do not match pin_map.csv")
    pin_universes = [cell.get("universe") for cell in fuel_cells]
    if None in pin_universes or len(set(pin_universes)) != N_BINS:
        fail("three floors do not contain 651 independent pin universes")

    lattices = root.findall("hex_lattice")
    if len(lattices) != N_FLOORS:
        fail("geometry does not contain three independent hex lattices")
    all_lattice_universes = []
    for floor in range(1, N_FLOORS + 1):
        candidates = [entry for entry in lattices
                      if entry.get("name") == f"floor_{floor}_217_pin_lattice"]
        if len(candidates) != 1:
            fail(f"floor {floor} lattice name differs")
        lattice = candidates[0]
        if lattice.get("n_rings") != "9":
            fail(f"floor {floor} lattice ring count differs")
        exact_sequence(lattice.findtext("pitch", "").split(), (PIN_PITCH_CM,),
                       f"floor {floor} lattice pitch")
        universe_ids = lattice.findtext("universes", "").split()
        if len(universe_ids) != N_PINS or len(set(universe_ids)) != N_PINS:
            fail(f"floor {floor} lattice does not have 217 unique pin universes")
        all_lattice_universes.extend(universe_ids)
    if len(set(all_lattice_universes)) != N_BINS:
        fail("pin universes are reused between axial floors")
    if set(all_lattice_universes) != set(pin_universes):
        fail("lattice universes do not match the 651 fuel-cell universes")

    surfaces = root.findall("surface")
    boundaries = Counter(
        surface.get("boundary", "transmission") for surface in surfaces
    )
    if boundaries["white"] != 6 or boundaries["vacuum"] != 2:
        fail("boundary count is not six white plus two vacuum")
    if boundaries["reflective"] != 0 or boundaries["periodic"] != 0:
        fail("reflective or periodic boundary is present")
    unexpected = set(boundaries) - {"white", "vacuum", "transmission"}
    if unexpected:
        fail(f"unexpected boundary types: {sorted(unexpected)}")

    z_surfaces = [surface for surface in surfaces if surface.get("type") == "z-plane"]
    if len(z_surfaces) != 4:
        fail("axial z-plane count differs")
    z_by_value = {}
    for surface in z_surfaces:
        coefficients = surface_coefficients(surface)
        if len(coefficients) != 1:
            fail("z-plane coefficient count differs")
        z_by_value[coefficients[0].hex()] = surface
    if set(z_by_value) != {value.hex() for value in Z_EDGES_CM}:
        fail("axial z-plane coordinates differ")
    for index, value in enumerate(Z_EDGES_CM):
        boundary = z_by_value[value.hex()].get("boundary", "transmission")
        expected = "vacuum" if index in (0, 3) else "transmission"
        if boundary != expected:
            fail(f"z={value} boundary differs")

    root_names = {
        f"floor_{floor}_{suffix}"
        for floor in range(1, N_FLOORS + 1)
        for suffix in ("lattice_region", "wrapper_EM10", "outer_Na")
    }
    roots = {cell.get("name"): cell for cell in cells if cell.get("name") in root_names}
    if set(roots) != root_names:
        fail("three-floor root cell set differs")
    for floor in range(1, N_FLOORS + 1):
        low_id = int(z_by_value[Z_EDGES_CM[floor - 1].hex()].get("id"))
        high_id = int(z_by_value[Z_EDGES_CM[floor].hex()].get("id"))
        for suffix in ("lattice_region", "wrapper_EM10", "outer_Na"):
            region = roots[f"floor_{floor}_{suffix}"].get("region", "")
            signed_ids = [int(token) for token in re.findall(r"[+-]?\d+", region)]
            if low_id not in signed_ids or -high_id not in signed_ids:
                fail(f"floor {floor} axial cell interval differs")

    radial_surfaces = [surface for surface in surfaces
                       if surface.get("type") in {"x-plane", "plane"}]
    if len(radial_surfaces) != 18:
        fail("three radial hexagon surface sets are not present")
    actual = Counter()
    for surface in radial_surfaces:
        key = (
            surface.get("type"),
            tuple(value.hex() for value in surface_coefficients(surface)),
            surface.get("boundary", "transmission"),
        )
        actual[key] += 1
    expected = Counter()
    for side_index, side in enumerate(HEX_SIDES_CM):
        boundary = "white" if side_index == 2 else "transmission"
        apothem = math.sqrt(3.0) / 2.0 * side
        for x0 in (apothem, -apothem):
            expected[("x-plane", (x0.hex(),), boundary)] += 1
        slope = math.sqrt(3.0) / 3.0
        for coefficients in (
            (slope, 1.0, 0.0, side),
            (-slope, 1.0, 0.0, side),
            (-slope, 1.0, 0.0, -side),
            (slope, 1.0, 0.0, -side),
        ):
            expected[("plane", tuple(value.hex() for value in coefficients),
                      boundary)] += 1
    if actual != expected:
        fail("radial hexagon dimensions or boundary assignment differ")


def check_settings(output: Path, execution):
    root = ET.parse(output / "settings.xml").getroot()
    if root.findtext("run_mode") != "eigenvalue":
        fail("settings run mode is not eigenvalue")
    if root.findtext("energy_mode") != "continuous-energy":
        fail("settings energy mode is not continuous-energy")
    for key in ("particles", "batches", "inactive", "seed"):
        if int(root.findtext(key, "-1")) != execution[key]:
            fail(f"settings {key} differs from contract")
    if root.findtext("temperature_method") != "interpolation":
        fail("settings temperature interpolation is absent")
    if root.findall(".//temperature_tolerance") or root.findall(".//temperature/tolerance"):
        fail("settings contains a temperature tolerance")
    sources = root.findall("source")
    if len(sources) != 1:
        fail("settings source count differs")
    if sources[0].findtext("constraints/fissionable") != "true":
        fail("initial source is not restricted to fissionable material")


def check_temperature_grids(library_paths):
    try:
        import h5py
    except ImportError as exc:
        fail(f"h5py is required for the temperature-grid audit: {exc}")
    for nuclide, path in library_paths.items():
        with h5py.File(path, "r") as handle:
            if nuclide not in handle or "kTs" not in handle[nuclide]:
                fail(f"missing kTs data for {nuclide}")
            grids = set(handle[nuclide]["kTs"].keys())
            if not {"600K", "900K", "1200K"}.issubset(grids):
                fail(f"interpolation grid is incomplete for {nuclide}")


def audit(output: Path, relocated_cross_sections: Path | None = None) -> None:
    if not output.is_dir():
        fail(f"not an output directory: {output}")
    missing = sorted(name for name in REQUIRED_OUTPUTS if not (output / name).is_file())
    if missing:
        fail(f"missing generated inputs: {missing}")
    (
        _manifest,
        _xs_path,
        base_path,
        declared_xs_path,
        library_paths,
    ) = check_manifest(output, relocated_cross_sections)
    base = load_base(base_path)
    contract = load_json(output / "model_contract.json")
    execution, expected_materials = check_contract(
        contract, declared_xs_path, base
    )
    check_materials(output, declared_xs_path, expected_materials)
    fuel_cell_ids = check_pin_map(output)
    check_tally(output, fuel_cell_ids)
    check_geometry(output, fuel_cell_ids)
    check_settings(output, execution)
    check_temperature_grids(library_paths)


def timeout_handler(_signum, _frame):
    fail("static audit exceeded the hard 30-second limit")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--cross-sections", type=Path)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, 30.0)
    try:
        audit(args.output.resolve(), args.cross_sections)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
    print("D4A CE STATIC PASS: sealed corrected materials, 651 unique fuel cells, "
          "six white sides, two vacuum ends, and one nu-fission CellFilter")


if __name__ == "__main__":
    try:
        main()
    except (AuditFailure, OSError, ValueError, ET.ParseError) as exc:
        print(f"D4A CE STATIC FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
