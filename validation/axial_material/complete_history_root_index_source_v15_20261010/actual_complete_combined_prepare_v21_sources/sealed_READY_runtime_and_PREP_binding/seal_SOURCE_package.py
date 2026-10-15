"""Seal only this fixed TMP SOURCE package; do not import or execute its candidates."""
import hashlib
import json
import os
import stat
from pathlib import Path

BASE = Path('/private/tmp/axmat_v21_actual_joint_Q_READY_runtime_PREP_SOURCE_binding_20261010_m2r8v')
MANIFEST = BASE / 'sealed_SOURCE_manifest.json'


def identity(st):
    return [st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size,
            st.st_mtime_ns, st.st_ctime_ns]


def pin(path):
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise ValueError('Only ordinary single-link SOURCE files may be sealed')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        if identity(before) != identity(opened):
            raise ValueError('SOURCE identity changed before complete reading')
        digest = hashlib.sha256()
        size = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
        after_open = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after = path.lstat()
    if identity(before) != identity(after_open) or identity(before) != identity(after):
        raise ValueError('SOURCE identity changed during complete reading')
    if size != before.st_size:
        raise ValueError('SOURCE complete EOF byte count mismatch')
    return {'path': str(path), 'sha256': digest.hexdigest(),
            'size_bytes': size, 'identity': identity(before)}


def inventory():
    files = []
    directories = []
    for directory, subdirs, names in os.walk(BASE, followlinks=False):
        directory = Path(directory)
        st = directory.lstat()
        if not stat.S_ISDIR(st.st_mode):
            raise ValueError('Unexpected non-directory in SOURCE package')
        directories.append(str(directory.relative_to(BASE)))
        for name in subdirs:
            if not stat.S_ISDIR((directory / name).lstat().st_mode):
                raise ValueError('No SOURCE symlink directories are permitted')
        for name in names:
            path = directory / name
            if path != MANIFEST:
                files.append(path)
    return sorted(files), sorted(directories)


def main():
    if MANIFEST.exists():
        raise ValueError('The SOURCE manifest must not already exist')
    if BASE.resolve() != BASE or BASE.parent != Path('/private/tmp'):
        raise ValueError('Only this fixed fresh TMP package may be sealed')
    review = json.loads((BASE / 'SELF_REVIEW.json').read_bytes())
    if review['all_checks_typed_true'] is not True or review['blockers'] != []:
        raise ValueError('SOURCE self-review did not pass')
    if review['installed'] is not False or review['helper_API_guard_business_executed'] is not False:
        raise ValueError('SOURCE self-review scope is not metadata-only')
    inner_path = BASE / 'BOUND_READY_SOURCE/generated_SOURCE_manifest.json'
    inner = json.loads(inner_path.read_bytes())
    files_before, directories_before = inventory()
    before = {str(path.relative_to(BASE)): pin(path) for path in files_before}
    inner_members = {item['relative']: {key: value for key, value in item.items()
                                       if key != 'relative'} for item in inner['members']}
    if len(inner_members) != len(inner['members']) or len(inner_members) != inner['member_count']:
        raise ValueError('Generated SOURCE manifest member sequence is not complete and unique')
    for relative, expected in inner_members.items():
        current = before['BOUND_READY_SOURCE/' + relative]
        if current != expected:
            raise ValueError('Fixed generated SOURCE member changed before outer sealing')
    expected_inner = {'BOUND_READY_SOURCE/' + relative for relative in inner_members}
    expected_inner.add('BOUND_READY_SOURCE/generated_SOURCE_manifest.json')
    actual_inner = {relative for relative in before if relative.startswith('BOUND_READY_SOURCE/')}
    if actual_inner != expected_inner:
        raise ValueError('Fixed generated SOURCE full member inventory differs')
    fixed = {
        'BOUND_READY_SOURCE/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py':
            '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5',
        'BOUND_READY_SOURCE/combined_prepare_host.py':
            '776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405',
        'BOUND_READY_SOURCE/generated_SOURCE_manifest.json':
            '45124504c1a259a2b863245211dd3202060998fc5ec07dc1d6221ad353834ed2',
        'SELF_REVIEW.json':
            '141ba02c8c83163b1f9a5177980d0107b4239faa3e7e0270bd346c6e4b102998',
    }
    if any(before[relative]['sha256'] != sha for relative, sha in fixed.items()):
        raise ValueError('Fixed candidate, self-review or inner manifest differs')
    files_after, directories_after = inventory()
    after = {str(path.relative_to(BASE)): pin(path) for path in files_after}
    if before != after or directories_before != directories_after:
        raise ValueError('Full SOURCE EOF SHA7ID or namespace changed before sealing')
    document = {
        'schema': 'AXMAT_V21_ACTUAL_JOINT_Q_READY_RUNTIME_PREP_FULL_SOURCE_SEAL_V1',
        'status': 'SEALED_SOURCE_READY_UNINSTALLED_NO_BUSINESS_QUALIFICATION',
        'package_path': str(BASE),
        'member_count_excluding_this_manifest': len(before),
        'member_bytes_excluding_this_manifest': sum(item['size_bytes'] for item in before.values()),
        'full_member_inventory': before,
        'complete_directory_relative_paths': directories_before,
        'full_EOF_SHA256_exact7ID_before_after_unchanged': True,
        'all_generated_inner_SOURCE_members_retained_exact': True,
        'complete_canonical_4hunk_inverse_and_70_definition_bytes_preserved': True,
        'complete_genuine_PREP_host_11hunk_inverse_and_original_caps_preserved': True,
        'metadata_SOURCE_binding_actual_terminal_chunk': '3594d1',
        'metadata_SOURCE_binding_typed_integer_exit_code': 0,
        'SOURCE_self_review_actual_terminal_chunk': '61a062',
        'SOURCE_self_review_typed_integer_exit_code': 0,
        'SOURCE_self_review_checks': len(review['checks']),
        'initial_SOURCE_condition_failure_preserved_and_corrected_without_business_execution': True,
        'future_business_six_pins_all_None': True,
        'helper_qualification_scope': 'Original full metadata protocol and complete current graph metadata verifier only',
        'ART_graph_numeric_payload_read': False,
        'helper_API_guard_business_executed': False,
        'canonical_or_frozen_namespace_written': False,
        'installed': False,
        'future_actual_PREP_build_INPUT_native_AAA_ABA_success_claimed': False,
    }
    with MANIFEST.open('x', encoding='utf-8') as stream:
        json.dump(document, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
    manifest_pin = pin(MANIFEST)
    final_files, final_directories = inventory()
    final = {str(path.relative_to(BASE)): pin(path) for path in final_files}
    if before != final or directories_before != final_directories:
        raise ValueError('Full sealed SOURCE member inventory changed after manifest creation')
    if pin(MANIFEST) != manifest_pin:
        raise ValueError('SOURCE seal changed during final complete reading')
    print(json.dumps({'status': document['status'], 'manifest': manifest_pin,
                      'members': len(before), 'member_bytes': document['member_bytes_excluding_this_manifest'],
                      'source_self_review_checks': document['SOURCE_self_review_checks'],
                      'all_full_EOF_SHA7ID_before_after_exact': True,
                      'API_guard_business_executed': False, 'installed': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
