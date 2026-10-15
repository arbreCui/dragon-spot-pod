"""One bounded read-only audit of actual production source-factor activity.

No transport, solve, replay, compilation or import-time file I/O is performed.
All 370 groups and all compressed SCAT01/02 entries are retained, including
signed zeros and signed coefficients. Saved final FLUX64 operands are only
diagnostics: they are never claimed to reproduce the internal slot-7 iterate.
The compiled sender selector is separately bound; TRACK metadata or NFUNL is
not substituted for actual sender NLF. Root alone records actual tool exit0.
"""
import argparse
from array import array
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import shutil
import struct
import sys
import time
import zlib

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
SOURCE = ART / 'axial-material-source-factor-activity-admission-20261006'
OUT = ART / 'axial-material-source-factor-activity-20261006'
TERMINAL = ART / 'axial-material-source-factor-activity-terminal-20261006'
OLD = ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
NEW = ART / 'axial-material-production-qualified-AB-source-factor-20261006'
CAPTURE = ART / 'axial-material-AAA-production-angular-capture-20261006'
BUILD = ART / 'axial-material-source-factor-build-20261006'
CE = ART / 'axial-material-qualified-AAA-source-factor-reference-20261006'
FULL = ART / 'axial-material-AAA-white-trace-refined-layered-full-20261005'
CAUSAL = ART / 'axial-material-AAA-white-trace-refined-layered-propagation-causal-20261005'
CE_FACTORY = ROOT / 'validation/axial_material/prepare_qualified_AAA_source_factor_reference_analysis.py'
BUILD_FACTORY = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
FULL_FACTORY = ROOT / 'validation/axial_material/qualify_refined_AAA_layered_full.py'
REVIEW = ROOT / 'validation/axial_material/production_moment_order_binary_review.json'
ORIGINAL_SPEC = ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005/case_spec.json'
ORIGINAL_ADDENDUM = ORIGINAL_SPEC.parent / 'resource_addendum.json'
ORIGINAL_SPEC_SHA = '8c2297533ff582e81cef6430947a0557e921830304673a6a8a6c0149fd7a33ae'
ORIGINAL_ADDENDUM_SHA = 'b68ca3ee2802b69900c5085757898872a220de4f038ab9cd14cb4287b9c5fd15'
INDEPENDENT_JOBS_NOTE = 'Existing material/native jobs retain their separate already-declared supervisors and caps.'
READER = OLD / 'runtime/snapshot_control_preflight.py'
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python')
PYTHON_SHA = 'ba725dca52e02b5382d6acf3e6ac92afb0d65662f1ce8820d75a59a095490860'
CE_FACTORY_SHA = '0fc9a674ff7579f8adaa21618cbb3aead028d2e216e7946964c5df90a1b39a99'
BUILD_FACTORY_SHA = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
FULL_FACTORY_SHA = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
BUILD_SEAL = '2a005852d49e4929e05b6835d5b8a51f9ce68afb6f15fc665fb5e7bd7547ed1e'
CAPTURE_SEAL = '16f67ec74e41d3282a7e90fe342e0165c81a8fb97a6cfc1cd72615e6a9ac9c0a'
CE_SEAL = '49b927dc3628d5a998373152adbdb7897b695c4f8479c20801c8fe86596daa89'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
NG, NR, NZ, NL, NUN = 370, 8, 48, 3, 1800
STAGE_WALL, TOTAL_WALL, RSS_CAP, RESERVE = 60, 120, 512, 16 * 2**20
REVIEW_SCHEMA = 'AXMAT_PRODUCTION_COMPILED_ANGULAR_SELECTOR_REVIEW_V1'
REVIEW_SHA = '86a1556f5759bb9475ca0cc40b31cd50031fee78f23eb684cb5dd3dc1730c41a'
TERMINAL_SCHEMA = 'AXMAT_SOURCEFACTOR_ACTIVITY_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
TAIL_FIELDS = ('full_closeout_tail_gate', 'actual_elapsed_through_full_closeout_seconds',
               'actual_complete_archive_bytes', 'resources_after_full_closeout')
RAW_STORAGE_RECIPE = 'Original-byte SHA256 content address; one zlib(level1) stream per unique original record, indexed by compressed offset/stored length and original length/SHA; every owner record is readback-decompressed and byte/SHA checked before finite/sign gates.'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(path, wanted=None):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts or path.is_symlink() or not path.is_file():
        raise ValueError('absolute regular non-symlink dependency required: ' + str(path))
    if wanted is not None and digest(path) != wanted:
        raise ValueError('declared dependency changed: ' + str(path))
    return path


def pin(path):
    path = require(Path(path).resolve())
    return dict(path=str(path), sha256=digest(path))


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def write_table(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, separators=(',', ':'), allow_nan=False)
        stream.write('\n')


def verify(files):
    for path, wanted in files.items():
        require(path, wanted)


def review_references(files):
    """Only the two documented TRACK aliases may reference bootstrap bytes."""
    allowed = {root / 'AAA/map012/initial_axial_track.xsm': root / 'AAA/bootstrap/initial_axial_track.xsm'
        for root in (OLD, NEW)}
    originals, links = {}, []
    for name, wanted in files.items():
        path = Path(name)
        if path.is_symlink():
            target = allowed.get(path)
            if target is None or os.readlink(path) != str(target) or path.resolve(strict=True) != target:
                raise ValueError('compiled-selector evidence contains an undeclared scientific input alias')
            require(target, wanted)
            links.append(dict(path=str(path), literal_target=os.readlink(path), target=pin(target)))
            originals[str(target)] = wanted
        else:
            require(path, wanted); originals[str(path)] = wanted
    if {item['path'] for item in links} != {str(path) for path in allowed}:
        raise ValueError('both actual documented old/new TRACK aliases must remain bound')
    return originals, links


def load(path, name):
    path = require(path).resolve()
    if name in sys.modules:
        obj = sys.modules[name]
        if Path(obj.__file__).resolve() != path:
            raise ValueError('actual imported dependency path differs')
        return obj
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    sys.modules[name] = obj
    spec.loader.exec_module(obj)
    if Path(obj.__file__).resolve() != path:
        raise ValueError('import identity changed')
    return obj


def environment(expected=None):
    require(PYTHON.resolve(), PYTHON_SHA)
    if (Path(sys.executable).resolve() != PYTHON.resolve() or sys.version_info[:2] != (3, 12)
            or any(os.environ.get(key) != '1' for key in THREADS)):
        raise ValueError('pinned Python3.12 and exactly one thread required')
    loader = {key: os.environ.get(key) for key in ('PYTHONPATH', 'DYLD_LIBRARY_PATH',
        'DYLD_INSERT_LIBRARIES', 'LD_LIBRARY_PATH')}
    current = dict(python_version=platform.python_version(), executable=pin(PYTHON.resolve()),
        invocation=str(PYTHON), byteorder=sys.byteorder, loader_environment=loader,
        thread_environment={key: os.environ[key] for key in THREADS})
    if current['byteorder'] != 'little' or (expected is not None and current != expected):
        raise ValueError('actual interpreter/loader/reader execution environment differs')
    return current


def seal_admission(root, expected=None):
    seal_path = require(root / 'seal.json', expected)
    seal = read(seal_path)
    verify({str(root / name): sha for name, sha in seal['files'].items()})
    regular = {str(path.relative_to(root)) for path in root.rglob('*') if path.is_file() and not path.is_symlink()}
    if regular != set(seal['files']) | {'seal.json'}:
        raise ValueError('sealed family namespace changed: ' + str(root))
    return pin(seal_path)


