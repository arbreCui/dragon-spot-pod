"""Separate bounded conditional white-trace native OFF/ON diagnostic.

The branch changes a declared approximate angular operator, not arithmetic.
It never fits CE, changes physical materials, produces a coupled map, or
qualifies AAA/ABA. Shared sources, executables and sealed inputs stay intact.
"""
import argparse
import csv
import difflib
import json
from pathlib import Path
import re
import shutil
import struct
import sys
import time

sys.dont_write_bytecode = True
import frozen_AAA_axial_sensitivities as base
import white_side_trace_kernel as model

ROOT, ART, PROD = base.ROOT, base.ART, base.PROD
OUT = ART / 'axial-material-AAA-white-trace-cold-control-paths-20261004'
CE = ART / 'axial-material-ce-qualified-AAA-long-generations-20261004/AAA'
ALGEBRA = ART / 'axial-material-AAA-white-trace-angular-model-20261004'
PRIOR = ART / 'axial-material-AAA-frozen-axial-sensitivities-20261004'
FLIGHT = ART / 'axial-material-AAA-compensated-flight-20261004'
CE_SHA = 'ac11a8edc48d0a288a41a37fe0f0c7ebdbec66317d49c63203f18e37c75337c6'
ALGEBRA_SHA = '8dee14347eea9d029e4053f7760aa8d1e5e7524df0a1fb502e0529e9b77d880e'


def require_file(path, expected, executable=False):
    return base.require_file(Path(path), expected, executable)


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('ambiguous native insertion anchor: ' + old[:70])
    return text.replace(old, new, 1)


