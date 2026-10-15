"""Source-only derivation of the complete strict SPOSTATE64 candidate.

No Fortran compiler, native process, physics, training or numerical library is
called.  Every transformation and its exact byte inverse are saved locally.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import resource
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = REC / 'continuous_chain_source'
START = time.monotonic()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def fullpin(path):
    before = identity(path.lstat())
    with path.open('rb') as stream:
        opened = identity(os.fstat(stream.fileno()))
        data = stream.read()
        eof = identity(os.fstat(stream.fileno()))
    after = identity(path.lstat())
    if not before == opened == eof == after:
        raise ValueError('input identity changed: ' + str(path))
    return data, dict(path=str(path), size_bytes=len(data), sha256=sha(data),
                     identity=after, before_open_EOF_after_identity_equal=True)


original, original_pin = fullpin(ROOT / 'src/SPOSTATE.f90')
if original_pin['sha256'] != 'f99691472f42cad00d96915c4a1a38403ac0cc71fe6580bf61651d0d2f015788':
    raise ValueError('exact reviewed SPOSTATE Source changed')
protected = [ROOT / 'src/SPOSTATE.f90',
             REC / 'new_source/SPOR64_BOOT64.f90',
             REC / 'new_source/SPOBOOT64.f90']
protected_before = {str(p): fullpin(p)[1] for p in protected}
dependencies = [ROOT / 'src/SPOT_LEAKAGE.f90', ROOT / 'Ganlib/src/ganlib.f90',
                ROOT / 'Ganlib/src/lcmmod.f90', ROOT / 'Ganlib/src/LCMAUX.f90']
dependency_pins = [fullpin(p)[1] for p in dependencies]
source = original.decode('utf8')
steps = []


def replace_once(label, old, new):
    global source
    if source.count(old) != 1:
        raise ValueError('unique exact transform anchor required: ' + label)
    before = source.encode('utf8')
    position = before.index(old.encode('utf8'))
    source = source.replace(old, new, 1)
    after = source.encode('utf8')
    if after[:position] != before[:position] or after[position+len(new.encode('utf8')):] != before[position+len(old.encode('utf8')):]:
        raise ValueError('nonlocal bytes changed: ' + label)
    steps.append(dict(label=label, mode='one_exact_local_byte_splice',
                      byte_offset_in_step_input=position, old=old, new=new,
                      old_bytes=len(old.encode('utf8')), new_bytes=len(new.encode('utf8')),
                      before_sha256=sha(before), after_sha256=sha(after),
                      outside_splice_exact_bytes_equal=True))


def rename_token(label, old, new):
    global source
    if new in source:
        raise ValueError('rename target already present: ' + label)
    before = source.encode('utf8')
    pattern = r'\b' + re.escape(old) + r'\b'
    count = len(re.findall(pattern, source))
    if not count:
        raise ValueError('rename token absent: ' + label)
    source = re.sub(pattern, new, source)
    steps.append(dict(label=label, mode='exact_identifier_token_rename',
                      old=old, new=new, occurrence_count=count,
                      before_sha256=sha(before), after_sha256=sha(source.encode('utf8'))))


rename_token('new independent entry and diagnostics name', 'SPOSTATE', 'SPOSTATE64')
rename_token('legacy unknown array is explicitly a checked mirror only', 'unknown', 'mirror32')
replace_once('honest new Source scope comment', '!DECK SPOSTATE64\n',
             '!DECK SPOSTATE64\n'
             '! NEW SOURCE, strict REAL64 canonical-state component.\n'
             '! Derived by exact saved local transformations of the complete SPOSTATE.\n'
             '! FLUX64/SPOT-KEFF64 are mandatory numerical inputs; type2 is a mirror.\n'
             '! This routine is not GLOBAL64 provenance, a new terminal solve,\n'
             '! bootstrap/QFISS production, online BOOT or scientific qualification.\n')
replace_once('use only the existing REAL64 leakage operator',
             '  use SPOT_LEAKAGE, only : SPOLE1, SPOLE1D\n',
             '  use SPOT_LEAKAGE, only : SPOLE1D\n')
replace_once('explicit GANLIB arithmetic-kind contract',
             '  use, intrinsic :: iso_fortran_env, only : int64\n',
             '  use, intrinsic :: iso_fortran_env, only : int32, int64, real32, real64\n')
replace_once('compile-time arithmetic-kind guard',
             '  integer, parameter :: nstate=40\n',
             '  integer, parameter :: nstate=40\n'
             '  integer, parameter :: kind_guard=1/merge(1,0, &\n'
             '    kind(1)==int32.and.kind(1.0)==real32.and.dp==real64)\n')
replace_once('REAL64 restriction accumulator declarations',
             '  real :: flott,keff,projected_sp,weight_sp\n',
             '  real :: flott,keff\n'
             '  real(kind=dp) :: projected64,restriction_weight64\n')
replace_once('remove unused binary32 leakage arrays',
             '  real, allocatable :: phi(:,:),current(:,:),leak_sp(:)\n'
             '  real, allocatable :: numerator(:),denominator(:)\n', '')
replace_once('remove optional precision switch', '  logical :: lr64\n', '')

replace_once('mandatory REAL64 keff, no REAL32 fallback',
'''  rho=1.0_dp/real(keff,dp)
  lr64=.false.
  keff64=real(keff,dp)
  call LCMLEN(kentry(1),'SPOT-KEFF64',ilong,itylcm)
  if (ilong /= 0) then
    if ((ilong /= 1).or.(itylcm /= 4)) &
      call XABORT('SPOSTATE64: INVALID SPOT-KEFF64.')
    call LCMGET(kentry(1),'SPOT-KEFF64',keff64)
    if ((.not.ieee_is_finite(keff64)).or.(keff64 <= 0.0_dp)) &
      call XABORT('SPOSTATE64: NONPOSITIVE SPOT-KEFF64.')
    if (transfer(real(keff64),0) /= transfer(keff,0)) &
      call XABORT('SPOSTATE64: K-EFFECTIVE MIRROR MISMATCH.')
    rho=1.0_dp/keff64
    lr64=.true.
  endif
''',
'''  call LCMLEN(kentry(1),'SPOT-KEFF64',ilong,itylcm)
  if ((ilong /= 1).or.(itylcm /= 4)) &
    call XABORT('SPOSTATE64: INVALID SPOT-KEFF64.')
  call LCMGET(kentry(1),'SPOT-KEFF64',keff64)
  if ((.not.ieee_is_finite(keff64)).or.(keff64 <= 0.0_dp)) &
    call XABORT('SPOSTATE64: NONPOSITIVE SPOT-KEFF64.')
  if (transfer(real(keff64,real32),0_int32) /= transfer(keff,0_int32)) &
    call XABORT('SPOSTATE64: K-EFFECTIVE MIRROR MISMATCH.')
  rho=1.0_dp/keff64
''')

replace_once('exact complete mirror list preflight before LCMGID',
             "  jpflux=LCMGID(kentry(1),'FLUX')\n",
             "  call require_record(kentry(1),'FLUX',ngrp,10,'AXIAL FLUX MIRROR')\n"
             "  jpflux=LCMGID(kentry(1),'FLUX')\n")
replace_once('mandatory complete REAL64 field and checked mirror',
'''  if (lr64) then
    call LCMLEN(kentry(1),'FLUX64',ilong,itylcm)
    if ((ilong /= ngrp).or.(itylcm /= 10)) &
      call XABORT('SPOSTATE64: MISSING FLUX64 LIST.')
    jpflux64=LCMGID(kentry(1),'FLUX64')
    allocate(unknown64(nunk,ngrp))
    do igr=1,ngrp
      call LCMLEL(jpflux64,igr,ilong,itylcm)
      if ((ilong /= nunk).or.(itylcm /= 4)) &
        call XABORT('SPOSTATE64: INVALID FLUX64 ITEM.')
      call LCMGDL(jpflux64,igr,unknown64(:,igr))
      do i=1,nunk
        if (transfer(real(unknown64(i,igr)),0) /= &
            transfer(mirror32(i,igr),0)) &
          call XABORT('SPOSTATE64: FLUX64 MIRROR MISMATCH.')
      enddo
    enddo
  endif
''',
'''  call LCMLEN(kentry(1),'FLUX64',ilong,itylcm)
  if ((ilong /= ngrp).or.(itylcm /= 10)) &
    call XABORT('SPOSTATE64: MISSING FLUX64 LIST.')
  jpflux64=LCMGID(kentry(1),'FLUX64')
  allocate(unknown64(nunk,ngrp))
  do igr=1,ngrp
    call LCMLEL(jpflux64,igr,ilong,itylcm)
    if ((ilong /= nunk).or.(itylcm /= 4)) &
      call XABORT('SPOSTATE64: INVALID FLUX64 ITEM.')
    call LCMGDL(jpflux64,igr,unknown64(:,igr))
    if (any(.not.ieee_is_finite(unknown64(:,igr)))) &
      call XABORT('SPOSTATE64: NON-FINITE REAL64 AXIAL FIELD.')
    do i=1,nunk
      if (transfer(real(unknown64(i,igr),real32),0_int32) /= &
          transfer(mirror32(i,igr),0_int32)) &
        call XABORT('SPOSTATE64: FLUX64 MIRROR MISMATCH.')
    enddo
  enddo
''')
replace_once('active scalar positivity uses REAL64 authority',
             '        if (mirror32(keyflx(ireg),igr) <= 0.0) &\n',
             '        if (unknown64(keyflx(ireg),igr) <= 0.0_dp) &\n')
replace_once('single global production norm uses REAL64 authority',
             '        real(mirror32(keyflx(ireg),igr),dp)*production\n',
             '        unknown64(keyflx(ireg),igr)*production\n')

leak_begin = source.index('  ! Reconstruct the signed plane leakage from this same axial field.\n')
leak_end = source.index('  if (any(.not.ieee_is_finite(leak))) &\n', leak_begin)
replace_once('full original signed REAL64 leakage, no binary32 branch',
             source[leak_begin:leak_end],
'''  ! Reconstruct the original signed leakage from the same REAL64 field.
  ! SPOLE1D promotes only the unchanged stored geometric measures.
  allocate(leak(ngrp*nsnap))
  allocate(phi64(nfloor,nreg2d),current64(nfloor+1,nreg2d))
  allocate(leak64(nsnap),num64(nsnap),den64(nsnap))
  do igr=1,ngrp
    do i=1,nreg2d
      do ifloor=1,nfloor
        ireg=(i-1)*nfloor+ifloor
        if (keyflx(ireg) > 0) then
          phi64(ifloor,i)=unknown64(keyflx(ireg),igr)
        else
          phi64(ifloor,i)=0.0_dp
        endif
      enddo
      do a=1,nfloor+1
        current64(a,i)=unknown64(ll4+(i-1)*(nfloor+1)+a,igr)
      enddo
    enddo
    call SPOLE1D(nreg2d,nfloor,nsnap,mat1d,dz,area,phi64, &
                 current64,leak64,num64,den64)
    do isnap=1,nsnap
      index=(isnap-1)*ngrp+igr
      leak(index)=leak64(isnap)
    enddo
  enddo
''')

replace_once('same volume restriction formula evaluated in REAL64',
'''        ! Match SPOPROJ's production restriction exactly: each product,
        ! accumulation, and division is performed in stored binary32 before
        ! the single global normalization and Gram projection.
        projected_sp=0.0
        weight_sp=0.0
        do ifloor=1,nfloor
          if (mat1d(ifloor) /= isnap) cycle
          ireg=(i-1)*nfloor+ifloor
          if (keyflx(ireg) <= 0) cycle
          projected_sp=projected_sp+volume(ireg)* &
            mirror32(keyflx(ireg),igr)
          weight_sp=weight_sp+volume(ireg)
        enddo
        if (weight_sp <= 0.0) &
          call XABORT('SPOSTATE64: EMPTY PLANE RESTRICTION.')
        projected_sp=projected_sp/weight_sp
        if ((.not.ieee_is_finite(projected_sp)).or. &
            (projected_sp <= 0.0)) &
          call XABORT('SPOSTATE64: INVALID PLANE RESTRICTION.')
        plane(i)=real(projected_sp,dp)/norm
''',
'''        ! Preserve the original volume restriction and floor order.
        ! Every product, sum and division uses the REAL64 authority.
        projected64=0.0_dp
        restriction_weight64=0.0_dp
        do ifloor=1,nfloor
          if (mat1d(ifloor) /= isnap) cycle
          ireg=(i-1)*nfloor+ifloor
          if (keyflx(ireg) <= 0) cycle
          projected64=projected64+real(volume(ireg),dp)* &
            unknown64(keyflx(ireg),igr)
          restriction_weight64=restriction_weight64+real(volume(ireg),dp)
        enddo
        if (restriction_weight64 <= 0.0_dp) &
          call XABORT('SPOSTATE64: EMPTY PLANE RESTRICTION.')
        projected64=projected64/restriction_weight64
        if ((.not.ieee_is_finite(projected64)).or. &
            (projected64 <= 0.0_dp)) &
          call XABORT('SPOSTATE64: INVALID PLANE RESTRICTION.')
        plane(i)=projected64/norm
''')
replace_once('always publish the admitted native REAL64 keff',
             "  if (lr64) call LCMPUT(kentry(1),'SPOT-X-KEFF',1,4,keff64)\n",
             "  call LCMPUT(kentry(1),'SPOT-X-KEFF',1,4,keff64)\n")
replace_once('release actual REAL64 leakage and authority arrays',
             '  deallocate(leak,denominator,numerator,leak_sp,current,phi)\n',
             '  deallocate(leak,den64,num64,leak64,current64,phi64,unknown64)\n')

candidate = source.encode('utf8')
reverse = source
for step in reversed(steps):
    if sha(reverse.encode('utf8')) != step['after_sha256']:
        raise ValueError('inverse step input differs: ' + step['label'])
    if step['mode'] == 'one_exact_local_byte_splice':
        position = step['byte_offset_in_step_input']
        raw = reverse.encode('utf8')
        new = step['new'].encode('utf8')
        if raw[position:position+len(new)] != new:
            raise ValueError('inverse local bytes differ: ' + step['label'])
        reverse = (raw[:position] + step['old'].encode('utf8') + raw[position+len(new):]).decode('utf8')
    else:
        pattern = r'\b' + re.escape(step['new']) + r'\b'
        if len(re.findall(pattern, reverse)) != step['occurrence_count']:
            raise ValueError('inverse token count differs: ' + step['label'])
        reverse = re.sub(pattern, step['old'], reverse)
    if sha(reverse.encode('utf8')) != step['before_sha256']:
        raise ValueError('inverse step output differs: ' + step['label'])
if reverse.encode('utf8') != original:
    raise ValueError('entire original Source not recovered by exact inverse')
original_renamed = re.sub(r'\bSPOSTATE\b', 'SPOSTATE64', original.decode('utf8'))
spd_before = original_renamed[original_renamed.index('  subroutine solve_spd('):]
spd_after = source[source.index('  subroutine solve_spd('):]
if spd_before != spd_after:
    raise ValueError('full original SPD algorithm changed')
for forbidden in ('lr64', 'projected_sp', 'weight_sp', 'real(mirror32', 'call SPOLE1('):
    if forbidden in source:
        raise ValueError('legacy numerical path retained: ' + forbidden)
if any(len(line) > 132 for line in candidate.splitlines()):
    raise ValueError('free-form Source line exceeds 132 bytes')

OUT.mkdir(exist_ok=True)
(OUT / 'read_only_original').mkdir(exist_ok=True)
original_copy = OUT / 'read_only_original/SPOSTATE.f90'
target = OUT / 'SPOSTATE64.f90'
for path, data in ((original_copy, original), (target, candidate)):
    with path.open('xb') as stream:
        stream.write(data)
saved_original = fullpin(original_copy)[1]
saved_candidate = fullpin(target)[1]
if saved_original['sha256'] != original_pin['sha256']:
    raise ValueError('saved complete original Source bytes differ')
protected_after = {str(p): fullpin(p)[1] for p in protected}
if protected_after != protected_before:
    raise ValueError('protected original/frozen Source changed')

proof_path = OUT / 'SPOSTATE64_TRANSFORM_LOCAL_BYTE_INVERSE_PROOF.json'
proof = dict(schema='SPOSTATE64_EXACT_COMPLETE_SOURCE_LOCAL_BYTE_TRANSFORM_INVERSE_V1',
             source_only=True, original_source=original_pin,
             original_exact_retained_copy=saved_original, candidate_source=saved_candidate,
             local_transform_count=len(steps), complete_local_transform_steps=steps,
             inverse_stepwise_before_after_sha_all_equal=True,
             complete_inverse_bytes_equal_original=True,
             untouched_original_SPD_body_exact_except_entry_diagnostic_rename=True,
             free_form_over132_line_count=0,
             Fortran_parser_or_compiler_executed=False,
             Native_or_numeric_executed=False)
with proof_path.open('x') as stream:
    json.dump(proof, stream, ensure_ascii=False, indent=2)
    stream.write('\n')

notes_path = OUT / 'SPOSTATE64_CHANGES_AND_REMAINING_SCOPE.txt'
notes = '''SPOSTATE64：完整新Source候选，不是旧源码同字节恢复或科学资格。
原SPOSTATE完整源码已保存；每项局部byte splice/rename及逐步SHA逆证保存于JSON。
保留原四参LCM ABI、所有signature/geometry/FIXB/basis/layout/offset/Gram/POD检查、全部输出record布局、原signed SPOLE1D算子、SPD算法与数值门槛。
FLUX64所有项/type4与SPOT-KEFF64/type4均mandatory，不能缺失或type2伪装；真实unknown64新增finite检查。原type2 FLUX/K为exactdemote镜像检查，仅用于mirror admission，不供norm、positivity、restriction、leakage或canonical state数值计算。
全局nu-fission norm、active scalar positivity、逐floor体积限制均从unknown64运算；静态VOLUME/AREA/VOL1D/NUSIGF/basis仍是原输入，在REAL64乘法/累加时精确提升。Gram/RHS/solve/offspace保持原公式与顺序。始终输出真实SPOT-X-KEFF。
新入口只形成canonical-state组件；不会生成GLOBAL64 producer认证、ROOT-QFISS64、native终态证据、epoch commit或实际BOOT，不能用本组件代替完整链。
当前不修改dispatcher、decks、任何original src或已编译冻结ROOT64两文件。仅完成实际Source文本/EOF身份/精确逆证检查；没有Fortran语法编译PASS，没有Native、controls、AAA/ABA资格。下一步Root真实original-guard编译后，继续原生GLOBAL64、三plane投影、真实QFISS/e0/BOOT/B2I接线，所有原门槛保留。
'''
with notes_path.open('x') as stream:
    stream.write(notes)
elapsed = time.monotonic() - START
peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
if os.uname().sysname != 'Darwin':
    peak *= 1024
if peak > 512 * 2**20 or elapsed > 600:
    raise ValueError('Source-only writer own resource bound exceeded')
manifest = dict(schema='SPOSTATE64_CURRENT_SOURCE_PINNED_DERIVATION_SCOPE_V1',
                scope='complete new canonical-state Source only',
                original_source=original_pin,
                original_exact_retained_copy=saved_original,
                candidate_source=saved_candidate,
                derivation_source=fullpin(Path(__file__).resolve())[1],
                exact_local_inverse_proof=fullpin(proof_path)[1],
                changes_and_remaining_scope=fullpin(notes_path)[1],
                actual_GANLIB_and_leakage_dependency_source_pins=dependency_pins,
                protected_Source_before=protected_before,
                protected_Source_after=protected_after,
                protected_Source_fullpins_unchanged=True,
                exact_complete_inverse_verified=True,
                own_elapsed_seconds=elapsed, own_peak_RSS_bytes=peak,
                compiler_or_parser_executed=False, Native_or_numeric_executed=False,
                original_thresholds_rank_material_unchanged=True,
                GLOBAL64_QFISS_BOOT_epoch_or_science_qualification=False)
manifest_path = OUT / 'SPOSTATE64_SOURCE_PINS_AND_SCOPE.json'
with manifest_path.open('x') as stream:
    json.dump(manifest, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
print(json.dumps(dict(candidate_source=saved_candidate,
                     exact_complete_inverse_verified=True,
                     local_transform_count=len(steps),
                     manifest=fullpin(manifest_path)[1],
                     protected_Source_fullpins_unchanged=True,
                     own_elapsed_seconds=elapsed, own_peak_RSS_bytes=peak,
                     compiler_or_parser_executed=False,
                     Native_or_numeric_executed=False), ensure_ascii=False))
