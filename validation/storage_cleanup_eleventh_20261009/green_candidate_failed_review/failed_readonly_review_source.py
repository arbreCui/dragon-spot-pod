"""Fixed nine old replay input NPZ pairs; readonly scientific files, own TMP reports."""
import ast
import hashlib
import json
import os
import re
import stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');ART=ROOT/'validation/artifacts'
OUT=Path('/private/tmp/spot_storage_eleventh_green_readonly_review_20261009')
OUT.mkdir(exist_ok=False)
FAMILIES=['native-oblique-streaming-20260930','native-oblique-full-preflight-20260929','native-oblique-track-pilot-compact-20260929']
GROUPS=[51,61,98]
EXPECTED={51:'276a5308ddccf17c6fd5c513ae9aa49b2188ae6f7f0f1913d61af9c7edb7f8f9',61:'4ce339dcbb518d28473c68240a311eab412e700e0165bf8f40798df7a12f0625',98:'d2de5d3f16552bd195374d272291a5b89149ce43eefcdfe3920030aa26fa83b7'}
PINS={}
def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def read(p,expected=None,return_raw=True):
 p=Path(p);s=p.lstat();before=ident(s)
 assert p.is_absolute() and p.parent.resolve(strict=True)==p.parent and stat.S_ISREG(s.st_mode)
 h=hashlib.sha256();parts=[]
 with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  assert ident(os.fstat(f.fileno()))==before
  while data:=f.read(1024**2):
   h.update(data)
   if return_raw:parts.append(data)
  assert ident(os.fstat(f.fileno()))==before
 assert ident(p.lstat())==before
 if expected:assert h.hexdigest()==expected,(str(p),'SHA mismatch')
 PINS[str(p)]=dict(path=str(p),size=s.st_size,allocated_bytes=s.st_blocks*512,sha256=h.hexdigest(),identity=before)
 return b''.join(parts) if return_raw else PINS[str(p)]
