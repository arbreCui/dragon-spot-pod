#!/usr/bin/env python3
"""Prepare fresh, same-temperature A/B pin material and snapshot decks.

This module executes no native program. Atom densities remain computations in
the current corrected rnr_cc/rnr_interpol procedures, with Pu/U supplied as
procedure arguments. The 2012 alternative composition is a sensitivity case,
not a qualified IRENA design.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = Path('/Users/wen/dragon-5.1/Dragon/irena_colorset_assembly_pin')
CORRECTED = ORIGINAL/'pincell/results_new_materials_pincell_20260527/dragon'
CANDIDATE = ROOT/'validation/artifacts/d4a-actual-temperature-library-run-20261003/import/DLIB_370_bin'
CANDIDATE_SHA256 = 'e78b87094b67bd4d1bcdc3a5dd2beeb168318853a48321473bb9b86df5ba19cc'
PRODUCTION = Path('/Users/wen/draglib_output/shem370_endfb8r1_v5p1/draglibshem370_endfb8r1_v5p1.xsm')
PRODUCTION_SHA256 = '66b9a7b3e8534a54cf590db63a7c1dbd96b4a95c636f0e3a6eee5b219bbcc1e9'


def digest(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


@dataclass(frozen=True)
class MaterialConfig:
    pu_A: float = 0.21
    u_A: float = 0.79
    pu_B: float = 0.2436
    u_B: float = 0.7564
    fuel_C: float = 750.0
    clad_C: float = 620.0
    sodium_C: float = 475.0
    snapshot_eps: float = 2.5e-7
    mccg_eps: float = 1.0e-5
    maxout: int = 500
    track_angles: int = 48
    track_density: float = 100.0

    def validate(self) -> None:
        # This experiment fixes compositions and temperatures before results.
        # Pu is parameterized in the generated CLE procedure, not atom densities.
        if (self.pu_A, self.u_A, self.pu_B, self.u_B) != (0.21, 0.79, 0.2436, 0.7564):
            raise ValueError('only the declared A/B composition pair is admitted')
        if (self.fuel_C, self.clad_C, self.sodium_C) != (750.0, 620.0, 475.0):
            raise ValueError('all layers must retain the declared common temperatures')
        for name in ('snapshot_eps', 'mccg_eps', 'track_density'):
            value = getattr(self, name)
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f'{name} must be finite and positive')
        for name in ('maxout', 'track_angles'):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f'{name} must be a positive integer')


def sources() -> dict[str, Path]:
    return {
        'current_snapshot': ROOT/'data/SpotD4Snap.c2m',
        'rnr_cc.c2m': ROOT/'data/rnr_0burn_spot_proc/rnr_cc.c2m',
        'rnr_interpol.c2m': ROOT/'data/rnr_0burn_spot_proc/rnr_interpol.c2m',
        'corrected_rnr_cc': CORRECTED/'rnr_cc.c2m',
        'corrected_rnr_interpol': CORRECTED/'rnr_interpol.c2m',
        'geometry.dat': CORRECTED/'rnr_pincell.dat',
        'corrected_pin_deck': CORRECTED/'rnr_pincell_glow.x2m',
        'composition_provenance': ORIGINAL/'rnr_0burn.x2m',
    }


def load_sources(paths: dict[str, Path] | None = None) -> dict[str, str]:
    paths = sources() if paths is None else paths
    # The historical French CLE comments include Latin-1 bytes. Decode and
    # re-encode losslessly; never silently rewrite copied procedure identities.
    text = {name: path.read_text(encoding='latin-1') for name, path in paths.items()}
    for name in ('rnr_cc', 'rnr_interpol'):
        if text[f'{name}.c2m'] != text[f'corrected_{name}']:
            raise ValueError(f'{name}: corrected-20260527/current provenance differs')
    if '*REAL p_Pu p_U := 0.2436 0.7564 ;' not in text['composition_provenance']:
        raise ValueError('declared B composition provenance is missing')
    return text


def material_procedure(source: str) -> str:
    """Reuse current density calculation, with an explicit pin material map."""
    begin, end = 'REAL p_Pu38', 'ECHO "SpotD4Snap: T_comb='
    if source.count(begin) != 1 or source.count(end) != 1:
        raise ValueError('current material declaration anchors changed')
    calculation = source[source.index(begin):source.index(end)]
    if calculation.count('273.15 +') != 3 or 'rnr_cc ::' not in calculation:
        raise ValueError('current corrected temperature/density route changed')
    clad_begin = '    MIX 2 (*ACIER AIM1 GAINE COMBUSTIBLE*)'
    clad_end = '    MIX 6 (*ACIER EM10 BOITIER*)'
    if source.count(clad_begin) != 1 or source.count(clad_end) != 1:
        raise ValueError('current clad material anchors changed')
    clad = source[source.index(clad_begin):source.index(clad_end)]
    first, last = "    Mo92_AIM1 = 'Mo92'", "    Si_AIM1 = 'Si28'"
    if clad.count(first) != 1 or clad.count(last) != 1:
        raise ValueError('Mo routing anchors changed')
    clad = clad.replace(first, "    MIXS LIB: DRAGON FIL: 'DLIB8R1_370'\n" + first)
    clad = clad.replace(last, "    MIXS LIB: DRAGON FIL: 'DLIB_ACTUAL'\n" + last)
    fuel = '\n'.join(f"    {alias} = '{nuclide}' <<N_{alias}>> 1"
                     for alias, nuclide in [('U5', 'U235'), ('U8', 'U238'),
                        ('Pu38', 'Pu238'), ('Pu39', 'Pu239'), ('Pu40', 'Pu240'),
                        ('Pu41', 'Pu241'), ('Pu42', 'Pu242'), ('Am', 'Am241')])
    return '''* Fresh pin material; density formulas are the corrected current procedures.
PARAMETER MICROLIB2 glow ::
  ::: LINKED_LIST MICROLIB2 ;
  ::: SEQ_ASCII glow ; ;
LINKED_LIST MICROLIB TRACK_T ;
SEQ_BINARY TRACK_T_f ;
MODULE LIB: SALT: TONE: DELETE: END: ;
PROCEDURE rnr_cc rnr_interpol ;
REAL p_Pu p_U T_comb T_clad T_Na ;
:: >>p_Pu<< >>p_U<< >>T_comb<< >>T_clad<< >>T_Na<< ;
''' + calculation + '''MICROLIB := LIB: ::
    EDIT 0 NMIX 8 CTRA APOL ANIS 3
    MIXS LIB: DRAGON FIL: 'DLIB_ACTUAL'
    MIX 7 (*MOX inner fuel ring*) <<T_comb_K>>
''' + fuel + '''
    MIX 1 (*SODIUM*) <<T_Na_K>> NOEV
    Na = 'Na23' <<N_Na>>
    MIX 7 <<T_comb_K>>
    O = 'O16' <<N_O>> NOEV
    MIX 6 COMB 7 1.0
    MIX 5 COMB 7 1.0
    MIX 4 COMB 7 1.0
''' + clad + '''    MIX 8 (*He central hole*) <<T_comb_K>> NOEV
    He4int = 'He4' <<N_He_1>>
    MIX 3 (*He pellet-clad gap*) <<T_clad_K>> NOEV
    He4ext = 'He4' <<N_He_2>>
;
TRACK_T TRACK_T_f := SALT: glow ::
  EDIT 0 ANIS 1 TISO 48 100.0 LONG MERGMIX ;
MICROLIB2 := TONE: MICROLIB TRACK_T TRACK_T_f ::
  EDIT 1 MXIT 20 EPS 1.0E-5 TRAN PIJ ;
TRACK_T TRACK_T_f := DELETE: TRACK_T TRACK_T_f ;
MICROLIB := DELETE: MICROLIB ;
END: ;
'''


DIMENSION_GATE = '''MACRO := MICROLIB2 :: STEP UP MACROLIB ;
GREP: MACRO :: GETVAL 'STATE-VECTOR' 1 >>ng<< ;
GREP: MACRO :: GETVAL 'STATE-VECTOR' 2 >>nmix<< ;
GREP: MACRO :: GETVAL 'STATE-VECTOR' 4 >>nfis<< ;
IF ng 370 <> THEN
  ECHO "AXMAT: wrong energy-group count" ; ABORT: ;
ENDIF ;
IF nmix 8 <> THEN
  ECHO "AXMAT: wrong mixture count" ; ABORT: ;
ENDIF ;
IF nfis 32 <> THEN
  ECHO "AXMAT: expected 32 fission components" ; ABORT: ;
ENDIF ;
'''


def build_decks(config: MaterialConfig = MaterialConfig(),
                source_text: dict[str, str] | None = None) -> dict[str, str]:
    config.validate()
    text = load_sources() if source_text is None else source_text
    procedure = material_procedure(text['current_snapshot'])
    decks: dict[str, str] = {}
    for state in ('A', 'B'):
        pu, uranium = getattr(config, f'pu_{state}'), getattr(config, f'u_{state}')
        decks[f'{state}/AxMatTone.c2m'] = procedure
        decks[f'{state}/material.x2m'] = f'''* {state}: declared same-temperature composition sensitivity, no transport.
SEQ_ASCII glow :: FILE './geometry.dat' ;
XSM_FILE MAT_OUT :: FILE './material.xsm' ;
SEQ_ASCII MICRO_OUT :: FILE './microlib.ascii' ;
SEQ_ASCII MACRO_OUT :: FILE './macro.ascii' ;
SEQ_ASCII META_OUT :: FILE './metadata.ascii' ;
LINKED_LIST MICROLIB2 MACRO META ;
MODULE GREP: ABORT: UTL: END: ;
PROCEDURE AxMatTone rnr_cc rnr_interpol ;
INTEGER ng nmix nfis ;
MICROLIB2 := AxMatTone glow ::
  {pu:.4f} {uranium:.4f} {config.fuel_C:.1f} {config.clad_C:.1f} {config.sodium_C:.1f} ;
''' + DIMENSION_GATE + f'''MAT_OUT := MICROLIB2 ;
MICRO_OUT := MICROLIB2 ;
MACRO_OUT := MACRO ;
META := MICROLIB2 ;
META := UTL: META :: EDIT 0 DEL ISOTOPESLIST DEL MACROLIB ;
META_OUT := META ;
ECHO "AXMAT-MATERIAL-{state}-COMPLETE" ;
END: ;
QUIT "LIST" .
'''
        decks[f'{state}/snapshot.x2m'] = f'''* Fresh TYPE-K snapshot from this state's separately sealed TONE material.
SEQ_ASCII glow :: FILE './geometry.dat' ;
SEQ_BINARY TRACK_f :: FILE './radial_track.bin' ;
XSM_FILE MAT_IN :: FILE './material.xsm' ;
XSM_FILE SNAP_OUT :: FILE './snapshot_{state}.xsm' ;
LINKED_LIST MICROLIB2 MACRO TRACK SYSTEM FLUX SNAP ;
MODULE SALT: MCCGT: ASM: FLU: GREP: BACKUP: ABORT: END: ;
INTEGER ng nmix nfis ;
REAL k_snap ;
MICROLIB2 := MAT_IN ;
''' + DIMENSION_GATE + f'''TRACK TRACK_f := SALT: glow ::
  EDIT 0 ANIS 1 TISO {config.track_angles} {config.track_density:.8E} LONG ;
TRACK := MCCGT: TRACK TRACK_f ::
  EDIT 0 GAUS 4 AAC 80 TMT STIS 1 EPSI {config.mccg_eps:.8E} MCU 10000 ;
SYSTEM := ASM: MICROLIB2 TRACK TRACK_f :: EDIT 0 ARM ;
FLUX := FLU: SYSTEM MICROLIB2 TRACK TRACK_f ::
  EDIT 1 TYPE K EXTE {config.maxout} {config.snapshot_eps:.8E}
  UNKT {config.snapshot_eps:.8E} THER {config.snapshot_eps:.8E} ;
GREP: FLUX :: GETVAL 'K-EFFECTIVE' 1 >>k_snap<< ;
SNAP := BACKUP: TRACK :: LIST 1 ITEM 1 ;
SNAP := BACKUP: SNAP MICROLIB2 :: ITEM 1 ;
SNAP := BACKUP: SNAP SYSTEM :: ITEM 1 ;
SNAP := BACKUP: SNAP FLUX :: ITEM 1 ;
SNAP_OUT := SNAP ;
ECHO "AXMAT-SNAPSHOT-{state}-COMPLETE" k_snap ;
END: ;
QUIT "LIST" .
'''
    return decks


def write_inputs(output: Path, config: MaterialConfig = MaterialConfig(),
                 candidate: Path = CANDIDATE, production: Path = PRODUCTION) -> dict:
    paths = sources()
    text = load_sources(paths)
    decks = build_decks(config, text)
    candidate_hash, production_hash = digest(candidate), digest(production)
    if candidate_hash != CANDIDATE_SHA256:
        raise ValueError('candidate library differs from the reviewed 28-nuclide roundtrip')
    if production_hash != PRODUCTION_SHA256:
        raise ValueError('original Mo library differs from the preserved production input')
    source_hashes = {name: {'path': str(path.resolve()), 'sha256': digest(path)}
                     for name, path in paths.items()}
    output.mkdir(parents=True, exist_ok=False)
    generated = dict(decks)
    for state in ('A', 'B'):
        for name in ('geometry.dat', 'rnr_cc.c2m', 'rnr_interpol.c2m'):
            generated[f'{state}/{name}'] = text[name]
    for name, contents in generated.items():
        target = output/name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding='latin-1')
    manifest = {
        'schema_version': 1, 'classification': 'PREPARED_INPUTS_ONLY_NO_NATIVE_EXECUTION',
        'config': asdict(config), 'source_files': source_hashes,
        'generated_sha256': {name: digest(output/name) for name in generated},
        'required_staging_per_state': {
            'DLIB_ACTUAL': {'path': str(candidate.resolve()), 'sha256': candidate_hash},
            'DLIB8R1_370': {'path': str(production.resolve()), 'sha256': production_hash}},
        'material_entries_expected': 62, 'fission_components_expected': 32,
        'geometry': {'regions': 8, 'hex_side_cm': 0.61776479,
                     'radii_cm': [0.11, 0.308712, 0.381084, 0.412536, 0.4225, 0.435, 0.485],
                     'fuel_mixtures_inner_to_outer': [7, 6, 5, 4],
                     'other_mixtures': {'Na': 1, 'AIM1': 2, 'gap_He': 3, 'hole_He': 8}},
        'snapshots': {state: {'material_deck': f'{state}/material.x2m',
            'material': f'{state}/material.xsm', 'material_log': f'{state}/material.log',
            'deck': f'{state}/snapshot.x2m', 'archive': f'{state}/snapshot_{state}.xsm',
            'log': f'{state}/snapshot.log', 'radial_track': f'{state}/radial_track.bin',
            'marker': f'AXMAT-SNAPSHOT-{state}-COMPLETE', 'archive_slots': 1,
            'archive_objects': ['TRACK', 'MICROLIB2', 'SYSTEM', 'FLUX']}
            for state in ('A', 'B')},
        'training_slots': ['A', 'B', 'A'], 'cases': {'AAA': ['A', 'A', 'A'], 'ABA': ['A', 'B', 'A']},
        'composition_scope': 'B derives from a commented alternative at rnr_0burn.x2m:29; declared sensitivity only, not validated IRENA design.',
        'execution_scope': 'No engines started; protocol, runtime, caps and completed material/snapshot checks must be frozen separately.',
    }
    (output/'material_inputs.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--candidate-library', type=Path, default=CANDIDATE)
    parser.add_argument('--production-library', type=Path, default=PRODUCTION)
    args = parser.parse_args()
    config = MaterialConfig(**({} if args.config is None else json.loads(args.config.read_text())))
    result = write_inputs(args.output, config, args.candidate_library, args.production_library)
    print(result['classification'])


if __name__ == '__main__':
    main()
