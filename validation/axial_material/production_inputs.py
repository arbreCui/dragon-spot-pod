#!/usr/bin/env python3
"""Generate inputs for the existing production SPOT route; execute nothing.

The caller supplies new material archives and a pinned repaired runtime.  A
single A/B/A training archive builds the basis once; AAA and ABA use that exact
package through ASM FIXB.  Material construction is deliberately external.
Uniform rank 1 and rank 2 are selected by separate frozen experiment declarations.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path


@dataclass(frozen=True)
class ProductionConfig:
    cells_per_zone: int = 4
    zone_height_cm: float = 50.0
    sn: int = 8
    rank: int = 2
    eps_radial: float = 2.5e-7
    eps_axial: float = 5.0e-8
    eps_mccg: float = 1.0e-5
    maxout: int = 500
    maxinr: int = 740
    radial_acce_free: int = 3
    radial_acce_accel: int = 3
    axial_acce_free: int = 3
    axial_acce_accel: int = 0

    def validate(self) -> None:
        for name in ("cells_per_zone", "sn", "rank", "maxout", "maxinr"):
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.sn % 2 or self.sn < 4:
            raise ValueError("an even SN order >= 4 must represent SCAT 3")
        if self.rank > 2:
            raise ValueError("A/B/A training has at most two independent snapshots")
        for name in ("zone_height_cm", "eps_radial", "eps_axial", "eps_mccg"):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")
        for prefix in ("radial", "axial"):
            free = getattr(self, f"{prefix}_acce_free")
            accel = getattr(self, f"{prefix}_acce_accel")
            if type(free) is not int or type(accel) is not int:
                raise ValueError("acceleration counts must be integers")
            if min(free, accel) < 0 or free + accel == 0:
                raise ValueError("acceleration cycles must be nonnegative and nonempty")

    def contract_arguments(self, case: str) -> list[str]:
        self.validate()
        if case not in ("AAA", "ABA"):
            raise ValueError("case must be AAA or ABA")
        return ["route_contract.xsm", f"PIN-{case}",
                real_literal(self.eps_radial), real_literal(self.eps_axial),
                real_literal(self.eps_mccg), str(self.maxout), str(self.maxinr),
                str(self.radial_acce_free), str(self.radial_acce_accel), "B0"]


def real_literal(value: float) -> str:
    return f"{value:.8E}"


def _geometry(config: ProductionConfig) -> str:
    n = config.cells_per_zone
    mesh = [config.zone_height_cm * i / n for i in range(3 * n + 1)]
    mesh_lines = ["  " + " ".join(real_literal(x) for x in mesh[i:i + 5])
                  for i in range(0, len(mesh), 5)]
    # GEOIN1 consumes integer REDGET tokens here. Fortran-style n*value is
    # a character token in CLE and selects named sub-geometries, not repetition.
    mixtures = [str(zone) for zone in (1, 2, 3) for _ in range(n)]
    mix_lines = ["  " + " ".join(mixtures[i:i + 12])
                 for i in range(0, len(mixtures), 12)]
    return (f"GEOM_AX := GEO: :: CAR1D {3*n}\n"
            "  X- VOID X+ VOID\n  MESHX\n" + "\n".join(mesh_lines)
            + "\n  MIX\n" + "\n".join(mix_lines) + "\n;\n"
            "TRACK_AX := SPOT: GEOM_AX SNAP ::\n"
            "  EDIT 1 MAXR 2500 TITL 'Same-temperature material comparison'\n"
            f"  ALLG DIAM 0 SN {config.sn} SCAT 3\n;\n"
            "MACROLIB3 := SPOLIB: SNAP :: ;\n")


def _rank_gate(config: ProductionConfig, owner: str) -> str:
    # Read all retained counts, not only the requested SPOD argument: SPOPOD
    # deliberately truncates a request to each group's numerical rank.
    return f"""GREP: {owner} :: GETVAL 'STATE-VECTOR' 8 >>ngroup<< ;
IF ngroup 370 <> THEN
  ECHO "AXMAT: expected exactly 370 energy groups" ;
  ABORT: ;
