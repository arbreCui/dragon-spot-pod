program check_gmres_activity_pair_xsm
  ! Read-only proof that the candidate differs from the legacy XSM only
  ! by one root-level SPOT-GMR-AUD directory.
  use GANLIB
  use, intrinsic :: iso_c_binding, only : c_ptr, c_int32_t, &
    c_associated, c_f_pointer
  use, intrinsic :: iso_fortran_env, only : error_unit, output_unit
  implicit none

  integer, parameter :: max_path=72
  character(len=12), parameter :: gmres_audit='SPOT-GMR-AUD'
  character(len=1024) :: legacy_path,candidate_path
  type(c_ptr) :: legacy_root,candidate_root
  logical :: exists

  if (command_argument_count() /= 2) &
    call fail('expected LEGACY_ON_XSM CANDIDATE_ON_XSM')
  call get_command_argument(1,legacy_path)
  call get_command_argument(2,candidate_path)
  if (len_trim(legacy_path) == 0) call fail('empty legacy path')
  if (len_trim(candidate_path) == 0) call fail('empty candidate path')
  if (len_trim(legacy_path) > max_path) &
    call fail('legacy XSM path exceeds Ganlib limit')
  if (len_trim(candidate_path) > max_path) &
    call fail('candidate XSM path exceeds Ganlib limit')
  if (trim(legacy_path) == trim(candidate_path)) &
    call fail('XSM paths must be distinct')
  inquire(file=trim(legacy_path),exist=exists)
  if (.not.exists) call fail('legacy XSM does not exist')
  inquire(file=trim(candidate_path),exist=exists)
  if (.not.exists) call fail('candidate XSM does not exist')

  call LCMOP(legacy_root,trim(legacy_path),2,2,0)
  call LCMOP(candidate_root,trim(candidate_path),2,2,0)
  call compare_roots(legacy_root,candidate_root)
  call LCMCL(candidate_root,1)
  call LCMCL(legacy_root,1)

  write(output_unit,'(A)') 'GMRES-ACTIVITY PAIR CHECK PASS'

