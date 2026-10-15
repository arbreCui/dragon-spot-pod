"""Prepare an isolated MOMENT_ORDER_BUILD; never launch transport.

The successful source-factor build remains an immutable dependency. Only a
private FLU.o is newly compiled for the production executable: SPOT's angular
selector uses TRACK slots 15/16 and clamps NANIS to NANI-1. A separate, explicit
observer prints the actual NLF/NANI/NANIS/NFUNL/NLIN before dispatch. All other
FLU source bytes restore to the recovered Git baseline. Synthetic extracted
selector/producer controls and actual object/executable instruction checks
admit a runtime input, not a coupled solution or an accuracy qualification.

No import-time file reads, compilation, tests or numerical work occur here.
Prepare/run/audit require future explicit CLI invocation after source review.
"""

import argparse
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
import stat
import struct
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
SOURCE = ART / "axial-material-qualified-AB-moment-order-build-admission-20261006"
OUT = ART / "axial-material-moment-order-build-20261006"
TERMINAL = ART / "axial-material-qualified-AB-moment-order-build-terminal-20261006"
PARENT = ART / "axial-material-source-factor-build-20261006"
PARENT_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_production.py"
PARENT_FACTORY_SHA = "619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743"
PARENT_SEAL = "2a005852d49e4929e05b6835d5b8a51f9ce68afb6f15fc665fb5e7bd7547ed1e"
PARENT_RUNTIME_SHA = "b346f5cef9482dd350f5f7fc749809fc2572603db655d88ea24c22d1e8f56a83"
PARENT_SENDER_OBJECT_SHA = "46431a2490c23b28a91b49eaf455b28a59ed2c64e10523b2fc3985df8a595458"
PARENT_SENDER_SOURCE_SHA = "15b0a314886ed224204a53dc77e52fe79114ef00eee81230f80d28eaed4a8316"
REVIEW = ROOT / "validation/axial_material/production_moment_order_binary_review.json"
REVIEW_SHA = "86a1556f5759bb9475ca0cc40b31cd50031fee78f23eb684cb5dd3dc1730c41a"
RESOURCE_SPEC = ART / "axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json"
RESOURCE_SPEC_SHA = "8c2297533ff582e81cef6430947a0557e921830304673a6a8a6c0149fd7a33ae"
RESOURCE_ADDENDUM = RESOURCE_SPEC.with_name("resource_addendum.json")
RESOURCE_ADDENDUM_SHA = "b68ca3ee2802b69900c5085757898872a220de4f038ab9cd14cb4287b9c5fd15"
BASE_REVISION = "299546c405a47f7e3a7f75af54d392492d649781"
BASE_SHA = "0c52238090466f19d865a26167a1511b803eeced85de3da9adf35df86ac627e2"
CURRENT_SHA = "b002f499eced15e9aceea1538fe5802d2dc70e66a0c54bf30d6a71997ae6a94b"
BASE_OBJECT_SHA = "f49eb5e85038277d2bdc393db6599c41a990e91205553af198779cfad2167493"
LIB_SHA = "954ed8568c59fdfc3ee566d027abac35c7a1469436afb0b147e4db7a7f28a1d9"
TOTAL_WALL, STAGE_WALL, RSS_CAP = 1800, 600, 512
ARCHIVE_RESERVE = 2 * 2**30
FAMILY = "MOMENT_ORDER_BUILD"
LABELS = ("build/build_00", "build/build_01", "build/build_02", "build/build_03",
          "controls/controls", "audit/audit")
OBSERVER_PREFIX = "AXMAT-MOMENT-ORDER SELECTOR "
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
OLD_SELECTOR = ("      ELSE IF(CXDOOR.EQ.'SPOT') THEN\n"
                "         NLF=ISTATE(9)\n"
                "         NANI=MAX(1,ISTATE(10))")
NEW_SELECTOR = ("      ELSE IF(CXDOOR.EQ.'SPOT') THEN\n"
                "*        9/10 ARE THE SPATIAL ELEMENT/SCHEME, NOT ANGULAR ORDERS.\n"
                "         NLF=ISTATE(15)\n"
                "         NANI=MAX(1,ISTATE(16))\n"
                "         NANIS=MIN(NANIS,NANI-1)")
OBSERVER_ANCHOR = ("         CALL LCMGET(IPTRK,'KEYFLX',KEYFLX)\n"
                   "      ENDIF\n"
                   "      CALL LCMLEN(IPTRK,'TITLE',ILNLCM,ITYLCM)")
OBSERVER = ("      IF(CXDOOR.EQ.'SPOT') WRITE(IOUT,'(A,5(I8,1X))')\n"
            "     1 'AXMAT-MOMENT-ORDER SELECTOR ',NLF,NANI,NANIS,NFUNL,NLIN\n")
CONTROL_CASES = (
    ("SPOT", 2, 3, {}), ("SPOT", 8, 3, {}),
    ("SPOT", 2, 3, {16: 1}), ("SPOT", 2, 3, {16: 0}),
    ("SPOT", 2, 3, {15: 2}), ("SPOT", 2, 3, {15: 4}),
    ("MCCG", 2, 3, {}), ("BIVAC", 2, 3, {}),
    ("TRIVAC", 2, 3, {}), ("SN", 2, 3, {}), ("OTHER", 2, 3, {}),
    ("SPOT", 2, 3, {15: 0}), ("SPOT", -1, 3, {}), ("SPOT", 2, 1, {}))
ROWS = len(CONTROL_CASES) * 2 * 4
SELECTOR_CALLS = 2 * ROWS
SOURCE_CALLS = 192
PHIS = (0.0, 1.0, -0.125, 0.9)
TERMINAL_SCHEMA = "AXMAT_MOMENT_ORDER_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
TAIL_FIELDS = ("actual_tail_check", "actual_elapsed_seconds", "actual_archive_bytes", "actual_resources")
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"


class DynamicHistoryFailure(RuntimeError):
    def __init__(self, snapshot):
        self.snapshot = snapshot
        super().__init__("FAIL_RESOURCE: " + snapshot["reason"])


def history_roots(declared, artifacts_root):
    """Keep all declared extras and current axial-family roots; reject aliases."""
    artifacts_root = Path(artifacts_root)
    return sorted(set(declared) | {str(p) for pattern in ("axial-material-*",)
        for p in artifacts_root.glob(pattern)})


def resource_scope_contract():
    spec = read(require(RESOURCE_SPEC, RESOURCE_SPEC_SHA))
    addendum = read(require(RESOURCE_ADDENDUM, RESOURCE_ADDENDUM_SHA))
    notes = ("Caps are limits, not runtime promises. Existing material/native jobs retain their separate "
        "already-declared supervisors and caps. Routine implementation/debug fixes may be tested in new "
        "directories; no overwrite or numerical gate relaxation.")
    if (spec["resource_caps"]["notes"] != notes or spec["resource_caps"]["new_case_artifact_budget_GiB"] != 96
            or spec["resource_caps"]["disk_min_free_GiB"] != 8
            or spec["conditional_white_trace_trial"]["resource_addendum"] != dict(
                path=str(RESOURCE_ADDENDUM), sha256=RESOURCE_ADDENDUM_SHA)
            or addendum["new_storage_budget_GiB"] != 96 or addendum["min_free_GiB"] != 8
            or any(Path(root).parent != ART or not Path(root).name.startswith("axial-material-")
                for root in addendum["resources_before"]["resource_roots"])):
        raise ValueError("actual inherited axial-family96GiB/global-disk8GiB scope required")
    return dict(schema="AXMAT_INHERITED_AXIAL_FAMILY_RESOURCE_SCOPE_V1",
        case_spec=dict(path=str(RESOURCE_SPEC), sha256=RESOURCE_SPEC_SHA),
        resource_addendum=dict(path=str(RESOURCE_ADDENDUM), sha256=RESOURCE_ADDENDUM_SHA),
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        artifact_bytes_scope="All explicit declared roots plus current direct axial-material experiment-family roots",
        all_declared_extras_retained=True, entire_project_artifact_cap_claimed=False,
        existing_material_native_jobs_retain_separate_declared_supervisors_and_caps=True,
        native_readonly_dependency_pins_are_not_a_project_wide_storage_scope=True,
        free_disk_floor_applies_to_entire_filesystem=True, artifact_budget_GiB=96, min_free_GiB=8)


