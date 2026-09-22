#!/usr/bin/env python3
"""Short exact synthetic tests of the read-only radial projection algebra."""
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("executable")
    args = parser.parse_args()
    result = subprocess.run([args.executable, "--self-test"], timeout=10,
                            check=True, capture_output=True, text=True)
    rows = [line.split() for line in result.stdout.splitlines() if line.startswith("SYNTHETIC ")]
    expected = {
        1: [0.0, 1.0, 9.5, 4.5],   # non-unit/non-diagonal Gram, known W-orthogonal component
        2: [0.0, 1.0, 5.0, 0.0],   # exactly in span
        3: [0.0, 8.0, 608.0, 288.0],  # amplitude x8, squared norms x64
        4: [0.0, 0.0, 0.0, 0.0],   # zero norm remains zero; no denominator floor
    }
    assert len(rows) == 4, result.stdout
    for row in rows:
        case = int(row[1])
        assert [float(value) for value in row[2:]] == expected[case], row
    # The chosen dyadic inputs make every expected coefficient/squared norm
    # exact in binary64; no synthetic tolerance or physical threshold is used.
    singular = subprocess.run([args.executable, "--singular-test"], timeout=10,
                              capture_output=True, text=True)
    assert singular.returncode != 0 and "singular Gram matrix" in singular.stdout
    missing = subprocess.run([args.executable], timeout=10, capture_output=True, text=True)
    assert missing.returncode != 0 and "expected SHORT_SOURCE_DIRECTORY" in missing.stdout
    nonpositive = subprocess.run([args.executable, "/nonexistent", "0", "/unused"], timeout=10,
                                capture_output=True, text=True)
    assert nonpositive.returncode != 0 and "epoch must be a positive integer" in nonpositive.stdout
    print("7 SYNTHETIC CHECKS OK: non-unit Gram/offspace, in-span, scaling, zero, singular, missing input, nonpositive epoch")


if __name__ == "__main__":
    main()
