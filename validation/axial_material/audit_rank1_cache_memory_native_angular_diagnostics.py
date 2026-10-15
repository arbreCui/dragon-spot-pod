"""Source-only scientific worker for a future admitted native angular capture.

No transport, linear solve, experiment creation, or project import occurs on
import.  This is not a declaration/launch/qualification factory.  A future
driver must supply the tested own-child supervisor and the complete fresh
input/namespace/alias contract described by diagnostic_contract().  It must
obtain a real successful six-stage capture and Root terminal receipt first.

The two complete local DD arrays are retained uncompressed.  Components,
physical signs, and iteration defects are statistics of already archived raw
operands; none is a fit, a replacement convergence gate, or a qualification.
"""
from pathlib import Path
import hashlib
import json
import math
import os
import struct
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
SOURCE = ART / 'axial-material-rank1-cache-memory-native-angular-diagnostics-admission-20261007'
OUT = ART / 'axial-material-rank1-cache-memory-native-angular-diagnostics-20261007'
TERMINAL = ART / 'axial-material-rank1-cache-memory-native-angular-diagnostics-terminal-20261007'
CAPTURE = ART / 'axial-material-rank1-cache-memory-native-angular-capture-20261007'
CAPTURE_FACTORY = ROOT / 'validation/axial_material/prepare_rank1_cache_memory_native_angular_capture.py'
CAPTURE_FACTORY_SHA = 'ebc53e9e9fd88c4208ef776333b363d17c27ca2d40f3a09161dbdb51d1c93f8e'
NG, NZ, NA, NR, NL, NUN, NMAT = 370, 48, 32, 8, 3, 1800, 24
STAGE_WALL, TOTAL_WALL, RSS_MIB = 60, 120, 512
RESERVE, HISTORY_CAP, FREE_FLOOR = 16 * 2**20, 96 * 2**30, 8 * 2**30
DD_HEADER_BYTES = 40
DD_PAYLOAD_BYTES = 2 * NG * NZ * NA * 8
SOURCE_RESERVE = 2**20
RESULT_JSON_RESERVE = 2 * 2**20
OTHER_METADATA_RESERVE = 2 * 2**20
FORECAST = DD_HEADER_BYTES + DD_PAYLOAD_BYTES + SOURCE_RESERVE + RESULT_JSON_RESERVE + OTHER_METADATA_RESERVE
TAIL_FIELDS = ('actual_tail_check', 'actual_elapsed_seconds', 'actual_archive_bytes', 'actual_resources')


def diagnostic_contract():
    """A target contract, not evidence of a declaration, launch, or success."""
    if DD_PAYLOAD_BYTES != 9093120 or FORECAST >= RESERVE:
        raise ValueError('complete uncompressed local ledger does not fit the fixed reserve')
    return dict(schema='AXMAT_RANK1_MEMORY_ANGULAR_DIAGNOSTIC_SOURCE_PLAN_V1',
        source_root=str(SOURCE), output_root=str(OUT), terminal_root=str(TERMINAL),
        total_wall_seconds=TOTAL_WALL, stage_wall_seconds=STAGE_WALL,
        rss_cap_mib=RSS_MIB, threads=1, children_at_once=1, retries=0,
        complete_archive_roots=[str(SOURCE), str(OUT)], archive_cap_bytes=RESERVE,
        artifact_budget_bytes=HISTORY_CAP, min_free_bytes=FREE_FLOOR,
        exact_uncompressed_DD_ledger_bytes=DD_HEADER_BYTES + DD_PAYLOAD_BYTES,
        source_reserve_bytes=SOURCE_RESERVE, result_json_reserve_bytes=RESULT_JSON_RESERVE,
        other_metadata_reserve_bytes=OTHER_METADATA_RESERVE, complete_archive_forecast_bytes=FORECAST,
        actual_six_stage_capture_admission_required=True, actual_Root_exit_zero_required=True,
        complete_Root_stdout_and_stderr_required=True, complete_four_tail_fields=list(TAIL_FIELDS),
        fresh_input_bytes_and_complete_namespaces_and_aliases_required=True,
        tested_direct_own_child_RSS_supervisor_required=True,
        stage_cap_is_not_parent_remaining_cap=True,
        full_matrix_diagnostic_limit=1e-10, local_DD_diagnostic_limit=1e-10,
        actual_block_inverse_required='Every lower/diagonal/upper REAL64 bit, including signed zero',
        source_fields_required=['actual SGAS', 'actual QEXT', 'source_m', 'MN', 'DN',
            'Gram mass', 'total_m', 'scat_m', 'radial_m', 'white_mode', 'white_angle'],
        native_fields_required=['last actual angular cell and all shared faces', 'last S2',
            'slot6/slot7 before terminal acceleration', 'old outer/slot3/slot7/slot8',
            'one actual global normalization factor', 'all370 first-miss blocks and all hit keys'],
        approximation_changed=False, source_fitting=False, thresholds_changed=False,
        declared=False, executed=False, AAA_accuracy_qualified=False, ABA_admitted=False)


