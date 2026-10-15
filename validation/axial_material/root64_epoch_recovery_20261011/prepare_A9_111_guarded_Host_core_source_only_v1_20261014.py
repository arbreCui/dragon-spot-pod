"""Create an A9-only guarded BOOT Host core draft; no business/compile/MF/delete."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'boot_v16_BIND47_strict_native17_consumer_host_source_v1_20261014'
OUT=R/'boot_v16_A9_111_false_return_diagnostic_host_source_draft_v1_20261014'
HOST='run_guarded_one_BOOT_A9_false_return_diagnostic.py'
JOB=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-A9-false-return-diagnostic-20261014-v1')
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        d=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('SourceFD7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(d).hexdigest(),size_bytes=len(d),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
def write(p,v):
    b=(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(v,dict)else v.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
A9_PARSER=r'''def parse_A9_failed_return_chain(rows,plan):
    events=[r for r in rows if r.get('schema')=='ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1']
    mapping={r['predicate_id']:r for r in plan['exact_A9_original_false_return_mapping']}
    if len(mapping)!=111:raise RuntimeError('actual original111 A9 false-return Source mapping')
    if not 1<=len(events)<=2:raise RuntimeError('A9 status2 requires one CORE false return and at most one direct helper')
    seen=set()
    for e in events:
        m=mapping.get(e.get('predicate_id'));scope=e.get('scope')
        if set(e)!={'schema','scope','predicate_id','original_return_source_line','actual_boolean_status_integer'}or m is None or scope!=m['scope']or type(e['original_return_source_line'])is not int or e['original_return_source_line']!=m['original_return_source_line']or type(e['actual_boolean_status_integer'])is not int or e['actual_boolean_status_integer']!=0 or scope in seen:raise RuntimeError('one original Source A9 failed scope/ID/line/okFalse0 each')
        seen.add(scope)
    core=events[-1]
    if core['scope']!='FLU2DR64_CORE':raise RuntimeError('A9 chain ends at actual original FLU2DR64_CORE false return')
    if len(events)==2:
        helper=events[0];allowed=plan['actual_original_A9_helper_to_CORE_failed_guard_map'].get(helper['scope'])
        if allowed is None or core['original_return_source_line']not in allowed['CORE_failed_return_source_lines']or rows.index(helper)>=rows.index(core):raise RuntimeError('direct A9 helper only at its original actual CORE call guard')
    return events
'''
A9_ADMIT=r'''    if psf!=hf['selected_A9_Fortran_Source_freeze_pin']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['replacement_zero_based_link_index']!=2 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']or sf['original_module_pin']!=plan['selected_original_A9_module_pin']:raise RuntimeError('exact failure-only A9 Source freeze and object2/module4018')
    for flag in plan['required_A9_Source_freeze_true_flags']:
        if sf[flag]is not True:raise RuntimeError('A9 original single conditions/math/ABI/status/success/MAXOUT obligations')
    if sf['original_return_mapping']!=plan['exact_A9_original_false_return_mapping']or sf['scope_counts']!=plan['exact_A9_scope_counts']or sf['failed_original_okFalse_return_count']!=111 or sf['event_schema']!='ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1':raise RuntimeError('actual111 false returns and exact diagnostic event Source contract')
    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['active_original_Source_pin'],sf['complete_byte_inverse_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)
    nativepin=plan['selected_current_native17_Fortran_Source_freeze_pin'];native=c.load_json_exact(nativepin['path'],nativepin['sha256'],json.dumps(nativepin['identity']))[0]
    if nativepin!=hf['selected_current_native17_Fortran_Source_freeze_pin']or dt.get(nativepin['path'])!=nativepin or native['schema']!='COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_FORTRAN_SOURCE_ONLY_FREEZE_V1'or native['all_82_original_eligibility_conditions_unchanged']is not False or any(native[k]is not True for k in plan['required_current_native17_Source_true_flags']):raise RuntimeError('actual Native17 object47/SF6e retained unchanged')
    sfrows=unique(sfrows+[nativepin]+native['files']);c.verify_rows(sfrows)
    sp=sf['control_plan_pin'];sourceplan=c.load_json_exact(sp['path'],sp['sha256'],json.dumps(sp['identity']))[0]
    if sp!=plan['A9_false_return_Source_plan_pin']or sourceplan['failed_original_okFalse_return_count']!=111 or sourceplan['original_return_mapping']!=plan['exact_A9_original_false_return_mapping']or sourceplan['normal_MAXOUT_okTrue_acceptedFalse_fallthrough_wholebytes_unchanged']is not True or sourceplan['original_DOORFV64_A8_child_Source_not_instrumented_or_changed']is not True:raise RuntimeError('actual A9 Source111/normal returns/A8 original contract')
'''
def main():
    if OUT.exists()or JOB.exists():raise RuntimeError('unique Source/future runtime')
    originalpath=OLD/'run_guarded_one_BOOT_strict_native17_consumer.py';original=originalpath.read_text();s=original;plan=read(OLD/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json')
    rolepath=R/'readonly_next_A9_core_exact27_role_budget_survey_20261014/REVIEW.json';role=read(rolepath);retired=[norm(x['pin'])for x in role['ordered_literal_candidate_role_rows']];postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);basepin=post['actual_report_pin'];base=read(basepin);live={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};old70=[live[p]for p in base['actual_ordered70_link_inputs']]
    if role['candidate_count']!=27 or role['candidate_logical_bytes']!=1436473280 or len(retired)!=27 or sum(p['size_bytes']for p in retired)!=1436473280 or role['failure']is not None or post['failure']is not None or post['actual_BOOT_return_status']!=2 or post['actual_no_admission_BIND_native_rejection_inventory_or_seal_events']is not True:raise RuntimeError('actual exact27 scope and current Native CORE_FAILED2 only')
    sfpin=pin(R/'boot_v16_A9_111_false_return_diagnostic_source_v1_20261014/COMPLETE_A9_111_FALSE_RETURN_DIAGNOSTIC_SOURCE_FREEZE.json');sf=read(sfpin);ap=sf['control_plan_pin'];a9plan=read(ap)
    if sfpin['sha256']!='ad2968f5c5de9b359f712585f8b71db46fd5cbc72814999267d424da08f7be83'or sf['actual_retained_A9_object2_pin']!=old70[2]:raise RuntimeError('actual once A9SF/slot2 Source authority')
    flags=['whole_file_inverse_byte_equal','only111_original_okFalse_return_site_stdout_and_flush_added','all_original_condition_expressions_single_evaluation_unchanged','all_original_declarations_public_ABI_math_loops_allocations_status_assignments_and_write_order_unchanged','normal_MAXOUT_okTrue_acceptedFalse_fallthrough_wholebytes_unchanged','normal_MAXOUT_would_original_BOOTB_NOT_ACCEPTED3_not_CORE_FAILED2','original_DOORFV64_A8_child_Source_not_instrumented_or_changed','no_new_helper_or_API_or_module_declaration','callee_to_caller_failure_stdout_chain_only']
    if any(sf[k]is not True for k in flags):raise RuntimeError('actual nine A9 source-only obligations')
    mapping=sf['original_return_mapping'];relations={};variables={'VALIDATE_OFFGROUP32':'operator_ok','FLUBAL64':'balance_ok','FLU2AC64':'accel_ok','SCALAR_GROUP_NORM64':'norm_ok'}
    for name,var in variables.items():
        guards=[m['original_return_source_line']for m in mapping if m['scope']=='FLU2DR64_CORE'and '.not. '+var in m['original_statement_complete']]
        if not guards:raise RuntimeError('actual original CORE helper guard Source mapping')
        relations[name]=dict(original_return_boolean_variable=var,CORE_failed_return_source_lines=guards,relationship_derived_from_actual_original_return_statements=True)
    nativepin=plan['selected_bind_Fortran_Source_freeze_pin'];nativeflags=plan['required_BIND_Source_freeze_true_flags'];nextnine=[norm(p)for p in role['next_exact_nine_source_input_copy_pins']];kept18=[norm(p)for p in role['retained_current18_original9_latest_native9_input_pins']]
    if len(nextnine)!=9 or len(kept18)!=18 or any(live.get(p['path'])!=p for p in nextnine)or set(p['path']for p in kept18)&set(p['path']for p in retired):raise RuntimeError('actual current18 retained, latest Native9 only new inputs')
    def change(before,after):
        nonlocal s
        if s.count(before)!=1:raise RuntimeError('unique A9 Host splice '+before[:80])
        s=s.replace(before,after,1)
    def glob(before,after):
        nonlocal s
        if not s.count(before):raise RuntimeError('nonempty A9 literal splice')
        s=s.replace(before,after)
    glob('exact11','exact27');glob('bind-source-freeze','a9-source-freeze');glob('selected_bind_Fortran_Source_freeze_pin','selected_A9_Fortran_Source_freeze_pin')
    glob('BIND47_STRICT_NATIVE17_CONSUMER','A9_111_FALSE_RETURN_DIAGNOSTIC')
    change("OUT=R/'validation/artifacts/axial-material-new-one-BOOT-strict-native17-consumer-20261014-v1'","OUT=R/'validation/artifacts/axial-material-new-one-BOOT-A9-false-return-diagnostic-20261014-v1'")
    change("SF_SCHEMA='COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_FORTRAN_SOURCE_ONLY_FREEZE_V1'","SF_SCHEMA='COMPLETE_SPOR64_A9_111_FALSE_RETURN_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'")
    def fn(name):return ast.get_source_segment(s,next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name==name))
    commands=fn('make_commands');commands=commands.replace("Path(old[47]).name!='SPOR64_BOOT_BIND64.o'","old[47]!=plan['retained_actual_current_native17_BIND47_pin']['path']or old[2]!=plan['retained_actual_A9_object2_pin']['path']or Path(old[2]).name!='SPOR64_A9.o'").replace("obj=str(OUT/'build/SPOR64_BOOT_BIND64.o');new=list(old);new[47]=obj","obj=str(OUT/'build/SPOR64_A9.o');new=list(old);new[2]=obj").replace('!=[47]','!=[2]').replace('only object47','only object2')
    change(fn('make_commands'),commands)
    outcome=fn('read_BOOT_outcome');outcome=outcome.replace("    if w['returncode']==1:","    a9_events=[r for r in rows if r.get('schema')=='ACTUAL_SPOR64_A9_FAILED_RETURN_DIAGNOSTIC_V1']\n    if w['returncode']==1:")
    outcome=outcome.replace("        return dict(kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY'", "        a9chain=parse_A9_failed_return_chain(rows,plan)if status==2 else []\n        if status!=2 and a9_events:raise RuntimeError('A9 false-return events only at original CORE_FAILED2, never normal MAXOUT/status1/3..8')\n        if any(rows.index(e)>=rows.index(row)for e in a9chain):raise RuntimeError('actual A9 callee→CORE events precede outer status2')\n        return dict(actual_A9_failed_return_chain=a9chain,actual_A9_first_false_return=a9chain[0]if a9chain else None,kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY'")
    outcome=outcome.replace("or native_events or len(seals)!=1","or native_events or a9_events or len(seals)!=1")
    change(fn('read_BOOT_outcome'),A9_PARSER+'\n'+outcome)
    change("post['actual_BOOT_return_status']!=1","post['actual_BOOT_return_status']!=2")
    change("or post['actual_unique_first_admission_predicate']['original_return_source_line']!=466", "or post['actual_no_admission_BIND_native_rejection_inventory_or_seal_events']is not True")
    begin="    if post['schema']!='INDEPENDENT_BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'";end="    if psf!=hf['selected_A9_Fortran_Source_freeze_pin']";a=s.index(begin);z=s.index(end,a)
    s=s[:a]+"    if post['schema']!='INDEPENDENT_BIND47_STRICT_NATIVE17_CONSUMER_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_BIND47_STRICT_NATIVE17_CONSUMER_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_CORE_specific_first_failure_reason_still_unknown']is not True:raise RuntimeError('actual prior CORE_FAILED2 no helper reason assumed')\n    if base['schema']!='ACTUAL_GUARDED_ONE_BOOT_BIND47_STRICT_NATIVE17_CONSUMER_V1'or base['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or base['failure']!=post['actual_summary_failure']or base['actual_outcome']!=post['actual_summary_outcome_metadata']or base['actual_host_Source_freeze_pin']!=hf['selected_prior_probe_Host_freeze_pin']or base['full50_executed']is not False or base['engineering_qualified']is not False:raise RuntimeError('actual sealed prior Native CORE_FAILED2 and first error retained')\n"+s[z:]
    a=s.index("    if psf!=hf['selected_A9_Fortran_Source_freeze_pin']");z=s.index("    v16pin=plan['actual_closed_v16_report_pin']",a);s=s[:a]+A9_ADMIT+s[z:]
    glob('len(retired)!=11','len(retired)!=27');glob("len({r['path']for r in retired})!=11","len({r['path']for r in retired})!=27");glob('1330716816','1436473280');glob("release['deleted_files']!=11","release['deleted_files']!=27");glob('len(rr)!=11','len(rr)!=27')
    glob('SPOR64_BOOT_BIND64.o','SPOR64_A9.o');glob('spor64_boot_bind64.mod','spor64_a9.mod');glob('selected_original_BIND_module_pin','selected_original_A9_module_pin')
    glob('retained_original9_old_diag4_eight_old_BOOTB_eight_latest_inventory_nine_input_sources_full_EOF_and_all7_preserved','retained_original9_latest_native_nine_input_sources_full_EOF_and_all7_preserved')
    change('replacement_zero_based_link_index=47','replacement_zero_based_link_index=2')
    ast.parse(s)
    guards=['load_common','unique','rewrite_summary','empty_final_metadata_kind','classify_storage_inventory','FirstFatal','PhaseResources','genuine_terminal']
    def defs(x):return{n.name:ast.get_source_segment(x,n)for n in ast.parse(x).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    f0=defs(original);f1=defs(s)
    if any(f0[n]!=f1[n]for n in guards)or f0['parse_BIND_return_chain']!=f1['parse_BIND_return_chain']or f0['parse_failed_PHYS_inventory']!=f1['parse_failed_PHYS_inventory']:raise RuntimeError('eight original guards and original BIND/inventory parsers unchanged')
    plan={k.replace('exact11','exact27'):v for k,v in plan.items()}
    for key in ['retained_old_diag4_remaining_eight_copy_pins','retained_prior_probe_eight_input_copy_pins','retained_latest_probe_nine_input_copy_pins','retained_latest_inventory_nine_input_copy_pins','current34_original9_oldDiag8_oldBOOTB8_latestInventory9_input_pins','all_original9_old_diag4_eight_old_BOOTB8_latestInventory9_inputs_and_current70_retained','actual_retirement_external_pins','Source_generator_pin','reviewed_core_draft_complete_metadata_pins','required_BIND_Source_freeze_true_flags']:
        plan.pop(key,None)
    plan.update(schema='SOURCE_ONLY_GUARDED_ONE_BOOT_A9_111_FALSE_RETURN_HOST_CORE_DRAFT_V1',source_only=True,draft_only=True,runtime_authorities_complete=False,planned_output_root=str(JOB),diagnostic_Source_pin=sf['diagnostic_source_pin'],selected_A9_Fortran_Source_freeze_pin=sfpin,selected_A9_Fortran_Source_freeze_path=sfpin['path'],selected_current_native17_Fortran_Source_freeze_pin=nativepin,required_current_native17_Source_true_flags=nativeflags,required_A9_Source_freeze_true_flags=flags,A9_false_return_Source_plan_pin=ap,exact_A9_original_false_return_mapping=mapping,exact_A9_scope_counts=sf['scope_counts'],actual_original_A9_helper_to_CORE_failed_guard_map=relations,retained_actual_current_native17_BIND47_pin=old70[47],retained_actual_A9_object2_pin=old70[2],selected_original_A9_module_pin=sf['original_module_pin'],actual_prior_probe_report_pin=basepin,selected_prior_probe_Host_freeze_pin=post['actual_Host_freeze_pin'],selected_prior_probe_Root_tool_pin=post['actual_Root_true_tool_return_pin'],selected_prior_probe_actual_post_review_pin=postpin,selected_prior_probe_actual_post_tools_pin=role['genuine_latest_actual_post_true_tool_pin'],current_ordered70_input_pins=old70,base_Dragon_pin=live[base['records'][1]['command'][-1]],original_compile_include_arguments=[x for x in base['records'][0]['command']if x.startswith('-I')],owned_readonly_input_rows=[dict(owned_filename=Path(p['path']).name,target_pin=p)for p in nextnine],retained_latest_native_nine_input_copy_pins=nextnine,retained_current18_original9_latest_native9_input_pins=kept18,truthful_current_retained_input_source_count=18,all_original9_and_latest_native9_current18_inputs_and_current70_retained=True,exact_historical_retired_private_body_pins=retired,exact_historical_retired_private_body_count=27,exact_historical_retired_private_body_bytes=1436473280,only_replacement_zero_based_index=2,expected_compile_directory_files=sorted(['SPOR64_A9.o','spor64_a9.mod','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json']),expected_final_build_directory_files=sorted(['SPOR64_A9.o','spor64_a9.mod','compile_BOOT_diagnostic.log','compile_BOOT_diagnostic.watchdog.json','link_Dragon.log','link_Dragon.watchdog.json']),selected_exact27_actual_release_pin=None,selected_exact27_actual_Root_tool_pin=None,selected_exact27_actual_post_review_pin=None,selected_exact27_actual_post_tools_pin=None,selected_exact27_actual_manifest_pin=None,selected_exact27_post_schema=None,selected_exact27_post_status=None,selected_exact27_release_Source_freeze_pin=None,selected_exact27_release_schema=None,selected_exact27_release_status=None,actual_retirement_external_pins=None,Source_role_survey_pin=pin(rolepath),current_MF8482_exact25_history_indices=role['current_MF8482_exact25_candidate_indices'],current_HF3696_exact25_history_indices=role['current_HF3696_exact25_candidate_indices'],A9_false_events_only_original_status2=True,A9_success309_490_and_normal_MAXOUT_not_failed_events=True,current_root_authority_is_latest3697fixed27outputs_HF3696=True,actual_Fortran_Source_freeze_creation_true_tool_pin=pin(R/'ACTUAL_A9_111_FALSE_RETURN_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json'),core_draft_predecessor_Host_pin=pin(originalpath),future_actual_A9_first_scope=None,future_actual_A9_first_predicate_ID=None,future_own_Host_freeze_pin=None)
    OUT.mkdir();hp=OUT/HOST;write(hp,s);pp=OUT/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json';write(pp,plan);ip=OUT/'COMPLETE_NATIVE17_HOST_TO_A9_111_ONLY2_CORE_SOURCE_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_NATIVE17_HOST_TO_A9_111_ONLY2_CORE_SOURCE_WHOLE_BYTE_INVERSE_V1',original_Host_pin=pin(originalpath),candidate_Host_pin=pin(hp),changes=[dict(before=original,after=s)],whole_Source_inverse_exact=s.replace(s,original,1).encode()==originalpath.read_bytes(),eight_original_guard_classes_methods_wholebytes_equal=guards,original_BIND82_and_header_inventory_parsers_wholebytes_equal=True,source_only=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False));rp=OUT/'SOURCE_ONLY_DRAFT_READY.json';write(rp,dict(schema='SOURCE_ONLY_A9_111_GUARDED_HOST_CORE_DRAFT_READY_V1',status='SOURCE_ONLY_CORE_READY_PENDING_REAL_EXACT27_RETIREMENT_PROOFS',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),Source_author_pin=pin(__file__),selected_A9_Fortran_Source_freeze_pin=sfpin,retained_native17_BIND47_Source_freeze_pin=nativepin,only_object2_replaced=True,other69_unchanged=True,current_input_source_count18=18,target_count27=27,target_bytes1436473280=1436473280,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_true_tool_pin=None,future_actual_Root_argv_pin=None,future_actual_post_review_pin=None,future_actual_post_tools_pin=None,actual_Host_freeze_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False))
    print(json.dumps(dict(status='SOURCE_ONLY_A9_111_GUARDED_HOST_CORE_READY_NO_RUNTIME',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),ready_pin=pin(rp),Source_author_pin=pin(__file__),runtime_authorities_complete=False,only_object2_replaced=True,other69_unchanged=True,eight_original_guard_methods_wholebytes_equal=True,business_executed=False,compiler_executed=False,numerical_executed=False,files_deleted=False)))
if __name__=='__main__':main()
