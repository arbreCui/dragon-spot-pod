from pathlib import Path
import json,hashlib,os,stat
R=Path('/Users/wen/spot');O=Path('/private/tmp/spot_storage_nineteenth_cache_backup_readonly_20261009')
KEYS=('dev','ino','mode','size','mtime_ns','ctime_ns','nlink');pins=[]
def ident(p):
 s=Path(p).lstat();return [getattr(s,'st_'+k) for k in KEYS]
def pin(p,sha=None):
 p=Path(p);before=ident(p);b=p.read_bytes();assert before==ident(p)
 h=hashlib.sha256(b).hexdigest()
 if sha:assert h==sha,(str(p),h,sha)
 pins.append({'path':str(p),'bytes':len(b),'sha256':h,'identity':before});return b
def read(p,sha=None):return json.loads(pin(p,sha))
def meta(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 return {'path':str(p),'logical_bytes':s.st_size,'allocated_bytes':s.st_blocks*512,'identity':ident(p)}
before=read('/private/tmp/spot_storage_eighteenth_root_readonly_20261009/before.json')
post=read('/private/tmp/spot_storage_review_eighteenth_core_postterminal_20261009/REPORT.json','27a343f1c2d5499220d7e83c2f4cfae3e37b2004178430f2fbd350fe756fab54')
prior=read('/private/tmp/spot_storage_review_eighteenth_build_cache_20261009/REPORT.json','501c2257acb1f25b6278028dec7432d3c7644a8ccc6d0918c66c9fe6f212206f')
pin(R/'validation/storage_review_eighteenth_20261009/REPORT.txt')
retained=read(R/'validation/storage_review_eighteenth_20261009/retained_results/FINAL_REPORT.json')
screen=read(O/'initial_filtered_readonly_tool_observations.json')
assert screen['explicit_no_ignore_screen']['exit_code']==0
matched=sorted(str(R/p) for p in screen['explicit_no_ignore_screen']['output'].splitlines())
cache=[meta(q['path']) for q in before['cache_like']]
assert all(q['identity']==old['identity'] for q,old in zip(cache,before['cache_like']))
derivative={q['path']:q for q in prior['held_cache_current_source_derivative_paths']}
assert set(matched)==set(derivative)
W=R/'validation/artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009'
binding=read(W/'own_rss_binding.json','4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930')
graph=read(R/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
expected=set(binding['files']);canonical={q['path'] for q in graph['canonical_files']}
resource_roots=[Path(x) for x in binding['resource_info']['resource_roots']]
holds=[]
for q in cache:
 p=Path(q['path']);source=p.parent.parent/(p.name.split('.cpython-',1)[0]+'.py') if '.cpython-' in p.name else None
 reason={'exact_frozen_expected':str(p) in expected,'current_canonical_input':str(p) in canonical,'current_complete_resource_root_subtree':any(p.is_relative_to(x) for x in resource_roots),'explicit_current_canonical_source_derived_cache_location':str(p) in derivative,'paired_source_current_canonical':source is not None and str(source) in canonical,'declared_environment_namespace_cache_position_excluded_from_candidate_review':str(p) in binding['producer_environment']['files']}
 assert any(reason.values()),str(p)
 holds.append({**q,'protection':reason})
candidate=read('/private/tmp/spot_storage_review_eighteenth_build_cache_20261009/compiled_candidate_screen.json','4023b780e79414db91a238e3c169f0e78d6b9c211dd03f74049246221ea04ae5')
assert all(not os.path.lexists(q['path']) for q in candidate['candidates'])
directories=[]
for rel in ('build','target','dist','node_modules','vendor','.cache','.ruff_cache','.pytest_cache','__pycache__','tmp','temp','src/build','Ganlib/build','Trivac/build','Utilib/build'):
 p=R/rel;directories.append({'path':str(p),'present':os.path.lexists(p),'is_directory':p.is_dir() and not p.is_symlink()})
objects=[meta(p) for stem in ('src','Ganlib/src','Trivac/src','Utilib/src') for p in (R/stem).glob('*.o')]
assert {q['path'] for q in objects}==set(post['remaining_o_exact15_paths'])
assert set(q['path'] for q in objects)=={q['path'] for q in candidate['frozen_object_HOLD']+candidate['current_source_reference_context_HOLD']}
assert all(q['identity']==next(x['identity'] for x in candidate['frozen_object_HOLD']+candidate['current_source_reference_context_HOLD'] if x['path']==q['path']) for q in objects)
assert all(ident(q['path'])==q['identity'] for q in cache)
unique={(q['identity'][0],q['identity'][1]):q for q in cache}
summary={'regular_paths':len(cache),'unique_inodes':len(unique),'logical_bytes':sum(q['logical_bytes'] for q in unique.values()),'allocated_bytes':sum(q['allocated_bytes'] for q in unique.values())}
out={'schema':'SPOT_R19_FINITE_COMMON_CACHE_BACKUP_READONLY_V1','status':'NOOP_NO_NEW_SAFE_CACHE_BACKUP_CANDIDATES','approved_deletion_candidates':[],'files_deleted':0,'project_written':False,'business_import_API_constructor_solver_native_build_executed':False,'scientific_progress_or_budgets_changed':False,'cache_complete_R18_known_set_fresh_seven_identities_exact':True,'held_cache_summary':summary,'current_frozen_expected_path_count':len(expected),'current_canonical_path_count':len(canonical),'current_resource_root_count':len(resource_roots),'nonartifact_common_backup_tmp_cache_pattern_matches':matched,'matched_are_only_previous_current_source_derivative_cache_HOLD':True,'cache_HOLD_exact_metadata_and_current_membership':holds,'finite_root_build_tmp_presence':directories,'remaining_objects_exact_R18_HOLD_count':len(objects),'remaining_objects_HOLD_paths':[q['path'] for q in objects],'R18_already_retired_core_absent':len(candidate['candidates']),'R18_low_benefit_support5_files_still_retained':retained['low_benefit_support5_files_retained'],'no_new_scan_of_artifact_payloads_or_recovery_history':'159 known cache paths only; no all-artifacts walk, science-content hash or Git/history scan','all_result_documents_failed_facts_stdio_seals_restore_sources_archives_and_current_frozen_inputs_preserved':True,'full_input_pins':pins}
with (O/'REPORT.json').open('x') as f:json.dump(out,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
with (O/'REPORT.txt').open('x') as f:
 f.write('第十九轮普通缓存/备份有限只读复查：NOOP，新可安全删除项0；未删除或修改项目，无业务/编译/native。\n')
 f.write(f'R18后已退役{len(candidate["candidates"])}份core产物仍缺席，不重复列收益。剩余{len(objects)}个.o与R18 frozen/current source引用保留集合和七身份一致；根build/target/dist/vendor/tmp等没有新增。\n')
 f.write(f'现存{len(cache)}个已知Python缓存七身份与R18完整记录相同：logical{summary["logical_bytes"]:,}B、allocated{summary["allocated_bytes"]:,}B。全部命中当前冻结读取、完整历史资源根或明确current canonical源衍生缓存位置，严格排除，不因可生成便移除。\n')
 f.write('非ART显式含ignored的常见.bak/.orig/~/.tmp/.temp/.backup/.log.bak/.pyc/.pyo筛选只出现2个原frozen_AAA衍生.pyc：validation/axial_material/__pycache__/frozen_AAA_axial_sensitivities.cpython-312.pyc和frozen_AAA_axial_sensitivities_metadata.cpython-312.pyc；它们原已明确HOLD，配套源仍在当前canonical集合。无新增常见备份或临时文件。\n')
 f.write('R18约55KiB的5份旧审计源码支持副本继续保留；收益低且有来源/恢复说明价值。所有结果/失败/日志/永久恢复资料和当前37,395读集、35,647主本、声明环境及源码缓存位置均保留。没有重复扫描整个artifacts/Git历史或读取35GB科学内容；本结论仅覆盖上述有限常见缓存/备份范围，不宣称全部旧数据不可精简。\n')
b=(O/'REPORT.json').read_bytes()
print(json.dumps({'status':out['status'],'report':{'path':str(O/'REPORT.json'),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()},'cache_count':len(cache),'common_matches':matched,'approved_deletion_candidates':[],'files_deleted':0,'project_written':False},ensure_ascii=False))
