! DRAFT controls: not compiled or executed. No transport/physics qualification.
! Link against the actual candidate SPOT1P64_CACHE_MOD and ordinary kernel deps.
! All comparisons/qualification belong to the independent external byte auditor.
module keycodec_abort_state
  implicit none
  logical, save :: rejection_expected=.false.
  character(len=*), parameter :: identity_message= &
    'SPOT1P64 RANK1 CACHE: IMMUTABLE OPERATOR CHANGED.'
end module keycodec_abort_state

program keycodec_controls
  use, intrinsic :: iso_fortran_env, only: int32,int64
  use SPOT1P64_CACHE_MOD
  use keycodec_abort_state
  implicit none
  integer, parameter :: declared_groups=12
  integer :: manifest,event_id,phase_arg,ios
  character(len=80) :: mode,mutation,phase_text
  integer(int64) :: base1(6),base2(6)

  call get_command_argument(1,mode)
  if (storage_size(0) /= 32 .or. storage_size(0_int32) /= 32 .or. &
      storage_size(0_int64) /= 64) stop 2
  event_id=0
  open(newunit=manifest,file='keycodec_manifest.jsonl',status='new',action='write')
  ! The words are integer identities, never evaluated as floating point.
  base1=[0_int64,int(z'8000000000000000',int64), &
    int(z'7FFFFFFFFFFFFFFF',int64),int(z'FFFFFFFFFFFFFFFF',int64), &
    int(z'7FF8000000000123',int64),int(z'7FF0000000000001',int64)]
  base2=[int(z'7FF0000000000000',int64),int(z'FFF0000000000000',int64), &
    int(z'FFF8000000000456',int64),int(z'3FF0000000000000',int64), &
    int(z'8000000000000000',int64),0_int64]
  select case(trim(mode))
  case('positive')
    call threshold_fixture()
    call lifecycle_fixture()
    close(manifest)
    write(*,'(A)') 'RAW_KEYCODEC_CONTROLS_COMPLETE'
  case('negative')
    call get_command_argument(2,mutation)
    call get_command_argument(3,phase_text)
    read(phase_text,*,iostat=ios) phase_arg
    if (ios /= 0) stop 2
    if (phase_arg /= 1 .and. phase_arg /= 2) stop 2
    call negative_fixture(trim(mutation),phase_arg)
    stop 1
  case default
    stop 2
  end select

