from pathlib import Path
import ast, datetime, hashlib, json, os, re, stat, subprocess

OUT=Path('/private/tmp/spot_ninth_old_compensated_intermediate_independent_review_20261009');OUT.mkdir(exist_ok=True)
ROOT=Path('/Users/wen/spot');V=ROOT/'validation';ART=V/'artifacts';A=V/'axial_material'
FAMILY=ART/'axial-material-production-qualified-AB-compensated-20261004'
V8=ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v8-20261009'
PROPOSAL=Path('/private/tmp/spot_ninth_storage_review_20261009/root_old_compensated_intermediate_proposal.json')
PINS={}
def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink]
def pin(p,expected=None,retain=False):
 p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not stat.S_ISLNK(s.st_mode)
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW);h=hashlib.sha256();size=0;blocks=[]
 try:
  assert identity(os.fstat(fd))==identity(s)
  while True:
   raw=os.read(fd,8*1024*1024)
   if not raw:break
   h.update(raw);size+=len(raw)
   if retain:blocks.append(raw)
  assert identity(os.fstat(fd))==identity(s)
 finally:os.close(fd)
 assert identity(p.lstat())==identity(s) and size==s.st_size
 if expected:assert h.hexdigest()==expected,(str(p),h.hexdigest(),expected)
 info=dict(path=str(p),sha256=h.hexdigest(),size=size,allocated_bytes=s.st_blocks*512,identity=identity(s),fresh_full_SHA=True)
 PINS[str(p)]=info
 return (info,b''.join(blocks))if retain else info
def jp(p,expected=None):return json.loads(pin(p,expected,True)[1])
def preserved_member_pin(p,wanted):
 p=Path(p);s=p.lstat()
 if stat.S_ISREG(s.st_mode):return pin(p,wanted)
 assert stat.S_ISLNK(s.st_mode),'original member has unsupported kind'
 text=os.readlink(p);target=p.resolve(strict=True);actual=pin(target,wanted)
 assert identity(p.lstat())==identity(s) and os.readlink(p)==text and p.resolve(strict=True)==target
 info=dict(path=str(p),kind='PRESERVED_ORIGINAL_SYMLINK_MEMBER',sha256=wanted,size=actual['size'],
           identity=identity(s),literal_link_text=text,canonical_target=actual,fresh_full_target_SHA=True)
 PINS[str(p)]=info
 return info
def absolute_paths(o):
 result=set();todo=[o]
 while todo:
  x=todo.pop()
  if isinstance(x,str):
   if x.startswith('/'):result.add(x)
  elif isinstance(x,dict):todo.extend(x.keys());todo.extend(x.values())
  elif isinstance(x,list):todo.extend(x)
 return result
def within(path,roots):return [r for r in roots if path==r or path.startswith(r.rstrip('/')+'/')]

proposal=jp(PROPOSAL,'120c4e0fc45fc97dc042907a64f461298c29adc5b4bad9529d46e24112233eb3')
assert len(proposal['candidates'])==9 and len(proposal['retained_closed_anchors_and_stage_documents'])==80 and len(proposal['source_and_review_pins'])==7
expected_paths={str(FAMILY/'AAA'/('map%03d'%i)/name)for i in(1,2,3)for name in('candidate_radial.xsm','candidate_snapshots.xsm','projected_proposal.xsm')}
actual_paths={row['path']for row in proposal['candidates']};assert actual_paths==expected_paths
manifest=jp(V/'storage_cleanup_eighth_20261009/manifest.json','dcc76b4a6f6cdacd52edcaf004d206d64018f0d7b72b4f9e303e1aacf8529e8a')
graph=jp(V8/'input_graph.json','242e995536b1b1cb92a03a16dd7936814f646ea6c02d486c71b6e8e2fb5d9044')
decl=jp(V8/'declaration.json','3c7f3c1fc8f5ce73b15136442df2622aa30538c4f7806abf8f2fddd1da7387ae')
oldindex=jp(manifest['old_index_pin']['path'],manifest['old_index_pin']['sha256'])
cold=jp(V/'storage_cleanup_eighth_20261009/cold_dynamic/current_cold_dynamic_protected_files.json','11f9f07e92ca6c11ccb90ed4bf58b9d98a0e726bf2893a40e457c32edbc9e161')
COLD_R=A/'last_cprime_trim_combined_live_resource_v8_build_review_20261009/next_cold_input_readonly_integrity_review'
required=jp(COLD_R/'derived_required_path_SHA_owners.json')
actual_sources=jp(COLD_R/'actual_source_pins_and_function_definitions.json')
graph_paths=absolute_paths(graph);old_paths=absolute_paths(oldindex)
cold_paths=set(manifest['current_cold_extra_protected_files'])|absolute_paths(cold['current_cold_dynamic_protected_files'])
required_paths=absolute_paths(required)
for path in expected_paths:
 assert path not in graph_paths and path not in old_paths and path not in cold_paths and path not in required_paths
 assert not within(path,manifest['critical_roots']) and not within(path,[x['root']for x in graph['namespaces']])
 # The family remains an unfiltered directory-only resource scope. Retiring
 # exact leaves does not remove that root or weaken its original budget.
 assert within(path,graph['live_resource_roots'])==[str(FAMILY)]
