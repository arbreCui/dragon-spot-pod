import hashlib
import json
import re
import time
from pathlib import Path

OUT = Path('/private/tmp/axmat_v11_cross_group_identity_key_source_independent_review_20261009')
SRC = Path('/private/tmp/axmat-rank1-cross-group-identity-key-delta-source-v11-20261009')
PARENT = Path('/Users/wen/spot/validation/axial_material/factor_diagonal_trim_source_v10_20261009/SPOT1P64.f90')
EXPECTED_PARENT = '5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809'
EXPECTED_NEW = '0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def ident(path):
    s = path.lstat()
    return dict(dev=s.st_dev, ino=s.st_ino, mode=s.st_mode, nlink=s.st_nlink,
                size=s.st_size, mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns)

def line(text, literal):
    assert literal in text, literal
    return text[:text.index(literal)].count('\n') + 1

def procedures(text):
    # Names are unique, including the original internal full-key builders.
    starts = re.finditer(r'^\s*(?:(?:logical|integer(?:\([^\n]*?\))?)\s+)?(subroutine|function)\s+(\w+)\s*\(', text, re.M | re.I)
    result = {}
    for m in starts:
        kind, name = m.group(1).lower(), m.group(2)
        assert name not in result, name
        end = re.search(r'^\s*end\s+' + kind + r'\s+' + re.escape(name) + r'\s*$', text[m.end():], re.M | re.I)
        assert end, name
        offset = m.end() + end.end()
        if offset < len(text) and text[offset] == '\n':
            offset += 1
        result[name] = text[m.start():offset]
    return result

started = time.monotonic()
paths = [PARENT, SRC/'SPOT1P64.f90', SRC/'region_edits.json', SRC/'source_inverse_proof.json', SRC/'source.diff', SRC/'generate_source_only.py']
before = {str(p): ident(p) for p in paths}
payloads = {str(p): p.read_bytes() for p in paths}
parent_b = payloads[str(PARENT)]
new_b = payloads[str(SRC/'SPOT1P64.f90')]
assert sha(parent_b) == EXPECTED_PARENT
assert sha(new_b) == EXPECTED_NEW
parent = parent_b.decode('utf-8')
new = new_b.decode('utf-8')
edits = json.loads(payloads[str(SRC/'region_edits.json')])
assert len(edits) == 6
rebuilt = parent
forward_checks = []
for e in edits:
    assert rebuilt.count(e['old']) == 1, e['name']
    rebuilt = rebuilt.replace(e['old'], e['new'], 1)
    forward_checks.append(dict(name=e['name'], old_sha256=sha(e['old'].encode()), new_sha256=sha(e['new'].encode())))
assert rebuilt.encode() == new_b
inverse = new
for e in reversed(edits):
    assert inverse.count(e['new']) == 1, e['name']
    inverse = inverse.replace(e['new'], e['old'], 1)
assert inverse.encode() == parent_b

old_procs = procedures(parent)
new_procs = procedures(new)
changed = ['SPOT1P64_CACHE_CLEAR', 'SPOT1P64_RANK1_GUARD']
assert set(old_procs).issubset(new_procs)
for name, body in old_procs.items():
    if name not in changed:
        assert new_procs[name] == body, name
added = sorted(set(new_procs) - set(old_procs))
assert len(added) == 9, added
for name in added:
    # The added codec has no floating variables/arithmetic, FP solver calls,
    # key conversion, business calls, random state or external I/O.
    body = new_procs[name]
    assert not re.search(r'\b(?:real|double\s+precision|matmul|transfer|factor64|solve64|ieee_is_finite)\b', body, re.I), name
    assert not re.search(r'^\s*(?:write|read|open|close)\s*\(', body, re.M | re.I), name

guard_old = old_procs['SPOT1P64_RANK1_GUARD']
guard_new = new_procs['SPOT1P64_RANK1_GUARD']
assert guard_old[:guard_old.index('      if (phase == 1) then')] == guard_new[:guard_new.index('      if (phase == 1) then')]
assert guard_old[guard_old.index('      else\n        call XABORT(\'SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.'):] == guard_new[guard_new.index('      else\n        call XABORT(\'SPOT1P64 RANK1 CACHE: INVALID IDENTITY PHASE.'):]
for name in ['SPOT1P64_RANK1_KEY_STATS', 'SPOT1P64_RANK1_KEY_LOAD', 'SPOT1P64_RANK1_KEY_LOAD_DATA', 'SPOT1P64_RANK1_KEY_CHECK_DATA', 'SPOT1P64_RANK1_KEY_VALIDATE_DATA', 'SPOT1P64_RANK1_KEY_BASE_VALIDATE']:
    body = new_procs[name]
    assert not re.search(r'^\s*(?:allocate|deallocate|call\s+SPOT1P64_RANK1_RESERVE|call\s+SPOT1P64_RANK1_RELEASE)\b', body, re.M | re.I), name

