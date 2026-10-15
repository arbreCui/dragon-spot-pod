import hashlib,json,os,pathlib,stat
ROOT=pathlib.Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts';OUT=pathlib.Path('/private/tmp/spot_storage_eleventh_result_preservation_review_20261009')
def pin(p):
 p=pathlib.Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode)
 with p.open('rb') as f:b=f.read()
 assert s==p.lstat()
 return dict(path=str(p),size=len(b),sha256=hashlib.sha256(b).hexdigest(),identity=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]),b
def j(p):return json.loads(pin(p)[1])
def save(n,v):
 with (OUT/n).open('x') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
exact=j(OUT/'legacy_bootstrap_exact_five_fullpins.json')['rows'];candidates=exact[:3];primaries=exact[3:]
cp={x['path'] for x in candidates}
graphpath=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009/input_graph.json'
graphpin,raw=pin(graphpath);assert graphpin['sha256']=='242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044';graph=json.loads(raw)
def strings(v):
 if isinstance(v,str):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield k;yield from strings(x)
 elif isinstance(v,list):
  for x in v:yield from strings(x)
allpaths={x for x in strings(graph) if x.startswith('/')};canonical={x['path'] for x in graph['canonical_files']}
assert len(canonical)==35647 and len(graph['namespaces'])==86 and len(graph['aliases'])==186 and len(graph['live_resource_roots'])==228
assert not cp&allpaths and not cp&canonical
for ns in graph['namespaces']:
 root=pathlib.Path(ns['canonical_root']);assert all(not pathlib.Path(x).is_relative_to(root) for x in cp)
idxpath=V/'storage_review_more_20261008/normalized_protection_index.json';idxpin,raw=pin(idxpath);idx=json.loads(raw)
assert not cp&set(idx['protected_files']) and not cp&set(idx['inbound_alias_targets'])
assert all(not pathlib.Path(x).is_relative_to(pathlib.Path(d)) for x in cp for d in idx['protected_directories'])
m8path=V/'storage_cleanup_eighth_20261009/manifest.json';m9path=V/'storage_cleanup_ninth_20261009/manifest.json';m8pin,raw=pin(m8path);m8=json.loads(raw);m9pin,raw=pin(m9path);m9=json.loads(raw)
cold=set(m8['current_cold_extra_protected_files']);assert len(cold)==6248 and not cp&cold
critical=m9['critical_roots'];assert all(not pathlib.Path(x).is_relative_to(pathlib.Path(d)) for x in cp for d in critical)
coldpath=V/'axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/next_cold_input_readonly_integrity_review/derived_required_path_SHA_owners.json';coldpin,raw=pin(coldpath);business=json.loads(raw)
assert len(business)==1534 and not cp&{x['path'] for x in business}
remainingpath=pathlib.Path('/private/tmp/spot_storage_tenth_root_audit_20261009/remaining_after_prior_restore_primary_screen.json');remainingpin,raw=pin(remainingpath);remain=json.loads(raw);remainpaths={str(ROOT/x['path']) for x in remain['rows']}
assert cp<=remainpaths
round_names=['storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_third_20261008','storage_cleanup_fourth_20261008','storage_cleanup_fifth_20261009','storage_cleanup_sixth_20261009','storage_cleanup_seventh_20261009','storage_cleanup_eighth_20261009','storage_cleanup_ninth_20261009','storage_cleanup_tenth_20261009']
rounds=[];retired=set();prior_retained=set();coveragepins=[]
for name in round_names:
 p=V/name;resultpin,raw=pin(p/'cleanup_result.json');result=json.loads(raw);reportpin,_=pin(p/'REPORT.txt');ledgerpin,raw=pin(p/'retirement_ledger.jsonl');rows=[json.loads(x) for x in raw.splitlines()]
 count=result.get('deleted_files',result.get('removed_count'));amount=result.get('deleted_allocated_bytes',result.get('removed_allocated_bytes'));assert len(rows)==count
 paths=[]
 for row in rows:
  item=row.get('candidate',row);path=item.get('path',row.get('path'));assert path and path.startswith('/Users/wen/spot/');paths.append(path)
 assert len(set(paths))==count and not retired&set(paths);retired.update(paths)
 # Actual retained-primary/source contracts; old candidate paths never count
 # as restoration sources by virtue of merely being mentioned in reports.
 mf=p/'manifest.json';manifest=None
 if mf.exists():
  mp,b=pin(mf);manifest=json.loads(b);coveragepins.append(mp)
 else:
  pp,b=pin(p/'preflight.json');pf=json.loads(b);coveragepins.append(pp)
  for key in ('retained_fresh_contents','review_documents'):
   prior_retained.update(x for x in strings(pf.get(key,[])) if x.startswith('/Users/wen/spot/'))
 if manifest:
  for key in ('retained_primaries','source_and_review_pins','source_review_pins','retained_files'):
   prior_retained.update(x for x in strings(manifest.get(key,[])) if x.startswith('/Users/wen/spot/'))
  for c in manifest.get('candidates',[]):
   for key in ('retained_primary','duplicate_primary','primary','restoration_source'):
    prior_retained.update(x for x in strings(c.get(key)) if x.startswith('/Users/wen/spot/'))
 assert not cp&set(paths)
 rounds.append(dict(round=name,removed_paths=count,nominal_retired_allocated_bytes=amount,report_pin=reportpin,result_pin=resultpin,ledger_pin=ledgerpin))
