"""Build the isolated MCCG TYPE-K double-precision snapshot candidate."""
import datetime
import difflib
import json
from pathlib import Path
import shutil
import subprocess

from production_runner import ROOT, dump_json, require_file, sha256


def once(text, before, after):
    if text.count(before) != 1:
        raise ValueError('source anchor differs: ' + before[:70])
    return text.replace(before, after)


def sources():
    source = (ROOT / 'src/FLUDRV.f').read_text()
    begin = source.index("      IF(CXDOOR.EQ.'SPOT') THEN\n      CALL FLU2DR64")
    end = source.index('      ELSE\n      CALL FLU2DR', begin)
    block = source[begin:end]
    new = block.replace("IF(CXDOOR.EQ.'SPOT')", "IF((CXDOOR.EQ.'MCCG').AND.(ITYPEC.EQ.2))").replace('CALL FLU2DR64', 'CALL AXMAT_SNAPSHOT_DRIVER64')
    source = source[:begin] + new + block.replace('      IF(', '      ELSEIF(', 1) + source[end:]
    result = {'FLUDRV.f':source}
    source = (ROOT / 'src/FLU2DR64.f').read_text().split('*DECK FLUSP64')[0]
    source = once(source, 'SUBROUTINE FLU2DR64(', 'SUBROUTINE AXMAT_SNAPSHOT_DRIVER64(')
    source = once(source, "      IF(CXDOOR.NE.'SPOT') CALL XABORT('FLU2DR64: SPOT DOOR ONLY.')", """      IF(CXDOOR.NE.'MCCG'.OR.ITYPEC.NE.2.OR.ILEAK.NE.0)
     1 CALL XABORT('AXMAT SNAPSHOT: MCCG TYPE K, NO LEAKAGE ONLY')
      IF(NREG.NE.8.OR.NUNKNO.NE.14.OR.NMAT.NE.8.OR.NGRP.NE.370)
     1 CALL XABORT('AXMAT SNAPSHOT: UNDECLARED SHAPE')
      IF(NIFIS.NE.32.OR.NLF.NE.1.OR.NLIN.NE.1.OR.NFUNL.NE.1)
     1 CALL XABORT('AXMAT SNAPSHOT: UNDECLARED MOMENTS')
      IF(LSCAL.OR.LEAKSW) CALL XABORT('AXMAT SNAPSHOT: CLOSED VECTOR')
      IF(EPSINR.NE.2.5E-7.OR.EPSUNK.NE.2.5E-7.OR.EPSOUT.NE.2.5E-7)
     1 CALL XABORT('AXMAT SNAPSHOT: UNDECLARED OUTER TOLERANCE')""")
    source = source.replace('CALL FLUSP64(JPSYS,NPSYS,IPTRK,IPRT', 'CALL AXMAT_MCCG_DOOR64(JPSYS,NPSYS,IPTRK,IFTRAK,IPRT')
    source = once(source, "IF((CXDOOR.EQ.'SPOT').AND.(ITYPEC.GE.2).AND.", "IF((CXDOOR.EQ.'MCCG').AND.(ITYPEC.GE.2).AND.")
    # Retain the existing k-update equation, but never demote the input field.
    for level, indent, cont in ((2,'         ','     2'),(3,'          ','     2')):
        before = indent+'ALLOCATE(FLX32(NUNKNO,NGRP))\n'+indent+f'FLX32(:NUNKNO,:NGRP)=REAL(FLUX(:NUNKNO,:NGRP,{level}))\n'+indent+'CALL FLUKEF'
        source = once(source, before, indent+'CALL AXMAT_FLUKEF64')
        before = f'IMERG,DIFHET,FLX32,B2,ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)\n{indent}DEALLOCATE(FLX32)'
        source = once(source, before, f'IMERG,DIFHET,FLUX(1,1,{level}),B2,ILEAK,LEAKSW,OLDBIL,AKEFF,AFLNOR)')
    source = once(source, 'TYPE(C_PTR) JPFLUX64', 'TYPE(C_PTR) JPFLUX64,JPSOUR64')
    source = once(source, "JPFLUX64=LCMLID(IPFLUX,'FLUX64',NGRP)", "JPFLUX64=LCMLID(IPFLUX,'FLUX64',NGRP)\n           JPSOUR64=LCMLID(IPFLUX,'SOUR64',NGRP)")
    source = once(source, 'CALL LCMPDL(JPSOUR,IG,NUNKNO,2,GAR32)', 'CALL LCMPDL(JPSOUR,IG,NUNKNO,2,GAR32)\n      CALL LCMPDL(JPSOUR64,IG,NUNKNO,4,FLUX(1,IG,4))')
    result['AXMAT_SNAPSHOT_DRIVER64.f'] = source
    source = (ROOT / 'src/FLUKEF.f').read_text()
    source = once(source, 'SUBROUTINE FLUKEF(', 'SUBROUTINE AXMAT_FLUKEF64(')
    source = once(source, 'DIFHET(NMERG,NGRP),FLUX(NUNKNO,NGRP),B2(4)', 'DIFHET(NMERG,NGRP),B2(4)\n      DOUBLE PRECISION FLUX(NUNKNO,NGRP)')
    result['AXMAT_FLUKEF64.f'] = source
    return result


