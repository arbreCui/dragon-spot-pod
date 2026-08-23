#---------------------------------------------------------------------------
#
#  Makefile for executing the Dragon non-regression tests
#  Author : A. Hebert (2018-5-10)
#
#---------------------------------------------------------------------------
#
OS = $(shell uname -s | cut -d"_" -f1)
ifneq (,$(filter $(OS),SunOS AIX))
  MAKE = gmake
endif
ifeq ($(openmp),1)
  nomp = 16
else
  nomp = 0
endif
ifeq ($(intel),1)
  fcompilerSuite = intel
else
  ifeq ($(nvidia),1)
    fcompilerSuite = nvidia
  else
    ifeq ($(llvm),1)
      fcompilerSuite = llvm
    else
      fcompilerSuite = custom
    endif
  endif
endif
all :
	$(MAKE) -C src
.PHONY: spot-fast spot-rank-census spot-rank2-basis spot-rank2-map \
	spot-rank2-axial-only spot-rank2-next-map \
	spot-rank2-modal-aa1-candidate spot-rank2-modal-aa1-map \
	spot-rank2-modal-aa1-next-candidate spot-rank2-modal-aa1-next-map \
	spot-rank2-modal-aa1-u-candidate spot-rank2-modal-aa1-u-map \
	spot-rank2-modal-aa1-consecutive-candidate \
	spot-rank2-modal-aa1-consecutive-map \
	spot-rank2-modal-aa1-post-candidate \
	spot-rank2-modal-aa1-post-map \
	spot-rank2-modal-aa1-rolling-candidate \
	spot-rank2-modal-aa1-rolling-map \
	spot-rank2-modal-aa1-rolling-next-candidate \
	spot-rank2-modal-aa1-rolling-next-map \
	spot-rank2-modal-aa2-candidate \
	spot-rank2-current-aa2-candidate \
	spot-rank2-current-aa2-map \
	spot-rank2-current-aa2-picard-map \
	spot-rank2-current-aa2-picard-aa1-candidate \
	spot-rank2-current-aa2-picard-aa1-map \
	spot-rank2-current-qpzst-aa2-candidate \
	spot-rank2-current-stuvvw-aa2-candidate \
	spot-rank2-current-stuvvw-aa2-map \
	spot-rank2-current-uvvwxy-aa2-candidate \
	spot-rank2-current-uvvwxy-aa2-map \
	spot-rank2-current-z-picard-map \
	spot-rank2-current-zplus-picard-map \
	spot-rank2-current-zrs-aa1-candidate \
	spot-rank2-current-zrs-aa1-map \
	spot-rank2-current-t-picard-map \
	spot-rank2-current-ptu-aa1-candidate \
	spot-rank2-current-ptu-aa1-map \
	spot-rank2-current-ptuqv-aa2-candidate \
	spot-rank2-current-ptuqv-aa2-map \
	spot-rank2-current-qvwx-aa1-candidate \
	spot-rank2-current-qvwx-aa1-map \
	spot-rank2-current-qvwx-z-picard-map \
	spot-rank2-current-qvwx-zplus-aa1-candidate \
	spot-rank2-current-qvwx-zplus-aa1-map \
	spot-rank2-current-zpcd-aa1-candidate \
	spot-rank2-current-zpcd-aa1-map \
	spot-rank2-current-zpcd-e-picard-map \
	spot-rank2-current-cef-aa1-candidate \
	spot-rank2-current-cef-aa1-map \
	spot-rank2-current-cefg-aa2-candidate \
	spot-rank2-current-cefg-aa2-map \
	spot-rank2-current-gh-aa1-candidate \
	spot-rank2-current-gh-aa1-map \
	spot-rank2-current-ghi-aa2-candidate \
	spot-rank2-current-ghi-aa2-map \
	spot-rank2-current-ij-aa1-candidate \
	spot-rank2-current-ij-aa1-map \
	spot-rank2-current-k-picard-map \
	spot-rank2-current-kl-aa1-candidate \
	spot-rank2-current-kl-aa1-map \
	spot-rank2-current-klm-aa1-candidate \
	spot-rank2-current-klm-aa1-map \
	spot-rank2-current-klmn-aa2-candidate \
	spot-rank2-current-klmn-aa2-map \
	spot-rank2-current-no-aa1-candidate \
	spot-rank2-current-no-aa1-map \
	spot-rank2-current-op-aa1-candidate \
	spot-rank2-current-op-aa1-map \
	spot-rank2-current-pr-aa1-candidate \
	spot-rank2-current-pr-aa1-map \
	spot-rank2-current-rs-aa1-candidate \
	spot-rank2-current-rs-aa1-map \
	spot-rank2-current-qpzst-aa2-map \
	spot-rank2-current-v-picard-map \
	spot-rank2-modal-aa2-rolling-next-candidate \
	spot-rank2-modal-aa2-rolling-next-map \
	spot-rank2-modal-aa2-rolling-next-picard-map \
	spot-rank2-latest-picard-next-map \
	spot-rank2-latest-modal-aa1-candidate \
	spot-rank2-latest-modal-aa1-next-candidate \
	spot-rank2-latest-modal-aa1-recovery-candidate \
	spot-rank2-latest-modal-aa1-qv-candidate \
	spot-rank2-latest-modal-aa1-map \
	spot-rank2-latest-modal-aa1-next-map \
	spot-rank2-latest-modal-aa1-next-map-recovery \
	spot-rank2-latest-modal-aa1-recovery-map \
	spot-rank2-qv-picard-map \
	spot-rank2-qsvw-aa1-candidate \
	spot-rank2-qsvw-aa1-map \
	spot-rank2-vwx-picard-map \
	spot-rank2-vwx-aa1-candidate \
	spot-rank2-vwx-aa1-map \
	spot-rank2-wxcd-aa1-candidate \
	spot-rank2-wxcd-aa1-map \
	spot-rank2-modal-aa2-map
