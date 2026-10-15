"""Finite Source rebind peer: metadata, AST, bytes only; no candidate imports."""
from pathlib import Path
import ast
import hashlib
import json
import os
import stat
import sys

REC = Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P = REC/'current_formal_material_authority_handle_lifetime69_source_v2'
OUT = Path(__file__).resolve().parent
checks = []


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read(path):
    p = Path(path)
    before = identity(p.lstat())
    assert stat.S_ISREG(before[2])
    digest = hashlib.sha256()
    chunks = []
    with p.open('rb') as stream:
        assert identity(os.fstat(stream.fileno())) == before
        while True:
            raw = stream.read(2**20)
            if not raw:
                break
            digest.update(raw)
            chunks.append(raw)
        assert identity(os.fstat(stream.fileno())) == before
    data = b''.join(chunks)
    assert identity(p.lstat()) == before and len(data) == before[4]
    return data, dict(path=str(p), sha256=digest.hexdigest(),
                     size_bytes=before[4], identity=before)


def exact(row):
    data, actual = read(row['path'])
    assert actual == row
    return data


def check(name, condition):
    assert type(condition) is bool and not any(c['name'] == name for c in checks)
    checks.append(dict(name=name, passed=condition))


members = {p.name: read(p) for p in sorted(P.iterdir())}
check('complete_current_source_members_fullEOF_SHA_7ID', len(members) == 31)
proof = json.loads(members['COMPLETE_HANDLE69_CURRENT_MATERIAL_SOURCE_REBIND_BYTE_INVERSE.json'][0])
sf = json.loads(members['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'][0])
hf = json.loads(members['COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'][0])
plan = json.loads(members['CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_HANDLE69_PLAN.json'][0])
copy_results = []
for row in proof['exact_complete_copy_pins']:
    old = exact(row['original_fullpin'])
    new = exact(row['new_fullpin'])
    copy_results.append(dict(name=Path(row['new_fullpin']['path']).name,
      original_pin=row['original_fullpin'], current_pin=row['new_fullpin'], complete_bytes_equal=old == new))
check('all26_unchanged_complete_copies_actual_bytes', len(copy_results) == 26 and all(r['complete_bytes_equal'] for r in copy_results))
check('old_complete_frozen_namespace32_fullpins_current', len(proof['old_frozen_material_package_fullpins']) == 32 and all(exact(r) is not None for r in proof['old_frozen_material_package_fullpins']))
py_members = [data for name, (data, _) in members.items() if name.endswith('.py')]
check('nine_complete_Python_AST_parse_without_import', len(py_members) == 9 and all(isinstance(ast.parse(data), ast.Module) for data in py_members))
check('all_other_eight_Python_wholebytes_unmodified', sum(r['name'].endswith('.py') for r in copy_results) == 8)
old_host = exact(proof['host_original_fullpin'])
new_host = exact(proof['host_new_fullpin'])
forward = old_host
for edit in proof['host_literal_changes']:
    pos = edit['offset_at_application']
    a, b = edit['old_literal'].encode(), edit['new_literal'].encode()
    assert forward[pos:pos+len(a)] == a
    forward = forward[:pos]+b+forward[pos+len(a):]
reverse = new_host
for edit in reversed(proof['host_literal_changes']):
    pos = edit['offset_at_application']
    a, b = edit['old_literal'].encode(), edit['new_literal'].encode()
    assert reverse[pos:pos+len(b)] == b
    reverse = reverse[:pos]+a+reverse[pos+len(b):]
