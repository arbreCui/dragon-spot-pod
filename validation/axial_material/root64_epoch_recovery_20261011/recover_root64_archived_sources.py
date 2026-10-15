"""Read-only exact-byte ROOT64 lookup inside retained Source tar archives."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import tarfile
import time

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('byte_lookup', HERE / 'recover_root64_source_mapping_v2.py')
lookup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lookup)


def main():
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(RuntimeError('600 second audit cap')))
    signal.alarm(600)
    start = time.monotonic()
    old_mapping = json.loads((HERE / 'ROOT64_CURRENT_SOURCE_MAPPING.json').read_text())
    expected = {(r['historical_pin']['sha256'], r['historical_pin']['size_bytes']): r['historical_pin']
                for r in old_mapping['rows'] if r['status'] == 'MISSING_NO_EXACT_COPY_FOUND'}
    sizes = {size for _, size in expected}
    archives = []
    unique = {}
    members_seen = 0
    member_bytes_hashed = 0
    matches = []
    source_body_hits = []
    for root in [lookup.ROOT / 'validation/axial_material', lookup.ROOT / 'validation/artifacts']:
        for directory, _, names in os.walk(root, followlinks=False):
            lookup.budget()
            for name in names:
                if not name.endswith(('.tar.gz', '.tgz', '.tar')):
                    continue
                path = Path(directory) / name
                if path.is_symlink():
                    continue
                archive_pin = lookup.pin(path)
                archives.append(archive_pin)
                unique.setdefault(archive_pin['sha256'], archive_pin)
    for archive_pin in unique.values():
        lookup.budget()
        with tarfile.open(archive_pin['path'], 'r:*') as archive:
            for member in archive:
                lookup.budget()
                members_seen += 1
                if not member.isfile():
                    continue
                source_ext = Path(member.name).suffix.lower() in {'.py', '.f', '.f90', '.patch', '.diff', '.txt'}
                if member.size not in sizes and not (source_ext and member.size <= 1024 * 1024):
                    continue
                stream = archive.extractfile(member)
                raw = stream.read()
                if len(raw) != member.size:
                    raise RuntimeError('short archived member read')
                member_bytes_hashed += len(raw)
                digest = hashlib.sha256(raw).hexdigest()
                if (digest, len(raw)) in expected:
                    matches.append({'historical_pin': expected[(digest, len(raw))],
                                    'archive_current_pin': archive_pin, 'member_name': member.name,
                                    'member_size_bytes': len(raw), 'member_sha256': digest})
                lowered = raw.lower()
                if source_ext and any(marker in lowered for marker in
                    [b'module spor64_boot64', b'subroutine spoboot64', b'program test_root64_boot_connected']):
                    source_body_hits.append({'archive_current_pin': archive_pin,
                                             'member_name': member.name, 'size_bytes': len(raw),
                                             'sha256': digest})
    result = {'schema': 'ROOT64_RETAINED_SOURCE_ARCHIVE_LOOKUP_V1',
              'source': lookup.pin(__file__), 'input_mapping': lookup.pin(HERE / 'ROOT64_CURRENT_SOURCE_MAPPING.json'),
              'archives': archives, 'unique_archive_count': len(unique), 'members_seen': members_seen,
              'member_bytes_read_and_hashed': member_bytes_hashed,
              'exact_missing_input_matches': matches, 'complete_source_signature_hits': source_body_hits,
              'wall_seconds': time.monotonic() - start,
              'no_extraction_no_native_no_compile_no_numerical_execution': True,
              'old_identity_or_online_or_science_qualification': False}
    lookup.save(HERE / 'ROOT64_ARCHIVED_SOURCE_MAPPING.json', result)
    print(json.dumps({'status': 'READ_ONLY_SOURCE_ARCHIVE_LOOKUP_COMPLETED',
                      'unique_archive_count': len(unique), 'archive_copy_count': len(archives),
                      'members_seen': members_seen, 'member_bytes_hashed': member_bytes_hashed,
                      'exact_missing_input_match_count': len(matches),
                      'complete_source_signature_hit_count': len(source_body_hits),
                      'wall_seconds': result['wall_seconds'],
                      'result': lookup.pin(HERE / 'ROOT64_ARCHIVED_SOURCE_MAPPING.json')}, allow_nan=False))


if __name__ == '__main__':
    main()
