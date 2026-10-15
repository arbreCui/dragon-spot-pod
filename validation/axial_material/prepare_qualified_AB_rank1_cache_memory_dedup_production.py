"""Future lossless ordinary-rank1 lower-block dictionary component, source only.

The complete 92d rank1 build and actual Root exit-zero witness are compulsory.
Only SPOT1P64.o changes in production; sender/SPOASM/white/all other inputs stay
exact. All original controls reexecute, with independently archived dense c017
lower/packed/full decode comparisons. Unit success cannot prove native RSS or
AAA/ABA accuracy. Root alone supplies actual exit-zero/full stdout/stderr proof.
"""

import argparse
import ast
import copy
import difflib
import hashlib
import importlib.util
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
SOURCE = ART / "axial-material-qualified-AB-rank1-factor-cache-memory-dedup-build-admission-20261007"
OUT = ART / "axial-material-rank1-factor-cache-memory-dedup-build-20261007"
TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-memory-dedup-build-terminal-20261007"
PARENT = ART / "axial-material-rank1-factor-cache-build-20261007"
PARENT_SOURCE = ART / "axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007"
PARENT_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-build-terminal-20261007"
PARENT_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_production.py"
PARENT_FACTORY_SHA = "92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a"
PARENT_SEAL = "e86ee99baec88585c5965b67043658a519ebde61bb32d195fc35598970e4b39f"
PARENT_RUNTIME_SHA = "292c10b259ead4d9123dcba7efd48dea0bf31b41963c620149c685c93906663c"
PARENT_TERMINAL_SHA = "c5eecbff0064a9285460c98bc01bad26ab9180a4b4e38a6186be779378ba9d96"
MEMORY_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_cache_memory_production.py"
MEMORY_FACTORY_SHA = "438309418dc49137559c88e3a291c93c90696e7b8af420c115c14efe268778de"
MEMORY_ROOT = ART / "axial-material-rank1-factor-cache-memory-build-20261007"
MEMORY_SOURCE = ART / "axial-material-qualified-AB-rank1-factor-cache-memory-build-admission-20261007"
MEMORY_TERMINAL = ART / "axial-material-qualified-AB-rank1-factor-cache-memory-build-terminal-20261007"
MEMORY_SEAL_SHA = "ff1fc61b7b4094ab93d7403a1862bdd47f6d86ccf0178e87822ef0b5015532e5"
MEMORY_TERMINAL_SHA = "b0bec2a8c435cc8fba2e2691d399455bb68d410fd889fa82e91c15a84b39b7a7"
MEMORY_KERNEL_SOURCE = MEMORY_SOURCE / "SPOT1P64.f90"
MEMORY_KERNEL_SOURCE_SHA = "c0fddcd2ddc4dba6969440024a9205fbb297727a6a045886acba626323ab5718"
MEMORY_KERNEL_OBJECT_SHA = "b9dfb5f82902e696ed68ef403003c1e94d0e9159fe3e31bb0109c4aeabf801d4"
MEMORY_RUNTIME_SHA = "4034e0b842f9a4bcb5360fa00b2e55da0bfbafe5614b26b4a5f50f5974a6cd61"
FAILED_MEMORY_CAPTURE_TERMINAL_SHA = "3387bf47688456526d1b73a682bab17107572b5417b87f7d45e08f9cbdf6bcff"
FAILED_CAPTURE_TERMINAL_SHA = "648405e5477630afcf9ee7583ebfddfc0315348ae27e11e997c578a050a08d29"
ANG = ART / "axial-material-AAA-white-trace-angular-convergence-20261005/build"
KERNEL_SOURCE = PARENT_SOURCE / "SPOT1P64.f90"
KERNEL_SOURCE_SHA = "c017167b5c48bc922efb7353db8c11a91758add1c2c5a02c42bd2baaeba210a2"
KERNEL_OBJECT = PARENT / "build/SPOT1P64.o"
KERNEL_OBJECT_SHA = "323c4631fbea0a2044d523be70ba3ad1909b5814c484a77b806772be45d508f1"
WHITE_SOURCE = ANG / "axmat_white_trace_model.f90"
WHITE_SOURCE_SHA = "5ff57deb56ffec2ed74fd7efe023e5245432fbee6c42abc7ddba7dd9b7d01adc"
WHITE_OBJECT = ANG / "axmat_white_trace_model.o"
WHITE_OBJECT_SHA = "3a0a2517c086f91c79f770cfb6c44f2c04104510ded5e990c464d18a0375e4e2"
SENDER_SOURCE = PARENT_SOURCE / "FLU2DR64.f"
SENDER_SOURCE_SHA = "bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81"
SENDER_OBJECT = PARENT / "build/FLU2DR64.o"
SENDER_OBJECT_SHA = "74b22d403667e78686aef52b97933478779d4dfeb250b1cd1cb86343c930cfb9"
PATCH_HELPER = ROOT / "validation/axial_material/rank1_factor_cache_memory_dedup_patch.py"
CONTROL_SOURCE = ROOT / "validation/axial_material/rank1_factor_cache_memory_dedup_controls.f90"
ORIGINAL_PATCH = ROOT / "validation/axial_material/rank1_factor_cache_patch.py"
ORIGINAL_PATCH_SHA = "c309a37bad260ebdf377370689b3295476c31fefde8269257c597666f6f78f3e"
ORIGINAL_CONTROL = ROOT / "validation/axial_material/rank1_factor_cache_controls.f90"
ORIGINAL_CONTROL_SHA = "377e5b3c8f183763fa2749dcfee6090c553283ae2f58a7d725ab653fc5b2210b"
TOTAL_WALL, STAGE_WALL, RSS_CAP = 1800, 600, 512
ARCHIVE_RESERVE = 2 * 2**30
HISTORY_CAP, FREE_FLOOR = 96 * 2**30, 8 * 2**30
FAMILY = "RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD"
HISTORY_SCOPE_POLICY = "AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1"
OBSERVER_EXPECTED = [32, 3, 2, 3, 1]
TERMINAL_SCHEMA = "AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
TAIL_FIELDS = ("actual_tail_check", "actual_elapsed_seconds", "actual_archive_bytes", "actual_resources")


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(path, expected=None):
    path = Path(path)
    if (not path.is_absolute() or path.is_symlink() or not path.is_file()
            or (expected is not None and digest(path) != expected)):
        raise ValueError("missing, aliased or changed rank-one build input: " + str(path))
    return path


def pin(path):
    return dict(path=str(require(path)), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, data):
    with Path(path).open("x") as stream:
        json.dump(data, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def absent(path):
    if Path(path).exists() or Path(path).is_symlink():
        raise ValueError("exclusive new build root or claim exists; no overwrite/retry: " + str(path))


def load(path, name):
    path = require(path)
    if name in sys.modules:
        result = sys.modules[name]
        if Path(result.__file__).resolve() != path.resolve():
            raise ValueError("actual imported source identity differs: " + name)
        return result
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    if Path(result.__file__).resolve() != path.resolve():
        raise ValueError("actual module identity differs")
    return result


def parent_factory():
    return load(require(PARENT_FACTORY, PARENT_FACTORY_SHA), "rank1_memory_dedup_actual_parent_build")


def helper():
    return parent_factory().helper()


def resource_scope_contract():
    return parent_factory().resource_scope_contract()


def history_roots(declared, artifacts_root):
    return parent_factory().history_roots(declared, artifacts_root)


def validate_history_roots(values, artifacts_root):
    return parent_factory().validate_history_roots(values, artifacts_root)


def DynamicHistoryResources(artifacts_root, roots, min_free_bytes, max_bytes, failure_type=None):
    """Lazy public constructor; return the genuine inherited resource class."""
    return parent_factory().DynamicHistoryResources(
        artifacts_root, roots, min_free_bytes, max_bytes, failure_type)


def resources_for(roots, failure=None):
    return DynamicHistoryResources(ART, roots, FREE_FLOOR, HISTORY_CAP, failure)


def archive_bytes():
    roots = validate_history_roots([str(SOURCE), str(OUT)], ART)
    total, stack = 0, list(roots)
    while stack:
        path = stack.pop()
        try:
            fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            try:
                with os.scandir(fd) as entries:
                    for entry in entries:
                        value = entry.stat(follow_symlinks=False)
                        if stat.S_ISDIR(value.st_mode):
                            stack.append(path / entry.name)
                        elif stat.S_ISREG(value.st_mode):
                            total += value.st_size
            finally:
                os.close(fd)
        except FileNotFoundError:
            continue
    validate_history_roots([str(SOURCE), str(OUT)], ART)
    return total


def exact_directories(root):
    require_root=Path(root)
    if require_root.is_symlink() or not require_root.is_dir():raise ValueError("actual canonical family root required")
    result=[]
    for parent,dirs,names in os.walk(require_root,followlinks=False):
        if any((Path(parent)/name).is_symlink() for name in [*dirs,*names]):raise ValueError("new family namespace cannot contain symlinks")
        for name in dirs:result.append(str((Path(parent)/name).relative_to(require_root)))
    return sorted(result)


def resource_admission(resources):
    snapshot = resources.check()
    if snapshot["artifact_bytes"] + ARCHIVE_RESERVE >= HISTORY_CAP or snapshot["disk_free_bytes"] - ARCHIVE_RESERVE < FREE_FLOOR:
        raise ValueError("complete axial family plus fresh 2GiB build exceeds original 96GiB/free8GiB")
    return snapshot


def predecessor_admission(seal, terminal, terminal_sha):
    if seal != PARENT_SEAL or terminal_sha != PARENT_TERMINAL_SHA or Path(terminal) != PARENT_TERMINAL / "terminal_return.json":
        raise ValueError("actual completed rank1 build and Root terminal pins are mandatory")
    result = parent_factory().production_admission(seal, terminal, terminal_sha)
    if (result["schema"] != "AXMAT_RANK1_FACTOR_CACHE_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or result["admission"] != "RANK1_FACTOR_CACHE_RUNTIME_INPUT_ONLY"
            or result["corrected_runtime"] != pin(PARENT / "runtime/Dragon")
            or result["corrected_runtime"]["sha256"] != PARENT_RUNTIME_SHA
            or result["rank1_factor_cache_controls_passed"] is not True
            or result["all_new_cache_outputs_bitwise_equal_to_uncached"] is not True
            or result["operator_identity_guard_negative_controls_passed"] is not True
            or result["actual_full_FLU_entry_executed"] is not False
            or result["AAA_accuracy_qualified"] is not False or result["ABA_admitted"] is not False):
        raise ValueError("the actual complete predecessor input-only scope must remain exact")
    return result


def memory_predecessor_admission(seal, terminal, terminal_sha, original_parent):
    """The real completed compact-row component remains a full prerequisite."""
    if (seal != MEMORY_SEAL_SHA or terminal_sha != MEMORY_TERMINAL_SHA
            or Path(terminal) != MEMORY_TERMINAL / "terminal_return.json"):
        raise ValueError("actual completed memory build and Root terminal pins are mandatory")
    factory = load(require(MEMORY_FACTORY, MEMORY_FACTORY_SHA), "rank1_dedup_actual_memory_parent")
    result = factory.production_admission(seal, terminal, terminal_sha)
    if (result["schema"] != "AXMAT_RANK1_FACTOR_CACHE_MEMORY_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1"
            or result["admission"] != "RANK1_FACTOR_CACHE_MEMORY_RUNTIME_INPUT_ONLY"
            or result["inherited_rank1_factor_cache_admission"] != original_parent
            or result["compiled_kernel_source"] != pin(MEMORY_KERNEL_SOURCE)
            or result["compiled_kernel_source"]["sha256"] != MEMORY_KERNEL_SOURCE_SHA
            or result["compiled_kernel"] != dict(path=str(MEMORY_ROOT / "build/SPOT1P64.o"),sha256=MEMORY_KERNEL_OBJECT_SHA)
            or result["corrected_runtime"] != dict(path=str(MEMORY_ROOT / "runtime/Dragon"),sha256=MEMORY_RUNTIME_SHA)
            or result["actual_external_terminal_evidence"] != pin(MEMORY_TERMINAL / "terminal_return.json")
            or result["native_RSS_proof_obtained"] is not False
            or result["fresh_512MiB_native_capture_required"] is not True
            or result["actual_full_FLU_entry_executed"] is not False
            or result["AAA_accuracy_qualified"] is not False or result["ABA_admitted"] is not False
            or any(result[key] is not True for key in ("lower_structural_zero_rows_losslessly_packed",
                "full_shape_MATMUL_and_RHS_order_unchanged", "all_original_and_memory_controls_bitwise_passed",
                "rowmap_dimensions_zero_and_cap_negative_controls_passed"))):
        raise ValueError("actual completed compact memory prerequisite changed or claims unproved native accuracy")
    return result


def cold_failure_admission(terminal_sha):
    # Preserve the originally witnessed failed cold case through the compulsory
    # complete parent. It remains failure evidence, never a scientific PASS.
    return parent_factory().cold_failure_admission(terminal_sha)


def terminal_contract(python):
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / "terminal_return.json"),
        record_producer="root", full_stdout_is_retained=True, actual_tool_exit_zero_required=True,
        record_written_after_actual_terminal_return_required=True, tail_fields=list(TAIL_FIELDS),
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=resource_scope_contract(),
        tail_roots_are_dynamic_union=True, actual_run_command=[python, str(Path(__file__).resolve()),
            "run-build", "--sha256", "__DECLARATION_SHA256__"],
        archive_bytes_scope="Complete SOURCE plus OUT; external terminal root also belongs to complete axial-family history",
        evidence_producer_implemented_by_this_factory=False)


def source_inputs():
    expected = {MEMORY_KERNEL_SOURCE:MEMORY_KERNEL_SOURCE_SHA, MEMORY_FACTORY:MEMORY_FACTORY_SHA,
        KERNEL_SOURCE:KERNEL_SOURCE_SHA, KERNEL_OBJECT:KERNEL_OBJECT_SHA,
        SENDER_SOURCE:SENDER_SOURCE_SHA, SENDER_OBJECT:SENDER_OBJECT_SHA,
        WHITE_SOURCE:WHITE_SOURCE_SHA, WHITE_OBJECT:WHITE_OBJECT_SHA,
        ORIGINAL_PATCH:ORIGINAL_PATCH_SHA, ORIGINAL_CONTROL:ORIGINAL_CONTROL_SHA}
    for path,wanted in expected.items():
        require(path,wanted)
    old = read(require(PARENT / "declaration.json"))
    link = old["build_commands"][2]
    for path in (KERNEL_OBJECT,SENDER_OBJECT,WHITE_OBJECT):
        if link.count(str(path)) != 1:
            raise ValueError("actual complete parent explicit object chain differs")
    if (link.index(str(KERNEL_OBJECT)) >= link.index(str(ROOT / "lib/Darwin_arm64/libDragon.a"))
            or link[-2:] != ["-o",str(PARENT / "runtime/Dragon")]):
        raise ValueError("actual parent override precedence/output differs")
    return old,{str(path):wanted for path,wanted in expected.items()}


def cache_observer_contract():
    return dict(prefix="AXMAT-RANK1-CACHE TERMINAL ",
        columns=["builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes", "cap_bytes"],
        cap_bytes=536870912, exact_operator_identity_required=True,
        positive_build_reuse_and_validation_required=True, all_actual_full_logs_required=True)


def control_source_equivalence():
    """Pin literal inherited operator/source/output/pivot routines separately."""
    old=require(ORIGINAL_CONTROL,ORIGINAL_CONTROL_SHA).read_text()
    new=require(CONTROL_SOURCE).read_text()
    retained={}
    for name in ("configure","source","solve","save_input","save_result","pivot_control"):
        pattern=r"(?ms)^  subroutine "+name+r"\(.*?^  end subroutine "+name+r"\n"
        a=re.findall(pattern,old);b=re.findall(pattern,new)
        if len(a)!=1 or a!=b:raise ValueError("literal inherited unit arithmetic routine changed: "+name)
        retained[name]=hashlib.sha256(a[0].encode()).hexdigest()
    return dict(schema="AXMAT_RANK1_MEMORY_DEDUP_CONTROL_SOURCE_EQUIVALENCE_V1",original_source=pin(ORIGINAL_CONTROL),
        new_source=pin(CONTROL_SOURCE),retained_subroutine_byte_sha256=retained,
        original1146pairs_operator_and14identity_and2cap_attempts_retained=True,
        additional_source_solver_fixture_is_only_synchronized_angle_permutation=True,
        additional_dictionary_primitives_have_no_solver=True,
        new_memory_raw_observation_and_module_guard_calls_are_explicit=True,
        whole_new_driver_is_not_claimed_byteidentical=True,actual_controls_executed=False)