ENDIF ;
EVALUATE igr := 0 ;
WHILE igr ngroup < DO
  EVALUATE igr := igr 1 + ;
  GREP: {owner} :: GETVAL 'POD-RANK-G' <<igr>> >>nmode<< ;
  IF nmode {config.rank} <> THEN
    ECHO "AXMAT: common basis rank unavailable in group" igr nmode ;
    ABORT: ;
  ENDIF ;
ENDWHILE ;
"""


def _axial_solve(config: ProductionConfig, continuation: bool) -> str:
    parent = "AX_CURRENT " if continuation else ""
    return (f"AX_CURRENT := FLU: {parent}MACROLIB3 TRACK_AX SYSTEM_NEXT ::\n"
            f"  EDIT -3 TYPE K B1 SIGS EXTE {config.maxout} "
            f"{real_literal(config.eps_axial)} REBA OFF\n"
            f"  ACCE {config.axial_acce_free} {config.axial_acce_accel}\n"
            f"  UNKT {real_literal(config.eps_axial)} "
            f"THER {config.maxinr} {real_literal(config.eps_axial)} ;\n"
            "AX_CURRENT := SPOGBAL: AX_CURRENT TRACK_AX SYSTEM_NEXT MACROLIB3 :: ;\n"
            "AX_CURRENT := SPOSTATE: AX_CURRENT TRACK_AX SYSTEM_NEXT MACROLIB3 :: ;\n")


def build_decks(config: ProductionConfig = ProductionConfig()) -> dict[str, str]:
    config.validate()
    decks: dict[str, str] = {}
    decks["common_basis.x2m"] = """* New A/B/A training archive; never train separately on AAA.
XSM_FILE SNAP :: FILE './training_snapshots.xsm' ;
XSM_FILE BASIS_ARCH :: FILE './common_basis.xsm' ;
LINKED_LIST GEOM_AX TRACK_AX MACROLIB3 SYSTEM ;
MODULE GEO: SPOT: SPOLIB: ASM: GREP: ABORT: END: ;
INTEGER ngroup igr nmode nsnap ;
GREP: SNAP :: GETVAL 'LISTDIM' 1 >>nsnap<< ;
IF nsnap 3 <> THEN
  ECHO "AXMAT: three training slots required" ;
  ABORT: ;
ENDIF ;
""" + _geometry(config) + f"""SYSTEM := ASM: MACROLIB3 TRACK_AX SNAP ::
  EDIT 1 SPOD {config.rank} ;
""" + _rank_gate(config, "SYSTEM") + """BASIS_ARCH := SYSTEM ;
ECHO "AXMAT-COMMON-BASIS-COMPLETE" ;
END: ;
QUIT "LIST" .
"""
    decks["case_setup.x2m"] = """* Run identically in AAA/ABA directories with case-specific snapshots.
XSM_FILE SNAP :: FILE './case_snapshots.xsm' ;
XSM_FILE BASIS_REF :: FILE './basis_reference.xsm' ;
XSM_FILE TRACK_OUT :: FILE './initial_axial_track.xsm' ;
XSM_FILE MACRO_OUT :: FILE './initial_axial_macrolib.xsm' ;
XSM_FILE SYSTEM_OUT :: FILE './initial_system.xsm' ;
LINKED_LIST GEOM_AX TRACK_AX MACROLIB3 SYSTEM_NEXT ;
MODULE GEO: SPOT: SPOLIB: ASM: GREP: ABORT: END: ;
INTEGER ngroup igr nmode ;
""" + _rank_gate(config, "BASIS_REF") + _geometry(config) + f"""SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX SNAP BASIS_REF ::
  EDIT 1 SPOD {config.rank} FIXB ;
TRACK_OUT := TRACK_AX ;
MACRO_OUT := MACROLIB3 ;
SYSTEM_OUT := SYSTEM_NEXT ;
ECHO "AXMAT-CASE-SETUP-COMPLETE" ;
END: ;
QUIT "LIST" .
"""
    decks["bootstrap_axial.x2m"] = """XSM_FILE TRACK_AX :: FILE './initial_axial_track.xsm' ;
