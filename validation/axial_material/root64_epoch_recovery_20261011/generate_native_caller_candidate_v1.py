"""Source-only full FLU/FLUDRV caller derivation; no compiler/native run."""
from pathlib import Path
import hashlib
import json
import os
import resource
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'native_producer_chain_source/caller_candidate_v1'
START=time.monotonic()

def sha(data): return hashlib.sha256(data).hexdigest()
def identity(s): return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(path):
    before=identity(path.lstat())
    with path.open('rb') as f:
        opened=identity(os.fstat(f.fileno())); data=f.read(); eof=identity(os.fstat(f.fileno()))
    after=identity(path.lstat())
    assert before==opened==eof==after and len(data)==after[4],str(path)
    return data,dict(path=str(path),bytes=len(data),sha256=sha(data),identity=after,fullEOF_stable=True)

class ExactSource:
    def __init__(self,path,expected):
        self.original,self.original_pin=fullpin(path)
        assert self.original_pin['sha256']==expected,str(path)
        self.source=self.original.decode('utf8'); self.steps=[]
    def replace(self,label,old,new):
        assert self.source.count(old)==1,label
        before=self.source.encode('utf8'); pos=before.index(old.encode('utf8'))
        self.source=self.source.replace(old,new,1); after=self.source.encode('utf8')
        assert after[:pos]==before[:pos] and after[pos+len(new.encode('utf8')):]==before[pos+len(old.encode('utf8')):],label
        self.steps.append(dict(label=label,mode='one_exact_local_byte_splice',byte_offset_in_step_input=pos,
            old=old,new=new,old_bytes=len(old.encode('utf8')),new_bytes=len(new.encode('utf8')),
            before_sha256=sha(before),after_sha256=sha(after),outside_splice_exact_bytes_equal=True))
    def save(self,name):
        data=self.source.encode('utf8'); inverse=data
        assert max(map(len,data.splitlines()))<=132,name
        for s in reversed(self.steps):
            assert sha(inverse)==s['after_sha256'],s['label']
            pos=s['byte_offset_in_step_input']; new=s['new'].encode('utf8')
            assert inverse[pos:pos+len(new)]==new,s['label']
            inverse=inverse[:pos]+s['old'].encode('utf8')+inverse[pos+len(new):]
            assert sha(inverse)==s['before_sha256'],s['label']
        assert inverse==self.original,name
        (OUT/name).write_bytes(data)
        (OUT/'read_only_original'/Path(self.original_pin['path']).name).write_bytes(self.original)
        proof=dict(classification='COMPLETE_ORIGINAL_SOURCE_EXACT_LOCAL_BYTE_TRANSFORM_INVERSE_ONLY',
            original_source=self.original_pin,candidate_source_sha256=sha(data),steps=self.steps,
            local_transform_count=len(self.steps),complete_inverse_equals_original_bytes=True,
            complete_inverse_sha256=sha(inverse),maximum_source_line_bytes=max(map(len,data.splitlines())),
            compiler_or_parser_executed=False,Native_or_numerical_executed=False)
        proof_path=OUT/(name+'.EXACT_INVERSE_PROOF.json')
        proof_path.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf8')
        return dict(candidate_source=fullpin(OUT/name)[1],inverse_proof=fullpin(proof_path)[1],
            local_transform_count=len(self.steps),complete_inverse_equals_original_bytes=True)

base_manifest_data,base_manifest_pin=fullpin(REC/'native_producer_chain_source/NATIVE_PRODUCER_SOURCE_PINS_SEED_AUDIT_AND_SCOPE.json')
base_manifest=json.loads(base_manifest_data)
protected=[ROOT/'src/FLU.f',ROOT/'src/FLUDRV.f',ROOT/'src/FLU2DR64.f',
    REC/'native_producer_chain_source/AXMAT_CONTINUOUS_DRIVER64.f',
    REC/'native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90',
    REC/'new_source/SPOR64_BOOT64.f90',REC/'new_source/SPOBOOT64.f90',
    REC/'continuous_chain_source/SPOSTATE64.f90',REC/'projection_chain_source/SPOPROJ64.f90']
