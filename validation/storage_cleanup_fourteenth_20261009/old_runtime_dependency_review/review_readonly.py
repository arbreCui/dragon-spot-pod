import ast, hashlib, json, math, os, stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts'
O=Path('/private/tmp/spot_storage_fourteenth_old_runtime_exact_dependency_review_20261009')
T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
PINS={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]) and p.parent.resolve(strict=True)==p.parent
 h=hashlib.sha256()
 with p.open('rb') as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
  while block:=f.read(4*1024**2):h.update(block)
 assert identity(p)==before
 r=dict(path=str(p),sha256=h.hexdigest(),size_bytes=before[3],allocated_bytes=p.lstat().st_blocks*512,identity=before)
 if expected:assert r['sha256']==expected,(str(p),r['sha256'])
 PINS[str(p)]=r;return r
def pairs(rows):
 d={}
 for k,v in rows:
  assert k not in d;d[k]=v
 return d
def floating(x):
 x=float(x);assert math.isfinite(x);return x
def reject(x):raise ValueError(x)
def obj(p,expected=None):
 r=pin(p,expected);x=json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_float=floating,parse_constant=reject);assert identity(p)==r['identity'];return x
def strings(x):
 out=set();stack=[x]
 while stack:
  y=stack.pop()
  if type(y)is str:out.add(y)
  elif type(y)is dict:stack.extend(y);stack.extend(y.values())
  elif type(y)is list:stack.extend(y)
 return out
