"""Prepare a closed A10 continuation Source; no Dragon, compiler, collection or release here."""
import ast,hashlib,json,os
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'current_formal_first_A_short_FIL_producer_source_v10_20261014'
OUT=R/'current_formal_short_FIL_A10_closed_capture_continuation_source_v1_20261014'
NAME='complete_closed_short_FIL_A10_capture_and_release.py'
MAIN=r'''def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    roles=['original-phase','original-Root-tools','original-Root-argv','original-host-freeze','original-CLI','failed-post','failed-post-tools','continuation-host-freeze']
    for role in roles:
        for suffix in ['summary','sha256','seven-id']:parser.add_argument('--'+role+'-'+suffix,required=True)
    parser.add_argument('--output-dir',required=True)
    args=parser.parse_args();start=time.monotonic();pins={};data={}
    for role in roles:
        key=role.replace('-','_');data[role],pins[role]=c.load_json_exact(getattr(args,key+'_summary'),getattr(args,key+'_sha256'),getattr(args,key+'_seven_id'))
    d=data['original-phase'];root=data['original-Root-tools'];ra=data['original-Root-argv'];oldhf=data['original-host-freeze'];cli=data['original-CLI'];post=data['failed-post'];pt=data['failed-post-tools'];hf=data['continuation-host-freeze']
    import copy,hashlib,shlex,sys,stat
    q=root['actual_terminal_return']
    require(root['observed_closed']is True and type(root['original_integer_exit_code'])is int and root['original_integer_exit_code']==1 and type(q['exit_code'])is int and q['exit_code']==1 and q.get('session_id')is None,'original actual Root1 retained')
    require(shlex.split(root['exact_executed_command'])==ra['exact_argv']==cli['exact_argv']and len(ra['exact_argv'])==32 and ra['actual_CLI_pin']==pins['original-CLI']and ra['actual_Host_freeze_pin']==pins['original-host-freeze']and cli['Host_freeze_pin']==pins['original-host-freeze'],'original genuine exact32/HF/CLI')
    require(d['schema']=='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1'and d['status']=='FAILED_CURRENT_OBSERVATION_NO_RETRY'and d['failure']=='RuntimeError: both real process metadata tools fully pinned'and d['actual_closed_owned_library_copy_release_pin']is None and d['actual_full_A_observation_executed']is False and len(d['records'])==1 and d['records'][0]['status']=='PASS','only original post-stage process-tool omission; not material retry')
    require(post['schema']=='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1'and post['status']=='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION'and post['failure']is None and post['actual_material_stage_closed0']is True and post['actual_stage_statuses']==['PASS']and post['actual_context_collection_source_function_verified']is True,'required actual cached collection factual post0')
    canonical={'actual_report_pin':pins['original-phase'],'actual_Host_freeze_pin':pins['original-host-freeze'],'actual_CLI_pin':pins['original-CLI'],'actual_Root_true_tool_return_pin':pins['original-Root-tools'],'actual_Root_argv_pin':pins['original-Root-argv']}
    require(all(post[k]==v for k,v in canonical.items())and all(post[k]is False for k in ['business_executed','compiler_executed','numerical_executed','files_deleted'])and post['actual_observation_manifest_pin']is None and post['actual_closed_owned_library_copy_release_pin']is None,'five real authorities; original no manifest/release')
    require(pt['observed_closed']is True and type(pt['original_integer_exit_code'])is int and pt['original_integer_exit_code']==0,'factual post observed closed0')
    for k in ['actual_review_return','actual_postverification_return']:
        z=pt[k];require(type(z['exit_code'])is int and z['exit_code']==0 and z.get('session_id')is None and json.loads(z['output'].strip().splitlines()[-1])['review_pin']==pins['failed-post'],'genuine post original integer0/stdoutPF')
    require(hf['schema']=='COMPLETE_SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_HOST_SOURCE_ONLY_FREEZE_V1'and hf['host_source']==c.pin(Path(__file__).absolute())and hf['selected_original_failed_phase_pin']==pins['original-phase']and hf['selected_original_failed_post_pin']==pins['failed-post']and hf['selected_original_Host_freeze_pin']==pins['original-host-freeze']and hf['Dragon_rerun_permitted']is False,'explicit own continuation Source binding')
    owner=Path(pins['original-phase']['path']).parent;out=Path(args.output_dir)
    require(str(owner)==cli['output_root']and out.is_absolute()and out.parent==c.ART and not os.path.lexists(out)and not out.is_relative_to(owner)and not owner.is_relative_to(out),'fresh separate reports; original owner unchanged')
    require(ra['exact_argv'][-2:]==['--output-dir',str(owner)]and d['actual_B_observation_executed']is False and d['three_recaptured_plane_histories_claimed']is False,'actual original A only')
    def current7(p):
        path=Path(p['path']);s=path.lstat()
        require(stat.S_ISREG(s.st_mode)and not any(a.is_symlink()for a in [path,*path.parents])and c.identity(path)==p['identity'],'selected live current7; no generic historical skip')
    for p in hf['dependencies']:current7(p)
    original_source=Path(oldhf['host_source']['path']);c.same_pin(original_source,oldhf['host_source'])
    for field in ['original_release_function_Source','original_collect_function_Source']:
        require(hf[field]['source_pin']==oldhf['host_source'],'original function Source')
    supportspec=importlib.util.spec_from_file_location('continuation_original_support',c.SUPPORT);support=importlib.util.module_from_spec(supportspec);supportspec.loader.exec_module(support)
    require(c.pin(c.SUPPORT)['sha256']==c.SUPPORT_SHA and Path(sys.executable).resolve()==support.PYTHON and not sys.flags.optimize and not os.environ.get('PYTHONOPTIMIZE')and sys.getprofile()is None and all(os.environ.get(k)=='1'for k in c.THREADS),'original environment and guard Source')
    helper,_=support.load(support.OLD_HELPER,support.OLD_HELPER_SHA,'continuation_original_helper');factory,_=support.load(support.RESOURCE_FACTORY,support.RESOURCE_SHA,'continuation_original_resources');full,production=helper.modules();helper.guard_admission(full)
    require(full.OwnRSSSerialExecutor.__bases__==(production.SerialExecutor,)and Path(full.__file__).resolve()==support.FULL and Path(production.__file__).resolve()==support.PARENT,'original OwnRSS guard class/MRO; no stage execution')
    history=factory.DynamicHistoryResources(c.ART,factory.history_roots([str(owner),str(out)],c.ART),8*2**30,96*2**30,production.ResourceFailure)
    fresh=production.DiskResources(c.ART,[str(owner),str(out)],8*2**30,2*2**30)
    class Resources:
        def check(self):
            h=history.check();f=fresh.check()
            if h['artifact_bytes']+20971764748+64*2**20>=96*2**30:raise RuntimeError('history96GiB original cold reserve')
            if f['disk_free_bytes']-20971764748-2*2**30<8*2**30:raise RuntimeError('filesystem8GiB original reserves')
            return dict(h,fresh_output=f)
    resources=Resources();before=resources.check()
    def budget():
        require(time.monotonic()-start<1800,'original whole1800');resources.check();check_original_host_limits(c,start)
    records=copy.deepcopy(d['records']);state=copy.deepcopy(post['actual_collected_A_observation_state']);states={'A':state}
    require(state['state']=='A'and state['actual_genuine_material_stage']==records[0]and state['actual_cwd']==str(owner/'A')and state['actual_material_child_closed_before_manifest']is True and state['all_producer_file_handles_closed_before_next_state']is True,'only cached exact original closed A collection')
    require(state['complete_observed_file_pins']and state['actual_procedure_three_literal_inverse']['whole_reverse_replacement_equals_original_bytes']is True and state['actual_procedure_three_literal_inverse']['all_numeric_and_non_FIL_Source_bytes_unchanged']is True,'cached original complete collection/procedure proof required')
    plan=json.loads(Path(cli['seed_plan_pin']['path']).read_bytes());c.same_pin(cli['seed_plan_pin']['path'],cli['seed_plan_pin'])
    originals=original_shared_libraries(plan);copies=post['actual_owned_library_copy_pins_current']
    require(type(copies)is list and len(copies)==2 and sum(p['size_bytes']for p in copies)==979740136,'exact original private2 current')
    shared=dict(schema='ACTUAL_AB_SINGLE_COPY_COMPLETE_ORIGINAL_LIBRARY_EVIDENCE_V1',original_input_pins=originals,shared_copy_pins=dict(zip(originals,copies)),material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,shared_library_directory=str(owner/'s'),all_library_bytes_preserved_without_symlinks_or_hardlinks=True,actual_state_library_full_EOF_observations={})
    for name,p in shared['shared_copy_pins'].items():require(p['path']==str(owner/'s'/SHARED_INPUT_LIBRARY_LAYOUT['physical_file_names'][name])and p['sha256']==originals[name]['sha256']and p['size_bytes']==originals[name]['size_bytes'],'exact actual original shared two copies')
    fixed=list(d['fixed_current_pins']);lsof=c.pin('/usr/sbin/lsof');require('/usr/sbin/lsof'not in {p['path']for p in fixed},'only omitted lsof authority appended');fixed+=[lsof]+list(pins.values())+hf['dependencies']
    table={}
    for p in fixed:require(p['path']not in table or table[p['path']]==p,'same current path exactPF');table[p['path']]=p
    fixed=list(table.values());owned=[p for p in d['owned_input_copy_pins']];outputs_original=list(d['output_pins'])
    def check_current():
        budget()
        for p in fixed+owned+outputs_original:current7(p)
    check_current();out.mkdir();newwatch=[]
    for suffix in ['.log','.watchdog.json']:
        oldpath=owner/(records[0]['label']+suffix);want=next(p for p in outputs_original if p['path']==str(oldpath));target=out/oldpath.name
        with oldpath.open('rb')as src,target.open('xb')as dst:shutil.copyfileobj(src,dst,2**20)
        pp=fullpin(target,budget);require(pp['sha256']==want['sha256']and pp['size_bytes']==want['size_bytes']and pp['identity'][:2]!=want['identity'][:2],'entire original log/watch ordinary distinct copies')
        if suffix=='.watchdog.json':newwatch.append(dict(path=pp['path'],sha256=pp['sha256']))
    release_receipt=None;failure=None;first=None;tb=None;after=None
    try:
        check_current()
        release_receipt,released=release_closed_owned_library_copies(owner,shared,states,records,fixed,budget)
        owned=[p for p in owned if p['path']not in released];outputs_original=[p for p in outputs_original if p['path']not in released]
        check_current();after=resources.check()
        require(after['artifact_bytes']+20971764748+64*2**20+2*2**30<96*2**30,'after exact release original real fullfresh2 reserve')
    except BaseException as error:first=error;tb=error.__traceback__;failure=repr(error)
    phase=out/'Root_actual_material_observation_execution_summary.json';phase_data=dict(schema='ACTUAL_CURRENT_FORMAL_A_MATERIAL_OBSERVATION_EXECUTION_V1',status='ACTUAL_ONE_A_MATERIAL_STAGE_CLOSED0_EVIDENCE_ONLY'if failure is None else'FAILED_CURRENT_OBSERVATION_NO_RETRY',failure=failure,after_check_error=None,records=records,actual_watchdog_checks=newwatch,fixed_current_pins=fixed,owned_input_copy_pins=owned,output_pins=outputs_original+[fullpin(p,budget)for p in out.iterdir()if p.is_file()],current_case_spec_pin=d['current_case_spec_pin'],actual_observer_build_report_pin=d['actual_observer_build_report_pin'],actual_runtime_pin=d['actual_runtime_pin'],original_guard_class=d['original_guard_class'],original_guard_MRO_unchanged=d['original_guard_MRO_unchanged'],SELF_peak_bytes=max(d['SELF_peak_bytes'],c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss),wall_seconds=time.monotonic()-start,resources_before=before,resources_after=after,actual_full_A_observation_executed=failure is None,actual_B_observation_executed=False,three_recaptured_plane_histories_claimed=False,actual_closed_owned_library_copy_release_pin=release_receipt,completion_only_existing_closed_stage=True,Dragon_or_compiler_or_material_child_launched_by_continuation=False,original_failed_phase_pin=pins['original-phase'],original_Root_true_tool_pin=pins['original-Root-tools'],original_Root_exit_code_retained=1,original_Root_failure_retained=d['failure'],actual_prior_material_stage_record_reused_wholebytes=True,actual_prior_A_cwd=str(owner/'A'),original_material_host_wall_seconds=d['wall_seconds'],cached_actual_collection_post_pin=pins['failed-post'],original_capture_collector_not_reexecuted=True,original_release_owner_output_root=str(owner),original_release_four_library_full_EOF_observations_required=True,new_scientific_outputs_created=False,requires_host_process_metadata_access=True,final_report_bytes_in_original_resources=True,**FUTURE)
    c.write(phase,phase_data);phasepin=fullpin(phase,budget)
    if first is not None:raise first.with_traceback(tb)
    state['actual_owning_report_pin']=phasepin;state['actual_stage_label']=records[0]['label'];state['actual_command']=records[0]['command']
    manifest=out/'ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST.json'
    c.write(manifest,dict(schema='ACTUAL_CURRENT_FORMAL_COMPLETE_OBSERVATION_MANIFEST_V1',current_case_spec_pin=d['current_case_spec_pin'],state_order=['A'],states=states,observation_scope='ONE_SAME_PHYSICAL_A_MATERIAL_CONSTRUCTION_NOT_THREE_HISTORIES',actual_observer_build_report_pin=d['actual_observer_build_report_pin'],actual_runtime_pin=d['actual_runtime_pin'],actual_shared_input_library_evidence=shared,actual_closed_owned_library_copy_release_pin=release_receipt,shared_copy_pins_are_historical_closed_consumption_not_current_live_inputs=True,material_input_layout=SHARED_INPUT_LIBRARY_LAYOUT,all_host_managed_handles_closed=True,actual_lsof_owner_handle_closure_qualified=False,original_caps=dict(whole_seconds=1800,stage_seconds=600,rss_mib=512,joint_archive_bytes=2*2**30,history_bytes=96*2**30,free_floor_bytes=8*2**30,threads=1,children_at_once=1,retries=0),completion_only_original_Root1_preserved=True,original_failed_phase_pin=pins['original-phase'],original_Root_true_tool_pin=pins['original-Root-tools'],cached_actual_collection_post_pin=pins['failed-post'],**FUTURE))
    check_current();resources.check();check_original_host_limits(c,start)
    print(json.dumps(dict(status='ACTUAL_EXISTING_A10_CAPTURE_CONTINUATION_AND_PRIVATE_COPY_RELEASE_CLOSED0_NO_DRAGON_RERUN',completion_report_pin=phasepin,observation_manifest_pin=fullpin(manifest,budget),release_receipt_pin=release_receipt,original_Root_exit_code_retained=1,actual_original_material_stage_count=1,new_material_child_launch_count=0,physics_qualified=False)),flush=True)
'''
def pin(p):
 s=p.stat();return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),size_bytes=s.st_size,identity=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns])