before={str(p):fullpin(p)[1] for p in protected}
assert before[str(protected[3])]['sha256']=='fff770a409704a3c9283aedeb4f59a5fb17384ccd405508c0a6f338ce76f9fca'
assert before[str(protected[4])]['sha256']=='650a785b277bd5266f797b5bd026e1e8977f48ac17cb986b84c13ac1955ccd3e'
oldpins=base_manifest['protected_Source_after']
flu=ExactSource(ROOT/'src/FLU.f',oldpins[str(ROOT/'src/FLU.f')]['sha256'])
drv=ExactSource(ROOT/'src/FLUDRV.f',oldpins[str(ROOT/'src/FLUDRV.f')]['sha256'])
OUT.mkdir(exist_ok=True)
(OUT/'read_only_original').mkdir(exist_ok=True)

drv.replace('new isolated complete driver symbol; diagnostics remain original',
    '*DECK FLUDRV\n      SUBROUTINE FLUDRV(',
'''*DECK FLUDRVN64
*     NEW SOURCE: complete retained FLUDRV with a typed native MCCG path.
*     SPOT still calls its original FLU2DR64, never the MCCG driver.
*     Native output validity returns only after the full original header.
      SUBROUTINE FLUDRVN64(''')
drv.replace('append native selector and actual allocatable terminal outputs',
    '     4 MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64)\n',
'''     4 MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64,LNATIVE,
     5 TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,
     6 TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,
     7 TERMINAL_VALID)
''')
drv.replace('actual typed producer and strict loader imports','      USE GANLIB\n',
'''      USE GANLIB
      USE ISO_FORTRAN_ENV, ONLY: REAL64
      USE AXMAT_NATIVE_PRODUCER_CHAIN, ONLY: AXMAT_CONTINUOUS_DRIVER64,
     1 AXMAT_LOAD_WARM_NATIVE64,AXMAT_SEED64_LOADED
''')
drv.replace('make original implicit EPSOUT explicit at its unchanged kind',
    '      REAL        EPSUNK,EPSINR,B2(4),VOL(NREG)\n',
    '      REAL        EPSUNK,EPSINR,EPSOUT,B2(4),VOL(NREG)\n')
