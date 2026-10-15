import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

ROOT = Path('/Users/wen/spot')
REVIEW = ROOT / 'validation/storage_review_fifteenth_20261009'
INDEX_PATHS = {
    ROOT / 'validation/README.md',
    ROOT / 'validation/axial_material/last_cprime_trim_build_review_20261008/current_progress.json',
}
BASELINE = Path('/private/tmp/spot_fifteenth_storage_preservation_before_20261009.json')
AFTER = Path('/private/tmp/spot_fifteenth_storage_preservation_after_20261009.json')

def record(digest, value):
    digest.update(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode())
    digest.update(b'\n')

def inventory():
    digests = {name: hashlib.sha256() for name in ('regular', 'symlink', 'directory_paths')}
    counts = {name: 0 for name in digests}
    logical = 0
    for directory, directories, files in os.walk(ROOT, followlinks=False):
        parent = Path(directory)
        directories.sort()
        files.sort()
        directories[:] = [name for name in directories if parent / name not in (ROOT / '.git', REVIEW)]
        record(digests['directory_paths'], str(parent.relative_to(ROOT)))
        counts['directory_paths'] += 1
        linked_dirs = [name for name in directories if (parent / name).is_symlink()]
        directories[:] = [name for name in directories if name not in linked_dirs]
        for name in sorted(files + linked_dirs):
            path = parent / name
            if path in INDEX_PATHS:
                continue
            value = path.lstat()
            identity = [value.st_dev, value.st_ino, value.st_mode, value.st_size,
                        value.st_mtime_ns, value.st_ctime_ns, value.st_nlink]
            relative = str(path.relative_to(ROOT))
            if stat.S_ISREG(value.st_mode):
                record(digests['regular'], [relative, identity])
                counts['regular'] += 1
                logical += value.st_size
            elif stat.S_ISLNK(value.st_mode):
                record(digests['symlink'], [relative, identity, os.readlink(path)])
                counts['symlink'] += 1
            else:
                raise ValueError('Unexpected special file: ' + str(path))
    observation = subprocess.run(['du', '-k', '-s', str(ROOT)], check=True,
                                 capture_output=True, text=True)
    return {
        'schema': 'SPOT_FIFTEENTH_STORAGE_READONLY_METADATA_PRESERVATION_V1',
        'observed_unix': time.time(),
        'scope': 'project outside Git, new review, and two intentional documentation indexes',
        'counts': counts,
        'metadata_identity_sha256': {name: digest.hexdigest() for name, digest in digests.items()},
        'logical_regular_bytes_in_scope': logical,
        'project_du_KiB': int(observation.stdout.split()[0]),
        'full_scientific_data_content_read': False,
        'no_business_import_or_solver': True,
        'deleted_files': 0,
    }

mode = sys.argv[1]
body = inventory()
if mode == 'before':
    assert not BASELINE.exists() and not REVIEW.exists()
    BASELINE.write_text(json.dumps(body, ensure_ascii=False, indent=2) + '\n')
elif mode == 'after':
    before = json.loads(BASELINE.read_text())
    for field in ('counts', 'metadata_identity_sha256', 'logical_regular_bytes_in_scope'):
        assert body[field] == before[field], (field, body[field], before[field])
    body['preservation_status'] = 'PASS_METADATA_IDENTITIES_AND_PATHS_UNCHANGED'
    body['baseline_sha256'] = hashlib.sha256(BASELINE.read_bytes()).hexdigest()
    AFTER.write_text(json.dumps(body, ensure_ascii=False, indent=2) + '\n')
else:
    raise ValueError(mode)
print(json.dumps(body, ensure_ascii=False))
