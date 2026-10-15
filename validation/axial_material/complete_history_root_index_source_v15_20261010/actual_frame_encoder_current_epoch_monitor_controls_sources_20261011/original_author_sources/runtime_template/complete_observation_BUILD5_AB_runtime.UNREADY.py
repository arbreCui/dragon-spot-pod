"""UNREADY complete five-group fresh native build and full A/B observer production.
Only a Root-bound reviewed genuine host may call run; no import-time work.
Original physical source bytes and original Darwin arm64 compiler flags retained.
No old binary/object/archive or material deck construction; only three procedure FIL path literals change. No payload truncation.
"""
import hashlib
import base64
import traceback
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import stat
import struct
import subprocess
import sys
import tarfile
import time

SOURCE_STATUS='UNREADY_SOURCE_ONLY'
CAPS=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0)
THREAD_KEYS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS')
FUTURE=dict(actual_runtime_qualification_sha256=None,actual_observer_native_controls_run=None,actual_native_Source_binary_linkage_qualification_sha256=None,actual_scientific_qualification_sha256=None,scientific_accuracy_qualified=False,physical_neutron_balance_qualified=False,AAA_accuracy_qualified=False,ABA_admitted=False,native_transport_executed=False,complete_context_aggregation_qualified=False)
# Complete selected original Makefile variables, preserving empty/undefined
# variables rather than inventing common flags. Original Darwin/arm64, GNU
# compilers, openmp/mpi/hdf5/intel/nvidia/llvm disabled. Relative INCLUDE is
# evaluated from each original component src directory in the fresh tree.
ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES = {
    'Ganlib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-Wno-maybe-uninitialized','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':'cpp','FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Ganlib/lib/Darwin_arm64/modules','module_copy':True},
    'Utilib': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':[], 'PREPRO':None,'FMPI':[], 'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Utilib/lib/Darwin_arm64/modules','module_copy':True},
    'Trivac': {'C':None,'CFLAGS':[],'FLAGS':[],
        'F90':'fortran','FFLAGS':['-fPIC','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':None,'FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[], 'lib_module':None,'module_copy':False},
    'Dragon': {'C':'c','CFLAGS':['-Wall','-fPIC'],'FLAGS':['-DLinux','-DUnix'],
        'F90':'fortran','FFLAGS':['-fPIC','-Wall','-ffpe-summary=none'],
        'FFLAG77':['-fPIC','-Wall','-frecord-marker=4','-ffpe-summary=none'],
        'INCLUDE':['-I../../Ganlib/lib/Darwin_arm64/modules/'], 'PREPRO':'cpp','FMPI':[],
        'opt':['-O','-g'], 'COMP':[], 'LFLAGS':[],
        'lib_module':'Dragon/lib/Darwin_arm64/modules','module_copy':True},
}

ROLE_LABELS={'LIBMIX_BEFORE':'oldmacro-pre-LIBMIX','LIBDEN_OLD_CONTEXT':'oldmacro-LIBDEN','LIBMIX_AFTER':'postmacro-LIBMIX','TONDRV_FINAL_AFTER_SHIBA':'final-complete-micro'}
LABELS=('LIBMIX_BEFORE','LIBDEN_OLD_CONTEXT','LIBDEN_BEFORE_FISSION_SLOT_MUTATION','LIBMIX_AFTER','TONDRV_AFTER_REAL_MAT_ELIMINATION','TONDRV_ACTUAL_FINAL_LIBMIX_MASK','TONSPH_BEFORE_ACTUAL_TONCMI','TONDRV_ACTUAL_SPH_CALL_DECISION','TONDRV_FINAL_AFTER_SHIBA')

CANONICAL_OS_TOOL_PATHS = {'fortran': '/opt/homebrew/Cellar/gcc/15.2.0_1/bin/gfortran-15', 'c': '/usr/bin/gcc', 'cpp': '/usr/bin/cpp', 'ar': '/usr/bin/ar', 'lsof': '/usr/sbin/lsof', 'ps': '/bin/ps'}

def source_tool_nlink_allowed(path,nlink,tool_role=None):
    # Default stays the original single-link contract. Only an explicit one of
    # these six original OS tool roles may preserve a positive real hardlink
    # count. Paths, bytes, all seven identity integers and caller order stay real.
    if tool_role is None:return type(nlink)is int and nlink==1
    require(type(tool_role)is str and tool_role in CANONICAL_OS_TOOL_PATHS,'declared original canonical OS tool role only')
    return str(path)==CANONICAL_OS_TOOL_PATHS[tool_role]and type(nlink)is int and nlink>=1

def require(value,message):
    if type(value)is not bool or not value:raise ValueError(message)

def strict_json(raw):
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate metadata key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))

def identity(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]

def fullpin(path,budget=lambda:None,tool_role=None):
    path=Path(path);before=identity(path.lstat())
    require(path.is_absolute()and all(not q.is_symlink()for q in(path,*path.parents))and stat.S_ISREG(before[2])and source_tool_nlink_allowed(path,before[3],tool_role),'regular nonalias full input; default single-link except explicit canonical OS tools')
    d=hashlib.sha256();size=0
    with path.open('rb')as f:
        require(identity(os.fstat(f.fileno()))==before,'open fullpin identity')
        while True:
            budget();raw=f.read(2**20)
            if not raw:break
            d.update(raw);size+=len(raw)
        require(identity(os.fstat(f.fileno()))==before,'EOF fullpin identity')
    require(identity(path.lstat())==before and size==before[4],'full EOF identity unchanged')
    return dict(path=str(path),sha256=d.hexdigest(),size_bytes=size,identity=before)

def pinshape(p,tool_role=None):
    require(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'},'exact fullpin shape')
    require(type(p['path'])is str and Path(p['path']).is_absolute()and '..'not in Path(p['path']).parts and type(p['sha256'])is str and re.fullmatch('[0-9a-f]{64}',p['sha256'])is not None,'absolute path and SHA')
    require(type(p['size_bytes'])is int and p['size_bytes']>=0 and type(p['identity'])is list and len(p['identity'])==7 and all(type(x)is int and x>=0 for x in p['identity'])and source_tool_nlink_allowed(p['path'],p['identity'][3],tool_role)and p['identity'][4]==p['size_bytes'],'strict integer 7ID and size')

def recheck(p,budget=lambda:None,tool_role=None):
    pinshape(p,tool_role=tool_role);require(fullpin(p['path'],budget,tool_role=tool_role)==p,'complete input SHA/7ID changed: '+p['path']);return p

def write_new(path,value):
    with Path(path).open('x',encoding='utf-8')as f:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')

def tree(path):
    path=Path(path);files=[];dirs={}
    require(path.is_dir()and not path.is_symlink(),'frozen real directory')
    for p in [path,*sorted(path.rglob('*'))]:
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no aliases in complete namespace')
        if stat.S_ISDIR(s.st_mode):dirs[str(p)]=identity(s)
        else:
            require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'no unaccounted special/hardlink');files.append(fullpin(p))
    return dict(files=files,directories=dirs)

def frozen_sources(native,index,observation_source):
    overridden={'Dragon/src/LIBMIX.f':'LIBMIX.observe.UNREADY.f','Dragon/src/LIBDEN.f':'LIBDEN.observe.UNREADY.f','Dragon/src/TONDRV.f':'TONDRV.context_observe.UNREADY.f','Dragon/src/TONSPH.f':'TONSPH.observe.UNREADY.f'}
    expected={r['relative_path']:r['full_original_Source_pin']['sha256']for r in index['members']}
    expected.update({k:fullpin(observation_source/v)['sha256']for k,v in overridden.items()})
    expected['Dragon/src/AXMAT_CONTEXT_OBSERVATION_MOD.f90']=fullpin(observation_source/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90')['sha256']
    actual=[]
    for rel,wanted in expected.items():
        p=fullpin(native/rel);require(p['sha256']==wanted,'full native Source freeze differs: '+rel);actual.append(dict(relative_path=rel,input_pin=p))
    all_source={str(p.relative_to(native))for p in native.rglob('*')if p.is_file()and(p.name=='Makefile'or p.suffix in('.f','.F','.f90','.F90','.c','.h','.inc','.py'))}
    require(all_source==set(expected),'full compile Source namespace coverage; no skipped extra Source')
    return actual

N8_CASE_IDS=('01_exact_environment_and_sole_wait_owner','02_actual_live_business_and_descendants','03_actual_closed_after_live_PS_census','04_actual_nonzero_exit_preserves_stage_failure','05_actual_closed_leader_and_reparented_group','06_unknown_owner_ECHILD_and_PID_reuse_refusals','07_actual_late_descendant_exit_strict_lsof_failure','08_actual_strict_stream_nonzero_timeout_oversize','09_original_resource_caps_and_frozen_Source','10_original_cleanup_exceptions_and_group_evidence','11_actual_watchdog_pipe_and_group_closure','12_actual_Root_and_independent_saved_control_closure')

def n8_require(value,message):
    if type(value) is not bool or not value:raise ValueError(message)

def n8_validate_saved_metadata_types(value):
    if type(value)is dict:
        if set(value) in ({'path','sha256','identity'},{'path','sha256','size_bytes','identity'}):
            n8_require(type(value['path'])is str and Path(value['path']).is_absolute()and '..'not in Path(value['path']).parts and type(value['sha256'])is str and len(value['sha256'])==64 and all(c in '0123456789abcdef'for c in value['sha256']),'typed complete metadata pin path/SHA')
            n8_require(type(value['identity'])is list and len(value['identity'])==7 and all(type(x)is int and x>=0 for x in value['identity']),'typed complete metadata integer7ID')
            if 'size_bytes'in value:n8_require(type(value['size_bytes'])is int and value['size_bytes']>=0 and value['size_bytes']==value['identity'][4],'typed complete metadata size')
        for k,v in value.items():
            if k=='original_caps':n8_require(type(v)is dict and set(v)==set(CAPS)and all(type(x)is int for x in v.values())and v==CAPS,'typed unchanged original nine caps')
            if k=='directories':n8_require(type(v)is dict and all(type(row)is list and len(row)==7 and all(type(x)is int and x>=0 for x in row)for row in v.values()),'typed complete directory7IDs')
            n8_validate_saved_metadata_types(v)
    elif type(value)is list:
        for v in value:n8_validate_saved_metadata_types(v)
    elif type(value)is float:n8_require(value-value==0,'finite saved metadata float')
    return value

def n8_strict_json(raw):
    def pairs(items):
        result={}
        for key,value in items:
            n8_require(key not in result,'duplicate controls metadata key');result[key]=value
        return result
    return n8_validate_saved_metadata_types(json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v))))

