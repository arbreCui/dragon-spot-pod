import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import stat
import sys
import tempfile
import time

started = time.monotonic()
process_attempts = []
def block_process(event, args):
    if event in ('subprocess.Popen', 'os.system', 'os.fork', 'os.forkpty', 'os.exec', 'os.posix_spawn', 'os.spawn'):
        process_attempts.append(event)
        raise RuntimeError('Source-only author prohibits process launches')
sys.addaudithook(block_process)
assert sys.flags.optimize == 0 and sys.dont_write_bytecode
parser = argparse.ArgumentParser()
parser.add_argument('--failed-peer-report', required=True)
args = parser.parse_args()
R = Path('/Users/wen/spot')
V = R/'validation/axial_material'
A = R/'validation/artifacts'
BASE = V/'complete_history_root_index_source_v15_20261010'
OLD_PACKAGE = Path('/private/tmp/SPOT_NEW6A_ACTUAL_READY_FACTORY_AND_FRESH_PREP_SOURCE_ONLY_ec6f2wm3')
OLD_PROOF = OLD_PACKAGE/'COMPLETE_SOURCE_WHOLE_INVERSE_AND_ACTUAL_ROOT_BINDING_PROOF.json'
OLD_MANIFEST = OLD_PACKAGE/'FINAL_READY_FRESH_PREP_SOURCE_ONLY_MANIFEST.json'
OLD_F = V/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v29_installed6a_20261011.py'
OLD_D = BASE/'actual_complete_combined_prepare_v29_installed6a_20261011_sources'
OLD_E = BASE/'actual_complete_combined_prepare_v29_installed6a_20261011_receipts'
OLD_HOST = OLD_D/'combined_prepare_host.py'
OLD_WRITER = OLD_D/'write_actual_prepare_terminal.py'
FAILURE_FREEZE = OLD_E/'Root_actual_failed_PREP_namespace_and_streams_freeze.json'
FAILURE_TOOLS = OLD_E/'Root_actual_failed_PREP_freeze_and_resource_tools.json'
CACHE_REVIEW = Path('/private/tmp/actual_failed_v29_new_Q_cache_Source_only_review_20261011.json')
ORIGINAL_F = V/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py'
ORIGINAL_HOST_ROOT = BASE/'actual_complete_combined_prepare_v25_memory_observation_capture_sources/original_closed_monitor_access_complete_PREP_Source/sealed_namespace_only_complete_PREP_Source'
F = V/'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v30_installed6a_20261011.py'
D = BASE/'actual_complete_combined_prepare_v30_installed6a_20261011_sources'
E = BASE/'actual_complete_combined_prepare_v30_installed6a_20261011_receipts'
H = A/'axial-material-complete-combined-prepare-host-v30-installed6a-20261011'
S = A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v30-installed6a-20261011'
O = A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v30-installed6a-20261011'
T = A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v30-installed6a-20261011'
inputs = {}
def ids(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]
def pin(path):
    p = Path(path)
    for q in (p, *p.parents):
        assert not q.is_symlink(), str(q)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode) and s.st_nlink == 1
    h = hashlib.sha256()
    with p.open('rb') as f:
        assert ids(os.fstat(f.fileno())) == ids(s)
        for chunk in iter(lambda: f.read(2**20), b''):
            h.update(chunk)
        assert ids(os.fstat(f.fileno())) == ids(s)
    assert ids(p.lstat()) == ids(s)
    return dict(path=str(p), size_bytes=s.st_size, sha256=h.hexdigest(), identity=ids(s))
def hold(row):
    assert type(row['identity']) is list and len(row['identity']) == 7 and all(type(v) is int for v in row['identity'])
    actual = pin(row['path'])
    assert actual == {k: row[k] for k in actual}
    if actual['path'] in inputs:
        assert inputs[actual['path']] == actual
    inputs[actual['path']] = actual
    return actual
def pairs(rows):
    out = {}
    for key, value in rows:
        assert key not in out
        out[key] = value
    return out
def reject(value):
    raise ValueError('nonfinite JSON '+value)
def read(path):
    row = hold(pin(path))
    value = json.loads(Path(path).read_bytes(), object_pairs_hook=pairs, parse_constant=reject)
    assert pin(path) == row
    return value
def functions(source):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(source).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
def change(source, rows, before, after):
    assert source.count(before) == 1, (before[:100], source.count(before))
    rows.append(dict(before=before, after=after))
    return source.replace(before, after, 1)
def assignment(source, rows, name, expression):
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id==name)
    return change(source, rows, ast.get_source_segment(source, node), name+'='+expression)
def inverse(source, rows):
    for row in reversed(rows):
        assert source.count(row['after']) == 1
        source = source.replace(row['after'], row['before'], 1)
    return source
def tree(root):
    p = Path(root)
    assert p.is_dir() and not p.is_symlink()
    files, directories = [], {str(p): ids(p.lstat())}
    for q in sorted(p.rglob('*')):
        st = q.lstat()
        assert not stat.S_ISLNK(st.st_mode), str(q)
        if stat.S_ISDIR(st.st_mode):
            directories[str(q)] = ids(st)
        else:
            assert stat.S_ISREG(st.st_mode) and st.st_nlink == 1
            files.append(hold(pin(q)))
    return dict(root=str(p), files=files, directories=directories, symlinks={})
def verify_tree(row):
    p = Path(row['root'])
    observed = {str(p), *(str(q) for q in p.rglob('*'))}
    assert observed == set(row['directories']) | {r['path'] for r in row['files']}
    for path, identity in row['directories'].items():
        assert ids(Path(path).lstat()) == identity
    for q in row['files']:
        hold(q)
