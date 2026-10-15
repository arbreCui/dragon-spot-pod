"""Independent finite stdlib review. No candidate imports, tool execution, or physical EOF."""
import ast, hashlib, json, math, os, stat, sys
from pathlib import Path

F=Path('/private/tmp/axmat_N7_actual_closed_failure_Source_small_META_1zi95nma')
B=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART=Path('/Users/wen/spot/validation/artifacts')
ROOTS=dict(H=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-host-20261010',O=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-runtime-20261010',C=ART/'axial-material-complete-native-observation-BUILD5-AB-v7-control-20261010',D=B/'actual_complete_native_observation_BUILD5_AB_v7_sources',E=B/'actual_complete_native_observation_BUILD5_AB_v7_receipts')
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2147483648,history_bytes=103079215104,free_floor_bytes=8589934592,threads=1,children_at_once=1,retries=0)
CONFIG=B/'Root_actual_N7_closed_failure_saved_Source_small_META_review_INPUTS.json'
CONFIG_SHA='4c402426f4cf51c6c8d2e26390bdd87bb185c9ec1a751e4209fe29306a7e35ba'
EXPECTED={
 'actual_Root_native_tool_terminal':('4c6b023beb6682ca7701b6c2b8acebcbe11750207cadc6835496c1b2935c9121',12025),
 'actual_failed_host_result':('0b5fddefebe0727981e6af1b9b323436fa3ac2278adda256bf4fff30d744941c',592032),
 'actual_failure_journal':('fd7edde38a76ef03e6ff0bfd36432e8f9045a4d7d624d4bcb0c1458d92a9bbbb',1268881),
 'actual_native_first_watch':('1eea676bca685bdfadb4864fe1787b1ce95d2a44f4a83f2a223476ddfcbb6d11',731),
 'actual_complete_failure_summary':('a6db484afa20c88d6b2c4c433267058635d3a8975b2ac0e55ee6df09ed91420d',9812),
 'actual_complete_failure_namespace_manifest':('0218e203863a5c756530846db44fc73c153c5de44516a3b5d4b17294510d0d44',866467),
 'actual_failure_META_writer_tool_terminal':('ac53d08d85f81e97cd2aeca33248f4c05109ad8ac85ff251b0425f3bf2be6bcb',2507),
 'actual_failure_META_writer_Source':('25b2e6059c80c4a6d66154dcfa71d14853ce377e7507b3fab74ecd4b50a5dc2a',9802),
 'actual_prelaunch_D_E_Source_freeze':('3764f2e2b9ac954515d6d7cc845b1229dd812b7feb35b2f837722e544779e6fd',115247),
 'actual_prelaunch_Source_freeze_tool_terminal':('6aaef4bbfd55d945c8b3cd15559a909cbd0a8c4f37f6c960153cde29adbdf2d3',1543),
 'actual_current_group_liveness':('d16f6027eee6e6aa40de618ea4736a5ecdd62d65d28d03f1d5ba77f9b65047c1',19779),
 'actual_current_group_liveness_tool_terminal':('6aeb485d20c6603cf205a54a468606ecad6a3f46bc797d94f807dfbda9bad189',2808)}
TOOLS={'fortran':'/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15','c':'/usr/bin/gcc','cpp':'/usr/bin/cpp','ar':'/usr/bin/ar','lsof':'/usr/sbin/lsof','ps':'/bin/ps'}
FUTURE_NONE=['actual_runtime_qualification_sha256','actual_observer_native_controls_run','actual_native_Source_binary_linkage_qualification_sha256','actual_scientific_qualification_sha256']
FUTURE_FALSE=['scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted','native_transport_executed','complete_context_aggregation_qualified']
checks=[];readpins={};copies={}

def check(name, value, evidence):
    assert type(value) is bool and name not in [c['name'] for c in checks]
    checks.append(dict(name=name,passed=value,evidence=evidence))
    if not value:raise AssertionError(name)
def identity(p):
    s=p.lstat();return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def fullpin(p):
    p=Path(p);i=identity(p)
    assert p.is_absolute() and p.resolve()==p and stat.S_ISREG(i[2]) and i[3]==1
    h=hashlib.sha256();n=0
    with p.open('rb') as f:
        while True:
            raw=f.read(2**20)
            if not raw:break
            h.update(raw);n+=len(raw)
    assert n==i[4] and identity(p)==i
    q=dict(path=str(p),sha256=h.hexdigest(),size_bytes=n,identity=i);readpins[str(p)]=q;return q
def strict(raw):
    def pairs(rows):
        d={}
        for k,v in rows:
            assert k not in d;d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def load(p,expected=None):
    p=Path(p);q=fullpin(p);m=strict(p.read_bytes());assert fullpin(p)==q
    if expected is not None:assert q==expected
    return m,q
def source(p,expected=None):
    p=Path(p);q=fullpin(p);raw=p.read_bytes();s=raw.decode('utf-8');tree=ast.parse(s,filename=str(p));assert fullpin(p)==q
    if expected is not None:assert q==expected
    return s,tree,q
def pinshape(q):
    return type(q)is dict and set(q)=={'path','sha256','size_bytes','identity'} and type(q['path'])is str and Path(q['path']).is_absolute() and type(q['sha256'])is str and len(q['sha256'])==64 and all(c in '0123456789abcdef'for c in q['sha256']) and type(q['size_bytes'])is int and q['size_bytes']>=0 and type(q['identity'])is list and len(q['identity'])==7 and all(type(v)is int for v in q['identity']) and q['identity'][4]==q['size_bytes']
