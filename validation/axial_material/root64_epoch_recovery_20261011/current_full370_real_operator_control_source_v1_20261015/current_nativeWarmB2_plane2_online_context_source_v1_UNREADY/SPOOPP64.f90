subroutine SPOOPP64(nentry,hentry,ientry,jentry,kentry)
  ! Actual standard CLE entry. Mandatory RANK comes from the externally pinned
  ! case/prepared deck; internal canonical labels never supply authorization.
  use GANLIB
  use SPOR64_VERIFY, only: EMPTY_ROOT,CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  integer::i,j,indic,nitma,rank,impx
  real::flott
  double precision::dflott
  character(len=4)::text4
  character(len=12)::signature
  logical::rank_seen,ok
  type(SPOR64_ROUTE_CONTRACT)::contract,plane_contract
  type(c_ptr)::plane_rcontracts(3)
  if(nentry/=9)call XABORT('SPOOPP64: NINE FULL OPERANDS REQUIRED.')
  if(any(ientry/=1.and.ientry/=2))call XABORT('SPOOPP64: LCM/XSM REQUIRED.')
  if(jentry(1)/=0.or.any(jentry(2:9)/=2))call XABORT('SPOOPP64: FRESH OUTPUT/READONLY INPUTS REQUIRED.')
  do i=1,9
    if(.not.c_associated(kentry(i)))call XABORT('SPOOPP64: NULL OPERAND.')
    if(i>1)then
      if(c_associated(kentry(1),kentry(i)))call XABORT('SPOOPP64: OUTPUT ALIAS.')
    endif
  enddo
  ! GLOBAL and each plane contract are distinct readonly operands.
  ! This structural check does not replace the host's independent full-file pins.
  do i=6,9
    do j=2,i-1
      if(c_associated(kentry(i),kentry(j)))call XABORT('SPOOPP64: CONTRACT OPERAND ALIAS.')
    enddo
  enddo
  if(.not.EMPTY_ROOT(kentry(1)))call XABORT('SPOOPP64: FRESH EMPTY ROOT REQUIRED.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(2),'SIGNATURE',3,12,'L_MACROLIB'))call XABORT('SPOOPP64: AX MACRO.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(3),'SIGNATURE',3,12,'L_TRACK'))call XABORT('SPOOPP64: AX TRACK.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(4),'SIGNATURE',3,12,'L_ARCHIVE'))call XABORT('SPOOPP64: ARCHIVE.')
  if(.not.CHARACTER_RECORD_MATCHES(kentry(5),'SIGNATURE',3,12,'L_PIJ'))call XABORT('SPOOPP64: FIXED BASIS.')
  call SPOR64_RCONTRACT_LOAD(kentry(6),contract,ok)
  if(.not.ok)call XABORT('SPOOPP64: COMPLETE GLOBAL RCONTRACT REQUIRED.')
  plane_rcontracts=kentry(7:9)
  do i=1,3
    call SPOR64_RCONTRACT_LOAD(plane_rcontracts(i),plane_contract,ok)
    if(.not.ok)call XABORT('SPOOPP64: COMPLETE PLANE RCONTRACT REQUIRED.')
  enddo
  rank=0;rank_seen=.false.;impx=1
  do
    call REDGET(indic,nitma,flott,text4,dflott)
    if(indic/=3)call XABORT('SPOOPP64: KEYWORD EXPECTED.')
    if(text4==';')exit
    if(text4=='RANK')then
      if(rank_seen)call XABORT('SPOOPP64: DUPLICATE RANK.')
      call REDGET(indic,rank,flott,text4,dflott)
      if(indic/=1.or.rank<=0)call XABORT('SPOOPP64: EXPLICIT POSITIVE RANK REQUIRED.')
      rank_seen=.true.
    else if(text4=='EDIT')then
      call REDGET(indic,impx,flott,text4,dflott)
      if(indic/=1)call XABORT('SPOOPP64: INTEGER EDIT REQUIRED.')
    else
      call XABORT('SPOOPP64: ONLY RANK/EDIT ARE VALID.')
    endif
  enddo
  if(.not.rank_seen)call XABORT('SPOOPP64: RANK MUST BE EXPLICIT, NO DEFAULT.')
  call SPOASMP64(kentry(1),kentry(2),kentry(3),kentry(4),kentry(5),1,impx,rank,kentry(6),plane_rcontracts)
  signature='L_PIJ'
  call LCMPTC(kentry(1),'SIGNATURE',12,signature)
  call LCMPTC(kentry(1),'LINK.MACRO',12,hentry(2))
  call LCMPTC(kentry(1),'LINK.TRACK',12,hentry(3))
end subroutine SPOOPP64