def main():
    base = ROOT / 'validation/artifacts/axial-material-r64-first-call-20261003'
    manifest = json.loads(require_file(base / 'execution.json', '56f2187a292241568977cf0543c1a641359e4a7d60efc92387ec1c8560eb9e61').read_text())
    for name, wanted in manifest['files'].items():
        require_file(Path(name), wanted)
    observations = json.loads((base / 'independent_observations.json').read_text())
    if observations['classification'] != 'R64_FIRST_CALL_AND_NEGATIVE_CONTROLS_VERIFIED' or observations['double_passes'] != 370:
        raise ValueError('positive/negative controls must pass first')
    work = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-20261003'
    work.mkdir(exist_ok=False)
    for sub in ('build', 'runtime', 'A'):
        (work / sub).mkdir()
    for name in ('SPOASM.o', 'FLU.o', 'FLU2DR.o', 'FLU2DR64.o', 'SPOR64_A8.o', 'SPOR64_A8_ACA.o'):
        shutil.copy2(base / 'build' / name, work / 'build' / name)
    for p in (base / 'build').glob('*.mod'):
        shutil.copy2(p, work / 'build' / p.name)
    for p in (base / 'runtime').glob('*.py'):
        shutil.copy2(p, work / 'runtime' / p.name)
    for name in ('material.xsm', 'geometry.dat'):
        shutil.copy2(base / 'A' / name, work / 'A' / name)
    deck = (base / 'A/snapshot.x2m').read_text()
    deck = once(deck, 'UNKT 2.50000000E-07 THER 2.50000000E-07 ;', 'UNKT 2.50000000E-07 THER 2.50000000E-07 REBA OFF ;')
    (work / 'A/snapshot.x2m').write_text(deck)
    generated = sources()
    for name, contents in generated.items():
        (work / 'build' / name).write_text(contents)
        original = 'FLU2DR64.f' if name.startswith('AXMAT_SNAPSHOT') else 'FLUKEF.f' if name.startswith('AXMAT_FLUKEF') else name
        (work / 'build' / (name+'.patch')).write_text(''.join(difflib.unified_diff((ROOT/'src'/original).read_text().splitlines(True),contents.splitlines(True),fromfile=original,tofile=name)))
    shutil.copy2(Path(__file__).with_name('snapshot_r64_door.f90'), work / 'build/snapshot_r64_door.f90')
    flags = ['-O2','-march=native','-ffp-contract=off','-fcheck=all','-fbacktrace','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
             '-I'+str(work/'build'),'-I'+str(ROOT/'lib/Darwin_arm64/modules'),'-I'+str(ROOT/'Ganlib/lib/Darwin_arm64/modules'),'-J'+str(work/'build')]
    commands, objects = [], list((work/'build').glob('*.o'))
    for name in (*generated, 'snapshot_r64_door.f90'):
        p = work/'build'/name
        commands.append(['gfortran',*flags,'-c',str(p),'-o',str(p.with_suffix('.o'))])
        objects.append(p.with_suffix('.o'))
    libraries = [ROOT/'lib/Darwin_arm64/libDragon.a', ROOT/'Trivac/lib/Darwin_arm64/libTrivac.a',ROOT/'Utilib/lib/Darwin_arm64/libUtilib.a',ROOT/'Ganlib/lib/Darwin_arm64/libGanlib.a']
    commands.append(['gfortran','-O2','-ffp-contract=off',str(ROOT/'src/DRAGON.o'),*map(str,objects),*map(str,libraries),'-o',str(work/'runtime/Dragon')])
    protected = json.loads((base/'protocol.json').read_text())['protected_base']
    protocol = dict(schema='AXMAT_R64_SNAPSHOT_A_PROTOCOL_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),user_authorization='可以',
        scope='One fresh A-state snapshot from identical sealed material/geometry, using existing REAL64 radial and eigen iteration with REAL64 flux/source/k records. No automatic B, AAA or ABA execution.',wall_seconds=600,automatic_retries=0,threads=1,
        changes=['MCCG TYPE-K driver uses binary64 flux/source and same k-update equation; source coefficients remain their original binary32 data.',
                 'REBA OFF is explicitly required by the existing REAL64 outer driver; acceleration setting change, not a material/boundary change.',
                 'Original FLU tolerances 2.5e-7 and MCCG tolerance 2.5e-8 retained. Legacy binary32 records are mirrors, not certified inner terminals.'],
        acceptance='Normal native completion and fresh independent serialized-double terminal audit required before snapshot qualification. Physical/AAA gates unchanged.',
        prerequisite_probe_sha256=sha256(base/'independent_observations.json'),build_commands=commands,protected_base=protected,
        source_inputs={str(ROOT/'src'/n):sha256(ROOT/'src'/n) for n in ('FLUDRV.f','FLU2DR64.f','FLUKEF.f')})
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    files = {str(p):sha256(p) for p in work.rglob('*') if p.is_file()}
    files.update(protected); files.update(protocol['source_inputs'])
    files[str(Path(__file__).resolve())] = sha256(Path(__file__))
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__ == '__main__':
    main()
