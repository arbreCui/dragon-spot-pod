import json,pathlib,hashlib,stat,os,gzip,time
R=pathlib.Path('/Users/wen/spot');B=R/'validation/artifacts';V=R/'validation/iterative';D=pathlib.Path(__file__).parent;t=time.monotonic()
P=pathlib.Path('/private/tmp/spot_storage_twentieth_root_20261009/proposed_candidates_full_byte_proof.json')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
pins={}
def raw(p):
 p=pathlib.Path(p);before=ident(p);v=p.read_bytes();assert ident(p)==before,str(p)
 pins[str(p)]={'sha256':sha(v),'size_bytes':len(v),'identity':before};return v
def obj(p):
 b=raw(p);return json.loads(gzip.decompress(b) if str(p).endswith('.gz') else b)
assert sha(raw(P))=='517ef094a4cfb8163ef12db9fdc8d58c0d12584f891c09f2e90fd7af3ef6632e'
proof=obj(P);cs=proof['candidates'];assert len(cs)==30
names={'projected_proposal.xsm','candidate_radial.xsm','candidate_snapshots.xsm','candidate_axial.xsm','candidate_system.xsm','parent_for_checker.xsm'}
maps={}
for n in range(1,10):
 choices=[p for p in B.glob(f'd4a-scattering-mesh12-picard-map{n}-*') if '-review-' not in p.name and '-control-' not in p.name];assert len(choices)==1;maps[n]=choices[0]
expected={str(maps[n]/name) for n in range(1,6) for name in names};assert expected=={c['path'] for c in cs}
for c in cs:assert ident(pathlib.Path(c['path']))==c['identity'] and stat.S_ISREG(c['identity'][2]) and c['identity'][6]==1
seals={}
def manifest(p):
 v={}
 for line in raw(p).decode().splitlines():
  if line.strip():h,name=line.split(None,1);name=name.strip();assert name not in v;v[name]=h
 return v
map_evidence=[]
for n,p in maps.items():
 seal=manifest(p/'result.sha256');seals[n]=seal
 for c in cs:
  if pathlib.Path(c['path']).parent==p:
   name=pathlib.Path(c['path']).name;assert seal[name]==c['sha256']
   for manifest_name,want in c['original_manifest_sha256s'].items():assert manifest(p/manifest_name)[name]==want==c['sha256']
 gate=raw(p/'gate.log').decode();close=raw(p/'close.log').decode();chk=raw(p/'independent_check.log').decode()
 assert 'SPOT-GATE COMPLETE' in gate and f'SPOT-R64 CLOSED/{n} COMPLETE NO-TRANSPORT' in close and 'ONE-MAP-XSM COMPLETE' in chk
 classification='VALID_MET' if n==9 else 'VALID_NOT_MET';assert 'CLASSIFICATION='+classification in gate
 ctrl=list(B.glob(f'd4a-scattering-mesh12-picard-map{n}-control-*'));assert len(ctrl)==1
 st=obj(ctrl[0]/'run_status.json');assert st.get('finished_utc') and st.get('result_manifest_sha256')==pins[str(p/'result.sha256')]['sha256']
 assert st['automatic_retries']==0 and st['next_map_authorized'] is False
 for fn in ['prepare.log','admission.log','radial.runner.log','axial.runner.log','checker_parent.runner.log','map_runner.sh','radial.x2m','axial.x2m','checker_parent.x2m','parent_inputs.sha256']:
  raw(p/fn)
 raw(V/f'd4a_scattering_mesh12_picard_map{n}_result.md')
 for fn in ['closed_axial.xsm','closed_snapshots.xsm']:
  q=p/fn;assert q.is_file() and str(q) not in expected
 map_evidence.append({'map':n,'root':str(p),'classification':classification,'result_manifest_sha256':pins[str(p/'result.sha256')]['sha256'],'finished_utc':st['finished_utc'],'elapsed_seconds':st['elapsed_seconds'],'closed_states_exist_not_rehashed_in_this_scope':True})
diagnostic_evidence=[]
for n in range(1,6):
 for kind in ['pin','current']:
  choices=list(B.glob(f'd4a-mesh12-map{n}-{kind}-diagnostic-*'));assert len(choices)==1;d=choices[0]
  script=d/('read_saved.sh' if kind=='pin' else 'read_saved_current.py');s=raw(script).decode();assert 'closed_axial.xsm' in s
  if kind=='pin':assert 'closed_snapshots.xsm' in s
  inp=manifest(d/'inputs.sha256');assert not expected.intersection(inp)
  outseal=manifest(d/'result.sha256')
  for filename,h in outseal.items():assert sha(raw(d/filename))==h,(str(d),filename)
  diagnostic_evidence.append({'directory':str(d),'source_script':str(script),'direct_input_candidate_intersection':[],'retained_outputs_fresh_fullSHA':len(outseal),'historical_whole_map_manifest_precheck_requires_reconstruction_after_retirement':True})
