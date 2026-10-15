from pathlib import Path
import ast,hashlib,json,os,stat,time
R=Path('/Users/wen/spot');REC=R/'validation/axial_material/root64_epoch_recovery_20261011'
OLD=REC/'current_formal_material_authority_handle_lifetime69_source_v2'
NEW=REC/'current_formal_material_authority_exact_cache70_source_v4'
COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'
BUILD=R/'validation/artifacts/axial-material-new-native-rank1-exact-block-cache-complete70-build-only-20261012-v2/Root_actual_build_only_summary.json'
BOOT_HOST=REC/'aaa_three_plane_streaming_pipeline_source_v9/run_actual_three_plane_pipeline.py'
BOOT_HF=REC/'aaa_three_plane_streaming_pipeline_source_v9/COMPLETE_PIPELINE_HOST_SOURCE_FREEZE.json'
SCI_HF=REC/'saved_full370_terminal_audit_host_source_v2/COMPLETE_SAVED_FULL370_GUARD_HOST_SOURCE_FREEZE.json'
SCI_HOST=REC/'saved_full370_terminal_audit_host_source_v2/run_actual_saved_full370_terminal_source_original_guard.py'
CAT=REC/'current_mount_identity_reattestation_20261012/CURRENT_MOUNT_FULL_EOF_IDENTITY_CATALOG.json'
def identity(p):
 s=Path(p).lstat();return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);before=identity(p);assert p.is_absolute()and stat.S_ISREG(before[2])
 with p.open('rb')as f:
  assert [os.fstat(f.fileno()).st_dev,os.fstat(f.fileno()).st_ino,os.fstat(f.fileno()).st_mode,os.fstat(f.fileno()).st_nlink,os.fstat(f.fileno()).st_size,os.fstat(f.fileno()).st_mtime_ns,os.fstat(f.fileno()).st_ctime_ns]==before
  sha=hashlib.file_digest(f,'sha256').hexdigest()
 assert identity(p)==before
 return dict(path=str(p),sha256=sha,size_bytes=before[4],identity=before)
