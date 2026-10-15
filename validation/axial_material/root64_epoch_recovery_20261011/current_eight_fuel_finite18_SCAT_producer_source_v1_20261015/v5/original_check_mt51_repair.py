"""Read-only MT51 scope and exact DRAGR scattering-storage replay.

The compression constants below reproduce the existing DRAGR implementation;
they are NOT new acceptance tolerances. Stored REAL32 values must match bytes.
This checker does not perform nuclear-data processing or a transport solve.
"""
from __future__ import annotations

import hashlib
import math
import re
import numpy as np

MTS = (2, 5, 16, 17, 28, 37, *range(51, 92))
OLD_T = (293., 550., 900., 1200., 2000.)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def number(field):
    s = field.strip()
    value = float(re.sub(r'(?<=[0-9.])([+-][0-9]+)$', r'e\1', s)) if s else 0.0
    require(math.isfinite(value), 'nonfinite GENDF value')
    return value


def fields(line):
    return [number(line[i:i+11]) for i in range(0,66,11)]


def identity(line):
    require(len(line) >= 75, 'short GENDF line')
    return tuple(int(line[a:b]) for a,b in ((66,70),(70,72),(72,75)))


def integer(value):
    require(value == int(value), 'nonintegral GENDF structure')
    return int(value)


def parse(raw, mat):
    """Read MF1 grids and MF6 scattering LISTs used by original drasc."""
    lines = iter(raw.decode('ascii').splitlines())
    result, grids = {}, {}
    for line in lines:
        m,mf,mt = identity(line)
        selected = mf == 6 and (mt in MTS or 221 <= mt <= 250)
        if (mf,mt) != (1,451) and not selected:
            continue
        require(m == mat, 'wrong GENDF material')
        h = fields(line)
        nz = integer(h[3])
        require(1 <= nz <= 30, 'unsupported dilution count')
        if (mf,mt) == (1,451):
            first = next(lines)
            require(identity(first) == (m,mf,mt), 'MF1 LIST identity')
            a = fields(first)
            ng, ngg, npl = map(integer, a[2:5])
            require(ng == 370 and npl == 1+nz+ng+1+ngg+1, 'MF1 dimensions')
            values = []
            for _ in range((npl+5)//6):
                data = next(lines)
                require(identity(data) == (m,mf,mt), 'MF1 payload identity')
                values += fields(data)
            require(a[0] not in grids, 'duplicate MF1 temperature')
            grids[a[0]] = dict(sigma0=values[1:1+nz], ascending_energy=values[1+nz:2+nz+ng])
            continue
        nl, ng = integer(h[2]), integer(h[5])
        require(nl == 2 and ng == 370, 'only original P0/P1 SHEM370 matrices supported')
        records, temperature = {}, None
        for first in lines:
            mid = identity(first)
            if mid != (m,mf,mt):
                require(mid == (m,mf,0), 'MF6 missing SEND')
                break
            a = fields(first)
            ng2, lower, npl, ig = map(integer,a[2:])
            require(ng2 >= 1 and npl == ng2*nl*nz and 0 <= ig <= ng, 'MF6 LIST dimensions')
            require(temperature is None or temperature == a[0], 'temperature changed within section')
            temperature = a[0]
            payload = []
            for _ in range((npl+5)//6):
                data = next(lines)
                require(identity(data) == (m,mf,mt), 'MF6 payload identity')
                payload += fields(data)
            require(ig not in records, 'duplicate MF6 incident group')
            records[ig] = (lower, np.asarray(payload[:npl],dtype='f8').reshape(ng2,nz,nl))
        else:
            raise ValueError('truncated MF6 section')
        require(temperature is not None and (temperature,mt) not in result, 'empty/duplicate MF6 section')
        result[temperature,mt] = dict(nz=nz, nl=nl, ng=ng, records=records)
    require(grids and result, 'missing GENDF data')
    return result, grids


def matrix(section):
    nz, nl, ng = (section[k] for k in ('nz','nl','ng'))
    rm = np.zeros((nz,nl,ng,ng),dtype='f8')  # dilution, moment, incident, outgoing
    flux = np.zeros((nz,nl,ng),dtype='f8')
    spectrum = np.zeros(ng,dtype='f8')
    for ig,(lower,data) in section['records'].items():
        if ig == 0:
            require(1 <= lower and lower+len(data)-1 <= ng, 'spectrum bounds')
            spectrum[lower-1:lower-1+len(data)] = data[:,0,0]
            continue
        jg = ng-ig
        flux[:,:,jg] = data[0]
        if lower:
            require(lower >= 1 and lower+len(data)-2 <= ng, 'outgoing group bounds')
            dest = ng-np.arange(lower,lower+len(data)-1)
            rm[:,:,jg,dest] += data[1:].transpose(1,2,0)
        else:
            for part in data[1:]:
                rm[:,:,jg,:] += part[:,:,None]*spectrum[::-1]
    return rm, flux


def non_mt51_digest(raw):
    h, count = hashlib.sha256(), 0
    for line in raw.decode('ascii').splitlines():
        if identity(line)[1:] == (6,51):
            continue
        h.update(line[:75].encode('ascii') + b'\n')
        count += 1
    return h.hexdigest(), count


def gendf_scope(before, after, mat, temperatures=OLD_T):
    require(non_mt51_digest(before) == non_mt51_digest(after), 'non-MF6/MT51 content changed')
    old, old_grid = parse(before,mat)
    new, new_grid = parse(after,mat)
    require(old_grid == new_grid and set(old_grid) == set(temperatures), 'grid/control-temperature drift')
    require(old.keys() == new.keys(), 'scattering reaction family drift')
    rows = []
    for t in temperatures:
        require(old[t,51]['nz'] == 1 and new[t,51]['nz'] == len(new_grid[t]['sigma0']), 'MT51 width not repaired')
        a,_ = matrix(old[t,51])
        b,_ = matrix(new[t,51])
        changed = np.any(a[0] != b[0],axis=(0,2))
        rows.append(dict(temperature_K=t, old_nz=1, new_nz=b.shape[0],
                         infinite_changed_primary_groups=(np.flatnonzero(changed)+1).tolist(),
                         new_P0_negative_values=int((b[:,0] < 0).sum())))
        require(not np.any(b[:,0] < 0), 'negative processed MT51 P0')
    return dict(non_MT51_content_exact=True, control_grids_exact=True, rows=rows,
                scope_only_not_physics_acceptance=True)


def accumulated_scattering(sections, temperature, thermal_groups):
    elastic = sections[temperature,2]
    require(elastic['nz'] > 1, 'finite-dilution trace requires elastic grid')
    nz, ng = elastic['nz'], elastic['ng']
    total = np.zeros((nz,2,ng,ng),dtype='f8')
    thermals = [mt for t,mt in sections if t == temperature and 221 <= mt <= 250]
    require(thermals == [221], 'this route declares only free-gas MT221')
    section = sections[temperature,221]
    ngther = min(max(ig for ig in section['records'] if ig != ng), thermal_groups)
    first = ng-ngther
    thermal,_ = matrix(section)
    require(section['nz'] == 1, 'thermal matrix dilution')
    total[:,:,first:,:] += thermal[:,:,first:,:]
    rm,flux = matrix(elastic)
    total[:,:,first:,:] -= rm[0:1,:,first:,:]
    for mt in MTS:
        if (temperature,mt) not in sections:
            continue
        part,_ = matrix(sections[temperature,mt])
        require(part.shape[0] in (1,nz), 'incompatible reaction dilution count')
        total += part
    return total, flux


def packed(matrix_, finite, ss, reference):
    """Original drasc index search/REAL32 storage, including existing cutoffs."""
    ng = matrix_.shape[0]
    first,last = ss
    counts, tops, stored = [], [], []
    # Fortran default-REAL literals are promoted to kr after REAL32 rounding.
    support_factor = float(np.float32(1e-6))
    tail_factor = float(np.float32(1e-8))
    for outgoing in range(ng):
        lo = hi = outgoing
        if finite:
            if outgoing < first-1:
                counts.append(1); tops.append(outgoing+1); stored.append(0.)
                continue
            selected = np.flatnonzero(np.abs(matrix_[first-1:last,outgoing]) >
                                      support_factor*np.abs(np.diag(reference)[first-1:last])) + first-1
        else:
            selected = np.flatnonzero(matrix_[:,outgoing] != 0)
        if len(selected):
            lo,hi = min(lo,int(selected.min())),max(hi,int(selected.max()))
        counts.append(hi-lo+1); tops.append(hi+1)
        for incoming in range(hi,lo-1,-1):
            stored.append(float(matrix_[incoming,outgoing]) if not finite or first-1 <= incoming < last else 0.)
    stored = np.asarray(stored,dtype='f4')
    if finite:
        limit = tail_factor*float(np.abs(stored).max())
        hit = np.flatnonzero(np.abs(stored).astype('f8') >= limit)
        stored = stored[:int(hit[-1])+1] if len(hit) else stored[:0]
    return counts,tops,stored


def equal_stored(actual, expected, kind, label):
    if kind == 2:
        require(np.isfinite(actual).all() and np.isfinite(expected).all(), label+': nonfinite value')
        require(np.asarray(actual,dtype='f4').tobytes() == np.asarray(expected,dtype='f4').tobytes(), label)
    else:
        require(tuple(actual) == tuple(expected), label)


def replay(raw, records, name, mat, ss, thermal_groups):
    sections, grids = parse(raw,mat)
    data = lambda key: records[key][1]
    require(records[(name,'TEMPERATURE')][0] == 2, 'temperature record type')
    library_t = np.asarray(data((name,'TEMPERATURE')),dtype='f4')
    require(np.isfinite(library_t).all() and len(np.unique(library_t)) == len(library_t),
            'nonfinite/duplicate library temperature')
    checked, rows = 0, []
    for t in sorted(grids):
        hits_t = np.flatnonzero(library_t == np.float32(t))
        require(len(hits_t) == 1, 'missing/ambiguous library temperature')
        prefix = (name,f'SUBTMP{int(hits_t[0])+1:04d}')
        sigma = np.asarray(grids[t]['sigma0'],dtype='f4')
        require(records[prefix+('DILUTION',)][0] == 2, 'dilution record type')
        dilutions = np.asarray(data(prefix+('DILUTION',)),dtype='f4')
        require(np.isfinite(dilutions).all() and len(np.unique(dilutions)) == len(dilutions),
                'nonfinite/duplicate finite dilution')
        require(all(np.count_nonzero(dilutions == value) == 1 for value in sigma[1:]),
                'finite dilution missing/duplicated in output')
        total,flux = accumulated_scattering(sections,t,thermal_groups)
        require(total.shape[0] == len(sigma), 'GENDF elastic/global sigma dimension')
        for z in range(len(sigma)):
            if z:
                hits = np.flatnonzero(dilutions == sigma[z])
                require(len(hits) == 1, 'finite dilution missing/duplicated in output')
                target = prefix+(f'SUBMAT{int(hits[0])+1:04d}',)
            else:
                target = prefix
            for moment in (0,1):
                if z:
                    ratio = flux[z,moment].copy()
                    nonzero = flux[0,moment] != 0
                    ratio[nonzero] /= flux[0,moment,nonzero]
                    value = total[z,moment]*ratio[:,None]-total[0,moment]
                else:
                    value = total[0,moment]
                njjs,ijjs,scat = packed(value,bool(z),ss,total[0,moment])
                suffix = f'{moment:02d}'
                for key,kind,expected in (('NJJS',1,njjs),('IJJS',1,ijjs),('SCAT',2,scat)):
                    record = target+(key+suffix,)
                    require(record in records and records[record][0] == kind, f'missing/type: {record}')
                    equal_stored(data(record),expected,kind,f'GENDF storage replay differs: {record}')
                    checked += 1
            rows.append(dict(temperature_K=t,sigma0_b=float(sigma[z]),finite=bool(z)))
    return dict(status='GENDF_TO_STORED_SCATTER_EXACT',records_checked=checked,nodes=rows,
                constants='Original DRAGR REAL32 1e-6 support and 1e-8 tail cutoffs, not new tolerances',
                production_accepted=False)


def non_scatter_records_exact(before, after):
    require(before.keys() == after.keys(), 'library record inventory changed')
    count = 0
    for key,(kind,value) in before.items():
        if key and re.fullmatch(r'(?:NJJS|IJJS|SCAT)0[01]',str(key[-1])):
            continue
        require(kind == after[key][0], f'record type changed: {key}')
        if kind in (2,4):
            dtype = 'f4' if kind == 2 else 'f8'
            require(np.asarray(value,dtype=dtype).tobytes() == np.asarray(after[key][1],dtype=dtype).tobytes(),
                    f'non-scattering real record changed: {key}')
        else:
            require(value == after[key][1], f'non-scattering record changed: {key}')
        count += 1
    return count
