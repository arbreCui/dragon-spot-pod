from pathlib import Path
import json, hashlib, os, stat, ast, re

R=Path('/Users/wen/spot')
O=Path('/private/tmp/spot_storage_review_eighteenth_build_cache_20261009')
OLD=Path('/private/tmp/spot_storage_review_seventeenth_build_cache_20261009')
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
pins=[];pin_cache={}
def identity(p):
    s=Path(p).lstat()
    return [getattr(s,'st_'+k) for k in KEYS]
def pin(p,expected=None):
    p=Path(p);before=identity(p)
    assert stat.S_ISREG(before[2]) and not p.is_symlink()
    if str(p) in pin_cache:
        b,q=pin_cache[str(p)];assert q['identity']==before
        if expected is not None:assert q['sha256']==expected
        return b,q
    b=p.read_bytes();assert identity(p)==before
    h=hashlib.sha256(b).hexdigest()
    if expected is not None:assert h==expected,(str(p),h,expected)
    q={'path':str(p),'bytes':len(b),'sha256':h,'identity':before}
    pins.append(q);pin_cache[str(p)]=(b,q);return b,q
def read(p,expected=None):return json.loads(pin(p,expected)[0])
def meta(p):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
    return {'path':str(p),'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'identity':[getattr(s,'st_'+k) for k in KEYS]}
def summary(rows):
    unique={(q['identity'][0],q['identity'][1]):q for q in rows}
    return {'regular_paths':len(rows),'unique_inodes':len(unique),'logical_bytes':sum(q['logical_bytes'] for q in unique.values()),'allocated_bytes':sum(q['allocated_bytes'] for q in unique.values())}
def stream_sha(rows):
    h=hashlib.sha256()
    for q in sorted(rows,key=lambda q:q['path']):
        h.update(json.dumps([q['path'],q['identity']],ensure_ascii=False,separators=(',',':')).encode()+b'\n')
    return h.hexdigest()
def write(name,value):
    p=O/name
    with p.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
    return pin(p)[1]

prior=read(OLD/'REPORT.json','0e7685370305044a323a5b1a605a947e7b2d7a465582e77d84b1213194fdac33')
read(OLD/'actual_readonly_tool_receipt.json','fd6dd4028e2a5a7ea1db8fa111a01f14499ed1f56ad9e4aec26865f78ad3296e')
pin(OLD/'REPORT.txt','84b99fd105ef2c39fe5e41ac7d314afd787a51a86a65e8435db9042740c47742')
root17=read('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json','45cc1ac8b5cc943811a6a8ee3f2e0ad3c17bb7568e29837bf80ec626115e8e76')
root18=read('/private/tmp/spot_storage_eighteenth_root_readonly_20261009/before.json')
obs=read(O/'initial_actual_readonly_observations.json')
assert all(obs[k]['exit_code']==0 for k in ('git_count_objects','git_du','source_dependency_search'))

# Finite established non-validation trees only. No all-project/artifacts/.git-object walk.
core=[];links=[]
for stem in ('src','Trivac','Ganlib','Utilib','lib','bin','data','SPOT_doc','script','.ruff_cache'):
    top=R/stem
    if not top.exists():continue
    for folder,ds,ns in os.walk(top,followlinks=False):
        for name in ds+ns:
            p=Path(folder)/name;s=p.lstat()
            if stat.S_ISREG(s.st_mode):core.append(meta(p))
            elif stat.S_ISLNK(s.st_mode):links.append({'path':str(p),'target':os.readlink(p),'identity':identity(p)})
for p in R.iterdir():
    if p.is_file() and not p.is_symlink():core.append(meta(p))
core_sha=stream_sha(core)
assert core_sha==prior['core_complete_regular_identity_comparison']['current_identity_stream_sha256']
assert summary(core)==prior['core_current_summary']
assert links==prior['core_symlinks_current_metadata_without_prior_link_completeness_claim']

libraries=[q for q in core if Path(q['path']).suffix=='.a']
programs=[q for q in core if Path(q['path']).name in ('Dragon','Trivac','Ganlib')]
old_binary={q['path']:q for q in prior['static_libraries_exact_paths']+prior['root_native_program_exact_paths']}
assert {q['path']:q for q in libraries+programs}==old_binary
compiled={s:summary([q for q in core if Path(q['path']).suffix==s]) for s in ('.o','.a','.pyc','.mod')}
builds=[]
for rel in ('build','target','dist','node_modules','vendor','.cache','.ruff_cache','.pytest_cache','__pycache__','src/build','Trivac/build','Ganlib/build','Utilib/build','tmp','temp'):
    p=R/rel
    builds.append({'path':str(p),'present':os.path.lexists(p),'is_directory':p.is_dir() and not p.is_symlink(),'regular_paths_in_reviewed_core':sum(Path(q['path']).is_relative_to(p) for q in core)})
temporary_core=[q for q in core if Path(q['path']).suffix.lower() in ('.tmp','.temp','.log','.out','.zip','.gz','.tgz','.tar','.bak')]

assert root18['cache_like']==root17['cache_like']
cache=[meta(q['path']) for q in root18['cache_like']]
assert all(q['identity']==x['identity'] for q,x in zip(cache,root18['cache_like']))
assert stream_sha(cache)==prior['cache_identity_stream_sha256']
deleted=read(R/'validation/storage_cleanup_twelfth_20261009/cache_manifest.json','85e7d25c110b2045119b403eb2e34e72182260bd74115b922e53ad8a77b31a47')
assert all(not os.path.lexists(q['path']) for q in deleted['candidates'])
source_evidence=[]
for q in prior['current_direct_dependency_source_references']:
    b,s=pin(q['path'],q['source_sha256'])
    lines=b.decode().splitlines();ex=q['source_excerpt'];start=ex['first_line']-1
    assert lines[start:start+len(ex['lines'])]==ex['lines']
    source_evidence.append(q)
for rel in ('Trivac/src/Makefile','Ganlib/src/Makefile','Utilib/src/Makefile'):
    old=next(q for q in prior['full_input_pins'] if q['path']==str(R/rel))
    pin(R/rel,old['sha256'])
for rel in ('validation/storage_review_seventeenth_20261009/REPORT.txt','validation/storage_review_sixteenth_20261009/REPORT.txt','validation/storage_review_fifteenth_20261009/REPORT.txt','validation/storage_cleanup_twelfth_20261009/REPORT.txt'):
    pin(R/rel)

# Git count/du came from observed purpose-limited commands; do not read object contents.
git_counts={}
for line in obs['git_count_objects']['output'].splitlines():
    k,v=line.split(': ',1);git_counts[k]=int(v)
git_du={}
for line in obs['git_du']['output'].splitlines():
    value,path=line.split('\t',1);git_du[path]=int(value)
lost=[]
for folder,ds,ns in os.walk(R/'.git/lost-found',followlinks=False):
    for n in ns:
        p=Path(folder)/n
        if stat.S_ISREG(p.lstat().st_mode):lost.append(meta(p))
assert stream_sha(lost)==prior['git_lost_found_path_identity_stream_sha256']
assert summary(lost)==prior['git_lost_found_current_summary']

# Small controls only; immutable old failures/results and recovery descriptions retain their SHA.
small=[]
for q in prior['small_restore_controls_and_old_failed_receipts_full_SHA_preserved']:
    _,s=pin(q['path'],q['sha256']);small.append(s)
recovery=meta(prior['runtime_unique_recovery_master_identity_exact']['path'])
assert recovery==prior['runtime_unique_recovery_master_identity_exact']

# Frozen evidence membership is separate from mere Makefile rebuild references.
W=R/'validation/artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
binding=read(W/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
gp=R/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
graph=read(gp,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
expected=set(binding['files']);canon={q['path'] for q in graph['canonical_files']}
all_graph_core_paths=set()
def collect_core_paths(v):
    if isinstance(v,str):
        if v.startswith(str(R)+'/') and not v.startswith(str(R/'validation')+'/'):all_graph_core_paths.add(v)
    elif isinstance(v,list):
        for x in v:collect_core_paths(x)
    elif isinstance(v,dict):
        for k,x in v.items():collect_core_paths(k);collect_core_paths(x)
collect_core_paths(graph)
nsroots=[Path(q['canonical_root']) for q in graph['namespaces']]
alias_paths=[Path(q[k]) for q in graph['aliases'] for k in ('path','target')]
resource_roots=[Path(x) for x in binding['resource_info']['resource_roots']+graph['live_resource_roots']]
def locks(p):
    s=str(p)
    return {'binding_expected':s in expected,'canonical':s in canon,'any_complete_graph_literal':s in all_graph_core_paths,'namespace_subtree':any(p.is_relative_to(x) for x in nsroots),'alias_file_or_subtree':any(p==x or p.is_relative_to(x) for x in alias_paths),'resource_subtree':any(p.is_relative_to(x) for x in resource_roots)}
fixed=[];object_candidates=[]
exts=('.f','.F','.f90','.F90','.c','.C','.f77','.F77','.cc','.cpp')
for q in core:
    p=Path(q['path'])
    if p.suffix!='.o':continue
    locked=locks(p)
    if any(locked.values()):fixed.append({**q,'frozen_membership':locked});continue
    source_paths=[p.with_suffix(e) for e in exts if p.with_suffix(e).is_file() and not p.with_suffix(e).is_symlink()]
    assert source_paths, str(p)
    makefile=p.parent/'Makefile';mb,mp=pin(makefile)
    assert '%.o' in mb.decode() and '$(OBJ' in mb.decode()
    srcpins=[pin(x)[1] for x in source_paths]
    object_candidates.append({**q,'retained_sources':srcpins,'retained_regeneration_makefile':{'path':mp['path'],'sha256':mp['sha256']},'frozen_membership':locked,'classification':'REBUILDABLE_OBJECT_NOT_FROZEN_PENDING_ROOT_FIXED_MANIFEST_REVIEW'})

# Static current launch reads the already built runtime; no source-tree archive link is issued here.
fpath=R/'validation/axial_material/prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py'
fb,fp=pin(fpath,'59d0c9b0f0a3b9ca6764f628ade537ec9b09eaa6edfe69e734994a7323adbfc8')
fs=fb.decode();ft=ast.parse(fs);launch=[]
for n in ft.body:
    if isinstance(n,ast.FunctionDef) and n.name in ('run_AAA','cold_launch_in_clean_process'):
        text=ast.get_source_segment(fs,n)
        launch.append({'source':fp['path'],'function':n.name,'first_line':n.lineno,'last_line':n.end_lineno,'source_segment_sha256':hashlib.sha256(text.encode()).hexdigest(),'source_segment':text})
assert len(launch)==2

# Sources actually in the current dependency graph can mention historical .o controls.
# Preserve any unbound object basename referenced there for Root's precise source review.
source_reference_hits={}
object_basenames={Path(q['path']).name:q['path'] for q in object_candidates}
for path in sorted(expected|canon):
    p=Path(path)
    if not p.is_relative_to(R/'validation') or p.suffix not in ('.py','.sh'):continue
    content=p.read_text();seen=set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*\.o\b',content))&set(object_basenames)
    for basename in seen:source_reference_hits.setdefault(object_basenames[basename],[]).append(str(p))
object_review_hold=[q for q in object_candidates if q['path'] in source_reference_hits]
object_candidates=[q for q in object_candidates if q['path'] not in source_reference_hits]
for q in object_review_hold:q['current_source_basename_reference_locations']=source_reference_hits[q['path']];q['classification']='REBUILDABLE_BUT_CURRENT_SOURCE_REFERENCE_NEEDS_CONTEXT_HOLD'

archive_candidates=[];archive_different=[]
for subtree,name,master in [('src','libDragon.a','lib/Darwin_arm64/libDragon.a'),('Trivac/src','libTrivac.a','Trivac/lib/Darwin_arm64/libTrivac.a'),('Ganlib/src','libGanlib.a','Ganlib/lib/Darwin_arm64/libGanlib.a'),('Utilib/src','libUtilib.a','Utilib/lib/Darwin_arm64/libUtilib.a')]:
    p=R/subtree/name;m=R/master;pb,pp=pin(p);mb,mp=pin(m)
    q={**meta(p),'full_sha256':pp['sha256'],'retained_master':{**meta(m),'sha256':mp['sha256']},'frozen_membership':locks(p),'regeneration_makefile':str(p.parent/'Makefile')}
    assert not any(q['frozen_membership'].values())
    assert str(m) in expected
    if pb==mb:q['classification']='BYTE_EXACT_SRC_ARCHIVE_COPY_OF_FROZEN_DARWIN_MASTER_PENDING_ROOT_FIXED_MANIFEST_REVIEW';archive_candidates.append(q)
    else:q['classification']='DIFFERENT_BYTES_HOLD';archive_different.append(q)
potential=object_candidates+archive_candidates
candidate_report={'schema':'SPOT_R18_COMPILED_FIXED_CANDIDATE_SCREEN_V1','status':'CANDIDATES_FOR_ROOT_DEPENDENCY_AND_FIXED_MANIFEST_REVIEW_NOT_DELETE_AUTHORITY','candidates':potential,'candidate_summary':summary(potential),'frozen_object_HOLD':fixed,'current_source_reference_context_HOLD':object_review_hold,'different_archive_HOLD':archive_different,'binding_expected_count':len(expected),'complete_graph_canonical_count':len(canon),'complete_graph_namespace_count':len(nsroots),'complete_graph_alias_count':len(graph['aliases']),'binding_resource_count':len(binding['resource_info']['resource_roots']),'graph_resource_count':len(graph['live_resource_roots']),'next_native_launch_original_source':launch,'approved_deletion_candidates':[],'files_deleted':0,'project_written':False,'mod_native_executables_Darwin_masters_not_candidates':True}
candidate_pin=write('compiled_candidate_screen.json',candidate_report)

e={'schema':'SPOT_EIGHTEENTH_NON_ARTIFACT_BUILD_GIT_AND_HELD_CACHE_READONLY_V1','status':'NO_NEW_SAFE_DELETE_CANDIDATES','approved_deletion_candidates':[],'approved_logical_reclaim_bytes':0,'approved_allocated_reclaim_bytes':0,'files_deleted':0,'project_written':False,'git_written':False,'scientific_business_executed':False,'scope':'Established non-validation core;159 held cache metadata;Git count/du/lost-found metadata;small immutable restoration/result controls. No full-project walk or large-object/scientific-content hash.','Root_R18_before_metadata_only':{'path':str(Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009/before.json')),'counts':root18['counts'],'project_du_KiB':root18['project_du_KiB'],'large_roots_and_large_files_are_source_inventory_not_full_content_proof':True},'core_current_summary':summary(core),'core_identity_fields':KEYS,'core_identity_stream_sha256':core_sha,'core_R17_identity_stream_exact':True,'core_R17_summary_exact':True,'core_symlink_metadata':links,'compiled_summary_by_suffix':compiled,'static_libraries_exact_paths':libraries,'root_native_program_exact_paths':programs,'root_library_program_identity_and_sizes_R17_exact':True,'current_direct_dependency_source_references':source_evidence,'build_vendor_cache_tmp_directory_observations':builds,'temporary_named_core_paths':temporary_core,'cache_R18_R17_complete_records_exact':True,'held_cache_fresh_summary':summary(cache),'held_cache_fresh_seven_identity_stream_sha256':stream_sha(cache),'held_cache_current_resource_count':prior['R12_original_held_resource_count'],'held_cache_current_source_derivative_paths':prior['R12_original_source_derivative_hold'],'R12_retired_fixed_cache_still_absent_count':len(deleted['candidates']),'Git_count_objects_observed':git_counts,'Git_du_observed_KiB':git_du,'Git_loose_count_change_vs_R17':git_counts['count']-prior['git_count_objects_actual_readonly']['count'],'Git_total_du_change_vs_R17_KiB':git_du['.git']-prior['git_du_actual_readonly_KiB']['.git'],'Git_growth_cause_not_inferred':True,'Git_statistics_not_reachability_or_content_verification':True,'Git_lost_found_summary':summary(lost),'Git_lost_found_seven_identity_stream_sha256':stream_sha(lost),'Git_lost_found_R17_exact':True,'Git_lost_found_largest_exact_paths':sorted(lost,key=lambda q:-q['logical_bytes'])[:2],'Git_objects_refs_logs_index_lost_found_HOLD_due_to_uncommitted_work_and_permanent_recovery':True,'git_gc_prune_clean_repack_fsck_not_run':True,'history_and_sensitive_config_content_not_read':True,'historical_rebuildable_compiled_without_full_current_exclusion_or_recovery_proof_HOLD':True,'same_size_not_duplicate_proof':True,'immutable_restore_controls_and_failed_results_fresh_full_SHA':small,'unique_V9_runtime_recovery_master_identity_exact':recovery,'permanent_gzip_full_rehash_or_decompression_not_done':True,'all_results_failed_records_seals_stdio_reports_restore_chains_current_runtime_INPUT_history_HOLD':True,'full_input_pins':pins,'earlier_source_discovery_absent_path_EXIT1_preserved':obs['earlier_source_discovery_path_error']}
e.update(status='COMPILED_CANDIDATES_PENDING_ROOT_FIXED_MANIFEST_REVIEW_NO_DELETIONS',proposed_compiled_candidate_screen=candidate_pin,proposed_compiled_candidate_summary=summary(potential),proposed_regenerable_object_count=len(object_candidates),proposed_exact_archive_copy_count=len(archive_candidates),frozen_object_HOLD_count=len(fixed),current_source_context_object_HOLD_count=len(object_review_hold),different_archive_HOLD_count=len(archive_different),historical_rebuildable_compiled_without_full_current_exclusion_or_recovery_proof_HOLD=False,makefile_reference_alone_is_not_immutable_dependency_proof=True)
assert all(identity(q['path'])==q['identity'] for q in core+cache+lost)
rep=write('REPORT.json',e)
text=f'''第十八轮非 artifacts 构建/Git/缓存独立只读复查：向Root提出{len(potential)}个精确编译候选待完整固定清单核验，logical{summary(potential)['logical_bytes']:,}B、allocated{summary(potential)['allocated_bytes']:,}B；尚无删除批准，批准逻辑/分配回收量均0。仅写TMP，无项目或Git修改，无科学业务。

有限非validation核心{len(core)}普通文件，完整路径与七字段排序指纹和R17完全相同；独有inode logical{summary(core)['logical_bytes']:,}B、allocated{summary(core)['allocated_bytes']:,}B。未全项目walk或读取Git历史内容。build/target/dist/node_modules/vendor/tmp/temp等精确存在性见机器报告；没有新增可安全退役的根构建或临时批次。

当前必需：lib/Darwin_arm64/libDragon.a、Trivac/lib/Darwin_arm64/libTrivac.a、Utilib/lib/Darwin_arm64/libUtilib.a、Ganlib/lib/Darwin_arm64/libGanlib.a仍被当前V9/原trim链接源码直接引用；src/FLU.o仍被原activity auditor直接读取。上述source SHA和原行上下文fresh匹配。库/程序完整路径、logical/allocated和七字段与R17相同。
实际frozen集合与Makefile再生引用分开：完整binding expected{len(expected)}和graph canonical{len(canon)}/namespace{len(nsroots)}/alias{len(graph['aliases'])}/resource {len(binding['resource_info']['resource_roots'])}+{len(graph['live_resource_roots'])}交叉核。{len(fixed)}个.o真的命中frozen输入，精确路径在候选屏幕文件中，继续HOLD。{len(object_review_hold)}个不受frozen保护但在current依赖源码被basename引用，保守交Root审核上下文。其余{len(object_candidates)}个.o有保留源文件全文SHA+原Makefile再生规则，不命中上述保护，作为可清理候选；并非因为Makefile引用就全部保留。四src库全文与Darwin保留主本比较，{len(archive_candidates)}个byte-exact副本候选，{len(archive_different)}个不同字节HOLD。全部.mod、Darwin主库、bin/原程序不在候选。compiled_candidate_screen.json给每项exact路径/七身份/逻辑分配量/保留源或主本SHA及再生入口；这不是已执行清理或完整Root固定清单批准。

缓存{len(cache)}项，R18/R17完整records完全相同，fresh七身份逐项匹配；logical{summary(cache)['logical_bytes']:,}B，uniqueinode allocated{summary(cache)['allocated_bytes']:,}B。原resource HOLD及2个当前canonical源衍生HOLD继续保留；R12已删除{len(deleted['candidates'])}项仍absent，不重复报收益。有限核心.pyc为{compiled['.pyc']['regular_paths']}；.ruff_cache无普通文件，没有新安全项。

Git统计只读：.git{git_du['.git']:,}KiB、objects{git_du['.git/objects']:,}KiB、lost-found{git_du['.git/lost-found']:,}KiB；loose{git_counts['count']}较R17变化{git_counts['count']-prior['git_count_objects_actual_readonly']['count']:+d}，总Git分配统计变化{git_du['.git']-prior['git_du_actual_readonly_KiB']['.git']:+d}KiB；packs{git_counts['packs']}、packed{git_counts['in-pack']}、garbage{git_counts['garbage']}、prune-packable{git_counts['prune-packable']}。统计不证明可达性或备份，不归因新增历史捕获。lost-found{len(lost)}份七身份指纹与R17相同，logical{summary(lost)['logical_bytes']:,}B、allocated{summary(lost)['allocated_bytes']:,}B。两最大exact路径见JSON；大量未提交工作与恢复链仍需保留objects/refs/logs/index/lost-found，不进行gc/prune/clean/repack/fsck。

所有结果文档、失败/stdout/stderr/seal、永久恢复包及控制/ledger/RESTORE、唯一OUT9恢复主本与当前runtime/INPUT/full-history依赖保留。小不可变恢复/失败控制逐SHA核实；大永久gzip未重新全文hash/解压。完整冷INPUT和新增finalization成功不能取消旧失败、独立2000active/八精度门或恢复职责。本轮Rootbefore只作metadata概览，不冒充科学内容验证。

REPORT.json保存小来源pins、exact路径、分配/逻辑量与指纹；真实工具终态另外封存。一次查找旧TMP源错用不存在文件名而EXIT1，已保留观察后找到真实源文件，不是业务失败或业务重试。
'''
with (O/'REPORT.txt').open('x') as f:f.write(text)
print(json.dumps({'status':e['status'],'report':rep,'text_report':pin(O/'REPORT.txt')[1],'core_summary':summary(core),'cache_summary':summary(cache),'Git_lost_found_summary':summary(lost),'approved_deletion_candidates':[],'files_deleted':0,'project_written':False},ensure_ascii=False,sort_keys=True))
