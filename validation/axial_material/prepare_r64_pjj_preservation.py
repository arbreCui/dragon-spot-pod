"""Preserve existing double PJJ assembly values through source-term recovery."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT,dump_json,require_file,sha256


def once(text,before,after):
    if text.count(before)!=1:
        raise ValueError('unexpected source anchor: '+before[:60])
    return text.replace(before,after,1)


def main():
    base=ROOT/'validation/artifacts/axial-material-r64-rebalance-inputfix-20261003'
    compiled=ROOT/'validation/artifacts/axial-material-r64-rebalance-20261003'
    manifest=json.loads(require_file(base/'execution.json','5b62c23869f5d75105ff6a6cdf3c35bd2cd547ba93f47fc335c9c4bc3488be00').read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    audit=json.loads((base/'audit_initialized/observations.json').read_text())
    if audit['classification']!='R64_SNAPSHOT_TERMINAL_AUDIT_FAIL':
        raise ValueError('requires the preserved bare-image mismatch')
    work=ROOT/'validation/artifacts/axial-material-r64-pjj64-20261003'
    work.mkdir(exist_ok=False)
    shutil.copytree(compiled/'build',work/'build',ignore=shutil.ignore_patterns('build.log'))
    for name in ('runtime','audit_build'):
        shutil.copytree(base/name,work/name,ignore=shutil.ignore_patterns('__pycache__','build_readonly_memory.log'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm','snapshot.x2m'):
        shutil.copy2(base/'A'/name,work/'A'/name)
    source=(ROOT/'src/MCGASM.f').read_text()
    source=once(source,'      DOUBLE PRECISION WEIGHT,WEIGHT0','      DOUBLE PRECISION WEIGHT,WEIGHT0\n      INTEGER AXI,AXMODE,AXINDEX\n      DOUBLE PRECISION, ALLOCATABLE :: AXPJJ64(:)')
    anchor='         DEALLOCATE(PJJD,PJJDX,PJJDY,PJJDZ,PJJDXI,PJJDYI,PJJDZI)'
    source=once(source,anchor,"""*        Preserve the original normalized double owner before demotion.
         IF(NREG.EQ.8.AND.NPJJM.EQ.1.AND.NGEFF.EQ.370.AND.NDIM.EQ.2)
     1   THEN
           ALLOCATE(AXPJJ64(NREG*NPJJM))
           DO II=1,NGEFF
             DO AXMODE=1,NPJJM
               DO AXI=1,NREG
                 AXINDEX=(AXMODE-1)*NREG+AXI
                 AXPJJ64(AXINDEX)=PJJD((II-1)*NREG*NPJJM+AXINDEX)*
     1             (2.D0/DBLE(V(AXI)))
               ENDDO
             ENDDO
             JPSYS=KPSYS(II)
             CALL LCMPUT(JPSYS,'PJJ64$MCCG',NREG*NPJJM,4,AXPJJ64)
           ENDDO
           DEALLOCATE(AXPJJ64)
         ENDIF
