#!/usr/bin/env python3
"""Interpret existing B4 failure metadata; never open any original product body.

This is a distinct supplement to the frozen prior post. It preserves its []
child-code observation, and binds the separate watchdog and completed-entry
records. It does not repeat compression, decompression, or Root's byte control.
"""
import argparse
import hashlib
import json
import pathlib
import stat
import time

AUTHOR = '/root/b2_build_source_peer'
EXECUTOR = '/root/b_capture_actual_post_source'
HERE = pathlib.Path(__file__).absolute().parent
B4 = HERE.parent
OUT = pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-current-B4-complete-product-lossless-archive-20261015-v1')
STATUS = 'PASS_SUPPLEMENTAL_B4_FAILURE_CHILD1_MEMBER0_RECORDED_FACTS_METADATA_ONLY'
FLAGS = {
    'compression_repeated': False, 'decompression_repeated': False,
    'original_plain_payload_body_opened': False,
    'original_plain_payload_SHA_recomputed': False,
    'scientific_values_decoded': False, 'result_values_decoded': False,
    'native_executed': False, 'compiler_executed': False,
    'worker_or_guard_helpers_imported': False, 'Source_GEN_or_publication_executed': False,
    'files_deleted': False, 'plain_retirement_authorized': False,
    'archive_all4_complete': False, 'archive_all4_success_inferred': False,
    'physics_qualified': False, 'scientific_accuracy_qualified': False,
    'full_reference_qualified': False, 'AAA_qualified': False,
    'ABA_admitted': False, 'goal_complete': False,
}


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def current(p):
    need(type(p) is dict and set(p) == {'path', 'sha256', 'size_bytes', 'identity'}, 'invalid full-pin schema')
    need(type(p['path']) is str and pathlib.Path(p['path']).is_absolute(), 'non-absolute pin path')
    need(type(p['sha256']) is str and len(p['sha256']) == 64 and all(c in '0123456789abcdef' for c in p['sha256']), 'invalid SHA')
    need(type(p['size_bytes']) is int and p['size_bytes'] >= 0, 'invalid size')
    need(type(p['identity']) is list and len(p['identity']) == 7 and all(type(x) is int for x in p['identity']), 'invalid current7')
    path = pathlib.Path(p['path'])
    s = path.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_nlink == 1, 'not single-link regular file')
    need(identity(s) == p['identity'] and s.st_size == p['size_bytes'], 'current7 changed: ' + str(path))
    return path


def full(p, max_bytes, keep=False):
    path = current(p)
    need(p['size_bytes'] <= max_bytes, 'full read exceeds role bound')
    saved = None
    for iteration in range(2):
        h = hashlib.sha256()
        count = 0
        chunks = [] if keep and iteration == 0 else None
        with path.open('rb') as f:
            for block in iter(lambda: f.read(1024 * 1024), b''):
                count += len(block)
                need(count <= max_bytes, 'stream exceeds role bound')
                h.update(block)
                if chunks is not None:
                    chunks.append(block)
        need(count == p['size_bytes'] and h.hexdigest() == p['sha256'], 'full SHA/length changed: ' + str(path))
        current(p)
        if chunks is not None:
            saved = b''.join(chunks)
    return saved


def meta(p):
    return json.loads(full(p, 8 * 1024 * 1024, True).decode('utf-8'))


def pin(p):
    s = p.lstat()
    raw = p.read_bytes()
    h = hashlib.sha256(raw).hexdigest()
    need(hashlib.sha256(p.read_bytes()).hexdigest() == h and identity(p.lstat()) == identity(s), 'own report changed')
    return {'path': str(p), 'sha256': h, 'size_bytes': len(raw), 'identity': identity(s)}


def genuine_return(v, code, chunk):
    need(type(v) is dict and type(v.get('exit_code')) is int and v['exit_code'] == code, 'wrong genuine integer return')
    need(v.get('chunk_id') == chunk and 'session_id' not in v, 'wrong terminal tool object')


