"""Freeze already closed finite proof and actual Source, no business execution."""
import hashlib,json,os,stat,sys
from pathlib import Path
ROOT=Path('/Users/wen/spot')
REC=ROOT/'validation/axial_material/root64_epoch_recovery_20261011'
BUNDLE=REC/'streaming_full_ledger_serializer_min5_source_bundle_v1_20261013'
PROOF=Path(__file__).resolve().parent
ART=ROOT/'validation/artifacts'
ACTUAL=ART/'axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v12'

def identity(p):
 s=p.lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p,wanted=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2])
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before
  sha=hashlib.file_digest(f,'sha256').hexdigest();s=os.fstat(f.fileno())
  assert[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]==before==identity(p)
 row=dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
 if wanted is not None:assert all(row[k]==wanted[k]for k in row)
 return row
def write(p,d):
 with p.open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def main():
 inverse=json.loads((BUNDLE/'COMPLETE_FOUR_SOURCE_BYTE_INVERSE.json').read_bytes())
 originals=[];selected={}
 for change in inverse['changes']:
  old=pin(change['original_Source_pin']['path'],change['original_Source_pin'])
  new=pin(change['new_Source_pin']['path'],change['new_Source_pin'])
  a=Path(old['path']).read_bytes();b=Path(new['path']).read_bytes();restored=b.decode()
  for delta in reversed(change['exact_ordered_changes']):
   assert restored.count(delta['new_block'])==delta['count']
   restored=restored.replace(delta['new_block'],delta['old_block'])
  assert restored.encode()==a
  originals.append(old);selected[change['role']]=new
 reports={};checked={}
 for mode in ('canonical','guard'):
  path=PROOF/mode/'REVIEW.json';p=pin(path);d=json.loads(path.read_bytes())
  assert d['status']=='FINITE_COMPLETE_NOT_BUSINESS_QUALIFICATION'and d['failure']is None
  for row in d['complete_input_pins']:
   current=pin(row['path'],row)
   assert current['path']not in checked or checked[current['path']]==current
   checked[current['path']]=current
  reports[mode]=p
 canonical=json.loads(Path(reports['canonical']['path']).read_bytes())['evidence']
 guard=json.loads(Path(reports['guard']['path']).read_bytes())['evidence']
 assert canonical['all45_full_byte_comparison'] and len(canonical['canonical_prefixes'])==45
 assert canonical['canonical_prefixes']==guard['all45_verified_prefixes']
 assert guard['full45_records_preserved']and guard['actual_new_guard_record']['status']=='PASS'
 assert guard['baseline']['current_RSS_bytes']==294928384 and guard['final']['SELF_peak_bytes']==295092224
 tools=pin(PROOF/'ACTUAL_TWO_FINITE_TRUE_TOOL_RETURNS.json')
 td=json.loads(Path(tools['path']).read_bytes())
 assert all(td[k]['original_integer_exit_code']==0 and td[k]['observed_closed']for k in ('canonical','guard'))
 original_hf_path=REC/'aaa_three_plane_streaming_pipeline_source_v12/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
 original_hf_pin=pin(original_hf_path);original_hf=json.loads(original_hf_path.read_bytes())
 original_dependencies=[pin(row['path'],row)for row in original_hf['dependencies']]
 provenance=[pin(p)for p in (
  REC/'ROOT_EXACT_ACTUAL_PIPELINE_V12_ARGV_20261013.json',
  REC/'ACTUAL_PIPELINE_V12_PARENT_PHASE_ROOT_TRUE_TOOL_RETURNS_20261013.json',
  REC/'ROOT_MIN5_FOUR_SOURCE_DRAFT_READONLY_BYTE_REVIEW_20261013.json',
  ACTUAL/'AAA3-streaming/stages.json',ACTUAL/'Root_actual_complete_execution_record_before_final_publication.json',
  ACTUAL/'Root_actual_parent_memory_checkpoint_journal.json')]
 proof_sources=[pin(p)for p in (
  PROOF/'finite_original_bytes_and_derived_guard.py',PROOF/'EXACT_FINITE_V2_DELTA.json',Path(__file__),
  REC/'streaming_serializer_min5_finite_proof_20261013/finite_original_bytes_and_derived_guard.py',
  REC/'streaming_serializer_min5_finite_proof_20261013/canonical/REVIEW.json',
  REC/'streaming_serializer_min5_finite_proof_20261013/ACTUAL_V1_CANONICAL_TRUE_TOOL_RETURNS.json')]
 argv_prefix=['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1','OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1','VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1','/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(PROOF/'finite_original_bytes_and_derived_guard.py')]
 argv=dict(schema='CLOSED_ACTUAL_FINITE_CANONICAL_AND_DERIVED_GUARD_ARGV_V2',
  canonical_argv=argv_prefix+['--mode','canonical'],
  guard_argv=argv_prefix+['--mode','guard','--canonical-report',reports['canonical']['path'],'--canonical-sha',reports['canonical']['sha256'],'--canonical-seven',json.dumps(reports['canonical']['identity'],separators=(',',':'))],
  actual_runs_already_closed=True,reexecution_authorized=False,business_HOST_created=False,
  finite_extra_fresh_upper_bound_bytes=64*2**20,complete_business_fresh_initial_reserve_bytes=2*2**30)
 write(PROOF/'ACTUAL_FINITE_ARGV_FREEZE.json',argv);argvpin=pin(PROOF/'ACTUAL_FINITE_ARGV_FREEZE.json')
 report=(
  '四份诚实派生 Source 与两个一次性有限检查已经闭合。父 production_runner 只改完整 ledger 序列化，helper 的正常导入顺序和 ROOT、support 路径、Common 原 authority 锚点变化均有完整字节逆向记录。原 FULL/OwnRSS、全部 parent 非 dump 定义、数据、Fortran、控制与资源上限保持。\n\n'
  'canonical 真 b31802/session7787 → 4eaae9 EXIT0：45 个完整前缀由原 dump 实际写出，与新流式文件全文逐字相同；最后 11,200,725B 等于真实 v12 stages。Unicode/浮点/NaN/defaults 与三个 encoding-error 及已有目标/tmp 副作用保持。\n'
  'guard 真 937e39/session84577 → 663952 EXIT0：独立进程完整原 metadata/current69/17/catalog 准入后，保留真实 45 records、2654 fixed、163 owned 及其余运行状态；45 流式结果匹配真实 canonical SHA。原 OwnRSS 正常导入新 parent，新增一个 Python marker child 为第46项，PASS/已退出；短 child 原 watch sampled_peak=0，未冒称实际峰值采样。\n'
  'baseline 294,928,384B；stream45+guard 后峰值 295,092,224B，增加 163,840B（160KiB）。2828 唯一输入在该有限检查前后全文 EOF/all7 保持。无 profiling/peak reset/测量期 GC、module/class monkeypatch 或 numerical。\n\n'
  '第一次 v1 canonical 真 c409ce/session17997 → 7a04a7 EXIT1 被额外完整业务2GiB初始预留拦住，未开始dump；原失败与Source保留。v2 仅对本有限检查加64MiB输出上限/预留，原 history96/fresh2/cold+64metadata/free8/SELF512/stage600/whole1800 保持。完整业务仍必须预留2GiB。\n'
  '本证据说明有限数据/错误契约一致，完整实际运行状态下该序列化路径未累计大内存。没有执行或创建 v13 HOST，也不授完整工程、AAA/ABA、材料或 reference 资格。v12 原 EXIT1/45 stages/1997 journal 为历史失败因果保留。\n')
 with(BUNDLE/'REPORT.txt').open('x')as f:f.write(report)
 reportpin=pin(BUNDLE/'REPORT.txt')
 freeze=dict(schema='COMPLETE_IMMUTABLE_MIN5_FOUR_SOURCE_SERIALIZER_BUNDLE_AND_CLOSED_FINITE_PROOF_V1',
  source_rebound_serializer_only=True,selected_derived_source_pins=selected,
  original_source_lineage_pins=originals,complete_byte_inverse_pin=pin(BUNDLE/'COMPLETE_FOUR_SOURCE_BYTE_INVERSE.json'),
  original_v12_host_source_freeze_pin=original_hf_pin,original_v12_dependencies_as_unchanged_authority_and_provenance=original_dependencies,
  closed_actual_finite_report_pins=reports,actual_true_tool_returns_pin=tools,actual_finite_argv_pin=argvpin,
  finite_fixture_source_and_first_failure_pins=proof_sources,historical_v12_failure_and_root_source_review_pins=provenance,
  current_finite_observed_input_count=len(checked),current_finite_observed_input_bytes=sum(x['size_bytes']for x in checked.values()),
  fullEOF_sameSHA_all7_observation_complete=True,
  finite_input_tables_are_report_evidence_not_a_new_business_dependency_graph=True,
  final_report_pin=reportpin,source_writers_stopped=True,normal_import_no_production_module_cache_mutation=True,
  original_FULL_and_OwnRSS_Source_identity_retained=True,new_parent_module_identity_honestly_derived=True,
  whole_parent_non_dump_functions_and_classes_byteexact=True,all45_original_complete_JSON_bytes_equal=True,
  canonical_errors_and_existing_tmp_sideeffects_equal=True,pure_stream_complete_live_state_growth_bytes=163840,
  finite_guard_dummy_closed0=True,short_child_sampled_peak_MiB=0.0,
  original_time_memory_storage_environment_caps_retained=True,finite_additional_fresh_cap_bytes=64*2**20,
  complete_business_initial_fresh_reserve_bytes=2*2**30,
  memory_repair_full_pipeline_proven=False,v13_business_HOST_created=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
 hf_path=BUNDLE/'COMPLETE_SERIALIZER_BUNDLE_SOURCE_FREEZE.json';write(hf_path,freeze);hfpin=pin(hf_path)
 handoff=dict(schema='FINAL_MIN5_ACTUAL_FOUR_SOURCE_AND_TWO_FINITE_PROOFS_FROZEN_HANDOFF_V1',
  source_freeze_pin=hfpin,selected_derived_source_pins=selected,closed_finite_reports=reports,
  actual_true_tool_returns_pin=tools,actual_finite_argv_pin=argvpin,final_report_pin=reportpin,
  source_writers_stopped=True,awaits_independent_finite_source_review=True,
  v13_business_HOST_created=False,pipeline_repair_proven=False,AAA_qualified=False,ABA_admitted=False)
 hp=PROOF/'FINAL_ACTUAL_FROZEN_BUNDLE_HANDOFF.json';write(hp,handoff)
 print(json.dumps(dict(status='FROZEN_CLOSED_FINITE_ONLY',unique_complete_current_inputs=len(checked),complete_current_bytes=sum(x['size_bytes']for x in checked.values()),source_freeze_pin=hfpin,argv_pin=argvpin,handoff_pin=pin(hp)),allow_nan=False))
if __name__=='__main__':main()
