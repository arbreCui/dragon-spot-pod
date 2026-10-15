'UNREADY SOURCE ONLY complete V25 Root five-stage build postclose metadata writer. Root must first bind actual Q/canonical and all required future Source values, freeze this writer in D, then record a genuine strict closed terminal before executing it. All original success and failure branches, complete streams/namespaces/inputs, caps and scientific boundaries remain required. Source supplies no actual result or qualification.'
import argparse
import ast
import hashlib
import json
import math
import os
from pathlib import Path
import stat
import time

FUTURE_V25_ACTUAL_Q_SHA=None
FUTURE_V25_CANONICAL_SHA=None
FUTURE_V25_DECLARATION_SHA=None
FUTURE_V25_PREP_SHA=None
FUTURE_V25_BUILD_HOST_SHA=None

BASE = Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
ART = Path('/Users/wen/spot/validation/artifacts')
D = BASE/'actual_complete_combined_build_v25_memory_observation_sources'
E = BASE/'actual_complete_combined_build_v25_memory_observation_receipts'
H = ART/'axial-material-complete-combined-build-host-v25-memory-observation-20261010'
S = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-memory-observation-20261010'
O = ART/'axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-20261010'
T = ART/'axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-memory-observation-20261010'
FACTORY = Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation.py')
FACTORY_SHA = FUTURE_V25_CANONICAL_SHA
HOST_SOURCE = D/'combined_build_host.py'
HOST_SHA = FUTURE_V25_BUILD_HOST_SHA
DECL_SHA = FUTURE_V25_DECLARATION_SHA
PREP_SHA = FUTURE_V25_PREP_SHA
HELPER = Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py')
HELPER_SHA = '3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'
Q = BASE/'Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'
Q_SHA = FUTURE_V25_ACTUAL_Q_SHA
MERGED_CAPTURE_SOURCE = Path('/Users/wen/spot/validation/axial_material/qualify_refined_AAA_layered_full.py')
MERGED_CAPTURE_SHA = '70516d764e05cffa6e82e780a991ff64e56b9c29bc99f3f1b18bcb0ff63195c6'
INNER_FAMILY = 'SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'
PREFIX = 'AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25'
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

BUILD_MEMORY_DIAGNOSTIC_CONTRACT = {'schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_OUTPUT_CONTRACT_V1', 'relative_path': 'build_memory_diagnostic.jsonl', 'row_schema': 'AXMAT_V25_BUILD_MEMORY_DIAGNOSTIC_ROW_V1', 'phases': ['run_build', 'declaration_admission', 'before_build_link', 'before_metadata_objects', 'before_metadata_executable', 'before_metadata_dependencies', 'run_finally'], 'points': ['declaration_enter', 'declaration_return', 'commands_constructed', 'execute_enter', 'execute_return', 'environment_enter', 'environment_return', 'complete_input_enter', 'specs1_enter', 'specs1_return', 'owned1_enter', 'owned1_return', 'current_before_enter', 'current_before_return', 'verify_graph_enter', 'verify_graph_return', 'snapshot_enter', 'snapshot_return', 'trace_digest_enter', 'trace_digest_return', 'specs2_enter', 'specs2_return', 'current_after_enter', 'current_after_return', 'owned2_enter', 'owned2_return', 'graph2_enter', 'graph2_return', 'bindings_enter', 'bindings_return', 'lengths_enter', 'lengths_return', 'complete_input_return', 'archive_resources_return', 'normal_pre_inventory'], 'max_rows': 256, 'max_line_bytes_including_newline': 4096, 'max_bytes': 1048576, 'open_flags': 'O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW', 'mode_octal': '0600', 'one_parent_descriptor': True, 'write_only': True, 'read_during_active_input_audit': False, 'last_normal_marker': 'normal_pre_inventory', 'close_before_original_OUT_inventory': True, 'no_append_after_close': True, 'ru_maxrss_semantics': 'DARWIN_RUSAGE_SELF_NATIVE_BYTES_PROCESS_HISTORICAL_HIGH_WATER_NOT_CURRENT_RSS_OR_GUARD_PEAK', 'diagnostic_runtime_dependency_provenance': 'FUTURE_ROOT_SOURCE_BIND_AND_PRELAUNCH_ENVIRONMENT_WITNESS_REQUIRED', 'actual_runtime_pin': None, 'current_RSS_qualified': False, 'whole_INPUT_build_native_or_science_qualified': False}

