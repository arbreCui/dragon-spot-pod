#!/usr/bin/env python3
"""Independent finite saved META audit; no reviewed Source execution/import."""
import ast
import collections
import hashlib
import json
import os
import pathlib
import shlex
import stat
import sys

HERE = pathlib.Path(__file__).parent
B = pathlib.Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E = B / 'actual_complete_combined_build_v21_receipts'
EXPECTED = {
    'Root_actual_failed_complete_combined_build_summary.json': ('8ad3faae061d6ebed13245c6446500e821c93cdd8b81b37f902a73db3ebdc8dc', 927120),
    'Root_actual_failed_build_namespace_manifest.json': ('d690769b29c3f73ed14d048caf819f57c9a31f800229960d27a7a9a3f1aee294', 92240),
    'Root_actual_failed_build_META_writer_tool_terminal_return.json': ('ec01dcc781552682cf2f02d8e28aa2d8e6517044e9102871eed39d94cd13b299', 5055),
    'Root_actual_build_tool_terminal_return.json': ('38815705e9e27c62e423dd4501ff41308d6ec1c219ea8ab9c264a27807420791', 2132),
    'Root_actual_failed_complete_build_postclose_input_check.json': ('d1b50da7b06fa22b1276960c7a55f03d33995a337093f0253d262b163f592101', 67718),
}
CHECKS = []
READS = []
def check(name, ok, details=None):
    row = {'check': name, 'PASS': bool(ok)}
    if details is not None: row['details'] = details
    CHECKS.append(row)
    return bool(ok)

def identity(st):
    return [st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size, st.st_mtime_ns, st.st_ctime_ns]

def normalized(pin):
    return {'path': pin['path'], 'sha256': pin['sha256'], 'identity': pin['identity']}

def hash_eof(path):
    path = pathlib.Path(path)
    before = identity(path.lstat())
    check('regular single link file: ' + str(path), stat.S_ISREG(before[2]) and before[3] == 1)
    h = hashlib.sha256(); count = 0
    with path.open('rb') as stream:
        check('descriptor identity before read: ' + str(path), identity(os.fstat(stream.fileno())) == before)
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk: break
            h.update(chunk); count += len(chunk)
        check('descriptor identity after complete EOF: ' + str(path), identity(os.fstat(stream.fileno())) == before)
    after = identity(path.lstat())
    check('full 7ID stable across complete EOF: ' + str(path), after == before)
    check('full EOF byte count: ' + str(path), count == before[4])
    actual = {'path': str(path), 'sha256': h.hexdigest(), 'size_bytes': count, 'identity': after}
    READS.append(actual)
    return actual

def verify_pin(pin, name=None):
    actual = hash_eof(pin['path'])
    check('exact saved SHA/7ID pin: ' + (name or pin['path']), normalized(actual) == normalized(pin), {'expected': pin, 'actual': actual})
    if 'size_bytes' in pin: check('saved explicit size: ' + pin['path'], actual['size_bytes'] == pin['size_bytes'])
    return actual

def read_meta(path, limit=2 * 1024 * 1024):
    path = pathlib.Path(path)
    check('bounded explicit META decode: ' + str(path), path.stat().st_size <= limit)
    if path.stat().st_size > limit: raise ValueError('META decode limit exceeded')
    with path.open('rb') as stream: raw = stream.read(limit + 1)
    return json.loads(raw)

def terminal_ok(value, code, chunk):
    return type(value.get('exit_code')) is int and value['exit_code'] == code and value.get('chunk_id') == chunk and 'session_id' not in value

def same_bytes(a, b):
    with pathlib.Path(a).open('rb') as sa, pathlib.Path(b).open('rb') as sb:
        while True:
            ca, cb = sa.read(1024 * 1024), sb.read(1024 * 1024)
            if ca != cb: return False
            if not ca: return True

def finite_tree(root):
    root = pathlib.Path(root); files={}; dirs={}; links={}
    for cur, ds, fs in os.walk(root, followlinks=False):
        cur = pathlib.Path(cur); rel = cur.relative_to(root).as_posix()
        dirs[rel] = identity(cur.lstat())
        for n in ds[:]:
            p=cur/n
            if p.is_symlink(): links[p.relative_to(root).as_posix()] = os.readlink(p); ds.remove(n)
        for n in fs:
            p=cur/n; r=p.relative_to(root).as_posix()
            if p.is_symlink(): links[r]=os.readlink(p)
            else: files[r] = identity(p.lstat())
    return files,dirs,links