def under(p,roots):return sorted(r for r in roots if p==r or p.startswith(r+'/'))
config=obj(T/'config.json');OUT=Path(config['OUT']);SOURCE=Path(config['SOURCE']);TERM=Path(config['TERM']);F=Path(config['F'])
pin(F,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46')
d=obj(OUT/'declaration.json','7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0')
g=obj(OUT/'input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
seal=obj(OUT/'seal.json','ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed')
canonical={x['path'] for x in g['canonical_files']};nsroots={x[k]for x in g['namespaces']for k in ('root','canonical_root')}
aliases={x[k]for x in g['aliases']for k in ('path','target')};aliasdirs={x[k]for x in g['aliases']if x['kind']=='directory'for k in ('path','target')}
assert len(canonical)==35647 and len(g['namespaces'])==86 and len(g['aliases'])==186 and len(g['absence_inputs'])==445 and len(g['live_resource_roots'])==231
idx=obj(Path('/private/tmp/spot_storage_second_dependency_20261008/protection_index.json'))
m9=obj(V/'storage_cleanup_ninth_20261009/manifest.json','e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8')
cold=set(m9['current_cold_extra_protected_files']);assert len(cold)==6248
spec=obj(V/'axial_material/combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
hist=obj(ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
failed=obj(V/'axial_material/historical_input_combined_unowned_specs_failed_prep_namespace_20261007.json','cd2c8c2ea75011ed433a441a4126cfda86c87068429c6f176d918524977137be')
trim=obj(ART/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008/declaration.json','e6dd804a473ae25888ecf5e070af708a024618772c0f753d836127af6074dc00')
INTAKE=ART/'axial-material-owned-specs-trim-v9-standalone-bounded-runtime-api-intake-evidence-20261009'
actual=obj(INTAKE/'intake/admit.log','0e5727aee267c24c3a74c387c628b3633a23826e38c41eda1bfe14ecd02872f5')
rootinput=obj(INTAKE/'Root_terminal_return.json','23acbccb31befbba6ae52ffaf80ae119fd3b7341faa263c18a45c0cd239062ba')
assert type(rootinput['actual_exit_code'])is int and rootinput['actual_exit_code']==0
assert rootinput['actual_tool']==dict(initial_chunk_id='0a5d42',session_id=11005,terminal_chunk_id='cbbfbe',exit_code=0)
assert len(actual)==65 and len(actual['descriptor_files'])==35675
ownscope=obj(Path('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009/complete_graph_and_whole_returned_INPUT_review.json'),'defdf82d849912f795fae8a8fea856bb20c475771cdb41d67a11ffe2a49f78f8')
assert ownscope['status']=='PASS'
primary=pin(OUT/'runtime/Dragon','77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba')
assert seal['files']['runtime/Dragon']==primary['sha256'] and primary['size_bytes']==9225720 and primary['identity'][6]==1
candidates=[]
for version in range(2,7):
 family=ART/f'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v{version}-20261008'
 r=pin(family/'runtime/Dragon',primary['sha256']);assert r['size_bytes']==primary['size_bytes'] and r['identity'][:2]!=primary['identity'][:2] and r['identity'][6]==1
 candidates.append(dict(version=version,family=str(family),**r))
targets={x['path']for x in candidates}
assert len({tuple(x['identity'][:2])for x in candidates})==5
all_current_literals=set().union(*(strings(x)for x in (g,d,spec,hist,failed,trim,actual,rootinput)))
for p in targets:
 assert p not in canonical and p not in all_current_literals and not under(p,nsroots|aliasdirs) and p not in aliases
 assert p not in idx['canonical_protected_files'] and not under(p,idx['exhaustive_dir_paths']) and p not in cold
 assert p not in actual['descriptor_files']
retained=set();restore_sources=set();prior=[];historic_audit_mentions=[]
for folder in sorted(V.glob('storage_cleanup*')):
 for report in folder.glob('*REPORT*.txt'):pin(report)
 for manifest in sorted(folder.glob('*manifest*.json')):
  if manifest.name not in ('manifest.json','retire_manifest.json','cleanup_manifest.json','cache_manifest.json','cleanup_plan_manifest.json','retirement_manifest.json','approved_manifest.json'):continue
  data=obj(manifest);prior.append(PINS[str(manifest)])
  for key,value in data.items():
   if key in ('retained_primaries','retained_primaries_and_critical_sources','retained_tapes','final_merge_retained','retained_closed_anchors'):
    retained.update(s for s in strings(value)if s.startswith(str(ROOT)+'/'))
  for row in data.get('candidates',[]):
   for key in ('retained_primary','retained_primary_pin','compressed_backup','restoration','restore_byte_exact_mapping'):
    restore_sources.update(s for s in strings(row.get(key))if s.startswith(str(ROOT)+'/'))
  hits=sorted(targets & strings(data))
  if hits:historic_audit_mentions.append(dict(manifest=PINS[str(manifest)],paths=hits,role='Historical audit snapshot/control pin, not a current INPUT read or a restore-primary claim; original manifest is retained unchanged.'))
for p in targets:
 assert p not in retained|restore_sources and not under(p,retained|restore_sources)
restore_utilities=[]
for folder in V.glob('storage_cleanup*'):
 for p in folder.glob('*restore*.py'):
  r=pin(p);text=p.read_text();assert not any(target in text for target in targets);restore_utilities.append(r)
inv=Path('/private/tmp/spot_storage_recheck_20261009_root13/full_metadata_inventory.jsonl');pin(inv)
link_rows=[]
for line in inv.open():
 row=json.loads(line)
 if row['type']!='symlink':continue
 p=ROOT/row['path'];before=identity(p);resolved=str(p.resolve(strict=False));text=os.readlink(p)
 assert not any(target==resolved or (Path(resolved).is_dir()and target.startswith(resolved+'/'))for target in targets)
 assert identity(p)==before;link_rows.append(dict(path=str(p),identity=before,target=resolved,text=text))
assert len(link_rows)==687
# Re-read full source and every exact function/class from both sealed R13
# proofs. Their definitions are unchanged; candidate-specific input exclusions
# above cover the five old paths instead of relying on filename/date similarity.
proofbase=V/'storage_cleanup_thirteenth_20261009/candidate_current_dependency_review'
proof=obj(proofbase/'current_actual_source_readchain_proof.json','26f7536790457d71715093b70fad3ae6089619ef49cefb797265d991e2b6609b')
tail=obj(proofbase/'tail_and_R9_allocation_supplement.json','284b7e3689ab96d48c9aa647fe11635ee8e80563468ac5c5a70d98a8828c70be')
clauses=[];sourcecache={}
for old in proof['all_current_pipeline_clauses']+tail['source_clauses']:
 p=Path(old['source']['path']);pin(p,old['source']['sha256'])
 if str(p)not in sourcecache:
  text=p.read_text();sourcecache[str(p)]=(text,ast.parse(text))
 text,tree=sourcecache[str(p)];nodes=[x for x in ast.walk(tree)if isinstance(x,(ast.FunctionDef,ast.ClassDef))and x.name==old['definition']];assert len(nodes)==1
 definition=ast.get_source_segment(text,nodes[0]);sha=hashlib.sha256(definition.encode()).hexdigest();assert definition==old['exact_definition'] and sha==old['whole_definition_sha256']
 clauses.append(dict(source=PINS[str(p)],definition=old['definition'],start_line=nodes[0].lineno,end_line=nodes[0].end_lineno,whole_definition_sha256=sha,exact_definition=definition))
assert len(clauses)==37
new_INPUT_cold_clauses=[]
COLDD=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-input-v5-draft-20261009')
for p,sha,names in (
 (COLDD/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py','040f3ec2b201eeeba850c5dff72d66604784d99d97bf9f2c6c991e9ceb48d588',('intake_witness','body_header','current_cold_binding','current_checks','complete_input_phase','consume_completed_inputs','expected_union')),
 (COLDD/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py','76ac45bd9fc22d7a23abea6f46f182207fbea4f34d6be421cd68afbe6fc71a9e',('component_intake','component_current_context','completed_components','complete_history_resources','fresh_storage_admission'))):
 pin(p,sha);text=p.read_text();tree=ast.parse(text)
 for name in names:
  node=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name==name);definition=ast.get_source_segment(text,node)
  new_INPUT_cold_clauses.append(dict(source=PINS[str(p)],definition=name,start_line=node.lineno,end_line=node.end_lineno,exact_definition=definition,whole_definition_sha256=hashlib.sha256(definition.encode()).hexdigest()))
sourcepeer=obj(Path('/private/tmp/spot_v9_actual_bound_INPUT_source_witness_math_independent_review_20261009/REPORT.json'),'c19a572f913f06339e6d8fdb16d143f15eab3b2aa2ae5268e77335b7562a4147');assert sourcepeer['status']=='PASS'
old_raw_proofs=[];retained_documents=[]
for row in candidates:
 version=row['version'];family=Path(row['family']);driver=obj(family/'driver_result.json');st=obj(family/f'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V{version}/stages.json')['stages']
 assert driver['classification']=='FAILED_COMBINED_RUNTIME_LINK_NO_RETRY' and driver['error']is not None
 assert st
 links=[stage for stage in st if stage['label']=='build/link'];assert len(links)==1 and links[0]['status']in ('PASS','FAILED')
 assert links[0]['command'][-1]==row['path']
 assert not os.path.lexists(family/'seal.json') and not os.path.lexists(family/'audit/result.json')
 original_matches=[]
 def find_original(x,pointer=''):
  if type(x)is dict:
   if x.get('path')==row['path']and x.get('sha256')==row['sha256']:original_matches.append(pointer)
   if x.get(row['path'])==row['sha256']:original_matches.append(pointer+'/'+row['path'])
   for k,v in x.items():find_original(v,pointer+'/'+str(k))
  elif type(x)is list:
   for i,v in enumerate(x):find_original(v,pointer+'/'+str(i))
 find_original(m9);assert original_matches
 immutable=[]
 for p in sorted(family.rglob('*')):
  if p.is_file() and str(p)!=row['path']:
   immutable.append(dict(path=str(p),identity=identity(p),role='Preserved original failed build result/source/metadata/raw/watch; not selected for deletion.'))
 td=ART/f'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v{version}-20261008'
 terminal_paths=[dict(path=str(p),identity=identity(p))for p in sorted(td.rglob('*'))if p.is_file()]
 doc=V/'axial_material'/f'last_cprime_trim_combined_live_resource_v{version}_build_review_20261008'
 documents=[dict(path=str(p),identity=identity(p))for p in sorted(doc.rglob('*'))if p.is_file()]
 for p in (family/'execution_claim.json',family/'build/link.watchdog.json',family/'raw_metadata_receipt.json'):pin(p)
 old_raw_proofs.append(dict(version=version,failed_driver=PINS[str(family/'driver_result.json')],stage_records=PINS[str(family/f'HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_V{version}/stages.json')],stage_statuses=[s['status']for s in st],original_link_output_path=row['path'],old_seal_absent=True,old_audit_result_absent=True,prior_R9_original_full_sha_manifest=PINS[str(V/'storage_cleanup_ninth_20261009/manifest.json')],original_full_sha_locations=original_matches,all_original_nonselected_family_files=immutable,all_original_terminals_retained=terminal_paths,all_original_review_documents_retained=documents))
 row['category']='EXACT_DUPLICATE_OLD_FAILED_BUILD_RUNTIME_COPY'
 row['retained_primary']=primary
 row['restore_byte_exact_mapping']=dict(target=row['path'],source=primary['path'],expected_sha256=row['sha256'],expected_size=row['size_bytes'],restore_mode=stat.S_IMODE(row['identity'][2]),restore_mtime_ns=row['identity'][4],overwriting_forbidden=True,original_inode_or_ctime_restorable=False)
 row['original_failure_unchanged']=True
 row['current_dependency_exclusions']=dict(all_canonical=True,all_graph_and_fullnormative_literals=True,exhaustive_namespaces=True,aliases_and_absence=True,actual_complete_35675_INPUT_descriptors=True,cold6248=True,old_index=True,restore_primaries_and_archives=True,all687_inbound_links=True,complete37_current_readchain_definitions_unchanged=True)
metadata_candidates_path=Path('/private/tmp/spot_storage_recheck_20261009/audit_metadata_compression_candidates.json')
metadata=obj(metadata_candidates_path);assert type(metadata)is list and len(metadata)==10
metadata_screen=[]
for row in metadata:
 p=row['path'];assert p.startswith(str(V)+'/storage_cleanup_')
 assert p not in all_current_literals and p not in canonical and not under(p,nsroots|aliasdirs) and p not in aliases and p not in cold
 assert p not in actual['descriptor_files']
 oldindex_direct=p in idx['canonical_protected_files'];oldindex_dirs=under(p,idx['exhaustive_dir_paths']);retained_label_hits=under(p,retained|restore_sources)
 assert not under(p,g['live_resource_roots'])
 metadata_screen.append(dict(path=p,size_bytes=row['size'],allocated_bytes=row['allocated'],current_identity=identity(p)if os.path.lexists(p)else None,original_path_present_at_this_review=os.path.lexists(p),status='HOLD_OLD_PROTECTION_OR_RETAINED_LABEL_REVIEW_REQUIRED'if oldindex_direct or oldindex_dirs or retained_label_hits else'SOURCE_SCIENCE_DEPENDENCY_EXCLUDED_ONLY',oldindex_canonical_protected=oldindex_direct,oldindex_exhaustive_parents=oldindex_dirs,retained_prior_labels=retained_label_hits,current_graph_all_literals_and_actual_INPUT_and_cold_excluded=True,outside_all_current_axial_resource_roots=True,role='Old audit metadata snapshot. Original full bytes/hash must be retained through verified exact archive and explicit restoration recipe; this is source dependency exclusion only, not compression/deletion approval.'))
for p,r in PINS.items():assert identity(p)==r['identity']
for r in link_rows:assert identity(r['path'])==r['identity'] and os.readlink(r['path'])==r['text']
sourceproof=dict(schema='SPOT_OLD_V2_V6_RUNTIME_CURRENT_WHOLE_INPUT_COMPLETE_SOURCE_EXCLUSION_V1',status='PASS',clauses=clauses,new_actual_INPUT_to_future_cold_complete_definitions=new_INPUT_cold_clauses,selected_targets=sorted(targets),actual_INPUT_pin=PINS[str(INTAKE/'intake/admit.log')],actual_INPUT_Root_pin=PINS[str(INTAKE/'Root_terminal_return.json')],current_35675_actual_INPUT_files_retained=True,all231_declared_roots_retained=True,current_resource_members_are_dynamic_stat_caps_not_old_binary_payload_inventory=True,earlier_RUN51693_file_count_not_a_current_requirement=True,new_actual_INPUT_independent_current51701_files_not_a_future_frozen_requirement=True,cold_intake_witness_only_compares_frozen_host_result_to_frozen_stdout_watch_stage_and_payload=True,cold_fresh_resource_gate_rederives_same_declared_roots_dynamic_union_policy_class_and_96_free8_original_reserve=True,cold_future_source_only_UNREADY_no_new_binding_or_execution=True,full_normative_input_predicates_unchanged=True,prior_restore_manifests=prior,prior_restore_sources=restore_utilities,inbound_link_count=len(link_rows),historical_audit_only_mentions=historic_audit_mentions)
report=dict(schema='SPOT_FOURTEENTH_OLD_V2_V6_EXACT_RUNTIME_SOURCE_DEPENDENCY_READONLY_REVIEW_V1',status='PASS',scope='FIVE_FIXED_OLD_FAILED_RUNTIME_DUPLICATES_ONLY_NOT_DELETE',candidates=candidates,retained_primary=primary,selected_count=5,logical_bytes=sum(x['size_bytes']for x in candidates),allocated_bytes=sum(x['allocated_bytes']for x in candidates),unique_inode_allocated_bytes=sum(x['allocated_bytes']for x in candidates),current_complete_input_graph_pin=PINS[str(OUT/'input_graph.json')],current_full35GB_proof_retained_not_repeated=PINS[str(Path('/private/tmp/axmat_v9_actual_bounded_INPUT_graph_descriptor_independent_review_20261009/complete_graph_and_whole_returned_INPUT_review.json'))],original_failed_build_results_and_documents=old_raw_proofs,metadata10_science_dependency_exclusion_only=metadata_screen,prior_R13_actual_retirement_remains_only_V7_V8=True,no_old_seal_or_result_or_failure_fact_rewritten=True,bootstrap51_HOLD_remains=True,original_unique_scientific_material_snapshots_native_full_and_all_restore_masters_kept=True,science_business_API_import_or_constructor_or_PREP_or_RUN_or_native_child_executed=False,formal_or_ART_writes=False,files_deleted=0,all_full_fresh_control_and_metadata_pins=list(PINS.values()),read_only_tool_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),recommendation='Root may prepare exact5 manifest with byteexact restore mappings to sealed V9 runtime. Independent source/manifest/fresh preflight must pass before deletion. Keep all old docs/logs/graphs/trace/driver/SOURCE/TERM and all resource root directories. Replaying old package/commands must first restore exact retired paths and applicable previous rounds; inode/ctime not recoverable. Ten audit JSONs have only current science dependency exclusion here; whole exact archive/restore proof separately required.')
for name,value in [('exact5_runtime_candidates.json',dict(status='PASS',candidates=candidates,retained_primary=primary,logical_bytes=report['logical_bytes'],allocated_bytes=report['allocated_bytes'])),('current_actual_source_readchain_proof.json',sourceproof),('metadata10_current_science_dependency_exclusion.json',dict(status='PASS_SOURCE_DEPENDENCY_EXCLUSION_ONLY',rows=metadata_screen)),('REPORT.json',report)]:
 with (O/name).open('x')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
(O/'REPORT.txt').write_text('只读候选审查PASS：V2–V6五份旧失败OUT/runtime/Dragon均与保留的V9 sealed runtime全文SHA77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba一致。逻辑46,128,600B，分配46,141,440B（44.004MiB）。全五源为不同singlelink inode，原R9全文SHA记录也吻合。完整当前35647 graph、35675实际INPUT descriptor、86命名空间/186别名/445缺席、原2cad/aa3e/trim/failedPREP、旧index、cold6248、恢复主本与687链接排除；37个完整原调用定义重新鲜读同SHA，含production/declaration/PREP/externalterminal/actualcomponents/current/ordinary/trim/provider/resource/futurecold。当前资源按原目录全集与caps动态计量，不要求旧失败程序继续存在或旧RUN文件数不变。保留全部原失败driver/stage/raw/watch/graph/trace/SOURCE/TERM/文档及所有根；旧重放先恢复精确路径，inode/ctime不可恢复。bootstrap51和唯一科学数据保持HOLD。另10份旧审查metadata仅确认无当前科学读取/资源/恢复主本依赖，压缩或退役仍须另行完整原字节归档与解压SHA/恢复证明。本工具仅TMP写，不删除、不执行业务/API/cold/native，不重读35GB。\n')
print(json.dumps(dict(status='PASS',count=5,logical_bytes=report['logical_bytes'],allocated_bytes=report['allocated_bytes'],primary_sha256=primary['sha256'],metadata10_dependency_only=True,report=str(O/'REPORT.json'),report_sha256=hashlib.sha256((O/'REPORT.json').read_bytes()).hexdigest())))
