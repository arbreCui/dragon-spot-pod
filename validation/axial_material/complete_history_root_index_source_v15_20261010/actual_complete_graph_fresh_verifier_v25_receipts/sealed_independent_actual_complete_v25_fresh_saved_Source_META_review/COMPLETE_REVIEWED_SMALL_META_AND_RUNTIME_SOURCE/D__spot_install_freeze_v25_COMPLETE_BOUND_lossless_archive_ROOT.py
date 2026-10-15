"""Standard-library complete Source copy/freeze; controllers are not executed."""
from pathlib import Path
import importlib.util
import json
import gzip
import tarfile
import hashlib
import os
import shutil
import sys

INSTALLER = Path('/private/tmp/spot_install_v23_complete_helper_SOURCE_ROOT.py')
INSTALLER_SHA = 'c37bd0e2d6aebcb59bd31689824ef48f7532031d574d825b50719c18b43a6f5f'
R = Path('/Users/wen/spot')
B = R / 'validation/axial_material/complete_history_root_index_source_v15_20261010'
ART = R / 'validation/artifacts'
KINDS = {
    'pure': ('actual_complete_graph_helper_controls_v25_sources', 'actual_complete_graph_helper_controls_v25_receipts',
             'axial-material-complete-graph-inactive-audit-helper-controls-host-v25-20261010',
             'axial-material-complete-graph-inactive-audit-helper-controls-v25-20261010'),
    'fresh': ('actual_complete_graph_fresh_verifier_v25_sources', 'actual_complete_graph_fresh_verifier_v25_receipts',
              'axial-material-complete-graph-inactive-audit-fresh-verifier-host-v25-20261010',
              'axial-material-complete-graph-inactive-audit-fresh-verifier-v25-20261010'),
}

