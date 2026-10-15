"""Declare a separate tighter multigroup work-accuracy contrast if needed."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT,dump_json,require_file,sha256


def once(text,before,after):
    if text.count(before)!=1:
        raise ValueError('source anchor differs: '+before[:60])
    return text.replace(before,after,1)


def main():
    base=ROOT/'validation/artifacts/axial-material-r64-inner-polish-20261003'
    manifest=json.loads(require_file(base/'execution.json','6cc3b721c6c473eef6bd9a8eabe0cbc69922227b0dd786990140135954354540').read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    status=json.loads((base/'run_status.json').read_text())
    if status['classification']!='FAILED_NO_RETRY' or not status['frozen_inputs_unchanged'] or 'TimeoutExpired' not in status['error']:
        raise ValueError('requires the preserved inner-only contrast budget stop')
    work=ROOT/'validation/artifacts/axial-material-r64-thermal-polish-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build','runtime','audit_build'):
        shutil.copytree(base/name,work/name,ignore=shutil.ignore_patterns('__pycache__','build.log','build_readonly_memory.log'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm','snapshot.x2m'):
        shutil.copy2(base/'A'/name,work/'A'/name)
    p=work/'build/AXMAT_SNAPSHOT_DRIVER64.f'
    source=p.read_text()
    source=once(source,'DOUBLE PRECISION AXMAT_EPS64','DOUBLE PRECISION AXMAT_THER64\n      PARAMETER(AXMAT_THER64=2.5D-9)\n      DOUBLE PRECISION AXMAT_EPS64')
    source=once(source,'IF((GINN.LT.EPSINR).AND.(IGDEB.EQ.IG)) THEN','IF((GINN.LT.AXMAT_THER64).AND.(IGDEB.EQ.IG)) THEN')
    source=once(source,'IF(EINN.LT.EPSINR) THEN','IF(EINN.LT.AXMAT_THER64) THEN')
    source=once(source,"      IF(IPRT.GT.0) WRITE(6,1080) JT,EINN,EPSINR,IGDEB,ZMU", "      IF(IPRT.GT.0) WRITE(6,1080) JT,EINN,AXMAT_THER64,IGDEB,ZMU")
    anchor="         CALL LCMPUT(IPFLUX,'AXMAT-EPS64',1,4,AXMAT_EPS64)"
    source=once(source,anchor,anchor+"\n         CALL LCMPUT(IPFLUX,'AXMAT-THR64',1,4,AXMAT_THER64)")
    p.write_text(source)
    (work/'build/thermal-only.patch').write_text(''.join(difflib.unified_diff((base/'build/AXMAT_SNAPSHOT_DRIVER64.f').read_text().splitlines(True),source.splitlines(True),fromfile=str(base/'build/AXMAT_SNAPSHOT_DRIVER64.f'),tofile=str(p))))
    p=work/'audit_build/audit_r64_snapshot.f90'
    source=p.read_text()
    source=once(source,'real(real64) :: work_epsi','real(real64) :: work_epsi,work_thermal')
    anchor="  if(work_epsi/=2.5e-10_real64) call fail('wrong internal work tolerance')"
    source=once(source,anchor,anchor+"\n  call require(flux,'AXMAT-THR64',1,4);call LCMGET(flux,'AXMAT-THR64',work_thermal)\n  if(work_thermal/=2.5e-9_real64) call fail('wrong thermal work tolerance')")
    p.write_text(source)
    previous=json.loads((base/'protocol.json').read_text())
    commands=[[arg.replace(str(base),str(work)) for arg in command] for command in previous['build_commands']]
    # Same radial object, so only rebuild changed thermal driver, link, audit.
    commands=commands[1:]
    protocol=dict(schema='AXMAT_R64_THERMAL_ACCURACY_CONTRAST_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='Relative to the inner-only sensitivity, tighten group-freezing and multigroup-stop work tolerance from 2.5e-7 to 2.5e-9. Keep the existing inner work accuracy 2.5e-10. This tests accumulated multigroup solve error.',
        wall_seconds=600,automatic_retries=0,threads=1,
        unchanged=['same A material/geometry/boundary','same initial guess','same REAL64 arithmetic','same acceleration and REBA OFF','outer and stored acceptance controls 2.5e-7','tracked radial acceptance control 2.5e-8'],
        metadata='Store actual work targets as AXMAT-EPS64 and AXMAT-THR64; print actual thermal work target. EPS-CONVERGE retains original acceptance controls.',
        acceptance='Normal executed completion and independent saved-double source, flux-image and balance checks at original acceptance tolerances; no B/AAA/ABA or physics acceptance.',
        predecessor_status_sha256=sha256(base/'run_status.json'),build_commands=commands,protected_base=previous['protected_base'])
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    dump_json(work/'audit_build/build_command.json',commands[-1])
    (work/'audit_build/build_readonly_memory.log').write_bytes((work/'build/build.log').read_bytes())
    files=dict(manifest['files'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'run_status.json',Path(__file__).resolve()):
        files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':
    main()
