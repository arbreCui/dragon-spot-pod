"""Finite saved V21 PREP META review; graph/trace/ART payloads are streamed SHA only."""
import hashlib
import json
import math
import os
import re
import stat
from pathlib import Path, PurePosixPath

B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
E=B/'actual_complete_combined_prepare_v21_receipts'
D=B/'actual_complete_combined_prepare_v21_sources'
A=Path('/Users/wen/spot/validation/artifacts')
H=A/'axial-material-complete-combined-prepare-host-v21-20261010'
S=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010'
O=A/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'
T=A/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010'
OUT=Path('/private/tmp/axmat_v21_actual_complete_PREP_independent_saved_META_review_20261010_p4nw2')
FACTORY=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')
SUMMARY_SHA='21ee531ce1a2032cb2d6fb86fe86603ae1a9bec3300ff982d033248ac9700344'
NAMESPACE_SHA='f0759d38c8cc6c5340968ea6905b9537eeb5f80bafc71a452d76bfb12b58852f'


def identity(path):
    st=path.lstat()
    return [st.st_dev,st.st_ino,st.st_mode,st.st_nlink,st.st_size,st.st_mtime_ns,st.st_ctime_ns]


def pin(path):
    path=Path(path)
    before=identity(path)
    if not stat.S_ISREG(before[2]) or before[3]!=1:
        raise ValueError('Saved evidence must be ordinary single-link files')
    descriptor=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
    try:
        st=os.fstat(descriptor)
        fields=lambda s:[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        if fields(st)!=before:raise ValueError('Saved evidence identity changed before open')
        digest=hashlib.sha256();size=0
        while True:
            chunk=os.read(descriptor,1024*1024)
            if not chunk:break
            size+=len(chunk);digest.update(chunk)
        if fields(os.fstat(descriptor))!=before:raise ValueError('Saved evidence changed during full EOF read')
    finally:os.close(descriptor)
    if identity(path)!=before or size!=before[4]:raise ValueError('Saved evidence full EOF identity changed')
    return dict(path=str(path),sha256=digest.hexdigest(),identity=before)


def strict_metadata(path):
    path=Path(path)
    if path.is_relative_to(O) or path.is_relative_to(S):
        raise ValueError('No prepared ART source payload or graph/declaration/trace decoding allowed')
    before=pin(path)
    if before['identity'][4]>8*2**20:raise ValueError('Finite explicitly saved META must be bounded')
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('Duplicate saved META key')
            result[key]=value
        return result
    def reject(value):raise ValueError('Nonfinite saved META')
    value=json.loads(path.read_bytes(),object_pairs_hook=pairs,parse_constant=reject)
    if pin(path)!=before:raise ValueError('Saved META complete EOF pin changed during decoding')
    return value,before


def same_pin(actual, expected):
    if set(expected) not in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'}):return False
    if not isinstance(expected['identity'],list) or len(expected['identity'])!=7 or any(type(x) is not int for x in expected['identity']):return False
    if re.fullmatch('[0-9a-f]{64}',expected['sha256']) is None:return False
    if 'size_bytes' in expected and (type(expected['size_bytes']) is not int or expected['size_bytes']!=actual['identity'][4]):return False
    return actual=={k:expected[k] for k in ('path','sha256','identity')}


def namespace(root):
    if root not in (H,S,O,T,D,E):raise ValueError('Only exact new V21 frozen evidence roots may be enumerated')
    directories={};files={};root_identity=identity(root)
    if not stat.S_ISDIR(root_identity[2]):raise ValueError('Exact frozen evidence directory required')
    for folder,dirs,names in os.walk(root,followlinks=False):
        folder=Path(folder)
        for name in dirs:
            path=folder/name;ident=identity(path)
            if not stat.S_ISDIR(ident[2]):raise ValueError('No saved evidence symlink/non-directory permitted')
            directories[str(path.relative_to(root))]=ident
        for name in names:
            path=folder/name;files[str(path.relative_to(root))]=pin(path)
    if identity(root)!=root_identity:raise ValueError('Exact saved namespace root changed during enumeration')
    return dict(root=str(root),root_identity=root_identity,files=files,directories=directories,symlinks={})


def main():
    checks=[];explicit_before={}
    def check(name,value):
        if value is not True:raise ValueError('Saved META check: '+name)
        checks.append(dict(name=name,value=True))
    def actual(path,expected=None):
        path=Path(path);current=pin(path)
        if expected is not None:check('full EOF exact7ID saved pin '+str(path),same_pin(current,expected))
        if str(path) in explicit_before:check('repeated explicit evidence full EOF pin remains exact '+str(path),explicit_before[str(path)]==current)
        explicit_before[str(path)]=current
        return current
    def meta(path,expected=None):
        value,current=strict_metadata(path)
        if expected is not None:check('full strict saved META reference '+str(path),same_pin(current,expected))
        if str(path) in explicit_before:check('strict saved META reread pin exact '+str(path),explicit_before[str(path)]==current)
        explicit_before[str(path)]=current
        return value
    summary=meta(E/'Root_actual_complete_combined_prepare_summary.json')
    check('fixed actual successful summary SHA',explicit_before[str(E/'Root_actual_complete_combined_prepare_summary.json')]['sha256']==SUMMARY_SHA)
    check('complete PREP-only summary schema/status',summary['schema']=='ROOT_V21_ACTUAL_COMPLETE_COMBINED_PREPARE_SUMMARY_V1' and summary['status']=='ACTUAL_COMPLETE_PREPARE_EXIT0_CLOSED_ONLY_NOT_COMPLETE_BUILD')
    freeze=meta(E/'Root_actual_complete_prepare_namespace_manifest.json',summary['namespace_manifest'])
    check('fixed actual complete five-namespace manifest SHA',explicit_before[str(E/'Root_actual_complete_prepare_namespace_manifest.json')]['sha256']==NAMESPACE_SHA)
    check('complete five-namespace manifest schema and honest scope',freeze['schema']=='ROOT_V21_ACTUAL_COMPLETE_PREPARE_ALL_NAMESPACES_V1' and freeze['no_build_or_native_credit'] is True)
    roots={record['root']:record for record in freeze['namespaces']}
    check('complete manifest all five roots unique and exact',len(roots)==len(freeze['namespaces'])==5 and set(roots)=={str(p) for p in (H,S,O,T,D)})
    namespaces_before={str(root):namespace(root) for root in (H,S,O,T,D,E)}
    expected_counts={str(H):5,str(S):11,str(O):4,str(T):6,str(D):58}
    for root in (H,S,O,T,D):
        old=roots[str(root)];live=namespaces_before[str(root)]
        check('complete saved namespace symlink boundary '+str(root),old['symlinks']==live['symlinks']=={})
        check('complete saved namespace full file member count '+str(root),len(old['files'])==len(live['files'])==expected_counts[str(root)])
        check('complete saved namespace full directories with exact7IDs '+str(root),{q['path']:q['identity'] for q in old['directories']}==live['directories'] and len(old['directories'])==len(live['directories']))
        check('complete saved namespace full EOF SHA7ID files '+str(root),old['files']==live['files'])
        for relative,current in live['files'].items():
            explicit_before[current['path']]=current
            check('whole retained saved file '+str(root/relative),same_pin(current,old['files'][relative]))
    for current in namespaces_before[str(E)]['files'].values():explicit_before[current['path']]=current
    terminal=meta(E/'Root_actual_prepare_tool_terminal_return.json',summary['actual_root_terminal'])
    check('Root full terminal alias exact',summary['Root_actual_terminal']==summary['actual_root_terminal'])
    check('Root terminal actual schema producer and observed timing',terminal['schema']=='ROOT_V21_ACTUAL_COMPLETE_PREP_TOOL_TERMINAL_RETURN_V1' and terminal['record_producer']=='root' and terminal['observed_after_actual_terminal_return'] is True)
    tr=terminal['terminal_tool_return'];initial=terminal['initial_tool_return']
    check('true original Root session16256/launch78a34b',initial['chunk_id']=='78a34b' and type(initial['session_id']) is int and initial['session_id']==16256 and 'exit_code' not in initial and terminal['original_session_id']==16256)
    check('true Root actual terminal e0647a typed integer0 CLOSED no live session',tr['chunk_id']=='e0647a' and type(tr['exit_code']) is int and tr['exit_code']==0 and 'session_id' not in tr and type(terminal['exit_code']) is int and terminal['exit_code']==0 and terminal['closed'] is True)
    check('Root terminal no closed session repoll',terminal['session_repolled_after_close'] is False)
    check('all actual observations end at same final typed terminal',terminal['observations'][-1]==tr and all(q.get('session_id')==16256 and 'exit_code' not in q for q in terminal['observations'][:-1]))
    check('Root actual external executor output honestly redirected',tr['output']=='' and initial['output']=='')
    for key in ['new_five_stage_build_executed','whole_combined_INPUT_executed','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted']:
        check('Root actual PREP only business/science false '+key,terminal[key] is False)
    initial_receipt=meta(E/'Root_actual_initial_tool_return.json')
    check('actual initial Root receipt enumerated and preserved',initial_receipt is not None)
    writer=meta(E/'Root_actual_prepare_metadata_writer_tool_return.json')
    wtr=writer['terminal_tool_return']
    check('true saved Root metadata writer22276d typed0 closed',writer['schema']=='ROOT_V21_ACTUAL_PREP_POSTCLOSE_METADATA_WRITER_TOOL_RETURN_V1' and wtr['chunk_id']=='22276d' and type(wtr['exit_code']) is int and wtr['exit_code']==0 and 'session_id' not in wtr and writer['closed'] is True and type(writer['exit_code']) is int and writer['exit_code']==0 and writer['initial_tool_return']==wtr and writer['observations']==[])
    check('Root writer created metadata only not business/numeric',writer['business_API_or_numeric_executed_by_writer'] is False)
    writer_stdout=json.loads(wtr['output'])
    check('actual writer stdout exact status and whole measured fields',writer_stdout=={k:summary[k] for k in ('status','whole_seconds','child_seconds','sampled_peak_rss_mib','joint_archive_bytes','all_source_files_verified_count')})
    prelaunch=meta(E/'Root_final_prelaunch_source_and_reserve_check.json')
    prefreeze=meta(E/'Root_prelaunch_complete_source_freeze.json')
    check('Source freeze exact schema and no append',prefreeze['schema']=='ROOT_V21_COMPLETE_PREP_SOURCE_NAMESPACE_PRELAUNCH_FREEZE_V1' and prefreeze['source_root']==str(D) and prefreeze['no_SOURCE_append_after_freeze'] is True and prefreeze['all_file_SHA7ID_recorded'] is True and prefreeze['actual_PREP_not_started'] is True)
    check('Source58 full prelaunch/current directory root7ID exact',prefreeze['source_root_identity']==namespaces_before[str(D)]['root_identity'])
    check('Source58 prelaunch full all files and7ID unchanged',len(prefreeze['complete_files'])==58 and set(prefreeze['complete_files'])==set(roots[str(D)]['files']) and all(same_pin(roots[str(D)]['files'][name],record) for name,record in prefreeze['complete_files'].items()))
    check('Source prelaunch full directories no omissions',sorted(namespaces_before[str(D)]['directories'])==prefreeze['complete_directories'] and prefreeze['symlinks']=={})
    check('final prelaunch exact58 Source full fresh pins',prelaunch['schema']=='ROOT_V21_COMPLETE_PREP_FINAL_PRELAUNCH_META_V1' and prelaunch['complete_SOURCE58_EOF_SHA7ID_fresh_same'] is True and prelaunch['complete_SOURCE_files']==prefreeze['complete_files'])
    check('all final prelaunch9 subdirectory7IDs unchanged',prelaunch['complete_SOURCE_directory_7IDs']==namespaces_before[str(D)]['directories'])
    check('prelaunch Source readonly META only no append',prelaunch['guard_API_business_numeric_executed'] is False and prelaunch['no_SOURCE_append_after_freeze'] is True)
    check('all four original fresh one-use namespaces proven absent before launch',set(prelaunch['four_business_namespaces_absent'])=={p.name for p in (H,S,O,T)} and len(prelaunch['four_business_namespaces_absent'])==4)
    check('prelaunch original free8 and joint2GiB reserve',prelaunch['free_floor_bytes']==8*2**30 and prelaunch['free_bytes']>=8*2**30 and prelaunch['joint_archive_cap_bytes']==2*2**30 and 0<prelaunch['joint_existing_Source_receipts_factory_bytes']<2*2**30)
    check('all six future business pins remain None in actual prelaunch',len(prelaunch['six_future_business_pins'])==6 and all(value is None for value in prelaunch['six_future_business_pins'].values()))
    canonical=actual(FACTORY,freeze['canonical_factory'])
    check('fixed actual installed canonical runtime023abc and all prelaunch aliases exact',canonical['sha256']=='023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5' and same_pin(canonical,prefreeze['canonical_factory']) and prefreeze['canonical_factory']==prelaunch['canonical_factory'])
    actual(Path(prelaunch['actual_joint_helper_Q']['path']),prelaunch['actual_joint_helper_Q'])
    check('fixed actual joint Q29ac all metadata fields retained',prelaunch['actual_joint_helper_Q']['sha256']=='29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2')
    install=meta(E/'Root_actual_source_install_tool_return.json')
    check('actual complete SOURCE installation strict0 closed and no business',install['schema']=='ROOT_V21_ACTUAL_COMPLETE_PREP_SOURCE_INSTALL_TOOL_RETURN_V1' and type(install['actual_tool_return']['exit_code']) is int and install['actual_tool_return']['exit_code']==0 and install['closed'] is True and install['business_executed'] is False and 'session_id' not in install['actual_tool_return'])
    install_stdout=json.loads(install['actual_tool_return']['output'])
    check('actual SOURCE installation exact58 full Source/canonical pins',install_stdout['complete_SOURCE_files']==58 and same_pin(canonical,install_stdout['canonical_factory']) and same_pin(explicit_before[str(E/'Root_prelaunch_complete_source_freeze.json')],install_stdout['SOURCE_freeze']))
    prelaunch_return=meta(E/'Root_actual_final_prelaunch_tool_return.json')
    ptr=prelaunch_return['actual_tool_return']
    check('actual final prelaunch strict0 closed META only',type(ptr['exit_code']) is int and ptr['exit_code']==0 and 'session_id' not in ptr and prelaunch_return['closed'] is True and prelaunch_return['business_executed'] is False)
    check('actual final prelaunch saved record full exactpin',same_pin(explicit_before[str(E/'Root_final_prelaunch_source_and_reserve_check.json')],json.loads(ptr['output'])['record']))
    host=meta(H/'result.json',summary['actual_host_result'])
    watch=meta(H/'run/prepare.watchdog.json',host['actual_watchdog'])
    stages=meta(H/'COMBINED_PREPARATION/stages.json')
    command=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12',str(FACTORY),'prepare-build']
    check('complete genuine normal PREP host schema/status',host['schema']=='AXMAT_V21_GENUINE_COMPLETE_COMBINED_PREPARE_HOST_V1' and host['status']=='ACTUAL_COMPLETE_COMBINED_PREPARE_EXTERNAL_ROOT_REQUIRED')
    check('same one genuine actual command everywhere',host['actual_canonical_command']==watch['command']==command)
    check('host watchdog full record matches standalone metadata',host['watchdog']==watch)
    check('one genuine PREP stage PASS and all original saved stage fields',len(host['stage_records'])==len(stages['stages'])==1 and host['stage_records']==stages['stages'] and host['stage_records'][0]['status']=='PASS' and host['stage_records'][0]['label']=='run/prepare' and host['stage_records'][0]['command']==command)
    check('actual own child watchdog8984 typed return0 and completecleanup',type(watch['pid']) is int and watch['pid']==8984 and type(watch['returncode']) is int and watch['returncode']==0 and watch['limit_failure'] is None and watch['own_child_only'] is True and watch['liveness_group_cleanup'] is True)
    stage=host['stage_records'][0]
    check('original watchdog600stage512RSS elapsed measured bound',watch['rss_cap_mib']==512 and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 and 0<=watch['sampled_peak_rss_mib']<512)
    check('saved whole193/child191/peak467 exact Root summary aliases',host['whole_seconds']==summary['whole_seconds']==193.33837633300573 and watch['elapsed_seconds']==summary['child_seconds']==191.8211530839326 and watch['sampled_peak_rss_mib']==summary['sampled_peak_rss_mib']==467.859375 and watch['elapsed_seconds']<=stage['elapsed_seconds']<=host['whole_seconds']<1800)
    cap_fields=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_cap_mib','archive_cap_bytes','threads','children_at_once','retries')
    check('all original host caps and typed int1/1/0 exact',tuple(host[k] for k in cap_fields)==(1800,600,512,2*2**30,1,1,0) and all(type(host[k]) is int for k in cap_fields))
    summary_cap_fields=('whole_wall_cap_seconds','stage_wall_cap_seconds','rss_mib','joint_archive_cap_bytes','history_cap_bytes','free_floor_bytes','threads','children','retries')
    check('all original summary complete caps exact and typed',tuple(summary[k] for k in summary_cap_fields)==(1800,600,512,2*2**30,96*2**30,8*2**30,1,1,0) and all(type(summary[k]) is int for k in summary_cap_fields))
    check('original summary caps preserved flag',summary['original_caps_preserved'] is True)
    for key in ['profile_used','supervisor_class_or_MRO_modified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted']:
        check('genuine host unchanged/science false '+key,host[key] is False)
    resource_records=[host['resources_before'],host['resources_after'],stage['resource_before'],stage['resource_after']]
    for index,resource in enumerate(resource_records):
        check('saved actual history96/free8 bounds '+str(index),resource['artifact_budget_bytes']==96*2**30 and resource['min_free_bytes']==8*2**30 and type(resource['artifact_bytes']) is int and 0<=resource['artifact_bytes']<=96*2**30 and resource['disk_free_bytes']>=8*2**30)
        check('saved original dynamic family scope '+str(index),resource['resource_scope_policy']=='AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1' and resource['resource_scope_contract']==host['resources_before']['resource_scope_contract'])
        root_names=resource['resource_roots'];declared=resource['declared_resource_roots']
        check('saved complete history roots lexical exactART scope no live rescan '+str(index),len(root_names)==len(set(root_names)) and set(declared).issubset(root_names) and all(PurePosixPath(p).is_absolute() and PurePosixPath(p).is_relative_to(PurePosixPath(str(A))) and PurePosixPath(p)!=PurePosixPath(str(A)) and '..' not in PurePosixPath(p).parts for p in root_names))
        check('all current PREP ART roots retained in original saved scope '+str(index),{str(p) for p in (H,S,O)}.issubset(root_names))
    check('original complete twoGiB initial reserve actual saved resources',host['resources_before']['artifact_bytes']+2*2**30<96*2**30 and host['resources_before']['disk_free_bytes']-2*2**30>=8*2**30)
    inputs=host['input_sources']+[host['original_helper'],host['resource_factory']]
    check('all67 original fixed inputs full enumerable and retained',len(inputs)==summary['all_original_pinned_inputs_unchanged_count']==67 and inputs==freeze['all_original_inputs_fresh_full_EOF_SHA7ID_unchanged'])
    check('all65 host SOURCE input entries preserved',len(host['input_sources'])==65)
    for entry in inputs:actual(Path(entry['path']),entry)
    source_inputs={entry['path']:entry for entry in host['input_sources']}
    check('all58 frozen D SOURCE files in host original input range',all(record['path'] in source_inputs and record==source_inputs[record['path']] for record in roots[str(D)]['files'].values()))
    check('actual original619 genuine supervisor SOURCE unchanged',host['original_helper']['sha256']=='619ed1e3115e0f9f25fd20cc259d384891f2fff52d913acebd5d9ca8f39d5743')
    check('actual originalebbb dynamic resource SOURCE unchanged',host['resource_factory']['sha256']=='ebbb0235ca5eaf7f7d896c225925f6705d2ba32f70295d957206548571575022')
    host_source=D/'sealed_READY_runtime_and_PREP_binding/BOUND_READY_SOURCE/combined_prepare_host.py'
    host_source_pin=actual(host_source,source_inputs[str(host_source)])
    check('actual exact SOURCE approved normal host776bf',host_source_pin['sha256']=='776bf8300f5c5a55c9e9f4929760b0db10b5f6d2392ea0971483364d19365405')
    host_source_text=host_source.read_text()
    for anchor in ('helper.guard_admission(full)','full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)','runner.execute(HOST/\'run\',\'prepare\',command,STAGE_CAP)','supervisor_class_or_MRO_modified=False','resources=resource.DynamicHistoryResources'):
        check('whole original genuine normal SOURCE guard/call '+anchor,anchor in host_source_text)
    check('actual one-use normal host SOURCE launch zero extra argv',str(host_source)+' > '+str(E/'parent_stdout.log')+' 2> '+str(E/'parent_stderr.log') in terminal['actual_launch_arguments']['cmd'])
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
        check('actual original single-thread launch '+key,key+'=1' in terminal['actual_launch_arguments']['cmd'])
    check('actual original nonoptimized no profile launch','env -u PYTHONOPTIMIZE' in terminal['actual_launch_arguments']['cmd'] and 'PYTHONDONTWRITEBYTECODE=1' in terminal['actual_launch_arguments']['cmd'])
    formal=meta(T/'declaration_terminal_return.json',summary['formal_PREP_terminal'])
    check('new actual formal PREP schema and true terminal observations',formal['schema']=='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21_ACTUAL_EXTERNAL_PREP_RETURN_V1' and formal['record_producer']=='root' and formal['successful_declaration_input_observed'] is True and formal['actual_tool_terminal_return_observed'] is True and formal['record_written_after_actual_terminal_return'] is True and type(formal['returncode']) is int and formal['returncode']==0)
    check('formal actual Root terminal and command copied exact',formal['actual_tool_result']==tr and formal['command']==command and formal['actual_root_host_launchargs']==terminal['actual_launch_arguments'])
    check('formal canonical SOURCE and declaration bindings exact',formal['source']=={k:canonical[k] for k in ('path','sha256')} and formal['declaration']=={k:summary['actual_declaration'][k] for k in ('path','sha256')})
    check('formal full graph bound exact without graph payload decoding',formal['input_graph']['path']==summary['actual_complete_input_graph']['path'] and formal['input_graph']['sha256']==summary['actual_complete_input_graph']['sha256'] and formal['input_graph']['scope']=='COMPLETE_HISTORICAL_INPUT_ONLY')
    check('graph aliases exact complete pin',summary['actual_input_graph']==summary['actual_complete_input_graph'])
    for key in ['actual_declaration','actual_complete_input_graph','actual_complete_creation_trace']:
        actual(Path(summary[key]['path']),summary[key])
    actual(Path(host['actual_declaration']['path']),host['actual_declaration'])
    actual(Path(host['actual_source_admission']['path']),host['actual_source_admission'])
    check('new prepared SOURCE exact all11 files retained',summary['all_source_files_verified_count']==11 and host['actual_source_admission']==roots[str(S)]['files']['source_admission.json'])
    source_inventory=meta(T/'Root_actual_SOURCE_inventory.json')
    check('complete original SOURCE inventory all11files all dirs symlinks exact',source_inventory==dict(files={name:record['sha256'] for name,record in roots[str(S)]['files'].items()},directories=sorted(namespaces_before[str(S)]['directories']),symlinks={}))
    actual(Path(formal['source_inventory']['path']))
    check('formal full Source inventory binding exact',formal['source_inventory']=={k:explicit_before[str(T/'Root_actual_SOURCE_inventory.json')][k] for k in ('path','sha256')})
    for source,name in [(H/'run/prepare.log','actual_child_merged_stdout_stderr.json'),(E/'parent_stderr.log','actual_external_host_stderr.txt'),(E/'parent_stdout.log','actual_external_host_stdout.json'),(E/'Root_actual_prepare_tool_terminal_return.json','actual_external_Root_tool_terminal.json')]:
        a=actual(source);b=actual(T/name)
        check('full actual original merged/external stream bytehash and size exact '+name,a['sha256']==b['sha256'] and a['identity'][4]==b['identity'][4])
    child_stream=meta(H/'run/prepare.log',host['actual_prepare_stdout'])
    check('actual child full merged stream entire declaration metadata exact',child_stream==dict(declaration=summary['actual_declaration']['path'],declaration_sha256=summary['actual_declaration']['sha256']) and stage['log_sha256']==explicit_before[str(H/'run/prepare.log')]['sha256'])
    external_stream=meta(E/'parent_stdout.log')
    check('actual separate external host entire stdout contract exact',external_stream==dict(status=host['status'],actual_host_result=summary['actual_host_result'],actual_prepare_stdout=host['actual_prepare_stdout'],actual_external_Root_terminal_required=True))
    check('actual external host stderr zero full bytes only',explicit_before[str(E/'parent_stderr.log')]['identity'][4]==0 and roots[str(T)]['files']['actual_external_host_stderr.txt']['identity'][4]==0)
    check('formal honest merged-child and external-host stderr scopes',formal['full_stdout_scope']=='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR' and formal['full_stderr_scope']=='ACTUAL_EXTERNAL_ROOT_HOST_STDERR' and formal['separate_child_stderr_captured'] is False and formal['independent_child_stderr_empty_verified'] is False)
    for key in ['full_stdout','full_stderr','actual_child_watchdog','actual_root_host_terminal_tool_return','actual_root_host_stdout','original_executor_merged_capture_source']:
        expected=formal[key];current=actual(Path(expected['path']))
        check('formal complete actual stream/source pin '+key,current['sha256']==expected['sha256'] and ('identity' not in expected or current['identity']==expected['identity']))
    check('unchanged original705 merged capture SOURCE exact',formal['original_executor_merged_capture_source']['sha256']=='70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6' and 'stderr=subprocess.STDOUT' in formal['original_executor_capture_semantics'])
    check('whole seven-key INPUT historical body honest retained',formal['historical_whole_component_body']['whole_seven_key_body_retained'] is True and formal['historical_whole_component_body']['original_component_API_execution_claimed'] is False and formal['historical_whole_component_body']['historical_FAILED_RUN_promoted'] is False)
    check('actual trim metadata API honestly retained without old RSS/new native credit',formal['trim_component_API_executed_in_this_PREP'] is True and formal['actual_last_cprime_trim_component_INPUT']['actual_component_API_called_in_this_PREP'] is True and formal['actual_last_cprime_trim_component_INPUT']['original_historical_seven_key_body_unchanged'] is True and formal['actual_last_cprime_trim_component_INPUT']['old_capture_RSS_transferred'] is False and formal['actual_last_cprime_trim_component_INPUT']['trim_native_RSS_proof_obtained'] is False)
    check('actual trim INPUT metadata file whole SHA saved unchanged',formal['actual_last_cprime_trim_component_INPUT']['path']==str(S/'trim_component_admission_INPUT.json') and formal['actual_last_cprime_trim_component_INPUT']['sha256']==roots[str(S)]['files']['trim_component_admission_INPUT.json']['sha256'])
    for key in ['successful_new_runtime_build_observed','original_component_APIs_executed_now','native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted']:
        check('formal complete PREP-only business/science false '+key,formal[key] is False)
    for key in ['new_five_stage_build_executed','whole_combined_INPUT_admitted','new_native_transport_executed','AAA_accuracy_qualified','ABA_admitted','goal_complete','original_five_build_stages_executed','native_RSS_qualified','cleanup_performed']:
        check('summary actual PREP only all future false '+key,summary[key] is False)
    current_total=sum(record['identity'][4] for ns in namespaces_before.values() for record in ns['files'].values())+canonical['identity'][4]
    exact_added_post_total=explicit_before[str(E/'Root_actual_complete_combined_prepare_summary.json')]['identity'][4]+explicit_before[str(E/'Root_actual_prepare_metadata_writer_tool_return.json')]['identity'][4]
    check('actual writer joint140790142 complete archive count stage correct',summary['joint_archive_bytes']==140790142 and current_total==summary['joint_archive_bytes']+exact_added_post_total and current_total<2*2**30)
    check('PREP-only complete O four files and five dirs no actual build',set(roots[str(O)]['files'])=={'declaration.json','input_graph.json','input_creation_python_open_trace.json','runtime/run_bounded_dragon.py'} and all(name not in roots[str(O)]['files'] for name in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','runtime/Dragon')))
    namespaces_after={str(root):namespace(root) for root in (H,S,O,T,D,E)}
    check('all six bounded saved evidence namespaces complete membership/fullEOF SHA7ID/dirs/root7IDs unchanged beforeafter',namespaces_after==namespaces_before)
    for path,before in explicit_before.items():check('all explicit saved evidence full EOF SHA7ID beforeafter '+path,pin(Path(path))==before)
    report={
      'schema':'AXMAT_V21_ACTUAL_COMPLETE_PREP_FINITE_SAVED_META_INDEPENDENT_REVIEW_V1',
      'status':'ACTUAL_COMPLETE_PREP_EXIT0_CLOSED_SAVED_META_PASS_NOT_BUILD_OR_WHOLE_INPUT',
      'checks':checks,'all_checks_typed_true':True,'blockers':[],
      'actual_Root_terminal_chunk_id':'e0647a','actual_Root_terminal_exit_code':0,'actual_Root_terminal_closed':True,
      'actual_Root_metadata_writer_chunk_id':'22276d','actual_Root_metadata_writer_exit_code':0,
      'actual_PREP_summary_pin':explicit_before[str(E/'Root_actual_complete_combined_prepare_summary.json')],
      'actual_complete_namespace_manifest_pin':explicit_before[str(E/'Root_actual_complete_prepare_namespace_manifest.json')],
      'all_full_namespace_saved_evidence_before_after':namespaces_before,
      'all_explicit_saved_evidence_pins_before_after':explicit_before,
      'complete_Source58_prelaunch_SHA7ID_and_directory7IDs_unchanged':True,
      'all67_original_host_fixed_input_entries_full_EOF_SHA7ID_unchanged':True,
      'complete_SOURCE11_OUT4_HOST5_formal_TERMINAL6_retained':True,
      'all_original_streams_byteexact_and_scope_honest':True,
      'whole_seconds':summary['whole_seconds'],'child_seconds':summary['child_seconds'],'sampled_peak_RSS_MiB':summary['sampled_peak_rss_mib'],
      'summary_joint_archive_bytes_at_writer_count':summary['joint_archive_bytes'],
      'current_joint_archive_bytes_including_summary_and_writer_tool_receipt':current_total,
      'all_original_caps_genuine_guard_MRO_own_child_cleanup_and_one_stage_PASS_saved_evidence_verified':True,
      'actual_trim_metadata_API_and_full_historical_seven_body_honest_boundaries_retained':True,
      'graph_creation_trace_declaration_prepared_SOURCE_payloads_only_streamed_full_SHA_no_numeric_decode':True,
      'historical_resource_scope_saved_metadata_lexically_checked_no_history_rescan':True,
      'new_production_PREP_saved_META_verified':True,
      'whole_five_stage_build_verified':False,'whole_combined_INPUT_admitted':False,
      'native_RSS_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'goal_complete':False,
      'helper_API_guard_business_executed_by_reviewer':False,'numeric_payload_decoded':False,
      'history_or_unrelated_ART_glob_performed':False,'closed_session16256_repolled':False,
      'D_E_canonical_or_frozen_business_outputs_written':False,
    }
    with (OUT/'REVIEW.json').open('x') as stream:json.dump(report,stream,indent=2,allow_nan=False);stream.write('\n')
    review_pin=pin(OUT/'REVIEW.json')
    print(json.dumps(dict(status=report['status'],checks=len(checks),blockers=[],review=review_pin,
                          unique_explicit_pins=len(explicit_before),Source58=True,inputs67=True,
                          all_namespaces_beforeafter_exact=True,numeric_decode=False,
                          business_or_guard_executed=False)))


if __name__=='__main__':main()
