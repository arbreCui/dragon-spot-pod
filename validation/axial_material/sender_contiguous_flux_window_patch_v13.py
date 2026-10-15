"""Remove the FLUSP64 output copy for contiguous active group windows.

This patch leaves the full sender, the source copy and leakage arithmetic, and
the separately compiled SPOF64/SPOT1P64 routines unchanged. A sparse active set
keeps the original F2 gather/solve/scatter path. Source evidence alone does not
qualify native memory, convergence, physical accuracy, or ABA.
"""

import hashlib


ORIGINAL_SENDER_SHA256 = "bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81"
WRAPPER_START = "      SUBROUTINE FLUSP64("


def digest_text(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def patch_sender(source):
    if digest_text(source) != ORIGINAL_SENDER_SHA256:
        raise ValueError("the exact archived complete sender is required")
    if source.count(WRAPPER_START) != 1:
        raise ValueError("the original wrapper must occur exactly once")
    edits = [
        {
            "name": "private_window_state_and_explicit_receiver_interface",
            "old": "      INTEGER IG,JJ,NGEFF,IR,IND,IBM,INM\n",
            "new": """      INTEGER IG,JJ,NGEFF,IR,IND,IBM,INM,IGFIRST,IGLAST
      LOGICAL DIRECT_OUTPUT_WINDOW
*  An explicit interface permits scalar array-element sequence association
*  to the original contiguous NUN by NGEFF receiver, without a section copy.
      INTERFACE
        SUBROUTINE SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,
     1   MAT,KEYFLX,FUNKNO,SUNKNO,TITR)
          USE GANLIB
          INTEGER NGEFF,NGIND(NGEFF),IMPX,NREG,NMAT,NUN,MAT(NREG),
     1     KEYFLX(NREG)
          TYPE(C_PTR) KPSYS(NGEFF),IPTRK
          DOUBLE PRECISION FUNKNO(NUN,NGEFF),SUNKNO(NUN,NGEFF)
          CHARACTER TITR*72
        END SUBROUTINE SPOF64
      END INTERFACE
""",
        },
        {
            "name": "ascending_active_window_detection_and_conditional_allocation",
            "old": """      NGEFF=0
      DO IG=1,NGRP
        IF(NPSYS(IG).NE.0) NGEFF=NGEFF+1
      ENDDO
      IF(NGEFF.EQ.0) RETURN
      ALLOCATE(KPSYS(NGEFF),NGIND(NGEFF),F2(NUN,NGEFF),S2(NUN,NGEFF))
""",
            "new": """      NGEFF=0
      IGFIRST=0
      IGLAST=0
      DO IG=1,NGRP
        IF(NPSYS(IG).NE.0) THEN
          NGEFF=NGEFF+1
          IF(IGFIRST.EQ.0) IGFIRST=IG
          IGLAST=IG
        ENDIF
      ENDDO
      IF(NGEFF.EQ.0) RETURN
      DIRECT_OUTPUT_WINDOW=(IGLAST-IGFIRST+1.EQ.NGEFF)
      ALLOCATE(KPSYS(NGEFF),NGIND(NGEFF),S2(NUN,NGEFF))
      IF(.NOT.DIRECT_OUTPUT_WINDOW) ALLOCATE(F2(NUN,NGEFF))
""",
        },
        {
            "name": "retain_copy_in_only_for_sparse_fallback",
            "old": "          F2(:NUN,JJ)=FUN(:NUN,IG)\n",
            "new": """          IF(.NOT.DIRECT_OUTPUT_WINDOW) THEN
            F2(:NUN,JJ)=FUN(:NUN,IG)
          ENDIF
""",
        },
        {
            "name": "direct_output_window_or_original_sparse_solve_and_scatter",
            "old": """      CALL SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,
     1 KEYFLX,F2,S2,TITR)
      DO JJ=1,NGEFF
        FUN(:NUN,NGIND(JJ))=F2(:NUN,JJ)
      ENDDO
""",
            "new": """      IF(DIRECT_OUTPUT_WINDOW) THEN
        CALL SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,
     1   KEYFLX,FUN(1,NGIND(1)),S2,TITR)
      ELSE
        CALL SPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,
     1   KEYFLX,F2,S2,TITR)
        DO JJ=1,NGEFF
          FUN(:NUN,NGIND(JJ))=F2(:NUN,JJ)
        ENDDO
      ENDIF
""",
        },
        {
            "name": "release_only_the_allocated_output_fallback",
            "old": "      DEALLOCATE(S2,F2,NGIND,KPSYS)\n",
            "new": """      IF(ALLOCATED(F2)) DEALLOCATE(F2)
      DEALLOCATE(S2,NGIND,KPSYS)
""",
        },
    ]
    candidate = source
    for edit in edits:
        if candidate.count(edit["old"]) != 1:
            raise ValueError("nonunique original patch region: " + edit["name"])
        candidate = candidate.replace(edit["old"], edit["new"], 1)
    inverse = candidate
    for edit in reversed(edits):
        if inverse.count(edit["new"]) != 1:
            raise ValueError("nonunique inverse patch region: " + edit["name"])
        inverse = inverse.replace(edit["new"], edit["old"], 1)
    if inverse != source:
        raise ValueError("complete sender inverse must be byte exact")
    original_prefix, original_wrapper = source.split(WRAPPER_START)
    candidate_prefix, candidate_wrapper = candidate.split(WRAPPER_START)
    if candidate_prefix != original_prefix:
        raise ValueError("all sender code outside FLUSP64 must be byte exact")
    original_wrapper = WRAPPER_START + original_wrapper
    candidate_wrapper = WRAPPER_START + candidate_wrapper
    reference_wrapper = original_wrapper.replace(
        WRAPPER_START, "      SUBROUTINE FLUSP64_REFERENCE(", 1
    )
    proof = {
        "schema": "AXMAT_FLUSP64_CONTIGUOUS_OUTPUT_WINDOW_SOURCE_PATCH_V13",
        "scope": "CONTIGUOUS_ACTIVE_OUTPUT_COPY_STORAGE_ONLY_WITH_ORIGINAL_SPARSE_FALLBACK",
        "original_sender_sha256": digest_text(source),
        "candidate_sender_sha256": digest_text(candidate),
        "original_wrapper_sha256": digest_text(original_wrapper),
        "candidate_wrapper_sha256": digest_text(candidate_wrapper),
        "reference_wrapper_sha256": digest_text(reference_wrapper),
        "edits": edits,
        "complete_inverse_byteexact": True,
        "sender_outside_wrapper_byteexact": True,
        "receiver_interface": "ORIGINAL_EXPLICIT_SHAPE_SPOF64_WITHOUT_PUBLIC_ABI_CHANGE",
        "direct_window_condition": "ascending active last-first+1 == NGEFF, NGEFF > 0",
        "source_copy_and_leakage_arithmetic_retained": True,
        "sparse_gather_scatter_retained": True,
        "empty_active_set_returns_before_allocation": True,
        "no_pointer_or_target_or_assumed_shape_added": True,
        "partial_output_on_failed_direct_call_must_not_be_reused": True,
        "successful_receiver_does_not_read_incoming_output_required": True,
        "caller_old_source_output_nonalias_required": True,
        "conditional_payload_saving_bytes": {"formula": "8 * NUN * NGEFF", "NUN": 1800, "NGEFF": 370, "bytes": 5328000},
        "observed_native_RSS_saving": None,
        "native_RSS_verified": False,
        "AAA_accuracy_qualified": False,
        "ABA_admitted": False,
    }
    return {
        "sender": candidate,
        "candidate_wrapper": candidate_wrapper,
        "reference_wrapper": reference_wrapper,
        "proof": proof,
    }
