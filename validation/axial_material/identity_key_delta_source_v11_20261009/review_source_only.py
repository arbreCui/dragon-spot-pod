import ast, hashlib, json, pathlib, re
D=pathlib.Path('/private/tmp/axmat-rank1-cross-group-identity-key-delta-source-v11-20261009')
K=D/'SPOT1P64.f90'
proof=json.loads((D/'source_inverse_proof.json').read_text())
source=K.read_text()
P=pathlib.Path(proof['parent_path'])
factory=pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_rank1_factor_cache_factor_diagonal_trim_production.py')
controls=pathlib.Path('/Users/wen/spot/validation/axial_material/rank1_factor_cache_factor_diagonal_trim_controls.f90')
helper=pathlib.Path('/Users/wen/spot/validation/axial_material/rank1_factor_cache_factor_diagonal_trim_patch.py')
pins={str(p):dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in (K,P,factory,controls,helper,D/'generate_source_only.py',D/'region_edits.json',D/'source_inverse_proof.json',D/'source.diff')}
assert pins[str(K)]['sha256']==proof['candidate_sha256']
assert pins[str(P)]['sha256']=='5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809'
inverse=source
edits=json.loads((D/'region_edits.json').read_text())
for e in reversed(edits):
    assert inverse.count(e['new'])==1
    inverse=inverse.replace(e['new'],e['old'],1)
