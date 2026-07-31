#!/usr/bin/env python3
"""Fail-closed static checker for the Phase-A7 REAL64-lane blueprint."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "precision_ownership_manifest.json"
README = HERE / "README.md"
RUNNER = HERE / "run_phase_a7.sh"
RECEIPT = HERE / "phase_a7_implementation_receipt.sha256"
BASELINE_COMMIT = "3668b8736d17f14a17376f123ec19795aecd2536"
ROUTE_RECEIPT_COMMIT = "3162369d66287b3664a16c98cc03481e99d4e421"
PLACEHOLDER = "PLACEHOLDER"

ROUTE_RECEIPT_TARGETS = [
    "validation/iterative/radial_real64_route_protocol.json",
    "validation/iterative/radial_real64_route.md",
    "validation/iterative/check_radial_real64_route_protocol.py",
    "validation/iterative/test_radial_real64_route_protocol.py",
    "validation/iterative/run_radial_real64_route_tests.sh",
    "README.md",
    "SPOT_doc/validation_plan.md",
    "validation/iterative/README.md",
]
ROUTE_LIVE_REPLAY_TARGETS = [
    "validation/iterative/radial_real64_route_protocol.json",
    "validation/iterative/check_radial_real64_route_protocol.py",
    "validation/iterative/test_radial_real64_route_protocol.py",
    "validation/iterative/run_radial_real64_route_tests.sh",
]
ROUTE_EVOLVED_DOCUMENT_TARGETS = [
    "validation/iterative/radial_real64_route.md",
    "README.md",
    "SPOT_doc/validation_plan.md",
    "validation/iterative/README.md",
]

SELF_NORMALIZED_FIELDS = (
    "precision_ownership_manifest_sha256",
    "readme_sha256",
    "canonical_json_sha256",
)

EXPECTED_STATUS = {
    "classification":
        "FROZEN-COMPLETE-SUFFIXED-REAL64-OWNERSHIP-ABI-BLUEPRINT",
    "blueprint_frozen": True,
    "locked_branch_design_complete": True,
    "implementation_present": False,
    "production_source_changed": False,
    "production_route_connected": False,
    "default_runtime_route_changed": False,
    "fortran_compilation_performed": False,
    "object_link_performed": False,
    "object_execution_performed": False,
    "tracking_reads": 0,
    "transport_operator_applications": 0,
    "dragon_processes": 0,
    "radial_convergence": "NOT-EVALUATED",
    "outer_picard_convergence": "NOT-EVALUATED",
}

EXPECTED_SCIENTIFIC_SCOPE = {
    "final_method": "ONLINE-ITERATIVE-2D1D-SPOD",
    "online_radial_feedback_preserved": True,
    "physical_equations_changed": False,
    "cross_sections_changed": False,
    "geometry_changed": False,
    "tracking_changed": False,
    "source_terms_added": 0,
    "pod_rank_changed": False,
    "relaxation": None,
    "damping": None,
    "fitting": None,
    "clipping": None,
    "flux_floor": None,
    "new_empirical_parameters": None,
    "new_acceptance_thresholds": None,
}

EXPECTED_LOCKED_BRANCH = {
    "calculation_type": "S",
    "itypec": 0,
    "door": "MCCG",
    "IPHASE": 1,
    "itpij": 1,
    "itranc": 2,
    "insb": 1,
    "leaksw": False,
    "dimension": 2,
    "cyclic": False,
    "direct_vector_door": True,
    "double_heterogeneity": False,
    "lprism": False,
    "groups": 370,
    "mixtures": 8,
    "nifis": 32,
    "regions": 8,
    "unknowns_per_group": 14,
    "nani": 1,
    "nlin": 1,
    "nfunl": 1,
    "forward": True,
    "ileak": 0,
    "idir": 0,
    "stis": 1,
    "npjjm": 1,
    "isch": 11,
    "kryl": 10,
    "iaac": 80,
    "iscr": 0,
    "idifc": 0,
    "paca": 4,
    "lrebal": True,
    "initfl": 1,
    "real64_route_enabled": True,
    "route_enable_keyword": "R64",
    "ipsou_associated": True,
    "ipflup_associated": False,
    "source_mode": "FROZEN-DSOUR-WITH-ZERO-NUSIGF",
    "maxout": 500,
    "maxinr": 740,
    "solver_tolerance_h2_binary32_bits": "0x348637bd",
    "solver_tolerance_h2_decimal": "2.4999999936881070e-7",
    "acce": [3, 3],
    "lexac": False,
    "lexf": False,
    "hdd_positive": False,
    "isch_before_stis": 1,
    "transport_scheme": "NON CYCLIC - STIS 1 - SC SCHEME - TABULATED EXP",
    "unsupported_branch_action": "FAIL-CLOSED-BEFORE-TRACKING-CONSUMPTION",
    "optional_funkno_uss": {
        "required_state": "ABSENT-FOR-EVERY-ADMITTED-GROUP",
        "required_length": 0,
        "checked_before_real32_payload_read": True,
        "mismatch_action": "FAIL-CLOSED-NO-LCMGET-NO-FALLBACK",
        "reason": "The legacy DOORFV read would inject type-2 mutable flux "
                  "after the unique entry promotion.",
    },
    "derived_inner_control_flow": {
        "mcgflx_solver": "MCGMRE64-ONLY",
        "richardson_branch_live": False,
        "bicgstab_branch_live": False,
        "last_on_every_mcgmre64_to_mcgfl164_call": False,
        "macflg": False,
        "combflg": False,
        "rebflg_inside_mcgfca64": False,
        "aca_path":
            "ONE-GROUP-MCGFCA64-TO-MCGFCR64-AND-DIRECT-MCGPRA64-TO-"
            "MSRLUS1-AND-MCGABG64-TO-MCGPRA64-TO-MSRLUS1",
        "mcgfmc_live": False,
        "mcgabgr_live": False,
        "mcgaca_live": False,
        "scr_live": False,
        "macro_scattering_branch_live": False,
        "note": "LREBAL=true is implemented later by FLUBAL64 outside the "
                "MCGFL164 ACA call.",
    },
    "group_tail": {
        "initial_ngeff": 370,
        "first_group": "NG-NGEFF+1",
        "ordering": "NGIND(II)=NG-NGEFF+II",
        "last_group": 370,
        "npsys_identity": "NPSYS(IG)=0 before the tail and NPSYS(IG)=IG "
                          "for every admitted tail group",
        "jpsys_identity":
            "JPSYS(II)=LCMGIL(IPSYS,NPSYS(NGIND(II)))",
        "kpsys_identity_without_double_heterogeneity":
            "KPSYS_TAIL(II)=JPSYS(II)=LCMGIL(IPSYS,NGIND(II))",
        "initial_tail_evidence":
            "IPSOU/NBS is absent; after exact DSOUR promotion, require "
            "finite nonnegative source values and compute XCSOU64(1) "
            "directly in the unchanged IR order from "
            "FIXED_SOURCE64(KEYFLX_BASE1(IR),1)*VOL(IR), requiring "
            "XCSOU64(1)>0 exactly. The unchanged scan then gives "
            "IGDEB=1 and initial NGEFF=370 without a threshold.",
        "ngeff_may_decrease": True,
        "nconv_within_tail":
            "ANY-NONEMPTY-ORDERED-NONCONTIGUOUS-ACTIVE-MASK",
        "force_ngeff_to_370_after_gather": False,
    },
}

EXPECTED_ROUTE_INVARIANTS = {
    "mutable_state_precision":
        "IEEE-BINARY64-FROM-ONE-ENTRY-PROMOTION-THROUGH-STRICT-"
        "TERMINAL-DECISION",
    "immutable_operator_storage": "PRESERVE-FROZEN-STORED-KIND",
    "operator_real32_to_real64_use":
        "EXACT-VALUE-PROMOTION-AT-ARITHMETIC-USE",
    "terminal_public_rounding_events": 1,
    "authoritative_output_kind": "GANLIB-TYPE-4",
    "compatibility_output_kind": "GANLIB-TYPE-2",
    "type2_readback_before_terminal": False,
    "global_default_real_8_build": False,
    "unversioned_legacy_abi_kind_change": False,
    "selected_on_arm_may_fall_back_to_off": False,
    "tracking_stream_traversals_per_response": 1,
    "stis_applications_per_response": 1,
    "xdrta2_initializations_per_on_visit": 1,
    "xdrta2_role":
        "Initialize the unchanged /EXP1/ tabulated-exponential operator "
        "table after ON admission and before the first MCGSCA use; it is "
        "operator state, not mutable solver state, and may not be skipped, "
        "repeated or replaced.",
}

EXPECTED_CALL_GRAPH = [
    "FLU/FLUDRV guarded default-off dispatch",
    "FLU admitted ON -> unchanged XDRTA2 exactly once before first "
    "MCGSCA use",
    "FLU/FLUDRV ON audit arm -> SPOMOC_BEGIN64; OFF audit arm -> "
    "legacy SPOMOC_BEGIN",
    "FLU2DR64",
    "FLU2DR64 -> SPOMOC_FLU_PATH, SPOMOC_FLU_CONTEXT and "
    "SPOMOC_DOOR_BEGIN",
    "DOORFV64",
    "MCCGF64 -> MCGSIG and SPOMOC_MCCGF_BEGIN",
    "MCGFLX64 -> PRINDM for IPRINT>5 REAL64 diagnostics",
    "MCGMRE64 -> SPOMOC_SET_ROLE and SPOMOC_PUBLISH",
    "MCGFL164",
    "MCGFCS64",
    "MOCIK3",
    "MCGFCF -> MCGFFIR64_RANK_ADAPTER -> MCGFFIR -> MCGSCA -> "
    "MCGFST",
    "MCGFL164 -> SPOMOC_CAPTURE64 REAL64 type-4 audit capture",
    "MCGFCA64 -> MCGFCR64; MCGFCA64 -> MCGPRA64 -> MSRLUS1; "
    "MCGFCA64 -> MCGABG64 -> MCGPRA64 -> MSRLUS1",
    "FLUBAL64 -> ALSBD",
    "FLU2AC64",
    "FLU2DR64 strict terminal norms",
    "terminal GANLIB type-4 authority writer",
    "single terminal GANLIB type-2 compatibility mirror",
    "FLU2DR64 success -> FLUDRV -> FLU accepted host metadata and "
    "SPOT-LEAK1D writes",
    "FLU/FLUDRV selected audit arm -> SPOMOC_FINISH",
]

EXPECTED_OWNER_ORDER = [
    "FLU2DR64",
    "DOORFV64",
    "MCCGF64",
    "MCGFLX64",
    "MCGMRE64",
    "MCGFL164",
    "MCGFCS64",
    "ACA64",
    "FLUBAL64",
    "FLU2AC64",
    "FLU2DR64 terminal boundary",
]

EXPECTED_ABI_ORDER = [
    "FLU2DR64",
    "DOORFV64",
    "MCCGF64",
    "MCGFLX64",
    "MCGMRE64",
    "MCGFL164",
    "MCGFFIR64_RANK_ADAPTER",
    "MCGFCS64",
    "ACA64",
    "FLUBAL64",
    "FLU2AC64",
    "SPOMOC_BEGIN64",
    "SPOMOC_CAPTURE64",
]

EXPECTED_CONVERSION_ACTIONS = [
    (
        "FLU2DR initial type-2 FLUX group-list loads",
        "READ-REAL32-GROUP-STAGING-AND-PROMOTE-ONCE",
    ),
    (
        "FLU2DR frozen FSOURCE/DSOUR loads and outer-source "
        "reconstruction",
        "READ-REAL32-STAGING-AND-PROMOTE-ONCE",
    ),
    (
        "FLU2DR REAL(FISOUR) fission-source accumulation",
        "EXCLUDE-BY-FROZEN-ZERO-NUSIGF",
    ),
    (
        "FLU2DR ITPIJ-dependent XSDIA self-scattering and live off-group "
        "XSCAT source products using REAL(2*IAL+1)",
        "EVALUATE-MUTABLE-SOURCE-EXPRESSION-IN-REAL64",
    ),
    (
        "DOORFV FUNKNO$USS type-2 flux reload",
        "REQUIRE-ABSENT",
    ),
    (
        "DOORFV SUNKNO/FUNKNO, MCCGF FUNKNO/SUNKNO, and MCGFLX "
        "FIMEM/QFR mutable REAL32 ABIs",
        "REPLACE-WITH-CHECKED-SUFFIXED-REAL64-ABIS",
    ),
    (
        "DOORFV REAL32 FGAR source/flux diagnostic capture",
        "REPLACE-DIAGNOSTIC-DOWNCAST-WITH-REAL64-VIEW",
    ),
    (
        "MCCGF implicit REAL32 TEMP=EPS(II) convergence warning/print "
        "capture",
        "REPLACE-DIAGNOSTIC-AND-CONTROL-DOWNCAST",
    ),
    (
        "MCCGF REPS/EPS and MCCGF-to-MCGFLX EPSI REAL32 control-state "
        "ABIs",
        "REPLACE-MUTABLE-CONTROL-ABIS-WITH-REAL64",
    ),
    (
        "MCGFLX Richardson REAL(FLUX) updates and REAL32 norms",
        "EXCLUDED-BY-KRYL-10-GUARD",
    ),
    (
        "MCGMRE REAL(RHO/DENOM), REAL(FLOUT), REAL(V), and REAL(G*V)",
        "REMOVE-ALL-DOWNCASTS",
    ),
    (
        "MCGFCS QN/FI and MCGFCR FIOLD mutable REAL32 inputs plus "
        "REAL(2*IL+1) times REAL32 SC",
        "REPLACE-MUTABLE-ABIS-AND-PROMOTE-FROZEN-COEFFICIENTS",
    ),
    (
        "MCGFCA PHIIN/EPSACA mutable-control REAL32 ABIs, "
        "REAL(ABS(PHIOUT)) assigned to REAL32 FLXN/TEMP, and FLXN "
        "passed as MCGABG FAC",
        "REPLACE-MUTABLE-ABI-AND-REMOVE-DOWNCAST",
    ),
    (
        "MCGABG EPSM/FAC mutable-control REAL32 ABI, REAL(RHSN), and "
        "REAL32 EPSMAX/EPSINF/EPS2 arithmetic",
        "REPLACE-CONTROL-ABI-AND-REMOVE-DOWNCAST",
    ),
    (
        "FLUBAL REAL(XCSOU) and REAL32 rebalancing solve",
        "REMOVE-DOWNCAST-AND-USE-ALSBD",
    ),
    (
        "FLU2AC REAL(DMU), REAL32 ZMU and REAL32 flux update",
        "REMOVE-DOWNCAST",
    ),
    (
        "FLU2DR REAL32 FL(NREG) terminal flux diagnostic capture",
        "REPLACE-DIAGNOSTIC-DOWNCAST-WITH-REAL64-VIEW",
    ),
    (
        "FLU2DR RKEFF=REAL(AKEFF) under the locked ITYPEC=0 branch",
        "OMIT-DEAD-DOWNCAST",
    ),
    (
        "MCGFLX IPRINT>5 call PRINAM(FIMEM) through a REAL32 dummy",
        "USE-EXISTING-REAL64-PRINT-KERNEL",
    ),
    (
        "MCGFL1 SPOMOC_CAPTURE REAL32 QFR/EVAL diagnostic ABI",
        "REPLACE-WITH-CHECKED-SPOMOC_CAPTURE64",
    ),
    (
        "MCGSCA TAU=REAL(TAUD) and binary32 exponential-table arithmetic",
        "PRESERVE-FROZEN-MIXED-PRECISION-OPERATOR",
    ),
    (
        "Accepted public GANLIB type-2 FLUX/SOUR compatibility records",
        "ALLOW-ONE-TERMINAL-STAGING-PASS",
    ),
]

EXPECTED_CONVERSION_REPLACEMENTS = [
    "For every physical group, require an exact type-2 record of length "
    "NUNKNO, read it into an explicit REAL32 group staging array, and "
    "promote elementwise into FLUX64(:,IG,2) during the unique entry event.",
    "Require the exact frozen L_SOURCE/DSOUR hierarchy, populate "
    "FIXED_SOURCE64 once at entry, and copy it into FLUX64(:,:,4) on "
    "every outer iteration; the no-IPSOU FIXE branch is not admitted.",
    "Before source construction, require every frozen MACRO0 NUSIGF "
    "payload to be finite numerical zero, then lexically omit the ON-arm "
    "fission loop and do not read CHI; no CHI*zero IEEE edge or live "
    "fission source remains.",
    "Lock ITPIJ=1 and skip the ITPIJ=2/4 XSDIA self-scattering-addition "
    "branch; after copying outer source slice 4 to inner source slice 8, "
    "evaluate only JG!=IG XSCAT products in REAL64 with exact promotion "
    "of the frozen REAL32 coefficient and integer factor before "
    "DOORFV64.",
    "Require zero record length for every admitted group and perform no "
    "payload read.",
    "Pass QFR_TAIL64 and PHIIN_TAIL64 through explicit checked REAL64 "
    "interfaces from DOORFV64 through MCCGF64 and MCGFLX64; no implicit "
    "legacy-kind boundary is retained.",
    "Use FGAR64(NREG) for IMPX>3 region source/flux formatting and print "
    "PHIIN_TAIL64(:,II) directly for IMPX>4 full-unknown output; no "
    "diagnostic assignment may round QFR_TAIL64 or PHIIN_TAIL64.",
    "Assign TEMP64=EPS64(II), compare TEMP64>EPSI64, and print TEMP64 "
    "directly; the warning decision and diagnostic record never return "
    "to REAL32.",
    "MCCGF64 owns REPS64 and EPS64, exactly promotes the frozen EPSI "
    "binary32 value once, and passes all three through checked REAL64 "
    "interfaces without changing the tolerance value.",
    "MCGFLX64 dispatches only to MCGMRE64.",
    "Keep REPS64, EPS64, RHS64, GAR64, PHIIN_TAIL64, and all GMRES "
    "arithmetic REAL64; compute EPSINTO64=ERRTOL64/100.0_real64 after "
    "exact EPSI entry promotion.",
    "Use checked REAL64 QN64, FI64 and FIOLD64 inputs; keep SC and XSCAT "
    "stored REAL32 and promote them exactly only where used by the REAL64 "
    "source or residual expression. The locked MACFLG=false branch does "
    "not consume XSCAT.",
    "Use checked REAL64 PHIIN64 and pass EPSINTO64 unchanged through "
    "MCGFL164 EPSACC64 to MCGFCA64 EPSACA64; keep FLXN64, TEMP64, norms, "
    "AR and PSI REAL64, and pass FLXN64 unchanged as MCGABG64 FAC64.",
    "Use checked REAL64 EPSM64 and FAC64 inputs, exactly promote the "
    "inherited EPSMAX bits, and evaluate RHSN, EPSINF, EPS2 and all four "
    "cutoff guards in REAL64.",
    "Keep XCSOU64, matrix, right-hand side, solution and flux update "
    "REAL64.",
    "Keep DMU, ZMU64, AKEEP64 and all accelerated state REAL64.",
    "Use FL_PRINT64(NREG), or print the indexed FLUX64 values directly, "
    "for IPRT>=3/4 diagnostics; this does not consume the single allowed "
    "type-2 terminal mirror.",
    "Do not instantiate RKEFF in the first suffixed lane; the only later "
    "uses are guarded by ITYPEC>=2, which is outside the frozen branch.",
    "Call the existing PRINDM with the REAL64 PHIIN_TAIL64/FIMEM view and "
    "KPN; the ON arm never calls PRINAM for mutable state and allocates no "
    "REAL32 print adapter.",
    "The ON arm calls SPOMOC_CAPTURE64 with QFR_TAIL64, PHIIN_TAIL64, "
    "SOURCE64 and RESPONSE64 all REAL64; it performs the existing finite/"
    "identity checks and writes type-4 audit payloads directly without "
    "QFR/EVAL downcast or re-promotion.",
    "No change; this is immutable transport-operator arithmetic, not "
    "mutable-state storage.",
    "After strict acceptance and type-4 publication, round once into "
    "write-only REAL32 staging; never read it back.",
]

PHASE_A6_EXACT_PATHS = (
    "src/FLU.f",
    "src/FLUDRV.f",
    "src/FLU2DR.f",
    "src/DOORFV.f",
    "src/MCCGF.f",
    "src/MCGFLX.f",
    "src/MCGMRE.f",
    "src/MCGFL1.f",
    "src/MCGFCS.f",
    "src/MCGFCF.f",
    "src/MCGFFIR.f",
    "src/MCGSCA.f",
    "src/MCGFST.f",
    "src/MCGFCA.f",
    "src/MCGFCR.f",
    "src/MCGABG.f",
    "src/MCGPRA.f",
    "Utilib/src/MSRLUS1.f",
    "src/FLUBAL.f",
    "src/FLU2AC.f",
)

EXPECTED_ADDITIONAL_SOURCE_HASHES = {
    "src/MOCIK3.f":
        "5193a5a8a4922f4c20b34fae19f1d1278722c31c33dae143bf970b7e2595e007",
    "src/MCGPJJ.f":
        "b695949d91921778a7fbe9e1a377057e87d821b8d2cd8027de9413ccfcc36de2",
    "src/MCGFFAR.f":
        "4bd72f5ec4c71d22e582afdb7f3d7e259e87b308d59c888a67ce88ec33916461",
    "src/MCGFFAL.f":
        "35f4e9e862e19cce47c0caa40dbe43168265c1170653875813bed0fcaaad7056",
    "src/MCGSIG.f":
        "ab587811d170886439ff7ab1333ac2e89556f2e9deccc95a802b7d7b61eea30d",
    "src/XDRTA2.f":
        "625f5738da3ecc62b82ef29217111c2e789bd853e392ae6ecbe7c2c64e456fff",
    "src/SPOMOC.f90":
        "23a1927a133c19a86ffef9c3e0f4e619a899752cae0e7c2f0baa1bfc226502bc",
    "src/FLUGPI.f":
        "0155090fc67f38184c4602b0d330cf241a0eeba7f82c203fc25529267b5401ac",
    "Utilib/src/PRINAM.f":
        "97720815ae3160d75a5dd3d0fcf74183089f2ac693ee7c0567bfde14c012a7b6",
    "Utilib/src/MSRLUS1.f":
        "28af3f35832c64b382f5f6fde155e5d1a72eb0ca3c0eb54375e65fa3d39539bc",
}

EXPECTED_RECEIPT_PATHS = [
    "validation/iterative/radial_real64_route_freeze_receipt.sha256",
    "validation/iterative/real64_phase_a6/"
    "phase_a6_implementation_receipt.sha256",
    "README.md",
    "validation/iterative/README.md",
    "Makefile",
    "validation/iterative/real64_phase_a7/README.md",
    "validation/iterative/real64_phase_a7/"
    "precision_ownership_manifest.json",
    "validation/iterative/real64_phase_a7/check_phase_a7.py",
    "validation/iterative/real64_phase_a7/test_phase_a7_contract.py",
    "validation/iterative/real64_phase_a7/run_phase_a7.sh",
]

REQUIRED_FORBIDDEN_ACTIONS = [
    "Implement only a local QFR/PHIIN shadow owner at MCGFL1.",
    "Let the SC bundle owner also own or convert mutable REAL64 iteration "
    "state.",
    "Gather DRAGON-S0XSC inside MCGFL164 or the Phase-A6 rendezvous.",
    "Read FUNKNO$USS after entry promotion or silently ignore a nonzero "
    "FUNKNO$USS record.",
    "Return mutable state to REAL32 at DOORFV64, MCCGF64, MCGFLX64, "
    "MCGMRE64, ACA64, FLUBAL64 or FLU2AC64.",
    "Capture QFR_TAIL64, PHIIN_TAIL64, EPS64 or another mutable/control "
    "REAL64 value in a REAL32 diagnostic temporary.",
    "Pass a mutable REAL64 FIMEM view to PRINAM or to a REAL32 print "
    "adapter instead of PRINDM.",
    "Call legacy SPOMOC_CAPTURE from the ON arm or downcast QFR/EVAL for "
    "audit capture.",
    "Use legacy sequence association or a flat C_F_POINTER mapping to hide "
    "KEYFLX or PJJIND rank changes.",
    "Assign MCGFFIR64_RANK_ADAPTER to the legacy rank-2 "
    "MCGFFI_TEMPLATE procedure pointer.",
    "Form XSIXYZ(:,0) or another out-of-bounds XSI actual on the locked "
    "IDIR=0 route.",
    "Map a live tracking, MCGSIG, BC-REFL+TRAN, PJJ or PACA=4 record "
    "before exact length and GANLIB-type admission.",
    "Map active CF$MCCG with extent N1, or call legacy MCGPRA with its "
    "undersized IM(NLONG) dummy, on the ON arm.",
    "Pass DIAGF_INACTIVE32 to MCGABG64 or to an MCGPRA64 call inside "
    "MCGABG64.",
    "Change an unsuffixed legacy F77 dummy kind while retaining old callers.",
    "Use -fdefault-real-8 as the implementation mechanism.",
    "Add relaxation, damping, Aitken, Anderson mixing, fitting, clipping, "
    "a flux floor or a new threshold.",
    "Tune MAXOUT, MAXINR, KRYL, IAAC, ISCR, PACA, rebalancing, the "
    "inherited ACA cutoff or the h/h2 tolerance pair.",
    "Call a source-to-primary-response partial slice a continuous REAL64 "
    "radial lane.",
    "Use element-actual sequence association instead of the frozen direct "
    "FLUBAL64 or FLU2AC64 array sections.",
    "Admit a no-IPSOU FIXE source, a nonzero frozen NUSIGF payload, or an "
    "ITPIJ=2/4 self-scattering-addition branch into the first lane.",
    "Read CHI or execute fission-source arithmetic on the frozen "
    "zero-NUSIGF ON arm.",
    "Leave MCGFLX64 SOURCE64 or RESPONSE64 undefined before use, or "
    "overwrite an inactive/unrepresented positive-zero element outside "
    "the admitted formula/response.",
    "Use FLU rank-1 KEYFLX storage as an implicit rank-3 actual or admit "
    "different outer and MOC material-volume maps.",
    "Use unvalidated NJJS00/IJJS00/IPOS00/SCAT00 payloads or reread them "
    "after OFFGROUP32 admission.",
    "Write LINK metadata, host metadata or SPOT-LEAK1D before strict "
    "terminal acceptance.",
    "Claim rollback or crash-atomic publication after accepted-block "
    "writing has begun.",
    "Run Dragon, a tracking traversal, a transport solve, Stage 4 or a "
    "Picard trajectory under Phase-A7.",
]

EXPECTED_RUNNER = """#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../../.." && pwd)
HERE="$ROOT/validation/iterative/real64_phase_a7"
RECEIPT="$HERE/phase_a7_implementation_receipt.sha256"
LC_ALL=C
export LC_ALL

