"""Unfrozen, source-only exact block dictionary for the c0 rank1 lower cache.

No import performs I/O or imports a production module.  This changes retained
storage only; all original full-size floating-point operations remain in the
parent kernel.  No runtime, RSS, transport, or scientific pass is claimed.
"""
from __future__ import annotations

import hashlib

SCHEMA = "AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_SOURCE_PATCH_V1"
PARENT_KERNEL_SHA256 = "c0fddcd2ddc4dba6969440024a9205fbb297727a6a045886acba626323ab5718"
DENSE_PARENT_KERNEL_SHA256 = "c017167b5c48bc922efb7353db8c11a91758add1c2c5a02c42bd2baaeba210a2"
PARENT_PATCH_SHA256 = "d3e8a696363b58ab181d3ee6496d30fb50e44b83a5dd3079d697ae77233b0f78"
PARENT_CONTROLS_SHA256 = "3ddb64b634026a70be5a5bf024ff09b00837e8d8942823a6c54f9834cca3ccd9"
CAP_BYTES = 536870912
ROW_ERROR = "SPOT1P64 RANK1 LOWER: INVALID ROW MAP."
DIMENSION_ERROR = "SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS."
ZERO_ERROR = "SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW."
BLOCK_MAP_ERROR = "SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP."
DICTIONARY_ERROR = "SPOT1P64 RANK1 LOWER: DUPLICATE DICTIONARY BLOCK."
CAP_ERROR = "SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED."

