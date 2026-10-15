"""Source text for the sole public7 completed SRC retirement admission.

This file is read as text by the Source preparer. It does not import or run a
pipeline, control, compiler, or retirement operation.
"""

def exact_public_pin(row,path):
    if not isinstance(row,dict)or set(row)!={'path','sha256','size_bytes','identity'}or row['path']!=str(path):
        raise RuntimeError('exact public stale fullpin path and four fields')
    identity=row['identity']
    if not isinstance(identity,list)or len(identity)!=7 or any(type(x)is not int for x in identity)or \
       not stat.S_ISREG(identity[2])or identity[3]!=1 or type(row['size_bytes'])is not int or \
       row['size_bytes']<=0 or identity[4]!=row['size_bytes']or \
       not isinstance(row['sha256'],str)or len(row['sha256'])!=64 or \
       any(x not in '0123456789abcdef'for x in row['sha256']):
        raise RuntimeError('ordinary singlelink exact public stale historical/current fullpin')
    return row

def exact_public_live_pin(report,row,path):
    exact_public_pin(row,path)
    for key in ('output_pins','owned_runtime_pins'):
        if sum(x==row for x in report[key])!=1 or any(x['path']==str(path)and x!=row for x in report[key]):
            raise RuntimeError('exact current public stale file belongs to own output/owned closure')
    c.same_pin(path,row)
    return row

def exact_public_nulls(document,keys):
    if any(key not in document or document[key]is not None for key in keys):
        raise RuntimeError('explicit null public historical/failure/future fields required')

