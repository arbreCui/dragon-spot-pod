"""Reject fabricated or incomplete serialized normalization authorities."""
import argparse
import json
from pathlib import Path
import struct
import tempfile

from analyze_r64_tracking_moments import analyze


def check(track, moments, volume64):
    positive = analyze(track, moments, volume64)
    payload = volume64.read_bytes()
    wrong = bytearray(payload)
    struct.pack_into('<d', wrong, 4, struct.unpack_from('<d', wrong, 4)[0] * 1.01)
    nonfinite = bytearray(payload)
    struct.pack_into('<d', nonfinite, 4, float('nan'))
    cases = {'wrong_volume': bytes(wrong), 'nonfinite_volume': bytes(nonfinite),
             'truncated_volume': payload[:-8]}
    results = {}
    with tempfile.TemporaryDirectory(prefix='spot-v64-rejection-', dir='/private/tmp') as temporary:
        for name, data in cases.items():
            path = Path(temporary) / (name + '.bin')
            path.write_bytes(data)
            try:
                analyze(track, moments, path)
            except ValueError as error:
                results[name] = dict(rejected=True, reason=str(error))
            else:
                raise AssertionError(name + ' falsely accepted')
        corrupt_track = Path(temporary) / 'wrong_track.bin'
        altered = bytearray(track.read_bytes())
        altered[4:8] = b'FAKE'
        corrupt_track.write_bytes(altered)
        try:
            analyze(corrupt_track, moments, volume64)
        except ValueError as error:
            results['wrong_track_identity'] = dict(rejected=True, reason=str(error))
        else:
            raise AssertionError('wrong track falsely accepted')
    return dict(classification='NORMALIZATION_AUTHORITY_NEGATIVE_CONTROLS_PASS',
        actual_binary64_positive_control=positive['classification'],
        authority_sha256=positive['binary64_normalization_sha256'], controls=results,
        snapshot_qualified=False, production_qualified=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('track', type=Path)
    parser.add_argument('moments', type=Path)
    parser.add_argument('volume64', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = check(args.track, args.moments, args.volume64)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
