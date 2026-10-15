"""SOURCE DESIGN ONLY. Root may run once after an actual closed V21 build tool return.
Standard-library metadata operations only; no project module import or API call.
Successful metadata is link-identity evidence, never whole INPUT/native/science admission.
"""
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import time

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART = Path('/Users/wen/spot/validation/artifacts')
D = BASE/'actual_complete_combined_build_v21_sources'
E = BASE/'actual_complete_combined_build_v21_receipts'
H = ART/'axial-material-complete-combined-build-host-v21-20261010'
S = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v21-20261010'
O = ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v21-20261010'
T = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v21-20261010'
FACTORY = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v21.py')
FACTORY_SHA = '023abc88dd60e89cb49ebacb881f555850b7732149b14caf14503bd135a391e5'
HOST_SOURCE = D/'combined_build_host.py'
HOST_SHA = 'ebe99a7aaf7abd4e073d0e206bea205344e186d5a3be144a012443f1cd51a196'
DECL_SHA = '80d67cd194eed1d229e46cd5512df9ba4b00954e7f6e7b36dd8ea6902851d6af'
PREP_SHA = '7e340a31596aa58518ebde4231bd3542554acb0a4ea1888f1df7ea14bec50dcf'
HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py')
HELPER_SHA = 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7'
Q = BASE/'Root_actual_complete_graph_private_verifier_helper_admission_v21.json'
Q_SHA = '29ac1abd0df3ff9d1d71a3239842e1c97cb2619cc4627292b0d25f6e16218bb2'
MERGED_CAPTURE_SOURCE = Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py')
MERGED_CAPTURE_SHA = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
INNER_FAMILY = 'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V21'
PREFIX = 'AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V21'
TERMINAL_SCHEMA = PREFIX+'_ACTUAL_EXTERNAL_TERMINAL_RETURN_V1'
LABELS = ['build/link','metadata/objects','metadata/executable','metadata/dependencies','audit/audit']
TAIL_FIELDS = ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')
WHOLE, STAGE, RSS, ARCHIVE, HISTORY, FREE = 1800, 600, 512, 2*2**30, 96*2**30, 8*2**30
HISTORY_POLICY = 'AXMAT_DYNAMIC_AXIAL_FAMILY_COMPLETE_HISTORY_V1'
ROOTS = (H,S,O,T,D)
FALSE_FIELDS = ('whole_combined_INPUT_admitted','production_admission_API_executed',
    'new_native_transport_executed','native_RSS_qualified','combined_runtime_native_RSS_proved',
    'mathematical_controls_newly_executed','actual_full_FLU_entry_executed',
    'AAA_accuracy_qualified','ABA_admitted','physics_qualified','goal_complete')
OUT_NAMES = ('Root_actual_complete_build_namespace_manifest.json',
    'Root_actual_complete_combined_build_summary.json',
    'Root_actual_failed_build_namespace_manifest.json',
    'Root_actual_failed_complete_combined_build_summary.json')
T_NAMES = ('actual_build_child_merged_stdout_stderr.json','actual_build_external_host_stdout.json',
    'actual_build_external_host_stderr.txt','actual_build_external_Root_tool_terminal.json',
    'terminal_return.json','failed_build_terminal_return.json')

def identity(p):
    s=Path(p).lstat()
    return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def ordinary(p, directory=False):
    p=Path(p)
    if not p.is_absolute() or '..' in p.parts: raise ValueError('absolute ordinary path required')
    for q in [*reversed(p.parents),p]:
        qid=identity(q)
        if stat.S_ISLNK(qid[2]) or (q!=p and not stat.S_ISDIR(qid[2])):
            raise ValueError('ordinary ancestors required: '+str(q))
    if directory and not stat.S_ISDIR(identity(p)[2]): raise ValueError('ordinary directory required')
    return p

def pin(p):
    p=ordinary(p); before=identity(p)
    if not stat.S_ISREG(before[2]): raise ValueError('regular metadata/input file required')
    with p.open('rb') as f: digest=hashlib.file_digest(f,'sha256').hexdigest()
    if identity(p)!=before: raise ValueError('full EOF file changed: '+str(p))
    return dict(path=str(p),sha256=digest,identity=before)

def short(p):
    q=pin(p)
    return dict(path=q['path'],sha256=q['sha256'])

