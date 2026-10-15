! Deep-copy tracking and add the two declared diagnostic markers only.
program AXMAT_WHITE_TRACE_TRACKING
  use GANLIB
  use AXMAT_WHITE_TRACE_MOD, only: AXMAT_WHITE_CONFIGURE
  implicit none
  type(c_ptr) :: input,output
  character(len=72) :: input_path,output_path
  integer :: marker(4),state(40),length,kind,info
  double precision :: perimeter
  if (command_argument_count() /= 2) call XABORT('AXMAT WHITE TRACK: TWO PATHS REQUIRED.')
  call get_command_argument(1,input_path,length=length)
  if (length > 72) call XABORT('AXMAT WHITE TRACK: INPUT PATH TOO LONG.')
  call get_command_argument(2,output_path,length=length)
  if (length > 72) call XABORT('AXMAT WHITE TRACK: OUTPUT PATH TOO LONG.')
  call LCMOP(input,trim(input_path),2,2,0)
  call LCMLEN(input,'AXMAT-WHITE',length,kind)
  if (length /= 0) call XABORT('AXMAT WHITE TRACK: INPUT ALREADY MARKED.')
  call LCMLEN(input,'AXMAT-W-P',length,kind)
  if (length /= 0) call XABORT('AXMAT WHITE TRACK: INPUT ALREADY MARKED.')
  call LCMLEN(input,'STATE-VECTOR',length,kind)
  if (length /= 40 .or. kind /= 1) call XABORT('AXMAT WHITE TRACK: INVALID STATE.')
  call LCMGET(input,'STATE-VECTOR',state)
  marker=[1,1,8,3]
  perimeter=6.0d0*0.61776479d0
  call AXMAT_WHITE_CONFIGURE(.true.,marker,perimeter,state(6),state(7), &
       state(8),state(15),state(16),state(9),info)
  if (info /= 0) call XABORT('AXMAT WHITE TRACK: OUTSIDE DECLARED SCOPE.')
  call LCMOP(output,trim(output_path),0,2,0)
  call LCMEQU(input,output)
  call LCMPUT(output,'AXMAT-WHITE',4,1,marker)
  call LCMPUT(output,'AXMAT-W-P',1,4,perimeter)
  call LCMCL(output,1)
  call LCMCL(input,1)
  write(*,'(A)') 'AXMAT-WHITE-TRACKING-COMPLETE'
end program AXMAT_WHITE_TRACE_TRACKING
