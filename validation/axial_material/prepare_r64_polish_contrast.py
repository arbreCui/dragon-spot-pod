"""Build one explicit stricter inner-accuracy contrast, preserving acceptance controls."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def replace_once(text,before,after):
    if text.count(before)!=1:
        raise ValueError('source anchor differs: '+before[:60])
    return text.replace(before,after,1)


def main():
    warm=ROOT/'validation/artifacts/axial-material-r64-snapshot-A-warm-inputfix-20261003'
    manifest=json.loads(require_file(warm/'execution.json','6beef5bd97e804ef4e05fffbff0b7df590132ce289497a8350d885b11acb82bd').read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    status=json.loads((warm/'run_status.json').read_text())
    if status['classification']!='FAILED_NO_RETRY' or not status['frozen_inputs_unchanged'] or 'TimeoutExpired' not in status['error']:
        raise ValueError('only a preserved warm-start budget stop admits this contrast')
    base=ROOT/'validation/artifacts/axial-material-r64-snapshot-A-20261003'
    work=ROOT/'validation/artifacts/axial-material-r64-inner-polish-20261003'
    work.mkdir(exist_ok=False)
    for name in ('A','build','runtime','audit_build'):
        (work/name).mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm','snapshot.x2m'):
        shutil.copy2(warm/'A'/name,work/'A'/name)
    for p in (warm/'runtime').glob('*.py'):
        shutil.copy2(p,work/'runtime'/p.name)
    # The frozen earlier classifier mistakenly counts the echoed source line.
    # Fix only this reporting bug, requiring an actually executed marker.
    p=work/'runtime/run_r64_snapshot_experiment.py'
    source=p.read_text()
    source=replace_once(source,"if text.count(marker) != 1:","if (sum(line == marker for line in text.splitlines()) if c['mode'] == 'first_call_probe' else sum(line.startswith('>|'+marker+' ') for line in text.splitlines())) != 1:")
    p.write_text(source)
    for p in (base/'build').iterdir():
        if p.suffix in ('.o','.mod'):
            shutil.copy2(p,work/'build'/p.name)
    radial=(ROOT/'src/SPOR64_A8.f90').read_text()
    old='    if (any(leak1d64 /= 0.0_real64)) epsi64 = DP_MCCG_EPSI64'
    radial=replace_once(radial,old,old+"\n    ! Isolated snapshot sensitivity: stricter work target, never a relaxed gate.\n    epsi64 = min(epsi64, 2.5e-10_real64)\n    write(6,'(A,ES24.16)') ' AXMAT-INNER-WORK-TARGET=',epsi64")
    (work/'build/SPOR64_A8.f90').write_text(radial)
    driver=(base/'build/AXMAT_SNAPSHOT_DRIVER64.f').read_text()
    driver=replace_once(driver,'DOUBLE PRECISION EINN,GINN,FINN,EEXT,ERRDEB1','DOUBLE PRECISION AXMAT_EPS64\n      PARAMETER(AXMAT_EPS64=2.5D-10)\n      DOUBLE PRECISION EINN,GINN,FINN,EEXT,ERRDEB1')
    anchor="         CALL LCMPUT(IPFLUX,'SPOT-KEFF64',1,4,AKEFF)"
    driver=replace_once(driver,anchor,anchor+"\n         CALL LCMPUT(IPFLUX,'AXMAT-EPS64',1,4,AXMAT_EPS64)")
    (work/'build/AXMAT_SNAPSHOT_DRIVER64.f').write_text(driver)
    for original,new in ((ROOT/'src/SPOR64_A8.f90',work/'build/SPOR64_A8.f90'),(base/'build/AXMAT_SNAPSHOT_DRIVER64.f',work/'build/AXMAT_SNAPSHOT_DRIVER64.f')):
        new.with_suffix(new.suffix+'.patch').write_text(''.join(difflib.unified_diff(original.read_text().splitlines(True),new.read_text().splitlines(True),fromfile=str(original),tofile=str(new))))
    audit=(base/'audit/audit_r64_snapshot.f90').read_text()
    audit=replace_once(audit,'real(real64) :: k,phi','real(real64) :: work_epsi\n  real(real64) :: k,phi')
    anchor="  call require(flux,'SPOT-KEFF64',1,4);call LCMGET(flux,'SPOT-KEFF64',k)"
    audit=replace_once(audit,anchor,"  call require(flux,'AXMAT-EPS64',1,4);call LCMGET(flux,'AXMAT-EPS64',work_epsi)\n  if(work_epsi/=2.5e-10_real64) call fail('wrong internal work tolerance')\n"+anchor)
    (work/'audit_build/audit_r64_snapshot.f90').write_text(audit)
    flags=['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
           '-I'+str(work/'build'),'-I'+str(ROOT/'lib/Darwin_arm64/modules'),'-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(work/'build')]
    commands=[]
    for name in ('SPOR64_A8.f90','AXMAT_SNAPSHOT_DRIVER64.f'):
        p=work/'build'/name
        commands.append(['gfortran',*flags,'-c',str(p),'-o',str(p.with_suffix('.o'))])
    libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    commands.append(['gfortran','-O2','-ffp-contract=off',str(ROOT/'src/DRAGON.o'),*map(str,sorted((work/'build').glob('*.o'))),*map(str,libraries),'-o',str(work/'runtime/Dragon')])
    audit_command=['gfortran',*flags,str(work/'audit_build/audit_r64_snapshot.f90'),str(work/'build/SPOR64_A8.o'),str(work/'build/SPOR64_A8_ACA.o'),*map(str,libraries),'-o',str(work/'audit_build/audit_snapshot')]
    commands.append(audit_command)
    protocol=dict(schema='AXMAT_R64_INNER_ACCURACY_CONTRAST_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='One warm A snapshot, same inputs/binary64 driver. Tighten only inner GMRES and its ACA work accuracy from tracked 2.5e-8 to min(tracked,2.5e-10). This is a numerical accuracy sensitivity, not a pure-precision contrast.',
        wall_seconds=600,automatic_retries=0,threads=1,
        unchanged=['material','geometry','boundary','thermal threshold 2.5e-7','outer thresholds 2.5e-7','REBA OFF','same legacy A initial guess','Krylov work cap 20'],
        metadata='TRACK REAL-PARAM remains the acceptance control 2.5e-8; FLUX AXMAT-EPS64 records actual stricter work target 2.5e-10.',
        acceptance='Normal executed completion plus independent saved binary64 source, flux-image and balance audit at original 2.5e-7 terminal gates. No automatic B/AAA/ABA or physical accuracy acceptance.',
        predecessor_status_sha256=sha256(warm/'run_status.json'),build_commands=commands,
        protected_base=json.loads((base/'protocol.json').read_text())['protected_base'])
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
    dump_json(work/'audit_build/build_command.json',audit_command)
    (work/'audit_build/build_readonly_memory.log').write_bytes((work/'build/build.log').read_bytes())
    files=dict(manifest['files'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (warm/'run_status.json',Path(__file__).resolve()):
        files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':
    main()
