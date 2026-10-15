# The sole lifetime retirement is the completed first SRC synthetic bundle.
# All primitive controls, both native read phases, statuses and raw checks stay original.
def retire_completed_first_SRC_bundle(c,cwd,state,read_record,read_oracle,owned,fixed,retirements):
    if KIND!='public' or cwd!=OUT/'public_read_stale_BQ_SRC' or retirements:
        raise RuntimeError('one exact first SRC synthetic bundle retirement only')
    bundle=cwd/'coherent_complete_context.xsm';sentinel=cwd/'BQ64-SRC-ST';other=cwd/'BQ64-MAC-ST'
    before=state['bundle_pin'];stale=state['stale_pin'];mf=state['manifest_pin']
    prepare=state['actual_prepare_record']
    if before['path']!=str(bundle) or stale['path']!=str(sentinel) or \
       prepare['status']!='PASS' or read_record['status']!='PASS' or \
       prepare['command'][-2:]!=['public_read_stale_BQ_SRC','prepare'] or \
       read_record['command'][-2:]!=['public_read_stale_BQ_SRC','read'] or \
       (read_oracle['case'],read_oracle['phase'])!=('public_read_stale_BQ_SRC','read'):
        raise RuntimeError('genuine completed SRC prepare/read and exact bundle path')
    expected=read_oracle['actual_terminal']
    for key,value in [('actual_public_read_status',1),('actual_control_public_read_calls',1),('actual_baseline_public_read_calls',0)]:
        if type(expected.get(key))is not int or expected[key]!=value:
            raise RuntimeError('strict genuine completed SRC READ refusal oracle before retirement')
    c.verify_rows([mf,before,stale])
    value,checked=c.read_bound_json_current(mf['path'],mf)
    if checked!=mf or value['actual_bundle_pin']!=before or value['actual_stale_pin']!=stale or \
       value.get('genuine_prepare_child_closed0')is not True or value['actual_prepare_record']!=prepare or \
       other.exists() or other.is_symlink():
        raise RuntimeError('immutable exact SRC before manifest/sentinel and other BQ absent')
    after=c.pin(bundle);after_stale=c.pin(sentinel)
    if after!=before or after_stale!=stale or before['identity'][3]!=1 or \
       not stat.S_ISREG(before['identity'][2]) or bundle.is_symlink() or \
       sum(row==before for row in owned)!=1 or \
       any(row['identity'][:2]==before['identity'][:2]for row in fixed) or \
       any(row['path']!=before['path']and row['identity'][:2]==before['identity'][:2]for row in owned):
        raise RuntimeError('completed SRC full EOF/all7 stable exclusive owned ordinary single-link bundle')
    def seven(s):return[s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
    parent=cwd.lstat()
    if not stat.S_ISDIR(parent.st_mode) or cwd.is_symlink() or parent.st_uid!=os.getuid():
        raise RuntimeError('exact owned non-symlink SRC parent directory')
    parent_before_intent=seven(parent);uid=os.getuid()
    intent_path=cwd/'Host_completed_SRC_bundle_retirement_intent.json'
    receipt_path=cwd/'Host_completed_SRC_bundle_retirement_receipt.json'
    intent=dict(schema='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_INTENT_V1',case='public_read_stale_BQ_SRC',
      exact_bundle_fullpin=before,actual_bundle_after_completed_READ_fullpin=after,
      actual_stale_before_fullpin=stale,actual_stale_after_fullpin=after_stale,actual_before_manifest_pin=mf,
      actual_prepare_record=prepare,actual_completed_read_record=read_record,actual_read_oracle=read_oracle,
      other_BQ_absent=True,actual_before_equals_after_full_SHA_all7=True,
      target_uid=uid,target_single_link_required=True,parent_before_intent_identity=parent_before_intent,
      current_owned_target_count=1,only_this_exact_bundle_may_be_unlinked=True,
      no_retry=True,no_old_v5_file_targeted=True,physics_qualified=False)
    c.write(intent_path,intent);intent_pin=c.pin(intent_path);owned.append(intent_pin)
    parent_now=cwd.lstat();parent_before=seven(parent_now)
    if parent_before[:4]!=parent_before_intent[:4] or parent_now.st_uid!=uid or cwd.is_symlink():
        raise RuntimeError('same owned SRC parent after fsynced retirement intent creation')
    attempted=dict(schema='EXACT_COMPLETED_FIRST_SRC_BUNDLE_RETIREMENT_RECEIPT_V1',case='public_read_stale_BQ_SRC',
      actual_intent_pin=intent_pin,exact_retired_bundle_fullpin=before,
      historical_completed_read_after_fullpin=after,actual_before_manifest_pin=mf,
      actual_stale_before_fullpin=stale,actual_stale_after_fullpin=after_stale,
      actual_prepare_record=prepare,actual_completed_read_record=read_record,
      actual_read_oracle=read_oracle,parent_before_identity=parent_before,
      parent_before_intent_identity=parent_before_intent,target_uid=uid,
      actual_before_equals_after_full_SHA_all7=True,other_BQ_absent=True,
      unlink_attempted=False,unlink_returned=False,parent_fsync_attempted=False,parent_fsync_returned=False,
      target_absent_observed=False,removed_current_owned_fullpin=False,actual_retired_count=0,
      retirement_completed=False,current_bundle_pin=before,retired_bundle_historical_only=False,
      no_retry=True,no_old_v5_file_targeted=True,physics_qualified=False,
      primary_operation_failure=None,secondary_operation_failures=[],
      receipt_written_before_directory_close_and_any_later_check=True,directory_close_not_claimed_by_receipt=True)
    event=dict(case='public_read_stale_BQ_SRC',intent_pin=intent_pin,receipt_pin=None,
      historical_bundle_before_pin=before,historical_bundle_after_completed_read_pin=after,
      operation=attempted,retirement_completed=False,current_bundle_pin=before)
    retirements.append(event)  # one truthful attempt, including failures; never replayed
    local=FirstFailure();fd=None
    try:
        fd=os.open(cwd,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        if seven(os.fstat(fd))!=parent_before or os.fstat(fd).st_uid!=uid:
            raise RuntimeError('same owned parent dirfd before exact leaf retirement')
        leaf=os.stat(bundle.name,dir_fd=fd,follow_symlinks=False)
        if seven(leaf)!=before['identity'] or leaf.st_uid!=uid or leaf.st_nlink!=1 or not stat.S_ISREG(leaf.st_mode):
            raise RuntimeError('same exact owned fullpin/UID/singlelink leaf before unlink')
        c.same_pin(bundle,before)
        leaf=os.stat(bundle.name,dir_fd=fd,follow_symlinks=False)
        if seven(leaf)!=before['identity'] or leaf.st_uid!=uid:
            raise RuntimeError('stable exact leaf after complete EOF before single unlink')
        attempted['unlink_attempted']=True
        os.unlink(bundle.name,dir_fd=fd)
        attempted['unlink_returned']=True
        attempted['current_bundle_pin']=None;attempted['retired_bundle_historical_only']=True
        event['current_bundle_pin']=None
        owned.remove(before)
        attempted['removed_current_owned_fullpin']=True;attempted['actual_retired_count']=1
        attempted['parent_fsync_attempted']=True
        os.fsync(fd);attempted['parent_fsync_returned']=True
        try:os.stat(bundle.name,dir_fd=fd,follow_symlinks=False)
        except FileNotFoundError:attempted['target_absent_observed']=True
        if not attempted['target_absent_observed']:raise RuntimeError('retired exact SRC bundle must remain absent')
        attempted['parent_after_identity']=seven(os.fstat(fd))
        attempted['retirement_completed']=True
        event['retirement_completed']=True
    except BaseException as error:local.capture(error,'exact_retirement_operation')
    attempted['primary_operation_failure']=None if local.error is None else safe_repr(local.error)
    attempted['secondary_operation_failures']=list(local.secondary)
    # Persist truthful attempted/returned flags before close or any subsequent resource check.
    try:
        c.write(receipt_path,attempted)
        receipt_pin=c.pin(receipt_path);owned.append(receipt_pin);event['receipt_pin']=receipt_pin
    except BaseException as error:local.capture(error,'retirement_receipt_publication')
    if fd is not None:
        try:os.close(fd)
        except BaseException as error:local.capture(error,'retirement_directory_close')
    event['post_receipt_failure']=None if local.error is None else safe_repr(local.error)
    event['secondary_operation_failures']=list(local.secondary)
    local.reraise()
    if not event['retirement_completed'] or event['receipt_pin']is None:
        raise RuntimeError('only exact completed SRC retirement permits the next synthetic bundle')
    c.verify_rows([mf,stale,intent_pin,event['receipt_pin']])
    if bundle.exists()or bundle.is_symlink()or other.exists()or other.is_symlink():
        raise RuntimeError('only completed first SRC bundle absent; opposite stage absent')
    return event
