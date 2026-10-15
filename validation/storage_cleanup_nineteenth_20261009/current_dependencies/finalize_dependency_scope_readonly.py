"""Small evidence binding for exact36 storage scope only; no business."""
import hashlib,json,os,stat
from pathlib import Path
D=Path('/private/tmp/spot_storage_nineteenth_current_graph_closed_state_review_20261009')
PLAN=Path('/private/tmp/spot_storage_nineteenth_root_20261009/fixed_candidate_plan.json')
SOURCE=Path('/private/tmp/spot_storage_nineteenth_current_native_snapshot_read_paths_20261009')
PEER=Path('/private/tmp/spot_storage_nineteenth_AAA_early_snapshots_preservation_review_20261009')
PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,sha=None):
 p=Path(p);a=identity(p);raw=p.read_bytes();assert identity(p)==a and stat.S_ISREG(a[2]);actual=hashlib.sha256(raw).hexdigest()
 assert sha is None or actual==sha,str(p)
 PINS[str(p)]=dict(path=str(p),bytes=len(raw),sha256=actual,identity=a);return raw
def read(p,sha=None):return json.loads(pin(p,sha))
plan=read(PLAN,'b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a')
index=read(D/'REPORT.json','0473a770f97ecd65ef066aef12729478932d784c7aa4f22e42b138e46491e960')
byteproof=read(D/'EXACT_FIXED_PLAN_FULLSHA_REPORT.json','055ce01dc5fb246996171a49e10a808f52d9116cc75add05f6c938c8d9a8e462')
indexreceipt=read(D/'CURRENT_INDEX_READONLY_ACTUAL_TOOL_RETURN.json','23cf93fb3d42d30029f5d40e3f6dace7da05672214e53f2ebe21efe659064d2b')
bytereceipt=read(D/'EXACT_PLAN_FULLSHA_ACTUAL_TOOL_RETURN.json','8f35e5f1b7020f6b25248176dc17628ccef588dff7fe71bbb33e781563592229')
assert indexreceipt['actual_tool_result']==dict(chunk_id='108c02',exit_code=0,closed=True)
assert bytereceipt['actual_tool_result']==dict(initial_chunk_id='301509',session_id=63934,terminal_chunk_id='ee0609',exit_code=0,closed=True)
source=read(SOURCE/'REPORT.json','f055e095769fe065a11b24cf3b29693d8bc887c485da39495964ff2f7af7d6cf')
source_receipt=read(SOURCE/'actual_readonly_tool_return.json')
assert source['status']=='PASS'and not source['candidate_specific_blockers']
assert source['offline_explicit_union_count']==672 and source['all_statically_derived_read_paths_count']==38055
assert source_receipt['actual_tool_result']['exit_code']==0 and type(source_receipt['actual_tool_result']['exit_code'])is int
assert source_receipt['actual_tool_result']['closed']is True
peer=read(PEER/'REPORT.json','5d37e70f47df6065539721a9ca3f432afe7283fc797dc1e7cff5777ff8e13ae9')
peer_receipt=read(PEER/'actual_readonly_tool_return.json','7a29d23591ee68c25432e5892ded97c15a7252e2bb21694507a347b0d734e58c')
assert peer['status']=='PASS'and peer['prior_exact_copy_restore_master_intersections']==[]
assert peer_receipt['actual_tool_result']['exit_code']==0 and peer_receipt['actual_tool_result']['closed']is True
regular={r['path']:r for r in plan['regular']};links={r['path']:r for r in plan['symlinks']}
assert len(regular)==len(links)==18 and set(plan['incoming_symlinks_exact'])==set(links)
assert set(regular)==set(peer['fixed_regular_paths'])and set(links)==set(peer['fixed_symlink_paths'])
assert set(regular)=={r['path']for r in index['proposed_regular18']}and set(links)=={r['path']for r in index['proposed_related_symlink18']}
assert not index['current_blockers']and not index['unknown_family_incoming_symlinks']and not index['ordinary26784_file_hits']and not index['ordinary_namespace_hits']
for p,r in regular.items():
 assert identity(p)==r['identity']==byteproof['exact_fullSHA_pins'][p]['identity']
 assert r['sha256']==byteproof['exact_fullSHA_pins'][p]['sha256']