def patch_admission(helper_sha, controls_sha):
    if not all(re.fullmatch(r"[0-9a-f]{64}", value or "") for value in (helper_sha,controls_sha)):
        raise ValueError("actual independently reviewed memory source hashes required")
    patch = load(require(PATCH_HELPER,helper_sha),"rank1_memory_dedup_actual_patch")
    require(CONTROL_SOURCE,controls_sha)
    source = require(MEMORY_KERNEL_SOURCE,MEMORY_KERNEL_SOURCE_SHA).read_text()
    changed = patch.patch_kernel(source)
    dense = patch.dense_reference_kernel(require(KERNEL_SOURCE,KERNEL_SOURCE_SHA).read_text())
    original = load(require(ORIGINAL_PATCH,ORIGINAL_PATCH_SHA),"rank1_memory_dedup_actual_original_patch")
    # This genuine 754421 original is independently recompiled for uncached
    # unit comparison, not falsely identified as the historical object bytes.
    ref = original.patch_sources(require(ANG / "SPOT1P64.f90","7544212ac8419f9c73688c12339c8779358a24f4065523fbbf891cc4fe1c79e0").read_text(),
        require(ART / "axial-material-source-factor-build-20261006/build/FLU2DR64.f",
        "15b0a314886ed224204a53dc77e52fe79114ef00eee81230f80d28eaed4a8316").read_text())
    c = copy.deepcopy(original.control_contract())
    c["schema"] = "AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_CONTROL_CONTRACT_V1"
    c["experiment"] = "rank1-factor-cache-memory-dedup-20261007"
    c["positive_cases"].append("permuted_angles")
    c["inherited_dense_key_accounting_description"] = c["key_accounting"]
    c["key_accounting"] = "Raw/projected key bytes and 4096/group descriptor unchanged. Four-argument FACTORS reserves the original full packed49-block factor bound plus4*nblock int32 map bytes before allocation. STORE allocates only first-occurrence IEEE64 bit dictionaries, then releases8*npositive*nstate*(nblock-nunique) unallocated bytes. Retained factors=(16*nstate^2+12*nstate)*nblock+4*npositive+4*nblock+8*npositive*nstate*nunique. Actual ascending DU-positive rowmap retained; hit full-shape8*nstate^2 reconstruction workspace reserved/released. Reservation peak is not RSS. Legacy full lower unchanged."

    c["inherited_literal_control_source"] = dict(path=str(ORIGINAL_CONTROL),sha256=ORIGINAL_CONTROL_SHA)
    c["positive_fixtures"].append(dict(name="permuted_angles",groups=2,nrhs=3,nreg2d=8,nfloor=48,
        npq=32,nsct=3,nmode=1,white=True,rank1=True))
    memory = patch.control_contract()
    c["memory_control_contract"] = memory
    c["memory_positive_command_args"] = ["memory-positive"]
    c["memory_negative_cases"] = [dict(item,args=["memory-negative",item["name"]])
        for item in memory["additional_negative_cases"]]
    c["dedup_control_contract"] = memory
    c["dedup_positive_command_args"] = ["dedup-positive"]
    c["dedup_negative_cases"] = [dict(item,args=["dedup-negative",item["name"]]) for item in memory["dedup_negative_cases"]]
    if ([item['name'] for item in c['dedup_negative_cases']] != ['block_index_out_of_range','block_map_dimensions',
            'missing_unique_block','noncanonical_first_occurrence','duplicate_dictionary_value','dictionary_dimensions',
            'accounting_bytes','release_exceeds_live'] or len(c['memory_negative_cases'])!=6):
        raise ValueError('all original6 memory and8 independent dictionary/release guards are required')
    c["inherited_source_pairs_must_reexecute"] = 1146
    c["additional_permutation_source_pairs"] = 6
    c["dense_reference_only_one_runtime_group_live"] = True
    c["dense_reference_group_address_is_one_not_physics_input"] = True
    c["memory_stream_layout"] = dict(endianness="little", integer_header="12 int64", real_field="IEEE REAL64",
        dense_header=["version","nstate","nblock","logical_group","reference_runtime_group","flux_count","cour_count","xnei_count","zero","zero","zero","zero"],
        dense_payload=["full lower REAL64[nstate,nstate,nblock] Fortran order","flux","cour","xnei"],
        packed_header=["version","nstate","nblock","nrow","logical_group","factor_bytes","live","peak","cap","built","reused","hits"],
        packed_payload=["actual ascending rowmap int32[nrow]","actual blockmap int32[nblock]","unique_count int32[1]",
            "first-occurrence dictionary REAL64[nrow,nstate,nunique] Fortran order"],
        decoded_header=["version","nstate","nblock","nrow","logical_group","workspace_bytes","before_live","reserved_live","peak","cap","zero","zero"],
        decoded_payload=["all actual LOAD full REAL64[nstate,nstate,nblock] streamed block by block"],
        packed_version=2,primitive_version=2,
        primitive_header=["version","nstate","nblock","saved_row_count","allocated_rows","dictionary_dim1","dictionary_dim2","dictionary_dim3","factor_bytes","live","peak","cap"],
        primitive_payload=["actual DU REAL32[nstate]","full original lower REAL64[nstate,nstate,nblock]",
            "allocated rowmap int32[allocated_rows]","map_count int32[1]","unique_count int32[1]",
            "allocated blockmap int32[map_count]","allocated dictionary REAL64[dictionary_dim1,dictionary_dim2,dictionary_dim3]"],
        original_memory_primitive_shape=[4,3],additional_dictionary_primitive_shapes=[[4,6],[4,6],[4,49]],
        raw_numeric_PASSED_by_Fortran_driver=False, all_actual_raw_must_be_archived_before_finite_or_bitwise_audit=True)
    control_proof=control_source_equivalence()
    proof=changed["proof"]
    if (proof["parent_kernel_sha256"] != MEMORY_KERNEL_SOURCE_SHA or proof["complete_inverse_byteexact"] is not True
            or proof['scope']!='ORDINARY_RANK1_PERSISTENT_LOWER_RAW_BIT_DICTIONARY_ONLY'
            or proof['dense_parent_kernel_sha256']!=KERNEL_SOURCE_SHA
            or proof['rank1_factor_cache_budget_bytes']!=536870912
            or proof['new_plan_descriptor_fields_covered_by_parent_4096_bytes'] is not True
            or proof["factorization_and_pivots_unchanged"] is not True or proof["RHS_order_unchanged"] is not True
            or proof["legacy_and_uncached_formula_bytes_retained"] is not True or proof["sender_changed"] is not False
            or proof["actual_controls_executed"] is not False or proof["actual_native_RSS_passed"] is not False
            or dense["proof"]["complete_inverse_byteexact"] is not True
            or dense["proof"]["production_link_must_exclude_this_object"] is not True):
        raise ValueError("only exact reversible ordinary-rank1 storage patch is admitted as source")
    return dict(kernel=changed["kernel"],reference_kernel=ref["reference_kernel"],dense_reference_kernel=dense["kernel"],
        proof=proof,dense_reference_proof=dense["proof"],original_reference_proof=ref["proof"],control_source_proof=control_proof),c


