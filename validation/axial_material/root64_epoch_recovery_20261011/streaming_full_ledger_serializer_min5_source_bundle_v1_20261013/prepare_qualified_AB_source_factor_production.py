"""Prepare an isolated SOURCEFACTOR_BUILD family; never prepare transport.

Only the two historical FLU2DR64 intergroup source entries change, and only
for SPOT's one-dimensional raw Legendre coordinates.  The unchanged frozen
48-cell/SN32/SCAT3 receiver, white kernel, radial objects and archive chain
are linked explicitly.  Successful compiled arithmetic and receiver controls
admit this build as an input to a future fresh coupled trial, not as an AAA,
ABA, continuous-transport, physical-balance or CE accuracy qualification.

There is no import-time file I/O, compilation or numerical calculation.  The
three CLI actions require an explicit invocation after source review.  An
actual completed, sealed, word-exact production capture is a run dependency.
"""

import argparse
import ast
import difflib
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / "validation/artifacts"
OUT = ART / "axial-material-source-factor-build-20261006"
PROD = ART / "axial-material-production-qualified-AB-white-trace-refined-envpin-20261005"
SOURCE = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005"
CAPTURE = ART / "axial-material-AAA-production-angular-capture-20261006"
ANG = ART / "axial-material-AAA-white-trace-angular-convergence-20261005"
COMP = ART / "axial-material-AAA-compensated-flight-20261004"
COLD = ART / "axial-material-AAA-white-trace-cold-control-paths-20261004"
CAUSAL = ART / "axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005"
FULL_SOURCE = ROOT / "validation/axial_material/qualify_refined_AAA_layered_full.py"
PARENT_RUNTIME = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/streaming_full_ledger_serializer_min5_source_bundle_v1_20261013/runtime')
PARENT_SOURCE_SHA = 'b8418e994a3765540dd6e0f36970c80a166813d4d75c39943c7b7dbfb359176d'
REVIEW = ROOT / "validation/axial_material/production_source_factor_binary_review.json"
BASE_REVISION = "299546c405a47f7e3a7f75af54d392492d649781"
BASE_SHA = "90bedc3f7cc4d320355dbbf43988ca8fb43e59dbee493a7f19fa8c050c42e8a5"
LIB_SHA = "954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9"
OBJECT_SHA = "4ba03f8b762eb1936118b35b5196a3257d151e5564cdb0fe77a41d9b36b6d175"
DRAGON_SHA = "51b2d3ff947daa3ea523932bcc28276b054632f0bfc6cf76fa21ac458a4f7be4"
REVIEW_SHA = "7970e6e93b8d71b6df420278d83fc3ab8793783428f9ed843990edf715166450"
FULL_SHA = "70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6"
PREPARED_SHA = "024ffb9263e3d3b6cf10301d6fe2bac5a87a9b368008440e01038982291a6d53"
SPEC_SHA = "8c2297533ff582e81cef6430947a0557e921830304673a6a8a6c0149fd7a33ae"
ANG_DECL_SHA = "aec1389e18a009a09fd1919e5e8291b23be1122136b0dbc301afd19d46ee91a8"
RECIPE_SHA = "56ebbfcc334dc77b1134a218f46a60393503a79bd9b167f2ef2e74aba11e5806"
THREAD_KEYS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
               "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS")
GATES = ("source_convergence", "block_stability", "statistical_resolution", "keff",
         "scalar_flux", "nu_fission", "input_equivalence", "currents_balance_symmetry")
NR, NZ, NA, NL, NM, NSNAP = 8, 48, 32, 3, 24, 3
FIELD_LIMIT = 5e-12
SOURCE_ROWS = 384
SOURCE_COMPARISON_SCALAR_CALLS = 768
INTERFACE_CALLS = 14
INTERFACE_SOURCE_SCALAR_CALLS = 42
TOTAL_WALL, STAGE_WALL, RSS_CAP = 1800, 600, 512
ARCHIVE_RESERVE = 2 * 2**30
LABELS = ("build/build_00", "build/build_01", "build/build_02", "build/build_03",
          "controls/controls", "audit/audit")
CAPTURE_SEAL_SHA = "16f67ec74e41d3282a7e90fe342e0165c81a8fb97a6cfc1cd72615e6a9ac9c0a"
CAPTURE_DECL_SHA = "6ed345f39f4ddab3299b2845877f10903f38fe89d9f9a5ebf875acadd3d3ce2b"

OLD_BLOCK = (
    "               IF(JG.NE.IG) THEN\n"
    "                  FLUX(IND,IG,8)=FLUX(IND,IG,8)+REAL(2*IAL+1)*\n"
    "     >            XSCAT(IPOS(IBM)+JND-1)*FLUX(IND,JG,7)\n"
    "               ENDIF")
NEW_BLOCK = (
    "               IF(JG.NE.IG) THEN\n"
    "                  IF((CXDOOR.EQ.'SPOT').AND.(NDIM.EQ.1)) THEN\n"
    "                     FLUX(IND,IG,8)=FLUX(IND,IG,8)+\n"
    "     >               XSCAT(IPOS(IBM)+JND-1)*FLUX(IND,JG,7)\n"
    "                  ELSE\n"
    "                  FLUX(IND,IG,8)=FLUX(IND,IG,8)+REAL(2*IAL+1)*\n"
    "     >            XSCAT(IPOS(IBM)+JND-1)*FLUX(IND,JG,7)\n"
    "                  ENDIF\n"
    "               ENDIF")


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if not path.is_file() or (wanted is not None and digest(path) != wanted):
        raise ValueError("missing or changed declared file: " + str(path))
    return path


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def inventory(folder):
    """Pin regular files and symlink targets, without traversing symlink dirs."""
    files, links = {}, {}
    for parent, directories, names in os.walk(folder, followlinks=False):
        for name in [*directories, *names]:
            path = Path(parent) / name
            relative = str(path.relative_to(folder))
            if path.is_symlink():
                links[relative] = os.readlink(path)
            elif path.is_file():
                files[relative] = digest(path)
    return dict(files=files, symlinks=links)


def verify_inventory(folder, expected):
    if inventory(folder) != expected:
        raise ValueError("preserved predecessor namespace or hash changed: " + str(folder))


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, require(path))
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    if Path(result.__file__).resolve() != Path(path).resolve():
        raise ValueError("actual module source binding differs")
    return result


def modules():
    """Normal selected serializer import first; original FULL bytes unchanged."""
    require(PARENT_RUNTIME / "production_runner.py", PARENT_SOURCE_SHA)
    cached = sys.modules.get("production_runner")
    if cached is not None and Path(cached.__file__).resolve() != (PARENT_RUNTIME / "production_runner.py").resolve():
        raise ValueError("existing production_runner is not the selected serializer Source; no cache replacement")
    # Original immutable production_inputs and other imports remain available.
    sys.path.insert(0, str(PROD / "runtime"))
    sys.path.insert(0, str(PARENT_RUNTIME))
    import production_runner as production
    if Path(production.__file__).resolve() != (PARENT_RUNTIME / "production_runner.py").resolve():
        raise ValueError("actual derived serializer parent import binding differs")
    full = module(require(FULL_SOURCE, FULL_SHA), "axsf_frozen_full")
    return full, production


