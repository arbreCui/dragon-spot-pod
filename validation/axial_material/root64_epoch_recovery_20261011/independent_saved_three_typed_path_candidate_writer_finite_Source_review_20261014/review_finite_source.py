"""Independent finite Source review; reads code/small metadata and data current7 only."""
import ast
import base64
import hashlib
import json
import os
from pathlib import Path
import stat

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE = REC / 'saved_three_macro_exact_typed_path_join_source_v1_20261014'
OUT = Path(__file__).parent
ROLES = ('host_source_pin', 'child_source_pin', 'original_admission_Source_pin',
         'original_adapter_Source_pin', 'plan_pin', 'inverse_pin',
         'Source_author_pin', 'writer_source_pin')
FLAGS = dict(business_executed=False, compiler_executed=False,
             numerical_executed=False, files_deleted=False)


def require(value, detail):
    if value is not True:
        raise AssertionError(detail)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def current7(p):
    q = Path(p['path'])
    s = q.lstat()
    require(q.is_absolute() and stat.S_ISREG(s.st_mode) and s.st_nlink == 1
            and identity(s) == p['identity'] and s.st_size == p['size_bytes']
            and not any(x.is_symlink() for x in (q, *q.parents)),
            'ordinary exact current7: ' + str(q))
    require(all(type(v) is int for v in p['identity']), 'all seven fields exact Python int')


def fullpin(path, expected=None):
    q = Path(path).absolute()
    s = q.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_nlink == 1 and s.st_size < 64*2**20
            and not any(x.is_symlink() for x in (q, *q.parents)), 'bounded ordinary Source/metadata')
    raw = q.read_bytes()
    require(identity(q.lstat()) == identity(s), 'full EOF before/after current7')
    p = dict(path=str(q), sha256=hashlib.sha256(raw).hexdigest(),
             size_bytes=len(raw), identity=identity(s))
    if expected is not None:
        require(p == expected, 'exact four-field full PF: ' + str(q))
    return p, raw


def read(p):
    _, raw = fullpin(p['path'], p)
    return json.loads(raw)


def node(source, name):
    return next(n for n in ast.parse(source).body
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name)


def segment(source, name):
    return ast.get_source_segment(source, node(source, name))


def contains(value, p):
    return (value == p or isinstance(value, dict) and any(contains(v, p) for v in value.values())
            or isinstance(value, list) and any(contains(v, p) for v in value))


def literals(source):
    return {n.targets[0].id: ast.literal_eval(n.value) for n in ast.parse(source).body
            if isinstance(n, ast.Assign) and len(n.targets) == 1
            and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Constant)}