def checkpoint():
    assert time.monotonic()-started < 600
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 512*2**20
    assert not process_attempts

for future in (F,D,E,H,S,O,T):
    assert not os.path.lexists(future)
oldproof = read(OLD_PROOF)
oldmanifest = read(OLD_MANIFEST)
assert oldmanifest['Source_roles'] == oldproof['new_Source_roles']
for row in oldproof['actual_all235_Q_and257Root_inputs_held']:
    hold(row)
for row in oldproof['original_five_guards']:
    hold(row)
for rec in oldproof['complete_D_E_freeze'].values():
    for row in rec['files']:
        hold(row)
    for literal, wanted in rec['directories'].items():
        assert ids(Path(literal).lstat()) == wanted
    root = Path(min(rec['directories'], key=lambda p: len(Path(p).parts)))
    assert {str(root), *(str(q) for q in root.rglob('*'))} == set(rec['directories']) | {q['path'] for q in rec['files']}
hold(oldproof['original_failed_provenance'])
hold(oldproof['original_environment_witness945b'])
for path in (OLD_F,OLD_HOST,OLD_WRITER,ORIGINAL_F,ORIGINAL_HOST_ROOT/'combined_prepare_host.py',ORIGINAL_HOST_ROOT/'write_actual_prepare_terminal.py',Path(__file__)):
    hold(pin(path))
assert inputs[str(OLD_F)]['sha256'] == '7383448b86d9a432a4704ddadbe6edb6d3c9779f8611eb2e72deae51d6bd34b9'
assert inputs[str(ORIGINAL_F)]['sha256'] == '117ec099ce288db10fe86c47d441192a3d697f9cd0a4d48e4dff86600bf5d604'
freeze = read(FAILURE_FREEZE)
tools = read(FAILURE_TOOLS)
assert inputs[str(FAILURE_FREEZE)]['sha256'] == '6bf77d3ea3675ccc2ebeb1cf2275a09537345c6dc568f77ea3b0aa782fddc50c'
assert inputs[str(FAILURE_TOOLS)]['sha256'] == '3242a93d661f6992b17a2b1a82bf1c85da205c817f564c8a01b2a15de8d20b55'
assert freeze['schema'] == 'ROOT_ACTUAL_FAILED_EC6_COMPLETE_PREP_NAMESPACE_AND_STREAM_FREEZE_V1'
assert freeze['status'] == 'ACTUAL_EC6_COMPLETE_PREP_EXIT1_CLOSED_NOT_ADMITTED'
assert tools['fresh_PREP_succeeded'] is False and tools['formal_PREP_writer_executed'] is False and tools['complete_BUILD_executed'] is False
receipt = read(freeze['actual_tool_receipt']['path'])
assert receipt['schema'] == 'ROOT_V25_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1'
assert receipt['closed'] is True and receipt['observed_terminal'] is True and receipt['actual_tool_return_not_synthetic'] is True
assert receipt['closed_session_not_repolled'] is True
assert (receipt['initial_tool_return']['chunk_id'],receipt['initial_tool_return']['session_id'],receipt['terminal_tool_return']['chunk_id'],receipt['terminal_tool_return']['exit_code']) == ('9696a8',62951,'0f2c97',1)
assert type(receipt['terminal_tool_return']['exit_code']) is int and 'session_id' not in receipt['terminal_tool_return']
assert receipt['all_actual_tool_observations'][0] == receipt['initial_tool_return'] and receipt['all_actual_tool_observations'][-1] == receipt['terminal_tool_return']
assert sum('exit_code' in r for r in receipt['all_actual_tool_observations']) == 1
falsekeys = ('complete_PREP_qualified','formal_PREP_receipt_created','whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','science_or_BOOT_admitted','goal_complete')
assert all(freeze[k] is False for k in falsekeys)
assert freeze['actual_canonical_Source'] == inputs[str(OLD_F)]
for key in ('actual_tool_receipt','actual_external_host_stdout','actual_external_host_stderr','actual_child_merged_stdout_stderr','actual_watchdog','actual_failed_host_result','actual_stages','root_prelaunch_ledger','root_postclose_ledger','immutable_installed_sources','freeze_Source'):
    hold(freeze[key])
historical_namespaces = []
absent_namespaces = []
for row in freeze['all_complete_namespaces_before_this_freeze_file']:
    if row.get('observed_absent') is True:
        assert set(row)=={'root','observed_absent'} and not os.path.lexists(row['root'])
        absent_namespaces.append(row)
    elif row['root'] == str(OLD_E):
        for p in row['files']:
            hold(p)
        current = tree(OLD_E)
        assert len(current['files']) == 8
        assert {p['path'] for p in current['files']} == {p['path'] for p in row['files']} | {str(FAILURE_FREEZE),str(FAILURE_TOOLS)}
        historical_namespaces.append(current)
    else:
        verify_tree(row)
        historical_namespaces.append(row)
assert len(historical_namespaces)==5 and len(absent_namespaces)==1
assert sum(len(row['files']) for row in freeze['all_complete_namespaces_before_this_freeze_file'] if 'files' in row)==35
assert sum(p['size_bytes'] for row in freeze['all_complete_namespaces_before_this_freeze_file'] if 'files' in row for p in row['files'])==88139403
assert not os.path.lexists(Path(absent_namespaces[0]['root']))
oldout = next(Path(row['root']) for row in historical_namespaces if 'combined-runtime-v29-installed6a' in row['root'])
for member in ('declaration.json','input_graph.json','seal.json','runtime/Dragon'):
    assert not os.path.lexists(oldout/member)
