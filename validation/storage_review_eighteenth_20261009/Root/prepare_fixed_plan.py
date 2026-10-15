import hashlib,json,stat,subprocess,time
from pathlib import Path
R=Path('/Users/wen/spot')
D=Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
CD=Path('/private/tmp/spot_storage_review_eighteenth_build_cache_20261009')
RD=Path('/private/tmp/spot_storage_review_eighteenth_graph_20261009')
ID=Path('/private/tmp/spot_storage_eighteenth_native_layered_raw_independent_review_20261009')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_bytes())
def ident(p):
 s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p): return dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p))

c=read(CD/'compiled_candidate_screen.json')
z=read(RD/'layered_raw_candidates.json')
grp=read(RD/'LAYERED_RAW_REVIEW.json')
ir=read(ID/'REPORT.json')
fin=read(ID/'FINAL_REPORT.json')
assert fin['status']=='PASS' and fin['previous_manifest_count']==16 and fin['previous_ledger_count']==14
assert fin['previous_restore_mapping_intersections']==[] and fin['previous_ledger_intersections']==[] and fin['previous_restore_source_literal_intersections']==[]
assert fin['recovery_contract']['historical_copy_restore_fast_path_affected'] is False
assert grp['status']=='PASS' and ir['status']=='PASS'
assert ir['candidate_count']==12960 and ir['previous_restore_master_or_exact_candidate_path_intersections']==[]
assert type(ir['retained_batch_operators_controls_result_complete']) is int and ir['retained_batch_operators_controls_result_complete']==1080 and type(ir['full_jobs_watchdog_true_typed_zero']) is int and ir['full_jobs_watchdog_true_typed_zero']==2191
assert grp['all12960_raw_fresh_fullSHA_original_manifest_and_both_receipts_equal'] is True
assert len(c['candidates'])==1372 and len(z['candidates'])==12960
B=R/'validation/artifacts/axial-material-production-qualified-AB-historical-input-owned-specs-physical-cache-memory-dedup-last-cprime-trim-file-snapshot-scipy-env-physical-basis-own-pid-peak-v9-20261009/own_rss_binding.json'
G=R/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
assert sha(B)=='4e8de93043fa08ac0c6e1f1702b69606a6bf0b155c30007c356ec4837919c930'
assert sha(G)=='0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3'
b=read(B);g=read(G)
held=set(b['files'])|{x['path'] for x in g['canonical_files']}|set(g['requirements']['paths'])
subtrees=[x['canonical_root'] for x in g['namespaces']]+g['live_resource_roots']+b['resource_info']['resource_roots']
for x in g['aliases']:
 held.update([x['path'],x['target']]);subtrees.extend([x['path'],x['target']])
T=R/'validation/artifacts/native-layered-full-20261001'
jobs=[x for x in read(T/'full_jobs.json') if x['script']=='run_native_layered_full_batch.py' and x.get('args',[None,None])[1]=='primary']
cases={x['args'][0] for x in jobs};assert len(cases)==1080
tracked={str(R/p.decode()) for p in subprocess.check_output(['git','ls-files','-z'],cwd=R).split(b'\0') if p}
cp=read(D/'compiled_Root_preflight.json');fixed=[]
for group,items in [('compiled',c['candidates']),('layered_raw',z['candidates'])]:
 for x in items:
  p=Path(x['path']);i=ident(p)
  assert p.is_relative_to(R) and i==x['identity'] and stat.S_ISREG(i[2]) and i[-1]==1
  assert str(p) not in held and str(p) not in tracked
  assert not any(str(p)==s or str(p).startswith(s+'/') for s in subtrees)
  if group=='compiled':
   assert p.suffix in ('.o','.a') and all(v is False for v in x['frozen_membership'].values())
   h=cp['candidate_full_fresh_sha256'][str(p)]
   assert sha(p)==h
  else:
   assert p.parent.parent==T/'primary' and p.parent.name in cases and p.name.startswith('raw_g') and p.suffix=='.npz'
   assert x['current_exact_expected_canonical_namespace_alias_literal_hits']==0
   assert read(Path(x['primary_result_path']))['all_checks_passed'] is True
   assert Path(x['retained_operators_path']).is_file() and Path(x['retained_controls_path']).is_file()
   h=x['sha256']
  fixed.append(dict(path=str(p),identity=i,logical_bytes=x['logical_bytes'],allocated_bytes=x['allocated_bytes'],sha256=h,category=group))
assert len(fixed)==14332 and len({x['path'] for x in fixed})==14332
assert sum(x['logical_bytes'] for x in fixed)==11468991672
for p,h in cp['retained_source_master_makefile_full_fresh_sha256'].items():assert sha(Path(p))==h
plan=dict(schema='SPOT_R18_ROOT_EXACT_DERIVED_RETIREMENT_FIXED_PLAN_V1',status='ROOT_FIXED_DELETION_PLAN_AFTER_COMPLETE_READONLY_ADMISSION',
 authorization='User requested revisiting old disposable files and retaining result documents; earlier authorized autonomous cleanup continues.',
 selected_count=len(fixed),categories={'compiled':1372,'layered_raw':12960},logical_bytes=sum(x['logical_bytes'] for x in fixed),allocated_bytes=sum(x['allocated_bytes'] for x in fixed),
 selected=fixed,original_raw_bytes_independently_full_SHA_checked=True,Root_raw_full_content_rehash_repeated=False,
 candidates_absent_from_current_expected_canonical_requirement_namespace_alias_resource_sets=True,
 all_result_documents_numerical_operators_controls_inputs_code_logs_failed_facts_and_unique_recovery_gzip_retained=True,
 historical_per_track_reverification_requires_isolated_recomputation_and_original_SHA_check=True,
 no_instant_or_lossless_raw_restore_promised=True,no_business_execution=True,
 review_pins=[pin(CD/'compiled_candidate_screen.json'),pin(RD/'layered_raw_candidates.json'),pin(RD/'LAYERED_RAW_REVIEW.json'),pin(ID/'REPORT.json'),pin(ID/'FINAL_REPORT.json'),pin(ID/'actual_retained_results_readonly_tool_return.json'),pin(ID/'actual_prior_restore_and_peer_binding_tool_return.json'),pin(RD/'actual_layered_raw_reader_tool_return.json'),pin(CD/'actual_readonly_tool_receipt.json'),pin(D/'compiled_Root_preflight.json'),pin(B),pin(G)],
 source_pins=cp['retained_source_master_makefile_full_fresh_sha256'],observed_unix=time.time())
out=D/'approved_fixed_plan.json'
with out.open('x') as f:json.dump(plan,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':plan['status'],'count':len(fixed),'logical_bytes':plan['logical_bytes'],'allocated_bytes':plan['allocated_bytes'],'plan_sha256':sha(out)},ensure_ascii=False))
