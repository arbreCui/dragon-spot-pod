from pathlib import Path
import collections, hashlib, json, os, shlex, shutil, stat, sys
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART=Path('/Users/wen/spot/validation/artifacts')
D=Path(__file__).parent
H=ART/'axial-material-current-first-A-complete-aggregate-empty-root-cumulative12-20261014-v1/Root_actual_current_material_evidence_summary.json'
C=ART/'axial-material-current-first-A-complete-aggregate-empty-root-cumulative12-20261014-v1-evidence/ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
def ids(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def seven(p):
    q=Path(p['path']);s=q.lstat();assert stat.S_ISREG(s.st_mode) and not q.is_symlink() and ids(s)==p['identity'] and s.st_size==p['size_bytes'],str(q)
def pin(p,maximum=64*2**20):
    p=Path(p);s=p.lstat();assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size<=maximum
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
        assert ids(os.fstat(f.fileno()))==ids(s);sha=hashlib.file_digest(f,'sha256').hexdigest();assert ids(os.fstat(f.fileno()))==ids(s)
    assert ids(p.lstat())==ids(s)
    return dict(path=str(p),sha256=sha,size_bytes=s.st_size,identity=ids(s))
def load(p):
    if isinstance(p,dict):assert pin(p['path'])==p;p=p['path']
    return json.loads(Path(p).read_bytes())
def table(rows):
    result={}
    for p in rows:
        assert p['path'] not in result or result[p['path']]==p
        result[p['path']]=p
    return result
def files(root):
    root=Path(root);assert root.is_dir() and not root.is_symlink();todo=[root];result=[]
    while todo:
        for p in todo.pop().iterdir():
            s=p.lstat();assert not p.is_symlink()
            if stat.S_ISDIR(s.st_mode):todo.append(p)
            else:assert stat.S_ISREG(s.st_mode);result.append((str(p),s.st_size))
    return sorted(result)
def genuine_zero(z):assert type(z['exit_code']) is int and z['exit_code']==0 and z.get('session_id') is None
assert not (D/'REVIEW.json').exists() and not (D/'TRUE_TOOL_RETURNS.json').exists()
fp=pin(R/'independent_empty_root_cumulative12_aggregate_final_SF_HF_request_ROOT30_metadata_review_20261014/REVIEW.json');final=load(fp)
assert fp['sha256'].startswith('88e4a635') and final['failure'] is None and final['all_declared_current_pins_seven_fields_verified_twice'] is True
ftp=pin(Path(fp['path']).parent/'TRUE_TOOL_RETURNS.json');ft=load(ftp);genuine_zero(ft['actual_review_return'])
assert ftp['sha256'].startswith('d821182d') and ft['observed_closed'] is True and type(ft['original_integer_exit_code']) is int and ft['original_integer_exit_code']==0
assert json.loads(ft['actual_review_return']['output'].strip().splitlines()[-1])['review_pin']==fp
sp=final['actual_Source_freeze_pin'];sf=load(sp);hp=final['actual_Host_freeze_pin'];hf=load(hp);dp=final['actual_dynamic_interface_pin'];dyn=load(dp)
qp=final['actual_request_pin'];q=load(qp);ap=final['actual_Root_argv_pin'];a=load(ap)
assert sp['sha256']=='d470f04f631521420b52924ca6fcbde816d27c70200a209d4f4de91678fd597e'
assert hp['sha256']=='924412106fa0818cb32c994752275b8c1578c7bb7a4ab17c14399f20798802a2' and len(hf['dependencies'])==5955
assert dp['sha256']=='ac4dc926ceed6edc6ed73498a9962a4b24d815d9ddee1983bd7b19cf57f8c451'
assert qp['sha256']=='1673c6377ea1ef7857ff651706e6b0c9315f5d6eb91c94b963ceaf03b671d2ad' and qp['size_bytes']==2582429 and len(q['complete_input_pins'])==5937
assert q['complete_source_freeze_pin']==sp and q['original_caps']==final['original_caps']==CAPS
assert a['request_pin']==qp and a['published_dynamic_interface_pin']==dp and len(a['argv'])==30 and shlex.split(a['exact_command'])==a['argv']
assert a['argv']==dyn['known_argv_prefix']+['--request-summary',qp['path'],'--request-sha256',qp['sha256'],'--request-seven-id',json.dumps(qp['identity'],separators=(',',':'))]
assert dyn['selected_source_freeze_pin']==sp and dyn['selected_host_freeze_pin']==hp and dyn['host_source_pin']==hf['host_source']
tp=pin(sys.argv[1]);tools=load(tp);z=tools['actual_terminal_return']
assert tools['actual_initial_return']['chunk_id']=='11e83c' and tools['actual_initial_return']['session_id']==46518
assert type(z['exit_code']) is int and z['exit_code'] in (0,1) and z.get('session_id') is None
assert tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and tools['original_integer_exit_code']==z['exit_code']
assert tools['exact_executed_command']==a['exact_command']
hpin=pin(H);h=load(H);fixed=table(h['fixed_current_pins'])
assert hpin['sha256']=='ad8d7a7070841fe49632c1d061d5e741477dce0ea58227277060aae2326cca1b' and hpin['size_bytes']==3134837
assert len(fixed)==len(h['fixed_current_pins'])==5958
expected=table([qp,sp,hp,hf['host_source']]+hf['dependencies']+sf['complete_source_file_pins']+q['complete_input_pins'])
assert fixed==expected and len(expected)==5958 and final['complete_distinct_current_pin_count']==5956
for p in fixed.values():seven(p)
assert h['schema']=='ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1' and h['operation']=='aggregate' and len(h['records'])==1
rec=h['records'][0];assert rec['status']=='FAILED' and rec['error']=='own-child stage failed; no retry' and rec['wall_cap_seconds']==600
assert h['original_guard_class']=='OwnRSSSerialExecutor' and h['original_guard_MRO_unchanged'] is True
wp=h['actual_watchdog_full_pin'];w=load(wp);lp=h['actual_log_full_pin'];assert pin(lp['path'])==lp
assert type(w['returncode']) is int and w['command']==rec['command'] and w['rss_cap_mib']==512 and w['wall_cap_seconds']<=600
assert w['own_child_only'] is True and w['liveness_group_cleanup'] is True
if z['exit_code']==0:
    assert h['status']=='ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY' and h['failure'] is None and h['after_check_error'] is None and h['actual_intentional_exit2_normal_closure'] is True
    assert w['returncode']==2 and w['limit_failure'] is None and 0<w['elapsed_seconds']<w['wall_cap_seconds'] and w['sampled_peak_rss_mib']<512
    assert h['SELF_peak_bytes']<512*2**20 and 0<h['wall_seconds']<1800
else:
    assert h['failure'] is not None or h['after_check_error'] is not None
outputs=table(h['complete_output_pins']);assert len(outputs)==len(h['complete_output_pins'])
assert len(outputs)==14
actual=files(q['owning_host_output_directory'])+files(q['output_directory'])
assert sorted(path for path,size in actual)==sorted(list(outputs)+[str(H)])
assert outputs[wp['path']]==wp and outputs[lp['path']]==lp
counts={};comparisons=compared=mismatches=unknown=issues=original_count=macro_count=producer_count=0
phase_events=[];sph_events=[];categories=collections.Counter();field_outcomes=collections.Counter();producer_outcomes=collections.Counter();end=0
for p in outputs.values():
    path=Path(p['path']);s=path.lstat();assert ids(s)==p['identity'] and not path.is_symlink();digest=hashlib.sha256();lines=0
    with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW),'rb') as stream:
        assert ids(os.fstat(stream.fileno()))==ids(s)
        if path.suffix=='.jsonl':
            for line in stream:
                digest.update(line);lines+=1;row=json.loads(line)
                if path.name=='complete_original_coverage.jsonl':
                    original_count+=1;macro_count+=int(row['record']['path'][:1]==['MACROLIB'])
                elif path.name=='complete_field_comparisons.jsonl':
                    comparisons+=1;field_outcomes[row['outcome']]+=1
                    assert row['expected_pool_begin']==end and row['expected_pool_end']>=end;end=row['expected_pool_end']
                    if 'compared_known_components' in row:
                        compared+=row['compared_known_components'];mismatches+=row['differing_known_components']
                    elif row['outcome'] in ['MODEL_BITS_MATCH','MODEL_BITS_MISMATCH']:
                        compared+=row['expected_count'];mismatches+=row['differing_elements']
                elif path.name=='all_presence_branch_and_missing.jsonl':
                    category=row['category'];categories[category]+=1
                    issues+=int(category in ['REQUIRED_OPERAND_MISSING','PHASE_FAILED','UNSUPPORTED_SOURCE_BRANCH','SOURCE_CONTEXT_NOT_SAVED'])
                    if category=='PHASE_FAILED':phase_events.append(row)
                    if 'SPH' in category:sph_events.append(row)
                elif path.name=='complete_producer_coverage.jsonl':
                    producer_count+=1;producer_outcomes[row['producer']]+=1
                    unknown+=int(row['producer']=='ORIGINAL_PRESENT_NO_PROVED_AGGREGATION_RULE')
        else:
            for chunk in iter(lambda:stream.read(8*2**20),b''):digest.update(chunk)
        assert ids(os.fstat(stream.fileno()))==ids(s)
    assert ids(path.lstat())==ids(s) and digest.hexdigest()==p['sha256'] and s.st_size==p['size_bytes']
    if path.suffix=='.jsonl':counts[path.name]=lines