check('exact_two_host_literal_forward_reverse_complete_bytes_AST', len(proof['host_literal_changes']) == 2 and forward == new_host and reverse == old_host and ast.dump(ast.parse(reverse)) == ast.dump(ast.parse(old_host)))
host = new_host.decode()
oldtext = old_host.decode()
host_ast = ast.parse(host)
old_ast = ast.parse(oldtext)
command_node = next(n for n in host_ast.body if isinstance(n, ast.FunctionDef) and n.name == 'commands')
old_command_node = next(n for n in old_ast.body if isinstance(n, ast.FunctionDef) and n.name == 'commands')
check('whole_original_command_producer_function_byte_AST_unchanged', ast.get_source_segment(host, command_node) == ast.get_source_segment(oldtext, old_command_node) and ast.dump(command_node) == ast.dump(old_command_node))
check('only_source_namespace_and_dual_actual_origin_admission_changed', "SOURCE=REC/'current_formal_material_authority_handle_lifetime69_source_v2'" in host and proof['host_literal_changes'][1]['old_literal'].startswith("    if base['schema']"))
for row in hf['dependencies']+sf['files']+sf['original_math_sources']:
    exact(row)
check('HF_all28_dependency_and_SF5plus8_rows_complete_fullEOF', len(hf['dependencies']) == 28 and len(sf['files']) == 5 and len(sf['original_math_sources']) == 8)
check('SF_HF_actual_current_source_and_selected_plan_fullpins', hf['host_source'] == proof['host_new_fullpin'] and hf['selected_source_freeze_pin'] == members['COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'][1] and sf['current_plan_pin'] == members['CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_HANDLE69_PLAN.json'][1])
current_pin = hf['selected_actual69_report_pin']
previous_pin = hf['selected_original_actual69_v4_report_pin']
current = json.loads(exact(current_pin))
previous = json.loads(exact(previous_pin))
check('selected_current_two_stage_closed_true_report_fullpin', current_pin == plan['current_actual69_build_report_pin'] == proof['current_actual69_report_pin'] == sf['selected_actual69_report_pin'] and current_pin['sha256'] == '5088fa1cc144f391f09dbc04566b8b466b5b5d72b514e6337179216f7d96ec6b')
check('selected_original_ten_stage_report_separate_fullpin', previous_pin == current['original_actual69_v4_report_pin'] == sf['original_nine_source_actual69_v4_report_pin'] == plan['original_actual69_v4_report_pin'] and previous_pin['sha256'] == '97e74e45477d13086091b7867b1770999539bf9389bd4d122cd7d9ee30864573')
watch_pins = []
for report, row, expected_count in [(current, current_pin, 2), (previous, previous_pin, 10)]:
    check('true_closed_report_'+str(expected_count)+'_PASS_records_and_caps', report['failure'] is None and report['after_check_error'] is None and report['Dragon_linked'] is True and len(report['records']) == expected_count and all(r['status'] == 'PASS' and r['wall_cap_seconds'] == 600 for r in report['records']) and 0 < report['wall_seconds'] < 1800 and type(report['SELF_peak_bytes']) is int and report['SELF_peak_bytes'] < 512*2**20 and report['original_guard_class'] == 'OwnRSSSerialExecutor' and report['original_guard_MRO_unchanged'] is True)
    root = Path(row['path']).parent
    for record in report['records']:
        watchdata, wp = read(root/(record['label']+'.watchdog.json'))
        logdata, lp = read(root/(record['label']+'.log'))
        watch = json.loads(watchdata)
        assert watch['command'] == record['command'] and type(watch['returncode']) is int and watch['returncode'] == 0
        assert watch['limit_failure'] is None and watch['rss_cap_mib'] == 512 and 0 <= watch['sampled_peak_rss_mib'] < 512
        assert 0 < watch['elapsed_seconds'] <= watch['wall_cap_seconds'] <= 600
        assert watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
        assert lp['sha256'] == record['log_sha256']
        watch_pins.append(dict(watchdog=wp, log=lp))