def write(p,d):
 with p.open('x')as f:json.dump(d,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def save(name,raw):
 with(NEW/name).open('xb')as f:f.write(raw)
def replace(raw,a,b):
 assert raw.count(a)==1,(a[:100],raw.count(a));return raw.replace(a,b)
rows=[]
def reattest(p):
 actual=pin(p['path']);assert actual['sha256']==p['sha256']and actual['size_bytes']==p['size_bytes']and actual['identity'][1:]==p['identity'][1:]
 assert p['identity'][0]in(16777234,16777229)and actual['identity'][0]==16777229
 row=dict(historical_pin=p,current_pin=actual,only_actual_device_field_transition=True)
 if row not in rows:rows.append(row)
 return actual
oldpins=[pin(p)for p in sorted(OLD.iterdir())if p.is_file()]
oldplan=json.loads((OLD/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_HANDLE69_PLAN.json').read_bytes())
oldsf=json.loads((OLD/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json').read_bytes())
build=json.loads(BUILD.read_bytes());buildpin=pin(BUILD)
assert buildpin['sha256']=='962c1c5810fd409db47db2ac65742b835f9f360af253978068239f6fdcc0bf44'
assert build['schema']=='ACTUAL_NATIVE_RANK1_EXACT_BLOCK_CACHE_COMPLETE70_BUILD_ONLY_V2'and build['status']=='ACTUAL_TWO_CACHE_SOURCE_COMPILE_COMPLETE70_LINK_CLOSED0_ONLY'and build['failure']is None and build['after_check_error']is None and len(build['records'])==3 and build['final_report_resource_check_passed']is True
copies=[]
for p in sorted(OLD.iterdir()):
 if p.suffix.lower()in('.f','.f90')or p.name in('complete_context_aware_MICROLIB_MACROLIB_aggregation_engine.UNREADY.py','complete_observed_old_post_final_XSM_extractor.UNREADY.py','extract_actual_complete_context_with_SPH_decisions.UNREADY.py','saved_native_data_access_adapter.UNREADY.py','COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json','COMPLETE_OBSERVATION_FORTRAN_SOURCE_INVERSE.json','FULL_ACTUAL_CONTEXT_AND_SNAPSHOT_EXTENSION_CONTRACT.UNREADY.json','COMPLETE_CONTEXT_AWARE_FIELD_PRODUCER_SCOPE_AND_GAPS.json','CURRENT_OBSERVATION_SIX_INTACT_FUNCTION_BODY_COPY_PROOF.json'):
  raw=p.read_bytes();save(p.name,raw);assert(NEW/p.name).read_bytes()==raw
  if p.suffix=='.py':ast.parse(raw)
  copies.append(dict(original=pin(p),copy=pin(NEW/p.name),entire_bytes_equal=True))
# Compiler is immutable nlink2. Only this exact role/pin may have two links;
# all owned outputs and every other evidence file keep single-link admission.
compiler=pin(build['records'][0]['command'][0]);assert compiler['identity'][3]==2
# Gate metadata Source is independent of all numerical/material bodies.
header='''"""Actual prerequisites for the ordered material transaction; no transport code.

Root must supply true completed AAA3/BOOT and saved full370 audit report pins.
No future file hash, receipt or successful stage is predicted in Source metadata.
"""
import hashlib,json,os,stat,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
'''
helper=header+'''def require(ok,message):
    if type(ok)is not bool or not ok:raise RuntimeError(message)

def exact_load(c,path,sha,seven):
    value,p=c.load_json_exact(path,sha,seven)
    return value,p

def admit_limits(d):
    require(d['failure']is None and d['after_check_error']is None and
      d['original_guard_class']=='OwnRSSSerialExecutor'and d['original_guard_MRO_unchanged']is True and
      type(d['SELF_peak_bytes'])is int and 0<=d['SELF_peak_bytes']<512*2**20 and
      type(d['wall_seconds'])in(int,float)and 0<d['wall_seconds']<1800,'actual original own SELF/whole closure')

def admit_prerequisites(c,args,hf,helper):
    boot,pboot=exact_load(c,args.aaa3_summary,args.aaa3_sha256,args.aaa3_seven_id)
    require(Path(pboot['path']).parent==Path(hf['required_actual_AAA3_output_directory'])and
      boot['schema']=='ACTUAL_INDEPENDENT_AAA3_INITIAL_GLOBAL_PROJECT_BOOT_ENGINEERING_ROOT_V1'and
      boot['status']=='ACTUAL_THREE_PLANE_ENGINEERING_CLOSED0_ONLY'and
      boot['engineering_three_plane_closed0']is True and boot['all_new_storage_entry_controls_closed']is True,
      'real full three-plane GLOBAL PROJECT onlineBOOT engineering closure')
    admit_limits(boot);c.verify_rows(boot['fixed_current_pins']);c.verify_rows(boot['output_pins'])
    require(hf['required_actual_AAA3_host_freeze_pin']in boot['fixed_current_pins'],
      'actual prerequisite must consume exact frozen v9 host Source')
    raw,checked=c.read_bound_json_current(boot['complete_unmodified_execution_records_pin']['path'],boot['complete_unmodified_execution_records_pin'])
    require(raw['failure']is None and raw['after_check_error']is None and len(raw['records'])==50 and
      len(boot['records'])==50 and sum(r['status']=='PASS'for r in boot['records'])==17 and
      sum(r['status']=='FAILED'for r in boot['records'])==33 and len(boot['actual_operator_refusals'])==33,
      'all50 actual original stages:17 success and33 exact refused inputs')
    table={p['path']:p for p in boot['output_pins']}
    for original,compact in zip(raw['records'],boot['records']):
        require({k:v for k,v in original.items()if k not in('resource_before','resource_after')}==compact,
          'all original stage fields preserved in compact report')
        root=Path(pboot['path']).parent;wp=root/(compact['label']+'.watchdog.json');lp=root/(compact['label']+'.log')
        require(str(wp)in table and str(lp)in table,'full actual watchdog/log output authority')
        c.same_pin(wp,table[str(wp)]);c.same_pin(lp,table[str(lp)])
        watch=json.loads(wp.read_bytes())
        require(watch['command']==compact['command']and watch['returncode']==(0 if compact['status']=='PASS'else 1)and
          watch['limit_failure']is None and watch['rss_cap_mib']==512 and watch['own_child_only']is True and
          watch['liveness_group_cleanup']is True and 0<watch['elapsed_seconds']<watch['wall_cap_seconds']<=600 and
          0<=watch['sampled_peak_rss_mib']<512 and table[str(lp)]['sha256']==compact['log_sha256'],
          'each actual original successful or intended-refusal child fully closed')
    for case in boot['actual_operator_refusals']:
        require(case['actual_exit_code']==1 and case['actual_abort_message_exact']is True and
          case['all_actual_assertions_completed']is True and case['pre_transport_abort_at_frozen_validation_branch']is True,
          'exact actual original negative control verdict')
        c.same_pin(case['actual_log_pin']['path'],case['actual_log_pin'])
        require(Path(case['actual_log_pin']['path']).read_text().count(case['expected_abort'])==1,
          'one original exact expected refusal message')
    require(boot['actual_terminal']['actual_Fortran_complete_copy_readback']['status']=='PASS'and
      boot['actual_terminal']['actual_Fortran_complete_copy_readback']['all_payload_bits_equal']is True,
      'complete actual sealed output pair bit readback required')
    for key in('AAA_qualified','ABA_admitted','goal_complete'):
        require(boot[key]is False,'engineering completion cannot mint physics accuracy')
    audit,paudit=exact_load(c,args.saved_audit_summary,args.saved_audit_sha256,args.saved_audit_seven_id)
    require(Path(paudit['path']).parent==Path(hf['required_actual_saved_audit_output_directory'])and
      audit['schema']=='ACTUAL_ROOT_GUARDED_SAVED_FULL370_TERMINAL_SOURCE_DIAGNOSTIC_V2'and
      audit['status']=='ACTUAL_SAVED_FULL370_THREE_AXIAL_MOMENT_DIAGNOSTIC_CLOSED0_ONLY'and
      audit['final_report_bytes_in_original_resources']is True and audit['postwrite_cap_PASS_requires_actual_true_closed0']is True,
      'real saved full370 audit diagnostic closure after onlineBOOT')
    admit_limits(audit);c.closed_report(audit,helper,Path(paudit['path']).parent,1)
    require(hf['required_actual_saved_audit_host_freeze_pin']in audit['fixed_current_pins'],
      'actual saved diagnostic exact frozen v2 Source')
    c.verify_rows(audit['actual_TMP_output_pins'])
    result=audit['actual_result']
    require(result['classification']=='COMPLETE_SAVED_TERMINAL_THREE_AXIAL_MOMENT_SOURCE_DIAGNOSTIC_ONLY_NDIM3_NINE_MOMENTS_UNREADY'and
      (result['groups'],result['regions'],result['axial_cells'])==(370,8,48)and
      result['axes']['known_NDIM3_R_indices_0based']==[0,2,6]and
      result['axes']['unknown_NDIM3_R_indices_0based']==[1,3,4,5,7,8]and
      result['no_clip_no_drop_no_local_renormalization']is True and result['child_launch_attempts']==[],
      'complete original saved scope and six unobserved moments remain unknown')
    for key in('full_neutron_balance_qualified','full_eigen_reference_qualified','AAA_qualified','ABA_admitted','goal_complete'):
        require(audit[key]is False,'diagnostic cannot mint neutron balance/reference/accuracy')
    return [pboot,paudit,checked]+boot['fixed_current_pins']+boot['output_pins']+audit['fixed_current_pins']+audit['output_pins']+audit['actual_TMP_output_pins'],dict(actual_AAA3_report_pin=pboot,actual_saved_full370_diagnostic_report_pin=paudit,prerequisite_order_requires_Root_true_tool_terminal_receipts=True,scope_is_engineering_and_saved_diagnostic_only=True)


def replace_owned_failure_summary(c,path,wanted,value):
    path=Path(path);require(wanted['identity'][3]==1 and c.pin(path)==wanted,'exact just-created owned summary only')
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\\n').encode()
    fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW)
    with os.fdopen(fd,'r+b')as stream:
        s=os.fstat(stream.fileno());opened=[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
        require(opened==wanted['identity']and stat.S_ISREG(s.st_mode)and s.st_nlink==1,'same opened owned7ID')
        require(hashlib.file_digest(stream,'sha256').hexdigest()==wanted['sha256']and c.identity(path)==opened,
          'same-fd entire owned summary SHA and unchanged path7ID')
        stream.seek(0);stream.write(raw);stream.truncate();stream.flush();os.fsync(stream.fileno())
    actual=c.pin(path);require(actual['identity'][:4]==opened[:4]and actual['sha256']==hashlib.sha256(raw).hexdigest(),
      'same owned summary truthful failure publication')
    return actual
'''
save('current_material_prerequisite_admission.py',helper.encode())
# Build host retains compile/guard/storage/caps and replaces only predecessor
# admission with the same independently reviewed complete70 admission used v9.
raw=(OLD/'build_current_observation_runtime.py').read_text()
raw=raw.replace('All complete69 inputs','All complete70 inputs').replace("SOURCE=REC/'current_formal_material_authority_handle_lifetime69_source_v2'", "SOURCE=REC/'current_formal_material_authority_exact_cache70_source_v4'")
raw=raw.replace("COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'", "COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'")
raw=raw.replace("c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)","c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)\nfrom current_material_prerequisite_admission import admit_prerequisites,replace_owned_failure_summary")
raw=raw.replace('69','70').replace('74','75')
raw=raw.replace('20971764758','20971764748')
# Restore predecessor semantic block by extracting immutable v9 full admission.
start=raw.index("    base,pbase=load('current70')")
stop=raw.index("    sf,psf=load('source_freeze')",start)
pipeline=BOOT_HOST.read_text();a=pipeline.index("    build,pbuild=ext(args,'build70')");z=pipeline.index("    direct_binding_path=",a)
admission=pipeline[a:z].replace("build,pbuild=ext(args,'build70')","build,pbuild=load('current70')")
admission=admission.replace('    old9=binding[', '    old9=binding[')
admission+='    base=build;pbase=pbuild\n    gate_fixed,gate_receipts=admit_prerequisites(c,args,hf,helper)\n    fixed+=gate_fixed+current69[\'fixed_current_pins\']+current69[\'output_pins\']+[current69_pin]+original69[\'fixed_current_pins\']+original69[\'output_pins\']+[original69_pin]+native_sf_rows\n'
raw=raw[:start]+admission+raw[stop:]
raw=raw.replace("['current70','source-freeze','host-freeze']", "['current70','source-freeze','host-freeze','aaa3','saved-audit']")
raw=raw.replace("hf['schema']!='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_ONLY_FREEZE_V1'", "hf['schema']!='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_ONLY_FREEZE_V3'")
raw=raw.replace("plan['current_actual70_build_report_pin']", "plan['current_actual70_build_report_pin']")
raw=raw.replace("current70_actual_origin=pbase,current_case_spec_pin=plan['current_case_spec_pin'],", "current70_actual_origin=pbase,current_case_spec_pin=plan['current_case_spec_pin'],\n      actual_prerequisite_receipts=gate_receipts,current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),")
raw=raw.replace("c.write(out/'Root_actual_observation_build_summary.json',dict(", "summary=out/'Root_actual_observation_build_summary.json'\n    report=dict(")
raw=replace(raw,"requires_host_process_metadata_access=True,**c.scope()))\n    if not good", "requires_host_process_metadata_access=True,final_report_bytes_in_original_resources=True,**c.scope())\n    c.write(summary,report);sp=c.pin(summary)\n    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:\n        report['status']='ACTUAL_OBSERVATION_BUILD_FAILED_UNQUALIFIED';report['failure']=type(error).__name__+': '+str(error)\n        report['after_check_error']=report['failure'];report['wall_seconds']=time.monotonic()-start\n        report['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss\n        replace_owned_failure_summary(c,summary,sp,report);good=False\n    if not good")
save('build_current_observation_runtime.py',raw.encode());ast.parse(raw)
# Producer changes source binding and actual count only. Original six capture
# and library lifecycle functions are byte-exact; future actual build selected
# solely by mandatory runtime fullpin args, never Source prediction.
raw=(OLD/'produce_current_formal_material_observations.py').read_text()
raw=raw.replace("COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'", "COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'")
raw=raw.replace("c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)","c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)\nfrom current_material_prerequisite_admission import replace_owned_failure_summary")
raw=raw.replace('observer74','observer75').replace('complete74','complete75').replace('unique74','unique75').replace('74link','75link').replace('COMPLETE74','COMPLETE75')
raw=raw.replace("hf['schema']=='COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_ONLY_FREEZE_V1'", "hf['schema']=='COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_ONLY_FREEZE_V3'")
raw=replace(raw,"    require(hf['selected_observer75_report_pin']==pbuild,\n      'own host freeze exact selected actual observation74 build report')", "    require(build['fixed_current_pins'].count(hf['selected_build_host_freeze_pin'])==1 and\n      build['current70_actual_origin']==hf['selected_actual_build70_report']and\n      build['final_report_bytes_in_original_resources']is True,\n      'runtime actual75 build must consume exact whole build host freeze and actual70 origin')")
raw=raw.replace("      requires_host_process_metadata_access=True,**FUTURE))\n    if not good", "      requires_host_process_metadata_access=True,final_report_bytes_in_original_resources=True,\n      current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),**FUTURE))\n    phase_pin=fullpin(phase)\n    try:c.check_full_current(fixed,owned);budget()\n    except BaseException as error:\n        failed=json.loads(phase.read_bytes());failed['status']='FAILED_CURRENT_OBSERVATION_NO_RETRY'\n        failed['failure']=type(error).__name__+': '+str(error);failed['after_check_error']=failed['failure']\n        failed['wall_seconds']=time.monotonic()-start;failed['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss\n        replace_owned_failure_summary(c,phase,phase_pin,failed);good=False\n    if not good")
raw=replace(raw,"    resources.check()\n\n\nif __name__=='__main__':main()", "    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:\n        failed=json.loads(phase.read_bytes());failed['status']='FAILED_CURRENT_OBSERVATION_NO_RETRY'\n        failed['failure']=type(error).__name__+': '+str(error);failed['after_check_error']=failed['failure']\n        failed['wall_seconds']=time.monotonic()-start;failed['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss\n        replace_owned_failure_summary(c,phase,fullpin(phase),failed)\n        raise\n\n\nif __name__=='__main__':main()")
save('produce_current_formal_material_observations.py',raw.encode());ast.parse(raw)
# Evidence wrapper uses explicit current metadata reader, while all extraction,
# construction, macro comparison and Budget bodies remain byte-exact.
raw=(OLD/'run_current_material_lineage_evidence.py').read_text().replace("COMMON=REC/'native_warm_A_bounded_host_source_v3/guarded_warm_A_common.py'", "COMMON=REC/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'")
raw=raw.replace("requires_host_process_metadata_access=True,physical_neutron_balance_qualified=False,", "requires_host_process_metadata_access=True,current_metadata_reattestation_provenance=c.current_metadata_reattestation_provenance(),physical_neutron_balance_qualified=False,")
raw=raw.replace("c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)","c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)\nfrom current_material_prerequisite_admission import replace_owned_failure_summary")
raw=raw.replace("c.write(out/'Root_actual_current_material_evidence_summary.json',dict(","summary=out/'Root_actual_current_material_evidence_summary.json'\n    report=dict(")
raw=replace(raw,"coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,**c.scope()))\n    if not good","coupled_370group_reference_qualified=False,scientific_accuracy_qualified=False,final_report_bytes_in_original_resources=True,**c.scope())\n    c.write(summary,report);sp=c.pin(summary)\n    try:c.check_full_current(fixed,owned);resources.check()\n    except BaseException as error:\n        report['status']='ACTUAL_CURRENT_EVIDENCE_FAILED_NO_RETRY';report['failure']=type(error).__name__+': '+str(error)\n        report['after_check_error']=report['failure'];report['wall_seconds']=time.monotonic()-start\n        report['SELF_peak_bytes']=c.resource.getrusage(c.resource.RUSAGE_SELF).ru_maxrss\n        replace_owned_failure_summary(c,summary,sp,report);good=False\n    if not good")
save('run_current_material_lineage_evidence.py',raw.encode());ast.parse(raw)
raw=(OLD/'current_material_lineage_evidence.py').read_text()
raw=replace(raw,"BASE=Path(__file__).absolute().parent", "BASE=Path(__file__).absolute().parent\nCOMMON=BASE.parent/'current_mount_full_identity_common_source_v1/guarded_warm_A_common.py'\n_cs=importlib.util.spec_from_file_location('current_evidence_explicit_mount',COMMON)\nc=importlib.util.module_from_spec(_cs);_cs.loader.exec_module(c)\nCOMPILER_EXACT_ROLE_PIN="+repr(compiler))
raw=replace(raw,"require(stat.S_ISREG(before.st_mode)and before.st_nlink==1,'regular single-link file')", "require(stat.S_ISREG(before.st_mode)and(before.st_nlink==1 or(str(path)==COMPILER_EXACT_ROLE_PIN['path']and identity(before)==COMPILER_EXACT_ROLE_PIN['identity'])),\n      'regular single-link file or exact immutable compiler role')")
raw=replace(raw,"expected['identity'][3]==1 and expected['identity'][4]==expected['size_bytes'],'strict typed SHA/size/7ID')", "(expected['identity'][3]==1 or expected==COMPILER_EXACT_ROLE_PIN)and expected['identity'][4]==expected['size_bytes'],'strict typed SHA/size/7ID and exact immutable compiler role')")
raw=replace(raw,"check(expected,budget);value=strict(Path(expected['path']).read_bytes());check(expected,budget);return value", "check(expected,budget);value,actual=c.read_bound_json_current(expected['path'],expected);require(actual==expected,'exact current metadata fullpin');check(expected,budget);return value")
save('current_material_lineage_evidence.py',raw.encode());ast.parse(raw)
raw=(OLD/'prepare_current_material_evidence_requests.py').read_bytes();save('prepare_current_material_evidence_requests.py',raw);ast.parse(raw)
# Current plan pins and physical Source/math originals are actual EOF verified.
plan=dict(oldplan)
for name in list(plan):
 if any(x in name for x in ('current_actual69','current_native_handle','current_build69','actual74')):del plan[name]
plan['schema']='CURRENT_FORMAL_MATERIAL_AUTHORITY_SOURCE_PLAN_V3'
plan['complete_source_copies']=[dict(original=reattest(r['original']),copy=pin(NEW/Path(r['copy']['path']).name),byte_exact=True)for r in oldplan['complete_source_copies']]
plan['original4_math_source_copies']=[dict(original=reattest(r['original']),copy=pin(NEW/Path(r['copy']['path']).name),byte_exact=True)for r in oldplan['original4_math_source_copies']]
for key in('current_case_spec_pin','protected_formal_and_producer_plan_pin','original_nine_Fortran_Source_freeze_pin','original_actual69_v4_report_pin'):plan[key]=reattest(oldplan[key])
plan['current_actual70_build_report_pin']=buildpin
plan['current_actual70_independent_review_pin']=pin(REC/'ROOT_INDEPENDENT_ACTUAL_COMPLETE70_CURRENT_MOUNT_BUILD_REVIEW_20261012.json')
plan['current_cache_Source_freeze_pin']=pin(build['actual_new_Source_freeze_pin']['path'])
plan['current_build70_host_Source_freeze_pin']=pin(build['actual_host_Source_freeze_pin']['path'])
plan['current_actual_build_stage_count']=3;plan['required_link']='Five observation objects inserted immediately before first archive in actual complete70; preserve all70 inputs/order including SPOT1P64.o, complete75 link.'
plan['original69_old9_and_remaining68_preserved']=True
plan['actual75_observer_build_executed']=False;plan['mandatory_replacement_zero_based_link_index']=37
plan['required_order']='true v9 AAA3 GLOBAL PROJECT onlineBOOT -> true saved full370 audit -> actual75 build -> actual one A capture -> actual extraction -> independent review -> actual aggregation and all three raw macro comparisons'
seed=json.loads((OLD/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json').read_bytes())
seed['current_case_spec_pin']=reattest(seed['current_case_spec_pin'])
for state in('A','B'):
 for row in seed['states'][state]['native_stage_inputs']:row['input_pin']=reattest(row['input_pin'])
write(NEW/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json',seed)
plan['current_seed_plan_pin']=pin(NEW/'CURRENT_FORMAL_COMPLETE_AB_ORIGINAL_MATERIAL_SEED_PLAN_SOURCE_ONLY.json')
write(NEW/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json',plan)
# Entire all70 runtime order plus5 observer inputs, linked75 no future output pins.
old70=build['records'][-1]['command'][3:-2];assert len(old70)==70 and old70==build['actual_complete70_link_inputs']
at=next(i for i,p in enumerate(old70)if p.endswith('.a'));assert at==58 and Path(old70[57]).name=='SPOT1P64.o'
out=R/'validation/artifacts/axial-material-new-current-material-observer-complete75-build-only-20261013-v4'
order=['AXMAT_CONTEXT_OBSERVATION_MOD.UNREADY.f90','LIBMIX.observe.UNREADY.f','LIBDEN.observe.UNREADY.f','TONDRV.context_observe.UNREADY.f','TONSPH.observe.UNREADY.f']
added=[str(out/'build'/(Path(n).stem+'.o'))for n in order];new75=old70[:at]+added+old70[at:];assert len(new75)==75 and [p for p in new75 if p not in added]==old70
# Explicit current view derivation only, historical JSON files untouched.
write(NEW/'EXPLICIT_CURRENT_MATERIAL_ORIGIN_REATTESTATION_SOURCE_ONLY.json',dict(schema='EXPLICIT_CURRENT_MATERIAL_ORIGIN_FULL_EOF_REATTESTATION_SOURCE_ONLY_V3',rows=rows,actual_current_catalog_pin=pin(CAT),metadata_only_not_execution=True,old_source_package_unchanged=True))
# Function inverse proof includes all science functions/classes, unchanged 4 helpers.
changes=[]
for name in('build_current_observation_runtime.py','produce_current_formal_material_observations.py','current_material_lineage_evidence.py','run_current_material_lineage_evidence.py','prepare_current_material_evidence_requests.py'):
 a=(OLD/name).read_text();b=(NEW/name).read_text();ta=ast.parse(a);tb=ast.parse(b)
 af={n.name:ast.get_source_segment(a,n)for n in ta.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))};bf={n.name:ast.get_source_segment(b,n)for n in tb.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 same=[n for n in af if af[n]==bf.get(n)];changed=[n for n in af if af[n]!=bf.get(n)]
 changes.append(dict(name=name,old_pin=pin(OLD/name),new_pin=pin(NEW/name),entire_unchanged_function_or_class_names=same,changed_function_or_class_names=changed,complete_old_source=a,complete_new_source=b))
 if name=='produce_current_formal_material_observations.py':assert all(n in same for n in('original_shared_libraries','prepare_shared_libraries','recheck_shared_libraries','derive_original_procedure','copy_state_seeds','collect_state','release_closed_owned_library_copies'))
 if name=='current_material_lineage_evidence.py':assert all(n in same for n in('Budget','extract','aggregate','compare_raw_macro','source_admission','admit_owning_stage'))
 if name=='prepare_current_material_evidence_requests.py':assert a==b
write(NEW/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json',dict(schema='COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_AND_METADATA_INVERSE_V3',source_only=True,old_frozen_package_fullpins=oldpins,entire_byte_copy_pins=copies,changed_Source_full_old_new_bodies=changes,actual_complete70_origin_pin=buildpin,complete70_order=old70,observer_insertion_zero_based_index_in70=at,observer_objects=added,complete75_order=new75,all70_inputs_order_preserved=True,four_archives_preserved=True,only_metadata_admission_and_count_changes_not_math=True,compiler_exact_immutable_role_pin=compiler,no_future_output_pins_predicted=True,compiler_executed=False,material_job_executed=False,evidence_or_science_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
# MathSource freeze new paths but identical full5 hooks and all math copies.
sf=dict(schema='COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE_V1',files=[pin(NEW/n)for n in order],original_math_sources=[reattest(p)for p in oldsf['original_math_sources']],current_plan_pin=pin(NEW/'CURRENT_FORMAL_MATERIAL_AUTHORITY_SELECTED_CACHE70_PLAN.json'),original_caps=oldsf['original_caps'],original_five_Source_order=order,complete_math_inverse_proof_pins=[pin(NEW/'COMPLETE_CURRENT70_CURRENT_MATERIAL_SOURCE_INVERSE.json')]+[pin(NEW/n)for n in('COMPLETE_CONTEXT_AWARE_SOURCE_FULL_INVERSE.json','COMPLETE_OBSERVATION_FORTRAN_SOURCE_INVERSE.json')],selected_actual70_report_pin=buildpin,compiler_executed=False,material_job_executed=False,candidate_imported_or_executed=False,scientific_accuracy_qualified=False,reaction_multiplicity_qualified=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json',sf)
bhf=dict(schema='COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_ONLY_FREEZE_V3',host_source=pin(NEW/'build_current_observation_runtime.py'),dependencies=[pin(p)for p in sorted(NEW.iterdir())if p.is_file()and p.name!='build_current_observation_runtime.py']+[pin(COMMON),pin(COMMON.parent/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'),pin(CAT),buildpin,pin(BOOT_HF),pin(BOOT_HOST),pin(SCI_HF),pin(SCI_HOST)],selected_actual_build70_report=buildpin,selected_original_actual69_handle_lifetime_report=pin(build['original_actual69_handle_lifetime_report_pin']['path']),selected_original_actual69_v4_report=pin(build['original_actual69_v4_report_pin']['path']),selected_native_exact_block_cache_source_freeze=pin(build['actual_new_Source_freeze_pin']['path']),selected_source_freeze_pin=pin(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),required_actual_AAA3_output_directory=str(R/'validation/artifacts/axial-material-new-AAA3-streaming-actual-operator-global-BOOT-20261012-v9'),required_actual_saved_audit_output_directory=str(R/'validation/artifacts/axial-material-AAA-saved-full370-terminal-source-diagnostic-current-mount-guarded-20261013-v2'),required_actual_AAA3_host_freeze_pin=pin(BOOT_HF),required_actual_saved_audit_host_freeze_pin=pin(SCI_HF),required_future_receipt_arguments=['aaa3-summary','aaa3-sha256','aaa3-seven-id','saved-audit-summary','saved-audit-sha256','saved-audit-seven-id'],future_actual_receipts_not_predicted_or_pinned=True,all70_inputs_order_retained=True,new_link_input_count=75,planned_stage_count=6,compiler_executed=False,transport_executed=False,material_job_executed=False,original_caps=oldsf['original_caps'],requires_host_process_metadata_access=True,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json',bhf)
# Static producer freeze has exact current70/buildSource origins; Root supplies
# the actual75 report after true6stage closure, no future actual report pins.
phf=dict(schema='COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_ONLY_FREEZE_V3',host_source=pin(NEW/'produce_current_formal_material_observations.py'),dependencies=bhf['dependencies']+[pin(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json')],selected_actual_build70_report=buildpin,selected_build_host_freeze_pin=pin(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'),selected_seed_plan_pin=plan['current_seed_plan_pin'],required_dynamic_actual75_report_arguments=['observer75-summary','observer75-sha256','observer75-seven-id'],future_actual75_report_not_predicted_or_pinned=True,material_job_executed=False,compiler_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False)
write(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_HOST_SOURCE_FREEZE.json',phf)
sourcefiles=[pin(p)for p in sorted(NEW.glob('*.py'))]+[pin(COMMON),pin(COMMON.parent/'CURRENT_WARM_A_COMPLETE_HOST_SOURCE_BINDING.json'),pin(CAT)]
write(NEW/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json',dict(schema='COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_ONLY_FREEZE_V1',complete_source_file_pins=sourcefiles,candidate_executed=False,compiler_executed=False,material_job_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
write(NEW/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_FREEZE.json',dict(schema='COMPLETE_CURRENT_MATERIAL_EVIDENCE_HOST_SOURCE_ONLY_FREEZE_V1',host_source=pin(NEW/'run_current_material_lineage_evidence.py'),dependencies=sourcefiles+[pin(NEW/'COMPLETE_CURRENT_MATERIAL_EVIDENCE_SOURCE_FREEZE.json')],candidate_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
argv=['/Users/wen/miniforge3/envs/openmc-dev/bin/python3.12','-B',str(NEW/'build_current_observation_runtime.py')]
for prefix,p in [('current70',buildpin),('source-freeze',pin(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json')),('host-freeze',pin(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'))]:
 for suffix,v in [('summary',p['path']),('sha256',p['sha256']),('seven-id',json.dumps(p['identity'],separators=(',',':')))]:argv+=['--'+prefix+'-'+suffix,v]
argv+=['--output-dir',str(out)]
write(NEW/'ROOT_REVIEWABLE_CURRENT70_OBSERVER75_STATIC_ARGV_AND_REQUIRED_ACTUAL_GATES_SOURCE_ONLY.json',dict(schema='CURRENT70_OBSERVER75_STATIC_SOURCE_ONLY_ARGV_WITH_MANDATORY_FUTURE_ACTUAL_ARGUMENTS_V3',static_argv=argv,mandatory_actual_arguments_to_append=['--aaa3-summary','--aaa3-sha256','--aaa3-seven-id','--saved-audit-summary','--saved-audit-sha256','--saved-audit-seven-id'],is_complete_executable_argv=False,incomplete_until_Root_supplies_actual_completed_receipts=True,environment={k:'1'for k in('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONDONTWRITEBYTECODE')},environment_to_remove=['PYTHONOPTIMIZE'],cwd=str(R),source_plan=sf['current_plan_pin'],actual70_report=buildpin,math_source_freeze=pin(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),build_host_freeze=pin(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'),planned_complete75_link_order=new75,compiler_executed=False,material_job_executed=False,AAA_qualified=False,ABA_admitted=False,goal_complete=False))
# Read whole old/new Source and AST only; no import/compile/build/material/evidence.
for p in OLD.glob('*.py'):ast.parse(p.read_bytes())
for p in NEW.glob('*.py'):ast.parse(p.read_bytes())
for p in oldpins:assert pin(p['path'])==p
print(json.dumps(dict(status='NEW_MATERIAL_CURRENT70_SOURCE_WRITTEN_NO_CANDIDATE_IMPORT_OR_BUSINESS_EXECUTION',namespace=str(NEW),Python_source_count=len(list(NEW.glob('*.py'))),byte_exact_file_count=len(copies),complete70_inputs=len(old70),complete75_inputs=len(new75),new_math_source_freeze=pin(NEW/'COMPLETE_CURRENT_MATERIAL_OBSERVATION_MATH_SOURCE_FREEZE.json'),new_build_host_freeze=pin(NEW/'COMPLETE_CURRENT_OBSERVATION_BUILD_HOST_SOURCE_FREEZE.json'))))
