#!/usr/bin/env python3
"""Bind complete frozen operator/BOOT Source to the unchanged actual bounded host."""
import ast
import hashlib
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
PACKAGE = REC / 'online_boot_native64_source_v1'
TEMPLATE = REC / 'compile_global_native64_caller_v2_dependencies_only_20261012.py'
HOST = REC / 'compile_true_online_boot_operator_seven_only_20261012.py'
BINDING = REC / 'TRUE_ONLINE_BOOT_OPERATOR_CURRENT_COMPILE_BINDING_20261012.json'
DERIVATION = REC / 'TRUE_ONLINE_BOOT_OPERATOR_COMPILE_HOST_DERIVATION_20261012.json'
FREEZE = PACKAGE / 'COMPLETE_TRUE_ONLINE_BOOT_AND_OPERATOR_SOURCE_FREEZE.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    s = Path(path).lstat()
    if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
        raise RuntimeError('regular single-link fixed input required')
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = identity(path)
    with path.open('rb') as f:
        s = os.fstat(f.fileno())
        opened = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                  s.st_mtime_ns, s.st_ctime_ns]
        if opened != before:
            raise RuntimeError('opened identity changed')
        digest = hashlib.file_digest(f, 'sha256').hexdigest()
        s = os.fstat(f.fileno())
        eof = [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
               s.st_mtime_ns, s.st_ctime_ns]
    if eof != before or identity(path) != before:
        raise RuntimeError('EOF/after identity changed')
    return dict(path=str(path), bytes=before[4], sha256=digest, seven_id=before)


def normalized(p):
    return dict(path=p['path'], bytes=p.get('bytes', p.get('size_bytes')),
                sha256=p['sha256'], seven_id=p.get('seven_id', p.get('identity')))


def write(path, value):
    with path.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())


def inverse(candidate, basis, proof):
    data = candidate.read_bytes()
    if sha(data) != proof['candidate_sha256']:
        raise RuntimeError('frozen complete candidate differs')
    for step in reversed(proof['steps']):
        if sha(data) != step['after_sha256']:
            raise RuntimeError('complete inverse after SHA')
        old, new = step['old'].encode(), step['new'].encode()
        if step['mode'] == 'exact_local_byte_splice':
            offset = step['byte_offset']
            if data[offset:offset + len(new)] != new:
                raise RuntimeError('complete inverse exact offset')
            data = data[:offset] + old + data[offset + len(new):]
        elif step['mode'] == 'whole_identifier_rename':
            pattern = rb'(?<![A-Za-z0-9_])' + re.escape(new) + rb'(?![A-Za-z0-9_])'
            data, count = re.subn(pattern, lambda _: old, data)
            if count != step['count']:
                raise RuntimeError('whole identifier inverse count')
        else:
            raise RuntimeError('undeclared complete Source transformation')
        if sha(data) != step['before_sha256']:
            raise RuntimeError('complete inverse before SHA')
    if data != basis.read_bytes() or sha(data) != proof['basis_sha256']:
        raise RuntimeError('complete inverse not equal complete original Source')
    return dict(candidate=str(candidate), basis=str(basis),
                complete_inverse_equals_complete_basis_bytes=True,
                steps=len(proof['steps']), candidate_sha256=proof['candidate_sha256'],
                basis_sha256=proof['basis_sha256'])


