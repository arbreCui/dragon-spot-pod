program probe_native_signed_axial
  ! Private zero-axial-gradient sign extension. Native kernels are unchanged.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer,parameter :: nr=8,nb=6,nu=14
  type(c_ptr) :: track,system,groups,kpsys(1)
  integer :: st(40),mc(40),zone(nu),key(nr,1),cur(nb),bc(nb),pjjind(1,2)
  integer :: m,nmu,nmax,nangl,ntr,ncom,fmt,ndim,ispec,n2r,n2s,nalb,ncor,mxsub,mxseg
  integer :: i,t,u,z,g,lastg,n,nsub,tf,out,inp,nalbp,typ,c,ncase,r,ios
  integer :: matalb(-nb:nr),nom3(3),ka(1),is(nb+1),js(1)
  integer,allocatable :: nseg(:),angle(:),nom(:,:)
  real(real32) :: vol(nu),psj(1),tr1(1,1,1),tr(1,1,2)
  real(real32),allocatable :: sigal(:,:),cpo(:),zmu(:),wzmu(:)
  real(real64) :: h3(3),pd(nr,1),weight
  real(real64),allocatable :: h2(:,:),wei(:),hh(:),bb(:),self_d(:,:,:),sp(:),sm(:)
  real(real64),allocatable :: q(:,:,:),incoming(:,:,:),f(:,:,:),own(:,:,:)
  logical :: lvoid
  character(len=4) :: magic
  character(len=1024) :: source_path,dest
  external :: MCGSCA
  if(command_argument_count()/=2) error stop 'usage: probe INPUT OUTPUT (cwd: real input directory)'
  call get_command_argument(1,source_path);call get_command_argument(2,dest)
  call LCMOP(track,'track.xsm',2,2,0);call LCMOP(system,'system.xsm',2,2,0)
  call LCMGET(track,'STATE-VECTOR',st);call LCMGET(track,'MCCG-STATE',mc)
  if(st(1)/=nr.or.st(2)/=nu.or.st(5)/=nb.or.st(6)/=1) error stop 'fixture dimensions'
  if(st(9)/=0.or.mc(15)/=1.or.mc(16)/=1.or.mc(20)/=1) error stop 'need noncyclic P0 STIS'
  m=st(4);nmu=mc(2);nmax=mc(5)
  call LCMGET(track,'V$MCCG',vol);call LCMGET(track,'NZON$MCCG',zone)
  call LCMGET(track,'KEYFLX$ANIS',key);call LCMGET(track,'KEYCUR$MCCG',cur)
  call LCMGET(track,'BC-REFL+TRAN',bc);call LCMGET(track,'PJJIND$MCCG',pjjind)
  if(any(key(:,1)/=[(i,i=1,nr)]).or.any(cur/=[(i,i=nr+1,nu)])) error stop 'identity keys'
  if(any(bc/=[(i,i=1,nb)]).or.any(pjjind/=1)) error stop 'white identity/P0 PJJ'
  allocate(cpo(nmu),zmu(nmu),wzmu(nmu),sigal(-6:m,1))
  call LCMGET(track,'XMU$MCCG',cpo);call LCMGET(track,'ZMU$MCCG',zmu)
  call LCMGET(track,'WZMU$MCCG',wzmu)
  open(newunit=tf,file='rays.bin',status='old',action='read',form='unformatted')
  read(tf) magic,ncom,ntr,fmt
  do i=1,ncom
    read(tf)
  enddo
  read(tf) ndim,ispec,n2r,n2s,nalb,ncor,nangl,mxsub,mxseg
  if(ndim/=2.or.n2r/=nr.or.n2s/=nb.or.ncor/=1.or.mxseg/=nmax.or.mxsub/=1) error stop 'ray layout'
  allocate(nseg(ntr),angle(ntr),nom(nmax,ntr),h2(nmax,ntr),wei(ntr))
  allocate(hh(nmax),bb(nmax),sp(nmax),sm(nmax),self_d(nmax,nmu,ntr))
  allocate(q(nr,nmu,2),incoming(nb,nmu,2),f(nu,nmu,2),own(nr,nmu,2))
  read(tf);read(tf) matalb
  do i=1,4
    read(tf)
  enddo
  if(any(matalb(1:nr)/=zone(:nr))) error stop 'material mismatch'
  nom=0;h2=0
  do t=1,ntr
    read(tf) nsub,nseg(t),wei(t),angle(t),(nom(i,t),i=1,nseg(t)),(h2(i,t),i=1,nseg(t))
    n=nseg(t)
    if(nsub/=1.or.n<3.or.n>nmax) error stop 'invalid track'
    if(nom(1,t)>=0.or.nom(n,t)>=0.or.any(nom(2:n-1,t)<1).or.any(nom(2:n-1,t)>nr)) &
      error stop 'invalid region ordering'
  enddo
  close(tf);call XDRTA2;groups=LCMGID(system,'GROUP')
  is=0;js=0;tr1=1;tr=1;ka=1;h3=0;nom3=[nr+1,1,nr+1];lastg=0
  open(newunit=inp,file=trim(source_path),status='old',action='read')
  read(inp,*) ncase
  if(ncase<1.or.ncase>1000) error stop 'invalid case count'
  open(newunit=out,file=trim(dest),status='new',access='stream',form='unformatted')
  write(out) 290902,nr,nb,nmu,ncase
  write(out) vol,cpo,zmu,wzmu
  do c=1,ncase
    read(inp,*,iostat=ios) g,q,incoming
    if(ios/=0.or.g<1.or.g>370) error stop 'invalid source record'
    if(.not.all(ieee_is_finite(q)).or..not.all(ieee_is_finite(incoming))) error stop 'nonfinite source'
    if(g/=lastg) then
      kpsys(1)=LCMGIL(groups,g);call LCMLEN(kpsys(1),'ALBEDO',nalbp,typ)
      call MCGSIG(track,m,1,nalbp,kpsys,sigal,lvoid)
      if(any(sigal(zone(:nr),1)<=0)) error stop 'fixture needs positive totals'
      self_d=0
      do t=1,ntr
        n=nseg(t)
        do u=1,nmu
          hh=0;hh(2:n-1)=h2(2:n-1,t)*real(zmu(u),real64)
          do i=2,n-1
            r=nom(i,t);nom3(2)=r;h3(2)=hh(i);pd=0;psj=0
            call MCGDSCA(m,3,1,0,is,js,h3,ka,nom3,zone,sigal(0,1),1.0_real64, &
              nu,nr,pd,psj,1,1,1,1,1,tr1,.false.,pjjind)
            self_d(i,u,t)=pd(r,1)
          enddo
        enddo
      enddo
      lastg=g
    endif
    f=0;own=0
    ! z is independent of planar RP/RM. Both planar orientations use q(:,:,z).
    do z=1,2
      do u=1,nmu
        do t=1,ntr
          n=nseg(t);hh=0;hh(2:n-1)=h2(2:n-1,t)*real(zmu(u),real64)
          weight=0.5_real64*wei(t)*real(wzmu(u),real64)
          sp=0;sm=0
          sp(1)=incoming(-nom(1,t),u,z)*weight
          sm(n)=incoming(-nom(n,t),u,z)*weight
          do i=2,n-1
            r=nom(i,t);sp(i)=q(r,u,z)*weight;sm(i)=sp(i)
            own(r,u,z)=own(r,u,z)+self_d(i,u,t)*(sp(i)+sm(i))
          enddo
          call MCGFFAR(MCGSCA,nu,nu,m,n,hh,nom(:,t),zone,sigal(0,1),sp,sm, &
            nr,1,1,1,tr,key,cur,1,f(:,u,z),bb)
        enddo
      enddo
    enddo
    write(out) g,c,f,own
  enddo
  read(inp,*,iostat=ios)
  if(ios>=0) error stop 'extra source record'
  close(inp);close(out);call LCMCL(system,1);call LCMCL(track,1)
  write(*,*) 'SIGNED AXIAL-STATE NATIVE FLIGHTS COMPLETE',ncase
end program
