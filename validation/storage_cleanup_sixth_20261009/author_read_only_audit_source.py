import os,stat,json,hashlib,collections,time,datetime
from pathlib import Path
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts';OUT=Path('/private/tmp/spot_sixth_storage_duplicate_review_20261009')
FAMILIES=['native-radial-response-20260928','native-axial-coupling-20260928','native-segment-composition-compact-20260929','native-segment-composition-20260929','d4a-map6-physical-column-trace-20260928','native-directional-response-20260929']
LIBS={'libDragon.a':ROOT/'lib/Darwin_arm64/libDragon.a','libTrivac.a':ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a','libUtilib.a':ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a','libGanlib.a':ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a'}
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p):
 p=Path(p);a=p.lstat();assert stat.S_ISREG(a.st_mode),str(p);h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(4*1024**2):h.update(b)
 b=p.lstat();assert ident(a)==ident(b),str(p)
 return dict(path=str(p),identity=ident(a),bytes=a.st_size,allocated_bytes=a.st_blocks*512,sha256=h.hexdigest(),stable_full_content_read=True)
GP=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v6-20261008/input_graph.json'; IP=ROOT/'validation/storage_review_more_20261008/normalized_protection_index.json'; CP=ROOT/'validation/storage_cleanup_fifth_20261009/critical_source_scope_scan.json'
g=json.loads(GP.read_text());idx=json.loads(IP.read_text());critical=json.loads(CP.read_text())['critical_roots_excluded_wholesale']
abs_paths=set()
def walk(o):
 if isinstance(o,dict):
  for k,v in o.items():walk(k);walk(v)
 elif isinstance(o,list):
  for x in o:walk(x)
 elif isinstance(o,str) and o.startswith('/'):abs_paths.add(o)
walk(g)
ns=[x['canonical_root'] for x in g['namespaces']];d_alias=[x['target'] for x in g['aliases'] if x['kind'] in ('directory','dir')];graphdirs=set(ns+d_alias)
oldfiles=set(idx['protected_files'])|set(idx['inbound_alias_targets']); olddirs=idx['protected_directories']
symlinks=[];stat_errors=[]
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 dn[:]=[n for n in dn if n not in ('.git','.aws','.codex','.agents')]
 for n in fn+dn:
  p=Path(dp)/n
  try:s=p.lstat()
  except OSError as e:stat_errors.append({'path':str(p),'error':str(e)});continue
  if stat.S_ISLNK(s.st_mode):symlinks.append(dict(path=str(p),text=os.readlink(p),resolved_target=str(p.resolve(strict=False))))
assert not stat_errors
primaries=[pin(x) for x in LIBS.values()];bp={Path(x['path']).name:x for x in primaries}
candidates=[]
for fam in FAMILIES:
 for lib,primary in LIBS.items():
  p=ART/fam/'build'/lib;r=pin(p);path=str(p)
  checks=dict(no_old_index_file=path not in oldfiles,no_old_index_directory=not any(path==x or path.startswith(x+'/') for x in olddirs),no_v6_absolute_reference=path not in abs_paths,no_v6_namespace_or_directory_alias=not any(path==x or path.startswith(x+'/') for x in graphdirs),no_critical_root=not any(path==x or path.startswith(x+'/') for x in critical),no_inbound_symlink=not any(path==x['resolved_target'] or x['resolved_target'].startswith(path+'/') for x in symlinks),single_hardlink=r['identity'][-1]==1,exact_primary_hash=r['sha256']==bp[lib]['sha256'],exact_primary_bytes=r['bytes']==bp[lib]['bytes'])
  assert all(checks.values()),(path,checks)
  r.update(retained_primary=bp[lib],screen_checks=checks,role='OLD_PRIVATE_LINK_LIBRARY_COPY',family=fam,historical_full_replay_restore_required=True)
  candidates.append(r)
selected=set(x['path'] for x in candidates)
# Fresh source literal evidence: every source occurrence for candidate families and the explicitly preserved signed host.
source_evidence=[];source_suffixes={'.py','.sh','.f','.f90','.c','.h','.cpp','.cmake'};all_families=FAMILIES+['native-signed-axial-state-20260929']
for dp,dn,fn in os.walk(ROOT,followlinks=False):
 dn[:]=[n for n in dn if n not in ('.git','.aws','.codex','.agents')]
 for n in fn:
  p=Path(dp)/n
  if p.suffix not in source_suffixes and n not in ('Makefile','CMakeLists.txt'):continue
  if p.is_symlink():continue
  try:raw=p.read_bytes();text=raw.decode('utf-8')
  except (OSError,UnicodeDecodeError):continue
  matches=[]
  for i,line in enumerate(text.splitlines(),1):
   matched=[f for f in all_families if f in line]
   if matched:matches.append(dict(line=i,families=matched,text=line))
  if matches:source_evidence.append({**pin(p),'matches':matches})
