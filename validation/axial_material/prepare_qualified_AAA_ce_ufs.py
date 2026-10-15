"""Predeclare one native weighted-UFS diagnostic; never modify prior evidence."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
PARENT = ART / 'axial-material-ce-qualified-AB-compensated-20261004'
OUT = ART / 'axial-material-ce-qualified-AAA-ufs-20261004'
PRODUCTION = ART / 'axial-material-production-qualified-AB-compensated-20261004'
PREPARED_SHA = '2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7'
PARENT_EXEC_SHA = '49404f9db97d3908df2c279f40b620ec7b9a0db80ce9f8935a8d6de77a03701f'
PARENT_ASSESS_SHA = 'da448e5668d155a32f88e68d5cca2a302dd7fa9ebbc7e4584f6b5841c3f88b8a'
COMMIT = 'e542b2f035e397a647cc3ad0ae39946b1ad81e7b'
SOURCE = Path('/Users/wen/openmc-workspace/src')
MESH = dict(id=2, dimension=[1, 1, 12], lower_left=[-0.61776479, -0.61776479, 0.0], upper_right=[0.61776479, 0.61776479, 150.0])


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def pin(path):
    return dict(path=str(Path(path).resolve()), sha256=digest(path))


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def verify(files):
    for name, wanted in files.items():
        if digest(name) != wanted:
            raise ValueError('frozen evidence changed: ' + name)


def ufs_settings(folder, smoke):
    original = ET.parse(PARENT / 'AAA/settings.xml')
    root = original.getroot()
    ET.SubElement(root, 'ufs_mesh').text = str(MESH['id'])
    mesh = ET.SubElement(root, 'mesh', id=str(MESH['id']))
    for name in ('dimension', 'lower_left', 'upper_right'):
        ET.SubElement(mesh, name).text = ' '.join(map(str, MESH[name]))
    if smoke:
        root.find('particles').text = '1000'
        root.find('inactive').text = '10'
        root.find('batches').text = '20'
        root.find('state_point/batches').text = ' '.join(map(str, range(11, 21)))
        source = root.find('source_point')
        source.find('write').text = 'true'
        ET.SubElement(source, 'batches').text = '20'
        ET.SubElement(source, 'separate').text = 'false'
    ET.indent(original, space='  ')
    original.write(folder / 'settings.xml', encoding='UTF-8', xml_declaration=True)
    # Removing just the two declared UFS elements must recover every original
    # setting in the formal run. Smoke additionally changes only sample/output.
    replay = ET.parse(folder / 'settings.xml').getroot()
    replay.remove(replay.find('ufs_mesh'))
    added = [node for node in replay.findall('mesh') if node.get('id') == '2']
    if len(added) != 1:
        raise ValueError('ambiguous UFS mesh')
    replay.remove(added[0])
    if smoke:
        base = ET.parse(PARENT / 'AAA/settings.xml').getroot()
        for name in ('particles', 'inactive', 'batches', 'state_point', 'source_point'):
            replay.remove(replay.find(name))
            base.remove(base.find(name))
    else:
        base = ET.parse(PARENT / 'AAA/settings.xml').getroot()
    def value(node):
        return (node.tag, tuple(sorted(node.attrib.items())), (node.text or '').strip(), tuple(value(child) for child in node))
    if value(replay) != value(base):
        raise ValueError('undeclared physical, source, temperature or statistical setting change')


def stage(folder, smoke, common):
    folder.mkdir()
    for name in ('materials.xml', 'geometry.xml', 'tallies.xml'):
        shutil.copy2(PARENT / 'AAA' / name, folder / name)
        if digest(folder / name) != digest(PARENT / 'AAA' / name):
            raise ValueError('physical XML changed')
    ufs_settings(folder, smoke)
    contract = json.loads((PARENT / 'AAA/reference_contract.json').read_text())
    contract['input_hashes']['settings.xml'] = digest(folder / 'settings.xml')
    contract['source_sampling_diagnostic'] = dict(method='native_weighted_uniform_fission_site', mesh=MESH,
        original_independent_source_unchanged=True, physics_changed=False,
        expectation_compensation='Native birth multiplicity multiplied by v_i/s_i, birth weight s_i/v_i, and starting total source weight normalized to particles; no score clipping or postprocessing reweighting.')
    if smoke:
        contract['config'].update(particles=1000, inactive=10, active=10)
        contract['statepoint_batches'] = list(range(11, 21))
        contract['scope'] = 'Activation/weight/coverage smoke only; never scientific qualification or a source-stationarity test.'
    write_new(folder / 'reference_contract.json', contract)
    return dict(common, wall_seconds=120 if smoke else 5400,
        source_sampling_declaration=str(OUT / 'declaration.json'),
        scope='Single native UFS diagnostic. Physical XML and formal original statistical/engineering gates retained; no automatic retry.')


def prepare():
    if digest(PRODUCTION / 'prepared.json') != PREPARED_SHA or digest(PARENT / 'AAA/execution.json') != PARENT_EXEC_SHA or digest(PARENT / 'AAA/reference_assessment.json') != PARENT_ASSESS_SHA:
        raise ValueError('parent evidence changed')
    parent = json.loads((PARENT / 'AAA/execution.json').read_text())
    verify(parent['files'])
    code = [SOURCE / 'src' / name for name in ('eigenvalue.cpp', 'settings.cpp', 'physics.cpp', 'mesh.cpp', 'simulation.cpp', 'state_point.cpp')]
    if subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip() != COMMIT:
        raise ValueError('native source checkout no longer matches executable commit')
    if subprocess.check_output(['git', '-C', str(SOURCE), 'diff', 'HEAD', '--', *[str(p.relative_to(SOURCE)) for p in code]], text=True):
        raise ValueError('UFS implementation source modified')
    OUT.mkdir(exist_ok=False)
    (OUT / 'runtime').mkdir()
    for name in ('ce_execution.py', 'production_runner.py', 'production_inputs.py'):
        shutil.copy2(PARENT / 'runtime' / name, OUT / 'runtime' / name)
    for name in ('statistical_rules.json', 'balance_symmetry_rules.json'):
        shutil.copy2(PARENT / name, OUT / name)
    addendum = json.loads((PARENT / 'resource_addendum.json').read_text())
    addendum.update(parent_resource_addendum=pin(PARENT / 'resource_addendum.json'),
        scope='One predeclared UFS formal diagnostic after activation smoke, same 17.5 million histories and 5400 second hard cap; no repeat or threshold change.')
    write_new(OUT / 'resource_addendum.json', addendum)
    declaration = dict(schema='AXMAT_NATIVE_UFS_SOURCE_DIAGNOSTIC_V1', declared_unix=time.time(),
        parent_execution=pin(PARENT / 'AAA/execution.json'), parent_assessment=pin(PARENT / 'AAA/reference_assessment.json'),
        production_prepared=pin(PRODUCTION / 'prepared.json'), implementation=pin(__file__),
        native_commit=COMMIT, source_files={str(p): digest(p) for p in code}, native_executable=pin(parent['executable']),
        mesh=MESH, mesh_rationale='One transverse bin spanning the full hexagon; 12 equal axial bins chosen from the preexisting tally cells before execution. All bins contain fissionable material.',
        smoke=dict(particles=1000, inactive=10, active=10, seed=310031, wall_seconds=120, source_bank_at_final=True),
        formal=dict(particles=50000, inactive=100, active=250, seed=310031, wall_seconds=5400, source_bank_output=False),
        threads=1, new_children_at_once=1, automatic_retries=0, physical_inputs_changed=False, original_thresholds_changed=False,
        analysis=dict(block_lengths=[5, 10], original_rules=pin(PARENT / 'statistical_rules.json'), current_rules=pin(PARENT / 'balance_symmetry_rules.json')),
        formal_admission='Smoke must exit zero, preserve physical/tally XML, and return 1000 finite positive nonunit source weights located in every declared UFS axial bin. Source mesh/source weighting judged from native final bank, not guessed from a setting.',
        scientific_decision='Re-run every unchanged original AAA statistical, engineering and current/symmetry gate; failed or inconclusive results remain unqualified. Never select a new UFS mesh from this outcome. Never tune to the SPOT result.',
        links=['https://docs.openmc.org/en/stable/methods/eigenvalue.html', 'https://docs.openmc.org/en/stable/io_formats/settings.html'],
        interpretation='Native UFS redistributes fission-site sampling and compensates weights; it does not establish faster decorrelation or independent accuracy by itself.')
    write_new(OUT / 'declaration.json', declaration)
    common = copy.deepcopy(parent)
    common.update(resource_addendum=str(OUT / 'resource_addendum.json'),
        resource_roots=sorted(str(p.resolve()) for p in ART.glob('axial-material-*') if p.is_dir()))
    smoke = stage(OUT / 'AAA-smoke', True, common)
    formal = stage(OUT / 'AAA', False, common)
    audit = dict(status='PASS', case='AAA', physical_and_tally_XML_identical=True,
        formal_setting_delta=['add ufs_mesh=2', 'add regular mesh 2 with dimension 1x1x12 over original box'],
        original_source_entropy_and_temperature_settings_unchanged=True, original_formal_samples_seeds_and_outputs_unchanged=True,
        original_rules_unchanged=True, parent_reference_qualified=False,
        files={str(p): digest(p) for p in [*code, *[OUT / name for name in ('declaration.json', 'statistical_rules.json', 'balance_symmetry_rules.json')],
            *[OUT / 'AAA' / name for name in ('settings.xml', 'materials.xml', 'geometry.xml', 'tallies.xml', 'reference_contract.json')]]})
    write_new(OUT / 'input_sampling_review.json', audit)
    # Freeze all current inputs. A future smoke receipt is not guessed or
    # included in the formal manifest; formal admission binds it separately.
    files = dict(parent['files'])
    files.update({str(p.resolve()): digest(p) for p in OUT.rglob('*') if p.is_file()})
    files[str(Path(__file__).resolve())] = digest(__file__)
    files.update({str(p): digest(p) for p in code})
    for folder, execution in ((OUT / 'AAA-smoke', smoke), (OUT / 'AAA', formal)):
        execution['files'] = files
        write_new(folder / 'execution.json', execution)
    print(json.dumps(dict(classification='UFS_DIAGNOSTIC_PREDECLARED_NO_TRANSPORT',
        smoke=pin(OUT / 'AAA-smoke/execution.json'), formal=pin(OUT / 'AAA/execution.json')), indent=2))


def admit():
    declaration = json.loads((OUT / 'declaration.json').read_text())
    verify(declaration['source_files'])
    import h5py
    import numpy as np
    smoke = OUT / 'AAA-smoke'
    native = json.loads((smoke / 'native_result.json').read_text())
    if native['status'] != 'NATIVE_COMPLETE_PENDING_INDEPENDENT_ANALYSIS' or native['returncode'] != 0 or native['error'] is not None:
        raise ValueError('activation smoke failed; no formal launch')
    verify({str(smoke / name): wanted for name, wanted in native['outputs'].items()})
    with h5py.File(smoke / 'statepoint.20.h5') as stream:
        bank = stream['source_bank'][()]
        weights = bank['wgt']
        position = np.column_stack([bank['r'][name] for name in ('x', 'y', 'z')])
        if len(bank) != 1000 or not np.all(np.isfinite(position)) or not np.all(np.isfinite(weights)) or not np.all(weights > 0):
            raise ValueError('native source bank is incomplete/nonfinite/nonpositive')
        if np.all(weights == 1) or float(weights.max() - weights.min()) < 1e-10:
            raise ValueError('nonunit compensated source weights not observed')
        lower = np.array(MESH['lower_left']); upper = np.array(MESH['upper_right'])
        if np.any(position < lower) or np.any(position >= upper):
            raise ValueError('native source bank outside UFS mesh')
        bins = np.floor(position[:, 2] / 12.5).astype(int)
        counts = np.bincount(bins, minlength=12)
        if np.any(counts == 0):
            raise ValueError('UFS activation smoke has an empty axial bank bin')
        weighted = np.bincount(bins, weights=weights, minlength=12)
    original = json.loads((PARENT / 'AAA/measurement_admission.json').read_text())
    for name in ('prepared', 'AAA_status', 'final_seal', 'input_equivalence', 'production_checks', 'implementation'):
        record = original[name]
        if digest(record['path']) != record['sha256']:
            raise ValueError('parent saved fixed point/input measurement admission changed')
    formal = OUT / 'AAA'
    if any((formal / name).exists() for name in ('run_claim.json', 'openmc.log', 'native_result.json', 'measurement_admission.json')):
        raise ValueError('formal evidence already exists; no retry')
    smoke_receipt = dict(status='PASS', scientific_qualification=False, native_result=pin(smoke / 'native_result.json'),
        final_statepoint=pin(smoke / 'statepoint.20.h5'), source_count=len(bank), min_weight=float(weights.min()),
        max_weight=float(weights.max()), sum_weight=float(weights.sum()), axial_counts=counts.tolist(), axial_weight_sums=weighted.tolist(),
        all_source_sites_inside_mesh=True, all_axial_bins_nonempty=True, physical_input_review=pin(OUT / 'input_sampling_review.json'),
        scope='Actual native weighted-UFS activation only; smoke samples do not test source convergence or accuracy.')
    write_new(OUT / 'smoke_activation_receipt.json', smoke_receipt)
    receipt = dict(original, CE_manifest=pin(formal / 'execution.json'), implementation=pin(__file__),
        parent_measurement_admission=pin(PARENT / 'AAA/measurement_admission.json'),
        sampling_declaration=pin(OUT / 'declaration.json'), sampling_review=pin(OUT / 'input_sampling_review.json'),
        smoke_activation=pin(OUT / 'smoke_activation_receipt.json'),
        scope='Same saved AAA fixed point and identical physical/tally inputs admitted only to the independently weighted-UFS diagnostic; no accuracy qualification.')
    write_new(formal / 'measurement_admission.json', receipt)
    print(json.dumps(dict(classification='UFS_ACTIVATION_PASS_FORMAL_ADMITTED', admission=pin(formal / 'measurement_admission.json'), smoke=smoke_receipt), indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'admit'))
    args = parser.parse_args()
    prepare() if args.action == 'prepare' else admit()
