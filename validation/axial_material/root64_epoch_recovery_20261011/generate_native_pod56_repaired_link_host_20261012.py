#!/usr/bin/env python3
"""Repair the demonstrated missing native POD object with one complete Source compile."""
import importlib.util
import json
import os
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
ART = ROOT / 'validation/artifacts'
sp = importlib.util.spec_from_file_location('full_current_build_Source_helpers', REC / 'generate_true_online_complete_link_host_20261012.py')
common = importlib.util.module_from_spec(sp)
sp.loader.exec_module(common)
pin = common.pin
sha = common.sha
SOURCE = ROOT / 'src/SPOPOD.f90'
TEMPLATE = REC / 'build_complete_true_online_boot_operator_route_only_20261012.py'
HOST = REC / 'build_complete_true_online_boot_operator_native_pod56_only_20261012.py'
PLAN = REC / 'TRUE_ONLINE_BOOT_NATIVE_POD56_CURRENT_BUILD_PLAN_20261012.json'
FREEZE = REC / 'TRUE_ONLINE_BOOT_NATIVE_POD56_SOURCE_DEPENDENCY_FREEZE_20261012.json'
DERIVATION = REC / 'TRUE_ONLINE_BOOT_NATIVE_POD56_BUILD_HOST_DERIVATION_20261012.json'
OUT = ART / 'axial-material-new-true-online-BOOT-native-POD56-complete-route-build-only-20261012-v2'


