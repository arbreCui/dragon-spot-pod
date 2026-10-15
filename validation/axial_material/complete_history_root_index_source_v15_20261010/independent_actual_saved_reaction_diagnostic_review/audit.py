import ast, csv, hashlib, json, math, os, stat, time
from pathlib import Path
B=Path('/Users/wen/spot')
S=B/'validation/axial_material/complete_history_root_index_source_v15_20261010'
A=S/'actual_saved_reaction_ledger_sources'
E=S/'actual_saved_reaction_ledger_receipts'
O=B/'validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-20261010'
H=B/'validation/artifacts/axial-material-AAA-refined-all-group-source-reaction-diagnostic-host-20261010'
T=Path(__file__).parent
K=('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
def identity(s): return {k:getattr(s,k) for k in K}
def pin(p):
    p=Path(p); lb=identity(p.lstat()); tb=identity(p.stat())
    alias=os.readlink(p) if stat.S_ISLNK(lb['st_mode']) else None
    h=hashlib.sha256(); n=0
    with p.open('rb') as f:
        fb=identity(os.fstat(f.fileno())); assert tb==fb
        while True:
            block=f.read(2**20)
            if not block: break
            h.update(block); n+=len(block)
        fa=identity(os.fstat(f.fileno()))
    la=identity(p.lstat()); ta=identity(p.stat())
    alia=os.readlink(p) if stat.S_ISLNK(la['st_mode']) else None
    assert lb==la and tb==ta==fb==fa and alias==alia and n==fb['st_size']
    return dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,literal_7id_before=lb,literal_7id_after=la,target_7id_before=tb,target_7id_after=ta,fd_7id_before=fb,fd_7id_after=fa,literal_symlink_text=alias)
def check(p,sha,size=None):
    assert p['sha256']==sha,(p['path'],p['sha256'],sha)
    if size is not None: assert p['size_bytes']==size
def saved(p,s):
    check(p,s['sha256'])
    assert p['path']==s['path']
    if 'identity' in s: assert [p['literal_7id_before'][k] for k in K]==s['identity']
def load(p): return json.loads(Path(p).read_text())
m=load(O/'payload_manifest.json'); l=load(O/'layout.json'); r=load(O/'result.json'); i=load(O/'input_identities.json'); h=load(H/'result.json'); q=load(A/'Root_source_binding_proof.json')
paths={p.name:p for p in O.iterdir() if p.is_file()}
assert set(paths)==set(m['files'])|{'payload_manifest.json'}
pp={k:pin(p) for k,p in sorted(paths.items())}
for k,v in m['files'].items(): check(pp[k],v['sha256'],v['size_bytes'])
assert len(l['arrays'])==77 and len(m['files'])==82 and len(pp)==83
assert {v['file'] for v in l['arrays'].values()}=={k for k in pp if k.endswith('.bin')}
rawbytes=0
for k,v in l['arrays'].items():
    assert v['file']==k+'.bin' and v['order']=='C'
    assert math.prod(v['shape'])*{'<f8':8,'<f4':4,'<i4':4}[v['dtype']]==v['bytes']
    check(pp[v['file']],v['sha256'],v['bytes']); rawbytes+=v['bytes']
assert rawbytes==48553420 and sum(v['size_bytes'] for k,v in pp.items() if k!='payload_manifest.json')==m['payload_bytes_before_manifest']==54353509
plan=load(A/'source_only_evaluator_review/EVALUATOR_INPUTS_BUDGETS_AND_SCOPE.json')
assert set(i['before'])==set(i['after'])==set(plan['inputs']) and len(i['before'])==11
ip={}
for k,v in i['before'].items():
    assert v==i['after'][k]
    ip[k]=pin(v['path']); assert ip[k]==v
    assert plan['inputs'][k]['path']==v['path']; check(ip[k],plan['inputs'][k]['sha256'])