(
  cd "$ROOT"
  shasum -a 256 -c "$RECEIPT" >/dev/null
)
echo "SPOR64 PHASE-A7 RECEIPT PASS"

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/check_phase_a7.py"
PYTHONPATH="$HERE" PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \\
  test_phase_a7_contract

echo "SPOR64 PHASE-A7 STATIC OWNERSHIP/ABI BLUEPRINT PASS"
echo "SPOR64 PHASE-A7 FORTRAN-COMPILATIONS=0 OBJECT-LINKS=0"
echo "SPOR64 PHASE-A7 OBJECT-EXECUTIONS=0 TRACKING-READS=0"
echo "SPOR64 PHASE-A7 TRANSPORT-APPLICATIONS=0 DRAGON-RUNS=0"
echo "SPOR64 PHASE-A7 RADIAL-CONVERGENCE=NOT-EVALUATED"
echo "SPOR64 PHASE-A7 OUTER-PICARD-CONVERGENCE=NOT-EVALUATED"
"""


class PhaseA7Error(RuntimeError):
    """Raised when the Phase-A7 blueprint is incomplete or altered."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PhaseA7Error(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PhaseA7Error(f"cannot load manifest: {exc}") from exc
    require(isinstance(data, dict), "manifest root must be an object")
    return data


def normalized_freeze_view(data: dict[str, Any]) -> dict[str, Any]:
    """Return the canonical self-hash view with all three fields blanked."""
    normalized = copy.deepcopy(data)
    freeze = normalized["hash_freeze"]
    for field in SELF_NORMALIZED_FIELDS:
        require(field in freeze, f"missing self-normalized field: {field}")
        freeze[field] = PLACEHOLDER
    return normalized


def canonical_freeze_sha256(data: dict[str, Any]) -> str:
    encoded = json.dumps(
        normalized_freeze_view(data),
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return sha256_bytes(encoded)


def normalized_manifest_file_sha256(path: Path) -> str:
    """Hash the formatted JSON after restoring the three placeholder values."""
    text = path.read_text()
    for field in SELF_NORMALIZED_FIELDS:
        pattern = rf'("{re.escape(field)}"\s*:\s*")[^"]*(")'
        text, count = re.subn(
            pattern,
            rf"\g<1>{PLACEHOLDER}\g<2>",
            text,
            count=1,
        )
        require(count == 1, f"cannot normalize manifest field: {field}")
    return sha256_bytes(text.encode())


def git_blob(commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(
        result.returncode == 0,
        f"cannot read baseline blob {relative_path}: "
        f"{result.stderr.decode(errors='replace').strip()}",
    )
    return result.stdout


def find_owner(data: dict[str, Any], routine: str) -> dict[str, Any]:
    owners = data["owners"]
    matches = [owner for owner in owners if owner.get("routine") == routine]
    require(len(matches) == 1, f"unique owner record: {routine}")
    return matches[0]


def find_owned(owner: dict[str, Any], name: str) -> dict[str, Any]:
    items = owner["owns"]
    matches = [
        item for item in items
        if isinstance(item, dict) and item.get("name") == name
    ]
    require(len(matches) == 1, f"unique owned object: {name}")
    return matches[0]


def find_abi(data: dict[str, Any], routine: str) -> dict[str, Any]:
    matches = [
        entry for entry in data["abi_requirements"]
        if entry.get("routine") == routine
    ]
    require(len(matches) == 1, f"unique ABI record: {routine}")
    return matches[0]


def validate_hash_freeze(
    data: dict[str, Any],
    *,
    manifest_path: Path,
) -> None:
    freeze = data["hash_freeze"]
    require(freeze["baseline_commit"] == BASELINE_COMMIT, "baseline commit")
    for field in SELF_NORMALIZED_FIELDS:
        value = freeze[field]
        require(value != PLACEHOLDER, f"unfrozen hash field: {field}")
        require(
            isinstance(value, str)
            and re.fullmatch(r"[0-9a-f]{64}", value) is not None,
            f"malformed hash field: {field}",
        )
    require(
        freeze["precision_ownership_manifest_sha256"]
        == normalized_manifest_file_sha256(manifest_path),
        "normalized formatted manifest hash",
    )
    require(
        freeze["canonical_json_sha256"] == canonical_freeze_sha256(data),
        "normalized canonical manifest hash",
    )
    require(
        freeze["readme_sha256"] == sha256_file(README),
        "README direct hash",
    )
    receipts = freeze["required_upstream_receipts"]
    require(
        list(receipts)
        == [
            "validation/iterative/radial_real64_route_freeze_receipt.sha256",
            "validation/iterative/real64_phase_a6/"
            "phase_a6_implementation_receipt.sha256",
        ],
        "upstream receipt scope or order",
    )
    for relative, expected in receipts.items():
        require(expected != PLACEHOLDER, f"unfrozen receipt: {relative}")
        require(
            re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            f"malformed receipt digest: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"upstream receipt hash: {relative}",
        )
    validate_upstream_receipt_policy(freeze)
    radial_entries = validate_receipt_entries(
        "validation/iterative/radial_real64_route_freeze_receipt.sha256",
        historical_commit=ROUTE_RECEIPT_COMMIT,
        live_paths=set(ROUTE_LIVE_REPLAY_TARGETS),
    )
    require(
        list(radial_entries) == ROUTE_RECEIPT_TARGETS,
        "radial route receipt target scope or order",
    )
    require(
        set(ROUTE_LIVE_REPLAY_TARGETS)
        | set(ROUTE_EVOLVED_DOCUMENT_TARGETS)
        == set(ROUTE_RECEIPT_TARGETS)
        and not (
            set(ROUTE_LIVE_REPLAY_TARGETS)
            & set(ROUTE_EVOLVED_DOCUMENT_TARGETS)
        ),
        "radial route live/evolved partition",
    )
    validate_receipt_entries(
        "validation/iterative/real64_phase_a6/"
        "phase_a6_implementation_receipt.sha256",
    )
    validate_scoped_receipt()


def validate_upstream_receipt_policy(freeze: dict[str, Any]) -> None:
    validation_policy = freeze["upstream_receipt_validation"]
    require(
        validation_policy
        == {
            "radial_route": {
                "receipt_freeze_commit": ROUTE_RECEIPT_COMMIT,
                "historical_replay_all_entries": True,
                "live_replay_targets": ROUTE_LIVE_REPLAY_TARGETS,
                "evolved_document_targets": ROUTE_EVOLVED_DOCUMENT_TARGETS,
                "evolved_documents_are_not_live_hash_authorities": True,
            },
            "phase_a6": {
                "live_replay_all_entries": True,
            },
        },
        "upstream receipt replay policy",
    )


def validate_receipt_entries(
    relative_receipt: str,
    *,
    historical_commit: str | None = None,
    live_paths: set[str] | None = None,
) -> dict[str, str]:
    receipt = ROOT / relative_receipt
    entries: dict[str, str] = {}
    for line in receipt.read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s].*)", line)
        require(match is not None, f"malformed receipt: {relative_receipt}")
        digest, relative = match.groups()
        require(
            relative not in entries,
            f"duplicate receipt path: {relative}",
        )
        entries[relative] = digest
    require(entries, f"empty receipt: {relative_receipt}")
    if historical_commit is not None:
        for relative, digest in entries.items():
            require(
                sha256_bytes(git_blob(historical_commit, relative)) == digest,
                f"historical receipt target mismatch: {relative}",
            )
    replay = set(entries) if live_paths is None else live_paths
    require(
        replay <= set(entries),
        f"unknown live receipt target: {relative_receipt}",
    )
    for relative in replay:
        require(
            sha256_file(ROOT / relative) == entries[relative],
            f"live receipt target changed: {relative}",
        )
    return entries


def validate_readme_contract(readme: str) -> None:
    normalized = re.sub(r"\s+", " ", readme)
    required = (
        "FROZEN-COMPLETE-SUFFIXED-REAL64-OWNERSHIP-ABI-BLUEPRINT",
        "IMPLEMENTATION=NONE",
        "PRODUCTION-SOURCE-CHANGES=0",
        "DEFAULT-RUNTIME-ROUTE=UNCHANGED",
        "FORTRAN-COMPILATIONS=0",
        "OBJECT-LINKS=0",
        "OBJECT-EXECUTIONS=0",
        "TRACKING-READS=0",
        "TRANSPORT-SOLVES=0",
        "DRAGON-RUNS=0",
        "RADIAL-CONVERGENCE=NOT-EVALUATED",
        "OUTER-PICARD-CONVERGENCE=NOT-EVALUATED",
        "FLU2DR64",
        "DOORFV64",
        "MCCGF64",
        "MCGFLX64",
        "MCGMRE64",
        "MCGFL164",
        "MCGFCS64",
        "MCGPRA64",
        "PRINDM",
        "never calls REAL32 `PRINAM`",
        "SPOMOC_CAPTURE64",
        "not legacy `SPOMOC_CAPTURE`",
        "`SPOT-M-QFR/EVAL/SRC/RAW` directly as GANLIB type 4",
        "MCGSIG",
        "MOCIK3",
        "FLUBAL64",
        "FLU2AC64",
        "SC_BY_GROUP32(0:NBMIX,1,NGEFF)",
        "FUNKNO$USS",
        "ITYPEC=0",
        "KRYL=10",
        "mutually exclusive formulas",
        "An `MCGMRE` or `MCGABG` cap by itself is not a new rejection rule.",
        "omits inactive `NJJ/IJJ/IPOS/XSCAT` arguments",
        "LUCF_INACTIVE32(LC)",
        "DIAGF_INACTIVE32(N1)",
        "KEYFLX(:,1,1)",
        "KEYFLX_TRK3(NREG,NLIN,NFUNL)",
        "KEYFLX_TRK3(:,1,:)",
        "ITYLCM=1",
        "PJJIND_TRK2(NPJJM,2)",
        "Only `MCGFST` receives it.",
        "LCMLEN(CF$MCCG) = LC",
        "CF32(LC)",
        "IM(NLONG+1)",
        "FGAR64(NREG)",
        "TEMP64=EPS64(II)",
        "TEMP64>EPSI64",
        "rejects REAL32 `FGAR/TEMP` captures",
        "FL_PRINT64(NREG)",
        "omits the dead `RKEFF=REAL(AKEFF)` assignment",
        "EPSINTO64=ERRTOL64/100.0_real64",
        "independent default-false R64 selector",
        "one-pass `FLUGPI` parse",
        "`SIGNATURE` length 3",
        "`KEYFLX_HOST3(NREG,NLIN,NFUNL)`",
        "`ITPIJ=1`, `ITRANC=2`, `INSB=1`, `LEAKSW=false`",
        "`FSOURCE` is mandatory",
        "`NBS` is absent",
        "`NORM-FS` is also absent",
        "The two optional initial-flux records `B2 HETE` and "
        "`B2 B1HOM` are absent.",
        "`IPTRK/TITLE` has exact length 18",
        "does not read `CHI`",
        "interface omits dead `XSCHI/XSNUF`",
        "NJJ_OFF(NMAT,NGRP)",
        "SCAT_OFF32(NMAT*NGRP,NGRP)",
        "whole `SOURCE64` matrix once to `+0.0_real64`",
        "whole `RESPONSE64` view to `+0.0_real64`",
        "`CHILD_OK`",
        "`DRIVER_OK=false`",
        "`HOST_OK=false`",
        "does not claim rollback or crash atomicity",
        "`abs(x)<=real(huge(0.0_real32),real64)`",
        "not an empirical parameter or a convergence threshold",
        "unchanged XDRTA2 exactly once",
        "`SPOR64 CUTOFF-ACTIVE-VISIT64=<decimal-int64>`",
        "call counts byte-identical",
        "CUTOFF_ACTIVE_VISIT64",
        "MCGABG64 -> MCGFCA64 -> MCGFL164 -> MCGMRE64",
        "shared mutable leaf counter",
        "one entry-promotion event",
        "one terminal GANLIB type-2 compatibility mirror",
        "No long calculation is authorized by Phase-A7.",
        "three `hash_freeze` artifact fields",
        "restored to the literal `PLACEHOLDER`",
        "historical hashes are not misrepresented as live hashes",
        "phase_a7_implementation_receipt.sha256",
        "isolated three-line `spot-real64-phase-a7` target",
        "has no prerequisite and is not part of `all`, `tests`, or "
        "`spot-fast`",
    )
    for token in required:
        require(token in normalized, f"README contract token: {token}")
    overclaims = (
        "RADIAL-CONVERGENCE=CONVERGED",
        "OUTER-PICARD-CONVERGENCE=CONVERGED",
        "PRODUCTION-SOURCE-CHANGES=1",
        "DEFAULT-RUNTIME-ROUTE=REAL64",
    )
    for token in overclaims:
        require(token not in normalized, f"README overclaim: {token}")
    require(
        "-> MCGPRA ->" not in normalized,
        "README legacy MCGPRA ON-route edge",
    )


def validate_runner_contract(runner: str) -> None:
    require(runner == EXPECTED_RUNNER, "runner is not the exact static runner")
    lower = runner.lower()
    for token in (
        "gfortran", "ifort", "ifx", "flang", "nvfortran",
        "make -c", "cmake", "ninja", "rdragon",
    ):
        require(token not in lower, f"runner compile/execute token: {token}")
    require(
        len(re.findall(r"(?m)^[^#\n]*\bpython3\b", runner)) == 2,
        "runner must invoke exactly checker and mutation tests",
    )


