#!/usr/bin/env python3
"""Create one new Source-only typed keff entry, without compiling or running it."""
from pathlib import Path
import hashlib
import json
import os
import stat
import time

OUT = Path(__file__).resolve().parent
ROOT = Path('/Users/wen/spot')
BASIS = ROOT / 'validation/artifacts/axial-material-r64-snapshot-A-20261003/build/AXMAT_FLUKEF64.f'
LEGACY = ROOT / 'src/FLUKEF.f'
PROTECTED_DRIVER = ROOT / 'src/FLU2DR64.f'
EXPECTED_BASIS_SHA = '4fada005a3f6a601ba59ccde076bcbd45e3829458cf7637aa86c4891574d9553'
HEADER = (
    '*DECK SPOT_FLUKEF_TYPED64\n'
    '*     NEW SOURCE: dimensioned REAL64-flux keff caller API.\n'
    '*     Complete AXMAT_FLUKEF64 numerical body retained byte-for-byte.\n'
    '*     FLUX(NUNKNO,NGRP) is DOUBLE PRECISION; coefficients remain REAL.\n'
    '*     All original arguments, formulas, and leakage branches remain.\n'
    '*     This helper imposes no fixed door or 8/14/370 shape policy.\n'
    '*     Caller must bind its full typed field and valid maps/context.\n'
    '*     Caller and build must retain the original compatible kinds.\n'
    '*     No compiler, numeric execution, producer or physics PASS here.\n'
)


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def complete_pin(path):
    path = Path(path)
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as f:
        opened = os.fstat(f.fileno())
        data = f.read()
        eof = os.fstat(f.fileno())
    after = path.lstat()
    assert identity(before) == identity(opened) == identity(eof) == identity(after), str(path)
    assert len(data) == after.st_size, str(path)
    return data, {
        'path': str(path), 'size_bytes': len(data),
        'sha256': hashlib.sha256(data).hexdigest(), 'identity': identity(after),
        'before_open_EOF_after_identity_equal': True, 'read_scope': 'complete EOF',
    }


def write_new(name, data):
    path = OUT / name
    assert path.parent == OUT
    if isinstance(data, dict):
        data = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()
    if isinstance(data, str):
        data = data.encode()
    with path.open('xb') as f:
        f.write(data)
    actual, pin = complete_pin(path)
    assert actual == data
    return pin


def exact_replace(data, old, new):
    assert old and data.count(old) == 1, repr(old)
    return data.replace(old, new, 1)