assert not cp&prior_retained
assert len(retired)==10018 and all(not os.path.lexists(p) for p in retired)
# Exact preserved old seals/recipes; no old verifier or process is invoked.
sourcepaths=[ART/'d4a-scattering-bootstrap-prepared-20260924'/n for n in ('prepare.py','preparation.json','prepared_inputs.sha256','prepare_seed.log','check_seed.log')]+[ART/'d4a-scattering-bootstrap-run-20260924'/n for n in ('run_once.py','run_status.json','input_manifest.sha256','result.sha256','radial.log','b2i_seal_bootstrap.log')]+[ART/'d4a-corrected-closed0-runtime-release-20260920'/n for n in ('snapshot_build_result.sha256','admitted_snapshot_archive.sha256','d4a_closed0_release.sha256')]+[V/'iterative/test_d4a_picard_map_preflight.py']
sourcepins={str(p):pin(p)[0] for p in sourcepaths}
def table(p):
 return {line.split()[1].lstrip('*'):line.split()[0] for line in pin(p)[1].decode().splitlines() if line.strip()}
prep=table(ART/'d4a-scattering-bootstrap-prepared-20260924/prepared_inputs.sha256');inp=table(ART/'d4a-scattering-bootstrap-run-20260924/input_manifest.sha256');res=table(ART/'d4a-scattering-bootstrap-run-20260924/result.sha256')
assert prep['d4a_snapshots.xsm']==inp['d4a_snapshots.xsm']==res['d4a_snapshots.xsm']==exact[0]['sha256']
assert prep['d4a_seed_snapshots.xsm']==inp['d4a_seed_snapshots.xsm']==res['d4a_seed_snapshots.xsm']==exact[2]['sha256']
release_tables=[table(ART/'d4a-corrected-closed0-runtime-release-20260920'/n) for n in ('snapshot_build_result.sha256','admitted_snapshot_archive.sha256','d4a_closed0_release.sha256')]
assert any(x.get('d4a_snapshots.xsm')==exact[4]['sha256'] for x in release_tables)
assert j(ART/'d4a-scattering-bootstrap-run-20260924/run_status.json')['classification']=='CLOSED0_SEALED_PROJECTABLE_NOT_FIXED_POINT'
assert "'d4a_snapshots.xsm': RELEASE/'d4a_snapshots.xsm'" in pin(ART/'d4a-scattering-bootstrap-prepared-20260924/prepare.py')[1].decode()
assert "source=PREPARED/name" in pin(ART/'d4a-scattering-bootstrap-run-20260924/run_once.py')[1].decode()
# Fresh link target and real identity screen, no project mutation.
links=[];inbound=[]
for base,dirs,files in os.walk(ROOT,followlinks=False):
 if pathlib.Path(base)==ROOT:dirs[:]=[d for d in dirs if d!='.git']
 for n in list(dirs)+files:
  p=pathlib.Path(base)/n
  if p.is_symlink():
   target=os.readlink(p);resolved=str((p.parent/target).resolve(strict=False));links.append(dict(path=str(p),target=target,resolved=resolved))
   if resolved in cp:inbound.append(str(p))