def main():
    for path in (HOST, BINDING, DERIVATION):
        if path.exists() or path.is_symlink():
            raise RuntimeError('fresh Source binding only; no overwrite')
    if sha(TEMPLATE.read_bytes()) != 'cd2e6b21389a561ce8b11fc55dedf29555e219e85ee03a59c381cb5cb80030da':
        raise RuntimeError('actually executed previous host full Source changed')
    if pin(FREEZE)['sha256'] != '88cb3d57d5a4df75f8e407f5a12683611e9b9dfbcbcc9f73e44bb223ece9d9f5':
        raise RuntimeError('complete independent Source freeze changed')
    freeze = json.loads(FREEZE.read_text())
    declared = freeze['fixed_files'] + [pin(FREEZE)]
    for name, key_before, key_after in [
        ('CURRENT_COMPLETE_ONLINE_BOOT_SOURCE_BINDING.json', 'complete_dependencies_before', 'complete_dependencies_after'),
        ('operator_source_v2/CURRENT_COMPLETE_NATIVE_RADIAL_OPERATOR_SOURCE_BINDING.json', 'basis_and_protected_dependencies_before', 'after')]:
        d = json.loads((PACKAGE / name).read_text())
        if d[key_before] != d[key_after]:
            raise RuntimeError('Source dependency before/after mismatch')
        declared.extend(d[key_before])
    proofs = json.loads((PACKAGE / 'COMPLETE_ONLINE_BOOT_WHOLE_BYTE_INVERSE_PROOFS.json').read_text())
    operator_proofs = json.loads((PACKAGE / 'operator_source_v2/COMPLETE_NATIVE_RADIAL_OPERATOR_WHOLE_BYTE_PROOFS.json').read_text())
    inverse_results = [
        inverse(PACKAGE / 'SPOR64_BOOTB64.f90', ROOT / 'src/SPOR64_B2B.f90', proofs['kernel']),
        inverse(PACKAGE / 'SPOR64_BOOTC64.f90', ROOT / 'src/SPOR64_B2C.f90', proofs['publisher']),
        inverse(PACKAGE / 'operator_source_v2/SPOASMG64.f', ROOT / 'src/SPOASM.f', operator_proofs['SPOASMG64']),
        inverse(PACKAGE / 'operator_source_v2/SPOT_RADIAL_NATIVE_MATH64.f90', ROOT / 'src/SPOT_LEAKAGE.f90', operator_proofs['native_math'])]
    binder = (PACKAGE / 'SPOR64_BOOT_BIND64.f90').read_bytes()
    original = (ROOT / 'src/SPOR64_B2K.f90').read_bytes()
    for record in proofs['system_full_functions']:
        name = record['name'].encode()
        pattern = rb'(?mi)^  logical function ' + name + rb'\([^\n]*\n[\s\S]*?^  end function ' + name + rb'\n'
        new_parts = re.findall(pattern, binder)
        old_parts = re.findall(pattern, original)
        if len(new_parts) != 1 or len(old_parts) != 1 or new_parts != old_parts:
            raise RuntimeError('full original system function not preserved')
        if sha(new_parts[0]) != record['sha256'] or len(new_parts[0]) != record['bytes']:
            raise RuntimeError('full system function SHA/length')
    dependencies = [
        ('axial-material-new-bootstrap-global-projection-v2-compile-only-20261012', 'Root_actual_compile_only_summary.json'),
        ('axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012', 'Root_actual_compile_only_summary.json'),
        ('axial-material-new-global-native64-caller-compile-only-20261012', 'Root_actual_compile_only_summary.json'),
        ('axial-material-new-SPOT-global-native64-dependencies-compile-only-20261011', 'Root_actual_compile_only_summary.json'),
        ('axial-material-new-REAL64-native-route-build-only-20261011', 'Root_actual_build_only_summary.json'),
        ('axial-material-new-ROOT64-BOOT-compile-only-20261011', 'Root_actual_compile_only_summary.json')]
    for directory, filename in dependencies:
        summary_path = ART / directory / filename
        summary = json.loads(summary_path.read_text())
        if summary['failure'] is not None or summary['after_check_error'] is not None:
            raise RuntimeError('actual dependency build did not close')
        if not summary['records'] or any(r['status'] != 'PASS' for r in summary['records']):
            raise RuntimeError('actual dependency build step did not pass')
        declared.extend(summary['output_pins'])
        declared.append(pin(summary_path))
    plan = json.loads((PACKAGE / 'EXACT_CURRENT_SOURCE_COMPILE_ORDER_AND_TRUE_ROUTE.json').read_text())
    relative_sources = plan['new_operator_source_order'] + plan['new_boot_source_order']
    if len(relative_sources) != 7:
        raise RuntimeError('complete seven-source compilation scope')
    sources = [PACKAGE / name for name in relative_sources]
    by_path = {}
    for p in declared:
        p = normalized(p)
        if pin(p['path']) != p:
            raise RuntimeError('complete current fixed Source/dependency EOF SHA/7ID changed')
        if p['path'] in by_path and by_path[p['path']] != p:
            raise RuntimeError('duplicate dependency identity conflict')
        by_path[p['path']] = p
    source_pins = [by_path[str(p)] for p in sources]
    actual_dependency_pins = [p for path, p in by_path.items() if path not in {str(p) for p in sources}]
    includes = [ART / name / 'build' for name in [
        'axial-material-new-bootstrap-global-projection-v2-compile-only-20261012',
        'axial-material-new-bootstrap-QFISS64-v2-compile-only-20261012',
        'axial-material-new-global-native64-caller-compile-only-20261012',
        'axial-material-new-SPOT-global-native64-dependencies-compile-only-20261011',
        'axial-material-new-REAL64-native-route-build-only-20261011',
        'axial-material-new-REAL64-producer-compile-only-20261011',
        'axial-material-new-ROOT64-BOOT-compile-only-20261011',
        'axial-material-r64-system-normalization-20261003']] + [ROOT / 'lib/Darwin_arm64/modules', ROOT / 'Ganlib/lib/Darwin_arm64/modules']
    old = TEMPLATE.read_text()
    new = old
    steps = []
    def replace(label, before, after):
        nonlocal new
        if new.count(before) != 1:
            raise RuntimeError('exact previous-host transformation cardinality: ' + label)
        offset = new.index(before)
        prior = new
        new = new[:offset] + after + new[offset + len(before):]
        steps.append(dict(label=label, byte_offset=len(prior[:offset].encode()), old=before, new=after,
                          before_sha256=sha(prior.encode()), after_sha256=sha(new.encode())))
    replace('scope docstring', 'Five complete global native64 caller compiles against actual v2 publisher; no transport.', 'Seven complete native radial operator and true online BOOT Source compiles; no transport.')
    replace('fresh current compile output', "OUT=ART/'axial-material-new-global-native64-caller-compile-only-20261012'", "OUT=ART/'axial-material-new-true-online-BOOT-operator-seven-compile-only-20261012'")
    replace('frozen seven Source directory', "BOOT=REC/'global_native64_caller_source_v1'", "BOOT=REC/'online_boot_native64_source_v1'")
    replace('current full EOF dependency binding', "MANIFEST=REC/'GLOBAL_NATIVE64_CALLER_NEW_PUBLISHER_DEPENDENCY_BINDING_20261012.json'", "MANIFEST=REC/'TRUE_ONLINE_BOOT_OPERATOR_CURRENT_COMPILE_BINDING_20261012.json'")
    before = next(line for line in new.splitlines(True) if line.startswith('    sources=[BOOT/name'))
    replace('complete seven-source order', before, '    sources=[BOOT/name for name in ' + repr(relative_sources) + ']\n')
    start = new.index('    includes=[')
    end = new.index('    module_files=', start)
    replace('exact actual module include order', new[start:end], '    includes=[' + ',\n              '.join('Path(' + repr(str(p)) + ')' for p in includes) + ']\n')
    before = next(line for line in new.splitlines(True) if line.startswith('    reviewed_new_sources='))
    ast.literal_eval(before.split('=', 1)[1].strip())
    replace('complete independently frozen seven Source SHA', before, '    reviewed_new_sources=' + repr({p['path']: p['sha256'] for p in source_pins}) + '\n')
    replace('exact compile result schema', "schema='ACTUAL_GLOBAL_NATIVE64_CALLER_FIVE_COMPILE_ONLY_V2_DEPENDENCIES'", "schema='ACTUAL_TRUE_ONLINE_BOOT_NATIVE_OPERATOR_SEVEN_COMPILE_ONLY_V1'")
    replace('exact compiled step count', "status='FIVE_GLOBAL_NATIVE64_CALLER_COMPILE_STEPS_CLOSED0_ONLY'", "status='SEVEN_TRUE_ONLINE_BOOT_OPERATOR_COMPILE_STEPS_CLOSED0_ONLY'")
    replace('explicit result scope', 'five unchanged full frozen global native64 caller Sources compiled against the actually compiled new v2 canonical/context/publisher and full global native64 dependencies; no link, global solve, online BOOT or control/physics qualification', 'seven complete frozen native radial operator and true online BOOT Sources compiled against actual frozen v2 canonical/context/Q and original strict CORE/module interfaces; original ROOT library modules are pinned compile dependencies, no whole Source-to-archive claim; no dispatcher link, transport, original17 controls, online BOOT or physics qualification')
    restored = new.encode()
    for step in reversed(steps):
        if sha(restored) != step['after_sha256']:
            raise RuntimeError('complete host inverse after SHA')
        old_bytes, new_bytes = step['old'].encode(), step['new'].encode()
        offset = step['byte_offset']
        if restored[offset:offset + len(new_bytes)] != new_bytes:
            raise RuntimeError('complete host inverse exact bytes')
        restored = restored[:offset] + old_bytes + restored[offset + len(new_bytes):]
        if sha(restored) != step['before_sha256']:
            raise RuntimeError('complete host inverse before SHA')
    if restored != TEMPLATE.read_bytes():
        raise RuntimeError('full previous actual host not restored')
    compile(new, str(HOST), 'exec')
    write(BINDING, dict(scope='Current complete frozen seven Source compile binding, no transport qualification',
                        previous_goal_turn_classification='no_progress: user status report and documentation update only; no business execution',
                        next_safe_action='actual guarded complete seven Source compilation',
                        source_pins=source_pins, actual_dependency_pins=actual_dependency_pins,
                        full_Source_inverse_results=inverse_results,
                        full_original_system_functions=proofs['system_full_functions'],
                        includes=[str(p) for p in includes],
                        guard='previous actually executed whole host inverse, original MRO/guard_admission/caps/whole EOF identities retained',
                        transport_executed=False, online_BOOT_qualified=False, goal_complete=False))
    with HOST.open('x') as f:
        f.write(new)
        f.flush()
        os.fsync(f.fileno())
    write(DERIVATION, dict(template=pin(TEMPLATE), current_host=pin(HOST), current_binding=pin(BINDING),
                           complete_inverse_equals_complete_actual_template_bytes=True,
                           exact_host_transform_steps=steps, full_Source_inverse_results=inverse_results,
                           fixed_Source_and_dependency_count=len(by_path), guard_body_and_MRO_unchanged=True,
                           compiled=False, transport_executed=False, goal_complete=False))
    print(json.dumps(dict(host=pin(HOST), binding=pin(BINDING), source_count=7,
                          full_Source_inverse_steps=[p['steps'] for p in inverse_results],
                          host_inverse_steps=len(steps), compiled=False)))


if __name__ == '__main__':
    main()
