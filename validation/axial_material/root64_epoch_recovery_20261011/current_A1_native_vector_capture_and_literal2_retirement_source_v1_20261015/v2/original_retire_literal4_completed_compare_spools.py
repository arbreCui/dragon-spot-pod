"""Source only: Root may retire the four completed comparison spool files once."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

BASE = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/literal4_completed_compare_spool_retirement_20261014_v1')
SOURCE = BASE / 'retire_literal4_completed_compare_spools.py'
PREFIX = Path('/Users/wen/spot/validation/artifacts/axial-material-current-three-plane-raw-macro-compare-after-GENDF-cumulative25-20261014-v1-evidence')
LITERALS = [
    ('A2/original_archive_index.sqlite', 'bf4cac511a1a916207989fca39aa52fc9cd53b7a97cd9137a00605aeed9af72a', [16777229,50187727,33188,1,52441088,1791980279306817934,1791980279306817934]),
    ('A2/original_words.bin', 'cc603381a444eb7a4c0d84ee0c3823eb1b255dac3b7f177a290f89d3c514b5eb', [16777229,50187730,33188,1,150267572,1791980279315954621,1791980279315954621]),
    ('A3/original_archive_index.sqlite', '1c7221ecd185ab490ef90ab2a84006b346dd6ddf13c0d8714c1674f0028e8c77', [16777229,50187739,33188,1,52441088,1791980282810113123,1791980282810113123]),
    ('A3/original_words.bin', '0efa6bcf3a07596af266e6a1d796ed78b500f98a1b9964b0539caf8c6389c2f6', [16777229,50187742,33188,1,150267572,1791980282818463517,1791980282818463517]),
]
TARGETS = [dict(path=str(PREFIX / name), sha256=sha, size_bytes=ids[4], identity=ids) for name, sha, ids in LITERALS]

def require(value, message):
    if value is not True:
        raise RuntimeError(message)

def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def current(pin):
    q = Path(pin['path'])
    s = q.lstat()
    require(q.is_absolute() and stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and
            s.st_uid == os.getuid() and identity(s) == pin['identity'] and
            s.st_size == pin['size_bytes'] and
            not any(p.is_symlink() for p in (q, *q.parents)), 'exact ordinary current7: ' + str(q))
    return q

def full(pin, parse=False):
    q = current(pin)
    sha = hashlib.sha256()
    size = 0
    parts = []
    fd = os.open(q, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        require(identity(os.fstat(fd)) == pin['identity'], 'opened exact7')
        while True:
            raw = os.read(fd, 2**20)
            if not raw:
                break
            sha.update(raw)
            size += len(raw)
            if parse:
                parts.append(raw)
        require(identity(os.fstat(fd)) == pin['identity'], 'after EOF exact7')
    finally:
        os.close(fd)
    current(pin)
    require(size == pin['size_bytes'] and sha.hexdigest() == pin['sha256'], 'complete EOF SHA: ' + str(q))
    return json.loads(b''.join(parts)) if parse else None

def argument_pin(path, sha, seven):
    ids = json.loads(seven)
    require(type(ids) is list and len(ids) == 7 and all(type(v) is int for v in ids), 'seven integer identity')
    return dict(path=str(path),sha256=sha,size_bytes=ids[4],identity=ids)

def snapshot(file, result):
    data = (json.dumps(result,indent=2,allow_nan=False) + '\n').encode()
    file.seek(0)
    file.write(data)
    file.truncate()
    file.flush()
    os.fsync(file.fileno())

def actual_pin(path):
    s = path.lstat()
    return dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=identity(s))

def closure(plan):
    p = plan['closure_pins']
    post = full(p['typed_post_review'], True)
    tools = full(p['typed_post_tools'], True)
    require(post['status'] == 'PASS_ACTUAL_SAVED_THREE_TYPED_PATH_FINITE_POSTVERIFICATION' and
            post['failure'] is None and type(post['actual_Root_integer_exit_code']) is int and
            post['actual_Root_integer_exit_code'] == 0, 'independent closed typed postverification')
    terminal = tools['actual_terminal_return']
    require(tools['observed_closed'] is True and type(tools['original_integer_exit_code']) is int and
            tools['original_integer_exit_code'] == 0 and type(terminal['exit_code']) is int and
            terminal['exit_code'] == 0 and terminal.get('session_id') is None and
            json.loads(tools['actual_full_stdout'])['review_pin'] == p['typed_post_review'], 'genuine typed post closed0')
    root = full(p['typed_root_tools'], True)
    terminal = root['actual_terminal_return']
    receipt = json.loads(terminal['output'])
    require(root['observed_closed'] is True and type(root['original_integer_exit_code']) is int and
            root['original_integer_exit_code'] == 0 and type(terminal['exit_code']) is int and
            terminal['exit_code'] == 0 and terminal.get('session_id') is None and
            receipt['report_pin'] == p['typed_host_report'], 'genuine owning Root closed0')
    host = full(p['typed_host_report'], True)
    result = full(p['typed_result'], True)
    watch = full(p['typed_watchdog'], True)
    full(p['typed_log'])
    old = full(p['original_spool_report'], True)
    require(host['status'] == receipt['status'] == 'ACTUAL_SAVED_THREE_MACRO_TYPED_PATH_COMPARISON_EXIT2_CLOSED_ONLY' and
            host['failure'] is None and host['secondary_failures'] == [] and
            host['final_report_resource_check_passed'] is True and type(watch['returncode']) is int and
            watch['returncode'] == 2 and watch['limit_failure'] is None, 'completed typed child2 with no limit failure')
    require(post['actual_Host_report_pin'] == p['typed_host_report'] and
            post['actual_child_report_pin'] == p['typed_result'] and
            post['actual_Root_true_tool_pin'] == p['typed_root_tools'] and
            post['actual_watchdog_full_pin'] == p['typed_watchdog'] and
            post['actual_log_full_pin'] == p['typed_log'], 'post binds owning closure metadata')
    require(len(result['comparisons']) == 3 and post['total_macro_record_comparisons'] == 58860 and
            post['total_compared_original_words'] == 6792456 and
            result['all_raw_word_mismatches'] == result['all_metadata_mismatches'] ==
            post['all_raw_word_mismatches'] == post['all_metadata_mismatches'] == 0 and
            result['all_three_original_producer_seals_preserved'] is True and
            result['comparison_contract'] == 'EXACT_TYPED_FULL_PATH_KIND_COUNT_WORDS_AND_ALL_RAW_BYTES', 'all three completed typed comparisons')
    for comp, pair in zip(result['comparisons'], plan['original_native_pairs']):
        require(comp['plane'] == pair['plane'] and comp['compared_all_macro_records'] == 19620 and
                comp['compared_original_payload_words'] == 2264152 and
                comp['raw_word_mismatches'] == comp['metadata_mismatches'] == 0 and
                comp['native_sqlite_pin'] == pair['sqlite_pin'] and comp['native_pool_pin'] == pair['native_pool_pin'] and
                all(comp[k] is True for k in ('path_sets_equal','all_original_records_and_typed_root_preserved',
                    'original_archive_not_redecoded','original_orders_not_sorted_or_rewritten')), 'completed original plane spool lifecycle')
        current(comp['detail_pin'])
        original = old['comparisons'][pair['plane'] - 1]
        require(original['archive_pin'] == pair['archive_pin'] and
                pair['sqlite_pin'] in original['all_output_pins'] and
                pair['native_pool_pin'] in original['all_output_pins'], 'original spool producer metadata preserved')
    require(old['all_raw_word_mismatches'] == 9501687 and
            result['original_Root_exit_code_retained'] == host['original_Root_exit_code_retained'] ==
            post['original_compare_Root_exit_code_retained'] == 1 and
            result['original_positional_mismatch_report_not_modified'] is True and
            post['original_compare_budget_failure_and_positional_reports_retained'] is True, 'historical ordinal failure unchanged')
    for data in (post, host, result, old):
        require(all(v is False for k,v in data.items() if k.endswith('_qualified') or
                    k.endswith('_verified') or k in ('ABA_admitted','goal_complete')), 'no scientific qualification')

def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--mode', choices=['check','execute'], required=True)
    for name in ('source','plan'):
        parser.add_argument('--' + name + '-sha256', required=True)
        parser.add_argument('--' + name + '-seven-id', required=True)
    parser.add_argument('--review-pin')
    parser.add_argument('--readonly-receipt-pin')
    args = parser.parse_args()
    source_pin = argument_pin(SOURCE,args.source_sha256,args.source_seven_id)
    plan_pin = argument_pin(BASE / 'PLAN.json',args.plan_sha256,args.plan_seven_id)
    require(Path(__file__).absolute() == SOURCE, 'literal Source location')
    path = BASE / ('READONLY_RECEIPT.json' if args.mode == 'check' else 'EXECUTION_RECEIPT.json')
    result = dict(schema='LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_RECEIPT_V1',mode=args.mode,
        status='STARTED',failure=None,source_pin=source_pin,plan_pin=plan_pin,exact_target_pins=TARGETS,
        actual_released_pins=[],actual_released_bytes=0,completed_temporary_file_lifecycle_only=True,
        sameSHA_duplicate_claim=False,original_Root_exit_code_retained=1,old_reports_rewritten=False,
        business_executed=False,compiler_executed=False,numerical_executed=False,
        physics_qualified=False,scientific_accuracy_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
    # Exclusive claim forbids every retry, including a failed prevalidation attempt.
    with path.open('xb') as file:
        try:
            snapshot(file,result)
            full(source_pin)
            plan = full(plan_pin,True)
            require(plan['schema'] == 'LITERAL4_COMPLETED_COMPARE_SPOOL_RETIREMENT_PLAN_V1' and
                    plan['target_pins'] == TARGETS and plan['planned_released_bytes'] == 405417320 and
                    len({p['sha256'] for p in TARGETS}) == 4, 'literal four distinct spool pins and byte total')
            if args.mode == 'execute':
                require(args.review_pin is not None and args.readonly_receipt_pin is not None, 'reviewed Source and exact readonly receipt required')
                review_pin = json.loads(args.review_pin)
                review = full(review_pin,True)
                require(review['status'].startswith('PASS') and review['failure'] is None and
                        review['source_pin'] == source_pin and review['plan_pin'] == plan_pin, 'peer reviewed exact Source and plan')
                readonly_pin = json.loads(args.readonly_receipt_pin)
                require(readonly_pin['path'] == str(BASE / 'READONLY_RECEIPT.json'), 'literal readonly receipt')
                readonly = full(readonly_pin,True)
                require(readonly['status'] == 'READONLY_READY_EXACT_LITERAL4' and readonly['failure'] is None and
                        readonly['source_pin'] == source_pin and readonly['plan_pin'] == plan_pin and
                        readonly['exact_target_pins'] == TARGETS and readonly['actual_released_pins'] == [] and
                        readonly['actual_released_bytes'] == 0, 'exact successful readonly receipt')
                result.update(review_pin=review_pin,readonly_receipt_pin=readonly_pin)
            closure(plan)
            for pin in plan['preserved_current7_pins']:
                current(pin)
            # Complete EOF validation of all four precedes the first unlink.
            for pin in TARGETS:
                full(pin)
            result['preserved_current7_pins'] = plan['preserved_current7_pins']
            result['closure_pins'] = plan['closure_pins']
            if args.mode == 'execute':
                for pin in TARGETS:
                    q = current(pin)
                    directory = os.open(q.parent,os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
                    try:
                        require(identity(os.stat(q.name,dir_fd=directory,follow_symlinks=False)) == pin['identity'], 'immediate exact target7')
                        os.unlink(q.name,dir_fd=directory)
                        result['actual_released_pins'].append(pin)
                        result['actual_released_bytes'] += pin['size_bytes']
                        os.fsync(directory)
                    finally:
                        os.close(directory)
                    result['status'] = 'PARTIAL_EXACT_LITERAL4'
                    snapshot(file,result)
                require(all(not os.path.lexists(pin['path']) for pin in TARGETS), 'all four exact targets absent')
                for pin in plan['preserved_current7_pins']:
                    current(pin)
                result['status'] = 'RETIRED_EXACT_LITERAL4_COMPLETED_COMPARE_SPOOLS_ONLY'
            else:
                result['status'] = 'READONLY_READY_EXACT_LITERAL4'
            snapshot(file,result)
        except BaseException as error:
            result['status'] = 'FAILED_PARTIAL_EXACT_LITERAL4' if result['actual_released_pins'] else 'FAILED_BEFORE_UNLINK'
            result['failure'] = repr(error)
            snapshot(file,result)
            raise
    print(json.dumps(dict(status=result['status'],receipt_pin=actual_pin(path),
        actual_released_bytes=result['actual_released_bytes'],physics_qualified=False)),flush=True)

if __name__ == '__main__':
    main()
