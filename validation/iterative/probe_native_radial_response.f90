program probe_native_radial_response
  ! Read-only historical pin fixture; raw native flight before ACA/rebalance.
  ! Probe order is physical regions followed by physical boundary surfaces.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,real64,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer,parameter :: nr=8,nb=6,nu=14,ng=370
  type(c_ptr) :: track,system,groups,kpsys(1)
  integer :: st(40),mc(40),ss(40),key(nr,1,1),cur(nb),zone(nu),bc(nb),idx(nu)
  integer :: pjjind(1,2),isgn(4,1),keyani(1),icode(6)
  integer :: m,nmu,nmax,nangl,nbtr,ncomnt,ifmt,ndim,ispec,n2reg,n2sou,nalbg,ncor,mxsub,mxseg
  integer :: i,j,g,probe,nprobe,ios,inp,out,meta,nalbp,t,tf
  integer :: matalb(-nb:nr)
  real(real32) :: vol(nu),albedo(6)
  real(real32),allocatable :: sigal(:,:),cpo(:),zmu(:),wzmu(:),sc(:)
  real(real64) :: s(nu,1),phi(nu,1),physical(nu)
  real(real64),allocatable :: caz0(:),caz1(:),caz2(:)
  real(real64) :: xsi(nb)
  logical :: nconv(1),lvoid,seen(nu),exists
  character(len=4) :: text4
  character(len=1024) :: input_path,output_path,metadata_path
  external :: MCGFFIR64_RANK_ADAPTER,MCGFFAR,MCGFFAL,MCGSCA

  if(command_argument_count()/=3) call fail('usage: probe INPUT OUTPUT METADATA (cwd contains track/system/rays)')
  call get_command_argument(1,input_path)
  call get_command_argument(2,output_path)
  call get_command_argument(3,metadata_path)
  inquire(file=trim(output_path),exist=exists)
  if(exists) call fail('output exists')
  inquire(file=trim(metadata_path),exist=exists)
  if(exists) call fail('metadata exists')
  call LCMOP(track,'track.xsm',2,2,0)
  call LCMOP(system,'system.xsm',2,2,0)
  call record(track,'STATE-VECTOR',40,1)
  call record(track,'MCCG-STATE',40,1)
  call record(system,'STATE-VECTOR',40,1)
  call LCMGET(track,'STATE-VECTOR',st)
  call LCMGET(track,'MCCG-STATE',mc)
  call LCMGET(system,'STATE-VECTOR',ss)
  write(*,*) 'TRACK STATE',st
  write(*,*) 'MCCG STATE',mc
  write(*,*) 'SYSTEM STATE',ss
  if(st(1)/=nr.or.st(2)/=nu.or.st(5)/=nb.or.st(6)/=1) call fail('fixture dimensions/anisotropy')
  if(st(9)/=0.or.mc(15)/=1.or.mc(16)/=1.or.mc(20)/=1) call fail('noncyclic isotropic STIS required')
  m=st(4);nmu=mc(2);nmax=mc(5)
  if(m<=0.or.nmu<=0.or.nmax<=0) call fail('invalid dimensions')
  call record(system,'GROUP',ng,10)
  groups=LCMGID(system,'GROUP')
  call record(track,'V$MCCG',nu,2)
  call record(track,'NZON$MCCG',nu,1)
  call record(track,'KEYFLX$ANIS',nr,1)
  call record(track,'KEYCUR$MCCG',nb,1)
  call record(track,'BC-REFL+TRAN',nb,1)
  call record(track,'PJJIND$MCCG',2,1)
  call record(track,'ICODE',6,1)
  call record(track,'ALBEDO',6,2)
  call LCMGET(track,'V$MCCG',vol)
  call LCMGET(track,'NZON$MCCG',zone)
  call LCMGET(track,'KEYFLX$ANIS',key)
  call LCMGET(track,'KEYCUR$MCCG',cur)
  call LCMGET(track,'BC-REFL+TRAN',bc)
  call LCMGET(track,'PJJIND$MCCG',pjjind)
  call LCMGET(track,'ICODE',icode)
  call LCMGET(track,'ALBEDO',albedo)
  if(any(vol<=0).or..not.all(ieee_is_finite(vol))) call fail('invalid native weights')
  if(any(zone(:nr)<0).or.any(zone(:nr)>m)) call fail('invalid material index')
  if(any(zone(nr+1:)>=0).or.any(zone(nr+1:)< -6)) call fail('invalid boundary index')
  if(any(pjjind/=1).or.any(bc<1).or.any(bc>nb)) call fail('invalid source isolation/boundary mapping')
  idx(:nr)=key(:,1,1);idx(nr+1:)=cur;seen=.false.
  do i=1,nu
    if(idx(i)<1.or.idx(i)>nu) call fail('invalid unknown mapping')
    if(seen(idx(i))) call fail('duplicate unknown mapping')
    seen(idx(i))=.true.
  enddo
  allocate(cpo(nmu),zmu(nmu),wzmu(nmu),sigal(-6:m,1),sc(0:m))
  call record(track,'XMU$MCCG',nmu,2)
  call record(track,'ZMU$MCCG',nmu,2)
  call record(track,'WZMU$MCCG',nmu,2)
  call LCMGET(track,'XMU$MCCG',cpo)
  call LCMGET(track,'ZMU$MCCG',zmu)
  call LCMGET(track,'WZMU$MCCG',wzmu)
  open(newunit=tf,file='rays.bin',status='old',action='read',form='unformatted',iostat=ios)
  if(ios/=0) call fail('cannot open rays')
  call header()
  allocate(caz0(nangl),caz1(nangl),caz2(nangl))
  read(tf)
  read(tf) matalb
  read(tf)
  read(tf)
  read(tf) (caz1(i),caz2(i),i=1,nangl)
  read(tf)
  if(any(matalb(1:nr)/=zone(:nr))) call fail('ray/material mismatch')
  caz0=0; xsi=0; nconv=.true.
  call MOCIK3(0,1,4,isgn,keyani)
  if(keyani(1)/=0.or.any(isgn/=1)) call fail('isotropic harmonics mismatch')
  call XDRTA2
  open(newunit=inp,file=trim(input_path),status='old',action='read',iostat=ios)
  if(ios/=0) call fail('cannot open probes')
  read(inp,*,iostat=ios) nprobe
  if(ios/=0.or.nprobe<=0.or.nprobe>1000) call fail('invalid probe count')
  open(newunit=out,file=trim(output_path),status='new',action='write')
  open(newunit=meta,file=trim(metadata_path),status='new',action='write')
  write(out,'(A)') 'group,probe,slot,source,response'
  write(meta,'(A)') 'group,slot,key,zone,weight,total,stored_self_scatter,albedo,return_index'
  do probe=1,nprobe
    read(inp,*,iostat=ios) g,physical
    if(ios/=0.or.g<1.or.g>ng) call fail('invalid probe record')
    if(.not.all(ieee_is_finite(physical))) call fail('nonfinite source')
    kpsys(1)=LCMGIL(groups,g)
    call record(kpsys(1),'DRAGON-TXSC',m+1,2)
    call record(kpsys(1),'DRAGON-S0XSC',m+1,2)
    call record(kpsys(1),'PJJ$MCCG',nr,2)
    call LCMLEN(kpsys(1),'ALBEDO',nalbp,t)
    if(nalbp<0.or.any(icode>nalbp)) call fail('albedo extent mismatch')
    call MCGSIG(track,m,1,nalbp,kpsys,sigal,lvoid)
    call LCMGET(kpsys(1),'DRAGON-S0XSC',sc)
    if(.not.all(ieee_is_finite(sigal))) call fail('invalid native coefficients')
    s=0
    do i=1,nu
      s(idx(i),1)=physical(i)
    enddo
    call header()
    do j=1,6
      read(tf)
    enddo
    call MCGFCF(MCGFFIR64_RANK_ADAPTER,MCGFFAR,MCGFFAL,MCGSCA, &
      tf,nbtr,nmax,2,nu,nu,nr,m,1,nangl,nmu,1,1,4,1,1,1,key,cur,zone,nconv, &
      caz0,caz1,caz2,cpo,zmu,wzmu,s,sigal,isgn,0,nb,1,xsi,phi)
    call MCGFST(1,kpsys,nconv,nu,nu,nr,1,1,1,key(:,1,:),cur,pjjind,zone,vol,s,phi,0)
    if(.not.all(ieee_is_finite(phi))) call fail('nonfinite response')
    do i=1,nu
      write(out,'(I0,2(A,I0),2(A,ES25.17E3))') g,',',probe,',',i,',',physical(i),',',phi(idx(i),1)
      if(i<=nr) then
        write(meta,'(I0,3(A,I0),4(A,ES25.17E3),A,I0)') &
          g,',',i,',',idx(i),',',zone(i),',',real(vol(i),real64), &
          ',',real(sigal(zone(i),1),real64),',',real(sc(zone(i)),real64),',',0.0_real64,',',0
      else
        write(meta,'(I0,3(A,I0),4(A,ES25.17E3),A,I0)') &
          g,',',i,',',idx(i),',',zone(i),',',real(vol(i),real64), &
          ',',0.0_real64,',',0.0_real64,',',real(sigal(zone(i),1),real64),',',bc(i-nr)
      endif
    enddo
  enddo
  read(inp,*,iostat=ios)
  if(ios>=0) call fail('extra probe records')
  close(inp);close(out);close(meta);close(tf)
  call LCMCL(system,1);call LCMCL(track,1)
  write(*,'(A,I0)') 'NATIVE-FLIGHT COMPLETE; NO ACA/REBALANCE; PROBES=',nprobe
contains
  subroutine fail(message)
    character(len=*),intent(in) :: message
    write(error_unit,'(A)') 'NATIVE-FLIGHT ERROR: '//message
    error stop 1
  end subroutine
  subroutine record(ptr,name,length,kind)
    type(c_ptr),intent(in) :: ptr
    character(len=*),intent(in) :: name
    integer,intent(in) :: length,kind
    integer :: l,k
    call LCMLEN(ptr,name,l,k)
    if(l/=length.or.k/=kind) call fail('record mismatch: '//name)
  end subroutine
  subroutine header()
    rewind(tf)
    read(tf,iostat=ios) text4,ncomnt,nbtr,ifmt
    if(ios/=0.or.ncomnt<0.or.nbtr<=0) call fail('invalid ray header')
    do j=1,ncomnt
      read(tf)
    enddo
    read(tf,iostat=ios) ndim,ispec,n2reg,n2sou,nalbg,ncor,nangl,mxsub,mxseg
    if(ios/=0) call fail('invalid ray dimensions')
    if(ndim/=2.or.n2reg/=nr.or.n2sou/=nb.or.ncor/=1.or.mxseg/=nmax.or.nangl<=0) &
      call fail('ray dimensions mismatch')
  end subroutine
end program