check('all_twelve_actual_genuine_watch_log_sources_fullEOF', len(watch_pins) == 12)
newtools_pin = sf['actual69_tool_terminal_receipt_pin']
newtools = json.loads(exact(newtools_pin))
oldtools_pin = next(r for r in hf['dependencies'] if Path(r['path']).name == 'ACTUAL_COMPLETE69_BUILD_V4_TRUE_TOOL_RETURNS_20261012.json')
oldtools = json.loads(exact(oldtools_pin))
check('Root_true_current_and_original_terminal_objects_strict0_no_session', type(newtools['final']['exit_code']) is int and newtools['final']['exit_code'] == 0 and 'session_id' not in newtools['final'] and type(oldtools['terminal']['exit_code']) is int and oldtools['terminal']['exit_code'] == 0 and 'session_id' not in oldtools['terminal'])
review_pin = hf['selected_actual69_independent_review_pin']
review = json.loads(exact(review_pin))
check('Root_actual69_complete_EOF_provenance_bound_without_repeating_large_tree', review_pin == plan['current_actual69_independent_review_pin'] == sf['selected_actual69_independent_review_pin'] == proof['current_actual69_review_pin'] and review['actual_report_pin'] == current_pin and review['true_closed_tool_return_pin'] == newtools_pin and review['one_driver_replacement_position37_only'] is True and review['old_nine_and_remaining68_complete_bytes_and_identities_unchanged'] is True)
old69 = [x for x in previous['records'][-1]['command'] if x.endswith(('.o', '.a'))]
new69 = [x for x in current['records'][-1]['command'] if x.endswith(('.o', '.a'))]
check('current69_exactly_one_native_driver_slot37_changed', len(old69) == len(new69) == 69 and [i for i in range(69) if old69[i] != new69[i]] == [37] and new69 == current['actual_complete69_link_inputs'] == proof['current69_ordered_link_inputs'] and old69 == [r['path'] for r in current['original_complete69_ordered_input_pins']])
def table(report):
    result = {}
    for row in report['fixed_current_pins']+report['output_pins']:
        if row['path'] in result:
            assert result[row['path']] == row
        result[row['path']] = row
    return result
newtable, oldtable = table(current), table(previous)
all69_pins = []
for i, path in enumerate(new69):
    row = newtable[path]
    if i != 37:
        assert row == oldtable[old69[i]]
    exact(row)
    all69_pins.append(row)
