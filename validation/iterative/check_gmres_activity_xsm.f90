program check_gmres_activity_xsm
  ! Independent, read-only closure of the SPOT GMRES activity ledger.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32
  implicit none

  integer, parameter :: ng=370
  integer, parameter :: nu=14
  integer, parameter :: ntrack_state=40
  integer, parameter :: naudit_state=24
  integer, parameter :: nrole=3
  integer, parameter :: nkbin=11
  integer, parameter :: max_path=72
  integer, parameter :: max_records=64
  integer, parameter :: max_events=20
  integer, parameter :: max_blocks=19
  integer, parameter :: max_global_iter=19
  integer(int32), parameter :: epsi_bits=int(z'3727C5AC',int32)

  type :: ledger_data
    integer :: state(naudit_state)=0
    integer :: ngind(ng)=0
    integer :: role_calls(nrole)=0
    integer :: role_groups(nrole)=0
    integer :: histogram(nkbin)=0
    integer, allocatable :: call_meta(:)
    integer, allocatable :: role_events(:)
    integer, allocatable :: role_active(:)
    integer, allocatable :: block_meta(:)
    integer, allocatable :: block_active(:)
    integer, allocatable :: block_kmax(:)
  end type ledger_data

  character(len=1024) :: track_path,flux_path
  type(ledger_data) :: ledger
  integer :: nonzero_k,sum_k,max_k
  character(len=36) :: classification

  if (command_argument_count() /= 2) &
    call fail('expected TRACK ACTIVITY-XSM')
  call get_command_argument(1,track_path)
  call get_command_argument(2,flux_path)
  if ((len_trim(track_path) == 0).or.(len_trim(flux_path) == 0)) &
    call fail('empty argument')
  if ((len_trim(track_path) > max_path).or. &
      (len_trim(flux_path) > max_path)) &
    call fail('XSM path exceeds Ganlib limit')
  if (trim(track_path) == trim(flux_path)) &
    call fail('XSM paths must be distinct')

  call check_track(trim(track_path))
  call load_ledger(trim(flux_path),ledger)
  call close_ledger(ledger,nonzero_k,sum_k,max_k)
  if (nonzero_k == 0) then
    classification='VALID-GMRES-UPDATE-INACTIVE'
  else
    classification='VALID-GMRES-UPDATE-ACTIVE'
  endif
  call print_ledger(ledger,nonzero_k,sum_k,max_k,trim(classification))

