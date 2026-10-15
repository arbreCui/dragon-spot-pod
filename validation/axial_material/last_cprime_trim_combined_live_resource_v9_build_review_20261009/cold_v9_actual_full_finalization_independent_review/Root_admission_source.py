from pathlib import Path
import json, copy, math, struct, runpy, shutil, os, hashlib, time

H = runpy.run_path('/private/tmp/axmat_v9_Root_admit_actual_original_controls_20261009.py', run_name='pure_stdlib_metadata_helpers_only')
pin, read, identity, digest = [H[k] for k in ('pin', 'read', 'identity', 'digest')]
ROOT = Path('/Users/wen/spot'); ART = ROOT/'validation/artifacts'
R = ROOT/'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
SD = Path('/private/tmp/spot_v9_actual_finalization_full_source_independent_review_20261009')
TD = Path('/private/tmp/axmat_v9_cold_actual_finalization_postterminal_scope_20261009')
FD = Path('/private/tmp/axmat_v9_finalization_after_R19_typed_readback_20261009')
GD = Path('/private/tmp/axmat_v9_actual_controls_graph_resource_scope_20261009')

def typed(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return list(a) == list(b) and all(typed(a[k], b[k]) for k in a)
    if type(a) is list: return len(a) == len(b) and all(typed(x, y) for x, y in zip(a, b))
    if type(a) is float: return math.isfinite(a) and math.isfinite(b) and struct.pack('!d',a) == struct.pack('!d',b)
    return a == b

def actual_zero(a, closed):
    assert type(a['exit_code']) is int and a['exit_code'] == 0 and closed is True

def main():
    s, sp = read(SD/'REPORT.json', 'ead5085edb5b09ab3a2de65102565bc7493672302c2f4873512b0b3c7594d85e')
    sr, srp = read(SD/'actual_readonly_tool_return.json', 'd3cc2a2f16ac2737ae5b339103d28ec84c8321fb90870d89b02f4f0de75c264a')
    t, tp = read(TD/'actual_finalization_readonly_REPORT.json', 'd02e1b4659d3f21559fface13562ecec3699ef455f1c80d84561827947f3fbbc')
    tr, trp = read(TD/'actual_finalization_readonly_postterminal_tool_receipt.json', '1e88eb9a6fdfad77634fe2cd2f5e63d436edbcc89d8dbb28b5ceb07026c2df2b')
    f, fp = read(FD/'REPORT.json', '529d43996dc14b7edf0fbe31dd7bd5853533204513b760994918db27c7154adf')
    fr, frp = read(FD/'actual_readonly_tool_receipt.json', '7aed2fa3e8d2de0decb5983916e18d98151780be4fb23409ca41da6646f778e6')
    assert s['status'] == 'PASS' and t['status'] == 'PASS_ACTUAL_FINALIZATION_METADATA_ONLY_NO_NATIVE_CREDIT'
    actual_zero(sr['actual_tool_result'], sr['closed'])
    actual_zero(tr['actual_tool'], tr['actual_tool']['closed'])
    assert sr['actual_tool_result'] == dict(initial_chunk_id='2dd716',session_id=None,terminal_chunk_id='2dd716',exit_code=0)
    assert tr['actual_tool'] == dict(initial_chunk_id='84349b',session_id=None,terminal_chunk_id='84349b',exit_code=0,closed=True)
    for field in ('fullSOURCE31_namespace_sourcebytes_unchanged', 'all1860_expected_environment_pins_fullSHA_and1860wholebody_unchanged', 'all391_moduleowners_sourcebytes_unchanged', 'original_runtime31_flat_and7preloads_unchanged', 'all43_preparedlocalfiles_fullSHA_unchanged', 'original_full_SerialExecutor_resource_monitor_qualifyABA_bytes_unchanged', 'inherited_actual_MRO_and11compiled_code_source_proof_fresh_fullSHA', 'original8_finalization_source_declarations_fullspan_and_AST_segment_pins_unchanged', 'oldprepared_whole_typed_order_list_floatbit_inverse_and35f_exact_bytes_verified', 'Root_f14_before_after_only_finalization_bind_inverse', 'source_only_plan408a_and_allfuture_None_unchanged', 'original_math_physics_AB_layout_dtype_budget_whole_oldbody_invariance', 'all_pins_beforeafter_seven_identity_stable'):
        assert s[field] is True, field
    assert type(s['inherited_controls2079_fullSHA_and7field_identities_preserved']) is int and s['inherited_controls2079_fullSHA_and7field_identities_preserved'] == 2079
    assert type(s['distinct_fullSHA_pins']) is int and s['distinct_fullSHA_pins'] == len(s['all_fresh_pins']) == 2096
    assert s['only_added_key'] == 'own_child_supervision'
    assert t['only_own_child_supervision_added'] is True and t['whole_original_serialized_byte_inverse_exact'] is True and t['whole_original_typed_order_float64bits_inverse_exact'] is True
    assert t['reference250_legacy_and_separate2000_eight_gate_contract_unchanged'] is True
    for body in (s,t):
        for field in ('scientific_qualification','AAA_accuracy_qualified','ABA_admitted'):
            assert body[field] is False
    fresh = []
    for row in s['all_fresh_pins']:
        assert identity(row['path']) == row['identity'], row['path']
        rec = pin(row['path'], row['sha256']); assert rec['identity'] == row['identity']
        fresh.append(rec)
    for row in t['source_scope_read_pins']: pin(row['path'],row['sha256'])
    for row in (sr['source'],sr['stdout'],sr['stderr'],tr['reader'],tr['actual_config']): pin(row['path'],row['sha256'])
    obs, op = read(R/'Root_actual_V9_cold_finalization_tool_return.json','8cf6d184e65b25f1f5cc6a7328a35781af68509038617a0d35eba31b17bb7893')
    actual = dict(initial_chunk_id='a76002',session_id=47736,terminal_chunk_id='195dc5',exit_code=0)
    assert obs['actual_tool_result'] == s['actual_finalization_tool'] == dict(actual,closed=True)
    actual_zero(actual,obs['actual_tool_result']['closed'])
    term, ep = read(obs['finalization_terminal']['path'],'ea33c7159edf82ce4ac1ba3682cc013c013431961a7ef7ad2e6f4dc0efd5bdb4')
    assert typed(term['actual_tool_result'],actual) and set(term['actual_tool_result']) == set(actual)
    assert term['returncode'] == 0 and type(term['returncode']) is int and term['transport_started'] is False
    oldpath = Path(t['original_prepared']['path']); newpath = Path(t['prepared']['path']); work = newpath.parent
    old, oldpin = read(oldpath,'35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7')
    new, newpin = read(newpath,'1290a19501ba7801deafe351407b244bd32f71a6cf0d010d4a14fd64e61d8b3e')
    assert list(new) == list(old)+['own_child_supervision']
    inverse = copy.deepcopy(new); own = inverse.pop('own_child_supervision')
    assert typed(inverse,old) and (json.dumps(inverse,indent=2,allow_nan=False)+'\n').encode() == oldpath.read_bytes()
    assert typed(own,s['supervision_all3_real_descriptors_exact']) and own == t['supervision']
    assert set(own) == {'binding','controls'} and set(own['controls']) == {'seal','terminal_evidence'}
    for d in (own['binding'],own['controls']['seal'],own['controls']['terminal_evidence']):
        assert set(d) == {'path','sha256'}; pin(d['path'],d['sha256'])
    stdout, stdoutpin = read(term['full_stdout']['path'],term['full_stdout']['sha256'])
    assert typed(stdout,s['actual_entire_stdout_expected_whole_typed_order_floatbits_and_result_keys_exact'])
    assert stdout == obs['actual_stdout_result'] == term['actual_stdout_result']
    stderrpin = pin(term['full_stderr']['path'],term['full_stderr']['sha256']); assert stdoutpin['bytes'] == 846 and stderrpin['bytes'] == 0
    controls, controlsp = read(R/'Root_actual_full_V9_cold_controls_independent_admission.json','f00c085928e047447b974a76d8efc01750e7dd4347bfd9aefadadeed4da14642')
    assert controls['status'] == 'QUALIFIED_COMPLETE_ACTUAL_ORIGINAL_THREE_CONTROLS_ONLY_READY_FOR_UNIQUE_FINALIZATION'
    b, bp = read(own['binding']['path'],own['binding']['sha256'])
    assert b['caps'] == s['original_caps_complete_unchanged'] == controls['original_caps']
    assert b['caps'] == dict(rss_cap_mib=512,control_stage_seconds=60,control_total_seconds=120,control_archive_reserve_bytes=67108864,cold_total_seconds=43200,min_free_bytes=8*2**30,history_cap_bytes=96*2**30,threads=1,children_at_once=1,retries=0)
    policy = s['reference_policy_boundary']
    assert policy == controls['reference_policy_boundary']
    assert policy['unchanged_legacy_case_spec_active_batches'] == 250 and policy['separate_frozen_recipe_fixed_history_active_batches'] == 2000
    assert (policy['first_active_statepoint'],policy['last_active_statepoint']) == (101,2100)
    assert policy['original_all8_checks_required'] == ['input_equivalence','source_convergence','block_stability','statistical_resolution','keff','scalar_flux','nu_fission','currents_balance_symmetry']
    pin(policy['source_recipe_path'],policy['source_recipe_sha256'])
    graph_review, grp = read(GD/'REPORT.json','891ba5161ae1759187bd5f840419e2b1cc8125aba8865ffed4476121e30af0ba')
    bg, bgp = read(graph_review['inherited_complete_binding_graph_report']['path'],graph_review['inherited_complete_binding_graph_report']['sha256'])
    mpath = next(p for p in bg['additional_expected_files'] if p.endswith('/rank1_factor_cache_admission.json') and '/runtime/' not in p)
    m, mp = read(mpath,bg['additional_expected_files'][mpath]); expected = dict(m['files']); expected.update(bg['additional_expected_files'])
    assert list(expected.items()) == list(b['files'].items()) and len(expected) == 37395 and digest(expected) == graph_review['expected_map_sha256']
    graph, graphpin = read(graph_review['graph_whole_pin']['path'],graph_review['graph_whole_pin']['sha256'])
    canonical = {row['path']:row['sha256'] for row in graph['canonical_files']}
    assert len(canonical) == 35647 and digest({p:identity(p) for p in canonical}) == graph_review['canonical_full_seven_field_beforeafter_digest']
    assert digest({p:identity(p) for p in m['files']}) == graph_review['metadata37339_beforeafter_identity_digest']
    assert [H['current_graph_namespace'](row,canonical) for row in graph['namespaces']] == graph_review['namespaces86_beforeafter']
    assert H['aliases_and_absences'](graph,canonical) == graph_review['aliases186_absences445_beforeafter']
    # All four current namespaces remain pre-native; no old iteration state is resumed.
    current_namespaces = {}
    for label, root, count in [('source',Path(tr['actual_config']['path']),31)]:
        pass
    cfg, cfgpin = read(Path('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/Root_phase_config.json'))
    for key,count in [('source',31),('work',56),('terminal',12),('controlTerminal',3)]:
        root = Path(cfg[key]); names = sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
        assert len(names) == count and not any(p.is_symlink() for p in root.rglob('*'))
        current_namespaces[key] = {'root':str(root),'regular_files':count,'names':names}
    assert all(not os.path.lexists(work/name) for name in ('AAA','ABA','archives','training','cold_source_failure.json','cold_source_complete_result.json','cold_closeout_seal.json'))
    assert not os.path.lexists(Path(cfg['terminal'])/'terminal_return.json')
    roots = H['dynamic_roots'](b['resource_info']['resource_roots'],ART)
    assert len(roots) == 236 and roots == m['component_resource_roots']
    resources = H['resource_inventory'](roots,ART); free = shutil.disk_usage(ART).free; reserve = 20971764748
    assert resources['artifact_bytes']+reserve < 96*2**30 and free-reserve >= 8*2**30
    storage, storagepin = read(ROOT/'validation/storage_cleanup_nineteenth_20261009/Root_actual_storage_closeout.json','e54bac07e53f0b02f29886685536717dcb35158fdf5f38333cdc4829a7289022')
    assert storage['whole_existing_protected_set_preserved_after_report_save'] is True
    assert storage['protected_counts'] == dict(files=160404,links=669,directories=7064)
    recorder = Path('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/record_actual_phase_terminal.py')
    recorderpin = pin(recorder,'f14d84493fa81d49b5dfa0749cc72bf4bef96ed8317b99475ed254bd1f0bb3f0')
    pure = runpy.run_path(str(recorder),run_name='root_pure_command_derivation_only')
    cli, handoff = pure['expected_commands']('cold',cfg['future_values'])
    assert len(cli) == 9 and cli[2] == 'run-AAA' and cli[6] == newpin['sha256']
    for row in fresh: assert identity(row['path']) == row['identity']
    dest = R/'cold_v9_actual_full_finalization_independent_review'; assert not dest.exists();dest.mkdir();copies=[]
    for source,label in [(SD,'source_environment_witness'),(TD,'typed_original_inverse'),(FD,'R19_fresh_typed_namespace')]:
        for p in sorted(source.rglob('*')):
            if p.is_dir(): continue
            assert p.is_file() and not p.is_symlink(); rec=pin(p); q=dest/label/p.relative_to(source);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());assert pin(q)['sha256'] == rec['sha256'];copies.append({'source':rec,'destination':str(q)})
    q=dest/'Root_admission_source.py';q.write_bytes(Path(__file__).read_bytes());assert pin(q)['sha256']==pin(__file__)['sha256']
    report = dict(schema='AXMAT_ROOT_V9_ACTUAL_ORIGINAL_FINALIZATION_FULL_COMPLEMENTARY_ADMISSION_V1',status='QUALIFIED_COMPLETE_ACTUAL_FINALIZATION_INPUT_ONLY_READY_FOR_UNIQUE_ORIGINAL_COLD_AAA',actual_finalization_tool=dict(actual,closed=True),actual_finalization_terminal=ep,actual_original_controls_admission=controlsp,source_report=sp,typed_report=tp,current_R19_typed_report=fp,actual_source_review_tool=sr['actual_tool_result'],actual_typed_review_tool=tr['actual_tool'],current_R19_typed_receipt=frp,fresh_fullSHA_and_seven_identity_pins=len(fresh),prepared_cold=newpin,original_prepared=oldpin,only_own_child_supervision_added=True,whole_original_typed_order_float64bits_and_serialized_inverse_exact=True,supervision_all_three_actual_descriptors=own,complete_expected_files=37395,canonical_files=35647,new_35GB_scientific_payload_read=False,current_namespaces=current_namespaces,current_complete_dynamic_resources=resources,current_disk_free_bytes=free,future_AAA_reserve_bytes=reserve,original_caps=b['caps'],reference_policy_boundary=policy,storage_R19_preservation=storagepin,pure_recorder=recorderpin,source_derived_unique_original_cold_CLI=cli,source_derived_original_handoff=handoff,actual_execve_syscall_trace=None,evidence_copies=copies,native_actual_tool=None,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,scientific_qualification=False)
    target=R/'Root_actual_full_V9_cold_finalization_independent_admission.json';assert not target.exists();target.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':report['status'],'admission':pin(target),'fresh_fullSHA_and_seven_identity_pins':len(fresh),'current_artifact_bytes':resources['artifact_bytes'],'free_bytes':free,'CLI':cli,'copied_evidence':len(copies),'science':False}),flush=True)

if __name__ == '__main__': main()