def n8_fullpin(path):
    p=Path(path);s=p.lstat();before=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    n8_require(p.is_absolute() and all(not q.is_symlink() for q in (p,*p.parents)) and stat.S_ISREG(s.st_mode) and s.st_nlink==1,'complete Source/META nonalias singlelink')
    with p.open('rb') as stream:
        n8_require(list((lambda t:(t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns))(os.fstat(stream.fileno())))==before,'opened Source/META identity')
        digest=hashlib.file_digest(stream,'sha256').hexdigest()
    t=p.lstat();n8_require([t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]==before,'complete Source/META EOF unchanged')
    return dict(path=str(p),sha256=digest,size_bytes=s.st_size,identity=before)

def n8_recheck_pinned(pin):
    n8_require(type(pin) is dict and set(pin)=={'path','sha256','size_bytes','identity'} and type(pin['path']) is str and Path(pin['path']).is_absolute() and type(pin['sha256']) is str and re.fullmatch('[0-9a-f]{64}',pin['sha256']) is not None,'actual controls exact n8_fullpin required; None refused')
    n8_require(type(pin['size_bytes']) is int and pin['size_bytes']>=0 and type(pin['identity']) is list and len(pin['identity'])==7 and all(type(x) is int and x>=0 for x in pin['identity']) and pin['identity'][3]==1 and pin['identity'][4]==pin['size_bytes'],'controls typed integer7ID/size')
    n8_require(n8_fullpin(pin['path'])==pin,'actual controls Source/META full EOF pin unchanged')
    return pin

def n8_read_pinned(pin):
    n8_recheck_pinned(pin)
    return n8_strict_json(Path(pin['path']).read_bytes())

def n8_actual_closed_zero(pin,expected_schema):
    wrapper=n8_read_pinned(pin);terminal=wrapper['terminal_tool_return']
    n8_require(wrapper['schema']==expected_schema and wrapper['closed'] is True and wrapper['observed_terminal'] is True and wrapper['session_repolled_after_close'] is False,'actual observed CLOSED controls terminal')
    n8_require(type(terminal) is dict and type(terminal['exit_code']) is int and terminal['exit_code']==0 and 'session_id' not in terminal and type(terminal['chunk_id']) is str and bool(terminal['chunk_id']) and wrapper['actual_terminal_chunk']==terminal['chunk_id'],'actual typed zero, exact terminal chunk and no live session')
    return wrapper,n8_strict_json(terminal['output'])

def n8_recheck_saved_regular_file_pins(pins,allow_empty=False):
    n8_require(type(pins)is list and (allow_empty is True or bool(pins)) and all(type(p)is dict and set(p)=={'path','sha256','size_bytes','identity'}for p in pins),'declared complete regular-file fullpins, no missing or filtered evidence')
    n8_require(len({p['path']for p in pins})==len(pins),'unique declared complete regular-file paths')
    for p in pins:n8_recheck_pinned(p)

def n8_recheck_complete_saved_case(case):
    views=case['actual_complete_postclose_namespace_views']
    n8_require(type(views)is dict and set(views)=={'host','output','control','source','receipts'},'all five declared postclose namespace views retained')
    for view in views.values():n8_recheck_saved_regular_file_pins(view['files'],allow_empty=True)
    n8_recheck_saved_regular_file_pins(case['actual_complete_evidence_pins'])