XSM_FILE MACROLIB3 :: FILE './initial_axial_macrolib.xsm' ;
XSM_FILE SYSTEM_NEXT :: FILE './initial_system.xsm' ;
XSM_FILE SNAP_IN :: FILE './case_snapshots.xsm' ;
XSM_FILE SEED_AX :: FILE './seed_axial.xsm' ;
XSM_FILE SEED_SNAP :: FILE './seed_snapshots.xsm' ;
LINKED_LIST SNAP AX_CURRENT ;
MODULE FLU: SPOGBAL: SPOSTATE: SPOLEAK: END: ;
REAL leak_change ;
SNAP := SNAP_IN ;
""" + _axial_solve(config, False) + """SNAP := SPOLEAK: SNAP AX_CURRENT TRACK_AX :: >>leak_change<< ;
SEED_AX := AX_CURRENT ;
SEED_SNAP := SNAP ;
ECHO "AXMAT-BOOTSTRAP-AXIAL-COMPLETE" leak_change ;
END: ;
QUIT "LIST" .
"""
    decks["bootstrap_radial.x2m"] = f"""SEQ_BINARY TRACK_f :: FILE './initial_radial_track.bin' ;
XSM_FILE SNAP_IN :: FILE './seed_snapshots.xsm' ;
XSM_FILE AX_IN :: FILE './seed_axial.xsm' ;
XSM_FILE TRACK_AX :: FILE './initial_axial_track.xsm' ;
XSM_FILE RCONTRACT_IN :: FILE './route_contract.xsm' ;
XSM_FILE SNAP_OUT :: FILE './refreshed_snapshots.xsm' ;
LINKED_LIST SNAP TRACK AX_CURRENT RCONTRACT ;
MODULE RECOVER: GREP: SPOPROJ: END: ;
PROCEDURE SpotRefR64 SpotPlaneR64 ;
REAL keff ;
SNAP := SNAP_IN ;
AX_CURRENT := AX_IN ;
RCONTRACT := RCONTRACT_IN ;
TRACK := RECOVER: SNAP :: ITEM 1 ;
GREP: AX_CURRENT :: GETVAL 'K-EFFECTIVE' 1 >>keff<< ;
SNAP := SPOPROJ: SNAP AX_CURRENT TRACK_AX :: FIXB ;
SNAP := SpotRefR64 SNAP TRACK TRACK_f RCONTRACT ::
  <<keff>> {real_literal(config.eps_radial)}
  {config.maxout} {config.maxinr} {config.radial_acce_free} {config.radial_acce_accel} ;
SNAP_OUT := SNAP ;
ECHO "AXMAT-BOOTSTRAP-RADIAL-COMPLETE" ;
END: ;
QUIT "LIST" .
"""
    decks["picard_radial.x2m"] = f"""SEQ_BINARY TRACK_f :: FILE './initial_radial_track.bin' ;
XSM_FILE PROJECTED_IN :: FILE './projected_proposal.xsm' ;
XSM_FILE RCONTRACT_IN :: FILE './route_contract.xsm' ;
XSM_FILE TRACK_AX :: FILE './initial_axial_track.xsm' ;
XSM_FILE MACROLIB3 :: FILE './initial_axial_macrolib.xsm' ;
XSM_FILE BASIS_REF :: FILE './basis_reference.xsm' ;
XSM_FILE SYSTEM_OUT :: FILE './candidate_system.xsm' ;
XSM_FILE RADIAL_OUT :: FILE './candidate_radial.xsm' ;
LINKED_LIST PROJECTED RETURNED SYSTEM_NEXT RCONTRACT ;
MODULE ASM: END: ;
PROCEDURE SpotStepR64 ;
PROJECTED := PROJECTED_IN ;
RCONTRACT := RCONTRACT_IN ;
RETURNED := SpotStepR64 PROJECTED TRACK_f RCONTRACT :: ;
SYSTEM_NEXT := ASM: MACROLIB3 TRACK_AX RETURNED BASIS_REF ::
  EDIT 0 SPOD {config.rank} FIXB ;
SYSTEM_OUT := SYSTEM_NEXT ;
RADIAL_OUT := RETURNED ;
ECHO "AXMAT-PICARD-RADIAL-COMPLETE" ;
END: ;
QUIT "LIST" .
"""
    decks["picard_axial.x2m"] = """XSM_FILE TRACK_AX :: FILE './initial_axial_track.xsm' ;
