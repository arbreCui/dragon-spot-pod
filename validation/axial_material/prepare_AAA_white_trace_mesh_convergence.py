"""Bounded 12/24/48-cell cold study of the same frozen white-trace AAA state.

Only numerical axial layout and its storage/scope guards change. This is not
a new radial solve, coupled fixed point, accuracy qualification or CE fit.
"""
import argparse
import csv
import difflib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
PROD = ART / 'axial-material-production-qualified-AB-white-trace-20261004'
CE = ART / 'axial-material-ce-qualified-AAA-white-trace-precision-specpin-20261004'
COLD = ART / 'axial-material-AAA-white-trace-cold-control-paths-20261004'
CLOSEOUT = ART / 'axial-material-AAA-white-trace-precision-closeout-20261005'
OUT = ART / 'axial-material-AAA-white-trace-mesh-convergence-20261005'
TOOLS = ROOT / 'validation/axial_material'
sys.path.insert(0, str(PROD / 'runtime'))
from production_runner import DiskResources, SerialExecutor, verify_prepared, verify_sealed_directory, require_file
import frozen_AAA_axial_sensitivities as base
import frozen_AAA_axial_sensitivities_metadata as metadata
import white_side_trace_kernel as model

PREPARED_SHA = '88640bfd32cbca03d4e527b99760f99288528bb0ff5720c81f758bca60beffbf'
ASSESSMENT_SHA = '5fa0435dff49977ab0b0ae3e8e50af1482467cfae22df3b6effd83ce3b2228f0'
CASES = [('cold12_sn8', 12, 300), ('cold24_sn8', 24, 1200), ('cold48_sn8', 48, 3000)]


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('ambiguous numerical-scope anchor: ' + old[:80])
    return text.replace(old, new, 1)


def ready():
    info = verify_prepared(PROD / 'prepared.json', PREPARED_SHA)
    assessment = json.loads(require_file(CE / 'AAA/reference_assessment.json', ASSESSMENT_SHA).read_text())
    if (assessment['classification'] != 'AAA_REFERENCE_NOT_QUALIFIED'
            or assessment['checks']['nu_fission'] != 'FAIL' or assessment['ABA_admitted']):
        raise ValueError('actual completed unqualified precision assessment required')
    for label in ('CE_execution', 'CE_native_result', 'measurement_admission'):
        item = assessment[label]
        require_file(Path(item['path']), item['sha256'])
    for item in assessment['evidence'].values():
        require_file(Path(item['path']), item['sha256'])
    native = json.loads((CE / 'AAA/native_result.json').read_text())
    analysis = json.loads((CE / 'AAA/analysis_result.json').read_text())
    if (native['returncode'] != 0 or native['error'] is not None
            or native['status'] != 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS'
            or analysis['classification'] != 'COMPLETE_REFERENCE_ANALYSIS'):
        raise ValueError('native reference and complete original analysis must be terminal')
    status = json.loads((PROD / 'AAA/run_status.json').read_text())
    if status['cases']['AAA']['classification'] != 'VALID_MET' or (PROD / 'ABA').exists():
        raise ValueError('same saved AAA fixed point, with ABA unstarted, required')
    final = Path(status['cases']['AAA']['final_directory'])
    for folder in (PROD / 'archives', PROD / 'training', PROD / 'AAA/bootstrap', final):
        verify_sealed_directory(folder)
    seal = json.loads(require_file(CLOSEOUT / 'seal.json',
        '8c5fee1abd5aec4436280c7ce20d72077e69b528600b5fe7beb143b3f190e595').read_text())
    for name, wanted in seal['files'].items():
        require_file(CLOSEOUT / name, wanted)
    closeout = json.loads((CLOSEOUT / 'result.json').read_text())
    require_file(CE / 'AAA/analysis_result.json', closeout['analysis_result_sha256'])
    return info, final