def validate_actual_N8_monitor_controls(qualification_pin,qualification_terminal_pin,author):
    q=n8_read_pinned(qualification_pin)
    n8_require(q['schema']=='ROOT_ACTUAL_N8_EXACT_OWNER_MONITOR_CONTROLS_QUALIFICATION_V1' and q['status']=='ACTUAL_TWELVE_GENUINE_MONITOR_CONTROLS_QUALIFIED_NO_NATIVE_OR_SCIENCE' and q['source_only'] is False and q['actual_monitor_controls_qualified'] is True,'actual Root monitor controls qualification required')
    n8_require(q['actual_author_Source_contract']==author and q['original_caps']==CAPS and all(type(x) is int for x in q['original_caps'].values()),'complete actual controls Source owner contract and original caps')
    for key in ('actual_native_build_or_AB_executed','native_transport_executed','scientific_qualification_created','scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted'):
        n8_require(q[key] is False,'control qualification cannot create native/science fact: '+key)
    binding=n8_read_pinned(q['actual_controls_Source_binding_pin'])
    n8_require(binding['schema']=='ROOT_ACTUAL_N8_MONITOR_CONTROLS_SOURCE_BINDING_V1' and binding['source_only'] is True and binding['actual_author_Source_contract']==author and binding['actual_control_execution'] is None,'actual Source-bound monitor controls roles, not guessed execution')
    manifest=n8_read_pinned(q['actual_controls_manifest_pin'])
    n8_require(manifest['schema']=='ACTUAL_N8_TWELVE_GENUINE_MONITOR_CONTROLS_MANIFEST_V1' and manifest['actual_author_Source_contract']==author and manifest['source_only'] is False and manifest['all_required_controls_passed'] is True and manifest['blockers']==[],'complete actual controls manifest, not a Source protocol')
    n8_require(manifest['actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and manifest['original_caps']==CAPS,'controls Source binding and unchanged limits')
    cases=manifest['cases']
    n8_require(type(cases) is list and len(cases)==len(N8_CASE_IDS) and [c['case_id'] for c in cases]==list(N8_CASE_IDS),'all twelve genuine controls; no filtering unknown cases')
    for case in cases:
        n8_require(case['passed'] is True and case['actual_genuine_runner_used'] is True and case['actual_shared_resource_factory_used'] is True and case['actual_exact_owner_observer_used'] is True and case['synthetic_PS_or_lsof_or_cleanup_error_used_for_qualification'] is False,'actual same monitoring implementation, no mock qualification')
        n8_require(case['actual_complete_raw_evidence_saved'] is True and case['actual_Source_D_and_receipt_E_frozen'] is True and case['actual_original_caps_verified'] is True and case['actual_remaining_owned_groups_absent_after_Root_closure'] is True,'complete raw, frozen Source, original caps and actual residual-group closure')
        n8_actual_closed_zero(case['actual_Root_case_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROL_CASE_TOOL_TERMINAL_RETURN_V1')
        n8_require(type(case['actual_complete_evidence_pins']) is list and bool(case['actual_complete_evidence_pins']),'actual complete Source/small-META raw evidence, no empty case')
        n8_recheck_complete_saved_case(case)
    n8_recheck_saved_regular_file_pins(manifest['actual_complete_controls_regular_file_pins_before_own_append'])
    n8_recheck_saved_regular_file_pins(q['actual_complete_controls_regular_file_pins_before_own_append'])
    _,controls_output=n8_actual_closed_zero(q['actual_Root_controls_tool_terminal_return_pin'],'ROOT_ACTUAL_N8_MONITOR_CONTROLS_TOOL_TERMINAL_RETURN_V1')
    n8_require(controls_output['actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and controls_output['all_required_controls_passed'] is True,'actual Root complete controls zero output coupling')
    peer=n8_read_pinned(q['actual_independent_saved_controls_review_pin'])
    n8_require(peer['schema']=='INDEPENDENT_ACTUAL_N8_SAVED_GENUINE_MONITOR_CONTROLS_REVIEW_V1' and peer['status']=='PASS_ACTUAL_SAVED_TWELVE_GENUINE_MONITOR_CONTROLS_NO_NATIVE_OR_SCIENCE' and peer['actual_author_Source_contract']==author and peer['qualified_actual_controls_manifest_pin']==q['actual_controls_manifest_pin'] and peer['qualified_actual_controls_Source_binding_pin']==q['actual_controls_Source_binding_pin'] and peer['qualified_actual_Root_controls_tool_terminal_return_pin']==q['actual_Root_controls_tool_terminal_return_pin'] and peer['all_checks_passed'] is True and peer['blockers']==[],'independent review of these actual saved controls required')
    checks=peer['checks']
    n8_require(type(checks) is list and type(peer['check_count']) is int and peer['check_count']==len(checks)>0 and len({c['check'] for c in checks})==len(checks) and all(type(c) is dict and set(c)=={'check','passed'} and type(c['check']) is str and bool(c['check']) and c['passed'] is True for c in checks),'unique typed independent actual controls checks')
    _,q_output=n8_actual_closed_zero(qualification_terminal_pin,'ROOT_ACTUAL_N8_MONITOR_CONTROLS_QUALIFICATION_TOOL_TERMINAL_RETURN_V1')
    n8_require(q_output['actual_monitor_controls_qualification_pin']==qualification_pin and q_output['actual_monitor_controls_qualified'] is True and q_output['native_or_scientific_qualification_created'] is False,'actual Root qualification output coupled to this immutable Q')
    return dict(schema='ACTUAL_N8_REQUIRED_MONITOR_CONTROLS_SCOPE_COUPLING_V1',actual_monitor_controls_qualification_pin=qualification_pin,actual_Root_qualification_tool_terminal_return_pin=qualification_terminal_pin,actual_complete_controls_manifest_pin=q['actual_controls_manifest_pin'],actual_independent_saved_controls_review_pin=q['actual_independent_saved_controls_review_pin'],actual_stdlib_subprocess_Source_pin=q['actual_stdlib_subprocess_Source_pin'],all_twelve_actual_controls_required=True,native_or_scientific_qualification_created=False)


def actual_scope(request,author):
    expected=request['actual_author_Source_contract']
    monitor_scope=validate_actual_N8_monitor_controls(request['actual_monitor_controls_qualification_pin'],request['actual_monitor_controls_qualification_terminal_pin'],author)
    require(request['actual_required_monitor_controls_scope']==monitor_scope,'actual monitor controls complete Source coupling before native action')
    require(type(expected)is dict and expected==author,'exact whole observer author Source roles')
    for p in expected.values():recheck(p)
    peer=strict_json(Path(request['independent_observation_Source_review_pin']['path']).read_bytes())
    require(peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_BINDER_SOURCE_REVIEW_V1'and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'and peer['source_only']is True and peer['all_checks_passed']is True and peer['blockers']==[],'independent full observer Source pass required')
    checks=peer['checks'];require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0 and all(type(c)is dict and set(c)=={'check','passed'}and type(c['check'])is str and bool(c['check'])and c['passed']is True for c in checks)and len({c['check']for c in checks})==len(checks),'independent aggregate checks strictly typed')
    admission=strict_json(Path(request['independent_observation_Source_admission_pin']['path']).read_bytes())
    require(admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_V1'and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'and admission['source_only']is True and admission['scientific_qualification_created']is False and admission['independent_Source_review_pin']==request['independent_observation_Source_review_pin'],'Root Source-only admission binds independent review')
    require(peer['actual_author_Source_contract']==expected and admission['actual_author_Source_contract']==expected,'whole Source body pins coupled to peer/admission')
    for k in FUTURE:require(admission[k]is FUTURE[k],'Root Source admission cannot invent actual future: '+k)
    truth=strict_json(Path(request['actual_Root_observation_Source_admission_tool_return_pin']['path']).read_bytes());terminal=truth['terminal_tool_return']
    require(truth['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1'and truth['closed']is True and truth['observed_terminal']is True and truth['session_repolled_after_close']is False and type(terminal['exit_code'])is int and terminal['exit_code']==0 and 'session_id'not in terminal and type(terminal['chunk_id'])is str and bool(terminal['chunk_id'])and truth['actual_terminal_chunk']==terminal['chunk_id'],'actual Root admission CLOSED typed zero')
    output=strict_json(terminal['output']);require(output['status']=='ACTUAL_COMPLETE_NATIVE_OBSERVATION_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE'and output['source_only']is True and output['source_admission_pin']==request['independent_observation_Source_admission_pin'],'Root actual Source admission tool output exact coupling')
    return dict(schema='ACTUAL_COMPLETE_OBSERVATION_SOURCE_SCOPE_COUPLING_V1',source_only=True,actual_author_Source_contract=expected,independent_Source_review_pin=request['independent_observation_Source_review_pin'],independent_observation_Source_admission_pin=request['independent_observation_Source_admission_pin'],actual_Root_admission_tool_return_pin=request['actual_Root_observation_Source_admission_tool_return_pin'],independent_aggregate_check_count=len(checks),**FUTURE)

SHARED_INPUT_LIBRARY_LAYOUT = {'schema': 'COMPLETE_AB_SINGLE_COPY_ORIGINAL_SHARED_LIBRARIES_AND_EXACT_PROCEDURE_FILE_LITERALS_V1', 'shared_directory': 'shared_input_libraries', 'state_order': ['A', 'B'], 'seed_destination_order': ['material.x2m', 'AxMatTone.c2m', 'geometry.dat', 'rnr_cc.c2m', 'rnr_interpol.c2m', 'DLIB_ACTUAL', 'DLIB8R1_370'], 'original_procedure_copy_name': 'AxMatTone.c2m.original', 'literal_replacements': [{'original': "FIL: 'DLIB_ACTUAL'", 'derived': "FIL: '../shared_input_libraries/DLIB_ACTUAL'", 'count': 2}, {'original': "FIL: 'DLIB8R1_370'", 'derived': "FIL: '../shared_input_libraries/DLIB8R1_370'", 'count': 1}]}
REQUIRED_N8_FRESH_NAMESPACES = {'host': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v9-link-count-host-20261011', 'output': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v9-link-count-runtime-20261011', 'control': '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v9-link-count-control-20261011', 'source': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v9_link_count_sources', 'receipts': '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v9_link_count_receipts'}

def validate_request(b,author):
    require(b.get('material_input_layout')==SHARED_INPUT_LIBRARY_LAYOUT and all(type(row['count'])is int for row in b['material_input_layout']['literal_replacements']),'exact shared-library/procedure Source layout; no implicit old duplicate layout')
    require(b['namespaces']==REQUIRED_N8_FRESH_NAMESPACES,'new fixed v9-link-count namespaces only; no N4/N5 reuse')
    require(b['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_BINDING_V1'and b['source_only']is True and b['Root_only_actual_execution']is True and b['scientific_qualification_created']is False,'strict Root observer Source binding')
    require(type(b['original_caps'])is dict and set(b['original_caps'])==set(CAPS)and all(type(v)is int for v in b['original_caps'].values())and b['original_caps']==CAPS,'unchanged typed caps')
    require(b['state_order']==['A','B']and b['build_stage_order']==['Ganlib','Utilib','Trivac','Dragon','Dragon_link']and b['SPOT_AXMAT_OBSERVATION']=='ADMITTED_SOURCE_ONLY','actual full ordered A then B/5groups')
    for k,v in FUTURE.items():require(b[k]is v,'unknown/false future flag '+k)
    seed_contract=strict_json(Path(author['original_material_seed_contract']['path']).read_bytes());require(b['original129_input_pins']==seed_contract['original129_input_pins'],'original129 complete pin contract unchanged');rows=b['original129_input_pins'];require(type(rows)is list and len(rows)==129 and len({p['path']for p in rows})==129,'complete original129 pins')
    extra=b['additional_actual_evidence_input_pins'];require(type(extra)is list and bool(extra)and len({p['path']for p in extra})==len(extra),'nonempty whole additional input list')
    allpins={p['path']:p for p in rows+extra}
    require(len(allpins)==len(rows+extra),'original129 and extra disjoint')
    for p in (b['actual_monitor_controls_qualification_pin'],b['actual_monitor_controls_qualification_terminal_pin']):
        require(allpins.get(p['path'])==p,'actual required monitor Q inputs protected completely before native action')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])==set(CANONICAL_OS_TOOL_PATHS),'complete fixed six OS tool roles before extra input shapes')
    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role)
    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}
    for p in rows:pinshape(p)
    for p in extra:pinshape(p,tool_role=tool_roles_by_path.get(p['path']))
    for k in ('independent_observation_Source_review_pin','independent_observation_Source_admission_pin','actual_Root_observation_Source_admission_tool_return_pin'):
        pinshape(b[k]);require(allpins.get(b[k]['path'])==b[k],'all admission evidence included in protected full inputs')
    require(type(b['tool_pins'])is dict and set(b['tool_pins'])=={'fortran','c','cpp','ar','lsof','ps'},'full native and accounting tool pins')
    for role,p in b['tool_pins'].items():pinshape(p,tool_role=role);require(allpins.get(p['path'])==p,'all actual tools in full protected input list')
    require(Path(b['tool_pins']['fortran']['path']).name.startswith('gfortran')and Path(b['tool_pins']['c']['path']).name.startswith('gcc'),'original GNU Fortran and Darwin C recipe required')
    required={'material.x2m','AxMatTone.c2m','geometry.dat','rnr_cc.c2m','rnr_interpol.c2m','DLIB_ACTUAL','DLIB8R1_370'}
    require(type(b['states'])is dict and list(b['states'])==['A','B'],'A/B source insertion order')
    for state in ('A','B'):
        inputs=b['states'][state]['native_stage_inputs'];require(type(inputs)is list and [row['destination']for row in inputs]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order']and {row['destination']for row in inputs}==required and len(inputs)==len(required),'exact original complete material input set')
        for row in inputs:
            require(type(row)is dict and set(row)=={'destination','input_pin'},'exact immutable seed mapping');pinshape(row['input_pin']);require(allpins.get(row['input_pin']['path'])==row['input_pin'],'all original material inputs protected')
        require(b['states'][state]['original_material_deck_pin']==next(x['input_pin']for x in inputs if x['destination']=='material.x2m'),'exact original deck; no regenerated deck')
        for row in inputs:
            destination=row['destination'];expected=seed_contract['states'][state].get(destination)
            if expected is not None:require(row['input_pin']==expected,'original whole material input fullpin unchanged: '+destination)
            else:require(row['input_pin']['path']==seed_contract['libraries'][destination]['path']and row['input_pin']['sha256']==seed_contract['libraries'][destination]['generation_sha256'],'original material library path and generation SHA')
    return actual_scope(b,author)

def joint_bytes(roots,lsof_tool,ps_tool,monitor=None,owner_observer=None,control_barrier=None):
    monitor_scan_started=None if monitor is None else time.monotonic()
    try:
        total=0;seen=set()
        for root in roots:
            if not Path(root).exists():continue
            for p in Path(root).rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'joint archive aliases forbidden')
                if stat.S_ISDIR(s.st_mode):continue
                require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'joint regular singlelink scope');key=(s.st_dev,s.st_ino);require(key not in seen,'joint hardlink aliases forbidden');seen.add(key);total+=s.st_size
        # Diagnostic scans have the same status as the original guard's /bin/ps:
        # they do not constitute additional material/build business children.
        require(control_barrier is None or (owner_observer is not None and owner_observer.control_mode is True),'no controls barrier in production scope')
        if owner_observer is not None:owner_observer.poll_for_snapshot()
        ps_started_monotonic=time.monotonic()
        ps_argv=[ps_tool,'-axo','pid=,ppid=,pgid=,stat=']
        with subprocess.Popen(ps_argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)as ps_process:
            ps_diagnostic_pid=ps_process.pid
            try:
                ps_stdout,ps_stderr=ps_process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                ps_process.kill();ps_process.wait();raise
            except BaseException:
                ps_process.kill();raise
            ps_returncode=ps_process.poll()
            if ps_returncode:
                raise subprocess.CalledProcessError(ps_returncode,ps_process.args,output=ps_stdout,stderr=ps_stderr)
        require(type(ps_diagnostic_pid)is int and ps_diagnostic_pid>0 and type(ps_returncode)is int and ps_returncode==0,'exact actual PS diagnostic closed EXIT0 before PID exclusion')
        require(len(ps_stdout)<8*2**20 and len(ps_stderr)<8*2**20,'complete bounded fullPS raw streams, never truncated')
        ps_rows={}
        for line in ps_stdout.splitlines():
            words=line.split();require(len(words)==4 and all(w.isdigit()for w in words[:3])and bool(words[3]),'full actual PS pid/ppid/pgid/state rows')
            pid,ppid,pgid=map(int,words[:3]);require(pid>0 and pid not in ps_rows,'unique positive fullPS PID');ps_rows[pid]=dict(pid=pid,ppid=ppid,pgid=pgid,state=words[3])
        parents={pid:r['ppid']for pid,r in ps_rows.items()}
        selected={os.getpid()}
        while True:
            new={p for p,parent in parents.items()if parent in selected};expanded=selected|new
            if expanded==selected:break
            selected=expanded
        # Exclude only this captured, already reaped EXIT0 diagnostic child.
        # Every actual own business descendant remains in the same full closure.
        selected.discard(ps_diagnostic_pid)
        if control_barrier is not None:control_barrier(ps_rows,selected)
        if owner_observer is not None:
            owner_observer.poll_for_snapshot()
            selected=owner_observer.expand_selection(ps_rows,selected,ps_diagnostic_pid,ps_started_monotonic)
        observed=subprocess.run([lsof_tool,'-nP','-F','pfnsiDtk','-a','-p',','.join(map(str,sorted(selected)))],capture_output=True,text=True,timeout=2)
        require(observed.returncode==0,'full live own process file scan required')
        require(len(observed.stdout)<8*2**20 and len(observed.stderr)<8*2**20,'finite complete lsof streams; never truncated')
        returned_pids=[]
        for line in observed.stdout.splitlines():
            if line.startswith('p'):require(line[1:].isdigit(),'actual lsof PID field');returned_pids.append(int(line[1:]))
        require(set(returned_pids)==selected and len(returned_pids)==len(set(returned_pids)),'single strict lsof0 complete selected PID coverage; no absent-PID acceptance')
        records=[];row={}
        for line in observed.stdout.splitlines():
            if line.startswith('f'):
                if row:records.append(row)
                row={'f':line[1:]}
            elif line and line[0]in'nsiDtk':
                if line[0]=='k':require('k'not in row,'single actual link-count field per file record required')
                row[line[0]]=line[1:]
        if row:records.append(row)
        unlinked=set();unlinked_bytes=0
        for row in records:
            if 'k'in row:
                require(row['k'].isascii()and row['k'].isdigit(),'actual file link count is nonnegative ASCII decimal')
                if int(row['k'])==0:require('t'in row,'zero-link actual file type required')
            if row.get('t')!='REG':continue
            require('k'in row,'complete actual regular-file link count required')
            if int(row['k'])!=0:continue
            require(all(k in row for k in('n','s','i','D','t'))and row['t']=='REG'and row['s'].isdigit(),'complete open-unlinked live size/inode/device required')
            name=row['n'];require(Path(name).is_absolute(),'complete actual open-unlinked name for namespace attribution required')
            if any(Path(name).is_relative_to(Path(root))for root in roots):
                key=(row['D'],row['i']);
                if key not in unlinked:total+=int(row['s']);unlinked_bytes+=int(row['s']);unlinked.add(key)
        if monitor is not None:monitor.remember_successful_scan(locals())
        return dict(complete_joint_HOCDE_bytes=total,open_unlinked_files=len(unlinked),open_unlinked_bytes=unlinked_bytes,actual_open_regular_paths=[r['n']for r in records if 'n'in r and r['n'].startswith('/')and (r.get('t')!='REG'or int(r['k'])>0)],live_own_processes_observed=sorted(selected),all_regular_and_open_unlinked_counted=True)
    except BaseException as error:
        if monitor is not None:
            try:monitor.joint_failure(locals(),error)
            except BaseException as recording_error:monitor.recording_errors.append(monitor_error(recording_error))
        raise

def guarded(runner,support,resources,folder,label,argv,deadline,budget,deck=None,marker=None):
    monitor=getattr(resources,'_failure_only_monitor',None)
    previous_deadline=None if monitor is None else monitor.stage_deadline
    if monitor is not None:monitor.stage_deadline=deadline
    try:
        budget();remaining=min(600,deadline-time.monotonic());require(remaining>0,'group600/whole1800 remaining')
        require(not os.path.lexists(folder/(label+'.log')),'fresh command log zero retry')
        runner.execute(folder,label,argv,remaining,deck=deck,marker=marker)
        watch_path=folder/(label+'.watchdog.json');watch=strict_json(watch_path.read_bytes())
        require(type(watch['pid'])is int and watch['pid']>0 and type(watch['returncode'])is int and watch['returncode']==0 and watch['command']==argv and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'genuine actual command closed zero and liveness cleanup')
        require(type(watch['sampled_peak_rss_mib'])in(int,float)and not isinstance(watch['sampled_peak_rss_mib'],bool)and math.isfinite(watch['sampled_peak_rss_mib'])and 0<=watch['sampled_peak_rss_mib']<512 and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and watch['rss_cap_mib']==512,'original actual own-child RSS/wall scope')
        require(runner.records[-1]['status']=='PASS','actual genuine PASS stage')
        budget();return dict(label=label,command=argv,actual_watchdog_pin=fullpin(watch_path,budget),actual_merged_stdout_stderr_pin=fullpin(folder/(label+'.log'),budget),actual_child_PID=watch['pid'],watchdog=watch)
    finally:
        if monitor is not None:monitor.stage_deadline=previous_deadline

def compile_all(native,index,observation_source,tools,runner,support,resources,budget):
    require(platform.system()=='Darwin'and platform.machine()=='arm64','exact original selected Makefile platform, no inferred compiler flags')
    original=frozen_sources(native,index,observation_source);generator,generator_pin=support.load(native/'script/make_depend.py',next(r['input_pin']['sha256']for r in original if r['relative_path']=='script/make_depend.py'),'axmat_observation_original_native_make_depend')
    sources={r['relative_path']:r['input_pin']for r in original};stages=[];archives={};all_objects=[]
    require(list(ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES)==['Ganlib','Utilib','Trivac','Dragon'],'all original component-specific recipe variables')
    for component in ('Ganlib','Utilib','Trivac','Dragon'):
        started=time.monotonic();deadline=started+600;folder=native/component/'src';recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES[component]
        library_dir=native/component/'lib/Darwin_arm64';library_dir.mkdir(parents=True)
        if recipe['lib_module']is not None:(native/recipe['lib_module']).mkdir(parents=True)
        require(not any(p.suffix in('.o','.a','.mod')for p in folder.iterdir()),'all native objects/archives/modules fresh; no old build reuse')
        c=sorted(folder.glob('*.c'));f90=[*sorted(folder.glob('*.f90')),*sorted(folder.glob('*.F90'))];f77_lower=sorted(folder.glob('*.f'));f77_upper=sorted(folder.glob('*.F'));f77=[*f77_lower,*f77_upper]
        # The original default generator excludes module-contained include files.
        ordered90=[Path(v)for v in generator.build_dependency_order([str(p)for p in f90])]
        objects_order=[p.with_suffix('.o')for p in [*c,*ordered90,*f77]]
        require(len(set(objects_order))==len(objects_order),'original object basename uniqueness')
        units=generator.build_units([str(p)for p in [*f90,*f77]]);module_source={u.module:Path(u.name)for u in units if u.module};by_source={Path(u.name):u for u in units};pending=[*c,*ordered90,*f77];commands=[];objects=[];completed=set()
        while pending:
            chosen=None
            for p in pending:
                uses=[]if p not in by_source else by_source[p].uses
                dependencies={module_source[m]for m in uses if m in module_source and module_source[m]!=p}
                if dependencies<=completed:chosen=p;break
            require(chosen is not None,'original native module dependencies must be acyclic; never guess ordering');pending.remove(chosen);p=chosen;budget();sp=fullpin(p,budget);obj=p.with_suffix('.o');require(not os.path.lexists(obj),'new object required')
            src=p
            if p.suffix in('.F','.F90'):
                src=p.with_suffix('.pp.f90'if p.suffix=='.F90'else'.pp.f');require(not os.path.lexists(src),'fresh actual preprocessor output')
                require(recipe['PREPRO']is not None,'original selected Makefile PREPRO undefined for this suffix; no invented tool')
                argv=[tools[recipe['PREPRO']]['path'],'-P','-W','-traditional',*recipe['FLAGS']]
                if p.suffix=='.F':argv+=recipe['FMPI']
                argv+=[str(p),str(src)]
                commands.append(guarded(runner,support,resources,folder,'preprocess_'+p.stem,argv,deadline,budget));preprocessed=fullpin(src,budget)
            else:preprocessed=None
            if p.suffix=='.c':
                require(recipe['C']is not None,'original selected Makefile C undefined, no invented compiler')
                argv=[tools[recipe['C']]['path'],*recipe['CFLAGS'],*recipe['FLAGS'],*recipe['opt'],*recipe['COMP'],'-c',str(src),'-o',str(obj)]
            else:
                flags=recipe['FFLAG77']if p.suffix in('.f','.F')else recipe['FFLAGS']
                argv=[tools[recipe['F90']]['path'],*flags,*recipe['opt'],*recipe['COMP'],*recipe['INCLUDE'],'-c',str(src),'-o',str(obj)]
            stage=guarded(runner,support,resources,folder,'compile_'+p.stem,argv,deadline,budget);op=fullpin(obj,budget);require(fullpin(p,budget)==sp,'compiler Source unchanged')
            retained_preprocessed=None
            if preprocessed is not None:
                retained=native.parent/'retained_preprocessor_Source'/component/src.name;retained.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,retained);retained_preprocessed=fullpin(retained,budget);require(retained_preprocessed['sha256']==preprocessed['sha256']and retained_preprocessed['size_bytes']==preprocessed['size_bytes'],'lossless exact actual preprocessed compiler input kept');src.unlink()
            row=dict(original_source_pin=sp,preprocessor_output_pin=preprocessed,retained_complete_preprocessor_Source_pin=retained_preprocessed,actual_compile=stage,new_object_pin=op);objects.append(row);all_objects.append(row);commands.append(stage);completed.add(p)
        require({x['new_object_pin']['path']for x in objects}==set(map(str,objects_order)),'all original library objects compiled exactly once')
        archive=folder/('lib'+component+'.a');argv=[tools['ar']['path'],'rcs',str(archive),*map(str,objects_order)];archive_stage=guarded(runner,support,resources,folder,'archive_'+component,argv,deadline,budget);ap=fullpin(archive,budget)
        for row in objects:recheck(row['new_object_pin'],budget)
        # Original ar emits src/lib*.a, then original cp places the same fresh
        # archive into each component's own lib directory used by final link.
        library_copy=library_dir/archive.name;require(not os.path.lexists(library_copy),'fresh original recipe library copy')
        shutil.copy2(archive,library_copy);library_copy_pin=fullpin(library_copy,budget)
        require(library_copy_pin['sha256']==ap['sha256']and library_copy_pin['size_bytes']==ap['size_bytes'],'original library copy full bytes equal actual fresh ar output')
        module_copy_pins=[]
        if recipe['module_copy']:
            modules=native/recipe['lib_module'];generated_modules=list(folder.glob('*.mod'))
            require(component!='Utilib'or bool(generated_modules),'original Utilib unguarded cp *.mod requires actual modules')
            for p in generated_modules:
                target=modules/p.name;require(not os.path.lexists(target),'original per-library module namespace fresh')
                shutil.copy2(p,target);module_copy_pins.append(dict(original_generated_module_pin=fullpin(p,budget),original_recipe_module_copy_pin=fullpin(target,budget)))
        # Trivac's original library recipe never copies module files.
        require(time.monotonic()-started<600,'entire library compile/archive group600 cap')
        archives[component]=library_copy_pin;stages.append(dict(component=component,exact_original_selected_recipe=recipe,original_recipe_library_copy_pin=library_copy_pin,original_recipe_module_copy_pins=module_copy_pins,archive_object_source_suffix_group_order=['.c','original_dependency_order(.f90_then_.F90)','.f','.F'],stage_wall_cap_seconds=600,elapsed_seconds=time.monotonic()-started,all_object_inputs_in_original_archive_order=[r for p in objects_order for r in objects if r['new_object_pin']['path']==str(p)],all_commands=commands,actual_archive_command=archive_stage,new_archive_pin=ap))
        require(frozen_sources(native,index,observation_source)==original,'complete native Source freeze after whole group')
    link_started=time.monotonic();exe=native/'Dragon/src/Dragon';dragon_o=native/'Dragon/src/DRAGON.o';require(not os.path.lexists(exe),'new final executable required')
    link_inputs=[fullpin(dragon_o,budget),*[archives[k]for k in('Dragon','Trivac','Utilib','Ganlib')]]
    link_recipe=ORIGINAL_DARWIN_ARM64_NATIVE_RECIPES['Dragon'];argv=[tools[link_recipe['F90']]['path'],*link_recipe['opt'],*link_recipe['COMP'],*[p['path']for p in link_inputs],*link_recipe['LFLAGS'],'-o',str(exe)];link=guarded(runner,support,resources,native/'Dragon/src','Dragon_link',argv,link_started+600,budget)
    ep=fullpin(exe,budget)
    for p in link_inputs:recheck(p,budget)
    for r in all_objects:recheck(r['new_object_pin'],budget)
    require(frozen_sources(native,index,observation_source)==original,'whole native Source-to-new-object/archive/link final freeze')
    evidence=dict(schema='ACTUAL_FROZEN_COMPLETE_NATIVE_SOURCE_OBJECT_ARCHIVE_LINK_EXECUTABLE_EVIDENCE_V1',source_only=False,frozen_all_compiled_and_include_Source=original,original_Source_index_pin=fullpin(index['_path'],budget),original_dependency_generator_pin=dict(generator_pin,size_bytes=generator_pin['identity'][4]),original_platform=dict(OS='Darwin',ARCH='arm64',openmp=0,mpi=0,hdf5=0,opt=['-O','-g']),stage_order=['Ganlib','Utilib','Trivac','Dragon','Dragon_link'],all_four_complete_library_build_stages=stages,actual_final_link_command=link,all_actual_link_input_pins=link_inputs,new_actual_executable_pin=ep,all_sources_objects_archives_checked_after_actual_link=True,no_old_binary_object_archive_used=True,compiler_descendant_RSS_scope_not_certified=True,original_own_child_guard_scope_preserved=True,whole5stage_executed=True,**FUTURE)
    return ep,evidence