def _write_json(path, value, limit):
    raw = (json.dumps(value, separators=(',', ':'), allow_nan=False) + '\n').encode('utf-8')
    if len(raw) > limit:
        raise ValueError('declared compact JSON bound exceeded')
    with Path(path).open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())


def _check_time(started):
    if time.monotonic() - started >= STAGE_WALL:
        raise ValueError('original sixty-second scientific worker cap exhausted')


def _relative(defect, scale):
    import numpy as np
    if defect.shape != scale.shape or not np.isfinite(defect).all() or not np.isfinite(scale).all() or (scale < 0).any():
        raise ValueError('finite raw defect and nonnegative scale required')
    zero = (scale == 0) & (defect != 0)
    ratio = np.divide(abs(defect), scale, out=np.zeros_like(scale), where=scale > 0)
    return float(ratio.max(initial=0)), int(zero.sum())


def _blocks(folder, group, first_dispatch):
    import numpy as np
    path = Path(folder) / f'angular_collision_g{group:03d}.bin'
    with path.open('rb') as stream:
        if stream.read(8) != b'AXCBL001':
            raise ValueError('original first-miss block schema differs')
        raw = stream.read(32)
        if len(raw) != 32:
            raise ValueError('incomplete first-miss block header')
        header = struct.unpack('<8i', raw)
        payload = stream.read()
    expected_bytes = 3 * NA * NA * (NZ + 1) * 8
    if (header[0] != group or header[1] != first_dispatch or header[4:] != (NA, NZ + 1, 1, 0)
            or len(payload) != expected_bytes):
        raise ValueError('all original rank-one first-miss blocks required')
    # Each complete matrix was written separately in Fortran order.
    width = NA * NA * (NZ + 1)
    values = np.frombuffer(payload, '<f8')
    arrays = tuple(values[i*width:(i+1)*width].reshape((NA, NA, NZ+1), order='F') for i in range(3))
    if any(not np.isfinite(a).all() for a in arrays):
        raise ValueError('nonfinite archived native collision block')
    return arrays


def collision(a, z):
    """Exact rank-one native KVALUE expression order; no scalar optical shortcut.

    SPOT1P64 boundary_solve starts KVALUE at +0, adds the diagonal total,
    subtracts three MN*S*DN terms, adds MN0*R*DN0, then the full white exchange.
    Separate NumPy elementary operations retain that element-wise order and do
    not replace the native coupled angular matrix with an attenuation formula.
    """
    import numpy as np
    c = np.zeros((NA, NA), dtype='<f8')
    i = np.arange(NA)
    c[i, i] += float(a['total_projected'][0, 0, z])
    for l in range(NL):
        term = a['mn'][:, l, None] * float(a['scat_projected'][0, 0, l, z])
        c -= term * a['dn'][l, None, :]
    term = a['mn'][:, 0, None] * float(a['radial_projected'][0, 0, z])
    c += term * a['dn'][0, None, :]
    c += float(a['white_mode'][0, 0]) * a['white_angle']
    return c


