"""Current Root binding, exact ordinary EOF pins and complete protocol contracts.

This new Source never restores an old pathname or an old identity.  Historical
results remain data.  Only a real current Root review can authorize a bounded
full pure run; the separate complete-current fresh path remains blocked by the
53 missing original canonical byte inputs until every owner is resolved.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import struct
import sys

RETURN_FIELDS = ['schema', 'classification', 'consumer_scope', 'consumer_selected_literal_and_canonical_paths', 'consumer_complete_namespace_root_sequence', 'scope', 'phase', 'graph_content_sha256', 'fresh_reader_contract', 'canonical_files_read', 'actual_bytes_read', 'byte_count_scope', 'logical_owner_requirements', 'exhaustive_namespaces_checked', 'explicit_aliases_checked', 'coverage', 'trace_coverage', 'live_io_scope', 'live_subprocesses_reexecuted', 'declared_absence_inputs_checked_before_and_after_bytes', 'absence_inputs_are_not_regular_bytes_or_science', 'caller_must_recheck_current_OS_identity_and_live_probe_results', 'typed_snapshot', 'science_qualification_created', 'live_resources_verified', 'external_declaration_exit0_verified', 'caller_must_verify_live_environment_modules_PID_time_and_resources']
SNAPSHOT_FIELDS = ['schema', 'coverage', 'records', 'subprocess_records', 'unique_records', 'actual_read_open_attempts', 'record_storage', 'success_of_open_attempt_is_not_observed', 'native_libc_HDF5_loader_and_directory_stat_are_not_traced']
THREAD_KEYS = ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')

def require(value, message):
    if type(value) is not bool or not value:
        raise ValueError(message)

def identity(info):
    return [info.st_dev,info.st_ino,info.st_mode,info.st_nlink,info.st_size,info.st_mtime_ns,info.st_ctime_ns]

def pin(path, expected_sha256=None):
    path=Path(path)
    require(path.is_absolute(),'absolute input path required')
    for ancestor in (path,*path.parents):
        require(not ancestor.is_symlink(),'ordinary pin cannot follow a symlink')
    before=path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_nlink==1,'single-link regular input required')
    h=hashlib.sha256();count=0
    with path.open('rb') as stream:
        require(identity(os.fstat(stream.fileno()))==identity(before),'open FD identity differs')
        while True:
            block=stream.read(1048576)
            if not block:break
            count+=len(block);h.update(block)
        require(identity(os.fstat(stream.fileno()))==identity(before),'FD changed through full EOF')
    require(identity(path.lstat())==identity(before) and count==before.st_size,'pathname changed through full EOF')
    digest=h.hexdigest()
    if expected_sha256 is not None:require(digest==expected_sha256,'full SHA changed')
    return dict(path=str(path),size_bytes=count,sha256=digest,identity=identity(before))

def exact(left,right,where='root'):
    require(type(left)is type(right),where+': exact type differs')
    if type(left)is dict:
        require(list(left)==list(right),where+': whole dict key order differs')
        for key in left:exact(left[key],right[key],where+'/'+str(key))
    elif type(left) in (list,tuple):
        require(len(left)==len(right),where+': length differs')
        for index,(a,b)in enumerate(zip(left,right)):exact(a,b,where+'/'+str(index))
    elif type(left)is float:
        require(struct.pack('>d',left)==struct.pack('>d',right),where+': float bits differ')
    else:require(left==right,where+': value differs')

def read_pinned(wanted):
    require(type(wanted)is dict and set(wanted)=={'path','size_bytes','sha256','identity'},'complete pin schema required')
    require(type(wanted['identity'])is list and len(wanted['identity'])==7 and all(type(v)is int for v in wanted['identity']),'exact integer seven-field identity required')
    before=pin(wanted['path'],wanted['sha256']);require(before==wanted,'current full EOF pin mismatch')
    data=Path(wanted['path']).read_bytes()
    require(pin(wanted['path'],wanted['sha256'])==before,'input changed while reading complete value')
    return data

def load(wanted,name):
    read_pinned(wanted)
    spec=importlib.util.spec_from_file_location(name,wanted['path'])
    require(spec is not None and spec.loader is not None,'normal Source loader required')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    require(Path(module.__file__).resolve()==Path(wanted['path']).resolve(),'actual module path differs')
    require(pin(wanted['path'])==wanted,'Source changed during import')
    return module

def authorize(path,digest,role):
    require(sys.dont_write_bytecode and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile()is None,'normal -B nonoptimized unprofiled process required')
    require(all(os.environ.get(k)=='1' for k in THREAD_KEYS),'original one-thread environment required')
    before=pin(path,digest);cfg=json.loads(read_pinned(before))
    require(cfg['schema']=='SPOT_CURRENT_ROOT_FULL_PURE_EXECUTION_BINDING_V1' and cfg['status']=='ROOT_REVIEWED_NEW_EPOCH_FULL_PURE_SOURCE_ONLY','real current Root Source review required')
    require(cfg['scope']=='FULL_ORIGINAL_PURE_PLUS_REAL_INDEX_WIRE67_CACHE_ABSENCE_NO_FRESH_OR_Q','complete pure scope required')
    require(cfg['caps']==dict(whole_seconds=60,stage_seconds=60,rss_mib=512,archive_bytes=64*2**20,threads=1,children_at_once=1,retries=0),'original pure bounds changed')
    flag_names={'current_complete_fresh_qualified','new_Q_created','whole_INPUT_admitted','whole_build_qualified','native_RSS_verified','AAA_accuracy_qualified','ABA_admitted','science_or_BOOT_admitted'}
    require(set(cfg['qualification_flags'])==flag_names and all(type(v)is bool and v is False for v in cfg['qualification_flags'].values()),'Source review must retain every false fresh/Q/business/science boundary')
    for item in cfg['source_namespace_files']:read_pinned(item)
    require(pin(Path(__file__))in cfg['source_namespace_files'],'binding Source must belong to complete reviewed Source namespace')
    require(pin(cfg[role]['path'])==cfg[role] and cfg[role]in cfg['source_namespace_files'],'actual entry Source not reviewed')
    review=json.loads(read_pinned(cfg['Root_Source_review']))
    require(review['status']=='ROOT_REVIEWED_NEW_EPOCH_FULL_PURE_SOURCE_ONLY' and review['blockers']==[] and review['actual_source_namespace_files']==cfg['source_namespace_files'],'independent actual Root Source review differs')
    tool=json.loads(read_pinned(cfg['Root_Source_review_actual_tool_return']))
    if 'actual_tool_return'in tool:tool=tool['actual_tool_return']
    require(type(tool.get('exit_code'))is int and tool['exit_code']==0 and 'session_id'not in tool,'genuine current Source review must be closed zero')
    review_stdout=json.loads(tool['output'])
    require(review_stdout['review_pin']==cfg['Root_Source_review'],'genuine current Root Source review stdout must bind this exact review')
    for key in ('helper','current_epoch_input_observation','small_data_result','small_data_true_closed_tool'):
        read_pinned(cfg[key])
    small=json.loads(read_pinned(cfg['small_data_result']))
    require(small['status']=='ACTUAL_SMALL_DATA_CONTROLS_PASS_ONLY_NOT_FULL_PURE_FRESH_OR_Q' and small['children_started']==0 and small['current_complete_fresh_qualified']is False and small['new_Q_created']is False,'actual small-data result remains small-only')
    small_tool=json.loads(read_pinned(cfg['small_data_true_closed_tool']))
    if 'actual_tool_return'in small_tool:small_tool=small_tool['actual_tool_return']
    if 'closed'in small_tool:small_tool=small_tool['closed']
    require(type(small_tool.get('exit_code'))is int and small_tool['exit_code']==0 and 'session_id'not in small_tool,'actual small-data tool must be closed zero')
    small_stdout=json.loads(small_tool['output'])
    require(small_stdout['result']==cfg['small_data_result'] and small_stdout['new_Q_created']is False,'actual small-data stdout must bind this whole result')
    require(pin(path,digest)==before,'current Root binding changed')
    cfg['_binding_pin']=before
    return cfg

def validate_complete_current_fresh(g,graph,expected,actual,trace,scope):
    """Future full-current gate.  Never accepts a sampled/old479 return.

    The caller must really build the current complete graph and repeat every
    ordinary-byte/namespace/alias and all480 negative-input observations.  This
    callable contract is retained for the next phase, and is NOT run by pure.
    """
    require(scope['status']=='ALL_ORIGINAL_CANONICAL_BYTES_OWNERS_RESOLVED_CURRENT_EPOCH' and scope['unresolved_original_canonical_endpoints']==[],'53 unknown old canonical bytes cannot be erased, substituted by absence, or claimed current')
    require(len(scope['original_canonical_expected_sha256'])==37590,'whole original37590 owner scope must remain explicit')
    require(set(scope['current_literal_path_by_original'])==set(scope['original_canonical_expected_sha256']),'every original literal owner must have a declared current binding')
    require(len(graph['absence_inputs'])==480 and set(graph['absence_observations'])==set(graph['absence_inputs']),'all480 original declared absence roles and observations required')
    require(set(scope['original_absence_roles_by_current_path'])==set(graph['absence_inputs']),'all480 absence owner/category/reason bindings required')
    require(graph['consumer_scope']is None and graph['scope']=='INPUT_ONLY_NO_SCIENCE_OR_RESOURCE_DECISION','full graph cannot become a selected consumer')
    require(list(expected)==list(actual)==RETURN_FIELDS and list(trace)==SNAPSHOT_FIELDS,'all27 public and9 complete snapshot fields required')
    exact(expected,actual,'full27_current_expected_actual')
    require(actual['declared_absence_inputs_checked_before_and_after_bytes']==480 and actual['canonical_files_read']==len(graph['canonical_files']) and actual['logical_owner_requirements']==graph['requirements']['rows']['row_count'],'complete graph counts must come from real graph, never a patched old count')
    require(actual['live_subprocesses_reexecuted']is False and all(actual[k]is False for k in ('science_qualification_created','live_resources_verified','external_declaration_exit0_verified')),'full fresh metadata cannot grant business/science/live resource admission')
    paths={entry['path']for entry in graph['canonical_files']}
    require(set(scope['current_literal_path_by_original'].values())<=paths,'every original canonical owner must resolve in the whole current canonical graph')
    actual_paths=[]
    for record in trace['records']:
        require(type(record)is dict and record['kind']=='path' and record['event']=='open' and record['access']=='read' and record['observation']=='OPEN_ATTEMPT' and type(record['attempt_count'])is int and record['attempt_count']==1,'every actual full fresh read must be observed exactly once')
        actual_paths.append(record['path'])
    require(len(actual_paths)==len(set(actual_paths))==len(paths)+1 and set(actual_paths)==paths|{scope['current_graph_pin']['path']},'entire canonical union plus external graph must be actually read in one genuine phase')
    require(trace['unique_records']==len(trace['records']) and trace['actual_read_open_attempts']==len(actual_paths) and trace['subprocess_records']==[],'complete nine-field actual trace counts differ')
    negative={p:{k:v[k]for k in ('owner','category','reason')}for p,v in graph['absence_inputs'].items()}
    aliases=g._alias_map(graph['aliases'])
    observed=g._absence_phase(g._absence_inputs(negative),aliases,expected=graph['absence_observations'])
    require(len(observed)==480,'all480 current ENOENT observations required')
    return dict(complete27_return_fields=RETURN_FIELDS,complete9_snapshot_fields=SNAPSHOT_FIELDS,all480_negative_inputs_actual=True,new_Q_created=False,whole_INPUT_admitted=False)
