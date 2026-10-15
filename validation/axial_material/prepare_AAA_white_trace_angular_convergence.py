"""Bounded SN8/16/32 cold convergence study at the same 48-cell axial mesh.

Reuse the completed SN8 state. Only two new angular-order solves are allowed.
This does not establish a coupled fixed point or independent accuracy.
"""
import argparse
import csv
import difflib
import inspect
import json
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True
import prepare_AAA_white_trace_mesh_convergence as mesh

ROOT, ART, PROD, CE = mesh.ROOT, mesh.ART, mesh.PROD, mesh.CE
MESH = mesh.OUT
CLOSEOUT = ART / 'axial-material-AAA-white-trace-mesh-closeout-20261005'
OUT = ART / 'axial-material-AAA-white-trace-angular-convergence-20261005'
CASES = [('cold48_sn16', 48, 16, 3600), ('cold48_sn32', 48, 32, 9600)]
MESH_RESULT_SHA = '821d500a67fbff6acac4a1f0d9ec604157b3f21fb14436357b6c126da5cefdcc'
CLOSEOUT_SEAL_SHA = 'a0bd7c8d7d53e76be1086ee5c2183db0a79dc48f836d95c2a0d867f27550cf2e'


def read(path):
    return json.loads(Path(path).read_text())


def ready():
    info, final = mesh.ready()
    mesh.require_file(MESH / 'result.json', MESH_RESULT_SHA)
    result = read(MESH / 'result.json')
    declaration = read(MESH / 'declaration.json')
    if (result['classification'] != 'COMPLETE_WHITE_TRACE_FROZEN_MESH_SENSITIVITY_ONLY'
            or result['error'] is not None or result['completed_cases'] != [x[0] for x in mesh.CASES]
            or result['elapsed_seconds'] > declaration['total_wall_seconds']):
        raise ValueError('complete original bounded mesh convergence study required')
    for name, wanted in declaration['files'].items():
        mesh.require_file(Path(name), wanted)
    for name, wanted in result['outputs'].items():
        mesh.require_file(MESH / name, wanted)
    mesh.require_file(CLOSEOUT / 'seal.json', CLOSEOUT_SEAL_SHA)
    for name, wanted in read(CLOSEOUT / 'seal.json')['files'].items():
        mesh.require_file(CLOSEOUT / name, wanted)
    if read(CLOSEOUT / 'result.json')['classification'] != 'COMPLETE_COLD_MESH_CLOSEOUT_UNQUALIFIED':
        raise ValueError('completed cold-only closeout required')
    return info, final


def source_copy(name, replacements, proofs):
    original = (MESH / 'build' / name).read_text()
    changed = original
    for old, new in replacements:
        changed = mesh.replace_once(changed, old, new)
    restored = changed
    for old, new in reversed(replacements):
        restored = mesh.replace_once(restored, new, old)
    if restored != original:
        raise ValueError('native source changed outside declared numerical scope')
    path = OUT / 'build' / name
    path.write_text(changed)
    path.with_suffix(path.suffix+'.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), changed.splitlines(True),
        fromfile='frozen-SN8-mesh-study', tofile='isolated-SN8-16-32-controls')))
    proofs[name] = dict(original=mesh.base.pin(MESH / 'build' / name),
        candidate=mesh.base.pin(path), replacements=replacements,
        full_text_restored_exactly=True)


