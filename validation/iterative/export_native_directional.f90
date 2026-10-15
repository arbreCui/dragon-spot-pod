program export_native_directional
  ! Private read-only diagnostic. No replacement of any library routine.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,real64
  implicit none
  integer,parameter :: nr=8,nb=6,nu=14,ng=3
  integer,parameter :: selected(ng)=[51,61,98]
  type(c_ptr) :: track,system,groups,kpsys(1)
  integer :: st(40),mc(40),zone(nu),key(nr,1),cur(nb),bc(nb),pjjind(1,2)
  integer :: m,nmu,nmax,nangl,ntr,nc,fmt,ndim,ispec,n2r,n2s,nalb,ncor,mxsub,mxseg
  integer :: i,j,t,u,g,gg,n,nsub,tf,out,meta,nalbp,typ,ii,c,r,b1,bn
  integer :: matalb(-nb:nr),nom3(3),ka(1),is(nb+1),js(1),key2(nr,2),cur2(nb)
  integer,allocatable :: nseg(:),angle(:),nom(:,:)
  real(real32) :: vol(nu),pjj(nr),pjj_rebuilt(nr),psj(1),tr1(1,1,1),tr2(1,2,2)
  real(real32),allocatable :: sigal(:,:),cpo(:),zmu(:),wzmu(:),harm(:,:,:),rh(:,:)
  real(real64) :: h3(3),pd(nr,1),weight,mux,qplus,qminus,sgn,odd
  real(real64) :: pjsum(nr),f2(2*nr+nb),self2(2*nr),dummy(3)
  real(real64),allocatable :: h2(:,:),wei(:),azx(:),azy(:),hh(:),bb(:)
  real(real64),allocatable :: flight_b(:,:,:),self_d(:,:,:),sp(:),sm(:)
  logical :: lvoid
  character(len=4) :: magic
  character(len=1024) :: dest,metadata
  external :: MCGSCA
  if(command_argument_count()/=2) error stop 'usage: export BINARY METADATA'
  call get_command_argument(1,dest);call get_command_argument(2,metadata)
  call LCMOP(track,'track.xsm',2,2,0);call LCMOP(system,'system.xsm',2,2,0)
  call LCMGET(track,'STATE-VECTOR',st);call LCMGET(track,'MCCG-STATE',mc)
  if(st(1)/=nr.or.st(2)/=nu.or.st(5)/=nb.or.st(6)/=1) error stop 'fixture dimensions'
  if(st(9)/=0.or.mc(15)/=1.or.mc(16)/=1.or.mc(20)/=1) error stop 'need noncyclic P0 STIS'
  m=st(4);nmu=mc(2);nmax=mc(5)
  call LCMGET(track,'V$MCCG',vol);call LCMGET(track,'NZON$MCCG',zone)
  call LCMGET(track,'KEYFLX$ANIS',key);call LCMGET(track,'KEYCUR$MCCG',cur)
  call LCMGET(track,'BC-REFL+TRAN',bc);call LCMGET(track,'PJJIND$MCCG',pjjind)
  if(any(key(:,1)/=[(i,i=1,nr)]).or.any(cur/=[(i,i=nr+1,nu)])) error stop 'identity keys required'
  if(any(bc/=[(i,i=1,nb)]).or.any(pjjind/=1)) error stop 'white identity/P0 PJJ required'
  allocate(cpo(nmu),zmu(nmu),wzmu(nmu),sigal(-6:m,1))
  call LCMGET(track,'XMU$MCCG',cpo);call LCMGET(track,'ZMU$MCCG',zmu)
  call LCMGET(track,'WZMU$MCCG',wzmu)
  open(newunit=tf,file='rays.bin',status='old',action='read',form='unformatted')
  read(tf) magic,nc,ntr,fmt
  do i=1,nc
    read(tf)
  enddo
  read(tf) ndim,ispec,n2r,n2s,nalb,ncor,nangl,mxsub,mxseg
  if(ndim/=2.or.n2r/=nr.or.n2s/=nb.or.ncor/=1.or.mxseg/=nmax.or.mxsub/=1) error stop 'ray layout'
  allocate(azx(nangl),azy(nangl),nseg(ntr),angle(ntr),nom(nmax,ntr),h2(nmax,ntr),wei(ntr))
  allocate(hh(nmax),bb(nmax),sp(nmax),sm(nmax),harm(nmu,3,nangl),rh(nmu,3))
  allocate(flight_b(nmax,nmu,ntr),self_d(nmax,nmu,ntr))
  read(tf);read(tf) matalb;read(tf);read(tf)
  read(tf) (azx(i),azy(i),i=1,nangl)
  read(tf)
  if(any(matalb(1:nr)/=zone(:nr))) error stop 'material mismatch'
  nom=0;h2=0
  do t=1,ntr
    read(tf) nsub,nseg(t),wei(t),angle(t),(nom(i,t),i=1,nseg(t)),(h2(i,t),i=1,nseg(t))
    n=nseg(t)
    if(nsub/=1.or.n<3.or.n>nmax) error stop 'invalid track'
    if(nom(1,t)>=0.or.nom(n,t)>=0.or.any(nom(2:n-1,t)<1).or.any(nom(2:n-1,t)>nr)) &
      error stop 'invalid region ordering'
    if(any(h2(2:n-1,t)<=0).or.wei(t)<=0) error stop 'nonpositive tracking measure'
  enddo
  close(tf)
  do i=1,nangl
    call MOCCHR(2,1,3,nmu,cpo,azx(i),azy(i),rh)
    harm(:,:,i)=rh
  enddo
  call XDRTA2
  groups=LCMGID(system,'GROUP')
  open(newunit=out,file=trim(dest),status='new',access='stream',form='unformatted')
  open(newunit=meta,file=trim(metadata),status='new')
  write(out) 290901,nr,nb,ng,ntr,nmax,nmu,nangl,m
  write(out) selected,zone,vol,cpo,zmu,wzmu,azx,azy,harm,nseg,angle,nom,h2,wei
  write(meta,'(A)') 'Native library coefficients, regional PJJ rebuild and directional-source callback controls'
  write(meta,*) 'dimensions',ntr,nmax,nmu,nangl
  is=0;js=0;tr1=1;ka=1;h3=0;nom3=[nr+1,1,nr+1]
  key2(:,1)=[(i,i=1,nr)];key2(:,2)=[(i,i=nr+1,2*nr)]
  cur2=[(i,i=2*nr+1,2*nr+nb)]
  do gg=1,ng
    g=selected(gg);kpsys(1)=LCMGIL(groups,g)
    call LCMLEN(kpsys(1),'ALBEDO',nalbp,typ)
    call MCGSIG(track,m,1,nalbp,kpsys,sigal,lvoid)
    call LCMGET(kpsys(1),'PJJ$MCCG',pjj)
    if(any(sigal(zone(:nr),1)<=0)) error stop 'positive totals required for this fixture'
    flight_b=0;self_d=0;pjsum=0
    do t=1,ntr
      n=nseg(t)
      do u=1,nmu
        hh=0;bb=0;hh(2:n-1)=h2(2:n-1,t)*real(zmu(u),real64)
        call MCGSCA(n,nu,m,nom(:,t),zone,hh,sigal(0,1),bb)
        flight_b(:,u,t)=bb
        weight=wei(t)*real(wzmu(u),real64)
        do i=2,n-1
          r=nom(i,t);nom3(2)=r;h3(2)=hh(i);pd=0;psj=0
          ! Native per-segment own-source integral, per orientation, unit source and weight.
          call MCGDSCA(m,3,1,0,is,js,h3,ka,nom3,zone,sigal(0,1),1.0_real64, &
            nu,nr,pd,psj,1,1,1,1,1,tr1,.false.,pjjind)
          self_d(i,u,t)=pd(r,1)
          ! Native assembly multiplies D by W before accumulating.
          pjsum(r)=pjsum(r)+pd(r,1)*weight
        enddo
      enddo
    enddo
    call MCGDS6(1,1,nr,pjsum,vol,pjj_rebuilt)
    write(out) sigal(zone(:nr),1),pjj,pjj_rebuilt,pjsum,flight_b,self_d
    write(meta,*) 'group/PJJ max difference',g,maxval(abs(pjj-pjj_rebuilt))
    ! Explicit private source extension: S(r,Omega)=1+s*x_harmonic*r/16.
    ! Native 2D harmonics order is [1,y,x]. No axial odd source is present.
    do c=1,3
      sgn=real(c-2,real64);f2=0;self2=0
      do t=1,ntr
        n=nseg(t);b1=cur2(-nom(1,t));bn=cur2(-nom(n,t))
        do u=1,nmu
          hh=0;hh(2:n-1)=h2(2:n-1,t)*real(zmu(u),real64)
          weight=wei(t)*real(wzmu(u),real64)
          mux=real(harm(u,3,angle(t)),real64)
          tr2(1,1,:)=1;tr2(1,2,1)=real(mux,real32);tr2(1,2,2)=-real(mux,real32)
          sp=0;sm=0
          do i=2,n-1
            r=nom(i,t);odd=sgn*real(r,real64)/16.0_real64
            qplus=1.0_real64+mux*odd;qminus=1.0_real64-mux*odd
            sp(i)=qplus*weight;sm(i)=qminus*weight
            self2(r)=self2(r)+self_d(i,u,t)*(sp(i)+sm(i))
            self2(nr+r)=self2(nr+r)+self_d(i,u,t)*(sp(i)-sm(i))*mux
          enddo
          call MCGFFAR(MCGSCA,nu,2*nr+nb,m,n,hh,nom(:,t),zone,sigal(0,1),sp,sm, &
            nr,1,2,2,tr2,key2,cur2,1,f2,bb)
        enddo
      enddo
      write(out) f2,self2
    enddo
  enddo
  ! Native single-segment controls: thin, moderate and thick optical lengths.
  do ii=1,3
    dummy=[0.001_real64,0.7_real64,100.0_real64]
    sigal=0;sigal(1,1)=2.0_real32
    h3=0;h3(2)=dummy(ii)/2.0_real64;nom3=[-1,1,-2]
    sp(:3)=[0.7_real64,1.3_real64,0.0_real64]
    sm(:3)=[0.0_real64,0.4_real64,1.1_real64]
    tr2(1,1,:)=1;tr2(1,2,1)=1;tr2(1,2,2)=-1;f2=0
    call MCGFFAR(MCGSCA,nu,2*nr+nb,m,3,h3,nom3,zone,sigal(0,1),sp(:3),sm(:3), &
      nr,1,2,2,tr2,key2,cur2,1,f2,bb(:3))
    nom3=[nr+1,1,nr+2];pd=0;psj=0
    call MCGDSCA(m,3,1,0,is,js,h3,ka,nom3,zone,sigal(0,1),1.0_real64, &
      nu,nr,pd,psj,1,1,1,1,1,tr1,.false.,pjjind)
    write(out) h3(2),bb(2),pd(1,1),f2
  enddo
  close(out);close(meta)
  call LCMCL(system,1);call LCMCL(track,1)
end program
