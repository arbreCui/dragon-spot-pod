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
spot-fast :
	sh validation/run_fast.sh
.PHONY: spot-real64-phase-a1
spot-real64-phase-a1 :
	sh validation/iterative/real64_phase_a1/run_phase_a1.sh
.PHONY: spot-real64-phase-a2
spot-real64-phase-a2 :
	sh validation/iterative/real64_phase_a2/run_phase_a2.sh
.PHONY: spot-real64-phase-a3
spot-real64-phase-a3 :
	sh validation/iterative/real64_phase_a3/run_phase_a3.sh
.PHONY: spot-real64-phase-a4
spot-real64-phase-a4 :
	sh validation/iterative/real64_phase_a4/run_phase_a4.sh
.PHONY: spot-real64-phase-a5
spot-real64-phase-a5 :
	sh validation/iterative/real64_phase_a5/run_phase_a5.sh
.PHONY: spot-real64-phase-a6
spot-real64-phase-a6 :
	sh validation/iterative/real64_phase_a6/run_phase_a6.sh
.PHONY: spot-real64-phase-a7
spot-real64-phase-a7 :
	sh validation/iterative/real64_phase_a7/run_phase_a7.sh
.PHONY: spot-real64-phase-a8
spot-real64-phase-a8 :
	sh validation/iterative/real64_phase_a8/run_phase_a8.sh
.PHONY: spot-real64-phase-a9a
spot-real64-phase-a9a :
	sh validation/iterative/real64_phase_a9/run_phase_a9a.sh
.PHONY: spot-real64-phase-a9b-promotion
spot-real64-phase-a9b-promotion :
	sh validation/iterative/real64_phase_a9b_promotion/run_phase_a9b_promotion.sh
.PHONY: spot-real64-phase-a9b-spomoc-abi
spot-real64-phase-a9b-spomoc-abi :
	sh validation/iterative/real64_phase_a9b_spomoc_abi/run_phase_a9b_spomoc_abi.sh
.PHONY: spot-real64-phase-a9b-b2a-selector
spot-real64-phase-a9b-b2a-selector :
	sh validation/iterative/real64_phase_a9b_b2a_selector/run_phase_a9b_b2a_selector.sh
.PHONY: spot-real64-phase-a9b-b2b-ingress
spot-real64-phase-a9b-b2b-ingress :
	sh validation/iterative/real64_phase_a9b_b2b_ingress/run_phase_a9b_b2b_ingress.sh
.PHONY: spot-real64-phase-a9b-b2c-publication
spot-real64-phase-a9b-b2c-publication :
	sh validation/iterative/real64_phase_a9b_b2c_publication/run_phase_a9b_b2c_publication.sh
.PHONY: spot-real64-phase-a9b-b2h-projection
spot-real64-phase-a9b-b2h-projection :
	sh validation/iterative/real64_phase_a9b_b2h_projection_authority/run_phase_a9b_b2h_projection_authority.sh
.PHONY: spot-real64-phase-a9b-b2i-bootstrap
spot-real64-phase-a9b-b2i-bootstrap :
	sh validation/iterative/real64_phase_a9b_b2i_bootstrap_lifecycle/run_phase_a9b_b2i_bootstrap_lifecycle.sh
.PHONY: spot-real64-phase-a9b-b2j-projection
spot-real64-phase-a9b-b2j-projection :
	sh validation/iterative/real64_phase_a9b_b2j_archive_projection/run_phase_a9b_b2j_archive_projection.sh
.PHONY: spot-real64-phase-a9b-b2k-system-assembly
spot-real64-phase-a9b-b2k-system-assembly :
	sh validation/iterative/real64_phase_a9b_b2k_system_assembly/run_phase_a9b_b2k_system_assembly.sh
.PHONY: spot-real64-phase-a9b-b2l-one-plane-real-asm
spot-real64-phase-a9b-b2l-one-plane-real-asm :
	sh validation/iterative/real64_phase_a9b_b2l_one_plane_real_asm/run_phase_a9b_b2l_one_plane_real_asm.sh
