"""Independent finite stdlib source inspection; no business import/run/compile."""
import ast
import hashlib
import json
import pathlib
import re

B = pathlib.Path('/Users/wen/spot/validation/axial_material/sender_contiguous_flux_window_source_v13_20261009')
O = pathlib.Path('/private/tmp/axmat_v13_sender_incoming_fun_static_review_20261009')
K = pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009/SPOT1P64.f90')
pins = {}
checks = []

def must(value, note):
    if not value:
        raise AssertionError(note)
    checks.append(note)

def raw(p, sha=None):
    p = pathlib.Path(p)
    must(p.is_file() and not p.is_symlink() and p.stat().st_size < 200000, 'bounded regular source: ' + str(p))
    d = p.read_bytes()
    h = hashlib.sha256(d).hexdigest()
    if sha is not None:
        must(h == sha, 'expected exact source pin: ' + str(p))
    pins[str(p)] = dict(bytes=len(d), sha256=h)
    return d.decode('utf-8')

def fixed_statements(text):
    result = []
    for ln, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line[0] in '*cC!':
            continue
        must(len(line) >= 6, 'fixed-form statement prefix at source line ' + str(ln))
        fragment = line[6:].strip()
        if line[5] not in ' 0':
            must(bool(result), 'continuation has predecessor at source line ' + str(ln))
            result[-1]['text'] += fragment
            result[-1]['lines'].append(ln)
        else:
            result.append(dict(text=fragment, lines=[ln]))
    return result

def compact(value):
    return re.sub(r'\s+', '', value).upper()

def split_args(value):
    result = []; start = 0; depth = 0
    for i, char in enumerate(value):
        if char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char == ',' and depth == 0:
            result.append(value[start:i].strip()); start = i + 1
    must(depth == 0, 'balanced source argument parentheses')
    result.append(value[start:].strip())
    return result

meta = json.loads(raw(B / 'source_admission_INPUT.json'))
must(meta['source_only'] is True and all(meta[k] is False for k in
     ('compiled', 'controls_executed', 'native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted')),
     'source-only metadata has no compile/control/native/scientific credit')
helper = raw(meta['helper']['path'], '77c037a14a3852f628344d9a7cdee3b09e757b00420bf78eddcc1f3a17a6f163')
ast.parse(helper)
must(meta['helper']['sha256'] == pins[meta['helper']['path']]['sha256'], 'metadata owns exact helper')
candidate = raw(B / 'FLU2DR64.f', 'cd8e419c19f3a473beb6ded27705c513a07363a1a37e003c64266c5ef9cf5fb1')
old = raw(meta['original_sender']['path'], 'bb901bfed9a4199a5b4c98c58c93bf3b3dda597fd2047bfed6d267c8dcadac81')
receiver = raw(meta['original_receiver']['path'], '876eed542d97a368dd40e00ff92b1310cd106b03cbf766b618afda74f8566df2')
kernel = raw(K, '0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5')
unit = raw(B / 'FLUSP64.candidate_unit.f', 'e4f6beac894a62f9dc463b787bfe1d0b9673bc9eb8bebcef9470e3e7e885d2e3')
reference = raw(B / 'FLUSP64.original_reference_unit.f', '52b1db5a5ea73de548e437386798099cdb28b7c28cd98f0de21e949973266043')
proof = json.loads(raw(B / 'source_patch_proof.json', meta['proof']['sha256']))
start = candidate.index('      SUBROUTINE FLUSP64(')
must(candidate[start:] == unit, 'standalone candidate unit is exact actual sender trailing wrapper')
must(candidate[:start] == old[:old.index('      SUBROUTINE FLUSP64(')], 'complete outer sender caller/storage source byte-exact')
rs = fixed_statements(receiver)
us = fixed_statements(unit)
cs = fixed_statements(candidate)
reference_s = fixed_statements(reference)
header = next(x for x in rs if x['text'].upper().startswith('SUBROUTINE SPOF64('))
interface = next(x for x in us if x['text'].upper().startswith('SUBROUTINE SPOF64('))
must(compact(header['text']) == compact(interface['text']), 'private explicit interface exact13 formal parameter names/order')
expected_args = ['KPSYS','IPTRK','IMPX','NGEFF','NGIND','NREG','NMAT','NUN','MAT','KEYFLX','FUNKNO','SUNKNO','TITR']
must([compact(x) for x in split_args(header['text'].split('(',1)[1][:-1])] == expected_args,
     'original receiver parameter list independently parsed')
decls = ['INTEGERNGEFF,NGIND(NGEFF),IMPX,NREG,NMAT,NUN,MAT(NREG),KEYFLX(NREG)',
         'TYPE(C_PTR)KPSYS(NGEFF),IPTRK',
         'DOUBLEPRECISIONFUNKNO(NUN,NGEFF),SUNKNO(NUN,NGEFF)', 'CHARACTERTITR*72']
