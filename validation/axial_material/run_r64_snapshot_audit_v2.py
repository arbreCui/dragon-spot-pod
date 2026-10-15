"""Corrected standalone audit: initialize native MOC tables and use regular input copies."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import time

from production_runner import ROOT, DiskResources, SerialExecutor, dump_json, require_file, sha256
from analyze_r64_snapshot import analyze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('execution',type=Path)
    parser.add_argument('--sha256',required=True)
    args = parser.parse_args()
    execution = args.execution.resolve()
    work = execution.parent
    manifest = json.loads(require_file(execution,args.sha256).read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    status = json.loads((work/'run_status.json').read_text())
    if status['classification']!='R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT' or not status['frozen_inputs_unchanged']:
        raise ValueError('completed immutable snapshot required')
    for name,wanted in status['outputs'].items():
        require_file(work/'A'/name,wanted)
    audit = work/'audit_initialized'
    audit.mkdir(exist_ok=False)
    built = work/'audit_build'
    if not built.is_dir():
        built = ROOT/'validation/artifacts/axial-material-r64-snapshot-A-20261003/audit'
    for name in ('audit_r64_snapshot.f90','audit_snapshot','build_command.json','build_readonly_memory.log'):
        shutil.copy2(built/name,audit/name)
    for name in ('snapshot_A.xsm','radial_track.bin'):
        shutil.copy2(work/'A'/name,audit/name)
    shutil.copy2(Path(__file__).with_name('analyze_r64_snapshot.py'),audit/'analyze_r64_snapshot.py')
    # FLU normally initializes the shared MOC function tables before any door.
    # This standalone caller must establish the identical kernel precondition.
    p=audit/'audit_r64_snapshot.f90'
    source=p.read_text()
    anchor="  call DOORFV64(sg,npsys,track,91,0,ng,nu,key,title,leakage,q,fresh,contract,cutoff,ok)"
    if source.count(anchor)!=1:
        raise ValueError('unexpected audit source')
    p.write_text(source.replace(anchor,"  call XDRTA2\n"+anchor,1))
    command=json.loads((audit/'build_command.json').read_text())
    command=[str(p) if item.endswith('/audit_r64_snapshot.f90') else item for item in command]
    command[command.index('-o')+1]=str(audit/'audit_snapshot')
    dump_json(audit/'build_command.json',command)
    with (audit/'build_readonly_memory.log').open('wb') as log:
        subprocess.run(command,cwd=audit,check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)

    files = {str(p):sha256(p) for p in audit.iterdir() if p.is_file()}
    for p in (execution,work/'run_status.json',work/'A/snapshot_A.xsm',work/'A/radial_track.bin',work/'audit/run_status.json',work/'audit/protocol.json',ROOT/'src/XDRTA2.f',Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    protocol = dict(schema='AXMAT_SERIALIZED_R64_AUDIT_INITIALIZED_V2',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        wall_seconds=60,automatic_retries=0,threads=1,
        scope='Correct prior standalone-tool precondition bug by calling the same XDRTA2 initializer as FLU.f:420; use regular verified input copies. Preserve prior failed audit. Read saved XSM into memory, rebuild all 370 external sources independently, evaluate a fresh unaccelerated all-group image with the unchanged 2.5e-8 radial tolerance, export and independently analyze binary64 records.',
        acceptance={'scalar_image_defect':2.5e-7,'full_image_defect':2.5e-7,'balance_keff_relative_defect':2.5e-7,'geometry_relative_error':5e-6},
        files=files)
    dump_json(audit/'protocol.json',protocol)
    protocol_hash=sha256(audit/'protocol.json')
    with (audit/'claim.json').open('x') as stream:
        json.dump({'started_unix':time.time(),'protocol_sha256':protocol_hash},stream)
    resources=DiskResources(Path(manifest['artifact_root']),manifest['resource_roots'],8*2**30,12*2**30)
    runner=SerialExecutor(work,60,'A',resources)
    result=dict(classification='AUDIT_FAILED_NO_RETRY',snapshot_qualified=False,production_qualified=False,
                protocol_sha256=protocol_hash,resources_before=resources.check())
    start=time.monotonic()
    try:
        with (audit/'audit.log').open('xb') as out:
            runner._process([str(audit/'audit_snapshot')],audit,subprocess.DEVNULL,out,60)
        if (audit/'audit.log').read_text().count('AXMAT-R64-SNAPSHOT-AUDIT-EXPORTED')!=1:
            raise ValueError('audit export incomplete')
        observations=analyze(audit/'audit.bin')
        dump_json(audit/'observations.json',observations)
        result['classification']=observations['classification']
        result['snapshot_qualified']=observations['classification']=='R64_SNAPSHOT_TERMINAL_AUDIT_PASS'
    except BaseException as error:
        result['error']=repr(error)
        raise
    finally:
        result['elapsed_seconds']=time.monotonic()-start
        try:
            require_file(audit/'protocol.json',protocol_hash)
            for name,wanted in {**manifest['files'],**files}.items():
                require_file(Path(name),wanted)
            result['frozen_inputs_unchanged']=True
        except BaseException as error:
            result.update(classification='INPUT_IDENTITY_FAILURE',identity_error=repr(error),snapshot_qualified=False)
        result['outputs']={p.name:sha256(p) for p in audit.iterdir() if p.is_file() and p.name not in ('run_status.json',) and str(p) not in files}
        result['resources_after']=resources.check()
        dump_json(audit/'run_status.json',result)
    print(json.dumps({k:v for k,v in result.items() if not k.startswith('resources')},indent=2))


if __name__=='__main__':
    main()
