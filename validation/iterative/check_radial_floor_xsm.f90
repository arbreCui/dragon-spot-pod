program check_radial_floor_xsm
  ! Independent, Ganlib-only, read-only audit of the bounded radial-floor
  ! diagnostic.
  !
  ! Arguments:
  !   PREPARED: track source system cap PREPARED
  !   FINAL:    track source system cap
  !             native_pre native_post stationary_pre stationary_post
  !
  ! TRACK, SOURCE, and SYSTEM are the common immutable inputs.  CAP and the
  ! four arm objects are L_FLUX objects.  Every object must carry a bitwise
  ! copy of frozen SPOT-QFISS and SPOT-FS-K.  The forensic CAP leakage
  ! metadata is excluded because the returned-axial SPOLEAK call replaced it
  ! with L1 after the cap solve; SYSTEM retains the actual L0 solve input.
  ! In final mode the four new solver outputs must carry SYSTEM/SPOT-LEAK1D
  ! bit for bit.  PREPARED mode reads no surrogate solver outputs and
  ! performs only the pre-solve structural and source checks.  For each arm,
  ! PRE is phi and POST is one step T(phi).
  !
  ! The two reported fixed-point defects are input-normalized:
  !
  !   D-V2  = sqrt(sum_g sum_r V_r (post-pre)^2)
  !           / sqrt(sum_g sum_r V_r pre^2)
  !
  !   D-MAX = max_g,r |post-pre| / max_g,r |pre|.
  !
  ! All arithmetic in these reductions is binary64 and the specified loop
  ! order is group-major, region-minor.  They are one-step fixed-point
  ! defects, without an equation-residual or error-bound interpretation.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  use, intrinsic :: iso_c_binding, only : c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,real32,real64
  implicit none

  integer, parameter :: nstate=40
  integer, parameter :: expected_groups=370
  integer, parameter :: expected_regions=8
  integer, parameter :: max_xsm_path=72
  integer, parameter :: nargs=8
  integer, parameter :: nflux=5

  type :: frozen_input
    integer :: ngroup=0
    integer :: nregion=0
    integer :: nunknown=0
    integer, allocatable :: material(:)
    integer, allocatable :: keyflux(:)
    real(real32), allocatable :: volume(:)
    real(real32), allocatable :: qfiss(:,:)
    real(real32), allocatable :: leakage(:)
    real(real32) :: source_keff=0.0_real32
  end type frozen_input

  type :: flux_state
    real(real32), allocatable :: flux(:,:)
  end type flux_state

  type :: defect_result
    real(real64) :: v2_numerator=0.0_real64
    real(real64) :: v2_denominator=0.0_real64
    real(real64) :: d_v2=0.0_real64
    real(real64) :: max_numerator=0.0_real64
    real(real64) :: max_denominator=0.0_real64
    real(real64) :: d_max=0.0_real64
    integer :: delta_group=0
    integer :: delta_region=0
    integer :: input_group=0
    integer :: input_region=0
  end type defect_result

  character(len=1024) :: path(nargs)
  character(len=16) :: mode
  character(len=16), parameter :: flux_owner(nflux) = &
    [character(len=16) :: 'CAP','NATIVE PRE','NATIVE POST', &
      'STATIONARY PRE','STATIONARY POST']
  type(frozen_input) :: frozen
  type(flux_state) :: flux(nflux)
  type(defect_result) :: native,stationary
  integer :: argument_count,input_count,i,j
  logical :: prepared_mode

  argument_count=command_argument_count()
  select case(argument_count)
  case(5)
    call get_command_argument(5,mode)
    if (trim(mode) /= 'PREPARED') call fail('INVALID CHECKER MODE.')
    prepared_mode=.true.
    input_count=4
  case(nargs)
    prepared_mode=.false.
    input_count=nargs
  case default
    call fail('EXPECTED FOUR XSM ARGUMENTS PLUS PREPARED, OR EIGHT XSM ARGUMENTS.')
  end select
  do i=1,input_count
    call get_command_argument(i,path(i))
    if (len_trim(path(i)) == 0) call fail('EMPTY XSM PATH ARGUMENT.')
    if (len_trim(path(i)) > max_xsm_path) &
      call fail('XSM PATH ARGUMENT EXCEEDS GANLIB LIMIT.')
    do j=1,i-1
      if (trim(path(i)) == trim(path(j))) &
        call fail('XSM PATH ARGUMENTS MUST BE DISTINCT.')
    enddo
  enddo

  call load_track(trim(path(1)),frozen)
  call load_source(trim(path(2)),frozen)
  call load_system(trim(path(3)),frozen)
  call load_flux(trim(path(4)),trim(flux_owner(1)),frozen,flux(1),.false.)
  if (.not.prepared_mode) then
    do i=2,nflux
      call load_flux(trim(path(i+3)),trim(flux_owner(i)),frozen,flux(i), &
        .true.)
    enddo
    call compute_defect(flux(2),flux(3),frozen,native)
    call compute_defect(flux(4),flux(5),frozen,stationary)
  endif

  write(6,'(A,3(1X,I0))') 'RADIAL-FLOOR-XSM DIMS', &
    frozen%ngroup,frozen%nregion,frozen%nunknown
  write(6,'(A)') 'RADIAL-FLOOR-XSM SOURCE-METADATA BITWISE PASS'
  write(6,'(A)') 'RADIAL-FLOOR-XSM CAP LEAKAGE-METADATA EXCLUDED'
  if (prepared_mode) then
    write(6,'(A)') 'RADIAL-FLOOR-XSM PREPARED NO SOLVER OUTPUTS'
  else
    write(6,'(A)') &
      'RADIAL-FLOOR-XSM SOLVER-OUTPUT LEAKAGE-METADATA BITWISE PASS'
    write(6,'(A)') &
      'RADIAL-FLOOR-XSM QUANTITY ONE-STEP PRODUCTION-MAP FIXED-POINT DEFECT'
    write(6,'(A)') 'RADIAL-FLOOR-XSM ORDER GROUP-MAJOR REGION-MINOR'
    call print_defect('NATIVE',native)
    call print_defect('STATIONARY',stationary)
  endif
  write(6,'(A)') 'RADIAL-FLOOR-XSM COMPLETE'