contains

  subroutine check_track(path)
    character(len=*), intent(in) :: path
    type(c_ptr) :: root
    character(len=12) :: track_type
    integer :: mccg_state(ntrack_state)
    real(real32) :: real_param(4)
    integer(int32) :: stored_bits

    call LCMOP(root,path,2,2,0)
    call require_signature(root,'L_TRACK','TRACK')
    call require_record(root,'TRACK-TYPE',3,3,'TRACK')
    call LCMGTC(root,'TRACK-TYPE',12,track_type)
    if (trim(track_type) /= 'MCCG') call fail('TRACK is not MCCG')
    call require_record(root,'MCCG-STATE',ntrack_state,1,'TRACK')
    call require_record(root,'REAL-PARAM',4,2,'TRACK')
    call LCMGET(root,'MCCG-STATE',mccg_state)
    call LCMGET(root,'REAL-PARAM',real_param)
    stored_bits=transfer(real_param(1),0_int32)
    if (mccg_state(13) /= 20) call fail('TRACK MAXI differs')
    if (mccg_state(3) /= 10) call fail('TRACK NSTART differs')
    if (stored_bits /= epsi_bits) call fail('TRACK ERRTOL bits differ')
    call LCMCL(root,1)
  end subroutine check_track


  subroutine load_ledger(path,data)
    character(len=*), intent(in) :: path
    type(ledger_data), intent(out) :: data
    type(c_ptr) :: root,audit
    integer :: entries,total_events,blocks
    integer :: i

    call LCMOP(root,path,2,2,0)
    call require_signature(root,'L_FLUX','ACTIVITY')
    call require_record(root,'SPOT-GMR-AUD',-1,0,'ACTIVITY')
    audit=LCMGID(root,'SPOT-GMR-AUD')
    call require_record(audit,'STATE-VECTOR',naudit_state,1, &
      'AUDIT ROOT')
    call LCMGET(audit,'STATE-VECTOR',data%state)
    call check_static_state(data%state)

    entries=data%state(9)
    blocks=data%state(17)
    if (any(data%state(11:13) < 0)) call fail('negative role count')
    if (any(data%state(14:16) < 0)) &
      call fail('negative role active-group sum')
    if ((blocks < 0).or.(blocks > max_blocks)) &
      call fail('correction-block count outside checker bound')
    total_events=sum(data%state(11:13))
    if ((total_events < 0).or.(total_events > max_events)) &
      call fail('role-event count outside checker bound')

    call require_audit_names(audit,total_events,blocks)
    call require_record(audit,'NGIND',ng,1,'AUDIT ROOT')
    call require_record(audit,'CALL-META',5*entries,1,'AUDIT ROOT')
    call require_record(audit,'ROLE-CALLS',nrole,1,'AUDIT ROOT')
    call require_record(audit,'ROLE-GROUPS',nrole,1,'AUDIT ROOT')
    call require_record(audit,'K-HISTOGRAM',nkbin,1,'AUDIT ROOT')
    allocate(data%call_meta(5*entries))
    call LCMGET(audit,'NGIND',data%ngind)
    call LCMGET(audit,'CALL-META',data%call_meta)
    call LCMGET(audit,'ROLE-CALLS',data%role_calls)
    call LCMGET(audit,'ROLE-GROUPS',data%role_groups)
    call LCMGET(audit,'K-HISTOGRAM',data%histogram)
    do i=1,ng
      if (data%ngind(i) /= i) call fail('NGIND differs')
    enddo

    if (total_events == 0) then
      call require_absent(audit,'ROLE-EVENTS','AUDIT ROOT')
      call require_absent(audit,'ROLE-ACTIVE','AUDIT ROOT')
      allocate(data%role_events(0),data%role_active(0))
    else
      call require_record(audit,'ROLE-EVENTS',6*total_events,1, &
        'AUDIT ROOT')
      call require_record(audit,'ROLE-ACTIVE',ng*total_events,1, &
        'AUDIT ROOT')
      allocate(data%role_events(6*total_events))
      allocate(data%role_active(ng*total_events))
      call LCMGET(audit,'ROLE-EVENTS',data%role_events)
      call LCMGET(audit,'ROLE-ACTIVE',data%role_active)
    endif

    if (blocks == 0) then
      call require_absent(audit,'BLOCK-META','AUDIT ROOT')
      call require_absent(audit,'BLOCK-ACTIVE','AUDIT ROOT')
      call require_absent(audit,'BLOCK-KMAX','AUDIT ROOT')
      allocate(data%block_meta(0),data%block_active(0))
      allocate(data%block_kmax(0))
    else
      call require_record(audit,'BLOCK-META',4*blocks,1,'AUDIT ROOT')
      call require_record(audit,'BLOCK-ACTIVE',ng*blocks,1, &
        'AUDIT ROOT')
      call require_record(audit,'BLOCK-KMAX',ng*blocks,1, &
        'AUDIT ROOT')
      allocate(data%block_meta(4*blocks))
      allocate(data%block_active(ng*blocks))
      allocate(data%block_kmax(ng*blocks))
      call LCMGET(audit,'BLOCK-META',data%block_meta)
      call LCMGET(audit,'BLOCK-ACTIVE',data%block_active)
      call LCMGET(audit,'BLOCK-KMAX',data%block_kmax)
    endif
    call LCMCL(root,1)
  end subroutine load_ledger


  subroutine check_static_state(state)
    integer, intent(in) :: state(naudit_state)

    if (state(1) /= 1) call fail('audit schema version differs')
    if (state(2) /= 1) call fail('audit status is not COMPLETE')
    if (state(3) /= 2) call fail('audit MOCA arm differs')
    if (state(4) /= 1) call fail('audit plane differs')
    if ((state(5) /= ng).or.(state(6) /= nu).or. &
        (state(7) /= ng)) call fail('audit dimensions differ')
    if (state(8) /= 10) call fail('audit KRYL differs')
    if (state(9) /= 1) call fail('MCGMRE entry count is not one')
    if (state(10) /= 1) call fail('MCGMRE exit count is not one')
    if (state(21) /= 20) call fail('audit MCGMRE MAXI differs')
    if (state(22) /= int(epsi_bits)) &
      call fail('audit MCGMRE ERRTOL bits differ')
    if (state(23) /= 0) call fail('operator applications were added')
    if (state(24) /= 0) call fail('reserved audit state is nonzero')
  end subroutine check_static_state


  subroutine close_ledger(data,nonzero_k,sum_k,max_k)
    type(ledger_data), intent(in) :: data
    integer, intent(out) :: nonzero_k,sum_k,max_k
    integer :: entries,total_events,blocks
    integer :: event,block,group,call_index,role,iteration
    integer :: event_index,block_index,active_count
    integer :: call_event_seen(data%state(9))
    integer :: call_block_seen(data%state(9))
    integer :: last_event_iter(data%state(9))
    integer :: last_block_iter(data%state(9))
    integer :: last_nonprimary_block(data%state(9))
    integer :: previous_role_mask(ng,data%state(9))
    integer :: computed_role_calls(nrole)
    integer :: computed_role_groups(nrole)
    integer :: computed_histogram(nkbin)
    integer :: exit_count,event_offset,block_offset
    integer :: event_mask_sum,block_mask_sum,stored_k
    integer :: event_count_for_block,block_max,group_k_sum
    integer :: previous_mask,current_mask,first_event
    integer :: sum_block_max

    entries=data%state(9)
    total_events=sum(data%state(11:13))
    blocks=data%state(17)
    call_event_seen=0
    call_block_seen=0
    last_event_iter=0
    last_block_iter=0
    last_nonprimary_block=0
    previous_role_mask=1
    computed_role_calls=0
    computed_role_groups=0
    computed_histogram=0
    exit_count=0

    do call_index=1,entries
      event_offset=5*(call_index-1)
      if (data%call_meta(event_offset+1) /= call_index) &
        call fail('CALL-META call index is not contiguous')
      if (data%call_meta(event_offset+2) /= 1) &
        call fail('CALL-META normal exit flag differs')
      exit_count=exit_count+data%call_meta(event_offset+2)
      if ((data%call_meta(event_offset+3) < 0).or. &
          (data%call_meta(event_offset+4) < 0).or. &
          (data%call_meta(event_offset+5) < 0).or. &
          (data%call_meta(event_offset+5) > max_global_iter)) &
        call fail('CALL-META count or ITER is outside the frozen range')
    enddo

    do event=1,total_events
      event_offset=6*(event-1)
      call_index=data%role_events(event_offset+1)
      event_index=data%role_events(event_offset+2)
      role=data%role_events(event_offset+3)
      iteration=data%role_events(event_offset+4)
      block_index=data%role_events(event_offset+5)
      active_count=data%role_events(event_offset+6)
      if ((call_index < 1).or.(call_index > entries)) &
        call fail('ROLE-EVENTS call index outside range')
      call_event_seen(call_index)=call_event_seen(call_index)+1
      if (event_index /= call_event_seen(call_index)) &
        call fail('ROLE-EVENTS index is not contiguous')
      if (event > 1) then
        if (call_index < data%role_events(6*(event-2)+1)) &
          call fail('ROLE-EVENTS call order differs')
      endif
      if ((role < 1).or.(role > nrole)) &
        call fail('ROLE-EVENTS role outside range')
      if ((iteration <= 0).or.(iteration > max_global_iter)) &
        call fail('ROLE-EVENTS ITER is outside the frozen range')
      if (iteration < last_event_iter(call_index)) &
        call fail('ROLE-EVENTS ITER decreases within call')
      last_event_iter(call_index)=iteration
      if ((active_count < 0).or.(active_count > ng)) &
        call fail('ROLE-EVENTS active count outside range')
      if (active_count == 0) &
        call fail('ROLE-EVENTS cannot be empty on the MCGMRE path')
      if (role == 1) then
        if (block_index /= 0) call fail('PRIMARY block index is not zero')
      else
        if ((block_index < 1).or. &
            (block_index > data%call_meta(5*(call_index-1)+4))) &
          call fail('nonprimary block index outside range')
        if (block_index < last_nonprimary_block(call_index)) &
          call fail('nonprimary block order decreases')
        last_nonprimary_block(call_index)=block_index
        if ((role == 2).and.(block_index /= 1)) &
          call fail('AFFINE-RHS is not attached to the first block')
      endif
      event_mask_sum=0
      do group=1,ng
        current_mask=data%role_active(ng*(event-1)+group)
        if ((current_mask /= 0).and.(current_mask /= 1)) &
          call fail('ROLE-ACTIVE is not a binary mask')
        if (current_mask > previous_role_mask(group,call_index)) &
          call fail('ROLE-ACTIVE globally changes from zero to one')
        previous_role_mask(group,call_index)=current_mask
        event_mask_sum=event_mask_sum+current_mask
      enddo
      if (event_mask_sum /= active_count) &
        call fail('ROLE-EVENTS active count does not close')
      computed_role_calls(role)=computed_role_calls(role)+1
      computed_role_groups(role)=computed_role_groups(role)+ &
        event_mask_sum
    enddo

    do call_index=1,entries
      event_offset=5*(call_index-1)
      if (call_event_seen(call_index) /= &
          data%call_meta(event_offset+3)) &
        call fail('CALL-META role-event count does not close')
      if (call_event_seen(call_index) == 0) then
        if (data%call_meta(event_offset+5) /= 0) &
          call fail('empty call has nonzero last ITER')
      else if (last_event_iter(call_index) /= &
          data%call_meta(event_offset+5)) then
        call fail('CALL-META last ITER does not close')
      endif
    enddo
    if (exit_count /= data%state(10)) &
      call fail('MCGMRE exit count does not close')
    if (any(computed_role_calls /= data%role_calls)) &
      call fail('ROLE-CALLS does not close from events')
    if (any(computed_role_groups /= data%role_groups)) &
      call fail('ROLE-GROUPS does not close from masks')
    if (any(data%state(11:13) /= computed_role_calls)) &
      call fail('STATE-VECTOR role calls do not close')
    if (any(data%state(14:16) /= computed_role_groups)) &
      call fail('STATE-VECTOR role groups do not close')
    if (computed_role_calls(1) < 1) &
      call fail('at least one PRIMARY role event is required')
    if (computed_role_calls(2) > 1) &
      call fail('more than one AFFINE-RHS event was recorded')
    if (computed_role_calls(1)+computed_role_calls(3) /= &
        data%call_meta(5)) &
      call fail('ITER does not close PRIMARY plus KRYLOV calls')
    if (total_events /= data%call_meta(5)+computed_role_calls(2)) &
      call fail('role-event count does not close frozen ITER semantics')
    if ((blocks == 0).neqv.(computed_role_calls(2) == 0)) &
      call fail('AFFINE-RHS and correction-block presence differ')
    if ((computed_role_calls(1)-blocks < 0).or. &
        (computed_role_calls(1)-blocks > 1)) &
      call fail('PRIMARY and correction-block counts are unreachable')
    call check_event_sequence(data,total_events,blocks)

    nonzero_k=0
    sum_k=0
    max_k=0
    do block=1,blocks
      block_offset=4*(block-1)
      call_index=data%block_meta(block_offset+1)
      block_index=data%block_meta(block_offset+2)
      iteration=data%block_meta(block_offset+3)
      active_count=data%block_meta(block_offset+4)
      if ((call_index < 1).or.(call_index > entries)) &
        call fail('BLOCK-META call index outside range')
      call_block_seen(call_index)=call_block_seen(call_index)+1
      if (block_index /= call_block_seen(call_index)) &
        call fail('BLOCK-META index is not contiguous')
      if (block > 1) then
        if (call_index < data%block_meta(4*(block-2)+1)) &
          call fail('BLOCK-META call order differs')
      endif
      if ((iteration <= 0).or.(iteration > max_global_iter)) &
        call fail('BLOCK-META ITER is outside the frozen range')
      if (iteration < last_block_iter(call_index)) &
        call fail('BLOCK-META ITER decreases within call')
      last_block_iter(call_index)=iteration
      if ((active_count < 1).or.(active_count > ng)) &
        call fail('BLOCK-META active count outside range')
      block_mask_sum=0
      block_max=0
      do group=1,ng
        current_mask=data%block_active(ng*(block-1)+group)
        stored_k=data%block_kmax(ng*(block-1)+group)
        if ((current_mask /= 0).and.(current_mask /= 1)) &
          call fail('BLOCK-ACTIVE is not a binary mask')
        if ((stored_k < 0).or.(stored_k > 10)) &
          call fail('BLOCK-KMAX outside range')
        if ((current_mask == 0).and.(stored_k /= 0)) &
          call fail('inactive group has nonzero KMAX')
        block_mask_sum=block_mask_sum+current_mask
        computed_histogram(stored_k+1)= &
          computed_histogram(stored_k+1)+1
        if (stored_k > 0) nonzero_k=nonzero_k+1
        sum_k=sum_k+stored_k
        max_k=max(max_k,stored_k)
        block_max=max(block_max,stored_k)
      enddo
      if (block_mask_sum /= active_count) &
        call fail('BLOCK-META active count does not close')

      event_count_for_block=0
      first_event=0
      do event=1,total_events
        event_offset=6*(event-1)
        if ((data%role_events(event_offset+1) == call_index).and. &
            (data%role_events(event_offset+3) == 3).and. &
            (data%role_events(event_offset+5) == block_index)) then
          event_count_for_block=event_count_for_block+1
          if (first_event == 0) first_event=event
        endif
      enddo
      if (event_count_for_block /= block_max) &
        call fail('Krylov calls do not equal block maximum KMAX')
      if (block_max == 0) then
        if ((block /= blocks).or.(iteration /= max_global_iter)) &
          call fail('zero-K block is not the final MAXIT block')
      else
        event_index=0
        do event=1,total_events
          event_offset=6*(event-1)
          if ((data%role_events(event_offset+1) == call_index).and. &
              (data%role_events(event_offset+3) == 3).and. &
              (data%role_events(event_offset+5) == block_index)) &
            event_index=max(event_index,data%role_events(event_offset+4))
        enddo
        if (event_index /= iteration) &
          call fail('BLOCK-META ITER does not close Krylov events')
      endif
      do group=1,ng
        group_k_sum=0
        previous_mask=1
        event_index=0
        do event=1,total_events
          event_offset=6*(event-1)
          if ((data%role_events(event_offset+1) == call_index).and. &
              (data%role_events(event_offset+3) == 3).and. &
              (data%role_events(event_offset+5) == block_index)) then
            event_index=event_index+1
            current_mask=data%role_active(ng*(event-1)+group)
            if (event == first_event) then
              if (current_mask /= &
                  data%block_active(ng*(block-1)+group)) &
                call fail('first Krylov mask differs from block mask')
            else if (current_mask > previous_mask) then
              call fail('Krylov active mask changes from zero to one')
            endif
            previous_mask=current_mask
            group_k_sum=group_k_sum+current_mask
          endif
        enddo
        if (group_k_sum /= data%block_kmax(ng*(block-1)+group)) &
          call fail('KMAX does not reconstruct from Krylov masks')
        if ((block_max > 0).and. &
            (data%block_active(ng*(block-1)+group) == 1).and. &
            (data%block_kmax(ng*(block-1)+group) < 1)) &
          call fail('active group lacks first Krylov visit')
      enddo
    enddo

    do call_index=1,entries
      if (call_block_seen(call_index) /= &
          data%call_meta(5*(call_index-1)+4)) &
        call fail('CALL-META block count does not close')
    enddo
    if (sum(call_block_seen) /= data%state(17)) &
      call fail('STATE-VECTOR block count does not close')

    sum_block_max=0
    do block=1,blocks
      block_max=maxval(data%block_kmax(ng*(block-1)+1:ng*block))
      sum_block_max=sum_block_max+block_max
    enddo
    if (computed_role_calls(3) /= sum_block_max) &
      call fail('Krylov ROLE-CALLS cross identity differs')
    if (computed_role_groups(3) /= sum_k) &
      call fail('Krylov ROLE-GROUPS cross identity differs')
    if (any(computed_histogram /= data%histogram)) &
      call fail('K-HISTOGRAM does not close')
    if (sum(computed_histogram) /= ng*blocks) &
      call fail('K-HISTOGRAM row count does not close')
    if (nonzero_k /= ng*blocks-computed_histogram(1)) &
      call fail('nonzero K count does not close from histogram')
    if (data%state(18) /= nonzero_k) &
      call fail('STATE-VECTOR nonzero K count does not close')
    if (data%state(19) /= sum_k) &
      call fail('STATE-VECTOR sum K does not close')
    if (data%state(20) /= max_k) &
      call fail('STATE-VECTOR max K does not close')
    if ((nonzero_k == 0).neqv.(sum_k == 0)) &
      call fail('zero nonzero-count and sum-K equivalence differs')
    if ((nonzero_k == 0).neqv.(max_k == 0)) &
      call fail('zero nonzero-count and max-K equivalence differs')
    if ((nonzero_k == 0).neqv.(computed_role_calls(3) == 0)) &
      call fail('zero K and Krylov-call equivalence differs')
  end subroutine close_ledger


  subroutine check_event_sequence(data,total_events,blocks)
    type(ledger_data), intent(in) :: data
    integer, intent(in) :: total_events,blocks
    integer :: event,block,group,k,event_offset,block_offset,primary_event
    integer :: primary_iter,block_end,block_max,expected_primary_iter

    event=1
    expected_primary_iter=1
    do block=1,blocks
      if (event > total_events) &
        call fail('correction block has no preceding PRIMARY event')
      event_offset=6*(event-1)
      if ((data%role_events(event_offset+1) /= 1).or. &
          (data%role_events(event_offset+3) /= 1).or. &
          (data%role_events(event_offset+5) /= 0)) &
        call fail('event sequence does not begin block with PRIMARY')
      primary_iter=data%role_events(event_offset+4)
      primary_event=event
      if (primary_iter /= expected_primary_iter) &
        call fail('PRIMARY ITER does not follow the previous block')

      block_offset=4*(block-1)
      if ((data%block_meta(block_offset+1) /= 1).or. &
          (data%block_meta(block_offset+2) /= block)) &
        call fail('block sequence identity differs')
      block_end=data%block_meta(block_offset+3)
      block_max=maxval(data%block_kmax(ng*(block-1)+1:ng*block))
      do group=1,ng
        if (data%block_active(ng*(block-1)+group) > &
            data%role_active(ng*(primary_event-1)+group)) &
          call fail('block-entry mask is not a subset of PRIMARY')
      enddo
      event=event+1

      if (block == 1) then
        if (event > total_events) &
          call fail('first correction block has no AFFINE-RHS event')
        event_offset=6*(event-1)
        if ((data%role_events(event_offset+1) /= 1).or. &
            (data%role_events(event_offset+3) /= 2).or. &
            (data%role_events(event_offset+4) /= primary_iter).or. &
            (data%role_events(event_offset+5) /= block)) &
          call fail('AFFINE-RHS event is not immediately after PRIMARY')
        do group=1,ng
          if (data%role_active(ng*(event-1)+group) /= &
              data%block_active(ng*(block-1)+group)) &
            call fail('AFFINE-RHS mask differs from block-entry mask')
        enddo
        event=event+1
      endif

      do k=1,block_max
        if (event > total_events) &
          call fail('correction block has too few KRYLOV events')
        event_offset=6*(event-1)
        if ((data%role_events(event_offset+1) /= 1).or. &
            (data%role_events(event_offset+3) /= 3).or. &
            (data%role_events(event_offset+4) /= primary_iter+k).or. &
            (data%role_events(event_offset+5) /= block)) &
          call fail('KRYLOV event sequence or ITER differs')
        event=event+1
      enddo
      if (block_end /= primary_iter+block_max) &
        call fail('block end ITER does not close its event sequence')
      expected_primary_iter=block_end+1
    enddo

    if (event <= total_events) then
      if (event /= total_events) &
        call fail('more than one terminal event follows the last block')
      event_offset=6*(event-1)
      if ((data%role_events(event_offset+1) /= 1).or. &
          (data%role_events(event_offset+3) /= 1).or. &
          (data%role_events(event_offset+4) /= expected_primary_iter).or. &
          (data%role_events(event_offset+5) /= 0)) &
        call fail('terminal PRIMARY event sequence differs')
      event=event+1
    endif
    if (event /= total_events+1) &
      call fail('event sequence does not consume the complete ledger')
  end subroutine check_event_sequence


  subroutine print_ledger(data,nonzero_k,sum_k,max_k,classification)
    type(ledger_data), intent(in) :: data
    integer, intent(in) :: nonzero_k,sum_k,max_k
    character(len=*), intent(in) :: classification
    integer :: entries,total_events,blocks
    integer :: field,call_index,event,group,block,offset

    entries=data%state(9)
    total_events=sum(data%role_calls)
    blocks=data%state(17)
    write(6,'(A,1X,I0,1X,I0,1X,Z8.8)') &
      'GMRES-ACTIVITY RAW TRACK',20,10,epsi_bits
    do field=1,naudit_state
      write(6,'(A,1X,I0,1X,I0)') &
        'GMRES-ACTIVITY RAW STATE',field,data%state(field)
    enddo
    do group=1,ng
      write(6,'(A,1X,I0,1X,I0)') &
        'GMRES-ACTIVITY RAW NGIND',group,data%ngind(group)
    enddo
    do call_index=1,entries
      offset=5*(call_index-1)
      write(6,'(A,5(1X,I0))') 'GMRES-ACTIVITY RAW CALL', &
        data%call_meta(offset+1:offset+5)
    enddo
    do field=1,nrole
      write(6,'(A,3(1X,I0))') 'GMRES-ACTIVITY RAW ROLE-SUM', &
        field,data%role_calls(field),data%role_groups(field)
    enddo
    do event=1,total_events
      offset=6*(event-1)
      write(6,'(A,6(1X,I0))') 'GMRES-ACTIVITY RAW ROLE', &
        data%role_events(offset+1:offset+6)
      do group=1,ng
        write(6,'(A,3(1X,I0))') &
          'GMRES-ACTIVITY RAW ROLE-ACTIVE',event,group, &
          data%role_active(ng*(event-1)+group)
      enddo
    enddo
    do block=1,blocks
      offset=4*(block-1)
      write(6,'(A,4(1X,I0))') 'GMRES-ACTIVITY RAW BLOCK', &
        data%block_meta(offset+1:offset+4)
      do group=1,ng
        write(6,'(A,4(1X,I0))') &
          'GMRES-ACTIVITY RAW BLOCK-GROUP',block,group, &
          data%block_active(ng*(block-1)+group), &
          data%block_kmax(ng*(block-1)+group)
      enddo
    enddo
    do field=1,nkbin
      write(6,'(A,2(1X,I0))') 'GMRES-ACTIVITY RAW K-HISTOGRAM', &
        field-1,data%histogram(field)
    enddo
    write(6,'(A,1X,I0)') &
      'GMRES-ACTIVITY NONZERO-K-GROUP-BLOCKS',nonzero_k
    write(6,'(A,1X,I0)') 'GMRES-ACTIVITY SUM-K',sum_k
    write(6,'(A,1X,I0)') 'GMRES-ACTIVITY MAX-K',max_k
    write(6,'(A)') 'GMRES-ACTIVITY THRESHOLD NONE'
    write(6,'(A,1X,A)') 'GMRES-ACTIVITY CLASSIFICATION',classification
    write(6,'(A)') 'GMRES-ACTIVITY COMPLETE'
  end subroutine print_ledger


  subroutine require_audit_names(audit,total_events,blocks)
    type(c_ptr), intent(in) :: audit
    integer, intent(in) :: total_events,blocks
    character(len=12) :: expected(11)
    integer :: count

    expected=' '
    count=6
    expected(1:6)=[character(len=12) :: 'CALL-META', &
      'K-HISTOGRAM','NGIND','ROLE-CALLS','ROLE-GROUPS','STATE-VECTOR']
    if (total_events > 0) then
      count=count+2
      expected(count-1:count)=[character(len=12) :: &
        'ROLE-ACTIVE','ROLE-EVENTS']
    endif
    if (blocks > 0) then
      count=count+3
      expected(count-2:count)=[character(len=12) :: &
        'BLOCK-ACTIVE','BLOCK-KMAX','BLOCK-META']
    endif
    call require_table_names(audit,expected(1:count),'AUDIT ROOT')
  end subroutine require_audit_names


  subroutine require_table_names(table,expected,owner)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(in) :: expected(:)
    character(len=*), intent(in) :: owner
    character(len=12) :: found(max_records)
    character(len=12) :: sorted_expected(size(expected))
    integer :: count

    call collect_names(table,found,count)
    sorted_expected=expected
    call sort_names(sorted_expected)
    if (count /= size(expected)) call fail(trim(owner)//' census differs')
    if (any(found(1:count) /= sorted_expected)) &
      call fail(trim(owner)//' names differ')
  end subroutine require_table_names


  subroutine collect_names(table,names,count)
    type(c_ptr), intent(in) :: table
    character(len=12), intent(out) :: names(max_records)
    integer, intent(out) :: count
    character(len=12) :: name,first

    names=' '
    count=0
    name=' '
    call LCMNXT(table,name)
    if (name == ' ') return
    first=name
    do
      count=count+1
      if (count > max_records) call fail('too many audit records')
      names(count)=name
      call LCMNXT(table,name)
      if (name == first) exit
    enddo
    call sort_names(names(1:count))
  end subroutine collect_names


  subroutine sort_names(names)
    character(len=12), intent(inout) :: names(:)
    character(len=12) :: held
    integer :: i,j

    do i=2,size(names)
      held=names(i)
      j=i-1
      do while (j >= 1)
        if (names(j) <= held) exit
        names(j+1)=names(j)
        j=j-1
      enddo
      names(j+1)=held
    enddo
  end subroutine sort_names


  subroutine require_signature(ptr,expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: expected,owner
    character(len=12) :: signature

    call require_record(ptr,'SIGNATURE',3,3,owner)
    call LCMGTC(ptr,'SIGNATURE',12,signature)
    if (signature /= expected) call fail(trim(owner)//' signature differs')
  end subroutine require_signature


  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner)//' invalid record', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('record contract failure')
    endif
  end subroutine require_record


  subroutine require_absent(ptr,name,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if (length_found /= 0) &
      call fail(trim(owner)//' unexpected zero-case record')
  end subroutine require_absent


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'GMRES-ACTIVITY CHECK FAIL: '//trim(message)
    error stop 1
  end subroutine fail

end program check_gmres_activity_xsm
