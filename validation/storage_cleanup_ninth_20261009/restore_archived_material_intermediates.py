"""List archived old material files, or explicitly restore their exact bytes."""
import argparse, gzip, hashlib, json, os, stat
from pathlib import Path
from pack_old_material_intermediates import BASE, PACK, CHUNK, identity, pin, material_path, verify_gzip

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--restore-all', action='store_true')
    parser.add_argument('--path')
    args = parser.parse_args()
    assert not (args.restore_all and args.path)
    manifest = json.loads((BASE / 'manifest.json').read_text())
    rows = [r for r in manifest['candidates'] if r['category'] == 'GZIP_ARCHIVED_OLD_MATERIAL_INTERMEDIATE']
    if not args.restore_all and not args.path:
        print(json.dumps(dict(restored=False, files=[dict(path=r['path'], archive=r['compressed_backup']['path']) for r in rows]), indent=2)); return
    if args.path:
        rows = [r for r in rows if r['path'] == args.path]
        assert len(rows) == 1
    checked = []
    for row in rows:
        target, rel = material_path(row['path'])
        backup = Path(row['compressed_backup']['path'])
        assert backup == PACK / (str(rel) + '.gz') and backup.parent.resolve(strict=True) == backup.parent
        fresh = pin(backup); expected = row['compressed_backup']
        assert fresh['sha256'] == expected['sha256'] and fresh['size'] == expected['size']
        verify_gzip(backup, row['size'], row['sha256'])
        assert not target.is_symlink()
        if target.exists():
            current = pin(target); assert current['size'] == row['size'] and current['sha256'] == row['sha256']
        checked.append((row, target, backup))
    restored = []
    for row, target, backup in checked:
        if target.exists():
            continue
        size = 0; h = hashlib.sha256()
        with target.open('xb') as destination:
            try:
                with gzip.open(backup, 'rb') as stream:
                    while chunk := stream.read(CHUNK):
                        size += len(chunk); assert size <= row['size']
                        h.update(chunk); destination.write(chunk)
                assert size == row['size'] and h.hexdigest() == row['sha256']
                destination.flush(); os.fsync(destination.fileno())
            except BaseException:
                destination.close(); target.unlink(); raise
        os.chmod(target, stat.S_IMODE(row['identity'][2]))
        os.utime(target, ns=(row['identity'][4], row['identity'][4]))
        restored.append(str(target))
    print(json.dumps(dict(status='PASS', restored=restored, order='Restore archived material originals before using earlier rounds\u2019 duplicate-copy restoration tools.')))

if __name__ == '__main__':
    main()
