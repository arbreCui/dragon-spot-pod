"""Source-only caller-owned A8 MAP lifetime repair; no compiler/business/delete.

The frozen capture Source is the complete byte parent.  Only caller-local
owners, typed LCMGET reads after the original successful MAP guards, pointer
reassociation, and splitting the existing P3 owner allocation are added.
"""
import hashlib,json,os,re,stat
from pathlib import Path
R=Path('/Users/wen/spot/validation/axial_material/root64_epoch_recovery_20261011')
P=R/'boot_v16_A8_18_owned_persistent_MAP_lifetime_source_v1_20261014'
CAP=R/'boot_v16_A8_MCCGF442_state_failure_snapshot_source_v1_20261014'
ORIGINAL=CAP/'SPOR64_A8.f90'
CAP_SF=CAP/'COMPLETE_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_SOURCE_FREEZE.json'
ROOT_TOOLS=R/'ROOT_ACTUAL_ONE_MCCGF442_FAILURE_SNAPSHOT_V1_TRUE_TOOL_RETURNS_20261014.json'
ROOT_ARGV=R/'ROOT_EXACT_ONE_MCCGF442_FAILURE_SNAPSHOT_V1_ACTUAL_ARGV_20261014.json'
REPORT=Path('/Users/wen/spot/validation/artifacts/axial-material-new-one-BOOT-MCCGF442-failure-snapshot-20261014-v1/Root_actual_one_BOOT_status_diagnostic_summary.json')
ROOT_HF=R/'boot_v16_A8_MCCGF442_failure_snapshot_host_source_v1_20261014/COMPLETE_GUARDED_ONE_BOOT_MCCGF442_FAILURE_SNAPSHOT_HOST_SOURCE_FREEZE.json'
def identity(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def norm(p):return{k:p[k]for k in('path','sha256','size_bytes','identity')}
def pin(p):
    p=Path(p);s=p.lstat()
    if not stat.S_ISREG(s.st_mode)or s.st_size>64*2**20:raise RuntimeError('bounded Source/metadata only; no scientific body EOF')
    with os.fdopen(os.open(p,os.O_RDONLY|os.O_NOFOLLOW),'rb')as f:
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('opened7')
        b=f.read()
        if identity(os.fstat(f.fileno()))!=identity(s):raise RuntimeError('FD7')
    if identity(p.lstat())!=identity(s):raise RuntimeError('after7')
    return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),identity=identity(s))
def read(p):
    if isinstance(p,dict):
        if pin(p['path'])!=norm(p):raise RuntimeError('exact metadata Source PF')
        p=p['path']
    else:pin(p)
    return json.loads(Path(p).read_bytes())
def write(p,v):
    b=(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()if isinstance(v,dict)else v.encode()
    with os.fdopen(os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644),'wb')as f:f.write(b);f.flush();os.fsync(f.fileno())