def compiled_selector(path, wanted):
    if Path(path) != REVIEW or wanted != REVIEW_SHA:
        raise ValueError('the independently completed compiled-selector review identity is required')
    evidence = read(require(path, wanted))
    if (evidence['schema'] != REVIEW_SCHEMA
            or evidence['compiled_SPOT_selector'] != dict(NLF_state_index=9, NANI_state_index=10, NANI_transform='MAX(1,STATE)', NANIS_clamped_to_NANI_minus_one=False)
            or evidence['current_source_SPOT_selector'] != dict(NLF_state_index=15, NANI_state_index=16, NANI_transform='MAX(1,STATE)', NANIS_clamped_to_NANI_minus_one=True)
            or evidence['actual_sender_NLF_is_TRACK_state9'] is not True or evidence['NFUNL_is_not_NLF'] is not True):
        raise ValueError('actual compiled sender selector review required; no current-text fallback')
    review_references(evidence['files'])
    for path in (NEW / 'runtime/Dragon', ROOT / 'lib/Darwin_arm64/libDragon.a', ROOT / 'src/FLU.o', ROOT / 'src/FLU.f'):
        if evidence['files'].get(str(path)) != digest(require(path)):
            raise ValueError('compiled selector review does not bind the actual runtime/library/object/source')
    return evidence


def modules():
    sys.path.insert(0, str(NEW / 'runtime'))
    c = load(NEW / 'runtime/production_runner.py', 'production_runner')
    ce = load(require(CE_FACTORY, CE_FACTORY_SHA), 'source_factor_activity_guard_provenance')
    full = load(require(FULL_FACTORY, FULL_FACTORY_SHA), 'source_factor_activity_guard')
    builder = load(require(BUILD_FACTORY, BUILD_FACTORY_SHA), 'source_factor_activity_build')
    info = c.verify_prepared(NEW / 'prepared.json', digest(NEW / 'prepared.json'))
    provenance = ce.live_guard_provenance(full, c, info)
    controls = builder.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,):
        raise ValueError('actual own-child supervisor base differs')
    return c, full, provenance, controls


def source_plan():
    owners, files = {}, {}
    for label, root in (('old', OLD), ('new', NEW)):
        for stage in ('bootstrap', 'map001', 'map012'):
            result_path = root / 'AAA' / stage / 'result.json'
            result = read(require(result_path))
            files[str(result_path)] = digest(result_path)
            names = ('initial_axial_macrolib.xsm', 'initial_axial_track.xsm') if stage == 'bootstrap' else ('candidate_axial.xsm', 'closed_axial.xsm')
            for name in names:
                path = require(root / 'AAA' / stage / name, result['sha256'][name])
                owners[label + '/' + stage + '/' + name] = pin(path)
                files[str(path)] = digest(path)
        for path in (root / 'prepared.json', root / 'declaration.json', root / 'AAA/run_status.json',
                     root / 'runtime/Dragon', root / 'runtime/production_runner.py'):
            files[str(path)] = digest(require(path))
    capture = read(require(CAPTURE / 'seal.json', CAPTURE_SEAL))
    capture_inputs = {}
    for name in ['angular_capture_events.bin', *[f'angular_source_g{g:03d}.bin' for g in range(1, NG + 1)]]:
        path = CAPTURE / 'AAA' / name
        require(path, capture['files']['AAA/' + name])
        capture_inputs[name] = pin(path)
        files[str(path)] = digest(path)
    return owners, capture_inputs, files


def raw_codec():
    return dict(name='zlib', level=1, wrapper='zlib', compiled_version=zlib.ZLIB_VERSION,
        runtime_version=zlib.ZLIB_RUNTIME_VERSION, implementation=pin(Path(zlib.__file__).resolve()))


def archive_plan(owners, captures):
    """Exact byte-compression forecast plus unchanged conservative table bounds.

    This preflight never decodes floating words or applies scientific gates.
    Only integer record metadata and the original byte payloads are inspected.
    """
    reader = load(READER, 'source_factor_activity_planning_reader')
    stored_bytes = 0; original_bytes = 0; unique_original_bytes = 0; records = 0; entries = 0; seen_records = set()
    def charge(raw):
        nonlocal stored_bytes, original_bytes, unique_original_bytes, records
        records += 1; original_bytes += len(raw)
        sha = hashlib.sha256(raw).hexdigest()
        if sha not in seen_records:
            seen_records.add(sha); unique_original_bytes += len(raw)
            stored_bytes += len(zlib.compress(raw, level=1))
    for item in captures.values():
        charge(Path(item['path']).read_bytes())
    for owner, item in owners.items():
        if '/bootstrap/' not in owner: continue
        with stream_xsm(item['path'], reader) as a:
            entry = a.root['STATE-VECTOR']; charge(a.read(entry[0], entry[1]))
            if owner.endswith('track.xsm'):
                for name in ('MATCOD', 'KEYFLX', 'KEYFLX$ANIS'):
                    entry = a.root[name]; charge(a.read(entry[0], entry[1]))
            else:
                for group in handles(a, a.root, 'GROUP', NG):
                    directory = a.directory(group[0])
                    for l in (1, 2):
                        for prefix in ('NJJS', 'IJJS', 'IPOS', 'SCAT'):
                            entry = directory.get(prefix + f'{l:02d}')
                            charge(a.read(entry[0], entry[1]) if entry is not None else b'')
                        entry = directory['NJJS' + f'{l:02d}']
                        counts = struct.unpack(f'<{entry[1]}i', a.read(entry[0], entry[1]))
                        if any(value < 0 for value in counts): raise ValueError('negative compressed metadata count')
                        entries += sum(counts)
    # The worker uses the identical original-byte SHA deduplication and codec.
    # Every owner's index, compressed entry and mapping remains present.
    # Final XSM records stay pinned in place; no scientific value is selected.
    unique_finals = {tuple(owners[name]['sha256'] for name in (owner, owner.split('/')[0] + '/bootstrap/initial_axial_macrolib.xsm',
        owner.split('/')[0] + '/bootstrap/initial_axial_track.xsm')) for owner in owners if '/bootstrap/' not in owner}
    parts = dict(raw_records_stored_compressed_bytes=stored_bytes, lossless_compressed_entry_index_bytes=500 * (2 * NG * 2),
        raw_record_index_bytes=512 * records, mapping_table_bytes=350 * (2 * NR * NZ * NL),
        scattering_count_table_bytes=1000 * (2 * NG * 2), capture_count_table_bytes=1000 * NG,
        final_record_and_operand_tables_bytes=1900 * NG * len(unique_finals) + 500 * 8, closeout_and_monitor_bytes=256 * 2**10,
        source_metadata_and_copied_runtime_reserve=2**20)
    bound = sum(parts.values())
    if bound >= RESERVE:
        raise ValueError('complete raw/table metadata reservation exceeds fixed 16 MiB; no partial inventory admitted')
    return dict(parts=parts, total_reserved_bytes=bound, raw_archive_codec=raw_codec(), raw_archive_storage_recipe=RAW_STORAGE_RECIPE,
        original_record_bytes_without_deduplication=original_bytes, unique_original_record_bytes=unique_original_bytes,
        original_byte_identity_deduplication_credit_bytes=original_bytes - unique_original_bytes,
        original_record_count=records, unique_original_record_count=len(seen_records),
        compressed_entries_from_original_NJJS=entries, final_original_bytes_copied=0,
        unique_final_archive_macro_track_identities=len(unique_finals),
        all_original_final_bytes_remain_pinned=True)


def terminal_contract():
    return dict(schema=TERMINAL_SCHEMA, root=str(TERMINAL), receipt=str(TERMINAL / 'terminal_return.json'),
        complete_archive_scope_roots=[str(SOURCE), str(OUT)],
        record_producer='root', evidence_producer_implemented_by_this_factory=False,
        actual_tool_exit_zero_required=True, record_written_after_actual_terminal_return_required=True,
        tail_fields=list(TAIL_FIELDS), actual_run_command=[str(PYTHON), str(Path(__file__).resolve()), 'run', '--sha256', '__DECLARATION_SHA256__'])