def obj(p,expected=None):return json.loads(read(p,expected))
def write(name,x):
 with (OUT/name).open('x') as f:json.dump(x,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
def strings(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if isinstance(k,str):yield k
   yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 elif isinstance(x,str):yield x
exact={};prefixes={}
def protect(p,why):
 if type(p) is str and p.startswith('/'):
  exact.setdefault(p,set()).add(why)
  if '#' in p:exact.setdefault(p.split('#',1)[0],set()).add(why+' OWNER_PREFIX')
def prefix(p,why):
 if type(p) is str and p.startswith('/'):prefixes.setdefault(p.rstrip('/'),set()).add(why)
def reasons(p):
 rs=set(exact.get(p,set()))
 for base,v in prefixes.items():
  if p==base or p.startswith(base+'/'):rs.update(v)
 return sorted(rs)

m9=obj(ROOT/'validation/storage_cleanup_ninth_20261009/manifest.json','e4b9c50d79ae6370cd62bb90ed4f2896b6e010438139c52af920672ccad8b4f8')
m10=obj(ROOT/'validation/storage_cleanup_tenth_20261009/manifest.json')
index=obj(m9['old_index_pin']['path'],m9['old_index_pin']['sha256'])
graph=obj(m9['graph_pin']['path'],m9['graph_pin']['sha256'])
assert len(graph['canonical_files'])==35647 and len(graph['namespaces'])==86 and len(graph['aliases'])==186
for p in index['protected_files']:protect(p,'OLD_PROTECTION_INDEX')
for p in index['protected_directories']:prefix(p,'OLD_PROTECTED_DIRECTORY')
for p in index['inbound_alias_targets']:protect(p,'OLD_LINK_TARGET')
for p in graph['canonical_files']:protect(p['path'],'CURRENT_V8_CANONICAL')
for p in graph['namespaces']:prefix(p['canonical_root'],'CURRENT_V8_EXHAUSTIVE_NAMESPACE')
for p in graph['aliases']:
 for key in ['path','target']:
  if p['kind']=='directory':prefix(p[key],'CURRENT_V8_DIRECTORY_ALIAS')
  else:protect(p[key],'CURRENT_V8_FILE_ALIAS')
for s in strings(graph):
 if s.startswith('/') and '\n' not in s:protect(s,'CURRENT_V8_ALL_ABSOLUTE_STRINGS')
for p in m9['critical_roots']:prefix(p,'CRITICAL_ROOT')
for p in m9['current_cold_extra_protected_files']:protect(p,'CURRENT_FUTURE_COLD_DYNAMIC')
assert len(m9['current_cold_extra_protected_files'])==6248
cold=obj(m9['current_cold_dynamic_proof']['report']['path'],m9['current_cold_dynamic_proof']['report']['sha256'])
for group in ('source_pins_and_actual_function_definitions','actual_pinned_metadata'):
 for row in cold[group]:read(row['path'],row['sha256'],False)
for row in cold['current_cold_dynamic_protected_files']:protect(row['path'],'COLD_DYNAMIC_PATH_FROM_FRESH_PINNED_SOURCES_AND_METADATA')
restores=obj(ROOT/'validation/storage_cleanup_ninth_20261009/reviews/prior_restore_cross_176/all_9124_existing_old_restoration_sources_fresh_stat_canonical_paths.json')
for row in restores:protect(row['path'],'ROUND1_TO8_RESTORATION_SOURCE')
rounds=['storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_third_20261008','storage_cleanup_fourth_20261008','storage_cleanup_fifth_20261009','storage_cleanup_sixth_20261009','storage_cleanup_seventh_20261009','storage_cleanup_eighth_20261009','storage_cleanup_ninth_20261009','storage_cleanup_tenth_20261009']
rules=[]
for name in rounds:
 directory=ROOT/'validation'/name;read(directory/'REPORT.txt',return_raw=False);rules.append(PINS[str(directory/'REPORT.txt')])
 mp=directory/'manifest.json'
 if mp.exists():
  m=obj(mp)
  for key in ('retained_primaries','retained_tapes','source_and_review_pins','source_metadata_pins'):
   if key in m:
    for p in strings(m[key]):protect(p,'PRIOR_ROUND_EXPLICIT_RETAINED_OR_SOURCE_'+name)
prefix(str(ROOT/'validation/storage_cleanup_ninth_20261009/packed_material_intermediates'),'PERMANENT_GZIP_RESTORE_ARCHIVE')

# Fresh inventory used only for the selected paths and actual symlink closure.
inv=obj(Path('/private/tmp/spot_storage_eleventh_root_audit_20261009/inventory_before.json'))
by_path={str(ROOT/r['path']):r for r in inv['files']}
linkrows=[]
for base,ds,fs in os.walk(ROOT,followlinks=False):
 ds[:]=[d for d in ds if d not in ('.git','.aws','.codex','.agents')]
 for name in list(ds)+fs:
  q=Path(base)/name
  if q.is_symlink():
   target=str(q.resolve(strict=False));row=dict(path=str(q),text=os.readlink(q),target=target,directory_target=q.is_dir());linkrows.append(row)
   if q.is_dir():prefix(target,'FRESH_DIRECTORY_SYMLINK_TARGET');prefix(str(q),'FRESH_DIRECTORY_SYMLINK_PATH')
   else:protect(target,'FRESH_FILE_SYMLINK_TARGET');protect(str(q),'FRESH_FILE_SYMLINK_PATH')
assert len(linkrows)==687
assert {(str(ROOT/r['path']),r['target']) for r in inv['links']}=={(r['path'],r['target']) for r in linkrows}

# Bind the actual intended V9 source: only source admission has occurred, no PREP/RUN.
f9=ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v9.py'
known9=Path('/private/tmp/axmat_last_cprime_trim_v9_ready_source_admission_candidate_20261009')/f9.name
if f9.exists():assert read(f9,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46')==read(known9,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46')
else:read(known9,'44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46')
review9=obj('/private/tmp/axmat_v9_ready_source_independent_review_20261009/independent_review.json','02acf5fd8f67715a8e2085b9666ec06fc19b1c2b8f31fe6277c34a9c5cf61b5f')
assert review9['status']=='PASS' and review9['factory_65_top_definitions_byte_AST_exact'] and review9['complete_original_historical_seven_body_same_whole_dict']
read(ROOT/'validation/axial_material/combined_runtime_current_predicates_final_private_last_uses_20261009.py','fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19',False)
for row in review9['all5_formal_helpers_fresh_FULL_SHA']:read(row['path'],row['sha256'],False)

# Original manifests retain both replay and source-input entries unchanged.
manifest_entries={};evidence=[]
for family in FAMILIES+['exact-native-flight-20260929']:
 p=ART/family/'result.sha256';text=read(p).decode();entries={};lines={}
 for i,line in enumerate(text.splitlines(),1):
  if not line.strip():continue
  match=re.fullmatch(r'([0-9a-f]{64})\s+\*?(.+)',line);assert match
  rel=match.group(2);resolved=str((p.parent/rel).absolute());assert str(Path(resolved).resolve(strict=False))==resolved
  assert resolved not in entries or entries[resolved]==match.group(1)
  entries[resolved]=match.group(1);lines[resolved]=i
 manifest_entries[family]=(p,entries,lines)

candidate_paths={str(ART/f/'replay/inputs'/f'green_{g}.npz') for f in FAMILIES for g in GROUPS}
assert len(candidate_paths)==9
assert not candidate_paths & {r['path'] for r in m10['candidates']}
recommendations=[];kept={};oldreaders=[]
for family in FAMILIES:
 folder=ART/family
 docs=['initial_inputs.json','copied_inputs.json','source_inputs.json','replay_inputs.json','calibration_inputs.json','verification_inputs.json','verification.json','verification/result.json','verification/final_integrity.json','report.md','README.md']
 documents={}
 for name in docs:
  p=folder/name
  if p.exists():
   raw=read(p);documents[name]=json.loads(raw) if p.suffix=='.json' else raw.decode();evidence.append(PINS[str(p)])
 mp,entries,lines=manifest_entries[family]
 for group in GROUPS:
  q=folder/'replay/inputs'/f'green_{group}.npz';same=folder/'inputs'/f'green_{group}.npz';primary=ART/'exact-native-flight-20260929/analysis'/f'{group}_whole/green.npz'
  for p in (q,same,primary):read(p,EXPECTED[group],False)
  assert PINS[str(q)]['size']==PINS[str(same)]['size']==PINS[str(primary)]['size']
  assert PINS[str(q)]['identity'][6]==1 and len({tuple(PINS[str(p)]['identity'][:2]) for p in (q,same,primary)})==3
  assert not reasons(str(q)),(str(q),reasons(str(q)))
  assert str(q) in by_path and by_path[str(q)]['identity']==PINS[str(q)]['identity'] and by_path[str(q)]['allocated_bytes']==PINS[str(q)]['allocated_bytes']
  assert entries[str(q)]==entries[str(same)]==EXPECTED[group]
  native_mp,native_entries,native_lines=manifest_entries['exact-native-flight-20260929'];assert native_entries[str(primary)]==EXPECTED[group]
  json_edges=[]
  for name,body in documents.items():
   if not isinstance(body,dict):continue
   for rel,val in body.items():
    if not isinstance(rel,str) or not isinstance(val,str) or val!=EXPECTED[group]:continue
    if (folder/rel).absolute() in (q,same) or (ROOT/rel).absolute()==primary:
     json_edges.append(dict(path=str(folder/name),pointer=rel,sha256=val,resolved_path=str((ROOT/rel).absolute() if rel.startswith('validation/') else (folder/rel).absolute())))
  assert any(e['resolved_path']==str(same) for e in json_edges)
  if family=='native-oblique-streaming-20260930':assert any(e['resolved_path']==str(q) and e['path'].endswith('/replay_inputs.json') for e in json_edges)
  kept[str(same)]=dict(role='SAME_FAMILY_ORIGINAL_INPUT_NOT_DELETED',**PINS[str(same)]);kept[str(primary)]=dict(role='PERMANENT_ORIGINAL_SCIENTIFIC_EXACT_NATIVE_FLIGHT_PRIMARY',**PINS[str(primary)])
  recommendations.append(dict(category='EXACT_DUPLICATE_OLD_NATIVE_REPLAY_INPUT',**PINS[str(q)],primary=PINS[str(primary)],retained_same_family_input=PINS[str(same)],same_size_SHA_complete_fresh_reads=True,current_canonical_namespace_alias_allstring_cold_critical_prior_restore_and_symlink_intersections=[],original_manifest_edges=[dict(path=str(mp),manifest_sha256=PINS[str(mp)]['sha256'],line=lines[str(p)],original_path=str(p.relative_to(folder)),sha256=entries[str(p)]) for p in (q,same)]+[dict(path=str(native_mp),manifest_sha256=PINS[str(native_mp)]['sha256'],line=native_lines[str(primary)],original_path=str(primary.relative_to(native_mp.parent)),sha256=EXPECTED[group])],original_INPUT_snapshot_edges=json_edges,restore=dict(from_path=str(primary),to_path=str(q),sha256=EXPECTED[group],size=PINS[str(q)]['size'],mode=stat.S_IMODE(PINS[str(q)]['identity'][2]),mtime_ns=PINS[str(q)]['identity'][4],original_bytes_and_path_recoverable=True,inode_ctime_not_recoverable=True),historical_limit='Original whole result manifest verification and old generic artifact replay/readers require restoring this exact path first. Earlier retired replay outputs may separately require their prior-round restoration recipes. Original receipts/seals/results stay unchanged; no new scientific validation is claimed.'))
 # Fresh-pinned archived sources disclose actual legacy readers and frozen input snapshots.
 for sub in ('build','replay/build'):
  for p in sorted((folder/sub).glob('*')):
   if not p.is_file() or p.suffix not in ('.py','.cpp','.c','.h','.md'):continue
   text=read(p).decode()
   if str(p) in entries:assert PINS[str(p)]['sha256']==entries[str(p)]
   lines_e=[dict(line=i,text=line) for i,line in enumerate(text.splitlines(),1) if any(s in line for s in ('green_','replay_inputs.json','copied_inputs.json','source_inputs.json','compare_primary','compare-primary','a/\'replay','root/\'replay'))]
   if lines_e:oldreaders.append(dict(path=str(p),sha256=PINS[str(p)]['sha256'],generic_artifact_parameter_reader_or_original_snapshot_audit=True,lines=lines_e))

# Preserve and fully SHA-read every document/log/result-json inside the three old families.
docrows=[];suffixes={'.json','.jsonl','.log','.txt','.md','.sha256','.csv','.tsv','.png','.svg','.pdf'}
for family in FAMILIES:
 for base,ds,fs in os.walk(ART/family,followlinks=False):
  for name in sorted(fs):
   p=Path(base)/name
   if p.is_symlink():continue
   if p.suffix not in suffixes and p.name not in ('stdout','stderr'):continue
   assert str(p) not in candidate_paths
   read(p,return_raw=False);docrows.append(PINS[str(p)])
assert len(docrows)==3742
# Current formal source consumers have no fixed reference to the nine replay paths or families.
source_reference_hits=[];source_texts={}
for p in sorted((ROOT/'validation/axial_material').glob('*')):
 if not p.is_file() or p.suffix not in ('.py','.sh','.c2m','.x2m'):continue
 text=read(p).decode();source_texts[str(p)]=text
 for i,line in enumerate(text.splitlines(),1):
  if any(name in line for name in FAMILIES) or any(q in line for q in candidate_paths):source_reference_hits.append(dict(path=str(p),line=i,text=line))
assert not source_reference_hits
all_current_source_exact_path_or_family_search_no_hits=True

# Seven-field identities are rechecked after all reads; no science file was written.
for path,row in PINS.items():assert ident(Path(path).lstat())==row['identity'],('changed',path)
write('fixed_exact9_recommendations.json',recommendations)
write('retained12_primary_and_same_family_inputs.json',list(kept.values()))
write('all_fresh_full_SHA_identity_pins.json',list(PINS.values()))
write('preserved3742_document_log_result_json_FULL_SHA.json',docrows)
write('legacy_readers_original_snapshots_and_restore_limits.json',dict(readers=oldreaders,original_snapshot_and_seal_evidence=evidence,current_axial_source_reference_hits=source_reference_hits,current_axial_source_file_count=len(source_texts),cold_source_and_metadata_fresh_pin_count=len(cold['source_pins_and_actual_function_definitions'])+len(cold['actual_pinned_metadata']),cold_original_call_chain=cold['call_chain']))
write('protection_and_current_intake_scope.json',dict(graph=PINS[m9['graph_pin']['path']],old_index=PINS[m9['old_index_pin']['path']],graph_canonical=35647,graph_namespaces=86,graph_aliases=186,critical_roots=len(m9['critical_roots']),cold_protected=6248,fresh_links=687,prior_round1_to8_restore_source_records=len(restores),all_previous1_to10_explicit_restoration_primary_source_paths_included=True,current_v9_source_same_original_F8_contract_and_completeINPUT_bound=True,current_v9_source_only_review=PINS['/private/tmp/axmat_v9_ready_source_independent_review_20261009/independent_review.json'],rules_read=rules,candidate_intersections=[],unknown_arbitrary_old_artifact_consumers_require_restoration=True,no_live_API_or_cold_intake_admission=True))
logical=sum(x['size'] for x in recommendations);allocated=sum({tuple(x['identity'][:2]):x['allocated_bytes'] for x in recommendations}.values())
report=dict(schema='SPOT_ELEVENTH_FIXED_NATIVE_REPLAY_GREEN_INPUT_EXACT_RECOMMENDATION_V1',status='PASS',scope='READONLY_FIXED9_EXACT_WORK_COPY_RECOMMENDATIONS_NOT_DELETE_AUTHORIZATION_OR_SCIENCE_ADMISSION',recommendation_count=9,logical_bytes=logical,allocated_unique_inode_bytes=allocated,allocated_unique_inode_GiB=allocated/2**30,retained_inputs_and_scientific_primaries=12,original_manifest_both_copy_and_main_input_and_original_scientific_primary_entries_verified=True,all9_current_canonical_namespace_alias_allstring_cold6248_critical92_and_all_prior_restore_sources_intersection_empty=True,current_V9_source_admission_is_same_F8_INPUT_math_contract=True,original_result_document_and_log_count=3742,original_result_document_and_log_bytes=sum(x['size'] for x in docrows),all_document_logs_and_original_result_seals_remain=True,full_fresh_SHA_pin_count=len(PINS),all_source_metadata_and_fixed_payload_identities_stable=True,old_generic_parameter_readers_not_claimed_absent=True,old_whole_replay_and_manifest_validation_requires_restore_first=True,restore_mapping_per_candidate_complete=True,scientific_raw_unique_npz_not_selected=True,native_layered_full_and_native_oblique_full_response_inputs_not_selected=True,all_current_A_B_material_inputs_snapshots_basis_and_V8_failure_evidence_not_selected=True,temporary_reports_only=True,project_formal_ART_files_written=False,deleted_files=0,business_import_API_constructor_PREP_RUN_native_or_probe=False,new_RSS_science_AAA_ABA_credit=False,actual_readonly_review_tool_terminal=None,limitations=['This is a fixed nine-path readonly recommendation. Root must bind the exact candidate/current primary/source and document pins in a fresh preflight before any retirement.','No generic or historical reader is asserted globally absent: old manifests and artifact-parameter readers require restoration of the nine paths before use. Original inode/ctime cannot be restored.','Allocated-byte total uses nine distinct single-link inodes and is not an attribution of system free-space change.','Current graph/protection and intended cold source metadata were parsed statically; no scientific admission or current data API was executed.'])
write('REPORT.json',report)
print(json.dumps(dict(status=report['status'],count=9,logical_bytes=logical,allocated_unique_inode_bytes=allocated,retained=12,preserved_documents=3742,fullSHAfiles=len(PINS),report_sha256=hashlib.sha256((OUT/'REPORT.json').read_bytes()).hexdigest(),recommendations_sha256=hashlib.sha256((OUT/'fixed_exact9_recommendations.json').read_bytes()).hexdigest(),files_deleted=0,no_business=True)))
