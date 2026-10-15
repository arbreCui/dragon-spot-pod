"""Bounded failure-facts review. Standard library only; no scientific file bodies."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

BASE = Path(__file__).absolute().parent
ENTRY = BASE.parent
START = time.monotonic()
READ_CAP = 8 * 2**20
FLAGS = ('physics_qualified', 'complete_reaction_authority_qualified',
         'full_reference_qualified', 'formal_H150_NZ48_full_controls_qualified',
         'historical_machine_bit_replay', 'historical_native_RAM_bits_verified',
         'original_XSM_memory_bits_verified', 'scientific_accuracy_qualified',
         'three_plane_qualified', 'GLOBAL_qualified', 'rank_qualified',
         'online_BOOT_qualified', 'AAA_qualified', 'ABA_admitted', 'goal_complete')

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def budget():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == 'darwin' else 1024)
    need(peak < 512 * 2**20 and time.monotonic() - START < 600, 'review own SELF512/stage600')

def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def current(p):
    need(set(p) == {'path', 'sha256', 'size_bytes', 'identity'}, 'exact Python fullPF keys')
    need(type(p['size_bytes']) is int and p['size_bytes'] == p['identity'][4], 'fullPF size')
    q = Path(p['path']); s = q.lstat()
    need(stat.S_ISREG(s.st_mode) and identity(s) == p['identity'], 'current7: ' + str(q))
    return q

def full(p):
    q = current(p)
    need(p['size_bytes'] <= READ_CAP, 'bounded Source/report-metadata role')
    fd = os.open(q, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        need(identity(os.fstat(fd)) == p['identity'], 'opened7')
        parts = []; total = 0; digest = hashlib.sha256()
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk); need(total <= READ_CAP, 'bounded EOF'); digest.update(chunk); parts.append(chunk); budget()
        need(total == p['size_bytes'] and digest.hexdigest() == p['sha256'], 'whole EOF/SHA')
        need(identity(os.fstat(fd)) == p['identity'], 'closed7')
    finally:
        os.close(fd)
    current(p)
    return b''.join(parts)

def actual(d, key, code):
    need(d['observed_closed'] is True and type(d['original_integer_exit_code']) is int
         and d['original_integer_exit_code'] == code, 'genuine closed original integer')
    r = d[key]
    need(type(r['exit_code']) is int and r['exit_code'] == code and 'session_id' not in r, 'genuine terminal return')
    return r

def output_pin(path):
    q = Path(path); s = q.lstat(); data = q.read_bytes()
    need(len(data) <= READ_CAP and identity(q.lstat()) == identity(s), 'own bounded output pin')
    return dict(path=str(q), sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data), identity=identity(s))

def main():
    seed = json.loads((BASE / 'REVIEWER_SOURCE_ONLY_FREEZE.json').read_bytes())
    need(seed['schema'] == 'INDEPENDENT_FULL370_V5_FAILURE_FACTS_REVIEWER_SOURCE_FREEZE_V1', 'own Source freeze')
    full(seed['reviewer_source_pin'])
    pins = seed['bounded_full_eof_role_pins']
    payload = {p['path']: full(p) for p in pins}
    doc = lambda path: json.loads(payload[str(path)])
    host = doc(seed['actual_host_report_pin']['path'])
    plan = doc(ENTRY / 'PLAN.json')
    root = doc(ENTRY / 'ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json')
    terminal = actual(root, 'actual_terminal_return', 1)
    need(root['actual_initial_return']['session_id'] == 3970
         and root['actual_initial_return']['chunk_id'] == 'f7d5ee' and terminal['chunk_id'] == 'c59d97', 'preserved original actual1 route')
    need(host['schema'] == 'ACTUAL_FULL370_REAL_OPERATOR_CONTROL_GUARDED_REPORT_V1'
         and host['status'] == 'ACTUAL_FULL370_REAL_OPERATOR_CONTROL_FAILED_UNQUALIFIED'
         and host['failure'] == "RuntimeError('own-child stage failed; no retry')"
         and host['after_check_error'] is None and host['final_report_resource_check_passed'] is True,
         'actual failed host facts')
    need(host['actual_control_results'] is None and host['actual_watchdog_checks'] == [], 'no admitted child result')
    need(all(host[k] is False for k in FLAGS) and host['formal_SN32_equivalence_claimed'] is False
         and host['stored_native_REAL32_temperature_selection_qualified'] is False
         and host['native_AxMatTone_temperature_mapping_qualified'] is False, 'all qualifications remain false')
    need(host['original_caps'] == plan['original_caps'] == seed['original_caps'], 'original unchanged caps')
    out = Path(plan['planned_actual_output_root'])
    need(out == Path(seed['actual_output_root']), 'literal failed output')
    records = host['records']; need(len(records) == 1 and records[0]['status'] == 'FAILED', 'exact one failed stage')
    r = records[0]
    stages = doc(out / 'operator-control/stages.json')
    need(stages['stages'] == records and r['wall_cap_seconds'] == 600.0
         and r['elapsed_seconds'] < 600 and host['wall_seconds'] < 1800, 'actual retained stage ledger and elapsed')
    watch = doc(out / 'control/full370_real_operator.watchdog.json')
    need(watch['command'] == r['command'] and type(watch['returncode']) is int and watch['returncode'] == 1
         and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
         and watch['limit_failure'] is None and watch['sampled_peak_rss_mib'] == 511.078125
         and watch['rss_cap_mib'] == 512 and watch['elapsed_seconds'] < watch['wall_cap_seconds'] < 600,
         'saved watchdog facts; no watchdog limit kill')
    log = payload[str(out / 'control/full370_real_operator.log')].decode('utf-8')
    need('operator.prepare_white()' in log and 'line 128, in prepare_white' in log
         and 'count += 1; self.budget.check()' in log and 'original childSELF512/stage600' in log,
         'actual white preparation child guard traceback')
    worker = payload[plan['worker_source_pin']['path']].decode('utf-8')
    helper = payload[plan['original_v6_vector_helper_pin']['path']].decode('utf-8')
    operator = payload[plan['mathematical_operator_Source_copy_pin']['path']].decode('utf-8')
    for p in seed['selected_candidate_source_pins']:
        ast.parse(payload[p['path']], filename=p['path'])
    need('def __init__(self):self.started=time.monotonic()' in helper
         and "require(peak<512*2**20 and time.monotonic()-self.started<600,'original childSELF512/stage600')" in helper
         and 'original_budget=helpers.Budget();budget=BoundedBudgetDiagnostic(' in worker
         and 'started=original_budget.started' in worker
         and 'try:return self.inner.check()' in worker
         and worker.index('original_budget=helpers.Budget();budget=BoundedBudgetDiagnostic(') < worker.index('operator.prepare_white()')
         and 'count += 1; self.budget.check()' in operator, 'unchanged original peak/stage guard path')
    need(len(plan['complete_joint_roots']) == 57 and plan['new_control_reserved_bytes'] == 291566880, 'original roots/reservation')
    for p in (plan['historical_retired_A1_SQLite_pin'], plan['historical_retired_A1_pool_pin']):
        need(not os.path.lexists(p['path']), 'exact historical retired pair remains absent')
    need(host['actual_initial_parent_science_fullhash_pins'] == plan['scientific_input_current7_pins'], 'Root original fullhash authority retained')
    science = plan['scientific_input_current7_pins'] + [plan['actual_kernel_library_pin']]
    need(len(science) == 7 and all(p in host['fixed_current_pins'] for p in science), 'science6 and dylib current7 roles')
    for p in host['fixed_current_pins'] + host['owned_runtime_pins']:
        current(p)
    resources = {}
    for role in ('resources_before', 'resources_after', 'resources_after_including_summary_bytes'):
        q = host[role]; joint = q['complete_joint']; history = q['original_history']
        need(joint['resource_roots'] == plan['complete_joint_roots'] and joint['artifact_budget_bytes'] == 2 * 2**30
             and joint['min_free_bytes'] == 8 * 2**30 and history['artifact_budget_bytes'] == 96 * 2**30
             and history['min_free_bytes'] == 8 * 2**30 and q['host_SELF_peak_bytes'] < 512 * 2**20
             and q['whole_elapsed_seconds'] < 1800
             and joint['artifact_bytes'] + q['explicit_external_metadata_bytes'] + q['host_open_unlinked_bytes'] < 2 * 2**30
             and history['artifact_bytes'] + 20971764748 + 64 * 2**20 < 96 * 2**30
             and joint['disk_free_bytes'] - 20971764748 - 2 * 2**30 >= 8 * 2**30, 'saved actual original resource checks')
        resources[role] = dict(complete_joint_bytes=joint['artifact_bytes'], original_history_bytes=history['artifact_bytes'],
            explicit_external_metadata_bytes=q['explicit_external_metadata_bytes'], host_open_unlinked_bytes=q['host_open_unlinked_bytes'],
            host_SELF_peak_bytes=q['host_SELF_peak_bytes'], whole_elapsed_seconds=q['whole_elapsed_seconds'])
    gen = doc(ENTRY / 'ROOT_SOURCE_PREPARATION_TRUE_TOOL_RETURNS.json'); gen_output = json.loads(actual(gen, 'actual_Source_preparation_return', 0)['output'])
    need(gen_output['ready_pin'] == seed['ready_pin'], 'original Sourcegen0 READY')
    pub = doc(ENTRY / 'ROOT_FINAL_PUBLICATION_TRUE_TOOL_RETURNS.json'); pub_output = json.loads(actual(pub, 'actual_publication_return', 0)['output'])
    receipt = doc(ENTRY / 'FINAL_PUBLICATION_RECEIPT.json')
    need(pub_output['publication_receipt_pin'] == seed['publication_receipt_pin']
         and pub_output['Source_freeze_pin'] == receipt['source_freeze_pin']
         and pub_output['Host_freeze_pin'] == receipt['host_freeze_pin']
         and pub_output['CLI_pin'] == receipt['CLI_pin'], 'original once publication0 retained')
    prior = doc(seed['original_Source_review_pin']['path']); prior_tools = doc(seed['original_Source_review_tools_pin']['path'])
    prior_output = json.loads(actual(prior_tools, 'actual_review_return', 0)['output'])
    need(prior_output['review_pin'] == seed['original_Source_review_pin']
         and prior['status'] == 'PASS_SOURCE_METADATA_SCOPE_WITH_SCIENTIFIC_DOCUMENT_CURRENT7_ONLY', 'prior actual Source review0 retained')
    scientific_docs = [p for p in host['fixed_current_pins'] if p['path'].endswith('_actual_saved_MT5_P0.json')]
    need(len(scientific_docs) == 11 and all(p['path'] not in payload for p in scientific_docs + science), 'no science bodies opened or hashed')
    present = sorted(str(q.relative_to(out)) for q in out.rglob('*') if q.is_file())
    need(present == ['Root_actual_full370_real_operator_control_summary.json',
         'control/ORIGINAL_BUDGET_FAILURE_CHECKPOINT.json', 'control/full370_real_operator.log',
         'control/full370_real_operator.watchdog.json', 'operator-control/stages.json', 'runtime/run_bounded_dragon.py']
         and not os.path.lexists(out / 'control/ACTUAL_FULL370_REAL_OPERATOR_CONTROL.json')
         and not any(q.is_file() for q in (out / 'control/white_cache').glob('*')), 'literal outputs: no child report/cache/result')
    checkpoint=doc(out/'control/ORIGINAL_BUDGET_FAILURE_CHECKPOINT.json')
    need(host['budget_failure_checkpoint_present'] is True
         and host['budget_failure_checkpoint_pin']==next(p for p in pins if p['path']==str(out/'control/ORIGINAL_BUDGET_FAILURE_CHECKPOINT.json'))
         and checkpoint['schema']=='ACTUAL_ORIGINAL_BUDGET_ONCE_FAILURE_CHECKPOINT_V1'
         and checkpoint['status']=='ORIGINAL_BUDGET_EXCEPTION_UNQUALIFIED'
         and checkpoint['phase']=='WHITE_PREPARATION' and checkpoint['check_count_in_phase']==6860
         and checkpoint['check_count_total']==8858 and checkpoint['native_action_count_claimed'] is False
         and checkpoint['count_scope']=='ORIGINAL_BUDGET_CHECK_INVOCATIONS_ONLY_NOT_NATIVE_ACTIONS'
         and checkpoint['original_elapsed_seconds_before_check']<=checkpoint['original_elapsed_seconds_on_exception']<600
         and checkpoint['original_elapsed_seconds_on_exception']==532.1985355840006
         and checkpoint['SELF_ru_maxrss_raw_before_original_check']==checkpoint['SELF_ru_maxrss_raw_on_original_exception']==542736384
         and checkpoint['SELF_ru_maxrss_bytes_before_original_check']==checkpoint['SELF_ru_maxrss_bytes_on_original_exception']==542736384
         and checkpoint['SELF_ru_maxrss_unit']=='bytes' and 542736384>512*2**20
         and checkpoint['original_exception_type']=='RuntimeError'
         and checkpoint['original_exception_repr']=="RuntimeError('original childSELF512/stage600')"
         and checkpoint['original_helper_source_pin']==plan['original_v6_vector_helper_pin']
         and checkpoint['original_budget_instance_type_unchanged'] is True
         and checkpoint['original_budget_check_delegated_every_time'] is True
         and checkpoint['original_caps']==plan['original_caps'], 'exact original SELF peak failure checkpoint, check counts only')
    need(len(payload[str(out/'control/ORIGINAL_BUDGET_FAILURE_CHECKPOINT.json')])<=8192, 'original checkpoint cap')
    need(worker.index('source_min>0')<worker.index('validated_fixture_digest=digest(coefficient)')
         <worker.index('del coefficient,q')<worker.index('operator.prepare_white()')
         <worker.index('digest(coefficient)==validated_fixture_digest')<worker.index('operator.apply(coefficient)'), 'original fixture setup/bitdigest/release assertions preserved')
    need(plan['mathematical_operator_Source_copy_pin']['sha256']=='731b921e0c5f64955c0f4b358b03bfbd70e88f7c1eeaf644c7ff275517ef02f5'
         and payload[plan['mathematical_operator_Source_copy_pin']['path']]==payload[plan['original_mathematical_operator_Source_pin']['path']], 'whole original operator remains unchanged')
    light=doc(ENTRY/'ROOT_FINAL_LIGHT_REVIEW_20261015.json'); light_tools=doc(ENTRY/'ROOT_FINAL_LIGHT_TRUE_TOOL_RETURNS_20261015.json')
    light_output=json.loads(actual(light_tools,'actual_light_return',0)['output'])
    need(light['failure'] is None and light['status']=='PASS_EXACT_CURRENT_CLI24_AND_ORIGINAL57_RESERVATION'
         and light_output['status']==light['status'], 'original actual LIGHT0 status-only proof retained')
    prior_root=doc(ENTRY.parent/'v4/ROOT_ACTUAL24_TRUE_TOOL_RETURNS.json'); actual(prior_root,'actual_terminal_return',1)
    prior_facts=doc(seed['prior_v4_failure_facts_pin']['path']); prior_facts_tools=doc(seed['prior_v4_failure_facts_tools_pin']['path'])
    need(prior_facts['status']=='PASS_FAILURE_FACTS_ONLY' and prior_facts['actual_Root_original_integer_exit_code']==1
         and prior_facts['actual_child_original_integer_exit_code']==1
         and json.loads(actual(prior_facts_tools,'actual_review_return',0)['output'])['review_pin']==seed['prior_v4_failure_facts_pin'], 'v4 Root1/child1 and failure-facts0 retained')
    temperature_root=doc(seed['temperature_root_tools_pin']['path']); temperature_post=doc(seed['temperature_post_tools_pin']['path'])
    need(json.loads(actual(temperature_root,'actual_terminal_return',0)['output'])['report_pin']==seed['temperature_host_current7_pin']
         and json.loads(actual(temperature_post,'actual_review_return',0)['output'])['review_pin']==seed['temperature_post_current7_pin'], 'original temperature Root0/post0 exact pins retained')
    for p in seed['temperature_current7_only_pins']:current(p)
    for p in pins:
        need(full(p) == payload[p['path']], 'second metadata wholeEOF')
    for p in seed['temperature_current7_only_pins']:current(p)
    for p in host['fixed_current_pins'] + host['owned_runtime_pins']:
        current(p)
    for p in (plan['historical_retired_A1_SQLite_pin'], plan['historical_retired_A1_pool_pin']):
        need(not os.path.lexists(p['path']), 'second exact retired absence')
    report = dict(schema='INDEPENDENT_ACTUAL_FULL370_V5_FAILURE_FACTS_METADATA_ASSESSMENT_V1', status='PASS_FAILURE_FACTS_ONLY',
        failure=None, metadata_only=True, actual_Root_original_integer_exit_code=1, actual_child_original_integer_exit_code=1,
        actual_failed_stage_count=1, actual_child_stage_elapsed_seconds=r['elapsed_seconds'], actual_host_wall_seconds=host['wall_seconds'],
        actual_watchdog_elapsed_seconds=watch['elapsed_seconds'], actual_watchdog_sampled_peak_rss_mib=watch['sampled_peak_rss_mib'],
        actual_watchdog_limit_failure=None, liveness_group_cleanup=True, exact_child_ru_maxrss_logged=True, exact_child_SELF_ru_maxrss_bytes_before_original_check=542736384, exact_child_SELF_ru_maxrss_bytes_on_original_exception=542736384, exact_child_SELF_ru_maxrss_MiB=517.59375, original_budget_elapsed_seconds_on_exception=checkpoint['original_elapsed_seconds_on_exception'], actual_checkpoint_phase='WHITE_PREPARATION', original_budget_check_count_in_phase=6860, original_budget_check_count_total=8858, checkpoint_count_scope='ORIGINAL_BUDGET_CHECK_INVOCATIONS_ONLY_NOT_NATIVE_ACTIONS', native_action_count_claimed=False, actual_budget_failure_checkpoint_pin=host['budget_failure_checkpoint_pin'],
        failure_location='prepare_white original child SELF512/stage600 conjunction',
        confirmed_failure='Original SELF512 guard violated: exact peak542736384B exceeds536870912B while original elapsed532.198535584s is below600',
        watchdog_RSS_kill_claimed=False, stage600_timeout_claimed=False, actual_host_report_pin=seed['actual_host_report_pin'],
        actual_Root_true_tools_pin=seed['actual_Root_true_tools_pin'], original_Sourcegen_integer_exit_code=0,
        original_publication_integer_exit_code=0, original_Source_review_integer_exit_code=0,
        bounded_full_eof_role_pins=pins, new_failure_report_artifacts_fullEOF_twice=5,
        fixed_current7_pins_verified_twice=host['fixed_current_pins'], fixed_current7_count=len(host['fixed_current_pins']),
        owned_runtime_current7_pins_verified_twice=host['owned_runtime_pins'], scientific_inputs_and_dylib_current7_only=science,
        scientific_extraction_documents_current7_only=scientific_docs, exact_retired_pair_absent_twice=True,
        child_report_present=False, white_cache_files_present=False, actual_control_results_present=False,
        saved_actual_resource_checks=resources, fresh_history_scan_claimed=False, original_caps=host['original_caps'],
        original_complete_joint_roots=plan['complete_joint_roots'], original_reserved_bytes=291566880,
        existing_failed_evidence_rewritten=False, historical_v4_Root_integer_exit_code1_preserved=True, historical_v4_child_integer_exit_code1_preserved=True, temperature_original_Root0_and_post0_preserved_current7_only=True, temperature_current7_only_pins_verified_twice=seed['temperature_current7_only_pins'], temperature_scientific_reports_body_opened_or_hashed=False, original_LIGHT_integer_exit_code=0, setup_fixture_bitdigest_and_release_assertions_preserved=True, whole_mathematical_operator_unchanged=True, retry_executed=False, science_bodies_read=False, science_bodies_hashed=False,
        helper_imported=False, compiler_executed=False, business_executed=False, numerical_executed=False,
        files_deleted=False, **{k: False for k in FLAGS})
    target = BASE / 'REVIEW.json'; need(not os.path.lexists(target), 'fresh review output only')
    with target.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, indent=2, allow_nan=False); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    print(json.dumps(dict(status=report['status'], review_pin=output_pin(target)), separators=(',', ':')), flush=True)

if __name__ == '__main__':
    main()