def original_shared_libraries(b):
    libraries={}
    for state in ('A','B'):
        for row in b['states'][state]['native_stage_inputs']:
            if row['destination']in('DLIB_ACTUAL','DLIB8R1_370'):
                previous=libraries.get(row['destination'])
                require(previous is None or previous==row['input_pin'],'same complete original library source for A and B')
                libraries[row['destination']]=row['input_pin']
    require(list(libraries)==['DLIB_ACTUAL','DLIB8R1_370'],'both complete original library roles ordered')
    return libraries

def prepare_shared_libraries(out,b,budget):
    shared=out/SHARED_INPUT_LIBRARY_LAYOUT['shared_directory'];require(not os.path.lexists(shared),'fresh one-copy original library directory');shared.mkdir()
    originals=original_shared_libraries(b);copies={}
    for name,p in originals.items():
        recheck(p,budget);dest=shared/name
        with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
        actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'entire original library copied once without aliases');copies[name]=actual;recheck(p,budget)
    return dict(schema='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1',original_input_pins=originals,shared_copy_pins=copies,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,shared_library_directory=str(shared),all_library_bytes_preserved_without_symlinks_or_hardlinks=True,actual_state_library_full_EOF_observations={})

def recheck_shared_libraries(shared,budget):
    originals={name:recheck(p,budget)for name,p in shared['original_input_pins'].items()}
    copies={name:recheck(p,budget)for name,p in shared['shared_copy_pins'].items()}
    return dict(original_library_full_EOF_pins=originals,shared_library_full_EOF_pins=copies)