def baseline():
    require(ROOT / "lib/Darwin_arm64/libDragon.a", LIB_SHA)
    require(ROOT / "src/FLU2DR64.o", OBJECT_SHA)
    raw_member = subprocess.run(["/usr/bin/ar", "-p",
        str(ROOT / "lib/Darwin_arm64/libDragon.a"), "FLU2DR64.o"],
        check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(raw_member).hexdigest() != OBJECT_SHA:
        raise ValueError("actual frozen library member differs")
    raw = subprocess.run(["/usr/bin/git", "-C", str(ROOT), "show",
        BASE_REVISION + ":src/FLU2DR64.f"], check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError("recovered compiled-arithmetic baseline differs")
    return raw.decode("utf-8")


def correct_source(original):
    if original.count(OLD_BLOCK) != 2 or original.count("REAL(2*IAL+1)*") != 2:
        raise ValueError("exactly both historical source entries required")
    candidate = original.replace(OLD_BLOCK, NEW_BLOCK)
    if candidate.count(NEW_BLOCK) != 2 or candidate.replace(NEW_BLOCK, OLD_BLOCK) != original:
        raise ValueError("two-entry whole-source byte restoration failed")
    # This expression is deliberately untouched: actual production ITPIJ=1
    # bypasses the ITPIJ=2/4 self-reduction branch; do not change that branch.
    self_lines = [line for line in original.splitlines() if "XSDIA" in line and "2*IAL+1" in line]
    if len(self_lines) != 1 or any(candidate.count(line) != original.count(line) for line in self_lines):
        raise ValueError("the historical XSDIA self-reduction expression must remain exact")
    return candidate


def fixed_to_free(block):
    """Extract the literal production statements, preserving expression order."""
    lines = []
    for line in block.splitlines():
        body = line[6:].strip()
        if line[5] not in (" ", "0"):
            if not lines:
                raise ValueError("orphan fixed-form continuation")
            lines[-1] += " &"
            body = "& " + body
        lines.append("    " + body)
    return "\n".join(lines)


def guard_admission(full):
    folder = full.OUT / "preflight/live_guard"
    path = require(folder / "guard_controls.json",
        "ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454")
    guard = read(path)
    tested = require(folder / "tested_driver_source.py", guard["source_sha256"])
    verify({str(folder / name): sha for name, sha in guard["control_files"].items()})
    def class_text(source):
        text = Path(source).read_text()
        return next(ast.get_source_segment(text, node) for node in ast.parse(text).body
            if isinstance(node, ast.ClassDef) and node.name == "OwnRSSSerialExecutor")
    if (class_text(FULL_SOURCE) != class_text(tested)
            or not guard["positive_child_completed"] or not guard["actual_oversize_child_rejected"]
            or not guard["terminated_own_child_not_live"] or guard["rss_cap_mib"] != RSS_CAP):
        raise ValueError("actual immutable positive/oversize live guard proof required")
    return [path, tested, *[folder / name for name in guard["control_files"]]]


def check_watch(root, stage):
    path = (Path(root) / (stage["label"] + ".log")).with_suffix(".watchdog.json")
    value = read(require(path))
    if (value["returncode"] != 0 or value["limit_failure"] is not None
            or value["command"] != stage["command"] or value["rss_cap_mib"] != RSS_CAP
            or not 0 < value["wall_cap_seconds"] <= STAGE_WALL
            or not 0 <= value["sampled_peak_rss_mib"] < RSS_CAP
            or not 0 <= value["elapsed_seconds"] < STAGE_WALL
            or value["own_child_only"] is not True or value["liveness_group_cleanup"] is not True):
        raise ValueError("actual bounded stage watchdog failed: " + stage["label"])
    require(Path(root) / (stage["label"] + ".log"), stage["log_sha256"])
    return dict(path=str(path), sha256=digest(path), peak_rss_mib=value["sampled_peak_rss_mib"],
                elapsed_seconds=value["elapsed_seconds"])


def capture_admission(expected_seal=None):
    """Require the real all-group capture and replay, not static review flags."""
    if expected_seal is not None and expected_seal != CAPTURE_SEAL_SHA:
        raise ValueError("the fixed original successful production capture seal is required")
    seal_path = require(CAPTURE / "seal.json", CAPTURE_SEAL_SHA)
    require(CAPTURE / "declaration.json", CAPTURE_DECL_SHA)
    seal = read(seal_path)
    if seal["schema"] != "AXMAT_PRODUCTION_ANGULAR_CAPTURE_SEAL_V1":
        raise ValueError("completed actual angular capture seal required")
    actual = {str(p.relative_to(CAPTURE)) for p in CAPTURE.rglob("*") if p.is_file()}
    if actual != set(seal["files"]) | {"seal.json"}:
        raise ValueError("capture seal must cover the exact complete namespace")
    verify({str(CAPTURE / name): sha for name, sha in seal["files"].items()})
    declaration, driver, audit = (read(CAPTURE / name) for name in
        ("declaration.json", "driver_result.json", "audit/result.json"))
    verify(declaration["files"])
    if (driver["classification"] != "COMPLETE_BOUNDED_PRODUCTION_ANGULAR_CAPTURE_ONLY"
            or driver["error"] is not None
            or audit["classification"] != "COMPLETE_PRODUCTION_ANGULAR_CAPTURE_ONLY"
            or not audit["original_map012_scientific_records_word_exact"]
            or not audit["complete_production_370_groups"] or not audit["original_terminal_passed"]
            or not audit["all_three_moments_and_currents_byte_exact"]
            or not audit["original_keff_byte_exact"] or not audit["raw_fields_and_sources_unmodified"]
            or driver["AAA_accuracy_qualified"] or driver["ABA_admitted"]
            or audit["AAA_accuracy_qualified"] or audit["ABA_admitted"]):
        raise ValueError("actual complete word-exact replay PASS required")
    if declaration["actual_source_contract"] != dict(ITPIJ=1, NANIS=2, NDIM=1, INSB=1,
            LSCAL=False, self_scattering_reduction_branch_reachable=False):
        raise ValueError("actual source/self-reduction dispatch contract differs")
    rows = audit["groups"]
    if (len(rows) != 370 or [row["group"] for row in rows] != list(range(1, 371))
            or any(not row["all_three_raw_moments_and_currents_byte_exact"]
                   or not row["all_rebuilt_native_blocks_byte_exact"] for row in rows)):
        raise ValueError("all actual capture group/source coordinates required")
    stages = read(CAPTURE / "AAA/stages.json")["stages"]
    if len(stages) != 6 or any(stage["status"] != "PASS" for stage in stages):
        raise ValueError("all six actual capture stages required")
    for stage in stages:
        check_watch(CAPTURE, stage)
    raw = read(CAPTURE / "raw_capture_receipt.json")
    if raw["raw_capture_count"] != 1483 or len(raw["files"]) != 1483:
        raise ValueError("all 1483 actual native source/field/return/block files required")
    verify({str(CAPTURE / name): sha for name, sha in raw["files"].items()})
    return dict(root=str(CAPTURE), seal_sha256=digest(seal_path),
                declaration_sha256=digest(CAPTURE / "declaration.json"),
                replay_classification=driver["classification"], groups=370, raw_archives=1483)


def capture_fixture():
    """Copy the actual stored SN32, PL, basis and region-volume REAL32 words."""
    path = require(CAPTURE / "AAA/angular_field_g051.bin")
    with path.open("rb") as stream:
        if stream.read(8) != b"AXCFD001":
            raise ValueError("actual native angular field schema differs")
        header = struct.unpack("<8i", stream.read(32))
        ni, ns, nd = header[4:7]
        if header[0] != 51 or ni != NZ + NZ * NR + 2 + NA:
            raise ValueError("actual captured field dimensions differ")
        stream.seek(ni * 4, 1)
        single = stream.read(ns * 4)
        if len(single) != ns * 4 or ns != NZ + (NM + 1) * (1 + NL) + 2 * NR + 2 + NA * (2 + NL):
            raise ValueError("actual production primitive layout differs")
        if len(stream.read()) != nd * 8:
            raise ValueError("actual native angular payload incomplete")
    first = (NZ + (NM + 1) * (1 + NL)) * 4
    basis = single[first:first + NR * 4]
    volume = single[first + NR * 4:first + 2 * NR * 4]
    angles = single[first + (2 * NR + 2) * 4:]
    # Header declares exact shapes; payload uses Fortran's native column order.
    result = b"AXSFF001" + struct.pack("<6i", NA, NZ, NR, NL, NM, NSNAP)
    result += angles + basis + volume
    return result, dict(source=str(path), source_sha256=digest(path), group=51,
        payload="mu(32),w(32),PL(3,32),basis(8,1),vol2d(8), all REAL32 Fortran order",
        numerical_primitive_words_copied_exactly=True,
        fixture_basis_scale=2.0, fixture_basis_orientation_unchanged=True,
        fixture_operator="Synthetic independent diagonal source-interface control: sigma=1/16, "
          "cell width=1/8, no self scattering/radial feedback/white term; production objects unchanged.")


CONTROL_PROGRAM = r"""program source_factor_controls
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  use SPOT1P64_CACHE_MOD, only: SPOT1P64_CACHE_BEGIN,SPOT1P64_CACHE_CLEAR
  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_CONFIGURE
  implicit none
  integer,parameter :: nr=8,nz=48,na=32,nl=3,nmat=24,nsnap=3
  integer :: e,s,l,g,x,p,k,i,z,u,info,mark(4),dims(6),it(6)
  character(8) :: magic
  character(12) :: door
  real(real32) :: xs,du(na),w(na),pl(nl,na),basis(nr,1),vol2d(nr)
  real(real32) :: vol1d(nz),total(0:nmat),sgas(0:nmat,nl),zcode(2)
  integer :: mat1d(nz),mat(nz,nr),ncode(2)
  real(real64) :: phi,oldq,newq,seed,qext(1,nl,nz,nr),radial(nr,nsnap)
  real(real64) :: flux(1,nl,nz,nr),cour(nz+1,nr),xnei(na,nr),coeff(nl),c(nl,7)
  real(real64),parameter :: phis(4)=[0.d0,1.d0,-0.125d0,0.9d0]
  real(real32),parameter :: xss(2)=[0.125,1.0/7.0]
  external SPOT1P64
  if (storage_size(1_int32)/=32 .or. storage_size(1.0_real32)/=32 .or. &
      storage_size(1.0_real64)/=64) stop 101
  open(newunit=u,file='source_controls.bin',access='stream',form='unformatted',status='new')
  write(u) 'AXSFU001',int(384,int32)
  seed=0.375d0
  do e=1,2
    do s=1,4
      door='SPOT';k=s
      if(s==4) then
        door='MCCG';k=2
      endif
      do l=0,2
        do g=1,2
          do x=1,2
            do p=1,4
              xs=xss(x);phi=phis(p)
              call old_source(e,door,k,l,g,xs,phi,seed,oldq)
              call new_source(e,door,k,l,g,xs,phi,seed,newq)
              write(u) int([e,s,l,g,x,p],int32),xs,phi,seed,oldq,newq
            enddo
          enddo
        enddo
      enddo
    enddo
  enddo
  close(u)
  open(newunit=u,file='receiver_fixture.bin',access='stream',form='unformatted',status='old')
  read(u) magic,dims
  if(magic/='AXSFF001'.or.any(dims/=[na,nz,nr,nl,nmat,nsnap])) stop 102
  read(u) du,w,pl,basis,vol2d
  close(u)
  ! Preserve the actual basis orientation; explicitly scale only this unit
  ! fixture to exercise the production receiver's nonunit Gram handling.
  basis=2.0*basis
  c(:,1)=[1.d0,0.d0,0.d0];c(:,2)=[0.d0,1.d0,0.d0];c(:,3)=[0.d0,0.d0,1.d0]
  c(:,4)=[1.d0,0.01d0,0.d0];c(:,5)=[1.d0,-0.01d0,0.d0]
  c(:,6)=[1.d0,0.01d0,0.005d0];c(:,7)=[1.d0,-0.02d0,0.0125d0]
  vol1d=0.125;total=0.0625;total(0)=0.0;sgas=0.0;radial=0.d0
  ncode=1;zcode=0.0;mark=0
  call AXMAT_WHITE_CONFIGURE(.false.,mark,0.d0,nr,nz,nsnap,na,nl,1,info)
  if(info/=0) stop 103
  do z=1,nz
    mat1d(z)=(z-1)/16+1
    do i=1,nr
      mat(z,i)=i
    enddo
  enddo
  open(newunit=u,file='interface_controls.bin',access='stream',form='unformatted',status='new')
  write(u) 'AXSFI001',int([14,na,nz,nr,nl],int32)
  do e=1,2
    do p=1,7
      do l=1,nl
        call new_source(e,'SPOT',1,l-1,2,0.125,8.d0*c(l,p),0.d0,coeff(l))
      enddo
      do i=1,nr
        do z=1,nz
          do l=1,nl
            qext(1,l,z,i)=real(basis(i,1),real64)*coeff(l)
          enddo
        enddo
      enddo
      call SPOT1P64_CACHE_BEGIN(1,.false.)
      call SPOT1P64(1,nr,nz,1,nmat,nsnap,1,1,na,nl,.false., &
        mat1d,vol1d,mat,total,sgas,basis,vol2d,radial,ncode,zcode,qext,du,w,pl,flux,cour,xnei)
      call SPOT1P64_CACHE_CLEAR()
      write(u) int([e,p],int32),coeff,flux,cour,xnei
    enddo
  enddo
  close(u)
  print '(A)', 'AXMAT-SOURCEFACTOR-CONTROLS-RETURNED'
contains
__EXTRACTED_PRODUCTION_SUBROUTINES__
end program source_factor_controls
"""


def control_source(original, candidate):
    if original.count(OLD_BLOCK) != 2 or candidate.count(NEW_BLOCK) != 2:
        raise ValueError("both literal production source blocks required for compiled extraction")
    routines = []
    for role, text, block in (("old", original, OLD_BLOCK), ("new", candidate, NEW_BLOCK)):
        positions = list(re.finditer(re.escape(block), text))
        routine = [f"  subroutine {role}_source(entry,CXDOOR,NDIM,IAL,JG,xs,phi,seed,result)",
            "    integer,intent(in) :: entry,NDIM,IAL,JG",
            "    character(*),intent(in) :: CXDOOR",
            "    real(real32),intent(in) :: xs",
            "    real(real64),intent(in) :: phi,seed",
            "    real(real64),intent(out) :: result",
            "    integer :: IND,IG,IBM,JND,IPOS(1)",
            "    real(real32) :: XSCAT(1)", "    real(real64) :: FLUX(1,2,8)",
            "    IND=1;IG=1;IBM=1;JND=1;IPOS=1;XSCAT=xs;FLUX=0.d0",
            "    FLUX(IND,JG,7)=phi;FLUX(IND,IG,8)=seed", "    select case(entry)"]
        for i, match in enumerate(positions, 1):
            routine.extend([f"    case({i})", fixed_to_free(text[match.start():match.end()])])
        routine.extend(["    case default", "      stop 104", "    end select",
                        "    result=FLUX(IND,IG,8)", f"  end subroutine {role}_source"])
        routines.append("\n".join(routine))
    return CONTROL_PROGRAM.replace("__EXTRACTED_PRODUCTION_SUBROUTINES__", "\n".join(routines))


def production_contract(production):
    """Freeze future trial dependencies without constructing a coupled trial."""
    info = production.verify_prepared(PROD / "prepared.json", PREPARED_SHA)
    require(SOURCE / "case_spec.json", SPEC_SHA)
    recipe_path = require(SOURCE / "refined_reference_analysis_recipe.json", RECIPE_SHA)
    recipe = read(recipe_path)
    producer_environment = read(require(SOURCE / "analysis_environment.json"))
    verify(producer_environment["files"])
    if (producer_environment["python_version"] != "3.14.4"
            or producer_environment["numpy_version"] != "2.4.4"):
        raise ValueError("original exact producer/ingestion analysis environment differs")
    pins = [recipe[key] for key in ("reference_execution", "complete_independent_native_sample",
        "original_candidate_assessment", "observation_projection_recipe", "projection_precheck",
        "native_export_source_proof", "physical_input_precheck")]
    pins += list(recipe["unchanged_reference_implementations"].values())
    for pin in pins:
        require(pin["path"], pin["sha256"])
    execution = read(recipe["reference_execution"]["path"])
    if (set(recipe["original_eight_checks"]) != set(GATES)
            or recipe["fixed_history"] != dict(inactive_batches=100, active_batches=2000,
                particles_per_generation=10000, generations_per_batch=10, first_active=101,
                last_active=2100, raw_generation_entries=21000, batched_generation_entries=2100)):
        raise ValueError("unchanged original eight gates and complete 2000-batch history required")
    native = read(recipe["complete_independent_native_sample"]["path"])
    if (native["status"] != "NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS"
            or native["returncode"] != 0 or native["error"] is not None):
        raise ValueError("retained complete native CE sample required")
    sample_root = Path(recipe["complete_independent_native_sample"]["path"]).parent
    verify({str(sample_root / name): sha for name, sha in native["outputs"].items()})
    statepoints = [f"statepoint.{batch:04d}.h5" for batch in range(101, 2101)]
    actual_statepoints = {name for name in native["outputs"]
                         if name.startswith("statepoint.") and name.endswith(".h5")}
    if len(actual_statepoints) != 2000 or actual_statepoints != set(statepoints):
        raise ValueError("complete original 2000 consecutive active statepoints required")
    return dict(schema="AXMAT_SOURCEFACTOR_FUTURE_COUPLED_CONTRACT_V1",
        original_prepared=dict(path=str(PROD / "prepared.json"), sha256=PREPARED_SHA),
        case_spec=dict(path=str(SOURCE / "case_spec.json"), sha256=SPEC_SHA),
        scientific_spec=read(SOURCE / "case_spec.json"), production_config=info["production_config"],
        budgets=info["budgets"], inputs=info["inputs"], common_training=dict(
            order=["A", "B", "A"], rank=1, original_archive_root=str(PROD / "archives"),
            original_training_root=str(PROD / "training"), fresh_common_basis_required=True),
        source_factor_changes_only=True, fresh_bootstrap_and_complete_maps_required=True,
        producer_environment=dict(path=str(SOURCE / "analysis_environment.json"),
            sha256=digest(SOURCE / "analysis_environment.json"), python="3.14.4", numpy="2.4.4"),
        reference_analysis_recipe=dict(path=str(recipe_path), sha256=RECIPE_SHA),
        reference_analysis_environment=dict(execution=recipe["reference_execution"],
            interpreter="/Users/wen/miniforge3/envs/openmc-dev/bin/python",
            original_source=str(ROOT / "validation/axial_material/prepare_qualified_AAA_refined_reference_analysis.py"),
            must_use_actual_reference_analysis_interpreter=True,
            producer_and_CE_analysis_environments_are_separate=True),
        retained_reference=dict(native=recipe["complete_independent_native_sample"],
            active_batches=2000, active_statepoints=statepoints, new_CE_transport_required=False),
        mandatory_original_gates=list(GATES), require_all_eight_actual_PASS_before_ABA=True,
        conservative_48_to_12_observation_projection_required=True,
        one_global_nu_fission_normalization_only=True, no_CE_fitting=True,
        pipeline_prepared=False, coupled_qualified=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def environment(declaration, require_build_interpreter=True):
    verify(declaration["files"])
    if (require_build_interpreter
            and str(Path(sys.executable).resolve()) != declaration["build_python_executable"]):
        raise ValueError("declared genuine build/audit interpreter required")
    for name, target in declaration["native_library_aliases"].items():
        if str(Path(name).resolve()) != target:
            raise ValueError("declared native-library alias changed")
    actual = {key: value for key, value in os.environ.items()
              if key.startswith("DYLD_") or key == "OPENBLAS_CORETYPE"}
    expected = {key: value for key, value in declaration["numerical_loader_environment"].items()
                if key.startswith("DYLD_") or key == "OPENBLAS_CORETYPE"}
    if actual != expected:
        raise ValueError("native loader/dispatch environment differs")
    if any(os.environ.get(key) != "1" for key in THREAD_KEYS):
        raise ValueError("one thread required for every admitted child")
    for entry in declaration["preserved_predecessors"]:
        verify_inventory(Path(entry["root"]), entry["inventory"])


def prepare_build(capture_sha):
    """Create one fresh declaration and sources; compile/run nothing."""
    if OUT.exists():
        raise ValueError("fresh source-factor family root required; no resume or overwrite")
    if not capture_sha:
        raise ValueError("explicit completed capture seal SHA256 required")
    capture = capture_admission(capture_sha)
    full, production = modules()
    guard_files = guard_admission(full)
    original = baseline()
    candidate = correct_source(original)
    require(REVIEW, REVIEW_SHA)
    review = read(REVIEW)
    if review["classification"] != "CONFIRMED_COMPILED_INTERGROUP_LEGENDRE_FACTOR_MISMATCH":
        raise ValueError("independent actual binary evidence required")
    for evidence in review["actual_files"].values():
        if "path" in evidence and "sha256" in evidence:
            require(evidence["path"], evidence["sha256"])
    require(ANG / "declaration.json", ANG_DECL_SHA)
    old = read(ANG / "declaration.json")
    verify(old["files"])
    require(ANG / "runtime/Dragon", DRAGON_SHA)
    contract = production_contract(production)
    fixture, fixture_proof = capture_fixture()
    causal = read(require(CAUSAL / "declaration.json"))
    link = list(old["build_commands"][-1])
    expected_chain = [ROOT / "src/DRAGON.o", COMP / "build/SPOR64_A8.o",
        COMP / "build/AXMAT_MCGFCF_COMP.o", ANG / "build/axmat_white_trace_model.o",
        ANG / "build/SPOT1P64.o", COLD / "build/SPOF64.o",
        ROOT / "lib/Darwin_arm64/libDragon.a", ROOT / "Trivac/lib/Darwin_arm64/libTrivac.a",
        ROOT / "Utilib/lib/Darwin_arm64/libUtilib.a", ROOT / "Ganlib/lib/Darwin_arm64/libGanlib.a"]
    if link[5:-2] != list(map(str, expected_chain)) or link[-2] != "-o":
        raise ValueError("actual original full production object/archive link chain differs")
    compiler = str(Path(link[0]).resolve())
    if compiler != link[0]:
        raise ValueError("original compiler must have a canonical frozen path")
    paths = [Path(__file__).resolve(), REVIEW, FULL_SOURCE, Path(production.__file__),
        Path(sys.executable).resolve(), Path(compiler), Path("/bin/ps"), Path("/usr/bin/ar"),
        Path("/usr/bin/git"), *guard_files, *expected_chain, ANG / "build/SPOT1P64.f90",
        ANG / "build/axmat_white_trace_model.f90", ANG / "declaration.json", ANG / "runtime/Dragon",
        PROD / "prepared.json", SOURCE / "case_spec.json", SOURCE / "analysis_environment.json",
        SOURCE / "refined_reference_analysis_recipe.json", CAPTURE / "seal.json",
        ROOT / "validation/axial_material/prepare_qualified_AB_white_trace_refined_production.py",
        ROOT / "validation/axial_material/prepare_qualified_AB_white_trace_refined_environmentpin.py",
        ROOT / "validation/axial_material/prepare_qualified_AAA_refined_reference_analysis.py",
        PROD / "runtime/run_bounded_dragon.py", Path("/Users/wen/miniforge3/envs/openmc-dev/bin/python").resolve()]
    files = dict(old["files"])
    # Capture preparation already co-pinned these exact reused objects.  Its
    # override receiver is different, so separately use the independent actual
    # binary review to bind the original uninstrumented SPOT1P64 object.
    capture_files = read(CAPTURE / "declaration.json")["files"]
    for path in expected_chain:
        if path == ANG / "build/SPOT1P64.o":
            require(path, review["actual_files"]["receiver_object"]["sha256"])
        else:
            require(path, capture_files[str(path)])
    for path in paths:
        files[str(path)] = digest(require(path))
    files.update(read(SOURCE / "analysis_environment.json")["files"])
    for path, sha in causal["files"].items():
        if path.endswith((".dylib", ".so")):
            files[path] = sha
    for folder in (ROOT / "lib/Darwin_arm64/modules", ROOT / "Ganlib/lib/Darwin_arm64/modules", ANG / "build"):
        for path in folder.glob("*.mod"):
            files[str(path)] = digest(path)
    preserved = [dict(root=str(folder), inventory=inventory(folder)) for folder in (PROD, CAUSAL)]
    roots = sorted({str(p.resolve()) for p in ART.glob("axial-material-*") if p.is_dir()}
        | set(causal["resource_roots"]) | set(read(full.OUT / "declaration.json")["resource_roots"])
        | set(read(PROD / "prepared.json")["resource_roots"]) | {str(OUT)})
    resources = production.DiskResources(ART, roots, 8 * 2**30, 96 * 2**30)
    before = resources.check()
    if (before["artifact_bytes"] + ARCHIVE_RESERVE >= 96 * 2**30
            or before["disk_free_bytes"] - ARCHIVE_RESERVE < 8 * 2**30):
        raise ValueError("complete build and control storage admission failed")
    flags = ["-O2", "-march=native", "-ffp-contract=off", "-g", "-fPIC", "-frecord-marker=4",
        "-ffixed-line-length-none", "-I" + str(OUT / "build"), "-I" + str(ANG / "build"),
        "-I" + str(ROOT / "lib/Darwin_arm64/modules"),
        "-I" + str(ROOT / "Ganlib/lib/Darwin_arm64/modules"), "-J" + str(OUT / "build")]
    new_link = link[:-2]
    index = new_link.index(str(ROOT / "lib/Darwin_arm64/libDragon.a"))
    new_link[index:index] = [str(OUT / "build/FLU2DR64.o")]
    new_link += ["-o", str(OUT / "runtime/Dragon")]
    commands = [[compiler, *flags, "-c", str(OUT / "build/FLU2DR64.f"),
        "-o", str(OUT / "build/FLU2DR64.o")], new_link,
        [compiler, *flags, "-c", str(OUT / "build/source_factor_controls.f90"),
         "-o", str(OUT / "build/source_factor_controls.o")],
        [compiler, "-O2", "-march=native", "-ffp-contract=off", "-g",
         str(OUT / "build/source_factor_controls.o"), str(ANG / "build/axmat_white_trace_model.o"),
         str(ANG / "build/SPOT1P64.o"), *map(str, expected_chain[6:]),
         "-o", str(OUT / "runtime/source_factor_controls")]]
    # Check environment and all immutable predecessor inputs before any output.
    admitted = dict(files=files, build_python_executable=str(Path(sys.executable).resolve()),
        preserved_predecessors=preserved, native_library_aliases=causal["native_library_aliases"],
        numerical_loader_environment=causal["numerical_loader_environment"])
    environment(admitted)
    OUT.mkdir(exist_ok=False)
    for name in ("build", "runtime", "controls", "audit", "SOURCEFACTOR_BUILD"):
        (OUT / name).mkdir()
    shutil.copy2(PROD / "runtime/run_bounded_dragon.py", OUT / "runtime/run_bounded_dragon.py")
    (OUT / "build/FLU2DR64.compiled_baseline.f").write_bytes(original.encode())
    (OUT / "build/FLU2DR64.f").write_bytes(candidate.encode())
    (OUT / "build/source_factor_controls.f90").write_text(control_source(original, candidate))
    (OUT / "controls/receiver_fixture.bin").write_bytes(fixture)
    (OUT / "build/FLU2DR64.patch").write_text("".join(difflib.unified_diff(
        original.splitlines(True), candidate.splitlines(True), fromfile="git:" + BASE_REVISION,
        tofile="isolated-SPOT-NDIM1-two-entry-source-factor-correction")))
    write_new(OUT / "source_admission.json", dict(
        schema="AXMAT_SOURCEFACTOR_TWO_ENTRY_SOURCE_ADMISSION_V1", baseline_revision=BASE_REVISION,
        baseline_source_sha256=BASE_SHA, baseline_library_sha256=LIB_SHA,
        baseline_object_sha256=OBJECT_SHA, baseline_runtime_sha256=DRAGON_SHA,
        corrected_source_sha256=digest(OUT / "build/FLU2DR64.f"),
        exact_replacements=[dict(old=OLD_BLOCK, new=NEW_BLOCK, count=2)],
        full_restoration_byte_exact=True, correction_scope=dict(door="SPOT", ndim=1, intergroup_only=True),
        XSDIA_self_reduction_unchanged=True, actual_self_branch_reachable=False, actual_ITPIJ=1,
        actual_binary_review=dict(path=str(REVIEW), sha256=REVIEW_SHA),
        recovered_Git_baseline_complete_original_compilation_identity_proved=False,
        recovered_baseline_actual_370_group_warm_capture_word_exact=True,
        frozen_link_chain=list(map(str, expected_chain)), only_new_override="FLU2DR64.o",
        white_closure_unchanged=True, angle_grid_unchanged=True, physical_data_unchanged=True,
        compiled_control_entries_extracted_from_actual_source=True,
        receiver_fixture=fixture_proof, coupled_accuracy_qualified=False))
    write_new(OUT / "future_coupled_contract.json", contract)
    for path in OUT.rglob("*"):
        if path.is_file():
            files[str(path)] = digest(path)
    write_new(OUT / "declaration.json", dict(
        schema="AXMAT_SOURCEFACTOR_BUILD_DECLARATION_V1", family="SOURCEFACTOR_BUILD", files=files,
        build_commands=commands, build_python_executable=str(Path(sys.executable).resolve()),
        capture_dependency=capture, preserved_predecessors=preserved, resource_roots=roots,
        resources_before=before, min_free_bytes=8 * 2**30, artifact_budget_bytes=96 * 2**30,
        archive_reserve_bytes=ARCHIVE_RESERVE, total_wall_seconds=TOTAL_WALL,
        stage_wall_seconds=STAGE_WALL, rss_cap_mib=RSS_CAP, threads=1, numeric_children_at_once=1, retries=0,
        numeric_environment={key: "1" for key in THREAD_KEYS},
        native_library_aliases=causal["native_library_aliases"],
        numerical_loader_environment=causal["numerical_loader_environment"],
        source_comparison_rows=SOURCE_ROWS,
        source_comparison_scalar_invocations=SOURCE_COMPARISON_SCALAR_CALLS,
        interface_source_scalar_invocations=INTERFACE_SOURCE_SCALAR_CALLS,
        source_control_rows=SOURCE_ROWS, actual_receiver_calls=INTERFACE_CALLS,
        receiver_shapes=dict(flux=[1, NL, NZ, NR], cour=[NZ + 1, NR], xnei=[NA, NR]),
        field_relative_limit=FIELD_LIMIT, field_gate_operator="strictly_less_than",
        actual_receiver_object=str(ANG / "build/SPOT1P64.o"),
        production_transport_launched=False, production_pipeline_prepared=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, coefficient_fitting=False))
    print(json.dumps(dict(declaration=str(OUT / "declaration.json"),
                         declaration_sha256=digest(OUT / "declaration.json"))))


def declaration_admission(expected, require_build_interpreter=True):
    if not expected:
        raise ValueError("explicit frozen build declaration SHA256 required")
    declaration = read(require(OUT / "declaration.json", expected))
    if (declaration["schema"] != "AXMAT_SOURCEFACTOR_BUILD_DECLARATION_V1"
            or declaration["family"] != "SOURCEFACTOR_BUILD"
            or declaration["total_wall_seconds"] != TOTAL_WALL
            or declaration["stage_wall_seconds"] != STAGE_WALL
            or declaration["rss_cap_mib"] != RSS_CAP or declaration["threads"] != 1
            or declaration["numeric_children_at_once"] != 1 or declaration["retries"] != 0
            or declaration["artifact_budget_bytes"] != 96 * 2**30
            or declaration["min_free_bytes"] != 8 * 2**30
            or declaration["field_relative_limit"] != FIELD_LIMIT
            or declaration["field_gate_operator"] != "strictly_less_than"
            or declaration["source_control_rows"] != SOURCE_ROWS
            or declaration["source_comparison_rows"] != SOURCE_ROWS
            or declaration["source_comparison_scalar_invocations"] != SOURCE_COMPARISON_SCALAR_CALLS
            or declaration["interface_source_scalar_invocations"] != INTERFACE_SOURCE_SCALAR_CALLS
            or declaration["actual_receiver_calls"] != INTERFACE_CALLS
            or declaration["AAA_accuracy_qualified"] or declaration["ABA_admitted"]):
        raise ValueError("immutable bounded build contract differs")
    environment(declaration, require_build_interpreter=require_build_interpreter)
    if capture_admission(declaration["capture_dependency"]["seal_sha256"]) != declaration["capture_dependency"]:
        raise ValueError("actual completed capture dependency changed")
    return declaration


class Words:
    def __init__(self, path):
        self.stream = require(path).open("rb")

    def bytes(self, count):
        raw = self.stream.read(count)
        if len(raw) != count:
            raise ValueError("truncated actual compiled control archive")
        return raw

    def values(self, code, count):
        return list(struct.unpack("<" + str(count) + code,
                                self.bytes(struct.calcsize("<" + code) * count)))

    def end(self):
        trailing = self.stream.read(1)
        self.stream.close()
        if trailing:
            raise ValueError("unexpected compiled archive trailing words")


def real32(value):
    return struct.unpack("<f", struct.pack("<f", value))[0]


def source_audit():
    archive = Words(OUT / "controls/source_controls.bin")
    if archive.bytes(8) != b"AXSFU001" or archive.values("i", 1) != [SOURCE_ROWS]:
        raise ValueError("actual complete source control schema differs")
    expected_indices = itertools.product(range(1, 3), range(1, 5), range(3),
        range(1, 3), range(1, 3), range(1, 5))
    rows = []
    for expected in expected_indices:
        indices = archive.values("i", 6)
        xs = archive.values("f", 1)[0]
        phi, seed, old, new = archive.values("d", 4)
        e, scope, degree, group_case, xindex, pindex = indices
        if (indices != list(expected) or seed != 0.375
                or xs != [0.125, real32(1 / 7)][xindex - 1]
                or phi != [0.0, 1.0, -0.125, 0.9][pindex - 1]):
            raise ValueError("actual source coordinates/order/primitive values differ")
        # REAL(2*IAL+1)*XSCAT is evaluated in REAL32 before the REAL64 flux
        # multiply; explicitly preserve that original non-SPOT arithmetic.
        old_expected = seed if group_case == 1 else seed + real32((2 * degree + 1) * xs) * phi
        new_expected = seed if group_case == 1 else seed + (
            xs if scope == 1 else real32((2 * degree + 1) * xs)) * phi
        if (not all(math.isfinite(value) for value in (xs, phi, seed, old, new))
                or old != old_expected or new != new_expected
                or (scope != 1 and struct.pack("<d", old) != struct.pack("<d", new))):
            raise ValueError("actual compiled old/new source arithmetic or preserved scope failed")
        rows.append(dict(coordinates=indices, sigma_legendre=xs, raw_flux_moment=phi,
            source_seed=seed, old_source=old, corrected_source=new,
            independent_old_source=old_expected, independent_corrected_source=new_expected))
    archive.end()
    if len(rows) != SOURCE_ROWS:
        raise ValueError("all two-entry source/scattering-order/sign/scope coordinates required")
    return dict(schema="AXMAT_SOURCEFACTOR_COMPILED_SOURCE_CONTROL_V1", status="PASS",
        rows=rows, actual_source_rows=len(rows), actual_source_comparison_rows=len(rows),
        actual_source_comparison_scalar_invocations=2 * len(rows), source_entries=2, degrees=[0, 1, 2],
        scopes=["SPOT/NDIM1", "SPOT/NDIM2", "SPOT/NDIM3", "MCCG/NDIM2"],
        self_group_excluded=True, non_SPOT_or_non_1D_old_arithmetic_byte_exact=True,
        source_relative_error=0.0, actual_archive_sha256=digest(OUT / "controls/source_controls.bin"))


def relative(actual, expected, name):
    if len(actual) != len(expected) or not all(math.isfinite(x) for x in [*actual, *expected]):
        raise ValueError("finite complete interface field required: " + name)
    scale = max(map(abs, expected), default=0.0)
    defect = max((abs(x - y) for x, y in zip(actual, expected)), default=0.0)
    if (scale == 0 and defect != 0) or (scale > 0 and defect / scale >= FIELD_LIMIT):
        raise ValueError("original strict <5e-12 raw receiver field gate failed: " + name)
    return 0.0 if scale == 0 else defect / scale


def interface_audit():
    fixture = Words(OUT / "controls/receiver_fixture.bin")
    if fixture.bytes(8) != b"AXSFF001" or fixture.values("i", 6) != [NA, NZ, NR, NL, NM, NSNAP]:
        raise ValueError("sealed actual receiver primitive fixture differs")
    mu, weights, pl, basis, volume = (fixture.values("f", n) for n in (NA, NA, NL * NA, NR, NR))
    fixture.end()
    if (not all(math.isfinite(x) for x in [*mu, *weights, *pl, *basis, *volume])
            or any(x <= 0 for x in [*weights, *volume]) or any(x == 0 or abs(x) >= 1 for x in mu)
            or len([x for x in mu if x > 0]) != NA // 2
            or any(mu.count(-x) != 1 for x in mu)):
        raise ValueError("complete actual symmetric native primitive coordinates required")
    basis = [real32(2.0 * value) for value in basis]
    radial_weight = [x / sum(volume) for x in volume]
    gram = sum(radial_weight[i] * basis[i] * basis[i] for i in range(NR))
    sigma_mass = sum(radial_weight[i] * basis[i] * 0.0625 * basis[i] for i in range(NR))
    if not gram > 0 or gram == 1.0:
        raise ValueError("actual nonunit positive native rank-one Gram control required")
    coefficients = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.], [1., .01, 0.],
                    [1., -.01, 0.], [1., .01, .005], [1., -.02, .0125]]
    output = Words(OUT / "controls/interface_controls.bin")
    if output.bytes(8) != b"AXSFI001" or output.values("i", 5) != [INTERFACE_CALLS, NA, NZ, NR, NL]:
        raise ValueError("complete actual frozen receiver archive required")
    rows = []
    witnesses_path = OUT / "audit/independent_interface_fields.bin"
    with witnesses_path.open("xb") as witnesses:
        witnesses.write(b"AXSFW001" + struct.pack("<5i", INTERFACE_CALLS, NA, NZ, NR, NL))
        for entry, case in itertools.product(range(1, 3), range(1, 8)):
            if output.values("i", 2) != [entry, case]:
                raise ValueError("all actual two-entry receiver case coordinates required")
            coeff = output.values("d", NL)
            if coeff != coefficients[case - 1]:
                raise ValueError("source producer's actual raw moments differ")
            actual_flux = output.values("d", NL * NZ * NR)
            actual_current = output.values("d", (NZ + 1) * NR)
            actual_xnei = output.values("d", NA * NR)
            projected = [sum(radial_weight[i] * basis[i] * (basis[i] * coeff[l])
                             for i in range(NR)) for l in range(NL)]
            cells = [[0.] * NZ for _ in range(NA)]
            faces = [[0.] * (NZ + 1) for _ in range(NA)]
            angular_source = [sum(.5 * (2 * l + 1) * pl[l + NL * n] * projected[l]
                                  for l in range(NL)) for n in range(NA)]
            for n in range(NA):
                order = range(NZ) if mu[n] > 0 else range(NZ - 1, -1, -1)
                inflow = 0.
                for z in order:
                    outflow = ((abs(mu[n]) * gram - .0625 * sigma_mass) * inflow
                               + .125 * angular_source[n]) / (abs(mu[n]) * gram + .0625 * sigma_mass)
                    cells[n][z] = .5 * (inflow + outflow)
                    faces[n][z + 1 if mu[n] > 0 else z] = outflow
                    inflow = outflow
            modal = [[sum(weights[n] * pl[l + NL * n] * cells[n][z] for n in range(NA))
                      for z in range(NZ)] for l in range(NL)]
            current = [sum(weights[n] * mu[n] * faces[n][z] for n in range(NA))
                       for z in range(NZ + 1)]
            expected_flux = [basis[i] * modal[l][z] for i in range(NR) for z in range(NZ) for l in range(NL)]
            expected_current = [basis[i] * current[z] for i in range(NR) for z in range(NZ + 1)]
            expected_xnei = [basis[i] * faces[n][0] for i in range(NR) for n in range(NA)]
            # Publish this complete independent witness before any field or
            # vacuum gate, so a failed row retains its unrepaired expectations.
            witnesses.write(struct.pack("<2i", entry, case))
            for field in (projected, angular_source, [x for row in cells for x in row],
                          [x for row in faces for x in row], expected_flux, expected_current, expected_xnei):
                witnesses.write(struct.pack("<" + str(len(field)) + "d", *field))
            witnesses.flush()
            errors = dict(flux=relative(actual_flux, expected_flux, "flux"),
                cour=relative(actual_current, expected_current, "cour"),
                xnei=relative(actual_xnei, expected_xnei, "xnei"))
            if any(actual_xnei[n + NA * i] != 0.0 for i in range(NR) for n in range(NA) if mu[n] > 0):
                raise ValueError("actual bottom vacuum inflow must be strictly zero")
            rows.append(dict(entry=entry, case=case, raw_legendre_coefficients=coeff,
                projected_source_moments=projected, raw_gram=gram, total_mass=sigma_mass,
                complete_field_relative_errors=errors, exact_bottom_vacuum_inflow=True,
                field_entries=dict(flux=len(actual_flux), cour=len(actual_current), xnei=len(actual_xnei))))
    output.end()
    return dict(schema="AXMAT_SOURCEFACTOR_FROZEN_RECEIVER_INTERFACE_CONTROL_V1", status="PASS",
        actual_calls=len(rows), actual_native_receiver_calls=len(rows),
        actual_interface_source_scalar_invocations=NL * len(rows), rows=rows,
        native_Gram_is_nonunit=True, field_relative_limit=FIELD_LIMIT, field_gate_operator="strictly_less_than",
        actual_archive_sha256=digest(OUT / "controls/interface_controls.bin"),
        independent_fields_sha256=digest(witnesses_path), independent_angular_coordinates=[NA, NZ],
        receiver_object_sha256=digest(ANG / "build/SPOT1P64.o"),
        source_contract="Raw phi_l=sum_n w_n*P_l*psi_n; receiver reconstructs (2*l+1)/2 once.",
        fixture_only=True, continuous_BVP_qualified=False, physical_balance_qualified=False)


def audit_build(expected):
    declaration = declaration_admission(expected)
    claim = read(OUT / "execution_claim.json")
    stages = read(OUT / "SOURCEFACTOR_BUILD/stages.json")["stages"]
    if (claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected
            or len(stages) != 6 or [stage["label"] for stage in stages] != list(LABELS)
            or any(stage["status"] != "PASS" for stage in stages[:-1])
            or stages[-1]["status"] != "RUNNING"
            or stages[-1]["command"] != [sys.executable, *sys.argv]):
        raise ValueError("actual own-parent final audit with five completed stages required")
    expected_commands = [*declaration["build_commands"], [str(OUT / "runtime/source_factor_controls")],
        [sys.executable, str(Path(__file__).resolve()), "audit-build", "--sha256", expected]]
    if [stage["command"] for stage in stages] != expected_commands:
        raise ValueError("actual complete source-factor build/control command identities differ")
    previous_watch = [check_watch(OUT, stage) for stage in stages[:-1]]
    receipt = read(OUT / "raw_controls_receipt.json")
    if set(receipt["files"]) != {"controls/source_controls.bin", "controls/interface_controls.bin"}:
        raise ValueError("both actual raw returned control archives required")
    verify({str(OUT / path): sha for path, sha in receipt["files"].items()})
    identity = read(OUT / "runtime/build_identity.json")
    verify({str(OUT / path): sha for path, sha in identity["files"].items()})
    if (set(identity["files"]) != {"runtime/Dragon", "runtime/source_factor_controls",
            "build/FLU2DR64.o", "build/source_factor_controls.o"}
            or identity["files"]["runtime/Dragon"] == DRAGON_SHA):
        raise ValueError("actual newly compiled corrected runtime and controls required")
    original = (OUT / "build/FLU2DR64.compiled_baseline.f").read_text()
    candidate = (OUT / "build/FLU2DR64.f").read_text()
    if (hashlib.sha256(original.encode()).hexdigest() != BASE_SHA
            or candidate != correct_source(original)
            or (OUT / "build/source_factor_controls.f90").read_text() != control_source(original, candidate)):
        raise ValueError("actual build source and extracted compiled controls differ")
    source = source_audit()
    write_new(OUT / "audit/source_controls.json", source)
    interface = interface_audit()
    write_new(OUT / "audit/interface_controls.json", interface)
    write_new(OUT / "audit/result.json", dict(
        classification="PASS_SOURCEFACTOR_COMPILED_SOURCE_AND_RECEIVER_CONTROLS_ONLY",
        declaration_sha256=expected, capture_dependency=declaration["capture_dependency"],
        actual_source_rows=source["actual_source_rows"],
        actual_source_comparison_rows=source["actual_source_comparison_rows"],
        actual_source_comparison_scalar_invocations=source["actual_source_comparison_scalar_invocations"],
        actual_interface_source_scalar_invocations=interface["actual_interface_source_scalar_invocations"],
        actual_receiver_calls=interface["actual_calls"],
        source_control_status=source["status"], interface_control_status=interface["status"],
        previous_stage_watchdogs=previous_watch, compiled_identity_sha256=digest(OUT / "runtime/build_identity.json"),
        full_source_restoration_byte_exact=True, actual_original_receiver_linked=True,
        scientific_scope="Compiled source arithmetic and synthetic production receiver interface only.",
        production_transport_launched=False, production_pipeline_prepared=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, coefficient_fitting=False))
    print("AXMAT-SOURCEFACTOR-BUILD-AUDITED")


def run_build(expected):
    started = time.monotonic()
    declaration = declaration_admission(expected)
    full, production = modules()
    guard_admission(full)
    resources = production.DiskResources(ART, declaration["resource_roots"],
        declaration["min_free_bytes"], declaration["artifact_budget_bytes"])
    before = resources.check()
    if (before["artifact_bytes"] + ARCHIVE_RESERVE >= declaration["artifact_budget_bytes"]
            or before["disk_free_bytes"] - ARCHIVE_RESERVE < declaration["min_free_bytes"]):
        raise ValueError("current complete build storage admission failed")
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected,
        started_unix=time.time(), started_monotonic=started, retries=0))
    remaining = TOTAL_WALL - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError("bounded family admission exhausted the total wall budget")
    runner = full.OwnRSSSerialExecutor(OUT, remaining, "SOURCEFACTOR_BUILD", resources)
    result = dict(classification="FAILED_SOURCEFACTOR_BUILD_NO_RETRY", error=None,
        AAA_accuracy_qualified=False, ABA_admitted=False, production_transport_launched=False,
        production_pipeline_prepared=False)
    try:
        for i, command in enumerate(declaration["build_commands"]):
            # Bind inputs before every compiler/link child; preserving all old
            # output namespaces is part of the actual execution contract.
            environment(declaration)
            runner.execute(OUT / "build", f"build_{i:02d}", command, STAGE_WALL)
        identity_paths = [OUT / path for path in ("runtime/Dragon", "runtime/source_factor_controls",
            "build/FLU2DR64.o", "build/source_factor_controls.o")]
        write_new(OUT / "runtime/build_identity.json", dict(
            files={str(path.relative_to(OUT)): digest(require(path)) for path in identity_paths},
            genuine_frozen_link_chain=True, only_production_override="FLU2DR64.o"))
        environment(declaration)
        runner.execute(OUT / "controls", "controls", [str(OUT / "runtime/source_factor_controls")],
            STAGE_WALL, "AXMAT-SOURCEFACTOR-CONTROLS-RETURNED")
        # Keep both raw archives before any numerical acceptance gate.
        write_new(OUT / "raw_controls_receipt.json", dict(files={str(path.relative_to(OUT)): digest(require(path))
            for path in (OUT / "controls/source_controls.bin", OUT / "controls/interface_controls.bin")}))
        runner.execute(OUT / "audit", "audit", [sys.executable, str(Path(__file__).resolve()),
            "audit-build", "--sha256", expected], STAGE_WALL, "AXMAT-SOURCEFACTOR-BUILD-AUDITED")
        stages = read(OUT / "SOURCEFACTOR_BUILD/stages.json")["stages"]
        if (len(stages) != 6 or [stage["label"] for stage in stages] != list(LABELS)
                or any(stage["status"] != "PASS" for stage in stages)):
            raise ValueError("four builds, actual compiled controls and final audit must all complete")
        result["watchdogs"] = [check_watch(OUT, stage) for stage in stages]
        audit = read(OUT / "audit/result.json")
        if (audit["classification"] != "PASS_SOURCEFACTOR_COMPILED_SOURCE_AND_RECEIVER_CONTROLS_ONLY"
                or audit["actual_source_rows"] != SOURCE_ROWS or audit["actual_receiver_calls"] != INTERFACE_CALLS
                or audit["actual_source_comparison_rows"] != SOURCE_ROWS
                or audit["actual_source_comparison_scalar_invocations"] != SOURCE_COMPARISON_SCALAR_CALLS
                or audit["actual_interface_source_scalar_invocations"] != INTERFACE_SOURCE_SCALAR_CALLS
                or audit["source_control_status"] != "PASS" or audit["interface_control_status"] != "PASS"
                or audit["AAA_accuracy_qualified"] or audit["ABA_admitted"]):
            raise ValueError("actual complete source/interface PASS required")
        if time.monotonic() - started >= TOTAL_WALL:
            raise ValueError("complete family exceeded total wall limit")
        size = sum(path.stat().st_size for path in OUT.rglob("*") if path.is_file() and not path.is_symlink())
        if size >= ARCHIVE_RESERVE:
            raise ValueError("complete bounded build archive exceeded admission reserve")
        result.update(classification="COMPLETE_SOURCEFACTOR_BUILD_AND_INTERFACE_CONTROLS_ONLY",
            actual_source_rows=SOURCE_ROWS, actual_receiver_calls=INTERFACE_CALLS,
            actual_source_comparison_rows=SOURCE_ROWS,
            actual_source_comparison_scalar_invocations=SOURCE_COMPARISON_SCALAR_CALLS,
            actual_interface_source_scalar_invocations=INTERFACE_SOURCE_SCALAR_CALLS,
            runtime_sha256=digest(OUT / "runtime/Dragon"), actual_archive_bytes_before_closeout=size)
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        try:
            environment(declaration)
            result["resources"] = resources.check()
        except BaseException as error:
            result.update(classification="FAILED_SOURCEFACTOR_BUILD_NO_RETRY", error=repr(error),
                          elapsed_seconds=time.monotonic() - started)
            write_new(OUT / "driver_result.json", result)
            raise
        result["elapsed_seconds"] = time.monotonic() - started
        if result["error"] is None and result["elapsed_seconds"] >= TOTAL_WALL:
            result.update(classification="FAILED_SOURCEFACTOR_BUILD_NO_RETRY",
                          error="complete build including final immutable-input checks exceeded total wall cap")
            write_new(OUT / "driver_result.json", result)
            raise ValueError(result["error"])
        write_new(OUT / "driver_result.json", result)
    write_new(OUT / "seal.json", dict(schema="AXMAT_SOURCEFACTOR_BUILD_SEAL_V1",
        files={str(path.relative_to(OUT)): digest(path) for path in OUT.rglob("*") if path.is_file()}))
    print(json.dumps(result, allow_nan=False))