def metadata_view(p):
    p=Path(p);files={};dirs={};seen=set()
    assert p.is_absolute()and p.resolve()==p
    for q in [p,*sorted(p.rglob('*'))]:
        i=identity(q);assert not stat.S_ISLNK(i[2])
        if stat.S_ISDIR(i[2]):dirs[str(q)]=i
        else:
            assert stat.S_ISREG(i[2])and i[3]==1 and (i[0],i[1])not in seen
            seen.add((i[0],i[1]));files[str(q)]=i
    return dict(root=str(p),files=files,directory_identity=dirs,total_bytes=sum(i[4]for i in files.values()))
def saved_metadata(v):
    assert set(v)=={'root','files','directory_identity','total_bytes'} and all(pinshape(q)for q in v['files'])
    paths=[q['path']for q in v['files']];assert len(paths)==len(set(paths))
    assert v['total_bytes']==sum(q['size_bytes']for q in v['files'])
    return dict(root=v['root'],files={q['path']:q['identity']for q in v['files']},directory_identity=v['directory_identity'],total_bytes=v['total_bytes'])
def typed_caps(v):return type(v)is dict and v==CAPS and all(type(z)is int for z in v.values())
def terminal(v,schema,chunk,exitcode,initial=None,session=None):
    assert v['schema']==schema and v['closed']is True and v['observed_terminal']is True and v['session_repolled_after_close']is False
    t=v['terminal_tool_return'];assert type(t['exit_code'])is int and t['exit_code']==exitcode and 'session_id'not in t and t['chunk_id']==v['actual_terminal_chunk']==chunk and type(t['output'])is str
    if initial is not None:
        i=v['initial_tool_return'];assert i['chunk_id']==initial and i['session_id']==v['original_session_id']==session and 'exit_code'not in i
    return t
def parse_ps(raw,count):
    assert type(raw)is str
    rows=[]
    for line in raw.splitlines():
        words=line.split();assert len(words)==count and all(w.isdigit()for w in words)
        row=tuple(map(int,words));assert row[0]>0;rows.append(row)
    assert len({r[0]for r in rows})==len(rows);return rows
def copy(role,p):
    p=Path(p);q=fullpin(p);dest=F/'REVIEWED_SOURCE_AND_SMALL_META'/role
    dest.parent.mkdir(exist_ok=True);dest.write_bytes(p.read_bytes());dq=fullpin(dest);assert fullpin(p)==q and dq['sha256']==q['sha256']and dq['size_bytes']==q['size_bytes']
    copies[role]=dict(original_fullpin=q,review_copy_fullpin=dq)
def defs(s,t):
    lines=s.splitlines(keepends=True)
    return [(n.name,ast.dump(n,include_attributes=False),''.join(lines[n.lineno-1:n.end_lineno]))for n in ast.walk(t)if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))]
def inverse(bound,rows):
    lines=bound.splitlines(keepends=True)
    for row in rows:
        assert type(row['line'])is int and lines[row['line']-1]==row['new'];lines[row['line']-1]=row['old']
    return ''.join(lines)

