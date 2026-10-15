"""Finite standard-library raw/static review; never imports or calls business code."""
import ast
import hashlib
import json
import pathlib
import re

W = pathlib.Path('/Users/wen/spot/validation/artifacts/axial-material-owned-specs-identity-key-delta-graph-table-cold-runtime-v12-20261009')
OUT = pathlib.Path('/private/tmp/axmat_v12_failed_cold_native_independent_raw_review_20261009')
F = pathlib.Path('/Users/wen/spot/validation/axial_material/prepare_owned_specs_identity_key_delta_graph_table_cold_runtime_v12.py')
OWN = pathlib.Path('/Users/wen/spot/validation/axial_material/cold_own_pid_peak_supervisor_20261008/qualify_refined_AAA_layered_full.py')
pins = {}
checks = []

def must(condition, message):
    if not condition:
        raise AssertionError(message)
    checks.append(message)

def read_raw(p):
    p = pathlib.Path(p)
    must(p.is_file() and not p.is_symlink(), 'regular raw source/record: ' + str(p))
    must(p.stat().st_size < 2**21, 'finite small read: ' + str(p))
    data = p.read_bytes()
    pins[str(p)] = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    return data

def read_json(p):
    return json.loads(read_raw(p))

def read_source(p, expected):
    data = read_raw(p)
    must(hashlib.sha256(data).hexdigest() == expected, 'fixed original source pin: ' + str(p))
    s = data.decode('utf-8')
    return s, ast.parse(s)

def node_named(tree, name, kind=ast.FunctionDef):
    found = [n for n in ast.walk(tree) if isinstance(n, kind) and n.name == name]
    must(len(found) == 1, 'unique static AST node: ' + name)
    return found[0]

def source_of(source, tree, name, kind=ast.FunctionDef):
    return ast.get_source_segment(source, node_named(tree, name, kind))

def top_call_kwargs(tree, name):
    matches = [n.value for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(x, ast.Name) and x.id == name for x in n.targets)]
    must(len(matches) == 1 and isinstance(matches[0], ast.Call), 'unique top dict call: ' + name)
    return {kw.arg: kw.value for kw in matches[0].keywords}

failure = read_json(W / 'cold_source_failure.json')
status = read_json(W / 'AAA/run_status.json')
claim = read_json(W / 'AAA/run_claim.json')
prepared = read_json(W / 'prepared_cold.json')
stages = read_json(W / 'AAA/stages.json')['stages']
labels = ['archives/pack_archives', 'training/common_basis', 'training/rank_precision',
          'AAA/bootstrap/case_setup', 'AAA/bootstrap/white_tracking',
          'AAA/bootstrap/make_route_contract', 'AAA/bootstrap/bootstrap_axial']
must([s['label'] for s in stages] == labels, 'exact seven ordered original cold stages; no eighth/retry')
must([s['status'] for s in stages] == ['PASS'] * 6 + ['FAILED'], 'first six PASS and seventh FAILED')
must([s['wall_cap_seconds'] for s in stages] == [120.0] * 6 + [4200.0], 'original 120 setup/host and 4200 bootstrap stage caps')
must(status['classification'] == 'FAILED_NO_RETRY' and status['case'] == 'AAA', 'actual AAA no-retry status')
must(status['completed_maps'] == 0 and status['cases'] == {}, 'zero completed maps and no case map admission')
must(status['reference_qualification'] is None, 'actual reference qualification remains None')
must(status['wall_cap_seconds_per_case'] == 43200 and status['max_maps_per_case'] == 100,
     'original whole-case 43200 and 100-map caps')
must(status['error'] == stages[-1]['error'] == 'own-child 512 MiB RSS cap reached', 'status and failed stage identify own-child RSS cap')
must(claim['case'] == 'AAA' and claim['pid'] == 62618 and claim['prepared_sha256'] == status['prepared_sha256'],
     'permanent actual claim PID62618 and prepared pin')
must(pins[str(W / 'prepared_cold.json')]['sha256'] == claim['prepared_sha256'], 'claim/status pin actual prepared_cold bytes')
must(not (W / 'ABA').exists(), 'no ABA attempt directory')
must(sorted(p.name for p in (W / 'AAA').iterdir() if p.is_dir()) == ['bootstrap'],
     'AAA directory contains bootstrap only; no map directories')
must(not any((W / name).exists() for name in ('cold_source_complete_result.json', 'cold_closeout_seal.json')),
     'no complete cold return or successful closeout seal')
must(failure['classification'] == 'FAILED_COMBINED_COLD_NO_RETRY' and
     failure['error'] == "RuntimeError('own-child 512 MiB RSS cap reached')", 'original factory failure classification/error')