contains

  subroutine load_track(xsm_path,data)
    character(len=*), intent(in) :: xsm_path
    type(frozen_input), intent(inout) :: data
    type(c_ptr) :: root
    character(len=12) :: track_type
    integer :: state(nstate),length_found,type_found
    integer, allocatable :: key_all(:)

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_TRACK','TRACK')
    call require_record(root,'TRACK-TYPE',3,3,'TRACK')
    call LCMGTC(root,'TRACK-TYPE',12,track_type)
    if (trim(track_type) /= 'MCCG') &
      call fail('TRACK DOES NOT SELECT THE MCCG PRODUCTION DOOR.')
    call require_record(root,'STATE-VECTOR',nstate,1,'TRACK')
    call LCMGET(root,'STATE-VECTOR',state)
    data%nregion=state(1)
    data%nunknown=state(2)
    if ((data%nregion /= expected_regions).or.(data%nunknown <= 0)) &
      call fail('TRACK DIMENSIONS DO NOT MATCH THE FROZEN DIAGNOSTIC.')

    allocate(data%material(data%nregion))
    allocate(data%keyflux(data%nregion))
    allocate(data%volume(data%nregion))
    call require_record(root,'MATCOD',data%nregion,1,'TRACK')
    call require_record(root,'VOLUME',data%nregion,2,'TRACK')
    call LCMLEN(root,'KEYFLX$ANIS',length_found,type_found)
    if ((length_found < data%nregion).or.(type_found /= 1)) &
      call fail('TRACK INVALID KEYFLX$ANIS RECORD.')
    allocate(key_all(length_found))
    call LCMGET(root,'MATCOD',data%material)
    call LCMGET(root,'VOLUME',data%volume)
    call LCMGET(root,'KEYFLX$ANIS',key_all)
    data%keyflux=key_all(1:data%nregion)

    if (any(data%material <= 0)) &
      call fail('TRACK CONTAINS AN INACTIVE RADIAL REGION.')
    if (any(data%keyflux <= 0).or. &
        any(data%keyflux > data%nunknown)) &
      call fail('TRACK CONTAINS AN INVALID REGION FLUX KEY.')
    if (has_duplicate(data%keyflux)) &
      call fail('TRACK REGION FLUX KEYS ARE NOT UNIQUE.')
    if (any(.not.ieee_is_finite(data%volume)).or. &
        any(data%volume <= 0.0_real32)) &
      call fail('TRACK CONTAINS AN INVALID REGION VOLUME.')

    deallocate(key_all)
    call LCMCL(root,1)
  end subroutine load_track


  subroutine load_source(xsm_path,data)
    character(len=*), intent(in) :: xsm_path
    type(frozen_input), intent(inout) :: data
    type(c_ptr) :: root,source_outer,source_groups
    integer :: state(nstate),marker,group
    real(real32), allocatable :: qint(:)

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_SOURCE','SOURCE')
    call require_record(root,'STATE-VECTOR',nstate,1,'SOURCE')
    call LCMGET(root,'STATE-VECTOR',state)
    data%ngroup=state(1)
    if ((data%ngroup /= expected_groups).or. &
        (state(2) /= data%nunknown).or.(state(3) /= 1)) &
      call fail('SOURCE DIMENSIONS DO NOT MATCH TRACK.')

    call require_record(root,'SPOT-FROZEN',1,1,'SOURCE')
    call require_record(root,'SPOT-KEFF',1,2,'SOURCE')
    call require_record(root,'SPOT-QINT',data%ngroup,2,'SOURCE')
    call require_record(root,'DSOUR',1,10,'SOURCE')
    call LCMGET(root,'SPOT-FROZEN',marker)
    call LCMGET(root,'SPOT-KEFF',data%source_keff)
    if (marker /= 1) call fail('SOURCE IS NOT MARKED FROZEN.')
    if ((.not.ieee_is_finite(data%source_keff)).or. &
        (data%source_keff <= 0.0_real32)) &
      call fail('SOURCE HAS AN INVALID SPOT-KEFF.')

    allocate(qint(data%ngroup))
    allocate(data%qfiss(data%nunknown,data%ngroup))
    call LCMGET(root,'SPOT-QINT',qint)
    if (any(.not.ieee_is_finite(qint)).or. &
        (sum(real(qint,real64)) <= 0.0_real64)) &
      call fail('SOURCE HAS AN INVALID SPOT-QINT.')
    source_outer=LCMGID(root,'DSOUR')
    call require_list_item(source_outer,1,data%ngroup,10, &
      'SOURCE DSOUR OUTER')
    source_groups=LCMGIL(source_outer,1)
    do group=1,data%ngroup
      call require_list_item(source_groups,group,data%nunknown,2, &
        'SOURCE DSOUR GROUP')
      call LCMGDL(source_groups,group,data%qfiss(:,group))
    enddo
    if (any(.not.ieee_is_finite(data%qfiss)).or. &
        any(data%qfiss < 0.0_real32).or. &
        (maxval(data%qfiss) <= 0.0_real32)) &
      call fail('SOURCE HAS AN INVALID FROZEN FISSION SOURCE.')

    deallocate(qint)
    call LCMCL(root,1)
  end subroutine load_source


  subroutine load_system(xsm_path,data)
    character(len=*), intent(in) :: xsm_path
    type(frozen_input), intent(inout) :: data
    type(c_ptr) :: root
    integer :: state(nstate)

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_PIJ','SYSTEM')
    call require_record(root,'STATE-VECTOR',nstate,1,'SYSTEM')
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(8) /= data%ngroup).or. &
        (state(9) /= data%nunknown)) &
      call fail('SYSTEM DIMENSIONS DO NOT MATCH TRACK AND SOURCE.')
    allocate(data%leakage(data%ngroup))
    call require_record(root,'SPOT-LEAK1D',data%ngroup,2,'SYSTEM')
    call LCMGET(root,'SPOT-LEAK1D',data%leakage)
    if (any(.not.ieee_is_finite(data%leakage))) &
      call fail('SYSTEM HAS NON-FINITE SPOT-LEAK1D.')
    call LCMCL(root,1)
  end subroutine load_system


  subroutine load_flux(xsm_path,owner,data,state_data,check_leakage)
    character(len=*), intent(in) :: xsm_path,owner
    type(frozen_input), intent(in) :: data
    type(flux_state), intent(out) :: state_data
    logical, intent(in) :: check_leakage
    type(c_ptr) :: root,flux_groups,q_outer,q_groups
    integer :: state(nstate),marker,group
    real(real32), allocatable :: qfiss(:,:),leakage(:)
    real(real32) :: source_keff

    call LCMOP(root,xsm_path,2,2,0)
    call require_signature(root,'L_FLUX',owner)
    call require_record(root,'STATE-VECTOR',nstate,1,owner)
    call LCMGET(root,'STATE-VECTOR',state)
    if ((state(1) /= data%ngroup).or. &
        (state(2) /= data%nunknown)) &
      call fail(trim(owner)//' FLUX DIMENSIONS DO NOT MATCH INPUTS.')

    allocate(state_data%flux(data%nunknown,data%ngroup))
    call require_record(root,'FLUX',data%ngroup,10,owner)
    flux_groups=LCMGID(root,'FLUX')
    do group=1,data%ngroup
      call require_list_item(flux_groups,group,data%nunknown,2, &
        trim(owner)//' FLUX GROUP')
      call LCMGDL(flux_groups,group,state_data%flux(:,group))
    enddo
    if (any(.not.ieee_is_finite(state_data%flux))) &
      call fail(trim(owner)//' CONTAINS NON-FINITE FLUX.')

    call require_record(root,'SPOT-FS-EQN',1,1,owner)
    call require_record(root,'SPOT-FS-K',1,2,owner)
    call require_record(root,'SPOT-LEAK1D',data%ngroup,2,owner)
    call require_record(root,'SPOT-QFISS',1,10,owner)
    call LCMGET(root,'SPOT-FS-EQN',marker)
    call LCMGET(root,'SPOT-FS-K',source_keff)
    if (marker /= 1) &
      call fail(trim(owner)//' HAS AN INVALID SPOT-FS-EQN MARKER.')
    if (real32_bits(source_keff) /= real32_bits(data%source_keff)) &
      call fail(trim(owner)//' SPOT-FS-K DIFFERS BITWISE.')

    allocate(leakage(data%ngroup))
    allocate(qfiss(data%nunknown,data%ngroup))
    call LCMGET(root,'SPOT-LEAK1D',leakage)
    if (any(.not.ieee_is_finite(leakage))) &
      call fail(trim(owner)//' HAS NON-FINITE SPOT-LEAK1D.')
    if (check_leakage.and. &
        any(real32_bits(leakage) /= real32_bits(data%leakage))) &
      call fail(trim(owner)//' SPOT-LEAK1D DIFFERS BITWISE.')
    q_outer=LCMGID(root,'SPOT-QFISS')
    call require_list_item(q_outer,1,data%ngroup,10, &
      trim(owner)//' SPOT-QFISS OUTER')
    q_groups=LCMGIL(q_outer,1)
    do group=1,data%ngroup
      call require_list_item(q_groups,group,data%nunknown,2, &
        trim(owner)//' SPOT-QFISS GROUP')
      call LCMGDL(q_groups,group,qfiss(:,group))
    enddo
    if (any(real32_bits(qfiss) /= real32_bits(data%qfiss))) &
      call fail(trim(owner)//' SPOT-QFISS DIFFERS BITWISE.')

    deallocate(qfiss,leakage)
    call LCMCL(root,1)
  end subroutine load_flux


  subroutine compute_defect(pre,post,data,result)
    type(flux_state), intent(in) :: pre,post
    type(frozen_input), intent(in) :: data
    type(defect_result), intent(out) :: result
    integer :: group,region,key
    real(real64) :: value_pre,value_post,delta,weight
    real(real64) :: abs_delta,abs_input,v2_num2,v2_den2

    v2_num2=0.0_real64
    v2_den2=0.0_real64
    result%max_numerator=-1.0_real64
    result%max_denominator=-1.0_real64
    do group=1,data%ngroup
      do region=1,data%nregion
        key=data%keyflux(region)
        weight=real(data%volume(region),real64)
        value_pre=real(pre%flux(key,group),real64)
        value_post=real(post%flux(key,group),real64)
        delta=value_post-value_pre
        abs_delta=abs(delta)
        abs_input=abs(value_pre)
        v2_num2=v2_num2+weight*delta*delta
        v2_den2=v2_den2+weight*value_pre*value_pre
        if (abs_delta > result%max_numerator) then
          result%max_numerator=abs_delta
          result%delta_group=group
          result%delta_region=region
        endif
        if (abs_input > result%max_denominator) then
          result%max_denominator=abs_input
          result%input_group=group
          result%input_region=region
        endif
      enddo
    enddo

    if ((.not.ieee_is_finite(v2_num2)).or.(v2_num2 < 0.0_real64).or. &
        (.not.ieee_is_finite(v2_den2)).or.(v2_den2 <= 0.0_real64).or. &
        (.not.ieee_is_finite(result%max_numerator)).or. &
        (result%max_numerator < 0.0_real64).or. &
        (.not.ieee_is_finite(result%max_denominator)).or. &
        (result%max_denominator <= 0.0_real64)) &
      call fail('INVALID INPUT-NORMALIZED FIXED-POINT DEFECT.')

    result%v2_numerator=sqrt(v2_num2)
    result%v2_denominator=sqrt(v2_den2)
    result%d_v2=result%v2_numerator/result%v2_denominator
    result%d_max=result%max_numerator/result%max_denominator
    if ((.not.ieee_is_finite(result%d_v2)).or. &
        (.not.ieee_is_finite(result%d_max))) &
      call fail('NON-FINITE INPUT-NORMALIZED FIXED-POINT DEFECT.')
  end subroutine compute_defect


  subroutine print_defect(arm,result)
    character(len=*), intent(in) :: arm
    type(defect_result), intent(in) :: result

    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'V2-NUM',result%v2_numerator
    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'V2-DEN',result%v2_denominator
    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'D-V2',result%d_v2
    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'MAX-NUM',result%max_numerator
    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'MAX-DEN',result%max_denominator
    write(6,'(A,1X,A,1X,A,1X,ES25.17E3)') &
      'RADIAL-FLOOR-XSM',trim(arm),'D-MAX',result%d_max
    write(6,'(A,1X,A,1X,A,2(1X,I0))') &
      'RADIAL-FLOOR-XSM',trim(arm),'DELTA-ARGMAX', &
      result%delta_group,result%delta_region
    write(6,'(A,1X,A,1X,A,2(1X,I0))') &
      'RADIAL-FLOOR-XSM',trim(arm),'INPUT-ARGMAX', &
      result%input_group,result%input_region
  end subroutine print_defect


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

    write(0,'(A)') 'RADIAL-FLOOR-XSM ERROR: '//trim(message)
    error stop 2
  end subroutine fail

end program check_radial_floor_xsm