interface_span = unit[unit.index('      INTERFACE'):unit.index('      END INTERFACE')]
interface_s = fixed_statements(interface_span)
for declaration in decls:
    must(any(compact(x['text']) == declaration for x in rs), 'original receiver complete type/shape: ' + declaration)
    must(any(compact(x['text']) == declaration for x in interface_s), 'new interface complete type/shape: ' + declaration)
must('USEGANLIB' in [compact(x['text']) for x in interface_s], 'same GANLIB C_PTR type identity')
fun_mentions = [x for x in rs if re.search(r'\bFUNKNO\b', x['text'], re.I)]
must(len(fun_mentions) == 3 and fun_mentions[0] == header and
     compact(fun_mentions[1]['text']) == decls[2] and fun_mentions[2]['text'].upper().startswith('CALL SPOT1P64('),
     'complete executable SPOF64 FUNKNO mentions are header, declaration and sole output call')
spot_call = fun_mentions[2]
spot_args = split_args(spot_call['text'].split('(',1)[1][:-1])
must([compact(x) for x in spot_args[-3:]] == ['FUNKNO(1,II)','FUNKNO(LL4+1,II)','FUNKNO(LL4+LL5+1,II)'],
     'SPOF64 only forwards three original output-block starting addresses')
must([compact(x) for x in spot_args if 'FUNKNO' in x.upper()] == [compact(x) for x in spot_args[-3:]],
     'no output storage passed as receiver input/source argument')
kernel_start = kernel.index('subroutine SPOT1P64(')
kernel_end = kernel.index('end subroutine SPOT1P64', kernel_start)
kernel_body = kernel[kernel_start:kernel_end]
must('double precision, intent(out) :: flux(ielem,nsct,nfloor,nreg2d)' in kernel_body and
     'double precision, intent(out) :: cour(nfloor+1,nreg2d),xnei(npq,nreg2d)' in kernel_body,
     'actual inherited kernel declares all three receiver blocks INTENT(OUT)')
assign_pos = {}
for name in ('flux','cour','xnei'):
    matches = list(re.finditer(r'^\s*' + name + r'=0\.0\s*$', kernel_body, re.M))
    must(len(matches) == 1, 'one complete output-block zero initialization: ' + name)
    assign_pos[name] = matches[0].start()
    before = kernel_body[:matches[0].start()]
    mentions = [line for line in before.splitlines() if re.search(r'\b' + name + r'\b', line, re.I)
                and not line.lstrip().startswith('!') and "'" not in line]
    must(len(mentions) == 2 and ('radial2d,ncode,zcode,qext,du,w,pl,flux,cour,xnei)' in mentions[0]) and
         'intent(out)' in mentions[1], 'no incoming predefinition read of actual output block: ' + name)
all_calls = [x for x in cs if x['text'].upper().startswith('CALL FLUSP64(')]
must(len(all_calls) == 4, 'all four actual private sender callers found')
for call in all_calls:
    args = [compact(x) for x in split_args(call['text'].split('(',1)[1][:-1])]
    must(args[-3:] == ['FLUX(1,1,2)','FLUX(1,1,8)','FLUX(1,1,7)'], 'caller input/output are original planes2/8/7 at ' + str(call['lines']))
must(any('FLUX(NUNKNO,NGRP,8)' in compact(x['text']) and x['text'].upper().startswith('ALLOCATE(') for x in cs),
     'single original allocatable contiguous FLUX storage has eight explicit planes')
flux_alloc = [x for x in cs if x['text'].upper().startswith('ALLOCATE(') and 'FLUX(' in x['text'].upper()]
must(len(flux_alloc) == 1 and not any('EQUIVALENCE' in x['text'].upper() or
     ('POINTER' in x['text'].upper() and 'FLUX' in x['text'].upper()) for x in cs),
     'no FLUX EQUIVALENCE/pointer remapping; distinct plane regions for positive dimensions')
uc = [compact(x['text']) for x in us]
for statement in ('IF(NGEFF.EQ.0)RETURN', 'DIRECT_OUTPUT_WINDOW=(IGLAST-IGFIRST+1.EQ.NGEFF)',
                  'DOIG=1,NGRP','NGIND(JJ)=IG','ALLOCATE(KPSYS(NGEFF),NGIND(NGEFF),S2(NUN,NGEFF))',
                  'IF(.NOT.DIRECT_OUTPUT_WINDOW)ALLOCATE(F2(NUN,NGEFF))',
                  'S2(:NUN,JJ)=SUN(:NUN,IG)', 'F2(:NUN,JJ)=FUN(:NUN,IG)',
                  'CALLSPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,KEYFLX,FUN(1,NGIND(1)),S2,TITR)',
                  'CALLSPOF64(KPSYS,IPTRK,IMPX,NGEFF,NGIND,NREG,NMAT,NUN,MAT,KEYFLX,F2,S2,TITR)',
                  'FUN(:NUN,NGIND(JJ))=F2(:NUN,JJ)', 'IF(ALLOCATED(F2))DEALLOCATE(F2)',
                  'DEALLOCATE(S2,NGIND,KPSYS)'):
    must(statement in uc, 'expected direct-window/sparse fallback statement: ' + statement)
