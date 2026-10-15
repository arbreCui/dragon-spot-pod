from pathlib import Path
import hashlib, json, os, shlex, shutil, stat, time

R = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
ART = Path('/Users/wen/spot/validation/artifacts')
D = Path(__file__).parent
H = ART / 'axial-material-current-first-A-complete-aggregate-eight-roots-20261014-v1/Root_actual_current_material_evidence_summary.json'
C = ART / 'axial-material-current-first-A-complete-aggregate-eight-roots-20261014-v1-evidence/ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_REPORT.json'
CAPS = dict(whole_seconds=1800, stage_seconds=600, rss_mib=512, joint_archive_bytes=2147483648,
            history_bytes=103079215104, free_floor_bytes=8589934592, threads=1, children_at_once=1, retries=0)

def ids(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def seven(p):
    q = Path(p['path'])
    s = q.lstat()
    assert stat.S_ISREG(s.st_mode) and not q.is_symlink(), str(q)
    assert ids(s) == p['identity'] and s.st_size == p['size_bytes'], str(q)
    assert all(type(x) is int for x in p['identity']) and len(p['identity']) == 7

def pin(p, maximum=64 * 2**20):
    p = Path(p)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and not p.is_symlink() and s.st_size <= maximum, str(p)
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        assert ids(os.fstat(f.fileno())) == ids(s)
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        assert ids(os.fstat(f.fileno())) == ids(s)
    assert ids(p.lstat()) == ids(s)
    return dict(path=str(p), sha256=digest, size_bytes=s.st_size, identity=ids(s))

def load(p):
    if isinstance(p, dict):
        assert pin(p['path']) == p
        p = p['path']
    return json.loads(Path(p).read_bytes())

def table(rows):
    ans = {}
    for p in rows:
        assert p['path'] not in ans or ans[p['path']] == p
        ans[p['path']] = p
    return ans

def files(root):
    result = []
    root = Path(root)
    assert root.is_dir() and not root.is_symlink()
    todo = [root]
    while todo:
        for p in todo.pop().iterdir():
            s = p.lstat()
            assert not p.is_symlink(), str(p)
            if stat.S_ISDIR(s.st_mode):
                todo.append(p)
            else:
                assert stat.S_ISREG(s.st_mode), str(p)
                result.append((str(p), s.st_size))
    return sorted(result)

def closed_zero(z):
    assert type(z['exit_code']) is int and z['exit_code'] == 0 and z.get('session_id') is None

start = time.monotonic()
assert not (D / 'REVIEW.json').exists() and not (D / 'TRUE_TOOL_RETURNS.json').exists()
hp = pin(H); h = load(H)
assert hp['sha256'].startswith('62813b4e') and hp['size_bytes'] == 3113281
cp = pin(C); c = load(C)
assert cp['sha256'] == '2687f29c00bc3234ec8140588f5abe39503d0fdfee23f24138f8d3ef24577726' and cp['size_bytes'] == 7647
fp = pin(R / 'independent_eight_root_first_A_aggregate_final_SF_HF_request_ROOT30_metadata_review_20261014/REVIEW.json')
assert fp['sha256'].startswith('e51f7eae')
f = load(fp)
assert f['failure'] is None and f['all_declared_current_pins_seven_fields_verified_twice'] is True
sp = f['actual_Source_freeze_pin']; sf = load(sp)
hfpin = f['actual_Host_freeze_pin']; hf = load(hfpin)
dp = f['actual_dynamic_interface_pin']; dyn = load(dp)
qp = f['actual_request_pin']; q = load(qp)
ap = f['actual_Root_argv_pin']; a = load(ap)
assert sp['sha256'] == '80ff0cf02fe3f8b3a98910dff9604352f736553cfe1a73444aa7c7f66eeacc41'
assert hfpin['sha256'] == 'ca69ff68da07d305aced968d2f6737774c4b5ddc6000399a9dc9e9443729cc07'
assert dp['sha256'].startswith('872c')
assert qp['sha256'] == 'bbf1330ed599188c2b57fbbeea39715583909a359428edfcf9c199ab710e6a61' and qp['size_bytes'] == 2570605
assert q['operation'] == 'aggregate' and q['original_caps'] == CAPS == c['original_caps'] == f['original_caps']
assert q['complete_source_freeze_pin'] == sp == c['complete_source_freeze_pin']
assert a['request_pin'] == qp and a['published_dynamic_interface_pin'] == dp
assert len(a['argv']) == 30 and shlex.split(a['exact_command']) == a['argv']
assert a['argv'] == dyn['known_argv_prefix'] + ['--request-summary', qp['path'], '--request-sha256', qp['sha256'], '--request-seven-id', json.dumps(qp['identity'], separators=(',', ':'))]
assert dyn['selected_source_freeze_pin'] == sp and dyn['selected_host_freeze_pin'] == hfpin and dyn['host_source_pin'] == hf['host_source']
rtp = pin(R / 'ROOT_ACTUAL_EIGHT_ROOT_FIRST_A_COMPLETE_AGGREGATE_TRUE_TOOL_RETURNS_20261014.json'); rt = load(rtp)
assert rt['actual_initial_return']['chunk_id'] == 'dbb27b' and rt['actual_initial_return']['session_id'] == 31220
assert rt['actual_initial_return']['output'] == '' and rt['actual_terminal_return']['output'] == ''
assert rt['actual_terminal_return']['chunk_id'] == '8ee7d2'
closed_zero(rt['actual_terminal_return'])
assert rt['observed_closed'] is True and type(rt['original_integer_exit_code']) is int and rt['original_integer_exit_code'] == 0
assert rt['exact_executed_command'] == a['exact_command']
fixed = table(h['fixed_current_pins'])
assert len(h['fixed_current_pins']) == len(fixed) == 5921
assert fixed == table(q['complete_input_pins'] + [qp])
assert len(q['complete_input_pins']) == 5920
for p in sf['complete_source_file_pins'] + hf['dependencies'] + [hf['host_source']]:
    assert fixed[p['path']] == p
for p in fixed.values():
    seven(p)
assert h['schema'] == 'ACTUAL_CURRENT_FORMAL_MATERIAL_COMPLETE_EVIDENCE_GUARDED_ROOT_V1'
assert h['status'] == 'ACTUAL_COMPLETE_CURRENT_EVIDENCE_EXIT2_CLOSED_ONLY' and h['operation'] == 'aggregate'
assert h['failure'] is None and h['after_check_error'] is None and h['actual_intentional_exit2_normal_closure'] is True
assert len(h['records']) == 1
rec = h['records'][0]
assert rec['status'] == 'FAILED' and rec['error'] == 'own-child stage failed; no retry'
assert rec['wall_cap_seconds'] == 600 and 'resource_before' in rec and 'resource_after' not in rec
assert h['actual_complete_child_receipt']['report'] == cp
assert h['actual_complete_child_receipt']['status'] == 'ACTUAL_COMPLETE_CURRENT_EVIDENCE_ONLY_EXIT2'
wp = h['actual_watchdog_full_pin']; watch = load(wp)
assert type(watch['returncode']) is int and watch['returncode'] == 2
assert watch['command'] == rec['command'] and watch['limit_failure'] is None and watch['rss_cap_mib'] == 512
assert 0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= 600 and 0 <= watch['sampled_peak_rss_mib'] < 512
assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
assert rec['command'][:-2] == ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', str(Path(hf['host_source']['path']).parent / 'current_material_lineage_evidence.py'), 'aggregate', '--request-pin', json.dumps(qp, separators=(',', ':')), '--output-dir', q['output_directory']]
assert rec['command'][-2] == '--expected-parent-pid' and int(rec['command'][-1]) > 1
lp = h['actual_log_full_pin']; assert pin(lp['path']) == lp
log = [s for s in Path(lp['path']).read_text().splitlines() if s.strip()]
assert len(log) == 1 and json.loads(log[0]) == h['actual_complete_child_receipt']
assert h['original_guard_class'] == 'OwnRSSSerialExecutor' and h['original_guard_MRO_unchanged'] is True
assert h['requires_host_process_metadata_access'] is True and h['final_report_bytes_in_original_resources'] is True
assert h['SELF_peak_bytes'] == 140132352 and h['SELF_peak_bytes'] < 512 * 2**20 and 0 < h['wall_seconds'] < 1800
assert c['schema'] == 'ACTUAL_COMPLETE_FINAL_MICRO_MACRO_CONSTRUCTION_EVIDENCE_ONLY_V1'
assert c['status'] == 'ACTUAL_CURRENT_COMPLETE_ORIGINAL_MATH_CONSTRUCTION_EVIDENCE_ONLY_EXIT2' and c['error'] is None
assert c['state_order'] == ['A'] and len(c['states']) == 1 and c['states'][0]['state'] == 'A'
assert c['current_case_spec_pin'] == q['current_case_spec_pin']
assert c['observation_scope'] == 'ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES'
assert c['all_complete_state_scope_retained'] is True and c['complete_final_construction_qualified'] is False
assert c['new_aggregation_qualification_sha256'] is None and c['actual_scientific_qualification_sha256'] is None
s = c['states'][0]
assert s['error'] == "ValueError('all original 19619 macro records retained')"
assert s['all_original_records'] == 23895 and s['complete_MACROLIB_records'] == 19620
assert s['unknown_macro_producers'] == 19248 and s['all_context_or_operand_issues'] == 1 and s['all_mismatching_elements'] == 0
assert s['original_scope'] == [370, 8, 3, 32, 64, 62, 18, 6, 48]
for k in ['all_original_native_records_and_bytes_preserved', 'full_output_scope_retained_even_on_failure', 'all_missing_fields_not_zero_filled', 'all_state_databases_and_pool_closed_before_next_state']:
    assert s[k] is True
for obj in [h, c, s, h['actual_complete_child_receipt']]:
    for k, v in obj.items():
        if k.endswith('_qualified') or k in ['ABA_admitted', 'goal_complete', 'historical_native_RAM_bits_verified', 'original_XSM_memory_bits_verified', 'historical_unsaved_context_recovered', 'reaction_multiplicity_verified', 'original_native_build_binary_Source_linkage_qualified', 'historical_LIBDEN_machine_arithmetic_replayed', 'native_transport_executed', 'genuine_supervisor_watch_verified_here']:
            assert v is False, (k, v)
outputs = table(h['complete_output_pins'])
assert len(h['complete_output_pins']) == len(outputs) == 13
for p in outputs.values():
    assert pin(p['path']) == p
assert outputs[cp['path']] == cp and outputs[wp['path']] == wp and outputs[lp['path']] == lp
actual_output_files = files(q['owning_host_output_directory']) + files(q['output_directory'])
assert sorted(p for p, _ in actual_output_files) == sorted(list(outputs) + [str(H)])
assert len(actual_output_files) == 14
for p in s['complete_output_file_pins']:
    assert outputs[p['path']] == p
statep = outputs[str(Path(q['output_directory']) / 'A/ACTUAL_COMPLETE_STATE_CONSTRUCTION_REPORT.json')]
state_report = load(statep)
for k, v in state_report.items():
    assert s[k] == v
stagep = outputs[str(Path(q['owning_host_output_directory']) / 'evidence-stage/stages.json')]
assert load(stagep)['stages'] == h['records']
zero_names = ['all_numeric_mismatches.jsonl', 'complete_field_comparisons.jsonl', 'complete_model_expected_bytes.bin']
for name in zero_names:
    p = outputs[str(Path(q['output_directory']) / 'A' / name)]
    assert p['size_bytes'] == 0 and p['sha256'] == hashlib.sha256(b'').hexdigest()
rootfalse = ['three_plane_qualified', 'GLOBAL_qualified', 'rank_qualified', 'online_BOOT_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete', 'physical_neutron_balance_qualified', 'coupled_370group_reference_qualified', 'scientific_accuracy_qualified']
for k in rootfalse:
    assert h[k] is False
roots = q['joint_archive_roots']
assert len(roots) == len(set(roots)) == 8 and roots == f['cumulative_joint_roots']
for resource in [rec['resource_before']['complete_joint_five_root_fresh'], h['resources_after']['complete_joint_five_root_fresh']]:
    assert resource['resource_roots'] == roots and resource['artifact_budget_bytes'] == CAPS['joint_archive_bytes']
    assert resource['min_free_bytes'] == CAPS['free_floor_bytes'] and resource['artifact_bytes'] < CAPS['joint_archive_bytes'] and resource['disk_free_bytes'] >= CAPS['free_floor_bytes']
for resource in [h['resources_before'], rec['resource_before']['original_history_cold_free'], h['resources_after']['original_history_cold_free']]:
    assert resource['artifact_budget_bytes'] == CAPS['history_bytes'] and resource['min_free_bytes'] == CAPS['free_floor_bytes']
    assert resource['artifact_bytes'] < CAPS['history_bytes'] and resource['disk_free_bytes'] >= CAPS['free_floor_bytes']
current_rows = [row for root in roots for row in files(root)]
current_bytes = sum(n for _, n in current_rows)
assert len(set(p for p, _ in current_rows)) == len(current_rows)
assert current_bytes < CAPS['joint_archive_bytes'] and shutil.disk_usage(R).free >= CAPS['free_floor_bytes']
ep = q['actual_extraction_independent_review_pin']; e = load(ep)
assert ep['sha256'] == '393eddcf2637a68426e3a191a0432030383e71be8254498b65d7819e7509d00a'
assert c['actual_extraction_independent_review_pin'] == ep
assert e['failure'] is None and e['actual_new_outputs_full_EOF_SHA_and7_verified'] is True
assert e['all_original_snapshot_and_context_pins_verified'] is True and e['actual_original_capture_context_snapshot_pin_current7_provenance_chain_verified'] is True
assert e['actual_original_failed_record_preserved'] is True and e['original_tree_decode_or_collect_repeated'] is False
erp = pin(Path(ep['path']).parent / 'REVIEW.json'); er = load(erp)
assert erp['sha256'] == '172b0a0564fabe9768c7c0e7542939d24b2c7ad9264317a674d96492751d961b'
etp = pin(Path(ep['path']).parent / 'TRUE_TOOL_RETURNS.json'); et = load(etp)
closed_zero(et['actual_review_return']); closed_zero(et['actual_postverification_return'])
assert et['actual_review_return'] == et['actual_postverification_return'] and et['observed_closed'] is True
assert type(et['original_integer_exit_code']) is int and et['original_integer_exit_code'] == 0
assert json.loads(et['actual_postverification_return']['output'])['review_pin'] == erp
assert json.loads(et['actual_postverification_return']['output'])['actual_extraction_review_pin'] == ep
provenance = h['current_metadata_reattestation_provenance']
assert provenance['strict_actual_seven_field_file_identity_preserved'] is True
for k in ['historical_files_modified', 'prior_business_stages_reexecuted_by_metadata_view', 'physical_accuracy_or_reference_qualification_inferred_from_reattestation']:
    assert provenance[k] is False
for p in fixed.values():
    seven(p)
for p in [hp, cp, fp, sp, hfpin, dp, qp, ap, rtp, ep, erp, etp] + list(outputs.values()):
    seven(p)
result = dict(schema='INDEPENDENT_EIGHT_ROOT_FIRST_A_AGGREGATE_ACTUAL_EVIDENCE_POSTVERIFICATION_V1',
              status='PASS_ACTUAL_EIGHT_ROOT_FIRST_A_AGGREGATE_EVIDENCE_POSTVERIFICATION', failure=None,
              business_executed=False, compiler_executed=False, numerical_executed=False, files_deleted=False,
              actual_aggregate_host_pin=hp, actual_aggregate_report_pin=cp, actual_Root_true_tool_pin=rtp,
              actual_Root_argv_pin=ap, actual_request_pin=qp, actual_Source_freeze_pin=sp,
              actual_Host_freeze_pin=hfpin, actual_dynamic_interface_pin=dp,
              actual_final_metadata_review_pin=fp, actual_extraction_review_pin=ep,
              actual_extraction_post_pin=erp, actual_extraction_post_tools_pin=etp,
              reviewer_source_pin=pin(__file__),
              complete_fixed_current_pin_count=5921, all_fixed_current_seven_fields_verified_twice=True,
              complete_new_output_pin_count=13, complete_output_file_pins=list(outputs.values()),
              all_new_outputs_full_EOF_SHA_and7_verified=True, complete_output_scene_equals_13_outputs_plus_host=True,
              actual_Root_integer_exit_code=rt['original_integer_exit_code'], actual_child_integer_exit_code=watch['returncode'],
              actual_original_FAILED_no_retry_record_preserved=True, actual_original_stage_status=rec['status'],
              actual_watchdog_pin=wp, actual_log_pin=lp, actual_watchdog=watch,
              actual_SELF_peak_bytes=h['SELF_peak_bytes'], actual_root_wall_seconds=h['wall_seconds'],
              original_caps=CAPS, cumulative_joint_roots=roots,
              current_eight_root_metadata=dict(artifact_bytes=current_bytes, regular_files=len(current_rows), disk_free_bytes=shutil.disk_usage(R).free),
              original_history_and_joint_resource_caps_preserved=True,
              all_original_records=s['all_original_records'], complete_MACROLIB_records=s['complete_MACROLIB_records'],
              unknown_macro_producers=s['unknown_macro_producers'], all_context_or_operand_issues=s['all_context_or_operand_issues'],
              all_mismatching_elements=s['all_mismatching_elements'], original_math_initialization_error=s['error'],
              mathematical_initialization_stopped_before_comparison=True, zero_mismatches_does_not_mean_PASS=True,
              comparison_expected_and_mismatch_files_zero_bytes=True,
              historical_snapshots_redecoded=False, large_original_scientific_payload_EOF_repeated=False,
              prior_complete_scientific_EOF_proof_bound_to_genuine_closed_post_return=True,
              physical_neutron_balance_qualified=False, coupled_370group_reference_qualified=False,
              scientific_accuracy_qualified=False, physics_qualified=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False)
assert time.monotonic() - start < 1800
with (D / 'REVIEW.json').open('x') as out:
    json.dump(result, out, indent=2); out.write('\n'); out.flush(); os.fsync(out.fileno())
fd = os.open(D, os.O_RDONLY | os.O_DIRECTORY); os.fsync(fd); os.close(fd)
print(json.dumps(dict(status=result['status'], review_pin=pin(D / 'REVIEW.json'), actual_Root_integer_exit_code=rt['original_integer_exit_code'], actual_child_integer_exit_code=watch['returncode'], mathematical_initialization_stopped_before_comparison=True, zero_mismatches_does_not_mean_PASS=True)), flush=True)
