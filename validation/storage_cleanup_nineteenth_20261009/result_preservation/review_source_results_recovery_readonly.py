"""Finite read-only old iteration state/result and restore-source audit. No business imports."""
import ast,hashlib,json,os,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts'
OUT=Path('/private/tmp/spot_storage_nineteenth_AAA_early_snapshots_preservation_review_20261009')
PLAN=Path('/private/tmp/spot_storage_nineteenth_root_20261009/fixed_candidate_plan.json')
PS='b0cf9e8577d91ee6c3be70eada54d3f7f20078335e60db08a43ed1b3a093b79a'
PINS={}
def identity(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,expected=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]);b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
 assert identity(p)==before and (expected is None or h==expected),(str(p),h,expected)
 PINS[str(p)]={'path':str(p),'identity':before,'sha256':h,'bytes':len(b)};return b
def obj(p,expected=None):return json.loads(raw(p,expected))
def strings(x):
 if isinstance(x,dict):
  for k,v in x.items():yield str(k);yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 elif isinstance(x,str):yield x
def normalize(s):
 if s.startswith('validation/'):return str(ROOT/s)
 return s
started=time.monotonic();p=obj(PLAN,PS)
families={'axial-material-production-qualified-AB-white-trace-20261004':11,'axial-material-production-qualified-AB-rank1-factor-cache-20261007':12,'axial-material-production-qualified-AB-compensated-20261004':4}
regular={str(ART/n/'AAA'/f'map{i:03d}'/'closed_snapshots.xsm') for n,last in families.items() for i in range(1,last-2)}
links={str(ART/n/'AAA'/f'map{i+1:03d}'/'parent_snapshots_closed.xsm') for n,last in families.items() for i in range(1,last-2)}
assert len(regular)==len(links)==18 and {r['path'] for r in p['regular']}==regular and {r['path'] for r in p['symlinks']}==links
assert p['logical_bytes']==4283202816 and p['allocated_bytes']==4283228160
for row in p['regular']:
 path=Path(row['path']);assert identity(path)==row['identity'] and stat.S_ISREG(row['identity'][2]) and row['identity'][-1]==1
 seal=obj(Path(row['original_stage_seal']),row['original_stage_seal_sha256']);assert seal['classification']=='SEALED_STAGE_OUTPUTS' and seal['sha256'][path.name]==row['sha256']
for row in p['symlinks']:
 path=Path(row['path']);assert stat.S_ISLNK(path.lstat().st_mode) and identity(path)==row['identity']
 assert os.readlink(path)==row['link_text'] and str(path.resolve(strict=True))==row['target'] and row['target'] in regular
 incoming_seal=obj(path.parent/'result.json');target_row=next(r for r in p['regular'] if r['path']==row['target'])
 assert incoming_seal['sha256'][path.name]==target_row['sha256']
for path,h in p['stage_documents'].items():obj(Path(path),h)
binding=obj(Path(p['current_binding']['path']),p['current_binding']['sha256'])
assert len(binding['files'])==37395 and not (regular|links)&set(binding['files'])
mother=V/'axial_material/production_runner.py';mothertext=raw(mother).decode();mother_ast=ast.parse(mothertext)
mother_defs={n.name:ast.get_source_segment(mothertext,n) for n in ast.walk(mother_ast) if isinstance(n,ast.FunctionDef)}
source_details=[];statuses={};alllogs=0;allstagepass=0;retained_last_two_meta=[];boundary=[];prior_retired_last_two=[]
prior_deletion_rows={}
for ledger in sorted(V.glob('storage_cleanup*/*ledger*.jsonl')):
 for line_number,line in enumerate(raw(ledger).splitlines(),1):
  d=json.loads(line);candidate=d.get('candidate',d)
  if not isinstance(candidate,dict):continue
  path=candidate.get('path');h=candidate.get('sha256')
  if path and h and (d.get('deleted') is True or d.get('absent_after_unlink') is True):
   prior_deletion_rows[path]={'ledger':str(ledger),'line':line_number,'sha256':h}
