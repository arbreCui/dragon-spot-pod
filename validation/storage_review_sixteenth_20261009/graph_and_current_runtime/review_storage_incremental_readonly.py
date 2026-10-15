import hashlib,json,os,stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');D=Path('/private/tmp/spot_storage_sixteenth_graph_readonly_20261009'); PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def metadata(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink()
 return dict(path=str(p),logical_bytes=s.st_size,allocated_bytes=s.st_blocks*512,identity=identity(p))
def pin(p,sha=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and p.resolve()==p
 h=hashlib.sha256()
 with p.open('rb') as stream:
  while b:=stream.read(4*2**20):h.update(b)
 assert identity(p)==before
 r=dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[3],identity=before)
 assert sha is None or r['sha256']==sha
 PINS[str(p)]=r;return r

def read(p,sha=None):
 r=pin(p,sha);d=json.loads(Path(p).read_text());assert identity(p)==r['identity'];return d
R15=ROOT/'validation/storage_review_fifteenth_20261009'
old=read(R15/'large_inputs_and_cache/REPORT.json','001e4095acac86552450194e333f5f0541d6fda6513210cd41db26516ae275e2')
pin(R15/'REPORT.txt');pin(ROOT/'validation/storage_cleanup_fourteenth_20261009/REPORT.txt')
oldclose=read(R15/'Root_actual_preservation_closeout.json')
fresh=read('/private/tmp/spot_storage_sixteenth_root_readonly_20261009/before.json','8da7a4c7c8b51d9552a22c686e2f4ea390abc7e214b1331fbc92383dffb57857')
plan=read('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
SOURCE=Path(plan['source_root']);OUTPUT=Path(plan['future_output_root']);TERM=Path(plan['declaration_terminal_root']);CONTROL=Path(plan['future_control_terminal_root'])
for k in ['formal_factory','formal_consumer','formal_intake_binding']:pin(plan[k]['path'],plan[k]['sha256'])
proof=read('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json','31f29c1b5642ad86d980623363a29cb15f19c2f7094bb95a4fa6393e2651f8d0')
proofreceipt=read('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/actual_readonly_tool_return.json','29130c3bd1315061174d540308b331b9838fa57f69618847251e3fd1583f8b4c')
assert proof['status']=='PASS' and type(proofreceipt['actual_tool_result']['exit_code']) is int and proofreceipt['actual_tool_result']['exit_code']==0 and proofreceipt['actual_tool_result']['closed'] is True
# Fresh stat binding to the recent full actualDECLARE scientific input audit.
# Do not re-read those 35GB or the complete graph64MB a second time.
assert identity(proof['graph_pin']['path'])==proof['graph_pin']['identity']
source_metas={str(p):metadata(p) for p in SOURCE.iterdir()}
assert sorted(Path(p).name for p in source_metas)==plan['expected_SOURCE_files']
for path,rec in proof['SOURCE31_pins'].items():assert source_metas[path]['identity']==rec['identity']
seal=read(SOURCE/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
prepared=read(OUTPUT/'prepared.json');assert prepared['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision' not in prepared
output_metas={str(p):metadata(p) for p in OUTPUT.rglob('*') if p.is_file() and not p.is_symlink()}
assert len(prepared['local_files'])==43 and set(output_metas)=={str(OUTPUT/k) for k in prepared['local_files']}|{str(OUTPUT/'prepared.json')}
assert len(output_metas)==44
m=read(SOURCE/'rank1_factor_cache_admission.json',seal['files']['rank1_factor_cache_admission.json'])
assert len(m['files'])==37339 and len(m['component_resource_roots'])==236
assert prepared['resource_roots']==m['component_resource_roots']
for k in ['case_spec','rank_addendum','declaration']:
 item=prepared[k];assert Path(item['path']).parent==SOURCE
rootset=set(m['component_resource_roots']);assert str(SOURCE) in rootset and str(OUTPUT) in rootset and str(TERM) in rootset and str(CONTROL) in rootset
# Only selected already-held duplicate pairs are hashed. They remain required
# by actual local_files and SOURCE full namespace; no deletion permission.
master=Path(m['combined_runtime']['path']);pairs=[]
for name,primary in [('runtime/Dragon',master),('runtime/rank1_factor_cache_admission.json',SOURCE/'rank1_factor_cache_admission.json'),('runtime/conditional_white_receiver_variant.json',SOURCE/'conditional_white_receiver_variant.json'),('declaration.json',SOURCE/'declaration.json')]:
 candidate=OUTPUT/name;want=prepared['local_files'][name];cp=pin(candidate,want);pp=pin(primary,want)
 row=metadata(candidate);row.update(status='HOLD',full_fresh_SHA=cp['sha256'],retained_primary=pp,exact_byte_duplicate=True,
  current_exact_path_dependency=dict(prepared=str(OUTPUT/'prepared.json'),local_files_key=name,expected_SHA=want,controller_source=str(SOURCE/'production_runner.py'),consumer='verify_prepared lines638-659; all local_files hashes required; binding/finalize/cold verify this whole prepared inventory'),
  replacement_does_not_remove_original_path_dependency=True,deletion_authorized=False,
  restore_limit='A peer byte copy exists; removing this live original path would break the actual prepared inventory. No retirement or restore mapping is admitted.')
 pairs.append(row)
# Complete root sizes are allocation observations, not APFS exclusive space.
def root_meta(root):
 files=[metadata(p) for p in root.rglob('*') if p.is_file() and not p.is_symlink()]
 unique={tuple(r['identity'][:2]):r['allocated_bytes'] for r in files}
 return dict(path=str(root),regular_files=len(files),logical_bytes=sum(r['logical_bytes'] for r in files),unique_inode_allocated_bytes=sum(unique.values()))
new_roots=[root_meta(SOURCE),root_meta(OUTPUT),root_meta(TERM)]
for r in new_roots:r.update(status='HOLD',current_declared_resource_root=True,reason='Current admitted SOURCE31/declaration and actual fresh prepared runtime; exact namespace/local file/source/receipt paths still required. Declaration/prepare/input evidence is not replaceable cache.')
case=metadata(SOURCE/'case_spec.json');case.update(status='HOLD',expected_factory_seal_SHA=seal['files']['case_spec.json'],full_SHA_freshly_verified_in_actualDECLARE_proof=True,prior_fresh_identity_still_equal=True,source_declaration=str(SOURCE/'declaration.json'),prepared_reference=prepared['case_spec'],reason='Complete immutable ordinary65/whole7/trim73 plus original math/reference2000 case metadata; full SOURCE factory seal and prepared.case_spec require original file.',deletion_authorized=False)
# Cache universe is Root's independent fresh metadata scan, crosschecked by our
# lstat and the sealed R12/R15 exact159 set. No new copy of the large path list.
oldinventory=read(R15/'spot_fifteenth_storage_metadata_inventory_20261009.json')
held={str(ROOT/row['path']) for row in oldinventory['cache_like']}
current={row['path'] for row in fresh['cache_like']};assert len(held)==len(current)==159 and held==current
caches=[metadata(p) for p in sorted(current)]
for r in fresh['cache_like']:assert metadata(r['path'])['identity']==r['identity']
cache_allocated=sum({tuple(r['identity'][:2]):r['allocated_bytes'] for r in caches}.values());cache_logical=sum(r['logical_bytes'] for r in caches)
cache_set_sha=hashlib.sha256(('\n'.join(sorted(current))+'\n').encode()).hexdigest()
assert cache_set_sha==old['cache_set_check']['sorted_absolute_path_set_sha256']
assert cache_logical==4254785 and cache_allocated==4534272
base=read('/private/tmp/spot_storage_twelfth_current_v9_graph_protection_boundary_20261009/cache_223_current_closure_intersection.json','8189a99f7a5bb111a883d3953470f40618c3874100938ec4b73d551a206312c8')
boundary=read(ROOT/'validation/storage_cleanup_twelfth_20261009/current_protection_review/cache_64_current_canonical_source_boundary.json','38e419a8c62e2790cccf67fbf04a64bc46d9d6e1b1b9a2e30e5a79353c381d23')
resource_cache={r['path'] for r in base['resource_root_hits']};source_cache={r['path'] for r in boundary['extra_current_canonical_source_cache_HOLD']}
assert resource_cache|source_cache==current and len(resource_cache)==157 and len(source_cache)==2
assert all(any(Path(path).is_relative_to(Path(root)) for root in rootset) for path in resource_cache)
# Large older items are metadata-screened and retained, not given speculative
# new consumer-clearance just because V9 DECLARE or PREP exists.
old_big={r['path']:r for r in old['top50_actual_large_files_metadata_and_protection_intersections']};large=[]
for row in fresh['large_files']:
 p=row['path'];r=metadata(p);assert r['identity']==row['identity']
 r.update(status='HOLD',current_compact_metadata_exact_file_dependency=p in m['files'],expected_current_SHA_not_new_payload_hash=m['files'].get(p),prior_R15_protection_reason=old_big.get(p,{}).get('reason'),new_safe_exact_replacement_and_current_reader_exclusion_proved=False,deletion_authorized=False)
 if p in old_big:assert r['identity']==old_big[p]['identity']
 r['reason']='Current file/namespace/resource or original scientific/recovery main payload; no new complete reader exclusion and exact restore proof. Existing R15 protection is retained.'
 large.append(r)
# All new OUTPUT copies and old restoration master remain. Previously retired
# runtime5 are derived from exact frozen manifest, not guessed by version.
r14=read(ROOT/'validation/storage_cleanup_fourteenth_20261009/runtime_retirement_manifest.json','00b3ff33f045f825137763dca4dbaffa61d013c92e0e3c5e946d4e72eb1f1096')
# Record its complete pinned identity as recovery obligation; no manager runs.
controller=pin(SOURCE/'production_runner.py',seal['files']['production_runner.py'])
text=(SOURCE/'production_runner.py').read_text()
assert 'for name, digest in data["local_files"].items():' in text and 'require_file(prepared.parent / target, digest)' in text
assert 'runtime/conditional_white_receiver_variant.json' in text
for p,r in PINS.items():assert identity(p)==r['identity']
for r in list(source_metas.values())+list(output_metas.values())+caches+large:assert identity(r['path'])==r['identity']
new_logical=sum(r['logical_bytes'] for r in new_roots);new_allocated=sum(r['unique_inode_allocated_bytes'] for r in new_roots)
result=dict(schema='SPOT_SIXTEENTH_INCREMENTAL_CURRENT_GRAPH_COLD_RUNTIME_STORAGE_READONLY_REVIEW_V1',status='PASS',conclusion='新增安全删除候选0。新cold SOURCE/OUTPUT当前有准确路径和全清单依赖；159缓存仍为原HOLD集，大科学主本与永久恢复来源未解除。',
 approved_deletion_candidates=[],approved_logical_bytes=0,approved_allocated_bytes=0,new_current_roots=new_roots,current_copy_candidates_all_HOLD=pairs,current_complete_case_metadata_HOLD=case,
 SOURCE31_identity_and_expected_sealed_SHA_reuses_recent_actual_full_freshproof=True,OUTPUT44_inventory_exact43_localfiles_plus_prepared=True,
 cache_set=dict(count=159,new_paths=0,missing_held_paths=0,exact_R15_R12_HOLD_set_equal=True,sorted_absolute_path_set_sha256=cache_set_sha,logical_bytes=cache_logical,unique_inode_allocated_bytes=cache_allocated,resource_HOLD157_current_roots_preserved=True,source_HOLD2_rule_preserved=True,cache_content_not_rehashed=True),
 older_large_file_metadata60=large,dominant_R15_retention_categories=old['major_protected_categories'],compiled_direct_consumer_HOLD_unchanged=old['direct_compiled_consumers'],
 current_graph_scope=dict(canonical35647_retained_recent_fullproof_identity_equal=True,requirements235528_namespaces86_aliases186_absence445_recent_fullproof_bound=True,original_declared_roots231_retained_under_current_roots236=True),
 fresh_Root_inventory=PINS['/private/tmp/spot_storage_sixteenth_root_readonly_20261009/before.json'],recent_actual_fullgraph_readonly_proof=PINS['/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json'],
 R15_project_du_KiB=oldclose['after']['project_du_KiB'],current_project_du_KiB=fresh['project_du_KiB'],whole_project_observed_du_increase_KiB=fresh['project_du_KiB']-oldclose['after']['project_du_KiB'],current_SOURCE_OUTPUT_TERM_logical_bytes=new_logical,current_SOURCE_OUTPUT_TERM_unique_inode_allocated_bytes=new_allocated,
 all_original_result_documents_logs_failed_facts_source_seals_restore_masters_preserved=True,
 scientific_data_35GB_or_main_arrays_rehashed=False,new_business_or_PREP_RUN_API_cold_native_executed=False,whole_project_new_metadata_baseline_written=False,project_formal_ART_written=False,files_deleted=0,reclaimed_bytes=0,
 native_RSS_or_AAA_ABA_credit=False,pins=PINS,limits=['Root fresh metadata overview + independent lstat and narrowly selected live duplicate pair SHA; no whole scientific byte reread.','No R15 old HOLD automatically released by V9 successes. Exact bytes alone do not remove current original-path dependencies.','Cold OUTPUT observed PREPARED_NO_TRANSPORT and kept; this storage review does not admit actual PREP or fill any future phase receipt.','Allocated observations and whole-project du delta are not exclusive APFS freed-space measurements.'])
(D/'REPORT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
(D/'REPORT.txt').write_text('第十六轮增量只读复查：新增可安全删除项0，删除0。\n新冷启动SOURCE/OUTPUT约79MiB均是当前声明、准备和后续准确路径校验输入；程序/两大元数据/声明副本虽与主本完全同字节，仍受prepared.local_files和SOURCE完整清单约束。\n159缓存与R12/R15保留集完全相同；无新增普通无依赖缓存。旧大科学主数据、恢复主本与结果文档继续保留。\n只复用最近实际完整图证明和元数据/路径身份，未重读35GB、运行科学业务或写项目。\n')
print(json.dumps(dict(status='PASS',safe_new_candidates=0,cache_count=159,new_SOURCE_OUTPUT_TERM_allocated_bytes=new_allocated,whole_project_du_increase_KiB=result['whole_project_observed_du_increase_KiB'],report_sha256=hashlib.sha256((D/'REPORT.json').read_bytes()).hexdigest())))
