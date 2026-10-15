"""Read preserved NJOY GENDF reactions, with no engine or library writes.

Source only: this module has not been admitted or executed by a numerical host.
The caller supplies the actual input pin and its original budget callback.
Its result is processed GENDF evidence, not current TONE context, DRAGLIB byte
replay, full physical neutron balance, or reference qualification.

The bounded reader follows NJOY endf.f90 unformatted records and DRAGR
fvect/fmatr. NX is MT5 in DRAGR's malist/namedi, not a scalar multiplicity.
All 370 incident groups are covered by each section; unlisted groups are
the zero-initialized entries in original fvect/fmatr, with their presence
mask retained explicitly. MF6 values already include neutron yields.
"""

import hashlib
import math
import os
from pathlib import Path
import re
import stat
import struct


NG = 370
MAX_RECORD_BYTES = 2 ** 20
MAX_LIST_VALUES = 30 * 8 * (NG + 1)
MAX_RECORDS = 2_000_000


class ReactionReadError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReactionReadError(message)


def identity(value):
    return [value.st_dev, value.st_ino, value.st_mode, value.st_nlink,
            value.st_size, value.st_mtime_ns, value.st_ctime_ns]


def exact_integer(value, name):
    require(math.isfinite(value) and value == int(value), name)
    return int(value)


def validate_pin(expected):
    require(type(expected) is dict and set(expected) ==
            {'path', 'sha256', 'size_bytes', 'identity'}, 'complete typed pin')
    require(type(expected['sha256']) is str and
            re.fullmatch('[0-9a-f]{64}', expected['sha256']) is not None,
            'complete input SHA256')
    require(type(expected['size_bytes']) is int and expected['size_bytes'] > 0,
            'positive complete input size')
    require(type(expected['identity']) is list and len(expected['identity']) == 7
            and all(type(v) is int for v in expected['identity']), 'exact 7ID')
    path = Path(expected['path'])
    require(path.is_absolute() and '..' not in path.parts,
            'literal absolute input path')
    for item in (path, *path.parents):
        require(not item.is_symlink(), 'no input path aliases')
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            'regular single-link input')
    require(identity(before) == expected['identity'] and
            before.st_size == expected['size_bytes'], 'current complete input pin')
    return path, before


class Records:
    def __init__(self, stream, before, budget_check):
        self.stream = stream
        self.before = before
        self.budget_check = budget_check
        self.digest = hashlib.sha256()
        self.bytes = self.records = 0

    def read(self, count):
        self.budget_check()
        value = self.stream.read(count)
        self.digest.update(value)
        self.bytes += len(value)
        require(identity(os.fstat(self.stream.fileno())) == identity(self.before),
                'opened GENDF changed during fullEOF read')
        return value

    def next(self):
        marker = self.read(4)
        if not marker:
            return None
        require(len(marker) == 4, 'truncated GENDF record marker')
        count = struct.unpack('<i', marker)[0]
        require(20 <= count <= MAX_RECORD_BYTES and (count - 20) % 8 == 0,
                'bounded little-endian NJOY record size')
        data = self.read(count)
        trailer = self.read(4)
        require(len(data) == count and trailer == marker,
                'complete matching Fortran record markers')
        self.records += 1
        require(self.records <= MAX_RECORDS, 'bounded GENDF record count')
        mat, mf, mt, remaining, words = struct.unpack('<5i', data[:20])
        require(remaining >= 0 and words >= 0 and count == 20 + 8 * words,
                'NJOY unformatted header dimensions')
        return (mat, mf, mt), remaining, struct.unpack('<' + str(words) + 'd', data[20:])


def complete_list(reader, first):
    key, remaining, initial = first
    require(len(initial) >= 6, 'LIST header is complete')
    header = initial[:6]
    count = exact_integer(header[4], 'integer LIST NPL')
    require(0 <= count <= MAX_LIST_VALUES, 'bounded complete LIST payload')
    payload = list(initial[6:])
    require(len(payload) + remaining == count, 'first LIST continuation count')
    while remaining:
        row = reader.next()
        require(row is not None and row[0] == key, 'complete LIST identity')
        _, following, values = row
        require(0 < len(values) <= remaining and following == remaining - len(values),
                'strict continuation progress')
        payload.extend(values)
        remaining = following
    require(len(payload) == count and all(math.isfinite(v) for v in (*header, *payload)),
            'complete finite LIST values')
    return header, payload


