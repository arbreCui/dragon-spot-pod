"""Bounded actual temperature postverification; old science bodies stay unopened."""
import ast
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import struct
import time

HERE = Path(__file__).absolute().parent
BASE = HERE.parent
PIN_KEYS = {'path', 'sha256', 'size_bytes', 'identity'}
START = time.monotonic()
NEW_OUTPUTS = {'/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/ACTUAL_TEMPERATURE_OPERAND_CAPTURE.json': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/ACTUAL_TEMPERATURE_OPERAND_CAPTURE.json', 'sha256': '9a1dc69ff682782b8d1f8b74f109744cf95d4b33555d1eba5abdcd78caff4b4d', 'size_bytes': 43967, 'identity': [16777229, 50492895, 33188, 1, 43967, 1792007781878939516, 1792007781878939516]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/original_four_temperature_operand_records_1984B.bin': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/original_four_temperature_operand_records_1984B.bin', 'sha256': '489407f046ecb452dedcfcbde689d3148079b9d8d912efea36e817c4a1123e4f', 'size_bytes': 1984, 'identity': [16777229, 50492894, 33188, 1, 1984, 1792007781878088430, 1792007781878088430]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/temperature_operand.log': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/temperature_operand.log', 'sha256': '47e506199cefebd0456cd62f14866e3e203f8c4efe5257a475bd252cc4f26871', 'size_bytes': 1231, 'identity': [16777229, 50492892, 33188, 1, 1231, 1792007781879177017, 1792007781879177017]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/temperature_operand.watchdog.json': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/capture/temperature_operand.watchdog.json', 'sha256': 'b9d103491cfc92b8e199ee929be96b8bdcbb0aba2bdb63c6bb085fa75c61c5ab', 'size_bytes': 1090, 'identity': [16777229, 50492897, 33188, 1, 1090, 1792007783173649741, 1792007783173649741]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/runtime/run_bounded_dragon.py': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/runtime/run_bounded_dragon.py', 'sha256': 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09', 'size_bytes': 6019, 'identity': [16777229, 50492890, 33261, 1, 6019, 1787952565114585932, 1792007780371484856]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/temperature/stages.json': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/temperature/stages.json', 'sha256': '666aa146592fc402b126ca4591ce57450dd98515a346c3857e66119f325c2e58', 'size_bytes': 424262, 'identity': [16777229, 50492898, 33188, 1, 424262, 1792007783868694777, 1792007783868854444]}, '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/Root_actual_temperature_operand_capture_summary.json': {'path': '/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011/current_A1_native_vector_capture_and_literal2_retirement_source_v1_20261015/current_temperature_operand_capture_source_v1/v5/actual_temperature_operand_capture/Root_actual_temperature_operand_capture_summary.json', 'sha256': '29a034cf32b53641416370158c99349f27b9bc83bdc59f853ec9092945222e47', 'size_bytes': 872424, 'identity': [16777229, 50492899, 33188, 1, 872424, 1792007785961685913, 1792007785961685913]}}
GUARD_LOGS = {'/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard/positive.log': {'path': '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard/positive.log', 'sha256': 'ec0afc5e197cabac3c13a56fc633dbb9c0cf59de42241ef0bc24b588aa29f822', 'size_bytes': 19, 'identity': [16777229, 48427938, 33188, 1, 19, 1791178807981512279, 1791178948678021872]}, '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard/memorycap.log': {'path': '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-refined-layered-full-20261005/preflight/live_guard/memorycap.log', 'sha256': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'size_bytes': 0, 'identity': [16777229, 48427941, 33188, 1, 0, 1791178808389861012, 1791178948678412623]}}


def require(ok, message):
    if ok is not True:
        raise ValueError(message)


