from pathlib import Path
import os,json,stat,hashlib,importlib.util,collections,datetime
R=Path('/Users/wen/spot');V=R/'validation';B=V/'artifacts';D=Path('/private/tmp/spot_storage_twelfth_result_preservation_readonly_review_20261009');O=B/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009'
pins={}
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def raw(p,h=None):
 p=Path(p);a=ident(p);assert stat.S_ISREG(a[2])and not p.is_symlink();v=p.read_bytes();assert ident(p)==a;x=hashlib.sha256(v).hexdigest();assert h is None or x==h;pins[str(p)]=dict(path=str(p),size=len(v),sha256=x,identity=a,allocated_bytes=p.stat().st_blocks*512);return v
def obj(p,h=None):return json.loads(raw(p,h))
def strings(v):
 if isinstance(v,str):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield from strings(k);yield from strings(x)
 elif isinstance(v,list):
  for x in v:yield from strings(x)
inv=obj('/private/tmp/spot_storage_twelfth_root_inventory_20261009.json');d=obj(O/'declaration.json','7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0');g=obj(O/'input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3');old=obj(V/'storage_review_more_20261008/normalized_protection_index.json');t11=obj(V/'storage_cleanup_eleventh_20261009/manifest.json');raw(V/'storage_cleanup_eleventh_20261009/REPORT.txt');doc=obj(V/'storage_cleanup_eleventh_20261009/result_document_full_sha_baseline.json');resources=[Path(x)for x in d['resource_roots']];ns=[Path(x['root'])for x in g['namespaces']];oldroots=[Path(x)for x in old['protected_directories']];canonical=set(d['files'])|{x['path']for x in g['canonical_files']};all_g=set(strings(g));oldexact=set(old['protected_files'])|set(old['inbound_alias_targets']);rest=set();cold=set();originalmanifests=[]
for p in sorted(V.glob('storage_cleanup_*/manifest.json')):
 m=obj(p);rest.update(x for x in strings(m.get('retained_primaries',[]))if x.startswith(str(R)));rest.update(x for x in strings(m.get('source_and_review_pins',[]))if x.startswith(str(R)));cold.update(x for x in strings(m.get('current_cold_extra_protected_files',[]))if x.startswith(str(R)));originalmanifests.append(pins[str(p)])
assert len(inv['cache_files'])==223 and len(resources)==231 and len(ns)==86
candidates=[];holds=[]
for row in inv['cache_files']:
 p=Path(row['path']);a=ident(p);assert stat.S_ISREG(a[2])and not p.is_symlink();assert a[3]==row['size'] and p.stat().st_blocks*512==row['allocated_bytes'];reasons=[]
 if str(p)in canonical or str(p.resolve())in canonical:reasons.append('CURRENT_V9_CANONICAL_INPUT')
 if any(p.is_relative_to(x)for x in resources):reasons.append('CURRENT_V9_231_COMPLETE_RESOURCE_ROOT_MEMBER')
 if any(p.is_relative_to(x)for x in ns):reasons.append('CURRENT_V9_86_EXACT_NAMESPACE_MEMBER')
 if str(p)in all_g:reasons.append('CURRENT_V9_GRAPH_LITERAL_OR_ABSENCE_REFERENCE')
 if str(p)in oldexact or any(p.is_relative_to(x)for x in oldroots):reasons.append('OLD_PROTECTION_INDEX_MEMBER')
 if str(p)in rest:reasons.append('PRIOR_RESTORE_PRIMARY_OR_SOURCE_PIN')
 if str(p)in cold:reasons.append('CURRENT_COLD_6248_MEMBER')
 owner=None
 if p.suffix=='.pyc':
  owner=Path(importlib.util.source_from_cache(str(p)));assert owner.is_file()and not owner.is_symlink()
  if str(owner)in canonical:reasons.append('CONSERVATIVE_HOLD_SOURCE_OWNER_CURRENT_CANONICAL_POSSIBLE_IMPLICIT_LOADER')
 if reasons:holds.append(dict(path=str(p),allocated_bytes=row['allocated_bytes'],reasons=reasons));continue
 v=raw(p);assert a==pins[str(p)]['identity'] and a[-1]==1
 if owner is not None:
  assert len(v)>16 and int.from_bytes(v[4:8],'little')in (0,1,3);raw(owner);category='REBUILDABLE_PYTHON_BYTECODE_CACHE';description='Only per-version __pycache__ bytecode; complete source remains. A future interpreter may regenerate different bytes; original inode/ctime not recoverable.'
 else:
  assert p.is_relative_to(R/'.ruff_cache') and str(p.relative_to(R/'.ruff_cache'))in ('CACHEDIR.TAG','.gitignore','0.15.14/7217266486644075063');category='REBUILDABLE_RUFF_CACHE';description='Ordinary Ruff cache/tag; no source or scientific result.'
 candidates.append(dict(**pins[str(p)],category=category,source_owner=None if owner is None else pins[str(owner)],use_and_retirement_reason=description,not_in_current_graph_canonical_namespace_resource_old_restore_or_cold=True))