fixed = {}
for name,(sha,size) in EXPECTED.items():
    actual=hash_eof(E/name)
    check('Root explicitly authorized saved META SHA/size: '+name, actual['sha256']==sha and actual['size_bytes']==size)
    fixed[name]=actual
summary=read_meta(E/'Root_actual_failed_complete_combined_build_summary.json')
manifest=read_meta(E/'Root_actual_failed_build_namespace_manifest.json')
writer_receipt=read_meta(E/'Root_actual_failed_build_META_writer_tool_terminal_return.json')
build=read_meta(E/'Root_actual_build_tool_terminal_return.json')
postcheck=read_meta(E/'Root_actual_failed_complete_build_postclose_input_check.json')
check('all actual schemas exact', [summary['schema'],manifest['schema'],writer_receipt['schema'],build['schema'],postcheck['schema']] == [
 'ROOT_V21_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_SUMMARY_V1',
 'ROOT_V21_ACTUAL_FAILED_BUILD_ALL_NAMESPACES_FULL_EOF_SHA7ID_V1',
 'ROOT_ACTUAL_V21_FAILURE_ONLY_META_WRITER_TOOL_TERMINAL_RETURN_V1',
 'ROOT_V21_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1',
 'ROOT_V21_ACTUAL_FAILED_COMPLETE_BUILD_POSTCLOSE_INPUT_CHECK_V1'])
check('genuine original build 875da7 strict int1 closed', terminal_ok(build['terminal_tool_return'],1,'875da7') and type(build['exit_code']) is int and build['exit_code']==1 and build['closed'] is True and build['session_repolled_after_close'] is False)
check('original last observation is true terminal', build['observations'][-1] == build['terminal_tool_return'])
check('saved summary keeps exact actual terminal and launch', summary['actual_terminal_tool_result']==build['terminal_tool_return'] and summary['actual_root_launch_arguments']==build['actual_launch_arguments'])
check('genuine failure-only META writer 1a8bff strict int0 closed', terminal_ok(writer_receipt['actual_tool_terminal_return'],0,'1a8bff') and type(writer_receipt['actual_root_meta_writer_exit_code']) is int and writer_receipt['actual_root_meta_writer_exit_code']==0 and writer_receipt['closed'] is True)
check('META int0 explicitly not build success', writer_receipt['original_build_is_failed_exit1_closed'] is True and writer_receipt['meta_exit0_is_not_build_success'] is True and writer_receipt['new_numeric_or_business_execution'] is False and writer_receipt['goal_complete'] is False)
tool_output=json.loads(writer_receipt['actual_tool_terminal_return']['output'])
for label in ('namespace_manifest','summary'):
    verify_pin(tool_output[label], 'actual 1a8bff output '+label)
check('actual writer stdout failure status/counts', tool_output['status']==summary['status']=='ACTUAL_NONZERO_BUILD_CLOSED_NO_RETRY_NO_SUCCESS_RECEIPT' and type(tool_output['actual_root_exit_code']) is int and tool_output['actual_root_exit_code']==1 and tool_output['observed_PASS_stage_labels']==summary['observed_PASS_stage_labels'] and tool_output['dynamic_SOURCE_count']==30 and tool_output['fixed_input_entry_count']==62 and tool_output['joint_archive_bytes']==summary['joint_archive_bytes_after_summary'] and tool_output['no_success_whole_INPUT_native_science_credit'] is True)
check('genuine archive tool strict int0 closed before writer', terminal_ok(writer_receipt['source_archive_actual_tool_return'],0,'53a9e5'))
archive_output=json.loads(writer_receipt['source_archive_actual_tool_return']['output'])
check('archive explicitly Source-only before writer', archive_output['status']=='FULL_FAILURE_ONLY_META_SOURCE_AND_PEER_ARCHIVED_NOT_EXECUTED' and archive_output['copied_files']==16 and archive_output['complete_Source30_unchanged'] is True)

