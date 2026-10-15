"""Readonly current gate/PF enumeration and oldv10 exact candidate survey.
No unlink/rename/copy/compiler/CLE or future v13 Source qualification.
"""
import ast,hashlib,importlib.util,json,os,resource,stat,subprocess,time
from pathlib import Path
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011';ART=R/'validation/artifacts';HERE=Path(__file__).resolve().parent
OLD=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v10';TARGET=OLD/'AAA/projected_boot.xsm'
START=time.monotonic();CACHE={};PROTECTED={};ROLES={};CHANGES=[];ORIGINS=[];OBSERVED_TARGET_PF_FIELDS=[];CHECKS=0

def ident(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def guard():
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss>=512*2**20 or time.monotonic()-START>=1800:raise RuntimeError('original SELF512/whole1800 survey cap')
def pin(path):
 global CHECKS
 p=Path(path);before=p.lstat();assert stat.S_ISREG(before.st_mode)and not any(x.is_symlink()for x in(p,*p.parents))
 if str(p)in CACHE:
  assert ident(before)==CACHE[str(p)]['identity'];return CACHE[str(p)]
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();count=0
 with os.fdopen(fd,'rb')as f:
  assert ident(os.fstat(f.fileno()))==ident(before)
  while True:
   raw=f.read(2**20)
   if not raw:break
   h.update(raw);count+=len(raw);guard()
  assert ident(os.fstat(f.fileno()))==ident(before)
 assert ident(p.lstat())==ident(before)and count==before.st_size
 row=dict(path=str(p),sha256=h.hexdigest(),size_bytes=count,identity=ident(before));CACHE[str(p)]=row;CHECKS+=1;return row

def norm(v):
 if not isinstance(v,dict)or not isinstance(v.get('path'),str)or not isinstance(v.get('sha256'),str):return None
 i=v.get('identity',v.get('seven_id'));n=v.get('size_bytes',v.get('bytes'))
 if isinstance(i,list)and len(i)==7 and  all(type(x)is int for x in i):
  return dict(path=v['path'],sha256=v['sha256'],size_bytes=i[4]if n is None else n,identity=i)
 return None

def pins(value,prefix):
 row=norm(value)
 if row is not None:yield row,prefix;return
 if isinstance(value,dict):
  for k,x in value.items():yield from pins(x,prefix+'/'+k)
 elif isinstance(value,list):
  for i,x in enumerate(value):yield from pins(x,prefix+'/'+str(i))

def add(wanted,role):
 wanted=norm(wanted);assert wanted is not None
 actual=pin(wanted['path'])
 if actual!=wanted:
  assert wanted['sha256']==actual['sha256']and wanted['size_bytes']==actual['size_bytes']and wanted['identity'][0]==16777234 and  actual['identity'][0]==16777229 and  wanted['identity'][1:]==actual['identity'][1:]
  event=dict(historical_pin=wanted,current_pin=actual,only_device_changed=True)
  if event not in CHANGES:CHANGES.append(event)
 assert actual['path']not in PROTECTED or PROTECTED[actual['path']]==actual
 PROTECTED[actual['path']]=actual;ROLES.setdefault(role,set()).add(actual['path']);return actual

def read(path,role=None):
 p=pin(path);raw=Path(path).read_bytes();assert len(raw)==p['size_bytes']and hashlib.sha256(raw).hexdigest()==p['sha256']and ident(Path(path).lstat())==p['identity']
 if role:add(p,role);ORIGINS.append(dict(role=role,metadata_pin=p))
 return json.loads(raw)

def rows(value,role):
 for p,_ in pins(value,role):add(p,role)

def gate_manifest(path,role,fields=None):
 d=read(path,role)
 if fields is None:fields=[k for k in d if k not in ['original_caps','original_five_Source_order','required_future_receipt_arguments','required_dynamic_actual75_report_arguments']and(k in ['host_source','dependencies','files','complete_source_file_pins','fixed_source_files','static_input_pins','inputs','source_pin','current_plan_pin','original_math_sources','complete_math_inverse_proof_pins','additional_current_input_pins']or k.startswith(('selected_','required_actual_'))and k.endswith(('_pin','_report')))]
 for field in fields:
  if field in d:rows(d[field],role+'/'+field)
 return d

roots=[REC/x for x in ['aaa_three_plane_streaming_pipeline_source_v12','current_formal_material_authority_exact_cache70_source_v7','current_eleven_saved_gendf_current_mount_host_source_v4','reaction_genDF_current_mount_stream_source_v2','saved_full370_terminal_audit_host_source_v2','full370_unreduced_eigen_reference_source_v2']]
# Exact source-file JSON fullpin enumeration is broader than selected gates.
# It is NOT recursive promotion of historical business raw output arrays.
for root in roots:
 assert root.is_dir()and not root.is_symlink()
 before=sorted(str(p)for p in root.rglob('*')if p.is_file())
 for name in before:
  row=pin(name);add(row,'complete_current_Source_files/'+root.name)
  if Path(name).suffix=='.py':ast.parse(Path(name).read_text())
  if Path(name).suffix=='.json':
   d=read(name)
   for p,field in pins(d,name):
    if p['path']==str(TARGET):OBSERVED_TARGET_PF_FIELDS.append(dict(metadata=name,field=field,pin=p))
 assert before==sorted(str(p)for p in root.rglob('*')if p.is_file())
cat=read(REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json','selected_current_catalog')
assert len(cat['rows'])==3040;rows([x['current_pin']for x in cat['rows']],'all3040_current_catalog_rows')
common=read(REC/'current_mount_full_identity_common_source_v1/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json','selected_current_Common_binding')
assert len(common['fixed_current_pins'])==2012;rows(common['fixed_current_pins'],'all2012_Common_mandatory')
for version,count in [('v11',2643),('v12',2654)]:
 out=ART/('axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-'+version)
 raw=read(out/'Root_actual_complete_execution_record_before_final_publication.json','actual_'+version+'_complete_raw_document')
 assert len(raw['fixed_current_pins'])==count and len(raw['owned_runtime_pins'])==163
 rows(raw['fixed_current_pins'],'actual_'+version+'_full_fixed'+str(count));rows(raw['owned_runtime_pins'],'actual_'+version+'_current_owned163')
 add(pin(out/'AAA/projected_boot.xsm'),'must_keep_current_'+version+'_PROJECT')
 # Current v12 evidence curves are all retained, not candidates.
 if version=='v12':
  for path in sorted(out.rglob('*')):
   if path.is_file():add(pin(path),'all_latest_v12_files_curveproof_preserved')
 latest_raw=raw
for path in sorted((REC/'aaa_three_plane_streaming_pipeline_source_v12').glob('COMPLETE*FREEZE.json')):gate_manifest(path,'v12HF_selected')
sc=REC/'saved_full370_terminal_audit_host_source_v2';d=read(sc/'CURRENT_SAVED_FULL370_GUARD_INPUT_BINDING.json','saved_v2_current_BIND');assert len(d['fixed_current_pins'])==3315 and  len(d['science_original_input_pins'])==1129
rows(d['fixed_current_pins'],'saved_v2_3315');rows(d['science_original_input_pins'],'saved_v2_1129science')
for p in sorted(sc.glob('COMPLETE*FREEZE.json')):gate_manifest(p,'saved_v2_freeze',fields=['fixed_source_files','input_binding_pin','host_pin','selected_actual_science_source_freeze_pin','selected_actual_current_mapping_pin','source_pin','science_manifest_pin','actual_current1129_input_pins'])
mat=REC/'current_formal_material_authority_exact_cache70_source_v7'
for p in sorted(mat.glob('COMPLETE*FREEZE.json')):gate_manifest(p,'material_v7_selected_freeze')
for name in ['CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json','CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json']:
 d=read(mat/name,'material_v7_selected_plan/'+name)
 # These are exact active plan fields, not inverse-package proof observations.
 for field in ['current_case_spec_pin','protected_formal_and_producer_plan_pin','complete_source_copies','original4_math_source_copies','observation_module','current_seed_plan_pin','original_nine_Fortran_Source_freeze_pin','original_actual69_v4_report_pin','current_actual70_build_report_pin','current_actual70_independent_review_pin','current_cache_Source_freeze_pin','current_build70_host_Source_freeze_pin']:
  if field in d:rows(d[field],'material_v7_plan_gate/'+field)
for root in [REC/'current_eleven_saved_gendf_current_mount_host_source_v4',REC/'reaction_genDF_current_mount_stream_source_v2']:
 for p in sorted(root.glob('COMPLETE*FREEZE.json')):gate_manifest(p,'GENDF_current_selected_freeze')
 for p in sorted(root.glob('*PLAN.json')):gate_manifest(p,'GENDF_current_selected_plan')
ref=read(REC/'full370_unreduced_eigen_reference_source_v2/CURRENT_FORMAL_FULL370_INPUT_PLAN_SOURCE_ONLY.json','reference_v2_selected_plan')
for k in ['protected_formal_and_producer_plan_pin','current_case_spec_pin','current_prepared_pin','current_axial_track_pin','additional_current_input_pins']:rows(ref[k],'reference_v2_gate/'+k)
formal=read(ref['protected_formal_and_producer_plan_pin']['path'],'selected_formal_plan_metadata')
rows(formal['formal_inputs'],'reference_all_formal_inputs')
for row in formal['producers']:rows([row[k]for k in ['report','archive','radial_binary_track']],'reference_all3_actual_native_producer_inputs')
# Current actual selection documents; no future v13 namespace exists in this
# authority selection. Future release must re-prove its genuine Source DAG.
for name in ['ROOT_EXACT_ACTUAL_PIPELINE_V12_PARENT_PHASE_ARGV_20261013.json','ACTUAL_PIPELINE_V12_PARENT_PHASE_ROOT_TRUE_TOOL_RETURNS_20261013.json']:
 p=REC/name
 if p.exists():add(pin(p),'selected_v12_Root_current_document')
summary=read(OLD/'Root_actual_three_plane_engineering_summary.json','oldv10_retained_failed_summary');truth=read(REC/'ACTUAL_PIPELINE_V10_TRUE_TOOL_RETURNS_20261013.json','oldv10_Root_true_closed1')
assert truth['observed_closed']is True and truth['original_integer_exit_code']==truth['terminal']['exit_code']==1
assert summary['status']=='FAILED_UNQUALIFIED_NO_RETRY'and summary['engineering_three_plane_closed0']is False and len(summary['records'])==46 and summary['output_pins']==[]
closures=[]
for record in summary['records']:
 lp=pin(OLD/(record['label']+'.log'));wp=pin(OLD/(record['label']+'.watchdog.json'));w=read(wp['path'])
 assert record['status']in ['PASS','FAILED']and type(w['returncode'])is int and w['returncode']==(0 if  record['status']=='PASS'else 1)and w['command']==record['command']and w['limit_failure']is None and w['rss_cap_mib']==512 and  w['own_child_only']is True and w['liveness_group_cleanup']is True
 assert 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 and  0<=w['sampled_peak_rss_mib']<512
 if record['status']=='PASS':assert record['log_sha256']==lp['sha256']
 add(lp,'oldv10_all46_current_logs_preserved');add(wp,'oldv10_all46_current_watchdogs_preserved');closures.append(dict(label=record['label'],status=record['status'],actual_exit=w['returncode'],log_pin=lp,watchdog_pin=wp))
target=pin(TARGET);assert target['size_bytes']==749355952 and  target['identity'][3]==1 and  TARGET.lstat().st_uid==os.getuid()
assert str(TARGET)not in PROTECTED and not OBSERVED_TARGET_PF_FIELDS
assert not any(p['identity'][:2]==target['identity'][:2]for p in PROTECTED.values())
files=[];dirs={};links={};stack=[OLD]
while stack:
 folder=stack.pop();dirs[str(folder)]=ident(folder.lstat())
 for p in sorted(folder.iterdir()):
  q=p.lstat()
  if stat.S_ISDIR(q.st_mode):stack.append(p)
  elif stat.S_ISREG(q.st_mode):
   if p!=TARGET:files.append(pin(p))
  elif stat.S_ISLNK(q.st_mode):links[str(p)]=dict(identity=ident(q),target=os.readlink(p))
  else:raise RuntimeError('unexpected oldv10 special file')
 for p in files:
  if p['path']not in PROTECTED:add(p,'all_other_oldv10_files_must_remain')
 guard()
# Genuine original full ART logical nofollow observer, no compiler/numerics.
fpath=R/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py';fpin=pin(fpath);spec=importlib.util.spec_from_file_location('readonly_original_history_factory_v10_survey',fpath);factory=importlib.util.module_from_spec(spec);spec.loader.exec_module(factory)
observer=factory.DynamicHistoryResources(ART,factory.history_roots([],ART),8*2**30,96*2**30);budget=observer.check();guard()
reserve=96*2**30-budget['artifact_bytes']-20971764748-64*2**20-2*2**30
prediction=dict(after_only_candidate_artifact_bytes=budget['artifact_bytes']-749355952,after_only_candidate_regular_files=budget['regular_files']-1,after_original_initial_reserve_bytes=reserve+749355952,initial_reserve_would_be_admitted=reserve+749355952>0,free_bytes_after_unlink_not_predicted_APFS_reclaim_not_assumed=True)
proc=subprocess.run(['/bin/ps','-axo','pid=,command='],capture_output=True,text=True,timeout=10)
assert proc.returncode==0;live=[]
for line in proc.stdout.splitlines():
 f=line.strip().split(None,1)
 if len(f)==2 and  int(f[0])!=os.getpid()and(str(OLD/'runtime/')in f[1]or str(REC/'aaa_three_plane_streaming_pipeline_source_v10/run_actual_three_plane_pipeline.py')in f[1]):live.append(dict(pid=int(f[0]),command=f[1]))
assert not live
value=dict(schema='READONLY_OLD_V10_PRIVATE_PROJECT_ACTUAL_CURRENT_GATE_UNION_AND_BUDGET_SURVEY_V1',status='ONE_CANDIDATE_NO_CURRENT_PHYSICAL_DEPENDENCY_OBSERVED_NO_RELEASE',candidate_current_full_EOF_pin=target,
 all_current_protected_EOF_pins=sorted(PROTECTED.values(),key=lambda x:x['path']),selected_gate_metadata_origins=ORIGINS,selected_gate_roles={k:sorted(v)for k,v in ROLES.items()},explicit_only_device_current_reattestations=CHANGES,
 current_completed_Source_namespaces=[str(x)for x in roots],direct_typed_TARGET_pin_occurrences_in_all_selected_Source_JSON=OBSERVED_TARGET_PF_FIELDS,target_path_and_inode_disjoint_from_complete_selected_mandatory_union=True,
 oldv10_all46_genuine_child_closures=closures,oldv10_other_complete_regular_file_pins=sorted(files,key=lambda x:x['path']),oldv10_complete_directory_identities=dirs,oldv10_complete_symlinks=links,
 oldv10_failed_summary_preserved=True,current_v11_and_v12_PROJECT_and_v12_all_curveproof_files_protected=True,
 genuine_original_ART_budget_snapshot=budget,original_initial_reserve_bytes=reserve,one_candidate_release_prediction_only=prediction,
 no_live_oldv10_owner_or_runtime_observed=True,future_v13_Source_and_current_gates_unknown_not_prefilled=True,release_requires_reprove_final_actual_v13_frozen_DAG=True,
 old10_business_cleanup_79files_12605160148bytes_not_incremented=True,unlink_or_release_Source_written=False,numerical_or_compile_business_started=False,
 future_replay_cost='After future exact release only oldv10 wholePROJECT/GLOBAL-subtree raw path unavailable; all current original producer/math/control receipts and oldv10 other files retained.',
 checks=CHECKS,unique_full_EOF_files=len(CACHE),unique_full_EOF_bytes=sum(x['size_bytes']for x in CACHE.values()),wall_seconds=time.monotonic()-START,SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,qualified=False,goal_complete=False)
p=HERE/'FULL_CURRENT_GATE_UNION_AND_EXACT_OLD_V10_CANDIDATE_READONLY_REVIEW.json'
with p.open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
report=f'''旧v10 private PROJECT单候选只读调查（2026-10-13）
当前选定v12HF/actualfixed2654、v11fixed2643/currentowned163、catalog3040/Common2012、savedv2 3315/1129、materialv7/GENDFv4/parserv2/refv2实际selected gate fullpins及完整Source枚举：候选path/inode无物理依赖；不是文本grep结论。全选定Source JSON typed fullPF也无该target出现。
候选 {TARGET}\nSHA {target['sha256']}\n全部7ID {target['identity']}\n唯一749355952B、当前UID-owned nlink1独立inode，仅作候选；未删除、未写释放执行Source。
旧v10真Root closedEXIT1、46watch/log均真实闭合；保留全部其他{len(files)}普通文件/{len(dirs)}目录/{len(links)}symlink完整清单与PF，failed aggregate不变为PASS。当前v11及v12 PROJECT保留，v12全部最新曲线文件也列mandatory保护。
原ART真实logical {budget['artifact_bytes']}B，{budget['regular_files']}files，free {budget['disk_free_bytes']}B；扣原cold20971764748+meta64MiB+完整fresh2GiB后reserve={reserve}B。
若后续仅释放此候选，预测ART {prediction['after_only_candidate_artifact_bytes']}B/{prediction['after_only_candidate_regular_files']}files、reserve={prediction['after_original_initial_reserve_bytes']}B；不猜APFS实际free回收。完整当前gate union及原资源roots在JSON保留，不重复大量资源日志。
候选代价：以后旧v10完整PROJECT/GLOBAL-subtree原路径不能raw回放，其它生产/math/control/结果文件保留；原v11和v12的大PROJECT继续live。
未来v13 SourceHF尚未知，不能预填保护或把这次调查当最终释放准入；必须在真正新DAG冻结后重证明，再由Root决定单次清理。原业务10批79文件12605160148B不增加。
真实读取{len(CACHE)}文件、{sum(x['size_bytes']for x in CACHE.values())}B，checks={CHECKS}；无physics/编译/删除，qualification=false/goal_complete=false。
'''
with(HERE/'REPORT.txt').open('x')as f:f.write(report);f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=value['status'],review_pin=pin(p),report_pin=pin(HERE/'REPORT.txt'),candidate_pin=target,
 art_bytes=budget['artifact_bytes'],art_files=budget['regular_files'],free_bytes=budget['disk_free_bytes'],original_initial_reserve_bytes=reserve,
 predicted_after_release_reserve=reserve+749355952,protected_count=len(PROTECTED),other_v10_files=len(files),full_EOF_files=len(CACHE),full_EOF_bytes=sum(x['size_bytes']for x in CACHE.values()),release_executed=False)))
