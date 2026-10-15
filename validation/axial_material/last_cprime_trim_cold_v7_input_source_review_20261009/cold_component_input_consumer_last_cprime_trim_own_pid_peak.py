"""UNREADY source-only trim cold INPUT consumer.

Whole old seven-key ancestry remains unchanged. An independent actual trim
return is added as INPUT; no API, child, old RSS or science credit is executed.
All future combined graph and bounded-intake evidence are unbound.
"""
import ast
import gc
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import re
import stat
import sys

ROOT = Path('/Users/wen/spot')
ART = ROOT/'validation/artifacts'
SCHEMA = 'AXMAT_COLD_COMPLETE_LAST_CPRIME_TRIM_COMPONENT_INPUT_INTAKE_V1'
WITNESS_SCHEMA = 'AXMAT_OWNED_SPECS_STANDALONE_BOUNDED_RUNTIME_API_INTAKE_ROOT_ACTUAL_RETURN_V1'
SEMANTICS = 'COMPLETE_FRESH_COLD_INPUT_REUSE_NOT_COMPONENT_API_REEXECUTION'
STATUS = 'UNREADY_TRIM_COMBINED_AND_BOUNDED_INTAKE_PENDING'
INTAKE_ROOT = ART/'axial-material-owned-specs-trim-v7-standalone-bounded-runtime-api-intake-evidence-20261009'
INTAKE_ROOT_SHA = None
INTAKE_RETURN_SHA = None
THREADS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
GRAPH_SOURCE_SHA = '85551979317309cfa70bb27a4b0e04ae908bbd33865dc3edfbe6c7f4d70baf6c'
CODEC_SOURCE_SHA = '758c6d39ecb4c37e5ff5b3d6639ab8404447719e7cfd3ff72336276a94bb2e69'
CHECK_SOURCE_SHA = '86e7d6340da59c74abcff57fa52bb07d690f51cc33fe76f330ece2e0d158258e'
SPECS = ROOT/'validation/axial_material/combined_runtime_complete_historical_input_specs_20261007.json'
SPECS_SHA = '2cad9a8a711ce49a6cfd14b897166c24102a047dac1d54d0add61f16c88a99fa'
API_SOURCE = ROOT/'validation/axial_material/prepare_historical_input_owned_specs_trim_combined_physical_dedup_file_snapshot_runtime_build_live_resource_scopes_v7.py'
API_SOURCE_SHA = '45783d9920a53ca517f28abbff9071e81cd29b0ef87336f45216aa86d8e4bc5a'
API_SCHEMA = 'AXMAT_HISTORICAL_INPUT_OWNED_SPECS_LAST_CPRIME_TRIM_COMBINED_PHYSICAL_DEDUP_RUNTIME_LIVE_RESOURCE_SCOPES_V7_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
API_BUILD = ART/'axial-material-historical-input-physical-dedup-combined-runtime-build-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009'
API_SOURCE_ROOT = ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-admission-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009'
API_TERMINAL = ART/'axial-material-qualified-AB-historical-input-physical-dedup-combined-runtime-build-terminal-owned-specs-last-cprime-trim-live-resource-scopes-v7-20261009'
API_SEAL_SHA = None
API_TERMINAL_SHA = None
API_PREP_SHA = None
PYTHON = '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
PRIOR_DECL = ART/'axial-material-physical-dedup-combined-runtime-build-20261007/declaration.json'
PRIOR_DECL_SHA = 'aa3e33a10b64deb947f82fd9f8b19559f9f700f58396e641a4e66def5d4b46a4'
PRIOR_SOURCE = ART/'axial-material-qualified-AB-physical-dedup-combined-runtime-build-admission-20261007'
CAPTURE_FACTORY = ROOT/'validation/axial_material/prepare_rank1_cache_memory_dedup_file_snapshot_native_angular_capture.py'
CAPTURE_FACTORY_SHA = '48ffa6568487bd4d57503cb9a6e8ee8b70ae7e24584e1757363a1ab4874bfc6c'
PHYSICAL_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_spoasm_physical_abi_serial_guarded_production.py'
PHYSICAL_FACTORY_SHA = 'b7f361bc1d8dcdcfabf1cd2d33af3730ffb146ebe610e12370ea2b409f1ca230'
RESOURCE_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_cache_production.py'
RESOURCE_FACTORY_SHA = '92d73658e349ea2b2816b2b770549ca22378c2595f2c9e5c9331bbf91c6abf8a'
BASE_CONTROLLER = ART/'axial-material-production-qualified-AB-rank1-factor-cache-20261007/runtime/production_runner.py'
BASE_CONTROLLER_SHA = '844fe18738a2232d2947a8c65dc13afebcfbfd2e2afc9f0743c1c94c06fd0f7d'
FULL = ROOT/'validation/axial_material/cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py'
FULL_SHA = 'ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b'
GUARD = ROOT/'validation/axial_material/prepare_qualified_AB_source_factor_production.py'
GUARD_SHA = '619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743'
HISTORY_POLICY = 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'

