! Source-only fixture. This module is never linked into Dragon.
module BQ64_COMPACT_CONTROL_ACCESS
  use, intrinsic :: iso_c_binding, only : c_associated,c_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64
  use GANLIB
  implicit none
  private
  ! Private composed comparison retains the original BOOT64 limits.
  integer, parameter :: MAX_DEPTH = 64, MAX_NODES = 2000000
  integer, parameter :: MAX_RECORD_WORDS = 16777216
  integer, parameter :: composed_integer_kind_guard = &
      1 / merge(1,0,kind(1) == int32)
  integer, parameter :: VIEW_NONE = -1, VIEW_ROOT = 0, VIEW_AUTH = 1
  integer, parameter :: VIEW_GLOBAL = 2, VIEW_SEED = 3
  integer(int64), parameter :: COMPACT_FIXED_BYTES = 844632_int64
  integer(int64), parameter :: COMPACT_BYTES_PER_UNKNOWN = 7400_int64
  integer(int64), parameter :: COMPACT_STORAGE_CAP = 32_int64*1024_int64*1024_int64

  public :: COMPACT_EXPECTED_STORAGE_FITS,BQ64_SAME_COMPOSED_SOURCE
  public :: BQ64_COMPOSED_NODE,BQ64_SAME_RECORD,VIEW_ROOT,MAX_NODES,MAX_RECORD_WORDS
