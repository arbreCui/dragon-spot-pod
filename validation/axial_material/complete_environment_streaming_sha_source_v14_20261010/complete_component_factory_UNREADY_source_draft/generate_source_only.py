"""Compose an UNREADY source candidate using text/AST only; no business import."""
import ast
import hashlib
import json
from pathlib import Path

D = Path('/private/tmp/axmat_v14_streaming_sha_component_source_draft_hardlink_and_defs_fix_20261010')
P = Path('/Users/wen/spot/validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py')
O = D/'prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py'
P_SHA = 'd2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633'
original = P.read_text()
assert hashlib.sha256(original.encode()).hexdigest() == P_SHA
text = original; regions = []

def region(name, before, after, count=1):
    global text
    assert before != after and text.count(before) == count, (name, text.count(before), count)
    text = text.replace(before, after, count)
    regions.append(dict(name=name, old=before, new=after, count=count))

def assignment(name, value):
    tree = ast.parse(text)
    nodes = [node for node in tree.body if isinstance(node, ast.Assign) and any(
        isinstance(target, ast.Name) and target.id == name for target in node.targets)]
    assert len(nodes) == 1, name
    region('active_assignment_'+name, ast.get_source_segment(text, nodes[0]), name+' = '+value)

def function(name, replacements):
    nodes = [node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef) and node.name == name]
    assert len(nodes) == 1
    before = ast.get_source_segment(text, nodes[0]); after = before
    for old, new, count in replacements:
        assert after.count(old) == count, (name, old, after.count(old), count)
        after = after.replace(old, new, count)
    region('function_'+name, before, after)

region('source_only_documentation', ast.get_source_segment(text, ast.parse(text).body[0]), repr(
    'Source-only V14 complete sender window component with an isolated environment SHA context.\n\n'
    'The original complete86 build, raw numerical controls, mathematical source and\n'
    'genuine original helper/runner/resource MRO remain intact. Only per-environment\n'
    'same-literal SHA memoization and a bounded streaming buffer use the separately\n'
    'pinned canonical private helper. Every unique literal in each environment call\n'
    'still receives complete SHA bytes and fresh full identity/alias checks.\n\n'
    'UNREADY: the new helper, source proof and true Root helper-control admission\n'
    'pins are unknown. This TMP source cannot declare, import business modules, run\n'
    'fixtures, compile, admit a component or confer native/AAA/ABA qualification.'))
assignment('SOURCE', 'ART / "axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-admission-v14-20261010"')
assignment('OUT', 'ART / "axial-material-sender-contiguous-flux-window-streaming-sha-build-v14-20261010"')
assignment('TERMINAL', 'ART / "axial-material-qualified-AB-sender-contiguous-flux-window-streaming-sha-build-terminal-v14-20261010"')
assignment('FAMILY', repr('SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_V14'))
assignment('TERMINAL_SCHEMA', repr('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ACTUAL_EXTERNAL_TERMINAL_RETURN_V14'))
assignment('SOURCE_STATUS', repr('UNREADY_SOURCE_ONLY_REQUIRES_ROOT_STREAMING_HELPER_SOURCE_AND_ACTUAL_CONTROL_PINS_V14'))
constants = '''# All new operational SOURCE pins are intentionally unknown.
FORMAL_STREAM_FACTORY = ROOT / "validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14.py"
STREAM_ENVIRONMENT_PARENT_HELPER = ROOT / "validation/axial_material/prepare_qualified_AB_source_factor_production.py"
STREAM_ENVIRONMENT_PARENT_HELPER_SHA = "619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743"
STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT = ROOT / "validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_production_v13.py"
STREAM_ENVIRONMENT_COMPONENT_SOURCE_PARENT_SHA = "d2d2c7616d329cd8ffbf30f749de6ef8ae08d294240b653cfe8b92a3fe1c8633"
STREAM_ENVIRONMENT_HELPER = ROOT / "validation/axial_material/complete_environment_streaming_sha_helper_v14.py"
STREAM_ENVIRONMENT_HELPER_SHA = None
STREAM_ENVIRONMENT_SOURCE_PROOF = ROOT / "validation/axial_material/complete_environment_streaming_sha_source_v14_20261010/source_patch_proof.json"
STREAM_ENVIRONMENT_SOURCE_PROOF_SHA = None
STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS = STREAM_ENVIRONMENT_SOURCE_PROOF.parent / "Root_actual_helper_controls_admission.json"
STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA = None

'''
region('stream_environment_source_only_bindings', 'FUTURE_ACTUAL_BUILD_TERMINAL_SHA = None', constants+'FUTURE_ACTUAL_BUILD_TERMINAL_SHA = None')
gate = (D/'stream_environment_source_gate.functions.py').read_text()
ast.parse(gate)
region('new_private_helper_and_pure_source_control_gate', '\n\ndef sender_source_admission():', '\n\n'+gate+'\n\ndef sender_source_admission():')
function('require_ready', [
    ('SOURCE_STATUS != "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_COMPONENT_EXECUTION"',
     'SOURCE_STATUS != "READY_SOURCE_ONLY_FOR_ROOT_REVIEWED_STREAMING_SHA_COMPONENT_EXECUTION_V14"', 1),
    ('        raise ValueError("the complete frozen sender raw layout must be bound; no inferred defaults")',
     '        raise ValueError("the complete frozen sender raw layout must be bound; no inferred defaults")\n'
     '    if Path(__file__).resolve() != FORMAL_STREAM_FACTORY:\n'
     '        raise ValueError("TMP source-only V14 draft is not the formal component factory")\n'
     '    for value in (STREAM_ENVIRONMENT_HELPER_SHA, STREAM_ENVIRONMENT_SOURCE_PROOF_SHA,\n'
     '                  STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA):\n'
     '        if not isinstance(value, str) or re.fullmatch("[0-9a-f]{64}", value) is None or value == "0"*64:\n'
     '            raise ValueError("new canonical helper/source proof/actual Root controls pins remain unknown")', 1)])