assert len(links)==687 and not inbound
for row in exact:
 s=pathlib.Path(row['path']).lstat();ident=[s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
 assert ident==row['identity']
assert all(c['identity'][6]==1 for c in candidates)
mapping=[]
for i,c in enumerate(candidates):
 primary=exact[4] if i<2 else exact[3];assert primary['sha256']==c['sha256'] and primary['size']==c['size'] and primary['identity'][:2]!=c['identity'][:2]
 mapping.append(dict(candidate=c,retained_primary=primary,original_candidate_manifest=str(ART/('d4a-scattering-bootstrap-prepared-20260924/prepared_inputs.sha256' if i==0 else 'd4a-scattering-bootstrap-run-20260924/result.sha256')),purpose='旧bootstrap原始快照或准备seed的独立工作副本',decision='EXACT_DUPLICATE_CANDIDATE_FOR_ROOT_FRESH_PREFLIGHT_NOT_DELETE_AUTHORIZATION',restoration='旧全manifest核验/重放须先按完整SHA从保留主本恢复本路径；不能恢复原inode/ctime'))
report=dict(status='PASS_READONLY_CANDIDATE_AND_RESULT_PRESERVATION_REVIEW',approved_apply=False,source_and_business_executed=False,formal_or_ART_written=False,exact_candidate_count=3,exact_candidate_allocated_bytes=sum(c['allocated'] for c in candidates),candidate_restore_mapping=mapping,bootstrap_four_holds=j(OUT/'bootstrap_six_complete_current_SHA.json'),ten_round_coverage=rounds,total_distinct_retired_paths=10018,all_prior_retired_paths_still_absent=True,nominal_retired_allocated_bytes=sum(x['nominal_retired_allocated_bytes'] for x in rounds),capacity_note='累计为退役原文件的名义分配量，含89原材料raw归档，不能当项目净降或APFS即时空闲；第九轮89 gzip恢复主件必须永久保留。',screen=dict(current_V8_graph_pin=graphpin,current_canonical_count=35647,current_namespaces=86,current_aliases=186,current_live_resource_roots=228,current_graph_all_absolute_string_hits=[],old_index_pin=idxpin,old_index_file_dir_alias_hits=[],cold6248_manifest_pin=m8pin,current_cold1534_pin=coldpin,prior_manifest_restore_primary_or_source_hits=[],prior_restore_primary_screen_pin=remainingpin,prior_restore_screen_status=remain['status'],all_687_symlinks_fresh_screened=True,candidate_inbound_symlinks=[],full_numerical_business_graph_verifier_executed=False),retained_source_and_result_pins=sourcepins,coverage_manifest_or_preflight_pins=coveragepins,documents_policy=['每轮保留精确manifest/实际账本/真实工具退出/独审/原科学result与seal，原凭证不重写。','结果文档应包含stdout/stderr/watch采样/分阶段记录/数值表格/图表/参数/源码来源，而非仅README。','第十轮已全SHA核对32,452结果文档；后增V8失败与V9隔离诊断原失败及剩余三案例证据应进入下一轮新的文档基线，不能沿用旧快照当完整当前全集。','旧包缺失中间件须明确先restore；无同SHA主本的唯一数值状态须保留或单独通过可重建/无依赖审查，不按日期或失败名称删除。','主/副恢复链不可环，不得删任何已退休文件唯一的保留primary；89 gzip不能计缓存。'],scope_limits=['这里只批准三项候选进入Root精确fresh预检；不运行或批准删除脚本。','fresh候选与主本全SHA来自独立5b28c3；此轮再次lstat identity保持，不重读全35GB科学输入。','当前V9尚未新business执行，F8 full inputs/冷动态闭包继续保留；不改变225旧根或新family scope。','源检索未发现当前factory/冷控制器直接读取这三个旧副本；历史run_once.py和旧全manifest将需要恢复。Root最终must bind latest source/dependency pins before apply.','原V2诊断故障与候选未采纳事实保持，不计科学信用。'])
save('REPORT.json',report)
text='本轮只读复核：三份早期bootstrap完整相同副本可进入精确预检，约0.388 GiB；四份较新bootstrap虽等长但六SHA不同，全部保留。前十轮实际退役10,018个不重复路径，鲜查仍缺席，原结果/账本/恢复说明均在。不得删89份gzip恢复主件、当前INPUT/冷动态数据、唯一closed/final结果。旧fullmanifest与回放须先恢复原字节；后增V8失败、V9隔离证据需加入本轮新的完整结果文档SHA基线。没有删除、业务运行或正式写入。详见REPORT.json。\n'
with (OUT/'REPORT.txt').open('x') as f:f.write(text)
print(json.dumps(dict(status=report['status'],report=str(OUT/'REPORT.json'),sha256=pin(OUT/'REPORT.json')[0]['sha256'],candidate_count=3,allocated_bytes=report['exact_candidate_allocated_bytes'],prior_deleted_count=10018,no_apply=True)))