def main():
    if P.exists():raise RuntimeError('unique new Source package; never overwrite old frozen Source')
    original_pin=pin(ORIGINAL);original=ORIGINAL.read_text();s=original
    if original_pin['sha256']!='70799cf8cda3131dd785dbedf1818e58094c5793eae7214ce21c4949ae6c2115':raise RuntimeError('only frozen actual capture Source parent')
    sfpin=pin(CAP_SF);sf=read(sfpin);reportpin=pin(REPORT);report=read(reportpin);rootpin=pin(ROOT_TOOLS);root=read(rootpin);argvpin=pin(ROOT_ARGV);hfpin=pin(ROOT_HF);hf=read(hfpin)
    tr=root['actual_terminal_return']
    if type(tr['exit_code'])is not int or tr['exit_code']!=1 or tr.get('session_id')is not None or root['observed_closed']is not True or type(root['original_integer_exit_code'])is not int or root['original_integer_exit_code']!=1:raise RuntimeError('genuine closed Root capture EXIT1, not a success qualification')
    outcome=report['actual_outcome'];snapshot=outcome['actual_MCCGF442_failure_snapshot']
    if snapshot!=dict(schema='ACTUAL_SPOR64_A8_MCCGF442_STATE_FAILURE_SNAPSHOT_V1',original_return_source_line=442,nbmix=0,nsou=0,nreg=8,nun=14,actual_STATE_length=40,actual_STATE_type=1,actual_LCMINF_memory_object=False,snapshot_verified=True,fresh_STATE4=8,fresh_STATE5=6)or [(r['scope'],r['original_return_source_line'])for r in outcome['actual_A8_failed_return_chain']]!=[('MCCGF64',442),('DOORFV64',359)]or [(r['scope'],r['original_return_source_line'])for r in outcome['actual_A9_failed_return_chain']]!=[('FLU2DR64_CORE',233)]or outcome['actual_diagnostic']['actual_return_status']!=2 or report['engineering_qualified']is not False or report['physics_qualified']is not False:raise RuntimeError('actual bounded mismatch only; no guessed overwrite/free distinction or physics claim')
    if report['actual_host_Source_freeze_pin']!=hfpin or report['actual_diagnostic_Fortran_Source_freeze_pin']!=sfpin or sf['diagnostic_source_pin']!=original_pin or sf['original_return_mapping247']!=read(sf['control_plan_pin'])['original_return_mapping247']:raise RuntimeError('exact compiled capture Source/Host/report bindings')
    live={p['path']:norm(p)for p in report['fixed_current_pins']+report['output_pins']};current70=[live[x]for x in report['actual_ordered70_link_inputs']]
    if len(current70)!=70 or report['records'][0]['command'][-3:]!=[str(ORIGINAL),'-o',current70[1]['path']]:raise RuntimeError('actual current70 compiled only1 parent')
    modulepin=pin(Path(current70[1]['path']).parent/'spor64_a8.mod')
    if modulepin['size_bytes']!=6092 or modulepin['sha256']!='2d1878cbfbf324af67c2be7980946b26244f9b7d59594abbbb4bad167ccc2203':raise RuntimeError('actual original6092 module ABI parent')
    activepin=sf['original_active_normalization_source_pin'];active=Path(activepin['path']).read_text()
    if pin(activepin['path'])!=activepin:raise RuntimeError('exact active normalized original Source')
    # Derive all29 calls/typed shapes from the original Source rather than mirroring them.
    lines=active.splitlines();scope=None;map29=[]
    for i,line in enumerate(lines):
        m=re.match(r'\s*subroutine\s+(\w+)\(',line,re.I)
        if m:scope=m.group(1)
        if re.match(r'\s*call MAP_',line):
            j=i;parts=[line]
            while parts[-1].rstrip().endswith('&'):j+=1;parts.append(lines[j])
            call=' '.join(x.strip().replace('&','')for x in parts);m=re.fullmatch(r'call (MAP_\w+)\((.*)\)',call);args=[x.strip()for x in m.group(2).split(',')]
            map29.append(dict(scope=scope,call_source_line=i+1,caller_failed_guard_source_line=j+2,original_call_complete='\n'.join(parts),callee=m.group(1),object_expression=args[0],record_name=args[1].strip("'"),shape_expressions=args[2:-2],pointer_variable=args[-2],type_code=2 if m.group(1)=='MAP_REAL321'else 1))
    persistent_lines={434,436,438,541,543,545,547,549,552,582,806,811,878,880,882,884,888,890}
    if len(map29)!=29 or len([r for r in map29 if r['call_source_line']in persistent_lines])!=18:raise RuntimeError('derived original29 and exact18 persistent sites')
    changes=[]
    def splice(label,before,after):
        nonlocal s
        if s.count(before)!=1:raise RuntimeError('one whole Source splice before '+label)
        at=s.index(before);s=s[:at]+after+s[at+len(before):]
        if s.count(after)!=1:raise RuntimeError('one whole Source splice after '+label)
        changes.append(dict(label=label,before=before,after=after,offset_at_application=at,original_before_occurrences=1,candidate_after_occurrences_at_application=1))
    for scope in ('MCCGF64','MCGFL164'):
        a=s.index('  subroutine '+scope+'(');b=s.index('    integer, intent(in)',a)
        old=s[a:b];new=old+'    use GANLIB, only : A8_OWN_LCMGET => LCMGET\n'
        splice(scope+'_local_LCMGET_import',old,new)
    old='    integer, allocatable :: itst(:), matalb_trk(:)\n'
    new=old+'    integer, allocatable, target :: owned_state_vector(:)\n    integer, allocatable, target :: owned_mccg_state(:), owned_icode_trk1(:)\n    integer, allocatable, target :: owned_nzon_trk1(:), owned_keycur_trk1(:)\n    integer, allocatable, target :: owned_keyflx_trk3(:,:,:)\n    real(real32), allocatable, target :: owned_real_param32(:)\n    real(real32), allocatable, target :: owned_wzmu32(:), owned_zmu32(:)\n    real(real32), allocatable, target :: owned_volume_trk32(:)\n'
    splice('MCCGF64_local_owners_only',old,new)
    old='    integer, allocatable :: im0_data(:), mcu0_data(:)\n'
    new='    integer, allocatable, target :: im0_data(:), mcu0_data(:)\n    integer, allocatable, target :: owned_bc_index_trk1(:)\n    integer, allocatable, target :: owned_pjjind_trk2(:,:)\n    integer, allocatable, target :: owned_im(:), owned_mcu(:)\n    integer, allocatable, target :: owned_iperm(:), owned_ju(:)\n'
    splice('MCGFL164_local_owners_and_existing_P3_targets',old,new)
    owned18=[]
    for row in map29:
        if row['call_source_line']not in persistent_lines:continue
        pred='A8_'+row['scope']+'_RETURN_L'+str(row['caller_failed_guard_source_line']).zfill(4);at=s.index("'\"predicate_id\":\""+pred+"\",'// &")
        start=s.rfind('if (.not. map_ok) then',0,at);start=s.rfind('\n',0,start)+1;indent=s[start:s.index('if',start)];end=s.index(indent+'end if\n',at)+len(indent+'end if\n');guard=s[start:end]
        pointer=row['pointer_variable'];owner={'im0_view':'im0_data','mcu0_view':'mcu0_data'}.get(pointer,'owned_'+pointer);shape=','.join(row['shape_expressions'])
        addition=indent+'allocate('+owner+'('+shape+'))\n'+indent+'call A8_OWN_LCMGET('+row['object_expression']+", '"+row['record_name']+"', "+owner+')\n'+indent+pointer+' => '+owner+'\n'
        splice(pred+'_success_owned_read_before_any_next_MAP',guard,guard+addition)
        owned18.append(dict(**row,owner_variable=owner,owner_rank=len(row['shape_expressions']),original_success_guard_predicate_id=pred,new_read_only_after_unchanged_success_guard=True,new_read='LCMGET typed rank'+str(len(row['shape_expressions'])),old_borrowed_pointer_never_read_by_new_code=True,owner_reassociation_before_next_MAP=True,owner_is_caller_local_allocatable_TARGET=True,owner_automatically_released_at_every_return=True,P3_existing_owner_reused=pointer in('im0_view','mcu0_view')))
    splice('P3_remove_duplicate_combined_allocation_preserve_two_original_assignments','      allocate(im0_data(nlong+1),mcu0_data(lc0))\n      im0_data = im0_view\n      mcu0_data = mcu0_view\n','      im0_data = im0_view\n      mcu0_data = mcu0_view\n')
    restored=s
    for c in reversed(changes):
        if restored.count(c['after'])!=1:raise RuntimeError('unique reverse whole Source '+c['label'])
        restored=restored.replace(c['after'],c['before'],1)
    if restored!=original:raise RuntimeError('whole Source reverse differs frozen capture')
    def routine(text,name):
        a=text.index('  subroutine '+name+'(');b=text.index('  end subroutine '+name,a)+len('  end subroutine '+name);return text[a:b]
    for name in ('MAP_INTEGER1','MAP_REAL321','MAP_INTEGER2','MAP_INTEGER3','DOORFV64','MCGFCS64','MCGFLX64','MCGMRE64','SPOR64_A8_MUTABLE_PROBE','SPOR64_A8_CAPTURE_PROBE','SPOR64_A8_RANK_PROBE','SPOR64_A8_OPERATOR_PROBE'):
        if routine(s,name)!=routine(original,name):raise RuntimeError('all other routines and public/private MAP signatures wholebytes '+name)
    if s[:s.index('\ncontains\n')]!=original[:original.index('\ncontains\n')]:raise RuntimeError('module declarations/public ABI Source byte change')
    # The original all247 failure conditions/events and existing442 observer remain byte-identical.
    predicates=sf['original_return_mapping247']
    for row in predicates:
        token='\"predicate_id\":\"'+row['predicate_id']+'\"'
        if s.count(token)!=1 or original.count(token)!=1:raise RuntimeError('all247 event IDs once')
    capture_start=original.index('      block\n        use GANLIB, only : A8_DIAG_LCMINF');capture_end=original.index('      end block\n',capture_start)+len('      end block\n');capture=original[capture_start:capture_end]
    if s.count(capture)!=1:raise RuntimeError('original failure-only442 snapshot full block bytes changed')
    immediate_specs={530:(533,'cpo32 = cpo_view32'),584:(586,'all(ieee_is_finite(albedo_trk32))'),600:(603,'all(ieee_is_finite(group_albedo32))'),605:(608,'all(ieee_is_finite(txsc_record32))'),609:(612,'sc_by_group32(:,1,i) = sc_record32'),906:(908,'diagq32(:,i) = record32'),909:(911,'cq32(:,i) = record32'),912:(914,'iludf32(:,i) = record32'),916:(918,'ilucf32(:,i) = record32'),920:(922,'cf32(:,i) = record32'),923:(925,'diagf32(:,i) = record32')}
    lifecycle29=[]
    for row in map29:
        proof=dict(row)
        if row['call_source_line']in persistent_lines:
            own=next(x for x in owned18 if x['call_source_line']==row['call_source_line']);proof.update(role='caller_owned_persistent',owner_variable=own['owner_variable'],ownership_before_next_MAP_required=True,ownership_added_at_original_success_guard=True)
        else:
            use_line,use=immediate_specs[row['call_source_line']];proof.update(role='original_immediate_consume_or_existing_owned_copy',original_consume_source_line=use_line,original_consume_statement=lines[use_line-1],consume_kind='owned_array_copy'if' = 'in use else'finite_check_then_no_later_view_read',borrow_not_used_after_next_GPD=True,original_consume_statement_bytes_unchanged=s.count(lines[use_line-1])==original.count(lines[use_line-1]))
            if not proof['original_consume_statement_bytes_unchanged']:raise RuntimeError('original11 immediate consume bytes')
        lifecycle29.append(proof)
    P.mkdir();src=P/'SPOR64_A8.f90';write(src,s);iv=P/'COMPLETE_CAPTURE_TO_A8_18_CALLER_OWNED_MAP_LIFETIME_WHOLE_BYTE_INVERSE.json'
    flags=dict(whole_file_inverse_byte_equal=True,only18_original_successful_MAP_callers_owned_storage_and_reads_added=True,all_original247_failed_conditions_events_returns_and_failure_snapshot_wholebytes_unchanged=True,all_original_module_declarations_public_ABI_MAP_signatures_math_scalar_assignments_loops_thresholds_and_original_IO_order_unchanged=True,all11_original_immediate_consume_or_copy_sequences_wholebytes_unchanged=True,no_new_SAVE_moduleglobal_owner_or_public_API_or_new_early_return=True,all18_owners_local_automatic_release_on_every_return=True,P3_IM0_owned_before_MCU0_existing_owner_arrays_no_duplicate_allocation=True,typed_LCMGET_owned_rank_and_raw_word_order_no_real_kind_conversion=True)
    write(iv,dict(schema='COMPLETE_CAPTURE_TO_A8_18_CALLER_OWNED_MAP_LIFETIME_WHOLE_BYTE_INVERSE_V1',original_source_pin=original_pin,candidate_source_pin=pin(src),original_complete_UTF8=original,changes=changes,all29_original_MAP_site_lifecycle_proof=lifecycle29,exact18_owned_site_mapping=owned18,Source_flags=flags,source_only=True,compiler_executed=False,numerical_executed=False,business_executed=False,files_deleted=False))
    plan=P/'SOURCE_ONLY_A8_18_CALLER_OWNED_MAP_LIFETIME_PLAN.json'
    api_pins=sf['actual_API_Source_pins'];api_more=[pin(Path('/Users/wen/spot/Ganlib/src/lcmmod.f90')),pin(Path('/Users/wen/spot/Ganlib/src/ganlib.f90'))]
    write(plan,dict(schema='SOURCE_ONLY_A8_18_CALLER_OWNED_PERSISTENT_MAP_LIFETIME_PLAN_V1',source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,original_source_pin=original_pin,diagnostic_source_pin=pin(src),complete_byte_inverse_pin=pin(iv),Source_preparer_pin=pin(__file__),selected_capture_Fortran_Source_freeze_pin=sfpin,actual_capture_Host_freeze_pin=hfpin,actual_capture_report_pin=reportpin,actual_capture_Root_true_tool_pin=rootpin,actual_capture_Root_argv_pin=argvpin,actual_capture_value_snapshot=snapshot,actual_capture_inference='old borrowed STATE4/5 differ from owned persisted STATE4/5 in actual XSM; neither overwrite nor freed-buffer mechanism is individually measured',actual_capture_claim_does_not_admit_geometry443_solver_core_or_physics=True,actual_capture_log_pin=outcome['actual_log_pin'],actual_capture_watchdog_pin=outcome['actual_watchdog_pin'],original_return_mapping247=predicates,exact18_owned_site_mapping=owned18,all29_original_MAP_site_lifecycle_proof=lifecycle29,original11_immediate_consume_copy_site_count=11,caller_owned_site_count=18,new_owner_array_count16=16,P3_existing_owner_array_count=2,original_module_pin=modulepin,original_module6092_wholebyte_equality_required=True,current_actual_ordered70_pins=current70,replacement_zero_based_link_index=1,all_other69_A9actual2_Native47_BOOTB49_BOXX68_Driver37_BOOTQ40_math57_archives_unchanged_required=True,actual_API_Source_pins=api_pins+api_more,selected_actual_Ganlib_archive_pin=sf['selected_actual_Ganlib_archive_pin'],selected_actual_Dragon_archive_pin=sf['selected_actual_Dragon_archive_pin'],owned_record_bits_are_typed_original32bit_words_without_conversion=True,owned_resource_bound=dict(bytes_per_original_integer_or_REAL32_word=4,MCCGF_new_owned_word_bound='90 + 2*nmu + 3*nlong',MCGFL164_new_owned_word_bound='4*nlong - nreg + lc + 3',combined_extra_payload_byte_bound='4*(93 + 2*nmu + 7*nlong - nreg + lc)',original_guarded_nmu=4,combined_original_nmu4_extra_payload_byte_bound='4*(101 + 7*nlong - nreg + lc)',P3_original_existing_owned_payload_bytes='4*(nlong+1+lc0)',P3_additional_copy_count=0,all_scope_local_owners_released_on_original_return=True,source_formula_is_not_actual_RSS_or_next_budget_admission=True,allocation_runtime_overhead_not_assumed_zero=True),future_owner_raw_bit_controls_plan=dict(actual_control_Source_pin=None,actual_compiler_object_pin=None,actual_executable_pin=None,actual_result_pin=None,actual_root_terminal_pin=None,cases=['XSM and linked-list typed I1/R1/I2/I3 exactshape owned rawword bits','40→40→4 XSM outputslot reuse never dereference old freed view','P3 IM0 owned before MCU0; existing arrays only one allocation each','all18 successful typed guards preserve32bit recordwords including REAL32 signedzero/finite','all_original malformed record shape/type guards and247 failure event identities remain strict','local owner allocations release at both original okFalse and okTrue returns'],actual_pass_count=None),future_actual_Source_freeze_pin=None,future_actual_Host_freeze_pin=None,future_actual_cleanup_proof_pins=None,future_actual_object_pin=None,future_actual_mod_pin=None,future_actual_Dragon_pin=None,future_actual_BOOT_report_pin=None,future_actual_owner_bit_control_results=None,engineering_qualified=False,physics_qualified=False,Source_flags=flags))
    ready=P/'READY.json';write(ready,dict(status='SOURCE_ONLY_A8_18_CALLER_OWNED_MAP_LIFETIME_CANDIDATE_READY_FOR_SAME_ROUND_REVIEW',failure=None,source_pin=pin(src),inverse_pin=pin(iv),plan_pin=pin(plan),Source_preparer_pin=pin(__file__),source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False,original_module6092_wholebyte_equality_required=True,only_slot1_recompiled_in_future=True,other69_current_inputs_unchanged_required=True,caller_owned_site_count=18,original_MAP_site_count=29,actual_owner_bit_control_results=None,actual_object_pin=None,actual_mod_pin=None,actual_executable_pin=None,actual_runtime_report_pin=None,engineering_qualified=False,physics_qualified=False))
    fd=os.open(P,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
    try:os.fsync(fd)
    finally:os.close(fd)
    print(json.dumps(dict(status='SOURCE_ONLY_A8_18_OWNED_PERSISTENT_MAP_LIFETIME_READY_NO_COMPILER_OR_BUSINESS',source_pin=pin(src),inverse_pin=pin(iv),plan_pin=pin(plan),ready_pin=pin(ready),Source_preparer_pin=pin(__file__),whole_Source_inverse_equal=True,caller_owned_site_count=18,all_original_MAP_site_count=29,source_only=True,compiled=False,numerical_executed=False,business_executed=False,files_deleted=False)))
if __name__=='__main__':main()