def block_inverse(a, blocks):
    """Match every native first-miss bit before drawing local-equation conclusions."""
    import numpy as np
    lower, diagonal, upper = (np.zeros((NA, NA, NZ+1), dtype='<f8', order='F') for _ in range(3))
    gram = float(a['mass'][0, 0]); mu = a['mu'].astype('<f8')
    if a['ncode'].tolist() != [1, 1] or (a['zcode'] != 0).any():
        raise ValueError('this diagnostic only implements the original paired vacuum boundaries')
    for n in range(NA):
        endpoint = 0 if mu[n] > 0 else NZ
        diagonal[n, n, endpoint] = 1.0
        diagonal[n, int(a['opposite'][n])-1, endpoint] = -float(a['zcode'][0 if endpoint == 0 else 1])
    matrices = []
    for z in range(NZ):
        c = collision(a, z); matrices.append(c)
        half = (0.5 * float(a['vol1d'][z])) * c
        for n in range(NA):
            d = float(mu[n]) * gram
            if mu[n] > 0:
                lower[n, :, z+1] = half[n]; diagonal[n, :, z+1] = half[n]
                lower[n, n, z+1] -= d; diagonal[n, n, z+1] += d
            else:
                diagonal[n, :, z] = half[n]; upper[n, :, z] = half[n]
                diagonal[n, n, z] -= d; upper[n, n, z] += d
    exact = all(actual.tobytes(order='F') == wanted.tobytes(order='F')
                for actual, wanted in zip(blocks, (lower, diagonal, upper), strict=True))
    maximum = max(float(abs(actual-wanted).max()) for actual, wanted in zip(blocks, (lower, diagonal, upper), strict=True))
    return matrices, dict(all_first_miss_block_words_exact=exact, maximum_absolute_block_inverse_difference=maximum)


def dd_ledger(a, matrices):
    """The actual DD equation, evaluated on the actual last source and angle field.

    For cell z and angle n: mu[n]*G*(face[z+1]-face[z]) + h*C(z)*cell = h*q.
    q[n]=sum_l MN[n,l]*source_m[l,z]. Positive rows reside at block z+1;
    negative rows reside at block z. Incoming vacuum rows are separate boundary
    identity equations. This follows the archived lower/diagonal/upper system.
    """
    import numpy as np
    defect = np.empty((NA, NZ), dtype='<f8', order='F')
    scale = np.empty_like(defect, order='F')
    stats = dict(streaming_abs_sum=0.0, total_abs_sum=0.0, scattering_abs_sum=[0.0]*NL,
        radial_return_abs_sum=0.0, white_exchange_abs_sum=0.0, source_abs_sum=0.0,
        white_P0_weighted_abs_sum=0.0, radial_P0_weighted_abs_sum=0.0,
        signed_P0_components_by_original_axial_band={name:dict(streaming=0.0,total=0.0,
            scattering=[0.0]*NL,radial=0.0,white=0.0,source_RHS=0.0)
            for name in ('bottom_four_fine_layers','interior_fine_layers','top_four_fine_layers')})
    gram = float(a['mass'][0, 0]); mu = a['mu'].astype('<f8')
    for z, c in enumerate(matrices):
        h = float(a['vol1d'][z]); phi = a['cell'][:, 0, z]
        left, right = a['face'][:, 0, z], a['face'][:, 0, z+1]
        q = np.zeros(NA, dtype='<f8')
        for l in range(NL):
            q += a['mn'][:, l] * float(a['source_projected'][l, z, 0])
        streaming = mu * gram * (right-left)
        defect[:, z] = streaming + h*(c @ phi) - h*q
        scale[:, z] = abs(mu)*gram*(abs(left)+abs(right)) + h*(abs(c) @ abs(phi)) + h*abs(q)
        total = h*float(a['total_projected'][0, 0, z])*phi
        radial = h*a['mn'][:, 0]*float(a['radial_projected'][0, 0, z])*float(a['dn'][0] @ phi)
        white = h*float(a['white_mode'][0, 0])*(a['white_angle'] @ phi)
        stats['streaming_abs_sum'] += float(abs(streaming).sum())
        stats['total_abs_sum'] += float(abs(total).sum())
        stats['radial_return_abs_sum'] += float(abs(radial).sum())
        stats['white_exchange_abs_sum'] += float(abs(white).sum())
        stats['source_abs_sum'] += float(abs(h*q).sum())
        stats['white_P0_weighted_abs_sum'] += abs(float(a['dn'][0] @ white))
        stats['radial_P0_weighted_abs_sum'] += abs(float(a['dn'][0] @ radial))
        band = stats['signed_P0_components_by_original_axial_band'][
            'bottom_four_fine_layers' if z < 4 else 'top_four_fine_layers' if z >= NZ-4 else 'interior_fine_layers']
        for name, term in (('streaming',streaming),('total',total),('radial',radial),
                ('white',white),('source_RHS',h*q)):
            band[name] += float(a['dn'][0] @ term)
        for l in range(NL):
            term = -h*a['mn'][:, l]*float(a['scat_projected'][0, 0, l, z])*float(a['dn'][l] @ phi)
            stats['scattering_abs_sum'][l] += float(abs(term).sum())
            band['scattering'][l] += float(a['dn'][0] @ term)
    return defect, scale, stats


