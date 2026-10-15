"""Independent saved FAILED ec6 PREP audit. Stdlib only; never imports reviewed Source.
Hashes explicit frozen files to EOF, including graph/trace/gzip bytes without decoding.
No reviewed entry point, child, Native, numerical array, history scan or project write.
"""
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import stat
import struct
import sys
import time

START = time.monotonic()
OUT = Path(__file__).parent
BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E = BASE / 'actual_complete_combined_prepare_v29_installed6a_20261011_receipts'
D = BASE / 'actual_complete_combined_prepare_v29_installed6a_20261011_sources'
R = Path('/Users/wen/spot')
V = R / 'validation/axial_material'
A = R / 'validation/artifacts'
C = V / 'prepare_sender_window_root_index_graph_trace_table_combined_runtime_v29_installed6a_20261011.py'
H = A / 'axial-material-complete-combined-prepare-host-v29-installed6a-20261011'
S = A / 'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v29-installed6a-20261011'
O = A / 'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v29-installed6a-20261011'
T = A / 'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v29-installed6a-20261011'
TIMING = Path('/private/tmp/Root_current_original_account_phase_timing_m9t382tr/CURRENT_ACCOUNT_TIMING.json')
PYTHON = '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12'
FALSE_FLAGS = ('whole_build_qualified', 'whole_INPUT_admitted', 'native_RSS_verified',
               'AAA_accuracy_qualified', 'ABA_admitted', 'physical_balance_qualified',
               'science_or_BOOT_admitted')
CACHE = '/private/tmp/SPOT_INSTALLED6A_NEW_Q_FACTORY_SOURCE_ONLY_V29_wbh7cowp/__pycache__/installed6a_closed_metadata_admission_contract.cpython-312.pyc'
CHECKS = []
INPUTS = {}
HASH_BYTES = 0
CHILD_BEFORE = resource.getrusage(resource.RUSAGE_CHILDREN)
RESERVE = 8 * 2**20

def ck(name, truth):
    if truth is not True:
        raise AssertionError(name)
    CHECKS.append(name)

def ids(s):
    return [s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns]

