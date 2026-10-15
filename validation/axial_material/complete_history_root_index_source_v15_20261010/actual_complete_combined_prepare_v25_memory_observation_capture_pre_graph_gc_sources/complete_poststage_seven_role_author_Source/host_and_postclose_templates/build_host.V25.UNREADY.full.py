"""One normal whole five-stage combined build under the unchanged genuine guard."""
import hashlib
import math
import stat
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
FUTURE_V25_ACTUAL_Q_SHA=None
FUTURE_V25_CANONICAL_SHA=None
FUTURE_V25_DECLARATION_SHA=None
FUTURE_V25_PREP_SHA=None
FUTURE_V25_GRAPH_SHA=None
FUTURE_V25_TRACE_SHA=None
FUTURE_V25_PREP_SUMMARY_SHA=None

BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SUPPORT=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-combined-build-host-v25-memory-observation-capture-pre-graph-gc-20261010')
TARGET=Path('/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py')
TARGET_SHA=FUTURE_V25_CANONICAL_SHA
SOURCE=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-source-v25-memory-observation-capture-pre-graph-gc-20261010')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010')
TERMINAL=Path('/Users/wen/spot/validation/artifacts/axial-material-qualified-AB-sender-window-root-index-graph-trace-table-combined-terminal-v25-memory-observation-capture-pre-graph-gc-20261010')
SEAL_SHA='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
TERM_SHA='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
SOURCE_ARCHIVE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_combined_build_v25_memory_observation_capture_pre_graph_gc_sources')
DECLARATION_SHA=FUTURE_V25_DECLARATION_SHA
PREP_SHA=FUTURE_V25_PREP_SHA
INNER_FAMILY='SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_LINK_V25'
EXPECTED_LABELS=['build/link', 'metadata/objects', 'metadata/executable', 'metadata/dependencies', 'audit/audit']
EXPECTED_COMMANDS=[['/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', '-O2', '-march=native', '-ffp-contract=off', '-g', '/Users/wen/spot/src/DRAGON.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-compensated-flight-20261004/build/SPOR64_A8.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-compensated-flight-20261004/build/AXMAT_MCGFCF_COMP.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-angular-convergence-20261005/build/axmat_white_trace_model.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/SPOT1P64.o', '/Users/wen/spot/validation/artifacts/axial-material-AAA-white-trace-cold-control-paths-20261004/build/SPOF64.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/FLU2DR64.o', '/Users/wen/spot/validation/artifacts/axial-material-moment-order-build-20261006/build/FLU.o', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o', '/Users/wen/spot/lib/Darwin_arm64/libDragon.a', '/Users/wen/spot/Trivac/lib/Darwin_arm64/libTrivac.a', '/Users/wen/spot/Utilib/lib/Darwin_arm64/libUtilib.a', '/Users/wen/spot/Ganlib/lib/Darwin_arm64/libGanlib.a', '-o', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/runtime/Dragon'], ['/usr/bin/nm', '-g', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/SPOT1P64.o', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/build/SPOASM.o', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/build/FLU2DR64.o', '/Users/wen/spot/validation/artifacts/axial-material-moment-order-build-20261006/build/FLU.o'], ['/usr/bin/nm', '-g', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/runtime/Dragon'], ['/usr/bin/otool', '-L', '/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v25-memory-observation-capture-pre-graph-gc-20261010/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-spoasm-physical-abi-serial-guarded-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-memory-dedup-build-20261007/runtime/Dragon', '/Users/wen/spot/validation/artifacts/axial-material-sender-contiguous-flux-window-root-index-build-v15-20261010/runtime/Dragon'], ['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12', '/Users/wen/spot/validation/axial_material/prepare_sender_window_root_index_graph_trace_table_combined_runtime_v25_memory_observation_capture_pre_graph_gc.py', 'audit-build', '--sha256', FUTURE_V25_DECLARATION_SHA, '--prep-sha256', FUTURE_V25_PREP_SHA]]
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30

SOURCE_BINDING_STATUS='UNREADY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_UNBOUND'

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