check('complete six namespaces exact order and counts', len(manifest['namespaces'])==6 and [len(n['files']) for n in manifest['namespaces']]==[5,11,11,11,30,29] and [len(n['directories']) for n in manifest['namespaces']]==[4,2,6,1,3,3])
H,S,O,T,D,Er=[pathlib.Path(n['root']) for n in manifest['namespaces']]
check('explicit namespace roots authorized', str(H)=='/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v21-20261010' and str(S)=='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010' and str(O)=='/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010' and str(T)=='/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010' and D==B/'actual_complete_combined_build_v21_sources' and Er==E)
later_E=set(EXPECTED)-{'Root_actual_build_tool_terminal_return.json','Root_actual_failed_complete_build_postclose_input_check.json'}
namespace_results=[]; snapshot_bytes=0; current_namespace_bytes=0
for label,ns in zip(('H','S','O','T','D','E'),manifest['namespaces']):
    root=pathlib.Path(ns['root']); files,dirs,links=finite_tree(root)
    expected_files=set(ns['files']) | (later_E if label=='E' else set())
    check(label+' complete finite namespace file set, no crop', set(files)==expected_files, {'expected':sorted(expected_files),'actual':sorted(files)})
    check(label+' complete finite namespace directories and symlinks', set(dirs)==set(ns['directories']) and links==ns['symlinks']=={} and ns['present'] is True)
    for rel,pin in ns['files'].items():
        check(label+' pin path matches root relative path: '+rel, pathlib.Path(pin['path'])==root/rel)
        verify_pin(pin,label+'/'+rel);snapshot_bytes+=pin['identity'][4]
    for rel,pinid in ns['directories'].items():
        if label=='E' and rel=='.':
            check('E root directory updated only at documented append boundary', dirs[rel]!=pinid and dirs[rel][:3]==pinid[:3],{'snapshot_7ID':pinid,'current_7ID':dirs[rel]})
        else: check(label+' unchanged directory full 7ID: '+rel, dirs[rel]==pinid)
    current_namespace_bytes+=sum(i[4] for i in files.values())
    namespace_results.append({'label':label,'root':str(root),'snapshot_file_count':len(ns['files']),'current_file_count':len(files),'directories':dirs,'symlinks':links,'snapshot_files':ns['files'],'current_E_append_only':sorted(later_E) if label=='E' else []})
check('manifest E boundary explicit not false forever-stable claim', manifest['E_root_complete_snapshot_before_this_manifest_and_summary'] is True and manifest['E_root_directory_full7stable_after_metadata_append_required'] is False and manifest['unchanged_namespace_roots_require_full7stable'] is True)

freeze=read_meta(E/'Root_prelaunch_complete_build_source_freeze.json')
preflight=read_meta(E/'Root_final_prelaunch_source_input_and_reserve_check.json')
check('all30 Source freeze files and all3 directories exact preserved', freeze['source_root']==str(D) and freeze['actual_complete_SOURCE_file_count']==30 and freeze['complete_files']==preflight['complete_SOURCE_files'] and freeze['complete_directories']==preflight['complete_SOURCE_directories'] and {k:normalized(v) for k,v in freeze['complete_files'].items()}=={k:normalized(v) for k,v in manifest['namespaces'][4]['files'].items()} and freeze['complete_directories']==manifest['namespaces'][4]['directories'] and freeze['symlinks']=={} and freeze['no_SOURCE_append_after_freeze'] is True)
fixed62=preflight['fixed_input_pins']
check('original62 complete ordered fixed pins preserved', len(fixed62)==62 and preflight['fixed_input_entries_count']==62 and fixed62==summary['original_fixed_input_expected_pins']==manifest['ordered_original_fixed_input_pins']==postcheck['Root_postclose_all62_build_fixed_input_entries_unchanged'])
check('all62 ordered results keep all indices and pin types', len(summary['ordered_fixed_input_unchanged_results'])==62 and all(type(row['index']) is int and row['index']==i and normalized(row['pin'])==normalized(fixed62[i]) for i,row in enumerate(summary['ordered_fixed_input_unchanged_results'])))
ordered62_actual=[]
for i,pin in enumerate(fixed62): ordered62_actual.append({'index':i,'actual':verify_pin(pin,'original fixed ordered index '+str(i))})
duplicates={p:[i for i,pin in enumerate(fixed62) if pin['path']==p] for p,c in collections.Counter(pin['path'] for pin in fixed62).items() if c>1}
check('duplicate fixed pins intentionally kept, no dedup/reorder', bool(duplicates) and summary['original_fixed_input_failures']==[] and summary['all_original_fixed_input_pins_unchanged'] is True and summary['original_fixed_input_entry_count']==62,duplicates)