keydocs=['d4a_mesh12_map9_final_comparison_result.md','d4a_radial_balance_result.md','d4a_neutron_balance_readiness.md','d4a_final_validation_handoff.md','d4a_corrected_acceptance_matrix.md']
for fn in keydocs:raw(V/fn)
assert 'CE k accuracy: FAIL' in (V/keydocs[0]).read_text()
balance=(V/'d4a_radial_balance_result.md').read_text();assert 'map6-20260927/candidate_radial.xsm' in balance
assert str(maps[6]/'candidate_radial.xsm') not in expected and (maps[6]/'candidate_radial.xsm').is_file()
sources=[V/'run_d4a_rank2_picard_map.sh',V/'check_d4a_corrected_acceptance.sh',V/'d4a_rank2_picard_radial.x2m',V/'d4a_rank2_picard_axial.x2m',V/'d4a_rank2_checker_parent.x2m',R/'src/SPOR64_B2W.f90']
for p in sources:raw(p)
runner=(V/'run_d4a_rank2_picard_map.sh').read_text();assert 'closed_axial.xsm closed_snapshots.xsm' in runner and 'candidate_system.xsm parent_for_checker.xsm' in runner
closer=(R/'src/SPOR64_B2W.f90').read_text();assert "call LCMDEL(output_authority,'QFISS')" in closer
for fn in ['storage_review_eighteenth_20261009/REPORT.txt','storage_cleanup_nineteenth_20261009/REPORT.txt','axial_material/last_cprime_trim_build_review_20261008/current_progress.json']:raw(R/'validation'/fn)
mapping_paths=set(R.glob('validation/storage_cleanup*/*manifest*.json'))
mapping_paths.update([R/'validation/storage_review_20261008/first_batch_24_files.json',R/'validation/storage_review_20261008/second_batch_replay_arrays.json',R/'validation/storage_review_more_20261008/exact_retirement_manifest.json'])
mapping_paths={p for p in mapping_paths if p.name in ['manifest.json','cache_manifest.json','audit_metadata_manifest.json','runtime_retirement_manifest.json','exact_retirement_manifest.json','first_batch_24_files.json','second_batch_replay_arrays.json']}
mapping_paths.update([R/'validation/storage_review_eighteenth_20261009/Root/approved_fixed_plan.json.gz',R/'validation/storage_cleanup_nineteenth_20261009/Root/fixed_candidate_plan.json'])
def strings(x):
 if isinstance(x,dict):
  for k,v in x.items():yield str(k);yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 elif isinstance(x,str):yield x
intersections=[]
for p in sorted(mapping_paths):
 x=obj(p);hit=expected&set(strings(x));assert not hit,(str(p),hit)
ledgers=set(R.glob('validation/storage_cleanup*/**/*ledger*.jsonl'));ledger_rows=0
for p in sorted(ledgers):
 data=raw(p).decode()
 for line in data.splitlines():
  if line.strip():x=json.loads(line);ledger_rows+=1;assert not expected&set(strings(x)),str(p)
old_restore_source=[]
for p in sorted(R.glob('validation/storage_cleanup*/**/*restore*.py')):
 data=raw(p).decode();hits=[x for x in expected if x in data];assert not hits,(str(p),hits);old_restore_source.append(str(p))
