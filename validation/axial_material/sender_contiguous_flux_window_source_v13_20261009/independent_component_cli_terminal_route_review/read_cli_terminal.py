"""Pure readonly source/JSON inspection, no business module imports or calls."""
import ast, hashlib, json
from pathlib import Path
D=Path('/private/tmp/axmat_v13_cli_terminal_source_route_readonly_20261009')
P=Path('/private/tmp/axmat_v13_full_sender_window_component_READY_source_candidates_20261009')
F=P/'prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
Q=P/'Root_pending_actual_prepare_command.json'
A=Path('/private/tmp/axmat_v13_full_sender_window_component_source_draft_20261009/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert digest(F)=='d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
assert digest(Q)=='4a92c4ec8a4607c6cb86d7f6ed51e0076026433e174fb630ae0ee2a5b9230b7b'
assert digest(A)=='a6dd0796316aec5b6c16ff73677c689a7e7146697759a0cde9187be962807821'
s=F.read_text();tr=ast.parse(s);p=json.loads(Q.read_text());mother=A.read_text();mt=ast.parse(mother)
assert sorted(ast.get_source_segment(s,n) for n in ast.walk(tr) if isinstance(n,ast.FunctionDef))==sorted(ast.get_source_segment(mother,n) for n in ast.walk(mt) if isinstance(n,ast.FunctionDef))
defs=[n for n in ast.walk(tr) if isinstance(n,ast.FunctionDef)];assert len(defs)==96
values={}
def literal(n):
    if isinstance(n,ast.Name):return values[n.id]
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Path' and len(n.args)==1 and not n.keywords:
        return Path(ast.literal_eval(n.args[0]))
    if isinstance(n,ast.Attribute) and n.attr=='parent':return literal(n.value).parent
    if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Div):return literal(n.left)/literal(n.right)
    return ast.literal_eval(n)
for n in tr.body:
    if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
        try:values[n.targets[0].id]=literal(n.value)
        except (ValueError,KeyError,TypeError):pass