assert inverse.encode()==P.read_bytes()
tree=ast.parse(factory.read_text())
function_lines={n.name:n.lineno for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
assert '45' in factory.read_text() and '1146' in factory.read_text()
calls=re.search(r'(?ms)^  subroutine rank1_identity\(.*?^  end subroutine rank1_identity\n',source).group()
assert 'call SPOT1P64_RANK1_GUARD(igroup,key,phase,eligible,active)' in calls
guard=re.search(r'(?ms)^  subroutine SPOT1P64_RANK1_GUARD\(.*?^  end subroutine SPOT1P64_RANK1_GUARD\n',source).group()
assert guard.count('rank1_validated_hits=rank1_validated_hits+1_int64')==1
assert guard.index('call SPOT1P64_RANK1_KEY_MATCH(igroup,key,phase)',guard.index('else if (phase == 2)'))<guard.index('rank1_validated_hits=rank1_validated_hits+1_int64')
assert ".not.allocated(plan%rank1_raw_bits)" in guard
line=lambda phrase: source[:source.index(phrase)].count('\n')+1
control_cases=[
 dict(kind='positive',required=['base full owner per phase','same key zero-length delta','sparse nonzero int64 delta with negative/signed-zero bit patterns','same-length strict saving selection','12*d==8*n full fallback','12*d>8*n full fallback','different-length full fallback','nonmonotone group arrival with separate phase owners','CLEAR then new unrelated full bases','original ready-hit counter increments only after full comparison']),
 dict(kind='negative',required=['full logical unchanged-position mutation','delta-position mutation','changed full owner (use zero-delta follower to avoid overridden position)','new current key length','ineligible existing group','index zero/negative/past end','duplicate/descending indices','value/count/position mismatches','delta value equal to base is noncanonical','nonprofitable encoded shape','missing owner bits/mode','owner with encoded positions','inaccurate original_size','invalid output length','missing phase1 before phase2','existing original14 identity mutations +6 memory +8 lower dictionary +4 factor codec negatives'])]
report=dict(status='SOURCE_ONLY_DRAFT',draft_status='UNREADY',source_inverse_status='PASS',candidate_sha256=proof['candidate_sha256'],
 original_full_IEEE_key_builder_byteexact=True,public_Factor64_Solve64_byteexact=True,full_boundary_solve_byteexact=True,
 base_ownership='First stored full key per phase, never a delta or copy; private owner indices reset by the original full PLAN CLEAR.',
 format='Positions unallocated: bits is full original key and size(bits)==original_size. Positions allocated: bits is differences, including two allocated zero-length arrays; original_size==base size, strict ascending distinct positive int32 positions, values differ from base, 12*d<8*n.',
 original_phase2_raw_presence_gate_retained=True,complete_integer_word_equality_not_hash=True,
 allocation_and_lifetime='Original 8*n full temporary key remains reserved before the unchanged builder. Store reserves exactly 8*n full or 12*d delta before allocation. Two added int64 sizes and two int32 allocatable descriptors remain within the original declared 4096/group reserve, requiring actual compiler ABI confirmation. No decoded full temporary is made during MATCH. Public KEY_LOAD writes a caller-owned full output.',
 public_interfaces=dict(KEY_LOAD='(igroup, phase, int64 key(:) intent(out))',KEY_STATS='(igroup, phase, owner defaultINTEGER out, count int64 out, compressed LOGICAL out, stored_words int64 out, stored_positions int64 out)'),
 error_boundary='Original GUARD eligibility/group/phase2-missing-raw order is retained. Invalid compressed metadata uses the original IMMUTABLE OPERATOR CHANGED message. KEY_STATS observes malformed metadata without validating it; only MATCH/LOAD establishes validity. Tests must not treat KEY_STATS as admission.',
 source_lines={n:line('  subroutine '+n+'(') for n in ('SPOT1P64_RANK1_GUARD','SPOT1P64_RANK1_KEY_STATS','SPOT1P64_RANK1_KEY_VALIDATE_DATA','SPOT1P64_RANK1_KEY_SAVE_DATA','SPOT1P64_RANK1_KEY_MATCH','SPOT1P64_RANK1_KEY_LOAD','rank1_identity','boundary_solve')},
 actual_difference_counts=None,actual_RSS_saving=None,actual_compile=None,actual_controls=None,actual_native_AAA=None,
 claimed_failure_line=None,
 comparison_to_other_candidates=dict(pivot_int8='nstate32 pivot compression saves (4-1)*32*49*370=1740480 bytes (1.659851MiB), but is an additional public-plan type/codec adaptation and is smaller than potentially shared identity data.',
  early_miss_workspace_release='Separate alternative: deallocate lower/diagonal/upper/solve_pack immediately before FactorPack only on ordinary rank1 miss. Their last reads are in the completed forward loop; backsub uses only plan cprime+dprime. Saves 3*8*32*32*49+8*32*33=1212672 bytes at miss/PACK overlap. Not in this V11 source; no warm-hit or RSS claim.',
  cprime_sparse_columns='Rejected assumption: original upper has negative-DU rows but all columns may be dense; Factor/Solve mixes rows. No source proof of ignorable Cprime columns exists.'),
 future_controls_required=control_cases,
 original_45_mandatory=True,original_field_pairs=1152,original_dense_references=378,
 new_factory_changes_required=dict(source_inputs=function_lines['source_inputs'],patch_admission=function_lines['patch_admission'],production_cache_shape_forecast=function_lines['production_cache_shape_forecast'],cache_accounting=function_lines['cache_accounting'],check_counters=function_lines['check_counters'],control_audit=function_lines['control_audit'],run_build=function_lines['run_build'],production_admission=function_lines['production_admission'],
  changes='New helper/control/kernel pins and independent SOURCE/OUT/TERM family. Original45 and all numeric thresholds remain. Recompute key live/peak from raw recorded full keys and actual canonical stored formats, not constant full-key bytes. Extend archive forecast/namespaces/commands/stages/raw-receipt-before-audit for genuine codec cases. New combined/cold intake must bind the actual new successful component, no aliasing old V10 credentials.'),
 limits=['Source text and integer-storage reasoning only; no Fortran syntax compile, codec execution or business run.', 'Theoretical repeated white/moment components are not actual ndiff observations; compression always falls back safely when not smaller.', 'Cache accounting peak is not retained live bytes and is not own-PID RSS. V10 actual native failure remains 514.203125MiB, zero completed maps.', 'No caps, physics parameters, ranks, SN32, cells16, groups, reference or precision thresholds changed.'],
 pins=pins,project_written=False,business_executed=False)
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('V11 完整身份键无损 base+差异存储源码草稿\n\n状态：SOURCE_ONLY_DRAFT / UNREADY；未编译、未控制执行、未运行科学业务。\n'+
 '母本：5e0d4afc9a4ebfb6f26b2e3c4ab98c53f501afa861c33a098e6ab55031c5e809。候选：'+proof['candidate_sha256']+'。\n'+
 '6处源码替换可完整逆向回母本；原 full key 生成、Factor64/Solve64、Lower/Factor PACK/LOAD、boundary_solve 均完整字节不变。\n'+
 '每phase首个完整键只存一次；后续同长度键仅在12*差异数<8*键长时存int32位置+原int64值，否则回退完整键。零差异合法。每次完整逻辑键仍逐字比较，原phase2 raw门及ready hit计数保持。\n'+
 '新KEY_LOAD供真实controls输出完整键；KEY_STATS只观察元数据，不能充当准入。CLEAR释放全PLAN并清零两个base owner。原512MiB cap和4096/group描述符预留不变。\n'+
 '实际差异数和RSS收益均未知。必须独立源码审核、实际编译、原45阶段全控制，以及新编码边界/损坏/完整负例控制后，才可建立新family。V10失败事实不改。\n'+
 '另有可独立实施的缓存miss提前释放4个工作数组方案，理论临时重叠减少1212672B；当前候选未包含此改动。不得把Cprime假定为可删零列。\n')
print(json.dumps(dict(status=report['status'],report_sha256=hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest(),candidate_sha256=proof['candidate_sha256'],full_inverse=True,source_only=True)))
