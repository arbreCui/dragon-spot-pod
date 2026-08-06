program CHECK_B2E_REAL_SCHEMA
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : error_unit, int32, real32
  use, intrinsic :: ieee_arithmetic, only : ieee_is_finite
  implicit none

  integer, parameter :: NGRP=370, NSTATE=40
  type(c_ptr) :: flux, macro, track, system, source, groups, group_dir
  character(len=1024) :: flux_path, macro_path, track_path
  character(len=1024) :: system_path, source_path
  integer :: flux_state(NSTATE), macro_state(NSTATE), track_state(NSTATE)
  integer :: imerge(8), length, record_type, group, item
  integer :: nonzero_p1, nonzero_p2
  integer(int32), parameter :: ABS_MASK=int(z'7fffffff',int32)
  integer(int32), parameter :: EPS_BITS=int(z'348637bd',int32)
  real(real32) :: eps(5)
  real(real32), allocatable :: values(:)

  if (command_argument_count() /= 5) &
    error stop 'expected FLUX MACRO0 TRACK SYSTEM FSOURCE paths'
  call get_command_argument(1,flux_path)
  call get_command_argument(2,macro_path)
  call get_command_argument(3,track_path)
  call get_command_argument(4,system_path)
  call get_command_argument(5,source_path)
  call LCMOP(flux,trim(flux_path),2,2,0)
  call LCMOP(macro,trim(macro_path),2,2,0)
  call LCMOP(track,trim(track_path),2,2,0)
  call LCMOP(system,trim(system_path),2,2,0)
  call LCMOP(source,trim(source_path),2,2,0)

  call REQUIRE_CHARACTER(flux,'SIGNATURE','L_FLUX')
  call REQUIRE_RECORD(flux,'SOUR',NGRP,10)
  call REQUIRE_ABSENT(flux,'SPOT-R64')
  call REQUIRE_ABSENT(flux,'B2  HETE')
  call REQUIRE_ABSENT(flux,'B2  B1HOM')
  call REQUIRE_ABSENT(flux,'AFLUX')
  call REQUIRE_ABSENT(flux,'DFLUX')
  call REQUIRE_ABSENT(flux,'ADFLUX')
  call REQUIRE_ABSENT_OR_RECORD(flux,'KEYFLX',8,1)
  call REQUIRE_ABSENT_OR_RECORD(flux,'OPTION',1,3)
  call REQUIRE_ABSENT_OR_RECORD(flux,'LINK.MACRO',3,3)
  call REQUIRE_ABSENT_OR_RECORD(flux,'LINK.TRACK',3,3)
  call REQUIRE_ABSENT_OR_RECORD(flux,'LINK.SYSTEM',3,3)
  call REQUIRE_ABSENT_OR_RECORD(flux,'SPOT-LEAK1D',NGRP,2)
  call REQUIRE_RECORD(flux,'STATE-VECTOR',NSTATE,1)
  call LCMGET(flux,'STATE-VECTOR',flux_state)
  if (any(flux_state(1:18) /= &
      [370,14,1,0,0,0,0,3,3,1,740,500,0,0,0,0,8,1])) &
    error stop 'real FLUX state differs before macro guard'
  call REQUIRE_RECORD(flux,'EPS-CONVERGE',5,2)
  call LCMGET(flux,'EPS-CONVERGE',eps)
  if (any(transfer(eps(1:3),[0_int32,0_int32,0_int32]) /= EPS_BITS)) &
    error stop 'real FLUX tolerance bits differ'
  if (any(transfer(eps(4:5),[0_int32,0_int32]) /= 0_int32)) &
    error stop 'real FLUX terminal fields differ'
  call REQUIRE_RECORD(flux,'IMERGE-LEAK',8,1)
  call LCMGET(flux,'IMERGE-LEAK',imerge)
  if (any(imerge /= 1)) error stop 'real FLUX merge map differs'

  call REQUIRE_CHARACTER(macro,'SIGNATURE','L_MACROLIB')
  call REQUIRE_RECORD(macro,'STATE-VECTOR',NSTATE,1)
  call LCMGET(macro,'STATE-VECTOR',macro_state)
  if (macro_state(1) /= NGRP .or. macro_state(2) /= 8 .or. &
      macro_state(3) /= 3 .or. macro_state(4) /= 32 .or. &
      macro_state(6) /= 2 .or. macro_state(13) /= 0) &
    error stop 'real MACRO0 state differs'

  call REQUIRE_CHARACTER(track,'SIGNATURE','L_TRACK')
  call REQUIRE_RECORD(track,'STATE-VECTOR',NSTATE,1)
  call LCMGET(track,'STATE-VECTOR',track_state)
  if (track_state(1) /= 8 .or. track_state(2) /= 14 .or. &
      track_state(6) /= 1) error stop 'real TRACK active-order state differs'

  call REQUIRE_CHARACTER(system,'SIGNATURE','L_PIJ')
  call REQUIRE_CHARACTER(source,'SIGNATURE','L_SOURCE')

  groups=LCMGID(macro,'GROUP')
  if (.not. c_associated(groups)) error stop 'real MACRO0 GROUP missing'
  nonzero_p1=0
  nonzero_p2=0
  do group=1,NGRP
    group_dir=LCMGIL(groups,group)
    if (.not. c_associated(group_dir)) error stop 'real MACRO0 group missing'
    call LCMLEN(group_dir,'SCAT01',length,record_type)
    if (length > 0) then
      if (record_type /= 2) error stop 'SCAT01 type differs'
      allocate(values(length))
      call LCMGET(group_dir,'SCAT01',values)
      if (.not. all(ieee_is_finite(values))) &
        error stop 'SCAT01 contains a nonfinite value'
      do item=1,length
        if (iand(transfer(values(item),0_int32),ABS_MASK) /= 0_int32) &
          nonzero_p1=nonzero_p1+1
      end do
      deallocate(values)
    end if
    call LCMLEN(group_dir,'SCAT02',length,record_type)
    if (length > 0) then
      if (record_type /= 2) error stop 'SCAT02 type differs'
      allocate(values(length))
      call LCMGET(group_dir,'SCAT02',values)
      if (.not. all(ieee_is_finite(values))) &
        error stop 'SCAT02 contains a nonfinite value'
      do item=1,length
        if (iand(transfer(values(item),0_int32),ABS_MASK) /= 0_int32) &
          nonzero_p2=nonzero_p2+1
      end do
      deallocate(values)
    end if
  end do
  if (nonzero_p1 <= 0 .or. nonzero_p2 <= 0) &
    error stop 'higher-order stored scattering unexpectedly zero'

  call LCMCL(source,1)
  call LCMCL(system,1)
  call LCMCL(track,1)
  call LCMCL(macro,1)
  call LCMCL(flux,1)
  write(*,'(A)') 'B2E REAL-SCHEMA PASS'
  write(*,'(A)') 'B2E LEGACY-SOUR-COLLISION=true'
  write(*,'(A)') 'B2E MACRO-STORED-LEGENDRE-COMPONENTS=3'
  write(*,'(A)') 'B2E TRACK-ACTIVE-FLUX-LEGENDRE-COMPONENTS=1'
  write(*,'(A)') &
    'B2E SOUR-FREE-NEXT-BLOCKER=MACRO0/STATE-VECTOR(3)=3'
  write(*,'(A,I0,1X,A,I0)') &
    'B2E NONZERO-SCAT01=',nonzero_p1,'NONZERO-SCAT02=',nonzero_p2