for family,last in families.items():
 r=ART/family;case=r/'AAA';status=obj(case/'run_status.json');stages=obj(case/'stages.json')['stages']
 assert status['classification']=='WAITING_REFERENCE' and status['completed_maps']==last
 c=status['cases']['AAA'];assert c['classification']=='VALID_MET' and c['completed_maps']==last and c['final_directory']==str(case/f'map{last:03d}')
 assert len(c['maps'])==last and [x['epoch'] for x in c['maps']]==list(range(1,last+1))
 assert all(x['classification']=='VALID_NOT_MET' for x in c['maps'][:-1]) and c['maps'][-1]['classification']=='VALID_MET'
 assert all(x['defects']['THRESHOLD']==5e-7 for x in c['maps'])
 assert all(x['status']=='PASS' for x in stages);allstagepass+=len(stages);statuses[family]=status
 for i in range(1,last+1):
  folder=case/f'map{i:03d}';seal=obj(folder/'result.json');assert seal['classification']=='SEALED_STAGE_OUTPUTS'
  for name,h in seal['sha256'].items():
   if name.endswith('.log'):
    b=raw(folder/name,h);alllogs+=1
    if name=='check_convergence_gate.log':assert b'SPOT-GATE COMPLETE' in b and ('CLASSIFICATION='+c['maps'][i-1]['classification']).encode() in b
    if name=='check_one_map_xsm.log':assert b'ONE-MAP-XSM COMPLETE' in b
  if i>=last-1:
   assert str(folder/'closed_snapshots.xsm') not in regular and str(folder/'parent_snapshots_closed.xsm') not in links
   for name,h in seal['sha256'].items():
    path=folder/name
    if not path.exists():
     assert str(path) in prior_deletion_rows and prior_deletion_rows[str(path)]['sha256']==h,(str(path),'unknown or unmatched missing')
     prior_retired_last_two.append({'path':str(path),'original_stage_sha256':h,'prior_actual_deletion':prior_deletion_rows[str(path)]});continue
    if path.is_symlink():assert str(path.resolve(strict=True)) not in regular
    retained_last_two_meta.append({'path':str(path),'identity':identity(path),'original_stage_sha256':h,'is_symlink':path.is_symlink()})
  if i==last-2:
   q=folder/'closed_snapshots.xsm';assert str(q) not in regular and q.is_file()
   final_parent=case/f'map{last-1:03d}'/'parent_snapshots_closed.xsm'
   assert final_parent.resolve(strict=True)==q and str(final_parent) not in links
   boundary.append({'kept_closed_boundary':str(q),'kept_last_two_parent_link':str(final_parent),'original_stage_sha256':seal['sha256'][q.name]})
 assert (case/'bootstrap/result.json').is_file() and not any(Path(x).is_relative_to(case/'bootstrap') for x in regular|links)
 for name in ['prepared.json','declaration.json']:obj(r/name)
 src=r/'runtime/production_runner.py';text=raw(src).decode();tree=ast.parse(text);defs={n.name:ast.get_source_segment(text,n) for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
 for name in ['_link','verify_sealed_directory','base_inputs','seal_directory']:assert defs[name]==mother_defs[name],(str(src),name)
 assert '"parent_snapshots_closed.xsm"' in defs['run'] and '"close_r64_returned"' in defs['run'] and '"closed_snapshots.xsm"' in defs['run']
 source_details.append({'source':str(src),'sha256':PINS[str(src)]['sha256'],'exact_mother_nested_definitions':['_link','verify_sealed_directory','base_inputs','seal_directory'],'run_full_source_sha_preserved':True,'source_semantics':'bootstrap parent state -> projected proposal -> radial/axial -> close_r64_returned -> next parent; old stage seal verifies all entries if rerun'})
manifests=list(V.glob('storage_cleanup*/manifest.json'))+[V/'storage_review_20261008/first_batch_24_files.json',V/'storage_review_20261008/second_batch_replay_arrays.json',V/'storage_review_more_20261008/exact_retirement_manifest.json']
copy_master_hits=[];historic_retained_anchor_mentions=[]
def directmasters(d):
 if isinstance(d,dict):
  for k,v in d.items():
   if k in ('retained_primary','duplicate_primary','primary'):
    for s in strings(v):yield normalize(s)
   else:yield from directmasters(v)
 elif isinstance(d,list):
  for v in d:yield from directmasters(v)
for f in sorted(manifests):
 d=obj(f);hits=set(directmasters(d))&(regular|links)
 if hits:copy_master_hits.append({'manifest':str(f),'hits':sorted(hits)})
 if isinstance(d,dict):
  for key in ['retained_closed_anchors','retained_primaries']:
   if key in d:
    hits=set(map(normalize,strings(d[key])))&(regular|links)
    if hits:historic_retained_anchor_mentions.append({'manifest':str(f),'field':key,'hits':sorted(hits),'role':'historical preservation anchors, not exact-copy restore row master'})
ledger_count=0;ledger_rows=0
for f in sorted(V.glob('storage_cleanup*/*ledger*.jsonl')):
 b=raw(f);ledger_count+=1
 for line in b.splitlines():
  d=json.loads(line);ledger_rows+=1;hits=set(directmasters(d))&(regular|links)
  if hits:copy_master_hits.append({'ledger':str(f),'hits':sorted(hits)})
assert not copy_master_hits,copy_master_hits
for rec in PINS.values():assert identity(Path(rec['path']))==rec['identity']
for row in p['regular']+p['symlinks']:assert identity(Path(row['path']))==row['identity']
report={'schema':'SPOT_R19_EARLY_AAA_STATE_RESULT_PRESERVATION_AND_PRIOR_RESTORE_SOURCE_REVIEW_V1','status':'PASS','scope':'FINITE_SOURCE_SEAL_DOCUMENT_LOG_STATUS_PRIOR_COPY_RESTORE_SCOPE_ONLY; ROOT_CURRENT_GRAPH_AND_GLOBAL_INCOMING_AND_FIXED_PREDELETE_FULLSHA_ARE_COMPLEMENTARY','plan':PINS[str(PLAN)],'fixed_regular_count':18,'fixed_symlink_count':18,'fixed_regular_paths':sorted(regular),'fixed_symlink_paths':sorted(links),'logical_bytes':p['logical_bytes'],'allocated_bytes':p['allocated_bytes'],'all_18_original_stage_seal_expected_SHA_present':True,'current_binding_exact_files_hits':0,'stage_seal_is_result_json_sha256_dict_not_result_sha256_text':True,'original_run_status_fullbody_preserved':statuses,'all_map_results_and_logs_fullSHA_checked':True,'map_log_fullSHA_count':alllogs,'original_stage_PASS_count':allstagepass,'independent_accuracy_pass_inferred':False,'boundary_last_three_closed_preserved':boundary,'last_two_current_remaining_files_complete_metadata_preserved':retained_last_two_meta,'last_two_nine_original_seal_files_previously_retired_with_actual_ledger_proof':prior_retired_last_two,'original_last_two_full_seal_direct_revalidation_already_requires_prior_restoration':True,'last_two_large_numerical_content_fullSHA_reread_by_this_reader':False,'last_two_original_expected_hashes_are_from_stage_seals_and_Root_full_kept_observation':True,'all_current_existing_bootstrap_files_kept':True,'failed_AB_storage_cases_kept':True,'source_authority':source_details,'prior_exact_copy_restore_master_intersections':copy_master_hits,'prior_manifest_count':len(manifests),'prior_ledger_count':ledger_count,'prior_ledger_rows':ledger_rows,'historic_preservation_anchor_mentions_not_executable_copy_restore_edges':historic_retained_anchor_mentions,'recovery_limit':{'selected_closed_is_intermediate_immutable_per_epoch_committed_state':True,'selected_closed_is_not_exact_duplicate':True,'last_maps_or_metrics_are_not_lossless_substitute':True,'retained_last_two_current_remaining_native_results_and_closed_boundary_unchanged':True,'old_selected_stage_direct_verify_requires_recomputation_and_path_restore':True,'root_original_plan_source_training_basis_bootstrap_material_decks_and_commands_preserved':True,'original_run_cannot_overwrite_old_case_directory':True,'isolated_scratch_recompute_entire_needed_prefix_then_full_size_SHA_match_original_stage_seals_required':True,'earlier_retired_unique_projected_candidate_state_may_also_need_recompute_as_already_declared':True,'no_immediate_or_future_byte_equal_replay_promise':True,'no_new_lossless_archive_required_by_explicit_scope':True,'no97_material_metadata_unique_pack_changed':True},'candidate_snapshot_contents_fullSHA_reads_in_this_reader':0,'all_fresh_small_metadata_and_source_pins':list(PINS.values()),'all_pins_seven_identity_before_after_stable':True,'files_deleted':0,'project_written':False,'business_executed':False,'new_scientific_credit':False,'readonly_elapsed_seconds':time.monotonic()-started}
with (OUT/'REPORT.json').open('x') as f:json.dump(report,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with (OUT/'REPORT.txt').open('x') as f:f.write('第十九轮旧迭代状态独立保留审查：PASS（有限源/结果/旧恢复链范围，尚未删除）。\n'+'固定仅18份早期closed_snapshots.xsm及18条下一map parent_snapshots_closed链接，约3.989067GiB；white map001–008、rank1 map001–009、compensated map001。后三份closed、最后2map本轮前现存内容与父链接目标保留，bootstrap、失败AB/storage场景、其他数值结果不选。\n'+'原producer每map以上一closed状态制作proposal、径向/轴向更新后提交新的closed，用于下一次迭代；这些是早期迭代中间状态。三旧run_status全文保持WAITING_REFERENCE，AAA最终分别11/12/4map达到VALID_MET；不代表独立参考/AAA精度通过。所有每map result.json原sha256封存字典、checker/convergence及其他日志全文哈希核验，原门限5e-7不改。white map010和compensated map003原seal已有9项被R2/R4/R9退休，逐条原SHA和真实账本证明；最后2map的原全seal并非现在全字节齐备，不伪造恢复，也不把最后结果当旧状态无损副本。\n'+f'旧{len(manifests)}份精确manifest、{ledger_count}份账本/{ledger_rows}条直接copy恢复主本均无选中路径。R4/R9曾将部分closed作为旧唯一中间件退休后的保留anchor，该历史选择被如实记载；它们不是实际复制恢复工具的源。旧中间件本来就需重算，本轮会再增加所需重算的早期状态前缀，不暗称旧全stage直接重验仍可用。97永久gzip保留。\n'+'清理后若重验被选早期stage，须从保留原输入、训练basis、bootstrap、runtime、deck、参数与命令在隔离目录重算所需完整前缀，逐份长度/原stage SHA匹配后恢复；不能直接覆盖原case。未来逐字节重现未实证、不承诺即时恢复。不改原结果/日志/科学门，不增加科学资格。\n'+'本reader仅读源、原seal/status/log与恢复元数据并核候选身份；没有重读4GiB快照或35GiB全图。候选全文SHA与保留boundary全文SHA由Root固定plan提供，当前图/所有入链为互补独审。未删除、未写项目、未执行业务。\n')
print(json.dumps({'status':'PASS','report':str(OUT/'REPORT.json'),'sha256':hashlib.sha256((OUT/'REPORT.json').read_bytes()).hexdigest(),'regular':18,'symlinks':18,'allocated_GiB':p['allocated_bytes']/2**30,'prior_copy_restore_master_intersections':0,'small_fullSHA_pins':len(PINS),'files_deleted':0,'project_written':False}))