def write(p,v):
 raw=v.encode()if isinstance(v,str)else(json.dumps(v,indent=2,allow_nan=False)+'\n').encode()
 with p.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 if OUT.exists():raise RuntimeError('unique continuation Source namespace')
 old=OLD/'produce_current_formal_material_observations.py';a=old.read_text();tree=ast.parse(a);n=next(x for x in tree.body if isinstance(x,ast.FunctionDef)and x.name=='main');segment=ast.get_source_segment(a,n)
 if a.count(segment)!=1:raise RuntimeError('original complete main unique')
 z=a.replace(segment,MAIN.rstrip(),1);ast.parse(z)
 for name in ['collect_state','release_closed_owned_library_copies','recheck_shared_libraries','original_shared_libraries','fullpin','recheck','derive_original_procedure']:
  f=lambda text:ast.get_source_segment(text,next(x for x in ast.parse(text).body if isinstance(x,ast.FunctionDef)and x.name==name))
  if f(a)!=f(z):raise RuntimeError('original entire function bytes '+name)
 if 'runner.execute('in MAIN or 'collect_state('in MAIN or 'c.initialize('in MAIN:raise RuntimeError('no job, recollection or scientific initialize')
 OUT.mkdir();cp=write(OUT/NAME,z);hp=write(OUT/'current_material_prerequisite_admission.py',(OLD/'current_material_prerequisite_admission.py').read_bytes().decode())
 iv=write(OUT/'COMPLETE_SHORT_FIL_A10_CONTINUATION_WHOLE_MAIN_BYTE_INVERSE.json',dict(schema='COMPLETE_SHORT_FIL_A10_CONTINUATION_WHOLE_MAIN_BYTE_INVERSE_V1',predecessor_source_pin=pin(old),candidate_source_pin=cp,changes=[dict(before=segment,after=MAIN.rstrip())],whole_file_inverse_byte_equal=z.replace(MAIN.rstrip(),segment,1).encode()==old.read_bytes(),original_collect_and_release_and_other_functions_wholebytes_unchanged=True,original_records_never_synthesized_or_modified=True,only_actual_cached_collection_reused_no_second_collect=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 plan=write(OUT/'CONTINUATION_SOURCE_PLAN.json',dict(schema='SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_SOURCE_PLAN_V1',source_only=True,host_source_pin=cp,helper_source_pin=hp,inverse_pin=iv,original_producer_source_pin=pin(old),selected_original_Host_freeze_pin=pin(OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json'),selected_original_CLI_pin=pin(OLD/'ROOT_REVIEWABLE_EXACT_MATERIAL_FIRST_A_SHORT_FIL_V10_ARGV_20261014.json'),expected_failed_post_schema='INDEPENDENT_MATERIAL_FIRST_A_SHORT_FIL_V10_ACTUAL_OBSERVATION_POSTVERIFICATION_V1',expected_failed_post_status='PASS_ACTUAL_MATERIAL_FIRST_A_SHORT_FIL_V10_STAGE0_CAPTURE_RELEASE_BLOCKED_FACTUAL_POSTVERIFICATION',required_cached_state_field='actual_collected_A_observation_state',required_cached_state_original_keys=['actual_cwd','complete_observed_file_pins','physical_input_pins','actual_seed_copy_pins','actual_seed_role_mapping','actual_procedure_three_literal_inverse'],original_release_owner_uses_original_OUT_s=True,new_reports_only_in_distinct_OUT=True,new_log_watch_copies_exact_original_SHA_distinct_nodes=True,no_Dragon_or_compiler_or_collect_call=True,ordinary_resource_class_and_512_600_1800_2GiB_8GiB_96GiB_caps_unchanged=True,initial_fresh2_new_scientific_copy_not_attempted=True,after_actual_release_original_fullfresh2_admission_required=True,original_release_rechecks_two_original_and_two_owned_libraries_full_EOF=True,original_release_rechecks_cached_observed_files_without_second_collection_or_payload_decode=True,future_actual_failed_post_pin=None,future_actual_failed_post_tools_pin=None,future_actual_own_Host_freeze_pin=None,future_actual_completion_report_pin=None,future_actual_manifest_pin=None,future_actual_release_pin=None,physics_qualified=False,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 ready=write(OUT/'SOURCE_REVIEW_READY.json',dict(schema='SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_SOURCE_ONLY_READY_V1',host_source_pin=cp,helper_source_pin=hp,plan_pin=plan,inverse_pin=iv,Source_preparer_pin=pin(__file__),future_actual_failed_post_pin=None,future_actual_failed_post_tools_pin=None,future_actual_own_HF_pin=None,future_actual_own_CLI_pin=None,Source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
 print(json.dumps(dict(status='SHORT_FIL_A10_CLOSED_CAPTURE_CONTINUATION_SOURCE_ONLY_READY',host_source_pin=cp,helper_source_pin=hp,plan_pin=plan,inverse_pin=iv,ready_pin=ready,Source_preparer_pin=pin(__file__),business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)),flush=True)
if __name__=='__main__':main()