def resource_scope_contract():
    """Freeze the original family allocation and separate native input pins."""
    spec = read(require(ORIGINAL_SPEC, ORIGINAL_SPEC_SHA))
    addendum = read(require(ORIGINAL_ADDENDUM, ORIGINAL_ADDENDUM_SHA))
    caps = spec['resource_caps']; original_roots = addendum['resources_before']['resource_roots']
    if (caps['new_case_artifact_budget_GiB'] != 96 or caps['disk_min_free_GiB'] != 8
            or INDEPENDENT_JOBS_NOTE not in caps['notes']
            or spec['conditional_white_trace_trial']['resource_addendum'] != pin(ORIGINAL_ADDENDUM)
            or addendum['prior_storage_budget_GiB'] != 40 or addendum['new_storage_budget_GiB'] != 96
            or addendum['min_free_GiB'] != 8 or not original_roots
            or any(Path(name).parent != ART or not Path(name).name.startswith('axial-material-') for name in original_roots)):
        raise ValueError('original family cap, separate material/native jobs note or declared original scope differs')
    predecessors, explicit_roots, native = [], set(), {}
    for root in (OLD, NEW, BUILD, CAPTURE, CE, FULL, CAUSAL):
        path = require(root / 'declaration.json'); declaration = read(path)
        predecessors.append(pin(path)); explicit_roots.update(declaration['resource_roots'])
        for name, wanted in declaration.get('files', {}).items():
            original = Path(name)
            if not original.is_relative_to(ART) or not original.relative_to(ART).parts[0].startswith('native-'):
                continue
            actual = pin(original)
            if actual['sha256'] != wanted:
                raise ValueError('separately declared immutable native dependency changed: ' + name)
            item = dict(original_path=name, sha256=wanted, actual_file=actual,
                literal_alias_target=os.readlink(original) if original.is_symlink() else None)
            if name in native and native[name] != item:
                raise ValueError('predecessor native dependency pins disagree')
            native[name] = item
    return dict(schema='AXMAT_SOURCEFACTOR_ACTIVITY_ORIGINAL_FAMILY_RESOURCE_SCOPE_V1',
        original_case_spec=pin(ORIGINAL_SPEC), original_resource_addendum=pin(ORIGINAL_ADDENDUM),
        original_case_resource_notes=caps['notes'], original_addendum_resource_roots=original_roots,
        predecessor_declarations=predecessors, inherited_explicit_resource_roots=sorted(explicit_roots),
        artifact_cap_scope='Inherited explicitly declared roots plus every current axial-material-* family root and this new family. No blanket native-/material project root addition.',
        unchanged_family_artifact_cap_bytes=96 * 2**30, unchanged_global_disk_free_floor_bytes=8 * 2**30,
        existing_material_native_jobs_keep_separate_declared_supervisors_and_caps=True,
        readonly_native_dependency_pins=native, readonly_native_dependencies_are_not_new_activity_outputs=True)


def complete_history_scope(roots):
    """Every current axial family is counted; original explicit extras stay."""
    declared = {str(path) for path in roots}
    for path in ART.iterdir():
        if path.is_dir() and path.name.startswith('axial-material-'):
            if path.is_symlink() or str(path) not in declared:
                raise ValueError('current complete-history root was not declared: ' + str(path))


def history_resources(c, roots, min_free, budget):
    class CompleteHistoryResources(c.DiskResources):
        def check(self):
            complete_history_scope(self.roots)
            return super().check()
    return CompleteHistoryResources(ART, roots, min_free, budget)


def declare(evidence_path, evidence_sha):
    if SOURCE.exists() or OUT.exists() or TERMINAL.exists():
        raise ValueError('independent new activity roots must be absent; no overwrite/retry')
    env = environment()
    review = compiled_selector(evidence_path, evidence_sha)
    c, full, provenance, controls = modules()
    owners, captures, files = source_plan()
    review_files, review_links = review_references(review['files']); files.update(review_files)
    planned = archive_plan(owners, captures)
    scope = resource_scope_contract()
    seals = [seal_admission(BUILD, BUILD_SEAL), seal_admission(CAPTURE, CAPTURE_SEAL), seal_admission(CE, CE_SEAL)]
    roots = set(scope['inherited_explicit_resource_roots']) | {str(SOURCE), str(OUT), str(TERMINAL)}
    roots.update(str(path.resolve()) for path in ART.iterdir() if path.is_dir() and path.name.startswith('axial-material-'))
    roots = sorted(roots)
    resources = history_resources(c, roots, 8 * 2**30, 96 * 2**30)
    before = resources.check()
    if before['artifact_bytes'] + RESERVE >= 96 * 2**30 or before['disk_free_bytes'] - RESERVE < 8 * 2**30:
        raise ValueError('complete current history plus activity reserve does not fit')
    for path in [Path(__file__).resolve(), READER, CE_FACTORY, BUILD_FACTORY, FULL_FACTORY, Path(evidence_path),
                 ORIGINAL_SPEC, ORIGINAL_ADDENDUM, *[Path(item['path']) for item in scope['predecessor_declarations']],
                 *[Path(item['path']) for item in seals], *controls,
                 NEW / 'runtime/run_bounded_dragon.py', ROOT / 'src/FLU2DR64.f', ROOT / 'src/FLU.f',
                 ROOT / 'src/FLU.o', ROOT / 'lib/Darwin_arm64/libDragon.a',
                 BUILD / 'build/FLU2DR64.f', BUILD / 'build/FLU2DR64.o', CAPTURE / 'build/FLU2DR64.f']:
        files[str(path)] = digest(require(path))
    for item in scope['readonly_native_dependency_pins'].values():
        files[item['actual_file']['path']] = item['actual_file']['sha256']
    # Bind actual loaded helper and stdlib/native module files, without replacing
    # module.__file__. The worker itself uses only this pinned stdlib reader.
    for obj in list(sys.modules.values()):
        path = getattr(obj, '__file__', None)
        if path and Path(path).resolve().is_file():
            path = Path(path).resolve()
            files[str(path)] = digest(path)
    verify(files)
    SOURCE.mkdir()
    runtime = SOURCE / 'runtime'; runtime.mkdir()
    shutil.copy2(READER, runtime / 'snapshot_control_preflight.py')
    require(runtime / 'snapshot_control_preflight.py', digest(READER))
    shutil.copy2(NEW / 'runtime/run_bounded_dragon.py', runtime / 'run_bounded_dragon.py')
    write_new(SOURCE / 'guard_provenance.json', provenance)
    files.update({str(path): digest(path) for path in SOURCE.rglob('*') if path.is_file()})
    d = dict(schema='AXMAT_SOURCEFACTOR_PRODUCTION_ACTIVITY_DECLARATION_V1', files=files, environment=env,
        owners=owners, capture_inputs=captures, input_seals=seals, compiled_selector_review=pin(evidence_path),
        compiled_selector_actual_reference_links=review_links,
        guard_provenance=pin(SOURCE / 'guard_provenance.json'), reader=pin(runtime / 'snapshot_control_preflight.py'),
        source=pin(Path(__file__).resolve()), resource_roots=roots, resources_before=before,
        resource_scope_contract=scope,
        complete_history_new_root_policy='Refuse undeclared current axial-material-* family roots at admission and every resource poll; preserve all inherited explicit extra roots.',
        archive_plan=planned,
        min_free_bytes=8 * 2**30, artifact_budget_bytes=96 * 2**30, archive_reserve_bytes=RESERVE,
        archive_reserve_roots=[str(SOURCE), str(OUT)],
        stage_wall_seconds=STAGE_WALL, total_wall_seconds=TOTAL_WALL, rss_cap_mib=RSS_CAP,
        threads=1, children_at_once=1, retries=0, groups=list(range(1, NG + 1)), orders=[1, 2],
        actual_external_terminal_return_contract=terminal_contract(), transport_calls=0, linear_solves=0, replays=0,
        final_operand_scope='Saved FLUX64 only; not an exact internal slot-7/source iteration replay.',
        actual_NLF_scope='Only the separately reviewed compiled selector and raw TRACK word9 prove sender NLF; NFUNL3 and TRACK15 do not.',
        AAA_accuracy_qualified=False, ABA_admitted=False)
    write_new(SOURCE / 'declaration.json', d)
    write_new(SOURCE / 'source_inventory.json', dict(files={str(path.relative_to(SOURCE)): digest(path) for path in SOURCE.rglob('*') if path.is_file()}))
    if source_bytes() > planned['parts']['source_metadata_and_copied_runtime_reserve'] or archive_bytes() >= RESERVE:
        raise ValueError('actual complete SOURCE metadata/copies exceed the declared SOURCE+OUT archive reserve')
    print(json.dumps(dict(classification='DECLARED_READ_ONLY_SOURCEFACTOR_ACTIVITY_NOT_RUN', declaration=pin(SOURCE / 'declaration.json'), output=str(OUT))))