drv.replace('typed terminal ABI and exclusively REAL64 seed storage',
    '      DOUBLE PRECISION REFKEF\n',
'''      DOUBLE PRECISION REFKEF
      LOGICAL, INTENT(IN) :: LNATIVE
      REAL(REAL64), ALLOCATABLE, INTENT(OUT) :: TERMINAL_FLUX64(:,:),
     1 TERMINAL_SOURCE64(:,:)
      REAL(REAL64), INTENT(OUT) :: TERMINAL_KEFF64,
     1 TERMINAL_RESID64(3)
      INTEGER, INTENT(OUT) :: TERMINAL_COUNTERS(2),
     1 TERMINAL_INNER_STATE
      LOGICAL, INTENT(OUT) :: TERMINAL_VALID
      REAL(REAL64), ALLOCATABLE :: INITIAL_FLUX64(:,:)
      REAL(REAL64) SEED_KEFF64
      INTEGER NATIVE_SEED_STATUS
      LOGICAL NATIVE_KERNEL_VALID
''')
drv.replace('fail-closed native outputs and door distinction before work',
    '      IF(LR64) THEN\n',
'''      TERMINAL_VALID=.FALSE.
      TERMINAL_KEFF64=0.0D0
      TERMINAL_RESID64=0.0D0
      TERMINAL_COUNTERS=0
      TERMINAL_INNER_STATE=0
      NATIVE_KERNEL_VALID=.FALSE.
      IF(LNATIVE) THEN
        IF(CXDOOR.NE.'MCCG'.OR.ITYPEC.NE.2.OR.ILEAK.NE.0.OR.
     1     .NOT.LFORW.OR.LEAKSW.OR.INITFL.NE.1.OR.LR64)
     2   CALL XABORT('FLUDRVN64: INVALID NATIVE MCCG WARM ROUTE.')
        IF(NREG.NE.8.OR.NUN.NE.14.OR.NMAT.NE.8.OR.NGRP.NE.370.OR.
     1     NIFIS.NE.32.OR.NLF.NE.1.OR.NLIN.NE.1.OR.NFUNL.NE.1)
     2   CALL XABORT('FLUDRVN64: UNDECLARED NATIVE SHAPE.')
      ENDIF
      IF(LR64) THEN
''')
start=drv.source.index("      IF(LFORW) THEN\n        CALL LCMLEN(IPFLUX,'FLUX',ILINIT,ITYLCM)\n")
finish=drv.source.index('  130   CONTINUE\n      ENDIF\n',start)+len('  130   CONTINUE\n      ENDIF\n')
oldinit=drv.source[start:finish]
drv.replace('full native type4 warm load bypasses only legacy uniform initialization',oldinit,
'''      IF(LNATIVE) THEN
        CALL AXMAT_LOAD_WARM_NATIVE64(IPFLUX,NUN,NGRP,INITIAL_FLUX64,
     1   SEED_KEFF64,NATIVE_SEED_STATUS)
        IF(NATIVE_SEED_STATUS.NE.AXMAT_SEED64_LOADED) CALL XABORT(
     1   'FLUDRVN64: COMPLETE TYPE4 WARM SEED ADMISSION FAILED.')
        ALLOCATE(TERMINAL_FLUX64(NUN,NGRP),
     1   TERMINAL_SOURCE64(NUN,NGRP))
        TERMINAL_FLUX64=0.0D0
        TERMINAL_SOURCE64=0.0D0
      ELSE
'''+oldinit+'''      ENDIF
''')
drv.replace('actual native solve call before separately preserved SPOT branch',
    "      IF(CXDOOR.EQ.'SPOT') THEN\n      CALL FLU2DR64(",
'''      IF(LNATIVE) THEN
      CALL AXMAT_CONTINUOUS_DRIVER64(IPRT,IPMACR,IPFLUX,IPSYS,IPTRK,
     1 IPFLUP,IPSOU,IGPT,IFTRAK,CXDOOR,TITLE,NUN,NREG,NSOUT,NANIS,
     2 NLF,NLIN,NFUNL,NGRP,NMAT,NIFIS,LFORW,LEAKSW,MAXINR,EPSINR,
     3 MAXOUT,EPSUNK,EPSOUT,IFRITR,IACITR,ITYPEC,IPHASE,ITPIJ,
     4 ILEAK,OPTION,REFKEF,MATCOD,KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,
     5 LREBAL,INITFL,NMERG,IMERG,INITIAL_FLUX64,TERMINAL_FLUX64,
     6 TERMINAL_SOURCE64,TERMINAL_KEFF64,TERMINAL_RESID64,
     7 TERMINAL_COUNTERS,TERMINAL_INNER_STATE,NATIVE_KERNEL_VALID)
      IF(.NOT.NATIVE_KERNEL_VALID) CALL XABORT(
     1 'FLUDRVN64: ACTUAL NATIVE STRICT TERMINAL REQUIRED.')
      ELSE IF(CXDOOR.EQ.'SPOT') THEN
      CALL FLU2DR64(''')
drv.replace('complete original header precedes caller-visible terminal validity',
    "      CALL LCMPTC(IPFLUX,'OPTION',4,OPTION)\n",
'''      CALL LCMPTC(IPFLUX,'OPTION',4,OPTION)
      IF(LNATIVE) THEN
        IF(.NOT.NATIVE_KERNEL_VALID) CALL XABORT(
     1   'FLUDRVN64: NATIVE HEADER WITHOUT STRICT TERMINAL.')
        DEALLOCATE(INITIAL_FLUX64)
        TERMINAL_VALID=.TRUE.
      ENDIF
''')

