program make_gmres_activity_fixture
  ! Test-only Ganlib writer for the independent GMRES activity checker.
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

  character(len=1024) :: outdir,mode
  character(len=1024) :: track_path,activity_path
  type(ledger_data) :: data
  integer :: mccg_state(ntrack_state)
  real(real32) :: real_param(4)

  if (command_argument_count() /= 2) &
    error stop 'expected OUTDIR MODE'
  call get_command_argument(1,outdir)
  call get_command_argument(2,mode)
  if ((len_trim(outdir) == 0).or.(len_trim(mode) == 0)) &
    error stop 'empty argument'
  track_path=trim(outdir)//'/track.xsm'
  activity_path=trim(outdir)//'/activity.xsm'
  if ((len_trim(track_path) > max_path).or. &
      (len_trim(activity_path) > max_path)) &
    error stop 'fixture path exceeds Ganlib limit'

  select case (trim(mode))
  case ('zero-block')
    call setup_zero_block(data)
  case ('zero-k')
    call setup_zero_k(data)
  case ('active')
    call setup_active(data)
  case ('mixed')
    call setup_mixed(data)
  case ('tamper-zero-role')
    call setup_zero_role(data)
  case ('tamper-unexpected-block')
    call setup_zero_block(data)
  case default
    call setup_mixed(data)
    call apply_tamper(data,trim(mode))
  end select

  mccg_state=0
  mccg_state(3)=10
  mccg_state(13)=20
  real_param=0.0_real32
  real_param(1)=transfer(epsi_bits,0.0_real32)
  if (trim(mode) == 'tamper-track-kryl') mccg_state(3)=9
  if (trim(mode) == 'tamper-track-maxi') mccg_state(13)=19
  if (trim(mode) == 'tamper-track-epsi') &
    real_param(1)=transfer(epsi_bits+1_int32,0.0_real32)

  call write_track(trim(track_path),mccg_state,real_param)
  call write_activity(trim(activity_path),data,trim(mode))