def full_matrix_ledger(a, blocks):
    """Freshly evaluate all 32x49 original equations, including vacuum rows."""
    import numpy as np
    lower, diagonal, upper = blocks
    face = a['face'][:, 0]
    rhs = np.zeros((NA, NZ+1), dtype='<f8')
    for z in range(NZ):
        q = np.zeros(NA, dtype='<f8')
        for l in range(NL):
            q += a['mn'][:, l]*a['source_projected'][l, z, 0]
        positive, negative = a['mu'] > 0, a['mu'] < 0
        rhs[positive, z+1] = float(a['vol1d'][z])*q[positive]
        rhs[negative, z] = float(a['vol1d'][z])*q[negative]
    defect = np.empty_like(rhs); scale = np.empty_like(rhs)
    for block in range(NZ+1):
        terms = [diagonal[:, :, block] @ face[:, block]]
        absolute = [abs(diagonal[:, :, block]) @ abs(face[:, block])]
        if block:
            terms.append(lower[:, :, block] @ face[:, block-1])
            absolute.append(abs(lower[:, :, block]) @ abs(face[:, block-1]))
        if block < NZ:
            terms.append(upper[:, :, block] @ face[:, block+1])
            absolute.append(abs(upper[:, :, block]) @ abs(face[:, block+1]))
        defect[:, block] = sum(terms)-rhs[:, block]
        scale[:, block] = sum(absolute)+abs(rhs[:, block])
    return defect, scale


def physical_signs(a):
    import numpy as np
    result = {}
    for label in ('cell', 'face'):
        modal = a[label][:, 0]
        physical = a['basis'][:, 0, None, None].astype('<f8') * modal[None]
        if not np.isfinite(physical).all():
            raise ValueError('nonfinite physical angular reconstruction')
        coordinates = np.argwhere(physical < 0)
        result[label] = dict(physical_values=int(physical.size), minimum_physical=float(physical.min()),
            negative_physical_count=int((physical < 0).sum()),
            negative_physical_zero_count=int(((physical == 0) & np.signbit(physical)).sum()),
            first_negative_coordinates_radial_angle_layer=coordinates[:8].tolist(),
            minimum_modal=float(modal.min()), negative_modal_count=int((modal < 0).sum()),
            modal_negativity_is_not_physical_negativity=True)
    incoming = np.concatenate((a['face'][a['mu']>0,0,0],a['face'][a['mu']<0,0,-1]))
    result['vacuum_inflow'] = dict(modal_nonzero_count=int((incoming!=0).sum()),
        mathematically_exact_zero=bool((incoming==0).all()), signed_zero_is_not_negative_flux=True)
    return result


