"""Root standard-library Source installation for qualification, no helper import."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import stat
import sys

R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
D = B / 'actual_complete_graph_helper_controls_v23_sources'
E = B / 'actual_complete_graph_helper_controls_v23_receipts'
HELPER = R / 'validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
HELPER_BYTES = 150986
PROTECTED = {
    R / 'validation/axial_material/combined_runtime_complete_input_graph_private_owner_namespace_last_use_20261010.py': 'cf0c2b6b6fd6b1adceec85b261008871f12769832b4dbd4fdb4204f650b4e72c',
    B / 'Root_actual_complete_graph_private_owner_namespace_helper_admission_v22.json': '89d2f03c0af74844731ddf5225307c38ae40521d99ca29c88c5d8db39796b816',
    R / 'validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v22.py': '09e53974005082a14d9675f69258549609a991f86ec231ab6b15edfe20dd265e',
}
ROLES = ('pure_helper_controls.UNREADY.py', 'pure_helper_controls_host.UNREADY.py',
         'fresh_verifier_controls.UNREADY.py', 'fresh_verifier_host.UNREADY.py',
         'inactive_audit_snapshot_controls_SOURCE_ONLY.py')

def require(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)

def identity(path):
    s = Path(path).lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def full_pin(path, expected_sha=None):
    path = Path(path)
    require(path.is_absolute() and os.path.normpath(str(path)) == str(path), 'absolute normalized Source path')
    before = identity(path)
    require(stat.S_ISREG(before[2]) and before[3] == 1, 'regular one-link Source file')
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    require(identity(path) == before and len(raw) == before[4], 'complete EOF Source changed')
    require(expected_sha is None or sha == expected_sha, 'full Source SHA differs')
    return dict(path=str(path), sha256=sha, size_bytes=len(raw), identity=before)

def pin3(pin):
    return {k: pin[k] for k in ('path', 'sha256', 'identity')}

def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, 'duplicate META key')
        result[k] = v
    return result

def reject_nonfinite(value):
    raise ValueError('nonfinite META ' + value)

def read(path, sha=None):
    pin = full_pin(path, sha)
    value = json.loads(Path(path).read_bytes(), object_pairs_hook=unique_pairs, parse_constant=reject_nonfinite)
    require(full_pin(path, sha) == pin, 'META changed during decode')
    return value, pin

def package(manifest_path, sha):
    manifest_path = Path(manifest_path)
    root = manifest_path.parent
    value, mpin = read(manifest_path, sha)
    members = value['members']
    require(type(members) is list and len(members) == value['member_count'], 'whole package member count')
    expected = {}
    for item in members:
        rel = Path(item.get('relative_path', Path(item['path']).relative_to(root)))
        require(not rel.is_absolute() and '..' not in rel.parts and str(rel) != manifest_path.name,
                'normalized complete Source member')
        require(rel.as_posix() not in expected and str(root / rel) == item['path'], 'unique original member path')
        pin = full_pin(root / rel, item['sha256'])
        require(pin == {k: item[k] for k in pin}, 'exact complete member SHA/7ID')
        expected[rel.as_posix()] = pin
    actual_paths = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p != manifest_path}
    require(actual_paths == set(expected) and not any(p.is_symlink() for p in root.rglob('*')), 'whole Source inventory, no aliases')
    directories = {p.relative_to(root).as_posix(): identity(p) for p in root.rglob('*') if p.is_dir()}
    declared = value.get('directories', value.get('subdirectories'))
    if isinstance(declared, list):
        declared = {x.get('relative_path', Path(x['path']).relative_to(root).as_posix())
                    if 'path' in x else x['relative_path']: x['identity'] for x in declared}
    require(declared is None or directories == declared, 'all Source subdirectories exact')
    require('package_root_identity' not in value or identity(root) == value['package_root_identity'], 'Source root exact')
    return dict(root=str(root), manifest=mpin, members=expected, directories=directories, root_identity=identity(root))

def closed_receipt(path, sha):
    value, pin = read(path, sha)
    require(value.get('closed') is True, 'actual closed Source seal receipt')
    tool = next((value[k] for k in ('terminal_tool_return', 'exec_command_result', 'actual_tool_return')
                 if isinstance(value.get(k), dict)), None)
    require(type(tool) is dict and type(tool.get('exit_code')) is int and tool['exit_code'] == 0
            and tool.get('session_id') is None, 'real int0 Source seal with no live session')
    return pin

def copy_package(view, destination, seal=None):
    require(not os.path.lexists(destination), 'fresh complete package destination')
    shutil.copytree(view['root'], destination)
    copied = {}
    for rel, original in view['members'].items():
        target = full_pin(destination / rel, original['sha256'])
        require(target['size_bytes'] == original['size_bytes'], 'complete copied Source bytes')
        copied[rel] = target
    manifest = full_pin(destination / 'MANIFEST.json', view['manifest']['sha256'])
    if seal is not None:
        shutil.copyfile(seal['path'], destination / '_actual_Source_seal_tool_return.json')
        copied['_actual_Source_seal_tool_return.json'] = full_pin(destination / '_actual_Source_seal_tool_return.json', seal['sha256'])
    return dict(original_source_package=view, copied_manifest=manifest, copied_members=copied,
                copied_directories={p.relative_to(destination).as_posix(): identity(p) for p in destination.rglob('*') if p.is_dir()},
                copied_root_identity=identity(destination))

def write_new(path, value):
    require(not os.path.lexists(path), 'fresh actual Source record')
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n')

def main():
    require(sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 8, 'seven Source arguments with -B')
    qroot, qsha, proot, psha, report_sha, seal_path, seal_sha = sys.argv[1:]
    qroot = Path(qroot); proot = Path(proot)
    qview = package(qroot / 'MANIFEST.json', qsha)
    pview = package(proot / 'MANIFEST.json', psha)
    qseal_path = qroot.parent / (qroot.name + '_seal_receipt') / 'ACTUAL_EXACT_INTEGER_SOURCE_SEAL_TOOL_RETURN.json'
    qseal = closed_receipt(qseal_path, 'e97cc21a44dfea9bfdf6af8eab15b0fbb5585fc2fa712e43fd0c0c581f5e2afc')
    pseal = closed_receipt(Path(seal_path), seal_sha)
    peer, peer_pin = read(proot / 'REVIEW.json', report_sha)
    require(peer['schema'] == 'INDEPENDENT_PRIVATE_INACTIVE_AUDIT_COMPLETE_QUALIFICATION_SOURCE_REVIEW_V1'
            and peer['status'] == 'SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'
            and peer['source_only'] is True and peer['all_checks_typed_true'] is True and peer['blockers'] == []
            and type(peer['check_count']) is int and peer['check_count'] > 0
            and len(peer['checks']) == peer['check_count']
            and all(type(c['passed']) is bool and c['passed'] is True for c in peer['checks']), 'complete actual Source peer PASS')
    require(peer['qualified_template_manifest_pin'] == qview['manifest']
            and peer['qualified_helper_candidate_SHA'] == HELPER_SHA
            and peer['qualified_template_Source_pins'] == {name: full_pin(qroot / name) for name in ROLES},
            'Source peer exact complete five roles/helper/manifest')
    hroot = Path('/private/tmp/axmat_complete_helper_inactive_audit_snapshot_SOURCE_candidate_yiyxo77u')
    hview = package(hroot / 'MANIFEST.json', '13aa3f853077199546b292bc6f0b00d74069e3001f44bb919443760d8076e918')
    oldpeerroot = Path('/private/tmp/axmat_INDEPENDENT_complete_inactive_audit_helper_SOURCE_review_20261010_66a52zbh')
    oldpeer = package(oldpeerroot / 'MANIFEST.json', '096044f6febf626e0ab94f4abf672f0f60bf09edcbce22dfe6cb4ecd8da12f11')
    oldreview, oldreview_pin = read(oldpeerroot / 'REVIEW.json', '4b6155f567de5bd8b1aa861d4ff5cf65193b17c6f7c31352c782a0426353edf9')
    require(oldreview['check_count'] == 479 and len(oldreview['checks']) == 479
            and all(type(c['passed']) is bool and c['passed'] is True for c in oldreview['checks']), 'whole 479-check helper Source peer')
    source = hroot / 'combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume.UNREADY.py'
    candidate = full_pin(source, HELPER_SHA)
    require(candidate['size_bytes'] == HELPER_BYTES, 'complete reviewed helper bytes')
    before = [full_pin(p, sha) for p, sha in PROTECTED.items()]
    for p in (D, E, HELPER):
        require(not os.path.lexists(p), 'fresh planned actual Source namespace')
    D.mkdir(mode=0o700); E.mkdir(mode=0o700)
    packages = {
        'complete_helper_candidate': copy_package(hview, D / 'sealed_complete_helper_candidate_SOURCE'),
        'complete_helper_Source_peer': copy_package(oldpeer, D / 'sealed_independent_complete_helper_SOURCE_review'),
        'complete_qualification_template': copy_package(qview, D / 'sealed_complete_qualification_template_SOURCE', qseal),
        'complete_qualification_Source_peer': copy_package(pview, D / 'sealed_independent_complete_qualification_SOURCE_review', pseal),
    }
    shutil.copyfile(source, HELPER)
    installed = full_pin(HELPER, HELPER_SHA)
    shutil.copyfile(__file__, D / Path(__file__).name)
    require([full_pin(p, sha) for p, sha in PROTECTED.items()] == before, 'original helper/Q/canonical unchanged')
    for v in (qview, pview, hview, oldpeer):
        require(package(v['manifest']['path'], v['manifest']['sha256']) == v, 'all original complete Source packages unchanged')
    record = dict(schema='ROOT_V23_COMPLETE_HELPER_SOURCE_INSTALL_RECORD_V1', source_only=True,
                  installed_helper=pin3(installed), source_packages=packages,
                  source_file_count=sum(p.is_file() for p in D.rglob('*')),
                  installed_helper_source_file_count=1, Source_installer=full_pin(Path(__file__).resolve()),
                  actual_independent_template_Source_peer=peer_pin, actual_independent_helper_Source_peer=oldreview_pin,
                  actual_pure_helper_protocol_qualified=False, actual_full_current_graph_verifier_qualified=False,
                  actual_new_helper_qualification_sha256=None, actual_complete_build_qualified=False,
                  whole_INPUT_admitted=False, native_RSS_qualified=False, AAA_accuracy_qualified=False, ABA_admitted=False,
                  business_or_guard_or_helper_API_executed=False,
                  old_helper_Q_canonical_fullEOF_unchanged=before)
    rp = E / 'Root_actual_complete_helper_SOURCE_install_record.json'
    write_new(rp, record)
    print(json.dumps(dict(status='ACTUAL_COMPLETE_SOURCE_ONLY_HELPER_INSTALLED_FOR_QUALIFICATION_NOT_EXECUTED',
          installed_helper=pin3(installed), source_install_record=pin3(full_pin(rp)),
          source_file_count=record['source_file_count'], source_only=True), separators=(',', ':')))

if __name__ == '__main__':
    main()
