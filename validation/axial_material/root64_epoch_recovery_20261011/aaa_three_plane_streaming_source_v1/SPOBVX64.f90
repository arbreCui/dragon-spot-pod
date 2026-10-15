subroutine SPOBVX64(nentry,hentry,ientry,jentry,kentry)
  ! The independent host must first pin+compare the whole nested GLOBAL/ARCH
  ! against the original independent full inputs and the three actual producers.
  ! Its complete proof binds the readonly PROJECT file before/after this child.
  ! Ordered: two private XSM outputs, PROJECT, AX, AXTRACK, AXSYSTEM, AXMACRO,
  ! RCON, three fresh ASM systems, three readonly binary radial tracks.
  use GANLIB
  use SPOR64_VERIFY,only:RECORD_MATCHES
  use, intrinsic::iso_c_binding,only:c_ptr,c_associated
  implicit none
  integer,intent(in)::nentry,ientry(nentry),jentry(nentry)
  character(len=12),intent(in)::hentry(nentry)
  type(c_ptr),intent(in)::kentry(nentry)
  type(c_ptr)::operands(16),global,archive
  integer::kinds(16),access(16),i,j
  character(len=12)::names(16)
  if(nentry/=14)call XABORT('SPOBVX64: EXACT FOURTEEN ORDERED OPERANDS REQUIRED.')
  if(any(ientry(1:2)/=2).or.any(jentry(1:2)/=0)) &
    call XABORT('SPOBVX64: FRESH PRIVATE XSM OUTPUT PAIR REQUIRED.')
  if(any((ientry(3:11)/=1).and.(ientry(3:11)/=2)).or.any(jentry(3:14)/=2)) &
    call XABORT('SPOBVX64: READONLY CONTEXT AND SYSTEMS REQUIRED.')
  if(any(ientry(12:14)/=3))call XABORT('SPOBVX64: BINARY TRACKS REQUIRED.')
  do i=1,14
    if(.not.c_associated(kentry(i)))call XABORT('SPOBVX64: NULL OPERAND.')
    do j=1,i-1
      if(c_associated(kentry(i),kentry(j)).or.hentry(i)==hentry(j)) &
        call XABORT('SPOBVX64: OPERAND ALIAS OR REPEATED NAME.')
    enddo
  enddo
  if(.not.RECORD_MATCHES(kentry(3),'GLOBAL64',-1,0)) &
    call XABORT('SPOBVX64: COMPLETE RETAINED GLOBAL REQUIRED.')
  global=LCMGID(kentry(3),'GLOBAL64')
  if(.not.RECORD_MATCHES(global,'ARCHIVE',-1,0)) &
    call XABORT('SPOBVX64: COMPLETE RETAINED PRODUCER ARCHIVE REQUIRED.')
  archive=LCMGID(global,'ARCHIVE')
  operands(1:3)=kentry(1:3);operands(4)=global
  operands(5:8)=kentry(4:7);operands(9)=archive;operands(10)=kentry(8)
  operands(11:16)=kentry(9:14)
  kinds(1:3)=ientry(1:3);kinds(4)=ientry(3)
  kinds(5:8)=ientry(4:7);kinds(9)=ientry(3);kinds(10)=ientry(8)
  kinds(11:16)=ientry(9:14)
  access(1:2)=0;access(3:16)=2
  names(1:3)=hentry(1:3);names(4)='GLOBAL_VIEW'
  names(5:8)=hentry(4:7);names(9)='ARCH_VIEW';names(10)=hentry(8)
  names(11:16)=hentry(9:14)
  call SPOBOOX64(16,names,kinds,access,operands)
end subroutine SPOBVX64