def derive_original_procedure(raw):
    require(type(raw)is bytes and len(raw)<=2**20,'small complete pinned procedure Source only')
    result=raw
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii')
        require(raw.count(old)==row['count']and raw.count(new)==0 and len(new.split(b"'")[1])<=64,'all and only original FIL literal occurrences fit actual NAMFIL64')
        result=result.replace(old,new)
    restored=result
    for row in SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements']:
        old=row['original'].encode('ascii');new=row['derived'].encode('ascii');require(restored.count(new)==row['count'],'derived complete FIL occurrence count');restored=restored.replace(new,old)
    require(restored==raw,'entire procedure reverse replacement exactly original Source bytes')
    return result

def copy_state_seeds(folder,seeds,shared,budget):
    require([row['destination']for row in seeds]==SHARED_INPUT_LIBRARY_LAYOUT['seed_destination_order'],'all seven original seed roles in original order')
    copies=[];mapping=[];procedure=None
    for row in seeds:
        p=row['input_pin'];name=row['destination'];recheck(p,budget);original_procedure_pin=None
        if name in('DLIB_ACTUAL','DLIB8R1_370'):
            require(p==shared['original_input_pins'][name],'same original library role source');actual=recheck(shared['shared_copy_pins'][name],budget)
        else:
            dest=folder/name;require(not os.path.lexists(dest),'fresh material seed Source')
            if name=='AxMatTone.c2m':
                original=folder/SHARED_INPUT_LIBRARY_LAYOUT['original_procedure_copy_name'];require(not os.path.lexists(original),'fresh retained complete original procedure')
                with Path(p['path']).open('rb')as src,original.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                original_procedure_pin=fullpin(original,budget);require(original_procedure_pin['sha256']==p['sha256']and original_procedure_pin['size_bytes']==p['size_bytes'],'complete original procedure independently retained')
                raw=original.read_bytes();derived=derive_original_procedure(raw)
                with dest.open('xb')as dst:dst.write(derived)
                actual=fullpin(dest,budget)
                procedure=dict(schema='ACTUAL_COMPLETE_ORIGINAL_PROCEDURE_THREE_FIL_LITERAL_PATH_REPLACEMENTS_V1',original_input_pin=p,retained_original_procedure_pin=original_procedure_pin,actual_consumed_derived_procedure_pin=actual,original_complete_ASCII_Source=raw.decode('ascii'),derived_complete_ASCII_Source=derived.decode('ascii'),exact_literal_replacements=SHARED_INPUT_LIBRARY_LAYOUT['literal_replacements'],whole_reverse_replacement_equals_original_bytes=True,all_numeric_and_non_FIL_Source_bytes_unchanged=True,actual_genuine_material_CWD=str(folder),relative_shared_library_targets={name:str((folder/('../shared_input_libraries/'+name)).resolve())for name in shared['shared_copy_pins']},ILIBRARYNAME_filename_provenance_changes_are_preserved_not_claimed_equal=True)
                require(procedure['relative_shared_library_targets']=={name:p['path']for name,p in shared['shared_copy_pins'].items()},'actual A/B relative file paths resolve only to original shared copies')
            else:
                with Path(p['path']).open('rb')as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                actual=fullpin(dest,budget);require(actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes'],'all other original seed Source bytes unchanged')
        copies.append(actual);mapping.append(dict(destination=name,original_input_pin=p,actual_consumed_pin=actual,retained_original_procedure_pin=original_procedure_pin))
        recheck(p,budget)
    require(procedure is not None,'complete original and actual consumed procedure evidence')
    copies.append(procedure['retained_original_procedure_pin'])
    return copies,mapping,procedure

def collect_state(folder,state,deck_pin,exe_pin,stage,budget):
    # Read headers in actual consecutive event number order, never native record
    # sorting. Every full event file reaches EOF in fullpin/extract_event.
    files={p.name:p for p in folder.glob('axobs-*')};events=[];snapshots=[];contexts=[];number=1;last_libmix=0;closed=[];all_observer_names=set()
    while True:
        name='axobs-'+format(number,'06d')+'.context.bin'
        if name not in files:break
        path=files[name];pp=fullpin(path,budget)
        with path.open('rb')as stream:
            require(stream.read(8)==b'AXOBSCTX','whole observer magic')
            raw=stream.read(16);require(len(raw)==16,'actual full event header');version,event,libmix,length=struct.unpack('<4i',raw)
            require(version==2 and event==number and libmix>=last_libmix and 1<=length<=256,'actual consecutive AXOBSCTXv2 event/libmix header')
            label=stream.read(length).decode('ascii');require(label in LABELS,'no unknown/omitted observer event')
        role=ROLE_LABELS.get(label);snapshot=None;all_observer_names.add(name);contexts.append(pp)
        if role is not None:
            n='axobs-'+format(event,'06d')+'-'+role+'.xsm'
            if n in files:
                snapshot=fullpin(files[n],budget);all_observer_names.add(n);snapshots.append(dict(event=event,role=role,root_prefix=[],logical_prefix=[]if role=='final-complete-micro'else['MACROLIB'],input_pin=snapshot))
            else:require(role not in('postmacro-LIBMIX','final-complete-micro'),'every postmacro and actual final micro snapshot mandatory')
        if label=='LIBMIX_BEFORE':require(libmix==last_libmix+1,'every actual LIBMIX begin counted')
        events.append(dict(event=event,libmix=libmix,label=label,complete_context_pin=pp,snapshot_role=role,actual_snapshot_pin=snapshot,actual_native_snapshot_root_prefix=[]if snapshot is not None else None,snapshot_logical_prefix=([]if role=='final-complete-micro'else['MACROLIB'])if snapshot is not None else None,actual_old_macro_absent_at_event=(role is not None and snapshot is None)))
        last_libmix=libmix;number+=1
    require(events and set(files)==all_observer_names,'full actual observer namespace no holes/unknown/leftover entries')
    require(any(e['label']=='TONDRV_FINAL_AFTER_SHIBA'for e in events)and any(e['label']=='TONDRV_ACTUAL_SPH_CALL_DECISION'for e in events),'complete final snapshot and true/false SPH decision events required')
    # The existing full context parser is separately bound/read by the context
    # host. Production manifest retains all bytes and original order now.
    outputs=[]
    for name in('material.xsm','microlib.ascii','macro.ascii','metadata.ascii'):outputs.append(fullpin(folder/name,budget))
    return dict(state=state,actual_material_deck_pin=deck_pin,actual_executable_pin=exe_pin,actual_genuine_material_stage=stage,actual_material_product_pins=outputs,actual_all_event_headers_in_original_execution_order=events,complete_context_pins=contexts,complete_state_snapshot_inputs=snapshots,legacy_context_source_snapshot_request_rows=[dict(event=item['event'],role=item['role'],root_prefix=item['logical_prefix'],input_pin=item['input_pin'])for item in snapshots],legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],selected_last_libmix_number=last_libmix,all_actual_events_and_snapshots_saved=True,actual_material_child_closed_before_manifest=True,all_producer_file_handles_closed_before_next_state=True,new_final_micro_from_actual_TONDRV_observer=True,native_snapshot_api_or_memory_bits_qualified=False,**FUTURE)