def memory_diagnostic_pin(path):
    path=Path(path);s=path.lstat()
    ident=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if path.is_symlink() or not stat.S_ISREG(s.st_mode) or s.st_nlink!=1:raise ValueError('ordinary single-link diagnostic required')
    bound=BUILD_MEMORY_DIAGNOSTIC_CONTRACT['max_bytes']
    if type(bound) is not int or bound!=1048576 or type(s.st_size) is not int or not 0<=s.st_size<=bound:raise ValueError('diagnostic pre-open size exceeds reserved byte bound')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        opened=os.fstat(fd);opened_ident=[opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns]
        if not stat.S_ISREG(opened.st_mode) or opened.st_nlink!=1 or opened_ident!=ident:raise ValueError('diagnostic no-follow descriptor differs from pre-open identity')
        with os.fdopen(fd,'rb',buffering=0,closefd=False) as stream:raw=stream.read(bound+1)
        if len(raw)>bound or len(raw)!=ident[4]:raise ValueError('diagnostic bounded full EOF bytes differ from exact stat size')
        finished=os.fstat(fd);finished_ident=[finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns]
        if finished_ident!=ident:raise ValueError('diagnostic descriptor changed during bounded full EOF pin')
    finally:
        os.close(fd)
    s=path.lstat();after=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    if after!=ident:raise ValueError('full EOF diagnostic changed during pin')
    return dict(path=str(path),sha256=hashlib.sha256(raw).hexdigest(),size_bytes=ident[4],identity=ident)

def memory_diagnostic_rows(path,expected_pid=None,success=False):
    contract=BUILD_MEMORY_DIAGNOSTIC_CONTRACT;path=Path(path)
    if not os.path.lexists(path):
        if success:raise ValueError('successful build requires complete saved diagnostic')
        return dict(parse_status='ABSENT',journal_if_present=None,saved_complete_rows=[],trailing_fragment=None,final_marker_observed=False,diagnostic_credit=False)
    before=memory_diagnostic_pin(path)
    output=dict(parse_status='INVALID_DIAGNOSTIC',journal_if_present=before,saved_complete_rows=[],trailing_fragment=None,final_marker_observed=False,diagnostic_credit=False,fsync_or_close_proved_by_rows_alone=False,ru_maxrss_is_original_guard_peak=False)
    try:
        if type(before['size_bytes']) is not int or not 0<=before['size_bytes']<=contract['max_bytes']:raise ValueError('diagnostic exceeds reserved byte bound')
        current=path.lstat();current_ident=[current.st_dev,current.st_ino,current.st_mode,current.st_nlink,current.st_size,current.st_mtime_ns,current.st_ctime_ns]
        if path.is_symlink() or not stat.S_ISREG(current.st_mode) or current.st_nlink!=1 or current_ident!=before['identity']:raise ValueError('diagnostic pre-open parser identity changed')
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
        try:
            opened=os.fstat(fd);opened_ident=[opened.st_dev,opened.st_ino,opened.st_mode,opened.st_nlink,opened.st_size,opened.st_mtime_ns,opened.st_ctime_ns]
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink!=1 or opened_ident!=before['identity']:raise ValueError('diagnostic parser no-follow descriptor identity changed')
            with os.fdopen(fd,'rb',buffering=0,closefd=False) as stream:raw=stream.read(contract['max_bytes']+1)
            if len(raw)>contract['max_bytes'] or len(raw)!=before['size_bytes']:raise ValueError('diagnostic bounded read differs from full pin')
            finished=os.fstat(fd);finished_ident=[finished.st_dev,finished.st_ino,finished.st_mode,finished.st_nlink,finished.st_size,finished.st_mtime_ns,finished.st_ctime_ns]
            if finished_ident!=before['identity']:raise ValueError('diagnostic parser descriptor changed during read')
        finally:
            os.close(fd)
        current=path.lstat();current_ident=[current.st_dev,current.st_ino,current.st_mode,current.st_nlink,current.st_size,current.st_mtime_ns,current.st_ctime_ns]
        if current_ident!=before['identity'] or hashlib.sha256(raw).hexdigest()!=before['sha256']:raise ValueError('diagnostic parser full SHA or exact identity changed')
        pieces=raw.split(b'\n');fragment=pieces.pop()
        if fragment:
            output['trailing_fragment']=dict(size_bytes=len(fragment),sha256=hashlib.sha256(fragment).hexdigest())
        if len(pieces)>contract['max_rows']:raise ValueError('diagnostic row count exceeds bound')
        rows=output['saved_complete_rows'];last_time=None;last_high_water=None;parent=expected_pid
        keys={'schema','sequence_exact_int','pid_exact_int','phase_fixed_enum','point_fixed_enum','monotonic_seconds_finite','self_ru_maxrss_native_bytes_exact_int','ru_maxrss_semantics'}
        def pairs(items):
            out={}
            for key,value in items:
                if key in out:raise ValueError('duplicate diagnostic JSON key')
                out[key]=value
            return out
        def bad_constant(value):raise ValueError('nonfinite diagnostic JSON constant '+value)
        for index,line in enumerate(pieces):
            if len(line)+1>contract['max_line_bytes_including_newline']:raise ValueError('diagnostic line exceeds bound')
            row=json.loads(line.decode('ascii'),object_pairs_hook=pairs,parse_constant=bad_constant)
            if type(row) is not dict or set(row)!=keys:raise ValueError('exact eight diagnostic fields required')
            if row['schema']!=contract['row_schema'] or row['ru_maxrss_semantics']!=contract['ru_maxrss_semantics']:raise ValueError('diagnostic schema/native-byte semantics changed')
            if type(row['sequence_exact_int']) is not int or row['sequence_exact_int']!=index:raise ValueError('strict consecutive diagnostic sequence')
            pid=row['pid_exact_int'];peak=row['self_ru_maxrss_native_bytes_exact_int'];clock=row['monotonic_seconds_finite']
            if type(pid) is not int or pid<=0 or type(peak) is not int or peak<0 or type(clock) not in (int,float) or not math.isfinite(clock):raise ValueError('strict PID/high-water integers and finite clock')
            if parent is None:parent=pid
            if type(parent) is not int or parent<=0 or pid!=parent:raise ValueError('single actual canonical parent PID required')
            if row['phase_fixed_enum'] not in contract['phases'] or row['point_fixed_enum'] not in contract['points']:raise ValueError('fixed phase/point required')
            if last_time is not None and (clock<last_time or peak<last_high_water):raise ValueError('diagnostic clock/high-water decreased')
            rows.append(row);last_time=clock;last_high_water=peak
        if fragment and len(fragment)>=contract['max_line_bytes_including_newline']:raise ValueError('trailing fragment exceeds line bound')
        output['parse_status']='PARTIAL_TRAILING_FRAGMENT' if fragment else 'COMPLETE_LINES'
        output['final_marker_observed']=bool(rows and rows[-1]['phase_fixed_enum']=='run_build' and rows[-1]['point_fixed_enum']=='normal_pre_inventory')
        if success and (fragment or not rows or not output['final_marker_observed'] or any(r['point_fixed_enum']=='normal_pre_inventory' for r in rows[:-1])):
            raise ValueError('successful diagnostic requires unique final pre-inventory marker and no fragment')
    except (ValueError, TypeError, KeyError, OverflowError) as error:
        output['parse_status']='INVALID_DIAGNOSTIC';output['validation_error']=repr(error)
        if success:raise
    after=memory_diagnostic_pin(path)
    if after!=before:raise ValueError('saved diagnostic changed during bounded postclose read')
    return output

