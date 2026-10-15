"""Seal only existing finite TMP evidence; no further project or historical reads."""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).parent
names = ('review_script.py','REVIEW.json','REPORT.txt','complete_remaining_review_script.py','FINAL_REVIEW.json','FINAL_REPORT.txt','finish_encoded_metadata_tail_review.py','FINAL_VERIFIED_REVIEW.json','FINAL_VERIFIED_REPORT.txt','verify_remaining_encoded_scope_actual.py','VERIFIED_REVIEW.json','VERIFIED_REPORT.txt','actual_readonly_tool_returns.json','seal_finite_review.py')
assert len(names) == len(set(names)) == 14

def pin(name):
    p = OUT/name
    before = p.stat()
    raw = p.read_bytes()
    after = p.stat()
    keys = ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
    before_id = [getattr(before,k) for k in keys]
    assert before_id == [getattr(after,k) for k in keys] and len(raw) == before.st_size
    return raw, dict(path=str(p),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=len(raw),identity7=before_id)

raw, final_pin = pin('VERIFIED_REVIEW.json')
assert final_pin['sha256'] == 'b5f1bd2740e42a72a2dfd30cab68cc6a402adc103a9c7f93e15810e5e7d2ee9f'
assert final_pin['size_bytes'] == 283658
r = json.loads(raw)
assert r['status'] == 'ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE'
assert len(r['checks']) == 973 and all(type(v) is bool and v is True for v in r['checks'].values())
assert len(r['file_pins']) == 87 and r['blocking_findings'] == []
assert r['qualification']['actual_complete_PREP_resource_evidence_verified'] is True
assert all(type(v) is bool and v is False for k,v in r['qualification'].items() if k != 'actual_complete_PREP_resource_evidence_verified')
actual = json.loads(pin('actual_readonly_tool_returns.json')[0])
returns = actual['actual_readonly_tool_returns']
assert len(returns) == 4
assert [x['actual_tool_return']['exit_code'] for x in returns] == [1,1,1,0]
assert [x['actual_tool_return']['chunk_id'] for x in returns] == ['0ca96a','dc1edf','1d63a5','813607']
for entry in returns:
    tool = entry['actual_tool_return']
    assert type(tool['exit_code']) is int and 'session_id' not in tool
    assert entry['actual_exit_code_typed_integer'] is True and entry['actual_tool_closed_without_live_session'] is True and entry['production_business_retry'] is False
members = [pin(name)[1] for name in names]
assert set(p.name for p in OUT.iterdir()) == set(names)
manifest = dict(schema='AXMAT_V19_INDEPENDENT_ACTUAL_COMPLETE_PREP_FINITE_REVIEW_SEALED_MANIFEST_V1',status='SEALED_ACTUAL_COMPLETE_PREP_EVIDENCE_PASS_ONLY_NOT_BUILD_INPUT_NATIVE_SCIENCE',members=members,member_count=14,final_review=final_pin,all_973_checks_typed_true=True,actual_readonly_final_tool=dict(chunk_id='813607',exit_code=0,exit_code_typed_integer=True,closed_without_live_session=True),actual_previous_three_readonly_exit1_preserved=True,only_reviewer_archive_storage_wrapper_internal_scope_assumptions_corrected=True,original_PREP_business_retries_still_zero=True,actual_PREP_root_tool_chunk_id='c5790b',actual_PREP_root_session_id=2985,actual_PREP_root_integer_exit0_closed=True,actual_PREP_root_not_repolled_after_close=True,actual_PREP_child_PID=96184,whole_seconds=199.32746954192407,child_seconds=198.1557341669686,sampled_peak_rss_mib=473.09375,namespace_regular_files_verified=68,namespace_subdirectories_verified=14,namespace_symlinks_verified=0,frozen_source_files_verified=42,source_inventory_files_verified=11,original_pinned_inputs_full_EOF_SHA7ID_verified=51,unique_files_full_EOF_SHA7ID_verified=87,graph_metadata_counts=r['graph_metadata_counts'],original_caps=r['original_caps'],qualification=r['qualification'],scope=dict(project_import_or_helper_API_called=False,business_or_numerical_program_executed=False,guard_or_resource_check_called=False,canonical_H_S_O_T_D_E_or_original_inputs_written=False,whole_INPUT_build_native_scientific_or_balance_credit=False,cleanup_performed=False))
with (OUT/'sealed_manifest.json').open('x') as f:
    json.dump(manifest,f,ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)
    f.write('\n')
for member in members:
    assert pin(Path(member['path']).name)[1] == member
raw, seal_pin = pin('sealed_manifest.json')
print(json.dumps(dict(status=manifest['status'],directory=str(OUT),manifest_sha256=seal_pin['sha256'],manifest_bytes=seal_pin['size_bytes'],member_count=14,final_review_sha256=final_pin['sha256'],final_review_bytes=final_pin['size_bytes'],actual_readonly_final_tool_integer0_closed=True,all973_checks_typed_true=True,original_PREP_whole_seconds=199.32746954192407,original_PREP_sampled_peak_rss_mib=473.09375,project_import_API_guard_or_business_called=False,whole_INPUT_build_native_science_credit=False),indent=2))