assert len(candidates)==64 and len(holds)==159
# Fresh all-project link screen; no links/directories or any other path is a candidate.
links=[]
for folder,dirs,names in os.walk(R,followlinks=False):
 if Path(folder)==R and '.git'in dirs:dirs.remove('.git')
 for name in list(dirs):
  p=Path(folder)/name
  if p.is_symlink():links.append((str(p),os.readlink(p),str(p.resolve(strict=False))));dirs.remove(name)
 for name in names:
  p=Path(folder)/name
  if p.is_symlink():links.append((str(p),os.readlink(p),str(p.resolve(strict=False))))
assert len(links)==687
chosen={x['path']for x in candidates};assert not any(target in chosen for _,_,target in links)
# Source-only literal-reference screen across project executable text; .git/data/metadata not loaded as code.
source_hits=[];tokens={Path(x['path']).name:x['path']for x in candidates}
for folder,dirs,names in os.walk(V,followlinks=False):
 for name in list(dirs):
  if (Path(folder)/name).is_symlink()or name=='__pycache__':dirs.remove(name)
 for name in names:
  p=Path(folder)/name
  if p.suffix not in ('.py','.sh','.bash','.c2m','.x2m'):continue
  if p.is_symlink():continue
  text=p.read_bytes()
  for token,path in tokens.items():
   if token.encode()in text:source_hits.append(dict(source=str(p),candidate=path))
assert source_hits==[dict(source=str(V/'iterative/check_spophys_contract.py'),candidate=str(R/'.ruff_cache/.gitignore'))]
contract_source=raw(V/'iterative/check_spophys_contract.py').decode();assert 'ignore_path = ROOT / \".gitignore\"' in contract_source and '.ruff_cache' not in contract_source
false_positive_basename_only_hit=list(source_hits);source_hits=[]
# Original .sha256/seal manifests must not own these caches; preserve generated outputs, not rewrite manifests.
manifest_hits=[]
for folder,dirs,names in os.walk(B,followlinks=False):
 for name in list(dirs):
  if (Path(folder)/name).is_symlink():dirs.remove(name)
 for name in names:
  if not(name.endswith('.sha256')or name in ('seal.json','result.json','declaration.json')):continue
  p=Path(folder)/name
  if p.is_symlink():continue
  text=p.read_bytes()
  for token,path in tokens.items():
   target=Path(path)
   if path.encode()in text or (target.is_relative_to(p.parent) and str(target.relative_to(p.parent)).encode()in text):manifest_hits.append(dict(source=str(p),candidate=path))
assert not manifest_hits
# Largest repeated whole metadata group refreshed without rewriting/deduplicating result documents.
dups=obj(D/'document_duplicate_prior_full_SHA_and_fresh_identity_screen.json');whole=next(x for x in dups['groups']if x['size']==19356767);copies=[Path(x['absolute_path'])for x in whole['rows']];new=Path(d['historical_whole_component_body']['path']);extra=Path(d['actual_last_cprime_trim_component_INPUT']['path']).parent/'input_specs.json'
for p in (new,extra):
 if p not in copies:copies.append(p)
