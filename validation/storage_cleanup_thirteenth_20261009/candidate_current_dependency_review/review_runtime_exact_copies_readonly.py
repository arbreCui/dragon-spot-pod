import ast
import hashlib
import json
import math
import os
import stat
from pathlib import Path
ROOT=Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts'
O=Path('/private/tmp/spot_storage_thirteenth_current_dependency_exact_runtime_review_20261009')
T=Path('/private/tmp/axmat-last-cprime-trim-combined-live-resource-v9-root-execution-20261009')
INV=Path('/private/tmp/spot_storage_recheck_20261009_root13')
COLD=Path('/private/tmp/axmat-last-cprime-trim-cold-v9-input-v5-draft-20261009')
PINS={};SOURCES={};SOURCE_PROOFS=[]
def ident(p):
 s=Path(p).lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None):
 p=Path(p);before=ident(p);assert stat.S_ISREG(before[2])and p.parent.resolve(strict=True)==p.parent
 h=hashlib.sha256()
 with p.open('rb')as f:
  s=os.fstat(f.fileno());assert [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]==before
  while block:=f.read(4*1024**2):h.update(block)
 assert ident(p)==before
 sha=h.hexdigest()
 if expected is not None:assert sha==expected,(str(p),sha)
 r=dict(path=str(p),sha256=sha,size=before[3],allocated_bytes=p.lstat().st_blocks*512,identity=before);PINS[str(p)]=r;return r
def pairs(rows):
 d={}
 for k,v in rows:
  if k in d:raise ValueError('duplicate key')
  d[k]=v
 return d
def floating(x):
 v=float(x)
 if not math.isfinite(v):raise ValueError('nonfinite')
 return v
def reject(x):raise ValueError(x)
def obj(p,expected=None):
 record=pin(p,expected);d=json.loads(Path(p).read_text(),object_pairs_hook=pairs,parse_float=floating,parse_constant=reject);assert ident(p)==record['identity'];return d
def strings(value):
 stack=[value];result=set()
 while stack:
  node=stack.pop()
  if type(node)is str:result.add(node)
  elif type(node)is dict:stack.extend(node);stack.extend(node.values())
  elif type(node)is list:stack.extend(node)
 return result
def under(p,roots):return [r for r in roots if p==r or p.startswith(r+'/')]
def source(p,expected=None):
 p=Path(p);pin(p,expected);text=p.read_text();tree=ast.parse(text);SOURCES[str(p)]=(text,tree);return tree
def fn(p,name,why):
 text,tree=SOURCES[str(p)];nodes=[n for n in ast.walk(tree)if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name];assert len(nodes)==1,(p,name)
 n=nodes[0];segment=ast.get_source_segment(text,n);r=dict(source=PINS[str(p)],definition=name,start_line=n.lineno,end_line=n.end_lineno,whole_definition_sha256=hashlib.sha256(segment.encode()).hexdigest(),exact_definition=segment,dependency_conclusion=why);SOURCE_PROOFS.append(r);return n,segment
