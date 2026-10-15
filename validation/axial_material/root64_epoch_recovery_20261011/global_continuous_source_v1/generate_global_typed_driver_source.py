#!/usr/bin/env python3
"""Source-only full SPOT driver derivation; never imports/runs numerical code."""
import hashlib
import json
import os
from pathlib import Path
import re
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = REC / 'global_continuous_source_v1'
ORIGINAL = ROOT / 'src/FLU2DR64.f'
DRIVER = OUT / 'SPOT_GLOBAL_TYPED_DRIVER64.f'
API = OUT / 'SPOT_GLOBAL_TYPED_DRIVER_API.f90'
PROOF = OUT / 'SPOT_GLOBAL_TYPED_DRIVER64_EXACT_BYTE_INVERSE_PROOF.json'
MANIFEST = OUT / 'CURRENT_GLOBAL_TYPED_DRIVER_SOURCE_PINS_AND_BOUNDARY.json'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read_pin(path):
    path = Path(path)
    before = identity(path.stat())
    with path.open('rb') as handle:
        opened = identity(os.fstat(handle.fileno()))
        raw = handle.read()
        eof = identity(os.fstat(handle.fileno()))
    after = identity(path.stat())
    if before != opened or opened != eof or eof != after:
        raise RuntimeError('full EOF identity changed: ' + str(path))
    return raw, dict(path=str(path), size_bytes=len(raw),
                    sha256=hashlib.sha256(raw).hexdigest(), identity=before,
                    before_open_EOF_after_identity_equal=True,
                    read_scope='complete EOF')


def write_new(path, raw):
    with Path(path).open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


def write_json(path, data):
    write_new(path, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())