"""+anchor)
    (work/'build/MCGASM.f').write_text(source)
    source=(ROOT/'src/MCGFST.f').read_text()
    source=once(source,'INTEGER II,I,IND,IMOD,INU,INUP,INDP','INTEGER II,I,IND,IMOD,INU,INUP,INDP,AXLEN,AXTYPE')
    source=once(source,'      CHARACTER*12 NPJJT,NPJJIT','      CHARACTER*12 NPJJT,NPJJIT\n      DOUBLE PRECISION, ALLOCATABLE :: AXPJJ64(:,:)')
    source=once(source,'      ALLOCATE(PJJ(NREG,NPJJM),PJJI(NREG,NPJJM))','''      IF(NREG.NE.8.OR.KPN.NE.14.OR.NANI.NE.1.OR.NFUNL.NE.1.OR.
     1 NPJJM.NE.1.OR.IDIR.NE.0) CALL XABORT('AXMAT PJJ64: SCOPE')
      ALLOCATE(PJJ(NREG,NPJJM),PJJI(NREG,NPJJM),AXPJJ64(NREG,NPJJM))''')
    source=once(source,'         CALL LCMGET(JPSYS,NPJJT,PJJ)', '''         CALL LCMGET(JPSYS,NPJJT,PJJ)
         CALL LCMLEN(JPSYS,'PJJ64$MCCG',AXLEN,AXTYPE)
         IF(AXLEN.NE.NREG*NPJJM.OR.AXTYPE.NE.4)
     1     CALL XABORT('AXMAT PJJ64: MISSING DOUBLE AUTHORITY')
         CALL LCMGET(JPSYS,'PJJ64$MCCG',AXPJJ64)
         DO I=1,NREG
           IF(TRANSFER(REAL(AXPJJ64(I,1)),0).NE.
     1        TRANSFER(PJJ(I,1),0)) CALL XABORT('AXMAT PJJ64: MIRROR')
         ENDDO''')
    source=source.replace('PJJ(I,IMOD)*S','AXPJJ64(I,IMOD)*S')
    source=once(source,'      DEALLOCATE(PJJI,PJJ)','      DEALLOCATE(PJJI,PJJ,AXPJJ64)')
    (work/'build/MCGFST.f').write_text(source)
    for name in ('MCGASM.f','MCGFST.f'):
        p=work/'build'/name
        p.with_suffix('.f.patch').write_text(''.join(difflib.unified_diff((ROOT/'src'/name).read_text().splitlines(True),p.read_text().splitlines(True),fromfile=name,tofile=str(p))))
    p=work/'audit_build/audit_r64_snapshot.f90'
    source=p.read_text()
    source=once(source,'  real(real32) :: volume(nr),k32,controls(4),eps(5)', '  real(real32) :: volume(nr),k32,controls(4),eps(5),pjj32(nr,ng)\n  real(real64) :: pjj64(nr,ng)')
    anchor='  fresh=phi;npsys=[(i,i=1,ng)];leakage=0.0_real64'
    source=once(source,anchor,"""  do ig=1,ng
    g=LCMGIL(sg,ig)
    call require(g,'PJJ64$MCCG',nr,4);call LCMGET(g,'PJJ64$MCCG',pjj64(:,ig))
    call require(g,'PJJ$MCCG',nr,2);call LCMGET(g,'PJJ$MCCG',pjj32(:,ig))
    do i=1,nr
      if(transfer(real(pjj64(i,ig),real32),0_int32)/=transfer(pjj32(i,ig),0_int32)) &
        call fail('PJJ32 mirror differs')
    enddo
  enddo
  if(.not.all(ieee_is_finite(pjj64)).or.any(pjj64<0)) call fail('invalid PJJ64')
  open(newunit=u,file='pjj.bin',status='new',access='stream',form='unformatted',action='write')
  write(u) [nr,ng],pjj64,pjj32
  close(u)
  write(*,'(A)') 'AXMAT-PJJ64-MIRROR-PASS GROUPS=370'
"""+anchor)
    p.write_text(source)
    old=json.loads((compiled/'protocol.json').read_text())
    flags=[x.replace(str(compiled),str(work)) for x in old['build_commands'][0][1:old['build_commands'][0].index('-c')]]
    commands=[['gfortran',*flags,'-c',str(work/'build'/name),'-o',str((work/'build'/name).with_suffix('.o'))] for name in ('MCGASM.f','MCGFST.f')]
    libraries=[ROOT/'lib/Darwin_arm64/libDragon.a',ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    commands.append(['gfortran','-O2','-ffp-contract=off',str(ROOT/'src/DRAGON.o'),*map(str,sorted((work/'build').glob('*.o'))),*map(str,libraries),'-o',str(work/'runtime/Dragon')])
    commands.append(['gfortran',*flags,str(p),str(work/'build/MCGFST.o'),str(work/'build/SPOR64_A8.o'),str(work/'build/SPOR64_A8_ACA.o'),*map(str,libraries),'-o',str(work/'audit_build/audit_snapshot')])
    protocol=dict(schema='AXMAT_PJJ64_PRESERVATION_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='Preserve already computed PJJD normalization in a double record and consume it in source-term isolation recovery. Original legacy PJJ record remains an exact binary32 mirror. Same input, geometry, track, material, work targets, rebalancing and acceptance gates.',
        wall_seconds=600,threads=1,automatic_retries=0,predecessor_audit_sha256=sha256(base/'audit_initialized/observations.json'),
        acceptance='Normal completion plus unchanged saved-double bare-transport/source/balance audit and exact PJJ32 mirror checks. No automatic B/AAA/ABA.',
        build_commands=commands,protected_base=old['protected_base'],source_inputs={str(ROOT/'src'/name):sha256(ROOT/'src'/name) for name in ('MCGASM.f','MCGFST.f')})
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    dump_json(work/'audit_build/build_command.json',commands[-1])
    (work/'audit_build/build_readonly_memory.log').write_bytes((work/'build/build.log').read_bytes())
    files=dict(manifest['files']);files.update(protocol['source_inputs'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'audit_initialized/observations.json',Path(__file__).resolve()):files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':main()