save = new_procs['SPOT1P64_RANK1_KEY_SAVE_DATA']
assert save.index('call SPOT1P64_RANK1_RESERVE(amount)') < save.index('allocate(bits(d),positions(d))')
fallback = save[save.index('    else\n      amount=8_int64*size(key,kind=int64)'):]
assert fallback.index('call SPOT1P64_RANK1_RESERVE(amount)') < fallback.index('allocate(bits(size(key)))')
assert 'use_delta=12_int64*int(d,int64) < 8_int64*size(key,kind=int64)' in save
assert 'positions(k)=int(i,int32)' in save and 'bits(k)=key(i)' in save
assert save.index('if (present(base)) then') < save.index('if (size(base) == size(key)) then') < save.index('if (key(i) /= base(i)) d=d+1')
validate = new_procs['SPOT1P64_RANK1_KEY_VALIDATE_DATA']
assert validate.index('if (.not.allocated(bits))') < validate.index('if (size(bits,kind=int64) /= nkey)')
assert validate.index('if (.not.present(base))') < validate.index('size(base,kind=int64)')
assert validate.index('if (size(base,kind=int64) /= nkey .or. size(bits) /= size(positions))') < validate.index('do k=1,size(positions)')
assert validate.index('if (p <= previous .or. int(p,int64) > nkey)') < validate.index('if (bits(k) == base(p))')
assert 'if (12_int64*size(bits,kind=int64) >= 8_int64*nkey)' in validate
check = new_procs['SPOT1P64_RANK1_KEY_CHECK_DATA']
assert check.index('call SPOT1P64_RANK1_KEY_VALIDATE_DATA') < check.index('do i=1,size(key)')
assert check.index('if (k <= size(positions)) then') < check.index('p=int(positions(k))')
assert 'if (expected /= key(i))' in check
load = new_procs['SPOT1P64_RANK1_KEY_LOAD_DATA']
assert load.index('call SPOT1P64_RANK1_KEY_VALIDATE_DATA') < load.index('key=base')
assert 'key(int(positions(k)))=bits(k)' in load and 'key=bits' in load
assert new.count('deallocate(SPOT1P64_PLAN)') == parent.count('deallocate(SPOT1P64_PLAN)') == 1
assert 'rank1_raw_base_owner=0\n    rank1_operator_base_owner=0' in new_procs['SPOT1P64_CACHE_CLEAR']
assert new.count('rank1_raw_base_owner=igroup') == new.count('rank1_operator_base_owner=igroup') == 1
for literal in ['integer(int64), parameter :: RANK1_CAP=536870912_int64', 'integer(int64), parameter :: RANK1_DESCRIPTOR_PER_GROUP=4096_int64', 'if (ngroup > 370)', 'if (.not.allocated(plan%rank1_raw_bits))', 'if (plan%ready) rank1_validated_hits=rank1_validated_hits+1_int64']:
    assert literal in parent and literal in new

