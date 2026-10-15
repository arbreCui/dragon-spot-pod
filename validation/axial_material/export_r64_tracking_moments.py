"""Export quadrature and tracking owners without launching any transport solve."""
import argparse
import datetime
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256

SOURCE = '''program export_tracking
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,int32
  implicit none
  type(c_ptr) :: disk,archive,objects,track
  real(real32) :: zmu(4),wzmu(4),xmu(4),volume(14),albedo(6)
  integer(int32) :: mccg(40),state(40),nzon(14),keycur(6),bc(6)
  integer :: u,n,t
  call LCMOP(disk,'snapshot_A.xsm',2,2,0)
  call LCMOP(archive,'MOMENTMEM',0,1,0)
  call LCMEQU(disk,archive)
  call LCMCL(disk,1)
  objects=LCMGID(archive,'TRACK');track=LCMGIL(objects,1)
  call LCMGET(track,'STATE-VECTOR',state)
  call LCMGET(track,'MCCG-STATE',mccg)
  if(state(1)/=8.or.state(2)/=14.or.mccg(2)/=4) call XABORT('MOMENT: SCOPE')
  call get32('ZMU$MCCG',zmu);call get32('WZMU$MCCG',wzmu)
  call get32('XMU$MCCG',xmu);call get32('V$MCCG',volume)
  call get32('ALBEDO',albedo)
  call LCMGET(track,'NZON$MCCG',nzon)
  call LCMGET(track,'KEYCUR$MCCG',keycur)
  call LCMGET(track,'BC-REFL+TRAN',bc)
  open(newunit=u,file='moments.bin',status='new',access='stream',form='unformatted')
  write(u) [4_int32,14_int32],zmu,wzmu,xmu,volume,albedo,nzon,keycur,bc,mccg,state
  close(u)
  call LCMCL(archive,2)
  write(*,'(A)') 'AXMAT-TRACKING-MOMENTS-EXPORTED'
contains
  subroutine get32(name,x)
    character(len=*),intent(in) :: name
    real(real32),intent(out) :: x(:)
    call LCMLEN(track,name,n,t)
    if(n/=size(x).or.t/=2) call XABORT('MOMENT: BAD RECORD')
    call LCMGET(track,name,x)
  end subroutine
end program
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('execution', type=Path)
    parser.add_argument('--sha256', required=True)
    args = parser.parse_args()
    execution = args.execution.resolve()
    manifest = json.loads(require_file(execution, args.sha256).read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    work = execution.parent
    status = json.loads((work / 'run_status.json').read_text())
    snapshot = require_file(work / 'A/snapshot_A.xsm', status['outputs']['snapshot_A.xsm'])
    out = work / 'tracking_moments'
    out.mkdir(exist_ok=False)
    shutil.copy2(snapshot, out / snapshot.name)
    source = out / 'export_tracking.f90'
    source.write_text(SOURCE)
    command = json.loads((work / 'audit_build/build_command.json').read_text())
    command = [str(source) if x.endswith('/audit_r64_snapshot.f90') else x for x in command]
    command[command.index('-o') + 1] = str(out / 'export_tracking')
    dump_json(out / 'build_command.json', command)
    files = {str(p): sha256(p) for p in (execution, snapshot, source,
        out / snapshot.name, out / 'build_command.json', Path(__file__).resolve())}
    protocol = dict(schema='AXMAT_TRACKING_OWNER_EXPORT_V1',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        wall_seconds=60, automatic_retries=0, transport_solves=0,
        scope='Read-only export of saved native quadrature, geometry and boundary normalization owners.',
        files=files)
    dump_json(out / 'protocol.json', protocol)
    with (out / 'build.log').open('xb') as log:
        subprocess.run(command, check=True, cwd=out, stdout=log, stderr=subprocess.STDOUT, timeout=60)
    with (out / 'export.log').open('xb') as log:
        subprocess.run([str(out / 'export_tracking')], check=True, cwd=out,
            stdout=log, stderr=subprocess.STDOUT, timeout=60)
    if (out / 'export.log').read_text().count('AXMAT-TRACKING-MOMENTS-EXPORTED') != 1:
        raise ValueError('incomplete owner export')
    for name, wanted in {**manifest['files'], **files}.items():
        require_file(Path(name), wanted)
    result = dict(classification='TRACKING_OWNERS_EXPORTED',
        frozen_inputs_unchanged=True, protocol_sha256=sha256(out / 'protocol.json'),
        outputs={p.name: sha256(p) for p in out.iterdir() if p.is_file() and str(p) not in files})
    dump_json(out / 'run_status.json', result)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
