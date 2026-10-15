program check_d4a_axial_mesh_probe
  ! Read-only wordwise radial-package comparison and real-track mesh check.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  character(len=512) :: paths(4)
  character(len=12), parameter :: names(*)=[character(len=12) :: &
    'NREG2D','NSNAP','POD-NMODE','VOL2D','POD-BASIS','POD-COEFF', &
    'RADIAL-OP','RADIAL-OP64','POD-SIGMA','POD-REC-ERR','POD-ORTHO', &
    'DRAGON-TXSC','DRAGON-S0XSC']
  type(c_ptr) :: ref,sys,trk,ax,gr,gs,rr,ss
  integer :: i,g,nf,st(40),sr(40),ns,nt,ts,tt,nword,ios
  integer, allocatable :: a(:),b(:),mat(:)
  real, allocatable :: dz(:)
  real(kind=dp) :: k,kstate
  if(command_argument_count()/=4) error stop 'EXPECTED reference system track axial'
  do i=1,4
    call get_command_argument(i,paths(i),status=ios)
    if(ios/=0) error stop 'PATH ARGUMENT'
  enddo
  call LCMOP(ref,trim(paths(1)),2,2,0)
  call LCMOP(sys,trim(paths(2)),2,2,0)
  call LCMOP(trk,trim(paths(3)),2,2,0)
  if(trim(paths(4))/='-') call LCMOP(ax,trim(paths(4)),2,2,0)
  call LCMGET(ref,'STATE-VECTOR',sr)
  call LCMGET(sys,'STATE-VECTOR',st)
  if(sr(8)/=370.or.st(8)/=370) error stop 'GROUP COUNT'
  gr=LCMGID(ref,'GROUP')
  gs=LCMGID(sys,'GROUP')
  do g=1,370
    rr=LCMGIL(gr,g)
    ss=LCMGIL(gs,g)
    do i=1,size(names)
      call LCMLEN(rr,names(i),ns,ts)
      call LCMLEN(ss,names(i),nt,tt)
      if(ns<=0.or.ns/=nt.or.ts/=tt) error stop 'RADIAL RECORD SHAPE'
      if(names(i)=='RADIAL-OP64'.and.ts/=4) error stop 'REAL64 AUTHORITY'
      if(ts<1.or.ts>4) error stop 'RADIAL RECORD TYPE'
      nword=ns
      if(ts==4) nword=2*ns
      allocate(a(nword),b(nword))
      call LCMGET(rr,names(i),a)
      call LCMGET(ss,names(i),b)
      if(any(a/=b)) then
        write(*,*) 'RADIAL WORD MISMATCH ',g,names(i)
        error stop 'RADIAL PACKAGE CHANGED'
      endif
      deallocate(a,b)
    enddo
  enddo
  call LCMGET(trk,'STATE-VECTOR',st)
  nf=st(7)
  if(st(6)/=132.or.st(8)/=3.or.mod(nf,3)/=0) error stop 'TRACK DIMENSIONS'
  if(nf/=3.and.nf/=6.and.nf/=12.and.nf/=24) error stop 'UNDECLARED MESH'
  allocate(mat(nf),dz(nf))
  call LCMGET(trk,'MAT1D',mat)
  call LCMGET(trk,'VOL1D',dz)
  do i=1,nf
    if(mat(i)/=(i-1)/(nf/3)+1) error stop 'TEMPERATURE ZONE'
    if(dz(i)/=150.0/real(nf)) error stop 'MESH WIDTH'
  enddo
  if(trim(paths(4))=='-') then
    write(*,'(A,I0)') 'AXIAL-MESH-STRUCTURE-ONLY PASS NFLOOR=',nf
  else
    call LCMGET(ax,'STATE-VECTOR',sr)
    if(sr(1)/=370.or.sr(2)/=st(2)) error stop 'AXIAL/TRACK DIMENSIONS'
    call LCMGET(ax,'SPOT-KEFF64',k)
    call LCMGET(ax,'SPOT-X-KEFF',kstate)
    if(.not.ieee_is_finite(k).or.k<=0.0_dp.or.k/=kstate) error stop 'K AUTHORITY'
    write(*,'(A,I0,A,ES24.16)') 'AXIAL-MESH-CHECK PASS NFLOOR=',nf,' K64=',k
    call LCMCL(ax,1)
  endif
  call LCMCL(trk,1)
  call LCMCL(sys,1)
  call LCMCL(ref,1)
end program check_d4a_axial_mesh_probe