assert graph['live_resource_roots']==sorted(decl['resource_roots']) and len(graph['live_resource_roots'])==228
retired=set()
for d in sorted(V.glob('storage_cleanup_*')):
 p=d/'retirement_ledger.jsonl'
 if p.exists():
  raw=pin(p,retain=True)[1]
  for line in raw.splitlines():
   if not line:continue
   row=json.loads(line);key=row.get('path')or row.get('candidate',{}).get('path');assert key;retired.add(key)
assert not expected_paths&retired

original_documents={}
for row in proposal['source_and_review_pins']:
 v=jp(row['path'],row['sha256']);assert PINS[row['path']]['identity']==row['identity'];original_documents[row['path']]=v
status=original_documents[str(FAMILY/'AAA/run_status.json')]
assert status['classification']=='WAITING_REFERENCE' and status['cases']['AAA']['classification']=='VALID_MET'
assert status['completed_maps']==status['cases']['AAA']['completed_maps']==4
assert status['cases']['AAA']['final_directory']==str(FAMILY/'AAA/map004')
assert [x['classification']for x in status['cases']['AAA']['maps']]==['VALID_NOT_MET']*3+['VALID_MET']
results={i:original_documents[str(FAMILY/'AAA'/('map%03d'%i)/'result.json')]for i in (1,2,3)}
for i in(1,2,3):assert results[i]['classification']=='SEALED_STAGE_OUTPUTS'
candidate_records=[]
for row in proposal['candidates']:
 path=Path(row['path']);i=int(path.parent.name[3:]);proof=row['historical_payload_proof']
 assert proof['format']=='JSON_SHA256_MAP' and proof['field']=='sha256' and proof['key']==path.name
 assert proof['path']==str(path.parent/'result.json') and proof['sha256']==PINS[proof['path']]['sha256']
 assert results[i]['sha256'][path.name]==row['sha256']
 info=pin(path,row['sha256']);assert info['identity']==row['identity'] and info['size']==row['size'] and info['allocated_bytes']==row['allocated_bytes']
 assert info['identity'][6]==1
 for ancestor in [*reversed(path.parents),path]:assert not ancestor.is_symlink()
 candidate_records.append(dict(candidate=info,original_result_proof=proof,classification='TERMINAL_OLD_INTERMEDIATE_PAYLOAD',
                                no_retained_equal_primary_asserted=True,reconstruction_not_byteidentical_promise=True))
assert sum(x['candidate']['allocated_bytes']for x in candidate_records)==proposal['allocated_bytes']==2122850304
anchors=[]
for row in proposal['retained_closed_anchors_and_stage_documents']:
 assert row['path']not in expected_paths
 info=pin(row['path'],row['sha256']);assert info['identity']==row['identity'];anchors.append(info)
anchor_paths={x['path']for x in anchors}
for i in (1,2,3,4):
 for name in ('closed_axial.xsm','closed_snapshots.xsm'):
  assert str(FAMILY/'AAA'/('map%03d'%i)/name)in anchor_paths
bootstrap=jp(FAMILY/'AAA/bootstrap/result.json')
assert bootstrap['classification']=='SEALED_STAGE_OUTPUTS'
bootstrap_pins=[]
for name,wanted in bootstrap['sha256'].items():
 info=preserved_member_pin(FAMILY/'AAA/bootstrap'/name,wanted)
 assert info['path']not in expected_paths
 bootstrap_pins.append(info)
lastmap=jp(FAMILY/'AAA/map004/result.json')
assert lastmap['classification']=='SEALED_STAGE_OUTPUTS'
for name,wanted in lastmap['sha256'].items():
 # Every final stage output is retained and independently freshly checked,
 # including final radial/snapshot/proposal files deliberately not selected.
 info=preserved_member_pin(FAMILY/'AAA/map004'/name,wanted)
 assert info['path']not in expected_paths

