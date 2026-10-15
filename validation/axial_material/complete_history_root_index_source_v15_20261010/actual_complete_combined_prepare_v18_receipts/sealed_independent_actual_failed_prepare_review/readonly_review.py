from pathlib import Path
import ast,hashlib,json,os,stat,tempfile
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_combined_prepare_v18_receipts'
ART=Path('/Users/wen/spot/validation/artifacts')
H=ART/'axial-material-complete-combined-prepare-host-v18-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v18-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v18-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v18-20261010'
D=B/'actual_complete_combined_prepare_v18_sources'
C=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v18.py')
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,read_metadata=False):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode),str(p);h=hashlib.sha256()
 parts=[] if read_metadata else None
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):
   h.update(b)
   if parts is not None:parts.append(b)
 z=p.lstat();assert ident(a)==ident(z),(str(p),'identity changed during whole EOF SHA')
 r=dict(path=str(p),sha256=h.hexdigest(),identity=ident(a),size_bytes=a.st_size)
 return (r,b''.join(parts)) if parts is not None else r
def load(p):
 r,b=pin(p,True);return r,json.loads(b)
mp,m=load(E/'Root_actual_failed_prepare_namespace_manifest.json')
sp,s=load(E/'Root_actual_failed_complete_combined_prepare_summary.json')
tp,tr=load(E/'Root_actual_prepare_tool_terminal_return.json')
fixed={mp['path']:'5a85f64360451fd8d283ecfc53ac8e749cf7f538396af323183dba321ffec0c0',sp['path']:'31531d0d3fc902a94fa8da1417c40832b42eff107dbddf7c6c83876902d819ad',tp['path']:'373f757086a2150b1808a6f7d427bf63d91a6a6bbb90dd5113b960753fb6e13a'}
for r in (mp,sp,tp):assert r['sha256']==fixed[r['path']]
def compare(actual,record):
 assert actual['path']==record['path']
 assert actual['sha256']==record['sha256'],actual['path']
 assert actual['identity']==record['identity'],actual['path']
 if 'size_bytes' in record:assert actual['size_bytes']==record['size_bytes']
def snapshot(root):
 root=Path(root);a=root.lstat();assert stat.S_ISDIR(a.st_mode)
 files={};dirs={};links={}
 def visit(p):
  for x in sorted(p.iterdir()):
   r=str(x.relative_to(root));ss=x.lstat()
   if stat.S_ISLNK(ss.st_mode):links[r]=dict(path=str(x),target=os.readlink(x),identity=ident(ss))
   elif stat.S_ISDIR(ss.st_mode):dirs[r]=dict(path=r,identity=ident(ss));visit(x)
   elif stat.S_ISREG(ss.st_mode):files[r]=pin(x)
   else:raise ValueError('unsupported namespace type '+str(x))
 visit(root)
 z=root.lstat();assert ident(a)==ident(z)
 return dict(root=str(root),root_identity=ident(a),files=files,directories=dirs,symlinks=links,bytes=sum(x['size_bytes'] for x in files.values()))
assert [Path(x['root']) for x in m['namespaces']]==[H,S,O,T,D]
before={}
counts=[]
for n in m['namespaces']:
 root=Path(n['root']);assert n['absent'] is False
 a=snapshot(root);before[str(root)]=a
 assert set(a['files'])==set(n['files'])
 for k,r in n['files'].items():compare(a['files'][k],r)
 assert a['directories']=={x['path']:x for x in n['directories']}
 assert a['symlinks']==n['symlinks']
 counts.append(dict(root=str(root),regular_files=len(a['files']),directories=len(a['directories']),symlinks=len(a['symlinks']),bytes=a['bytes']))