def main():
    started = time.monotonic()
    for target in (DRIVER, API, PROOF, MANIFEST, OUT / 'ORIGINAL_COMPLETE_FLU2DR64.f'):
        if target.exists() or target.is_symlink():
            raise RuntimeError('fresh candidate files required: ' + str(target))
    protected_paths = [ROOT / 'src/FLU2DR64.f', ROOT / 'src/FLUDRV.f', ROOT / 'src/FLU.f',
                       ROOT / 'src/B1HOM64.f90', ROOT / 'src/B1HXS1.f', ROOT / 'src/B1DIF.f',
                       REC / 'native_producer_chain_source/AXMAT_CONTINUOUS_DRIVER64.f',
                       REC / 'native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90',
                       REC / 'new_source/SPOR64_BOOT64.f90', REC / 'new_source/SPOBOOT64.f90',
                       REC / 'continuous_chain_source/SPOSTATE64.f90',
                       REC / 'projection_chain_source/SPOPROJ64.f90']
    protected_before = [read_pin(path)[1] for path in protected_paths]
    original, original_pin = read_pin(ORIGINAL)
    if original_pin['sha256'] != 'df3cfcb6c320f62afe91b6c63563173e4b510d1b142afb9baa2594d80d18db67':
        raise RuntimeError('reviewed complete original FLU2DR64 bytes required')
    data = original
    steps = []

    def splice(label, old, new):
        nonlocal data
        old = old.encode(); new = new.encode()
        if data.count(old) != 1:
            raise RuntimeError('exact unique splice expected: ' + label)
        offset = data.index(old)
        before = data
        data = before[:offset] + new + before[offset + len(old):]
        if data[:offset] != before[:offset] or data[offset + len(new):] != before[offset + len(old):]:
            raise RuntimeError('outside splice changed')
        steps.append(dict(label=label, mode='one_exact_local_byte_splice',
                          byte_offset_in_step_input=offset, old=old.decode(), new=new.decode(),
                          old_bytes=len(old), new_bytes=len(new),
                          before_sha256=hashlib.sha256(before).hexdigest(),
                          after_sha256=hashlib.sha256(data).hexdigest(),
                          outside_splice_exact_bytes_equal=True))

    splice('new independent SPOT driver entry only',
           '      SUBROUTINE FLU2DR64(', '      SUBROUTINE SPOT_GLOBAL_TYPED_DRIVER64(')
    old = b'FLUSP64'; new = b'SPOT_GLOBAL_FLUSP_TYPED64'
    before = data
    pattern = rb'\b' + re.escape(old) + rb'\b'
    occurrences = len(re.findall(pattern, data))
    if occurrences != 7:
        raise RuntimeError('complete private SPOT dispatch identifier namespace')
    data = re.sub(pattern, new, data)
    steps.append(dict(label='distinct complete retained SPOT door helper symbol',
                      mode='exact_identifier_token_rename', old=old.decode(), new=new.decode(),
                      occurrence_count=occurrences,
                      before_sha256=hashlib.sha256(before).hexdigest(),
                      after_sha256=hashlib.sha256(data).hexdigest()))
    splice('honest driver-only typed ABI and retained TYPE3 boundary header',
           '*DECK FLU2DR64\n',
           '*DECK SPOT_GLOBAL_TYPED_DRIVER64\n'
           '*     NEW SOURCE, entire retained SPOT TYPE2/3 kernel and door.\n'
           '*     This is a typed-driver candidate, not whole-chain qualification.\n'
           '*     Original B1HOM64 TYPE3 homogenization precision remains below.\n'
           '*     The separately recorded B1 dynamic-field gap must be repaired.\n'
           '*     INITIAL_FLUX64 is a full independently admitted real64 array.\n'
           '*     No fixed MCCG 8/14/370 shape or MCCG-only driver is used here.\n'
           '*     Validity is committed only after genuine strict normal return.\n')
    splice('append complete typed input and actual terminal output ABI',
           '     4 KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG)\n',
           '     4 KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG,\n'
           '     5 INITIAL_FLUX64,TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,\n'
           '     6 TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,\n'
           '     7 TERMINAL_VALID)\n')
    splice('explicit intrinsic kind and finite checks on new ABI',
           '      USE GANLIB\n      USE SPOMOC_AUDIT,',
           '      USE GANLIB\n'
           '      USE, INTRINSIC :: ISO_FORTRAN_ENV, ONLY: INT32,INT64,REAL32,\n'
           '     1 REAL64\n'
           '      USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY: IEEE_IS_FINITE\n'
           '      USE SPOMOC_AUDIT,')
    splice('complete typed ABI declarations and strict captured native values',
           '      DOUBLE PRECISION REFKEF\n',
           '      DOUBLE PRECISION REFKEF\n'
           '      DOUBLE PRECISION, INTENT(IN) :: INITIAL_FLUX64(NUNKNO,NGRP)\n'
           '      DOUBLE PRECISION, INTENT(OUT) ::\n'
           '     1 TERMINAL_FLUX64(NUNKNO,NGRP),TERMINAL_SOURCE64(NUNKNO,NGRP),\n'
           '     2 TERMINAL_KEFF64,TERMINAL_RESID64(3)\n'
           '      INTEGER, INTENT(OUT) :: TERMINAL_COUNTERS(2),\n'
           '     1 TERMINAL_INNER_STATE\n'
           '      LOGICAL, INTENT(OUT) :: TERMINAL_VALID\n'
           '      DOUBLE PRECISION CAPTURED_KEFF64,CAPTURED_RESID64(3)\n'
           '      INTEGER CAPTURED_COUNTERS(2),CAPTURED_INNER_STATE\n'
           '      LOGICAL TERMINAL_GATE_REACHED\n'
           '      INTEGER, PARAMETER :: KIND_GUARD=1/MERGE(1,0,\n'
           '     1 KIND(1).EQ.INT32.AND.KIND(1.0).EQ.REAL32.AND.\n'
           '     2 KIND(0.0D0).EQ.REAL64.AND.DP.EQ.REAL64)\n')
    splice('independent native terminal source carrier',
           '      TYPE(C_PTR) JPFLUX64\n', '      TYPE(C_PTR) JPFLUX64,JPSOUR64\n')
    splice('clear outputs before any kernel work and validate general typed input',
           '      ALLOCATE(IJJ(0:NMAT),NJJ(0:NMAT),IPOS(0:NMAT),NPSYS(NGRP))\n',
           '*     Never inherit previous output validity or a previous field.\n'
           '      TERMINAL_VALID=.FALSE.\n'
           '      TERMINAL_FLUX64=0.0D0\n'
           '      TERMINAL_SOURCE64=0.0D0\n'
           '      TERMINAL_KEFF64=0.0D0\n'
           '      TERMINAL_RESID64=0.0D0\n'
           '      TERMINAL_COUNTERS=0\n'
           '      TERMINAL_INNER_STATE=0\n'
           '      TERMINAL_GATE_REACHED=.FALSE.\n'
           '      CAPTURED_KEFF64=0.0D0\n'
           '      CAPTURED_RESID64=0.0D0\n'
           '      CAPTURED_COUNTERS=0\n'
           '      CAPTURED_INNER_STATE=0\n'
           '*     General declared SPOT dimensions; no MCCG fixed shape.\n'
           '      IF(NUNKNO.LE.0.OR.NREG.LE.0.OR.NMAT.LE.0.OR.NGRP.LE.0.OR.\n'
           '     1 NIFIS.LT.0.OR.NANIS.LT.0.OR.NLF.LE.0.OR.NLIN.LE.0.OR.\n'
           '     2 NFUNL.LE.0.OR.NMERG.LE.0) CALL XABORT(\n'
           '     3 "SPOT GLOBAL TYPED: INVALID DECLARED DIMENSIONS.")\n'
           '      IF(.NOT.ALL(IEEE_IS_FINITE(INITIAL_FLUX64))) CALL XABORT(\n'
           '     1 "SPOT GLOBAL TYPED: NON-FINITE REAL64 INITIAL FIELD.")\n'
           '      IF(ANY(KEYFLX.LT.0).OR.ANY(KEYFLX.GT.NUNKNO).OR.\n'
           '     1 ANY(MATCOD.LT.0).OR.ANY(MATCOD.GT.NMAT)) CALL XABORT(\n'
           '     2 "SPOT GLOBAL TYPED: INVALID INPUT SCALAR OR MATERIAL MAP.")\n'
           '      DO IR=1,NREG\n'
           '        IND=KEYFLX(IR,1,1)\n'
           '        IF(MATCOD(IR).GT.0) THEN\n'
           '          IF(IND.LE.0) CALL XABORT(\n'
           '     1     "SPOT GLOBAL TYPED: ACTIVE SCALAR KEY REQUIRED.")\n'
           '          IF(ANY(INITIAL_FLUX64(IND,:).LE.0.0D0)) CALL XABORT(\n'
           '     1     "SPOT GLOBAL TYPED: NONPOSITIVE ACTIVE INITIAL FIELD.")\n'
           '        ENDIF\n'
           '      ENDDO\n'
           '      ALLOCATE(IJJ(0:NMAT),NJJ(0:NMAT),IPOS(0:NMAT),NPSYS(NGRP))\n')
    splice('create full native source output list alongside native flux',
           "           JPFLUX64=LCMLID(IPFLUX,'FLUX64',NGRP)\n",
           "           JPFLUX64=LCMLID(IPFLUX,'FLUX64',NGRP)\n"
           "           JPSOUR64=LCMLID(IPFLUX,'SOUR64',NGRP)\n")
    splice('typed numerical ingress with no REAL32 mirror promotion',
           '      CALL LCMLEL(JPFLUX,1,ILINIT,ITYLCM)\n'
           '      IF(LFORW) THEN\n'
           '         CALL LCMGDL(JPFLUX,IG,GAR32)\n'
           '      ELSE\n'
           '         CALL LCMGDL(JPFLUX,NGRP-IG+1,GAR32)\n'
           '      ENDIF\n'
           '      FLUX(:NUNKNO,IG,2)=DBLE(GAR32(:NUNKNO))\n',
           '*     Only the actual admitted full real64 caller array enters.\n'
           '*     Legacy FLUX type2 remains output compatibility, not ingress.\n'
           '      FLUX(:NUNKNO,IG,2)=INITIAL_FLUX64(:NUNKNO,IG)\n')
    splice('first TYPE-K estimate from complete REAL64 flux with original formula',
           '         ALLOCATE(FLX32(NUNKNO,NGRP))\n'
           '         FLX32(:NUNKNO,:NGRP)=REAL(FLUX(:NUNKNO,:NGRP,2))\n'
           '         CALL FLUKEF(IPRT,IPMACR,NGRP,NREG,NUNKNO,NMAT,NIFIS,NANIS,\n'
           '     1   MATCOD(1),VOL,KEYFLX(1,1,1),XSTRC,XSDIA,XSNUF,XSCHI,NMERG,\n'
           '     2   IMERG,DIFHET,FLX32,B2,ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)\n'
           '         DEALLOCATE(FLX32)\n',
           '         CALL SPOT_FLUKEF_TYPED64(IPRT,IPMACR,NGRP,NREG,NUNKNO,\n'
           '     1   NMAT,NIFIS,NANIS,MATCOD(1),VOL,KEYFLX(1,1,1),XSTRC,\n'
           '     2   XSDIA,XSNUF,XSCHI,NMERG,IMERG,DIFHET,FLUX(1,1,2),B2,\n'
           '     3   ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)\n')
    splice('TYPE2 estimate update keeps complete native REAL64 flux',
           '          ALLOCATE(FLX32(NUNKNO,NGRP))\n'
           '          FLX32(:NUNKNO,:NGRP)=REAL(FLUX(:NUNKNO,:NGRP,3))\n'
           '          CALL FLUKEF(IPRT,IPMACR,NGRP,NREG,NUNKNO,NMAT,NIFIS,NANIS,\n'
           '     1    MATCOD(1),VOL,KEYFLX(1,1,1),XSTRC,XSDIA,XSNUF,XSCHI,NMERG,\n'
           '     2    IMERG,DIFHET,FLX32,B2,ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)\n'
           '          DEALLOCATE(FLX32)\n',
           '          CALL SPOT_FLUKEF_TYPED64(IPRT,IPMACR,NGRP,NREG,NUNKNO,\n'
           '     1    NMAT,NIFIS,NANIS,MATCOD(1),VOL,KEYFLX(1,1,1),XSTRC,\n'
           '     2    XSDIA,XSNUF,XSCHI,NMERG,IMERG,DIFHET,FLUX(1,1,3),B2,\n'
           '     3    ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)\n')
    splice('capture genuine unchanged raw strict SPOT terminal branch',
           '         WRITE(6,1190) ITERF_LAST,MAXINR,EINR_LAST,EPSINR,\n'
           '     1   IGDEB_LAST,IINR_STATE,NGRP\n'
           '         GO TO 410\n',
           '         WRITE(6,1190) ITERF_LAST,MAXINR,EINR_LAST,EPSINR,\n'
           '     1   IGDEB_LAST,IINR_STATE,NGRP\n'
           '*        Capture native variables, never reconstruct rounded logs.\n'
           '         CAPTURED_RESID64=(/EEXT,EUNK_LAST,EINR_LAST/)\n'
           '         IF(.NOT.ALL(IEEE_IS_FINITE(CAPTURED_RESID64)).OR.\n'
           '     1      ANY(CAPTURED_RESID64.LT.0.0D0).OR.\n'
           '     2      .NOT.IEEE_IS_FINITE(AKEFF).OR.AKEFF.LE.0.0D0.OR.\n'
           '     3      IUNK_EVAL.NE.1) CALL XABORT(\n'
           '     4      "SPOT GLOBAL TYPED: INVALID STRICT TERMINAL STATE.")\n'
           '         CAPTURED_KEFF64=AKEFF\n'
           '         CAPTURED_COUNTERS=(/IT,ITERF_LAST/)\n'
           '         CAPTURED_INNER_STATE=IINR_STATE\n'
           '         TERMINAL_GATE_REACHED=.TRUE.\n'
           '         GO TO 410\n')
    splice('validate final real normalized fields before original serialization',
           '*  SAVE THE SOLUTION\n*----\n      DO 510 IG=1,NGRP\n',
           '*  SAVE THE SOLUTION\n*----\n'
           '*     Residuals describe raw Picard acceptance before normalization.\n'
           '*     Returned arrays retain the complete original normalization.\n'
           '      IF(.NOT.TERMINAL_GATE_REACHED) CALL XABORT(\n'
           '     1 "SPOT GLOBAL TYPED: NO STRICT TERMINAL BRANCH.")\n'
           '      IF(.NOT.ALL(IEEE_IS_FINITE(FLUX(:,:,3))).OR.\n'
           '     1   .NOT.ALL(IEEE_IS_FINITE(FLUX(:,:,4)))) CALL XABORT(\n'
           '     2 "SPOT GLOBAL TYPED: NON-FINITE NORMALIZED TERMINAL FIELD.")\n'
           '      IF(.NOT.ALL(IEEE_IS_FINITE(REAL(FLUX(:,:,3),REAL32))).OR.\n'
           '     1   .NOT.ALL(IEEE_IS_FINITE(REAL(FLUX(:,:,4),REAL32))))\n'
           '     2 CALL XABORT("SPOT GLOBAL TYPED: NON-FINITE OUTPUT MIRROR.")\n'
           '      IF(TRANSFER(AKEFF,0_INT64).NE.\n'
           '     1   TRANSFER(CAPTURED_KEFF64,0_INT64)) CALL XABORT(\n'
           '     2 "SPOT GLOBAL TYPED: KEFF CHANGED AFTER STRICT GATE.")\n'
           '      DO IR=1,NREG\n'
           '        IND=KEYFLX(IR,1,1)\n'
           '        IF((MATCOD(IR).GT.0).AND.(IND.GT.0)) THEN\n'
           '          IF(ANY(FLUX(IND,:,3).LE.0.0D0)) CALL XABORT(\n'
           '     1     "SPOT GLOBAL TYPED: NONPOSITIVE TERMINAL SCALAR.")\n'
           '        ENDIF\n'
           '      ENDDO\n'
           '      DO 510 IG=1,NGRP\n')
    splice('serialize all native source groups as true type4 alongside mirrors',
           '      CALL LCMPDL(JPSOUR,IG,NUNKNO,2,GAR32)\n',
           '      CALL LCMPDL(JPSOUR,IG,NUNKNO,2,GAR32)\n'
           '      CALL LCMPDL(JPSOUR64,IG,NUNKNO,4,FLUX(1,IG,4))\n')
    splice('return actual full terminal fields then commit validity last',
           '      CALL SPOT1P64_CACHE_CLEAR()\n'
           '      DEALLOCATE(LEAK1D,XCSOU,DIFHET,DHOM,GAMMA,XSCAT,FLUX,GAR32)\n'
           '      DEALLOCATE(NPSYS,IPOS,NJJ,IJJ)\n'
           '      RETURN\n',
           '      CALL SPOT1P64_CACHE_CLEAR()\n'
           '      TERMINAL_FLUX64=FLUX(:,:,3)\n'
           '      TERMINAL_SOURCE64=FLUX(:,:,4)\n'
           '      TERMINAL_KEFF64=CAPTURED_KEFF64\n'
           '      TERMINAL_RESID64=CAPTURED_RESID64\n'
           '      TERMINAL_COUNTERS=CAPTURED_COUNTERS\n'
           '      TERMINAL_INNER_STATE=CAPTURED_INNER_STATE\n'
           '      DEALLOCATE(LEAK1D,XCSOU,DIFHET,DHOM,GAMMA,XSCAT,FLUX,GAR32)\n'
           '      DEALLOCATE(NPSYS,IPOS,NJJ,IJJ)\n'
           '      TERMINAL_VALID=.TRUE.\n'
           '      RETURN\n')

    # Verify the complete inverse, including the appended SPOT door body.
    reverse = data
    for step in reversed(steps):
        if hashlib.sha256(reverse).hexdigest() != step['after_sha256']:
            raise RuntimeError('inverse step output hash')
        old = step['old'].encode(); new = step['new'].encode()
        if step['mode'] == 'exact_identifier_token_rename':
            pattern = rb'\b' + re.escape(new) + rb'\b'
            if len(re.findall(pattern, reverse)) != step['occurrence_count']:
                raise RuntimeError('inverse exact symbol count')
            reverse = re.sub(pattern, old, reverse)
        else:
            offset = step['byte_offset_in_step_input']
            if reverse[offset:offset + len(new)] != new:
                raise RuntimeError('inverse exact splice body')
            reverse = reverse[:offset] + old + reverse[offset + len(new):]
        if hashlib.sha256(reverse).hexdigest() != step['before_sha256']:
            raise RuntimeError('inverse step input hash')
    if reverse != original:
        raise RuntimeError('complete inverse is not original complete EOF bytes')
    if max(map(len, data.splitlines())) > 132:
        raise RuntimeError('new fixed Source line overflow')
    if data.count(b'      TERMINAL_VALID=.TRUE.') != 1 or b'DBLE(GAR32' in data:
        raise RuntimeError('typed ingress or final validity structural invariant')
    if b'CALL AXMAT_MCCG_DOOR64' in data or b'CALL AXMAT_CONTINUOUS_DRIVER64' in data:
        raise RuntimeError('MCCG driver substituted for SPOT kernel')
    if data.count(b'CALL SPOT_FLUKEF_TYPED64') != 2 or data.count(b'CALL B1HOM64') != original.count(b'CALL B1HOM64'):
        raise RuntimeError('complete TYPE2 and retained TYPE3 callsites')
    # Full interface reuses the independently reviewed complete 47+8 parameter ABI.
    helper_raw, helper_pin = read_pin(REC / 'native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90')
    start = helper_raw.index(b'  interface\n')
    end = helper_raw.index(b'  end interface\n', start) + len(b'  end interface\n')
    interface = helper_raw[start:end].replace(b'AXMAT_CONTINUOUS_DRIVER64', b'SPOT_GLOBAL_TYPED_DRIVER64')
    api = (b'module SPOT_GLOBAL_TYPED_DRIVER_API\n'
           b'  ! Complete typed-driver ABI only; no caller, solve or seal is executed here.\n'
           b'  ! Original TYPE3 B1HOM64 precision boundary remains explicit in the manifest.\n'
           b'  use GANLIB\n'
           b'  use, intrinsic :: iso_fortran_env, only: int32,real32,real64\n'
           b'  implicit none\n  private\n'
           b'  integer, parameter :: kind_guard=1/merge(1,0, &\n'
           b'    kind(1)==int32.and.kind(1.0)==real32.and.kind(0.0d0)==real64.and.dp==real64)\n'
           b'  public :: SPOT_GLOBAL_TYPED_DRIVER64\n' + interface +
           b'end module SPOT_GLOBAL_TYPED_DRIVER_API\n')
    if max(map(len, api.splitlines())) > 132:
        raise RuntimeError('free Source line overflow')
    dependency_paths = [ROOT / 'src/B1HOM64.f90', ROOT / 'src/B1HXS1.f',
                        ROOT / 'src/B1DIF.f', ROOT / 'src/B1SOL.f',
                        ROOT / 'src/SPOF64.f', ROOT / 'src/SPOT1P64.f90',
                        ROOT / 'src/SPOR64_A9.f90', ROOT / 'src/SPOMOC.f90',
                        ROOT / 'Ganlib/src/ganlib.f90', ROOT / 'Ganlib/src/lcmmod.f90',
                        OUT / 'callee_source/SPOT_FLUKEF_TYPED64.f',
                        OUT / 'callee_source/SPOT_FLUKEF_TYPED64_EXACT_FORWARD_INVERSE_PROOF.json',
                        OUT / 'callee_source/SPOT_FLUKEF_TYPED64_SOURCE_PINS_AND_SCOPE.json']
    dependency_pins = [read_pin(path)[1] for path in dependency_paths]
    write_new(OUT / 'ORIGINAL_COMPLETE_FLU2DR64.f', original)
    write_new(DRIVER, data)
    write_new(API, api)
    proof = dict(schema='FULL_ORIGINAL_SPOT_TYPED_DRIVER_LOCAL_TRANSFORM_INVERSE_PROOF_V1',
                 classification='NEW_TYPED_DRIVER_API_ONLY_NOT_WHOLE_CONTINUOUS_TYPE3_CHAIN',
                 original_source_pin=original_pin, steps=steps, local_transform_count=len(steps),
                 candidate_source_sha256=hashlib.sha256(data).hexdigest(),
                 complete_inverse_equals_original_bytes=True,
                 complete_inverse_sha256=hashlib.sha256(reverse).hexdigest(),
                 complete_original_and_appended_SPOT_door_body_preserved_outside_exact_splices=True,
                 candidate_max_line_bytes=max(map(len, data.splitlines())),
                 Fortran_parser_or_compiler_executed=False, transport_executed=False)
    write_json(PROOF, proof)
    protected_after = [read_pin(path)[1] for path in protected_paths]
    if protected_before != protected_after:
        raise RuntimeError('protected original or frozen Source changed')
    manifest = dict(schema='CURRENT_SPOT_GLOBAL_TYPED_DRIVER_SOURCE_AND_PRECISION_BOUNDARY_V1',
                    status='COMPLETE_TYPED_DRIVER_SOURCE_ONLY_TYPE3_CALLEE_GAP_EXPLICIT',
                    original_source_pin=original_pin, driver_pin=read_pin(DRIVER)[1],
                    explicit_API_pin=read_pin(API)[1], inverse_proof_pin=read_pin(PROOF)[1],
                    complete_original_copy_pin=read_pin(OUT / 'ORIGINAL_COMPLETE_FLU2DR64.f')[1],
                    actual_writer_pin=read_pin(Path(__file__).resolve())[1],
                    exact_complete_interface_basis_pin=helper_pin,
                    dependency_Source_and_helper_proof_full_EOF_pins=dependency_pins,
                    protected_Source_before=protected_before, protected_Source_after=protected_after,
                    protected_Source_unchanged=True,
                    entry='SPOT_GLOBAL_TYPED_DRIVER64',
                    private_complete_SPOT_dispatch='SPOT_GLOBAL_FLUSP_TYPED64',
                    ABI_original_arguments=47, ABI_new_typed_arguments=8,
                    dimensions='original dynamic SPOT NUNKNO,NREG,NMAT,NGRP/NIFIS/moments; no MCCG 8/14 fixed shape',
                    preserved_semantics=['SPOT-only TYPE2/3 and forward/no-REBA/B1 SIGS-or-no-leakage original gates.',
                                         'All original epsilon arguments, MAXINR/MAXOUT, scalar/vector group paths, original acceleration cycle and strict raw Picard gate.',
                                         'Complete original appended door: general geometry/maps, SIGS leakage correction, full SPOF64/POD call, no MCCG substitution.',
                                         'Complete original TYPE3 B1HOM64 formula/ABI and current original B1DIF dependency remain unchanged at this first freeze.',
                                         'Final original native flux normalization and serialization, plus SOUR64 true-native carrier and explicit actual terminal outputs.'],
                    actual_first_TYPEK_and_TYPE2_keff_no_flux_demote=True,
                    driver_ingress_from_full_real64_parameter_only=True,
                    residual_scope='Actual accepted raw Picard residuals before original terminal normalization; not a fresh independent-image audit.',
                    header_and_publication='No publication here. Real owning FLUDRV/FLU caller must write complete header/links then admit real direct terminal output; do not call MCCG-only PUBLISH_NATIVE for a SPOT global state.',
                    explicit_unrepaired_precision_boundaries=[
                        {'path':str(ROOT / 'src/B1HOM64.f90'), 'dynamic_roundtrip':'flux32=real(flux(:,:,1)) -> B1HXS2 -> phi -> real64 normalization; B2/DHOM/GAMMA use original real32 interface/storage.', 'required_next_step':'New separate complete B1HOM/B1HXS2/B1DIF native64 dynamic-field graph with original formulas/order/caps and explicit ABI.'},
                        {'path':str(ROOT / 'src/FLU2DR64.f'), 'TYPE3_legacy_feedback':'Original B1HOM64 real32 DIFFHET storage/reload and real32 B2 feed SIGS source correction remain in this driver-only candidate.', 'whole_continuous64_claim':False},
                        {'path':str(ROOT / 'src/SPOF64.f'), 'authority_boundary':'Existing RADIAL-OP64 path and exact legacy mirror test retained; legacy-only RADIAL-OP fallback cannot establish a current dynamic native64 operator lineage.', 'required_runtime_admission':'Future owning caller/host must require admitted RADIAL-OP64 as applicable; no static Source-only qualification.'}],
                    external_full_EOF_Source_input_context_runtime_and_output_binding_still_required=True,
                    actual_caller_dispatcher_deck_not_installed=True,
                    original_resource_limits_not_changed={'whole_seconds':1800,'stage_seconds':600,'SELF_and_child_RSS_MiB':512,'threads':1,'active_business_children':1,'retries':0},
                    full_TYPE3_continuous64_qualified=False, native_global_producer_qualified=False,
                    Fortran_parser_or_compiler_executed=False, transport_executed=False,
                    original_seventeen_controls_qualified=False, online_BOOT_qualified=False,
                    whole_INPUT_admitted=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False,
                    actual_Source_writer_wall_seconds=time.monotonic()-started)
    write_json(MANIFEST, manifest)
    print(json.dumps(dict(status=manifest['status'], driver_pin=manifest['driver_pin'],
                          API_pin=manifest['explicit_API_pin'], manifest_pin=read_pin(MANIFEST)[1],
                          actual_local_transform_count=len(steps), actual_full_original_byte_inverse=True,
                          Fortran_compiler_or_transport_executed=False)))


if __name__ == '__main__':
    main()
