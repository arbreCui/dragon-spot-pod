program extract_radial_collision_inputs
  ! Copy the actual first AAA radial TRACK/SYSTEM without numerical changes.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr
  implicit none
  type(c_ptr) :: archive,items,child,output
  integer :: count,which
  character(len=6) :: names(2)=[character(len=6) :: 'TRACK','SYSTEM']
  character(len=10) :: paths(2)=[character(len=10) :: 'track.xsm','system.xsm']
  call LCMOP(archive,'archive.xsm',2,2,0)
  call LCMGET(archive,'LISTDIM',count)
  if(count/=3) error stop 'actual three-plane archive required'
  do which=1,2
    items=LCMGID(archive,trim(names(which)))
    child=LCMGIL(items,1)
    call LCMOP(output,trim(paths(which)),0,2,0)
    call LCMEQU(child,output)
    call LCMCL(output,1)
  enddo
  call LCMCL(archive,1)
  write(*,'(A)') 'AXMAT-RADIAL-COLLISION-INPUTS-COPIED'
end program
