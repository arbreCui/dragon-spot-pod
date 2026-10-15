"""Read only bounded existing metadata/source; no business import or execution."""
import ast
import collections
import hashlib
import json
import math
import statistics
from pathlib import Path

A = Path('/Users/wen/spot/validation/artifacts')
C = Path('/Users/wen/spot/validation/axial_material')
D = Path('/private/tmp/axmat_component_driver_timing_readonly_review_20261010')
sources = {
    'V10': (C/'prepare_qualified_AB_rank1_factor_cache_factor_diagonal_trim_production.py',
        'd82d89daa779c8e1f3087e5c49f05279d35a9b3320ea1ae0257f7eaa586ebc8e'),
    'V11': (C/'prepare_qualified_AB_rank1_factor_cache_cross_group_identity_key_delta_production.py',
        'f136baab5047a8727cfd2c0abb5399acf617c25c4f4e7692242419e6f9daef4e'),
    'V13': (C/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py',
        'd2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633')}

def descriptor(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}, raw

def document(path):
    pin, raw = descriptor(path)
    return pin, json.loads(raw)

def literal_constants(tree):
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('FAMILY', 'TOTAL_WALL', 'STAGE_WALL', 'RSS_CAP'):
                    values[target.id] = ast.literal_eval(node.value)
    return values

def category(label):
    if label.startswith('build/'): return 'build'
    if label.startswith('audit/'): return 'audit'
    if label.startswith('sender_controls/'): return 'sender'
    if label.startswith('controls/keycodec'): return 'keycodec'
    return 'original_other_controls'

versions = []
for name, (source, expected_sha) in sources.items():
    source_pin, raw = descriptor(source)
    assert source_pin['sha256'] == expected_sha
    text = raw.decode('utf-8'); tree = ast.parse(text); constants = literal_constants(tree)
    top = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    out_assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == 'OUT' for target in node.targets))
    assert isinstance(out_assignment.value, ast.BinOp)
    root = A / ast.literal_eval(out_assignment.value.right)
    family = constants['FAMILY']
    result_pin, result = document(root/'driver_result.json')
    claim_pin, claim = document(root/'execution_claim.json')
    journal_pin, journal = document(root/family/'stages.json')
    decl_pin, declaration = document(root/'declaration.json')
    assert claim['declaration_sha256'] == decl_pin['sha256']
    assert (declaration['total_wall_seconds'], declaration['stage_wall_seconds'], declaration['rss_cap_mib'],
        declaration['threads'], declaration['numeric_children_at_once'], declaration['retries']) == (1800, 600, 512, 1, 1, 0)
    stages = journal['stages']; rows = []; groups = {}; watches = []
    for stage in stages:
        watch_pin, watch = document(root/(stage['label']+'.watchdog.json'))
        assert watch['command'] == stage['command']
        assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['rss_cap_mib'] == 512
        group = groups.setdefault(category(stage['label']), {'count': 0, 'stage_elapsed_sum': 0.0, 'watch_elapsed_sum': 0.0})
        group['count'] += 1; group['stage_elapsed_sum'] += stage['elapsed_seconds']; group['watch_elapsed_sum'] += watch['elapsed_seconds']
        watches.append(watch_pin)
        rows.append({'label': stage['label'], 'status': stage['status'], 'stage_elapsed_seconds': stage['elapsed_seconds'],
            'started_unix': stage['started_unix'], 'stage_wall_cap_seconds': stage['wall_cap_seconds'],
            'watch_elapsed_seconds': watch['elapsed_seconds'], 'watch_wall_cap_seconds': watch['wall_cap_seconds'],
            'returncode': watch['returncode'], 'limit_failure': watch['limit_failure'],
            'sampled_peak_rss_mib': watch['sampled_peak_rss_mib']})
    gaps = [{'before_label': right['label'], 'seconds': right['started_unix']-left['started_unix']-left['elapsed_seconds']}
        for left, right in zip(stages, stages[1:])]
    stage_sum = math.fsum(stage['elapsed_seconds'] for stage in stages)
    watch_sum = math.fsum(row['watch_elapsed_seconds'] for row in rows)
    negative_expected = []
    unexpected = []
    for row in rows:
        expected_rc = 23 if row['label'].startswith('controls/keycodec_negative_') else 1 if row['label'].startswith('sender_controls/unsupported_') else 0
        valid = row['returncode'] == expected_rc and row['limit_failure'] is None and row['status'] == ('FAILED' if expected_rc else 'PASS')
        if valid and expected_rc: negative_expected.append(row['label'])
        elif not valid: unexpected.append(row)
    output = {
        'version': name, 'root': str(root), 'source': source_pin, 'source_constants': constants,
        'driver_result': result_pin, 'execution_claim': claim_pin, 'stage_journal': journal_pin, 'declaration': decl_pin,
        'driver_classification': result['classification'], 'driver_error': result['error'],
        'driver_elapsed_seconds': result['elapsed_seconds'], 'stage_count': len(stages),
        'stage_elapsed_seconds_sum': stage_sum, 'own_watch_process_interval_seconds_sum': watch_sum,
        'driver_minus_stage_sum_seconds': result['elapsed_seconds']-stage_sum,
        'driver_minus_own_watch_sum_seconds': result['elapsed_seconds']-watch_sum,
        'stage_minus_own_watch_sum_seconds': stage_sum-watch_sum,
        'claim_to_first_stage_unix_seconds': stages[0]['started_unix']-claim['started_unix'],
        'inter_stage_gap_estimate_seconds_sum': math.fsum(gap['seconds'] for gap in gaps),
        'inter_stage_gap_estimate_min_median_max_seconds': [min(gap['seconds'] for gap in gaps), statistics.median(gap['seconds'] for gap in gaps), max(gap['seconds'] for gap in gaps)],
        'inter_stage_gap_estimate_count': len(gaps), 'largest_inter_stage_gaps': sorted(gaps, key=lambda gap: gap['seconds'], reverse=True)[:5],
        'category_sums': groups, 'stage_status_counts': dict(collections.Counter(row['status'] for row in rows)),
        'valid_completed_stage_count': len(rows)-len(unexpected), 'expected_rejection_stage_count': len(negative_expected),
        'unexpected_or_resource_failed_stages': unexpected, 'last_audit': rows[-1],
        'declared_file_pin_count': len(declaration['files']),
        'preserved_predecessor_inventory_count': len(declaration['preserved_predecessors']),
        'preserved_predecessor_inventory_file_count': sum(len(entry['inventory']['files']) for entry in declaration['preserved_predecessors']),
        'old_cache_counts': result.get('control_counts'), 'qualification_flags': {key: result.get(key) for key in
            ('actual_full_FLU_entry_executed', 'transport_launched', 'AAA_accuracy_qualified', 'ABA_admitted')},
        'watchdog_files': watches, 'all_stage_times': rows,
        'run_build_source_lines': [top['run_build'].lineno, top['run_build'].end_lineno],
        'declaration_admission_source_lines': [top['declaration_admission'].lineno, top['declaration_admission'].end_lineno],
        'environment_source_lines': [top['environment'].lineno, top['environment'].end_lineno]}
    versions.append(output)