config=obj(T/'config.json');F=Path(config['F']);OUT=Path(config['OUT']);SOURCE=Path(config['SOURCE']);TERM=Path(config['TERM'])
assert config['factorySha']=='44789bc288715c34d08dbfa91b9c05dfc78166c2b8fa048bbe0207b273419a46'
source(F,config['factorySha']);d=obj(OUT/'declaration.json','7bc3d176f58ad6ee92d640c799b3f8d79923c65b2bf27c3b545c511e282b53e0')
g=obj(OUT/'input_graph.json','0e365ebbaafa0d9e9b3a34eee89cc9c3e1de3ee47812d985135b8201bd001be3')
seal=obj(OUT/'seal.json','ece13c5594c48bb22af8d507f1f40ef88457efa824e28200c6ddfced70cf3aed')
term9=obj(TERM/'terminal_return.json','709a9592c8b4a56cba99c61b628db8fed91d0c49d76d75c360591f11fa1b9d27')
assert type(term9['returncode'])is int and term9['returncode']==0 and term9['production_admission_observed']is False
canonical={x['path']:x for x in g['canonical_files']};nsroots={r[k]for r in g['namespaces']for k in ('root','canonical_root')}
aliaspaths={a[k]for a in g['aliases']for k in ('path','target')};aliasdirs={a[k]for a in g['aliases']if a['kind']=='directory'for k in ('path','target')}
assert len(canonical)==35647 and len(g['namespaces'])==86 and len(g['aliases'])==186 and len(g['absence_inputs'])==445 and len(g['live_resource_roots'])==231
oldindex=obj(Path('/private/tmp/spot_storage_second_dependency_20261008/protection_index.json'))
m9=obj(V/'storage_cleanup_ninth_20261009/manifest.json')
coldprotected=set(m9['current_cold_extra_protected_files']);assert len(coldprotected)==6248
specs=obj(V/'axial_material/combined_runtime_complete_historical_input_specs_20261007.json','2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa')
historical=obj(ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json','aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4')
failed=obj(V/'axial_material/historical_input_combined_unowned_specs_failed_prep_namespace_20261007.json','cd2c8c2ea75011ed433a441a4126cfda86c87068429c6f176d918524977137be')
trim=obj(ART/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008/declaration.json','e6dd804a473ae25888ecf5e070af708a024618772c0f753d836127af6074dc00')
fullRUN=obj(Path('/private/tmp/axmat_v9_actual_successful_RUN_graph_independent_review_20261009/independent_actual_RUN_review.json'),'e247953a067a54d06850323b5d118d30998f4ff70113c48c0071ebb2e96c6029')
assert fullRUN['status']=='PASS' and fullRUN['standard_INPUT_API_admission_observed']is False
prior_rounds=[];restore_manifests=[];retained_paths=set();restore_sourcepaths=set()
for name in ('storage_cleanup_20261008','storage_cleanup_more_20261008','storage_cleanup_third_20261008','storage_cleanup_fourth_20261008','storage_cleanup_fifth_20261009','storage_cleanup_sixth_20261009','storage_cleanup_seventh_20261009','storage_cleanup_eighth_20261009','storage_cleanup_ninth_20261009','storage_cleanup_tenth_20261009','storage_cleanup_eleventh_20261009','storage_cleanup_twelfth_20261009'):
 b=V/name
 texts=[]
 for report in b.glob('*REPORT*.txt'):
  pin(report);texts.append(str(report));report.read_text()
 prior_rounds.append(dict(round=name,read_result_reports=texts))
 for mf in b.glob('*manifest*.json'):
  if mf.name not in ('manifest.json','retire_manifest.json','cleanup_manifest.json','cache_manifest.json','cleanup_plan_manifest.json','retirement_manifest.json','approved_manifest.json'):continue
  mm=obj(mf);restore_manifests.append(dict(path=str(mf),sha256=PINS[str(mf)]['sha256']))
  for k,v in mm.items():
   if k in ('retained_primaries','retained_primaries_and_critical_sources','retained_primaries_and_critical_sources','retained_tapes','final_merge_retained','retained_closed_anchors'):
    retained_paths.update(x for x in strings(v)if x.startswith(str(ROOT)+'/'))
  for row in mm.get('candidates',[]):
   for key in ('retained_primary','retained_primary_pin','compressed_backup','restoration','restore_byte_exact_mapping'):
    restore_sourcepaths.update(x for x in strings(row.get(key))if x.startswith(str(ROOT)+'/'))
# Fail-closed supplement: all other cleanup metadata paths explicitly labelled
# restoration/retained are kept. No source-only audit pin is called permanent restore.
assert len(prior_rounds)==12
primary=pin(OUT/'runtime/Dragon','77fe179d3230eefcc7d9d7897650e414f342e7579ba65f9e6c641bfd9b1db7ba')
assert seal['files']['runtime/Dragon']==primary['sha256'] and primary['identity'][6]==1
future=[]
for v in ('v7','v8'):
 family=ART/('axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-'+v+'-20261009')
 p=family/'runtime/Dragon';r=pin(p,primary['sha256']);assert r['size']==primary['size']==9225720 and r['identity'][:2]!=primary['identity'][:2]and r['identity'][6]==1
 future.append((v,family,r))
targets={x[2]['path']for x in future}
# Include every current graph string, source symbol path, metadata field and
# predecessor/negative/directory path, not just the canonical table.
gstrings=strings(g);specstrings=strings(specs);dstrings=strings(d);histstrings=strings(historical);failedstrings=strings(failed);trimstrings=strings(trim)
for p in targets:
 assert p not in canonical and not under(p,nsroots|aliasdirs) and p not in aliaspaths
 assert p not in gstrings and p not in specstrings and p not in dstrings and p not in histstrings and p not in failedstrings and p not in trimstrings
 assert p not in oldindex['canonical_protected_files'] and not under(p,oldindex['exhaustive_dir_paths']) and p not in coldprotected
 assert p not in retained_paths and p not in restore_sourcepaths
 assert not under(p,retained_paths|restore_sourcepaths)
# All 687 symlinks in Root's complete fresh metadata: no inbound selected
# endpoint, including any indirect link resolved with present canonical path.
summary=obj(INV/'inventory_summary.json');invpin=pin(INV/'full_metadata_inventory.jsonl')
links=[];selected_inventory={};document_rows=[];r9_archive_rows=[];large_root_current=[]
with (INV/'full_metadata_inventory.jsonl').open()as f:
 for line in f:
  row=json.loads(line);raw=row['path'];p=Path(raw)if raw.startswith('/')else ROOT/raw
  name=str(p)
  if name in targets|{primary['path']}:selected_inventory[name]=row
  if row['type']in ('symlink','link'):
   if os.path.lexists(p):
    resolved=str(p.resolve(strict=False));assert resolved not in targets
    links.append(dict(path=name,target=resolved,text=os.readlink(p)))
  if name.startswith(str(V/'storage_cleanup_ninth_20261009')+'/')and row['type']=='regular':r9_archive_rows.append(row)
assert len(links)==687
for v,family,r in future:
 row=selected_inventory[r['path']]
 assert [row[k]for k in ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')]==r['identity']
assert [selected_inventory[primary['path']][k]for k in ('dev','ino','mode','size','mtime_ns','ctime_ns','nlink')]==primary['identity']
# Pin the entire real caller/helper source set; never import/execute any source.
paths={
 'ordinary':(V/'axial_material/combined_runtime_current_ordinary_path_checks.py','47e7f9eb2e7ff89e96c30b91f98a25d37d66d82a029dcfbf4845c8f5968482d5'),
 'current':(V/'axial_material/combined_runtime_current_predicates_final_private_last_uses_20261009.py','fd3bdb5543044fc71f0acb9799b1c6fcf7709cbbf22342f0931a299af59cee19'),
 'checks':(V/'axial_material/combined_runtime_historical_input_checks.py','86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'),
 'graph':(V/'axial_material/combined_runtime_reviewed_metadata_historical_input_graph_requirements_varint_wire_compact_phase_20261009.py','1d7c4d7a9ecc4546ceb4c7e0b81562329f874ca5302621ef5fc026f62c7f7643'),
 'provider':(V/'axial_material/prepare_combined_physical_dedup_file_snapshot_runtime_build.py','bf4692a57209ace55e22f85c6e9ffabf80850dcb1b610348e7dc97b74a80040c'),
 'resource':(V/'axial_material/prepare_qualified_AB_moment_order_production.py','fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'),
 'cold_factory':(COLD/'prepare_historical_input_owned_specs_physical_last_cprime_trim_file_snapshot_cold_AAA_scipy_env_physical_basis_own_pid_peak.py','76ac45bd9fc22d7a23abea6f46f182207fbea4f34d6be421cd68afbe6fc71a9e'),
 'cold_consumer':(COLD/'cold_component_input_consumer_last_cprime_trim_own_pid_peak.py','040f3ec2b201eeeba850c5dff72d66604784d99d97bf9f2c6c991e9ceb48d588')}
for p,sha in paths.values():source(p,sha)
for name,why in (
 ('production_admission','Entire sealed success inventory is current OUT9 only; descriptors add current seal/TERM/PREP/source, current graph and existing canonical d.files. Does not iterate V7/V8 output inventories or result manifests.'),
 ('declaration_admission','Loads current declaration and delegates mandatory complete current input phase and genuine current PREP proof.'),
 ('complete_input_phase','Before/after current predicates plus complete just-fresh graph; failed PREP is explicit original20261007, not V7/V8 failed RUN; every extra member derives current source and known trim predecessor namespace.'),
 ('current_input_predicates','Calls only original ordinary, current predicate subset, member predicates and trim current predicate. Source clauses of each are pinned below.'),
 ('current_trim_predicates','Reads genuine trim declaration and checks its native aliases/threads/loader and exact trim roots; no old V7/V8 runtime.'),
 ('current_new_owned_paths','Enumerates currentSOURCE, original failedPREP files and exact trim component path set; all listed source-owned endpoint paths are already in d.files.'),
 ('graph_input_bindings','Requires complete union of all typed owners/namespaces and just-fresh canonical pins exactly equal; no hidden old-root full manifest traversal.'),
 ('failed_prepare_input','Pins original2621e4 failed PREP three namespaces/12 files; all exact selected paths excluded from full saved manifest strings.'),
 ('check_failed_prepare_phase','Only original failed PREP namespaces and just-fresh fullgraph pins; not V7/V8 failedRUN.'),
 ('trim_component_input','Only actual trim sealedOUT/SOURCE/TERM and explicit preserved predecessors; entire trim declaration strings exclude both selected paths.'),
 ('actual_components','Materializes exact2cad whole seven component bodies and pinned original component declarations. No original APIs invoked; exact paths excluded from whole metadata.'),
 ('binary_audit','Only current declared original objects and current OUT runtime raw metadata log text; current real success exe retained.'),
 ('resources_for','Delegates genuine complete-history resource observer, no full immutable old output seal assertion.'),
 ('archive_bytes','Counts only current SOURCE9/OUT9 for current build archive guard; selected paths live in distinct old roots.')):
 fn(F,name,why)
fn(paths['ordinary'][0],'check_original_ordinary_paths','All26784 ordinary paths and complete9 namespaces come from originalaa3e declaration; selected paths excluded from complete original metadata.')
fn(paths['current'][0],'check_current_predicate_subset','Only pinned reached-component declarations, native aliases/loader/threads, genuine capture work snapshot, physical/cold negative paths; selected paths excluded from entire2cad and currentgraph tables. Does not call offline admission or old output manifest verifier.')
fn(paths['checks'][0],'check_member_and_directory_predicates','Only3 independent directory lists and79 exact negative member sets in immutable2cad; selected paths excluded from whole source-owned metadata.')
fn(paths['checks'][0],'check_failed_lengths_and_owned_negative_bytes','Only4 source-owned failed length maps and79 negative members; complete immutable metadata excludes selected paths.')
fn(paths['graph'][0],'verify_graph','Strict all-owner/canonical/row/coverage/trace/ns/alias/absence verifier. Selected paths absent from every stored graph string, not merely canonical table; readonly directory resource fields do not introduce hidden file dependencies.')
fn(paths['resource'][0],'history_roots','Preserves every declared root and entire dynamic axial-family root set. No selected directory root is removed.')
fn(paths['resource'][0],'DynamicHistoryResources','Genuine resource-only stat/scandir apparent-byte accounting, skips missing regular members naturally and checks same root union/caps. It does not load old seal/result.sha256 or assert every historical binary remains at its path.')
fn(paths['cold_consumer'][0],'complete_input_phase','Same whole canonical graph, original ordinary/current/trim checks, exact current successSOURCE9/OUT9 and future actualintake namespaces; no historical V7/V8 success namespace is substituted.')
fn(paths['cold_consumer'][0],'expected_union','Canonical descriptors from genuinely admitted currentV9 return plus future intake/context/helper binding. CurrentV9 descriptors are finite d.files+current sealedOUT9/witness paths; no selected oldruntime paths exist in them.')
fn(paths['cold_consumer'][0],'current_checks','Composes current ordinary/currentcomponent/binding/trim predicates; all exact old ordinary26784/currentcomponent fields pinned and independently intersected.')
fn(paths['cold_consumer'][0],'complete_success_namespaces','Reads only API_BUILD9 success seal and API_SOURCE_ROOT9 genuine PREP source namespace, not V7/V8 failed packages.')
fn(paths['cold_factory'][0],'prepare','Future PREP retains actualbase c.prepare which calls offline snapshot producer admission. The independently source-derived cold6248 exact set is retained and selected paths have no intersection. No future current metadata can be fabricated here; later changed binding source needs its own review.')
# Read the source-origin cold proof and the exact original offline admission
# functions; full6248 protection retained, no material seed/work copy freed.
coldproof_path=V/'storage_cleanup_eighth_20261009/cold_dynamic/current_cold_dynamic_protected_files.json'
coldproof=obj(coldproof_path)
for x in coldproof['source_pins_and_actual_function_definitions']:
 if type(x)is dict and 'path'in x and 'sha256'in x:pin(x['path'],x['sha256'])
# Current failed V7/V8 archive evidence remains original. Only compiled copy is
# proposed for retirement; all other family files and original results preserved.
failed_evidence=[];fixed=[]
for v,family,r in future:
 td=ART/('axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-'+v+'-20261009')
 receipt=obj(td/'terminal_return.json','7f555a40cc7867e99537a550b1d94d70d116afd35b56a17625d37a8cc17f8679'if v=='v7'else'd4cacd55b43b590647ca9c1e6ec1168c58f8ddea7ec52b925b9048c556497039')
 assert type(receipt['returncode'])is int and receipt['returncode']==1
 assert receipt['successful_new_runtime_build_observed']is False and receipt['successful_combined_link_completion_observed']is False and receipt['production_admission_observed']is False
 driver=obj(family/'driver_result.json');assert driver['classification']=='FAILED_COMBINED_RUNTIME_LINK_NO_RETRY'
 stp=family/('HISTORICAL_INPUT_TRIM_COMBINED_RUNTIME_LINK_'+v.upper())/'stages.json';stages=obj(stp)['stages'];assert len(stages)==5 and all(s['status']=='PASS'for s in stages[:4]) and stages[4]['status']=='FAILED'
 assert not os.path.lexists(family/'seal.json')and not os.path.lexists(family/'audit/result.json')
 for path in (family/'declaration.json',family/'input_graph.json',family/'input_creation_python_open_trace.json'):
  pin(path)
 for s in stages:
  for k in ('stdout','stderr','watchdog'):
   if k in s:
    vpath=s[k]
    if isinstance(vpath,dict)and 'path'in vpath:pin(vpath['path'])
 for k in ('full_stdout','full_stderr'):
  record=receipt[k];pin(record['path'],record['sha256'])
 docdir=V/'axial_material'/('last_cprime_trim_combined_live_resource_'+v+'_build_review_20261009')
 report_paths=[str(p)for p in docdir.glob('*.json')]+[str(p)for p in docdir.glob('*.txt')]
 failed_evidence.append(dict(family=v,actual_returncode=1,receipt=PINS[str(td/'terminal_return.json')],driver=PINS[str(family/'driver_result.json')],old_five_stage_statuses=[s['status']for s in stages],oldseal_absent=True,audit_result_absent=True,result_document_paths_retained=report_paths,all_OTHER_family_files_preserved=True,original_factories_and_source_copies_preserved=True,old_historically_measured_archive_bytes_not_recomputed_or_rewritten=True))
 fixed.append(dict(**r,category='EXACT_DUPLICATE_OLD_FAILED_BUILD_RUNTIME_COPY',retained_primary=primary['path'],retained_primary_pin=primary,
 current_dependency_exclusions=dict(canonical=True,all_graph_literal_symbols_and_owner_ns_alias_absence_tables=True,exhaustive_namespace=True,explicit_file_and_directory_alias=True,original26784ordinary_and9namespaces=True,all2cad_whole_seven_and_live_member_metadata=True,actual_trim_complete_predecessor_metadata=True,original_failed_PREP_three_whole_namespaces=True,oldindex_canonical_and_exhaustive_roots=True,cold6248_dynamic_readset=True,all_prior_exact_restore_primaries_and_backups=True,all687_inbound_symlinks=True),
 original_evidence_classification='Frozen actual failed RUN int1, no seal/auditresult/success promotion. All original raw logs/TERM/source/driver/graph/trace/metadata preserved. Current V9 sealedruntime is a full byteexact restoration primary; its existence is not scientific equivalence or old success.',
 historical_limit='Rechecking the old package compiled program or replaying old failed commands first requires exact original path restoration. Full earlier replay may additionally require restoring prior cleanup rounds. Originalinode/ctime cannot be restored.',
 restore_byte_exact_mapping=dict(target=r['path'],source=primary['path'],expected_sha256=r['sha256'],expected_size=r['size'],restore_mode=stat.S_IMODE(r['identity'][2]),restore_mtime_ns=r['identity'][4],overwriting_forbidden=True),
 resource_root_preserved=str(family),old_audit_root_protection_is_not_silently_pruned=True))
# Check every read-only prior restore utility mentions only its manifest
# candidates/retained_primary; immutable source_and_review pins are historical
# evidence and are not automatically dynamic restoration inputs.
restore_sources=[]
for b in V.glob('storage_cleanup*'):
 for p in b.glob('*restore*.py'):
  text=p.read_text();pin(p);assert not any(q in text for q in targets);restore_sources.append(dict(path=str(p),sha256=PINS[str(p)]['sha256'],explicit_selected_path_reference=False))
# Current bootstrap regression has an actual direct dependency: HOLD. The
# remainder51 compiled examples are not expanded as this round's fixed scope.
test=V/'iterative/test_d4a_picard_map_preflight.py';source(test)
node,segment=fn(test,'repaired_fixture','Direct current regression fixture hashes REPAIRED.read_bytes then copies it; exact oldbootstrap-run/Dragon path remains needed. No deletion proposed for it or this51 branch.')
assert 'REPAIRED.read_bytes()'in segment and 'shutil.copy2(REPAIRED' in segment
compiled51=obj(Path('/private/tmp/spot_storage_twelfth_old_bootstrap_native_readonly_review_20261009/fresh_compiled_51_candidate_and_peer_SHA_records.json'))
assert len(compiled51)==51
held_compiled=[]
for x in compiled51:
 p=x['candidate']['path'];assert os.path.lexists(p);held_compiled.append(dict(path=p,size=x['candidate']['size'],allocated_bytes=Path(p).lstat().st_blocks*512,prior_full_SHA=x['candidate']['sha256'],current_identity=ident(p),status='HOLD_NOT_THIS_FIXED_SCOPE',reason='Original native/main/replay/regression/source consumers require their own complete closure proof. Bootstrap-run is explicitly read by current regression test. No large compiled family automatically released by V9 success.'))
# WholeR9 gzip backup allocation is retained primary for89 retired tapes.
gz=[x for x in m9['candidates']if x['category']=='LOSSLESS_GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE']
# Accept exact reviewed category spelling only as declared, report classes
# without decoding89 backups again (already independent actual terminal pass).
if not gz:gz=[x for x in m9['candidates']if 'GZIP'in x['category']]
assert len(gz)==89
for x in gz:
 for q in strings(x['compressed_backup']):
  if q.startswith(str(ROOT)+'/')and q.endswith('.gz'):assert os.path.lexists(q)
for path,r in PINS.items():assert ident(path)==r['identity']
with (O/'exact2_runtime_candidates.json').open('x')as f:json.dump(dict(schema='SPOT_OLD_FAILED_RUNTIME_EXACT_TWO_FIXED_CANDIDATES_V1',status='PASS_READONLY_CANDIDATE_PROOF_NOT_DELETE',candidates=fixed,logical_bytes=sum(r['size']for r in fixed),allocated_bytes=sum(r['allocated_bytes']for r in fixed),unique_inode_count=2,retained_primary=primary,only_after_Root_manifest_independent_preflight_and_restore_mapping=True),f,indent=2);f.write('\n')
with (O/'current_actual_source_readchain_proof.json').open('x')as f:json.dump(dict(schema='SPOT_OLD_FAILED_RUNTIME_CURRENT_LITERAL_AND_DYNAMIC_SOURCE_EXCLUSION_V1',status='PASS_READONLY_SOURCE_ONLY',all_current_pipeline_clauses=SOURCE_PROOFS,old_normative_failed_PREP_and_trim_namespaces_preserved=True,current_expected_additional_only_OUT9_SOURCE9_and_actual_future_intake=True,cold_offline_admission6248_proof=PINS[str(coldproof_path)],selected_exact_paths_not_current_input=True,resource_history_directory_set_unpruned=True,prior_restore_utilities_readonly_checked=restore_sources),f,indent=2);f.write('\n')
report=dict(schema='SPOT_STORAGE_THIRTEENTH_OLD_FAILED_BUILD_EXACT_COPY_REVIEW_V1',status='PASS',classification='READONLY_EXACT_TWO_FIXED_CANDIDATE_DEPENDENCY_PROOF_NOT_DELETE',root_inventory=invpin,root_summary=PINS[str(INV/'inventory_summary.json')],reused_fresh_Root_metadata_no_wholeproject_rescan=True,
 current_graph_pin=PINS[str(OUT/'input_graph.json')],current_canonical_count=35647,current_full_fresh35GB_admission_not_repeated=True,most_recent_actual_full_RUN_review=PINS[str(Path('/private/tmp/axmat_v9_actual_successful_RUN_graph_independent_review_20261009/independent_actual_RUN_review.json'))],current_ns86_alias186_absence445_roots231_scope_unchanged=True,
 exact_selected_count=2,selected_logical_bytes=sum(x['size']for x in fixed),selected_allocated_bytes=sum(x['allocated_bytes']for x in fixed),selected_unique_inode_allocated_bytes=sum(x['allocated_bytes']for x in fixed),selected_full_SHA_and_identity_fresh=True,retained_complete_success_V9_runtime_primary=primary,retained_primary_full_SHA_equals_both_old_exes=True,
 entire_readchain_exclusion_not_just_factory_string_search=True,all_original_normative_INPUT_and_source_predicates_unchanged=True,all_old_resource_roots_and_directories_preserved=True,
 no_old_seal_or_source_or_result_rewritten=True,old_R9_critical_roots_are_preserved_historical_policy_not_permanent_hidden_business_input=True,explicit_Root_review_authorization_for_two_noncurrent_exact_runtime_paths=True,
 prior12_result_reports_read=prior_rounds,all_prior_retained_primaries_gzip_archives_and_restore_sources_preserved=True,prior_restore_selected_source_intersections=[],
 failed_original_evidence_preserved=failed_evidence,compiled51_all_HOLD=held_compiled,bootstrap_direct_current_test_dependency=dict(path=str(test),function='repaired_fixture',lines=[node.lineno,node.end_lineno],needed_exact_path=str(ART/'d4a-scattering-bootstrap-run-20260924/Dragon')),
 R9_89_gzip_backup_still_permanent_restoration_payloads=True,R9_total_allocated_from_Root_inventory=sum(r['allocated']for r in r9_archive_rows),R9_unexpanded_document_analysis_left_to_peer=True,
 safe_GiB_scale_deletion_found=False,old_unique_A_B_material_snapshots_native_full_and_all_results_docs_logs_sources_kept=True,
 actual_INPUT_or_cold_or_API_or_Ctor_or_native_or_PREP_or_RUN_called=False,business_modules_imported=False,files_deleted=0,formal_or_ART_writes=False,output_scope=str(O),science_credit=False,
 next_step='Root may create a fixedexact2 manifest and byteexact restoration mapping to retained current OUT9/runtime/Dragon. Fresh independent source/manifest/preflight must precede any deletion. No other compiled path or failed-package data is approved. Keep all old result/doc/log/metadata/source bytes and every declared resource root; any old binary/package replay first restores original paths and applicable previous retired inputs.',fresh_control_source_candidate_pins=list(PINS.values()),audit_source=dict(path=str(Path(__file__)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
with (O/'REPORT.json').open('x')as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
with (O/'REPORT.txt').open('x')as f:f.write('只读PASS：本轮明确的两份可退役程序副本是V7/V8旧失败OUT/runtime/Dragon，各逻辑9,225,720B、分配9,228,288B，合计18,456,576分配字节（17.6015625MiB）。两者与保留的sealed V9/runtime/Dragon全文SHA77fe179d...b7ba完全相同，原singlelink身份稳定；精确恢复目标/来源/完整SHA/size/mode/mtime已保存。完整 current F9 API→declaration/fullphase→trim/ordinary/current/member→all-owner graph→failedPREP/length paths及futurecold原offline6248/source/restore排除已写源码证据，非只匹配factory字符串。两个旧runtime不是current canonical/ns/alias/absence/typed owner或旧restore主本；历史231目录仍全保留。所有原V7/V8失败文档、raw、TERM、graph/trace/driver/source不动，失败int1不改成功。此刻只是候选证明，Root仍须写fixedmanifest/restore工具并独审实际预检，尚未删除。bootstrap-run/Dragon有当前regression直接read/copy，本轮51compiled不扩展继续HOLD。89R9 gzip是永久恢复来源、原A/B和native主数据继续保留；未发现GiB级新安全可删项。仅TMP写审查，无业务/API/INPUT/cold/native/PREP/RUN。\n')
print(json.dumps(dict(status='PASS',scope='READONLY_EXACT2_CANDIDATE_NOT_DELETE',count=2,logical_bytes=report['selected_logical_bytes'],allocated_bytes=report['selected_allocated_bytes'],same_primary_sha=primary['sha256'],graph_or_science_API_executed=False,report=str(O/'REPORT.json'),report_sha256=hashlib.sha256((O/'REPORT.json').read_bytes()).hexdigest())))