def main():
    for path in (HOST, PLAN, FREEZE, DERIVATION, OUT):
        if path.exists() or path.is_symlink():
            raise RuntimeError('fresh missing-native-POD repair only; no overwrite')
    if pin(TEMPLATE)['sha256'] != '5ba106142ffc7c0347da6b325c4f80397b9bdd51e2ad3404c1921ca2f195fa71':
        raise RuntimeError('actual failed predecessor host full Source changed')
    if pin(SOURCE)['sha256'] != '488c5e9e262ae171ca2a3ce52c26273dc61e082e0fc395af6cd35022c53d9f0d':
        raise RuntimeError('original frozen complete native POD Source changed')
    original_plan_path = REC / 'TRUE_ONLINE_BOOT_OPERATOR_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'
    original_plan = json.loads(original_plan_path.read_text())
    failed_path = ART / 'axial-material-new-true-online-BOOT-operator-complete-route-build-only-20261012/Root_actual_build_only_summary.json'
    failed = json.loads(failed_path.read_text())
    if len(failed['records']) != 2 or [r['status'] for r in failed['records']] != ['PASS', 'FAILED']:
        raise RuntimeError('exact actual successful dispatcher and failed full link required')
    log_path = failed_path.parent / 'build/link_Dragon.log'
    log = log_path.read_text()
    expected_log = 'Undefined symbols for architecture arm64:\n  "_spopod64_", referenced from:\n      _spoasmg64_ in SPOASMG64.o\nld: symbol(s) not found for architecture arm64\ncollect2: error: ld returned 1 exit status\n'
    if log != expected_log or failed['after_check_error'] is not None:
        raise RuntimeError('whole real failed link log not exactly native POD dependency gap')
    base = failed['records'][-1]['command']
    if base != original_plan['complete_link_command'] or len(base[3:-2]) != 55:
        raise RuntimeError('exact actually attempted complete 55-input link')
    includes = original_plan['includes']
    flags = original_plan['original_compile_flags']
    build = OUT / 'build'
    compiler = base[0]
    commands = [[compiler, *flags, '-I' + str(build), *['-I' + p for p in includes],
                 '-J' + str(build), '-c', str(SOURCE), '-o', str(build / 'SPOPOD.o')]]
    extra = [str(build / 'SPOPOD.o')]
    link = [compiler, '-O2', '-ffp-contract=off', *base[3:-6], *extra, *base[-6:-2], '-o', str(OUT / 'runtime/Dragon')]
    if len(link[3:-2]) != 56:
        raise RuntimeError('full repaired 56-input link scope')
    failed_outputs = {p['path']: p for p in failed['output_pins']}
    dispatcher = failed_path.parent / 'build/KDRDRV.o'
    if str(dispatcher) not in failed_outputs or pin(dispatcher) != failed_outputs[str(dispatcher)]:
        raise RuntimeError('genuine actual passed dispatcher object required')
    common.common.write(FREEZE, dict(scope='Complete existing SPOPOD64 Source and actual missing-symbol diagnosis; no numeric or physics qualification',
                                    source=pin(SOURCE), source_changes=0,
                                    actual_passed_dispatcher_object=pin(dispatcher),
                                    actual_failed_full_link_summary=pin(failed_path), actual_full_failed_link_log=pin(log_path),
                                    original_guard_caps_unchanged=True, automatic_retry=False,
                                    next_action='one complete existing SPOPOD Source compile and full repaired56 link in a new fresh directory'))
    declared = original_plan['current_full_EOF_pins'] + failed['output_pins']
    declared.extend(pin(p) for p in (TEMPLATE, SOURCE, original_plan_path, failed_path, log_path, FREEZE, Path(__file__).resolve()))
    by_path = {}
    for p in declared:
        if pin(p['path']) != p:
            raise RuntimeError('full pinned precursor Source/object/reference changed')
        if p['path'] in by_path and by_path[p['path']] != p:
            raise RuntimeError('duplicate input identity conflict')
        by_path[p['path']] = p
    old = TEMPLATE.read_text()
    new = old
    steps = []
    def replace(label, before, after):
        nonlocal new
        if new.count(before) != 1:
            raise RuntimeError('exact repaired host transformation cardinality: ' + label)
        offset = new.index(before)
        prior = new
        new = new[:offset] + after + new[offset + len(before):]
        steps.append(dict(label=label, byte_offset=len(prior[:offset].encode()), old=before, new=after,
                          before_sha256=sha(prior.encode()), after_sha256=sha(new.encode())))
    replace('scope', 'Compile legal true online dispatcher and complete 55-input operator/BOOT Dragon link; no transport.', 'Compile complete native POD dependency and full repaired56-input operator/BOOT Dragon link; no transport.')
    replace('fresh repaired56 output', "OUT=ART/'axial-material-new-true-online-BOOT-operator-complete-route-build-only-20261012'", "OUT=ART/'axial-material-new-true-online-BOOT-native-POD56-complete-route-build-only-20261012-v2'")
    replace('complete native POD Source freeze', "FREEZE=ROUTE/'COMPLETE_CURRENT_ONLINE_BOOT_DISPATCHER_SOURCE_FREEZE.json'", "FREEZE=REC/'TRUE_ONLINE_BOOT_NATIVE_POD56_SOURCE_DEPENDENCY_FREEZE_20261012.json'")
    replace('complete repaired56 exact build plan', "DECLARATION=REC/'TRUE_ONLINE_BOOT_OPERATOR_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'", "DECLARATION=REC/'TRUE_ONLINE_BOOT_NATIVE_POD56_CURRENT_BUILD_PLAN_20261012.json'")
    replace('new complete Source freeze SHA', '0c145b90fe947406a651705fe237ad571432400f20609995a4a6284f7fa06c63', pin(FREEZE)['sha256'])
    before = next(line for line in new.splitlines(True) if line.startswith('    reviewed_new_sources='))
    replace('exact complete native POD Source', before, '    reviewed_new_sources=' + repr({str(SOURCE): pin(SOURCE)['sha256']}) + '\n')
    replace('exact55 predecessor plus1 dependency', "if len(base[3:-2])!=48 or len(extra)!=7:raise RuntimeError('full link scope')", "if len(base[3:-2])!=55 or len(extra)!=1:raise RuntimeError('full link scope')")
    replace('reuse the actually passed dispatcher object without a fabricated fresh object', "original_objects=[str(build/'KDRDRV.o')if x==command_declaration['old_KDRDRV_object']else x for x in base[3:-6]]", "original_objects=list(base[3:-6])")
    replace('complete56 link validation', "if link!=expected_link or len(link[3:-2])!=55:raise RuntimeError('complete exact 55 ordered link inputs')", "if link!=expected_link or len(link[3:-2])!=56:raise RuntimeError('complete exact 56 ordered link inputs')")
    replace('actual native POD compile and full link scope', 'one legal short-alias dispatcher Source compile and complete 55 ordered input Dragon link; all original entries preserved plus actual native operator and true online BOOT callees; no transport, online BOOT, full archive Source-build or physics qualification', 'one unchanged complete existing native POD Source compile and complete repaired56 ordered input Dragon link; reuses only actual passed dispatcher object from the preserved failed55 attempt, adds missing SPOPOD64 with original math/ABI; no transport, online BOOT, full archive Source-build or physics qualification')
    replace('complete56 result count', 'complete_ordered_link_input_count=55', 'complete_ordered_link_input_count=56')
    replace('schema', "schema='ACTUAL_COMPLETE_TRUE_ONLINE_BOOT_NATIVE_OPERATOR_ROUTE_BUILD_ONLY_V1'", "schema='ACTUAL_COMPLETE_TRUE_ONLINE_BOOT_NATIVE_POD56_REPAIRED_ROUTE_BUILD_ONLY_V2'")
    replace('exact repaired status', "status='CURRENT_DISPATCHER_COMPILE_AND_COMPLETE_55_INPUT_DRAGON_LINK_CLOSED0_ONLY'", "status='NATIVE_POD_COMPILE_AND_COMPLETE_REPAIRED56_INPUT_DRAGON_LINK_CLOSED0_ONLY'")
    restored = new.encode()
    for step in reversed(steps):
        if sha(restored) != step['after_sha256']:
            raise RuntimeError('full actual predecessor host inverse after SHA')
        offset = step['byte_offset']
        before, after = step['old'].encode(), step['new'].encode()
        if restored[offset:offset + len(after)] != after:
            raise RuntimeError('full actual predecessor host inverse exact bytes')
        restored = restored[:offset] + before + restored[offset + len(after):]
        if sha(restored) != step['before_sha256']:
            raise RuntimeError('full actual predecessor host inverse before SHA')
    if restored != TEMPLATE.read_bytes():
        raise RuntimeError('full actual predecessor host not recovered')
    compile(new, str(HOST), 'exec')
    plan = dict(schema='EXACT_COMPLETE_TRUE_ONLINE_BOOT_NATIVE_POD56_REPAIRED_BUILD_PLAN_V2',
                current_full_EOF_pins=list(by_path.values()), compile_sources=[str(SOURCE)], compile_commands=commands,
                includes=includes, complete_link_command=link, original_compile_flags=flags,
                fresh_output_root=str(OUT), working_directory=str(build), prior_actual_complete_link=base,
                old_KDRDRV_object=str(dispatcher), additional_ordered_inputs=extra,
                complete_ordered_link_input_count=56, complete_original55_input_order_preserved=True,
                original_four_archive_order_retained=True, actual_missing_POD_link_failure=pin(log_path),
                genuine_passed_dispatcher_reused=True, source_changes=0, automatic_retry=False,
                compile_or_link_executed=False, transport_executed=False, online_BOOT_qualified=False)
    common.common.write(PLAN, plan)
    with HOST.open('x') as f:
        f.write(new)
        f.flush()
        os.fsync(f.fileno())
    common.common.write(DERIVATION, dict(template=pin(TEMPLATE), current_host=pin(HOST), current_plan=pin(PLAN),
                                        complete_inverse_equals_complete_actual_failed_template_bytes=True,
                                        exact_host_transform_steps=steps, original_guard_body_MRO_unchanged=True,
                                        genuine_dependency_repair=True, automatic_retry=False,
                                        compiled=False, transport_executed=False, goal_complete=False))
    print(json.dumps(dict(host=pin(HOST), plan=pin(PLAN), exact_host_inverse_steps=len(steps),
                          compile_count=1, full_ordered_link_input_count=56, executed=False)))


if __name__ == '__main__':
    main()