def main():
    started = time.monotonic()
    ap = argparse.ArgumentParser(allow_abbrev=False)
    for name in ['author-freeze-pin', 'Root-tools-pin', 'Host-pin', 'prior-post-pin', 'prior-post-tools-pin']:
        ap.add_argument('--' + name, required=True)
    ap.add_argument('--executor-task-name', required=True)
    args = ap.parse_args()
    need(args.executor_task_name == EXECUTOR and EXECUTOR != AUTHOR, 'independent executor required')
    freeze_pin = json.loads(args.author_freeze_pin)
    freeze = meta(freeze_pin)
    need(freeze['schema'] == 'SUPPLEMENTAL_B4_FAILURE_MEMBER0_METADATA_SOURCE_AUTHOR_FREEZE_V1', 'wrong author freeze')
    need(freeze['Source_author_task'] == AUTHOR and freeze['independent_executor_task'] == EXECUTOR, 'wrong identities')
    need(freeze['source_only'] is True and freeze['supplement_executed_by_author'] is False, 'author ran supplement')
    supplied = {
        'Root_tools': json.loads(args.Root_tools_pin), 'Host': json.loads(args.Host_pin),
        'prior_post': json.loads(args.prior_post_pin),
        'prior_post_tools': json.loads(args.prior_post_tools_pin),
    }
    expected = freeze['exact_input_role_pins']
    need(supplied == {k: expected[k] for k in supplied}, 'argument pin differs from frozen role')
    own = freeze['supplement_Source_pin']
    need(pathlib.Path(own['path']) == pathlib.Path(__file__).absolute(), 'wrong supplement Source path')
    full(own, 8 * 1024 * 1024)
    raw, host, prior, prior_tools = [meta(supplied[k]) for k in ['Root_tools', 'Host', 'prior_post', 'prior_post_tools']]
    need(raw['schema'] == 'ROOT_CURRENT_B4_ARCHIVE_ACTUAL24_TRUE_TOOL_RETURNS_V1', 'wrong actual raw schema')
    need(raw['observed_closed'] is True and type(raw['original_integer_exit_code']) is int and raw['original_integer_exit_code'] == 1, 'Root1 not retained')
    need(raw['actual_execution_permission_mode'] == 'require_escalated' and raw['actual_retried'] is False, 'permission/retry changed')
    genuine_return(raw['actual_terminal_return'], 1, '434819')
    initial = raw['initial_actual_return']
    need(initial['chunk_id'] == '2da97b' and type(initial['session_id']) is int and initial['session_id'] == 6673 and 'exit_code' not in initial, 'wrong actual initial return')
    need(host['schema'] == 'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_GUARDED_HOST_REPORT_V1', 'wrong Host schema')
    need(host['status'] == 'FAILED_ARCHIVE_NO_RETRY_ALL_ORIGINALS_RETAINED', 'all4 failure not retained')
    need(host['failure'] == "RuntimeError('own-child stage failed; no retry')" and host['retries'] == 0, 'Host failure changed')
    need(host['actual_watchdog'] is None and host['actual_child_receipt'] is None, 'original NULL Host fields changed')
    need(host['all4_original_products_current7_retained'] is True and host['archive_complete'] is False and host['plain_retirement_allowed'] is False, 'Host retained-originals facts changed')
    need(prior['schema'] == 'CURRENT_B4_ARCHIVE_ACTUAL_FAILURE_FACTS_METADATA_POST_V1' and prior['status'] == 'PASS_FAILURE_FACTS_ONLY' and prior['failure'] is None, 'wrong original post')
    need(prior['actual_Root_tools_pin'] == supplied['Root_tools'] and prior['actual_Host_report_pin'] == supplied['Host'], 'original post role mismatch')
    need(type(prior['actual_Root_integer_exit_code']) is int and prior['actual_Root_integer_exit_code'] == 1 and prior['actual_recorded_child_integer_exit_codes'] == [], 'original [] observation changed')
    need(prior['absent_child_code_invented'] is False and prior['child_code_inferred_from_Root_return'] is False and prior['archive_success_or_roundtrip_inferred'] is False, 'original post invented a fact')
    need(prior_tools['schema'] == 'CURRENT_B4_ARCHIVE_FAILURE_FACTS_ACTUAL_METADATA_POST_TRUE_TOOL_RETURNS_V1' and prior_tools['observed_closed'] is True, 'wrong original post tools')
    need(type(prior_tools['original_integer_exit_code']) is int and prior_tools['original_integer_exit_code'] == 0 and prior_tools['post_retried'] is False, 'wrong original post0')
    genuine_return(prior_tools['actual_review_return'], 0, 'f67eab')
    stdout = json.loads(prior_tools['actual_review_return']['output'])
    need(stdout == {'status': 'PASS_FAILURE_FACTS_ONLY', 'review_pin': supplied['prior_post']}, 'original post stdout pin mismatch')
    need(prior_tools['actual_executor_task'] == AUTHOR and prior_tools['Source_author_task'] == EXECUTOR, 'original post author/executor mismatch')
    sf = meta(expected['original_Source_freeze'])
    hf = meta(expected['original_Host_freeze'])
    binding = meta(expected['original_binding'])
    need(host['source_freeze_pin'] == expected['original_Source_freeze'] and host['host_freeze_pin'] == expected['original_Host_freeze'] and host['binding_pin'] == expected['original_binding'], 'actual Host freeze bindings changed')
    need(sf['schema'] == 'CURRENT_B4_LOSSLESS_ARCHIVE_SOURCE_FREEZE_V1' and hf['schema'] == 'CURRENT_B4_LOSSLESS_ARCHIVE_HOST_FREEZE_V1', 'wrong original freeze schemas')
    need(host['original_caps'] == hf['original_caps'] == binding['original_caps'] == freeze['unchanged_original_caps'], 'original caps changed')
    need(sf['complete_source_file_pins'] == freeze['unchanged_original_five_core_Source_pins'] and len(sf['complete_source_file_pins']) == 5, 'original Source table changed')
    for p in sf['complete_source_file_pins']:
        full(p, 8 * 1024 * 1024)
    need(sf['execution_binding_pin'] == expected['original_binding'] and hf['selected_source_freeze_pin'] == expected['original_Source_freeze'], 'original Source binding mismatch')
    need(binding['schema'] == 'CURRENT_B4_COMPLETE_PRODUCT_LOSSLESS_ARCHIVE_BINDING_V1', 'wrong archive binding schema')
    need(binding['bounded_total_output_bytes'] == 64 * 1024 * 1024 and binding['bounded_archive_payload_bytes'] == 56 * 1024 * 1024 and binding['bounded_Source_metadata_bytes'] == 16 * 1024 * 1024, 'archive bounds changed')
    need(binding['metadata_runtime_headroom_bytes'] == 8 * 1024 * 1024, 'original archive metadata headroom changed')
    products = binding['all4_product_pins']
    need(len(products) == 4 and [pathlib.Path(p['path']).name for p in products] == ['m.xsm', 'u.asc', 'a.asc', 't.asc'], 'wrong original four roles')
    for p in products:
        current(p)
    rows = prior['new_partial_output_blind_fullEOF_twice_pins']
    need(len(rows) == 10 and len({p['path'] for p in rows}) == 10, 'wrong ten partial outputs')
    table = {p['path']: p for p in rows}
    need(len(host['records']) == 1 and prior['actual_stage_records'] == host['records'], 'stage record changed')
    record = host['records'][0]
    need(record['label'] == 'archive-stage/serial_B4_complete_product_byte_archive' and record['status'] == 'FAILED' and record['error'] == 'own-child stage failed; no retry', 'wrong failed stage record')
    watch_path = OUT / (record['label'] + '.watchdog.json')
    watch_pin = table[str(watch_path)]
    watch = meta(watch_pin)
    need(watch_pin == expected['standalone_watchdog'], 'wrong standalone watchdog role')
    need(watch['command'] == record['command'], 'watchdog command differs from actual failed stage')
    need(type(watch['returncode']) is int and watch['returncode'] == 1 and watch['elapsed_seconds'] == 9.668703583010938 and watch['sampled_peak_rss_mib'] == 60.078125, 'actual child1 facts changed')
    need(watch['limit_failure'] is None and watch['rss_cap_mib'] == 512 and 0 < watch['wall_cap_seconds'] <= 600 and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True, 'actual watchdog limits changed')
    failure_pin = table[str(OUT / 'FIRST_ARCHIVE_FAILURE.json')]
    need(failure_pin == expected['first_archive_failure'], 'wrong first failure role')
    failure = meta(failure_pin)
    need(failure['schema'] == 'CURRENT_B4_LOSSLESS_ARCHIVE_FIRST_FAILURE_V1' and failure['phase'] == 'ARCHIVE_1', 'wrong first failure phase')
    need(failure['failure'] == "RuntimeError('all4 gzip payload below56MiB; no compression assumption')", 'payload hard-bound failure changed')
    need(failure['original_product_files_deleted'] is False and failure['retry_performed'] is False, 'failure deleted/retried')
    need(len(failure['completed_entry_pins']) == 1, 'not uniquely completed entry000')
    entry_pin = failure['completed_entry_pins'][0]
    need(entry_pin == expected['completed_entry000'] == table[str(OUT / 'archive_entry_000.json')], 'completed entry pin mismatch')
    entry = meta(entry_pin)
    need(entry['ordinal'] == 0 and entry['actual_B_capture_product_name'] == 'm.xsm' and entry['original_plain_full_pin'] == products[0], 'wrong member000 original role')
    need(entry['original_product_is_complete'] is True and entry['original_plain_preserved'] is True and entry['exact_original_plain_bytes_recoverable'] is True, 'Root single-member completion records absent')
    need(entry['compression_input_SHA'] == entry['streamed_decompressed_SHA'] == products[0]['sha256'], 'recorded single-member SHA unequal')
    need(type(entry['compression_input_length']) is int and type(entry['streamed_decompressed_length']) is int and entry['compression_input_length'] == entry['streamed_decompressed_length'] == products[0]['size_bytes'], 'recorded single-member lengths unequal')
    need(entry['scientific_values_decoded'] is False and entry['result_values_decoded'] is False, 'member science decoding claimed')
    gzip0 = entry['compressed_archive_full_pin']
    need(gzip0 == expected['completed_gzip000'] == table[str(OUT / 'archives/000_m.xsm.gz')], 'wrong complete gzip000 role')
    need(gzip0['size_bytes'] == 33559716, 'wrong complete gzip000 length')
    full(gzip0, 56 * 1024 * 1024)
    partial1 = table[str(OUT / 'archives/001_u.asc.gz')]
    need(partial1 == expected['incomplete_gzip001'] and partial1['size_bytes'] == 25099039, 'wrong partial gzip001 role')
    current(partial1)
    need(failure['partial_archive_paths'] == [gzip0['path'], partial1['path']], 'partial archive path roles changed')
    need(not (OUT / 'archive_entry_001.json').exists()
         and not (OUT / 'CURRENT_B4_LOSSLESS_ARCHIVE_INDEX.json').exists()
         and not (OUT / 'ACTUAL_CURRENT_B4_LOSSLESS_ARCHIVE_REPORT.json').exists(), 'unrecorded complete all4 receipt exists')
    for p in supplied.values():
        current(p)
    for p in products:
        current(p)
    report = {
        'schema': 'SUPPLEMENTAL_B4_ACTUAL_FAILURE_CHILD1_MEMBER0_METADATA_FACTS_V1',
        'status': STATUS, 'failure': None, 'metadata_only': True,
        'author_freeze_pin': freeze_pin, 'reviewer_Source_pin': own,
        'Source_author_task': AUTHOR, 'actual_executor_task': EXECUTOR,
        'actual_post_not_executed_by_Source_author': True,
        'actual_Root_tools_pin': supplied['Root_tools'], 'actual_Host_report_pin': supplied['Host'],
        'prior_post_pin': supplied['prior_post'], 'prior_post_tools_pin': supplied['prior_post_tools'],
        'actual_Root_integer_exit_code': 1, 'original_prior_post_integer_exit_code': 0,
        'original_prior_post_recorded_child_integer_exit_codes': [],
        'original_Host_actual_watchdog': None, 'original_Host_actual_child_receipt': None,
        'original_Host_or_prior_post_modified': False,
        'standalone_watchdog_pin': watch_pin, 'standalone_watchdog': watch,
        'supplemental_actual_recorded_child_integer_exit_codes': [watch['returncode']],
        'child_code_inferred_from_Root_return': False,
        'first_archive_failure_pin': failure_pin, 'first_archive_failure': failure,
        'uniquely_completed_entry000_pin': entry_pin, 'recorded_complete_member000': entry,
        'current_complete_member000_gzip_blind_fullEOF_twice_pin': gzip0,
        'current_original_all4_plain_current7_only_pins': products,
        'recorded_compression_input_and_streamed_decompressed_SHA_length_equal_original_full_pin': True,
        'Root_recorded_single_member_complete_facts_verified_metadata_only': True,
        'streamed_decompressed_bytes_independently_recomputed_by_supplement': False,
        'future_Root_independent_single_member_stream_control_pin': None,
        'incomplete_gzip001_current7_only_pin': partial1,
        'incomplete_member001_success_inferred': False,
        'unchanged_original_five_core_Source_pins': sf['complete_source_file_pins'],
        'original_archive_bounds_unchanged': True, 'wall_seconds': time.monotonic() - started,
        **FLAGS,
    }
    report_path = HERE / 'REVIEW.json'
    with report_path.open('x') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(json.dumps({'status': STATUS, 'review_pin': pin(report_path)}))


if __name__ == '__main__':
    main()