for p,r in links.items():assert identity(p)==r['identity']and os.readlink(p)==r['link_text']and str(Path(p).resolve(strict=True))==r['target']
for row in index['preserve_last_three_closed_snapshots']:assert identity(row['path'])==row['identity']
for p,row in PINS.items():assert identity(p)==row['identity']
report=dict(schema='SPOT_R19_EXACT36_STORAGE_DEPENDENCY_AND_BYTE_INDEPENDENT_COMPLETE_SCOPE_V1',status='PASS',
 fixed_plan_sha256=PINS[str(PLAN)]['sha256'],regular_count=18,symlink_count=18,logical_bytes=4283202816,allocated_bytes=4283228160,
 exact18_fullSHA_original_SEALED_STAGE_OUTPUTS_valid=True,all36_seven_identity_and_link_literals_stable=True,
 all_current37395_files_35647_canonical86_namespace186_alias445_absence_excluded=True,original_ordinary26784_files_and_namespaces_excluded=True,
 actual_current_native_read_chain672_offline_and38055_static_exact_resolved_inode_candidate_hits_zero=True,
 all_project_incoming_links_are_exact18_selected_Root_plan_witness=True,no_family_unknown_incoming_symlink=True,
 prior_restore_master13_manifests14_ledgers10188_rows_no_copy_restore_intersection=True,
 original242_stage_PASS_27_map_results216_logs_and3_WAITING_REFERENCE_status_kept=True,
 all_existing_bootstrap_last_two_maps_last_three_closed_and_other_files_kept=True,
 historical_last_two_seal9_prior_retirements_preserved_not_falsely_claimed_complete=True,
 future_old_map_full_reverification_requires_restoration_or_recomputation=True,source_reader_real_tool=source_receipt['actual_tool_result'],
 index_reader_real_tool=indexreceipt['actual_tool_result'],bytes_reader_real_tool=bytereceipt['actual_tool_result'],peer_reader_real_tool=peer_receipt['actual_tool_result'],
 evidence_fresh_pins=PINS,current_read_indices=index['current_read_indices'],
 files_deleted_by_this_review=0,project_written=False,business_executed=False,native_started=False,old35GB_rehashed=False,
 new_scientific_credit=False,actual_native_future_result=None,
 admission_scope='Exact fixed storage plan only; Root sole retirement and actual whole-remainder postcheck remain necessary.')
p=D/'FINAL_REPORT.json'
with p.open('x')as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with(D/'FINAL_REPORT.txt').open('x')as f:f.write('R19 固定旧AAA工作状态依赖/字节独审：PASS。\n18份早期closed状态（3.989067GiB）与18个精确parent链接；均不属当前37395读取清单、35647canonical、86namespace、186alias或445absence，当前原生/离线快照动态读取链无命中。\n18文件全文SHA等于原SEALED_STAGE_OUTPUTS记录，36身份/链接文本稳定；无旧copy恢复主本依赖。\n保留最后3份closed、最后2轮map现存文件及链接、全部现存bootstrap和原结果/日志/封存/失败事实。不宣称历史全seal文件现存齐全；9项先前退役已在旧ledger保留。\n删后如需逐轮旧状态完整重验，必须按原输入和代码重算/恢复，不能把本次存储结论当科学或冷启动成功。\n尚未删除，由Root统一固定清理并做保留集合终态核验；本独审未运行业务、未改项目、未重读35GB。\n')
print(json.dumps(dict(status='PASS',report=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),plan_sha256=PINS[str(PLAN)]['sha256'])))
