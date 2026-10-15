"""Source-only lossless lower-row storage change for the ordinary rank1 cache.

No import reads files, imports a production module, or grants an admission.
Only the successful c017 kernel is accepted.  All edits are reversible exact
string substitutions.  Factorization, full-size MATMUL, RHS order, the sender,
and every uncached/legacy formula remain unchanged.  Runtime controls and true
native RSS supervision must pass in a separately declared family.
"""

from __future__ import annotations

import hashlib


SCHEMA = "AXMAT_RANK1_FACTOR_CACHE_MEMORY_SOURCE_PATCH_V1"
PARENT_KERNEL_SHA256 = "c017167b5c48bc922efb7353db8c11a91758add1c2c5a02c42bd2baaeba210a2"
CAP_BYTES = 536870912
ROW_ERROR = "SPOT1P64 RANK1 LOWER: INVALID ROW MAP."
DIMENSION_ERROR = "SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS."
ZERO_ERROR = "SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW."
CAP_ERROR = "SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED."


PACKED_ROUTINES = """  ! Only ordinary rank1 uses this storage.  The full original matrix is
  ! reconstructed before the original full-size MATMUL; no shortened dot
  ! product, different factorization, or floating-point conversion is used.
  subroutine SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)
    integer, intent(in) :: igroup
    double precision, intent(in) :: lower(:,:,:)
    real, intent(in) :: du(:)
    integer :: nstate,nblock,nrow,i,j,block,row
    if (.not.rank1_enabled) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.all(ieee_is_finite(du))) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
    nstate=size(du)
    nblock=size(lower,3)
    nrow=count(du > 0.0)
    if (nstate <= 0 .or. nblock <= 0 .or. nrow <= 0 .or. &
        size(lower,1) /= nstate .or. size(lower,2) /= nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          plan%rank1_factor_bytes <= 0_int64 .or. &
          plan%rank1_lower_rows_count /= nrow) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (allocated(plan%lower) .or. allocated(plan%rank1_lower_rows) .or. &
          allocated(plan%rank1_lower)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      ! Exact INTEGER64 bits, not a numerical zero test: omitted -0 is refused.
      do block=1,nblock
        do j=1,nstate
          do i=1,nstate
            if (du(i) > 0.0) cycle
            if (transfer(lower(i,j,block),0_int64) /= 0_int64) &
              call XABORT('SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW.')
          enddo
        enddo
      enddo
      ! Persistent row indices and packed values were reserved by FACTORS.
      allocate(plan%rank1_lower_rows(nrow),plan%rank1_lower(nrow,nstate,nblock))
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1
        plan%rank1_lower_rows(row)=i
        plan%rank1_lower(row,:,:)=lower(i,:,:)
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_STORE

  subroutine SPOT1P64_RANK1_LOWER_VALIDATE(igroup,nstate,nblock,du)
    integer, intent(in) :: igroup,nstate,nblock
    real, intent(in) :: du(:)
    integer :: nrow,i,row
    if (.not.rank1_enabled .or. nstate <= 0 .or. nblock <= 0 .or. &
        size(du) /= nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.all(ieee_is_finite(du))) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
    nrow=count(du > 0.0)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          nrow <= 0 .or. allocated(plan%lower) .or. &
          plan%rank1_lower_rows_count /= nrow) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (.not.allocated(plan%rank1_lower_rows) .or. &
          .not.allocated(plan%rank1_lower)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (size(plan%rank1_lower_rows) /= nrow .or. &
          size(plan%rank1_lower,1) /= nrow .or. &
          size(plan%rank1_lower,2) /= nstate .or. &
          size(plan%rank1_lower,3) /= nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (any(plan%rank1_lower_rows < 1) .or. &
          any(plan%rank1_lower_rows > nstate)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1
        if (plan%rank1_lower_rows(row) /= i) &
          call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_VALIDATE

  subroutine SPOT1P64_RANK1_LOWER_LOAD(igroup,block,lower,du)
    integer, intent(in) :: igroup,block
    double precision, intent(out) :: lower(:,:)
    real, intent(in) :: du(:)
    integer :: row,nblock
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    nblock=SPOT1P64_PLAN(igroup)%mode(1)%nblock
    call SPOT1P64_RANK1_LOWER_VALIDATE(igroup,size(lower,1), &
      nblock,du)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (size(lower,2) /= plan%nstate .or. block < 1 .or. &
          block > plan%nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      lower=0.0d0
      do row=1,size(plan%rank1_lower_rows)
        lower(plan%rank1_lower_rows(row),:)=plan%rank1_lower(row,:,block)
      enddo
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_LOAD

"""


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _replace(text, old, new, edits):
    if text.count(old) != 1:
        raise ValueError("exact one source anchor required: " + old[:100])
    edits.append({"old": old, "new": new, "count": 1})
    return text.replace(old, new, 1)


