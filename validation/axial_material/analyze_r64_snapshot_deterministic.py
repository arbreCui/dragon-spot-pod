"""Independent binary export, source reconstruction and saved-terminal checks."""
import argparse
import hashlib
import math
import struct
from fractions import Fraction
import json
from pathlib import Path
import numpy as np


def _exact_square_sum_rn64(values):
    """Round an exact dyadic sum of squares once; refuse undefined extremes."""
    pairs = [float(value).as_integer_ratio() for value in values]
    power = max(denominator.bit_length() - 1 for _, denominator in pairs)
    accumulator = sum(
        numerator * numerator << (2 * (power - (denominator.bit_length() - 1)))
        for numerator, denominator in pairs
    )
    try:
        rounded = float(Fraction(accumulator, 1 << (2 * power)))
    except OverflowError as error:
        raise ValueError('deterministic diagnostic square sum overflow') from error
    if not math.isfinite(rounded):
        raise ValueError('deterministic diagnostic square sum overflow')
    if rounded == 0.0 and accumulator:
        raise ValueError('deterministic diagnostic square sum underflow')
    return rounded


def _sqrt_rn64(value):
    """Select the nearest binary64 sqrt by exact midpoint comparison."""
    if not math.isfinite(value) or value < 0.0:
        raise ValueError('invalid deterministic diagnostic square sum')
    if value == 0.0:
        return 0.0
    exact = Fraction(value)
    candidate = math.sqrt(value)
    square = Fraction(candidate) ** 2
    if square == exact:
        return candidate
    if square < exact:
        lower, upper = candidate, math.nextafter(candidate, math.inf)
    else:
        lower, upper = math.nextafter(candidate, 0.0), candidate
    if not (math.isfinite(upper) and
            Fraction(lower) ** 2 <= exact <= Fraction(upper) ** 2):
        raise ValueError('deterministic diagnostic sqrt seed is not an adjacent bracket')
    midpoint = (Fraction(lower) + Fraction(upper)) / 2
    if exact < midpoint ** 2:
        return lower
    if exact > midpoint ** 2:
        return upper
    lower_bits = struct.unpack('<Q', struct.pack('<d', lower))[0]
    return lower if lower_bits % 2 == 0 else upper


def _deterministic_saved_source_relative_l2(source_saved, q):
    """A diagnostic only: exact squares -> RN64 -> RN64 sqrt -> RN64 divide.

    All original qualification predicates are evaluated independently. Zero
    numerator returns 0.0. A zero denominator, nonfinite difference, overflow,
    or nonzero square sum that rounds to zero is refused, never admitted.
    """
    if (source_saved.shape != (14, 370) or q.shape != (14, 370) or
            source_saved.dtype != np.dtype('float64') or
            q.dtype != np.dtype('float64') or
            not np.isfinite(source_saved).all() or not np.isfinite(q).all()):
        raise ValueError('unsupported deterministic diagnostic operands')
    with np.errstate(over='ignore', invalid='ignore'):
        difference = np.subtract(source_saved, q)
    if not np.isfinite(difference).all():
        raise ValueError('nonfinite deterministic diagnostic difference')
    numerator = _sqrt_rn64(_exact_square_sum_rn64(difference.ravel(order='K')))
    denominator = _sqrt_rn64(_exact_square_sum_rn64(q.ravel(order='K')))
    if denominator <= 0.0:
        raise ValueError('nonpositive deterministic diagnostic denominator')
    try:
        result = float(Fraction(numerator) / Fraction(denominator))
    except OverflowError as error:
        raise ValueError('deterministic diagnostic ratio overflow') from error
    if not math.isfinite(result):
        raise ValueError('nonfinite deterministic diagnostic ratio')
    return result



