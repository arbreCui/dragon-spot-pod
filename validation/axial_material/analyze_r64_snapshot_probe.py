"""Recompute REAL64/serialized/negative residuals from saved probe vectors."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import struct
import sys


def analyze(text):
    rows, vectors = {}, {}
    for line in text.splitlines():
        if line.startswith('AXMAT-R64 GROUP='):
            fields = line.removeprefix('AXMAT-R64 GROUP=').split()
            group = int(fields[0])
            if group in rows or len(fields) != 7:
                raise ValueError('bad or duplicate group')
            rows[group] = list(map(float, fields[1:]))
        elif line.startswith('AXMAT-R64-VECTOR '):
            fields = line.split()
            key = tuple(map(int, fields[1:3]))
            if key in vectors or len(fields) != 11:
                raise ValueError('bad or duplicate vector')
            vectors[key] = list(map(float, fields[3:]))
    if set(rows) != set(range(1, 371)) or set(vectors) != {(g, i) for g in rows for i in range(1, 15)}:
        raise ValueError('incomplete coverage')
    if text.count('AXMAT-R64-FIRST-CALL-PROBE-COMPLETE') != 1:
        raise ValueError('incomplete probe')
    if 'STRICT INNER TERMINAL FAILED; GROUPS=370 ARNOLDI=2' not in text:
        raise ValueError('cap negative control did not reject')
    eps = struct.unpack('f', struct.pack('f', 2.5e-8))[0]
    result = []
    for group, summary in rows.items():
        field = [vectors[group, i] for i in range(1, 15)]
        if not all(math.isfinite(v) for r in [summary, *field] for v in r):
            raise ValueError('nonfinite observation')
        estimate, true64, true32, negative, repeat, norm = summary
        measured_norm = math.sqrt(math.fsum(r[0]**2 for r in field))
        if norm <= 0 or abs(norm-measured_norm) > 112*sys.float_info.epsilon*norm:
            raise ValueError('source norm differs')
        computed = [math.sqrt(math.fsum((r[y]-r[x])**2 for r in field))/norm
                    for x, y in ((1, 2), (4, 5), (6, 7))]
        for actual, saved in zip(computed, (true64, true32, negative)):
            if abs(actual-saved) > 112*sys.float_info.epsilon*max(actual, saved):
                raise ValueError('residual differs from vectors')
        if repeat != 0 or any(r[2] != r[3] for r in field):
            raise ValueError('nonrepeatable map')
        if any(struct.unpack('f', struct.pack('f', r[1]))[0] != r[4] for r in field):
            raise ValueError('incorrect demoted vector')
        if true64 >= eps or estimate >= eps or negative < eps:
            raise ValueError('positive/negative control failed')
        result.append(dict(group=group, true64=computed[0], true32=computed[1],
                           negative=computed[2], binary32_passes=computed[1]<eps))
    return dict(classification='R64_FIRST_CALL_AND_NEGATIVE_CONTROLS_VERIFIED',
        groups=370, vectors=5180, double_passes=370,
        binary32_passes=sum(r['binary32_passes'] for r in result),
        maximum_double_residual=max(r['true64'] for r in result),
        maximum_binary32_residual=max(r['true32'] for r in result),
        repeated_map_exact=True, perturbed_vector_rejected_groups=370,
        two_arnoldi_cap_rejected_groups=370, threshold=eps,
        snapshot_qualified=False, production_qualified=False,
        scope='First within-group solve only. Same source and coefficients; existing REAL64 operator. Binary32 mirror is not a qualified terminal at this inner tolerance.', rows=result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = analyze(args.log.read_text())
    result['log_sha256'] = hashlib.sha256(args.log.read_bytes()).hexdigest()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