sp={k:pin(q[k]['path']) for k in ['READY_source','UNREADY_source','host','host_parent']}
for k,v in sp.items(): check(v,q[k]['sha256'])
assert sp['READY_source']==i['evaluator_before']==i['evaluator_after']
ub=Path(sp['UNREADY_source']['path']).read_bytes(); rb=Path(sp['READY_source']['path']).read_bytes()
assert ub.count(b"SOURCE_STATUS = 'UNREADY'")==1 and ub.replace(b"SOURCE_STATUS = 'UNREADY'",b"SOURCE_STATUS = 'READY'",1)==rb
ut=ub.decode(); rt=rb.decode()
assert ut.count("SOURCE_STATUS = 'UNREADY'")==1 and ut.replace("SOURCE_STATUS = 'UNREADY'","SOURCE_STATUS = 'READY'",1)==rt
def funcs(t): return [ast.get_source_segment(t,n) for n in ast.walk(ast.parse(t)) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
assert funcs(ut)==funcs(rt) and len(funcs(rt))==23
inverse=Path(sp['host']['path']).read_text(); inverse_bytes=Path(sp['host']['path']).read_bytes(); steps=[]
for v in reversed(q['host_finite_changes']):
    n=inverse.count(v['after']); assert n==v['occurrences'],(n,v)
    assert inverse_bytes.count(v['after'].encode())==v['occurrences']
    steps.append(dict(after=v['after'],observed_occurrences=n)); inverse=inverse.replace(v['after'],v['before']); inverse_bytes=inverse_bytes.replace(v['after'].encode(),v['before'].encode())
assert inverse==Path(sp['host_parent']['path']).read_text()
assert inverse_bytes==Path(sp['host_parent']['path']).read_bytes()
sap={str(p.relative_to(A)):pin(p) for p in sorted(A.rglob('*')) if p.is_file()}
sm=load(A/'source_only_evaluator_review/MANIFEST.json')
for k,v in sm['files'].items(): check(sap['source_only_evaluator_review/'+k],v['sha256'],v['size_bytes'])
hp={str(p.relative_to(H)):pin(p) for p in sorted(H.rglob('*')) if p.is_file()}
ep={p.name:pin(p) for p in sorted(E.iterdir()) if p.is_file()}
receipt=load(E/'Root_actual_diagnostic_tool_terminal_return.json'); stdout=load(E/'host.full_stdout.json'); log=load(H/'run/admit.log'); w=load(H/'run/admit.watchdog.json'); stages=load(H/'SAVED_REACTION_DIAGNOSTIC/stages.json')
assert receipt['initial']['result']['chunk_id']=='21844c' and receipt['initial']['result']['session_id']==17312
assert len(receipt['observations'])==1 and receipt['observations'][0]['chunk_id']=='b763a2' and type(receipt['observations'][0]['exit_code']) is int and receipt['observations'][0]['exit_code']==0 and receipt['session_closed'] is True
assert ep['host.full_stderr.txt']['size_bytes']==0
saved(hp['result.json'],stdout['actual_host_result']); saved(hp['run/admit.log'],stdout['actual_diagnostic_stdout'])
for key,name in [('actual_diagnostic_stdout','run/admit.log'),('actual_watchdog','run/admit.watchdog.json')]: saved(hp[name],h[key])
for key,name in [('actual_diagnostic_result','result.json'),('actual_diagnostic_manifest','payload_manifest.json')]: saved(pp[name],h[key])
assert log['sha256']==pp['result.json']['sha256'] and log['manifest_sha256']==pp['payload_manifest.json']['sha256'] and log['archive_bytes']==sum(v['size_bytes'] for v in pp.values())
assert w==h['watchdog'] and stages['stages']==h['stage_records'] and len(stages['stages'])==1
assert w['command']==h['actual_canonical_command']==stages['stages'][0]['command']
assert w['pid']==load(O/'execution_claim.json')['PID'] and w['returncode']==0 and w['limit_failure'] is None and w['own_child_only'] is True and w['liveness_group_cleanup'] is True
assert h['whole_seconds']<h['whole_wall_cap_seconds']==60 and 0<w['elapsed_seconds']<w['wall_cap_seconds']<=h['stage_wall_cap_seconds']==60 and w['sampled_peak_rss_mib']<w['rss_cap_mib']==h['rss_cap_mib']==512
assert h['threads']==h['children_at_once']==1 and h['retries']==0 and h['profile_used'] is False and h['supervisor_class_or_MRO_modified'] is False
capscope=sum(v['size_bytes'] for v in pp.values())+sum(v['size_bytes'] for v in hp.values())+sum(v['size_bytes'] for v in sap.values())
assert capscope==h['archive_before_result_bytes']+hp['result.json']['size_bytes']<h['archive_cap_bytes']==64*2**20
for phase in ['resources_before','resources_after']:
    z=h[phase]; assert z['artifact_bytes']<z['artifact_budget_bytes']==96*2**30 and z['disk_free_bytes']>z['min_free_bytes']==8*2**30 and z['resource_scope_contract']['all_declared_extras_retained'] is True
assert h['resources_before']['artifact_bytes']+64*2**20<96*2**30 and h['resources_before']['disk_free_bytes']-64*2**20>8*2**30
fixed={
 'support':(S/'actual_prepare_sources/prepare_cli_host_v15.py','3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'),
 'original_helper':(B/'validation/axial_material/prepare_qualified_AB_source_factor_production.py','619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'),
 'ownrss_full':(B/'validation/axial_material/qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),
 'production_runner':(B/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),
 'bounded_runner':(B/'validation/artifacts/axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'),
 'dynamic_history_factory':(B/'validation/axial_material/moment_order_complete_history_resource_trie_20261010.py','ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')}
fp={k:pin(v[0]) for k,v in fixed.items()}
for k,v in fixed.items(): check(fp[k],v[1])
check(hp['runtime/run_bounded_dragon.py'],fixed['bounded_runner'][1]); saved(fp['original_helper'],h['original_helper']); saved(fp['dynamic_history_factory'],h['resource_factory'])
G=B/'validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard'
g=load(G/'guard_controls.json'); gp={k:pin(G/k) for k in ['guard_controls.json','tested_driver_source.py']}
check(gp['guard_controls.json'],'ae4d7e86423a187c29efd5bf87d54053081d7b7fcf18ac88cd9e49639cb07454'); check(gp['tested_driver_source.py'],g['source_sha256'])
for k,v in g['control_files'].items(): gp[k]=pin(G/k); check(gp[k],v)
def cls(p):
    text=p.read_text(); return next(ast.get_source_segment(text,n) for n in ast.parse(text).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
assert cls(fixed['ownrss_full'][0])==cls(G/'tested_driver_source.py') and all(g[k] is True for k in ['positive_child_completed','actual_oversize_child_rejected','terminated_own_child_not_live']) and g['rss_cap_mib']==512
assert 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)' in Path(sp['host']['path']).read_text()
node=next(n for n in ast.parse(fixed['ownrss_full'][0].read_text()).body if isinstance(n,ast.ClassDef) and n.name=='OwnRSSSerialExecutor')
assert [ast.dump(n) for n in node.bases]==[ast.dump(ast.Name(id='SerialExecutor',ctx=ast.Load()))]
keys=['scientific_accuracy_qualified','AAA_qualified','ABA_admitted','same_MG_unreduced_reference_qualified','reaction_raw_transfer_equivalence_qualified','full_physical_neutron_balance_qualified','transport_launched','basis_rank_or_white_coefficients_modified']
assert all(r[k] is False for k in keys)
assert r['classification']=='ALL_370_GROUP_SAVED_SOURCE_REACTION_FLUX_DIAGNOSTICS_COMPLETE_NOT_PHYSICAL_BALANCE_QUALIFIED'
assert r['dimensions']==dict(axial_cells=48,cells=384,faces=392,fission_components=32,groups=370,mixtures=24,radial_regions=8,unknowns_per_group=1800)
assert all(r[k] is True for k in ['full_group_fine_cell_coverage','original_scientific_thresholds_unchanged','no_clipping_renormalization_or_dropped_bin'])
assert r['export_replay']['cells']['rows']==384 and r['export_replay']['faces']['rows']==392 and len(r['export_replay']['cells']['fields'])==9 and len(r['export_replay']['faces']['fields'])==4
assert all(v['max_abs_delta']==0 for part in r['export_replay'].values() for v in part['fields'].values())
assert len(r['scatter_coverage'])==370 and [v['group'] for v in r['scatter_coverage']]==list(range(1,371))
assert len(r['reaction_scope']['all_present_named_channels_retained'])==12 and r['reaction_scope']['neutron_multiplicity_contract_supplied'] is False and r['reaction_scope']['NX_semantics_assessed'] is False
assert r['source_scope']['axial_R64_work_source_present'] is False and r['source_scope']['saved_work_source_equals_final_state_source_assessed'] is False
csvkeys={}
for role,cols,expect in [('regions',('radial_region','axial_cell'),{(a,b) for a in range(1,9) for b in range(1,49)}),('faces',('radial_region','face'),{(a,b) for a in range(1,9) for b in range(49)})]:
    with Path(ip[role]['path']).open(newline='') as f:
        reader=csv.DictReader(f); headers=reader.fieldnames; rows=list(reader)
    got=[tuple(int(v[c]) for c in cols) for v in rows]
    assert len(got)==len(set(got))==len(expect) and set(got)==expect
    part='cells' if role=='regions' else 'faces'
    assert set(headers)==set(cols)|set(r['export_replay'][part]['fields'])
    csvkeys[role]=dict(rows=len(rows),columns=headers,complete_unique_expected_keys=True,numeric_columns_not_recomputed=True)
old=B/'validation/artifacts/axial-material-AAA-white-trace-refined-closeout-20261005/REPORT.txt'
bad=B/'validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-table-combined-terminal-v15-20261010/failed_terminal_return.json'
oldpin=pin(old); badpin=pin(bad); check(badpin,'d0ceba77e4bf2395b3da686cd0297f941965932dd99be09ad98201574430895c'); badjson=load(bad)
assert '原八项门槛 7 PASS、nu_fission FAIL；AAA_REFERENCE_NOT_QUALIFIED。' in old.read_text() and '3.9525%' in old.read_text()
assert badjson['classification']=='FAILED_COMBINED_PREP_ORIGINAL_512_MIB_NO_RETRY' and badjson['returncode']==1 and badjson['successful_new_runtime_build_observed'] is False and badjson['full_input_graph_created'] is False
check(ep['REPORT.txt'],'da8da235663c3c96b1de80e909168955fcedd8a2ead3d240e28b75f19d2da73b')
assert set(p.name for p in O.iterdir() if p.is_file())==set(paths)
review=dict(
 schema='AXMAT_FINITE_ACTUAL_SAVED_SOURCE_REACTION_EVIDENCE_REVIEW_V1',classification='READ_ONLY_BYTE_IDENTITY_AND_RECORDED_DIAGNOSTIC_EVIDENCE_COMPLETE_NO_NEW_PHYSICS_QUALIFICATION',created_unix=time.time(),fresh_report_directory=str(T),
 scope=dict(project_files_modified=False,business_modules_imported_or_executed=False,numpy_imported_or_numeric_recomputed=False,transport_launched=False,Root_tool_handles_accessed=False,history_or_all_artifact_resource_scan_performed=False,raw_array_content_decoded=False,fixed_11_input_full_EOF_hash_authorized_and_completed=True),
 receipt_review=dict(raw_receipt=receipt,integer_exit_0=True,session_closed=True,host_stdout_pins_match=True,stderr_empty=True),
 payload_integrity=dict(raw_arrays=77,manifest_members_excluding_manifest=82,total_payload_files_including_manifest=83,raw_bytes=rawbytes,payload_bytes_before_manifest=54353509,final_payload_bytes=sum(v['size_bytes'] for v in pp.values()),exact_complete_current_file_set_matches_manifest=True,all_fresh_SHA_and_7ID_stable=True,all_layout_shapes_dtype_bytes_SHA_match=True,file_pins=pp),
 input_integrity=dict(file_count=11,total_bytes=sum(v['size_bytes'] for v in ip.values()),all_saved_before_after_structures_equal=True,all_fresh_SHA_and_7ID_match_saved_before_after=True,identity_representation='7ID dictionaries compared directly',file_pins=ip),
 source_binding=dict(source_pins=sp,READY_only_one_status_assignment_changed_remaining_text_byte_exact=True,all_23_function_source_segments_byte_exact=True,host_finite_inverse_count=len(steps),host_inverse_parent_byte_exact=True,inverse_occurrences=steps,source_only_archive_manifest_verified=True,source_archive_pins=sap),
 normal_guard_and_caps=dict(fixed_source_pins=fp,live_guard_pins=gp,live_guard_class_source_byte_exact=True,unchanged_SerialExecutor_base_static_check=True,actual_host_explicit_MRO_runner_type_and_resource_binding_checks_completed=True,guard_failure=w['limit_failure'],whole_seconds=h['whole_seconds'],child_seconds=w['elapsed_seconds'],stage_seconds=stages['stages'][0]['elapsed_seconds'],sampled_child_peak_rss_mib=w['sampled_peak_rss_mib'],whole_cap_seconds=60,stage_cap_seconds=60,rss_cap_mib=512,archive_cap_bytes=64*2**20,threads=1,children_at_once=1,retries=0,profile_used=False,all_recorded_and_final_archive_caps_satisfied=True,archive_before_result_bytes=h['archive_before_result_bytes'],final_cap_scope_host_payload_source_archive_bytes=capscope,external_READY_and_Root_receipts_bytes=sp['READY_source']['size_bytes']+sum(v['size_bytes'] for v in ep.values()),extended_current_evidence_bundle_bytes=capscope+sp['READY_source']['size_bytes']+sum(v['size_bytes'] for v in ep.values()),resource_metadata={phase:{k:v for k,v in h[phase].items() if k not in ['resource_roots','declared_resource_roots']} for phase in ['resources_before','resources_after']},resource_totals_not_rescanned=True,host_pins=hp,Root_receipt_pins=ep),
 coverage_and_replay=dict(dimensions=r['dimensions'],csv_key_coverage=csvkeys,export_replay_record=r['export_replay'],all_13_recorded_numeric_column_max_abs_deltas_zero=True,source_checks_every_row_every_declared_column_complete_keyset=True,faces_0_to_48_retained=True,single_global_denominator=r['global_nufission_replayed'],normalization_roundoff_bound=r['normalization_roundoff_bound'],original_four_to_one_96cell_and_13plane_view_retained=True,physical_replay_recomputed_by_reviewer=False),
 recorded_diagnostic_values={k:r['summary'][k] for k in ['saved_source_difference','saved_source_relative','transport_correction','fission_source','corrected_collision','axial_outflow','transverse_closure','with_closure','without_closure','correction_identity','closure_identity']},
 scientific_scope=dict(source_scope=r['source_scope'],reaction_scope=r['reaction_scope'],all_science_flags={k:r[k] for k in keys},transfer_identity=r['transfer_row_column_identity'],physical_balance_PASS_created=False,endpoint_3_9525_percent_cause_established=False),
 historical_outcomes=dict(AAA_REPORT_pin=oldpin,AAA='7 PASS / nu_fission FAIL; AAA_REFERENCE_NOT_QUALIFIED',endpoint_max_deviation_percent=3.9525,ABA='not admitted',combined_failed_terminal_pin=badpin,combined_classification=badjson['classification'],combined_exit_code=1,combined_peak_rss_mib=badjson['sampled_own_child_peak_rss_mib'],successful_new_runtime_build_observed=False,full_input_graph_created=False,no_new_diagnostic_overturns_previous_outcomes=True),
 initial_strict_file_set_failure=dict(note=str(T/'INITIAL_STRICT_FILESET_CHECK_FAILED_NOTE.json'),assertion_source=str(T/'INITIAL_STRICT_FILESET_CHECK_SOURCE.py'),transient_file_count=84,extra_file='REPORT.txt',Root_moved_own_postprocessing_doc_to_receipts=True,repaired_doc_pin=ep['REPORT.txt'],current_exact_payload_83_verified=True,no_business_or_numerical_retry=True),
 supported_physical_interpretation=[
 'Saved REAL32 last-buffer scalar projection versus final-flux fission-plus-offgroup-source reconstruction has max local relative discrepancy 1.3413243042088778e-7 (scale=max(abs(saved),abs(rebuilt))). This supports close numerical agreement in the saved state, without proving final authoritative axial R64 work RHS or source phase/partition equivalence.',
 'Shared total/self transport correction absolute sum is 6.471867109013756e-7 versus fission-source integral 1.0000000025192153. It is nonzero; the observation cannot establish the zero-correction hypothesis or a physical absorption formula.',
 'With stored transverse closure the diagnostic absolute residual sum is 0.0006564854561199579 and signed sum -3.544405277894619e-7; without closure the absolute sum is 3.1422361959516816. Strong cancellation across group/cell terms makes the signed aggregate much smaller than the magnitude ledger. These residuals remain diagnostic and cannot grant full physical neutron balance PASS.',
 'Exact transfer row/column identity and tiny correction/closure subtraction identities support reconstructed accounting consistency. Neutron-multiplicity processing contracts and raw-channel to transfer equivalence are still missing.',
 'No causal attribution of the historical terminal fuel-share 3.9525 percent discrepancy is supported. AAA 7/8 and the new combined-preparation failure remain unchanged.'
 ],
 next_rigorous_source_physics_evidence_action='Prepare an executable-provenance-bound source-only plan to identify and capture the final authoritative axial REAL64 work RHS at the precise converged phase, with all groups/cells and explicit ITPIJ/LSCAL/ILEAK and guarded S2/SIGS source partitions. Bind the historical Dragon51b executable/source/processing contract rather than substitute current source. Obtain canonical emitted-neutron multiplicity and transfer semantics for every retained reaction channel, especially NX/NNP/N2A, before constructing physical absorption/neutron balance. Any future bounded capture requires separate admission; this review performs no capture or transport.'
)
(T/'REVIEW.json').write_text(json.dumps(review,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
print(json.dumps(dict(report=str(T/'REVIEW.json'),payload_files=83,raw_arrays=77,raw_bytes=rawbytes,payload_bytes=review['payload_integrity']['final_payload_bytes'],fixed_11_input_bytes=review['input_integrity']['total_bytes'],host_inverse_steps=len(steps),final_cap_scope_bytes=capscope,external_document_and_receipt_bytes=review['normal_guard_and_caps']['external_READY_and_Root_receipts_bytes'],extended_current_evidence_bundle_bytes=review['normal_guard_and_caps']['extended_current_evidence_bundle_bytes'],all_assertions='PASS'),ensure_ascii=False,indent=2))