def validate_history_roots(values, artifacts_root):
    base = Path(artifacts_root).resolve(strict=True)
    if not isinstance(values, list) or not values:
        raise ValueError("explicit complete-history resource roots required")
    roots = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError("resource roots must be absolute directory paths")
        path = Path(value)
        if (not path.is_absolute() or ".." in path.parts or path == base or not path.is_relative_to(base)):
            raise ValueError("resource roots must be strict validation/artifacts descendants")
        cursor = path
        while cursor != base:
            if cursor.is_symlink() or (cursor.exists() and not cursor.is_dir()):
                raise ValueError("resource root or ancestor is a symlink/non-directory")
            cursor = cursor.parent
        if any(path == old or path.is_relative_to(old) or old.is_relative_to(path) for old in roots):
            raise ValueError("resource roots overlap or repeat")
        roots.append(path)
    return roots


class DynamicHistoryResources:
    """Original apparent-byte/no-follow accounting with a dynamic root union.

    This is an explicit resource-only addition, not a claim that the original
    DiskResources AST is unchanged. A caller can retain its original failure
    type; read-only admission does not import a canonical production controller.
    """
    def __init__(self, artifacts_root, roots, min_free_bytes, max_bytes, failure_type=None):
        self.artifacts_root = Path(artifacts_root)
        self.declared_roots = list(roots)
        validate_history_roots(self.declared_roots, self.artifacts_root)
        if min_free_bytes != 8 * 2**30 or max_bytes != 96 * 2**30:
            raise ValueError("unchanged complete-history96GiB/free8GiB caps required")
        self.min_free_bytes, self.max_bytes = min_free_bytes, max_bytes
        self.failure_type = failure_type or DynamicHistoryFailure
        self.latest = None

    def check(self):
        snapshot = dict(checked_unix=time.time(), min_free_bytes=self.min_free_bytes,
            artifact_budget_bytes=self.max_bytes, declared_resource_roots=list(self.declared_roots),
            resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=resource_scope_contract())
        try:
            roots = validate_history_roots(history_roots(self.declared_roots, self.artifacts_root),
                self.artifacts_root)
            snapshot["resource_roots"] = [str(p) for p in roots]
            total, count, stack = 0, 0, list(roots)
            while stack:
                directory = stack.pop()
                try:
                    descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try:
                        with os.scandir(descriptor) as entries:
                            for entry in entries:
                                try:
                                    item = entry.stat(follow_symlinks=False)
                                except FileNotFoundError:
                                    continue
                                if stat.S_ISDIR(item.st_mode):
                                    stack.append(directory / entry.name)
                                elif stat.S_ISREG(item.st_mode):
                                    total += item.st_size
                                    count += 1
                    finally:
                        os.close(descriptor)
                except FileNotFoundError:
                    continue
            # Refuse a root that appeared during this traversal. A subsequent
            # check may include it, but this check must not report a false PASS.
            if snapshot["resource_roots"] != history_roots(self.declared_roots, self.artifacts_root):
                raise ValueError("complete-history root set changed during resource observation")
            validate_history_roots(snapshot["resource_roots"], self.artifacts_root)
            snapshot.update(artifact_bytes=total, regular_files=count,
                disk_free_bytes=shutil.disk_usage(self.artifacts_root).free)
            self.latest = snapshot
            reasons = []
            if snapshot["disk_free_bytes"] < self.min_free_bytes:
                reasons.append("free disk space below declared minimum")
            if total > self.max_bytes:
                reasons.append("complete history regular-file total exceeds declared artifact budget")
            if reasons:
                snapshot["reason"] = "; ".join(reasons)
                raise self.failure_type(snapshot)
            return snapshot
        except self.failure_type:
            raise
        except (OSError, ValueError) as error:
            snapshot["reason"] = "cannot verify complete dynamic resource scope: " + str(error)
            self.latest = snapshot
            raise self.failure_type(snapshot) from error


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, expected=None):
    path = Path(path)
    if path.is_symlink() or not path.is_file() or (expected is not None and digest(path) != expected):
        raise ValueError("missing, symlink or changed declared file: " + str(path))
    return path


def write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def terminal_contract(python):
    """Only Root records the real tool terminal return; this code consumes it."""
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / "terminal_return.json"),
        record_producer="root", full_stdout_is_retained=True, actual_tool_exit_zero_required=True,
        record_written_after_actual_terminal_return_required=True, tail_fields=list(TAIL_FIELDS),
        resource_scope_policy=HISTORY_SCOPE_POLICY, tail_roots_are_dynamic_union=True,
        resource_scope_contract=resource_scope_contract(),
        actual_run_command=[python, str(Path(__file__).resolve()), "run-build", "--sha256", "__DECLARATION_SHA256__"],
        archive_bytes_scope="Complete SOURCE and OUT after the seal; external Root evidence also lies in declared total-history roots",
        evidence_producer_implemented_by_this_factory=False)


def helper():
    path = require(PARENT_FACTORY, PARENT_FACTORY_SHA)
    name = "axmat_moment_order_frozen_source_factor_build"
    if name in sys.modules:
        result = sys.modules[name]
    else:
        spec = importlib.util.spec_from_file_location(name, path)
        result = importlib.util.module_from_spec(spec)
        sys.modules[name] = result
        spec.loader.exec_module(result)
    if Path(result.__file__).resolve() != path.resolve():
        raise ValueError("genuine frozen build helper source binding required")
    return result