def analyze(path):
    data = path.read_bytes()
    offset = 0
    def take(dtype, shape):
        nonlocal offset
        count = int(np.prod(shape))
        result = np.frombuffer(data, dtype=dtype, count=count, offset=offset).reshape(shape, order='F').copy()
        offset += result.nbytes
        if not np.isfinite(result).all():
            raise ValueError('nonfinite exported values')
        return result
    header = take('<i4',(5,))
    if header.tolist() != [370,8,14,8,32]:
        raise ValueError('unsupported export dimensions')
    k = float(take('<f8',(1,))[0]); volume = take('<f4',(8,)).astype('f8')
    mat = take('<i4',(8,)); key = take('<i4',(8,))-1
    phi = take('<f8',(14,370)); mirror = take('<f4',(14,370))
    source_saved = take('<f8',(14,370))
    nuf = take('<f4',(8,32,370)).astype('f8'); chi = take('<f4',(8,32,370)).astype('f8')
    total = take('<f4',(9,370)).astype('f8'); within = take('<f4',(9,370)).astype('f8')
    scat = take('<f4',(8,370,370)).astype('f8')
    q = take('<f8',(14,370)); fresh = take('<f8',(14,370))
    if offset != len(data) or mat.tolist() != list(range(1,9)) or len(set(key)) != 8 or np.any((key<0)|(key>=14)):
        raise ValueError('invalid export layout or mapping')
    if k <= 0 or np.any(volume<=0) or np.any(phi[key]<=0) or np.any(fresh[key]<=0):
        raise ValueError('nonpositive state')
    if not np.array_equal(phi.astype('<f4').view('<u4'), mirror.view('<u4')):
        raise ValueError('binary32 mirror differs')
    scalar = phi[key]
    production = np.einsum('msj,mj->ms', nuf, scalar, optimize=False)
    qfis = np.einsum('msi,ms->mi', chi, production, optimize=False)/k
    idx = np.arange(370)
    scat[:,idx,idx] = 0.0
    qoff = np.einsum('mij,mj->mi', scat, scalar, optimize=False)
    q_check = np.zeros_like(q); q_check[key] = qfis+qoff
    bound = 4096*np.finfo('f8').eps*np.maximum(np.abs(q), np.abs(q_check))
    if np.any(np.abs(q_check-q)>bound):
        raise ValueError('independently reconstructed source differs')
    prod = np.sum(qfis*volume[:,None])*k
    loss = np.sum(((total[1:]-within[1:])*scalar-qoff)*volume[:,None])
    if prod<=0 or loss<=0:
        raise ValueError('nonpositive global production/loss')
    balance_k = float(prod/loss)
    delta = np.max(np.abs(fresh[key]-scalar),axis=0)/np.max(np.abs(fresh[key]),axis=0)
    all_delta = np.max(np.abs(fresh-phi),axis=0)/np.max(np.abs(fresh),axis=0)
    eps = float(np.float32(2.5e-7))
    k_defect = abs(k-balance_k)/balance_k
    geometry_r = np.array([.11,.308712,.381084,.412536,.4225,.435,.485])
    rings = np.diff(np.r_[0,np.pi*geometry_r**2])
    area = 3*np.sqrt(3)*.61776479**2/2
    expected_volume = np.r_[area-np.pi*geometry_r[-1]**2, rings[::-1]]
    geometry_error = float(np.max(np.abs(volume/expected_volume-1)))
    checks = dict(exact_binary32_mirror=True, positive_scalar_flux=True,
        source_reconstruction=True, geometry=geometry_error<=5e-6,
        fresh_scalar_image=bool(np.max(delta)<eps), fresh_full_image=bool(np.max(all_delta)<eps),
        global_balance_keff=k_defect<eps)
    return dict(classification='R64_SNAPSHOT_TERMINAL_AUDIT_PASS' if all(checks.values()) else 'R64_SNAPSHOT_TERMINAL_AUDIT_FAIL',
        checks=checks, k_effective64=k, independent_balance_k=balance_k,
        relative_k_balance_defect=k_defect, maximum_scalar_image_defect=float(np.max(delta)),
        maximum_full_image_defect=float(np.max(all_delta)), terminal_threshold=eps,
        maximum_geometry_relative_error=geometry_error, minimum_scalar_flux=float(np.min(scalar)),
        maximum_source_reconstruction_difference=float(np.max(np.abs(q-q_check))),
        saved_source_vs_rebuilt_relative_l2=_deterministic_saved_source_relative_l2(source_saved, q),
        binary32_terminal_qualified=False, production_qualified=False, aaa_qualified=False,
        scope='Saved binary64 terminal, exact binary32 mirror and one independently reconstructed all-group fixed-source image at unchanged tolerances. Not independent transport physics or a CE accuracy comparison.',
        groups=[dict(group=i+1,scalar_image_defect=float(delta[i]),full_image_defect=float(all_delta[i])) for i in range(370)],
        export_sha256=hashlib.sha256(data).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export',type=Path);parser.add_argument('output',type=Path)
    args = parser.parse_args()
    result = analyze(args.export)
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False);stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='groups'},indent=2))


if __name__=='__main__':
    main()