prepared_check=summary['original_prepared_metadata_check']; verify_pin(prepared_check['original_manifest'],'original PREP namespace manifest')
prep_manifest=read_meta(prepared_check['original_manifest']['path'])
prep_by_root={n['root']:n for n in prep_manifest['namespaces']}
check('original prepared S11/T6/O4 complete sets', len(prep_by_root[str(S)]['files'])==11 and len(prep_by_root[str(T)]['files'])==6 and len(prep_by_root[str(O)]['files'])==4 and set(prep_by_root[str(O)]['files'])=={'declaration.json','input_graph.json','input_creation_python_open_trace.json','runtime/run_bounded_dragon.py'})
expected_original=[]
for root in (S,T,O):
    ordered_original_relatives = ['declaration.json','input_graph.json','input_creation_python_open_trace.json','runtime/run_bounded_dragon.py'] if root==O else list(prep_by_root[str(root)]['files'])
    for rel in ordered_original_relatives:
        pin=prep_by_root[str(root)]['files'][rel]
        current=next(n for n in manifest['namespaces'] if n['root']==str(root))['files'][rel]
        check('original PREP file full byte/SHA/7ID unchanged: '+str(root/rel), normalized(pin)==normalized(current))
        expected_original.append({'scope':'ORIGINAL_PREP_OUT_FOUR_FILES' if root==O else 'ORIGINAL_PREPARED_SOURCE_OR_TERMINAL','relative_path':rel,'pin':normalized(pin)})
check('saved original PREP check includes exactly21 complete entries, full original S/T then declared O4 order', len(prepared_check['verified_original_entries'])==21 and [{**row,'pin':normalized(row['pin'])} for row in prepared_check['verified_original_entries']]==expected_original)
check('PREP stable flags truthful S/T and O4', prepared_check['failures']==[] and prepared_check['original_S_T_entries_unchanged'] is True and prepared_check['original_PREP_OUT_four_unchanged'] is True and summary['original_PREP_SOURCE_TERMINAL_unchanged'] is True and summary['original_PREP_OUT_four_unchanged'] is True)
check('old PREP terminal did not capture root7ID', prep_by_root[str(T)]['directories']==[])
for row in prep_by_root[str(S)]['directories']: check('old PREP source captured directory stable '+row['path'],identity((S/row['path']).lstat())==row['identity'])
old67=prep_manifest['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged']; root67=postcheck['Root_postclose_all67_original_PREP_fixed_inputs_unchanged']
check('original67 Root postclose observation complete ordered META agrees with original67', len(old67)==len(root67)==67 and [normalized(p) for p in old67]==[normalized(p) for p in root67])
original67_scope='This peer independently checked only the explicitly authorized 62 current host fixed inputs by fresh EOF/SHA7ID. The complete ordered original 67 PREP pins were compared as META between the original PREP manifest and Root postclose receipt, without re-reading additional payloads. Root original67 revalidation is its observation, not a substitute by the 62 and not this peer independent67 physical input PASS.'