after = {str(p): ident(p) for p in paths}
assert before == after
pins = [{ 'path': str(p), 'sha256': sha(payloads[str(p)]), 'identity': before[str(p)] } for p in paths]
report = dict(
    schema='axmat_v11_cross_group_identity_key_source_independent_review_v1',
    status='PASS_SOURCE_CONTRACT_ONLY',
    candidate_sha256=EXPECTED_NEW, parent_sha256=EXPECTED_PARENT,
    complete_six_region_inverse_byteexact=True,
    regions=forward_checks,
    parent_procedure_count=len(old_procs), candidate_procedure_count=len(new_procs),
    changed_original_procedures=changed, added_integer_only_procedures=added,
    all_other_original_procedure_bodies_byteexact=True,
    original_complete_temporary_keys_and_FP_and_boundary_bodies_byteexact=True,
    original_eligibility_phase_order_and_missing_raw_and_validated_hits_order_retained=True,
    source_pins=pins, all_source_seven_identities_before_after_equal=True,
    source_reasoning=[
      'Raw/operator use separate phase-global first-full owner indices. New owner is set only after a successful full allocation/copy. No second full anchor allocation exists.',
      'Plan bits is either original full int64 key or difference values. Allocated positions, including zero length, selects delta; zero difference bits remains allocated, preserving the original phase2 raw-existence gate.',
      'Optional base is forwarded only to optional dummy arguments. Full-format validation returns without touching an absent base. Delta branches validate base presence and full shape before use. This relies on the original fatal XABORT contract, not Fortran logical short-circuit behavior.',
      'Base owner index/mode shape/allocation/full format is validated before plan indexing and optional assumed-shape base passage. The source keeps base arrays unmodified until whole CACHE_CLEAR.',
      'Delta lengths, strict byte benefit, ascending unique positive positions, bounds, and value difference from base are validated before indexed reads or writes. CAP/8 bounds nkey to 67108864, below signed int32/default32 integer maximum.',
      'Key SAVE counts every int64 word against same-size full base. Compression requires strict 12*ndiff < 8*nkey; absent/different-size base or equality/larger cost uses the original full allocation/copy.',
      'Every MATCH loops over every complete current key word, selecting full/base/difference expected int64 words. Signed-zero and floating bit payloads remain integer comparisons; no hash or shortened semantic identity exists.',
      'All byte products use int64 operands before multiplication. The delta/full allocation is preceded by RESERVE for exact persistent data bytes. No decode allocation or extra full-key buffer is introduced.',
      'Only whole CACHE_CLEAR deallocates the plan. It resets both phase owner indices. CACHE_BEGIN invokes the original CLEAR, so no owner survives a lifecycle change.',
      'KEY_LOAD writes only caller output after complete shape/canonical gates, without changing plan/accounting. KEY_STATS observes stored metadata/count/phase base owner without validating corruption or granting a cache hit.',
      'The public SPOT1P64_PLAN is an inherited control mutation surface, not a tamper-resistant archive. Internal production code never mutates the anchor after storage. Arbitrary external writes to otherwise well-formed full anchor data are not independently authenticated by this representation.',
    ],
    line_evidence={s: line(new,s) for s in [
      'integer(int64) :: rank1_raw_size', 'rank1_raw_base_owner=0\n    rank1_operator_base_owner=0',
      'subroutine SPOT1P64_RANK1_KEY_STATS(', 'subroutine SPOT1P64_RANK1_KEY_BASE_VALIDATE(',
      'subroutine SPOT1P64_RANK1_KEY_VALIDATE_DATA(', 'subroutine SPOT1P64_RANK1_KEY_SAVE_DATA(',
      'subroutine SPOT1P64_RANK1_KEY_STORE(', 'subroutine SPOT1P64_RANK1_KEY_CHECK_DATA(',
      'subroutine SPOT1P64_RANK1_KEY_MATCH(', 'subroutine SPOT1P64_RANK1_KEY_LOAD_DATA(',
      'subroutine SPOT1P64_RANK1_KEY_LOAD(']},
    required_actual_followups=[
      'Compile the unchanged production ABI/compiler and verify actual aggregate group/mode descriptor+scalar storage still fits the original 4096 bytes/group allowance. Source review does not measure ABI descriptor sizes.',
      'Actual codec controls: zero/one/all differences; nkey zero/one; strict benefit equality; unequal dimensions; both phase owners and clear/begin; full key equality/signed-zero bits; malformed size/missing base/delta base/noncanonical equal value/positions order/duplicate/out-of-range/length.',
      'Original full physics/build/hit controls must keep their scope. KEY_STATS owner means the phase first-full anchor, including when a group has an independent full fallback; it is not necessarily that full array owner.',
      'Measure real production difference counts and separate accounted/live bytes from own-PID ps RSS under unchanged 512 MiB. Source PASS grants no actual memory benefit or AAA/ABA/native qualification.',
    ],
    actual_compile=None, actual_codec_controls=None, actual_native_RSS=None,
    actual_native_AAA=None, actual_native_ABA=None, actual_business_executed=False,
    project_written=False, elapsed_seconds=time.monotonic()-started)
with (OUT/'REPORT.json').open('x') as f:
    json.dump(report,f,indent=2,allow_nan=False)
    f.write('\n')
with (OUT/'REPORT.txt').open('x') as f:
    f.write('V11 rank1 跨群身份键差异压缩：独立源码合同审查通过。\n'
            '六处编辑完整逆向为 5e0d 母本；原完整临时键、浮点计算、边界求解及其余原过程逐字保留。\n'
            '严格完整键比较、12*d<8*n 回退、零差异 allocated(0)、独立 phase owner、全生命周期清理及分配前记账未见源码阻断。\n'
            'KEY_LOAD 仅写调用者输出；KEY_STATS 仅观察，其 owner 是 phase 基准 owner。\n'
            '尚未编译或运行 codec/业务；4096B 每组 ABI 实占、实际差异数量与 RSS 收益仍待真实检查，不能授予 native/AAA/ABA 信用。\n')
print(json.dumps(dict(status=report['status'], report_sha256=sha((OUT/'REPORT.json').read_bytes()), parent_procedures=len(old_procs), new_procedures=len(new_procs), source_files=len(pins)),allow_nan=False))