def archive_complete_source(original, destination, m):
    """Save every original member and manifest; verify all decompressed bytes."""
    root = Path(original['root'])
    expected_files = dict(original['members'])
    manifest_name = Path(original['manifest']['path']).relative_to(root).as_posix()
    m.require(manifest_name not in expected_files, 'original manifest distinct from all members')
    expected_files[manifest_name] = original['manifest']
    expected_dirs = {'.', *original['directories']}
    m.require(not os.path.lexists(destination), 'fresh lossless complete Source archive')
    with destination.open('xb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w', format=tarfile.PAX_FORMAT) as archive:
                archive.add(root, arcname='.', recursive=False)
                for item in sorted(root.rglob('*')):
                    m.require(not item.is_symlink(), 'complete Source archive aliases forbidden')
                    relative = item.relative_to(root).as_posix()
                    m.require(relative in expected_files or relative in expected_dirs,
                              'every archived Source entry is from complete original inventory')
                    archive.add(item, arcname=relative, recursive=False)
    actual_files = {}; actual_dirs = set()
    with destination.open('rb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='rb') as zipped:
            with tarfile.open(fileobj=zipped, mode='r|') as archive:
                for entry in archive:
                    name = entry.name
                    m.require(name == '.' or not Path(name).is_absolute() and '..' not in Path(name).parts,
                              'exact relative archive member path')
                    if entry.isdir():
                        m.require(name in expected_dirs and name not in actual_dirs,
                                  'all Source directories exactly once')
                        actual_dirs.add(name)
                    else:
                        m.require(entry.isfile() and name in expected_files and name not in actual_files,
                                  'all complete regular Source members exactly once, no links')
                        handle = archive.extractfile(entry)
                        m.require(handle is not None, 'complete archived Source file readable')
                        digest = hashlib.sha256(); count = 0
                        with handle:
                            while True:
                                chunk = handle.read(1024*1024)
                                if not chunk: break
                                digest.update(chunk); count += len(chunk)
                        pin = expected_files[name]
                        m.require(count == entry.size == pin['size_bytes'] and digest.hexdigest() == pin['sha256'],
                                  'full decompressed Source EOF/byte count/SHA equals original')
                        actual_files[name] = dict(size_bytes=count, sha256=digest.hexdigest())
            # Consume the complete gzip stream and trailer, including ordinary tar padding.
            while zipped.read(1024*1024): pass
    m.require(set(actual_files) == set(expected_files) and actual_dirs == expected_dirs,
              'no missing or extra Source members, manifest or directories')
    m.require(m.package(original['manifest']['path'], original['manifest']['sha256']) == original,
              'whole original Source unchanged during lossless archive creation/readback')
    return dict(original_complete_package=original, compressed_archive=m.full_pin(destination),
                compression='lossless_tar_gzip_complete_members_manifest_and_directories',
                full_decompressed_members=actual_files, full_decompressed_directories=sorted(actual_dirs),
                complete_file_count_including_manifest=len(actual_files),
                complete_directory_count_including_root=len(actual_dirs),
                all_member_bytes_and_SHA_verified_after_decompression=True,
                no_original_member_omission=True, runtime_Source_entrypoints_are_separate_original_bytes=True)


def main():
    import hashlib
    assert sys.dont_write_bytecode and not sys.flags.optimize and len(sys.argv) == 8
    assert hashlib.sha256(INSTALLER.read_bytes()).hexdigest() == INSTALLER_SHA
    spec = importlib.util.spec_from_file_location('Root_complete_Source_inventory_copy_support_only', INSTALLER)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    broot, bsha, proot, psha, rsha, seal_path, seal_sha = sys.argv[1:]
    broot = Path(broot); proot = Path(proot)
    bv = m.package(broot / 'ROOT_FULL_GENERATED_QUALIFICATION_SOURCE_MANIFEST.json', bsha)
    pv = m.package(proot / 'MANIFEST.json', psha)
    seal = m.closed_receipt(seal_path, seal_sha)
    report, report_pin = m.read(proot / 'REVIEW.json', rsha)
    m.require(report['schema'] == 'INDEPENDENT_V25_ACTUAL_COMPLETE_BOUND_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_REVIEW_V1'
              and report['status'] == 'SOURCE_ONLY_PASS_NO_EXECUTION_OR_QUALIFICATION'
              and report['source_only'] is True and report['all_checks_typed_true'] is True and report['blockers'] == []
              and report['bound_manifest_pin'] == bv['manifest'] and type(report['check_count']) is int
              and report['check_count'] > 0 and len(report['checks']) == report['check_count']
              and all(type(c['passed']) is bool and c['passed'] is True for c in report['checks']), 'actual complete bound Source peer')
    protected = [m.full_pin(p, sha) for p, sha in m.PROTECTED.items()]
    helper = m.full_pin(m.HELPER, m.HELPER_SHA)
    frozen = {}
    for kind, (dname, ename, hname, oname) in KINDS.items():
        d = B / dname; e = B / ename
        m.require(not os.path.lexists(ART / hname) and not os.path.lexists(ART / oname), 'fresh genuine host/output')
        m.require(not os.path.lexists(d) and not os.path.lexists(e), 'fresh complete V25 Source/receipt namespace')
        d.mkdir(mode=0o700); e.mkdir(mode=0o700)
        archived_packages = {}
        for original, dst_name, receipt in [(bv, 'sealed_full_ROOT_BOUND_qualification_SOURCE', None),
                                           (pv, 'sealed_independent_complete_BOUND_qualification_SOURCE_review', seal)]:
            archived_packages[dst_name] = archive_complete_source(original, d / (dst_name + '.tar.gz'), m)
            if receipt is not None:
                receipt_path = d / '_actual_peer_Source_seal_tool_return.json'
                shutil.copyfile(receipt['path'], receipt_path)
                m.require(m.full_pin(receipt_path)['sha256'] == receipt['sha256'], 'actual Source peer seal exact bytes')
        for name in ('pure_helper_controls.py', 'pure_helper_controls_host.py', 'fresh_verifier_controls.py',
                     'fresh_verifier_host.py', 'inactive_audit_snapshot_controls_SOURCE_ONLY.py'):
            m.require(not os.path.lexists(d / name), 'fresh full direct Source entrypoint')
            shutil.copyfile(broot / name, d / name)
            m.require(m.full_pin(d / name)['sha256'] == m.full_pin(broot / name)['sha256'], 'direct Source entrypoint exact bytes')
        shutil.copyfile(__file__, d / Path(__file__).name)
        if kind == 'fresh':
            shutil.copyfile(INSTALLER, d / INSTALLER.name)
        view = dict(root=str(d), files=[m.full_pin(p) for p in sorted(d.rglob('*')) if p.is_file()],
                    directories={'.': m.identity(d), **{p.relative_to(d).as_posix(): m.identity(p) for p in sorted(d.rglob('*')) if p.is_dir()}})
        m.require(not any(p.is_symlink() for p in d.rglob('*')), 'no installed Source aliases')
        freeze = dict(schema='ROOT_V25_COMPLETE_PRIVATE_INACTIVE_AUDIT_QUALIFICATION_SOURCE_FREEZE_V1', source_only=True,
                      kind=kind, source_namespace=view, complete_bound_source=bv, independent_complete_bound_Source_peer=pv,
                      lossless_complete_Source_archives=archived_packages,
                      bound_Source_peer_report=report_pin, Source_installer=m.full_pin(Path(__file__).resolve()),
                      actual_installed_helper=helper, original_helper_Q_canonical_fullEOF_unchanged=protected,
                      controller_or_helper_guard_API_executed=False, new_actual_helper_qualification=None,
                      six_future_business_pins=[None] * 6)
        fp = e / 'Root_final_complete_qualification_SOURCE_freeze.json'
        m.write_new(fp, freeze)
        frozen[kind] = dict(source_files=len(view['files']), source_directories=len(view['directories']), freeze=m.full_pin(fp),
                            prelaunch_source_receipt_bytes=sum(p.stat().st_size for root in (d,e) for p in root.rglob('*') if p.is_file()))
    m.require(m.package(bv['manifest']['path'], bsha) == bv and m.package(pv['manifest']['path'], psha) == pv,
              'all original full generated and reviewed Source unchanged')
    m.require([m.full_pin(p, sha) for p, sha in m.PROTECTED.items()] == protected
              and m.full_pin(m.HELPER, m.HELPER_SHA) == helper, 'all original fixed helper/Q/canonical and new helper unchanged')
    print(json.dumps(dict(status='COMPLETE_BOUND_SOURCE_INSTALLED_AND_FROZEN_NOT_EXECUTED', source_only=True,
                          complete_scopes=frozen, new_actual_helper_qualification=None), separators=(',', ':')))

if __name__ == '__main__':
    main()