def prepare():
    info, final = ready()
    OUT.mkdir(exist_ok=False)
    for name in ('runtime','inputs','build','unit','AAA'):
        (OUT / name).mkdir()
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    inputs = {name:Path(item['path']) for name,item in read(MESH / 'declaration.json')['inputs'].items()}
    for name,path in inputs.items():
        (OUT / 'inputs' / (name+'.xsm')).symlink_to(path.resolve())
    proofs = {}
    source_copy('SPOT1P64.f90', [('nmode /= 1 .or. npq /= 8 .or. nsct /= 3',
        'nmode /= 1 .or. all(npq /= [8,16,32]) .or. nsct /= 3')], proofs)
    source_copy('axmat_white_trace_model.f90', [('nlf /= 8 .or. iscat /= 3 .or. ielem /= 1',
        'all(nlf /= [8,16,32]) .or. iscat /= 3 .or. ielem /= 1')], proofs)
    shutil.copy2(MESH / 'build/axmat_white_trace_tracking.f90', OUT / 'build/axmat_white_trace_tracking.f90')
    source_copy('axmat_white_trace_unit.f90', [
        ('  real :: mu32(8),w32(8),areas32(8)',
         '  real :: areas32(8)\n  real, allocatable :: mu32(:),w32(:)'),
        ('  double precision :: mu(8),w(8),matrix(8,8),p,area,bad_mu(8),bad_w(8)',
         '  double precision :: p,area\n  double precision, allocatable :: mu(:),w(:),matrix(:,:),bad_mu(:),bad_w(:)'),
        ('  integer :: info,i,j,marker(4),negative_controls',
         '  integer :: info,i,j,marker(4),negative_controls,nlf,state(40),length,kind,nz,sn'),
        ("  call LCMGET(track,'U',mu32)",
         "  call LCMGET(track,'STATE-VECTOR',state)\n  nlf=state(15)\n"
         "  if (all(nlf /= [8,16,32])) call XABORT('AXMAT WHITE UNIT: UNDECLARED SN ORDER.')\n"
         "  call LCMLEN(track,'U',length,kind)\n"
         "  if (length /= nlf .or. kind /= 2) call XABORT('AXMAT WHITE UNIT: INVALID COSINE RECORD.')\n"
         "  call LCMLEN(track,'W',length,kind)\n"
         "  if (length /= nlf .or. kind /= 2) call XABORT('AXMAT WHITE UNIT: INVALID WEIGHT RECORD.')\n"
         "  allocate(mu32(nlf),w32(nlf),mu(nlf),w(nlf),matrix(nlf,nlf),bad_mu(nlf),bad_w(nlf))\n"
         "  call LCMGET(track,'U',mu32)"),
        ('  do i=1,8','  do i=1,nlf'), ('    do j=1,8','    do j=1,nlf'),
        ("  if (negative_controls /= 7) call XABORT('AXMAT WHITE UNIT: INCOMPLETE NEGATIVE CONTROLS.')",
         "  marker=[1,1,8,3]\n  do nz=12,48,12\n"
         "    if (nz == 36) cycle\n    do sn=8,32,8\n      if (sn == 24) cycle\n"
         "      call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,nz,3,sn,3,1,info)\n"
         "      if (info /= 0) call XABORT('AXMAT WHITE UNIT: DECLARED MESH/ANGLE SCOPE REJECTED.')\n"
         "    enddo\n  enddo\n"
         "  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,48,3,12,3,1,info)\n  call rejected()\n"
         "  if (negative_controls /= 8) call XABORT('AXMAT WHITE UNIT: INCOMPLETE NEGATIVE CONTROLS.')")], proofs)
    original_saved = inspect.getsource(mesh.saved_state)
    saved = mesh.replace_once(original_saved, 'def saved_state(folder, nz, balance):',
        'def saved_state(folder, nz, sn, balance):')
    saved = mesh.replace_once(saved, 'nunk != 8*(4*nz+9)', 'nunk != 8*(4*nz+1+sn)')
    if saved.replace('nunk != 8*(4*nz+1+sn)', 'nunk != 8*(4*nz+9)').replace(
            'def saved_state(folder, nz, sn, balance):', 'def saved_state(folder, nz, balance):') != original_saved:
        raise ValueError('saved-field verifier changed beyond explicit angular storage word')
    (OUT / 'runtime/saved_field_verifier.py').write_text(
        'import json\nfrom prepare_AAA_white_trace_mesh_convergence import base\n\n'+saved)
    admissions = {}
    original_host = (PROD / 'runtime/white_receiver_tracking.py').read_text()
    original_basis = inputs['basis'].read_bytes()
    with mesh.base._open_xsm(inputs['basis']) as archive:
        entry = archive.root['STATE-VECTOR']
    for case,nz,sn,cap in CASES:
        folder = OUT / case
        folder.mkdir()
        (folder / 'unit').mkdir()
        adapted, receipt = mesh.metadata.adapt_bytes(original_basis, entry, 8*(4*nz+1+sn))
        with (folder / 'basis.xsm').open('xb') as stream:
            stream.write(adapted)
        deck = mesh.base.build_deck(nz, sn).replace("FILE '../inputs/basis.xsm'", "FILE './basis.xsm'")
        (folder / 'build.x2m').write_text(deck.replace("FILE './track.xsm'", "FILE './unmarked_track.xsm'"))
        (folder / 'solve.x2m').write_text(mesh.base.SOLVE)
        host = mesh.replace_once(original_host, '!=(8,12,3,1,8,3)', f'!=(8,{nz},3,1,{sn},3)')
        if mesh.replace_once(host, f'!=(8,{nz},3,1,{sn},3)', '!=(8,12,3,1,8,3)') != original_host:
            raise ValueError('tracking verifier changed outside declared numerical dimensions')
        (folder / 'verify_tracking.py').write_text(host)
        shutil.copy2(MESH / 'cold48_sn8/production_rules.json', folder / 'production_rules.json')
        admissions[case] = dict(**receipt, sn=sn, axial_cells=nz, axial_wall_seconds=cap,
            original=mesh.base.pin(inputs['basis']), adapted=mesh.base.pin(folder / 'basis.xsm'),
            production_rules_byte_exact=mesh.base.digest(folder / 'production_rules.json') ==
                                       mesh.base.digest(MESH / 'cold48_sn8/production_rules.json'))
    mesh.base.write_new(OUT / 'source_and_layout_admission.json', dict(
        status='PASS_DECLARED_ANGULAR_NUMERICAL_SCOPE_ONLY', source_changes=proofs,
        layouts=admissions, native_kernel_formula_changed=False, shared_sources_changed=False,
        scalar_verifier_only_explicit_sn_argument_and_storage_word_changed=True,
        reused_SN8_without_transport=mesh.base.pin(MESH / 'cold48_sn8/saved_state_admission.json')))
    old = read(MESH / 'declaration.json')
    commands = [[word.replace(str(MESH), str(OUT)) for word in command] for command in old['build_commands']]
    files = dict(old['files'])
    files.update({str(MESH / name):wanted for name,wanted in read(MESH / 'result.json')['outputs'].items()})
    extras = [Path(__file__).resolve(), Path(mesh.__file__).resolve(), MESH / 'declaration.json',
        MESH / 'run_claim.json', MESH / 'result.json', CLOSEOUT / 'seal.json',
        *[CLOSEOUT / name for name in read(CLOSEOUT / 'seal.json')['files']],
        *[p for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()]]
    files.update({str(p.resolve()):mesh.base.digest(p) for p in extras})
    roots = sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    resources = mesh.DiskResources(ART, roots, 8*2**30, 40*2**30)
    before = resources.check()
    forecast = before['artifact_bytes']+512*2**20
    if forecast > 40*2**30:
        raise ValueError('512 MiB angular-study reservation exceeds unchanged history cap')
    mesh.base.write_new(OUT / 'declaration.json', dict(
        schema='AXMAT_WHITE_TRACE_FROZEN_48_CELL_ANGULAR_CONVERGENCE_V1',
        declared_unix=time.time(), files=files, inputs={n:mesh.base.pin(p) for n,p in inputs.items()},
        build_commands=commands, cases=[dict(name=c,axial_cells=nz,sn=sn,axial_wall_seconds=cap)
            for c,nz,sn,cap in CASES], reused_baseline=str(MESH / 'cold48_sn8'),
        total_wall_seconds=14400, stage_caps=dict(build=60,unit=60,assembly=120,tracking=60,export=60),
        threads=1, numeric_children_at_once=1, retries=0,
        artifact_budget_bytes=40*2**30, min_free_bytes=8*2**30, resource_roots=roots,
        resources_before=before, storage_forecast_bytes=forecast,
        physical_inputs_changed=False, original_inner_and_accuracy_gates_changed=False,
        kernel_formula_changed=False, shared_solver_promoted=False,
        scope='Same 48 cells, three 50 cm physical zones, same final radial operator and common rank1 basis. '
              'Reuse actual complete SN8 state; execute only SN16 and SN32 cold axial solves. '
              'Only isolated SN scope guards and one fixed-package storage word change. '
              'All 3330 frozen radial/basis records must match before each solve. '
              'Actual compiled SN8 matrix must be byte-identical; all three compiled matrices must match '
              'the same declared analytic formula and conservation/PSD properties before transport.',
        negative_controls='Preserve all seven original malformed controls; add undeclared SN12 rejection. '
                          'Positive exact 12/24/48 by SN8/16/32 configuration controls.',
        bounds_basis='Completed 48/SN8 took 379.341 seconds. 3600/9600-second child caps conservatively '
                     'cover increased dense angular block cost; the total four-hour cap is fixed before compilation. '
                     'No retries, parallel solves, optional stopping or modified sealed earlier caps.',
        comparison='Conservatively sum every four complete fine-cell integrals into each original 12-cell bin. '
                   'Use one global nu-fission denominator per state. Report SN8-to-16 and SN16-to-32 '
                   'internal numerical changes and CE saved means diagnostically, with no new accuracy classification.',
        decision='Numerical convergence diagnostics only. No CE-fit coefficient, local normalization, '
                 'end-cell removal, coupled fixed-point claim, independent accuracy qualification or ABA admission. '
                 'Full coupling and all original independent gates remain required.'))
    print(json.dumps(dict(status='PREDECLARED_TWO_COLD_ANGULAR_SOLVES_BASELINE_REUSED',
        declaration=mesh.base.pin(OUT / 'declaration.json')), indent=2))


