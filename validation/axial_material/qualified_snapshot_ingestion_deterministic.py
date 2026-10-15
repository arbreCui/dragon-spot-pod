"""Explicitly admit audited offline snapshots to the unchanged legacy BOOT ingress.

The producer executable and online executable have separate identities.  Reading
an offline REAL64 record is not evidence that the online BOOT consumes it: the
receiver promotes the exact REAL32 mirror once, and CONT requires its own R64
authority.  Native receiver predicates and all coupled gates remain mandatory.
"""
import hashlib
import json
from pathlib import Path
import struct

import numpy as np

from analyze_r64_snapshot_deterministic import analyze
from analyze_r64_tracking_moments import analyze as analyze_moments
from check_r64_audit_rejections import check as snapshot_negatives
from check_r64_normalization_rejections import check as normalization_negatives
from snapshot_control_preflight import _open_xsm

PRODUCER_SHA = 'd13f921ea3b9209efe28d153933ab1732c2683b100269d4eda53ed7230e86e04'
ONLINE_SHA = '873ad14272a2f0765d95e6de067194a01708ccf9aa88d58cd782049e6d331fef'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def descriptor(path):
    return dict(path=str(Path(path).resolve()), sha256=digest(path))


def pinned(item):
    p = Path(item['path'])
    if not p.is_absolute() or digest(p) != item['sha256']:
        raise ValueError('snapshot evidence identity differs: ' + str(p))
    return p


def list_handles(archive, directory, name, count):
    raw = archive.record(directory, name, count, 10)
    return [archive.directory(offset)['***HANDLE***'] for offset in struct.unpack(f'<{count}i', raw)]


def audit_payload(path):
    """Read all 370 groups in the actual little-endian XSM, without mutation."""
    with _open_xsm(path) as a:
        if struct.unpack('<i', a.record(a.root, 'LISTDIM', 1, 1))[0] != 1:
            raise ValueError('one archived snapshot required')
        flux, system = a.object('FLUX'), a.object('SYSTEM')
        matrices = {}
        for name, length, kind, dtype in (('FLUX',14,2,'<f4'), ('FLUX64',28,4,'<f8'), ('SOUR64',28,4,'<f8')):
            entries = list_handles(a, flux, name, 370)
            if any(e[1:] != (length,kind) for e in entries):
                raise ValueError('bad saved payload type/length: ' + name)
            matrices[name] = np.array([np.frombuffer(a.read(e[0],length),dtype) for e in entries])
            if not np.isfinite(matrices[name]).all():
                raise ValueError('nonfinite saved payload: ' + name)
        if not np.array_equal(matrices['FLUX64'].astype('<f4').view('<u4'), matrices['FLUX'].view('<u4')):
            raise ValueError('legacy BOOT initial flux is not an exact mirror')
        if not np.all(matrices['FLUX64'][:,:8] > 0):
            raise ValueError('nonpositive saved scalar flux')
        k64 = struct.unpack('<d', a.record(flux,'SPOT-KEFF64',2,4))[0]
        k32 = a.record(flux,'K-EFFECTIVE',1,2)
        if not np.isfinite(k64) or k64 <= 0 or struct.pack('<f',k64) != k32:
            raise ValueError('keff mirror differs')
        volume = None
        for e in list_handles(a, system, 'GROUP',370):
            if e[1:] != (-1,0):
                raise ValueError('SYSTEM group is not a directory')
            g = a.directory(e[0])
            v = a.record(g,'AXMAT-V64',28,4)
            if volume is None:
                volume = v
            if v != volume or not np.all(np.frombuffer(v,'<f8') > 0):
                raise ValueError('volume64 owners differ or are invalid')
            p64 = np.frombuffer(a.record(g,'PJJ64$MCCG',16,4),'<f8')
            p32 = a.record(g,'PJJ$MCCG',8,2)
            if not np.isfinite(p64).all() or np.any(p64 < 0) or p64.astype('<f4').tobytes() != p32:
                raise ValueError('PJJ mirror differs')
    return dict(classification='PASS_OFFLINE_PAYLOAD_AND_LEGACY_BOOT_MIRROR', groups=370,
        k_effective64=k64, archive_sha256=digest(path),
        payload_sha256={k:hashlib.sha256(v.tobytes()).hexdigest() for k,v in matrices.items()},
        volume64_sha256=hashlib.sha256(volume).hexdigest(),
        receiving_record='FLUX/FLUX, REAL32 promoted once by SPOR64_B2B BOOT',
        offline_r64_directly_consumed_by_boot=False, coupled_terminal_qualified=False)