contains
  logical function COMPACT_EXPECTED_STORAGE_FITS(nunkno)
    integer, intent(in) :: nunkno
    integer(int64) :: required_bytes
    COMPACT_EXPECTED_STORAGE_FITS = .false.
    if (nunkno <= 0) return
    required_bytes = COMPACT_FIXED_BYTES + &
        COMPACT_BYTES_PER_UNKNOWN*int(nunkno,int64)
    COMPACT_EXPECTED_STORAGE_FITS = required_bytes <= COMPACT_STORAGE_CAP
  end function COMPACT_EXPECTED_STORAGE_FITS

  ! Exactly two empty expected placeholders are resolved to immutable inputs.
  ! Every resolved subtree then uses the original full raw tree comparison.
  logical function BQ64_SAME_COMPOSED_SOURCE(left,right,ipglobal,ipseed)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer :: nodes, visited(2)
    logical :: equal
    nodes = 0
    visited = 0
    BQ64_SAME_COMPOSED_SOURCE = .false.
    if (.not.c_associated(left).or..not.c_associated(right)) return
    if (.not.c_associated(ipglobal).or..not.c_associated(ipseed)) return
    equal = BQ64_COMPOSED_NODE(left,right,0,nodes,VIEW_ROOT, &
        ipglobal,ipseed,visited)
    BQ64_SAME_COMPOSED_SOURCE = equal.and.all(visited == 1)
  end function BQ64_SAME_COMPOSED_SOURCE

  recursive logical function BQ64_COMPOSED_NODE(left,right,depth,nodes, &
      view,ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: depth,view
    integer, intent(inout) :: nodes,visited(2)
    type(c_ptr) :: resolved_left
    character(len=72) :: file_name
    character(len=12) :: object_name
    integer :: slot,extent,next_view
    logical :: empty,medium
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not.c_associated(left).or..not.c_associated(right)) return
    resolved_left = left
    next_view = view
    if (view == VIEW_GLOBAL.or.view == VIEW_SEED) then
      if (depth /= 2) return
      slot = view-1
      if (visited(slot) /= 0) return
      ! The parent has already compared both directory type/length metadata.
      call LCMINF(left,file_name,object_name,empty,extent,medium)
      if (.not.empty.or.extent /= -1) return
      if (view == VIEW_GLOBAL) then
        resolved_left = ipglobal
      else
        resolved_left = ipseed
      endif
      if (.not.c_associated(resolved_left)) return
      visited(slot) = 1
      next_view = VIEW_NONE
    else if (view == VIEW_ROOT) then
      if (depth /= 0) return
    else if (view == VIEW_AUTH) then
      if (depth /= 1) return
    else if (view /= VIEW_NONE) then
      return
    endif
    ! This call compares empty flags, inventories, extents and all raw words
    ! after resolution, with the original cumulative depth and shared nodes.
    equal = BQ64_SAME_DIRECTORY(resolved_left,right,depth,nodes,next_view, &
        ipglobal,ipseed,visited)
  end function BQ64_COMPOSED_NODE

  recursive logical function BQ64_SAME_DIRECTORY(left,right,depth,nodes, &
      view,ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: depth,view
    integer, intent(inout) :: nodes,visited(2)
    integer :: child_view
    character(len=72) :: file_name
    character(len=12) :: object_name, item_name, first_name
    integer :: left_extent, right_extent, count_left, count_right
    integer :: length_left, type_left, length_right, type_right
    logical :: left_empty, right_empty, medium
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    call LCMINF(left,file_name,object_name,left_empty,left_extent,medium)
    call LCMINF(right,file_name,object_name,right_empty,right_extent,medium)
    if (left_extent /= -1 .or. right_extent /= -1) return
    if (left_empty .neqv. right_empty) return
    if (left_empty) then
      equal = .true.
      return
    end if
    item_name = ' '
    call LCMNXT(left,item_name)
    first_name = item_name
    count_left = 0
    do
      nodes = nodes+1
      count_left = count_left+1
      if (nodes > MAX_NODES .or. item_name == ' ') return
      call LCMLEN(left,item_name,length_left,type_left)
      call LCMLEN(right,item_name,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        child_view = VIEW_NONE
        if (view == VIEW_ROOT.and.depth == 0.and.item_name == 'SPOT-R64') then
          child_view = VIEW_AUTH
        else if (view == VIEW_AUTH.and.depth == 1) then
          if (item_name == 'GLOBAL64') child_view = VIEW_GLOBAL
          if (item_name == 'SEED') child_view = VIEW_SEED
        endif
        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &
            child_view,ipglobal,ipseed,visited)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGID(left,item_name)
        child_right = LCMGID(right,item_name)
        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &
            ipglobal,ipseed,visited)) return
      else
        if (.not. BQ64_SAME_RECORD(left,right,item_name,0,length_left,type_left)) return
      end if
      call LCMNXT(left,item_name)
      if (item_name == first_name) exit
    end do
    item_name = ' '
    call LCMNXT(right,item_name)
    first_name = item_name
    count_right = 0
    do
      count_right = count_right+1
      if (count_right > MAX_NODES .or. item_name == ' ') return
      call LCMNXT(right,item_name)
      if (item_name == first_name) exit
    end do
    equal = count_left == count_right
  end function BQ64_SAME_DIRECTORY

  recursive logical function BQ64_SAME_LIST(left,right,extent,depth,nodes, &
      ipglobal,ipseed,visited) result(equal)
    type(c_ptr), intent(in) :: left,right,ipglobal,ipseed
    integer, intent(in) :: extent, depth
    integer, intent(inout) :: nodes,visited(2)
    integer :: index, length_left, type_left, length_right, type_right
    type(c_ptr) :: child_left, child_right
    equal = .false.
    if (depth > MAX_DEPTH .or. extent <= 0) return
    if (.not. c_associated(left) .or. .not. c_associated(right)) return
    do index = 1, extent
      nodes = nodes+1
      if (nodes > MAX_NODES) return
      call LCMLEL(left,index,length_left,type_left)
      call LCMLEL(right,index,length_right,type_right)
      if (length_left /= length_right .or. type_left /= type_right) return
      if (type_left == 99 .and. length_left == 0) cycle
      if (type_left == 0) then
        if (length_left /= -1) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. BQ64_COMPOSED_NODE(child_left,child_right,depth+1,nodes, &
            VIEW_NONE,ipglobal,ipseed,visited)) return
      else if (type_left == 10) then
        if (length_left <= 0) return
        child_left = LCMGIL(left,index)
        child_right = LCMGIL(right,index)
        if (.not. BQ64_SAME_LIST(child_left,child_right,length_left,depth+1,nodes, &
            ipglobal,ipseed,visited)) return
      else
        if (.not. BQ64_SAME_RECORD(left,right,' ',index,length_left,type_left)) return
      end if
    end do
    equal = .true.
  end function BQ64_SAME_LIST

  logical function BQ64_SAME_RECORD(left,right,name,index,length,type_code)
    type(c_ptr), intent(in) :: left, right
    character(len=*), intent(in) :: name
    integer, intent(in) :: index, length, type_code
    integer(int64) :: words64
    integer :: words, allocation_status
    integer, allocatable :: left_bits(:), right_bits(:)
    BQ64_SAME_RECORD = .false.
    if (length <= 0 .or. type_code < 1 .or. type_code > 6) return
    words64 = int(length,int64)
    if (type_code == 4 .or. type_code == 6) words64 = 2_int64*words64
    if (words64 > int(MAX_RECORD_WORDS,int64)) return
    words = int(words64)
    allocate(left_bits(words),right_bits(words),stat=allocation_status)
    if (allocation_status /= 0) return
    ! GANLIB's GET wrappers copy raw words without coercion. The allocated
    ! buffer is two int32 words per REAL64/complex value, one for other types.
    if (index == 0) then
      call LCMGET(left,name,left_bits)
      call LCMGET(right,name,right_bits)
    else
      call LCMGDL(left,index,left_bits)
      call LCMGDL(right,index,right_bits)
    end if
    BQ64_SAME_RECORD = all(left_bits == right_bits)
  end function BQ64_SAME_RECORD
