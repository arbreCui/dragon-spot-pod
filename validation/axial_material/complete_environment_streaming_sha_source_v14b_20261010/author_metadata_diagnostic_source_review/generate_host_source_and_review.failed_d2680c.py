from pathlib import Path
import ast,hashlib,json
D=Path(__file__).parent
mother=Path('/Users/wen/spot/validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_control_sources/helper_only_host_v14b.py')
factory=Path('/private/tmp/axmat_v14b_complete_component_ready_source_binding_20261010/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py')
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
original=mother.read_text();text=original;edits=[]
def replace(old,new):
    global text
    assert text.count(old)==1,(old[:70],text.count(old))
    text=text.replace(old,new);edits.append(dict(old=old,new=new,count=1))
old_doc=ast.get_source_segment(original,ast.parse(original).body[0])
replace(old_doc,'"""One real read-only metadata diagnostic under the unchanged original supervisor.\n\nOnly Root binds this source and starts the new exclusive diagnostic namespace.\nNo component prepare/build/audit/admit, numerical controls or transport action.\nThe original619/FULL705/parent38de/boundedbc/f136 resources remain genuine.\nImporting this host creates no files and loads no business module.\n"""')
replace("STATUS = 'READY_ROOT_BOUND_HELPER_ONLY_GENUINE_SUPERVISOR'", "STATUS = 'UNREADY_ROOT_REVIEW_AND_SOURCE_BINDINGS_REQUIRED'")
replace("DRIVER = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/actual_control_sources/helper_only_controls_v14b.py'", "DRIVER = None")
replace("DRIVER_SHA256 = 'a0cd6a7b37d0b9f9cce786d78c1336d0edbe870c44be6be939f1b7ed5e9a0f30'", "DRIVER_SHA256 = None\nTARGET_FACTORY = None\nTARGET_FACTORY_SHA256 = None\nCANONICAL_TARGET = ROOT / 'validation/axial_material/prepare_qualified_AB_sender_contiguous_flux_window_streaming_sha_production_v14b.py'\nHELPER_ADMISSION = ROOT / 'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010/Root_actual_helper_controls_admission.json'\nHELPER_ADMISSION_SHA256 = '16d4548b1cc4ffe935bd8d28219e99a6e9da9af949e7577a82eb758e99d7f568'")
old_main=ast.get_source_segment(original,next(n for n in ast.parse(original).body if isinstance(n,ast.FunctionDef) and n.name=='main'))
new_main='''def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    started = time.monotonic()
    if STATUS != 'READY_ROOT_BOUND_READONLY_METADATA_GENUINE_SUPERVISOR':
        raise ValueError('UNREADY: metadata diagnostic source and bindings require Root review')
    for value in (DRIVER_SHA256, TARGET_FACTORY_SHA256, HELPER_SHA256, PROOF_SHA256):
        if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
            raise ValueError('all reviewed metadata source pins required')
    if (DRIVER is None or not Path(DRIVER).is_absolute() or Path(DRIVER).parent.parent != ROOT/'validation/axial_material/complete_environment_streaming_sha_source_v14b_20261010'
            or TARGET_FACTORY is None or Path(TARGET_FACTORY) != CANONICAL_TARGET):
        raise ValueError('normal canonical target and Root-installed metadata driver required')
    if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE') or any(os.environ.get(k) != '1' for k in THREAD_KEYS):
        raise ValueError('nonoptimized single-thread interpreter required')
    sys.dont_write_bytecode = True
    if Path(sys.executable).resolve() != PYTHON:
        raise ValueError('declared genuine Python3.12 required')
    host_root = ART / 'axial-material-complete-environment-metadata-timing-host-v14b-20261010'
    control_root = ART / 'axial-material-complete-environment-metadata-timing-v14b-20261010'
    if os.path.lexists(host_root) or os.path.lexists(control_root):
        raise ValueError('fresh metadata-only evidence namespaces required; no retry')
    inputs = [pin(DRIVER, DRIVER_SHA256), pin(TARGET_FACTORY, TARGET_FACTORY_SHA256),
              pin(HELPER, HELPER_SHA256), pin(PROOF, PROOF_SHA256), pin(HELPER_ADMISSION, HELPER_ADMISSION_SHA256),
              pin(FULL, FULL_SHA256), pin(PARENT, PARENT_SHA256), pin(BOUNDED, BOUNDED_SHA256)]
    # This imports only the same original supervisor/resource chain already
    # used by H14b. The target factory is imported exclusively by the child.
    h, hpin = load(OLD_HELPER, OLD_HELPER_SHA256, 'axmat_v14b_metadata_genuine_original619')
    resource_factory, resource_pin = load(RESOURCE_FACTORY, RESOURCE_FACTORY_SHA256, 'axmat_v14b_metadata_genuine_resources_f136')
    full, production = h.modules()
    if (full.OwnRSSSerialExecutor.__bases__ != (production.SerialExecutor,)
            or Path(full.__file__).resolve() != FULL or Path(production.__file__).resolve() != PARENT):
        raise ValueError('genuine unchanged supervisor and direct parent MRO required')
    h.guard_admission(full)
    roots = resource_factory.history_roots([str(host_root), str(control_root)], ART)
    resources = resource_factory.resources_for(roots, production.ResourceFailure)
    before = resources.check()
    if before['artifact_bytes'] + ARCHIVE_CAP >= 96 * 2**30 or before['disk_free_bytes'] - ARCHIVE_CAP < 8 * 2**30:
        raise ValueError('original complete-history/free-space allowance required')
    host_root.mkdir()
    for name in ('runtime', 'run', 'METADATA_TIMING'):
        (host_root / name).mkdir()
    shutil.copy2(BOUNDED, host_root / 'runtime/run_bounded_dragon.py')
    remaining = WALL_CAP - (time.monotonic() - started)
    if remaining <= 0:
        raise ValueError('whole metadata-diagnostic budget exhausted before child launch')
    runner = full.OwnRSSSerialExecutor(host_root, remaining, 'METADATA_TIMING', resources)
    if (type(runner) is not full.OwnRSSSerialExecutor or runner.resources is not resources
            or Path(runner.bounded.__file__).resolve() != host_root / 'runtime/run_bounded_dragon.py'):
        raise ValueError('genuine supervisor constructor binding differs')
    command = [str(PYTHON), '-B', str(DRIVER), '--out', str(control_root)]
    try:
        runner.execute(host_root / 'run', 'metadata', command, remaining)
        log = host_root / 'run/metadata.log'
        stdout = json.loads(log.read_text())
        result_path = control_root / 'result.json'
        result = json.loads(result_path.read_text())
        watch_path = log.with_suffix('.watchdog.json')
        watch = json.loads(watch_path.read_text())
        after = resources.check()
        elapsed = time.monotonic() - started
        archived = archive_bytes((host_root, control_root))
        expected_status = 'READONLY_METADATA_PROFILE_COMPLETE_DIAGNOSTIC_ONLY'
        if (stdout['status'] != expected_status or result['status'] != expected_status
                or stdout['result_sha256'] != pin(result_path)['sha256']
                or stdout['Root_actual_child_terminal_required_before_admission'] is not True
                or result['profile']['direct_invocations'] != {name:1 for name in ('sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs')}
                or result['profile']['profiler_cleared'] is not True or result['profile']['forbidden_canonical_calls']
                or len(runner.records) != 1 or runner.records[0]['status'] != 'PASS'
                or type(watch['returncode']) is not int or watch['returncode'] != 0
                or watch['command'] != command or watch['limit_failure'] is not None
                or watch['own_child_only'] is not True or watch['liveness_group_cleanup'] is not True
                or not 0 <= watch['sampled_peak_rss_mib'] < RSS_CAP or not elapsed < WALL_CAP
                or not archived < ARCHIVE_CAP):
            raise ValueError('complete actual bounded metadata-only diagnostic return required')
        for entry in inputs:
            if pin(entry['path'], entry['sha256']) != entry:
                raise ValueError('whole source or proof identity changed during metadata diagnostic')
        value = {'schema':'AXMAT_V14B_READONLY_METADATA_GENUINE_SUPERVISOR_ACTUAL_HOST_V1',
                 'status':'ACTUAL_BOUNDED_METADATA_DIAGNOSTIC_CLOSED_EXTERNAL_ROOT_REQUIRED',
                 'input_sources':inputs,'original_helper':hpin,'resource_factory':resource_pin,
                 'actual_command':command,'actual_full_merged_stdout_stderr':pin(log),
                 'actual_child_result':pin(result_path),'actual_watchdog':pin(watch_path),
                 'stage_records':runner.records,'watchdog':watch,
                 'resources_before':before,'resources_after':after,'resource_roots':[str(x) for x in roots],
                 'whole_elapsed_seconds':elapsed,'whole_archive_bytes':archived,
                 'whole_wall_cap_seconds':WALL_CAP,'rss_cap_mib':RSS_CAP,'archive_cap_bytes':ARCHIVE_CAP,
                 'threads':1,'children_at_once':1,'retries':0,
                 'supervisor_class_or_MRO_modified':False,'failed_V13_audit_reexecuted':False,
                 'old_failed_V13_factory_imported_or_called':False,'four_pure_metadata_calls_only':True,
                 'numerical_component_or_transport_executed':False,'original86_stage_count_increment':0,
                 'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False}
        write_new(host_root/'result.json',value)
        print(json.dumps({'status':value['status'],'host_result':pin(host_root/'result.json'),
                          'actual_external_Root_terminal_still_required':True},allow_nan=False),flush=True)
    except BaseException as error:
        write_new(host_root/'failed_host_result.json',{'status':'FAILED_METADATA_ONLY_HOST_NO_RETRY',
            'error':repr(error),'stage_records':runner.records,'elapsed_seconds':time.monotonic()-started,
            'native_RSS_verified':False,'AAA_accuracy_qualified':False,'ABA_admitted':False})
        raise'''