spot-fast :
	sh validation/run_fast.sh
.PHONY: spot-b2c-dimensions
spot-b2c-dimensions :
	sh validation/iterative/run_b2c_runtime_dimensions.sh
spot-rank-census :
	sh validation/iterative/run_rank_census.sh
spot-rank2-basis :
	sh validation/iterative/run_rank2_basis.sh
spot-rank2-map :
	sh validation/iterative/run_rank2_map.sh
spot-rank2-axial-only :
	sh validation/iterative/run_rank2_axial_only.sh
spot-rank2-next-map :
	sh validation/iterative/run_rank2_next_map.sh
spot-rank2-modal-aa1-candidate :
	sh validation/iterative/run_rank2_modal_aa1_candidate.sh
spot-rank2-modal-aa1-map :
	sh validation/iterative/run_rank2_modal_aa1_map.sh
spot-rank2-modal-aa1-next-candidate :
	sh validation/iterative/run_rank2_modal_aa1_next_candidate.sh
spot-rank2-modal-aa1-next-map :
	sh validation/iterative/run_rank2_modal_aa1_next_map.sh
spot-rank2-modal-aa1-u-candidate :
	sh validation/iterative/run_rank2_modal_aa1_u_candidate.sh
spot-rank2-modal-aa1-u-map :
	sh validation/iterative/run_rank2_modal_aa1_u_map.sh
spot-rank2-modal-aa1-consecutive-candidate :
	sh validation/iterative/run_rank2_modal_aa1_consecutive_candidate.sh
spot-rank2-modal-aa1-consecutive-map :
	sh validation/iterative/run_rank2_modal_aa1_consecutive_map.sh
spot-rank2-modal-aa1-post-candidate :
	sh validation/iterative/run_rank2_modal_aa1_post_candidate.sh
spot-rank2-modal-aa1-post-map :
	sh validation/iterative/run_rank2_modal_aa1_post_map.sh
spot-rank2-modal-aa1-rolling-candidate :
	sh validation/iterative/run_rank2_modal_aa1_rolling_candidate.sh
spot-rank2-modal-aa1-rolling-map :
	sh validation/iterative/run_rank2_modal_aa1_rolling_map.sh
spot-rank2-modal-aa1-rolling-next-candidate :
	sh validation/iterative/run_rank2_modal_aa1_rolling_next_candidate.sh
spot-rank2-modal-aa1-rolling-next-map :
	sh validation/iterative/run_rank2_modal_aa1_rolling_next_map.sh
spot-rank2-modal-aa2-candidate :
	sh validation/iterative/run_rank2_modal_aa2_candidate.sh
spot-rank2-current-aa2-candidate :
	sh validation/iterative/run_rank2_current_aa2_candidate.sh