def main():
    assert len(sys.argv)==1 and not sys.flags.optimize and sys.getprofile()is None
    cfg,cp=load(CONFIG)
    assert cp['sha256']==CONFIG_SHA and cp['size_bytes']==6300
    pins=cfg['actual_fullpins'];assert set(pins)==set(EXPECTED)
    m={}
    for k,(sha,size)in EXPECTED.items():
        q=pins[k];assert pinshape(q)and(q['sha256'],q['size_bytes'])==(sha,size)and fullpin(q['path'])==q
        if k=='actual_failure_journal':continue
        if k.endswith('_Source'):m[k]=source(q['path'],q)
        else:m[k]=load(q['path'],q)[0]
    check('exact_current_Root_input_contract_and_all_twelve_original_Source_small_META_fullpins',cfg['schema']=='ROOT_ACTUAL_N7_CLOSED_FAILURE_SAVED_SOURCE_SMALL_META_REVIEW_INPUTS_V1'and cfg['source_only']is True and cfg['complete_native_or_AB_observation_success']is False and cfg['new_runtime_or_scientific_qualification']is False,dict(config_pin=cp,roles=pins))
    nt=m['actual_Root_native_tool_terminal'];tr=terminal(nt,'ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_TOOL_TERMINAL_RETURN_V1','d1b354',1,'852d8e',29272)
    assert nt['all_actual_tool_observations']==[nt['initial_tool_return'],tr] and nt['observed_after_actual_terminal_return']is True
    command=nt['actual_launch_arguments']['cmd'];assert str(ROOTS['D']/'Root_bound_complete_observation_genuine_host.py')in command and '/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12 -B'in command and 'PYTHONOPTIMIZE'in command and 'SPOT_AXMAT_OBSERVATION=ADMITTED_SOURCE_ONLY'in command
    for key in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:assert key+'=1'in command
    check('genuine_Root_native_terminal_is_observed_closed_one_no_retry_with_original_launch_and_full_terminal_stream',all(nt[k]is False for k in ['actual_complete_native_build_success','actual_AB_observation_success','scientific_qualification_created','AAA_accuracy_qualified','ABA_admitted','goal_complete'])and nt['actual_instrumented_runtime_controls']is None,dict(initial_chunk='852d8e',session=29272,terminal_chunk=tr['chunk_id'],exit_code=1,output_utf8_bytes=len(tr['output'].encode())))
    summary=m['actual_complete_failure_summary'];ns=m['actual_complete_failure_namespace_manifest'];failed=m['actual_failed_host_result'];freeze=m['actual_prelaunch_D_E_Source_freeze'];watch=m['actual_native_first_watch'];live=m['actual_current_group_liveness']
    wt=terminal(m['actual_failure_META_writer_tool_terminal'],'ROOT_N7_ACTUAL_CLOSED_FAILURE_COMPLETE_META_WRITER_TOOL_TERMINAL_RETURN_V1','ff0f6e',0,'f4a532',74159);wo=strict(wt['output'])
    assert wo['summary_pin']==pins['actual_complete_failure_summary']and wo['complete_namespace_manifest_pin']==pins['actual_complete_failure_namespace_manifest']and wo['failure_journal_pin']==pins['actual_failure_journal']and wo['regular_complete_HOCDE_bytes_after_Root_terminal']==23380698
    assert all(wo[k]is True for k in ['complete_D_E_source_freeze_unchanged','Root_postclose_full_EOF_all154_inputs_unchanged'])and wo['scientific_qualification_created']is False
    check('actual_Root_failure_META_writer_closed_zero_rawstdout_couples_the_current_summary_namespace_and_journal',m['actual_failure_META_writer_tool_terminal']['native_or_material_business_reexecuted']is False and m['actual_failure_META_writer_tool_terminal']['new_runtime_or_scientific_qualification']is False,dict(initial='f4a532',session=74159,terminal='ff0f6e',summary_pin=wo['summary_pin'],manifest_pin=wo['complete_namespace_manifest_pin']))
    ft=terminal(m['actual_prelaunch_Source_freeze_tool_terminal'],'ROOT_N7_ACTUAL_COMPLETE_SOURCE_PRELAUNCH_FREEZE_TOOL_TERMINAL_RETURN_V1','5b9a33',0);fo=strict(ft['output'])
    assert fo['freeze_pin']==pins['actual_prelaunch_D_E_Source_freeze']and(fo['Source_file_count'],fo['Source_directory_count'],fo['receipt_file_count'],fo['receipt_directory_count'])==(186,24,5,1)
    assert freeze['schema']=='ROOT_ACTUAL_N7_COMPLETE_BOUND_SOURCE_META_PRELAUNCH_FREEZE_V1'and freeze['source_only']is True
    assert freeze['all_D_E_members_full_EOF_SHA7ID_verified']is True and freeze['all_D_E_directories_full_7ID_verified']is True and freeze['all_H_O_C_absent']is True
    peer,pp=load(freeze['independent_actual_bound_Source_review_pin']['path'],freeze['independent_actual_bound_Source_review_pin'])
    assert pp['sha256']=='36aab198a4c1bff0a23a86ab234babd1f8e41d9b9c6c42562b7a1e3c206398b0'
    assert peer['schema']=='INDEPENDENT_ACTUAL_N7_BOUND_SOURCE_META_PRELAUNCH_REVIEW_V1'and peer['status']=='PASS_ACTUAL_BOUND_SOURCE_META_PRELAUNCH_NO_EXECUTION_OR_SCIENCE'
    assert peer['check_count']==len(peer['checks'])==4299 and peer['all_checks_typed_true']is True and peer['blockers']==[]and all(c['passed']is True for c in peer['checks'])
    check('actual_prelaunch_Source_only_peer_and_Root_freeze_are_current_N7_not_substituted_old_runtime_qualification',freeze['actual_native_build_or_material_execution']is False and freeze['native_RSS_verified']is False and freeze['scientific_qualification_created']is False,dict(peer_pin=pp,peer_Source_check_count=4299,freeze_pin=pins['actual_prelaunch_D_E_Source_freeze'],full_D_E_counts=[186,24,5,1]))
    request,rp=load(summary['actual_request_pin']['path'],summary['actual_request_pin'])
    inputs=request['original129_input_pins']+request['additional_actual_evidence_input_pins']+list(request['actual_author_Source_contract'].values())
    assert [len(request['original129_input_pins']),len(request['additional_actual_evidence_input_pins']),len(request['actual_author_Source_contract'])]==[129,11,14]
    assert len(inputs)==154 and inputs==failed['complete_input_pins_before']==failed['complete_input_pins_after_failure']==ns['complete_ordered_protected_inputs']==peer['actual_ordered_protected_input_pins']
    assert {k:q['path']for k,q in request['tool_pins'].items()}==TOOLS
    for q in inputs:
        assert pinshape(q)and Path(q['path']).resolve()==Path(q['path'])and identity(Path(q['path']))==q['identity']and stat.S_ISREG(q['identity'][2])
        if q['path']in TOOLS.values():assert q==request['tool_pins'][next(k for k,v in TOOLS.items()if v==q['path'])]and type(q['identity'][3])is int and q['identity'][3]>=1
        else:assert q['identity'][3]==1
    check('all_154_ordered_protected_input_pins_and_six_original_canonical_tool_roles_match_current_full7ID_without_reading_protected_bodies',ns['Root_postclose_full_EOF_all154_inputs_unchanged']is True and summary['Root_postclose_full_EOF_all154_inputs_unchanged']is True,dict(ordered_count=154,groups=[129,11,14],tool_fullpins=request['tool_pins'],independent_check='current7ID and saved exact ordered pin contracts; Root actual postclose fullEOF source/tool coupling'))
    views=ns['actual_complete_namespace_views'];assert set(views)==set(ROOTS)
    before={k:metadata_view(p)for k,p in ROOTS.items()}
    assert all(before[k]==saved_metadata(views[k])for k in ROOTS)
    assert views['D']==freeze['complete_Source_D']and views['E']==freeze['complete_receipt_E']
    assert ns['complete_D_E_source_freeze_unchanged']is True and summary['complete_D_E_source_freeze_unchanged']is True
    assert sum(v['total_bytes']for v in before.values())==23380698
    counts={k:dict(files=len(v['files']),directories=len(v['directory_identity']),regular_bytes=v['total_bytes'])for k,v in before.items()}
    assert counts==dict(H=dict(files=1374,directories=16,regular_bytes=14591009),O=dict(files=0,directories=1,regular_bytes=0),C=dict(files=0,directories=1,regular_bytes=0),D=dict(files=186,directories=24,regular_bytes=8587462),E=dict(files=5,directories=1,regular_bytes=202227))
    all_nodes=[(i[0],i[1])for v in before.values()for i in v['files'].values()];assert len(all_nodes)==len(set(all_nodes))
    check('complete_saved_H_O_C_D_E_namespace_has_exact_current_regular_file7ID_directory7ID_noalias_and_regular_byte_account',True,dict(counts=counts,full_saved_namespace_pin=pins['actual_complete_failure_namespace_manifest'],all1565_current_regular_files_metadata_only=True,object_library_physical_payloads_not_opened=True))
    oldfreeze={a:dict(files=views[k]['files'],directories=views[k]['directory_identity'])for a,k in [('Source','D'),('receipts','E')]}
    assert failed['complete_D_E_freeze_before']==failed['complete_D_E_freeze_after_failure']==oldfreeze
    assert failed['full_postfailure_freeze_errors']==[]and failed['full_postfailure_freeze_checked']is True
    check('failed_runtime_before_after_and_Root_postclose_freezes_preserve_complete_original_D_E_186_and5',True,dict(runtime_failed_result_pin=pins['actual_failed_host_result'],D_root_7ID=views['D']['directory_identity'][str(ROOTS['D'])],E_root_7ID=views['E']['directory_identity'][str(ROOTS['E'])]))
    jp=pins['actual_failure_journal'];raw=Path(jp['path']).read_bytes();assert fullpin(jp['path'])==jp and raw.endswith(b'\n')and len(raw)<8*2**20
    events=[strict(line)for line in raw.splitlines()]
    expected_events=['original_joint_bytes_failure','additional_postfailure_PS_liveness','before_original_terminate_group','additional_postfailure_PS_liveness','original_terminate_group_exception','after_original_terminate_group','additional_postfailure_PS_liveness','before_original_finish_liveness_watchdog','additional_postfailure_PS_liveness','after_original_finish_liveness_watchdog','additional_postfailure_PS_liveness']
    assert len(events)==11 and [e['sequence']for e in events]==list(range(1,12))and [e['event']for e in events]==expected_events
    assert all(e['schema']=='ACTUAL_N7_FAILURE_ONLY_MONITOR_EVENT_V1'and e['actual_host_PID']==51052 for e in events)
    mon=failed['actual_failure_only_monitor_evidence'];assert mon['schema']=='ACTUAL_N7_FAILURE_ONLY_MONITOR_SUMMARY_V1'and mon['journal_pin']==jp and mon['failure_event_count']==11 and mon['additional_recording_errors']==[]and mon['unpersisted_complete_events']==[]and mon['complete_failed_event_journal_persistence_verified']is True
    check('actual_failure_journal_is_complete_saved_EOF_with_eleven_unique_ordered_events_no_recording_errors',True,dict(journal_pin=jp,events=expected_events,raw_line_lengths=[len(line)+1 for line in raw.splitlines()]))
    first=events[0];ps=first['original_ps'];ls=first['original_lsof'];assert ps['actual_argv']==['/bin/ps','-axo','pid=,ppid=']and ps['actual_returncode']==ps['closed_returncode_cached']==0 and ps['streams_complete']is True
    psrows=parse_ps(ps['actual_stdout'],2);selected={51052}
    while True:
        grown=selected|{pid for pid,ppid in psrows if ppid in selected}
        if grown==selected:break
        selected=grown
    assert ps['actual_diagnostic_PID']==51079 and ps['actual_diagnostic_PID']in selected;selected.remove(ps['actual_diagnostic_PID'])
    assert sorted(selected)==first['original_parent_chain_selected_PIDs']==[51052,51076,51077]
    argv=['/usr/sbin/lsof','-nP','-F','pfnsiDt','-a','-p','51052,51076,51077'];assert ls['source_argv_for_actual_selected_PIDs']==ls['actual_returned_argv']==argv and type(ls['actual_returncode'])is int and ls['actual_returncode']==1 and ls['streams_complete']is True and ls['actual_stderr']==''
    headers=[int(line[1:])for line in ls['actual_stdout'].splitlines()if line.startswith('p')and line[1:].isdigit()];assert headers==[51052,51077]and len(ls['actual_stdout'].encode())==16722
    assert first['original_error']['type']=='builtins.ValueError'and first['original_error']['repr']=="ValueError('full live own process file scan required')"and 'joint_bytes'in first['original_error']['complete_traceback']and first['original_scan_failure_still_raises']is True
    assert first['no_strip_or_stream_truncation']is True and first['N6_original_failed_lsof_raw_remains_unknown']is True
    prior=first['latest_prior_successful_original_scan'];assert prior['not_new_liveness_at_cleanup_time']is True and prior['original_lsof_returncode']==0 and prior['original_scan_finished_monotonic']<first['original_scan_started_monotonic']
    check('original_failed_PS_parent_chain_and_lsof_raw_streams_independently_reconstruct_missing_compiler_header_without_accepting_rc1',True,dict(PS_diagnostic_PID=51079,excluded_only_actual_closed_PS_diagnostic=True,selected_PIDs=sorted(selected),lsof_returncode=1,headers=headers,missing=[51076],full_stdout_UTF8_bytes=16722,complete_stderr=ls['actual_stderr'],compiler_state_at_original_scan='unknown; PS has no state column',lsof_failure_cause='unknown',prior_successful_scan_is_only_prior=True))
    psev=[e for e in events if e['event']=='additional_postfailure_PS_liveness'];assert len(psev)==5
    for e in psev:
        assert e['actual_argv']==['/bin/ps','-axo','pid=,ppid=,pgid=']and e['actual_returncode']==0 and e['actual_stderr']==''and e['streams_complete']is True and e['observed']is True and e['original_failed_selection']==[51052,51076,51077]and e['original_selection_not_changed']is True and e['used_to_accept_original_failure']is False
        rows=[dict(zip(['pid','ppid','pgid'],r))for r in parse_ps(e['actual_stdout'],3)];targets=set(selected)
        if e['business_child_PID']is not None:targets.add(e['business_child_PID'])
        assert [r for r in rows if r['pid']in targets]==e['actual_selected_or_child_rows']and [r for r in rows if e['business_child_PID']is not None and r['pgid']==e['business_child_PID']]==e['actual_child_process_group_rows']
    assert [r['pid']for r in psev[-1]['actual_selected_or_child_rows']]==[51052,51076]
    cleanup=events[4];assert events[2]['cached_business_returncode']is None and events[2]['actual_business_PID']==51076 and events[2]['original_object_captured_before_wrapping']is True
    assert cleanup['actual_cleanup_exception']['type']=='builtins.PermissionError'and cleanup['actual_cleanup_exception']['repr']=="PermissionError(1, 'Operation not permitted')"and 'os.killpg'in cleanup['actual_cleanup_exception']['complete_traceback']and cleanup['actual_business_PID']==51076
    assert events[5]['original_delegate_returned']is False and events[5]['cached_business_returncode']is None
    assert events[7]['actual_watchdog_PID']==51077 and events[7]['original_active_exception']['type']=='builtins.PermissionError'and events[9]['actual_watchdog_PID']==51077 and events[9]['cached_watchdog_returncode']==1 and events[9]['original_delegate_returned']is True
    assert all(e['cleanup_success_not_inferred']is True for e in events if 'cleanup_success_not_inferred'in e)
    check('full_original_cleanup_EP ERM_and_watchdog_lifecycle_are_preserved_without_backfilling_success'.replace('EP ERM','EPERM'),True,dict(original_cleanup_exception=cleanup['actual_cleanup_exception'],compiler_cached_returncode_during_cleanup=None,watchdog_final_cached_returncode=1,postfinish_PS_still_lists_compiler=True,no_PS_state_evidence=True))
    for e in events:
        cl=e['clock'];assert all(type(cl[k])in(int,float)and math.isfinite(cl[k])and cl[k]>0 for k in ['whole_seconds_remaining','stage_seconds_remaining'])and all(cl[k]is True for k in ['whole_cap_satisfied','stage_cap_satisfied','no_additional_time_budget'])
        account=e['actual_diagnostic_write_byte_account_before'];history=account['actual_original_history_check'];assert account['current_open_unlinked_verified']is False and account['failed_scan_never_replaced_by_this_account']is True
        assert all(type(account[k])is int and account[k]>=0 for k in ['actual_regular_joint_bytes','additional_record_bytes','previous_complete_open_unlinked_bytes','external_D_E_bytes'])
        assert account['actual_regular_joint_bytes']+account['previous_complete_open_unlinked_bytes']+account['additional_record_bytes']<CAPS['joint_archive_bytes']
        assert history['artifact_bytes']+account['external_D_E_bytes']+account['previous_complete_open_unlinked_bytes']+account['additional_record_bytes']<=CAPS['history_bytes']and history['disk_free_bytes']-account['additional_record_bytes']>=CAPS['free_floor_bytes']
    assert typed_caps(mon['original_caps'])and mon['new_instrumented_runtime_controls_actual']is None and mon['new_native_runtime_qualification']is None and mon['N6_original_failed_lsof_raw_remains_unknown']is True
    check('added_failure_evidence_has_original_clock_and_recorded_byte_caps_with_failed_current_open_unlinked_scope_explicitly_unknown',True,dict(original_caps=CAPS,actual_recorded_clock_rows=[e['clock']for e in events],recorded_byte_accounts_checked=11,current_failed_open_unlinked_bytes=None,regular_only_postclose_snapshot_not_resource_gate_repair=True))
    assert failed['schema']=='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1'and failed['status']=='FAILED_NO_RETRY_NO_QUALIFICATION'and failed['error']=="PermissionError(1, 'Operation not permitted')"and typed_caps(failed['original_caps'])
    stages=failed['all_stage_records'];assert len(stages)==1 and stages[0]['label']=='native/Ganlib/src/compile_cle2000_c'and stages[0]['status']=='FAILED'and stages[0]['command']==watch['command']and stages[0]['error']=='[Errno 1] Operation not permitted'
    assert watch['pid']==51076 and type(watch['returncode'])is int and watch['returncode']==0 and watch['limit_failure']=="ValueError('full live own process file scan required')"and watch['sampled_peak_rss_mib']==0.0 and watch['rss_cap_mib']==512 and watch['own_child_only']is True and watch['liveness_group_cleanup']is True
    assert watch['elapsed_seconds']==9.764043999952264 and failed['whole_seconds']==14.147054916946217 and stages[0]['elapsed_seconds']==10.10903479193803 and summary['actual_host_whole_seconds']==failed['whole_seconds']
    assert len(views['O']['files'])==len(views['C']['files'])==0 and failed['actual_observation_manifest_pin_if_saved']is None and failed['actual_Root_observed_terminal']is None
    for p in [ROOTS['H']/'result.json',ROOTS['C']/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',ROOTS['O']/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json']:assert not os.path.lexists(p)
    compiled=[q for q in views['H']['files']if Path(q['path']).suffix in ['.o','.a']];assert len(compiled)==1 and compiled[0]['path']==str(ROOTS['H']/'native/Ganlib/src/cle2000_c.o')
    check('only_first_compiler_child_closed_zero_but_genuine_stage_and_host_failed_no_whole_BUILD_link_or_A_B_material_result',True,dict(first_child_watch_pin=pins['actual_native_first_watch'],child_elapsed_seconds=watch['elapsed_seconds'],stage_elapsed_seconds=stages[0]['elapsed_seconds'],whole_seconds=failed['whole_seconds'],compiled_object_saved_Root_pin_metadata_only=compiled[0],watch_cleanup_true_literal_is_not_cleanup_proof=True,sampled_RSS_zero_is_not_RSS_qualification=True))
    lt=terminal(m['actual_current_group_liveness_tool_terminal'],'ROOT_N7_CLOSED_FAILURE_CURRENT_PROCESS_GROUP_LIVENESS_TOOL_TERMINAL_RETURN_V1','51aa23',0);lo=strict(lt['output']);assert lo['diagnostic_path']==pins['actual_current_group_liveness']['path']and lo['actual_pid_ppid_pgid_matches']==[]and lo['current_target_groups_absent']is True and lo['no_process_termination_attempted']is True
    assert live['schema']=='ROOT_ACTUAL_N7_CLOSED_FAILURE_CURRENT_PROCESS_GROUP_LIVENESS_DIAGNOSTIC_V1'and live['actual_PS_argv']==['/bin/ps','-axo','pid=,ppid=,pgid=']and live['actual_PS_returncode']==0 and live['complete_actual_PS_stderr']==''and live['targets']==[51052,51076,51077]
    targets=set(live['targets']);matches=[dict(zip(['pid','ppid','pgid'],r))for r in parse_ps(live['complete_actual_PS_stdout'],3)if any(z in targets for z in r)]
    assert matches==live['actual_pid_ppid_pgid_matches']==[]and live['current_target_groups_absent']is True and live['original_runtime_cleanup_success_not_backfilled']is True and live['no_process_termination_attempted']is True and live['original_N6_failed_lsof_raw_remains_unknown']is True
    check('later_Root_current_liveness_closed_zero_has_no_PID_PPID_PGID_target_matches_and_no_termination_attempt',True,dict(actual_liveness_pin=pins['actual_current_group_liveness'],actual_UTC=live['observed_at_UTC'],actual_chunk='51aa23',matches=[],past_cleanup_and_original_scan_state_not_backfilled=True))
    bound_source={};inverse_m,invpin=load(ROOTS['D']/'Root_actual_observation_bound_Source_full_inverse.json')
    for role,filename,key in [('host','Root_bound_complete_observation_genuine_host.py','host_complete_inverse_hunks'),('runtime','Root_bound_complete_observation_runtime.py','runtime_complete_inverse_hunks')]:
        q=peer['actual_four_Root_bound_output_pins'][filename];s,t,sq=source(q['path'],q);bound_source[role]=(s,t,sq)
        oq=peer['actual_full_source_inverse'][role]['actual_original_Source_pin'];old,ot,op=source(oq['path'],oq);back=inverse(s,inverse_m[key]);assert back==old and ast.dump(ast.parse(back),include_attributes=False)==ast.dump(ot,include_attributes=False)and defs(s,t)==defs(old,ot)
        copy('original_author_'+role+'.py',oq['path']);copy('actual_bound_'+role+'.py',q['path'])
    assert len(inverse_m['host_complete_inverse_hunks'])==11 and len(inverse_m['runtime_complete_inverse_hunks'])==1
    runsrc=next(body for name,at,body in defs(bound_source['runtime'][0],bound_source['runtime'][1])if name=='run')
    assert 'class JointHistoryResources(resource.DynamicHistoryResources)'in runsrc and 'full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)'in runsrc and 'runner=full.OwnRSSSerialExecutor'in runsrc and "for state in('A','B')"in runsrc
    assert runsrc.index('before=resources.check()')<runsrc.index('host.mkdir()')<runsrc.index('runner=full.OwnRSSSerialExecutor')<runsrc.index('monitor.install_bounded_wrappers')<runsrc.index('ep,build=compile_all')<runsrc.index("for state in('A','B')")
    check('current_actual_bound_complete_host_and_runtime_byte_AST_inverse_and_all_definition_occurrences_preserve_original_Source',True,dict(bound_Source_pins={k:z[2]for k,z in bound_source.items()},whole_inverse_pin=invpin,host_hunks=11,runtime_hunks=1,original_guard_MRO_and_build_A_B_order_preserved=True,no_import_or_execution=True))
    guard_info={}
    for name,sha in [('qualify_refined_AAA_layered_full.py','70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'),('production_runner.py','38de03ed0f5b3e2d82b4153a45d1e548d58a34747f526f8bcd51bbe01e935128'),('run_bounded_dragon.py','bc4ff7a5dc82ed023b726f2304b6a298954f54d7891414925b7d6d68dd80cf09')]:
        p=ROOTS['D']/'GUARD_SOURCE'/name;s,t,q=source(p);assert q['sha256']==sha;guard_info[name]=dict(pin=q,definitions=[dict(name=n.name,start=n.lineno,end=n.end_lineno)for n in ast.walk(t)if isinstance(n,(ast.FunctionDef,ast.ClassDef))]);copy('actual_guard_'+name,p)
        if name=='run_bounded_dragon.py':assert fullpin(ROOTS['H']/'runtime'/name)['sha256']==sha;copy('actual_H_guard_'+name,ROOTS['H']/'runtime'/name)
    fulltext=(ROOTS['D']/'GUARD_SOURCE/qualify_refined_AAA_layered_full.py').read_text();assert fulltext.index('self.resources.check();last_disk=now')<fulltext.index('failure=repr(error);self.bounded.terminate_group(process);raise')<fulltext.index('self.bounded.finish_liveness_watchdog(write_fd,watchdog)')
    check('genuine_OwnRSS_production_and_bounded_guard_fullSource_bytes_AST_and_actual_H_guard_copy_are_unchanged',True,dict(guard_Source=guard_info,guard_lifecycle='poll -> resources.check -> except terminate_group -> finally finish_watchdog -> watch poll; EPERM can replace prior ValueError; unconditional cleanup flag is not proof'))
    wsource,wtree,wsourcepin=m['actual_failure_META_writer_Source'];assert 'inputs=request[\'original129_input_pins\']+request[\'additional_actual_evidence_input_pins\']+list(request[\'actual_author_Source_contract\'].values())'in wsource and 'for q in inputs:assert pin(Path(q[\'path\']),tool=q[\'path\'] in tools)==q'in wsource
    assert 'ns={k:tree(p)'in wsource and "ns['D']==freeze['complete_Source_D']"in wsource and "ns['E']==freeze['complete_receipt_E']"in wsource and 'actual_complete_namespace_views=ns'in wsource
    assert "assert {k:tree(p)"in wsource and 'sum(v[\'total_bytes\'] for v in ns.values())'in wsource and 'failed_original_scan_open_unlinked_bytes_unknown=True'in wsource
    check('actual_closed_Root_META_writer_complete_Source_contract_checks_all154_fullEOF_twice_and_all_five_namespace_fullEOF_views',True,dict(actual_writer_Source_pin=wsourcepin,actual_META_writer_terminal_pin=pins['actual_failure_META_writer_tool_terminal'],Root_fullEOF_claim_exactly_scoped_to_actual_writer_not_independent_payload_read=True))
    assert summary['schema']=='ROOT_ACTUAL_N7_CLOSED_FAILURE_COMPLETE_SUMMARY_V1'and summary['status']=='ACTUAL_NATIVE_DIAGNOSTIC_FAILED_CLOSED_NO_RETRY_NO_QUALIFICATION'and ns['schema']=='ROOT_ACTUAL_N7_CLOSED_FAILURE_COMPLETE_HOCDE_NAMESPACE_MANIFEST_V1'
    links={'actual_Root_terminal_pin':'actual_Root_native_tool_terminal','actual_failed_host_result_pin':'actual_failed_host_result','actual_prelaunch_D_E_freeze_pin':'actual_prelaunch_D_E_Source_freeze','actual_complete_failure_namespace_manifest_pin':'actual_complete_failure_namespace_manifest','actual_failure_journal_pin':'actual_failure_journal','actual_genuine_watchdog_pin':'actual_native_first_watch','actual_current_group_liveness_evidence_pin':'actual_current_group_liveness','failure_META_writer_pin':'actual_failure_META_writer_Source'}
    assert all(summary[k]==pins[v]for k,v in links.items())and summary['actual_genuine_watchdog']==watch and summary['actual_cleanup_error']==cleanup['actual_cleanup_exception']
    assert summary['actual_Root_terminal_chunk']=='d1b354'and summary['actual_Root_terminal_exit_code']==1 and summary['actual_failure_journal_rows']==11 and summary['regular_complete_HOCDE_bytes_after_Root_terminal']==23380698
    assert typed_caps(summary['original_caps'])and typed_caps(ns['original_caps'])and typed_caps(request['original_caps'])
    for obj in [failed,request,peer]:assert all(obj[k]is None for k in FUTURE_NONE)and all(obj[k]is False for k in FUTURE_FALSE)
    assert all(summary[k]is True for k in ['Root_postclose_revalidation_does_not_replace_original_runtime_failed_monitor','watchdog_elapsed_includes_added_failure_diagnostics_and_cleanup','sampled_RSS_zero_is_early_exit_not_native_RSS_qualification','current_closed_failure_groups_absent','original_cleanup_success_not_backfilled','original_N6_failed_lsof_raw_and_cause_remain_unknown','closed_compiler_process_state_at_original_scan_unknown','failed_original_scan_open_unlinked_bytes_unknown','regular_only_snapshot_does_not_repair_failed_resource_gate'])
    assert all(summary[k]is False for k in ['whole_five_stage_build_executed','actual_AB_observation_manifest_saved','native_RSS_verified','native_build_qualified','complete_context_aggregation_qualified','physical_neutron_balance_qualified','scientific_accuracy_qualified','AAA_accuracy_qualified','ABA_admitted','goal_complete'])and summary['new_instrumented_guard_controls_actual']is None and ns['new_runtime_or_native_or_scientific_qualification']is False
    check('all_saved_failure_evidence_exactly_couples_current_truth_and_leaves_original_unknowns_and_future_native_science_unqualified',True,dict(N6_original_raw_unknown=True,N7_original_lsof_cause_unknown=True,N7_original_process_state_unknown=True,failed_current_open_unlinked_bytes=None,current_later_absence_not_past_cleanup_proof=True,no_whole_native_BUILD_link_A_B_science=True))
    for role,q in pins.items():copy(role+('.py'if role.endswith('_Source')else'.jsonl'if role=='actual_failure_journal'else'.json'),q['path'])
    copy('actual_Root_INPUTS.json',CONFIG);copy('actual_prelaunch_bound_Source_peer_REVIEW.json',pp['path']);copy('actual_request.json',rp['path']);copy('actual_bound_full_inverse.json',invpin['path'])
    after={k:metadata_view(p)for k,p in ROOTS.items()};assert after==before
    for q in inputs:assert identity(Path(q['path']))==q['identity']
    for q in list(readpins.values()):assert fullpin(q['path'])==q
    check('complete_original_namespace_and_all_reviewed_Source_META_fullpins_remain_unchanged_after_independent_read_and_finite_copy',True,dict(no_project_H_O_C_D_E_write=True,all_154_current7ID_after_same=True,full_namespace_counts=counts,finite_reviewed_copy_count=len(copies)))
    report=dict(schema='INDEPENDENT_ACTUAL_CLOSED_N7_FAILURE_SOURCE_SMALL_META_REVIEW_V1',status='PASS_SAVED_FAILED_N7_SOURCE_SMALL_META_ONLY_NO_RUNTIME_OR_SCIENCE',source_only=True,checks=checks,check_count=len(checks),all_checks_passed=True,all_checks_typed_true=True,blockers=[],actual_input_config_pin=cp,actual_Root_input_contract_pins=pins,actual_Root_closed_native_terminal=dict(initial_chunk='852d8e',session_id=29272,terminal_chunk='d1b354',exit_code=1,closed=True),actual_Root_closed_META_writer_terminal=dict(initial_chunk='f4a532',session_id=74159,terminal_chunk='ff0f6e',exit_code=0,closed=True),actual_current_process_liveness_terminal=dict(chunk='51aa23',exit_code=0,closed=True),actual_current_Root_complete_HOCDE_namespace_manifest_pin=pins['actual_complete_failure_namespace_manifest'],actual_complete_namespace_counts=counts,actual_independent_current_metadata_views_before=before,actual_independent_current_metadata_views_after=after,actual_Root_full_EOF_scope_preserved=True,actual_independent_full_EOF_reads_limited_to_Source_and_saved_small_META=True,all_154_original_payload_or_tool_bodies_not_reread=True,native_object_and_libraries_payload_not_opened=True,actual_regular_complete_HOCDE_bytes=23380698,actual_failed_current_open_unlinked_bytes=None,actual_complete_original_failure_journal_pin=jp,actual_original_failure_sequence=[dict(sequence=e['sequence'],event=e['event'])for e in events],actual_original_monitor_facts=dict(host_PID=51052,PS_returncode=0,selected_PIDs=[51052,51076,51077],lsof_returncode=1,actual_lsof_headers=[51052,51077],missing_header_PID=51076,stdout_utf8_bytes=16722,stderr='',original_process_state='unknown',original_failure_cause='unknown',cleanup_exception=cleanup['actual_cleanup_exception'],watchdog_cached_final_returncode=1),first_compiler_child_watch_pin=pins['actual_native_first_watch'],actual_whole_seconds=failed['whole_seconds'],actual_first_child_elapsed_seconds=watch['elapsed_seconds'],first_child_elapsed_includes_failure_diagnostics_and_cleanup=True,actual_current_groups_absent_after_closed=True,original_cleanup_not_backfilled=True,N6_original_lsof_raw_and_cause_remain_unknown=True,actual_reviewed_Source_small_META_original_pins={k:v for k,v in readpins.items()if not Path(k).is_relative_to(F)},finite_lossless_reviewed_Source_small_META_copies=copies,original_caps=CAPS,all_154_ordered_protected_input_pins=inputs,no_candidate_guard_API_PS_lsof_native_compile_material_numeric_executed_by_review=True,project_or_parent_or_HOCDE_modified=False,complete_native_build_qualified=False,actual_AB_observation_saved=False,new_runtime_qualification=None,actual_instrumented_guard_controls=None,native_RSS_verified=False,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,goal_complete=False)
    report['actual_independent_executed_reviewer_Source_pin']=fullpin(Path(__file__))
    out=F/'REVIEW.json';out.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');q=fullpin(out)
    print(json.dumps(dict(status=report['status'],review_directory=str(F),review_pin=q,check_count=len(checks),all_checks_typed_true=True,blockers=[],reviewed_copy_count=len(copies),namespace_counts=counts,native_or_science_qualification=False),allow_nan=False))

if __name__=='__main__':main()
