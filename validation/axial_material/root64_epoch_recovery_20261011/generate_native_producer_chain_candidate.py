"""Source-only exact derivation of a complete continuous native driver.

Only stdlib byte reads/writes, full-EOF pins and exact inverse proofs.
No compiler, parser, Native transport, numeric library or process spawn.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import resource
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
OUT=REC/'native_producer_chain_source'
START=time.monotonic()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def fullpin(path, retain=True):
    before=identity(path.lstat())
    digest=hashlib.sha256()
    blocks=[]
    length=0
    with path.open('rb') as stream:
        opened=identity(os.fstat(stream.fileno()))
        while True:
            block=stream.read(1048576)
            if not block:
                break
            digest.update(block)
            length+=len(block)
            if retain:
                blocks.append(block)
        eof=identity(os.fstat(stream.fileno()))
    after=identity(path.lstat())
    assert before==opened==eof==after, str(path)
    assert length==after[4], str(path)
    return (b''.join(blocks) if retain else None),dict(
        path=str(path),size_bytes=length,sha256=digest.hexdigest(),identity=after,
        before_open_EOF_after_identity_equal=True,read_scope='complete EOF')

original_path=ROOT/'validation/artifacts/axial-material-r64-system-normalization-20261003/build/AXMAT_SNAPSHOT_DRIVER64.f'
original,original_pin=fullpin(original_path)
assert original_pin['sha256']=='ab98848880334ce3b3b680261a40dd4841ca02cb8588bc5e7da649e223bcc46e'
protected=[ROOT/'src/FLU.f',ROOT/'src/FLUDRV.f',ROOT/'src/FLU2DR64.f',
    REC/'new_source/SPOR64_BOOT64.f90',REC/'new_source/SPOBOOT64.f90',
    REC/'continuous_chain_source/SPOSTATE64.f90',REC/'projection_chain_source/SPOPROJ64.f90']
protected_before={str(p):fullpin(p)[1] for p in protected}
dependencies=[ROOT/'Ganlib/src/ganlib.f90',ROOT/'Ganlib/src/lcmmod.f90',
    ROOT/'src/SPOR64_RCONTRACT.f90',ROOT/'src/SPOR64_VERIFY.f90',ROOT/'src/SPOR64_A9.f90',
    ROOT/'validation/artifacts/axial-material-r64-snapshot-A-20261003/build/AXMAT_FLUKEF64.f',
    ROOT/'validation/artifacts/axial-material-r64-snapshot-A-20261003/build/snapshot_r64_door.f90',
    ROOT/'validation/artifacts/axial-material-r64-system-normalization-20261003/build/snapshot_r64_balance.f90',
    ROOT/'validation/artifacts/axial-material-r64-system-normalization-20261003/build/SPOR64_A8.f90',
    ROOT/'validation/artifacts/axial-material-r64-system-normalization-20261003/build/MCGFST.f',
    ROOT/'validation/artifacts/axial-material-r64-system-normalization-20261003/build/MCGDSCA.f']
dependency_pins=[fullpin(p)[1] for p in dependencies]
source=original.decode('utf8')
steps=[]

def replace_once(label,old,new):
    global source
    assert source.count(old)==1, label
    before=source.encode('utf8')
    position=before.index(old.encode('utf8'))
    source=source.replace(old,new,1)
    after=source.encode('utf8')
    assert after[:position]==before[:position], label
    assert after[position+len(new.encode('utf8')):]==before[position+len(old.encode('utf8')):],label
    steps.append(dict(label=label,mode='one_exact_local_byte_splice',
        byte_offset_in_step_input=position,old=old,new=new,old_bytes=len(old.encode('utf8')),
        new_bytes=len(new.encode('utf8')),before_sha256=sha(before),after_sha256=sha(after),
        outside_splice_exact_bytes_equal=True))

def rename_token(label,old,new):
    global source
    assert new not in source,label
    before=source.encode('utf8')
    pattern=r'\b'+re.escape(old)+r'\b'
    count=len(re.findall(pattern,source))
    assert count,label
    source=re.sub(pattern,new,source)
    steps.append(dict(label=label,mode='exact_identifier_token_rename',old=old,new=new,
        occurrence_count=count,before_sha256=sha(before),after_sha256=sha(source.encode('utf8'))))

rename_token('new entry name, old kernel is preserved in full','AXMAT_SNAPSHOT_DRIVER64','AXMAT_CONTINUOUS_DRIVER64')
replace_once('honest new ABI and proof scope header','*DECK FLU2DR64\n',
'''*DECK AXMAT_CONTINUOUS_DRIVER64
*     NEW SOURCE, complete retained native kernel with new typed ABI.
*     No recovery of missing historical Source bytes or qualification.
*     INITIAL_FLUX64 is a full real64 caller array from exact type4 data.
*     Terminal outputs remain invalid until normal strict completion.
*     No GLOBAL64, QFISS/epoch bootstrap, deck or dispatcher is added here.
''')
replace_once('append explicit native input and terminal output ABI',
    '     4 KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG)\n',
'''     4 KEYFLX,VOL,XSTRC,XSDIA,XSNUF,XSCHI,LREBAL,INITFL,NMERG,IMERG,
     5 INITIAL_FLUX64,TERMINAL_FLUX64,TERMINAL_SOURCE64,TERMINAL_KEFF64,
     6 TERMINAL_RESID64,TERMINAL_COUNTERS,TERMINAL_INNER_STATE,
     7 TERMINAL_VALID)
''')
replace_once('explicit real/integer kind and finite guards','      USE GANLIB\n',
'''      USE GANLIB
      USE, INTRINSIC :: ISO_FORTRAN_ENV, ONLY: INT32,INT64,REAL32,
     1 REAL64
      USE, INTRINSIC :: IEEE_ARITHMETIC, ONLY: IEEE_IS_FINITE
''')
replace_once('typed ABI declarations and internal strict-branch capture',
    '      DOUBLE PRECISION REFKEF\n',
'''      DOUBLE PRECISION REFKEF
      DOUBLE PRECISION, INTENT(IN) :: INITIAL_FLUX64(NUNKNO,NGRP)
      DOUBLE PRECISION, INTENT(OUT) ::
     1 TERMINAL_FLUX64(NUNKNO,NGRP),TERMINAL_SOURCE64(NUNKNO,NGRP),
     2 TERMINAL_KEFF64,TERMINAL_RESID64(3)
      INTEGER, INTENT(OUT) :: TERMINAL_COUNTERS(2),
     1 TERMINAL_INNER_STATE
      LOGICAL, INTENT(OUT) :: TERMINAL_VALID
      DOUBLE PRECISION CAPTURED_KEFF64,CAPTURED_RESID64(3)
      INTEGER CAPTURED_COUNTERS(2),CAPTURED_INNER_STATE
      LOGICAL TERMINAL_GATE_REACHED
      INTEGER, PARAMETER :: KIND_GUARD=1/MERGE(1,0,
     1 KIND(1).EQ.INT32.AND.KIND(1.0).EQ.REAL32.AND.
     2 KIND(0.0D0).EQ.REAL64.AND.DP.EQ.REAL64)
''')
replace_once('every invocation starts with cleared invalid terminal outputs',
    '      ALLOCATE(IJJ(0:NMAT),NJJ(0:NMAT),IPOS(0:NMAT),NPSYS(NGRP))\n',
'''*     Output validity is independent from any previous caller image.
      TERMINAL_VALID=.FALSE.
      TERMINAL_FLUX64=0.0D0
      TERMINAL_SOURCE64=0.0D0
      TERMINAL_KEFF64=0.0D0
      TERMINAL_RESID64=0.0D0
      TERMINAL_COUNTERS=0
      TERMINAL_INNER_STATE=0
      TERMINAL_GATE_REACHED=.FALSE.
      CAPTURED_KEFF64=0.0D0
      CAPTURED_RESID64=0.0D0
      CAPTURED_COUNTERS=0
      CAPTURED_INNER_STATE=0
*     Check the same declared original shape before scalar-map indexing.
      IF(NREG.NE.8.OR.NUNKNO.NE.14.OR.NMAT.NE.8.OR.NGRP.NE.370.OR.
     1   NIFIS.NE.32.OR.NLF.NE.1.OR.NLIN.NE.1.OR.NFUNL.NE.1)
     2 CALL XABORT('AXMAT CONTINUOUS: UNDECLARED INITIAL SHAPE.')
      IF(.NOT.ALL(IEEE_IS_FINITE(INITIAL_FLUX64))) CALL XABORT(
     1 'AXMAT CONTINUOUS: NON-FINITE REAL64 INITIAL FIELD.')
      IF(INITFL.NE.1) CALL XABORT(
     1 'AXMAT CONTINUOUS: EXPLICIT REAL64 WARM INITIAL FIELD REQUIRED.')
      IF(ANY(KEYFLX.LT.0).OR.ANY(KEYFLX.GT.NUNKNO)) CALL XABORT(
     1 'AXMAT CONTINUOUS: INVALID INITIAL SCALAR MAP.')
      DO IR=1,NREG
        IND=KEYFLX(IR,1,1)
        IF((MATCOD(IR).GT.0).AND.(IND.GT.0)) THEN
          IF(ANY(INITIAL_FLUX64(IND,:).LE.0.0D0)) CALL XABORT(
     1     'AXMAT CONTINUOUS: NONPOSITIVE ACTIVE REAL64 INITIAL FIELD.')
        ENDIF
      ENDDO
      ALLOCATE(IJJ(0:NMAT),NJJ(0:NMAT),IPOS(0:NMAT),NPSYS(NGRP))
''')
replace_once('remove the reachable REAL32 flux promotion at warm ingress',
'''      CALL LCMLEL(JPFLUX,1,ILINIT,ITYLCM)
      IF(LFORW) THEN
         CALL LCMGDL(JPFLUX,IG,GAR32)
      ELSE
         CALL LCMGDL(JPFLUX,NGRP-IG+1,GAR32)
      ENDIF
      FLUX(:NUNKNO,IG,2)=DBLE(GAR32(:NUNKNO))
''',
'''*     Numerical ingress is only the complete true real64 caller array.
*     GAR32 is reserved for legacy mirrors at the terminal output.
      FLUX(:NUNKNO,IG,2)=INITIAL_FLUX64(:NUNKNO,IG)
''')
replace_once('capture the real unmodified strict terminal branch',
'''         WRITE(6,1190) ITERF_LAST,MAXINR,EINR_LAST,EPSINR,
     1   IGDEB_LAST,IINR_STATE,NGRP
         GO TO 410
''',
'''         WRITE(6,1190) ITERF_LAST,MAXINR,EINR_LAST,EPSINR,
     1   IGDEB_LAST,IINR_STATE,NGRP
*        Capture actual kernel values, not rounded log reconstructions.
         CAPTURED_RESID64=(/EEXT,EUNK_LAST,EINR_LAST/)
         IF(.NOT.ALL(IEEE_IS_FINITE(CAPTURED_RESID64)).OR.
     1      ANY(CAPTURED_RESID64.LT.0.0D0).OR.
     2      .NOT.IEEE_IS_FINITE(AKEFF).OR.AKEFF.LE.0.0D0.OR.
     3      IUNK_EVAL.NE.1) CALL XABORT(
     4      'AXMAT CONTINUOUS: INVALID STRICT TERMINAL STATE.')
         CAPTURED_KEFF64=AKEFF
         CAPTURED_COUNTERS=(/IT,ITERF_LAST/)
         CAPTURED_INNER_STATE=IINR_STATE
         TERMINAL_GATE_REACHED=.TRUE.
         GO TO 410
''')
replace_once('validate the final actual normalized image before serialization',
'''*  SAVE THE SOLUTION
*----
      DO 510 IG=1,NGRP
''',
'''*  SAVE THE SOLUTION
*----
*     Raw terminal residuals above refer to the accepted Picard image.
*     The full output below includes the unchanged final normalization.
      IF(.NOT.TERMINAL_GATE_REACHED) CALL XABORT(
     1 'AXMAT CONTINUOUS: NO STRICT TERMINAL BRANCH.')
      IF(.NOT.ALL(IEEE_IS_FINITE(FLUX(:,:,3))).OR.
     1   .NOT.ALL(IEEE_IS_FINITE(FLUX(:,:,4)))) CALL XABORT(
     2 'AXMAT CONTINUOUS: NON-FINITE NORMALIZED TERMINAL FIELD.')
      IF(.NOT.ALL(IEEE_IS_FINITE(REAL(FLUX(:,:,3),REAL32))).OR.
     1   .NOT.ALL(IEEE_IS_FINITE(REAL(FLUX(:,:,4),REAL32))))
     2 CALL XABORT('AXMAT CONTINUOUS: NON-FINITE TERMINAL MIRROR.')
      IF(TRANSFER(AKEFF,0_INT64).NE.
     1   TRANSFER(CAPTURED_KEFF64,0_INT64)) CALL XABORT(
     2 'AXMAT CONTINUOUS: TERMINAL KEFF CHANGED AFTER STRICT GATE.')
      DO IR=1,NREG
        IND=KEYFLX(IR,1,1)
        IF((MATCOD(IR).GT.0).AND.(IND.GT.0)) THEN
          IF(ANY(FLUX(IND,:,3).LE.0.0D0)) CALL XABORT(
     1     'AXMAT CONTINUOUS: NONPOSITIVE NORMALIZED SCALAR FIELD.')
        ENDIF
      ENDDO
      DO 510 IG=1,NGRP
''')
replace_once('return complete true terminal arrays and commit validity last',
'''      CALL SPOT1P64_CACHE_CLEAR()
      DEALLOCATE(LEAK1D,XCSOU,DIFHET,DHOM,GAMMA,XSCAT,FLUX,GAR32)
      DEALLOCATE(NPSYS,IPOS,NJJ,IJJ)
      RETURN
''',
'''      CALL SPOT1P64_CACHE_CLEAR()
*     All original terminal records are saved before output validity.
      TERMINAL_FLUX64=FLUX(:,:,3)
      TERMINAL_SOURCE64=FLUX(:,:,4)
      TERMINAL_KEFF64=CAPTURED_KEFF64
      TERMINAL_RESID64=CAPTURED_RESID64
      TERMINAL_COUNTERS=CAPTURED_COUNTERS
      TERMINAL_INNER_STATE=CAPTURED_INNER_STATE
      DEALLOCATE(LEAK1D,XCSOU,DIFHET,DHOM,GAMMA,XSCAT,FLUX,GAR32)
      DEALLOCATE(NPSYS,IPOS,NJJ,IJJ)
      TERMINAL_VALID=.TRUE.
      RETURN
''')

candidate=source.encode('utf8')
assert b'DBLE(GAR32' not in candidate
assert b'CALL AXMAT_FLUKEF64' in candidate
assert source.count('TERMINAL_VALID=.TRUE.')==1
assert max(map(len,candidate.splitlines()))<=132
inverse=source
for step in reversed(steps):
    assert sha(inverse.encode('utf8'))==step['after_sha256'],step['label']
    if step['mode']=='one_exact_local_byte_splice':
        raw=inverse.encode('utf8')
        pos=step['byte_offset_in_step_input']
        new=step['new'].encode('utf8')
        assert raw[pos:pos+len(new)]==new,step['label']
        inverse=(raw[:pos]+step['old'].encode('utf8')+raw[pos+len(new):]).decode('utf8')
    else:
        inverse=re.sub(r'\b'+re.escape(step['new'])+r'\b',step['old'],inverse)
    assert sha(inverse.encode('utf8'))==step['before_sha256'],step['label']
assert inverse.encode('utf8')==original

OUT.mkdir(exist_ok=True)
(OUT/'read_only_original').mkdir(exist_ok=True)
(OUT/'read_only_original/AXMAT_SNAPSHOT_DRIVER64.f').write_bytes(original)
(OUT/'AXMAT_CONTINUOUS_DRIVER64.f').write_bytes(candidate)
proof=dict(classification='NEW_COMPLETE_SOURCE_EXACT_LOCAL_TRANSFORM_BYTE_INVERSE_PROOF_ONLY',
    original_source_pin=original_pin,local_transform_count=len(steps),steps=steps,
    complete_inverse_equals_original_bytes=True,complete_inverse_sha256=sha(inverse.encode('utf8')),
    candidate_source_sha256=sha(candidate),candidate_max_line_length=max(map(len,candidate.splitlines())),
    compiler_or_parser_executed=False,Native_or_numeric_executed=False)
(OUT/'AXMAT_CONTINUOUS_DRIVER64_EXACT_TRANSFORM_INVERSE_PROOF.json').write_text(
    json.dumps(proof,indent=2)+'\n',encoding='utf8')

receipt_path=ROOT/'validation/artifacts/axial-material-qualified-AB-admission-v2-20261004/producer_ingestion_receipt.json'
receipt_data,receipt_pin=fullpin(receipt_path)
old_receipt=json.loads(receipt_data)
seed_pins=[]
for name in ('A','B'):
    old=old_receipt['states'][name]['archive']
    _,current=fullpin(Path(old['path']),retain=False)
    assert current['sha256']==old['sha256'],name
    seed_pins.append(dict(state=name,current_complete_EOF_pin=current,
        original_archive_expected_sha256=old['sha256'],
        original_SHA_equal_current=True,selected_for_first_new_warm_case=(name=='A'),
        source_load_path='archive FLUX item 1 -> complete L_FLUX FLUX64 type10/370 each type4/14',
        old_payload_FLUX64_sha256=old_receipt['states'][name]['payload_audit']['payload_sha256']['FLUX64'],
        current_logical_payload_read_executed=False,
        inheritance_of_old_seed_or_wholeInput_qualification=False))
selected_context_pins=[]
for field in ('material','track'):
    item=old_receipt['states']['A'][field]
    _,pin=fullpin(Path(item['path']),retain=False)
    assert pin['sha256']==item['sha256'],field
    selected_context_pins.append(dict(field=field,current_complete_EOF_pin=pin,
        original_expected_sha256=item['sha256'],original_SHA_equal_current=True))
geometry=ROOT/'validation/artifacts/axial-material-inputs-20261003/A/geometry.dat'
_,geometry_pin=fullpin(geometry)
assert geometry_pin['sha256']=='d70e7308937e157ccaea03426cf02187827166be80d7806757e9f212729317ec'
selected_context_pins.append(dict(field='geometry',current_complete_EOF_pin=geometry_pin))

helper_data,helper_pin=fullpin(OUT/'AXMAT_NATIVE_PRODUCER_CHAIN.f90')
assert max(map(len,helper_data.splitlines()))<=132
candidate_pin=fullpin(OUT/'AXMAT_CONTINUOUS_DRIVER64.f')[1]
protected_after={str(p):fullpin(p)[1] for p in protected}
assert protected_before==protected_after
manifest=dict(classification='NEW_NATIVE_PRODUCER_SOURCE_ONLY_NOT_COMPILED_OR_RUN',
    candidate_source=candidate_pin,typed_caller_helper=helper_pin,original_source=original_pin,
    exact_full_original_copy=fullpin(OUT/'read_only_original/AXMAT_SNAPSHOT_DRIVER64.f')[1],
    transform_inverse_proof=fullpin(OUT/'AXMAT_CONTINUOUS_DRIVER64_EXACT_TRANSFORM_INVERSE_PROOF.json')[1],
    generator=fullpin(Path(__file__))[1],dependency_sources=dependency_pins,
    protected_Source_before=protected_before,protected_Source_after=protected_after,
    protected_Source_fullpins_unchanged=True,seed_original_ingestion_receipt=receipt_pin,
    actual_current_seed_full_EOF_audit=seed_pins,selected_A_context_full_EOF_pins=selected_context_pins,
    first_new_case=dict(name='ROOT64_NEW_WARM_A_20261011',role='new explicitly declared warm experiment',
        numerical_ingress='actual archived FLUX64, no GAR32 promotion; helper full370 exactpair read still to be run',
        same_temperature_and_A_material=True,initial_flag='INITFL=1',
        cold_init_equivalence_claim=False,old_seed_or_wholeInput_qualification_inherited=False,
        actual_retained_MCCG_EPSI=2.5e-8,original_outer_eps_all=2.5e-7,
        original_AXMAT_THER64=2.5e-9,original_AXMAT_EPS64=2.5e-10,
        current_material_track_system_ROUTE_bindings_must_be_independently_admitted=True),
    missing_integration=['actual FLUDRV/FLU new route call','full caller context and seed preflight',
        'bounded compiler and exact Native producer execution','external immutable output SHA/7ID seal',
        'GLOBAL64 projection/source bootstrap epoch lifecycle','full actual controls and original scientific qualification'],
    inherited_old_physical_rank_resource_or_accuracy_PASS=False,
    compiler_or_parser_executed=False,Native_or_numeric_executed=False,
    own_elapsed_seconds=time.monotonic()-START,own_peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
(OUT/'NATIVE_PRODUCER_SOURCE_PINS_SEED_AUDIT_AND_SCOPE.json').write_text(
    json.dumps(manifest,indent=2)+'\n',encoding='utf8')
print(json.dumps(dict(candidate_source=candidate_pin,typed_caller_helper=helper_pin,
    exact_complete_inverse_verified=True,local_transform_count=len(steps),
    seed_A_B_actual_complete_EOF_SHA_equal_original_expected=True,
    protected_Source_fullpins_unchanged=True,compiler_or_parser_executed=False,Native_or_numeric_executed=False,
    own_elapsed_seconds=time.monotonic()-START,own_peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)))
