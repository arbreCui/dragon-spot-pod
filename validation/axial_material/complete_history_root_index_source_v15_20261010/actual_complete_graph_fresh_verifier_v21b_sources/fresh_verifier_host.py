"""UNREADY complete current graph fresh verifier, unchanged genuine guard."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
import gzip
import hashlib
import math
import stat
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SUPPORT=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
HOST=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-host-v21b-20261010')
OUT=Path('/Users/wen/spot/validation/artifacts/axial-material-complete-graph-fresh-verifier-v21b-20261010')
SOURCE_ARCHIVE=BASE/'actual_complete_graph_fresh_verifier_v21b_sources'
RECEIPTS=BASE/'actual_complete_graph_fresh_verifier_v21b_receipts'
TARGET=SOURCE_ARCHIVE/'fresh_verifier_controls.py'
TARGET_SHA='895c889569507f2b5e28ee1da6efc6c91bbdd30cd05338dd6e039d9591e72f84'
SOURCE_STATUS='READY_SOURCE_BOUND_BY_ROOT'
BOUND_HELPER_PIN={'path': '/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_private_verifier_trace_consume_20261010.py', 'sha256': 'dc01d8cf4478f9dc918ecb828acf7d79a50fb93422bfcffe165df38978ede6a7', 'identity': [16777229, 49380106, 33188, 1, 147870, 1791589379138539325, 1791589879966481802]}
INSTALL_WITNESS_PIN={'path': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v21_receipts/Root_actual_helper_SOURCE_install_tool_return_exact_integer.json', 'sha256': 'f8e83e8ca68397f30657ed5a8fc5b0f2fdcb0e4bd8071a006cca75ba570a68b9', 'identity': [16777229, 49380365, 33188, 1, 6617, 1791590239870875131, 1791590239870875131]}
SOURCE_INSTALL_RECORD_PIN={'path': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_graph_helper_controls_v21_sources/Root_helper_SOURCE_install_record.json', 'sha256': '7f5a98632ac8210de1ae0926bebcd51a43359ec9f17e89b7e81ecf931879fc37', 'identity': [16777229, 49380107, 33188, 1, 7507, 1791589879966736928, 1791589879966736928]}
UNKNOWN_Q=None
UNKNOWN_BUSINESS_PINS=None
GRAPH_PATH=Path('/Users/wen/spot/validation/artifacts/axial-material-sender-window-root-index-graph-trace-table-combined-runtime-v20-20261010/input_graph.json')
GRAPH_SHA='dfaaaff743d8edf4c94b262c5ee8104f606eddecaf39260010167f0884c6d976'
GRAPH_IDENTITY=[16777229,49377441,33188,1,45530035,1791587709451819342,1791587709451819342]
SEAL_SHA='b6b3b1477835bd6e312ac833d4cc681e0b7ca15482964f88daf0edb581d60206'
TERM_SHA='ad1d11d68f2ae052068bd6d752ce7b2d64c6cbfcf699713aa684cdc347655d7e'
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,64*2**20

RETURN_FIELDS=['schema', 'classification', 'consumer_scope', 'consumer_selected_literal_and_canonical_paths', 'consumer_complete_namespace_root_sequence', 'scope', 'phase', 'graph_content_sha256', 'fresh_reader_contract', 'canonical_files_read', 'actual_bytes_read', 'byte_count_scope', 'logical_owner_requirements', 'exhaustive_namespaces_checked', 'explicit_aliases_checked', 'coverage', 'trace_coverage', 'live_io_scope', 'live_subprocesses_reexecuted', 'declared_absence_inputs_checked_before_and_after_bytes', 'absence_inputs_are_not_regular_bytes_or_science', 'caller_must_recheck_current_OS_identity_and_live_probe_results', 'typed_snapshot', 'science_qualification_created', 'live_resources_verified', 'external_declaration_exit0_verified', 'caller_must_verify_live_environment_modules_PID_time_and_resources']
TRACE_FIELDS=['schema', 'coverage', 'records', 'subprocess_records', 'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed', 'native_libc_HDF5_loader_and_directory_stat_are_not_traced']

def _fail_constant(value):
    raise ValueError('nonfinite JSON metadata is rejected: '+value)

def _json_object(path):
    with Path(path).open('r') as stream:value=json.load(stream,parse_constant=_fail_constant)
    if type(value) is not dict:raise ValueError('complete object metadata required')
    return value

def _finite_number(value,low,high):
    return type(value) in (int,float) and math.isfinite(value) and low<=value<high

def _source_namespace(support):
    root=SOURCE_ARCHIVE
    if not stat.S_ISDIR(root.lstat().st_mode) or root.is_symlink():raise ValueError('normal SOURCE directory required')
    directories=[];files=[]
    for parent,dirs,names in os.walk(root,followlinks=False):
        dirs.sort();names.sort();directory=Path(parent)
        if directory.is_symlink():raise ValueError('SOURCE alias directory prohibited')
        directories.append(dict(path=str(directory),identity=support.identity(directory)))
        for name in dirs:
            if (directory/name).is_symlink():raise ValueError('SOURCE symlink prohibited')
        for name in names:
            path=directory/name
            if not stat.S_ISREG(path.lstat().st_mode) or path.lstat().st_nlink!=1 or path.is_symlink():raise ValueError('SOURCE namespace contains a nonregular/nonprivate member')
            files.append(support.pin(path))
    if not files or not any(Path(p['path'])==TARGET for p in files) or not any(Path(p['path']).resolve()==Path(__file__).resolve() for p in files):raise ValueError('complete actual driver and host SOURCE required')
    return dict(schema='AXMAT_V21_ACTUAL_COMPLETE_FRESH_VERIFIER_SOURCE_NAMESPACE_V1',root=str(root),directories=directories,files=files,symlinks=[],complete_dynamic_before_after=True,Root_external_freeze_and_host_source_pin_required=True)

def _driver_pin(support,pin,path):
    actual=support.pin(path,pin['sha256'])
    if actual!={key:pin[key] for key in ('path','sha256','identity')} or type(pin.get('size_bytes')) is not int or pin['size_bytes']!=actual['identity'][4]:raise ValueError('complete driver-produced output/input SHA7identity differs')
    return actual

def _gzip_object(support,pin,path):
    actual=_driver_pin(support,pin,path)
    if pin.get('complete_JSON_wire_gzip_decompression_EOF_SHA_verified') is not True or pin.get('no_fields_or_records_filtered') is not True:raise ValueError('complete gzip wire evidence required')
    digest=hashlib.sha256();count=0
    with gzip.open(path,'rb') as stream:
        while True:
            block=stream.read(2**20)
            if not block:break
            digest.update(block);count+=len(block)
    if type(pin.get('uncompressed_JSON_bytes')) is not int or count!=pin['uncompressed_JSON_bytes'] or digest.hexdigest()!=pin['uncompressed_JSON_sha256']:raise ValueError('full gzip decompression EOF/SHA differs')
    with gzip.open(path,'rt',encoding='ascii') as stream:value=json.load(stream,parse_constant=_fail_constant)
    if type(value) is not dict or support.pin(path,pin['sha256'])!=actual:raise ValueError('complete gzip JSON object or byte identity changed')
    return value,actual

def _full_controls(support,report,admission,watch,command):
    expected='ACTUAL_COMPLETE_FRESH_HELPER_VERIFIER_CONTROL_RETURNED_PENDING_EXTERNAL_ROOT'
    if admission['status']!=expected or Path(admission['report']['path'])!=OUT/'ACTUAL_REPORT.json':raise ValueError('actual complete fresh verifier stdout required')
    report_pin=_driver_pin(support,admission['report'],OUT/'ACTUAL_REPORT.json')
    if report['schema']!='AXMAT_NEXT_HELPER_COMPLETE_FRESH_VERIFIER_CONTROL_V1' or report['status']!=expected or type(report['actual_success_pins']) is not dict:raise ValueError('actual full fresh report required')
    scope=('business_component_executed','numeric_or_native_executed','whole_business_INPUT_qualified','native_RSS_qualified','AAA_accuracy_qualified','ABA_admitted','physical_balance_qualified','helper_metadata_qualified')
    if any(report.get(k) is not False for k in scope) or report.get('actual_external_genuine_host_and_Root_closed_exit0_required') is not True:raise ValueError('metadata-only scope and external actual Root terminal required')
    if (report['whole_host_seconds'],report['stage_seconds'],report['rss_mib'],report['joint_HOST_SOURCE_OUT_archive_bytes'],report['history_bytes'],report['min_free_bytes'],report['threads'],report['children'],report['retries'])!=(1800,600,512,64*2**20,96*2**30,8*2**30,1,1,0):raise ValueError('complete unchanged control resource contract required')
    claim=_json_object(OUT/'ACTUAL_RUN_CLAIM.json')
    if any(type(v) is not int for v in (watch.get('pid'),claim.get('PID'),claim.get('parent_PID'),report.get('PID'),report.get('parent_PID'),admission.get('PID'),admission.get('parent_PID'))) or not watch['pid']>0 or not claim['PID']==report['PID']==admission['PID']==watch['pid'] or not claim['parent_PID']==report['parent_PID']==admission['parent_PID']==os.getpid():raise ValueError('actual normal host and watched child PID binding required')
    if claim['phase']!='helper_complete_fresh_verifier_control' or (claim['threads'],claim['children'],claim['retries'])!=(1,1,0):raise ValueError('actual driver claim contract differs')
    if report['fixed_inputs_before']!=report['fixed_inputs_after']:raise ValueError('all actual driver fixed inputs changed')
    for key,pin in report['fixed_inputs_before'].items():_driver_pin(support,pin,Path(pin['path']))
    helper=report['fixed_inputs_before']['new_helper'];graph=report['fixed_inputs_before']['stored_graph'];driver=report['fixed_inputs_before']['driver']
    if {k:helper[k] for k in ('path','sha256','identity')}!=BOUND_HELPER_PIN or helper!=claim['helper'] or graph!=claim['graph'] or driver!=claim['driver'] or Path(driver['path'])!=TARGET or driver['sha256']!=TARGET_SHA or Path(graph['path'])!=GRAPH_PATH or graph['sha256']!=GRAPH_SHA or graph['identity']!=GRAPH_IDENTITY:raise ValueError('actual installed helper/full storedgraph/driver identity differs')
    small=report['private_trace_controls'];positive=small['positive_controls'];negative=small['rejections']
    if len(positive)!=4 or {c['case'] for c in positive}!={'default_list','default_tuple','explicit_False_list','probe_owned_builtin_list_True'} or len(negative)!=3 or {c['case'] for c in negative}!={'nonbool_consume','tuple_True','list_subclass_True'}:raise ValueError('all new private trace controls required')
    for case in positive:
        if case['full_normalized_return_type_order_value_floatbits_and_bytes_equal_old_bcd'] is not True or (case.get('caller_full_identity_type_order_value_floatbits_unchanged') is not True and case.get('owned_list_completely_cleared') is not True):raise ValueError('complete private trace equivalence/nonmutation control failed')
    if any(c['rejected'] is not True or c['class_name']!='InputGraphError' or c['caller_type_identity_nested_value_order_floatbits_unchanged'] is not True for c in negative) or small['old60pure_control_functions_not_changed'] is not True or small['augmented_records_are_not_claimed_as_actual_full_verifier_trace'] is not True:raise ValueError('all private rejects and honest small codec trace required')
    metadata=report['independent_full_saved_graph_metadata']
    wanted=dict(requirement_row_count=238441,requirement_column_count=5,canonical_files=37111,owners=4473,namespaces=86,aliases=186,saved_trace_records=63469,absence_inputs=479,closure_categories=9,scope='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION',consumer_scope=None,newly_declared_input_paths={},newly_declared_input_pins={})
    if any(metadata.get(k)!=v or type(metadata.get(k)) is not type(v) for k,v in wanted.items()) or len(metadata['complete_coverage_fields'])!=9:raise ValueError('all complete current storedgraph scope/counts required')
    expected,expected_pin=_gzip_object(support,report['expected_complete_return_contract'],OUT/'EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz')
    verified,verified_pin=_gzip_object(support,report['actual_complete_verifier_return'],OUT/'ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz')
    encoder=dict(ensure_ascii=True,sort_keys=False,separators=(',',':'),allow_nan=False)
    if json.dumps(expected,**encoder)!=json.dumps(verified,**encoder) or list(verified)!=RETURN_FIELDS or report['complete_return_fields_retained']!=RETURN_FIELDS or report['complete_expected_coverage_tracecoverage_scope_snapshot_and_counts_equal'] is not True:raise ValueError('full public expected/actual return field/type/order/value equality required')
    if report['expected_complete_return_contract']['uncompressed_JSON_sha256']!=report['actual_complete_verifier_return']['uncompressed_JSON_sha256']:raise ValueError('complete expected/actual return wire SHA differs')
    if verified['schema']!='AXMAT_COMBINED_RUNTIME_FRESH_INPUT_GRAPH_VERIFICATION_V2' or verified['classification']!='FRESH_INPUT_BYTES_NAMESPACES_ALIASES_VERIFIED_ONLY' or verified['consumer_scope'] is not None or verified['scope']!='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION' or verified['phase']!='helper_complete_fresh_verifier_control' or verified['canonical_files_read']!=37111 or verified['logical_owner_requirements']!=238441 or verified['exhaustive_namespaces_checked']!=86 or verified['explicit_aliases_checked']!=186 or verified['declared_absence_inputs_checked_before_and_after_bytes']!=479 or len(verified['coverage'])!=9 or any(verified[k] is not False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified','live_subprocesses_reexecuted')):raise ValueError('complete current fresh verifier returned scope required')
    del expected,verified
    trace,trace_pin=_gzip_object(support,report['actual_complete_ReadOpenAudit_trace'],OUT/'ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz')
    if list(trace)!=TRACE_FIELDS or trace['schema']!='AXMAT_READ_OPEN_ATTEMPT_TRACE_V1' or trace['coverage']!='PYTHON_AUDIT_OPEN_ATTEMPTS_ONLY' or trace['subprocess_records']!=[] or type(trace['records']) is not list or len(trace['records'])!=37112:raise ValueError('all actual unfiltered37112 read-open records required')
    paths=[]
    for record in trace['records']:
        if type(record) is not dict or record['event']!='open' or record['kind']!='path' or record['access']!='read' or record['observation']!='OPEN_ATTEMPT' or type(record['attempt_count']) is not int or record['attempt_count']!=1:raise ValueError('every real canonical/graph read-only open attempt must be retained')
        paths.append(record['path'])
    if len(set(paths))!=37112 or paths.count(str(GRAPH_PATH))!=1 or type(trace['unique_records']) is not int or trace['unique_records']!=37112 or type(trace['actual_read_open_attempts']) is not int or trace['actual_read_open_attempts']!=37112 or trace['record_storage']!='EXACT_RECORD_DEDUPLICATION_WITH_ACTUAL_ATTEMPT_COUNTS' or trace['success_of_open_attempt_is_not_observed'] is not True or trace['native_libc_HDF5_loader_and_directory_stat_are_not_traced'] is not True:raise ValueError('full real trace counts/attempts and honest observation scope required')
    if report['actual_complete_trace_counts']!=dict(records=37112,attempts=37112,canonical_files=37111,external_graph_reads=1,no_subprocess_reexecuted=True):raise ValueError('complete reported actual trace counts differ')
    del trace,paths
    if set(p.name for p in OUT.iterdir())!={'ACTUAL_RUN_CLAIM.json','ACTUAL_REPORT.json','private_trace_fixture.txt','EXPECTED_COMPLETE_RETURN_CONTRACT.json.gz','ACTUAL_COMPLETE_VERIFIER_RETURN.json.gz','ACTUAL_COMPLETE_READ_OPEN_TRACE.json.gz'} or any(not stat.S_ISREG(p.lstat().st_mode) or p.is_symlink() for p in OUT.iterdir()):raise ValueError('full exact fresh output namespace required')
    success=report['actual_success_pins']
    if success['helper']!=helper or success['graph']!=graph or success['full_return']!=report['actual_complete_verifier_return'] or success['full_trace']!=report['actual_complete_ReadOpenAudit_trace']:raise ValueError('all full actual success pins required')
    return dict(actual_report=report_pin,actual_claim=support.pin(OUT/'ACTUAL_RUN_CLAIM.json'),actual_host_PID=os.getpid(),actual_child_PID=watch['pid'],actual_claim_parent_and_watch_PID_match=True,complete_expected_return=expected_pin,complete_actual_return=verified_pin,complete_actual_unfiltered_trace=trace_pin,complete_private_controls=True,complete_current_graph_verifier_returned=True,external_Root_closed_terminal_required=True)

def main():
    started=time.monotonic()
    if SOURCE_STATUS!='READY_SOURCE_BOUND_BY_ROOT' or any(type(p) is not dict for p in (BOUND_HELPER_PIN,INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN)) or type(TARGET_SHA) is not str or len(TARGET_SHA)!=64:
        raise ValueError('UNREADY host requires actual Root SOURCE bindings before I/O or guard import')
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
    if os.path.lexists(HOST) or os.path.lexists(OUT):raise ValueError('fresh one-use controls host and output required; no retry')
    source_before=_source_namespace(support)
    if support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256'])!=BOUND_HELPER_PIN or support.pin(INSTALL_WITNESS_PIN['path'],INSTALL_WITNESS_PIN['sha256'])!=INSTALL_WITNESS_PIN or support.pin(SOURCE_INSTALL_RECORD_PIN['path'],SOURCE_INSTALL_RECORD_PIN['sha256'])!=SOURCE_INSTALL_RECORD_PIN:
        raise ValueError('actual installed helper and closed exact-integer SOURCE witness pins changed')
    inputs=[support.pin(TARGET,TARGET_SHA),support.pin(BOUND_HELPER_PIN['path'],BOUND_HELPER_PIN['sha256']),support.pin(Path('/Users/wen/spot/validation/axial_material/combined_runtime_complete_input_graph_fresh_wire_trace_table_order_preserved_20261010.py'),'bcd692aa3e42ecf4336bb70068c560bd322c789fd3fd458baade409ab6f829a6'),support.pin(GRAPH_PATH,GRAPH_SHA),support_pin,support.pin(support.TARGET,support.TARGET_SHA),support.pin(support.OUT/'seal.json',SEAL_SHA),support.pin(support.TERMINAL/'terminal_return.json',TERM_SHA),INSTALL_WITNESS_PIN,SOURCE_INSTALL_RECORD_PIN]+source_before['files']
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    declared_history_roots=(HOST,OUT,support.SOURCE,support.OUT,support.TERMINAL)
    if len(declared_history_roots)!=5 or any(path==support.ART or not path.is_relative_to(support.ART) for path in declared_history_roots):
        raise ValueError('all five declared history roots must remain strict ART descendants')
    roots=resource.history_roots([str(path) for path in declared_history_roots],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        HOST.mkdir()
        for name in ('runtime','run','COMPLETE_FRESH_VERIFIER'):(HOST/name).mkdir()
        shutil.copy2(support.BOUNDED,HOST/'runtime/run_bounded_dragon.py')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(HOST,remaining,'COMPLETE_FRESH_VERIFIER',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources:raise ValueError('genuine runner binding required')
        command=[str(support.PYTHON),'-B',str(TARGET),'--output-dir',str(OUT),'--driver-sha256',TARGET_SHA]
        runner.execute(HOST/'run','admit',command,STAGE_CAP)
        log=HOST/'run/admit.log';watch_path=HOST/'run/admit.watchdog.json'
        admission=_json_object(log);watch=_json_object(watch_path)
        control_report=_json_object(OUT/'ACTUAL_REPORT.json')
        actual_full_controls=_full_controls(support,control_report,admission,watch,command)
        report_pin=actual_full_controls['actual_report']
        if len(runner.records)!=1 or runner.records[0]['status']!='PASS' or type(watch['returncode']) is not int or watch['returncode']!=0 or watch['command']!=command or watch['limit_failure'] is not None or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True or not 0<=watch['sampled_peak_rss_mib']<RSS_CAP:
            raise ValueError('one genuine bounded read-only child PASS required')
        if type(watch['pid']) is not int or watch['pid']<=0 or watch['rss_cap_mib']!=RSS_CAP or not _finite_number(watch['sampled_peak_rss_mib'],0,RSS_CAP) or not _finite_number(watch['elapsed_seconds'],0,STAGE_CAP) or not _finite_number(watch['wall_cap_seconds'],0,STAGE_CAP+1) or not 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=runner.records[0]['wall_cap_seconds']<=STAGE_CAP:
            raise ValueError('actual genuine600-second watched child contract differs')
        source_after=_source_namespace(support)
        if source_after!=source_before:raise ValueError('complete SOURCE directories/files/SHA7identity changed')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))
        if not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        value=dict(schema='AXMAT_V21_GENUINE_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_HOST_V1',status='ACTUAL_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_EXTERNAL_ROOT_REQUIRED',actual_full_controls=actual_full_controls,source_namespace_before=source_before,source_namespace_after=source_after,installed_helper=BOUND_HELPER_PIN,actual_closed_SOURCE_install_witness=INSTALL_WITNESS_PIN,source_install_record=SOURCE_INSTALL_RECORD_PIN,actual_host_PID=os.getpid(),helper_metadata_qualified=False,whole_business_INPUT_qualified=False,physical_balance_qualified=False,UNKNOWN_Q=None,UNKNOWN_BUSINESS_PINS=None,input_sources=inputs,original_helper=hpin,resource_factory=rpin,actual_canonical_command=command,actual_control_report=report_pin,actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False,actual_watchdog=support.pin(watch_path),watchdog=watch,stage_records=runner.records,resources_before=before,resources_after=after,whole_seconds=elapsed,archive_before_result_bytes=archived,whole_wall_cap_seconds=WHOLE_CAP,stage_wall_cap_seconds=STAGE_CAP,rss_cap_mib=RSS_CAP,archive_cap_bytes=ARCHIVE_CAP,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False)
        support.write_new(HOST/'result.json',value)
        if support.archive_bytes((HOST,OUT,SOURCE_ARCHIVE,RECEIPTS))>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(HOST/'result.json'),actual_merged_child_stdout_stderr=support.pin(log),independent_child_stdout_captured=False,independent_child_stderr_captured=False,actual_external_Root_terminal_required=True),allow_nan=False),flush=True)
    except BaseException as error:
        if HOST.is_dir():support.write_new(HOST/'failed_host_result.json',dict(status='FAILED_COMPLETE_CURRENT_GRAPH_FRESH_VERIFIER_NO_RETRY',error=repr(error),stage_records=[] if runner is None else runner.records,native_RSS_verified=False,AAA_accuracy_qualified=False,ABA_admitted=False))
        raise

if __name__=='__main__':main()