def compiled_kernel(folder, track_path, sn, baseline=False):
    import numpy as np
    with mesh.base._open_xsm(track_path) as track:
        mu = mesh.base.field(track,track.root,'U','<f4').astype(float)
        w = mesh.base.field(track,track.root,'W','<f4').astype(float)
        area = float(mesh.base.field(track,track.root,'AREA2D','<f4').astype(float).sum())
    if mu.size != sn or w.size != sn:
        raise ValueError('actual complete declared angular grid required')
    for i in range(sn):
        partner = np.flatnonzero(mu == -mu[i])
        if len(partner) != 1 or w[partner[0]] != w[i]:
            raise ValueError('actual quadrature exact opposite/weight pair absent')
    matrix = np.full((sn,sn), np.nan)
    rows = list(csv.DictReader((folder / 'kernel.csv').open()))
    if len(rows) != sn*sn:
        raise ValueError('complete compiled angular matrix required')
    for row in rows:
        i,j = int(row['row'])-1,int(row['column'])-1
        if not (0 <= i < sn and 0 <= j < sn) or np.isfinite(matrix[i,j]):
            raise ValueError('duplicate or outside compiled matrix entry')
        matrix[i,j] = float(row['value'])
    expected = mesh.model.trace_exchange(mu,w,6*.61776479,area)
    tolerance = 128*np.finfo(float).eps*np.linalg.norm(expected,np.inf)
    error = float(np.max(abs(matrix-expected)))
    if not np.isfinite(matrix).all() or error > tolerance:
        raise ValueError('actual native matrix differs from unchanged formula')
    weighted = w[:,None]*matrix
    similarity = np.sqrt(w)[:,None]*matrix/np.sqrt(w)[None,:]
    properties = dict(isotropic_null=float(np.max(abs(matrix@np.ones(sn)))),
        weighted_conservation=float(np.max(abs(w@matrix))),
        weighted_symmetry=float(np.max(abs(weighted-weighted.T))),
        similarity_symmetry=float(np.max(abs(similarity-similarity.T))),
        minimum_symmetric_eigenvalue=float(np.linalg.eigvalsh((similarity+similarity.T)/2).min()))
    if any(properties[k] > tolerance for k in properties if k != 'minimum_symmetric_eigenvalue') or properties['minimum_symmetric_eigenvalue'] < -tolerance:
        raise ValueError('compiled kernel failed original conservative PSD model properties')
    if 'negative_controls_rejected=8' not in (folder / 'native.log').read_text().splitlines():
        raise ValueError('all eight actual malformed controls must pass')
    if baseline and mesh.base.digest(folder / 'kernel.csv') != mesh.base.digest(MESH / 'unit/kernel.csv'):
        raise ValueError('compiled original SN8 matrix changed')
    return dict(status='PASS_COMPILED_UNCHANGED_ANGULAR_FORMULA_AND_CONTROLS',sn=sn,
        maximum_absolute_difference=error,roundoff_bound=tolerance,properties=properties,
        original_SN8_matrix_byte_exact=True if baseline else None,
        malformed_controls_rejected=8,matrix=mesh.base.pin(folder / 'kernel.csv'))


