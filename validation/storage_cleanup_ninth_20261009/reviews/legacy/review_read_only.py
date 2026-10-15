from pathlib import Path
import datetime, hashlib, json, os, re, stat, subprocess

OUT=Path('/private/tmp/spot_storage_ninth_legacy_snapshot_candidate_review_20261009')
OUT.mkdir(exist_ok=True)
ROOT=Path('/Users/wen/spot'); ART=ROOT/'validation/artifacts'; V=ROOT/'validation'
R8=V/'storage_cleanup_eighth_20261009'
V8=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009'
PINS={}

def ident(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None,retain=False):
 p=Path(p);first=p.lstat();assert stat.S_ISREG(first.st_mode) and not stat.S_ISLNK(first.st_mode)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();n=0;blocks=[]
 try:
  assert ident(os.fstat(fd))==ident(first)
  while True:
   raw=os.read(fd,8*1024*1024)
   if not raw:break
   h.update(raw);n+=len(raw)
   if retain:blocks.append(raw)
  assert ident(os.fstat(fd))==ident(first)
 finally:os.close(fd)
 assert ident(p.lstat())==ident(first) and n==first.st_size
 actual=h.hexdigest()
 if expected:assert actual==expected,(str(p),actual,expected)
 info=dict(path=str(p),size=n,allocated_bytes=first.st_blocks*512,sha256=actual,identity=ident(first),fresh_full_SHA=True)
 PINS[str(p)]=info
 return (info,b''.join(blocks)) if retain else info
def jp(p,expected=None):
 info,raw=pin(p,expected,True);return json.loads(raw)
def all_absolute(o):
 result=set();todo=[o]
 while todo:
  x=todo.pop()
  if isinstance(x,str):
   if x.startswith('/'):result.add(x)
  elif isinstance(x,dict):todo.extend(x.keys());todo.extend(x.values())
  elif isinstance(x,(tuple,list)):todo.extend(x)
 return result
def inside(path,roots):return [r for r in roots if path==r or path.startswith(r.rstrip('/')+'/')]

