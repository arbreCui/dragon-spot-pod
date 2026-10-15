"""Read-only incremental recovery/archive review. No restore or business run."""
from pathlib import Path
import collections,hashlib,json,os,stat,time
H=Path(__file__).resolve().parent;V=Path('/Users/wen/spot/validation');R16=V/'storage_review_sixteenth_20261009';R9=V/'storage_cleanup_ninth_20261009';R14=V/'storage_cleanup_fourteenth_20261009'
PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,wanted=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]);b=p.read_bytes();assert identity(p)==before;sha=hashlib.sha256(b).hexdigest()
 if wanted:assert sha==wanted,(str(p),'SHA changed')
 PINS[str(p)]=dict(path=str(p),sha256=sha,bytes=len(b),identity=before);return b
def obj(p,wanted=None):return json.loads(raw(p,wanted))
def metadata(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode);return dict(path=str(p),identity=identity(p),logical_bytes=s.st_size,allocated_bytes=s.st_blocks*512)
def main():
 start=time.monotonic();rootbefore=obj('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json');baseline=obj(R16/'recovery_git_and_project/REPORT.json');close=obj(R16/'Root_actual_preservation_closeout.json');raw(R16/'REPORT.txt',close['main_report']['sha256']);obj(R16/'after.json',close['after_sha256']);obj(R16/'before.json',close['before_sha256'])
 assert close['metadata_fingerprints_equal']is True and close['files_deleted']==0 and close['storage_reclaimed_bytes']==0
 for row in baseline['R15_small_control_full_SHA_preserved']+baseline['retained_result_and_failure_record_small_pins']:raw(row['path'],row['sha256'])
 m9=obj(R9/'manifest.json','e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8');m14=obj(R14/'audit_metadata_manifest.json','90f6851e4fb4d40f795467ae06bb8669d8311d282b8c49253a9a1d805e582035')
 materials=[row for row in m9['candidates']if row['category']=='GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE'];assert len(materials)==89
 archives={row['compressed_backup']['path']:dict(sha256=row['compressed_backup']['sha256'],size=row['compressed_backup']['size'],restores=[row['path']],raw_sha256=row['sha256'],kind='material')for row in materials}
 for row in m14['records']:
  p=row['archive_path']
  if p not in archives:archives[p]=dict(sha256=row['archive_sha256'],size=row['archive_size'],restores=[],raw_sha256=row['sha256'],kind='audit_metadata')
  assert archives[p]['sha256']==row['archive_sha256']and archives[p]['raw_sha256']==row['sha256'];archives[p]['restores'].append(row['path'])
 assert len(m14['records'])==10 and len(archives)==97
 old={row['path']:row for row in baseline['gzip_exact_metadata_paths']};assert set(old)==set(archives)
 current=[];changed=[]
 for path,row in archives.items():
  meta=metadata(path);assert meta['identity']==old[path]['identity'],(path,'R16 archive immutable identity changed')
  assert meta['logical_bytes']==row['size']and meta['identity'][-1]==1
  current.append(dict(meta,expected_full_sha256=row['sha256'],original_payload_sha256=row['raw_sha256'],restores=row['restores'],kind=row['kind'],full_archive_bytes_credit='Inherited prior strict complete gzip/full SHA proof through unchanged R16 seven-field identity; not rehashed/decompressed here'))
 groups=collections.defaultdict(list);rawgroups=collections.defaultdict(list)
 for path,row in archives.items():groups[(row['size'],row['sha256'])].append(path);rawgroups[row['raw_sha256']].append(path)
 duplicates=[{'expected_size':key[0],'expected_sha256':key[1],'paths':paths}for key,paths in groups.items()if len(paths)>1]
 rawduplicates=[{'raw_sha256':key,'archive_paths':paths}for key,paths in rawgroups.items()if len(paths)>1]
 cleanup_files=[];gzip_paths=[];summary={}
 for path in baseline['recovery_directories']:
  folder=Path(path);rows=[]
  for base,ds,fs in os.walk(folder,followlinks=False):
   for name in ds:assert stat.S_ISDIR((Path(base)/name).lstat().st_mode)
   for name in fs:
    p=Path(base)/name;row=metadata(p);rows.append(row);cleanup_files.append(row)
    if p.suffix=='.gz':gzip_paths.append(str(p))
  unique={(x['identity'][0],x['identity'][1]):x for x in rows};summary[path]=dict(regular_paths=len(rows),unique_inodes=len(unique),logical_bytes=sum(x['logical_bytes']for x in rows),allocated_bytes=sum(x['allocated_bytes']for x in unique.values()))
 assert set(gzip_paths)==set(archives)and len(cleanup_files)==873
 for path,oldsummary in baseline['recovery_directories'].items():assert summary[path]['regular_paths']==oldsummary['regular_paths']and summary[path]['logical_bytes']==oldsummary['logical_bytes']
 restored=[];absent=[]
 for row in m14['records']:
  if os.path.lexists(row['path']):
   assert row['path']==str(V/'storage_cleanup_20261008/preservation_baseline.json');raw(row['path'],row['sha256']);restored.append(row['path'])
  else:absent.append(row['path'])
 assert len(restored)==1 and len(absent)==9 and all(not os.path.lexists(row['path'])for row in materials)
 source9=raw(R9/'restore_archived_material_intermediates.py').decode();source14=raw(R14/'manage_audit_metadata.py',m14['management_source_sha256']).decode();raw(R9/'restore_retired_work_copies.py');raw(R14/'RESTORE.txt');raw(R9/'REPORT.txt')
 assert 'compressed_backup'in source9 and 'archive_path'in source14
 runtime=baseline['V9_runtime_unique_restore_master_current_metadata'];assert identity(runtime['path'])==runtime['identity']
 for row in baseline['large_old_audit_json_HOLD']:assert os.path.lexists(row['path'])
 current_binding=V/'artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009/own_rss_binding.json';binding_metadata=metadata(current_binding);assert binding_metadata['logical_bytes']==60598579
 rscience=V/'axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009';obj(rscience/'Root_actual_V9_cold_binding_tool_return.json','c24ff19a49b77d904057faeb694faaeeaaa181c621850f62353f7a43c839ad98')
 assert all(identity(row['path'])==row['identity']for row in PINS.values())and all(identity(row['path'])==row['identity']for row in current)
 unique={(row['identity'][0],row['identity'][1]):row for row in cleanup_files};permanent_unique={(row['identity'][0],row['identity'][1]):row for row in current}
 report={'schema':'SPOT_SEVENTEENTH_RECOVERY_ARCHIVE_AND_OLD_REPORT_INCREMENTAL_READONLY_REVIEW_V1','status':'NO_NEW_SAFE_DELETE_CANDIDATES','approved_delete_paths':[],'approved_reclaim_bytes':0,'files_deleted':0,'decompression_or_restore_executed':False,'scientific_business_executed':False,'project_formal_ART_or_git_written':False,'Root_R17_current_baseline_counts':rootbefore['counts'],'Root_R17_project_du_KiB':rootbefore['project_du_KiB'],'Root_R16_preservation_full_metadata_credit':dict(status=close['status'],counts=close['counts'],metadata_identity_sha256=close['metadata_identity_sha256']),'no_false_R16_to_R17_whole_project_unchanged_claim':'Scientific phase completed and durable evidence/progress legitimately added after R16; only current fixed R17 window compares project preservation.','recovery_directories_current':summary,'cleanup_summary':dict(regular_paths=len(cleanup_files),unique_inodes=len(unique),logical_bytes=sum(row['logical_bytes']for row in cleanup_files),allocated_bytes=sum(row['allocated_bytes']for row in unique.values())),'all97_permanent_archives_current':current,'all97_archive_immutable_identities_same_R16':True,'all97_expected_archive_unique_content_groups':len(groups),'archive_exact_duplicate_groups_from_pinned_original_full_SHA':duplicates,'payload_SHA_multiple_archive_groups':rawduplicates,'archive_source_content_credit':'Original R9 strict complete single-member gzip/CRC/EOF/rawSHA proof and R14 full decode proof are retained; archives not re-read2.39GiB or decompressed this round. Current97 seven-field identities exactR16 and fixed original manifest control SHA stable.','permanent_archive_summary':dict(paths=97,unique_inodes=len(permanent_unique),logical_bytes=sum(row['logical_bytes']for row in current),allocated_bytes=sum(row['allocated_bytes']for row in permanent_unique.values())),'R9_material_raw89_remain_absent':True,'R14_retired_audit_JSON9_remain_absent':absent,'R14_protected_R1_baseline_present_full_SHA':restored,'retention_reasons':[dict(paths=[str(R9/'packed_material_intermediates')],purpose='89 lossless material raw recovery primaries',reason='These recover89 retiredraws then permit prior120 work-copy restorations; original failed batches, receipts and all final result documents remain. Gzip is not cache; no replacement archive/alternate current restore mapping established.',deletable=False),dict(paths=[str(R14/'metadata_archives')],purpose='8 content-addressed metadata recovery archives for10 original paths',reason='Two same-content historical metadata pairs were already pooled into8 archives. Nine original paths absent; one protectedR1 baseline restored. Fixed original manifest and restore reader still require these exactarchives. Existing restoredR1 raw is not authorization to break the permanent archive contract.',deletable=False),dict(paths=[row['path']for row in baseline['large_old_audit_json_HOLD']],purpose='large old audit metadata, protected index and result fullSHA baselines',reason='Explicit historical reader/recovery inputs with no new retirement or replacement proof; keep original exactpath documents/control manifests and source.',deletable=False),dict(paths=[str(R9/'REPORT.txt'),str(R14/'REPORT.txt'),str(R16/'REPORT.txt')],purpose='result summaries, failure facts, ledgers, restore source and cross-review bundles',reason='All original documents and failed stdout/stderr/receipts remain; derivative summaries cannot replace complete failure observations or old sealed reader inputs. No new large redundant unreferenced evidence found.',deletable=False),dict(paths=[str(current_binding)],purpose='current completedactualbinding and all SOURCE/PREP/terminal/proof files',reason='Current independent binding review complete but Root joint admission not yet declared in this storage task; active next-stage dependency, not obsolete artifact.',deletable=False)],'new_current_binding_metadata_only_preserved':binding_metadata,'V9_unique_runtime_restore_master_identity_still_same':True,'small_control_and_result_document_fullSHA_pins':list(PINS.values()),'readonly_elapsed_seconds':time.monotonic()-start,'write_scope':str(H),'limits':['No whole35GB scientific content reread; no2.39GiB archive reread/decompression; no Git maintenance.','Metadata identity stability inherits previously verified immutable byte evidence, not a new full-content verification.','Allocatedbytes are current filesystem observations, not APFS exclusive free-space claims.']}
 report['approved_deletion_candidates']=[];report['project_written']=False
 with(H/'REPORT.json').open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
 text='SPOT 第十七轮恢复档案与旧审计资料只读复查\n\n新增可安全删除项0，批准回收量0；未删除、未恢复、未解压到项目、未运行科学业务。\n\n97份永久恢复gzip全部仍为普通单链接文件，七字段身份与第十六轮完全一致。它们的原始完整SHA/无损验证按不变身份继承，本轮没有重复读取约2.39GiB压缩档。原清单显示'+str(len(groups))+'个不同的压缩内容组；8份审计清单档已将10份原清单中的相同内容合并，未发现可直接丢弃而仍保持原恢复工具完整的新冗余。\n\n89份材料档是已退役raw及早先120份工作副本的恢复主本，全部原raw仍缺席；8份元数据档继续恢复9个缺席清单和已还原的保护R1路径。现存R1原JSON虽与其归档同内容，固定恢复清单仍保留这份档，不能当缓存删除。所有原报告、失败日志、收据、清单、账本、恢复工具和受旧reader引用的大清单保留；旧失败事实不改。\n\n14个旧清理目录仍有873份普通文件，逻辑大小与R16各目录一致。SOURCE/PREP/绑定及其真实终态是当前下一阶段依赖，完整保留。R16之后科学阶段新增资料和进度更新属于已记录正常变更，本轮不拿旧全项目指纹错误宣称没有变化；Root当前R17窗口单独核验项目保留。\n\n证据详见REPORT.json：97条准确路径与原SHA/恢复映射、当前身份/大小，以及小恢复控制和结果文档的鲜读SHA。文件分配量不代表APFS即时独占释放。\n'
 (H/'REPORT.txt').write_text(text)
 print(json.dumps({'status':report['status'],'approved_paths':0,'approved_reclaim_bytes':0,'97_archive_identity_stable':True,'expected_archive_unique_SHA_groups':len(groups),'old_cleanup_files':873,'permanent_gzip_allocated_bytes':report['permanent_archive_summary']['allocated_bytes'],'small_fullSHA_pins':len(PINS),'report_path':str(H/'REPORT.json'),'report_sha256':hashlib.sha256((H/'REPORT.json').read_bytes()).hexdigest(),'text_sha256':hashlib.sha256((H/'REPORT.txt').read_bytes()).hexdigest(),'no_business_or_project_writes':True}))
if __name__=='__main__':main()
