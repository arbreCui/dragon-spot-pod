"""Independently replay unchanged tracks and verify their binary64 normalization."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct

import numpy as np


def analyze(track_path, moments_path, volume64_path=None):
    data = track_path.read_bytes()
    records = []
    offset = 0
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError('truncated tracking record')
        n = struct.unpack_from('<i', data, offset)[0]
        if n < 0 or offset + n + 8 > len(data):
            raise ValueError('invalid tracking record length')
        if struct.unpack_from('<i', data, offset + n + 4)[0] != n:
            raise ValueError('tracking record marker mismatch')
        records.append(data[offset + 4:offset + n + 4])
        offset += n + 8
    magic, comments, count, version = struct.unpack('<4s3i', records[0])
    shape = struct.unpack('<9i', records[comments + 1])
    if magic != b'$TRK' or version != 1 or shape[:6] != (2, 0, 8, 6, 6, 1):
        raise ValueError('unsupported tracking shape')
    tracks = records[comments + 8:]
    if len(tracks) != count:
        raise ValueError('incomplete track inventory')
    moments = moments_path.read_bytes()
    if len(moments) != 560 or struct.unpack_from('<2i', moments) != (4, 14):
        raise ValueError('unsupported owner export')
    zmu = np.frombuffer(moments, '<f4', 4, 8).astype('f8')
    wzmu = np.frombuffer(moments, '<f4', 4, 24).astype('f8')
    old_volume = np.frombuffer(moments, '<f4', 14, 56).astype('f8')
    if not all(np.isfinite(x).all() and np.all(x > 0) for x in (zmu, wzmu, old_volume)):
        raise ValueError('invalid tracking owner')
    polar = math.fsum(float(z)*float(w) for z, w in zip(zmu, wzmu))
    boundary = math.fsum(map(float, wzmu))
    terms = [[] for _ in range(14)]
    for row in tracks:
        nsub, nseg, weight = struct.unpack_from('<iid', row)
        if nsub != 1 or not 3 <= nseg <= shape[8] or not math.isfinite(weight) or weight <= 0:
            raise ValueError('invalid track header')
        region = np.frombuffer(row, '<i4', nseg, 16 + 4*nsub)
        lengths = np.frombuffer(row, '<f8', nseg, 16 + 4*nsub + 4*nseg)
        if np.any(region[1:-1] < 1) or np.any(region[1:-1] > 8) or not np.isfinite(lengths).all():
            raise ValueError('invalid track segments')
        for r, length in zip(region[1:-1], lengths[1:-1]):
            if length <= 0:
                raise ValueError('nonpositive segment')
            terms[r-1].append(2.0*weight*float(length)*polar)
        for r in (region[0], region[-1]):
            if not -6 <= r <= -1:
                raise ValueError('invalid boundary index')
            terms[8-r-1].append(weight*boundary)
    reconstructed = np.array([math.fsum(t) for t in terms])
    if np.any(reconstructed <= 0):
        raise ValueError('missing region or boundary')
    old_defect = np.abs(reconstructed/old_volume-1)
    if np.max(old_defect) > 2e-6:
        raise ValueError('reconstructed geometry drift')
    result = dict(classification='TRACKING_MOMENTS_DIAGNOSTIC', tracks=count,
        original_polar_moment=polar, original_boundary_weight=boundary,
        reconstructed_volume_and_boundary=reconstructed.tolist(),
        maximum_legacy_normalization_defect=float(np.max(old_defect)),
        legacy_normalization_defects=old_defect.tolist(),
        track_sha256=hashlib.sha256(data).hexdigest(),
        owner_export_sha256=hashlib.sha256(moments).hexdigest(),
        snapshot_qualified=False, production_qualified=False)
    if volume64_path is not None:
        saved = volume64_path.read_bytes()
        if len(saved) != 116 or struct.unpack_from('<i', saved)[0] != 14:
            raise ValueError('invalid binary64 normalization export')
        actual = np.frombuffer(saved, '<f8', 14, 4)
        if not np.isfinite(actual).all() or np.any(actual <= 0):
            raise ValueError('invalid binary64 normalization values')
        defect = float(np.max(np.abs(actual/reconstructed-1)))
        if defect > 2e-12:
            raise ValueError('binary64 owner differs from independent track replay')
        result.update(classification='BINARY64_TRACK_NORMALIZATION_VERIFIED',
            maximum_binary64_replay_defect=defect,
            binary64_normalization_sha256=hashlib.sha256(saved).hexdigest())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('track', type=Path)
    parser.add_argument('moments', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--volume64', type=Path)
    args = parser.parse_args()
    result = analyze(args.track, args.moments, args.volume64)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
