#!/usr/bin/env python3
"""Save one source-only byte repair and current dependencies; execute no build."""
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import time

ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
REC = ROOT / 'validation/axial_material/root64_epoch_recovery_20261011'
OLD = REC / 'native_case_route_source_v1'
OUT = Path(__file__).resolve().parent
BUILT = ART / 'axial-material-new-REAL64-native-route-build-only-20261011'
FUTURE = ART / 'axial-material-new-REAL64-native-route-repair-build-only-20261012-v2'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def identity(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
            s.st_mtime_ns, s.st_ctime_ns]


def pin(path):
    p = Path(path)
    before = identity(p.lstat())
    if not stat.S_ISREG(before[2]):
        raise ValueError('regular file required: ' + str(p))
    with p.open('rb') as stream:
        if identity(os.fstat(stream.fileno())) != before:
            raise ValueError('opened identity differs: ' + str(p))
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
        if identity(os.fstat(stream.fileno())) != before:
            raise ValueError('full EOF identity differs: ' + str(p))
    if identity(p.lstat()) != before:
        raise ValueError('after identity differs: ' + str(p))
    return dict(path=str(p), size_bytes=before[4], sha256=digest, identity=before)


def write_bytes(path, data):
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def write_json(path, data):
    write_bytes(path, (json.dumps(data, ensure_ascii=False, indent=2,
                                 allow_nan=False) + '\n').encode())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    start = time.monotonic()
    signal.alarm(600)
    if any(os.environ.get(k) != '1' for k in THREADS):
        raise ValueError('one-thread source writer required')
    if set(p.name for p in OUT.iterdir()) != {Path(__file__).name}:
        raise ValueError('fresh v2 source namespace required; no overwrite or retry')
    if FUTURE.exists() or FUTURE.is_symlink():
        raise ValueError('future build namespace is already occupied')
    binding_path = BUILT / 'Root_current_compile_only_binding.json'
    summary_path = BUILT / 'Root_actual_build_only_summary.json'
    binding = json.loads(binding_path.read_bytes())
    summary = json.loads(summary_path.read_bytes())
    if (summary['status'] != 'FIFTEEN_SOURCE_COMPILES_AND_DRAGON_LINK_CLOSED0_ONLY'
            or summary['failure'] is not None or summary['Dragon_linked'] is not True
            or summary['transport_executed'] is not False
            or len(summary['records']) != 16
            or binding['fixed_current_pins'] != summary['fixed_current_pins']):
        raise ValueError('actual closed compile/link receipt differs')
    commands = binding['actual_commands']
    if len(commands) != 16:
        raise ValueError('fifteen compiles and one full link required')
    original = OLD / 'AXNCASE64.f90'
    object_old = BUILT / 'build/AXNCASE64.o'
    chosen = [c for c in commands[:-1] if str(original) in c]
    if len(chosen) != 1 or chosen[0][-2:] != ['-o', str(object_old)]:
        raise ValueError('actual AXNCASE command uniqueness/output differs')
    expected_rows = summary['fixed_current_pins'] + summary['output_pins']
    expected_by_path = {}
    for row in expected_rows:
        prior = expected_by_path.get(row['path'])
        if prior is not None and prior != row:
            raise ValueError('conflicting retained pins')
        expected_by_path[row['path']] = row
    extra = [binding_path, summary_path, ROOT / 'Ganlib/src/LCMTLC.f90',
             ROOT / 'src/SPOR64_VERIFY.f90', Path(__file__).resolve()]
    current = [pin(p) for p in dict.fromkeys([*expected_by_path, *map(str, extra)])]
    by_path = {p['path']: p for p in current}
    for path, row in expected_by_path.items():
        if any(by_path[path][k] != row[k] for k in ('size_bytes', 'sha256')):
            raise ValueError('retained input bytes differ: ' + path)
    identity_differences = [dict(path=p, historical_identity=row['identity'],
        current_identity=by_path[p]['identity']) for p, row in expected_by_path.items()
        if by_path[p]['identity'] != row['identity']]
    before = original.read_bytes()
    old = b"  call LCMPTC(kentry(2),'SIGNATURE',12,'L_BOOTBIND ')\n"
    new = b"  call LCMPTC(kentry(2),'SIGNATURE',12,'L_BOOTBIND  ')\n"
    if (before.count(old) != 1 or len(b'L_BOOTBIND ') != 11
            or len(b'L_BOOTBIND  ') != 12
            or digest(before) != 'baeb38c4a49e78a53fb8dfc3edd2070c639c8adcda7f07ecc8b64972ae192d13'):
        raise ValueError('exact reviewed original Source anchor differs')
    position = before.index(old)
    insertion = position + old.index(b"')\n")
    after = before[:insertion] + b' ' + before[insertion:]
    if (after != before.replace(old, new, 1)
            or after[:insertion] + after[insertion+1:] != before):
        raise ValueError('complete forward/inverse bytes differ')
    library = (ROOT / 'Ganlib/src/LCMTLC.f90').read_bytes()
    if b"   read(carr(1:leng),fmt) (ibase(j),j=1,n)\n" not in library:
        raise ValueError('actual reviewed GANLIB substring implementation differs')
    write_bytes(OUT / 'ORIGINAL_COMPLETE_AXNCASE64_V1.f90', before)
    write_bytes(OUT / 'AXNCASE64.f90', after)
    proof = dict(schema='AXNCASE64_ONE_BYTE_EXACT_PADDING_REPAIR_V2',
        original=by_path[str(original)], corrected=pin(OUT/'AXNCASE64.f90'),
        original_complete_copy=pin(OUT/'ORIGINAL_COMPLETE_AXNCASE64_V1.f90'),
        changes=1, inserted_bytes_hex='20', zero_based_byte_offset=insertion,
        line_number=before[:insertion].count(b'\n')+1,
        original_full_line=old.decode(), corrected_full_line=new.decode(),
        original_character_count=11, corrected_character_count=12,
        requested_character_count=12, complete_forward_exact=True,
        complete_inverse_exact=True, all_other_bytes_exact=True,
        symbols_ABI_controls_physical_inputs_unchanged=True,
        reviewed_GANLIB_source=by_path[str(ROOT/'Ganlib/src/LCMTLC.f90')],
        cause='LCMPTC_S0 reads carr(1:leng) with assumed-length carr; 12 exceeds literal length 11.',
        observed_runtime_failure=False, compile_executed=False, transport_executed=False)
    write_json(OUT/'AXNCASE64_EXACT_WHOLE_BYTE_FORWARD_INVERSE_PROOF.json', proof)
    compile_command = [str(OUT/'AXNCASE64.f90') if p == str(original)
                       else str(FUTURE/'build/AXNCASE64.o') if p == str(object_old)
                       else '-J'+str(FUTURE/'build') if p == '-J'+str(BUILT/'build')
                       else p for p in chosen[0]]
    original_link = commands[-1]
    if original_link.count(str(object_old)) != 1:
        raise ValueError('exactly one old AXNCASE link object required')
    link_command = [str(FUTURE/'build/AXNCASE64.o') if p == str(object_old)
                    else str(FUTURE/'runtime/Dragon') if p == str(BUILT/'runtime/Dragon')
                    else p for p in original_link]
    if link_command[:-2].count(str(FUTURE/'build/AXNCASE64.o')) != 1:
        raise ValueError('one repaired object must be linked')
    reused = link_command[3:-2]
    reused = [p for p in reused if p != str(FUTURE/'build/AXNCASE64.o')]
    if any(p not in by_path for p in reused):
        raise ValueError('complete link inputs lack current full pins')
    plan = dict(schema='SOURCE_ONLY_EXACT_AXNCASE_RECOMPILE_AND_FULL_RELINK_PLAN_V2',
        plan_only=True, commands_executed=False, working_directory=str(FUTURE/'build'),
        fresh_output_root=str(FUTURE), actual_prior_binding=by_path[str(binding_path)],
        actual_prior_summary=by_path[str(summary_path)], original_compile_command=chosen[0],
        compile_command=compile_command, original_complete_link_command=original_link,
        complete_link_command=link_command, original_compile_flags=binding['original_flags'],
        reused_ordered_link_input_pins=[by_path[p] for p in reused],
        replaced_object_current_pin=by_path[str(object_old)],
        original_Dragon_current_pin=by_path[str(BUILT/'runtime/Dragon')],
        unchanged_dispatcher_source_current_pin=by_path[str(OLD/'KDRDRV.F')],
        unchanged_deck_current_pin=by_path[str(OLD/'ROOT64_NEW_WARM_A_20261011.x2m')],
        guardian='Reuse original SUPPORT/load/helper.modules()/guard_admission and genuine OwnRSSSerialExecutor; no replacement supervisor.',
        execution_caps=dict(stage_seconds=600, whole_seconds=1800, sampled_child_RSS_MiB=512,
            SELF_RSS_MiB=512, threads=1, numeric_children_at_once=1, retries=0,
            complete_history_bytes=96*2**30, fresh_output_bytes=2*2**30,
            disk_min_free_bytes=8*2**30, original_cold_reserve_bytes=20971764748),
        required_host_actions=['Verify all current bindings before and after each stage.',
            'Create fresh output/build/runtime/ROOT64_COMPILE_ONLY; copy only original bounded runner.',
            'Compile only the repaired AXNCASE64; then perform the complete ordered Dragon link.',
            'Retain actual complete streams, process exits, original watchdog checks and output fullEOF/7ID pins.',
            'No transport, BOOT, controls, training or scientific qualification follows these two build steps.'],
        no_large_history_copy=True, full_source_archive_build_qualified=False)
    write_json(OUT/'EXACT_PLANNED_RECOMPILE_AND_COMPLETE_LINK_COMMANDS.json', plan)
    for row in current:
        if pin(row['path']) != row:
            raise ValueError('protected current input changed before close: '+row['path'])
    manifest = dict(schema='CURRENT_COMPLETE_ROUTE_REPAIR_DEPENDENCY_IDENTITY_BINDING_V2',
        source_only=True, current_full_EOF_pins=current,
        actual_prior_fixed_rows=len(summary['fixed_current_pins']),
        actual_prior_output_rows=len(summary['output_pins']),
        current_unique_files=len(current), prior_recorded_unique_files=len(expected_by_path),
        all_retained_input_and_output_SHA_and_sizes_exact=True,
        historical_identity_difference_count=len(identity_differences),
        historical_identity_differences=identity_differences,
        current_7ID_measured_not_inherited=True, full_EOF_before_and_after_unchanged=True,
        whole_writer_wall_seconds=time.monotonic()-start,
        SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        original_v1_and_src_unmodified=True, objects_rebuilt=False, Dragon_relinked=False,
        native_execution=False, scientific_qualification=False)
    write_json(OUT/'CURRENT_COMPLETE_DEPENDENCY_IDENTITY_BINDING.json', manifest)
    text = '''AXNCASE64 signature padding repair — Source only\n\nConfirmed source defect: the retained v1 literal L_BOOTBIND plus one blank is 11 characters, while LCMPTC requests 12. The reviewed GANLIB LCMPTC_S0 reads carr(1:leng) without padding or a length guard; this substring exceeds the supplied literal. No runtime failure was observed by this source review.\n\nThe new complete AXNCASE64 inserts exactly one blank at line 46. Names, ABI, case, thresholds, caps, materials, formulas, dispatcher and deck remain byte identical. The complete original is retained and the forward/inverse proof checks every byte. No original or frozen v1 file was changed.\n\nThe full current input and saved-output SHA/size/7ID binding is recorded separately, including historical identity differences without claiming inherited identity qualification. Existing objects and opaque archive inputs can be reused only after Root validates this current binding. The plan recompiles one object and repeats the complete ordered link into a fresh output; it does not execute either command. The original 512 MiB / 600 s stage / 1800 s whole / one-thread / one-child / no-retry supervisor and storage reserves remain required. No large history directory is copied.\n\nNo new compile, transport, native BOOT, original 17 controls, training, AAA, ABA or physics qualification is asserted.\n'''
    write_bytes(OUT/'FINAL_SOURCE_ONLY_REPAIR_AND_BUILD_PLAN.txt', text.encode())
    if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss >= 512*2**20:
        raise ValueError('source writer SELF exceeds original RSS cap')
    signal.alarm(0)
    print(json.dumps(dict(status='COMPLETE_SOURCE_ONLY_ONE_BYTE_REPAIR_AND_CURRENT_BINDING',
        corrected_source=pin(OUT/'AXNCASE64.f90'), proof=pin(OUT/'AXNCASE64_EXACT_WHOLE_BYTE_FORWARD_INVERSE_PROOF.json'),
        binding=pin(OUT/'CURRENT_COMPLETE_DEPENDENCY_IDENTITY_BINDING.json'),
        plan=pin(OUT/'EXACT_PLANNED_RECOMPILE_AND_COMPLETE_LINK_COMMANDS.json'),
        current_unique_files=len(current), historical_identity_difference_count=len(identity_differences),
        wall_seconds=time.monotonic()-start, SELF_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        compile_executed=False, transport_executed=False)))


if __name__ == '__main__':
    main()
