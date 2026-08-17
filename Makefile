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
