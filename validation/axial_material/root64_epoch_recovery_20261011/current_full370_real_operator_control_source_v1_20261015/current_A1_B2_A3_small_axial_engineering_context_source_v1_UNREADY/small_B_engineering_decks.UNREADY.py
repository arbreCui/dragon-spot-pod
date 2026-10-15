"""New current A1/B2/A3 engineering decks; original geometry/rank/axial math wholebytes."""
import math,re
from dataclasses import dataclass
from types import SimpleNamespace
class Refusal(RuntimeError):pass
RANK_RATIO_MIN=9.5367431640625e-7
EXPECTED_CONFIG={'axial_acce_accel': 0, 'axial_acce_free': 3, 'cells_per_zone': 16, 'eps_axial': 5e-08, 'eps_mccg': 2.5e-08, 'eps_radial': 2.5e-07, 'maxinr': 740, 'maxout': 500, 'radial_acce_accel': 3, 'radial_acce_free': 3, 'rank': 1, 'sn': 32, 'zone_height_cm': 50.0}

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


def rank_precision_deck(requested_rank: int = 2) -> str:
    # GREP reads the actual REAL64 POD-SIGMA-G record independently of SPOPOD's
    # requested/retained rank. Each group stores three contiguous singular values.
    if type(requested_rank) is not int or requested_rank not in (1, 2):
        raise Refusal("rank admission supports only declared uniform rank 1 or 2")
    selected = "sone" if requested_rank == 1 else "stwo"
    return f'''* No numerical solve: independent admission of the frozen basis records.
XSM_FILE BASIS :: FILE './common_basis.xsm' ;
MODULE GREP: END: ;
INTEGER igr idx rank ngroup ;
DOUBLE sone stwo sthree limit ;
LOGICAL allgood good ;
EVALUATE igr := 0 ;
GREP: BASIS :: GETVAL 'STATE-VECTOR' 8 >>ngroup<< ;
EVALUATE allgood := ngroup 370 = ;
WHILE igr 370 < DO
  EVALUATE igr := igr 1 + ;
  EVALUATE idx := igr 1 - 3 * 1 + ;
  GREP: BASIS :: GETVAL 'POD-RANK-G' <<igr>> >>rank<< ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>sone<< ;
  EVALUATE idx := idx 1 + ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>stwo<< ;
  EVALUATE idx := idx 1 + ;
  GREP: BASIS :: GETVAL 'POD-SIGMA-G' <<idx>> >>sthree<< ;
  EVALUATE limit := sone 9.5367431640625D-7 * ;
  EVALUATE good := rank {requested_rank} = sone 0.0D0 > * {selected} limit > *
    sone stwo >= * stwo sthree >= * sthree 0.0D0 >= * ;
  ECHO "AXMAT-RANK-SPECTRUM" igr rank sone stwo sthree good ;
  EVALUATE allgood := allgood good * ;
ENDWHILE ;
IF allgood THEN
  ECHO "AXMAT-RANK-INPUT-PRECISION-PASS" ;
ELSE
  ECHO "AXMAT-RANK-INPUT-PRECISION-FAIL" ;
ENDIF ;
ECHO "AXMAT-RANK-RECORD-CHECK-COMPLETE" ;
END: ;
QUIT "LIST" .
'''


def parse_rank_admission(text: str, requested_rank: int = 2) -> dict:
    if type(requested_rank) is not int or requested_rank not in (1, 2):
        raise Refusal("rank admission supports only declared uniform rank 1 or 2")
    number = r"([+-]?[\d.]+[EeDd][+-]?\d+)"
    pattern = (r"^>\|AXMAT-RANK-SPECTRUM\s+(\d+)\s+(\d+)\s+"
               + r"\s+".join([number] * 3) + r"\s+\.(TRUE|FALSE)\.")
    rows = re.findall(pattern, text, re.M)
    if len(rows) != 370 or [int(r[0]) for r in rows] != list(range(1, 371)):
        raise Refusal("rank record log must contain exactly 370 ordered group spectra")
    groups, all_good = [], True
    for group, rank, *fields in rows:
        sigma = [float(v.replace("D", "E").replace("d", "e")) for v in fields[:3]]
        good = (int(rank) == requested_rank and all(math.isfinite(v) for v in sigma)
                and sigma[0] >= sigma[1] >= sigma[2] >= 0 and sigma[0] > 0
                and sigma[requested_rank - 1] > RANK_RATIO_MIN * sigma[0])
        if good != (fields[3] == "TRUE"):
            raise Refusal("independent Python/CLE rank decisions differ; preserve evidence for review")
        all_good = all_good and good
        groups.append({"group": int(group), "production_rank": int(rank), "sigma": sigma,
                       "input_resolution_floor": RANK_RATIO_MIN * sigma[0], "pass": good})
    expected = "PASS" if all_good else "FAIL"
    labels = re.findall(r"^>\|AXMAT-RANK-INPUT-PRECISION-(PASS|FAIL)(?:\s|$)", text, re.M)
    if labels != [expected]:
        raise Refusal("rank input-precision classification is missing or inconsistent")
    threshold_field = ("sigma2_over_sigma1_strict_min" if requested_rank == 2
                       else "selected_sigma_over_sigma1_strict_min")
    return {"classification": "VALID_RANK_INPUT_PRECISION" if all_good else "INCONCLUSIVE_RANK_INPUT_PRECISION",
            "requested_rank": requested_rank, threshold_field: RANK_RATIO_MIN, "groups": groups}


