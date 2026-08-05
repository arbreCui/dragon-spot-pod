program TEST_SPOR64_GANLIB_ABI
  use, intrinsic :: iso_c_binding, only : c_associated, c_f_pointer, c_ptr
  use GANLIB, only : LCMDIL, LCMCL, LCMGET, LCMLID, LCMOP, LCMPUT
  implicit none

  type(c_ptr) :: root, list, writer, reader, address
  integer, target :: values(3)
  integer, pointer :: borrowed(:)
  integer :: found(3), marker, length, record_type

  interface
    subroutine LCMLEN(iplist,name,length,itylcm)
      import :: c_ptr
      type(c_ptr) :: iplist
      character(len=*) :: name
      integer :: length, itylcm
    end subroutine LCMLEN

    subroutine LCMGPD(iplist,name,address)
      import :: c_ptr
      type(c_ptr) :: iplist, address
      character(len=*) :: name
    end subroutine LCMGPD

    function LCMGIL(iplist,index) result(directory)
      import :: c_ptr
      type(c_ptr) :: iplist, directory
      integer :: index
    end function LCMGIL
  end interface

  values = [17,23,31]
  call LCMOP(root,'B2D-LINK-TEST',0,1,0)
  if (.not. c_associated(root)) error stop 'LCMOP failed'

  call LCMPUT(root,'VALUES',3,1,values)
  call LCMLEN(root,'VALUES',length,record_type)
  if (length /= 3 .or. record_type /= 1) &
      error stop 'LCMLEN bridge differs'

  call LCMGPD(root,'VALUES',address)
  if (.not. c_associated(address)) error stop 'LCMGPD bridge returned null'
  call c_f_pointer(address,borrowed,[3])
  if (any(borrowed /= values)) error stop 'LCMGPD bridge payload differs'

  list = LCMLID(root,'DIR-LIST',1)
  if (.not. c_associated(list)) error stop 'LCMLID failed'
  writer = LCMDIL(list,1)
  if (.not. c_associated(writer)) error stop 'LCMDIL failed'
  call LCMPUT(writer,'MARKER',1,1,97)
  reader = LCMGIL(list,1)
  if (.not. c_associated(reader)) error stop 'LCMGIL bridge returned null'
  call LCMGET(reader,'MARKER',marker)
  if (marker /= 97) error stop 'LCMGIL bridge selected wrong directory'

  call LCMGET(root,'VALUES',found)
  if (any(found /= values)) error stop 'bridge mutated GANLIB state'
  call LCMCL(root,2)
  write(*,'(A)') 'SPOR64 B2D GANLIB ABI PASS'
end program TEST_SPOR64_GANLIB_ABI
