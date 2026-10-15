from pathlib import Path
import json,hashlib,os,stat,collections
R=Path('/Users/wen/spot');V=R/'validation';O=Path('/private/tmp/spot_storage_sixteenth_recovery_readonly_20261009');F=V/'storage_review_fifteenth_20261009';T14=V/'storage_cleanup_fourteenth_20261009'
def read(p):return json.loads(Path(p).read_text())
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),allocated_bytes=p.stat().st_blocks*512)
def metadata(p):
 p=Path(p);s=p.lstat();return dict(path=str(p),logical_bytes=s.st_size,allocated_bytes=s.st_blocks*512,identity=[getattr(s,'st_'+k) for k in ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')])
def walk_roots(roots):
 rows=[]
 for root in roots:
  for b,ds,ns in os.walk(root,followlinks=False):
   for n in ns:
    p=Path(b)/n
    if stat.S_ISREG(p.lstat().st_mode):rows.append(metadata(p))
 return rows
def summary(xs):
 u={(x['identity'][0],x['identity'][1]):x for x in xs};return dict(regular_paths=len(xs),unique_inodes=len(u),logical_bytes=sum(x['logical_bytes'] for x in u.values()),allocated_bytes=sum(x['allocated_bytes'] for x in u.values()))
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
prior=read(F/'recovery_and_old_reports/REPORT.json');oldsummary=read(F/'recovery_and_old_reports/inventory_summary.json')
roots=[Path(x['root']) for x in oldsummary['roots']];rows=walk_roots(roots);now=summary(rows)
per_root={str(p):summary([x for x in rows if Path(x['path']).is_relative_to(p)]) for p in roots}
assert now['regular_paths']==prior['regular_paths']
small=[]
for x in prior['small_control_pins']:
 z=pin(x['path']);assert z['sha256']==x['sha256'];small.append(z)
status=read(T14/'Root_actual_metadata_retirement_and_protected_restore.json');retired=status['final_retired_metadata_paths'];assert all(not os.path.lexists(p) for p in retired);assert Path(status['held_original_path']).is_file()
meta_manifest=read(T14/'audit_metadata_manifest.json');archives=sorted({x['archive_path'] for x in meta_manifest['records']});assert all(Path(p).is_file() for p in archives)
runtime_manifest=read(T14/'runtime_retirement_manifest.json');assert all(not os.path.lexists(x['path']) for x in runtime_manifest['candidates']);master=runtime_manifest['candidates'][0]['retained_primary'];assert Path(master['path']).is_file() and Path(master['path']).stat().st_size==master['size_bytes']
# All restored material bytes/metadata archives are permanent primary recovery sources.
gz=[x for x in rows if x['path'].endswith('.gz')];holdlarge=[]
for x in prior['large_HOLD_paths']:
 z=metadata(x['path']);z['reason']=x['reason'];z['logical_and_allocated_same_R15']=z['logical_bytes']==x['bytes'] and z['allocated_bytes']==x['allocated_bytes'];holdlarge.append(z)
priorcore=read(F/'git_and_project_build/retention_evidence.json')
oldall=read(Path('/private/tmp/spot_storage_recheck_20261009/current_regular_file_metadata.json'));base={x['path']:x for x in oldall if not Path(x['path']).is_relative_to(V)}
core=walk_roots([R/x for x in ('src','Trivac','Ganlib','Utilib','lib','bin','data','SPOT_doc','script','.ruff_cache')])
for p in R.iterdir():
 if p.is_file() and not p.is_symlink():core.append(metadata(p))
current={x['path']:x for x in core};keys=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
added=sorted(set(current)-set(base));gone=sorted(set(base)-set(current));changed=sorted(p for p in set(base)&set(current) if current[p]['identity']!=[base[p][k] for k in keys]);assert not added and not gone and not changed
compiled=[x for x in core if Path(x['path']).suffix in ('.o','.a','.pyc')];bins=[x for x in core if Path(x['path']).name in ('Dragon','Trivac','Ganlib')]
rootbefore=Path('/private/tmp/spot_storage_sixteenth_root_readonly_20261009/before.json');fresh=read(rootbefore);r15after=read(F/'spot_fifteenth_storage_preservation_after_20261009.json');freshcache=fresh['cache_like'];r15cache=read(F/'spot_fifteenth_storage_metadata_inventory_20261009.json')['cache_like']
oldcache={str(R/x['path']):[x['size'],x['allocated']] for x in r15cache};newcache={x['path']:[x['bytes'],x['allocated_bytes']] for x in freshcache};assert oldcache==newcache
for x in freshcache:assert metadata(x['path'])['identity']==x['identity']
for p,h in fresh['document_sha256'].items():assert pin(R/p)['sha256']==h
lost=walk_roots([R/'.git/lost-found']);lostsummary=summary(lost)
source_refs=[dict(path=str(R/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'),line=291,reason='ROOT static library input remains direct current source dependency'),dict(path=str(R/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_last_cprime_trim_production.py'),line=552,reason='original four root static archive link inputs'),dict(path=str(R/'validation/axial_material/audit_source_factor_production_activity.py'),line=181,reason='reads root src/FLU.o and static archive'),dict(path=str(R/'src/Makefile'),line=252,reason='archive/object and Dragon target dependencies; duplicate sized source/root outputs not a new retirement proof')]
keptdocs=[V/'storage_review_fifteenth_20261009/REPORT.txt',T14/'REPORT.txt',T14/'RESTORE.txt',V/'axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/REPORT.txt',V/'axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/run_terminal_return.json',R/'validation/artifacts/axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v3-20261008/cold_failure_terminal_return.json',R/'validation/artifacts/axial-material-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-terminal-scipy-env-physical-basis-own-pid-peak-v9-20261009/declaration_terminal_return.json']
evidence=dict(schema='SPOT_SIXTEENTH_RECOVERY_GIT_AND_NONVALIDATION_READONLY_RECHECK_V1',status='NO_NEW_SAFE_DELETE_CANDIDATES',approved_delete_paths=[],approved_reclaim_bytes=0,root_fresh_small_baseline=pin(rootbefore),root_actual_inventory_tool=dict(initial_chunk_id='39e207',session_id=42958,terminal_chunk_id='a21d0d',exit_code=0,closed=True),root_project_du_KiB=fresh['project_du_KiB'],R15_after_project_du_KiB=r15after['project_du_KiB'],project_du_increase_KiB=fresh['project_du_KiB']-r15after['project_du_KiB'],project_increase_reason_not_inferred_from_metadata=True,R15_and_R16_preservation_counts_different_exclusion_scopes_not_subtracted=True,recovery_directories=per_root,recovery_current_summary=now,R15_recovery_summary=dict(regular_paths=prior['regular_paths'],allocated_bytes=prior['allocated_unique_inode_bytes']),all97_permanent_gzip_current_summary=summary(gz),gzip_exact_metadata_paths=gz,R14_8_archives_present=True,R14_9_retired_JSON_absent=True,R14_protected_baseline_present=metadata(status['held_original_path']),R14_5_runtime_copies_still_absent=True,V9_runtime_unique_restore_master_current_metadata=metadata(master['path']),large_old_audit_json_HOLD=holdlarge,R15_small_control_full_SHA_preserved=small,core_summary=summary(core),R15_core_summary=priorcore['fresh_nonvalidation_project_core'],core_no_new_missing_changed_paths_vs_baseline_in_R15_reader=dict(added=added,missing=gone,changed=changed),compiled_core_summary_by_suffix={s:summary([x for x in compiled if Path(x['path']).suffix==s]) for s in sorted({Path(x['path']).suffix for x in compiled})},root_archive_and_program_paths=[x for x in core if Path(x['path']).suffix=='.a' or Path(x['path']).name in ('Dragon','Trivac','Ganlib')],source_dependency_references=source_refs,Root_fresh_cache_159_path_size_alloc_exact_R15=True,cache_summary=dict(paths=len(freshcache),logical_bytes=sum(x['bytes'] for x in freshcache),allocated_bytes=sum(x['allocated_bytes'] for x in freshcache)),core_ruff_cache_files=[x for x in core if '/.ruff_cache/' in x['path']],git_du_KiB=dict(total=2943612,objects=2712712,lost_found=230372),R15_git_du_KiB=priorcore['git_du_KiB'],git_du_increase_KiB=2943612-priorcore['git_du_KiB']['total'],git_count_objects=dict(count=3089,size_KiB=2558532,in_pack=6890,packs=3,size_pack_KiB=153911,prune_packable=0,garbage=0,size_garbage_KiB=0),R15_git_count_objects=priorcore['git_count_objects_actual_readonly_output'],git_lost_found_metadata=lostsummary,largest_lost_found_paths=sorted(lost,key=lambda x:-x['logical_bytes'])[:2],git_objects_or_history_contents_not_read=True,git_fsck_gc_prune_repack_not_run=True,git_and_large_uncommitted_recovery_HOLD=True,retained_result_and_failure_record_small_pins=[pin(p) for p in keptdocs],old_failures_not_reclassified=True,all_recovery_full_bytes_not_rehashed_or_decompressed=True,scientific_full35GB_not_rehashed=True,scientific_business_not_executed=True,project_formal_ART_git_not_written=True,write_scope=str(O))
write('REPORT.json',evidence)
(O/'REPORT.txt').write_text('''第十六轮恢复/Git/非validation只读结论：新增可安全删除项0，批准回收量0。仅TMP报告，无删除/压缩/恢复/Git维护/科学业务。

R15后增量：Root fresh真实39e207/42958→a21d0d EXIT0，项目155,866,632KiB，R15after155,781,444KiB，观测增加85,188KiB（83.1914MiB）。不同轮preservation counts排除目录不同，不把count差当新增文件审计，也不从总占用推断新内容原因。README/current_progress已按本轮before的全文SHA复核，未写这些文档。Root当前159缓存path/size/allocated与R15完整相等，逐159身份与fresh before相等；没有新clear cache。非validation3016 regular/uniqueinode，logical/allocated详见JSON（allocated146,280,448B），逐7field与R15 reader所用metadata完全相同，新增/缺席/变化均0。.ruff_cache无普通文件。

Git：.git2,943,612KiB，objects2,712,712KiB，lost-found230,372KiB；相比R15统计增432KiB，loose3026→3089（+63），3packs/6890packed和garbage0/prune-packable0保持。只读du/count和lost-found metadata，不读取大object/历史/reflog内容，不查敏感配置，不执行fsck/gc/repack/prune。HOLD .git/objects、refs、logs、index、lost-found/other。lost-found79独有inode，235,627,205 logical/235,900,928allocated B；最大5351fb9cb8f5cbbfc53a2c961fad91117c1a3db6为228,676,484logical/228,679,680allocated B，次大2fbe5be57a931a24545f265cc8b54d184dce03d3为6,530,116/6,533,120B。未提交工作及恢复对象没有准确外部替代证明，不能清空。R9旧REPORT说明历史大归档捕获来源；本次新增63对象原因不推断。

旧清理/恢复：14个目录仍873普通文件，97永久gzip；准确现存logical/allocated和97路径写入REPORT.json。R15小恢复control全部fresh全文SHA保持，R14退休9JSON和5旧runtime路径仍absent，保护R1 baseline原路径仍present，8 metadata archives及V9 runtime唯一恢复master仍present。没有再解压/全hash2.39GiB永久档案；原R9/R14完整无损证明和restore映射必须保留。R9 packed_material_intermediates/89材料gzip恢复已退役raw及更早工作副本；R14 metadata_archives/8gzip恢复9旧清单，不是过期报告副本。R13/R14已退休程序不重复列为本轮候选。

大审计JSON继续HOLD，准确bytes见JSON：storage_cleanup_20261008/preservation_baseline.json（43,033,170B，旧protected index）；R9 all_eight_rounds_explicit_restoration_source_paths_and_fresh_stat.json（16,485,047B，cross_prior recovery reader）；R9 fresh_metadata_scan.json（12,237,350B，候选边界证据）；build_cache_metadata_screen.json（9,405,989B）和compiled_exact_screen_and_holds.json（5,572,118B，原full compiled review）；T10/T11 result_document_full_sha_baseline.json（12,686,315/9,093,035B，原清理reader绑定）。不能因metadata-only直接unlink已封存reader输入。

项目非validation .o1383条35,663,872allocated B；.a8条65,978,368B。8静态库准确路径，以及src/Dragon、bin/Darwin_arm64/Dragon、Trivac/Ganlib各src/bin程序准确size/alloc见JSON。原V9factory:291、trimproducer:552、auditor:181以及Makefiles继续直接读取root库/object/原目标。相同size不是SHA重复证明；本轮没有新的内容相等和完整依赖排除证据，不解锁旧compiled HOLD。核心总量仅139.5MiB，删除全部也不是多GiB大项，且会破坏源码构建/当前校核/恢复能力。

保留结果与失败：全部原REPORT、结果正文、图表、日志、失败收据、stdout/stderr、源码/reader、seal/manifest/retirementledger/restore入口、保护索引继续原路径保留。V8真实RUN失败、旧coldV3 RSS失败、旧nu-fission精度FAIL不能因新INPUT/新declare成功改写。V9 runtime/wholeINPUT+Rootreceipt以及新cold declaration source/receipt仍是当前完整证据，不能当旧临时复制资料删。结果摘要不能替代唯一原始数据、恢复primary或完整失败观察。selected small docs/真实失败收据freshSHA在JSON；没有重新科学验收或运行任何阶段。

本轮limited root概览+873cleanup metadata+3016core metadata+selected small controlSHA，无新多MBbaseline或全项目walk；不hash35GB科学输入，不读Git大历史，不改任何项目路径。文件allocated与APFS即时独占空闲不同；以上新增安全回收为0。
''')
for n in ['REPORT.txt','REPORT.json']:print(json.dumps(pin(O/n)))
