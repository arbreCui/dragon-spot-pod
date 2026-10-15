import ast, hashlib, json, os, stat, time
from pathlib import Path

ROOT=Path('/Users/wen/spot');D=Path('/private/tmp/spot_storage_review_seventeenth_graph_20261009');PINS={};START=time.monotonic()
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def metadata(p):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and p.resolve(strict=True)==p
 return dict(path=str(p),logical_bytes=s.st_size,allocated_bytes=s.st_blocks*512,identity=identity(p))
def pin(p,sha=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and p.resolve(strict=True)==p
 h=hashlib.sha256()
 with p.open('rb')as f:
  while block:=f.read(4*2**20):h.update(block)
 assert identity(p)==before
 r=dict(path=str(p),sha256=h.hexdigest(),logical_bytes=before[3],identity=before)
 assert sha is None or r['sha256']==sha,p
 PINS[str(p)]=r;return r
def read(p,sha=None):
 r=pin(p,sha)
 def pairs(rows):
  d={}
  for k,v in rows:assert k not in d;d[k]=v
  return d
 d=json.loads(Path(p).read_text(),object_pairs_hook=pairs);assert identity(p)==r['identity'];return d
def digest(d):
 h=hashlib.sha256()
 for block in json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).iterencode(d):h.update(block.encode())
 return h.hexdigest()
def root_meta(root):
 files=[metadata(p)for p in root.rglob('*')if p.is_file()and not p.is_symlink()]
 return dict(path=str(root),regular_files=len(files),logical_bytes=sum(r['logical_bytes']for r in files),unique_inode_allocated_bytes=sum({tuple(r['identity'][:2]):r['allocated_bytes']for r in files}.values()),status='HOLD')

