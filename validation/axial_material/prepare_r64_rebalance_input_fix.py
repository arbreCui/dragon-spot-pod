"""Preserve the rejected REBA ON spelling; use the documented bare REBA keyword."""
import datetime
import json
from pathlib import Path
import shutil
from production_runner import ROOT,dump_json,require_file,sha256


def main():
    base=ROOT/'validation/artifacts/axial-material-r64-rebalance-20261003'
    manifest=json.loads(require_file(base/'execution.json','2b3ed05441066c02145ea7bdfd1e23af94a45db06266adc52a9e2ce683a913bc').read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    log=(base/'A/solve.log').read_text()
    if 'FLUGPI: READ ERROR - ILLEGAL KEYWORD ON' not in log or 'MCCGF64-CENSUS' in log:
        raise ValueError('not the expected input-only rejection')
    work=ROOT/'validation/artifacts/axial-material-r64-rebalance-inputfix-20261003'
    work.mkdir(exist_ok=False)
    for name in ('runtime','audit_build'):
        shutil.copytree(base/name,work/name,ignore=shutil.ignore_patterns('__pycache__'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm'):
        shutil.copy2(base/'A'/name,work/'A'/name)
    deck=(base/'A/snapshot.x2m').read_text()
    if deck.count('REBA ON INIT ON')!=1:
        raise ValueError('unexpected deck')
    (work/'A/snapshot.x2m').write_text(deck.replace('REBA ON INIT ON','REBA INIT ON',1))
    protocol=json.loads((base/'protocol.json').read_text())
    protocol.update(schema='AXMAT_R64_REBALANCE_INPUT_FIX_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        input_correction='FLUGPI accepts bare REBA to enable rebalancing; ON is only legal after INIT. Preserve previous pre-solve rejection and all numerical controls.',
        predecessor_status_sha256=sha256(base/'run_status.json'),predecessor_log_sha256=sha256(base/'A/solve.log'))
    dump_json(work/'protocol.json',protocol)
    files=dict(manifest['files']);files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'A/solve.log',base/'run_status.json',ROOT/'src/FLUGPI.f',Path(__file__).resolve()):
        files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':
    main()
