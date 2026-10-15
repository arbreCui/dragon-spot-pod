"""Preserve the rejected deck and declare its in-place FLUX syntax correction."""
import datetime
import json
from pathlib import Path
import shutil
from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-warm-20261003'
    manifest = json.loads(require_file(base/'execution.json','7c6406376c49656a02bd539ad4c229abcc1e6084cc5770b250d5e11fe21f8e69').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    log = (base/'A/solve.log').read_text()
    if 'LINKED_LIST *FLUX* ALREADY EXISTS' not in log or 'MCCGF64-CENSUS' in log or 'OUT(' in log:
        raise ValueError('not the known pre-solve input failure')
    work = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-warm-inputfix-20261003'
    work.mkdir(exist_ok=False)
    shutil.copytree(base/'runtime',work/'runtime',ignore=shutil.ignore_patterns('__pycache__'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm'):
        shutil.copy2(base/'A'/name,work/'A'/name)
    deck = (base/'A/snapshot.x2m').read_text()
    if deck.count('FLUX := FLU: SYSTEM') != 1:
        raise ValueError('unexpected deck')
    (work/'A/snapshot.x2m').write_text(deck.replace('FLUX := FLU: SYSTEM','FLUX := FLU: FLUX SYSTEM',1))
    protocol = json.loads((base/'protocol.json').read_text())
    protocol.update(schema='AXMAT_R64_WARM_INPUT_FIX_PROTOCOL_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        input_correction='List existing FLUX on RHS to mark the recovered object as modified. The rejected predecessor never entered eigen iteration.',
        predecessor_log_sha256=sha256(base/'A/solve.log'),predecessor_status_sha256=sha256(base/'run_status.json'))
    dump_json(work/'protocol.json',protocol)
    files = dict(manifest['files'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'A/solve.log',base/'run_status.json',Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__ == '__main__':
    main()