contains

  subroutine compare_roots(legacy,candidate)
    type(c_ptr), intent(in) :: legacy,candidate
    character(len=12), allocatable :: legacy_names(:)
    character(len=12), allocatable :: candidate_all(:)
    character(len=12), allocatable :: candidate_names(:)
    integer :: audit_count,audit_length,audit_type
    integer :: i,j

    call collect_names(legacy,legacy_names)
    call collect_names(candidate,candidate_all)
    if (count(legacy_names == gmres_audit) /= 0) &
      call fail('legacy root already contains SPOT-GMR-AUD')
    audit_count=count(candidate_all == gmres_audit)
    if (audit_count /= 1) &
      call fail('candidate root SPOT-GMR-AUD census differs')
    call LCMLEN(candidate,gmres_audit,audit_length,audit_type)
    if ((audit_length /= -1).or.(audit_type /= 0)) &
      call fail('candidate SPOT-GMR-AUD is not a directory')

    if (size(candidate_all) /= size(legacy_names)+1) &
      call fail('candidate root record census differs')
    allocate(candidate_names(size(legacy_names)))
    j=0
    do i=1,size(candidate_all)
      if (candidate_all(i) == gmres_audit) cycle
      j=j+1
      if (j > size(candidate_names)) &
        call fail('candidate root filtering overflow')
      candidate_names(j)=candidate_all(i)
    enddo
    if (j /= size(candidate_names)) &
      call fail('candidate root filtering census differs')
    if (any(legacy_names /= candidate_names)) &
      call fail('candidate root record name or order differs')

    ! SPOT-MOC-AUD is deliberately not excluded: if present, it and every
    ! other legacy record are compared recursively and bit for bit.
    do i=1,size(legacy_names)
      call compare_named_record(legacy,candidate,legacy_names(i))
    enddo
  end subroutine compare_roots


  recursive subroutine compare_table_exact(left,right)
    type(c_ptr), intent(in) :: left,right
    character(len=12), allocatable :: left_names(:),right_names(:)
    integer :: i

    call collect_names(left,left_names)
    call collect_names(right,right_names)
    if (size(left_names) /= size(right_names)) &
      call fail('nested table record census differs')
    if (any(left_names /= right_names)) &
      call fail('nested table record name or order differs')
    do i=1,size(left_names)
      call compare_named_record(left,right,left_names(i))
    enddo
  end subroutine compare_table_exact


  recursive subroutine compare_named_record(left,right,name)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    type(c_ptr) :: left_child,right_child
    integer :: left_length,right_length,left_type,right_type

    call LCMLEN(left,name,left_length,left_type)
    call LCMLEN(right,name,right_length,right_type)
    if (left_type /= right_type) call fail('record type differs')
    if (left_length /= right_length) call fail('record length differs')

    select case (left_type)
    case (0)
      if (left_length /= -1) &
        call fail('directory length violates Ganlib contract')
      left_child=LCMGID(left,name)
      right_child=LCMGID(right,name)
      if ((.not.c_associated(left_child)).or. &
          (.not.c_associated(right_child))) &
        call fail('directory handle is not associated')
      call compare_table_exact(left_child,right_child)
    case (10)
      if (left_length < 0) call fail('negative list length')
      left_child=LCMGID(left,name)
      right_child=LCMGID(right,name)
      if ((.not.c_associated(left_child)).or. &
          (.not.c_associated(right_child))) &
        call fail('list handle is not associated')
      call compare_list_exact(left_child,right_child,left_length)
    case (1:6)
      call compare_table_payload(left,right,name,left_length,left_type)
    case default
      call fail('unsupported Ganlib record type')
    end select
  end subroutine compare_named_record


  recursive subroutine compare_list_exact(left,right,list_length)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: list_length
    type(c_ptr) :: left_child,right_child
    integer :: item,left_length,right_length,left_type,right_type

    if (list_length < 0) call fail('negative recursive list length')
    do item=1,list_length
      call LCMLEL(left,item,left_length,left_type)
      call LCMLEL(right,item,right_length,right_type)
      if (left_type /= right_type) call fail('list item type differs')
      if (left_length /= right_length) &
        call fail('list item length differs')
      select case (left_type)
      case (0)
        if (left_length /= -1) &
          call fail('list directory length violates Ganlib contract')
        left_child=LCMGIL(left,item)
        right_child=LCMGIL(right,item)
        if ((.not.c_associated(left_child)).or. &
            (.not.c_associated(right_child))) &
          call fail('list directory handle is not associated')
        call compare_table_exact(left_child,right_child)
      case (10)
        if (left_length < 0) call fail('negative nested list length')
        left_child=LCMGIL(left,item)
        right_child=LCMGIL(right,item)
        if ((.not.c_associated(left_child)).or. &
            (.not.c_associated(right_child))) &
          call fail('nested list handle is not associated')
        call compare_list_exact(left_child,right_child,left_length)
      case (1:6)
        call compare_list_payload(left,right,item,left_length,left_type)
      case (99)
        if (left_length /= 0) &
          call fail('empty list item has nonzero length')
      case default
        call fail('unsupported Ganlib list item type')
      end select
    enddo
  end subroutine compare_list_exact


  subroutine compare_table_payload(left,right,name,length,lcm_type)
    type(c_ptr), intent(in) :: left,right
    character(len=*), intent(in) :: name
    integer, intent(in) :: length,lcm_type
    type(c_ptr) :: left_data,right_data

    if (length < 0) call fail('negative primitive record length')
    if (length == 0) return
    call LCMGPD(left,name,left_data)
    call LCMGPD(right,name,right_data)
    call compare_words(left_data,right_data,length,lcm_type)
  end subroutine compare_table_payload


  subroutine compare_list_payload(left,right,item,length,lcm_type)
    type(c_ptr), intent(in) :: left,right
    integer, intent(in) :: item,length,lcm_type
    type(c_ptr) :: left_data,right_data

    if (length < 0) call fail('negative primitive list length')
    if (length == 0) return
    call LCMGPL(left,item,left_data)
    call LCMGPL(right,item,right_data)
    call compare_words(left_data,right_data,length,lcm_type)
  end subroutine compare_list_payload


  subroutine compare_words(left_data,right_data,length,lcm_type)
    type(c_ptr), intent(in) :: left_data,right_data
    integer, intent(in) :: length,lcm_type
    integer(c_int32_t), pointer :: left_words(:),right_words(:)
    integer :: word_count

    select case (lcm_type)
    case (1:3,5)
      word_count=length
    case (4,6)
      if (length > shiftr(huge(word_count),1)) &
        call fail('primitive word count overflows')
      word_count=2*length
    case default
      call fail('primitive type cannot be compared')
    end select
    if (word_count == 0) return
    if ((.not.c_associated(left_data)).or. &
        (.not.c_associated(right_data))) &
      call fail('primitive payload pointer is not associated')
    call c_f_pointer(left_data,left_words,[word_count])
    call c_f_pointer(right_data,right_words,[word_count])
    if (any(left_words /= right_words)) &
      call fail('primitive payload differs')
  end subroutine compare_words


  subroutine collect_names(table,names)
    type(c_ptr), intent(in) :: table
    character(len=12), allocatable, intent(out) :: names(:)
    character(len=72) :: object_name
    character(len=12) :: directory_name,name,first
    logical :: empty,is_lcm
    integer :: object_length,count_names,i

    call LCMINF(table,object_name,directory_name,empty,object_length,is_lcm)
    if (object_length /= -1) &
      call fail('name collection target is not a table')
    if (empty) then
      allocate(names(0))
      return
    endif

    name=' '
    call LCMNXT(table,name)
    if (name == ' ') call fail('nonempty table has no first record')
    first=name
    count_names=1
    do
      call LCMNXT(table,name)
      if (name == first) exit
      if (name == ' ') call fail('table traversal returned an empty name')
      count_names=count_names+1
    enddo

    allocate(names(count_names))
    name=' '
    call LCMNXT(table,name)
    names(1)=name
    do i=2,count_names
      call LCMNXT(table,name)
      names(i)=name
    enddo
    call LCMNXT(table,name)
    if (name /= first) call fail('table traversal does not close')
  end subroutine collect_names


  subroutine fail(message)
    character(len=*), intent(in) :: message

    write(error_unit,'(A)') &
      'GMRES-ACTIVITY PAIR CHECK FAIL: '//trim(message)
    error stop 1
  end subroutine fail

end program check_gmres_activity_pair_xsm