def main():
    started = time.monotonic()
    basis, basis_pin = complete_pin(BASIS)
    legacy, legacy_pin = complete_pin(LEGACY)
    _, driver_pin = complete_pin(PROTECTED_DRIVER)
    _, writer_pin = complete_pin(Path(__file__).resolve())
    assert len(basis) == 6068 and basis_pin['sha256'] == EXPECTED_BASIS_SHA

    # Exact two known legacy changes, rather than a formula-level approximation.
    legacy_transforms = [
        (b'SUBROUTINE FLUKEF(', b'SUBROUTINE AXMAT_FLUKEF64('),
        (b'     2 DIFHET(NMERG,NGRP),FLUX(NUNKNO,NGRP),B2(4)\n',
         b'     2 DIFHET(NMERG,NGRP),B2(4)\n'
         b'      DOUBLE PRECISION FLUX(NUNKNO,NGRP)\n'),
    ]
    legacy_forward = legacy
    for old, new in legacy_transforms:
        legacy_forward = exact_replace(legacy_forward, old, new)
    assert legacy_forward == basis
    legacy_inverse = basis
    for old, new in reversed(legacy_transforms):
        legacy_inverse = exact_replace(legacy_inverse, new, old)
    assert legacy_inverse == legacy

    transforms = [
        (b'*DECK FLUKEF\n', HEADER.encode()),
        (b'SUBROUTINE AXMAT_FLUKEF64(', b'SUBROUTINE SPOT_FLUKEF_TYPED64('),
    ]
    candidate = basis
    for old, new in transforms:
        candidate = exact_replace(candidate, old, new)
    inverse = candidate
    for old, new in reversed(transforms):
        inverse = exact_replace(inverse, new, old)
    assert inverse == basis
    numeric_marker = b'      FISOUR=DZERO\n'
    assert basis.count(numeric_marker) == candidate.count(numeric_marker) == legacy.count(numeric_marker) == 1
    numeric_body = basis[basis.index(numeric_marker):]
    assert candidate[candidate.index(numeric_marker):] == numeric_body
    assert legacy[legacy.index(numeric_marker):] == numeric_body
    assert b'DOUBLE PRECISION FLUX(NUNKNO,NGRP)' in candidate
    assert b'CALL XABORT' not in candidate
    assert b'MCCG' not in basis and b'NREG.NE.8' not in basis and b'NUNKNO.NE.14' not in basis

    original_copy_pin = write_new('ORIGINAL_COMPLETE_AXMAT_FLUKEF64.f', basis)
    legacy_copy_pin = write_new('ORIGINAL_COMPLETE_LEGACY_FLUKEF.f', legacy)
    candidate_pin = write_new('SPOT_FLUKEF_TYPED64.f', candidate)
    proof = {
        'schema': 'SPOT_FLUKEF_TYPED64_EXACT_BYTES_DERIVATION_V1',
        'basis': basis_pin, 'original_complete_copy': original_copy_pin,
        'legacy_reference': legacy_pin, 'legacy_complete_copy': legacy_copy_pin,
        'candidate': candidate_pin,
        'new_Source_transforms': [{'old': a.decode(), 'new': b.decode(), 'occurrences': 1} for a, b in transforms],
        'legacy_to_REAL64_basis_transforms': [{'old': a.decode(), 'new': b.decode(), 'occurrences': 1} for a, b in legacy_transforms],
        'forward_complete_bytes_equal_saved_candidate': candidate == complete_pin(OUT / 'SPOT_FLUKEF_TYPED64.f')[0],
        'inverse_complete_bytes_equal_original_basis': inverse == basis,
        'legacy_forward_complete_bytes_equal_REAL64_basis': legacy_forward == basis,
        'legacy_inverse_complete_bytes_equal_original_legacy': legacy_inverse == legacy,
        'all_numeric_body_bytes_equal_legacy_basis_candidate': True,
        'numeric_body_from_FISOUR_through_END_size_bytes': len(numeric_body),
        'numeric_body_from_FISOUR_through_END_sha256': hashlib.sha256(numeric_body).hexdigest(),
        'all_original_arguments_and_formulas_retained': True,
        'fixed_MCCG_8_14_370_shape_restriction_added': False,
        'Fortran_parser_compiler_or_numeric_execution': False,
    }
    proof_pin = write_new('SPOT_FLUKEF_TYPED64_EXACT_FORWARD_INVERSE_PROOF.json', proof)
    _, basis_after = complete_pin(BASIS)
    _, legacy_after = complete_pin(LEGACY)
    _, driver_after = complete_pin(PROTECTED_DRIVER)
    assert basis_after == basis_pin and legacy_after == legacy_pin and driver_after == driver_pin
    manifest = {
        'schema': 'SPOT_FLUKEF_TYPED64_CURRENT_SOURCE_PINS_AND_SCOPE_V1',
        'classification': 'NEW_SOURCE_ONLY_NOT_COMPILED_OR_RUN',
        'candidate_Source': candidate_pin, 'original_basis': basis_pin,
        'legacy_reference': legacy_pin, 'writer_Source': writer_pin,
        'fixed_created_files_before_this_manifest': [original_copy_pin, legacy_copy_pin, candidate_pin, proof_pin],
        'protected_Source_before': [basis_pin, legacy_pin, driver_pin],
        'protected_Source_after': [basis_after, legacy_after, driver_after],
        'protected_Source_fullpins_unchanged': True,
        'namespace': str(OUT),
        'writes_restricted_to_callee_source_subdirectory': True,
        'manifest_ownfile_exception': 'This manifest cannot hash itself; the actual writer return contains its observed full-EOF pin.',
        'actual_tool_metadata_exception': 'The caller saves the true completed writer tool return afterward without fabricating process status.',
        'scope': 'dimensioned REAL64-flux keff helper; original REAL coefficient ABI and complete numerical body retained',
        'global_driver_required_call_sites': ['first K from true REAL64 FLUX(:,:,2)', 'TYPE2 update from true REAL64 FLUX(:,:,3)'],
        'global_driver_firstK_or_TYPE2_FLX32_demotion_permitted': False,
        'original_SPOT_TYPE2_TYPE3_door_or_other_leakage_routes_changed': False,
        'compiler_or_native_or_numeric_executed': False,
        'general_shape_runtime_qualified': False,
        'producer_qualified': False, 'online_BOOT_qualified': False,
        'original_seventeen_controls_qualified': False,
        'physics_accuracy_qualified': False, 'goal_complete': False,
        'own_elapsed_seconds': time.monotonic() - started,
    }
    manifest_pin = write_new('SPOT_FLUKEF_TYPED64_SOURCE_PINS_AND_SCOPE.json', manifest)
    print(json.dumps({
        'schema': 'SPOT_FLUKEF_TYPED64_ACTUAL_SOURCE_ONLY_WRITER_RESULT_V1',
        'status': 'NEW_SOURCE_BYTES_WRITTEN_AND_EXACT_INVERSE_VERIFIED',
        'candidate_Source': candidate_pin, 'proof': proof_pin, 'manifest': manifest_pin,
        'new_transforms': len(transforms), 'legacy_comparison_transforms': len(legacy_transforms),
        'Source_only': True, 'compiler_native_numeric_executed': False,
        'protected_Source_fullpins_unchanged': True,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