fresh=read('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json','45cc1ac8b5cc943811a6a8ee3f2e0ad3c17bb7568e29837bf80ec626115e8e76')
freshreceipt=read('/private/tmp/spot_storage_seventeenth_root_readonly_20261009/actual_baseline_tool_return.json')
assert freshreceipt['actual_tool_result']==dict(initial_chunk_id='7fef04',session_id=None,terminal_chunk_id='7fef04',exit_code=0,closed=True)
assert freshreceipt['baseline_sha256']==PINS['/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json']['sha256']
assert fresh['counts']==dict(regular=174519,symlink=687,directory_paths=7031)
old=read('/private/tmp/spot_storage_sixteenth_graph_readonly_20261009/REPORT.json','ebd5ada6401e63e584cc07b4d801e3e011f3b1407fe0ba3b8785f19244771294')
oldreceipt=read('/private/tmp/spot_storage_sixteenth_graph_readonly_20261009/actual_readonly_tool_return.json','8c8b48edc96a6386b765c877fc3f4233a291e2d3786af66bedde0388f9bbe34d')
assert old['status']=='PASS' and old['approved_deletion_candidates']==[] and oldreceipt['actual_tool_result']['exit_code']==0
r16close=read(ROOT/'validation/storage_review_sixteenth_20261009/Root_actual_preservation_closeout.json','a171403217b5ccb41f23219f6489dc1121c8f310d3b4f4270777c42ec015e2a5')
R15=ROOT/'validation/storage_review_fifteenth_20261009'
old15=read(R15/'large_inputs_and_cache/REPORT.json','001e4095acac86552450194e333f5f0541d6fda6513210cd41db26516ae275e2')
for p,sha in fresh['document_sha256'].items():pin(ROOT/p,sha)
plan=read('/private/tmp/axmat_v9_cold_actual_DECLARE_readonly_scope_plan_20261009/PLAN.json','59781ef14365a7b17d37d3992eeaf7bc7fd1967c249ad7a381e103e12a41ce52')
SOURCE=Path(plan['source_root']);OUTPUT=Path(plan['future_output_root']);TERM=Path(plan['declaration_terminal_root']);CONTROL=Path(plan['future_control_terminal_root'])
G=Path('/private/tmp/axmat_v9_actual_cold_binding_graph_resource_independent_review_20261009')
proof=read(G/'REPORT.json','03ebde650f63e045ae7a35f1018e02f787aac47fef28812a9a7a7fd719760e3c')
proofreceipt=read(G/'actual_readonly_tool_return.json','34075c6b3c6f0e4197ab6e5ea93bd16b615ca25a3b38f6b57af87b6d8edaa1dd')
joint=read(G/'joint_scope_binding.json','f6d7fe1efff715350daa344d74ce40f1416089270d09347f0f1dca54e151fe91')
jointreceipt=read(G/'actual_joint_readonly_tool_return.json','38bfc4346fd806b05124998ec01ff5aea1832dbdff7374d0128e74a11b0db5f5')
assert proof['status']==joint['status']=='PASS' and proofreceipt['actual_tool_result']==dict(initial_chunk_id='9a9803',session_id=71255,terminal_chunk_id='c050ac',exit_code=0,closed=True)
assert jointreceipt['actual_tool_result']==dict(chunk_id='208936',exit_code=0,closed=True)
assert joint['whole_scope_complementary_reports_pass'] is True and joint['scientific_qualification'] is False
for key in ('source_report','source_actual_reader_receipt'):pin(joint[key]['path'],joint[key]['sha256'])
for key in ('Root_observer','actual_binding_receipt','prior_full_PREP_admission'):pin(proof[key]['path'],proof[key]['sha256'])
for key in ('formal_factory','formal_consumer','formal_intake_binding'):pin(plan[key]['path'],plan[key]['sha256'])
for p,row in proof['full_read_pins'].items():assert identity(p)==row['identity'],p
seal=read(SOURCE/'factory_seal.json','810f8b897d31d48128eda6a5349e3ff55c2d47c71695dab51db0055e4551d5ce')
prepared=read(OUTPUT/'prepared.json','35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
m=read(SOURCE/'rank1_factor_cache_admission.json',seal['files']['rank1_factor_cache_admission.json'])
assert len(m['files'])==37339 and len(prepared['local_files'])==43
expected=dict(m['files']);expected.update(proof['additional_expected_files'])
assert len(expected)==37395 and digest(expected)==proof['expected_files_whole_sha256']
assert prepared['classification']=='PREPARED_NO_TRANSPORT' and 'own_child_supervision'not in prepared
assert sorted(p.name for p in SOURCE.iterdir())==plan['expected_SOURCE_files']
output_meta={str(p):metadata(p)for p in OUTPUT.rglob('*')if p.is_file()and not p.is_symlink()}
assert set(output_meta)=={str(OUTPUT/name)for name in prepared['local_files']}|{str(OUTPUT/'prepared.json'),str(OUTPUT/'own_rss_binding.json')}
assert len(output_meta)==45
term_names=sorted(p.name for p in TERM.iterdir());assert term_names==sorted([phase+suffix for phase in ('declaration','prepare','binding')for suffix in ('.stdout','.stderr','_terminal_return.json')])
assert not os.path.lexists(CONTROL)
for name in ('prepared_cold.json','binding_controls','AAA','ABA','training','archives','cold_closeout_seal.json'):assert not os.path.lexists(OUTPUT/name)

# Metadata index is read once without rehashing/validating the graph64MB or
# the canonical35GB again. The complete semantics were just independently
# audited and the whole graph endpoint's seven fields remain identical.
graphpin=proof['graph_full_json_pin'];assert identity(graphpin['path'])==graphpin['identity']
graph=json.loads(Path(graphpin['path']).read_text())
assert identity(graphpin['path'])==graphpin['identity']
canonical={r['path']:r['sha256']for r in graph['canonical_files']}
canonbefore={p:identity(p)for p in canonical}
assert len(canonical)==35647 and digest(canonbefore)==proof['complete_canonical_before_after_seven_field_identity_digest']
oldfull=read('/private/tmp/axmat_v9_actual_cold_DECLARE_graph_INPUT_resource_independent_review_20261009/REPORT.json','31f29c1b5642ad86d980623363a29cb15f19c2f7094bb95a4fa6393e2651f8d0')
deps={}
for p,wanted in m['files'].items():
 prior=canonbefore[p]if p in canonical else oldfull['reviewed_pins'][p]['identity']
 assert wanted==(canonical[p]if p in canonical else oldfull['reviewed_pins'][p]['sha256']) and identity(p)==prior
 deps[p]=prior
assert digest(deps)==proof['metadata_before_after_identity_digest']
roots=set(prepared['resource_roots']);assert len(roots)==236 and roots==set(m['component_resource_roots'])
assert set(graph['live_resource_roots']).issubset(roots)and len(graph['live_resource_roots'])==231
assert roots=={str(p)for p in (ROOT/'validation/artifacts').glob('axial-material-*')}|roots
for p in (SOURCE,OUTPUT,TERM,CONTROL):assert str(p)in roots

# The new binding is a unique actual result with exact descriptor consumers.
# Future function names/calls below are source evidence, not executed tests.
factory=Path(plan['formal_factory']['path']);ftext=factory.read_text();ftree=ast.parse(ftext)
source_calls={}
for name in ('prepare_binding_in_clean_process','run_controls','final_cold_info','finalize_cold_in_clean_process'):
 fn=next(n for n in ftree.body if isinstance(n,ast.FunctionDef)and n.name==name)
 s=ast.get_source_segment(ftext,fn);source_calls[name]=dict(path=str(factory),first_line=fn.lineno,whole_definition_sha256=hashlib.sha256(s.encode()).hexdigest())
assert "binding=read(require(OUTPUT/'own_rss_binding.json',nonzero_sha(binding_sha)))"in ftext
assert "binding=dict(path=str(OUTPUT/'own_rss_binding.json'),sha256=nonzero_sha(binding_sha))"in ftext
host=ROOT/'validation/axial_material/combined_cold_own_rss_host_physical_basis_own_pid_peak_20261008.py'
pin(host,'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7')
htext=host.read_text();assert "path != work / 'own_rss_binding.json'"in htext
newbinding=metadata(OUTPUT/'own_rss_binding.json');assert newbinding['identity']==proof['actual_binding']['identity']
newbinding.update(status='HOLD',expected_SHA=proof['actual_binding']['sha256'],full_byte_SHA_inherited_from_true_current_binding_review=True,new_full_byte_rehash=False,current_root_receipt=str(TERM/'binding_terminal_return.json'),source_exact_descriptor_consumers=source_calls,expected_self_file_entry_absent=str(OUTPUT/'own_rss_binding.json')not in expected,reason='实际绑定产物；当前Root收据与后续run_controls/finalize/bind_controller都要求该准确路径及全SHA。没有获准替代或恢复映射。',deletion_authorized=False)
roots_meta=[root_meta(p)for p in (SOURCE,OUTPUT,TERM)]
for row in roots_meta:row.update(current_declared_resource_root=True,reason='当前SOURCE完整31文件、prepared完整43本地文件+prepared+新binding、DECL/PREP/BINDING三组原始流和收据。准确路径和身份仍受消费链约束，全部保留。')
pairs=[]
for prior in old['current_copy_candidates_all_HOLD']:
 cp=metadata(prior['path']);pp=prior['retained_primary'];assert cp['identity']==prior['identity']and identity(pp['path'])==pp['identity']
 want=prepared['local_files'][str(Path(prior['path']).relative_to(OUTPUT))]
 assert expected[prior['path']]==want==prior['full_fresh_SHA']==pp['sha256']
 # Narrow small duplicate rehash only; no main scientific array reread.
 pin(prior['path'],want);pin(pp['path'],want)
 cp.update(status='HOLD',full_fresh_SHA=want,retained_primary=dict(path=pp['path'],sha256=want),current_exact_path_dependency=prior['current_exact_path_dependency'],now_in_complete_binding_expected_files=True,reason='字节相同并不解除prepared.local_files与绑定37395全路径依赖；删除原工作路径会使正常校验缺文件。',deletion_authorized=False)
 pairs.append(cp)

# No copied large cache list: exact159-set hash/count and old preserved rules.
oldinventory=read(R15/'spot_fifteenth_storage_metadata_inventory_20261009.json')
held={str(ROOT/row['path'])for row in oldinventory['cache_like']};current={row['path']for row in fresh['cache_like']}
assert held==current and len(current)==159
cache=[]
for row in fresh['cache_like']:
 r=metadata(row['path']);assert r['identity']==row['identity'];cache.append(r)
cache_sha=hashlib.sha256(('\n'.join(sorted(current))+'\n').encode()).hexdigest();assert cache_sha==old['cache_set']['sorted_absolute_path_set_sha256']
base=read('/private/tmp/spot_storage_twelfth_current_v9_graph_protection_boundary_20261009/cache_223_current_closure_intersection.json','8189a99f7a5bb111a883d3953470f40618c3874100938ec4b73d551a206312c8')
boundary=read(ROOT/'validation/storage_cleanup_twelfth_20261009/current_protection_review/cache_64_current_canonical_source_boundary.json','38e419a8c62e2790cccf67fbf04a64bc46d9d6e1b1b9a2e30e5a79353c381d23')
resource_cache={r['path']for r in base['resource_root_hits']};source_cache={r['path']for r in boundary['extra_current_canonical_source_cache_HOLD']}
assert current==resource_cache|source_cache and len(resource_cache)==157 and len(source_cache)==2
assert all(any(Path(p).is_relative_to(Path(r))for r in roots)for p in resource_cache)
assert sum(r['logical_bytes']for r in cache)==4254785 and sum({tuple(r['identity'][:2]):r['allocated_bytes']for r in cache}.values())==4534272
# Only old large metadata60 aggregate counts/categories are recorded, without
# copying its file list or treating old scientific arrays as disposable cache.
oldbig={r['path']:r for r in old['older_large_file_metadata60']};big=[]
for row in fresh['large_files']:
 r=metadata(row['path']);assert r['identity']==row['identity']
 if row['path']in oldbig:assert r['identity']==oldbig[row['path']]['identity']
 big.append(r)
newbig=set(r['path']for r in big)-set(oldbig)
for category in old['dominant_R15_retention_categories']:
 for path in category['paths']:assert os.path.lexists(path),path
for root in (SOURCE,OUTPUT,TERM):
 for p in root.rglob('*'):
  if p.is_file()and not p.is_symlink():assert identity(p)==proof['full_read_pins'][str(p)]['identity']
assert canonbefore=={p:identity(p)for p in canonical}and deps=={p:identity(p)for p in m['files']}
for p,row in PINS.items():assert identity(p)==row['identity']
for r in cache+big+list(output_meta.values()):assert identity(r['path'])==r['identity']
current_logical=sum(r['logical_bytes']for r in roots_meta);current_allocated=sum(r['unique_inode_allocated_bytes']for r in roots_meta)
delta=fresh['project_du_KiB']-r16close['project_du_KiB_at_after_preservation_observation']
assert delta==61828 and delta/1024==60.37890625
binding_allocated=newbinding['allocated_bytes'];other_allocated=(current_allocated-old['current_SOURCE_OUTPUT_TERM_unique_inode_allocated_bytes'])-binding_allocated
report=dict(schema='SPOT_SEVENTEENTH_INCREMENTAL_CURRENT_BINDING_GRAPH_DEPENDENCY_STORAGE_READONLY_REVIEW_V1',status='PASS',conclusion='新增可安全删除项0；新增空间主要为真实own_rss_binding及审查/收据文档。所有当前科学输入、工作副本、缓存与恢复主本继续保留。',approved_deletion_candidates=[],approved_logical_bytes=0,approved_allocated_bytes=0,
 observed_project_du_KiB=fresh['project_du_KiB'],R16_after_project_du_KiB=r16close['project_du_KiB_at_after_preservation_observation'],observed_increment_KiB=delta,observed_increment_MiB=delta/1024,
 new_binding_exact_path_HOLD=newbinding,current_SOURCE31_OUTPUT45_TERMINAL9_roots_HOLD=roots_meta,current_held_duplicate_pairs=pairs,current_root_logical_bytes=current_logical,current_root_unique_inode_allocated_bytes=current_allocated,new_binding_unique_inode_allocated_bytes=binding_allocated,new_ROOT_receipts_streams_increment_allocated_bytes=other_allocated,
 allocation_accounting='实际分配按inode去重；全项目du窗口还包括审查文档与本地Git，不能把所有增长/物理独占空间精确归因于一个文件。',
 cache_set=dict(count=159,exact_R12_R15_R16_HOLD_set_equal=True,new_paths=0,missing_held_paths=0,path_set_sha256=cache_sha,logical_bytes=4254785,unique_inode_allocated_bytes=4534272,resource_HOLD157_retained=True,derived_current_source_HOLD2_retained=True,cache_contents_not_rehashed=True),
 old_large_metadata=dict(observed_items=len(big),same_prior_R16_items=len(set(r['path']for r in big)&set(oldbig)),new_unreviewed_large_paths_count=len(newbig),safe_release_dependency_proof_obtained=False,reason='仅鲜stat与旧R16保护原因承继；主数值数据、规范引用和恢复来源不能由新binding PASS自动释放。'),major_protected_categories=old['dominant_R15_retention_categories'],compiled_direct_consumers_HOLD=old15['direct_compiled_consumers'],
 fresh_scope=dict(canonical_files35647=True,canonical_fresh_seven_field_identity_digest=digest(canonbefore),metadata_dependency37339_fresh_seven_field_identity_digest=digest(deps),complete_expected_ownerunion37395_proof_fresh_bound=True,all235528_requirements86namespaces186aliases445absences_complete_prior_proof_retained=True,current_declared_roots236_original231_retained=True,new_numerical_payload_bytes_read=0,graph64MB_index_metadata_read_only_not_new_graph_semantics_revalidation=True),
 source_graph_and_joint_independent_binding_reviews_bound=True,independent_binding_review_not_Root_science_or_joint_admission=True,control_terminal_and_controls_prepared_cold_future_outputs_absent=True,new_business_API_constructor_PREP_RUN_native_or_science_executed=False,project_formal_ART_written=False,whole_project_new_metadata_baseline_written=False,files_deleted=0,reclaimed_bytes=0,scientific_qualification=False,
 Root_actual_metadata_baseline_tool=freshreceipt['actual_tool_result'],Root_baseline=PINS['/private/tmp/spot_storage_seventeenth_root_readonly_20261009/before.json'],elapsed_seconds=time.monotonic()-START,evidence_pins=PINS)
with(D/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
lines=['第十七轮存储增量只读复查：新增可安全删除项0，删除0。',f"项目当前观测 {fresh['project_du_KiB']} KiB；较第十六轮收口增加 {delta} KiB（{delta/1024:.8f} MiB）。",f"新增 own_rss_binding.json 为 {newbinding['logical_bytes']:,} 逻辑字节、{binding_allocated:,} 当前分配字节，完整SHA {newbinding['expected_SHA']}。这是实际绑定结果，Root收据和后续准确路径/SHA消费者都需要保留。",f"当前SOURCE31、OUTPUT45和TERM9合计 {current_logical:,} 逻辑字节、{current_allocated:,} 去重inode分配字节；新绑定之外，三根较R16新增的流/收据分配为 {other_allocated:,} 字节。项目窗口还包括审查文档及本地Git，实际读数不代表文件系统独占或可释放空间。",'程序Dragon、两大运行元数据及声明的4份工作副本虽与主本完全同字节，仍被prepared.local_files和37395完整绑定清单逐路径校验，不能删除。精确路径、主本和消费者记录见REPORT.json。','159缓存与R12/R15/R16保留集合完全相同：157受当前资源根保护，2是当前规范源码对应派生缓存；没有新增无依赖缓存。','旧大历史输入、完整原始数值响应、DLIB/材料与快照主本、永久gzip恢复包和保护基线继续保留。复用旧完整证明及鲜元数据身份，没有重新读取35GB科学内容。','本报告是存储复查；绑定的独立审查通过不等于Root科学联合准入，更不代表controls/native/AAA/ABA执行。只在TMP保存证据，项目、原日志、结果文档和历史失败事实均未修改。']
with(D/'REPORT.txt').open('x')as f:f.write('\n'.join(lines)+'\n')
print(json.dumps(dict(status='PASS',safe_candidates=0,cache159_unchanged=True,new_binding_logical_bytes=newbinding['logical_bytes'],new_binding_allocated_bytes=binding_allocated,project_increment_MiB=delta/1024,elapsed_seconds=report['elapsed_seconds']),sort_keys=True),flush=True)