factory='/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py'
parent=json.loads((values['PARENT']/'declaration.json').read_text())
python=parent['build_python_executable']
assert python=='/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
flags={
 '--rank1-cache-build-seal-sha256':values['PARENT_SEAL'],
 '--rank1-cache-terminal-evidence':str(values['PARENT_TERMINAL']/'terminal_return.json'),
 '--rank1-cache-terminal-evidence-sha256':values['PARENT_TERMINAL_SHA'],
 '--failed-capture-terminal-evidence-sha256':values['FAILED_CAPTURE_TERMINAL_SHA'],
 '--memory-build-seal-sha256':values['MEMORY_SEAL_SHA'],
 '--memory-terminal-evidence':str(values['MEMORY_TERMINAL']/'terminal_return.json'),
 '--memory-terminal-evidence-sha256':values['MEMORY_TERMINAL_SHA'],
 '--failed-memory-capture-terminal-evidence-sha256':values['FAILED_MEMORY_CAPTURE_TERMINAL_SHA'],
 '--patch-helper-sha256':values['PATCH_HELPER_SHA'],
 '--controls-source-sha256':values['CONTROL_SOURCE_SHA'],
}
expected=[python,factory,'prepare-build',*[x for k,v in flags.items() for x in (k,v)]]
assert p['command']==expected
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    assert p['environment'][key]=='1'
assert parent['numerical_loader_environment']=={}
assert p['business_execution_performed'] is False
assert p['source_candidate']==dict(path=str(F),sha256=digest(F))
assert values['TAIL_FIELDS']==('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
assert values['SOURCE_STATUS']=='READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_COMPONENT_EXECUTION'
for name in ('FUTURE_ACTUAL_BUILD_TERMINAL_SHA','FUTURE_ACTUAL_BUILD_SEAL_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):
    assert values[name] is None
required_inputs={}
for name in ('SENDER_FACTORY_SOURCE_PARENT','SENDER_PATCH_HELPER','CANDIDATE_SENDER_SOURCE','SENDER_SOURCE_PROOF','SENDER_SOURCE_INPUT',
             'SENDER_CONTROL_SOURCE','SENDER_CONTROL_CONTRACT','SENDER_CONTROLS_AUDITOR'):
    sha_name='CANDIDATE_SENDER_SHA' if name=='CANDIDATE_SENDER_SOURCE' else name+'_SHA'
    # The remaining names already have the exact _SHA suffix except source controls.
    if name=='SENDER_FACTORY_SOURCE_PARENT':sha_name='SENDER_FACTORY_SOURCE_PARENT_SHA'
    path=values[name];wanted=values[sha_name]
    exists=path.is_file() and not path.is_symlink()
    required_inputs[name]=dict(path=str(path),expected_sha256=wanted,currently_regular_file=exists,
        current_sha256=digest(path) if exists else None)
    if exists:assert required_inputs[name]['current_sha256']==wanted,name
canonical_factory=Path(factory)
roots={name:dict(path=str(values[name]),exists_at_readonly_snapshot=values[name].exists()) for name in ('SOURCE','OUT','TERMINAL')}
schema=values['TERMINAL_SCHEMA'];term=values['TERMINAL']
template=dict(schema=schema,record_producer='root',actual_tool_terminal_return_observed=True,
    record_written_after_actual_terminal_return=True,returncode=0,
    command=[python,factory,'run-build','--sha256','<ACTUAL_NEW_DECLARATION_SHA256>'],
    source=dict(path=factory,sha256=digest(F)),
    declaration=dict(path=str(values['OUT']/'declaration.json'),sha256='<ACTUAL_NEW_DECLARATION_SHA256>'),
    build_seal=dict(path=str(values['OUT']/'seal.json'),sha256='<ACTUAL_NEW_BUILD_SEAL_SHA256>'),
    full_stdout=dict(path=str(term/'run.stdout'),sha256='<SHA_OF_COMPLETE_ACTUAL_STDOUT>'),
    full_stderr=dict(path=str(term/'run.stderr'),sha256='<SHA_OF_COMPLETE_ACTUAL_STDERR>'),
    actual_tail_check='<COPY_EXACT_RETURNED_actual_tail_check>',
    actual_elapsed_seconds='<COPY_EXACT_RETURNED_actual_elapsed_seconds>',
    actual_archive_bytes='<COPY_EXACT_RETURNED_actual_archive_bytes>',
    actual_resources='<COPY_EXACT_RETURNED_actual_resources>')
report=dict(schema='AXMAT_V13_COMPONENT_CLI_AND_EXTERNAL_TERMINAL_PURE_SOURCE_ROUTE_REVIEW_V1',
    status='PASS_STATIC_ARGV_AND_TERMINAL_ROUTE_NO_BUSINESS_EXECUTION',
    candidate=dict(path=str(F),sha256=digest(F)),pending_plan=dict(path=str(Q),sha256=digest(Q)),
    actual_prepare_command_plan_checked=expected,
    actual_prepare_stdout_shape=dict(declaration='<absolute OUT/declaration.json>',declaration_sha256='<actual declaration SHA>',source_root='<SOURCE>',classification='DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_ONLY_V13'),
    run_command_plan=[python,factory,'run-build','--sha256','<ACTUAL_NEW_DECLARATION_SHA256>'],
    admit_command_plan=[python,factory,'admit','--sha256','<ACTUAL_NEW_BUILD_SEAL_SHA256>',
        '--terminal-evidence',str(term/'terminal_return.json'),'--terminal-evidence-sha256','<ACTUAL_ROOT_RECEIPT_SHA256>'],
    full_external_terminal_template_not_actual_evidence=template,
    terminal_generation_sequence=[
        'Install exact canonical reviewed source + driver + full contract; required source pins must match.',
        'PREP requires SOURCE/OUT/TERMINAL all absent. Retain PREP streams outside these three roots.',
        'Read actual prepare stdout wrapper and exact OUT/declaration SHA. Only then create independent TERMINAL to retain direct actual RUN fullstdout/stderr.',
        'Observe actual typed exec terminal integer exit0 and closed job. A seal alone never supplies success.',
        'Parse full actual stdout as one strict finite JSON object; returned.result must equal sealed driver_result.json exactly.',
        'Copy all four returned tail values unchanged; do not reconstruct/recalculate them from elapsed tool time or a later resources snapshot.',
        'Write canonical terminal_return.json only after observed close, retaining separate fullstdout/fullstderr regular files in TERM.',
        'Run admit with actual sealSHA, canonical Root receipt absolute path and actual receiptSHA; no numerical/native launch is implied.'
    ],
    external_terminal_exactness=[
        'source/declaration/build_seal/fullstdout/fullstderr descriptors must have exactly path+sha256; adding bytes to these descriptors would fail equality.',
        'receipt must be TERM/terminal_return.json; stdout and stderr must be separate regular files directly inside TERM and distinct from each other and receipt.',
        'no path or ancestor may be symlink; paths canonical absolute, no ..; entire terminal JSON rejects duplicate/nonfinite keys/numbers.',
        'receipt sourceSHA must equal canonical executed sourceSHA and its declaration.files binding, command exact P12 business argv.',
        'actual_stdout == {result: sealed_driver_result, fourtails}; receipt fourtails must equal returned fourtails exactly.',
        'tail_check PASS; driver.elapsed <= returned.elapsed <1800; actual archive integer <2GiB and exact current SOURCE+OUT bytes.',
        'resources original96GiB/free8GiB, policy/contract/declared roots exact, dynamic union includes all declared roots, artifact bytes >=SOURCE+OUT, free >=8GiB, ordinary files>=1, finite positive checked_unix.',
        'Do not add/change any SOURCE/OUT file after successful fulltail; it would change the exact archive/namespace/seal.'
    ],
    original_cache_cli_SHA_flags_correct_not_sender_SHA_flags=True,
    all96_function_definitions_byteexact_to_a6dd=True,
    source_input_snapshot=required_inputs,three_roots_readonly_snapshot=roots,
    canonical_factory_currently_installed=canonical_factory.is_file(),
    necessary_environment=dict(threads={k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')},
        numerical_loader_environment={},forbidden_ambient_dispatch_keys='Any DYLD_* or OPENBLAS_CORETYPE must be absent to match original {}.',PYTHONOPTIMIZE='unset'),
    planned_stage_outcomes=dict(total=86,PASS=62,expected_FAILED=24,keycodec_expected_rc23=20,sender_expected_rc1=4,
        expected_rejections_do_not_turn_failed_status_into_PASS=True),
    deterministic_code_or_argv_blockers_found=[],
    scope='Pure source/pending argv review only. Canonical installation dependencies are reported, not presumed performed; no actual build/intake/native result exists.',
    business_modules_imported=False,business_programs_or_fixtures_started=False,project_written=False,
    native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],report_sha256=digest(D/'REPORT.json'),functions_byteexact=96,
    absent_canonical_dependencies=[name for name,item in required_inputs.items() if not item['currently_regular_file']],
    business_executed=False)))
