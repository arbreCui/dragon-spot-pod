"""Prepare one private BIND consumer correction; no compiler/business/deletion."""
import hashlib,json,os,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=R/'boot_v16_BIND64_failed_PHYS_inventory_diagnostic_source_v1_20261014'
OUT=R/'boot_v16_BIND64_strict_native17_consumer_source_v1_20261014'
def ids(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def pin(p):
 p=Path(p);s=p.lstat();f=os.open(p,os.O_RDONLY|os.O_NOFOLLOW)
 try:
  if not stat.S_ISREG(s.st_mode)or ids(os.fstat(f))!=ids(s):raise RuntimeError('ordinary Source/proof')
  h=hashlib.sha256()
  while True:
   b=os.read(f,1024*1024)
   if not b:break
   h.update(b)
  if ids(os.fstat(f))!=ids(s)or ids(p.lstat())!=ids(s):raise RuntimeError('Source/proof changed')
 finally:os.close(f)
 return dict(path=str(p),sha256=h.hexdigest(),size_bytes=s.st_size,identity=ids(s))
def write(name,data):
 p=OUT/name
 if isinstance(data,dict):data=(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()
 elif isinstance(data,str):data=data.encode()
 with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(data);f.flush();os.fsync(f.fileno())
 return pin(p)
def main():
 oldpin=pin(BASE/'SPOR64_BOOT_BIND64.f90')
 if oldpin['sha256']!='c56db28afac9fb3944e8cd617531fb7dd8d8a504677e84e4d6a037a1d6b54318':raise RuntimeError('exact actual inventory BIND Source')
 old=Path(oldpin['path']).read_text();new=old;changes=[]
 def change(before,after,reason):
  nonlocal new
  if new.count(before)!=1:raise RuntimeError('unique Source splice')
  new=new.replace(before,after,1);changes.append(dict(before=before,after=after,reason=reason))
 change('''    integer :: response_lengths(size(SCHEMA_RESPONSE_GROUP)), i

    RESPONSE_GROUP_IS_EXACT = .false.''','''    integer :: response_lengths(size(SCHEMA_RESPONSE_GROUP)), i
    character(len=12),parameter :: native17_names(17) = &
        [SCHEMA_RESPONSE_GROUP_PHYS,'AXMAT-V64   ','PJJ64$MCCG  ']
    integer :: native_length,native_type
    real(real64) :: native_axv64(14),native_pjj64(8)
    real(real32) :: native_pjj32(8)
    logical :: native17

    RESPONSE_GROUP_IS_EXACT = .false.''',
 'Function-local exact17 names and bounded validation scratch only; module declarations/public and private function signatures unchanged.')
 before='''      if (.not. EXACT_INVENTORY(group,SCHEMA_RESPONSE_GROUP_PHYS)) then
        write(6,'(A,I0,A)') &'''
 after='''      if (.not. EXACT_INVENTORY(group,SCHEMA_RESPONSE_GROUP_PHYS)) then
        native17=EXACT_INVENTORY(group,native17_names)
        if(native17)then
          native17=nreg==8.and.nunkno==14.and.nsurf==6.and.paca==4.and.lc0==0
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_SCOPE_8_14_6_PACA4_LC0ZERO","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMLEN(group,'AXMAT-V64',native_length,native_type)
          native17=native_length==14.and.native_type==4
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_AXMAT_14_TYPE4","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMLEN(group,'PJJ64$MCCG',native_length,native_type)
          native17=native_length==8.and.native_type==4
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_PJJ64_8_TYPE4","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMLEN(group,'PJJ$MCCG',native_length,native_type)
          native17=native_length==8.and.native_type==2
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_PJJ32_8_TYPE2","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMGET(group,'AXMAT-V64',native_axv64)
          native17=all(ieee_is_finite(native_axv64)).and.all(native_axv64>0.0_real64)
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_AXMAT_FINITE_POSITIVE","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMGET(group,'PJJ64$MCCG',native_pjj64)
          native17=all(ieee_is_finite(native_pjj64))
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_PJJ64_FINITE","actual_boolean_status_integer":0}'
          endif
        endif
        if(native17)then
          call LCMGET(group,'PJJ$MCCG',native_pjj32)
          native17=all(transfer(real(native_pjj64,real32),[0_int32],8)== &
              transfer(native_pjj32,[0_int32],8))
          if(.not.native17)then
            write(6,'(A)') &
              '{"schema":"ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1",'// &
              '"predicate_id":"NATIVE17_PJJ32_DEMOTE_WORD_BITS","actual_boolean_status_integer":0}'
          endif
        endif
        if(.not.native17)then
        write(6,'(A,I0,A)') &'''
 change(before,after,
 'Only after original exact15 fails, exact native17 complete names then fixed native owner scope/typed bounded reads/finite positive AXV/finite PJJ and REAL32 demote bitmirror. No generic extras or value changes; no new return.')
 before='''        end block
        return
      endif
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)'''
 after='''        end block
        return
        endif
      endif
    end if
    do i = 1, size(SCHEMA_RESPONSE_GROUP)'''
 change(before,after,
 'Close native17 rejection wrapper around original236 failed event/header inventory/return; all original subsequent P3/15 FINITE and macro bit validation stays in place once.')
 back=new
 for x in reversed(changes):
  if back.count(x['after'])!=1:raise RuntimeError('unique whole Source inverse')
  back=back.replace(x['after'],x['before'],1)
 if back!=old or max(map(len,new.splitlines()))>132 or new.count('ACTUAL_BOOT_BIND64_EXPLICIT_RETURN_DIAGNOSTIC_V1')!=82:raise RuntimeError('whole inverse/line bound/82 original events')
 reportpath=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-failed-PHYS-group-inventory-diagnostic-20261014-v1/Root_actual_one_BOOT_status_diagnostic_summary.json')
 report=json.loads(reportpath.read_bytes());outcome=report['actual_outcome'];inv=outcome['actual_failed_PHYS_group_inventory'];rows=inv['actual_inventory_records']
 observed=[dict(name_bytes_hex=e['name_bytes_hex'],name=bytes.fromhex(e['name_bytes_hex']).decode('ascii'),length=e['length'],type=e['type'])for e in rows]
 names={e['name'].rstrip(' ')for e in observed};expected={'CF$MCCG','ILUDF$MCCG','CQ$MCCG','DIAGQ$MCCG','PJJ$MCCG','PJJX$MCCG','PJJY$MCCG','PJJZ$MCCG','PJJXI$MCCG','PJJYI$MCCG','PJJZI$MCCG','DRAGON-TXSC','SPOT-S0-PHYS','DRAGON-S0XSC','DIAGF$MCCG','AXMAT-V64','PJJ64$MCCG'}
 if inv['actual_complete_header_inventory_observed']is not True or inv['actual_inventory_end']['complete_integer']!=1 or inv['actual_inventory_end']['truncated_integer']!=0 or len(rows)!=17 or inv['actual_caller']['group_index']!=1 or inv['actual_caller']['plane_index']!=1 or names!=expected:raise RuntimeError('actual group1 plane1 complete exact17 header provenance')
 for name,length in [('AXMAT-V64',14),('PJJ64$MCCG',8)]:
  if [e for e in observed if e['name'].rstrip(' ')==name][0]['length']!=length or [e for e in observed if e['name'].rstrip(' ')==name][0]['type']!=4:raise RuntimeError('actual native header shape4')
 OUT.mkdir();candidate=write('SPOR64_BOOT_BIND64.f90',new)
 ip=write('COMPLETE_NATIVE17_CONSUMER_SOURCE_WHOLE_BYTE_INVERSE.json',dict(schema='COMPLETE_FAILED_PHYS_INVENTORY_TO_STRICT_NATIVE17_CONSUMER_SOURCE_WHOLE_BYTE_INVERSE_V1',original_source_pin=oldpin,candidate_source_pin=candidate,changes=changes,whole_byte_inverse_exact=True,source_only=True))
 science=[pin('/Users/wen/spot/validation/artifacts/axial-material-r64-system-normalization-20261003/build/'+n)for n in ['MCGASM.f','MCGFST.f']]
 rejection_ids=['NATIVE17_SCOPE_8_14_6_PACA4_LC0ZERO','NATIVE17_AXMAT_14_TYPE4','NATIVE17_PJJ64_8_TYPE4','NATIVE17_PJJ32_8_TYPE2','NATIVE17_AXMAT_FINITE_POSITIVE','NATIVE17_PJJ64_FINITE','NATIVE17_PJJ32_DEMOTE_WORD_BITS']
 pp=write('SOURCE_ONLY_STRICT_NATIVE17_CONSUMER_PLAN.json',dict(schema='SOURCE_ONLY_PRIVATE_BIND64_STRICT_NATIVE17_CONSUMER_PLAN_V1',source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,diagnostic_source_pin=candidate,predecessor_source_pin=oldpin,predecessor_Fortran_Source_freeze_pin=pin(BASE/'COMPLETE_BOOT_BIND64_FAILED_PHYS_GROUP_INVENTORY_DIAGNOSTIC_SOURCE_FREEZE.json'),complete_byte_inverse_pin=ip,actual_prior_inventory_report_pin=pin(reportpath),actual_prior_inventory_Root_true_tool_pin=pin(R/'ROOT_ACTUAL_ONE_BIND47_FAILED_PHYS_INVENTORY_DIAGNOSTIC_V1_TRUE_TOOL_RETURNS_20261014.json'),actual_complete_observed_group_index=1,actual_complete_observed_plane_index=1,actual_complete_observed_header_inventory=observed,unobserved_other369_groups_not_claimed=True,actual_native_payload_not_previously_read_or_validated=True,active_original_native_producer_and_consumer_Source_pins=science,all_other69_ordered_runtime_inputs_must_remain_exact=True,only_zero_based_runtime_replacement_index=47,retain_actual_BOOTB49_and_BOXX68_and_Q40_Driver37_math57=True,module_public_ABI_and_private_function_signatures_unchanged=True,new_module_wholebytes_original2988_ABI_equality_required=True,native17_complete_names=sorted(expected),native17_fixed_scope=dict(nreg=8,nunkno=14,nsurf=6,paca=4,lc0=0),native17_checks=['AXMAT-V64 exact14/type4/finite/positive','PJJ64$MCCG exact8/type4/finite','PJJ$MCCG exact8/type2 then REAL32 demote exact INT32 bits'],original15_and_P3_exact_forms_and_original_all_subsequent_checks_preserved=True,unknown_extra_missing_one_native_field_and_native_wrong_shape_rejected=True,original_EXACT_INVENTORY_not_modified=True,all_original82_events_returns_condition_expressions_and_loops_preserved_except_explicit_native17_inventory_extension=True,no_new_API_no_new_return_no_solver_flux_source_formula_or_operand_value_change=True,geometry_source_authority='Actual unchanged nonprism regular MCGASM integrates AXV then original positive and relative-to-V <=2e-6 check; no new geometry recomputation or new tolerance',native_records_are_numerical_owners_in_original_MCGFST_not_unused_metadata=True,native17_rejection_event_schema='ACTUAL_BOOT_BIND64_NATIVE17_REJECTION_V1',native17_rejection_predicate_ids=rejection_ids,native17_rejection_event_before_original_RESPONSE236_inventory_SYSTEM168_READ97_BOOTB466_outer_status=True,all_original_resource_and_physics_thresholds_unchanged=True,original_caps=report['original_caps'],future_actual_independent_prior_post_review_pin=None,future_actual_independent_prior_post_tools_pin=None,future_cleanup_receipt_pin=None,future_current_budget_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,future_actual_native17_payload_checks_all370_passed=None,engineering_qualified=False,physics_qualified=False,source_preparer_pin=pin(__file__)))
 rp=write('READY.json',dict(schema='PREPARED_STRICT_NATIVE17_BIND_CONSUMER_SOURCE_ONLY_V1',status='PASS_SOURCE_ONLY_PREPARATION_NO_COMPILER_OR_BUSINESS',failure=None,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,source_pin=candidate,inverse_pin=ip,plan_pin=pp,preparer_pin=pin(__file__),whole_byte_inverse_exact=True,future_actual_object_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None))
 f=os.open(OUT,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
 try:os.fsync(f)
 finally:os.close(f)
 print(json.dumps(dict(status='PREPARED_STRICT_NATIVE17_BIND_CONSUMER_SOURCE_ONLY',source_pin=candidate,inverse_pin=ip,plan_pin=pp,ready_pin=rp,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
