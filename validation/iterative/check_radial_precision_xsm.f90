program check_radial_precision_xsm
  ! Read-only audit of the binary32 lattice distance between each retained
  ! radial scalar-flux value in the bounded radial-floor probes.
  !
  ! This program does not evaluate an equation residual and does not apply
  ! an acceptance threshold.  For positive finite IEEE binary32 values,
  ! the difference between their positive integer bit patterns is exactly
  ! the number of adjacent representable values separating them.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: expected_groups=370
  integer, parameter :: expected_regions=8
  integer, parameter :: max_xsm_path=72
  integer, parameter :: nargs=5

  type :: radial_layout
    integer :: nregion=0
    integer :: nunknown=0
    integer, allocatable :: keyflux(:)
  end type radial_layout

  type :: flux_state
    real(real32), allocatable :: flux(:,:)
  end type flux_state

  type :: step_result
    integer(int64), allocatable :: steps(:)
    integer(int64) :: unchanged=0_int64
    integer(int64) :: upward=0_int64
    integer(int64) :: downward=0_int64
    integer(int64) :: adjacent=0_int64
    integer(int64) :: max_steps=-1_int64
  end type step_result

  character(len=1024) :: path(nargs)
  character(len=1024) :: mode
  type(radial_layout) :: layout
  type(flux_state) :: native_pre,native_post
  type(flux_state) :: stationary_pre,stationary_post
  type(step_result) :: native,stationary
  integer :: i,j

  if (command_argument_count() == 1) then
    call get_command_argument(1,mode)
    if (trim(mode) /= 'SELFTEST') call fail('INVALID ONE-ARGUMENT MODE.')
    call self_test()
    write(6,'(A)') 'RADIAL-PRECISION-XSM SELFTEST PASS'
    stop
  endif
  if (command_argument_count() /= nargs) &
    call fail('EXPECTED TRACK AND FOUR PROBE XSM ARGUMENTS.')

  do i=1,nargs
    call get_command_argument(i,path(i))
    if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(path(i)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    do j=1,i-1
      if (trim(path(i)) == trim(path(j))) &
        call fail('XSM PATH ARGUMENTS MUST BE DISTINCT.')
    enddo
  enddo

  call load_track(trim(path(1)),layout)
  call load_flux(trim(path(2)),'NATIVE PRE',layout,native_pre)
  call load_flux(trim(path(3)),'NATIVE POST',layout,native_post)
  call load_flux(trim(path(4)),'STATIONARY PRE',layout,stationary_pre)
  call load_flux(trim(path(5)),'STATIONARY POST',layout,stationary_post)
  call compute_steps(native_pre,native_post,layout,native)
  call compute_steps(stationary_pre,stationary_post,layout,stationary)

  write(6,'(A,3(1X,I0))') 'RADIAL-PRECISION-XSM DIMS', &
    expected_groups,layout%nregion,layout%nunknown
  write(6,'(A)') &
    'RADIAL-PRECISION-XSM QUANTITY EXACT-BINARY32-REPRESENTABLE-STEPS'
  write(6,'(A)') 'RADIAL-PRECISION-XSM SCOPE RETAINED-SCALAR-FLUX'
  call print_result('NATIVE',native,native_pre,native_post,layout)
  call print_result('STATIONARY',stationary,stationary_pre, &
    stationary_post,layout)
  write(6,'(A)') 'RADIAL-PRECISION-XSM COMPLETE'

contains

  subroutine load_track(xsm_path,data)
    character(len=*), intent(in) :: xsm_path
    type(radial_layout), intent(out) :: data
    type(c_ptr) :: root
    character(len=12) :: track_type
    integer :: state(nstate),length_found,type_found
    integer, allocatable :: key_all(:)

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_TRACK','TRACK')
    call require_record(root,'TRACK-TYPE',3,3,'TRACK')
    call LCMGTC(root,'TRACK-TYPE',12,track_type)
    if (trim(track_type) /= 'MCCG') &
      call fail('TRACK DOES NOT SELECT MCCG.')
    call require_record(root,'STATE-VECTOR',nstate,1,'TRACK')
    call LCMGET(root,'STATE-VECTOR',state)
    data%nregion=state(1)
    data%nunknown=state(2)
    if ((data%nregion /= expected_regions).or.(data%nunknown <= 0)) &
      call fail('TRACK DIMENSIONS DO NOT MATCH THE FROZEN DIAGNOSTIC.')

    call LCMLEN(root,'KEYFLX$ANIS',length_found,type_found)
    if ((length_found < data%nregion).or.(type_found /= 1)) &
      call fail('TRACK HAS AN INVALID KEYFLX$ANIS RECORD.')
    allocate(key_all(length_found),data%keyflux(data%nregion))
    call LCMGET(root,'KEYFLX$ANIS',key_all)
    data%keyflux=key_all(1:data%nregion)
    if (any(data%keyflux <= 0).or. &
        any(data%keyflux > data%nunknown)) &
      call fail('TRACK HAS AN INVALID REGION FLUX KEY.')
    if (has_duplicate(data%keyflux)) &
      call fail('TRACK REGION FLUX KEYS ARE NOT UNIQUE.')

    deallocate(key_all)
    call LCMCL(root,1)
  end subroutine load_track


  subroutine load_flux(xsm_path,owner,data,state_data)
    character(len=*), intent(in) :: xsm_path,owner
    type(radial_layout), intent(in) :: data
    type(flux_state), intent(out) :: state_data
    type(c_ptr) :: root,flux_groups
    integer :: state(nstate),group

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_FLUX',owner)
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= expected_groups).or. &
        (state(2) /= data%nunknown)) &
      call fail(trim(owner)//' FLUX DIMENSIONS DO NOT MATCH TRACK.')

    allocate(state_data%flux(data%nunknown,expected_groups))
    call require_record(root,'FLUX',expected_groups,10,owner)
    flux_groups=LCMGID(root,'FLUX')
    do group=1,expected_groups
      call require_list_item(flux_groups,group,data%nunknown,2, &
        trim(owner)//' FLUX GROUP')
      call LCMGDL(flux_groups,group,state_data%flux(:,group))
    enddo
    if (any(.not.ieee_is_finite(state_data%flux))) &
      call fail(trim(owner)//' CONTAINS NON-FINITE FLUX.')

    call LCMCL(root,1)
  end subroutine load_flux


  subroutine compute_steps(pre,post,data,result)
    type(flux_state), intent(in) :: pre,post
    type(radial_layout), intent(in) :: data
    type(step_result), intent(out) :: result
    integer :: group,region,key,index
    integer(int32) :: pre_bits,post_bits
    integer(int64) :: signed_distance,absolute_distance
    logical :: any_positive

    result%unchanged=0_int64
    result%upward=0_int64
    result%downward=0_int64
    result%adjacent=0_int64
    result%max_steps=-1_int64
    allocate(result%steps(expected_groups*data%nregion))
    index=0
    any_positive=.false.
    do group=1,expected_groups
      do region=1,data%nregion
        index=index+1
        key=data%keyflux(region)
        pre_bits=real32_bits(pre%flux(key,group))
        post_bits=real32_bits(post%flux(key,group))
        if ((.not.positive_finite_bits(pre_bits)).or. &
            (.not.positive_finite_bits(post_bits))) &
          call fail('SCALAR FLUX MUST BE POSITIVE FINITE BINARY32.')
        any_positive=.true.
        signed_distance=signed_positive_ulp_steps(pre%flux(key,group), &
          post%flux(key,group))
        absolute_distance=abs(signed_distance)
        result%steps(index)=signed_distance
        if (signed_distance == 0_int64) then
          result%unchanged=result%unchanged+1_int64
        else
          if (absolute_distance == 1_int64) &
            result%adjacent=result%adjacent+1_int64
          if (signed_distance > 0_int64) then
            result%upward=result%upward+1_int64
          else
            result%downward=result%downward+1_int64
          endif
        endif
        result%max_steps=max(result%max_steps,absolute_distance)
      enddo
    enddo
    if (.not.any_positive) call fail('SCALAR FLUX IS IDENTICALLY ZERO.')
    if (index /= size(result%steps)) call fail('INTERNAL CENSUS FAILURE.')
    if (result%unchanged+result%upward+result%downward /= index) &
      call fail('STEP DIRECTION CENSUS FAILURE.')
    if ((result%max_steps < 0_int64).or. &
        (result%adjacent > result%upward+result%downward)) &
      call fail('STEP SUMMARY FAILURE.')
  end subroutine compute_steps


  subroutine print_result(arm,result,pre,post,data)
    character(len=*), intent(in) :: arm
    type(step_result), intent(in) :: result
    type(flux_state), intent(in) :: pre,post
    type(radial_layout), intent(in) :: data
    integer(int64), allocatable :: sorted(:)
    integer(int64) :: signed_distance
    integer(int32) :: pre_bits,post_bits
    integer :: first,last,total,index,group,region,key

    total=size(result%steps)
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'TOTAL',total
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'UNCHANGED',result%unchanged
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'UPWARD',result%upward
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'DOWNWARD',result%downward
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'ADJACENT',result%adjacent
    write(6,'(A,1X,A,1X,A,1X,I0)') &
      'RADIAL-PRECISION-XSM',trim(arm),'MAX-STEPS',result%max_steps
    if (result%unchanged == total) then
      write(6,'(A,1X,A,1X,A)') &
        'RADIAL-PRECISION-XSM',trim(arm),'ALL-BITS-IDENTICAL'
    else
      write(6,'(A,1X,A,1X,A)') &
        'RADIAL-PRECISION-XSM',trim(arm),'NONIDENTICAL'
    endif

    allocate(sorted(total))
    sorted=result%steps
    call sort_int64(sorted)
    first=1
    do while (first <= total)
      last=first
      do while (last < total)
        if (sorted(last+1) /= sorted(first)) exit
        last=last+1
      enddo
      write(6,'(A,1X,A,1X,A,2(1X,I0))') &
        'RADIAL-PRECISION-XSM',trim(arm),'HIST', &
        sorted(first),last-first+1
      first=last+1
    enddo
    deallocate(sorted)

    index=0
    do group=1,expected_groups
      do region=1,data%nregion
        index=index+1
        key=data%keyflux(region)
        signed_distance=result%steps(index)
        pre_bits=real32_bits(pre%flux(key,group))
        post_bits=real32_bits(post%flux(key,group))
        write(6,'(A,1X,A,1X,A,3(1X,I0),2(1X,Z8.8),2(1X,I0))') &
          'RADIAL-PRECISION-XSM',trim(arm),'LEDGER', &
          group,region,key,pre_bits,post_bits,signed_distance, &
          abs(signed_distance)
        if (abs(signed_distance) == result%max_steps) then
          write(6,'(A,1X,A,1X,A,3(1X,I0))') &
            'RADIAL-PRECISION-XSM',trim(arm),'MAX-TIE', &
            group,region,signed_distance
        endif
      enddo
    enddo
  end subroutine print_result


  subroutine sort_int64(values)
    integer(int64), intent(inout) :: values(:)
    integer(int64) :: held
    integer :: i,j

    do i=2,size(values)
      held=values(i)
      j=i-1
      do while (j >= 1)
        if (values(j) <= held) exit
        values(j+1)=values(j)
        j=j-1
      enddo
      values(j+1)=held
    enddo
  end subroutine sort_int64


  subroutine self_test()
    real(real32) :: one,next_one,next_two,smallest
    real(real32) :: max_subnormal,min_normal,below_one,max_finite
    integer(int32) :: positive_infinity,quiet_nan

    one=1.0_real32
    next_one=nearest(one,1.0_real32)
    next_two=nearest(next_one,1.0_real32)
    smallest=transfer(1_int32,0.0_real32)
    max_subnormal=transfer(int(z'007FFFFF',int32),0.0_real32)
    min_normal=transfer(int(z'00800000',int32),0.0_real32)
    below_one=transfer(int(z'3F7FFFFF',int32),0.0_real32)
    max_finite=transfer(int(z'7F7FFFFF',int32),0.0_real32)
    positive_infinity=int(z'7F800000',int32)
    quiet_nan=int(z'7FC00000',int32)

    if (real32_bits(one) /= int(z'3F800000',int32)) &
      call fail('SELFTEST IEEE ONE ENCODING FAILURE.')
    if (real32_bits(tiny(one)) /= int(z'00800000',int32)) &
      call fail('SELFTEST IEEE TINY ENCODING FAILURE.')
    if (real32_bits(huge(one)) /= int(z'7F7FFFFF',int32)) &
      call fail('SELFTEST IEEE HUGE ENCODING FAILURE.')
    if (signed_positive_ulp_steps(one,one) /= 0_int64) &
      call fail('SELFTEST IDENTICAL FAILURE.')
    if (signed_positive_ulp_steps(one,next_one) /= 1_int64) &
      call fail('SELFTEST ADJACENT FAILURE.')
    if (signed_positive_ulp_steps(next_two,one) /= -2_int64) &
      call fail('SELFTEST SIGNED TWO-STEP FAILURE.')
    if (signed_positive_ulp_steps(smallest, &
        transfer(2_int32,0.0_real32)) /= 1_int64) &
      call fail('SELFTEST SUBNORMAL ADJACENCY FAILURE.')
    if (signed_positive_ulp_steps(max_subnormal,min_normal) /= 1_int64) &
      call fail('SELFTEST SUBNORMAL-NORMAL BOUNDARY FAILURE.')
    if (signed_positive_ulp_steps(below_one,one) /= 1_int64) &
      call fail('SELFTEST BINade BOUNDARY FAILURE.')
    if ((one-below_one) == (next_one-one)) &
      call fail('SELFTEST BINade GAP ASYMMETRY FAILURE.')
    if ((.not.positive_finite_bits(real32_bits(max_finite))).or. &
        positive_finite_bits(0_int32).or. &
        positive_finite_bits(int(z'80000000',int32)).or. &
        positive_finite_bits(positive_infinity).or. &
        positive_finite_bits(quiet_nan)) &
      call fail('SELFTEST POSITIVE-FINITE CLASSIFICATION FAILURE.')
    call self_test_layout()
  end subroutine self_test


  subroutine self_test_layout()
    type(radial_layout) :: data
    type(flux_state) :: pre,post
    type(step_result) :: result
    integer(int32) :: bits
    integer(int64) :: expected_step
    integer(int64) :: unchanged,upward,downward,adjacent
    integer :: group,region,key,index

    data%nregion=3
    data%nunknown=7
    allocate(data%keyflux(data%nregion))
    data%keyflux=[5,2,7]
    allocate(pre%flux(data%nunknown,expected_groups))
    allocate(post%flux(data%nunknown,expected_groups))
    pre%flux=1.0_real32
    post%flux=1.0_real32
    unchanged=0_int64
    upward=0_int64
    downward=0_int64
    adjacent=0_int64
    index=0
    do group=1,expected_groups
      post%flux(1,group)=transfer( &
        real32_bits(pre%flux(1,group))+1000_int32,0.0_real32)
      do region=1,data%nregion
        index=index+1
        key=data%keyflux(region)
        bits=int(z'3F000000',int32)+int(8*group+region,int32)
        expected_step=int(mod(group+2*region,5)-2,int64)
        pre%flux(key,group)=transfer(bits,0.0_real32)
        post%flux(key,group)=transfer(bits+int(expected_step,int32), &
          0.0_real32)
        if (expected_step == 0_int64) then
          unchanged=unchanged+1_int64
        else if (expected_step > 0_int64) then
          upward=upward+1_int64
        else
          downward=downward+1_int64
        endif
        if (abs(expected_step) == 1_int64) adjacent=adjacent+1_int64
      enddo
    enddo

    call compute_steps(pre,post,data,result)
    if ((result%unchanged /= unchanged).or. &
        (result%upward /= upward).or. &
        (result%downward /= downward).or. &
        (result%adjacent /= adjacent).or. &
        (result%max_steps /= 2_int64)) &
      call fail('SELFTEST PERMUTED-LAYOUT SUMMARY FAILURE.')
    index=0
    do group=1,expected_groups
      do region=1,data%nregion
        index=index+1
        expected_step=int(mod(group+2*region,5)-2,int64)
        if (result%steps(index) /= expected_step) &
          call fail('SELFTEST GROUP-REGION-KEY LAYOUT FAILURE.')
      enddo
    enddo
  end subroutine self_test_layout


  pure integer(int64) function signed_positive_ulp_steps(left,right)
    real(real32), intent(in) :: left,right

    signed_positive_ulp_steps=int(real32_bits(right),int64)- &
      int(real32_bits(left),int64)
  end function signed_positive_ulp_steps


  pure logical function positive_finite_bits(bits)
    integer(int32), intent(in) :: bits

    positive_finite_bits=(bits > 0_int32).and. &
      (iand(bits,int(z'7F800000',int32)) /= int(z'7F800000',int32))
  end function positive_finite_bits


  subroutine require_signature(ptr,expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: expected,owner
    character(len=12) :: signature

    call require_record(ptr,'SIGNATURE',3,3,owner)
    call LCMGTC(ptr,'SIGNATURE',12,signature)
    if (signature /= expected) &
      call fail(trim(owner)//' INVALID SIGNATURE.')
  end subroutine require_signature


  subroutine require_record(ptr,name,length_expected,type_expected,owner)
    type(c_ptr), intent(in) :: ptr
    character(len=*), intent(in) :: name,owner
    integer, intent(in) :: length_expected,type_expected
    integer :: length_found,type_found

    call LCMLEN(ptr,name,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,A,4(1X,I0))') trim(owner)//' INVALID RECORD', &
        trim(name),length_found,type_found,length_expected,type_expected
      call fail('RECORD CONTRACT FAILURE.')
    endif
  end subroutine require_record


  subroutine require_list_item(ptr,index,length_expected,type_expected, &
      owner)
    type(c_ptr), intent(in) :: ptr
    integer, intent(in) :: index,length_expected,type_expected
    character(len=*), intent(in) :: owner
    integer :: length_found,type_found

    call LCMLEL(ptr,index,length_found,type_found)
    if ((length_found /= length_expected).or. &
        (type_found /= type_expected)) then
      write(0,'(A,1X,I0,4(1X,I0))') &
        trim(owner)//' INVALID LIST ITEM',index,length_found,type_found, &
        length_expected,type_expected
      call fail('LIST ITEM CONTRACT FAILURE.')
    endif
  end subroutine require_list_item


  pure logical function has_duplicate(values)
    integer, intent(in) :: values(:)
    integer :: left,right

    has_duplicate=.false.
    do left=1,size(values)-1
      do right=left+1,size(values)
        if (values(left) == values(right)) then
          has_duplicate=.true.
          return
        endif
      enddo
    enddo
  end function has_duplicate


  pure elemental integer(int32) function real32_bits(value)
    real(real32), intent(in) :: value

    real32_bits=transfer(value,0_int32)
  end function real32_bits


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(0,'(A)') 'RADIAL-PRECISION-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_radial_precision_xsm
