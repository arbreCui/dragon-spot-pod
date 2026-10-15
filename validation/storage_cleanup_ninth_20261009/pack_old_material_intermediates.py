"""Create and verify lossless backups; this tool never removes original files."""
import argparse, gzip, hashlib, json, os, stat, time
from pathlib import Path

ROOT = Path('/Users/wen/spot')
BASE = ROOT / 'validation/storage_cleanup_ninth_20261009'
PACK = BASE / 'packed_material_intermediates'
FAMILIES = ('d4a-final-four-fuel-temperature-run-20261002', 'd4a-remaining-fuel-temperature-run-20261001', 'd4a-remaining-temperature-run-20261001')
CHUNK = 4 * 1024 ** 2
if not __debug__:
    raise RuntimeError('Safety checks require optimization disabled')

def identity(p):
    s = p.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_nlink]

def pin(p):
    before = identity(p)
    assert stat.S_ISREG(before[2]) and before[-1] == 1
    h = hashlib.sha256()
    with p.open('rb') as stream:
        assert os.fstat(stream.fileno()).st_ino == before[1]
        while chunk := stream.read(CHUNK):
            h.update(chunk)
    assert identity(p) == before
    return dict(path=str(p), identity=before, size=before[3], sha256=h.hexdigest(), allocated_bytes=p.stat().st_blocks * 512)

def verify_gzip(p, wanted_size, wanted_sha):
    before = identity(p)
    h = hashlib.sha256(); size = 0
    with gzip.open(p, 'rb') as stream:
        while chunk := stream.read(CHUNK):
            size += len(chunk); assert size <= wanted_size
            h.update(chunk)
    assert identity(p) == before and size == wanted_size and h.hexdigest() == wanted_sha
    return dict(size=size, sha256=h.hexdigest())

def material_path(raw):
    p = Path(raw)
    assert p.is_absolute() and str(p) == raw and '..' not in p.parts
    rel = p.relative_to(ROOT / 'validation/artifacts')
    assert rel.parts[0] in FAMILIES and p.name == 'tape30' and p.parent.name in ('pendf', 'groupr')
    assert p.parent.resolve(strict=True) == p.parent
    return p, rel

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-sha256', required=True)
    args = parser.parse_args(); start = time.monotonic()
    source = BASE / 'material_archive_input.json'
    assert pin(source)['sha256'] == args.input_sha256
    rows = json.loads(source.read_text())
    assert len(rows) == 89 and len({r['path'] for r in rows}) == 89
    assert BASE.resolve(strict=True) == BASE and not PACK.exists()
    PACK.mkdir(); records = []
    with (BASE / 'backup_creation_ledger.jsonl').open('x') as ledger:
        for row in rows:
            p, rel = material_path(row['path']); before = identity(p)
            assert before == row['identity'] and stat.S_ISREG(before[2]) and before[-1] == 1
            target = PACK / (str(rel) + '.gz')
            target.parent.mkdir(parents=True, exist_ok=True)
            assert target.parent.resolve(strict=True) == target.parent
            h = hashlib.sha256(); size = 0
            with p.open('rb') as source_stream, target.open('xb') as destination:
                assert os.fstat(source_stream.fileno()).st_ino == before[1]
                with gzip.GzipFile(filename='', mode='wb', compresslevel=6, mtime=0, fileobj=destination) as compressed:
                    while chunk := source_stream.read(CHUNK):
                        size += len(chunk); h.update(chunk); compressed.write(chunk)
                destination.flush(); os.fsync(destination.fileno())
            assert identity(p) == before and size == row['size'] and h.hexdigest() == row['sha256']
            backup = pin(target)
            verified = verify_gzip(target, row['size'], row['sha256'])
            record = dict(original=row, backup=backup, verified_decompressed=verified)
            records.append(record)
            ledger.write(json.dumps(record, separators=(',', ':')) + '\n'); ledger.flush(); os.fsync(ledger.fileno())
            print(json.dumps(dict(backups_completed=len(records), total=len(rows))), flush=True)
    report = dict(schema='SPOT_NINTH_VERIFIED_LOSSLESS_MATERIAL_BACKUPS_V1', status='PASS', input_sha256=args.input_sha256, records=records, raw_allocated_bytes=sum(r['allocated_bytes'] for r in rows), compressed_allocated_bytes=sum(r['backup']['allocated_bytes'] for r in records), originals_removed=0, elapsed_seconds=time.monotonic()-start)
    with (BASE / 'packed_material_intermediate_backups.json').open('x') as stream:
        json.dump(report, stream, indent=2); stream.write('\n')
    print(json.dumps(dict(status='PASS', backups=len(records), raw_GiB=report['raw_allocated_bytes']/2**30, compressed_GiB=report['compressed_allocated_bytes']/2**30, originals_removed=0, elapsed_seconds=report['elapsed_seconds'])), flush=True)

if __name__ == '__main__':
    main()
