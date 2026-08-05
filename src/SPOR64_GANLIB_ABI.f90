! Narrow ABI bridge for the three GANLIB entry points used by SPOR64_A8.
!
! SPOR64_A8 retains the checked external interfaces frozen by Phase A8.
! Modern GANLIB exposes the implementations as LCMAUX module procedures,
! whose linker names are different.  These wrappers connect only that ABI
! seam; they contain no state, numerical operation, or publication policy.

subroutine LCMLEN(iplist,name,length,itylcm)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB, only : GANLIB_LCMLEN => LCMLEN
  implicit none

  type(c_ptr) :: iplist
  character(len=*) :: name
  integer :: length, itylcm

  call GANLIB_LCMLEN(iplist,name,length,itylcm)
end subroutine LCMLEN


subroutine LCMGPD(iplist,name,address)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB, only : GANLIB_LCMGPD => LCMGPD
  implicit none

  type(c_ptr) :: iplist, address
  character(len=*) :: name

  call GANLIB_LCMGPD(iplist,name,address)
end subroutine LCMGPD


function LCMGIL(iplist,index) result(directory)
  use, intrinsic :: iso_c_binding, only : c_ptr
  use GANLIB, only : GANLIB_LCMGIL => LCMGIL
  implicit none

  type(c_ptr) :: iplist, directory
  integer :: index

  directory = GANLIB_LCMGIL(iplist,index)
end function LCMGIL
