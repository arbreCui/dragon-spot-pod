"""STOPPED diagnostic wrapper: one actual input admission, never a build/audit/API.

The profiling hook sees Python events but emits only whole-function boundaries.
Its overhead remains inside the original limits. RUSAGE_SELF is a high-water
allocation observation, not a live RSS sample or a causal attribution.
"""
import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import resource
import sys
import time
STARTED = time.monotonic()
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')


def load_config(path, expected):
    payload = Path(path).read_bytes()
    if hashlib.sha256(payload).hexdigest() != expected:
        raise ValueError('external diagnostic config SHA differs')
    value = json.loads(payload)
    if (value['schema'] != 'AXMAT_TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC_CONFIG_V1'
        or value['status'] != 'READY_ROOT_REVIEWED_INPUT_DIAGNOSTIC_ONLY'):
        raise ValueError('UNREADY: stopped source diagnostic, no execution authorized by config')
    if value['caps'] != dict(total_wall_seconds=1800,stage_wall_seconds=600,rss_mib=512,
        archive_bytes=2*2**30,history_bytes=96*2**30,min_free_bytes=8*2**30,
        threads=1,children=1,retries=0):
        raise ValueError('original diagnostic limits differ')
    return value


def require_small_source(descriptor):
    path = Path(descriptor['path'])
    if not path.is_absolute() or path.is_symlink() or path.resolve(strict=True) != path:
        raise ValueError('ordinary canonical diagnostic source required')
    if hashlib.sha256(path.read_bytes()).hexdigest() != descriptor['sha256']:
        raise ValueError('diagnostic source SHA differs')
    return path


def normal_factory(descriptor):
    path = require_small_source(descriptor)
    name = path.stem
    prior = sys.modules.get(name)
    if prior is not None and Path(prior.__file__).resolve() != path:
        raise ValueError('foreign pre-existing canonical producer binding')
    sys.path.insert(0,str(path.parent))
    module = importlib.import_module(name)
    if (Path(module.__file__).resolve() != path or module.__spec__ is None
        or Path(module.__spec__.origin).resolve() != path or module.__name__ != name):
        raise ValueError('actual normal producer import differs')
    require_small_source(descriptor)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',required=True)
    parser.add_argument('--config-sha256',required=True)
    args = parser.parse_args()
    if sys.flags.optimize != 0 or os.environ.get('PYTHONOPTIMIZE'):
        raise ValueError('nonoptimized Python required before project reads')
    if any(os.environ.get(key) != '1' for key in THREAD_KEYS):
        raise ValueError('five single-thread bindings required')
    if sys.platform != 'darwin':
        raise ValueError('Darwin RUSAGE_SELF raw byte unit required')
    sys.dont_write_bytecode = True
    config = load_config(args.config,args.config_sha256)
    if str(Path(sys.executable).resolve()) != config['python_executable']:
        raise ValueError('actual original build Python3.12 required')
    require_small_source(config['child_source'])
    if Path(__file__).resolve() != Path(config['child_source']['path']):
        raise ValueError('actual child source binding differs')
    for descriptor in config['profile_source_files'].values():
        require_small_source(descriptor)
    factory = normal_factory(config['factory'])
    selected = {(entry['path'],name) for entry in config['profile_markers'] for name in entry['functions']}
    counts = {}
    emitted = 0
    suppressed = 0
    maximum_events = config['maximum_boundary_events']
    if type(maximum_events) is not int or maximum_events != 1024:
        raise ValueError('fixed bounded whole-function marker count required')

    def profile(frame,event,arg):
        nonlocal emitted,suppressed
        if event not in ('call','return'):
            return
        filename = frame.f_code.co_filename
        function = frame.f_code.co_name
        if (filename,function) not in selected:
            return
        # Only immutable names, integer counters and scalar observations survive.
        # The frame, arg, return object, locals and code object are never retained.
        key = filename + ':' + function + ':' + event
        counts[key] = counts.get(key,0) + 1
        if emitted >= maximum_events:
            suppressed += 1
            return
        raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        record = dict(schema='AXMAT_INPUT_FUNCTION_ALLOCATION_BOUNDARY_V1',event=event,
            source_path=filename,function=function,monotonic_seconds=time.monotonic(),
            elapsed_seconds=time.monotonic()-STARTED,ru_maxrss_raw_bytes=raw,
            ru_maxrss_mib=raw/2**20,ru_maxrss_unit='DARWIN_BYTES',
            function_return_event_is_not_a_success_assertion=True)
        print('AXMAT_INPUT_BOUNDARY ' + json.dumps(record,allow_nan=False,separators=(',',':')),flush=True)
        emitted += 1

    completed = False
    sys.setprofile(profile)
    try:
        # Real immutable function body, original true build-interpreter branch.
        declaration = factory.declaration_admission(config['declaration']['sha256'], True,
            prep_sha256=config['actual_PREP']['sha256'])
        del declaration
        completed = True
    finally:
        sys.setprofile(None)
        raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print('AXMAT_INPUT_PROFILE_STOP ' + json.dumps(dict(
            actual_input_admission_returned=completed,boundary_events=emitted,
            suppressed_boundary_events=suppressed,profile_disabled=True,
            ru_maxrss_raw_bytes=raw,ru_maxrss_mib=raw/2**20),allow_nan=False),flush=True)
    # No business calls occur after the hook is disabled.
    result = dict(schema='AXMAT_TRIM_V5_INPUT_ALLOCATION_DIAGNOSTIC_CHILD_V1',
        classification='COMPLETE_INPUT_ADMISSION_ALLOCATION_DIAGNOSTIC_ONLY',
        actual_input_admission_returned=True,actual_true_build_interpreter_branch=True,
        actual_call='declaration_admission(DECLSHA, True, prep_sha256=PREPSHA)',
        factory=config['factory'],declaration=config['declaration'],actual_PREP=config['actual_PREP'],
        boundary_event_counts=counts,boundary_events=emitted,suppressed_boundary_events=suppressed,
        boundary_trace_complete_for_selected_functions=(suppressed == 0),profile_disabled=True,
        whole_elapsed_seconds=time.monotonic()-STARTED,
        ru_maxrss_raw_bytes=raw,ru_maxrss_mib=raw/2**20,ru_maxrss_unit='DARWIN_BYTES',
        genuine_constructor_preflight_in_true_original_call=True,
        profiling_overhead_is_inside_limits=True,normal_performance_measurement_claimed=False,
        live_RSS_time_series_claimed=False,allocation_cause_proved=False,
        audit_build_executed=False,production_admission_executed=False,new_build_seal_admitted=False,
        native_or_numerical_child_executed=False,cold_prepared=False,
        combined_runtime_native_RSS_proved=False,AAA_accuracy_qualified=False,ABA_admitted=False)
    target = Path(config['result_path'])
    if target.parent != Path(config['base'])/'diagnostic':
        raise ValueError('fixed diagnostic result path required')
    with target.open('x') as stream:
        json.dump(result,stream,allow_nan=False,sort_keys=True,indent=2)
        stream.write('\n')
    print('AXMAT_INPUT_DIAGNOSTIC_COMPLETE ' + json.dumps(result,allow_nan=False),flush=True)


if __name__ == '__main__':
    main()