def native_sources():
    original = (ROOT / 'src/SPOT1P64.f90').read_text()
    modified = replace_once(original, '  implicit none\n  integer, parameter :: dp=kind(1.0d0)',
        '''  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_ON,AXMAT_WHITE_ROW, &
    AXMAT_WHITE_PERIMETER,AXMAT_WHITE_KERNEL,AXMAT_WHITE_NOTE
  implicit none
  integer, parameter :: dp=kind(1.0d0)''')
    modified = replace_once(modified, '  integer :: npositive,nnegative,npair',
        '''  integer :: npositive,nnegative,npair,white_info
  double precision, allocatable :: white_angle(:,:),white_mode(:,:)''')
    modified = replace_once(modified, '  weight=real(vol2d,dp)/vtot', '''  weight=real(vol2d,dp)/vtot
  if (AXMAT_WHITE_ON) then
    if (nreg2d /= 8 .or. nfloor /= 12 .or. nsnap /= 3 .or. &
        nmode /= 1 .or. npq /= 8 .or. nsct /= 3 .or. &
        any(ncode /= 1) .or. any(zcode /= 0.0)) &
      call XABORT('AXMAT WHITE: OUTSIDE DECLARED RANK1 VACUUM SCOPE.')
    if (abs(vtot/(sqrt(3.0d0)*AXMAT_WHITE_PERIMETER**2/24.0d0)- &
        1.0d0) > 5.0d-6) &
      call XABORT('AXMAT WHITE: PHYSICAL AREA/PERIMETER MISMATCH.')
    allocate(white_angle(npq,npq),white_mode(nmode,nmode))
    call AXMAT_WHITE_KERNEL(real(du,dp),real(w,dp), &
      AXMAT_WHITE_PERIMETER,vtot,white_angle,white_info)
    if (white_info /= 0) call XABORT('AXMAT WHITE: INVALID ANGULAR KERNEL.')
    do b=1,nmode
      do a=1,nmode
        white_mode(a,b)=real(basis(AXMAT_WHITE_ROW,a),dp)* &
                       real(basis(AXMAT_WHITE_ROW,b),dp)
      enddo
    enddo
    call AXMAT_WHITE_NOTE(igroup,white_mode(1,1))
  endif''')
    modified = replace_once(modified,
        '              kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)',
        '''              kvalue=kvalue+mn(in,1)*radial_m(ia,ib,iz)*dn(1,jn)
              ! Conditional constant side trace: conservative angular exchange.
              if (AXMAT_WHITE_ON) kvalue=kvalue+ &
                white_mode(ia,ib)*white_angle(in,jn)''')
    yield 'SPOT1P64.f90', original, modified
    original = (ROOT / 'src/SPOF64.f').read_text()
    modified = replace_once(original, '      USE GANLIB',
        '      USE GANLIB\n      USE AXMAT_WHITE_TRACE_MOD, ONLY: AXMAT_WHITE_CONFIGURE')
    modified = replace_once(modified, '      INTEGER     IPAR(NSTATE),NCODE(2)',
        '''      INTEGER     IPAR(NSTATE),NCODE(2)
      INTEGER     WHITE_MARKER(4),WHITE_LEN,WHITE_KIND,WP_LEN,WP_KIND
      INTEGER     WHITE_INFO
      DOUBLE PRECISION WHITE_PERIMETER
      LOGICAL WHITE_ENABLE''')
    modified = replace_once(modified, "      IF(IPAR(4).GT.NMAT) CALL XABORT('SPOF: INVALID NMAT.')", '''      IF(IPAR(4).GT.NMAT) CALL XABORT('SPOF: INVALID NMAT.')
*     EXPLICIT, EXPERIMENT-SPECIFIC CONDITIONAL WHITE TRACE MARKER.
      CALL LCMLEN(IPTRK,'AXMAT-WHITE',WHITE_LEN,WHITE_KIND)
      CALL LCMLEN(IPTRK,'AXMAT-W-P',WP_LEN,WP_KIND)
      WHITE_MARKER=0
      WHITE_PERIMETER=0.0D0
      WHITE_ENABLE=(WHITE_LEN.NE.0.OR.WP_LEN.NE.0)
      IF(WHITE_ENABLE) THEN
        IF(WHITE_LEN.NE.4.OR.WHITE_KIND.NE.1.OR.
     1     WP_LEN.NE.1.OR.WP_KIND.NE.4) CALL XABORT(
     2    'AXMAT WHITE: PARTIAL OR MALFORMED TRACK MARKERS.')
        CALL LCMGET(IPTRK,'AXMAT-WHITE',WHITE_MARKER)
        CALL LCMGET(IPTRK,'AXMAT-W-P',WHITE_PERIMETER)
      ENDIF
      CALL AXMAT_WHITE_CONFIGURE(WHITE_ENABLE,WHITE_MARKER,
     1 WHITE_PERIMETER,NREG2D,NFLOOR,NSNAP,NLF,ISCAT,IELEM,WHITE_INFO)
      IF(WHITE_INFO.NE.0) CALL XABORT(
     1 'AXMAT WHITE: INVALID DECLARED CONFIGURATION.')''')
    yield 'SPOF64.f', original, modified


