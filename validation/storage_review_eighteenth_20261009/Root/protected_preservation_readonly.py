import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import time

ROOT = Path('/Users/wen/spot')
REVIEW = ROOT / 'validation/storage_review_eighteenth_20261009'
TMP = Path('/private/tmp/spot_storage_eighteenth_root_readonly_20261009')
PLAN = json.loads((TMP/'approved_fixed_plan.json').read_bytes())
DELETE_PATHS = {x['path'] for x in PLAN['selected']}

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
                if str(p) in DELETE_PATHS:
                    continue
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
                'validation/storage_review_fifteenth_20261009/REPORT.txt', 'validation/storage_review_sixteenth_20261009/REPORT.txt', 'validation/storage_review_sixteenth_20261009/Root_actual_preservation_closeout.json', 'validation/storage_cleanup_fourteenth_20261009/REPORT.txt', 'validation/storage_review_seventeenth_20261009/REPORT.txt', 'validation/storage_review_seventeenth_20261009/Root_actual_preservation_closeout.json', 'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009/REPORT.txt', 'validation/axial_material/last_cprime_trim_combined_live_resource_v9_build_review_20261009/Root_actual_V9_cold_finalization_tool_return.json'):
        p = ROOT / rel
        pins[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return dict(schema='SPOT_EIGHTEENTH_READONLY_METADATA_PRESERVATION_V1', observed_unix=time.time(),
                scope='whole project except Git automatic capture and new R18 report directory; README and science progress INCLUDED',
                counts=counts, metadata_identity_sha256={k: v.hexdigest() for k, v in digests.items()},
                logical_regular_bytes=logical, unique_inode_allocated_bytes=allocated,
                project_du_KiB=int(du.stdout.split()[0]), document_sha256=pins,
                large_roots=sorted(roots.items(), key=lambda x: -x[1][2])[:45],
                large_files=sorted(large, key=lambda x: -x['bytes'])[:60], cache_like=caches,
                full_scientific_payload_rehashed=False, scientific_business_executed=False,
                files_deleted_by_this_readonly_reader=0, scientific_credit=False, excluded_exact_deletion_candidates=len(DELETE_PATHS))


mode=sys.argv[1]
body=inventory()
body['fixed_plan_sha256']=hashlib.sha256((TMP/'approved_fixed_plan.json').read_bytes()).hexdigest()
body['scope']='whole project protected remainder; exclude exact approved 14332 candidates, Git auto captures, new R18 report directory; original dirs/links and README/progress INCLUDED'
if mode=='before':
 original=json.loads((TMP/'before.json').read_bytes())
 assert body['counts']['regular']+len(DELETE_PATHS)==original['counts']['regular']
 assert body['logical_regular_bytes']+PLAN['logical_bytes']==original['logical_regular_bytes']
 assert body['document_sha256']==original['document_sha256']
 target=TMP/'protected_before.json'
elif mode=='after':
 before=json.loads((TMP/'protected_before.json').read_bytes())
 for k in ('counts','metadata_identity_sha256','logical_regular_bytes','document_sha256','fixed_plan_sha256'):
  assert body[k]==before[k],(k,body[k],before[k])
 assert all(not os.path.lexists(p) for p in DELETE_PATHS)
 body['approved_exact_selected_absent_count']=len(DELETE_PATHS)
 body['preservation_status']='PASS_ALL_NONSELECTED_IDENTITIES_AND_ORIGINAL_DIR_PATHS_LINKS_DOCUMENT_SHA_UNCHANGED'
 target=TMP/'protected_after.json'
else:raise ValueError(mode)
with target.open('x') as f:json.dump(body,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({k:body[k] for k in ('counts','metadata_identity_sha256','logical_regular_bytes','project_du_KiB','excluded_exact_deletion_candidates')},ensure_ascii=False))