def iteration_summary(previous, current, actual_volume, actual_factor):
    import numpy as np
    if previous.shape != (NUN,) or current.shape != (NUN,) or not math.isfinite(actual_factor) or actual_factor <= 0:
        raise ValueError('complete actual slots and positive single global normalization required')
    before = (previous[:1152]*actual_factor).reshape((1, NL, NZ, NR), order='F')[0]
    after = (current[:1152]*actual_factor).reshape((1, NL, NZ, NR), order='F')[0]
    volume = actual_volume
    rows = []
    for l in range(NL):
        delta = after[l]-before[l]
        norm = math.sqrt(float((volume*after[l]*after[l]).sum()))
        value = math.sqrt(float((volume*delta*delta).sum()))
        rows.append(dict(moment=l, observed_volume_L2_defect=value, current_volume_L2_norm=norm,
            relative_volume_L2=None if norm == 0 else value/norm,
            zero_norm_nonzero_defect=bool(norm == 0 and value != 0),
            maximum_absolute_physical_region_defect=float(abs(delta).max()),
            norm_is_actual_keff_over_FISOUR_applied_to_both_slots=True,
            fitting_or_independent_rescaling=False, diagnostic_only=True))
    return rows


def end_shape(a, actual_volume):
    """P0 volume fractions of the original endpoint bands; no CE fit or target."""
    import numpy as np
    phi = a['flux'][0, 0].astype('<f8')
    volume = actual_volume
    weighted = volume*phi; total = float(weighted.sum())
    if not math.isfinite(total) or total == 0:
        return dict(pre_normal_P0_volume_integral=total, fractions_defined=False, diagnostic_only=True)
    by_ring = []
    for i in range(NR):
        ring_total = float(weighted[:, i].sum())
        by_ring.append(dict(radial_index=i+1, full_height_integral=ring_total,
            bottom_four_layers_integral=float(weighted[:4, i].sum()),
            top_four_layers_integral=float(weighted[-4:, i].sum()),
            bottom_fraction=None if ring_total == 0 else float(weighted[:4, i].sum())/ring_total,
            top_fraction=None if ring_total == 0 else float(weighted[-4:, i].sum())/ring_total))
    return dict(pre_normal_P0_volume_integral=total, fractions_defined=True, radial_rows=by_ring,
        original_height_cm=150, original_endpoint_band_cm=12.5,
        actual_stored_REAL32_VOLUME_used=True, actual_global_normalization_cancels_from_fractions=True,
        new_CE_bias_or_accuracy_claim=False, fitted=False, diagnostic_only=True)


def nusigf(macro, directory, nfis):
    """The original export's isotope-column sum; no regenerated XS or fitted rate."""
    import numpy as np
    entry = directory.get('NUSIGF')
    if entry is None:
        return np.zeros(NMAT,dtype='<f8'),dict(present=False,original_export_zero_field_convention=True)
    if entry[1:] != (NMAT*nfis,2):
        raise ValueError('original all-isotope NUSIGF material/word ABI differs')
    raw = macro.read(entry[0],entry[1])
    field = np.frombuffer(raw,'<f4').reshape((NMAT,nfis),order='F')
    if not np.isfinite(field).all() or (field<0).any():
        raise ValueError('finite nonnegative original NUSIGF required')
    coefficients = np.zeros(NMAT,dtype='<f8')
    for material in range(NMAT):
        for isotope in range(nfis):
            coefficients[material] += float(field[material,isotope])
    return coefficients,dict(present=True,isotope_columns=nfis,actual_materials=NMAT,
        original_REAL32_words_sha256=hashlib.sha256(raw).hexdigest())


def coarse_shape(phi, rate):
    """Original 48-to-12 volume-integral grouping; no new CE accuracy assessment."""
    import numpy as np
    total = float(rate.sum())
    if not math.isfinite(total) or total <= 0:
        raise ValueError('original positive globally normalized nu-fission integral required')
    rows=[]
    for radial in range(NR):
        for z in range(12):
            rows.append(dict(radial_index=radial+1,observer_cell=z+1,
                phi_volume_integral_over_global_F=float(phi[4*z:4*z+4,radial].sum())/total,
                nu_fission_fraction=float(rate[4*z:4*z+4,radial].sum())/total))
    return dict(actual_370_group_global_F=total,original_observer_bins=96,rows=rows,
        actual_published_FLUX64_and_stored_VOLUME_and_NUSIGF_used=True,
        reference_CE_statistics_consumed=False,new_discrepancy_or_qualification_claim=False,fitted=False)