flu.replace('new standard CLE entry; keep original diagnostic Hollerith bytes',
    '*DECK FLU\n      SUBROUTINE FLU(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n',
'''*DECK FLUNAT64
*     NEW SOURCE, standard CLE entry with a true native MCCG warm path.
*     Full original FLU checks and all SPOT/other doors are retained.
*     Native only: read-only RCONTRACT and existing L_BOOTBIND operands.
*     No qualified GLOBAL64/QFISS/bootstrap epoch or online BOOT claim.
      SUBROUTINE FLUNAT64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)
''')
flu.replace('actual explicit driver interface and final publisher imports',
    '      USE ISO_FORTRAN_ENV, ONLY: INT64\n',
'''      USE ISO_FORTRAN_ENV, ONLY: INT32,INT64,REAL32,REAL64
      USE AXMAT_NATIVE_CALLER_API, ONLY: FLUDRVN64
      USE AXMAT_NATIVE_PRODUCER_CHAIN, ONLY: AXMAT_PUBLISH_REAL_TERMINAL64
      USE SPOR64_BOOT64, ONLY: ROOT64_PUBLISHED
      USE SPOR64_VERIFY, ONLY: ABSENT_RECORD,CHARACTER_RECORD_MATCHES,
     1 EXACT_INVENTORY,RECORD_MATCHES
''')
flu.replace('preserve complete material root and existing independent binding',
    '      TYPE(C_PTR) IPRCON\n',
'''      TYPE(C_PTR) IPRCON,IPMATERIAL,IPBIND
      INTEGER NATIVE_PLANE,NATIVE_EPOCH,NATIVE_PUBLISH_STATUS
      LOGICAL LNATIVE,NATIVE_TERMINAL_VALID
      REAL(REAL64), ALLOCATABLE :: NATIVE_FLUX64(:,:),NATIVE_SOURCE64(:,:)
      REAL(REAL64) NATIVE_KEFF64,NATIVE_RESID64(3)
      REAL(REAL32) NATIVE_TRACK_CONTROL(4)
      INTEGER NATIVE_COUNTERS(2),NATIVE_INNER_STATE
      CHARACTER(LEN=12), PARAMETER :: NATIVE_BIND_NAMES(3)=
     1 [CHARACTER(LEN=12) :: 'SIGNATURE','PLANE','EPOCH']
''')
flu.replace('initialize every new native handle/state without prior-call residue',
    '      IPRCON=C_NULL_PTR\n',
'''      IPRCON=C_NULL_PTR
      IPMATERIAL=C_NULL_PTR
      IPBIND=C_NULL_PTR
      LNATIVE=.FALSE.
      NATIVE_TERMINAL_VALID=.FALSE.
      NATIVE_PLANE=0
      NATIVE_EPOCH=-1
      NATIVE_PUBLISH_STATUS=0
      NATIVE_KEFF64=0.0D0
      NATIVE_RESID64=0.0D0
      NATIVE_COUNTERS=0
      NATIVE_INNER_STATE=0
''')
flu.replace('retain direct macro material identity alongside numerical macro handle',
    '          IPMACR=KENTRY(I1)\n          HPMACR=HENTRY(I1)\n',
'''          IPMACR=KENTRY(I1)
          IPMATERIAL=KENTRY(I1)
          HPMACR=HENTRY(I1)
''')
flu.replace('retain full microscopic library instead of only its macro child',
    "            IPMACR=LCMGID(KENTRY(I1),'MACROLIB')\n            HPMACR=HENTRY(I1)\n",
'''            IPMACR=LCMGID(KENTRY(I1),'MACROLIB')
            IPMATERIAL=KENTRY(I1)
            HPMACR=HENTRY(I1)
''')
flu.replace('recognize only the already established read-only L_BOOTBIND',
    "        ELSE IF((HSIGN.EQ.'L_SOURCE').AND.(.NOT.C_ASSOCIATED(IPSOU)))\n",
'''        ELSE IF((HSIGN.EQ.'L_BOOTBIND').AND.
     1  (.NOT.C_ASSOCIATED(IPBIND))) THEN
          IF(HENTRY(I1).NE.'BOOT_BIND') CALL XABORT(
     1     'FLUNAT64: NAMED READ-ONLY BOOT_BIND REQUIRED.')
          IPBIND=KENTRY(I1)
        ELSE IF((HSIGN.EQ.'L_SOURCE').AND.(.NOT.C_ASSOCIATED(IPSOU)))
''')
flu.replace('native MCCG admission uses actual track type before CXDOOR initialization',
    '      LR64=IR64MD.NE.0\n',
'''      LR64=IR64MD.NE.0
      IF(.NOT.RECORD_MATCHES(IPTRK,'TRACK-TYPE',3,3)) CALL XABORT(
     1 'FLUNAT64: COMPLETE TRACK-TYPE REQUIRED.')
      CALL LCMGTC(IPTRK,'TRACK-TYPE',12,CMODUL)
      LNATIVE=(CMODUL.EQ.'MCCG').AND.(IPHASE.EQ.1).AND.
     1 (ITYPEC.EQ.2)
      IF(LNATIVE) THEN
        IF(LR64.OR..NOT.REC.OR.INITFL.NE.1.OR.ILEAK.NE.0.OR.
     1     .NOT.LFORW.OR.LEAKSW.OR.IREBAL.NE.1.OR.NMERG.NE.1.OR.
     2     IMCAUD.NE.0) CALL XABORT(
     3   'FLUNAT64: ORIGINAL NATIVE MCCG WARM TYPE K ROUTE REQUIRED.')
        IF(.NOT.C_ASSOCIATED(IPMATERIAL).OR.
     1     .NOT.C_ASSOCIATED(IPRCON).OR..NOT.C_ASSOCIATED(IPBIND))
     2   CALL XABORT('FLUNAT64: MATERIAL/CONTRACT/BOOT_BIND REQUIRED.')
        IF((HPTRK.NE.'TRACK').OR.(HPSYS.NE.'SYSTEM').OR.
     1    ((HPMACR.NE.'MICROLIB2').AND.(HPMACR.NE.'MACRO0')))
     2   CALL XABORT('FLUNAT64: ORIGINAL NAMED NATIVE CONTEXT REQUIRED.')
        IF(C_ASSOCIATED(IPFLUX,IPMATERIAL).OR.
     1     C_ASSOCIATED(IPFLUX,IPTRK).OR.C_ASSOCIATED(IPFLUX,IPSYS).OR.
     2     C_ASSOCIATED(IPFLUX,IPRCON).OR.C_ASSOCIATED(IPFLUX,IPBIND))
     3   CALL XABORT('FLUNAT64: NATIVE OUTPUT ALIASES INPUT CONTEXT.')
        IF(.NOT.EXACT_INVENTORY(IPBIND,NATIVE_BIND_NAMES).OR.
     1     .NOT.CHARACTER_RECORD_MATCHES(IPBIND,'SIGNATURE',3,12,
     2     'L_BOOTBIND').OR..NOT.RECORD_MATCHES(IPBIND,'PLANE',1,1).OR.
     3     .NOT.RECORD_MATCHES(IPBIND,'EPOCH',1,1)) CALL XABORT(
     4   'FLUNAT64: COMPLETE INDEPENDENT BOOT_BIND REQUIRED.')
        CALL LCMGET(IPBIND,'PLANE',NATIVE_PLANE)
        CALL LCMGET(IPBIND,'EPOCH',NATIVE_EPOCH)
        IF(NATIVE_PLANE.LT.1.OR.NATIVE_PLANE.GT.3.OR.
     1     NATIVE_EPOCH.LT.0) CALL XABORT(
     2   'FLUNAT64: INVALID NATIVE PLANE/EPOCH BINDING.')
        CALL SPOR64_RCONTRACT_LOAD(IPRCON,RCON,LRCON)
        IF(.NOT.LRCON) CALL XABORT(
     1   'FLUNAT64: INDEPENDENT NATIVE ROUTE CONTRACT REQUIRED.')
        IF(TRANSFER(EPSINR,0_INT32).NE.RCON%EPS_RADIAL_BITS.OR.
     1     TRANSFER(EPSUNK,0_INT32).NE.RCON%EPS_RADIAL_BITS.OR.
     2     TRANSFER(EPSOUT,0_INT32).NE.RCON%EPS_RADIAL_BITS.OR.
     3     MAXOUT.NE.RCON%FLU_MAXOUT.OR.MAXINR.NE.RCON%FLU_MAXINR.OR.
     4     IFRITR.NE.RCON%FLU_ACCE_FREE.OR.
     5     IACITR.NE.RCON%FLU_ACCE_ACCEL.OR.
     6     COPTIO.NE.RCON%FLU_OPTION) CALL XABORT(
     7   'FLUNAT64: ORIGINAL NATIVE CONTROLS DIFFER FROM CONTRACT.')
        IF(.NOT.RECORD_MATCHES(IPTRK,'REAL-PARAM',4,2)) CALL XABORT(
     1   'FLUNAT64: ACTUAL MCCG CUTOFF REQUIRED.')
        CALL LCMGET(IPTRK,'REAL-PARAM',NATIVE_TRACK_CONTROL)
        IF(TRANSFER(NATIVE_TRACK_CONTROL(1),0_INT32).NE.
     1     TRANSFER(2.5E-8_REAL32,0_INT32).OR.
     2     TRANSFER(NATIVE_TRACK_CONTROL(1),0_INT32).NE.
     3     RCON%EPS_MCCG_BITS.OR.ANY(NATIVE_TRACK_CONTROL(2:4).NE.0.0))
     4   CALL XABORT('FLUNAT64: RETAINED ACTUAL MCCG CUTOFF MISMATCH.')
        IF(.NOT.ABSENT_RECORD(IPFLUX,'ROOT-FLUX64').OR.
     1     .NOT.ABSENT_RECORD(IPFLUX,'ROOT64-SEAL').OR.
     2     .NOT.ABSENT_RECORD(IPFLUX,'SPOT-R64')) CALL XABORT(
     3   'FLUNAT64: FRESH OWNED NATIVE TARGET WITHOUT OLD SEAL REQUIRED.')
      ELSE IF(C_ASSOCIATED(IPBIND)) THEN
        CALL XABORT('FLUNAT64: BOOT_BIND IS ONLY FOR NATIVE MCCG TYPE K.')
      ENDIF
''')
flu.replace('call the explicit actual driver interface with direct native outputs',
'''        CALL FLUDRV(IPRINT,IPFLUX,IPTRK,IPMACR,IPSOU,IFTRAK,IPSYS,
     1  IPHASE,ITPIJ,CXDOOR,ITRANC,TITLE,B2,INITFL,LFORW,LEAKSW,IREBAL,
     2  NGRP,NMAT,NIFIS,NANIS,NLF,NLIN,NFUNL,COPTIO,NUN,MAXINR,EPSINR,
     3  MAXOUT,EPSUNK,EPSOUT,IFRITR,IACITR,ITYPEC,ILEAK,NREG,NSOUT,
     4  MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64)
''',
'''        CALL FLUDRVN64(IPRINT,IPFLUX,IPTRK,IPMACR,IPSOU,IFTRAK,IPSYS,
     1  IPHASE,ITPIJ,CXDOOR,ITRANC,TITLE,B2,INITFL,LFORW,LEAKSW,IREBAL,
     2  NGRP,NMAT,NIFIS,NANIS,NLF,NLIN,NFUNL,COPTIO,NUN,MAXINR,EPSINR,
     3  MAXOUT,EPSUNK,EPSOUT,IFRITR,IACITR,ITYPEC,ILEAK,NREG,NSOUT,
     4  MATCOD,KEYFLX,VOL,REFKEF,NMERG,IMERG,IMCAUD,LR64,LNATIVE,
     5  NATIVE_FLUX64,NATIVE_SOURCE64,NATIVE_KEFF64,NATIVE_RESID64,
     6  NATIVE_COUNTERS,NATIVE_INNER_STATE,NATIVE_TERMINAL_VALID)
''')
flu.replace('publisher is the final original-normal-exit native operation',
'''*  RELEASE GENERAL TRACKING INFORMATION.
*----
      DEALLOCATE(IMERG)
''',
'''*  RELEASE GENERAL TRACKING INFORMATION.
*----
*     Complete FLUDRV header and every later original FLU check precede
*     publication. No reconstructed residual or synthetic terminal enters.
      IF(LNATIVE) THEN
        IF(.NOT.NATIVE_TERMINAL_VALID.OR.
     1     .NOT.ALLOCATED(NATIVE_FLUX64).OR.
     2     .NOT.ALLOCATED(NATIVE_SOURCE64)) CALL XABORT(
     3   'FLUNAT64: COMPLETE ACTUAL NATIVE TERMINAL REQUIRED.')
        CALL AXMAT_PUBLISH_REAL_TERMINAL64(IPFLUX,IPTRK,IPSYS,
     1   IPMATERIAL,IPRCON,NATIVE_PLANE,NATIVE_EPOCH,NATIVE_FLUX64,
     2   NATIVE_SOURCE64,NATIVE_KEFF64,NATIVE_RESID64,NATIVE_COUNTERS,
     3   NATIVE_INNER_STATE,NATIVE_TERMINAL_VALID,NATIVE_PUBLISH_STATUS)
        IF(NATIVE_PUBLISH_STATUS.NE.ROOT64_PUBLISHED) CALL XABORT(
     1   'FLUNAT64: ACTUAL NATIVE TERMINAL PUBLICATION REFUSED.')
        DEALLOCATE(NATIVE_SOURCE64,NATIVE_FLUX64)
      ENDIF
      DEALLOCATE(IMERG)
''')

