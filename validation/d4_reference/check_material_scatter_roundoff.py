"""Saved-output diagnosis, not a new physical acceptance tolerance."""
import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import runpy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
NEW = ROOT/'validation/artifacts/d4a-linear-temperature-namefix-tone650-run-20260929'
OLD = ROOT/'validation/artifacts/d4a-fe56-ganlib-tone650-run-20260929'


def rounding_interval(value):
    """Closed outer interval for one nearest-even binary32 rounding."""
    x = np.float32(value)
    if not np.isfinite(x):
        raise ValueError('finite binary32 values required')
    adjacent = [np.nextafter(x, np.float32(-np.inf)), x,
                np.nextafter(x, np.float32(np.inf))]
    if not all(np.isfinite(v) for v in adjacent):
        raise ValueError('overflow endpoint unsupported')
    lo, mid, hi = [Fraction.from_float(float(v)) for v in adjacent]
    return (lo+mid)/2, (mid+hi)/2


def diagnose_column(scalar, column):
    s = np.float32(scalar)
    c = np.asarray(column, dtype=np.float32)
    if c.ndim != 1 or not np.isfinite(c).all() or not np.isfinite(s):
        raise ValueError('finite scalar and one-dimensional column required')
    exact = sum((Fraction.from_float(float(v)) for v in c), Fraction())
    sl, sh = rounding_interval(s)
    intervals = [rounding_interval(v) for v in c]
    cl = sum((v[0] for v in intervals), Fraction())
    ch = sum((v[1] for v in intervals), Fraction())
    forward = reverse = np.float32(0)
    for v in c:
        forward = np.float32(forward+v)
    for v in c[::-1]:
        reverse = np.float32(reverse+v)
    sf = float(s)
    gap = exact-Fraction.from_float(sf)
    spacing = float(np.spacing(s))
    return dict(scalar_binary32=sf, exact_stored_column_sum=float(exact),
        exact_gap=float(gap), exact_gap_fraction=str(gap),
        relative_gap=float(gap)/sf if sf else None,
        scalar_ulp=spacing, gap_in_scalar_ulps=float(gap)/spacing if spacing else None,
        nonzero_entries=int(np.count_nonzero(c)),
        one_final_rounding_intervals_overlap=max(sl, cl) <= min(sh, ch),
        scalar_pre_rounding_interval=[float(sl), float(sh)],
        column_pre_rounding_sum_interval=[float(cl), float(ch)],
        ascending_binary32_sum=float(forward), descending_binary32_sum=float(reverse),
        ascending_equals_scalar=bool(forward == s), descending_equals_scalar=bool(reverse == s))


def check():
    a = runpy.run_path(str(NEW/'run_once.py'), run_name='read_only')
    sha, decode, verify, nr = (a[k] for k in ('sha', 'decode', 'verify', 'nr'))
    assert sha(NEW/'result.sha256') == '6dbcf7a175ef03f07f73621c1c194eff8d1cf0642f2d9edbdb88f943348e12cf'
    assert sha(OLD/'result.sha256') == '26770010b089c335a791499e4353b7443c6c3c8b9ac5e5b70a53403e2e330b5f'
    pins = {}
    for run in (NEW, OLD):
        pins.update({str(run/s.split(maxsplit=1)[1]): s.split(maxsplit=1)[0]
                     for s in (run/'result.sha256').read_text().splitlines()})
    for name in ('LIBDEN.f', 'LIBDRA.f', 'LIBDRB.f', 'LIBMIX.f'):
        p = ROOT/'src'/name
        pins[str(p)] = sha(p)
    verify(pins)
    rows = []
    for label, run in (('cubic', OLD), ('linear', NEW)):
        path = run/'material/macro.ascii'
        decode(path)
        macro = nr.macro(path.read_bytes(), 370, 6)
        matrix = nr.scatter(macro, 0).astype('f4')
        scalar = nr.field(macro, 'SIGS00').astype('f4')
        sums = np.array([[math.fsum(matrix[m, :, g]) for g in range(370)] for m in range(6)])
        gaps = sums-scalar.astype('f8')
        m, g = np.unravel_index(np.argmax(abs(gaps)), gaps.shape)
        row = diagnose_column(scalar[m, g], matrix[m, :, g])
        row.update(label=label, worst_mix=int(m)+1, worst_group=int(g)+1,
                   scope='maximum absolute gap among all 2220 P0 columns')
        rows.append(row)
    meta = decode(NEW/'material/metadata.ascii')
    data = lambda key: nr.data(meta, (key,))
    names = data('ISOTOPESUSED').ljust(59*12)
    isotopes = [dict(index=i+1, alias=names[12*i:12*i+12].strip(),
                     density=data('ISOTOPESDENS')[i], temperature_K=data('ISOTOPESTEMP')[i])
                for i, m in enumerate(data('ISOTOPESMIX')) if m == rows[-1]['worst_mix']]
    assert len(isotopes) == 9 and not any(x['alias'].startswith('Fe56') for x in isotopes)
    verify(pins)
    return dict(status='SAVED_FLOAT32_DIAGNOSIS_NOT_ACCEPTANCE', rows=rows,
        worst_mixture_isotopes=isotopes, inputs_unchanged=True, sources=pins,
        script_sha256=sha(__file__), native_engines_started=0, production_accepted=False,
        source_findings=['LIBDEN.f:368 independently accumulates density-weighted SIGS in REAL.',
                         'LIBDEN.f:371 independently accumulates density-weighted SCAT in REAL.',
                         'Material deck deletes full MICROLIB after exporting Fe56 only.'],
        limits=['Closed rounding intervals give a necessary compatibility test, not a historical trace.',
                'A matching chosen sum order does not prove the actual LIBDEN accumulation path.',
                'Failure of one-final-rounding overlap does not rule out earlier accumulated rounding.',
                'Saved fuel isotope microscopic arrays are absent; exact mixing replay is unavailable.',
                'No source mutation, empirical tolerance or physical acceptance follows from this check.'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = check()
    with args.output.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'sources'}, indent=2))
