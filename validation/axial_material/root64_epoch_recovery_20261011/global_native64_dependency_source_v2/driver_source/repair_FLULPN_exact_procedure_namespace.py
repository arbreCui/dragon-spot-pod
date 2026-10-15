#!/usr/bin/env python3
"""Actual stdlib Source repair before any compilation or namespace freeze."""
import json
from pathlib import Path
import runpy
import os
import ast

OUT = Path(__file__).resolve().parent
module = runpy.run_path(str(OUT / 'generate_global_native64_dependency_source.py'))
Transform = module['Transform']
read_pin = module['read_pin']
fresh = module['fresh']
fresh_json = module['fresh_json']


def replace(path, raw):
    with path.open('wb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())


def main():
    source = OUT / 'SPOT_FLULPN_NATIVE64.f'
    proof_path = OUT / 'COMPLETE_NATIVE64_LOCAL_TRANSFORM_PROOFS.json'
    manifest_path = OUT / 'CURRENT_GLOBAL_NATIVE64_SOURCE_PINS_AND_BOUNDARIES.json'
    old_source, old_pin = read_pin(source)
    old_proof, old_proof_pin = read_pin(proof_path)
    old_manifest, old_manifest_pin = read_pin(manifest_path)
    assert old_pin['sha256'] == '65b73015ee0572ebba1a57b3a9beb4a2673fb6d4785e82a703577096108c3950'
    history = OUT / 'Source_repair_history'
    assert not history.exists()
    history.mkdir()
    fresh(history / 'ORIGINAL_UNFROZEN_FLULPN_BAD_HOLLERITH_NAMESPACE.f', old_source)
    fresh(history / 'ORIGINAL_UNFROZEN_LOCAL_TRANSFORM_PROOFS.json', old_proof)
    fresh(history / 'ORIGINAL_UNFROZEN_SOURCE_PINS_AND_BOUNDARIES.json', old_manifest)
    original, original_pin = read_pin(OUT / 'ORIGINAL_COMPLETE_FLULPN.f')
    assert original == read_pin(Path('/Users/wen/spot/src/FLULPN.f'))[0]
    t = Transform(original)
    t.splice('independent FLULPN DECK without changing Hollerith diagnostic text',
             '*DECK FLULPN\n', '*DECK SPOT_FLULPN_NATIVE64\n')
    t.splice('independent true FLULPN procedure without changing diagnostics',
             '      SUBROUTINE FLULPN(', '      SUBROUTINE SPOT_FLULPN_NATIVE64(')
    t.splice('native Todorova flux and leakage dynamic parameters',
             '      REAL VOL(NREG),FLUX(NUNKNO,NGRP),B2,DIFHET(NMERG,NGRP),DHOM(NGRP)\n',
             '      REAL VOL(NREG)\n'
             '      DOUBLE PRECISION FLUX(NUNKNO,NGRP),B2,\n'
             '     1 DIFHET(NMERG,NGRP),DHOM(NGRP),FLTOT\n')
    t.splice('integrated iteration flux stays native, macrolib ST remains static32',
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: ST,FLXIN\n',
             '      REAL, ALLOCATABLE, DIMENSION(:,:) :: ST\n'
             '      DOUBLE PRECISION, ALLOCATABLE, DIMENSION(:,:) :: FLXIN\n')
    for old,new in [
        ('DIFHET(INM,IGR)=REAL(1.0D0/(3.0D0*GAMMA*ST2))','DIFHET(INM,IGR)=1.0D0/(3.0D0*GAMMA*ST2)'),
        ('DIFHET(INM,IGR)=REAL(1.0D0/(3.0D0*STR))','DIFHET(INM,IGR)=1.0D0/(3.0D0*STR)'),
        ('DIFHET(INM,IGR)=REAL(STOD(IGR,NGRP+1))','DIFHET(INM,IGR)=STOD(IGR,NGRP+1)')]:
        t.splice('same native coefficient expression without dynamic demote',old,new)
    t.splice('new honest independent complete Todorova Source header',
             '*DECK SPOT_FLULPN_NATIVE64\n',
             '*DECK SPOT_FLULPN_NATIVE64\n'
             '*     New full native dynamic API; original equations/order retained.\n'
             '*     Static macrolib records remain type2, never dynamic flux.\n'
             '*     No compiler, transport or physical qualification here.\n')
    proof = json.loads(old_proof)
    proof['proofs']['FLULPN'] = t.verify()
    proof['actual_before_freeze_Source_repair'] = {
        'reason':'Whole identifier rename had changed FORMAT Hollerith diagnostic text without updating original character counts. Only the DECK and true procedure are now renamed; every original diagnostic and FORMAT is preserved.',
        'original_unfrozen_Source_pin':old_pin,
        'original_unfrozen_proof_pin':old_proof_pin,
        'original_unfrozen_manifest_pin':old_manifest_pin,
        'bad_candidate_not_compiled_or_executed':True,
        'repair_writer_pin':read_pin(Path(__file__).resolve())[1],
        'original_complete_basis_pin':original_pin}
    original_formats = original[original.index(b'  100 FORMAT'):]
    assert t.raw[t.raw.index(b'  100 FORMAT'):] == original_formats
    replace(source,t.raw)
    replace(proof_path,(json.dumps(proof,ensure_ascii=False,indent=2)+'\n').encode())
    manifest=json.loads(old_manifest)
    manifest['source_pins']['FLULPN']=read_pin(source)[1]
    manifest['source_writer_pin']=read_pin(OUT/'generate_global_native64_dependency_source.py')[1]
    manifest['proof_pin']=read_pin(proof_path)[1]
    manifest['actual_before_freeze_Source_repair']=proof['actual_before_freeze_Source_repair']
    replace(manifest_path,(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode())
    ast.parse(read_pin(OUT/'generate_global_native64_dependency_source.py')[0])
    assert read_pin(Path('/Users/wen/spot/src/FLULPN.f'))[1]==proof['complete_bases']['FLULPN']
    print(json.dumps({'status':'ACTUAL_SOURCE_ONLY_HOLLERITH_NAMESPACE_REPAIR0',
                      'FLULPN_pin':read_pin(source)[1],
                      'proof_pin':read_pin(proof_path)[1],
                      'manifest_pin':read_pin(manifest_path)[1],
                      'full_original_FORMAT_and_diagnostics_preserved':True,
                      'complete_inverse_equals_original_bytes':True,
                      'compiler_or_numeric_executed':False}))


if __name__=='__main__':
    main()
