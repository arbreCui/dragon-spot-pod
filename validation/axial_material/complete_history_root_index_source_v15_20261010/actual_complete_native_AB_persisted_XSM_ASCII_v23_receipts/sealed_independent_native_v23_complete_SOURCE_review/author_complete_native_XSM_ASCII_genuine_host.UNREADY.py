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
SOURCE_STATUS = 'UNREADY_SOURCE_ONLY'
SOURCE_ARCHIVE = None
RECEIPTS = None
HOST = None
OUT = None
CONTROL = None
TARGET = None
TARGET_SHA = None
PROTOCOL = None
PROTOCOL_SHA = None
BINDING = None
BINDING_SHA = None
SOURCE_ADMISSION_SHA = None
ACTUAL_PROTOCOL_QUALIFICATION_SHA256 = None
ACTUAL_TRANSFER_QUALIFICATION_SHA256 = None
REACTION_MULTIPLICITY_QUALIFICATION_SHA256 = None
ACTUAL_SCIENTIFIC_REFERENCE_SHA256 = None
WHOLE_CAP,STAGE_CAP,RSS_CAP,ARCHIVE_CAP=1800,600,512,2*2**30
CAPS={'whole_seconds':1800,'stage_seconds':600,'rss_mib':512,'joint_archive_bytes':2*2**30,'history_bytes':96*2**30,'free_floor_bytes':8*2**30,'threads':1,'children_at_once':1,'retries':0}
FALSE={'actual_protocol_qualified':False,'actual_full_rawrecord_transfer_qualified':False,'original_XSM_memory_bits_verified':False,'reaction_multiplicity_verified':False,'physical_neutron_balance_qualified':False,'scientific_accuracy_qualified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False,'coupled_370group_reference_qualified':False,'native_transport_executed':False,'whole_combined_build_or_INPUT_qualified':False}

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


def typed_full_pin(expected):
    require(type(expected)is dict and set(expected)=={'path','sha256','size_bytes','identity'},'exact full native pin schema')
    require(type(expected['path'])is str and Path(expected['path']).is_absolute()and type(expected['sha256'])is str and len(expected['sha256'])==64 and all(c in '0123456789abcdef'for c in expected['sha256']),'exact absolute file and SHA')
    require(type(expected['size_bytes'])is int and expected['size_bytes']>=0 and type(expected['identity'])is list and len(expected['identity'])==7 and all(type(v)is int and v>=0 for v in expected['identity'])and expected['identity'][3]==1 and expected['identity'][4]==expected['size_bytes'],'typed size and7ID; bool/equalfloat forbidden')

def recheck_full_pin(support,expected):
    typed_full_pin(expected)
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
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile()is not None:
        raise ValueError('fixed unprofiled nonoptimized read-only native host required')
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and all(type(v)is str and bool(v)for v in(SOURCE_ARCHIVE,RECEIPTS,HOST,OUT,CONTROL,TARGET,TARGET_SHA,BINDING,BINDING_SHA,SOURCE_ADMISSION_SHA)),'UNREADY native host refuses runtime/API action')
    require(PROTOCOL is None and PROTOCOL_SHA is None and all(v is None for v in(ACTUAL_PROTOCOL_QUALIFICATION_SHA256,ACTUAL_TRANSFER_QUALIFICATION_SHA256,REACTION_MULTIPLICITY_QUALIFICATION_SHA256,ACTUAL_SCIENTIFIC_REFERENCE_SHA256)),'no fabricated new walker protocol or future success qualification')
    import hashlib
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:raise ValueError('fixed original normal support source required')
    spec=importlib.util.spec_from_file_location('axmat_v15_normal_readonly_admission_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    support_pin=support.pin(SUPPORT,SUPPORT_SHA)
    if any(os.environ.get(k)!='1'for k in support.THREAD_KEYS)or Path(sys.executable).resolve()!=support.PYTHON:raise ValueError('original single-thread Python required')
    host,out,control,archive,receipts,target,binding_path=map(Path,(HOST,OUT,CONTROL,SOURCE_ARCHIVE,RECEIPTS,TARGET,BINDING))
    require(all(p.is_absolute()and p!=support.ART and p.is_relative_to(support.ART)and '..'not in p.parts for p in(host,out,control,support.OUT,support.TERMINAL)),'strict five ART history roots; D/E separately counted')
    require(archive.is_relative_to(BASE)and receipts.is_relative_to(BASE)and archive!=BASE and receipts!=BASE,'Source D/receipt E outsideART within original B')
    roots5=(host,out,control,archive,receipts)
    require(len(set(roots5))==5 and not any(a.is_relative_to(b)for a in roots5 for b in roots5 if a!=b),'joint H/O/C/D/E roots distinct and nonoverlapping')
    if any(os.path.lexists(p)for p in(host,out,control)):raise ValueError('fresh native namespaces required; no retry')
    bpin=support.pin(binding_path,BINDING_SHA);b=strict_json(binding_path.read_bytes())
    require(b['schema']=='ROOT_ACTUAL_COMPLETE_NATIVE_XSM_ASCII_BINDING_V1'and b['source_only']is True and b['scientific_qualification_created']is False and b['Root_only_actual_execution']is True,'actual Root native Source-only binding')
    require(type(b['original_caps'])is dict and set(b['original_caps'])==set(CAPS)and all(type(v)is int for v in b['original_caps'].values())and b['original_caps']==CAPS,'exact original integer caps')
    require(b['namespaces']==dict(host=str(host),output=str(out),control=str(control),source=str(archive),receipts=str(receipts))and b['joint_archive_roots']==list(map(str,roots5))and b['state_order']==['A','B'],'full original serial state and joint namespace bindings')
    require(b['new_native_walker_controls_actual_run']is None and b['actual_native_byte_qualification_sha256']is None and b['actual_scientific_qualification_sha256']is None,'new controls and all future qualification unknown')
    require(b['source_admission_pin']['sha256']==SOURCE_ADMISSION_SHA,'actual Source admission SHA binding')
    require(type(b['complete_input_pins'])is list and len(b['complete_input_pins'])==129 and len({p['path']for p in b['complete_input_pins']})==129,'all original129 complete input pins')
    inputs=[support_pin,support.pin(Path(__file__).absolute()),support.pin(target,TARGET_SHA),bpin]
    for p in b['complete_input_pins']:inputs.append(recheck_full_pin(support,p))
    inputs.append(recheck_full_pin(support,b['source_admission_pin']))
    inputs.append(recheck_full_pin(support,b['actual_Root_Source_admission_tool_return_pin']))
    inputs.append(recheck_full_pin(support,b['independent_host_binder_Source_review_pin']))
    inputs.append(recheck_full_pin(support,b['prior_actual_V22_build_tool_return_pin']))
    prior=actual_closed_prior(b['prior_actual_V22_build_tool_return_pin'])
    expected_sources=b['actual_author_Source_contract']
    require(type(expected_sources)is dict and set(expected_sources)=={'qualified_source_manifest','host_template','checker_template','binder'},'all four exact original author Source contract pins required')
    for p in expected_sources.values():inputs.append(recheck_full_pin(support,p))
    source_truth=actual_closed_prior(b['actual_Root_Source_admission_tool_return_pin'],True,'ROOT_ACTUAL_COMPLETE_NATIVE_SOURCE_ADMISSION_TOOL_TERMINAL_RETURN_V1')
    scope_coupling=source_scope_contract(b,expected_sources,source_truth)
    require(scope_coupling==b['actual_Source_scope_coupling'],'all Source admission/peer coupling equals actual binder record')
    source_inputs=complete_source_inputs(support,archive);receipt_inputs=complete_source_inputs(support,receipts)
    source_directories=complete_directory_identity(archive);receipt_directories=complete_directory_identity(receipts)
    inputs+=source_inputs+receipt_inputs
    inputs=list({entry['path']:entry for entry in inputs}.values())
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,)or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:raise ValueError('unchanged genuine supervisor required')
    genuine_pins=[support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
    roots=resource.history_roots([str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:raise ValueError('complete original resource reserve required')
        require(support.archive_bytes(roots5)<ARCHIVE_CAP,'complete H/O/C/D/E before reserve')
        host.mkdir();control.mkdir()
        for name in('runtime','native_run','COMPLETE_NATIVE_XSM_ASCII'):(host/name).mkdir()
        support.write_new(control/'NEW_NATIVE_WALKER_CONTROLS_NOT_EXECUTED.json',dict(source_only=False,new_native_walker_controls_actual_run=None,not_a_protocol_PASS=True,historical_raw_protocol5_positive10_reject_is_saved_separate_scope=True,**FALSE))
        shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
        require(support.pin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original bounded runtime full bytes')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole native host budget exhausted')
        runner=full.OwnRSSSerialExecutor(host,remaining,'COMPLETE_NATIVE_XSM_ASCII',resources)
        if type(runner)is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=host/'runtime/run_bounded_dragon.py':raise ValueError('genuine runner binding required')
        host_pid=os.getpid()
        command=[str(support.PYTHON),'-B',str(target),'--binding',str(binding_path),'--binding-sha256',BINDING_SHA,'--output-dir',str(out),'--expected-parent-pid',str(host_pid)]
        runner.execute(host/'native_run','native_xsm_ascii',command,STAGE_CAP)
        stage,report=observed_stage(support,runner,host/'native_run','native_xsm_ascii',command,out/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json',host_pid)
        require(report['schema']=='ACTUAL_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_BIT_EVIDENCE_ONLY_V1'and report['source_binding']['sha256']==BINDING_SHA and report['original_caps']==CAPS and report['native_persisted_XSM_value_bits_verified']is True,'actual complete persisted-native byte comparison only')
        require([row['state']for row in report['states']]==['A','B']and report['all_complete_state_scope_retained']is True,'complete A release then B required')
        for row in report['states']:
            macro,micro=row['complete_MACROLIB'],row['complete_MICROLIB']
            require(type(macro['records'])is int and macro['records']==19619 and macro['physical_headers_including_all_closes']==19990 and macro['numeric_components']==2264113,'full original macro scope')
            require(row['native_persisted_XSM_value_bits_verified']is True and all(v['all_persisted_native_value_bits_equal_ASCII']is True and v['native_physical_preorder_equal_original_ASCII']is True and v['all_complete_orders_preserved_on_disk']is True for v in(macro,micro)),'full original micro/macro type/order/value bits')
        require(len(runner.records)==1 and runner.records[0]['status']=='PASS','one genuine serial native stage; no retry')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes(roots5)
        if not math.isfinite(elapsed)or not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged native host caps exceeded')
        for entry in inputs+[hpin,rpin,*genuine_pins]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        require(complete_source_inputs(support,archive)==source_inputs and complete_source_inputs(support,receipts)==receipt_inputs and complete_directory_identity(archive)==source_directories and complete_directory_identity(receipts)==receipt_directories,'complete frozen D/E Source and directories unchanged')
        value=dict(schema='CURRENT150_AB_GENUINE_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_HOST_V1',status='ACTUAL_SAVED_COMPLETE_NATIVE_PERSISTED_BYTE_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED',actual_host_PID=host_pid,input_sources=inputs,original_helper=hpin,resource_factory=rpin,genuine_guard_sources=genuine_pins,actual_native=stage,stage_records=runner.records,resources_before=before,resources_after=after,history_roots=roots,source_and_receipts_outsideART_counted_separately=True,complete_source_freeze=source_inputs,complete_source_directory_freeze=source_directories,complete_receipt_input_freeze=receipt_inputs,complete_receipt_directory_freeze=receipt_directories,whole_seconds=elapsed,archive_before_result_bytes=archived,archive_roots=list(map(str,roots5)),original_caps=CAPS,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,actual_software_payload_saved=True,native_persisted_XSM_value_bits_verified=True,original_native_build_binary_Source_linkage_qualified=False,new_native_walker_controls_actual_run=None,historical_raw_protocol_is_not_new_native_protocol_qualification=True,prior_actual_V22_build_terminal=prior,actual_Source_scope_coupling=scope_coupling,actual_author_Source_contract=expected_sources,external_actual_Root_typed_EXIT0_CLOSED_required=True,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,**FALSE)
        support.write_new(host/'result.json',value)
        if support.archive_bytes(roots5)>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final native host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(host/'result.json'),actual_external_Root_terminal_required=True,**FALSE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():
            saved=out/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json'
            support.write_new(host/'failed_host_result.json',dict(status='FAILED_COMPLETE_NATIVE_BYTE_CHECK_NO_RETRY_NO_QUALIFICATION',error=repr(error),stage_records=[]if runner is None else runner.records,actual_native_report_pin_if_saved=support.pin(saved)if saved.is_file()and not saved.is_symlink()else None,whole_seconds=time.monotonic()-started,new_native_walker_controls_actual_run=None,native_persisted_XSM_value_bits_verified=False,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,original_native_build_binary_Source_linkage_qualified=False,**FALSE))
        raise


if __name__=='__main__':main()
