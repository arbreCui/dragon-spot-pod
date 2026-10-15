"""Prepare one failure-only A8 MCCGF442 owned STATE observer; no business."""
import hashlib,json,os,re,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
BASE=R/'boot_v16_A8_247_false_return_diagnostic_source_v1_20261014'
OUT=R/'boot_v16_A8_MCCGF442_state_failure_snapshot_source_v1_20261014'
EVENT_SCHEMA='ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1'

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

SNAPSHOT_BLOCK='''      block
        use GANLIB, only : A8_DIAG_LCMINF => LCMINF, &
            A8_DIAG_LCMLEN => LCMLEN, A8_DIAG_LCMGET => LCMGET
        integer :: diag_state_length, diag_state_type, diag_list_length
        integer :: diag_state_owned40(40)
        logical :: diag_empty, diag_memory, diag_snapshot_verified
        character(len=72) :: diag_object_name
        character(len=12) :: diag_directory_name

        call A8_DIAG_LCMINF(iptrk,diag_object_name,diag_directory_name, &
            diag_empty,diag_list_length,diag_memory)
        call A8_DIAG_LCMLEN(iptrk,'STATE-VECTOR', &
            diag_state_length,diag_state_type)
        diag_snapshot_verified = diag_state_length == 40 .and. &
            diag_state_type == 1
        if (diag_snapshot_verified) then
          call A8_DIAG_LCMGET(iptrk,'STATE-VECTOR',diag_state_owned40)
          write(6,'(*(G0))') &
              '{"schema":"ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1",', &
              '"original_return_source_line":442,"nbmix":',nbmix, &
              ',"nsou":',nsou,',"nreg":',nreg,',"nun":',nun, &
              ',"actual_STATE_length":',diag_state_length, &
              ',"actual_STATE_type":',diag_state_type, &
              ',"actual_LCMINF_memory_object":', &
              trim(merge('true ','false',diag_memory)), &
              ',"snapshot_verified":true,"fresh_STATE4":',diag_state_owned40(4), &
              ',"fresh_STATE5":',diag_state_owned40(5),'}'
        else
          write(6,'(*(G0))') &
              '{"schema":"ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1",', &
              '"original_return_source_line":442,"nbmix":',nbmix, &
              ',"nsou":',nsou,',"nreg":',nreg,',"nun":',nun, &
              ',"actual_STATE_length":',diag_state_length, &
              ',"actual_STATE_type":',diag_state_type, &
              ',"actual_LCMINF_memory_object":', &
              trim(merge('true ','false',diag_memory)), &
              ',"snapshot_verified":false,"fresh_STATE4":null,"fresh_STATE5":null}'
        end if
        flush(6)
      end block
'''