def main():
    rp, raw = fullpin(BASE/'SOURCE_REVIEW_READY.json')
    ready = json.loads(raw)
    require(ready['source_only'] is True and all(ready[k] is False for k in FLAGS), 'READY Source only')
    selected = [ready[k] for k in ROLES] + [rp]
    raw_by_role = {}
    for role in ROLES:
        _, content = fullpin(ready[role]['path'], ready[role])
        raw_by_role[role] = content
    plan = json.loads(raw_by_role['plan_pin'])
    inverse = json.loads(raw_by_role['inverse_pin'])
    sources = {k: v.decode() for k, v in raw_by_role.items() if k.endswith('source_pin')
               or k in ('original_admission_Source_pin', 'original_adapter_Source_pin', 'Source_author_pin')}
    for source in sources.values():
        ast.parse(source)
    host, child, writer = (sources[k] for k in ('host_source_pin', 'child_source_pin', 'writer_source_pin'))
    admission, adapter = (sources[k] for k in ('original_admission_Source_pin', 'original_adapter_Source_pin'))
    author = sources['Source_author_pin']
    require(plan['source_only'] is True and plan['physics_qualified'] is False
            and plan['actual_comparison_report_pin'] is None
            and plan['original_archive_decode_repeated'] is False
            and plan['original_report_or_physical_record_order_rewritten'] is False, 'Source-only plan scope')
    # Verify the actual author literal output, without importing or executing it.
    template = literals(author)
    require(template['CHILD'].encode() == raw_by_role['child_source_pin'], 'author complete child bytes')
    original_guard = REC/'bq64_private_GANLIB_model_control_host_source_v5_20261013/run_guarded_model_controls.py'
    guard_pin, guard_raw = fullpin(original_guard)
    guard = guard_raw.decode()
    borrowed = []
    for row in inverse['original_guard_methods_whole_bytes']:
        name = row['name']
        exact = segment(guard, name)
        require(row['whole_bytes'] == exact == segment(host, name), 'whole unchanged original guard method: '+name)
        require(ast.dump(node(guard, name), include_attributes=False)
                == ast.dump(node(host, name), include_attributes=False), 'whole original guard AST '+name)
        borrowed.append(dict(name=name, original_source_line=node(guard, name).lineno,
                             exact_whole_bytes_sha256=hashlib.sha256(exact.encode()).hexdigest()))
    require([r['name'] for r in borrowed] == ['rewrite_summary','unique','safe_repr','FirstFailure'], 'all original four methods')
    expected_host = template['HOST'].replace('def main():\n',
        '\n\n'.join(r['whole_bytes'] for r in inverse['original_guard_methods_whole_bytes'])+'\n\ndef main():\n', 1)
    require(expected_host.encode() == raw_by_role['host_source_pin'], 'author complete host bytes')
    writer_blobs = [n for n in ast.walk(ast.parse(author)) if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute) and n.func.attr == 'b64decode']
    require(len(writer_blobs) == 1 and base64.b64decode(ast.literal_eval(writer_blobs[0].args[0]))
            == raw_by_role['writer_source_pin'], 'author complete oncewriter bytes')
    copied = []
    for row in inverse['unchanged_admission_and_adapter_Source_copies']:
        original, original_raw = fullpin(row['original_Source_pin']['path'], row['original_Source_pin'])
        candidate, candidate_raw = fullpin(row['candidate_Source_pin']['path'], row['candidate_Source_pin'])
        require(original_raw == candidate_raw and row['whole_bytes_unchanged'] is True, 'complete unmodified Source copy')
        copied.append(dict(original_Source_pin=original, candidate_Source_pin=candidate,
                           exact_whole_bytes_equal=True))
    require(len(copied) == 2, 'both original admission and adapter whole copies')
    require(inverse['original_wrong_compare_function_whole_bytes']
            == segment(admission, 'compare_raw_macro'), 'original positional comparison preserved in inverse')
    require(inverse['new_child_Source_pin'] == ready['child_source_pin']
            and inverse['new_host_Source_pin'] == ready['host_source_pin'], 'inverse binds exact selected host and child')
    # Read code only. Data/archive/old ordinal-detail bodies are never opened.
    current = plan['source_dependency_pins']
    require(len(current) == 32, 'complete 32 current dependency PFs')
    for p in current:
        current7(p)
    data = plan['data_pair_pins']
    require(len(data) == 8, 'original observation and three saved SQLite/pool pairs')
    for p in data + [plan['retained_A1_physical_pin']] + plan['original_ordinal_detail_pins']:
        current7(p)
    require(len(plan['original_ordinal_detail_pins']) == 3, 'all original wrong-ordinal details retained')
    for producer, pair in zip(plan['original_native_producers'], plan['native_pairs']):
        require(producer['plane'] == pair['plane'] and producer['archive_pin'] == pair['archive_pin'], 'original producer/archive seal')
        current7(producer['archive_pin'])
        current7(producer['actual_report_pin'])
    current7(plan['observed_pair']['input_pin'])
    require([r['plane'] for r in plan['native_pairs']] == [1,2,3], 'three original planes')
    require("b=native.row(right_path)" in child and "right_path=['MICROLIB2',1]+a['path']" in child
            and "key=adapter.path_key(canonical)" in child and "original[2:]" in child
            and "native_keys==observed_keys" in child and "19620" in child
            and "count==len(observed_keys)==len(native_keys)" in child,
            'full typed-path bidirectional 19620 join, original typed root included')
    require("a['path_types']==b['path_types'][2:]" in child
            and "('kind','declared_count','original_word_count')" in child
            and 'itertools.zip_longest(saved.iter_raw(a),native.iter_raw(b)' in child
            and "'native_payload_sha256'" in segment(adapter, 'SavedNativeInput'),
            'all kind/count/words, all raw words and each complete original record SHA')
    require('digest.hexdigest() == row[\'native_payload_sha256\']' in adapter
            and 'ORDER BY ordinal' in adapter
            and all(x in child for x in ('original_observation_ordinal', 'original_observation_api_key',
                'original_archive_ordinal', 'original_archive_api_key'))
            and 'sorted(' not in child and 'tree.walk' not in child and '.xsm' not in child,
            'each record SHA checked at exhausted stream; saved original physical/API order retained; no archive decode')
    require("strict_json(result[0])" in segment(adapter,'SavedNativeInput')
            and "row['path'] == list(path)" in adapter and "row['path_types'] ==" in adapter,
            'actual SavedNativeInput.row validates typed full path and record shape')
    for term in ('full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)',
        "type(runner)is full.OwnRSSSerialExecutor", "runner.resources is resources",
        '20971764748', '64*2**20', '96*2**30', '8*2**30', '2*2**30',
        'peak<512*2**20', 'time.monotonic()-start<1800', "],600)",
        "error=='own-child stage failed; no retry'and len(runner.records)==1"):
        require(term in host, 'original guarded host bound: '+term)
    require('admit_owning_stage(' in child and "producer['actual_report_pin']" in child,
            'original producer admission function directly used')
    release = read(plan['actual_duplicate_physical_release_proof_pin'])
    root = read(plan['actual_duplicate_physical_release_Root_tool_pin'])
    post = read(plan['actual_release_independent_post_pin'])
    posttools = read(plan['actual_release_independent_post_tools_pin'])
    terminal = root['actual_terminal_return']
    require(type(terminal['exit_code']) is int and terminal['exit_code'] == 0
            and terminal.get('session_id') is None and root['observed_closed'] is True
            and type(root['original_integer_exit_code']) is int and root['original_integer_exit_code'] == 0,
            'actual original closed Root0 release return')
    require(json.loads(terminal['output'])['receipt_pin'] == plan['actual_duplicate_physical_release_proof_pin']
            and post['actual_Root_release_true_tool_pin'] == plan['actual_duplicate_physical_release_Root_tool_pin']
            and post['actual_release_receipt_pin'] == plan['actual_duplicate_physical_release_proof_pin'],
            'release actual terminal output and independent post bind same exact PFs')
    require(post['status'].startswith('PASS') and post['failure'] is None
            and posttools['observed_closed'] is True and type(posttools['original_integer_exit_code']) is int
            and posttools['original_integer_exit_code'] == 0
            and json.loads(posttools['actual_review_return']['output'])['review_pin']
                == plan['actual_release_independent_post_pin'], 'actual independent release post closed0 PF')
    historical = plan['historical_A2_A3_physical_pins']
    require(historical == post['exact_released_historical_target_pins'] == release['exact_target_pins']
            and len(historical) == 2 and all(contains(release,p) and not os.path.lexists(p['path']) for p in historical)
            and release['retained_complete_owner_pin'] == plan['retained_A1_physical_pin'],
            'only historical exact A2/A3 physical duplicates absent and original A1 retained')
    require(release['actual_released_bytes'] == plan['retired_physical_duplicate_byte_total'] == 68743634
            and release['original_Root_exit_code_retained'] == post['original_compare_Root_exit_code_retained'] == 1
            and release['original_resource_failure_retained'] is True
            and post['original_compare_resource_failure_retained'] is True
            and post['original_positional_mismatch_reports_not_rewritten'] is True
            and post['original_all_SQLite_pools_comparison_reports_logs_and_archives_retained'] is True,
            'original Root1 budget failure, false positional difference and saved outputs remain historical facts')
    roots = plan['complete_joint_roots']
    old25 = post['actual_original_joint25_resource_snapshot_after_release']['resource_roots']
    require(len(roots) == len(set(roots)) == 30 and roots[:25] == old25
            and roots[25:27] == [plan['planned_actual_output_root'], str(BASE)]
            and roots[27:] == post['required_following_cumulative_release_evidence_roots']
            and not any(Path(a).is_relative_to(Path(b)) for a in roots for b in roots if a != b),
            'complete old25 plus new output/Source2 plus release package/review/post3, disjoint30')
    metadata = plan['explicit_cumulative_metadata_file_pins']
    require(len(metadata) == 4 and metadata == post['actual_external_metadata_file_pins'], 'original extra metadata4 exactly retained')
    for p in metadata:
        current7(p)
    recipe = read(plan['original_recipe_pin'])
    expected_env = ['/usr/bin/env','-u','PYTHONOPTIMIZE','PYTHONDONTWRITEBYTECODE=1',
        'OMP_NUM_THREADS=1','OPENBLAS_NUM_THREADS=1','MKL_NUM_THREADS=1',
        'VECLIB_MAXIMUM_THREADS=1','NUMEXPR_NUM_THREADS=1',
        '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B']
    require(recipe['argv'][:11] == expected_env, 'current original env11/current recipe wholePF')
    require("old['argv'][:11]+[ready['host_source_pin']['path']]" in writer
            and "len(argv)==24" in writer and "for role,p in(('source-freeze',sp),('host-freeze',hp))" in writer
            and "json.dumps(p['identity'],separators=(',',':'))" in writer,
            'writer exact current env11 + selected host + two actual fullPF triples CLI24')
    require("same round nine exact selected Source fullPF" in writer and 'all(has(peer,p)for p in selected)' in writer
            and "'writer_source_pin')]+[rp]" in writer and "tool['actual_review_return']" in writer
            and "z['exit_code']" in writer and "z.get('session_id')is None" in writer
            and "['review_pin']==proof['peer-review']" in writer,
            'same-round review recursively includes all nine exactPFs; genuine closed integer0 binds review stdout PF')
    require("with p.open('xb')" in writer and 'os.fsync(' in writer
            and "code=[ready[k]for k in('host_source_pin','child_source_pin','original_admission_Source_pin','original_adapter_Source_pin')]" in writer
            and "dependencies=deps+[sp]" in writer,
            'oncewriter exclusive publication, Source freeze exact four code PFs and Host complete current dependency PFs')
    for source in (host, child, writer, author):
        tree = ast.parse(source)
        require(not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in ('unlink','remove','rmtree','system','Popen','run','exec','eval')
                for n in ast.walk(tree)), 'no deletion/new scientific/compiler subprocess in candidate Source')
    for p in selected + current + data + plan['original_ordinal_detail_pins']:
        current7(p)
    review = dict(schema='INDEPENDENT_SAVED_THREE_TYPED_PATH_CANDIDATE_WRITER_FINITE_SOURCE_REVIEW_V1',
        status='PASS_SAVED_THREE_TYPED_PATH_CANDIDATE_AND_ONCEWRITER_FINITE_SOURCE_REVIEW',
        source_only=True, failure=None, **FLAGS,
        exact_same_round_nine_selected_Source_full_pins=selected,
        original_guard_Source_full_pin=guard_pin,
        original_four_guard_methods_whole_bytes_and_AST_equal=borrowed,
        original_admission_and_adapter_complete_bytes_equal=copied,
        original_32_dependency_current7_pins=current,
        original_saved_SQLite_pool_current7_pins=data,
        original_wrong_ordinal_detail_current7_pins=plan['original_ordinal_detail_pins'],
        retained_A1_physical_current7_pin=plan['retained_A1_physical_pin'],
        historical_exact_absent_A2_A3_physical_pins=historical,
        actual_release_receipt_full_pin=plan['actual_duplicate_physical_release_proof_pin'],
        actual_Root_release_true_tool_full_pin=plan['actual_duplicate_physical_release_Root_tool_pin'],
        actual_release_independent_post_full_pin=plan['actual_release_independent_post_pin'],
        actual_release_independent_post_tools_full_pin=plan['actual_release_independent_post_tools_pin'],
        original_current_recipe_full_pin=plan['original_recipe_pin'],
        complete_joint_disjoint_30_roots=roots, original_external_metadata4_full_pins=metadata,
        child_join_contract=dict(exact_typed_full_path=True, bidirectional_complete_keysets=True,
            expected_complete_macro_record_count=19620, typed_MACROLIB_root_included=True,
            kind_declared_count_original_words_checked=True, all_raw_words_compared=True,
            both_complete_record_SHA_verified_by_exhausted_iter_raw=True,
            both_original_physical_and_API_ordinals_preserved=True,
            original_record_orders_not_rewritten=True, original_archives_not_redecoded=True),
        original_guard_contract=dict(genuine_OwnRSS_MRO=True, single_thread=1, rss_mib=512,
            child_seconds=600, whole_seconds=1800, retries=0, history_bytes=96*2**30,
            free_floor_bytes=8*2**30, cold_reserve_bytes=20971764748,
            metadata_reserve_bytes=64*2**20, joint_archive_bytes=2*2**30),
        oncewriter_contract=dict(exact_same_round_nine_source_PFs=True,
            recursively_embedded_for_actual_has_check=True, genuine_closed_integer0_required=True,
            review_stdout_exact_PF_binding=True, Source_freeze_code_count=4,
            Host_dependencies_exact_current_fullPF=True, current_original_environment_11=expected_env,
            future_actual_CLI_argc=24, future_SF_HF_pin_triples_must_be_actual=True,
            exclusive_three_metadata_outputs=True),
        original_failed_Root_integer_exit_code_retained=1,
        original_budget_failure_and_positional_9_5M_false_difference_history_preserved=True,
        original_scientific_archive_SQLite_pool_and_ordinal_detail_bytes_not_read=True,
        no_candidate_modules_imported_or_business_run=True, actual_comparison_report_pin=None,
        physics_qualified=False, scientific_accuracy_qualified=False, goal_complete=False,
        reviewer_Source_full_pin=fullpin(__file__)[0])
    target = OUT/'REVIEW.json'
    with target.open('xb') as f:
        f.write((json.dumps(review, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode())
        f.flush()
        os.fsync(f.fileno())
    reviewpin, _ = fullpin(target)
    print(json.dumps(dict(status=review['status'], review_pin=reviewpin, **FLAGS)), flush=True)


if __name__ == '__main__':
    main()