replace(old_main,new_main)
inverse=text
for edit in reversed(edits):
    assert inverse.count(edit['new'])==1;inverse=inverse.replace(edit['new'],edit['old'])
assert inverse==original
host=D/'metadata_timing_host.UNREADY.py';host.write_text(text)
driver=D/'metadata_timing_driver.UNREADY.py'
for path in (host,driver):ast.parse(path.read_text());compile(path.read_text(),str(path),'exec')
def defs(source):
    return {n.name:ast.get_source_segment(source,n) for n in ast.parse(source).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
olddefs=defs(original);newdefs=defs(text)
assert olddefs.keys()==newdefs.keys() and [n for n in olddefs if olddefs[n]!=newdefs[n]]==['main']
source=factory.read_text();ft=ast.parse(source);top={n.name:n for n in ft.body if isinstance(n,ast.FunctionDef)}
selected=['sender_source_admission','sender_control_contract','stream_environment_helper_source_admission','source_inputs']
safe=set(selected)|{'require','read','pin','digest'}
calls=[]
for name in selected:
    node=top[name];segment=ast.get_source_segment(source,node)
    for call in ast.walk(node):
        if not isinstance(call,ast.Call):continue
        if isinstance(call.func,ast.Name) and call.func.id in top:
            assert call.func.id in safe,(name,call.func.id,call.lineno)
            calls.append(dict(caller=name,callee=call.func.id,line=call.lineno))
        if isinstance(call.func,ast.Attribute):
            assert call.func.attr not in {'write','write_text','write_bytes','mkdir','unlink','rmdir','rename','replace','execute','run','Popen','call','system','exec_module','launch'},(name,ast.unparse(call.func),call.lineno)
            if call.func.attr=='open':
                assert all(not(isinstance(a,ast.Constant) and isinstance(a.value,str) and any(c in a.value for c in 'wax+')) for a in call.args[1:])
functionscope={name:dict(first_line=top[name].lineno,last_line=top[name].end_lineno,
    full_source_sha256=hashlib.sha256(ast.get_source_segment(source,top[name]).encode()).hexdigest(),
    normal_import_allowed_only_after_root_binding=True,static_no_write_child_transport=True) for name in selected}
proof={'schema':'AXMAT_V14B_METADATA_HOST_COMPLETE_SOURCE_INVERSE_V1','parent_host':{'path':str(mother),'sha256':sha(mother)},
       'new_host':{'path':str(host),'sha256':sha(host)},'edits':edits,'complete_inverse_byteexact':True,
       'all_original_eight_support_functions_byteexact':True,'only_host_main_definition_changed':True,
       'original_supervisor_classes_and_MRO_unchanged':True,'driver_new_source_no_parent_function_overlay':True}
(D/'HOST_COMPLETE_SOURCE_INVERSE.json').write_text(json.dumps(proof,indent=2)+'\n')
review={'schema':'AXMAT_V14B_METADATA_TIMING_SOURCE_ONLY_PRECHECK_V1','status':'SOURCE_ONLY_UNREADY_NOT_EXECUTED',
    'frozen_target_candidate':{'path':str(factory),'sha256':sha(factory)},'canonical_target_required':str(factory).replace('/private/tmp/axmat_v14b_complete_component_ready_source_binding_20261010','/Users/wen/spot/validation/axial_material'),
    'all_four_metadata_functions_static_readonly':True,'source_inputs_not_reduced_to_three':True,
    'four_function_full_source_pins':functionscope,'direct_same_factory_call_sites':calls,
    'source_inputs_reads_original_parent_declaration_not_failed_V13':{'line':top['source_inputs'].lineno+30,'literal':'PARENT / declaration.json','PARENT':'/Users/wen/spot/validation/artifacts/axial-material-rank1-factor-cache-build-20261007'},
    'failed_V13_factory_only_source_file_SHA_and_text_owner_not_module_call':True,
    'target_import_top_level_STDlib_constants_and_guarded_main_only':True,
    'host_original_support_defs_preserved':len(olddefs)-1,'host_complete_inverse':proof,
    'profile_exactly_four_direct_calls_each_once':selected,'canonical_support_profile_scope':['require','read','pin','digest'],
    'canonical_function_replacements':False,'selected_inclusive_and_exclusive_ns_plus_edges':True,
    'exclusive_interpretation':'Exclude selected canonical Python children only; remaining stdlib/C work and passive profile overhead are retained.',
    'full_return_files_not_truncated':True,'complete_input_literal_SHA_and_7ID_before_after':True,
    'future_target_path_SHA_and_host_driver_path_SHA':None,'future_actual_terminal_and_measurements':None,
    'caps':dict(whole_wall_seconds=120,own_child_RSS_MiB=512,archive_bytes=64*2**20,threads=1,children=1,retries=0,history_bytes=96*2**30,free_bytes=8*2**30),
    'new_host_root':'/Users/wen/spot/validation/artifacts/axial-material-complete-environment-metadata-timing-host-v14b-20261010',
    'new_driver_root':'/Users/wen/spot/validation/artifacts/axial-material-complete-environment-metadata-timing-v14b-20261010',
    'original86_stage_count_increment':0,'helper_or_metadata_API_imported_or_called_now':False,
    'prepare_compile_audit_build_or_numerical_executed':False,'Root_polled':False,'project_written':False,
    'component_native_AAA_ABA_credit':False,'actual_tools_so_far':None}
(D/'REPORT.json').write_text(json.dumps(review,indent=2)+'\n')
(D/'REPORT.txt').write_text('V14b受限纯元数据诊断SOURCE草稿：UNREADY。四个真实函数全源只读，source_inputs会重复sender/helper准入读并取Oct07父声明，但不导入/运行failedV13工厂。未来normalcanonical import后四函数各直接调用一次，选定canonical code被动sys.setprofile记调用/返回、inclusive/exclusive选定帧时间和完整边；不替换函数或MRO。原120秒/512MiB/64MiB/96GiB/free8/线程1/子1/重试0保留。完整return JSON及所有源码/控制证明literal SHA/7ID前后独立保留；不算新增86数学stage、不授组件/native/AAA/ABA。此稿未执行任何业务/metadata API或benchmark。\n')
print(json.dumps({'status':review['status'],'host_sha256':sha(host),'driver_sha256':sha(driver),
                 'report_sha256':sha(D/'REPORT.json'),'inverse_sha256':sha(D/'HOST_COMPLETE_SOURCE_INVERSE.json'),
                 'source_only_generation':True},indent=2))