drv_source=drv.source
assert drv_source.count('CALL AXMAT_CONTINUOUS_DRIVER64(')==1
assert drv_source.count('CALL AXMAT_LOAD_WARM_NATIVE64(')==1
assert drv_source.count('CALL FLU2DR64(')==1
assert "ELSE IF(CXDOOR.EQ.'SPOT') THEN\n      CALL FLU2DR64(" in drv_source
assert drv_source.index("CALL LCMPTC(IPFLUX,'OPTION'")<drv_source.index('TERMINAL_VALID=.TRUE.')
assert flu.source.count('CALL AXMAT_PUBLISH_REAL_TERMINAL64(')==1
assert flu.source.index("'FLU: MISSING SPOD INFORMATION.'")<flu.source.index('CALL AXMAT_PUBLISH_REAL_TERMINAL64(')
assert flu.source.index("'FLU: INVALID SYSTEM SPOT-LEAK1D LENGTH.'")<flu.source.index('CALL AXMAT_PUBLISH_REAL_TERMINAL64(')
outputs=[drv.save('FLUDRVN64.f'),flu.save('FLUNAT64.f')]
api_data,api_pin=fullpin(OUT/'AXMAT_NATIVE_CALLER_API.f90')
assert max(map(len,api_data.splitlines()))<=132
after={str(p):fullpin(p)[1] for p in protected}
assert before==after
manifest=dict(classification='NEW_COMPLETE_NATIVE_CALLER_SOURCE_ONLY_NOT_COMPILED_OR_RUN',
    full_original_derivations=outputs,explicit_API_source=api_pin,base_producer_source_manifest=base_manifest_pin,
    generator=fullpin(Path(__file__))[1],protected_before=before,protected_after=after,
    protected_fullEOF_SHA_7ID_unchanged=True,
    standard_CLE_entry='FLUNAT64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)',
    additional_input_operand='Existing L_BOOTBIND SIGNATURE/PLANE/EPOCH, read-only BOOT_BIND plus RCONTRACT',
    true_native_calls_in_source=['FLUNAT64 -> FLUDRVN64 -> AXMAT_LOAD_WARM_NATIVE64 -> AXMAT_CONTINUOUS_DRIVER64',
        'FLUDRVN64 full original header -> FLUNAT64 full original checks -> AXMAT_PUBLISH_REAL_TERMINAL64 -> SPOR64_BOOT64_PUBLISH_NATIVE'],
    SPOT_kept_distinct='LNATIVE=false; original FLU2DR64 call retained verbatim, not replaced by MCCG',
    original_material_threshold_iteration_preserved=True,
    no_dispatcher_or_deck_installed=True,old_wholeInput_or_17controls_qualification_inherited=False,
    full_GLOBAL_QFISS_BOOT_physical_qualification=False,
    compiler_or_parser_executed=False,Native_or_numerical_executed=False,
    remaining_runtime_build=['Root bounded compile/link of API,FLUDRVN64,FLUNAT64 with pinned real driver/helper/dependencies',
        'dispatcher registration FLUNAT64 and new independently pinned warm case deck',
        'actual full-type4 seed loader/transport/native publisher controls and strict execution',
        'external complete-input/output SHA/7ID binding','continuous global SPOT ingress plus GLOBAL64/QFISS/bootstrap epoch/online BOOT',
        'original rank2, AAA, independent coupled reference and ABA scientific qualification'],
    own_elapsed_seconds=time.monotonic()-START,own_peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
manifest_path=OUT/'CURRENT_COMPLETE_CALLER_SOURCE_PINS_AND_SCOPE.json'
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(candidate_sources=[item['candidate_source'] for item in outputs]+[api_pin],
    exact_full_original_inverse_verified=True,local_transform_counts=[item['local_transform_count'] for item in outputs],
    protected_fullEOF_SHA_7ID_unchanged=True,manifest=fullpin(manifest_path)[1],
    compiler_or_parser_executed=False,Native_or_numerical_executed=False,
    own_elapsed_seconds=time.monotonic()-START,own_peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))
