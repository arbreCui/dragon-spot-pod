import hashlib,json,math,os,stat,time
from pathlib import Path
ROOT=Path('/Users/wen/spot');R=ROOT/'validation/storage_cleanup_twelfth_20261009';TMP=Path('/private/tmp/spot_storage_twelfth_actual_postcleanup_independent_review_20261009')
M_SHA='85e7d25c110b2045119b403eb2e34e72182260bd74115b922e53ad8a77b31a47';C_SHA='ab474911150d31c4d90e74c8879caa90253bcc05e88de608d072fd7bef5f8115';O_SHA='066da16473671b323e44d818d0bc08a1dab6a4d15f3f100728c0f78b69048d38';BASELINE='d0607ceeba81dfa6e8053b04aa1e7a8823ee301ceade9fd43f32329dbf0f8efd'
PINS={};START=time.monotonic()
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None):
 p=Path(p);s=p.lstat();before=identity(s);assert stat.S_ISREG(s.st_mode)and p.parent.resolve(strict=True)==p.parent
 h=hashlib.sha256()
 with p.open('rb')as f:
  assert identity(os.fstat(f.fileno()))==before
  while b:=f.read(4*1024**2):h.update(b)
 assert identity(p.lstat())==before
 d=dict(path=str(p),sha256=h.hexdigest(),size=s.st_size,identity=before)
 if expected:assert d['sha256']==expected,str(p)
 PINS[str(p)]=d;return d
def pairs(rows):
 d={}
 for k,v in rows:assert k not in d;d[k]=v
 return d
def floating(s):
 v=float(s);assert math.isfinite(v);return v
def reject(s):raise ValueError(s)
def loads(data):return json.loads(data,object_pairs_hook=pairs,parse_float=floating,parse_constant=reject)
def obj(p,expected=None):
 d=pin(p,expected);v=loads(Path(p).read_text(encoding='utf-8'));assert identity(Path(p).lstat())==d['identity'];return v
def other_paths(excluded):
 h=hashlib.sha256();counts=dict(regular_files=0,symlinks=0,directories=0)
 # Reproduced, not imported, original sorted no-follow identity fingerprint.
 # Stream hash only; do not save a second giant baseline or read file bodies.
 for cur,sub,names in os.walk(ROOT,followlinks=False):
  base=Path(cur);sub[:]=sorted(n for n in sub if base/n not in {ROOT/'.git',R})
  h.update(json.dumps(['directory',str(base.relative_to(ROOT))],separators=(',',':')).encode()+b'\n');counts['directories']+=1
  for name in sorted(sub+names):
   p=base/name
   if str(p)in excluded:continue
   s=p.lstat()
   if stat.S_ISLNK(s.st_mode):v=['link',str(p.relative_to(ROOT)),identity(s),os.readlink(p)];counts['symlinks']+=1
   elif stat.S_ISREG(s.st_mode):v=['file',str(p.relative_to(ROOT)),identity(s)];counts['regular_files']+=1
   else:continue
   h.update(json.dumps(v,separators=(',',':')).encode()+b'\n')
 return dict(sha256=h.hexdigest(),**counts)
m=obj(R/'cache_manifest.json',M_SHA);pin(R/'cleanup_fixed_caches.py',C_SHA);assert m['cleanup_source_sha256']==C_SHA
obs=obj(R/'cleanup_terminal_observation.json',O_SHA);assert type(obs['actual_exit_code'])is int and obs['actual_exit_code']==0 and obs['closed']is True
assert (obs['initial_tool_chunk'],obs['session_id'],obs['terminal_tool_chunk'])==('6595ca',88144,'57a543')
assert obs['manifest_sha256']==M_SHA and obs['scientific_credit']is False
result=obj(R/'cleanup_result.json',obs['result_sha256']);assert result['status']=='PASS_ACTUAL_FIXED_CACHE_CLEANUP'and result['executed']is True and result['scientific_credit']is False
stdout=pin(R/'cleanup.stdout',obs['raw_stdout_sha256']);stderr=pin(R/'cleanup.stderr',obs['raw_stderr_sha256']);assert stderr['size']==obs['raw_stderr_bytes']==0
assert loads((R/'cleanup.stdout').read_text(encoding='utf-8'))==result
lp=pin(R/'retirement_ledger.jsonl',obs['retirement_ledger_sha256']);ledger=[loads(x)for x in (R/'retirement_ledger.jsonl').read_text(encoding='utf-8').splitlines()];assert len(ledger)==64
rows=m['candidates'];paths={x['path']for x in rows};assert len(paths)==len(rows)==result['count']==64
assert [(x['path'],x['sha256'])for x in ledger]==[(x['path'],x['sha256'])for x in rows]
for x in ledger:assert set(x)=={'path','sha256','removed_at'}and type(x['removed_at'])is float and math.isfinite(x['removed_at'])
for x in rows:assert not os.path.lexists(x['path']),x['path']
assert result['logical_bytes']==sum(x['size']for x in rows)==1343393 and result['allocated_bytes']==sum(x['allocated_bytes']for x in rows)==1474560
sources=m['retained_sources'];assert len(sources)==len({x['path']for x in sources})==45
for x in sources:
 p=pin(x['path'],x['sha256']);assert p['identity']==x['identity']and p['size']==x['size']
