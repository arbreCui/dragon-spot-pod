! Actual native SN8 matrix and malformed-input controls; no transport solve.
program AXMAT_WHITE_TRACE_UNIT
  use GANLIB
  use AXMAT_WHITE_TRACE_MOD
  implicit none
  type(c_ptr) :: track
  character(len=72) :: path
  real :: mu32(8),w32(8),areas32(8)
  double precision :: mu(8),w(8),matrix(8,8),p,area,bad_mu(8),bad_w(8)
  integer :: info,i,j,marker(4),negative_controls
  if (command_argument_count() /= 1) call XABORT('AXMAT WHITE UNIT: TRACK PATH REQUIRED.')
  call get_command_argument(1,path)
  call LCMOP(track,trim(path),2,2,0)
  call LCMGET(track,'U',mu32)
  call LCMGET(track,'W',w32)
  call LCMGET(track,'AREA2D',areas32)
  call LCMCL(track,1)
  mu=real(mu32,8);w=real(w32,8)
  p=6.0d0*0.61776479d0;area=sum(real(areas32,8))
  call AXMAT_WHITE_KERNEL(mu,w,p,area,matrix,info)
  if (info /= 0) call XABORT('AXMAT WHITE UNIT: ACTUAL GRID REJECTED.')
  open(21,file='kernel.csv',status='new',action='write')
  write(21,'(A)') 'row,column,value'
  do i=1,8
    do j=1,8
      write(21,'(I0,A,I0,A,ES26.17E3)') i,',',j,',',matrix(i,j)
    enddo
  enddo
  close(21)
  negative_controls=0
  bad_mu=mu;bad_mu(1)=1.0d0
  call AXMAT_WHITE_KERNEL(bad_mu,w,p,area,matrix,info)
  call rejected()
  bad_w=w;bad_w(1)=-w(1)
  call AXMAT_WHITE_KERNEL(mu,bad_w,p,area,matrix,info)
  call rejected()
  call AXMAT_WHITE_KERNEL(mu,w,0.0d0,area,matrix,info)
  call rejected()
  call AXMAT_WHITE_KERNEL(mu,w,p,-area,matrix,info)
  call rejected()
  marker=[1,1,8,3]
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,12,3,8,3,1,info)
  if (info /= 0 .or. .not.AXMAT_WHITE_ON) call XABORT('AXMAT WHITE UNIT: VALID FLAG REJECTED.')
  marker(2)=2
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,12,3,8,3,1,info)
  call rejected()
  marker=[1,1,8,3]
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p,8,24,3,8,3,1,info)
  call rejected()
  call AXMAT_WHITE_CONFIGURE(.true.,marker,p*1.01d0,8,12,3,8,3,1,info)
  call rejected()
  marker=0
  call AXMAT_WHITE_CONFIGURE(.false.,marker,0.0d0,8,12,3,8,3,1,info)
  if (info /= 0 .or. AXMAT_WHITE_ON) call XABORT('AXMAT WHITE UNIT: OFF RESET FAILED.')
  if (negative_controls /= 7) call XABORT('AXMAT WHITE UNIT: INCOMPLETE NEGATIVE CONTROLS.')
  write(*,'(A,I0)') 'negative_controls_rejected=',negative_controls
  write(*,'(A)') 'AXMAT-WHITE-NATIVE-UNIT-COMPLETE'
contains
  subroutine rejected()
    if (info == 0) call XABORT('AXMAT WHITE UNIT: MALFORMED INPUT ACCEPTED.')
    negative_controls=negative_controls+1
  end subroutine rejected
end program AXMAT_WHITE_TRACE_UNIT