def archive_forecast(contract, changed):
    """Exact fixed raw sizes plus complete all-unique dictionary bounds before roots."""
    def input_bytes(f, modes=None):
        nr,nh,nq,nl,nm=[f[k] for k in ('nreg2d','nfloor','npq','nsct','nmode')]
        nm=nm if modes is None else modes
        return 96+4*(nh+nh*nr+nh+4+4*nl+nr*nm+nr+4+2*nq+nl*nq)+8*(nr*3+1)
    total=0; variable_dictionary_upper=0; parts=[]; rows=0
    for f in contract['positive_fixtures']:
        nr,nh,nq,nl=[f[k] for k in ('nreg2d','nfloor','npq','nsct')]
        calls=f['groups']*f['nrhs']*2
        amount=calls*(96+8*(2*nr*nh*nl+nr*(nh+1)+nr*nq))+(f['groups']+1)*input_bytes(f)
        if f['rank1']:
            amount+=f['groups']*(3*96+4*(nq//2)+8*(2*nq*nq*(nh+1)+(nq//2)*nq*(nh+1)
                +nr*nh*nl+nr*(nh+1)+nr*nq))
            amount+=f['groups']*(4*(nh+1)+4)
            variable_dictionary_upper+=f['groups']*(100+4*(nq//2)+4*(nh+1)+8*(nq//2)*nq*(nh+1))
            rows+=3*f['groups']
        total+=amount; rows+=calls+1
        parts.append(dict(name=f['name'],complete_binary_bytes_upper_bound=amount))
    prime=contract['positive_fixtures'][0]
    for c in contract['negative_cases']:
        total+=96+8*(2*8*48*3+8*49+8*32)+input_bytes(prime)+input_bytes(prime,2 if c['name']=='dims' else None)
        dictionary_upper=100+4*16+4*49+8*16*32*49
        total+=dictionary_upper+96+8*32*32*49
        variable_dictionary_upper+=dictionary_upper
        total+=len((c['expected_message']+'\n').encode()); rows+=3
    for c in contract['cap_negative_cases']:
        total+=96+len((c['expected_message']+'\n').encode()); rows+=1
    # V2 original memory primitives retain every original lower/DU field.
    primitive_before=504;primitive_stored=716
    total+=primitive_before+primitive_stored+312+480;rows+=4
    for case in contract['memory_negative_cases']:
        mutation_bytes=(504 if case['name'] in ('omitted_nonzero','omitted_negative_zero')
            else 652 if case['name']=='packed_dimensions' else 716)
        total+=primitive_before+mutation_bytes+len((case['expected_message']+'\n').encode());rows+=3
    for fixture in contract['dedup_control_contract']['dedup_positive_fixtures']:
        blocks,unique=fixture['nblock'],fixture['expected_unique']
        total+=(120+128*blocks)+(128+132*blocks+64*unique)+(108+4*blocks+64*unique)+(96+128*blocks);rows+=4
    for case in contract['dedup_negative_cases']:
        mutation_bytes=1108 if case['name']=='block_map_dimensions' else 1048 if case['name']=='dictionary_dimensions' else 1112
        total+=888+1112+mutation_bytes+len((case['expected_message']+'\n').encode())
        if case['name']=='release_exceeds_live':total+=32
        rows+=4
    total+=28*8+104+104+184; rows+=2
    source_bytes=sum(len(changed[k].encode()) for k in ('kernel','reference_kernel','dense_reference_kernel'))
    source_bytes+=require(CONTROL_SOURCE).stat().st_size+require(PARENT/'runtime/run_bounded_dragon.py').stat().st_size
    allowance=1*2**30; manifest_allowance=rows*2048
    forecast=total+source_bytes+manifest_allowance+allowance
    if forecast>=ARCHIVE_RESERVE:
        raise ValueError('complete exact raw archive and all build/source allowances exceed original 2GiB')
    return dict(schema='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_COMPLETE_ARCHIVE_FORECAST_V1',
        complete_scope_roots=[str(SOURCE),str(OUT)],complete_control_raw_binary_and_abort_message_bytes_upper_bound=total,
        fixed_control_raw_binary_and_abort_message_bytes=total-variable_dictionary_upper,
        variable_dictionary_raw_bytes_upper_bound=variable_dictionary_upper,
        variable_dictionary_forecast_uses_all_blocks_unique=True,
        exact_copied_source_bytes=source_bytes,declared_manifest_rows_upper_bound=rows,
        manifest_json_allowance_bytes=manifest_allowance,nonraw_binary_diff_watch_log_and_metadata_allowance_bytes=allowance,
        forecast_complete_bytes=forecast,original_archive_reserve_bytes=ARCHIVE_RESERVE,positive_fixtures=parts,
        actual_complete_archive_cap_remains_mandatory=True,actual_production_transport_outputs_not_in_this_build=True)


def production_cache_shape_forecast(parent,contract):
    original=copy.deepcopy(parent_factory().production_cache_shape_forecast(parent['inherited_moment_order_admission'],
        read(PARENT/'declaration.json')['control_contract']))
    f=contract['positive_fixtures'][0]
    synthetic=cache_accounting(f); physical=cache_accounting(f,nmat=24)
    peak=physical['final_retained_bytes']+max(physical['raw_key_bytes'],physical['projected_key_bytes'],physical['hit_workspace_bytes'])
    if peak>=536870912:
        raise ValueError('complete packed production cache forecast exceeds inherited accounted cap')
    return dict(schema='AXMAT_RANK1_MEMORY_DEDUP_STORED_TRACK_FORECAST_V1',inherited_actual_shape_witness=original,
        inherited_completed_memory_shape_forecast=read(MEMORY_ROOT/'declaration.json')['stored_production_shape_cache_forecast'],
        NREG2D=8,NFLOOR=48,NPQ=32,NSCT=3,NSNAP=3,TRACK_material_bound=24,synthetic_controls_NMAT=3,
        actual_positive_rows=16,synthetic_cache_accounting=synthetic,material_bound_cache_accounting=physical,
        predicted_peak_accounted_bytes=peak,accounted_cache_cap_bytes=536870912,
        all370_dense_lower_gross_bytes_removed=370*16*32*49*8,
        all370_persistent_rowmap_bytes_added=370*16*4,
        all370_net_persistent_factor_storage_bytes_saved=370*(16*32*49*8-16*4),
        additional_per_hit_full_reconstruction_accounted_bytes=32*32*8,
        dictionary_forecast_uses_worst_case49_unique_per_group=True,
        all370_additional_persistent_blockmap_bytes=370*49*4,
        dictionary_cardinality_not_inferred_from_prior_partial_capture=True,
        forecast_is_not_actual_production_RSS_measurement=True,fresh_native_RSS_under_512_required=True)


def stage_commands(d,expected):
    exe=str(OUT/'runtime/rank1_factor_cache_memory_dedup_controls')
    return [*d['build_commands'],[exe,*d['control_contract']['positive_command_args']],
        *[[exe,*c['args']] for c in [*d['control_contract']['negative_cases'],*d['control_contract']['cap_negative_cases']]],
        [exe,*d['control_contract']['memory_positive_command_args']],
        *[[exe,*c['args']] for c in d['control_contract']['memory_negative_cases']],
        [exe,*d['control_contract']['dedup_positive_command_args']],
        *[[exe,*c['args']] for c in d['control_contract']['dedup_negative_cases']],
        [d['build_python_executable'],str(Path(__file__).resolve()),'audit-build','--sha256',expected]]


def stage_labels(d):
    return [f'build/build_{i:02d}' for i in range(len(d['build_commands']))]+['controls/positive/execute']+[
        'controls/negative_'+c['name']+'/execute' for c in [*d['control_contract']['negative_cases'],*d['control_contract']['cap_negative_cases']]
        ]+['controls/memory_positive/execute']+['controls/memory_negative_'+c['name']+'/execute'
        for c in d['control_contract']['memory_negative_cases']]+['controls/dedup_positive/execute']+[
        'controls/dedup_negative_'+c['name']+'/execute' for c in d['control_contract']['dedup_negative_cases']]+['audit/audit']


def prepare_build(parent_seal,parent_terminal,parent_terminal_sha,failed_capture_terminal_sha,patch_sha,controls_sha,
                  memory_seal,memory_terminal,memory_terminal_sha,failed_memory_capture_terminal_sha):
    for path in (SOURCE,OUT,TERMINAL): absent(path)
    parent=predecessor_admission(parent_seal,parent_terminal,parent_terminal_sha)
    failed=failed_capture_admission(failed_capture_terminal_sha)
    memory_parent=memory_predecessor_admission(memory_seal,memory_terminal,memory_terminal_sha,parent)
    memory_failed=failed_memory_capture_admission(failed_memory_capture_terminal_sha)
    old,originals=source_inputs(); changed,c=patch_admission(patch_sha,controls_sha)
    forecast=archive_forecast(c,changed); shape=production_cache_shape_forecast(parent,c)
    h=helper(); full,production=h.modules(); guard_files=h.guard_admission(full)
    h.environment(old)
    compiler=old['build_commands'][0][0]
    link=list(old['build_commands'][2]); link[link.index(str(KERNEL_OBJECT))]=str(OUT/'build/SPOT1P64.o'); link[-1]=str(OUT/'runtime/Dragon')
    restore=list(link); restore[restore.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT); restore[-1]=str(PARENT/'runtime/Dragon')
    if restore!=old['build_commands'][2]:raise ValueError('sole kernel link inverse must be exact')
    common=[compiler,'-O2','-march=native','-ffp-contract=off','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
        '-I'+str(OUT/'build'),'-I'+str(ANG),'-I'+str(ROOT/'lib/Darwin_arm64/modules'),
        '-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(OUT/'build')]
    commands=[[*common,'-c',str(SOURCE/'SPOT1P64.f90'),'-o',str(OUT/'build/SPOT1P64.o')],link,
        [*common,'-c',str(SOURCE/'SPOT1P64.original_reference.f90'),'-o',str(OUT/'build/SPOT1P64.original_reference.o')],
        [*common,'-c',str(SOURCE/'SPOT1P64.dense_reference.f90'),'-o',str(OUT/'build/SPOT1P64.dense_reference.o')],
        [*common,'-c',str(SOURCE/'rank1_factor_cache_memory_dedup_controls.f90'),'-o',str(OUT/'build/rank1_factor_cache_memory_dedup_controls.o')],
        [compiler,'-O2','-march=native','-ffp-contract=off','-g',str(OUT/'build/rank1_factor_cache_memory_dedup_controls.o'),
        str(OUT/'build/SPOT1P64.o'),str(OUT/'build/SPOT1P64.original_reference.o'),str(OUT/'build/SPOT1P64.dense_reference.o'),
        str(WHITE_OBJECT),str(ROOT/'lib/Darwin_arm64/libDragon.a'),str(ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a'),
        str(ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a'),str(ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a'),
        '-o',str(OUT/'runtime/rank1_factor_cache_memory_dedup_controls')]]
    files=dict(old['files']); files.update(originals)
    memory_decl=read(require(MEMORY_ROOT/'declaration.json'))
    for path,wanted in memory_decl['files'].items():
        if path in files and files[path]!=wanted:raise ValueError('memory prerequisite owner SHA conflict')
        files[path]=wanted
    files.update({str(MEMORY_ROOT/name):sha for name,sha in read(MEMORY_ROOT/'seal.json')['files'].items()})
    files.update({str(PARENT/name):sha for name,sha in read(PARENT/'seal.json')['files'].items()})
    for value in (parent['actual_external_terminal_evidence'],parent['actual_external_terminal_validation']['full_stdout'],
            failed['terminal'],*failed['proofs'].values()):files[value['path']]=value['sha256']
    for value in (memory_parent['actual_external_terminal_evidence'], memory_parent['actual_external_terminal_validation']['full_stdout'],
            memory_parent['actual_external_terminal_validation']['full_stderr'], *memory_failed['proofs'].values()):
        if value['path'] in files and files[value['path']]!=value['sha256']:raise ValueError('new failed-input owner SHA conflict')
        files[value['path']]=value['sha256']
    for path in (Path(__file__).resolve(),PARENT_FACTORY,PARENT/'seal.json',MEMORY_FACTORY,MEMORY_ROOT/'seal.json',PATCH_HELPER,CONTROL_SOURCE,
            Path('/usr/bin/nm'),Path('/usr/bin/otool'),Path('/usr/bin/dwarfdump'),Path('/bin/ps'),*guard_files):
        files[str(path)]=digest(require(path))
    roots=history_roots(sorted(set(old['resource_roots'])|{str(SOURCE),str(OUT),str(TERMINAL),failed['root'],
        str(Path(failed['terminal']['path']).parent),str(MEMORY_ROOT),str(MEMORY_SOURCE),str(MEMORY_TERMINAL),memory_failed['root'],
        memory_failed['source_root'],str(Path(memory_failed['terminal']['path']).parent)}),ART)
    resources=resources_for(roots,production.ResourceFailure); before=resource_admission(resources)
    preserved=copy.deepcopy(old['preserved_predecessors']);preserved.append(dict(root=str(PARENT),inventory=h.inventory(PARENT)))
    preserved.append(dict(root=str(MEMORY_ROOT),inventory=h.inventory(MEMORY_ROOT)))
    preserved.append(dict(root=str(MEMORY_SOURCE),inventory=h.inventory(MEMORY_SOURCE)))
    # Prepare the real constructor's runtime input before declaration. No
    # duplicate class or altered __init__/__file__/parent callable is used.
    SOURCE.mkdir();OUT.mkdir()
    for name in ('build','runtime','controls','audit',FAMILY):(OUT/name).mkdir()
    names=['positive',*["negative_"+x['name'] for x in [*c['negative_cases'],*c['cap_negative_cases']]],
        'memory_positive',*["memory_negative_"+x['name'] for x in c['memory_negative_cases']],
        'dedup_positive',*["dedup_negative_"+x['name'] for x in c['dedup_negative_cases']]]
    if len(commands)+len(names)+1!=40:raise ValueError('all original31 and additional9 guarded stages must remain declared')
    for name in names:(OUT/'controls'/name).mkdir()
    for name,key in (('SPOT1P64.f90','kernel'),('SPOT1P64.original_reference.f90','reference_kernel'),
            ('SPOT1P64.dense_reference.f90','dense_reference_kernel')):(SOURCE/name).write_text(changed[key])
    shutil.copy2(require(CONTROL_SOURCE,controls_sha),SOURCE/'rank1_factor_cache_memory_dedup_controls.f90')
    runner=require(PARENT/'runtime/run_bounded_dragon.py');shutil.copy2(runner,OUT/'runtime/run_bounded_dragon.py')
    if (OUT/'runtime/run_bounded_dragon.py').read_bytes()!=runner.read_bytes():raise ValueError('actual runtime constructor input copy must be byteexact')
    files[str(OUT/'runtime/run_bounded_dragon.py')]=digest(OUT/'runtime/run_bounded_dragon.py')
    (SOURCE/'SPOT1P64.patch').write_text(''.join(difflib.unified_diff(MEMORY_KERNEL_SOURCE.read_text().splitlines(True),
        changed['kernel'].splitlines(True),fromfile=str(MEMORY_KERNEL_SOURCE),tofile=str(SOURCE/'SPOT1P64.f90'))))
    write_new(SOURCE/'source_admission.json',dict(schema='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_SOURCE_ADMISSION_V1',
        actual_original_source_objects=originals,source_patch_proof=changed['proof'],dense_reference_proof=changed['dense_reference_proof'],
        inherited_completed_memory_source_admission=memory_parent['source_admission'],
        actual_dictionary_parent_source=pin(MEMORY_KERNEL_SOURCE),dictionary_parent_is_not_dense_reference=True,
        original_reference_proof=changed['original_reference_proof'],control_source_proof=changed['control_source_proof'],sole_new_production_objects=['SPOT1P64.o'],
        unchanged_sender_object=pin(SENDER_OBJECT),unchanged_Flu_selector_object=parent['compiled_selector'],
        unchanged_white_object=pin(WHITE_OBJECT),whole_link_inverse_restoration_exact=True,control_contract=c,
        reference_objects_unit_only=True,actual_full_FLU_entry_executed=False,native_RSS_proof_obtained=False,
        fresh_512MiB_native_capture_required=True,scientific_qualification=False))
    inv=h.inventory(SOURCE);files.update({str(SOURCE/name):sha for name,sha in inv['files'].items()})
    d=dict(schema='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_DECLARATION_V1',family=FAMILY,source_root=str(SOURCE),source_inventory=inv,source_directories=exact_directories(SOURCE),
        files=files,build_commands=commands,production_link_command=commands[1],inherited_rank1_factor_cache_admission=parent,
        inherited_rank1_factor_cache_memory_admission=memory_parent,actual_failed_compact_memory_native_capture_evidence=memory_failed,
        actual_failed_cold_AAA_evidence=parent['actual_failed_cold_AAA_evidence'],actual_failed_native_capture_evidence=failed,
        patch_helper=pin(PATCH_HELPER),controls_source=pin(CONTROL_SOURCE),control_contract=c,complete_archive_forecast=forecast,
        stored_production_shape_cache_forecast=shape,preserved_predecessors=preserved,build_python_executable=old['build_python_executable'],
        native_library_aliases=old['native_library_aliases'],numerical_loader_environment=old['numerical_loader_environment'],
        resource_roots=roots,resources_before=before,artifact_budget_bytes=HISTORY_CAP,min_free_bytes=FREE_FLOOR,
        archive_reserve_bytes=ARCHIVE_RESERVE,total_wall_seconds=TOTAL_WALL,stage_wall_seconds=STAGE_WALL,rss_cap_mib=RSS_CAP,
        threads=1,numeric_children_at_once=1,retries=0,rank1_factor_cache_budget_bytes=536870912,
        resource_scope_policy=HISTORY_SCOPE_POLICY,resource_scope_contract=resource_scope_contract(),
        actual_external_terminal_return_contract=terminal_contract(old['build_python_executable']),
        future_actual_factor_cache_observer_required=cache_observer_contract(),actual_full_FLU_entry_executed=False,transport_launched=False,
        inherited_selector_source_controls_not_newly_executed=True,white_closure_unchanged=True,physical_data_unchanged=True,
        radial_arithmetic_unchanged=True,angle_grid_unchanged=True,original_accuracy_thresholds_changed=False,coefficient_fitting=False,
        fresh_cold_AAA_required=True,fresh_512MiB_native_capture_required=True,native_RSS_proof_obtained=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    h.environment(d);write_new(OUT/'declaration.json',d)
    if archive_bytes()>=ARCHIVE_RESERVE:raise ValueError('complete SOURCE plus OUT exceeded original 2GiB reservation')
    resources.check()
    print(json.dumps(dict(declaration=str(OUT/'declaration.json'),declaration_sha256=digest(OUT/'declaration.json'),
        source_root=str(SOURCE),classification='DECLARED_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_ONLY'),allow_nan=False))


def environment(d, require_build_interpreter=True):
    helper().environment(d, require_build_interpreter=require_build_interpreter)
    if d["resource_scope_policy"] != HISTORY_SCOPE_POLICY or d["resource_scope_contract"] != resource_scope_contract():
        raise ValueError("actual inherited axial-family policy differs")
    validate_history_roots(history_roots(d["resource_roots"], ART), ART)


def declaration_admission(expected,require_build_interpreter=True):
    d=read(require(OUT/'declaration.json',expected))
    if (not re.fullmatch(r'[0-9a-f]{64}',expected or '') or d['schema']!='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_DECLARATION_V1'
            or d['family']!=FAMILY or d['source_root']!=str(SOURCE) or d['total_wall_seconds']!=1800 or d['stage_wall_seconds']!=600
            or d['rss_cap_mib']!=512 or d['archive_reserve_bytes']!=2*2**30 or d['artifact_budget_bytes']!=96*2**30
            or d['min_free_bytes']!=8*2**30 or d['threads']!=1 or d['numeric_children_at_once']!=1 or d['retries']!=0
            or d['rank1_factor_cache_budget_bytes']!=536870912 or d['actual_full_FLU_entry_executed'] is not False
            or d['AAA_accuracy_qualified'] is not False or d['ABA_admitted'] is not False
            or d['native_RSS_proof_obtained'] is not False or d['fresh_512MiB_native_capture_required'] is not True
            or d['actual_external_terminal_return_contract']!=terminal_contract(d['build_python_executable'])
            or d['future_actual_factor_cache_observer_required']!=cache_observer_contract()):
        raise ValueError('immutable original caps and memory-only input scope differ')
    if d['production_link_command']!=d['build_commands'][1]:raise ValueError('explicit actual production link command differs')
    environment(d,require_build_interpreter);helper().verify_inventory(SOURCE,d['source_inventory'])
    if exact_directories(SOURCE)!=d["source_directories"]:raise ValueError("complete source directory namespace changed")
    prior=d['inherited_rank1_factor_cache_admission']
    if predecessor_admission(PARENT_SEAL,prior['actual_external_terminal_evidence']['path'],prior['actual_external_terminal_evidence']['sha256'])!=prior:
        raise ValueError('actual compulsory complete parent return changed')
    memory_prior=d['inherited_rank1_factor_cache_memory_admission']
    if memory_predecessor_admission(MEMORY_SEAL_SHA,memory_prior['actual_external_terminal_evidence']['path'],
            memory_prior['actual_external_terminal_evidence']['sha256'],prior)!=memory_prior:
        raise ValueError('actual compulsory complete memory return changed')
    memory_failed=d['actual_failed_compact_memory_native_capture_evidence']
    if failed_memory_capture_admission(memory_failed['terminal']['sha256'])!=memory_failed:
        raise ValueError('retained failed compact-memory capture changed')
    failed=d['actual_failed_native_capture_evidence']
    if failed_capture_admission(failed['terminal']['sha256'])!=failed:raise ValueError('retained failed capture identity changed')
    changed,c=patch_admission(d['patch_helper']['sha256'],d['controls_source']['sha256'])
    if c!=d['control_contract'] or archive_forecast(c,changed)!=d['complete_archive_forecast'] or production_cache_shape_forecast(prior,c)!=d['stored_production_shape_cache_forecast']:
        raise ValueError('complete source/controls/shape/archive contract changed')
    for name,key in (('SPOT1P64.f90','kernel'),('SPOT1P64.original_reference.f90','reference_kernel'),('SPOT1P64.dense_reference.f90','dense_reference_kernel')):
        if (SOURCE/name).read_text()!=changed[key]:raise ValueError('actual new complete source differs from reversible source proof')
    if (SOURCE/'rank1_factor_cache_memory_dedup_controls.f90').read_bytes()!=CONTROL_SOURCE.read_bytes():raise ValueError('actual controls source differs')
    return d


def check_watch(stage):
    item = helper().check_watch(OUT, stage)
    watch = read(item["path"])
    if (watch["command"] != stage["command"] or watch["rss_cap_mib"] != RSS_CAP
            or not 0 < watch["wall_cap_seconds"] <= stage["wall_cap_seconds"] <= STAGE_WALL
            or not 0 <= watch["elapsed_seconds"] < watch["wall_cap_seconds"]):
        raise ValueError("actual and recorded positive stage wall caps must both hold")
    return item


def raw_inventory(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("actual raw control directory missing or aliased")
    files = {}
    for parent, dirs, names in os.walk(folder, followlinks=False):
        if any((Path(parent) / name).is_symlink() for name in [*dirs, *names]):
            raise ValueError("no raw control entry may be a symlink")
        for name in names:
            path = Path(parent) / name
            if not path.is_file():
                raise ValueError("no special raw control file is eligible")
            files[str(path.relative_to(OUT))] = digest(path)
    return files


def control_file(folder, name):
    if type(name) is not str or Path(name).name != name or name in ("", ".", ".."):
        raise ValueError("a raw control filename must be one literal basename")
    return require(Path(folder) / name)


def unpack_finite(raw, code, count):
    size = struct.calcsize("<" + code)
    if len(raw) != size * count:
        raise ValueError("actual raw field has an incorrect byte count")
    values = struct.unpack("<" + str(count) + code, raw)
    if code in ("f", "d") and any(not math.isfinite(item) for item in values):
        raise ValueError("an archived raw control field is nonfinite")
    return values


def input_record(path):
    """Read only one actual primitive fixture; preserve IEEE field bytes."""
    raw = require(path).read_bytes()
    if len(raw) < 96:
        raise ValueError("incomplete primitive input header")
    header = struct.unpack("<12q", raw[:96])
    version, nr, nh, nq, nl, nm, nmat, nsnap, row, white, z0, z1 = header
    if (version != 1 or z0 != 0 or z1 != 0 or white not in (0, 1) or not 1 <= row <= nr
            or any(value <= 0 for value in (nr, nh, nq, nl, nm, nmat, nsnap))
            or max(nr, nh, nq, nl, nm, nmat, nsnap) > 384):
        raise ValueError("unsupported primitive input dimensions/version")
    layout = [("mat1d", "i", nh), ("mat", "i", nh*nr), ("dz", "f", nh),
        ("total", "f", nmat+1), ("sgas", "f", (nmat+1)*nl), ("basis", "f", nr*nm),
        ("volume", "f", nr), ("radial", "d", nr*nsnap), ("ncode", "i", 2),
        ("zcode", "f", 2), ("du", "f", nq), ("w", "f", nq), ("pl", "f", nl*nq),
        ("white_perimeter", "d", 1)]
    offset, fields, values = 96, {}, {}
    for name, code, count in layout:
        length = struct.calcsize("<" + code) * count
        fields[name] = raw[offset:offset+length]
        values[name] = unpack_finite(fields[name], code, count)
        offset += length
    if offset != len(raw):
        raise ValueError("unexpected trailing or missing primitive input bytes")
    return dict(header=header, raw=raw, fields=fields, values=values)


def field_record(folder, record, fixture):
    """One complete returned field, never an assembled surrogate result."""
    path = control_file(folder, record["file"])
    raw = path.read_bytes()
    nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
    counts = (nr*nh*nl, nr*(nh+1), nr*nq)
    expected = (1, nr, nh, nq, nl, nm, record["group"], record["rhs"], *counts, 0)
    if len(raw) < 96 or struct.unpack("<12q", raw[:96]) != expected:
        raise ValueError("actual source/layer/angle returned field header differs")
    unpack_finite(raw[96:], "d", sum(counts))
    q_path = control_file(folder, record["q_file"])
    q = q_path.read_bytes()
    unpack_finite(q, "d", counts[0])
    # The source family is independently constructed in the external auditor,
    # in Fortran q(1,moment,floor,region) storage order, for every actual call.
    independent_q = b"".join(struct.pack("<3d",
        0.125 + record["rhs"]/32.0 + (region+floor)/1024.0,
        record["rhs"]/512.0, -record["rhs"]/1024.0)
        for region in range(1, nr+1) for floor in range(1, nh+1))
    if nl != 3 or q != independent_q:
        raise ValueError("actual independently stored raw P0/P1/P2 source family differs")
    return raw, q


def json_lines(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("duplicate actual control manifest key")
            value[key] = item
        return value
    rows = []
    with require(path).open() as stream:
        for line in stream:
            value = json.loads(line, object_pairs_hook=unique,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite manifest value")))
            if type(value) is not dict:
                raise ValueError("actual manifest must consist solely of JSON object rows")
            rows.append(value)
    return rows


def cache_accounting(fixture,nmat=3,unique_count=None):
    nr,nh,nq,nl,nm=[fixture[k] for k in ('nreg2d','nfloor','npq','nsct','nmode')]
    raw=17+nh+nh*nr+nh+nmat+1+(nmat+1)*nl+nr*nm+nr+nr*3+2*nq+nl*nq+2
    projected=2+nr+nm*nm+2*nm*nm*nh+nm*nm*nl*nh+2*nq*nl
    if fixture['white']:projected+=nq*nq+nm*nm
    rows=nq//2
    blocks=nh+1
    unique_count=blocks if unique_count is None else unique_count
    if type(unique_count) is not int or not 1<=unique_count<=blocks:raise ValueError('actual dictionary cardinality outside complete block range')
    worst=(16*nq*nq+8*rows*nq+12*nq)*blocks+4*rows+4*blocks
    factors=(16*nq*nq+12*nq)*blocks+4*rows+4*blocks+8*rows*nq*unique_count
    return dict(descriptor_bytes=fixture['groups']*4096,raw_key_bytes=raw*8,projected_key_bytes=projected*8,
        factor_bytes_per_group=factors,persistent_bytes_per_group=(raw+projected)*8+factors,
        final_retained_bytes=fixture['groups']*(4096+(raw+projected)*8+factors),hit_workspace_bytes=8*nq*nq,
        dictionary_unique_count=unique_count,dictionary_bytes=8*rows*nq*unique_count,block_map_bytes=4*blocks,
        worst_factor_reservation_bytes_per_group=worst,duplicate_unallocated_bytes_released=worst-factors,
        reservation_peak_is_not_actual_RSS=True)


def check_counters(record, state, fixture, update, unique_count=None):
    keys = ("built", "reused", "hits", "live", "peak", "cap", "legacy_built", "legacy_reused")
    if any(type(record[key]) is not int or record[key] < 0 for key in keys):
        raise ValueError("actual cache counters must be nonnegative integers")
    account = cache_accounting(fixture,unique_count=unique_count)
    if fixture["rank1"]:
        if update:
            if record["rhs"] == 1:
                before = state["live"]
                first = before+2*account["raw_key_bytes"]
                second = before+account["raw_key_bytes"]+2*account["projected_key_bytes"]
                worst = before+account["raw_key_bytes"]+account["projected_key_bytes"]+account["worst_factor_reservation_bytes_per_group"]
                state["live"] += account["persistent_bytes_per_group"]
                state["peak"] = max(state["peak"], first, second, worst, state["live"])
                state["built"] += fixture["nfloor"]+1
            else:
                state["peak"] = max(state["peak"], state["live"]+max(
                    account["raw_key_bytes"], account["projected_key_bytes"], account["hit_workspace_bytes"]))
                state["reused"] += fixture["nfloor"]+1
                state["hits"] += 1
        # Ordinary POD previously had its legacy cache disabled. Its ABI stays
        # at zero; the new rank-one counters are independent int64 values.
        expected = dict(state, cap=536870912, legacy_built=0, legacy_reused=0)
    else:
        if fixture["name"] == "legacy_physical" and update:
            if record["rhs"] == 1:
                state["legacy_built"] += fixture["nmode"]*(fixture["nfloor"]+1)
            else:
                state["legacy_reused"] += fixture["nmode"]*(fixture["nfloor"]+1)
        elif update:
            # The enabled rank-one pool checks raw identity before declining
            # an ineligible dense/translation first call. Its one temporary
            # raw key is accounted even though no plan/factor is retained.
            state["peak"] = max(state["peak"], state["live"]+account["raw_key_bytes"])
        expected = dict(state, cap=536870912)
    if any(record[key] != expected[key] for key in keys):
        raise ValueError("actual cache allocation/build/reuse/identity counters do not match independent accounting")
    if not record["live"] <= record["peak"] <= record["cap"]:
        raise ValueError("cache retained/peak accounted bytes exceed their explicitly new 512MiB cap")


def input_fixture_audit(folder, fixture):
    nr, nh, nq, nl, nm = [fixture[key] for key in ("nreg2d", "nfloor", "npq", "nsct", "nmode")]
    name = fixture["name"]
    base = input_record(control_file(folder, name+".inputs.bin"))
    if base["header"] != (1, nr, nh, nq, nl, nm, 3, 3, 1, int(fixture["white"]), 0, 0):
        raise ValueError("actual fixture primitive dimensions/white closure metadata differs")
    values = base["values"]
    if sum(values["dz"]) != 150.0 or values["ncode"] != ((4, 4) if name == "legacy_translation" else (1, 1)):
        raise ValueError("actual full-height mesh or original boundary control differs")
    if (sum(value > 0 for value in values["du"]) != nq//2
            or sum(value < 0 for value in values["du"]) != nq//2
            or any(value <= 0 for value in values["w"])):
        raise ValueError("actual original ALGPT angular coverage is incomplete")
    for index, direction in enumerate(values["du"]):
        matches = [j for j, other in enumerate(values["du"]) if struct.pack("<f", other) == struct.pack("<f", -direction)]
        if len(matches) != 1 or struct.pack("<f", values["w"][index]) != struct.pack("<f", values["w"][matches[0]]):
            raise ValueError("actual SN directions/weights do not have an exact paired involution")
    if any(values["pl"][nl*index] != 1.0 or values["pl"][nl*index+1] != values["du"][index] for index in range(nq)):
        raise ValueError("actual source-moment angular mapping is not complete P0/P1/P2")
    volume_sum = sum(values["volume"])
    if volume_sum <= 0 or any(value <= 0 for value in values["volume"]):
        raise ValueError("actual radial volumes must be positive")
    gram = [[sum(values["volume"][region]/volume_sum * values["basis"][region+nr*a]
        * values["basis"][region+nr*b] for region in range(nr)) for b in range(nm)] for a in range(nm)]
    if fixture["rank1"] and (gram[0][0] == 1.0 or not any(value < 0 for value in values["basis"])
            or not any(value > 0 for value in values["basis"])):
        raise ValueError("the actual ordinary rank-one fixture must expose signed nonunit Gram coordinates")
    for group in range(1, fixture["groups"]+1):
        changed = input_record(control_file(folder, name+"_g"+str(group)+".inputs.bin"))
        if changed["header"] != base["header"] or any(changed["fields"][key] != base["fields"][key]
                for key in base["fields"] if key != "total"):
            raise ValueError("a group's actual raw operator changed outside the declared total entry")
        variant = 1 if name == "lifecycle_reset_2" else 0
        wanted = base["fields"]["total"][:4]+struct.pack("<f", 1.125+0.0625*variant+group/8192.0)+base["fields"]["total"][8:]
        if changed["fields"]["total"] != wanted:
            raise ValueError("actual group-specific primitive operator/source coverage differs")
    return dict(weighted_Gram=gram, actual_signed_basis=any(value < 0 for value in values["basis"]),
        actual_geometry=[nr, nh, nq, nl, nm], archived_group_inputs=fixture["groups"])


def control_audit(d):
    """Independent streaming audit; all raw files were already hashed first."""
    dirs={"positive","memory_positive","dedup_positive",*["negative_"+c["name"] for c in [*d["control_contract"]["negative_cases"],
        *d["control_contract"]["cap_negative_cases"]]],*["memory_negative_"+c["name"] for c in d["control_contract"]["memory_negative_cases"]],
        *["dedup_negative_"+c["name"] for c in d["control_contract"]["dedup_negative_cases"]]}
    if {p.name for p in (OUT / "controls").iterdir()}!=dirs:raise ValueError("complete declared controls root namespace differs")
    receipt = read(require(OUT / "raw_controls_receipt.json"))
    if receipt["before_numeric_gates"] is not True or receipt["files"] != raw_inventory(OUT / "controls"):
        raise ValueError("complete original raw bytes/hashes must precede every numerical gate")
    c = d["control_contract"]
    if (c["raw_header"] != ["version", "nreg2d", "nfloor", "npq", "nsct", "nmode", "group", "rhs",
            "flux_count", "cour_count", "xnei_count", "reserved_zero"]
            or c["roles"] != ["original", "build", "reuse"] or c["descriptor_bytes_per_group"] != 4096
            or len(c["positive_fixtures"]) != 8 or len(c["negative_cases"]) != 14):
        raise ValueError("actual complete independently interpretable raw control protocol differs")
    memory = memory_controls_audit(d)
    unique_by_group={(row['case'],row['group']):row['unique_count'] for row in memory['actual_group_dictionary_accounting']}
    folder = OUT / "controls/positive"
    rows = json_lines(control_file(folder, "manifest.jsonl"))
    cursor, pairs, scalar_fields, data_bytes = 0, 0, 0, 0
    seen_files = {"manifest.jsonl", "execute.log", "execute.watchdog.json", *memory["positive_extra_files"]}
    fixture_results = []
    expected_terminals = []
    for fixture in c["positive_fixtures"]:
        witness = input_fixture_audit(folder, fixture)
        name = fixture["name"]
        seen_files.add(name+".inputs.bin")
        seen_files.update(name+"_g"+str(group)+".inputs.bin" for group in range(1, fixture["groups"]+1))
        account = cache_accounting(fixture)
        live = account["descriptor_bytes"] if name != "legacy_physical" else 0
        state = dict(built=0, reused=0, hits=0, live=live, peak=live)
        if not fixture["rank1"]:
            state.update(legacy_built=0, legacy_reused=0)
        q_by_rhs = {}
        for group in range(1, fixture["groups"]+1):
            for rhs in range(1, fixture["nrhs"]+1):
                original, cached = rows[cursor:cursor+2]
                cursor += 2
                expected_role = "build" if rhs == 1 else "reuse"
                for record, role, update in ((original, "original", False), (cached, expected_role, True)):
                    stem = name+"_g"+str(group)+"_r"+str(rhs)+"_"+role
                    if (record["kind"] != "field" or record["case"] != name or record["role"] != role
                            or record["group"] != group or record["rhs"] != rhs
                            or record["file"] != stem+".bin" or record["q_file"] != stem+".q.bin"
                            or record["input_file"] != name+"_g"+str(group)+".inputs.bin"):
                        raise ValueError("actual all-group/all-RHS/original-build-hit manifest order differs")
                    check_counters(record, state, fixture, update,
                        unique_by_group[(name,group)] if fixture['rank1'] else None)
                    seen_files.update((record["file"], record["q_file"]))
                reference_raw, reference_q = field_record(folder, original, fixture)
                cached_raw, cached_q = field_record(folder, cached, fixture)
                if reference_raw != cached_raw or reference_q != cached_q:
                    raise ValueError("actual returned flux/cour/xnei fields or source differ bitwise from the uncached original source")
                if rhs in q_by_rhs and reference_q != q_by_rhs[rhs]:
                    raise ValueError("same declared source RHS must remain identical across all groups")
                q_by_rhs[rhs] = reference_q
                pairs += 1
                scalar_fields += (len(reference_raw)-96)//8
                data_bytes += len(reference_raw)+len(cached_raw)+len(reference_q)+len(cached_q)
        if len(set(q_by_rhs.values())) != 3:
            raise ValueError("all three independent changing raw RHS sources must actually occur")
        final_state = dict(state)
        clear = rows[cursor]
        cursor += 1
        if clear != dict(kind="clear", case=name, built=0, reused=0, hits=0, live=0, peak=0):
            raise ValueError("actual lifecycle CLEAR must reset all new counters and all retained cache bytes")
        actual_retained=(account['descriptor_bytes']+sum(cache_accounting(fixture,unique_count=unique_by_group[(name,g)])['persistent_bytes_per_group']
            for g in range(1,fixture['groups']+1))) if fixture['rank1'] else 0
        if fixture["rank1"] and final_state["live"] != actual_retained:
            raise ValueError("all actually filled group plans must equal independent complete allocation accounting")
        fixture_results.append(dict(name=name, source_pairs=fixture["groups"]*fixture["nrhs"],
            primitive_witness=witness, independent_accounting=account, actual_final_counters=final_state,
            all_fields_bitwise_equal=True, lifecycle_zero_verified=True))
        if fixture["rank1"]:
            expected_terminals.append([final_state["built"], final_state["reused"], final_state["hits"],
                final_state["peak"], 536870912])
    pivot = rows[cursor]
    cursor += 1
    if pivot != dict(kind="pivot", original="pivot_original.bin", split="pivot_split.bin", factors="pivot_factors.bin", rows=4, rhs=3):
        raise ValueError("independent pivot/tie/multiple RHS control must be actually archived")
    pivot_inputs = control_file(folder, "pivot_inputs.bin").read_bytes()
    unpack_finite(pivot_inputs, "d", 28)
    matrix_rows = [[0.0, 2.0, 1.0, 0.0], [2.0, 1.0, 0.0, 1.0],
        [-2.0, 0.0, 3.0, 1.0], [1.0, 1.0, 1.0, 4.0]]
    independent_pivot_input = b"".join(struct.pack("<d", matrix_rows[row][column])
        for column in range(4) for row in range(4))
    independent_pivot_input += b"".join(struct.pack("<d", (row-column)/8.0)
        for column in range(1, 4) for row in range(1, 5))
    if pivot_inputs != independent_pivot_input:
        raise ValueError("actual first-tie matrix and all three independent pivot RHS columns differ")
    original = control_file(folder, "pivot_original.bin").read_bytes()
    split = control_file(folder, "pivot_split.bin").read_bytes()
    factors = control_file(folder, "pivot_factors.bin").read_bytes()
    if len(original) != 104 or len(split) != 104 or original[:8] != struct.pack("<q", 0) or split != original:
        raise ValueError("the actual split pivot solver and original ALSBD fields must succeed and be bitwise identical")
    unpack_finite(original[8:], "d", 12)
    if len(factors) != 184 or factors[:8] != struct.pack("<q", 0):
        raise ValueError("actual factorization raw fields/info incomplete")
    unpack_finite(factors[8:136], "d", 16)
    pivot_rows = struct.unpack("<4i", factors[136:152])
    unpack_finite(factors[152:], "d", 4)
    if any(not index+1 <= value <= 4 for index, value in enumerate(pivot_rows)) or pivot_rows[0] != 2:
        raise ValueError("actual strict-first pivot/tie choice differs from original ALSBD")
    seen_files.update(("pivot_inputs.bin", "pivot_original.bin", "pivot_factors.bin", "pivot_split.bin"))
    if rows[cursor:] != [dict(kind="clear", built=0, reused=0, hits=0, live=0, peak=0)]:
        raise ValueError("all actual manifest rows must have been independently interpreted once")
    if {path.name for path in folder.iterdir()} != seen_files:
        raise ValueError("positive complete raw archive namespace differs from the independent expected coverage")
    actual_log = (folder / "execute.log").read_text()
    if "RAW_CONTROLS_COMPLETE" not in actual_log:
        raise ValueError("the complete real positive child return marker is missing")
    terminal_rows = []
    for line in actual_log.splitlines():
        if "AXMAT-RANK1-CACHE TERMINAL" in line:
            match = re.fullmatch(r"\s*AXMAT-RANK1-CACHE TERMINAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*", line)
            if match is None:
                raise ValueError("the actual cache-terminal observer has a malformed five-int64 record")
            terminal_rows.append([int(value) for value in match.groups()])
    if terminal_rows != expected_terminals:
        raise ValueError("every actual unit cache terminal must equal independently counted build/reuse/identity/peak/cap state")
    negative_results = []
    mutation_field = dict(total="total", selfscat="sgas", radial="radial", basis="basis", mesh="dz",
        du="du", weights="w", pl="pl", boundary="ncode", signed_zero="total", white_perimeter="white_perimeter")
    prime_fixture = dict(name="negative", nreg2d=8, nfloor=48, npq=32, nsct=3, nmode=1, groups=2, white=True, rank1=True)
    for case in c["negative_cases"]:
        name = case["name"]
        folder = OUT / "controls" / ("negative_"+name)
        rows = json_lines(control_file(folder, "manifest.jsonl"))
        stem = "negative_"+name
        if len(rows) != 2 or rows[1] != dict(kind="negative_expected", case=name, expected_XABORT=case["expected_message"]):
            raise ValueError("the actual independent negative attempt metadata differs")
        prime = rows[0]
        if (prime["kind"] != "field" or prime["case"] != stem or prime["role"] != "prime"
                or prime["group"] != 1 or prime["rhs"] != 1
                or prime["file"] != stem+"_g1_r1_prime.bin" or prime["q_file"] != stem+"_g1_r1_prime.q.bin"
                or prime["input_file"] != stem+"_prime.inputs.bin"):
            raise ValueError("an actual cached production-shape call must prime each independent negative process")
        account = cache_accounting(prime_fixture)
        state = dict(built=0, reused=0, hits=0, live=account["descriptor_bytes"], peak=account["descriptor_bytes"])
        field_record(folder, prime, prime_fixture)
        first = input_record(control_file(folder, stem+"_prime.inputs.bin"))
        positive_rows=tuple(index+1 for index,v in enumerate(first['values']['du']) if v>0)
        packed,packed_row=audited_storage(folder,stem+'_g1',None,positive_rows)
        if packed['header'][1:5]!=(32,49,16,1) or packed['header'][6:]!=(prime['live'],prime['peak'],536870912,prime['built'],prime['reused'],prime['hits']):
            raise ValueError('independent identity-negative actual priming dictionary/counter dimensions differ')
        check_counters(prime, state, prime_fixture, True,packed['unique_count'])
        changed = input_record(control_file(folder, stem+"_mutated.inputs.bin"))
        if first["header"] != (1, 8, 48, 32, 3, 1, 3, 3, 1, 1, 0, 0):
            raise ValueError("each negative's actual priming operator must have the declared full production shape")
        if first["raw"] == changed["raw"]:
            raise ValueError("a negative control must actually change raw operator identity")
        if name in mutation_field:
            target = mutation_field[name]
            if first["header"] != changed["header"] or any(first["fields"][key] != changed["fields"][key]
                    for key in first["fields"] if key != target) or first["fields"][target] == changed["fields"][target]:
                raise ValueError("the negative operator mutation is outside its exact declared field")
            if name == "signed_zero" and (first["fields"]["total"][:4] != b"\x00\x00\x00\x00"
                    or changed["fields"]["total"][:4] != b"\x00\x00\x00\x80"):
                raise ValueError("the actual IEEE signed-zero identity mutation is missing")
        elif name in ("white_on", "white_row"):
            index, wanted = (9, 0) if name == "white_on" else (8, 2)
            independent_header = list(first["header"])
            independent_header[index] = wanted
            if tuple(independent_header) != changed["header"] or first["fields"] != changed["fields"]:
                raise ValueError("the actual white metadata mutation differs from its declared single-entry control")
        elif name == "dims":
            if first["header"][5] != 1 or changed["header"][5] != 2:
                raise ValueError("the actual mode-count mutation was not independently witnessed")
            wanted = list(first["header"])
            wanted[5] = 2
            if tuple(wanted) != changed["header"] or any(first["fields"][key] != changed["fields"][key]
                    for key in first["fields"] if key != "basis"):
                raise ValueError("the actual dimension guard changed unrelated primitive inputs")
        else:
            raise ValueError("a negative mutation has no independent raw interpretation")
        message = control_file(folder, "actual_XABORT.txt").read_text()
        if message != case["expected_message"]+"\n" or "RAW_ACTUAL_UNIT_XABORT "+case["expected_message"] not in (folder / "execute.log").read_text():
            raise ValueError("the actual kernel guard must refuse through the exact archived expected unit XABORT")
        expected_files = {"manifest.jsonl", "memory_manifest.jsonl", "execute.log", "execute.watchdog.json", "actual_XABORT.txt",
            prime["file"], prime["q_file"], stem+"_prime.inputs.bin", stem+"_mutated.inputs.bin",stem+'_g1_packed.bin',stem+'_g1_decoded.bin'}
        if {path.name for path in folder.iterdir()} != expected_files:
            raise ValueError("each negative must preserve exactly its raw prime/mutation/rejection archive, with no normal return")
        if json_lines(folder/'memory_manifest.jsonl')!=[packed_row]:raise ValueError('actual identity-negative raw dictionary/full-decode observation missing or changed')
        negative_results.append(dict(name=name, actual_message=message.rstrip("\n"),
            raw_prime=pin(folder / (stem+"_prime.inputs.bin")), raw_mutation=pin(folder / (stem+"_mutated.inputs.bin")),
            archived_actual_XABORT=pin(folder / "actual_XABORT.txt"), expected_rejection=True))
    cap_results = []
    for case in c["cap_negative_cases"]:
        name = case["name"]
        folder = OUT / "controls" / ("negative_"+name)
        raw_request = control_file(folder, "cap_request.bin").read_bytes()
        if len(raw_request) != 96:
            raise ValueError("the actual pre-allocation cap request must retain all twelve int64 values")
        request = struct.unpack("<12q", raw_request)
        live = 370*4096
        operation = 1 if name == "cap_reserve" else 2
        asked = 536870912-live+1 if operation == 1 else 0
        expected = (1, operation, 370, 0 if operation == 1 else 2147483647,
            0 if operation == 1 else 49, asked, 0, 0, 0, live, live, 536870912)
        if request != expected:
            raise ValueError("the actual cap negative dimensions/remaining-byte request differ from independent int64 accounting")
        rows = json_lines(control_file(folder, "manifest.jsonl"))
        if rows != [dict(kind="resource_negative_expected", case=name, file="cap_request.bin",
                expected_XABORT=case["expected_message"], operation=operation,
                requested_bytes=asked, live=live, peak=live, cap=536870912)]:
            raise ValueError("actual cap negative metadata must bind the exact archived pre-allocation request")
        message = control_file(folder, "actual_XABORT.txt").read_text()
        if (message != case["expected_message"]+"\n"
                or "RAW_ACTUAL_UNIT_XABORT "+case["expected_message"] not in (folder / "execute.log").read_text()
                or {path.name for path in folder.iterdir()} != {"manifest.jsonl", "memory_manifest.jsonl", "execute.log", "execute.watchdog.json",
                    "cap_request.bin", "actual_XABORT.txt"}):
            raise ValueError("the actual guarded cap call must refuse with its exact raw command-specific unit message and no normal return")
        if (folder / "memory_manifest.jsonl").stat().st_size != 0:raise ValueError("unexpected memory observation in inherited cap negative")
        cap_results.append(dict(name=name, raw_request=pin(folder / "cap_request.bin"),
            actual_XABORT=pin(folder / "actual_XABORT.txt"), expected_rejection=True,
            cache_accounting_preallocation_guard=True, actual_OwnRSS_oversize_child_test=False))
    actual_raw_bytes = sum(require(OUT / name).stat().st_size for name in receipt["files"]
        if name.endswith(".bin") or Path(name).name == "actual_XABORT.txt")
    forecast=d['complete_archive_forecast']
    variable_paths=[OUT/'controls/positive'/(row['case']+'_g'+str(row['group'])+'_packed.bin') for row in memory['actual_group_dictionary_accounting']]
    variable_paths.extend(OUT/'controls'/('negative_'+case['name'])/('negative_'+case['name']+'_g1_packed.bin') for case in c['negative_cases'])
    actual_variable_bytes=sum(require(path).stat().st_size for path in variable_paths)
    if (actual_variable_bytes>forecast['variable_dictionary_raw_bytes_upper_bound'] or actual_raw_bytes!=
            forecast['fixed_control_raw_binary_and_abort_message_bytes']+actual_variable_bytes
            or actual_raw_bytes>forecast['complete_control_raw_binary_and_abort_message_bytes_upper_bound']):
        raise ValueError('complete fixed raw bytes and actual complete dictionaries must satisfy their independently declared exact/upper-bound forecast')
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_FULL_RAW_CONTROLS_AUDIT_V1", status="PASS",
        counts=dict(fixtures=8, inherited_bitwise_source_pairs_reexecuted=1146, additional_permutation_source_pairs=6,
            dense_reference_kernel_calls=memory["dense_reference_calls"], memory_module_negative_calls=6,
            dictionary_positive_primitives=3,dictionary_module_negative_calls=8,original_stages_retained=31,total_declared_stages=40,
            actual_returned_unit_kernel_calls=pairs*2+14+memory["dense_reference_calls"],
            actual_guard_rejected_unit_kernel_calls=14, actual_total_unit_kernel_invocations=pairs*2+28+memory["dense_reference_calls"], bitwise_source_pairs=pairs,
            independent_pivot_rhs=3, negative_calls=14, cache_cap_negative_calls=2, production_groups=370,
            production_layers=48, production_angles=32, source_moments=3,
            bitwise_compared_output_scalars=scalar_fields, compared_actual_field_and_source_bytes=data_bytes),
        memory_controls=memory,dictionary_controls=memory['dictionary_controls'],fixtures=fixture_results, negative_controls=negative_results, cache_cap_negative_controls=cap_results,
        actual_first_tie_pivot=pivot_rows[0], actual_complete_raw_binary_and_abort_message_bytes=actual_raw_bytes,
        actual_cache_terminal_observer_rows=terminal_rows,
        actual_variable_dictionary_raw_bytes=actual_variable_bytes,variable_dictionary_raw_upper_bound_verified=True,
        complete_raw_receipt=pin(OUT / "raw_controls_receipt.json"),
        all_actual_outputs_finite=True, all_flux_cour_xnei_bitwise_equal=True,
        all_sources_independently_reconstructed=True, all370_plans_retained_and_accounted=True,
        all_lifecycle_clears_zero=True, signed_nonunit_Gram_controls=True,
        physical_dense_translation_outputs_bitwise_unchanged=True,
        actual_guard_rejections=True, independent_complete_LU_reconstruction_claimed=False,
        cache_accounting_preallocation_guard_rejections=True, new_OwnRSS_oversize_child_test_claimed=False,
        historical_object_used_in_unit_baseline=False, actual_full_FLU_entry_executed=False,
        original_moment_selector_controls_newly_executed=False,
        scientific_accuracy_or_performance_qualified=False)


def binary_audit(d):
    paths={'new_kernel':OUT/'build/SPOT1P64.o','reference_kernel':OUT/'build/SPOT1P64.original_reference.o',
        'dense_reference_kernel':OUT/'build/SPOT1P64.dense_reference.o','unit_executable':OUT/'runtime/rank1_factor_cache_memory_dedup_controls',
        'actual_Dragon':OUT/'runtime/Dragon'}
    raw={}
    for name,path in paths.items():
        require(path)
        for tool,args in (('symbols',['/usr/bin/nm','-gU',str(path)]),('instructions',['/usr/bin/otool','-tV',str(path)]),
                ('debug',['/usr/bin/dwarfdump','--debug-info',str(path)])):
            r=subprocess.run(args,capture_output=True,check=True,timeout=60);target=OUT/'audit'/(name+'_'+tool+'.txt')
            with target.open('xb') as stream:stream.write(r.stdout)
            raw[name+'_'+tool]=pin(target)
    write_new(OUT/'audit/raw_binary_receipt.json',dict(files=raw,before_binary_gates=True))
    def symbols(name):return [line.split()[-1] for line in Path(raw[name+'_symbols']['path']).read_text().splitlines() if line.split()]
    for name,symbol in (('new_kernel','_spot1p64_'),('reference_kernel','_spot1p64_original_'),('dense_reference_kernel','_spot1p64_dense_')):
        if symbols(name).count(symbol)!=1:raise ValueError('actual uniquely renamed separately compiled routine missing/duplicate')
    for symbol in ('_spot1p64_','_spot1p64_original_','_spot1p64_dense_'):
        if symbols('unit_executable').count(symbol)!=1:raise ValueError('all three actual unit-only kernels need unique linked symbols')
    for symbol in ('_spot1p64_','_flu2dr64_','_flu_'):
        if symbols('actual_Dragon').count(symbol)!=1:raise ValueError('actual normal production override definition missing/duplicate')
    if any(symbol in symbols('actual_Dragon') for symbol in ('_spot1p64_original_','_spot1p64_dense_')):
        raise ValueError('production must exclude every unit reference routine')
    if digest(paths['new_kernel']) in (KERNEL_OBJECT_SHA,MEMORY_KERNEL_OBJECT_SHA) or digest(paths['actual_Dragon']) in (PARENT_RUNTIME_SHA,MEMORY_RUNTIME_SHA):
        raise ValueError('actual new compiled storage object/runtime must differ from original')
    for name,file in (('new_kernel','SPOT1P64.f90'),('reference_kernel','SPOT1P64.original_reference.f90'),('dense_reference_kernel','SPOT1P64.dense_reference.f90')):
        if str(SOURCE/file) not in Path(raw[name+'_debug']['path']).read_text():raise ValueError('actual compilation unit must name declared private source')
    link=list(d['build_commands'][1]);old=read(PARENT/'declaration.json')['build_commands'][2]
    if link.count(str(OUT/'build/SPOT1P64.o'))!=1 or str(KERNEL_OBJECT) in link or str(OUT/'build/SPOT1P64.dense_reference.o') in link:
        raise ValueError('sole new production kernel precedence/reference exclusion differs')
    if link.index(str(OUT/'build/SPOT1P64.o'))>=link.index(str(ROOT/'lib/Darwin_arm64/libDragon.a')):raise ValueError('override must precede original archive')
    link[link.index(str(OUT/'build/SPOT1P64.o'))]=str(KERNEL_OBJECT);link[-1]=str(PARENT/'runtime/Dragon')
    if link!=old:raise ValueError('entire link recipe must invert exactly outside sole new kernel/output')
    return dict(status='PASS',source_and_command_identity_verified=True,exact_parent_link_inverse_restoration=True,
        actual_private_object_definitions_verified=True,executable_definitions_verified=True,raw_metadata=raw,
        actual_objects={key:pin(path) for key,path in paths.items()},unchanged_sender_object=pin(SENDER_OBJECT),
        production_references_excluded=True,unit_three_symbols_unique=True,
        entire_historical_compiled_source_reconstruction_claimed=False,independent_complete_instruction_equivalence_claimed=False,
        independent_LU_reconstruction_claimed=False)


def audit_build(expected):
    d = declaration_admission(expected)
    claim = read(require(OUT / "execution_claim.json"))
    stages = read(require(OUT / FAMILY / "stages.json"))["stages"]
    labels, commands = stage_labels(d), stage_commands(d, expected)
    if (claim["parent_pid"] != os.getppid() or claim["declaration_sha256"] != expected
            or len(stages) != len(labels) or [row["label"] for row in stages] != labels
            or [row["command"] for row in stages] != commands or stages[-1]["command"] != [sys.executable, *sys.argv]
            or stages[-1]["status"] != "RUNNING" or any(row["status"] != "PASS" for row in stages[:-1])):
        raise ValueError("only the actual serial last audit child may accept complete previous stages")
    watches = [check_watch(row) for row in stages[:-1]]
    raw = read(require(OUT / "raw_controls_receipt.json"))
    if raw["files"] != raw_inventory(OUT / "controls") or raw["before_numeric_gates"] is not True:
        raise ValueError("all actual raw controls must be archived before numerical acceptance")
    identity = read(require(OUT / "runtime/build_identity.json"))
    helper().verify({str(OUT / name):sha for name,sha in identity["files"].items()})
    controls = control_audit(d)
    write_new(OUT / "audit/controls.json", controls)
    binary = binary_audit(d)
    write_new(OUT / "audit/binary_identity.json", binary)
    write_new(OUT / "audit/result.json", dict(classification="PASS_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_CONTROLS_ONLY",
        declaration_sha256=expected, control_status=controls["status"], binary_status=binary["status"],
        rank1_factor_cache_controls_passed=True, all_new_cache_outputs_bitwise_equal_to_uncached=True,
        operator_identity_guard_negative_controls_passed=True, rank1_factor_cache_math_and_rhs_order_unchanged=True,
        control_counts=controls["counts"], previous_stage_watchdogs=watches,
        inherited_rank1_factor_cache_admission=d["inherited_rank1_factor_cache_admission"],
        inherited_rank1_factor_cache_memory_admission=d["inherited_rank1_factor_cache_memory_admission"],
        actual_failed_compact_memory_native_capture_evidence=d["actual_failed_compact_memory_native_capture_evidence"],
        actual_failed_cold_AAA_evidence=d["actual_failed_cold_AAA_evidence"],
        inherited_selector_source_controls_not_newly_executed=True, newly_executed_original_interface_receiver_calls=0,
        newly_executed_native_receiver_calls=controls["counts"]["actual_total_unit_kernel_invocations"],
        actual_full_FLU_entry_executed=False, transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False,
        future_actual_factor_cache_observer_required=cache_observer_contract(),
        lower_structural_zero_rows_losslessly_packed=True, full_shape_MATMUL_and_RHS_order_unchanged=True,
        lower_repeated_blocks_losslessly_deduplicated=True,
        all_original_memory_and_dictionary_controls_bitwise_passed=True,
        canonical_dictionary_signed_zero_and_all_unique_fallback_verified=True,
        dictionary_dimensions_indices_canonical_and_release_negative_controls_passed=True,
        all_original_and_memory_controls_bitwise_passed=True,
        rowmap_dimensions_zero_and_cap_negative_controls_passed=True, fresh_512MiB_native_capture_required=True,
        native_RSS_proof_obtained=False,
        fresh_cold_AAA_required=True, coefficient_fitting=False))
    print("AXMAT-RANK1-CACHE-BUILD-AUDITED", flush=True)


def run_build(expected):
    started = time.monotonic()
    d = declaration_admission(expected)
    h = helper()
    full, production = h.modules()
    h.guard_admission(full)
    resources = resources_for(d["resource_roots"], production.ResourceFailure)
    resource_admission(resources)
    write_new(OUT / "execution_claim.json", dict(parent_pid=os.getpid(), declaration_sha256=expected,
        started_unix=time.time(), started_monotonic=started, retries=0))
    remaining = TOTAL_WALL - (time.monotonic()-started)
    if remaining <= 0:
        raise ValueError("whole build budget already exhausted before the first real compilation")
    runner = full.OwnRSSSerialExecutor(OUT, remaining, FAMILY, resources)
    result = dict(classification="FAILED_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_NO_RETRY", error=None,
        actual_full_FLU_entry_executed=False, transport_launched=False, AAA_accuracy_qualified=False, ABA_admitted=False)
    try:
        for index, command in enumerate(d["build_commands"]):
            environment(d)
            runner.execute(OUT / "build", f"build_{index:02d}", command, STAGE_WALL)
        names = ("runtime/Dragon", "runtime/rank1_factor_cache_memory_dedup_controls", "build/SPOT1P64.o", "build/SPOT1P64.dense_reference.o",
            "build/SPOT1P64.original_reference.o", "build/rank1_factor_cache_memory_dedup_controls.o")
        write_new(OUT / "runtime/build_identity.json", dict(files={name:digest(require(OUT / name)) for name in names},
            sole_new_production_overrides=["SPOT1P64.o"], inherited_sender_override=pin(SENDER_OBJECT),
            inherited_Flu_override=read(PARENT / "runtime/build_identity.json")["inherited_Flu_override"]))
        try:
            environment(d)
            command = [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *d["control_contract"]["positive_command_args"]]
            runner.execute(OUT / "controls/positive", "execute", command, STAGE_WALL)
            for case in [*d["control_contract"]["negative_cases"], *d["control_contract"]["cap_negative_cases"]]:
                environment(d)
                runner.execute(OUT / "controls" / ("negative_" + case["name"]), "execute",
                    [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *case["args"]], STAGE_WALL)
            environment(d)
            runner.execute(OUT / "controls/memory_positive", "execute",
                [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *d["control_contract"]["memory_positive_command_args"]], STAGE_WALL)
            for case in d["control_contract"]["memory_negative_cases"]:
                environment(d)
                runner.execute(OUT / "controls" / ("memory_negative_" + case["name"]), "execute",
                    [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *case["args"]], STAGE_WALL)
            environment(d)
            runner.execute(OUT / "controls/dedup_positive", "execute",
                [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *d["control_contract"]["dedup_positive_command_args"]], STAGE_WALL)
            for case in d["control_contract"]["dedup_negative_cases"]:
                environment(d)
                runner.execute(OUT / "controls" / ("dedup_negative_" + case["name"]), "execute",
                    [str(OUT / "runtime/rank1_factor_cache_memory_dedup_controls"), *case["args"]], STAGE_WALL)
        finally:
            # Preserve all returned/partial raw files and actual stdout before
            # any independent finite/bitwise or expected-negative-message gate.
            write_new(OUT / "raw_controls_receipt.json", dict(files=raw_inventory(OUT / "controls"),
                before_numeric_gates=True, declared_control_contract=d["control_contract"]))
        runner.execute(OUT / "audit", "audit", stage_commands(d, expected)[-1], STAGE_WALL,
                       "AXMAT-RANK1-CACHE-BUILD-AUDITED")
        stages = read(OUT / FAMILY / "stages.json")["stages"]
        if (len(stages) != len(stage_labels(d)) or [row["label"] for row in stages] != stage_labels(d)
                or [row["command"] for row in stages] != stage_commands(d, expected)
                or any(row["status"] != "PASS" for row in stages)):
            raise ValueError("all declared build/control/audit stages must actually pass exactly once")
        audit = read(OUT / "audit/result.json")
        if (audit["classification"] != "PASS_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_CONTROLS_ONLY"
                or audit["control_status"] != "PASS" or audit["binary_status"] != "PASS"
                or any(audit[key] is not True for key in ("rank1_factor_cache_controls_passed",
                    "all_new_cache_outputs_bitwise_equal_to_uncached", "operator_identity_guard_negative_controls_passed",
                    "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required",
                    "lower_repeated_blocks_losslessly_deduplicated","all_original_memory_and_dictionary_controls_bitwise_passed",
                    "canonical_dictionary_signed_zero_and_all_unique_fallback_verified",
                    "dictionary_dimensions_indices_canonical_and_release_negative_controls_passed"))):
            raise ValueError("actual complete raw cache controls and compiled override identity must pass")
        result.update(classification="COMPLETE_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_CONTROLS_ONLY", watchdogs=[check_watch(row) for row in stages],
            control_counts=audit["control_counts"], runtime_sha256=digest(OUT / "runtime/Dragon"),
            rank1_factor_cache_budget_bytes=536870912, source_root=str(SOURCE),
            all_new_cache_outputs_bitwise_equal_to_uncached=True, fresh_cold_AAA_required=True)
    except BaseException as error:
        result["error"] = repr(error)
        raise
    finally:
        try:
            environment(d)
            h.verify_inventory(SOURCE, d["source_inventory"])
            result["resources"] = resources.check()
            actual_size, elapsed = archive_bytes(), time.monotonic()-started
            if actual_size >= ARCHIVE_RESERVE or elapsed >= TOTAL_WALL:
                raise ValueError("complete SOURCE plus OUT or whole build wall budget exceeded")
            result.update(elapsed_seconds=elapsed, archive_bytes_before_closeout=actual_size)
        except BaseException as error:
            result.update(classification="FAILED_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_NO_RETRY", error=repr(error),
                elapsed_seconds=time.monotonic()-started)
            write_new(OUT / "driver_result.json", result)
            raise
        write_new(OUT / "driver_result.json", result)
    write_new(OUT / "seal.json", dict(schema="AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_SEAL_V1", directories=exact_directories(OUT), files={
        str(path.relative_to(OUT)):digest(path) for path in OUT.rglob("*") if path.is_file() and not path.is_symlink()}))
    try:
        final_resources = resources.check()
        final_size, final_elapsed = archive_bytes(), time.monotonic()-started
        if final_size >= ARCHIVE_RESERVE or final_elapsed >= TOTAL_WALL:
            raise ValueError("mandatory complete post-seal tail failed")
    except BaseException as error:
        write_new(OUT / "closeout_failure.json", dict(error=repr(error), complete=False,
            AAA_accuracy_qualified=False, ABA_admitted=False))
        raise
    print(json.dumps(dict(result=result, actual_tail_check="PASS", actual_elapsed_seconds=final_elapsed,
        actual_archive_bytes=final_size, actual_resources=final_resources), allow_nan=False), flush=True)


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
    def finite_tree(value):
        if type(value) is float and not math.isfinite(value):raise ValueError("overflow nonfinite external JSON number")
        if type(value) is dict:
            for item in value.values():finite_tree(item)
        elif type(value) is list:
            for item in value:finite_tree(item)
    finite_tree(result)
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
    stderr = terminal_file(e["full_stderr"]["path"], e["full_stderr"]["sha256"])
    stderr_pin = pin(stderr)
    if stderr in (receipt, stdout) or e["full_stderr"] != stderr_pin:raise ValueError("actual full stderr must be independently retained")
    returned = strict_terminal_json(stdout)
    tail = {key: returned[key] for key in TAIL_FIELDS}
    if returned != dict(result=sealed_result, **tail) or any(e[key] != tail[key] for key in TAIL_FIELDS):
        raise ValueError("full actual stdout, sealed result and Root terminal-tail values differ")
    elapsed, retained_bytes, snapshot = tail["actual_elapsed_seconds"], tail["actual_archive_bytes"], tail["actual_resources"]
    actual_bytes = archive_bytes()
    if (tail["actual_tail_check"] != "PASS" or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not sealed_result["elapsed_seconds"] <= elapsed < TOTAL_WALL
            or type(retained_bytes) is not int or not 0 <= retained_bytes < ARCHIVE_RESERVE or retained_bytes != actual_bytes
            or type(snapshot) is not dict or "reason" in snapshot
            or snapshot["artifact_budget_bytes"] != 96 * 2**30 or snapshot["min_free_bytes"] != 8 * 2**30
            or snapshot["resource_scope_policy"] != HISTORY_SCOPE_POLICY
            or snapshot["resource_scope_contract"] != d["resource_scope_contract"]
            or snapshot["declared_resource_roots"] != d["resource_roots"]
            or type(snapshot["resource_roots"]) is not list
            or not set(d["resource_roots"]).issubset(snapshot["resource_roots"])
            or type(snapshot["artifact_bytes"]) is not int
            or not retained_bytes <= snapshot["artifact_bytes"] <= d["artifact_budget_bytes"]
            or type(snapshot["disk_free_bytes"]) is not int or snapshot["disk_free_bytes"] < d["min_free_bytes"]
            or type(snapshot["regular_files"]) is not int or snapshot["regular_files"] < 1
            or type(snapshot["checked_unix"]) not in (int, float) or not math.isfinite(snapshot["checked_unix"])
            or snapshot["checked_unix"] <= 0):
        raise ValueError("actual complete terminal-tail wall/archive/resource gates must hold")
    validate_history_roots(snapshot["resource_roots"], ART)
    return dict(receipt=dict(path=str(receipt), sha256=digest(receipt)), full_stdout=stdout_pin, full_stderr=stderr_pin,
                command=command, schema=TERMINAL_SCHEMA, **tail)


def production_admission(build_seal_sha, terminal_evidence, terminal_evidence_sha256):
    """Future read-only runtime input admission, with no AAA/ABA launch."""
    if not re.fullmatch(r"[0-9a-f]{64}", build_seal_sha or ""):
        raise ValueError("the actual new rank-one-cache build seal hash is mandatory")
    seal = read(require(OUT / "seal.json", build_seal_sha))
    if seal["schema"] != "AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_SEAL_V1":
        raise ValueError("the actual complete new rank-one-cache build seal is required")
    if exact_directories(OUT)!=seal["directories"]:raise ValueError("complete final directory namespace changed")
    actual = {}
    for root, folders, names in os.walk(OUT, followlinks=False):
        if any((Path(root) / name).is_symlink() for name in [*folders, *names]):
            raise ValueError("the final sealed build namespace may contain no symlinks")
        for name in names:
            path = require(Path(root) / name)
            actual[str(path.relative_to(OUT))] = digest(path)
    if set(actual) != set(seal["files"]) | {"seal.json"} or any(actual[name] != sha for name, sha in seal["files"].items()):
        raise ValueError("every final raw/control/watch/binary file must belong to the exact successful sealed namespace")
    declared_sha = digest(OUT / "declaration.json")
    d = declaration_admission(declared_sha, require_build_interpreter=False)
    result = read(require(OUT / "driver_result.json"))
    audit = read(require(OUT / "audit/result.json"))
    flags = ("rank1_factor_cache_controls_passed", "all_new_cache_outputs_bitwise_equal_to_uncached",
        "operator_identity_guard_negative_controls_passed", "rank1_factor_cache_math_and_rhs_order_unchanged", "fresh_cold_AAA_required")
    if (result["classification"] != "COMPLETE_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_CONTROLS_ONLY" or result["error"] is not None
            or audit["classification"] != "PASS_RANK1_FACTOR_CACHE_MEMORY_DEDUP_BUILD_CONTROLS_ONLY"
            or audit["declaration_sha256"] != declared_sha or audit["control_status"] != "PASS" or audit["binary_status"] != "PASS"
            or any(audit[key] is not True for key in flags)
            or audit["inherited_rank1_factor_cache_admission"] != d["inherited_rank1_factor_cache_admission"]
            or audit["inherited_rank1_factor_cache_memory_admission"] != d["inherited_rank1_factor_cache_memory_admission"]
            or audit["actual_failed_compact_memory_native_capture_evidence"] != d["actual_failed_compact_memory_native_capture_evidence"]
            or audit["actual_failed_cold_AAA_evidence"] != d["actual_failed_cold_AAA_evidence"]
            or audit["future_actual_factor_cache_observer_required"] != cache_observer_contract()
            or audit["inherited_selector_source_controls_not_newly_executed"] is not True
            or audit["newly_executed_original_interface_receiver_calls"] != 0
            or audit["newly_executed_native_receiver_calls"] != result["control_counts"]["actual_total_unit_kernel_invocations"]
            or result["actual_full_FLU_entry_executed"] is not False or audit["actual_full_FLU_entry_executed"] is not False
            or any(result[key] is not False or audit[key] is not False for key in ("transport_launched", "AAA_accuracy_qualified", "ABA_admitted"))
            or result["rank1_factor_cache_budget_bytes"] != 536870912
            or result["runtime_sha256"] != digest(OUT / "runtime/Dragon")
            or result["control_counts"] != audit["control_counts"]):
        raise ValueError("only complete raw cache controls and genuine compiled overrides may admit this runtime as an input")
    if any(audit[k] is not True for k in ("lower_structural_zero_rows_losslessly_packed",
            "full_shape_MATMUL_and_RHS_order_unchanged", "all_original_and_memory_controls_bitwise_passed",
            "rowmap_dimensions_zero_and_cap_negative_controls_passed", "fresh_512MiB_native_capture_required",
            "lower_repeated_blocks_losslessly_deduplicated","all_original_memory_and_dictionary_controls_bitwise_passed",
            "canonical_dictionary_signed_zero_and_all_unique_fallback_verified",
            "dictionary_dimensions_indices_canonical_and_release_negative_controls_passed")) or audit["native_RSS_proof_obtained"] is not False:
        raise ValueError("actual memory control result must pass without claiming native RSS")
    controls = control_audit(d)
    if controls != read(OUT / "audit/controls.json") or controls["counts"] != result["control_counts"]:
        raise ValueError("actual full raw finite/bitwise/coverage/allocation audit differs from its sealed result")
    binary = read(require(OUT / "audit/binary_identity.json"))
    if (binary["status"] != "PASS" or binary["source_and_command_identity_verified"] is not True
            or binary["exact_parent_link_inverse_restoration"] is not True
            or binary["actual_private_object_definitions_verified"] is not True
            or binary["executable_definitions_verified"] is not True):
        raise ValueError("actual normal compiled-source/object/link provenance is required")
    for value in [*binary["raw_metadata"].values(), *binary["actual_objects"].values()]:
        require(value["path"], value["sha256"])
    identity = read(require(OUT / "runtime/build_identity.json"))
    if (identity["sole_new_production_overrides"] != ["SPOT1P64.o"]
            or identity["inherited_Flu_override"] != read(PARENT / "runtime/build_identity.json")["inherited_Flu_override"]
            or identity["inherited_sender_override"] != pin(SENDER_OBJECT)):
        raise ValueError("the actual compiled 15/16 selector object and sole new override set must remain exact")
    helper().verify({str(OUT / name):sha for name,sha in identity["files"].items()})
    stages = read(require(OUT / FAMILY / "stages.json"))["stages"]
    if (len(stages) != len(stage_labels(d)) or [row["label"] for row in stages] != stage_labels(d)
            or [row["command"] for row in stages] != stage_commands(d, declared_sha)
            or any(row["status"] != "PASS" for row in stages)):
        raise ValueError("all actual original serial guarded build/control/audit stages must pass once")
    watches = [check_watch(row) for row in stages]
    if watches != result["watchdogs"] or watches[:-1] != audit["previous_stage_watchdogs"]:
        raise ValueError("actual final watchdogs must match both independent child and parent verification")
    terminal = external_terminal_admission(d, declared_sha, build_seal_sha, result,
        terminal_evidence, terminal_evidence_sha256)
    # Admit the current complete family history, including legitimate future
    # family roots, without introducing a changing snapshot into this immutable
    # runtime identity that a consuming pipeline must compare exactly.
    resources_for(d["resource_roots"]).check()
    prior = d["inherited_rank1_factor_cache_admission"]
    return dict(schema="AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1",
        admission="RANK1_FACTOR_CACHE_MEMORY_DEDUP_RUNTIME_INPUT_ONLY", build_root=str(OUT), source_root=str(SOURCE),
        build_seal_sha256=build_seal_sha, corrected_runtime=pin(OUT / "runtime/Dragon"),
        compiled_kernel_source=pin(SOURCE / "SPOT1P64.f90"),
        source_admission=pin(SOURCE / "source_admission.json"),
        inherited_rank1_factor_cache_admission=prior, actual_failed_cold_AAA_evidence=d["actual_failed_cold_AAA_evidence"],
        inherited_rank1_factor_cache_memory_admission=d["inherited_rank1_factor_cache_memory_admission"],
        actual_failed_compact_memory_native_capture_evidence=d["actual_failed_compact_memory_native_capture_evidence"],
        actual_failed_native_capture_evidence=d["actual_failed_native_capture_evidence"],
        actual_external_terminal_evidence=terminal["receipt"], actual_external_terminal_validation=terminal,
        future_contract=prior["future_contract"], capture_dependency=prior["capture_dependency"],
        source_and_receiver_controls=prior["source_and_receiver_controls"],
        source_and_receiver_controls_inherited_not_newly_executed=True,
        dispatch_evidence=prior["dispatch_evidence"], predecessor=prior,
        inherited_selector_and_source_unit_controls=dict(compiled_selector=prior["compiled_selector"],
            compiled_unit_controls=prior["compiled_unit_controls"], rows=112, selector_invocations=224,
            source_unit_invocations=192, actual_native_receiver_calls=14, newly_executed=False),
        compiled_selector=prior["compiled_selector"], compiled_unit_controls=pin(OUT / "audit/controls.json"),
        compiled_cache_identity=pin(OUT / "audit/binary_identity.json"),
        actual_control_rows=prior["actual_control_rows"], actual_selector_invocations=prior["actual_selector_invocations"],
        actual_source_unit_invocations=prior["actual_source_unit_invocations"],
        inherited_native_receiver_calls=14, newly_executed_original_interface_receiver_calls=0,
        newly_executed_native_receiver_calls=controls["counts"]["actual_total_unit_kernel_invocations"],
        cache_unit_control_counts=controls["counts"], inherited_selector_source_controls_not_newly_executed=True,
        rank1_factor_cache_controls_passed=True, all_new_cache_outputs_bitwise_equal_to_uncached=True,
        operator_identity_guard_negative_controls_passed=True, rank1_factor_cache_math_and_rhs_order_unchanged=True,
        rank1_factor_cache_budget_bytes=536870912, fresh_cold_AAA_required=True,
        future_actual_factor_cache_observer_required=cache_observer_contract(),
        future_actual_FLU_observer_required=prior["future_actual_FLU_observer_required"],
        future_bounded_progress_observer=dict(prefix="AXMAT-RANK1-CACHE PROGRESS ",
            columns=["IT", "JT", "IGDEB", "EINN", "builtblocks", "reusedblocks", "validated_hits", "peak_accounted_bytes"],
            frequency="First and every 32nd completed inner iteration, ordinary rank-one built pool only",
            scientific_gate=False, iteration_algorithm_and_IPRT_unchanged=True),
        lower_structural_zero_rows_losslessly_packed=True, full_shape_MATMUL_and_RHS_order_unchanged=True,
        lower_repeated_blocks_losslessly_deduplicated=True,
        all_original_memory_and_dictionary_controls_bitwise_passed=True,
        canonical_dictionary_signed_zero_and_all_unique_fallback_verified=True,
        dictionary_dimensions_indices_canonical_and_release_negative_controls_passed=True,
        all_original_and_memory_controls_bitwise_passed=True,
        rowmap_dimensions_zero_and_cap_negative_controls_passed=True, fresh_512MiB_native_capture_required=True,
        native_RSS_proof_obtained=False,
        production_link_command=d["production_link_command"],
        compiled_kernel=pin(OUT / "build/SPOT1P64.o"),
        source_patch_proof=pin(SOURCE / "source_admission.json"),
        actual_resource_class_factory=dict(path=str(parent_factory().PARENT_FACTORY), sha256=parent_factory().PARENT_FACTORY_SHA,
            class_name="DynamicHistoryResources", genuine_class_not_overlay=True),
        corrected_sender_retained=True, white_closure_unchanged=True, collision_self_operator_unchanged=True,
        angle_grid_unchanged=True, radial_arithmetic_unchanged=True, physical_data_unchanged=True,
        original_accuracy_thresholds_changed=False, no_CE_fitting=True,
        resource_scope_policy=HISTORY_SCOPE_POLICY, resource_scope_contract=d["resource_scope_contract"],
        current_complete_history_admission_required=True,
        inherited_physical_flags_scope="Actual completed source-factor/moment-order input controls; no new transport or CE qualification",
        actual_full_FLU_entry_executed=False, full_FLU_entry_execution_proved_by_build=False,
        production_pipeline_prepared=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def failed_capture_admission(expected):
    folder=ART/'axial-material-rank1-cache-native-angular-capture-20261007'
    term=ART/'axial-material-rank1-cache-native-angular-capture-terminal-20261007'
    if expected!=FAILED_CAPTURE_TERMINAL_SHA:raise ValueError("actual retained capture failure Root receipt SHA is mandatory")
    receipt=require(term/'terminal_return.json',expected)
    e=read(receipt)
    if (e['record_producer']!='root' or e['actual_tool_terminal_return_observed'] is not True
            or e['record_written_after_actual_terminal_return'] is not True or e['returncode']!=1
            or e['capture_seal'] is not None or e['failure_classification']!='FAILED_RANK1_NATIVE_ANGULAR_CAPTURE_NO_RETRY'
            or e['diagnostic_admitted'] is not False or e['AAA_accuracy_qualified'] is not False or e['ABA_admitted'] is not False
            or (folder/'seal.json').exists()):
        raise ValueError('actual failed RSS capture must remain retained failure, not success or retried')
    descriptors={k:e[k] for k in ('source','declaration','full_stdout','full_stderr','driver_result','native_watchdog','raw_capture_receipt')}
    for value in descriptors.values(): require(value['path'],value['sha256'])
    result=read(e['driver_result']['path']); w=read(e['native_watchdog']['path'])
    if result['error']!="RuntimeError('own-child 512 MiB RSS cap reached')" or w['sampled_peak_rss_mib']<=512:
        raise ValueError('the original actual native RSS failure evidence differs')
    return dict(root=str(folder),terminal=pin(receipt),proofs=descriptors,
        reason='Actual capture native own-child RSS exceeded 512 MiB; retained failure, never qualification',
        native_RSS_passed=False,diagnostic_admitted=False,AAA_accuracy_qualified=False,ABA_admitted=False)


def failed_memory_capture_admission(expected):
    """Thirteen literal failed-input pins; incomplete fields give no PASS credit."""
    if expected != FAILED_MEMORY_CAPTURE_TERMINAL_SHA:
        raise ValueError("the actual compact-row capture failure Root pin is mandatory")
    folder = ART / "axial-material-rank1-cache-memory-native-angular-capture-20261007"
    source = ART / "axial-material-rank1-cache-memory-native-angular-capture-admission-20261007"
    term = ART / "axial-material-rank1-cache-memory-native-angular-capture-terminal-20261007"
    fixed = {
        "terminal": (term / "terminal_return.json", FAILED_MEMORY_CAPTURE_TERMINAL_SHA),
        "source": (ROOT / "validation/axial_material/prepare_rank1_cache_memory_native_angular_capture.py", "ebc53e9e9fd88c4208ef776333b363d17c27ca2d40f3a09161dbdb51d1c93f8e"),
        "declaration": (folder / "declaration.json", "24d703d9d1214bfe9967b23e0792527483f21cd54c19e1af8f8a16ad70025dea"),
        "full_stdout": (term / "capture_full_stdout.json", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
        "full_stderr": (term / "capture_full_stderr.txt", "a51eec1ce4f46ac63acaa9fed1c4ffab105d93d7ad03a0e712f4bd471e69f987"),
        "driver_result": (folder / "driver_result.json", "564bdb9592f924b98e4d35081fc344ce41ea8ce00473ea781601754481837dca"),
        "execution_claim": (folder / "execution_claim.json", "eebcf94b097a086cd8409725d69ab77f93dbd9a0c4a51c2089a7366a77e4c4fa"),
        "stage_index": (folder / "AAA/stages.json", "c91af17e35efc466501968a759570a8161c7eb2af418f9eb77634be4d4c20235"),
        "raw_capture_receipt": (folder / "raw_capture_receipt.json", "3a3718581cb585c75b89acfb5dda12ec036c60338e74975f287e7f8d0c726ff9"),
        "failed_native_watch": (folder / "AAA/capture_replay.watchdog.json", "63dc61f1b42eacf77dbf56c123fa92378e40683304b17bd6d6ecfa3647bd9052"),
        "failed_native_full_log": (folder / "AAA/capture_replay.log", "b8edd63e322e1978e90f350bde6bd02f16e36c24d6857ec0dca09e131b3b5189"),
        "source_admission": (source / "source_admission.json", "7afcfadc73ddaab5e6bf4257f49f957e8e549eb78d98998e4ed9172276257b00"),
        "capture_module_source": (source / "rank1_cache_capture_angles.f90", "0bc23f7fe5c401460ad153430de703ad1b8570e6a15bbfe0e7d97fb01825991d"),
    }
    proofs = {name: dict(path=str(require(path, wanted)), sha256=wanted) for name, (path, wanted) in fixed.items()}
    e = strict_terminal_json(proofs["terminal"]["path"])
    expected_keys = ("source", "declaration", "full_stdout", "full_stderr", "driver_result", "execution_claim",
        "stage_index", "raw_capture_receipt", "failed_native_watch", "failed_native_full_log")
    if (e["schema"] != "AXMAT_RANK1_MEMORY_NATIVE_ANGULAR_CAPTURE_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1"
            or e["record_producer"] != "root" or e["actual_tool_terminal_return_observed"] is not True
            or e["record_written_after_actual_terminal_return"] is not True or type(e["returncode"]) is not int
            or e["returncode"] != 1 or any(e[name] != proofs[name] for name in expected_keys)
            or e["actual_tool_result"] != dict(initial_chunk_id="3a8eaa", session_id=32364, terminal_chunk_id="457d75", exit_code=1)
            or e["command"] != ["/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12", proofs["source"]["path"],
                "run", "--sha256", proofs["declaration"]["sha256"]]
            or e["capture_seal"] is not None or any(e[name] is not None for name in TAIL_FIELDS)
            or e["actual_completed_build_stages"] != 4 or e["actual_completed_native_stages"] != 0
            or e["actual_raw_capture_files"] != 1283 or e["actual_native_RSS_mib"] != 574.78125
            or e["capture_only"] is not True or e["retries"] != 0
            or any(e[name] is not False for name in ("native_RSS_proof_obtained", "production_solver_promoted",
                "AAA_accuracy_qualified", "ABA_admitted")) or (folder / "seal.json").exists()):
        raise ValueError("actual compact-row capture failure may not be promoted, retried or reclassified")
    result = read(proofs["driver_result"]["path"])
    stages = read(proofs["stage_index"]["path"])["stages"]
    watch = read(proofs["failed_native_watch"]["path"])
    raw = read(proofs["raw_capture_receipt"]["path"])
    if (result["classification"] != "FAILED_RANK1_MEMORY_NATIVE_ANGULAR_CAPTURE_NO_RETRY"
            or result["error"] != "RuntimeError('own-child 512 MiB RSS cap reached')"
            or result["capture_only"] is not True
            or any(result[name] is not False for name in ("production_solver_promoted", "AAA_accuracy_qualified", "ABA_admitted"))
            or [row["label"] for row in stages] != ["build/build_00", "build/build_01", "build/build_02", "build/build_03", "AAA/capture_replay"]
            or [row["status"] for row in stages] != ["PASS", "PASS", "PASS", "PASS", "FAILED"]
            or stages[-1]["error"] != "own-child 512 MiB RSS cap reached"
            or watch["rss_cap_mib"] != 512 or watch["sampled_peak_rss_mib"] != 574.78125 or watch["returncode"] != -15
            or watch["limit_failure"] != result["error"] or watch["own_child_only"] is not True
            or watch["liveness_group_cleanup"] is not True or raw["raw_capture_count"] != 1283
            or raw["before_numeric_gates"] is not True or Path(proofs["full_stdout"]["path"]).stat().st_size != 0):
        raise ValueError("actual retained incomplete compact-row native boundary differs")
    return dict(schema="AXMAT_RANK1_MEMORY_DEDUP_PRIOR_FAILED_CAPTURE_INPUT_V1", root=str(folder), source_root=str(source),
        terminal=proofs["terminal"], proofs=proofs, actual_completed_build_stages=4, actual_completed_native_stages=0,
        incomplete_raw_capture_files=1283, input_only=True, incomplete_raw_used_for_current_bitwise_controls=False,
        native_RSS_passed=False, diagnostic_admitted=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def primitive_record(path):
    raw=require(path).read_bytes()
    if len(raw)<120:raise ValueError('complete V2 primitive raw header/DU/lower required')
    h=struct.unpack('<12q',raw[:96]);n,b=h[1:3]
    if (h[0]!=2 or n!=4 or not 1<=b<=49 or not 0<=h[4]<=n or any(not 0<=x<=49 for x in h[5:8])
            or any(x<0 for x in h[8:11]) or h[11]!=536870912):raise ValueError('primitive V2 dimensions invalid')
    offset=96;du=unpack_finite(raw[offset:offset+4*n],'f',n);offset+=4*n
    lower=raw[offset:offset+8*n*n*b];unpack_finite(lower,'d',n*n*b);offset+=len(lower)
    map_raw=raw[offset:offset+4*h[4]]
    if len(map_raw)!=4*h[4]:raise ValueError('primitive allocated rowmap truncated')
    rowmap=struct.unpack('<'+str(h[4])+'i',map_raw);offset+=len(map_raw)
    if len(raw)<offset+8:raise ValueError('primitive V2 map_count and unique_count missing')
    nmap,unique=struct.unpack('<2i',raw[offset:offset+8]);offset+=8
    if not 0<=nmap<=49 or not 0<=unique<=50:raise ValueError('primitive allocated dictionary count invalid')
    block_raw=raw[offset:offset+4*nmap]
    if len(block_raw)!=4*nmap:raise ValueError('primitive allocated blockmap truncated')
    blockmap=struct.unpack('<'+str(nmap)+'i',block_raw);offset+=len(block_raw)
    packed=raw[offset:];unpack_finite(packed,'d',h[5]*h[6]*h[7])
    return dict(raw=raw,header=h,du=du,lower=lower,map_raw=map_raw,rowmap=rowmap,
        nmap=nmap,unique_count=unique,block_raw=block_raw,blockmap=blockmap,packed=packed)


def independent_primitive():
    values=[]
    for block in range(1,4):
        for column in range(1,5):
            for row in range(1,5):
                if row==1: value=struct.pack('<d',(1+2*column+3*block)/8)
                elif row==3:value=(bytes.fromhex('0000000000000080') if (column,block)==(2,2)
                    else struct.pack('<d',-(3+2*column+3*block)/8))
                else:value=b'\0'*8
                values.append(value)
    return b''.join(values)


def independent_dictionary(full, nstate, nblock, rowmap):
    """First-occurrence dictionaries use complete raw IEEE words, including -0."""
    if (type(nstate) is not int or type(nblock) is not int or not 1<=nstate<=384 or not 1<=nblock<=385
            or len(full)!=8*nstate*nstate*nblock or not rowmap or len(set(rowmap))!=len(rowmap)
            or any(type(row) is not int or not 1<=row<=nstate for row in rowmap)):
        raise ValueError('complete dense lower and actual distinct positive row map required')
    first,blocks,mapping={},[],[]
    kept=set(rowmap)
    for block in range(nblock):
        packed=b''.join(full[8*((row-1)+nstate*column+nstate*nstate*block):
            8*((row-1)+nstate*column+nstate*nstate*block)+8] for column in range(nstate) for row in rowmap)
        for column in range(nstate):
            for row in range(1,nstate+1):
                if row not in kept:
                    at=8*((row-1)+nstate*column+nstate*nstate*block)
                    if full[at:at+8]!=b'\0'*8:raise ValueError('only exact omitted positive-zero lower rows may be packed')
        if packed not in first:
            first[packed]=len(blocks)+1;blocks.append(packed)
        mapping.append(first[packed])
    return dict(unique_count=len(blocks),blockmap=tuple(mapping),dictionary=b''.join(blocks),
        dictionary_bytes=sum(len(block) for block in blocks),block_map_bytes=4*nblock)


def dictionary_record(path):
    raw=require(path).read_bytes()
    if len(raw)<100:raise ValueError('complete V2 dictionary header/maps required')
    header=struct.unpack('<12q',raw[:96]);version,nstate,nblock,nrow,group,factor_bytes,live,peak,cap,built,reused,hits=header
    if (version!=2 or any(type(v) is not int or v<=0 for v in (nstate,nblock,nrow,group))
            or not 1<=nrow<=nstate<=384 or nblock>385 or any(v<0 for v in (factor_bytes,live,peak,built,reused,hits))
            or cap!=536870912 or not live<=peak<=cap):raise ValueError('unsupported complete dictionary dimensions/counter ABI')
    offset=96;row_raw=raw[offset:offset+4*nrow];offset+=4*nrow
    if len(row_raw)!=4*nrow:raise ValueError('complete actual row map missing')
    rowmap=struct.unpack('<'+str(nrow)+'i',row_raw)
    map_raw=raw[offset:offset+4*nblock];offset+=4*nblock
    if len(map_raw)!=4*nblock or len(raw)<offset+4:raise ValueError('complete actual block map missing')
    blockmap=struct.unpack('<'+str(nblock)+'i',map_raw)
    unique=struct.unpack('<i',raw[offset:offset+4])[0];offset+=4
    if not 1<=unique<=nblock:raise ValueError('actual dictionary cardinality outside original complete block count')
    values=raw[offset:];unpack_finite(values,'d',nrow*nstate*unique)
    return dict(raw=raw,header=header,rowmap=rowmap,blockmap=blockmap,unique_count=unique,dictionary=values,
        dictionary_bytes=len(values),block_map_bytes=len(map_raw))


def audited_storage(folder, stem, full, expected_rows):
    """Validate actual packed/full-decode raw files without any transport call."""
    stored=dictionary_record(control_file(folder,stem+'_packed.bin'));ph=stored['header']
    n,b,nrow=ph[1:4]
    decode=control_file(folder,stem+'_decoded.bin').read_bytes()
    if len(decode)!=96+8*n*n*b:raise ValueError('all original full decoded blocks must be archived')
    dh=struct.unpack('<12q',decode[:96]);unpack_finite(decode[96:],'d',n*n*b)
    if full is None:full=decode[96:]
    if stored['rowmap']!=tuple(expected_rows):raise ValueError('actual rows differ from raw DU-positive row indices')
    independent=independent_dictionary(full,n,b,tuple(expected_rows))
    if any(stored[key]!=independent[key] for key in ('unique_count','blockmap','dictionary','dictionary_bytes','block_map_bytes')):
        raise ValueError('complete first-occurrence IEEE dictionary and actual blockmap differ')
    factor=(16*n*n+12*n)*b+4*nrow+4*b+8*nrow*n*stored['unique_count'];work=8*n*n
    if (ph[5]!=factor or dh!=(1,n,b,nrow,ph[4],work,ph[6],ph[6]+work,max(ph[7],ph[6]+work),536870912,0,0)
            or decode[96:]!=full):raise ValueError('full decode bits or precise allocated/workspace accounting differs')
    row=dict(kind='packed',case=stem.rsplit('_g',1)[0],group=ph[4],file=stem+'_packed.bin',decoded_file=stem+'_decoded.bin',
        before_live=ph[6],after_live=ph[6],workspace_bytes=work,peak=max(ph[7],ph[6]+work),
        unique_count=stored['unique_count'],dictionary_bytes=stored['dictionary_bytes'],block_map_bytes=stored['block_map_bytes'],factor_bytes=ph[5])
    return stored,row


def independent_dedup_primitive(name):
    if name not in ('exact_repeated_blocks','permuted_rows_repeated_blocks','all_unique_fallback'):
        raise ValueError('unknown explicitly declared dictionary primitive')
    b=49 if name=='all_unique_fallback' else 6
    rows=(2,4) if name=='permuted_rows_repeated_blocks' else (1,3)
    du=(-.5,.25,-1.,.75) if rows==(2,4) else (.25,-.5,.75,-1.)
    full=bytearray(128*b)
    if b==49:
        for block in range(1,b+1):
            for col in range(1,5):
                for ri,row in enumerate(rows,1):
                    at=8*((row-1)+4*(col-1)+16*(block-1));full[at:at+8]=struct.pack('<d',(block+2*col+3*ri)/16)
    else:
        block=bytearray(128)
        for col in range(1,5):
            for ri,row in enumerate(rows,1):
                at=8*((row-1)+4*(col-1));block[at:at+8]=struct.pack('<d',(2*col+3*ri)/16)
        at=8*((rows[1]-1)+4);block[at:at+8]=b'\0'*8
        full[128:256]=block;full[256:384]=block;full[384:512]=block
        full[384+at:384+at+8]=bytes.fromhex('0000000000000080')
        full[512:640]=full[384:512];full[640:768]=block
    dictionary=independent_dictionary(bytes(full),4,b,rows)
    unique=dictionary['unique_count'];worst=(16*16+12*4)*b+8+4*b+64*b
    factor=worst-64*(b-unique);live=4096+32+factor;peak=4096+32+worst
    return dict(nblock=b,rowmap=rows,du=du,lower=bytes(full),dictionary=dictionary,
        worst_factor=worst,factor=factor,live=live,peak=peak)


def dedup_controls_audit(d):
    c=d['control_contract'];folder=OUT/'controls/dedup_positive'
    if len(c['dedup_control_contract']['dedup_positive_fixtures'])!=3 or len(c['dedup_negative_cases'])!=8:
        raise ValueError('all three dictionary primitives and eight actual refusals must be declared')
    rows=json_lines(control_file(folder,'memory_manifest.jsonl'));expected_rows=[]
    files={'manifest.jsonl','memory_manifest.jsonl','execute.log','execute.watchdog.json'};positives=[]
    for f in c['dedup_control_contract']['dedup_positive_fixtures']:
        name=f['name'];x=independent_dedup_primitive(name);b=x['nblock'];u=x['dictionary']['unique_count']
        if f!=dict(name=name,nstate=4,nrow=2,nblock=b,expected_unique=u):raise ValueError('full dictionary primitive contract changed')
        before_name=name+'_before_store.bin';stored_name=name+'_stored.bin'
        before=primitive_record(control_file(folder,before_name));stored=primitive_record(control_file(folder,stored_name))
        h_before=(2,4,b,2,0,0,0,0,x['worst_factor'],x['peak'],x['peak'],536870912)
        h_stored=(2,4,b,2,2,2,4,u,x['factor'],x['live'],x['peak'],536870912)
        if (before['header']!=h_before or stored['header']!=h_stored or before['du']!=x['du'] or stored['du']!=x['du']
                or before['lower']!=x['lower'] or stored['lower']!=x['lower'] or before['rowmap']!=()
                or before['nmap']!=0 or before['unique_count']!=0 or before['packed']!=b''
                or stored['rowmap']!=x['rowmap'] or stored['nmap']!=b or stored['unique_count']!=u
                or stored['blockmap']!=x['dictionary']['blockmap'] or stored['packed']!=x['dictionary']['dictionary']):
            raise ValueError('raw repeated/permuted/all-unique dictionary primitive changed bits or exact allocation accounting')
        packed,row=audited_storage(folder,name+'_g1',x['lower'],x['rowmap'])
        if packed['header']!=(2,4,b,2,1,x['factor'],x['live'],x['peak'],536870912,0,0,0):
            raise ValueError('primitive dictionary actual retained/reserved byte counters differ')
        expected_rows.extend([dict(kind='dedup_primitive',file=before_name),dict(kind='dedup_primitive',file=stored_name),row,
            dict(kind='memory_clear',case=name,built=0,reused=0,hits=0,live=0,peak=0)])
        files.update((before_name,stored_name,name+'_g1_packed.bin',name+'_g1_decoded.bin'))
        positives.append(dict(name=name,nblock=b,unique_count=u,retained_factor_bytes=x['factor'],
            worst_preallocation_reservation_bytes=x['worst_factor'],unallocated_duplicate_bytes_released=x['worst_factor']-x['factor'],
            original_full_lower=pin(folder/stored_name),complete_full_decode=pin(folder/(name+'_g1_decoded.bin'))))
    if (rows!=expected_rows or {p.name for p in folder.iterdir()}!=files or (folder/'manifest.jsonl').stat().st_size!=0
            or 'RAW_DEDUP_CONTROLS_COMPLETE' not in (folder/'execute.log').read_text()):
        raise ValueError('complete three-primitive dictionary raw namespace/order/CLEAR marker differs')
    x=independent_dedup_primitive('exact_repeated_blocks');b=6;u=3;negative_results=[]
    for case in c['dedup_negative_cases']:
        name=case['name'];folder=OUT/'controls'/('dedup_negative_'+name)
        before=primitive_record(control_file(folder,'dedup_before_store.bin'))
        stored=primitive_record(control_file(folder,'dedup_stored.bin'))
        mut=primitive_record(control_file(folder,'dedup_mutated.bin'))
        if (before['header']!=(2,4,6,2,0,0,0,0,x['worst_factor'],x['peak'],x['peak'],536870912)
                or stored['header']!=(2,4,6,2,2,2,4,3,x['factor'],x['live'],x['peak'],536870912)
                or before['du']!=x['du'] or stored['du']!=x['du'] or before['lower']!=x['lower'] or stored['lower']!=x['lower']
                or before['rowmap']!=() or before['nmap']!=0 or before['unique_count']!=0 or before['packed']!=b''
                or stored['rowmap']!=x['rowmap'] or stored['nmap']!=6 or stored['unique_count']!=3
                or stored['blockmap']!=x['dictionary']['blockmap'] or stored['packed']!=x['dictionary']['dictionary']):
            raise ValueError('each independent dictionary rejection must archive the same actual full primitive and canonical store')
        h=list(stored['header']);maps=stored['blockmap'];nmap=6;unique=3;dictionary=stored['packed']
        if name!='release_exceeds_live':h[9]+=128;h[10]=max(h[10],h[9])
        if name=='block_index_out_of_range':maps=(1,4,2,3,3,2)
        elif name=='block_map_dimensions':nmap=5;maps=(1,2,2,3,3)
        elif name=='missing_unique_block':unique=4
        elif name=='noncanonical_first_occurrence':
            maps=tuple(2 if i==1 else 1 if i==2 else i for i in maps)
            dictionary=dictionary[64:128]+dictionary[:64]+dictionary[128:]
        elif name=='duplicate_dictionary_value':dictionary=dictionary[:128]+dictionary[64:128]
        elif name=='dictionary_dimensions':h[7]=2;dictionary=dictionary[:128]
        elif name=='accounting_bytes':h[8]-=1
        elif name!='release_exceeds_live':raise ValueError('unknown dictionary negative has no explicit raw mutation interpretation')
        if (mut['header']!=tuple(h) or mut['du']!=x['du'] or mut['lower']!=x['lower'] or mut['rowmap']!=x['rowmap']
                or mut['blockmap']!=maps or mut['nmap']!=nmap or mut['unique_count']!=unique or mut['packed']!=dictionary):
            raise ValueError('actual dictionary mutation changed undeclared fields or lacks exact expected damaged bytes')
        files={'manifest.jsonl','memory_manifest.jsonl','execute.log','execute.watchdog.json','actual_XABORT.txt',
            'dedup_before_store.bin','dedup_stored.bin','dedup_mutated.bin'}
        if name=='release_exceeds_live':
            files.add('dedup_release_request.bin')
            if control_file(folder,'dedup_release_request.bin').read_bytes()!=struct.pack('<4q',x['live']+1,x['live'],x['peak'],536870912):
                raise ValueError('real RELEASE over-live request must be archived before the actual rejection')
        expected_rows=[dict(kind='dedup_primitive',file='dedup_before_store.bin'),dict(kind='dedup_primitive',file='dedup_stored.bin'),
            dict(kind='dedup_primitive',file='dedup_mutated.bin'),dict(kind='dedup_negative_expected',case=name,expected_XABORT=case['expected_message'])]
        message=control_file(folder,'actual_XABORT.txt').read_text()
        if (json_lines(control_file(folder,'memory_manifest.jsonl'))!=expected_rows or message!=case['expected_message']+'\n'
                or 'RAW_ACTUAL_UNIT_XABORT '+case['expected_message'] not in (folder/'execute.log').read_text()
                or (folder/'manifest.jsonl').stat().st_size!=0 or {p.name for p in folder.iterdir()}!=files):
            raise ValueError('each real direct/default dictionary LOAD or RELEASE must refuse its precise damaged raw input')
        negative_results.append(dict(name=name,actual_XABORT=pin(folder/'actual_XABORT.txt'),mutation=pin(folder/'dedup_mutated.bin'),expected_rejection=True))
    return dict(schema='AXMAT_RANK1_MEMORY_DEDUP_DICTIONARY_RAW_AUDIT_V1',status='PASS',positive_primitives=positives,
        dictionary_and_release_negative_controls=negative_results,all_original_full_lower_bits_retained=True,
        canonical_first_occurrence_and_signed_zero_verified=True,all_unique_fallback_verified=True,
        actual_worst_reserve_and_duplicate_release_accounted=True,actual_native_RSS_proof_obtained=False,actual_full_FLU_entry_executed=False)


def memory_controls_audit(d):
    """One group at a time; raw receipt already pins every partial/returned byte."""
    c=d['control_contract'];folder=OUT/'controls/positive'
    rows=json_lines(control_file(folder,'memory_manifest.jsonl'))
    cursor=0;extra_files={'memory_manifest.jsonl'};dense_calls=0;lower_bits=0;dictionary_groups=[]
    field_rows=json_lines(control_file(folder,'manifest.jsonl'))
    fields={(r['case'],r['group'],r['rhs'],r['role']):r for r in field_rows if r['kind']=='field'}
    for f in c['positive_fixtures']:
        if not f['rank1']:continue
        n=f['npq'];b=f['nfloor']+1;nrow=n//2
        account=cache_accounting(f)
        dense_fixture=dict(f,groups=1)
        dense_account=parent_factory().cache_accounting(dense_fixture)
        dense_live=dense_account['final_retained_bytes']
        dense_peak=max(4096+2*dense_account['raw_key_bytes'],4096+dense_account['raw_key_bytes']+2*dense_account['projected_key_bytes'],dense_live)
        for group in range(1,f['groups']+1):
            dense,clear,packed=rows[cursor:cursor+3];cursor+=3
            stem=f['name']+'_g'+str(group)
            expected_dense=dict(kind='dense',case=f['name'],group=group,file=stem+'_dense.bin',runtime_group=1,
                built=b,reused=0,hits=0,live=dense_live,peak=dense_peak,cap=536870912)
            if dense!=expected_dense or clear!=dict(kind='dense_clear',case=f['name'],group=group,built=0,reused=0,hits=0,live=0,peak=0):
                raise ValueError('one-group dense c017 reference must actually build once, archive and completely CLEAR')
            raw=control_file(folder,dense['file']).read_bytes();h=struct.unpack('<12q',raw[:96])
            counts=(f['nreg2d']*f['nfloor']*f['nsct'],f['nreg2d']*b,f['nreg2d']*n)
            if h!=(1,n,b,group,1,*counts,0,0,0,0) or len(raw)!=96+8*(n*n*b+sum(counts)):
                raise ValueError('actual dense lower/full field record has wrong explicit ABI')
            full=raw[96:96+8*n*n*b];unpack_finite(full,'d',n*n*b)
            actual_original=control_file(folder,fields[(f['name'],group,1,'original')]['file']).read_bytes()
            if raw[96+8*n*n*b:]!=actual_original[96:]:raise ValueError('same dense source-compiled full fields must be bitwise equal to original uncached fields')
            stored=dictionary_record(control_file(folder,stem+'_packed.bin'));ph=stored['header']
            primitive=input_record(control_file(folder,stem+'.inputs.bin'))
            expected_rows=tuple(i+1 for i,v in enumerate(primitive['values']['du']) if v>0)
            if stored['rowmap']!=expected_rows:raise ValueError('saved map must be exact ascending actual DU-positive indices')
            independent=independent_dictionary(full,n,b,expected_rows)
            if any(stored[k]!=independent[k] for k in ('unique_count','blockmap','dictionary','dictionary_bytes','block_map_bytes')):
                raise ValueError('actual first-occurrence dictionary and complete49-block map differ from dense raw IEEE bits')
            account=cache_accounting(f,unique_count=independent['unique_count'])
            actual_last=fields[(f['name'],group,3,'reuse')]
            if ph!=(2,n,b,nrow,group,account['factor_bytes_per_group'],actual_last['live'],actual_last['peak'],536870912,
                    actual_last['built'],actual_last['reused'],actual_last['hits']):
                raise ValueError('actual dictionary dimensions/counters/factor allocation bytes differ')
            rowmap=stored['rowmap'];values=stored['dictionary']
            dictionary_groups.append(dict(case=f['name'],group=group,unique_count=independent['unique_count'],
                dictionary_bytes=independent['dictionary_bytes'],block_map_bytes=independent['block_map_bytes'],
                actual_factor_bytes=account['factor_bytes_per_group'],worst_factor_reservation_bytes=account['worst_factor_reservation_bytes_per_group']))
            decode=control_file(folder,stem+'_decoded.bin').read_bytes();dh=struct.unpack('<12q',decode[:96]);work=8*n*n
            if dh!=(1,n,b,nrow,group,work,ph[6],ph[6]+work,max(ph[7],ph[6]+work),536870912,0,0):
                raise ValueError('full-shape decode temporary must be reserved before allocation and archived')
            expected_decode=bytearray(8*n*n*b)
            for block in range(b):
                for column in range(n):
                    for ri,row in enumerate(rowmap):
                        target=8*((row-1)+n*column+n*n*block);source=8*(ri+nrow*column+nrow*n*(stored['blockmap'][block]-1))
                        expected_decode[target:target+8]=values[source:source+8]
            if decode[96:]!=expected_decode or decode[96:]!=full:
                raise ValueError('all original dense lower bits including retained signed-zero/omitted +0 must equal packed full decode')
            if packed!=dict(kind='packed',case=f['name'],group=group,file=stem+'_packed.bin',decoded_file=stem+'_decoded.bin',
                    before_live=ph[6],after_live=ph[6],workspace_bytes=work,peak=max(ph[7],ph[6]+work),
                    unique_count=stored['unique_count'],dictionary_bytes=stored['dictionary_bytes'],block_map_bytes=stored['block_map_bytes'],factor_bytes=ph[5]):
                raise ValueError('full decode workspace must actually RELEASE and restore persistent live bytes')
            extra_files.update((dense['file'],packed['file'],packed['decoded_file']));dense_calls+=1;lower_bits+=n*n*b
    if cursor!=len(rows) or dense_calls!=378:raise ValueError('all370 plus lifecycle/signed/permuted dense memory coverage incomplete')
    folder=OUT/'controls/memory_positive';pr=json_lines(control_file(folder,'memory_manifest.jsonl'))
    before=primitive_record(control_file(folder,'primitive_before_store.bin'));stored=primitive_record(control_file(folder,'primitive_stored.bin'))
    full=independent_primitive();factor=1124;live=4096+32+factor
    if (before['header']!=(2,4,3,2,0,0,0,0,factor,live,live,536870912)
            or before['du']!=(.25,-.5,.75,-1.) or before['lower']!=full or before['nmap']!=0 or before['unique_count']!=0
            or stored['header']!=(2,4,3,2,2,2,4,3,factor,live,live,536870912)
            or stored['du']!=before['du'] or stored['lower']!=full or stored['rowmap']!=(1,3)):
        raise ValueError('noncontiguous primitive lower/signed-zero setup not independently witnessed')
    independent=independent_dictionary(full,4,3,(1,3));wanted=independent['dictionary']
    if (stored['packed']!=wanted or stored['blockmap']!=independent['blockmap'] or stored['nmap']!=3 or stored['unique_count']!=3):
        raise ValueError('positive-row signed-zero, canonical dictionary and all block indices must retain exact bits')
    allocated,packedrow=audited_storage(folder,'primitive_g1',full,(1,3))
    if allocated['header']!=(2,4,3,2,1,factor,live,live,536870912,0,0,0):raise ValueError('actual primitive allocation counters differ')
    if pr!=[dict(kind='primitive',file='primitive_before_store.bin'),dict(kind='primitive',file='primitive_stored.bin'),packedrow,
            dict(kind='memory_clear',case='primitive',built=0,reused=0,hits=0,live=0,peak=0)]:
        raise ValueError('actual primitive raw order/reserve release/global CLEAR evidence differs')
    expected_files={'manifest.jsonl','memory_manifest.jsonl','execute.log','execute.watchdog.json','primitive_before_store.bin',
        'primitive_stored.bin','primitive_g1_packed.bin','primitive_g1_decoded.bin'}
    if {p.name for p in folder.iterdir()}!=expected_files or (folder/'manifest.jsonl').stat().st_size!=0 or 'RAW_MEMORY_CONTROLS_COMPLETE' not in (folder/'execute.log').read_text():
        raise ValueError('complete returned primitive raw namespace/terminal marker differs')
    negatives=[]
    for case in c['memory_negative_cases']:
        name=case['name'];folder=OUT/'controls'/('memory_negative_'+name)
        base=primitive_record(control_file(folder,'primitive_before_store.bin'));mut=primitive_record(control_file(folder,'primitive_mutated.bin'))
        if base!=before:raise ValueError('each independent negative must actually prime the same primitive raw input')
        expected_h=list(stored['header']);expected_map=stored['rowmap'];expected_values=stored['packed'];expected_full=full
        expected_blockmap=stored['blockmap'];expected_nmap=stored['nmap'];expected_unique=stored['unique_count']
        if name=='row_count':expected_h[3]=1
        elif name=='row_out_of_range':expected_map=(0,3)
        elif name=='row_duplicate_or_reordered':expected_map=(3,1)
        elif name=='packed_dimensions':expected_h[7]=2;expected_values=wanted[:128]
        elif name in ('omitted_nonzero','omitted_negative_zero'):
            expected_h=list(before['header']);expected_map=();expected_values=b'';expected_blockmap=();expected_nmap=0;expected_unique=0
            pos=8*(1+16);repl=struct.pack('<d',.125) if name=='omitted_nonzero' else bytes.fromhex('0000000000000080')
            expected_full=full[:pos]+repl+full[pos+8:]
        else:raise ValueError('unknown memory rejection has no independent raw mutation interpretation')
        if (mut['header']!=tuple(expected_h) or mut['du']!=before['du'] or mut['lower']!=expected_full
                or mut['rowmap']!=expected_map or mut['packed']!=expected_values or mut['blockmap']!=expected_blockmap
                or mut['nmap']!=expected_nmap or mut['unique_count']!=expected_unique):
            raise ValueError('actual row/dim/omitted-zero negative changed undeclared fields or lacks expected mutation')
        expected_rows=[dict(kind='primitive',file='primitive_before_store.bin'),dict(kind='primitive',file='primitive_mutated.bin'),
            dict(kind='memory_negative_expected',case=name,expected_XABORT=case['expected_message'])]
        if json_lines(control_file(folder,'memory_manifest.jsonl'))!=expected_rows:
            raise ValueError('actual independent negative must archive its mutation before calling the true module guard')
        message=control_file(folder,'actual_XABORT.txt').read_text()
        if (message!=case['expected_message']+'\n' or 'RAW_ACTUAL_UNIT_XABORT '+case['expected_message'] not in (folder/'execute.log').read_text()
                or (folder/'manifest.jsonl').stat().st_size!=0 or {p.name for p in folder.iterdir()}!={
                'manifest.jsonl','memory_manifest.jsonl','primitive_before_store.bin','primitive_mutated.bin','execute.log','execute.watchdog.json','actual_XABORT.txt'}):
            raise ValueError('actual row/dim/+0/-0 guard must reject exactly, with no normal return')
        negatives.append(dict(name=name,actual_message=message.rstrip(),actual_XABORT=pin(folder/'actual_XABORT.txt')))
    dedup=dedup_controls_audit(d)
    return dict(schema='AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_RAW_AUDIT_V1',status='PASS',
        dense_reference_calls=dense_calls,complete_lower_IEEE64_elements_compared=lower_bits,
        actual_group_dictionary_accounting=dictionary_groups,dictionary_controls=dedup,
        positive_extra_files=sorted(extra_files),rowmap_dimension_omitted_zero_negative_controls=negatives,
        all_dense_reference_groups_cleared=True,all_packed_lower_decode_bitwise_equal=True,
        persistent_account_and_full_workspace_reserve_release_verified=True,primitive_signed_zero_bits_retained=True,
        actual_native_RSS_proof_obtained=False,actual_full_FLU_entry_executed=False)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("prepare-build","run-build","audit-build","admit"))
    parser.add_argument("--rank1-cache-build-seal-sha256")
    parser.add_argument("--rank1-cache-terminal-evidence")
    parser.add_argument("--rank1-cache-terminal-evidence-sha256")
    parser.add_argument("--failed-capture-terminal-evidence-sha256")
    parser.add_argument("--memory-build-seal-sha256")
    parser.add_argument("--memory-terminal-evidence")
    parser.add_argument("--memory-terminal-evidence-sha256")
    parser.add_argument("--failed-memory-capture-terminal-evidence-sha256")
    parser.add_argument("--patch-helper-sha256")
    parser.add_argument("--controls-source-sha256")
    parser.add_argument("--sha256")
    parser.add_argument("--terminal-evidence")
    parser.add_argument("--terminal-evidence-sha256")
    args=parser.parse_args()
    {"prepare-build":lambda:prepare_build(args.rank1_cache_build_seal_sha256,args.rank1_cache_terminal_evidence,
        args.rank1_cache_terminal_evidence_sha256,args.failed_capture_terminal_evidence_sha256,
        args.patch_helper_sha256,args.controls_source_sha256,args.memory_build_seal_sha256,
        args.memory_terminal_evidence,args.memory_terminal_evidence_sha256,args.failed_memory_capture_terminal_evidence_sha256),"run-build":lambda:run_build(args.sha256),
     "audit-build":lambda:audit_build(args.sha256),"admit":lambda:print(json.dumps(production_admission(args.sha256,
        args.terminal_evidence,args.terminal_evidence_sha256),allow_nan=False))}[args.action]()