def macro_comparison(macro, directory, a):
    """Only actual SIGW operands; unavailable fields are never manufactured as zero."""
    import numpy as np
    rows = []
    for l in range(NL):
        name = f'SIGW{l:02d}'
        entry = directory.get(name)
        if entry is None:
            rows.append(dict(moment=l, original_macro_field=name, present=False,
                reconstructed_as_zero=False, lack_of_field_is_not_an_operator_validation=True))
            continue
        if entry[1:] != (NMAT, 2):
            raise ValueError('original SIGW material/type ABI differs')
        raw = macro.read(entry[0], entry[1])
        if len(raw) != NMAT*4:
            raise ValueError('complete raw original SIGW words required')
        wanted = np.frombuffer(raw, '<f4')
        actual = a['sgas'][1:, l]
        if not np.isfinite(wanted).all():
            raise ValueError('nonfinite raw macro SIGW')
        rows.append(dict(moment=l, original_macro_field=name, present=True,
            all_actual_24_SGAS_words_raw_equal=actual.tobytes()==raw,
            macro_nonzero_count=int((wanted != 0).sum()), actual_receiver_nonzero_count=int((actual != 0).sum()),
            maximum_absolute_difference=float(abs(actual.astype('<f8')-wanted.astype('<f8')).max()),
            upstream_transport_self_reduction_is_not_assumed_absent=True,
            difference_is_not_automatically_the_CE_bias_cause=True))
    return rows