def source_copy(name, old, new, proofs):
    original = (COLD / 'build' / name).read_text()
    changed = replace_once(original, old, new)
    if replace_once(changed, new, old) != original:
        raise ValueError('source restoration outside declared scope change')
    (OUT / 'build' / name).write_text(changed)
    (OUT / 'build' / (name + '.patch')).write_text(''.join(difflib.unified_diff(
        original.splitlines(True), changed.splitlines(True), fromfile='frozen-white-12-cell', tofile='isolated-12-24-48-scope')))
    proofs[name] = dict(original=base.pin(COLD / 'build' / name),
        candidate=base.pin(OUT / 'build' / name), full_text_restored_exactly=True,
        old_anchor=old, new_anchor=new)


def prepare():
    info, final = ready()
    OUT.mkdir(exist_ok=False)
    for name in ('runtime', 'inputs', 'build', 'unit', 'AAA'):
        (OUT / name).mkdir()
    shutil.copy2(PROD / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    inputs = dict(radial=final / 'candidate_radial.xsm', system=final / 'candidate_system.xsm',
        basis=PROD / 'AAA/bootstrap/basis_reference.xsm',
        macro=PROD / 'AAA/bootstrap/initial_axial_macrolib.xsm',
        original_track=PROD / 'AAA/bootstrap/initial_axial_track.xsm')
    for name, path in inputs.items():
        (OUT / 'inputs' / (name + '.xsm')).symlink_to(path.resolve())
    proofs = {}
    source_copy('SPOT1P64.f90', 'nreg2d /= 8 .or. nfloor /= 12 .or. nsnap /= 3',
        'nreg2d /= 8 .or. all(nfloor /= [12,24,48]) .or. nsnap /= 3', proofs)
    source_copy('axmat_white_trace_model.f90', 'nreg /= 8 .or. nfloor /= 12 .or. nsnap /= 3',
        'nreg /= 8 .or. all(nfloor /= [12,24,48]) .or. nsnap /= 3', proofs)
    for name in ('axmat_white_trace_tracking.f90', 'axmat_white_trace_unit.f90'):
        shutil.copy2(COLD / 'build' / name, OUT / 'build' / name)
    unit = OUT / 'build/axmat_white_trace_unit.f90'
    original = unit.read_text()
    old = '  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,24,3,8,3,1,info)\n  call rejected()'
    new = '''  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,24,3,8,3,1,info)
  if (info /= 0) call XABORT('AXMAT WHITE UNIT: DECLARED 24-CELL SCOPE REJECTED.')
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,48,3,8,3,1,info)
  if (info /= 0) call XABORT('AXMAT WHITE UNIT: DECLARED 48-CELL SCOPE REJECTED.')
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,13,3,8,3,1,info)
  call rejected()'''
    changed = replace_once(original, old, new)
    if replace_once(changed, new, old) != original:
        raise ValueError('native unit changed outside explicit layout controls')
    unit.write_text(changed)
    (OUT / 'build/axmat_white_trace_unit.f90.patch').write_text(''.join(difflib.unified_diff(
        original.splitlines(True), changed.splitlines(True), fromfile='frozen-12-cell-unit', tofile='declared-layout-controls')))
    proofs['unit'] = dict(original=base.pin(COLD / 'build/axmat_white_trace_unit.f90'),
        candidate=base.pin(unit), full_text_restored_exactly=True,
        change='24 and 48 are positive scope controls; undeclared 13 replaces formerly invalid 24. All seven malformed-input checks remain.')
    original_basis = inputs['basis'].read_bytes()
    with base._open_xsm(inputs['basis']) as archive:
        entry = archive.root['STATE-VECTOR']
    admissions = {}
    original_host = (PROD / 'runtime/white_receiver_tracking.py').read_text()
    rules = json.loads((CE / 'balance_symmetry_rules.json').read_text())
    for case, nz, cap in CASES:
        folder = OUT / case
        folder.mkdir()
        target = 8 * (4 * nz + 1 + 8)
        adapted, receipt = metadata.adapt_bytes(original_basis, entry, target)
        with (folder / 'basis.xsm').open('xb') as stream:
            stream.write(adapted)
        deck = base.build_deck(nz, 8).replace("FILE '../inputs/basis.xsm'", "FILE './basis.xsm'")
        (folder / 'build.x2m').write_text(deck.replace("FILE './track.xsm'", "FILE './unmarked_track.xsm'"))
        (folder / 'solve.x2m').write_text(base.SOLVE)
        host = replace_once(original_host, '!=(8,12,3,1,8,3)', f'!=(8,{nz},3,1,8,3)')
        if replace_once(host, f'!=(8,{nz},3,1,8,3)', '!=(8,12,3,1,8,3)') != original_host:
            raise ValueError('tracking verifier changed outside declared layout')
        (folder / 'verify_tracking.py').write_text(host)
        actual_rules = dict(rules, axial_cells=nz)
        restored = dict(actual_rules, axial_cells=12)
        if restored != rules:
            raise ValueError('original current/positivity/symmetry thresholds changed')
        base.write_new(folder / 'production_rules.json', actual_rules)
        admissions[case] = dict(**receipt, axial_cells=nz, sn=8, axial_wall_seconds=cap,
            original=base.pin(inputs['basis']), adapted=base.pin(folder / 'basis.xsm'),
            tracking_verifier_only_declared_cell_count_changed=True,
            production_rules_only_declared_cell_count_changed=True)
    base.write_new(OUT / 'source_and_layout_admission.json', dict(status='PASS_DECLARED_NUMERICAL_SCOPE_ONLY',
        source_changes=proofs, layouts=admissions, shared_sources_changed=False,
        all_other_source_text_exact=True, angular_kernel_formula_changed=False,
        radial_and_basis_records_must_match_before_each_solve=3330))
    compiler = Path(shutil.which('gfortran')).resolve()
    libs = [ROOT / 'lib/Darwin_arm64/libDragon.a', ROOT / 'Trivac/lib/Darwin_arm64/libTrivac.a',
            ROOT / 'Utilib/lib/Darwin_arm64/libUtilib.a', ROOT / 'Ganlib/lib/Darwin_arm64/libGanlib.a']
    flags = ['-O2', '-march=native', '-ffp-contract=off', '-g', '-fPIC', '-frecord-marker=4',
        '-ffixed-line-length-none', '-I'+str(OUT / 'build'), '-I'+str(ROOT / 'lib/Darwin_arm64/modules'),
        '-I'+str(ROOT / 'Ganlib/lib/Darwin_arm64/modules'), '-J'+str(OUT / 'build')]
    commands = [[str(compiler), *flags, '-c', str(OUT / 'build' / name),
                 '-o', str((OUT / 'build' / name).with_suffix('.o'))]
                for name in ('axmat_white_trace_model.f90', 'SPOT1P64.f90',
                             'axmat_white_trace_tracking.f90', 'axmat_white_trace_unit.f90')]
    module_object = OUT / 'build/axmat_white_trace_model.o'
    for name, binary in [('axmat_white_trace_tracking', 'tracking'), ('axmat_white_trace_unit', 'unit')]:
        commands.append([str(compiler), *flags, str(OUT / 'build' / (name+'.o')),
                         str(module_object), str(libs[2]), str(libs[3]), '-o', str(OUT / 'runtime' / binary)])
    flight = ART / 'axial-material-AAA-compensated-flight-20261004/build'
    commands.append([str(compiler), '-O2', '-march=native', '-ffp-contract=off', '-g',
        str(ROOT / 'src/DRAGON.o'), str(flight / 'SPOR64_A8.o'), str(flight / 'AXMAT_MCGFCF_COMP.o'),
        str(module_object), str(OUT / 'build/SPOT1P64.o'), str(COLD / 'build/SPOF64.o'),
        *map(str, libs), '-o', str(OUT / 'runtime/Dragon')])
    files = [Path(__file__).resolve(), Path(base.__file__), Path(metadata.__file__), Path(model.__file__),
        Path(sys.modules['production_runner'].__file__),
        Path(sys.modules['snapshot_control_preflight'].__file__), Path(sys.modules['qualified_snapshot_ingestion'].__file__),
        PROD / 'prepared.json', PROD / 'AAA/run_status.json', PROD / 'runtime/Dragon',
        PROD / 'runtime/white_receiver_tracking.py', Path(info['case_spec']['path']),
        final / 'result.json', CE / 'AAA/execution.json', CE / 'AAA/native_result.json',
        CE / 'AAA/analysis_result.json', CE / 'AAA/reference_assessment.json', CE / 'AAA/statistics.json',
        CE / 'AAA/currents_balance_symmetry.json', CE / 'balance_symmetry_rules.json',
        CE / 'runtime/compare_balance_symmetry.py', CE / 'runtime/reference_statistics.py',
        CLOSEOUT / 'seal.json', CLOSEOUT / 'result.json',
        COLD / 'declaration.json', COLD / 'build_identity.json', COLD / 'unit/kernel.csv', COLD / 'build/SPOF64.o',
        *[COLD / 'build' / name for name in ('SPOT1P64.f90', 'axmat_white_trace_model.f90', 'axmat_white_trace_tracking.f90', 'axmat_white_trace_unit.f90')],
        ART / 'axial-material-tools-20261003/export_observables', TOOLS / 'export_observables.f90',
        ART / 'axial-material-qualified-AAA-white-trace-observables-20261004/observables.regions.csv',
        ART / 'axial-material-qualified-AAA-white-trace-observables-20261004/observables.summary.txt',
        ROOT / 'src/DRAGON.o', ROOT / 'Ganlib/lib/Darwin_arm64/modules/ganlib.mod',
        flight / 'SPOR64_A8.o', flight / 'AXMAT_MCGFCF_COMP.o', compiler, *libs, *inputs.values(),
        *[p for p in OUT.rglob('*') if p.is_file() and not p.is_symlink()]]
    roots = sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir())
    resources = DiskResources(ART, roots, 8*2**30, 40*2**30)
    before = resources.check()
    projected = before['artifact_bytes'] + 512*2**20
    if projected > 40*2**30:
        raise ValueError('512 MiB reserved study/storage forecast exceeds unchanged 40 GiB history bound')
    base.write_new(OUT / 'declaration.json', dict(schema='AXMAT_WHITE_TRACE_FROZEN_AXIAL_MESH_CONVERGENCE_V1',
        declared_unix=time.time(), files={str(p.resolve()):base.digest(p) for p in files},
        inputs={name:base.pin(path) for name,path in inputs.items()}, build_commands=commands,
        cases=[dict(name=name, axial_cells=nz, sn=8, axial_wall_seconds=cap) for name,nz,cap in CASES],
        total_wall_seconds=5400, stage_caps=dict(build=60, unit=60, assembly=120, tracking=60, export=60),
        threads=1, numeric_children_at_once=1, retries=0, artifact_budget_bytes=40*2**30,
        min_free_bytes=8*2**30, resource_roots=roots, resources_before=before,
        storage_forecast_bytes=projected,
        source_gate='Actual complete 2000-batch precision reference and unchanged unqualified nu-fission assessment, all sealed AAA stages and no ABA execution.',
        physical_inputs_changed=False, original_inner_and_accuracy_gates_changed=False,
        source_scope='Only exact 12/24/48-cell guards extend the isolated native scope. Original SN8 kernel formula, rank1 outer-sodium trace, all other Fortran source text and compensated radial flight objects remain unchanged. Seven malformed controls and actual compiled SN8 matrix must pass before any transport solve.',
        numerical_layout='Uniform 12,24,48 cells across the same 150 cm and three 50 cm physical zones. All 3330 frozen radial/basis records exact before each solve. Only reference root STATE-VECTOR(9) storage word changes; native guard stays active.',
        transport_scope='Three cold axial solves only, each from the same final AAA radial operator and common basis. No new radial transport, training, coupled map or CE transport.',
        comparison='Sum 1/2/4 complete fine-cell integrals conservatively into each original 12-cell bin, using one global nu-fission denominator per state and exact physical-volume checks. Report original eight-gate CE assessment unchanged; refined cold-state CE means are diagnostic only.',
        decision='Report 12-to-24 and 24-to-48 numerical changes and spatial patterns. Do not select a fitted multiplier, modify a threshold, attribute a quantitative cause from one factor alone, qualify AAA/ABA or promote shared runtime. Full coupling and independent original-rule accuracy remain required.'))
    print(json.dumps(dict(status='PREDECLARED_THREE_COLD_MESH_STUDIES_NO_TRANSPORT',
        declaration=base.pin(OUT / 'declaration.json')), indent=2))


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compiled_kernel():
    import numpy as np
    with base._open_xsm(OUT / 'inputs/original_track.xsm') as track:
        mu = base.field(track, track.root, 'U', '<f4').astype(float)
        weights = base.field(track, track.root, 'W', '<f4').astype(float)
        area = float(base.field(track, track.root, 'AREA2D', '<f4').astype(float).sum())
    matrix = np.full((8,8), np.nan)
    rows = list(csv.DictReader((OUT / 'unit/kernel.csv').open()))
    if len(rows) != 64:
        raise ValueError('incomplete compiled SN8 kernel')
    for row in rows:
        i, j = int(row['row'])-1, int(row['column'])-1
        if not (0 <= i < 8 and 0 <= j < 8) or np.isfinite(matrix[i,j]):
            raise ValueError('duplicate or outside native kernel entry')
        matrix[i,j] = float(row['value'])
    expected = model.trace_exchange(mu, weights, 6*.61776479, area)
    tolerance = 128*np.finfo(float).eps*np.linalg.norm(expected, np.inf)
    error = float(np.max(abs(matrix-expected)))
    if not np.isfinite(matrix).all() or error > tolerance:
        raise ValueError('compiled/Python original angular formula mismatch')
    if base.digest(OUT / 'unit/kernel.csv') != base.digest(COLD / 'unit/kernel.csv'):
        raise ValueError('compiled SN8 angular matrix differs from original white implementation')
    if 'negative_controls_rejected=7' not in (OUT / 'unit/native.log').read_text().splitlines():
        raise ValueError('seven actual malformed-input controls did not pass')
    return dict(status='PASS_SAME_COMPILED_SN8_ANGULAR_KERNEL_AND_SCOPE_CONTROLS',
        maximum_absolute_difference=error, roundoff_bound=tolerance,
        original_matrix_byte_exact=True, malformed_controls_rejected=7,
        valid_scope_controls=[12,24,48], matrix=base.pin(OUT / 'unit/kernel.csv'))