cp=outputs.get(str(C));c=load(cp) if cp else None
assert cp['sha256']=='3454fca4507f138fb5594a1b572605e2a4b504c6ca3660a1af8364f3248c0bce' and cp['size_bytes']==10072
state=None
if c is not None:
    assert c['current_case_spec_pin']==q['current_case_spec_pin'] and c['complete_source_freeze_pin']==sp and c['original_caps']==CAPS
    assert c['state_order']==['A'] and c['observation_scope']=='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES'
    assert c['complete_final_construction_qualified'] is False and c['new_aggregation_qualification_sha256'] is None and c['actual_scientific_qualification_sha256'] is None
    if c['states']:
        assert len(c['states'])==1 and c['states'][0]['state']=='A';state=c['states'][0]
        assert original_count==producer_count==state['all_original_records'] and macro_count==state['complete_MACROLIB_records']
        assert unknown==state['unknown_macro_producers'] and issues==state['all_context_or_operand_issues'] and mismatches==state['all_mismatching_elements']
        assert counts.get('all_numeric_mismatches.jsonl',0)==mismatches
        if 'complete_source_field_comparisons' in state:assert comparisons==state['complete_source_field_comparisons'] and compared==state['compared_known_elements']
        expectedpin=outputs[str(Path(q['output_directory'])/'A/complete_model_expected_bytes.bin')];assert expectedpin['size_bytes']==end
        statep=outputs[str(Path(q['output_directory'])/'A/ACTUAL_COMPLETE_STATE_CONSTRUCTION_REPORT.json')];ss=load(statep)
        assert all(state[k]==v for k,v in ss.items())
        for p in state['complete_output_file_pins']:assert outputs[p['path']]==p
    if z['exit_code']==0:
        assert c['error'] is None and len(c['states'])==1 and len(outputs)==14 and h['actual_complete_child_receipt']['report']==cp
        log=[line for line in Path(lp['path']).read_text().splitlines() if line.strip()];assert len(log)==1 and json.loads(log[0])==h['actual_complete_child_receipt']