def comparisons():
    import numpy as np
    folders = [('cold48_sn8',MESH / 'cold48_sn8',8), *[(c,OUT/c,sn) for c,nz,sn,cap in CASES]]
    reference = read(CE / 'AAA/statistics.json')
    rf = np.array(reference['reference_flux'])
    rn = np.array(reference['reference_nufission_fraction'])
    with mesh.base._open_xsm(MESH / 'cold12_sn8/track.xsm') as track:
        areas = mesh.base.field(track,track.root,'AREA2D','<f4').astype(float)
    volume = np.repeat(areas*12.5,12)
    fuel = np.repeat(np.array([False,False,False,True,True,True,True,False]),12)
    states, output_rows, points = {}, [], {}
    for case,folder,sn in folders:
        rows = list(csv.DictReader((folder / 'observables.regions.csv').open()))
        summary = dict(line.split('=',1) for line in (folder / 'observables.summary.txt').read_text().splitlines() if '=' in line)
        if len(rows) != 8*48 or {(int(x['radial_region']),int(x['axial_cell'])) for x in rows} != {(r,c) for r in range(1,9) for c in range(1,49)}:
            raise ValueError('complete unique 48-cell observable map required')
        mapped = []
        for region in range(1,9):
            for cell in range(1,13):
                selected = [x for x in rows if int(x['radial_region']) == region and (int(x['axial_cell'])-1)//4+1 == cell]
                if len(selected) != 4:
                    raise ValueError('incomplete conservative original-cell map')
                mapped.append(dict(case=case,radial_region=region,axial_cell=cell,
                    volume_cm3=sum(float(x['volume_cm3']) for x in selected),
                    flux_per_global_nufission=sum(float(x['flux_per_global_nufission']) for x in selected),
                    nufission_fraction=sum(float(x['nufission_fraction']) for x in selected)))
        av = np.array([x['volume_cm3'] for x in mapped])
        if np.max(abs(av-volume)/volume) > 5e-6:
            raise ValueError('original-cell physical volume changed')
        flux = np.array([x['flux_per_global_nufission']/x['volume_cm3'] for x in mapped])
        fraction = np.array([x['nufission_fraction'] for x in mapped])
        k,escape = float(summary['k64']),float(summary['escape_per_nufission'])
        states[case] = dict(flux=flux,fraction=fraction,k=k,escape=escape)
        points[case] = dict(axial_cells=48,sn=sn,k64=k,escape_per_nufission=escape,
            diagnostic_only=True,new_accuracy_classification=None,
            CE_saved_mean_flux_l2=float(np.sqrt(np.sum(volume*(flux-rf)**2)/np.sum(volume*rf**2))),
            CE_saved_mean_max_fuel_relative=float(np.max(abs(fraction[fuel]/rn[fuel]-1))))
        for index,row in enumerate(mapped):
            row.update(normalized_flux_density=float(flux[index]),
                CE_reference_nufission_fraction=float(rn[index]),
                signed_fuel_relative_difference=float(fraction[index]/rn[index]-1) if fuel[index] else None)
        output_rows.extend(mapped)
    changes = {}
    for first,second in [('cold48_sn8','cold48_sn16'),('cold48_sn16','cold48_sn32')]:
        a,b = states[first],states[second]
        changes[first+'_to_'+second] = dict(reactivity_change_pcm=1e5*(1/a['k']-1/b['k']),
            normalized_flux_l2=float(np.sqrt(np.sum(volume*(b['flux']-a['flux'])**2)/np.sum(volume*b['flux']**2))),
            max_fuel_fraction_relative=float(np.max(abs(b['fraction'][fuel]/a['fraction'][fuel]-1))),
            escape_change=b['escape']-a['escape'])
    with (OUT / 'original_cell_comparison.csv').open('x') as stream:
        writer = csv.DictWriter(stream,fieldnames=list(output_rows[0]))
        writer.writeheader();writer.writerows(output_rows)
    return dict(angular_changes=changes,diagnostic_CE_saved_mean_comparisons=points,
        original_complete_AAA_reference_classification='AAA_REFERENCE_NOT_QUALIFIED',
        independent_accuracy_qualified=False,
        scope='Fixed 48-cell cold angular sensitivity; conservative original-cell integrals, '
              'one global nu-fission denominator per state. No new original-rule candidate accuracy assessment.')


def run(expected):
    mesh.require_file(OUT / 'declaration.json', expected)
    declaration = read(OUT / 'declaration.json')
    for name,wanted in declaration['files'].items():
        mesh.require_file(Path(name),wanted)
    ready()
    resources = mesh.DiskResources(ART,declaration['resource_roots'],
        declaration['min_free_bytes'],declaration['artifact_budget_bytes'])
    resources.check()
    mesh.base.write_new(OUT / 'run_claim.json',dict(declaration_sha256=expected,started_unix=time.time(),retries=0))
    runner = mesh.SerialExecutor(OUT,declaration['total_wall_seconds'],'AAA',resources)
    started = time.monotonic()
    result = dict(classification='FAILED_ANGULAR_CONVERGENCE_NO_RETRY',error=None,
        completed_new_cases=[],reused_baseline='cold48_sn8',AAA_accuracy_qualified=False,
        ABA_admitted=False,shared_solver_promoted=False)
    sys.path.insert(0,str(CE / 'runtime'))
    balance = mesh.load_module('angular_original_balance',CE / 'runtime/compare_balance_symmetry.py')
    saved_verifier = mesh.load_module('angular_saved_fields',OUT / 'runtime/saved_field_verifier.py')
    mesh.base.OUT = OUT
    try:
        for i,command in enumerate(declaration['build_commands'],1):
            runner.execute(OUT / 'build','build'+str(i),command,60)
        mesh.base.write_new(OUT / 'build_identity.json',dict(declaration_sha256=expected,
            binaries={n:mesh.base.pin(OUT / 'runtime' / n) for n in ('Dragon','tracking','unit')},
            original_shared_inputs_unchanged=True))
        runner.execute(OUT / 'unit','native',[str(OUT / 'runtime/unit'),'../inputs/original_track.xsm'],
            60,'AXMAT-WHITE-NATIVE-UNIT-COMPLETE')
        result['original_SN8_kernel'] = compiled_kernel(OUT / 'unit',inputs_path('original_track'),8,True)
        mesh.base.write_new(OUT / 'kernel_SN8_receipt.json',result['original_SN8_kernel'])
        for case,nz,sn,cap in CASES:
            folder = OUT / case
            runner.execute(folder,'assembly',[str(OUT / 'runtime/Dragon')],120,'AXMAT-FROZEN-ASSEMBLY-COMPLETE','build.x2m')
            runner.execute(folder,'tracking',[str(OUT / 'runtime/tracking'),'unmarked_track.xsm','track.xsm'],60,'AXMAT-WHITE-TRACKING-COMPLETE')
            tracking = mesh.load_module('angular_tracking_'+str(sn),folder / 'verify_tracking.py').verify_white_tracking_copy(folder / 'unmarked_track.xsm',folder / 'track.xsm')
            structure = mesh.base.structure(folder,nz,sn)
            with mesh.base._open_xsm(folder / 'track.xsm') as track, mesh.base._open_xsm(folder / 'basis.xsm') as basis:
                nunk = int(mesh.base.field(track,track.root,'STATE-VECTOR','<i4')[1])
                stored = int(mesh.base.field(basis,basis.root,'STATE-VECTOR','<i4')[8])
                if nunk != stored or nunk != 8*(4*nz+1+sn):
                    raise ValueError('actual TRACK storage differs from one-word admission')
            mesh.base.write_new(folder / 'structure.json',dict(**structure,tracking_copy=tracking,
                actual_track_nunk=nunk,admitted_storage_nunk=stored))
            runner.execute(folder / 'unit','native',[str(OUT / 'runtime/unit'),'../track.xsm'],60,'AXMAT-WHITE-NATIVE-UNIT-COMPLETE')
            mesh.base.write_new(folder / 'kernel_receipt.json',compiled_kernel(folder / 'unit',folder / 'track.xsm',sn))
            text = runner.execute(folder,'solve',[str(OUT / 'runtime/Dragon')],cap,'AXMAT-FROZEN-AXIAL-COMPLETE','solve.x2m')
            mesh.base.check_terminal(text)
            application = mesh.applied_groups(folder,text)
            runner.execute(folder,'export',[str(ART / 'axial-material-tools-20261003/export_observables'),
                'track.xsm','axial.xsm','../inputs/macro.xsm','observables'],60)
            if not any(x.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for x in (folder / 'export.log').read_text().splitlines()):
                raise ValueError('actual native REAL64 exporter marker absent')
            saved = saved_verifier.saved_state(folder,nz,sn,balance)
            mesh.base.write_new(folder / 'saved_state_admission.json',dict(**saved,white_application=application,
                scope='Unchanged saved positivity/current/symmetry/accounting gates only; no coupled or accuracy qualification.'))
            result['completed_new_cases'].append(case)
        result.update(classification='COMPLETE_WHITE_TRACE_FROZEN_ANGULAR_SENSITIVITY_ONLY',comparisons=comparisons())
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        for name,wanted in declaration['files'].items():
            if mesh.base.digest(name) != wanted:
                result.update(classification='INPUT_CHANGED',error='changed: '+name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        result['outputs'] = {str(p.relative_to(OUT)):mesh.base.digest(p) for p in OUT.rglob('*')
            if p.is_file() and not p.is_symlink() and p.name not in ('declaration.json','run_claim.json','result.json')}
        mesh.base.write_new(OUT / 'result.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('resources','outputs')},indent=2))


def inputs_path(name):
    return OUT / 'inputs' / (name+'.xsm')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)