cache = read(CACHE_REVIEW)
assert cache['status'] == 'SOURCE_ONLY_ACTUAL_FAILED_TRACE_SCOPE_REVIEW_NO_FUTURE_COLD_PASS_CLAIM'
assert cache['all_actual_trace_records']==65124 and len(cache['genuine_current_absent_read_records'])==14 and len(cache['genuine_absent_reads_already_declared'])==13 and len(cache['genuinely_uncovered_absent_read_records'])==1
hold(cache['review_Source'])
candidate = importlib.util.cache_from_source(cache['unchanged_Q_contract_Source']['path'])
assert candidate == cache['fixed_pinned_contract_candidate'] == freeze['observed_read_attempt_missing_contract_path']
assert not os.path.lexists(candidate) and not os.path.lexists(Path(candidate).parent)
hold(cache['unchanged_Q_contract_Source'])
peerpath = Path(args.failed_peer_report)
peer = read(peerpath)
assert peer['schema']=='INDEPENDENT_ACTUAL_FAILED_EC6_PREP_SAVED_EVIDENCE_REVIEW_V1'
assert peer['status']=='PASS_SAVED_ACTUAL_FAILURE_EVIDENCE_ONLY_PREP_REMAINS_FAILED'
assert inputs[str(peerpath)]['sha256']=='171c3769105c151a0a88bfb7c3d71b029db0de92ecd252e7ca37f246734563a6'
assert type(peer['complete_check_count'])is int and peer['complete_check_count']==len(peer['checks'])==11763
assert all(type(name)is str and name for name in peer['checks'])
assert type(peer['actual_exit_code'])is int and peer['actual_exit_code']==1
assert (peer['actual_launch_chunk'],peer['actual_session'],peer['actual_closed_chunk'])==('9696a8',62951,'0f2c97')
assert len(peer['all_explicit_input_pins'])==402 and peer['original_fixed_reference_count']==353
assert peer['source_derived_original_host_input_count']==len(peer['source_derived_original_host_input_pins'])==20
assert all(peer[k]is False for k in ('formal_PREP_receipt_created','complete_PREP_qualified','goal_complete','whole_build_qualified','whole_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','science_or_BOOT_admitted','own_reviewed_code_imported','own_candidate_or_helper_executed','own_Native_or_solver_executed','own_ART_D_E_project_writes','original_host_success_final_checks_reached'))
peer_sources = [hold(peer['Source_audit_pin'])]
assert peer_sources[0]['sha256']=='2e0f948baa7ace48a15741ebe3c515725ca8770ce491257af3661e7296f18a1d'
peer_source_text=Path(peer_sources[0]['path']).read_text()
assert "if truth is not True:\n        raise AssertionError(name)\n    CHECKS.append(name)" in peer_source_text
def declared_refs(value):
    if isinstance(value,dict):
        if {'path','size_bytes','sha256','identity'} <= set(value):
            hold(value)
        for child in value.values():declared_refs(child)
    elif isinstance(value,list):
        for child in value:declared_refs(child)
declared_refs(peer)
peer_final_path=peerpath.parent/'FINAL_ARTIFACT_MANIFEST.json'
peer_final=read(peer_final_path)
assert inputs[str(peer_final_path)]['sha256']=='d3876ff69844848859f0c21b4b170cea5de0c5a5de552b020c8b2a65adcab288'
assert peer_final['schema']=='INDEPENDENT_FAILED_PREP_SAVED_REVIEW_V3_FINAL_ARTIFACT_BINDING' and peer_final['status']==peer['status']
assert peer_final['original_review_errors_preserved']is True and peer_final['original_PREP_failed_exit1_preserved']is True
assert peer_final['full_evidence_input_count']==402 and all(peer_final[k]is False for k in ('qualified_complete_PREP','qualified_BUILD','qualified_science_or_BOOT'))
actual_peer_tool=peer_final['actual_review_tool_return']
assert actual_peer_tool['chunk_id']=='d419e2' and type(actual_peer_tool['exit_code'])is int and actual_peer_tool['exit_code']==0 and 'session_id'not in actual_peer_tool
actual_peer_stdout=json.loads(actual_peer_tool['output'],object_pairs_hook=pairs,parse_constant=reject)
assert actual_peer_stdout['status']==peer['status'] and actual_peer_stdout['checks']==11763 and actual_peer_stdout['distinct_full_EOF_inputs']==402
assert actual_peer_stdout['result']==inputs[str(peerpath)]
peer_artifacts=[hold(row)for row in peer_final['explicit_review_artifacts']]
assert len(peer_artifacts)==13
assert actual_peer_stdout['report']in peer_artifacts and peer_sources[0]in peer_artifacts and inputs[str(peerpath)]in peer_artifacts
declared_refs(peer_final)
peer_tools_path=peerpath.parent/'ACTUAL_AUDIT_TOOL_RETURNS.json'
peer_tools=read(peer_tools_path)
assert inputs[str(peer_tools_path)]['sha256']=='a496b297b188e6dfa54f1ef70e8c7b0a20c28ddec05a9a2de75bacc255eb69ed'
assert peer_tools['schema']=='INDEPENDENT_FAILED_PREP_SAVED_REVIEW_V3_ACTUAL_TOOL_RETURNS'
assert peer_tools['actual_candidate_PREP_kept_failed']is True and peer_tools['candidate_or_Native_executed']is False
assert peer_tools['reviewer_V1_V2_failures_are_reviewer_errors_not_new_candidate_runs']is True
assert sum(row['actual_tool_return']==actual_peer_tool for row in peer_tools['actual_observations'])==1
peer_artifacts.append(inputs[str(peer_final_path)])
checkpoint()
failure_files = {}
for ns in historical_namespaces:
    for row in ns['files']:failure_files[row['path']]=row
