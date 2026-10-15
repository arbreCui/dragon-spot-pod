"""Canonical production controller + genuine frozen OwnRSS binding, source only.

Normal imports are used; no module/global/class/filename is replaced. The
reviewed future factory must supply real binding and completed new-control
pins. This module neither invents them nor creates terminal evidence. Its only
production mutation is the separately reviewed explicit executor callsite.
"""
import ast
import hashlib
import importlib
import json
import math
import marshal
import os
from pathlib import Path
import platform
import stat
import struct
import sys
import time
import types

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
BASE = ART / 'axial-material-production-qualified-AB-rank1-factor-cache-20261007/runtime/production_runner.py'
BASE_SHA = '844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d'
FULL = ROOT / 'validation/axial_material/cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py'
FULL_SHA = 'ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b'
GUARD_FACTORY = ROOT / 'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
GUARD_FACTORY_SHA = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
RESOURCE_CLASS_SOURCE = ROOT / 'validation/axial_material/prepare_qualified_AB_moment_order_production.py'
RESOURCE_CLASS_SHA = 'fe81150fbf270cac44e241ad64f352cf2f623fa65f7ccb4a9b0ded0a4f2c2d41'
BOUNDED_SHA = 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09'
SCHEMA = 'AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_OWN_RSS_BINDING_V1'
CONTROL_SCHEMA = 'AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_CONTROLS_V1'
SEAL_SCHEMA = 'AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_SEAL_V1'
TERMINAL_SCHEMA = 'AXMAT_COMBINED_PHYSICAL_MEMORY_CANONICAL_GUARD_ACTUAL_TERMINAL_V1'
CAPS = dict(rss_cap_mib=512, control_stage_seconds=60, control_total_seconds=120,
            control_archive_reserve_bytes=64 * 2**20, cold_total_seconds=43200,
            min_free_bytes=8 * 2**30, history_cap_bytes=96 * 2**30,
            threads=1, children_at_once=1, retries=0)
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
TAIL = ('actual_tail_check', 'actual_elapsed_seconds', 'actual_archive_bytes', 'actual_resources')
PRELOAD_RUNTIME_MODULES = ('production_inputs', 'snapshot_control_preflight',
                          'qualified_snapshot_ingestion', 'numerical_layout_admission',
                          'rank1_factor_cache_admission', 'white_receiver_tracking',
                          'physical_common_basis_admission')
CONSTRUCTOR_BEFORE = '    executor = SerialExecutor(work, budget.total_seconds, case, resources)\n'
CONSTRUCTOR_AFTER = ('    from combined_cold_own_rss_host import make_executor\n'
                     '    executor = make_executor(work, budget.total_seconds, case, resources,\n'
                     '                             info["own_child_supervision"])\n')


def source_contract():
    """A construction recipe only; real component and fixture pins are absent."""
    return dict(schema=SCHEMA,caps=CAPS,
        binding_file='WORK/own_rss_binding.json',
        controller='WORK/runtime/production_runner.py',
        host='WORK/runtime/combined_cold_own_rss_host.py',
        controls_source='WORK/runtime/combined_cold_own_rss_controls.py',
        bounded_helper='WORK/runtime/run_bounded_dragon.py',
        runtime_namespace=dict(files='EXACT_BASENAME_TO_ACTUAL_SHA256',directories=[]),
        runtime_module_owners=list(PRELOAD_RUNTIME_MODULES),
        module_owners='EXACT_ACTUAL_NORMAL_OR_GENUINE_LAZY_MODULE_NAME_TO_PATH_SHA256',
        resource_info='ACTUAL_ORIGINAL_CONTROLLER_INPUT_FIELDS_CASE_SPEC_ARTIFACT_ROOT_RESOURCE_ROOTS',
        producer_environment='REAL_CANONICAL_EXECUTABLE_PY3144_NUMPY244_ROOT_AND_COMPLETE_FILES',
        tested_guard_files='COMPLETE_ORIGINAL_619_GUARD_ADMISSION_DESCRIPTORS_IN_RETURN_ORDER',
        files='COMPLETE_EXPECTED_OWNER_UNION_INCLUDING_MODULES_ENV_AND_GUARD_PROOFS',
        control_output='WORK/binding_controls',control_terminal_root='INDEPENDENT_DIRECT_ARTIFACTS_CHILD',
        prepared_field='own_child_supervision',
        prepared_value=dict(binding='ACTUAL_BINDING_PATH_SHA256',
            controls=dict(seal='ACTUAL_COMPLETED_CONTROL_SEAL_PATH_SHA256',
                          terminal_evidence='ACTUAL_ROOT_EXIT_ZERO_PATH_SHA256')),
        explicit_constructor_before=CONSTRUCTOR_BEFORE,explicit_constructor_after=CONSTRUCTOR_AFTER,
        proposed_work_root='axial-material-production-qualified-AB-spoasm-physical-cache-memory-20261007',
        proposed_control_terminal_root='axial-material-qualified-AB-spoasm-physical-cache-memory-own-rss-terminal-20261007',
        memory_and_physical_component_admissions_required_by_future_factory=True,
        both_original_92d_predecessor_returns_must_be_entirely_equal=True,
        combined_link_delta_only=['memory_SPOT1P64.o_override','physical_SPOASM.o_override','new_Dragon_output'],
        fresh_cold_AAA_required=True,original_2000_batch_eight_gate_reference_still_required=True,
        no_actual_pins_invented=True,new_binding_fixture_executed=False,
        native_RSS_or_scientific_qualification_granted=False)


