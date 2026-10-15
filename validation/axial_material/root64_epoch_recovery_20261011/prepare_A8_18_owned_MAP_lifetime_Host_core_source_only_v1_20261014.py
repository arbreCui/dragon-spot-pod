"""Source-only A8 caller-owned MAP Host core. No compiler/business/delete."""
import ast,hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
OLD=R/'boot_v16_A8_MCCGF442_failure_snapshot_host_source_v1_20261014'
OUT=R/'boot_v16_A8_18_owned_MAP_lifetime_host_source_draft_v1_20261014'
HOST='run_guarded_one_BOOT_A8_owned_MAP_lifetime.py'
JOB=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-A8-owned-MAP-lifetime-20261014-v1')
SF_PATH=R/'boot_v16_A8_18_owned_persistent_MAP_lifetime_source_v1_20261014/COMPLETE_A8_18_CALLER_OWNED_MAP_LIFETIME_SOURCE_FREEZE.json'

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
PRIOR_GATE="    if post['schema']!='INDEPENDENT_MCCGF442_FAILURE_SNAPSHOT_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'or post['status']!='PASS_ACTUAL_MCCGF442_FAILURE_SNAPSHOT_FACTS_POSTVERIFIED_NO_ENGINEERING_QUALIFICATION'or post['failure']is not None or post['actual_A8_first_false_return']['predicate_id']!='A8_MCCGF64_RETURN_L0442'or post['actual_MCCGF442_failure_snapshot']!=base['actual_outcome']['actual_MCCGF442_failure_snapshot']:raise RuntimeError('actual prior borrowed0/0 versus owned8/6; no individual overwrite/free cause assumed')\n    if base['schema']!='ACTUAL_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_V1'or base['status']!='FAILED_DIAGNOSTIC_UNQUALIFIED'or base['failure']!=post['actual_summary_failure']or base['actual_outcome']!=post['actual_summary_outcome_metadata']or base['actual_host_Source_freeze_pin']!=hf['selected_prior_probe_Host_freeze_pin']or base['full50_executed']is not False or base['engineering_qualified']is not False:raise RuntimeError('sealed capture failure1 and original first error unchanged')\n"
OWNED_GATE="    if psf!=hf['selected_owned_Fortran_Source_freeze_pin']or sf['schema']!=SF_SCHEMA or sf['source_only']is not True or sf['compiled']is not False or sf['numerical_executed']is not False or sf['replacement_zero_based_link_index']!=1 or sf['diagnostic_source_pin']!=plan['diagnostic_Source_pin']or sf['original_module_pin']!=plan['selected_original_A8_module_pin']or sf['original_return_mapping247']!=plan['exact_A8_original_false_return_mapping']:raise RuntimeError('exact owned18 Source/object1/module6092/original247map')\n    if any(sf[k]is not True for k in plan['required_owned_Source_freeze_true_flags']):raise RuntimeError('original conditions/math/IO and all18 local typed owners; no SAVE/public API')\n    sfrows=unique(sf['files']+[sf['diagnostic_source_pin'],sf['original_source_pin'],sf['complete_byte_inverse_pin'],sf['control_plan_pin']]);c.verify_rows(sfrows)\n    cappin=plan['selected_current_capture_Fortran_Source_freeze_pin'];cap=c.load_json_exact(cappin['path'],cappin['sha256'],json.dumps(cappin['identity']))[0]\n    if cappin!=hf['selected_current_capture_Fortran_Source_freeze_pin']or dt.get(cappin['path'])!=cappin or cap['schema']!='COMPLETE_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_FORTRAN_SOURCE_ONLY_FREEZE_V1'or cap['original_return_mapping247']!=plan['exact_A8_original_false_return_mapping']or any(cap[k]is not True for k in plan['required_capture_Source_freeze_true_flags']):raise RuntimeError('actual capture Source proof and original snapshot mapping retained')\n    sfrows=unique(sfrows+[cappin]+cap['files']);c.verify_rows(sfrows)\n"
PLAN_GATE="    if sp!=plan['owned_Source_plan_pin']or sourceplan['original_return_mapping247']!=plan['exact_A8_original_false_return_mapping']or sourceplan['exact18_owned_site_mapping']!=plan['exact18_owned_MAP_Source_mapping']or sourceplan['caller_owned_site_count']!=18 or sourceplan['original11_immediate_consume_copy_site_count']!=11 or any(sourceplan['Source_flags'][k]is not True for k in plan['required_owned_Source_freeze_true_flags']):raise RuntimeError('exact18 persistent and11 immediate consumers, original247 and6092 obligations')\n"