def budget():
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak *= 1 if sys.platform == 'darwin' else 1024
    require(peak < 512 * 2**20 and time.monotonic() - START < 600,
            'bounded Source auditor SELF512/stage600')


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def typed(p):
    require(type(p) is dict and set(p) == PIN_KEYS, 'exact full PF schema')
    require(type(p['path']) is str and Path(p['path']).is_absolute(), 'absolute PF')
    require(type(p['sha256']) is str and len(p['sha256']) == 64 and
            all(x in '0123456789abcdef' for x in p['sha256']), 'SHA256 PF')
    require(type(p['size_bytes']) is int and p['size_bytes'] >= 0, 'integer bytes')
    require(type(p['identity']) is list and len(p['identity']) == 7 and
            all(type(x) is int for x in p['identity']), 'Python integer seven ID')
    require(p['identity'][4] == p['size_bytes'], 'PF matching size')


def current(p):
    budget(); typed(p); q = Path(p['path']); s = q.lstat()
    require(stat.S_ISREG(s.st_mode) and identity(s) == p['identity'], 'exact current7: ' + str(q))
    require(not any(x.is_symlink() for x in (q, *q.parents)), 'no aliases: ' + str(q))


def exact(p):
    current(p); q = Path(p['path'])
    require((q.suffix in ('.py', '.json') or GUARD_LOGS.get(str(q)) == p or NEW_OUTPUTS.get(str(q)) == p) and p['size_bytes'] < 8 * 2**20,
            'bounded Source/report metadata only')
    raw = bytearray(); digest = hashlib.sha256(); total = 0
    with q.open('rb') as f:
        require(identity(os.fstat(f.fileno())) == p['identity'], 'opened current7')
        while True:
            budget(); part = f.read(2**20)
            if not part:
                break
            raw.extend(part); digest.update(part); total += len(part)
        require(identity(os.fstat(f.fileno())) == p['identity'], 'EOF current7')
    require(total == p['size_bytes'] and digest.hexdigest() == p['sha256'], 'whole EOF PF')
    current(p); return bytes(raw)


def pin(q):
    q = Path(q); s = q.lstat()
    require((q.suffix in ('.py', '.json') or str(q) in GUARD_LOGS or str(q) in NEW_OUTPUTS) and s.st_size < 8 * 2**20, 'own Source/report or literal guard control role only')
    p = dict(path=str(q), sha256=hashlib.sha256(q.read_bytes()).hexdigest(),
             size_bytes=s.st_size, identity=identity(s))
    current(p); require(str(q) not in GUARD_LOGS or GUARD_LOGS[str(q)] == p, 'own exact original guard log fullPF'); return p