must(all(failure[k] is False for k in ('scientific_qualification', 'AAA_accuracy_qualified', 'ABA_admitted')),
     'failure has no scientific, AAA accuracy or ABA admission credit')
must(0 < failure['actual_elapsed_seconds'] < 43200, 'actual all-entry failed elapsed below original43200')
stage_summary = []
watch_fields = ('pid', 'returncode', 'elapsed_seconds', 'sampled_peak_rss_mib', 'limit_failure',
                'wall_cap_seconds', 'rss_cap_mib', 'own_child_only', 'liveness_group_cleanup',
                'own_pid_wait4_observed', 'own_pid_wait4_pid', 'own_pid_wait4_status',
                'own_pid_wait4_ru_maxrss_bytes', 'own_pid_wait4_peak_rss_mib',
                'observed_peak_rss_mib', 'live_rss_sample_count', 'rss_peak_observation_contract')
expected_pids = [62699, 62714, 62718, 62737, 62743, 62745, 62748]
markers = ['AXMAT-ARCHIVE-PACK-COMPLETE', 'AXMAT-COMMON-BASIS-COMPLETE',
           'AXMAT-RANK-RECORD-CHECK-COMPLETE', 'AXMAT-CASE-SETUP-COMPLETE',
           'AXMAT-WHITE-TRACKING-COMPLETE', None, 'AXMAT-BOOTSTRAP-AXIAL-COMPLETE']
for i, stage in enumerate(stages):
    label = stage['label']
    watch = read_json(W / (label + '.watchdog.json'))
    raw = read_raw(W / (label + '.log'))
    text = raw.decode('utf-8', 'replace')
    must(watch['command'] == stage['command'] and watch['pid'] == expected_pids[i], label + ': exact own command/PID')
    must(watch['own_child_only'] is True and watch['rss_cap_mib'] == 512 and
         watch['rss_peak_observation_contract'] == 'EXACT_OWN_PID_DARWIN_WAIT4_BYTES_AND_LIVE_PS_V1',
         label + ': original own-PID observation contract/cap')
    must(watch['liveness_group_cleanup'] is True, label + ': archived original cleanup observation true')
    must(0 < watch['elapsed_seconds'] < watch['wall_cap_seconds'] <= stage['wall_cap_seconds'],
         label + ': actual watch elapsed within shortened original stage cap')
    must(stage['elapsed_seconds'] >= watch['elapsed_seconds'], label + ': stage includes supervision elapsed')
    if i < 6:
        must(pins[str(W / (label + '.log'))]['sha256'] == stage['log_sha256'], label + ': raw success log matches stage SHA')
        must(watch['returncode'] == 0 and watch['limit_failure'] is None, label + ': actual success/no limit error')
        must(watch['own_pid_wait4_observed'] is True and watch['own_pid_wait4_pid'] == watch['pid'] and
             watch['own_pid_wait4_status'] == 0, label + ': successful terminal wait4 exact own PID')
        must(watch['own_pid_wait4_ru_maxrss_bytes'] / 2**20 == watch['own_pid_wait4_peak_rss_mib'],
             label + ': independent Darwin bytes/MiB conversion')
        must(watch['observed_peak_rss_mib'] == max(watch['sampled_peak_rss_mib'], watch['own_pid_wait4_peak_rss_mib']) < 512,
             label + ': actual successful observed peak below512')
        if i in (0, 1, 2, 3):
            must(re.search(r'^>\|' + re.escape(markers[i]) + r'(?:\s|$)', text, re.M) is not None,
                 label + ': executed Dragon completion marker')
            must('normal end of execution for dragon' in text, label + ': actual normal Dragon terminal')
        elif i == 4:
            must(markers[i] in text.splitlines(), label + ': actual host completion line')
    else:
        must(watch['returncode'] == -15 and watch['limit_failure'] == failure['error'], 'actual own-PID62748 SIGTERM/RSS error')
        must(watch['sampled_peak_rss_mib'] == watch['observed_peak_rss_mib'] == 512.890625 > 512 and
             watch['live_rss_sample_count'] == 460, 'failed live own-PID sampled peak512.890625 and460 actual samples')
        must(watch['elapsed_seconds'] == 122.09484879102092, 'actual failed watchdog elapsed122.09484879102092')
        must(watch['own_pid_wait4_observed'] is False and
             all(watch[k] is None for k in ('own_pid_wait4_pid', 'own_pid_wait4_status',
                                          'own_pid_wait4_ru_maxrss_bytes', 'own_pid_wait4_peak_rss_mib')),
             'failed cleanup retains unavailable exact wait4 fields as None')
        must('log_sha256' not in stage, 'failed original stage omits success-only log SHA; audit uses independent raw pin')
        listing = [dict(line=n, text=line) for n, line in enumerate(text.splitlines(), 1) if markers[i] in line]
        must(len(listing) == 1 and listing[0]['text'].startswith('ECHO "AXMAT-BOOTSTRAP-AXIAL-COMPLETE"') and
             re.search(r'\s\d{4,}$', listing[0]['text']) is not None,
             'one completion-marker substring is input source listing only')
        must(re.search(r'^>\|' + re.escape(markers[i]) + r'(?:\s|$)', text, re.M) is None and
             'normal end of execution for dragon' not in text,
             'no executed axial completion or normal Dragon terminal')
        must(not re.search(r'XABORT|ABORT:|FATAL|SIG(?:SEGV|FPE|BUS|ILL|ABRT)|fortran runtime error', text, re.I),
             'failed raw native log has no solver-abort diagnostic; termination is supervisor RSS kill')
    stage_summary.append(dict(label=label, status=stage['status'], original_stage_cap_seconds=stage['wall_cap_seconds'],
                              stage_elapsed_seconds=stage['elapsed_seconds'], watch={k: watch[k] for k in watch_fields}))
