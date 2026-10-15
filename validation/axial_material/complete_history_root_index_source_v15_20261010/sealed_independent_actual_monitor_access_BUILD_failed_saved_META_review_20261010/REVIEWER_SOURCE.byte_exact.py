"""Finite independent saved-failure Source/small META audit. Never import project code.

Root must supply actual already CLOSED writer/tool pins in a strict small contract.
No executable, graph, trace, material, DB, archive or numerical payload is decoded.
Only frozen installer Source and the explicitly selected small META/streams are
hashed; other physical entries receive a separately labelled lstat-only check.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat

BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
D=BASE/'actual_complete_combined_build_v25_monitor_access_sources'
E=BASE/'actual_complete_combined_build_v25_monitor_access_receipts'
H=ART/'axial-material-complete-combined-build-host-v25-monitor-access-20261010'
S=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-monitor-access-20261010'
O=ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-monitor-access-20261010'
T=ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-monitor-access-20261010'
FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'
LABELS=['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
FALSE_FIELDS=('whole_combined_INPUT_admitted','production_admission_API_executed',
    'new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved',
    'mathematical_controls_newly_executed','actual_full_FLU_entry_executed',
    'AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete')
CAPS=dict(whole_wall_cap_seconds=1800,inner_stage_wall_cap_seconds=600,rss_cap_mib=512,
    joint_archive_cap_bytes=2*2**30,history_cap_bytes=96*2**30,free_floor_bytes=8*2**30,
    threads=1,children_at_once=1,retries=0)
SMALL_META_LIMIT=16*2**20
checks=[];blockers=[];fullpins={};identity_only_paths=set();parsed_sources=[]

def check(name,value,detail=None):
    value=value is True
    checks.append(dict(name=name,typed_true=value,detail=detail))
    if not value: blockers.append(name)
    return value

def identity(p):
    q=Path(p).lstat()
    return [q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns]

def ordinary(p,directory=False):
    p=Path(p)
    if not p.is_absolute() or '..' in p.parts: raise ValueError('absolute ordinary path required')
    for q in [*reversed(p.parents),p]:
        i=identity(q)
        if stat.S_ISLNK(i[2]) or (q!=p and not stat.S_ISDIR(i[2])):
            raise ValueError('ordinary ancestors required: '+str(q))
    if directory and not stat.S_ISDIR(identity(p)[2]): raise ValueError('ordinary directory required')
    return p

def pin(p,source=False):
    p=ordinary(p);before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular Source/META required')
    if not source and before[4]>SMALL_META_LIMIT: raise ValueError('small META bound exceeded')
    if not source and any(x in p.name.lower() for x in ('input_graph','open_trace','material','database')):
        raise ValueError('payload read prohibited: '+str(p))
    with p.open('rb') as f: sha=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('changed while reading full EOF: '+str(p))
    q=dict(path=str(p),sha256=sha,identity=before)
    fullpins[str(p)]=q
    return q

def normalized(q):
    i=q.get('identity',q.get('identity7'))
    if type(i) is not list or len(i)!=7 or any(type(v) is not int for v in i):
        raise ValueError('strict seven integer identity required')
    if 'identity' in q and 'identity7' in q and q['identity']!=q['identity7']:
        raise ValueError('identity aliases differ')
    return dict(path=q['path'],sha256=q['sha256'],identity=i)

def fullcheck(name,q,source=False):
    want=normalized(q)
    return check(name,pin(want['path'],source)==want)

def idcheck(name,q):
    want=normalized(q);p=ordinary(want['path']);i=identity(p)
    identity_only_paths.add(str(p))
    return check(name,stat.S_ISREG(i[2]) and i==want['identity'])

def unique_pairs(items):
    answer={}
    for k,v in items:
        if k in answer: raise ValueError('duplicate JSON key '+k)
        answer[k]=v
    return answer

def reject_constant(value): raise ValueError('nonfinite JSON '+value)

def read(p,sha=None):
    before=pin(p)
    if sha is not None and before['sha256']!=sha: raise ValueError('actual supplied SHA differs '+str(p))
    b=Path(p).read_bytes()
    value=json.loads(b.decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=reject_constant)
    if pin(p)!=before: raise ValueError('META changed during parse')
    return value

def scan_ids(root):
    root=ordinary(root,True);files={};directories={'.':identity(root)};symlinks={}
    for folder,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort()
        for name in dirs+names:
            p=Path(folder)/name;i=identity(p);key=str(p.relative_to(root))
            if stat.S_ISDIR(i[2]): directories[key]=i
            elif stat.S_ISREG(i[2]): files[key]=i
            elif stat.S_ISLNK(i[2]): symlinks[key]=dict(identity=i,literal_target=os.readlink(p))
            else: raise ValueError('nonregular entry '+str(p))
        dirs[:]=[name for name in dirs if not (Path(folder)/name).is_symlink()]
    return dict(root=str(root),files=files,directories=directories,symlinks=symlinks)

def false_fields(name,value):
    for key in FALSE_FIELDS: check(name+'.'+key,value.get(key) is False)

def caps(name,value):
    for key,want in CAPS.items():
        check(name+'.'+key,type(value.get(key)) is int and value[key]==want)

def terminal(name,value,expected_exit,expected_session=None):
    t=value.get('terminal_tool_return',value.get('actual_tool_return',value.get('exec_command_result')))
    if type(t) is not dict: raise ValueError('actual tool terminal object required')
    check(name+'.closed',value.get('closed') is True)
    check(name+'.strict_integer_exit',type(t.get('exit_code')) is int and t['exit_code']==expected_exit)
    check(name+'.no_live_handle','session_id' not in t)
    if expected_session is not None:
        check(name+'.observed_after_terminal',value.get('observed_after_actual_terminal_return') is True)
        check(name+'.no_repoll',value.get('session_repolled_after_close') is False)
        check(name+'.producer',value.get('record_producer')=='root')
        check(name+'.own_session',type(value.get('original_session_id')) is int and value['original_session_id']==expected_session)
        first=value['initial_tool_return'];observations=value['observations']
        check(name+'.initial_live',first.get('session_id')==expected_session and 'exit_code' not in first)
        check(name+'.exact_terminal_last',type(observations) is list and len(observations)>0 and observations[-1]==t)
        check(name+'.no_earlier_terminal',all('exit_code' not in q for q in observations[:-1]))
        check(name+'.no_foreign_session',all(q.get('session_id',expected_session)==expected_session for q in observations))
        check(name+'.outer_integer_exit',type(value.get('exit_code')) is int and value['exit_code']==expected_exit)
    return t

def pure_literals(source):
    tree=ast.parse(source);values={}
    class Substitute(ast.NodeTransformer):
        def visit_Name(self,node):
            return ast.copy_location(ast.Constant(values[node.id]),node) if node.id in values and type(values[node.id]) in (str,int,float,bool,type(None)) else node
    for node in tree.body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            try: values[node.targets[0].id]=ast.literal_eval(Substitute().visit(ast.parse(ast.unparse(node.value),mode='eval')).body)
            except (ValueError,TypeError): pass
    return values

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--contract',required=True);ap.add_argument('--contract-sha256',required=True)
    ap.add_argument('--output',required=True)
    args=ap.parse_args();out=Path(args.output)
    if not str(out).startswith('/private/tmp/') or os.path.lexists(out):
        raise ValueError('fresh private TMP output required')
    c=read(args.contract,args.contract_sha256)
    if c.get('actual_closed_writer_inputs_ready') is not True:
        raise ValueError('future or live writer inputs refused')
    if c.get('BUILD_exit_code')!=1 or type(c.get('BUILD_exit_code')) is not int:
        raise ValueError('this auditor is exactly actual failed EXIT1 scope')
    writer=pin(D/'write_actual_build_postclose_META.py',True)
    host=pin(D/'combined_build_host.py',True)
    check('reviewed_writer_original_bytes',writer['sha256']=='54d30f415a162e80fa91619489beeb4eb776d7787b66a91fd9d55ec2221baf1a')
    check('reviewed_host_original_bytes',host['sha256']=='b47fa026c4b9317741c67c35d4a708294c1a5cb7b5a84e18911c908116f14c24')
    host_values=pure_literals((D/'combined_build_host.py').read_text())
    check('original_five_source_labels',host_values['EXPECTED_LABELS']==LABELS)
    check('original_source_caps','WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30' in (D/'combined_build_host.py').read_text())
    records={}
    for key,q in c['actual_small_META_pins'].items():
        fullcheck('Root_supplied_actual_pin.'+key,q)
        records[key]=read(q['path'],q['sha256'])
    actual=records['BUILD_Root_terminal'];writer_actual=records['postclose_writer_Root_terminal']
    bt=terminal('actual_BUILD',actual,1,7747)
    wt=terminal('actual_postclose_writer',writer_actual,0,c.get('writer_original_session_id'))
    check('writer_source_does_not_supply_business_success',wt['exit_code']==0 and bt['exit_code']==1)
    writer_stdout=json.loads(wt['output'],object_pairs_hook=unique_pairs,parse_constant=reject_constant)
    check('actual_writer_stdout_failed_status',writer_stdout['status']=='ACTUAL_NONZERO_BUILD_NO_RETRY' and type(writer_stdout['actual_tool_exit_code']) is int and writer_stdout['actual_tool_exit_code']==1 and writer_stdout['no_whole_INPUT_native_science_credit'] is True)
    check('actual_writer_stdout_summary_pin',normalized(writer_stdout['summary'])==normalized(c['actual_small_META_pins']['postclose_failed_summary']))
    check('actual_writer_stdout_manifest_pin',normalized(writer_stdout['namespace_manifest'])==normalized(c['actual_small_META_pins']['postclose_failed_namespace_manifest']))
    launch=writer_actual.get('actual_launch_arguments',{})
    check('real_writer_failure_only_argument','--mode failure-only' in json.dumps(launch) or ('--mode' in json.dumps(launch) and 'failure-only' in json.dumps(launch)))
    check('writer_actual_source_argument',writer['sha256'] in json.dumps(launch))
    mf=records['postclose_failed_namespace_manifest'];summary=records['postclose_failed_summary']
    proof=records['formal_failed_terminal'];freeze=records['Source_freeze'];prelaunch=records['final_prelaunch']
    check('failed_manifest_schema',mf['schema']=='ROOT_V25_ACTUAL_COMPLETE_BUILD_POSTCLOSE_FINITE_NAMESPACES_V1')
    check('failed_manifest_mode',mf['mode']=='FAILED_BUILD_SAVED_METADATA_ONLY')
    check('failed_summary_schema',summary['schema']=='ROOT_V25_ACTUAL_COMPLETE_COMBINED_BUILD_POSTCLOSE_SUMMARY_V1')
    check('failed_summary_status',summary['status']=='ACTUAL_NONZERO_BUILD_NO_RETRY')
    check('formal_failed_schema',proof['schema']=='ROOT_V25_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1')
    check('formal_failed_status',proof['status']=='ACTUAL_NONZERO_BUILD_NO_RETRY')
    check('formal_failed_returncode',type(proof['returncode']) is int and proof['returncode']==1)
    check('formal_failed_actual_tool',proof['actual_tool_result']==bt)
    check('formal_failed_actual_launchargs',proof['actual_root_host_launchargs']==actual['actual_launch_arguments'])
    check('formal_observed_actual_terminal',proof['actual_tool_terminal_return_observed'] is True and proof['record_written_after_actual_terminal_return'] is True)
    check('formal_build_success_false',proof['successful_new_runtime_build_observed'] is False)
    for name,v in (('summary',summary),('formal',proof)):
        false_fields(name,v);caps(name,v)
        check(name+'.separate_child_stderr_false',v['separate_child_stderr_captured'] is False)
        check(name+'.child_stderr_empty_not_invented',v['independent_child_stderr_empty_verified'] is False)
        check(name+'.cleanup_false',v['cleanup_performed'] is False)
        check(name+'.host_finalpass_unreached',v['original_host_final_input_revalidation_observed'] is False)
        check(name+'.postclose_not_replace_host_finalpass',v['Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass'] is True)
        check(name+'.physical_finalpass_false',v['full_declared_physical_input_finalpass_claimed'] is False)
    check('metadata_check_errors_truthful',summary['metadata_check_errors']==proof['metadata_check_errors']==['actual Root nonzero terminal 1'])
    check('summary_allfive_success_false',summary['original_five_build_stages_executed'] is False and summary['all_five_build_stages_passed'] is False and summary['completed_inner_stage_labels']==[])
    check('summary_actual_EXIT1_closed',type(summary['actual_terminal_exit_code']) is int and summary['actual_terminal_exit_code']==1 and summary['actual_tool_session_closed'] is True)
    check('summary_Source_unchanged',summary['complete_SOURCE_unchanged'] is True)
    check('summary_original_fixed_unchanged',summary['all_original_fixed_inputs_unchanged'] is True)
    check('summary_API_not_called',summary['metadata_writer_does_not_run_API'] is True and summary['actual_original_guard_or_numeric_API_called'] is False and summary['independent_raw_binary_audit_API_reexecuted'] is False)
    check('mf_no_payload_finalpass',mf['full_declared_physical_input_postclose_pins']==[] and mf['full_declared_physical_input_finalpass_claimed'] is False and mf['full_declared_physical_input_prelaunch_7ID_claimed'] is False)
    check('mf_explicit_scope',mf['all_saved_files_full_EOF_SHA7ID'] is True and mf['no_business_or_numeric_API_called_by_writer'] is True and mf['no_whole_INPUT_native_science_credit'] is True)
    check('mf_original_inputs_source_clean',mf['original_fixed_input_failures']==[] and mf['complete_SOURCE_unchanged'] is True and mf['complete_SOURCE_error'] is None)
    check('mf_E_append_boundary',mf['final_E_root_directory_identity_stability_claimed'] is False and 'before those appends' in mf['E_root_reason'])
    for name,q,want in (
        ('summary_Root_terminal',summary['actual_Root_terminal'],c['actual_small_META_pins']['BUILD_Root_terminal']),
        ('manifest_Root_terminal',mf['actual_Root_terminal'],c['actual_small_META_pins']['BUILD_Root_terminal']),
        ('summary_manifest',summary['namespace_manifest'],c['actual_small_META_pins']['postclose_failed_namespace_manifest']),
        ('summary_formal_terminal',summary['formal_build_terminal'],c['actual_small_META_pins']['formal_failed_terminal']),
        ('manifest_formal_terminal',mf['exact_formal_terminal'],c['actual_small_META_pins']['formal_failed_terminal']),
        ('manifest_source_freeze',mf['complete_SOURCE_freeze'],c['actual_small_META_pins']['Source_freeze']),
        ('manifest_prelaunch',mf['original_prelaunch_check'],c['actual_small_META_pins']['final_prelaunch'])):
        check(name,normalized(q)==normalized(want));fullcheck(name+'.actual',q)
    check('manifest_actual_writer_pin',normalized(mf['actual_metadata_writer_source'])==writer)
    check('formal_actual_writer_pin',normalized(proof['actual_metadata_writer_source'])==writer)
    check('source_freeze_schema',freeze['schema']=='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' and freeze['source_root']==str(D))
    check('source_freeze_no_append',freeze['no_SOURCE_append_after_freeze'] is True and freeze['symlinks']=={})
    check('prelaunch_actual_Sourcefreeze_pin',normalized(prelaunch['source_freeze'])==normalized(c['actual_small_META_pins']['Source_freeze']))
    check('prelaunch_actual_normal_host_pin',normalized(prelaunch['normal_host'])==host)
    check('prelaunch_actual_postclose_writer_pin',normalized(prelaunch['postclose_META_writer'])==writer)
    dview=scan_ids(D)
    check('Source_complete_frozen_sets',set(dview['files'])==set(freeze['complete_files']) and dview['symlinks']=={})
    check('Source_complete_frozen_directories',dview['directories']==freeze['complete_directories'])
    check('actual_source_count_328',type(freeze['actual_complete_SOURCE_file_count']) is int and freeze['actual_complete_SOURCE_file_count']==len(dview['files'])==len(freeze['complete_files'])==328 and summary['full_SOURCE_file_count']==328)
    for key,q in freeze['complete_files'].items():
        fullcheck('frozen_Source_full_EOF.'+key,q,True)
        check('frozen_Source_size.'+key,q['size_bytes']==normalized(q)['identity'][4])
        if Path(key).suffix=='.py':
            ast.parse(Path(q['path']).read_bytes(),filename=q['path']);parsed_sources.append(q['path'])
    fixed=prelaunch['fixed_input_pins'];ordered=mf['ordered_original_fixed_input_expected_pins'];unchanged=mf['unchanged_ordered_original_fixed_input_results']
    check('original_ordered_fixed_count_360',type(fixed) is list and len(fixed)==len(ordered)==len(unchanged)==360 and summary['original_fixed_input_entry_count']==360)
    check('original_ordered_input_duplicates_preserved',ordered==fixed and [q['index'] for q in unchanged]==list(range(360)))
    for index,(expected,actual_q) in enumerate(zip(fixed,unchanged)):
        check('writer_ordered_fixed_pin_coupling.'+str(index),normalized(expected)==normalized(actual_q['pin']))
        idcheck('independent_ordered_fixed_7ID.'+str(index),expected)
        if expected['path'].startswith(str(D)+'/'):
            check('ordered_Source_fullEOF_coupling.'+str(index),fullpins.get(expected['path'])==normalized(expected))
        elif expected['path'] in fullpins:
            check('ordered_selected_META_fullEOF_coupling.'+str(index),fullpins[expected['path']]==normalized(expected))
    check('formal_original_inputs_unchanged',proof['all_original_fixed_inputs_unchanged'] is True and proof['original_fixed_input_final_revalidation_reached_by_this_writer'] is True)
    check('finite_namespace_order',[q['root'] for q in mf['namespaces']]==[str(q) for q in (H,S,O,T,D,E)])
    extra_namespaces={};before_bytes=0
    allowed_E_appends=set(c['allowed_actual_E_post_manifest_appends'])
    for view in mf['namespaces']:
        root=Path(view['root']);current=scan_ids(root)
        check('namespace_present.'+str(root),view['present'] is True)
        check('namespace_no_symlinks.'+str(root),view['symlinks']==current['symlinks']=={})
        expected_set=set(view['files']);actual_set=set(current['files']);extra=actual_set-expected_set
        check('namespace_no_original_file_loss.'+str(root),expected_set.issubset(actual_set))
        check('namespace_exact_directory_set.'+str(root),set(view['directories'])==set(current['directories']))
        for key,want in view['directories'].items():
            check('namespace_directory_identity.'+str(root)+'/'+key,current['directories'][key][:3]==want[:3] if root==E and key=='.' else current['directories'][key]==want)
        check('namespace_only_finite_E_appends.'+str(root),extra==allowed_E_appends if root==E else extra==set())
        for key,q in view['files'].items():
            idcheck('saved_namespace_original_7ID.'+str(root)+'/'+key,q)
            before_bytes+=normalized(q)['identity'][4]
            if q['path'] in fullpins: check('saved_namespace_selected_fullEOF.'+str(root)+'/'+key,fullpins[q['path']]==normalized(q))
        extra_namespaces[str(root)]=sorted(extra)
    for name in allowed_E_appends:
        p=E/name
        if str(p) not in fullpins: pin(p)
    stdout=pin(E/'parent_stdout.log');stderr=pin(E/'parent_stderr.log');merged=pin(H/'run/build.log')
    for name,source,q in (
        ('Root_stdout_copy',stdout,proof['actual_root_host_stdout']),
        ('Root_stderr_copy',stderr,proof['actual_root_host_stderr']),
        ('Root_terminal_copy',pin(c['actual_small_META_pins']['BUILD_Root_terminal']['path']),proof['actual_root_tool_record']),
        ('canonical_child_merged_copy',merged,proof['actual_child_merged_output'])):
        fullcheck(name,q);check(name+'.byte_exact',source['sha256']==q['sha256'] and source['identity'][4]==normalized(q)['identity'][4])
    check('merged_capture_scope_truthful',proof['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and proof['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and proof['original_executor_capture_semantics']=='705 subprocess.Popen stderr=subprocess.STDOUT')
    fullcheck('original_merged_capture_Source',proof['original_executor_merged_capture_source'],True)
    check('original_merged_capture_Source_exact',proof['original_executor_merged_capture_source']['sha256']=='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6')
    stages=records['partial_inner_stages']['stages'];outer=records['outer_watchdog'];failed_host=records['failed_host_result']
    check('actual_partial_stages_coupled',stages==summary['observed_partial_inner_stages'])
    check('actual_all_five_inner_PASS_overall_failed',[q['label'] for q in stages]==LABELS and [q['status'] for q in stages]==['PASS']*5 and summary['observed_PASS_inner_stage_labels']==LABELS and summary['observed_inner_stage_count']==5)
    saved_inner_watches=[]
    for index,q in enumerate(stages):
        check('original_partial_stage_command.'+str(index),q['command']==host_values['EXPECTED_COMMANDS'][index])
        w=read(O/(q['label']+'.watchdog.json'));log=pin(O/(q['label']+'.log'))
        saved_inner_watches.append(w)
        check('partial_actual_log_pin.'+str(index),log['sha256']==q['log_sha256'])
        check('partial_original_watch_command.'+str(index),w['command']==q['command'])
        check('partial_actual_watch_PASS.'+str(index),type(w['returncode']) is int and w['returncode']==0 and w['limit_failure'] is None and w['rss_cap_mib']==512 and 0<=w['sampled_peak_rss_mib']<512 and 0<=w['elapsed_seconds']<w['wall_cap_seconds']<=q['wall_cap_seconds']<=600 and w['own_child_only'] is True and w['liveness_group_cleanup'] is True)
    audit=records['saved_link_identity_audit'];binary=records['saved_binary_identity_META']
    check('saved_audit_link_identity_ONLY',audit['classification']=='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' and audit['binary_status']=='PASS' and audit['declaration_sha256']==host_values['FUTURE_V25_DECLARATION_SHA'])
    check('saved_audit_previous_four_watchdogs',audit['previous_stage_watchdogs']==saved_inner_watches[:4])
    check('saved_audit_science_native_false',all(audit[k] is False for k in ('mathematical_controls_newly_executed','native_transport_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')))
    check('saved_binary_identity_META_PASS_ONLY',binary['status']=='PASS' and all(binary[k] is False for k in ('whole_instruction_equivalence_claimed','actual_full_FLU_entry_executed','combined_runtime_native_RSS_proved','AAA_accuracy_qualified','ABA_admitted')))
    check('audit_inner_observed_seconds',stages[-1]['elapsed_seconds']==48.33631362498272)
    observed={key:outer[key] for key in ('returncode','elapsed_seconds','sampled_peak_rss_mib','limit_failure','own_child_only','liveness_group_cleanup','rss_cap_mib','wall_cap_seconds')}
    check('outer_saved_summary_coupled',observed==summary['observed_outer_watchdog_fields'])
    check('actual_outer_RSS_failure',type(outer['returncode']) is int and outer['returncode']==-15 and outer['rss_cap_mib']==512 and outer['sampled_peak_rss_mib']==c['actual_sampled_peak_rss_mib']==512.578125 and outer['sampled_peak_rss_mib']>outer['rss_cap_mib'] and outer['limit_failure'] is not None)
    check('actual_outer_elapsed',type(outer['elapsed_seconds']) in (int,float) and math.isfinite(outer['elapsed_seconds']) and outer['elapsed_seconds']==c['actual_outer_elapsed_seconds'] and 0<outer['elapsed_seconds']<outer['wall_cap_seconds']<=1800)
    check('actual_outer_own_child_cleanup',outer['own_child_only'] is True and outer['liveness_group_cleanup'] is True)
    check('actual_failed_host_status',failed_host['status']=='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY')
    check('actual_failed_host_science_false',all(failed_host.get(k) is False for k in ('native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')))
    check('outer_actual_original_command',outer['command']==[host_values['EXPECTED_COMMANDS'][-1][0],host_values['EXPECTED_COMMANDS'][-1][1],'run-build','--sha256',host_values['FUTURE_V25_DECLARATION_SHA'],'--prep-sha256',host_values['FUTURE_V25_PREP_SHA']])
    for name in ('terminal_return.json',): check('no_false_success_terminal.'+name,not os.path.lexists(T/name))
    for name in ('seal.json','driver_result.json'):
        check('no_false_complete_success_metadata.'+name,not os.path.lexists(O/name))
    check('no_false_success_host_result',not os.path.lexists(H/'result.json'))
    check('no_false_success_postclose_outputs',not os.path.lexists(E/'Root_actual_complete_build_namespace_manifest.json') and not os.path.lexists(E/'Root_actual_complete_combined_build_summary.json'))
    check('joint_archive_writer_saved_original_cap',type(summary['joint_archive_bytes_after_summary']) is int and summary['joint_archive_bytes_after_summary']<2*2**30 and type(summary['joint_archive_bytes_before_summary']) is int and summary['joint_archive_bytes_after_summary']-summary['joint_archive_bytes_before_summary']==pin(c['actual_small_META_pins']['postclose_failed_summary']['path'])['identity'][4])
    original_sizes=sum(normalized(q)['identity'][4] for view in mf['namespaces'] for q in view['files'].values())
    factory=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_monitor_access.py')
    expected_before=original_sizes+pin(c['actual_small_META_pins']['postclose_failed_namespace_manifest']['path'])['identity'][4]+factory.stat().st_size+writer['identity'][4]
    check('joint_archive_preappend_byte_accounting',expected_before==summary['joint_archive_bytes_before_summary'])
    for q in list(fullpins.values()): check('final_selected_Source_META_7ID_stable.'+q['path'],identity(q['path'])==q['identity'])
    for q in fixed: check('final_ordered_physical_7ID_stable.'+q['path'],identity(q['path'])==normalized(q)['identity'])
    report=dict(schema='INDEPENDENT_V25_ACTUAL_FAILED_BUILD_SAVED_SMALL_META_SOURCE_REVIEW_V1',
        status='PASS_ACTUAL_FAILED_BUILD_SAVED_SMALL_META_SOURCE_ONLY' if not blockers else 'BLOCKED_ACTUAL_FAILED_BUILD_SAVED_SMALL_META_SOURCE_REVIEW',
        all_checks_typed_true=not blockers,typed_true_check_count=sum(q['typed_true'] for q in checks),checks=checks,blockers=blockers,
        actual_BUILD_Root_terminal_pin=normalized(c['actual_small_META_pins']['BUILD_Root_terminal']),
        actual_postclose_writer_Root_terminal_pin=normalized(c['actual_small_META_pins']['postclose_writer_Root_terminal']),
        actual_saved_failed_summary_pin=normalized(c['actual_small_META_pins']['postclose_failed_summary']),
        actual_saved_failed_namespace_manifest_pin=normalized(c['actual_small_META_pins']['postclose_failed_namespace_manifest']),
        actual_failed_formal_terminal_pin=normalized(c['actual_small_META_pins']['formal_failed_terminal']),
        actual_reviewed_writer_Source_pin=writer,actual_reviewed_host_Source_pin=host,
        actual_BUILD_exit_code=1,actual_writer_exit_code=0,actual_outer_child_returncode=outer['returncode'],
        actual_outer_elapsed_seconds=outer['elapsed_seconds'],actual_sampled_peak_rss_mib=outer['sampled_peak_rss_mib'],rss_cap_mib=512,
        actual_all_five_inner_PASS_stage_labels=LABELS,all_five_inner_stages_observed_PASS=True,whole_BUILD_qualified=False,
        actual_Source_count=328,actual_ordered_fixed_input_entry_count=360,actual_Source_AST_parse_count=len(parsed_sources),
        independent_full_EOF_Source_and_selected_small_META_pins=list(fullpins.values()),
        independent_nonselected_physical_entries_lstat_only=sorted(identity_only_paths-set(fullpins)),
        no_graph_trace_material_database_archive_or_binary_payload_decoded=True,
        no_large_physical_payload_full_EOF_reread=True,independent_whole_physical_input_full_EOF_revalidation=False,
        Root_writer_declared_full_EOF_records_are_saved_source_coupled_attestations=True,
        independent_selected_Source_and_small_META_full_EOF_SHA_7ID_verified=True,
        E_manifest_is_explicit_before_actual_appends=True,actual_observed_namespace_post_manifest_appends=extra_namespaces,
        no_project_or_frozen_D_E_mutation=True,no_candidate_guard_API_compile_or_business_execution=True,
        cleanup_performed=False,no_whole_INPUT_native_science_credit=True,
        **{key:False for key in FALSE_FIELDS})
    out.mkdir();(out/'REVIEW.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    (out/'REVIEWER_SOURCE.byte_exact.py').write_bytes(Path(__file__).read_bytes())
    (out/'ACTUAL_CLOSED_ROOT_INPUT_CONTRACT.byte_exact.json').write_bytes(Path(args.contract).read_bytes())
    print(json.dumps(dict(status=report['status'],all_checks_typed_true=report['all_checks_typed_true'],typed_true_check_count=report['typed_true_check_count'],blockers=blockers,report=pin(out/'REVIEW.json'),no_whole_INPUT_native_science_credit=True),allow_nan=False))

if __name__=='__main__': main()