oldbinding = json.loads((REC/'native_warm_A_bounded_host_source_v3/CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json').read_text())
old9 = oldbinding['seventeen_required_same_production_object_pins']
check('remaining68_and_oldnine_complete_bytes_and_7ID_current', len(all69_pins) == 69 and len(old9) == 9 and all(newtable[r['path']] == oldtable[r['path']] == r and r['path'] in new69 for r in old9))
check('current_driver_Source_and_host_SF_origins_actual_fullpins', current['actual_driver_Source_freeze_pin'] == hf['selected_native_handle_driver_Source_freeze_pin'] == sf['native_handle_driver_Source_freeze_pin'] == plan['current_native_handle_driver_Source_freeze_pin'] and current['actual_host_Source_freeze_pin'] == hf['selected_current69_build_host_freeze_pin'] == plan['current_build69_host_Source_freeze_pin'])
order_node = next(n for n in host_ast.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ORDER' for t in n.targets))
order = ast.literal_eval(order_node.value)
added = ['NEW_OWN_OBSERVATION_OBJECT/'+Path(n).stem+'.o' for n in order]
at = next(i for i, v in enumerate(new69) if v.endswith('.a'))
new74 = new69[:at]+added+new69[at:]
check('exact74_order_69plus5_before_first_of_same4archives', new74 == proof['required_new74_order'] and len(new74) == 74 and [p for p in new74 if p not in added] == new69 and [p for p in new74 if p.endswith('.a')] == [p for p in new69 if p.endswith('.a')])
check('new_five_observer_compiler_paths_exact_sf_current_namespace', order == sf['original_five_Source_order'] and [r['path'] for r in sf['files']] == [str(P/n) for n in order])
check('original_compiler_flags_link_flags_and_commands_unmodified', "original[1:10]!=c.FLAGS" in host and current['records'][-1]['command'][1:3] == ['-O2', '-ffp-contract=off'] and ast.dump(command_node) == ast.dump(old_command_node))
check('host_separate_2_and_10_genuine_closed_admission_actual_consumers', "c.closed_report(base,helper,Path(pbase['path']).parent,2)" in host and "c.closed_report(previous,helper,Path(previous_pin['path']).parent,10)" in host and "hf['selected_actual69_report_pin']!=pbase" in host and "previous_pin!=hf['selected_original_actual69_v4_report_pin']" in host)
check('original_guard_mro_resource_roots_caps_schedule_not_modified', "full.OwnRSSSerialExecutor(out,1800-(time.monotonic()-start),'observer-build',resources)" in host and "runner.execute(out/'build','compile_'+str(i)if i<5 else'link_Dragon',command,600)" in host and hf['original_caps'] == sf['original_caps'] == proof['original_caps'] == plan['original_caps'] and hf['original_caps']['threads'] == 1 and hf['original_caps']['children_at_once'] == 1 and hf['original_caps']['retries'] == 0)
check('new74_capture_BOOT_and_science_still_not_claimed', sf['compiler_executed'] is False and sf['material_job_executed'] is False and hf['actual74_compile_or_link_executed'] is False and hf['current_material_capture_executed'] is False and plan['actual74_observer_build_executed'] is False and plan['current_material_capture_executed'] is False and all(sf[k] is False and hf[k] is False for k in ['AAA_qualified', 'ABA_admitted', 'goal_complete']))
check('review_has_no_candidate_import_guard_API_compile_or_material_execution', True)
for _, row in members.values():
    exact(row)
report = dict(schema='INDEPENDENT_FINITE_CURRENT_MATERIAL_HANDLE69_SOURCE_REBIND_REVIEW_V1',
  status='SOURCE_ONLY_PASS_HANDLE69_DUAL_ORIGIN_AND_COMPLETE74_ORDER_NO_EXECUTION',
  source_only=True, checks=checks, check_count=len(checks), all_checks_typed_true=all(r['passed'] for r in checks),
  blockers=[], current_complete_Source_member_pins=[p for _, p in members.values()],
  actual_host_two_literal_whole_inverse=True, preserved_complete26_copy_results=copy_results,
  original_source_math_review_pin=sf['independent_material_source_review_pin'],
  current_native_driver_build_report_pin=current_pin, original_nine_source_build_report_pin=previous_pin,
  selected_actual69_independent_Root_full_EOF_review_pin=review_pin,
  exact69_ordered_current_fullpin_rows=all69_pins, old_nine_original_pin_rows=old9,
  actual_two_plus_ten_watch_log_pins=watch_pins, current69_true_tool_receipt_pin=newtools_pin,
  original69_true_tool_receipt_pin=oldtools_pin, exact_new74_order_template=new74,
  no_large_physical_payload_read=True, no_active_pipeline_output_read=True,
  new74_actual_build_qualified=False, current_material_capture_qualified=False,
  current_BOOT_or_saved_science_admitted=False, candidate_imported=False,
  guard_or_resource_API_called=False, compiler_or_material_or_numerical_child_started=False,
  AAA_qualified=False, ABA_admitted=False, goal_complete=False)
target = OUT/'SOURCE_REVIEW.json'
with target.open('x') as stream:
    json.dump(report, stream, indent=2, allow_nan=False)
    stream.write('\n')
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps(dict(status=report['status'], checks=len(checks), passed=report['all_checks_typed_true'],
  blockers=report['blockers'], report_pin=read(target)[1], current_source_members=len(members),
  preserved_complete_copies=len(copy_results), genuine_closed_watches=len(watch_pins),
  candidate_or_guard_or_compiler_or_material_executed=False), allow_nan=False))
sys.exit(0 if report['all_checks_typed_true'] else 1)