def require(path, expected=None):
    p = Path(path)
    if not p.is_absolute() or '..' in p.parts or str(p) != str(path):
        raise ValueError('literal absolute input path required')
    for item in (p, *p.parents):
        st = item.lstat()
        if stat.S_ISLNK(st.st_mode) or (item == p and not stat.S_ISREG(st.st_mode)):
            raise ValueError('regular canonical endpoint and nonalias ancestors required')
        if item != p and not stat.S_ISDIR(st.st_mode):
            raise ValueError('input ancestor is not a directory')
    if expected is not None and digest(p) != expected:
        raise ValueError('pinned canonical binding input changed: ' + str(p))
    return p


def digest(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        before = os.fstat(f.fileno())
        result = hashlib.file_digest(f, 'sha256').hexdigest()
        after = os.fstat(f.fileno())
        keys = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        if any(getattr(before, k) != getattr(after, k) for k in keys):
            raise ValueError('binding input changed during actual byte read')
    return result


def pin(path):
    p = require(path)
    return dict(path=str(p), sha256=digest(p))


def strict_json(path):
    def object_pairs(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError('duplicate JSON key')
            value[key] = item
        return value
    def finite_float(text):
        value = float(text)
        if not math.isfinite(value):
            raise ValueError('nonfinite JSON number')
        return value
    def nonfinite(text):
        raise ValueError('nonfinite JSON constant: ' + text)
    value = json.loads(require(path).read_text(), object_pairs_hook=object_pairs,
                       parse_float=finite_float, parse_constant=nonfinite)
    if type(value) is not dict:
        raise ValueError('JSON object required')
    return value


def pinned_descriptor(value):
    if (type(value) is not dict or set(value) != {'path', 'sha256'}
            or type(value['sha256']) is not str or len(value['sha256']) != 64
            or any(c not in '0123456789abcdef' for c in value['sha256'])
            or value['sha256'] == '0' * 64):
        raise ValueError('real nonplaceholder path/SHA descriptor required')
    return require(value['path'], value['sha256'])


def verify_files(files):
    if type(files) is not dict or not files:
        raise ValueError('complete explicit input owners required')
    for p, sha in files.items():
        pinned_descriptor(dict(path=p, sha256=sha))


def class_text(path, name):
    text = require(path).read_text()
    matches = [n for n in ast.parse(text).body if isinstance(n, ast.ClassDef) and n.name == name]
    if len(matches) != 1:
        raise ValueError('one actual class definition required')
    return ast.get_source_segment(text, matches[0])


def function_text(path, name):
    text = require(path).read_text()
    matches = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(matches) != 1:
        raise ValueError('one entire original function source required')
    return ast.get_source_segment(text, matches[0])


def patch_executor_callsite(source):
    """An explicit source transformation, never a runtime callable overlay."""
    if type(source) is not str or source.count(CONSTRUCTOR_BEFORE) != 1:
        raise ValueError('one original explicit SerialExecutor constructor required')
    baseline = require(BASE, BASE_SHA).read_text()
    def class_segment(text):
        nodes = [n for n in ast.parse(text).body
                 if isinstance(n, ast.ClassDef) and n.name == 'SerialExecutor']
        if len(nodes) != 1:
            raise ValueError('one complete original SerialExecutor class required')
        return ast.get_source_segment(text, nodes[0])
    if class_segment(source) != class_segment(baseline):
        raise ValueError('entire SerialExecutor class must remain 844 source-byte exact')
    changed = source.replace(CONSTRUCTOR_BEFORE, CONSTRUCTOR_AFTER, 1)
    if changed.count(CONSTRUCTOR_AFTER) != 1 or changed.replace(CONSTRUCTOR_AFTER, CONSTRUCTOR_BEFORE, 1) != source:
        raise ValueError('only the explicit production constructor source delta is allowed')
    ast.parse(changed)
    return changed, dict(schema='AXMAT_COMBINED_COLD_EXPLICIT_EXECUTOR_SOURCE_DELTA_V1',
        original_sha256=hashlib.sha256(source.encode()).hexdigest(),
        changed_sha256=hashlib.sha256(changed.encode()).hexdigest(),
        inverse_original_source_byte_exact=True,whole_SerialExecutor_844_source_byte_exact=True,
        constructor_delta=dict(before=CONSTRUCTOR_BEFORE,after=CONSTRUCTOR_AFTER),
        scientific_loop_body_changed=False,callable_or_globals_overlay=False,
        newly_bound_fixture_executed=False)


def compiled_code(path, class_name, member):
    """Derive code from pinned source without executing the compiled module."""
    source = require(path).read_text()
    code = compile(source, str(path), 'exec', dont_inherit=True, optimize=0)
    constants = code.co_consts
    if class_name is not None:
        classes = [n for n in constants if isinstance(n, types.CodeType) and n.co_name == class_name]
        if len(classes) != 1:
            raise ValueError('one pinned class code object required')
        constants = classes[0].co_consts
    functions = [n for n in constants if isinstance(n, types.CodeType) and n.co_name == member]
    if len(functions) != 1:
        raise ValueError('one pinned callable code object required')
    return functions[0]


CODE_IDENTITY_ENCODING = 'AXMAT_TYPED_COMPLETE_CODETYPE_CONSTRUCTOR_FIELDS_V1'
CODE_CONSTRUCTOR_FIELDS = (
    'co_argcount','co_posonlyargcount','co_kwonlyargcount','co_nlocals',
    'co_stacksize','co_flags','co_code','co_consts','co_names','co_varnames',
    'co_filename','co_name','co_qualname','co_firstlineno','co_linetable',
    'co_exceptiontable','co_freevars','co_cellvars')


def canonical_code_value(value):
    """Exact constructor fields and typed constants, without reference flags."""
    if type(value) is types.CodeType:
        return ['code',[[name,canonical_code_value(getattr(value,name))]
                        for name in CODE_CONSTRUCTOR_FIELDS]]
    if value is None:return ['None']
    if value is Ellipsis:return ['Ellipsis']
    if type(value) is bool:return ['bool',value]
    if type(value) is int:return ['int',str(value)]
    if type(value) is float:return ['float',struct.pack('!d',value).hex()]
    if type(value) is complex:
        return ['complex',struct.pack('!d',value.real).hex(),struct.pack('!d',value.imag).hex()]
    if type(value) is str:return ['str',value]
    if type(value) is bytes:return ['bytes',value.hex()]
    if type(value) is tuple:return ['tuple',[canonical_code_value(v)for v in value]]
    if type(value) is frozenset:
        items=[canonical_code_value(v)for v in value]
        return ['frozenset',sorted(items,key=lambda item:json.dumps(item,ensure_ascii=True,
                                    sort_keys=True,separators=(',',':'),allow_nan=False))]
    if type(value) is slice:
        return ['slice',canonical_code_value(value.start),canonical_code_value(value.stop),
                canonical_code_value(value.step)]
    raise ValueError('unsupported independently compiled code constant kind')


def canonical_code_bytes(code):
    if type(code) is not types.CodeType:
        raise ValueError('a genuine complete compiled code object required')
    return json.dumps([CODE_IDENTITY_ENCODING,canonical_code_value(code)],ensure_ascii=True,
                      sort_keys=True,separators=(',',':'),allow_nan=False).encode('ascii')


def code_identity(actual, path, class_name, member, globals_owner):
    expected = compiled_code(path, class_name, member)
    if (actual.__globals__ is not vars(globals_owner)
            or actual.__code__.co_filename != str(path)
            or canonical_code_bytes(actual.__code__) != canonical_code_bytes(expected)):
        raise ValueError('actual imported callable differs from its entire pinned compiled source')
    return hashlib.sha256(canonical_code_bytes(actual.__code__)).hexdigest()


def normal_module(name, expected_path):
    """Import normally or reject an existing different binding; never replace."""
    expected_path = require(expected_path)
    if name in sys.modules:
        old = sys.modules[name]
        if old is None or Path(getattr(old, '__file__', '')).resolve() != expected_path:
            raise ValueError('existing canonical module has a different source: ' + name)
    obj = importlib.import_module(name)
    if (Path(obj.__file__).resolve() != expected_path or obj.__spec__ is None
            or Path(obj.__spec__.origin).resolve() != expected_path
            or obj.__name__ != name or obj.__spec__.name != name):
        raise ValueError('normal import resolved outside the pinned actual source')
    return obj


def runtime_namespace(work, expected):
    """No copied runtime alias, package shadow or new bytecode directory."""
    if type(expected) is not dict or set(expected) != {'files', 'directories'} or expected['directories'] != []:
        raise ValueError('complete flat copied runtime namespace required')
    root = Path(work) / 'runtime'
    if root.is_symlink() or not root.is_dir():
        raise ValueError('real copied runtime directory required')
    actual = {}
    for p in root.iterdir():
        if p.is_dir() or p.is_symlink():
            raise ValueError('unexpected runtime directory/package/alias')
        actual[p.name] = digest(require(p))
    if actual != expected['files']:
        raise ValueError('complete copied runtime bytes/namespace changed')


def binding_admission(descriptor):
    path = pinned_descriptor(descriptor)
    b = strict_json(path)
    if (b.get('schema') != SCHEMA or b.get('caps') != CAPS
            or b.get('scientific_qualification') is not False
            or b.get('module_global_or_class_overlay') is not False
            or b.get('canonical_controller_name') != 'production_runner'):
        raise ValueError('complete source-only new-binding contract required')
    work = Path(b['work_root'])
    if (work.parent != ART or work.is_symlink() or not work.is_dir()
            or path != work / 'own_rss_binding.json'
            or b['controller']['path'] != str(work / 'runtime/production_runner.py')
            or b['host']['path'] != str(work / 'runtime/combined_cold_own_rss_host.py')
            or b['controls_source']['path'] != str(work / 'runtime/combined_cold_own_rss_controls.py')
            or b['bounded_helper'] != dict(path=str(work / 'runtime/run_bounded_dragon.py'), sha256=BOUNDED_SHA)
            or b['serial_baseline'] != dict(path=str(BASE), sha256=BASE_SHA)
            or b['own_rss_source'] != dict(path=str(FULL), sha256=FULL_SHA)
            or b['guard_factory'] != dict(path=str(GUARD_FACTORY), sha256=GUARD_FACTORY_SHA)
            or b['resource_class_source'] != dict(path=str(RESOURCE_CLASS_SOURCE), sha256=RESOURCE_CLASS_SHA)):
        raise ValueError('actual controller, original class and local-helper identities required')
    for key in ('controller', 'host', 'controls_source', 'bounded_helper', 'serial_baseline',
                'own_rss_source', 'guard_factory', 'resource_class_source'):
        item = b[key]
        pinned_descriptor(item)
        if b['files'].get(item['path']) != item['sha256']:
            raise ValueError('declared code owner does not bind actual module descriptor')
    for owners in (b['runtime_module_owners'], b['module_owners']):
        if type(owners) is not dict:
            raise ValueError('explicit normally imported module owner mapping required')
        for item in owners.values():
            pinned_descriptor(item)
            if b['files'].get(item['path']) != item['sha256']:
                raise ValueError('module owner is absent from complete independently pinned files')
    if b['host']['path'] != str(Path(__file__).resolve()):
        raise ValueError('constructor helper must execute its actual copied source')
    verify_files(b['files'])
    runtime_namespace(work, b['runtime_namespace'])
    if (class_text(BASE, 'SerialExecutor') != class_text(work / 'runtime/production_runner.py', 'SerialExecutor')
            or function_text(BASE, 'qualify_aba') != function_text(work / 'runtime/production_runner.py', 'qualify_aba')
            or function_text(BASE, 'resource_monitor') != function_text(work / 'runtime/production_runner.py', 'resource_monitor')
            or any(os.environ.get(k) != '1' for k in THREADS)
            or os.environ.get('PYTHONDONTWRITEBYTECODE') != '1'
            or platform.python_version() != '3.14.4'
            or sys.flags.optimize != 0
            or str(Path(sys.executable).resolve()) != b['producer_environment']['executable']):
        raise ValueError('original SerialExecutor class and exact producer environment required')
    verify_files(b['producer_environment']['files'])
    if (b['producer_environment']['python_version'] != '3.14.4'
            or b['producer_environment']['numpy_version'] != '2.4.4'):
        raise ValueError('original Py3.14.4/NumPy2.4.4 environment required')
    return b


def source_mro_proof(c, full, b):
    """Actual live class/callable identities, not a copied class or old fixture."""
    path = Path(b['controller']['path'])
    probe = normal_module('probe_refined_AAA_white_odd_response',
                          ROOT / 'validation/axial_material/probe_refined_AAA_white_odd_response.py')
    if (c.__name__ != 'production_runner' or c.SerialExecutor.__module__ != 'production_runner'
            or full.OwnRSSSerialExecutor.__module__ != 'qualify_refined_AAA_layered_full'
            or full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,)
            or full.SerialExecutor is not c.SerialExecutor
            or full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__
            or full.OwnRSSSerialExecutor.execute is not c.SerialExecutor.execute
            or full.write_new is not probe.write_new or full.Path is not Path
            or full.subprocess is not importlib.import_module('subprocess')
            or full.time is not importlib.import_module('time')
            or c.Path is not Path or c.os is not os
            or c.subprocess is not importlib.import_module('subprocess')
            or c.time is not importlib.import_module('time')
            or c.importlib is not importlib or c.RESOURCE_POLL_SECONDS != 1.0):
        raise ValueError('genuine canonical base/init/execute and unmodified original process globals required')
    codes = {name: code_identity(getattr(c.SerialExecutor, name), path, 'SerialExecutor', name, c)
             for name in ('__init__', 'execute', '_process')}
    codes['OwnRSS._process'] = code_identity(full.OwnRSSSerialExecutor._process, FULL,
                                            'OwnRSSSerialExecutor', '_process', full)
    codes['write_new'] = code_identity(probe.write_new, Path(probe.__file__), None, 'write_new', probe)
    for name in ('resource_monitor','run','qualify_aba','dump_json','check_dragon_log','sha256'):
        codes[name] = code_identity(getattr(c, name), path, None, name, c)
    return dict(controller=b['controller'], serial_baseline=b['serial_baseline'], own_rss_source=b['own_rss_source'],
        canonical_controller_name='production_runner',actual_direct_bases=['production_runner.SerialExecutor'],
        inherited_original_init=True,inherited_original_execute=True,
        entire_SerialExecutor_source_byte_exact=True,actual_compiled_callable_sha256=codes,
        actual_original_process_globals_identity=True,existing_guard_is_prior_proof_only=True,
        new_binding_fixture_pass_claimed=False,module_global_or_class_overlay=False)


def bounded_helper_provenance(executor, b):
    module = executor.bounded
    path = Path(b['bounded_helper']['path'])
    if (module.__file__ != str(path) or module.__spec__ is None
            or module.__spec__.origin != str(path) or digest(require(path)) != BOUNDED_SHA):
        raise ValueError('actual inherited constructor local bounded-helper loader/source differs')
    return dict(source=b['bounded_helper'],actual_compiled_callable_sha256={
        name:code_identity(getattr(module,name),path,None,name,module)
        for name in ('start_liveness_watchdog','finish_liveness_watchdog','terminate_group','process_group_exists')},
        original_bounded_group_cleanup_code_identity=True,helper_globals_or_callable_overlay=False)


def loaded_project_module_admission(b):
    """Actual names and sources, including genuine lazy resource ancestors."""
    for name, obj in list(sys.modules.items()):
        source = getattr(obj, '__file__', None)
        if not source:
            continue
        p = Path(source).resolve()
        if p.is_relative_to(ROOT / 'validation'):
            wanted = b['module_owners'].get(name)
            if wanted is None or pinned_descriptor(wanted) != p:
                raise ValueError('actual imported project module has no explicit expected owner: ' + name)


def bind_controller(descriptor):
    """Establish genuine canonical MRO; this function never launches a child."""
    b = binding_admission(descriptor)
    work = Path(b['work_root'])
    sys.path.insert(0, str(work / 'runtime'))
    # Preload declared current copies before the frozen probe prepends its old
    # runtime. Ordinary import rejects an already loaded different source.
    for name in PRELOAD_RUNTIME_MODULES:
        item = b['runtime_module_owners'].get(name)
        if item is None or pinned_descriptor(item) != work / 'runtime' / (name + '.py'):
            raise ValueError('explicit current copied-runtime module owner required: ' + name)
        normal_module(name, item['path'])
    c = normal_module('production_runner', work / 'runtime/production_runner.py')
    sys.path.insert(0, str(ROOT / 'validation/axial_material'))
    sys.path.insert(0, str(FULL.parent))
    full = normal_module('qualify_refined_AAA_layered_full', FULL)
    guard = normal_module('prepare_qualified_AB_source_factor_production', GUARD_FACTORY)
    sys.path.insert(0, str(work / 'runtime'))
    if (full.OwnRSSSerialExecutor.__bases__ != (c.SerialExecutor,)
            or full.SerialExecutor is not c.SerialExecutor
            or full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__
            or full.OwnRSSSerialExecutor._process.__code__.co_filename != str(FULL)
            or c.SerialExecutor.__init__.__code__.co_filename != str(work / 'runtime/production_runner.py')):
        raise ValueError('genuine frozen OwnRSS must inherit this normally imported real SerialExecutor')
    np = importlib.import_module('numpy')
    if np.__version__ != '2.4.4' or str(Path(np.__file__).parent.resolve()) != b['producer_environment']['numpy_root']:
        raise ValueError('actual loaded original NumPy environment differs')
    old_guard = guard.guard_admission(full)
    expected_guard = b['tested_guard_files']
    if [str(p) for p in old_guard] != [v['path'] for v in expected_guard]:
        raise ValueError('complete original tested guard proof identities required')
    for item in expected_guard:
        pinned_descriptor(item)
        if b['files'].get(item['path']) != item['sha256']:
            raise ValueError('tested guard dependency not independently source-bound')
    source_mro_proof(c, full, b)
    # Explicit module owners are supplied by the future declare graph. Every
    # actual project module imported by this old full/probe chain must belong.
    loaded_project_module_admission(b)
    verify_files(b['files'])
    runtime_namespace(work, b['runtime_namespace'])
    return c, full, b


def resource_provenance(resources, c, b):
    loaded_project_module_admission(b)
    cls = type(resources)
    module = sys.modules.get(cls.__module__)
    if (module is None or pin(module.__file__) != b['resource_class_source']
            or getattr(module, 'DynamicHistoryResources', None) is not cls
            or resources.min_free_bytes != 8 * 2**30 or resources.max_bytes != 96 * 2**30
            or Path(resources.artifacts_root) != ART
            or resources.declared_roots != b['resource_info']['resource_roots']
            or resources.failure_type is not c.ResourceFailure):
        raise ValueError('genuine unchanged dynamic family96/free8 resource class required')
    return dict(class_module=cls.__module__, class_source=pin(module.__file__),
                class_name=cls.__name__, no_class_or_resource_overlay=True)


def control_namespace(root):
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('actual control root required')
    files, directories = {}, []
    for folder, dirs, names in os.walk(root, followlinks=False):
        if any((Path(folder) / x).is_symlink() for x in dirs + names):
            raise ValueError('control namespace alias')
        for name in dirs:
            directories.append(str((Path(folder) / name).relative_to(root)))
        for name in names:
            p = require(Path(folder) / name)
            files[str(p.relative_to(root))] = digest(p)
    return dict(files=files, directories=sorted(directories))


def control_archive_bytes(b):
    root = Path(b['work_root']) / 'binding_controls'
    total = 0
    if root.exists():
        for folder, dirs, names in os.walk(root, followlinks=False):
            if any((Path(folder) / n).is_symlink() for n in dirs + names):
                raise ValueError('control archive alias')
            total += sum(require(Path(folder) / n).stat().st_size for n in names)
    total += sum(pinned_descriptor(b[key]).stat().st_size for key in ('host', 'controls_source'))
    total += require(Path(b['work_root']) / 'own_rss_binding.json').stat().st_size
    return total


def own_pid_peak_admission(watch):
    """Validate actual live samples plus the exact returned own-PID receipt."""
    import math
    required = {'pid','returncode','sampled_peak_rss_mib','limit_failure','rss_cap_mib',
        'own_pid_wait4_observed','own_pid_wait4_pid','own_pid_wait4_status',
        'own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib',
        'observed_peak_rss_mib','live_rss_sample_count','rss_peak_observation_contract'}
    if type(watch) is not dict or not required.issubset(watch):
        raise ValueError('complete actual own-PID peak fields required')
    if (sys.platform != 'darwin' or watch['rss_cap_mib'] != 512
            or type(watch['pid']) is not int or watch['pid'] <= 0
            or type(watch['returncode']) is not int
            or type(watch['own_pid_wait4_observed']) is not bool
            or watch['rss_peak_observation_contract'] != 'EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'):
        raise ValueError('exact Darwin own-PID peak observation contract required')
    sampled = watch['sampled_peak_rss_mib'];count = watch['live_rss_sample_count']
    observed = watch['observed_peak_rss_mib']
    if (type(sampled) not in (int,float) or not math.isfinite(sampled) or sampled < 0
            or type(observed) not in (int,float) or not math.isfinite(observed) or observed < 0
            or type(count) is not int or count < 0 or count == 0 and sampled != 0):
        raise ValueError('actual finite live sample/count and observed peak required')
    kernel = watch['own_pid_wait4_peak_rss_mib']
    if watch['own_pid_wait4_observed']:
        pid = watch['own_pid_wait4_pid'];status = watch['own_pid_wait4_status']
        raw = watch['own_pid_wait4_ru_maxrss_bytes']
        if (type(pid) is not int or pid != watch['pid']
                or type(status) is not int or not 0 <= status <= 65535
                or not (os.WIFEXITED(status) or os.WIFSIGNALED(status))
                or os.waitstatus_to_exitcode(status) != watch['returncode']
                or type(raw) not in (int,float) or not math.isfinite(raw) or raw <= 0 or raw != int(raw)
                or type(kernel) not in (int,float) or not math.isfinite(kernel) or kernel <= 0
                or kernel != raw / (1024.*1024.)):
            raise ValueError('real returned own PID/status/integer Darwin-byte peak required')
    elif any(watch[name] is not None for name in ('own_pid_wait4_pid','own_pid_wait4_status',
             'own_pid_wait4_ru_maxrss_bytes','own_pid_wait4_peak_rss_mib')):
        raise ValueError('absent terminal receipt cannot carry invented kernel fields')
    expected = max(sampled,kernel if kernel is not None else 0.)
    if observed != expected:
        raise ValueError('observed peak must equal actual live/own-PID kernel maximum')
    if watch['limit_failure'] is None:
        if (watch['returncode'] != 0 or watch['own_pid_wait4_observed'] is not True
                or not 0 < observed < 512):
            raise ValueError('normal completion requires real own-PID peak below512')
        classification = 'PASS_REAL_OWN_PID_COMPLETION_PEAK'
    elif watch['limit_failure'] == "RuntimeError('own-child 512 MiB RSS cap reached')":
        if watch['returncode'] not in (-15,-9) or sampled < 512 or observed < 512:
            raise ValueError('expected oversize requires actual original live512 rejection')
        classification = 'EXPECTED_ACTUAL_LIVE_RSS_REJECTION_KERNEL_RECEIPT_NOT_REQUIRED'
    else:
        raise ValueError('unqualified failure cannot satisfy own-PID completion peak gate')
    return dict(classification=classification,pid=watch['pid'],live_sample_count=count,
        sampled_peak_rss_mib=sampled,own_pid_wait4_observed=watch['own_pid_wait4_observed'],
        own_pid_wait4_peak_rss_mib=kernel,observed_peak_rss_mib=observed,
        rss_peak_observation_contract=watch['rss_peak_observation_contract'])


def controls_admission(b, binding, descriptor):
    """Only actual new-control exit zero permits the production constructor."""
    if type(descriptor) is not dict or set(descriptor) != {'seal', 'terminal_evidence'}:
        raise ValueError('new independent completed control seal/Root terminal pins required')
    root = Path(b['work_root']) / 'binding_controls'
    seal_path = pinned_descriptor(descriptor['seal'])
    if seal_path != root / 'seal.json':
        raise ValueError('fixed new binding-control seal required')
    seal = strict_json(seal_path)
    actual = control_namespace(root)
    if (seal['schema'] != SEAL_SCHEMA or actual['directories'] != seal['namespace_directories']
            or set(actual['files']) != set(seal['files']) | {'seal.json'}
            or any(actual['files'][p] != w for p, w in seal['files'].items())):
        raise ValueError('complete sealed new-binding controls required')
    result = strict_json(root / 'result.json')
    if (result['schema'] != CONTROL_SCHEMA or result['classification'] != 'PASS_NEW_CANONICAL_OWN_RSS_BINDING_CONTROLS_ONLY'
            or result['binding'] != binding or result['caps'] != CAPS
            or result['scientific_qualification'] is not False
            or result['positive_completed'] is not True or result['actual_oversize_rejected'] is not True
            or result['short_completed'] is not True or result['short_allocation_bytes'] != 16*2**20
            or result['rss_peak_observation_contract'] != 'EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1'
            or result['own_children_no_longer_live'] is not True):
        raise ValueError('all three actual new canonical-binding fixture controls required')
    c = normal_module('production_runner', b['controller']['path'])
    full = normal_module('qualify_refined_AAA_layered_full', FULL)
    if result['source_identity'] != source_mro_proof(c, full, b):
        raise ValueError('the exact actual canonical MRO/callable identities tested by new controls required')
    helper_path = Path(b['bounded_helper']['path'])
    expected_helper = dict(source=b['bounded_helper'],actual_compiled_callable_sha256={
        name:hashlib.sha256(canonical_code_bytes(compiled_code(helper_path,None,name))).hexdigest()
        for name in ('start_liveness_watchdog','finish_liveness_watchdog','terminate_group','process_group_exists')},
        original_bounded_group_cleanup_code_identity=True,helper_globals_or_callable_overlay=False)
    if result['actual_bounded_helper'] != expected_helper:
        raise ValueError('the actually constructor-loaded original bounded cleanup code is not the tested source')
    if ([o['mode'] for o in result['observations']] != ['positive','oversize','short']
            or any(o['actual_group_no_longer_live'] is not True for o in result['observations'])):
        raise ValueError('all three actual new-child observations and no-live-group gates required')
    for observation in result['observations']:
        watch_path = pinned_descriptor(observation['watchdog'])
        log_path = pinned_descriptor(observation['raw_log'])
        if (watch_path != root / observation['mode'] / 'execute.watchdog.json'
                or log_path != root / observation['mode'] / 'execute.log'
                or strict_json(watch_path) != observation['watch']):
            raise ValueError('actual raw watchdog/log identities differ from sealed new controls')
    stages = strict_json(root / 'stages.json')['stages']
    if ([s['label'] for s in stages] != ['binding_controls/positive/execute','binding_controls/oversize/execute','binding_controls/short/execute']
            or [s['status'] for s in stages] != ['PASS','FAILED','PASS']):
        raise ValueError('exact three guarded fixture stages required')
    for stage, observation in zip(stages, result['observations']):
        mode = observation['mode']
        command = [b['producer_environment']['executable'],b['controls_source']['path'],'fixture',mode]
        watch = observation['watch']
        if (stage['command'] != command or observation['command'] != command or watch['command'] != command
                or watch['rss_cap_mib'] != 512 or watch['own_child_only'] is not True
                or watch['liveness_group_cleanup'] is not True
                or type(watch['pid']) is not int or watch['pid'] <= 0
                or not 0 < watch['wall_cap_seconds'] <= stage['wall_cap_seconds'] <= 60
                or not 0 <= watch['elapsed_seconds'] < watch['wall_cap_seconds']):
            raise ValueError('actual original direct-own-child command, PID, cleanup and limits required')
        peak_identity = own_pid_peak_admission(watch)
        if mode in ('positive','short'):
            if (watch['returncode'] != 0 or watch['limit_failure'] is not None
                    or not 0 < peak_identity['observed_peak_rss_mib'] < 512
                    or observation['actual_expected_rejection'] is not None
                    or stage['log_sha256'] != observation['raw_log']['sha256']):
                raise ValueError('actual normally completed positive/short control required')
            if mode == 'short' and watch['own_pid_wait4_peak_rss_mib'] < 16:
                raise ValueError('short real16MiB allocation needs its own kernel peak')
        elif (watch['returncode'] not in (-15,-9) or watch['sampled_peak_rss_mib'] < 512
                or watch['limit_failure'] != "RuntimeError('own-child 512 MiB RSS cap reached')"
                or stage['error'] != 'own-child 512 MiB RSS cap reached'
                or observation['actual_expected_rejection'] != 'own-child 512 MiB RSS cap reached'):
            raise ValueError('actual original RSS branch rejection, not a wall/metadata failure, required')
    terminal_path = pinned_descriptor(descriptor['terminal_evidence'])
    terminal_root = Path(b['control_terminal_root'])
    if (terminal_root.parent != ART or terminal_root.is_relative_to(Path(b['work_root']))
            or terminal_path != terminal_root / 'terminal_return.json'):
        raise ValueError('independent fixed actual Root control terminal root required')
    e = strict_json(terminal_path)
    actual_tool = e['actual_tool_result']
    if (type(actual_tool) is not dict
            or set(actual_tool) != {'initial_chunk_id','session_id','terminal_chunk_id','exit_code'}
            or type(actual_tool['exit_code']) is not int or actual_tool['exit_code'] != 0
            or any(type(actual_tool[k]) is not str or not actual_tool[k] for k in ('initial_chunk_id','terminal_chunk_id'))
            or actual_tool['session_id'] is not None
               and (type(actual_tool['session_id']) is not int or actual_tool['session_id'] <= 0)):
        raise ValueError('actual observed Root tool terminal exit-zero record required')
    command = [b['producer_environment']['executable'], b['controls_source']['path'], 'run-controls',
               '--binding', binding['path'], '--binding-sha256', binding['sha256']]
    if (e['schema'] != TERMINAL_SCHEMA or e['record_producer'] != 'root'
            or e['actual_tool_terminal_return_observed'] is not True
            or e['record_written_after_actual_terminal_return'] is not True
            or type(e['returncode']) is not int or e['returncode'] != 0
            or e['command'] != command or e['binding'] != binding
            or e['source'] != b['controls_source'] or e['host'] != b['host']
            or e['control_seal'] != descriptor['seal']):
        raise ValueError('actual new-control Root exit zero proof required')
    stdout = pinned_descriptor(e['full_stdout'])
    stderr = pinned_descriptor(e['full_stderr'])
    if stdout.parent != terminal_root or stderr.parent != terminal_root or len({stdout, stderr, terminal_path}) != 3:
        raise ValueError('full stdout/stderr must be independently retained')
    returned = strict_json(stdout)
    tail = {k: returned[k] for k in TAIL}
    r = tail['actual_resources']
    if (returned != dict(result=result, **tail) or any(e[k] != tail[k] for k in TAIL)
            or tail['actual_tail_check'] != 'PASS'
            or type(tail['actual_elapsed_seconds']) not in (int, float)
            or not result['elapsed_before_closeout'] <= tail['actual_elapsed_seconds'] < 120
            or type(tail['actual_archive_bytes']) is not int
            or not tail['actual_archive_bytes'] == control_archive_bytes(b) < 64 * 2**20
            or r['artifact_budget_bytes'] != 96 * 2**30 or r['min_free_bytes'] != 8 * 2**30
            or r['artifact_bytes'] > 96 * 2**30 or r['disk_free_bytes'] < 8 * 2**30
            or r['resource_scope_policy'] != 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
            or 'reason' in r):
        raise ValueError('complete actual new-control tail must fit original caps')
    return result


def make_executor(work, total_seconds, case, resources, supervision_contract):
    """Explicit sole constructor replacement for a future reviewed c.run."""
    started = time.monotonic()
    if type(supervision_contract) is not dict or set(supervision_contract) != {'binding', 'controls'}:
        raise ValueError('explicit prepared new-binding and real completed-control pins required')
    c, full, b = bind_controller(supervision_contract['binding'])
    if Path(work) != Path(b['work_root']) or case not in ('AAA', 'ABA') or total_seconds != 43200:
        raise ValueError('unchanged original cold work/case/whole43200 budget required')
    controls_admission(b, supervision_contract['binding'], supervision_contract['controls'])
    resource_provenance(resources, c, b)
    resources.check()
    executor = full.OwnRSSSerialExecutor(Path(work), total_seconds, case, resources)
    # Include this new constructor's actual input/guard admission work. This
    # only shortens the inherited deadline; it never grants additional time.
    executor.deadline = min(executor.deadline, started + total_seconds)
    if (executor.records != [] or executor.bounded.__file__ != b['bounded_helper']['path']
            or digest(require(executor.bounded.__file__)) != BOUNDED_SHA):
        raise ValueError('genuine inherited constructor must load this actual pinned local helper only')
    bounded_helper_provenance(executor, b)
    return executor


def launch(work, prepared_sha, supervision_contract):
    """Call the real c.run after canonical import; never execute it as __main__."""
    c, _, b = bind_controller(supervision_contract['binding'])
    if Path(work) != Path(b['work_root']):
        raise ValueError('actual fresh work identity required')
    controls_admission(b, supervision_contract['binding'], supervision_contract['controls'])
    prepared = require(Path(work) / 'prepared.json', prepared_sha)
    return c.run(prepared, prepared_sha, 'AAA', None, None)
