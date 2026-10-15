"""Root-only future standard-library SOURCE binding; never run controllers.

argv: actual_install_witness witness_SHA template_manifest_SHA
      independent_SOURCE_report report_SHA fresh_TMP_output
No installed Source, terminal, qualification or business pin is invented.
"""
from pathlib import Path
import ast
import hashlib
import json
import os
import shutil
import stat
import sys

HERE = Path(__file__).resolve().parent
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
HELPER_BYTES = 150986
PROTECTED_PARENT_SHA = {
    '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py':
        'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c',
    '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json':
        '89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816',
    '/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py':
        '09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e',
}
READY = 'READY_SOURCE_BOUND_BY_ROOT'
MODULE = 'inactive_audit_snapshot_controls_SOURCE_ONLY.py'
TEMPLATES = ('pure_helper_controls.UNREADY.py', 'pure_helper_controls_host.UNREADY.py',
             'fresh_verifier_controls.UNREADY.py', 'fresh_verifier_host.UNREADY.py')
PEER_SCHEMA = 'INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1'
PEER_STATUS = 'SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'

def require(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)

def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate metadata key')
        result[key] = value
    return result

def reject_nonfinite(value):
    raise ValueError('nonfinite metadata constant ' + value)

def identity(path):
    value = Path(path).lstat()
    return [value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns]

def full_pin(path, sha=None):
    path = Path(path)
    require(path.is_absolute() and os.path.normpath(str(path)) == str(path), 'absolute normalized Source path')
    before = identity(path)
    require(stat.S_ISREG(before[2]) and before[3] == 1, 'one regular non-symlink Source/META file')
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    require(before == identity(path) and len(raw) == before[4], 'fresh full EOF/7ID changed')
    require(sha is None or type(sha) is str and len(sha) == 64 and actual == sha, 'actual SHA differs')
    return dict(path=str(path), sha256=actual, size_bytes=len(raw), identity=before)

def read(path, sha=None):
    pin = full_pin(path, sha)
    value = json.loads(Path(path).read_bytes(), object_pairs_hook=unique_pairs,
                       parse_constant=reject_nonfinite)
    require(full_pin(path, sha) == pin, 'META changed after strict full decode')
    return value, pin

def pin3(pin):
    require(type(pin) is dict and set(pin) in ({'path', 'sha256', 'identity'},
            {'path', 'sha256', 'size_bytes', 'identity'}), 'complete 3/4-field pin')
    require(type(pin['path']) is str and type(pin['sha256']) is str
            and len(pin['sha256']) == 64 and all(c in '0123456789abcdef' for c in pin['sha256'])
            and type(pin['identity']) is list and len(pin['identity']) == 7
            and all(type(item) is int for item in pin['identity']), 'exact integer pin shape')
    if 'size_bytes' in pin:
        require(type(pin['size_bytes']) is int and pin['size_bytes'] == pin['identity'][4], 'pin bytes exact')
    actual = full_pin(pin['path'], pin['sha256'])
    require(actual['identity'] == pin['identity'], 'actual current pin identity differs')
    return {key: actual[key] for key in ('path', 'sha256', 'identity')}, actual

def segment(source, node):
    return ''.join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])

