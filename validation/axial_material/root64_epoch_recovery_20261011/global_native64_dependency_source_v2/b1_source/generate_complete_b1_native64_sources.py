#!/usr/bin/env python3
"""Create complete new typed B1 Sources; never compile, import, or run Fortran."""
from pathlib import Path
import hashlib
import json
import os
import re
import stat
import time

ROOT = Path('/Users/wen/spot')
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OUT = Path(__file__).resolve().parent
ORIGINALS = {
    'HOM': ROOT / 'src/B1HOM64.f90',
    'HXS_CONTAINER': ROOT / 'src/B1HXS1.f',
    'DIF': ROOT / 'src/B1DIF.f',
}
DEPENDENCIES = [ROOT / p for p in (
    'src/B1SOL.f', 'src/B1BETA.f', 'src/B1GAMA.f',
    'Utilib/src/ALSBD.f', 'Utilib/src/ALEIGD.f', 'Utilib/src/ALINVD.f',
    'Ganlib/src/ganlib.f90', 'Ganlib/src/lcmmod.f90',
)]


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def read_pin(path):
    path = Path(path)
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode), str(path)
    with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)), 'rb') as f:
        opened = os.fstat(f.fileno())
        data = f.read()
        eof = os.fstat(f.fileno())
    after = path.lstat()
    assert identity(before) == identity(opened) == identity(eof) == identity(after), str(path)
    assert len(data) == after.st_size
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
    elif isinstance(data, str):
        data = data.encode()
    if path.exists() or path.is_symlink():
        assert name.startswith('ORIGINAL_COMPLETE_') or name in {
            'SPOT_B1HOM_NATIVE64.f90', 'SPOT_B1HXS2_NATIVE64.f',
            'SPOT_B1DIF_NATIVE64.f'}, str(path)
        observed, pin = read_pin(path)
        assert observed == data, str(path)
        return pin
    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    observed, pin = read_pin(path)
    assert observed == data
    return pin


class Derivation:
    def __init__(self, label, basis):
        self.label = label
        self.basis = basis
        self.data = basis
        self.steps = []

    def splice(self, label, old, new):
        old = old.encode() if isinstance(old, str) else old
        new = new.encode() if isinstance(new, str) else new
        assert old and self.data.count(old) == 1, (self.label, label)
        offset = self.data.index(old)
        before = self.data
        self.data = before[:offset] + new + before[offset + len(old):]
        assert self.data[:offset] == before[:offset]
        assert self.data[offset + len(new):] == before[offset + len(old):]
        self.steps.append({
            'label': label, 'mode': 'one_exact_local_byte_splice',
            'byte_offset_in_step_input': offset,
            'old': old.decode(), 'new': new.decode(),
            'old_bytes': len(old), 'new_bytes': len(new),
            'before_sha256': hashlib.sha256(before).hexdigest(),
            'after_sha256': hashlib.sha256(self.data).hexdigest(),
            'outside_splice_exact_bytes_equal': True,
        })

    def rename(self, label, old, new, count):
        old = old.encode(); new = new.encode()
        pattern = rb'\b' + re.escape(old) + rb'\b'
        assert len(re.findall(pattern, self.data)) == count, (self.label, label)
        assert not re.search(rb'\b' + re.escape(new) + rb'\b', self.data)
        before = self.data
        self.data = re.sub(pattern, new, before)
        self.steps.append({
            'label': label, 'mode': 'exact_identifier_token_rename',
            'old': old.decode(), 'new': new.decode(), 'occurrence_count': count,
            'before_sha256': hashlib.sha256(before).hexdigest(),
            'after_sha256': hashlib.sha256(self.data).hexdigest(),
        })

    def verify(self):
        inverse = self.data
        for step in reversed(self.steps):
            assert hashlib.sha256(inverse).hexdigest() == step['after_sha256']
            old = step['old'].encode(); new = step['new'].encode()
            if step['mode'] == 'one_exact_local_byte_splice':
                assert inverse.count(new) == 1, (self.label, step['label'])
                inverse = inverse.replace(new, old, 1)
            else:
                pattern = rb'\b' + re.escape(new) + rb'\b'
                assert len(re.findall(pattern, inverse)) == step['occurrence_count']
                inverse = re.sub(pattern, old, inverse)
            assert hashlib.sha256(inverse).hexdigest() == step['before_sha256']
        assert inverse == self.basis, self.label
        forward = self.basis
        for step in self.steps:
            assert hashlib.sha256(forward).hexdigest() == step['before_sha256']
            old = step['old'].encode(); new = step['new'].encode()
            if step['mode'] == 'one_exact_local_byte_splice':
                assert forward.count(old) == 1
                assert forward.index(old) == step['byte_offset_in_step_input']
                forward = forward.replace(old, new, 1)
            else:
                pattern = rb'\b' + re.escape(old) + rb'\b'
                assert len(re.findall(pattern, forward)) == step['occurrence_count']
                forward = re.sub(pattern, new, forward)
            assert hashlib.sha256(forward).hexdigest() == step['after_sha256']
        assert forward == self.data
        return {
            'name': self.label, 'steps': self.steps,
            'step_count': len(self.steps),
            'basis_whole_bytes_sha256': hashlib.sha256(self.basis).hexdigest(),
            'candidate_whole_bytes_sha256': hashlib.sha256(self.data).hexdigest(),
            'complete_forward_equals_candidate': True,
            'complete_inverse_equals_original_basis': True,
            'complete_inverse_sha256': hashlib.sha256(inverse).hexdigest(),
        }