def prepare():
    info, final = base.prepared()
    spec=json.loads(Path(info['case_spec']['path']).read_text())
    if spec['geometry']['hex_edge_cm']!=.61776479:
        raise ValueError('fixed native side perimeter differs from original physical geometry')
    require_file(ART / 'axial-material-tools-20261003/export_observables',
        '81da2ac2ea98009181cc54a1ab254c99d1cb362b4e89c468fe7bc44ea14e7524',True)
    require_file(CE / 'execution.json', CE_SHA)
    require_file(ALGEBRA / 'declaration.json', ALGEBRA_SHA)
    old = json.loads((PRIOR / 'result.json').read_text())
    for name, sha in old['outputs'].items():
        require_file(PRIOR / name, sha)
    OUT.mkdir(exist_ok=False)
    for name in ('runtime', 'inputs', 'build', 'AAA', 'off', 'on', 'unit'):
        (OUT / name).mkdir()
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    original_files = []
    for name, original, modified in native_sources():
        (OUT / 'build' / name).write_text(modified)
        (OUT / 'build' / (name + '.patch')).write_text(''.join(difflib.unified_diff(
            original.splitlines(True), modified.splitlines(True), fromfile='shared-original', tofile='isolated-conditional-trace')))
        original_files.append(ROOT / 'src' / name)
    for name in ('axmat_white_trace_model.f90', 'axmat_white_trace_tracking.f90', 'axmat_white_trace_unit.f90'):
        shutil.copy2(Path(__file__).parent / name, OUT / 'build' / name)
        original_files.append(Path(__file__).parent / name)
    original_inputs = json.loads((PRIOR / 'execution.json').read_text())['inputs']
    for name, item in original_inputs.items():
        require_file(item['path'], item['sha256'])
        (OUT / 'inputs' / (name + '.xsm')).symlink_to(Path(item['path']).resolve())
    for case in ('off', 'on'):
        shutil.copy2(PRIOR / 'cold12_sn8/system.xsm', OUT / case / 'system.xsm')
        shutil.copy2(PRIOR / 'cold12_sn8/track.xsm', OUT / case / ('track.xsm' if case == 'off' else 'base_track.xsm'))
        (OUT / case / 'solve.x2m').write_text(base.SOLVE)
    compiler = Path(shutil.which('gfortran')).resolve()
    libs = [ROOT / 'lib/Darwin_arm64/libDragon.a', ROOT / 'Trivac/lib/Darwin_arm64/libTrivac.a',
        ROOT / 'Utilib/lib/Darwin_arm64/libUtilib.a', ROOT / 'Ganlib/lib/Darwin_arm64/libGanlib.a']
    flags = ['-O2','-march=native','-ffp-contract=off','-g','-fPIC','-frecord-marker=4','-ffixed-line-length-none',
        '-I'+str(OUT / 'build'), '-I'+str(ROOT / 'lib/Darwin_arm64/modules'),
        '-I'+str(ROOT / 'Ganlib/lib/Darwin_arm64/modules'), '-J'+str(OUT / 'build')]
    commands = []
    for name in ('axmat_white_trace_model.f90','SPOT1P64.f90','SPOF64.f',
                 'axmat_white_trace_tracking.f90','axmat_white_trace_unit.f90'):
        source = OUT / 'build' / name
        commands.append([str(compiler), *flags, '-c', str(source), '-o', str(source.with_suffix('.o'))])
    model_obj = OUT / 'build/axmat_white_trace_model.o'
    for name, binary in [('axmat_white_trace_tracking','tracking'),('axmat_white_trace_unit','unit')]:
        commands.append([str(compiler), *flags, str(OUT / 'build' / (name + '.o')), str(model_obj),
            str(libs[2]),str(libs[3]),'-o',str(OUT / 'runtime' / binary)])
    commands.append([str(compiler),'-O2','-march=native','-ffp-contract=off','-g',str(ROOT / 'src/DRAGON.o'),
        str(FLIGHT / 'build/SPOR64_A8.o'),str(FLIGHT / 'build/AXMAT_MCGFCF_COMP.o'),str(model_obj),
        str(OUT / 'build/SPOT1P64.o'),str(OUT / 'build/SPOF64.o'),*map(str,libs),'-o',str(OUT / 'runtime/Dragon')])
    files = [Path(__file__).resolve(),Path(base.__file__),Path(model.__file__),
        ROOT / 'validation/axial_material/prepare_AAA_white_trace_cold_control.py',
        ART / 'axial-material-AAA-white-trace-cold-control-20261004/preparation_rejection.json',
        *original_files,compiler,*libs,
        ROOT / 'src/DRAGON.o',ROOT / 'Ganlib/lib/Darwin_arm64/modules/ganlib.mod',
        FLIGHT / 'build/SPOR64_A8.o',FLIGHT / 'build/AXMAT_MCGFCF_COMP.o',FLIGHT / 'execution.json',
        PROD / 'prepared.json',PROD / 'AAA/run_status.json',Path(info['case_spec']['path']),
        CE / 'execution.json',CE / 'run_claim.json',ALGEBRA / 'declaration.json',
        PRIOR / 'execution.json',PRIOR / 'result.json',PRIOR / 'cold12_sn8/observables.summary.txt',
        PRIOR / 'cold12_sn8/observables.regions.csv',PRIOR / 'cold12_sn8/axial.xsm',
        PRIOR / 'cold12_sn8/track.xsm',PRIOR / 'cold12_sn8/system.xsm',
        ART / 'axial-material-tools-20261003/export_observables',ROOT / 'validation/axial_material/export_observables.f90',
        *[Path(v['path']) for v in original_inputs.values()],
        *[Path(__import__(m).__file__) for m in ('production_runner','snapshot_control_preflight','qualified_snapshot_ingestion')],
        *[p for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()]]
    base.write_new(OUT / 'declaration.json',dict(schema='AXMAT_CONDITIONAL_WHITE_TRACE_COLD_NATIVE_CONTROL_V1',
        declared_unix=time.time(),files={str(p.resolve()):base.digest(p) for p in files},
        current_ce_manifest_sha256=CE_SHA,white_algebra_declaration_sha256=ALGEBRA_SHA,build_commands=commands,
        wall_seconds=1080,stage_caps=dict(build=60,unit=60,tracking=60,axial=300,export=60),
        threads=1,numeric_children_at_once=1,retries=0,artifact_budget_bytes=24*2**30,min_free_bytes=8*2**30,
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()),
        source_gate='The specific ordinary CE native run must be terminal, and the frozen independent white angular algebra audit must PASS before any compiler or native child.',
        conditional_model='Uniform transverse azimuth and a regionwise constant side trace equal to the outer sodium basis row. Conservative P/(pi*A)*sqrt(1-mu^2) angular exchange; common rank1 weak projection B_boundary^T K B_boundary. Geometry fixes P=6*0.61776479 cm; no fitted multiplier.',
        physical_inputs_unchanged=True,original_inner_and_engineering_gates_changed=False,
        ideal_angular_operator_changed=True,shared_solver_promoted=False,
        scope='Only two cold axial solves with the same frozen final AAA radial operator and common basis. OFF compatibility first, then ON diagnostic. No new radial solve, training, full coupled map, boundary-trace measurement, or AAA/ABA accuracy qualification.',
        off_compatibility=dict(relative_k=5e-8,max_relative_scalar_group_flux=5e-8,
            requirement='Actual saved positive REAL64 group scalar flux normalized by one global nu-fission total; match the prior successful native cold12 SN8 baseline at original 5e-8 inner precision. No ON solve if it fails.'),
        on_admission='Every inherited TRACK record byte-exact, only two new markers; same system bytes and all 3330 radial/basis records; actual native branch must log all 370 positive basis trace factors. Original native inner/outer terminals, REAL64 authority, positivity and signed-current telescoping screens apply.',
        native_matrix_comparison='Actual compiled module matrix on saved SN8 quadrature vs independent frozen Python model at 128*eps64*infinity norm; seven malformed native inputs reject.',
        decision='Report sensitivity and conservative angular-model implementation only. Do not attribute the CE gap, promote the solver, select a coefficient, or admit ABA from this result.'))
    print(json.dumps(dict(status='PREDECLARED_NO_BUILD_OR_TRANSPORT',declaration=base.pin(OUT / 'declaration.json')),indent=2))


