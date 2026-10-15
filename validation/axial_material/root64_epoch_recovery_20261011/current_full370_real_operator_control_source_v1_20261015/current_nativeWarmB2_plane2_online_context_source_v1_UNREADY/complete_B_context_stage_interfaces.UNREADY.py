"""UNREADY explicit complete-context interfaces only; no process, build or payload IO."""
PREFIX="XSM_FILE MACRO :: FILE './axial_macro.xsm' ;\nXSM_FILE AXTRACK :: FILE './axial_track.xsm' ;\nXSM_FILE BASIS :: FILE './basis.xsm' ;\nXSM_FILE PACK :: FILE './initial_pack.xsm' ;\nXSM_FILE GRCON :: FILE './global_rcon.xsm' ;\nXSM_FILE RCON1 :: FILE './plane1_rcon.xsm' ;\nXSM_FILE RCON2 :: FILE './plane2_rcon.xsm' ;\nXSM_FILE RCON3 :: FILE './plane3_rcon.xsm' ;\n"
BOOT_PREFIX="XSM_FILE PROJECT :: FILE './projected_boot.xsm' ;\nXSM_FILE AX :: FILE './ax_current.xsm' ;\nXSM_FILE AXTRACK :: FILE './axial_track.xsm' ;\nXSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;\nXSM_FILE AXMACRO :: FILE './axial_macro.xsm' ;\nXSM_FILE GRCON :: FILE './global_rcon.xsm' ;\nSEQ_BINARY TRACK_f1 :: FILE './radial1.bin' ;\nSEQ_BINARY TRACK_f2 :: FILE './radial2.bin' ;\nSEQ_BINARY TRACK_f3 :: FILE './radial3.bin' ;\nLINKED_LIST MICROLIB2 MACRO0 TRACK SYS1 SYS2 SYS3 ;\nMODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;\nMICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 1 EDIT 0 ;\nMACRO0 := MICROLIB2 ;\nMICROLIB2 := DELETE: MICROLIB2 ;\nSYS1 := ASM: MACRO0 TRACK TRACK_f1 PROJECT :: EDIT 0 ARM LK1D 1 ;\nMACRO0 TRACK := DELETE: MACRO0 TRACK ;\nMICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 2 EDIT 0 ;\nMACRO0 := MICROLIB2 ;\nMICROLIB2 := DELETE: MICROLIB2 ;\nSYS2 := ASM: MACRO0 TRACK TRACK_f2 PROJECT :: EDIT 0 ARM LK1D 2 ;\nMACRO0 TRACK := DELETE: MACRO0 TRACK ;\nMICROLIB2 TRACK := RECOVER: PROJECT :: ITEM 3 EDIT 0 ;\nMACRO0 := MICROLIB2 ;\nMICROLIB2 := DELETE: MICROLIB2 ;\nSYS3 := ASM: MACRO0 TRACK TRACK_f3 PROJECT :: EDIT 0 ARM LK1D 3 ;\nMACRO0 TRACK := DELETE: MACRO0 TRACK ;\n"
ROOT_NAMES={'AX': 'ax_current.xsm', 'AXTRACK': 'axial_track.xsm', 'AXSYSTEM': 'initial_system.xsm', 'AXMACRO': 'axial_macro.xsm', 'ARCHIVE': 'initial_pack.xsm', 'RCON': 'global_rcon.xsm'}

def complete_context_decks(plan):
    if plan['Source_admission_ready']is not True or plan['draft_unready']is not False:
        raise RuntimeError('independent Source/Root runtime/budget/current producer admission still required')
    if [(x['plane'],x['material'],x['expected_case'])for x in plan['producers']]!=[(1,'A','R64WARM-A-V1 '),(2,'B','R64WARM-B-V1 '),(3,'A','R64-A3-WARM1 ')]:
        raise RuntimeError('exact independent A1/B2/A3 producer plan')
    if any(x['archive']is None or x['radial_binary_track']is None for x in plan['producers']):
        raise RuntimeError('missing current epoch selected readonly role binding')
    # Paths below are fresh host-owned working copies, never old catalog aliases.
    pack=''
    for i in range(1,4):pack+=f"XSM_FILE RCON{i} :: FILE './plane{i}_rcon.xsm' ;\n"
    pack+="XSM_FILE PACK :: FILE './initial_pack.xsm' ;\n"
    for i in range(1,4):pack+=f"XSM_FILE {'B2'if i==2 else'A'+str(i)} :: FILE './producer{i}.xsm' ;\n"
    pack+='MODULE APACKX64: END: ;\nPACK RCON1 RCON2 RCON3 := APACKX64: A1 B2 A3 :: ;\nEND: ; QUIT "LIST" .\n'
    initial=PREFIX+"XSM_FILE SYSOUT :: FILE './initial_system.xsm' ;\nMODULE SPOOPP64: END: ;\nSYSOUT := SPOOPP64: MACRO AXTRACK PACK BASIS GRCON RCON1 RCON2 RCON3 :: RANK 1 EDIT 0 ;\nEND: ; QUIT \"LIST\" .\n"
    global_deck=PREFIX+"XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;\nXSM_FILE AX :: FILE './ax_current.xsm' ;\nXSM_FILE GLOBAL :: FILE './global.xsm' ;\nMODULE FLUGLOBAL64: END: ;\nAX GLOBAL := FLUGLOBAL64: MACRO AXTRACK AXSYSTEM PACK GRCON ::\n  EDIT -3 TYPE K B1 SIGS EXTE 500 5.00000000E-08 REBA OFF\n  ACCE 3 0 UNKT 5.00000000E-08 THER 740 5.00000000E-08 ;\nEND: ; QUIT \"LIST\" .\n"
    project=PREFIX+"XSM_FILE AXSYSTEM :: FILE './initial_system.xsm' ;\nXSM_FILE AX :: FILE './ax_current.xsm' ;\nXSM_FILE GLOBAL :: FILE './global.xsm' ;\nXSM_FILE PROJECT :: FILE './projected_boot.xsm' ;\nMODULE BPROJX64: END: ;\nPROJECT := BPROJX64: GLOBAL AX AXTRACK AXSYSTEM MACRO PACK GRCON :: RANK 1 ;\nEND: ; QUIT \"LIST\" .\n"
    plane2=BOOT_PREFIX.replace('MODULE RECOVER: ASM: DELETE: SPOBVX64: END: ;','MODULE RECOVER: ASM: DELETE: B2PLNX64: END: ;')+"XSM_FILE GLOBAL :: FILE './global.xsm' ;\nXSM_FILE PACK :: FILE './initial_pack.xsm' ;\nXSM_FILE FLUXOUT :: FILE './unsealed_plane2_flux.xsm' ;\nXSM_FILE QOUT :: FILE './unsealed_plane2_fixed_source.xsm' ;\nFLUXOUT QOUT := B2PLNX64: PROJECT GLOBAL AX AXTRACK AXSYSTEM AXMACRO PACK GRCON SYS1 SYS2 SYS3 TRACK_f1 TRACK_f2 TRACK_f3 :: RANK 1 EDIT 0 ;\nEND: ; QUIT \"LIST\" .\n"
    return dict(pack=pack,initial=initial,GLOBAL=global_deck,projection=project,plane2=plane2)