def patch_kernel(source):
    """Return only source and inverse witnesses; never compile or execute it."""
    if not isinstance(source, str) or _sha(source) != PARENT_KERNEL_SHA256:
        raise ValueError("actual frozen c017 kernel source required")
    kernel, edits = source, []
    kernel = _replace(kernel, "module SPOT1P64_CACHE_MOD\n"
        "  use, intrinsic :: iso_fortran_env, only: int32,int64\n",
        "module SPOT1P64_CACHE_MOD\n"
        "  use, intrinsic :: iso_fortran_env, only: int32,int64\n"
        "  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite\n", edits)
    kernel = _replace(kernel, "    double precision, allocatable :: lower(:,:,:)\n",
        "    double precision, allocatable :: lower(:,:,:)\n"
        "    integer :: rank1_lower_rows_count=0\n"
        "    integer, allocatable :: rank1_lower_rows(:)\n"
        "    double precision, allocatable :: rank1_lower(:,:,:)\n", edits)
    kernel = _replace(kernel, "  public :: SPOT1P64_FACTOR64,SPOT1P64_SOLVE64\n",
        "  public :: SPOT1P64_FACTOR64,SPOT1P64_SOLVE64\n"
        "  public :: SPOT1P64_RANK1_LOWER_STORE,SPOT1P64_RANK1_LOWER_VALIDATE\n"
        "  public :: SPOT1P64_RANK1_LOWER_LOAD\n", edits)
    kernel = _replace(kernel,
        "  subroutine SPOT1P64_RANK1_FACTORS(igroup,nstate,nblock)\n"
        "    integer, intent(in) :: igroup,nstate,nblock\n"
        "    integer(int64) :: square,amount,blocks\n",
        "  subroutine SPOT1P64_RANK1_FACTORS(igroup,nstate,nblock,npositive)\n"
        "    integer, intent(in) :: igroup,nstate,nblock\n"
        "    integer, optional, intent(in) :: npositive\n"
        "    integer :: positive_rows\n"
        "    integer(int64) :: square,amount,blocks,row_bytes\n", edits)
    kernel = _replace(kernel,
        "    ! factor/lower/cprime REAL64; pivot_value REAL64; pivot INTEGER32.\n"
        "    amount=24_int64*square+12_int64*int(nstate,int64)\n",
        "    positive_rows=nstate\n"
        "    if (present(npositive)) positive_rows=npositive\n"
        "    if (positive_rows <= 0 .or. positive_rows > nstate) &\n"
        "      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')\n"
        "    ! Dense factor/cprime, packed lower; pivots and persistent row map.\n"
        "    amount=16_int64*square+8_int64*int(positive_rows,int64)*int(nstate,int64)+ &\n"
        "      12_int64*int(nstate,int64)\n"
        "    row_bytes=4_int64*int(positive_rows,int64)\n", edits)
    kernel = _replace(kernel, "    amount=amount*blocks\n    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))\n",
        "    amount=amount*blocks\n"
        "    if (row_bytes > RANK1_CAP-amount) &\n"
        "      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')\n"
        "    amount=amount+row_bytes\n"
        "    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))\n", edits)
    kernel = _replace(kernel, "      plan%rank1_factor_bytes=amount\n",
        "      plan%rank1_factor_bytes=amount\n"
        "      plan%rank1_lower_rows_count=positive_rows\n", edits)
    kernel = _replace(kernel, "  subroutine SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)\n",
        PACKED_ROUTINES + "  subroutine SPOT1P64_RANK1_STATS(built,reused,hits,live,peak,cap)\n", edits)
    kernel = _replace(kernel, "    SPOT1P64_RANK1_GUARD,SPOT1P64_RANK1_FACTORS\n",
        "    SPOT1P64_RANK1_GUARD,SPOT1P64_RANK1_FACTORS, &\n"
        "    SPOT1P64_RANK1_LOWER_STORE,SPOT1P64_RANK1_LOWER_VALIDATE, &\n"
        "    SPOT1P64_RANK1_LOWER_LOAD\n", edits)
    kernel = _replace(kernel, "    double precision, allocatable :: solve_pack(:,:),rhs_one(:,:)\n",
        "    double precision, allocatable :: solve_pack(:,:),rhs_one(:,:)\n"
        "    double precision, allocatable :: rank1_lower_work(:,:)\n"
        "    integer(int64) :: rank1_lower_work_bytes\n", edits)
    kernel = _replace(kernel,
        "          if (.not.allocated(plan%lower)) &\n"
        "            call XABORT('SPOT1P64 CACHE: MISSING STORED LOWER BLOCKS.')\n"
        "          if (size(plan%lower,1) /= local_state .or. &\n"
        "              size(plan%lower,2) /= local_state .or. &\n"
        "              size(plan%lower,3) /= nfloor+1) &\n"
        "            call XABORT('SPOT1P64 CACHE: INVALID STORED LOWER BLOCKS.')\n",
        "          if (rank1_identity_active) then\n"
        "            call SPOT1P64_RANK1_LOWER_VALIDATE(igroup,local_state,nfloor+1,du)\n"
        "          else\n"
        "          if (.not.allocated(plan%lower)) &\n"
        "            call XABORT('SPOT1P64 CACHE: MISSING STORED LOWER BLOCKS.')\n"
        "          if (size(plan%lower,1) /= local_state .or. &\n"
        "              size(plan%lower,2) /= local_state .or. &\n"
        "              size(plan%lower,3) /= nfloor+1) &\n"
        "            call XABORT('SPOT1P64 CACHE: INVALID STORED LOWER BLOCKS.')\n"
        "          endif\n", edits)
    kernel = _replace(kernel, "        allocate(rhs_one(local_state,1))\n",
        "        if (rank1_identity_active) then\n"
        "          if (int(local_state,int64) > 536870912_int64/8_int64/int(local_state,int64)) &\n"
        "            call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')\n"
        "          rank1_lower_work_bytes=8_int64*int(local_state,int64)*int(local_state,int64)\n"
        "          call SPOT1P64_RANK1_RESERVE(rank1_lower_work_bytes)\n"
        "          allocate(rank1_lower_work(local_state,local_state))\n"
        "        endif\n"
        "        allocate(rhs_one(local_state,1))\n", edits)
    kernel = _replace(kernel,
        "            if (block > 1) rhs_one(:,1)=rhs_one(:,1)- &\n"
        "              matmul(plan%lower(:,:,block),dprime(:,block-1))\n",
        "            if (rank1_identity_active) then\n"
        "              if (block > 1) then\n"
        "                call SPOT1P64_RANK1_LOWER_LOAD(igroup,block,rank1_lower_work,du)\n"
        "                rhs_one(:,1)=rhs_one(:,1)- &\n"
        "                  matmul(rank1_lower_work,dprime(:,block-1))\n"
        "              endif\n"
        "            else\n"
        "            if (block > 1) rhs_one(:,1)=rhs_one(:,1)- &\n"
        "              matmul(plan%lower(:,:,block),dprime(:,block-1))\n"
        "            endif\n", edits)
    kernel = _replace(kernel, "            call SPOT1P64_RANK1_FACTORS(igroup,local_state,nfloor+1)\n",
        "            call SPOT1P64_RANK1_FACTORS(igroup,local_state,nfloor+1,count(du > 0.0))\n", edits)
    kernel = _replace(kernel,
        "          allocate(plan%lower(local_state,local_state,nfloor+1))\n"
        "          plan%lower=lower\n",
        "          if (rank1_identity_active) then\n"
        "            call SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)\n"
        "          else\n"
        "          allocate(plan%lower(local_state,local_state,nfloor+1))\n"
        "          plan%lower=lower\n"
        "          endif\n", edits)
    kernel = _replace(kernel, "    if (allocated(rhs_one)) deallocate(rhs_one)\n",
        "    if (allocated(rhs_one)) deallocate(rhs_one)\n"
        "    if (allocated(rank1_lower_work)) then\n"
        "      deallocate(rank1_lower_work)\n"
        "      call SPOT1P64_RANK1_RELEASE(rank1_lower_work_bytes)\n"
        "    endif\n", edits)
    restored = kernel
    for edit in reversed(edits):
        if restored.count(edit["new"]) != 1:
            raise ValueError("source inverse anchor is ambiguous")
        restored = restored.replace(edit["new"], edit["old"], 1)
    if restored != source:
        raise ValueError("complete c017 source inverse must be byte-exact")
    if any(len(line) > 132 for line in kernel.splitlines()):
        raise ValueError("private free-form Fortran source exceeds 132 columns")
    return {"kernel": kernel, "proof": {
        "schema": SCHEMA, "parent_kernel_sha256": PARENT_KERNEL_SHA256,
        "candidate_kernel_sha256": _sha(kernel), "inverse_kernel_sha256": _sha(restored),
        "edits": edits, "complete_inverse_byteexact": True,
        "scope": "ORDINARY_RANK1_PERSISTENT_LOWER_STORAGE_ONLY",
        "activation": "rank1_identity_active; no global-enable or legacy-only shortcut",
        "row_map": "Actual du>0 original 1..npq order; count, shape, bounds and every index checked",
        "omitted_rows": "Exact +0 INTEGER64 bits required for every omitted row/column/block",
        "retained_bits": "REAL64 assignments preserve every positive-row IEEE value including signed zero",
        "hit_operation": "Reconstruct full original nstate by nstate contiguous +0 block then same full MATMUL",
        "persistent_accounting": "(16*nstate^2+8*npositive*nstate+12*nstate)*nblock+4*npositive bytes",
        "hit_temporary_accounting": "8*nstate^2 reserved before allocation and released after deallocation",
        "rank1_factor_cache_budget_bytes": CAP_BYTES,
        "factorization_and_pivots_unchanged": True, "RHS_order_unchanged": True,
        "legacy_and_uncached_formula_bytes_retained": True,
        "sender_changed": False, "other_runtime_objects_changed": False,
        "actual_controls_executed": False, "actual_full_FLU_entry_executed": False,
        "actual_native_RSS_passed": False, "AAA_accuracy_qualified": False, "ABA_admitted": False}}