source_evidence=[]
for source in actual_sources:
 info,raw=pin(source['path'],source['sha256'],True);text=raw.decode();tree=ast.parse(text)
 for definition in source['definitions']:
  nodes=[n for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name==definition['name']and n.lineno==definition['line']]
  assert len(nodes)==1
  segment=ast.get_source_segment(text,nodes[0]);assert segment==definition['source']
 source_evidence.append(dict(pin=info,all_recorded_function_definitions_actual_source_exact=True,
                             functions=[dict(name=d['name'],line=d['line'],source_sha256=hashlib.sha256(d['source'].encode()).hexdigest())for d in source['definitions']]))
current_function_sources=[d['source']for s in actual_sources for d in s['definitions']]
assert any('def verify_offline_state(state):'in x and "manifest['files'].items()"in x for x in current_function_sources)
assert any('def pinned_runtime_files('in x and 'variant["files"].items()'in x for x in current_function_sources)
assert all(not any(path in x for path in expected_paths)for x in current_function_sources)

# Inspect existing compensated analysis callers: their whole-seal checks use
# the saved final map004 and bootstrap. Legacy map001--003 full re-verification
# must separately remain honest about retirement of its old numeric payload.
compensated_callers=[]
for name in ['frozen_AAA_axial_sensitivities.py','export_qualified_AAA_observables_compensated.py','assess_qualified_AAA_reference_compensated.py','audit_AAA_global_transverse_balance.py','review_qualified_AB_input_identity_compensated.py','prepare_qualified_AB_compensated_production.py','reference_transitive_input_owners.py']:
 p=A/name;info,raw=pin(p,retain=True);text=raw.decode();ast.parse(text)
 assert not any(path in text for path in expected_paths)
 excerpts=[dict(line=i+1,text=line)for i,line in enumerate(text.splitlines())if any(x in line for x in ['final_directory','verify_sealed_directory','closed_axial','closed_snapshots','map004','candidate_radial','candidate_snapshots','projected_proposal'])]
 compensated_callers.append(dict(pin=info,relevant_lines=excerpts))
controller=FAMILY/'runtime/production_runner.py';info,raw=pin(controller,retain=True);text=raw.decode();tree=ast.parse(text)
controller_functions={n.name:ast.get_source_segment(text,n)for n in tree.body if isinstance(n,ast.FunctionDef)}
assert 'verify_sealed_directory'in controller_functions
historical_seal=controller_functions['verify_sealed_directory']
assert 'result.json'in historical_seal and 'sha256'in historical_seal
source_evidence.append(dict(pin=info,original_historical_whole_stage_verifier=historical_seal,
                           source_scope='Old explicit stage checks would fail after retirement; code/results stay unchanged.'))

links=[]
for folder,dirs,names in os.walk(ROOT,followlinks=False):
 for name in dirs+names:
  p=Path(folder)/name;s=p.lstat()
  if stat.S_ISLNK(s.st_mode):links.append(dict(path=str(p),text=os.readlink(p),target=str(p.resolve(strict=False)),identity=identity(s)))
