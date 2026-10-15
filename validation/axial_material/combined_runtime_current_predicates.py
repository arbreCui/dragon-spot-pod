"""Actual current-only predicate subset; no complete API replacement claim.

All modules are normally imported from their actual immutable formal sources.
Original globals, classes and environment functions remain untouched. This
readonly measurement deliberately reports incomplete production closure.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path('/Users/wen/spot')
ART = ROOT / 'validation/artifacts'
FACTORY = ROOT / 'validation/axial_material/prepare_combined_physical_dedup_file_snapshot_runtime_build.py'
FACTORY_SHA = 'bf4692a57209ace55e22f85c6e9ffabf80850dcb1b610348e7dc97b74a80040c'
SPECS = Path('/private/tmp/combined_runtime_source_owned_typed_input_specs_draft_20261007.json')
SPECS_SHA = 'c9c7414f71ac6f857d8f8dcf959cd558ea2bd26b6fb137ed28870f95473da2d6'
HELPER = Path('/private/tmp/combined_runtime_complete_input_graph_mechanics_stopped_draft_20261007.py')
HELPER_SHA = 'c8e58bcad7b9f4a6b1d6615050d41854397c4d102efd2af81b402b376827bb44'
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')


def actual_module(path, wanted, name):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == wanted
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert Path(m.__file__).resolve() == path and Path(m.__spec__.origin).resolve() == path
    return m


def check_current_predicate_subset(g, specs, provider, *, require_build_interpreter):
    if type(require_build_interpreter) is not bool:
        raise ValueError('explicit build-interpreter policy required')
    b, h, full, c = provider.modules()
    assert full.OwnRSSSerialExecutor.__bases__ == (c.SerialExecutor,)
    assert Path(full.__file__).resolve() == h.FULL_SOURCE
    declarations = {}
    observed = []
    actual_loader = {k: v for k, v in os.environ.items() if k.startswith('DYLD_') or k == 'OPENBLAS_CORETYPE'}
    for record in specs['reached_component_records']:
        label = record['label']
        d = g.strict_json(record['declaration']['path'], record['declaration']['sha256'])
        declarations[label] = d
        # 619.capture_admission verifies the old16f bytes directly; it does not
        # call that older capture factory's environment as a current API.
        if label == 'original_capture16f':
            continue
        if require_build_interpreter:
            assert str(Path(sys.executable).resolve()) == d['build_python_executable']
        for name, target in d['native_library_aliases'].items():
            assert str(Path(name).resolve()) == target
        wanted_loader = {k: v for k, v in d['numerical_loader_environment'].items()
                         if k.startswith('DYLD_') or k == 'OPENBLAS_CORETYPE'}
        assert actual_loader == wanted_loader
        assert all(os.environ.get(k) == '1' for k in THREAD_KEYS)
        observed.append(dict(owner=record['declaration'], checks='CURRENT_INTERPRETER_NATIVE_RESOLUTION_LOADER_THREADS',
                             interpreter_policy=require_build_interpreter))
    capture = provider.load(provider.CAPTURE_FACTORY, provider.CAPTURE_FACTORY_SHA,
                            'actual_readonly_current_capture_topology_predicate')
    physical = provider.load(provider.PHYSICAL_FACTORY, provider.PHYSICAL_FACTORY_SHA,
                             'actual_readonly_current_physical_absence_predicates')
    cd = declarations['capture']
    for path, wanted in cd['native_dependency_alias_bindings'].items():
        p = Path(path)
        assert p.is_symlink() and os.readlink(p) == wanted['text']
        assert str(p.resolve(strict=True)) == wanted['target']
        capture.normal_path(wanted['target'])
    work = capture.working_snapshot_admission(cd, require_present=True)
    # Genuine original function checks independent regular/noalias/nlink1 and
    # not-samefile with all three original candidate/parent snapshot paths.
    observed.append(dict(owner='genuine capture.working_snapshot_admission', path=str(work),
                         stat_nlink=work.stat().st_nlink, actual_original_function_called=True))
    pd = declarations['physical']
    absence_results = []
    for name in pd['prior_constructor_failure_input']['missing_paths']:
        assert not os.path.lexists(name)
        absence_results.append(dict(path=name, predicate='os.path.lexists == False',
                                   source_owner='physical.prior_constructor_failure_input'))
    for root, owner in ((physical.PRIOR_GUARDED_OUT, 'physical.prior_signature_failure_input'),
                        (physical.PRIOR_ABI_OUT, 'physical.prior_resource_observation_failure_input')):
        for name in ('seal.json', 'audit/result.json'):
            physical.absent(root / name)
            absence_results.append(dict(path=str(root/name), predicate='genuine physical.absent', source_owner=owner))
    cold_result = b.COLD / 'AAA/bootstrap/result.json'
    assert not cold_result.exists()
    actual_maps = list((b.COLD / 'AAA').glob('map*'))
    assert actual_maps == []
    absence_results.append(dict(path=str(cold_result), predicate='Path.exists == False', source_owner='old92.cold_failure_admission'))
    observed.append(dict(owner='old92.cold_failure_admission', glob_root=str(b.COLD/'AAA'), pattern='map*', actual_matches=[]))
    for case in pd['control_contract']['negative_cases']:
        path = physical.OUT / 'controls' / ('negative_' + case['name']) / 'unexpected_return.txt'
        assert not path.exists()
        absence_results.append(dict(path=str(path), predicate='Path.exists == False', source_owner='physical.control_audit'))
    # Literal roots are the exact two original readonly failure-function names;
    # do not import their old failed declarations or arbitrary nested manifests.
    for family, owner in (
        ('axial-material-rank1-cache-native-angular-capture-20261007', 'memory.failed_capture_admission'),
        ('axial-material-rank1-cache-memory-native-angular-capture-20261007', 'dedup.failed_memory_capture_admission')):
        path = ART/family/'seal.json'
        assert not path.exists()
        absence_results.append(dict(path=str(path), predicate='Path.exists == False', source_owner=owner))
    resources = provider.resources_for([str(p) for p in b.history_roots([], ART)], c.ResourceFailure)
    snapshot = resources.check()
    return dict(observed_predicates=observed, named_absence_predicates=absence_results,
                actual_live_resources=snapshot, all_remaining_production_predicates_accounted=False,
                complete_raw_negative_member_sets_checked=False,
                complete_failed_namespaces_and_original_file_sizes_checked=False,
                current_constructor_for_new_business_family_exercised=False,
                no_module_global_or_identity_overlay=True, original_component_API_reexecuted=False,
                complete_parent_predicate_replacement_proved=False, new_business_contract_READY=False,
                combined_runtime_admitted=False, science_qualification_created=False,
                AAA_accuracy_qualified=False, ABA_admitted=False)


def main():
    started = time.monotonic()
    assert str(Path(sys.executable).resolve()) == '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
    assert all(os.environ.get(k) == '1' for k in THREAD_KEYS)
    g = actual_module(HELPER, HELPER_SHA, 'actual_current_predicate_readonly_strict_metadata_reader')
    specs = g.strict_json(str(SPECS), SPECS_SHA)
    provider = actual_module(FACTORY, FACTORY_SHA, 'actual_current_predicate_genuine_module_provider')
    result = check_current_predicate_subset(g, specs, provider, require_build_interpreter=True)
    result.update(schema='AXMAT_COMBINED_RUNTIME_CURRENT_ONLY_SUBSET_ACTUAL_READONLY_MEASUREMENT_V1',
                  typed_specs=dict(path=str(SPECS), sha256=SPECS_SHA), elapsed_seconds=time.monotonic()-started)
    out = Path('/private/tmp/combined_runtime_current_only_predicate_subset_measurement_result_20261007.json')
    with out.open('x') as f:
        json.dump(result, f, indent=2, allow_nan=False)
        f.write('\n')
    print(json.dumps(dict(observed_predicates=len(result['observed_predicates']),
        named_absence_predicates=len(result['named_absence_predicates']),
        elapsed_seconds=result['elapsed_seconds'], READY=False,
        output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())))


if __name__ == '__main__':
    main()