def control_contract():
    """Additional source-control plan; inherited controls must also rerun."""
    return {"schema": "AXMAT_RANK1_FACTOR_CACHE_MEMORY_CONTROL_PLAN_V1",
        "parent_kernel_sha256": PARENT_KERNEL_SHA256,
        "inherited_bitexact_pairs": 1146, "inherited_operator_negative_cases": 14,
        "inherited_cap_negative_cases": 2, "all_inherited_controls_must_reexecute": True,
        "rank1_factor_cache_budget_bytes": CAP_BYTES,
        "additional_positive_requirements": [
            "Permuted noncontiguous positive-angle rows, including positive-row -0 bits",
            "Every full decoded block versus original full lower bytes before any numeric gate",
            "Full original shape MATMUL outputs and complete flux/cour/xnei bitwise equal",
            "All 370 persistent row maps/packed values/factors/keys and exact live/peak bytes",
            "Hit workspace reservation visible before decode and released afterward",
            "CLEAR/lifecycle reset releases all packed allocations and returns live to zero"],
        "additional_negative_cases": [
            {"name": "row_count", "expected_message": DIMENSION_ERROR},
            {"name": "row_out_of_range", "expected_message": ROW_ERROR},
            {"name": "row_duplicate_or_reordered", "expected_message": ROW_ERROR},
            {"name": "packed_dimensions", "expected_message": DIMENSION_ERROR},
            {"name": "omitted_nonzero", "expected_message": ZERO_ERROR},
            {"name": "omitted_negative_zero", "expected_message": ZERO_ERROR}],
        "raw_before_gate": True, "new_build_and_native_RSS_proof_required": True,
        "observed_RSS_reduction_is_not_a_qualification": True,
        "AAA_accuracy_qualified": False, "ABA_admitted": False}