manifest=jp(R8/'manifest.json','dcc76b4a6f6cdacd52edcaf004d206d64018f0d7b72b4f9e303e1aacf8529e8a')
groups=jp(R8/'inventory/exact_content_groups.json','e88304048fb5c9c38b72a641891881a9ae352bfe41c6e91d00b6a8ddd2ddd564')
metadata=jp(R8/'inventory/metadata_scan.json','75d3c47c3c94ba60b80c461dd82f8c00b9dc74bd646c15bc8847b37458fef250')
cold=jp(R8/'cold_dynamic/current_cold_dynamic_protected_files.json','11f9f07e92ca6c11ccb90ed4bf58b9d98a0e726bf2893a40e457c32edbc9e161')
oldindex=jp(manifest['old_index_pin']['path'],manifest['old_index_pin']['sha256'])
graph=jp(V8/'input_graph.json','242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
decl=jp(V8/'declaration.json','3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae')
assert len(graph['canonical_files'])==35647 and len(graph['namespaces'])==86 and len(graph['aliases'])==186 and len(graph['live_resource_roots'])==228
assert graph['live_resource_roots']==sorted(decl['resource_roots'])
graph_paths=all_absolute(graph); index_paths=all_absolute(oldindex)
coldpaths=set(manifest['current_cold_extra_protected_files'])|all_absolute(cold['current_cold_dynamic_protected_files'])
assert len(manifest['current_cold_extra_protected_files'])==6248 and len(cold['current_cold_dynamic_protected_files'])==6194
newcold=jp(V/'axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/next_cold_input_readonly_integrity_review/derived_required_path_SHA_owners.json')
newcoldpaths=all_absolute(newcold)
critical=manifest['critical_roots']
namespace_roots=[n['root'] for n in graph['namespaces']]
resource_roots=graph['live_resource_roots']
retired=set();prior_results=[]
for d in sorted(V.glob('storage_cleanup_*')):
 p=d/'cleanup_result.json'
 if not p.exists():continue
 result=jp(p);prior_results.append(dict(directory=str(d),result=PINS[str(p)],status=result.get('status')))
 for name in ['manifest.json','REPORT.txt']:
  q=d/name
  if q.exists():pin(q)
 ledger=d/'retirement_ledger.jsonl'
 if ledger.exists():
  _,raw=pin(ledger,retain=True)
  for line in raw.splitlines():
   if not line:continue
   row=json.loads(line)
   retired_path=row.get('path') or row.get('candidate',{}).get('path')
   assert isinstance(retired_path,str) and retired_path.startswith('/')
   retired.add(retired_path)

specs_path=V/'axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
pin(specs_path,'2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
pin(V/'axial_material/last_cprime_trim_build_review_20261008/actual_complete_production_admission.json','fed2090ee0db4bb718c6c3fbbc9ed520ed9eeddda3fca6b2cadc2f4623edb114')
pin(V/'axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v8.py','4fc0dc0e794962a371cae55ca210026b008b09879a332d497083f3c856e940a4')

pairs=[
 ('iterative-map6-axial-80s/state6_radial.xsm','iterative-map6-radial-120s/state6_radial.xsm','OLD_AXIAL_WORKING_COPY_OF_RADIAL_OUTPUT'),
 ('iterative-map6-radial-120s/state5_snapshots.xsm','iterative-map5-axial-80s/state5_snapshots.xsm','OLD_RADIAL_PARENT_INPUT_COPY'),
 ('iterative-map5-radial-120s/state4_snapshots.xsm','iterative-map4-axial-80s/state4_snapshots.xsm','OLD_RADIAL_PARENT_INPUT_COPY'),
 ('iterative-map5-axial-80s/state5_radial.xsm','iterative-map5-radial-120s/state5_radial.xsm','OLD_AXIAL_WORKING_COPY_OF_RADIAL_OUTPUT'),
 ('iterative-map4-axial-80s/state4_radial.xsm','iterative-map4-radial-120s/state4_radial.xsm','OLD_AXIAL_WORKING_COPY_OF_RADIAL_OUTPUT'),
 ('iterative-map4-radial-120s/state3_snapshots.xsm','iterative-map3-strict-current/state3_snapshots.xsm','OLD_PARENT_INPUT_COPY_OF_ORIGINAL_SCIENTIFIC_MANIFEST_PRIMARY'),
 ('iterative-sensitivity-h2-failed/base/snap1.xsm','iterative-map1/state1_snapshots.xsm','OLD_FAILED_INPUT_COPY_OF_ORIGINAL_SCIENTIFIC_MANIFEST_PRIMARY'),
 ('iterative-sensitivity-h2-failed/initial_snapshots.xsm','iterative-seed/initial_snapshots.xsm','OLD_FAILED_INPUT_COPY_OF_RETAINED_CURRENT_GENERIC_SEED'),
]
selected_paths=[str(ART/c) for c,_,_ in pairs]
rows_by_path={r['path']:r for g in groups['groups'] for r in g['rows']}
for path in selected_paths:
 assert path not in graph_paths and path not in index_paths and path not in coldpaths and path not in newcoldpaths
 assert not inside(path,critical) and not inside(path,namespace_roots) and not inside(path,resource_roots)
 # Only retired original candidate paths are relevant: retained_primary values
 # in prior ledgers are deliberately not interpreted as prior deletions.
 assert os.path.exists(path),path
 assert path not in retired,path

# Read each local original recipe/manifest/log in full, preserving its own raw
# bytes. Current/default-source matching is collected separately from historic
# recipes that naturally refer to their own retirable working copies.
source_documents={};original_text={};families=sorted({p.split('/')[0] for pair in pairs for p in pair[:2]})
for family in families:
 base=ART/family
 for p in sorted(base.rglob('*')):
  if not p.is_file() or p.is_symlink():continue
  if p.stat().st_size<2*1024*1024 and (p.suffix in ['.log','.sha256','.json','.txt','.md','.x2m','.c2m','.l2m','.o2m','.sh'] or p.name.startswith('Makefile')):
   info,raw=pin(p,retain=True);source_documents[str(p)]=info;original_text[str(p)]=raw.decode('utf-8',errors='replace')
local_manifest_rows=[]
for path,text in original_text.items():
 if not path.endswith('.sha256'):continue
 for line in text.splitlines():
  m=re.fullmatch(r'([0-9a-f]{64})\s+(.+)',line)
  if m:local_manifest_rows.append(dict(manifest=path,sha256=m[1],original_path_token=m[2]))
def resolved_original_token(row):
 token=row['original_path_token'];p=Path(token)
 if p.is_absolute():return str(p)
 if token.startswith('validation/') or token.startswith('data/'):return str(ROOT/p)
 return str((Path(row['manifest']).parent/p).resolve(strict=False))

newcold_source_path=V/'axial_material/last_cprime_trim_combined_live_resource_v8_build_review_20261009/next_cold_input_readonly_integrity_review/actual_source_pins_and_function_definitions.json'
newcold_sources=jp(newcold_source_path)
actual_cold_source_pins=[]
for source in cold['source_pins_and_actual_function_definitions']+newcold_sources:
 if source['path'] in {r['path']for r in actual_cold_source_pins}:continue
 actual_cold_source_pins.append(pin(source['path'],source['sha256']))

patterns=['iterative-map6-radial-120s','iterative-map6-axial-80s','iterative-map5-radial-120s','iterative-map5-axial-80s','iterative-map4-radial-120s','iterative-map4-axial-80s','iterative-sensitivity-h2-failed','iterative-seed']
args=['rg','-l','-F']
for x in patterns:args+=['-e',x]
args+=[str(V)]
for glob in ['*.py','*.sh','*.c2m','*.x2m','*.f','*.f90','*.cc','*.cpp','*.h','Makefile*']:args+=['-g',glob]
search=subprocess.run(args,text=True,capture_output=True)
assert search.returncode in (0,1) and search.stderr==''
source_matches=[]
for line in search.stdout.splitlines():
 path=Path(line);info,raw=pin(path,retain=True);text=raw.decode('utf-8');matched=[x for x in patterns if x in text]
 assert not any(x!='iterative-seed' for x in matched),('direct-current-source-candidate-family-reference',str(path),matched)
 source_matches.append(dict(pin=info,matched_families=matched,decision='KEEP_DEFAULT_ITERATIVE_SEED_PRIMARY; no selected candidate family direct reference'))

# Fresh link inventory, including target chains and alias directory targets.
links=[];regular_count=0;dir_count=0;archive_rows=[];large_legacy=[];runtime_holds=[]
for folder,dirs,names in os.walk(ROOT,followlinks=False):
 fp=Path(folder);dir_count+=1
 for name in list(dirs):
  p=fp/name;st=p.lstat()
  if stat.S_ISLNK(st.st_mode):
   links.append(dict(path=str(p),text=os.readlink(p),resolved_target=str(p.resolve(strict=False)),identity=ident(st)))
   dirs.remove(name)
 for name in names:
  p=fp/name;st=p.lstat()
  if stat.S_ISLNK(st.st_mode):links.append(dict(path=str(p),text=os.readlink(p),resolved_target=str(p.resolve(strict=False)),identity=ident(st)))
  elif stat.S_ISREG(st.st_mode):
   regular_count+=1
   if str(p).startswith(str(ART)+'/'):
    s=dict(path=str(p),size=st.st_size,allocated_bytes=st.st_blocks*512,identity=ident(st))
    if '/archives/' in str(p) or p.suffix in ['.tar','.tgz','.zip','.gz']:
     if st.st_size>1024*1024:
      why=[]
      if str(p) in graph_paths:why.append('CURRENT_V8_GRAPH_EXACT_PATH')
      if str(p) in index_paths:why.append('OLD_PROTECTION_INDEX_EXACT_PATH')
      if str(p) in coldpaths or str(p) in newcoldpaths:why.append('CURRENT_OR_NEXT_COLD_REQUIRED_PATH')
      if inside(str(p),critical):why.append('CRITICAL_RESULT_ROOT')
      if inside(str(p),namespace_roots):why.append('COMPLETE_INPUT_NAMESPACE')
      if inside(str(p),resource_roots):why.append('CURRENT_UNFILTERED_RESOURCE_FAMILY')
      s['decision']='HOLD';s['reasons']=why or ['UNIQUE_ARCHIVE_OR_SOURCE_AND_RECONSTRUCTION_IDENTITY_NOT_PROVED']
      archive_rows.append(s)
    if st.st_size>200*1024*1024 and p.suffix=='.xsm' and not inside(str(p),resource_roots):large_legacy.append(s)
    if st.st_size>1024*1024 and p.name=='Dragon' and inside(str(p),resource_roots):
     runtime_holds.append(dict(**s,decision='HOLD',reasons=['CURRENT_UNFILTERED_AXIAL_MATERIAL_FAMILY_AND_PRODUCER_OR_IMMUTABLE_PACKET'],
                               exact_cold_path=(str(p)in coldpaths or str(p)in newcoldpaths),exact_graph_path=(str(p)in graph_paths)))
assert len(links)==687
inbound=[]
for path in selected_paths:
 for link in links:
  target=link['resolved_target']
  if path==target or path.startswith(target.rstrip('/')+'/'):inbound.append(dict(candidate=path,link=link))
assert not inbound

candidates=[];primaries={}
for c,p,reason in pairs:
 cpath=ART/c;ppath=ART/p;record=rows_by_path[str(cpath)];primary_record=rows_by_path[str(ppath)]
 assert record['sha256']==primary_record['sha256'] and record['size']==primary_record['size']
 ci=pin(cpath,record['sha256']);pi=pin(ppath,record['sha256'])
 assert ci['identity']==record['identity'] and pi['identity']==primary_record['identity']
 assert ci['identity'][6]==pi['identity'][6]==1 and ci['identity'][:2]!=pi['identity'][:2] and ci['size']==pi['size']
 for q in [cpath,ppath]:
  for ancestor in [*reversed(q.parents),q]:assert not ancestor.is_symlink()
 original_rows=[row for row in local_manifest_rows if row['sha256']==ci['sha256'] and row['original_path_token'].endswith(cpath.name)]
 primary_original_rows=[row for row in local_manifest_rows if row['sha256']==ci['sha256'] and resolved_original_token(row)==str(ppath)]
 classification='ORIGINAL_MANIFEST_BOUND_PRIMARY' if primary_original_rows else 'FRESH_EQUALITY_AND_RETAINED_ORIGINAL_RECIPE_LOG_NO_ORIGINAL_CANDIDATE_MANIFEST'
 candidates.append(dict(candidate=ci,retained_primary=pi,reason=reason,original_rows_with_same_content=original_rows,
                        primary_original_exact_path_rows=primary_original_rows,
                        original_evidence_classification=classification,
                        same_family_primary=False,all_current_literal_namespace_critical_resource_cold_sets_zero_hits=True,
                        fresh_687_links_zero_inbound=True,restore_required_before_original_legacy_stage_or_manifest_replay=True,
                        current_generic_seed_primary_kept=(p=='iterative-seed/initial_snapshots.xsm'),
                        original_failed_sensitivity_outputs_logs_manifests_kept=True,
                        eligibility='CANDIDATE_ONLY_ROOT_FINAL_SCOPE_AND_FULL_PREFLIGHT_REQUIRED'))
 primaries[str(ppath)]=pi

for path,info in PINS.items():assert ident(Path(path).lstat())==info['identity'],('identity_changed_at_end',path)
summary=dict(schema='SPOT_NINTH_LEGACY_SNAPSHOT_AND_ARCHIVE_INDEPENDENT_READONLY_CANDIDATE_REVIEW_V1',
 status='PASS_CANDIDATE_SOURCE_AND_BYTE_REVIEW_NOT_PREFLIGHT_OR_DELETION',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 candidates=candidates,exact_count=len(candidates),logical_bytes=sum(x['candidate']['size']for x in candidates),
 allocated_bytes=sum(x['candidate']['allocated_bytes']for x in candidates),allocated_GiB=sum(x['candidate']['allocated_bytes']for x in candidates)/2**30,
 retained_primaries=list(primaries.values()),fresh_full_content_pairs=True,
 prior_eighth_content_equality_records_fresh_lstat_and_full_SHA_rechecked=True,
 current_V8_graph_pin=PINS[str(V8/'input_graph.json')],current_V8_declaration_pin=PINS[str(V8/'declaration.json')],
 current_V8_graph_counts=dict(canonical=35647,namespaces=86,aliases=186,resource_roots=228),
 current_graph_all_absolute_fields_and_old_index_literal_screen_zero_hits=True,
 current_cold_protection=dict(eighth_extra6248=True,dynamic6194=True,newer_actual_required_metadata_read=True,
                              newer_scope_read_is_not_business_admission=True,all_selected_paths_zero_hits=True),
 source_literal_matches=source_matches,source_reference_limits='Formal/source regex scan finds only retained iterative-seed default references; generic user-selectable historical stages remain runnable only after mapping restore. Local original recipes are retained and naturally reference retired working names. This is not an assertion that every possible future arbitrary argument excludes candidates.',
 archive_HOLD_records=archive_rows,archive_HOLD_count=len(archive_rows),
 runtime_snapshot_Dragon_HOLD_records=runtime_holds,runtime_snapshot_Dragon_HOLD_count=len(runtime_holds),
 current_cold_original_source_pins=actual_cold_source_pins,
 archive_policy='All current production archives, complete namespace snapshots, R64 snapshot/runtime/protocol inheritance and unproven unique tar/zip contents HOLD. No production archive is a candidate. Previously retired rehearsal tar remains governed by seventh reconstruction mapping.',
 unique_legacy_XSM_large_rows_not_approved=large_legacy,
 unique_legacy_policy='Large old final/closed/state XSM are not selected merely for age. This branch supplies only byte-equal working inputs, keeps outputs/primary snapshots and leaves any broader unique intermediate retirement to Root with original source/result/recipe proof.',
 preserved_results_and_recipe_documents=list(source_documents.values()),prior_cleanup_result_pins=prior_results,
 prior_eight_actual_retired_paths_count=len(retired),all_selected_prior_actual_deletion_overlap_zero=True,
 restore_requirements=['Save this exact candidate-primary SHA/length map and original unmodified metadata before any deletion.',
                       'Restore all selected old working paths from retained primaries before generic old recipe/whole manifest/replay; no old seal is rewritten and no historical full replay is claimed after retirement.',
                       'Five unsealed map4-6 working copies have no independent original candidate result manifest. Evidence is fresh full equality plus retained local source/logs; Root must retain this distinction in final manifest/report.',
                       'Failed sensitivity original input manifests use the original temporary run paths for these copies. Same SHA/end-name mapping is provenance, not falsely a current absolute-path original binding. Preserve its genuinely failed outputs and receipt bytes.'],
 fresh_all_project_symlinks=dict(count=len(links),zero_selected_inbound=True,regular_count=regular_count,directory_count=dir_count),
 initial_review_harness_failure=dict(chunk_id='c7a054',exit_code=1,cause='Existing cold records are dictionaries, not strings. Fixed only this readonly TMP harness to collect absolute fields; no candidate content hash or business action ran in that failed attempt.',record=str(OUT/'initial_harness_schema_failure.json')),
 all_fresh_pins=list(PINS.values()),files_deleted=0,ART_or_formal_source_written=False,
 business_import_API_constructor_PREP_RUN_solver_restore_or_native_executed=False,new_RSS_or_scientific_credit=False,
 limits=['No fresh business API/current canonical union verification is run. V8 wire graph is only read as standard JSON metadata and hashed; no varint/business helper is imported.',
         'All eight selected candidates and eight primaries receive new full SHA reads and stable lstat; archive HOLD assessment uses metadata and current closure, not full archive reconstruction or execution.',
         'Candidate report is not independent final-union preflight or actual cleanup completion. Root must bind the latest complete protection closure, nonselected baseline and exact fresh preflight before deletion.'])
raw=(json.dumps(summary,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();(OUT/'REPORT.json').write_bytes(raw)
linkraw=(json.dumps(links,indent=2,allow_nan=False)+'\n').encode();(OUT/'fresh_symlink_inventory.json').write_bytes(linkraw)
print(json.dumps(dict(status=summary['status'],report=str(OUT/'REPORT.json'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),exact_count=8,allocated_bytes=summary['allocated_bytes'],allocated_GiB=summary['allocated_GiB'],archive_HOLD_count=len(archive_rows),fresh_pins=len(PINS),links=len(links),unique_legacy_large_HOLD=len(large_legacy))))
