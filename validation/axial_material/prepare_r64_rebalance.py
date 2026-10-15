"""Restore the native rebalancing step using the existing REAL64 implementation."""
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
    base=ROOT/'validation/artifacts/axial-material-r64-thermal-polish-20261003'
    manifest=json.loads(require_file(base/'execution.json','5625e3f442e4b82df04907bfcf23876f34df2007359c2d6994a5a2aacef5b00e').read_text())
    for name,wanted in manifest['files'].items():
        require_file(Path(name),wanted)
    status=json.loads((base/'run_status.json').read_text())
    if status['classification']!='FAILED_NO_RETRY' or not status['frozen_inputs_unchanged'] or 'TimeoutExpired' not in status['error']:
        raise ValueError('requires the preserved no-rebalance thermal contrast budget stop')
    work=ROOT/'validation/artifacts/axial-material-r64-rebalance-20261003'
    work.mkdir(exist_ok=False)
    for name in ('build','runtime','audit_build'):
        shutil.copytree(base/name,work/name,ignore=shutil.ignore_patterns('__pycache__','build.log','build_readonly_memory.log'))
    (work/'A').mkdir()
    for name in ('material.xsm','geometry.dat','seed_A.xsm'):
        shutil.copy2(base/'A'/name,work/'A'/name)
    (work/'A/snapshot.x2m').write_text(once((base/'A/snapshot.x2m').read_text(),'REBA OFF','REBA ON'))
    p=work/'build/AXMAT_SNAPSHOT_DRIVER64.f'
    source=p.read_text()
    source=once(source,"      IF(LREBAL) CALL XABORT('FLU2DR64: USE REBA OFF.')", "      IF(.NOT.LREBAL) CALL XABORT('AXMAT REBALANCE: REBA ON REQUIRED')")
    source=once(source,"         CALL XABORT('FLU2DR64: REBALANCE UNSUPPORTED.')", """         CALL AXMAT_BALANCE64(IPMACR,NGRP,ILEAK,NMAT,NREG,ICREB,
     1   NUNKNO,NANIS,MATCOD,VOL,KEYFLX(1,1,1),XSTRC,XSDIA,XCSOU,
     2   IGDEB,B2,NMERG,IMERG,DIFHET,KEYCUR,MATALB(NNN+1),ALBEDO,
     3   V(NNN+1),FLUX(1,1,7))""")
    p.write_text(source)
    (work/'build/rebalance-only.patch').write_text(''.join(difflib.unified_diff((base/'build/AXMAT_SNAPSHOT_DRIVER64.f').read_text().splitlines(True),source.splitlines(True),fromfile=str(base/'build/AXMAT_SNAPSHOT_DRIVER64.f'),tofile=str(p))))
    shutil.copy2(Path(__file__).with_name('snapshot_r64_balance.f90'),work/'build/snapshot_r64_balance.f90')
    previous=json.loads((base/'protocol.json').read_text())
    commands=[[arg.replace(str(base),str(work)) for arg in command] for command in previous['build_commands']]
    driver=commands[0]
    balance=[arg.replace('AXMAT_SNAPSHOT_DRIVER64.f','snapshot_r64_balance.f90').replace('AXMAT_SNAPSHOT_DRIVER64.o','snapshot_r64_balance.o') for arg in driver]
    commands.insert(0,balance)
    commands[2].insert(commands[2].index(str(ROOT/'lib/Darwin_arm64/libDragon.a')),str(work/'build/snapshot_r64_balance.o'))
    protocol=dict(schema='AXMAT_R64_REBALANCE_CONTRAST_V1',declared_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        scope='Restore the native REBA ON step through the already implemented SPOR64_A9.FLUBAL64, with a narrow macro-data bridge. Retain stricter work targets and original acceptance thresholds.',
        wall_seconds=600,automatic_retries=0,threads=1,
        acceptance='Normal executed completion and the unchanged independent bare-transport image/source/global-balance audit. A rebalanced outer PASS alone cannot qualify the saved snapshot.',
        predecessor_status_sha256=sha256(base/'run_status.json'),build_commands=commands,protected_base=previous['protected_base'],
        source_inputs={str(ROOT/'src/SPOR64_A9.f90'):sha256(ROOT/'src/SPOR64_A9.f90')})
    dump_json(work/'protocol.json',protocol)
    with (work/'build/build.log').open('xb') as log:
        for command in commands:
            subprocess.run(command,cwd=work/'build',check=True,stdout=log,stderr=subprocess.STDOUT,timeout=60)
    dump_json(work/'audit_build/build_command.json',commands[-1])
    (work/'audit_build/build_readonly_memory.log').write_bytes((work/'build/build.log').read_bytes())
    files=dict(manifest['files']);files.update(protocol['source_inputs'])
    files.update({str(p):sha256(p) for p in work.rglob('*') if p.is_file()})
    for p in (base/'run_status.json',Path(__file__).resolve(),Path(__file__).with_name('snapshot_r64_balance.f90').resolve()):
        files[str(p)]=sha256(p)
    dump_json(work/'execution.json',dict(schema='AXMAT_R64_SNAPSHOT_EXPERIMENT_V1',mode='snapshot_A',wall_seconds=600,automatic_retries=0,
        artifact_root=str(ROOT/'validation/artifacts'),resource_roots=sorted(str(p.resolve()) for p in (ROOT/'validation/artifacts').glob('axial-material-*') if p.is_dir()),files=files))
    print(sha256(work/'execution.json'))


if __name__=='__main__':
    main()
