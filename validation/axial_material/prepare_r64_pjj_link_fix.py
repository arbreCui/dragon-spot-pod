"""Retain the inactive-link trial and explicitly link both new PJJ objects."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess
from production_runner import ROOT,dump_json,require_file,sha256


def main():
    base=ROOT/'validation/artifacts/axial-material-r64-pjj64-20261003'
    manifest=json.loads(require_file(base/'execution.json','72c31825bbdb3f80e4a807c9850ee6f6bd9bffc2a365652289c841a49616020f').read_text())
    for name,wanted in manifest['files'].items():require_file(Path(name),wanted)
    if 'record mismatch: PJJ64$MCCG' not in (base/'audit_initialized/audit.log').read_text():
        raise ValueError('requires preserved missing-record rejection')
    work=ROOT/'validation/artifacts/axial-material-r64-pjj64-linkfix-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build','runtime','audit_build'):
        shutil.copytree(base/name,work/name,ignore=shutil.ignore_patterns('__pycache__','build.log','build_readonly_memory.log'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm','snapshot.x2m'):shutil.copy2(base/'A'/name,work/'A'/name)
    old=json.loads((base/'protocol.json').read_text())
    commands=[[arg.replace(str(base),str(work)) for arg in command] for command in old['build_commands']]
    link=commands[2]
    first_library=link.index(str(ROOT/'lib/Darwin_arm64/libDragon.a'))
    link[first_library:first_library]=[str(work/'build/MCGASM.o'),str(work/'build/MCGFST.o')]
    if not all(link.count(str(work/'build'/name))==1 for name in ('MCGASM.o','MCGFST.o')):
        raise ValueError('new object activation is not explicit')
    protocol=dict(old,schema='AXMAT_PJJ64_EXPLICIT_LINK_V2',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        build_correction='The predecessor generated its link object list before compiling new files, so the full executable omitted both new objects. Preserve its inactive-candidate results; explicitly include MCGASM.o and MCGFST.o.',
        build_commands=commands,predecessor_audit_status_sha256=sha256(base/'audit_initialized/run_status.json'))
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    dump_json(work/'audit_build/build_command.json',commands[-1])
    (work/'audit_build/build_readonly_memory.log').write_bytes((work/'build/build.log').read_bytes())
    files=dict(manifest['files']);files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'audit_initialized/run_status.json',base/'audit_initialized/audit.log',Path(__file__).resolve()):files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':main()