def admission(expected):
    d = read(require(SOURCE / 'declaration.json', expected))
    if (d['schema'] != 'AXMAT_SOURCEFACTOR_PRODUCTION_ACTIVITY_DECLARATION_V1'
            or d['source'] != pin(Path(__file__).resolve()) or d['stage_wall_seconds'] != STAGE_WALL
            or d['total_wall_seconds'] != TOTAL_WALL or d['rss_cap_mib'] != RSS_CAP
            or (d['threads'], d['children_at_once'], d['retries']) != (1, 1, 0)
            or (d['transport_calls'], d['linear_solves'], d['replays']) != (0, 0, 0)
            or d['artifact_budget_bytes'] != 96 * 2**30 or d['min_free_bytes'] != 8 * 2**30
            or d['archive_reserve_bytes'] != RESERVE or d['groups'] != list(range(1, NG + 1)) or d['orders'] != [1, 2]
            or d['archive_reserve_roots'] != [str(SOURCE), str(OUT)]
            or d['actual_external_terminal_return_contract'] != terminal_contract()):
        raise ValueError('frozen all-group read-only scope or resources differ')
    inventory = read(SOURCE / 'source_inventory.json')
    if {str(path.relative_to(SOURCE)) for path in SOURCE.rglob('*') if path.is_file()} != set(inventory['files']) | {'source_inventory.json'}:
        raise ValueError('frozen activity source namespace differs')
    verify({str(SOURCE / name): sha for name, sha in inventory['files'].items()})
    verify(d['files']); environment(d['environment'])
    descriptor = d['compiled_selector_review']; review = compiled_selector(descriptor['path'], descriptor['sha256'])
    originals, links = review_references(review['files'])
    if links != d['compiled_selector_actual_reference_links'] or any(d['files'].get(name) != sha for name, sha in originals.items()):
        raise ValueError('actual compiled-selector aliases or underlying byte identities differ')
    if (not {str(SOURCE), str(OUT), str(TERMINAL)}.issubset(d['resource_roots'])
            or d['complete_history_new_root_policy'] != 'Refuse undeclared current axial-material-* family roots at admission and every resource poll; preserve all inherited explicit extra roots.'
            or d['archive_plan']['total_reserved_bytes'] != sum(d['archive_plan']['parts'].values())
            or not 0 <= d['archive_plan']['total_reserved_bytes'] < RESERVE
            or d['archive_plan']['raw_archive_codec'] != raw_codec()
            or d['archive_plan']['raw_archive_storage_recipe'] != RAW_STORAGE_RECIPE
            or d['archive_plan']['parts']['source_metadata_and_copied_runtime_reserve'] != 2**20
            or source_bytes() > d['archive_plan']['parts']['source_metadata_and_copied_runtime_reserve']
            or not 0 <= d['archive_plan']['parts']['raw_records_stored_compressed_bytes'] < RESERVE
            or not 0 < d['archive_plan']['unique_original_record_count'] <= d['archive_plan']['original_record_count']
            or not 0 <= d['archive_plan']['unique_original_record_bytes'] <= d['archive_plan']['original_record_bytes_without_deduplication']
            or d['archive_plan']['original_byte_identity_deduplication_credit_bytes'] != d['archive_plan']['original_record_bytes_without_deduplication'] - d['archive_plan']['unique_original_record_bytes']
            or d['AAA_accuracy_qualified'] is not False or d['ABA_admitted'] is not False):
        raise ValueError('complete reservation or diagnostic-only scope differs')
    scope = resource_scope_contract()
    if (d['resource_scope_contract'] != scope or not set(scope['inherited_explicit_resource_roots']).issubset(d['resource_roots'])
            or any(d['files'].get(item['actual_file']['path']) != item['actual_file']['sha256'] for item in scope['readonly_native_dependency_pins'].values())):
        raise ValueError('original family allocation or separately pinned native dependencies differ')
    complete_history_scope(d['resource_roots'])
    for item in d['input_seals']:
        require(item['path'], item['sha256'])
    return d


@contextmanager
def stream_xsm(path, reader):
    """Frozen _XSM parser, record-sized pread; no resident whole-file mapping."""
    with Path(path).open('rb') as stream:
        before = os.fstat(stream.fileno())
        class Words:
            def __len__(self):
                return before.st_size
            def __getitem__(self, item):
                if not isinstance(item, slice) or item.step not in (None, 1):
                    raise ValueError('unsupported frozen reader byte access')
                first, stop, _ = item.indices(before.st_size)
                raw = os.pread(stream.fileno(), stop - first, first)
                if len(raw) != stop - first:
                    raise ValueError('incomplete original XSM byte read')
                return raw
        yield reader._XSM(Words())
        after = os.fstat(stream.fileno())
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            raise ValueError('immutable scientific input changed during read')


def handles(a, directory, name, count):
    raw = a.record(directory, name, count, 10)
    return [a.directory(offset)['***HANDLE***'] for offset in struct.unpack(f'<{count}i', raw)]


def typed(raw, code):
    result = array(code)
    if result.itemsize != (8 if code == 'd' else 4): raise ValueError('original little-endian word size differs')
    result.frombytes(raw)
    return result


class RawArchive:
    """Original-byte content address, lossless encoding, readback before gates."""
    def __init__(self):
        self.stream = (OUT / 'audit/raw_records.bin').open('x+b')
        self.seen, self.index = {}, {}
        self.all_decompression_checks_passed = True
    def add(self, label, raw, origin):
        sha = hashlib.sha256(raw).hexdigest()
        if sha not in self.seen:
            stored = zlib.compress(raw, level=1)
            if archive_bytes() + len(stored) >= RESERVE:
                raise ValueError('raw input archive exceeds the fixed activity reserve')
            offset = self.stream.tell(); self.stream.write(stored); self.stream.flush()
            self.seen[sha] = dict(offset_bytes=offset, original_length_bytes=len(raw), sha256=sha,
                stored_compressed_length_bytes=len(stored), codec='zlib-level1')
        self.index[label] = dict(self.seen[sha], original=origin)
        descriptor = self.seen[sha]
        try:
            stored = os.pread(self.stream.fileno(), descriptor['stored_compressed_length_bytes'], descriptor['offset_bytes'])
            if len(stored) != descriptor['stored_compressed_length_bytes']:
                raise ValueError('incomplete stored compressed original record')
            decoder = zlib.decompressobj()
            decoded = decoder.decompress(stored, descriptor['original_length_bytes'] + 1)
            if (not decoder.eof or decoder.unused_data or decoder.unconsumed_tail
                    or len(decoded) != descriptor['original_length_bytes'] or decoded != raw
                    or hashlib.sha256(decoded).hexdigest() != sha):
                raise ValueError('original record decompression byte/length/SHA identity failed')
        except BaseException:
            self.all_decompression_checks_passed = False
            raise
        return decoded
    def close(self):
        self.stream.close()
        write_table(OUT / 'audit/raw_record_index.json', dict(schema='AXMAT_SOURCEFACTOR_ACTIVITY_RAW_RECORDS_V2',
            blob=pin(OUT / 'audit/raw_records.bin'), records=self.index, bit_patterns_preserved=True,
            codec=raw_codec(), storage_recipe=RAW_STORAGE_RECIPE, all_decompression_checks_passed=self.all_decompression_checks_passed,
            decode='Read offset_bytes/stored_compressed_length_bytes from blob, zlib-decompress, require original_length_bytes and original sha256 before interpreting any words.'))


def raw_record(a, owner, directory, name, raw, allow_absent=False):
    if name not in directory and allow_absent:
        return raw.add(owner + '/' + name, b'', dict(record=name, present=False))
    entry = directory[name]
    data = a.read(entry[0], entry[1])
    return raw.add(owner + '/' + name, data, dict(record=name, xsm_word_offset=entry[0], length_words=entry[1], type=entry[2]))