spot-rank2-current-aa2-map :
	sh validation/iterative/run_rank2_current_aa2_map.sh
spot-rank2-current-aa2-picard-map :
	sh validation/iterative/run_rank2_current_aa2_picard_map.sh
spot-rank2-current-aa2-picard-aa1-candidate :
	sh validation/iterative/run_rank2_current_aa2_picard_aa1_candidate.sh
spot-rank2-current-aa2-picard-aa1-map :
	sh validation/iterative/run_rank2_current_aa2_picard_aa1_map.sh
spot-rank2-current-qpzst-aa2-candidate :
	sh validation/iterative/run_rank2_current_qpzst_aa2_candidate.sh
spot-rank2-current-stuvvw-aa2-candidate :
	sh validation/iterative/run_rank2_current_stuvvw_aa2_candidate.sh
spot-rank2-current-stuvvw-aa2-map :
	sh validation/iterative/run_rank2_current_stuvvw_aa2_map.sh
spot-rank2-current-uvvwxy-aa2-candidate :
	sh validation/iterative/run_rank2_current_uvvwxy_aa2_candidate.sh
spot-rank2-current-uvvwxy-aa2-map :
	sh validation/iterative/run_rank2_current_uvvwxy_aa2_map.sh
spot-rank2-current-z-picard-map :
	sh validation/iterative/run_rank2_current_z_picard_map.sh
spot-rank2-current-zplus-picard-map :
	sh validation/iterative/run_rank2_current_zplus_picard_map.sh
spot-rank2-current-zrs-aa1-candidate :
	sh validation/iterative/run_rank2_current_zrs_aa1_candidate.sh
spot-rank2-current-zrs-aa1-map :
	sh validation/iterative/run_rank2_current_zrs_aa1_map.sh
spot-rank2-current-t-picard-map :
	sh validation/iterative/run_rank2_current_t_picard_map.sh
spot-rank2-current-ptu-aa1-candidate :
	sh validation/iterative/run_rank2_current_ptu_aa1_candidate.sh
spot-rank2-current-ptu-aa1-map :
	sh validation/iterative/run_rank2_current_ptu_aa1_map.sh
spot-rank2-current-ptuqv-aa2-candidate :
	sh validation/iterative/run_rank2_current_ptuqv_aa2_candidate.sh
spot-rank2-current-ptuqv-aa2-map :
	sh validation/iterative/run_rank2_current_ptuqv_aa2_map.sh
spot-rank2-current-qvwx-aa1-candidate :
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-qvwx-aa1-map :
	sh validation/iterative/run_rank2_current_qvwx_aa1_map.sh
spot-rank2-current-qvwx-z-picard-map :
	sh validation/iterative/run_rank2_current_qvwx_z_picard_map.sh
spot-rank2-current-qvwx-zplus-aa1-candidate :
	sh validation/iterative/run_rank2_current_qvwx_zplus_aa1_candidate.sh
spot-rank2-current-qvwx-zplus-aa1-map :
	sh validation/iterative/run_rank2_current_qvwx_zplus_aa1_map.sh
spot-rank2-current-zpcd-aa1-candidate :
	sh validation/iterative/run_rank2_current_zpcd_aa1_candidate.sh
spot-rank2-current-zpcd-aa1-map :
	sh validation/iterative/run_rank2_current_zpcd_aa1_map.sh
spot-rank2-current-zpcd-e-picard-map :
	sh validation/iterative/run_rank2_current_zpcd_e_picard_map.sh
spot-rank2-current-cef-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_cef_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-cef-aa1-candidate" \
	EXPECTED_AX_SHA=76f38e5076c6e060866401d81dac5f177babebac0e220af73aa77a90a3f486bd \
	EXPECTED_SNAP_SHA=5b7d6d7c0cf00a4097284b53816d7e3c91ca4e27656f0bc437f6a0472555ac68 \
	sh validation/iterative/run_rank2_current_qvwx_zplus_aa1_candidate.sh
spot-rank2-current-cef-aa1-map :
	sh validation/iterative/run_rank2_current_cef_aa1_map.sh