def monitor_error(error):
    return dict(type=type(error).__module__+'.'+type(error).__qualname__,repr=repr(error),
        complete_traceback=''.join(traceback.format_exception(type(error),error,error.__traceback__)))

def monitor_stream(value):
    # Preserve the exact object returned by the original text=True call. A
    # TimeoutExpired may instead carry partial bytes: never call those complete.
    if value is None or type(value)is str:return value
    if type(value)is bytes:return dict(original_type='bytes',base64=base64.b64encode(value).decode('ascii'))
    raise TypeError('unexpected actual subprocess stream type')

class FailureOnlyMonitorEvidence:
    """Failure evidence only; no accepted scan, cleanup, or new qualification.

    Every successful original monitor scan remains ephemeral. The original
    failed call is committed before any added PS query and is never rewritten.
    Disk checks refuse writes above the unchanged known byte caps. A failed
    original lsof leaves open-unlinked accounting unverified; a previous value
    is explicitly stale evidence, never a replacement passing observation.
    """
    def __init__(self,roots,tools,started,resources,base_history_check,dfreeze,efreeze):
        self.roots=tuple(map(Path,roots));self.host=self.roots[0];self.tools=tools
        self.started=started;self.resources=resources;self.base_history_check=base_history_check
        self.dfreeze=dfreeze;self.efreeze=efreeze;self.stage_deadline=None
        self.latest_joint=None;self.latest_original_scan=None;self.latest_failed_selection=[];self.events=0
        self.unpersisted=[];self.recording_errors=[];self.journal=None;self.originals=None
        self.host_created_only_for_failure=False
    def clock(self):
        now=time.monotonic();whole=CAPS['whole_seconds']-(now-self.started)
        stage=None if self.stage_deadline is None else self.stage_deadline-now
        return dict(whole_seconds_remaining=whole,stage_seconds_remaining=stage,
            whole_cap_satisfied=whole>0,stage_cap_satisfied=stage is None or stage>0,
            no_additional_time_budget=True)
    def disk_account(self,increment):
        require(type(increment)is int and increment>=0,'exact diagnostic byte increment')
        total=0;seen=set()
        for root in self.roots:
            if not root.exists():continue
            for p in root.rglob('*'):
                s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'diagnostic whole namespace noalias')
                if stat.S_ISDIR(s.st_mode):continue
                require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'diagnostic regular singlelink only')
                key=(s.st_dev,s.st_ino);require(key not in seen,'diagnostic no hardlink duplicate');seen.add(key);total+=s.st_size
        require(tree(self.roots[3])==self.dfreeze and tree(self.roots[4])==self.efreeze,'diagnostic never changes frozen D/E')
        history=self.base_history_check(self.resources)
        external=sum(p['size_bytes']for p in self.dfreeze['files']+self.efreeze['files'])
        previous_unlinked=0 if self.latest_joint is None else self.latest_joint['open_unlinked_bytes']
        require(total+previous_unlinked+increment<CAPS['joint_archive_bytes'],'diagnostic bytes within original joint2GiB; no new allowance')
        require(history['artifact_bytes']+external+previous_unlinked+increment<=CAPS['history_bytes'],'diagnostic bytes within original history96GiB')
        require(history['disk_free_bytes']-increment>=CAPS['free_floor_bytes'],'diagnostic bytes within original free8GiB floor')
        return dict(actual_regular_joint_bytes=total,additional_record_bytes=increment,
            previous_complete_open_unlinked_bytes=previous_unlinked,
            current_open_unlinked_verified=False,failed_scan_never_replaced_by_this_account=True,
            actual_original_history_check=history,external_D_E_bytes=external,clock=self.clock())
    def record(self,event):
        appended=False
        self.events+=1
        event=dict(schema='ACTUAL_N8_FAILURE_ONLY_MONITOR_EVENT_V1',sequence=self.events,
            actual_host_PID=os.getpid(),clock=self.clock(),**event)
        try:
            if not self.host.exists():
                self.disk_account(0);self.host.mkdir();self.host_created_only_for_failure=True
            require(self.host.is_dir()and not self.host.is_symlink(),'failure evidence actual fresh H')
            folder=self.host/'runtime';folder.mkdir(exist_ok=True)
            require(folder.is_dir()and not folder.is_symlink(),'failure evidence actual H runtime directory')
            target=folder/'ACTUAL_FAILURE_ONLY_MONITOR_EVENTS.jsonl'
            if target.exists():
                s=target.lstat();require(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and not target.is_symlink(),'failure journal noalias')
            else:require(not os.path.lexists(target),'failure journal fresh ordinary file')
            # Accounting precedes each real append; the journal itself belongs
            # to H and every later original/full postclose traversal counts it.
            raw=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
            account=self.disk_account(len(raw));event['actual_diagnostic_write_byte_account_before']=account
            raw=(json.dumps(event,ensure_ascii=False,allow_nan=False)+'\n').encode('utf-8')
            self.disk_account(len(raw))
            with target.open('ab')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
            appended=True;self.journal=target;self.disk_account(0)
        except BaseException as error:
            # Recording errors never swallow/replace the original guard or
            # cleanup exception. Unwritten raw is retained for the bounded
            # failure result, if the same original disk caps permit it.
            if not appended:self.unpersisted.append(event)
            self.recording_errors.append(dict(actual_record_appended=appended,recording_error=monitor_error(error)))
    def failure_ps(self,phase,business_pid=None):
        event=dict(event='additional_postfailure_PS_liveness',phase=phase,
            original_failed_selection=list(self.latest_failed_selection),business_child_PID=business_pid,
            original_selection_not_changed=True,used_to_accept_original_failure=False,
            observed=False,actual_argv=None,actual_returncode=None,actual_stdout=None,actual_stderr=None)
        try:
            timing=self.clock();remaining=timing['whole_seconds_remaining']
            if timing['stage_seconds_remaining']is not None:remaining=min(remaining,timing['stage_seconds_remaining'])
            require(remaining>0,'no additional diagnostic query after original whole/stage deadline')
            self.disk_account(0)
            argv=[self.tools['ps']['path'],'-axo','pid=,ppid=,pgid=']
            event['actual_argv']=argv
            observed=subprocess.run(argv,capture_output=True,text=True,timeout=min(2,remaining))
            event.update(observed=True,actual_returncode=observed.returncode,
                actual_stdout=observed.stdout,actual_stderr=observed.stderr,streams_complete=True)
            # This additional query is evidence only. Nonzero never qualifies
            # or repairs a failed scan; parsing cannot change any selected PID.
            if type(observed.returncode)is int and observed.returncode==0:
                rows=[]
                for line in observed.stdout.splitlines():
                    words=line.split();require(len(words)==3 and all(w.isdigit()for w in words),'complete actual failure-only PS three-column output')
                    rows.append(dict(pid=int(words[0]),ppid=int(words[1]),pgid=int(words[2])))
                targets=set(self.latest_failed_selection)
                if type(business_pid)is int and business_pid>0:targets.add(business_pid)
                event['actual_selected_or_child_rows']=[r for r in rows if r['pid']in targets]
                event['actual_child_process_group_rows']=[r for r in rows if type(business_pid)is int and r['pgid']==business_pid]
        except BaseException as error:
            event['observation_error']=monitor_error(error)
            if isinstance(error,(subprocess.TimeoutExpired,subprocess.CalledProcessError)):
                event.update(actual_stdout=monitor_stream(error.output),actual_stderr=monitor_stream(error.stderr),
                    streams_complete=False,actual_returncode=error.returncode if isinstance(error,subprocess.CalledProcessError)else None)
        self.record(event)
    def remember_successful_scan(self,frame):
        # One current observation in memory only. Replacement releases the
        # previous complete streams; no accumulated successful scan history.
        observed=frame['observed']
        self.latest_original_scan=dict(original_scan_started_monotonic=frame['monitor_scan_started'],
            original_scan_finished_monotonic=time.monotonic(),original_PS_argv=frame['ps_argv'],
            original_PS_PID=frame['ps_diagnostic_pid'],original_PS_returncode=frame['ps_returncode'],
            original_PS_stdout=frame['ps_stdout'],original_PS_stderr=frame['ps_stderr'],
            original_selected_PIDs=sorted(frame['selected']),original_lsof_argv=observed.args,
            original_lsof_returncode=observed.returncode,original_lsof_stdout=observed.stdout,
            original_lsof_stderr=observed.stderr,not_new_liveness_at_cleanup_time=True)
    def write_failure_result(self,path,value):
        # The complete original failure result and all added diagnostic bytes
        # are subject to the same disk caps. No partial result is substituted.
        raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode('utf-8')
        try:self.disk_account(len(raw))
        except BaseException as error:
            self.recording_errors.append(dict(failure_result_not_written=True,actual_recording_error=monitor_error(error)))
            print(json.dumps(dict(status='FAILED_DIAGNOSTIC_RESULT_NOT_WRITTEN_OR_QUALIFIED',
                actual_failure_result_write_error=monitor_error(error),complete_original_failure_result_retained_in_memory_only=True,
                new_instrumented_runtime_qualification=None),allow_nan=False),file=sys.stderr,flush=True)
            return
        try:
            write_new(path,value);self.disk_account(0)
        except BaseException as error:
            self.recording_errors.append(dict(actual_failure_result_write_error=monitor_error(error)))
            print(json.dumps(dict(status='FAILED_DIAGNOSTIC_RESULT_WRITE_OR_POSTWRITE_ACCOUNT_ERROR',
                actual_failure_result_write_error=monitor_error(error),new_instrumented_runtime_qualification=None),allow_nan=False),file=sys.stderr,flush=True)
        # Both cases leave the original exception pending in the caller.
    def joint_failure(self,frame,error):
        observed=frame.get('observed');ps_process=frame.get('ps_process')
        selected=frame.get('selected');self.latest_failed_selection=[]if selected is None else sorted(selected)
        ps_complete='ps_stdout'in frame and 'ps_stderr'in frame
        ps_stdout=frame.get('ps_stdout');ps_stderr=frame.get('ps_stderr')
        lsof_stdout=None if observed is None else observed.stdout;lsof_stderr=None if observed is None else observed.stderr
        if isinstance(error,(subprocess.TimeoutExpired,subprocess.CalledProcessError)):
            command=error.cmd
            if command==frame.get('ps_argv') and not ps_complete:ps_stdout=error.output;ps_stderr=error.stderr
            elif observed is None:lsof_stdout=error.output;lsof_stderr=error.stderr
        original_lsof_argv=None if selected is None else [self.tools['lsof']['path'],'-nP','-F','pfnsiDtk','-a','-p',','.join(map(str,sorted(selected)))]
        self.record(dict(event='original_joint_bytes_failure',original_error=monitor_error(error),
            original_scan_started_monotonic=frame.get('monitor_scan_started'),
            latest_prior_successful_original_scan=self.latest_original_scan,
            original_ps=dict(actual_argv=frame.get('ps_argv'),actual_diagnostic_PID=frame.get('ps_diagnostic_pid'),
                actual_returncode=frame.get('ps_returncode'),actual_stdout=monitor_stream(ps_stdout),actual_stderr=monitor_stream(ps_stderr),
                streams_complete=ps_complete,closed_returncode_cached=None if ps_process is None else ps_process.returncode),
            original_parent_chain_selected_PIDs=list(self.latest_failed_selection),
            original_lsof=dict(source_argv_for_actual_selected_PIDs=original_lsof_argv,
                actual_returned_argv=None if observed is None else observed.args,
                actual_returncode=None if observed is None else observed.returncode,
                actual_stdout=monitor_stream(lsof_stdout),actual_stderr=monitor_stream(lsof_stderr),streams_complete=observed is not None),
            original_text_mode_unchanged=True,no_strip_or_stream_truncation=True,
            N6_original_failed_lsof_raw_remains_unknown=True,
            original_scan_failure_still_raises=True))
        self.failure_ps('after_original_failed_joint_scan')
    def install_bounded_wrappers(self,runner):
        bounded=runner.bounded
        original_terminate_group=bounded.terminate_group
        original_finish_liveness_watchdog=bounded.finish_liveness_watchdog
        self.originals=(bounded,original_terminate_group,original_finish_liveness_watchdog)
        def terminate_group(process):
            active=sys.exc_info()[1];cleanup_error=None
            if active is not None:
                self.record(dict(event='before_original_terminate_group',original_active_exception=monitor_error(active),
                    actual_business_PID=process.pid,cached_business_returncode=process.returncode,
                    latest_prior_successful_original_scan=self.latest_original_scan,
                    original_object_captured_before_wrapping=True,cleanup_success_not_inferred=True))
                self.failure_ps('before_original_terminate_group',process.pid)
            try:return original_terminate_group(process)
            except BaseException as error:
                cleanup_error=error
                self.record(dict(event='original_terminate_group_exception',original_active_exception=None if active is None else monitor_error(active),
                    actual_cleanup_exception=monitor_error(error),actual_business_PID=process.pid,
                    cached_business_returncode=process.returncode,cleanup_success_not_inferred=True))
                raise
            finally:
                if active is not None or cleanup_error is not None:
                    self.record(dict(event='after_original_terminate_group',actual_business_PID=process.pid,
                        cached_business_returncode=process.returncode,original_delegate_returned=cleanup_error is None,
                        cleanup_success_not_inferred=True))
                    self.failure_ps('after_original_terminate_group',process.pid)
        def finish_liveness_watchdog(write_fd,watchdog):
            active=sys.exc_info()[1];cleanup_error=None
            if active is not None:
                self.record(dict(event='before_original_finish_liveness_watchdog',original_active_exception=monitor_error(active),
                    actual_watchdog_PID=watchdog.pid,actual_original_write_fd=write_fd,
                    cached_watchdog_returncode=watchdog.returncode,latest_prior_successful_original_scan=self.latest_original_scan,cleanup_success_not_inferred=True))
                self.failure_ps('before_original_finish_liveness_watchdog',watchdog.pid)
            try:return original_finish_liveness_watchdog(write_fd,watchdog)
            except BaseException as error:
                cleanup_error=error
                self.record(dict(event='original_finish_liveness_watchdog_exception',original_active_exception=None if active is None else monitor_error(active),
                    actual_cleanup_exception=monitor_error(error),actual_watchdog_PID=watchdog.pid,
                    cached_watchdog_returncode=watchdog.returncode,cleanup_success_not_inferred=True))
                raise
            finally:
                if active is not None or cleanup_error is not None:
                    self.record(dict(event='after_original_finish_liveness_watchdog',actual_watchdog_PID=watchdog.pid,
                        cached_watchdog_returncode=watchdog.returncode,original_delegate_returned=cleanup_error is None,
                        cleanup_success_not_inferred=True))
                    self.failure_ps('after_original_finish_liveness_watchdog',watchdog.pid)
        bounded.terminate_group=terminate_group
        bounded.finish_liveness_watchdog=finish_liveness_watchdog
    def restore_bounded_objects(self):
        if self.originals is not None:
            bounded,original_terminate_group,original_finish_liveness_watchdog=self.originals
            bounded.terminate_group=original_terminate_group
            bounded.finish_liveness_watchdog=original_finish_liveness_watchdog
    def summary(self,include_unpersisted=False):
        return dict(schema='ACTUAL_N8_FAILURE_ONLY_MONITOR_SUMMARY_V1',failure_event_count=self.events,
            journal_pin=None if self.journal is None else fullpin(self.journal),
            additional_recording_errors=list(self.recording_errors),
            unpersisted_complete_events=list(self.unpersisted)if include_unpersisted else [],
            original_successful_scan_raw_history_not_persisted=True,
            original_lsof_argv_and_single_strict_zero_timeout_unchanged=False,
            lsof_link_count_field_explicitly_added=True,
            lsof_selected_PID_and_FD_scope_strict_zero_timeout_and_full_stream_limits_unchanged=True,
            full_PS_pid_ppid_pgid_state_and_captured_union_explicitly_new=True,
            original_parent_chain_never_reduced_except_individually_proven_closed_owned_PIDs=True,
            three_bounded_callable_objects_and_two_private_methods_per_actual_owned_Popen_declared=True,
            actual_owner_scope_state=None if getattr(self.resources,'_exact_owner_observer',None)is None else self.resources._exact_owner_observer.summary(),
            original_bounded_Source_bytes_and_supervisor_classes_unchanged=True,
            original_exceptions_never_accepted_or_replaced_by_instrumentation=True,
            complete_failed_event_journal_persistence_verified=(self.recording_errors==[] and self.unpersisted==[]),
            original_watchdog_cleanup_flag_not_actual_cleanup_proof=True,
            host_created_only_for_failure_evidence=self.host_created_only_for_failure,
            original_caps=CAPS,actual_clock=self.clock(),
            diagnostic_source_contract_is_not_runtime_qualification=True,
            actual_required_new_monitor_controls_scope=getattr(self.resources,'_required_monitor_controls_scope',None),new_native_runtime_qualification=None,
            N6_original_failed_lsof_raw_remains_unknown=True)

