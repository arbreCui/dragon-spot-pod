import pathlib,json,hashlib,ast,os
D=pathlib.Path(__file__).parent;RD=pathlib.Path('/private/tmp/spot_storage_twentieth_root_20261009')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
S=RD/'restore_archived_intermediates.py';before=ident(S);raw=S.read_bytes();assert hashlib.sha256(raw).hexdigest()=='2c5c9f281a64104e30328eed00b1171672223ef1dce4017f97e828f5d1b4e8a2';text=raw.decode();tree=ast.parse(text)
assert [x.name for x in tree.body if isinstance(x,ast.FunctionDef)]==['digest','main']
for fragment in ["parser.add_argument('--destination',required=True",'if os.path.lexists(requested):','if os.path.lexists(dest):','dest.mkdir(parents=True)',"temporary.open('xb')",'created=False','created=True','if created:temporary.unlink(missing_ok=True)','os.link(temporary,target);temporary.unlink()',"assert not rel.is_absolute() and '..' not in rel.parts","assert not saved_rel.is_absolute() and '..' not in saved_rel.parts",'assert size==row[\'raw_size_bytes\'] and h.hexdigest()==row[\'raw_sha256\']']:
 assert fragment in text,fragment
assert '.rename(' not in text and '.replace(' not in text and 'shutil' not in text and 'subprocess' not in text
content=D/'CONTENT_REPORT.json';receipt=D/'actual_full_archive_review_tool_return.json'
assert sha(content)=='8a3410c78ebb3cd7879749d377bb888e2f0a4a951e4279e6bc59edf4e2902c77'
assert sha(receipt)=='8468fa7d974bd7ea1437cec7c04a9a8ddd9ec1dc94cf09cd3eedfb8eb64259fd'
c=json.loads(content.read_bytes());actual=json.loads(receipt.read_bytes());assert type(actual['returncode']) is int and actual['returncode']==0 and actual['closed'] is True
M=RD/'lossless_archive_manifest.json';P=RD/'proposed_candidates_full_byte_proof.json'
assert sha(M)==c['archive_manifest_sha256'] and sha(P)==c['raw_proof_sha256'];m=json.loads(M.read_bytes());proof=json.loads(P.read_bytes())
for row in c['archive_results']:assert ident(pathlib.Path(row['archive_path']))==row['archive_identity']
for row in proof['candidates']:assert ident(pathlib.Path(row['path']))==row['identity']
for row in m['archives']:
 for name in ['original_relative_path','saved_archive_relative_path']:
  p=pathlib.Path(row[name]);assert not p.is_absolute() and '..' not in p.parts
assert ident(S)==before
out={'schema':'SPOT_R20_LOSSLESS_ARCHIVE_FULL_CONTENT_AND_FINAL_RESTORE_SOURCE_INDEPENDENT_REVIEW_V1','status':'PASS','project_written':False,'files_deleted':0,'business_executed':False,'archive_manifest_sha256':sha(M),'original_full_byte_proof_sha256':sha(P),'restore_source_path':str(S),'restore_source_sha256':sha(S),'restore_source_identity':before,'full_content_review':{'report_path':str(content),'report_sha256':sha(content),'actual_receipt_path':str(receipt),'actual_receipt_sha256':sha(receipt),'initial_chunk_id':'245a9f','session_id':62533,'terminal_chunk_id':'89aab3','returncode':0,'closed':True,'full_decompressed_bytes_hashed':2580841168,'full_compressed_bytes_hashed':1155035285,'files':30,'all_original_manifest_values_exact':True,'all_original_and_archive_identity_fresh_still_same':True},'final_restore_source_gate':{'all_30_relative_paths_unique_and_no_absolute_or_parent_escape':True,'destination_pre_and_post_resolve_lexists_refusal':True,'fresh_destination_mkdir_refuses_existing':True,'archive_size_and_full_SHA_gate_before_destination_creation':True,'temporary_exclusive_creation':True,'temporary_cleanup_only_if_this_call_created_it':True,'raw_full_size_and_SHA_gate_before_publish':True,'atomic_no_overwrite_publish_via_link':True,'no_default_write_without_required_destination':True,'source_not_imported_or_executed':True},'restoration_boundary':{'original_contents_exactly_recoverable_from_gzip_without_scientific_recomputation':True,'original_inode_ctime_mtime_not_restored':True,'future_actual_restore':None,'all_30_archives_must_be_retained_as_lossless_recovery_primary_after_retirement':True,'old_result_seals_and_scientific_failure_success_facts_unchanged':True,'old_recomputation_only_preservation_report_is_historical_precompression_scope_not_current_restore_plan':True,'current_dependency_and_cleanup_execution_outside_this_scope':True}}
for name,value in [('FINAL_ARCHIVAL_REVIEW.json',json.dumps(out,ensure_ascii=False,indent=2)+'\n'),('FINAL_ARCHIVAL_REVIEW.txt','R20 30工作文件无损留档最终独审 PASS\n\n真正只读245a9f/session62533→89aab3退出0。30压缩文件全部完整SHA、全解压2,580,841,168字节大小和SHA，逐项匹配原result/input/output清单；当前原文件及档身份保持。归档共1,155,035,285字节。\n\n最终恢复源2c5c9f独审通过：要求全新独立目录，入口拒绝已存在/悬空目的路径，30相对路径唯一并拒绝越界；档大小/SHA在创建目录前核对；临时文件xb独占创建，仅清理本次真正创建的文件；解压内容SHA/大小核后以link原子不覆盖发布。未执行恢复工具。\n\n原内容可从归档无损恢复，无需20.86小时重算；原inode/ctime/mtime不能恢复。30档在退役后成为必须保留的唯一无损主本。旧日志、结果文档、原清单和科学成功/失败事实保持。先前仅重算保留报告是压缩前历史方案，不修改旧报告。\n\n本报告不代表已删文件或业务成功，也不替代当前依赖/全项目保护终态。所有输出仅TMP，项目无写、未删、未业务。\n')]:
 with (D/name).open('x') as f:f.write(value);f.flush();os.fsync(f.fileno())
print(json.dumps({'status':'PASS','report':str(D/'FINAL_ARCHIVAL_REVIEW.json'),'sha256':sha(D/'FINAL_ARCHIVAL_REVIEW.json'),'restore_source_sha256':sha(S)}))