for obj in [h]+([c] if c else [])+([state] if state else [])+([h['actual_complete_child_receipt']] if h.get('actual_complete_child_receipt') else []):
    for key,value in obj.items():
        if key.endswith('_qualified') or key in ['ABA_admitted','goal_complete','historical_native_RAM_bits_verified','original_XSM_memory_bits_verified','historical_unsaved_context_recovered','historical_old_macro_proved','historical_actual_tracking_MASK_proved','historical_SPHand_compiled_arithmetic_proved']:
            assert value is False,(key,value)
roots=q['joint_archive_roots'];assert len(roots)==len(set(roots))==12 and roots==final['cumulative_joint_roots']
assert set(q['retained_prior_joint_archive_roots'])<=set(roots) and q['prior_aggregation_mathematical_qualification_claimed'] is False
for name,resource in h['resources_after'].items():
    if name=='complete_joint_five_root_fresh':
        assert resource['resource_roots']==roots and resource['artifact_budget_bytes']==CAPS['joint_archive_bytes'] and resource['artifact_bytes']<CAPS['joint_archive_bytes']
all_rows=[row for root in roots for row in files(root)];current_bytes=sum(n for _,n in all_rows)
assert len({p for p,_ in all_rows})==len(all_rows) and current_bytes<CAPS['joint_archive_bytes'] and shutil.disk_usage(R).free>=CAPS['free_floor_bytes']
ep=q['actual_extraction_independent_review_pin'];ex=load(ep)
assert ep['sha256'].startswith('393eddcf') and ex['actual_new_outputs_full_EOF_SHA_and7_verified'] is True and ex['original_tree_decode_or_collect_repeated'] is False
for p in fixed.values():seven(p)
for p in [hpin,fp,ftp,sp,hp,dp,qp,ap,tp,ep]+list(outputs.values()):seven(p)
result=dict(schema='INDEPENDENT_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_ACTUAL_EVIDENCE_POSTVERIFICATION_V1',status='PASS_ACTUAL_EMPTY_ROOT_CUMULATIVE12_FIRST_A_AGGREGATE_EVIDENCE_POSTVERIFICATION',failure=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False,
    actual_aggregate_host_pin=hpin,actual_aggregate_report_pin=cp,actual_Root_true_tool_pin=tp,actual_Root_argv_pin=ap,actual_request_pin=qp,actual_Source_freeze_pin=sp,actual_Host_freeze_pin=hp,actual_dynamic_interface_pin=dp,actual_final_metadata_review_pin=fp,actual_final_metadata_tools_pin=ftp,actual_extraction_review_pin=ep,reviewer_source_pin=pin(__file__),
    complete_fixed_current_pin_count=len(fixed),all_fixed_current7_verified_twice=True,current_request_input_count=5937,current_HF_dependency_count=5955,complete_new_output_pin_count=len(outputs),complete_output_pins=list(outputs.values()),all_new_outputs_full_EOF_SHA_and7_verified=True,output_scene_equals_all_declared_new_outputs_plus_host=True,
    actual_Root_integer_exit_code=tools['original_integer_exit_code'],actual_child_integer_exit_code=w['returncode'],actual_host_status=h['status'],actual_host_failure=h['failure'],actual_after_check_error=h['after_check_error'],actual_original_FAILED_no_retry_preserved=True,actual_watchdog_pin=wp,actual_watchdog=w,actual_root_wall_seconds=h['wall_seconds'],actual_SELF_peak_bytes=h['SELF_peak_bytes'],
    actual_complete_mathematical_report=c,actual_state_mathematical_facts=state,actual_phase_failure_events=phase_events,actual_SPH_metadata_events=sph_events,new_saved_JSONL_record_counts=counts,actual_comparison_file_rows=comparisons,actual_compared_known_elements=compared,actual_numeric_mismatch_rows=mismatches,actual_unknown_macro_producers=unknown,actual_context_or_operand_issues=issues,actual_event_category_counts=dict(categories),actual_field_outcome_counts=dict(field_outcomes),actual_producer_counts=dict(producer_outcomes),
    zero_mismatches_does_not_mean_physics_PASS=True,known_component_matches_do_not_qualify_unknown_or_inherited_fields=True,original_caps=CAPS,cumulative_joint_roots=roots,current_twelve_root_metadata=dict(artifact_bytes=current_bytes,regular_files=len(all_rows),disk_free_bytes=shutil.disk_usage(R).free),
    historical_native_or_SQLite_trees_redecoded=False,large_original_scientific_payload_EOF_repeated=False,only_new_output_JSONL_metadata_inspected=True,physical_neutron_balance_qualified=False,coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,physics_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
with (D/'REVIEW.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps(dict(status=result['status'],review_pin=pin(D/'REVIEW.json'),actual_Root_integer_exit_code=tools['original_integer_exit_code'],actual_child_integer_exit_code=w['returncode'],actual_comparison_file_rows=comparisons,actual_compared_known_elements=compared,actual_numeric_mismatch_rows=mismatches,actual_unknown_macro_producers=unknown,actual_context_or_operand_issues=issues)),flush=True)
