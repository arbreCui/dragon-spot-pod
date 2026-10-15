#!/usr/bin/env python3
"""Derive the actual full 55-input Dragon build without changing the original guard."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
ART = ROOT / 'validation/artifacts'
ROUTE = REC / 'online_boot_dispatcher_source_v1'
FREEZE = ROUTE / 'COMPLETE_CURRENT_ONLINE_BOOT_DISPATCHER_SOURCE_FREEZE.json'
TEMPLATE = REC / 'build_complete_bootstrap_cle_global_route_only_20261012.py'
HOST = REC / 'build_complete_true_online_boot_operator_route_only_20261012.py'
PLAN = REC / 'TRUE_ONLINE_BOOT_OPERATOR_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'
DERIVATION = REC / 'TRUE_ONLINE_BOOT_OPERATOR_COMPLETE_BUILD_HOST_DERIVATION_20261012.json'
OUT = ART / 'axial-material-new-true-online-BOOT-operator-complete-route-build-only-20261012'
COMMON = REC / 'generate_online_boot_seven_compile_host_20261012.py'
sp = importlib.util.spec_from_file_location('current_compile_host_source_helpers', COMMON)
common = importlib.util.module_from_spec(sp)
sp.loader.exec_module(common)
sha = common.sha


def pin(path):
    path = Path(path)
    def identity():
        s = path.lstat()
        if not stat.S_ISREG(s.st_mode):
            raise RuntimeError('original regular non-symlink fixed input required')
        return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    before = identity()
    with path.open('rb') as f:
        s = os.fstat(f.fileno())
        opened = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
        if opened != before:
            raise RuntimeError('original opened identity changed')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        s = os.fstat(f.fileno())
        eof = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
    if eof != before or identity() != before:
        raise RuntimeError('original EOF/after identity changed')
    return dict(path=str(path), size_bytes=before[4], sha256=digest, identity=before)


def norm(p):
    p = common.normalized(p)
    return dict(path=p['path'], size_bytes=p['bytes'], sha256=p['sha256'], identity=p['seven_id'])


def main():
    for path in (HOST, PLAN, DERIVATION, OUT):
        if path.exists() or path.is_symlink():
            raise RuntimeError('fresh complete build Source/OUT; no overwrite')
    if sha(TEMPLATE.read_bytes()) != 'd78d617f7f5c4afea1e217d353c300df33a8faea20ba3722bb7f5baedd005f62':
        raise RuntimeError('full actually executed 48-input build host Source changed')
    freeze = json.loads(FREEZE.read_text())
    frozen_files = freeze['files']
    for p in frozen_files:
        if pin(p['path']) != norm(p):
            raise RuntimeError('reviewed dispatcher freeze full EOF changed')
    source = ROUTE / 'KDRDRV.F'
    if pin(source)['sha256'] != '9f87dafbe62da049fd3c059f2fc79d0603013bc99ba88538eec3fc78db6fdac6':
        raise RuntimeError('independently reviewed legal short-alias dispatcher changed')
    proof = json.loads((ROUTE / 'COMPLETE_DISPATCHER_WHOLE_BYTE_INVERSE_PROOF.json').read_text())
    basis = REC / 'bootstrap_cle_entry_source_v1/KDRDRV.F'
    inverse = common.inverse(source, basis, proof)
    labels = re.findall(rb'HMODUL\.EQ\.\x27([^\x27]*)\x27', source.read_bytes())
    if len(labels) != 68 or len(set(labels)) != 68 or any(len(s) > 12 for s in labels):
        raise RuntimeError('exact complete 68 real CLE labels/width')
    if b'SPOBOOT64:' not in labels or b'SPOBOOTRUN64:' in labels:
        raise RuntimeError('actual supported short CLE alias')
    old_plan_path = REC / 'BOOTSTRAP_CLE_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'
    old_plan = json.loads(old_plan_path.read_text())
    old_summary_path = ART / 'axial-material-new-bootstrap-CLE-global-complete-route-build-only-20261012/Root_actual_build_only_summary.json'
    old_summary = json.loads(old_summary_path.read_text())
    seven_summary_path = ART / 'axial-material-new-true-online-BOOT-operator-seven-compile-only-20261012/Root_actual_compile_only_summary.json'
    seven_summary = json.loads(seven_summary_path.read_text())
    for summary in (old_summary, seven_summary):
        if summary['failure'] is not None or summary['after_check_error'] is not None:
            raise RuntimeError('actual precursor build did not close')
        if any(r['status'] != 'PASS' for r in summary['records']):
            raise RuntimeError('actual precursor build step did not pass')
    base = old_summary['records'][-1]['command']
    if base != old_plan['complete_link_command'] or len(base[3:-2]) != 48:
        raise RuntimeError('complete actual 48-input precursor command')
    seven_source_plan = json.loads((REC / 'online_boot_native64_source_v1/EXACT_CURRENT_SOURCE_COMPILE_ORDER_AND_TRUE_ROUTE.json').read_text())
    seven_build = seven_summary_path.parent / 'build'
    extras = [str(seven_build / (Path(name).stem + '.o')) for name in
              seven_source_plan['new_operator_source_order'] + seven_source_plan['new_boot_source_order']]
    actual_outputs = {p['path']: p for p in seven_summary['output_pins']}
    if len(extras) != 7 or any(p not in actual_outputs for p in extras):
        raise RuntimeError('actual full seven compiled objects required')
    includes = [str(seven_build)] + old_plan['includes']
    compiler = base[0]
    flags = old_plan['original_compile_flags']
    build = OUT / 'build'
    commands = [[compiler, *flags, '-I' + str(build), *['-I' + p for p in includes],
                 '-J' + str(build), '-c', str(source), '-o', str(build / 'KDRDRV.o')]]
    old_dispatcher_object = str(old_summary_path.parent / 'build/KDRDRV.o')
    if base.count(old_dispatcher_object) != 1:
        raise RuntimeError('one original dispatcher replacement only')
    objects = [str(build / 'KDRDRV.o') if p == old_dispatcher_object else p for p in base[3:-6]]
    link = [compiler, '-O2', '-ffp-contract=off', *objects, *extras, *base[-6:-2], '-o', str(OUT / 'runtime/Dragon')]
    if len(link[3:-2]) != 55 or link[-6:-2] != base[-6:-2]:
        raise RuntimeError('complete 55-input order and original four archives')
    declared = old_plan['current_full_EOF_pins'] + old_summary['output_pins'] + seven_summary['fixed_current_pins'] + seven_summary['output_pins'] + frozen_files
    declared.extend(pin(p) for p in (FREEZE, TEMPLATE, old_plan_path, old_summary_path, seven_summary_path, COMMON, Path(__file__).resolve()))
    by_path = {}
    for p in declared:
        p = norm(p)
        if pin(p['path']) != p:
            raise RuntimeError('whole current fixed Source/object/reference EOF or identity changed')
        if p['path'] in by_path and by_path[p['path']] != p:
            raise RuntimeError('duplicate input identity conflict')
        by_path[p['path']] = p
    old = TEMPLATE.read_text()
    new = old
    steps = []
    def replace(label, before, after):
        nonlocal new
        if new.count(before) != 1:
            raise RuntimeError('exact full host replacement count: ' + label)
        offset = new.index(before)
        prior = new
        new = new[:offset] + after + new[offset + len(before):]
        steps.append(dict(label=label, byte_offset=len(prior[:offset].encode()), old=before, new=after,
                          before_sha256=sha(prior.encode()), after_sha256=sha(new.encode())))
    replace('scope', 'Compile actual bootstrap CLE entries and complete 48-input global/native Dragon link; no transport.', 'Compile legal true online dispatcher and complete 55-input operator/BOOT Dragon link; no transport.')
    replace('fresh build root', "OUT=ART/'axial-material-new-bootstrap-CLE-global-complete-route-build-only-20261012'", "OUT=ART/'axial-material-new-true-online-BOOT-operator-complete-route-build-only-20261012'")
    replace('frozen dispatcher directory', "ROUTE=REC/'bootstrap_cle_entry_source_v1'", "ROUTE=REC/'online_boot_dispatcher_source_v1'")
    replace('current Source freeze', "FREEZE=ROUTE/'COMPLETE_BOOTSTRAP_CLE_ENTRY_SOURCE_FREEZE.json'", "FREEZE=ROUTE/'COMPLETE_CURRENT_ONLINE_BOOT_DISPATCHER_SOURCE_FREEZE.json'")
    replace('current whole link plan', "DECLARATION=REC/'BOOTSTRAP_CLE_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'", "DECLARATION=REC/'TRUE_ONLINE_BOOT_OPERATOR_COMPLETE_CURRENT_BUILD_PLAN_20261012.json'")
    replace('reviewed current dispatcher freeze SHA', '81a3dbfda485f3a0503ed15834d81ad1da9a540a317ea1457bb85da281f22ec4', pin(FREEZE)['sha256'])
    replace('one complete dispatcher Source', "if len(sources)!=3:raise RuntimeError('exact three full CLE Sources')", "if len(sources)!=1:raise RuntimeError('exact complete current dispatcher Source')")
    before = next(line for line in new.splitlines(True) if line.startswith('    reviewed_new_sources='))
    replace('exact reviewed current dispatcher Source SHA', before, '    reviewed_new_sources=' + repr({str(source): pin(source)['sha256']}) + '\n')
    replace('one exact dispatcher compile command', "if len(commands)!=3:raise RuntimeError('exact three compile commands')", "if len(commands)!=1:raise RuntimeError('exact one dispatcher compile command')")
    replace('full old48 and new7 link scope', "if len(base[3:-2])!=27 or len(extra)!=21:raise RuntimeError('full link scope')", "if len(base[3:-2])!=48 or len(extra)!=7:raise RuntimeError('full link scope')")
    replace('full55 ordered link validation', "if link!=expected_link or len(link[3:-2])!=48:raise RuntimeError('complete exact 48 ordered link inputs')", "if link!=expected_link or len(link[3:-2])!=55:raise RuntimeError('complete exact 55 ordered link inputs')")
    replace('exact new build scope', 'three actual standard CLE Source compiles and complete 48 ordered input Dragon link; global/project/Q callable routes added, original corrected native entry retained; no transport, online BOOT, full archive Source-build or physics qualification', 'one legal short-alias dispatcher Source compile and complete 55 ordered input Dragon link; all original entries preserved plus actual native operator and true online BOOT callees; no transport, online BOOT, full archive Source-build or physics qualification')
    replace('complete link count', 'complete_ordered_link_input_count=48', 'complete_ordered_link_input_count=55')
    replace('one compile then real link labels', "stage='compile_'+str(index)if index<3 else 'link_Dragon'", "stage='compile_'+str(index)if index<1 else 'link_Dragon'")
    replace('actual result schema', "schema='ACTUAL_COMPLETE_BOOTSTRAP_CLE_GLOBAL_ROUTE_BUILD_ONLY_V1'", "schema='ACTUAL_COMPLETE_TRUE_ONLINE_BOOT_NATIVE_OPERATOR_ROUTE_BUILD_ONLY_V1'")
    replace('actual result step status', "status='THREE_CLE_SOURCE_COMPILES_AND_COMPLETE_48_INPUT_DRAGON_LINK_CLOSED0_ONLY'", "status='CURRENT_DISPATCHER_COMPILE_AND_COMPLETE_55_INPUT_DRAGON_LINK_CLOSED0_ONLY'")
    restored = new.encode()
    for step in reversed(steps):
        if sha(restored) != step['after_sha256']:
            raise RuntimeError('full host inverse after SHA')
        offset = step['byte_offset']
        before, after = step['old'].encode(), step['new'].encode()
        if restored[offset:offset + len(after)] != after:
            raise RuntimeError('full host inverse exact splice')
        restored = restored[:offset] + before + restored[offset + len(after):]
        if sha(restored) != step['before_sha256']:
            raise RuntimeError('full host inverse before SHA')
    if restored != TEMPLATE.read_bytes():
        raise RuntimeError('full actual previous host inverse')
    compile(new, str(HOST), 'exec')
    plan = dict(schema='EXACT_COMPLETE_TRUE_ONLINE_BOOT_NATIVE_OPERATOR_BUILD_PLAN_V1',
                current_full_EOF_pins=list(by_path.values()), compile_sources=[str(source)],
                compile_commands=commands, includes=includes, complete_link_command=link,
                original_compile_flags=flags, fresh_output_root=str(OUT), working_directory=str(build),
                prior_actual_complete_link=base, old_KDRDRV_object=old_dispatcher_object,
                additional_ordered_inputs=extras, complete_ordered_link_input_count=55,
                original_44_object_order_retained_except_dispatcher=True, original_four_archive_order_retained=True,
                independent_Root_full_dispatcher_inverse=inverse,
                true_entry_mapping={'SPOOPG64:': 'SPOOPG64', 'SPOBOOT64:': 'SPOBOOTRUN64'},
                compiled_seven_actual_objects_bound=True, compile_or_link_executed=False,
                transport_executed=False, online_BOOT_qualified=False)
    common.write(PLAN, plan)
    with HOST.open('x') as f:
        f.write(new)
        f.flush()
        os.fsync(f.fileno())
    common.write(DERIVATION, dict(template=pin(TEMPLATE), current_host=pin(HOST), current_plan=pin(PLAN),
                                 complete_inverse_equals_complete_actual_template_bytes=True,
                                 exact_host_transform_steps=steps, full_dispatcher_inverse=inverse,
                                 fixed_complete_plan_inputs=len(by_path), original_guard_body_MRO_unchanged=True,
                                 compiled=False, transport_executed=False, goal_complete=False))
    print(json.dumps(dict(host=pin(HOST), plan=pin(PLAN), exact_host_inverse_steps=len(steps),
                          compile_count=1, full_ordered_link_input_count=55, executed=False)))


if __name__ == '__main__':
    main()