TRIM_FACTORY = ROOT/'validation/axial_material/prepare_qualified_AB_rank1_factor_cache_last_cprime_trim_production.py'
TRIM_FACTORY_SHA = '8f6947392a087cd722fc2cbc3075db54c256c73bcf9dab72cac708392b5ef92a'
TRIM_SOURCE = ART/'axial-material-qualified-AB-rank1-factor-cache-last-cprime-trim-build-admission-20261008'
TRIM_BUILD = ART/'axial-material-rank1-factor-cache-last-cprime-trim-build-20261008'
TRIM_TERMINAL = ART/'axial-material-qualified-AB-rank1-factor-cache-last-cprime-trim-build-terminal-20261008'
TRIM_DECL_SHA = 'e6dd804a473ae25888ecf5e070af708a024618772c0f753d836127af6074dc00'
TRIM_SEAL_SHA = '38f44fe55187199e467f8445015e505814cf0df911d9a51d1b35c8e264bb0e0e'
TRIM_TERMINAL_SHA = '076565db2dc0048db70166d37bd6e81107d30acb9a72b14945b436a473094a88'
TRIM_KERNEL_SHA = '343e731fa190d80f8d390831185aef11dabcab32f51a229a5761c827a4aeb1e1'
TRIM_OBJECT_SHA = 'd9818c7aa7d10cef2cbb95119c13db449867a01518ec5928566462880b2cb767'
TRIM_RUNTIME_SHA = 'b807c72ca393bca3a21297ea15d5e44d008cac49fc7623781fca9303a9141ddf'
TRIM_SOURCE_ADMISSION_SHA = '559b25aa80ff165ce6edc756de9c9309929288c5e601ef2ce71a1e9805c11677'
TRIM_SCHEMA = 'AXMAT_RANK1_FACTOR_CACHE_LAST_CPRIME_TRIM_PRODUCTION_RUNTIME_INPUT_ADMISSION_V1'
TRIM_INPUT_SEMANTICS = 'ACTUAL_TRIM_3ARG_RETURN_IN_THIS_PREP_THEN_COMPLETE_FRESH_INPUT_REUSE_NO_API_REEXECUTION'


def nonzero_sha(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}',value) is None or value=='0'*64:
        raise ValueError('independently expected nonplaceholder SHA256 required')
    return value


def input_guard():
    if sys.flags.optimize != 0 or 'PYTHONOPTIMIZE' in os.environ:
        raise ValueError('nonoptimized source predicates required before project input read')
    if STATUS != 'REVIEWED_TRIM_COMPLETE_INPUT_CONSUMER_WITH_ACTUAL_BOUNDED_INTAKE':
        raise ValueError('UNREADY: no actual intake or cold binding/fixture credit')
    if any(os.environ.get(k)!='1' for k in THREADS):
        raise ValueError('original single-thread contract required')

    for value in (INTAKE_ROOT_SHA,INTAKE_RETURN_SHA,API_SOURCE_SHA,API_SEAL_SHA,API_TERMINAL_SHA,API_PREP_SHA):
        nonzero_sha(value)
    for path in (API_SOURCE,API_BUILD,API_SOURCE_ROOT,API_TERMINAL):
        if path is None or not Path(path).is_absolute():raise ValueError('UNREADY: actual winning combined bindings required')
    if type(API_SCHEMA)is not str or not API_SCHEMA:raise ValueError('UNREADY: actual winning combined schema required')

def normal(path,missing=False):
    path=Path(path)
    if not path.is_absolute() or '..' in path.parts:raise ValueError('absolute canonical path required')
    for p in [*reversed(path.parents),path]:
        try:s=p.lstat()
        except FileNotFoundError:
            if missing:continue
            raise
        if stat.S_ISLNK(s.st_mode):raise ValueError('ordinary root/ancestor aliases forbidden: '+str(p))
        if p!=path and not stat.S_ISDIR(s.st_mode):raise ValueError('ordinary parent must be a directory')
    return path


def digest(path):
    path=normal(path);endpoint_before=path.lstat()
    if not stat.S_ISREG(endpoint_before.st_mode):raise ValueError('regular byte input required')
    keys=('st_dev','st_ino','st_mode','st_size','st_mtime_ns','st_ctime_ns','st_nlink')
    signature=lambda info:tuple(getattr(info,k)for k in keys)
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    try:
        first=os.fstat(fd)
        if not stat.S_ISREG(first.st_mode)or signature(endpoint_before)!=signature(first):
            raise ValueError('pathname identity changed before opened byte input')
        h=hashlib.sha256();size=0
        while raw:=os.read(fd,8*2**20):h.update(raw);size+=len(raw)
        last=os.fstat(fd)
        if signature(first)!=signature(last)or size!=first.st_size:
            raise ValueError('input changed during fresh byte read')
        normal(path);endpoint_after=path.lstat()
        if not stat.S_ISREG(endpoint_after.st_mode)or signature(endpoint_after)!=signature(last):
            raise ValueError('pathname identity changed during fresh byte read')
        return h.hexdigest(),size
    finally:os.close(fd)


def require(path,expected):
    p=normal(path)
    if digest(p)[0]!=nonzero_sha(expected):raise ValueError('source-owned input bytes changed: '+str(p))
    return p


def descriptor(value):
    if type(value)is not dict or set(value)!={'path','sha256'}:
        raise ValueError('exact independently pinned descriptor required')
    return require(value['path'],value['sha256'])


def normal_module(path,expected):
    p=require(path,expected);name=p.stem;old=sys.modules.get(name)
    if old is not None:
        if getattr(old,'__file__',None)!=str(p)or getattr(old,'__spec__',None)is None or old.__spec__.origin!=str(p):
            raise ValueError('existing ordinary module has another source: '+name)
        return old
    sys.path.insert(0,str(p.parent));m=importlib.import_module(name)
    if m.__file__!=str(p)or m.__spec__ is None or m.__spec__.origin!=str(p):
        raise ValueError('ordinary import actual source differs')
    return m


def helpers(binding):
    wanted=dict(graph=GRAPH_SOURCE_SHA,codec=CODEC_SOURCE_SHA,checks=CHECK_SOURCE_SHA)
    if set(binding['helper_sources'])!=set(wanted):raise ValueError('complete three pure helpers required')
    result={}
    for key,sha in wanted.items():
        item=binding['helper_sources'][key]
        if item['sha256']!=sha:raise ValueError('reviewed helper source differs')
        result[key]=normal_module(item['path'],sha)
    return result