def read_declaration(expected):
    require_file(OUT / 'declaration.json', expected)
    value=json.loads((OUT / 'declaration.json').read_text())
    for name, wanted in value['files'].items(): require_file(name,wanted)
    base.prepared()
    claim=json.loads((CE / 'run_claim.json').read_text())
    native=json.loads((CE / 'native_result.json').read_text())
    if claim['manifest_sha256']!=CE_SHA or native['returncode'] is None:
        raise ValueError('specific long-generation CE is not terminal')
    algebra=json.loads((ALGEBRA / 'result.json').read_text())
    driver=json.loads((ALGEBRA / 'driver_result.json').read_text())
    if algebra['classification']!='PASS_CONDITIONAL_WHITE_TRACE_ANGULAR_ALGEBRA_ONLY' or driver['declaration_sha256']!=ALGEBRA_SHA or driver['status']!='COMPLETE_BOUNDED_ALGEBRA_ONLY':
        raise ValueError('frozen independent white angular algebra did not pass')
    for name,wanted in json.loads((ALGEBRA / 'declaration.json').read_text())['files'].items():require_file(name,wanted)
    require_file(driver['result']['path'],driver['result']['sha256'])
    return value


def exact_track_copy():
    """Recurse through inherited directories/lists and compare raw record words."""
    count=0
    with base._open_xsm(OUT / 'on/base_track.xsm') as old, base._open_xsm(OUT / 'on/track.xsm') as new:
        def walk(previous, actual, root=False):
            nonlocal count
            additions={'AXMAT-WHITE','AXMAT-W-P'} if root else set()
            if set(actual)!=set(previous)|additions:raise ValueError('TRACK record names changed')
            for name,p in previous.items():
                n=actual[name]
                if p[1:]!=n[1:]:raise ValueError('TRACK record kind/length changed: '+name)
                if p[2]==0:
                    walk(old.directory(p[0]),new.directory(n[0]))
                elif p[2]==10:
                    po=old.integers(p[0],p[1]);pn=new.integers(n[0],n[1])
                    for a,b in zip(po,pn,strict=True):walk(old.directory(a),new.directory(b))
                else:
                    if old.read(p[0],p[1])!=new.read(n[0],n[1]):raise ValueError('TRACK inherited record changed: '+name)
                    count+=1
        walk(old.root,new.root,True)
        if new.record(new.root,'AXMAT-WHITE',4,1)!=struct.pack('<4i',1,1,8,3):raise ValueError('wrong marker')
        if new.record(new.root,'AXMAT-W-P',2,4)!=struct.pack('<d',6*.61776479):raise ValueError('wrong perimeter')
    return dict(status='PASS_COMPLETE_INHERITED_TRACK_COPY',inherited_records=count,new_records=2)