def saved_state(folder, nz, balance):
    import numpy as np
    rules = json.loads((folder / 'production_rules.json').read_text())
    parsed = balance.read_production(folder / 'observables.regions.csv',
        folder / 'observables.faces.csv', folder / 'observables.summary.txt', rules)
    report = balance.evaluate_production(parsed, rules)
    if any(value != 'PASS' for value in report['checks'].values()):
        raise ValueError('original saved positivity/current/accounting/symmetry checks failed')
    with base._open_xsm(folder / 'track.xsm') as track:
        keys = base.field(track, track.root, 'KEYFLX', '<i4')
        state = base.field(track, track.root, 'STATE-VECTOR', '<i4')
        nunk = int(state[1])
        if (nunk != 8*(4*nz+9) or keys.size != 8*nz
                or len(set(keys.tolist())) != 8*nz or np.any(keys < 1) or np.any(keys > nunk)):
            raise ValueError('complete declared scalar KEYFLX layout required')
    with base._open_xsm(folder / 'axial.xsm') as state:
        k = base.field(state, state.root, 'SPOT-KEFF64', '<f8')
        tag = base.field(state, state.root, 'SPOT-X-KEFF', '<f8')
        if len(k) != 1 or k[0] <= 0 or not np.array_equal(k, tag) or k[0] != float(parsed['summary']['k64']):
            raise ValueError('actual saved REAL64 eigenvalue authority differs')
        scalar_min = float('inf')
        for item in base.list_handles(state, state.root, 'FLUX64', 370):
            if item[1:] != (2*nunk, 4):
                raise ValueError('incomplete REAL64 group vector')
            values = np.frombuffer(state.read(item[0], item[1]), '<f8')[keys-1]
            if not np.isfinite(values).all() or np.any(values <= 0):
                raise ValueError('nonpositive actual saved scalar group field')
            scalar_min = min(scalar_min, float(values.min()))
    report.update(saved_k64=float(k[0]), saved_scalar_entries=8*nz*370,
        actual_minimum_scalar_group_flux=scalar_min, all_group_scalar_entries_positive=True)
    return report