def validate_makefile_contract(makefile: str) -> None:
    block = (
        ".PHONY: spot-real64-phase-a7\n"
        "spot-real64-phase-a7 :\n"
        "\tsh validation/iterative/real64_phase_a7/run_phase_a7.sh\n"
    )
    require(makefile.count(block) == 1, "exact isolated Phase-A7 block")
    baseline = git_blob(BASELINE_COMMIT, "Makefile").decode()
    require(
        makefile.replace(block, "", 1) == baseline,
        "Makefile differs from A6 baseline beyond exact Phase-A7 block",
    )
    target = re.search(
        r"(?m)^spot-real64-phase-a7\s*:(?P<prerequisites>[^\n]*)\n"
        r"(?P<recipes>(?:\t[^\n]*(?:\n|$))*)",
        makefile,
    )
    require(target is not None, "missing Phase-A7 Make target")
    require(
        target.group("prerequisites").strip() == "",
        "Phase-A7 Make target has prerequisites",
    )
    require(
        target.group("recipes").splitlines()
        == ["\tsh validation/iterative/real64_phase_a7/run_phase_a7.sh"],
        "Phase-A7 Make recipe is not exact",
    )
    ordinary = re.findall(
        r"(?m)^([A-Za-z][A-Za-z0-9_.-]*)\s*:", makefile
    )
    require(ordinary and ordinary[0] == "all", "default Make target changed")
    for name in ("all", "tests", "spot-fast"):
        dependency = re.search(
            rf"(?m)^{re.escape(name)}\s*:(.*)$",
            makefile,
        )
        require(dependency is not None, f"missing Make target: {name}")
        require(
            "spot-real64-phase-a7" not in dependency.group(1),
            f"Phase-A7 added to Make target: {name}",
        )


def validate_scoped_receipt(
    receipt_text: str | None = None,
    *,
    verify_hashes: bool = True,
) -> None:
    text = RECEIPT.read_text() if receipt_text is None else receipt_text
    require(text.strip() != PLACEHOLDER, "A7 receipt is not frozen")
    entries: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\s].*)", line)
        require(match is not None, "malformed A7 receipt line")
        digest, relative = match.groups()
        require(
            relative not in entries,
            f"duplicate A7 receipt path: {relative}",
        )
        entries[relative] = digest
    require(
        list(entries) == EXPECTED_RECEIPT_PATHS,
        "A7 receipt scope or order mismatch",
    )
    require(
        "validation/iterative/real64_phase_a7/"
        "phase_a7_implementation_receipt.sha256" not in entries,
        "A7 receipt may not hash itself",
    )
    if verify_hashes:
        for relative, expected in entries.items():
            require(
                sha256_file(ROOT / relative) == expected,
                f"A7 receipt target changed: {relative}",
            )


def validate_source_baseline_contract(data: dict[str, Any]) -> None:
    source = data["hash_freeze"]["source_baseline"]
    require(
        source["parent_protocol_commit"]
        == "94cb8b3a455d941a2d6bdcf0721daac289d1880a",
        "source baseline parent commit",
    )
    require(
        source["parent_protocol_field"]
        == "baseline.source_sha256_at_commit"
        and source["parent_source_count"] == 24
        and source["live_parent_sources_must_match_parent_hashes"] is True,
        "parent source authority",
    )
    require(
        source["phase_a6_commit"] == BASELINE_COMMIT,
        "source baseline A6 commit",
    )
    require(
        source["phase_a6_exact_path_scope"] == list(PHASE_A6_EXACT_PATHS),
        "A6 exact source path scope",
    )
    require(
        source["additional_source_sha256"]
        == EXPECTED_ADDITIONAL_SOURCE_HASHES,
        "additional source hash scope",
    )


def validate_baseline_sources(data: dict[str, Any]) -> None:
    route = load_manifest(
        ROOT / "validation/iterative/radial_real64_route_protocol.json"
    )
    parent_baseline = route["baseline"]
    parent_commit = parent_baseline["commit"]
    require(
        parent_commit == "94cb8b3a455d941a2d6bdcf0721daac289d1880a",
        "parent protocol baseline commit",
    )
    parent_sources = parent_baseline["source_sha256_at_commit"]
    require(
        isinstance(parent_sources, dict) and len(parent_sources) == 24,
        "parent protocol source map scope",
    )
    for relative, expected in parent_sources.items():
        require(
            re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
            f"parent source digest form: {relative}",
        )
        require(
            sha256_bytes(git_blob(parent_commit, relative)) == expected,
            f"parent baseline source mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live parent source drift: {relative}",
        )
    for relative in PHASE_A6_EXACT_PATHS:
        require(
            (ROOT / relative).read_bytes() == git_blob(BASELINE_COMMIT, relative),
            f"production source changed from A6 baseline: {relative}",
        )
    for relative, expected in EXPECTED_ADDITIONAL_SOURCE_HASHES.items():
        require(
            sha256_bytes(git_blob(BASELINE_COMMIT, relative)) == expected,
            f"additional baseline source mismatch: {relative}",
        )
        require(
            sha256_file(ROOT / relative) == expected,
            f"live additional source drift: {relative}",
        )