def baseline():
    require(ROOT / "src/FLU.f", CURRENT_SHA)
    require(ROOT / "src/FLU.o", BASE_OBJECT_SHA)
    require(ROOT / "lib/Darwin_arm64/libDragon.a", LIB_SHA)
    member = subprocess.run(["/usr/bin/ar", "-p", str(ROOT / "lib/Darwin_arm64/libDragon.a"), "FLU.o"],
                            check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(member).hexdigest() != BASE_OBJECT_SHA:
        raise ValueError("actual compiled historical FLU archive member differs")
    raw = subprocess.run(["/usr/bin/git", "-C", str(ROOT), "show", BASE_REVISION + ":src/FLU.f"],
                         check=True, capture_output=True, timeout=60).stdout
    if hashlib.sha256(raw).hexdigest() != BASE_SHA:
        raise ValueError("recovered selector baseline source differs")
    original = raw.decode("utf-8")
    if (original.count(OLD_SELECTOR) != 1
            or original.replace(OLD_SELECTOR, NEW_SELECTOR) != (ROOT / "src/FLU.f").read_text()):
        raise ValueError("complete current-vs-Git FLU diff must be precisely the SPOT selector correction")
    return original


def correct_source(original):
    if original.count(OLD_SELECTOR) != 1 or original.count(OBSERVER_ANCHOR) != 1:
        raise ValueError("unique selector and post-KEYFLX observer insertion point required")
    candidate = original.replace(OLD_SELECTOR, NEW_SELECTOR)
    candidate = candidate.replace(OBSERVER_ANCHOR, OBSERVER_ANCHOR.replace(
        "      CALL LCMLEN(IPTRK,'TITLE',ILNLCM,ITYLCM)", OBSERVER +
        "      CALL LCMLEN(IPTRK,'TITLE',ILNLCM,ITYLCM)"))
    if candidate.replace(OBSERVER, "").replace(NEW_SELECTOR, OLD_SELECTOR) != original:
        raise ValueError("only the SPOT selector and explicit observer may differ")
    return candidate


def selector_block(text):
    start = "      IF(CXDOOR.EQ.'MCCG') THEN\n         NLF=ISTATE(6)"
    if text.count(start) != 1:
        raise ValueError("one complete production angular selector required")
    first = text.index(start)
    last = text.index("      ENDIF", first) + len("      ENDIF")
    return text[first:last]


CONTROL_PROGRAM = r"""program moment_order_controls
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  implicit none
  integer :: s,e,p,u,nanis,nfun,nlf0,nani0,nanis0,nlf1,nani1,nanis1,j
  integer :: state(40),base(40),active0(3),active1(3),calls
  logical :: good0,good1
  character(12) :: door
  real(real64) :: phi,seed,q0(3),q1(3)
  real(real64),parameter :: phis(4)=[0.d0,1.d0,-0.125d0,0.9d0]
  if(storage_size(1_int32)/=32.or.storage_size(1.0_real32)/=32.or. &
     storage_size(1.0_real64)/=64) stop 101
  base=0;base(6)=4;base(9)=1;base(10)=1;base(14)=2;base(15)=32
  base(16)=3;base(30)=3;base(32)=5;base(27)=1
  open(newunit=u,file='moment_order_controls.bin',status='new',access='stream',form='unformatted')
  write(u) 'AXMOU001',int([112,224,192],int32)
  calls=0;seed=0.375d0
  do s=1,14
    state=base;door='SPOT';nanis=2;nfun=3
    select case(s)
    case(2);nanis=8
    case(3);state(16)=1
    case(4);state(16)=0
    case(5);state(15)=2
    case(6);state(15)=4
    case(7);door='MCCG'
    case(8);door='BIVAC'
    case(9);door='TRIVAC'
    case(10);door='SN'
    case(11);door='OTHER'
    case(12);state(15)=0
    case(13);nanis=-1
    case(14);nfun=1
    end select
    do e=1,2
      do p=1,4
        phi=phis(p);nanis0=nanis;nanis1=nanis
        call old_selector(door,state,nanis0,nlf0,nani0)
        call new_selector(door,state,nanis1,nlf1,nani1)
        good0=admissible(nlf0,nani0,nanis0,nfun,phi)
        good1=admissible(nlf1,nani1,nanis1,nfun,phi)
        q0=seed;q1=seed;active0=0;active1=0
        if(good0) then
          call transmit(e,door,nlf0,nanis0,phi,seed,q0,active0)
          calls=calls+1
        endif
        if(good1) then
          call transmit(e,door,nlf1,nanis1,phi,seed,q1,active1)
          calls=calls+1
        endif
        ! Raw complete returned row precedes all Python acceptance gates.
        write(u) int([s,e,p,nanis,nfun,nlf0,nani0,nanis0,nlf1,nani1,nanis1, &
          merge(1,0,good0),merge(1,0,good1)],int32),int(state,int32), &
          int(active0,int32),int(active1,int32),phi,seed,q0,q1
      enddo
    enddo
  enddo
  write(u) int(calls,int32)
  close(u)
  print '(A)', 'AXMAT-MOMENT-ORDER-CONTROLS-RETURNED'
contains
  logical function admissible(nlf,nani,nanis,nfun,phi)
    use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
    integer,intent(in) :: nlf,nani,nanis,nfun
    real(real64),intent(in) :: phi
    admissible=nlf>=1.and.nani>=1.and.nanis>=0.and.nfun>=min(nlf,nanis+1) &
       .and.ieee_is_finite(phi)
  end function
__SELECTORS__
  subroutine transmit(entry,CXDOOR,NLF,NANIS,phi,seed,result,active)
    integer,intent(in) :: entry,NLF,NANIS
    character(*),intent(in) :: CXDOOR
    real(real64),intent(in) :: phi,seed
    real(real64),intent(out) :: result(3)
    integer,intent(out) :: active(3)
    integer :: IAL,IAM,NDIM,IND,IG,IBM,JG,JND,IPOS(1),KEYFLX(3)
    real(real32) :: XSCAT(1)
    real(real64) :: FLUX(3,2,8),scale(3)
    NDIM=1;IND=1;IG=1;IBM=1;JG=2;JND=1;IPOS=1;KEYFLX=[1,2,3]
    XSCAT=0.125;FLUX=0.d0;FLUX(:,IG,8)=seed;scale=[1.d0,-0.125d0,0.75d0]
    FLUX(:,JG,7)=phi*scale;active=0
    select case(entry)
__TRANSMISSION_CASES__
    case default
      stop 102
    end select
    result=FLUX(:,IG,8)
  end subroutine
end program moment_order_controls
"""


def control_source(original, candidate, sender):
    h = helper()
    selectors = []
    for role, text in (("old", original), ("new", candidate)):
        selectors.append("\n".join([
            f"  subroutine {role}_selector(CXDOOR,ISTATE,NANIS,NLF,NANI)",
            "    character(*),intent(in) :: CXDOOR", "    integer,intent(in) :: ISTATE(40)",
            "    integer,intent(inout) :: NANIS", "    integer,intent(out) :: NLF,NANI",
            h.fixed_to_free("\n".join(row for row in selector_block(text).splitlines()
                if row and row[0] not in "Cc*!")), f"  end subroutine {role}_selector"]))
    if sender.count(h.NEW_BLOCK) != 2:
        raise ValueError("successful corrected source-factor sender with both literal entries required")
    cases = []
    for entry, end in ((1, 105), (2, 182)):
        # The original loop bound and sender expressions are literal source
        # extracts. This is a synthetic unit transmission, not a full FLU call.
        loop = f"            DO {end} IAL=0,MIN(NLF-1,NANIS)"
        if sender.count(loop) != 1:
            raise ValueError("complete actual production sender loop header required")
        cases.extend([f"    case({entry})", h.fixed_to_free(loop),
            "      DO IAM=0,MIN(NLF-1,NANIS)", "        IF(IAM.EQ.IAL) THEN",
            "          IND=KEYFLX(1+IAL);active(1+IAL)=1",
            h.fixed_to_free(h.NEW_BLOCK), "        ENDIF", "      ENDDO",
            f"{end} CONTINUE"])
    return CONTROL_PROGRAM.replace("__SELECTORS__", "\n".join(selectors)).replace(
        "__TRANSMISSION_CASES__", "\n".join(cases))


def review_admission(expected):
    if expected != REVIEW_SHA:
        raise ValueError("explicit independent compiled-selector review SHA required")
    review = read(require(REVIEW, expected))
    if (review["schema"] != "AXMAT_PRODUCTION_COMPILED_ANGULAR_SELECTOR_REVIEW_V1"
            or review["classification"] != "CONFIRMED_COMPILED_SPOT_SPATIAL_SLOTS_USED_AS_SOURCE_ANGULAR_ORDER"
            or review["compiled_SPOT_selector"]["NLF_state_index"] != 9
            or review["compiled_SPOT_selector"]["NANI_state_index"] != 10
            or review["current_source_SPOT_selector"]["NLF_state_index"] != 15
            or review["current_source_SPOT_selector"]["NANI_state_index"] != 16
            or review["actual_sender_NLF_is_TRACK_state9"] is not True
            or review["NFUNL_is_not_NLF"] is not True
            or review["actual_sender_activity"]["actual_degrees"] != [0]):
        raise ValueError("independent compiled-selector evidence does not match this correction")
    helper().verify(review["files"])
    return dict(path=str(REVIEW), sha256=expected)


def predecessor_admission(expected):
    if expected != PARENT_SEAL:
        raise ValueError("actual successful source-factor build seal must be supplied")
    h = helper()
    admission = h.production_admission(expected)
    if (admission["corrected_runtime"] != dict(path=str(PARENT / "runtime/Dragon"), sha256=PARENT_RUNTIME_SHA)
            or admission["source_and_receiver_controls"]["actual_receiver_calls"] != 14
            or admission["source_and_receiver_controls"]["actual_source_comparison_rows"] != 384
            or admission["source_and_receiver_controls"]["actual_source_comparison_scalar_invocations"] != 768
            or admission["source_and_receiver_controls"]["actual_interface_source_scalar_invocations"] != 42):
        raise ValueError("genuine completed predecessor arithmetic/receiver inputs required")
    require(PARENT / "build/FLU2DR64.o", PARENT_SENDER_OBJECT_SHA)
    require(PARENT / "build/FLU2DR64.f", PARENT_SENDER_SOURCE_SHA)
    return admission


def resource_admission(resources):
    before = resources.check()
    if (before["artifact_bytes"] + ARCHIVE_RESERVE >= 96 * 2**30
            or before["disk_free_bytes"] - ARCHIVE_RESERVE < 8 * 2**30):
        raise ValueError("complete history plus fresh moment-order build reservation rejected")
    return before


def prepare_build(parent_seal, evidence_sha):
    if SOURCE.exists() or OUT.exists() or TERMINAL.exists():
        raise ValueError("new source and build roots required; no overwrite, resume or retry")
    h = helper()
    parent = predecessor_admission(parent_seal)
    evidence = review_admission(evidence_sha)
    original = baseline()
    candidate = correct_source(original)
    sender = (PARENT / "build/FLU2DR64.f").read_text()
    controls = control_source(original, candidate, sender)
    full, production = h.modules()
    guard_files = h.guard_admission(full)
    old = read(PARENT / "declaration.json")
    h.environment(old)
    compiler = old["build_commands"][0][0]
    link = list(old["build_commands"][1])
    parent_override = str(PARENT / "build/FLU2DR64.o")
    archive = str(ROOT / "lib/Darwin_arm64/libDragon.a")
    if (link.count(parent_override) != 1 or link.count(archive) != 1
            or link.index(parent_override) + 1 != link.index(archive)
            or link[-2:] != ["-o", str(PARENT / "runtime/Dragon")]
            or any(Path(p).name == "FLU.o" for p in link)):
        raise ValueError("exact successful corrected-sender link chain without FLU override required")
    link.insert(link.index(archive), str(OUT / "build/FLU.o"))
    link[-1] = str(OUT / "runtime/Dragon")
    flags = ["-O2", "-march=native", "-ffp-contract=off", "-g", "-fPIC", "-frecord-marker=4",
        "-ffixed-line-length-none", "-I" + str(OUT / "build"), "-I" + str(h.ANG / "build"),
        "-I" + str(ROOT / "lib/Darwin_arm64/modules"), "-I" + str(ROOT / "Ganlib/lib/Darwin_arm64/modules"),
        "-J" + str(OUT / "build")]
    commands = [[compiler, *flags, "-c", str(SOURCE / "FLU.f"), "-o", str(OUT / "build/FLU.o")], link,
        [compiler, *flags, "-c", str(SOURCE / "moment_order_controls.f90"),
         "-o", str(OUT / "build/moment_order_controls.o")],
        [compiler, "-O2", "-march=native", "-ffp-contract=off", "-g",
         str(OUT / "build/moment_order_controls.o"), "-o", str(OUT / "runtime/moment_order_controls")]]
    files = dict(old["files"])
    files.update({str(PARENT / name): sha for name, sha in read(PARENT / "seal.json")["files"].items()})
    files[str(PARENT / "seal.json")] = parent_seal
    files.update(read(REVIEW)["files"])
    paths = [Path(__file__).resolve(), PARENT_FACTORY, REVIEW, RESOURCE_SPEC, RESOURCE_ADDENDUM,
        ROOT / "src/FLU.f", ROOT / "src/FLU.o",
        Path("/usr/bin/ar"), Path("/usr/bin/git"), Path("/usr/bin/otool"), Path("/usr/bin/nm"),
        Path("/usr/bin/dwarfdump"), Path("/bin/ps"), *guard_files]
    for path in paths:
        files[str(path)] = digest(require(path))
    roots = history_roots(sorted(set(old["resource_roots"])
        | set(read(full.OUT / "declaration.json")["resource_roots"])
        | {str(SOURCE), str(OUT), str(TERMINAL)}), ART)
    resources = DynamicHistoryResources(ART, roots, 8 * 2**30, 96 * 2**30, production.ResourceFailure)
    before = resource_admission(resources)
    # Preserve the parent's declared historical namespaces, the complete
    # successful build and the successful current case. No predecessor edits.
    preserved = list(old["preserved_predecessors"])
    for folder in (PARENT, ART / "axial-material-production-qualified-AB-source-factor-20261006"):
        preserved.append(dict(root=str(folder), inventory=h.inventory(folder)))
    admitted = dict(files=files, build_python_executable=old["build_python_executable"],
        native_library_aliases=old["native_library_aliases"],
        numerical_loader_environment=old["numerical_loader_environment"], preserved_predecessors=preserved)
    h.environment(admitted)
    SOURCE.mkdir(exist_ok=False)
    OUT.mkdir(exist_ok=False)
    for name in ("build", "runtime", "controls", "audit", FAMILY):
        (OUT / name).mkdir()
    (SOURCE / "FLU.compiled_baseline.f").write_text(original)
    (SOURCE / "FLU.f").write_text(candidate)
    (SOURCE / "moment_order_controls.f90").write_text(controls)
    (SOURCE / "FLU.patch").write_text("".join(difflib.unified_diff(original.splitlines(True),
        candidate.splitlines(True), fromfile="git:" + BASE_REVISION + ":src/FLU.f",
        tofile="private-SPOT-angular-selector-plus-explicit-observer")))
    shutil.copy2(PARENT / "runtime/run_bounded_dragon.py", OUT / "runtime/run_bounded_dragon.py")
    write_new(SOURCE / "source_admission.json", dict(schema="AXMAT_MOMENT_ORDER_SOURCE_ADMISSION_V1",
        recovered_baseline_revision=BASE_REVISION, recovered_baseline_source_sha256=BASE_SHA,
        historical_compiled_object_sha256=BASE_OBJECT_SHA, current_source_sha256=CURRENT_SHA,
        entire_original_compiled_source_Git_byte_identity_proved=False,
        complete_current_vs_baseline_diff_is_only_SELECTOR=True,
        full_source_restoration_byte_exact=True, selector_replacement=dict(old=OLD_SELECTOR, new=NEW_SELECTOR, count=1),
        observer_only_delta=dict(text=OBSERVER, anchor=OBSERVER_ANCHOR, prefix=OBSERVER_PREFIX,
            columns=["NLF", "NANI", "NANIS", "NFUNL", "NLIN"], required_future_actual_values=OBSERVER_EXPECTED),
        corrected_source_sha256=digest(SOURCE / "FLU.f"), prior_corrected_sender_object=parent_override,
        prior_corrected_sender_sha256=PARENT_SENDER_OBJECT_SHA, sole_new_production_object="FLU.o",
        actual_INSB=1, actual_active_production_sender=1,
        second_sender_is_synthetic_counterpath_only=True,
        white_closure_unchanged=True, physical_data_unchanged=True,
        radial_arithmetic_unchanged=True, angle_grid_unchanged=True))
    # The source root itself is frozen by the build declaration; its successful
    # namespace is not fabricated into a runtime receipt before compilation.
    source_inventory = h.inventory(SOURCE)
    files.update({str(SOURCE / name): sha for name, sha in source_inventory["files"].items()})
    files[str(OUT / "runtime/run_bounded_dragon.py")] = digest(OUT / "runtime/run_bounded_dragon.py")
    write_new(OUT / "declaration.json", dict(schema="AXMAT_MOMENT_ORDER_BUILD_DECLARATION_V1", family=FAMILY,
        source_root=str(SOURCE), source_inventory=source_inventory, files=files, build_commands=commands,
        predecessor=parent, dispatch_evidence=evidence, preserved_predecessors=preserved,
        build_python_executable=old["build_python_executable"], native_library_aliases=old["native_library_aliases"],
        numerical_loader_environment=old["numerical_loader_environment"], resource_roots=roots,
        resources_before=before, artifact_budget_bytes=96 * 2**30, min_free_bytes=8 * 2**30,
        archive_reserve_bytes=ARCHIVE_RESERVE, total_wall_seconds=TOTAL_WALL, stage_wall_seconds=STAGE_WALL,
        rss_cap_mib=RSS_CAP, threads=1, numeric_children_at_once=1, retries=0,
        control_rows=ROWS, selector_invocations=SELECTOR_CALLS, source_unit_invocations=SOURCE_CALLS,
        inherited_native_receiver_calls=14, inherited_receiver_control_scope="Immutable input; not newly executed",
        actual_full_FLU_entry_executed_by_build_controls=False, transport_launched=False,
        required_future_actual_observer_values=OBSERVER_EXPECTED,
        actual_external_terminal_return_contract=terminal_contract(old["build_python_executable"]),
        resource_scope_policy=HISTORY_SCOPE_POLICY,
        resource_scope_contract=resource_scope_contract(),
        resource_accounting_delta="Dynamic union of declared roots and current direct axial-material family roots at every resource check; original no-follow/apparent-byte caps retained",
        original_DiskResources_AST_exact=False,
        physics_delta="SPOT angular selector 9/10 to15/16 plus NANIS clamp; separate observer-only WRITE",
        white_closure_unchanged=True, angle_grid_unchanged=True, radial_arithmetic_unchanged=True,
        physical_data_unchanged=True, source_factor_correction_retained=True,
        original_accuracy_thresholds_changed=False, coefficient_fitting=False,
        AAA_accuracy_qualified=False, ABA_admitted=False))
    print(json.dumps(dict(declaration=str(OUT / "declaration.json"),
        declaration_sha256=digest(OUT / "declaration.json"), source_root=str(SOURCE)), allow_nan=False))


def declaration_admission(expected, require_build_interpreter=True):
    if not expected:
        raise ValueError("actual frozen moment-order declaration SHA required")
    d = read(require(OUT / "declaration.json", expected))
    if (d["schema"] != "AXMAT_MOMENT_ORDER_BUILD_DECLARATION_V1" or d["family"] != FAMILY
            or d["source_root"] != str(SOURCE) or d["total_wall_seconds"] != TOTAL_WALL
            or d["stage_wall_seconds"] != STAGE_WALL or d["rss_cap_mib"] != RSS_CAP
            or d["archive_reserve_bytes"] != ARCHIVE_RESERVE or d["artifact_budget_bytes"] != 96 * 2**30
            or d["min_free_bytes"] != 8 * 2**30 or d["threads"] != 1 or d["numeric_children_at_once"] != 1
            or d["retries"] != 0 or d["control_rows"] != ROWS or d["selector_invocations"] != SELECTOR_CALLS
            or d["source_unit_invocations"] != SOURCE_CALLS or d["inherited_native_receiver_calls"] != 14
            or d["required_future_actual_observer_values"] != OBSERVER_EXPECTED
            or d["actual_external_terminal_return_contract"] != terminal_contract(d["build_python_executable"])
            or d["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or d["resource_scope_contract"] != resource_scope_contract()
            or str(TERMINAL) not in d["resource_roots"]
            or d["actual_full_FLU_entry_executed_by_build_controls"] is not False
            or d["transport_launched"] or d["AAA_accuracy_qualified"] or d["ABA_admitted"]):
        raise ValueError("immutable bounded moment-order build contract differs")
    h = helper()
    environment(d, require_build_interpreter=require_build_interpreter)
    h.verify_inventory(SOURCE, d["source_inventory"])
    if predecessor_admission(PARENT_SEAL) != d["predecessor"] or review_admission(REVIEW_SHA) != d["dispatch_evidence"]:
        raise ValueError("actual successful predecessor or dispatch evidence changed")
    return d


def environment(d, require_build_interpreter=True):
    helper().environment(d, require_build_interpreter=require_build_interpreter)
    if d["resource_scope_policy"] != HISTORY_SCOPE_POLICY or d["resource_scope_contract"] != resource_scope_contract():
        raise ValueError("immutable dynamic complete-history policy required")
    validate_history_roots(history_roots(d["resource_roots"], ART), ART)


def check_watch(stage):
    value = helper().check_watch(OUT, stage)
    raw = read(Path(value["path"]))
    if not raw["elapsed_seconds"] < raw["wall_cap_seconds"] <= stage["wall_cap_seconds"] <= STAGE_WALL:
        raise ValueError("actual own wall limit and recorded stage limit must both hold")
    return value


def fixtures():
    base = [0] * 40
    for slot, value in {6: 4, 9: 1, 10: 1, 14: 2, 15: 32, 16: 3, 27: 1, 30: 3, 32: 5}.items():
        base[slot - 1] = value
    for door, nanis, nfun, edits in CONTROL_CASES:
        state = list(base)
        for slot, value in edits.items():
            state[slot - 1] = value
        yield door, nanis, nfun, state


def expected_selector(door, state, nanis, corrected):
    if door == "SPOT":
        nlf, nani = (state[14], max(1, state[15])) if corrected else (state[8], max(1, state[9]))
        if corrected:
            nanis = min(nanis, nani - 1)
    elif door == "MCCG":
        nlf = nani = state[5]
    elif door == "BIVAC":
        nlf, nani = max(1, state[13]), max(1, state[15])
    elif door == "TRIVAC":
        nlf, nani = max(1, state[29]), max(1, state[31])
    elif door == "SN":
        nlf, nani = state[14], max(1, state[15])
    else:
        nlf = nani = 1
    return [nlf, nani, nanis]


def control_audit():
    h = helper()
    raw_path = require(OUT / "controls/moment_order_controls.bin")
    words = h.Words(raw_path)
    if words.bytes(8) != b"AXMOU001" or words.values("i", 3) != [ROWS, SELECTOR_CALLS, SOURCE_CALLS]:
        raise ValueError("actual complete selector/transmission archive schema differs")
    rows, actual_calls = [], 0
    with (OUT / "audit/independent_control_rows.jsonl").open("x") as witnesses:
        for s, (door, nanis, nfun, state) in enumerate(fixtures(), 1):
            for entry, p in itertools.product(range(1, 3), range(1, 5)):
                indices = words.values("i", 13)
                actual_state = words.values("i", 40)
                old_active, new_active = words.values("i", 3), words.values("i", 3)
                phi, seed, *values = words.values("d", 8)
                old_q, new_q = values[:3], values[3:]
                old, new = expected_selector(door, state, nanis, False), expected_selector(door, state, nanis, True)
                def expectation(selector):
                    nlf, nani, anis = selector
                    good = nlf >= 1 and nani >= 1 and anis >= 0 and nfun >= min(nlf, anis + 1)
                    active = [int(good and degree <= min(nlf - 1, anis)) for degree in range(3)]
                    # Non-SPOT arithmetic retains the predecessor REAL32 factor
                    # before promotion; powers of two make this fixture exact.
                    q = [seed + (.125 if door == "SPOT" else (2 * l + 1) * .125) *
                         (phi * [1., -.125, .75][l]) if active[l] else seed for l in range(3)]
                    return good, active, q
                good0, active0, q0 = expectation(old)
                good1, active1, q1 = expectation(new)
                expected_indices = [s, entry, p, nanis, nfun, *old, *new, int(good0), int(good1)]
                witness = dict(coordinates=[s, entry, p], door=door, TRACK_state=state,
                    input_NANIS=nanis, NFUNL=nfun, expected_old_selector=old, expected_new_selector=new,
                    expected_guards=[good0, good1], expected_active_degrees=[active0, active1],
                    phi=PHIS[p - 1], seed=.375, expected_old_q=q0, expected_new_q=q1,
                    actual_indices=indices, actual_active_degrees=[old_active, new_active], actual_old_q=old_q, actual_new_q=new_q)
                witnesses.write(json.dumps(witness, allow_nan=False) + "\n")
                witnesses.flush()
                if (indices != expected_indices or actual_state != state or phi != PHIS[p - 1]
                        or seed != .375 or not all(math.isfinite(x) for x in [phi, seed, *values])
                        or old_active != active0 or new_active != active1 or old_q != q0 or new_q != q1):
                    raise ValueError("actual compiled selector/order transmission differs at " + str([s, entry, p]))
                if door != "SPOT" and struct.pack("<3d", *old_q) != struct.pack("<3d", *new_q):
                    raise ValueError("non-SPOT arithmetic and selector must remain byte exact")
                actual_calls += int(good0) + int(good1)
                rows.append(witness)
        returned_calls = words.values("i", 1)[0]
        words.end()
    if len(rows) != ROWS or actual_calls != SOURCE_CALLS or returned_calls != actual_calls:
        raise ValueError("complete selector/source invocation count required")
    if rows[0]["expected_active_degrees"] != [[1, 0, 0], [1, 1, 1]]:
        raise ValueError("actual TRACK fixture must expose the old P0-only selector and new P0/P1/P2")
    return dict(schema="AXMAT_MOMENT_ORDER_COMPILED_UNIT_CONTROLS_V1", status="PASS", rows=rows,
        actual_rows=len(rows), actual_selector_invocations=2 * len(rows), actual_source_unit_invocations=actual_calls,
        synthetic_new_negative_fixture_cases=[12, 13, 14], actual_full_FLU_entry_executed=False,
        no_transport=True, both_alternative_unit_entries_tested=True, actual_production_active_entry=1,
        all_orders=[0, 1, 2], non_SPOT_baseline_byte_exact=True,
        raw_archive=dict(path=str(raw_path), sha256=digest(raw_path)),
        independent_witness=dict(path=str(OUT / "audit/independent_control_rows.jsonl"),
                                 sha256=digest(OUT / "audit/independent_control_rows.jsonl")))


def raw_tool(name, command, load_text=True):
    path = OUT / "audit" / name
    with path.open("xb") as stream, path.with_suffix(path.suffix + ".stderr").open("xb") as error_stream:
        completed = subprocess.run(command, check=False, stdout=stream, stderr=error_stream, timeout=60)
    if completed.returncode != 0:
        raise ValueError("actual binary metadata command failed: " + str(command))
    return path.read_text() if load_text else path


def instructions(text):
    result = {}
    for line in text.splitlines():
        match = re.match(r"^([0-9a-fA-F]{16})\s+(.+)$", line)
        if match:
            result[int(match[1], 16)] = re.sub(r"\s+", " ", match[2]).strip()
    return result


def selected_instructions(path, addresses):
    """Stream the large whole executable listing; keep only selector witnesses."""
    result = {}
    with Path(path).open() as stream:
        for line in stream:
            if len(line) < 17 or line[16] not in " \t":
                continue
            try:
                address = int(line[:16], 16)
            except ValueError:
                continue
            if address in addresses:
                result[address] = re.sub(r"\s+", " ", line[17:]).strip()
    return result


def variable_fbreg(info, name):
    match = re.search(r'DW_AT_name\s+\("' + re.escape(name) + r'"\)(?:(?!DW_TAG_).)*?'
                      r'DW_AT_location\s+\(DW_OP_fbreg (-?\d+)\)', info, re.S)
    if not match:
        raise ValueError("actual unambiguous variable DWARF frame location required: " + name)
    return int(match[1])


def binary_audit():
    obj = OUT / "build/FLU.o"
    exe = OUT / "runtime/Dragon"
    object_text = raw_tool("FLU.object.disassembly.txt", ["/usr/bin/otool", "-tvV", str(obj)])
    executable_path = raw_tool("Dragon.disassembly.txt", ["/usr/bin/otool", "-tvV", str(exe)], load_text=False)
    info = raw_tool("FLU.debug_info.txt", ["/usr/bin/dwarfdump", "--debug-info", str(obj)])
    line = raw_tool("FLU.debug_line.txt", ["/usr/bin/dwarfdump", "--debug-line", str(obj)])
    frame = raw_tool("FLU.debug_frame.txt", ["/usr/bin/dwarfdump", "--debug-frame", str(obj)])
    symbols = raw_tool("Dragon.symbols.txt", ["/usr/bin/nm", "-g", str(exe)])
    object_symbols = raw_tool("FLU.object.symbols.txt", ["/usr/bin/nm", "-g", str(obj)])
    dylibs = raw_tool("Dragon.dependencies.txt", ["/usr/bin/otool", "-L", str(exe)])
    loads = raw_tool("Dragon.load_commands.txt", ["/usr/bin/otool", "-l", str(exe)])
    # Every original source and returned binary is already bound by command,
    # hash and restoration checks. This adds actual independent selector reads.
    if str(SOURCE / "FLU.f") not in info:
        raise ValueError("actual private production FLU compilation path must occur in DWARF")
    base_rows = re.findall(r"^([0-9a-fA-F]+) T _flu_$", symbols, re.M)
    obj_rows = re.findall(r"^([0-9a-fA-F]+) T _flu_$", object_symbols, re.M)
    if len(base_rows) != 1 or obj_rows != ["0000000000000000"]:
        raise ValueError("one real production FLU override symbol required")
    exe_base = int(base_rows[0], 16)
    cfa = re.search(r"DW_CFA_def_cfa: W29 \+(\d+)", frame)
    if not cfa:
        raise ValueError("actual FLU frame CFA definition required")
    frame_offset = int(cfa[1])
    state_base = frame_offset + variable_fbreg(info, "istate")
    nlf_location = frame_offset + variable_fbreg(info, "nlf")
    asm = instructions(object_text)
    source = (SOURCE / "FLU.f").read_text()
    selector_first = source.index(NEW_SELECTOR)
    selector_line = source[:selector_first].count("\n") + 1
    line_numbers = {"NLF": selector_line + 2, "NANI": selector_line + 3, "NANIS_clamp": selector_line + 4}
    selector_rows = {int(m[1], 16) for number in line_numbers.values() for m in re.finditer(
        r"^(0x[0-9a-fA-F]+)\s+" + str(number) + r"\s+", line, re.M)}
    selector_windows = {address + 4 * delta for address in selector_rows for delta in range(12)}
    binary = selected_instructions(executable_path, {exe_base + address for address in selector_windows})
    witnesses = {}
    for name, slot in (("NLF", 15), ("NANI", 16)):
        expected_offset = state_base + 4 * (slot - 1)
        matched = []
        for address in sorted(selector_windows):
            instruction = asm.get(address, "")
            single = re.fullmatch(r"ldr (w\d+), \[x29, #0x([0-9a-f]+)\]", instruction)
            pair = re.fullmatch(r"ldp (w\d+), (w\d+), \[x29, #0x([0-9a-f]+)\]", instruction)
            if single and int(single[2], 16) == expected_offset:
                matched.append((address, instruction, single[1]))
            elif pair and expected_offset in (int(pair[3], 16), int(pair[3], 16) + 4):
                matched.append((address, instruction, pair[1 if expected_offset == int(pair[3], 16) else 2]))
        if len(matched) != 1:
            raise ValueError("actual SPOT selector must load TRACK slot " + str(slot) + " at its DWARF line")
        address, instruction, register = matched[0]
        if binary.get(exe_base + address) != instruction:
            raise ValueError("actual new executable must contain the freshly compiled selector instruction")
        if name == "NLF":
            nearby = [asm.get(address + 4 * k, "") for k in range(1, 13)]
            if f"str {register}, [x29, #0x{nlf_location:x}]" not in nearby:
                raise ValueError("actual TRACK slot15 must be stored in the real NLF variable")
        witnesses[name] = dict(TRACK_slot=slot, source_line=line_numbers[name],
            object_address=hex(address), executable_address=hex(exe_base + address), instruction=instruction,
            actual_loaded_register=register, selected_DWARF_statement_window=True)
    clamp_rows = [int(m[1], 16) for m in re.finditer(r"^(0x[0-9a-fA-F]+)\s+" +
        str(line_numbers["NANIS_clamp"]) + r"\s+", line, re.M)]
    if not clamp_rows or any(address not in asm for address in clamp_rows):
        raise ValueError("actual NANIS clamp source line must have compiled instruction witnesses")
    clamp_instructions = [[hex(a), asm[a]] for a in clamp_rows]
    if any(binary.get(exe_base + a) != asm[a] for a in clamp_rows if not asm[a].startswith(("b", "adr"))):
        raise ValueError("actual executable must retain the clamp line's non-relocated instructions")
    if "libDragon" in dylibs:
        raise ValueError("unexpected dynamic Dragon dependency could bypass the static override")
    return dict(schema="AXMAT_MOMENT_ORDER_ACTUAL_COMPILED_SELECTOR_V1", status="PASS",
        object=dict(path=str(obj), sha256=digest(obj)), executable=dict(path=str(exe), sha256=digest(exe)),
        actual_single_FLU_symbol=hex(exe_base), DWARF_private_source_binding=True,
        selector_instruction_witnesses=witnesses, compiled_clamp_source_line_witnesses=clamp_instructions,
        clamp_full_expression_proof="Exact private production source/command/hash plus independently compiled literal controls; line instructions retained without pretending to symbolically reconstruct all optimized arithmetic.",
        explicit_new_FLU_object_precedes_archive=True, source_factor_object_retained=True,
        observer_prefix=OBSERVER_PREFIX, future_actual_values=OBSERVER_EXPECTED,
        full_FLU_execution_observed=False, dynamic_dependencies=dylibs, full_load_commands_retained=True)


def audit_build(expected):
    d = declaration_admission(expected)
    claim = read(require(OUT / "execution_claim.json"))
    stages = read(require(OUT / FAMILY / "stages.json"))["stages"]
    expected_commands = [*d["build_commands"], [str(OUT / "runtime/moment_order_controls")],
        [sys.executable, str(Path(__file__).resolve()), "audit-build", "--sha256", expected]]
    if (claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected
            or len(stages) != len(LABELS) or [s["label"] for s in stages] != list(LABELS)
            or [s["command"] for s in stages] != expected_commands
            or stages[-1]["command"] != [sys.executable, *sys.argv]
            or stages[-1]["status"] != "RUNNING" or any(s["status"] != "PASS" for s in stages[:-1])):
        raise ValueError("actual parent audit after all five build/control stages required")
    watches = [check_watch(s) for s in stages[:-1]]
    receipt = read(require(OUT / "raw_controls_receipt.json"))
    if set(receipt["files"]) != {"controls/moment_order_controls.bin"}:
        raise ValueError("complete raw selector/control output required before gates")
    helper().verify({str(OUT / name): sha for name, sha in receipt["files"].items()})
    identity = read(require(OUT / "runtime/build_identity.json"))
    helper().verify({str(OUT / name): sha for name, sha in identity["files"].items()})
    if (set(identity["files"]) != {"runtime/Dragon", "runtime/moment_order_controls", "build/FLU.o",
            "build/moment_order_controls.o"} or identity["files"]["runtime/Dragon"] == PARENT_RUNTIME_SHA
            or identity["files"]["build/FLU.o"] == BASE_OBJECT_SHA):
        raise ValueError("actual new compiled selector object and linked executable required")
    original = (SOURCE / "FLU.compiled_baseline.f").read_text()
    candidate = (SOURCE / "FLU.f").read_text()
    if (hashlib.sha256(original.encode()).hexdigest() != BASE_SHA or candidate != correct_source(original)
            or (SOURCE / "moment_order_controls.f90").read_text() != control_source(original, candidate,
                (PARENT / "build/FLU2DR64.f").read_text())):
        raise ValueError("actual private sources must restore exactly and use exact literal control extracts")
    controls = control_audit()
    write_new(OUT / "audit/controls.json", controls)
    binary = binary_audit()
    write_new(OUT / "audit/binary_identity.json", binary)
    write_new(OUT / "audit/result.json", dict(classification="PASS_MOMENT_ORDER_BUILD_CONTROLS_ONLY",
        declaration_sha256=expected, predecessor=d["predecessor"], dispatch_evidence=d["dispatch_evidence"],
        control_status=controls["status"], binary_status=binary["status"], actual_control_rows=ROWS,
        actual_selector_invocations=SELECTOR_CALLS, actual_source_unit_invocations=SOURCE_CALLS,
        inherited_native_receiver_calls=14, newly_executed_native_receiver_calls=0,
        previous_stage_watchdogs=watches, actual_full_FLU_entry_executed=False,
        required_future_actual_observer_values=OBSERVER_EXPECTED,
        first_sender_production_activity_scope="INSB1 selects non-scalar first sender; second is a unit counterpath",
        white_closure_unchanged=True, radial_arithmetic_unchanged=True, angle_grid_unchanged=True,
        physical_data_unchanged=True, source_factor_correction_retained=True,
        original_accuracy_thresholds_changed=False, transport_launched=False,
        AAA_accuracy_qualified=False, ABA_admitted=False, coefficient_fitting=False))
    print("AXMAT-MOMENT-ORDER-BUILD-AUDITED")


def run_build(expected):
    started = time.monotonic()
    d = declaration_admission(expected)
    h = helper()
    full, production = h.modules()
    h.guard_admission(full)
    resources = DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"],
        d["artifact_budget_bytes"], production.ResourceFailure)
    resource_admission(resources)
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected,
        started_unix=time.time(), started_monotonic=started, retries=0))
    remaining = TOTAL_WALL - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError("total family cap exhausted before compilation")
    runner = full.OwnRSSSerialExecutor(OUT, remaining, FAMILY, resources)
    result = dict(classification="FAILED_MOMENT_ORDER_BUILD_NO_RETRY", error=None,
        transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False)
    try:
        for index, command in enumerate(d["build_commands"]):
            environment(d)
            runner.execute(OUT / "build", f"build_{index:02d}", command, STAGE_WALL)
        names = ("runtime/Dragon", "runtime/moment_order_controls", "build/FLU.o", "build/moment_order_controls.o")
        write_new(OUT / "runtime/build_identity.json", dict(files={name: digest(require(OUT / name)) for name in names},
            sole_new_production_override="FLU.o", inherited_corrected_sender_object=dict(
                path=str(PARENT / "build/FLU2DR64.o"), sha256=PARENT_SENDER_OBJECT_SHA)))
        environment(d)
        runner.execute(OUT / "controls", "controls", [str(OUT / "runtime/moment_order_controls")],
                       STAGE_WALL, "AXMAT-MOMENT-ORDER-CONTROLS-RETURNED")
        write_new(OUT / "raw_controls_receipt.json", dict(files={"controls/moment_order_controls.bin":
            digest(require(OUT / "controls/moment_order_controls.bin"))}))
        runner.execute(OUT / "audit", "audit", [sys.executable, str(Path(__file__).resolve()),
            "audit-build", "--sha256", expected], STAGE_WALL, "AXMAT-MOMENT-ORDER-BUILD-AUDITED")
        stages = read(OUT / FAMILY / "stages.json")["stages"]
        if len(stages) != len(LABELS) or [s["label"] for s in stages] != list(LABELS) or any(s["status"] != "PASS" for s in stages):
            raise ValueError("all six actual bounded stages required")
        audit = read(OUT / "audit/result.json")
        if (audit["classification"] != "PASS_MOMENT_ORDER_BUILD_CONTROLS_ONLY" or audit["control_status"] != "PASS"
                or audit["binary_status"] != "PASS" or audit["actual_control_rows"] != ROWS
                or audit["actual_selector_invocations"] != SELECTOR_CALLS or audit["actual_source_unit_invocations"] != SOURCE_CALLS
                or audit["AAA_accuracy_qualified"] or audit["ABA_admitted"] or audit["transport_launched"]):
            raise ValueError("complete actual selector/source controls and binary proof required")
        result.update(classification="COMPLETE_MOMENT_ORDER_BUILD_CONTROLS_ONLY",
            watchdogs=[check_watch(s) for s in stages], actual_control_rows=ROWS,
            actual_selector_invocations=SELECTOR_CALLS, actual_source_unit_invocations=SOURCE_CALLS,
            runtime_sha256=digest(OUT / "runtime/Dragon"), source_root=str(SOURCE),
            actual_full_FLU_entry_executed=False, required_future_actual_observer_values=OBSERVER_EXPECTED)
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        try:
            environment(d)
            h.verify_inventory(SOURCE, d["source_inventory"])
            result["resources"] = resources.check()
            size = sum(p.stat().st_size for folder in (SOURCE, OUT) for p in folder.rglob("*")
                       if p.is_file() and not p.is_symlink())
            elapsed = time.monotonic() - started
            if elapsed >= TOTAL_WALL or size >= ARCHIVE_RESERVE:
                raise ValueError("complete build closeout wall/archive budget exceeded")
            result.update(elapsed_seconds=elapsed, archive_bytes_before_closeout=size)
        except BaseException as error:
            result.update(classification="FAILED_MOMENT_ORDER_BUILD_NO_RETRY", error=repr(error),
                          elapsed_seconds=time.monotonic() - started)
            write_new(OUT / "driver_result.json", result)
            raise
        write_new(OUT / "driver_result.json", result)
    write_new(OUT / "seal.json", dict(schema="AXMAT_MOMENT_ORDER_BUILD_SEAL_V1",
        files={str(p.relative_to(OUT)): digest(p) for p in OUT.rglob("*") if p.is_file()}))
    try:
        final_resource = resources.check()
        final_size = sum(p.stat().st_size for folder in (SOURCE, OUT) for p in folder.rglob("*")
                         if p.is_file() and not p.is_symlink())
        final_elapsed = time.monotonic() - started
        if final_size >= ARCHIVE_RESERVE or final_elapsed >= TOTAL_WALL:
            raise ValueError("mandatory post-seal tail cap failed")
    except BaseException as error:
        write_new(OUT / "closeout_failure.json", dict(error=repr(error), complete=False,
            AAA_accuracy_qualified=False, ABA_admitted=False))
        raise
    print(json.dumps(dict(result=result, actual_tail_check="PASS", actual_elapsed_seconds=final_elapsed,
        actual_archive_bytes=final_size, actual_resources=final_resource), allow_nan=False))