eb=snapshot(E);before[str(E)]=eb
cp=pin(C);compare(cp,m['canonical_factory'])
assert cp['sha256']=='5c4b48399b2a04383fc0b736127925bfb0ed9dca7cf63f0c62bedc35a4b07240'
hostp=before[str(D)]['files']['combined_prepare_host.py']
assert hostp['sha256']=='bc5c6fa1118b84641a5a66232080354074b49ad2c59ac809e28ee99cc6faac98'
assert len(before[str(D)]['files'])==len(m['all_frozen_input_receipts'])==35
for k,r in m['all_frozen_input_receipts'].items():compare(before[str(D)]['files'][k],r)
_,pre=load(E/'Root_prelaunch_complete_source_freeze.json')
assert len(pre['all_source_files'])==35
assert set(pre['all_source_files'])==set(before[str(D)]['files'])
for k,r in pre['all_source_files'].items():compare(before[str(D)]['files'][k],r)
compare(cp,pre['canonical_factory']);compare(hostp,pre['host'])
caps=dict(whole_wall_seconds=1800,stage_wall_seconds=600,rss_mib=512,archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
for k,v in caps.items():assert pre[k]==v
assert pre['all_business_namespaces_absent'] is True and pre['business_executed'] is False
_,pr=load(E/'Root_final_prelaunch_source_and_reserve_check.json')
for k in ('all35_frozen_source_files_full_SHA7ID_unchanged','canonical_factory_and_host_full_SHA7ID_unchanged','all_fresh_business_namespaces_absent','original_2GiB_reserve_passed','business_not_yet_executed'):assert pr[k] is True
assert type(tr['terminal_tool_return']['exit_code']) is int and tr['terminal_tool_return']['exit_code']==1
assert 'session_id' not in tr['terminal_tool_return']
assert tr['terminal_tool_return']['chunk_id']=='d1800c'
assert type(tr['exit_code']) is int and tr['exit_code']==1
assert tr['closed'] is True and tr['session_repolled_after_close'] is False
assert tr['initial_tool_return']['chunk_id']=='026dfe' and tr['original_session_id']==tr['initial_tool_return']['session_id']==47917
for k in ('new_five_stage_build_executed','whole_combined_INPUT_executed','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted'):assert tr[k] is False
wp,w=load(H/'run/prepare.watchdog.json');compare(wp,s['actual_watchdog'])
assert s['watchdog']==w
expected_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(C),'prepare-build']
assert w['command']==expected_command
assert type(w['returncode']) is int and w['returncode']==-15
assert w['rss_cap_mib']==512 and w['sampled_peak_rss_mib']==514.421875 and w['sampled_peak_rss_mib']>512
assert 0<w['wall_cap_seconds']<=600 and 0<w['elapsed_seconds']<w['wall_cap_seconds']
assert w['elapsed_seconds']==160.69891799998004
assert w['own_child_only'] is True and w['liveness_group_cleanup'] is True
assert w['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')"
fp,f=load(H/'failed_host_result.json');compare(fp,s['failed_host_result'])
assert f['status']=='FAILED_COMPLETE_COMBINED_PREPARE_NO_RETRY'
assert f['error']==w['limit_failure']
_,st=load(H/'COMBINED_PREPARATION/stages.json')
assert st=={'stages':f['stage_records']}
assert len(f['stage_records'])==1
r=f['stage_records'][0]
assert r['label']=='run/prepare' and r['command']==expected_command and r['wall_cap_seconds']==600 and r['status']=='FAILED'
assert all(f[k] is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted'))
assert set(before[str(T)]['files'])=={'failed_prepare_terminal_return.json'}
ft,fv=load(T/'failed_prepare_terminal_return.json');compare(ft,s['failed_canonical_terminal'])
assert fv['actual_tool_result']==tr['terminal_tool_return']
assert fv['actual_closed'] is True and type(fv['actual_returncode']) is int and fv['actual_returncode']==1 and fv['retries']==0
assert fv['watchdog']==w
for k in ('successful_declaration_input_observed','successful_new_runtime_build_observed','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted'):assert fv[k] is False
for r,k in ((tp,'Root_actual_terminal'),(mp,'namespace_manifest')):compare(r,s[k])
assert s['status']=='ACTUAL_PREP_EXIT1_CLOSED_ORIGINAL_512_MIB_EXCEEDED_NO_RETRY'
assert s['original_caps_preserved'] is True and s['all35_original_source_inputs_full_EOF_SHA7ID_unchanged'] is True
assert s['original_host_final_inputs_revalidation_reached'] is False and s['Root_post_failure_input_revalidation_performed'] is True
for k in ('successful_declaration_observed','complete_input_graph_observed','new_five_stage_build_executed','whole_combined_INPUT_admitted','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted','goal_complete','cleanup_performed'):assert s[k] is False
assert m['rss_failure_source_line_observed'] is False
absence=[O/'input_graph.json',O/'declaration.json',O/'seal.json',O/'driver_result.json',H/'result.json',T/'declaration_terminal_return.json',T/'terminal_return.json']
assert all(not os.path.lexists(p) for p in absence)
assert len(before[str(H)]['files'])==5 and len(before[str(S)]['files'])==11 and len(before[str(O)]['files'])==1
hr,hbytes=pin(D/'combined_prepare_host.py',True)
hs=hbytes.decode();ast.parse(hs)
cr,cbytes=pin(C,True);ast.parse(cbytes.decode());compare(cr,cp)
for fragment in ("WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30","helper.guard_admission(full)","full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)","resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)","runner.execute(HOST/'run','prepare',command,STAGE_CAP)","type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources","if any(os.path.lexists(p) for p in (HOST,SOURCE,OUT,TERMINAL))","threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False"):
 assert fragment in hs,fragment
assert hs.count('support.archive_bytes((HOST,SOURCE,OUT,SOURCE_ARCHIVE))')==2
assert "if support.pin(entry['path'],entry['sha256'])!=entry" in hs
tree_bytes=sum(x['bytes'] for x in counts)
current_joint=tree_bytes+eb['bytes']+cp['size_bytes']
added_summary_report=eb['files']['Root_actual_failed_complete_combined_prepare_summary.json']['size_bytes']+eb['files']['REPORT.txt']['size_bytes']
assert tree_bytes==42851094
assert current_joint==43219485 and added_summary_report==4273
assert s['joint_archive_bytes']==43215212==current_joint-added_summary_report
assert s['joint_archive_cap_bytes']==2*2**30 and current_joint<2*2**30
for root,a in before.items():assert snapshot(Path(root))==a,(root,'whole namespace changed before/after')
assert pin(C)==cp
for p,h in fixed.items():assert pin(p)['sha256']==h
d=Path(tempfile.mkdtemp(prefix='axmat_v18_failed_actual_prepare_finite_evidence_review_20261010_',dir='/private/tmp'))
review=dict(schema='AXMAT_V18_FAILED_ACTUAL_PREPARE_FINITE_READONLY_REVIEW_V1',status='PASS_EVIDENCE_REVIEW_ACTUAL_PREP_FAILED',Root_actual_tool_return=tr,Root_actual_terminal_receipt=tp,Root_summary=sp,Root_manifest=mp,actual_exit_code_integer=1,actual_Root_session_closed=True,original_session_id=47917,session_repolled_by_reviewer=False,watchdog=w,failed_stage_record_count=1,failed_prepare_only=True,all_namespace_files_dirs_symlinks_full_EOF_SHA_identity7_before_after_equal=True,namespaces=counts,complete_namespace_snapshot=before,canonical_factory=cp,host_fixed_sha=hostp['sha256'],all35_frozen_SOURCE_and_canonical_host_full_SHA7ID_match_prelaunch_and_Root_manifest=True,original_caps_source_preserved=caps,source_archive_joint_count_scope_preserved=True,archive=dict(five_frozen_namespace_bytes=tree_bytes,Root_summary_joint_bytes_before_summary_and_REPORT=s['joint_archive_bytes'],fresh_current_joint_bytes_including_E_all_files_and_canonical=current_joint,new_summary_REPORT_bytes=added_summary_report,cap_bytes=2*2**30,under_original_cap=True),absence_checked=[str(p) for p in absence],TERMINAL_is_failed_record_only=True,original_host_final_input_revalidation_reached=False,all_physical_inputs_final_pass_not_claimed=True,post_failure_revalidation_scope='35 frozen source files plus canonical factory and host; no broad historical physical input revalidation',rss_failure_exact_business_line_observed=False,failure_cause_attribution_beyond_observed_RSS_cap=False,retries=0,new_successful_PREP_or_whole_INPUT_or_build_or_native_or_AAA_or_ABA_credit=False,no_business_or_project_module_API_execution=True,no_numeric_payload_interpretation=True,numeric_or_project_payload_only_hashed_for_namespace_integrity=True,no_canonical_or_ART_or_frozen_namespace_writes=True,no_blocker=True)
p=d/'REVIEW.json';p.write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
(d/'REPORT.txt').write_text('V18 准备失败封存的一遍有限只读复核通过。\n真实 Root 026dfe/session 47917 → d1800c，严格整数退出码 1，已关闭，无重试或关闭后轮询。\n实际 watchdog：子进程 -15，160.698918 秒，峰值 514.421875 MiB 超过原 512 MiB，own-child 与进程组清理 true。只能确认 RSS 上限触发；具体业务源码行未观察。\nH/S/O/T/D 全部 53 个普通文件、13 个子目录、0 个链接，连同 E 及 canonical 全 SHA/7ID 前后保持，35 冻结 SOURCE 与 canonical/host 匹配原 prelaunch。\n原 1800/600 秒、512 MiB、2 GiB、history 96/free 8 GiB、1 thread/1 child/0 retry 仍保持。\n五个封存 namespace 合计 42,851,094 B；Root summary 写入前联计 43,215,212 B；包含新增 summary/REPORT 的当前 H/S/O/T/D/E+canonical 联计 43,219,485 B，均低于 2 GiB。\n没有成功 declaration/input_graph/seal/driver_result，T 仅 failed_prepare_terminal_return，不能当作成功凭证。\n原 host 最终输入复核未到达。这里只复核 35 冻结 source + canonical/host 和此次封存，不能声称全部物理输入 final pass。\n没有新的 PREP、whole INPUT、完整构建、native、AAA 或 ABA 成功信用。本审查不运行 API/业务/数值，不导入 driver，不改项目/ART，仅标准库源码/元数据及完整字节哈希。\n',encoding='utf-8')
print(json.dumps(dict(directory=str(d),review_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status=review['status'],namespace_file_count=sum(x['regular_files'] for x in counts),current_joint_bytes=current_joint,no_blocker=True,business_executed=False)))
