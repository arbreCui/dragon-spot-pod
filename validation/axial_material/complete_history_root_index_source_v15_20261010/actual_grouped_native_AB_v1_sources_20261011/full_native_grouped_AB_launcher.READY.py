"""UNREADY Root-bound CLI for the complete original grouped Native A/B workflow.

No candidate import or business work occurs at import time. A future immutable
READY copy, fresh real Root binding, independent full Source review and actual
sixteen-control gate must all exist. Source readiness grants no qualification.
The original public workflow owns all genuine build/material/monitor work.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import stat
import sys
import time

SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
READY_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
POLICY = 'FRESH_COMPLETE_CURRENT_CENSUS_TOTAL_2S_V1'
CAPS = dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,
    joint_archive_bytes=2*2**30,history_bytes=96*2**30,
    free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS',
    'VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
PYTHON = Path('/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12')
SUPPORT_PATH = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_prepare_sources/prepare_cli_host_v15.py')
SUPPORT_SHA = '3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
ADAPTER_SHA = 'd18ce676d776b674429d0c3e976466f5ab417ef4439f16f47aadef6a7ce9f50d'
CONTRACT_SHA = 'cac8532a9477824d7f68252196c74f86aaa4c06e12301836fa31976d0505f8cb'
GROUPED_UNREADY_SHA = 'ef35a10a289b99b02cd9136dbcdeed8732c02fe07e495d0af16aec27444720b7'
WORKFLOW_UNREADY_SHA = 'cd1842ec55d6f5d78ae5cffa876d03706e1c5ecc6c2c9f534a86d41d2eee7a1e'
REQUIRED_CASES = ['positive-mini-libraries','preexisting-original-object',
    'preexisting-default-pp-object','preexisting-pp-source','case-basename-collision',
    'mixed-flags','mixed-cwd','mixed-component','unmet-dependency-preflight',
    'unmet-dependency-planner','source-pin-mutation','pp-default-original-collision',
    'closed-driver-missing-object','closed-driver-extra-object',
    'closed-driver-source-mutation','second-input-syntax-error']


def require(value,message):
    if type(value) is not bool or not value:
        raise ValueError(message)


def identity(s):
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]


def pin(path,budget):
    budget();path=Path(path);before=identity(path.lstat())
    require(path.is_absolute() and '..' not in path.parts
        and all(not p.is_symlink() for p in (path,*path.parents))
        and stat.S_ISREG(before[2]) and before[3] == 1,
        'ordinary exact nonalias singlelink Source/META path')
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == before,'opened exact complete Source identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
        require(identity(os.fstat(stream.fileno())) == before,'complete EOF Source identity held')
    require(identity(path.lstat()) == before,'complete Source path identity held')
    budget()
    return dict(path=str(path),sha256=digest,size_bytes=before[4],identity=before)


def pin_shape(expected):
    require(type(expected) is dict and set(expected) == {'path','sha256','size_bytes','identity'}
        and type(expected['path']) is str and Path(expected['path']).is_absolute()
        and type(expected['sha256']) is str and len(expected['sha256']) == 64
        and all(c in '0123456789abcdef' for c in expected['sha256'])
        and type(expected['size_bytes']) is int and expected['size_bytes'] >= 0
        and type(expected['identity']) is list and len(expected['identity']) == 7
        and all(type(v) is int and v >= 0 for v in expected['identity'])
        and expected['identity'][4] == expected['size_bytes'],
        'full SHA/size and seven exact integer identity fields; no bool fields')


def recheck(expected,budget):
    pin_shape(expected)
    require(pin(expected['path'],budget) == expected,'every complete frozen Source/META pin held')


def read(raw):
    def pairs(items):
        result={}
        for key,value in items:
            require(key not in result,'no duplicate binding/review/gate key')
            result[key]=value
        return result
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda value:(_ for _ in ()).throw(ValueError(value)))


def complete_raw(expected,budget):
    recheck(expected,budget)
    with Path(expected['path']).open('rb') as stream:
        require(identity(os.fstat(stream.fileno())) == expected['identity'],'actual full-read open identity')
        raw=stream.read()
        require(identity(os.fstat(stream.fileno())) == expected['identity'],'actual full-read EOF identity')
    require(len(raw) == expected['size_bytes'] and hashlib.sha256(raw).hexdigest() == expected['sha256'],
        'complete actual Source/META bytes, no snippets or reconstructed payload')
    recheck(expected,budget)
    return raw


def metadata(expected,budget):
    return read(complete_raw(expected,budget))


def ready_inverse(ready,parent,budget,parent_sha=None,parent_size=None):
    raw=complete_raw(ready,budget);original=complete_raw(parent,budget)
    marker=("SOURCE_STATUS = '"+READY_STATUS+"'").encode('ascii')
    unready=("SOURCE_STATUS = '"+'UNREADY_SOURCE_ONLY'+"'").encode('ascii')
    require(raw.count(marker) == 1
        and raw.replace(marker,unready,1) == original
        and (parent_sha is None or parent['sha256'] == parent_sha)
        and (parent_size is None or parent['size_bytes'] == parent_size),
        'separate immutable READY Source differs only in one SourceStatus literal from exact full UNREADY parent')


def load_source(expected,name,budget):
    recheck(expected,budget)
    spec=importlib.util.spec_from_file_location(name,expected['path'])
    require(spec is not None and spec.loader is not None,'real file Source loader')
    module=importlib.util.module_from_spec(spec)
    require(name not in sys.modules,'fresh explicit Source import name')
    sys.modules[name]=module
    spec.loader.exec_module(module)
    require(Path(module.__file__).resolve() == Path(expected['path']),'exact actual loaded module Source path')
    recheck(expected,budget)
    return module


def main():
    started=time.monotonic()
    def budget():
        require(time.monotonic()-started < 1800,
            'original whole1800 includes CLI/binding/review/import/bootstrap/build/A/B and last Source closure')
    require(SOURCE_STATUS == READY_STATUS,
        'UNREADY full launcher refuses candidate imports and all Native/material action')
    parser=argparse.ArgumentParser()
    parser.add_argument('--binding',required=True)
    parser.add_argument('--binding-sha256',required=True)
    parser.add_argument('--independent-prelaunch-review',required=True)
    args=parser.parse_args();budget()
    require(not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')
        and sys.gettrace() is None and sys.getprofile() is None
        and all(os.environ.get(k) == '1' for k in THREAD_KEYS)
        and Path(sys.executable).resolve() == PYTHON
        and platform.system() == 'Darwin' and platform.machine() == 'arm64',
        'actual original nonoptimized unprofiled canonical Python/Darwin/arm64 and five single-thread values')
    sys.dont_write_bytecode=True
    binding_pin=pin(args.binding,budget)
    require(binding_pin['sha256'] == args.binding_sha256,'actual Root-bound full binding exact SHA')
    b=metadata(binding_pin,budget)
    require(b['schema'] == 'ROOT_GROUPED_COMPLETE_NATIVE_AB_SOURCE_BINDING_V1'
        and b['source_only'] is True and b['Root_only_actual_execution'] is True
        and b['actual_execution'] is None and b['policy'] == POLICY
        and b['old_controls_qualification_inherited'] is False
        and b['original_caps'] == CAPS
        and all(type(v) is int for v in b['original_caps'].values()),
        'true fresh complete Root Source binding, typed original nine caps and no inherited qualification')
    self_pin=pin(Path(__file__).absolute(),budget)
    require(self_pin == b['full_host_Source_pin'],'this exact ordinary Root-bound full host Source')
    review_pin=pin(args.independent_prelaunch_review,budget);review=metadata(review_pin,budget)
    require(review['schema'] == 'INDEPENDENT_GROUPED_COMPLETE_NATIVE_AB_SOURCE_REVIEW_V1'
        and review['source_only'] is True and review['all_checks_passed'] is True
        and review['blockers'] == [] and review['new_Source_binding_pin'] == binding_pin
        and review['full_host_Source_pin'] == self_pin
        and review['contract_entry_Source_pin'] == b['contract_entry_Source_pin']
        and review['full_workflow_Source_pin'] == b['full_workflow_Source_pin']
        and review['grouped_READY_Source_pin'] == b['grouped_READY_Source_pin']
        and review['actual_grouped_controls_gate_pin'] == b['actual_grouped_controls_gate_pin'],
        'real independent full Source review binds host/contract/immutable READY workflow/batch and actual controls')
    require(Path(binding_pin['path']).parent == Path(b['namespaces']['source'])
        and Path(self_pin['path']).parent == Path(b['namespaces']['source'])
        and Path(review_pin['path']).parent == Path(b['namespaces']['receipts']),
        'actual new full binding/host D and independent review E')
    expected=[self_pin,binding_pin,review_pin,b['full_host_UNREADY_Source_pin'],
        b['support_Source_pin'],b['adapter_Source_pin'],b['contract_entry_Source_pin'],
        b['grouped_tested_UNREADY_Source_pin'],b['grouped_READY_Source_pin'],
        b['full_workflow_UNREADY_Source_pin'],b['full_workflow_Source_pin']]
    for p in expected:recheck(p,budget)
    require(b['support_Source_pin']['path'] == str(SUPPORT_PATH)
        and b['support_Source_pin']['sha256'] == SUPPORT_SHA
        and b['adapter_Source_pin']['sha256'] == ADAPTER_SHA
        and b['contract_entry_Source_pin']['sha256'] == CONTRACT_SHA
        and b['direct_driver_batch_Source_pin'] == b['grouped_tested_UNREADY_Source_pin'],
        'fixed original support, controlled d18, actual cac public contract and tested ef35 provenance')
    ready_inverse(self_pin,b['full_host_UNREADY_Source_pin'],budget)
    ready_inverse(b['grouped_READY_Source_pin'],b['grouped_tested_UNREADY_Source_pin'],budget,
        GROUPED_UNREADY_SHA,42862)
    ready_inverse(b['full_workflow_Source_pin'],b['full_workflow_UNREADY_Source_pin'],budget,
        WORKFLOW_UNREADY_SHA,38470)
    gate_pin=b['actual_grouped_controls_gate_pin'];gate=metadata(gate_pin,budget)
    require(gate['schema'] == 'ROOT_GROUPED_DIRECT_COMPILER_SAVED_CONTROLS_V1'
        and gate['source_only'] is False and gate['all_required_controls_passed'] is True
        and gate['blockers'] == [] and gate['original_caps'] == CAPS
        and gate['tested_UNREADY_Source_pin'] == b['grouped_tested_UNREADY_Source_pin']
        and gate['actual_entry_Source_pin'] == b['contract_entry_Source_pin']
        and gate['required_case_ids'] == REQUIRED_CASES
        and gate['full_Native_build_qualified'] is False
        and gate['scientific_qualification_created'] is False,
        'actual all-sixteen-controls gate must exist before any candidate import, not a Source-only review')
    expected.append(gate_pin)
    for key in ('actual_facts_pin','actual_closed_zero_tool_return_pin',
            'actual_current_closeout_pin','independent_saved_result_review_pin',
            'actual_complete_stdout_pin','actual_complete_stderr_pin','actual_capture_tool_receipt_pin'):
        recheck(gate[key],budget);expected.append(gate[key])
    terminal=metadata(gate['actual_closed_zero_tool_return_pin'],budget)
    actual=terminal['terminal_tool_return']
    require(terminal['closed'] is True and terminal['observed_terminal'] is True
        and type(actual['exit_code']) is int and actual['exit_code'] == 0
        and 'session_id' not in actual and terminal['actual_terminal_chunk'] == actual['chunk_id']
        and actual['output'] == '',
        'genuine redirected CLOSED zero tool return with its real empty output preserved')
    capture=metadata(gate['actual_capture_tool_receipt_pin'],budget)
    require(capture['schema'] == 'ROOT_GENUINE_GROUPED16_TINY_CONTROLS_TOOL_AND_COMPLETE_CAPTURE_V1'
        and capture['actual_final_tool_return'] == actual
        and capture['actual_terminal_closed'] is True
        and capture['complete_original_stdout_available'] is True
        and capture['raw_output_truncation_preserved'] is False
        and capture['stdout_and_stderr_redirected_to_fresh_files_before_launch'] is True
        and capture['files_copied_only_after_actual_terminal_closed'] is True
        and capture['captured_streams_reconstructed'] is False
        and capture['actual_stdout_file_pin'] == gate['actual_complete_stdout_pin']
        and capture['actual_stderr_file_pin'] == gate['actual_complete_stderr_pin'],
        'actual complete redirected streams and capture receipt remain coupled to the original tool')
    raw_receipt=capture['actual_redirected_tool_receipt_pin']
    recheck(raw_receipt,budget);expected.append(raw_receipt)
    redirected=metadata(raw_receipt,budget)
    require(redirected['actual_final_tool_return'] == actual
        and redirected['actual_terminal_closed'] is True
        and redirected['fresh_redirect_paths_checked_before_launch'] is True
        and redirected['shell_noclobber_enforced'] is True,
        'actual raw prelaunch redirect receipt, no reconstructed stdout or terminal output')
    output=metadata(gate['actual_complete_stdout_pin'],budget)
    require(output['actual_facts_pin'] == gate['actual_facts_pin'],
        'full actual stdout JSON points to the exact real complete facts file')
    loaded=[]
    try:
        support=load_source(b['support_Source_pin'],'full_grouped_original_support',budget);loaded.append(b['support_Source_pin'])
        require(support.PYTHON == PYTHON and support.THREAD_KEYS == THREAD_KEYS,
            'original loaded support agrees with fixed canonical Python and thread environment')
        runtime=load_source(b['adapter_Source_pin'],'full_grouped_controlled_d18_runtime',budget);loaded.append(b['adapter_Source_pin'])
        contract=load_source(b['contract_entry_Source_pin'],'full_grouped_actual_cac_contract',budget);loaded.append(b['contract_entry_Source_pin'])
        batch=load_source(b['grouped_READY_Source_pin'],'full_grouped_immutable_READY_batch',budget);loaded.append(b['grouped_READY_Source_pin'])
        workflow=load_source(b['full_workflow_Source_pin'],'full_grouped_immutable_READY_workflow',budget);loaded.append(b['full_workflow_Source_pin'])
        require(runtime.CAPS == CAPS and contract.CAPS == CAPS and batch.CAPS == CAPS and workflow.CAPS == CAPS
            and runtime.SOURCE_STATUS == 'UNREADY_SOURCE_ONLY'
            and contract.SOURCE_STATUS == 'UNREADY_SOURCE_ONLY'
            and batch.SOURCE_STATUS == READY_STATUS and workflow.SOURCE_STATUS == READY_STATUS
            and contract.CONTROL_ORDER_GROUPED == tuple(REQUIRED_CASES),
            'exact immutable Source roles and original caps, no runtime status mutation')
        for p in expected:recheck(p,budget)
        budget()
        workflow.run_workflow(runtime,contract,b,binding_pin,review_pin,started,support,batch)
        budget()
    finally:
        # The workflow publishes only evidence. Final launcher failure keeps
        # actual tool EXIT nonzero; no result/Source repair or rerun is allowed.
        for p in loaded:recheck(p,budget)
        for p in expected:recheck(p,budget)
        require(pin(Path(__file__).absolute(),budget) == self_pin,'full host Source held through final closure')
        budget()


if __name__ == '__main__':
    main()