def build_exact_owner_resources(support,roots5,tools,started,dfreeze,efreeze,history,genuine_modules):
    resource,full,production=genuine_modules
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'same actual original classes/MRO for production and controls')
    archive,receipts=map(Path,roots5[3:]);monitor=None
    class JointHistoryResources(resource.DynamicHistoryResources):
        def check(self):
            value=super().check()
            joint=joint_bytes(roots5,tools['lsof']['path'],tools['ps']['path'],monitor,getattr(self,'_exact_owner_observer',None),getattr(self,'_actual_control_barrier',None));require(joint['complete_joint_HOCDE_bytes']<2*2**30,'live full jointHOCDE including open-unlinked2GiB')
            require(tree(archive)==dfreeze and tree(receipts)==efreeze,'complete D/E and all directory/fullSource identities frozen while live')
            require(value['artifact_bytes']+sum(p['size_bytes']for p in dfreeze['files']+efreeze['files'])+joint['open_unlinked_bytes']<=96*2**30,'complete history plus external D/E')
            if monitor is not None:monitor.latest_joint=dict(joint)
            sink=getattr(self,'_actual_control_scan_sink',None)
            if sink is not None:
                require(self._exact_owner_observer is not None and self._exact_owner_observer.control_mode is True,'full raw sink only in actual controls mode')
                sink(joint,monitor.latest_original_scan,self._exact_owner_observer.summary())
            value.update(joint);return value
    resources=JointHistoryResources(support.ART,history,8*2**30,96*2**30,production.ResourceFailure)
    resources._genuine_full=full;resources._exact_owner_observer=None;resources._actual_control_barrier=None;resources._actual_control_scan_sink=None
    monitor=FailureOnlyMonitorEvidence(roots5,tools,started,resources,resource.DynamicHistoryResources.check,dfreeze,efreeze)
    resources._failure_only_monitor=monitor
    return resources,monitor

def attach_exact_owner_observer(runner,resources,monitor,stdlib_pin,started,deadline_getter,helper_source_pin,support,control_mode=False):
    recheck(helper_source_pin)
    module,actual=support.load(Path(helper_source_pin['path']),helper_source_pin['sha256'],'axmat_N8_exact_owner_scope_Source')
    require(actual=={k:helper_source_pin[k]for k in actual},'complete actual owner helper Source pin')
    observer=module.ExactOwnerScopeObserver(runner,resources,monitor,resources._genuine_full,stdlib_pin,started,deadline_getter,control_mode)
    observer.install_original_start_capture();resources._exact_owner_observer=observer
    return observer


