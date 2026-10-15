"""Fresh environment-pinned declaration; preserve the rejected prototype.

The frozen layout factory and every mathematical admission rule are retained.
Only exact offline replay gains an explicit interpreter/library/thread guard.
No transport is launched by this preparation helper.
"""
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import sysconfig

sys.dont_write_bytecode = True
import numpy as np
import prepare_qualified_AB_white_trace_refined_production as factory

SOURCE = factory.ART / 'axial-material-qualified-AB-white-trace-refined-envpin-admission-20261005'
OUTPUT = factory.ART / 'axial-material-production-qualified-AB-white-trace-refined-envpin-20261005'
THREADS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
           'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
FACTORY = Path(factory.__file__).resolve()
FACTORY_SHA = '801a5985c3b50b232368821f3113972dd5b7bd14b39f9c88ad4073bee912b77b'
FAILED = factory.SOURCE
FAILURE_SHA = '2c7592894e5aea2f1426faddda6ef979f2425c531e88ce1646bf20d637ab4de0'
FAILED_DECL_SHA = '886eab28527f2d91a169d3fb1e1ba7eb68e2bfed7789ae988ee79c2295c704ea'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require(path, wanted):
    if digest(path) != wanted:
        raise ValueError('environment factory/evidence changed: ' + str(path))


def environment():
    executable = Path(sys.executable).resolve()
    numpy_root = Path(np.__file__).parent.resolve()
    library = Path(sysconfig.get_config_var('PYTHONFRAMEWORKPREFIX')) / sysconfig.get_config_var('LDLIBRARY')
    if (platform.python_version() != '3.14.4' or np.__version__ != '2.4.4'
            or str(executable) != '/opt/homebrew/Cellar/python@3.14/3.14.4_1/Frameworks/Python.framework/Versions/3.14/bin/python3.14'
            or any(os.environ.get(k) != '1' for k in THREADS)):
        raise ValueError('original exact-replay environment and explicit single threads required')
    require(FACTORY, FACTORY_SHA)
    require(FAILED / 'preflight_failure_record.json', FAILURE_SHA)
    require(FAILED / 'declaration.json', FAILED_DECL_SHA)
    paths = [executable, library.resolve(), FACTORY, FAILED / 'preflight_failure_record.json',
             FAILED / 'declaration.json']
    paths += sorted(p.resolve() for p in numpy_root.rglob('*')
                    if p.is_file() and p.suffix in ('.py', '.so', '.dylib'))
    return dict(schema='AXMAT_EXACT_OFFLINE_REPLAY_ENVIRONMENT_V1',
        executable=str(executable), python_version=platform.python_version(),
        numpy_version=np.__version__, numpy_root=str(numpy_root),
        thread_environment={k: '1' for k in THREADS},
        files={str(p): digest(p) for p in paths},
        scope='Version and thread admission applies to exact offline producer numerical replay. '
              'Independent CE analysis may use its separately frozen environment; all shared '
              'metadata checks still verify these dependency bytes.',
        original_exact_dictionary_comparison_changed=False,
        original_numerical_rules_changed=False,
        failed_prototype_preserved=True, transport_started=False)


ENVIRONMENT_GUARD = '''
import os
import platform
import sys


def verify_analysis_dependencies():
    for name,wanted in ANALYSIS_ENVIRONMENT["files"].items():
        require(name,wanted)


def verify_analysis_environment():
    import numpy as np
    if (str(Path(sys.executable).resolve()) != ANALYSIS_ENVIRONMENT["executable"]
            or platform.python_version() != ANALYSIS_ENVIRONMENT["python_version"]
            or np.__version__ != ANALYSIS_ENVIRONMENT["numpy_version"]
            or str(Path(np.__file__).parent.resolve()) != ANALYSIS_ENVIRONMENT["numpy_root"]
            or any(os.environ.get(k) != v for k,v in ANALYSIS_ENVIRONMENT["thread_environment"].items())):
        raise ValueError("exact offline replay environment differs from its declaration")
    verify_analysis_dependencies()
    return dict(status="PASS_EXACT_OFFLINE_REPLAY_ENVIRONMENT",python=platform.python_version(),
                numpy=np.__version__,dependency_files=len(ANALYSIS_ENVIRONMENT["files"]))
'''
INGESTION_ANCHOR = 'def verify_offline_state(state):\n'
INGESTION_GUARD = ('def verify_offline_state(state):\n'
                   '    from numerical_layout_admission import verify_analysis_environment\n'
                   '    verify_analysis_environment()\n')


def main():
    env = environment()
    original_patch = factory.patch_text

    def guarded_patch(original, replacements):
        result = original_patch(original, replacements)
        if INGESTION_ANCHOR in result:
            guarded = original_patch(result, [(INGESTION_ANCHOR, INGESTION_GUARD)])
            if guarded.replace(INGESTION_GUARD, INGESTION_ANCHOR, 1) != result:
                raise ValueError('mathematical replay body changed')
            factory.angular.mesh.base.write_new(SOURCE / 'analysis_environment.json', env)
            factory.angular.mesh.base.write_new(SOURCE / 'environment_source_equivalence.json', dict(
                status='PASS_ONLY_EXPLICIT_ENVIRONMENT_GUARD_ADDED',
                frozen_factory=dict(path=str(FACTORY), sha256=FACTORY_SHA),
                original_ingestion_body_restored_byte_exact=True,
                original_exact_comparison_and_negative_controls_retained=True,
                original_controller_and_scientific_rules_changed=False,
                prior_failed_declaration=dict(path=str(FAILED / 'declaration.json'),sha256=FAILED_DECL_SHA),
                prior_failure=dict(path=str(FAILED / 'preflight_failure_record.json'),sha256=FAILURE_SHA),
                AAA_accuracy_qualified=False, ABA_admitted=False, transport_started=False))
            return guarded
        return result

    original_layout = factory.LAYOUT_HOST
    layout = original_patch(original_layout, [(
        'def admit_layout_variant(variant):\n',
        'def admit_layout_variant(variant):\n    verify_analysis_dependencies()\n')])
    layout += '\nANALYSIS_ENVIRONMENT = ' + repr(env) + '\n' + ENVIRONMENT_GUARD
    factory.SOURCE, factory.OUTPUT = SOURCE, OUTPUT
    factory.EXPERIMENT = 'axial-material-qualified-AB-rank1-white-trace-refined-envpin-20261005'
    factory.LAYOUT_HOST = layout
    factory.patch_text = guarded_patch
    # The factory pins __file__ into both its variant and declaration. Bind this
    # wrapper there; the frozen factory itself is bound in the dependency set.
    factory.__file__ = str(Path(__file__).resolve())
    factory.main()


if __name__ == '__main__':
    main()