def exact(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        return struct.pack('>d', a) == struct.pack('>d', b)
    if isinstance(a, dict):
        return list(a) == list(b) and all(exact(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    return a == b

def sorted_dict_projection(value):
    # Original production_runner.write_json sorts JSON object keys recursively.
    # This comparison projection preserves all types, float bits and list order;
    # original saved metadata byte pins and each original dictionary order remain.
    if isinstance(value, dict):
        return {k:sorted_dict_projection(value[k]) for k in sorted(value)}
    if isinstance(value, list):
        return [sorted_dict_projection(q) for q in value]
    return value

def pin(path):
    global HASH_BYTES
    path = Path(path)
    for p in (path, *path.parents):
        ck('no-symlink:' + str(p), not p.is_symlink())
    initial = ids(path.lstat())
    ck('ordinary-single-link:' + str(path), stat.S_ISREG(initial[2]) and initial[3] == 1)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        ck('open-identity:' + str(path), ids(os.fstat(stream.fileno())) == initial)
        n = 0
        for chunk in iter(lambda: stream.read(2**20), b''):
            n += len(chunk)
            h.update(chunk)
        ck('EOF-size-and-identity:' + str(path), n == initial[4] and ids(os.fstat(stream.fileno())) == initial)
    ck('closed-identity:' + str(path), ids(path.lstat()) == initial)
    HASH_BYTES += n
    return dict(path=str(path), size_bytes=initial[4], sha256=h.hexdigest(), identity=initial)

def frozen(q, label):
    value = pin(q['path'])
    ck(label + ':full-EOF-SHA-7ID', exact(value, q))
    if value['path'] in INPUTS:
        ck(label + ':same-pin-alias', exact(value, INPUTS[value['path']]))
    INPUTS[value['path']] = value
    return value

def current(path, sha=None):
    p = pin(path)
    if sha is not None:
        ck('fixed-SHA:' + str(path), p['sha256'] == sha)
    if p['path'] in INPUTS:
        ck('current-same-pin-alias:' + str(path), exact(p, INPUTS[p['path']]))
    INPUTS[p['path']] = p
    return p

def pairs(items):
    d = {}
    for k, v in items:
        if k in d:
            raise ValueError('duplicate JSON key: ' + k)
        d[k] = v
    return d

def strict_bytes(b):
    return json.loads(b, object_pairs_hook=pairs,
                      parse_constant=lambda q: (_ for _ in ()).throw(ValueError('nonfinite JSON: ' + q)))

def read_small(path):
    p = Path(path)
    ck('small-metadata-only:' + str(path), p.stat().st_size < 4*2**20 and p.suffix == '.json')
    return strict_bytes(p.read_bytes())

def literal_bindings(source):
    """Evaluate only top-level declarative constants, never executes Source."""
    env = {}
    def expr(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.Name):
            return env[n.id]
        if isinstance(n, (ast.Tuple, ast.List)):
            vals = [expr(q) for q in n.elts]
            return tuple(vals) if isinstance(n, ast.Tuple) else vals
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'Path' and len(n.args) == 1 and not n.keywords:
            return Path(expr(n.args[0]))
        if isinstance(n, ast.BinOp):
            a, b = expr(n.left), expr(n.right)
            if isinstance(n.op, ast.Div): return a / b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Pow): return a ** b
            if isinstance(n.op, ast.Add): return a + b
        raise ValueError('not a declarative constant')
    tree = ast.parse(source)
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            try:
                value = expr(n.value)
            except (ValueError, KeyError, TypeError):
                continue
            t = n.targets[0]
            if isinstance(t, ast.Name):
                env[t.id] = value
            elif isinstance(t, ast.Tuple) and len(t.elts) == len(value):
                for k, v in zip(t.elts, value):
                    if not isinstance(k, ast.Name): raise ValueError('non-name tuple')
                    env[k.id] = v
    return env, tree

def domain(root):
    root = Path(root)
    if not os.path.lexists(root):
        return dict(root=str(root), observed_absent=True)
    ck('namespace-root-directory:' + str(root), root.is_dir() and not root.is_symlink())
    files, dirs, syms = [], {str(root): ids(root.lstat())}, {}
    for folder, children, names in os.walk(root, followlinks=False):
        for name in children + names:
            path = Path(folder) / name
            s = path.lstat()
            if stat.S_ISLNK(s.st_mode):
                syms[str(path)] = dict(identity=ids(s), literal_target=os.readlink(path))
            elif stat.S_ISDIR(s.st_mode):
                dirs[str(path)] = ids(s)
            else:
                files.append(str(path))
    return dict(root=str(root), files=sorted(files), directories=dirs, symlinks=syms)

def check_saved_namespace(n, later=()):
    got = domain(n['root'])
    if n.get('observed_absent'):
        ck('namespace-absent:' + n['root'], exact(got, n))
        return got
    ck('namespace-no-symlinks:' + n['root'], exact(got['symlinks'], n['symlinks']) and not got['symlinks'])
    ck('namespace-file-domain:' + n['root'], got['files'] == sorted([q['path'] for q in n['files']] + list(later)))
    ck('namespace-directory-domain:' + n['root'], set(got['directories']) == set(n['directories']))
    for p, identity in n['directories'].items():
        if later and p == n['root']:
            ck('E-root-same-directory-object-exact-named-appends',
               got['directories'][p][:3] == identity[:3])
        else:
            ck('directory-7ID:' + p, exact(got['directories'][p], identity))
    for q in n['files']:
        frozen(q, 'frozen namespace')
    return got

def caps_account(value, reserve, label):
    ck(label + ':caps', value['joint_cap_bytes'] == 2*2**30 and
       value['history_cap_bytes'] == 96*2**30 and value['free_floor_bytes'] == 8*2**30 and
       value['reserved_bytes'] == reserve and value['original_600s_check_budget'] is True)
    ck(label + ':sample-bounds', value['joint_bytes'] + reserve < value['joint_cap_bytes'] and
       value['history_including_original_DE_and_new_DE_formal_bytes'] + reserve <= value['history_cap_bytes'] and
       value['free_min_filesystem_bytes'] - reserve >= value['free_floor_bytes'] and
       0 < value['Root_SELF_historical_max_bytes'] < 512*2**20)
    x = value['original_resource_checks']
    ck(label + ':original-resource-caps', x['complete_history']['min_free_bytes'] == 8*2**30 and
       x['complete_history']['artifact_budget_bytes'] == 96*2**30 and
       x['fresh_output']['min_free_bytes'] == 8*2**30 and
       x['fresh_output']['artifact_budget_bytes'] == 2*2**30)

def main():
    ck('unoptimized-own-auditor', sys.flags.optimize == 0 and sys.dont_write_bytecode)
    ck('own-thread-environment-one', all(os.environ.get(k) == '1' for k in
       ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')))
    ck('fixed-own-Python', str(Path(sys.executable)) == PYTHON)
    fpath = E / 'Root_actual_failed_PREP_namespace_and_streams_freeze.json'
    toolpath = E / 'Root_actual_failed_PREP_freeze_and_resource_tools.json'
    current(fpath, '6bf77d3ea3675ccc2ebeb1cf2275a09537345c6dc568f77ea3b0aa782fddc50c')
    current(toolpath, '3242a93d661f6992b17a2b1a82bf1c85da205c817f564c8a01b2a15de8d20b55')
    freeze, tools = read_small(fpath), read_small(toolpath)
    ck('actual-failure-freeze-schema-status', freeze['schema'] == 'ROOT_ACTUAL_FAILED_EC6_COMPLETE_PREP_NAMESPACE_AND_STREAM_FREEZE_V1' and
       freeze['status'] == 'ACTUAL_EC6_COMPLETE_PREP_EXIT1_CLOSED_NOT_ADMITTED')
    ck('failure-boundaries', all(freeze[k] is False for k in FALSE_FLAGS + ('formal_PREP_receipt_created',
       'complete_PREP_qualified', 'goal_complete', 'cleanup_performed')) and
       freeze['failed_PREP_not_overwritten'] is True and freeze['original_host_full_success_final_checks_not_reached'] is True)
    ck('freeze-explicit-observed-cache-only', freeze['observed_read_attempt_missing_contract_path'] == CACHE and
       'no claim that all remaining new read paths are covered' in freeze['root_cause_scope'])
    current(TIMING, '4f07c5d192d6417ca3f989f1fec2e57a135eb4abfa7d4a91106374f3e8005da8')
    timing = read_small(TIMING)
    for q in timing['original_five_guard_pins']:
        frozen(q, 'original guard')
    ck('five-original-guards', len(timing['original_five_guard_pins']) == 5)
    old_de = []
    for name, n in timing['current_complete_D_E_freeze'].items():
        root = min(n['directories'], key=lambda x: len(Path(x).parts))
        old_de.append(check_saved_namespace(dict(root=root, symlinks={}, **n)))
    frozen(timing['original_failed_provenance_pin'], 'retained original d19 failure')
    ck('complete-old-DE-byte-count', sum(q['size_bytes'] for n in timing['current_complete_D_E_freeze'].values() for q in n['files']) == timing['current_external_DE_bytes'] == 3845194)

    for key in ('actual_tool_receipt', 'actual_canonical_Source', 'actual_external_host_stdout',
                'actual_external_host_stderr', 'actual_child_merged_stdout_stderr', 'actual_watchdog',
                'actual_failed_host_result', 'actual_stages', 'root_prelaunch_ledger', 'root_postclose_ledger',
                'immutable_installed_sources', 'freeze_Source'):
        frozen(freeze[key], key)
    installed = read_small(freeze['immutable_installed_sources']['path'])
    pre = read_small(freeze['root_prelaunch_ledger']['path'])
    post = read_small(freeze['root_postclose_ledger']['path'])
    ck('unchanged-353-pre-post-records', exact(pre['current_Source_and_evidence_input_pins'], post['current_Source_and_evidence_input_pins']) and
       len(pre['current_Source_and_evidence_input_pins']) == 353)
    for q in pre['current_Source_and_evidence_input_pins']:
        frozen(q, 'prelaunch/postclose fixed reference')
    caps_account(pre['account'], 64*2**20, 'prelaunch')
    caps_account(post['account'], 2**20, 'postclose')
    ck('original-resource-and-MRO-receipts-preserved',
       all(x['all_original_fiveguards_DE_failed_provenance_held'] is True and
           x['guard_functions_and_MRO_unmodified'] is True and
           x['installed_D_and_formal_complete_held'] is True and
           x['new_build_or_science_qualification'] is False for x in (pre, post)))
    ck('original-root-account-Source-identical', exact(pre['ledger_Source'], post['ledger_Source']))
    frozen(post['ledger_Source'], 'original Root account Source')
    frozen(installed['root_Source_review'], 'installed Root Source review')
    frozen(installed['source_manifest'], 'installed Source manifest')
    frozen(installed['canonical_installed_pin'], 'installed canonical')
    frozen(installed['canonical_source_original'], 'original canonical Source')
    ck('canonical-fixed-SHA-and-copy', installed['canonical_installed_pin']['sha256'] ==
       installed['canonical_source_original']['sha256'] == '7383448b86d9a432a4704ddadbe6edb6d3c9779f8611eb2e72deae51d6bd34b9' and
       installed['canonical_installed_pin']['size_bytes'] == 200462)
    ck('immutable-D-11-Source-copies', len(installed['Source_copies']) == len(installed['immutable_D_files']) == 11)
    for pair in installed['Source_copies']:
        a, b = frozen(pair['original'], 'original Source copy'), frozen(pair['saved'], 'installed Source copy')
        ck('full-Source-copy-byte-and-size-match:' + b['path'], a['sha256'] == b['sha256'] and a['size_bytes'] == b['size_bytes'])
    for q in installed['immutable_D_files']:
        frozen(q, 'D original new 7ID')
    ck('installed-not-science-qualification', all(installed[k] is False for k in FALSE_FLAGS))

    later = (str(fpath), str(toolpath))
    namespaces = freeze['all_complete_namespaces_before_this_freeze_file']
    ck('six-explicit-namespaces', [n['root'] for n in namespaces] == [str(x) for x in (H, S, O, T, D, E)])
    saved_count = sum(len(n.get('files', [])) for n in namespaces)
    saved_bytes = sum(q['size_bytes'] for n in namespaces for q in n.get('files', []))
    ck('35-complete-frozen-files-88139403B', saved_count == 35 and saved_bytes == 88139403)
    current_domains = [check_saved_namespace(n, later if n['root'] == str(E) else ()) for n in namespaces]
    ck('failed-no-success-artifacts', all(not os.path.lexists(p) for p in
       (T, H/'result.json', O/'declaration.json', O/'seal.json', O/'INPUT', O/'Dragon')))
    ck('exact-E-named-append-scope', 'before this new freeze file' in freeze['E_scope'])

    actual = read_small(freeze['actual_tool_receipt']['path'])
    obs = actual['all_actual_tool_observations']
    ck('seven-genuine-tool-observations', len(obs) == 7 and
       [q['chunk_id'] for q in obs] == ['9696a8','e51cb4','0dadfa','620e9c','498e1a','2a88ef','0f2c97'])
    ck('genuine-initial-and-closed-return', exact(actual['initial_tool_return'], obs[0]) and exact(actual['terminal_tool_return'], obs[-1]) and
       obs[0]['session_id'] == 62951 and all(q.get('session_id') == 62951 for q in obs[:-1]) and
       obs[-1]['exit_code'] == 1 and type(obs[-1]['exit_code']) is int and 'session_id' not in obs[-1])
    ck('actual-not-synthetic-closed', all(actual[k] is True for k in ('closed','observed_terminal','actual_tool_return_not_synthetic','closed_session_not_repolled')) and
       actual['new_build_whole_INPUT_native_or_science_qualification_created'] is False)
    ck('actual-stream-redirection-no-synthetic-terminal', all(q['output'] == '' for q in obs))
    launch = actual['actual_launch_arguments']
    launchcmd = ('set -o noclobber\nexec env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 '
       'VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 ' + PYTHON + ' -B ' + str(D/'combined_prepare_host.py') +
       ' > ' + str(E/'parent_stdout.log') + ' 2> ' + str(E/'parent_stderr.log'))
    ck('unchanged-genuine-launch', launch['cmd'] == launchcmd and launch['workdir'] == str(R) and
       launch['sandbox_permissions'] == 'require_escalated' and launch['yield_time_ms'] == 1000)
    outer_stdout = Path(freeze['actual_external_host_stdout']['path']).read_bytes()
    outer_stderr = Path(freeze['actual_external_host_stderr']['path']).read_text()
    child_log = Path(freeze['actual_child_merged_stdout_stderr']['path']).read_text()
    ck('outer-stdout-actually-empty', outer_stdout == b'')
    ck('outer-error-is-real-host-failure', 'RuntimeError: own-child stage failed; no retry' in outer_stderr and
       'runner.execute(HOST' in outer_stderr)
    ck('child-observed-missing-bytecode-owner-error', ('unowned or unavailable read-open attempt: '+CACHE) in child_log and
       'FileNotFoundError' in child_log and 'historical_reuse_actual_graph.InputGraphError' in child_log and
       '_trace_coverage' in child_log and 'create_fresh_complete_wire_graph' in child_log)
    watch = read_small(freeze['actual_watchdog']['path'])
    host = read_small(freeze['actual_failed_host_result']['path'])
    stages = read_small(freeze['actual_stages']['path'])
    command = [PYTHON, str(C), 'prepare-build']
    ck('true-watchdog-failed-one-child', watch['command'] == command and watch['pid'] == 32035 and
       watch['returncode'] == 1 and type(watch['returncode']) is int and
       watch['limit_failure'] is None and watch['rss_cap_mib'] == 512 and watch['own_child_only'] is True and
       watch['liveness_group_cleanup'] is True and watch['elapsed_seconds'] == 287.59398704208434 and
       watch['sampled_peak_rss_mib'] == 485.8125 and 0 < watch['wall_cap_seconds'] <= 600)
    ck('one-real-failed-stage', host['status'] == 'FAILED_COMPLETE_COMBINED_PREPARE_NO_RETRY' and
       host['error'] == "RuntimeError('own-child stage failed; no retry')" and len(host['stage_records']) == 1)
    stage = host['stage_records'][0]
    ck('failed-stage-original-command-cap', stage['status'] == 'FAILED' and stage['command'] == command and
       stage['wall_cap_seconds'] == 600.0 and stage['label'] == 'run/prepare' and
       stage['elapsed_seconds'] == 287.8547256250167 and stage['error'] == 'own-child stage failed; no retry')
    ck('full-typed-final-stages-original-sorted-dict-encoding', exact(sorted_dict_projection(stages['stages']), sorted_dict_projection(host['stage_records'])))
    ck('original-stage-serializer-sorts-dict-keys', 'json.dumps(data, sort_keys=True, indent=2)' in (V/'production_runner.py').read_text())
    ck('host-never-saved-success-input-checks', 'input_sources' not in host and all(host[k] is False for k in
       ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))
    sb = stage['resource_before']
    ck('genuine-stage-resource-before-original-scope', sb['min_free_bytes'] == 8*2**30 and sb['artifact_budget_bytes'] == 96*2**30 and
       sb['resource_scope_policy'] == 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and
       sb['artifact_bytes'] < 96*2**30 and sb['disk_free_bytes'] > 8*2**30)

    hp = current(D/'combined_prepare_host.py', '367f56486d029f9d260082f9d73767915156eb0fcafaf245ad5d74d27a66d778')
    hostsource = Path(hp['path']).read_text()
    hb, ht = literal_bindings(hostsource)
    ck('host-original-caps-literal', (hb['WHOLE_CAP'],hb['STAGE_CAP'],hb['RSS_CAP'],hb['ARCHIVE_CAP']) == (1800,600,512,2*2**30))
    ck('host-READY-and-canonical-Q-binding', hb['SOURCE_BINDING_STATUS'] == 'READY_V25_ACTUAL_Q_AND_TARGET_SOURCE_BOUND' and
       hb['TARGET'] == C and hb['SOURCE_ARCHIVE'] == D and hb['TARGET_SHA'] == installed['canonical_installed_pin']['sha256'])
    ck('host-real-supervisor-MRO-and-saved-failure-Source', 'full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)' in hostsource and
       "runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMBINED_PREPARATION',resources)" in hostsource and
       "FAILED_COMPLETE_COMBINED_PREPARE_NO_RETRY" in hostsource and 'for entry in inputs+[hpin,rpin]:' in hostsource)
    supportpath = hb['SUPPORT']
    current(supportpath, hb['SUPPORT_SHA'])
    sup, _ = literal_bindings(supportpath.read_text())
    host_input_specs = [
       (supportpath,hb['SUPPORT_SHA']), (C,hb['TARGET_SHA']),
       (sup['TARGET'],sup['TARGET_SHA']), (sup['OUT']/'seal.json',hb['SEAL_SHA']),
       (sup['TERMINAL']/'terminal_return.json',hb['TERM_SHA']),
       (V/'combined_runtime_complete_input_graph_read_open_short_index_stable_wire_sort_20261011.py','6a0b6816cbc8c4ce026018bf1952ffcc720c8a0efe6b4c3c39c4c1040da28ff3'),
       (hb['ACTUAL_HELPER_Q_PATH'],hb['ACTUAL_HELPER_Q_SHA'])]
    host_input_specs += [(Path(q['path']),q['sha256']) for q in installed['immutable_D_files']]
    host_input_specs += [(sup['OLD_HELPER'],sup['OLD_HELPER_SHA']), (sup['RESOURCE_FACTORY'],sup['RESOURCE_SHA'])]
    host_inputs = [current(path,sha) for path,sha in host_input_specs]
    before_index = {q['path']:q for q in pre['current_Source_and_evidence_input_pins'] +
                    installed['immutable_D_files'] + [installed['canonical_installed_pin']]}
    ck('20-host-inputs-derived-Source-not-fabricated-host-receipt', len(host_inputs) == 20 and len({q['path'] for q in host_inputs}) == 20)
    for q in host_inputs:
        ck('host-input-before-after-EOF-7ID:' + q['path'], q['path'] in before_index and exact(q, before_index[q['path']]))
    for pathkey, shakey in (('FULL','FULL_SHA'),('PARENT','PARENT_SHA'),('BOUNDED','BOUNDED_SHA')):
        current(sup[pathkey], sup[shakey])
    ck('watchdog-bounded-copy-retained-without-Native-run',
       INPUTS[str(sup['BOUNDED'])]['sha256'] == INPUTS[str(H/'runtime/run_bounded_dragon.py')]['sha256'])
    writer = current(D/'write_actual_prepare_terminal.py', '6ac53858885c8e4a79dfaaea5ae562dfe1ade3b9e76ef758fc3ff026c4c36011')
    writersource = Path(writer['path']).read_text()
    ck('writer-requires-real-closed-zero-no-failed-writer-qualification',
       "observed['exit_code']!=0" in writersource and not os.path.lexists(T))

    for key, chunk, code in (('install_closed','d5b9e0',0),('prelaunch','414965',0),
                             ('postclose_closed','4d6c45',0),('failed_freeze','a0a94b',0)):
        q = tools[key]
        ck('genuine-account-tool:' + key, q['chunk_id'] == chunk and q['exit_code'] == code and 'session_id' not in q)
        value = strict_bytes(q['output'])
        if key == 'install_closed':
            ck('install-stdout-coupled', exact(value['canonical_installed_pin'], installed['canonical_installed_pin']) and
               exact(value['ledger'], freeze['immutable_installed_sources']) and value['installed_files'] == 11)
        elif key in ('prelaunch','postclose_closed'):
            obj, fkey = (pre,'root_prelaunch_ledger') if key == 'prelaunch' else (post,'root_postclose_ledger')
            ck('resource-stdout-report-coupled:' + key, exact(value['report'], freeze[fkey]) and
               value['status'] == obj['status'] and all(exact(value['account'][k],v) for k,v in obj['account'].items() if k != 'original_resource_checks'))
        else:
            ck('freeze-stdout-count-pin-coupled', exact(value['report'], INPUTS[str(fpath)]) and value['files'] == 35 and value['frozen_bytes'] == 88139403)
    ck('no-hidden-metadata-run-success', all(tools[k] is False for k in ('fresh_PREP_succeeded','formal_PREP_writer_executed','complete_BUILD_executed')))

    # Original Root account is sampled BEFORE it writes the postclose ledger.
    # Add exactly the post ledger and the two explicitly appended E files.
    ledger_source = Path(post['ledger_Source']['path']).read_text()
    ck('post-account-before-postledger-write-Source', ledger_source.index('current=account(reserve)') <
       ledger_source.index("write(report,value)") and "reserve=1024*1024" in ledger_source)
    late_outputs = [INPUTS[str(Path(freeze['root_postclose_ledger']['path']))], INPUTS[str(fpath)], INPUTS[str(toolpath)]]
    late_bytes = sum(q['size_bytes'] for q in late_outputs)
    ck('exact-postsample-three-E-outputs-covered-by-original-reserve', late_bytes == 277917 and late_bytes < post['account']['reserved_bytes'])
    expanded_joint = post['account']['joint_bytes'] + late_bytes
    expanded_history = post['account']['history_including_original_DE_and_new_DE_formal_bytes'] + late_bytes
    ck('frozen-root-scope-late-output-byte-bound', expanded_joint + RESERVE < 2*2**30 and expanded_history + RESERVE < 96*2**30)
    ck('own-local-free-space-reserve', os.statvfs(OUT).f_bavail * os.statvfs(OUT).f_frsize - RESERVE >= 8*2**30)
    ck('no-array-or-Native-source-import-own-audit-Source', not any(isinstance(n, (ast.Import,ast.ImportFrom)) and
       any(q.name.split('.')[0] in ('numpy','ctypes','subprocess','multiprocessing') for q in n.names)
       for n in ast.walk(ast.parse(Path(__file__).read_text()))))
    # Second actual full EOF pass; no decoded graph/trace/gzip/business payload.
    for q in tuple(INPUTS.values()):
        ck('final-fullEOF-SHA-7ID:' + q['path'], exact(pin(q['path']), q))
    final_domains = [domain(n['root']) for n in namespaces]
    ck('own-audit-full-domain-held', exact(current_domains, final_domains))
    for old, record in zip(old_de, timing['current_complete_D_E_freeze'].values()):
        ck('old-DE-final-full-domain-held', exact(old, domain(old['root'])))
    children_after = resource.getrusage(resource.RUSAGE_CHILDREN)
    ck('own-no-observed-child-resource-use', children_after.ru_utime == CHILD_BEFORE.ru_utime and
       children_after.ru_stime == CHILD_BEFORE.ru_stime and children_after.ru_maxrss == CHILD_BEFORE.ru_maxrss)
    ck('own-600s-and-512MiB', time.monotonic()-START < 600 and resource.getrusage(resource.RUSAGE_SELF).ru_maxrss < 512*2**20)
    value = dict(
       schema='INDEPENDENT_ACTUAL_FAILED_EC6_PREP_SAVED_EVIDENCE_REVIEW_V1',
       status='PASS_SAVED_ACTUAL_FAILURE_EVIDENCE_ONLY_PREP_REMAINS_FAILED',
       Source_audit_pin=pin(__file__),
       genuine_actual_tool_receipt=INPUTS[str(Path(freeze['actual_tool_receipt']['path']))],
       genuine_root_freeze=INPUTS[str(fpath)], genuine_root_resource_tools=INPUTS[str(toolpath)],
       actual_launch_chunk='9696a8', actual_session=62951, actual_closed_chunk='0f2c97', actual_exit_code=1,
       complete_original_namespace_file_count=35, complete_original_namespace_frozen_bytes=88139403,
       current_file_domains=[dict(root=q['root'], file_count=len(q.get('files',[])), directory_count=len(q.get('directories',{})),
            observed_absent=q.get('observed_absent',False)) for q in current_domains],
       E_exact_named_additions=[INPUTS[p] for p in later],
       E_prior_directory_7ID=namespaces[-1]['directories'][str(E)],
       E_current_directory_7ID=current_domains[-1]['directories'][str(E)],
       original_fixed_reference_count=353, original_fixed_reference_full_EOF_SHA_7ID_twice=True,
       immutable_installed_D_file_count=11, canonical_Source_new_7ID_held=True,
       original_five_guard_Source_pins=timing['original_five_guard_pins'],
       original_complete_D_E_freeze_EOF_7ID_and_namespace_held=True,
       original_failed_d19_provenance_held=True,
       source_derived_original_host_input_pins=host_inputs,
       source_derived_original_host_input_count=20,
       source_derived_host_inputs_not_saved_success_host_receipt=True,
       original_host_success_final_checks_reached=False,
       original_small_saved_metadata_sorted_dict_typed_final_stage_equal=True,
       original_stage_serializer=dict(Source=str(V/"production_runner.py"),line=450,sort_keys=True),
       actual_external_stdout=INPUTS[str(E/'parent_stdout.log')],
       actual_external_stderr=INPUTS[str(E/'parent_stderr.log')],
       actual_child_merged_stdout_stderr=INPUTS[str(H/'run/prepare.log')],
       observed_missing_cache_read_attempt=CACHE,
       failure_cause_scope='One observed unavailable/unowned bytecode read. No proof all other read paths are covered.',
       watchdog=watch,
       watchdog_scope='A single failed metadata PREP stage sampled its own serial child. This is neither complete PREP admission nor whole build/online Native RSS evidence.',
       original_whole_cap_seconds=1800, original_stage_cap_seconds=600, original_rss_cap_mib=512,
       original_threads=1, original_children_at_once=1, original_retries=0,
       original_guard_MRO_source_receipts_preserved=True,
       original_prelaunch_account=pre['account'],
       original_postclose_account=post['account'],
       original_postclose_account_write_boundary='Account was sampled before postclose ledger write, per pinned Source lines130-134.',
       exact_later_E_output_bytes=late_bytes,
       original_postreserve_covers_postledger_freeze_and_tools=True,
       frozen_root_scope_joint_after_exact_E_outputs=expanded_joint,
       frozen_root_scope_history_after_exact_E_outputs=expanded_history,
       extended_sample_scope_is_not_new_full_live_history_scan=True,
       own_output_reserve_bytes=RESERVE,
       own_elapsed_seconds=time.monotonic()-START,
       own_historical_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       own_reviewed_code_imported=False, own_candidate_or_helper_executed=False, own_Native_or_solver_executed=False,
       own_NPZ_or_XSM_arrays_read=False, own_graph_trace_or_gzip_decoded=False, own_history_recomputed=False,
       own_ART_D_E_project_writes=False, own_no_observed_child_resource_use=True,
       all_explicit_input_pins=list(INPUTS.values()), complete_check_count=len(CHECKS),
       checks=CHECKS, formal_PREP_receipt_created=False, complete_PREP_qualified=False,
       goal_complete=False, **{k:False for k in FALSE_FLAGS})
    resultpath = OUT/'INDEPENDENT_FAILED_PREP_SAVED_RESULT.json'
    with resultpath.open('x') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    rp = pin(resultpath)
    ck('own-result-within-declared-output-reserve', sum(q.stat().st_size for q in OUT.iterdir() if q.is_file()) < RESERVE)
    report = (
       'PASS: independent saved evidence review of ACTUAL FAILED ec6 PREP only.\n'
       'Actual launch9696a8/session62951 closed0f2c97 EXIT1; all7 genuine observations and empty redirected terminal stdout retained.\n'
       'Observed rejection: '+CACHE+'\n'
       'The exact child trace records unavailable/unowned bytecode read. This does not establish coverage of other read paths.\n'
       '35 original H/S/O/T/D/E files,88,139,403 B, full frozen namespaces including T absence held; E only has its2 explicit later Root metadata additions.\n'
       'All353 original fixed refs checked twice to raw EOF SHA/7ID;11 immutable D files and canonical new7ID held. All20 actual host input paths reconstructed from Source have complete before/after pins.\n'
       'Original5 guard Sources, complete original D/E21file namespace, and prior d19 failure unchanged. Failedhost final success-input checks were not reached; no saved success receipt was fabricated.\n'
       'Actual two outer streams and childmerged stream fully bound; final stages match under original sorted-dict JSON encoding; exact types/list order/float bits preserved.\n'
       'Actual failed metadata-stage watchdog:287.59398704208434s,485.8125MiB sampled own-child peak, limit_failure=None, returncode1, cleanup=true.\n'
       'Original caps1800host/600stage/512MiB/thread1/child1/retry0,96GiB history/free8GiB/joint2GiB retained. Original postaccount precedes its ledger write:240,936B postledger+32,321B freeze+4,660B tools=277,917B covered by original1MiB reserve.\n'
       'Original sampled joint/history plus these exact outputs:'+str(expanded_joint)+'/'+str(expanded_history)+'B. This arithmetic extends the frozen scope; it is not a fresh full live-history check.\n'
       'No T/declaration/seal/INPUT/success result exists. PREP remains FAILED; whole build, whole INPUT, NativeRSS, AAA, ABA, physical balance, science/BOOT and goal-complete remain false.\n'
       'Own audit only: no reviewed code import, helper execution, Native/solver/PS, array read, gzip/graph/trace decode, history scan, or ART/project write.\n'
       'Full input/check evidence:'+str(resultpath)+'\n')
    with (OUT/'REPORT.txt').open('x') as f: f.write(report)
    print(json.dumps(dict(status=value['status'],checks=value['complete_check_count'],
       distinct_full_EOF_inputs=len(INPUTS),raw_EOF_bytes_read=HASH_BYTES,
       result=rp,report=pin(OUT/'REPORT.txt'),
       own_elapsed_seconds=time.monotonic()-START,
       own_historical_peak_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),allow_nan=False))

if __name__ == '__main__':
    try:
        main()
    except BaseException as error:
        failure=dict(schema='INDEPENDENT_AUDITOR_FAILURE_PRESERVED_V1',error=repr(error),
                     checks_completed=CHECKS,Source=pin(__file__),candidate_executed=False,
                     actual_failed_PREP_changed=False,qualifications_created=False)
        with (OUT/'AUDITOR_FAILURE.json').open('x') as f:
            json.dump(failure,f,indent=2,allow_nan=False);f.write('\n')
        raise

