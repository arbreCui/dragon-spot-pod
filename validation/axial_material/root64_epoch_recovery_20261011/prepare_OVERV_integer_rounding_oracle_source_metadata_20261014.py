"""Freeze only the integer oracle Source and its original arithmetic lineage."""
import ast
import hashlib
import json
import os
from pathlib import Path
import stat

REC = Path(__file__).absolute().parent
BASE = REC / 'OVERV_integer_rounding_oracle_source_v1_20261014'
ORIGINAL = REC / 'OVERV_original_mixed_precision_independent_control_source_v1_20261014'


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = path.lstat()
    assert path.is_absolute() and not any(p.is_symlink() for p in (path, *path.parents))
    assert stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and before.st_size < 2 ** 20
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
        assert identity(os.fstat(stream.fileno())) == identity(before)
        data = stream.read()
        assert identity(os.fstat(stream.fileno())) == identity(before)
    assert identity(path.lstat()) == identity(before)
    return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
                size_bytes=len(data), identity=identity(before))


def write(path, value):
    with path.open('xb') as stream:
        stream.write((json.dumps(value, indent=2, allow_nan=False) + '\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    return pin(path)


def main():
    oracle = BASE / 'OVERV_integer_rounding_oracle.py'
    source = oracle.read_text()
    ast.parse(source)
    binding_pin = pin(ORIGINAL / 'COMPLETE_ORIGINAL_OVERV_ARITHMETIC_STATEMENT_SOURCE_BINDING.json')
    binding = json.loads(Path(binding_pin['path']).read_bytes())
    oldplan_pin = pin(ORIGINAL / 'ORIGINAL_OVERV_INDEPENDENT_CONTROL_SOURCE_PLAN.json')
    oldplan = json.loads(Path(oldplan_pin['path']).read_bytes())
    control_pin = pin(ORIGINAL / 'OVERV_original_mixed_precision_control.f')
    assert control_pin == binding['control_Source_pin'] == oldplan['control_Source_pin']
    assert binding['each_original_arithmetic_statement_once_in_control'] is True
    assert binding['original_material_Source_not_modified'] is True
    for word in ('SQFMAS=SQRT(2.0D4*EVJ/NMASS)', 'ENEAVG=SQRT(GA1(LLL)*GA1(LLL+1))',
                 'ZNU=1.0/(SQRT(ENEAVG)*SQFMAS)', 'GAR(IBM,1)=REAL(ZNU)'):
        assert Path(control_pin['path']).read_text().count(word) == 1
    false = dict(business_executed=False, compiler_executed=False, numerical_executed=False,
                 files_deleted=False, physics_qualified=False, historical_machine_bit_replay=False)
    plan = dict(schema='OVERV_EXACT_INTEGER_ROUNDING_ORACLE_SOURCE_ONLY_PLAN_V1', source_only=True,
                oracle_Source_pin=pin(oracle), Source_author_pin=pin(__file__),
                original_arithmetic_statement_binding_pin=binding_pin,
                original_control_Source_plan_pin=oldplan_pin, original_control_Source_pin=control_pin,
                current_original_compile_flags=oldplan['original_selected_compile_flags'],
                exact_arithmetic_sequence=[
                    'EVJ and NMASS original decimal constants rounded to binary64',
                    'binary64 multiply 2.0D4*EVJ; binary64 divide by NMASS; binary64 square root',
                    'original last-zero ENERGY assignment to binary32 1.0E-5',
                    'binary32 ENERGY product; binary32 square root assigned ENEAVG',
                    'binary32 square root ENEAVG; exact promotion to binary64',
                    'binary64 multiply by SQFMAS; binary64 reciprocal; binary32 REAL conversion',
                    'original eight identical mixture entries for each of 370 groups'],
                arithmetic_implementation='Fraction integer ratios and isqrt squared-midpoint comparisons; RN-even',
                Python_float_or_libm_sqrt_used=False,
                model_domain='finite nonnegative ENERGY operands and finite nonzero reciprocal denominator',
                unsupported_nonfinite_or_zero_denominator_is_error_not_qualification=True,
                oracle_argv=['python', '-B', str(oracle), '--energy-pin', '<actual complete JSON fullPF>',
                             '--output', '<fresh bounded owning output>'],
                selfcheck_argv=['python', '-B', str(oracle), '--selfcheck'],
                oracle_stdout_and_file_rows_match_original_control_constants_and_group_shapes=True,
                future_actual371_ENERGY_pin=None, future_actual_control_compile_return=None,
                future_actual_control_link_return=None, future_actual_control_run_return=None,
                future_actual_integer_oracle_result_pin=None,
                future_current_control_word_comparison_pin=None,
                SOURCE_CONTEXT_NOT_SAVED_issue_removed=False,
                no_existing_historical_runtime_or_machine_bit_replay_proof_claimed=True, **false)
    plan_pin = write(BASE / 'OVERV_EXACT_INTEGER_ROUNDING_ORACLE_SOURCE_ONLY_PLAN.json', plan)
    ready = dict(schema='OVERV_EXACT_INTEGER_ROUNDING_ORACLE_SOURCE_ONLY_READY_V1', source_only=True,
                 status='SOURCE_ONLY_READY_FOR_GENUINE_GUARDED_CONTROL_AND_INDEPENDENT_REVIEW',
                 plan_pin=plan_pin, oracle_Source_pin=pin(oracle), Source_author_pin=pin(__file__),
                 original_control_Source_pin=control_pin, original_arithmetic_statement_binding_pin=binding_pin,
                 actual_input_pin=None, actual_control_result_pin=None, **false)
    ready_pin = write(BASE / 'SOURCE_ONLY_READY.json', ready)
    fd = os.open(BASE, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    print(json.dumps(dict(status=ready['status'], ready_pin=ready_pin, plan_pin=plan_pin,
                          oracle_Source_pin=ready['oracle_Source_pin'], **false), allow_nan=False), flush=True)


if __name__ == '__main__':
    main()
