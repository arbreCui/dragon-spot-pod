module SPOR64_VERIFY
  ! Shared record-level admission primitives for the SPOR64 lifecycle
  ! modules.  Each ownership handover still performs its own complete
  ! admission independently; only the implementation of these primitives
  ! is shared, so that a correction to one of them cannot reach some
  ! boundaries and miss others.  The LCMINF preflight in EXACT_INVENTORY
  ! is the standing example: it had propagated to two of eight private
  ! copies.
  use, intrinsic :: iso_c_binding, only : c_associated, c_ptr
  use, intrinsic :: iso_fortran_env, only : int32, real32
  use GANLIB
  implicit none
  private

  public :: RECORD_MATCHES, CHARACTER_RECORD_MATCHES, ABSENT_RECORD
  public :: LIST_ITEM_IS_DIRECTORY, SAME_REAL32_BITS, EXACT_INVENTORY
  public :: EMPTY_MEMORY_ROOT, EMPTY_ROOT

contains

  logical function RECORD_MATCHES(iplist,name,expected_length,expected_type)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer, intent(in) :: expected_length, expected_type
    integer :: actual_length, actual_type

    RECORD_MATCHES = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    RECORD_MATCHES = actual_length == expected_length .and. &
        actual_type == expected_type
  end function RECORD_MATCHES


  logical function CHARACTER_RECORD_MATCHES(iplist,name,expected_words, &
      character_count,expected_value)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name, expected_value
    integer, intent(in) :: expected_words, character_count
    character(len=72) :: value

    CHARACTER_RECORD_MATCHES = .false.
    if (character_count < 1 .or. character_count > len(value)) return
    if (.not. RECORD_MATCHES(iplist,name,expected_words,3)) return
    value = ' '
    call LCMGTC(iplist,name,character_count,value)
    CHARACTER_RECORD_MATCHES = value(1:character_count) == expected_value
  end function CHARACTER_RECORD_MATCHES


  logical function ABSENT_RECORD(iplist,name)
    type(c_ptr), intent(in) :: iplist
    character(len=*), intent(in) :: name
    integer :: actual_length, actual_type

    ABSENT_RECORD = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEN(iplist,name,actual_length,actual_type)
    ABSENT_RECORD = actual_length == 0 .and. actual_type == 99
  end function ABSENT_RECORD


  logical function LIST_ITEM_IS_DIRECTORY(iplist,index)
    type(c_ptr), intent(in) :: iplist
    integer, intent(in) :: index
    integer :: actual_length, actual_type

    LIST_ITEM_IS_DIRECTORY = .false.
    if (.not. c_associated(iplist)) return
    call LCMLEL(iplist,index,actual_length,actual_type)
    LIST_ITEM_IS_DIRECTORY = actual_length == -1 .and. actual_type == 0
  end function LIST_ITEM_IS_DIRECTORY


  logical function SAME_REAL32_BITS(left,right)
    real(real32), intent(in) :: left(:), right(:)

    SAME_REAL32_BITS = size(left) == size(right)
    if (SAME_REAL32_BITS) SAME_REAL32_BITS = all( &
        transfer(left,0_int32,size(left)) == &
        transfer(right,0_int32,size(right)))
  end function SAME_REAL32_BITS


  ! A fresh in-memory root.  LCMINF reports the storage medium in its
  ! final argument: true is an in-memory LCM table, false an XSM file.
  logical function EMPTY_MEMORY_ROOT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    EMPTY_MEMORY_ROOT = .false.
    if (.not. c_associated(iplist)) return
    call LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)
    EMPTY_MEMORY_ROOT = is_lcm .and. empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_MEMORY_ROOT


  ! A fresh root on either medium.  B2J and B2W drive in-memory tables and
  ! XSM files through the same GANLIB root operations, so for them
  ! freshness is a property of the active root, not of its storage.
  logical function EMPTY_ROOT(iplist)
    type(c_ptr), intent(in) :: iplist
    character(len=72) :: object_file
    character(len=12) :: object_name
    integer :: object_length
    logical :: empty, is_lcm

    EMPTY_ROOT = .false.
    if (.not. c_associated(iplist)) return
    call LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)
    EMPTY_ROOT = empty .and. object_length == -1 .and. &
        trim(object_name) == '/'
  end function EMPTY_ROOT


  logical function EXACT_INVENTORY(iplist,expected_names)
    type(c_ptr), intent(in) :: iplist
    character(len=12), intent(in) :: expected_names(:)
    character(len=72) :: object_file
    character(len=12) :: object_name
    character(len=12) :: first_name, item_name
    integer :: count, i, allocation_status, object_length
    logical :: empty, is_lcm
    logical, allocatable :: found(:)

    EXACT_INVENTORY = .false.
    if (.not. c_associated(iplist)) return
    ! LCMNXT is not defined for an empty directory or a list.
    ! LCMINF makes both ordinary preflight failures instead.
    call LCMINF(iplist,object_file,object_name,empty,object_length,is_lcm)
    if (empty .or. object_length /= -1) return
    allocate(found(size(expected_names)),stat=allocation_status)
    if (allocation_status /= 0) return
    found = .false.
    item_name = ' '
    call LCMNXT(iplist,item_name)
    if (item_name == ' ') return
    first_name = item_name
    count = 0
    do
      count = count+1
      if (count > size(expected_names)) return
      do i = 1, size(expected_names)
        if (item_name == expected_names(i)) exit
      end do
      if (i > size(expected_names)) return
      if (found(i)) return
      found(i) = .true.
      call LCMNXT(iplist,item_name)
      if (item_name == first_name) exit
    end do
    EXACT_INVENTORY = count == size(expected_names) .and. all(found)
  end function EXACT_INVENTORY


end module SPOR64_VERIFY
