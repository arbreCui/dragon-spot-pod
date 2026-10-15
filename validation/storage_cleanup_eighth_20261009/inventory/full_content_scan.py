import collections
import hashlib
import json
from pathlib import Path
import time

OUT = Path('/private/tmp/spot_eighth_storage_readonly_scan_20261009')
if not __debug__:
    raise RuntimeError('optimization must be disabled')

def identity(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(row):
    path = Path(row['path'])
    assert identity(path) == row['identity'], row['path']
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(4 * 1024 ** 2):
            digest.update(block)
    assert identity(path) == row['identity'], row['path']
    return dict(**row, sha256=digest.hexdigest(), stable_full_content_read=True)

def main():
    start = time.monotonic()
    source = json.loads((OUT / 'sample_groups.json').read_text())
    exact = []
    hashed = []
    for group in source['groups']:
        buckets = collections.defaultdict(list)
        for row in group['rows']:
            value = pin(row)
            hashed.append(value)
            buckets[value['sha256']].append(value)
        for digest, rows in buckets.items():
            if len(rows) > 1 and any(not row['protected'] and not row['inbound_link'] for row in rows):
                exact.append(dict(sha256=digest, size=rows[0]['size'], rows=rows))
    result = dict(status='READ_ONLY_EXACT_CONTENT_DUPLICATE_GROUPS_NO_DELETION',
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  sample_report_sha256=hashlib.sha256((OUT / 'sample_groups.json').read_bytes()).hexdigest(),
                  full_read_files=len(hashed), full_read_bytes=sum(row['size'] for row in hashed),
                  elapsed_seconds=time.monotonic() - start, files_deleted=0,
                  solver_or_API_executed=False, groups=exact, full_hash_records=hashed)
    output = OUT / 'exact_content_groups.json'
    with output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=result['status'], path=str(output),
                         sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                         groups=len(exact), full_read_files=len(hashed),
                         full_read_GiB=result['full_read_bytes'] / 2**30,
                         elapsed_seconds=result['elapsed_seconds'])))

if __name__ == '__main__':
    main()