def applied_groups(folder, text):
    import numpy as np
    rows = re.findall(r'^AXMAT-WHITE-APPLY GROUP=(\d+) TRACE-FACTOR=\s*(\S+)\s*$', text, re.M)
    factors = {int(group):float(value) for group,value in rows}
    if len(rows) != 370 or set(factors) != set(range(1,371)):
        raise ValueError('missing or duplicate actual native white branch group')
    with base._open_xsm(folder / 'system.xsm') as system:
        for group, item in enumerate(base.list_handles(system, system.root, 'GROUP', 370), 1):
            directory = system.directory(item[0])
            basis = base.field(system, directory, 'POD-BASIS', '<f4').astype(float)
            if base.field(system, directory, 'POD-NMODE', '<i4').tolist() != [1] or basis.size != 8:
                raise ValueError('original common rank-one basis required')
            if abs(factors[group]/float(basis[0]**2)-1) > 128*np.finfo(float).eps:
                raise ValueError('actual projected boundary trace factor differs')
    return dict(status='PASS_ALL_370_ORIGINAL_WHITE_TRACE_APPLICATIONS', groups=370,
                trace_factor_range=[min(factors.values()), max(factors.values())])


def comparisons():
    import numpy as np
    records = {}
    for case, nz, cap in CASES:
        folder = OUT / case
        rows = list(csv.DictReader((folder / 'observables.regions.csv').open()))
        summary = dict(line.split('=',1) for line in (folder / 'observables.summary.txt').read_text().splitlines() if '=' in line)
        mapped = []
        for region in range(1,9):
            for cell in range(1,13):
                selected = [row for row in rows if int(row['radial_region']) == region
                    and (int(row['axial_cell'])-1)//(nz//12)+1 == cell]
                if len(selected) != nz//12:
                    raise ValueError('incomplete conservative fine-to-original-cell map')
                volume = sum(float(row['volume_cm3']) for row in selected)
                mapped.append(dict(radial_region=region, axial_cell=cell, volume_cm3=volume,
                    flux_per_global_nufission=sum(float(row['flux_per_global_nufission']) for row in selected),
                    nufission_fraction=sum(float(row['nufission_fraction']) for row in selected)))
        records[case] = dict(rows=mapped, k=float(summary['k64']), escape=float(summary['escape_per_nufission']))
    reference = json.loads((CE / 'AAA/statistics.json').read_text())
    p12 = records['cold12_sn8']
    volume = np.array([row['volume_cm3'] for row in p12['rows']])
    rf = np.array(reference['reference_flux'])
    rn = np.array(reference['reference_nufission_fraction'])
    fuel = np.array([row['radial_region'] in (4,5,6,7) for row in p12['rows']])
    comparison_rows = []
    point_reports = {}
    for case,nz,cap in CASES:
        actual = records[case]
        av = np.array([row['volume_cm3'] for row in actual['rows']])
        if np.max(abs(av-volume)/volume) > 5e-6:
            raise ValueError('fine-to-original-cell physical volume mismatch')
        flux = np.array([row['flux_per_global_nufission']/row['volume_cm3'] for row in actual['rows']])
        fraction = np.array([row['nufission_fraction'] for row in actual['rows']])
        relative = fraction[fuel]/rn[fuel]-1
        point_reports[case] = dict(axial_cells=nz, k64=actual['k'], escape_per_nufission=actual['escape'],
            diagnostic_only=True, new_accuracy_classification=None,
            CE_saved_mean_flux_l2=float(np.sqrt(np.sum(volume*(flux-rf)**2)/np.sum(volume*rf**2))),
            CE_saved_mean_max_fuel_relative=float(np.max(abs(relative))))
        for row, f, n in zip(actual['rows'], flux, fraction, strict=True):
            index = (row['radial_region']-1)*12+row['axial_cell']-1
            comparison_rows.append(dict(case=case, **row, normalized_flux_density=float(f),
                CE_reference_nufission_fraction=float(rn[index]),
                signed_fuel_relative_difference=float(n/rn[index]-1) if row['radial_region'] in (4,5,6,7) else None))
    changes = {}
    for first,second in [('cold12_sn8','cold24_sn8'),('cold24_sn8','cold48_sn8')]:
        a,b = records[first],records[second]
        af = np.array([r['flux_per_global_nufission']/r['volume_cm3'] for r in a['rows']])
        bf = np.array([r['flux_per_global_nufission']/r['volume_cm3'] for r in b['rows']])
        an = np.array([r['nufission_fraction'] for r in a['rows']])
        bn = np.array([r['nufission_fraction'] for r in b['rows']])
        changes[first+'_to_'+second] = dict(reactivity_change_pcm=1e5*(1/a['k']-1/b['k']),
            normalized_flux_l2=float(np.sqrt(np.sum(volume*(bf-af)**2)/np.sum(volume*bf**2))),
            max_fuel_fraction_relative=float(np.max(abs(bn[fuel]/an[fuel]-1))),
            escape_change=b['escape']-a['escape'])
    with (OUT / 'original_cell_comparison.csv').open('x') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(comparison_rows[0]))
        writer.writeheader(); writer.writerows(comparison_rows)
    return dict(mesh_changes=changes, diagnostic_CE_saved_mean_comparisons=point_reports,
        original_complete_AAA_reference_classification='AAA_REFERENCE_NOT_QUALIFIED',
        independent_accuracy_qualified=False,
        scope='Conservative original-cell cold numerical sensitivity only. No resampling, local normalization, coupled fixed point or original-rule candidate accuracy assessment.')


