"""STDlib source transformation only; does not import/execute project code."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

ROOT=Path('/Users/wen/spot')
D=Path('/private/tmp/axmat_v11_full_component_factory_source_draft_20261009')
M=ROOT/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_factor_diagonal_trim_production.py'
OUT=D/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py'
original=M.read_text(); code=original; edits=[]
def sha(v): return hashlib.sha256(v if isinstance(v,bytes) else v.encode()).hexdigest()
def change(label,before,after):
    global code
    if code.count(before)!=1: raise AssertionError((label,code.count(before)))
    code=code.replace(before,after,1)
    edits.append(dict(label=label,before=before,after=after,before_sha256=sha(before),after_sha256=sha(after)))
def function(name,transform):
    tree=ast.parse(code)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    lines=code.splitlines(True);before=''.join(lines[node.lineno-1:node.end_lineno])
    after=transform(before)
    change('function:'+name,before,after)
def sub(s,a,b,count=1):
    if s.count(a)!=count: raise AssertionError((a[:100],s.count(a),count))
    return s.replace(a,b)

change('module_docstring',ast.get_source_segment(original,ast.parse(original).body[0]),'''"""Source-only complete V11 cross-group integer identity storage component.

The original 45 stages, dense c017 comparisons, all physical inputs and thresholds
remain compulsory. Two driver build stages and 21 independently audited keycodec
stages are additional. Expected persistent fees derive from archived original
dense full keys, never from candidate compressed output. No native RSS, AAA or ABA
qualification follows from component controls. Root's actual terminal is external.
This draft cannot execute until its complete source admission is reviewed.
"""''')
for old,new in (
('axial-material-qualified-AB-rank1-factor-cache-factor-diagonal-trim-build-admission-20261009','axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009'),
('axial-material-rank1-factor-cache-factor-diagonal-trim-build-20261009','axial-material-rank1-factor-cache-cross-group-identity-key-delta-build-v11-20261009'),
('axial-material-qualified-AB-rank1-factor-cache-factor-diagonal-trim-build-terminal-20261009','axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-terminal-v11-20261009'),
('PATCH_HELPER = ROOT / "validation/axial_material/rank1_factor_cache_factor_diagonal_trim_patch.py"','PATCH_HELPER = ROOT / "validation/axial_material/rank1_factor_cache_cross_group_identity_key_delta_patch.py"'),
('CONTROL_SOURCE = ROOT / "validation/axial_material/rank1_factor_cache_factor_diagonal_trim_controls.f90"','CONTROL_SOURCE = ROOT / "validation/axial_material/rank1_factor_cache_cross_group_identity_key_delta_controls.f90"'),
('FAMILY = "RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_BUILD"','FAMILY = "RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD_V11"'),
('SOURCE_STATUS = "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_COMPONENT_EXECUTION"','SOURCE_STATUS = "UNREADY"'),
('PATCH_HELPER_SHA = "d849ebbbe4dd7e59b17bd67e60a07f950aa7a2fc33f22011431c83c46cff1b6e"','PATCH_HELPER_SHA = "733855513a81ead79f797dc0843b061f1604ab61b6db9684613a06a067387300"'),
('CONTROL_SOURCE_SHA = "82b19974518f44952f829ef388a9b5fdbf58e2b4b7df2d7f7d61f7839038def4"','CONTROL_SOURCE_SHA = "eab3a7790e9f499282017cc37581be5acb07f8a4170e8fcaae95b0de47305d52"')):
    change('identity:'+old,old,new)
# Retarget only this family's schemas; immutable predecessor schemas are untouched.
for schema in sorted(set(__import__('re').findall(r'AXMAT_RANK1_FACTOR_CACHE_FACTOR_DIAGONAL_TRIM_[A-Z_0-9]+',code))):
    before=code
    replacement=schema.replace('FACTOR_DIAGONAL_TRIM','CROSS_GROUP_IDENTITY_KEY_DELTA')
    # Whole text replacements have multiple exact schema consumers; record one whole
    # region to retain a complete, deterministic inverse rather than a regex undo.
    positions=[i for i in range(len(code)) if code.startswith(schema,i)]
    for index in reversed(positions):
        prefix=code[max(0,index-36):index]; suffix=code[index+len(schema):index+len(schema)+36]
        change('schema:'+schema,prefix+schema+suffix,prefix+replacement+suffix)

new_constants='''
V10_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_rank1_factor_cache_factor_diagonal_trim_production.py"
V10_FACTORY_SHA = "__V10_SHA__"
V10_CONTROL_SOURCE = ROOT / "validation/axial_material/rank1_factor_cache_factor_diagonal_trim_controls.f90"
V10_CONTROL_SOURCE_SHA = "82b19974518f44952f829ef388a9b5fdbf58e2b4b7df2d7f7d61f7839038def4"
V10_PATCH_HELPER = ROOT / "validation/axial_material/rank1_factor_cache_factor_diagonal_trim_patch.py"
V10_PATCH_HELPER_SHA = "d849ebbbe4dd7e59b17bd67e60a07f950aa7a2fc33f22011431c83c46cff1b6e"
IDENTITY_KERNEL_SOURCE = ROOT / "validation/axial_material/identity_key_delta_source_v11_20261009/SPOT1P64.f90"
IDENTITY_KERNEL_SHA = "0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5"
IDENTITY_CONTRACT = ROOT / "validation/axial_material/identity_key_delta_source_v11_20261009/component_source_extension/identity_key_delta_contract.json"
IDENTITY_CONTRACT_SHA = "__CONTRACT_SHA__"
IDENTITY_SOURCE_ADMISSION = ROOT / "validation/axial_material/identity_key_delta_source_v11_20261009/Root_complete_component_source_extension_admission.json"
IDENTITY_SOURCE_ADMISSION_SHA = "cbe2ab7e81073ac1d8e65d3aad377deba986c2e88342c7e7d9e41174def00832"
KEYCODEC_CONTROL_SOURCE = ROOT / "validation/axial_material/identity_key_delta_source_v11_20261009/keycodec_controls.f90"
KEYCODEC_CONTROL_SHA = "3f59d94d49c049b206419b49c3a3ac437aa3d980548ab8fb27632ba4dfd472f7"
KEYCODEC_AUDITOR = ROOT / "validation/axial_material/rank1_cross_group_identity_key_codec_controls_audit.py"
KEYCODEC_AUDITOR_SHA = "8ecf321ed137de883160dade3b33f95765d5e5e71c54747ef2e49de8bd150903"
PRIMITIVE_ABI_REVIEW = ROOT / "validation/axial_material/identity_key_delta_codec_review_v11_20261009/independent_raw_review/REPORT.json"
PRIMITIVE_ABI_REVIEW_SHA = "7caee2f7e52180aa8d26f864168dab01e1aeb633d79349cabdb25b9fa40e8ce1"
KEYCODEC_MUTATIONS = ('unchanged_word','difference_word','stored_difference_word','base_word',
    'input_length','load_length','ineligible_existing','corrupt_index_zero','corrupt_index_high','missing_anchor')
KEYCODEC_CASES = tuple(dict(name=mutation+'_p'+str(phase),args=['negative',mutation,str(phase)],
    expected_returncode=23,expected_message='SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.')
    for phase in (1,2) for mutation in KEYCODEC_MUTATIONS)
KEYCODEC_RAW_BINARY_BYTES = 70792
KEYCODEC_JSONL_BYTES = 26930
KEYCODEC_ABORT_BYTES = 1000
KEYCODEC_MANIFEST_ROWS = 213  # 33 positive + 20 * 9 negative JSONL rows.
FUTURE_ACTUAL_BUILD_TERMINAL_SHA = None
FUTURE_ACTUAL_BUILD_SEAL_SHA = None
FUTURE_ACTUAL_NATIVE_TERMINAL_SHA = None
'''.replace('__V10_SHA__',sha(original)).replace('__CONTRACT_SHA__',sha((ROOT/'validation/axial_material/identity_key_delta_source_v11_20261009/component_source_extension/identity_key_delta_contract.json').read_bytes()))
change('new_constant_inventory','\ndef require_ready():',new_constants+'\ndef require_ready():')
function('require_ready',lambda s:sub(s,'(PATCH_HELPER_SHA, CONTROL_SOURCE_SHA)','(PATCH_HELPER_SHA, CONTROL_SOURCE_SHA, KEYCODEC_AUDITOR_SHA)'))
function('source_inputs',lambda s:sub(s,'        FACTOR_CODEC_PLAN:FACTOR_CODEC_PLAN_SHA}',
'''        FACTOR_CODEC_PLAN:FACTOR_CODEC_PLAN_SHA,
        V10_FACTORY:V10_FACTORY_SHA,V10_CONTROL_SOURCE:V10_CONTROL_SOURCE_SHA,V10_PATCH_HELPER:V10_PATCH_HELPER_SHA,
        IDENTITY_KERNEL_SOURCE:IDENTITY_KERNEL_SHA,IDENTITY_CONTRACT:IDENTITY_CONTRACT_SHA,
        IDENTITY_SOURCE_ADMISSION:IDENTITY_SOURCE_ADMISSION_SHA,
        KEYCODEC_CONTROL_SOURCE:KEYCODEC_CONTROL_SHA,KEYCODEC_AUDITOR:KEYCODEC_AUDITOR_SHA,
        PRIMITIVE_ABI_REVIEW:PRIMITIVE_ABI_REVIEW_SHA}'''))

def patch_admission(s):
    s=sub(s,'c["experiment"] = "rank1-factor-cache-factor-diagonal-trim-20261009"','c["experiment"] = "rank1-factor-cache-cross-group-identity-key-delta-v11-20261009"')
    s=sub(s,'    changed = patch.patch_kernel(source)','''    changed = patch.patch_kernel(source)
    composed_proof = copy.deepcopy(changed['proof'])
    identity = composed_proof['cross_group_identity_key_delta']
    inverse_v10 = changed['kernel']
    for edit in reversed(identity['edits']):
        if inverse_v10.count(edit['new']) != 1:
            raise ValueError('identity patch region not uniquely invertible')
        inverse_v10 = inverse_v10.replace(edit['new'],edit['old'],1)
    if (composed_proof['inherited_v10_complete_proof'] != read(require(COMPLETE_C0_FACTOR_PROOF,COMPLETE_C0_FACTOR_PROOF_SHA))
            or inverse_v10.encode() != require(FACTOR_DIAGONAL_SOURCE,FACTOR_DIAGONAL_KERNEL_SHA).read_bytes()
            or changed['kernel'].encode() != require(IDENTITY_KERNEL_SOURCE,IDENTITY_KERNEL_SHA).read_bytes()
            or composed_proof['candidate_kernel_sha256'] != IDENTITY_KERNEL_SHA
            or composed_proof['scope'] != 'ORDINARY_RANK1_LOWER_DICTIONARY_TERMINAL_CPRIME_DEAD_FACTOR_DIAGONAL_AND_CROSS_GROUP_INTEGER_IDENTITY_STORAGE_ONLY'
            or composed_proof['complete_inverse_byteexact'] is not True):
        raise ValueError('entire original V10 proof and complete c0 inverse must survive new integer key storage')''')
    s=sub(s,'    memory = patch.control_contract()','''    memory = copy.deepcopy(patch.control_contract())
    identity_contract = memory.pop('cross_group_identity_key_delta')
    if identity_contract != read(require(IDENTITY_CONTRACT,IDENTITY_CONTRACT_SHA)):
        raise ValueError('complete independent identity storage contract differs')
    c['cross_group_identity_key_delta'] = identity_contract
    c['inherited_factor_diagonal_key_accounting_description'] = c['key_accounting']
    c['key_accounting'] += ' V11 changes only retained raw/projected integer key fees to full8*n or strict12*ndiff, based on first same-size complete c017 dense keys per phase; full temporary8*n, FACTORS/LOWER/PACK coexisting allocations, all counters and all old arithmetic remain required.'
    c['keycodec_positive_command_args'] = ['positive']
    c['keycodec_negative_cases'] = copy.deepcopy(list(KEYCODEC_CASES))
    c['original45_required'] = True
    c['total_planned_stage_count'] = 68
    abi=read(require(PRIMITIVE_ABI_REVIEW,PRIMITIVE_ABI_REVIEW_SHA))
    dims=abi['actual_descriptor_bytes']
    if (abi['status']!='PASS_PRIMITIVE_CODEC_ONLY' or any(type(dims[k]) is not int or dims[k]<=0 for k in ('mode','group'))
            or dims['mode']+dims['group']>4096 or abi['original45_controls_completed'] is not False
            or not any(item['sha256']==IDENTITY_KERNEL_SHA and Path(item['path']).name=='SPOT1P64.f90' for item in abi['source_pins'])):
        raise ValueError('real identical-source ABI descriptor witness must fit existing4096, without replacing full controls')
    c['identity_descriptor_abi_witness']=dict(review=pin(PRIMITIVE_ABI_REVIEW),descriptor_bytes=dims,
        applies_to_identical_candidate_source=True,does_not_replace_new68_stages=True)''')
    s=sub(s,'codec["controls_source"] != pin(CONTROL_SOURCE)','codec["controls_source"] != pin(require(V10_CONTROL_SOURCE,V10_CONTROL_SOURCE_SHA))')
    s=sub(s,"    proof=changed[\"proof\"]","    proof=composed_proof['inherited_v10_complete_proof']")
    s=sub(s,'hashlib.sha256(changed["kernel"].encode()).hexdigest()!=FACTOR_DIAGONAL_KERNEL_SHA','hashlib.sha256(inverse_v10.encode()).hexdigest()!=FACTOR_DIAGONAL_KERNEL_SHA')
    s=sub(s,'changed["kernel"].encode()!=require(FACTOR_DIAGONAL_SOURCE,FACTOR_DIAGONAL_KERNEL_SHA).read_bytes()','inverse_v10.encode()!=require(FACTOR_DIAGONAL_SOURCE,FACTOR_DIAGONAL_KERNEL_SHA).read_bytes()')
    s=sub(s,'        proof=proof,dense_reference_proof=', '        proof=composed_proof,dense_reference_proof=')
    return s
function('patch_admission',patch_admission)
function('codec_controls_audit',lambda s:sub(s,"plan['controls_source']!=pin(CONTROL_SOURCE)","plan['controls_source']!=pin(require(V10_CONTROL_SOURCE,V10_CONTROL_SOURCE_SHA))"))

def cache_accounting(s):
    s=sub(s,'def cache_accounting(fixture,nmat=3,unique_count=None):','def cache_accounting(fixture,nmat=3,unique_count=None,identity_cost=None):')
    s=sub(s,'    factors=prepack-dead','''    factors=prepack-dead
    raw_stored,operator_stored=raw*8,projected*8
    if identity_cost is not None:
        if not ordinary_rank1 or type(identity_cost) is not dict or set(identity_cost)!={'raw','operator'}:
            raise ValueError('independent complete dense identity fee requires ordinary rank1')
        raw_stored,operator_stored=identity_cost['raw'],identity_cost['operator']
        if any(type(x) is not int or x<0 for x in (raw_stored,operator_stored)) or raw_stored>raw*8 or operator_stored>projected*8:
            raise ValueError('independent stored key cost outside lossless full fallback bound')''')
    s=sub(s,'factor_bytes_per_group=factors,persistent_bytes_per_group=(raw+projected)*8+factors,','factor_bytes_per_group=factors,persistent_bytes_per_group=raw_stored+operator_stored+factors,')
    s=sub(s,"final_retained_bytes=fixture['groups']*(4096+(raw+projected)*8+factors)","final_retained_bytes=fixture['groups']*(4096+raw_stored+operator_stored+factors)")
    s=sub(s,'reservation_peak_is_not_actual_RSS=True)','stored_raw_key_bytes=raw_stored,stored_projected_key_bytes=operator_stored,\n        full_temporary_key_bytes_unchanged=True,reservation_peak_is_not_actual_RSS=True)')
    return s
function('cache_accounting',cache_accounting)
def counters(s):
    s=sub(s,'def check_counters(record, state, fixture, update, unique_count=None):','def check_counters(record, state, fixture, update, unique_count=None,identity_cost=None):')
    s=sub(s,'account = cache_accounting(fixture,unique_count=unique_count)','account = cache_accounting(fixture,unique_count=unique_count,identity_cost=identity_cost)')
    s=sub(s,'first = before+2*account["raw_key_bytes"]','first = before+account["raw_key_bytes"]+account["stored_raw_key_bytes"]')
    s=sub(s,'second = before+account["raw_key_bytes"]+2*account["projected_key_bytes"]','second = before+account["stored_raw_key_bytes"]+account["projected_key_bytes"]+account["stored_projected_key_bytes"]')
    s=sub(s,'before+account["raw_key_bytes"]+account["projected_key_bytes"]+account["worst_factor_reservation_bytes_per_group"]','before+account["stored_raw_key_bytes"]+account["stored_projected_key_bytes"]+account["worst_factor_reservation_bytes_per_group"]')
    s=sub(s,'before+account["raw_key_bytes"]+account["projected_key_bytes"]+\\','before+account["stored_raw_key_bytes"]+account["stored_projected_key_bytes"]+\\')
    return s
function('check_counters',counters)

new_functions='''
def independent_key_encoding(full,base,is_owner):
    """Integer byte model from c017 only; never consumes candidate encoding."""
    if type(full) is not bytes or type(base) is not bytes or len(full)%8 or len(base)%8:
        raise ValueError('complete original identity keys must be integer64 bytes')
    positions=tuple(index+1 for index in range(len(full)//8)
        if full[8*index:8*index+8]!=base[8*index:8*index+8]) if len(full)==len(base) else ()
    compressed=not is_owner and len(full)==len(base) and 12*len(positions)<len(full)
    values=b''.join(full[8*(p-1):8*p] for p in positions) if compressed else full
    indices=struct.pack('<'+str(len(positions))+'i',*positions) if compressed else b''
    return dict(compressed=compressed,words=len(values)//8,positions=len(indices)//4,
        values=values,indices=indices,cost=len(values)+len(indices))


def dense_identity_record(folder,stem,fixture,group,expected_stats):
    raw=control_file(folder,stem+'_dense_keys.bin').read_bytes()
    a=cache_accounting(fixture);nr,no=a['raw_key_bytes']//8,a['projected_key_bytes']//8
    header=(1,group,1,nr,no,*expected_stats,0)
    if len(raw)!=96+8*(nr+no) or struct.unpack('<12q',raw[:96])!=header:
        raise ValueError('c017 original full integer keys/header/EOF differ')
    return (raw[96:96+8*nr],raw[96+8*nr:])


def candidate_identity_record(folder,stem,fixture,group,original_keys,base_keys,expected_stats):
    raw=control_file(folder,stem+'_identity_keys.bin').read_bytes();cursor=0;cost={};encoded_bytes=0
    for phase,(full,base) in enumerate(zip(original_keys,base_keys),1):
        expected=independent_key_encoding(full,base,group==1)
        n=len(full)//8;bn=len(base)//8
        header=(1,group,phase,1,n,int(expected['compressed']),expected['words'],expected['positions'],bn,*expected_stats,0)
        if len(raw)-cursor<128 or struct.unpack('<16q',raw[cursor:cursor+128])!=header:
            raise ValueError('candidate identity canonical owner/shape/format or counters differ from independent c017')
        cursor+=128
        wanted=expected['values']+expected['indices']+base+full
        if raw[cursor:cursor+len(wanted)]!=wanted:
            raise ValueError('actual stored full/delta words/indices/base/KEY_LOAD are not byte-exact original c017 keys')
        cursor+=len(wanted);encoded_bytes+=expected['cost']
        cost['raw' if phase==1 else 'operator']=expected['cost']
    if cursor!=len(raw):raise ValueError('candidate identity raw trailing/missing bytes')
    return cost,encoded_bytes


def prime_identity_record(folder,stem,fixture,prime):
    """Group1 must store full keys. Original fourteen mutation gates remain.

    No dense negative key file exists: the standalone two-phase codec controls
    plus original production-shape mutation guards are independent obligations.
    This parser does not claim an external dense-byte baseline for these14 primes.
    """
    raw=control_file(folder,stem+'_identity_keys.bin').read_bytes();cursor=0;a=cache_accounting(fixture)
    stats=tuple(prime[k] for k in ('built','reused','hits','live','peak','cap'))
    for phase,n in ((1,a['raw_key_bytes']//8),(2,a['projected_key_bytes']//8)):
        header=(1,1,phase,1,n,0,n,0,n,*stats,0)
        if len(raw)-cursor<128 or struct.unpack('<16q',raw[cursor:cursor+128])!=header:
            raise ValueError('first-group negative priming full keys/owner/shape/counters differ')
        cursor+=128;full=raw[cursor:cursor+8*n];cursor+=8*n
        if len(full)!=8*n or raw[cursor:cursor+16*n]!=full+full:
            raise ValueError('full negative prime stored/base/decoded byte representation differs')
        cursor+=16*n
    if cursor!=len(raw):raise ValueError('negative identity prime whole EOF differs')
    return dict(kind='candidate_identity_keys',case=stem.split('_g')[0],group=1,file=stem+'_identity_keys.bin',phases=[1,2])


def keycodec_controls_audit(d):
    require(KEYCODEC_AUDITOR,KEYCODEC_AUDITOR_SHA)
    module=load(KEYCODEC_AUDITOR,'rank1_cross_group_identity_key_codec_controls_audit')
    result=module.audit_keycodec_controls(OUT/'controls')
    if (result['actual_codec_controls_passed'] is not True or result['raw_binary_bytes']!=KEYCODEC_RAW_BINARY_BYTES
            or result['raw_manifest_jsonl_bytes']!=KEYCODEC_JSONL_BYTES or result['raw_xabort_bytes']!=KEYCODEC_ABORT_BYTES
            or result['raw_total_bytes']!=98722 or result['standalone_control_count']!=21
            or result['positive_key_count']!=27 or result['positive_stats_count']!=6
            or result['expected_negative_actual_rejection_count']!=20
            or any(result[k] is not True for k in ('complete_input_encoded_positions_anchor_decoded_wordwise_equal',
                'canonical_strict_cost_fallback_zero_delta_two_phase_lifecycle_and_hits_verified','exact_EOF_verified',
                'all_fresh_seven_identity_before_after_equal'))
            or any(result[k] is not False for k in ('original45_controls_completion_claimed',
                'full_component_build_admission_claimed','actual_full_FLU_entry_executed','native_RSS_verified',
                'AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('all fresh21 independent full raw codec cases/precise bytes must pass')
    result=dict(status='PASS',**result)
    return result


def expected_stage_exit(stage):
    prefix='controls/keycodec_negative_'
    if stage['label'].startswith(prefix):
        names={case['name'] for case in KEYCODEC_CASES}
        if stage['label'] not in {prefix+name+'/execute' for name in names}:
            raise ValueError('undeclared expected-negative stage')
        return 23
    return 0


def stage_outcome_valid(stage):
    return stage['status']==('FAILED' if expected_stage_exit(stage)==23 else 'PASS')


def check_keycodec_negative_watch(stage):
    path=OUT/(stage['label']+'.watchdog.json');watch=read(require(path))
    if (type(watch['returncode']) is not int or watch['returncode']!=23 or type(watch['pid']) is not int or watch['pid']<=0
            or watch['command']!=stage['command'] or expected_stage_exit(stage)!=23
            or stage['status']!='FAILED' or watch['limit_failure'] is not None
            or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True
            or watch['rss_cap_mib']!=512 or not 0<=watch['sampled_peak_rss_mib']<512
            or not 0<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=600
            or not 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']):
        raise ValueError('expected23 is accepted only from genuine own child without resource failure')
    return pin(path)


'''
change('integer_only_metadata_audits','\ndef input_fixture_audit(',new_functions+'def input_fixture_audit(')

def memory(s):
    s=sub(s,'dictionary_groups=[]','dictionary_groups=[];identity_groups=[];identity_encoded_bytes=0')
    s=sub(s,"        for group in range(1,f['groups']+1):","        base_keys=None\n        for group in range(1,f['groups']+1):")
    s=sub(s,'dense,clear,packed=rows[cursor:cursor+3];cursor+=3','dense,dense_keys_row,clear,packed,key_row=rows[cursor:cursor+5];cursor+=5')
    anchor="            stored=dictionary_record(control_file(folder,stem+'_packed.bin'));ph=stored['header']"
    addition='''            original_keys=dense_identity_record(folder,stem,f,group,(b,0,0,dense_live,dense_peak,536870912))
            if group==1:base_keys=original_keys
            if dense_keys_row!=dict(kind='dense_identity_keys',case=f['name'],group=group,runtime_group=1,
                    file=stem+'_dense_keys.bin',raw_key_words=len(original_keys[0])//8,operator_key_words=len(original_keys[1])//8):
                raise ValueError('complete dense identity observation row differs')
            actual_key_stats=tuple(fields[(f['name'],group,3,'reuse')][k] for k in ('built','reused','hits','live','peak','cap'))
            identity_cost,encoded_bytes=candidate_identity_record(folder,stem,f,group,original_keys,base_keys,actual_key_stats)
            if key_row!=dict(kind='candidate_identity_keys',case=f['name'],group=group,file=stem+'_identity_keys.bin',phases=[1,2]):
                raise ValueError('complete candidate identity observation row differs')
            identity_groups.append(dict(case=f['name'],group=group,independent_dense_key_cost=identity_cost,
                original_key_sha256=[hashlib.sha256(k).hexdigest() for k in original_keys],base_key_sha256=[hashlib.sha256(k).hexdigest() for k in base_keys],
                derived_from_c017_full_keys=True,candidate_all_integer_bytes_compared=True))
            identity_encoded_bytes+=encoded_bytes
            extra_files.update((dense_keys_row['file'],key_row['file']))
'''
    s=sub(s,anchor,addition+anchor)
    s=sub(s,"actual_group_dictionary_accounting=dictionary_groups,dictionary_controls=dedup,","actual_group_dictionary_accounting=dictionary_groups,dictionary_controls=dedup,\n        independent_dense_identity_accounting=identity_groups,actual_identity_encoded_bytes=identity_encoded_bytes,")
    return s
function('memory_controls_audit',memory)

def control(s):
    # Extend first namespace before its original exact check, not after it.
    s=sub(s,'    if {p.name for p in (OUT / "controls").iterdir()}!=dirs:',"    dirs.update({'keycodec_positive',*{'keycodec_negative_'+case['name'] for case in KEYCODEC_CASES}})\n    if {p.name for p in (OUT / \"controls\").iterdir()}!=dirs:")
    s=sub(s,'    codec = codec_controls_audit(d)','    codec = codec_controls_audit(d)\n    keycodec = keycodec_controls_audit(d)\n    key_cost_by_group={(row[\'case\'],row[\'group\']):row[\'independent_dense_key_cost\'] for row in memory[\'independent_dense_identity_accounting\']}')
    s=sub(s,"unique_by_group[(name,group)] if fixture['rank1'] else None)","unique_by_group[(name,group)] if fixture['rank1'] else None,\n                        key_cost_by_group[(name,group)] if fixture['rank1'] else None)")
    s=sub(s,"cache_accounting(fixture,unique_count=unique_by_group[(name,g)])['persistent_bytes_per_group']","cache_accounting(fixture,unique_count=unique_by_group[(name,g)],identity_cost=key_cost_by_group[(name,g)])['persistent_bytes_per_group']")
    s=sub(s,"stem+'_g1_packed.bin',stem+'_g1_decoded.bin'}","stem+'_g1_packed.bin',stem+'_g1_decoded.bin',stem+'_g1_identity_keys.bin'}")
    s=sub(s,"        if json_lines(folder/'memory_manifest.jsonl')!=[packed_row]:", "        identity_row=prime_identity_record(folder,stem+'_g1',prime_fixture,prime)\n        if json_lines(folder/'memory_manifest.jsonl')!=[packed_row,identity_row]:")
    s=sub(s,'actual_raw_bytes = sum(require(OUT / name).stat().st_size for name in receipt["files"]\n        if name.endswith(".bin") or Path(name).name == "actual_XABORT.txt")','''actual_raw_bytes = sum(require(OUT / name).stat().st_size for name in receipt["files"]
        if name.endswith(".bin") or Path(name).name in ("actual_XABORT.txt","actual_xabort.txt"))''')
    s=sub(s,"    if (actual_variable_bytes>forecast['variable_dictionary_raw_bytes_upper_bound']", "    actual_identity_bytes=memory['actual_identity_encoded_bytes']\n    if (actual_identity_bytes>forecast['variable_identity_encoded_bytes_upper_bound'] or actual_variable_bytes>forecast['variable_dictionary_raw_bytes_upper_bound']")
    s=sub(s,"forecast['fixed_control_raw_binary_and_abort_message_bytes']+actual_variable_bytes","forecast['fixed_control_raw_binary_and_abort_message_bytes']+actual_variable_bytes+actual_identity_bytes")
    s=sub(s,'total_declared_stages=45,','total_declared_stages=68,original_factor_diagonal_45_stages_retained=45,\n            additional_keycodec_driver_build_stages=2,additional_keycodec_execute_stages=21,')
    s=sub(s,"codec_controls=codec,fixtures=", "codec_controls=codec,keycodec_controls=keycodec,fixtures=")
    s=sub(s,'actual_variable_dictionary_raw_bytes=actual_variable_bytes,','actual_variable_dictionary_raw_bytes=actual_variable_bytes,actual_identity_encoded_bytes=actual_identity_bytes,\n        all_c017_full_identity_keys_bitwise_equal_to_candidate_decode=True,')
    return s
function('control_audit',control)

def forecast(s):
    s=sub(s,'total=0; variable_dictionary_upper=0; parts=[]; rows=0','total=0; variable_dictionary_upper=0; variable_identity_upper=0; parts=[]; rows=0')
    s=sub(s,"            rows+=3*f['groups']",'''            rows+=3*f['groups']
            key_bytes=cache_accounting(f)['raw_key_bytes']+cache_accounting(f)['projected_key_bytes']
            # Original full dense key + candidate two headers/base/decode fixed;
            # encoded part is independently variable, never above full fallback.
            amount+=f['groups']*(352+3*key_bytes+key_bytes)
            variable_identity_upper+=f['groups']*key_bytes;rows+=2*f['groups']''')
    s=sub(s,"    for c in contract['cap_negative_cases']:","    total+=len(contract['negative_cases'])*(256+3*(cache_accounting(prime)['raw_key_bytes']+cache_accounting(prime)['projected_key_bytes']))\n    rows+=len(contract['negative_cases'])\n    for c in contract['cap_negative_cases']:")
    s=sub(s,'    source_bytes=sum(',"    total+=KEYCODEC_RAW_BINARY_BYTES+KEYCODEC_ABORT_BYTES\n    rows+=KEYCODEC_MANIFEST_ROWS\n    source_bytes=sum(")
    s=sub(s,"    allowance=1*2**30; manifest_allowance=rows*2048", "    source_bytes+=require(KEYCODEC_CONTROL_SOURCE,KEYCODEC_CONTROL_SHA).stat().st_size\n    allowance=1*2**30; manifest_allowance=rows*2048")
    s=sub(s,'fixed_control_raw_binary_and_abort_message_bytes=total-variable_dictionary_upper,','fixed_control_raw_binary_and_abort_message_bytes=total-variable_dictionary_upper-variable_identity_upper,\n        variable_identity_encoded_bytes_upper_bound=variable_identity_upper,\n        standalone_keycodec_exact_jsonl_bytes=KEYCODEC_JSONL_BYTES,standalone_keycodec_exact_binary_and_abort_bytes=KEYCODEC_RAW_BINARY_BYTES+KEYCODEC_ABORT_BYTES,')
    return s
function('archive_forecast',forecast)
function('production_cache_shape_forecast',lambda s:sub(s,'forecast_is_not_actual_production_RSS_measurement=True,','identity_full_fallback_is_conservative_upper_bound=True,actual_cross_group_differences_not_predicted=True,\n        forecast_is_not_actual_production_RSS_measurement=True,'))

def stagecommands(s):
    s=sub(s,"    return [*d['build_commands']", "    keyexe=str(OUT/'runtime/keycodec_controls')\n    return [*d['build_commands']")
    s=sub(s,"        [d['build_python_executable']", "        [keyexe,*d['control_contract']['keycodec_positive_command_args']],\n        *[[keyexe,*case['args']] for case in d['control_contract']['keycodec_negative_cases']],\n        [d['build_python_executable']")
    return s
function('stage_commands',stagecommands)
function('stage_labels',lambda s:sub(s,"for c in d['control_contract']['factor_negative_cases']]+['audit/audit']", "for c in d['control_contract']['factor_negative_cases']]+['controls/keycodec_positive/execute']+[\n        'controls/keycodec_negative_'+case['name']+'/execute' for case in d['control_contract']['keycodec_negative_cases']]+['audit/audit']"))

def prepare(s):
    s=sub(s,"    files=dict(old['files']);",'''    commands.extend([
        [*common,'-c',str(SOURCE/'keycodec_controls.f90'),'-o',str(OUT/'build/keycodec_controls.o')],
        [compiler,'-O2','-march=native','-ffp-contract=off','-g',str(OUT/'build/keycodec_controls.o'),
         str(OUT/'build/SPOT1P64.o'),str(WHITE_OBJECT),str(ROOT/'lib/Darwin_arm64/libDragon.a'),
         str(ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a'),str(ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a'),
         str(ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a'),'-o',str(OUT/'runtime/keycodec_controls')]])
    files=dict(old['files']);''')
    s=sub(s,"    if len(commands)+len(names)+1!=45:raise ValueError('all original40 and5 new factor codec guarded stages must remain declared')",'''    names.extend(['keycodec_positive',*['keycodec_negative_'+case['name'] for case in KEYCODEC_CASES]])
    if len(commands)!=8 or len(commands)+len(names)+1!=68:
        raise ValueError('all original45 plus2 driver build and21 codec execute stages required')''')
    s=sub(s,"    runner=require(PARENT/'runtime/run_bounded_dragon.py');", "    shutil.copy2(require(KEYCODEC_CONTROL_SOURCE,KEYCODEC_CONTROL_SHA),SOURCE/'keycodec_controls.f90')\n    runner=require(PARENT/'runtime/run_bounded_dragon.py');")
    s=sub(s,"last_cprime_trim=c['last_cprime_trim'],factor_diagonal_trim=c['factor_diagonal_trim'],", "cross_group_identity_key_delta=c['cross_group_identity_key_delta'],keycodec_source=pin(KEYCODEC_CONTROL_SOURCE),keycodec_auditor=pin(KEYCODEC_AUDITOR),\n        last_cprime_trim=c['last_cprime_trim'],factor_diagonal_trim=c['factor_diagonal_trim'],")
    return s
function('prepare_build',prepare)
function('declaration_admission',lambda s:sub(s,'    return d','''    if (SOURCE/'keycodec_controls.f90').read_bytes()!=require(KEYCODEC_CONTROL_SOURCE,KEYCODEC_CONTROL_SHA).read_bytes():
        raise ValueError('fresh independent keycodec source differs')
    if d['control_contract']['original45_required'] is not True or len(stage_labels(d))!=68:
        raise ValueError('old complete45 and new independent23 stages mandatory')
    return d'''))
function('check_watch',lambda s:sub(s,'    item = helper().check_watch(OUT, stage)','    if expected_stage_exit(stage)==23:return check_keycodec_negative_watch(stage)\n    item = helper().check_watch(OUT, stage)'))

def run(s):
    s=sub(s,'"build/SPOT1P64.original_reference.o", "build/rank1_factor_cache_last_cprime_trim_controls.o")','"build/SPOT1P64.original_reference.o", "build/rank1_factor_cache_last_cprime_trim_controls.o",\n            "build/keycodec_controls.o","runtime/keycodec_controls")')
    s=sub(s,'        finally:\n            # Preserve all returned/partial raw files', '''            environment(d)
            runner.execute(OUT/'controls/keycodec_positive','execute',
                [str(OUT/'runtime/keycodec_controls'),*d['control_contract']['keycodec_positive_command_args']],STAGE_WALL)
            for case in d['control_contract']['keycodec_negative_cases']:
                environment(d)
                try:
                    runner.execute(OUT/'controls'/('keycodec_negative_'+case['name']),'execute',
                        [str(OUT/'runtime/keycodec_controls'),*case['args']],STAGE_WALL)
                except RuntimeError:
                    stage=read(OUT/FAMILY/'stages.json')['stages'][-1]
                    if stage['label']!='controls/keycodec_negative_'+case['name']+'/execute':raise
                    check_keycodec_negative_watch(stage)
                else:
                    raise ValueError('keycodec negative unexpectedly returned success; no retry')
        finally:
            # Preserve all returned/partial raw files''')
    s=sub(s,'or any(row["status"] != "PASS" for row in stages)', 'or any(not stage_outcome_valid(row) for row in stages)')
    s=sub(s,'factor_diagonal_codec_controls_passed=True)','factor_diagonal_codec_controls_passed=True,cross_group_identity_controls_passed=True)')
    return s
function('run_build',run)
function('audit_build',lambda s:sub(sub(sub(s,'any(row["status"] != "PASS" for row in stages[:-1])','any(not stage_outcome_valid(row) for row in stages[:-1])'),'factor_diagonal_codec_controls_passed=controls["codec_controls"]["status"]=="PASS",','factor_diagonal_codec_controls_passed=controls["codec_controls"]["status"]=="PASS",\n        cross_group_identity_controls_passed=controls["keycodec_controls"]["status"]=="PASS",'),'        control_counts=controls["counts"],','        control_counts=controls["counts"],'))
function('production_admission',lambda s:sub(sub(s,'any(row["status"] != "PASS" for row in stages)','any(not stage_outcome_valid(row) for row in stages)'), '    if controls != read(OUT / "audit/controls.json")', '''    if (audit.get('cross_group_identity_controls_passed') is not True or result.get('cross_group_identity_controls_passed') is not True
            or controls['keycodec_controls']['status']!='PASS' or controls['counts']['total_declared_stages']!=68):
        raise ValueError('all original45 plus actual21 independent codec cases must pass, without native qualification')
    if controls != read(OUT / "audit/controls.json")'''))

def binary(s):
    s=sub(s,"        'actual_Dragon':OUT/'runtime/Dragon'}", "        'actual_Dragon':OUT/'runtime/Dragon','keycodec_driver_object':OUT/'build/keycodec_controls.o',\n        'keycodec_executable':OUT/'runtime/keycodec_controls'}")
    s=sub(s,"    for symbol in ('_spot1p64_','_flu2dr64_','_flu_'):", "    if (symbols('keycodec_executable').count('_spot1p64_')!=1\n            or any(sym in symbols('keycodec_executable') for sym in ('_spot1p64_original_','_spot1p64_dense_'))\n            or str(SOURCE/'keycodec_controls.f90') not in Path(raw['keycodec_driver_object_debug']['path']).read_text()):\n        raise ValueError('fresh independent keycodec driver must compile actual source and link only candidate routine')\n    for symbol in ('_spot1p64_','_flu2dr64_','_flu_'):")
    return s
function('binary_audit',binary)

# These classifications identify only this new component's own records. All
# compulsory inherited predecessor and historical failure records stay exact.
for prefix in ('DECLARED_','FAILED_','PASS_','COMPLETE_'):
    old=prefix+'RANK1_FACTOR_CACHE_LAST_CPRIME_TRIM_BUILD'
    new=prefix+'RANK1_FACTOR_CACHE_CROSS_GROUP_IDENTITY_KEY_DELTA_BUILD'
    while old in code:
        index=code.index(old)
        prefix_text=code[max(0,index-32):index]
        suffix=code[index+len(old):index+len(old)+40]
        change('own_component_classifications:'+prefix,prefix_text+old+suffix,prefix_text+new+suffix)

ast.parse(code)
inverse=code
for e in reversed(edits):
    if inverse.count(e['after'])!=1:raise AssertionError(('inverse',e['label'],inverse.count(e['after'])))
    inverse=inverse.replace(e['after'],e['before'],1)
assert inverse.encode()==original.encode()
OUT.write_text(code)
(D/'factory_region_edits.json').write_text(json.dumps(edits,indent=2)+'\n')
(D/'factory.diff').write_text(''.join(difflib.unified_diff(original.splitlines(True),code.splitlines(True),fromfile=str(M),tofile=str(OUT))))
def funcs(s):
    return {n.name:ast.get_source_segment(s,n) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)}
a,b=funcs(original),funcs(code)
changed=[n for n in a if a[n]!=b[n]]; retained=[n for n in a if a[n]==b[n]]
report=dict(status='SOURCE_ONLY_DRAFT_UNREADY',factory=dict(path=str(OUT),sha256=sha(code),bytes=len(code.encode())),
    mother=dict(path=str(M),sha256=sha(original),bytes=len(original.encode())),complete_inverse_byteexact=True,
    source_only_ast_parse=True,region_count=len(edits),changed_original_functions=changed,
    original_functions_byteexact=retained,new_functions=sorted(set(b)-set(a)),original45_required=True,
    planned_stage_count=68,caps=dict(total_seconds=1800,stage_seconds=600,rss_mib=512,archive_bytes=2*2**30,history_bytes=96*2**30,free_bytes=8*2**30,threads=1,children=1,retries=0),
    arithmetic_fields_and_original_finite_bitwise_gates_retained=True,independent_expected_fees='c017 full key bytes first-owner strict 12*d<8*n',
    pending_source_bindings=[],actual_factory_import=None,actual_compile=None,actual_component_controls=None,
    actual_native_RSS=None,AAA_accuracy_qualified=False,ABA_admitted=False,project_written=False)
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