end module BQ64_COMPACT_CONTROL_ACCESS

program test_BQ64_compact_composed_tree
  use, intrinsic :: iso_c_binding, only : c_ptr,c_null_ptr
  use, intrinsic :: iso_fortran_env, only : int32,int64,real32,real64
  use GANLIB
  use BQ64_COMPACT_CONTROL_ACCESS
  implicit none
  type(c_ptr) :: expected,actual,global,seed,auth,branch,child,groups
  integer :: assertions,case_id,words(8),g,nodes,total_nodes,visited(2),deep
  integer(int64) :: file_size
  logical :: ok,exists
  assertions = 0
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(0))
  call check(COMPACT_EXPECTED_STORAGE_FITS(1))
  call check(COMPACT_EXPECTED_STORAGE_FITS(14))
  call check(COMPACT_EXPECTED_STORAGE_FITS(4420))
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(4421))
  call check(.not.COMPACT_EXPECTED_STORAGE_FITS(huge(1)))
  ! Model trees contain no physical solve or production inputs.
  do case_id=0,12
    call setup(1)
    auth=LCMGID(actual,'SPOT-R64')
    select case(case_id)
    case(1)
      branch=LCMGID(auth,'GLOBAL64');words=0;words(1)=99
      call LCMPUT(branch,'RAW-1',2,1,words)
    case(2)
      branch=LCMGID(auth,'SEED');words=0;words(1)=99
      call LCMPUT(branch,'RAW-1',2,1,words)
    case(3)
      branch=LCMGID(auth,'GLOBAL64');words=0;words(2)=int(z'80000000',int32)
      call LCMPUT(branch,'RAW-4',2,4,transfer(words(1:4),[0.0_real64,0.0_real64]))
    case(4)
      branch=LCMGID(auth,'GLOBAL64');call LCMPUT(branch,'EXTRA',1,1,1)
    case(5)
      auth=LCMGID(expected,'SPOT-R64');branch=LCMGID(auth,'GLOBAL64')
      call LCMPUT(branch,'DIRTY',1,1,1)
    case(6)
      auth=LCMGID(expected,'SPOT-R64');branch=LCMGID(auth,'SEED')
      call LCMPUT(branch,'DIRTY',1,1,1)
    case(7)
      call LCMPUT(actual,'STATE-VECTOR',1,1,1)
    case(8)
      branch=LCMGID(auth,'GLOBAL64');call LCMPUT(branch,'RAW-1',2,2,[0.0,0.0])
    case(9)
      call LCMPUT(actual,'EXTRA-ROOT',1,1,1)
    case(10)
      call LCMPUT(auth,'EXTRA-AUTH',1,1,1)
    case(11)
      branch=LCMGID(auth,'GLOBAL64');child=LCMGID(branch,'SEED')
      call LCMPUT(child,'MARKER',1,1,99)
    case(12)
      groups=LCMGID(actual,'ROOT-QFISS64');words=0;words(2)=int(z'80000000',int32)
      call LCMPDL(groups,370,1,4,[transfer(words(1:2),0.0_real64)])
    end select
    ok=BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed)
    call check(ok.eqv.(case_id == 0))
    if (case_id == 0) then
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(expected,actual,c_null_ptr,seed))
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,c_null_ptr))
      call check(.not.BQ64_SAME_COMPOSED_SOURCE(c_null_ptr,actual,global,seed))
      nodes=0;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(ok.and.all(visited == 1));total_nodes=nodes
      nodes=MAX_NODES-total_nodes;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(ok.and.nodes == MAX_NODES.and.all(visited == 1))
      nodes=MAX_NODES-total_nodes+1;visited=0
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(.not.ok)
      nodes=0;visited=1
      ok=BQ64_COMPOSED_NODE(expected,actual,0,nodes,VIEW_ROOT,global,seed,visited)
      call check(.not.ok)
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-1',0,MAX_RECORD_WORDS+1,1))
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-4',0,MAX_RECORD_WORDS/2+1,4))
      call check(.not.BQ64_SAME_RECORD(global,global,'RAW-1',0,1,7))
    endif
    call close_all()
  enddo
  do deep=62,63
    call setup(1)
    branch=global
    do g=1,deep
      child=LCMDID(branch,'DEEP');branch=child
    enddo
    call LCMPUT(branch,'END',1,1,1)
    auth=LCMGID(actual,'SPOT-R64');branch=LCMGID(auth,'GLOBAL64')
    call LCMEQU(global,branch)
    call check(BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed).eqv.(deep == 62))
    call close_all()
  enddo
  ! The physical-bound model uses the exact small writer layout and NUNKNO14.
  inquire(file='C64-EXP',exist=exists);call check(.not.exists)
  inquire(file='C64-ACT',exist=exists);call check(.not.exists)
  call setup(14,2)
  call check(BQ64_SAME_COMPOSED_SOURCE(expected,actual,global,seed))
  call LCMCL(expected,1)
  inquire(file='C64-EXP',size=file_size)
  call check(file_size == 844632_int64+7400_int64*14_int64)
  call check(file_size <= 32_int64*1024_int64*1024_int64)
  ! Future Host retains these two model files; no production artifact is touched.
  call LCMCL(actual,1);call LCMCL(global,2);call LCMCL(seed,2)
  write(*,'(A,I0,A)') '{"status":"ACTUAL_COMPACT_GANLIB_MODEL_CONTROLS_ONLY","assertions":', &
      assertions,',"physics_qualified":false,"reader_qualified":false,"AAA_qualified":false}'