for row in [inputs[str(OLD_F)],freeze['freeze_Source'],inputs[str(CACHE_REVIEW)],cache['review_Source'],inputs[str(peerpath)],*peer_sources,*peer_artifacts]:
    actual=hold(row)
    if actual['path'] in failure_files:assert failure_files[actual['path']]==actual
    failure_files[actual['path']]=actual
failure_manifest = dict(schema='SPOT_NEW6A_ACTUAL_FAILED_V29_PREP_INPUT_ONLY_NAMESPACE_MANIFEST_V1',
    status='INPUT_ONLY_GENUINE_SAVED_V29_CLOSED_EXIT1',Source_only=True,
    actual_failed_v29_freeze=inputs[str(FAILURE_FREEZE)],actual_failure_resource_and_freeze_tools=inputs[str(FAILURE_TOOLS)],
    actual_failed_tool_receipt=freeze['actual_tool_receipt'],actual_failed_factory=inputs[str(OLD_F)],
    actual_failed_tool_binding=dict(initial_chunk='9696a8',session_id=62951,terminal_chunk='0f2c97',exit_code=1),
    historical_original_freeze_file_count=35,historical_original_freeze_bytes=88139403,
    original_freeze_E_boundary_preserved=freeze['E_scope'],
    current_complete_v29_failed_namespaces=historical_namespaces,
    genuinely_absent_v29_terminal_namespace=absent_namespaces[0],
    actual_no_declaration_graph_seal_or_Dragon_in_failed_O=True,
    full_EOF7ID_regular_inputs=sorted(failure_files.values(),key=lambda r:r['path']),
    complete_input_only_files_bytes=sum(r['size_bytes'] for r in failure_files.values()),
    actual_saved_failure_independent_review=inputs[str(peerpath)],
    actual_saved_failure_independent_artifact_manifest=inputs[str(peer_final_path)],
    actual_saved_failure_independent_tool_returns=inputs[str(peer_tools_path)],
    actual_saved_failure_cache_Source_only_review=inputs[str(CACHE_REVIEW)],
    fixed_new_contract_optional_cache_Source=cache['unchanged_Q_contract_Source'],
    fixed_new_contract_optional_cache_candidate=candidate,
    old_failure_and_raw_streams_never_rewritten=True,
    complete_PREP_qualified=False,whole_build_qualified=False,whole_INPUT_admitted=False,
    native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,science_or_BOOT_admitted=False,
    future_PREP_receipt_or_new_business_result_created=False)