def read(p):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key'); result[key] = value
        return result
    return json.loads(exact(p), object_pairs_hook=pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def closed0(value, key, output_key, wanted):
    t = value[key]
    require(value['observed_closed'] is True and
            type(value['original_integer_exit_code']) is int and value['original_integer_exit_code'] == 0 and
            type(t['exit_code']) is int and t['exit_code'] == 0 and t.get('session_id') is None and
            json.loads(t['output'].strip().splitlines()[-1])[output_key] == wanted,
            'genuine exact stdout-PF typed closed0')


def unique(rows):
    result = {}
    for p in rows:
        typed(p)
        require(p['path'] not in result or result[p['path']] == p, 'consistent whole PF union')
        result[p['path']] = p
    return list(result.values())


def main():
    require(len(sys.argv) == 1 and not sys.flags.optimize and sys.getprofile() is None, 'fixed bounded postverify')
    freeze_pin = pin(HERE / 'AUDITOR_SOURCE_ONLY_FREEZE.json'); freeze = read(freeze_pin)
    require(freeze['auditor_Source_AST_parsed_before_freeze_and_execution'] is True and
            freeze['auditor_source_pin'] == pin(Path(__file__).absolute()), 'AST and whole auditor freeze')
    ast.parse(exact(freeze['auditor_source_pin']))
    rows = freeze['complete_metadata_Source_and_new_output_pins']
    contents = {p['path']: exact(p) for p in rows}
    for p in freeze['scientific_input_and_logical_inventory_current7_only_pins'] + freeze['inherited_metadata_current7_only_pins']:
        current(p)
    host_pin, child_pin, tools_pin, claim_pin = (freeze[k]for k in ('host_pin','child_pin','Root_actual_tools_pin','claim_pin'))
    host, child, tools, claim = read(host_pin), read(child_pin), read(tools_pin), read(claim_pin)
    closed0(tools, 'actual_terminal_return', 'report_pin', host_pin)
    require(tools['actual_initial_return']['chunk_id'] == 'f59794' and tools['actual_initial_return']['session_id'] == 95151 and
            tools['actual_terminal_return']['chunk_id'] == '38b4de', 'genuine owning Root initial and final returns')
    require(host['schema'] == 'ACTUAL_ROOT_62SLOT_TEMPERATURE_OPERAND_CAPTURE_V1' and
            host['status'] == 'ACTUAL_TEMPERATURE_OPERAND_CAPTURE_CLOSED0_ONLY' and host['failure'] is None and
            host['secondary_failures'] == [] and host['final_report_resource_check_passed'] is True, 'actual Root0 no failure')
    require(claim['schema'] == 'ACTUAL_TEMPERATURE_OPERAND_ONCE_ROOT_CLAIM_V1' and
            claim['status'] == 'ACTUAL_ONCE_TEMPERATURE_OPERAND_CAPTURE_RETURNED0_ONLY' and claim['failure'] is None and
            claim['exclusive_claim_before_source_metadata_resource_or_scientific_input_checks'] is True and
            claim['actual_Root_report_pin'] == host_pin, 'exclusive claim completed with exact Root report')
    plan = read(host['plan_pin']); ready = read(freeze['ready_pin']); seed = read(plan['seed_pin'])
    source_review = read(host['source_review_pin']); source_tools = read(host['source_review_tools_pin'])
    gen = read(host['source_generation_tools_pin'])
    require(source_review['status'] == 'PASS_CURRENT62_TEMPERATURE_OPERAND_V5_SOURCE_REVIEW_ONLY' and
            source_review['failure'] is None and source_review['concrete_blockers'] == [], 'same actual Source peer PASS')
    closed0(source_tools, 'actual_review_return', 'review_pin', host['source_review_pin'])
    closed0(gen, 'actual_Source_preparation_return', 'ready_pin', freeze['ready_pin'])
    require(source_tools['actual_review_return']['chunk_id'] == 'f1b85d' and
            gen['actual_Source_preparation_return']['chunk_id'] == 'db2515', 'actual Source peer0 and generation0')
    fixed = host['fixed_Source_metadata_before_after_full_PF_pins']
    require(all(p in fixed for p in ready['selected_Source_and_metadata_pins'] +
                [host['plan_pin'], freeze['ready_pin'], host['source_review_pin'], host['source_review_tools_pin'], host['source_generation_tools_pin']]) and
            all(p in rows for p in fixed) and host['selected_Source_and_metadata_before_verified'] is True and
            host['selected_Source_and_metadata_after_verified'] is True and host['selected_Source_and_metadata_before_after_verified'] is True,
            'complete exact Source and metadata actual before/after coverage')
    argv_meta, light, light_tools = (read(freeze[k]) for k in ('Root_argv_pin','Root_light_pin','Root_light_tools_pin'))
    argv = argv_meta['argv']
    require(argv_meta['command'] == tools['argv_command'] and light['exact_argv'] == argv and
            light['status'] == 'PASS_EXACT_CURRENT_REVIEWED_ROOT_ARGV_AND_ONCE_ABSENCE' and light['failure'] is None and
            light['plan_pin'] == host['plan_pin'] and light['complete_joint_roots_count'] == 56, 'exact Root argv/light proof')
    lt = light_tools['actual_light_return']
    require(light_tools['observed_closed'] is True and type(light_tools['original_integer_exit_code']) is int and
            light_tools['original_integer_exit_code'] == 0 and type(lt['exit_code']) is int and lt['exit_code'] == 0 and
            lt.get('session_id') is None and lt['chunk_id'] == 'ea7d6a' and
            json.loads(lt['output'])['status'] == light['status'], 'genuine light0 retained')
    for flag,key in [('--review-pin','source_review_pin'),('--review-tools-pin','source_review_tools_pin'),('--generation-tools-pin','source_generation_tools_pin')]:
        require(argv.count(flag) == 1 and json.loads(argv[argv.index(flag)+1]) == host[key], 'exact Python integer Root PF arguments')
    require(argv.count('--mode') == 1 and argv[argv.index('--mode')+1] == 'root' and
            claim['source_path'] in argv, 'one owning root mode, no rerun')
    require(len(host['records']) == 1, 'one original child')
    record = host['records'][0]; stage_pin = freeze['stage_pin']; stages = read(stage_pin)
    require(stages == {'stages':host['records']} and record['status'] == 'PASS' and
            record['label'] == 'capture/temperature_operand', 'actual one PASS stage preserved')
    watch_pin, log_pin = freeze['watch_pin'], freeze['log_pin']; watch = read(watch_pin)
    require(set(watch) == {'command','pid','returncode','elapsed_seconds','sampled_peak_rss_mib','limit_failure',
                         'wall_cap_seconds','rss_cap_mib','own_child_only','liveness_group_cleanup'}, 'actual raw monitor schema')
    require(type(watch['pid']) is int and watch['pid'] > 0 and type(watch['returncode']) is int and watch['returncode'] == 0 and
            watch['limit_failure'] is None and watch['command'] == record['command'] and
            0 <= watch['sampled_peak_rss_mib'] < 512 and watch['rss_cap_mib'] == 512 and
            0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= record['wall_cap_seconds'] <= 600 and
            watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True, 'genuine typed child0 original guard')
    require(host['actual_watchdog'] == dict(path=watch_pin['path'],sha256=watch_pin['sha256'],
                                          peak_rss_mib=watch['sampled_peak_rss_mib'],elapsed_seconds=watch['elapsed_seconds']) and
            record['log_sha256'] == log_pin['sha256'], 'structured helper assessment exactly matches raw monitor')
    command = record['command']
    require(command[:3] == ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',claim['source_path']] and
            command[3:6] == ['--mode','child','--plan-pin'] and json.loads(command[6]) == host['plan_pin'] and
            command[7] == '--expected-parent' and int(command[8]) > 0, 'exact child Source/plan and owning parent PID argument')
    log = contents[log_pin['path']].decode().splitlines()
    require(len(log) == 1 and json.loads(log[0]) == host['actual_child_receipt'] and
            json.loads(log[0])['report_pin'] == child_pin, 'actual child receipt exact fullPF')
    require(child['schema'] == 'ACTUAL_CURRENT_62SLOT_TEMPERATURE_OPERAND_CAPTURE_V1' and
            child['status'] == 'CURRENT_62SLOT_NATIVE_REAL32_TEMP_MIX_NAMES_AND_EXPECTED_C_TO_K_WORDS_CAPTURED_ONLY' and
            child['plan_pin'] == host['plan_pin'] and child['captured_record_count'] == 4 and
            child['captured_bytes'] == 1984 and child['captured_temperature_slots'] == 62 and
            child['all62_expected_C_to_K_REAL32_words_equal'] is True and
            0 <= child['child_SELF_peak_bytes'] < 512*2**20 and 0 < child['child_elapsed_seconds'] < 600,
            'complete actual narrow child capture')
    science = freeze['scientific_input_and_logical_inventory_current7_only_pins']
    require(host['initial_original_science_whole_PF_pins'] == plan['scientific_input_current7_pins'] ==
            [child['original_SQLite_pin'],child['original_pool_pin']] == science[:2] and
            child['original_fixed_context_pin'] == seed['fixed_context_pin'], 'same original final55 input pair')
    ctx = read(seed['fixed_context_pin']); selected = child['selected_descriptors']; raw_pin = freeze['raw_pin']
    raw = contents[raw_pin['path']]
    require(raw_pin == child['raw_capture_pin'] and len(raw) == 1984 and len(selected) == 4,
            'only new captured raw1984B decoded')
    parts = []; offset = 0
    for capture,expected,size in zip(selected,plan['selected_original_records'],[248,744,744,248]):
        part = raw[offset:offset+size]; digest = hashlib.sha256(part).hexdigest()
        require(capture['original_record'] == expected and capture['captured_offset_bytes'] == offset and
                capture['captured_bytes'] == size and digest == capture['captured_sha256'] == expected['native_payload_sha256'] and
                ctx['original_context_records'][json.dumps(expected['path'],separators=(',',':'))]['original_record'] == expected,
                'exact typed original descriptor and new captured byte-slice SHA')
        parts.append(part); offset += size
    require(offset == 1984 and [r['original_record']['path'] for r in selected] ==
            [['ISOTOPESTEMP'],['ISOTOPESUSED'],['ISOTOPERNAME'],['ISOTOPESMIX']], 'literal complete selected order')
    case = read(plan['current_case_spec_pin']); material = case['materials']; slots = child['slots']
    require(len(slots) == 62 and material['temperature_C_in_every_zone'] == dict(clad_and_gap=620,fuel_and_hole=750,sodium=475) and
            material['kelvin_offset'] == 273.15, 'same exact current parameter metadata')
    computed_slots = []
    for i,(temp,mix) in enumerate(zip(struct.unpack('<62f',parts[0]),struct.unpack('<62i',parts[3]))):
        budget(); require(type(mix) is int and 1 <= mix <= 8, 'actual original mix1..8')
        celsius = material['temperature_C_in_every_zone'][plan['expected_C_by_mix'][str(mix)]]
        expected = struct.pack('<f',float(celsius)+float(material['kelvin_offset'])); actual = parts[0][4*i:4*i+4]
        require(actual == expected, 'actual captured REAL32 word equals scoped expected C-to-K word')
        value = dict(slot_one_based=i+1,original_mix=mix,original_USED_12byte_hex=parts[1][12*i:12*i+12].hex(),
                     original_RNAME_12byte_hex=parts[2][12*i:12*i+12].hex(),original_USED_ascii=parts[1][12*i:12*i+12].decode('ascii'),
                     original_RNAME_ascii=parts[2][12*i:12*i+12].decode('ascii'),original_native_REAL32_temperature_K=temp,
                     original_native_REAL32_word_hex=actual.hex(),current_parameter_temperature_C=celsius,
                     current_kelvin_offset=material['kelvin_offset'],expected_C_to_K_REAL32_word_hex=expected.hex(),
                     expected_C_to_K_REAL32_words_equal=True)
        require(value == slots[i], 'all original names/mix/temp/current parameter slot fields from new bytes')
        computed_slots.append(value)
    loops = dict(Root_parent_before_child=1,child_original_constructor_before_selected_pread=1,
                 child_original_close_after_selected_pread=1,total_Root_parent=1,total_child=2,total_per_original_SQL_or_pool_file=3)
    require(host['planned_full_input_EOF_loops_per_file'] == plan['planned_full_input_EOF_loops_per_file'] == loops and
            host['actual_Root_parent_full_input_EOF_loops_per_file'] == 1 and host['actual_completed_child_full_input_EOF_loops_per_file'] == 2 and
            child['actual_child_full_input_EOF_loops_per_file'] == 2 and child['child_input_full_EOF_stages'] ==
            ['original_constructor_before_selected_pread','original_close_after_selected_pread'] and
            host['current_root_only_full_SQL_pool_EOF_before_selected_pread'] is child['current_root_only_full_SQL_pool_EOF_before_selected_pread'] is False and
            host['selected_pread_payload_bytes_only'] == child['selected_pread_payload_bytes_only'] == 1984,
            'truthful three complete EOF loops per original input file versus selected1984B pread')
    caps = plan['original_caps']; roots = plan['complete_joint_roots']
    require(host['original_caps'] == child['original_caps'] == caps and host['complete_joint_roots'] == roots and
            len(roots) == len(set(roots)) == 56 and any(BASE.is_relative_to(Path(p)) for p in roots), 'inherited56 roots/original caps')
    resource_facts = []
    for label,snap in [('Root_before',host['resources_before']),('Root_after',host['resources_after']),
                       ('child_stage_before',record['resource_before']),('child_stage_after',record['resource_after'])]:
        hist,joint = snap['original_history'],snap['complete_joint']
        require(hist['artifact_budget_bytes'] == 96*2**30 and hist['min_free_bytes'] == 8*2**30 and
                joint['artifact_budget_bytes'] == 2*2**30 and joint['min_free_bytes'] == 8*2**30 and
                joint['resource_roots'] == roots and
                hist['artifact_bytes']+caps['cold_reserve_bytes']+64*2**20 < 96*2**30 and
                joint['artifact_bytes']+snap['explicit_external_metadata_bytes']+snap['host_open_unlinked_bytes'] < 2*2**30 and
                joint['disk_free_bytes']-caps['cold_reserve_bytes']-2*2**30 >= 8*2**30 and
                0 <= snap['host_SELF_peak_bytes'] < 512*2**20 and 0 <= snap['whole_elapsed_seconds'] < 1800,
                'actual resource snapshot unchanged original caps')
        resource_facts.append(dict(label=label,history_bytes=hist['artifact_bytes'],joint_bytes=joint['artifact_bytes'],
                                   explicit_external_metadata_bytes=snap['explicit_external_metadata_bytes'],
                                   host_open_unlinked_bytes=snap['host_open_unlinked_bytes'],disk_free_bytes=joint['disk_free_bytes'],
                                   host_SELF_peak_bytes=snap['host_SELF_peak_bytes'],whole_elapsed_seconds=snap['whole_elapsed_seconds']))
    author = read(plan['author_source_freeze_pin'])
    for version,chunk in [('v2','f6e471'),('v3','b89517')]:
        prior_pin,prior_tools_pin = (author['preserved_formal_failed_'+version+'_review_pin'],author['preserved_formal_failed_'+version+'_review_tools_pin'])
        prior,prior_tools = read(prior_pin),read(prior_tools_pin); closed0(prior_tools,'actual_review_return','review_pin',prior_pin)
        require(prior['status'].startswith('FAILED') and prior['failure'] is not None and
                prior['Root_runtime_admission_issued'] is False and prior_tools['actual_review_return']['chunk_id'] == chunk,
                'original failed history exact audit0 remains refused')
    extraction_post,extraction_primary,extraction_tools,extraction_root = (read(seed[k])for k in
        ('original_extraction_post_pin','original_extraction_post_primary_pin','original_extraction_post_tools_pin','original_extraction_Root_tools_pin'))
    closed0(extraction_tools,'actual_review_return','review_pin',seed['original_extraction_post_primary_pin'])
    require(extraction_post['failure'] is None and extraction_primary['failure'] is None and
            extraction_post['actual_child_integer_exit_code'] == extraction_primary['actual_child_integer_exit_code'] == 2 and
            type(extraction_root['original_integer_exit_code']) is int and extraction_root['original_integer_exit_code'] == 0 and
            type(extraction_root['actual_terminal_return']['exit_code']) is int and extraction_root['actual_terminal_return']['exit_code'] == 0 and
            extraction_root['observed_closed'] is True, 'original extraction Root0/post0/intentional child2 retained')
    false_flags = ['business_executed','numerical_executed','compiler_executed','files_deleted','physics_qualified','scientific_accuracy_qualified',
                   'complete_reaction_authority_qualified','physical_neutron_balance_qualified','full_reference_qualified','unreduced_reference_qualified',
                   'finite18_replayed','temperature_interpolation_replayed','current_SPH_MASK_context_applied','native_AxMatTone_temperature_mapping_qualified',
                   'stored_native_REAL32_temperature_selection_qualified','historical_native_RAM_bits_verified','original_XSM_memory_bits_verified',
                   'AAA_qualified','ABA_admitted','goal_complete']
    for value in (host,child,claim):
        require(all(value[k] is False for k in false_flags) and value['actual_temperature_operand_capture_executed'] is True,
                'actual narrow capture retains every broad scope flag false')
    require(set(host['output_paths']) == set(NEW_OUTPUTS)-{host_pin['path']} and
            all(pin(Path(p['path'])) == p for p in freeze['new_output_pins']), 'all seven new outputs exact complete PF')
    for p in rows:
        require(exact(p) == contents[p['path']], 'second whole metadata/Source/new output EOF PF')
    for p in science + freeze['inherited_metadata_current7_only_pins']:
        current(p)
    budget()
    report = dict(schema='INDEPENDENT_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_POSTVERIFY_V1',
                  status='PASS_ACTUAL_CURRENT62_TEMPERATURE_OPERAND_CAPTURE_ONLY_POSTVERIFICATION',failure=None,
                  auditor_source_pin=freeze['auditor_source_pin'],auditor_source_freeze_pin=freeze_pin,
                  actual_Root_tools_pin=tools_pin,actual_Root_integer_exit_code=0,actual_Root_report_pin=host_pin,
                  actual_child_report_pin=child_pin,actual_child_integer_exit_code=0,actual_exclusive_claim_pin=claim_pin,
                  actual_raw_monitor_pin=watch_pin,actual_raw_monitor=watch,actual_helper_monitor_assessment=host['actual_watchdog'],
                  actual_Root_argv_pin=freeze['Root_argv_pin'],actual_Root_light_pin=freeze['Root_light_pin'],actual_Root_light_tools_pin=freeze['Root_light_tools_pin'],
                  actual_Source_review_pin=host['source_review_pin'],actual_Source_review_tools_pin=host['source_review_tools_pin'],
                  actual_Source_generation_tools_pin=host['source_generation_tools_pin'],actual_plan_pin=host['plan_pin'],
                  all_new_output_pins=freeze['new_output_pins'],all_new_outputs_full_EOF_PF_verified_twice=True,
                  new_raw_1984B_capture_pin=raw_pin,new_raw_all4_descriptor_bytes_SHA_verified=True,
                  captured_record_count=4,captured_bytes=1984,captured_temperature_slots=62,
                  all62_expected_C_to_K_REAL32_words_equal=True,all62_original_mix_USED_RNAME_temperature_slot_fields_verified=True,
                  actual_selected_descriptors=selected,actual_slot_fields= computed_slots,
                  complete_metadata_Source_and_new_output_pins=rows,complete_metadata_Source_full_EOF_PF_verified_twice=True,
                  actual_Host_fixed_Source_metadata_pins=fixed,actual_Host_fixed_Source_metadata_current7_verified_twice=True,
                  scientific_input_and_logical_inventory_current7_only_pins=science,old_scientific_inputs_current7_verified_twice=True,
                  inherited_metadata_current7_only_pins=freeze['inherited_metadata_current7_only_pins'],inherited_metadata_current7_verified_twice=True,
                  complete_joint_roots=roots,original_caps=caps,actual_original_resource_snapshot_facts=resource_facts,
                  truthful_full_input_EOF_loops_per_file=loops,selected_pread_payload_bytes_only=1984,
                  current_root_only_full_SQL_pool_EOF_before_selected_pread=False,
                  old_SQL_pool_XSM_GENDF_SCI_bodies_opened_or_hashed=False,new_raw1984B_only_decoded=True,
                  original_failed_v2_v3_and_unadmitted_v4_histories_preserved=True,original_extraction_Root0_post0_intentional_child2_preserved=True,
                  original_checker_preflight_failure_pin=freeze['original_checker_preflight_failure_pin'],
                  original_unfrozen_checker_Source_pin=freeze['original_unfrozen_checker_Source_pin'],
                  original_preflight_integer_exit_code1_preserved=True,
                  no_current_runtime_budget_admission_issued=True,helper_or_candidate_imported=False,
                  native_child_reexecuted=False,actual_capture_executed_by_reviewer=False,
                  Source_generation_executed_by_reviewer=False,**{k:False for k in false_flags},
                  SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024),elapsed_seconds=time.monotonic()-START)
    with (HERE/'REVIEW.json').open('x') as f:
        json.dump(report,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    rp=pin(HERE/'REVIEW.json');budget()
    print(json.dumps(dict(status=report['status'],review_pin=rp),separators=(',',':')),flush=True)


if __name__=='__main__':
    main()