.PHONY: spot-real64-phase-a9b-b2m-three-plane-real-asm-commit
spot-real64-phase-a9b-b2m-three-plane-real-asm-commit :
	sh validation/iterative/real64_phase_a9b_b2m_three_plane_real_asm_commit/run_phase_a9b_b2m_three_plane_real_asm_commit.sh
.PHONY: spot-real64-phase-a9b-b2n-real64-frozen-qfiss
spot-real64-phase-a9b-b2n-real64-frozen-qfiss :
	sh validation/iterative/real64_phase_a9b_b2n_real64_frozen_qfiss/run_phase_a9b_b2n_real64_frozen_qfiss.sh
.PHONY: spot-real64-phase-a9b-b2o-cont-binding-cutoff
spot-real64-phase-a9b-b2o-cont-binding-cutoff :
	sh validation/iterative/real64_phase_a9b_b2o_cont_binding_cutoff/run_phase_a9b_b2o_cont_binding_cutoff.sh
.PHONY: spot-real64-phase-a9b-b2p-solved-lifecycle
spot-real64-phase-a9b-b2p-solved-lifecycle :
	sh validation/iterative/real64_phase_a9b_b2p_solved_lifecycle/run_phase_a9b_b2p_solved_lifecycle.sh
.PHONY: spot-real64-phase-a9b-b2q-lifecycle-rho-contract
spot-real64-phase-a9b-b2q-lifecycle-rho-contract :
	sh validation/iterative/real64_phase_a9b_b2q_lifecycle_rho_contract/run_phase_a9b_b2q_lifecycle_rho_contract.sh
.PHONY: spot-real64-phase-a9b-b2r-returned-archive
spot-real64-phase-a9b-b2r-returned-archive :
	sh validation/iterative/real64_phase_a9b_b2r_returned_archive/run_phase_a9b_b2r_returned_archive.sh
.PHONY: spot-real64-phase-a9b-b2s-immediate-host-bridge
spot-real64-phase-a9b-b2s-immediate-host-bridge :
	sh validation/iterative/real64_phase_a9b_b2s_immediate_host_bridge/run_phase_a9b_b2s_immediate_host_bridge.sh
.PHONY: spot-real64-phase-a9b-b2t-owned-source-host-step
spot-real64-phase-a9b-b2t-owned-source-host-step :
	sh validation/iterative/real64_phase_a9b_b2t_owned_source_host_step/run_phase_a9b_b2t_owned_source_host_step.sh
.PHONY: spot-real64-phase-a9b-b2u-same-call-asm-host
spot-real64-phase-a9b-b2u-same-call-asm-host :
	sh validation/iterative/real64_phase_a9b_b2u_same_call_asm_host/run_phase_a9b_b2u_same_call_asm_host.sh
.PHONY: spot-real64-phase-a9b-b2v-one-real-continuation
spot-real64-phase-a9b-b2v-one-real-continuation :
	sh validation/iterative/real64_phase_a9b_b2v_one_real_continuation/run_phase_a9b_b2v_one_real_continuation.sh
.PHONY: spot-real64-phase-a9b-b2w-returned-close
spot-real64-phase-a9b-b2w-returned-close :
	sh validation/iterative/real64_phase_a9b_b2w_returned_close/run_phase_a9b_b2w_returned_close.sh
.PHONY: spot-real64-phase-a9b-b2x-same-call-returned-close
spot-real64-phase-a9b-b2x-same-call-returned-close :
	sh validation/iterative/real64_phase_a9b_b2x_same_call_returned_close/run_phase_a9b_b2x_same_call_returned_close.sh
spot-stage0 :
	@test -n "$(DRAGON_BIN)" || \
	  (echo "set DRAGON_BIN to a current SPOT executable" >&2; exit 2)
	DRAGON_BIN="$(DRAGON_BIN)" sh validation/iterative/run_stage0_runtime.sh
spot-one-map :
	@test -n "$(DRAGON_BIN)" || \
	  (echo "set DRAGON_BIN to a current SPOT executable" >&2; exit 2)
	DRAGON_BIN="$(DRAGON_BIN)" sh validation/iterative/run_one_map_runtime.sh
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
