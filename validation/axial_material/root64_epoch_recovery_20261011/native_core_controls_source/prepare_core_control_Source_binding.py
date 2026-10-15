#!/usr/bin/env python3
"""Current full-EOF Source/compiled-dependency inventory; never launches Fortran."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
HERE = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011/native_core_controls_source'
SOURCE = HERE / 'test_current_ROOT64_native_core.f90'
BOOT_REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
COMPILE_OUT = ROOT / 'validation/artifacts/axial-material-new-ROOT64-BOOT-compile-only-20261011'
BUILD = COMPILE_OUT / 'build'
PLANNED_OUT = ROOT / 'validation/artifacts/axial-material-new-ROOT64-native-core-controls-20261011'
COMPILER = Path('/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15')
GANLIB = ROOT / 'Ganlib/lib/Darwin_arm64/libGanlib.a'
FLAGS = ['-O2', '-march=native', '-ffp-contract=off', '-fcheck=all', '-fbacktrace', '-g',
         '-fPIC', '-frecord-marker=4', '-ffixed-line-length-none']
EXPECTED_SOURCE = {
    ROOT / 'src/SPOR64_VERIFY.f90': '19b1e8653cfa26efe465d9ec7aee6955f38de32f3343757c476a486b40e25173',
    ROOT / 'src/SPOR64_RCONTRACT.f90': '8463fa31e5d96e6764dc1fd4884342e22cbe778ed9af89f59cc12d8012d4c5d6',
    BOOT_REC / 'new_source/SPOR64_BOOT64.f90': 'cd19000790003d84645ea323ffa95766ba1478230c9c703d32b05b555f1425a7',
    BOOT_REC / 'new_source/SPOBOOT64.f90': '2c30871cdd4455061dca80df25431d6c375453ea910e6ec882f530d1f032b2f8',
}


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    path = Path(path)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or path.is_symlink():
        raise ValueError(('ordinary input required', str(path)))
    expected = identity(before)
    with path.open('rb') as handle:
        if identity(os.fstat(handle.fileno())) != expected:
            raise ValueError(('opened seven identity changed', str(path)))
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
        if identity(os.fstat(handle.fileno())) != expected:
            raise ValueError(('EOF seven identity changed', str(path)))
    if identity(path.lstat()) != expected:
        raise ValueError(('after seven identity changed', str(path)))
    return dict(path=str(path), sha256=digest, size_bytes=expected[4], identity=expected)


def write(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())


def case_names(text, array):
    segment = text.split(':: ' + array + '(', 1)[1].split(']', 1)[0]
    return re.findall(r"'([^']*)'", segment)


def main():
    if PLANNED_OUT.exists() or PLANNED_OUT.is_symlink():
        raise ValueError('future output must remain fresh; author does not create it')
    source_pin = pin(SOURCE)
    text = SOURCE.read_text()
    checks = []

    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        if not value:
            raise ValueError(('Source-only structural check failed', name))

    check('all free-form lines within original default 132 columns',
          all(len(line) <= 132 for line in text.splitlines()))
    pubs, reads = case_names(text, 'PUB_NAMES'), case_names(text, 'READ_NAMES')
    check('28 unique planned publish refusal labels', len(pubs) == len(set(pubs)) == 28)
    check('48 unique planned read/import refusal labels', len(reads) == len(set(reads)) == 48)
    check('83 planned case rows represented in complete-count assertion',
          'completed==3+NPUB+NREAD+3+1' in text)
    check('real original publish/read/import calls present', all(
        'call ' + name in text for name in ('SPOR64_BOOT64_PUBLISH_NATIVE',
                                           'SPOR64_BOOT64_READ_NATIVE',
                                           'SPOR64_BOOT64_IMPORT_NATIVE')))
    check('no fake wrapper definitions replace genuine tested calls', all(
        not re.search(r'^\s*(?:subroutine|function)\s+' + name + r'\b', text, re.I | re.M)
        for name in ('SPOR64_BOOT64_PUBLISH_NATIVE', 'SPOR64_BOOT64_READ_NATIVE',
                     'SPOR64_BOOT64_IMPORT_NATIVE')))
    check('whole 370 groups and explicit group-370 mutation source',
          'NG=370' in text and 'do group=1,NG' in text and 'f%image(:,NG)' in text)
    check('non-REAL32 low bits and signed zero actual fixture source',
          '2.0_real64**(-40)' in text and "z'8000000000000000'" in text)
    check('read refusal has no committed allocatable output',
          '.not. allocated(result)' in text and 'intent(out)' not in text.split(
              'subroutine read_import_refusal', 1)[1].split('end subroutine', 1)[0].split('type(fixture)', 1)[0])
    check('import refusal checks actual empty output', 'EMPTY_MEMORY_ROOT(out)' in text)
    check('independent full-tree raw word atomicity oracle',
          'recursive logical function compare_node' in text and
          'compare_words=all(words1==words2)' in text)
    check('coherent all-copy rewrite correctly expects internal acceptance',
          "call insist(rs==ROOT64_LOADED,'coherent internal rewrite" in text)
    check('no process launch calls in synthetic control program',
          not re.search(r'\b(?:execute_command_line|system|spawn)\s*\(', text, re.I))
    # GANLIB LCMPTC takes carr(1:leng), so every literal must contain the requested width.
    char_calls = re.findall(r"call LCMPTC\([^\n]*?,\s*'(?:[^']*)',\s*(\d+),\s*'([^']*)'\)", text)
    check('all literal GANLIB character payloads have sufficient storage',
          bool(char_calls) and all(len(value) >= int(length) for length, value in char_calls))
    starts = re.findall(r'^  (?:recursive )?(?:logical |real\(real(?:32|64)\) )?(?:function|subroutine) (\w+)', text, re.M)
    ends = re.findall(r'^  end (?:function|subroutine) (\w+)', text, re.M)
    check('subprogram start/end names agree', starts == ends)
    ast.parse(Path(__file__).read_bytes())
    check('author binding Python syntax', True)

    frozen_pins = [pin(path) for path in EXPECTED_SOURCE]
    check('all frozen scientific Source bytes remain unchanged', all(
        item['sha256'] == EXPECTED_SOURCE[Path(item['path'])] for item in frozen_pins))
    summary_path = COMPILE_OUT / 'Root_actual_compile_only_summary.json'
    summary_pin = pin(summary_path)
    summary = json.loads(summary_path.read_text())
    check('original four compile summary genuinely closed0 scope only',
          summary['schema'] == 'ACTUAL_NEW_ROOT64_FOUR_COMPILE_ONLY_V1' and
          summary['status'] == 'FOUR_COMPILE_STEPS_CLOSED0_ONLY' and
          summary['failure'] is None and len(summary['records']) == 4 and
          all(stage['status'] == 'PASS' for stage in summary['records']) and
          summary['original_seventeen_controls_executed'] is False)
    compiled_expected = {item['path']: item for item in summary['output_pins']}
    names = ['SPOR64_VERIFY.o', 'SPOR64_RCONTRACT.o', 'SPOR64_BOOT64.o',
             'spor64_verify.mod', 'spor64_rcontract.mod', 'spor64_boot64.mod']
    compiled_pins = [pin(BUILD / name) for name in names]
    check('current 3 objects and 3 interface modules match actual compile full pins',
          all(item == compiled_expected[item['path']] for item in compiled_pins))
    compiler_pin = pin(COMPILER)
    check('same originally pinned compiler bytes', compiler_pin['sha256'] ==
          '0784ca5eb133cde6a2112eddb4000eb36c9d60eae1b18df1c1ba52fe97737492')
    library_pin = pin(GANLIB)
    old_binding = ROOT / 'validation/artifacts/axial-material-ROOT64-connected-typed-fixture-original-guard-20261011/Root_fixed_source_and_exact_command_binding.json'
    original_inputs = {item['path']: item['sha256'] for item in json.loads(old_binding.read_text())['fixed']}
    check('same original GANLIB static library bytes',
          library_pin['sha256'] == original_inputs[str(GANLIB)])
    includes = [BUILD, ROOT / 'Ganlib/lib/Darwin_arm64/modules']
    module_paths = sorted((ROOT / 'Ganlib/lib/Darwin_arm64/modules').glob('*.mod'))
    interface_pins = [pin(path) for path in module_paths]
    check('GANLIB current complete interface namespace is nonempty', bool(interface_pins))
    check('GANLIB original interface byte pins where original binding includes them', all(
        item['sha256'] == original_inputs[item['path']]
        for item in interface_pins if item['path'] in original_inputs))
    dependency_pins = [compiler_pin, library_pin, summary_pin, *compiled_pins, *interface_pins]
    future_build = PLANNED_OUT / 'build'
    future_object = future_build / 'test_current_ROOT64_native_core.o'
    future_program = future_build / 'current_root64_native_core_controls'
    compile_command = [str(COMPILER), *FLAGS, *['-I' + str(path) for path in includes],
                       '-J' + str(future_build), '-c', str(SOURCE), '-o', str(future_object)]
    link_command = [str(COMPILER), '-O2', '-ffp-contract=off', str(future_object),
                    str(BUILD / 'SPOR64_BOOT64.o'), str(BUILD / 'SPOR64_RCONTRACT.o'),
                    str(BUILD / 'SPOR64_VERIFY.o'), str(GANLIB), '-o', str(future_program)]
    for item in [source_pin, *frozen_pins, *dependency_pins]:
        if pin(item['path']) != item:
            raise ValueError(('input changed at Source-only close', item['path']))
    plan = dict(
        schema='CURRENT_ROOT64_NATIVE_CORE_CONTROL_SOURCE_ONLY_BINDING_V1',
        status='SOURCE_ONLY_CURRENT_DEPENDENCIES_PINNED_NOT_COMPILED_OR_RUN',
        source_only=True, actual_control_Source_pin=source_pin,
        actual_author_Source_pin=pin(Path(__file__).resolve()),
        actual_frozen_scientific_Source_pins=frozen_pins,
        actual_current_full_EOF_dependency_pins=dependency_pins,
        compiled_module_dependency_scope='Only actual new four-step compile outputs; no control/science qualification inherited',
        original_binding_is_historical_byte_reference_only=True,
        Source_structural_checks=checks,
        planned_output_root=str(PLANNED_OUT), planned_compile_command=compile_command,
        planned_link_command=link_command, planned_run_command=[str(future_program)],
        planned_original_caps=dict(whole_wall_seconds=1800, stage_wall_seconds=600,
                                  own_child_RSS_MiB=512, SELF_RSS_MiB=512,
                                  active_children=1, numerical_threads=1, retries=0,
                                  joint_fresh_output_bytes=2*2**30, history_bytes=96*2**30,
                                  free_floor_bytes=8*2**30, cold_reserve_bytes=20971764748,
                                  metadata_headroom_bytes=64*2**20),
        expected_control_count=83, expected_explicit_publish_calls=32,
        expected_explicit_read_calls=52, expected_explicit_import_calls=55,
        expected_refused_publish_cases=pubs, expected_refused_read_import_cases=reads,
        expected_positive_cases=['positive_full_370_plane_' + str(i) for i in range(1, 4)],
        expected_output_atomicity_cases=['import_occupied_output', 'import_output_aliases_flux',
                                        'import_empty_daughter_not_root'],
        expected_core_acceptance_scope_case='scope_coherent_rewrite_needs_host_SHA',
        synthetic_fixture=True,
        fixture_dimensions=dict(energy_groups=370, regions=2, unknowns=3, materials=2,
                                surface_unknowns=1, macro_anisotropy=3, fission_components=32),
        scope='Real GANLIB current core contract and raw-word atomicity controls; no REDGET/SPOBOOT64 entry parser or transport',
        unexecuted_pending=['GLOBAL/source/epoch lifecycle controls',
                            'independent external SHA/7ID refusal of coherent all-copy edits',
                            'SPOBOOT64 seven-entry parser execution',
                            'actual strict REAL64 terminal producer wiring',
                            'complete original seventeen current controls',
                            'complete native build and solve', 'online BOOT', 'AAA/ABA science'],
        actual_Fortran_parser_or_compiler_validation=False,
        actual_native_core_controls_executed=False,
        original_seventeen_controls_qualified=False, native_producer_qualified=False,
        complete_native_build_qualified=False, online_BOOT_qualified=False,
        transport_executed=False, AAA_qualified=False, ABA_admitted=False, goal_complete=False)
    output = HERE / 'CURRENT_NATIVE_CORE_CONTROL_SOURCE_BINDING.json'
    write(output, plan)
    print(json.dumps(dict(status=plan['status'], Source=source_pin,
                          binding_pin=pin(output), Source_structural_checks=len(checks),
                          expected_control_count=83, actual_controls_executed=False), ensure_ascii=False))


if __name__ == '__main__':
    main()