def main():
    started = time.monotonic()
    protected_paths = list(ORIGINALS.values()) + DEPENDENCIES + [
        ROOT / 'src/FLU2DR64.f', ROOT / 'src/FLUDRV.f', ROOT / 'src/FLU.f',
        REC / 'global_continuous_source_v1/SPOT_GLOBAL_TYPED_DRIVER64.f',
        REC / 'global_continuous_source_v1/SPOT_GLOBAL_TYPED_DRIVER_API.f90',
        REC / 'global_continuous_source_v1/callee_source/SPOT_FLUKEF_TYPED64.f',
        REC / 'global_continuous_source_v1/callee_source/COMPLETE_CALLEE_SOURCE_FREEZE.json',
    ]
    protected_before = [read_pin(p)[1] for p in protected_paths]
    original = {k: read_pin(p) for k, p in ORIGINALS.items()}
    _, writer_pin = read_pin(Path(__file__).resolve())
    hom_basis, hom_pin = original['HOM']
    container_basis, container_pin = original['HXS_CONTAINER']
    dif_basis, dif_pin = original['DIF']

    # The complete HXS2 procedure is a delimited complete part of the full
    # original multi-procedure Source; preserve the full container as well.
    start_marker = b'      SUBROUTINE B1HXS2('
    end_marker = b'      SUBROUTINE B1HXS3('
    assert container_basis.count(start_marker) == container_basis.count(end_marker) == 1
    start = container_basis.index(start_marker)
    end = container_basis.index(end_marker)
    hxs_basis = container_basis[start:end]
    assert len(re.findall(rb'(?m)^      SUBROUTINE ', hxs_basis)) == 1
    assert hxs_basis.rstrip().endswith(b'END\n*')
    hom_copy = write_new('ORIGINAL_COMPLETE_B1HOM64.f90', hom_basis)
    container_copy = write_new('ORIGINAL_COMPLETE_B1HXS1_CONTAINER.f', container_basis)
    hxs_copy = write_new('ORIGINAL_COMPLETE_B1HXS2_PROCEDURE.f', hxs_basis)
    dif_copy = write_new('ORIGINAL_COMPLETE_B1DIF.f', dif_basis)

    hom = Derivation('SPOT_B1HOM_NATIVE64', hom_basis)
    hom.splice('honest full native64 dynamic dependency boundary header',
        '!   REAL64 flux/source update for the homogeneous B1 calculation used by\n'
        '!   the SPOT axial solver.  Nuclear-data homogenization and B1DIF remain\n'
        '!   the established REAL32 routines; only the live flux/source pair and\n'
        '!   its group normalization stay in REAL64.\n',
        '!   NEW SOURCE: complete native64 dynamic B1 dependency chain.\n'
        '!   Full original HOM64 formulas, loops, guards and order retained.\n'
        '!   FLUX, homogenized coefficients, PHI, B2 and live leakage stay DP.\n'
        '!   Static material/geometry inputs keep the original REAL ABI.\n'
        '!   No compiler, numeric, transport or physical qualification here.\n')
    hom.rename('new complete HOM symbol namespace', 'B1HOM64', 'SPOT_B1HOM_NATIVE64', 5)
    hom.rename('complete typed HXS2 dependency symbol', 'B1HXS2', 'SPOT_B1HXS2_NATIVE64', 2)
    hom.rename('complete typed DIF dependency symbol', 'B1DIF', 'SPOT_B1DIF_NATIVE64', 2)
    hom.splice('static volume stays REAL, dynamic leakage becomes DP',
        '  real, intent(in) :: vol(ipas),leak1d(ngro)\n',
        '  real, intent(in) :: vol(ipas)\n'
        '  double precision, intent(in) :: leak1d(ngro)\n')
    hom.splice('live diffusion and gamma output ABI stays DP',
        '  real, intent(inout) :: dhom(ngro),gamma(ngro)\n',
        '  double precision, intent(inout) :: dhom(ngro),gamma(ngro)\n')
    hom.splice('live full B2 ABI stays DP',
        '  real, intent(inout) :: b2(4)\n',
        '  double precision, intent(inout) :: b2(4)\n')
    hom.splice('flux-weighted coefficients allocated in DP with no flux32 buffer',
        '  real, allocatable :: flux32(:,:),st(:),sa(:),sfnu(:),xhi(:)\n'
        '  real, allocatable :: scat0(:),scat1(:)\n',
        '  double precision, allocatable :: st(:),sa(:),sfnu(:),xhi(:)\n'
        '  double precision, allocatable :: scat0(:),scat1(:)\n')
    hom.splice('retain scattering allocation and remove flux demotion',
        '  allocate(scat0(idel(1)),scat1(idel(2)),flux32(nunkno,ngro))\n'
        '  flux32=real(flux(:,:,1))\n',
        '  allocate(scat0(idel(1)),scat1(idel(2)))\n')
    hom.splice('whole real64 live input passed to typed HXS2',
        '              flux32,lfissi,ijj0,ijj1,njj0,njj1,idel,phi,sa,st,sfnu, &\n',
        '              flux(:,:,1),lfissi,ijj0,ijj1,njj0,njj1,idel,phi,sa,st,sfnu, &\n')
    hom.splice('retain actual DP old buckling without mirror promotion',
        '  b2old=real(b2(4),dp)\n', '  b2old=b2(4)\n')
    hom.splice('retain actual DP returned buckling without demotion',
        '  b2(4)=real(b2hom)\n', '  b2(4)=b2hom\n')
    hom.splice('same source correction order with direct native64 live coefficients',
        '      flux(:,i,2)=flux(:,i,2)+(real(b2(4),dp)-b2old)* &\n'
        '                    real(dhom(i),dp)*flux(:,i,1)\n',
        '      flux(:,i,2)=flux(:,i,2)+(b2(4)-b2old)* &\n'
        '                    dhom(i)*flux(:,i,1)\n')
    hom.splice('remove only obsolete flux32 cleanup',
        '  deallocate(flux32,scat1,scat0,phi,xhi,sfnu,sa,st)\n',
        '  deallocate(scat1,scat0,phi,xhi,sfnu,sa,st)\n')
    assert b'flux32' not in hom.data
    assert b'real(vol(l),dp)' in hom.data

    hxs = Derivation('SPOT_B1HXS2_NATIVE64', hxs_basis)
    hxs.rename('new complete HXS2 symbol namespace', 'B1HXS2', 'SPOT_B1HXS2_NATIVE64', 2)
    hxs.splice('native64 API header before complete original procedure',
        '      SUBROUTINE SPOT_B1HXS2_NATIVE64(',
        '*DECK SPOT_B1HXS2_NATIVE64\n'
        '*     NEW SOURCE: full original B1HXS2 procedure, typed dynamic ABI.\n'
        '*     Static VOL/GAR/GARFI/XSCAT material buffers remain REAL.\n'
        '*     Full live FLUX and every weighted result stay DP.\n'
        '*     Original equations, loop order and spectrum guard retained.\n'
        '*     No compilation, numerical execution or qualification here.\n'
        '      SUBROUTINE SPOT_B1HXS2_NATIVE64(')
    hxs.splice('static geometry ABI stays REAL; all weighted outputs and flux become DP',
        '      REAL VOL(IPAS),FLUX(NUNKNO,NGRO),SA(NGRO),ST(NGRO),SFNU(NGRO),\n'
        '     1 XHI(NGRO),SCAT0(IDEL(1)),SCAT1(IDEL(2))\n',
        '      REAL VOL(IPAS)\n'
        '      DOUBLE PRECISION FLUX(NUNKNO,NGRO),SA(NGRO),ST(NGRO),\n'
        '     1 SFNU(NGRO),XHI(NGRO),SCAT0(IDEL(1)),SCAT1(IDEL(2))\n')
    weighted_casts = [
        ('nu-fission weighted result', '         SFNU(LLL)=REAL(A11/FLXIN(LLL))', '         SFNU(LLL)=A11/FLXIN(LLL)'),
        ('total weighted result', '        ST(LLL)=REAL(A11/FLXIN(LLL))', '        ST(LLL)=A11/FLXIN(LLL)'),
        ('absorption weighted result', '      SA(LLL)=REAL(A11/FLXIN(LLL))', '      SA(LLL)=A11/FLXIN(LLL)'),
        ('spectrum weighted result', '         XHI(LLL)=REAL(A11/A13)', '         XHI(LLL)=A11/A13'),
        ('transport correction weighted result', '           ST(LLL)=ST(LLL)-REAL(A11/FLXIN(LLL))', '           ST(LLL)=ST(LLL)-A11/FLXIN(LLL)'),
        ('P0 scattering weighted result', '           SCAT0(IGAR)=REAL(GAF(IG)/FLXIN(IG))', '           SCAT0(IGAR)=GAF(IG)/FLXIN(IG)'),
        ('P1 scattering weighted result', '           SCAT1(IGAR)=REAL(GAF(IG)/FLXIN(IG))', '           SCAT1(IGAR)=GAF(IG)/FLXIN(IG)'),
    ]
    for label, old, new in weighted_casts:
        hxs.splice('remove only explicit REAL demotion: ' + label, old, new)
    assert not re.search(rb'\bREAL\s*\(', hxs.data)
    assert b'1.0D-3' in hxs.data
    assert b'      REAL, ALLOCATABLE, DIMENSION(:) :: XSCAT,GAR,GARFI\n' in hxs.data

    dif = Derivation('SPOT_B1DIF_NATIVE64', dif_basis)
    # Rename the true procedure and deck identifiers only. Original FORMAT
    # diagnostics contain counted Hollerith strings and must stay exact.
    dif.splice('new DIF deck identifier without touching counted FORMAT text',
        '*DECK B1DIF\n', '*DECK SPOT_B1DIF_NATIVE64\n')
    dif.splice('new actual complete DIF procedure symbol',
        '      SUBROUTINE B1DIF(', '      SUBROUTINE SPOT_B1DIF_NATIVE64(')
    dif.splice('honest native64 API header before original full DIF body',
        '*DECK SPOT_B1DIF_NATIVE64\n',
        '*DECK SPOT_B1DIF_NATIVE64\n'
        '*     NEW SOURCE: complete original B1DIF with typed live inputs.\n'
        '*     Weighted XS/scattering, leakage, DHOM/GAMMA remain DP.\n'
        '*     Original EPS=1.0D-6, MAXIT=50 and loop order retained.\n'
        '*     DP B1BETA/B1GAMA/B1SOL/ALEIGD dependencies stay unchanged.\n'
        '*     No compilation, numerical execution or qualification here.\n')
    dif.splice('every live weighted/leakage coefficient ABI becomes DP',
        '      REAL ST(NGRO),SFNU(NGRO),XHI(NGRO),LEAK1D(NGRO),SCAT0(*),SCAT1(*),\n'
        '     > DHOM(NGRO),GAMMA(NGRO)\n',
        '      DOUBLE PRECISION ST(NGRO),SFNU(NGRO),XHI(NGRO),LEAK1D(NGRO),\n'
        '     > SCAT0(*),SCAT1(*),DHOM(NGRO),GAMMA(NGRO)\n')
    # Individual contextual splices keep all original branches and loop order.
    cast_map = [
        ('DIFF gamma', '         GAMMA(I)=REAL(B1GAMA(IAPROX,B2,ST2))\n'
            '         IF(IAPROX.NE.0) DHOM(I)=REAL(1.0D0/(3.0D0*GAMMA(I)*ST2))\n'
            '   15    CONTINUE\n',
            '         GAMMA(I)=B1GAMA(IAPROX,B2,ST2)\n'
            '         IF(IAPROX.NE.0) DHOM(I)=1.0D0/(3.0D0*GAMMA(I)*ST2)\n'
            '   15    CONTINUE\n'),
        ('TYPE L P1 diffusion', '         DHOM(I)=REAL(ASTOC(I,NGRO+1))\n'
            '  210    CONTINUE\n', '         DHOM(I)=ASTOC(I,NGRO+1)\n'
            '  210    CONTINUE\n'),
        ('TYPE L gamma and diffusion', '         GAMMA(I)=REAL(B1GAMA(IAPROX,B2,ST2))\n'
            '         IF(IAPROX.NE.0) DHOM(I)=REAL(1.0D0/(3.0D0*GAMMA(I)*ST2))\n'
            '  220    CONTINUE\n',
            '         GAMMA(I)=B1GAMA(IAPROX,B2,ST2)\n'
            '         IF(IAPROX.NE.0) DHOM(I)=1.0D0/(3.0D0*GAMMA(I)*ST2)\n'
            '  220    CONTINUE\n'),
        ('final P1 diffusion', '         DHOM(I)=REAL(ASTOC(I,NGRO+1))\n'
            '  330    CONTINUE\n', '         DHOM(I)=ASTOC(I,NGRO+1)\n'
            '  330    CONTINUE\n'),
        ('final gamma and diffusion', '         GAMMA(I)=REAL(B1GAMA(IAPROX,B2,ST2))\n'
            '         IF(IAPROX.NE.0) DHOM(I)=REAL(1.0D0/(3.0D0*GAMMA(I)*ST2))\n'
            '  340    CONTINUE\n',
            '         GAMMA(I)=B1GAMA(IAPROX,B2,ST2)\n'
            '         IF(IAPROX.NE.0) DHOM(I)=1.0D0/(3.0D0*GAMMA(I)*ST2)\n'
            '  340    CONTINUE\n'),
        ('final migration gamma', '      ST2=DBLE(ST(I))\n'
            '      GAMMA(I)=REAL(B1GAMA(IAPROX,B2,ST2))\n'
            '  350 CONTINUE\n',
            '      ST2=DBLE(ST(I))\n'
            '      GAMMA(I)=B1GAMA(IAPROX,B2,ST2)\n'
            '  350 CONTINUE\n'),
    ]
    for label, old, new in cast_map:
        dif.splice('remove only explicit live REAL demotion: ' + label, old, new)
    assert not re.search(rb'\bREAL\s*\(', dif.data)
    assert b'      PARAMETER (EPS=1.0D-6,MAXIT=50)\n' in dif.data
    for p in (b'CALL B1SOL(', b'CALL ALEIGD(', b'B1BETA(', b'B1GAMA('):
        assert dif.data.count(p) == dif_basis.count(p)

    candidates = [
        ('SPOT_B1HOM_NATIVE64.f90', hom, hom_pin, hom_copy),
        ('SPOT_B1HXS2_NATIVE64.f', hxs, container_pin, hxs_copy),
        ('SPOT_B1DIF_NATIVE64.f', dif, dif_pin, dif_copy),
    ]
    proofs = []
    candidate_pins = []
    for name, derivation, origin_pin, basis_copy in candidates:
        proof = derivation.verify()
        candidate_pin = write_new(name, derivation.data)
        proof.update(original_complete_Source_pin=origin_pin,
                     original_complete_basis_copy=basis_copy, candidate_Source=candidate_pin,
                     original_formulas_and_summation_loop_order_retained=True,
                     original_guards_thresholds_and_caps_retained=True,
                     changes_are_only_identifier_header_dynamic_types_and_removal_of_REAL_demotion=True,
                     compiler_parser_native_numeric_executed=False)
        proofs.append(proof)
        candidate_pins.append(candidate_pin)

    proof_pin = write_new('COMPLETE_B1_NATIVE64_FORWARD_INVERSE_BYTES_PROOF.json', {
        'schema': 'COMPLETE_B1_NATIVE64_NEW_SOURCE_EXACT_BYTES_DERIVATION_V1',
        'derivations': proofs,
        'original_full_HXS_container': container_pin,
        'original_full_HXS_container_copy': container_copy,
        'HXS2_complete_procedure_extraction': {
            'start_byte_offset': start, 'end_byte_offset_exclusive': end,
            'start_marker': start_marker.decode(), 'next_procedure_marker': end_marker.decode(),
            'complete_byte_slice_equals_saved_basis': hxs_basis == read_pin(OUT / 'ORIGINAL_COMPLETE_B1HXS2_PROCEDURE.f')[0],
            'basis_size_bytes': len(hxs_basis),
            'basis_sha256': hashlib.sha256(hxs_basis).hexdigest(),
            'full_original_container_preserved_in_separate_complete_copy': True,
        },
        'HXS2_removed_REAL_demotions': 7, 'DIF_removed_REAL_demotions': 9,
        'source_only': True, 'compiler_parser_native_numeric_executed': False,
    })
    protected_after = [read_pin(p)[1] for p in protected_paths]
    assert protected_before == protected_after
    dependency_pins = [read_pin(p)[1] for p in DEPENDENCIES]
    manifest_pin = write_new('CURRENT_COMPLETE_B1_NATIVE64_SOURCE_PINS_AND_SCOPE.json', {
        'schema': 'CURRENT_COMPLETE_B1_NATIVE64_NEW_SOURCE_PINS_AND_SCOPE_V1',
        'status': 'NEW_COMPLETE_SOURCE_ONLY_NOT_COMPILED_OR_RUN',
        'candidate_Source_fullpins': candidate_pins,
        'original_Source_fullpins': [hom_pin, container_pin, dif_pin],
        'complete_original_copy_fullpins': [hom_copy, container_copy, hxs_copy, dif_copy],
        'wholebyte_derivation_proof': proof_pin, 'actual_writer_Source': writer_pin,
        'unchanged_DP_support_Source_graph_fullpins': dependency_pins,
        'call_graph': {
            'SPOT_B1HOM_NATIVE64': ['B1HXS1', 'SPOT_B1HXS2_NATIVE64', 'SPOT_B1DIF_NATIVE64'],
            'SPOT_B1HXS2_NATIVE64': ['GANLIB LCMGET/LCMLEN/LCMGID/LCMGIL', 'XABORT'],
            'SPOT_B1DIF_NATIVE64': ['B1BETA', 'B1GAMA', 'B1SOL', 'ALEIGD', 'XABORT'],
            'B1SOL': ['ALSBD'], 'ALEIGD': ['ALINVD', 'XABORT'],
        },
        'original_call_argument_order_retained': True,
        'dynamic_native64_values': ['FLUX', 'FLXIN/PHI', 'flux-weighted SA/ST/SFNU/XHI/SCAT0/SCAT1', 'B2(4)', 'DHOM', 'GAMMA', 'LEAK1D', 'ALAM1/CAET/A2'],
        'static_REAL32_authorities_retained': ['VOL', 'GAR/GARFI/XSCAT read from original material records'],
        'static_values_promote_exactly_when_multiplied_by_live_DOUBLE_PRECISION_flux': True,
        'original_formulas_summation_order_branch_guards_EPS_and_caps_retained': True,
        'B1DIF_original_EPS': '1.0D-6', 'B1DIF_original_MAXIT': 50,
        'ALEIGD_original_MMAX': 1000,
        'original_HOM64_INORM1_and_no_leakage_guards_retained': True,
        'protected_Source_before': protected_before, 'protected_Source_after': protected_after,
        'protected_Source_fullpins_unchanged': True,
        'writes_restricted_to_b1_source_subdirectory': True,
        'compiler_parser_native_numeric_executed': False,
        'runtime_general_shape_or_B1_qualified': False,
        'global_driver_native64_qualified': False,
        'native_global_producer_qualified': False,
        'original_seventeen_controls_qualified': False,
        'online_BOOT_qualified': False, 'whole_INPUT_admitted': False,
        'AAA_qualified': False, 'ABA_admitted': False, 'goal_complete': False,
        'remaining_scope': ['current independent v2 global typed caller ABI and TYPE4 B2/DIFHET authority wiring', 'bounded true compile/link/control/native transport', 'external complete current input and output binding', 'scientific and whole-chain qualification'],
        'own_elapsed_seconds': time.monotonic() - started,
        'own_manifest_pin_exception': 'Actual closed writer return separately contains this manifest full-EOF pin.',
    })
    print(json.dumps({
        'schema': 'COMPLETE_B1_NATIVE64_ACTUAL_SOURCE_ONLY_WRITER_RESULT_V1',
        'status': 'THREE_COMPLETE_NEW_SOURCE_BYTES_WRITTEN_AND_WHOLE_INVERSES_VERIFIED',
        'candidate_Source_fullpins': candidate_pins,
        'proof': proof_pin, 'manifest': manifest_pin,
        'derivation_step_counts': {p['name']: p['step_count'] for p in proofs},
        'protected_Source_fullpins_unchanged': True,
        'compiler_parser_native_numeric_executed': False,
        'goal_complete': False,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