def begin_section(header, key):
    require(len(header) == 6 and all(math.isfinite(v) for v in header),
            'complete finite reaction section header')
    nl = exact_integer(header[2], 'integer Legendre count')
    nz = exact_integer(header[3], 'integer dilution count')
    ng = exact_integer(header[5], 'integer energy-group count')
    require(1 <= nl <= 8 and 1 <= nz <= 30 and ng == NG,
            'current complete SHEM370 section dimensions')
    return {'mat': key[0], 'mf': key[1], 'mt': key[2], 'nl': nl, 'nz': nz,
            'temperature_K': None, 'incident_present': [False] * NG,
            'P0_vector64': [[0.0] * NG for _ in range(nz)],
            'separable_spectrum64': None, 'separable_spectrum_present': [False] * NG,
            'LIST_records': 0}


def consume(section, header, values):
    temperature = header[0]
    ng2, lower, group = [exact_integer(header[i], 'integer reaction LIST index')
                         for i in (2, 3, 5)]
    nl, nz, mf = section['nl'], section['nz'], section['mf']
    require(ng2 >= 1 and len(values) == ng2 * nl * nz and 0 <= group <= NG,
            'complete reaction LIST dimensions')
    require(section['temperature_K'] in (None, temperature), 'single section temperature')
    section['temperature_K'] = temperature
    section['LIST_records'] += 1
    if group == 0:
        require(mf == 6 and 1 <= lower and lower + ng2 - 1 <= NG,
                'explicit separable fission-spectrum indexing')
        require(section['separable_spectrum64'] is None, 'unique spectrum LIST')
        spectrum = [0.0] * NG
        for index in range(ng2):
            value = values[index * nz * nl]
            require(value >= 0.0, 'signed P0 spectrum is not repaired')
            spectrum[NG - (lower + index)] = value
            section['separable_spectrum_present'][NG - (lower + index)] = True
        section['separable_spectrum64'] = spectrum
        return
    incident = NG - group
    require(not section['incident_present'][incident], 'unique incident-group LIST')
    section['incident_present'][incident] = True
    require(ng2 >= 2, 'flux and reaction/transfer values required')
    if mf == 3:
        require(ng2 == 2, 'original fvect flux/reaction LIST layout')
        for z in range(nz):
            value = values[nl * nz + z * nl]
            require(value >= 0.0, 'signed P0 reaction XS is not repaired')
            section['P0_vector64'][z][incident] = value
    else:
        require(mf == 6 and (lower == 0 or 1 <= lower <= NG) and
                (lower == 0 or lower + ng2 - 2 <= NG), 'original fmatr destination range')
        for z in range(nz):
            row = [values[j * nz * nl + z * nl] for j in range(1, ng2)]
            require(all(v >= 0.0 for v in row), 'signed P0 production is not repaired')
            summed = math.fsum(row)
            if lower == 0:
                require(section['separable_spectrum64'] is not None,
                        'original fmatr separable spectrum must precede its rows')
                summed *= math.fsum(section['separable_spectrum64'])
            section['P0_vector64'][z][incident] = summed