def signed_counts(values, width):
    output = dict(positive=0, negative=0, positive_zero=0, negative_zero=0, nonfinite=0)
    for value in values:
        if not math.isfinite(value): key = 'nonfinite'
        elif value == 0: key = 'negative_zero' if math.copysign(1, value) < 0 else 'positive_zero'
        else: key = 'positive' if value > 0 else 'negative'
        output[key] += 1
    output['word_width_bits'] = width
    return output


def capture_events(data):
    offset, sequence, latest = 72, 0, {}
    while offset < len(data):
        if len(data) - offset < 16: raise ValueError('incomplete original source dispatch event')
        dispatch, outer, inner, nactive = struct.unpack('<4i', data[offset:offset + 16]); offset += 16
        if dispatch != sequence + 1 or outer <= 0 or inner <= 0 or not 1 <= nactive <= NG:
            raise ValueError('original chronological source dispatch metadata differs')
        size = 4 * (nactive + NG + 4)
        if offset + size > len(data): raise ValueError('incomplete original NGIND/NPSYS/B2 bytes')
        ngind = struct.unpack(f'<{nactive}i', data[offset:offset + 4 * nactive]); offset += 4 * nactive
        npsys = struct.unpack(f'<{NG}i', data[offset:offset + 4 * NG]); offset += 4 * NG
        b2 = struct.unpack('<4f', data[offset:offset + 16]); offset += 16
        if (len(set(ngind)) != nactive or list(ngind) != [g for g, value in enumerate(npsys, 1) if value]
                or any(not 1 <= g <= NG for g in ngind) or any(not math.isfinite(value) for value in b2) or b2[3] != 0):
            raise ValueError('actual original active source group/B2 mapping differs')
        for g in ngind: latest[g] = (dispatch, outer, inner)
        sequence = dispatch
    if set(latest) != set(range(1, NG + 1)): raise ValueError('original capture must cover all 370 groups')
    return sequence, latest


def mirror_matches(values, raw):
    try:
        return all(struct.pack('<f', value) == raw[j * 4:(j + 1) * 4] for j, value in enumerate(values))
    except OverflowError:
        return False