def main():
    if OUT.exists()or JOB.exists():raise RuntimeError('unique Source/future runtime')
    op=OLD/'run_guarded_one_BOOT_MCCGF442_failure_snapshot.py';original=op.read_text();s=original;plan=read(OLD/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json')
    if pin(op)['sha256']!='a26902bf5006c17cd830a6c3ec95bc4f46f5f447d16fcb6f18a7b70060af0e48':raise RuntimeError('actual capture complete Host parent')
    rp=R/'readonly_next_A8_owned_views_exact11_role_budget_survey_20261014/REVIEW.json';role=read(rp);postpin=role['genuine_latest_actual_post_review_pin'];post=read(postpin);basepin=post['actual_report_pin'];base=read(basepin);live={p['path']:norm(p)for p in base['fixed_current_pins']+base['output_pins']};old70=[live[p]for p in base['actual_ordered70_link_inputs']];retired=[norm(x['target_pin'])for x in role['ordered_literal_candidate_role_rows']]
    if role['failure']is not None or role['candidate_count']!=11 or role['candidate_logical_bytes']!=1330716816 or len(retired)!=11 or post['actual_MCCGF442_failure_snapshot']!=base['actual_outcome']['actual_MCCGF442_failure_snapshot']:raise RuntimeError('exact11 role and genuine observed snapshot')
    sfpin=pin(SF_PATH);sf=read(sfpin);cpp=sf['control_plan_pin'];cp=read(cpp);flags=list(cp['Source_flags'])
    if sf['schema']!='COMPLETE_SPOR64_A8_18_CALLER_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_ONLY_FREEZE_V1'or sf['diagnostic_source_pin']!=cp['diagnostic_source_pin']or sf['original_module_pin']!=cp['original_module_pin']or sf['original_return_mapping247']!=cp['original_return_mapping247']or len(flags)!=9 or any(sf[k]is not True for k in flags)or cp['caller_owned_site_count']!=18 or cp['original11_immediate_consume_copy_site_count']!=11 or cp['current_actual_ordered70_pins']!=old70:raise RuntimeError('real owned18 SF/current capture70/module6092 exact contract')
    if cp['diagnostic_source_pin']['sha256']!='cf644fb4b5081af901b3b807b96b159c964cf201415cb8253a5b2247945b3d97':raise RuntimeError('exact owned18 candidate')
    sfcreation=pin(R/'ACTUAL_A8_18_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_FREEZE_TRUE_TOOL_RETURN_20261014.json')
    nextnine=[norm(p)for p in role['next_exact_nine_source_input_copy_pins']];kept18=[norm(p)for p in role['retained_current18_original9_latest_capture_nine_input_pins']]
    if len(nextnine)!=9 or len(kept18)!=18 or any(live.get(p['path'])!=p for p in nextnine)or set(p['path']for p in kept18)&set(p['path']for p in retired):raise RuntimeError('actual current18/latestcapture9/disjoint11')
    def change(a,b):
        nonlocal s
        if s.count(a)!=1:raise RuntimeError('one Source splice '+a[:80])
        s=s.replace(a,b,1)
    change("OUT=R/'validation/artifacts/axial-material-new-one-BOOT-MCCGF442-failure-snapshot-20261014-v1'", "OUT=R/'validation/artifacts/axial-material-new-one-BOOT-A8-owned-MAP-lifetime-20261014-v1'")
    change("HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_HOST_SOURCE_ONLY_FREEZE_V1'", "HF_SCHEMA='COMPLETE_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_HOST_SOURCE_ONLY_FREEZE_V1'")
    change("SF_SCHEMA='COMPLETE_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_FORTRAN_SOURCE_ONLY_FREEZE_V1'", "SF_SCHEMA='COMPLETE_SPOR64_A8_18_CALLER_OWNED_MAP_LIFETIME_FORTRAN_SOURCE_ONLY_FREEZE_V1'")
    s=s.replace('capture-source-freeze','owned-source-freeze').replace('selected_capture_Fortran_Source_freeze_pin','selected_owned_Fortran_Source_freeze_pin')
    a=s.index("    if post['schema']!='INDEPENDENT_A8_247_FALSE_RETURN_DIAGNOSTIC_V1_ACTUAL_FAILURE_POSTVERIFICATION_V1'");z=s.index("    if psf!=hf['selected_owned_Fortran_Source_freeze_pin']",a);s=s[:a]+PRIOR_GATE+s[z:]
    a=s.index("    if psf!=hf['selected_owned_Fortran_Source_freeze_pin']");z=s.index("    a8pin=plan['selected_current_A8_247_Fortran_Source_freeze_pin']",a);s=s[:a]+OWNED_GATE+s[z:]
    a=s.index("    if sp!=plan['capture_Source_plan_pin']");z=s.index("    v16pin=plan['actual_closed_v16_report_pin']",a);s=s[:a]+PLAN_GATE+s[z:]
    s=s.replace("schema='ACTUAL_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_V1'", "schema='ACTUAL_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_V1'")
    s=s.replace('retained_original9_latest_A8_nine_input_sources_full_EOF_and_all7_preserved','retained_original9_latest_capture_nine_input_sources_full_EOF_and_all7_preserved')
    change("return dict(kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0", "return dict(single_boot_completed=True,kind='REAL_ORIGINAL_SINGLE_BOOT_SEAL_READBACK0_ONLY',actual_exit_code=0")
    ast.parse(s)
    def defs(x):return{n.name:ast.get_source_segment(x,n)for n in ast.parse(x).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
    f0=defs(original);f1=defs(s)
    for n in ['load_common','unique','rewrite_summary','empty_final_metadata_kind','classify_storage_inventory','FirstFatal','PhaseResources','genuine_terminal','make_commands','parse_MCCGF442_failure_snapshot','parse_A8_failed_return_chain','parse_A9_failed_return_chain','parse_BIND_return_chain','parse_failed_PHYS_inventory']:
        if f0[n]!=f1[n]:raise RuntimeError('all guards/commands/failure parsers wholebytes '+n)
    currentcap=plan.pop('selected_capture_Fortran_Source_freeze_pin')
    for k in('Source_generator_pin','reviewed_core_draft_complete_metadata_pins','retained_latest_A8_nine_input_copy_pins','retained_current18_original9_latest_A8_nine_input_pins','all_original9_and_latest_A8_nine_current18_inputs_and_current70_retained'):plan.pop(k,None)
    plan.update(schema='SOURCE_ONLY_GUARDED_ONE_BOOT_A8_18_OWNED_MAP_LIFETIME_HOST_CORE_DRAFT_V1',draft_only=True,runtime_authorities_complete=False,planned_output_root=str(JOB),diagnostic_Source_pin=cp['diagnostic_source_pin'],selected_owned_Fortran_Source_freeze_pin=sfpin,required_owned_Source_freeze_true_flags=flags,owned_Source_plan_pin=cpp,selected_current_capture_Fortran_Source_freeze_pin=currentcap,exact18_owned_MAP_Source_mapping=cp['exact18_owned_site_mapping'],actual_prior_probe_report_pin=basepin,selected_prior_probe_Host_freeze_pin=post['actual_Host_freeze_pin'],selected_prior_probe_Root_tool_pin=post['actual_Root_true_tool_return_pin'],selected_prior_probe_actual_post_review_pin=postpin,selected_prior_probe_actual_post_tools_pin=role['genuine_latest_actual_post_true_tool_pin'],current_ordered70_input_pins=old70,retained_actual_A8_object1_pin=old70[1],selected_original_A8_module_pin=cp['original_module_pin'],base_Dragon_pin=live[base['records'][1]['command'][-1]],original_compile_include_arguments=[x for x in base['records'][0]['command']if x.startswith('-I')],owned_readonly_input_rows=[dict(owned_filename=Path(p['path']).name,target_pin=p)for p in nextnine],retained_latest_capture_nine_input_copy_pins=nextnine,retained_current18_original9_latest_capture_nine_input_pins=kept18,all_original9_and_latest_capture_nine_current18_inputs_and_current70_retained=True,exact_historical_retired_private_body_pins=retired,selected_exact11_actual_release_pin=None,selected_exact11_actual_Root_tool_pin=None,selected_exact11_actual_post_review_pin=None,selected_exact11_actual_post_tools_pin=None,selected_exact11_actual_manifest_pin=None,selected_exact11_release_schema=None,selected_exact11_release_status=None,selected_exact11_post_schema=None,selected_exact11_post_status=None,selected_exact11_release_Source_freeze_pin=None,actual_retirement_external_pins=None,actual_Fortran_Source_freeze_creation_true_tool_pin=sfcreation,Source_role_survey_pin=pin(rp),current_MF8664_exact9_history_indices=role['current_MF8664_exact9_candidate_indices'],current_HF3839_exact9_history_indices=role['current_HF3839_exact9_candidate_indices'],current_root_authority_is_latest3840fixed27outputs_HF3839=True,only_slot1_replaced_and_bootstrap9_unchanged_required=True,source_only_owned_reads_not_owner_bit_or_solver_qualification=True,future_actual_owner_bit_control_results=None,core_draft_predecessor_Host_pin=pin(op))
    OUT.mkdir();hp=OUT/HOST;write(hp,s);pp=OUT/'EXACT_ONE_BOOT_DIAGNOSTIC_HOST_SOURCE_PLAN.json';write(pp,plan);ip=OUT/'COMPLETE_CAPTURE_HOST_TO_A8_OWNED_MAP_LIFETIME_CORE_SOURCE_WHOLE_BYTE_INVERSE.json';write(ip,dict(schema='COMPLETE_CAPTURE_HOST_TO_A8_OWNED_MAP_LIFETIME_CORE_SOURCE_WHOLE_BYTE_INVERSE_V1',original_Host_pin=pin(op),candidate_Host_pin=pin(hp),changes=[dict(before=original,after=s)],whole_Source_inverse_exact=True,original8guards_and_all_failure_parsers_and_commands_wholebytes_equal=True,only_readback0_metadata_single_boot_completed_added=True,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False));ready=OUT/'SOURCE_ONLY_DRAFT_READY.json';write(ready,dict(status='SOURCE_ONLY_A8_OWNED_MAP_HOST_CORE_WITH_ACTUAL_SF_PENDING_EXACT11_PROOFS',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),Source_author_pin=pin(__file__),selected_owned_Fortran_Source_freeze_pin=sfpin,future_actual_cleanup_external_pins=None,only_object1_replaced=True,other69_unchanged=True,current_input_source_count18=18,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_owner_bit_control_results=None))
    print(json.dumps(dict(status='SOURCE_ONLY_A8_OWNED_MAP_HOST_CORE_READY_NO_RUNTIME',host_source_pin=pin(hp),plan_pin=pin(pp),inverse_pin=pin(ip),ready_pin=pin(ready),Source_author_pin=pin(__file__),runtime_authorities_complete=False,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