def extract(expected_pin, material, wanted_mts, budget_check):
    """FullEOF GENDF extraction, without fitting/normalizing physical data.

    Typically wanted_mts=(5,) for the current eleven nonzero NX nuclides.
    The caller independently proves exact input provenance, absent reaction
    handling, DRAGR packed raw-word replay and TONE dilution/SPH context.
    No host may promote this extraction alone to whole reaction authority.
    """
    require(type(material) is int and material > 0, 'explicit actual material number')
    require(type(wanted_mts) in (list, tuple) and len(wanted_mts) > 0 and
            all(type(mt) is int and mt > 0 for mt in wanted_mts) and
            len(set(wanted_mts)) == len(wanted_mts), 'explicit unique reaction indices')
    path, before = validate_pin(expected_pin)
    selected = set(wanted_mts)
    sections = []
    seen = set()
    grids = []
    grid_temperatures = set()
    current_grid_nz = None
    active_key = active = None
    inventory = {}
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == identity(before), 'opened input identity')
        reader = Records(stream, before, budget_check)
        while True:
            first = reader.next()
            if first is None:
                break
            key, remaining, values = first
            mat, mf, mt = key
            if mf == 0 or mt == 0:
                require(remaining == 0, 'complete section boundary')
                if active is not None:
                    stamp = (active['mf'], active['mt'], active['temperature_K'])
                    require(stamp not in seen and active['LIST_records'] > 0,
                            'unique complete temperature/reaction section')
                    seen.add(stamp)
                    sections.append(active)
                active_key = active = None
                continue
            require(mat == material, 'single actual GENDF isotope material')
            if key != active_key:
                require(active_key is None and remaining == 0, 'explicit SEND before new section')
                active_key = key
                inventory[(mf, mt)] = inventory.get((mf, mt), 0) + 1
                if (mf, mt) == (1, 451):
                    require(len(values) == 6, 'complete GENDF grid section header')
                    current_grid_nz = exact_integer(values[3], 'integer MF1 dilution count')
                    require(1 <= current_grid_nz <= 30, 'bounded original dilution grid')
                if mf in (3, 6) and mt in selected:
                    active = begin_section(values, key)
                continue
            if mf in (1, 3, 5, 6):
                header, payload = complete_list(reader, first)
                if (mf, mt) == (1, 451):
                    ng = exact_integer(header[2], 'integer MF1 neutron groups')
                    ngg = exact_integer(header[3], 'integer MF1 photon groups')
                    require(ng == NG and ngg == 0 and current_grid_nz is not None and
                            len(payload) == 1 + current_grid_nz + NG + 1 + 1,
                            'complete original neutron-only SHEM370 grid')
                    require(header[0] not in grid_temperatures, 'unique original grid temperature')
                    sigma = payload[1:1 + current_grid_nz]
                    energy = payload[1 + current_grid_nz:2 + current_grid_nz + NG]
                    require(all(s > 0 for s in sigma) and len(set(sigma)) == len(sigma) and
                            all(a < b for a, b in zip(energy, energy[1:])),
                            'explicit finite original dilution/ascending energy grids')
                    grids.append({'temperature_K': header[0], 'sigma0_barn': sigma,
                                  'ascending_energy_eV': energy})
                    grid_temperatures.add(header[0])
                if active is not None:
                    consume(active, header, payload)
            else:
                require(remaining == 0, 'unknown format continuation requires Source extension')
        require(active_key is None, 'final complete GENDF section boundary')
        require(reader.bytes == before.st_size and reader.digest.hexdigest() == expected_pin['sha256'],
                'complete physical GENDF SHA/size')
        require(identity(os.fstat(stream.fileno())) == identity(before), 'final opened input identity')
    require(identity(path.lstat()) == identity(before), 'final physical input identity')
    require(sections, 'explicit requested reactions actually present')
    for section in sections:
        matches = [g for g in grids if g['temperature_K'] == section['temperature_K']]
        require(len(matches) == 1 and section['nz'] in (1, len(matches[0]['sigma0_barn'])),
                'actual section temperature/dilution grid is fully present')
    # Do not zero-fill a missing MF6 or assume that an MT label gives a constant
    # multiplicity. Keep actual per-file reaction absence and both masks.
    return {'schema': 'SAVED_BINARY_GENDF_REACTION_P0_EXTRACTION_ONLY_V1',
            'input_pin': expected_pin, 'mat': material, 'energy_groups': NG,
            'whole_file_records': reader.records,
            'P0_reduction_arithmetic': 'binary64 math.fsum of all saved outgoing contributions; no renormalization',
            'reaction_inventory': [{'mf': mf, 'mt': mt, 'sections': count}
                                   for (mf, mt), count in sorted(inventory.items())],
            'requested_mts': list(wanted_mts), 'actual_P0_sections': sections,
            'original_full_MF1_temperature_dilution_energy_grids': grids,
            'native_engines_started': 0, 'library_writes': 0,
            'current_SPH_MASK_context_produced': False,
            'DRAGR_packed_raw_words_replayed': False,
            'complete_reaction_authority_qualified': False,
            'physical_neutron_balance_qualified': False,
            'unreduced_reference_qualified': False}