def worker(expected):
    d = admission(expected)
    claim = read(OUT / 'execution_claim.json')
    stage = read(OUT / 'audit/stages.json')['stages']
    command = [str(PYTHON), str(Path(__file__).resolve()), 'worker', '--sha256', expected]
    if (claim['parent_pid'] != os.getppid() or claim['declaration_sha256'] != expected
            or len(stage) != 1 or stage[0]['status'] != 'RUNNING' or stage[0]['command'] != command):
        raise ValueError('only the actual declared sole own-child activity worker may read scientific records')
    reader = load(d['reader']['path'], 'source_factor_activity_frozen_xsm')
    raw = RawArchive(); tracks, macros, captures, pending_errors = {}, {}, {}, []
    try:
        # Complete original input records are archived before finite/sign gates.
        for owner, item in d['owners'].items():
            if '/bootstrap/' not in owner: continue
            with stream_xsm(item['path'], reader) as a:
                state_raw = raw_record(a, owner, a.root, 'STATE-VECTOR', raw)
                if a.root['STATE-VECTOR'][1:] != (40, 1): raise ValueError('original STATE-VECTOR record type/length differs')
                state = struct.unpack('<40i', state_raw)
                if owner.endswith('track.xsm'):
                    records = {name: raw_record(a, owner, a.root, name, raw) for name in ('MATCOD', 'KEYFLX', 'KEYFLX$ANIS')}
                    if any(a.root[name][2] != 1 for name in records): pending_errors.append('original mapping record type differs')
                    tracks[owner.split('/')[0]] = dict(state=state, mat=typed(records['MATCOD'], 'i'), scalar=typed(records['KEYFLX'], 'i'), keys=typed(records['KEYFLX$ANIS'], 'i'))
                else:
                    groups = handles(a, a.root, 'GROUP', NG); inventory = []
                    for g, entry in enumerate(groups, 1):
                        directory = a.directory(entry[0]); orders = {}
                        for l in (1, 2):
                            names = [prefix + f'{l:02d}' for prefix in ('NJJS', 'IJJS', 'IPOS', 'SCAT')]
                            rows = {name: raw_record(a, owner + f'/g{g:03d}', directory, name, raw,
                                allow_absent=name.startswith('SCAT')) for name in names}
                            if any(directory[name][2] != 1 for name in names[:3]) or (names[3] in directory and directory[names[3]][2] != 2):
                                pending_errors.append('original compressed scattering record type differs')
                            orders[l] = dict(njj=typed(rows[names[0]], 'i'), ijj=typed(rows[names[1]], 'i'), ipos=typed(rows[names[2]], 'i'),
                                scat=typed(rows[names[3]], 'f'), scat_bits=typed(rows[names[3]], 'I'))
                        inventory.append(orders)
                    macros[owner.split('/')[0]] = dict(state=state, groups=inventory)
        for name, item in d['capture_inputs'].items():
            data = Path(item['path']).read_bytes()
            captures[name] = raw.add('capture/' + name, data, item)
    finally:
        raw.close()
    if (not raw.all_decompression_checks_passed or len(raw.index) != d['archive_plan']['original_record_count']
            or len(raw.seen) != d['archive_plan']['unique_original_record_count']
            or sum(row['original_length_bytes'] for row in raw.index.values()) != d['archive_plan']['original_record_bytes_without_deduplication']
            or sum(row['original_length_bytes'] for row in raw.seen.values()) != d['archive_plan']['unique_original_record_bytes']
            or (OUT / 'audit/raw_records.bin').stat().st_size != d['archive_plan']['parts']['raw_records_stored_compressed_bytes']):
        raise ValueError('complete raw compressed archive differs from exact original-byte preflight')
    event = captures.pop('angular_capture_events.bin')
    if event[:8] != b'AXCEV001' or len(event) < 72: raise ValueError('actual original capture event header differs')
    header = struct.unpack('<16i', event[8:72])
    if header[:3] != (NG, NUN, NR * NZ) or header[4:] != (3, 3, 3, 1, 0, 3, 0, 1, 2, 1, 1, 0):
        raise ValueError('actual captured caller contract differs')
    dispatches, latest = capture_events(event)
    review_item = d['compiled_selector_review']; review = compiled_selector(review_item['path'], review_item['sha256'])
    capture_rows = []
    for g in range(1, NG + 1):
        data = captures[f'angular_source_g{g:03d}.bin']
        if data[:8] != b'AXCS2001' or len(data) != 28 + 8 * NUN: raise ValueError('actual capture source record differs')
        context = struct.unpack('<5i', data[8:28]); values = typed(data[28:], 'd')
        if context[0] != g or context[2:] != (3, 1, NUN) or context[1:4] != latest[g]:
            raise ValueError('complete chronological original capture source inventory differs')
        counts = signed_counts(values, 64)
        if counts['nonfinite']: pending_errors.append('nonfinite captured S2')
        capture_rows.append(dict(group=g, actual_context=list(context), signs=counts,
            all_three_source_moment_signs=[signed_counts([values[key - 1] for key in tracks['old']['keys'][l * NR * NZ:(l + 1) * NR * NZ] if key], 64) for l in range(NL)],
            actual_original_S2_not_new_sourcefix_replay=True))
    track_reports, term_reports, mapping, entry_index = {}, [], [], []
    for label in ('old', 'new'):
        track, macro = tracks[label], macros[label]; state = track['state']; nmat = macro['state'][1]
        if (state[0] != NR * NZ or state[1] != NUN or (state[5], state[6]) != (NR, NZ)
                or macro['state'][0] != NG or macro['state'][2] != NL
                or len(track['keys']) != NR * NZ * NL or len(track['scalar']) != NR * NZ or len(track['mat']) != NR * NZ
                or track['keys'][:NR * NZ] != track['scalar']):
            raise ValueError('original macro/track mapping dimensions differ')
        if list(state) != review['actual_TRACK_contract']['state_vector'] or nmat != header[3]:
            raise ValueError('actual raw TRACK and macro do not match the reviewed compiled caller contract')
        nlf, nani = state[8], max(1, state[9]); upper = min(nlf - 1, macro['state'][2] - 1)
        track_reports[label] = dict(raw_STATE_words={str(i): state[i - 1] for i in (9, 10, 15, 16, 27)},
            macro_STATE3=macro['state'][2], actual_compiled_sender_NLF=nlf, actual_compiled_sender_NANI=nani,
            actual_compiled_sender_NANIS=macro['state'][2] - 1, actual_compiled_sender_loop_upper_IAL=upper,
            actual_first_non_scalar_sender_active=header[15] == 0, actual_second_scalar_counterpath_active=header[15] != 0,
            capture_actual_NFUNL=header[4], capture_actual_NANIS=header[12],
            capture_did_not_record_sender_NLF=True, actual_NLF_equals_NFUNL_claimed=False,
            current_text_selector_NLF=state[14], current_text_selector_NANI=max(1, state[15]),
            current_text_selector_loop_upper_IAL=min(state[14] - 1, macro['state'][2] - 1, max(1, state[15]) - 1),
            current_text_is_not_actual_compiled_selector=True)
        reach = {}
        for l in range(NL):
            reach[l] = {}
            for ir in range(NR * NZ):
                key, material = track['keys'][ir + l * NR * NZ], track['mat'][ir]
                if not 0 <= key <= NUN or not 0 <= material <= nmat: raise ValueError('source KEYFLX/material outside original bounds')
                mapping.append(dict(owner=label, IAL=l, IAM=l, IE=1, IR=ir + 1, material=material, IND=key,
                    statically_addressable=key != 0 and material != 0, actual_sender_loop_reachable=l <= upper and key != 0 and material != 0))
                if key and material: reach[l].setdefault(material, []).append(key - 1)
            if l == 0: continue  # Full P0 mapping is retained; coefficient inventory is SCAT01/02.
            for g, orders in enumerate(macro['groups'], 1):
                row = orders[l]
                if any(len(row[name]) != nmat for name in ('njj', 'ijj', 'ipos')): raise ValueError('original compressed scattering metadata length differs')
                original_signs = signed_counts(row['scat'], 32)
                if original_signs['nonfinite']: pending_errors.append('nonfinite full original SCAT record')
                prefix = label + f'/bootstrap/initial_axial_macrolib.xsm/g{g:03d}/'
                entry_index.append(dict(owner=label, destination_group=g, IAL=l,
                    original_raw_labels={name: prefix + name + f'{l:02d}' for name in ('NJJS', 'IJJS', 'IPOS', 'SCAT')}))
                counts = dict(total_entries=0, self_entries=0, intergroup_entries=0, nonzero_intergroup_entries=0,
                    positive_zero_intergroup_entries=0, negative_zero_intergroup_entries=0,
                    negative_intergroup_entries=0, nonfinite_entries=0,
                    statically_addressable_region_operations=0, actual_sender_region_operations=0)
                for m in range(1, nmat + 1):
                    njj, ijj, ipos = row['njj'][m - 1], row['ijj'][m - 1], row['ipos'][m - 1]
                    if njj < 0 or (njj and (ipos < 1 or ipos + njj - 1 > len(row['scat']))): raise ValueError('compressed scattering index interval invalid')
                    for jnd in range(1, njj + 1):
                        jg, index = ijj - jnd + 1, ipos + jnd - 2
                        if not 1 <= jg <= NG: raise ValueError('original scattering source group outside 1..370')
                        value = row['scat'][index]; bits = row['scat_bits'][index]
                        counts['total_entries'] += 1
                        if not math.isfinite(value): counts['nonfinite_entries'] += 1
                        if jg == g: counts['self_entries'] += 1; continue
                        counts['intergroup_entries'] += 1
                        if math.isfinite(value) and value != 0: counts['nonzero_intergroup_entries'] += 1
                        elif value == 0:
                            if bits >> 31: counts['negative_zero_intergroup_entries'] += 1
                            else: counts['positive_zero_intergroup_entries'] += 1
                        if value < 0: counts['negative_intergroup_entries'] += 1
                        if math.isfinite(value) and value != 0:
                            counts['statically_addressable_region_operations'] += len(reach[l].get(m, ()))
                            if l <= upper: counts['actual_sender_region_operations'] += len(reach[l].get(m, ()))
                if counts['nonfinite_entries']: pending_errors.append('nonfinite original SCAT coefficients')
                term_reports.append(dict(owner=label, destination_group=g, IAL=l,
                    full_original_SCAT_record_signs=original_signs, **counts))
    write_table(OUT / 'audit/complete_compressed_scattering_entry_index.json', dict(
        raw_record_archive=pin(OUT / 'audit/raw_record_index.json'), groups=entry_index,
        lossless_decode='First decode each original_raw_label using raw_record_index codec/offset/stored length; zlib-decompress and verify original length/SHA before interpreting words. Then, for every material IBM and JND=1..NJJS[IBM], JG=IJJS[IBM]-JND+1; original coefficient bits=SCAT[(IPOS[IBM]+JND-2)*4:...+4].',
        all_original_entries_retained=True, no_nonzero_or_intergroup_selection=True))
    write_table(OUT / 'audit/complete_KEYFLX_mapping.json', mapping)
    write_table(OUT / 'audit/complete_scattering_counts.json', term_reports)
    write_new(OUT / 'audit/compiled_sender_mapping.json', dict(compiled_selector_review=d['compiled_selector_review'], owners=track_reports,
        compressed_entry_archive=pin(OUT / 'audit/complete_compressed_scattering_entry_index.json'),
        IAL1_2_inventory_is_not_proof_of_actual_sender_activity=True))
    write_table(OUT / 'audit/complete_capture_source_counts.json', dict(actual_header=list(header), groups=capture_rows,
        chronological_dispatches=dispatches, original_events_raw_archived=True, sourcefix_replay=False))
    if (len(term_reports) != 2 * NG * 2 or len(mapping) != 2 * NR * NZ * NL
            or sum(row['total_entries'] for row in term_reports) != d['archive_plan']['compressed_entries_from_original_NJJS']):
        raise ValueError('complete all-owner/group/order/original-entry coverage differs from declared metadata')
    if pending_errors: raise ValueError('; '.join(sorted(set(pending_errors))))
    # Archive per-group original final record hashes and sign/mirror diagnostics;
    # original final XSM bytes remain pinned in place. No final operand is called
    # slot7, and no reconstruction claims the source seen by an actual solve.
    finals, final_cache, final_errors = [], {}, []
    for owner, item in d['owners'].items():
        if '/bootstrap/' in owner: continue
        label = owner.split('/')[0]; macro, track = macros[label], tracks[label]
        cache_key = (item['sha256'], d['owners'][label + '/bootstrap/initial_axial_macrolib.xsm']['sha256'],
            d['owners'][label + '/bootstrap/initial_axial_track.xsm']['sha256'])
        if cache_key in final_cache:
            finals.append(dict(owner=owner, original_archive=item, exact_same_final_macro_track_bytes_as=final_cache[cache_key],
                per_group_and_operand_tables_in_referenced_owner=True, exact_slot7_replay=False))
            continue
        final_cache[cache_key] = owner
        with stream_xsm(item['path'], reader) as a:
            flux32, flux64 = handles(a, a.root, 'FLUX', NG), handles(a, a.root, 'FLUX64', NG)
            keff_raw = a.record(a.root, 'SPOT-KEFF64', 2, 4); keff = struct.unpack('<d', keff_raw)[0]
            k32 = a.record(a.root, 'K-EFFECTIVE', 1, 2)
            if not math.isfinite(keff) or keff <= 0 or struct.pack('<f', keff) != k32: raise ValueError('actual final keff mirror failed')
            operands, rows = {}, []
            for g, (single, double) in enumerate(zip(flux32, flux64, strict=True), 1):
                if single[1:] != (NUN, 2) or double[1:] != (2 * NUN, 4): raise ValueError('actual final FLUX/FLUX64 record shape differs')
                f32, f64 = a.read(single[0], single[1]), a.read(double[0], double[1]); values = typed(f64, 'd')
                signs = signed_counts(values, 64)
                mirror = mirror_matches(values, f32)
                if signs['nonfinite'] or not mirror: final_errors.append('actual final finite/mirror gate failed')
                operands[g] = values
                rows.append(dict(group=g, FLUX_sha256=hashlib.sha256(f32).hexdigest(), FLUX64_sha256=hashlib.sha256(f64).hexdigest(),
                    all_unknown_signs=signs, REAL32_mirror_byte_exact=mirror,
                    scalar_coordinate_signs=signed_counts([values[key - 1] for key in track['scalar'] if key], 64),
                    moment_signs=[signed_counts([values[key - 1] for key in track['keys'][l * NR * NZ:(l + 1) * NR * NZ] if key], 64) for l in range(NL)]))
            diagnostics = []
            for l in (1, 2):
                for g, orders in enumerate(macro['groups'], 1):
                    row = orders[l]; nonzero_products, zero_products, nonfinite_products = 0, 0, 0
                    positive_products, negative_products, negative_zero_products = 0, 0, 0
                    for ir, material in enumerate(track['mat']):
                        key = track['keys'][ir + l * NR * NZ]
                        if not material or not key: continue
                        for jnd in range(1, row['njj'][material - 1] + 1):
                            jg = row['ijj'][material - 1] - jnd + 1
                            if jg == g: continue
                            value = row['scat'][row['ipos'][material - 1] + jnd - 2] * operands[jg][key - 1]
                            if not math.isfinite(value): nonfinite_products += 1
                            elif value == 0:
                                zero_products += 1
                                if math.copysign(1, value) < 0: negative_zero_products += 1
                            else:
                                nonzero_products += 1
                                if value > 0: positive_products += 1
                                else: negative_products += 1
                    if nonfinite_products: final_errors.append('nonfinite saved-final-operand diagnostic product')
                    diagnostics.append(dict(destination_group=g, IAL=l, nonzero_saved_final_operand_products=nonzero_products,
                        zero_saved_final_operand_products=zero_products, nonfinite_saved_final_operand_products=nonfinite_products,
                        positive_products=positive_products, negative_products=negative_products, negative_zero_products=negative_zero_products,
                        exact_slot7_replay=False))
            finals.append(dict(owner=owner, original_archive=item, keff64_hex=keff.hex(), keff64_raw_sha256=hashlib.sha256(keff_raw).hexdigest(),
                groups=rows, saved_final_operand_diagnostics=diagnostics, exact_slot7_replay=False))
            del operands
    write_table(OUT / 'audit/final_saved_operand_diagnostics.json', dict(owners=finals, diagnostic_only=True, transport_calls=0, linear_solves=0, replays=0))
    if final_errors: raise ValueError('; '.join(sorted(set(final_errors))))
    actual_operations = sum(row['actual_sender_region_operations'] for row in term_reports)
    findings = dict(classification='COMPLETE_READ_ONLY_SOURCEFACTOR_ACTIVITY_DIAGNOSTIC_ONLY', groups=NG, orders=[1, 2],
        source_record_inventory_complete=True, raw_input_bits_retained_before_finite_gate=True,
        original_mapping_rows=len(mapping), compressed_entries=sum(row['total_entries'] for row in term_reports),
        intergroup_entries=sum(row['intergroup_entries'] for row in term_reports), actual_sender_high_order_region_operations=actual_operations,
        complete_compiled_sender_metadata=track_reports, final_operand_scope=d['final_operand_scope'],
        transport_calls=0, linear_solves=0, replays=0, AAA_accuracy_qualified=False, ABA_admitted=False)
    write_new(OUT / 'audit/findings.json', findings)
    admission(expected)
    print(json.dumps(findings))


