program probe_native_multigroup
  ! Historical pin data/source audit. No solve, rebalance, or XSM mutation.
  use GANLIB
  use SPOT_LEAKAGE, only: SPOQFSD
  use SPOR64_A8, only: MCGFCS64
  use, intrinsic :: iso_fortran_env, only: real32,real64,error_unit
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer,parameter :: nr=8,nb=6,nu=14,ng=370,nm=8
  type(c_ptr) :: track,system,macro,fsrc,sg,mg,fg,si,mi,kpsys(1)
  integer :: st(40),key(nr,1,1),cur(nb),zone(nu),bc(nb),idx(nu),raw,leak_kind
  integer :: njj(nm,ng),ijj(nm,ng),ipos(nm,ng),ns(ng),g,h,m,p,i,n,t,out,inp,ios,ic,ncase,nalbp,nfis
  real(real32) :: weights(nu),volume(nr),total(0:nm,ng),used(0:nm,ng),phys(0:nm,ng)
  real(real32) :: macro_total(nm,ng),sigw(nm,ng),sigs(nm,ng),leak(ng),q32(nu,ng),tranc(nm,ng)
  real(real32) :: dense(ng,ng,nm),sigal(-6:nm,1)
  real(real32),allocatable :: packed(:,:),nufis(:)
  real(real64) :: fixed(nr,ng),field(nu,ng),leak_extra(ng),qoff(nr),qn(nu),fi(nu),source(nu,ng)
  real(real64) :: off(nr,ng),outphysical(nu,ng),scalar_field(nr,ng)
  logical :: exists,lvoid,ok,seen(nu)
  character(len=1024) :: mode,input_path,output_path
  if(command_argument_count()/=3) call fail('usage: probe_native_multigroup dump|source|correction INPUT OUTPUT')
  call get_command_argument(1,mode);call get_command_argument(2,input_path);call get_command_argument(3,output_path)
  if(trim(mode)/='dump'.and.trim(mode)/='source'.and.trim(mode)/='correction') call fail('invalid mode')
  inquire(file=trim(output_path),exist=exists)
  if(exists) call fail('output exists')
  call LCMOP(track,'track.xsm',2,2,0);call LCMOP(system,'system.xsm',2,2,0)
  call LCMOP(macro,'macro.xsm',2,2,0);call LCMOP(fsrc,'source.xsm',2,2,0)
  call record(track,'STATE-VECTOR',40,1);call LCMGET(track,'STATE-VECTOR',st)
  if(st(1)/=nr.or.st(2)/=nu.or.st(4)/=nm.or.st(5)/=nb.or.st(6)/=1) call fail('pin dimensions')
  call record(macro,'STATE-VECTOR',40,1);call LCMGET(macro,'STATE-VECTOR',st)
  write(*,*) 'MACRO STATE ',st
  if(st(1)/=ng.or.st(2)/=nm.or.st(4)<1) call fail('macro dimensions')
  nfis=st(4);allocate(nufis(nm*nfis))
  call record(track,'KEYFLX$ANIS',nr,1);call LCMGET(track,'KEYFLX$ANIS',key)
  call record(track,'KEYCUR$MCCG',nb,1);call LCMGET(track,'KEYCUR$MCCG',cur)
  call record(track,'NZON$MCCG',nu,1);call LCMGET(track,'NZON$MCCG',zone)
  call record(track,'BC-REFL+TRAN',nb,1);call LCMGET(track,'BC-REFL+TRAN',bc)
  call record(track,'V$MCCG',nu,2);call LCMGET(track,'V$MCCG',weights)
  call record(track,'VOLUME',nr,2);call LCMGET(track,'VOLUME',volume)
  if(any(zone(:nr)<1).or.any(zone(:nr)>nm)) call fail('material mapping')
  if(any(zone(nr+1:)< -6).or.any(zone(nr+1:)> -1)) call fail('boundary mapping')
  if(any(bc<1).or.any(bc>nb)) call fail('return mapping')
  idx(:nr)=key(:,1,1);idx(nr+1:)=cur;seen=.false.
  do i=1,nu
    if(idx(i)<1.or.idx(i)>nu) call fail('unknown map range')
    if(seen(idx(i))) call fail('duplicate unknown')
    seen(idx(i))=.true.
  enddo
  call record(system,'SPOT-LEAK1D',ng,2);call LCMGET(system,'SPOT-LEAK1D',leak)
  leak_kind=2;raw=0
  call LCMLEN(system,'SPOT-L1-RAW',n,t)
  if(n/=0) then
    call record(system,'SPOT-L1-RAW',1,1);call LCMGET(system,'SPOT-L1-RAW',raw)
  endif
  ! The fixture audit requires legacy embedded leakage; no ambiguous authority.
  if(raw/=0) call fail('fixture requires separate REAL64 leakage authority; not this legacy audit')
  call record(system,'GROUP',ng,10);sg=LCMGID(system,'GROUP')
  call record(macro,'GROUP',ng,10);mg=LCMGID(macro,'GROUP')
  call record(fsrc,'DSOUR',1,10);fg=LCMGID(fsrc,'DSOUR');fg=LCMGIL(fg,1)
  allocate(packed(nm*ng,ng));packed=0;dense=0
  do g=1,ng
    si=LCMGIL(sg,g);mi=LCMGIL(mg,g)
    call record(si,'DRAGON-TXSC',nm+1,2);call LCMGET(si,'DRAGON-TXSC',total(:,g))
    call record(si,'DRAGON-S0XSC',nm+1,2);call LCMGET(si,'DRAGON-S0XSC',used(:,g))
    call record(si,'SPOT-S0-PHYS',nm+1,2);call LCMGET(si,'SPOT-S0-PHYS',phys(:,g))
    call record(mi,'NTOT0',nm,2);call LCMGET(mi,'NTOT0',macro_total(:,g))
    call record(mi,'SIGW00',nm,2);call LCMGET(mi,'SIGW00',sigw(:,g))
    call record(mi,'SIGS00',nm,2);call LCMGET(mi,'SIGS00',sigs(:,g))
    call record(mi,'TRANC',nm,2);call LCMGET(mi,'TRANC',tranc(:,g))
    call record(mi,'NUSIGF',nm*nfis,2);call LCMGET(mi,'NUSIGF',nufis)
    if(any(nufis/=0)) call fail('MACRO0 must have fission disabled')
    call record(mi,'NJJS00',nm,1);call LCMGET(mi,'NJJS00',njj(:,g))
    call record(mi,'IJJS00',nm,1);call LCMGET(mi,'IJJS00',ijj(:,g))
    call record(mi,'IPOS00',nm,1);call LCMGET(mi,'IPOS00',ipos(:,g))
    call LCMLEN(mi,'SCAT00',n,t)
    if(n<1.or.n>nm*ng.or.t/=2) call fail('packed scattering size/type')
    ns(g)=n;call LCMGET(mi,'SCAT00',packed(:n,g))
    do m=1,nm
      if(njj(m,g)<0) call fail('negative scatter count')
      if(njj(m,g)==0) cycle
      if(ipos(m,g)<1.or.ipos(m,g)+njj(m,g)-1>n) call fail('packed scattering bounds')
      if(ijj(m,g)>ng.or.ijj(m,g)-njj(m,g)+1<1) call fail('source-group bounds')
      do p=1,njj(m,g)
        h=ijj(m,g)-p+1
        dense(g,h,m)=packed(ipos(m,g)+p-1,g)
      enddo
    enddo
    call LCMLEL(fg,g,n,t)
    if(n/=nu.or.t/=2) call fail('frozen source layout')
    call LCMGDL(fg,g,q32(:,g))
  enddo
  if(.not.all(ieee_is_finite(dense)).or..not.all(ieee_is_finite(q32))) call fail('nonfinite data')
  open(newunit=out,file=trim(output_path),status='new',form='unformatted',access='stream')
  if(trim(mode)=='correction') then
    write(out) tranc
  else if(trim(mode)=='dump') then
    write(out) nr,nb,ng,nm,raw,leak_kind
    write(out) zone,idx,bc,weights,volume,leak,total,used,phys,macro_total,sigw,sigs,dense,q32
  else
    open(newunit=inp,file=trim(input_path),status='old',form='unformatted',access='stream')
    read(inp,iostat=ios) ncase
    if(ios/=0.or.ncase<1.or.ncase>100) call fail('source case count')
    write(out) ncase,nr,nb,ng
    do ic=1,ncase
      read(inp,iostat=ios) leak_extra,fixed,field
      if(ios/=0) call fail('source case truncated')
      if(.not.all(ieee_is_finite(field)).or..not.all(ieee_is_finite(leak_extra))) call fail('nonfinite field')
      scalar_field=field(:nr,:)
      do g=1,ng
        call SPOQFSD(nr,ng,nm,g,zone(:nr),scalar_field,njj(:,g),ijj(:,g),ipos(:,g), &
          packed(:ns(g),g),fixed(:,g),qoff)
        off(:,g)=qoff;qn=0;fi=0
        do i=1,nr
          qn(idx(i))=qoff(i)
        enddo
        do i=1,nu
          fi(idx(i))=field(i,g)
        enddo
        kpsys(1)=LCMGIL(sg,g);call LCMLEN(kpsys(1),'ALBEDO',nalbp,t)
        call MCGSIG(track,nm,1,nalbp,kpsys,sigal,lvoid)
        source(:,g)=0
        call MCGFCS64(nu,2,zone,qn,fi,nm,1,1,1,reshape(used(:,g),[nm+1,1]), &
          leak_extra(g),source(:,g),nu,nr,0,key,cur,bc,sigal(:,1),1,ok)
        if(.not.ok) call fail('native source constructor rejected')
        do i=1,nu
          outphysical(i,g)=source(idx(i),g)
        enddo
      enddo
      write(out) off,outphysical
    enddo
    read(inp,iostat=ios) i
    if(ios>=0) call fail('trailing source input')
    close(inp)
  endif
  close(out)
  call LCMCL(fsrc,1);call LCMCL(macro,1);call LCMCL(system,1);call LCMCL(track,1)
  write(*,*) 'NATIVE-MULTIGROUP READONLY ',trim(mode),' COMPLETE'
contains
  subroutine fail(message)
    character(len=*),intent(in) :: message
    write(error_unit,'(A)') 'NATIVE-MULTIGROUP ERROR: '//message
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
end program