def memory_diagnostic_declaration(d):
    expected=BUILD_MEMORY_DIAGNOSTIC_CONTRACT
    actual=d.get('build_memory_diagnostic_output_contract')
    if json.dumps(actual,sort_keys=True,allow_nan=False)!=json.dumps(expected,sort_keys=True,allow_nan=False):
        raise ValueError('exact declared write-only bounded output diagnostic contract required')
    forecast=d['complete_archive_forecast']
    fields=('copied_SOURCE_metadata_bound','trim_whole_component_metadata_and_trace_bound','full_graph_and_creation_trace_bound','combined_runtime_and_link_transient_bound','complete_raw_tools_and_closeout_bound','diagnostic_max_bytes','total_bound')
    if any(type(forecast[k]) is not int or forecast[k]<0 for k in fields):
        raise ValueError('exact integer complete forecast and diagnostic reservation required')
    if forecast['diagnostic_max_bytes']!=expected['max_bytes'] or forecast['total_bound']!=sum(forecast[k] for k in fields[:-1]) or forecast['total_bound']>=2*2**30:
        raise ValueError('all original complete forecast components plus diagnostic remain below original 2GiB')
    return actual

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
    if freeze['schema']!='ROOT_V25_COMPLETE_ACTUAL_BUILD_SOURCE_FREEZE_V1' or freeze['source_root']!=str(D):
        raise ValueError('fixed V25 SOURCE freeze required')
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

def finite_number(value,lower,upper):
    return type(value) in (int,float) and math.isfinite(value) and lower<=value<upper

def watch_ok(w,command,wall):
    if (w['command']!=command or type(w['returncode']) is not int or w['returncode']!=0
        or w['limit_failure'] is not None or w['rss_cap_mib']!=RSS
        or not finite_number(w['sampled_peak_rss_mib'],0,RSS)
        or not finite_number(w['wall_cap_seconds'],0,wall+1) or not 0<w['wall_cap_seconds']<=wall
        or not finite_number(w['elapsed_seconds'],0,w['wall_cap_seconds'])
        or w['own_child_only'] is not True or w['liveness_group_cleanup'] is not True):
        raise ValueError('actual bounded unchanged command/watch required')

def expected_commands(d):
    # Exact original canonical stage_commands Source, with its fixed V25 constants.
    return [d['production_link_command'],['/usr/bin/nm','-g',*d['actual_production_objects']],
        ['/usr/bin/nm','-g',str(O/'runtime/Dragon')],
        ['/usr/bin/otool','-L',str(O/'runtime/Dragon'),
         str(ART/'axial-material-rank1-factor-cache-build-20261007/runtime/Dragon'),
         str(ART/'axial-material-spoasm-physical-abi-serial-guarded-build-20261007/runtime/Dragon'),
         str(ART/'axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon'),
         str(ART/'axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/runtime/Dragon')],
        [d['python_command'],str(FACTORY),'audit-build','--sha256',DECL_SHA,'--prep-sha256',PREP_SHA]]

