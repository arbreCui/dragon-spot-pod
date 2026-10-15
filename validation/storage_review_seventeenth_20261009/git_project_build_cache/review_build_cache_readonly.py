from pathlib import Path
import json, hashlib, os, stat, collections

R=Path('/Users/wen/spot');V=R/'validation';O=Path('/private/tmp/spot_storage_review_seventeenth_build_cache_20261009')
T16=V/'storage_review_sixteenth_20261009';T15=V/'storage_review_fifteenth_20261009';T12=V/'storage_cleanup_twelfth_20261009'
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink');pins=[]
def ident(p):return [getattr(p.lstat(),'st_'+k) for k in KEYS]
def pin(p,wanted=None):
 p=Path(p);before=ident(p);assert p.is_file() and not p.is_symlink();b=p.read_bytes();assert ident(p)==before
 h=hashlib.sha256(b).hexdigest()
 if wanted:assert h==wanted,(str(p),h,wanted)
 q={'path':str(p),'sha256':h,'bytes':len(b),'identity':before};pins.append(q);return b,q
def read(p):return json.loads(pin(p)[0])
def meta(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return {'path':str(p),'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'identity':[getattr(s,'st_'+k) for k in KEYS]}
def summary(rows):
 u={(q['identity'][0],q['identity'][1]):q for q in rows}
 return {'regular_paths':len(rows),'unique_inodes':len(u),'logical_bytes':sum(q['logical_bytes'] for q in u.values()),'allocated_bytes':sum(q['allocated_bytes'] for q in u.values())}
def digest_rows(rows):
 h=hashlib.sha256()
 for q in sorted(rows,key=lambda x:x['path']):h.update(json.dumps([q['path'],q['identity']],ensure_ascii=False,separators=(',',':')).encode()+b'\n')
 return h.hexdigest()
root17=read('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json')
root16=read('/private/tmp/spot_storage_sixteenth_root_readonly_20261009/after.json')
prior=read(T16/'recovery_git_and_project/REPORT.json')
priorcache=read(T15/'spot_fifteenth_storage_metadata_inventory_20261009.json')['cache_like']
boundary=read(T12/'current_protection_review/cache_64_current_canonical_source_boundary.json')
cache12=read(T12/'cache_manifest.json');baseline_tool=read('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/actual_baseline_tool_return.json')
for p in (T16/'REPORT.txt',T15/'REPORT.txt',T12/'REPORT.txt',T15/'git_and_project_build/REPORT.txt',V/'storage_cleanup_ninth_20261009/REPORT.txt'):pin(p)
oldbytes,oldpin=pin('/private/tmp/spot_storage_recheck_20261009/current_regular_file_metadata.json')
oldall=json.loads(oldbytes);base={q['path']:q for q in oldall if not Path(q['path']).is_relative_to(V)};del oldall,oldbytes
core=[]; corelinks=[]
for stem in ('src','Trivac','Ganlib','Utilib','lib','bin','data','SPOT_doc','script','.ruff_cache'):
 top=R/stem
 if not top.exists():continue
 for folder,ds,ns in os.walk(top,followlinks=False):
  for name in ds+ns:
   p=Path(folder)/name;s=p.lstat()
   if stat.S_ISREG(s.st_mode):core.append(meta(p))
   elif stat.S_ISLNK(s.st_mode):corelinks.append({'path':str(p),'target':os.readlink(p),'identity':ident(p)})
for p in R.iterdir():
 if p.is_file() and not p.is_symlink():core.append(meta(p))
cur={q['path']:q for q in core};added=sorted(cur.keys()-base.keys());missing=sorted(base.keys()-cur.keys());changed=sorted(p for p in cur.keys()&base.keys() if cur[p]['identity']!=[base[p][k] for k in KEYS])
oldcore=[{'path':p,'identity':[q[k] for k in KEYS]} for p,q in base.items()]
cache_now=[meta(q['path']) for q in root17['cache_like']]
cachemap={q['path']:q for q in cache_now};cache16={q['path']:q for q in root16['cache_like']}
cache15={str(R/q['path']):(q['size'],q['allocated']) for q in priorcache}
assert set(cachemap)==set(cache16)==set(cache15)
assert all(q['identity']==cache16[p]['identity'] and (q['logical_bytes'],q['allocated_bytes'])==cache15[p] for p,q in cachemap.items())
assert all(q['identity']==x['identity'] for q,x in zip(cache_now,root17['cache_like']))
gone12=[]
for x in cache12['candidates']:
 p=x['path'];assert not os.path.lexists(p);gone12.append(p)
libraries=[q for q in core if Path(q['path']).suffix=='.a'];programs=[q for q in core if Path(q['path']).name in ('Dragon','Trivac','Ganlib')]
oldlibs={q['path']:q for q in prior['root_archive_and_program_paths']}
libcmp={'added':sorted(set(q['path'] for q in libraries+programs)-set(oldlibs)),'missing':sorted(set(oldlibs)-set(q['path'] for q in libraries+programs)),'changed':sorted(q['path'] for q in libraries+programs if q['path'] in oldlibs and q['identity']!=oldlibs[q['path']]['identity'])}
sources=prior['source_dependency_references'];source_evidence=[]
for q in sources:
 b,p=pin(q['path']);lines=b.decode().splitlines();i=q['line'];source_evidence.append({**q,'source_sha256':p['sha256'],'source_excerpt':{'first_line':max(1,i-1),'lines':lines[max(0,i-2):i+3]}})
for p in (R/'Trivac/src/Makefile',R/'Ganlib/src/Makefile',R/'Utilib/src/Makefile'):pin(p)
small=[]
for q in prior['R15_small_control_full_SHA_preserved']+prior['retained_result_and_failure_record_small_pins']:
 b,p=pin(q['path'],q['sha256']);small.append(p)
rootdocs=[];r16docs_changed=[]
for rel,sha in root17['document_sha256'].items():
 b,p=pin(R/rel,sha);rootdocs.append(p)
 if root16['document_sha256'].get(rel)!=sha:r16docs_changed.append({'path':str(R/rel),'R16_sha256':root16['document_sha256'].get(rel),'R17_sha256':sha})
gzip=[meta(q['path']) for q in prior['gzip_exact_metadata_paths']]
gzip_identity_changes=[q['path'] for q,x in zip(gzip,prior['gzip_exact_metadata_paths']) if q['identity']!=x['identity']]
recovery_master=meta(prior['V9_runtime_unique_restore_master_current_metadata']['path'])
assert recovery_master['identity']==prior['V9_runtime_unique_restore_master_current_metadata']['identity']
lost=[]
for folder,ds,ns in os.walk(R/'.git/lost-found',followlinks=False):
 for n in ns:
  p=Path(folder)/n
  if stat.S_ISREG(p.lstat().st_mode):lost.append(meta(p))
actual=read(O/'initial_actual_readonly_observations.json');count_output=actual['git_count_objects']['output'];git_counts={}
for line in count_output.splitlines():
 k,val=line.split(': ',1);git_counts[k]=int(val)
git_du={}
for line in actual['git_du']['output'].splitlines():
 value,p=line.split('\t',1);git_du[p]=int(value)
assert all(actual[k]['exit_code']==0 for k in ('git_count_objects','git_du','source_reference_search','scope_shape_read'))
build_roots=[]
for rel in ('build','target','dist','node_modules','.cache','.ruff_cache','.pytest_cache','__pycache__','src/build','Trivac/build','Ganlib/build','Utilib/build'):
 p=R/rel;build_roots.append({'path':str(p),'present':os.path.lexists(p),'is_directory':p.is_dir() and not p.is_symlink(),'regular_files_in_reviewed_core':sum(Path(q['path']).is_relative_to(p) for q in core)})
compiled={s:summary([q for q in core if Path(q['path']).suffix==s]) for s in ('.o','.a','.pyc')}
evidence={'schema':'SPOT_SEVENTEENTH_ROOT_BUILD_GIT_AND_HELD_CACHE_READONLY_REVIEW_V1','status':'NO_NEW_SAFE_DELETE_CANDIDATES','approved_delete_paths':[],'approved_logical_reclaim_bytes':0,'approved_allocated_reclaim_bytes':0,'write_scope':str(O),'Root_R17_baseline_actual_tool_evidence':baseline_tool,'Root_R17_project_du_KiB':root17['project_du_KiB'],'R16_after_project_du_KiB':root16['project_du_KiB'],'R16_to_R17_observed_project_du_increase_KiB':root17['project_du_KiB']-root16['project_du_KiB'],'observed_growth_not_given_content_or_cause_or_deletion_inference':True,'core_R16_recognized_baseline':oldpin,'R16_core_comparison_previously_exact':prior['core_no_new_missing_changed_paths_vs_baseline_in_R15_reader'],'core_current_summary':summary(core),'core_prior_R16_summary':prior['core_summary'],'core_complete_regular_identity_comparison':{'identity_fields':KEYS,'current_identity_stream_sha256':digest_rows(core),'R16_recognized_baseline_identity_stream_sha256':digest_rows(oldcore),'added':added,'missing':missing,'changed':changed,'all_regular_paths_and_seven_fields_exact':not added and not missing and not changed},'core_symlinks_current_metadata_without_prior_link_completeness_claim':corelinks,'compiled_summary_by_suffix':compiled,'static_libraries_exact_paths':libraries,'root_native_program_exact_paths':programs,'archive_program_identity_comparison_to_R16':libcmp,'current_direct_dependency_source_references':source_evidence,'new_build_target_cache_directory_observations':build_roots,'cache_R16_R15_exact_set_and_identity_match':True,'cache_current_summary':summary(cache_now),'cache_identity_stream_sha256':digest_rows(cache_now),'cache_new_paths':[],'cache_missing_held_paths':[],'R12_original_held_resource_count':boundary['resource_root_HOLD_files'],'R12_original_source_derivative_hold':boundary['extra_current_canonical_source_cache_HOLD'],'R12_previously_deleted_fixed_paths_still_absent_count':len(gone12),'R12_deleted_candidates_not_relisted':True,'git_count_objects_actual_readonly':git_counts,'git_du_actual_readonly_KiB':git_du,'Git_loose_count_change_since_R16':git_counts['count']-prior['git_count_objects']['count'],'Git_total_du_KiB_change_since_R16':git_du['.git']-prior['git_du_KiB']['total'],'git_lost_found_current_summary':summary(lost),'git_lost_found_R16_summary':prior['git_lost_found_metadata'],'git_lost_found_largest_paths':sorted(lost,key=lambda q:-q['logical_bytes'])[:2],'git_lost_found_path_identity_stream_sha256':digest_rows(lost),'git_stats_are_not_reachability_or_content_verification':True,'git_object_history_reflog_index_contents_not_read':True,'git_gc_prune_repack_fsck_clean_not_run':True,'Git_current_uncommitted_work_and_recovery_HOLD':True,'permanent_gzip_recovery_summary':summary(gzip),'permanent_gzip_R16_summary':prior['all97_permanent_gzip_current_summary'],'permanent_gzip_identity_changes_since_R16':gzip_identity_changes,'permanent_gzip_not_full_rehashed_or_decompressed':True,'runtime_unique_recovery_master_identity_exact':recovery_master,'small_restore_controls_and_old_failed_receipts_full_SHA_preserved':small,'R17_Root_baseline_document_SHA_preserved':rootdocs,'R16_to_R17_known_document_SHA_differences_reported_not_attributed':r16docs_changed,'all_results_failures_seals_ledgers_restore_chains_and_current_dependency_paths_HOLD':True,'current_runtime_or_history_gate_scope_not_narrowed':True,'no_scientific_business_or_full35GB_content_read':True,'project_or_git_written':False,'actual_deletions':0,'full_input_pins':pins,'scope_limit':'Only the established nonvalidation core,159 held caches,97 recovery archive metadata,small controls/failed receipts,Git stats/lost-found metadata. Whole project preservation is Root responsibility; no new allproject walk or baseline copy.'}
evidence.update(approved_deletion_candidates=[],files_deleted=0,project_written=False)
assert not added and not missing and not changed and not any(libcmp.values()) and not gzip_identity_changes
for p in root17['cache_like']:assert ident(Path(p['path']))==p['identity']
for n,d in [('REPORT.json',evidence)]:
 p=O/n;assert not p.exists();p.write_text(json.dumps(d,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
text=f'''第十七轮 Git/root native/build/cache 独立只读复查：新可安全删除候选0，批准逻辑和分配回收量均0。本代理只写TMP，不删文件、不改Git/项目、不gc/prune/clean/repack/fsck，不执行科学业务。

与R16对比：Root本轮真实7fef04 EXIT0完整项目metadata基线，项目{root17['project_du_KiB']:,}KiB，相对R16after增加{root17['project_du_KiB']-root16['project_du_KiB']:,}KiB（{(root17['project_du_KiB']-root16['project_du_KiB'])/1024:.8f}MiB）。总量增幅不证明具体新内容来源。独立fresh仅检查非validation核心{len(core)}普通文件，逐完整路径和七字段与R16已认可原metadata基线完全相同；新增/缺席/变化均0。核心独有inode分配{summary(core)['allocated_bytes']:,}B（{summary(core)['allocated_bytes']/2**20:.3f}MiB）。Root负责全项目before/after，本报告不冒充全项目内容或科学INPUT证明。

编译HOLD：.o {compiled['.o']['regular_paths']}项/{compiled['.o']['allocated_bytes']:,} allocated B；.a {compiled['.a']['regular_paths']}项/{compiled['.a']['allocated_bytes']:,}B。8库及6原程序完整exact路径、logical/allocated、七field都与R16一致，详见REPORT.json。现V9factory仍读root libDragon.a，原trimproducer仍链接四库，auditor仍读取src/FLU.o，四Makefile明确archive/object/target依赖。相同size不证明重复，也没有新增full依赖排除/可靠恢复证据，旧compiled HOLD不解锁。root build/target/dist/node_modules等存在性见JSON；没有新不受依赖的小构建批次。

缓存：完整{len(cache_now)}项与R16/R15/R12保留集合相同，逐现存身份完全相同；logical{summary(cache_now)['logical_bytes']:,}B，uniqueinode allocated{summary(cache_now)['allocated_bytes']:,}B。原157项resource HOLD+2项封存源码衍生HOLD继续保留。R12真已删{len(gone12)}项仍absent，不重复列为本轮收益；.ruff_cache无普通文件。没有新增可安全删除cache。

Git只读真实count/du：.git {git_du['.git']:,}KiB，objects{git_du['.git/objects']:,}KiB，lost-found{git_du['.git/lost-found']:,}KiB；loose {git_counts['count']}（较R16+{git_counts['count']-prior['git_count_objects']['count']}），packs{git_counts['packs']}/packed{git_counts['in-pack']}，garbage{git_counts['garbage']}、prune-packable{git_counts['prune-packable']}。这些不是可达性/已备份证明，未读历史或大objects。lost-found {summary(lost)['regular_paths']}份、logical{summary(lost)['logical_bytes']:,}B/allocated{summary(lost)['allocated_bytes']:,}B，两最大恢复对象路径见JSON。HOLD .git/objects、refs、logs、index和lost-found；现大量未提交工作与永久恢复均无逐项可安全丢弃证明。R9归档捕获为旧文档来源证据，本次Git新增原因不推断，不批准清空恢复对象或任何Git维护。

恢复和结果：97永久gzip七field与R16全同，当前logical{summary(gzip)['logical_bytes']:,}B/allocated{summary(gzip)['allocated_bytes']:,}B；未重hash或解压全部恢复包。R9材料89gzip、R14 metadata8gzip、其manifest/ledger/RESTORE/恢复工具及唯一OUT9恢复主本继续保留。小恢复control和旧V8运行失败/coldV3 RSS失败/新cold声明收据全文SHA保持；R17 README/科学progress等按本轮Rootbefore SHA保持。所有报告、原结果、失败、stdio、seal、源码、永久恢复链和当前runtime/INPUT/全history资源仍HOLD；成功INPUT/PREP不取消旧失败或2000active八门要求。

完整小机器证据/来源pin/精确路径/容量/比较指纹见REPORT.json；真实工具收据另封存。没有新增多MBbaseline、全项目walk或35GB内容读取。分配量不是APFS即时独占空闲承诺；本轮批准回收仍0。
'''
p=O/'REPORT.txt';assert not p.exists();p.write_text(text)
print(json.dumps({'status':evidence['status'],'report':{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'evidence':{'path':str(O/'REPORT.json'),'sha256':hashlib.sha256((O/'REPORT.json').read_bytes()).hexdigest()},'core_regular_paths':len(core),'core_identity_changes':len(added)+len(missing)+len(changed),'cache_count':len(cache_now),'approved_delete_paths':[],'approved_allocated_reclaim_bytes':0,'project_written':False},ensure_ascii=False,sort_keys=True))