assert len(links)==687
inbound=[dict(candidate=path,link=link)for path in expected_paths for link in links if path==link['target']or path.startswith(link['target'].rstrip('/')+'/')]
assert not inbound
for path,info in PINS.items():assert identity(Path(path).lstat())==info['identity'],('end_identity_change',path)
report=dict(schema='SPOT_NINTH_OLD_COMPENSATED_NUMERIC_INTERMEDIATE_INDEPENDENT_CANDIDATE_REVIEW_V1',
 status='PASS',scope='EXACT_NINE_CANDIDATES_SOURCE_PROVENANCE_AND_READONLY_SCOPE_NOT_FINAL_UNION_PREFLIGHT_OR_DELETION',
 proposal=PINS[str(PROPOSAL)],candidate_records=candidate_records,count=9,allocated_bytes=2122850304,allocated_GiB=2122850304/2**30,
 fresh_full_candidate_SHA_matches_original_three_result_tables=True,all_singlelink_ordinary_realparent_and_stable_original_identity=True,
 original_results_and_flags=dict(run_classification='WAITING_REFERENCE',AAA_case_classification='VALID_MET',completed_maps=4,
                                 final_directory=str(FAMILY/'AAA/map004'),map001_003_classification='VALID_NOT_MET',no_new_reference_accuracy_or_science_credit=True),
 retained_closed_anchors_and_stage_documents=anchors,retained_80_full_SHA_identity_and_all_final_map004_outputs_fresh=True,
 retained_bootstrap_complete_original_result=PINS[str(FAMILY/'AAA/bootstrap/result.json')],retained_bootstrap_complete_original_members=bootstrap_pins,
 preserved_original_bootstrap_alias_members=[x for x in bootstrap_pins if x.get('kind')=='PRESERVED_ORIGINAL_SYMLINK_MEMBER'],
 full_INPUT_original_trim_current_graph_and_cold_path_exclusion=dict(V8_graph=PINS[str(V8/'input_graph.json')],V8_declaration=PINS[str(V8/'declaration.json')],
   canonical_files=35647,namespaces=86,aliases=186,unfiltered_resource_roots=228,
   exact_candidate_hits_current_graph_all_paths_oldindex_critical_namespaces_cold6248_6194_and_actual1534_zero=True,
   prior_eight_actual_ledger_overlap_zero=True,full_687_links_zero_inbound=True),
 source_dynamic_review=dict(current_next_cold_actual_sources_and_functions_fresh_exact=source_evidence,original_compensated_analysis_callers=compensated_callers,
   next_cold_verify_offline_state_execution_run_audit_protocol_material_variant_loops_kept=True,
   actual_required_path_metadata_zero_selected_hits=True,
   old_qualified_compensated_exports_assessments_frozen_sensitivity_final_map004_and_bootstrap_kept=True,
   original_lastmap4_candidate_radial_and_candidate_snapshots_and_projected_proposal_kept=True,
   resource_scope_family_and_directories_must_stay=True,
   directory_scope_note='Selected old family remains one of all 228 original live resource roots. Only numeric leaves are proposed for retirement; no directory/root/INPUT owner/path scope or original resource gate is removed.'),
 reconstruction_policy=dict(exact_primary_restore_promised=False,original_whole_map001_003_seals_will_be_incomplete_after_retirement=True,
   future_old_stage_replay_requires_numeric_rebuild=True,byteidentical_regeneration_or_success_guaranteed=False,
   all_original_SHA_and_results_receipts_sources_logs_parameters_preserved=True,
   required_result_document='Root final report/manifest must identify these nine as old unique intermediate payloads, retain their original SHA, classification and exact recipes/anchors, and state that original whole-stage replay is retired until rebuilding. Do not route them through an exact-copy restoration promise.'),
 fresh_pins=list(PINS.values()),files_deleted=0,ART_or_formal_written=False,business_API_import_constructor_PREP_RUN_or_solver_executed=False,
 native_RSS_or_scientific_credit=False,complete=False,
 initial_harness_failure=dict(initial_chunk_id='72310a',session_id=74737,terminal_chunk_id='7f8ead',exit_code=1,
   cause='Review harness assumed Root 80-anchor shortlist included bootstrap. It does not. Bootstrap was present, so the corrected readonly harness separately pins its original whole result table and every member; no project/business mutation or deletion.',
   record=str(OUT/'initial_harness_anchor_scope_failure.json')),
 second_harness_failure=dict(initial_chunk_id='fbe18c',session_id=76980,terminal_chunk_id='0e4122',exit_code=1,
   cause='Bootstrap original sealed members include two genuine symlink inputs; ordinary-only readonly harness refused them. Corrected only preserved-member handling to pin literal link identity/text plus full expected-SHA canonical target, without granting candidates aliases.',
   record=str(OUT/'second_harness_original_alias_failure.json')),
 limits=['PASS is this fixed nine-file candidate/provenance/source scope, not actual deletion or a fresh complete union preflight.',
         'Sources and JSON records are read/parsed only; no controller, verifier, reconstruction, import/API/PREP/RUN or science execution.',
         'Current closure and required reads are frozen metadata; no new business admission or full multi-GiB current INPUT phase is claimed.',
         'Arbitrary historical whole-stage checks are intentionally no longer complete after retirement. All actual old classifications and stored results remain unmodified.'],
 completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
raw=(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode();(OUT/'REPORT.json').write_bytes(raw)
print(json.dumps(dict(status=report['status'],scope=report['scope'],report=str(OUT/'REPORT.json'),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),candidates=9,allocated_GiB=report['allocated_GiB'],fresh_pins=len(PINS),links=len(links))))