def kernel_receipt():
    import numpy as np
    with base._open_xsm(OUT / 'off/track.xsm') as tr:
        mu=base.field(tr,tr.root,'U','<f4').astype(float);w=base.field(tr,tr.root,'W','<f4').astype(float)
        area=float(base.field(tr,tr.root,'AREA2D','<f4').astype(float).sum())
    matrix=np.full((8,8),np.nan)
    rows=list(csv.DictReader((OUT / 'unit/kernel.csv').open()))
    if len(rows)!=64:raise ValueError('incomplete native kernel')
    for row in rows:
        i,j=int(row['row'])-1,int(row['column'])-1
        if not(0<=i<8 and 0<=j<8) or np.isfinite(matrix[i,j]):raise ValueError('duplicate/outside kernel entry')
        matrix[i,j]=float(row['value'])
    expected=model.trace_exchange(mu,w,6*.61776479,area)
    tolerance=128*np.finfo(float).eps*np.linalg.norm(expected,np.inf)
    error=float(np.max(abs(matrix-expected)))
    if not np.isfinite(matrix).all() or error>tolerance:raise ValueError('native/Python angular matrix mismatch')
    if 'negative_controls_rejected=7' not in (OUT / 'unit/native.log').read_text().splitlines():raise ValueError('native malformed controls incomplete')
    return dict(status='PASS_COMPILED_WHITE_KERNEL_ONLY',max_absolute_difference=error,roundoff_bound=tolerance,
        negative_controls_rejected=7,matrix=base.pin(OUT / 'unit/kernel.csv'))