failed_T=read_meta(T/'failed_build_terminal_return.json')
verify_pin(summary['failed_terminal_receipt'],'saved failed T receipt')
check('saved failed T and summary complete common fields identical', all(v==summary[k] for k,v in failed_T.items() if k in summary and k!='schema'))
check('failed T distinct schema and exact failure exit1 closed', failed_T['schema']=='ROOT_V21_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1' and type(failed_T['returncode']) is int and failed_T['returncode']==1 and failed_T['actual_tool_session_closed'] is True)
outer=read_meta(H/'run/build.watchdog.json'); failed_host=read_meta(H/'failed_host_result.json'); outer_stages=read_meta(H/'COMPLETE_COMBINED_BUILD/stages.json'); inner=read_meta(O/'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V21/stages.json')
check('saved complete actual failure objects exact', summary['actual_saved_failure_metadata']=={'failed_host_result':failed_host,'outer_watchdog':outer,'inner_stage_table':inner})
check('outer ownwatch real512 excess, -15 and cleanup', type(outer['returncode']) is int and outer['returncode']==-15 and outer['sampled_peak_rss_mib']==514.203125 and outer['rss_cap_mib']==512 and outer['sampled_peak_rss_mib']>outer['rss_cap_mib'] and outer['elapsed_seconds']==170.78790579200722 and outer['elapsed_seconds']<outer['wall_cap_seconds']<=1800 and outer['own_child_only'] is True and outer['liveness_group_cleanup'] is True and outer['limit_failure']=="RuntimeError('own-child 512 MiB RSS cap reached')")
check('summary outer fields all exact actual watch', all(outer[k]==v for k,v in summary['actual_outer_watchdog_summary'].items()))
check('outer failed stage table complete exact failed host records', outer_stages['stages']==failed_host['stage_records'] and len(outer_stages['stages'])==1 and outer_stages['stages'][0]['label']=='run/build' and outer_stages['stages'][0]['status']=='FAILED' and outer_stages['stages'][0]['command']==outer['command'] and failed_host['status']=='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY')
host_ast=ast.parse((D/'combined_build_host.py').read_bytes(),filename=str(D/'combined_build_host.py'))
expected_commands=next(ast.literal_eval(n.value) for n in host_ast.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED_COMMANDS' for t in n.targets))
check('original complete stage command plan still five', len(expected_commands)==5)
check('two real PASS stages are complete original prefix only', len(inner['stages'])==summary['observed_stage_count']==postcheck['completed_inner_stages']==2 and [r['label'] for r in inner['stages']]==summary['observed_PASS_stage_labels']==['build/link','metadata/objects'] and all(r['status']=='PASS' for r in inner['stages']) and [r['command'] for r in inner['stages']]==expected_commands[:2])
for i,row in enumerate(summary['actual_observed_partial_inner_stages']):
    check('complete stage '+str(i)+' saved row exact, all resource fields', row['stage']==inner['stages'][i])
    log=verify_pin(row['complete_log'],'inner full log '+str(i)); watchpin=verify_pin(row['watchdog'],'inner full watch '+str(i)); watch=read_meta(watchpin['path'])
    check('inner actual watch exact command/log/status/caps '+str(i), row['actual_watchdog_fields']==watch and watch['command']==row['stage']['command'] and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True and watch['rss_cap_mib']==512 and 0<watch['wall_cap_seconds']<=row['stage']['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<=512 and log['sha256']==row['stage']['log_sha256'])

sources=manifest['original_sources']
for label,pin in sources.items(): verify_pin(pin,'original source anchor '+label)
streams={'parent-stdout':sources['parent-stdout']['path'],'parent-stderr':sources['parent-stderr']['path'],'root-terminal':sources['root-terminal']['path'],'actual-child-merged':str(H/'run/build.log')}
for label,pin in failed_T['actual_original_full_stream_copies'].items():
    verify_pin(pin,'full stream saved copy '+label)
    check('full original stream byte equality, complete EOF: '+label,same_bytes(streams[label],pin['path']),{'original':streams[label],'copy':pin})
check('four original stream copies complete exact set',set(streams)==set(failed_T['actual_original_full_stream_copies'])=={'parent-stdout','parent-stderr','root-terminal','actual-child-merged'})
merged_source=verify_pin(summary['original_executor_merged_capture_source'],'original capture semantics Source')
tree=ast.parse(pathlib.Path(merged_source['path']).read_bytes())
check('original Source actually uses Popen stderr=subprocess.STDOUT', any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='subprocess' and n.func.attr=='Popen' and any(k.arg=='stderr' and isinstance(k.value,ast.Attribute) and isinstance(k.value.value,ast.Name) and k.value.value.id=='subprocess' and k.value.attr=='STDOUT' for k in n.keywords) for n in ast.walk(tree)))
check('two real stream scopes honest, no independent child stderr claimed', summary['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and summary['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and summary['separate_child_stderr_captured'] is False and summary['independent_child_stderr_empty_verified'] is False and summary['original_peak_RSS_source_line_observed'] is False and summary['cleanup_performed_by_metadata_writer'] is False)
for pin in summary['actual_fixed_Source_pins']: verify_pin(pin,'actual fixed Source/qualification pin')
writerpin=verify_pin(summary['actual_metadata_writer_source'],'actual failure-only META writer Source')
check('writer Source exact approved SHA',writerpin['sha256']=='7cbe4b7e2dfee381cf6b60fd720c38d1f4a38119d8b48506a3d330a1789ec6e9')
argv=shlex.split(writer_receipt['actual_launch_arguments']['cmd'])
check('actual writer argv targets only approved failure writer',argv[:3]==['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',writerpin['path']] and argv[3]=='--writer-sha256' and argv[4]==writerpin['sha256'])
for label,arg in [('root-terminal','--root-terminal'),('source-freeze','--source-freeze'),('prelaunch-pins','--prelaunch-pins'),('parent-stdout','--parent-stdout'),('parent-stderr','--parent-stderr')]:
    check('actual argv exact original Source/META pin '+label,argv[argv.index(arg)+1]==sources[label]['path'] and argv[argv.index(arg+'-sha256')+1]==sources[label]['sha256'])
caps={'whole_wall_cap_seconds':1800,'inner_stage_wall_cap_seconds':600,'rss_cap_mib':512,'joint_archive_cap_bytes':2147483648,'history_cap_bytes':103079215104,'free_floor_bytes':8589934592,'threads':1,'children_at_once':1,'retries':0}
pre_caps={'whole_seconds_cap':1800,'stage_seconds_cap':600,'rss_mib_cap':512,'joint_archive_cap_bytes':2147483648,'history_cap_bytes':103079215104,'free_floor_bytes':8589934592,'threads':1,'children':1,'retries':0}
check('all original caps exact ints remain fixed',all(type(summary[k]) is int and summary[k]==v and failed_T[k]==v for k,v in caps.items()) and all(type(preflight[k]) is int and preflight[k]==v for k,v in pre_caps.items()) and summary['original_caps_preserved'] is True)
check('original launch explicit all one-thread env',all(x+'=1' in build['actual_launch_arguments']['cmd'] for x in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS']))
check('all six success closeout files genuinely absent',set(summary['actual_success_closeout_files_absent'])=={'seal.json','driver_result.json','raw_metadata_receipt.json','audit/result.json','audit/binary_identity.json','closeout_failure.json'} and all(v is True and not (O/k).exists() for k,v in summary['actual_success_closeout_files_absent'].items()))
check('no success T terminal built or supplied',(T/'terminal_return.json').exists() is False)
science=['whole_combined_INPUT_admitted','production_admission_API_executed','new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved','mathematical_controls_newly_executed','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete']
check('all scientific/admission/success flags strict false',all(summary[k] is False and failed_T[k] is False for k in science) and summary['successful_new_runtime_build_observed'] is False and summary['all_five_original_stages_passed'] is False and summary['all_five_build_stages_passed'] is False and manifest['all_success_credit'] is False)
check('Root postclose explicitly not original host finalPASS',summary['original_host_final_input_revalidation_observed'] is False and summary['Root_postclose_pin_checks_do_not_replace_unreached_host_input_finalpass'] is True and summary['full_declared_physical_input_finalpass_claimed'] is False and postcheck['normal_host_final_input_PASS_reached'] is False and postcheck['Root_postclose_observation_is_not_host_final_PASS'] is True and manifest['Root_postclose_revalidation_is_not_original_host_final_input_PASS'] is True)
check('META no new business or cleaning claim',summary['no_project_API_guard_numeric_or_build_executed_by_metadata_writer'] is True and manifest['no_project_API_or_numeric_business_called'] is True and postcheck['metadata_decoded_only_no_new_numeric_execution'] is True)
before=snapshot_bytes+summary['actual_fixed_Source_pins'][0]['identity'][4]+writerpin['size_bytes']+EXPECTED['Root_actual_failed_build_namespace_manifest.json'][1]
after=before+EXPECTED['Root_actual_failed_complete_combined_build_summary.json'][1]
current=current_namespace_bytes+summary['actual_fixed_Source_pins'][0]['identity'][4]+writerpin['size_bytes']
check('joint archive accounting exact time boundaries',before==summary['joint_archive_bytes_before_summary']==149338093 and after==summary['joint_archive_bytes_after_summary']==150265213 and current==after+EXPECTED['Root_actual_failed_build_META_writer_tool_terminal_return.json'][1]==150270268 and current<2147483648,{'before_summary':before,'after_summary_before_METAtoolreceipt':after,'current_after_METAtoolreceipt':current})
for label,ns in zip(('H','S','O','T','D','E'),manifest['namespaces']):
    files,dirs,links=finite_tree(ns['root'])
    first=next(row for row in namespace_results if row['label']==label)
    check('namespace full directory identity stable during independent audit '+label,dirs==first['directories'] and links==first['symlinks'])
report={'schema':'INDEPENDENT_V21_ACTUAL_SAVED_FAILED_META_REVIEW_V1','scope':'FINITE_STANDARD_LIBRARY_SAVED_META_EOF_SHA7ID_ONLY','independent_reviewer_did_not_author_failure_writer':True,'hard_blockers':[r for r in CHECKS if not r['PASS']],'PASS':all(r['PASS'] for r in CHECKS),'check_count':len(CHECKS),'checks':CHECKS,'namespace_results':namespace_results,'full_EOF_reads':READS,'ordered_original62_actual_results':ordered62_actual,'ordered_original62_duplicate_indices':duplicates,'original67_scope':original67_scope,'original67_META_ordered_original':old67,'original67_META_Root_postclose':root67,'actual_build_terminal':build['terminal_tool_return'],'actual_META_writer_terminal':writer_receipt['actual_tool_terminal_return'],'actual_outer_watchdog':outer,'actual_two_inner_stage_labels':summary['observed_PASS_stage_labels'],'caps':caps,'streams_scope':{'child_stream':'canonical child stdout+stderr already merged by original subprocess.STDOUT','external_host_stream':'actual Root parent stderr separately preserved','all_four_original_streams_full_bytes_verified':True,'empty_original_streams_are_observations_not_constructed_empty_stderr':True},'E_snapshot_boundary':{'snapshot29_then_append_only':sorted(later_E),'current32':True,'E_root_full7ID_stable_forever_claimed':False},'joint_archive_accounting':{'before_summary':before,'after_summary_before_METAtoolreceipt':after,'current_after_METAtoolreceipt':current},'no_import_or_run_reviewed_source_API_guard_numeric_compile_or_build':True,'no_old_closed_session_poll':True,'no_project_or_original_package_write':True,'no_material_numeric_payload_decoded':True,'only_explicit_declared_namespace_files_stream_hashed':True,'actual_original67_physical_independent_check_by_this_peer':False,'science_credit':{k:False for k in science},'conclusion':'Saved failure evidence independently verified; original build remains failed 2/5 PASS, 514.203125 MiB >512, exit1 closed, no successful closeout or science admission. Root must satisfy a fresh complete protocol before any new helper/runtime qualification.'}
raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode();(HERE/'INDEPENDENT_ACTUAL_SAVED_META_REVIEW.json').write_bytes(raw)
print(json.dumps({'status':'INDEPENDENT_SAVED_FAILED_META_PASS' if report['PASS'] else 'INDEPENDENT_SAVED_FAILED_META_BLOCKED','check_count':len(CHECKS),'hard_blocker_count':len(report['hard_blockers']),'review_path':str(HERE/'INDEPENDENT_ACTUAL_SAVED_META_REVIEW.json'),'review_sha256':hashlib.sha256(raw).hexdigest(),'review_bytes':len(raw),'original_build_exit_code':1,'META_writer_exit_code':0,'observed_PASS_stage_count':2,'outer_sampled_peak_RSS_mib':514.203125,'joint_current_after_METAtoolreceipt_bytes':current,'original67_independent_physical_check':False},ensure_ascii=False))
sys.exit(0 if report['PASS'] else 1)
