"""Declare audited A/B producers and an explicit unchanged-online legacy BOOT trial."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys

from production_runner import ROOT, dump_json, sha256
from qualified_snapshot_ingestion import descriptor, verify_offline_state, PRODUCER_SHA, ONLINE_SHA


def main():
    art = ROOT / 'validation/artifacts'
    work = art / 'axial-material-qualified-AB-admission-v2-20261004'
    work.mkdir(exist_ok=False)
    src = Path(__file__).parent
    a = art / 'axial-material-r64-system-normalization-20261003'
    b = art / 'axial-material-r64-snapshot-B-dependencyfix-20261004'
    original = art / 'axial-material-inputs-20261003'
    old_manifest = original / 'material_inputs.json'
    old = json.loads(old_manifest.read_text())
    states = {}
    for letter,base in (('A',a),('B',b)):
        state = dict(archive=descriptor(base / letter / f'snapshot_{letter}.xsm'),
            track=descriptor(base / letter / 'radial_track.bin'), log=descriptor(base / letter / 'solve.log'),
            execution=descriptor(base / 'execution.json'), snapshot_run_status=descriptor(base / 'run_status.json'),
            audit_status=descriptor(base / 'audit_initialized/run_status.json'),
            material=descriptor(original / letter / 'material.xsm'),
            moments=descriptor(base / ('tracking_moments/moments.bin' if letter == 'A' else 'audit_initialized/moments.bin')))
        state['payload_audit'] = verify_offline_state(state)
        states[letter] = state
    manifest = dict(old)
    manifest['config'] = dict(old['config'], snapshot_eps=2.5e-7, mccg_eps=2.5e-8, maxout=500)
    manifest['schema'] = 'AXMAT_ORIGINAL_TONE_MATERIAL_WITH_QUALIFIED_R64_SNAPSHOTS_V1'
    manifest['original_material_preparation'] = dict(manifest=descriptor(old_manifest),
        results=descriptor(original / 'material_results.json'), original_config=old['config'],
        scope='Original TONE material is unchanged. Snapshot controls below belong to the new separate offline producers, not to the historical material run.')
    manifest['qualified_snapshots'] = {k:states[k]['execution'] for k in ('A','B')}
    dump_json(work / 'material_snapshot_manifest.json', manifest)
    receipt = dict(schema='AXMAT_QUALIFIED_OFFLINE_PRODUCER_TO_LEGACY_BOOT_V1', states=states,
        producer_runtime=descriptor(a / 'runtime/Dragon'), online_receiver_sha256=ONLINE_SHA,
        receiver_source=descriptor(ROOT / 'src/SPOR64_B2B.f90'),
        inputs_manifest_sha256=sha256(work / 'material_snapshot_manifest.json'),
        offline_r64_directly_consumed_by_boot=False, production_qualified=False,
        scope='The online executable is unchanged; BOOT consumes only exact REAL32 FLUX mirrors as initial guesses. No offline terminal is relabeled as a coupled terminal.')
    dump_json(work / 'producer_ingestion_receipt.json', receipt)
    parent_spec = src / 'case_spec_rank1_moc_precision.json'
    spec = json.loads(parent_spec.read_text())
    spec['experiment_id'] = 'axial-material-qualified-AB-rank1-legacy-boot-20261004'
    spec['status'] = 'PREDECLARED_QUALIFIED_OFFLINE_PRODUCER_LEGACY_BOOT_TRIAL'
    spec['qualified_snapshot_producers'] = dict(producer_sha256=PRODUCER_SHA,
        receiver_sha256=ONLINE_SHA, material_sha256={k:states[k]['material']['sha256'] for k in ('A','B')},
        receipt=descriptor(work / 'producer_ingestion_receipt.json'), parent_spec=descriptor(parent_spec),
        scope='Fresh declared online trial after separately qualified A/B offline snapshots. Same rank1, physical definitions, online controls and all reference gates; this receipt admits BOOT initial guesses only.')
    dump_json(work / 'case_spec.json', spec)
    spec_sha = sha256(work / 'case_spec.json')
    rank = json.loads((src / 'case_spec_rank1_moc_precision_addendum.json').read_text())
    rank['case_spec_sha256'] = spec_sha
    rank['experiment_id'] = spec['experiment_id']
    dump_json(work / 'rank_addendum.json', rank)
    # Version the orchestration code. The historical runner and its runtime
    # guard are never modified; the new admission is explicit and separately pinned.
    runner_text = (src / 'production_runner.py').read_text()
    start = runner_text.index('    if receipts.get("schema_version") != 1 or receipts.get("classification") != "VALID_SNAPSHOTS":')
    stop = runner_text.index('    # Resource-only consumers',start)
    replacement = '''    from qualified_snapshot_ingestion import admit_snapshots
    producer_admission = admit_snapshots(receipts, resolved, spec)
    for case in ("A", "B"):
        check_dragon_log(Path(resolved[f"snapshot_log_{case}"]["path"]).read_text(errors="replace"),
                         f"AXMAT-SNAPSHOT-{case}-COMPLETE")
'''
    runner_text = runner_text[:start] + replacement + runner_text[stop:]
    runner_text = runner_text.replace('"snapshot_control_audits": control_audits,',
        '"snapshot_control_audits": control_audits, "producer_admission": producer_admission,')
    anchor = '    config = ProductionConfig(**info["production_config"])\n    write_inputs(output / "decks", config)'
    extra = '''    for name in ("qualified_snapshot_ingestion.py", "analyze_r64_snapshot.py",
                 "analyze_r64_tracking_moments.py", "check_r64_audit_rejections.py",
                 "check_r64_normalization_rejections.py"):
        shutil.copy2(Path(__file__).with_name(name), runtime / name)
'''
    if runner_text.count(anchor) != 1:
        raise ValueError('unexpected historical runner layout')
    runner_text = runner_text.replace(anchor,extra + anchor)
    runner_text = runner_text.replace('ROOT = Path(__file__).resolve().parents[2]', 'ROOT = Path("/Users/wen/spot")')
    (work / 'production_runner_qualified.py').write_text(runner_text)
    for name in ('production_inputs.py','snapshot_control_preflight.py','qualified_snapshot_ingestion.py',
                 'analyze_r64_snapshot.py','analyze_r64_tracking_moments.py',
                 'check_r64_audit_rejections.py','check_r64_normalization_rejections.py'):
        shutil.copy2(src / name,work / name)
    # Validate the copied runner before any solver is started.
    module_spec = importlib.util.spec_from_file_location('qualified_runner',work / 'production_runner_qualified.py')
    module = importlib.util.module_from_spec(module_spec)
    sys.modules[module_spec.name] = module
    module_spec.loader.exec_module(module)
    pc = spec['production']; radial,axial=pc['radial_controls'],pc['axial_controls']
    config = dict(cells_per_zone=4,zone_height_cm=50.0,sn=8,rank=1,
        eps_radial=radial['eps'],eps_axial=axial['eps'],eps_mccg=radial['eps_mccg'],
        maxout=500,maxinr=740,radial_acce_free=3,radial_acce_accel=3,axial_acce_free=3,axial_acce_accel=0)
    caps=spec['resource_caps']
    budget=dict(setup_seconds=caps['common_basis_wall_s'],bootstrap_axial_seconds=caps['axial_wall_s'],
        bootstrap_radial_seconds=caps['bootstrap_radial_wall_s'],radial_seconds=caps['map_radial_wall_s'],
        axial_seconds=caps['axial_wall_s'],host_seconds=caps['postchecks_wall_s'],
        max_maps=caps['max_maps_per_case'],total_seconds=caps['total_wall_s_per_spot_case'])
    output=art / 'axial-material-production-qualified-AB-20261004'
    roots=sorted(str(p.resolve()) for p in art.glob('axial-material-*') if p.is_dir())+[str(output)]
    inputs={'material_manifest':descriptor(work / 'material_snapshot_manifest.json'),
            'material_results':descriptor(work / 'producer_ingestion_receipt.json')}
    for letter in ('A','B'):
        for field,key in (('archive','snapshot'),('track','radial_track'),('log','snapshot_log')):
            inputs[f'{key}_{letter}']=states[letter][field]
    declaration=dict(schema_version=1,experiment_id=spec['experiment_id'],cases=['AAA','ABA'],
        production_config=config,budgets=budget,inputs=inputs,
        case_spec=descriptor(work / 'case_spec.json'),rank_addendum=descriptor(work / 'rank_addendum.json'),
        resource_roots=roots)
    dump_json(work / 'declaration.json',declaration)
    info=module.preflight(work / 'declaration.json',sha256(work / 'declaration.json'))
    dump_json(work / 'preflight.json',info)
    print(json.dumps({'classification':'QUALIFIED_AB_LEGACY_BOOT_PREFLIGHT_PASS',
        'declaration':descriptor(work / 'declaration.json'), 'runner':descriptor(work / 'production_runner_qualified.py'),
        'production_output':str(output)},indent=2))


if __name__ == '__main__':
    main()
