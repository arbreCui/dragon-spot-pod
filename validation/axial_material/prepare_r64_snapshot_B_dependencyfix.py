"""Preserve the failed packaging attempt and declare one corrected B execution."""
import json
from pathlib import Path
import shutil

from production_runner import ROOT, dump_json, require_file, sha256


def main():
    art = ROOT / 'validation/artifacts'
    old = art / 'axial-material-r64-snapshot-B-20261004'
    wanted = '87e69fa51587c7ae4882329b27fd737e15f9385fdb2200eaf584b79537a94c81'
    original = json.loads(require_file(old / 'execution.json', wanted).read_text())
    for name, digest in original['files'].items():
        require_file(Path(name), digest)
    if (old / 'run_status.json').exists() or (old / 'B/solve.log').exists():
        raise ValueError('expected pre-transport constructor failure only')
    claim = old / 'run_claim.json'
    if json.loads(claim.read_text())['execution_sha256'] != wanted:
        raise ValueError('failed attempt claim differs')
    failure = old / 'packaging_failure_receipt.json'
    with failure.open('x') as stream:
        json.dump(dict(schema='AXMAT_PRE_TRANSPORT_PACKAGING_FAILURE_V1',
            execution_sha256=wanted, claim_sha256=sha256(claim),
            classification='MISSING_BOUNDED_RUNNER_BEFORE_TRANSPORT',
            missing_path=str(old / 'runtime/run_bounded_dragon.py'),
            transport_started=False, numerical_result_exists=False,
            error='FileNotFoundError during SerialExecutor.__init__',
            automatic_retries=0), stream, indent=2)
    work = art / 'axial-material-r64-snapshot-B-dependencyfix-20261004'
    work.mkdir(exist_ok=False)
    for name in ('runtime', 'B', 'audit_build'):
        shutil.copytree(old / name, work / name, ignore=shutil.ignore_patterns('__pycache__'))
    bounded = art / 'axial-material-r64-system-normalization-20261003/runtime/run_bounded_dragon.py'
    a = json.loads((art / 'axial-material-r64-system-normalization-20261003/execution.json').read_text())
    require_file(bounded, a['files'][str(bounded)])
    shutil.copy2(bounded, work / 'runtime/run_bounded_dragon.py')
    protocol = json.loads((old / 'protocol.json').read_text())
    protocol.update(schema='AXMAT_R64_B_CERTIFIED_PRODUCER_DEPENDENCYFIX_V1',
        prior_execution_sha256=wanted, prior_failure_receipt_sha256=sha256(failure),
        correction='Package the unchanged A bounded runner; all producer, material, deck, audit executables and numerical gates are unchanged.',
        automatic_retries=0)
    dump_json(work / 'protocol.json', protocol)
    files = dict(original['files'])
    files.update({str(p): sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (old / 'execution.json', failure, claim, bounded, Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    resources = sorted(set(original['resource_roots'] + [str(work)]))
    corrected = dict(original, files=files, resource_roots=resources)
    dump_json(work / 'execution.json', corrected)
    print(json.dumps({'execution':str(work / 'execution.json'), 'sha256':sha256(work / 'execution.json')}, indent=2))


if __name__ == '__main__':
    main()
