program mutate_owned_control
  ! Modify one explicitly owned private XSM clone for a declared negative control.
  ! Never accepts a producer-original path; the owning host checks its exact copy.
  use GANLIB
  use, intrinsic::iso_fortran_env,only:real32,real64
  implicit none
  type(c_ptr)::a,fluxes,f,seal,values,list
  character(len=72)::file
  character(len=32)::mode
  real(real64)::v(14)
  integer::n
  if(command_argument_count()/=2)error stop 'exact private filename and declared mutation'
  call get_command_argument(1,file);call get_command_argument(2,mode)
  if(trim(file)/='negative_pack.xsm'.and.trim(file)/='negative_project.xsm') &
    error stop 'only owning-host private negative clone filenames allowed'
  call LCMOP(a,trim(file),1,2,0)
  if(trim(file)=='negative_project.xsm')then
    if(mode/='global_case')error stop 'declared projected mutation only'
    seal=LCMGID(a,'GLOBAL64');call LCMPTC(seal,'CASE',12,'WRONG-AAA')
  else
    fluxes=LCMGID(a,'FLUX');f=LCMGIL(fluxes,2)
    select case(trim(mode))
    case('missing_seal')
      call LCMDEL(f,'ROOT64-SEAL')
    case('wrong_case','wrong_plane','wrong_epoch')
      seal=LCMGID(f,'ROOT64-SEAL')
      if(mode=='wrong_case')call LCMPTC(seal,'CASE',12,'WRONG-A2')
      if(mode=='wrong_plane')then
        n=1;call LCMPUT(seal,'PLANE',1,1,n)
      endif
      if(mode=='wrong_epoch')then
        n=1;call LCMPUT(seal,'EPOCH',1,1,n)
      endif
    case('flux32','source32')
      if(mode=='flux32')then
        list=LCMGID(f,'FLUX64')
      else
        list=LCMGID(f,'SOUR64')
      endif
      call LCMGDL(list,370,v);call LCMPDL(list,370,14,2,real(v,real32))
    case('LPOD_only')
      ! Retain complete offline typed lists; remove genuine Native producer seal.
      call LCMDEL(f,'ROOT64-SEAL')
      call LCMDEL(f,'ROOT-FLUX64')
    case default
      error stop 'no arbitrary mutation accepted'
    end select
  endif
  call LCMCL(a,1)
end program mutate_owned_control