def engineering_decks(plan):
 if plan['production_config']!=EXPECTED_CONFIG:raise RuntimeError('exact frozen48cell/SN32/rank1 declaration required')
 c=ProductionConfig(**plan['production_config']);c.validate()
 train="""XSM_FILE SNAP :: FILE '/dev/fd/101' ;
XSM_FILE BASIS_ARCH :: FILE './basis.xsm' ;
XSM_FILE TRACK_OUT :: FILE './axial_track_unmarked.xsm' ;
XSM_FILE MACRO_OUT :: FILE './axial_macro.xsm' ;
LINKED_LIST GEOM_AX TRACK_AX MACROLIB3 SYSTEM ;
MODULE GEO: SPOT: SPOLIB: ASM: GREP: ABORT: END: ;
INTEGER ngroup igr nmode nsnap ;
GREP: SNAP :: GETVAL 'LISTDIM' 1 >>nsnap<< ;
IF nsnap 3 <> THEN
  ABORT: ;
ENDIF ;
"""+_geometry(c)+"SYSTEM := ASM: MACROLIB3 TRACK_AX SNAP :: EDIT 1 SPOD 1 ;\n"+_rank_gate(c,'SYSTEM')+"""BASIS_ARCH := SYSTEM ;
TRACK_OUT := TRACK_AX ;
MACRO_OUT := MACROLIB3 ;
ECHO "CURRENT-B-CONTEXT-COMMON-BASIS-COMPLETE" ;
END: ; QUIT "LIST" .
"""
 rank=rank_precision_deck(c.rank).replace("FILE './common_basis.xsm'","FILE './basis.xsm'")
 initial="""XSM_FILE SYSOUT :: FILE './initial_system.xsm' ;
XSM_FILE MACRO :: FILE './axial_macro.xsm' ;
XSM_FILE AXTRACK :: FILE './axial_track.xsm' ;
XSM_FILE PACK :: FILE '/dev/fd/101' ;
XSM_FILE BASIS :: FILE './basis.xsm' ;
XSM_FILE GRCON :: FILE './global_rcon.xsm' ;
XSM_FILE RCON1 :: FILE '/dev/fd/102' ;
XSM_FILE RCON2 :: FILE '/dev/fd/103' ;
XSM_FILE RCON3 :: FILE './plane3_rcon.xsm' ;
MODULE SPOOPP64: END: ;
SYSOUT := SPOOPP64: MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2 RCON3 :: RANK 1 EDIT 0 ;
ECHO "CURRENT-B-CONTEXT-INITIAL-SYSTEM-COMPLETE" ;
END: ; QUIT "LIST" .
"""
 axial="""XSM_FILE TRACK_AX :: FILE './axial_track.xsm' ;
XSM_FILE MACROLIB3 :: FILE './axial_macro.xsm' ;
XSM_FILE SYSTEM_NEXT :: FILE './initial_system.xsm' ;
XSM_FILE AX_OUT :: FILE './ax_current.xsm' ;
LINKED_LIST AX_CURRENT ;
MODULE FLU: SPOGBAL: SPOSTATE: END: ;
"""+_axial_solve(c,False)+"""AX_OUT := AX_CURRENT ;
ECHO "CURRENT-B-CONTEXT-AXIAL-ENGINEERING-COMPLETE" ;
END: ; QUIT "LIST" .
"""
 return dict(train=train,rank=rank,initial=initial,axial=axial)
