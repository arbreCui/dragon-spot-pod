subroutine APACKX64(nentry,hentry,ientry,jentry,kentry)
  ! Three independent original actual Native producer files; never repeat plane1.
  ! Four fresh XSM outputs: ARCHIVE, RCON1, RCON2, RCON3; then A1 A2 A3 readonly.
  use GANLIB
  use SPOR64_XSM_STORE64,only:EMPTY_XSM_ROOT
  use SPOR64_BOOT64,only:SPOR64_BOOT64_READ_NATIVE,ROOT64_LOADED,SPOR64_BOOT64_SAME_TREE
  use SPOR64_VERIFY,only:EXACT_INVENTORY,CHARACTER_RECORD_MATCHES,RECORD_MATCHES,LIST_ITEM_IS_DIRECTORY
  use SPOR64_RCONTRACT,only:SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  use, intrinsic::iso_fortran_env,only:real64
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  character(len=12),parameter::fields(6)= &
    ['TRACK       ','MICROLIB2   ','SYSTEM      ','FLUX        ','RCONTRACT   ','BOOT_BIND   ']
  character(len=12),parameter::root_names(8)= &
    ['SIGNATURE   ','LISTDIM     ','TRACK       ','MICROLIB2   ','SYSTEM      ','FLUX        ','RCONTRACT   ','BOOT_BIND   ']
  character(len=12),parameter::cases(3)= &
    ['R64WARM-A-V1 ','R64-A2-WARM1 ','R64-A3-WARM1 ']
  character(len=12),parameter::archive_signature='L_ARCHIVE'
  type(c_ptr)::inputs(6,3),outputs(6),list,item,seal
  type(SPOR64_ROUTE_CONTRACT)::route
  real(real64),allocatable::admitted(:,:)
  integer::i,j,p,k,n,pl,ep,status,indic,ival
  real::rval
  double precision::dval
  character(len=12)::token
  logical::ok
  if(nentry/=7)call XABORT('APACKX64: FOUR OUTPUTS AND THREE INDEPENDENT INPUTS REQUIRED.')
  if(any(ientry/=2).or.any(jentry(1:4)/=0).or.any(jentry(5:7)/=2)) &
    call XABORT('APACKX64: STRICT FRESH XSM / READONLY XSM ORDER REQUIRED.')
  do i=1,7
    if(.not.c_associated(kentry(i)))call XABORT('APACKX64: NULL OPERAND.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
        call XABORT('APACKX64: INDEPENDENT DISTINCT OPERANDS REQUIRED.')
    enddo
    if(i<=4)then
      if(.not.EMPTY_XSM_ROOT(kentry(i)))call XABORT('APACKX64: EMPTY PRIVATE OUTPUT REQUIRED.')
    endif
  enddo
  call REDGET(indic,ival,rval,token,dval)
  if(indic/=3.or.token/=';')call XABORT('APACKX64: NO SYNTHETIC PRODUCER OPTIONS ALLOWED.')
  do p=1,3
    if(.not.EXACT_INVENTORY(kentry(4+p),root_names))call XABORT('APACKX64: COMPLETE ORIGINAL INVENTORY REQUIRED.')
    if(.not.CHARACTER_RECORD_MATCHES(kentry(4+p),'SIGNATURE',3,12,'L_ARCHIVE')) &
      call XABORT('APACKX64: ORIGINAL ARCHIVE SIGNATURE REQUIRED.')
    if(.not.RECORD_MATCHES(kentry(4+p),'LISTDIM',1,1))call XABORT('APACKX64: LISTDIM TYPE.')
    call LCMGET(kentry(4+p),'LISTDIM',n)
    if(n/=1)call XABORT('APACKX64: EACH ORIGINAL PRODUCER MUST HAVE ONE SLOT.')
    do k=1,6
      if(.not.RECORD_MATCHES(kentry(4+p),fields(k),1,10))call XABORT('APACKX64: ORIGINAL LIST EXTENT/TYPE.')
      list=LCMGID(kentry(4+p),fields(k))
      if(.not.LIST_ITEM_IS_DIRECTORY(list,1))call XABORT('APACKX64: ORIGINAL ITEM DIRECTORY.')
      inputs(k,p)=LCMGIL(list,1)
    enddo
    call SPOR64_RCONTRACT_LOAD(inputs(5,p),route,ok)
    if(.not.ok.or.route%case_name/=cases(p))call XABORT('APACKX64: OWN PLANE CASE REQUIRED.')
    if(.not.RECORD_MATCHES(inputs(6,p),'PLANE',1,1).or. &
       .not.RECORD_MATCHES(inputs(6,p),'EPOCH',1,1))call XABORT('APACKX64: ORIGINAL BIND TYPE.')
    call LCMGET(inputs(6,p),'PLANE',pl);call LCMGET(inputs(6,p),'EPOCH',ep)
    if(pl/=p.or.ep/=0)call XABORT('APACKX64: ORIGINAL PLANE/E0 BIND REQUIRED.')
    call SPOR64_BOOT64_READ_NATIVE(inputs(4,p),inputs(1,p),inputs(3,p), &
      inputs(2,p),inputs(5,p),p,0,admitted,status)
    if(status/=ROOT64_LOADED.or..not.allocated(admitted))call XABORT('APACKX64: FULL REAL NATIVE READ REFUSED.')
    if(any(shape(admitted)/=[14,370]))call XABORT('APACKX64: ORIGINAL FULL370/NONSCALAR EXTENT.')
    deallocate(admitted)
  enddo
  ! All three actual producers are independently admitted before the first write.
  call LCMPTC(kentry(1),'SIGNATURE',12,archive_signature)
  n=3;call LCMPUT(kentry(1),'LISTDIM',1,1,n)
  do k=1,6
    outputs(k)=LCMLID(kentry(1),fields(k),3)
  enddo
  do p=1,3
    do k=1,6
      item=LCMDIL(outputs(k),p);call LCMEQU(inputs(k,p),item)
      if(.not.SPOR64_BOOT64_SAME_TREE(inputs(k,p),item))call XABORT('APACKX64: WHOLE ITEM READBACK FAILED.')
    enddo
    call LCMEQU(inputs(5,p),kentry(1+p))
    if(.not.SPOR64_BOOT64_SAME_TREE(inputs(5,p),kentry(1+p)))call XABORT('APACKX64: OWN CONTRACT READBACK FAILED.')
  enddo
  if(.not.EXACT_INVENTORY(kentry(1),root_names))call XABORT('APACKX64: EXACT OUTPUT INVENTORY FAILED.')
end subroutine APACKX64
