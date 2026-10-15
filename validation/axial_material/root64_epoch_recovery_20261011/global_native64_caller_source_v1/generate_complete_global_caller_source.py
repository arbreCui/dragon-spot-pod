#!/usr/bin/env python3
"""Write complete isolated FLU/parser/driver callers. No business subprocess."""
from pathlib import Path
import json,runpy,re,os,ast,hashlib
ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'global_native64_caller_source_v1'
V2=REC/'global_native64_dependency_source_v2'
base=runpy.run_path(str(V2/'driver_source/generate_global_native64_dependency_source.py'))
Transform=base['Transform'];read_pin=base['read_pin'];fresh=base['fresh'];fresh_json=base['fresh_json']


def main():
    targets=['FLUGLOBAL64.f','FLUDRVG64.f','FLUGPG64.f','SPOT_GLOBAL_CALLER_API.f90',
             'ORIGINAL_COMPLETE_FLU.f','ORIGINAL_COMPLETE_FLUDRV.f','ORIGINAL_COMPLETE_FLUGPI.f','ORIGINAL_COMPLETE_REVIEWED_CALLER_API.f90',
             'COMPLETE_GLOBAL_CALLER_EXACT_BYTE_INVERSE_PROOFS.json','CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json']
    assert all(not(OUT/x).exists() for x in targets)
    freeze=json.loads(read_pin(V2/'COMPLETE_GLOBAL_NATIVE64_DEPENDENCY_SOURCE_FREEZE.json')[0])
    protected=[Path(x['path']) for x in freeze['fixed_regular_files']]+[V2/'COMPLETE_GLOBAL_NATIVE64_DEPENDENCY_SOURCE_FREEZE.json']
    protected += [ROOT/'src/FLU.f',ROOT/'src/FLUDRV.f',ROOT/'src/FLUGPI.f']
    before=[read_pin(x)[1] for x in protected]
    assert before[:len(freeze['fixed_regular_files'])]==freeze['fixed_regular_files']
    originals={k:read_pin(ROOT/'src'/v) for k,v in [('FLU','FLU.f'),('DRV','FLUDRV.f'),('GPI','FLUGPI.f')]}
    transforms={k:Transform(v[0]) for k,v in originals.items()}
    g=transforms['GPI']
    g.splice('new independent full parser DECK','*DECK FLUGPI\n','*DECK FLUGPG64\n')
    g.splice('new independent actual parser procedure','      SUBROUTINE FLUGPI(','      SUBROUTINE FLUGPG64(')
    g.splice('native B2 helper exact interface','      USE GANLIB\n','      USE GANLIB\n      USE SPOT_GLOBAL_CALLER_CARRIERS, ONLY:\n     1 SPOT_GLOBAL_LOAD_B2_NATIVE64\n')
    g.splice('native parser B2 and direction controls','      REAL        EPSOUT,EPSUNK,EPSINR,B2(4)\n','      REAL        EPSOUT,EPSUNK,EPSINR\n      DOUBLE PRECISION B2(4)\n      LOGICAL B2_NATIVE_OK\n')
    g.splice('native directional seed control carrier','      REAL        REALIR,BSDIR(NSDIR),EPSCON(5)\n','      REAL        REALIR,EPSCON(5),MACRO_B232(3),MACRO_B2S32\n      DOUBLE PRECISION BSDIR(NSDIR)\n')
    g.splice('all four initial B2 values explicit, CONT required native before parser',"      ISDIR=0\n      COPTIO='B0'\n",'      B2=0.0D0\n      IF(REC) THEN\n        CALL SPOT_GLOBAL_LOAD_B2_NATIVE64(IPFLUX,B2,B2_NATIVE_OK)\n        IF(.NOT.B2_NATIVE_OK) CALL XABORT(\n     1   "FLUGPG64: COMPLETE NATIVE CONT B2 REQUIRED.")\n      ENDIF\n      ISDIR=0\n'+"      COPTIO='B0'\n")
    g.splice('CONT directional buckling from native carrier only',"           CALL LCMGET(IPFLUX,'B2  HETE',BSDIR)\n",'           BSDIR(:3)=B2(:3)\n')
    g.splice('CONT scalar buckling from native carrier only',"           CALL LCMGET(IPFLUX,'B2  B1HOM',BSDIR(5))\n",'           BSDIR(5)=B2(4)\n')
    g.splice('static macro directional type2 exact promotion buffer',
             "            CALL LCMGET(IPMACR,'B2  HETE',BSDIR)\n",
             "            CALL LCMGET(IPMACR,'B2  HETE',MACRO_B232)\n"
             '            BSDIR(:3)=DBLE(MACRO_B232)\n')
    g.splice('static macro scalar type2 exact promotion buffer',
             "           CALL LCMGET(IPMACR,'B2  B1HOM',BSDIR(5))\n",
             "           CALL LCMGET(IPMACR,'B2  B1HOM',MACRO_B2S32)\n"
             '           BSDIR(5)=DBLE(MACRO_B2S32)\n')

    d=transforms['DRV']
    d.splice('new independent full driver DECK','*DECK FLUDRV\n','*DECK FLUDRVG64\n')
    d.splice('new independent actual driver entry','      SUBROUTINE FLUDRV(','      SUBROUTINE FLUDRVG64(')
    d.splice('append actual continuation selector and full native return','     4 MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64)\n','     4 MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64,LGCONT,\n     5 TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,\n     6 TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,\n     7 TERMINAL_VALID)\n')
    d.splice('full typed driver and warm helper interfaces','      USE GANLIB\n','      USE GANLIB\n      USE SPOT_GLOBAL_NATIVE_DRIVER_API, ONLY:\n     1 SPOT_GLOBAL_NATIVE_DRIVER64\n      USE SPOT_GLOBAL_CALLER_CARRIERS, ONLY:\n     1 SPOT_GLOBAL_LOAD_WARM64\n')
    d.splice('real64 actual B2 driver argument','      REAL        EPSUNK,EPSINR,B2(4),VOL(NREG)\n','      REAL        EPSUNK,EPSINR,VOL(NREG)\n      DOUBLE PRECISION B2(4)\n')
    d.splice('complete actual typed terminal interface declarations','      DOUBLE PRECISION REFKEF\n','      DOUBLE PRECISION REFKEF\n      LOGICAL, INTENT(IN) :: LGCONT\n      DOUBLE PRECISION, ALLOCATABLE, INTENT(OUT) ::\n     1 TERMINAL_FLUX64(:,:),TERMINAL_SOURCE64(:,:)\n      DOUBLE PRECISION, INTENT(OUT) :: TERMINAL_KEFF64,\n     1 TERMINAL_RESID64(3)\n      INTEGER, INTENT(OUT) :: TERMINAL_COUNTERS(2),\n     1 TERMINAL_INNER_STATE\n      LOGICAL, INTENT(OUT) :: TERMINAL_VALID\n      DOUBLE PRECISION, ALLOCATABLE :: INITIAL_FLUX64(:,:),\n     1 TDIF64(:,:),TDHOM64(:),TGAMMA64(:)\n      DOUBLE PRECISION INITIAL_B2_64(4),TB2_64(4),SEED_KEFF64\n      LOGICAL WARM_OK,KERNEL_VALID\n')
    d.splice('reset actual result before all work and enforce preserved native scope','      IF(LR64) THEN\n','      TERMINAL_VALID=.FALSE.\n      TERMINAL_KEFF64=0.0D0\n      TERMINAL_RESID64=0.0D0\n      TERMINAL_COUNTERS=0\n      TERMINAL_INNER_STATE=0\n      KERNEL_VALID=.FALSE.\n      IF(CXDOOR.NE."SPOT".OR.(ITYPEC.NE.2.AND.ITYPEC.NE.3))\n     1 CALL XABORT("FLUDRVG64: SPOT TYPE2/3 REQUIRED.")\n      IF(LGCONT.AND.INITFL.NE.1) CALL XABORT(\n     1 "FLUDRVG64: CONT REQUIRES FULL NATIVE INIT ON.")\n      IF(NUN.LE.0.OR.NGRP.LE.0.OR.NMERG.LE.0) CALL XABORT(\n     1 "FLUDRVG64: INVALID NATIVE DIMENSIONS.")\n      ALLOCATE(TERMINAL_FLUX64(NUN,NGRP),\n     1 TERMINAL_SOURCE64(NUN,NGRP),INITIAL_FLUX64(NUN,NGRP),\n     2 TDIF64(NMERG,NGRP),TDHOM64(NGRP),TGAMMA64(NGRP))\n      TERMINAL_FLUX64=0.0D0\n      TERMINAL_SOURCE64=0.0D0\n      INITIAL_FLUX64=0.0D0\n      INITIAL_B2_64=B2\n      IF(LGCONT) THEN\n        CALL SPOT_GLOBAL_LOAD_WARM64(IPFLUX,NUN,NGRP,NREG,\n     1   KEYFLX(:,1,1),INITIAL_FLUX64,SEED_KEFF64,WARM_OK)\n        IF(.NOT.WARM_OK) CALL XABORT(\n     1   "FLUDRVG64: COMPLETE NATIVE CONT FIELD REQUIRED.")\n      ENDIF\n      IF(LR64) THEN\n')
    d.splice('exact original cold scalar1 and other unknown0 mathematical rule',
             '              IF(IND.GT.0) FLUXO(IND,IGR)=1.0\n',
             '              IF(IND.GT.0) THEN\n                FLUXO(IND,IGR)=1.0\n                IF(.NOT.LGCONT) INITIAL_FLUX64(IND,IGR)=1.0D0\n              ENDIF\n')
    d.splice('B2 legacy scalar record is output-only mirror',"CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,B2(4))","CALL LCMPUT(IPFLUX,'B2  B1HOM',1,2,REAL(B2(4)))")
    d.splice('retained unreachable heterogeneous record is output-only mirror',"CALL LCMPUT(IPFLUX,'B2  HETE',3,2,B2)","CALL LCMPUT(IPFLUX,'B2  HETE',3,2,REAL(B2))")
    d.splice('actual complete native60 argument SPOT driver invocation',
             '      CALL FLU2DR64(IPRT,IPMACR,IPFLUX,IPSYS,IPTRK,IPFLUP,IPSOU,IGPT,\n'
             '     1 IFTRAK,CXDOOR,TITLE,NUN,NREG,NSOUT,NANIS,NLF,NLIN,NFUNL,NGRP,\n'
             '     2 NMAT,NIFIS,LFORW,LEAKSW,MAXINR,EPSINR,MAXOUT,EPSUNK,EPSOUT,\n'
             '     3 IFRITR,IACITR,ITYPEC,IPHASE,ITPIJ,ILEAK,OPTION,REFKEF,MATCOD,\n'
             '     4 KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG)\n',
             '      CALL SPOT_GLOBAL_NATIVE_DRIVER64(IPRT,IPMACR,IPFLUX,IPSYS,\n'
             '     1 IPTRK,IPFLUP,IPSOU,IGPT,IFTRAK,CXDOOR,TITLE,NUN,NREG,NSOUT,\n'
             '     2 NANIS,NLF,NLIN,NFUNL,NGRP,NMAT,NIFIS,LFORW,LEAKSW,\n'
             '     3 MAXINR,EPSINR,MAXOUT,EPSUNK,EPSOUT,IFRITR,IACITR,ITYPEC,\n'
             '     4 IPHASE,ITPIJ,ILEAK,OPTION,REFKEF,MATCOD,KEYFLX,VOL,XSTRC,\n'
             '     5 XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG,INITIAL_FLUX64,\n'
             '     6 TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,\n'
             '     7 TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,\n'
             '     8 KERNEL_VALID,INITIAL_B2_64,TB2_64,TDIF64,TDHOM64,TGAMMA64)\n'
             '      IF(.NOT.KERNEL_VALID) CALL XABORT(\n'
             '     1 "FLUDRVG64: ACTUAL STRICT NATIVE TERMINAL REQUIRED.")\n'
             '      B2=TB2_64\n')
    d.splice('complete original driver headers precede return validity',
             '      DEALLOCATE(XSTK,XSNUF,XSCHI,XSDIA,XSTRC,FLUXO)\n      RETURN\n',
             '      DEALLOCATE(XSTK,XSNUF,XSCHI,XSDIA,XSTRC,FLUXO)\n'
             '      DEALLOCATE(INITIAL_FLUX64,TDIF64,TDHOM64,TGAMMA64)\n'
             '      TERMINAL_VALID=KERNEL_VALID\n      RETURN\n')

    f=transforms['FLU']
    f.splice('new independent full global FLU DECK','*DECK FLU\n','*DECK FLUGLOBAL64\n')
    f.splice('new actual standard five tuple CLE entry','      SUBROUTINE FLU(','      SUBROUTINE FLUGLOBAL64(')
    f.splice('true typed caller and real canonical publisher interfaces','      USE GANLIB\n',
             '      USE GANLIB\n      USE SPOT_GLOBAL_CALLER_API, ONLY: FLUDRVG64\n'
             '      USE SPOR64_BOOT_CANONICAL64_V2, ONLY:\n     1 SPOR64_BOOT_CANONICAL64_WRITE\n'
             '      USE SPOR64_BOOT_PUBLISH64, ONLY: SPOR64_BOOT_GLOBAL_PUBLISH,\n     1 SPOR64_BOOT_GLOBAL_PUBLISHED\n')
    f.splice('native B2 and live result variables','      REAL B2(4)\n','      DOUBLE PRECISION B2(4),TERMINAL_KEFF64,TERMINAL_RESID64(3)\n      DOUBLE PRECISION, ALLOCATABLE :: TERMINAL_FLUX64(:,:),\n     1 TERMINAL_SOURCE64(:,:)\n      INTEGER TERMINAL_COUNTERS(2),TERMINAL_INNER_STATE,IGLOBAL_STAT\n      INTEGER IGLOBAL_LEN\n      TYPE(C_PTR) IPGLOBAL,IPARCH_BOOT\n      LOGICAL TERMINAL_VALID,CANONICAL_OK,GLOBAL_EMPTY,GLOBAL_LCM\n      CHARACTER GLOBAL_NAME*72,GLOBAL_DIRECTORY*12\n')
    f.splice('complete seven operand shape and fresh independent global preflight',
             '      IF(NENTRY.LE.1) THEN\n',
             '*     AX_CURRENT, GLOBAL_NEW, MACROLIB3, TRACK_AX, SYSTEM_NEXT,\n'
             '*     ARCH_BOOT, RCONTRACT. GLOBAL_NEW is separate and fresh.\n'
             '      TERMINAL_VALID=.FALSE.\n      IPARCH_BOOT=C_NULL_PTR\n'
             '      IF(NENTRY.NE.7) CALL XABORT(\n     1 "FLUGLOBAL64: EXACT SEVEN OPERANDS REQUIRED.")\n'
             '      IF((IENTRY(2).NE.1.AND.IENTRY(2).NE.2).OR.\n'
             '     1 JENTRY(2).NE.0.OR..NOT.C_ASSOCIATED(KENTRY(2)))\n'
             '     2 CALL XABORT("FLUGLOBAL64: FRESH GLOBAL OUTPUT REQUIRED.")\n'
             '      IPGLOBAL=KENTRY(2)\n'
             '      DO I1=1,NENTRY\n        IF(I1.EQ.2) CYCLE\n'
             '        IF(C_ASSOCIATED(IPGLOBAL,KENTRY(I1))) CALL XABORT(\n'
             '     1   "FLUGLOBAL64: INDEPENDENT GLOBAL OBJECT REQUIRED.")\n'
             '      ENDDO\n'
             '      CALL LCMINF(IPGLOBAL,GLOBAL_NAME,GLOBAL_DIRECTORY,\n'
             '     1 GLOBAL_EMPTY,IGLOBAL_LEN,GLOBAL_LCM)\n'
             '      IF(.NOT.GLOBAL_EMPTY.OR.IGLOBAL_LEN.NE.-1.OR.\n'
             '     1 TRIM(GLOBAL_DIRECTORY).NE."/") CALL XABORT(\n'
             '     2 "FLUGLOBAL64: EMPTY GLOBAL ROOT DIRECTORY REQUIRED.")\n'
             '      IF(ANY(JENTRY(3:7).NE.2)) CALL XABORT(\n'
             '     1 "FLUGLOBAL64: FIVE COMPLETE READONLY INPUTS REQUIRED.")\n'
             '      DO I1=3,7\n'
             '        IF(IENTRY(I1).NE.1.AND.IENTRY(I1).NE.2)\n'
             '     1   CALL XABORT("FLUGLOBAL64: READONLY LCM/XSM REQUIRED.")\n'
             '      ENDDO\n'
             '      IF(NENTRY.LE.1) THEN\n')
    f.splice('exclude fresh global output from original full RHS parser','      DO 10 I1=2,NENTRY\n','      DO 10 I1=3,NENTRY\n')
    f.splice('real readonly archive operand recognized',
             "        ELSE IF((HSIGN.EQ.'L_RCONTRACT').AND.\n",
             "        ELSE IF((HSIGN.EQ.'L_ARCHIVE').AND.\n"
             '     1  (.NOT.C_ASSOCIATED(IPARCH_BOOT))) THEN\n'
             '          IPARCH_BOOT=KENTRY(I1)\n'
             "        ELSE IF((HSIGN.EQ.'L_RCONTRACT').AND.\n")
    f.splice('both complete readonly bootstrap context operands mandatory',
             '*  RECOVER GENERAL TRACKING INFORMATION.\n',
             '*  RECOVER GENERAL TRACKING INFORMATION.\n'
             '*     Publisher receives real archive/contract pointers.\n'
             '      IF(.NOT.C_ASSOCIATED(IPMACR,KENTRY(3)).OR.\n'
             '     1 .NOT.C_ASSOCIATED(IPTRK,KENTRY(4)).OR.\n'
             '     2 .NOT.C_ASSOCIATED(IPSYS,KENTRY(5)).OR.\n'
             '     3 .NOT.C_ASSOCIATED(IPARCH_BOOT,KENTRY(6)).OR.\n'
             '     4 .NOT.C_ASSOCIATED(IPRCON,KENTRY(7))) CALL XABORT(\n'
             '     5 "FLUGLOBAL64: COMPLETE SEVEN OPERAND ORDER REQUIRED.")\n')
    f.splice('bootstrap archive and contract validated before initial parser',
             '      ISTATE(:NSTATE)=0\n',
             '      IF(.NOT.C_ASSOCIATED(IPARCH_BOOT).OR.\n'
             '     1 .NOT.C_ASSOCIATED(IPRCON)) CALL XABORT(\n'
             '     2 "FLUGLOBAL64: ARCH_BOOT AND RCONTRACT REQUIRED.")\n'
             '      ISTATE(:NSTATE)=0\n', 2)
    f.splice('complete native B2 continuation parser invocation','      CALL FLUGPI(','      CALL FLUGPG64(')
    f.splice('this standalone global route cannot enter radial R64 branch','      LR64=IR64MD.NE.0\n','      LR64=IR64MD.NE.0\n      IF(LR64) CALL XABORT(\n     1 "FLUGLOBAL64: GLOBAL TYPE K, NOT RADIAL R64 ROUTE.")\n')
    f.splice('complete original tracking to eligible native global door',
             "      IF(IMCAUD.NE.0) THEN\n",
             '      IF(CXDOOR.NE."SPOT".OR.(ITYPEC.NE.2.AND.ITYPEC.NE.3))\n'
             '     1 CALL XABORT("FLUGLOBAL64: SPOT TYPE2/3 REQUIRED.")\n'
             '      IF(IMCAUD.NE.0) THEN\n')
    f.splice('actual lower typed driver, no stored header masquerading as producer','        CALL FLUDRV(','        CALL FLUDRVG64(')
    f.splice('complete real terminal arrays returned to owning global operator',
             '     4  MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64)\n',
             '     4  MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64,REC,\n'
             '     5  TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,\n'
             '     6  TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,\n'
             '     7  TERMINAL_VALID)\n')
    f.splice('real canonical then real publisher only after complete original checks',
             '      DEALLOCATE(IMERG)\n      DEALLOCATE(KEYFLX,VOL,MATCOD)\n      RETURN\n',
             '      IF(.NOT.TERMINAL_VALID) CALL XABORT(\n'
             '     1 "FLUGLOBAL64: NO ACTUAL STRICT GLOBAL TERMINAL.")\n'
             '      CALL SPOR64_BOOT_CANONICAL64_WRITE(IPFLUX,IPTRK,IPSYS,\n'
             '     1 IPMACR,CANONICAL_OK)\n'
             '      IF(.NOT.CANONICAL_OK) CALL XABORT(\n'
             '     1 "FLUGLOBAL64: ACTUAL CANONICAL WRITE FAILED.")\n'
             '      CALL SPOR64_BOOT_GLOBAL_PUBLISH(IPGLOBAL,IPFLUX,IPTRK,\n'
             '     1 IPSYS,IPMACR,IPARCH_BOOT,IPRCON,TERMINAL_FLUX64,\n'
             '     2 TERMINAL_SOURCE64,TERMINAL_KEFF64,TERMINAL_RESID64,\n'
             '     3 TERMINAL_COUNTERS,TERMINAL_INNER_STATE,TERMINAL_VALID,\n'
             '     4 IGLOBAL_STAT)\n'
             '      IF(IGLOBAL_STAT.NE.SPOR64_BOOT_GLOBAL_PUBLISHED)\n'
             '     1 CALL XABORT("FLUGLOBAL64: GLOBAL PUBLICATION FAILED.")\n'
             '      DEALLOCATE(TERMINAL_FLUX64,TERMINAL_SOURCE64)\n'
             '      DEALLOCATE(IMERG)\n      DEALLOCATE(KEYFLX,VOL,MATCOD)\n      RETURN\n')

    api_path=REC/'native_producer_chain_source/caller_candidate_v1/AXMAT_NATIVE_CALLER_API.f90'
    api_raw,api_pin=read_pin(api_path)
    api=Transform(api_raw)
    api.splice('actual global owner Source-only publication scope',
               '  ! Real native terminal arrays are returned to FLUNAT64 for publication\n'
               '  ! only after all original FLU checks and complete headers have finished.\n',
               '  ! Real native terminal arrays are returned to FLUGLOBAL64 for publication\n'
               '  ! only after all original FLU checks and complete headers have finished.\n'
               '  ! Source-only; current external pins and real solve remain required.\n')
    api.rename('AXMAT_NATIVE_CALLER_API','SPOT_GLOBAL_CALLER_API',2)
    api.rename('FLUDRVN64','FLUDRVG64',4)
    api.rename('lnative','lgcont',2)
    api.splice('typed buckling ABI, static eps and geometry remain original',
               '      real(real32) :: epsunk,epsinr,epsout,b2(4),vol(nreg)\n',
               '      real(real32) :: epsunk,epsinr,epsout,vol(nreg)\n'
               '      real(real64) :: b2(4)\n')
    proof={k:t.verify() for k,t in transforms.items()};proof['API']=api.verify()
    mapping={'FLU':'FLUGLOBAL64.f','DRV':'FLUDRVG64.f','GPI':'FLUGPG64.f'}
    for k,v in mapping.items():
        fresh(OUT/v,transforms[k].raw)
        fresh(OUT/('ORIGINAL_COMPLETE_'+{'FLU':'FLU','DRV':'FLUDRV','GPI':'FLUGPI'}[k]+'.f'),originals[k][0])
    fresh(OUT/'SPOT_GLOBAL_CALLER_API.f90',api.raw)
    fresh(OUT/'ORIGINAL_COMPLETE_REVIEWED_CALLER_API.f90',api_raw)
    fresh_json(OUT/'COMPLETE_GLOBAL_CALLER_EXACT_BYTE_INVERSE_PROOFS.json',
               {'schema':'COMPLETE_GLOBAL_CALLER_WHOLE_BYTE_INVERSE_PROOFS_V1','proofs':proof,
                'full_original_basis_pins':{k:v[1] for k,v in originals.items()},'API_basis_pin':api_pin,
                'compiler_or_numeric_executed':False})
    after=[read_pin(x)[1] for x in protected];assert before==after
    ast.parse(read_pin(Path(__file__).resolve())[0])
    sources={k:read_pin(OUT/v)[1] for k,v in mapping.items()}
    sources.update(API=read_pin(OUT/'SPOT_GLOBAL_CALLER_API.f90')[1],
                   carriers=read_pin(OUT/'SPOT_GLOBAL_CALLER_CARRIERS.f90')[1])
    manifest={'schema':'CURRENT_COMPLETE_GLOBAL_TYPED_CALLER_SOURCE_BINDING_V1',
              'status':'COMPLETE_SOURCE_CANDIDATE_REAL_GLOBAL_DRIVER_AND_REAL_CANONICAL_PUBLISHER_CALLS',
              'source_pins':sources,'writer_pin':read_pin(Path(__file__).resolve())[1],
              'original_and_v2_frozen_Source_before':before,'original_and_v2_frozen_Source_after':after,
              'all_protected_Source_unchanged':True,'global_driver_60_ABI':freeze['eight_complete_Source_pins'],
              'actual_CLE_entry':'FLUGLOBAL64','seven_operand_order':['AX_CURRENT(new/mod)','GLOBAL_NEW(fresh independent empty tree)','MACROLIB3(readonly)','TRACK_AX(readonly)','SYSTEM_NEXT(readonly)','ARCH_BOOT(readonly)','RCONTRACT(readonly)'],
              'cold_rule':'Original FLUDRV scalar keys>0 = 1, all other unknowns = 0; direct REAL64 math, no mirror promotion.',
              'CONT_rule':'REC/JENTRY1 modification requires INIT ON; complete native FLUX64/SOUR64/keff/B2 and exact legacy mirrors; full dimensions/keys checks. GPI B2/BSDIR native64, old scalar mirror read removed from live CONT route.',
              'native_initial_vs_terminal_arrays_disjoint':True,
              'preserved':'Complete original FLU/FLUDRV/FLUGPI bodies, operand and physical checks, material extraction, parser/defaults/caps/eps/ACCE/TYPE K B1 SIGS->TYPE3, headers/links/SPOD and postchecks outside exact recorded changes.',
              'true_publication_order':'Original FLUDRV headers -> original complete FLU postchecks -> real SPOR64_BOOT_CANONICAL64_WRITE -> real SPOR64_BOOT_GLOBAL_PUBLISH receiving actual driver terminal arrays, not reconstructed records.',
              'new_publication_dependencies':[{'module':'SPOR64_BOOT_CANONICAL64_V2','entry':'SPOR64_BOOT_CANONICAL64_WRITE','path':str(REC/'bootstrap_qfiss_source_v2/SPOR64_BOOT_CANONICAL64_V2.f90'),'path_status':'progress preparing complete v2 TYPE3/B1 compatible Source; current physical pin required before build'},
                  {'module':'SPOR64_BOOT_PUBLISH64','entry':'SPOR64_BOOT_GLOBAL_PUBLISH','success_constant':'SPOR64_BOOT_GLOBAL_PUBLISHED','success_value':2,'path':str(REC/'bootstrap_global_projection_publish_source_v1/SPOR64_BOOT_PUBLISH64.f90'),'path_status':'Root complete Source saved but not frozen; current physical pin required before build'}],
              'publisher_can_only_commit_independent_full_global_tree_after_all_checks':True,
              'internal_type4_consistency_is_not_external_current_pins':True,
              'remaining':['Independent full Source review and final freeze','Pin actual complete canonical/publisher modules and current compiler/objects/lib','Dispatcher FLUGLOBAL64 entry and real production_inputs/deck route','Actual full original SPOT solve, externally bound strict global output, publisher/source controls/17/online BOOT/next epoch'],
              'Fortran_parser_or_compiler_executed':False,'transport_executed':False,
              'native_global_producer_qualified':False,'online_BOOT_qualified':False,'seventeen_controls_qualified':False,'whole_INPUT_admitted':False,'AAA_qualified':False,'ABA_admitted':False,'goal_complete':False}
    fresh_json(OUT/'CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json',manifest)
    print(json.dumps({'status':manifest['status'],'source_pins':sources,'inverse_step_counts':{k:v['actual_transform_steps'] for k,v in proof.items()},'manifest_pin':read_pin(OUT/'CURRENT_GLOBAL_CALLER_SOURCE_BINDING_AND_RUNTIME_SCOPE.json')[1],'compiler_or_numeric_executed':False}))


if __name__=='__main__':main()
