"""Author SOURCE strings only. Does not import or execute a candidate or guard."""
import ast
from pathlib import Path
P=Path(__file__).resolve().parent
raw=(P/'ORIGINAL_full_AB_rawrecord_genuine_host_READY.py').read_text()
tree=ast.parse(raw)
lines=raw.splitlines(keepends=True)
for n in reversed(tree.body):
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in {'SOURCE_STATUS','SOURCE_ARCHIVE','RECEIPTS','HOST','OUT','CONTROL','TARGET','TARGET_SHA','PROTOCOL','PROTOCOL_SHA','BINDING','BINDING_SHA','SOURCE_ADMISSION_SHA'} for t in n.targets):
  key=n.targets[0].id
  value="'UNREADY_SOURCE_ONLY'" if key=='SOURCE_STATUS' else 'None'
  lines[n.lineno-1:n.end_lineno]=[key+' = '+value+'\n']
raw=''.join(lines)
new_helpers='''
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

def actual_closed_prior(pin_value):
    value=strict_json(Path(pin_value['path']).read_bytes())
    actual=value['terminal_tool_return']
    require(type(actual)is dict and type(actual['exit_code'])is int and 'session_id'not in actual and type(actual['chunk_id'])is str and bool(actual['chunk_id']),'prior Root V22 build actual typed CLOSED tool truth required; any honest exit code allowed')
    return value

'''
main='''def main():
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
        value=dict(schema='CURRENT150_AB_GENUINE_COMPLETE_NATIVE_PERSISTED_XSM_ASCII_HOST_V1',status='ACTUAL_SAVED_COMPLETE_NATIVE_PERSISTED_BYTE_EVIDENCE_ONLY_EXTERNAL_ROOT_CLOSURE_REVIEW_REQUIRED',actual_host_PID=host_pid,input_sources=inputs,original_helper=hpin,resource_factory=rpin,genuine_guard_sources=genuine_pins,actual_native=stage,stage_records=runner.records,resources_before=before,resources_after=after,history_roots=roots,source_and_receipts_outsideART_counted_separately=True,complete_source_freeze=source_inputs,complete_source_directory_freeze=source_directories,complete_receipt_input_freeze=receipt_inputs,complete_receipt_directory_freeze=receipt_directories,whole_seconds=elapsed,archive_before_result_bytes=archived,archive_roots=list(map(str,roots5)),original_caps=CAPS,threads=1,children_at_once=1,retries=0,profile_used=False,supervisor_class_or_MRO_modified=False,actual_software_payload_saved=True,native_persisted_XSM_value_bits_verified=True,original_native_build_binary_Source_linkage_qualified=False,new_native_walker_controls_actual_run=None,historical_raw_protocol_is_not_new_native_protocol_qualification=True,prior_actual_V22_build_terminal=prior,external_actual_Root_typed_EXIT0_CLOSED_required=True,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,**FALSE)
        support.write_new(host/'result.json',value)
        if support.archive_bytes(roots5)>=ARCHIVE_CAP or time.monotonic()-started>=WHOLE_CAP:raise ValueError('final native host caps exceeded')
        print(json.dumps(dict(status=value['status'],actual_host_result=support.pin(host/'result.json'),actual_external_Root_terminal_required=True,**FALSE),allow_nan=False),flush=True)
    except BaseException as error:
        if host.is_dir():
            saved=out/'ACTUAL_COMPLETE_NATIVE_XSM_ASCII_EVIDENCE_REPORT.json'
            support.write_new(host/'failed_host_result.json',dict(status='FAILED_COMPLETE_NATIVE_BYTE_CHECK_NO_RETRY_NO_QUALIFICATION',error=repr(error),stage_records=[]if runner is None else runner.records,actual_native_report_pin_if_saved=support.pin(saved)if saved.is_file()and not saved.is_symlink()else None,whole_seconds=time.monotonic()-started,new_native_walker_controls_actual_run=None,native_persisted_XSM_value_bits_verified=False,actual_native_byte_qualification_sha256=None,actual_scientific_qualification_sha256=None,original_native_build_binary_Source_linkage_qualified=False,**FALSE))
        raise
'''
tree=ast.parse(raw);n=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main');lines=raw.splitlines(keepends=True);lines[n.lineno-1:n.end_lineno]=[new_helpers+main+'\n'];raw=''.join(lines)
raw=raw.replace('UNREADY SOURCE: two serial software stages under the original genuine guard.','UNREADY SOURCE: complete native persisted-byte stage under the original genuine guard.')
(P/'complete_native_XSM_ASCII_genuine_host.UNREADY.py').write_text(raw)
ast.parse(raw)
print('Source-only complete native host authored; no candidate/guard/native execution')
