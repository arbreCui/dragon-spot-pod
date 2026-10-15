from pathlib import Path
import json,hashlib,os,stat,collections
R=Path('/Users/wen/spot');O=Path('/private/tmp/spot_storage_nonart_git_retention_readonly_20261009')
def pin(p):p=Path(p);return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size=p.stat().st_size)
def write(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
metadata=Path('/private/tmp/spot_storage_recheck_20261009/current_regular_file_metadata.json')
old=json.loads(metadata.read_text());rows=[x for x in old if not Path(x['path']).is_relative_to(R/'validation/artifacts')]
fresh=[];missing=[];changed=[];keys=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')
for x in rows:
 p=Path(x['path'])
 try:s=p.lstat()
 except FileNotFoundError:missing.append(x['path']);continue
 z={k:getattr(s,'st_'+k) for k in keys};z.update(path=x['path'],allocated=s.st_blocks*512)
 if any(z[k]!=x[k] for k in keys):changed.append(x['path'])
 if stat.S_ISREG(s.st_mode):fresh.append(z)
def summarize(xs):
 u={(x['dev'],x['ino']):x for x in xs};return dict(paths=len(xs),unique_inodes=len(u),logical_bytes=sum(x['size'] for x in u.values()),allocated_bytes=sum(x['allocated'] for x in u.values()))
core=[x for x in fresh if not Path(x['path']).is_relative_to(R/'validation')]
compiled=[x for x in fresh if Path(x['path']).suffix in ('.o','.a','.pyc')]
perroot={}
for name in sorted({Path(x['path']).relative_to(R).parts[0] for x in core}):perroot[name]=summarize([x for x in core if Path(x['path']).relative_to(R).parts[0]==name])
gitstats={};lost=[]
for rel in ('objects','lost-found','refs','logs'):
 xs=[];ds_count=0;links=0;p=R/'.git'/rel
 for b,ds,fs in os.walk(p,followlinks=False):
  ds_count+=len(ds)
  for n in fs:
   q=Path(b)/n;s=q.lstat()
   if stat.S_ISLNK(s.st_mode):links+=1;continue
   if stat.S_ISREG(s.st_mode):xs.append(dict(path=str(q),dev=s.st_dev,ino=s.st_ino,nlink=s.st_nlink,size=s.st_size,allocated=s.st_blocks*512))
 gitstats[rel]={**summarize(xs), 'directory_paths_excluding_root':ds_count,'symlinks':links,'content_read':False}
 if rel=='lost-found':lost=sorted(xs,key=lambda x:-x['size'])[:2]
archives=R/'validation/storage_cleanup_ninth_20261009/packed_material_intermediates';xs=[]
for b,ds,fs in os.walk(archives,followlinks=False):
 for n in fs:
  p=Path(b)/n;s=p.lstat()
  if stat.S_ISREG(s.st_mode):xs.append(dict(path=str(p),dev=s.st_dev,ino=s.st_ino,size=s.st_size,allocated=s.st_blocks*512))
sourceevidence=[dict(path=str(R/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'),line=291,reason='current formal V9 compile/link identity reads ROOT/lib/Darwin_arm64/libDragon.a'),dict(path=str(R/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_last_cprime_trim_production.py'),line=552,reason='retained trim source links all four root static libraries'),dict(path=str(R/'validation/axial_material/audit_source_factor_production_activity.py'),line=181,reason='auditor directly reads src/FLU.o and root libDragon.a'),dict(path=str(R/'src/Makefile'),line=252,reason='build target libDragon.a depends on source objects; Dragon target links root lib archives'),dict(path=str(R/'Trivac/src/Makefile'),line=223,reason='current source-library target and original link dependencies'),dict(path=str(R/'Utilib/src/Makefile'),line=206,reason='current source-library target original build dependencies'),dict(path=str(R/'Ganlib/src/Makefile'),line=239,reason='current source-library target original build dependencies')]
reports=[R/'validation/storage_cleanup_ninth_20261009/REPORT.txt',R/'validation/storage_cleanup_twelfth_20261009/REPORT.txt',R/'validation/storage_cleanup_thirteenth_20261009/REPORT.txt',R/'validation/storage_cleanup_fourteenth_20261009/REPORT.txt',R/'validation/storage_cleanup_fourteenth_20261009/RESTORE.txt']
evidence=dict(schema='SPOT_NONART_GIT_SOURCE_CACHE_RETENTION_READONLY_V1',status='NO_NEW_SAFE_DELETE_FIXED_ITEMS',approved_delete_paths=[],estimated_approved_reclaim_bytes=0,root_metadata_scope='Reused existing Root metadata; fresh lstat only its non-artifacts file subset. No full project walk or scientific data/object content reads.',fresh_prior_metadata_nonartifact_scope=summarize(fresh),fresh_nonvalidation_project_core=summarize(core),core_by_top_directory=perroot,compiled_nonartifact_by_suffix={s:summarize([x for x in compiled if Path(x['path']).suffix==s]) for s in sorted({Path(x['path']).suffix for x in compiled})},retained_static_archive_exact_paths=[x for x in compiled if Path(x['path']).suffix=='.a'],git_directory_metadata_only=gitstats,git_count_objects_actual_readonly_output=dict(count=3026,size_KiB=2558100,in_pack=6890,packs=3,size_pack_KiB=153911,prune_packable=0,garbage=0,size_garbage_KiB=0),git_du_KiB=dict(total=2943180,objects=2712280,lost_found=230372),git_largest_lost_found_exact_paths=lost,git_objects_or_lost_found_content_read=False,git_fsck_or_reflog_or_gc_or_repack_or_prune_called=False,git_history_and_large_uncommitted_recovery_must_be_preserved=True,git_growth_provenance='R9 REPORT historical documentary explanation: 89 restore gzip archives entered automatic local Git capture. This is not a causal finding from the current metadata-only audit.',material_permanent_restore_archive_current_metadata=summarize(xs),source_dependency_evidence=sourceevidence,source_report_pins=[pin(p) for p in reports],prior_metadata_missing_9_already_retired_R14_paths=missing,prior_metadata_changed_3_intentional_R14_paths=changed,changes_observed_not_caused_by_this_reader=True,nonartifact_prior_scope_excludes_new_R14_docs=True,R14_retired_JSONs_not_relisted_for_deletion=True,all_proposed_actions='HOLD; no deletion, mutation, compression, restore or business execution',formal_ART_git_or_source_written=False,write_scope=str(O))
write('retention_evidence.json',evidence)
text='''本轮只读结论：新增可安全删除固定项0，已证明可回收量0。没有执行删除、Git维护、压缩、恢复或业务。

Git：/Users/wen/spot/.git 2,943,180 KiB（约2.807 GiB）；objects 2,712,280 KiB；lost-found 230,372 KiB（約225 MiB）。真实只读git count-objects：3026 loose对象、3 packs/6890 packed对象，prune-packable=0、garbage=0。统计是对象与文件metadata，不是可达性/内容/历史验收。未读取大object、索引内容、reflog内容或敏感配置，未运行fsck/gc/repack/prune。
HOLD /Users/wen/spot/.git/objects、.git/refs、.git/logs、.git/index、.git/lost-found/other。lost-found 79独有inode，最大5351fb9cb8f5cbbfc53a2c961fad91117c1a3db6逻辑228,676,484B，另2fbe5be57a931a24545f265cc8b54d184dce03d3为6,530,116B。没有逐项匹配当前工作树或已批准恢复主本的证据，不能删。当前未提交工作量很大，丢弃任何恢复对象可能失去工作。名称相同/对象统计或garbage0不能证明已安全备份。
第九轮REPORT明确记录89份材料gzip曾进入自动本地Git捕获，Git由425MiB增约2.792GiB；这是旧文档的来源证据，本次不做新增历史因果推断。未来如只做不丢对象的打包压缩，需要保全refs/reflogs/index/loose/unreachable及独立恢复保障后专门审查；本轮不批准执行gc/repack，也不承诺回收量，gzip材料本身已压缩。

非artifacts：复用Root原inventory并只fresh lstat5855条非artifacts旧scope，不再全walk。现该旧scope5846普通文件，约2.873GiB；已缺席9项均R14正式退役旧JSON，3项改变是R1保护基线恢复及README/current_progress已审有意索引更新。此subset数字不含后来新增R14报告，不能当新整项目baseline。非validation项目本体3016文件/uniqueinode，仅146,280,448 allocated B（139.5MiB）。src约69.3MiB、lib24.0MiB、Trivac23.6MiB、bin8.7MiB、Ganlib6.3MiB、Utilib4.0MiB，不是下一批多GiB候选。
非artifacts .o=1383条/35,663,872 allocated B；.a=8条/65,978,368B；.pyc=2条/49,152B。根静态库与src副本不能凭大小判重复。HOLD准确库路径：
/Users/wen/spot/lib/Darwin_arm64/libDragon.a（24,626,264B）
/Users/wen/spot/src/libDragon.a（24,626,264B）
/Users/wen/spot/Trivac/lib/Darwin_arm64/libTrivac.a（5,801,632B）
/Users/wen/spot/Trivac/src/libTrivac.a（5,801,632B）
/Users/wen/spot/Ganlib/lib/Darwin_arm64/libGanlib.a（1,476,784B）
/Users/wen/spot/Ganlib/src/libGanlib.a（1,476,784B）
/Users/wen/spot/Utilib/lib/Darwin_arm64/libUtilib.a（1,073,776B）
/Users/wen/spot/Utilib/src/libUtilib.a（1,073,776B）。
现V9 formal factory:291和trim原producer:552-553直接引用root静态库；audit_source_factor_production_activity.py:181读取src/FLU.o；四Makefiles依赖原object/archive目标。即使多数.o理论可再编译，当前正式pin/回放/原compiler来源及未提交源码尚未逐项排除，禁止按后缀整批删。原R9/R12/R14 compiled HOLD没有新的解锁证据。两pyc依原R12封存source规则保留；没有新增普通cache可批量清。

恢复资料：HOLD /Users/wen/spot/validation/storage_cleanup_ninth_20261009/packed_material_intermediates/ 全89永久gzip。当前metadata逻辑2,546,524,057B、allocated2,546,712,576B（约2.372GiB），是已删除89原material及更早120工作副本的准确恢复来源。仅metadata当前stat，未重新全读解压验证，不能把这些已压缩恢复档当普通下载。HOLD /Users/wen/spot/validation/storage_cleanup_fourteenth_20261009/metadata_archives/恢复档、audit_metadata_manifest.json、runtime_retirement_manifest.json、RESTORE.txt与manage_*恢复入口：已经退役的9清单/5程序副本需要这些恢复源；R1 preservation_baseline.json仍受旧保护索引引用，已恢复，不能再次压缩退役。各轮sameSHA保留主本、retirement ledger与restore映射继续保留，不重复列R13/R14已删项。

最小结果文档必须留下：各storage REPORT/manifest/ledger/真实terminal/stdout-stderr/独审/RESTORE入口和被引用保护索引；validation/README.md、current_progress.json、iterative/current_result.md、d4a_final_validation_handoff.md；当前V9 build/wholeINPUT来源及真实终态、cold UNREADY source/inverse/独审；旧V7/V8失败/native RSS/旧nu-fission FAIL真实资料。结果摘要不替代仍依赖的科学INPUT、源码、原始日志或唯一恢复材料。

没有扫描.git历史/敏感内容、没有cold绑定或任何producer/solver/control调用。本轮受限metadata+静态源码引用足以决定HOLD，未重hash35GB，未新增多MBbaseline或通用框架。allocated是当前文件分配统计，不等同APFS即时独占空闲。
'''
(O/'REPORT.txt').write_text(text)
print(json.dumps({'report':pin(O/'REPORT.txt'),'evidence':pin(O/'retention_evidence.json'),'safe_delete_count':0,'safe_reclaim_bytes':0},ensure_ascii=False))
