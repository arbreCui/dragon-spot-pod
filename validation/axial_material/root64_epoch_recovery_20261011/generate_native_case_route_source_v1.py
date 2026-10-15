"""Write a complete isolated native warm-A route; no compilation or process spawn."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import resource
import shlex
import struct
import time

ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
ART=ROOT/'validation/artifacts'
OUT=REC/'native_case_route_source_v1'
RUN=ART/'axial-material-new-REAL64-native-warm-A-20261011'
BUILD=RUN/'build'
START=time.monotonic()
COMPILER=Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
FLAGS=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none']

def digest(data): return hashlib.sha256(data).hexdigest()

def ident(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def pin(path):
    path=Path(path)
    before=ident(path.stat())
    with path.open('rb') as f:
        opened=ident(os.fstat(f.fileno()))
        sha=hashlib.file_digest(f,'sha256').hexdigest()
        eof=ident(os.fstat(f.fileno()))
    after=ident(path.stat())
    if before!=opened or before!=eof or before!=after:
        raise RuntimeError('input identity changed: '+str(path))
    return dict(path=str(path),sha256=sha,size_bytes=before[4],identity=before,
                full_EOF_before_open_after_stable=True)

def save(name,data):
    data=data.encode() if isinstance(data,str) else data
    p=OUT/name
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    return pin(p)

def js(name,data): return save(name,json.dumps(data,ensure_ascii=False,indent=2)+'\n')

protected_paths=[ROOT/'src/KDRDRV.F',ROOT/'src/FLU.f',ROOT/'src/FLUDRV.f',
    REC/'native_producer_chain_source/AXMAT_CONTINUOUS_DRIVER64.f',
    REC/'native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90',
    REC/'native_producer_chain_source/caller_candidate_v1/FLUDRVN64.f',
    REC/'native_producer_chain_source/caller_candidate_v1/FLUNAT64.f',
    REC/'native_producer_chain_source/caller_candidate_v1/AXMAT_NATIVE_CALLER_API.f90',
    REC/'new_source/SPOR64_BOOT64.f90',REC/'new_source/SPOBOOT64.f90']
protected_before=[pin(p) for p in protected_paths]
if OUT.exists() or OUT.is_symlink(): raise RuntimeError('fresh route directory required')
OUT.mkdir()
original=(ROOT/'src/KDRDRV.F').read_bytes()
old=b"      ELSE IF(HMODUL.EQ.'FLU:') THEN\n         CALL FLU(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
new=b"      ELSE IF(HMODUL.EQ.'AXNCASE64:') THEN\n         CALL AXNCASE64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n      ELSE IF(HMODUL.EQ.'FLUNAT64:') THEN\n         CALL FLUNAT64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"+old
if original.count(old)!=1: raise RuntimeError('exact original dispatcher splice')
offset=original.index(old)
candidate=original.replace(old,new,1)
if candidate.replace(new,old,1)!=original: raise RuntimeError('full dispatcher inverse')
if candidate[:offset]!=original[:offset] or candidate[offset+len(new):]!=original[offset+len(old):]:
    raise RuntimeError('nonlocal dispatcher changes')
source_pins=[save('KDRDRV.F',candidate)]
original_copy=save('read_only_original/KDRDRV.F',original)
proof=js('KDRDRV_EXACT_LOCAL_BYTE_INVERSE_PROOF.json',dict(
    schema='EXACT_COMPLETE_ORIGINAL_DISPATCHER_LOCAL_INVERSE_V1',
    original=protected_before[0],retained_complete_original=original_copy,
    candidate=source_pins[0],changes=[dict(offset=offset,old=old.decode(),new=new.decode(),
    outside_splice_bytes_equal=True)],complete_inverse_sha256=digest(original),
    complete_inverse_bytes_equal_original=True,preprocessor_suffix='.F',
    original_HDF5_LIB_condition_bytes_preserved=True,compiler_defines=[],
    original_nine_numeric_flags=FLAGS,compiled=False))

builder='''! NEW SOURCE: independent constants for ROOT64_NEW_WARM_A_20261011.
! Creates case operands only. It never certifies a solve or an epoch closure.
subroutine AXNCASE64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: int32,real32
  use SPOR64_VERIFY, only: EMPTY_MEMORY_ROOT,EXACT_INVENTORY, &
      CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  character(len=12), parameter :: names(2)=['RCONTRACT   ','BOOT_BIND   ']
  character(len=12), parameter :: route_names(6)= &
      ['SIGNATURE   ','CASE-NAME   ','EPS-TERMINAL','FLU-CAPS    ', &
       'FLU-ACCE    ','FLU-OPTION  ']
  character(len=12), parameter :: bind_names(3)= &
      ['SIGNATURE   ','PLANE       ','EPOCH       ']
  character(len=12), parameter :: case12='R64WARM-A-V1 '
  real(real32), parameter :: eps(3)=[2.5e-7_real32,5.0e-8_real32,2.5e-8_real32]
  integer, parameter :: caps(2)=[500,740],acce(2)=[3,3],plane=1,epoch=0
  type(SPOR64_ROUTE_CONTRACT) :: contract
  logical :: loaded
  integer :: i,token_type,token_integer,read_plane,read_epoch
  real :: token_real
  double precision :: token_double
  character(len=4) :: token_text
  if(nentry/=2) call XABORT('AXNCASE64: TWO FRESH CASE OUTPUTS REQUIRED.')
  if(any(hentry/=names).or.any(ientry/=1).or.any(jentry/=0)) &
      call XABORT('AXNCASE64: EXACT FRESH MEMORY OUTPUT ORDER REQUIRED.')
  do i=1,2
    if(.not.c_associated(kentry(i))) call XABORT('AXNCASE64: NULL OUTPUT.')
    if(.not.EMPTY_MEMORY_ROOT(kentry(i))) call XABORT('AXNCASE64: OUTPUT NOT EMPTY.')
  enddo
  if(c_associated(kentry(1),kentry(2))) call XABORT('AXNCASE64: OUTPUT ALIAS.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('AXNCASE64: ONLY THE DECLARED CASE IS ALLOWED.')
  ! Same mandatory LCM ABI as the retained independent RCONTRACT builder.
  call LCMPTC(kentry(1),'SIGNATURE',12,'L_RCONTRACT ')
  call LCMPTC(kentry(1),'CASE-NAME',12,case12)
  call LCMPUT(kentry(1),'EPS-TERMINAL',3,2,eps)
  call LCMPUT(kentry(1),'FLU-CAPS',2,1,caps)
  call LCMPUT(kentry(1),'FLU-ACCE',2,1,acce)
  call LCMPTC(kentry(1),'FLU-OPTION',4,'B0  ')
  call LCMPTC(kentry(2),'SIGNATURE',12,'L_BOOTBIND ')
  call LCMPUT(kentry(2),'PLANE',1,1,plane)
  call LCMPUT(kentry(2),'EPOCH',1,1,epoch)
  ! Structural/bit checks prove only the case declaration was constructed.
  call SPOR64_RCONTRACT_LOAD(kentry(1),contract,loaded)
  if(.not.loaded) call XABORT('AXNCASE64: DECLARATION LOAD REFUSED.')
  if(.not.EXACT_INVENTORY(kentry(1),route_names).or. &
      .not.EXACT_INVENTORY(kentry(2),bind_names)) &
      call XABORT('AXNCASE64: INCOMPLETE DECLARATION INVENTORY.')
  if(contract%case_name/=case12.or. &
      contract%eps_radial_bits/=transfer(eps(1),0_int32).or. &
      contract%eps_axial_bits/=transfer(eps(2),0_int32).or. &
      contract%eps_mccg_bits/=transfer(eps(3),0_int32).or. &
      contract%flu_maxout/=caps(1).or.contract%flu_maxinr/=caps(2).or. &
      contract%flu_acce_free/=acce(1).or.contract%flu_acce_accel/=acce(2).or. &
      contract%flu_option/='B0  ') call XABORT('AXNCASE64: CASE BITS MISMATCH.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(2),'SIGNATURE',3,12,'L_BOOTBIND').or. &
      .not.RECORD_MATCHES(kentry(2),'PLANE',1,1).or. &
      .not.RECORD_MATCHES(kentry(2),'EPOCH',1,1)) &
      call XABORT('AXNCASE64: BINDING TYPE/SHAPE MISMATCH.')
  call LCMGET(kentry(2),'PLANE',read_plane)
  call LCMGET(kentry(2),'EPOCH',read_epoch)
  if(read_plane/=plane.or.read_epoch/=epoch) call XABORT('AXNCASE64: BINDING BITS MISMATCH.')
end subroutine AXNCASE64
'''
if any(len(x)>132 for x in builder.splitlines()): raise RuntimeError('builder line length')
source_pins.append(save('AXNCASE64.f90',builder))
deck_path=ART/'axial-material-r64-system-normalization-20261003/A/snapshot.x2m'
deck=deck_path.read_text()
deck_steps=[]
def deck_replace(label,old,new):
    global deck
    if deck.count(old)!=1: raise RuntimeError('exact deck splice '+label)
    deck_steps.append(dict(label=label,old=old,new=new))
    deck=deck.replace(old,new,1)
deck_replace('explicit new case provenance','* Fresh TYPE-K snapshot from this state\'s separately sealed TONE material.\n',
    '* NEW CASE ROOT64_NEW_WARM_A_20261011; LCM CASE-NAME R64WARM-A-V1.\n'
    '* True native REAL64 warm guess from the independently bit-checked A archive.\n'
    '* Full A material/geometry/track and original controls are retained.\n'
    '* Plane 1 / epoch 0 is an input binding, not GLOBAL or CLOSED qualification.\n')
deck_replace('true native warm archive','XSM_FILE SEED_IN :: FILE \'./seed_A.xsm\' ;',
    "XSM_FILE SEED_IN :: FILE './snapshot_A.xsm' ;")
deck_replace('new owned output','XSM_FILE SNAP_OUT :: FILE \'./snapshot_A.xsm\' ;',
    "XSM_FILE SNAP_OUT :: FILE './new_native_A.xsm' ;")
deck_replace('independent case operands','LINKED_LIST MICROLIB2 MACRO TRACK SYSTEM FLUX SNAP SEEDSET ;',
    'LINKED_LIST MICROLIB2 MACRO TRACK SYSTEM FLUX SNAP SEEDSET\n  RCONTRACT BOOT_BIND ;')
deck_replace('actual new entry declaration','MODULE RECOVER: SALT: MCCGT: ASM: FLU: GREP: BACKUP: ABORT: END: ;',
    'MODULE RECOVER: SALT: MCCGT: ASM: FLUNAT64: AXNCASE64:\n  GREP: BACKUP: ABORT: END: ;')
deck_replace('strict independent case creation','FLUX := RECOVER: SEEDSET :: ITEM 1 ;\n',
    'FLUX := RECOVER: SEEDSET :: ITEM 1 ;\n'
    'RCONTRACT BOOT_BIND := AXNCASE64: :: ;\n')
deck_replace('actual native caller','FLUX := FLU: FLUX SYSTEM MICROLIB2 TRACK TRACK_f ::',
    'FLUX := FLUNAT64: FLUX SYSTEM MICROLIB2 TRACK TRACK_f\n  RCONTRACT BOOT_BIND ::')
deck_replace('save complete independent operands','SNAP_OUT := SNAP ;\n',
    'SNAP := BACKUP: SNAP RCONTRACT BOOT_BIND :: ITEM 1 ;\nSNAP_OUT := SNAP ;\n')
deck_replace('honest new completion marker','AXMAT-SNAPSHOT-A-COMPLETE',
    'ROOT64-NEW-WARM-A-NATIVE-COMPLETE')
inverse=deck
for step in reversed(deck_steps): inverse=inverse.replace(step['new'],step['old'],1)
if inverse.encode()!=deck_path.read_bytes(): raise RuntimeError('complete deck inverse')
deck_pin=save('ROOT64_NEW_WARM_A_20261011.x2m',deck)
deck_orig=save('read_only_original/snapshot_A.x2m',deck_path.read_bytes())
deck_proof=js('NEW_WARM_A_DECK_EXACT_ORIGINAL_INVERSE_PROOF.json',dict(
    original=pin(deck_path),retained_complete_original=deck_orig,candidate=deck_pin,
    changes=deck_steps,complete_original_bytes_recovered=True,
    physical_SALT_MCCGT_ASM_and_FLU_controls_bytes_unchanged=True,
    native_execution=False))

system=ART/'axial-material-r64-system-normalization-20261003'
snapshot=ART/'axial-material-r64-snapshot-A-20261003'
boot=ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/build'
prod=ART/'axial-material-new-REAL64-producer-compile-only-20261011/build'
caller=ART/'axial-material-new-REAL64-caller-compile-only-20261011/build'
includes=[BUILD,caller,prod,boot,system/'build',ROOT/'lib/Darwin_arm64/modules',ROOT/'Ganlib/lib/Darwin_arm64/modules']
# Actual numerical implementation Sources, explicitly rebuilt in this new route.
# Other standard operators remain supplied by separately pinned old archives.
support_sources=[ROOT/'src/SPOR64_A8_ACA.f90',system/'build/SPOR64_A8.f90',
    ROOT/'src/SPOR64_A9.f90',snapshot/'build/AXMAT_FLUKEF64.f',
    snapshot/'build/snapshot_r64_door.f90',system/'build/snapshot_r64_balance.f90',
    system/'build/MCGDSCA.f',system/'build/MCGFST.f',system/'build/MCGASM.f',
    ROOT/'src/MCGFFIR64_RANK_ADAPTER.f90',ROOT/'src/MCGFFIR.f',
    ROOT/'src/FLUGPI.f',ROOT/'src/DRAGON.f90']
route_sources=[OUT/'AXNCASE64.f90',OUT/'KDRDRV.F']
compile_sources=support_sources+route_sources
commands=[[str(COMPILER),*FLAGS,*['-I'+str(p) for p in includes],'-J'+str(BUILD),
           '-c',str(p),'-o',str(BUILD/(p.stem+'.o'))] for p in compile_sources]
fresh_objects=[BUILD/(p.stem+'.o') for p in compile_sources]
existing_objects=[caller/'AXMAT_NATIVE_CALLER_API.o',caller/'FLUDRVN64.o',caller/'FLUNAT64.o',
    prod/'AXMAT_CONTINUOUS_DRIVER64.o',prod/'AXMAT_NATIVE_PRODUCER_CHAIN.o',
    boot/'SPOR64_VERIFY.o',boot/'SPOR64_RCONTRACT.o',boot/'SPOR64_BOOT64.o']
libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',
    ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
link=[str(COMPILER),'-O2','-ffp-contract=off',*map(str,fresh_objects),
    *map(str,existing_objects),*map(str,libraries),'-o',str(RUN/'runtime/Dragon')]
command_pin=js('EXACT_PLANNED_COMPILE_AND_LINK_COMMANDS.json',dict(
    schema='SOURCE_ONLY_COMPLETE_NATIVE_CASE_BUILD_COMMANDS_V1',
    planned_output_root=str(RUN),working_directory=str(BUILD),
    original_nine_numeric_flags=FLAGS,cpp='KDRDRV.F automatically preprocessed; original #if blocks retained',
    compiler_macro_defines=[],compile_commands=commands,link_command=link,
    compile_sources=list(map(str,compile_sources)),already_compiled_objects=list(map(str,existing_objects)),
    old_archive_dependencies=list(map(str,libraries)),commands_executed=False,
    full_source_archive_build_qualified=False,transport_executed=False))
shell_lines=['# Source-only reviewable commands. Execute each with the original serial host guard.',
             '# No command in this file has been executed by the Source writer.',
             '# Build and runtime directories must first be created by the owning original host.',
             *[shlex.join(c) for c in commands],shlex.join(link)]
save('EXACT_PLANNED_COMPILE_AND_LINK_COMMANDS.sh','\n'.join(shell_lines)+'\n')

stage=[(system/'A/material.xsm','material.xsm'),(system/'A/geometry.dat','geometry.dat'),
       (system/'A/radial_track.bin','radial_track.bin'),(system/'A/snapshot_A.xsm','snapshot_A.xsm')]
stage_pins=[dict(source=pin(p),owned_runtime_relative_path='A/'+name,copy_exact_bytes=True,
    new_owned_7ID_must_be_pinned_by_original_host_before_execution=True) for p,name in stage]
if stage_pins[-1]['source']['sha256']!='8a60c979e8d1f84ef7efdbbda10c02e3d3bc8240dc548bb984b3603f7158cd42':
    raise RuntimeError('independently audited native A archive changed')
control_reader=ROOT/'validation/axial_material/snapshot_control_preflight.py'
reader_before=pin(control_reader)
spec=importlib.util.spec_from_file_location('new_warm_A_readonly_control_records',control_reader)
reader=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)
with reader._open_xsm(stage[-1][0]) as archive:
    flux_dir=archive.object('FLUX'); track_dir=archive.object('TRACK'); system_dir=archive.object('SYSTEM')
    raw_state=archive.record(flux_dir,'STATE-VECTOR',40,1)
    raw_eps=archive.record(flux_dir,'EPS-CONVERGE',5,2)
    raw_option=archive.record(flux_dir,'OPTION',1,3)
    raw_track=archive.record(track_dir,'REAL-PARAM',4,2)
    raw_system=archive.record(system_dir,'STATE-VECTOR',40,1)
    state=list(struct.unpack('<40i',raw_state))
    eps_bits=list(struct.unpack('<5I',raw_eps))
    track_bits=list(struct.unpack('<4I',raw_track))
    system_state=list(struct.unpack('<40i',raw_system))
    radial_bits=struct.unpack('<I',struct.pack('<f',2.5e-7))[0]
    mccg_bits=struct.unpack('<I',struct.pack('<f',2.5e-8))[0]
    if state[:2]!=[370,14] or state[5:12]!=[2,0,3,3,1,740,500] or state[16:18]!=[8,1]:
        raise RuntimeError('actual saved A header controls do not match new declaration')
    if raw_option!=b'B0  ' or eps_bits!=[radial_bits]*3+[0,0] or track_bits!=[mccg_bits,0,0,0]:
        raise RuntimeError('actual saved A option/EPS/TRACK bits do not match')
    if system_state[7]!=370 or system_state[0]%2!=1 or system_state[4]!=1:
        raise RuntimeError('actual A ARM ITPIJ does not support original MAXINR=2*370')
if pin(stage[-1][0])!=stage_pins[-1]['source'] or pin(control_reader)!=reader_before:
    raise RuntimeError('A archive or pure control reader changed during readonly byte audit')
header_audit=js('ACTUAL_A_SAVED_HEADER_READONLY_BYTE_AUDIT.json',dict(
    schema='ACTUAL_SAVED_A_CONTROL_RECORD_BYTES_ONLY_V1',archive=stage_pins[-1]['source'],
    complete_pure_stdlib_reader_Source=reader_before,FLUX_STATE_VECTOR=state,
    FLUX_EPS_CONVERGE_real32_bits=eps_bits,FLUX_OPTION_ascii=raw_option.decode(),
    TRACK_REAL_PARAM_real32_bits=track_bits,SYSTEM_STATE_VECTOR=system_state,
    raw_record_SHA256={k:digest(v) for k,v in [('FLUX/STATE-VECTOR',raw_state),
        ('FLUX/EPS-CONVERGE',raw_eps),('FLUX/OPTION',raw_option),
        ('TRACK/REAL-PARAM',raw_track),('SYSTEM/STATE-VECTOR',raw_system)]},
    current_A_header_exactly_matches_declared_caps_acce_option_eps=True,
    MAXINR_source_rule='actual SYSTEM ITPIJ odd; original FLUGPI MAXINR=2*NGROUP=740',
    no_numeric_library_or_transport=True,compiler_or_Native_executed=False))
saved_bindings=[ART/'axial-material-new-ROOT64-BOOT-compile-only-20261011/Root_current_compile_only_binding.json',
    ART/'axial-material-new-REAL64-producer-compile-only-20261011/Root_current_compile_only_binding.json',
    ART/'axial-material-new-REAL64-caller-compile-only-20261011/Root_current_compile_only_binding.json']
guard_and_prior_paths=set(saved_bindings)
for binding in saved_bindings:
    for p in json.loads(binding.read_text())['fixed_current_pins']:
        guard_and_prior_paths.add(Path(p['path']))
module_paths={p for folder in includes[1:] for p in folder.glob('*.mod')}
# Current complete Source reference trees for standard old archives. These pins
# do NOT establish that an old archive was built from this current Source tree.
tree_sources={p for base in [ROOT/'src',ROOT/'Trivac/src',ROOT/'Utilib/src',ROOT/'Ganlib/src']
    for p in base.rglob('*') if p.is_file() and p.suffix.lower() in ('.f','.f90','.c','.h')}
input_paths=set(protected_paths+support_sources+libraries+existing_objects+[COMPILER,Path(__file__).resolve(),
    deck_path,control_reader,system/'A/solve.log',REC/'native_warm_ingress_source_v1/test_actual_AB_warm_ingress64.f90',
    REC/'native_warm_ingress_source_v1/CURRENT_ACTUAL_AB_WARM_INGRESS_SOURCE_BINDING.json',
    REC/'native_core_controls_source/test_current_ROOT64_native_core.f90'])
input_paths|=guard_and_prior_paths|module_paths|tree_sources|{p for p,name in stage}
current_pins=[pin(p) for p in sorted(input_paths)]
protected_after=[pin(p) for p in protected_paths]
if protected_before!=protected_after: raise RuntimeError('protected original/frozen Source changed')
manifest=js('NEW_WARM_A_COMPLETE_INPUT_DECLARATION_AND_CURRENT_PINS.json',dict(
    schema='NEW_EXPLICIT_NATIVE_REAL64_WARM_A_SOURCE_DECLARATION_V1',
    case_name='ROOT64_NEW_WARM_A_20261011',LCM_case_name='R64WARM-A-V1',
    declaration_role='new owned warm experiment; no predecessor whole-input qualification',
    independent_case_operand_Source=source_pins[1],dispatcher_Source=source_pins[0],deck=deck_pin,
    new_source_pins=source_pins,exact_original_inverse_proofs=[proof,deck_proof],
    exact_build_command_declaration=command_pin,physical_input_staging=stage_pins,
    actual_saved_A_header_readonly_byte_evidence=header_audit,
    pinned_inputs=current_pins,current_source_reference_inventory_count=len(tree_sources),
    old_archive_source_to_object_mapping_proved=False,
    declared_controls=dict(FLU_eps_radial=2.5e-7,eps_axial=5e-8,TRACK_RCONTRACT_eps_mccg=2.5e-8,
        actual_DOOR_internal_work_min=2.5e-10,AXMAT_EPS64=2.5e-10,AXMAT_THER64=2.5e-9,
        EXTE=500,MAXINR=740,ACCE=[3,3],REBA=1,INITFL=1,OPTION='B0',TYPE='K',
        NGRP=370,NIFIS=32,NMAT=8,NREG=8,NUNK=14,plane=1,epoch=0),
    microscopic_material_tree='complete A material.xsm L_LIBRARY copied unchanged to MICROLIB2; MACROLIB is only a view',
    actual_native_warm_read='RECOVER FLUX from actual A archive FLUX[1], then full370 type4 loader; no old seed or REAL32 promotion',
    source_route='standard DRAMOD -> complete isolated KDRDRV.F -> FLUNAT64 -> complete native caller/driver -> real strict terminal publisher',
    planned_stdout_marker='ROOT64-NEW-WARM-A-NATIVE-COMPLETE',
    planned_native_run=dict(argv=[str(RUN/'runtime/Dragon')],cwd=str(RUN/'A'),
        stdin_deck=str(OUT/'ROOT64_NEW_WARM_A_20261011.x2m'),stdout_log=str(RUN/'A/solve.log'),
        maximum_wall_seconds=600,automatic_retries=0,threads=1,original_host_guard_required=True),
    required_external_binding='original independent host must repin every current input before/after build and native run, plus actual output fullEOF/7ID; copies get new independent owned 7IDs',
    protected_before=protected_before,protected_after=protected_after,
    original_nine_numeric_flags_unchanged=True,compiler_preprocessor_rule='.F automatic cpp; no added -D macro',
    source_writer_only=True,compiler_or_Native_executed=False,transport_executed=False,
    original_seventeen_controls_executed=False,full_370_GLOBAL_QFISS_epoch_controls_executed=False,
    continuous_REAL64_producer_qualified=False,online_BOOT_qualified=False,
    rank2_or_AAA_or_reference_or_ABA_qualification_inherited=False,goal_complete=False))
note='''SOURCE-ONLY native warm-A case route freeze, 2026-10-11

The complete isolated KDRDRV.F retains the original function symbol, every
ordinary dispatch branch, #if HDF5_LIB block and all other original bytes.
One exact local splice registers AXNCASE64: and FLUNAT64:. .F explicitly
preserves automatic cpp; no extra -D option or numerical flag is introduced.

AXNCASE64 is a real two-output standard CLE entry using retained GANLIB
LCMPTC/LCMPUT and the original SPOR64_RCONTRACT_LOAD/VERIFY ABI. It creates
exactly six independent RCONTRACT records and three BOOT_BIND records.
The full experiment name maps to the explicit fixed-12-character case token
R64WARM-A-V1. Plane1/epoch0 is a declared input; it does not fabricate
GLOBAL64, QFISS, a solved seal, bootstrap closure or scientific PASS.

The complete new deck preserves actual A's SALT/MCCGT/ASM input bytes,
complete material tree, geometry, tracking and FLU physical controls. Its
only warm guess is the actual full REAL64 snapshot_A.xsm FLUX list ITEM1,
already checked for all 5180 native bits by Root. RECOVER identifies object
names, so ITEM1 remains correct; the archive does not use FLUX ITEM4.
Only FLUNAT64 performs new transport. It uses direct full type4 REAL64 input
and publishes only its actual strict kernel return followed by full header
and all later original FLU checks. The complete output archive also saves
TRACK, full MICROLIB2, SYSTEM, FLUX, RCONTRACT and BOOT_BIND.

TRACK/RCONTRACT declaration is 2.5e-8. Actual A8 DOOR work uses
min(declared,2.5e-10); AXMAT_EPS64=2.5e-10 and AXMAT_THER64=2.5e-9.
Outer controls remain all2.5e-7, EXTE500, MAXINR740, ACCE3/3, REBA1,
INITFL1, OPTION B0 and TYPE K. No inherited wholecase with MCCG1e-5.
Axial5e-8 is only the original independent contract declaration here; this
radial native case does not execute or qualify an axial/global solve.

EXACT_PLANNED_COMPILE_AND_LINK_COMMANDS.json contains every full argv and
the exact fresh output paths. It explicitly rebuilds the real A8/ACA/A9,
AXMAT_FLUKEF64, real DOOR/balance, corrected MCGASM/MCGFST/MCGDSCA,
rank adapter, original MCGFFIR, original FLUGPI, DRAGON and both route
Sources. It links the current actual compiled new caller, driver/helper,
VERIFY/RCONTRACT/BOOT module objects before pinned old standard archives.
MCGFFIR64_RANK_ADAPTER is never replaced by a REAL32 adapter.
Ordinary fallback branches, including SPOT, remain distinct and are
resolved through the pinned old archives. This case is real MCCG TYPE K;
it does not replace or qualify continuous global SPOT.

The declaration includes fullEOF SHA/7ID of every actual current input,
compiled dependency/module, opaque archive, original guard Source and
current full standard Source reference trees. The old archives are valid
separately pinned build dependencies; pinning a current Source inventory
does not prove their historic Source-to-object mapping or a full Source
archive rebuild. No such qualification is claimed.

Root still must use the original serial host guard to create fresh build/
runtime/A directories, copy exactly the four declared physical inputs
to the short owned LCM filenames, repin each new owned copy, execute the
listed compile/link commands, then the one bounded genuine Native case.
No physical file copies, compile/link/Native or parser were run here.
External host full input/output SHA/7ID and real stdout/watchdog evidence
remain mandatory; an internal ROOT-REF64 self-copy is not independent proof.

Mandatory remaining admission: full original17 applicable controls plus
the explicitly new warm route's controls, all370 GLOBAL64 and native
source/QFISS/plane/epoch coherence, three-plane bootstrap with actual
kernel and independent closure, and online BOOT. None is bypassed or
labelled completed by this Source package. Current common rank2 remains
353/370 (groups1-17 fail); formal AAA endpoint remains3.9525259224%>3%.
Independent coupled reference and ABA are not admitted by this case.
'''
note_pin=save('FINAL_ROUTE_SOURCE_BUILD_AND_REMAINING_SCOPE.txt',note)
result=dict(status='COMPLETE_NATIVE_CASE_ROUTE_SOURCE_WRITTEN_AND_FROZEN',
    source_pins=source_pins,deck=deck_pin,manifest=manifest,notes=note_pin,
    complete_dispatcher_original_inverse=True,complete_deck_original_inverse=True,
    current_input_pin_count=len(current_pins),protected_original_and_frozen_Source_unchanged=True,
    planned_compile_count=len(commands),link_or_Native_executed=False,
    elapsed_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
print(json.dumps(result,ensure_ascii=False))