comparison = {'V11_minus_V10': {}, 'V13_minus_V11': {}}
for label, new, old in [('V11_minus_V10', versions[1], versions[0]), ('V13_minus_V11', versions[2], versions[1])]:
    for key in ('driver_elapsed_seconds', 'stage_elapsed_seconds_sum', 'own_watch_process_interval_seconds_sum',
        'driver_minus_stage_sum_seconds', 'driver_minus_own_watch_sum_seconds', 'inter_stage_gap_estimate_seconds_sum'):
        comparison[label][key] = new[key]-old[key]

support = []
for path, names in [
    (C/'prepare_qualified_AB_source_factor_production.py', ['digest','require','verify','verify_inventory','environment','modules']),
    (C/'qualify_refined_AAA_layered_full.py', []),
    (A/'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005/runtime/production_runner.py', [])]:
    pin, raw = descriptor(path); text = raw.decode(); tree = ast.parse(text)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    ranges = {name: [functions[name].lineno, functions[name].end_lineno] for name in names}
    if not names:
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name in ('OwnRSSSerialExecutor','SerialExecutor'))
        ranges = {cls.name:[cls.lineno,cls.end_lineno]}
    support.append({'source': pin, 'source_ranges': ranges})

report = {'schema': 'AXMAT_COMPONENT_DRIVER_TIMING_READONLY_COMPARISON_V1',
    'status': 'PASS_READONLY_METADATA_COMPARISON_ONLY', 'versions': versions, 'comparison': comparison,
    'source_support': support,
    'interpretation': [
        'driver_result.elapsed_seconds includes pre-first-stage declaration admission, parent/source checks, environment gates, raw receipt creation and pre-closeout checks; it excludes successful post-seal tail.',
        'stage.elapsed_seconds covers executor journal entry, resource_before, supervised process interval, resource_after and log checks; the final stages journal write follows the elapsed assignment and is outside this duration.',
        'OwnRSS watchdog elapsed_seconds is the _process interval including own child wall/RSS supervision, resource checks and group watchdog cleanup; it is not isolated solver compute time.',
        'Driver minus stage/watch sums is observed unallocated time, not a direct measurement of a specific metadata or static-parent function.',
        'Inter-stage gaps mix Unix journal starts with recorded monotonic duration; they estimate journal finalization plus outer parent/environment work and other boundary work, assuming no intervening clock adjustment.',
        'All three component environment gates delegate to source-factor environment(), which freshly hashes declaration.files and freshly inventories every preserved predecessor on each call.',
        'V13 first85 stages completed with61PASS and24 valid declared expected rejections. Final86 audit was resource-killed and no complete86 audit/admission or native/scientific qualification is granted.',
        'The V13 truncated audit prevents attributing its nearly equal own-watch sum versus V11 to equal complete work; V10/V11 successful audit intervals were each about105.8 seconds.' ],
    'business_imports': False, 'business_API_calls': False, 'candidate_execution': False, 'compile': False,
    'fixtures': False, 'live_poll': False, 'numeric_raw_read': False, 'large_history_tree_scan': False,
    'large_input_hash': False, 'project_write': False, 'native_RSS_credit': False, 'AAA_credit': False, 'ABA_credit': False}
with (D/'REPORT.json').open('x') as stream:
    json.dump(report, stream, indent=2, ensure_ascii=False, allow_nan=False); stream.write('\n')
summary = {key:value for key,value in report.items() if key not in ('versions','source_support')}
summary['versions'] = [{key:value for key,value in version.items() if key not in ('watchdog_files','all_stage_times','old_cache_counts')} for version in versions]
summary['report'] = descriptor(D/'REPORT.json')[0]
print(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False))
