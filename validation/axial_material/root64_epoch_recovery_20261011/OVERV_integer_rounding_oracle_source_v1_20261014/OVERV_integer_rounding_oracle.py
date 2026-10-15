"""Integer IEEE rounding model for the original LIBDEN OVERV fallback.

This models a current control; it cannot recover historical RAM or libm bits.
No Python floating-point operation participates in the arithmetic model.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import struct
from fractions import Fraction

FORMATS = {32: (23, 127), 64: (52, 1023)}
FALSE = dict(physics_qualified=False, historical_machine_bit_replay=False,
             original_XSM_memory_bits_verified=False,
             historical_native_RAM_bits_verified=False)


def require(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def power_two(exponent):
    return Fraction(1 << exponent, 1) if exponent >= 0 else Fraction(1, 1 << -exponent)


def floor_log2(value):
    require(value > 0, 'positive exact rational logarithm')
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    if value < power_two(exponent):
        exponent -= 1
    require(power_two(exponent) <= value < power_two(exponent + 1), 'exact exponent interval')
    return exponent


def finite_value(bits, width):
    fraction_bits, bias = FORMATS[width]
    require(type(bits) is int and 0 <= bits < (1 << width), 'unsigned IEEE word')
    exponent_bits = width - fraction_bits - 1
    exponent = (bits >> fraction_bits) & ((1 << exponent_bits) - 1)
    fraction = bits & ((1 << fraction_bits) - 1)
    require(exponent != (1 << exponent_bits) - 1, 'finite current control operand')
    significand = fraction if exponent == 0 else (1 << fraction_bits) + fraction
    unbiased = 1 - bias if exponent == 0 else exponent - bias
    result = Fraction(significand) * power_two(unbiased - fraction_bits)
    return -result if bits >> (width - 1) else result


def pack_rounded(significand, exponent, width):
    fraction_bits, bias = FORMATS[width]
    require(type(significand) is int and significand >= 0, 'rounded positive significand')
    if significand == 0:
        return 0
    if significand >= 1 << (fraction_bits + 1):
        require(significand == 1 << (fraction_bits + 1), 'only rounding carry')
        significand >>= 1
        exponent += 1
    if exponent > bias:
        return ((1 << (width - fraction_bits - 1)) - 1) << fraction_bits
    if significand < 1 << fraction_bits:
        require(exponent == 1 - bias, 'subnormal exponent')
        return significand
    require(1 - bias <= exponent <= bias, 'normal finite exponent')
    return ((exponent + bias) << fraction_bits) | (significand - (1 << fraction_bits))


def round_rational(value, width):
    """Round an exact rational to nearest, ties to an even IEEE significand."""
    require(type(value) is Fraction, 'exact rational input')
    if value == 0:
        return 0
    negative = value < 0
    value = abs(value)
    fraction_bits, bias = FORMATS[width]
    exponent = max(floor_log2(value), 1 - bias)
    scaled = value / power_two(exponent - fraction_bits)
    lower, remainder = divmod(scaled.numerator, scaled.denominator)
    twice = remainder * 2
    rounded = lower + int(twice > scaled.denominator or
                          (twice == scaled.denominator and lower % 2 == 1))
    result = pack_rounded(rounded, exponent, width)
    return result | ((1 << (width - 1)) if negative else 0)


def round_square_root(value, width):
    """Round sqrt(rational) by integer comparisons with exact squared midpoints."""
    require(type(value) is Fraction and value >= 0, 'nonnegative exact square-root input')
    if value == 0:
        return 0
    fraction_bits, bias = FORMATS[width]
    exponent = max(floor_log2(value) // 2, 1 - bias)
    scaled_square = value / power_two(2 * (exponent - fraction_bits))
    numerator, denominator = scaled_square.numerator, scaled_square.denominator
    lower = math.isqrt(numerator // denominator)
    require(lower * lower * denominator <= numerator <
            (lower + 1) * (lower + 1) * denominator, 'exact square-root floor')
    midpoint_left = 4 * numerator
    midpoint_right = denominator * (2 * lower + 1) ** 2
    rounded = lower + int(midpoint_left > midpoint_right or
                          (midpoint_left == midpoint_right and lower % 2 == 1))
    return pack_rounded(rounded, exponent, width)


def binary_operation(left, right, width, division=False):
    left = finite_value(left, width)
    right = finite_value(right, width)
    require(not division or right != 0, 'nonzero current control denominator')
    return round_rational(left / right if division else left * right, width)


def original_overv_model(energy_bytes):
    require(type(energy_bytes) is bytes and len(energy_bytes) == 1484, 'exact 371 REAL32 words')
    energy = list(struct.unpack('<371I', energy_bytes))
    require(all(finite_value(word, 32) >= 0 for word in energy), 'finite nonnegative energy controls')
    evj = round_rational(Fraction('1.60217653e-19'), 64)
    nmass = round_rational(Fraction('1.67492728e-27'), 64)
    two_d4 = round_rational(Fraction(20000), 64)
    sqfmas_argument = binary_operation(binary_operation(two_d4, evj, 64), nmass, 64, True)
    sqfmas = round_square_root(finite_value(sqfmas_argument, 64), 64)
    # Original LIBDEN assignment: IF(GA1(NGROUP+1).EQ.0.0) GA1(...)=1.0E-5.
    if finite_value(energy[370], 32) == 0:
        energy[370] = round_rational(Fraction('1e-5'), 32)
    one64 = round_rational(Fraction(1), 64)
    rows = [dict(EVJ64_hex=f'{evj:016X}', NMASS64_hex=f'{nmass:016X}',
                 SQFMAS64_hex=f'{sqfmas:016X}')]
    for group in range(370):
        product = binary_operation(energy[group], energy[group + 1], 32)
        eneavg = round_square_root(finite_value(product, 32), 32)
        second_sqrt = round_square_root(finite_value(eneavg, 32), 32)
        promoted = round_rational(finite_value(second_sqrt, 32), 64)
        denominator = binary_operation(promoted, sqfmas, 64)
        znu = binary_operation(one64, denominator, 64, True)
        gar = round_rational(finite_value(znu, 64), 32)
        rows.append(dict(group=group + 1, OVERV32_hex=[f'{gar:08X}'] * 8))
    rows.append(dict(control_scope='ORIGINAL_OVERV_FALLBACK_ONLY', **FALSE))
    return rows


def self_check():
    # Midpoint expectations are written independently of the rounding procedures.
    require(round_rational(Fraction(1), 32) == 0x3F800000, 'binary32 one')
    require(round_rational(Fraction(1) + Fraction(1, 1 << 24), 32) == 0x3F800000,
            'even lower binary32 tie')
    require(round_rational(Fraction(1) + Fraction(3, 1 << 24), 32) == 0x3F800002,
            'even upper binary32 tie')
    require(round_rational(Fraction(1) + Fraction(1, 1 << 53), 64) == 0x3FF0000000000000,
            'even lower binary64 tie')
    require(round_rational(power_two(-150), 32) == 0, 'zero subnormal midpoint tie')
    require(round_rational(3 * power_two(-150), 32) == 2, 'upper subnormal midpoint tie')
    require(round_square_root(Fraction(4), 32) == 0x40000000, 'exact square-root32')
    require(round_square_root(Fraction(4), 64) == 0x4000000000000000, 'exact square-root64')
    for width, word in [(32, 0x3F800000), (32, 0x3F800001),
                        (64, 0x3FF0000000000000), (64, 0x3FF0000000000001)]:
        midpoint = (finite_value(word, width) + finite_value(word + 1, width)) / 2
        require(round_square_root(midpoint * midpoint, width) == word + (word & 1),
                'exact squared square-root midpoint tie')
    return dict(status='INTEGER_ROUNDING_MODEL_SOURCE_BOUNDARY_SELFCHECK_ONLY',
                actual_energy_read=False, compiler_executed=False, numerical_executed=False,
                **FALSE)


def identity(status):
    return [status.st_dev, status.st_ino, status.st_mode, status.st_nlink,
            status.st_size, status.st_mtime_ns, status.st_ctime_ns]


def bound_energy(expected):
    require(type(expected) is dict and set(expected) == {'path', 'sha256', 'size_bytes', 'identity'},
            'explicit complete ENERGY fullPF')
    path = Path(expected['path'])
    require(path.is_absolute() and '..' not in path.parts and
            not any(p.is_symlink() for p in (path, *path.parents)), 'ordinary absolute input')
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_uid == os.getuid()
            and identity(before) == expected['identity'] and expected['size_bytes'] == 1484,
            'bound owned ENERGY identity/size')
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
        require(identity(os.fstat(stream.fileno())) == identity(before), 'opened ENERGY7')
        raw = stream.read(1485)
        require(identity(os.fstat(stream.fileno())) == identity(before), 'after ENERGY EOF7')
    require(identity(path.lstat()) == identity(before) and len(raw) == 1484 and
            hashlib.sha256(raw).hexdigest() == expected['sha256'], 'actual ENERGY SHA/EOF7')
    return raw


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--selfcheck', action='store_true')
    parser.add_argument('--energy-pin')
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.selfcheck:
        require(args.energy_pin is None and args.output is None, 'selfcheck never reads actual inputs')
        print(json.dumps(self_check(), allow_nan=False), flush=True)
        return
    require(args.energy_pin is not None and args.output is not None, 'two explicit current control arguments')
    expected = json.loads(args.energy_pin)
    rows = original_overv_model(bound_energy(expected))
    output = Path(args.output)
    require(output.is_absolute() and '..' not in output.parts and
            not any(p.is_symlink() for p in (output, *output.parents)), 'ordinary new output')
    with os.fdopen(os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600), 'w') as stream:
        for row in rows:
            stream.write(json.dumps(row, separators=(',', ':'), allow_nan=False) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    folder = os.open(output.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(folder)
    finally:
        os.close(folder)
    print(json.dumps(dict(status='CURRENT_ORIGINAL_OVERV_INTEGER_MODEL_WRITTEN_ONLY',
                          actual_energy_pin=expected, original_fields=370 * 8, **FALSE)), flush=True)


if __name__ == '__main__':
    main()
