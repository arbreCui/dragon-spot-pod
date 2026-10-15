"""Declare one distinct initial-guess contrast after the cold-start budget stop."""
import datetime
import json
from pathlib import Path
import shutil

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-20261003'
    manifest = json.loads(require_file(base / 'execution.json', '2fd06e51dbb80006658ef91b34aa5e7f6b5ed9d9265d5a3cd10493666f802b75').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    status = json.loads((base / 'run_status.json').read_text())
    if status['classification'] != 'FAILED_NO_RETRY' or not status['frozen_inputs_unchanged'] or 'TimeoutExpired' not in status['error']:
        raise ValueError('expected preserved cold-start budget stop')
    seed = ROOT / 'validation/artifacts/axial-material-inputs-20261003/A/snapshot_A.xsm'
    require_file(seed, 'bfa69cde92cc7ec6a3f3e81215d737293ce8846addb272b0bac7f8c68a63f936')
    work = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-warm-20261003'
    work.mkdir(exist_ok=False)
    for name in ('A', 'runtime'):
        (work / name).mkdir()
    for source in (base / 'runtime').iterdir():
        if source.is_file():
            shutil.copy2(source, work / 'runtime' / source.name)
    for name in ('material.xsm', 'geometry.dat'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    shutil.copy2(seed, work / 'A/seed_A.xsm')
    deck = (base / 'A/snapshot.x2m').read_text()
    deck = deck.replace("XSM_FILE SNAP_OUT", "XSM_FILE SEED_IN :: FILE './seed_A.xsm' ;\nXSM_FILE SNAP_OUT", 1)
    deck = deck.replace('SYSTEM FLUX SNAP ;', 'SYSTEM FLUX SNAP SEEDSET ;', 1)
    deck = deck.replace('MODULE SALT:', 'MODULE RECOVER: SALT:', 1)
    deck = deck.replace('FLUX := FLU:', 'SEEDSET := SEED_IN ;\nFLUX := RECOVER: SEEDSET :: ITEM 1 ;\nFLUX := FLU:', 1)
    deck = deck.replace('REBA OFF ;', 'REBA OFF INIT ON ;', 1)
    (work / 'A/snapshot.x2m').write_text(deck)
    protocol = dict(schema='AXMAT_R64_WARM_SNAPSHOT_PROTOCOL_V1',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='One separately declared initial-guess contrast; identical binary64 candidate, material, geometry, boundaries and convergence controls to the cold run.',
        change='Recover legacy binary32 A flux only as initial guess, then recompute in binary64 with INIT ON. The seed is not certified at the stricter tolerances.',
        cold_status_sha256=sha256(base / 'run_status.json'), seed_sha256=sha256(seed),
        wall_seconds=600, threads=1, automatic_retries=0,
        acceptance='Normal completion plus independent serialized binary64 audit. No automatic B/AAA/ABA execution or accuracy acceptance.',
        retained_controls={'outer':2.5e-7,'inner':2.5e-8,'rebalancing':'OFF'},
        protected_base=json.loads((base / 'protocol.json').read_text())['protected_base'])
    dump_json(work / 'protocol.json', protocol)
    files = dict(manifest['files'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (seed, base/'run_status.json', Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__ == '__main__':
    main()