contains
  subroutine check(condition)
    logical,intent(in) :: condition
    if (.not.condition) call XABORT('BQ64 COMPACT CONTROL ASSERTION FAILED.')
    assertions=assertions+1
  end subroutine check
  subroutine setup(nunkno,medium)
    integer,intent(in) :: nunkno
    integer,optional,intent(in) :: medium
    integer :: kind_file,t
    kind_file=1;if(present(medium))kind_file=medium
    call LCMOP(global,'C64-GLOBAL',0,1,0);call LCMOP(seed,'C64-SEED',0,1,0)
    words=0
    do t=1,6
      call put_raw(global,t);call put_raw(seed,t)
    enddo
    child=LCMDID(global,'SEED');call LCMPUT(child,'MARKER',1,1,7)
    child=LCMDID(seed,'GLOBAL64');call LCMPUT(child,'MARKER',1,1,8)
    groups=LCMLID(global,'LIST',3)
    child=LCMDIL(groups,1);call LCMPUT(child,'ONE',1,1,1)
    call LCMPDL(groups,2,2,1,[1,2])
    child=LCMDIL(groups,3);child=LCMDID(child,'GLOBAL64')
    call LCMPUT(child,'MARKER',1,1,9)
    call LCMOP(expected,'C64-EXP',0,kind_file,0)
    call LCMOP(actual,'C64-ACT',0,kind_file,0)
    call populate(expected,nunkno,.true.);call populate(actual,nunkno,.false.)
  end subroutine setup
  subroutine put_raw(root,type_code)
    type(c_ptr),intent(in) :: root
    integer,intent(in) :: type_code
    character(len=5) :: name
    write(name,'(A,I1)') 'RAW-',type_code
    select case(type_code)
    case(1,3)
      call LCMPUT(root,name,2,type_code,words(1:2))
    case(2)
      call LCMPUT(root,name,2,2,transfer(words(1:2),[0.0_real32,0.0_real32]))
    case(4)
      call LCMPUT(root,name,2,4,transfer(words(1:4),[0.0_real64,0.0_real64]))
    case(5)
      call LCMPUT(root,name,2,5,[.false.,.false.])
    case(6)
      call LCMPUT(root,name,2,6,[cmplx(0.0,0.0),cmplx(0.0,0.0)])
    end select
  end subroutine put_raw
  subroutine populate(root,nunkno,compact)
    type(c_ptr),intent(in) :: root
    integer,intent(in) :: nunkno
    logical,intent(in) :: compact
    type(c_ptr) :: a,outer,inner,qlist,rlist,c
    integer :: state(40),i
    real(real32),allocatable :: q32(:)
    real(real64),allocatable :: q64(:)
    allocate(q32(nunkno),q64(nunkno));q32=0.0_real32;q64=0.0_real64
    call LCMPTC(root,'SIGNATURE',12,'L_SOURCE    ')
    state=0;state(1:3)=[370,nunkno,1]
    call LCMPUT(root,'STATE-VECTOR',40,1,state)
    call LCMPUT(root,'SPOT-FROZEN',1,1,1)
    call LCMPUT(root,'SPOT-KEFF',1,2,1.0_real32)
    call LCMPUT(root,'SPOT-QINT',370,2,[(0.0_real32,i=1,370)])
    outer=LCMLID(root,'DSOUR',1);inner=LCMLIL(outer,1,370)
    do i=1,370
      call LCMPDL(inner,i,nunkno,2,q32)
    enddo
    a=LCMDID(root,'SPOT-R64')
    call LCMPUT(a,'RHO',1,4,1.0_real64);call LCMPUT(a,'PLANE',1,1,1)
    call LCMPTC(a,'STATE',12,'FROZEN-QFIS ')
    call LCMPUT(a,'NORM',1,4,1.0_real64)
    c=LCMDID(a,'GLOBAL64');if(.not.compact)call LCMEQU(global,c)
    c=LCMDID(a,'SEED');if(.not.compact)call LCMEQU(seed,c)
    qlist=LCMLID(a,'QFISS',370)
    do i=1,370
      call LCMPDL(qlist,i,nunkno,4,q64)
    enddo
    rlist=LCMLID(root,'ROOT-QFISS64',370)
    do i=1,370
      call LCMPDL(rlist,i,nunkno,4,q64)
    enddo
    call LCMPUT(a,'EPOCH',1,1,0)
  end subroutine populate
  subroutine close_all()
    call LCMCL(expected,2);call LCMCL(actual,2)
    call LCMCL(global,2);call LCMCL(seed,2)
  end subroutine close_all
end program test_BQ64_compact_composed_tree