def state(folder):
    import numpy as np
    summary={line.split('=',1)[0]:float(line.split('=',1)[1]) for line in (folder / 'observables.summary.txt').read_text().splitlines() if '=' in line}
    if summary['nonpositive_scalar_entries']!=0 or summary['negative_outward_end_region_group_currents']!=0 or summary['current_telescoping_difference']!=0:
        raise ValueError('saved scalar/current admission failed')
    with base._open_xsm(folder / 'axial.xsm') as a:
        k=base.field(a,a.root,'SPOT-KEFF64','<f8');tag=base.field(a,a.root,'SPOT-X-KEFF','<f8')
        if len(k)!=1 or k[0]<=0 or not np.array_equal(k,tag) or k[0]!=summary['k64']:
            raise ValueError('saved REAL64 eigenvalue authority differs')
    # Read actual saved group scalars by the complete native KEYFLX mapping.
    # The existing regional exporter deliberately sums over energy groups.
    with base._open_xsm(folder / 'track.xsm') as track:
        keys=base.field(track,track.root,'KEYFLX','<i4')
        dimensions=base.field(track,track.root,'STATE-VECTOR','<i4')
        if len(keys)!=96 or len(set(keys.tolist()))!=96 or dimensions[1]!=456 or np.any(keys<1) or np.any(keys>dimensions[10]):
            raise ValueError('invalid original native scalar mapping')
    groups=[]
    with base._open_xsm(folder / 'axial.xsm') as a:
        for item in base.list_handles(a,a.root,'FLUX64',370):
            if item[1:]!=(912,4):raise ValueError('incomplete REAL64 group layout')
            vector=np.frombuffer(a.read(item[0],item[1]),'<f8')
            groups.append(vector[keys-1])
    phi=np.array(groups).reshape(-1)
    if len(phi)!=8*12*370:raise ValueError('incomplete group field')
    if not np.isfinite(phi).all() or np.any(phi<=0):raise ValueError('nonpositive scalar group field')
    return summary,phi/summary['global_nufission']


def compare_states(actual, prior):
    import numpy as np
    a,pa=state(actual);b,pb=state(prior)
    if pa.shape!=pb.shape:raise ValueError('changed comparison layout')
    return dict(k64=a['k64'],reactivity_difference_pcm=1e5*(1/b['k64']-1/a['k64']),
        relative_k=abs(a['k64']/b['k64']-1),max_relative_scalar_group_flux=float(np.max(abs(pa/pb-1))),
        escape_per_nufission=a['escape_per_nufission'])


def apply_receipt(text):
    import numpy as np
    rows=re.findall(r'^AXMAT-WHITE-APPLY GROUP=(\d+) TRACE-FACTOR=\s*(\S+)\s*$',text,re.M)
    factors={int(g):float(v) for g,v in rows}
    if len(rows)!=370 or set(factors)!=set(range(1,371)):raise ValueError('missing/duplicate native white branch group')
    with base._open_xsm(OUT / 'on/system.xsm') as a:
        for group,h in enumerate(base.list_handles(a,a.root,'GROUP',370),1):
            directory=a.directory(h[0]);b=base.field(a,directory,'POD-BASIS','<f4').astype(float)
            nmode=base.field(a,directory,'POD-NMODE','<i4')
            expected=float(b[0]**2)
            if nmode.tolist()!=[1] or len(b)!=8 or abs(factors[group]/expected-1)>128*np.finfo(float).eps:
                raise ValueError('actual native projected trace differs')
    return dict(status='PASS_ALL_370_NATIVE_BRANCH_GROUPS',groups=370,trace_factor_range=[min(factors.values()),max(factors.values())])


