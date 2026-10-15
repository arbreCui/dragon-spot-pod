"""Author a guarded native17 BOOT Host draft only; no Host import/compiler/run/delete."""
import ast,hashlib,json,os,re,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'boot_v16_BIND47_failed_PHYS_inventory_diagnostic_host_source_v1_20261014'
OUT=R/'boot_v16_BIND47_strict_native17_consumer_host_source_draft_v1_20261014'
HOST='run_guarded_one_BOOT_strict_native17_consumer.py'
ART=Path('/Users/wen/spot/validation/artifacts')
JOB=ART/'axial-material-new-one-BOOT-strict-native17-consumer-20261014-v1'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened Source7')
        d=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('FD Source7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after Source7')
    return dict(path=str(p),sha256=hashlib.sha256(d).hexdigest(),size_bytes=len(d),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact Source/metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
def write(p,v):
    d=(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(v,dict)else v.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(d);f.flush();os.fsync(f.fileno())

NEW_OUTCOME=r'''def read_BOOT_outcome(c,runner,expected_error,expected_tb,plan):
    record=runner.records[-1];wp=c.pin(WORK/'BOOT_diagnostic.watchdog.json');lp=c.pin(WORK/'BOOT_diagnostic.log')
    w=json.loads(Path(wp['path']).read_text());text=Path(lp['path']).read_text();rows=[]
    for line in text.splitlines():
        if len(line)>65536:raise RuntimeError('bounded actual diagnostic JSON/log line')
        if line.strip().startswith('{')and line.strip().endswith('}'):
            row=json.loads(line)
            if isinstance(row,dict):rows.append(row)
    if w['command']!=record['command']or w['rss_cap_mib']!=512 or w['own_child_only']is not True or w['liveness_group_cleanup']is not True or \
       w['limit_failure']is not None or not 0<=w['sampled_peak_rss_mib']<512 or not 0<w['elapsed_seconds']<w['wall_cap_seconds']<=600 or type(w['returncode'])is not int:raise RuntimeError('true own-child closed BOOT watch with unchanged caps')
    diagnostics=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_EXACT_FAILURE_STATUS_DIAGNOSTIC_V1']
    seals=[r for r in rows if r.get('schema')=='ACTUAL_XSM_SEALED_PAIR_COMPLETE_COPY_READBACK_V1']
    predicates=[r for r in rows if r.get('schema')=='ACTUAL_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_V1']
    completed=[line for line in text.splitlines()if line.strip()=='ACTUAL-AAA3-TRUE-ONLINE-BOOT-COMPLETE']
    bind_events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1']
    inventory_events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1']
    native_events=[r for r in rows if r.get('schema')=='ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1']
    if w['returncode']==1:
        if expected_error is None or str(expected_error)!='own-child stage failed; no retry'or record['status']!='FAILED'or \
           text.count('SPOBOOX64: ACTUAL STRICT SOLVE NOT COMMITTED.')!=1 or len(diagnostics)!=1 or seals or completed:raise RuntimeError('exact original strict BOOT abort1 stays FAILED, never PASS')
        row=diagnostics[0];status=row.get('actual_return_status')
        if type(row.get('boot_plane'))is not int or row['boot_plane']not in(1,2,3)or type(status)is not int or status not in range(1,8)or type(row.get('required_committed_status'))is not int or row['required_committed_status']!=8:raise RuntimeError('actual failure plane1..3/original status1..7/required8')
        meaning=plan['original_BOOT_status_mapping'][str(status)]
        predicate=None;chain=[];native=None;inventory=dict(actual_inventory_header_events_observed=False,actual_complete_header_inventory_observed=False,actual_caller=None)
        if status==1:
            if len(predicates)!=1:raise RuntimeError('original admission-failed1 requires unique actual BOOTB first return')
            predicate=predicates[0];line=predicate.get('original_return_source_line');mapping={p['predicate_id']:p for p in plan['exact_BOOTB216_first_return_mapping']};m=mapping.get(predicate.get('predicate_id'))
            if set(predicate)!={'schema','predicate_id','original_return_source_line','actual_return_status'}or m is None or type(line)is not int or line!=m['original_return_source_line']or type(predicate.get('actual_return_status'))is not int or predicate['actual_return_status']!=1:raise RuntimeError('one of actual Source-derived original216 admission return IDs/lines/status1')
            if line==466:
                chain=parse_BIND_return_chain(rows,plan);inventory=parse_failed_PHYS_inventory(rows,chain,row)
                if any(rows.index(e)>=rows.index(predicate)for e in chain):raise RuntimeError('all original BIND nested events precede BOOTB466')
                if len(native_events)>1:raise RuntimeError('at most one native17 failed guard event')
                if native_events:
                    native=native_events[0];ids={p['predicate_id']for p in plan['exact_native17_rejection_Source_mapping']};by={e['scope']:e for e in chain};response=by.get('RESPONSE_GROUP_IS_EXACT');system=by.get('SYSTEM_PAYLOAD_IS_VALID')
                    if set(native)!={'schema','predicate_id','actual_boolean_status_integer'}or native['predicate_id']not in ids or type(native['actual_boolean_status_integer'])is not int or native['actual_boolean_status_integer']!=0 or response is None or response['original_return_source_line']!=236 or system is None or system['original_return_source_line']!=168 or by['SPOR64_BOOT_BIND64_READ']['original_return_source_line']!=97 or rows.index(native)>=rows.index(response):raise RuntimeError('Source native17 failed guard only before RESPONSE236→SYSTEM168→READ97→BOOTB466')
            elif bind_events or inventory_events or native_events:raise RuntimeError('BIND/native/inventory failed events only under original BOOTB466 caller')
            if rows.index(predicate)>=rows.index(row):raise RuntimeError('original first-admission JSON must precede outer status JSON')
        elif predicates or bind_events or inventory_events or native_events:raise RuntimeError('original status2..7 does not require or admit failed pre-core admission events')
        return dict(kind='REAL_ORIGINAL_BOOT_ABORT1_DIAGNOSTIC_ONLY',actual_exit_code=1,actual_failed_record_preserved=True,actual_diagnostic=row,original_status_symbol=meaning['symbol'],original_status_assignment_Source_evidence=meaning,progress_description_is_original_Source_assignment_inference_not_measured_solver_or_commit_qualification=True,actual_first_admission_predicate=predicate,actual_BIND_failed_return_chain=chain,actual_BIND_first_explicit_return=chain[0]if chain else None,actual_native17_rejection=native,actual_failed_PHYS_group_inventory=inventory,actual_log_pin=lp,actual_watchdog_pin=wp,original_expected_child_error_repr=repr(expected_error),original_expected_child_traceback_preserved=True,engineering_qualified=False,physics_qualified=False),None
    if w['returncode']!=0 or expected_error is not None or record['status']!='PASS'or diagnostics or predicates or bind_events or inventory_events or native_events or len(seals)!=1 or \
       seals[0].get('status')!='PASS'or seals[0].get('all_payload_bits_equal')is not True or seals[0].get('complete_lifecycle_checked')is not True or \
       (seals[0].get('groups'),seals[0].get('planes'),seals[0].get('epoch'))!=(370,3,0)or 'normal end of execution'not in text or len(completed)!=1:
        if expected_error is not None:raise expected_error.with_traceback(expected_tb)
        raise RuntimeError('original status8/process0 requires genuine full370×3 sealed-pair readback; no missing-event qualification')
    return dict(kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0,original_status_symbol=plan['original_BOOT_status_mapping']['8']['symbol'],actual_Fortran_complete_copy_readback=seals[0],actual_log_pin=lp,actual_watchdog_pin=wp,full50_executed=False,engineering_qualified=False,physics_qualified=False),seals[0]'''

def main():
    if OUT.exists()or JOB.exists():raise RuntimeError('unique Source and future business namespace')
    original=OLD/'run_guarded_one_BOOT_failed_PHYS_inventory_diagnostic.py';old=original.read_text();current=old;changes=[];plan=read(OLD/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json')
    rolepath=R/'readonly_next_native17_BIND_probe_exact11_private_role_and_current_budget_survey_20261014/REVIEW.json';role=read(rolepath);targets=[norm(p['pin'])for p in role['ordered_literal_candidate_role_rows']]
    postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);basepin=post['actual_report_pin'];base=read(basepin);posttools=role['genuine_latest_actual_post_true_tool_pin'];pt=read(posttools);pa=pt['actual_review_return']
    if role['candidate_count']!=11 or role['candidate_logical_bytes']!=1330716816 or len(targets)!=11 or len({p['path']for p in targets})!=11 or sum(p['size_bytes']for p in targets)!=1330716816 or role['failure']is not None or post['failure']is not None or post['verification_failure']is not None or post['actual_Root_exit_code']!=1 or post['actual_Root_closed']is not True or pt['observed_closed']is not True or type(pa['exit_code'])is not int or pa['exit_code']!=0 or pa.get('session_id')is not None or norm(json.loads(pa['output'].strip().splitlines()[-1])['review_pin'])!=postpin:raise RuntimeError('actual exact11 role and latest genuine inventory failure post0 only')
    sfp=pin(R/'boot_v16_BIND64_strict_native17_consumer_source_v1_20261014/COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_SOURCE_FREEZE.json');sf=read(sfp);sp=sf['control_plan_pin'];sourceplan=read(sp)
    flags=['public_and_private_function_signatures_and_module_declarations_unchanged','legacy15_and_P3_forms_and_all_original_subsequent_typed_finite_macro_bit_checks_preserved','only_PACA4_exact_native17_complete_inventory_plus_strict_native_payload_validation_added','no_solver_flux_source_formula_record_value_tolerance_resource_cap_changed','original_82_events_and_returns_preserved_and_only_original236_eligibility_extended']
    if sfp['sha256']!='6e454f420ab956bf48c4999a17d95891f3b05f23cd79fe67175a9265c759d819'or sf['schema']!='COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_FORTRAN_SOURCE_ONLY_FREEZE_V1'or any(sf[k]is not True for k in flags)or sf['all_82_original_eligibility_conditions_unchanged']is not False:raise RuntimeError('explicit strict native17 contract, not old inventory-only or all82-eligibility-unchanged flags')
    bt=R/'boot_v16_BOOTB_first_admission_predicate_diagnostic_source_v1_20261014';bsfp=pin(bt/'COMPLETE_BOOTB_FIRST_ADMISSION_PREDICATE_DIAGNOSTIC_SOURCE_FREEZE.json');bsf=read(bsfp);bi=read(bsf['complete_byte_inverse_pin']);predmap=[{k:x[k]for k in('predicate_id','original_return_source_line','original_statement_start_source_line','before')}for x in bi['changes']]
    if len(predmap)!=216 or len({x['predicate_id']for x in predmap})!=216 or any(x['predicate_id']!='BOOTB_INGRESS_RETURN_L'+str(x['original_return_source_line']).zfill(4)for x in predmap):raise RuntimeError('actual BOOTB216 original Source/inverse first-return mapping')
    statusmap={};statuspins=[]
    for path,prefix,expected in [(R/'online_boot_native64_source_v1/SPOR64_BOOTB64.f90','SPOR64_BOOTB64_',list(range(1,5))),(R/'online_boot_native64_source_v1/SPOR64_BOOTC64.f90','SPOR64_BOOTC64_',list(range(5,9)))]:
        pp=pin(path);statuspins.append(pp);lines=path.read_text().splitlines();defs=[]
        for i,line in enumerate(lines,1):
            m=re.fullmatch(r'\s*integer, parameter, public :: (SPOR64_BOOT[BC]64_[A-Z_]+) = ([1-8])\s*',line)
            if m and not m[1].endswith(('_BOOT','_CONT')):
                number=int(m[2]);assign=[dict(source_line=j,statement=s)for j,s in enumerate(lines,1)if re.fullmatch(r'\s*status\s*=\s*'+re.escape(m[1])+r'\s*',s)]
                if not assign:raise RuntimeError('actual original status assignment evidence')
                statusmap[str(number)]=dict(status_integer=number,symbol=m[1],original_Source_pin=pp,definition_source_line=i,definition_statement=line,original_assignment_sites=assign,Source_assignment_inference_only=True);defs.append(number)
        if defs!=expected:raise RuntimeError('actual original BOOTB20..23 and BOOTC15..18 enum, no invented statuses')
    native_text=Path(sf['consumer_Source_pin']['path']).read_text();nativemap=[]
    for pid in sourceplan['native17_rejection_predicate_ids']:
        hits=[(i,line)for i,line in enumerate(native_text.splitlines(),1)if '"predicate_id":"'+pid+'"'in line]
        if len(hits)!=1:raise RuntimeError('native7 unique actual Fortran stdout predicate IDs')
        nativemap.append(dict(predicate_id=pid,actual_consumer_Source_pin=sf['consumer_Source_pin'],actual_Source_line=hits[0][0],actual_statement=hits[0][1],actual_boolean_status_integer=0))
    live={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};ordered=[live[p]for p in base['actual_ordered70_link_inputs']]
    nextnine=[norm(p)for p in role['next_exact_nine_source_input_copy_pins']];kept34=[norm(p)for p in role['current34_original9_oldDiag8_oldBOOTB8_newest_inventory9_preserved_input_pins']]
    if len(ordered)!=70 or len(nextnine)!=9 or len(kept34)!=34 or any(live.get(p['path'])!=p for p in nextnine)or set(p['path']for p in kept34)&set(p['path']for p in targets):raise RuntimeError('exact latest actual70 and latest nine sourcecopies/current34 keep roles')
    for p in ordered+kept34:
        if identity(Path(p['path']).lstat())!=p['identity']:raise RuntimeError('current metadata7 only, no scientific EOF')
    def change(before,after):
        nonlocal current
        if current.count(before)!=1:raise RuntimeError('unique Host Source splice')
        current=current.replace(before,after,1);changes.append(dict(before=before,after=after))
    def global_change(before,after):
        nonlocal current
        count=current.count(before)
        if not count:raise RuntimeError('nonempty exact Host namespace splice')
        previous=current;current=current.replace(before,after);changes.append(dict(before=previous,after=current,occurrence_count=count,reason='literal namespace field change'))
    global_change('exact3','exact11')
    global_change('BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC','BIND47_STRICT_NATIVE17_CONSUMER')
    global_change('BIND47_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC','BIND47_STRICT_NATIVE17_CONSUMER')
    change("OUT=R/'validation/artifacts/axial-material-new-one-BOOT-failed-PHYS-group-inventory-diagnostic-20261014-v1'","OUT=R/'validation/artifacts/axial-material-new-one-BOOT-strict-native17-consumer-20261014-v1'")
    change("SF_SCHEMA='COMPLETE_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'","SF_SCHEMA='COMPLETE_BOOT_BIND64_STRICT_NATIVE17_CONSUMER_FORTRAN_SOURCE_ONLY_FREEZE_V1'")
    def fn(name):return ast.get_source_segment(current,next(n for n in ast.parse(current).body if isinstance(n,ast.FunctionDef)and n.name==name))
    change(fn('read_BOOT_outcome'),NEW_OUTCOME)
    change("len(retired)!=3 or len({r['path']for r in retired})!=3 or sum(r['size_bytes']for r in retired)!=1277838584","len(retired)!=11 or len({r['path']for r in retired})!=11 or sum(r['size_bytes']for r in retired)!=1330716816")
    change("release['deleted_files']!=3 or release['logical_bytes_released']!=1277838584","release['deleted_files']!=11 or release['logical_bytes_released']!=1330716816")
    change('or len(rr)!=3 or [r[\'original_fullpin\']for r in rr]!=retired','or len(rr)!=11 or [r[\'original_fullpin\']for r in rr]!=retired')
    change("lpost['failure']is not None or not lpost['status'].startswith('PASS')","lpost['failure']is not None or lpost['schema']!=plan['selected_exact11_post_schema']or lpost['status']!=plan['selected_exact11_post_status']")
    change("    if post['schema']!='INDEPENDENT_BIND47_EXPLICIT_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_BIND47_EXPLICIT_RETURN_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_unique_BIND_failed_return_chain']!=plan['actual_prior_failed_BIND_chain']or post['known_sealed_summary_metadata_discrepancy']['original_source_or_sealed_report_modified']is not False:raise RuntimeError('genuine prior RESP236/SYSTEM168/READ97/BOOTB466 failure facts and transparent parser defect')", "    if post['schema']!='INDEPENDENT_BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_BIND47_FAILED_PHYS_INVENTORY_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_unique_BIND_failed_return_chain']!=plan['actual_prior_failed_BIND_chain']or post['actual_failed_PHYS_complete_header_inventory']['actual_complete_header_inventory_observed']is not True or post['actual_failed_GROUP_caller_ig']!=1 or post['actual_failed_GROUP_caller_plane']!=1 or post['actual_missing_expected_PHYS15_names']!=[]or post['inventory_data_is_only_group1_plane1_headers_not_payload_finiteness_or_full370_pass']is not True:raise RuntimeError('real prior complete17 headers and original236→168→97→466; no payload or other369 claim')")
    change("base['schema']!='ACTUAL_GUARDED_ONE_BOOT_BIND47_EXPLICIT_RETURN_DIAGNOSTIC_V1'","base['schema']!='ACTUAL_GUARDED_ONE_BOOT_BIND47_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_V1'")
    change("base['actual_outcome']is not None","base['actual_outcome']!=post['actual_summary_outcome_metadata']")
    change("sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['diagnostic_plan_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)","sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['consumer_Source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)\n    if sf['consumer_Source_pin']!=sf['diagnostic_source_pin']or sf['all_82_original_eligibility_conditions_unchanged']is not False or sf['Source_extension_explicitly_limited_to_original236_PACA4_exact_inventory_branch']is not True:raise RuntimeError('explicit native17 extension is not an unchanged all82 inventory gate')")
    change("    if sp!=plan['failed_PHYS_inventory_Source_plan_pin']or sourceplan['failed_source_SITE']!=236 or sourceplan['failed_caller_SITE']!=168 or sourceplan['inventory_event_schema']!='ACTUAL_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_V1'or sourceplan['maximum_actual_inventory_records']!=64 or sourceplan['actual_record_content_not_read_or_dumped']is not True or sourceplan['native_schema_gate_not_changed']is not True:raise RuntimeError('actual frozen header-only64 diagnostic Source contract, unchanged original native inventory gate')", "    if sp!=plan['strict_native17_consumer_Source_plan_pin']or sourceplan['schema']!='SOURCE_ONLY_PRIVATE_BIND64_STRICT_NATIVE17_CONSUMER_PLAN_V1'or sourceplan['native17_fixed_scope']!={'nreg':8,'nunkno':14,'nsurf':6,'paca':4,'lc0':0}or sourceplan['native17_complete_names']!=plan['native17_complete_names']or sourceplan['native17_rejection_event_schema']!='ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1'or sourceplan['native17_rejection_predicate_ids']!=[r['predicate_id']for r in plan['exact_native17_rejection_Source_mapping']]or sourceplan['original15_and_P3_exact_forms_and_original_all_subsequent_checks_preserved']is not True or sourceplan['original_EXACT_INVENTORY_not_modified']is not True:raise RuntimeError('exact Source native17 shapes/finite/demote words and preserved legacy15/P3 contract')")
    global_change('retained_original9_old_diag4_eight_prior_probe_eight_latest_probe_nine_input_sources_full_EOF_and_all7_preserved','retained_original9_old_diag4_eight_old_BOOTB_eight_latest_inventory_nine_input_sources_full_EOF_and_all7_preserved')
    ast.parse(current)
    guards=['load_common','unique','rewrite_summary','empty_final_metadata_kind','classify_storage_inventory','FirstFatal','PhaseResources','genuine_terminal']
    def defs(src):return{n.name:ast.get_source_segment(src,n)for n in ast.parse(src).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    f0=defs(old);f1=defs(current)
    if any(f0[n]!=f1[n]for n in guards)or f0['make_commands']!=f1['make_commands']or f0['parse_BIND_return_chain']!=f1['parse_BIND_return_chain']or f0['parse_failed_PHYS_inventory']!=f1['parse_failed_PHYS_inventory']:raise RuntimeError('original guards/math70/82chain/bounded inventory parsers changed')
    for before in ["        try:runner.execute(WORK,'BOOT_diagnostic',planned[2],600,deck=deck.name)","            expected=exc;tb=exc.__traceback__;first.capture(exc,'actual_original_failed_BOOT_child')","    first.reraise()"]:
        if before not in current:raise RuntimeError('original actual failure object and TB preserved')
    plan={k.replace('exact3','exact11'):v for k,v in plan.items()}
    for key in ['failed_PHYS_inventory_Source_plan_pin','inventory_Host_draft_v1_pin','Source_generator_pin','actual_retirement_external_pins','reviewed_core_draft_complete_metadata_pins','selected_exact11_actual_release_pin','selected_exact11_actual_Root_tool_pin','selected_exact11_actual_post_review_pin','selected_exact11_actual_post_tools_pin','selected_exact11_actual_manifest_pin']:
        plan.pop(key,None)
    plan.update(schema='SOURCE_ONLY_GUARDED_ONE_BOOT_BIND47_STRICT_NATIVE17_CONSUMER_HOST_DRAFT_V1',draft_only=True,runtime_authorities_complete=False,planned_output_root=str(JOB),diagnostic_Source_pin=sf['consumer_Source_pin'],selected_bind_Fortran_Source_freeze_pin=sfp,selected_bind_Fortran_Source_freeze_path=sfp['path'],strict_native17_consumer_Source_plan_pin=sp,required_BIND_Source_freeze_true_flags=flags,exact_BIND_original_return_mapping=sf['original_explicit_return_mapping'],exact_BIND_scope_count=sf['exact_scope_counts'],exact_BOOTB216_first_return_mapping=predmap,selected_original_BOOTB216_Source_freeze_pin=bsfp,original_BOOT_status_mapping=statusmap,original_BOOT_status_definition_and_assignment_Source_pins=statuspins,exact_native17_rejection_Source_mapping=nativemap,native17_complete_names=sourceplan['native17_complete_names'],native17_fixed_scope=sourceplan['native17_fixed_scope'],native17_checks=sourceplan['native17_checks'],actual_prior_probe_report_pin=basepin,selected_prior_probe_Host_freeze_pin=post['actual_Host_freeze_pin'],selected_prior_probe_Root_tool_pin=post['actual_Root_true_tool_return_pin'],selected_prior_probe_actual_post_review_pin=postpin,selected_prior_probe_actual_post_tools_pin=posttools,base_Dragon_pin=next(norm(p)for p in base['output_pins']if p['path']==base['records'][1]['command'][-1]),current_ordered70_input_pins=ordered,original_compile_include_arguments=[v for v in base['records'][0]['command']if v.startswith('-I')],retained_Driver37_pin=ordered[37],retained_BOOTQ40_pin=ordered[40],retained_math57_pin=ordered[57],retained_actual_prior_BOOTB49_pin=ordered[49],retained_actual_prior_BOXX68_pin=ordered[68],original_four_archive_pins=[p for p in ordered if p['path'].endswith('.a')],owned_readonly_input_rows=[dict(owned_filename=Path(p['path']).name,target_pin=p)for p in nextnine],retained_latest_probe_nine_input_copy_pins=nextnine,retained_latest_inventory_nine_input_copy_pins=nextnine,historical_prior_BIND_nine_input_copy_pins=targets[2:],historical_prior_BIND_nine_current_pins=None,current34_original9_oldDiag8_oldBOOTB8_latestInventory9_input_pins=kept34,truthful_current_retained_input_source_count=34,exact_original_return_source_lines=[p['original_return_source_line']for p in predmap],exact_historical_retired_private_body_pins=targets,exact_historical_retired_private_body_count=11,exact_historical_retired_private_body_bytes=1330716816,selected_exact11_actual_release_pin=None,selected_exact11_actual_Root_tool_pin=None,selected_exact11_actual_post_review_pin=None,selected_exact11_actual_post_tools_pin=None,selected_exact11_actual_manifest_pin=None,selected_exact11_post_schema=None,selected_exact11_post_status=None,actual_retirement_external_pins=None,selected_exact11_release_Source_freeze_pin=pin(R/'storage_release_literal11_next_native17_BIND_duplicates_source_v2_20261014/COMPLETE_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_SOURCE_FREEZE.json'),selected_exact11_release_schema='ACTUAL_EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_OLD_PRIVATE_RELEASE_RECEIPT_V1',selected_exact11_release_status='EXACT_LITERAL11_NEXT_NATIVE17_BIND_DUPLICATES_OLD_PRIVATE_RELEASE_ALL_RETAINED_FULL_EOF_VERIFIED',Source_role_survey_pin=pin(rolepath),actual_prior_failed_BIND_chain=post['actual_unique_BIND_failed_return_chain'],actual_prior_observed_group1_plane1_inventory_headers_only=True,actual_prior_native_payload_and_other369_not_claimed=True,actual_Fortran_Source_freeze_creation_true_tool_pin=pin(R/'ACTUAL_STRICT_NATIVE17_BIND_CONSUMER_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json'),core_draft_predecessor_Host_pin=pin(original),future_own_Host_freeze_pin=None,future_actual_native17_payload_checks_all370_passed=None,all_original9_old_diag4_eight_old_BOOTB8_latestInventory9_inputs_and_current70_retained=True,ancestor_exact_eleven_targets_historical_only_no_current_read=True,no_generic_missing_pin_skip=True,no_recursive_historical_PF_body_promotion=True,original_status_mapping_derived_from_original_definitions_and_actual_assignment_sites=True,all1to7_actual_failures_remain_FAILED_and_original_first_error_object_TB=True,status8_requires_full370x3_pair_seal_and_terminal_readback=True,single_BOOT0_never_full50_or_physics_qualification=True)
    plan.pop('all_original9_old_diag4_eight_prior8_latest9_inputs_and_current70_retained',None)
    back=current
    for c in reversed(changes):
        if back.count(c['after'])!=1:raise RuntimeError('unique whole Host inverse')
        back=back.replace(c['after'],c['before'],1)
    if back.encode()!=original.read_bytes():raise RuntimeError('complete Host inverse')
    OUT.mkdir();write(OUT/HOST,current);pp=OUT/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json';write(pp,plan)
    ip=OUT/'COMPLETE_INVENTORY_HOST_TO_STRICT_NATIVE17_CONSUMER_DRAFT_SOURCE_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_INVENTORY_HOST_TO_STRICT_NATIVE17_CONSUMER_DRAFT_SOURCE_WHOLE_BYTE_INVERSE_V1',original_Host_pin=pin(original),candidate_Host_pin=pin(OUT/HOST),changes=changes,whole_source_inverse_equal=True,eight_original_guard_methods_wholebytes_equal=guards,original_make_commands_and_BIND82_chain_and_bounded_inventory_parsers_wholebytes_equal=True,original_first_actual_error_object_and_traceback_preserved=True,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,deletion_executed=False))
    rp=OUT/'SOURCE_ONLY_DRAFT_READY.json';write(rp,dict(schema='SOURCE_ONLY_BIND47_STRICT_NATIVE17_CONSUMER_HOST_CORE_DRAFT_READY_V1',status='SOURCE_ONLY_CORE_DRAFT_READY_RUNTIME_RETIREMENT_AUTHORITY_INCOMPLETE',Host_pin=pin(OUT/HOST),PLAN_pin=pin(pp),inverse_pin=pin(ip),Source_author_pin=pin(__file__),selected_native17_Fortran_Source_freeze_pin=sfp,scope_only47=True,retained_actual_BOOTB49_BOXX68_and_other69=True,target_count11=11,target_bytes1330716816=1330716816,truthful_current_input_count34=34,future_actual_manifest_pin=None,future_actual_release_receipt_pin=None,future_actual_Root_true_tool_pin=None,future_actual_Root_argv_pin=None,future_actual_post_review_pin=None,future_actual_post_tools_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False))
    print(json.dumps(dict(status='STRICT_NATIVE17_CONSUMER_GUARDED_HOST_CORE_SOURCE_ONLY_READY_NO_RUNTIME',Host_pin=pin(OUT/HOST),PLAN_pin=pin(pp),inverse_pin=pin(ip),READY_pin=pin(rp),Source_author_pin=pin(__file__),runtime_authorities_complete=False,only_replacement_index47=47,original8guards_wholebytes_equal=True,original_math_thresholds_caps_unchanged=True,business_executed=False,compiler_executed=False,numerical_executed=False,deletion_executed=False)))
if __name__=='__main__':main()
