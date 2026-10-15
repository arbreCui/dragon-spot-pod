"""UNREADY SOURCE: complete native persisted-byte stage under the original genuine guard.

Root must first bind actual source/material receipts and independently review
the bound READY Source. This host never certifies XSM memory bits, physical
reaction balance, a coupled reference, AAA or ABA. No import-time execution.
The original619/705/38de/bc4/ebbb guard modules/classes/MRO are not replaced.
"""
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import stat
import sys
import time
BASE=Path('/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010')
SUPPORT=BASE/'actual_prepare_sources/prepare_cli_host_v15.py'
SUPPORT_SHA='3c1856f8ec16414d4f07fe4d88b3be2b859b1eb64d0c2624c9c7015c1b9a52a7'
SOURCE_STATUS = 'READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'
SOURCE_ARCHIVE = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v7_sources'
RECEIPTS = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v7_receipts'
HOST = '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v7-host-20261010'
OUT = '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v7-runtime-20261010'
CONTROL = '/Users/wen/spot/validation/artifacts/axial-material-complete-native-observation-BUILD5-AB-v7-control-20261010'
TARGET = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v7_sources/Root_bound_complete_observation_runtime.py'
TARGET_SHA = '7cb8edd866ef25f88fcd6b0e0cb5d094f05e115e21b2d5aab10b33fb94fcf8ec'
PROTOCOL = None
PROTOCOL_SHA = None
BINDING = '/Users/wen/spot/validation/axial_material/complete_history_root_index_source_v15_20261010/actual_complete_native_observation_BUILD5_AB_v7_sources/Root_actual_observation_SOURCE_binding.json'
BINDING_SHA = 'e719f469430c2aaee7d941ca66e29acd4a510e086727b5be097f1ba33be501cd'
SOURCE_ADMISSION_SHA = 'bb8c46813c21ad72225b1822905352e9e0944096f1af1500f1c5ae6baafa0c31'
ACTUAL_PROTOCOL_QUALIFICATION_SHA256 = None
ACTUAL_TRANSFER_QUALIFICATION_SHA256 = None
REACTION_MULTIPLICITY_QUALIFICATION_SHA256 = None
ACTUAL_SCIENTIFIC_REFERENCE_SHA256 = None
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
FALSE={'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'whole_combined_build_or_INPUT_qualified':False}

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
        for k,v in items:require(k not in d,'duplicate full host metadata key');d[k]=v
        return d
    def reject(value):raise ValueError('nonfinite metadata literal '+value)
    value=json.loads(raw,object_pairs_hook=pairs,parse_constant=reject)
    def finite(v):
        if type(v)is dict:return all(finite(x)for x in v.values())
        if type(v)is list:return all(finite(x)for x in v)
        return type(v)is not float or math.isfinite(v)
    require(finite(value),'all host/report/watch/scale metadata must remain finite');return value

def complete_source_inputs(support,path):
    require(path.is_dir()and not path.is_symlink(),'complete frozen source or receipt namespace required')
    rows=[]
    for p in sorted(path.rglob('*')):
        s=p.lstat();require(not stat.S_ISLNK(s.st_mode),'no complete Source namespace aliases')
        if stat.S_ISDIR(s.st_mode):continue
        require(stat.S_ISREG(s.st_mode)and s.st_nlink==1,'no omitted special/source hardlink entry');rows.append(support.pin(p))
    return rows

def observed_stage(support,runner,folder,label,command,report_path,host_pid):
    log=folder/(label+'.log');watch_path=folder/(label+'.watchdog.json')
    watch=strict_json(watch_path.read_bytes());report=strict_json(report_path.read_bytes());returned=strict_json(log.read_bytes())
    require(type(watch['pid'])is int and type(watch['returncode'])is int and watch['returncode']==0 and watch['command']==command and watch['limit_failure']is None and watch['own_child_only']is True and watch['liveness_group_cleanup']is True,'actual own genuine watchdog exact command/return/cleanup')
    require(type(watch['sampled_peak_rss_mib'])in(int,float)and not isinstance(watch['sampled_peak_rss_mib'],bool)and math.isfinite(watch['sampled_peak_rss_mib'])and 0<=watch['sampled_peak_rss_mib']<RSS_CAP,'real finite genuine own child peak below512')
    require(type(watch['elapsed_seconds'])in(int,float)and not isinstance(watch['elapsed_seconds'],bool)and math.isfinite(watch['elapsed_seconds'])and 0<=watch['elapsed_seconds']<watch['wall_cap_seconds']<=STAGE_CAP and watch['rss_cap_mib']==RSS_CAP,'unchanged600 stage upper bound/512 caps')
    require(type(report['actual_child_PID'])is int and report['actual_child_PID']==watch['pid']and type(report['actual_parent_PID'])is int and report['actual_parent_PID']==host_pid,'saved actual PID binding to genuine watch/host')
    require(returned['status']==report['status']and returned['report']['path']==str(report_path)and returned['report']['sha256']==support.pin(report_path)['sha256']and returned['report']['identity']==support.pin(report_path)['identity'],'honest full merged child stdout/stderr matches actual saved report pin')
    require(report['genuine_supervisor_watch_verified_here']is False and all(report[k]is False for k in ('scientific_accuracy_qualified','physical_neutron_balance_qualified','AAA_accuracy_qualified','ABA_admitted')),'software child cannot certify parent resources or scientific gates')
    require(runner.records[-1]['status']=='PASS','real stage PASS record required')
    return {'label':label,'command':command,'report':support.pin(report_path),'actual_merged_child_stdout_and_stderr':support.pin(log),'child_separate_stderr_saved':False,'watchdog_file':support.pin(watch_path),'watchdog':watch,'actual_child_PID_equals_watch_PID':True,'actual_parent_PID_equals_host_PID':True},report


def typed_full_pin(expected,tool_role=None):
    require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact full native pin schema')
    require(type(expected['path'])is str and Path(expected['path']).is_absolute()and type(expected['sha256'])is str and len(expected['sha256'])==64 and all(c in '0123456789abcdef'for c in expected['sha256']),'exact absolute file and SHA')
    require(type(expected['size_bytes'])is int and expected['size_bytes']>=0 and type(expected['identity'])is list and len(expected['identity'])==7 and all(type(v)is int and v>=0 for v in expected['identity'])and source_tool_nlink_allowed(expected['path'],expected['identity'][3],tool_role)and expected['identity'][4]==expected['size_bytes'],'typed size and7ID; bool/equalfloat forbidden')

def recheck_full_pin(support,expected,tool_role=None):
    typed_full_pin(expected,tool_role=tool_role)
    actual=support.pin(expected['path'],expected['sha256'])
    require(actual=={key:expected[key]for key in actual}and actual['identity'][4]==expected['size_bytes'],'complete native full EOF SHA7ID input differs')
    return actual

def complete_directory_identity(path):
    require(path.is_dir()and not path.is_symlink(),'real complete namespace root')
    return {str(p):[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]for p in [path,*sorted(path.rglob('*'))]if (s:=p.lstat())and stat.S_ISDIR(s.st_mode)}

def actual_closed_prior(pin_value, zero=False, expected_schema='ROOT_V22_ACTUAL_COMPLETE_BUILD_TOOL_TERMINAL_RETURN_V1'):
    typed_full_pin(pin_value)
    value=strict_json(Path(pin_value['path']).read_bytes())
    require(type(value)is dict and value['schema']==expected_schema
            and value['closed']is True and value['observed_terminal']is True
            and value['session_repolled_after_close']is False,
            'prior Root actual observed CLOSED family required; PREP cannot stand for BUILD')
    actual=value['terminal_tool_return']
    require(type(actual)is dict and type(actual['exit_code'])is int and 'session_id'not in actual
            and type(actual['chunk_id'])is str and bool(actual['chunk_id'])
            and type(value['actual_terminal_chunk'])is str and value['actual_terminal_chunk']==actual['chunk_id'],
            'prior Root exact observed typed CLOSED tool truth required; any honest build exit allowed')
    require(not zero or actual['exit_code']==0,'actual Root Source admission typedzero required')
    return value


def source_scope_contract(request, expected_sources, source_truth):
    for expected in expected_sources.values():typed_full_pin(expected)
    peer=strict_json(Path(request['independent_host_binder_Source_review_pin']['path']).read_bytes())
    require(type(peer)is dict and peer['schema']=='INDEPENDENT_COMPLETE_NATIVE_GENUINE_HOST_BINDER_SOURCE_REVIEW_V1'
            and peer['status']=='SOURCE_ONLY_PASS_NO_EXECUTION_OR_SCIENCE'
            and peer['source_only']is True and peer['all_checks_passed']is True
            and type(peer['blockers'])is list and peer['blockers']==[],
            'actual independent full native host/binder Source review scope required')
    checks=peer['checks']
    require(type(checks)is list and type(peer['check_count'])is int and peer['check_count']==len(checks)>0
            and all(type(row)is dict and set(row)=={'check','passed'}
                    and type(row['check'])is str and bool(row['check'])and row['passed']is True for row in checks)
            and len({row['check']for row in checks})==len(checks),
            'all independent Source checks retained, exact count and typed PASS')
    admission=strict_json(Path(request['source_admission_pin']['path']).read_bytes())
    require(type(admission)is dict and admission['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_HOST_BINDER_SOURCE_ADMISSION_V1'
            and admission['status']=='SOURCE_ONLY_ADMITTED_NOT_RUNTIME_OR_SCIENCE'
            and admission['source_only']is True and admission['scientific_qualification_created']is False
            and admission['actual_native_byte_qualification_sha256']is None
            and admission['actual_scientific_qualification_sha256']is None,
            'actual Root Source admission must retain software-only scope and unknown qualifications')
    for key,expected in expected_sources.items():
        typed_full_pin(peer[key]);typed_full_pin(admission[key])
        require(peer[key]==expected and admission[key]==expected,
                'peer/admission fullpin must match actual complete author manifest and each Source body: '+key)
    typed_full_pin(admission['independent_Source_review_pin'])
    require(admission['independent_Source_review_pin']==request['independent_host_binder_Source_review_pin'],
            'Source admission must bind this same independently reviewed Source report')
    output=strict_json(source_truth['terminal_tool_return']['output'])
    require(type(output)is dict and output['source_only']is True
            and output['status']=='ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_ONLY_NOT_RUNTIME_OR_SCIENCE',
            'genuine actual Source admission output scope required')
    typed_full_pin(output['source_admission_pin'])
    require(output['source_admission_pin']==request['source_admission_pin'],
            'actual Source admission tool output fullpin must equal actual admission record')
    return dict(schema='ACTUAL_COMPLETE_NATIVE_SOURCE_SCOPE_COUPLING_V1',source_only=True,
                all_four_actual_author_Source_fullpins_coupled=True,independent_full_Source_checks_count=len(checks),
                Source_admission_actual_tool_output_fullpin_coupled=True,PREP_is_not_BUILD=True,
                actual_Source_admission=request['source_admission_pin'],
                actual_independent_Source_review=request['independent_host_binder_Source_review_pin'],
                actual_author_Source_contract=expected_sources)


def main():
    started=time.monotonic()
    require(len(sys.argv)==1 and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE') and sys.getprofile()is None,'fixed unprofiled nonoptimized genuine observation host')
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and all(type(v)is str and bool(v)for v in(SOURCE_ARCHIVE,RECEIPTS,HOST,OUT,CONTROL,TARGET,TARGET_SHA,BINDING,BINDING_SHA,SOURCE_ADMISSION_SHA)),'UNREADY Source refuses any runtime/native action')
    require(PROTOCOL is None and PROTOCOL_SHA is None and all(v is None for v in(ACTUAL_PROTOCOL_QUALIFICATION_SHA256,ACTUAL_TRANSFER_QUALIFICATION_SHA256,REACTION_MULTIPLICITY_QUALIFICATION_SHA256,ACTUAL_SCIENTIFIC_REFERENCE_SHA256)),'all future science/native qualifications unknown')
    import hashlib
    require(hashlib.sha256(SUPPORT.read_bytes()).hexdigest()==SUPPORT_SHA,'original complete genuine support Source')
    spec=importlib.util.spec_from_file_location('axmat_original_observation_support',SUPPORT);support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    require(Path(support.__file__).resolve()==SUPPORT.resolve()and all(os.environ.get(k)=='1'for k in support.THREAD_KEYS)and Path(sys.executable).resolve()==support.PYTHON and os.environ.get('SPOT_AXMAT_OBSERVATION')=='ADMITTED_SOURCE_ONLY','original Python and all five thread variables1 plus admitted observer env')
    support.pin(SUPPORT,SUPPORT_SHA);support.pin(BINDING,BINDING_SHA);b=strict_json(Path(BINDING).read_bytes())
    require(b['namespaces']==dict(host=HOST,output=OUT,control=CONTROL,source=SOURCE_ARCHIVE,receipts=RECEIPTS)and b['independent_observation_Source_admission_pin']['sha256']==SOURCE_ADMISSION_SHA,'whole actual Root namespace/admission binding')
    target_pin=support.pin(TARGET,TARGET_SHA);require(b['bound_runtime_pin']==dict(target_pin,size_bytes=target_pin['identity'][4]),'exact complete bound runtime Source pin')
    runtime,runtime_pin=support.load(Path(TARGET),TARGET_SHA,'axmat_Root_bound_observation_runtime')
    require(runtime.SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED','bound runtime status exact')
    runtime.run(sys.modules[__name__],support,b,b['actual_author_Source_contract'],started)


if __name__=='__main__':main()