DEDUP_ROUTINES = """  ! Only ordinary rank1 uses this storage.  Equality is INTEGER64 IEEE
  ! equality. First occurrence defines dictionary order; 49 unique blocks
  ! remain valid. Decode preserves full original matrix shape and arithmetic.
  subroutine SPOT1P64_RANK1_LOWER_STORE(igroup,lower,du)
    integer, intent(in) :: igroup
    double precision, intent(in) :: lower(:,:,:)
    real, intent(in) :: du(:)
    integer :: nstate,nblock,nrow,i,j,block,row,prior,match,nunique
    integer(int64) :: released_bytes
    logical :: equal_bits
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
    nstate=size(du); nblock=size(lower,3); nrow=count(du > 0.0)
    if (nstate <= 0 .or. nblock <= 0 .or. nrow <= 0 .or. &
        size(lower,1) /= nstate .or. size(lower,2) /= nstate) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          plan%rank1_factor_bytes <= 0_int64 .or. &
          plan%rank1_lower_rows_count /= nrow) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (allocated(plan%lower) .or. allocated(plan%rank1_lower_rows) .or. &
          allocated(plan%rank1_lower) .or. allocated(plan%rank1_lower_blocks) .or. &
          plan%rank1_lower_unique_count /= 0) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      do block=1,nblock
        do j=1,nstate
          do i=1,nstate
            if (du(i) > 0.0) cycle
            if (transfer(lower(i,j,block),0_int64) /= 0_int64) &
              call XABORT('SPOT1P64 RANK1 LOWER: NONZERO OR SIGNED ZERO OMITTED ROW.')
          enddo
        enddo
      enddo
      ! FACTORS reserved all row/map and worst-case 49-unique value bytes.
      ! No temporary packed matrix or floating-point equality is constructed.
      allocate(plan%rank1_lower_rows(nrow),plan%rank1_lower_blocks(nblock))
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1; plan%rank1_lower_rows(row)=i
      enddo
      nunique=0
      do block=1,nblock
        match=0
        do prior=1,block-1
          equal_bits=.true.
          do j=1,nstate
            do row=1,nrow
              i=plan%rank1_lower_rows(row)
              if (transfer(lower(i,j,block),0_int64) /= &
                  transfer(lower(i,j,prior),0_int64)) equal_bits=.false.
            enddo
          enddo
          if (equal_bits) then
            match=plan%rank1_lower_blocks(prior)
            exit
          endif
        enddo
        if (match == 0) then
          nunique=nunique+1; match=nunique
        endif
        plan%rank1_lower_blocks(block)=match
      enddo
      allocate(plan%rank1_lower(nrow,nstate,nunique))
      do block=1,nblock
        match=plan%rank1_lower_blocks(block)
        if (block > 1) then
          if (any(plan%rank1_lower_blocks(:block-1) == match)) cycle
        endif
        do j=1,nstate
          do row=1,nrow
            plan%rank1_lower(row,j,match)=lower(plan%rank1_lower_rows(row),j,block)
          enddo
        enddo
      enddo
      plan%rank1_lower_unique_count=nunique
      released_bytes=8_int64*int(nrow,int64)*int(nstate,int64)*int(nblock-nunique,int64)
      call SPOT1P64_RANK1_RELEASE(released_bytes)
      plan%rank1_factor_bytes=plan%rank1_factor_bytes-released_bytes
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_STORE

  subroutine SPOT1P64_RANK1_LOWER_VALIDATE(igroup,nstate,nblock,du,check_unique)
    integer, intent(in) :: igroup,nstate,nblock
    real, intent(in) :: du(:)
    logical, optional, intent(in) :: check_unique
    integer :: nrow,i,row,block,highest,which,other,j,nunique
    integer(int64) :: expected_bytes,square
    logical :: equal_bits,deep
    deep=.true.
    if (present(check_unique)) deep=check_unique
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
      nunique=plan%rank1_lower_unique_count
      if (plan%nstate /= nstate .or. plan%nblock /= nblock .or. &
          nrow <= 0 .or. allocated(plan%lower) .or. &
          plan%rank1_lower_rows_count /= nrow .or. nunique <= 0 .or. nunique > nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (.not.allocated(plan%rank1_lower_rows) .or. .not.allocated(plan%rank1_lower) .or. &
          .not.allocated(plan%rank1_lower_blocks)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (size(plan%rank1_lower_rows) /= nrow .or. &
          size(plan%rank1_lower,1) /= nrow .or. size(plan%rank1_lower,2) /= nstate .or. &
          size(plan%rank1_lower,3) /= nunique .or. size(plan%rank1_lower_blocks) /= nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      if (any(plan%rank1_lower_rows < 1) .or. any(plan%rank1_lower_rows > nstate)) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      row=0
      do i=1,nstate
        if (du(i) <= 0.0) cycle
        row=row+1
        if (plan%rank1_lower_rows(row) /= i) &
          call XABORT('SPOT1P64 RANK1 LOWER: INVALID ROW MAP.')
      enddo
      highest=0
      do block=1,nblock
        which=plan%rank1_lower_blocks(block)
        if (which < 1 .or. which > nunique .or. which > highest+1) &
          call XABORT('SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.')
        highest=max(highest,which)
      enddo
      if (highest /= nunique) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID CANONICAL BLOCK MAP.')
      if (deep) then
        do which=1,nunique
          do other=1,which-1
            equal_bits=.true.
            do j=1,nstate
              do row=1,nrow
                if (transfer(plan%rank1_lower(row,j,which),0_int64) /= &
                    transfer(plan%rank1_lower(row,j,other),0_int64)) equal_bits=.false.
              enddo
            enddo
            if (equal_bits) call XABORT('SPOT1P64 RANK1 LOWER: DUPLICATE DICTIONARY BLOCK.')
          enddo
        enddo
      endif
      ! Keep the parent's checked extreme-dimension boundary before products.
      if (int(nstate,int64) > RANK1_CAP/24_int64/int(nstate,int64)) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      square=int(nstate,int64)*int(nstate,int64)
      expected_bytes=16_int64*square+12_int64*int(nstate,int64)
      if (int(nblock,int64) > RANK1_CAP/expected_bytes) &
        call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')
      expected_bytes=expected_bytes*int(nblock,int64)+ &
        8_int64*int(nrow,int64)*int(nstate,int64)*int(nunique,int64)+ &
        4_int64*int(nrow,int64)+4_int64*int(nblock,int64)
      if (expected_bytes /= plan%rank1_factor_bytes) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    end associate
  end subroutine SPOT1P64_RANK1_LOWER_VALIDATE

  subroutine SPOT1P64_RANK1_LOWER_LOAD(igroup,block,lower,du,already_dictionary_validated)
    integer, intent(in) :: igroup,block
    double precision, intent(out) :: lower(:,:)
    real, intent(in) :: du(:)
    logical, optional, intent(in) :: already_dictionary_validated
    integer :: row,nblock
    logical :: deep
    deep=.true.
    if (present(already_dictionary_validated)) then
      if (already_dictionary_validated) deep=.false.
    endif
    if (.not.allocated(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (igroup < 1 .or. igroup > size(SPOT1P64_PLAN)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (.not.allocated(SPOT1P64_PLAN(igroup)%mode)) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    if (size(SPOT1P64_PLAN(igroup)%mode) /= 1) &
      call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
    nblock=SPOT1P64_PLAN(igroup)%mode(1)%nblock
    call SPOT1P64_RANK1_LOWER_VALIDATE(igroup,size(lower,1),nblock,du,deep)
    associate(plan => SPOT1P64_PLAN(igroup)%mode(1))
      if (size(lower,2) /= plan%nstate .or. block < 1 .or. block > plan%nblock) &
        call XABORT('SPOT1P64 RANK1 LOWER: INVALID PACKED DIMENSIONS.')
      lower=0.0d0
      do row=1,size(plan%rank1_lower_rows)
        lower(plan%rank1_lower_rows(row),:)=plan%rank1_lower(row,:,plan%rank1_lower_blocks(block))
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
    if not isinstance(source, str) or _sha(source) != PARENT_KERNEL_SHA256:
        raise ValueError("actual frozen c0 packed-row kernel source required")
    kernel, edits = source, []
    kernel = _replace(kernel,
        "    integer :: rank1_lower_rows_count=0\n",
        "    integer :: rank1_lower_rows_count=0\n"
        "    integer :: rank1_lower_unique_count=0\n"
        "    integer, allocatable :: rank1_lower_blocks(:)\n", edits)
    kernel = _replace(kernel,
        "    integer(int64) :: square,amount,blocks,row_bytes\n",
        "    integer(int64) :: square,amount,blocks,row_bytes,map_bytes\n", edits)
    kernel = _replace(kernel,
        "    amount=amount+row_bytes\n",
        "    amount=amount+row_bytes\n"
        "    map_bytes=4_int64*blocks\n"
        "    if (map_bytes > RANK1_CAP-amount) &\n"
        "      call XABORT('SPOT1P64 RANK1 CACHE: 512 MIB ACCOUNTED CAP EXCEEDED.')\n"
        "    amount=amount+map_bytes\n", edits)
    start = kernel.index("  ! Only ordinary rank1 uses this storage.")
    stop = kernel.index("  subroutine SPOT1P64_RANK1_STATS(", start)
    kernel = _replace(kernel, kernel[start:stop], DEDUP_ROUTINES, edits)
    kernel = _replace(kernel,
        "                call SPOT1P64_RANK1_LOWER_LOAD(igroup,block,rank1_lower_work,du)\n",
        "                call SPOT1P64_RANK1_LOWER_LOAD(igroup,block,rank1_lower_work,du,.true.)\n", edits)
    restored = kernel
    for edit in reversed(edits):
        if restored.count(edit["new"]) != 1:
            raise ValueError("source inverse anchor is ambiguous")
        restored = restored.replace(edit["new"], edit["old"], 1)
    if restored != source:
        raise ValueError("complete c0 source inverse must be byte-exact")
    if any(len(line) > 132 for line in kernel.splitlines()):
        raise ValueError("private Fortran source exceeds 132 columns")
    return {"kernel": kernel, "proof": {
        "schema": SCHEMA, "parent_kernel_sha256": PARENT_KERNEL_SHA256,
        "parent_patch_sha256": PARENT_PATCH_SHA256,
        "dense_parent_kernel_sha256": DENSE_PARENT_KERNEL_SHA256,
        "candidate_kernel_sha256": _sha(kernel), "inverse_kernel_sha256": _sha(restored),
        "edits": edits, "complete_inverse_byteexact": True,
        "scope": "ORDINARY_RANK1_PERSISTENT_LOWER_RAW_BIT_DICTIONARY_ONLY",
        "activation": "unchanged rank1_identity_active call sites",
        "dictionary_equality": "all retained INTEGER64 IEEE bits; +0 and -0 are distinct",
        "dictionary_order": "first occurrence in original block order; no fixed unique count",
        "fallback": "all nblock blocks unique is valid and reconstructs original full shape",
        "hit_validation_sequence": "original boundary hit entry performs default complete LOWER_VALIDATE; only subsequent immutable-loop LOAD calls explicitly pass already_dictionary_validated=True",
        "direct_LOAD_default": "complete deep dictionary validation; all LOAD paths always retain shape/rowmap/blockmap/index/accounting guards",
        "persistent_accounting": "(16*nstate^2+12*nstate)*nblock+8*nrow*nstate*nunique+4*nrow+4*nblock",
        "preallocation_accounting": "parent worst-case packed values plus int32 block map; release only unallocated duplicates",
        "construction_temporary_arrays": "none; comparisons and copies use scalar original-input elements",
        "hit_temporary_accounting": "unchanged 8*nstate^2 before allocation and release after deallocation",
        "new_plan_descriptor_fields_covered_by_parent_4096_bytes": True,
        "rank1_factor_cache_budget_bytes": CAP_BYTES,
        "additional_positive_requirements": [
            "Permuted noncontiguous positive-angle rows, including positive-row -0 bits",
            "Every full decoded block versus original full lower bytes before any numeric gate",
            "Full original shape MATMUL outputs and complete flux/cour/xnei bitwise equal",
            "All 370 row maps/dictionaries/block maps/factors/keys and exact live/peak bytes",
            "Worst-case factor reservation, exact duplicate release and hit-workspace release independently counted",
            "CLEAR releases every dictionary/block-map allocation and returns all counters/live/peak to zero"],
        "factorization_and_pivots_unchanged": True, "RHS_order_unchanged": True,
        "legacy_and_uncached_formula_bytes_retained": True,
        "sender_changed": False, "other_runtime_objects_changed": False,
        "actual_controls_executed": False, "actual_full_FLU_entry_executed": False,
        "actual_native_RSS_passed": False, "AAA_accuracy_qualified": False, "ABA_admitted": False}}


def control_contract():
    return {"schema": "AXMAT_RANK1_FACTOR_CACHE_MEMORY_DEDUP_CONTROL_PLAN_V1",
        "parent_kernel_sha256": PARENT_KERNEL_SHA256,
        "dense_parent_kernel_sha256": DENSE_PARENT_KERNEL_SHA256,
        "parent_patch_sha256": PARENT_PATCH_SHA256,
        "parent_controls_sha256": PARENT_CONTROLS_SHA256,
        "inherited_bitexact_pairs": 1146, "permuted_bitexact_pairs": 6,
        "all_bitexact_pairs": 1152, "dense_reference_calls": 378,
        "inherited_operator_negative_cases": 14, "inherited_cap_negative_cases": 2,
        "all_inherited_controls_must_reexecute": True,
        "rank1_factor_cache_budget_bytes": CAP_BYTES,
        "additional_positive_requirements": [
            "All original 1152 full-field bitwise comparisons and 378 dense lower references repeat",
            "Raw canonical dictionary, block indices and full decoded lower precede every bit/finite gate",
            "Positive-row +0 and -0 stay distinct dictionary entries; omitted rows remain exact +0",
            "All-unique fallback retains every original block without a uniqueness assumption",
            "Worst-case factor reservation, duplicate release, decoded workspace release and CLEAR are checked"],
        "additional_negative_cases": [
            {"name": "row_count", "expected_message": DIMENSION_ERROR},
            {"name": "row_out_of_range", "expected_message": ROW_ERROR},
            {"name": "row_duplicate_or_reordered", "expected_message": ROW_ERROR},
            {"name": "packed_dimensions", "expected_message": DIMENSION_ERROR},
            {"name": "omitted_nonzero", "expected_message": ZERO_ERROR},
            {"name": "omitted_negative_zero", "expected_message": ZERO_ERROR}],
        "dedup_positive_command_args": ["dedup-positive"],
        "dedup_positive_fixtures": [
            {"name": "exact_repeated_blocks", "nstate": 4, "nrow": 2, "nblock": 6, "expected_unique": 3},
            {"name": "permuted_rows_repeated_blocks", "nstate": 4, "nrow": 2, "nblock": 6, "expected_unique": 3},
            {"name": "all_unique_fallback", "nstate": 4, "nrow": 2, "nblock": 49, "expected_unique": 49}],
        "dedup_negative_cases": [
            {"name": "block_index_out_of_range", "args": ["dedup-negative", "block_index_out_of_range"],
             "expected_message": BLOCK_MAP_ERROR},
            {"name": "block_map_dimensions", "args": ["dedup-negative", "block_map_dimensions"],
             "expected_message": DIMENSION_ERROR},
            {"name": "missing_unique_block", "args": ["dedup-negative", "missing_unique_block"],
             "expected_message": DIMENSION_ERROR},
            {"name": "noncanonical_first_occurrence", "args": ["dedup-negative", "noncanonical_first_occurrence"],
             "expected_message": BLOCK_MAP_ERROR},
            {"name": "duplicate_dictionary_value", "args": ["dedup-negative", "duplicate_dictionary_value"],
             "expected_message": DICTIONARY_ERROR},
            {"name": "dictionary_dimensions", "args": ["dedup-negative", "dictionary_dimensions"],
             "expected_message": DIMENSION_ERROR},
            {"name": "accounting_bytes", "args": ["dedup-negative", "accounting_bytes"],
             "expected_message": DIMENSION_ERROR},
            {"name": "release_exceeds_live", "args": ["dedup-negative", "release_exceeds_live"],
             "expected_message": "SPOT1P64 RANK1 CACHE: INVALID ACCOUNTING RELEASE."}],
        "packed_stream": {"version": 2, "header_int64_count": 12,
            "header": ["version", "nstate", "nblock", "nrow", "group", "factor_bytes",
                       "live", "peak", "cap", "built", "reused", "hits"],
            "body": ["rowmap:int32[nrow]", "blockmap:int32[nblock]", "unique_count:int32[1]",
                     "dictionary:real64[nrow,nstate,nunique]"], "order": "Fortran/little_endian"},
        "decoded_stream_is_original_full_all_blocks": True,
        "primitive_stream": {"version": 2, "header_int64_count": 12,
            "header": ["version", "nstate", "nblock", "row_count", "allocated_rows", "dictionary_dim1",
                       "dictionary_dim2", "dictionary_dim3", "factor_bytes", "live", "peak", "cap"],
            "body": ["du:real32[nstate]", "original_lower:real64[nstate,nstate,nblock]",
                     "allocated_rowmap:int32[allocated_rows]", "map_count:int32[1]", "unique_count:int32[1]",
                     "allocated_blockmap:int32[map_count]", "allocated_dictionary:real64[dim1,dim2,dim3]"],
            "original_memory_primitives_use_same_layout": True, "order": "Fortran/little_endian"},
        "negative_identity_prime_dictionary_and_full_decode_archived": True,
        "direct_LOAD_default_bad_dictionary_rejections_exercised": True,
        "additional_stage_count": 9, "total_planned_stage_count": 40,
        "raw_before_gate": True, "new_build_and_native_RSS_proof_required": True,
        "observed_RSS_reduction_is_not_a_qualification": True,
        "AAA_accuracy_qualified": False, "ABA_admitted": False}


def dense_reference_kernel(source):
    if not isinstance(source, str) or _sha(source) != DENSE_PARENT_KERNEL_SHA256:
        raise ValueError("actual frozen c017 dense reference source required")
    edits = [("SPOT1P64_CACHE_MOD", "AXMAT_DENSE_CACHE_MOD", 3),
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
        "parent_kernel_sha256": DENSE_PARENT_KERNEL_SHA256,
        "reference_kernel_sha256": _sha(result), "inverse_kernel_sha256": _sha(inverse),
        "only_module_and_entry_symbol_renames": True, "complete_inverse_byteexact": True,
        "unit_only": True, "production_link_must_exclude_this_object": True,
        "only_one_reference_group_may_be_live_at_once": True,
        "full_original_arithmetic_and_array_shapes_retained": True,
        "actual_compiled_or_executed": False}}
