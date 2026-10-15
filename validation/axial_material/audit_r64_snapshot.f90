program audit_r64_snapshot
  ! Read the actual saved authority, rebuild all group sources, and solve
  ! one fresh frozen-source image without modifying the saved archive.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,real64,int32,int64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use SPOR64_A8, only: DOORFV64
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT
  implicit none
  integer, parameter :: ng=370,nr=8,nu=14,nm=8,nf=32
  type(c_ptr) :: archive,file_archive,track,flux,micro,macro,system,groups,fg64,fg32,sg64,g,sg
  type(SPOR64_ROUTE_CONTRACT) :: contract
  integer :: key(nr),mat(nr),sv(40),n,t,i,j,ir,ig,jg,is,ib,jnd,u
  integer :: njj(nm),ijj(nm),ipos(nm),npsys(ng)
  integer(int64) :: cutoff
  real(real32) :: volume(nr),k32,controls(4),eps(5)
  real(real32) :: flux32(nu,ng),nuf(nm,nf,ng),chi(nm,nf,ng)
  real(real32) :: total(0:nm,ng),within(0:nm,ng)
  real(real32),allocatable :: scat(:,:,:),packed(:)
  real(real64) :: k,phi(nu,ng),saved_source(nu,ng),q(nu,ng),fresh(nu,ng)
  real(real64) :: production(nr,nf),leakage(ng)
  logical :: ok
  character(len=12) :: signature
  character(len=72) :: title
  call LCMOP(file_archive,'snapshot_A.xsm',2,2,0)
  call LCMOP(archive,'AUDITMEM',0,1,0)
  call LCMEQU(file_archive,archive)
  call LCMCL(file_archive,1)
  call LCMGTC(archive,'SIGNATURE',12,signature)
  if(signature/='L_ARCHIVE') call fail('not archive')
  call require(archive,'LISTDIM',1,1)
  call LCMGET(archive,'LISTDIM',n)
  if(n/=1) call fail('not one snapshot')
  track=object('TRACK');flux=object('FLUX');micro=object('MICROLIB2');system=object('SYSTEM')
  macro=LCMGID(micro,'MACROLIB')
  call require(flux,'STATE-VECTOR',40,1);call LCMGET(flux,'STATE-VECTOR',sv)
  if(sv(1)/=ng.or.sv(2)/=nu.or.sv(6)/=2) call fail('wrong flux shape/type')
  call require(macro,'STATE-VECTOR',40,1);call LCMGET(macro,'STATE-VECTOR',sv)
  if(sv(1)/=ng.or.sv(2)/=nm.or.sv(4)/=nf) call fail('wrong macro shape')
  call require(track,'KEYFLX',nr,1);call LCMGET(track,'KEYFLX',key)
  call require(track,'MATCOD',nr,1);call LCMGET(track,'MATCOD',mat)
  call require(track,'VOLUME',nr,2);call LCMGET(track,'VOLUME',volume)
  if(any(key<1).or.any(key>nu).or.any(mat/=[(i,i=1,nr)])) call fail('bad mapping')
  do i=1,nr
    if(count(key==key(i))/=1) call fail('duplicate scalar index')
  enddo
  if(any(volume<=0).or..not.all(ieee_is_finite(volume))) call fail('bad volume')
  call require(flux,'EPS-CONVERGE',5,2);call LCMGET(flux,'EPS-CONVERGE',eps)
  if(any(eps(1:3)/=2.5e-7_real32).or.any(eps(4:5)/=0.0_real32)) call fail('wrong outer controls')
  call require(track,'REAL-PARAM',4,2);call LCMGET(track,'REAL-PARAM',controls)
  if(controls(1)/=2.5e-8_real32.or.any(controls(2:4)/=0.0_real32)) call fail('wrong inner controls')
  call require(flux,'SPOT-KEFF64',1,4);call LCMGET(flux,'SPOT-KEFF64',k)
  call require(flux,'K-EFFECTIVE',1,2);call LCMGET(flux,'K-EFFECTIVE',k32)
  if(.not.ieee_is_finite(k).or.k<=0) call fail('bad k')
  if(transfer(real(k,real32),0_int32)/=transfer(k32,0_int32)) call fail('k mirror differs')
  call require(flux,'FLUX64',ng,10);fg64=LCMGID(flux,'FLUX64')
  call require(flux,'FLUX',ng,10);fg32=LCMGID(flux,'FLUX')
  call require(flux,'SOUR64',ng,10);sg64=LCMGID(flux,'SOUR64')
  do ig=1,ng
    call LCMLEL(fg64,ig,n,t)
    if(n/=nu.or.t/=4) call fail('bad double group')
    call LCMGDL(fg64,ig,phi(:,ig))
    call LCMLEL(fg32,ig,n,t)
    if(n/=nu.or.t/=2) call fail('bad float group')
    call LCMGDL(fg32,ig,flux32(:,ig))
    call LCMLEL(sg64,ig,n,t)
    if(n/=nu.or.t/=4) call fail('bad double source')
    call LCMGDL(sg64,ig,saved_source(:,ig))
    do i=1,nu
      if(transfer(real(phi(i,ig),real32),0_int32)/=transfer(flux32(i,ig),0_int32)) &
        call fail('flux mirror differs')
    enddo
  enddo
  if(.not.all(ieee_is_finite(phi)).or..not.all(ieee_is_finite(saved_source))) call fail('nonfinite field')
  if(any(phi(key,:)<=0)) call fail('nonpositive scalar field')
  allocate(scat(nm,ng,ng));scat=0.0_real32
  groups=LCMGID(macro,'GROUP');sg=LCMGID(system,'GROUP')
  do ig=1,ng
    g=LCMGIL(groups,ig)
    call require(g,'NUSIGF',nm*nf,2);call LCMGET(g,'NUSIGF',nuf(:,:,ig))
    call require(g,'CHI',nm*nf,2);call LCMGET(g,'CHI',chi(:,:,ig))
    call require(g,'NJJS00',nm,1);call LCMGET(g,'NJJS00',njj)
    call require(g,'IJJS00',nm,1);call LCMGET(g,'IJJS00',ijj)
    call require(g,'IPOS00',nm,1);call LCMGET(g,'IPOS00',ipos)
    call LCMLEN(g,'SCAT00',n,t)
    if(n<1.or.n>nm*ng.or.t/=2) call fail('bad scattering length')
    allocate(packed(n));call LCMGET(g,'SCAT00',packed)
    do ib=1,nm
      do jnd=1,njj(ib)
        jg=ijj(ib)-jnd+1;j=ipos(ib)+jnd-1
        if(j<1.or.j>n.or.jg<1.or.jg>ng) call fail('bad scattering index')
        scat(ib,ig,jg)=packed(j)
      enddo
    enddo
    deallocate(packed)
    g=LCMGIL(sg,ig)
    call require(g,'DRAGON-TXSC',nm+1,2);call LCMGET(g,'DRAGON-TXSC',total(:,ig))
    call require(g,'DRAGON-S0XSC',nm+1,2);call LCMGET(g,'DRAGON-S0XSC',within(:,ig))
  enddo
  if(.not.all(ieee_is_finite(nuf)).or..not.all(ieee_is_finite(chi)).or. &
     .not.all(ieee_is_finite(scat))) call fail('nonfinite coefficient')
  production=0.0_real64
  do ir=1,nr
    do is=1,nf
      do ig=1,ng
        production(ir,is)=production(ir,is)+real(nuf(mat(ir),is,ig),real64)*phi(key(ir),ig)
      enddo
    enddo
  enddo
  q=0.0_real64
  do ir=1,nr
    ib=mat(ir)
    do ig=1,ng
      do is=1,nf
        q(key(ir),ig)=q(key(ir),ig)+real(chi(ib,is,ig),real64)*production(ir,is)/k
      enddo
      do jg=1,ng
        if(jg==ig) cycle
        q(key(ir),ig)=q(key(ir),ig)+real(scat(ib,ig,jg),real64)*phi(key(ir),jg)
      enddo
    enddo
  enddo
  fresh=phi;npsys=[(i,i=1,ng)];leakage=0.0_real64
  contract%eps_mccg_bits=transfer(controls(1),0_int32)
  title='SAL TRACKING'
  open(unit=91,file='radial_track.bin',status='old',form='unformatted',action='read')
  call DOORFV64(sg,npsys,track,91,0,ng,nu,key,title,leakage,q,fresh,contract,cutoff,ok)
  if(.not.ok) call fail('independent frozen-source image failed')
  close(91)
  open(newunit=u,file='audit.bin',status='new',access='stream',form='unformatted',action='write')
  write(u) [ng,nr,nu,nm,nf],k,volume,mat,key,phi,flux32,saved_source,nuf,chi,total,within,scat,q,fresh
  close(u)
  call LCMCL(archive,2)
  write(*,'(A)') 'AXMAT-R64-SNAPSHOT-AUDIT-EXPORTED'
contains
  function object(name) result(p)
    character(len=*),intent(in)::name
    type(c_ptr)::p,objects
    call require(archive,name,1,10)
    objects=LCMGID(archive,name);p=LCMGIL(objects,1)
  end function
  subroutine require(p,name,length,kind)
    type(c_ptr),intent(in)::p
    character(len=*),intent(in)::name
    integer,intent(in)::length,kind
    integer::a,b
    call LCMLEN(p,name,a,b)
    if(a/=length.or.b/=kind) call fail('record mismatch: '//name)
  end subroutine
  subroutine fail(message)
    character(len=*),intent(in)::message
    write(*,'(A)') 'AXMAT-R64-SNAPSHOT-AUDIT-FAIL: '//message
    error stop 1
  end subroutine
end program