for p in copies:raw(p,'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
for p,v in pins.items():assert ident(Path(p))==v['identity']
# Thin handoff: only chosen caches/source proofs plus protected input-root aggregate pins.
report=dict(schema='SPOT_TWELFTH_CACHE_AND_RESULT_PRESERVATION_READONLY_REVIEW_V1',status='PASS_FIXED_CACHE_CANDIDATES_FOR_ROOT_PREFLIGHT_ONLY',scope='Readonly cache fullSHA/identity, current V9 graph/resource/namespace/prior-restoration/cold/old-index/link/source/old-result-manifest screens; no deletion',observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exact_count=len(candidates),allocated_bytes=sum(x['allocated_bytes']for x in candidates),logical_bytes=sum(x['size']for x in candidates),candidates=candidates,held_cache_count=len(holds),held_cache_allocated_bytes=sum(x['allocated_bytes']for x in holds),held_reasons=collections.Counter(r for h in holds for r in h['reasons']),held_cache_paths=holds,current_scope=dict(declaration_sha256=pins[str(O/'declaration.json')]['sha256'],graph_sha256=pins[str(O/'input_graph.json')]['sha256'],canonical_files=len(g['canonical_files']),namespaces=len(ns),resource_roots=len(resources),whole_link_count=len(links),cold_protected_paths=len(cold),prior_restore_or_source_paths=len(rest)),control_metadata_pins=[pins[str(p)]for p in (O/'declaration.json',O/'input_graph.json',V/'storage_review_more_20261008/normalized_protection_index.json',V/'storage_cleanup_eleventh_20261009/manifest.json',V/'storage_cleanup_eleventh_20261009/result_document_full_sha_baseline.json')],prior_manifest_pins=originalmanifests,source_literal_cache_reference_hits=source_hits,source_basename_only_false_positive_context=dict(records=false_positive_basename_only_hit,explanation='check_spophys_contract uses ROOT/.gitignore, not ROOT/.ruff_cache/.gitignore; complete source pinned and explicit scope disambiguated',source_pin=pins[str(V/'iterative/check_spophys_contract.py')]),old_result_manifest_cache_reference_hits=manifest_hits,inbound_link_hits=[],result_docs_preserved=True,document_duplicate_summary=dict(baseline_source='T11 32585 fullSHA rows, fresh identity metadata; two intentional README/current_progress updates mean those changed rows are not assumed byte-stable',prior_duplicate_groups=dups['duplicate_groups'],prior_redundant_allocated_bytes=dups['redundant_allocated_bytes'],prior_redundant_logical_bytes=dups['redundant_logical_bytes'],unique_inode_accounting=True,all_original_docs_HOLD=True,largest_whole_specs_group_fresh_full_SHA_copies=len(copies),largest_whole_specs_group_current_canonical_paths=sum(str(p)in canonical for p in copies),largest_whole_specs_group_current_resource_member_paths=sum(any(p.is_relative_to(x)for x in resources)for p in copies),largest_whole_specs_group_pins=[pins[str(p)]for p in copies],not_a_DELETE_or_hardlink_authorization=True),old_large_data_and_frozen_build_binary_results_HOLD=True,permanent_89_material_gzip_and_prior_restore_primaries_HOLD=True,actual_PREP_RUN_watches_or_business_executed=False,formal_ART_written=False,files_deleted=0,actual_review_tool_terminal=None,limits=['PASS approves only entry of these exact cache paths into Root fresh fixed preflight; no actual deletion or whole-project preservation verification occurred here.','Keep all source owners, directories, result documents, scientific payloads, source/control seals and binary identities. Cache regeneration is allowed to produce different bytes and cannot recreate inode/ctime.','The current complete V9 SOURCE/OUT/TERM and 231 resources, all source-owner current-canonical possible implicit cache dependencies and old restorations remain excluded.','Document redundancy is about 0.5GiB logical/allocated upper bound, not safe reclaimable space; current canonical and historic source-seal metadata must retain original paths/identities.','No active writer/open-file process inventory was inferred; parent is keeping RUN stopped and must ensure the exact candidates remain unchanged during final fixed preflight/apply.','Previous scratch reader383846 exited1 due to graph canonical record field extraction. Initial review source70d5c2 had a Python identifier syntax typo;035f4c/6055e2 were basename-only .gitignore context assertions; e65c89 was old manifest basename-context assertion. TMP-only corrections preserved their sources; no deletion or business was invoked.', 'Accidental static checker62f9ce EXIT0 was check_spophys_contract.py --help; it ignores CLI help, reads six source texts and runs readonly git check-ignore. Complete source inspected. No business API/constructor/PREP/RUN/scientific solver or project write occurred; this static success gives no science credit.'])
(D/'fixed_cache_candidates_and_preservation_report.json').write_text(json.dumps(report,indent=2)+'\n')
(D/'REPORT.txt').write_text('只读结论：64份可再生成普通缓存可进入Root精确预检：61份Python .pyc、3份Ruff缓存，合计'+str(report['allocated_bytes'])+'分配字节。其他159份缓存HOLD（157在当前231资源目录，另2源.py是当前canonical可能隐式加载）。完整源码、所有目录和32,585份原结果文档保留，不执行删除或业务。\n文档确有完整SHA相同备份：按T11基线及fresh身份，名义冗余543,842,304分配字节（约0.5065GiB）。最大19,356,767B完整2cad输入包现'+str(len(copies))+'份重新全文SHA相同，其中'+str(sum(str(p)in canonical for p in copies))+'份current canonical、'+str(sum(any(p.is_relative_to(x)for x in resources)for p in copies))+'份当前资源根成员；其余需历史封存/恢复，全部HOLD，不硬链接改变身份。两份历史进度文档已按T11有记录更新，不误称全旧文档fresh SHA复读。\n89份永久材料gzip、前十一轮恢复主件、当前物理数据、唯一大XSM/native数据和原失败/成功build二进制身份保留。无新的GiB级可删确定项。缓存清理收益只有约1.4MiB，应避免新增大审计副本。\n')
print(json.dumps(dict(status=report['status'],exact_count=len(candidates),allocated_bytes=report['allocated_bytes'],logical_bytes=report['logical_bytes'],held_count=len(holds),canonical_cache_source_holds=2,full_linkscreen687=True,largest_docs_copy_count=len(copies),current_doc_canonical_paths=report['document_duplicate_summary']['largest_whole_specs_group_current_canonical_paths'],current_resource_copy_paths=report['document_duplicate_summary']['largest_whole_specs_group_current_resource_member_paths'],report_sha256=hashlib.sha256((D/'fixed_cache_candidates_and_preservation_report.json').read_bytes()).hexdigest(),report_size=(D/'fixed_cache_candidates_and_preservation_report.json').stat().st_size,no_business=True)))