def dense_reference_kernel(source):
    """Unit-only c017 reference with only module and entry-symbol renames."""
    if not isinstance(source, str) or _sha(source) != PARENT_KERNEL_SHA256:
        raise ValueError("actual frozen c017 dense reference source required")
    edits = [
        ("SPOT1P64_CACHE_MOD", "AXMAT_DENSE_CACHE_MOD", 3),
        ("subroutine SPOT1P64(", "subroutine SPOT1P64_DENSE(", 1),
        ("end subroutine SPOT1P64\n", "end subroutine SPOT1P64_DENSE\n", 1)]
    result = source
    for old, new, count in edits:
        if result.count(old) != count:
            raise ValueError("unit dense reference rename anchor differs")
        result = result.replace(old, new)
    inverse = result
    for old, new, count in reversed(edits):
        if inverse.count(new) != count:
            raise ValueError("unit dense reference inverse rename differs")
        inverse = inverse.replace(new, old)
    if inverse != source:
        raise ValueError("unit dense reference must restore all c017 bytes")
    return {"kernel": result, "proof": {
        "schema": "AXMAT_RANK1_MEMORY_UNIT_DENSE_REFERENCE_RENAME_V1",
        "parent_kernel_sha256": PARENT_KERNEL_SHA256,
        "reference_kernel_sha256": _sha(result), "inverse_kernel_sha256": _sha(inverse),
        "only_module_and_entry_symbol_renames": True, "complete_inverse_byteexact": True,
        "unit_only": True, "production_link_must_exclude_this_object": True,
        "only_one_reference_group_may_be_live_at_once": True,
        "full_original_arithmetic_and_array_shapes_retained": True,
        "actual_compiled_or_executed": False}}
