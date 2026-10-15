module SPOR64_XSM_RB64
  ! Readonly, complete copy readback after the unchanged B2I physical admission.
  ! Only the explicitly checked CLOSED/SOLVED lifecycle mutations may differ.
  use GANLIB
  use SPOR64_VERIFY,only:EXACT_INVENTORY,CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use, intrinsic::iso_c_binding,only:c_ptr,c_associated
  use, intrinsic::iso_fortran_env,only:int64,real64
  implicit none
  private
  integer,parameter::MAX_DEPTH=64,MAX_NODES=2000000,MAX_RECORD_WORDS=1048576
  public::SEALED_XSM_PAIR_READBACK
contains
  subroutine SEALED_XSM_PAIR_READBACK(axout,arcout,axin,arcin,ok)
    type(c_ptr),intent(in)::axout,arcout,axin,arcin
    logical,intent(out)::ok
    type(c_ptr)::auth,fluxes,flux
    character(len=12),parameter::auth_names(4)= &
      ['RHO         ','NPLANE      ','STATE       ','EPOCH       ']
    real(real64)::rho,got
    integer::nodes,n,p,epoch
    ok=.false.;nodes=0
    if(.not.SAME_DIRECTORY(axin,axout,0,nodes,1))return
    if(.not.SAME_DIRECTORY(arcin,arcout,0,nodes,2))return
    if(.not.CHARACTER_RECORD_MATCHES(axout,'SPOT-X-STATE',3,12,'CLOSED'))return
    if(.not.RECORD_MATCHES(axout,'SPOT-X-EPOCH',1,1))return
    call LCMGET(axout,'SPOT-X-EPOCH',epoch)
    if(epoch/=0)return
    if(.not.RECORD_MATCHES(axout,'SPOT-X-RHO',1,4))return
    call LCMGET(axout,'SPOT-X-RHO',rho)
    if(.not.RECORD_MATCHES(arcout,'SPOT-R64',-1,0))return
    auth=LCMGID(arcout,'SPOT-R64')
    if(.not.EXACT_INVENTORY(auth,auth_names))return
    if(.not.CHARACTER_RECORD_MATCHES(auth,'STATE',3,12,'CLOSED'))return
    if(.not.RECORD_MATCHES(auth,'EPOCH',1,1).or. &
       .not.RECORD_MATCHES(auth,'NPLANE',1,1).or. &
       .not.RECORD_MATCHES(auth,'RHO',1,4))return
    call LCMGET(auth,'EPOCH',epoch);call LCMGET(auth,'NPLANE',n)
    call LCMGET(auth,'RHO',got)
    if(epoch/=0.or.n/=3.or.transfer(got,0_int64)/=transfer(rho,0_int64))return
    if(.not.RECORD_MATCHES(arcout,'FLUX',3,10))return
    fluxes=LCMGID(arcout,'FLUX')
    do p=1,3
      flux=LCMGIL(fluxes,p)
      if(.not.RECORD_MATCHES(flux,'SPOT-R64',-1,0))return
      auth=LCMGID(flux,'SPOT-R64')
      if(.not.CHARACTER_RECORD_MATCHES(auth,'STATE',3,12,'SOLVED'))return
      if(.not.RECORD_MATCHES(auth,'EPOCH',1,1).or. &
         .not.RECORD_MATCHES(auth,'RHO',1,4))return
      call LCMGET(auth,'EPOCH',epoch);call LCMGET(auth,'RHO',got)
      if(epoch/=0.or.transfer(got,0_int64)/=transfer(rho,0_int64))return
    enddo
    ok=.true.
  end subroutine SEALED_XSM_PAIR_READBACK

  logical function SKIP_NAME(name,context)
    character(len=*),intent(in)::name
    integer,intent(in)::context
    SKIP_NAME=.false.
    select case(context)
    case(1)
      SKIP_NAME=name=='SPOT-X-STATE'.or.name=='SPOT-X-EPOCH'
    case(2)
      SKIP_NAME=name=='SPOT-R64'
    case(4)
      SKIP_NAME=name=='RHO'.or.name=='STATE'.or.name=='EPOCH'
    end select
  end function SKIP_NAME

  recursive logical function SAME_DIRECTORY(left,right,depth,nodes,context) result(equal)
    type(c_ptr),intent(in)::left,right
    integer,intent(in)::depth,context
    integer,intent(inout)::nodes
    character(len=72)::file_name
    character(len=12)::directory,item_name,first_name
    integer::le,re,ll,lt,rl,rt,child_context,nleft,nright
    logical::empty_left,empty_right,memory
    type(c_ptr)::a,b
    equal=.false.
    if(depth>MAX_DEPTH.or..not.c_associated(left).or..not.c_associated(right))return
    call LCMINF(left,file_name,directory,empty_left,le,memory)
    call LCMINF(right,file_name,directory,empty_right,re,memory)
    if(le/=-1.or.re/=-1)return
    nleft=0;nright=0
    if(.not.empty_left)then
      item_name=' ';call LCMNXT(left,item_name);first_name=item_name
      do
        nodes=nodes+1
        if(nodes>MAX_NODES.or.item_name==' ')return
        if(.not.SKIP_NAME(item_name,context))then
          nleft=nleft+1
          call LCMLEN(left,item_name,ll,lt);call LCMLEN(right,item_name,rl,rt)
          if(ll/=rl.or.lt/=rt)return
          child_context=0
          if(context==2.and.item_name=='FLUX')child_context=3
          if(context==3.and.item_name=='SPOT-R64')child_context=4
          if(lt==0)then
            if(ll/=-1)return
            a=LCMGID(left,item_name);b=LCMGID(right,item_name)
            if(.not.SAME_DIRECTORY(a,b,depth+1,nodes,child_context))return
          else if(lt==10)then
            if(ll<=0)return
            a=LCMGID(left,item_name);b=LCMGID(right,item_name)
            if(.not.SAME_LIST(a,b,ll,depth+1,nodes,child_context))return
          else
            if(.not.SAME_RECORD(left,right,item_name,0,ll,lt))return
          endif
        endif
        call LCMNXT(left,item_name)
        if(item_name==first_name)exit
      enddo
    endif
    if(.not.empty_right)then
      item_name=' ';call LCMNXT(right,item_name);first_name=item_name
      do
        nodes=nodes+1
        if(nodes>MAX_NODES.or.item_name==' ')return
        if(.not.SKIP_NAME(item_name,context))nright=nright+1
        call LCMNXT(right,item_name)
        if(item_name==first_name)exit
      enddo
    endif
    equal=nleft==nright
  end function SAME_DIRECTORY

  recursive logical function SAME_LIST(left,right,extent,depth,nodes,context) result(equal)
    type(c_ptr),intent(in)::left,right
    integer,intent(in)::extent,depth,context
    integer,intent(inout)::nodes
    integer::i,ll,lt,rl,rt
    type(c_ptr)::a,b
    equal=.false.
    if(depth>MAX_DEPTH.or.extent<=0.or..not.c_associated(left).or..not.c_associated(right))return
    do i=1,extent
      nodes=nodes+1
      if(nodes>MAX_NODES)return
      call LCMLEL(left,i,ll,lt);call LCMLEL(right,i,rl,rt)
      if(ll/=rl.or.lt/=rt)return
      if(lt==99.and.ll==0)cycle
      if(lt==0)then
        if(ll/=-1)return
        a=LCMGIL(left,i);b=LCMGIL(right,i)
        if(.not.SAME_DIRECTORY(a,b,depth+1,nodes,context))return
      else if(lt==10)then
        if(ll<=0)return
        a=LCMGIL(left,i);b=LCMGIL(right,i)
        if(.not.SAME_LIST(a,b,ll,depth+1,nodes,context))return
      else
        if(.not.SAME_RECORD(left,right,' ',i,ll,lt))return
      endif
    enddo
    equal=.true.
  end function SAME_LIST

  logical function SAME_RECORD(left,right,name,index,length,type_code)
    type(c_ptr),intent(in)::left,right
    character(len=*),intent(in)::name
    integer,intent(in)::index,length,type_code
    integer(int64)::nw
    integer::words,istat
    integer,allocatable::a(:),b(:)
    SAME_RECORD=.false.
    if(length<=0.or.type_code<1.or.type_code>6)return
    nw=int(length,int64)
    if(type_code==4.or.type_code==6)nw=2_int64*nw
    if(nw>MAX_RECORD_WORDS)return
    words=int(nw);allocate(a(words),b(words),stat=istat)
    if(istat/=0)return
    if(index==0)then
      call LCMGET(left,name,a);call LCMGET(right,name,b)
    else
      call LCMGDL(left,index,a);call LCMGDL(right,index,b)
    endif
    SAME_RECORD=all(a==b)
  end function SAME_RECORD
end module SPOR64_XSM_RB64
