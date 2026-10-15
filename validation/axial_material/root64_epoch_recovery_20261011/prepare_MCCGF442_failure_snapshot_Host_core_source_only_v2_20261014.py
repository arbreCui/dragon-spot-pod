"""Source-only capture Host core; no business/compiler/MF/delete."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'boot_v16_A8_247_false_return_diagnostic_host_source_v1_20261014'
OUT=R/'boot_v16_A8_MCCGF442_failure_snapshot_host_source_draft_v1_20261014'
HOST='run_guarded_one_BOOT_MCCGF442_failure_snapshot.py'
JOB=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-MCCGF442-failure-snapshot-20261014-v1')
SF_PATH=R/'boot_v16_A8_MCCGF442_state_failure_snapshot_source_v1_20261014/COMPLETE_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_SOURCE_FREEZE.json'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('Source/metadata only')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('Source opened7')
        b=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('Source FD7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('Source after7')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
def write(p,v):
    b=(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(v,dict)else v.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())

SNAPSHOT_PARSER='''def parse_MCCGF442_failure_snapshot(rows,a8chain,a9chain):
    events=[r for r in rows if r.get('schema')=='ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1']
    if [(r['scope'],r['original_return_source_line'])for r in a8chain]!=[('MCCGF64',442),('DOORFV64',359)]or len(a9chain)!=1 or a9chain[0]['scope']!='FLU2DR64_CORE'or a9chain[0]['original_return_source_line']!=233 or len(events)!=1:raise RuntimeError('only one original442 snapshot under actual MCCGF442→DOOR359→A9CORE233')
    e=events[0]
    if set(e)!={'schema','original_return_source_line','nbmix','nsou','nreg','nun','actual_STATE_length','actual_STATE_type','actual_LCMINF_memory_object','snapshot_verified','fresh_STATE4','fresh_STATE5'}or any(type(e[k])is not int for k in('original_return_source_line','nbmix','nsou','nreg','nun','actual_STATE_length','actual_STATE_type'))or e['original_return_source_line']!=442 or e['nbmix']>0 or e['nreg']<=0 or e['nun']<=0 or type(e['actual_LCMINF_memory_object'])is not bool or type(e['snapshot_verified'])is not bool:raise RuntimeError('exact bounded failure snapshot Source fields/types; original nbmixFalse not relaxed')
    valid=(e['actual_STATE_length']==40 and e['actual_STATE_type']==1)
    if e['snapshot_verified']is not valid:raise RuntimeError('owned160B snapshot iff both original STATE length40/type1')
    if valid:
        if type(e['fresh_STATE4'])is not int or type(e['fresh_STATE5'])is not int:raise RuntimeError('only fresh owned STATE4/5 typed integer values')
    elif e['fresh_STATE4']is not None or e['fresh_STATE5']is not None:raise RuntimeError('invalid shape does not read or invent fresh STATE values')
    if rows.index(e)>=rows.index(a8chain[0]):raise RuntimeError('failure-only observer precedes original442 failed event')
    return e
'''

def main():
    if OUT.exists()or JOB.exists():raise RuntimeError('unique Source/future runtime')
    op=OLD/'run_guarded_one_BOOT_A8_false_return_diagnostic.py';original=op.read_text();s=original;plan=read(OLD/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json')
    if pin(op)['sha256']!='458cb89280221da6c28043b1d2f630b53bfcdfc9c7ad6273d6056fb6cfcca336':raise RuntimeError('actual A8 final Host Source only')
    rolepath=R/'readonly_next_MCCGF_lifetime_exact11_role_budget_survey_20261014/REVIEW.json';role=read(rolepath);postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);basepin=post['actual_report_pin'];base=read(basepin);live={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};old70=[live[p]for p in base['actual_ordered70_link_inputs']];retired=[norm(x['target_pin'])for x in role['ordered_literal_candidate_role_rows']]
    if role['failure']is not None or role['candidate_count']!=11 or role['candidate_logical_bytes']!=1330716816 or len(retired)!=11 or post['actual_A8_first_false_return']['predicate_id']!='A8_MCCGF64_RETURN_L0442':raise RuntimeError('exact current11 role Source and genuine observed442 only')
    cpp=pin(R/'boot_v16_A8_MCCGF442_state_failure_snapshot_source_v1_20261014/SOURCE_ONLY_A8_MCCGF442_FAILURE_SNAPSHOT_PLAN.json');cp=read(cpp);flags=['whole_file_inverse_byte_equal','all247_original_failure_IDs_and_conditions_once_and_returns_unchanged','all_original_declarations_public_ABI_math_loops_allocations_status_assignments_and_original_IO_order_unchanged','only_original442_failure_observer_before_original_false_event_and_return_added','no_old_borrowed_view_read_or_address_evaluation','no_new_early_return_and_original_nbMix_false_condition_unchanged']
    if cp['actual_retained_A8_object1_pin']!=old70[1]or cp['only_additional_scientific_record_read']['maximum_bytes']!=160:raise RuntimeError('actual compiled slot1 and exact160B Source read bound')
    sfpin=pin(SF_PATH);sf=read(sfpin)
    if sfpin['sha256']!='ef3d0fc041a449f99d85ad83802629c44756324657f3e1d022a287a57f503be4'or sf['schema']!='COMPLETE_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_FORTRAN_SOURCE_ONLY_FREEZE_V1'or sf['control_plan_pin']!=cpp or sf['diagnostic_source_pin']!=cp['diagnostic_source_pin']or sf['original_module_pin']!=cp['original_module_pin']or sf['original_return_mapping247']!=cp['original_return_mapping247']or any(sf[k]is not True for k in flags):raise RuntimeError('real once frozen failure snapshot Source exact contract')
    sfcreation=pin(R/'ACTUAL_A8_MCCGF442_FAILURE_SNAPSHOT_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json')
    nextnine=[norm(p)for p in role['next_exact_nine_source_input_copy_pins']];kept18=[norm(p)for p in role['retained_current18_original9_latest_A8_nine_input_pins']]
    if len(nextnine)!=9 or len(kept18)!=18 or any(live.get(p['path'])!=p for p in nextnine)or set(p['path']for p in kept18)&set(p['path']for p in retired):raise RuntimeError('actual retained18/source latestA8nine/disjoint11 only')
    def change(a,b):
        nonlocal s
        if s.count(a)!=1:raise RuntimeError('one Source splice '+a[:80])
        s=s.replace(a,b,1)
    def fn(name):return ast.get_source_segment(s,next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name==name))
    change("OUT=R/'validation/artifacts/axial-material-new-one-BOOT-A8-false-return-diagnostic-20261014-v1'", "OUT=R/'validation/artifacts/axial-material-new-one-BOOT-MCCGF442-failure-snapshot-20261014-v1'")
    change("HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_HOST_SOURCE_ONLY_FREEZE_V1'", "HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_HOST_SOURCE_ONLY_FREEZE_V1'")
    change("SF_SCHEMA='COMPLETE_SPOR64_A8_247_FALSE_RETURN_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'", "SF_SCHEMA='COMPLETE_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_FORTRAN_SOURCE_ONLY_FREEZE_V1'")
    s=s.replace('a8-source-freeze','capture-source-freeze').replace('selected_A8_Fortran_Source_freeze_pin','selected_capture_Fortran_Source_freeze_pin')
    outcome=fn('read_BOOT_outcome');line="    a8_events=[r for r in rows if r.get('schema')=='ACTUAL_SPOR64_A8_FAILED_RETURN_DIAGNOSTIC_V1']";assert outcome.count(line)==1;outcome=outcome.replace(line,line+"\n    snapshot_events=[r for r in rows if r.get('schema')=='ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1']")
    line="        if not under_A8 and a8_events:raise RuntimeError('A8 failed events only under actual A9 CORE233/status2; never other A9/status paths')"
    after=line+"\n        under_snapshot=([(e['scope'],e['original_return_source_line'])for e in a8chain]==[('MCCGF64',442),('DOORFV64',359)])\n        snapshot=parse_MCCGF442_failure_snapshot(rows,a8chain,a9chain)if under_snapshot else None\n        if not under_snapshot and snapshot_events:raise RuntimeError('failure snapshot only at actual originalMCCGF442, not any other status/ID')"
    assert outcome.count(line)==1;outcome=outcome.replace(line,after).replace('return dict(actual_A8_failed_return_chain=', 'return dict(actual_MCCGF442_failure_snapshot=snapshot,actual_A8_failed_return_chain=').replace('or a8_events or len(seals)', 'or a8_events or snapshot_events or len(seals)');change(fn('read_BOOT_outcome'),SNAPSHOT_PARSER+'\n'+outcome)
    a=s.index("    if post['schema']!='INDEPENDENT_A9_111_FALSE_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'");z=s.index("    if psf!=hf['selected_capture_Fortran_Source_freeze_pin']",a)
    s=s[:a]+"    if post['schema']!='INDEPENDENT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_A8_247_FALSE_RETURN_FAILURE_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_A8_first_false_return']['predicate_id']!='A8_MCCGF64_RETURN_L0442':raise RuntimeError('actual prior A8MCCGF442 and unknown fresh snapshot')\n    if base['schema']!='ACTUAL_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1'or base['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or base['failure']!=post['actual_summary_failure']or base['actual_outcome']!=post['actual_summary_outcome_metadata']or base['actual_host_Source_freeze_pin']!=hf['selected_prior_probe_Host_freeze_pin']or base['full50_executed']is not False or base['engineering_qualified']is not False:raise RuntimeError('sealed prior A8real442 unchanged')\n"+s[z:]
    a=s.index("    if psf!=hf['selected_capture_Fortran_Source_freeze_pin']");z=s.index("    a9pin=plan['selected_current_A9_Fortran_Source_freeze_pin']",a)
    s=s[:a]+"    if psf!=hf['selected_capture_Fortran_Source_freeze_pin']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['replacement_zero_based_link_index']!=1 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']or sf['original_module_pin']!=plan['selected_original_A8_module_pin']or sf['original_return_mapping247']!=plan['exact_A8_original_false_return_mapping']:raise RuntimeError('exact failure-only capture Source/object1/module6092/original247map')\n    if any(sf[k]is not True for k in plan['required_capture_Source_freeze_true_flags']):raise RuntimeError('original247 conditions/math/IO/no oldviews failure-only Source obligations')\n    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)\n    a8pin=plan['selected_current_A8_247_Fortran_Source_freeze_pin'];a8=c.load_json_exact(a8pin['path'],a8pin['sha256'],json.dumps(a8pin['identity']))[0]\n    if a8pin!=hf['selected_current_A8_247_Fortran_Source_freeze_pin']or dt.get(a8pin['path'])!=a8pin or a8['schema']!='COMPLETE_SPOR64_A8_247_FALSE_RETURN_DIAGNOSTIC_FORTRAN_SOURCE_ONLY_FREEZE_V1'or a8['original_return_mapping']!=plan['exact_A8_original_false_return_mapping']or any(a8[k]is not True for k in plan['required_A8_Source_freeze_true_flags']):raise RuntimeError('original247 Source proof retained')\n    sfrows=unique(sfrows+[a8pin]+a8['files']);c.verify_rows(sfrows)\n"+s[z:]
    a=s.index("    if sp!=plan['A8_false_return_Source_plan_pin']");z=s.index("    v16pin=plan['actual_closed_v16_report_pin']",a)
    s=s[:a]+"    if sp!=plan['capture_Source_plan_pin']or sourceplan['original_return_mapping247']!=plan['exact_A8_original_false_return_mapping']or sourceplan['only_additional_scientific_record_read']!=plan['exact_capture_owned_record_contract']or sourceplan['old_borrowed_pointer_views_never_read_or_address_evaluated']is not True:raise RuntimeError('strict failure-only442 owned160B Source contract')\n"+s[z:]
    s=s.replace('ACTUAL_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1','ACTUAL_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_V1')
    # Restore the actual predecessor schema check; only the new summary schema changes.
    s=s.replace("base['schema']!='ACTUAL_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_V1'", "base['schema']!='ACTUAL_GUARDED_ONE_BOOT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1'")
    s=s.replace('retained_original9_latest_A9_nine_input_sources_full_EOF_and_all7_preserved','retained_original9_latest_A8_nine_input_sources_full_EOF_and_all7_preserved')
    ast.parse(s)
    def defs(x):return{n.name:ast.get_source_segment(x,n)for n in ast.parse(x).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    guard=['load_common','unique','rewrite_summary','empty_final_metadata_kind','classify_storage_inventory','FirstFatal','PhaseResources','genuine_terminal'];f0=defs(original);f1=defs(s)
    if any(f0[n]!=f1[n]for n in guard+['make_commands','parse_A8_failed_return_chain','parse_A9_failed_return_chain','parse_BIND_return_chain','parse_failed_PHYS_inventory']):raise RuntimeError('all original guards/commands/247/A9/BIND/inventory parsers wholebytes')
    for k in('retained_latest_A9_nine_input_copy_pins','retained_current18_original9_latest_A9_nine_input_pins','all_original9_and_latest_A9_nine_current18_inputs_and_current70_retained','Source_generator_pin','reviewed_core_draft_complete_metadata_pins'):plan.pop(k,None)
    currenta8=plan.pop('selected_A8_Fortran_Source_freeze_pin')
    plan.update(schema='SOURCE_ONLY_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_HOST_CORE_DRAFT_V1',draft_only=True,runtime_authorities_complete=False,planned_output_root=str(JOB),diagnostic_Source_pin=cp['diagnostic_source_pin'],selected_capture_Fortran_Source_freeze_pin=sfpin,selected_capture_Fortran_Source_freeze_path=str(SF_PATH),required_capture_Source_freeze_true_flags=flags,capture_Source_plan_pin=cpp,selected_current_A8_247_Fortran_Source_freeze_pin=currenta8,exact_capture_owned_record_contract=cp['only_additional_scientific_record_read'],actual_prior_probe_report_pin=basepin,selected_prior_probe_Host_freeze_pin=post['actual_Host_freeze_pin'],selected_prior_probe_Root_tool_pin=post['actual_Root_true_tool_return_pin'],selected_prior_probe_actual_post_review_pin=postpin,selected_prior_probe_actual_post_tools_pin=role['genuine_latest_actual_post_true_tool_pin'],current_ordered70_input_pins=old70,retained_actual_A8_object1_pin=old70[1],base_Dragon_pin=live[base['records'][1]['command'][-1]],original_compile_include_arguments=[x for x in base['records'][0]['command']if x.startswith('-I')],owned_readonly_input_rows=[dict(owned_filename=Path(p['path']).name,target_pin=p)for p in nextnine],retained_latest_A8_nine_input_copy_pins=nextnine,retained_current18_original9_latest_A8_nine_input_pins=kept18,all_original9_and_latest_A8_nine_current18_inputs_and_current70_retained=True,exact_historical_retired_private_body_pins=retired,selected_exact11_actual_release_pin=None,selected_exact11_actual_Root_tool_pin=None,selected_exact11_actual_post_review_pin=None,selected_exact11_actual_post_tools_pin=None,selected_exact11_actual_manifest_pin=None,selected_exact11_release_schema=None,selected_exact11_release_status=None,selected_exact11_post_schema=None,selected_exact11_post_status=None,selected_exact11_release_Source_freeze_pin=None,actual_retirement_external_pins=None,actual_Fortran_Source_freeze_creation_true_tool_pin=sfcreation,Source_role_survey_pin=pin(rolepath),current_MF8608_exact9_history_indices=role['current_MF8608_exact9_candidate_indices'],current_HF3787_exact9_history_indices=role['current_HF3787_exact9_candidate_indices'],current_root_authority_is_latest3788fixed27outputs_HF3787=True,maximum_capture_scientific_read_bytes=160,future_actual_snapshot_values=None,core_draft_predecessor_Host_pin=pin(op),selected_original_A8_module_pin=cp['original_module_pin'])
    OUT.mkdir();hp=OUT/HOST;write(hp,s);pp=OUT/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json';write(pp,plan);ip=OUT/'COMPLETE_A8_CURRENT_HOST_TO_MCCGF442_CAPTURE_CORE_SOURCE_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_A8_CURRENT_HOST_TO_MCCGF442_CAPTURE_CORE_SOURCE_WHOLE_BYTE_INVERSE_V1',original_Host_pin=pin(op),candidate_Host_pin=pin(hp),changes=[dict(before=original,after=s)],whole_Source_inverse_exact=True,eight_original_guard_methods_and_all_original_failure_chain_parsers_and_commands_wholebytes_equal=True,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False));rp=OUT/'SOURCE_ONLY_DRAFT_READY.json';write(rp,dict(status='SOURCE_ONLY_CAPTURE_HOST_CORE_WITH_ACTUAL_SF_PENDING_EXACT11_PROOFS',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),Source_author_pin=pin(__file__),selected_capture_Fortran_Source_freeze_pin=sfpin,selected_capture_Fortran_Source_freeze_path=str(SF_PATH),future_actual_cleanup_external_pins=None,maximum_capture_scientific_read_bytes=160,only_object1_replaced=True,other69_unchanged=True,current_input_source_count18=18,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_snapshot_values=None))
    print(json.dumps(dict(status='SOURCE_ONLY_MCCGF442_CAPTURE_HOST_CORE_READY_NO_RUNTIME',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),ready_pin=pin(rp),Source_author_pin=pin(__file__),runtime_authorities_complete=False,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