must(uc.index('IF(NGEFF.EQ.0)RETURN') < uc.index('ALLOCATE(KPSYS(NGEFF),NGIND(NGEFF),S2(NUN,NGEFF))'),
     'zero active groups return before allocation/indexing')
leak = 'S2(IND,JJ)=S2(IND,JJ)-DBLE(DIFHET(INM,IG))*DBLE(B2(4))*FLUOLD(IND,IG)'
must(leak in uc and leak in [compact(x['text']) for x in reference_s], 'entire original double leakage arithmetic exact')
must(unit.index('S2(:NUN,JJ)=SUN(:NUN,IG)') < unit.index('      IF(DIRECT_OUTPUT_WINDOW) THEN'),
     'all source/leakage gathering completed before any direct receiver writes')
must(not any('POINTER' in x['text'].upper() or 'TARGET' in x['text'].upper() or
     'INTENT(OUT)' in x['text'].upper() for x in us),
     'private FUN and receiver interface retain explicit shape without new pointer/target/output intent')
must(proof['observed_native_RSS_saving'] is None and all(proof[k] is False for k in
     ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')), 'source proof actual savings remains None and all qualificationsfalse')
report = dict(schema='AXMAT_V13_INDEPENDENT_INCOMING_FUN_STATIC_SOURCE_REVIEW_V1',
              classification='PASS_FINITE_STATIC_SOURCE_REVIEW_ONLY', defects=[], check_count=len(checks),
              raw_pins=pins, checks=checks,
              actual_receiver_fun_mentions=fun_mentions, actual_receiver_kernel_outputs=spot_args[-3:],
              actual_four_callers=all_calls,
              interface=dict(formals=expected_args, exact_types_shapes=decls, public_ABI_change=False),
              source_reasoning=[
                  'Active groups are scanned in ascending IG order. With nonempty set, last-first+1 == count iff there are no holes; NGIND(j)=first+j-1.',
                  'For positive entry NUN/NGRP, each FLUX plane spans P=NUNKNO*NGRP doubles. FLUOLD plane2=[P,2P), SUN plane8=[7P,8P), FUN plane7=[6P,7P), so the actual arguments do not overlap.',
                  'FUN explicit-shape dummy denotes one original contiguous plane. Passing scalar FUN(1,NGIND(1)) to explicit-shape FUNKNO(NUN,NGEFF) associates exactly the ascending column window, without pointer remapping or a vector-subscripted section.',
                  'SPOF64 has no incoming FUNKNO computation or input forwarding. Actual pinned SPOT1P64 receives three output blocks and initializes each whole block before any output read/accumulation.',
                  'Do not claim all NUN slots are overwritten. Slots outside three valid output blocks keep the original FUN bits; original F2 initialized them from FUN and scattered the same bits, while the direct path leaves them in place.',
                  'Inactive groups are untouched in both paths. The sparse branch retains original F2 gather, original receiver call and scatter; S2 gathering and ILEAK3 source subtraction remain exact.',
                  'Receiver NREG/NUN assignments from tracking STATE-VECTOR (lines96/97) remain original. Both paths use the same explicit-shape entry interface; this review assumes original valid consistent tracking dimensions and does not grant runtime validity for malformed inputs.',
                  'On a failed receiver call the direct path can leave partial FUN updates where the old F2 path had not scattered. This is deliberately limited to successful valid calls; failed direct state must not be reused.'],
              scope_limits=['No business/helper import or call, native/fixture execution, compilation, numerical payload reads, process polling, or project writes.',
                            'This is source reasoning, not an executed bitwise control or ABI/runtime proof. Root separately audits helper/inverse/outer ABI.',
                            'Fixed kernel pin0800cb is a dependency used to inspect output data flow; no old component/native success credit is transferred.',
                            'Observed RSS savings remain None; source-level conditional copy payload bytes are not a measured process RSS saving.'],
              controls_executed=False, compiled=False, actual_RSS_verified=False,
              AAA_accuracy_qualified=False, ABA_admitted=False)
O.mkdir(parents=True, exist_ok=True)
p = O / 'REPORT.json'
data = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
with p.open('xb') as stream:
    stream.write(data)
print(json.dumps(dict(classification=report['classification'], defects=[], check_count=len(checks),
                      report_path=str(p), report_sha256=hashlib.sha256(data).hexdigest(), report_bytes=len(data),
                      caller_count=4, planes=[2,8,7], original_receiver_pin=pins[meta['original_receiver']['path']]['sha256'],
                      incoming_FUN_not_read=True, residual_slots_preserved_on_success=True,
                      successful_valid_calls_only=True, controls_executed=False, compiled=False,
                      observed_native_RSS_saving=None, scientific_credit=False), sort_keys=True))