def run(host_module,support,b,author,started):
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','UNREADY observation runtime refuses native action')
    scope=validate_request(b,author);host,out,control,archive,receipts=[Path(b['namespaces'][k])for k in('host','output','control','source','receipts')];roots5=(host,out,control,archive,receipts)
    require(len(set(roots5))==5 and not any(a.is_relative_to(z)for a in roots5 for z in roots5 if a!=z),'nonoverlapping H/O/C/D/E')
    require(all(p.is_absolute()and p!=support.ART and p.is_relative_to(support.ART)and all(not q.is_symlink()for q in(p,*p.parents))for p in(host,out,control)),'fresh ART H/O/C')
    require(all(p.is_absolute()and p!=support.BASE and p.is_relative_to(support.BASE)for p in(archive,receipts)),'complete Source/receipt D/E separately underB')
    require(not any(os.path.lexists(p)for p in(host,out,control)),'fresh native namespaces zero retry')
    dfreeze,efreeze=tree(archive),tree(receipts);inputs=b['original129_input_pins']+b['additional_actual_evidence_input_pins']+list(author.values())
    tool_roles_by_path={p['path']:role for role,p in b['tool_pins'].items()}
    for p in inputs:recheck(p,tool_role=tool_roles_by_path.get(p['path']))
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_observer_original619');resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_observer_original_ebbb');full,production=helper.modules();helper.guard_admission(full)
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'genuine unchanged supervisor classes/MRO/modules')
    genuine=[support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
    history=resource.history_roots([str(p)for p in(host,out,control,Path(support.OUT),Path(support.TERMINAL))],support.ART)
    resources,monitor=build_exact_owner_resources(support,roots5,b['tool_pins'],started,dfreeze,efreeze,history,(resource,full,production));runner=None;owner_observer=None
    resources._required_monitor_controls_scope=b['actual_required_monitor_controls_scope']
    def budget():require(time.monotonic()-started<1800,'whole observation build+A/B+closure1800 cap')
    try:
        before=resources.check();require(before['artifact_bytes']+2*2**30<96*2**30 and before['disk_free_bytes']-2*2**30>=8*2**30,'original history/free complete reserve')
        host.mkdir();out.mkdir();control.mkdir();(host/'runtime').mkdir();(host/'OBSERVATION_BUILD').mkdir();shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py');require(fullpin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original bounded guard Source bytes')
        runner=full.OwnRSSSerialExecutor(host,1800-(time.monotonic()-started),'OBSERVATION_BUILD',resources)
        require(type(runner)is full.OwnRSSSerialExecutor and runner.resources is resources and Path(runner.bounded.__file__).resolve()==host/'runtime/run_bounded_dragon.py','original genuine guarded runner')
        monitor.install_bounded_wrappers(runner)
        owner_observer=attach_exact_owner_observer(runner,resources,monitor,b['actual_required_monitor_controls_scope']['actual_stdlib_subprocess_Source_pin'],started,lambda:monitor.stage_deadline,author['owner_scope_helper'],support,control_mode=False)
        require(all(runner.env.get(k)=='1'for k in THREAD_KEYS),'all five actual one-thread env')
        runner.env['SPOT_AXMAT_OBSERVATION']='ADMITTED_SOURCE_ONLY'
        native=host/'native';native.mkdir();index=strict_json((archive/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json').read_bytes());index['_path']=str(archive/'COMPLETE_ORIGINAL_NATIVE_SOURCE_INDEX.json');members={r['relative_path']:r for r in index['members']}
        with tarfile.open(archive/'COMPLETE_ORIGINAL_NATIVE_COMPILE_SOURCE.tar.gz','r:gz')as t:
            require(len(t.getmembers())==len(members)and {m.name for m in t.getmembers()}==set(members),'whole original native Source archive unique indexed exact count')
            for member in t.getmembers():
                budget();require(member.isfile()and member.name in members and '..'not in Path(member.name).parts and not Path(member.name).is_absolute(),'only complete expected Source members')
                dest=native/member.name;dest.parent.mkdir(parents=True,exist_ok=True)
                with t.extractfile(member)as src,dest.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
                pp=fullpin(dest,budget);require(pp['sha256']==members[member.name]['full_original_Source_pin']['sha256']and pp['size_bytes']==members[member.name]['full_original_Source_pin']['size_bytes'],'all original Source fullEOF archive bytes')
        observer=archive/'OBSERVATION_SOURCE'
        for original,derived in [('LIBMIX.f','LIBMIX.observe.UNREADY.f'),('LIBDEN.f','LIBDEN.observe.UNREADY.f'),('TONDRV.f','TONDRV.context_observe.UNREADY.f'),('TONSPH.f','TONSPH.observe.UNREADY.f')]:
            require(fullpin(native/'Dragon/src'/original)['sha256']==members['Dragon/src/'+original]['full_original_Source_pin']['sha256'],'original physical source before observation overlay');(native/'Dragon/src'/original).write_bytes((observer/derived).read_bytes())
        shutil.copy2(observer/'AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90',native/'Dragon/src/AXMAT_CONTEXT_OBSERVATION_MOD.f90')
        ep,build=compile_all(native,index,observer,b['tool_pins'],runner,support,resources,budget);write_new(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',build);bp=fullpin(control/'ACTUAL_COMPLETE_NATIVE_SOURCE_BINARY_LINK_EVIDENCE.json',budget);states={};shared=prepare_shared_libraries(out,b,budget);resources.check()
        for state in('A','B'):
            budget();recheck(ep,budget);folder=out/state;folder.mkdir();seeds=b['states'][state]['native_stage_inputs'];seedCopies=[]
            shared_before=recheck_shared_libraries(shared,budget);seedCopies,seedMapping,procedureEvidence=copy_state_seeds(folder,seeds,shared,budget)
            resources.check();stage=guarded(runner,support,resources,folder,'material',[ep['path']],time.monotonic()+600,budget,deck='material.x2m',marker='AXMAT-MATERIAL-'+state+'-COMPLETE')
            for p in seedCopies:recheck(p,budget)
            shared_after=recheck_shared_libraries(shared,budget);require(shared_before==shared_after,'all original and shared library whole EOF7IDs unchanged across actual state')
            states[state]=collect_state(folder,state,b['states'][state]['original_material_deck_pin'],ep,stage,budget)
            states[state]['actual_material_seed_copy_pins']=seedCopies
            states[state]['actual_material_seed_role_mapping']=seedMapping;states[state]['actual_original_and_consumed_procedure_Source_evidence']=procedureEvidence
            shared['actual_state_library_full_EOF_observations'][state]=dict(before_actual_material_stage=shared_before,after_actual_material_stage=shared_after)
            recheck(ep,budget)
            # This block has no open stream/SQLite/native handle. All host pins
            # and snapshot reads have exited their with blocks before B starts.
            closure=resources.check();require(not any(Path(v).is_relative_to(folder)or Path(v).is_relative_to(Path(shared['shared_library_directory']))for v in closure['actual_open_regular_paths']),'all own process material state and shared library handles closed before next state');states[state]['actual_no_open_state_handles_observation']=closure;write_new(control/('ACTUAL_'+state+'_CLOSED_OBSERVATION_CAPTURE.json'),states[state]);resources.check()
        manifest=dict(schema='ACTUAL_COMPLETE_AXOBSCTXv2_AB_OBSERVATION_MANIFEST_V1',source_only=False,state_order=['A','B'],states=states,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,actual_shared_input_library_evidence=shared,complete_state_snapshot_inputs={k:v['complete_state_snapshot_inputs']for k,v in states.items()},complete_context_inputs={k:v['complete_context_pins']for k,v in states.items()},legacy_context_source_snapshot_request_rows={k:v['legacy_context_source_snapshot_request_rows']for k,v in states.items()},legacy_context_root_prefix_semantics='output_pool_logical_path_prefix_only_not_native_directory_lookup',actual_native_snapshot_root_prefix=[],all_A_handles_closed_before_B=True,actual_Source_binary_link_evidence_pin=bp,actual_observer_executable_pin=ep,independent_observation_Source_admission_pin=b['independent_observation_Source_admission_pin'],actual_Source_scope_coupling=scope,original_caps=CAPS,actual_material_build_and_observation_executed=True,Root_observed_tool_terminal=None,Root_postclose_coverage_contract=None,new_native_walker_controls_actual_run=None,new_complete_aggregation_controls_actual_run=None,actual_frozen_native_Source_object_link_exe_evidence_saved=True,**FUTURE)
        write_new(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',manifest);mp=fullpin(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json',budget)
        for p in inputs:recheck(p,budget,tool_role=tool_roles_by_path.get(p['path']))
        after=resources.check();require(tree(archive)==dfreeze and tree(receipts)==efreeze,'whole D/E final freeze');budget()
        value=dict(schema='ACTUAL_COMPLETE_NATIVE_OBSERVATION_BUILD_GENUINE_HOST_RESULT_V1',status='ACTUAL_COMPLETE_FIVE_STAGE_BUILD_AND_AB_OBSERVATION_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REQUIRED',source_only=False,actual_host_PID=os.getpid(),original_caps=CAPS,original_helper_pin=hpin,resource_factory_pin=rpin,genuine_guard_pins=genuine,supervisor_class_or_MRO_modified=False,own_child_RSS_scope_only=True,compiler_descendant_RSS_scope_not_certified=True,actual_build_evidence_pin=bp,actual_observation_manifest_pin=mp,all_stage_records=runner.records,complete_input_pins_before_and_after=inputs,complete_Source_D_freeze=dfreeze,complete_receipt_E_freeze=efreeze,resources_before=before,resources_after=after,whole_seconds=time.monotonic()-started,actual_Source_scope_coupling=scope,actual_Root_observed_terminal=None,actual_failure_only_monitor_evidence=monitor.summary(),**FUTURE)
        write_new(host/'result.json',value);resources.check();budget();print(json.dumps(dict(status=value['status'],actual_host_result_pin=fullpin(host/'result.json'),actual_observation_manifest_pin=mp,actual_build_evidence_pin=bp,actual_external_Root_typed_CLOSED_required=True,**FUTURE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():
            freeze_errors=[];after_inputs=[];after_D_E=None;after_resources=None
            for p in inputs:
                try:after_inputs.append(recheck(p,tool_role=tool_roles_by_path.get(p['path'])))
                except BaseException as e:freeze_errors.append(dict(path=p['path'],error=repr(e)))
            try:
                after_D_E=dict(Source=tree(archive),receipts=tree(receipts));require(after_D_E==dict(Source=dfreeze,receipts=efreeze),'failed complete D/E differs');after_resources=resources.check()
            except BaseException as e:freeze_errors.append(dict(scope='failed_D_E_and_resource',error=repr(e)))
            monitor.write_failure_result(host/'failed_host_result.json',dict(schema='FAILED_COMPLETE_NATIVE_OBSERVATION_BUILD_HOST_RESULT_V1',status='FAILED_NO_RETRY_NO_QUALIFICATION',error=repr(error),complete_input_pins_before=inputs,complete_input_pins_after_failure=after_inputs,complete_D_E_freeze_before=dict(Source=dfreeze,receipts=efreeze),complete_D_E_freeze_after_failure=after_D_E,full_postfailure_freeze_errors=freeze_errors,full_postfailure_freeze_checked=(freeze_errors==[]),actual_resources_after_failure=after_resources,all_stage_records=[]if runner is None else runner.records,actual_observation_manifest_pin_if_saved=fullpin(out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json')if (out/'ACTUAL_AB_AXOBSCTXv2_OBSERVATION_MANIFEST.json').is_file()else None,whole_seconds=time.monotonic()-started,original_caps=CAPS,actual_Root_observed_terminal=None,actual_failure_only_monitor_evidence=monitor.summary(include_unpersisted=True),**FUTURE))
        raise
    finally:
        try:
            if owner_observer is not None:owner_observer.restore_original_objects()
        finally:monitor.restore_bounded_objects()