def production_admission(build_seal_sha):
    """Future factory dependency: actual completed controls; never launch ABA."""
    seal = read(require(OUT / "seal.json", build_seal_sha))
    if seal["schema"] != "AXMAT_SOURCEFACTOR_BUILD_SEAL_V1":
        raise ValueError("actual bounded source-factor build seal required")
    actual = {str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file()}
    if actual != set(seal["files"]) | {"seal.json"}:
        raise ValueError("exact complete build seal namespace required")
    verify({str(OUT / path): sha for path, sha in seal["files"].items()})
    result = read(OUT / "driver_result.json")
    audit = read(OUT / "audit/result.json")
    if (result["classification"] != "COMPLETE_SOURCEFACTOR_BUILD_AND_INTERFACE_CONTROLS_ONLY"
            or result["error"] is not None
            or result["actual_source_rows"] != SOURCE_ROWS or result["actual_receiver_calls"] != INTERFACE_CALLS
            or result["actual_source_comparison_rows"] != SOURCE_ROWS
            or result["actual_source_comparison_scalar_invocations"] != SOURCE_COMPARISON_SCALAR_CALLS
            or result["actual_interface_source_scalar_invocations"] != INTERFACE_SOURCE_SCALAR_CALLS
            or audit["source_control_status"] != "PASS" or audit["interface_control_status"] != "PASS"
            or result["AAA_accuracy_qualified"] or result["ABA_admitted"]):
        raise ValueError("actual completed source/interface controls, with limited scope, required")
    declaration = read(OUT / "declaration.json")
    # Inspection by the producer's separately pinned Python3.14 environment is
    # allowed; that does not change the interpreter used for build/audit stages.
    declaration_admission(digest(OUT / "declaration.json"), require_build_interpreter=False)
    stages = read(OUT / "SOURCEFACTOR_BUILD/stages.json")["stages"]
    if len(stages) != 6 or any(stage["status"] != "PASS" for stage in stages):
        raise ValueError("all six actual build/control/audit stages required")
    for stage in stages:
        check_watch(OUT, stage)
    source = read(OUT / "source_admission.json")
    if (source["white_closure_unchanged"] is not True or source["angle_grid_unchanged"] is not True
            or source["physical_data_unchanged"] is not True
            or source["XSDIA_self_reduction_unchanged"] is not True
            or source["correction_scope"] != dict(door="SPOT", ndim=1, intergroup_only=True)):
        raise ValueError("original physical inputs, receiver and exact source-only scope required")
    return dict(schema="AXMAT_SOURCEFACTOR_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1",
        build_root=str(OUT), build_seal_sha256=build_seal_sha,
        corrected_runtime=dict(path=str(OUT / "runtime/Dragon"), sha256=digest(OUT / "runtime/Dragon")),
        capture_dependency=declaration["capture_dependency"],
        source_admission=dict(path=str(OUT / "source_admission.json"), sha256=digest(OUT / "source_admission.json")),
        source_and_receiver_controls=dict(actual_source_rows=SOURCE_ROWS, actual_receiver_calls=INTERFACE_CALLS,
            actual_source_comparison_rows=SOURCE_ROWS,
            actual_source_comparison_scalar_invocations=SOURCE_COMPARISON_SCALAR_CALLS,
            actual_interface_source_scalar_invocations=INTERFACE_SOURCE_SCALAR_CALLS,
            source=dict(path=str(OUT / "audit/source_controls.json"), sha256=digest(OUT / "audit/source_controls.json")),
            receiver=dict(path=str(OUT / "audit/interface_controls.json"), sha256=digest(OUT / "audit/interface_controls.json"))),
        white_closure_unchanged=True, collision_self_operator_unchanged=True,
        angle_grid_unchanged=True, physical_data_unchanged=True,
        future_contract=read(OUT / "future_coupled_contract.json"),
        admission="SOURCEFACTOR_RUNTIME_INPUT_ONLY", production_pipeline_prepared=False,
        AAA_accuracy_qualified=False, ABA_admitted=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare-build", "run-build", "audit-build"))
    parser.add_argument("--capture-seal-sha256")
    parser.add_argument("--sha256")
    args = parser.parse_args()
    {"prepare-build": lambda: prepare_build(args.capture_seal_sha256),
     "run-build": lambda: run_build(args.sha256),
     "audit-build": lambda: audit_build(args.sha256)}[args.action]()
