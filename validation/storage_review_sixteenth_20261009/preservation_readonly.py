import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

ROOT = Path('/Users/wen/spot')
REVIEW = ROOT / 'validation/storage_review_sixteenth_20261009'
TMP = Path('/private/tmp/spot_storage_sixteenth_root_readonly_20261009')

def update(digest, value):
    digest.update(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode())
    digest.update(b'\n')

def inventory():
    digests = {k: hashlib.sha256() for k in ('regular', 'symlink', 'directory_paths')}
    counts = dict.fromkeys(digests, 0)
    logical = allocated = 0
    inodes = set()
    roots = {}
    large = []
    caches = []
    for directory, directories, files in os.walk(ROOT, followlinks=False):
        parent = Path(directory)
        directories.sort()
        files.sort()
        directories[:] = [n for n in directories if parent / n not in (ROOT / '.git', REVIEW)]
        update(digests['directory_paths'], str(parent.relative_to(ROOT)))
        counts['directory_paths'] += 1
        links = [n for n in directories if (parent / n).is_symlink()]
        directories[:] = [n for n in directories if n not in links]
        for name in sorted(files + links):
            p = parent / name
            s = p.lstat()
            identity = [s.st_dev, s.st_ino, s.st_mode, s.st_size,
                        s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]
            rel = str(p.relative_to(ROOT))
            if stat.S_ISLNK(s.st_mode):
                update(digests['symlink'], [rel, identity, os.readlink(p)])
                counts['symlink'] += 1
            elif stat.S_ISREG(s.st_mode):
                update(digests['regular'], [rel, identity])
                counts['regular'] += 1
                logical += s.st_size
                inode = (s.st_dev, s.st_ino)
                alloc = s.st_blocks * 512 if inode not in inodes else 0
                inodes.add(inode)
                allocated += alloc
                parts = Path(rel).parts
                depth = 3 if parts[:2] == ('validation', 'artifacts') else 2 if parts[0] == 'validation' else 1
                key = '/'.join(parts[:depth])
                v = roots.setdefault(key, [0, 0, 0])
                v[0] += 1
                v[1] += s.st_size
                v[2] += alloc
                if s.st_size >= 64 * 2**20:
                    large.append(dict(path=str(p), bytes=s.st_size, allocated_bytes=alloc, identity=identity))
                if p.suffix == '.pyc' or '__pycache__' in parts:
                    caches.append(dict(path=str(p), bytes=s.st_size, allocated_bytes=alloc, identity=identity))
            else:
                raise ValueError('unexpected special file: ' + str(p))
    du = subprocess.run(['du', '-sk', str(ROOT)], check=True, capture_output=True, text=True)
    pins = {}
    for rel in ('validation/README.md', 'validation/axial_material/last_cprime_trim_build_review_20261008/current_progress.json',
                'validation/storage_review_fifteenth_20261009/REPORT.txt', 'validation/storage_cleanup_fourteenth_20261009/REPORT.txt'):
        p = ROOT / rel
        pins[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return dict(schema='SPOT_SIXTEENTH_READONLY_METADATA_PRESERVATION_V1', observed_unix=time.time(),
                scope='whole project except Git automatic capture and new R16 report directory; README and science progress INCLUDED',
                counts=counts, metadata_identity_sha256={k: v.hexdigest() for k, v in digests.items()},
                logical_regular_bytes=logical, unique_inode_allocated_bytes=allocated,
                project_du_KiB=int(du.stdout.split()[0]), document_sha256=pins,
                large_roots=sorted(roots.items(), key=lambda x: -x[1][2])[:45],
                large_files=sorted(large, key=lambda x: -x['bytes'])[:60], cache_like=caches,
                full_scientific_payload_rehashed=False, scientific_business_executed=False,
                files_deleted=0, reclaimed_bytes=0)

mode = sys.argv[1]
TMP.mkdir(exist_ok=True)
body = inventory()
if mode == 'before':
    assert not REVIEW.exists()
    target = TMP / 'before.json'
elif mode == 'after':
    before = json.loads((TMP / 'before.json').read_bytes())
    for k in ('counts', 'metadata_identity_sha256', 'logical_regular_bytes', 'document_sha256'):
        assert body[k] == before[k], (k, body[k], before[k])
    body['preservation_status'] = 'PASS_ALL_EXISTING_SCOPE_IDENTITIES_PATHS_AND_DOCUMENT_CONTENT_PINS_UNCHANGED'
    body['before_sha256'] = hashlib.sha256((TMP / 'before.json').read_bytes()).hexdigest()
    target = TMP / 'after.json'
else:
    raise ValueError(mode)
with target.open('x') as f:
    json.dump(body, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({k: body[k] for k in ('counts', 'metadata_identity_sha256', 'logical_regular_bytes', 'project_du_KiB', 'files_deleted', 'reclaimed_bytes')}, ensure_ascii=False))