spot-rank2-current-cefg-aa2-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_cefg_aa2_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-cefg-aa2-candidate" \
	CANDIDATE_MODE=--current-cefg-aa2 \
	REPORT_PREFIX=RANK2-CURRENT-CEFG-AA2 \
	MANIFEST_HEADER='# spot-rank2-current-cefg-aa2-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=d4b25fc5bf9b3cc2eb4c6665833f7560073408ffd5462c0f07e4cf30ead0d1fe \
	EXPECTED_SNAP_SHA_OVERRIDE=b0aac9dd5575fc48ca351e0b330946afc968777152a6356f9846b5c9ac1b1c79 \
	sh validation/iterative/run_rank2_current_ptuqv_aa2_candidate.sh
spot-rank2-current-cefg-aa2-map :
	sh validation/iterative/run_rank2_current_cefg_aa2_map.sh
spot-rank2-current-gh-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_gh_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-gh-aa1-candidate" \
	CANDIDATE_MODE=--next-aa1aa2-screened \
	REPORT_PREFIX=RANK2-CURRENT-GH-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-gh-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=c40c7011626864da111ab6a8097dcb3d0d3a87b2683a72986660f7f0574569c6 \
	EXPECTED_SNAP_SHA_OVERRIDE=3cd88d1d7f65ad05cc7a62025cb12a2d50bc016a52d35b251685da71c559b37f \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-gh-aa1-map :
	sh validation/iterative/run_rank2_current_gh_aa1_map.sh
spot-rank2-current-ghi-aa2-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_ghi_aa2_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-ghi-aa2-candidate" \
	CANDIDATE_MODE=--current-ghi-aa2 \
	REPORT_PREFIX=RANK2-CURRENT-GHI-AA2 \
	MANIFEST_HEADER='# spot-rank2-current-ghi-aa2-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=5202ebe842a373800fe65c0748890a6a21fdc43e497bb24f152d536fb53ae391 \
	EXPECTED_SNAP_SHA_OVERRIDE=d841554d9bb0b9e158dfda323ead4016c98c450387bb656416218f3b6d1d5548 \
	sh validation/iterative/run_rank2_current_aa2_candidate.sh
spot-rank2-current-ghi-aa2-map :
	sh validation/iterative/run_rank2_current_ghi_aa2_map.sh
spot-rank2-current-ij-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_ij_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-ij-aa1-candidate" \
	CANDIDATE_MODE=--next-aa1aa2-ij-screened \
	REPORT_PREFIX=RANK2-CURRENT-IJ-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-ij-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=27250a1b370d2cdbf83f35fbf1a380919261bb938890b2f3d04d7390afb72743 \
	EXPECTED_SNAP_SHA_OVERRIDE=f7e351eab9c895c4b43023e37734f4675898fa39b70e07ca9c25c29eecd66f7c \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-ij-aa1-map :
	sh validation/iterative/run_rank2_current_ij_aa1_map.sh
spot-rank2-current-k-picard-map :
	sh validation/iterative/run_rank2_current_k_picard_map.sh
spot-rank2-current-kl-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_kl_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-kl-aa1-candidate" \
	MODE=--consecutive-q5kl-screened \
	REPORT_PREFIX=RANK2-CURRENT-KL-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-kl-aa1-candidate-inputs-v1' \
	PROPOSAL_ROLE=q5_aa1_pub PREVIOUS_ROLE=k LATEST_ROLE=l \
	LATEST_SNAPSHOTS_ROLE=l_snapshots BASIS_ROLE=basis_reference \
	EXPECTED_AX_SHA=d223068dbabd5424762f6f73fb488a927cca94ca4db3cee7ef3bbf7f090d825d \
	EXPECTED_SNAP_SHA=c6c9546bb7807864aa2b0eaa56e289ee91ffa1ec4328b7889a5deb81d9b2cec6 \
	sh validation/iterative/run_rank2_current_qvwx_zplus_aa1_candidate.sh
spot-rank2-current-kl-aa1-map :
	sh validation/iterative/run_rank2_current_kl_aa1_map.sh
spot-rank2-current-klm-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_klm_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-klm-aa1-candidate" \
	MANIFEST_HEADER='# spot-rank2-current-klm-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA=74cbee2ffcb72db1a86e728f8643cfbe9dfb6f2784965fe440bd20567a50ee89 \
	EXPECTED_SNAP_SHA=78a999ff7b2fab8f7fbfd4b29e0d433b9ae9e9ef5b124ff812c776b7422f437c \
	sh validation/iterative/run_rank2_current_zpcd_aa1_candidate.sh
