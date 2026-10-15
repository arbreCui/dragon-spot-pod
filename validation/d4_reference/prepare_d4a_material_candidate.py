"""Prepare the reviewed 28-nuclide library route; never invoke native engines.

The seven Mo isotopes stay on the existing production binary, read-only.
This prepares inputs and exact-record expectations, not a candidate library or
a material solve. A separate authorization is required for either operation.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import signal
import sys
import time
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'validation/artifacts'
MO = {'Mo92', 'Mo94', 'Mo95', 'Mo96', 'Mo97', 'Mo98', 'Mo100'}
LAST = {'Pu241', 'Pu242', 'U235', 'U238'}
RETAIN = {'Am241', 'Pu238', 'Pu239', 'Pu240'}
COV = ART / 'd4a-material-reference-coverage-20261002'
PREP = ART / 'd4a-final-four-fuel-temperature-prepared-20261002'
RUN = ART / 'd4a-final-four-fuel-temperature-run-20261002'
REVIEW = Path(str(RUN) + '-review')
OLD = ART / 'd4a-fe56-actual-temperature-material-retained-input-prepared-20260930'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def tree_digest(records):
    """Typed stored-value image, independent of ASCII record ordering."""
    h = hashlib.sha256()
    for key in sorted(records, key=lambda x: json.dumps(x)):
        kind, value = records[key]
        if kind in (1, 2, 4):
            array = np.asarray(value, dtype={1: '<i4', 2: '<f4', 4: '<f8'}[kind])
            require(np.isfinite(array).all(), 'nonfinite library record')
            payload = array.tobytes()
        elif kind in (0, 10, 99):
            require(isinstance(value, int), 'invalid directory/list count')
            payload = value.to_bytes(8, 'little', signed=True)
        else:
            require(kind == 3 and isinstance(value, str), 'unsupported library record')
            payload = value.encode('ascii')
        header = json.dumps([key, kind, len(payload)], separators=(',', ':')).encode()
        h.update(len(header).to_bytes(8, 'little') + header + payload)
    return h.hexdigest()


def candidate_procedure(original):
    anchor = 'STRING Library := "DLIB8R1_370" ;'
    require(original.count(anchor) == 1, 'original library declaration changed')
    result = original.replace(anchor, 'STRING Library := "DLIB_ACTUAL" ;')
    for alloy in ('AIM1', 'EM10'):
        first = f"    Mo92_{alloy} = 'Mo92'"
        last = f"    Si_{alloy} = 'Si28'" if alloy == 'AIM1' else "    C_EM10 = 'C12'"
        require(result.count(first) == result.count(last) == 1, 'Mo block boundary changed')
        result = result.replace(first, "    MIXS LIB: DRAGON FIL: 'DLIB8R1_370'\n" + first)
        result = result.replace(last, '    MIXS LIB: DRAGON FIL: <<Library>>\n' + last)
    # Removing precisely these file-routing edits must recover the old deck.
    recovered = result.replace('STRING Library := "DLIB_ACTUAL" ;', anchor)
    recovered = recovered.replace("    MIXS LIB: DRAGON FIL: 'DLIB8R1_370'\n", '')
    # The original first MIXS is retained; only the two restoration lines added above are removed.
    for line in ("    Si_AIM1 = 'Si28'", "    C_EM10 = 'C12'"):
        recovered = recovered.replace('    MIXS LIB: DRAGON FIL: <<Library>>\n' + line, line)
    require(recovered == original, 'non-routing material change')
    selected = 'DLIB_ACTUAL'
    routing = []
    for line in result.splitlines():
        if 'MIXS LIB: DRAGON FIL:' in line:
            selected = 'DLIB8R1_370' if "'DLIB8R1_370'" in line else 'DLIB_ACTUAL'
        elif ' = ' in line and '<<N_' in line:
            ref = line.split(' = ', 1)[1].split()[0].strip("'")
            require((selected == 'DLIB8R1_370') == (ref in MO), 'wrong library routing')
            routing.append(dict(nuclide=ref, library=selected))
    require(len(routing) == 59, 'material must retain 59 isotope entries')
    require(Counter(r['nuclide'] for r in routing if r['library'] == 'DLIB8R1_370') ==
            Counter({name: 2 for name in MO}), 'Mo routing count')
    return result, routing


def material_deck(temperature):
    require(temperature in (650, 750, 850), 'undeclared material temperature')
    return f'''* PREPARED ONLY: no transport; separate native budget required.
SEQ_ASCII glow_rnr :: FILE './geometry.dat' ;
LINKED_LIST MICROLIB2 META ;
SEQ_ASCII MICRO :: FILE './microlib.ascii' ;
SEQ_ASCII MACRO :: FILE './macro.ascii' ;
SEQ_ASCII INFO :: FILE './metadata.ascii' ;
MODULE UTL: DELETE: END: ;
PROCEDURE D4ActualTone rnr_cc rnr_interpol ;
REAL T_comb := {temperature}.0 ;
REAL T_clad := 620.0 ;
REAL T_Na := 475.0 ;
MICROLIB2 := D4ActualTone glow_rnr ::
  <<T_comb>> <<T_clad>> <<T_Na>> ;
MICRO := MICROLIB2 ;
MACRO := MICROLIB2 :: STEP UP MACROLIB ;
META := MICROLIB2 ;
META := UTL: META :: EDIT 0 DEL ISOTOPESLIST DEL MACROLIB ;
INFO := META ;
ECHO "D4A-ACTUAL-MATERIAL{temperature}-COMPLETE" ;
META MICROLIB2 := DELETE: META MICROLIB2 ;
END: ;
QUIT "LIST" .
'''


def prepare(destination):
    start = time.monotonic()
    require(not destination.exists(), 'never overwrite preparation')
    pins, trusted = {}, {}

    def checked(path, digest):
        path = Path(path)
        require(sha(path) == digest, f'changed input: {path}')
        require(str(path) not in pins or pins[str(path)] == digest, 'conflicting identity')
        pins[str(path)] = digest
        return path

    def seal(folder, expected, name='result.sha256'):
        path = checked(folder/name, expected)
        result = {}
        for line in path.read_text().splitlines():
            digest, relative = line.split(maxsplit=1)
            target = folder/relative
            require(target.resolve().is_relative_to(folder.resolve()), 'manifest path escape')
            require(str(target) not in result, 'duplicate manifest path')
            result[str(target)] = digest
        return result

    def saved(path, source):
        return json.loads(checked(path, source[str(path)]).read_text())

    cov_seal = seal(COV, '4b261b5ab86dbf999ad1a3aa337288f24d8752ab203441cacb6346b20a7acfb3')
    coverage = saved(COV/'coverage.json', cov_seal)
    reviewed = seal(REVIEW, '80e13092ede89ae055090fa94188a54b1736a2577391d6e181478f4053e43421')
    final = saved(REVIEW/'review.json', reviewed)
    require(final['status'] == 'PASS_FINAL_FOUR_FUEL_REFERENCES_ONLY', 'last four not reviewed')
    require({r['nuclide'] for r in final['cases']} == LAST, 'last-four membership')
    for source in (coverage['inputs'], saved(REVIEW/'inputs.json', reviewed),
                   seal(RUN, final['original_result_manifest_sha256'])):
        for path, digest in source.items():
            require(path not in trusted or trusted[path] == digest, 'conflicting accepted identity')
            trusted[path] = digest
    retained = saved(PREP/'retained_review.json', trusted)
    require(retained['status'] == 'PASS_FOUR_SAVED_FUEL_REFERENCES_ONLY', 'retained four not reviewed')
    require({r['nuclide'] for r in retained['cases']} == RETAIN, 'retained-four membership')
    old_seal = seal(OLD, '5fe9df89fe51c4c1e1cea308be08343160d9deb2f0639ca6afa0dda36d535a02', 'prepared.sha256')
    assets = {key: value for key, value in saved(OLD/'preflight.json', old_seal)['assets'].items()
              if key != 'candidate_ascii'}
    for row in assets.values():
        checked(row['path'], row['sha256'])
    require(assets['Dragon']['sha256'] == '873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef', 'runtime epoch')

    base = Path('/Users/wen/dragon-5.1/Dragon/irena_core/colorset_rebuild_20260527/ce_compare')
    paper = base/'mc2027_csd_rr_evidence_v1_20260909/paper_parallel_20260910'
    sys.path[:0] = [str(base/'fullpitch_pnl_s30_b0_closure_v1_20260907'),
                    str(paper/'angular_tracking/p3_pilot'), str(paper/'finegroup_acceptance')]
    import native_records as nr
    import stream_records as sr
    import independent_audit as adapter
    from audit_fe56_temperature_interpolation import weights
    for module in (nr, sr, adapter):
        expected = trusted.get(str(Path(module.__file__)), sha(module.__file__))
        checked(module.__file__, expected)
    checked(__file__, sha(__file__))
    checked(ROOT/'validation/d4_reference/audit_fe56_temperature_interpolation.py',
            sha(ROOT/'validation/d4_reference/audit_fe56_temperature_interpolation.py'))

    def decode(path, library=False):
        raw = path.read_bytes()
        if library:
            raw, _ = adapter.strict_xsm(raw)
        one = nr.decode(raw)
        require(one == sr.decode_stream(io.BytesIO(raw))[0], 'independent readers disagree')
        return one

    baseline = ART/'d4a-fe56-library-path-audit-20260929'
    energy = None
    for plane in (1, 2, 3):
        p = checked(baseline/f'meta{plane}.ascii', trusted[str(baseline/f'meta{plane}.ascii')])
        e = np.asarray(nr.data(decode(p), ('ENERGY',)), dtype='<f4').tobytes()
        require(energy is None or e == energy, 'baseline energy differs')
        energy = e
    rows, sources = [], []
    required = {r['nuclide'] for r in coverage['rows']}
    require(len(required) == 35 and MO <= required, '35-nuclide scope')
    for name in sorted(required - MO):
        needs = [r for r in coverage['rows'] if r['nuclide'] == name]
        libraries = {r['library'] for r in needs}
        require(len(libraries) == 1, 'inconsistent reference source')
        library = RUN/name/'expanded/high/dragr/tape30' if name in LAST else Path(libraries.pop())
        if name in RETAIN:
            accepted = next(r for r in retained['cases'] if r['nuclide'] == name)
            require(accepted['library'] == str(library) and accepted['sha256'] == trusted[str(library)], 'retained library drift')
        checked(library, trusted[str(library)])
        records = decode(library, True)
        require({k[0] for k in records if len(k) > 1} == {name}, 'unexpected isotope subtree')
        e = np.asarray(nr.data(records, ('ENERGY',)), dtype='<f4')
        require(len(e) == 371 and np.all(np.diff(e) < 0) and np.all(e > 0), 'energy grid shape')
        require(e.tobytes() == energy, 'reference energy bit image differs')
        temperatures = nr.data(records, (name, 'TEMPERATURE'))
        for needed in needs:
            w = weights(temperatures, needed['temperature_K'], 3)
            index = [i for i, t in enumerate(temperatures) if np.float32(t).tobytes() == np.float32(needed['temperature_K']).tobytes()]
            require(len(index) == 1 and np.count_nonzero(w) == 1 and w[index[0]] == 1, 'not an exact temperature node')
            rows.append(dict(needed, library=str(library), data_status='REVIEWED_DIRECT_NODE', node=index[0]+1))
        subtree = {k: v for k, v in records.items() if k[0] == name}
        sources.append(dict(nuclide=name, path=str(library), sha256=pins[str(library)],
                            records=len(subtree), typed_subtree_sha256=tree_digest(subtree),
                            temperatures_K=list(temperatures)))
    rows.extend(dict(r, library=assets['full_library']['path']) for r in coverage['rows'] if r['nuclide'] in MO)
    require(len(rows) == 79 and len(sources) == 28, 'coverage count')
    require(sum(len(r['locations']) for r in rows) == 177, 'three-plane entry count')
    procedure = checked(ROOT/'data/SpotD4Tone.c2m', 'f7882be83d8a8aea91c94b1475eaa259b1265e8d7976e828fe3b76857ef98d74')
    text, routing = candidate_procedure(procedure.read_text())
    for path, digest in pins.items():
        require(sha(path) == digest, 'input changed during preparation')

    destination.mkdir(parents=True)
    (destination/'D4ActualTone.c2m').write_text(text)
    for temperature in (650, 750, 850):
        (destination/f'material{temperature}.x2m').write_text(material_deck(temperature))
    (destination/'merge.inp').write_text('dragr\n0 0 0 0 0 29 30 0 /\nstop\n')
    for name in ('import.x2m', 'export.x2m'):
        source = checked(OLD/name, old_seal[str(OLD/name)])
        (destination/name).write_bytes(source.read_bytes())
    result = dict(status='STATIC_MATERIAL_CANDIDATE_PREPARED_NOT_AUTHORIZED',
        finished_utc=datetime.now(timezone.utc).isoformat(), elapsed_s=time.monotonic()-start,
        native_engines_started=0, material_solves=0, candidate_library_created=False,
        energy_float32_sha256=hashlib.sha256(energy).hexdigest(),
        reviewed_references=28, direct_temperature_pairs=65, original_Mo_pairs=14,
        original_Mo_entries_per_plane=14, candidate_entries_per_plane=45,
        sources=sources, temperature_routes=rows, material_routing=routing, assets=assets,
        private_binary_alias='DLIB_ACTUAL', original_Mo_alias='DLIB8R1_370',
        merge_protocol='Read each selected source as tape29; use only the private accumulated tape30. Never feed the full production library into the merge. Exact subtree comparison and separate GANLIB reopen/export must precede material use.',
        native_authorization=None, inputs=pins,
        limits=['Static routing and node coverage only; not a native deck/parser or material acceptance.',
                'Mo remains on the unchanged production binary and still uses original interpolation.',
                'No new empirical coefficients, interpolation changes, clipping or relaxed gates.',
                'All 59 microscopic entries and six mixtures in all three material states need new validation.',
                'No material/TONE/transport/Picard/CE or production replacement is authorized.'])
    with (destination/'preparation.json').open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    with (destination/'result.sha256').open('x') as stream:
        for path in sorted(destination.iterdir()):
            if path.name != 'result.sha256':
                stream.write(f'{sha(path)}  {path.name}\n')
    print(json.dumps({k: result[k] for k in ('status', 'elapsed_s', 'reviewed_references', 'direct_temperature_pairs', 'original_Mo_pairs', 'native_engines_started')}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('180-second static preparation limit')))
    signal.alarm(180)
    with patch('subprocess.Popen', side_effect=AssertionError('native launch forbidden during preparation')):
        prepare(args.output)