XSM_FILE MACROLIB3 :: FILE './initial_axial_macrolib.xsm' ;
XSM_FILE PARENT_AX :: FILE './parent_axial_closed.xsm' ;
XSM_FILE RADIAL_IN :: FILE './candidate_radial.xsm' ;
XSM_FILE SYSTEM_NEXT :: FILE './candidate_system.xsm' ;
XSM_FILE CANDIDATE_AX :: FILE './candidate_axial.xsm' ;
XSM_FILE CAND_SNAP :: FILE './candidate_snapshots.xsm' ;
LINKED_LIST SNAP AX_CURRENT ;
MODULE FLU: SPOGBAL: SPOSTATE: SPOXCONV: SPOLEAK: UTL: END: ;
REAL leak_change ;
SNAP := RADIAL_IN ;
AX_CURRENT := PARENT_AX ;
AX_CURRENT := UTL: AX_CURRENT ::
  EDIT 0
  DEL 'SPOT-X-STATE'
  DEL 'SPOT-X-EPOCH'
  DEL 'SPOT-X-RRHO'
  DEL 'SPOT-X-RLEAK'
  DEL 'SPOT-X-DLEAK'
  DEL 'SPOT-X-RA' ;
""" + _axial_solve(config, True) + """AX_CURRENT := SPOXCONV: AX_CURRENT PARENT_AX :: ;
SNAP := SPOLEAK: SNAP AX_CURRENT TRACK_AX :: >>leak_change<< ;
CANDIDATE_AX := AX_CURRENT ;
CAND_SNAP := SNAP ;
ECHO "AXMAT-PICARD-AXIAL-COMPLETE" leak_change ;
END: ;
QUIT "LIST" .
"""
    decks["checker_parent.x2m"] = """XSM_FILE PARENT_IN :: FILE './parent_axial_closed.xsm' ;
XSM_FILE PARENT_OUT :: FILE './parent_for_checker.xsm' ;
LINKED_LIST AX ;
MODULE UTL: END: ;
AX := PARENT_IN ;
AX := UTL: AX :: EDIT 0 DEL 'SPOT-X-STATE' DEL 'SPOT-X-EPOCH' ;
PARENT_OUT := AX ;
END: ;
QUIT "LIST" .
"""
    return decks


def write_inputs(output: Path, config: ProductionConfig = ProductionConfig()) -> dict:
    decks = build_decks(config)
    # A fresh directory is the transaction boundary. Never overwrite a prior
    # experiment's decks or take an existing artifact directory as scratch.
    output.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for name, text in decks.items():
        content = text.encode("utf-8")
        (output / name).write_bytes(content)
        hashes[name] = hashlib.sha256(content).hexdigest()
    manifest = {
        "schema_version": 1,
        "classification": "PREPARED_INPUTS_ONLY_NO_TRANSPORT",
        "config": asdict(config),
        "required_dimensions": {"groups": 370, "regions": 8,
                                "snapshots": 3, "fission_components": 32},
        "training_slots": ["A", "B", "A"],
        "case_slots": {"AAA": ["A", "A", "A"], "ABA": ["A", "B", "A"]},
        "shared_basis_required": True,
        "rank_gate": "Every POD-RANK-G must equal declared rank before publication",
        "make_route_contract_arguments": {
            case: config.contract_arguments(case) for case in ("AAA", "ABA")},
        "required_procedures": ["SpotRefR64.c2m", "SpotPlaneR64.c2m", "SpotStepR64.c2m"],
        "required_host_tools": ["make_route_contract", "b2i_seal_bootstrap",
                                "prepare_r64_next_projected", "admit_candidate_radial",
                                "close_r64_returned", "check_one_map_xsm",
                                "check_convergence_gate"],
        "deck_sha256": hashes,
    }
    (output / "production_inputs.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="fresh deck-output directory")
    parser.add_argument("--config", type=Path, help="JSON ProductionConfig overrides")
    args = parser.parse_args()
    overrides = {} if args.config is None else json.loads(args.config.read_text())
    manifest = write_inputs(args.output, ProductionConfig(**overrides))
    print(json.dumps({"classification": manifest["classification"],
                      "output": str(args.output.resolve()),
                      "decks": len(manifest["deck_sha256"])}, sort_keys=True))


if __name__ == "__main__":
    main()