def strict_terminal_json(path):
    def unique_object(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate key in actual external terminal JSON")
            value[key] = item
        return value
    def reject_constant(value):
        raise ValueError("nonfinite JSON constant in actual external terminal JSON: " + value)
    result = json.loads(Path(path).read_text(), object_pairs_hook=unique_object, parse_constant=reject_constant)
    if type(result) is not dict:
        raise ValueError("the full actual terminal output must be one JSON object")
    return result


def terminal_file(value, expected_sha=None):
    if not isinstance(value, (str, Path)):
        raise ValueError("actual external terminal evidence requires an absolute canonical regular path")
    path = Path(value)
    if (not path.is_absolute() or ".." in path.parts or str(value) != str(path)
            or path.parent != TERMINAL or path.resolve(strict=True) != path):
        raise ValueError("actual external terminal path is outside its independent fixed root")
    cursor = path
    while True:
        if cursor.is_symlink():
            raise ValueError("external terminal evidence or ancestor is a symlink")
        if cursor == cursor.parent:
            break
        cursor = cursor.parent
    return require(path, expected_sha)


def external_terminal_admission(d, declared_sha, expected_seal, sealed_result,
                                terminal_evidence, terminal_evidence_sha256):
    """Require Root's retained real exit-zero proof after all closeout work.

    A success seal can exist while this parent still runs or after interruption.
    It is never sufficient without this independently produced terminal record.
    This factory neither creates that record nor infers exit zero from a flag.
    """
    if (not isinstance(terminal_evidence_sha256, str) or len(terminal_evidence_sha256) != 64
            or any(c not in "0123456789abcdef" for c in terminal_evidence_sha256)):
        raise ValueError("actual independent terminal-return receipt SHA256 is mandatory")
    if (TERMINAL.parent != ART or TERMINAL in (SOURCE, OUT)
            or any(TERMINAL.is_relative_to(root) or root.is_relative_to(TERMINAL) for root in (SOURCE, OUT))
            or str(TERMINAL) not in d["resource_roots"]):
        raise ValueError("external terminal root must be independent and within the declared total-history scope")
    receipt = terminal_file(terminal_evidence, terminal_evidence_sha256)
    if receipt != TERMINAL / "terminal_return.json":
        raise ValueError("only the fixed actual external terminal-return record is eligible")
    e = strict_terminal_json(receipt)
    factory = Path(__file__).resolve()
    source_pin = dict(path=str(factory), sha256=digest(require(factory)))
    command = [d["build_python_executable"], str(factory), "run-build", "--sha256", declared_sha]
    if (e["schema"] != TERMINAL_SCHEMA or e["record_producer"] != "root"
            or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True
            or type(e["returncode"]) is not int or e["returncode"] != 0
            or e["command"] != command or e["source"] != source_pin
            or d["files"].get(str(factory)) != source_pin["sha256"]
            or e["declaration"] != dict(path=str(OUT / "declaration.json"), sha256=declared_sha)
            or e["build_seal"] != dict(path=str(OUT / "seal.json"), sha256=expected_seal)):
        raise ValueError("actual Root exit-zero evidence must bind this exact source/declaration/build seal")
    stdout = terminal_file(e["full_stdout"]["path"], e["full_stdout"]["sha256"])
    stdout_pin = dict(path=str(stdout), sha256=digest(stdout))
    if stdout == receipt or e["full_stdout"] != stdout_pin:
        raise ValueError("full actual stdout must be a separately retained regular file")
    returned = strict_terminal_json(stdout)
    tail = {key: returned[key] for key in TAIL_FIELDS}
    if returned != dict(result=sealed_result, **tail) or any(e[key] != tail[key] for key in TAIL_FIELDS):
        raise ValueError("full actual stdout, sealed result and Root terminal-tail values differ")
    elapsed, archive_bytes, snapshot = tail["actual_elapsed_seconds"], tail["actual_archive_bytes"], tail["actual_resources"]
    actual_bytes = sum(p.stat().st_size for folder in (SOURCE, OUT) for p in folder.rglob("*")
                       if p.is_file() and not p.is_symlink())
    if (tail["actual_tail_check"] != "PASS" or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or type(archive_bytes) is not int or not 0 <= archive_bytes < ARCHIVE_RESERVE or archive_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or snapshot["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["declared_resource_roots"] != d["resource_roots"]
            or type(snapshot["resource_roots"]) is not list
            or not set(d["resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int
            or not archive_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float) or not math.isfinite(snapshot["checked_unix"])
            or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete terminal-tail wall/archive/resource gates must hold")
    validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=dict(path=str(receipt), sha256=digest(receipt)), full_stdout=stdout_pin,
                command=command, schema=TERMINAL_SCHEMA, **tail)


def production_admission(build_seal_sha, terminal_evidence, terminal_evidence_sha256):
    """Read-only future pipeline input gate; does not admit AAA or ABA."""
    seal = read(require(OUT / "seal.json", build_seal_sha))
    if seal["schema"] != "AXMAT_MOMENT_ORDER_BUILD_SEAL_V1":
        raise ValueError("actual completed moment-order build seal required")
    actual = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()}
    if actual != set(seal["files"]) | {"seal.json"}:
        raise ValueError("successful exact build namespace required; tail failures are not admissible")
    helper().verify({str(OUT / name): sha for name, sha in seal["files"].items()})
    d = declaration_admission(digest(OUT / "declaration.json"), require_build_interpreter=False)
    result, audit = read(OUT / "driver_result.json"), read(OUT / "audit/result.json")
    if (result["classification"] != "COMPLETE_MOMENT_ORDER_BUILD_CONTROLS_ONLY" or result["error"] is not None
            or audit["classification"] != "PASS_MOMENT_ORDER_BUILD_CONTROLS_ONLY"
            or audit["control_status"] != "PASS" or audit["binary_status"] != "PASS"
            or result["actual_control_rows"] != ROWS or result["actual_selector_invocations"] != SELECTOR_CALLS
            or result["actual_source_unit_invocations"] != SOURCE_CALLS
            or result["transport_launched"] or result["AAA_accuracy_qualified"] or result["ABA_admitted"]):
        raise ValueError("actual limited-scope build/control PASS required")
    stages = read(OUT / FAMILY / "stages.json")["stages"]
    if len(stages) != len(LABELS) or [s["label"] for s in stages] != list(LABELS) or any(s["status"] != "PASS" for s in stages):
        raise ValueError("all actual build/control stages required")
    for stage in stages:
        check_watch(stage)
    terminal = external_terminal_admission(d, digest(OUT / "declaration.json"), build_seal_sha, result,
                                          terminal_evidence, terminal_evidence_sha256)
    # The terminal snapshot is immutable history at the actual build return.
    # Independently admit the current complete history, including legitimate
    # consuming-family roots, without inserting a changing snapshot into API
    # metadata that callers must compare byte for byte.
    DynamicHistoryResources(ART, d["resource_roots"], d["min_free_bytes"], d["artifact_budget_bytes"]).check()
    return dict(schema="AXMAT_MOMENT_ORDER_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1", build_root=str(OUT),
        source_root=str(SOURCE), build_seal_sha256=build_seal_sha,
        corrected_runtime=dict(path=str(OUT / "runtime/Dragon"), sha256=digest(OUT / "runtime/Dragon")),
        source_admission=dict(path=str(SOURCE / "source_admission.json"), sha256=digest(SOURCE / "source_admission.json")),
        dispatch_evidence=d["dispatch_evidence"], predecessor=d["predecessor"],
        future_contract=d["predecessor"]["future_contract"],
        capture_dependency=d["predecessor"]["capture_dependency"],
        source_and_receiver_controls=d["predecessor"]["source_and_receiver_controls"],
        source_and_receiver_controls_inherited_not_newly_executed=True,
        actual_external_terminal_evidence=terminal["receipt"], actual_external_terminal_validation=terminal,
        resource_scope_policy=HISTORY_SCOPE_POLICY, current_complete_history_admission_required=True,
        resource_scope_contract=d["resource_scope_contract"],
        compiled_selector=dict(path=str(OUT / "audit/binary_identity.json"), sha256=digest(OUT / "audit/binary_identity.json")),
        compiled_unit_controls=dict(path=str(OUT / "audit/controls.json"), sha256=digest(OUT / "audit/controls.json")),
        actual_control_rows=ROWS, actual_selector_invocations=SELECTOR_CALLS, actual_source_unit_invocations=SOURCE_CALLS,
        inherited_native_receiver_calls=14, newly_executed_native_receiver_calls=0,
        future_actual_FLU_observer_required=dict(prefix=OBSERVER_PREFIX,
            columns=["NLF", "NANI", "NANIS", "NFUNL", "NLIN"], expected=OBSERVER_EXPECTED),
        corrected_sender_retained=True, white_closure_unchanged=True, collision_self_operator_unchanged=True,
        angle_grid_unchanged=True, radial_arithmetic_unchanged=True, physical_data_unchanged=True,
        original_accuracy_thresholds_changed=False, no_CE_fitting=True,
        full_FLU_entry_execution_proved_by_build=False,
        admission="MOMENT_ORDER_RUNTIME_INPUT_ONLY", production_pipeline_prepared=False,
        AAA_accuracy_qualified=False, ABA_admitted=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare-build", "run-build", "audit-build", "admit"))
    parser.add_argument("--source-factor-build-seal-sha256")
    parser.add_argument("--dispatch-evidence-sha256")
    parser.add_argument("--sha256")
    parser.add_argument("--terminal-evidence")
    parser.add_argument("--terminal-evidence-sha256")
    args = parser.parse_args()
    {"prepare-build": lambda: prepare_build(args.source_factor_build_seal_sha256, args.dispatch_evidence_sha256),
     "run-build": lambda: run_build(args.sha256), "audit-build": lambda: audit_build(args.sha256),
     "admit": lambda: print(json.dumps(production_admission(args.sha256, args.terminal_evidence,
        args.terminal_evidence_sha256), allow_nan=False))}[args.action]()