def run(expected):
    declaration=read_declaration(expected)
    if (OUT / 'run_claim.json').exists():raise ValueError('no repeat or retry')
    base.write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time(),
        ce_terminal=base.pin(CE / 'native_result.json'),white_algebra=base.pin(ALGEBRA / 'driver_result.json')))
    resources=base.DiskResources(ART,declaration['resource_roots'],declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    runner=base.SerialExecutor(OUT,declaration['wall_seconds'],'AAA',resources)
    result=dict(classification='FAILED_CONDITIONAL_WHITE_TRACE_NATIVE_NO_RETRY',error=None,completed_cases=[],
        AAA_accuracy_qualified=False,ABA_admitted=False,shared_solver_promoted=False)
    started=time.monotonic()
    base.OUT=OUT
    try:
        for i,command in enumerate(declaration['build_commands']):runner.execute(OUT / 'build','build'+str(i+1),command,60)
        base.write_new(OUT / 'build_identity.json',dict(binaries={name:base.pin(OUT / 'runtime' / name) for name in ('Dragon','tracking','unit')},
            declaration_sha256=expected,shared_files_changed=False))
        runner.execute(OUT / 'unit','native',[str(OUT / 'runtime/unit'),'../off/track.xsm'],60,'AXMAT-WHITE-NATIVE-UNIT-COMPLETE')
        result['compiled_kernel']=kernel_receipt()
        base.write_new(OUT / 'kernel_receipt.json',result['compiled_kernel'])
        for case in ('off','on'):
            folder=OUT / case
            if case=='on':
                runner.execute(folder,'tracking',[str(OUT / 'runtime/tracking'),'base_track.xsm','track.xsm'],60,'AXMAT-WHITE-TRACKING-COMPLETE')
                result['tracking_copy']=exact_track_copy()
            if base.digest(folder / 'system.xsm')!=base.digest(PRIOR / 'cold12_sn8/system.xsm'):raise ValueError('frozen SYSTEM copy changed')
            result[case+'_structure']=base.structure(folder,12,8)
            text=runner.execute(folder,'solve',[str(OUT / 'runtime/Dragon')],300,'AXMAT-FROZEN-AXIAL-COMPLETE','solve.x2m')
            base.check_terminal(text)
            if case=='off' and 'AXMAT-WHITE-APPLY' in text:raise ValueError('white branch enabled in OFF control')
            if case=='on':result['native_application']=apply_receipt(text)
            runner.execute(folder,'export',[str(ART / 'axial-material-tools-20261003/export_observables'),
                'track.xsm','axial.xsm','../inputs/macro.xsm','observables'],60)
            if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in (folder / 'export.log').read_text().splitlines()):raise ValueError('native export marker missing')
            state(folder)
            result['completed_cases'].append(case)
            if case=='off':
                comparison=compare_states(folder,PRIOR / 'cold12_sn8')
                if any(comparison[key]>declaration['off_compatibility'][key] for key in ('relative_k','max_relative_scalar_group_flux')):
                    raise ValueError('OFF native compatibility failed; ON must not launch')
                result['off_compatibility']=dict(status='PASS_ORIGINAL_INNER_PRECISION',**comparison)
                base.write_new(OUT / 'off_compatibility.json',result['off_compatibility'])
        result['on_vs_off']=compare_states(OUT / 'on',OUT / 'off')
        result['classification']='COMPLETE_CONDITIONAL_WHITE_TRACE_COLD_SENSITIVITY_ONLY'
    except BaseException as exc:
        result['error']=repr(exc)
        raise
    finally:
        for name,wanted in declaration['files'].items():
            if base.digest(name)!=wanted:result.update(classification='INPUT_CHANGED',error='changed: '+name)
        result['elapsed_seconds']=time.monotonic()-started
        result['resources']=resources.check()
        result['outputs']={str(p.relative_to(OUT)):base.digest(p) for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()
            and p.name not in ('declaration.json','run_claim.json','result.json')}
        base.write_new(OUT / 'result.json',result)
    print(json.dumps({key:value for key,value in result.items() if key not in ('outputs','resources')},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run'));parser.add_argument('--sha256')
    args=parser.parse_args()
    prepare() if args.action=='prepare' else run(args.sha256)
