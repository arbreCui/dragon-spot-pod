"""Declare isolated compensated accumulation of unchanged native flight terms."""
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT,DiskResources,dump_json,require_file,sha256


def once(text,before,after):
    if text.count(before)!=1:raise ValueError('source anchor differs: '+before[:80])
    return text.replace(before,after)


def main():
    art=ROOT/'validation/artifacts'
    base=art/'axial-material-AAA-inner-terminal-capture-20261004'
    contract=json.loads(require_file(base/'execution.json','a15a24f89197e9985aeb9f6744b69a42a8de349997529b3ef05e3b8eabf51e02').read_text())
    for name,wanted in contract['files'].items():require_file(Path(name),wanted)
    result=json.loads((base/'run_status.json').read_text())
    if result['classification']!='NATIVE_FAILED_INNER_TUPLE_CAPTURED_AND_RECONSTRUCTED' or not result['original_rounded_census_identical']:
        raise ValueError('qualified failure capture required')
    work=art/'axial-material-AAA-compensated-flight-20261004'
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(work)]
    resources=DiskResources(art,roots,8*2**30,24*2**30);before=resources.check()
    work.mkdir(exist_ok=False)
    for name in ('build','runtime','AAA'):(work/name).mkdir()
    # Keep the diagnostic cache/export in the A8 copy; the single solver change
    # is the named summation routine called at its unchanged flight boundary.
    a8=(base/'build/SPOR64_A8.f90').read_text().replace('subroutine MCGFCF(','subroutine AXMAT_MCGFCF_COMP(').replace('end subroutine MCGFCF','end subroutine AXMAT_MCGFCF_COMP').replace('call MCGFCF(','call AXMAT_MCGFCF_COMP(')
    (work/'build/SPOR64_A8.f90').write_text(a8)
    original=(ROOT/'src/MCGFCF.f').read_text()
    text=once(original,'SUBROUTINE MCGFCF(','SUBROUTINE AXMAT_MCGFCF_COMP(')
    text=once(text,'      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:) :: T2D,WEITF,B,FLUX',
        '      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:) :: T2D,WEITF,B,FLUX\n      DOUBLE PRECISION, ALLOCATABLE :: FTERM(:),CFLUX(:),CPHI(:,:)')
    text=once(text,'      PHI(:KPN,:NGEFF)=0.0D0',
        "      IF(NDIM.NE.2.OR.NLF.NE.1.OR.NLIN.NE.1.OR.IDIR.NE.0)\n     1 CALL XABORT('AXMAT COMP FLIGHT: LOCKED 2D ISOTROPIC ONLY')\n      ALLOCATE(FTERM(KPN),CFLUX(KPN),CPHI(KPN,NGEFF))\n      CPHI=0.0D0\n      PHI(:KPN,:NGEFF)=0.0D0")
    begin=text.index('*        2D calculation -> loop over the polar angle')
    end=text.index('         DEALLOCATE(T2DB,OMEGA2B,WEIGHTB)',begin)
    block=text[begin:end]
    block=once(block,'             FLUX(:KPN)=0.0D0','             FLUX(:KPN)=0.0D0\n             CFLUX=0.0D0')
    block=once(block,'                 CALL SUBFFI(SUBSCH,K,KPN,M,NSEG(IL1),',
        '                 FTERM=0.0D0\n                 CALL SUBFFI(SUBSCH,K,KPN,M,NSEG(IL1),')
    block=once(block,'S(1,II),NREG,KEYFLX,KEYCUR,FLUX,B,','S(1,II),NREG,KEYFLX,KEYCUR,FTERM,B,')
    block=once(block,'     4                 NSOUT,XSI)\n               ENDDO',
        '     4                 NSOUT,XSI)\n                 CALL AXMAT_KAHAN_ADD(KPN,FTERM,FLUX,CFLUX)\n               ENDDO')
    block=once(block,'             PHI(:KPN,II)=PHI(:KPN,II)+FLUX(:KPN)',
        '             CALL AXMAT_KAHAN_ADD(KPN,FLUX,PHI(1,II),\n     1                            CPHI(1,II))')
    text=text[:begin]+block+text[end:]
    helper='''
      SUBROUTINE AXMAT_KAHAN_ADD(N,TERM,TOTAL,CORRECTION)
      IMPLICIT NONE
      INTEGER N,I
      DOUBLE PRECISION TERM(N),TOTAL(N),CORRECTION(N),Y,T
      DO I=1,N
        Y=TERM(I)-CORRECTION(I)
        T=TOTAL(I)+Y
        CORRECTION(I)=(T-TOTAL(I))-Y
        TOTAL(I)=T
      ENDDO
      END
'''
    text+=helper
    source=work/'build/AXMAT_MCGFCF_COMP.f';source.write_text(text)
    (work/'build/AXMAT_MCGFCF_COMP.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),text.splitlines(True),fromfile='original',tofile='compensated')))
    libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    flags=['-O2','-march=native','-ffp-contract=off','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
        '-I'+str(work/'build'),'-I'+str(ROOT/'lib/Darwin_arm64/modules'),'-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(work/'build')]
    commands=[]
    for path in (work/'build/SPOR64_A8.f90',source):
        commands.append(['gfortran',*flags,'-c',str(path),'-o',str(path.with_suffix('.o'))])
    commands.append(['gfortran','-O2','-march=native','-ffp-contract=off','-g',str(ROOT/'src/DRAGON.o'),str(work/'build/SPOR64_A8.o'),str(source.with_suffix('.o')),*map(str,libraries),'-o',str(work/'runtime/Dragon')])
    for name in ('production_runner.py','production_inputs.py','run_bounded_dragon.py'):
        shutil.copy2(base/'runtime'/name,work/'runtime'/name)
    for name in ('picard_radial.x2m','SpotStepR64.c2m'):shutil.copy2(base/'AAA'/name,work/'AAA'/name)
    inputs={}
    for p in (base/'AAA').iterdir():
        if p.is_symlink():
            actual=p.resolve();(work/'AAA'/p.name).symlink_to(actual);inputs[str(actual)]=sha256(actual)
    protocol=dict(schema='AXMAT_AAA_COMPENSATED_NATIVE_FLIGHT_REPLAY_V1',wall_seconds=300,threads=1,retries=0,
        scope='Separate arithmetic diagnostic from the exact frozen second-map proposal. Sum unchanged native single-track/polar contributions with compensated additions, then sum batch totals with compensation. Flight scheme, source, cross sections, normalization, ACA, GMRES and both 1e-13/2.5e-7 terminal predicates are unchanged. No production promotion or CE acceptance.',
        original_failure_capture_sha256=sha256(base/'run_status.json'),build_commands=commands,
        resources_before=before,algorithm_change='Floating-point accumulation order only; ideal real-arithmetic operator unchanged.',
        success_requires='Native normal completion, all three online radial terminals, returned-state admission, immutable source inputs; success alone is not a coupled fixed point.')
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for cmd in commands:subprocess.run(cmd,cwd=work/'build',stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
    files={str(p):sha256(p) for p in work.rglob('*') if p.is_file() and not p.is_symlink()};files.update(inputs)
    for path in (*libraries,ROOT/'src/DRAGON.o',ROOT/'src/MCGFCF.f',base/'execution.json',base/'run_status.json',Path(__file__).resolve()):files[str(path)]=sha256(path)
    dump_json(work/'execution.json',dict(schema=protocol['schema'],wall_seconds=300,threads=1,retries=0,
        artifact_root=str(art),resource_roots=roots,files=files))
    print(json.dumps(dict(execution=str(work/'execution.json'),sha256=sha256(work/'execution.json')),indent=2))


if __name__=='__main__':main()