first=other_paths(paths);assert first==result['other_paths']==result['other_paths_after']==dict(sha256=BASELINE,regular_files=174008,symlinks=687,directories=6971)
print('Full other-path sorted identity fingerprint PASS:174008 regular/687links/6971dirs',flush=True)
b=Path('/private/tmp/spot_storage_twelfth_current_v9_graph_protection_boundary_20261009')
old=obj(b/'cache_223_current_closure_intersection.json','8189a99f7a5bb111a883d3953470f40618c3874100938ec4b73d551a206312c8');clear=obj(b/'cache_64_current_canonical_source_boundary.json','38e419a8c62e2790cccf67fbf04a64bc46d9d6e1b1b9a2e30e5a79353c381d23')
assert paths=={x['path']for x in clear['current_and_source_and_resource_clear_64']}
held=old['resource_root_hits']+clear['extra_current_canonical_source_cache_HOLD'];assert len(held)==len({x['path']for x in held})==159
for x in held:
 s=Path(x['path']).lstat();assert stat.S_ISREG(s.st_mode)and identity(s)==x['current_identity']
gp=ROOT/'validation/artifacts/axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v9-20261009/input_graph.json'
g=obj(gp,'0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3');assert len(g['canonical_files'])==35647 and len(g['live_resource_roots'])==231
for x in g['canonical_files']:
 s=Path(x['path']).lstat();assert stat.S_ISREG(s.st_mode)and s.st_size==x['size_bytes']
for p in g['live_resource_roots']:
 s=Path(p).lstat();assert stat.S_ISDIR(s.st_mode)and not stat.S_ISLNK(s.st_mode)
# No scientific 35GB content read here. The established PREP full-byte proof
# remains frozen; this postcleanup check is existence/identity preservation.
second=other_paths(paths);assert second==first
for x in sources:assert identity(Path(x['path']).lstat())==x['identity']
for p,d in PINS.items():assert identity(Path(p).lstat())==d['identity']
config=obj(Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009/config.json'));assert all(config[k]is None for k in ('sealSha','terminalSha','terminalPath','failed_terminal_sha'))
assert m['preserved_result_documents']is True and m['large_or_unique_scientific_data_deleted']is False and m['business_or_physics_credit']is False
report=dict(schema='SPOT_TWELFTH_ACTUAL_CACHE_CLEANUP_INDEPENDENT_POST_REVIEW_V1',status='PASS',manifest_sha256=M_SHA,cleanup_source_sha256=C_SHA,actual_root_terminal_observation_sha256=O_SHA,cleanup_result_sha256=obs['result_sha256'],retirement_ledger_sha256=obs['retirement_ledger_sha256'],actual_root_return=dict(initial='6595ca',session=88144,terminal='57a543',actual_int_exit=0,closed=True),all64_selected_absent=True,ledger_all64_exact_original_SHA_order_and_paths=True,retained45_sources_full_SHA_and_identity=True,retained45_source_bytes=sum(x['size']for x in sources),raw_stdout_whole_JSON_equals_result=True,raw_stderr_bytes=0,nonselected_original_before_root_after_and_two_independent_passes_exact=first,held159_cache_all_current_original_identity_preserved=True,all_current35647_canonical_regular_paths_and_sizes_preserved=True,all_current231_resource_directories_preserved=True,current_graph_file_full_SHA_unchanged=True,canonical35GB_payload_rehashed=False,no_second_giant_baseline_saved=True,regular_file_identity_fingerprint_is_not_full_content_hash_for_all_other_files=True,actual_logical_removed_bytes=1343393,actual_unique_singlelink_allocated_removed_bytes=1474560,scientific_credit=False,V9_RUN_started=False,review_business_import_or_API_or_PREP_RUN_or_cleaner_or_restore_executed=False,review_formal_ART_writes=False,review_files_deleted=0,fresh_small_evidence_and_source_pins=list(PINS.values()),audit_source=pin(Path(__file__)),elapsed_seconds=time.monotonic()-START)
with (TMP/'REPORT.json').open('x')as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(dict(status='PASS',report=str(TMP/'REPORT.json'),sha256=hashlib.sha256((TMP/'REPORT.json').read_bytes()).hexdigest(),removed=64,retained_sources=45,held=159,nonselected=first,elapsed_seconds=report['elapsed_seconds'])),flush=True)