def main():
    if OUT.exists():raise RuntimeError('unique failure snapshot Source namespace')
    cp0=BASE/'SPOR64_A8.f90';originalpin=pin(cp0);original=cp0.read_text();invpin=pin(BASE/'COMPLETE_A8_247_FALSE_RETURN_SOURCE_WHOLE_BYTE_INVERSE.json');inv=read(invpin);spp=pin(BASE/'SOURCE_ONLY_A8_247_FALSE_RETURN_DIAGNOSTIC_PLAN.json');sfpin=pin(BASE/'COMPLETE_A8_247_FALSE_RETURN_DIAGNOSTIC_SOURCE_FREEZE.json');sf=read(sfpin)
    if originalpin['sha256']!='dbbe4e88abaa6dacfcfb7eaf56b01bcbf307f54bb73d05740ebad9539adb711f'or sfpin['sha256']!='a21fb8ae44041c923e9e134231c45d6b161002cb40c98d8b7ddca36ff0d0c76e'or len(inv['changes'])!=247 or sf['diagnostic_source_pin']!=originalpin:raise RuntimeError('actual compiled A8 Source247/SF original authority')
    site=[c for c in inv['changes']if c['scope']=='MCCGF64'and c['original_return_source_line']==442]
    if len(site)!=1 or site[0]['before']!='    if (nbmix <= 0) return\n':raise RuntimeError('original442 exact nbmix condition, never443')
    before=site[0]['after'];prefix='    if (nbmix <= 0) then\n'
    if not before.startswith(prefix)or original.count(before)!=1:raise RuntimeError('unique actual compiled failure442 block')
    after=prefix+SNAPSHOT_BLOCK+before[len(prefix):];current=original.replace(before,after,1)
    if current.count(after)!=1 or current.replace(after,before,1).encode()!=cp0.read_bytes():raise RuntimeError('complete one-block dbbe inverse')
    if any(len(l)>132 for l in current.splitlines()):raise RuntimeError('free-form lines <=132')
    if any(word in SNAPSHOT_BLOCK.lower()for word in('state_vector(', 'mccg_state(', 'real_param32(', 'c_loc(', 'loc('))or re.search(r'^\s*return\s*$',SNAPSHOT_BLOCK,re.M|re.I):raise RuntimeError('observer never reads old views, requests addresses, or adds return')
    if SNAPSHOT_BLOCK.count("call A8_DIAG_LCMGET(iptrk,'STATE-VECTOR',diag_state_owned40)")!=1 or SNAPSHOT_BLOCK.count('integer :: diag_state_owned40(40)')!=1:raise RuntimeError('exact single owned40int160B read')
    if current.count('"predicate_id":"A8_')!=247 or any(current.count(c['after'])!=1 for c in inv['changes']if c['original_return_source_line']!=442 or c['scope']!='MCCGF64'):raise RuntimeError('all247 events and other246 blocks retained')
    if current[:current.index('contains\n')+len('contains\n')]!=original[:original.index('contains\n')+len('contains\n')]:raise RuntimeError('whole original module declarations/public ABI')
    actualpath=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-A8-false-return-diagnostic-20261014-v1/Root_actual_one_BOOT_status_diagnostic_summary.json');actualpin=pin(actualpath);actual=read(actualpin);outcome=actual['actual_outcome'];e=outcome['actual_A8_first_false_return']
    if e['predicate_id']!='A8_MCCGF64_RETURN_L0442'or e['original_return_source_line']!=442 or e['actual_boolean_status_integer']!=0 or outcome['actual_diagnostic']['boot_plane']!=1 or outcome['actual_diagnostic']['actual_return_status']!=2:raise RuntimeError('actual failure442 only, no hypothetical443')
    table={p['path']:norm(p)for p in actual['fixed_current_pins']+actual['output_pins']};old70=[table[p]for p in actual['actual_ordered70_link_inputs']];modulepin=table[str(Path(old70[1]['path']).with_name('spor64_a8.mod'))]
    if modulepin['sha256']!='2d1878cbfbf324af67c2be7980946b26244f9b7d59594abbbb4bad167ccc2203'or modulepin['size_bytes']!=6092 or pin(modulepin['path'])!=modulepin:raise RuntimeError('actual6092 same ABI module')
    api_paths=[Path('/Users/wen/spot/src/SPOR64_GANLIB_ABI.f90'),Path('/Users/wen/spot/Ganlib/src/LCMAUX.f90'),Path('/Users/wen/spot/Ganlib/src/lcm_c.c'),Path('/Users/wen/spot/Ganlib/src/xsm_c.c'),Path('/Users/wen/spot/Ganlib/src/xsm.h')];api=[pin(q)for q in api_paths]
    if any(table.get(p['path'])!=p for p in api):raise RuntimeError('actual fixed Ganlib ABI/XSM Sources')
    OUT.mkdir();cp=OUT/'SPOR64_A8.f90';write(cp,current);ip=OUT/'COMPLETE_A8_247_TO_MCCGF442_FAILURE_SNAPSHOT_WHOLE_BYTE_INVERSE.json'
    write(ip,dict(schema='COMPLETE_A8_247_TO_MCCGF442_FAILURE_SNAPSHOT_WHOLE_BYTE_INVERSE_V1',original_source_pin=originalpin,diagnostic_source_pin=pin(cp),changes=[dict(scope='MCCGF64',original_return_source_line=442,before=before,after=after)],whole_file_inverse_byte_equal=True,all247_original_failure_IDs_and_conditions_once_and_returns_unchanged=True,all_original_declarations_public_ABI_math_loops_allocations_status_assignments_and_original_IO_order_unchanged=True,only_original442_failure_observer_before_original_false_event_and_return_added=True,no_old_borrowed_view_read_or_address_evaluation=True,no_new_early_return_and_original_nbMix_false_condition_unchanged=True,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False))
    pp=OUT/'SOURCE_ONLY_A8_MCCGF442_FAILURE_SNAPSHOT_PLAN.json'
    plan=dict(schema='SOURCE_ONLY_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_PLAN_V1',event_schema=EVENT_SCHEMA,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,original_source_pin=originalpin,original_active_normalization_source_pin=sf['original_source_pin'],diagnostic_source_pin=pin(cp),complete_byte_inverse_pin=pin(ip),Source_preparer_pin=pin(__file__),selected_original_A8_247_Fortran_Source_freeze_pin=sfpin,selected_original_A8_247_Source_plan_pin=spp,selected_original_A8_247_Source_inverse_pin=invpin,original_return_mapping247=sf['original_return_mapping'],original_scope_counts=sf['scope_counts'],all247_original_failed_events_unchanged=True,only_original_failed_MCCGF442_observer_added=True,original_nbMix442_condition_unchanged_and_evaluated_once=True,original443_state1_state2_condition_not_executed_or_changed_here=True,observer_existing_scalar_fields=['nbmix','nsou','nreg','nun'],only_additional_scientific_record_read=dict(name='STATE-VECTOR',LCM_length=40,LCM_type=1,maximum_bytes=160,owned_copy=True,read_only_if_both_exact_length40_and_type1=True,output_only_indices=[4,5],invalid_shape_does_not_read_and_outputs_explicit_null=True),actual_LCMINF_memory_flag_required_not_assumed=True,observed_old_borrowed_pointer_aliases=False,old_borrowed_pointer_views_never_read_or_address_evaluated=True,reason_old_pointer_address_observer_omitted='XSM GPD may free old borrowed targets; C_LOC association/lifetime prerequisites not proven. No address aliases or old view values claimed.',new_snapshot_cannot_change_original_false_status_or_add_any_return=True,block_local_GANLIB_module_imports_only_public_Module_ABI_unchanged=True,all_original_math_conditions_io_order_success_returns_probes_ACA_and_normalization486_488_unchanged=True,actual_prior_A8_failure_report_pin=actualpin,actual_prior_A8_failure_chain=outcome['actual_A8_failed_return_chain'],actual_prior_A9_failure_chain=outcome['actual_A9_failed_return_chain'],actual_retained_A8_object1_pin=old70[1],original_module_pin=modulepin,current_actual_ordered70_pins=old70,replacement_zero_based_link_index=1,all_other69_A9actual2_Native47_BOOTB49_BOXX68_Driver37_BOOTQ40_math57_archives_unchanged_required=True,actual_API_Source_pins=api,selected_actual_Ganlib_archive_pin=table['/Users/wen/spot/Ganlib/lib/Darwin_arm64/libGanlib.a'],selected_actual_Dragon_archive_pin=table['/Users/wen/spot/lib/Darwin_arm64/libDragon.a'],Source_API_lifetime_findings_not_actual_capture_values=dict(XSM_output_buffer_registry_key='address of output c_ptr storage cell, not record name',XSM_same_length_reuses_and_overwrites_buffer=True,XSM_different_length_frees_old_buffer_before_new_malloc=True,LCM_memory_backend_returns_record_specific_jdata=True),original_module6092_wholebyte_equality_required=True,future_actual_Source_freeze_pin=None,future_actual_Host_freeze_pin=None,future_actual_cleanup_proof_pins=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,future_actual_snapshot_values=None,engineering_qualified=False,physics_qualified=False)
    write(pp,plan);rp=OUT/'READY.json';write(rp,dict(schema='SOURCE_ONLY_A8_MCCGF442_FAILURE_SNAPSHOT_READY_V1',status='SOURCE_ONLY_FAILURE442_OWNED160B_SNAPSHOT_READY_NO_RUNTIME',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),Source_preparer_pin=pin(__file__),maximum_additional_scientific_record_read_bytes=160,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,future_actual_Source_freeze_pin=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,future_actual_snapshot_values=None))
    if pin(cp0)!=originalpin or pin(modulepin['path'])!=modulepin:raise RuntimeError('original Source/module wholeEOF7 retained')
    print(json.dumps(dict(status='SOURCE_ONLY_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_READY',Source_pin=pin(cp),inverse_pin=pin(ip),PLAN_pin=pin(pp),READY_pin=pin(rp),Source_preparer_pin=pin(__file__),compiled=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