def exact_pin(q):
    original_id=q.get('identity',q.get('identity7'))
    if 'identity' in q and 'identity7' in q and q['identity']!=q['identity7']:
        raise ValueError('explicit metadata seven-part identity aliases differ')
    expected=dict(path=q['path'],sha256=q['sha256'],identity=original_id)
    if type(expected['identity']) is not list or len(expected['identity'])!=7 or any(type(v) is not int for v in expected['identity']):
        raise ValueError('exact integer seven-part identity required')
    actual=pin(expected['path'])
    if actual!=expected: raise ValueError('prelaunch full EOF SHA/7ID differs: '+expected['path'])
    return actual

def pairs(items):
    answer={}
    for k,v in items:
        if k in answer: raise ValueError('duplicate metadata key: '+k)
        answer[k]=v
    return answer

def reject_nonfinite(value):
    raise ValueError('nonfinite metadata number: '+value)

def read(p):
    b=ordinary(p).read_bytes()
    return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=reject_nonfinite)

def bound_read(p,sha):
    if pin(p)['sha256']!=sha: raise ValueError('Root argument SHA differs: '+str(p))
    value=read(p)
    if pin(p)['sha256']!=sha: raise ValueError('Root metadata changed during parse')
    return value

def write_new(p,value):
    ordinary(Path(p).parent,directory=True)
    with Path(p).open('x') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def copy_exact(src,dst):
    before=pin(src)
    with ordinary(src).open('rb') as source,Path(dst).open('xb') as target:
        while True:
            chunk=source.read(1024*1024)
            if not chunk: break
            target.write(chunk)
    if pin(src)!=before or pin(dst)['sha256']!=before['sha256']: raise ValueError('byte-exact actual stream copy differs')
    return pin(dst)

def snapshot(root,missing_allowed=False):
    root=Path(root)
    if not os.path.lexists(root):
        if not missing_allowed: raise ValueError('required namespace absent: '+str(root))
        return dict(root=str(root),present=False,files={},directories={},symlinks={})
    ordinary(root,directory=True)
    files={};directories={'.':identity(root)};symlinks={}
    for folder,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort()
        for name in dirs+names:
            path=Path(folder)/name;key=str(path.relative_to(root));pid=identity(path)
            if stat.S_ISLNK(pid[2]):
                symlinks[key]=dict(identity=pid,literal_target=os.readlink(path))
            elif stat.S_ISDIR(pid[2]): directories[key]=pid
            elif stat.S_ISREG(pid[2]): files[key]=pin(path)
            else: raise ValueError('unexpected nonregular namespace entry: '+str(path))
        dirs[:]=[name for name in dirs if not (Path(folder)/name).is_symlink()]
    if any(identity(root/name)!=pid for name,pid in directories.items()): raise ValueError('namespace directories changed')
    if any(pin(q['path'])!=q for q in files.values()): raise ValueError('namespace files changed')
    for name,q in symlinks.items():
        if identity(root/name)!=q['identity'] or os.readlink(root/name)!=q['literal_target']: raise ValueError('namespace symlink changed')
    return dict(root=str(root),present=True,files=files,directories=directories,symlinks=symlinks)

def compact_inventory(view):
    if not view['present']: raise ValueError('complete inventory namespace absent')
    return dict(files={k:q['sha256'] for k,q in view['files'].items()},
        symlinks={k:q['literal_target'] for k,q in view['symlinks'].items()},
        directories=sorted(k for k in view['directories'] if k!='.'))

def namespace_bytes(views):
    return sum(q['identity'][4] for view in views for q in view['files'].values())

def typed_terminal(record):
    if record.get('closed') is not True or record.get('observed_after_actual_terminal_return') is not True:
        raise ValueError('Root actual observed CLOSED record required')
    if record.get('session_repolled_after_close') is not False:
        raise ValueError('actual no-repoll observation required')
    terminal=record['terminal_tool_return']
    if type(terminal.get('exit_code')) is not int or 'session_id' in terminal:
        raise ValueError('strict integer terminal code without live handle required')
    if type(record.get('exit_code')) is not int or record['exit_code']!=terminal['exit_code']:
        raise ValueError('Root terminal code fields disagree')
    initial=record['initial_tool_return'];sid=record['original_session_id']
    if type(sid) is not int or initial.get('session_id')!=sid or 'exit_code' in initial:
        raise ValueError('Root original live launch record required')
    closed_seen=False
    for value in record['observations']:
        if closed_seen: raise ValueError('Root observations after terminal forbidden')
        if 'session_id' in value and value['session_id']!=sid: raise ValueError('Root observed foreign session')
        if 'exit_code' in value:
            if value!=terminal: raise ValueError('Root terminal observations disagree')
            closed_seen=True
    if record.get('record_producer')!='root': raise ValueError('actual Root producer required')
    return terminal

