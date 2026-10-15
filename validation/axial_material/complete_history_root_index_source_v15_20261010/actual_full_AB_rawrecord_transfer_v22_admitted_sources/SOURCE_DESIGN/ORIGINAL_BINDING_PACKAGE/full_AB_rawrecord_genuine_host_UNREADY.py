"""UNREADY SOURCE: two serial software stages under the original genuine guard.

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
SOURCE_STATUS = None
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

def main():
    started=time.monotonic()
    if len(sys.argv)!=1 or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or sys.getprofile() is not None:
        raise ValueError('fixed unprofiled nonoptimized read-only admission host required')
    require(SOURCE_STATUS=='READY_SOURCE_REVIEWED_ROOT_ACTUAL_BINDING_REQUIRED'and all(type(v)is str and bool(v)for v in(SOURCE_ARCHIVE,RECEIPTS,HOST,OUT,CONTROL,TARGET,TARGET_SHA,PROTOCOL,PROTOCOL_SHA,BINDING,BINDING_SHA,SOURCE_ADMISSION_SHA)),'UNREADY normal host refuses every runtime/API action')
    require(all(v is None for v in(ACTUAL_PROTOCOL_QUALIFICATION_SHA256,ACTUAL_TRANSFER_QUALIFICATION_SHA256,REACTION_MULTIPLICITY_QUALIFICATION_SHA256,ACTUAL_SCIENTIFIC_REFERENCE_SHA256)),'future runtime/scientific success pins remain None')
    import hashlib
    if hashlib.sha256(SUPPORT.read_bytes()).hexdigest()!=SUPPORT_SHA:
        raise ValueError('fixed normal support source required')
    spec=importlib.util.spec_from_file_location('axmat_v15_normal_readonly_admission_support',SUPPORT)
    support=importlib.util.module_from_spec(spec);sys.modules[spec.name]=support;spec.loader.exec_module(support)
    support_pin=support.pin(SUPPORT,SUPPORT_SHA)
    if any(os.environ.get(k)!='1' for k in support.THREAD_KEYS) or Path(sys.executable).resolve()!=support.PYTHON:
        raise ValueError('original single-thread Python required')
    host,out,control,archive,receipts,target,protocol,binding_path=map(Path,(HOST,OUT,CONTROL,SOURCE_ARCHIVE,RECEIPTS,TARGET,PROTOCOL,BINDING))
    require(all(p.is_absolute()and p!=support.ART and p.is_relative_to(support.ART)and '..'not in p.parts for p in(host,out,control,support.OUT,support.TERMINAL)),'strict five ART history roots; D/E never history roots')
    require(archive.is_relative_to(BASE)and receipts.is_relative_to(BASE)and archive!=BASE and receipts!=BASE,'outsideART Source/receipts retained separately in joint archive')
    if any(os.path.lexists(p) for p in (host,out,control)):raise ValueError('fresh combined software transfer namespaces required; no retry')
    bpin=support.pin(binding_path,BINDING_SHA);b=strict_json(binding_path.read_bytes())
    require(b['schema']=='ROOT_ACTUAL_CURRENT150_AB_FULL_RAWRECORD_TRANSFER_SOURCE_BINDING_V1'and b['source_only']is True and b['scientific_qualification_created']is False and b['source_qualification_sha256']==SOURCE_ADMISSION_SHA and b['original_caps']==CAPS,'true Root Source/material binding with original caps')
    require(b['namespaces']=={'source':str(archive),'receipts':str(receipts),'host':str(host),'transfer':str(out),'protocol':str(control)}and b['full_default_retention']is True,'one-use Root namespace/default-full binding')
    inputs=[support_pin,support.pin(Path(__file__).absolute()),support.pin(target,TARGET_SHA),support.pin(protocol,PROTOCOL_SHA),bpin]
    for p in b['input_pins']:
        entry=support.pin(p['path'],p['sha256']);require(entry['identity']==p['identity']and entry['identity'][4]==p['size_bytes'],'all true Root source/material fullSHA7ID');inputs.append(entry)
    source_inputs=complete_source_inputs(support,archive);receipt_inputs=complete_source_inputs(support,receipts);inputs+=source_inputs+receipt_inputs
    inputs=list({entry['path']:entry for entry in inputs}.values())
    helper,hpin=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'axmat_v15_admission_original619')
    resource,rpin=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'axmat_v15_admission_real_resource_module')
    full,production=helper.modules();helper.guard_admission(full)
    if full.OwnRSSSerialExecutor.__bases__!=(production.SerialExecutor,) or Path(full.__file__).resolve()!=support.FULL or Path(production.__file__).resolve()!=support.PARENT:
        raise ValueError('unchanged genuine supervisor required')
    genuine_pins=[support.pin(support.FULL,support.FULL_SHA),support.pin(support.PARENT,support.PARENT_SHA),support.pin(support.BOUNDED,support.BOUNDED_SHA)]
    roots=resource.history_roots([str(host),str(out),str(control),str(support.OUT),str(support.TERMINAL)],support.ART)
    resources=resource.DynamicHistoryResources(support.ART,roots,8*2**30,96*2**30,production.ResourceFailure)
    runner=None
    try:
        before=resources.check()
        if before['artifact_bytes']+ARCHIVE_CAP>=96*2**30 or before['disk_free_bytes']-ARCHIVE_CAP<8*2**30:
            raise ValueError('complete original resource reserve required')
        joint_paths=(host,out,control,archive,receipts)
        require(support.archive_bytes(joint_paths)<ARCHIVE_CAP,'complete HOST+OUT+CONTROL+D+E before reserve')
        host.mkdir()
        for name in ('runtime','protocol_run','transfer_run','FULL_RAWRECORD_TRANSFER'):(host/name).mkdir()
        shutil.copy2(support.BOUNDED,host/'runtime/run_bounded_dragon.py')
        require(support.pin(host/'runtime/run_bounded_dragon.py')['sha256']==support.BOUNDED_SHA,'original bounded runtime full bytes')
        remaining=WHOLE_CAP-(time.monotonic()-started)
        if remaining<=0:raise ValueError('whole admission budget exhausted')
        runner=full.OwnRSSSerialExecutor(host,remaining,'FULL_RAWRECORD_TRANSFER',resources)
        if type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources or Path(runner.bounded.__file__).resolve()!=host/'runtime/run_bounded_dragon.py':raise ValueError('genuine runner binding required')
        host_pid=os.getpid()
        protocol_command=[str(support.PYTHON),'-B',str(protocol),'--ready-wrapper',str(target),'--ready-wrapper-sha256',TARGET_SHA,'--binding',str(binding_path),'--binding-sha256',BINDING_SHA,'--output-dir',str(control),'--expected-parent-pid',str(host_pid)]
        runner.execute(host/'protocol_run','protocol',protocol_command,STAGE_CAP)
        protocol_receipt,protocol_report=observed_stage(support,runner,host/'protocol_run','protocol',protocol_command,control/'ACTUAL_PROTOCOL_REPORT.json',host_pid)
        require(protocol_report['schema']=='CURRENT150_AB_ACTUAL_COMPLETE_RAWRECORD_PROTOCOL_CONTROLS_V1'and type(protocol_report['positive_count'])is int and protocol_report['positive_count']==len(protocol_report['complete_positive_controls'])==5 and type(protocol_report['negative_count'])is int and protocol_report['negative_count']==len(protocol_report['complete_negative_controls'])==10 and all(row['actual_control_passed']is True for row in protocol_report['complete_positive_controls']),'all five full positive/ten actual reject software controls')
        require(all(row.get('both_full_readers_rejected')is True or row.get('observed_rejection')is True for row in protocol_report['complete_negative_controls'])and all(len(row['actual_observed_errors'])==2 and{r['reader']for r in row['actual_observed_errors']}=={'native_default','stream_default'}for row in protocol_report['complete_negative_controls']if row.get('both_full_readers_rejected')is True),'every predeclared rejection genuinely observed; no omitted reader')
        require(protocol_report['original_caps']==CAPS and protocol_report['binding']['sha256']==BINDING_SHA and protocol_report['wrapper']['sha256']==TARGET_SHA,'protocol actual bindings and original caps')
        require(support.archive_bytes(joint_paths)<ARCHIVE_CAP and time.monotonic()-started<WHOLE_CAP,'original joint/whole caps after protocol')
        between=resources.check()
        transfer_command=[str(support.PYTHON),'-B',str(target),'--binding',str(binding_path),'--binding-sha256',BINDING_SHA,'--output-dir',str(out),'--expected-parent-pid',str(host_pid)]
        runner.execute(host/'transfer_run','transfer',transfer_command,STAGE_CAP)
        transfer_receipt,transfer_report=observed_stage(support,runner,host/'transfer_run','transfer',transfer_command,out/'ACTUAL_TRANSFER_REPORT.json',host_pid)
        require(transfer_report['schema']=='CURRENT150_AB_ACTUAL_FULL_RAWRECORD_SOFTWARE_TRANSFER_REPORT_V1'and transfer_report['source_binding']['sha256']==BINDING_SHA and transfer_report['declared_original_caps']==CAPS and transfer_report['actual_full_raw_and_typed_two_reader_transfer_complete']is True and transfer_report['all_both_reader_records_default_retained']is True,'actual complete two-reader A/B raw transfer only')
        require([row['state']for row in transfer_report['states']]==['A','B']and all(row['independent_full_reader_comparison']['all_paths_types_order_values_floatbits_equal']is True and row['scientific_contract_inventory']['future_solver_scientific_input_admitted']is False for row in transfer_report['states']),'all A thenB fields/gaps remain science-unadmitted')
        require(len(runner.records)==2 and all(row['status']=='PASS'for row in runner.records),'two real serial stage PASS records; never retry')
        after=resources.check();elapsed=time.monotonic()-started;archived=support.archive_bytes(joint_paths)
        if not math.isfinite(elapsed)or not elapsed<WHOLE_CAP or not archived<ARCHIVE_CAP:raise ValueError('unchanged admission host caps exceeded')
        for entry in inputs+[hpin,rpin,*genuine_pins]:
            if support.pin(entry['path'],entry['sha256'])!=entry:raise ValueError('normal complete pinned inputs changed')
        require(complete_source_inputs(support,archive)==source_inputs and complete_source_inputs(support,receipts)==receipt_inputs,'complete SOURCE/receipt namespace unchanged; no unpinned additions')
        value=dict(schema='CURRENT150_AB_GENUINE_COMPLETE_RAWRECORD_TRANSFER_HOST_V1',status='ACTUAL_SAVED_COMPLETE_SOFTWARE_TRANSFER_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED',actual_host_PID=host_pid,input_sources=inputs,original_helper=hpin,resource_factory=rpin,genuine_guard_sources=genuine_pins,actual_protocol=protocol_receipt,actual_transfer=transfer_receipt,stage_records=runner.records,resources_before=before,resources_between=between,resources_after=after,history_roots=roots,source_and_receipts_outsideART_counted_separately=True,whole_seconds=elapsed,archive_before_result_bytes=archived,archive_roots=list(map(str,joint_paths)),original_caps=CAPS,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,actual_software_payload_saved=True,external_actual_Root_typed_EXIT0_CLOSED_required=True,actual_protocol_qualification_sha256=None,actual_transfer_qualification_sha256=None,**FALSE)
        support.write_new(host/'result.json',value)
        if support.archive_bytes(joint_paths)>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final admission host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(host/'result.json'),actual_external_Root_terminal_required=True,**FALSE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():support.write_new(host/'failed_host_result.json',dict(status='FAILED_COMPLETE_SOFTWARE_RAW_TRANSFER_NO_RETRY_NO_QUALIFICATION',error=repr(error),stage_records=[] if runner is None else runner.records,**FALSE))
        raise

if __name__=='__main__':main()