must(len(set(expected_pids)) == 7, 'seven distinct actual child PIDs, no retry stage')
must(all(stages[i]['started_unix'] + stages[i]['elapsed_seconds'] <= stages[i+1]['started_unix'] + .002
         for i in range(6)), 'ordered stages serial without overlapping recorded intervals')
src_f, tree_f = read_source(F, '7037cf10b98e0f5098a87bb87808940a85132abce48e6156db7b136eddcfbf71')
src_own, tree_own = read_source(OWN, 'ac51e68866f96547fa620fd971a911f93841a824412c3fe0a050bdbce00ae76b')
src_host, tree_host = read_source(W / 'runtime/combined_cold_own_rss_host.py', 'dd2fad02343cb8ae9d4a4df428ddaf00885d6204d00cf8a2bdd5ac48e00ecaf7')
src_runner, tree_runner = read_source(W / 'runtime/production_runner.py', '8333871a81a2c78e7a6a7fd2f68ec0ff8dc2bfe0ce94002b1d4ac9a33a5fff40')
src_bounded, tree_bounded = read_source(W / 'runtime/run_bounded_dragon.py', 'bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')
expected_budgets = dict(setup_seconds=120, bootstrap_axial_seconds=4200, bootstrap_radial_seconds=600,
                        radial_seconds=300, axial_seconds=4200, host_seconds=120, max_maps=100, total_seconds=43200)
f_budgets = {k: ast.literal_eval(v) for k, v in top_call_kwargs(tree_f, 'BUDGETS').items()}
must(prepared['budgets'] == f_budgets == expected_budgets, 'prepared and original factory all eight budget fields exact')
host_caps = top_call_kwargs(tree_host, 'CAPS')
must({k: ast.literal_eval(host_caps[k]) for k in ('rss_cap_mib', 'cold_total_seconds', 'threads', 'children_at_once', 'retries')} ==
     dict(rss_cap_mib=512, cold_total_seconds=43200, threads=1, children_at_once=1, retries=0),
     'original host512/43200/one thread/one child/zero retries caps')
own_class = node_named(tree_own, 'OwnRSSSerialExecutor', ast.ClassDef)
must([ast.unparse(x) for x in own_class.bases] == ['SerialExecutor'], 'original genuine inherited OwnRSSSerialExecutor source')
own_code = ast.unparse(own_class)
for fragment in ("os.wait4(process.pid, os.WNOHANG)", "pid != process.pid", "wait4_raw_maxrss = usage.ru_maxrss",
                 "wait4_peak = wait4_raw_maxrss / (1024.0 * 1024.0)", "if effective >= 512:",
                 "['/bin/ps', '-o', 'rss=', '-p', str(process.pid)]", "self.bounded.terminate_group(process)",
                 "failure = repr(error)", "self.bounded.finish_liveness_watchdog(write_fd, watchdog)"):
    must(fragment in own_code, 'original static own-PID/limit/cleanup implementation: ' + fragment)
make_code = source_of(src_host, tree_host, 'make_executor')
must('executor = full.OwnRSSSerialExecutor(Path(work), total_seconds, case, resources)' in make_code and
     "total_seconds != 43200" in make_code and 'executor.deadline = min(executor.deadline, started + total_seconds)' in make_code,
     'actual host creates genuine inherited guard under shortened original whole43200 deadline')
