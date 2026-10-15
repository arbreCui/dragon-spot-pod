program compare_saved_axial
  ! Read-only comparison of same-grid or uniformly nested SPOT axial states.
  ! Physical scalar flux uses FLUX64 and its own global nu-fission integral.
  use GANLIB
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  type state
    integer :: ng,nr,nf,ns
    real(dp) :: k,f,norm32,leak
    real(dp),allocatable :: phi(:,:,:),area(:),dz(:),zone(:),a(:),gram(:),h(:),l(:)
    integer,allocatable :: rank(:),off(:),goff(:),zoneid(:)
    real,allocatable :: basis(:)
  end type
  type(state) :: a,b
  character(72) :: paths(6)
  integer :: i,j,g,r,n,ratio,lo,hi,s,ia,ib,idx,idx2,ig
  real(dp) :: x,y,num,den,w,ra,dl,rl,dr,physical,maxdiff,zchange
  logical :: physical_only
  character(32) :: option
  physical_only=.false.
  if(command_argument_count()==7) then
    call get_command_argument(7,option)
    if(trim(option)/='--physical-only') error stop 'unknown comparison option'
    physical_only=.true.
  else if(command_argument_count()/=6) then
    error stop 'six paths: AX TRACK MAC AX TRACK MAC [--physical-only]'
  endif
  do i=1,6
    call get_command_argument(i,length=n)
    if(n>len(paths(i))) error stop 'use short XSM paths'
    call get_command_argument(i,paths(i))
  enddo
  call load(a,paths(1:3))
  call load(b,paths(4:6))
  if(a%ng/=b%ng.or.a%nr/=b%nr.or.a%ns/=b%ns) error stop 'geometry/groups'
  if(mod(b%nf,a%nf)/=0) error stop 'second grid must refine first'
  if(any(a%area/=b%area)) error stop 'radial areas differ'
  if(.not.physical_only) then
    if(any(a%rank/=b%rank).or.any(a%off/=b%off).or.any(a%goff/=b%goff)) error stop 'modal layout'
    if(size(a%basis)/=size(b%basis)) error stop 'basis length'
    if(any(a%basis/=b%basis).or.any(a%gram/=b%gram).or.any(a%h/=b%h)) error stop 'fixed space'
  endif
  ratio=b%nf/a%nf
  num=0;den=0;maxdiff=0
  do i=1,a%nf
    lo=(i-1)*ratio+1;hi=i*ratio
    if(sum(b%dz(lo:hi))/=a%dz(i)) error stop 'nonmatching axial widths'
    if(any(b%zoneid(lo:hi)/=a%zoneid(i))) error stop 'physical zone map'
    do g=1,a%ng
      do r=1,a%nr
        x=a%phi(i,r,g)/a%f
        if(ratio==1) then
          y=b%phi(i,r,g)/b%f
        else
          y=sum(b%phi(lo:hi,r,g)*b%dz(lo:hi))/(a%dz(i)*b%f)
        endif
        w=a%area(r)*a%dz(i)
        num=num+w*(y-x)**2;den=den+w*y*y
        maxdiff=max(maxdiff,abs(y-x))
      enddo
    enddo
  enddo
  if(den<=0) error stop 'zero physical norm'
  physical=sqrt(num/den)
  if(.not.physical_only) then
  num=0;den=0
  do g=1,a%ng
    n=a%rank(g)
    do s=1,a%ns
      do ia=1,n
        idx=a%off(g)+(s-1)*n+ia
        do ib=1,n
          idx2=a%off(g)+(s-1)*n+ib;ig=a%goff(g)+(ib-1)*n+ia
          num=num+a%h(s)*(b%a(idx)-a%a(idx))*a%gram(ig)*(b%a(idx2)-a%a(idx2))
          den=den+a%h(s)*b%a(idx)*a%gram(ig)*b%a(idx2)
        enddo
      enddo
    enddo
  enddo
  if(num<0.or.den<=0) error stop 'invalid modal norm'
  ra=sqrt(num/den)
  endif
  dl=maxval(abs(b%l-a%l));rl=0
  w=max(maxval(abs(a%l)),maxval(abs(b%l)))
  if(w>0) rl=dl/w
  dr=1/a%k-1/b%k
  write(*,'(a,2i8)') 'NFLOOR ',a%nf,b%nf
  write(*,'(a,2es25.17)') 'K64 ',a%k,b%k
  write(*,'(a,es25.17)') 'REACTIVITY_CHANGE_PCM ',1e5_dp*dr
  if(physical_only) then
    write(*,'(a,3es25.17)') 'RRHO_RLEAK_DLEAK ',abs(dr),rl,dl
    write(*,'(a)') 'MODAL_COMPARISON OMITTED_PHYSICAL_ONLY'
  else
    write(*,'(a,4es25.17)') 'CANONICAL_RRHO_RLEAK_DLEAK_RA ',abs(dr),rl,dl,ra
  endif
  write(*,'(a,es25.17)') 'PHYSICAL_FLUX_RELATIVE_VOLUME_L2 ',physical
  write(*,'(a,es25.17)') 'PHYSICAL_FLUX_MAX_ABSOLUTE ',maxdiff
  write(*,'(a,2es25.17)') 'FISSION_NORM64 ',a%f,b%f
  write(*,'(a,2es25.17)') 'SAVED_FISSION_NORM32 ',a%norm32,b%norm32
  write(*,'(a,2es25.17)') 'SOURCE_NORMALIZED_LEAKAGE64 ',a%k*a%leak/a%f,b%k*b%leak/b%f
  write(*,'(a,3es25.17)') 'ZONE_FRACTIONS64_A ',a%zone/a%f
  write(*,'(a,3es25.17)') 'ZONE_FRACTIONS64_B ',b%zone/b%f
  write(*,'(a)') 'SAVED-AXIAL-COMPARISON COMPLETE; DIAGNOSTIC ONLY'