contains

  function number(n) result(s)
    integer(int64), intent(in) :: n
    character(len=:), allocatable :: s
    character(len=80) :: t
    write(t,'(I0)') n
    s=trim(t)
  end function number

  subroutine mutated(base,d,key)
    integer(int64), intent(in) :: base(:)
    integer, intent(in) :: d
    integer(int64), intent(out) :: key(:)
    integer :: i
    key=base
    do i=1,d
      key(i)=ieor(base(i),1_int64)
    enddo
  end subroutine mutated

  subroutine guard_capture(name,ig,phase,key,eligible)
    character(len=*), intent(in) :: name
    integer, intent(in) :: ig,phase
    integer(int64), intent(in) :: key(:)
    logical, optional, intent(in) :: eligible
    logical :: allow,active
    allow=.true.
    if (present(eligible)) allow=eligible
    call SPOT1P64_RANK1_GUARD(ig,key,phase,allow,active)
    call key_snapshot(name,ig,phase,key,active,.true.)
  end subroutine guard_capture

  subroutine key_snapshot(name,ig,phase,input,active,decode)
    character(len=*), intent(in) :: name
    integer, intent(in) :: ig,phase
    integer(int64), intent(in) :: input(:)
    logical, intent(in) :: active,decode
    integer :: out,owner
    integer(int64) :: h(32),count,words,positions,built,reuses,hits,live,peak,cap
    integer(int64), allocatable :: payload(:),anchor(:),decoded(:)
    integer(int32), allocatable :: indices(:)
    logical :: compressed,hasmode,ready,hasbits,haspositions,anchorbits,anchorpositions
    character(len=:), allocatable :: filename

    owner=0; count=0; words=0; positions=0; compressed=.false.
    hasmode=.false.; ready=.false.; hasbits=.false.; haspositions=.false.
    anchorbits=.false.; anchorpositions=.false.
    allocate(payload(0),anchor(0),decoded(0),indices(0))
    if (allocated(SPOT1P64_PLAN)) then
      if (ig >= 1 .and. ig <= size(SPOT1P64_PLAN)) then
        hasmode=allocated(SPOT1P64_PLAN(ig)%mode)
      endif
    endif
    if (hasmode) then
      call SPOT1P64_RANK1_KEY_STATS(ig,phase,owner,count,compressed,words,positions)
      associate(plan => SPOT1P64_PLAN(ig)%mode(1))
        ready=plan%ready
        if (phase == 1) then
          hasbits=allocated(plan%rank1_raw_bits)
          haspositions=allocated(plan%rank1_raw_positions)
          if (hasbits) payload=plan%rank1_raw_bits
          if (haspositions) indices=plan%rank1_raw_positions
        else
          hasbits=allocated(plan%rank1_operator_bits)
          haspositions=allocated(plan%rank1_operator_positions)
          if (hasbits) payload=plan%rank1_operator_bits
          if (haspositions) indices=plan%rank1_operator_positions
        endif
      end associate
      if (owner >= 1 .and. owner <= size(SPOT1P64_PLAN)) then
        if (allocated(SPOT1P64_PLAN(owner)%mode)) then
          associate(base => SPOT1P64_PLAN(owner)%mode(1))
            if (phase == 1) then
              anchorbits=allocated(base%rank1_raw_bits)
              anchorpositions=allocated(base%rank1_raw_positions)
              if (anchorbits) anchor=base%rank1_raw_bits
            else
              anchorbits=allocated(base%rank1_operator_bits)
              anchorpositions=allocated(base%rank1_operator_positions)
              if (anchorbits) anchor=base%rank1_operator_bits
            endif
          end associate
        endif
      endif
      if (decode) then
        deallocate(decoded)
        allocate(decoded(int(count)))
        call SPOT1P64_RANK1_KEY_LOAD(ig,phase,decoded)
      endif
    endif
    call SPOT1P64_RANK1_STATS(built,reuses,hits,live,peak,cap)
    event_id=event_id+1
    h=0_int64
    h(1:30)=[1_int64,int(event_id,int64),int(ig,int64),int(phase,int64), &
      size(input,kind=int64),size(decoded,kind=int64),count,words,positions, &
      merge(1_int64,0_int64,compressed),int(owner,int64), &
      size(payload,kind=int64),size(indices,kind=int64),size(anchor,kind=int64), &
      merge(1_int64,0_int64,hasmode),merge(1_int64,0_int64,ready), &
      merge(1_int64,0_int64,active),built,reuses,hits,live,peak,cap, &
      int(declared_groups,int64),merge(1_int64,0_int64,allocated(SPOT1P64_PLAN)), &
      merge(1_int64,0_int64,haspositions),merge(1_int64,0_int64,hasbits), &
      merge(1_int64,0_int64,anchorpositions),merge(1_int64,0_int64,anchorbits), &
      merge(1_int64,0_int64,decode)]
    filename=trim(name)//'.bin'
    open(newunit=out,file=filename,status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) h,input,payload,indices,anchor,decoded
    close(out)
    write(manifest,'(A)') '{"kind":"key_snapshot","name":"'//trim(name)// &
      '","file":"'//filename//'","event":'//number(int(event_id,int64))// &
      ',"group":'//number(int(ig,int64))//',"phase":'//number(int(phase,int64))//'}'
    flush(manifest)
  end subroutine key_snapshot

  subroutine stats_snapshot(name)
    character(len=*), intent(in) :: name
    integer :: out
    integer(int64) :: h(10),built,reuses,hits,live,peak,cap
    call SPOT1P64_RANK1_STATS(built,reuses,hits,live,peak,cap)
    event_id=event_id+1
    h=[1_int64,int(event_id,int64),built,reuses,hits,live,peak,cap, &
      merge(1_int64,0_int64,allocated(SPOT1P64_PLAN)),int(declared_groups,int64)]
    open(newunit=out,file=trim(name)//'.stats.bin',status='new',action='write', &
      form='unformatted',access='stream',convert='little_endian')
    write(out) h
    close(out)
    write(manifest,'(A)') '{"kind":"stats_snapshot","name":"'//trim(name)// &
      '","file":"'//trim(name)//'.stats.bin","event":'//number(int(event_id,int64))//'}'
    flush(manifest)
  end subroutine stats_snapshot

  subroutine threshold_fixture()
    integer(int64) :: key(6),long_key(7)
    call SPOT1P64_CACHE_BEGIN(declared_groups,.false.,.true.)
    call stats_snapshot('threshold_begin')
    ! Phase 1 owner is group 5; phase 2 owner below is group 2.
    call guard_capture('p1_owner5',5,1,base1)
    call guard_capture('p1_zero_delta',1,1,base1)
    call mutated(base1,1,key)
    call guard_capture('p1_single_delta',2,1,key)
    call mutated(base1,3,key)
    call guard_capture('p1_strict_12d36_lt_8n48',3,1,key)
    call mutated(base1,4,key)
    call guard_capture('p1_equal_12d48_eq_8n48_full',4,1,key)
    call mutated(base1,5,key)
    call guard_capture('p1_over_12d60_gt_8n48_full',6,1,key)
    long_key(:6)=base1; long_key(7)=17_int64
    call guard_capture('p1_different_size_full',7,1,long_key)
    call guard_capture('p2_owner2',2,2,base2)
    call guard_capture('p2_zero_delta',5,2,base2)
    call mutated(base2,1,key)
    call guard_capture('p2_single_delta',1,2,key)
    call mutated(base2,3,key)
    call guard_capture('p2_strict_12d36_lt_8n48',3,2,key)
    call mutated(base2,4,key)
    call guard_capture('p2_equal_12d48_eq_8n48_full',4,2,key)
    call mutated(base2,5,key)
    call guard_capture('p2_over_12d60_gt_8n48_full',6,2,key)
    long_key(:6)=base2; long_key(7)=19_int64
    call guard_capture('p2_different_size_full',7,2,long_key)
    ! Neither phase may allocate a plan for an ineligible fresh group.
    call guard_capture('p1_ineligible_fresh',11,1,base1,.false.)
    call guard_capture('p2_ineligible_fresh',11,2,base2,.false.)
    ! Mark ready explicitly: this is a GUARD counter primitive, no factor claim.
    SPOT1P64_PLAN(5)%mode(1)%ready=.true.
    call guard_capture('ready_phase1_no_hit',5,1,base1)
    call guard_capture('ready_phase2_first_hit',5,2,base2)
    call guard_capture('ready_phase2_second_hit',5,2,base2)
    SPOT1P64_PLAN(5)%mode(1)%ready=.false.
    call guard_capture('not_ready_phase2_no_hit',5,2,base2)
    call SPOT1P64_CACHE_CLEAR()
    call stats_snapshot('threshold_clear')
  end subroutine threshold_fixture

  subroutine lifecycle_fixture()
    integer(int64) :: key(6)
    ! New lifecycle owners must not retain the old 5 / 2 anchor identities.
    call SPOT1P64_CACHE_BEGIN(declared_groups,.false.,.true.)
    call stats_snapshot('lifecycle_begin')
    call guard_capture('lifecycle_p1_owner9',9,1,base2)
    call guard_capture('lifecycle_p1_group3_zero',3,1,base2)
    call guard_capture('lifecycle_p2_owner3',3,2,base1)
    call mutated(base1,1,key)
    call guard_capture('lifecycle_p2_group9_delta',9,2,key)
    SPOT1P64_PLAN(9)%mode(1)%ready=.true.
    call guard_capture('lifecycle_ready_hit',9,2,key)
    call SPOT1P64_CACHE_CLEAR()
    call stats_snapshot('lifecycle_clear')
    call SPOT1P64_CACHE_BEGIN(declared_groups,.false.,.false.)
    call stats_snapshot('disabled_begin')
    call guard_capture('disabled_phase1',1,1,base1)
    call guard_capture('disabled_phase2',1,2,base2)
    call SPOT1P64_CACHE_CLEAR()
    call stats_snapshot('disabled_clear')
  end subroutine lifecycle_fixture

  subroutine negative_fixture(which,phase)
    character(len=*), intent(in) :: which
    integer, intent(in) :: phase
    integer :: owner,out
    logical :: active,load_operation
    integer(int64) :: key(6),base(6),seed(6)
    integer(int64), allocatable :: attempted(:),output(:)
    character(len=:), allocatable :: label
    select case(which)
    case('unchanged_word','difference_word','stored_difference_word','base_word', &
         'input_length','load_length','ineligible_existing','corrupt_index_zero', &
         'corrupt_index_high','missing_anchor')
    case default
      stop 2
    end select
    call SPOT1P64_CACHE_BEGIN(declared_groups,.false.,.true.)
    call stats_snapshot('negative_begin')
    call guard_capture('negative_p1_owner5',5,1,base1)
    call guard_capture('negative_p1_owner7_prerequisite',7,1,base1)
    call mutated(base1,1,seed)
    call guard_capture('negative_p1_target2',2,1,seed)
    call guard_capture('negative_p2_owner7',7,2,base2)
    call guard_capture('negative_p2_group5_zero',5,2,base2)
    call mutated(base2,1,seed)
    call guard_capture('negative_p2_target2',2,2,seed)
    if (phase == 1) then
      base=base1; owner=5
    else
      base=base2; owner=7
    endif
    call mutated(base,1,key)
    attempted=key
    allocate(output(6))
    load_operation=.false.
    select case(which)
    case('unchanged_word')
      attempted(2)=ieor(attempted(2),1_int64)
    case('difference_word')
      attempted(1)=ieor(attempted(1),2_int64)
    case('stored_difference_word')
      if (phase == 1) then
        SPOT1P64_PLAN(2)%mode(1)%rank1_raw_bits(1)= &
          ieor(SPOT1P64_PLAN(2)%mode(1)%rank1_raw_bits(1),2_int64)
      else
        SPOT1P64_PLAN(2)%mode(1)%rank1_operator_bits(1)= &
          ieor(SPOT1P64_PLAN(2)%mode(1)%rank1_operator_bits(1),2_int64)
      endif
    case('base_word')
      if (phase == 1) then
        SPOT1P64_PLAN(owner)%mode(1)%rank1_raw_bits(2)= &
          ieor(SPOT1P64_PLAN(owner)%mode(1)%rank1_raw_bits(2),1_int64)
      else
        SPOT1P64_PLAN(owner)%mode(1)%rank1_operator_bits(2)= &
          ieor(SPOT1P64_PLAN(owner)%mode(1)%rank1_operator_bits(2),1_int64)
      endif
    case('input_length')
      deallocate(attempted)
      allocate(attempted(7))
      attempted(:6)=key; attempted(7)=17_int64
    case('load_length')
      deallocate(output)
      allocate(output(7))
      load_operation=.true.
    case('ineligible_existing')
      continue
    case('corrupt_index_zero','corrupt_index_high')
      if (phase == 1) then
        SPOT1P64_PLAN(2)%mode(1)%rank1_raw_positions(1)=0_int32
        if (which == 'corrupt_index_high') &
          SPOT1P64_PLAN(2)%mode(1)%rank1_raw_positions(1)=7_int32
      else
        SPOT1P64_PLAN(2)%mode(1)%rank1_operator_positions(1)=0_int32
        if (which == 'corrupt_index_high') &
          SPOT1P64_PLAN(2)%mode(1)%rank1_operator_positions(1)=7_int32
      endif
      load_operation=.true.
    case('missing_anchor')
      if (phase == 1) then
        deallocate(SPOT1P64_PLAN(owner)%mode(1)%rank1_raw_bits)
      else
        deallocate(SPOT1P64_PLAN(owner)%mode(1)%rank1_operator_bits)
      endif
      load_operation=.true.
    end select
    label='negative_'//trim(which)//'_p'//number(int(phase,int64))
    ! Malformed representation is archived without invoking LOAD first.
    call key_snapshot(label//'_attempt',2,phase,attempted,.false.,.false.)
    write(manifest,'(A)') '{"kind":"negative_expected","case":"'//label// &
      '","expected_XABORT":"'//identity_message//'","expected_exit":23,'// &
      '"operation":"'//trim(merge('load ','guard',load_operation))//'","output_words":'// &
      number(size(output,kind=int64))//'}'
    flush(manifest)
    close(manifest)
    rejection_expected=.true.
    if (load_operation) then
      call SPOT1P64_RANK1_KEY_LOAD(2,phase,output)
    else
      call SPOT1P64_RANK1_GUARD(2,attempted,phase,which /= 'ineligible_existing',active)
    endif
    open(newunit=out,file='unexpected_return.txt',status='new',action='write')
    write(out,'(A)') 'Actual key operation unexpectedly returned after declared mutation.'
    close(out)
    stop 1
  end subroutine negative_fixture
end program keycodec_controls

subroutine XABORT(message)
  use keycodec_abort_state
  implicit none
  character(len=*), intent(in) :: message
  integer :: out
  open(newunit=out,file='actual_xabort.txt',status='new',action='write')
  write(out,'(A)') trim(message)
  close(out)
  write(*,'(A)') 'ACTUAL_XABORT='//trim(message)
  if (rejection_expected .and. trim(message) == identity_message) stop 23
  stop 97
end subroutine XABORT