def api_command():
    return [PYTHON,str(API_SOURCE),'admit','--sha256',API_SEAL_SHA,
        '--terminal-evidence',str(API_TERMINAL/'terminal_return.json'),
        '--terminal-evidence-sha256',API_TERMINAL_SHA]


def intake_witness(g,binding):
    """Consume actual durable Root/result/watch/stage facts, never synthesize them.

    Root's original result retains original TMP path spellings as observations.
    Business reads are exclusively its independently pinned durable copies;
    their exact original SHA correspondence is checked without requiring a TMP
    source to remain present or turning its historical spelling into an owner.
    """
    if (binding['schema']!=SCHEMA or binding['semantics']!=SEMANTICS
        or binding['component_API_executed_in_cold_process']is not False
        or binding['production_module_identity_overlay']is not False
        or binding['science_qualification']is not False):raise ValueError('explicit new INPUT reuse contract required')
    receipt=binding['actual_bounded_api_terminal_evidence'];descriptor(receipt)
    if receipt!=dict(path=str(INTAKE_ROOT/'Root_terminal_return.json'),sha256=INTAKE_ROOT_SHA):
        raise ValueError('the independently observed durable Root bounded intake must be pinned')
    if binding['api_return']!=dict(path=str(INTAKE_ROOT/'intake/admit.log'),sha256=INTAKE_RETURN_SHA):
        raise ValueError('entire actual durable API return bytes must be retained')
    e=g.strict_json(receipt['path'],receipt['sha256']);tool=e['actual_tool']
    if (e['schema']!=WITNESS_SCHEMA or e['record_written_after_actual_tool_return']is not True
        or type(tool['exit_code'])is not int or tool['exit_code']!=0
        or type(e['actual_exit_code'])is not int or e['actual_exit_code']!=0
        or type(tool['initial_chunk_id'])is not str or not tool['initial_chunk_id']
        or type(tool['terminal_chunk_id'])is not str or not tool['terminal_chunk_id']
        or type(tool['session_id'])is not int or tool['session_id']<=0
        or e['actual_API_command']!=api_command()
        or e['actual_bounded_runtime_input_admission_observed']is not True
        or e['child_stderr_combined_into_actual_log']is not True
        or e['separate_child_stderr_observation_claimed']is not False
        or any(e[k]is not False for k in ('cold_controller_imported','cold_controller_bound','cold_prepared',
            'physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed',
            'AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('actual standalone bounded API Root EXIT0 INPUT evidence required')
    root=normal(Path(receipt['path']).parent);v=e['payload_inventory']
    if v['symlinks']!={}or type(v['files'])is not dict or len(v['files'])!=9:
        raise ValueError('complete durable intake payload inventory required')
    inventory_shape(g,root,dict(files={**v['files'],Path(receipt['path']).name:receipt['sha256']},
        directories=v['directories'],symlinks={}))
    proof=binding['intake_proof_files']
    wanted={str(root/name):sha for name,sha in v['files'].items()};wanted[receipt['path']]=receipt['sha256']
    if proof!=wanted:raise ValueError('exact entire durable intake proof map required')
    for relative,original in e['source_payload_pins'].items():
        if v['files'].get(relative)!=original['sha256']:raise ValueError('durable copies must equal every original observed payload')
    if set(e['source_payload_pins'])!=set(v['files']):raise ValueError('complete original/durable payload correspondence required')
    if e['actual_host_command']!=[PYTHON,e['source_payload_pins']['host.py']['path']]:
        raise ValueError('actual standalone host command source differs')
    if e['host_source']!=dict(path=str(root/'host.py'),sha256=v['files']['host.py']):
        raise ValueError('actual normally executed host source durable copy differs')
    result=g.strict_json(e['actual_host_result']['path'],e['actual_host_result']['sha256'])
    host_stdout=g.strict_json(e['host_stdout']['path'],e['host_stdout']['sha256'])
    if host_stdout!=result or descriptor(e['host_stderr']).stat().st_size!=0:
        raise ValueError('entire actual host stdout/result and empty host stderr required')
    watch=g.strict_json(e['actual_watchdog']['path'],e['actual_watchdog']['sha256'])
    stage_document=g.strict_json(e['actual_stage_records']['path'],e['actual_stage_records']['sha256'])
    stages=stage_document['stages']
    if (result['schema']!='AXMAT_OWNED_SPECS_STANDALONE_BOUNDED_RUNTIME_API_INTAKE_ACTUAL_HOST_V1'
        or result['producer']!=dict(path=str(API_SOURCE),sha256=API_SOURCE_SHA)
        or result['build_seal']!=dict(path=str(API_BUILD/'seal.json'),sha256=API_SEAL_SHA)
        or result['actual_run']!=dict(path=str(API_TERMINAL/'terminal_return.json'),sha256=API_TERMINAL_SHA)
        or result['actual_PREP']!=dict(path=str(API_TERMINAL/'declaration_terminal_return.json'),sha256=API_PREP_SHA)
        or result['actual_command']!=api_command()or result['watchdog']!=watch or result['stage_records']!=stages
        or type(stages)is not list or len(stages)!=1 or stages[0]['label']!='intake/admit'
        or stages[0]['status']!='PASS' or stages[0]['command']!=api_command()
        or stages[0]['log_sha256']!=e['whole_API_return']['sha256']
        or result['canonical_old_modules_only_in_isolated_process']is not True
        or result['child_stderr_combined_into_actual_log']is not True
        or result['separate_child_stderr_observation_claimed']is not False):
        raise ValueError('whole genuine standalone result/stage/watch must agree')
    if (watch['command']!=api_command()or type(watch['pid'])is not int or watch['pid']<=0
        or type(watch['returncode'])is not int or watch['returncode']!=0 or watch['limit_failure']is not None
        or watch['own_child_only']is not True or watch['liveness_group_cleanup']is not True
        or watch['rss_cap_mib']!=512 or type(watch['sampled_peak_rss_mib'])not in(int,float)
        or not 0<watch['sampled_peak_rss_mib']<512
        or type(watch['wall_cap_seconds'])not in(int,float)or not 0<watch['wall_cap_seconds']<=600
        or type(watch['elapsed_seconds'])not in(int,float)or not 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']
        or not 0<=stages[0]['elapsed_seconds']<stages[0]['wall_cap_seconds']<=600):
        raise ValueError('real isolated direct child512/600/PID/cleanup evidence required')
    for obj in (e,result):
        if (obj['total_wall_cap_seconds']!=1800 or obj['stage_wall_cap_seconds']!=600 or obj['RSS_cap_mib']!=512
            or obj['threads']!=1 or obj['children_at_once']!=1 or obj['retries']!=0
            or not 0<obj['whole_elapsed_seconds']<1800
            or any(obj[k]is not False for k in ('cold_controller_imported','cold_controller_bound','cold_prepared',
                'physics_or_native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed',
                'AAA_accuracy_qualified','ABA_admitted'))):raise ValueError('INPUT-only original bounded intake scope differs')
    if (result['actual_API_whole_return']!=e['source_payload_pins']['intake/admit.log']
        or result['actual_API_whole_merged_stream']!=result['actual_API_whole_return']
        or e['whole_API_return']!=binding['api_return']
        or e['sampled_API_child_peak_RSS_mib']!=watch['sampled_peak_rss_mib']):
        raise ValueError('full actual merged API stream identity differs')
    for key in ('actual_host_result','whole_API_return','actual_watchdog','actual_stage_records','host_source','host_stdout','host_stderr'):
        item=e[key]
        if proof.get(item['path'])!=item['sha256']:raise ValueError('actual durable fact is not explicitly owned')
    return e


def body_header(value,binding):
    if (value['schema']!=API_SCHEMA or value['admission']!='COMBINED_RUNTIME_INPUT_ONLY'
        or value['build_root']!=str(API_BUILD)or value['source_root']!=str(API_SOURCE_ROOT)
        or value['build_seal_sha256']!=API_SEAL_SHA
        or value['actual_external_terminal_evidence']!=dict(path=str(API_TERMINAL/'terminal_return.json'),sha256=API_TERMINAL_SHA)
        or value['actual_prepare_terminal_evidence']!=dict(path=str(API_TERMINAL/'declaration_terminal_return.json'),sha256=API_PREP_SHA)
        or value['component_INPUT_semantics']!='HISTORICAL_PREP_REUSE_WITH_COMPLETE_FRESH_PHASES_NOT_API_REEXECUTION'
        or value['original_component_APIs_executed_now']is not False
        or value['historical_input_graph']!=binding['complete_historical_input_graph']
        or set(value['actual_components'])!={'original92','physical','dedup','capture',
            'mathematical_controls_inherited_not_newly_executed','capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved'}
        or any(value['actual_components'][k]is not True for k in ('mathematical_controls_inherited_not_newly_executed',
            'capture_scope_is_original_operator_only','combined_runtime_RSS_not_proved'))
        or any(value[k]is not False for k in ('native_transport_executed','combined_runtime_native_RSS_proved',
            'actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('whole genuine combined API INPUT return required')
    files=value['descriptor_files'];aliases=value['input_aliases']
    if (type(files)is not dict or type(aliases)is not dict or type(binding['expected_complete_alias_count'])is not int
        or binding['expected_complete_alias_count']<=0 or len(aliases)!=binding['expected_complete_alias_count']):
        raise ValueError('complete canonical descriptor/alias maps required')
    for p,wanted in files.items():
        if not Path(p).is_absolute()or '..'in Path(p).parts:raise ValueError('canonical typed owner required')
        nonzero_sha(wanted)
    last_cprime_trim_return_admission(value)
    return files,aliases

def last_cprime_trim_return_admission(combined):
    """Validate an entire actual unit INPUT return without executing its API.

    The old seven-key body is retained, including its old operator capture.
    Those old observations provide no new trim/corrected-runtime RSS credit.
    """
    whole=combined['actual_components'];value=combined['actual_last_cprime_trim_admission']
    if (type(value)is not dict or value['schema']!=TRIM_SCHEMA
        or value['admission']!='RANK1_FACTOR_CACHE_LAST_CPRIME_TRIM_RUNTIME_INPUT_ONLY'
        or value['build_root']!=str(TRIM_BUILD)or value['source_root']!=str(TRIM_SOURCE)
        or value['build_seal_sha256']!=TRIM_SEAL_SHA
        or value['compiled_kernel']!=dict(path=str(TRIM_BUILD/'build/SPOT1P64.o'),sha256=TRIM_OBJECT_SHA)
        or value['compiled_kernel_source']!=dict(path=str(TRIM_SOURCE/'SPOT1P64.f90'),sha256=TRIM_KERNEL_SHA)
        or value['corrected_runtime']!=dict(path=str(TRIM_BUILD/'runtime/Dragon'),sha256=TRIM_RUNTIME_SHA)
        or value['actual_external_terminal_evidence']!=dict(path=str(TRIM_TERMINAL/'terminal_return.json'),sha256=TRIM_TERMINAL_SHA)
        or value['source_admission']!=dict(path=str(TRIM_SOURCE/'source_admission.json'),sha256=TRIM_SOURCE_ADMISSION_SHA)
        or value['source_patch_proof']!=value['source_admission']
        or value['inherited_rank1_factor_cache_admission']!=whole['original92']
        or value['inherited_rank1_factor_cache_memory_admission']!=whole['dedup']['inherited_rank1_factor_cache_memory_admission']
        or value['resource_scope_policy']!='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
        or value['resource_scope_contract']!=whole['original92']['resource_scope_contract']
        or any(value[k]is not True for k in ('lower_structural_zero_rows_losslessly_packed',
            'lower_repeated_blocks_losslessly_deduplicated','full_shape_MATMUL_and_RHS_order_unchanged',
            'all_original_memory_and_dictionary_controls_bitwise_passed',
            'canonical_dictionary_signed_zero_and_all_unique_fallback_verified',
            'dictionary_dimensions_indices_canonical_and_release_negative_controls_passed',
            'fresh_cold_AAA_required','fresh_512MiB_native_capture_required'))
        or any(value[k]is not False for k in ('native_RSS_proof_obtained','actual_full_FLU_entry_executed',
            'production_pipeline_prepared','AAA_accuracy_qualified','ABA_admitted'))):
        raise ValueError('entire actual trim unit INPUT identity/ancestry/scope differs')
    if (combined['compiled_trim_kernel']!=value['compiled_kernel']
        or combined['inherited_compiled_dedup_kernel']!=whole['dedup']['compiled_kernel']
        or combined['future_actual_FLU_observer_required']!=value['future_actual_FLU_observer_required']
        or combined['future_actual_factor_cache_observer_required']!=value['future_actual_factor_cache_observer_required']
        or combined['trim_component_INPUT_semantics']!=TRIM_INPUT_SEMANTICS
        or combined['trim_API_executed_in_this_consumer']is not False
        or combined['original_operator_capture_RSS_scope_not_transferred']is not True
        or combined['trim_native_RSS_proof_obtained']is not False
        or combined['fresh_trim_native_capture_required']is not True):
        raise ValueError('new selected trim object and unchanged old-capture scope required')
    item=combined['actual_last_cprime_trim_component_INPUT']
    if (item['path']!=str(Path(combined['source_root'])/'trim_component_admission_INPUT.json')
        or type(item['sha256'])is not str or re.fullmatch('[0-9a-f]{64}',item['sha256'])is None
        or item['sha256']=='0'*64 or combined['descriptor_files'].get(item['path'])!=item['sha256']
        or item['semantics']!=TRIM_INPUT_SEMANTICS
        or item['actual_component_API_called_in_this_PREP']is not True
        or item['original_historical_seven_key_body_unchanged']is not True
        or item['old_capture_RSS_transferred']is not False
        or item['trim_native_RSS_proof_obtained']is not False):
        raise ValueError('whole independently executed trim INPUT must be an explicit graph owner')
    return value


def current_trim_component_paths(g):
    """Current trim loader/thread/ordinary predicates; no producer API import.

    Historical unit files and complete SOURCE/OUT/TERM namespaces are full
    graph inputs. Its build-interpreter comparison does not apply to cold3.14.
    """
    d=g.strict_json(str(TRIM_BUILD/'declaration.json'),TRIM_DECL_SHA)
    for root in (TRIM_SOURCE,TRIM_BUILD,TRIM_TERMINAL):
        if not normal(root).is_dir():raise ValueError('actual trim ordinary namespace missing')
    for name,target in d['native_library_aliases'].items():
        if str(Path(name).resolve())!=target:raise ValueError('trim current native resolution changed')
    actual={k:v for k,v in os.environ.items()if k.startswith('DYLD_')or k=='OPENBLAS_CORETYPE'}
    wanted={k:v for k,v in d['numerical_loader_environment'].items()if k.startswith('DYLD_')or k=='OPENBLAS_CORETYPE'}
    if actual!=wanted or any(os.environ.get(k)!='1'for k in THREADS):
        raise ValueError('trim current loader/thread contract differs')
    return dict(current_trim_loader_and_threads_checked=True,
        original_build_interpreter_check_applies=False,current_cold_interpreter_has_separate_exact_contract=True,
        trim_producer_module_imported=False,trim_API_executed=False,
        trim_native_RSS_credit_inherited=False,full_trim_namespace_bytes_verified_by_complete_graph=True)


def original_ordinary_paths(g):
    """47e source predicates, explicitly derived; no provider module is imported."""
    d=g.strict_json(str(PRIOR_DECL),PRIOR_DECL_SHA)
    if len(d['files'])!=26784 or len(d['component_namespaces'])!=8:raise ValueError('original ordinary scope changed')
    for literal in d['files']:
        if not normal(literal).is_file():raise ValueError('original ordinary file missing')
    for literal,b in d['aliases'].items():
        p=Path(literal)
        if not p.is_symlink()or os.readlink(p)!=b['text']or str(p.resolve(strict=True))!=b['target']:
            raise ValueError('original literal alias changed')
        normal(b['target'])
    for row in list(d['component_namespaces'])+[dict(root=str(PRIOR_SOURCE),inventory=d['source_inventory'])]:
        root=normal(row['root']);v=row['inventory']
        if not root.is_dir()or v['symlinks']!={}:raise ValueError('original ordinary namespace changed')
        for name in v['directories']:
            if not normal(root/name).is_dir():raise ValueError('original ordinary directory missing')
        for name in v['files']:
            if not normal(root/name).is_file():raise ValueError('original ordinary member missing')
    return dict(original_ordinary_files=26784,original_literal_aliases=2,original_namespace_roots=9,
        source_owned_derivation=True,original_frozen_function_invoked=False,old16f_weak_alias_contract_unchanged=True)


def current_component_paths(g,specs):
    """0e source clauses except old producer.modules/MRO/resources.

    The build-interpreter comparison is explicitly not applicable to the
    producer3.14 cold INPUT consumer. Native/loader/thread/absence/work-inode
    predicates stay current. The genuine capture work predicate is called.
    """
    declarations={};observed=[]
    loader={k:v for k,v in os.environ.items()if k.startswith('DYLD_')or k=='OPENBLAS_CORETYPE'}
    for record in specs['reached_component_records']:
        label=record['label'];d=g.strict_json(record['declaration']['path'],record['declaration']['sha256']);declarations[label]=d
        if label=='original_capture16f':continue
        for name,target in d['native_library_aliases'].items():
            if str(Path(name).resolve())!=target:raise ValueError('original native resolution changed')
        wanted={k:v for k,v in d['numerical_loader_environment'].items()if k.startswith('DYLD_')or k=='OPENBLAS_CORETYPE'}
        if loader!=wanted or any(os.environ.get(k)!='1'for k in THREADS):raise ValueError('original current loader/threads changed')
        observed.append(label)
    capture=normal_module(CAPTURE_FACTORY,CAPTURE_FACTORY_SHA)
    physical=normal_module(PHYSICAL_FACTORY,PHYSICAL_FACTORY_SHA)
    cd=declarations['capture']
    for path,wanted in cd['native_dependency_alias_bindings'].items():
        p=Path(path)
        if not p.is_symlink()or os.readlink(p)!=wanted['text']or str(p.resolve(strict=True))!=wanted['target']:
            raise ValueError('original native dependency literal alias changed')
        capture.normal_path(wanted['target'])
    work=capture.working_snapshot_admission(cd,require_present=True)
    pd=declarations['physical'];absences=[]
    for name in pd['prior_constructor_failure_input']['missing_paths']:
        if os.path.lexists(name):raise ValueError('original failed constructor missing path appeared')
        absences.append(name)
    for root in (physical.PRIOR_GUARDED_OUT,physical.PRIOR_ABI_OUT):
        for name in ('seal.json','audit/result.json'):
            physical.absent(root/name);absences.append(str(root/name))
    cold=ART/'axial-material-production-qualified-AB-moment-order-20261006/AAA'
    if (cold/'bootstrap/result.json').exists()or list(cold.glob('map*'))!=[]:
        raise ValueError('original failed cold boundary changed')
    absences.append(str(cold/'bootstrap/result.json'))
    for case in pd['control_contract']['negative_cases']:
        path=physical.OUT/'controls'/('negative_'+case['name'])/'unexpected_return.txt'
        if path.exists():raise ValueError('original controlled-negative unexpected return appeared')
        absences.append(str(path))
    for family in ('axial-material-rank1-cache-native-angular-capture-20261007',
                   'axial-material-rank1-cache-memory-native-angular-capture-20261007'):
        path=ART/family/'seal.json'
        if path.exists():raise ValueError('original failed memory capture gained a seal')
        absences.append(str(path))
    if len(observed)!=7 or len(absences)!=24:raise ValueError('source-owned current scope differs')
    return dict(current_component_labels=observed,original_named_absences=absences,
        original_build_interpreter_check_applies=False,current_cold_interpreter_has_separate_exact_contract=True,
        genuine_capture_work_inode_path=str(work),original_component_APIs_executed=False,
        producer_modules_called=False,old_MRO_fixture_credit_inherited=False)


def source_definition(path,name):
    text=normal(path).read_text();nodes=[n for n in ast.parse(text).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name==name]
    if len(nodes)!=1:raise ValueError('one original source definition required')
    return ast.get_source_segment(text,nodes[0])


def current_cold_binding(context):
    """Actual cold sources and resource class, never old producer.modules()."""
    b=normal_module(RESOURCE_FACTORY,RESOURCE_FACTORY_SHA)
    resources=b.DynamicHistoryResources(ART,[str(p)for p in context['resource_roots']],8*2**30,96*2**30)
    snapshot=resources.check()
    if snapshot['resource_scope_policy']!=HISTORY_POLICY:raise ValueError('original complete family resource policy differs')
    current=context['runtime_context']
    if current is None:
        if context['allow_unbound_initial_INPUT_declaration']is not True:
            raise ValueError('actual current cold source context required')
        return dict(resources=snapshot,current_cold_MRO_established=False,new_binding_fixture_pass_claimed=False,
            INPUT_only_no_controller_or_transport_credit=True)
    if context['allow_unbound_initial_INPUT_declaration']is not False:raise ValueError('cold metadata phase must bind actual controller')
    runtime=normal(current['root'])
    for name in ('production_inputs','snapshot_control_preflight','qualified_snapshot_ingestion',
                 'numerical_layout_admission','rank1_factor_cache_admission','white_receiver_tracking'):
        normal_module(runtime/(name+'.py'),current['files'][name+'.py'])
    c=normal_module(runtime/'production_runner.py',current['files']['production_runner.py'])
    require(BASE_CONTROLLER,BASE_CONTROLLER_SHA)
    for name in ('SerialExecutor','qualify_aba','resource_monitor'):
        if source_definition(c.__file__,name)!=source_definition(BASE_CONTROLLER,name):
            raise ValueError('cold original Serial/qualification/resource definition changed')
    full=normal_module(FULL,FULL_SHA);guard=normal_module(GUARD,GUARD_SHA)
    if (full.OwnRSSSerialExecutor.__bases__!=(c.SerialExecutor,)or full.SerialExecutor is not c.SerialExecutor
        or full.OwnRSSSerialExecutor.__init__ is not c.SerialExecutor.__init__
        or full.OwnRSSSerialExecutor.execute is not c.SerialExecutor.execute
        or c.SerialExecutor.__init__.__code__.co_filename!=str(runtime/'production_runner.py')
        or full.OwnRSSSerialExecutor._process.__code__.co_filename!=str(FULL)):
        raise ValueError('genuine normally bound cold OwnRSS MRO differs')
    guard.guard_admission(full)  # Original tested guard remains an INPUT, not a new fixture PASS.
    resource_info=context['resource_info'];actual=c.resource_monitor(resource_info);live=actual.check()
    if type(actual)is not type(resources):raise ValueError('cold genuine dynamic resource class differs')
    return dict(resources=live,current_cold_MRO_established=True,whole_original_Serial_source_byte_exact=True,
        inherited_original_init_and_execute=True,new_binding_fixture_pass_claimed=False,
        full_79e_bind_controller_and_actual_positive_oversize_still_required=True,producer_modules_called=False)


def current_checks(h,specs,context):
    return dict(ordinary=original_ordinary_paths(h['graph']),paths=current_component_paths(h['graph'],specs),
        members=h['checks'].check_member_and_directory_predicates(h['graph'],specs,{}),
        cold_binding=current_cold_binding(context),trim_paths=current_trim_component_paths(h['graph']))

def inventory_shape(g,root,expected):
    """Original strict ordinary success namespace, files hashed in the phase."""
    root=normal(root);actual=g._scan_namespace(str(root),{})
    if (actual['files']!=set(expected['files'])or actual['directories']!=set(expected['directories'])
        or actual['symlinks']!=expected['symlinks']):raise ValueError('complete successful namespace changed')
    return actual


def complete_success_namespaces(g):
    seal=g.strict_json(str(API_BUILD/'seal.json'),API_SEAL_SHA)
    expected=dict(files={**seal['files'],'seal.json':API_SEAL_SHA},directories=seal['directories'],symlinks=seal['symlinks'])
    if expected['symlinks']!={}:raise ValueError('ordinary combined success namespace required')
    inventory_shape(g,API_BUILD,expected)
    prep=g.strict_json(str(API_TERMINAL/'declaration_terminal_return.json'),API_PREP_SHA)
    source_pin=prep['source_inventory'];source=g.strict_json(source_pin['path'],source_pin['sha256'])
    if source['symlinks']!={}:raise ValueError('ordinary actual Root SOURCE inventory required')
    inventory_shape(g,API_SOURCE_ROOT,source)
    return [(API_BUILD,expected),(API_SOURCE_ROOT,source)]


def expected_union(g,value,binding,context):
    files=dict(value['descriptor_files']);aliases=g._alias_map([dict(path=p,**row)for p,row in value['input_aliases'].items()])
    logical_edges=0
    for mapping in (binding['intake_proof_files'],context['additional_expected_files']):
        for literal,sha in mapping.items():
            nonzero_sha(sha);path=g._resolve(str(literal),aliases,kind='file')
            if path in files and files[path]!=sha:raise ValueError('canonical expected SHA ownership conflict')
            files[path]=sha;logical_edges+=1
    for item in (binding['binding_source'],binding['binding_descriptor']):
        path=g._resolve(item['path'],aliases,kind='file');sha=nonzero_sha(item['sha256'])
        if path in files and files[path]!=sha:raise ValueError('implementation expected SHA conflict')
        files[path]=sha
    return files


def post_graph_metadata(g,graph):
    """Extend original post-byte aliases/namespace/absence gates past new bytes."""
    aliases=g._alias_map(graph['aliases'])
    for path,row in aliases.items():
        if g._resolve(path,aliases,kind=row['kind'])!=row['target']:
            raise ValueError('original exact alias target changed during the extended full phase')
    for row in graph['namespaces']:
        actual=g._scan_namespace(row['root'],aliases)
        if (actual['canonical_root']!=row['canonical_root']or actual['files']!=set(row['files'])
            or actual['directories']!=set(row['directories'])
            or actual['symlinks']!={name:v['text']for name,v in row['symlinks'].items()}):
            raise ValueError('historical namespace changed during the extended full phase')
    g._absence_phase(graph['absence_inputs'],aliases,expected=graph['absence_observations'])


def complete_input_phase(binding,context,phase):
    input_guard()
    if type(phase)is not str or not phase:raise ValueError('explicit current consumption phase required')
    h=helpers(binding);g=h['graph'];intake_witness(g,binding)
    value=g.strict_json(binding['api_return']['path'],binding['api_return']['sha256'])
    body_header(value,binding);all_expected=expected_union(g,value,binding,context)
    aliases=value['input_aliases'];graph_pin=value['historical_input_graph'];del value;gc.collect()
    encoded=g.strict_json(str(SPECS),SPECS_SHA)
    specs={k:encoded['metadata'][k]for k in ('reached_component_records','independent_directory_owners',
        'remaining_source_owned_requirements','aliases')};del encoded;gc.collect()
    before=current_checks(h,specs,context);success=complete_success_namespaces(g)
    for row in binding['intake_namespaces']:inventory_shape(g,row['root'],row['inventory'])
    with g.ReadOpenAudit()as audit:
        verified=g.verify_graph(graph_pin['path'],expected_sha256=graph_pin['sha256'],phase='cold_INPUT/'+phase)
    trace=audit.snapshot();graph_reads=[r for r in trace['records']if r['kind']=='path'and r['path']==graph_pin['path']]
    regular=[r for r in trace['records']if r['kind']=='path'and r['path']!=graph_pin['path']]
    pathset={r['path']for r in regular}
    if (verified['consumer_scope']is not None or verified['graph_content_sha256']!=graph_pin['content_sha256']
        or len(regular)!=len(pathset)or len(regular)!=verified['canonical_files_read']
        or any(r['attempt_count']!=1 for r in regular)or len(graph_reads)!=1 or graph_reads[0]['attempt_count']!=1):
        raise ValueError('complete global graph must freshly open every canonical endpoint once')
    trace_digest=g._content_digest(trace);del trace,audit,regular,graph_reads;gc.collect()
    graph=g.strict_json(graph_pin['path'],graph_pin['sha256']);pins={r['path']:r for r in graph['canonical_files']}
    if (set(pins)!=pathset or len(pins)!=len(graph['canonical_files'])
        or any(all_expected.get(p)!=r['sha256']for p,r in pins.items())):
        raise ValueError('complete just-fresh canonical graph must be owned by genuine API return')
    actual_aliases={r['path']:{k:v for k,v in r.items()if k!='path'}for r in graph['aliases']}
    if actual_aliases!=aliases:raise ValueError('every original literal alias binding must stay intact')
    lengths=h['checks'].check_failed_lengths_and_owned_negative_bytes(g,specs,g._alias_map(graph['aliases']),pins)
    # Successful new bytes are not in the historical graph by design. Freshly
    # hash each distinct additional canonical endpoint once in THIS call. The
    # graph itself has just been freshly read using its external SHA witness.
    additional={p:sha for p,sha in all_expected.items()if p not in pins and p!=graph_pin['path']}
    if all_expected.get(graph_pin['path'])!=graph_pin['sha256']:raise ValueError('external graph owner missing')
    total=0
    with g.ReadOpenAudit()as extra_audit:
        for path,wanted in additional.items():
            observed,size=digest(path)
            if observed!=wanted:raise ValueError('additional canonical success/intake input changed')
            total+=size
    extra_trace=extra_audit.snapshot()
    if (any(r['kind']!='path'or r['attempt_count']!=1 for r in extra_trace['records'])
        or {r['path']for r in extra_trace['records']}!=set(additional)
        or len(extra_trace['records'])!=len(additional)or extra_trace['subprocess_records']!=[]):
        raise ValueError('every distinct additional canonical endpoint must freshly open exactly once')
    extra_trace_digest=g._content_digest(extra_trace);del extra_audit,extra_trace;gc.collect()
    for root,namespace in success:
        for relative,sha in namespace['files'].items():
            if all_expected.get(str(root/relative))!=sha:raise ValueError('whole success namespace byte member is unowned')
        inventory_shape(g,root,namespace)
    for row in binding['intake_namespaces']:
        inventory_shape(g,row['root'],row['inventory'])
        for name,sha in row['inventory']['files'].items():
            if all_expected.get(str(Path(row['root'])/name))!=sha:raise ValueError('complete intake namespace byte owner missing')
    post_graph_metadata(g,graph)
    after=current_checks(h,specs,context)
    count=len(all_expected);extra_count=len(additional)
    del graph,pins,specs,all_expected,additional,aliases,pathset;gc.collect()
    return dict(schema='AXMAT_COLD_COMPLETE_FRESH_INPUT_PHASE_V1',semantics=SEMANTICS,phase=phase,
        canonical_graph_files=verified['canonical_files_read'],canonical_graph_bytes=verified['actual_bytes_read'],
        logical_owner_edges=verified['logical_owner_requirements'],exhaustive_graph_namespaces=verified['exhaustive_namespaces_checked'],
        total_canonical_expected_files=count,additional_success_intake_bytes=total,trace_content_sha256=trace_digest,
        additional_canonical_files_freshly_read=extra_count,additional_trace_content_sha256=extra_trace_digest,
        original_failed_lengths_and_negative_bytes=lengths,current_before=before,current_after=after,
        original_component_APIs_executed_in_this_process=False,consumer_scope_used=False,
        new_binding_fixture_pass_claimed=False,science_qualification=False)


def consume_completed_inputs(binding,context,*,phase):
    """Whole unfiltered return is materialized only AFTER full phase release."""
    evidence=complete_input_phase(binding,context,phase)
    g=helpers(binding)['graph'];combined=g.strict_json(binding['api_return']['path'],binding['api_return']['sha256'])
    body_header(combined,binding);whole=combined['actual_components']
    memory=whole['dedup']['inherited_rank1_factor_cache_memory_admission']
    result=dict(original92=whole['original92'],memory438=memory,physical=whole['physical'],
        dedup=whole['dedup'],capture=whole['capture'],combined=combined)
    if (combined['inherited_rank1_cache_admission']!=result['original92']
        or combined['inherited_physical_admission']!=result['physical']
        or combined['inherited_dedup_admission']!=result['dedup']
        or combined['original_operator_capture_dependency']!=result['capture']
        or combined['inherited_rank1_factor_cache_memory_admission']!=memory):
        raise ValueError('whole nested INPUT return identities differ')
    result['last_cprime_trim']=last_cprime_trim_return_admission(combined)
    return result,evidence

def consume_metadata(data,*,phase):
    binding=data['component_input_intake'];context=data['component_current_context']
    components,evidence=consume_completed_inputs(binding,context,phase=phase)
    # The compact metadata pointer is not a filtered component return. Full
    # data are reconstructed after graph release, in the exact old field shape.
    restored=dict(data);restored['actual_components']=components
    restored['build_admission']=components['original92'];restored['combined_runtime_admission']=components['combined']
    return restored,evidence