PKG=Path(tempfile.mkdtemp(prefix='SPOT_V30_FIXED_CONTRACT_ABSENCE_FAILED_V29_SOURCE_ONLY_',dir='/private/tmp'))
failure_name='ACTUAL_FAILED_V29_PREP_INPUT_ONLY_MANIFEST.json'
local_failure=PKG/failure_name
with local_failure.open('x') as f:json.dump(failure_manifest,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
failure_sha=pin(local_failure)['sha256']
newconstants='\nACTUAL_FAILED_V29_PREP_INPUT_MANIFEST=Path('+repr(str(D/failure_name))+')\nACTUAL_FAILED_V29_PREP_INPUT_MANIFEST_SHA='+repr(failure_sha)+'\n'
newhelper = '''def actual_failed_v29_PREP_input_only(g):
    """Genuine v29 EXIT1 bytes and exact namespaces are INPUT; never success."""
    m=g.strict_json(str(ACTUAL_FAILED_V29_PREP_INPUT_MANIFEST),ACTUAL_FAILED_V29_PREP_INPUT_MANIFEST_SHA)
    if (m['schema']!='SPOT_NEW6A_ACTUAL_FAILED_V29_PREP_INPUT_ONLY_NAMESPACE_MANIFEST_V1'
        or m['status']!='INPUT_ONLY_GENUINE_SAVED_V29_CLOSED_EXIT1' or m['Source_only']is not True
        or m['actual_failed_tool_binding']!=dict(initial_chunk='9696a8',session_id=62951,terminal_chunk='0f2c97',exit_code=1)
        or type(m['actual_failed_tool_binding']['exit_code'])is not int
        or any(m[key]is not False for key in ('complete_PREP_qualified','whole_build_qualified','whole_INPUT_admitted','native_RSS_verified',
            'AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','science_or_BOOT_admitted','future_PREP_receipt_or_new_business_result_created'))):
        raise ValueError('genuine frozen v29 failed PREP has no eligibility')
    files={str(ACTUAL_FAILED_V29_PREP_INPUT_MANIFEST):ACTUAL_FAILED_V29_PREP_INPUT_MANIFEST_SHA}
    pins=m['full_EOF7ID_regular_inputs']
    if type(pins)is not list or len({row['path']for row in pins})!=len(pins):raise ValueError('failed v29 complete pins must be unique')
    for row in pins:
        path=normal(row['path']);s=path.lstat()
        if (not stat.S_ISREG(s.st_mode) or s.st_nlink!=1 or type(row['size_bytes'])is not int or row['size_bytes']!=s.st_size
            or type(row['identity'])is not list or len(row['identity'])!=7 or any(type(v)is not int for v in row['identity'])
            or [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=row['identity']):
            raise ValueError('failed v29 exact ordinary Source-owned input7ID changed')
        merge_expected(files,{str(path):row['sha256']})
    if sum(row['size_bytes']for row in pins)!=m['complete_input_only_files_bytes']:raise ValueError('failed v29 complete input byte sum changed')
    fpin=m['actual_failed_v29_freeze'];f=g.strict_json(fpin['path'],fpin['sha256'])
    tpin=m['actual_failed_tool_receipt'];t=g.strict_json(tpin['path'],tpin['sha256'])
    rpin=m['actual_failure_resource_and_freeze_tools'];r=g.strict_json(rpin['path'],rpin['sha256'])
    if (f['schema']!='ROOT_ACTUAL_FAILED_EC6_COMPLETE_PREP_NAMESPACE_AND_STREAM_FREEZE_V1'
        or f['status']!='ACTUAL_EC6_COMPLETE_PREP_EXIT1_CLOSED_NOT_ADMITTED' or f['actual_tool_receipt']!=tpin
        or f['actual_canonical_Source']!=m['actual_failed_factory']
        or any(f[key]is not False for key in ('complete_PREP_qualified','formal_PREP_receipt_created','whole_build_qualified','whole_INPUT_admitted',
            'native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','science_or_BOOT_admitted','goal_complete'))
        or t['schema']!='ROOT_V25_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' or t['closed']is not True
        or t['observed_terminal']is not True or t['actual_tool_return_not_synthetic']is not True or t['closed_session_not_repolled']is not True
        or t['initial_tool_return']['chunk_id']!='9696a8' or t['initial_tool_return']['session_id']!=62951
        or t['terminal_tool_return']['chunk_id']!='0f2c97' or type(t['terminal_tool_return']['exit_code'])is not int
        or t['terminal_tool_return']['exit_code']!=1 or 'session_id'in t['terminal_tool_return']
        or t['all_actual_tool_observations'][0]!=t['initial_tool_return'] or t['all_actual_tool_observations'][-1]!=t['terminal_tool_return']
        or sum('exit_code'in row for row in t['all_actual_tool_observations'])!=1
        or r['fresh_PREP_succeeded']is not False or r['formal_PREP_writer_executed']is not False or r['complete_BUILD_executed']is not False):
        raise ValueError('actual saved v29 external CLOSED EXIT1 and immutable streams required')
    rows=m['current_complete_v29_failed_namespaces']
    if type(rows)is not list or len(rows)!=5:raise ValueError('complete failed v29 H/S/O/D/E namespaces required')
    namespaces=[]
    for row in rows:
        root=normal(row['root']);directory_pins=row['directories']
        if set(row)!={'root','files','directories','symlinks'} or row['symlinks']!={} or str(root)not in directory_pins:
            raise ValueError('failed v29 namespace shape changed')
        for literal,wanted in directory_pins.items():
            path=normal(literal);s=path.lstat()
            if (not stat.S_ISDIR(s.st_mode) or [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]!=wanted):
                raise ValueError('failed v29 exact sealed directory7ID changed')
        observed={str(root),*(str(p)for p in root.rglob('*'))}
        if observed!=set(directory_pins)|{p['path']for p in row['files']}:raise ValueError('failed v29 exhaustive namespace pathset changed')
        relative_files={str(Path(p['path']).relative_to(root)):p['sha256']for p in row['files']}
        if len(relative_files)!=len(row['files']) or any(files.get(p['path'])!=p['sha256']for p in row['files']):raise ValueError('failed v29 namespace complete byte owners changed')
        relative_dirs=sorted(str(Path(p).relative_to(root))for p in directory_pins if p!=str(root))
        namespaces.append(dict(root=str(root),files=relative_files,directories=relative_dirs,symlinks={},
            owner=str(root)+'#ACTUAL_FAILED_V29_PREP_INPUT_ONLY',category='component_terminals'))
    absent_row=m['genuinely_absent_v29_terminal_namespace']
    normal(absent_row['root'],missing=True)
    if absent_row['observed_absent']is not True or os.path.lexists(absent_row['root']):raise ValueError('failed v29 terminal remained genuinely absent')
    old_out=next(Path(row['root'])for row in rows if 'combined-runtime-v29-installed6a'in row['root'])
    if any(os.path.lexists(old_out/name)for name in ('declaration.json','input_graph.json','seal.json','runtime/Dragon')):
        raise ValueError('failed v29 cannot acquire declaration graph seal or native output')
    return dict(files=files,namespaces=namespaces)


'''
oldfactory=OLD_F.read_text();oldhost=OLD_HOST.read_text();oldwriter=OLD_WRITER.read_text()
changes=dict(factory=[],host=[],Root_PREP_terminal_writer=[])
factory=oldfactory
for name,expression in [('SOURCE','ART/'+repr(S.name)),('OUT','ART/'+repr(O.name)),('TERMINAL','ART/'+repr(T.name)),('FORMAL_FACTORY','ROOT/'+repr(str(F.relative_to(R))))]:
    factory=assignment(factory,changes['factory'],name,expression)
old_doc=ast.get_source_segment(factory,ast.parse(factory).body[0])
factory=change(factory,changes['factory'],old_doc,repr('READY Source-only v30 binding for unchanged installed6a and genuine new Q/peer/Root CLOSED0. The genuine v29 PREP CLOSED EXIT1 and all original bytes remain INPUT only. One fixed source-derived contract optional cache ENOENT is explicitly declared before the unchanged full read-trace verifier. Original full PREP/five build stages/whole INPUT, physical and mathematical gates, guards, resource thresholds, own-child PS2s and environment witness remain required. No new v30 PREP, build, INPUT, Native or science result is supplied; six future business pins remain None.'))
factory=change(factory,changes['factory'],'\ndef create_complete_input_graph(helpers,source_inventory,extra,roots):',newconstants+'\n'+newhelper+'def create_complete_input_graph(helpers,source_inventory,extra,roots):')
node=next(n for n in ast.parse(factory).body if isinstance(n,ast.FunctionDef)and n.name=='create_complete_input_graph')
before_graph=ast.get_source_segment(factory,node);graph=before_graph
graph=graph.replace("    failed=failed_prepare_input(g);trim=trim_component_input(g)\n", "    failed=failed_prepare_input(g);trim=trim_component_input(g)\n    failed_v29=actual_failed_v29_PREP_input_only(g)\n",1)
graph=graph.replace("expected_files=trim['files']),*trim['support_owners']])", "expected_files=trim['files']),*trim['support_owners'],\n        dict(owner='ACTUAL_FROZEN_V29_FAILED_PREP_COMPLETE_INPUT_ONLY',category='component_terminals',expected_files=failed_v29['files'])])",1)
graph=graph.replace("    negative=g.strict_json(str(SOURCE/TRIM_ABSENCE_NAME))\n", "    aliases=g._alias_map([*aliases.values(),*g.capture_aliases([row['root']for row in failed_v29['namespaces']])])\n    negative=g.strict_json(str(SOURCE/TRIM_ABSENCE_NAME))\n",1)
negative_marker="    g._absence_phase(g._absence_inputs(negative['absence_inputs']),aliases,expected=negative['observations'])\n    namespaces=checks.bind_namespaces(g,expanded,aliases)"
negative_addition='''    g._absence_phase(g._absence_inputs(negative['absence_inputs']),aliases,expected=negative['observations'])
    # This single optional candidate comes from the unchanged explicit Source
    # pin and the actual interpreter, never from reached trace discovery.
    contract_path=require(NEW6A_METADATA_CONTRACT_PIN['path'],NEW6A_METADATA_CONTRACT_PIN['sha256']);contract_stat=contract_path.lstat()
    if ([contract_stat.st_dev,contract_stat.st_ino,contract_stat.st_mode,contract_stat.st_nlink,contract_stat.st_size,contract_stat.st_mtime_ns,contract_stat.st_ctime_ns]!=NEW6A_METADATA_CONTRACT_PIN['identity']
        or extra.get(str(contract_path))!=NEW6A_METADATA_CONTRACT_PIN['sha256']):raise ValueError('optional cache requires the exact already-owned new6a contract Source7ID')
    contract_cache=importlib.util.cache_from_source(str(contract_path))
    if contract_cache in negative['absence_inputs'] or os.path.lexists(contract_cache):raise ValueError('new6a contract optional cache must be separately declared genuine ENOENT')
    cache_parent=Path(contract_cache).parent
    while not os.path.lexists(cache_parent):cache_parent=cache_parent.parent
    aliases=g._alias_map([*aliases.values(),*g.capture_aliases([str(cache_parent)])])
    contract_absence={contract_cache:dict(owner=str(contract_path)+'#OPTIONAL_CURRENT_INTERPRETER_CACHE',category='source_namespace',
        reason='Exact cache_from_source candidate of the unchanged explicitly pinned new6a metadata contract; genuine ENOENT is INPUT only')}
    contract_observations=g._absence_phase(g._absence_inputs(contract_absence),aliases)
    negative=dict(absence_inputs={**negative['absence_inputs'],**contract_absence},aliases=list(aliases.values()),
        observations={**negative['observations'],**contract_observations})
    g._absence_phase(g._absence_inputs(negative['absence_inputs']),aliases,expected=negative['observations'])
    namespaces=checks.bind_namespaces(g,expanded,aliases)'''
assert graph.count(negative_marker)==1
graph=graph.replace(negative_marker,negative_addition,1)
ns_marker="    namespaces.append(g.explicit_sealed_namespace(str(SOURCE),source_inventory['files'],{},"
ns_addition="    for row in failed_v29['namespaces']:\n        namespaces.append(g.explicit_sealed_namespace(row['root'],row['files'],{},owner=row['owner'],\n            category='component_terminals',directories=row['directories']))\n    del failed_v29\n"
assert graph.count(ns_marker)==1
graph=graph.replace(ns_marker,ns_addition+ns_marker,1)
factory=change(factory,changes['factory'],before_graph,graph)
assert inverse(factory,changes['factory'])==oldfactory
factory_sha=hashlib.sha256(factory.encode()).hexdigest()
host=oldhost
for name,expression in [('FUTURE_V25_CANONICAL_SHA',repr(factory_sha)),('HOST','Path('+repr(str(H))+')'),('TARGET','Path('+repr(str(F))+')'),('SOURCE','Path('+repr(str(S))+')'),('OUT','Path('+repr(str(O))+')'),('TERMINAL','Path('+repr(str(T))+')'),('SOURCE_ARCHIVE','Path('+repr(str(D))+')')]:
    host=assignment(host,changes['host'],name,expression)
writer=oldwriter
for name,expression in [('FUTURE_V25_CANONICAL_SHA',repr(factory_sha)),('D','Path('+repr(str(D))+')'),('E','Path('+repr(str(E))+')'),('H','Path('+repr(str(H))+')'),('S','Path('+repr(str(S))+')'),('O','Path('+repr(str(O))+')'),('T','Path('+repr(str(T))+')'),('FACTORY','Path('+repr(str(F))+')')]:
    writer=assignment(writer,changes['Root_PREP_terminal_writer'],name,expression)
assert inverse(host,changes['host'])==oldhost and inverse(writer,changes['Root_PREP_terminal_writer'])==oldwriter
assert functions(host)==functions(oldhost) and functions(writer)==functions(oldwriter)
oldfunctions=functions(oldfactory);newfunctions=functions(factory)
assert set(newfunctions)==set(oldfunctions)|{'actual_failed_v29_PREP_input_only'}
assert all(newfunctions[k]==v for k,v in oldfunctions.items() if k!='create_complete_input_graph')
assert newfunctions['known_source_cache_absences']==oldfunctions['known_source_cache_absences']
assert newfunctions['require_ready']==functions(ORIGINAL_F.read_text())['require_ready']
restored = inverse(oldfactory,oldproof['new_Source_forward_changes']['factory'])
chain=oldproof['factory_v3_to_original117ec_chain']
for before,after in [(chain['factory_v3_to_failed_v2_assignment_before'],chain['factory_v3_to_failed_v2_assignment_after']), (chain['factory_v2_to_v1_assignment_before'],chain['factory_v2_to_v1_assignment_after'])]:
    assert restored.count(after)==1;restored=restored.replace(after,before,1)
assert restored.count(chain['factory_v1_added_constants'])==1
restored=restored.replace(chain['factory_v1_added_constants'],'',1)
restored=inverse(restored,chain['factory_v1_forward_changes'])
assert restored==ORIGINAL_F.read_text()
assert inverse(oldhost,oldproof['new_Source_forward_changes']['host'])==(ORIGINAL_HOST_ROOT/'combined_prepare_host.py').read_text()
assert inverse(oldwriter,oldproof['new_Source_forward_changes']['Root_PREP_terminal_writer'])==(ORIGINAL_HOST_ROOT/'write_actual_prepare_terminal.py').read_text()
originalfunctions=functions(restored)
assert all(newfunctions[k]==v for k,v in originalfunctions.items() if k not in ('helper_Q_admission','create_complete_input_graph'))
for literal in ("TOTAL_WALL, STAGE_WALL, RSS = 1800, 600, 512", "RESERVE, HISTORY_CAP, FREE_FLOOR = 2*2**30, 96*2**30, 8*2**30", "DRAFT_STATUS='READY_REVIEWED_V25_ROOT_INDEX_SENDER_COMPONENT_FULL_GRAPH_TRACE_TABLE_FORMAL_FACTORY'"):
    assert literal in factory
for name in ('FUTURE_ACTUAL_COMBINED_DECLARATION_SHA','FUTURE_ACTUAL_COMBINED_PREP_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_SEAL_SHA','FUTURE_ACTUAL_COMBINED_TERMINAL_SHA','FUTURE_ACTUAL_COMBINED_RUNTIME_SHA','FUTURE_ACTUAL_NATIVE_TERMINAL_SHA'):
    n=next(n for n in ast.parse(factory).body if isinstance(n,ast.Assign)and any(isinstance(x,ast.Name)and x.id==name for x in n.targets));assert ast.literal_eval(n.value) is None
for source in (factory,host,writer):ast.parse(source)
outputs={}
for role,name,source in [('factory',F.name,factory),('host','combined_prepare_host.py',host),('Root_PREP_terminal_writer','write_actual_prepare_terminal.py',writer)]:
    path=PKG/name
    with path.open('x') as f:f.write(source)
    outputs[role]=pin(path)
context=PKG/'PRESERVED_V29_AND_ORIGINAL_INVERSE_CONTEXT';context.mkdir()
copies=[]
copy_inputs=list(dict.fromkeys([OLD_F,OLD_HOST,OLD_WRITER,OLD_PROOF,OLD_MANIFEST,ORIGINAL_F,ORIGINAL_HOST_ROOT/'combined_prepare_host.py',ORIGINAL_HOST_ROOT/'write_actual_prepare_terminal.py',FAILURE_FREEZE,FAILURE_TOOLS,CACHE_REVIEW,Path(cache['review_Source']['path']),peerpath,*[Path(r['path'])for r in peer_sources],*[Path(r['path'])for r in peer_artifacts]]))
for i,path in enumerate(copy_inputs):
    before=hold(pin(path));dest=context/(str(i).zfill(2)+'_'+path.name)
    with path.open('rb') as src,dest.open('xb') as dst:
        for chunk in iter(lambda:src.read(2**20),b''):dst.write(chunk)
    saved=pin(dest);assert saved['sha256']==before['sha256'] and saved['size_bytes']==before['size_bytes']
    copies.append(dict(original=before,saved=saved))
proof=dict(schema='SPOT_V30_FIXED_CONTRACT_ABSENCE_AND_COMPLETE_FAILED_V29_SOURCE_INVERSE_PROOF_V1',
    status='SOURCE_ONLY_V30_CANDIDATE_NO_COLD_EXECUTION',Source_only=True,
    new_Source_roles=outputs,new_Source_forward_changes=changes,
    whole_inverse_exact_v29_factory7383=True,whole_inverse_chain_exact_original117ec_sha256=hashlib.sha256(restored.encode()).hexdigest(),
    old_ec6_original_inverse_proof=inputs[str(OLD_PROOF)],
    host_and_Root_PREP_writer_whole_inverse_exact_original=True,
    original_factory_AST_unchanged_except_helper_Q_and_create_complete_input_graph=True,
    v29_factory_AST_unchanged_except_create_complete_input_graph_and_one_new_failure_metadata_function=True,
    original_strict_require_ready_and_5stage_whole_INPUT_functions_AST_identical=True,
    original_known_source_cache_absences_AST_identical=True,
    unchanged_installed6a_Q_and_f574_metadata_contract=True,
    original_typed_snapshot_exactly_preserved=True,
    all_original479_absences_and_every_read_trace_attempt_preserved=True,
    Source_derived_new_optional_cache=cache['minimum_new_absence_input'],
    complete_failed_v29_graph_regular_INPUT_manifest=pin(local_failure),
    actual_new6a_Q=oldmanifest['actual_new6a_Q'],actual_closed_Root_binding=oldmanifest['actual_closed_Root_binding'],
    genuine_Q_writer_peer_Root_closed0_preserved=True,
    full_EOF7ID_inputs_held=list(inputs.values()),exact_failed_namespace_directory_bindings=historical_namespaces,
    genuine_absent_failed_terminal_namespace=absent_namespaces[0],
    retained_original_Source_and_actual_failure_copies=copies,
    original_fiveguards=oldproof['original_five_guards'],original_complete_D_E=oldproof['complete_D_E_freeze'],
    original_failed_provenance=oldproof['original_failed_provenance'],original_environment_witness945b=oldproof['original_environment_witness945b'],
    resources_original_600_1800_512_joint2GiB_history96GiB_free8GiB_PS2s_unmodified=True,
    all_six_business_pins_None=True,canonical_install_or_any_project_module_import_or_execution=False,
    no_future_PREP_BUILD_INPUT_Native_or_science_result_created=True)
proofpath=PKG/'COMPLETE_V30_SOURCE_WHOLE_INVERSE_AND_FAILED_INPUT_BINDING_PROOF.json'
with proofpath.open('x') as f:json.dump(proof,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
manifest=dict(schema='SPOT_V30_FIXED_SOURCE_DERIVED_CONTRACT_ABSENCE_AND_FROZEN_FAILED_V29_READY_SOURCE_ONLY_PACKAGE_V1',
    status='SOURCE_ONLY_V30_READY_BINDING_PENDING_ROOT_SOURCE_REVIEW_INSTALL_AND_UNIQUE_FRESH_PREP',Source_only=True,
    Source_roles=outputs,whole_inverse_and_binding_proof=pin(proofpath),failed_v29_INPUT_manifest=pin(local_failure),
    actual_new6a_Q=oldmanifest['actual_new6a_Q'],actual_closed_Root_binding=oldmanifest['actual_closed_Root_binding'],
    genuine_actual_Root_publisher_tool=oldmanifest['genuine_actual_Root_publisher_tool'],
    future_installed_paths=dict(formal_factory=str(F),Source_archive_D=str(D),receipts_E=str(E),host_H=str(H),source_S=str(S),output_O=str(O),terminal_T=str(T)),
    original_v29_failure_namespaces_preserved=historical_namespaces,genuinely_absent_v29_terminal_namespace=absent_namespaces[0],
    supplemental_current_root_joint_accounting_required=dict(scope='INODE_ONCE_COMPLETE_ORIGINAL_JOINT_PLUS_CURRENT_SOURCE_INPUT_FAMILY_PLUS_COMPLETE_V29_FAILURE_PLUS_V30_OUTPUTS',
        include_current_package_and_all_actual_participating_review_Source_and_report=True,
        include_all_failure_input_manifest_declared_file_pins=True,include_original_D_E_once=True,include_current_v30_D_E_formal_once=True,
        history_scope='UNCHANGED_ORIGINAL_FULL_ART_PLUS_EXTERNAL_ORIGINAL_DE_PLUS_V29_DE_CANONICAL_PLUS_V30_DE_CANONICAL_INODE_ONCE',
        no_ART_failed_H_S_O_double_history_count=True,free8_includes_TMP_filesystem=True,
        all_original_caps_unmodified=True),
    cache_absence_first_phase_and_full_before_after_graph_required=True,
    original_read_trace_no_record_filtered_or_inferred_owner=True,
    prospective_host_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(D/'combined_prepare_host.py')],
    prospective_canonical_command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(F),'prepare-build'],
    prospective_postclose_writer_only_after_genuine_new_closed0=str(D/'write_actual_prepare_terminal.py'),
    actual_old_PREP_exit1_cannot_authorize_new_build=True,canonical_installed=False,fresh_PREP_executed=False,
    all_six_future_business_pins_None=True,whole_build_qualified=False,whole_INPUT_admitted=False,native_RSS_verified=False,
    AAA_accuracy_qualified=False,ABA_admitted=False,physical_balance_qualified=False,science_or_BOOT_admitted=False,
    preparer_Source=inputs[str(Path(__file__))])
manifestpath=PKG/'FINAL_V30_READY_FRESH_PREP_SOURCE_ONLY_MANIFEST.json'
with manifestpath.open('x') as f:json.dump(manifest,f,ensure_ascii=False,indent=2,allow_nan=False);f.write('\n')
for row in tuple(inputs.values()):assert pin(row['path'])==row
for row in historical_namespaces:verify_tree(row)
filesystem=os.statvfs('/private/tmp')
assert filesystem.f_bavail*filesystem.f_frsize-32*2**20>=8*2**30
checkpoint()
print(json.dumps(dict(status=manifest['status'],package=str(PKG),Source_roles=outputs,manifest_pin=pin(manifestpath),proof_pin=pin(proofpath),failed_v29_manifest_pin=pin(local_failure),held_EOF7ID_inputs=len(inputs),original_caps_preserved=True,new_business_results_created=False),allow_nan=False))
