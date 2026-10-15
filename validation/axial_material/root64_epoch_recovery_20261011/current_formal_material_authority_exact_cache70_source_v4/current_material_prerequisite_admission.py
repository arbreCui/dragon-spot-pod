"""Actual prerequisites for the ordered material transaction; no transport code.

Root must supply true completed AAA3/BOOT and saved full370 audit report pins.
No future file hash, receipt or successful stage is predicted in Source metadata.
"""
import hashlib,json,os,stat,time
from pathlib import Path
BASE=Path(__file__).absolute().parent
def require(ok,message):
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
    raw=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
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
