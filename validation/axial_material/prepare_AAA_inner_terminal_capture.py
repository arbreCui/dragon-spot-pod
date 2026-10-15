"""Declare one read-only-parent replay with failure-only internal tuple export."""
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT,DiskResources,dump_json,require_file,sha256,verify_sealed_directory


def main():
    art=ROOT/'validation/artifacts'
    prod=art/'axial-material-production-qualified-AB-storage-20261004'
    require_file(prod/'prepared.json','2c7fe827864095bea9ff07781f14ec4292b5c2829c04f5e9eafe4769011dfb17')
    state=json.loads((prod/'AAA/run_status.json').read_text())
    if state['classification']!='FAILED_NO_RETRY' or state['completed_maps']!=1:
        raise ValueError('expected second radial stage failure required')
    parent=prod/'AAA/map001';verify_sealed_directory(parent)
    failed=prod/'AAA/map002'
    if 'MCGMRE64: STRICT INNER TERMINAL FAILED; GROUPS=1 ARNOLDI=20' not in (failed/'picard_radial.log').read_text():
        raise ValueError('expected true inner-terminal failure missing')
    work=art/'axial-material-AAA-inner-terminal-capture-20261004'
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(work)]
    resources=DiskResources(art,roots,8*2**30,24*2**30);before=resources.check()
    work.mkdir(exist_ok=False)
    for name in ('build','runtime','AAA'):(work/name).mkdir()
    original=(ROOT/'src/SPOR64_A8.f90').read_text()
    changed=original.replace('  integer, parameter :: NGRP = 370',
        '  real(real64), allocatable, save :: diagnostic_bare64(:,:)\n  integer, parameter :: NGRP = 370',1)
    anchor="    call SPOMOC_CAPTURE64(ngeff, ngind, nun, qfr64, phiin64, source64, &\n        response64, nconv)"
    if changed.count(anchor)!=1:raise ValueError('capture anchor differs')
    changed=changed.replace(anchor,anchor+'\n    diagnostic_bare64 = response64')
    anchor="      write(6,'(A,I0,A,I0,A,1P,E13.5)') &\n          ' MCGMRE64: STRICT INNER TERMINAL FAILED; GROUPS=', lnconv, &"
    if changed.count(anchor)!=1:raise ValueError('failure anchor differs')
    changed=changed.replace(anchor,'''      call EXPORT_FAILED_TUPLE(nun,ngeff,ngind,nconv,iter,narnoldi, &
          epsi64,denom64,eps64,qfr64,phiin64,source64, &
          diagnostic_bare64,response64)
'''+anchor)
    helper='''
  subroutine EXPORT_FAILED_TUPLE(nun,ngeff,ngind,nconv,iter,narnoldi, &
      epsi64,denom64,eps64,qfr64,phiin64,source64,bare64,response64)
    integer,intent(in) :: nun,ngeff,ngind(ngeff),iter,narnoldi
    logical,intent(in) :: nconv(ngeff)
    real(real64),intent(in) :: epsi64,denom64(ngeff),eps64(ngeff)
    real(real64),intent(in) :: qfr64(nun,ngeff),phiin64(nun,ngeff)
    real(real64),intent(in) :: source64(nun,ngeff),bare64(nun,ngeff)
    real(real64),intent(in) :: response64(nun,ngeff)
    integer :: output,ii,ios
    open(newunit=output,file='failed_inner_tuple.bin',status='new', &
         access='stream',form='unformatted',action='write',iostat=ios)
    if(ios /= 0) call XABORT('AXMAT FAILED TUPLE: CANNOT CREATE EXPORT')
    write(output) 1,nun,ngeff,count(nconv),iter,narnoldi,epsi64
    do ii=1,ngeff
      if(.not.nconv(ii)) cycle
      write(output) ngind(ii),denom64(ii),eps64(ii),qfr64(:,ii), &
          phiin64(:,ii),source64(:,ii),bare64(:,ii),response64(:,ii)
    enddo
    close(output)
    write(6,'(A)') 'AXMAT-FAILED-INNER-TUPLE-EXPORTED'
  end subroutine EXPORT_FAILED_TUPLE
'''
    changed=changed.replace('end module SPOR64_A8',helper+'\nend module SPOR64_A8')
    source=work/'build/SPOR64_A8.f90';source.write_text(changed)
    (work/'build/SPOR64_A8.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),changed.splitlines(True),fromfile='original',tofile='failure-only-capture')))
    libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    flags=['-O2','-march=native','-ffp-contract=off','-g','-fPIC','-frecord-marker=4',
        '-I'+str(ROOT/'lib/Darwin_arm64/modules'),'-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(work/'build')]
    commands=[['gfortran',*flags,'-c',str(source),'-o',str(source.with_suffix('.o'))],
        ['gfortran','-O2','-march=native','-ffp-contract=off','-g',str(ROOT/'src/DRAGON.o'),str(source.with_suffix('.o')),*map(str,libraries),'-o',str(work/'runtime/Dragon')]]
    for name in ('production_runner.py','production_inputs.py','run_bounded_dragon.py'):
        shutil.copy2(prod/'runtime'/name,work/'runtime'/name)
    target=work/'AAA'
    inputs={}
    for name in ('projected_proposal.xsm','initial_radial_track.bin','route_contract.xsm',
                 'initial_axial_track.xsm','initial_axial_macrolib.xsm','basis_reference.xsm'):
        actual=(failed/name).resolve();inputs[str(actual)]=sha256(actual);(target/name).symlink_to(actual)
    for name in ('picard_radial.x2m','SpotStepR64.c2m'):
        shutil.copy2(failed/name,target/name)
    protocol=dict(schema='AXMAT_AAA_FAILED_RADIAL_INNER_TUPLE_DIAGNOSTIC_V1',wall_seconds=300,threads=1,retries=0,
        original_stage_failure_sha256=sha256(failed/'picard_radial.log'),
        original_AAA_status_sha256=sha256(prod/'AAA/run_status.json'),parent_seal_sha256=sha256(parent/'result.json'),
        scientific_accuracy_accepted=False,scope='Failure-only tuple export after the unchanged TRUE 1e-13 acceptance decision and MAXI=20 limit. Cache the bare image before ACA without changing arguments, source values, iterates, tests or returned status. Fresh native replay is diagnostic only; no continuation or retry of the failed production instance.',
        build_commands=commands,resources_before=before)
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    files={str(p):sha256(p) for p in work.rglob('*') if p.is_file() and not p.is_symlink()}
    files.update(inputs)
    for path in (*libraries,ROOT/'src/DRAGON.o',ROOT/'src/SPOR64_A8.f90',prod/'AAA/run_status.json',failed/'picard_radial.log',parent/'result.json',Path(__file__).resolve()):files[str(path)]=sha256(path)
    dump_json(work/'execution.json',dict(schema=protocol['schema'],wall_seconds=300,threads=1,retries=0,
        artifact_root=str(art),resource_roots=roots,files=files))
    print(json.dumps(dict(execution=str(work/'execution.json'),sha256=sha256(work/'execution.json')),indent=2))


if __name__=='__main__':main()