def validate(
    data: dict[str, Any],
    *,
    verify_freeze: bool = True,
    verify_environment: bool = True,
) -> None:
    require(
        data["schema"]
        == "spot-radial-real64-phase-a7-complete-suffixed-lane-"
           "ownership-abi-blueprint-v1",
        "schema",
    )
    require(data["phase"] == "A7", "phase")
    require(
        data["title"]
        == "Complete suffixed REAL64 radial-lane ownership and ABI blueprint",
        "title",
    )
    require(data["status"] == EXPECTED_STATUS, "status or authorization")
    validate_source_baseline_contract(data)
    validate_upstream_receipt_policy(data["hash_freeze"])

    authority = data["authority"]
    require(
        authority["parent_route"]
        == "validation/iterative/radial_real64_route_protocol.json",
        "parent route",
    )
    require(authority["parent_route_status"] == "FROZEN-STATIC-ONLY",
            "parent status")
    require(
        authority["phase_a6_contract"]
        == "validation/iterative/real64_phase_a6/precision_manifest.json",
        "A6 contract",
    )
    for field in (
        "phase_a6_production_admission",
        "not_a_new_scientific_protocol",
        "not_a_new_spod_model",
    ):
        expected = field != "phase_a6_production_admission"
        require(authority[field] is expected, f"authority field: {field}")
    require(
        authority[
            "a1_through_a6_are_validation_evidence_not_production_dependencies"
        ] is True,
        "validation tree cannot become a production dependency",
    )

    require(
        data["scientific_scope"] == EXPECTED_SCIENTIFIC_SCOPE,
        "scientific scope or empirical parameter",
    )
    require(data["locked_branch"] == EXPECTED_LOCKED_BRANCH,
            "locked branch")
    require(
        data["route_invariants"] == EXPECTED_ROUTE_INVARIANTS,
        "route invariants",
    )
    require(data["complete_call_graph"] == EXPECTED_CALL_GRAPH,
            "complete call graph")

    policy = data["kind_policy"]
    require(policy["mutable_real_kind"] == "real64", "mutable kind")
    require(
        policy["control_affecting_norm_kind"] == "real64",
        "control norm kind",
    )
    require(policy["source_and_response_kind"] == "real64",
            "response kind")
    require(
        policy["mutable_state_diagnostic_capture_kind"] == "real64",
        "mutable/control diagnostic capture kind",
    )
    require(
        policy["spomoc_audit_capture_input_and_type4_payload_kind"]
        == "real64",
        "SPOMOC audit capture kind",
    )
    require(
        policy["legacy_double_precision_identity"]
        == {
            "required_relation":
                "kind(0.0d0)==real64 on the selected A8 toolchain",
            "checked_reuses": [
                "PRINDM",
                "MCGFCF",
                "MCGFFIR",
                "MCGFST",
                "MSRLUS1",
                "ALSBD",
            ],
            "mismatch_action":
                "A8 compile gate fails closed; no REAL32 or "
                "nonconforming adapter is allowed.",
        },
        "legacy DOUBLE PRECISION identity",
    )
    require(policy["sc_bundle_storage_kind"] == "real32", "SC stored kind")
    require(policy["sigal_storage_kind"] == "real32", "SIGAL stored kind")
    require(policy["mccg_cpo_storage_kind"] == "real32",
            "CPO stored kind")
    require(
        policy["inactive_caz0_and_xsi_storage_kind"] == "real64",
        "inactive CAZ0/XSI storage kind",
    )
    require(
        policy["mccg_quadrature_zmu_wzmu_storage_kind"] == "real32"
        and "zmu_wzmu_storage_kind" not in policy,
        "MCCG quadrature stored kind",
    )
    require(
        policy["frozen_mixed_precision_operator"]
        == {
            "sequence": [
                "MCGFCF",
                "MCGFFIR64_RANK_ADAPTER",
                "MCGFFIR",
                "MCGSCA",
                "MCGFST",
            ],
            "mcgsca_tau_real32_conversion_preserved": True,
            "binary32_exponential_table_arithmetic_preserved": True,
            "interpretation":
                "These are immutable operator operations, not a mutable-"
                "state round trip.",
        },
        "frozen mixed-precision operator",
    )
    require(
        data["rank_shape_adapters"]
        == {
            "outer_keyflx_base1": {
                "source": "FLU2DR64 KEYFLX(NREG,NLIN,NFUNL)",
                "locked_guard": "NLIN=1 and NFUNL=1",
                "actual": "KEYFLX(:,1,1)",
                "destination":
                    "DOORFV64 and MCCGF64 KEYFLX_BASE1(NREG)",
                "rank": 1,
                "contiguous": True,
            },
            "tracking_keyflx_trk3": {
                "descriptor_owner": "MCCGF64",
                "pointee_owner": "IPTRK KEYFLX$ANIS",
                "admission":
                    "Require exact record length NREG*NLIN*NFUNL and "
                    "GANLIB integer type ITYLCM=1 before LCMGPD.",
                "mapping":
                    "C_F_POINTER directly with shape "
                    "(NREG,NLIN,NFUNL)",
                "name": "KEYFLX_TRK3",
                "rank": 3,
                "passed_rank3_to": [
                    "MCGFLX64",
                    "MCGMRE64",
                    "MCGFL164",
                ],
                "flat_rank1_mapping_allowed": False,
            },
            "stis_aca_keyflx_stis2": {
                "source": "contiguous KEYFLX_TRK3(NREG,1,NFUNL)",
                "guard_before_section": "NLIN=1 and exact source shape",
                "actual": "KEYFLX_TRK3(:,1,:)",
                "rank": 2,
                "contiguity_basis":
                    "The first and third dimensions are complete and the "
                    "removed middle dimension has frozen extent one.",
                "passed_rank2_to": ["MCGFST", "MCGFCA64"],
                "sequence_association_allowed": False,
                "pointer_alias_created": False,
            },
            "mcgfcf_to_mcgffir_keyflx_rank2": {
                "caller":
                    "Legacy MCGFCF receives MCGFFIR64_RANK_ADAPTER as "
                    "SUBFFI only after NLIN=1 and NFUNL=1 are checked.",
                "adapter_dummy":
                    "integer :: KEYFLX_TRK3(NREG,1,1)",
                "actual": "KEYFLX_TRK3(:,:,1)",
                "rank": 2,
                "contiguity_basis":
                    "The first and second dimensions are complete and "
                    "the removed third dimension has frozen extent one.",
                "callee":
                    "legacy MCGFFIR with checked dummy KEYFLX(NREG,1)",
                "external_abi":
                    "Global external subroutine with explicit-shape "
                    "dummies only; no assumed-shape, assumed-rank, "
                    "OPTIONAL, POINTER, ALLOCATABLE, BIND(C) or "
                    "module-procedure ABI.",
                "subsch_rule":
                    "Keep SUBSCH as legacy EXTERNAL and forward it "
                    "unchanged.",
                "caller_guard":
                    "MCGFL164 proves NLF=NLIN=NFUNL=1 before entering "
                    "MCGFCF because NFUNL is not present in the callback "
                    "argument list.",
                "parallel_safety":
                    "No SAVE, COMMON, module state, I/O or guard state; "
                    "calls may occur inside the legacy MCGFCF OpenMP "
                    "region.",
                "sequence_association_allowed": False,
                "flat_alias_allowed": False,
                "numerical_work":
                    "None; the adapter forwards every non-KEYFLX dummy "
                    "in the exact legacy MCGFFIR type, kind, order and "
                    "explicit extent, and performs only the explicit "
                    "rank normalization.",
                "proof_boundary":
                    "A8 proves the external bridge object and its "
                    "checked internal MCGFFIR call compile; it does not "
                    "misrepresent legacy MCGFCF's implicit EXTERNAL "
                    "callback as an explicit procedure interface.",
            },
            "flubal64_outer_sections": {
                "keyflx":
                    "KEYFLX(:,1,1), rank 1 after NLIN=NFUNL=1",
                "matalb":
                    "MATALB(NNN+1:NNN+ICREB), rank 1, exact extent "
                    "ICREB",
                "surfac":
                    "V(NNN+1:NNN+ICREB), rank 1, exact extent ICREB",
                "mutable_flux":
                    "FLUX64(:,:,7), rank 2, exact shape "
                    "(NUNKNO,NGRP)",
                "sequence_association_allowed": False,
            },
            "flu2ac64_history_sections": {
                "inner_flux":
                    "FLUX64(:,:,5:7), rank 3, exact shape "
                    "(NUNKNO,NGRP,3)",
                "inner_akeep":
                    "AKEEP64(5:7), rank 1, exact extent 3",
                "outer_flux":
                    "FLUX64(:,:,1:3), rank 3, exact shape "
                    "(NUNKNO,NGRP,3)",
                "outer_akeep":
                    "AKEEP64(1:3), rank 1, exact extent 3",
                "sequence_association_allowed": False,
            },
            "tracking_pjjind_trk2": {
                "descriptor_owner": "MCGFL164",
                "pointee_owner": "IPTRK PJJIND$MCCG",
                "admission":
                    "Immediately before the single MCGFST call, require "
                    "exact record length 2*NPJJM and integer record type.",
                "mapping":
                    "LCMGPD followed by C_F_POINTER directly with shape "
                    "(NPJJM,2)",
                "name": "PJJIND_TRK2",
                "rank": 2,
                "passed_rank2_to": ["MCGFST"],
                "lifetime":
                    "From the local mapping until the single MCGFST return "
                    "within the same MCGFL164 response call.",
                "flat_rank1_mapping_allowed": False,
            },
        },
        "explicit KEYFLX/PJJIND rank adapters",
    )

    epochs = data["ownership_epochs"]
    require(epochs["radial_lane_epoch"]["owner"] == "FLU2DR64",
            "radial owner")
    require(
        epochs["mccg_operator_epoch"]["owner"] == "MCCGF64",
        "operator owner",
    )
    require(
        epochs["routine_scratch_epoch"][
            "save_common_or_module_singleton_allowed"
        ] is False,
        "hidden mutable state",
    )
    for epoch in ("radial_lane_epoch", "door_tail_epoch",
                  "mccg_operator_epoch"):
        require(
            epochs[epoch]["borrowed_objects_may_escape"] is False,
            f"borrowed lifetime escape: {epoch}",
        )

    require(
        data["audit_lifecycle"]
        == {
            "owner": "pre-existing SPOMOC_AUDIT diagnostic module state",
            "storage":
                "Existing SAVE module flags, integer STATE-VECTOR and "
                "borrowed GANLIB handles only; no solver REAL state or "
                "operator array is stored.",
            "new_on_begin": "SPOMOC_BEGIN64",
            "off_begin": "legacy SPOMOC_BEGIN unchanged",
            "on_begin_admission": {
                "arm": "1 or 2 when enabled; 0 returns inactive",
                "door": "MCCG",
                "itypec": 0,
                "groups": 370,
                "unknowns": 14,
                "regions": 8,
                "maxout": 500,
                "maxinr": 740,
                "acce": [3, 3],
                "initfl": 1,
                "epsout_epsunk_epsinr":
                    "unchanged exact binary32 bits",
                "forward": True,
                "ileak": 0,
                "lrebal": True,
            },
            "admission_delta_from_legacy_audit":
                "Only the audit-only MAXOUT and ACCE identities change "
                "from the obsolete one-map capture constants to the "
                "already frozen solver values MAXOUT=500 and ACCE=(3,3); "
                "no solver input is changed.",
            "shared_existing_calls": [
                "SPOMOC_FLU_PATH",
                "SPOMOC_FLU_CONTEXT",
                "SPOMOC_DOOR_BEGIN",
                "SPOMOC_MCCGF_BEGIN",
                "SPOMOC_SET_ROLE",
                "SPOMOC_PUBLISH",
                "SPOMOC_FINISH",
            ],
            "ordered_on_hooks": [
                "FLUDRV calls SPOMOC_BEGIN64 after frozen FLU controls "
                "are known and before FLU2DR64 state mutation or tracking "
                "consumption.",
                "FLU2DR64 calls SPOMOC_FLU_PATH exactly at the legacy "
                "direct-vector path check.",
                "At the first eligible IT=1,JT=1 door visit, FLU2DR64 "
                "calls SPOMOC_FLU_CONTEXT and then SPOMOC_DOOR_BEGIN "
                "immediately before DOORFV64.",
                "MCCGF64 calls SPOMOC_MCCGF_BEGIN once after exact "
                "group/geometry/control identities are known and before "
                "MCGFLX64.",
                "MCGMRE64 calls SPOMOC_SET_ROLE immediately before every "
                "MCGFL164 response call using the unchanged role and "
                "iteration identities.",
                "Every MCGFL164 call invokes SPOMOC_CAPTURE64 exactly at "
                "the legacy post-MCGFST, pre-ACA point; only active "
                "primary role 1 iteration 1 writes the tuple.",
                "MCGMRE64 calls SPOMOC_PUBLISH immediately after the "
                "first primary MCGFL164 return.",
                "FLUDRV calls SPOMOC_FINISH after the selected FLU2DR64 "
                "route returns.",
            ],
            "missing_reordered_or_duplicate_hook_action":
                "FAIL-CLOSED-AUDIT-WITHOUT-SOLVER-FEEDBACK",
            "real64_capture": "SPOMOC_CAPTURE64",
            "may_feed_solver_branch_state_terminal_or_publication": False,
            "solver_owner_or_cutoff_counter_may_use_saved_module_state":
                False,
            "interpretation":
                "This narrow pre-existing audit lifecycle exception does "
                "not weaken the prohibition on hidden mutable solver "
                "state, operator ownership or cutoff counters.",
        },
        "SPOMOC audit lifecycle and no-feedback boundary",
    )

    require(
        [owner["routine"] for owner in data["owners"]]
        == EXPECTED_OWNER_ORDER,
        "owner scope or order",
    )

    flu2dr = find_owner(data, "FLU2DR64")
    require(flu2dr["role"] == "UNIQUE-MUTABLE-RADIAL-STATE-OWNER",
            "mutable owner role")
    flux = find_owned(flu2dr, "FLUX64")
    require(
        flux["declaration"]
        == "real(real64), allocatable :: FLUX64(:,:,:)"
        and flux["allocation_shape"] == "(NUNKNO,NGRP,8)",
        "eight-slice owner declaration",
    )
    require(
        flux["slots"]
        == {
            "1": "old outer flux",
            "2": "present outer flux",
            "3": "new outer flux",
            "4": "outer source",
            "5": "old inner flux",
            "6": "present inner flux",
            "7": "new inner flux",
            "8": "inner source",
        },
        "eight-slice meanings",
    )
    require(flux["may_be_replaced_by_real32_storage"] is False,
            "REAL32 owner replacement")
    fixed_source = find_owned(flu2dr, "FIXED_SOURCE64")
    require(
        fixed_source["declaration"]
        == "real(real64), allocatable :: FIXED_SOURCE64(:,:)"
        and fixed_source["allocation_shape"] == "(NUNKNO,NGRP)"
        and fixed_source["later_lcm_payload_reads_allowed"] is False,
        "single-promoted fixed-source owner",
    )
    require(
        fixed_source["population"]
        == "At entry only, read each admitted FSOURCE/DSOUR type-2 group "
           "element through an explicit REAL32 staging array and promote "
           "elementwise.",
        "fixed-source population",
    )
    require(
        flu2dr["source_update_order"]
        == {
            "outer_iteration": [
                "Copy the immutable FIXED_SOURCE64 cache into "
                "FLUX64(:,:,4).",
                "Admit the frozen MACRO0 only after every NUSIGF payload "
                "is finite numerical zero; lexically omit the ON-arm "
                "fission loop and do not consume CHI, so no fission "
                "arithmetic is a live source term.",
                "Compute XCSOU64 from the resulting outer source without "
                "another type-2 payload read.",
            ],
            "inner_iteration": [
                "Copy FLUX64(:,:,6) into FLUX64(:,:,7), then copy "
                "FLUX64(:,:,4) into FLUX64(:,:,8).",
                "With exact ITPIJ=1, skip the ITPIJ=2/4 XSDIA "
                "self-scattering-addition block.",
                "With exact ILEAK=0, skip the ECCO and TIBERE "
                "leakage-source blocks.",
                "Accumulate only live JG!=IG off-group XSCAT products "
                "into FLUX64(:,:,8), promoting the frozen REAL32 "
                "coefficient and integer factor exactly at arithmetic "
                "use.",
                "Call DOORFV64 only after the ordered source construction "
                "is complete.",
            ],
            "excluded_first_lane_branches": [
                "No-IPSOU KPMACR/FIXE source loading",
                "ITPIJ=2/4 XSDIA self-scattering addition",
                "Any ON-arm CHI/fission arithmetic or nonzero NUSIGF "
                "contribution",
                "ILEAK>=6 leakage-source construction",
            ],
        },
        "exact frozen source update order",
    )
    require(
        flu2dr["off_group_operator_admission"]
        == {
            "position":
                "After frozen host/source admission and before the first "
                "inner-source construction or FLUBAL64 call.",
            "owner":
                "FLU2DR64 owns one immutable stored-REAL32 OFFGROUP32 "
                "bundle for the radial_lane_epoch and passes the same "
                "admitted bundle read-only to source construction and "
                "FLUBAL64.",
            "storage": {
                "NJJ_OFF": "integer :: NJJ_OFF(NMAT,NGRP)",
                "IJJ_OFF": "integer :: IJJ_OFF(NMAT,NGRP)",
                "IPOS_OFF": "integer :: IPOS_OFF(NMAT,NGRP)",
                "NSCAT_OFF": "integer :: NSCAT_OFF(NGRP)",
                "SCAT_OFF32":
                    "real(real32) :: SCAT_OFF32(NMAT*NGRP,NGRP)",
            },
            "initialization_and_fill":
                "Initialize NSCAT_OFF=0 and all SCAT_OFF32 elements to "
                "+0.0_real32 once; for each group copy exactly the "
                "admitted SCAT00 payload into "
                "SCAT_OFF32(1:NSCAT_OFF(IG),IG), and never read the "
                "padded tail.",
            "group_list":
                "IPMACR/GROUP has exact length NGRP and GANLIB type 10.",
            "per_group_records": {
                "NJJS00": "exact length NMAT and GANLIB type 1",
                "IJJS00": "exact length NMAT and GANLIB type 1",
                "IPOS00": "exact length NMAT and GANLIB type 1",
                "SCAT00":
                    "GANLIB type 2 with admitted stored length not "
                    "exceeding NMAT*NGRP",
            },
            "index_guards":
                "For every mixture, NJJ>=0; if NJJ>0 then IPOS>=1, "
                "IPOS+NJJ-1 is within the group SCAT00 extent, and the "
                "descending JG sequence beginning at IJJ remains in "
                "1..NGRP.",
            "value_guards":
                "Every admitted SCAT00 value is finite; every MATCOD "
                "value is in 1..NMAT and addresses the admitted integer "
                "records.",
            "reuse":
                "Read and validate each group once into OFFGROUP32; "
                "FLU2DR64 source construction and FLUBAL64 receive the "
                "rectangular members through explicit rank/shape "
                "read-only interfaces, perform no later "
                "NJJS00/IJJS00/IPOS00/SCAT00 LCMGET, and exactly promote "
                "SCAT_OFF32 only at arithmetic use.",
        },
        "admitted immutable off-group operator bundle",
    )
    cutoff_visit = find_owned(flu2dr, "CUTOFF_ACTIVE_VISIT64")
    require(
        cutoff_visit
        == {
            "name": "CUTOFF_ACTIVE_VISIT64",
            "kind": "integer(int64)",
            "initialization":
                "0_int64 once at admitted REAL64-lane entry",
            "purpose":
                "Exact visit-total count of production-versus-EPSMAX=0 "
                "Boolean differences returned by all completed MCGABG64 "
                "calls.",
            "observation":
                "On every normal ON-arm FLU2DR64 return, emit exactly one "
                "ASCII line 'SPOR64 "
                "CUTOFF-ACTIVE-VISIT64=<decimal-int64>' after the "
                "terminal decision; use an int64 edit path with no "
                "narrowing and emit no such line on OFF.",
            "lifetime": "radial_lane_epoch",
            "may_modify_physical_state_terminal_or_publication": False,
        },
        "visit-total cutoff diagnostic owner",
    )
    fl_print = find_owned(flu2dr, "FL_PRINT64")
    require(
        fl_print
        == {
            "name": "FL_PRINT64",
            "declaration":
                "real(real64), allocatable :: FL_PRINT64(:)",
            "allocation_shape": "(NREG)",
            "guard": "Allocate only when IPRT>=3.",
            "population":
                "Initialize to +0.0_real64 and copy represented "
                "FLUX64(IND,IG,3) values without kind conversion for "
                "scalar-flux or higher-moment formatting.",
            "purpose":
                "Terminal diagnostic formatting only; this is not the "
                "type-2 compatibility mirror and is never read by the "
                "solver.",
            "lifetime": "radial_lane_epoch",
        },
        "FLU2DR64 REAL64 terminal print view",
    )
    require(
        flu2dr["terminal_diagnostic_contract"]
        == {
            "state_view":
                "Use FL_PRINT64(NREG), or an equivalent direct REAL64 "
                "indexed view, for every IPRT>=3/4 flux print.",
            "real32_capture_allowed": False,
            "counts_as_terminal_type2_mirror": False,
            "may_modify_terminal_or_publication": False,
            "locked_dead_rkeff_assignment":
                "Omit RKEFF=REAL(AKEFF) from the ITYPEC=0 suffixed "
                "branch; ITYPEC>=2 K-effective storage is outside the "
                "first lane.",
        }
        and "Copying FLUX64 into a REAL32 FL array for IPRT diagnostics"
        in flu2dr["forbidden"],
        "FLU2DR64 terminal diagnostic no-downcast contract",
    )

    door = find_owner(data, "DOORFV64")
    require(
        find_owned(door, "QFR_TAIL64")["declaration"]
        == "real(real64), allocatable :: QFR_TAIL64(:,:)"
        and find_owned(door, "QFR_TAIL64")["allocation_shape"]
        == "(NUN,NGEFF)",
        "QFR tail ABI",
    )
    require(
        find_owned(door, "PHIIN_TAIL64")["declaration"]
        == "real(real64), allocatable :: PHIIN_TAIL64(:,:)"
        and find_owned(door, "PHIIN_TAIL64")["allocation_shape"]
        == "(NUN,NGEFF)",
        "PHIIN tail ABI",
    )
    fgar = find_owned(door, "FGAR64")
    require(
        fgar
        == {
            "name": "FGAR64",
            "declaration": "real(real64), allocatable :: FGAR64(:)",
            "allocation_shape": "(NREG)",
            "guard": "Allocate only when IMPX>3.",
            "population":
                "For source or region-flux printing, initialize to "
                "+0.0_real64 and copy represented QFR_TAIL64 or "
                "PHIIN_TAIL64 values without kind conversion.",
            "purpose":
                "Diagnostic formatting only; it is never solver input, "
                "state, or a control value.",
            "lifetime": "door_tail_epoch",
        },
        "DOORFV64 REAL64 diagnostic region view",
    )
    tail = door["tail_contract"]
    for field in (
        "ngind_is_checked_before_copy",
        "tail_is_strictly_consecutive",
        "npsys_is_zero_before_tail_and_identity_on_tail",
        "output_flux_scattered_back_only_after_success",
        "failure_is_atomic_for_parent_state",
    ):
        require(tail[field] is True, f"door tail: {field}")
    for field in ("input_source_scattered_back", "real32_staging_allowed"):
        require(tail[field] is False, f"door tail: {field}")
    require(
        tail["kpsys_identity"]
        == "KPSYS_TAIL(II)=LCMGIL(IPSYS,NGIND(II)) because double "
           "heterogeneity is false",
        "door KPSYS identity",
    )
    require(
        tail["successful_inner_return"]
        == "ADMITTED-STRUCTURALLY-VALID-FINITE-NORMAL-RETURN"
        and tail["mccgf_numerical_convergence_required_for_scatter"] is False
        and tail["mccgf_or_aca_cap_changes_scatter_rule"] is False
        and tail["inner_cap_policy"]
        == "Legacy MCGMRE MAXIT and MCGABG MAXINT exhaustion return "
           "normally and do not create a new DOORFV64 scatter veto; "
           "existing iteration and residual records are retained where "
           "available."
        and tail["diagnostic_precision"]
        == "For IMPX>3, region source and flux views use FGAR64(NREG); "
           "for IMPX>4, full unknown flux output reads "
           "PHIIN_TAIL64(:,II) directly. No REAL32 diagnostic capture of "
           "QFR_TAIL64 or PHIIN_TAIL64 is allowed.",
        "inner normal-return and cap scatter policy",
    )
    mccgf = find_owner(data, "MCCGF64")
    require(
        "NGIND physical-group identities" in mccgf["borrows"]
        and "NGIND and NCONV group identities" not in mccgf["borrows"],
        "MCCGF group-identity borrowing",
    )
    discrete = find_owned(mccgf, "discrete_convergence_state")
    require(
        discrete["members"] == ["ITST(NGEFF)", "NCONV(NGEFF)", "LNCONV"]
        and discrete["kind"] == "integer/logical",
        "MCCGF convergence-state ownership",
    )
    convergence_records = find_owned(mccgf, "convergence_records64")
    require(
        convergence_records["kind"] == "real64"
        and convergence_records["members"]
        == ["REPS64(MAXI,NGEFF)", "EPS64(NGEFF)", "TEMP64"]
        and convergence_records["diagnostic_rule"]
        == "For each printed group set TEMP64=EPS64(II), compare "
           "TEMP64>EPSI64 for the unchanged warning, and print TEMP64 "
           "without a REAL32 assignment.",
        "MCCGF REAL64 convergence diagnostic",
    )
    sc = find_owned(mccgf, "SC_BY_GROUP32")
    require(
        sc["declaration"]
        == "real(real32), allocatable :: SC_BY_GROUP32(:,:,:)"
        and sc["allocation_shape"] == "(0:NBMIX,1,NGEFF)",
        "S0 bundle kind/shape",
    )
    require(
        sc["population"]
        == "For II=1..NGEFF, copy the exact NBMIX+1 type-2 "
           "DRAGON-S0XSC record from KPSYS_TAIL(II) into "
           "SC_BY_GROUP32(:,1,II) without numerical conversion.",
        "S0 exact complete gather",
    )
    require(
        sc["ordering_identity"]
        == "SC_BY_GROUP32(:,1,II), KPSYS_TAIL(II) and NGIND(II) "
           "describe the same admitted group.",
        "SC/NGIND/KPSYS ordering",
    )
    require(
        sc["local_index_rule"]
        == "Use II as the third-dimension array index; NGIND(II) is a "
           "physical-group label and is never used as a local bundle "
           "subscript.",
        "SC local/physical index separation",
    )
    require(sc["mutability"] == "read-only after complete population",
            "SC immutability")
    sigal = find_owned(mccgf, "SIGAL32")
    require(
        sigal["declaration"]
        == "real(real32), allocatable :: SIGAL32(:,:)"
        and sigal["allocation_shape"] == "(-6:NBMIX,NGEFF)",
        "SIGAL owner declaration",
    )
    tracking_views = find_owned(
        mccgf,
        "checked_tracking_index_view_descriptors",
    )
    require(
        tracking_views
        == {
            "name": "checked_tracking_index_view_descriptors",
            "descriptor_ownership":
                "MCCGF64 owns only the local descriptors; IPTRK owns the "
                "immutable pointees.",
            "members": ["KEYFLX_TRK3(NREG,NLIN,NFUNL)"],
            "mapping":
                "Map KEYFLX$ANIS directly at rank three after exact "
                "record-length, GANLIB integer-type and locked-shape "
                "checks; never map it flat and rely on sequence "
                "association.",
            "mutability": "read-only",
            "lifetime": "mccg_operator_epoch",
        },
        "MCCGF64 tracking KEYFLX descriptor",
    )
    regular_tracking = find_owned(mccgf, "regular_tracking_support")
    require(
        regular_tracking
        == {
            "name": "regular_tracking_support",
            "guard":
                "NDIM=2, LPRISM=false, NANI=NLIN=NFUNL=1 and IDIR=0",
            "owned_storage": [
                "integer, allocatable :: MATALB_TRK(-NSOUT:NREG)",
                "real(real64), allocatable :: "
                "CAZ1_TRACK64(NANGL)",
                "real(real64), allocatable :: "
                "CAZ2_TRACK64(NANGL)",
                "real(real32), allocatable :: CPO32(NMU)",
            ],
            "borrowed_views": [
                "real(real32), contiguous :: ZMU32(NMU)",
                "real(real32), contiguous :: WZMU32(NMU)",
                "real(real32), contiguous :: V_TRACK32(NLONG)",
                "integer, contiguous :: NZON_TRK1(NLONG)",
                "integer, contiguous :: KEYCUR_TRK1(NLONG-NREG)",
            ],
            "record_admission": {
                "XMU$MCCG":
                    "length NMU, GANLIB type 2, before LCMGET into CPO32",
                "WZMU$MCCG":
                    "length NMU, GANLIB type 2, before "
                    "LCMGPD/C_F_POINTER",
                "ZMU$MCCG":
                    "length NMU, GANLIB type 2, before "
                    "LCMGPD/C_F_POINTER",
                "V$MCCG":
                    "length NLONG, GANLIB type 2, before "
                    "LCMGPD/C_F_POINTER",
                "NZON$MCCG":
                    "length NLONG, GANLIB type 1, before "
                    "LCMGPD/C_F_POINTER",
                "KEYCUR$MCCG":
                    "length NLONG-NREG, GANLIB type 1, before "
                    "LCMGPD/C_F_POINTER",
            },
            "cpo_rule":
                "Preserve the stored XMU$MCCG values even though the "
                "locked isotropic MCGFCF branch does not read CPO.",
            "lifetime": "mccg_operator_epoch",
        },
        "regular tracking storage and CPO provenance",
    )
    require(mccgf["downstream_lcm_sc_reads_allowed"] is False,
            "downstream SC gather")
    require(
        mccgf["admission_checks_before_sc_population"]
        == [
            "Locked branch identity including ISCH=11",
            "KPSYS length equals NGEFF",
            "Every KPSYS handle is associated",
            "NPSYS is zero before the tail and identity-valued on the tail",
            "With LBIHET=false, KPSYS_TAIL(II) equals "
            "LCMGIL(IPSYS,NGIND(II))",
            "NGIND is the exact admitted consecutive tail",
            "Every DRAGON-S0XSC record has exact length NBMIX+1 and type 2",
        ],
        "SC admission and exact record contract",
    )
    require(
        mccgf["tracking_index_admission"]
        == [
            "KEYFLX$ANIS has exact length NREG*NLIN*NFUNL and GANLIB "
            "integer type ITYLCM=1 before LCMGPD, then is mapped directly "
            "as KEYFLX_TRK3(NREG,NLIN,NFUNL)",
            "NLIN=1 is checked before KEYFLX_TRK3 is passed downstream",
        ],
        "tracking KEYFLX record/rank admission",
    )
    require(
        mccgf["regular_tracking_header_admission"]
        == {
            "position":
                "Immediately after reading the regular-tracking header "
                "and before reading the MATALB payload or any track.",
            "required_equalities": [
                "NREG_TRACK=NBREG=N2REG=8",
                "NSOU=N2SOU=NSOUT=6",
                "NFI=NLONG=K=KPN=NUNKNO=14",
                "NLONG=NFI=NREG_TRACK+NSOU",
            ],
            "matalb_storage":
                "MATALB_TRK(-NSOUT:NREG), exact length NREG+NSOUT+1; "
                "read the payload in index order JJ=-NSOUT..NREG",
            "failure":
                "FAIL-CLOSED-BEFORE-MATALB-PAYLOAD-OR-TRANSPORT",
        },
        "regular tracking header and MATALB extent admission",
    )
    require(
        mccgf["mcgsig_record_admission"]
        == {
            "position":
                "Before checked MCGSIG reuse or any LCMGET of the listed "
                "payload.",
            "IPTRK/ICODE": "length 6, GANLIB type 1",
            "IPTRK/ALBEDO": "length 6, GANLIB type 2",
            "KPSYS_TAIL(II)/DRAGON-TXSC":
                "for every II, length NBMIX+1, GANLIB type 2",
            "KPSYS_TAIL(II)/ALBEDO":
                "if NALBP>0, for every II exact length NALBP and GANLIB "
                "type 2; if NALBP=0 the record is absent for every II",
            "mismatch_action":
                "FAIL-CLOSED-BEFORE-MCGSIG-OR-PAYLOAD-READ",
        },
        "MCGSIG exact record preflight",
    )
    require(
        mccgf["incomplete_bundle_action"] == "FAIL-CLOSED-BEFORE-MCGFLX64",
        "incomplete SC action",
    )

    mcgflx = find_owner(data, "MCGFLX64")
    source64 = find_owned(mcgflx, "SOURCE64")
    require(
        source64
        == {
            "name": "SOURCE64",
            "declaration":
                "real(real64), allocatable :: SOURCE64(:,:)",
            "allocation_shape": "(KPN,NGEFF)",
            "initialization":
                "Assign the whole allocation +0.0_real64 exactly once "
                "immediately after allocation and before any MCGFCS64 "
                "call.",
            "preserved_initial_bits":
                "Every inactive-group or unrepresented element retains "
                "the initialized positive-zero bit pattern until and "
                "unless an admitted active represented formula "
                "overwrites it.",
            "lifetime": "one MCGFLX64 call",
        },
        "MCGFLX64 SOURCE64 defined zero-once owner",
    )
    response64 = find_owned(mcgflx, "RESPONSE64")
    require(
        response64
        == {
            "name": "RESPONSE64",
            "declaration":
                "real(real64), allocatable :: RESPONSE64(:,:)",
            "allocation_shape": "(KPN,NGEFF)",
            "initialization":
                "At the start of every MCGFL164 response call, assign "
                "the whole RESPONSE64 view +0.0_real64 exactly once "
                "before MCGFCF or MCGFST.",
            "preserved_initial_bits":
                "Inactive-group and unrepresented response elements "
                "retain the defined positive-zero bit pattern; only the "
                "admitted single transport/STIS response may overwrite "
                "active represented elements.",
            "lifetime": "one MCGFLX64 call",
        },
        "MCGFLX64 RESPONSE64 per-response defined zero owner",
    )
    require(
        mcgflx["real_response_to_real32_conversion_allowed"] is False,
        "MCGFLX REAL32 return",
    )
    require(
        mcgflx["diagnostic_contract"]
        == "When IPRINT>5, call PRINDM directly on each REAL64 "
           "PHIIN_TAIL64/FIMEM group view; PRINAM and REAL32 staging are "
           "forbidden on the ON arm.",
        "MCGFLX64 REAL64 print kernel",
    )

    gmres = find_owner(data, "MCGMRE64")
    require(gmres["control_arithmetic_kind"] == "real64",
            "GMRES control kind")
    require(
        gmres["forbidden_conversions"]
        == [
            "RHS64=REAL(FLOUT,real32)",
            "GAR64=REAL(V,real32)",
            "PHIIN_TAIL64=PHIIN_TAIL64+REAL(G*V,real32)",
            "REAL64 norm assigned to a REAL32 decision variable",
        ],
        "GMRES round-trip prohibition",
    )
    require(
        gmres["inherited_controls"]
        == {
            "nstart": 10,
            "maxi": 20,
            "maxit": 19,
            "errtol_epsi_binary32_bits": "0x3727c5ac",
            "errtol_epsi_stored_decimal": "9.99999974737875164e-6",
            "fac_value": 100,
            "epsinto_chain": "ERRTOL64=exact-promotion(EPSI32); "
                             "MCGMRE_FAC64=100.0_real64; "
                             "EPSINTO64=ERRTOL64/MCGMRE_FAC64",
            "maxint_value": 200,
            "change_or_tuning": "FORBIDDEN",
        },
        "GMRES inherited controls",
    )

    response = find_owner(data, "MCGFL164")
    require(
        response["borrows"]
        == [
            "QFR_TAIL64 and PHIIN_TAIL64",
            "SC_BY_GROUP32 and SIGAL32",
            "SOURCE64 and RESPONSE64",
            "KPSYS_TAIL pointees",
            "KEYFLX_TRK3 as an immutable checked tracking-index view",
            "BC_INDEX_TRK1(NLONG-NREG) from IPTRK BC-REFL+TRAN",
            "IFTRAK at the admitted response position",
            "MATALB_TRK(-NSOUT:NREG)",
            "CAZ1_TRACK64(NANGL) and CAZ2_TRACK64(NANGL)",
            "CPO32(NMU), ZMU32(NMU) and WZMU32(NMU)",
            "Frozen remaining geometry and tracking views",
        ],
        "MCGFL164 exact borrowed-object set",
    )
    require(
        response["ordered_operations"]
        == [
            "MCGFCS64 for every active NCONV group using "
            "rank-2 SC_BY_GROUP32(:,:,II)",
            "MOCIK3 discrete sign construction",
            "Exactly one MCGFCF traversal using "
            "MCGFFIR64_RANK_ADAPTER, legacy MCGFFIR and MCGSCA",
            "MCGFFIR64_RANK_ADAPTER passes KEYFLX_TRK3(:,:,1) as a "
            "direct contiguous rank-2 actual to checked legacy MCGFFIR",
            "One local checked rank-2 mapping of PJJIND$MCCG immediately "
            "before MCGFST",
            "After NLIN=1 and exact-shape checks, pass the contiguous "
            "rank-2 section KEYFLX_TRK3(:,1,:) to MCGFST and MCGFCA64",
            "Exactly one MCGFST correction",
            "Exactly one SPOMOC_CAPTURE64 call at the legacy capture point "
            "using four REAL64 arrays",
            "One-group ACA64 operation under the unchanged IAAC control",
        ],
        "response sequence",
    )
    inactive_tracking = find_owned(
        response,
        "legal_inactive_regular_tracking_storage",
    )
    require(
        inactive_tracking
        == {
            "name": "legal_inactive_regular_tracking_storage",
            "guard": "NDIM=2, LPRISM=false and IDIR=0",
            "members": [
                {
                    "name": "CAZ0_INACTIVE64",
                    "declaration":
                        "real(real64), allocatable :: "
                        "CAZ0_INACTIVE64(:)",
                    "allocation_shape": "(NANGL)",
                    "canonical_value": "+0.0_real64",
                    "live_reads_allowed": False,
                    "reason":
                        "The locked NDIM=2 MCGFCF branch does not read "
                        "CAZ0.",
                },
                {
                    "name": "XSI_INACTIVE64",
                    "declaration":
                        "real(real64), allocatable :: "
                        "XSI_INACTIVE64(:)",
                    "allocation_shape": "(NSOUT)",
                    "canonical_value": "+0.0_real64",
                    "live_reads_allowed": False,
                    "reason":
                        "MCGFFIR reads XSI only when IDIR>0; the locked "
                        "route has IDIR=0.",
                    "actual":
                        "Pass this valid rank-1 array to MCGFCF; never "
                        "form XSIXYZ(:,0) or another out-of-bounds column.",
                },
            ],
            "active_cpo_rule":
                "Pass the exact stored CPO32(NMU) values from XMU$MCCG; "
                "CPO is not replaced by canonical inactive storage.",
            "interpretation":
                "The two canonical arrays are defined conforming storage "
                "for observationally unread formals, not fitted physical "
                "values.",
        },
        "regular tracking inactive formal storage",
    )
    pjjind = find_owned(response, "PJJIND_TRK2")
    require(
        pjjind
        == {
            "name": "PJJIND_TRK2",
            "declaration":
                "integer, contiguous, pointer :: PJJIND_TRK2(:,:)",
            "mapping":
                "After exact length 2*NPJJM and integer-type checks, map "
                "IPTRK/PJJIND$MCCG directly as (NPJJM,2).",
            "access":
                "read-only and passed only to the single MCGFST call",
            "lifetime":
                "local descriptor from mapping through that MCGFST return",
        },
        "local rank-2 PJJIND mapping",
    )
    bc_index = find_owned(response, "BC_INDEX_TRK1")
    require(
        bc_index
        == {
            "name": "BC_INDEX_TRK1",
            "declaration":
                "integer, contiguous, pointer :: BC_INDEX_TRK1(:)",
            "mapping":
                "After exact length NLONG-NREG and GANLIB integer-type "
                "checks, map IPTRK/BC-REFL+TRAN directly as "
                "(NLONG-NREG).",
            "access":
                "read-only boundary-condition indexes for MCGFCS64",
            "lifetime": "one MCGFL164 call",
        },
        "BC-REFL+TRAN exact mapping",
    )
    require(
        response["audit_capture_contract"]
        == {
            "callee": "SPOMOC_CAPTURE64",
            "inputs": [
                "QFR_TAIL64",
                "PHIIN_TAIL64",
                "SOURCE64",
                "RESPONSE64",
            ],
            "input_kind": "real64",
            "semantics":
                "Preserve the existing SPOMOC_ACTIVE, context, role, "
                "iteration, group, NCONV and finite checks; write "
                "SPOT-M-QFR/EVAL/SRC/RAW as GANLIB type 4 directly from "
                "REAL64 inputs.",
            "qfr_or_eval_real32_staging_allowed": False,
            "legacy_spomoc_capture_allowed_on_arm": False,
            "classification":
                "validation audit output, not terminal SPOT-R64 authority "
                "or the type-2 compatibility mirror",
            "solver_state_or_control_may_change": False,
        },
        "SPOMOC_CAPTURE64 direct REAL64 audit contract",
    )
    require(
        response["callback_selection"]
        == {
            "selected_symbol": "MCGFFIR64_RANK_ADAPTER",
            "selection_basis":
                "The locked ISCH=11, NLF=NLIN=NFUNL=1 route.",
            "binding":
                "MCGFL164 names the global external adapter directly "
                "when calling legacy MCGFCF; the adapter is not passed "
                "through MCCGF64, MCGFLX64 or MCGMRE64.",
            "legacy_mcgffi_template_reused": False,
            "rank2_procedure_pointer_may_target_rank3_adapter": False,
            "subsch":
                "MCGSCA remains the fixed legacy EXTERNAL forwarded "
                "unchanged.",
        },
        "rank-adapter selection without legacy procedure-pointer mismatch",
    )
    require(
        response["stis_record_admission"]
        == {
            "guard": "STIS=1 and IDIR=0",
            "record": "PJJ$MCCG",
            "owner": "each active KPSYS_TAIL(II)",
            "required_length": "NREG*NPJJM",
            "required_ganlib_type": 2,
            "position":
                "Before the single MCGFST call and before any PJJ "
                "payload read.",
            "inactive_group_payload_read": False,
            "mismatch_action": "FAIL-CLOSED-BEFORE-MCGFST",
        },
        "active PJJ$MCCG exact record admission",
    )
    require(
        response["discrete_index_value_admission"]
        == {
            "position":
                "After exact record type/extent checks and before source "
                "construction or transport.",
            "PJJIND_TRK2":
                "With NPJJM=NFUNL=1, require "
                "PJJIND_TRK2(1,1:2)=[1,1].",
            "BC_INDEX_TRK1":
                "Every entry lies in 1..NLONG-NREG.",
            "KEYCUR_TRK1":
                "Every entry lies in 1..KPN and no value is duplicated.",
            "KEYFLX_TRK3":
                "Every KEYFLX_TRK3(:,:,1) entry lies in 1..KPN and no "
                "value is duplicated.",
            "combined_key_layout":
                "KEYFLX_TRK3(:,:,1) and KEYCUR_TRK1 together are an "
                "exact permutation of 1..KPN.",
            "NZON_TRK1_regions":
                "NZON_TRK1(1:NREG) lies in 0..NBMIX.",
            "NZON_TRK1_surface_tail":
                "Every NZON_TRK1(NREG+1:NLONG) entry lies in -6..-1.",
            "V_TRACK32":
                "Every entry is finite and strictly positive.",
            "ICODE_and_albedo":
                "Every ICODE entry is nonnegative; every positive entry "
                "is at most NALBP, and all tracking/group ALBEDO values "
                "are finite.",
            "cross_sections":
                "Every gathered DRAGON-S0XSC and checked DRAGON-TXSC "
                "value is finite.",
            "mismatch_action":
                "FAIL-CLOSED-BEFORE-SOURCE-OR-TRANSPORT",
        },
        "frozen tracking/index value admission",
    )
    require(
        response["derived_locked_flags"]
        == {
            "last": False,
            "macflg": False,
            "combflg": False,
            "rebflg_passed_to_mcgfca64": False,
        },
        "KRYL-derived legacy branch",
    )
    require(
        response["forbidden"]
        == [
            "LCM gathering of SC",
            "Second tracking traversal",
            "Second MCGFST application",
            "Rank-3 or flat KEYFLX sequence association into rank-2 "
            "MCGFFIR",
            "Assigning the rank-3 adapter to legacy rank-2 "
            "MCGFFI_TEMPLATE",
            "XSIXYZ(:,0) or another out-of-bounds XSI actual",
            "Fallback to the legacy response after ON selection",
            "REAL32 mutable QFR, PHIIN, SOURCE or RESPONSE",
        ],
        "MCGFL164 rank/XSI and response prohibitions",
    )

    source = find_owner(data, "MCGFCS64")
    require(source["role"] == "REAL64-SOURCE-CONSTRUCTION-BORROWER",
            "MCGFCS64 role")
    require(
        source["borrows"]
        == [
            "QFR_TAIL64(:,II) as read-only QN64",
            "PHIIN_TAIL64(:,II) as read-only FI64",
            "Rank-2 SC_BY_GROUP32(:,:,II) as read-only SC32",
            "SIGAL32(:,II) as read-only operator data",
        ],
        "source borrower identities",
    )
    require(
        source["writes"]
        == [
            "Only represented indices in the admitted active-group slice "
            "of MCGFLX64-owned SOURCE64, after complete layout validation"
        ],
        "source write owner",
    )
    require(
        source["arithmetic_contract"]
        == "For each represented volume unknown evaluate "
           "S=QN64+exactly-promoted(SC32)*FI64 in real64. For each "
           "represented boundary-current unknown evaluate "
           "S=exactly-promoted(SIGAL32)*FI64 in real64. The volume and "
           "boundary branches are mutually exclusive; there is no "
           "three-term sum.",
        "source mutually exclusive arithmetic",
    )
    require(
        source["inactive_group_contract"]
        == "Do not write the source slice for NCONV(II)=false.",
        "inactive source contract",
    )
    require(
        source["untouched_storage_contract"]
        == "SOURCE64 is read-write/inout; every unrepresented or untouched "
           "element retains its incoming bit pattern.",
        "source inout bit preservation",
    )
    require(
        source["forbidden"]
        == [
            "Compute QN+SC*FI in REAL32 before assignment to SOURCE64",
            "Add a SIGAL boundary term to a volume-cell source or add "
            "QN/SC terms to a boundary-current source",
            "Modify QN64, FI64, SC32 or SIGAL32",
            "Gather SC from LCM",
        ],
        "source construction prohibitions",
    )

    aca = find_owner(data, "ACA64")
    require(
        "integer(int64) per-call cutoff-active delta accumulation"
        in aca["owns"],
        "ACA cutoff delta kind and ownership",
    )
    require(
        aca["members"]
        == ["MCGFCA64", "MCGFCR64", "MCGABG64", "MCGPRA64"]
        and aca["reuses"] == ["MSRLUS1"],
        "ACA suffixed MCGPRA64 route",
    )
    require(
        aca["control_chain"]
        == "Receive EPSACA64 unchanged from MCGMRE64 EPSINTO64 through "
           "MCGFL164 EPSACC64, pass it unchanged as MCGABG64 EPSM64, "
           "retain FLXN64 from the REAL64 response norm, and pass FLXN64 "
           "unchanged as MCGABG64 FAC64; neither control chain returns "
           "to REAL32.",
        "ACA REAL64 control chain",
    )
    require(
        aca["mcgfcr_locked_macflg_false_interface"]
        == "Because MACFLG=false, use a checked MCGFCR64 interface for "
           "the no-macrolib-cross-group branch that omits NJJ, IJJ, "
           "IPOS and XSCAT; never pass unallocated allocatables as "
           "allegedly unread actual arguments."
        and aca["forbidden_abi_shortcuts"]
        == [
            "Passing unallocated NJJ, IJJ, IPOS or XSCAT actual "
            "arguments to an explicit MCGFCR64 interface",
            "Passing one-element DUMMY storage to explicit-shape "
            "LUCF(LC) or DIAGF(N1) formals on the PACA=4 route",
            "Mapping the active CF$MCCG record as CF32(N1) instead of "
            "CF32(LC)",
            "Passing DIAGF_INACTIVE32 to MCGABG64 or to an MCGPRA64 "
            "call inside MCGABG64",
            "Using SAVE IDUMMY for inactive IM0 or MCU0 instead of local "
            "defined storage",
            "Calling legacy MCGPRA from the ON arm with an explicit "
            "interface that preserves its undersized IM(NLONG) "
            "declaration",
            "Adding inactive placeholder operator data to the locked "
            "residual arithmetic",
        ],
        "MCGFCR64 locked explicit-interface safety",
    )
    require(
        aca["legal_inactive_paca4_integer_storage"]
        == {
            "guard": "PACA=4 and LC0=0",
            "members": [
                {
                    "name": "IM0_INACTIVE",
                    "declaration":
                        "integer, target :: IM0_INACTIVE(1)",
                    "canonical_value": 0,
                    "live_reads_allowed": False,
                },
                {
                    "name": "MCU0_INACTIVE",
                    "declaration":
                        "integer, target :: MCU0_INACTIVE(1)",
                    "canonical_value": 0,
                    "live_reads_allowed": False,
                },
            ],
            "why_one_element_is_conforming":
                "MCGPRA64 and MCGABG64 retain the legacy assumed-size "
                "IM0(*) and MCU0(*) formals, and LC0=0 makes them "
                "inactive.",
            "record_mapping_allowed": False,
            "save_common_or_module_state_allowed": False,
        },
        "PACA=4 inactive integer formal storage",
    )
    require(
        aca["legal_inactive_paca4_storage"]
        == {
            "guard": "PACA=4 before allocation and association",
            "storage_kind": "real32",
            "lifetime": "one ACA64 call",
            "members": [
                {
                    "name": "LUCF_INACTIVE32",
                    "declaration":
                        "real(real32), allocatable :: "
                        "LUCF_INACTIVE32(:)",
                    "allocation_shape": "(LC)",
                    "canonical_value": "+0.0_real32",
                    "live_reads_allowed": False,
                    "passed_to": [
                        "direct pre-MCGABG MCGPRA64",
                        "MCGABG64",
                    ],
                },
                {
                    "name": "DIAGF_INACTIVE32",
                    "declaration":
                        "real(real32), allocatable :: "
                        "DIAGF_INACTIVE32(:)",
                    "allocation_shape": "(N1)",
                    "canonical_value": "+0.0_real32",
                    "live_reads_allowed": False,
                    "passed_to": [
                        "direct pre-MCGABG MCGPRA64 only",
                    ],
                },
            ],
            "use":
                "LUCF_INACTIVE32 supplies the inactive ILUCF formal to "
                "the direct pre-MCGABG MCGPRA64 call and to MCGABG64. "
                "DIAGF_INACTIVE32 supplies only the inactive DIAGF formal "
                "of the direct pre-MCGABG MCGPRA64 call. MCGABG64 and "
                "every MCGPRA64 call inside it receive active "
                "DIAGF32(N1). These canonical values are not operator "
                "coefficients and may not enter arithmetic.",
        },
        "PACA=4 conforming inactive formal storage",
    )
    require(
        aca["active_paca4_operator_views"]
        == {
            "guard": "PACA=4",
            "admission_order":
                "For every record, call LCMLEN and require the exact "
                "length and GANLIB type before LCMGPD and C_F_POINTER; "
                "fail closed on any mismatch.",
            "records": {
                "IM$MCCG": {
                    "owner": "IPTRK",
                    "ganlib_type": 1,
                    "length": "N1+1",
                    "view":
                        "integer, contiguous, rank 1 :: IM(N1+1)",
                },
                "MCU$MCCG": {
                    "owner": "IPTRK",
                    "ganlib_type": 1,
                    "length": "LC",
                    "view":
                        "integer, contiguous, rank 1 :: MCU(LC)",
                },
                "PI$MCCG": {
                    "owner": "IPTRK",
                    "ganlib_type": 1,
                    "length": "N1",
                    "view":
                        "integer, contiguous, rank 1 :: IPERM(N1)",
                },
                "JU$MCCG": {
                    "owner": "IPTRK",
                    "ganlib_type": 1,
                    "length": "N1",
                    "view":
                        "integer, contiguous, rank 1 :: JU(N1)",
                },
                "DIAGQ$MCCG": {
                    "owner": "KPSYS_TAIL(II)",
                    "ganlib_type": 2,
                    "length": "N1",
                    "view":
                        "real(real32), contiguous, rank 1 :: "
                        "DIAGQ32(N1)",
                },
                "CQ$MCCG": {
                    "owner": "KPSYS_TAIL(II)",
                    "ganlib_type": 2,
                    "length": "LC",
                    "view":
                        "real(real32), contiguous, rank 1 :: CQ32(LC)",
                },
                "ILUDF$MCCG": {
                    "owner": "KPSYS_TAIL(II)",
                    "ganlib_type": 2,
                    "length": "N1",
                    "view":
                        "real(real32), contiguous, rank 1 :: "
                        "ILUDF32(N1)",
                },
                "CF$MCCG": {
                    "owner": "KPSYS_TAIL(II)",
                    "ganlib_type": 2,
                    "length": "LC",
                    "view":
                        "real(real32), contiguous, rank 1 :: CF32(LC)",
                },
                "DIAGF$MCCG": {
                    "owner": "KPSYS_TAIL(II)",
                    "ganlib_type": 2,
                    "length": "N1",
                    "view":
                        "real(real32), contiguous, rank 1 :: "
                        "DIAGF32(N1)",
                    "active_use":
                        "MCGABG64 and its internal MCGPRA64 calls; never "
                        "substitute DIAGF_INACTIVE32",
                },
            },
            "all_views":
                "read-only operator/index data at the frozen stored kind",
            "n1_identity":
                "N1=NLONG on the locked one-group ACA route",
            "inactive_paca4_records": [
                "IM0$MCCG",
                "MCU0$MCCG",
                "ILUCF$MCCG",
            ],
            "inactive_records_may_be_read_or_mapped": False,
            "legacy_unchecked_mapping_allowed": False,
        },
        "PACA=4 exact active-record contract",
    )
    require(
        aca["mcgpra64_shape_correction"]
        == {
            "reason":
                "Legacy MCGPRA declares IM(NLONG) but evaluates IM(I+1) "
                "through I=NLONG; the actual producer and MSRLUS1 both "
                "require NLONG+1 entries.",
            "replacement":
                "A suffixed MCGPRA64 preserves the locked matrix-vector "
                "and PACA=4 arithmetic and changes only the checked IM "
                "dummy extent to IM(NLONG+1).",
            "im_dummy":
                "integer, contiguous, intent(in) :: IM(NLONG+1)",
            "cf_dummy":
                "real(real32), contiguous, intent(in) :: CF32(LC)",
            "mutable_vectors": "real(real64)",
            "operator_arrays": "real(real32)",
            "calls": "MSRLUS1 with conforming IM(NLONG+1) and CF32(LC)",
            "legacy_mcgpra_allowed_on_arm": False,
            "arithmetic_or_iteration_order_changed": False,
        },
        "MCGPRA64 IM extent correction without arithmetic change",
    )
    cutoff = aca["inherited_cutoff"]
    require(
        cutoff["source"] == "MCGABG EPSMAX=1E-7"
        and cutoff["binary32_bits"] == "0x33d6bf95"
        and cutoff["binary32_exact_decimal"] == "1.0000000116860974e-7"
        and cutoff["change_or_tuning"] == "FORBIDDEN"
        and cutoff["counterfactual_value"] == 0
        and cutoff["counterfactual_may_modify_production_state"] is False
        and cutoff["counterfactual_may_modify_terminal_decision"] is False
        and cutoff["counterfactual_may_modify_publication"] is False,
        "inherited ACA cutoff",
    )
    require(
        cutoff["live_guard_inventory"]
        == [
            "RHSN < EPSINF",
            "CN > EPSMAX*ASIN2",
            "first FNORM < EPS2",
            "final FNORM < EPS2",
        ]
        and cutoff["guard_count"] == 4
        and cutoff["epsm_convergence_comparison_is_cutoff_counterfactual"]
        is False,
        "four live cutoff guards",
    )
    require(
        cutoff["counterfactual_rule"]
        == "For each live guard, evaluate the same finite operands with "
           "EPSMAX=0 and increment cutoff_active exactly when the Boolean "
           "result differs; never select a production branch from the "
           "counterfactual.",
        "cutoff counterfactual isolation",
    )
    require(
        cutoff["cutoff_active_nonzero_classification"]
        == "INCONCLUSIVE-INHERITED-CUTOFF",
        "cutoff classification",
    )

    flubal = find_owner(data, "FLUBAL64")
    require(
        flubal["borrows"]
        == [
            "FLU2DR64 new-inner flux slice in-place",
            "KEYFLX(:,1,1), MATALB(NNN+1:NNN+ICREB) and "
            "V(NNN+1:NNN+ICREB) direct sections",
            "The complete immutable OFFGROUP32 bundle through exact "
            "read-only NJJ_OFF(NMAT,NGRP), IJJ_OFF(NMAT,NGRP), "
            "IPOS_OFF(NMAT,NGRP), NSCAT_OFF(NGRP) and "
            "SCAT_OFF32(NMAT*NGRP,NGRP) dummies",
            "Frozen physical cross sections, materials, volumes and "
            "geometry at stored kinds",
        ]
        and
        flubal["forbidden"]
        == [
            "REAL(XCSOU64) downcast",
            "REAL32 matrix solve",
            "REAL32 flux update",
            "LCMGET or LCMGPD of NJJS00, IJJS00, IPOS00 or SCAT00 "
            "after OFFGROUP32 admission",
            "Element-actual sequence association for KEYFLX, MATALB, "
            "SURFAC or mutable flux",
        ],
        "rebalancing REAL64 closure and direct sections",
    )
    flu2ac = find_owner(data, "FLU2AC64")
    require(
        flu2ac["borrows"]
        == [
            "FLUX64(:,:,5:7) with AKEEP64(5:7) for inner acceleration",
            "FLUX64(:,:,1:3) with AKEEP64(1:3) for outer acceleration",
        ]
        and
        flu2ac["forbidden"]
        == [
            "REAL(DMU) downcast",
            "REAL32 AKEEP",
            "REAL32 flux update",
            "Element-actual sequence association for either flux or "
            "AKEEP history",
        ],
        "acceleration REAL64 closure and direct sections",
    )

    terminal_owner = find_owner(data, "FLU2DR64 terminal boundary")
    require(
        terminal_owner["authoritative_records"]["ganlib_value_type"] == 4,
        "type-4 authority",
    )
    require(
        terminal_owner["compatibility_records"]["ganlib_value_type"] == 2
        and terminal_owner["compatibility_records"]["mirror_passes"] == 1
        and terminal_owner["compatibility_records"][
            "read_back_by_real64_lane"
        ] is False,
        "single terminal type-2 mirror",
    )
    require(terminal_owner["failed_on_visit_publication"] == "NONE",
            "failed publication")

    aggregation = data["cutoff_counterfactual_aggregation"]
    require(
        aggregation
        == {
            "visit_owner": "FLU2DR64",
            "visit_counter": "CUTOFF_ACTIVE_VISIT64",
            "kind": "integer(int64)",
            "entry_initialization":
                "CUTOFF_ACTIVE_VISIT64=0_int64 exactly once before any "
                "inner call",
            "leaf_contract":
                "Each MCGABG64 call initializes "
                "CUTOFF_ACTIVE_CALL64=0_int64, increments it by exactly "
                "1_int64 for every live guard evaluation whose production "
                "and EPSMAX=0 Boolean outcomes differ, and returns that "
                "nonnegative delta on normal completion.",
            "propagation_chain": [
                "MCGABG64 -> MCGFCA64",
                "MCGFCA64 -> MCGFL164",
                "MCGFL164 -> MCGMRE64",
                "MCGMRE64 -> MCGFLX64",
                "MCGFLX64 -> MCCGF64",
                "MCCGF64 -> DOORFV64",
                "DOORFV64 -> FLU2DR64",
            ],
            "aggregation_rule":
                "Every caller initializes its local int64 delta to zero, "
                "sums each normally returned child delta exactly once in "
                "existing call order, and returns the sum; FLU2DR64 adds "
                "every normally returned DOORFV64 delta exactly once to "
                "CUTOFF_ACTIVE_VISIT64.",
            "reset_below_visit_owner": False,
            "overwrite_instead_of_add": False,
            "save_common_or_module_singleton_allowed": False,
            "shared_mutable_leaf_counter_allowed": False,
            "may_change_live_branch_state_terminal_or_publication": False,
            "later_feasibility_classification":
                "CUTOFF_ACTIVE_VISIT64=0 permits this diagnostic dimension "
                "to pass; CUTOFF_ACTIVE_VISIT64>0 gives "
                "INCONCLUSIVE-INHERITED-CUTOFF without changing the "
                "accepted production result.",
            "bound_derivation":
                "MAXOUT(500) times MAXINR(740) times NGEFF(370) times at "
                "most 20 MCGFL164 calls per MCGMRE64 times at most 203 "
                "counted live-guard evaluations per MCGABG64 call",
            "frozen_cap_conservative_upper_bound": 555814000000,
            "int64_capacity_is_sufficient_for_frozen_caps": True,
        },
        "cutoff counterfactual visit aggregation",
    )

    require(
        [entry["routine"] for entry in data["abi_requirements"]]
        == EXPECTED_ABI_ORDER,
        "ABI scope or order",
    )
    for entry in data["abi_requirements"]:
        expected_interface = (
            "legacy-ABI-compatible external bridge with checked internal "
            "MCGFFIR interface"
            if entry["routine"] == "MCGFFIR64_RANK_ADAPTER"
            else "explicit checked interface"
        )
        require(
            entry["interface"] == expected_interface,
            f"checked interface: {entry['routine']}",
        )
    require(
        find_abi(data, "FLU2DR64")["terminal_diagnostic_view"]
        == "FL_PRINT64 is real(real64), shape (NREG); no REAL32 FL "
           "capture and no RKEFF downcast for ITYPEC=0",
        "FLU2DR64 terminal diagnostic ABI",
    )
    require(
        find_abi(data, "FLU2DR64")["dead_fission_actuals"]
        == "The branch-specific FLU2DR64 interface omits XSCHI and "
           "XSNUF. FLUDRV validates every NUSIGF payload as finite "
           "numerical zero through per-group REAL32 staging, does not "
           "read or allocate CHI, and passes neither dead array to the "
           "ON arm.",
        "FLU2DR64 omitted dead fission actuals",
    )
    require(
        find_abi(data, "FLU2DR64")["owned_offgroup_storage"]
        == "integer :: NJJ_OFF(NMAT,NGRP), IJJ_OFF(NMAT,NGRP), "
           "IPOS_OFF(NMAT,NGRP), NSCAT_OFF(NGRP); real(real32) :: "
           "SCAT_OFF32(NMAT*NGRP,NGRP)",
        "FLU2DR64 exact owned OFFGROUP32 storage",
    )
    require(
        find_abi(data, "DOORFV64")["keyflx_base"]
        == "integer, contiguous, rank 1, shape (NREG), passed as "
           "KEYFLX(:,1,1) only after NLIN=NFUNL=1",
        "DOORFV64 rank-1 KEYFLX base ABI",
    )
    require(
        find_abi(data, "DOORFV64")["diagnostic_region_view"]
        == "FGAR64 is real(real64), shape (NREG); full unknown output "
           "reads PHIIN_TAIL64 directly",
        "DOORFV64 diagnostic REAL64 ABI",
    )
    require(
        find_abi(data, "MCCGF64")
        == {
            "routine": "MCCGF64",
            "qfr_and_phiin": "real(real64), contiguous",
            "epsi_reps_and_eps":
                "frozen EPSI binary32 value exactly promoted to real64; "
                "REPS and EPS real(real64)",
            "diagnostic_temp":
                "TEMP64=EPS64(II); warning comparison with EPSI64 and "
                "printing remain real(real64)",
            "sc_bundle":
                "real(real32), contiguous, rank 3, lower bound 0 on "
                "dimension 1",
            "keyflx_base":
                "integer, contiguous, rank 1, shape (NREG)",
            "tracking_keyflx":
                "integer, contiguous, rank 3, shape "
                "(NREG,NLIN,NFUNL)",
            "interface": "explicit checked interface",
        },
        "MCCGF64 state/control/SC ABI",
    )
    require(
        find_abi(data, "MCGFLX64")["tracking_keyflx"]
        == "integer, contiguous, rank 3, shape (NREG,NLIN,NFUNL)"
        and find_abi(data, "MCGFLX64")["iprint_gt5_diagnostic"]
        == "PRINDM receives the REAL64 FIMEM group view directly; PRINAM "
           "is forbidden"
        and find_abi(data, "MCGMRE64")["tracking_keyflx"]
        == "integer, contiguous, rank 3, shape (NREG,NLIN,NFUNL)",
        "inner rank-3 tracking KEYFLX ABI",
    )
    response_abi = find_abi(data, "MCGFL164")
    require(
        response_abi["tracking_keyflx_in"]
        == "integer, contiguous, rank 3, shape (NREG,1,NFUNL)"
        and response_abi["tracking_keyflx_rank2_section"]
        == "KEYFLX_TRK3(:,1,:) after exact guard; pass contiguous rank 2 "
           "to MCGFST and MCGFCA64"
        and response_abi["mcgfcf_callback_rank_adapter"]
        == "MCGFFIR64_RANK_ADAPTER accepts the exact frozen rank-3 "
           "callback actual and passes KEYFLX_TRK3(:,:,1) as a "
           "contiguous rank-2 actual to checked legacy MCGFFIR"
        and response_abi["pjjind_local_mapping"]
        == "No upstream PJJIND dummy; require exact integer length "
           "2*NPJJM and map IPTRK/PJJIND$MCCG directly as local rank-2 "
           "PJJIND_TRK2(NPJJM,2), consumed only by MCGFST",
        "MCGFL164 KEYFLX section and local PJJIND mapping ABI",
    )
    require(
        response_abi["regular_tracking_formals"]
        == "MATALB_TRK(-NSOUT:NREG), CAZ1_TRACK64(NANGL), "
           "CAZ2_TRACK64(NANGL), stored CPO32(NMU), ZMU32(NMU), "
           "WZMU32(NMU), V_TRACK32(NLONG), NZON_TRK1(NLONG), "
           "KEYCUR_TRK1(NLONG-NREG), BC_INDEX_TRK1(NLONG-NREG), "
           "CAZ0_INACTIVE64(NANGL) and XSI_INACTIVE64(NSOUT)"
        and response_abi["stis_pjj_record"]
        == "For each active group, PJJ$MCCG has exact length "
           "NREG*NPJJM and GANLIB type 2 before MCGFST",
        "MCGFL164 regular tracking formals ABI",
    )
    require(
        response_abi["audit_capture"]
        == "SPOMOC_CAPTURE64 receives QFR, EVAL, SOURCE and RAW as "
           "real(real64), contiguous rank-2 arrays and writes type-4 "
           "payloads without staging",
        "MCGFL164 SPOMOC_CAPTURE64 ABI",
    )
    require(
        find_abi(data, "MCGFFIR64_RANK_ADAPTER")
        == {
            "routine": "MCGFFIR64_RANK_ADAPTER",
            "purpose":
                "Zero-arithmetic callback ABI adapter for legacy MCGFCF "
                "on the frozen NLIN=NFUNL=1 route.",
            "keyflx_callback_dummy":
                "integer :: KEYFLX_TRK3(NREG,1,1)",
            "keyflx_to_mcgffir":
                "Pass direct contiguous section KEYFLX_TRK3(:,:,1) to "
                "checked legacy MCGFFIR dummy KEYFLX(NREG,1).",
            "xsi":
                "real(real64), contiguous rank 1, exact shape (NSOUT); "
                "XSI_INACTIVE64 is valid storage and no column-zero "
                "expression is allowed.",
            "external_abi":
                "Global external subroutine with explicit-shape dummies "
                "only; all non-KEYFLX dummies exactly match legacy "
                "MCGFFIR type, kind, order and extent.",
            "subsch": "Legacy EXTERNAL forwarded unchanged.",
            "forbidden_features": [
                "assumed-shape or assumed-rank dummy",
                "OPTIONAL, POINTER or ALLOCATABLE dummy",
                "BIND(C) or module-procedure callback ABI",
                "SAVE, COMMON, module mutable state or I/O",
            ],
            "caller_guard":
                "MCGFL164 proves NLF=NLIN=NFUNL=1 before MCGFCF.",
            "numerical_changes": 0,
            "interface":
                "legacy-ABI-compatible external bridge with checked "
                "internal MCGFFIR interface",
        },
        "MCGFFIR external rank bridge ABI",
    )
    for routine in ("MCCGF64", "MCGFLX64", "MCGMRE64", "ACA64"):
        require(
            "pjjind" not in find_abi(data, routine),
            f"no upstream PJJIND ABI expansion: {routine}",
        )
    require(
        find_abi(data, "MCGFCS64")
        == {
            "routine": "MCGFCS64",
            "qn_fi_and_s": "real(real64), contiguous, rank 1",
            "sc": "real(real32), contiguous, shape (0:NBMIX,1)",
            "sigal": "real(real32), contiguous, shape (-6:NBMIX)",
            "access": "QN and FI read-only; SC and SIGAL read-only; S "
                      "read-write/inout with untouched elements bitwise "
                      "preserved",
            "arithmetic": "Volume: S=QN+promoted(SC)*FI in real64. "
                          "Boundary current: S=promoted(SIGAL)*FI in "
                          "real64. These branches are mutually exclusive.",
            "interface": "explicit checked interface",
        },
        "MCGFCS64 ABI",
    )
    require(
        find_abi(data, "ACA64")
        == {
            "routine": "ACA64",
            "old_state_response_corrections_and_norms": "real(real64)",
            "mcgfcr_fiold": "real(real64)",
            "mcgfcr_locked_macflg_false_interface":
                "omits inactive NJJ, IJJ, IPOS and XSCAT arguments because "
                "the macrolib cross-group branch is disabled",
            "mcgfca_phiin_and_epsaca":
                "real(real64), with EPSACA equal to the unchanged EPSINTO64 "
                "derived in REAL64 from the exactly promoted EPSI input",
            "mcgabg_epsm_and_fac":
                "real(real64), with FLXN64 passed unchanged as FAC64",
            "keyflx":
                "integer, contiguous, rank 2, shape (NREG,NFUNL)",
            "mcgpra64_im":
                "integer, contiguous, shape (NLONG+1)",
            "paca4_active_cf":
                "real(real32), contiguous, shape (LC), never (N1)",
            "paca4_active_record_views":
                "IM int(N1+1); MCU int(LC); IPERM int(N1); JU int(N1); "
                "DIAGQ32 real32(N1); CQ32 real32(LC); ILUDF32 "
                "real32(N1); CF32 real32(LC); DIAGF32 real32(N1), each "
                "rank 1 contiguous after exact LCMLEN type/extent "
                "admission",
            "paca4_inactive_formal_storage":
                "LUCF_INACTIVE32(LC) and DIAGF_INACTIVE32(N1) are "
                "conforming defined REAL32 storage guarded by PACA=4 and "
                "are never read",
            "paca4_inactive_integer_storage":
                "local defined IM0_INACTIVE(1) and MCU0_INACTIVE(1), used "
                "only with LC0=0 assumed-size inactive formals; no SAVE "
                "or record mapping",
            "stored_operator_inputs": "real(real32)",
            "interface": "explicit checked interface",
        },
        "ACA REAL64 mutable/control ABI",
    )
    require(
        find_abi(data, "FLUBAL64")
        == {
            "routine": "FLUBAL64",
            "mutable_state_matrix_rhs_solution_and_norms":
                "real(real64)",
            "direct_sections":
                "KEYFLX(:,1,1); MATALB(NNN+1:NNN+ICREB); "
                "V(NNN+1:NNN+ICREB); FLUX64(:,:,7); NJJ_OFF(:,:); "
                "IJJ_OFF(:,:); IPOS_OFF(:,:); NSCAT_OFF(:); "
                "SCAT_OFF32(:,:)",
            "offgroup_read_only_dummies":
                "integer, intent(in) :: NJJ_OFF(NMAT,NGRP), "
                "IJJ_OFF(NMAT,NGRP), IPOS_OFF(NMAT,NGRP), "
                "NSCAT_OFF(NGRP); real(real32), intent(in) :: "
                "SCAT_OFF32(NMAT*NGRP,NGRP)",
            "later_offgroup_lcm_reads_allowed": False,
            "interface": "explicit checked interface",
        },
        "FLUBAL64 direct-section ABI",
    )
    require(
        find_abi(data, "FLU2AC64")
        == {
            "routine": "FLU2AC64",
            "mutable_state_history_differences_and_acceleration":
                "real(real64)",
            "inner_direct_sections":
                "FLUX64(:,:,5:7) and AKEEP64(5:7)",
            "outer_direct_sections":
                "FLUX64(:,:,1:3) and AKEEP64(1:3)",
            "interface": "explicit checked interface",
        },
        "FLU2AC64 direct-section ABI",
    )
    require(
        find_abi(data, "SPOMOC_BEGIN64")
        == {
            "routine": "SPOMOC_BEGIN64",
            "purpose":
                "Default-off ON-arm audit admission only; it does not "
                "change solver controls.",
            "stored_tolerances":
                "EPSOUT, EPSUNK and EPSINR remain exact binary32 inputs "
                "and are checked bitwise.",
            "exact_route_controls":
                "MCCG, ITYPEC=0, ITPIJ=1, ITRANC=2, INSB=1, "
                "LEAKSW=false, NGRP=370, NUN=14, NREG=8, MAXOUT=500, "
                "MAXINR=740, INITFL=1, ACCE=(3,3), direct, ILEAK=0, "
                "LREBAL=true, associated frozen IPSOU and no IPFLUP",
            "off_behavior":
                "The OFF arm calls legacy SPOMOC_BEGIN unchanged.",
            "interface": "explicit checked interface",
        },
        "SPOMOC_BEGIN64 audit-only ABI",
    )
    require(
        find_abi(data, "SPOMOC_CAPTURE64")
        == {
            "routine": "SPOMOC_CAPTURE64",
            "qfr_eval_source_raw":
                "real(real64), contiguous, rank 2, exact shape "
                "(NUN,NGEFF)",
            "discrete_inputs":
                "NGEFF, NGIND, NUN and NCONV retain exact "
                "integer/logical kinds and shapes.",
            "writes":
                "Direct GANLIB type-4 SPOT-M-QFR/EVAL/SRC/RAW payloads "
                "after unchanged audit identity and finite checks.",
            "solver_feedback": False,
            "interface": "explicit checked interface",
        },
        "SPOMOC_CAPTURE64 type-4 no-feedback ABI",
    )

    promotion = data["entry_promotion"]
    require(
        promotion["owner"] == "FLU2DR64"
        and type(promotion["events"]) is int
        and promotion["events"] == 1
        and promotion["later_real32_state_ingress_allowed"] is False,
        "single entry promotion",
    )
    require(
        promotion["record_contracts"]
        == {
            "initial_flux_group_list": {
                "records": "One FLUX list element for each IG=1..NGRP on "
                           "the locked forward route",
                "container_length": "NGRP",
                "container_type": 10,
                "expected_length": "NUNKNO",
                "expected_type": 2,
                "staging": "REAL32(NUNKNO)",
                "destination": "FLUX64(:,IG,2)",
                "payload_values":
                    "Every stored initial FLUX value is finite before "
                    "elementwise promotion.",
            },
            "frozen_dsour_with_ipsou": {
                "association":
                    "IPSOU is required, has direct L_SOURCE signature and "
                    "is the sole admitted source object; the no-IPSOU "
                    "KPMACR/FIXE branch is excluded.",
                "source_state_vector":
                    "Exact length 40 and GANLIB type 1 with values "
                    "(NGRP,NUNKNO,1,0,...,0)=(370,14,1,0,...,0).",
                "source_tags":
                    "SPOT-FROZEN has length 1, GANLIB type 1 and value 1; "
                    "SPOT-KEFF has length 1, GANLIB type 2, is positive "
                    "finite and is bitwise identical to "
                    "MACRO0/SPOT-KEFF.",
                "macro_tags":
                    "MACRO0/SPOT-FROZEN has length 1, GANLIB type 1 and "
                    "value 1; MACRO0/SPOT-KEFF has length 1 and GANLIB "
                    "type 2.",
                "zero_nusigf":
                    "For every IG=1..NGRP, "
                    "MACRO0/GROUP(IG)/NUSIGF has exact length NMAT*NIFIS, "
                    "GANLIB type 2, and every payload element is finite "
                    "numerical zero; either signed-zero representation is "
                    "admitted.",
                "nbs": "IPSOU/NBS is absent with record length zero.",
                "qint":
                    "IPSOU/SPOT-QINT has exact length NGRP, GANLIB type 2 "
                    "and finite values as frozen-source provenance; it is "
                    "not substituted for the direct XCSOU64 scan.",
                "hierarchy":
                    "DSOUR is an outer list of length 1 and GANLIB type "
                    "10; element 1 is an inner list of length NGRP and "
                    "GANLIB type 10.",
                "records":
                    "One DSOUR(1,IG) element for each forward IG=1..NGRP",
                "expected_length": "NUNKNO",
                "expected_type": 2,
                "staging": "REAL32(NUNKNO)",
                "destination": "FIXED_SOURCE64(:,IG)",
                "payload_values":
                    "Every DSOUR value is finite and nonnegative; after "
                    "promotion the direct ordered XCSOU64(1) sum is "
                    "required to be strictly positive.",
            },
        },
        "entry record contracts",
    )
    require(
        promotion["read_rule"]
        == "Before any entry payload read, validate the containing list "
           "length or source metadata; then for every physical group "
           "require the selected element or record's exact length and "
           "GANLIB type 2, read into the explicit REAL32 staging array "
           "named by record_contracts, and promote elementwise once. No "
           "GANLIB type-2 reader receives a REAL64 destination."
        and promotion["fixed_source_reuse"]
        == "At each outer iteration copy FIXED_SOURCE64 into "
           "FLUX64(:,:,4); admitted zero NUSIGF makes the legacy fission "
           "contribution identically zero. Do not reread DSOUR and do not "
           "admit the FIXE branch.",
        "entry staging and fixed-source reuse",
    )
    require(
        promotion["funkno_uss_policy"]
        == "Every admitted FUNKNO$USS record must have length zero; "
           "DOORFV64 performs no FUNKNO$USS payload read.",
        "FUNKNO$USS later ingress",
    )

    terminal = data["terminal_boundary"]
    require(
        terminal["strict_existing_terminal_rule_unchanged"] is True
        and terminal["strict_boolean"]
        == "(EEXT < EPSOUT) AND (EINN < EPSUNK) AND "
           "(EINR_LAST < EPSINR) AND (IINR_STATE == 1) AND (IT >= 2)"
        and terminal["required_real64_scalars"]
        == [
            "GINN",
            "FINN",
            "EINN",
            "EINR_LAST",
            "EUNK_LAST",
            "EEXT",
            "ERRDEB1",
            "ZMU64",
        ]
        and terminal["all_control_norms_evaluated_in_real64"] is True
        and terminal["type4_is_scientific_authority"] is True
        and terminal["type2_is_compatibility_only"] is True
        and type(terminal["type2_conversion_events"]) is int
        and terminal["type2_conversion_events"] == 1
        and terminal["type2_conversion_position"]
        == "After successful type-4 publication and strict terminal "
           "acceptance."
        and terminal["type2_conversion_can_affect_acceptance"] is False
        and terminal["failed_or_incomplete_state_can_be_mirrored"] is False
        and terminal["inner_solver_cap_is_new_rejection_gate"] is False
        and terminal["inner_cap_policy"]
        == "MCGMRE MAXIT or MCGABG MAXINT exhaustion alone does not "
           "veto state propagation or publication; only the unchanged "
           "FLU2DR64 strict terminal Boolean has publication authority."
        and terminal["publication_at_flu_cap_without_strict_acceptance"]
        == "NONE"
        and terminal["cutoff_counterfactual_is_diagnostic_only"] is True
        and terminal[
            "cutoff_active_can_change_live_terminal_or_publication"
        ] is False
        and terminal[
            "cutoff_active_nonzero_later_feasibility_classification"
        ] == "INCONCLUSIVE-INHERITED-CUTOFF",
        "terminal authority and mirror",
    )
    require(
        terminal["accepted_publication_preflight"]
        == {
            "position":
                "After the strict terminal Boolean succeeds and before "
                "any accepted-block creation or write.",
            "authoritative_finite_check":
                "Every REAL64 FLUX64 and source-slice element selected "
                "for SPOT-R64/FLUX or SPOT-R64/SOUR publication is IEEE "
                "finite.",
            "compatibility_binary32_finite_range_check":
                "For every value selected for the type-2 FLUX/SOUR "
                "mirror, require "
                "abs(value)<=real(huge(0.0_real32),real64) before the "
                "first type-4 write.",
            "role":
                "Machine-representation safety only; it does not alter "
                "the strict convergence Boolean, solver state, physical "
                "equations, tolerances or controls.",
            "failure_action":
                "Fail the selected ON visit before every accepted-block "
                "write, with no fallback and no authoritative, "
                "compatibility or host mutation.",
        },
        "accepted publication finite/representability preflight",
    )
    require(
        terminal["type2_staging"]
        == "Use one write-only REAL32 terminal staging pass; no GANLIB "
           "type-2 writer receives a REAL64 source and the REAL64 lane "
           "never reads the staging storage.",
        "terminal type-2 staging",
    )
    require(
        data["publication_lexical_gate"]
        == {
            "initial_flux_access":
                "Read-only lookup of the already existing type-2 FLUX "
                "group list after INITFL=1 admission; the ON arm never "
                "creates or replaces it before success.",
            "accepted_block_only": [
                "Create and write the authoritative SPOT-R64 FLUX/SOUR "
                "lists.",
                "Create and write the legacy type-2 SOUR compatibility "
                "list.",
                "Write any legacy type-2 FLUX compatibility mirror.",
                "Write IPFLUX LINK.MACRO, LINK.TRACK, LINK.SYSTEM, "
                "STATE-VECTOR, EPS-CONVERGE, KEYFLX and OPTION host "
                "metadata.",
                "Copy the admitted finite LEAK1D_INPUT32 cache to "
                "IPFLUX/SPOT-LEAK1D.",
            ],
            "static_negative_gate":
                "Reject any preterminal LCMLID, LCMDID, LCMPUT, LCMPPD "
                "or LCMPTC targeting SPOT-R64, legacy SOUR, a "
                "compatibility FLUX payload, IPFLUX "
                "LINK.MACRO/LINK.TRACK/LINK.SYSTEM/STATE-VECTOR/"
                "EPS-CONVERGE/KEYFLX/OPTION, or IPFLUX/SPOT-LEAK1D.",
            "write_failure_scope":
                "The guarantee is zero listed mutation before strict "
                "acceptance and success only after all accepted-block "
                "writes return normally; A7 does not claim rollback or "
                "crash-atomic publication after writing begins.",
            "diagnostic_exception":
                "SPOT-MOC-AUD is the single preterminal "
                "validation-diagnostic exception created by "
                "SPOMOC_BEGIN64; it may remain explicitly incomplete "
                "after failure and is never solver input or "
                "scientific/compatibility authority.",
        },
        "accepted-block publication and diagnostic exception",
    )

    controls = data["unchanged_control_values"]
    require(
        controls["stored_real32_inputs"]
        == ["EPSINR", "EPSUNK", "EPSOUT", "MCCGF EPSI"]
        and controls["new_or_tuned_value_count"] == 0,
        "unchanged controls",
    )

    ledger = data["conversion_ledger"]
    require(
        [
            (entry["legacy_location"], entry["locked_action"])
            for entry in ledger
        ] == EXPECTED_CONVERSION_ACTIONS,
        "conversion ledger scope/order",
    )
    require(
        [entry["replacement"] for entry in ledger]
        == EXPECTED_CONVERSION_REPLACEMENTS,
        "conversion ledger replacement semantics",
    )
    require(
        ledger[0]["mutable_real32_round_trip_after_entry"] is False
        and ledger[1]["mutable_real32_round_trip_after_entry"] is False,
        "entry mutable round trip",
    )

    host = data["host_ingress_and_return_contract"]
    require(
        set(host)
        == {
            "on_selection_position",
            "selection_mechanism",
            "entry_topology",
            "initfl_requirement",
            "records_before_payload",
            "derived_equalities_before_outer_sections",
            "control_use",
            "parsed_control_authority",
            "keyflx_rank_owner",
            "keyflx_identity",
            "region_identity",
            "leak1d_staging",
            "return_status",
            "failure_return",
            "success_return",
            "listed_mutation_before_strict_acceptance",
            "post_acceptance_crash_atomicity_claimed",
            "preterminal_public_diagnostic_exception",
        },
        "host ingress field scope",
    )
    require(
        host["on_selection_position"]
        == "On the admitted REC/direct-MACROLIB topology, parse once and "
           "select the ON arm before any LCMPTC, LCMSIX, legacy "
           "initial-FLUX creation, REAL64 state mutation, tracking-file "
           "consumption or authoritative, compatibility or host-metadata "
           "mutation."
        and host["selection_mechanism"]
        == "Defer the current FLU LINK writes, perform one read-only "
           "admitted FLUGPI parse that returns local "
           "REAL64_ROUTE_ENABLED from the exact R64 keyword together "
           "with the existing controls, and dispatch without parsing the "
           "input stream twice.",
        "one-pass side-effect-free ON selection",
    )
    require(
        host["entry_topology"]
        == [
            "Entry 1: existing modifiable L_FLUX with JENTRY(1)=1 "
            "(REC=true).",
            "Entry 2: read-only direct L_MACROLIB MACRO0; L_LIBRARY and "
            "LCMSIX MACROLIB descent are excluded.",
            "Entry 3: read-only L_TRACK TRACK.",
            "Entry 4: exactly one read-only sequential-binary TRACK_f "
            "unit.",
            "Entry 5: read-only L_PIJ SYSTEM.",
            "Entry 6: read-only L_SOURCE FSOURCE.",
            "No L_FLUX IPFLUP entry and no additional entry are admitted.",
        ]
        and host["initfl_requirement"]
        == "INITFL=1, REC=true, the existing L_FLUX signature is "
           "read-only, and its FLUX group list passes the exact "
           "entry-promotion record contract; the ON arm never writes "
           "SIGNATURE or creates a type-2 initial FLUX list.",
        "exact six-entry REC topology",
    )
    require(
        host["records_before_payload"]
        == {
            "IPFLUX/SIGNATURE":
                "length 3, GANLIB type 3 and exact value L_FLUX",
            "IPFLUX/B2  HETE":
                "absent with length 0 and GANLIB type 99",
            "IPFLUX/B2  B1HOM":
                "absent with length 0 and GANLIB type 99",
            "IPFLUX/STATE-VECTOR":
                "length 40, GANLIB type 1; admitted stored fields give "
                "ITYPEC=0, ILEAK=0, IFRITR=3, IACITR=3, IREBAL=1, "
                "NMERG=1 and NMAT=8 before exact deck overrides",
            "IPFLUX/EPS-CONVERGE":
                "length 5, GANLIB type 2; first three values have frozen "
                "h/2 bits 0x348637bd and final two values are numerical "
                "zero",
            "IPFLUX/IMERGE-LEAK":
                "length NMAT=8, GANLIB type 1, every value 1",
            "IPMACR/SIGNATURE":
                "length 3, GANLIB type 3 and exact value L_MACROLIB",
            "IPMACR/STATE-VECTOR":
                "length 40, GANLIB type 1; exact live dimensions include "
                "NGRP=370, NMAT=8, NIFIS=32 and ITRANC=2",
            "IPSYS/SIGNATURE":
                "length 3, GANLIB type 3 and exact value L_PIJ",
            "IPSYS/LINK.MACRO":
                "length 3, GANLIB type 3 and exact name MACRO0",
            "IPSYS/LINK.TRACK":
                "length 3, GANLIB type 3 and exact name TRACK",
            "IPSYS/STATE-VECTOR":
                "length 40, GANLIB type 1; exact fields 1:14 are "
                "(1,1,1,0,1,1,4,370,14,8,1,0,0,0), proving ITPIJ=1, "
                "IPHASE=1, NGRP=370, NUN=14, NMAT=8 and inactive "
                "ISPOD=0",
            "IPTRK/SIGNATURE":
                "length 3, GANLIB type 3 and exact value L_TRACK",
            "IPTRK/TITLE":
                "length 18, GANLIB type 3 and exact 72-character value "
                "SAL TRACKING padded with blanks",
            "IPTRK/STATE-VECTOR":
                "length 40, GANLIB type 1; fields "
                "(3,4,5,6,9,14,16,22,27,39,40)="
                "(1,8,6,1,0,4,2,1,0,0,0)",
            "IPTRK/TRACK-TYPE":
                "length 3, GANLIB type 3 and exact value MCCG",
            "IPTRK/LINK.FTRACK":
                "length 3, GANLIB type 3 and exact value TRACK_f "
                "matching the sole sequential-binary entry",
            "IPTRK/MCCG-STATE":
                "length 40, GANLIB type 1; fields "
                "(2,3,4,5,6,7,8,9,10,12,13,15,16,18,19,20)="
                "(4,10,0,17,32,80,0,0,4,0,20,1,1,0,1,1)",
            "IPTRK/REAL-PARAM":
                "length 4, GANLIB type 2; values are (EPSI32,0,0,0) "
                "with EPSI32 bits 0x3727c5ac",
            "IPTRK/MATCOD": "length NREG=8, GANLIB type 1",
            "IPTRK/VOLUME": "length NREG=8, GANLIB type 2",
            "IPTRK/KEYFLX$ANIS":
                "length NREG*NLIN*NFUNL=8, GANLIB type 1",
            "IPTRK/KEYCUR$MCCG":
                "length ICREB=NSOUT=NLONG-NREG=6, GANLIB type 1",
            "IPTRK/NZON$MCCG":
                "length NLONG=NREG+NSOUT=14, GANLIB type 1",
            "IPTRK/V$MCCG":
                "length NLONG=NREG+NSOUT=14, GANLIB type 2",
            "IPTRK/ALBEDO": "length 6, GANLIB type 2",
            "IPSOU/SIGNATURE":
                "length 3, GANLIB type 3 and exact value L_SOURCE",
            "IPSOU/NORM-FS":
                "absent with length 0 and GANLIB type 99; the legacy "
                "NORM-FS and MATCOD terminal writes are dead on the "
                "admitted route",
            "IPSOU/STATE-VECTOR":
                "length 40, GANLIB type 1; exact values "
                "(370,14,1,0,...,0)",
            "IPSOU/DSOUR":
                "outer list length 1/type 10, inner list length 370/type "
                "10, every group element length 14/type 2",
            "IPSOU/SPOT-QINT":
                "length NGRP=370, GANLIB type 2 and all finite; "
                "provenance only, never a substitute for the direct "
                "XCSOU64 source scan",
            "IPSYS/SPOT-LEAK1D":
                "required length NGRP=370 and GANLIB type 2; read once "
                "during side-effect-free admission into "
                "LEAK1D_INPUT32(NGRP) and require every value finite",
        },
        "host exact record admission",
    )
    require(
        host["derived_equalities_before_outer_sections"]
        == [
            "NREG_TRACK=NBREG=N2REG=NREG=8",
            "NSOU=N2SOU=NSOUT=6",
            "NFI=NLONG=K=KPN=NUNKNO=14",
            "NLONG=NFI=NREG_TRACK+NSOU",
            "ICREB=NSOUT=NLONG-NREG=6",
            "NNN=NLONG-ICREB=NREG=8",
        ],
        "host derived identities",
    )
    require(
        host["control_use"]
        == "FLU, FLUDRV, FLU2DR64 and MCCGF64 consume only admitted host "
           "records; exact ITPIJ=1, ITRANC=2, INSB=1 and LEAKSW=false "
           "are checked before source/operator payloads, and malformed or "
           "mismatched records cannot select or alter a control branch."
        and host["parsed_control_authority"]
        == "Only the values after the single "
           "TYPE/INIT/REBA/EXTE/UNKT/THER/ACCE/R64/MOCA parse are "
           "authoritative; exact deck overrides may replace admitted "
           "stored defaults, and no later parser or host record may "
           "change them.",
        "host parsed control authority",
    )
    require(
        host["keyflx_rank_owner"]
        == "FLU allocates one contiguous "
           "KEYFLX_HOST3(NREG,NLIN,NFUNL), reads the admitted "
           "KEYFLX$ANIS payload into that rank-3 storage, and passes it "
           "conformingly through FLUDRV to FLU2DR64; neither arm uses the "
           "legacy rank-1-to-rank-3 sequence association."
        and host["keyflx_identity"]
        == "KEYFLX_BASE1 is the same admitted "
           "IPTRK/KEYFLX$ANIS(:,1,1) value view as "
           "KEYFLX_TRK3(:,1,1); source mapping, FLUBAL64, DOORFV64 and "
           "MCGFST may not substitute a separately reconstructed map."
        and host["region_identity"]
        == "For every IR=1..NREG, admitted "
           "MATCOD(IR)=NZON$MCCG(IR)=MATALB_TRK(IR) is in 1..NMAT, and "
           "VOLUME(IR) is finite positive and bitwise identical to "
           "V$MCCG(IR); outer source/rebalancing, MOC source and ray "
           "attenuation therefore use one material-volume map.",
        "host rank and region identity",
    )
    require(
        host["leak1d_staging"]
        == "LEAK1D_INPUT32(NGRP) is an admission-owned read-only "
           "compatibility cache, populated and checked finite before "
           "solver-state mutation; it is never solver input and is "
           "copied to IPFLUX/SPOT-LEAK1D only after strict acceptance.",
        "host leakage compatibility staging",
    )
    require(
        host["return_status"]
        == "Layered explicit status: FLU2DR64 returns CHILD_OK only after "
           "strict acceptance and complete type-4/type-2 publication; "
           "FLUDRV initializes DRIVER_OK=false, writes host metadata only "
           "after CHILD_OK and returns DRIVER_OK=true only after those "
           "writes return normally; FLU initializes HOST_OK=false, writes "
           "deferred LINK.MACRO/LINK.TRACK/LINK.SYSTEM and SPOT-LEAK1D "
           "only after DRIVER_OK, and returns HOST_OK=true only after "
           "those writes return normally."
        and host["failure_return"]
        == "Before strict acceptance, destroy private REAL64 state, mark "
           "the selected ON visit failed, and write none of LINK.MACRO, "
           "LINK.TRACK, LINK.SYSTEM, STATE-VECTOR, EPS-CONVERGE, KEYFLX, "
           "OPTION, SPOT-LEAK1D, authoritative type-4 or compatibility "
           "type-2 output; an explicitly incomplete SPOT-MOC-AUD "
           "diagnostic may remain. A write failure after acceptance "
           "remains failure with no fallback, but rollback is not "
           "claimed."
        and host["success_return"]
        == "Only after strict terminal acceptance may publication begin; "
           "after complete type-4/type-2 publication, FLUDRV host metadata "
           "writes, then FLU deferred LINK.MACRO/LINK.TRACK/LINK.SYSTEM "
           "writes and the LEAK1D_INPUT32 compatibility copy all return "
           "normally, FLU returns success."
        and host["listed_mutation_before_strict_acceptance"] is False
        and host["post_acceptance_crash_atomicity_claimed"] is False
        and host["preterminal_public_diagnostic_exception"]
        == "SPOT-MOC-AUD only; no solver feedback and no authority",
        "host gated return without crash-atomic overclaim",
    )

    dispatch = data["default_off_and_fail_closed"]
    require(
        dispatch["default_enabled"] is False
        and dispatch["off_arm"]
        == "After the common one-pass parse, execute only the existing "
           "legacy FLU/FLUDRV/FLU2DR numerical route; without R64 no "
           "suffixed numerical routine is called."
        and dispatch["selection_authority"]
        == {
            "keyword": "R64",
            "local_flag": "REAL64_ROUTE_ENABLED",
            "default_without_keyword": False,
            "audit_control_relation":
                "Orthogonal to IMCAUD/MOCA; MOCA selects diagnostics only "
                "and never enables the REAL64 numerical route.",
            "storage_and_lifetime":
                "Local to one FLU call; no SAVE/module state, environment "
                "variable or mutable LCM selector record.",
        }
        and dispatch["route_selected_set_before_later_admission_checks"] is True
        and dispatch["both_arms_in_one_visit"] is False
        and dispatch["fallback_after_on_selection"] is False
        and dispatch["on_selection_position"]
        == "Before legacy initial-FLUX creation, allocating or mutating "
           "REAL64 lane state, tracking stream consumption or any "
           "authoritative, compatibility or host-metadata mutation.",
        "default-off mutually exclusive dispatch",
    )
    require(
        dispatch["unsupported_or_invalid_on_state"]
        == "STOP-SELECTED-VISIT-FAIL-CLOSED",
        "fail-closed ON action",
    )
    require(
        dispatch["public_output_atomicity"]
        == "No listed authoritative, compatibility or host record changes "
           "before strict terminal acceptance; rollback after "
           "accepted-block writing begins is not claimed."
        and dispatch["legacy_off_identity_requirement"]
        == "A9 must prove the parser/dispatch refactor leaves existing OFF "
           "scientific output, public records and call counts "
           "byte-identical in short synthetic tests and adds no "
           "scientific log record.",
        "public output gate and OFF identity",
    )

    require(
        data["forbidden_actions"] == REQUIRED_FORBIDDEN_ACTIONS,
        "forbidden action scope",
    )

    split = data["phase_split"]
    require(list(split) == ["A7", "A8", "A9"], "phase split scope/order")
    require(
        split["A7"]
        == {
            "name": "complete suffixed-lane ownership and ABI blueprint",
            "deliverable":
                "This manifest, its README, and later static checker/receipt "
                "only.",
            "production_fortran": False,
            "compilation": False,
            "execution": False,
            "scientific_claim": "DESIGN-COMPLETENESS-ONLY",
        },
        "A7 design-only boundary",
    )
    a8_nodes = split["A8"]["required_nodes"]
    for node in (
        "DOORFV64 active-tail owner",
        "MCCGF64 SC_BY_GROUP32 and SIGAL32 owner with checked MCGSIG reuse",
        "MCGFLX64",
        "checked PRINDM REAL64 diagnostic reuse",
        "MCGMRE64",
        "MCGFL164 using the A1-through-A6 contracts and MOCIK3",
        "MCGFFIR64_RANK_ADAPTER with a direct rank-2 KEYFLX section and "
        "valid XSI_INACTIVE64 storage",
        "checked SPOMOC_CAPTURE64 REAL64 audit interface",
        "MCGFCS64",
        "MCGFCA64 to MCGFCR64; MCGFCA64 direct to MCGPRA64 to "
        "MSRLUS1; and MCGFCA64 to MCGABG64 to MCGPRA64 to MSRLUS1",
        "suffixed MCGPRA64 IM(NLONG+1) shape correction and checked reuse "
        "of MSRLUS1",
    ):
        require(node in a8_nodes, f"A8 node: {node}")
    require(
        "IPRINT>5 diagnostics call PRINDM with REAL64 state; negative "
        "checks reject PRINAM and any REAL32 adapter."
        in split["A8"]["required_checks"],
        "A8 PRINDM diagnostic gate",
    )
    require(
        "The selected toolchain proves kind(0.0d0)==real64 before any "
        "checked legacy DOUBLE PRECISION kernel, including PRINDM, is "
        "accepted." in split["A8"]["required_checks"],
        "A8 DOUBLE PRECISION kind identity gate",
    )
    require(
        "MCGFL164 compiles against SPOMOC_CAPTURE64 with four REAL64 "
        "rank-2 inputs; negative checks reject legacy SPOMOC_CAPTURE or "
        "REAL32 QFR/EVAL actuals." in split["A8"]["required_checks"],
        "A8 SPOMOC_CAPTURE64 interface gate",
    )
    require(
        "IMPX diagnostics compile with FGAR64 and TEMP64; negative checks "
        "reject REAL32 captures of QFR_TAIL64, PHIIN_TAIL64 or EPS64 and "
        "the warning compares TEMP64 to EPSI64."
        in split["A8"]["required_checks"],
        "A8 diagnostic no-downcast gate",
    )
    require(
        "KEYFLX_BASE1, KEYFLX_TRK3, the direct KEYFLX_TRK3(:,1,:) "
        "rank-2 section and PJJIND_TRK2 compile with their frozen "
        "distinct ranks; sequence association and flat PJJIND are "
        "rejected." in split["A8"]["required_checks"],
        "A8 KEYFLX/PJJIND rank compile gate",
    )
    require(
        "The MCGFCF callback uses a global explicit-shape "
        "MCGFFIR64_RANK_ADAPTER and its direct KEYFLX_TRK3(:,:,1) "
        "rank-2 section; object and call-list checks enforce a checked "
        "internal MCGFFIR call, and negative checks reject "
        "descriptor-based callback ABIs or rank-3/flat sequence "
        "association into MCGFFIR." in split["A8"]["required_checks"],
        "A8 MCGFFIR rank bridge gate",
    )
    require(
        "The locked regular-tracking header proves "
        "NREG_TRACK=NBREG=N2REG=8, NSOU=N2SOU=NSOUT=6 and "
        "NFI=NLONG=K=KPN=NUNKNO=14 before MATALB payload consumption, "
        "and MATALB_TRK has exact bounds (-NSOUT:NREG)."
        in split["A8"]["required_checks"],
        "A8 regular tracking header extent gate",
    )
    require(
        "CAZ0_INACTIVE64(NANGL) and XSI_INACTIVE64(NSOUT) are "
        "conforming defined REAL64 storage; negative checks reject "
        "XSIXYZ(:,0) or any invalid XSI actual, while exact stored "
        "CPO32(NMU) is preserved." in split["A8"]["required_checks"],
        "A8 regular tracking inactive-formal gate",
    )
    require(
        "All live MCCGF tracking records XMU/WZMU/ZMU/V/NZON/KEYCUR "
        "and MCGSIG records ICODE/ALBEDO/DRAGON-TXSC pass exact LCMLEN "
        "type-and-extent admission before payload access."
        in split["A8"]["required_checks"],
        "A8 tracking and MCGSIG record gate",
    )
    require(
        "BC-REFL+TRAN has exact length NLONG-NREG and GANLIB type 1 "
        "before mapping, and every active PJJ$MCCG has exact length "
        "NREG*NPJJM and GANLIB type 2 before MCGFST."
        in split["A8"]["required_checks"],
        "A8 BC/PJJ record gate",
    )
    require(
        "Frozen discrete values pass the existing capture-layout "
        "admission: PJJIND_TRK2(1,:)=[1,1], scalar/current keys form a "
        "duplicate-free permutation of 1..KPN, boundary and zone "
        "indexes are in range, and volume/operator payloads are finite "
        "with positive volume." in split["A8"]["required_checks"],
        "A8 frozen discrete value gate",
    )
    require(
        "PACA=4 active CF$MCCG is mapped as CF32(LC), and negative "
        "compile contracts reject CF32(N1) whenever N1 differs from LC."
        in split["A8"]["required_checks"],
        "A8 active CF extent gate",
    )
    require(
        "All nine active PACA=4 records "
        "IM/MCU/PI/JU/DIAGQ/CQ/ILUDF/CF/DIAGF pass exact LCMLEN "
        "type-and-extent admission before mapping to their frozen "
        "one-dimensional views." in split["A8"]["required_checks"],
        "A8 all active PACA=4 record gate",
    )
    require(
        "DIAGF_INACTIVE32 is passed only to the direct pre-MCGABG "
        "MCGPRA64 call; MCGABG64 and its internal MCGPRA64 calls use "
        "active DIAGF32(N1)." in split["A8"]["required_checks"],
        "A8 DIAGF active/inactive use gate",
    )
    require(
        "PACA=4 uses local defined IM0_INACTIVE(1) and "
        "MCU0_INACTIVE(1) only with LC0=0 assumed-size inactive "
        "formals; no SAVE object or inactive-record mapping is allowed."
        in split["A8"]["required_checks"],
        "A8 inactive integer formal gate",
    )
    require(
        "MCGPRA64 declares IM(NLONG+1), preserves arithmetic and calls "
        "MSRLUS1 conformingly; the ON arm contains no call to legacy "
        "MCGPRA." in split["A8"]["required_checks"],
        "A8 MCGPRA64 IM extent gate",
    )
    require(
        "PACA=4 inactive explicit-shape formals use conforming defined "
        "storage, and negative compile contracts reject one-element "
        "substitutes." in split["A8"]["required_checks"],
        "A8 PACA=4 inactive-formal compile gate",
    )
    require(
        "Exact integer(int64) cutoff deltas propagate from every MCGABG64 "
        "call to the DOORFV64 boundary without reset, overwrite or hidden "
        "shared state." in split["A8"]["required_checks"],
        "A8 cutoff-delta propagation gate",
    )
    require(
        "complete continuous REAL64 lane" in split["A8"]["does_not_prove"],
        "A8 cannot overclaim complete lane",
    )
    a9_nodes = split["A9"]["required_nodes"]
    for node in (
        "Default-off FLU/FLUDRV dispatch",
        "Independent default-false R64 selector and one-pass admitted "
        "FLUGPI parse",
        "FLU KEYFLX_HOST3 rank-3 owner and admitted region identity",
        "Unchanged XDRTA2 operator initialization exactly once",
        "FLU2DR64 unique FLUX64 eight-slice owner",
        "Exact frozen DSOUR and off-group source-update order in REAL64",
        "Immutable admitted OFFGROUP32 scattering bundle shared with "
        "FLUBAL64",
        "Connection to the frozen A8 inner route",
        "Production SPOMOC_BEGIN64/SPOMOC_CAPTURE64 audit implementation "
        "and ON-arm wiring",
        "FLUBAL64 and ALSBD",
        "FLU2AC64",
        "All inner and outer terminal norms in REAL64",
        "FLU2DR64 visit-total integer(int64) cutoff counter",
        "SPOT-R64 type-4 authoritative publication",
        "One terminal type-2 compatibility mirror",
    ):
        require(node in a9_nodes, f"A9 node: {node}")
    require(
        "CUTOFF_ACTIVE_VISIT64 is initialized once and every normally "
        "returned DOORFV64 delta is added exactly once."
        in split["A9"]["required_checks"],
        "A9 cutoff visit aggregation gate",
    )
    require(
        "SPOMOC_BEGIN64 admits exactly MAXOUT=500, MAXINR=740, INITFL=1 "
        "and ACCE=(3,3) with all other frozen identities; it changes no "
        "solver control and the OFF arm still uses legacy SPOMOC_BEGIN."
        in split["A9"]["required_checks"],
        "A9 SPOMOC_BEGIN64 admission gate",
    )
    require(
        "SPOMOC_CAPTURE64 preserves the legacy audit admission/finite "
        "checks, writes SPOT-M-QFR/EVAL/SRC/RAW directly as type 4, and "
        "cannot change solver state, terminal acceptance or publication."
        in split["A9"]["required_checks"],
        "A9 SPOMOC_CAPTURE64 implementation gate",
    )
    require(
        "R64 alone enables the REAL64 route, defaults false and is "
        "orthogonal to MOCA; the common one-pass parser is read-only on "
        "the admitted REC route and short OFF tests prove legacy "
        "scientific/public-output identity."
        in split["A9"]["required_checks"],
        "A9 independent selector and OFF identity gate",
    )
    require(
        "The admitted ON route calls unchanged XDRTA2 exactly once before "
        "the first MCGSCA use; static checks reject omission, duplication "
        "or a replacement exponential table."
        in split["A9"]["required_checks"],
        "A9 XDRTA2 initialization gate",
    )
    require(
        "FLUBAL64 receives only the direct KEYFLX, MATALB, SURFAC and "
        "FLUX64(:,:,7) sections plus exact read-only OFFGROUP32 "
        "rectangular dummies, performs no later off-group LCMGET, and "
        "FLU2AC64 receives only the direct inner or outer three-slice "
        "FLUX64/AKEEP64 sections; element-actual sequence association is "
        "rejected."
        in split["A9"]["required_checks"],
        "A9 outer direct-section gate",
    )
    require(
        "Exact ITPIJ=1, ITRANC=2, INSB=1, LEAKSW=false and frozen "
        "associated FSOURCE admission precedes source construction; each "
        "outer iteration copies DSOUR, the zero-NUSIGF fission term is "
        "inactive, and each inner iteration skips ITPIJ=2/4 XSDIA "
        "addition before live JG!=IG XSCAT updates."
        in split["A9"]["required_checks"],
        "A9 frozen source order gate",
    )
    require(
        "SOURCE64 is initialized once to +0.0_real64 before MCGFCS64; "
        "inactive groups and unrepresented entries retain that defined "
        "positive-zero bit pattern."
        in split["A9"]["required_checks"]
        and
        "RESPONSE64 is initialized to +0.0_real64 at the start of every "
        "MCGFL164 response call before MCGFCF/MCGFST; inactive and "
        "unrepresented response entries remain defined positive zero."
        in split["A9"]["required_checks"],
        "A9 defined SOURCE64/RESPONSE64 storage gate",
    )
    require(
        "Every group NJJS00/IJJS00/IPOS00/SCAT00 record is admitted once "
        "with exact type, extent, index range and finite values into "
        "immutable OFFGROUP32, which both FLU2DR64 and FLUBAL64 reuse "
        "without later LCMGET."
        in split["A9"]["required_checks"],
        "A9 immutable OFFGROUP32 gate",
    )
    require(
        "FLU owns conforming KEYFLX_HOST3 rank-3 storage; KEYFLX_BASE1 "
        "and KEYFLX_TRK3(:,1,1) are the same admitted KEYFLX$ANIS values, "
        "MATCOD/NZON and VOLUME/V identities close, and layered "
        "CHILD_OK/DRIVER_OK/HOST_OK gates order FLU2DR64 publication, "
        "FLUDRV metadata, then FLU LINK.* and SPOT-LEAK1D writes."
        in split["A9"]["required_checks"],
        "A9 host rank/identity and layered status gate",
    )
    require(
        "SPOT-R64, legacy type-2 SOUR/FLUX, LINK.*, host metadata and "
        "SPOT-LEAK1D writes occur only inside the strict accepted block; "
        "static negative checks reject preterminal creation or writes, "
        "while SPOT-MOC-AUD remains the sole no-feedback diagnostic "
        "exception. Success requires a normal complete write sequence; "
        "post-acceptance rollback is not claimed."
        in split["A9"]["required_checks"],
        "A9 accepted-block publication gate",
    )
    require(
        "IPRT diagnostics compile with FL_PRINT64 or a direct REAL64 "
        "indexed view; negative checks reject a REAL32 FL capture, and "
        "the locked ITYPEC=0 route contains no RKEFF=REAL(AKEFF) "
        "assignment." in split["A9"]["required_checks"],
        "A9 terminal diagnostic no-downcast gate",
    )
    require(
        "Every normal ON return emits exactly one stable decimal-int64 "
        "CUTOFF_ACTIVE_VISIT64 diagnostic line with no int32 narrowing; "
        "the value remains no-feedback and OFF emits none."
        in split["A9"]["required_checks"],
        "A9 stable cutoff observation gate",
    )
    require(
        "After the strict terminal Boolean and before any accepted-block "
        "write, every authoritative REAL64 value is finite and every "
        "compatibility-mirror value satisfies "
        "abs(x)<=real(huge(0.0_real32),real64); this "
        "machine-representation preflight cannot change convergence."
        in split["A9"]["required_checks"],
        "A9 publication representation-safety gate",
    )
    require(
        split["A9"]["permitted_claim_after_pass"]
        == "COMPLETE-STATIC-REAL64-RADIAL-LANE-CLOSURE",
        "A9 claim boundary",
    )
    require(
        "Radial solver convergence" in split["A9"]["does_not_prove"]
        and "Outer Picard convergence" in split["A9"]["does_not_prove"],
        "A9 cannot claim convergence",
    )
    require(
        "Default-off, no-fallback, pre-acceptance write gating and the "
        "limited post-acceptance failure scope are explicit."
        in data["a7_can_establish"]
        and all(
            "failure-atomicity" not in item
            for item in data["a7_can_establish"]
        ),
        "A7 honest publication-failure claim boundary",
    )

    later = data["later_runtime_sequence"]
    require(
        [item["gate"] for item in later]
        == [
            "runtime provenance preflight",
            "bounded plane-1 REAL64 feasibility capture and exact replay",
            "new same-lane Stage-4 comparison",
            "direct Picard trajectory",
        ],
        "later runtime sequence",
    )
    require(
        later[0]["transport_applications"] == 0
        and later[1]["requires"]
        == "Successful separately authorized runtime provenance preflight"
        and later[2]["requires"] == "REAL64-RADIAL-FEASIBLE"
        and later[3]["requires"]
        == "Separately qualified and replayed all-component Stage-4 pass",
        "later gate preconditions",
    )

    if verify_environment:
        validate_readme_contract(README.read_text())
        require(RUNNER.is_file(), "missing A7 runner")
        validate_runner_contract(RUNNER.read_text())
        validate_makefile_contract((ROOT / "Makefile").read_text())
        validate_baseline_sources(data)

        production = "\n".join(
            path.read_text(errors="replace")
            for pattern in ("*.c", "*.f", "*.F", "*.f90", "*.F90")
            for path in (ROOT / "src").glob(pattern)
            if path.is_file()
        )
        for future_name in EXPECTED_ABI_ORDER:
            require(
                re.search(rf"(?i)\b{re.escape(future_name)}\b", production)
                is None,
                f"A7 future routine connected to production: {future_name}",
            )

    if verify_freeze:
        validate_hash_freeze(data, manifest_path=MANIFEST)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    try:
        data = load_manifest(args.manifest)
        require(
            args.manifest.resolve() == MANIFEST.resolve(),
            "alternate manifest path is not an A7 release authority",
        )
        validate(data)
    except (KeyError, OSError, TypeError, PhaseA7Error) as exc:
        raise SystemExit(f"SPOR64 PHASE-A7 REJECTED: {exc}") from exc
    print(
        "SPOR64 PHASE-A7 CONTRACT PASS: "
        "COMPLETE-REAL64-LANE-OWNERSHIP/ABI-BLUEPRINT; "
        "IMPLEMENTATION=NONE; FORTRAN-COMPILATIONS=0; "
        "TRACKING-READS=0; TRANSPORT-APPLICATIONS=0; DRAGON-RUNS=0"
    )


if __name__ == "__main__":
    main()