# Replace only active factory protocol literals. Frozen sender/raw/kernel source
# proof schemas, all inherited paths and mathematical contracts retain V13/V11.
for old, new in (
    ('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_SOURCE_ADMISSION_V13', 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_SOURCE_ADMISSION_V14'),
    ('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_DECLARATION_V13', 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_DECLARATION_V14'),
    ('DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_ONLY_V13', 'DECLARED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_ONLY_V14'),
    ('PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY', 'PASS_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14'),
    ('FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_NO_RETRY', 'FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_NO_RETRY_V14'),
    ('COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_CONTROLS_ONLY', 'COMPLETE_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_CONTROLS_ONLY_V14'),
    ('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_BUILD_SEAL_V13', 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_SEAL_V14'),
    ('AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_PRODUCTION_RUNTIME_INPUT_ADMISSION_V13', 'AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_PRODUCTION_RUNTIME_INPUT_ADMISSION_V14'),
    ('SENDER_CONTIGUOUS_FLUX_WINDOW_RUNTIME_INPUT_ONLY_V13', 'SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_RUNTIME_INPUT_ONLY_V14')):
    region('active_protocol_'+old, old, new, text.count(old))

function('source_inputs', [
    ('    for path,wanted in expected.items():',
     '    stream_admission = stream_environment_helper_source_admission()\n'
     '    for path, wanted in stream_admission["source_inputs"].items():\n'
     '        existing = expected.get(path, expected.get(Path(path)))\n'
     '        if existing is not None and existing != wanted:\n'
     '            raise ValueError("whole stream helper/control INPUT owner conflict")\n'
     '        expected[path] = wanted\n'
     '    for path,wanted in expected.items():', 1)])
function('complete_archive_forecast', [
    ('    return result',
     '    stream_admission = stream_environment_helper_source_admission()\n'
     '    stream_source = {\n'
     '        "complete_environment_streaming_sha_helper_v14.py": require(STREAM_ENVIRONMENT_HELPER, STREAM_ENVIRONMENT_HELPER_SHA).stat().st_size,\n'
     '        "stream_environment_helper_source_patch_proof.json": require(STREAM_ENVIRONMENT_SOURCE_PROOF, STREAM_ENVIRONMENT_SOURCE_PROOF_SHA).stat().st_size,\n'
     '        "stream_environment_helper_controls_admission.json": require(STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS, STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA).stat().st_size,\n'
     '    }\n'
     '    stream_source_bytes = sum(stream_source.values())\n'
     '    complete_with_stream = result["forecast_complete_with_sender_bytes"] + stream_source_bytes\n'
     '    if complete_with_stream >= ARCHIVE_RESERVE:\n'
     '        raise ValueError("whole cache+sender+three stream SOURCE copies exceed original2GiB")\n'
     '    result.update(stream_helper_exact_additional_SOURCE_file_bytes=stream_source,\n'
     '        stream_helper_exact_additional_SOURCE_bytes=stream_source_bytes,\n'
     '        forecast_complete_with_sender_and_stream_helper_bytes=complete_with_stream,\n'
     '        stream_helper_admission=stream_admission,\n'
     '        every_prior_cache_and_sender_forecast_field_retained_exact=True)\n'
     '    return result', 1)])
function('prepare_build', [
    ('    sender=sender_source_admission(); sender_contract=sender_control_contract()',
     '    sender=sender_source_admission(); sender_contract=sender_control_contract()\n'
     '    stream_admission=stream_environment_helper_source_admission()', 1),
    ("    (SOURCE/'FLU2DR64.f').write_text(sender['sender_text'])",
     '    shutil.copy2(require(STREAM_ENVIRONMENT_HELPER, STREAM_ENVIRONMENT_HELPER_SHA), SOURCE/"complete_environment_streaming_sha_helper_v14.py")\n'
     '    shutil.copy2(require(STREAM_ENVIRONMENT_SOURCE_PROOF, STREAM_ENVIRONMENT_SOURCE_PROOF_SHA), SOURCE/"stream_environment_helper_source_patch_proof.json")\n'
     '    shutil.copy2(require(STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS, STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA), SOURCE/"stream_environment_helper_controls_admission.json")\n'
     "    (SOURCE/'FLU2DR64.f').write_text(sender['sender_text'])", 1),
    ('        sender_window_source_admission=sender, sender_wrapper_control_contract=sender_contract,',
     '        sender_window_source_admission=sender, sender_wrapper_control_contract=sender_contract,\n'
     '        stream_environment_helper_admission=stream_admission,', 1),
    ('        sender_source_admission=sender,sender_control_contract=sender_contract,original_stage_count=68,',
     '        stream_environment_helper_admission=stream_admission,\n'
     '        sender_source_admission=sender,sender_control_contract=sender_contract,original_stage_count=68,', 1),
    ("    h.environment(d);write_new(OUT/'declaration.json',d)", "    environment(d);write_new(OUT/'declaration.json',d)", 1)])
function('environment', [
    ('    helper().environment(d, require_build_interpreter=require_build_interpreter)',
     '    private_helper = stream_environment_helper()\n'
     '    with private_helper.complete_environment_digest_context(d["native_library_aliases"]):\n'
     '        private_helper.environment(d, require_build_interpreter=require_build_interpreter)', 1)])
function('declaration_admission', [
    ("    if d['production_link_command']!=d['build_commands'][2]:raise ValueError('explicit actual production link command differs')",
     "    if d['production_link_command']!=d['build_commands'][2]:raise ValueError('explicit actual production link command differs')\n"
     '    stream_admission=stream_environment_helper_source_admission()\n'
     '    if d["stream_environment_helper_admission"] != stream_admission:\n'
     '        raise ValueError("entire actual helper SOURCE/control admission changed")\n'
     '    for original_path, copied_name, wanted in (\n'
     '            (STREAM_ENVIRONMENT_HELPER,"complete_environment_streaming_sha_helper_v14.py",STREAM_ENVIRONMENT_HELPER_SHA),\n'
     '            (STREAM_ENVIRONMENT_SOURCE_PROOF,"stream_environment_helper_source_patch_proof.json",STREAM_ENVIRONMENT_SOURCE_PROOF_SHA),\n'
     '            (STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS,"stream_environment_helper_controls_admission.json",STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA)):\n'
     '        if require(SOURCE/copied_name,wanted).read_bytes()!=require(original_path,wanted).read_bytes():\n'
     '            raise ValueError("actual SOURCE helper evidence copies differ; never import the copy")\n'
     '    source_admission=read(require(SOURCE/"source_admission.json"))\n'
     '    if (source_admission["schema"] != "AXMAT_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_SOURCE_ADMISSION_V14"\n'
     '            or source_admission["stream_environment_helper_admission"] != stream_admission):\n'
     '        raise ValueError("whole source admission must bind exact helper controls independently")\n'
     '    if not 0 < d["complete_archive_forecast"]["forecast_complete_with_sender_and_stream_helper_bytes"] < ARCHIVE_RESERVE:\n'
     '        raise ValueError("complete three-copy streaming helper forecast must fit original2GiB")', 1)])
function('audit_build', [
    ('        sender_window_source_admission=d[\'sender_source_admission\'],actual_new_sender_compiled_and_linked=True,',
     '        sender_window_source_admission=d[\'sender_source_admission\'],actual_new_sender_compiled_and_linked=True,\n'
     '        stream_environment_helper_admission=d["stream_environment_helper_admission"],', 1)])
function('run_build', [
    ('    result = dict(classification="FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_NO_RETRY_V14", error=None,',
     '    result = dict(classification="FAILED_SENDER_CONTIGUOUS_FLUX_WINDOW_STREAMING_SHA_BUILD_NO_RETRY_V14", error=None,\n'
     '        stream_environment_helper_admission=d["stream_environment_helper_admission"],', 1),
    ("        if (audit['sender_window_controls_passed'] is not True or audit['actual_new_sender_compiled_and_linked'] is not True",
     '        if audit["stream_environment_helper_admission"] != d["stream_environment_helper_admission"]:\n'
     '            raise ValueError("actual complete audit must bind original full helper controls")\n'
     "        if (audit['sender_window_controls_passed'] is not True or audit['actual_new_sender_compiled_and_linked'] is not True", 1)])
function('production_admission', [
    ('    flags = ("rank1_factor_cache_controls_passed",',
     '    stream_admission=stream_environment_helper_source_admission()\n'
     '    if (d["stream_environment_helper_admission"] != stream_admission\n'
     '            or result["stream_environment_helper_admission"] != stream_admission\n'
     '            or audit["stream_environment_helper_admission"] != stream_admission\n'
     '            or not 0 < d["complete_archive_forecast"]["forecast_complete_with_sender_and_stream_helper_bytes"] < ARCHIVE_RESERVE):\n'
     '        raise ValueError("actual complete86 component must retain whole stream helper/control INPUT")\n'
     '    flags = ("rank1_factor_cache_controls_passed",', 1),
    ('        sender_window_source_admission=d[\'sender_source_admission\'],sender_window_controls_passed=True,',
     '        stream_environment_helper_admission=stream_admission,\n'
     '        sender_window_source_admission=d[\'sender_source_admission\'],sender_window_controls_passed=True,', 1)])

candidate_tree = ast.parse(text)
inverse = text
for edit in reversed(regions):
    assert inverse.count(edit['new']) == edit['count'], edit['name']
    inverse = inverse.replace(edit['new'], edit['old'], edit['count'])
assert inverse == original and hashlib.sha256(inverse.encode()).hexdigest() == P_SHA
before_tree = ast.parse(original)
old_defs = {node.name: node for node in before_tree.body if isinstance(node, ast.FunctionDef)}
new_defs = {node.name: node for node in candidate_tree.body if isinstance(node, ast.FunctionDef)}
changed = []; retained = []
for name, node in old_defs.items():
    a = ast.get_source_segment(original,node); b = ast.get_source_segment(text,new_defs[name])
    if a == b: retained.append(name)
    else: changed.append(name)
assert set(changed) == {'require_ready','source_inputs','complete_archive_forecast','prepare_build',
    'environment','declaration_admission','audit_build','run_build','production_admission'}
assert all(name in retained for name in ('helper','parent_factory','DynamicHistoryResources','control_audit',
    'sender_controls_audit','sender_raw_receipt','sender_namespace_identities','binary_audit','stage_commands','stage_labels',
    'sender_source_admission','sender_control_contract','archive_forecast','production_cache_shape_forecast'))
future = {target.id: ast.literal_eval(node.value) for node in candidate_tree.body if isinstance(node,ast.Assign)
    for target in node.targets if isinstance(target,ast.Name) and target.id in
    ('STREAM_ENVIRONMENT_HELPER_SHA','STREAM_ENVIRONMENT_SOURCE_PROOF_SHA','STREAM_ENVIRONMENT_ACTUAL_HELPER_CONTROLS_SHA')}
assert len(future) == 3 and all(value is None for value in future.values())
prepare = ast.get_source_segment(text,new_defs['prepare_build'])
assert prepare.count('    h.environment(old)') == 1 and 'h.environment(d)' not in prepare
assert 'h=helper(); full,production=h.modules(); guard_files=h.guard_admission(full)' in prepare
O.write_text(text)
proof = dict(schema='AXMAT_V14_STREAMING_SHA_COMPLETE_COMPONENT_SOURCE_DRAFT_INVERSE_PROOF_V1',
    status='UNREADY_SOURCE_ONLY', parent=dict(path=str(P),sha256=P_SHA), candidate=dict(path=str(O),
    sha256=hashlib.sha256(text.encode()).hexdigest(),bytes=len(text.encode())), edits=regions,
    complete_inverse_byteexact=True, inverse_sha256=hashlib.sha256(inverse.encode()).hexdigest(),
    ast_parse_only=True, original_top_def_count=len(old_defs),candidate_top_def_count=len(new_defs),
    original_all_def_count=len([node for node in ast.walk(before_tree) if isinstance(node,ast.FunctionDef)]),
    candidate_all_def_count=len([node for node in ast.walk(candidate_tree) if isinstance(node,ast.FunctionDef)]),
    changed_original_functions=changed,byteexact_retained_original_functions=retained,
    all_three_new_pins=future,business_imports=False,helper_calls=False,fixture_execution=False,compile=False,
    component_execution=False,project_write=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
(D/'COMPLETE_INVERSE_PROOF.json').write_text(json.dumps(proof,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
summary = {key:value for key,value in proof.items() if key != 'edits'}
summary['edit_region_count']=len(regions)
summary['inverse_proof']=dict(path=str(D/'COMPLETE_INVERSE_PROOF.json'),sha256=hashlib.sha256(
    (D/'COMPLETE_INVERSE_PROOF.json').read_bytes()).hexdigest())
print(json.dumps(summary,indent=2,ensure_ascii=False,allow_nan=False))