def bind_globals(source, bindings):
    original = source
    hunks = []
    for key, value in bindings.items():
        tree = ast.parse(source)
        nodes = [node for node in tree.body if isinstance(node, ast.Assign)
                 and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                 and node.targets[0].id == key]
        require(len(nodes) == 1, 'unique Source binding global ' + key)
        old = segment(source, nodes[0])
        new = key + ' = ' + repr(value) + '\n'
        require(source.count(old) == 1, 'unique complete Source binding span')
        source = source.replace(old, new, 1)
        hunks.append(dict(global_name=key, old_utf8=old, new_utf8=new))
    restored = source
    for hunk in reversed(hunks):
        require(restored.count(hunk['new_utf8']) == 1, 'unique inverse Source span')
        restored = restored.replace(hunk['new_utf8'], hunk['old_utf8'], 1)
    require(restored == original and ast.dump(ast.parse(restored), include_attributes=False)
            == ast.dump(ast.parse(original), include_attributes=False), 'full template bytes/AST inverse')
    old_defs = [node for node in ast.parse(original).body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    new_defs = [node for node in ast.parse(source).body if isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    require([node.name for node in old_defs] == [node.name for node in new_defs], 'all definition names/order retained')
    require(all(segment(original, a) == segment(source, b)
                and ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)
                for a, b in zip(old_defs, new_defs)), 'all bound definition bytes/AST retained')
    return source, hunks

def validate_manifest(expected_sha):
    manifest, manifest_pin = read(HERE / 'MANIFEST.json', expected_sha)
    require(manifest['schema'] == 'COMPLETE_PRIVATE_INACTIVE_AUDIT_PURE_FRESH_SOURCE_PACKAGE_V1'
            and manifest['source_only'] is True and manifest['new_actual_helper_qualification'] is None
            and manifest['six_future_business_pins'] == [None] * 6, 'fixed UNREADY full Source manifest')
    members = manifest['members']
    require(type(members) is list and type(manifest['member_count']) is int
            and len(members) == manifest['member_count'], 'complete manifest count')
    expected = {Path(member['path']).relative_to(HERE).as_posix(): member for member in members}
    require(len(expected) == len(members), 'no duplicate Source member')
    actual = {path.relative_to(HERE).as_posix(): full_pin(path)
              for path in HERE.rglob('*') if path.is_file() and path != HERE / 'MANIFEST.json'}
    require(actual == expected, 'whole Source namespace EOF/SHA7ID mismatch')
    actual_directories = {path.relative_to(HERE).as_posix(): identity(path)
                          for path in HERE.rglob('*') if path.is_dir()}
    require(actual_directories == manifest['directories'], 'whole Source directories changed')
    require(identity(HERE) == manifest['package_root_identity'], 'whole Source root directory changed')
    require(not any(path.is_symlink() for path in HERE.rglob('*')), 'Source package aliases forbidden')
    return manifest, manifest_pin, actual, actual_directories

def write_new(path, value):
    require(not path.exists(), 'fresh Source metadata output')
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')

def main():
    require(len(sys.argv) == 7 and sys.dont_write_bytecode and not sys.flags.optimize,
            'six explicit actual META/Source arguments with -B')
    witness_path, witness_sha, manifest_sha, peer_path, peer_sha, out_path = sys.argv[1:]
    manifest, manifest_pin, original_members, original_directories = validate_manifest(manifest_sha)
    plan, plan_pin = read(HERE / 'ROOT_FIXED_SOURCE_NAMESPACES_AND_FUTURE_ACTUAL_PINS.UNREADY.json')
    peer, peer_pin = read(peer_path, peer_sha)
    require(peer['schema'] == PEER_SCHEMA and peer['status'] == PEER_STATUS and peer['source_only'] is True
            and peer['all_checks_typed_true'] is True and peer['blockers'] == []
            and type(peer['check_count']) is int and peer['check_count'] > 0
            and len(peer['checks']) == peer['check_count']
            and all(type(check['passed']) is bool and check['passed'] is True for check in peer['checks']),
            'actual complete independent Source-only peer report')
    require(peer['qualified_template_manifest_pin'] == manifest_pin
            and peer['qualified_helper_candidate_SHA'] == HELPER_SHA,
            'independent peer exact manifest/helper Source coupling')
    role_pins = {name: full_pin(HERE / name) for name in TEMPLATES + (MODULE,)}
    require(peer['qualified_template_Source_pins'] == role_pins, 'whole five reviewed Source role pins')
    witness, witness_pin = read(witness_path, witness_sha)
    require(witness['schema'] == 'ROOT_V23_ACTUAL_COMPLETE_HELPER_SOURCE_INSTALL_TOOL_RETURN_V1'
            and witness['source_only'] is True and witness['closed'] is True
            and witness['actual_tool_terminal_return_observed'] is True,
            'actual Root observed CLOSED Source install receipt')
    terminal = witness['terminal_tool_return']
    require(type(terminal) is dict and type(terminal['exit_code']) is int and terminal['exit_code'] == 0
            and ('session_id' not in terminal or terminal['session_id'] is None) and type(terminal['chunk_id']) is str
            and type(terminal['output']) is str, 'real integer0 terminal with no live session')
    observed = json.loads(terminal['output'], object_pairs_hook=unique_pairs, parse_constant=reject_nonfinite)
    require(observed['installed_helper'] == witness['installed_helper']
            and observed['source_install_record'] == witness['source_install_record'],
            'actual original terminal stdout exact install pins, no Javascript integer loss')
    helper, helper_full = pin3(witness['installed_helper'])
    record_ref, record_pin = pin3(witness['source_install_record'])
    require(helper['path'] == plan['namespaces']['planned_installed_helper']
            and helper['sha256'] == HELPER_SHA and helper_full['size_bytes'] == HELPER_BYTES,
            'exact reviewed new Source actually installed in planned helper namespace')
    record, record_current = read(record_pin['path'], record_pin['sha256'])
    require(record_current == record_pin and record['schema'] == 'ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1'
            and record['source_only'] is True and record['installed_helper'] == helper
            and record['business_or_guard_or_helper_API_executed'] is False,
            'actual complete Source-only install record')
    common_false = ('actual_pure_helper_protocol_qualified', 'actual_full_current_graph_verifier_qualified',
                    'whole_INPUT_admitted', 'native_RSS_qualified', 'AAA_accuracy_qualified', 'ABA_admitted')
    require(all(witness[key] is False and record[key] is False for key in common_false)
            and witness['complete_build_qualified'] is False and record['actual_complete_build_qualified'] is False
            and witness['actual_new_helper_qualification_sha256'] is None
            and record['actual_new_helper_qualification_sha256'] is None,
            'installed Source is not new qualification/build/INPUT/science')
    protected = record['old_helper_Q_canonical_fullEOF_unchanged']
    require(type(protected) is list and len(protected) == len(PROTECTED_PARENT_SHA)
            and {item['path']: item['sha256'] for item in protected} == PROTECTED_PARENT_SHA,
            'complete original helper/Q/canonical protected Source pins')
    protected_before = [pin3(item)[1] for item in protected]
    out = Path(out_path)
    require(out.is_absolute() and out.is_relative_to(Path('/private/tmp')) and not os.path.lexists(out),
            'fresh TMP SOURCE output only, never canonical or ART')
    out.mkdir(mode=0o700)
    shutil.copytree(HERE, out / 'COMPLETE_QUALIFICATION_TEMPLATE_SOURCE')
    shutil.copyfile(HERE / MODULE, out / MODULE)
    shutil.copyfile(witness_path, out / 'ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_WITNESS.json')
    shutil.copyfile(record_pin['path'], out / 'ORIGINAL_ROOT_ACTUAL_SOURCE_INSTALL_RECORD.json')
    shutil.copyfile(peer_path, out / 'ORIGINAL_INDEPENDENT_COMPLETE_SOURCE_REVIEW.json')
    proof = {}
    for kind, driver_name, host_name in [('pure', TEMPLATES[0], TEMPLATES[1]), ('fresh', TEMPLATES[2], TEMPLATES[3])]:
        namespace = plan['namespaces'][kind]
        module_path = str(Path(namespace['source']) / MODULE)
        original = (HERE / driver_name).read_text()
        bindings = dict(SOURCE_STATUS=READY, AUDIT_CONTROL_PATH=module_path)
        if kind == 'pure':
            bindings['HELPER_PATH'] = helper['path']
        else:
            bindings.update(NEW_HELPER_PATH=helper['path'], NEW_HELPER_IDENTITY=helper['identity'])
        source, hunks = bind_globals(original, bindings)
        driver = out / driver_name.replace('.UNREADY', '')
        driver.write_text(source)
        driver_pin = full_pin(driver)
        proof[driver.name] = dict(template_pin=role_pins[driver_name], bound_pin=driver_pin, full_hunks=hunks,
                                 all_definitions_bytes_AST_unchanged=True, full_template_bytes_AST_inverse=True)
        original = (HERE / host_name).read_text()
        source, hunks = bind_globals(original, dict(SOURCE_STATUS=READY, BOUND_HELPER_PIN=helper,
                INSTALL_WITNESS_PIN={key: witness_pin[key] for key in ('path', 'sha256', 'identity')},
                SOURCE_INSTALL_RECORD_PIN=record_ref, AUDIT_CONTROL_PATH=module_path, TARGET_SHA=driver_pin['sha256']))
        host = out / host_name.replace('.UNREADY', '')
        host.write_text(source)
        proof[host.name] = dict(template_pin=role_pins[host_name], bound_pin=full_pin(host), full_hunks=hunks,
                               all_definitions_bytes_AST_unchanged=True, full_template_bytes_AST_inverse=True)
    write_new(out / 'ALL_FOUR_ACTUAL_SOURCE_BINDING_INVERSES.json', dict(
        schema='ROOT_V23_ACTUAL_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_BINDING_INVERSES_V1',
        source_only=True, actual_installed_helper=helper_full, actual_Root_install_witness=witness_pin,
        actual_Source_install_record=record_pin, actual_independent_Source_peer=peer_pin,
        complete_template_manifest=manifest_pin, complete_control_module_Source=role_pins[MODULE],
        all_four_full_Source_bindings=proof, all_parent_fixture_protocol_guard_resource_Source_preserved=True,
        new_actual_helper_qualification=None, six_future_business_pins=[None] * 6))
    require(validate_manifest(manifest_sha)[2:] == (original_members, original_directories), 'whole template Source changed')
    require(full_pin(witness_path, witness_sha) == witness_pin and full_pin(peer_path, peer_sha) == peer_pin
            and full_pin(helper['path'], helper['sha256']) == helper_full
            and full_pin(record_pin['path'], record_pin['sha256']) == record_pin,
            'all actual Source/META pins changed during binding')
    require([full_pin(item['path'], item['sha256']) for item in protected_before] == protected_before,
            'original helper/Q/canonical changed during Source binding')
    namespace = [full_pin(path) for path in sorted(out.rglob('*')) if path.is_file()]
    write_new(out / 'ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json', dict(
        schema='ROOT_V23_ACTUAL_SOURCE_ONLY_FULL_QUALIFICATION_BOUND_NAMESPACE_V1', source_only=True,
        members=namespace, member_count=len(namespace), new_actual_helper_qualification=None,
        six_future_business_pins=[None] * 6, controller_helper_guard_API_or_business_executed=False))
    print(json.dumps(dict(status='ACTUAL_SOURCE_ONLY_BOUND_ALL_FOUR_FULL_CONTROLLERS_NOT_EXECUTED',
          source_only=True, output=str(out), bindings=proof,
          complete_bound_manifest=full_pin(out / 'ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json'),
          new_actual_helper_qualification=None, six_future_business_pins=[None] * 6), separators=(',', ':')))

if __name__ == '__main__':
    main()