def watch(stage):
    path = OUT / 'audit/activity.watchdog.json'; w = read(require(path))
    if (stage['status'] != 'PASS' or w['returncode'] != 0 or w['limit_failure'] is not None
            or w['command'] != stage['command'] or not 0 < w['wall_cap_seconds'] <= stage['wall_cap_seconds'] <= STAGE_WALL
            or not 0 <= w['elapsed_seconds'] < w['wall_cap_seconds'] or not 0 <= w['sampled_peak_rss_mib'] < RSS_CAP
            or w['rss_cap_mib'] != RSS_CAP or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True):
        raise ValueError('actual sole read-only child supervision failed')
    require(OUT / 'audit/activity.log', stage['log_sha256'])
    return pin(path)


def source_bytes():
    return sum(path.stat().st_size for path in SOURCE.rglob('*') if path.is_file() and not path.is_symlink())


def archive_bytes():
    """Complete new SOURCE+OUT regular bytes, including manifests and closeout."""
    return source_bytes() + sum(path.stat().st_size for path in OUT.rglob('*') if path.is_file() and not path.is_symlink())


def run(expected):
    started = time.monotonic(); d = admission(expected)
    if OUT.exists(): raise ValueError('one actual activity attempt only; no retry')
    c, full, provenance, _ = modules()
    if provenance != read(d['guard_provenance']['path']): raise ValueError('actual tested supervisor provenance changed')
    resources = history_resources(c, d['resource_roots'], d['min_free_bytes'], d['artifact_budget_bytes'])
    before = resources.check()
    if before['artifact_bytes'] + RESERVE >= d['artifact_budget_bytes'] or before['disk_free_bytes'] - RESERVE < d['min_free_bytes']:
        raise ValueError('actual remaining whole-history activity reservation no longer fits')
    OUT.mkdir(); (OUT / 'runtime').mkdir(); (OUT / 'audit').mkdir()
    shutil.copy2(SOURCE / 'runtime/run_bounded_dragon.py', OUT / 'runtime/run_bounded_dragon.py')
    write_new(OUT / 'execution_claim.json', dict(parent_pid=os.getpid(), declaration_sha256=expected, source=d['source'], started_unix=time.time(), retries=0))
    remaining = TOTAL_WALL - (time.monotonic() - started)
    result = dict(classification='READ_ONLY_SOURCEFACTOR_ACTIVITY_FAILED_NO_RETRY', declaration_sha256=expected,
        source=d['source'], completed_commands=0, error=None, transport_calls=0, linear_solves=0, replays=0,
        archive_scope_roots=d['archive_reserve_roots'],
        AAA_accuracy_qualified=False, ABA_admitted=False,
        elapsed_seconds_scope='Entire run admission and child through pre-closeout; actual full closeout tail measured after result/seal publication.')
    failed = None
    try:
        if remaining <= 0: raise ValueError('whole activity wall budget exhausted before sole child launch')
        runner = full.OwnRSSSerialExecutor(OUT, remaining, 'audit', resources)
        command = [str(PYTHON), str(Path(__file__).resolve()), 'worker', '--sha256', expected]
        runner.execute(OUT / 'audit', 'activity', command, STAGE_WALL)
        stages = read(OUT / 'audit/stages.json')['stages']
        if len(stages) != 1 or stages[0]['label'] != 'audit/activity' or stages[0]['command'] != command:
            raise ValueError('exactly one complete declared activity child required')
        monitor = watch(stages[0]); findings = read(OUT / 'audit/findings.json')
        if findings['classification'] != 'COMPLETE_READ_ONLY_SOURCEFACTOR_ACTIVITY_DIAGNOSTIC_ONLY' or findings['groups'] != NG:
            raise ValueError('complete original all-group diagnostic not present')
        result.update(classification='COMPLETE_READ_ONLY_SOURCEFACTOR_ACTIVITY_DIAGNOSTIC_ONLY', completed_commands=1,
            findings=pin(OUT / 'audit/findings.json'), actual_child_watchdog=monitor)
    except BaseException as error:
        failed = error; result['error'] = repr(error)
    finally:
        try:
            admission(expected); resources.check()
            elapsed = time.monotonic() - started
            if elapsed >= TOTAL_WALL or archive_bytes() >= RESERVE: raise ValueError('read-only activity pre-closeout resources failed')
            result.update(elapsed_seconds=elapsed, actual_archive_bytes_before_closeout=archive_bytes())
        except BaseException as error:
            failed = error; result.update(classification='READ_ONLY_SOURCEFACTOR_ACTIVITY_FAILED_NO_RETRY', error=repr(error))
        try:
            write_new(OUT / 'result.json', result)
            write_new(OUT / 'seal.json', dict(schema='AXMAT_SOURCEFACTOR_ACTIVITY_SEAL_V1',
                files={str(path.relative_to(OUT)): digest(path) for path in OUT.rglob('*') if path.is_file() and not path.is_symlink()}))
            snapshot = resources.check(); size = archive_bytes(); elapsed = time.monotonic() - started
            if elapsed >= TOTAL_WALL or size >= RESERVE: raise ValueError('read-only activity full closeout resources failed')
            result.update(full_closeout_tail_gate='PASS', actual_elapsed_through_full_closeout_seconds=elapsed,
                actual_complete_archive_bytes=size, resources_after_full_closeout=snapshot)
        except BaseException as error:
            failed = error; result.update(classification='READ_ONLY_SOURCEFACTOR_ACTIVITY_FAILED_NO_RETRY', error=repr(error))
            write_new(OUT / 'closeout_failure.json', result)
    print(json.dumps(result))
    if failed is not None: raise failed