def derive(capture_module, capture_admission, output_directory, fresh_checkpoint):
    """Future bounded child API; does not obtain or invent a completion admission.

    The future driver must genuinely call the pinned capture diagnostic_admission
    with its actual seal and actual Root receipt inside its 120-second budget.
    It supplies that exact returned dictionary, frozen inputs, and a callable
    fresh_checkpoint that actually rechecks the complete declared bytes,
    namespaces, aliases, environment and live family resources. No stat/hash
    cache or True-only callback is a valid implementation of that contract.
    This worker is not independently launchable until that driver is reviewed.
    """
    import numpy as np
    started = time.monotonic()
    module_path = Path(capture_module.__file__).resolve()
    if module_path != CAPTURE_FACTORY or hashlib.sha256(module_path.read_bytes()).hexdigest() != CAPTURE_FACTORY_SHA:
        raise ValueError('genuine frozen capture module identity required')
    if (capture_admission['schema'] != 'AXMAT_RANK1_MEMORY_NATIVE_ANGULAR_CAPTURE_INPUT_ADMISSION_V1'
            or capture_admission['capture_seal']['path'] != str(CAPTURE/'seal.json')
            or capture_admission['actual_native_RSS_under_512_guard_passed'] is not True
            or capture_admission['capture_only'] is not True
            or any(capture_admission[k] is not False for k in ('scientific_qualification',
                'AAA_accuracy_qualified', 'ABA_admitted', 'production_solver_promoted'))
            or capture_admission['source'] != dict(path=str(CAPTURE_FACTORY), sha256=CAPTURE_FACTORY_SHA)):
        raise ValueError('only the real completed new six-stage diagnostic may be an input')
    target = Path(output_directory)
    if target != OUT/'audit' or not target.is_dir() or any(target.iterdir()):
        raise ValueError('exclusive empty future diagnostic output required')
    fresh_checkpoint(); _check_time(started)
    capture = capture_module.read_capture(CAPTURE/'AAA/angular_capture.bin')
    if capture['dimensions'][6] != NMAT or capture['terminal_integer'][:7].tolist() != [3,1,371,1,1,500,740]:
        raise ValueError('original production shape and actual final call required')
    factor = float(capture['normalization'][0]/capture['normalization'][1])
    slot_path = CAPTURE/'AAA/angular_terminal_slots.bin'
    header, slots = capture_module.read_stream(slot_path, b'AXCTS001', 4, [NUN*NG]*4)
    if header.tolist() != [NUN,NG,3,1]:
        raise ValueError('actual chronological terminal slots required')
    old_outer, slot3, slot7, slot8 = [x.reshape((NUN,NG), order='F') for x in slots]
    inner_header, inner_slots = capture_module.read_stream(CAPTURE/'AAA/angular_slot7_phase1.bin',
        b'AXCS7001', 7, [NUN*NG]*2)
    if inner_header[:5].tolist() != [1,NUN,NG,3,1] or inner_header[6] != 0:
        raise ValueError('last actual unaccelerated inner slots required')
    slot6, inner7 = [x.reshape((NUN,NG), order='F') for x in inner_slots]
    if inner7.tobytes() != slot7.tobytes() or slot3.tobytes() != slot7.tobytes():
        raise ValueError('actual last group result must be terminal promoted slot7')
    full, production, _, handles = capture_module.modules()
    rows = []
    phi = np.zeros((NZ,NR),dtype='<f8'); rate = np.zeros_like(phi)
    with capture_module.stream_xsm(CAPTURE/'AAA/initial_axial_track.xsm') as track:
        keys = np.frombuffer(track.record(track.root,'KEYFLX',NZ*NR,1),'<i4').reshape((NZ,NR),order='F').copy()
        materials = np.frombuffer(track.record(track.root,'MATCOD',NZ*NR,1),'<i4').reshape((NZ,NR),order='F').copy()
        actual_volume = np.frombuffer(track.record(track.root,'VOLUME',NZ*NR,2),'<f4').astype('<f8').reshape((NZ,NR),order='F')
    if (not np.isfinite(actual_volume).all() or (actual_volume<=0).any()
            or (materials<1).any() or (materials>NMAT).any()
            or (keys<1).any() or (keys>1152).any() or np.unique(keys).size!=NZ*NR):
        raise ValueError('complete original physical scalar key/material/stored volume mapping required')
    ledger_path = target/'local_DD_defect_scale.bin'
    with capture_module.stream_xsm(CAPTURE/'AAA/initial_axial_macrolib.xsm') as macro:
        macro_state = struct.unpack('<40i',macro.record(macro.root,'STATE-VECTOR',40,1))
        nfis = macro_state[3]
        if macro_state[:2] != (NG,NMAT) or nfis<=0:
            raise ValueError('original macro group/material/fission-isotope dimensions required')
        groups = handles(macro, macro.root, 'GROUP', NG)
        with ledger_path.open('xb') as ledger:
            ledger.write(b'AXDDG001'); ledger.write(struct.pack('<8i',1,NG,NA,NZ,2,8,1,0))
            for g, group in enumerate(capture['groups'], 1):
                _check_time(started)
                a = capture_module.unpack(group, NMAT)
                if a['mat'].tobytes(order='F') != materials.astype('<i4').tobytes(order='F'):
                    raise ValueError('actual angular receiver and original exporter material maps differ')
                if group['context'][2:4].tolist() != [3,1]:
                    raise ValueError('only the actual last chronological source call may be analyzed')
                if slot7[:,g-1].tobytes() != group['returned'].tobytes() or slot8[:,g-1].tobytes() != group['s2'].tobytes():
                    raise ValueError('actual group source/result not bound to slot7/8')
                blocks = _blocks(CAPTURE/'AAA',g,int(group['context'][5]))
                matrices, inverse = block_inverse(a, blocks)
                defect, scale, components = dd_ledger(a, matrices)
                # Raw derived fields are durable before the floating-point gate.
                ledger.write(defect.tobytes(order='F')); ledger.write(scale.tobytes(order='F'))
                ledger.flush(); os.fsync(ledger.fileno())
                relative, zero = _relative(defect,scale)
                matrix_defect, matrix_scale = full_matrix_ledger(a,blocks)
                original_relative, original_zero = _relative(matrix_defect,matrix_scale)
                with np.load(CAPTURE/'audit'/f'ledger_g{g:03d}.npz',allow_pickle=False) as original:
                    saved_defect, saved_scale = original['defect'],original['scale']
                    matrix_exact = (saved_defect.shape == (NA,NZ+1) and saved_scale.shape == (NA,NZ+1)
                        and matrix_defect.tobytes() == saved_defect.tobytes()
                        and matrix_scale.tobytes() == saved_scale.tobytes())
                row = dict(group=g, original_final_context=group['context'].tolist(),
                    first_miss_block_inverse=inverse, local_DD_relative=relative,
                    local_zero_scale_nonzero_defects=zero, original_full_matrix_relative=original_relative,
                    original_full_matrix_zero_scale_nonzero_defects=original_zero,
                    freshly_recomputed_full_matrix_ledger_matches_original_words=matrix_exact,
                    physical_angular_signs=physical_signs(a), components=components,
                    measured_inner_P0_P1_P2=iteration_summary(slot6[:,g-1],slot7[:,g-1],actual_volume,factor),
                    measured_outer_P0_P1_P2=iteration_summary(old_outer[:,g-1],slot3[:,g-1],actual_volume,factor),
                    macro_receiver_SGAS=macro_comparison(macro,macro.directory(groups[g-1][0]),a),
                    endpoint_shape=end_shape(a,actual_volume), new_scientific_qualification=False)
                coefficient, provenance = nusigf(macro,macro.directory(groups[g-1][0]),nfis)
                row['original_NUSIGF_provenance'] = provenance
                # Same g/radial/z order and stored operands as the original export.
                for radial in range(NR):
                    for z in range(NZ):
                        value = float(group['published'][int(keys[z,radial])-1])
                        volume = float(actual_volume[z,radial])
                        phi[z,radial] += volume*value
                        rate[z,radial] += (volume*value)*float(coefficient[int(materials[z,radial])-1])
                rows.append(row)
                if not inverse['all_first_miss_block_words_exact'] or not matrix_exact or zero or original_zero or max(relative,original_relative)>1e-10:
                    _write_json(target/'failed_group.json',row,RESULT_JSON_RESERVE)
                    raise ValueError('actual block inverse or original full/local diagnostic ledger failed')
            ledger.flush(); os.fsync(ledger.fileno())
    if ledger_path.stat().st_size != DD_HEADER_BYTES+DD_PAYLOAD_BYTES:
        raise ValueError('complete original all370/all32/all48 local ledger coverage required')
    fresh_checkpoint(); _check_time(started)
    result = dict(schema='AXMAT_RANK1_MEMORY_NATIVE_ANGULAR_DIAGNOSTIC_FINDINGS_V1',
        classification='COMPLETE_READ_ONLY_NATIVE_ANGULAR_DIAGNOSTICS_ONLY',
        groups=rows, group_count=NG, directions=NA, fine_layers=NZ, radial_regions=NR,
        original_coarse_endpoint_shape=coarse_shape(phi,rate),
        actual_capture_admission=capture_admission,
        complete_local_DD_raw_ledger=dict(path=str(ledger_path),bytes=ledger_path.stat().st_size,
            sha256=hashlib.sha256(ledger_path.read_bytes()).hexdigest(),magic='AXDDG001',
            layout='Per group: defect[32,48], scale[32,48], each original REAL64 Fortran order'),
        input_raw_fields_copied_or_repaired=False, source_or_operator_reestimated=False,
        endpoint_CE_discrepancy_cause_proved=False, P1_P2_convergence_qualified=False,
        actual_whole_family_execution_or_RSS_claimed_by_this_worker=False,
        AAA_accuracy_qualified=False, ABA_admitted=False,
        resource_target=diagnostic_contract())
    _write_json(target/'findings.json',result,RESULT_JSON_RESERVE)
    _check_time(started)
    return result
