"""Independently recompute the first MOC returned-vector residuals."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import struct
import sys


def analyze(text, groups=370, unknowns=14):
    summaries, vectors = {}, {}
    for line in text.splitlines():
        if line.startswith('AXMAT-TRUE GROUP='):
            match = re.fullmatch(r'AXMAT-TRUE GROUP=\s*(\d+) ITER=\s*(\d+) EST/TRUE/REPEAT/NORM=\s*(.*)', line)
            if not match:
                raise ValueError('malformed summary')
            group, iteration = map(int, match.group(1, 2))
            values = list(map(float, match[3].split()))
            if group in summaries or len(values) != 4:
                raise ValueError('duplicate or malformed summary')
            summaries[group] = (iteration, *values)
        elif line.startswith('AXMAT-VECTOR '):
            fields = line.split()
            key = tuple(map(int, fields[1:3]))
            if key in vectors or len(fields) != 7:
                raise ValueError('duplicate or malformed vector')
            vectors[key] = list(map(float, fields[3:]))
    if text.count('AXMAT-TRUE-RESIDUAL-PROBE-COMPLETE') != 1:
        raise ValueError('missing or repeated completion')
    if set(summaries) != set(range(1, groups + 1)):
        raise ValueError('incomplete group coverage')
    if set(vectors) != {(g, u) for g in summaries for u in range(1, unknowns + 1)}:
        raise ValueError('incomplete vector coverage')
    threshold = struct.unpack('f', struct.pack('f', 2.5e-8))[0]
    rows = []
    for group in sorted(summaries):
        iteration, estimate, reported, repeat, norm = summaries[group]
        vv = [vectors[group, u] for u in range(1, unknowns + 1)]
        if not all(math.isfinite(x) for row in vv for x in row) or not all(
                math.isfinite(x) for x in summaries[group]):
            raise ValueError('nonfinite observation')
        if norm <= 0 or min(estimate, reported, repeat) < 0:
            raise ValueError('invalid norm/residual')
        recomputed = math.sqrt(math.fsum((row[2] - row[1])**2 for row in vv)) / norm
        repeat_recomputed = max(abs(row[2] - row[3]) for row in vv)
        # 17-digit output preserves binary64 values. Bound reduction-order error.
        bound = 8 * unknowns * sys.float_info.epsilon * max(recomputed, reported)
        if abs(recomputed - reported) > bound:
            raise ValueError(f'group {group}: saved vectors disagree with residual')
        if repeat != repeat_recomputed or repeat != 0:
            raise ValueError(f'group {group}: repeated application differs')
        # Source norm was evaluated in binary32 in the native routine.
        norm64 = math.sqrt(math.fsum(row[0]**2 for row in vv))
        if abs(norm64 - norm) > (2 * unknowns + 2) * 2**-24 * norm64:
            raise ValueError(f'group {group}: source norm inconsistent')
        rows.append(dict(group=group, iterations=iteration, estimated=estimate,
                         true_residual=recomputed, original_source_norm=norm,
                         estimate_passes=estimate < threshold,
                         true_passes=recomputed < threshold,
                         ratio_true_to_estimated=recomputed / estimate if estimate else None))
    return dict(classification='VERIFIED_FIRST_RETURNED_VECTOR_OBSERVATIONS',
                numerical_acceptance=False, threshold=threshold, groups=groups,
                vector_rows=len(vectors), repeat_max_absolute_difference=0.0,
                estimated_pass_count=sum(r['estimate_passes'] for r in rows),
                true_pass_count=sum(r['true_passes'] for r in rows),
                false_acceptance_count=sum(r['estimate_passes'] and not r['true_passes'] for r in rows),
                maximum_true_residual=max(r['true_residual'] for r in rows),
                median_true_residual=statistics.median(r['true_residual'] for r in rows),
                maximum_ratio_true_to_estimated=max(r['ratio_true_to_estimated'] or 0 for r in rows),
                limitations='First within-group solve only. Residual uses the same native preconditioned map and original source norm. Does not prove a unique cause of outer stagnation, a precision lower bound, physical accuracy, or a qualified snapshot.',
                rows=rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    raw = args.log.read_bytes()
    result = analyze(raw.decode())
    result['log'] = dict(path=str(args.log.resolve()), sha256=hashlib.sha256(raw).hexdigest())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