# Preserve original receipts, commands, logs, summaries and all unique executable bytes; source occurrence here never means absent.
retained=[];metadata_refs=[]
for fam in FAMILIES:
 a=ART/fam
 for p in sorted(a.iterdir()):
  if p.is_file() and not p.is_symlink() and p.suffix in ('.json','.md','.txt','.sha256'):retained.append(pin(p))
 for p in sorted((a/'build').iterdir()):
  if not p.is_file() or p.is_symlink() or str(p) in selected:continue
  if p.suffix in ('.json','.log','.tsv','.py','.f90','.f','.patch','.md','.txt') or (p.stat().st_mode&0o111):retained.append(pin(p))
 for p in a.rglob('*'):
  if not p.is_file() or p.is_symlink() or p.suffix not in ('.json','.md','.txt','.sha256','.tsv'):continue
  if p.stat().st_size>2*1024**2:continue
  try:t=p.read_text()
  except UnicodeDecodeError:continue
  lines=[]
  for i,line in enumerate(t.splitlines(),1):
   if any('/build/'+lib in line or 'build/'+lib in line for lib in LIBS):lines.append(dict(line=i,text=line))
  if lines:metadata_refs.append({**pin(p),'library_reference_lines':lines})
held_signed=[pin(ART/'native-signed-axial-state-20260929'/'build'/lib) for lib in LIBS]
# Pin existing fifth round retirement: no already retired file is a new candidate.
fifth=ROOT/'validation/storage_cleanup_fifth_20261009';manifest=json.loads((fifth/'manifest.json').read_text());old30={x['path'] for x in manifest['candidates']}
assert not(selected&old30);assert all(not Path(x).exists() for x in old30)
report=dict(schema='SPOT_SIXTH_READ_ONLY_EXACT_OLD_LINK_LIBRARY_CANDIDATE_REVIEW_V1',status='CANDIDATES_FOR_ROOT_PREFLIGHT_NOT_DELETED',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),no_deletion_performed=True,no_ART_write=True,no_source_edit=True,no_API_import_PREP_RUN_or_physics=True,fresh_full_content_read_only=True,current_input_graph_pin=pin(GP),old_protection_index_pin=pin(IP),critical_roots_source_pin=pin(CP),critical_roots_excluded_wholesale=critical,v6_graph_screen=dict(canonical_files=len(g['canonical_files']),all_absolute_strings=len(abs_paths),namespaces=len(g['namespaces']),distinct_namespace_roots=len(set(ns)),namespace_roots=ns,all_aliases_count=len(g['aliases']),directory_aliases_count=len(d_alias),aliases=g['aliases'],live_resource_roots=len(g['live_resource_roots']),canonical_and_namespace_and_all_alias_strings_screened=True,business_graph_verifier_executed=False),old_protection_screen=dict(protected_files=len(idx['protected_files']),protected_directories=len(olddirs),inbound_alias_targets=len(idx['inbound_alias_targets'])),fresh_symlink_screen=dict(count=len(symlinks),stat_errors=stat_errors,symlinks=symlinks),candidate_count=len(candidates),candidate_logical_bytes=sum(x['bytes'] for x in candidates),candidate_allocated_bytes=sum(x['allocated_bytes'] for x in candidates),families=FAMILIES,candidates=candidates,retained_primary_libraries=primaries,all_exact_duplicates_and_scope_checks_pass=True,source_literal_evidence_pins=source_evidence,metadata_library_reference_evidence_pins=metadata_refs,retained_original_result_source_log_parameter_command_and_unique_executable_pins=retained,explicitly_preserved_signed_host_libraries=held_signed,explicit_signed_source_dependency=dict(path=str(ROOT/'validation/axial_material/probe_refined_AAA_white_odd_response.py'),prepare_library_verification_lines=[78,79,80,81,82,83],prepare_link_lines=[92,93,94],reason='Source prepare verifies these four original signed-host libraries through OLD/result.sha256 and links Utilib/Ganlib; preserve all four.'),prior_fifth_round=dict(manifest_pin=pin(fifth/'manifest.json'),result_pin=pin(fifth/'cleanup_result.json'),previous_30_paths_absent=True,new_candidates_do_not_overlap_previous_30=True,previous_retired_bytes_not_recounted=True),noncandidate_large_result_policy=['Do not retire any closed_snapshot/state/candidate/returned_snapshot or unique basis/system/native-result array as part of this shortlist.','All scientific main closed states and result documents, original result.sha256 and input/copy manifests remain byte-exact.','No material/library math input, old/current full-map factor, graph canonical file or namespace root is selected.','Signed-host, POD build, main project lib and source-tree lib copies remain.'],limitations=['This is a candidate content and source screen, not authorization to delete; Root must fresh preflight and independently review exact 24 paths.','Old compile commands and immutable result/input manifests explicitly reference these private copies. Retirement preserves final executables, numerical results, original source and receipts but old full manifest verification and rebuild need restoration from retained primary bytes at exact old paths.','Every candidate family has literal and/or historical metadata references; absence of all source references is not claimed.','Dynamic generated path usage outside inspected source is not exhaustively disproven; current V6 graph/old index/critical roots/all aliases/symlinks exclude all selected paths.','V7 has not been run by this review; no production API, graph verifier or allocation/physics work executed.'])
(OUT/'exact_library_candidates.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'path':str(OUT/'exact_library_candidates.json'),'sha256':hashlib.sha256((OUT/'exact_library_candidates.json').read_bytes()).hexdigest(),'count':len(candidates),'allocated_bytes':report['candidate_allocated_bytes'],'allocated_gib':report['candidate_allocated_bytes']/2**30,'source_pins':len(source_evidence),'metadata_pins':len(metadata_refs),'retained_evidence_pins':len(retained),'no_deletion':True},indent=2))
