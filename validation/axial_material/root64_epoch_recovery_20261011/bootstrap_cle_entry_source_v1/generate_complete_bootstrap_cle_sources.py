from pathlib import Path
import hashlib
import json
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = Path(__file__).resolve().parent


def identity(stat):
    return [stat.st_dev, stat.st_ino, stat.st_mode, stat.st_nlink,
            stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = identity(path.stat())
    with path.open('rb') as stream:
        data = stream.read()
    after = identity(path.stat())
    assert before == after, str(path)
    assert len(data) == before[4], str(path)
    return {'path': str(path), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(), 'seven_id': before,
            'full_EOF_before_after_stable': True}


def write_new(name, data):
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(data if isinstance(data, bytes) else data.encode('utf-8'))
    return pin(target)


def write_json(name, data):
    return write_new(name, json.dumps(data, ensure_ascii=False, indent=2) + '\n')


started = time.monotonic()
origin = REC / 'native_case_route_source_v1/KDRDRV.F'
expected_origin_sha = '0e5f993424aeed2e973de97b146cd57bb8fc96c2f9d2478e897b82277588625c'
protected_paths = [origin,
    REC / 'bootstrap_global_projection_publish_source_v2/SPOR64_BOOT_PUBLISH64.f90',
    REC / 'bootstrap_global_projection_publish_source_v2/SPOR64_BOOT_PROJECT64.f90',
    REC / 'bootstrap_qfiss_source_v2/SPOR64_BOOT_CANONICAL64.f90',
    REC / 'bootstrap_qfiss_source_v2/SPOR64_BOOT_CONTEXT64.f90',
    REC / 'bootstrap_qfiss_source_v2/SPOR64_BOOTQ64.f90',
    REC / 'global_native64_caller_source_v1/FLUGLOBAL64.f', ROOT / 'src/KDRDRV.F']
protected_before = [pin(p) for p in protected_paths]
assert protected_before[0]['sha256'] == expected_origin_sha
assert protected_before[1]['sha256'] == 'cac30f92e0c246eca9ebaed798387696ee650029b9ff7a646b7437824701cff5'
assert protected_before[2]['sha256'] == 'd449d30d08907b29767a2e74d4ae761b92f0e5d99cd60ea3601e55ae4919398c'
assert protected_before[3]['sha256'] == '5d161094b3f5c671eb77d139042e396474225c138ae545de0384febfa7241bc2'
assert protected_before[4]['sha256'] == 'eeaf0bc9cdbbb35c71026eaa1c95995109a9d074a82feb3dd023515bafa69820'
assert protected_before[5]['sha256'] == '7172121d57c3411c62845a81cc41886ee9759d4c168423b13541fc3a91afecd8'

project = '''! NEW SOURCE: standard CLE entry for the complete bootstrap projection.
! Ordered operands: PROJECTED_OUT GLOBAL64 AX AXTRACK AXSYSTEM AXMACRO ARCHIVE RCON.
! Syntax is exactly :: RANK 1 ; or :: RANK 2 ;. No default or rank fallback.
subroutine BPROJ64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated
  use SPOR64_VERIFY, only: EMPTY_ROOT
  use SPOR64_BOOT_PROJECT64, only: SPOR64_BOOT_PROJECT_ARCHIVE, &
      SPOR64_BOOT_PROJECT_COMMITTED
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  integer :: i,j,object_length,requested_rank,status,token_type,token_integer
  real :: token_real
  double precision :: token_double
  character(len=12) :: token_text,object_directory
  character(len=72) :: object_file
  logical :: object_empty,is_lcm

  if(nentry/=8) call XABORT('BPROJ64: EXACT EIGHT ORDERED OPERANDS REQUIRED.')
  if(any((ientry/=1).and.(ientry/=2))) &
      call XABORT('BPROJ64: ONLY LCM/XSM OPERANDS ALLOWED.')
  if(jentry(1)/=0.or.any(jentry(2:8)/=2)) &
      call XABORT('BPROJ64: FRESH OUTPUT AND SEVEN READONLY INPUTS REQUIRED.')
  do i=1,nentry
    if(.not.c_associated(kentry(i))) call XABORT('BPROJ64: NULL OPERAND.')
    if(len_trim(hentry(i))==0) call XABORT('BPROJ64: EMPTY CLE OBJECT NAME.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
          call XABORT('BPROJ64: OPERAND ALIAS OR REPEATED CLE NAME.')
    enddo
    call LCMINF(kentry(i),object_file,object_directory,object_empty,object_length,is_lcm)
    if(object_length/=-1.or.trim(object_directory)/='/') &
        call XABORT('BPROJ64: ROOT DIRECTORY OPERANDS REQUIRED.')
    if((ientry(i)==1).neqv.is_lcm) &
        call XABORT('BPROJ64: CLE STORAGE DESCRIPTOR MISMATCH.')
  enddo
  if(.not.EMPTY_ROOT(kentry(1))) call XABORT('BPROJ64: OUTPUT MUST BE EMPTY.')

  ! Consume exactly one keyword, one integer and the terminating semicolon.
  ! The independent host binds this explicit rank to the frozen owning case.
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/='RANK') &
      call XABORT('BPROJ64: MANDATORY UNIQUE RANK KEYWORD REQUIRED.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=1) call XABORT('BPROJ64: INTEGER RANK REQUIRED.')
  requested_rank=token_integer
  if(requested_rank/=1.and.requested_rank/=2) &
      call XABORT('BPROJ64: RANK MUST BE EXACTLY ONE OR TWO.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('BPROJ64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.')

  ! The callee checks GLOBAL64 against all six independent physical inputs,
  ! recomputes the full canonical state and checks every requested rank.
  ! It publishes only PROJECTED-BOOT/e0, commits EPOCH last, and performs
  ! complete caller-output readback. This is not a transport or SVD gate.
  call SPOR64_BOOT_PROJECT_ARCHIVE(kentry(1),kentry(2),kentry(3),kentry(4), &
      kentry(5),kentry(6),kentry(7),kentry(8),requested_rank,status)
  if(status/=SPOR64_BOOT_PROJECT_COMMITTED) &
      call XABORT('BPROJ64: COMPLETE PROJECTION ADMISSION OR COMMIT FAILED.')
end subroutine BPROJ64
'''

source = '''! NEW SOURCE: standard CLE entry for the complete bootstrap QFISS64 path.
! Ordered operands: MACRO_OUT SOURCE_OUT PROJECTED GLOBAL64 AX AXTRACK
!                   AXSYSTEM AXMACRO ARCHIVE RCON.
! Syntax is exactly :: PLANE 1 ;, :: PLANE 2 ; or :: PLANE 3 ;.
subroutine BQFIS64(nentry,hentry,ientry,jentry,kentry)
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated
  use, intrinsic :: iso_fortran_env, only: real64
  use SPOR64_VERIFY, only: EMPTY_ROOT
  use SPOR64_BOOTQ64_V2, only: SPOR64_BOOTQ64_BUILD,SPOR64_BOOTQ64_READ, &
      SPOR64_BOOTQ64_COMMITTED,SPOR64_BOOTQ64_LOADED
  implicit none
  integer, intent(in) :: nentry,ientry(nentry),jentry(nentry)
  character(len=12), intent(in) :: hentry(nentry)
  type(c_ptr), intent(in) :: kentry(nentry)
  integer :: i,j,object_length,plane_index,status,token_type,token_integer
  real :: token_real
  double precision :: token_double
  real(real64), allocatable :: verified_q64(:,:)
  real(real64) :: verified_rho64
  character(len=12) :: token_text,object_directory
  character(len=72) :: object_file
  logical :: object_empty,is_lcm

  if(nentry/=10) call XABORT('BQFIS64: EXACT TEN ORDERED OPERANDS REQUIRED.')
  if(any((ientry/=1).and.(ientry/=2))) &
      call XABORT('BQFIS64: ONLY LCM/XSM OPERANDS ALLOWED.')
  if(any(jentry(1:2)/=0).or.any(jentry(3:10)/=2)) &
      call XABORT('BQFIS64: TWO FRESH OUTPUTS AND EIGHT READONLY INPUTS REQUIRED.')
  do i=1,nentry
    if(.not.c_associated(kentry(i))) call XABORT('BQFIS64: NULL OPERAND.')
    if(len_trim(hentry(i))==0) call XABORT('BQFIS64: EMPTY CLE OBJECT NAME.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
          call XABORT('BQFIS64: OPERAND ALIAS OR REPEATED CLE NAME.')
    enddo
    call LCMINF(kentry(i),object_file,object_directory,object_empty,object_length,is_lcm)
    if(object_length/=-1.or.trim(object_directory)/='/') &
        call XABORT('BQFIS64: ROOT DIRECTORY OPERANDS REQUIRED.')
    if((ientry(i)==1).neqv.is_lcm) &
        call XABORT('BQFIS64: CLE STORAGE DESCRIPTOR MISMATCH.')
  enddo
  do i=1,2
    if(.not.EMPTY_ROOT(kentry(i))) call XABORT('BQFIS64: OUTPUT MUST BE EMPTY.')
  enddo

  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/='PLANE') &
      call XABORT('BQFIS64: MANDATORY UNIQUE PLANE KEYWORD REQUIRED.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=1) call XABORT('BQFIS64: INTEGER PLANE REQUIRED.')
  plane_index=token_integer
  if(plane_index<1.or.plane_index>3) &
      call XABORT('BQFIS64: PLANE MUST BE ONE THROUGH THREE.')
  call REDGET(token_type,token_integer,token_real,token_text,token_double)
  if(token_type/=3.or.token_text/=';') &
      call XABORT('BQFIS64: DUPLICATE OR ADDITIONAL OPTIONS FORBIDDEN.')

  ! Full PROJECTED-BOOT/e0 admission precedes every output mutation.
  ! All 370 groups and 32 fission slots use the frozen original formula.
  ! The full selected macrolib is cloned; only NUSIGF physical records
  ! are cleared. DSOUR32 is a mirror of the actual type-4 QFISS authority.
  call SPOR64_BOOTQ64_BUILD(kentry(3),kentry(4),kentry(5),kentry(6), &
      kentry(7),kentry(8),kentry(9),kentry(10),plane_index, &
      kentry(1),kentry(2),status)
  if(status/=SPOR64_BOOTQ64_COMMITTED) &
      call XABORT('BQFIS64: COMPLETE QFISS ADMISSION OR COMMIT FAILED.')

  ! Actual independent recomputation and full-tree comparison, not metadata.
  ! A committed output whose complete readback fails is never returned.
  call SPOR64_BOOTQ64_READ(kentry(3),kentry(4),kentry(5),kentry(6), &
      kentry(7),kentry(8),kentry(9),kentry(10),plane_index, &
      kentry(1),kentry(2),verified_q64,verified_rho64,status)
  if(status/=SPOR64_BOOTQ64_LOADED) &
      call XABORT('BQFIS64: COMMITTED OUTPUT COMPLETE READBACK FAILED.')
  if(.not.allocated(verified_q64)) &
      call XABORT('BQFIS64: REAL64 READBACK ARRAY MISSING.')
  if(size(verified_q64,1)<=0.or.size(verified_q64,2)/=370) &
      call XABORT('BQFIS64: REAL64 READBACK SHAPE MISMATCH.')
  deallocate(verified_q64)
end subroutine BQFIS64
'''

old_dispatch = origin.read_bytes()
anchor = b"      ELSE IF(HMODUL.EQ.'FLU:') THEN\n         CALL FLU(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
new_dispatch = (b"      ELSE IF(HMODUL.EQ.'FLUGLOBAL64:') THEN\n"
                b"         CALL FLUGLOBAL64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
                b"      ELSE IF(HMODUL.EQ.'BPROJ64:') THEN\n"
                b"         CALL BPROJ64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n"
                b"      ELSE IF(HMODUL.EQ.'BQFIS64:') THEN\n"
                b"         CALL BQFIS64(NENTRY,HENTRY,IENTRY,JENTRY,KENTRY)\n" + anchor)
assert old_dispatch.count(anchor) == 1
candidate_dispatch = old_dispatch.replace(anchor, new_dispatch, 1)
assert candidate_dispatch.count(new_dispatch) == 1
assert candidate_dispatch.replace(new_dispatch, anchor, 1) == old_dispatch
source_pins = [write_new('BPROJ64.f90', project),
               write_new('BQFIS64.f90', source),
               write_new('KDRDRV.F', candidate_dispatch)]
retained = write_new('original_exact_source/KDRDRV.F', old_dispatch)
proof = write_json('KDRDRV_COMPLETE_SOURCE_EXACT_LOCAL_BYTE_INVERSE.json', {
    'schema': 'COMPLETE_NATIVE_DISPATCHER_THREE_ROUTE_EXTENSION_EXACT_INVERSE_V1',
    'original': protected_before[0], 'retained_complete_original': retained,
    'new': source_pins[2], 'original_size': len(old_dispatch),
    'new_size': len(candidate_dispatch),
    'literal_changes': [[anchor.decode(), new_dispatch.decode()]],
    'full_byte_inverse_matches': candidate_dispatch.replace(new_dispatch, anchor, 1) == old_dispatch,
    'only_new_routes': ['FLUGLOBAL64:', 'BPROJ64:', 'BQFIS64:'],
    'original_AXNCASE64_and_FLUNAT64_routes_preserved': True,
    'original_KTRDRV_fallback_and_all_old_routes_preserved': True,
    'HDF5_LIB_cpp_bytes_preserved': True, 'suffix': '.F',
    'new_numeric_flags': [], 'compiler_executed': False})

global_binding_path = REC / 'global_native64_caller_source_v1/FINAL_CURRENT_GLOBAL_CALLER_EXTERNAL_SOURCE_DEPENDENCY_BINDING.json'
global_binding = json.loads(global_binding_path.read_bytes())
q_binding_path = REC / 'bootstrap_qfiss_source_v2/SOURCE_PINS_DEPENDENCIES_AND_REMAINING_SCOPE.json'
q_binding = json.loads(q_binding_path.read_bytes())
route_plan_path = REC / 'native_case_route_source_v1/EXACT_PLANNED_COMPILE_AND_LINK_COMMANDS.json'
route_plan = json.loads(route_plan_path.read_bytes())
dependency_paths = set()
for key in ('caller_five_complete_Source_pins', 'bootstrap_v2_complete_Source_pins',
            'foundation_complete_Source_pins', 'original_and_frozen_global_v2_Source_pins'):
    for item in global_binding[key]:
        dependency_paths.add(item['path'])
for item in q_binding['actual_dependency_pins']:
    dependency_paths.add(item['path'])
dependency_paths.update(str(p) for p in protected_paths)
dependency_paths.update([
    str(ROOT / 'Ganlib/src/LCMTLC.f90'),
    str(REC / 'native_case_route_source_v2/AXNCASE64.f90'),
    str(REC / 'native_producer_chain_source/caller_candidate_v1/FLUNAT64.f'),
    str(REC / 'native_producer_chain_source/caller_candidate_v1/FLUDRVN64.f'),
    str(REC / 'native_producer_chain_source/caller_candidate_v1/AXMAT_NATIVE_CALLER_API.f90'),
    str(REC / 'native_producer_chain_source/AXMAT_CONTINUOUS_DRIVER64.f'),
    str(REC / 'native_producer_chain_source/AXMAT_NATIVE_PRODUCER_CHAIN.f90'),
    str(ROOT / 'Trivac/lib/Darwin_arm64/libTrivac.a'),
    str(ROOT / 'Utilib/lib/Darwin_arm64/libUtilib.a')])
dependencies = [pin(Path(p)) for p in sorted(dependency_paths)]
protected_after = [pin(p) for p in protected_paths]
assert protected_before == protected_after
scope = {
    'schema': 'COMPLETE_BOOTSTRAP_CLE_ENTRY_SOURCE_AND_DEPENDENCY_BINDING_V1',
    'status': 'NEW_COMPLETE_SOURCE_CANDIDATE_ONLY_NOT_COMPILED_NOT_RUN',
    'source_pins': source_pins, 'writer_pin': pin(Path(__file__)),
    'complete_dispatcher_original_inverse': proof,
    'protected_before': protected_before, 'protected_after': protected_after,
    'protected_Source_bytes_and_seven_ids_unchanged': protected_before == protected_after,
    'actual_complete_EOF_dependency_pins': dependencies,
    'inherited_global_dependency_binding': pin(global_binding_path),
    'inherited_bootstrap_dependency_binding': pin(q_binding_path),
    'inherited_legacy_native_link_dependency_plan': pin(route_plan_path),
    'legacy_native_link_order_reference_only': route_plan['link_command'],
    'standard_CLE_ABI': ['nentry', 'hentry(nentry):CHAR12', 'ientry(nentry):INTEGER',
                         'jentry(nentry):INTEGER', 'kentry(nentry):C_PTR'],
    'BPROJ64': {
        'NENTRY': 8,
        'ordered_operand_roles': ['PROJECTED_OUT', 'GLOBAL64', 'AX', 'AXTRACK',
                                  'AXSYSTEM', 'AXMACRO', 'ARCHIVE', 'RCON'],
        'IENTRY': 'every entry exactly 1 (LCM) or 2 (XSM), matched to actual LCMINF medium',
        'JENTRY': [0, 2, 2, 2, 2, 2, 2, 2],
        'syntax': [':: RANK 1 ;', ':: RANK 2 ;'],
        'required_rank': 'mandatory unique integer; all370 canonical ranks must match; no default or fallback',
        'callee': 'SPOR64_BOOT_PROJECT64::SPOR64_BOOT_PROJECT_ARCHIVE',
        'callee_ABI_argument_count': 10,
        'caller_output_complete_readback': 'performed inside frozen callee; failure XABORT'},
    'BQFIS64': {
        'NENTRY': 10,
        'ordered_operand_roles': ['MACRO_OUT', 'SOURCE_OUT', 'PROJECTED', 'GLOBAL64',
                                  'AX', 'AXTRACK', 'AXSYSTEM', 'AXMACRO', 'ARCHIVE', 'RCON'],
        'IENTRY': 'every entry exactly 1 (LCM) or 2 (XSM), matched to actual LCMINF medium',
        'JENTRY': [0, 0, 2, 2, 2, 2, 2, 2, 2, 2],
        'syntax': [':: PLANE 1 ;', ':: PLANE 2 ;', ':: PLANE 3 ;'],
        'plane': 'mandatory unique integer1..3; no default',
        'callees': ['SPOR64_BOOTQ64_V2::SPOR64_BOOTQ64_BUILD',
                    'SPOR64_BOOTQ64_V2::SPOR64_BOOTQ64_READ'],
        'callee_ABI_argument_counts': [12, 14],
        'complete_readback': 'rebuild fullphysical macro/source in private XSM then compare every tree/raw record',
        'readback_failure': 'fatal; no output returns as accepted on failure'},
    'CLE_HENTRY_names': 'actual caller names (CHAR12), roles bind by explicit operand position, no hardcoded oversized role-name strings',
    'all_operand_aliases': 'all pairwise C_PTR equality and repeated CLE HENTRY names rejected; host also binds external filesystem identity',
    'freshness': 'JENTRY0 and EMPTY_ROOT before calls; existing products not overwritten',
    'inputs_readonly': 'all inputs JENTRY2; no entry output mutation except by the full frozen callee',
    'lifecycle': 'PROJECTED-BOOT/e0 and FROZEN-QFIS/e0 only; no SOLVED/e0 or synthetice1',
    'source_ancestry': 'KDRDRV complete frozen original plus one exact splice; entries are explicitly new Source using exact standard descriptor ABI and true full callees',
    'compiler_order': ['BPROJ64.f90 after SPOR64_BOOT_PROJECT64.mod',
                       'BQFIS64.f90 after SPOR64_BOOTQ64_V2.mod',
                       'KDRDRV.F with automatic cpp preserving original HDF5_LIB conditional'],
    'new_link_overrides_required': ['new KDRDRV.o replaces old dispatcher (one definition)',
        'new BPROJ64.o and BQFIS64.o', 'complete frozen new project/publisher and bootstrapCAN/CTX/Q v2 objects',
        'complete frozen five globalcaller objects and full globaldriver dependencies',
        'preserved AXNCASE64 route must link corrected v2 entry object, not unready v1',
        'preserved FLUNAT64 route requires existing complete native caller/driver/helper objects',
        'then original libDragon, libTrivac, libUtilib, libGanlib order'],
    'not_an_executed_or_complete_new_link_command': True,
    'current_compiled_module_paths_and_new_link_order_host_binding_pending': True,
    'old_opaque_archives_remain_dependencies_not_full_source_build_qualification': True,
    'original_nine_numeric_flags_unchanged': route_plan['original_nine_numeric_flags'],
    'scientific_gate_changes': [], 'compiler_executed': False, 'link_executed': False,
    'transport_executed': False, 'original_17_controls_passed': False,
    'global_actual_runtime_qualified': False, 'bootstrap_actual_runtime_qualified': False,
    'AAA_qualified': False, 'ABA_started': False,
    'remaining_scope': [
        'Root builds this threeSource package under original resource/watchdog/SHA/7ID guard with current module and object pins.',
        'Root freezes the owning case/prepared rank and exact deck, unique fullphysical inputs, true globalcaller terminal and external pins.',
        'Run actual CLE descriptor/option/refusal controls and full XSM commit/readback controls before native bootstrap qualification.',
        'Actual BOOT kernel/caller and its later dispatcher registration remain separate unfinished work.',
        'Original17/global/sourceepoch/coherenttamper controls and complete physical transport admission remain required.',
        'Uniformrank1 formalAAA remains separate from independent originalrank2; new rankAPI grants neither admission.',
        'No material/threshold/rankselection/iteration/math changes or scienceABA run in this Source package.']}
manifest = write_json('SOURCE_PINS_DEPENDENCIES_ABI_AND_REMAINING_SCOPE.json', scope)
write_new('CLE_ABI_AND_COMPLETE_SOURCE_SCOPE.txt', '''NEW SOURCE ONLY. No compiler, link, parser, native, transport or numeric job executed.

BPROJ64 standard five-tuple CLE entry:
  NENTRY8 ordered PROJECTED_OUT GLOBAL64 AX AXTRACK AXSYSTEM AXMACRO ARCHIVE RCON
  first product JENTRY0, seven inputs JENTRY2, every IENTRY1/2 matched to actual medium.
  Exact options RANK 1 ; or RANK 2 ;. No default, fallback, duplicate or trailing option.
  Calls actual frozen project10arg ABI with mandatory rank, all370mustmatch.
  Full global/physical/canonical checks and complete readback occur in the real callee.

BQFIS64 standard five-tuple CLE entry:
  NENTRY10 ordered MACRO_OUT SOURCE_OUT PROJECTED GLOBAL64 AX AXTRACK AXSYSTEM AXMACRO ARCHIVE RCON
  first2 products JENTRY0, eight inputs JENTRY2, every IENTRY1/2 matched to actual medium.
  Exact options PLANE 1 ;, PLANE 2 ; or PLANE 3 ;. No default or extra tokens.
  Calls actual frozen BUILD12arg, then READ14arg for complete physical recomputation.
  Readback failures are fatal; rawtype4 all370QFISS array must be present.

Both entries require actual root directories, fresh products, non-null handles and pairwise
independent handles/names. HENTRY remains actual caller names rather than hardcoded long
role labels. External host SHA/7ID binding still ensures unique actual filesystem inputs;
coherent self-rewrites are not independently authenticated by metadata copies.

KDRDRV.F is the complete original native-route dispatcher with exactly one local splice
adding FLUGLOBAL64:, BPROJ64:, BQFIS64:. Original AXNCASE64:/FLUNAT64: routes and every
old branch/KTRDRV fallback/HDF5_LIB conditional remain byte-identical outside that splice.
It retains .F automatic cpp and the original nine numeric flags. Corrected AXNCASE64 v2
must be linked; the dispatcher does not duplicate or silently repair frozen entry Sources.

No whole-case deck is declared here: the owning host must provide its frozen prepared/case
rank, all independent physical inputs and actual terminal output pins. Actual BOOT kernel
and caller remain separate unfinished work, with later dispatcher registration still due.
Complete existing libraries are pinned opaque dependencies; no full-source archive-build
qualification, original17/global/sourceepoch/coherenttamper pass, AAA qualification or ABA
admission is claimed. NewSource is reviewable/callable, not runtime-qualified.
''')
print(json.dumps({'writer_completed': True, 'source_pins': source_pins,
                  'manifest': manifest, 'protected_unchanged': True,
                  'elapsed_seconds': time.monotonic()-started,
                  'compiler_executed': False, 'transport_executed': False}))
