"""Preserve actual track-integrated normalization in binary64 records."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def once(source, before, after):
    if source.count(before) != 1:
        raise ValueError('unexpected source anchor: ' + before[:80])
    return source.replace(before, after, 1)


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-kernel-consistency-20261003'
    manifest = json.loads(require_file(base / 'execution.json',
        'f79713e8de00a50c3d6fceb808e10413b0d544fdfb20a0f1b72bc4bf17760751').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    if json.loads((base / 'audit_initialized/observations.json').read_text())['classification'] != 'R64_SNAPSHOT_TERMINAL_AUDIT_FAIL':
        raise ValueError('preserved failed audit required')
    work = ROOT / 'validation/artifacts/axial-material-r64-track-normalization-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build', 'runtime', 'audit_build'):
        shutil.copytree(base / name, work / name,
            ignore=shutil.ignore_patterns('__pycache__', 'build.log', 'build_readonly_memory.log'))
    (work / 'A').mkdir()
    for name in ('material.xsm', 'geometry.dat', 'seed_A.xsm', 'snapshot.x2m'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    p = work / 'build/MCGASM.f'
    source = p.read_text()
    source = once(source, '      INTEGER AXI,AXMODE,AXINDEX',
        '      INTEGER AXI,AXMODE,AXINDEX\n      DOUBLE PRECISION AXV64(14),AXPOL64,AXSUR64')
    anchor = '      ALLOCATE(TRHAR(NMU,NFUNL,NANGL),RHARM(NMU,NFUNL))'
    source = once(source, anchor, '''      IF(NREG.NE.8.OR.NFI.NE.14.OR.NDIM.NE.2.OR.NMU.NE.4)
     1  CALL XABORT('AXMAT V64: SCOPE')
      AXV64=0.D0
      AXPOL64=0.D0
      AXSUR64=0.D0
      DO AXI=1,NMU
        AXPOL64=AXPOL64+DBLE(ZMU(AXI))*DBLE(WZMU(AXI))
        AXSUR64=AXSUR64+DBLE(WZMU(AXI))
      ENDDO
''' + anchor)
    # Track region numbers have already been converted from negative surfaces
    # to the ordinary NREG+surface layout at this unique regular-track anchor.
    anchor = '''         IF(LPJJ) THEN
*        ----------------------------
*        Self-Collision Probabilities'''
    regular_start = source.index('      DO 20 ILINE=1,NBTR')
    position = source.index(anchor, regular_start)
    addition = '''         DO AXI=2,NSEG-1
           IF(NOM(AXI).LT.1.OR.NOM(AXI).GT.NREG)
     1       CALL XABORT('AXMAT V64: REGION')
           AXV64(NOM(AXI))=AXV64(NOM(AXI))+
     1       2.D0*WEIGHT*H(AXI)*AXPOL64
         ENDDO
         AXV64(NOM(1))=AXV64(NOM(1))+WEIGHT*AXSUR64
         AXV64(NOM(NSEG))=AXV64(NOM(NSEG))+WEIGHT*AXSUR64
'''
    source = source[:position] + addition + source[position:]
    anchor = '      DEALLOCATE(TRHAR)'
    source = once(source, anchor, '''      IF(ANY(AXV64.LE.0.D0)) CALL XABORT('AXMAT V64: NONPOSITIVE')
      DO AXI=1,14
        IF(ABS(AXV64(AXI)/DBLE(V(AXI))-1.D0).GT.2.D-6)
     1    CALL XABORT('AXMAT V64: GEOMETRY DRIFT')
      ENDDO
      CALL LCMPUT(IPTRK,'AXMAT-V64',14,4,AXV64)
      DO II=1,NGEFF
        CALL LCMPUT(KPSYS(II),'AXMAT-V64',14,4,AXV64)
      ENDDO
''' + anchor)
    source = once(source, '(2.D0/DBLE(V(AXI)))', '(2.D0/AXV64(AXI))')
    anchor = "             CALL LCMPUT(JPSYS,'PJJ64$MCCG',NREG*NPJJM,4,AXPJJ64)"
    source = once(source, anchor, '''             DO AXINDEX=1,NREG*NPJJM
               PJJ((II-1)*NREG*NPJJM+AXINDEX)=REAL(AXPJJ64(AXINDEX))
             ENDDO
''' + anchor)
    p.write_text(source)
    p = work / 'build/MCGFST.f'
    source = p.read_text()
    source = once(source, '      DOUBLE PRECISION, ALLOCATABLE :: AXPJJ64(:,:)',
        '      DOUBLE PRECISION, ALLOCATABLE :: AXPJJ64(:,:)\n      DOUBLE PRECISION AXV64(14)')
    anchor = "         CALL LCMGET(JPSYS,'PJJ64$MCCG',AXPJJ64)"
    source = once(source, anchor, anchor + '''
         CALL LCMLEN(JPSYS,'AXMAT-V64',AXLEN,AXTYPE)
         IF(AXLEN.NE.14.OR.AXTYPE.NE.4)
     1     CALL XABORT('AXMAT V64: MISSING AUTHORITY')
         CALL LCMGET(JPSYS,'AXMAT-V64',AXV64)
         IF(ANY(AXV64.LE.0.D0)) CALL XABORT('AXMAT V64: NONPOSITIVE')''')
    source = source.replace('/V(I)', '/AXV64(I)')
    p.write_text(source)
    for name in ('MCGASM.f', 'MCGFST.f'):
        p = work / 'build' / name
        p.with_suffix('.f.patch').write_text(''.join(difflib.unified_diff(
            (ROOT / 'src' / name).read_text().splitlines(True), p.read_text().splitlines(True),
            fromfile=name, tofile=str(p))))
    p = work / 'audit_build/audit_r64_snapshot.f90'
    source = p.read_text()
    source = once(source, '  real(real64) :: pjj64(nr,ng)',
        '  real(real64) :: pjj64(nr,ng),volume64(nu),group_volume64(nu)')
    anchor = '  do ig=1,ng\n    g=LCMGIL(sg,ig)\n    call require(g,\'PJJ64$MCCG\',nr,4)'
    source = once(source, anchor, '''  call require(track,'AXMAT-V64',nu,4);call LCMGET(track,'AXMAT-V64',volume64)
  if(.not.all(ieee_is_finite(volume64)).or.any(volume64<=0)) call fail('invalid volume64')
  do ig=1,ng
    g=LCMGIL(sg,ig)
    call require(g,'AXMAT-V64',nu,4);call LCMGET(g,'AXMAT-V64',group_volume64)
    if(any(transfer(group_volume64,[0_int64],nu)/=transfer(volume64,[0_int64],nu))) &
      call fail('group/track volume64 mismatch')
    call require(g,'PJJ64$MCCG',nr,4)''')
    anchor = "  write(*,'(A)') 'AXMAT-PJJ64-MIRROR-PASS GROUPS=370'"
    source = once(source, anchor, anchor + '''
  open(newunit=u,file='volume64.bin',status='new',access='stream',form='unformatted',action='write')
  write(u) [nu],volume64
  close(u)''')
    p.write_text(source)
    old = json.loads((base / 'protocol.json').read_text())
    commands = [[arg.replace(str(base), str(work)) for arg in command]
                for command in old['build_commands']]
    protocol = dict(old, schema='AXMAT_BINARY64_TRACK_NORMALIZATION_V6',
        declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        normalization_correction='Accumulate actual fixed-track volume and boundary moments '
        'in binary64 using unchanged stored quadrature. Save AXMAT-V64 on TRACK and '
        'each SYSTEM group, normalize PJJ and scalar/current integration with that owner. '
        'Retain original geometry records and existing outer balance volumes. '
        'Independent Python track replay is required in addition to the unchanged terminal audit.',
        build_commands=commands, predecessor_audit_sha256=sha256(base / 'audit_initialized/observations.json'),
        tracking_moments_sha256=sha256(base / 'tracking_moments/moments.bin'))
    dump_json(work / 'protocol.json', protocol)
    with (work / 'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command, cwd=work / 'build', check=True,
                           stdout=log, stderr=subprocess.STDOUT, timeout=60)
    dump_json(work / 'audit_build/build_command.json', commands[-1])
    (work / 'audit_build/build_readonly_memory.log').write_bytes((work / 'build/build.log').read_bytes())
    files = dict(manifest['files'])
    files.update({str(p): sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base / 'audit_initialized/observations.json',
              base / 'tracking_moments/moments.bin', Path(__file__).resolve()):
        files[str(p)] = sha256(p)
    dump_json(work / 'execution.json', dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',
        mode='snapshot_A', wall_seconds=600, automatic_retries=0,
        artifact_root=str(ROOT / 'validation/artifacts'),
        resource_roots=sorted(str(p.resolve()) for p in
            (ROOT / 'validation/artifacts').glob('axial-material-*') if p.is_dir()), files=files))
    print(sha256(work / 'execution.json'))


if __name__ == '__main__':
    main()
