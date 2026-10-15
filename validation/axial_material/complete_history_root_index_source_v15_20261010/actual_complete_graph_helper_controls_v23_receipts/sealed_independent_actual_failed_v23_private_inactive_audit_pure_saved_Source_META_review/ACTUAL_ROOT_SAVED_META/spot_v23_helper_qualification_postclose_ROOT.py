"""Preserve actual closed tool observations and complete saved H/O/D/E bytes."""
from pathlib import Path
import importlib.util
import json
import os
import shutil
import stat
import sys

def main():
    kind, bundle_path, prelaunch_path = sys.argv[1:]
    assert kind in ('pure', 'fresh') and sys.dont_write_bytecode and not sys.flags.optimize
    cpath = Path('/private/tmp/spot_install_freeze_v23_COMPLETE_BOUND_helper_qualification_ROOT.py')
    spec = importlib.util.spec_from_file_location('Root_frozen_qualification_namespace_constants', cpath)
    c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    spec = importlib.util.spec_from_file_location('Root_frozen_qualification_Source_pin_support', c.INSTALLER)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    dname, ename, hname, oname = c.KINDS[kind]
    d = c.B / dname; e = c.B / ename; h = c.ART / hname; o = c.ART / oname
    def view(root, excludes=(), allow_output_aliases=False):
        if not root.is_dir():
            return dict(root=str(root), present=False, files=[], directories={})
        aliases = []
        files = []
        for p in sorted(root.rglob('*')):
            if p in excludes:
                continue
            if p.is_symlink():
                m.require(allow_output_aliases, 'Source/receipt aliases forbidden')
                before = m.identity(p); target = os.readlink(p)
                m.require(stat.S_ISLNK(before[2]) and m.identity(p) == before, 'actual output alias exact lstat')
                aliases.append(dict(path=str(p), identity=before, symlink_target_text=target,
                                    actual_resolved_target_full_EOF_pin=m.full_pin(p.resolve())))
            elif p.is_file():
                files.append(m.full_pin(p))
        result = dict(root=str(root), files=files,
                    directories={'.': m.identity(root), **{p.relative_to(root).as_posix(): m.identity(p) for p in sorted(root.rglob('*')) if p.is_dir()}})
        if allow_output_aliases:
            result['original_fixture_symlinks'] = aliases
        return result
    bundle, bundle_pin = m.read(bundle_path)
    terminal = bundle['terminal_tool_return']
    m.require(type(terminal.get('exit_code')) is int and terminal.get('session_id') is None
              and type(terminal.get('chunk_id')) is str and type(terminal.get('output')) is str,
              'actual closed terminal is required; never infer closure')
    observations = bundle['observations']
    m.require(type(observations) is list and len(observations) > 0
              and observations[-1]['actual_tool_return'] == terminal, 'complete real observation sequence')
    pre, pre_pin = m.read(prelaunch_path)
    m.require(pre['kind'] == kind and pre['D'] == view(d) and pre['E'] == view(e),
              'whole D and original E unchanged throughout actual host execution')
    m.require([m.full_pin(p, sha) for p, sha in m.PROTECTED.items()] == pre['original_helper_Q_canonical']
              and m.full_pin(m.HELPER, m.HELPER_SHA) == pre['installed_helper'], 'actual helper/Q/canonical unchanged')
    receipt = dict(schema='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_TOOL_TERMINAL_RETURN_V1',
                   kind=kind, closed=True, actual_tool_terminal_return_observed=True,
                   terminal_tool_return=terminal, actual_command=bundle['actual_command'], observations=observations,
                   original_outputs_preserved=True, merged_stdout_stderr_only=True,
                   independent_stdout_captured=False, independent_stderr_captured=False,
                   new_actual_helper_qualification=None, AAA_accuracy_qualified=False, ABA_admitted=False)
    tp = e / 'Root_actual_complete_qualification_tool_terminal_return.json'
    m.write_new(tp, receipt)
    log = e / 'Root_actual_complete_qualification_outer_merged_stdout_stderr.log'
    m.require(not log.exists(), 'new closed merged log')
    log.write_text(''.join(x['actual_tool_return']['output'] for x in observations))
    shutil.copyfile(prelaunch_path, e / 'Root_actual_complete_qualification_prelaunch_frozen_D_E.json')
    shutil.copyfile(__file__, e / Path(__file__).name)
    mp = e / 'Root_actual_complete_qualification_postclose_namespace_manifest.json'
    sp = e / 'Root_actual_complete_qualification_postclose_summary.json'
    m.write_new(mp, {}); m.write_new(sp, {})
    namespace = dict(schema='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_FULL_EOF_NAMESPACE_V1',
                     kind=kind, closed_actual_tool= m.full_pin(tp), views={'H':view(h),'O':view(o,allow_output_aliases=True),'D':view(d),'E':view(e,(mp,sp))},
                     E_explicit_self_excluded_current_writer_outputs=[str(mp),str(sp)],
                     all_declared_members_fresh_full_EOF_SHA7ID=True, original_frozen_D_E_unchanged_before_writer=True,
                     original_output_fixture_symlinks_retained_with_exact_link_text_lstat_and_target_full_EOF=True,
                     new_actual_helper_qualification=None)
    mp.write_text(json.dumps(namespace, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    host = json.loads((h / 'result.json').read_bytes()) if (h / 'result.json').exists() else None
    failed = json.loads((h / 'failed_host_result.json').read_bytes()) if (h / 'failed_host_result.json').exists() else None
    watch = json.loads((h / 'run/admit.watchdog.json').read_bytes()) if (h / 'run/admit.watchdog.json').exists() else None
    expected_status = ('ACTUAL_PURE_GRAPH_PROTOCOL_CONTROLS_EXTERNAL_ROOT_REQUIRED' if kind == 'pure'
                       else 'ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED')
    successful = (terminal['exit_code'] == 0 and type(host) is dict and host['status'] == expected_status
                  and type(watch) is dict and type(watch.get('returncode')) is int and watch['returncode'] == 0
                  and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True
                  and len(host['stage_records']) == 1 and host['stage_records'][0]['status'] == 'PASS')
    m.require(type(successful) is bool, 'typed actual result classification')
    summary = dict(schema='ROOT_V23_ACTUAL_COMPLETE_HELPER_QUALIFICATION_POSTCLOSE_SUMMARY_V1', kind=kind,
                   status=('ACTUAL_COMPLETE_CONTROLS_CLOSED0_PENDING_INDEPENDENT_SAVED_REVIEW' if successful
                           else 'ACTUAL_COMPLETE_CONTROLS_CLOSED_FAILURE_NO_RETRY'),
                   actual_closed=True, actual_exit_code=terminal['exit_code'], actual_terminal_chunk_id=terminal['chunk_id'],
                   actual_complete_control_success=successful, actual_host_status=None if host is None else host['status'],
                   actual_failure=failed, whole_host_seconds=None if host is None else host['whole_seconds'],
                   actual_child_seconds=None if watch is None else watch['elapsed_seconds'],
                   actual_own_child_sampled_peak_RSS_MiB=None if watch is None else watch['sampled_peak_rss_mib'],
                   frozen_D_files=len(pre['D']['files']), frozen_D_directories=len(pre['D']['directories']),
                   frozen_E_files=len(pre['E']['files']), frozen_E_directories=len(pre['E']['directories']),
                   whole_frozen_D_E_files_and_directories_unchanged_before_writer=True,
                   actual_terminal_receipt=m.full_pin(tp), actual_prelaunch=m.full_pin(e / 'Root_actual_complete_qualification_prelaunch_frozen_D_E.json'),
                   namespace_manifest=m.full_pin(mp), Root_actual_bundle=bundle_pin, Source_postclose_writer=m.full_pin(Path(__file__).resolve()),
                   normal_host_archive_scope='H+O+D' if kind == 'pure' else 'H+O+D+E',
                   original_archive_cap_bytes=64*2**20, normal_HOD_bytes=None, complete_HODE_bytes=None,
                   complete_HODE_bytes_accounting_includes_all_current_writer_outputs=True,
                   independent_saved_review_pending=True, new_actual_helper_qualification=None,
                   actual_complete_build_qualified=False, whole_INPUT_admitted=False,
                   native_RSS_qualified=False, AAA_accuracy_qualified=False, ABA_admitted=False)
    def size(roots):
        return sum(p.lstat().st_size for root in roots if root.is_dir() for p in root.rglob('*')
                   if stat.S_ISREG(p.lstat().st_mode))
    for _ in range(8):
        hod = size((h,o,d)); hode = size((h,o,d,e))
        if summary['normal_HOD_bytes'] == hod and summary['complete_HODE_bytes'] == hode:
            break
        summary.update(normal_HOD_bytes=hod, complete_HODE_bytes=hode,
                       original_normal_archive_under_cap=(hod if kind=='pure' else hode) < 64*2**20,
                       Root_separate_conservative_HODE_under_64MiB=hode < 64*2**20)
        sp.write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + '\n')
    else:
        raise ValueError('complete archive byte accounting did not stabilize')
    m.require(size((h,o,d,e)) == summary['complete_HODE_bytes'], 'actual full final HODE size')
    m.require(view(d) == pre['D'], 'whole D changed during postclose Source/META retention')
    for pin in pre['E']['files']:
        m.require(m.full_pin(pin['path'],pin['sha256']) == pin, 'original E complete file changed')
    print(json.dumps(dict(summary=m.full_pin(sp), namespace_manifest=m.full_pin(mp), actual_terminal_receipt=m.full_pin(tp),
                          actual_closed_success=successful, actual_exit_code=terminal['exit_code'],
                          actual_child_seconds=summary['actual_child_seconds'], actual_sampled_RSS_MiB=summary['actual_own_child_sampled_peak_RSS_MiB'],
                          normal_HOD_bytes=summary['normal_HOD_bytes'], complete_HODE_bytes=summary['complete_HODE_bytes'],
                          new_actual_helper_qualification=None), separators=(',', ':')))

if __name__ == '__main__':
    main()