spot-rank2-current-klm-aa1-map :
	sh validation/iterative/run_rank2_current_klm_aa1_map.sh
spot-rank2-current-klmn-aa2-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_klmn_aa2_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-klmn-aa2-candidate" \
	CANDIDATE_MODE=--current-klmn-aa2 \
	REPORT_PREFIX=RANK2-CURRENT-KLMN-AA2 \
	MANIFEST_HEADER='# spot-rank2-current-klmn-aa2-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=6dee27775279ddf1b75113ceafa62bf60acad27965b13f2122c146976ae892c8 \
	EXPECTED_SNAP_SHA_OVERRIDE=d925a87d087cf971b1d2a8f18dae9603caed3b3233b738ada97bae82a0b6998e \
	sh validation/iterative/run_rank2_current_aa2_candidate.sh
spot-rank2-current-klmn-aa2-map :
	sh validation/iterative/run_rank2_current_klmn_aa2_map.sh
spot-rank2-current-no-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_no_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-no-aa1-candidate" \
	CANDIDATE_MODE=--next-aa1aa2-no-screened \
	REPORT_PREFIX=RANK2-CURRENT-NO-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-no-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=c5d3275ead6dc8b5afb6d7ec125965678a0659ed8cf027d547edd6a009738b4e \
	EXPECTED_SNAP_SHA_OVERRIDE=f7476c9f42d5de128e56c01044609e233a11ec147019942d429b8db419ba30ab \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-no-aa1-map :
	sh validation/iterative/run_rank2_current_no_aa1_map.sh
spot-rank2-current-op-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_op_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-op-aa1-candidate" \
	CANDIDATE_MODE=--next-aa2aa1-op-screened \
	REPORT_PREFIX=RANK2-CURRENT-OP-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-op-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=bd0785e9f3da27b9639c3ac4c04d3bf25689c5dc7f16fc51cdcdde7306b154fb \
	EXPECTED_SNAP_SHA_OVERRIDE=4587fcc293ba18c40c0c785e6de4991d969cc10cca8975b4b4fddf114725c209 \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-op-aa1-map :
	sh validation/iterative/run_rank2_current_op_aa1_map.sh
spot-rank2-current-pr-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_pr_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-pr-aa1-candidate" \
	CANDIDATE_MODE=--next-aa1aa1-screened \
	REPORT_PREFIX=RANK2-CURRENT-MN-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-pr-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=20b4a9fb31f6baa4f62d9fa5b22cf0801709ceb37579bf9f16dfc7e6c450f05d \
	EXPECTED_SNAP_SHA_OVERRIDE=d974a4883eaa5460614d25cdf81284644760218308c88f35ed41bd54065d0167 \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-pr-aa1-map :
	sh validation/iterative/run_rank2_current_pr_aa1_map.sh
spot-rank2-current-rs-aa1-candidate :
	MANIFEST="$(CURDIR)/validation/iterative/rank2_current_rs_aa1_candidate_inputs.tsv" \
	ARTIFACT_DIR="$(CURDIR)/validation/artifacts/iterative-rank2-current-rs-aa1-candidate" \
	CANDIDATE_MODE=--next-aa1aa1-screened \
	REPORT_PREFIX=RANK2-CURRENT-MN-AA1 \
	MANIFEST_HEADER='# spot-rank2-current-rs-aa1-candidate-inputs-v1' \
	EXPECTED_AX_SHA_OVERRIDE=11c73abd4e35419da447429b6de73191b05d31cff132db0e762d45316f5b4e26 \
	EXPECTED_SNAP_SHA_OVERRIDE=779e419a8b2a378b837976dd726757c2bf13d406184126182eca64b00c065f6f \
	sh validation/iterative/run_rank2_current_qvwx_aa1_candidate.sh
spot-rank2-current-rs-aa1-map :
	sh validation/iterative/run_rank2_current_rs_aa1_map.sh
spot-rank2-current-qpzst-aa2-map :
	sh validation/iterative/run_rank2_current_qpzst_aa2_map.sh
spot-rank2-current-v-picard-map :
	sh validation/iterative/run_rank2_current_v_picard_map.sh
spot-rank2-modal-aa2-rolling-next-candidate :
	sh validation/iterative/run_rank2_modal_aa2_rolling_next_candidate.sh