def strict_json(path):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj: raise ValueError('duplicate terminal JSON key')
            obj[key] = value
        return obj
    def constant(value): raise ValueError('nonfinite terminal JSON constant: ' + value)
    obj = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=constant)
    if type(obj) is not dict: raise ValueError('complete actual stdout must be a single JSON object')
    return obj


def terminal_file(value, wanted):
    if not isinstance(wanted, str) or len(wanted) != 64 or any(char not in '0123456789abcdef' for char in wanted):
        raise ValueError('actual external terminal file SHA256 is required')
    path = Path(value)
    if not path.is_absolute() or '..' in path.parts or str(value) != str(path) or path.parent != TERMINAL or path.resolve(strict=True) != path:
        raise ValueError('actual external terminal evidence root/path differs')
    cursor = path
    while True:
        if cursor.is_symlink(): raise ValueError('external terminal evidence alias')
        if cursor == cursor.parent: break
        cursor = cursor.parent
    return require(path, wanted)


def diagnostic_admission(expected_seal, terminal_evidence, terminal_evidence_sha256):
    """Consumption needs Root's real original run exit0, never a static flag."""
    seal_admission(OUT, expected_seal)
    result = read(OUT / 'result.json'); d = admission(result['declaration_sha256'])
    if result['classification'] != 'COMPLETE_READ_ONLY_SOURCEFACTOR_ACTIVITY_DIAGNOSTIC_ONLY' or result['completed_commands'] != 1 or result['error'] is not None:
        raise ValueError('actual complete all-group activity diagnostic required')
    if result['archive_scope_roots'] != d['archive_reserve_roots']:
        raise ValueError('actual complete SOURCE+OUT archive scope differs')
    findings = read(OUT / 'audit/findings.json')
    for obj in (result, findings):
        if ((obj['transport_calls'], obj['linear_solves'], obj['replays']) != (0, 0, 0)
                or obj['AAA_accuracy_qualified'] is not False or obj['ABA_admitted'] is not False):
            raise ValueError('read-only diagnostic must not claim a transport result or scientific qualification')
    if (findings['groups'] != NG or findings['orders'] != [1, 2]
            or findings['source_record_inventory_complete'] is not True
            or findings['original_mapping_rows'] != 2 * NR * NZ * NL
            or result['findings'] != pin(OUT / 'audit/findings.json')):
        raise ValueError('complete actual all-group/moment mapping inventory is required')
    path = terminal_file(terminal_evidence, terminal_evidence_sha256)
    if path != TERMINAL / 'terminal_return.json': raise ValueError('fixed actual terminal-return receipt required')
    e = strict_json(path)
    command = [str(PYTHON), str(Path(__file__).resolve()), 'run', '--sha256', result['declaration_sha256']]
    if (e['schema'] != TERMINAL_SCHEMA or e['record_producer'] != 'root'
            or e['actual_tool_terminal_return_observed'] is not True or e['record_written_after_actual_terminal_return'] is not True
            or type(e['returncode']) is not int or e['returncode'] != 0 or e['command'] != command
            or e['source'] != d['source'] or e['declaration'] != pin(SOURCE / 'declaration.json')
            or e['activity_seal'] != dict(path=str(OUT / 'seal.json'), sha256=expected_seal)):
        raise ValueError('actual Root exit0 source/declaration/seal evidence differs')
    stdout = terminal_file(e['full_stdout']['path'], e['full_stdout']['sha256'])
    if stdout == path or e['full_stdout'] != pin(stdout): raise ValueError('actual complete stdout must be separately retained')
    returned = strict_json(stdout); tail = {key: returned[key] for key in TAIL_FIELDS}
    if returned != dict(result, **tail) or any(e[key] != tail[key] for key in TAIL_FIELDS): raise ValueError('actual retained stdout differs from sealed diagnostic and tail')
    elapsed, size, snap = tail[TAIL_FIELDS[1]], tail[TAIL_FIELDS[2]], tail[TAIL_FIELDS[3]]
    if (tail[TAIL_FIELDS[0]] != 'PASS' or type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not result['elapsed_seconds'] <= elapsed < TOTAL_WALL or type(size) is not int or not 0 <= size < RESERVE or size != archive_bytes()
            or snap['artifact_budget_bytes'] != 96 * 2**30 or snap['min_free_bytes'] != 8 * 2**30 or snap['resource_roots'] != d['resource_roots']
            or type(snap['artifact_bytes']) is not int or not size <= snap['artifact_bytes'] <= 96 * 2**30
            or type(snap['disk_free_bytes']) is not int or snap['disk_free_bytes'] < 8 * 2**30 or 'reason' in snap
            or type(snap['regular_files']) is not int or snap['regular_files'] < 1
            or type(snap['checked_unix']) not in (int, float) or not math.isfinite(snap['checked_unix']) or snap['checked_unix'] <= 0):
        raise ValueError('actual whole-closeout time/archive/history resources failed')
    stage = read(OUT / 'audit/stages.json')['stages']
    actual_child_command = [str(PYTHON), str(Path(__file__).resolve()), 'worker', '--sha256', result['declaration_sha256']]
    if len(stage) != 1 or stage[0]['label'] != 'audit/activity' or stage[0]['command'] != actual_child_command:
        raise ValueError('exactly one actual declared read-only child required')
    watch(stage[0])
    return dict(schema='AXMAT_SOURCEFACTOR_ACTIVITY_ACTUAL_TERMINAL_ADMISSION_V1', classification='ADMITTED_COMPLETE_READ_ONLY_DIAGNOSTIC_ONLY',
        activity_seal=pin(OUT / 'seal.json'), actual_external_terminal_evidence=pin(path), full_stdout=pin(stdout), findings=pin(OUT / 'audit/findings.json'),
        archive_scope_roots=d['archive_reserve_roots'],
        transport_calls=0, linear_solves=0, replays=0, AAA_accuracy_qualified=False, ABA_admitted=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('declare', 'run', 'worker', 'admit-diagnostic'))
    parser.add_argument('--sha256')
    parser.add_argument('--dispatch-evidence', type=Path)
    parser.add_argument('--dispatch-evidence-sha256')
    parser.add_argument('--terminal-evidence', type=Path)
    parser.add_argument('--terminal-evidence-sha256')
    args = parser.parse_args()
    if args.action == 'declare':
        if args.dispatch_evidence != REVIEW or not args.dispatch_evidence_sha256:
            parser.error('declare requires the actual reviewed compiled selector path and SHA256')
        declare(args.dispatch_evidence, args.dispatch_evidence_sha256)
    elif not args.sha256:
        parser.error('the actual frozen declaration SHA256 (or completed seal for admit-diagnostic) is required')
    elif args.action == 'admit-diagnostic':
        if not args.terminal_evidence or not args.terminal_evidence_sha256:
            parser.error('actual external terminal evidence and SHA256 required')
        print(json.dumps(diagnostic_admission(args.sha256, args.terminal_evidence, args.terminal_evidence_sha256)))
    else:
        {'run': run, 'worker': worker}[args.action](args.sha256)