contains
  subroutine require(p,key,n,t)
    type(c_ptr),intent(in) :: p
    character(*),intent(in) :: key
    integer,intent(in) :: n,t
    integer :: nn,tt
    call LCMLEN(p,key,nn,tt)
    if(nn/=n.or.tt/=t) then
      write(*,*) 'bad record ',key,nn,tt,n,t
      error stop 'record shape/type'
    endif
  end subroutine
  subroutine vector(p,key,out)
    type(c_ptr),intent(in) :: p
    character(*),intent(in) :: key
    real(dp),allocatable,intent(out) :: out(:)
    integer :: nn,tt
    call LCMLEN(p,key,nn,tt)
    if(nn<1.or.tt/=4) error stop 'missing REAL64 vector'
    allocate(out(nn));call LCMGET(p,key,out)
    if(any(.not.ieee_is_finite(out))) error stop 'nonfinite vector'
  end subroutine
  subroutine load(v,names)
    type(state),intent(out) :: v
    character(*),intent(in) :: names(3)
    type(c_ptr) :: ax,trk,mac,fl,mg,grp
    integer :: st(40),ms(40),fs(40),ng,nr,nf,ns,nu,nm,nfis,ll4,g,r,z,reg,k,n,t,ff
    integer,allocatable :: key(:),mat(:)
    real,allocatable :: vol(:),area(:),dz(:),sigf(:)
    real(dp),allocatable :: unknown(:)
    real(dp) :: prod,rr
    call LCMOP(ax,names(1),2,2,0);call LCMOP(trk,names(2),2,2,0);call LCMOP(mac,names(3),2,2,0)
    call require(ax,'STATE-VECTOR',40,1);call require(trk,'STATE-VECTOR',40,1)
    call require(mac,'STATE-VECTOR',40,1)
    call LCMGET(ax,'STATE-VECTOR',fs);call LCMGET(trk,'STATE-VECTOR',st);call LCMGET(mac,'STATE-VECTOR',ms)
    ng=fs(1);nr=st(6);nf=st(7);ns=st(8);nu=st(2);nm=ms(2);nfis=ms(4);ll4=st(11)
    if(min(ng,nr,nf,nu,nm,nfis)<=0.or.ns/=3.or.st(1)/=nr*nf.or.ng/=ms(1)) error stop 'dimensions'
    v%ng=ng;v%nr=nr;v%nf=nf;v%ns=ns
    allocate(key(nr*nf),mat(nr*nf),vol(nr*nf),area(nr),dz(nf),sigf(nm*nfis),unknown(nu))
    allocate(v%phi(nf,nr,ng),v%zone(ns),v%zoneid(nf),v%rank(ng),v%off(ng+1),v%goff(ng+1))
    call require(trk,'KEYFLX',nr*nf,1);call require(trk,'MATCOD',nr*nf,1)
    call require(trk,'VOLUME',nr*nf,2);call require(trk,'AREA2D',nr,2);call require(trk,'VOL1D',nf,2)
    call require(trk,'MAT1D',nf,1)
    call LCMGET(trk,'KEYFLX',key);call LCMGET(trk,'MATCOD',mat);call LCMGET(trk,'VOLUME',vol)
    call LCMGET(trk,'AREA2D',area);call LCMGET(trk,'VOL1D',dz);call LCMGET(trk,'MAT1D',v%zoneid)
    if(any(key<1).or.any(key>nu).or.any(mat<1).or.any(mat>nm)) error stop 'inactive/invalid region'
    if(any(v%zoneid<1).or.any(v%zoneid>ns).or.any(area<=0).or.any(dz<=0)) error stop 'geometry values'
    if(ll4+nr*(nf+1)>nu) error stop 'current layout'
    v%area=real(area,dp);v%dz=real(dz,dp);v%f=0;v%zone=0;v%leak=0
    call require(ax,'FLUX64',ng,10);fl=LCMGID(ax,'FLUX64');mg=LCMGID(mac,'GROUP')
    do g=1,ng
      call LCMLEL(fl,g,n,t)
      if(n/=nu.or.t/=4) error stop 'flux64 shape'
      call LCMGDL(fl,g,unknown)
      if(any(.not.ieee_is_finite(unknown))) error stop 'nonfinite flux'
      grp=LCMGIL(mg,g);call LCMLEN(grp,'NUSIGF',n,t);sigf=0
      if(n>0) then
        if(n/=nm*nfis.or.t/=2) error stop 'fission vector'
        call LCMGET(grp,'NUSIGF',sigf)
      endif
      do r=1,nr
        do z=1,nf
          reg=(r-1)*nf+z;k=mat(reg)
          if(abs(real(vol(reg),dp)-v%area(r)*v%dz(z))>0.5_dp*real(spacing(vol(reg)),dp)) &
            error stop 'volume mapping'
          v%phi(z,r,g)=unknown(key(reg));prod=0
          do ff=1,nfis
            prod=prod+real(sigf((ff-1)*nm+k),dp)
          enddo
          rr=real(vol(reg),dp)*v%phi(z,r,g)*prod
          v%f=v%f+rr;v%zone(v%zoneid(z))=v%zone(v%zoneid(z))+rr
        enddo
        v%leak=v%leak+v%area(r)*(unknown(ll4+r*(nf+1))-unknown(ll4+(r-1)*(nf+1)+1))
      enddo
    enddo
    if(v%f<=0) error stop 'fission norm'
    call require(ax,'SPOT-X-KEFF',1,4);call LCMGET(ax,'SPOT-X-KEFF',v%k)
    call require(ax,'SPOT-X-NORM',1,4);call LCMGET(ax,'SPOT-X-NORM',v%norm32)
    call require(ax,'SPOT-X-RANK',ng,1);call require(ax,'SPOT-X-OFF',ng+1,1)
    call require(ax,'SPOT-X-GOFF',ng+1,1)
    call LCMGET(ax,'SPOT-X-RANK',v%rank);call LCMGET(ax,'SPOT-X-OFF',v%off)
    call LCMGET(ax,'SPOT-X-GOFF',v%goff)
    call vector(ax,'SPOT-X-A',v%a);call vector(ax,'SPOT-X-GRAM',v%gram)
    call vector(ax,'SPOT-X-H',v%h);call vector(ax,'SPOT-X-L',v%l)
    if(size(v%a)/=v%off(ng+1).or.size(v%gram)/=v%goff(ng+1)) error stop 'canonical sizes'
    if(size(v%h)/=ns.or.size(v%l)/=ng*ns) error stop 'canonical zone sizes'
    if(any(v%off(2:)-v%off(:ng)/=ns*v%rank)) error stop 'coordinate offsets'
    if(any(v%goff(2:)-v%goff(:ng)/=v%rank**2)) error stop 'gram offsets'
    call LCMLEN(ax,'SPOT-X-BASIS',n,t)
    if(n<1.or.t/=2) error stop 'basis'
    allocate(v%basis(n));call LCMGET(ax,'SPOT-X-BASIS',v%basis)
    call LCMCL(ax,1);call LCMCL(trk,1);call LCMCL(mac,1)
  end subroutine
end program
