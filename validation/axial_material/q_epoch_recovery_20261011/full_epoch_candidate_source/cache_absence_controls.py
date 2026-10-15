"""New real five-case explicit CPython-cache absence controls; no process.

Cases are based on the durable v30 result's definitions, not its PASS flags.
Each result is recreated with current real file/parent identities and actual
read-open attempts.  No old absence observation is normalized or inherited.
"""
import copy
import errno
import hashlib
import importlib.util
import os
from pathlib import Path

CASE_NAMES=['DECLARED_REAL_F574_CACHE_ENOENT_READ_ACCEPTED','SAME_REAL_TRACE_UNDECLARED_REJECTED','PREEXISTING_CACHE_FILE_REJECTED','REAL_EXISTING_PARENT_REPLACEMENT_REJECTED','ACTUAL_READWRITE_ENOENT_REJECTED']

def require(value,message):
    if type(value)is not bool or not value:raise AssertionError(message)

def rejected(g,call,message):
    try:call()
    except g.InputGraphError as error:
        require(type(error)is g.InputGraphError and str(error)==message,'original exact rejection class/message required')
        return dict(error_type=type(error).__name__,message=str(error),rejected=True)
    raise AssertionError('required absence rejection did not occur')

def run_controls(g,root,f574_pin,exact_value):
    root=Path(root);require(not os.path.lexists(root),'fresh five-case fixture root required')
    root.mkdir(mode=0o700)
    source=Path(f574_pin['path']);require(hashlib.sha256(source.read_bytes()).hexdigest()==f574_pin['sha256'],'actual fixed historical f574 Source bytes required')
    cache=importlib.util.cache_from_source(str(source));require(not os.path.lexists(cache),'predeclared real f574 cache must be genuine ENOENT')
    owners=[dict(owner='actual_cache_control_'+c,category=c,expected_files={str(source):f574_pin['sha256']})for c in g.CLOSURE_CATEGORIES]
    absent={cache:dict(owner=str(source)+'#OPTIONAL_CURRENT_INTERPRETER_CACHE',category='code_environment',reason='cache_from_source of actual full-pinned f574 Source; declared before trace; ENOENT INPUT only')}
    aliases=g._alias_map(g.capture_aliases([str(p)for p in (source,*source.parents)]))
    pre=g._absence_phase(g._absence_inputs(absent),aliases)
    with g.ReadOpenAudit()as audit:
        with source.open('rb')as stream:stream.read()
        try:open(cache,'rb')
        except FileNotFoundError as error:
            require(error.errno==errno.ENOENT,'genuine read ENOENT required')
            actual_errno=dict(errno=error.errno,path=cache,type=type(error).__name__)
        else:raise AssertionError('real cache unexpectedly exists')
    trace=audit.snapshot();require(list(trace)==['schema','coverage','records','subprocess_records','unique_records','actual_read_open_attempts','record_storage','success_of_open_attempt_is_not_observed','native_libc_HDF5_loader_and_directory_stat_are_not_traced'],'all nine actual trace fields required')
    kwargs=dict(typed_snapshot=dict(actual_cache_control=True),owners=owners,aliases=list(aliases.values()),read_trace=trace,absence_inputs=absent)
    graph=g.create_fresh_complete_wire_graph(**kwargs)
    require(graph['trace_coverage']['explicit_declared_absent_file_attempts']==1 and len(graph['canonical_files'])==1 and graph['absence_observations']==pre,'real declared cache read must be owned as absence, never regular input bytes')
    require(graph['absence_inputs_are_not_regular_bytes_or_science']is True and graph['science_qualification_created']is False,'negative input cannot create byte/science qualification')
    records=g._trace_records(trace['records']);requirements=[dict(path=str(source),canonical_path=str(source),owner=o['owner'],category=o['category'],binding_role='EXPECTED_INPUT_BYTES')for o in owners]
    def coverage(records,negative):return g._trace_coverage(records,requirements,[],aliases,[],[],[],[],negative)
    result=[dict(case=CASE_NAMES[0],actual_errno=actual_errno,declaration_before_trace=absent,pre_absence=pre,trace=trace,graph=graph,coverage=graph['trace_coverage'])]
    result.append(dict(case=CASE_NAMES[1],direct=rejected(g,lambda:coverage(records,{}),'unowned or unavailable read-open attempt: '+cache)))
    preexisting=root/'preexisting_cache';preexisting.mkdir();fixture=preexisting/'fixed_fixture.py';fixture.write_bytes(b'fixed fixture = 1\n');existing_cache=Path(importlib.util.cache_from_source(str(fixture)));existing_cache.parent.mkdir();existing_cache.write_bytes(b'explicit preexisting cache fixture\n')
    existing_absent={str(existing_cache):dict(owner='actual_preexisting_cache',category='code_environment',reason='predeclared tiny cache candidate')}
    result.append(dict(case=CASE_NAMES[2],phase=rejected(g,lambda:g._absence_phase(g._absence_inputs(existing_absent),{}),'declared absent input exists: '+str(existing_cache))))
    replacement=root/'parent_replacement';replacement.mkdir();replacement_source=replacement/'fixed_fixture.py';replacement_source.write_bytes(b'fixed fixture = 1\n');replacement_cache=Path(importlib.util.cache_from_source(str(replacement_source)));replacement_cache.parent.mkdir();replacement_absent={str(replacement_cache):dict(owner='actual_parent_replacement',category='code_environment',reason='predeclared actual cache ancestor fixture')}
    replacement_before=g._absence_phase(g._absence_inputs(replacement_absent),{})
    replacement_digest=hashlib.sha256(replacement_source.read_bytes()).hexdigest()
    replacement_owners=[dict(owner='actual_parent_'+c,category=c,expected_files={str(replacement_source):replacement_digest})for c in g.CLOSURE_CATEGORIES]
    replacement_graph=g.create_fresh_complete_wire_graph(typed_snapshot=dict(parent_replacement=True),owners=replacement_owners,absence_inputs=replacement_absent)
    old_parent=replacement_cache.parent.lstat();retained=replacement/'retained_original_cache_parent';replacement_cache.parent.rename(retained);replacement_cache.parent.mkdir();new_parent=replacement_cache.parent.lstat()
    require(old_parent.st_ino!=new_parent.st_ino,'actual parent replacement must change inode')
    rejection='declared absent input or its existing ancestors/aliases changed'
    result.append(dict(case=CASE_NAMES[3],pre_absence=replacement_before,old_parent_inode=old_parent.st_ino,new_parent_inode=new_parent.st_ino,retained_original_parent=str(retained),phase=rejected(g,lambda:g._absence_phase(g._absence_inputs(replacement_absent),{},expected=replacement_before),rejection),graph_verification=rejected(g,lambda:g.verify_graph(replacement_graph,phase='actual_cache_parent_replacement'),rejection)))
    with g.ReadOpenAudit()as readwrite_audit:
        try:open(cache,'r+b')
        except FileNotFoundError as error:require(error.errno==errno.ENOENT,'real readwrite ENOENT required')
        else:raise AssertionError('real cache unexpectedly exists')
    readwrite_trace=readwrite_audit.snapshot()
    result.append(dict(case=CASE_NAMES[4],trace=readwrite_trace,direct=rejected(g,lambda:coverage(g._trace_records(readwrite_trace['records']),g._absence_inputs(absent)),'declared absent input covers only the exact read-only file path attempt')))
    require([r['case']for r in result]==CASE_NAMES,'all five original behavior case definitions required')
    exact_value(g._absence_phase(g._absence_inputs(absent),aliases,expected=pre),pre,'current_actual_cache_absence_before_after')
    return dict(schema='SPOT_NEW_EPOCH_ACTUAL_EXPLICIT_CACHE_ABSENCE_BEHAVIOR_V1',cases=result,case_count=5,current_exact_ENOENT_and_parent_identities=True,old_PASS_flags_not_used=True,all480_production_absences_verified=False,new_Q_created=False,whole_INPUT_admitted=False)
