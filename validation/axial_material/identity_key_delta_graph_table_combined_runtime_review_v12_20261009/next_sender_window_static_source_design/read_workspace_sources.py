"""Pure source/metadata review. No Fortran execution or project writes."""
import hashlib
import json
from pathlib import Path

D=Path(__file__).resolve().parent
R=Path('/Users/wen/spot')
A=R/'validation/artifacts'
CS=A/'axial-material-qualified-AB-owned-specs-identity-key-delta-graph-table-combined-source-v12-20261009'
CO=A/'axial-material-owned-specs-identity-key-delta-graph-table-combined-runtime-v12-20261009'
W=A/'axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009'
SENDER=A/'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/FLU2DR64.f'
SO=A/'axial-material-rank1-factor-cache-build-20261007/build/FLU2DR64.o'
SP=A/'axial-material-AAA-white-trace-cold-control-paths-20261004/build/SPOF64.f'
K=A/'axial-material-qualified-AB-rank1-factor-cache-cross-group-identity-key-delta-build-admission-v11-20261009/SPOT1P64.f90'

def digest(data):return hashlib.sha256(data).hexdigest()
def identity(p):
 s=p.lstat();assert p.is_file() and not p.is_symlink(),str(p)
 return {x:getattr(s,x) for x in ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')}
def load(p):return json.loads(p.read_bytes())
def write(name,data):
 with (D/name).open('x',encoding='utf-8')as f:json.dump(data,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')

decl=load(CO/'declaration.json')
files=[CO/'declaration.json',CO/'audit/binary_identity.json',CS/'trim_component_admission_INPUT.json',SENDER,SO,SP,K,R/'src/SPOT.f',
 A/'axial-material-rank1-factor-cache-build-20261007/audit/binary_identity.json',
 A/'axial-material-rank1-factor-cache-build-20261007/audit/new_sender_debug.txt',
 A/'axial-material-qualified-AB-rank1-factor-cache-build-admission-20261007/source_admission.json',
 CO/'runtime/Dragon',W/'AAA/bootstrap/bootstrap_axial.log',W/'AAA/bootstrap/bootstrap_axial.watchdog.json']
files += [CS/n for n in decl['source_inventory']['files']]
assert len(decl['source_inventory']['files'])==11
assert decl['source_inventory']['symlinks']=={} and decl['source_inventory']['directories']==['runtime']
files=list(dict.fromkeys(files))
before={str(p):identity(p) for p in files}
data={str(p):p.read_bytes() for p in files}
pins={str(p):dict(path=str(p),sha256=digest(data[str(p)]),size_bytes=len(data[str(p)]),identity=before[str(p)]) for p in files}
for name,expected in decl['source_inventory']['files'].items():assert pins[str(CS/name)]['sha256']==expected
assert pins[str(CO/'runtime/Dragon')]['sha256']=='8328a2a9a1c943f2d6703d9ec64ac42530c0017016b0a976645803a3256d4855'
assert pins[str(SO)]['sha256']=='74b22d403667e78686aef52b97933478779d4dfeb250b1cd1cb86343c930cfb9'
assert pins[str(K)]['sha256']=='0800cb54194a7736cb0309703dc2d1fe658171ce1496d6c22ac19fb0ebfcfff5'
assert decl['original_sender']==dict(path=str(SO),sha256=pins[str(SO)]['sha256'])
assert str(SO) in decl['production_link_command']
assert str(SP.with_suffix('.o')) in decl['production_link_command']
binary=load(CO/'audit/binary_identity.json')
assert binary['actual_runtime']==dict(path=str(CO/'runtime/Dragon'),sha256=pins[str(CO/'runtime/Dragon')]['sha256'])
assert binary['actual_object_definitions']['_flu2dr64_']['object']==decl['original_sender']
debug=data[str(A/'axial-material-rank1-factor-cache-build-20261007/audit/new_sender_debug.txt')].decode()
assert str(SENDER) in debug and 'DW_AT_name\t("flusp64")' in debug

sender=data[str(SENDER)].decode();sp=data[str(SP)].decode();kernel=data[str(K)].decode()
lines=sender.splitlines()
uses=[dict(line=i,text=v) for i,v in enumerate(lines,1) if any(x in v.upper() for x in ('CALL FLUSP64','SUBROUTINE FLUSP64','F2(','S2(','FUN(','SUN('))]
assert sum('CALL FLUSP64' in l for l in lines)==4
assert sum('CALL SPOF64' in l for l in lines)==1
flusp=sender[sender.index('*DECK FLUSP64'):]
assert 'ALLOCATE(KPSYS(NGEFF),NGIND(NGEFF),F2(NUN,NGEFF),S2(NUN,NGEFF))' in flusp
assert 'F2(:NUN,JJ)=FUN(:NUN,IG)' in flusp
assert 'FUN(:NUN,NGIND(JJ))=F2(:NUN,JJ)' in flusp
assert 'S2(:NUN,JJ)=SUN(:NUN,IG)' in flusp
assert 'S2(IND,JJ)=S2(IND,JJ)-DBLE(DIFHET(INM,IG))*DBLE(B2(4))*' in flusp
assert 'DO 150 IG=IGDEB,NGRP\n      NPSYS(IG)=IG' in sender
assert 'NPSYS(:NGRP)=0\n         NPSYS(IG)=IG' in sender
assert sender.count('FLUX(1,1,2),FLUX(1,1,8),FLUX(1,1,7)')==4
assert 'DOUBLE PRECISION FUNKNO(NUN,NGEFF),SUNKNO(NUN,NGEFF)' in sp
assert 'FUNKNO(1,II),FUNKNO(LL4+1,II),FUNKNO(LL4+LL5+1,II)' in sp
assert 'double precision, intent(in) :: qext(' in kernel
assert 'double precision, intent(out) :: flux(' in kernel
assert 'double precision, intent(out) :: cour(nfloor+1,nreg2d),xnei(npq,nreg2d)' in kernel
fun_uses=[dict(line=i,text=v) for i,v in enumerate(sp.splitlines(),1) if 'FUNKNO' in v or 'SUNKNO' in v]
assert not any('FUNKNO' in x['text'] for x in fun_uses if '=' in x['text'])
track=data[str(R/'src/SPOT.f')].decode()
assert 'NUNKN=NREG2D*(ISCAT*IELEM*NFLOOR+(NFLOOR+1)+NLF)' in track
assert 'LL4=NREG2D*ISCAT*IELEM*NFLOOR' in track and 'LL5=NREG2D*(NFLOOR+1)' in track
watch=load(W/'AAA/bootstrap/bootstrap_axial.watchdog.json')
assert watch['sampled_peak_rss_mib']==512.890625 and watch['returncode']==-15 and watch['rss_cap_mib']==512
assert watch['own_pid_wait4_observed']is False and all(watch[x]is None for x in ('own_pid_wait4_pid','own_pid_wait4_status','own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib'))
log=data[str(W/'AAA/bootstrap/bootstrap_axial.log')].decode()
progress=[l for l in log.splitlines() if 'AXMAT-RANK1-CACHE PROGRESS' in l]
assert progress
nreg2d,nfloor,iscat,ielem,nlf,ngrp=8,48,3,1,32,370
nun=nreg2d*(iscat*ielem*nfloor+nfloor+1+nlf)
full_window=8*nun*ngrp
assert nun==1800 and full_window==5328000
assert before=={str(p):identity(p) for p in files}

report=dict(schema='AXMAT_AFTER_V12_FLUSP64_OUTPUT_WINDOW_MEMORY_SOURCE_DESIGN_REVIEW_V1',status='PASS_STATIC_DESIGN_ONLY_UNREADY',
 code_modified=False,project_written=False,business_imports=0,business_calls=0,numerical_children=0,fixtures_run=0,compiled=False,root_polling=0,
 exact_runtime_provenance=dict(actual_runtime=pins[str(CO/'runtime/Dragon')],combined_declaration=pins[str(CO/'declaration.json')],
  sender_object=pins[str(SO)],sender_source=pins[str(SENDER)],compiled_sender_source_path_from_archived_debug=str(SENDER),
  source11_inventory_sha_exact=True,source11_files=list(decl['source_inventory']['files']),source11_not_fortran_sources=True,
  combined_only_original_SPOT_and_SPOASM_overrides=binary['sole_object_changes'],source_identity_not_entire_instruction_equivalence=True),
 actual_failed_observation=dict(watch=pins[str(W/'AAA/bootstrap/bootstrap_axial.watchdog.json')],log=pins[str(W/'AAA/bootstrap/bootstrap_axial.log')],
  sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],rss_cap_mib=512,pid=watch['pid'],returncode=-15,own_pid_wait4_observed=False,
  last_cached_progress_lines=progress[-3:],completed_coupled_maps=0,scientific_qualification=False,AAA_accuracy_qualified=False,ABA_admitted=False),
 exact_source_lines=dict(FLUSP64=[1611,1666],F2_S2_allocate=1635,copyin=[1642,1643],leak_source_math=[1644,1655],SPOF64_call=[1659,1660],copyback=[1661,1663],deallocate=1664,
  caller_FLUX_allocation=[204,205],caller_plane_meanings=[189,201],caller_inner_init=[716,721],caller_batch_NPSYS=[926,931],four_calls=[944,948,1074,1078],
  scalar_NPSYS=[1070,1071],SPOF64_source_file=str(SP),SPOF64_dims=[49,50],SPOF64_argument_offsets=[208,211],SPOT_kernel_source=str(K),
  SPOT_qext_intent_in=1023,SPOT_outputs_intent_out=[1025,1026],SPOT_full_reconstruction=[1311,1332],layout_formula=[310,312]),
 full_symbol_use_evidence=uses,SPOF64_FUN_and_SUN_all_uses=fun_uses,
 dataflow_and_lifetime=[
  'FLU2DR64 allocates FLUX(NUN,NGRP,8) for the entire FLU lifecycle. Four exact FLUSP64 calls pass old plane2, source plane8, output plane7; these are disjoint contiguous blocks of the same allocated parent.',
  'Before dispatch source plane8 is complete. Batch NPSYS activates ascending suffixIGDEB..NGRP; scalar activates onlyIG. FLUSP64 preserves ascendingIG→JJ and system pointers/NGIND. No arbitrary permutation is admitted by the current callsites.',
  'F2 is an owning copy of FUN; S2 is an owning copy of SUN and may apply original B1 SIGS correction using readonly FLUOLD. Both are allocated before group solve and live until all SPOF64 groups complete.',
  'SPOF64 never reads initial FUNKNO, only passes three contiguous segments to unchanged SPOT1P64 INTENT(OUT) flux/cour/xnei. SUNKNO remains readonly and maps to unchanged qext INTENT(IN). SPOT consumes qext before final outputs and retains no pointer to caller arrays.',
  'Output writes are group-local with the same ascending group loop; source plane8/oldplane2 are not changed. Direct current output plane7 window therefore cannot alter future group source or old flux. Unwritten tail words, if any in legal dimensions, remain as original FUN rather than copies round-tripped.',
  'Caller parent FLUX lives across the call, and the callee retains no output pointer after return. No pointer ownership/deallocation changes outside private F2 allocation are needed.',
 ],
 minimum_patch_design=dict(target=str(SENDER),target_routine='FLUSP64',actual_patch_created=False,public_ABI_changed=False,method='Explicit-shape sequence association to contiguous parent output window; no POINTER/TARGET/ASSUMED_SHAPE interface',
  edits=[
   'Add private logical direct_output_window and private first/last indices. After original NGEFF0 return, derive first/last active group with unchanged ascending scan; use only when last-first+1==NGEFF. All active groups occupy an exact contiguous window.',
   'Keep original KPSYS/NGIND/S2 allocations and original full S2 copy + leakage correction untouched. Allocate F2(NUN,NGEFF) only for non-contiguous fallback; conditional F2 copy-in remains original.',
   'For direct window call original SPOF64 with FUN(1,NGIND(1)) in place of F2. Keep all other arguments, group order, source array S2, and all math body bytes exact. Dummy FUNKNO is explicit-shapeNUN×NGEFF; first scalar element supplies the contiguous suffix storage sequence, avoiding any gathered-section temporary.',
   'For non-contiguous set call original SPOF64(F2,S2) and preserve original complete scatter-back. Only conditional F2 deallocate when allocated; original S2/NGIND/KPSYS deallocate retained.',
  ],
  not_safe_shortcuts=['Do not globally replace FUN with a vector-subscript/view for arbitrary holes (compiler gather/copy temp and wrong column mapping).',
   'Do not alias S2 to SUN for B1 SIGS nonzeroB2; original source correction would mutate FLUX plane8 and alter later residual/source behavior.',
   'Do not use FLUOLD as output workspace; it is still the old-flux authority during leakage and caller convergence.',
   'Do not deduplicate eight FLUX planes across lifetimes without a separate full convergence/acceleration alias proof.',
   'Do not change SPOT1P64/SPOF64 mathematics, dimensions, public ABI, physical sample, precision, cap or original failed namespaces.']),
 expected_payload_saving=dict(formula='8*NUN*NGEFF bytes for every direct contiguous active window; 0 for original fallback',
  declared_shape=dict(NREG2D=8,NFLOOR=48,ISCAT=3,IELEM=1,NLF=32,NGRP=370,NUN=1800,LL4=1152,LL5=392,XNEI=256),
  full370_window_bytes=full_window,full370_window_mib=full_window/2**20,single_group_bytes=8*nun,
  saved_payload_is_not_actual_live_RSS=False if False else True,actual_NGEFF_at_watchdog_failure_not_instrumented=True,
  no_actual_RSS_under512_proof=True,cache_accounted_peak_not_process_RSS=True),
 retained_and_next_validation=dict(original68_function_controls_required_unchanged=True,extra_wrapper_controls_not_run=True,
  necessary_additional_controls=['contiguous suffix includingFIRST>1 andNGEFF1; sparse/noncontiguous fallback; zeroactive return',
   'ILEAK0/B2zero andILEAK3/B2nonzero original S2 source correction byteexact; readonlySUN/FLUOLD unchanged',
   'wholeFP64 FUN/SUN/oldflux bytes across original copy wrapper vs direct output with current SPOT actual kernel, signedzero and untouched nonactive columns/tails',
   'compiler object/source/assembly binding to new FLU2DR64 object and actual link, no hidden full-window temporary; all original68 scientific/input controls kept',
   'fullnewcomponent→combined→wholeINPUT→cold source admissions and actual ownPID512 watch, stages+seals+Rootterminal+alltails; oldV12 failure not retried'],
  current_failed_namespace_immutable=True,actual_science_qualification=False),
 exploratory_readonly_error_preserved=dict(chunk_id='26f818',exit_code=1,reason='Incorrect exploratory filename source_patch_proof.json; authoritative proof is source_admission.json. No business execution or mutation.'),
 fresh_pins=pins,seven_identity_before_after_equal=True,actual_readonly_tool_terminal=None)
write('REPORT.json',report)
write('SOURCE_EVIDENCE_MANIFEST.json',dict(schema='FLUSP64_OUTPUT_WINDOW_READONLY_SOURCE_EVIDENCE_V1',pins=pins))
text='''V12 失败后的 FLUSP64 工作区最小内存设计（仅源码审查）

结论：可优先去掉连续活动群的 F2 整批输出副本，S2 源项副本暂保留。正式源码尚未修改，未编译、未运行控制或数值。

真实来源是已封存 rank1-build-admission/FLU2DR64.f 的 FLUSP64（1611–1666行），不是名为 FLUSP64F2 的独立函数。V12实际runtime8328的declaration/link与binary identity明确保留sender对象74b22；其debug绑定这份SOURCE路径。SOURCE11全部鲜SHA与原inventory精确相等，Fortran源由该继承编译来源提供。

1635行 F2/S2 各allocate(NUN,NGEFF)，1642–1643复制SUN/FUN。1659调用SPOF64，1662再复制F2→FUN，1664释放。F2在全部群求解中始终驻留。FLU2DR64四调用944/948/1074/1078均使用FLUX的plane2旧场、plane8源、plane7输出，无重叠；批量NPSYS是连续IGDEB..NGRP，标量是单群。SPOF64仅把FUN三个区段交SPOT1P64的INTENT(OUT)，不读取incoming FUN，qext/SUN是INTENT(IN)且不保存pointer。原全群顺序和浮点操作可不变。

最小设计：私有检测first/last活动群，只有last-first+1==NGEFF时，将FUN(1,NGIND(1))按原explicit-shape序列关联传给SPOF64；不需要新增pointer/TARGET或修改公共ABI。仅不连续活动群仍allocate原F2并原gather/scatter。原S2全部copy与泄漏修正式逐字保留。不能用vector-subscript制造隐藏temporary；也不能把S2直接aliasSUN，因为当前B1 SIGS的S2减leak会改掉caller FLUX plane8。

payload公式为8*NUN*NGEFF。原SPOT布局NUN=8*(3*48+49+32)=1800，完整370群窗口可少5,328,000字节=5.081176758 MiB，单群14,400字节。失效采样时的精确NGEFF没有单独动态记录；此为条件设计估算，不能当真实RSS削减或达标。

实际V12原watch记录PID62748，sample512.890625MiB>原512，return-15，own_wait4未观察且四字段None；0maps、无科学资格。cache记账峰302850600与processRSS是不同口径。新改动须新source/object/runtime来源和额外连续/稀疏/空群/泄漏/只读输入/逐位输出控制，保留全部68控制以及原物理、Float64、OwnPID512和预算，再按Root唯一新版本完整执行。旧失败不可重试或改写。本报告只证明源码最小候选与边界，不证明运行利益。
'''
with(D/'REPORT.txt').open('x',encoding='utf-8')as f:f.write(text)
print(json.dumps(dict(status=report['status'],report_sha256=digest((D/'REPORT.json').read_bytes()),source_files=len(files),source_bytes=sum(len(v)for v in data.values()),expected_full_window_saved_bytes=full_window,actual_RSS_pass=False,project_written=False),ensure_ascii=False))