def verify_offline_state(state):
    execution = pinned(state['execution'])
    manifest = json.loads(execution.read_text())
    for name,wanted in manifest['files'].items():
        if digest(name) != wanted:
            raise ValueError('producer input changed: ' + name)
    run_path = pinned(state['snapshot_run_status'])
    run = json.loads(run_path.read_text())
    if run['classification'] != 'R64_SNAPSHOT_COMPLETE_PENDING_INDEPENDENT_AUDIT' or not run['frozen_inputs_unchanged']:
        raise ValueError('completed immutable offline run required')
    directory = pinned(state['archive']).parent
    for name,wanted in run['outputs'].items():
        if digest(directory / name) != wanted:
            raise ValueError('offline output changed')
    audit_path = pinned(state['audit_status'])
    audit_dir = audit_path.parent
    audit = json.loads(audit_path.read_text())
    if audit['classification'] != 'R64_SNAPSHOT_TERMINAL_AUDIT_PASS' or not audit['snapshot_qualified'] or not audit['frozen_inputs_unchanged']:
        raise ValueError('saved-state terminal audit must pass')
    if digest(audit_dir / 'protocol.json') != audit['protocol_sha256']:
        raise ValueError('audit protocol changed')
    for name,wanted in json.loads((audit_dir / 'protocol.json').read_text())['files'].items():
        if digest(name) != wanted:
            raise ValueError('audit input changed')
    for name,wanted in audit['outputs'].items():
        if digest(audit_dir / name) != wanted:
            raise ValueError('audit output changed')
    observations = analyze(audit_dir / 'audit.bin')
    if observations != json.loads((audit_dir / 'observations.json').read_text()) or observations['classification'] != 'R64_SNAPSHOT_TERMINAL_AUDIT_PASS':
        raise ValueError('independent numerical replay differs')
    moments = pinned(state['moments'])
    track = pinned(state['track'])
    normalization = analyze_moments(track, moments, audit_dir / 'volume64.bin')
    if normalization != json.loads((audit_dir / 'volume_normalization_check.json').read_text()):
        raise ValueError('independent track normalization replay differs')
    if snapshot_negatives(audit_dir / 'audit.bin') != json.loads((audit_dir / 'negative_controls.json').read_text()):
        raise ValueError('saved-image rejection controls differ')
    if normalization_negatives(track,moments,audit_dir / 'volume64.bin') != json.loads((audit_dir / 'normalization_negative_controls.json').read_text()):
        raise ValueError('normalization rejection controls differ')
    return audit_payload(pinned(state['archive']))


def admit_snapshots(receipts, resolved, spec):
    if receipts.get('schema') != 'AXMAT_QUALIFIED_OFFLINE_PRODUCER_TO_LEGACY_BOOT_V1':
        raise ValueError('versioned producer/receiver receipt required')
    if receipts['producer_runtime']['sha256'] != PRODUCER_SHA or digest(pinned(receipts['producer_runtime'])) != PRODUCER_SHA:
        raise ValueError('unqualified offline producer executable')
    if receipts['online_receiver_sha256'] != ONLINE_SHA or receipts['offline_r64_directly_consumed_by_boot'] is not False:
        raise ValueError('receiver identity or legacy ingress semantics differ')
    if receipts['inputs_manifest_sha256'] != resolved['material_manifest']['sha256']:
        raise ValueError('material and snapshot manifest differs')
    source = pinned(receipts['receiver_source'])
    text = source.read_text()
    if "initial_flux64(:,ig) = real(flux_stage32,real64)" not in text or "seed_authority = LCMGID(ipseed,'SPOT-R64')" not in text:
        raise ValueError('receiver ingress/continuation source contract differs')
    reports = {}
    for letter in ('A','B'):
        state = receipts['states'][letter]
        for field,key in (('archive',f'snapshot_{letter}'),('track',f'radial_track_{letter}'),('log',f'snapshot_log_{letter}')):
            if state[field] != resolved[key]:
                raise ValueError('producer receipt does not bind ' + key)
        if state['material']['sha256'] != spec['qualified_snapshot_producers']['material_sha256'][letter]:
            raise ValueError('material provenance differs')
        pinned(state['material'])
        reports[letter] = verify_offline_state(state)
        if reports[letter] != state['payload_audit']:
            raise ValueError('saved payload receipt differs from actual archive')
    if reports['A']['volume64_sha256'] != reports['B']['volume64_sha256']:
        raise ValueError('A/B tracking normalization differs')
    return dict(classification='PASS_EXPLICIT_OFFLINE_PRODUCER_LEGACY_BOOT_ADMISSION',
        states=reports, producer_sha256=PRODUCER_SHA, online_receiver_sha256=ONLINE_SHA,
        offline_r64_directly_consumed_by_boot=False, coupled_qualified=False,
        scope='Eligible initial snapshots only; native online input, terminal, lineage, fixed-point and independent CE gates remain required.')