def success_checks(root_record,terminal,prelaunch,fixed_pins):
    if terminal['exit_code']!=0: raise ValueError('actual successful Root integer EXIT0 required')
    if any(pin(path)['sha256']!=sha for path,sha in ((FACTORY,FACTORY_SHA),(HOST_SOURCE,HOST_SHA),
            (HELPER,HELPER_SHA),(Q,Q_SHA),(MERGED_CAPTURE_SOURCE,MERGED_CAPTURE_SHA),
            (O/'declaration.json',DECL_SHA),(T/'declaration_terminal_return.json',PREP_SHA))):
        raise ValueError('fixed complete Source/helper/Q/PREP identity differs')
    h=read(H/'result.json');d=read(O/'declaration.json');watch=read(H/'run/build.watchdog.json')
    body=read(H/'run/build.log');result=read(O/'driver_result.json');audit=read(O/'audit/result.json')
    if h['schema']!='AXMAT_V25_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1' or h['status']!='ACTUAL_COMPLETE_COMBINED_BUILD_EXTERNAL_ROOT_REQUIRED':
        raise ValueError('genuine normal complete build host required')
    if os.path.lexists(H/'failed_host_result.json') or os.path.lexists(O/'closeout_failure.json'):
        raise ValueError('actual host/post-seal failure prevents success')
    if (h['whole_wall_cap_seconds'],h['stage_wall_cap_seconds'],h['rss_cap_mib'],h['archive_cap_bytes'],
            h['outer_command_wall_cap_seconds'],h['inner_original_stage_wall_cap_seconds'],
            h['threads'],h['children_at_once'],h['retries'])!=(WHOLE,STAGE,RSS,ARCHIVE,WHOLE,STAGE,1,1,0):
        raise ValueError('all original whole/stage/resource/thread/child/retry caps required')
    if h['profile_used'] is not False or h['supervisor_class_or_MRO_modified'] is not False:
        raise ValueError('unmodified genuine supervisor required')
    if (d['schema']!=PREFIX+'_DECLARATION_V1' or d['stages']!=LABELS or
        (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'],
            d['artifact_budget_bytes'],d['min_free_bytes'],d['threads'],d['numeric_children_at_once'],d['retries'])
        !=(WHOLE,STAGE,RSS,ARCHIVE,HISTORY,FREE,1,1,0)):
        raise ValueError('complete original declaration scope/caps required')
    memory_diagnostic_declaration(d)
    command=[d['python_command'],str(FACTORY),'run-build','--sha256',DECL_SHA,'--prep-sha256',PREP_SHA]
    if h['actual_canonical_command']!=command or h['watchdog']!=watch or h['actual_watchdog']!=pin(H/'run/build.watchdog.json'):
        raise ValueError('actual canonical outer command/watch mismatch')
    watch_ok(watch,command,WHOLE)
    if len(h['stage_records'])!=1 or h['stage_records'][0]['status']!='PASS' or not finite_number(h['whole_seconds'],0,WHOLE):
        raise ValueError('one genuine original whole PASS required')
    if set(body)!={'result',*TAIL_FIELDS} or body['result']!=result:
        raise ValueError('complete actual canonical merged return required')
    if result['classification']!='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or result['error'] is not None or result['fresh_cold_AAA_required'] is not True:
        raise ValueError('actual complete link identity only result required')
    if (audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS'
        or audit['declaration_sha256']!=DECL_SHA
        or audit['historical_whole_component_body']!=d['historical_whole_component_body']
        or audit['actual_last_cprime_trim_component_INPUT']!=d['actual_last_cprime_trim_component_INPUT']):
        raise ValueError('complete actual binary audit identity required')
    original_false=('native_transport_executed','mathematical_controls_newly_executed',
        'combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')
    if any(value[k] is not False for value in (result,audit) for k in original_false):
        raise ValueError('actual build cannot grant native/science admission')
    if any(h[k] is not False for k in ('whole_combined_INPUT_admitted','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted')):
        raise ValueError('host scientific boundary changed')
    stages=read(O/INNER_FAMILY/'stages.json')['stages'];commands=expected_commands(d)
    literal_commands=[]
    for node in ast.parse(HOST_SOURCE.read_bytes()).body:
        if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='EXPECTED_COMMANDS' for target in node.targets):
            literal_commands.append(ast.literal_eval(node.value))
    if literal_commands!=[commands]: raise ValueError('original fixed host five complete commands differ')
    if len(stages)!=5 or [q['label'] for q in stages]!=LABELS or [q['command'] for q in stages]!=commands or any(q['status']!='PASS' for q in stages):
        raise ValueError('all exact five original stages PASS required')
    watches=[]
    for q in stages:
        if not finite_number(q['wall_cap_seconds'],0,STAGE+1) or not 0<q['wall_cap_seconds']<=STAGE:
            raise ValueError('original stage declaration cap required')
        log=O/(q['label']+'.log');w=read(log.with_suffix('.watchdog.json'));watch_ok(w,q['command'],q['wall_cap_seconds'])
        if pin(log)['sha256']!=q['log_sha256']: raise ValueError('complete original stage log differs')
        watches.append(w)
    if watches!=result['watchdogs'] or watches[:-1]!=audit['previous_stage_watchdogs'] or stages!=h['actual_inner_stages'] or watches!=h['actual_inner_watchdogs']:
        raise ValueError('all five actual watches and stage records disagree')
    raw=read(O/'raw_metadata_receipt.json')
    if (raw['files']!={label+'.log':pin(O/(label+'.log'))['sha256'] for label in LABELS[:4]}
        or raw['before_binary_identity_gates'] is not True or raw['complete_raw_tools_and_link_stdout'] is not True):
        raise ValueError('all four raw tools retained before identity gates required')
    seal=read(O/'seal.json');outview=snapshot(O);actual=compact_inventory(outview)
    if (seal['schema']!=PREFIX+'_BUILD_SEAL_V1' or actual['symlinks']!={} or seal['symlinks']!={}
        or actual['directories']!=seal['directories'] or set(actual['files'])!=set(seal['files'])|{'seal.json'}
        or any(actual['files'][k]!=v for k,v in seal['files'].items())):
        raise ValueError('whole OUT files/dirs/raw/watch/runtime exact seal required')
    diagnostic=memory_diagnostic_rows(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],read(O/'execution_claim.json')['parent_pid'],success=True)
    if h['actual_build_memory_diagnostic']!=diagnostic or diagnostic['journal_if_present']['sha256']!=seal['files'][BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']]:raise ValueError('actual host/full OUT sealed diagnostic coupling')
    if result['corrected_runtime']!=short(O/'runtime/Dragon'): raise ValueError('full runtime identity differs')
    if any(h[field]!=pin(path) for field,path in (
        ('actual_build_stdout',H/'run/build.log'),('actual_build_seal',O/'seal.json'),
        ('actual_driver_result',O/'driver_result.json'),('actual_declaration',O/'declaration.json'),
        ('actual_source_admission',S/'source_admission.json'))):
        raise ValueError('all host actual output pins disagree')
    if compact_inventory(snapshot(S))!=d['source_inventory']: raise ValueError('whole prepared SOURCE inventory differs')
    actual_size=namespace_bytes([snapshot(S),outview]);tails={k:body[k] for k in TAIL_FIELDS};r=tails['actual_resources']
    if (tails!=h['actual_tail_fields'] or tails['actual_tail_check']!='PASS'
        or not finite_number(tails['actual_elapsed_seconds'],result['elapsed_seconds'],WHOLE)
        or type(tails['actual_archive_bytes']) is not int or tails['actual_archive_bytes']!=actual_size
        or not 0<actual_size<ARCHIVE or r['artifact_budget_bytes']!=HISTORY or r['min_free_bytes']!=FREE
        or r['resource_scope_policy']!=HISTORY_POLICY or r['resource_scope_contract']!=d['resource_scope_contract']
        or r['declared_resource_roots']!=d['resource_roots'] or not set(d['resource_roots']).issubset(r['resource_roots'])
        or not actual_size<=r['artifact_bytes']<=HISTORY or r['disk_free_bytes']<FREE):
        raise ValueError('all original actual four post-seal tails required')
    for resources in (h['resources_before'],h['resources_after']):
        if resources['artifact_budget_bytes']!=HISTORY or resources['min_free_bytes']!=FREE or resources['resource_scope_policy']!=HISTORY_POLICY or resources['artifact_bytes']>HISTORY or resources['disk_free_bytes']<FREE:
            raise ValueError('genuine saved original host resource bounds required')
    original=h['input_sources']+[h['original_helper'],h['resource_factory']]
    if original!=fixed_pins: raise ValueError('original ordered fixed inputs including repeats differ')
    for q in original: exact_pin(q)
    physical=[]
    for path,sha in d['files'].items():
        q=pin(path)
        if q['sha256']!=sha: raise ValueError('complete declared physical input SHA differs: '+path)
        physical.append(q)
    return dict(host=h,declaration=d,result=result,audit=audit,body=body,command=command,
        stages=stages,watches=watches,outer_watch=watch,tails=tails,
        full_declared_physical_input_postclose_pins=physical,
        full_declared_physical_input_prelaunch_7ID_claimed=False)

SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'

def main():
    if SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND':
        raise ValueError('UNREADY: actual new Q, complete PREP saved peer and bound Source required before any I/O')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',required=True,choices=('failure-only','success-if-complete'))
    parser.add_argument('--writer-sha256',required=True)
    for key in ('root-terminal','source-freeze','prelaunch-pins','parent-stdout','parent-stderr'):
        parser.add_argument('--'+key,required=True)
        parser.add_argument('--'+key+'-sha256',required=True)
    args=parser.parse_args()
    writer_pin=pin(Path(__file__).absolute())
    if writer_pin['sha256']!=args.writer_sha256: raise ValueError('actual reviewed metadata writer SOURCE required')
    paths={key:Path(getattr(args,key.replace('-','_'))) for key in ('root-terminal','source-freeze','prelaunch-pins','parent-stdout','parent-stderr')}
    expected={
        'root-terminal':E/'Root_actual_build_tool_terminal_return.json',
        'source-freeze':E/'Root_prelaunch_complete_build_source_freeze.json',
        'prelaunch-pins':E/'Root_final_prelaunch_source_input_and_reserve_check.json',
        'parent-stdout':E/'parent_stdout.log','parent-stderr':E/'parent_stderr.log'}
    if paths!=expected: raise ValueError('fixed Root original receipt/stream paths required')
    ordinary(E,directory=True);ordinary(T,directory=True)
    if any(os.path.lexists(E/name) for name in OUT_NAMES) or any(os.path.lexists(T/name) for name in T_NAMES):
        raise ValueError('fresh one-use metadata writer; no receipt retry or overwrite')
    metadata={}
    for key,path in paths.items():
        sha=getattr(args,key.replace('-','_')+'_sha256')
        if pin(path)['sha256']!=sha: raise ValueError('Root supplied stream/metadata SHA differs')
        metadata[key]=pin(path)
    actual=bound_read(paths['root-terminal'],args.root_terminal_sha256)
    terminal=typed_terminal(actual)
    if args.mode=='failure-only' and terminal['exit_code']==0:
        raise ValueError('failure-only writer refuses all Root EXIT0 and any success receipt')
    freeze=bound_read(paths['source-freeze'],args.source_freeze_sha256)
    prelaunch=bound_read(paths['prelaunch-pins'],args.prelaunch_pins_sha256)
    fixed=prelaunch['fixed_input_pins']
    if type(fixed) is not list: raise ValueError('ordered original fixed_input_pins list required')
    unchanged=[];pin_failures=[]
    for index,q in enumerate(fixed):
        try: unchanged.append(dict(index=index,pin=exact_pin(q)))
        except (ValueError,OSError) as error: pin_failures.append(dict(index=index,expected=q,error=repr(error)))
    source_ok=False;source_error=None
    try: compare_source_freeze(freeze);source_ok=True
    except (ValueError,OSError,KeyError) as error: source_error=repr(error)
    checks=None;errors=[]
    if pin_failures: errors.append('original fixed inputs differ; see exact indexed failures')
    if not source_ok: errors.append('complete frozen SOURCE differs: '+str(source_error))
    if args.mode=='success-if-complete' and terminal['exit_code']==0 and not errors:
        try:
            checks=success_checks(actual,terminal,prelaunch,fixed)
            parent=read(paths['parent-stdout'])
            if parent!={'status':checks['host']['status'],'actual_host_result':pin(H/'result.json'),
                'actual_build_stdout':pin(H/'run/build.log'),'actual_external_Root_terminal_required':True}:
                raise ValueError('real whole external host stdout differs')
            if metadata['parent-stderr']['identity'][4]!=0: raise ValueError('actual successful external host stderr must be empty')
        except (ValueError,OSError,KeyError,TypeError) as error:
            errors.append(repr(error));checks=None
    elif terminal['exit_code']!=0:
        errors.append('actual Root nonzero terminal '+str(terminal['exit_code']))
    before=[snapshot(root,missing_allowed=checks is None) for root in ROOTS]
    # These copies retain actual separate Root launcher streams and the original
    # canonical child MERGED stream. No independent child-stderr facts are invented.
    copies={}
    for key,name in (('parent-stdout','actual_build_external_host_stdout.json'),
        ('parent-stderr','actual_build_external_host_stderr.txt'),
        ('root-terminal','actual_build_external_Root_tool_terminal.json')):
        copies[key]=copy_exact(paths[key],T/name)
    merged=H/'run/build.log'
    if os.path.lexists(merged):
        copies['actual-child-merged']=copy_exact(merged,T/'actual_build_child_merged_stdout_stderr.json')
    proof=dict(record_producer='root',actual_tool_terminal_return_observed=True,
        record_written_after_actual_terminal_return=True,returncode=terminal['exit_code'],
        actual_tool_result=terminal,actual_root_host_launchargs=actual['actual_launch_arguments'],
        actual_root_tool_record=copies['root-terminal'],actual_root_host_stdout=copies['parent-stdout'],
        actual_root_host_stderr=copies['parent-stderr'],actual_child_merged_output=copies.get('actual-child-merged'),
        full_stdout_scope='ACTUAL_CANONICAL_CHILD_MERGED_STDOUT_STDERR',
        full_stderr_scope='ACTUAL_EXTERNAL_ROOT_HOST_STDERR',
        separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False,
        original_executor_merged_capture_source=pin(MERGED_CAPTURE_SOURCE),
        original_executor_capture_semantics='705 subprocess.Popen stderr=subprocess.STDOUT',
        observed_at_unix=time.time(),source_only_writer_does_not_execute_project_API=True,
        actual_metadata_writer_source=writer_pin,
        whole_wall_cap_seconds=WHOLE,inner_stage_wall_cap_seconds=STAGE,rss_cap_mib=RSS,
        joint_archive_cap_bytes=ARCHIVE,history_cap_bytes=HISTORY,free_floor_bytes=FREE,
        threads=1,children_at_once=1,retries=0,cleanup_performed=False,
        **{key:False for key in FALSE_FIELDS})
    if checks is not None:
        proof.update(schema=TERMINAL_SCHEMA,successful_new_runtime_build_observed=True,
            source=short(FACTORY),command=checks['command'],declaration=short(O/'declaration.json'),
            prep_terminal_evidence=short(T/'declaration_terminal_return.json'),build_seal=short(O/'seal.json'),
            full_stdout=short(T/'actual_build_child_merged_stdout_stderr.json'),
            full_stderr=short(T/'actual_build_external_host_stderr.txt'),**checks['tails'])
        receipt=T/'terminal_return.json'
        manifest_name=OUT_NAMES[0];summary_name=OUT_NAMES[1]
    else:
        proof.update(schema='ROOT_V25_ACTUAL_FAILED_COMPLETE_COMBINED_BUILD_TERMINAL_V1',
            status='ACTUAL_NONZERO_BUILD_NO_RETRY' if terminal['exit_code']!=0 else 'ACTUAL_ROOT_EXIT0_METADATA_CHECK_FAILED_NO_SUCCESS_RECEIPT',
            successful_new_runtime_build_observed=False,metadata_check_errors=errors,
            original_fixed_input_final_revalidation_reached_by_this_writer=True,
            original_host_final_input_revalidation_observed=False,
            Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass=True,
            all_original_fixed_inputs_unchanged=not pin_failures,
            full_declared_physical_input_finalpass_claimed=False)
        receipt=T/'failed_build_terminal_return.json'
        manifest_name=OUT_NAMES[2];summary_name=OUT_NAMES[3]
    # The future metadata write cost is kept inside the original joint 2GiB.
    current=[snapshot(root,missing_allowed=checks is None) for root in (*ROOTS,E)]
    anticipated=len((json.dumps(proof,indent=2,allow_nan=False)+'\n').encode())
    metadata_content=dict(namespaces=current,proof=proof,fixed=fixed,unchanged=unchanged,pin_failures=pin_failures,
        physical=[] if checks is None else checks['full_declared_physical_input_postclose_pins'])
    anticipated_metadata_bound=64*2**20+8*len(json.dumps(metadata_content,indent=2,allow_nan=False).encode())
    if namespace_bytes(current)+anticipated+anticipated_metadata_bound+FACTORY.stat().st_size+Path(__file__).stat().st_size>=ARCHIVE:
        raise ValueError('actual retained joint archive already exceeds original 2GiB; success not written')
    write_new(receipt,proof)
    views=[snapshot(root,missing_allowed=checks is None) for root in (*ROOTS,E)]
    if any(a!=b for root,a,b in zip(ROOTS,before,views) if root!=T):
        raise ValueError('unchanged SOURCE/OUT/HOST/D changed during metadata capture')
    old_t=before[3];new_t=views[3]
    if any(new_t['files'].get(key)!=q for key,q in old_t['files'].items()) or any(
        new_t['symlinks'].get(key)!=q for key,q in old_t['symlinks'].items()):
        raise ValueError('all original prepared TERMINAL entries must remain exact')
    if pin(T/'declaration_terminal_return.json')['sha256']!=PREP_SHA:
        raise ValueError('immutable actual PREP receipt changed')
    if any(pin(q['path'])!=q for q in metadata.values()): raise ValueError('original Root actual streams/metadata changed')
    manifest=dict(schema='ROOT_V25_ACTUAL_COMPLETE_BUILD_POSTCLOSE_FINITE_NAMESPACES_V1',
        mode='SUCCESSFUL_COMPLETE_BUILD_LINK_IDENTITY_METADATA_ONLY' if checks is not None else 'FAILED_BUILD_SAVED_METADATA_ONLY',
        actual_metadata_writer_source=writer_pin,
        actual_Root_terminal=metadata['root-terminal'],namespaces=views,
        final_E_root_directory_identity_stability_claimed=False,
        E_root_reason='manifest/summary and later real metadata tool receipts are new entries, snapshot is explicitly before those appends',
        complete_SOURCE_freeze=metadata['source-freeze'],original_prelaunch_check=metadata['prelaunch-pins'],
        ordered_original_fixed_input_expected_pins=fixed,unchanged_ordered_original_fixed_input_results=unchanged,
        original_fixed_input_failures=pin_failures,complete_SOURCE_unchanged=source_ok,complete_SOURCE_error=source_error,
        full_declared_physical_input_postclose_pins=[] if checks is None else checks['full_declared_physical_input_postclose_pins'],
        full_declared_physical_input_prelaunch_7ID_claimed=False,
        full_declared_physical_input_finalpass_claimed=checks is not None,
        exact_formal_terminal=pin(receipt),all_saved_files_full_EOF_SHA7ID=True,
        no_business_or_numeric_API_called_by_writer=True,no_whole_INPUT_native_science_credit=True)
    write_new(E/manifest_name,manifest)
    diagnostic=memory_diagnostic_rows(O/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],success=False)
    summary=dict(actual_build_memory_diagnostic=diagnostic,schema='ROOT_V25_ACTUAL_COMPLETE_COMBINED_BUILD_POSTCLOSE_SUMMARY_V1',
        status='ACTUAL_COMPLETE_FIVE_STAGE_LINK_IDENTITY_BUILD_EXIT0_CLOSED_ONLY' if checks is not None else proof['status'],
        actual_Root_terminal=metadata['root-terminal'],actual_terminal_exit_code=terminal['exit_code'],
        actual_tool_session_closed=True,formal_build_terminal=pin(receipt),namespace_manifest=pin(E/manifest_name),
        all_original_fixed_inputs_unchanged=not pin_failures,original_fixed_input_entry_count=len(fixed),
        complete_SOURCE_unchanged=source_ok,full_SOURCE_file_count=len(freeze['complete_files']),
        original_five_build_stages_executed=checks is not None,all_five_build_stages_passed=checks is not None,
        completed_inner_stage_labels=[] if checks is None else LABELS,
        metadata_check_errors=errors,original_caps_preserved=True,whole_wall_cap_seconds=WHOLE,
        inner_stage_wall_cap_seconds=STAGE,rss_cap_mib=RSS,joint_archive_cap_bytes=ARCHIVE,
        history_cap_bytes=HISTORY,free_floor_bytes=FREE,threads=1,children_at_once=1,retries=0,
        separate_child_stderr_captured=False,independent_child_stderr_empty_verified=False,
        actual_original_guard_or_numeric_API_called=False,
        independent_raw_binary_audit_API_reexecuted=False,
        metadata_writer_does_not_run_API=True,cleanup_performed=False,**{key:False for key in FALSE_FIELDS})
    if checks is not None:
        summary.update(actual_host_result=pin(H/'result.json'),actual_build_seal=pin(O/'seal.json'),
            actual_driver_result=pin(O/'driver_result.json'),actual_binary_identity=pin(O/'audit/binary_identity.json'),
            actual_audit_result=pin(O/'audit/result.json'),actual_runtime=pin(O/'runtime/Dragon'),
            actual_inner_stages=checks['stages'],actual_inner_watchdogs=checks['watches'],
            actual_outer_watchdog=checks['outer_watch'],whole_seconds=checks['host']['whole_seconds'],
            canonical_child_seconds=checks['outer_watch']['elapsed_seconds'],
            sampled_canonical_child_peak_rss_mib=checks['outer_watch']['sampled_peak_rss_mib'],
            native_RSS_qualified=False,actual_tail_fields=checks['tails'])
    else:
        # Partial records are observations, not substituted for exact five PASS.
        summary['original_host_final_input_revalidation_observed']=False
        summary['Root_postclose_revalidation_does_not_replace_unreached_host_input_finalpass']=True
        summary['full_declared_physical_input_finalpass_claimed']=False
        stage_path=O/INNER_FAMILY/'stages.json'
        if os.path.lexists(stage_path):
            try:
                partial=read(stage_path)['stages']
                summary['observed_partial_inner_stages']=partial
                summary['observed_PASS_inner_stage_labels']=[value['label'] for value in partial if value['status']=='PASS']
                summary['observed_inner_stage_count']=len(partial)
            except (ValueError,OSError,KeyError,TypeError) as error:
                summary['actual_partial_stage_metadata_parse_error']=repr(error)
        outer_path=H/'run/build.watchdog.json'
        if os.path.lexists(outer_path):
            try:
                partial_watch=read(outer_path)
                summary['observed_outer_watchdog_fields']={key:partial_watch[key] for key in (
                    'returncode','elapsed_seconds','sampled_peak_rss_mib','limit_failure',
                    'own_child_only','liveness_group_cleanup','rss_cap_mib','wall_cap_seconds')}
            except (ValueError,OSError,KeyError,TypeError) as error:
                summary['actual_outer_watchdog_metadata_parse_error']=repr(error)
        for key,path in (('actual_failed_host_result',H/'failed_host_result.json'),
            ('actual_outer_watchdog',H/'run/build.watchdog.json'),
            ('actual_partial_inner_stage_records',O/INNER_FAMILY/'stages.json'),
            ('actual_driver_result_if_present',O/'driver_result.json'),
            ('actual_build_seal_if_present',O/'seal.json')):
            if os.path.lexists(path): summary[key]=pin(path)
    saved=[snapshot(root,missing_allowed=checks is None) for root in (*ROOTS,E)]
    total=namespace_bytes(saved)+FACTORY.stat().st_size+Path(__file__).stat().st_size
    summary['joint_archive_bytes_before_summary']=total
    summary['joint_archive_bytes_after_summary']=0
    # Fixed point is only byte accounting of this metadata serialization.
    for _ in range(20):
        size=len((json.dumps(summary,indent=2,allow_nan=False)+'\n').encode())
        after=total+size
        if summary['joint_archive_bytes_after_summary']==after: break
        summary['joint_archive_bytes_after_summary']=after
    else: raise ValueError('metadata byte-accounting did not settle')
    if summary['joint_archive_bytes_after_summary']>=ARCHIVE: raise ValueError('complete retained joint 2GiB exceeded')
    write_new(E/summary_name,summary)
    final=[snapshot(root,missing_allowed=checks is None) for root in (*ROOTS,E)]
    if namespace_bytes(final)+FACTORY.stat().st_size+Path(__file__).stat().st_size!=summary['joint_archive_bytes_after_summary']:
        raise ValueError('complete actual final joint byte accounting differs')
    print(json.dumps(dict(status=summary['status'],actual_tool_exit_code=terminal['exit_code'],
        namespace_manifest=pin(E/manifest_name),summary=pin(E/summary_name),
        no_whole_INPUT_native_science_credit=True),allow_nan=False))

if __name__=='__main__':
    main()