for c in cs:assert ident(pathlib.Path(c['path']))==c['identity']
for p,pin in pins.items():assert ident(pathlib.Path(p))==pin['identity'],p
out={'schema':'SPOT_R20_MESH12_EARLY_WORK_FILES_RESULT_PRESERVATION_READONLY_REVIEW_V1','status':'PASS_RESULT_PRESERVATION_AND_PRIOR_RESTORE_SCOPE','scope':'ORIGINAL_SOURCE_AND_RETAINED_RESULTS; CURRENT_DEPENDENCY_AND_ACTUAL_CLEANUP_REQUIRE_PEER_AND_ROOT_SCOPE','project_written':False,'files_deleted':0,'business_executed':False,'approved_scope_candidate_paths':sorted(expected),'candidate_count':30,'candidate_logical_bytes':sum(c['size_bytes'] for c in cs),'candidate_allocated_bytes':sum(c['allocated_bytes'] for c in cs),'candidate_whole_content_read_bytes_here':0,'candidate_fullSHA_inherited_from_fresh_root_proof':{'path':str(P),'sha256':pins[str(P)]['sha256'],'candidate_all_identities_stable_in_this_scope':True,'all_original_seal_SHA_values_independently_reparsed':True},'original_map_outcomes':map_evidence,'diagnostic_direct_input_review':diagnostic_evidence,'prior_restore_mapping_count':len(mapping_paths),'prior_mapping_candidate_or_master_intersections':intersections,'prior_ledger_count':len(ledgers),'prior_ledger_rows':ledger_rows,'prior_ledger_candidate_intersections':[],'prior_restore_source_count':len(old_restore_source),'prior_restore_literal_candidate_intersections':[],'all_small_source_document_and_retained_diagnostic_pins':pins,'retention_boundary':{'all_bootstrap_kept':True,'all_nine_closed_pairs_kept':True,'all_maps6_to9_files_kept':True,'map6_real64_QFISS_balance_authority_kept':True,'all_existing_reports_numeric_summaries_logs_seals_sources_inputs_kept':True,'map9_VALID_MET_and_final_CE_k_FAIL_kept':True,'unique_final_result_retired':False},'recompute_boundary':{'early_work_files_are_exact_duplicates':False,'closed_states_are_lossless_substitute_for_RETURNED_QFISS_or_early_raw':False,'historical_full_manifest_and_checker_or_diagnostic_precheck_will_no_longer_pass_directly':True,'must_recompute_in_separate_scratch_with_retained_bootstrap_previous_closed_runtime_sources_inputs_original_parameters_and_compare_every_old_size_SHA_before_restoring':True,'same_bytes_reproducibility_not_demonstrated_by_this_review':True,'no_instant_lossless_restore_promised':True,'old_result_manifests_and_failure_facts_must_not_be_edited':True,'estimated_original_elapsed_seconds_maps1_to5':sum(x['elapsed_seconds'] for x in map_evidence[:5])},'no_new_scientific_accuracy_credit':True,'limits':['Does not authorize running existing historical validators on deleted inputs; restore by verified recomputation first.','Current complete graph/namespace/alias/owner/read-chain/incoming-link exclusion remains a separate peer review.','No new full read of the 35GB scientific input set or candidate 2.58GB in this reader.'],'reviewer_preliminary_discovery_error':{'chunk_id':'85b73d','returncode':1,'cause':'Review-only date suffix filter also matched control/review directories; no project write or business execution; corrected by explicit exclusion.'},'elapsed_seconds':time.monotonic()-t}
text='R20 mesh12 旧工作文件结果保留独审\n\n固定建议仅 map1..5 六类共30份：projected_proposal、candidate_radial、candidate_snapshots、candidate_axial、candidate_system、parent_for_checker。逻辑2,580,841,168字节，分配2,580,910,080字节。它们是原 B2J/径向/轴向/检查器过程的阶段工作状态，不是逐字节重复文件；本独审不声称 closed 可无损替代 RETURNED/QFISS。\n\n九轮全部 closed 状态与 bootstrap/原输入链接留，map6..9全套留。早五轮原 VALID_NOT_MET、map9 VALID_MET、最终 CE k FAIL 原事实留。10组早期 pin/current 保存诊断的直接提取输入为 closed 状态/track，未命中这30份；现有诊断结果逐份全文SHA通过。map6 candidate_radial 是独立 REAL64 QFISS balance 输入，必须留。\n\n旧16份恢复清单及R18/R19实际计划、既有逐项账本和恢复源码都未把这30份作为已删产物的唯一复制主本。保留全部文档、数值汇总、源代码、输入、参数、日志与原SHA清单。\n\n删除后早期 result/input/output wholemanifest 和九轮整链独立 checker 无法原地直接完整重验，早期诊断脚本的全清单前置检查也会拒绝。需要在隔离目录按保留原输入/runtime/父closed和原命令重算并逐份比旧size/SHA后恢复；未证明未来逐字节重现，也不承诺即时恢复。原五轮耗时合计约20.86小时。\n\n本报告仅结果保留/原源码用途/恢复链范围PASS；完整当前依赖和全入链排除、正式预检/精确执行仍须Root与graph独审。未删、未改项目、未执行科学业务；未重读35GB或候选2.58GB。\n'
for name,value in [('REPORT.json',json.dumps(out,ensure_ascii=False,indent=2)+'\n'),('REPORT.txt',text)]:
 with (D/name).open('x') as f:f.write(value);f.flush();os.fsync(f.fileno())
print(json.dumps({'status':out['status'],'report':str(D/'REPORT.json'),'sha256':sha((D/'REPORT.json').read_bytes()),'count':len(expected),'small_pins':len(pins),'prior_manifests':len(mapping_paths),'prior_ledgers':len(ledgers)},ensure_ascii=False))