def compare_source_freeze(freeze):
    if freeze['schema']!='ROOT_V21_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' or freeze['source_root']!=str(D):
        raise ValueError('fixed V21 SOURCE freeze required')
    if freeze['symlinks']!={} or freeze['no_SOURCE_append_after_freeze'] is not True:
        raise ValueError('complete no-append SOURCE freeze required')
    view=snapshot(D)
    if view['symlinks']!={} or set(view['files'])!=set(freeze['complete_files']):
        raise ValueError('complete frozen SOURCE file set changed')
    for key,q in freeze['complete_files'].items():
        original=exact_pin(q)
        if view['files'][key]!=original or q['size_bytes']!=original['identity'][4]: raise ValueError('full SOURCE pin differs')
    if view['directories']!=freeze['complete_directories']:
        raise ValueError('all original SOURCE directory seven-part identities differ')
    if type(freeze['actual_complete_SOURCE_file_count']) is not int or freeze['actual_complete_SOURCE_file_count']!=len(view['files']):
        raise ValueError('dynamic complete SOURCE count differs')
    return view


def validate_prepared_metadata(preflight):
    q=preflight['prepared_namespace_manifest']
    exact_pin(q)
    saved=bound_read(q['path'],q['sha256'])
    originals={view['root']:view for view in saved['namespaces']}
    checks=[];failures=[]
    for root in (S,T):
        original=originals[str(root)]
        now=snapshot(root)
        if set(now['files'])!=set(original['files']) or now['symlinks']!=original.get('symlinks',{}):
            failures.append(dict(root=str(root),error='full original prepared SOURCE/TERMINAL file/symlink set changed'))
        for key,p in original['files'].items():
            try:
                exact_pin(p)
                checks.append(dict(scope='ORIGINAL_PREPARED_SOURCE_OR_TERMINAL',relative_path=key,pin=p))
            except (ValueError,OSError) as error:
                failures.append(dict(root=str(root),path=p['path'],error=repr(error)))
        original_dirs=original.get('directories',[])
        if type(original_dirs) is list:
            for item in original_dirs:
                if type(item) is dict:
                    if now['directories'].get(item['path'])!=item['identity']:
                        failures.append(dict(root=str(root),directory=item['path'],error='original directory full 7ID differs'))
        elif type(original_dirs) is dict:
            for key,value in original_dirs.items():
                if now['directories'].get(key)!=value:
                    failures.append(dict(root=str(root),directory=key,error='original directory full 7ID differs'))
    expected_o4=('declaration.json','input_graph.json','input_creation_python_open_trace.json','runtime/run_bounded_dragon.py')
    old_out=originals[str(O)]
    for key in expected_o4:
        p=old_out['files'][key]
        try:
            exact_pin(p);checks.append(dict(scope='ORIGINAL_PREP_OUT_FOUR_FILES',relative_path=key,pin=p))
        except (ValueError,OSError) as error:
            failures.append(dict(root=str(O),path=p['path'],error=repr(error)))
    return dict(original_manifest=q,verified_original_entries=checks,failures=failures,
        original_S_T_entries_unchanged=not any(p.get('root') in (str(S),str(T)) for p in failures),
        original_PREP_OUT_four_unchanged=not any(p.get('root')==str(O) for p in failures),
        original_root_directory_7ID_claimed_only_if_captured_in_saved_manifest=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--writer-sha256',required=True)
    for key in ('root-terminal','source-freeze','prelaunch-pins','parent-stdout','parent-stderr'):
        parser.add_argument('--'+key,required=True)
        parser.add_argument('--'+key+'-sha256',required=True)
    args=parser.parse_args()
    writer_pin=pin(Path(__file__).absolute())
    if writer_pin['sha256']!=args.writer_sha256: raise ValueError('actual reviewed failure-only writer SOURCE required')
    expected={'root-terminal':E/'Root_actual_build_tool_terminal_return.json',
        'source-freeze':E/'Root_prelaunch_complete_build_source_freeze.json',
        'prelaunch-pins':E/'Root_final_prelaunch_source_input_and_reserve_check.json',
        'parent-stdout':E/'parent_stdout.log','parent-stderr':E/'parent_stderr.log'}
    paths={key:Path(getattr(args,key.replace('-','_'))) for key in expected}
    if paths!=expected: raise ValueError('fixed original actual Root receipt and stream paths required')
    ordinary(E,directory=True);ordinary(T,directory=True)
    failure_outputs=('Root_actual_failed_build_namespace_manifest.json','Root_actual_failed_complete_combined_build_summary.json')
    if any(os.path.lexists(E/name) for name in failure_outputs) or any(os.path.lexists(T/name) for name in T_NAMES):
        raise ValueError('fresh one-use failure metadata writer; never overwrite or retry')
    metadata={}
    for key,path in paths.items():
        sha=getattr(args,key.replace('-','_')+'_sha256')
        if pin(path)['sha256']!=sha: raise ValueError('actual Root input SHA differs')
        metadata[key]=pin(path)
    actual=bound_read(paths['root-terminal'],args.root_terminal_sha256)
    terminal=typed_terminal(actual)
    if terminal['exit_code']==0: raise ValueError('failure-only refuses EXIT0; no success receipt construction exists')
    preflight=bound_read(paths['prelaunch-pins'],args.prelaunch_pins_sha256)
    freeze=bound_read(paths['source-freeze'],args.source_freeze_sha256)
    fixed=preflight['fixed_input_pins']
    if type(fixed) is not list: raise ValueError('original ordered fixed-input list required')
    unchanged=[];failures=[]
    for index,q in enumerate(fixed):
        try: unchanged.append(dict(index=index,pin=exact_pin(q)))
        except (ValueError,OSError) as error: failures.append(dict(index=index,expected=q,error=repr(error)))
    source_ok=False;source_error=None
    try: compare_source_freeze(freeze);source_ok=True
    except (ValueError,OSError,KeyError,TypeError) as error: source_error=repr(error)
    prepared=None;prepared_error=None
    try: prepared=validate_prepared_metadata(preflight)
    except (ValueError,OSError,KeyError,TypeError) as error: prepared_error=repr(error)
    fixed_sources=[]
    for path,sha in ((FACTORY,FACTORY_SHA),(HOST_SOURCE,HOST_SHA),(HELPER,HELPER_SHA),
        (Q,Q_SHA),(MERGED_CAPTURE_SOURCE,MERGED_CAPTURE_SHA)):
        p=pin(path)
        if p['sha256']!=sha: raise ValueError('fixed current canonical/normal-host/helper/Q/capture Source differs')
        fixed_sources.append(p)
    before=[snapshot(root,missing_allowed=True) for root in ROOTS]
    observed={}
    for key,path in (('failed_host_result',H/'failed_host_result.json'),('outer_watchdog',H/'run/build.watchdog.json'),
        ('inner_stage_table',O/INNER_FAMILY/'stages.json')):
        if os.path.lexists(path):
            try: observed[key]=read(path)
            except (ValueError,OSError,KeyError,TypeError) as error: observed[key+'_parse_error']=repr(error)
    actual_stages=observed.get('inner_stage_table',{}).get('stages',[])
    if type(actual_stages) is not list: raise ValueError('actual partial stages must be a list')
    observed_inner=[]
    for stage in actual_stages:
        record=dict(stage=stage)
        if type(stage.get('label')) is str and stage['label'] in LABELS:
            raw=O/(stage['label']+'.log');watch=raw.with_suffix('.watchdog.json')
            if os.path.lexists(raw): record['complete_log']=pin(raw)
            if os.path.lexists(watch):
                record['watchdog']=pin(watch)
                try: record['actual_watchdog_fields']=read(watch)
                except (ValueError,OSError,KeyError,TypeError) as error: record['watchdog_parse_error']=repr(error)
        observed_inner.append(record)
    observed_statuses=[stage.get('status') for stage in actual_stages]
    observed_labels=[stage.get('label') for stage in actual_stages]
    actual_prefix=observed_labels==LABELS[:len(observed_labels)]
    pass_labels=[stage.get('label') for stage in actual_stages if stage.get('status')=='PASS']
    absent_success={name:not os.path.lexists(O/name) for name in
        ('seal.json','driver_result.json','raw_metadata_receipt.json','audit/result.json','audit/binary_identity.json','closeout_failure.json')}
    originals=dict(actual_root_terminal=metadata['root-terminal'],actual_metadata_writer_source=writer_pin,
        actual_root_launch_arguments=actual['actual_launch_arguments'],actual_terminal_tool_result=terminal,
        returncode=terminal['exit_code'],actual_tool_session_closed=True,record_producer='root',
        observed_after_actual_terminal_return=True,record_written_after_actual_terminal_return=True,
        original_fixed_input_expected_pins=fixed,ordered_fixed_input_unchanged_results=unchanged,
        original_fixed_input_failures=failures,complete_SOURCE_unchanged=source_ok,complete_SOURCE_error=source_error,
        dynamic_complete_SOURCE_file_count=len(freeze['complete_files']),original_prepared_metadata_check=prepared,
        original_prepared_metadata_check_error=prepared_error,actual_fixed_Source_pins=fixed_sources,
        original_host_final_input_revalidation_observed=False,
        Root_postclose_pin_checks_do_not_replace_unreached_host_input_finalpass=True,
        full_declared_physical_input_finalpass_claimed=False,
        actual_observed_partial_inner_stages=observed_inner,observed_PASS_stage_labels=pass_labels,
        observed_stage_count=len(actual_stages),observed_labels_form_original_prefix=actual_prefix,
        actual_saved_failure_metadata=observed,actual_success_closeout_files_absent=absent_success,
        successful_new_runtime_build_observed=False,all_five_original_stages_passed=False,
        whole_wall_cap_seconds=WHOLE,inner_stage_wall_cap_seconds=STAGE,rss_cap_mib=RSS,
        joint_archive_cap_bytes=ARCHIVE,history_cap_bytes=HISTORY,free_floor_bytes=FREE,
        threads=1,children_at_once=1,retries=0,original_caps_preserved=True,
        original_peak_RSS_source_line_observed=False,cleanup_performed_by_metadata_writer=False,
        separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False,
        full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR',
        full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR',
        original_executor_merged_capture_source=pin(MERGED_CAPTURE_SOURCE),
        original_executor_capture_semantics='705 subprocess.Popen stderr=subprocess.STDOUT',
        no_project_API_guard_numeric_or_build_executed_by_metadata_writer=True,
        **{key:False for key in FALSE_FIELDS})
    current=[snapshot(root,missing_allowed=True) for root in (*ROOTS,E)]
    # Reserve only metadata encoding overhead, inside the same original 2GiB.
    payload=dict(namespaces=current,originals=originals)
    reserve=64*2**20+8*len(json.dumps(payload,indent=2,allow_nan=False).encode())
    if namespace_bytes(current)+reserve+FACTORY.stat().st_size+writer_pin['identity'][4]>=ARCHIVE:
        raise ValueError('retained all-scope original 2GiB would be exceeded; no receipt written')
    copies={}
    for key,name in (('parent-stdout','actual_build_external_host_stdout.json'),
        ('parent-stderr','actual_build_external_host_stderr.txt'),
        ('root-terminal','actual_build_external_Root_tool_terminal.json')):
        copies[key]=copy_exact(paths[key],T/name)
    merged=H/'run/build.log'
    if os.path.lexists(merged):
        copies['actual-child-merged']=copy_exact(merged,T/'actual_build_child_merged_stdout_stderr.json')
    receipt=T/'failed_build_terminal_return.json'
    proof=dict(schema='ROOT_V21_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1',
        status='ACTUAL_NONZERO_BUILD_CLOSED_NO_RETRY_NO_SUCCESS_RECEIPT',
        actual_original_full_stream_copies=copies,**originals)
    write_new(receipt,proof)
    views=[snapshot(root,missing_allowed=True) for root in (*ROOTS,E)]
    for index,root in enumerate(ROOTS):
        if root!=T and views[index]!=before[index]: raise ValueError('readonly H/S/O/D changed during failure metadata capture')
    old_t=before[3];new_t=views[3]
    if any(new_t['files'].get(key)!=p for key,p in old_t['files'].items()) or any(
        new_t['symlinks'].get(key)!=p for key,p in old_t['symlinks'].items()):
        raise ValueError('all original prepared TERMINAL entries changed')
    for p in metadata.values():
        if pin(p['path'])!=p: raise ValueError('Root original real tool/streams changed')
    for value in unchanged:
        exact_pin(value['pin'])
    for p in fixed_sources: exact_pin(p)
    if source_ok: compare_source_freeze(freeze)
    if prepared is not None:
        for value in prepared['verified_original_entries']: exact_pin(value['pin'])
    manifest=dict(schema='ROOT_V21_ACTUAL_FAILED_BUILD_ALL_NAMESPACES_FULL_EOF_SHA7ID_V1',
        actual_root_terminal=metadata['root-terminal'],failed_terminal_receipt=pin(receipt),
        namespaces=views,ordered_original_fixed_input_pins=fixed,all_success_credit=False,
        actual_metadata_writer_source=writer_pin,original_sources=metadata,
        E_root_complete_snapshot_before_this_manifest_and_summary=True,
        E_root_directory_full7stable_after_metadata_append_required=False,
        E_root_append_reason='manifest, summary and future real metadata tool receipts are appended after the explicit captured snapshot',
        unchanged_namespace_roots_require_full7stable=True,
        no_project_API_or_numeric_business_called=True,
        Root_postclose_revalidation_is_not_original_host_final_input_PASS=True)
    write_new(E/failure_outputs[0],manifest)
    summary=dict(originals)
    summary.update(schema='ROOT_V21_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_SUMMARY_V1',
        status=proof['status'],namespace_manifest=pin(E/failure_outputs[0]),
        failed_terminal_receipt=pin(receipt),all_original_fixed_input_pins_unchanged=not failures,
        original_fixed_input_entry_count=len(fixed),observed_PASS_stage_labels=pass_labels,
        observed_stage_count=len(actual_stages),all_five_build_stages_passed=False,
        complete_SOURCE_unchanged=source_ok,dynamic_complete_SOURCE_file_count=len(freeze['complete_files']),
        original_PREP_SOURCE_TERMINAL_unchanged=prepared is not None and prepared['original_S_T_entries_unchanged'],
        original_PREP_OUT_four_unchanged=prepared is not None and prepared['original_PREP_OUT_four_unchanged'],
        actual_success_closeout_files_absent=absent_success)
    w=observed.get('outer_watchdog')
    if type(w) is dict:
        summary['actual_outer_watchdog_summary']={key:w.get(key) for key in ('pid','returncode','elapsed_seconds',
            'sampled_peak_rss_mib','limit_failure','own_child_only','liveness_group_cleanup','rss_cap_mib','wall_cap_seconds')}
    total=namespace_bytes([snapshot(root,missing_allowed=True) for root in (*ROOTS,E)])+FACTORY.stat().st_size+writer_pin['identity'][4]
    summary['joint_archive_bytes_before_summary']=total
    summary['joint_archive_bytes_after_summary']=0
    for _ in range(20):
        after=total+len((json.dumps(summary,indent=2,allow_nan=False)+'\n').encode())
        if summary['joint_archive_bytes_after_summary']==after: break
        summary['joint_archive_bytes_after_summary']=after
    else: raise ValueError('metadata serialization byte accounting did not settle')
    if summary['joint_archive_bytes_after_summary']>=ARCHIVE: raise ValueError('retained original all-scope 2GiB exceeded')
    write_new(E/failure_outputs[1],summary)
    actual_size=namespace_bytes([snapshot(root,missing_allowed=True) for root in (*ROOTS,E)])+FACTORY.stat().st_size+writer_pin['identity'][4]
    if actual_size!=summary['joint_archive_bytes_after_summary']: raise ValueError('actual complete final joint byte count differs')
    print(json.dumps(dict(status=summary['status'],actual_root_exit_code=terminal['exit_code'],
        observed_PASS_stage_labels=pass_labels,dynamic_SOURCE_count=len(freeze['complete_files']),
        fixed_input_entry_count=len(fixed),joint_archive_bytes=actual_size,
        namespace_manifest=pin(E/failure_outputs[0]),summary=pin(E/failure_outputs[1]),
        no_success_whole_INPUT_native_science_credit=True),allow_nan=False))

if __name__=='__main__':
    main()