spot-rank2-modal-aa2-rolling-next-map :
	sh validation/iterative/run_rank2_modal_aa2_rolling_next_map.sh
spot-rank2-modal-aa2-rolling-next-picard-map :
	sh validation/iterative/run_rank2_modal_aa2_rolling_next_picard_map.sh
spot-rank2-latest-picard-next-map :
	sh validation/iterative/run_rank2_latest_picard_next_map.sh
spot-rank2-latest-modal-aa1-candidate :
	sh validation/iterative/run_rank2_latest_modal_aa1_candidate.sh
spot-rank2-latest-modal-aa1-next-candidate :
	sh validation/iterative/run_rank2_latest_modal_aa1_next_candidate.sh
spot-rank2-latest-modal-aa1-recovery-candidate :
	sh validation/iterative/run_rank2_latest_modal_aa1_recovery_candidate.sh
spot-rank2-latest-modal-aa1-qv-candidate :
	sh validation/iterative/run_rank2_latest_modal_aa1_qv_candidate.sh
spot-rank2-latest-modal-aa1-map :
	sh validation/iterative/run_rank2_latest_modal_aa1_map.sh
spot-rank2-latest-modal-aa1-next-map :
	sh validation/iterative/run_rank2_latest_modal_aa1_next_map.sh
spot-rank2-latest-modal-aa1-next-map-recovery :
	sh validation/iterative/run_rank2_latest_modal_aa1_next_map_recovery.sh
spot-rank2-latest-modal-aa1-recovery-map :
	sh validation/iterative/run_rank2_latest_modal_aa1_recovery_map.sh
spot-rank2-qv-picard-map :
	sh validation/iterative/run_rank2_qv_picard_map.sh
spot-rank2-qsvw-aa1-candidate :
	sh validation/iterative/run_rank2_qsvw_aa1_candidate.sh
spot-rank2-qsvw-aa1-map :
	sh validation/iterative/run_rank2_qsvw_aa1_map.sh
spot-rank2-vwx-picard-map :
	sh validation/iterative/run_rank2_vwx_picard_map.sh
spot-rank2-vwx-aa1-candidate :
	sh validation/iterative/run_rank2_vwx_aa1_candidate.sh
spot-rank2-vwx-aa1-map :
	sh validation/iterative/run_rank2_vwx_aa1_map.sh
spot-rank2-wxcd-aa1-candidate :
	sh validation/iterative/run_rank2_wxcd_aa1_candidate.sh
spot-rank2-wxcd-aa1-map :
	sh validation/iterative/run_rank2_wxcd_aa1_map.sh
spot-rank2-modal-aa2-map :
	sh validation/iterative/run_rank2_modal_aa2_map.sh
clean :
	$(MAKE) clean -C src
tests :
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q iaea2d.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q g2s_prestation.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q salmacro.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tmacro.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q VanDerGucht.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q VanDerGucht-295.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q uo2_295_kec1_openMP.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tdraglib.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q twimsE.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q twlup.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tndas.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tmatxs2.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q trowland_shem295_jeff3.1.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q uo2_kec1_ecco1962_light.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q lumpSS.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q ASSBLY_CASEA_1level_multicompo.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q OSC_CASEA_1level_rse.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q OSC_CASEA_2level_rse.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q OSC_openMP_tiso.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q sens.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q testVVER7.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q fbr_colorset.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q fbr_tone.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q TEST_GEO_hex_sect_tspc.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q TEST_GEO_latt_tspc_S30.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q testDuo.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q testDuo_B1.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q C2D20.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q CFC-CELL.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q ErmBeavrsPwrRefl.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q DF_RTBeavrsPwrRefl.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q rep900_het_gff_jef2p2.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q RegtestCNG_mccg.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q RegtestLZC_mccg.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q pincell_mco.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q pincell_sap.x2m
ifeq ($(apolib),1)
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tapollo1.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q tapollo2.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q uo2_evo_xsm.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q uo2_evo_hdf.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q ASSBLY_CASEA_1level_apex_boron.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q ASSBLY_CASEA_1level_mpo.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q ASSBLY_VVER_1level_mpo.x2m
endif
ifeq ($(hdf5),1)
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q UOX_5x5_TG6_sym8_multiDom.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q pincell_apx.x2m
	./rdragon -c $(fcompilerSuite) -p $(nomp) -q pincell_mpo.x2m
endif