def run(expected):
    require_file(OUT / 'declaration.json', expected)
    declaration = json.loads((OUT / 'declaration.json').read_text())
    for name,wanted in declaration['files'].items():
        require_file(Path(name), wanted)
    ready()
    if (OUT / 'run_claim.json').exists():
        raise ValueError('permanent cold study claim exists; no retry')
    resources = DiskResources(ART, declaration['resource_roots'], declaration['min_free_bytes'], declaration['artifact_budget_bytes'])
    resources.check()
    base.write_new(OUT / 'run_claim.json', dict(declaration_sha256=expected, started_unix=time.time(), retries=0))
    runner = SerialExecutor(OUT, declaration['total_wall_seconds'], 'AAA', resources)
    result = dict(classification='FAILED_WHITE_TRACE_MESH_STUDY_NO_RETRY', error=None,
        completed_cases=[], AAA_accuracy_qualified=False, ABA_admitted=False, shared_solver_promoted=False)
    started = time.monotonic()
    base.OUT = OUT
    sys.path.insert(0, str(CE / 'runtime'))
    balance = load_module('white_mesh_original_current_rules', CE / 'runtime/compare_balance_symmetry.py')
    try:
        for i,command in enumerate(declaration['build_commands'],1):
            runner.execute(OUT / 'build', 'build'+str(i), command, 60)
        base.write_new(OUT / 'build_identity.json', dict(declaration_sha256=expected,
            binaries={name:base.pin(OUT / 'runtime' / name) for name in ('Dragon','tracking','unit')},
            original_shared_inputs_unchanged=True))
        runner.execute(OUT / 'unit', 'native', [str(OUT / 'runtime/unit'), '../inputs/original_track.xsm'],
            60, 'AXMAT-WHITE-NATIVE-UNIT-COMPLETE')
        result['compiled_kernel'] = compiled_kernel()
        base.write_new(OUT / 'kernel_receipt.json', result['compiled_kernel'])
        for case,nz,cap in CASES:
            folder = OUT / case
            runner.execute(folder, 'assembly', [str(OUT / 'runtime/Dragon')], 120,
                'AXMAT-FROZEN-ASSEMBLY-COMPLETE', 'build.x2m')
            runner.execute(folder, 'tracking', [str(OUT / 'runtime/tracking'), 'unmarked_track.xsm', 'track.xsm'],
                60, 'AXMAT-WHITE-TRACKING-COMPLETE')
            verifier = load_module('white_mesh_tracking_'+str(nz), folder / 'verify_tracking.py')
            tracking = verifier.verify_white_tracking_copy(folder / 'unmarked_track.xsm', folder / 'track.xsm')
            structure = base.structure(folder, nz, 8)
            with base._open_xsm(folder / 'track.xsm') as tr, base._open_xsm(folder / 'basis.xsm') as basis:
                nunk = int(base.field(tr,tr.root,'STATE-VECTOR','<i4')[1])
                stored = int(base.field(basis,basis.root,'STATE-VECTOR','<i4')[8])
                if nunk != stored or nunk != 8*(4*nz+9):
                    raise ValueError('actual native TRACK differs from admitted storage word')
            base.write_new(folder / 'structure.json', dict(**structure, tracking_copy=tracking,
                actual_track_nunk=nunk, admitted_storage_nunk=stored))
            text = runner.execute(folder, 'solve', [str(OUT / 'runtime/Dragon')], cap,
                'AXMAT-FROZEN-AXIAL-COMPLETE', 'solve.x2m')
            base.check_terminal(text)
            application = applied_groups(folder,text)
            runner.execute(folder, 'export', [str(ART / 'axial-material-tools-20261003/export_observables'),
                'track.xsm', 'axial.xsm', '../inputs/macro.xsm', 'observables'], 60)
            if not any(line.startswith('AXMAT-OBSERVABLES-COMPLETE k64=') for line in (folder / 'export.log').read_text().splitlines()):
                raise ValueError('actual native REAL64 exporter marker missing')
            saved = saved_state(folder,nz,balance)
            base.write_new(folder / 'saved_state_admission.json', dict(**saved, white_application=application,
                scope='Original numerical/positivity/current/accounting/symmetry rules only; no coupled or physical-accuracy qualification.'))
            result['completed_cases'].append(case)
        result['comparisons'] = comparisons()
        result['classification'] = 'COMPLETE_WHITE_TRACE_FROZEN_MESH_SENSITIVITY_ONLY'
    except BaseException as error:
        result['error'] = repr(error)
        raise
    finally:
        for name,wanted in declaration['files'].items():
            if base.digest(name) != wanted:
                result.update(classification='INPUT_CHANGED', error='changed: '+name)
        result['elapsed_seconds'] = time.monotonic()-started
        result['resources'] = resources.check()
        result['outputs'] = {str(p.relative_to(OUT)):base.digest(p) for p in OUT.rglob('*')
            if p.is_file() and not p.is_symlink() and p.name not in ('declaration.json','run_claim.json','result.json')}
        base.write_new(OUT / 'result.json', result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('resources','outputs')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare','run'))
    parser.add_argument('--sha256')
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else run(args.sha256)