contains

  subroutine REQUIRE_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type
    call LCMLEN(root,name,found_length,found_type)
    if (found_length /= expected_length .or. found_type /= expected_type) then
      write(error_unit,'(A,1X,A,4(1X,I0))') 'B2E RECORD MISMATCH', &
        trim(name),found_length,found_type,expected_length,expected_type
      error stop 'real schema record mismatch'
    end if
  end subroutine REQUIRE_RECORD

  subroutine REQUIRE_ABSENT(root,name)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer :: found_length, found_type
    call LCMLEN(root,name,found_length,found_type)
    if (found_length /= 0 .or. found_type /= 99) then
      write(error_unit,'(A,1X,A,2(1X,I0))') 'B2E ABSENCE MISMATCH', &
        trim(name),found_length,found_type
      error stop 'unexpected real schema collision'
    end if
  end subroutine REQUIRE_ABSENT

  subroutine REQUIRE_ABSENT_OR_RECORD(root,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: found_length, found_type
    call LCMLEN(root,name,found_length,found_type)
    if (.not. ((found_length == 0 .and. found_type == 99) .or. &
        (found_length == expected_length .and. found_type == expected_type))) then
      write(error_unit,'(A,1X,A,4(1X,I0))') 'B2E OPTIONAL MISMATCH', &
        trim(name),found_length,found_type,expected_length,expected_type
      error stop 'real schema optional record mismatch'
    end if
  end subroutine REQUIRE_ABSENT_OR_RECORD

  subroutine REQUIRE_CHARACTER(root,name,expected)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name, expected
    character(len=72) :: found
    call REQUIRE_RECORD(root,name,3,3)
    found=' '
    call LCMGTC(root,name,12,found)
    if (trim(found(1:12)) /= trim(expected)) &
      error stop 'real schema character mismatch'
  end subroutine REQUIRE_CHARACTER
end program CHECK_B2E_REAL_SCHEMA