contains

  subroutine initialize_data(data,nevents,nblocks)
    type(ledger_data), intent(out) :: data
    integer, intent(in) :: nevents,nblocks
    integer :: group

    data%state=0
    data%state(1)=1
    data%state(2)=1
    data%state(3)=2
    data%state(4)=1
    data%state(5)=ng
    data%state(6)=nu
    data%state(7)=ng
    data%state(8)=10
    data%state(9)=1
    data%state(10)=1
    data%state(21)=20
    data%state(22)=int(epsi_bits)
    data%state(23)=0
    data%state(24)=0
    data%ngind=[(group,group=1,ng)]
    allocate(data%call_meta(5))
    allocate(data%role_events(6*nevents))
    allocate(data%role_active(ng*nevents))
    allocate(data%block_meta(4*nblocks))
    allocate(data%block_active(ng*nblocks))
    allocate(data%block_kmax(ng*nblocks))
    data%call_meta=0
    data%role_events=0
    data%role_active=0
    data%block_meta=0
    data%block_active=0
    data%block_kmax=0
  end subroutine initialize_data


  subroutine setup_zero_role(data)
    type(ledger_data), intent(out) :: data

    call initialize_data(data,0,0)
    data%call_meta=[1,1,0,0,0]
    call finalize_aggregates(data)
  end subroutine setup_zero_role


  subroutine setup_zero_block(data)
    type(ledger_data), intent(out) :: data
    integer :: mask(ng),group

    call initialize_data(data,1,0)
    do group=1,ng
      mask(group)=merge(1,0,(mod(group,7) == 0).or.(group == 1))
    enddo
    call set_event(data,1,1,1,1,1,0,mask)
    data%call_meta=[1,1,1,0,1]
    call finalize_aggregates(data)
  end subroutine setup_zero_block


  subroutine setup_zero_k(data)
    type(ledger_data), intent(out) :: data
    integer :: mask1(ng),mask2(ng),mask3(ng)
    integer :: kmax1(ng),kmax2(ng),kmax3(ng)
    integer :: event,group,k,count2,count3

    ! Reach the exact MAXIT=19 boundary through an attainable call trace.
    ! The last correction block has KMAX=0 because no Krylov iteration can
    ! start, while the complete ledger still retains the earlier activity.
    call initialize_data(data,20,3)
    mask2=0
    mask3=0
    do group=1,ng
      mask1(group)=merge(1,0,(mod(group,3) /= 0).or.(group == ng))
    enddo
    count2=0
    do group=1,ng
      if ((mask1(group) == 1).and.(count2 < 75)) then
        mask2(group)=1
        count2=count2+1
      endif
    enddo
    count3=0
    do group=1,ng
      if ((mask2(group) == 1).and.(count3 < 22)) then
        mask3(group)=1
        count3=count3+1
      endif
    enddo
    if ((count2 /= 75).or.(count3 /= 22)) &
      error stop 'nested zero-K masks differ'
    kmax1=10*mask1
    kmax2=6*mask2
    kmax3=0

    event=1
    call set_event(data,event,1,event,1,1,0,mask1)
    event=event+1
    call set_event(data,event,1,event,2,1,1,mask1)
    do k=1,10
      event=event+1
      call set_event(data,event,1,event,3,1+k,1,mask1)
    enddo
    event=event+1
    call set_event(data,event,1,event,1,12,0,mask2)
    do k=1,6
      event=event+1
      call set_event(data,event,1,event,3,12+k,2,mask2)
    enddo
    event=event+1
    call set_event(data,event,1,event,1,19,0,mask3)
    if (event /= 20) error stop 'zero-K capacity trace differs'

    call set_block(data,1,1,1,11,mask1,kmax1)
    call set_block(data,2,1,2,18,mask2,kmax2)
    call set_block(data,3,1,3,19,mask3,kmax3)
    data%call_meta=[1,1,20,3,19]
    call finalize_aggregates(data)
  end subroutine setup_zero_k


  subroutine setup_active(data)
    type(ledger_data), intent(out) :: data
    integer :: mask(ng),final_mask(ng),kmax(ng),group

    call initialize_data(data,4,1)
    do group=1,ng
      mask(group)=merge(1,0,(mod(group,4) == 1).or.(group == ng))
      final_mask(group)=merge(1,0,(mask(group) == 1).and. &
        (mod(group,11) == 1))
    enddo
    kmax=mask
    call set_event(data,1,1,1,1,1,0,mask)
    call set_event(data,2,1,2,2,1,1,mask)
    call set_event(data,3,1,3,3,2,1,mask)
    call set_event(data,4,1,4,1,3,0,final_mask)
    call set_block(data,1,1,1,2,mask,kmax)
    data%call_meta=[1,1,4,1,3]
    call finalize_aggregates(data)
  end subroutine setup_active


  subroutine setup_mixed(data)
    type(ledger_data), intent(out) :: data
    integer :: b1(ng),b1k2(ng),b1k3(ng),b1max(ng)
    integer :: b2(ng),b2k2(ng),b2max(ng),final_mask(ng)
    integer :: group,count3

    call initialize_data(data,9,2)
    do group=1,ng
      b1(group)=merge(1,0,(mod(group,2) == 1).or.(group == ng))
      b1k2(group)=merge(1,0,(b1(group) == 1).and. &
        (mod(group,4) == 1))
      b1k3(group)=0
      b2(group)=0
      b2k2(group)=0
      final_mask(group)=0
    enddo
    count3=0
    do group=1,ng
      if ((b1k2(group) == 1).and.(count3 < 75)) then
        b1k3(group)=1
        b2(group)=1
        count3=count3+1
      endif
    enddo
    if ((count3 /= 75).or.(b2(1) /= 1).or.(b2(297) /= 1)) &
      error stop 'nested mixed masks differ'
    b2k2(1)=1
    b2k2(297)=1
    final_mask(1)=1
    b1max=b1+b1k2+b1k3
    b2max=b2+b2k2

    call set_event(data,1,1,1,1,1,0,b1)
    call set_event(data,2,1,2,2,1,1,b1)
    call set_event(data,3,1,3,3,2,1,b1)
    call set_event(data,4,1,4,3,3,1,b1k2)
    call set_event(data,5,1,5,3,4,1,b1k3)
    call set_event(data,6,1,6,1,5,0,b2)
    call set_event(data,7,1,7,3,6,2,b2)
    call set_event(data,8,1,8,3,7,2,b2k2)
    call set_event(data,9,1,9,1,8,0,final_mask)
    call set_block(data,1,1,1,4,b1,b1max)
    call set_block(data,2,1,2,7,b2,b2max)
    data%call_meta=[1,1,9,2,8]
    call finalize_aggregates(data)
  end subroutine setup_mixed


  subroutine set_event(data,event,call_index,event_index,role,iteration, &
      block_index,mask)
    type(ledger_data), intent(inout) :: data
    integer, intent(in) :: event,call_index,event_index,role,iteration
    integer, intent(in) :: block_index,mask(ng)
    integer :: offset

    offset=6*(event-1)
    data%role_events(offset+1:offset+6)=[call_index,event_index,role, &
      iteration,block_index,sum(mask)]
    data%role_active(ng*(event-1)+1:ng*event)=mask
  end subroutine set_event


  subroutine set_block(data,block,call_index,block_index,iteration, &
      active,kmax)
    type(ledger_data), intent(inout) :: data
    integer, intent(in) :: block,call_index,block_index,iteration
    integer, intent(in) :: active(ng),kmax(ng)
    integer :: offset

    offset=4*(block-1)
    data%block_meta(offset+1:offset+4)=[call_index,block_index, &
      iteration,sum(active)]
    data%block_active(ng*(block-1)+1:ng*block)=active
    data%block_kmax(ng*(block-1)+1:ng*block)=kmax
  end subroutine set_block


  subroutine finalize_aggregates(data)
    type(ledger_data), intent(inout) :: data
    integer :: nevents,nblocks,event,block,group,offset,role,value
    integer :: nonzero_k,sum_k,max_k

    nevents=size(data%role_events)/6
    nblocks=size(data%block_meta)/4
    data%role_calls=0
    data%role_groups=0
    do event=1,nevents
      offset=6*(event-1)
      role=data%role_events(offset+3)
      data%role_events(offset+6)= &
        sum(data%role_active(ng*(event-1)+1:ng*event))
      data%role_calls(role)=data%role_calls(role)+1
      data%role_groups(role)=data%role_groups(role)+ &
        data%role_events(offset+6)
    enddo
    data%histogram=0
    nonzero_k=0
    sum_k=0
    max_k=0
    do block=1,nblocks
      offset=4*(block-1)
      data%block_meta(offset+4)= &
        sum(data%block_active(ng*(block-1)+1:ng*block))
      do group=1,ng
        value=data%block_kmax(ng*(block-1)+group)
        if ((value >= 0).and.(value <= 10)) &
          data%histogram(value+1)=data%histogram(value+1)+1
        if (value > 0) nonzero_k=nonzero_k+1
        sum_k=sum_k+value
        max_k=max(max_k,value)
      enddo
    enddo
    data%state(11:13)=data%role_calls
    data%state(14:16)=data%role_groups
    data%state(17)=nblocks
    data%state(18)=nonzero_k
    data%state(19)=sum_k
    data%state(20)=max_k
  end subroutine finalize_aggregates


  subroutine apply_tamper(data,mode)
    type(ledger_data), intent(inout) :: data
    character(len=*), intent(in) :: mode
    integer :: held6(6),held4(4)
    integer :: offset

    select case (mode)
    case ('tamper-track-kryl','tamper-track-maxi','tamper-track-epsi', &
        'tamper-extra','tamper-missing-role-active', &
        'tamper-wrong-role-type','tamper-wrong-role-length', &
        'tamper-missing-block-active','tamper-wrong-block-type', &
        'tamper-wrong-block-length')
      continue
    case ('tamper-status')
      data%state(2)=0
    case ('tamper-state-sum')
      data%state(19)=data%state(19)+1
    case ('tamper-added-operator')
      data%state(23)=1
    case ('tamper-ngind')
      data%ngind(1)=2
    case ('tamper-reordered-event')
      held6=data%role_events(13:18)
      data%role_events(13:18)=data%role_events(19:24)
      data%role_events(19:24)=held6
    case ('tamper-duplicate-event')
      data%role_events(20)=data%role_events(14)
    case ('tamper-role')
      data%role_events(15)=4
    case ('tamper-event-iter')
      data%role_events(16)=0
    case ('tamper-event-iter-high')
      data%role_events(16)=20
    case ('tamper-event-block')
      data%role_events(11)=3
    case ('tamper-event-active-count')
      data%role_events(12)=data%role_events(12)+1
    case ('tamper-role-mask')
      data%role_active(1)=2
    case ('tamper-event-sequence')
      data%role_events(6*(2-1)+3)=1
      data%role_events(6*(2-1)+5)=0
      data%role_events(6*(6-1)+3)=2
      data%role_events(6*(6-1)+5)=1
      call finalize_aggregates(data)
    case ('tamper-affine-mask')
      do offset=2,8
        data%role_active(ng*(offset-1)+5)=0
      enddo
      call finalize_aggregates(data)
    case ('tamper-global-mask-rise')
      data%role_active(ng*(9-1)+1)=0
      data%role_active(ng*(9-1)+2)=1
      call finalize_aggregates(data)
    case ('tamper-empty-primary')
      data%role_active(ng*(9-1)+1:ng*9)=0
      call finalize_aggregates(data)
    case ('tamper-call-exit')
      data%call_meta(2)=0
    case ('tamper-call-event-count')
      data%call_meta(3)=data%call_meta(3)+1
    case ('tamper-call-block-count')
      data%call_meta(4)=data%call_meta(4)+1
    case ('tamper-call-last-iter')
      data%call_meta(5)=data%call_meta(5)+1
    case ('tamper-reordered-block')
      held4=data%block_meta(1:4)
      data%block_meta(1:4)=data%block_meta(5:8)
      data%block_meta(5:8)=held4
    case ('tamper-duplicate-block')
      data%block_meta(6)=1
    case ('tamper-block-mask')
      data%block_active(1)=2
    case ('tamper-inactive-k')
      data%block_active(5)=0
      data%block_active(ng+5)=0
      do offset=2,size(data%role_events)/6
        data%role_active(ng*(offset-1)+5)=0
      enddo
      call finalize_aggregates(data)
    case ('tamper-k-range')
      data%block_kmax(1)=11
    case ('tamper-k-reconstruct')
      data%block_kmax(5)=data%block_kmax(5)-1
      call finalize_aggregates(data)
    case ('tamper-first-mask')
      offset=ng*(3-1)+ng
      data%role_active(offset)=0
      data%block_kmax(ng)=0
      call finalize_aggregates(data)
    case ('tamper-monotone')
      data%role_active(ng*(4-1)+5)=0
      data%role_active(ng*(5-1)+5)=1
      call finalize_aggregates(data)
    case ('tamper-histogram')
      data%histogram(2)=data%histogram(2)+1
    case ('tamper-role-groups')
      data%role_groups(3)=data%role_groups(3)+1
      data%state(16)=data%state(16)+1
    case default
      error stop 'unknown fixture mode'
    end select
  end subroutine apply_tamper


  subroutine write_track(path,mccg_state,real_param)
    character(len=*), intent(in) :: path
    integer, intent(in) :: mccg_state(ntrack_state)
    real(real32), intent(in) :: real_param(4)
    type(c_ptr) :: root
    character(len=12) :: text

    call LCMOP(root,path,0,2,0)
    text='L_TRACK'
    call LCMPTC(root,'SIGNATURE',12,text)
    text='MCCG'
    call LCMPTC(root,'TRACK-TYPE',12,text)
    call LCMPUT(root,'MCCG-STATE',ntrack_state,1,mccg_state)
    call LCMPUT(root,'REAL-PARAM',4,2,real_param)
    call LCMCL(root,1)
  end subroutine write_track


  subroutine write_activity(path,data,mode)
    character(len=*), intent(in) :: path,mode
    type(ledger_data), intent(in) :: data
    type(c_ptr) :: root,audit
    character(len=12) :: text
    integer :: nevents,nblocks
    integer :: one(1),dummy_meta(4),dummy_groups(ng)
    real(real32), allocatable :: real_record(:)

    nevents=size(data%role_events)/6
    nblocks=size(data%block_meta)/4
    call LCMOP(root,path,0,2,0)
    text='L_FLUX'
    call LCMPTC(root,'SIGNATURE',12,text)
    audit=LCMDID(root,'SPOT-GMR-AUD')
    call LCMPUT(audit,'STATE-VECTOR',naudit_state,1,data%state)
    call LCMPUT(audit,'NGIND',ng,1,data%ngind)
    call LCMPUT(audit,'CALL-META',size(data%call_meta),1, &
      data%call_meta)
    call LCMPUT(audit,'ROLE-CALLS',nrole,1,data%role_calls)
    call LCMPUT(audit,'ROLE-GROUPS',nrole,1,data%role_groups)
    call LCMPUT(audit,'K-HISTOGRAM',nkbin,1,data%histogram)

    if (nevents > 0) then
      if (mode == 'tamper-wrong-role-type') then
        allocate(real_record(size(data%role_events)))
        real_record=real(data%role_events,real32)
        call LCMPUT(audit,'ROLE-EVENTS',size(real_record),2,real_record)
        deallocate(real_record)
      else if (mode == 'tamper-wrong-role-length') then
        call LCMPUT(audit,'ROLE-EVENTS',size(data%role_events)-1,1, &
          data%role_events(1:size(data%role_events)-1))
      else
        call LCMPUT(audit,'ROLE-EVENTS',size(data%role_events),1, &
          data%role_events)
      endif
      if (mode /= 'tamper-missing-role-active') &
        call LCMPUT(audit,'ROLE-ACTIVE',size(data%role_active),1, &
          data%role_active)
    endif

    if (nblocks > 0) then
      call LCMPUT(audit,'BLOCK-META',size(data%block_meta),1, &
        data%block_meta)
      if (mode == 'tamper-wrong-block-type') then
        allocate(real_record(size(data%block_active)))
        real_record=real(data%block_active,real32)
        call LCMPUT(audit,'BLOCK-ACTIVE',size(real_record),2,real_record)
        deallocate(real_record)
      else if (mode == 'tamper-wrong-block-length') then
        call LCMPUT(audit,'BLOCK-ACTIVE',size(data%block_active)-1,1, &
          data%block_active(1:size(data%block_active)-1))
      else if (mode /= 'tamper-missing-block-active') then
        call LCMPUT(audit,'BLOCK-ACTIVE',size(data%block_active),1, &
          data%block_active)
      endif
      call LCMPUT(audit,'BLOCK-KMAX',size(data%block_kmax),1, &
        data%block_kmax)
    else if (mode == 'tamper-unexpected-block') then
      dummy_meta=[1,1,1,1]
      dummy_groups=0
      dummy_groups(1)=1
      call LCMPUT(audit,'BLOCK-META',4,1,dummy_meta)
      call LCMPUT(audit,'BLOCK-ACTIVE',ng,1,dummy_groups)
      call LCMPUT(audit,'BLOCK-KMAX',ng,1,dummy_groups)
    endif
    if (mode == 'tamper-extra') then
      one(1)=17
      call LCMPUT(audit,'EXTRA',1,1,one)
    endif
    call LCMCL(root,1)
  end subroutine write_activity

end program make_gmres_activity_fixture