def admit_exact_public_stale_lifetimes(hf,own,plan,report,root,exe):
    stale=report['actual_stale_host_evidence']
    if len(stale)!=2 or {x['case']for x in stale}!={'public_read_stale_BQ_SRC','public_read_stale_BQ_MAC'}:
        raise RuntimeError('exact two independent stale private stage refusals')
    life_pin=own.get('selected_completed_first_SRC_bundle_lifetime_Source_plan_pin')
    if life_pin!=selected_pin(hf,'selected_completed_first_SRC_bundle_lifetime_Source_plan_pin')or \
       plan.get('completed_first_SRC_bundle_lifetime_Source_plan_pin')!=life_pin or \
       any(own.get(k)is not True for k in ('exact_completed_first_SRC_bundle_retirement_scope_only',
          'retired_bundle_is_historical_not_current_no_generic_missing_skip',
          'original_Fortran_math_7controls_9phases_11commands_unchanged')):
        raise RuntimeError('exact frozen first completed SRC lifetime authority')
    for rows in (own['dependencies'],report['fixed_current_pins']):
        if current_pin_table(rows).get(life_pin['path'])!=life_pin:
            raise RuntimeError('public ownHF and actualreport fixed lifetime Source plan')
    life,checked=c.read_bound_json_current(life_pin['path'],life_pin)
    if checked!=life_pin or life.get('schema')!='EXACT_PUBLIC_READ_FIRST_COMPLETED_SRC_BUNDLE_LIFETIME_SOURCE_PLAN_V1'or \
       life.get('source_only')is not True or life.get('exact_retirement_case')!='public_read_stale_BQ_SRC'or \
       life.get('exact_bundle_relative_path')!='public_read_stale_BQ_SRC/coherent_complete_context.xsm'or \
       life.get('unchanged_Fortran_Source_pin')!=report['actual_control_Source_pin']or \
       life.get('unchanged_public_Fortran_Source_freeze_pin')!=report['actual_Source_freeze_pin']or \
       any(type(life.get(k))is not int or life[k]!=v for k,v in (
          ('logical_controls',7),('phases',9),('total_guarded_stages',11),
          ('exact_expected_read_status',1),('exact_expected_control_calls',1),('exact_expected_baseline_calls',0),
          ('maximum_live_synthetic_context_bundles',1),('original_aux_bytes',128*MI),('pending_bytes',8*MI)))or \
       any(life.get(k)is not True for k in (
          'fsynced_intent_before_single_attempt','intent_parent_entry_fsync_before_unlink',
          'exact_APFS_creation_delta_nlink_plus1_size_plus32_and_times_monotonic',
          'owned_directory_fd_NOFOLLOW_UID_singlelink_full_identity',
          'only_exact_new_owned_completed_SRC_bundle_unlink_authorized',
          'truthful_attempted_returned_unlink_parent_fsync_receipt_before_close_or_any_after_check',
          'receipt_and_intent_retained_as_current_owned_metadata','only_retired_bundle_removed_from_current_owned_PFs',
          'original_before_and_after_completed_read_PFs_retained_as_historical_time_facts',
          'original_manifest_sentinel_both_logs_current_and_unchanged','second_MAC_bundle_retained_current_through_final_report',
          'no_sparse_compression_move_threshold_or_generic_missing_skip','no_retries','old_v5_output_unmodified',
          'Fortran_math_old17_phase_oracle_flags_firsterror_unchanged',
          'downstream_v15_only_SRC_exact_completed_retirement_proof_admission_required'))or \
       any(life.get(k)is not False for k in ('compiler_executed','numerical_executed','reader_qualified')):
        raise RuntimeError('original public lifetime Source plan without future success claims')
    exact_public_nulls(life,('future_actual_retirement_receipt_pin','future_actual_public7_report_pin'))
    retirements=report.get('actual_completed_bundle_retirements')
    if not isinstance(retirements,list)or len(retirements)!=1:
        raise RuntimeError('one genuine completed first SRC retirement event')
    for evidence in stale:
        name=evidence['case'];cwd=root/name
        before=exact_public_live_pin(report,evidence['actual_before_manifest_pin'],cwd/'Host_independent_stale_before_full_EOF_SHA_all7.json')
        value,checked=c.read_bound_json_current(before['path'],before)
        prepare_record=next(x for x in report['records']if x['command']==[exe,name,'prepare'])
        read_record=next(x for x in report['records']if x['command']==[exe,name,'read'])
        read_oracle=next(x for x in report['actual_control_results']if (x['case'],x['phase'])==(name,'read'))
        if prepare_record['status']!='PASS'or read_record['status']!='PASS'or \
           value.get('schema')!='ACTUAL_PUBLIC_READ_STALE_BEFORE_FULL_EOF_SHA_ALL7_V1'or value.get('case')!=name or \
           value.get('other_BQ_absent')is not True or value.get('genuine_prepare_child_closed0')is not True or \
           value.get('actual_prepare_record')!=prepare_record or evidence.get('actual_read_record')!=read_record:
            raise RuntimeError('two-phase stale baseline binds genuine completed prepare/read records')
        bundle=exact_public_pin(evidence['actual_bundle_before_pin'],cwd/'coherent_complete_context.xsm')
        selected='BQ64-SRC-ST'if name=='public_read_stale_BQ_SRC'else'BQ64-MAC-ST'
        sentinel=exact_public_live_pin(report,evidence['actual_stale_after_pin'],cwd/selected)
        if checked!=before or value['actual_bundle_pin']!=bundle or value['actual_stale_pin']!=evidence['actual_stale_before_pin']or \
           bundle!=evidence['actual_bundle_after_pin']or evidence['actual_stale_before_pin']!=sentinel or \
           any(evidence.get(k)is not True for k in ('actual_two_files_full_EOF_SHA_all7_unchanged',
              'actual_other_BQ_absent','genuine_read_child_closed0')):
            raise RuntimeError('real same-file fullEOF stale before/after facts remain unchanged')
        terminal=read_oracle['actual_terminal']
        if any(type(terminal.get(k))is not int or terminal[k]!=v for k,v in (
           ('actual_public_read_status',1),('actual_control_public_read_calls',1),('actual_baseline_public_read_calls',0))):
            raise RuntimeError('genuine public stale READ status/call-count oracle')
        other=cwd/('BQ64-MAC-ST'if name=='public_read_stale_BQ_SRC'else'BQ64-SRC-ST')
        if other.exists()or other.is_symlink():raise RuntimeError('other stale BQ stage remains absent')
        if name=='public_read_stale_BQ_MAC':
            if evidence.get('bundle_lifetime_status')!='CURRENT_RETAINED_AFTER_COMPLETED_READ'or \
               evidence.get('current_bundle_pin')!=bundle or 'actual_completed_bundle_retirement'in evidence:
                raise RuntimeError('second MAC complete fixture remains current and unretired')
            exact_public_live_pin(report,bundle,cwd/'coherent_complete_context.xsm')
            continue
        event=retirements[0]
        exact_public_nulls(evidence,('current_bundle_pin',))
        exact_public_nulls(event,('current_bundle_pin','post_receipt_failure'))
        if evidence.get('bundle_lifetime_status')!='RETIRED_AFTER_COMPLETED_READ_BEFORE_SECOND_PREPARE'or \
           evidence.get('current_bundle_pin')is not None or evidence.get('actual_completed_bundle_retirement')!=event or \
           event.get('case')!=name or event.get('historical_bundle_before_pin')!=bundle or \
           event.get('historical_bundle_after_completed_read_pin')!=bundle or event.get('retirement_completed')is not True or \
           event.get('current_bundle_pin')is not None or event.get('post_receipt_failure')is not None or \
           event.get('secondary_operation_failures')!=[]:
            raise RuntimeError('sole SRC retirement event equals original completed READ evidence')
        for rows in (hf['dependencies'],own['dependencies'],report['fixed_current_pins'],report['output_pins'],report['owned_runtime_pins']):
            if any(x['path']==bundle['path']or x['identity'][:2]==bundle['identity'][:2]for x in rows):
                raise RuntimeError('retired exact SRC bundle has no current path or physical alias')
        if Path(bundle['path']).exists()or Path(bundle['path']).is_symlink():
            raise RuntimeError('only exact completed SRC bundle is absent')
        intent_pin=exact_public_live_pin(report,event['intent_pin'],cwd/'Host_completed_SRC_bundle_retirement_intent.json')
        receipt_pin=exact_public_live_pin(report,event['receipt_pin'],cwd/'Host_completed_SRC_bundle_retirement_receipt.json')
        intent,checked_intent=c.read_bound_json_current(intent_pin['path'],intent_pin)
        receipt,checked_receipt=c.read_bound_json_current(receipt_pin['path'],receipt_pin)
        exact_public_nulls(receipt,('current_bundle_pin','primary_operation_failure'))
        if checked_intent!=intent_pin or checked_receipt!=receipt_pin or receipt!=event['operation']or \
           intent.get('schema')!='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_INTENT_V1'or \
           receipt.get('schema')!='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_RECEIPT_V1'or \
           intent.get('case')!=name or receipt.get('case')!=name or receipt.get('actual_intent_pin')!=intent_pin:
            raise RuntimeError('actual fullEOF intent and returned receipt exactly match sole event')
        for document in (intent,receipt):
            if document.get('actual_before_manifest_pin')!=before or document.get('actual_stale_before_fullpin')!=sentinel or \
               document.get('actual_stale_after_fullpin')!=sentinel or document.get('actual_prepare_record')!=prepare_record or \
               document.get('actual_completed_read_record')!=read_record or document.get('actual_read_oracle')!=read_oracle or \
               any(document.get(k)is not True for k in ('other_BQ_absent','actual_before_equals_after_full_SHA_all7',
                  'no_retry','no_old_v5_file_targeted'))or document.get('physics_qualified')is not False or \
               type(document.get('target_uid'))is not int or document['target_uid']!=os.getuid():
                raise RuntimeError('strict intent/receipt bind original completed native records, fullpins and UID')
        if intent.get('exact_bundle_fullpin')!=bundle or intent.get('actual_bundle_after_completed_READ_fullpin')!=bundle or \
           intent.get('target_single_link_required')is not True or type(intent.get('current_owned_target_count'))is not int or \
           intent['current_owned_target_count']!=1 or intent.get('only_this_exact_bundle_may_be_unlinked')is not True or \
           receipt.get('exact_retired_bundle_fullpin')!=bundle or receipt.get('historical_completed_read_after_fullpin')!=bundle or \
           type(receipt.get('actual_retired_count'))is not int or receipt['actual_retired_count']!=1 or \
           receipt.get('current_bundle_pin')is not None or receipt.get('primary_operation_failure')is not None or \
           receipt.get('secondary_operation_failures')!=[]or \
           any(receipt.get(k)is not True for k in ('intent_parent_fsync_attempted','intent_parent_fsync_returned',
              'unlink_attempted','unlink_returned','parent_fsync_attempted','parent_fsync_returned',
              'target_absent_observed','removed_current_owned_fullpin','retirement_completed','retired_bundle_historical_only',
              'receipt_written_before_directory_close_and_any_later_check','directory_close_not_claimed_by_receipt')):
            raise RuntimeError('truthful sole completed unlink and both returned directory fsyncs, no failure/retry')
        before_intent=intent.get('parent_before_intent_identity');before_parent=receipt.get('parent_before_identity')
        after_parent=receipt.get('parent_after_identity')
        for identity in (before_intent,before_parent,after_parent):
            if not isinstance(identity,list)or len(identity)!=7 or any(type(x)is not int for x in identity)or not stat.S_ISDIR(identity[2]):
                raise RuntimeError('exact seven integer owned directory time-fact identities')
        if receipt.get('parent_before_intent_identity')!=before_intent or before_parent[:3]!=before_intent[:3]or \
           before_parent[3]!=before_intent[3]+1 or before_parent[4]!=before_intent[4]+32 or \
           before_parent[5]<before_intent[5]or before_parent[6]<before_intent[6]or \
           after_parent[:3]!=before_parent[:3]or after_parent[3]!=before_parent[3]-1 or \
           after_parent[4]!=before_parent[4]-32 or after_parent[5]<before_parent[5]or after_parent[6]<before_parent[6]:
            raise RuntimeError('exact APFS intent creation and sole unlink directory time-fact deltas')
        parent=cwd.lstat()
        if cwd.is_symlink()or not stat.S_ISDIR(parent.st_mode)or parent.st_uid!=os.getuid()or \
           [parent.st_dev,parent.st_ino,parent.st_mode]!=after_parent[:3]or \
           parent.st_nlink!=after_parent[3]+1 or parent.st_size!=after_parent[4]+32 or \
           parent.st_mtime_ns<after_parent[5]or parent.st_ctime_ns<after_parent[6]:
            raise RuntimeError('same owned SRC directory after sole retained receipt entry creation')
    return dict(sole_completed_SRC_bundle_retirement_admitted=True,retired_bundle_is_historical_only=True,
      MAC_bundle_retained_current=True,actual_completed_bundle_retirement=retirements[0],physics_qualified=False)
