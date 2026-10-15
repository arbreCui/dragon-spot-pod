import hashlib,json,os,stat,collections
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';OUT=Path('/private/tmp/spot_storage_eighth_candidate_review_20261009')
pins={}
def identity(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def fresh(p,wanted=None):
 p=Path(p);before=identity(p);assert stat.S_ISREG(before[2]);h=hashlib.sha256()
 with p.open('rb')as f:
  assert [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino]==before[:2]
  while b:=f.read(4*1024**2):h.update(b)
 assert identity(p)==before
 if wanted:assert h.hexdigest()==wanted,(str(p),h.hexdigest())
 row=dict(path=str(p),sha256=h.hexdigest(),identity=before,size=before[3],allocated_bytes=p.lstat().st_blocks*512)
 pins[str(p)]=row;return row
def doc(p,wanted=None):fresh(p,wanted);return json.loads(Path(p).read_text())
def seal(p):
 fresh(p);result={}
 for line in Path(p).read_text().splitlines():
  digest,name=line.split(None,1);name=name.strip()
  if name.startswith('./'):name=name[2:]
  assert name not in result;result[name]=digest
 return result

previous=[]
for directory in ['storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_third_20261008','storage_cleanup_fourth_20261008','storage_cleanup_fifth_20261009','storage_cleanup_sixth_20261009','storage_cleanup_seventh_20261009']:
 base=ROOT/'validation'/directory
 reports=[]
 for name in ['REPORT.txt','cleanup_result.json','manifest.json','retirement_ledger.jsonl']:
  if (base/name).is_file():reports.append(fresh(base/name))
 previous.append(dict(directory=str(base),pins=reports))
old_plan=doc(ROOT/'validation/storage_cleanup_seventh_20261009/manifest.json','80db08c34dcaa406950eb3680287f016d619ee76ac9503232dbf8e9348ee6038')
graph=doc(old_plan['graph_pin']['path'],'9103f35a3f121972969270162be56babe72143869b050f5220af6f3eb0715e68')
idx=doc(old_plan['old_index_pin']['path'],'30893b4a333c6dc39df420b136b095e076e0ad2ac6255336b8e3eb26ced49b86')
absolute=set()
def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():walk(k);walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
 elif isinstance(v,str) and v.startswith('/'):absolute.add(v)
walk(graph)
files=absolute|set(idx['protected_files'])|set(idx['inbound_alias_targets'])
directories=set(idx['protected_directories'])|set(old_plan['critical_roots'])|{r['canonical_root']for r in graph['namespaces']}|{r['target']for r in graph['aliases']if r['kind']in('directory','dir')}

generic='2908cf383be163cb0534847fe7115d42c9deed97684c28abdd9c29f24c6722db'
gmres='df83931c4ba0e5f5a7dfa534438967536a71d82e62e77ba4fc6bcb2e8f19f84a'
release=ART/'d4a-corrected-closed0-runtime-release-20260920'
gmres_root=ART/'gmres-activity-build'
pairs=[(gmres_root/'source/src/Dragon',gmres_root/'source/bin/Darwin_arm64/Dragon',gmres),
       (ART/'iterative-d4a-rank2-map8-observables/Dragon',release/'Dragon',generic),
       (ART/'iterative-d4a-rank2-picard-map8/frozen_runtime/Dragon',release/'Dragon',generic)]
candidates=[];selected=set()
for candidate,primary,wanted in pairs:
 c=fresh(candidate,wanted);p=fresh(primary,wanted)
 assert c['size']==p['size'] and c['identity'][:2]!=p['identity'][:2] and c['identity'][-1]==p['identity'][-1]==1
 assert candidate.parent.resolve(strict=True)==candidate.parent and primary.parent.resolve(strict=True)==primary.parent
 assert str(candidate)not in files and not any(str(candidate)==d or str(candidate).startswith(d+'/')for d in directories)
 assert candidate.is_relative_to(ART) and primary.is_relative_to(ART)
 selected.add(str(candidate))
 candidates.append(dict(**c,category='EXACT_DUPLICATE_OLD_COMPILED_WORK_COPY',retained_primary=str(primary),historical_whole_replay_restore_required=True,restoration_is_copy_of_complete_original_bytes_not_recompile=True))
release_manifest=seal(release/'d4a_closed0_release.sha256');assert release_manifest['Dragon']==generic
observables=ART/'iterative-d4a-rank2-map8-observables';obs_seal=seal(observables/'result.sha256');assert obs_seal['Dragon']==generic
picard=ART/'iterative-d4a-rank2-picard-map8';picard_seal=seal(picard/'result.sha256');assert picard_seal['frozen_runtime/Dragon']==generic
exe_manifest=seal(gmres_root/'executable.sha256');assert exe_manifest['bin/Darwin_arm64/Dragon']==gmres
receipt=fresh(gmres_root/'build_receipt.tsv');text=Path(receipt['path']).read_text();assert 'bin/Darwin_arm64/Dragon\t'+gmres in text
make=fresh(gmres_root/'source/src/Makefile');make_text=Path(make['path']).read_text();assert 'Dragon: libDragon.a DRAGON.o $(bin)/ sub-make' in make_text and 'cp $@ $(bin)/$@' in make_text
for p in [gmres_root/'source_identity.tsv',gmres_root/'instrumented_source_manifest.sha256',gmres_root/'Dragon.nm',gmres_root/'Dragon.otool',gmres_root/'symbol_audit.txt',picard/'input_manifest.sha256',picard/'execution_manifest.sha256',picard/'output_manifest.sha256',picard/'frozen_runtime/run_d4a_rank2_picard_map.sh',picard/'frozen_runtime/run_d4a_rank2_picard_maps_6_to_8.sh',ROOT/'validation/iterative/run_d4a_rank2_picard_map.sh',ROOT/'validation/iterative/run_d4a_rank2_picard_maps_6_to_8.sh',observables/'d4a_map8_observables.x2m',observables/'observables.log']:
 fresh(p)
literal_contracts=[]
for p in [picard/'frozen_runtime/run_d4a_rank2_picard_map.sh',ROOT/'validation/iterative/run_d4a_rank2_picard_map.sh']:
 text=p.read_text();assert 'DRAGON="$ROOT/bin/Darwin_arm64/Dragon"'in text
 literal_contracts.append(dict(source=str(p),default_runtime='MAIN_CANONICAL_BIN_RETAINED',explicit_runtime_option='RUNTIME argument selects its own complete manifest; old frozen stage requires restoration before replay',parent_full_result_manifest_checked='shasum -a 256 -c result.sha256'in text))
for p in [ROOT/'validation/axial_material/prepare_qualified_AB_production_v2.py',ROOT/'validation/axial_material/prepare_r64_snapshot_B_dependencyfix.py',ROOT/'validation/axial_material/verify_r64_normalized_snapshot.py',ROOT/'validation/axial_material/verify_r64_snapshot_diagnostics.py',ROOT/'validation/axial_material/probe_refined_AAA_white_odd_response.py',ROOT/'validation/iterative/run_d4a_flu650_gmres1300.sh',ROOT/'validation/iterative/run_d4a_flu650_canonical.sh']:
 fresh(p)
declaration=doc(ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009/declaration.json','df56e805ff04d9ec5cffc3b877f6054d9d68de849407c7ebee45fdc1175d7e52')
assert len(declaration['resource_roots'])==225 and all(Path(p).is_dir()and not Path(p).is_symlink()for p in declaration['resource_roots'])
f7=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v7.py'
fresh(f7,'45783d9920a53ca517f28abbff9071e81cd29b0ef87336f45216aa86d8e4bc5a')
v7_failure=doc(ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v7_build_review_20261009/independent_actual_failure_review.json','33bc79cf6c604c1f51efa60eb79e138fac718ec6bb1903dd944d65fe8995da00')
assert v7_failure['failed_final_watch']['sampled_peak_rss_mib']==516.78125
links=[]
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 for name in dn+fn:
  p=Path(dp)/name
  if p.is_symlink():
   target=p.resolve(strict=False)
   assert not any(Path(q)==target or Path(q).is_relative_to(target)for q in selected),(str(p),str(target))
   links.append(dict(path=str(p),text=os.readlink(p),target=str(target)))
assert len(links)==687
newfamily=[p.name for p in ART.iterdir()if 'scopes-v8-'in p.name or 'wire-compact'in p.name or 'requirements-varint'in p.name]
assert not newfamily,'New V8 artifact family requires refreshed closure before handoff'
# Locate references only; a literal scan alone never establishes no future dynamic
# path. The actual generic producer defaults and named restoration boundaries above
# are retained separately.
patterns=['gmres-activity-build','source/src/Dragon','iterative-d4a-rank2-map8-observables','iterative-d4a-rank2-picard-map8']
literal_hits=[];source_files=0
for dp,dn,fn in os.walk(ROOT/'validation',followlinks=False):
 for name in fn:
  p=Path(dp)/name
  if p.suffix not in ('.py','.sh','.c2m','.x2m') or p.is_symlink()or p.stat().st_size>2*1024**2:continue
  source_files+=1
  try:text=p.read_text()
  except UnicodeDecodeError:continue
  matches=[dict(line=i,text=line[:700])for i,line in enumerate(text.splitlines(),1)if any(pattern in line for pattern in patterns)]
  if matches:literal_hits.append(dict(pin=fresh(p),matches=matches))
for p,row in pins.items():assert identity(p)==row['identity'],p
for p,_,wanted in pairs:fresh(p,wanted)
index_hash=hashlib.sha256(json.dumps(sorted(links,key=lambda x:x['path']),separators=(',',':')).encode()).hexdigest()
inventory=doc(OUT/'compiled_complete_hash_duplicate_groups.json')
held_reasons=[
 dict(scope='Remaining 12 private .a files',reason='signed four directly verified/linked by current probe; POD four critical provenance; gmres four different main variant. All retained.'),
 dict(scope='V2-V7 failed combined runtime Dragon copies and all latest V7 actual failure source/result/watch/raw metadata',reason='Whole immutable real failed packets retained. Exact bytes elsewhere alone are not a reason to dismantle this still active failure evidence.'),
 dict(scope='R64 normalization, A/B snapshot, dependencyfix, rebalance runtime and duplicate build objects',reason='Current public producer/offline verifiers iterate whole execution/protocol file maps, retain older failed packaging provenance and qualified producer-runtime identity; explicit dynamic dependencies need HOLD despite absent graph literal.'),
 dict(scope='1699 old .o files, other Dragon variants and .dylib/.so cache copies',reason='Only a subset has exact duplicates; no complete original receipt/current dependency exclusion was established for further retirement. Unique compiler variants and current cached dylib must remain.'),
 dict(scope='153 unprotected old .pyc candidates',reason='No complete original cache ownership/seal/reconstruction proof; fresh hash grouping produced no byte-identical pyc pair. Small savings do not justify loosening evidence boundaries.'),
 dict(scope='Largest native layered/oblique archives, material products, source-factor/envpin/cold production snapshots',reason='Unique scientific results or complete current INPUT namespace/metadata. Keep original raw results/logs/docs/source; only separately proven old ordinary copies are candidates.')]
report=dict(schema='SPOT_EIGHTH_EXACT_COMPILED_WORK_COPY_SOURCE_CANDIDATE_REVIEW_V1',status='PASS_NARROW_CANDIDATE_SOURCE_REVIEW_ROOT_FRESH_PREFLIGHT_REQUIRED',utc=datetime.now(timezone.utc).isoformat(),
 candidates=candidates,exact_count=3,logical_bytes=sum(c['size']for c in candidates),allocated_bytes=sum(c['allocated_bytes']for c in candidates),allocated_GiB=sum(c['allocated_bytes']for c in candidates)/2**30,
 retained_primaries=[pins[str(p)]for p in sorted(set(primary for _,primary,_ in pairs))],all_candidate_and_primary_complete_fresh_SHA_byte_equal=True,all_distinct_singlelink_regular_realparent=True,
 original_proofs=dict(gmres_local_link_then_install_copy_source=pins[str(gmres_root/'source/src/Makefile')],gmres_original_installed_executable_SHA=pins[str(gmres_root/'executable.sha256')],gmres_original_build_receipt=pins[str(gmres_root/'build_receipt.tsv')],gmres_candidate_src_Dragon_has_no_independent_original_seal_row=True,gmres_proof_limit='src/Dragon is the linked build target installed by Makefile; original receipt binds retained bin/Dragon. Exact current src/bin bytes were independently freshly compared; no recompile identity proof is claimed.',observables_original_result_manifest=pins[str(observables/'result.sha256')],picard_original_result_manifest=pins[str(picard/'result.sha256')],release_original_manifest=pins[str(release/'d4a_closed0_release.sha256')]),
 graph_pin=pins[old_plan['graph_pin']['path']],old_index_pin=pins[old_plan['old_index_pin']['path']],critical_roots=old_plan['critical_roots'],current_graph_counts=dict(canonical=35646,namespaces=86,aliases=186,requirements=235528,resource_roots=225),candidate_current_old_closure_intersections=[],
 fresh_all_project_symlinks=dict(count=687,sha256=index_hash,candidate_or_ancestor_target_intersections=[]),original_V7_resource_roots=declaration['resource_roots'],V8_ART_family_not_created_at_this_observation=True,V8_final_current_closure_refresh_still_required_before_apply=True,
 source_literal_screen=dict(files_scanned=source_files,matched_files=literal_hits,not_a_universal_arbitrary_dynamic_path_proof=True),actual_generic_script_contracts=literal_contracts,
 prior_seven_reports_and_original_ledger_pins=previous,
 preserved_policy=['No directory removals; all current 225 root paths remain. Future V8 additions must not replace or subtract old roots.','Original results/source/logs/reports/scientific payloads and uniquely different programs stay. No old SHA manifest is rewritten.','Original full observables/Picard result checks and reused old parent stage need exact candidate bytes restored from retained ART release program before full replay. Main bin remains.','For GMRES, retained source/bin runtime and original executable receipt remain. Re-running old local Make target or directory replay needs restoring src/Dragon exact bytes; generic DRAGON_BIN supplied future src target is outside current saved fixed goal scope.','No candidate primary is only outside ART; the existing strict ART-only restore utility can be reviewed against these pairs without broadening safe roots.'],
 retained_HOLD_reasons=held_reasons,fresh_evidence_pins=list(pins.values()),
 wider_static_scan_limit=dict(compiled_archive_files=2147,unprotected_static_files=2051,wide_fresh_content_files=inventory['full_hashed_files'],wide_fresh_content_bytes=inventory['full_hashed_bytes'],wide_groups_are_not_deletion_approval=True),
 capacity_observed_read_only_du=dict(project_allocated_bytes=168700694528,ART_allocated_bytes=167800348672,initial_chunk_id='4c1ab1',session_id=52433,terminal_chunk_id='277aca',exit_code=0,not_final_after_cleanup_capacity=True),
 files_deleted=0,formal_or_ART_written=False,business_import_API_constructor_PREP_RUN_solver_or_native_executed=False,new_RSS_or_scientific_credit=False,limits=['This is a narrow candidate/source handoff, not final union manifest, actual fresh preflight approval or cleanup completion.','All wide exact groups other than the exact three selected paths remain HOLD; do not consume the inventory as a deletion list.','Current graph metadata was only parsed/read; no business input graph API was run.','Future arbitrary user-selectable runtime paths and full retired historical directory replay require restoration, as expressly recorded.'])
for name,value in [('exact_compiled_candidates.json',report),('fresh_symlink_inventory.json',links)]:
 p=OUT/name
 with p.open('x')as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
 b=p.read_bytes();print(json.dumps(dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),exact_count=3,allocated_bytes=report['allocated_bytes'],status=report['status']),ensure_ascii=False))