run_code = source_of(src_runner, tree_runner, 'run')
must('directory.mkdir()' in run_code and 'FAILED_NO_RETRY' in run_code and
     'executor = make_executor(work, budget.total_seconds, case, resources,' in run_code,
     'actual runner permanent claim, original no-retry abort, explicit own-PID executor constructor')
launch_code = source_of(src_f, tree_f, 'cold_launch_in_clean_process')
must("('AAA','archives','training')" in launch_code and 'one full fresh cold attempt' in launch_code and
     "result=c.run(OUTPUT/'prepared_cold.json',prepared_sha,'AAA',None,None)" in launch_code and
     "write_new(OUTPUT/'cold_source_failure.json'" in launch_code and
     "classification='FAILED_COMBINED_COLD_NO_RETRY'" in launch_code and
     "AAA_accuracy_qualified=False,ABA_admitted=False" in launch_code,
     'original final factory fresh claim, canonical actual run, original failure writer and creditfalse')
terminate = source_of(src_bounded, tree_bounded, 'terminate_process_group')
must('os.killpg(pgid, signal.SIGTERM)' in terminate and 'os.killpg(pgid, signal.SIGKILL)' in terminate,
     'original bounded group termination SIGTERM then bounded fallback SIGKILL')
must('terminate_process_group(process.pid, TERM_GRACE_SECONDS, process)' in source_of(src_bounded, tree_bounded, 'terminate_group'),
     'original termination targets actual own-child session group')
report = dict(schema='AXMAT_V12_INDEPENDENT_STD_LIB_FAILED_NATIVE_RAW_REVIEW_V1',
              classification='PASS_RAW_FAILURE_EVIDENCE_REVIEW_NO_SCIENTIFIC_CREDIT', defects=[],
              scope='Finite raw logs/watch/stages/claim/status/factory-failure and static original guard source; no business imports/calls, native or fixture execution, process polling, numerical payload reads, broad-history hashing, or project writes.',
              root_native_tool_reference=dict(dispatch_chunk='04a9cc', session_id=69320, final_chunk='1bacfa', exit_code=1,
                                              terminal_state='CLOSED', provenance='Parent-provided reference only; parent audits terminal evidence separately.'),
              original_budgets=expected_budgets, host_caps=dict(rss_cap_mib=512, cold_total_seconds=43200, threads=1, children_at_once=1, retries=0),
              stages=stage_summary, completion_marker_source_listing=listing,
              actual_status={k: status[k] for k in ('case', 'classification', 'completed_maps', 'cases', 'error', 'prepared_sha256',
                                                    'wall_cap_seconds_per_case', 'max_maps_per_case', 'reference_qualification')},
              actual_failure=failure, actual_claim=claim, raw_pins=pins,
              check_count=len(checks), checks=checks,
              limits=['Cleanup true is the archived observation produced after original bounded helper; this review does not probe current PID/group liveness.',
                      'Failed wait4 fields are unavailable and remain None; sampled512.890625 is a real own-PID live observation, not a reconstructed kernel peak.',
                      'The one axial-complete substring is source ECHO listing, not an executed >| completion line.',
                      'Failed native log has no original normal end or native solver-abort diagnostic; own-RSS supervisor termination is established jointly by watchdog/source/returncode.',
                      'No raw ps sample trace is separately archived; reviewed watchdog peak/sample count is the archived live observation.',
                      'Genuine loaded-object MRO and whole terminal closure are parent-reviewed; this finite review only corroborates pinned static guard/call source.',
                      'No physics, convergence, reference or AAA/ABA scientific admission is claimed.'])
OUT.mkdir(parents=True, exist_ok=True)
p = OUT / 'REPORT.json'
data = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
with p.open('xb') as stream:
    stream.write(data)
print(json.dumps(dict(classification=report['classification'], defects=[], check_count=len(checks),
                      report_path=str(p), report_sha256=hashlib.sha256(data).hexdigest(), report_bytes=len(data),
                      stages=[s['status'] for s in stages], completed_maps=status['completed_maps'],
                      failed_own_pid=expected_pids[-1], failed_peak_mib=stage_summary[-1]['watch']['sampled_peak_rss_mib'],
                      failed_returncode=-15, failed_wait4_fields_remain_None=True,
                      executed_axial_completion=False, source_listing_marker_only=True,
                      failed_elapsed_seconds=stage_summary[-1]['watch']['elapsed_seconds'],
                      factory_failure_elapsed_seconds=failure['actual_elapsed_seconds'], scientific_credit=False), sort_keys=True))
