import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import time

ROOT = Path('/Users/wen/spot')
R9 = ROOT / 'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009'
SOURCE = Path('/private/tmp/spot_v9_cold_actual_PREP_full_source_independent_review_20261009')
GRAPH = Path('/private/tmp/axmat_v9_actual_cold_PREP_graph_resource_independent_review_20261009')
NEXT = Path('/private/tmp/axmat_v9_cold_next_actions_source_scope_20261009')
OUT = R9 / 'cold_v9_actual_full_PREP_independent_review'

def sid(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(p):
    assert p.is_file() and not p.is_symlink(), str(p)
    with p.open('rb') as f:
        before = os.fstat(f.fileno())
        h = hashlib.file_digest(f, 'sha256').hexdigest()
        assert sid(os.fstat(f.fileno())) == sid(before) == sid(p.stat()), str(p)
    return dict(path=str(p), sha256=h, bytes=before.st_size, identity=sid(before))

def obj(p, h=None):
    v = pin(p)
    if h is not None:
        assert v['sha256'] == h
    return json.loads(p.read_bytes())

s = obj(SOURCE / 'REPORT.json', '4abf92d49fc9f8a50f9e410ad8c7c311f0790fb7451a8e6cc98a48b56ea25f24')
g = obj(GRAPH / 'REPORT.json', '2c124560cb591339ee1dbc0b43471db3d28a6b65a843c0381d7cf37607fea39d')
j = obj(GRAPH / 'joint_scope_binding.json', 'df1f768e051618f1f7f1134d398aaa6ee1cc9d965094c7f0c0e938e64ae1e208')
assert s['status'] == g['status'] == j['status'] == 'PASS'
tool = dict(initial_chunk_id='1a53dd', session_id=2047, terminal_chunk_id='d7ffa4', exit_code=0, closed=True)
assert s['actual_PREP_tool'] == g['actual_PREP_Root_tool'] == j['actual_PREP_Root_tool'] == tool
assert type(tool['exit_code']) is int and tool['closed'] is True
assert s['prepared_sha256'] == g['prepared']['sha256'] == j['prepared_sha256'] == '35f8100a753b149b6b100b8bc7154ca1b09f488a464a5068e0ffb826877d6ec7'
assert s['prepare_terminal_sha256'] == g['actual_prepare_receipt']['sha256'] == j['actual_PREP_receipt']['sha256'] == '2bcce12bb05d50b7dabce828f14dc7bd1dbff2a3383af5ac0ab81dbc10d8050a'
assert s['Root_observer_sha256'] == g['Root_observer']['sha256'] == j['Root_observer']['sha256'] == 'c1e24c926bb6aedd909f641717b3a4ec60970ec418aa3f3dfa023b696dd18f16'
for field in ('source31_exact_fullSHA_namespace', 'complete43_local_files_and_all31_runtime_copies_fullSHA',
              'complete_prepared_all_fields_checked', 'all7_other_deck_bytes_unchanged',
              'whole_production_inputs_manifest_inverse_to_original_base_typed_order_floatbits',
              'complete_original_AB_inputs_config_budget_parent_snapshot_control_outputs_preserved',
              'whole_original_producer_admission_inverse_only_current_receiver_SHA',
              'complete_independent_reference2000_and_original8_checks_retained_as_dependency_only',
              'source_FUNCTION_PLAN12_segments_all_same'):
    assert s[field] is True, field
assert s['complete2_axial_decks_inverse_to_original_bytes'] == {
    'bootstrap_axial.x2m': '13a43842e6fe32ea1568e476715f5ca3a0b44c7dbab5744d7667b9cc956e893e',
    'picard_axial.x2m': '0849ed24c071fde68957c32956b55dae619a8801c3e64a38e0a7a03c703b5cc4'}
for field in ('earlier_fullBYTE_35803098221_identity_exact_retained', 'descriptor_union35675_retained',
              'whole65_complete_type_order_values_floatbits_equal', 'original_API_raw65_order_unchanged',
              'prepared_original_cases_budgets_config_inputs_sources_descriptor_resource_fields_complete_equal',
              'SOURCE31_fullSHA_and_identity_unchanged', 'new_OUTPUT43localfiles_plus_prepared44_full_SHA',
              'terminal_exact6_fullSHA', 'resource_before_after_complete_inventory_equal', 'strict_reservation_gate_passed',
              'future_binding_controls_and_cold_outputs_absent'):
    assert g[field] is True, field
assert g['canonical_files'] == 35647 and g['requirement_rows'] == 235528 and g['duplicate_requirement_rows'] == 0
assert len(g['namespaces_before_after86']) == 86 and g['full_metadata_dependency_count'] == 37339
assert g['inherited_canonical_bytes'] == 35803098221
assert g['complete_canonical_before_after_seven_field_identity_digest'] == '44f01a30359e6b7bfd3bf16914b0dcf68699c92213f68d3d8631e4d73545b594'
assert g['current_resources_before'] == g['current_resources_after']
assert g['declared_roots_count'] == g['dynamic_current_roots_count'] == 236
assert g['history_budget_bytes'] == 96 * 2**30 and g['min_free_bytes'] == 8 * 2**30
assert g['fresh_AAA_reserve_bytes'] == 20971764748 and g['original_parent_case_bytes'] == 13265348616
assert s['reference_policy_boundary'] == j['reference_policy_boundary']
assert s['reference_policy_boundary']['unchanged_legacy_case_spec_active_batches'] == 250
assert s['reference_policy_boundary']['separate_frozen_recipe_fixed_history_active_batches'] == 2000
assert len(s['reference_policy_boundary']['original_all8_checks_required']) == 8
for body in (s, j):
    assert all(body[k] is False for k in ('native_RSS_verified', 'AAA_accuracy_qualified', 'ABA_admitted', 'scientific_qualification'))
assert all(g[k] is False for k in ('native_RSS_credit', 'AAA_accuracy_qualified', 'ABA_admitted', 'scientific_qualification'))
assert j['whole_PREP_source_environment_decks_metadata_and_input_graph_resource_scopes_covered'] is True
for receipt, h, expected in [
    (SOURCE / 'actual_readonly_tool_return.json', '7f59e5a3b79ccde4fbeb8a8fc476c1290a48467668296b3861f116436629050a', '5a91a1'),
    (GRAPH / 'actual_readonly_tool_return.json', '66dbf89138ae4af595ed0c3f30392400e67eb4947e77adba756d25958c6e00bc', 'dc11fe'),
    (GRAPH / 'actual_joint_readonly_tool_return.json', '462dd4f1022a059c80e3e54f365afc2fdbaced554071b18505c4ab64f49d46e2', 'd29043')]:
    d = obj(receipt, h)
    a = d['actual_tool_result']
    assert type(a['exit_code']) is int and a['exit_code'] == 0 and a['closed'] is True
    assert a['terminal_chunk_id'] == expected

expected = {}
for v in s['all_fresh_pins'] + list(g['full_read_pins'].values()) + list(j['full_pins'].values()):
    q = dict(path=v['path'], sha256=v['sha256'], bytes=v.get('bytes', v.get('size', v.get('size_bytes'))), identity=v['identity'])
    if q['path'] in expected:
        assert q == expected[q['path']], q['path']
    expected[q['path']] = q
for value in expected.values():
    assert pin(Path(value['path'])) == value, value['path']

cfg = json.loads(Path('/private/tmp/axmat-v9-cold-root-actual-execution-20261009/Root_phase_config.json').read_bytes())
work = Path(cfg['work'])
assert set(p.name for p in work.iterdir()) == {'prepared.json', 'declaration.json', 'decks', 'runtime'}
assert not Path(cfg['controlTerminal']).exists()
assert all(cfg['future_values'][k] is None for k in ('binding_sha256', 'control_seal_sha256', 'control_terminal_sha256', 'prepared_cold_sha256'))
assert obj(work / 'prepared.json')['classification'] == 'PREPARED_NO_TRANSPORT'

OUT.mkdir(exist_ok=False)
copied = []
for directory, name in [(SOURCE, 'source_environment_decks_metadata'), (GRAPH, 'graph_resources_joint'), (NEXT, 'next_actions_source_only')]:
    dest = OUT / name
    dest.mkdir()
    for p in sorted(directory.rglob('*')):
        assert not p.is_symlink(), str(p)
        target = dest / p.relative_to(directory)
        if p.is_dir():
            target.mkdir()
        elif p.is_file():
            original = pin(p)
            with target.open('xb') as f:
                f.write(p.read_bytes())
            saved = pin(target)
            assert saved['sha256'] == original['sha256'] and saved['bytes'] == original['bytes']
            copied.append(dict(source=original, saved=saved))
        else:
            raise ValueError(str(p))
record = dict(schema='AXMAT_ROOT_V9_ACTUAL_COLD_PREP_FULL_COMPLEMENTARY_ADMISSION_V1',
              status='QUALIFIED_COMPLETE_ACTUAL_PREP_INPUT_ONLY_READY_FOR_UNIQUE_CANONICAL_BINDING',
              observed_unix=time.time(), actual_PREP_tool=tool, prepared=pin(work / 'prepared.json'),
              actual_PREP_terminal=pin(Path(cfg['terminal']) / 'prepare_terminal_return.json'),
              source_report_sha256=pin(SOURCE / 'REPORT.json')['sha256'],
              graph_report_sha256=pin(GRAPH / 'REPORT.json')['sha256'],
              joint_scope_sha256=pin(GRAPH / 'joint_scope_binding.json')['sha256'],
              fresh_whole_source_and_metadata_pins=len(expected),
              inherited_full_canonical_inputs=dict(files=35647, bytes=35803098221,
                  current_seven_field_identity_digest=g['complete_canonical_before_after_seven_field_identity_digest'],
                  source_fullBYTE_observation=g['earlier_fullBYTE_proof'], new_full35GB_read=False),
              graph_complete_rows=235528, namespaces=86, aliases=186, absent_inputs=445,
              current_complete_resources=g['current_resources_after'], original_all_caps_retained=True,
              reference_policy_boundary=s['reference_policy_boundary'], evidence_copies=copied,
              actual_binding_tool=None, new_binding_controls_executed=False,
              native_RSS_verified=False, AAA_accuracy_qualified=False, ABA_admitted=False,
              scientific_qualification=False)
with (R9 / 'Root_actual_full_V9_cold_PREP_independent_admission.json').open('x') as f:
    json.dump(record, f, ensure_ascii=False, indent=2, allow_nan=False)
    f.write('\n')
with (OUT / 'Root_admission_source.py').open('xb') as f:
    f.write(Path(__file__).read_bytes())
print(json.dumps(dict(status=record['status'], Root_admission=pin(R9 / 'Root_actual_full_V9_cold_PREP_independent_admission.json'),
                      copied_evidence_files=len(copied), freshly_checked_pins=len(expected), actual_binding_tool=None), ensure_ascii=False))