def main():
    if SOURCE_BINDING_STATUS!='READY_V25_ACTUAL_COMPLETE_PREP_AND_SOURCE_BOUND':
        raise ValueError('UNREADY: actual new Q, complete PREP saved peer and bound Source required before any I/O')
    started=time.monotonic()
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed unprofiled nonoptimized read-only admission host required')
    import hashlib
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:
        raise ValueError('fixed normal support source required')
    spec=importlib.util.spec_from_file_location('axmat_v15_normal_readonly_admission_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    support_pin=support.pin(SUPPORT,SUPPORT_SHA)
    if any(os.environ.get(k)!='1' for k in support.THREAD_KEYS) or Path(sys.executable).resolve()!=support.PYTHON:
        raise ValueError('original single-thread Python required')
    if os.path.lexists(HOST):raise ValueError('fresh one-use whole build host required; no retry')
    if not all(p.is_dir() for p in (SOURCE,OUT,TERMINAL)):raise ValueError('actual prepared SOURCE/OUT/TERMINAL required')
    if any(os.path.lexists(OUT/p) for p in ('execution_claim.json','seal.json','driver_result.json','closeout_failure.json','raw_metadata_receipt.json','build_memory_diagnostic.jsonl','audit/binary_identity.json','audit/result.json',INNER_FAMILY+'/stages.json','runtime/Dragon')):raise ValueError('no prior build execution or build retry allowed')
    inputs=[support_pin,support.pin(TARGET,TARGET_SHA),support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA)]+[support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_inactive_audit_snapshot_consume_20261010.py'),'3b181f6366d5084fd6ccc87c1a6e7b757b706b7ba38cdf9156e1381cdb010092'),support.pin(Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/Root_actual_complete_graph_private_inactive_audit_helper_admission_v25.json'),FUTURE_V25_ACTUAL_Q_SHA)]+[support.pin(p) for p in sorted(SOURCE_ARCHIVE.rglob('*')) if p.is_file()]
    inputs += [support.pin(OUT/'declaration.json',DECLARATION_SHA),support.pin(TERMINAL/'declaration_terminal_return.json',PREP_SHA),support.pin(OUT/'input_graph.json',FUTURE_V25_GRAPH_SHA),support.pin(OUT/'input_creation_python_open_trace.json',FUTURE_V25_TRACE_SHA)]
    inputs += [support.pin(p) for root in (SOURCE,TERMINAL) for p in sorted(root.rglob('*')) if p.is_file()]
    inputs += [support.pin(BASE/'actual_complete_combined_prepare_v25_memory_observation_capture_pre_graph_gc_receipts/Root_actual_prepare_tool_terminal_return.json'),support.pin(BASE/'actual_complete_combined_prepare_v25_memory_observation_capture_pre_graph_gc_receipts/Root_actual_complete_combined_prepare_summary.json',FUTURE_V25_PREP_SUMMARY_SHA)]
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    roots=resource.history_roots([str(HOST),str(SOURCE),str(OUT),str(TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        HOST.mkdir()
        for name in ('runtime','run','COMPLETE_COMBINED_BUILD'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_COMBINED_BUILD',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),str(TARGET),'run-build','--sha256',DECLARATION_SHA,'--prep-sha256',PREP_SHA]
        runner.execute(HOST/'run','build',command,WHOLE_CAP)
        log=HOST/'run/build.log';watch_path=HOST/'run/build.watchdog.json'
        admission=json.loads(log.read_text());watch=json.loads(watch_path.read_text())
        declaration=OUT/'declaration.json';d=json.loads(declaration.read_text());memory_diagnostic_declaration(d)
        if support.pin(declaration)['sha256']!=DECLARATION_SHA:raise ValueError('immutable declaration changed')
        if d['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25_DECLARATION_V1' or d['stages']!=EXPECTED_LABELS or (d['total_wall_seconds'],d['stage_wall_seconds'],d['rss_cap_mib'],d['archive_reserve_bytes'])!=(1800,600,512,2*2**30):raise ValueError('original complete five stages and caps required')
        if set(admission)!=set(('result','actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')):raise ValueError('full whole-build return and four actual tails required')
        result=json.loads((OUT/'driver_result.json').read_text());audit=json.loads((OUT/'audit/result.json').read_text())
        if admission['result']!=result or result['classification']!='COMPLETE_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or result['error'] is not None or result['fresh_cold_AAA_required'] is not True:raise ValueError('actual complete build-only return required')
        if audit['classification']!='PASS_COMBINED_RUNTIME_LINK_IDENTITY_ONLY' or audit['binary_status']!='PASS' or audit['declaration_sha256']!=DECLARATION_SHA or audit['historical_whole_component_body']!=d['historical_whole_component_body'] or audit['actual_last_cprime_trim_component_INPUT']!=d['actual_last_cprime_trim_component_INPUT']:raise ValueError('complete original link audit required')
        if any(value[k] is not False for value in (result,audit) for k in ('native_transport_executed','mathematical_controls_newly_executed','combined_runtime_native_RSS_proved','actual_full_FLU_entry_executed','AAA_accuracy_qualified','ABA_admitted')):raise ValueError('link identity only science boundaries required')
        inner=json.loads((OUT/INNER_FAMILY/'stages.json').read_text())['stages']
        if len(inner)!=5 or [s['label'] for s in inner]!=EXPECTED_LABELS or [s['command'] for s in inner]!=EXPECTED_COMMANDS or any(s['status']!='PASS' for s in inner):raise ValueError('all exact five original supervised commands must pass once')
        inner_watches=[]
        for stage in inner:
            raw_log=OUT/(stage['label']+'.log');iw=json.loads(raw_log.with_suffix('.watchdog.json').read_text())
            if iw['command']!=stage['command'] or type(iw['returncode']) is not int or iw['returncode']!=0 or iw['limit_failure'] is not None or iw['rss_cap_mib']!=512 or not 0<=iw['sampled_peak_rss_mib']<512 or not 0<iw['wall_cap_seconds']<=stage['wall_cap_seconds']<=600 or not 0<=iw['elapsed_seconds']<iw['wall_cap_seconds'] or iw['own_child_only'] is not True or iw['liveness_group_cleanup'] is not True or support.pin(raw_log)['sha256']!=stage['log_sha256']:raise ValueError('each unchanged genuine inner stage watch required')
            inner_watches.append(iw)
        if inner_watches!=result['watchdogs'] or inner_watches[:-1]!=audit['previous_stage_watchdogs']:raise ValueError('all five watches must agree')
        raw=json.loads((OUT/'raw_metadata_receipt.json').read_text())
        if raw['files']!={label+'.log':support.pin(OUT/(label+'.log'))['sha256'] for label in EXPECTED_LABELS[:4]} or raw['before_binary_identity_gates'] is not True or raw['complete_raw_tools_and_link_stdout'] is not True:raise ValueError('complete raw metadata before all identity gates required')
        seal=json.loads((OUT/'seal.json').read_text());files={};directories=[]
        for folder,dirs,names in os.walk(OUT,followlinks=False):
            for name in dirs:
                p=Path(folder)/name
                if p.is_symlink():raise ValueError('unexpected build output symlink')
                directories.append(str(p.relative_to(OUT)))
            for name in names:
                p=Path(folder)/name
                if p.is_symlink():raise ValueError('unexpected build output symlink')
                files[str(p.relative_to(OUT))]=support.pin(p)['sha256']
        if seal['schema']!='AXMAT_SENDER_WINDOW_ROOT_INDEX_GRAPH_TRACE_TABLE_COMBINED_RUNTIME_V25_BUILD_SEAL_V1' or seal['symlinks']!={} or seal['directories']!=sorted(directories) or set(files)!=set(seal['files'])|{'seal.json'} or any(files[k]!=v for k,v in seal['files'].items()):raise ValueError('complete original OUT seal required')
        if result['corrected_runtime']!={k:support.pin(OUT/'runtime/Dragon')[k] for k in ('path','sha256')}:raise ValueError('actual built runtime identity required')
        actual_size=support.archive_bytes((SOURCE,OUT));tail_resources=admission['actual_resources']
        if admission['actual_tail_check']!='PASS' or not result['elapsed_seconds']<=admission['actual_elapsed_seconds']<WHOLE_CAP or type(admission['actual_archive_bytes']) is not int or admission['actual_archive_bytes']!=actual_size or not 0<actual_size<ARCHIVE_CAP or tail_resources['artifact_budget_bytes']!=96*2**30 or tail_resources['min_free_bytes']!=8*2**30 or tail_resources['declared_resource_roots']!=d['resource_roots'] or tail_resources['resource_scope_policy']!=d['resource_scope_policy'] or tail_resources['resource_scope_contract']!=d['resource_scope_contract'] or not set(d['resource_roots']).issubset(tail_resources['resource_roots']) or not actual_size<=tail_resources['artifact_bytes']<=96*2**30 or tail_resources['disk_free_bytes']<8*2**30:raise ValueError('all original actual post-seal budget tails required')
        resource.validate_history_roots(tail_resources['resource_roots'],support.ART)
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        diagnostic=memory_diagnostic_rows(OUT/BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path'],json.loads((OUT/'execution_claim.json').read_text())['parent_pid'],success=True)
        if diagnostic['journal_if_present']['sha256']!=seal['files'][BUILD_MEMORY_DIAGNOSTIC_CONTRACT['relative_path']]:raise ValueError('saved diagnostic matches whole OUT seal')
        value=dict(actual_build_memory_diagnostic=diagnostic,schema='AXMAT_V25_GENUINE_COMPLETE_COMBINED_BUILD_HOST_V1',status='ACTUAL_COMPLETE_COMBINED_BUILD_EXTERNAL_ROOT_REQUIRED',input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_build_stdout=support.pin(log),actual_build_seal=support.pin(OUT/'seal.json'),actual_driver_result=support.pin(OUT/'driver_result.json'),actual_inner_stages=inner,actual_inner_watchdogs=inner_watches,actual_tail_fields={k:admission[k] for k in ('actual_tail_check','actual_elapsed_seconds','actual_archive_bytes','actual_resources')},outer_command_wall_cap_seconds=WHOLE_CAP,inner_original_stage_wall_cap_seconds=STAGE_CAP,whole_combined_INPUT_admitted=False,actual_declaration=support.pin(declaration),actual_source_admission=support.pin(SOURCE/'source_admission.json'),actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,SOURCE,OUT,TERMINAL,SOURCE_ARCHIVE))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_build_stdout=support.pin(log),actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_COMPLETE_COMBINED_BUILD_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()
