! SOURCE-ONLY UNREADY: never compiled or executed by its author.
! Link real GANLIB plus separately extracted candidate FLUSP64 and exact
! original FLUSP64_REFERENCE.  The ONLY replaced business callee is SPOF64.
! This observer proves wrapper routing and bit preservation, not solver math.
module axmat_flusp64_window_observer
  use iso_fortran_env, only: int32,int64
  use iso_c_binding, only: c_ptr,c_associated
  use GANLIB, only: LCMGIL,LCMGET
  implicit none
  integer :: calls=0,expected_nun=0,expected_nr=0,expected_nm=0
  integer(int64) :: expected_caller_address=0_int64,observed_fun_address=0_int64
  logical :: expected_direct=.false.,observed_direct=.false.
  integer,allocatable :: expected_groups(:),expected_systems(:),expected_mat(:),expected_key(:)
  integer,allocatable :: observed_groups(:),observed_systems(:)
  real(kind(0.0d0)),allocatable :: observed_source(:,:)
  type(c_ptr) :: expected_list,expected_track
  character(len=72) :: expected_title
contains
  subroutine configure(list,track,np,mat,key,nun,nr,nm,title,caller_address,direct)
    type(c_ptr),intent(in) :: list,track
    integer,intent(in) :: np(:),mat(:),key(:),nun,nr,nm
    character(len=72),intent(in) :: title
    integer(int64),intent(in) :: caller_address
    logical,intent(in) :: direct
    integer :: i,j,n
    if(allocated(expected_groups)) then
      deallocate(expected_groups,expected_systems,expected_mat,expected_key)
      deallocate(observed_groups,observed_systems,observed_source)
    endif
    n=count(np/=0)
    allocate(expected_groups(n),expected_systems(n),expected_mat(nr),expected_key(nr))
    allocate(observed_groups(n),observed_systems(n),observed_source(nun,n))
    expected_mat=mat;expected_key=key;expected_nun=nun;expected_nr=nr;expected_nm=nm
    expected_list=list;expected_track=track;expected_title=title;calls=0
    expected_caller_address=caller_address;observed_fun_address=0_int64
    expected_direct=direct;observed_direct=.false.
    observed_groups=0;observed_systems=0;observed_source=0.0d0
    j=0
    do i=1,size(np)
      if(np(i)==0) cycle
      j=j+1;expected_groups(j)=i;expected_systems(j)=np(i)
    enddo
  end subroutine
  subroutine observe(kpsys,iptrk,impx,ngeff,ngind,nreg,nmat,nun,mat,key,fun,source,title)
    integer :: impx,ngeff,ngind(ngeff),nreg,nmat,nun,mat(nreg),key(nreg)
    type(c_ptr) :: kpsys(ngeff),iptrk,want
    real(kind(0.0d0)) :: fun(nun,ngeff),source(nun,ngeff)
    character(len=72) :: title
    integer :: i,j,marker(1)
    integer(int64) :: bits,salt
    calls=calls+1
    if(calls/=1) error stop 81
    ! GNU LOC is unit-observer instrumentation only; neither wrapper is edited.
    observed_fun_address=int(loc(fun(1,1)),int64)
    observed_direct=observed_fun_address==expected_caller_address
    if(observed_direct.neqv.expected_direct) error stop 107
    if(nun/=expected_nun.or.nreg/=expected_nr.or.nmat/=expected_nm) error stop 82
    if(ngeff/=size(expected_groups).or.impx/=0) error stop 83
    if(.not.c_associated(iptrk,expected_track)) error stop 84
    if(title/=expected_title.or.any(mat/=expected_mat).or.any(key/=expected_key)) error stop 85
    call LCMGET(iptrk,'V13-TRACK',marker)
    if(marker(1)/=13713) error stop 86
    if(any(ngind/=expected_groups)) error stop 87
    do j=1,ngeff
      want=LCMGIL(expected_list,expected_systems(j))
      if(.not.c_associated(kpsys(j),want)) error stop 88
      call LCMGET(kpsys(j),'V13-GROUP',marker)
      if(marker(1)/=expected_systems(j)) error stop 89
      observed_groups(j)=ngind(j);observed_systems(j)=marker(1)
    enddo
    ! Capture the complete source before writing output; never read FUN.
    observed_source=source
    do j=1,ngeff
      do i=1,nun
        salt=ishft(int(ngind(j),int64),20)+int(i,int64)
        bits=ior(iand(ieor(transfer(source(i,j),0_int64),salt), &
          int(z'800FFFFFFFFFFFFF',int64)),int(z'3FF0000000000000',int64))
        if(mod(i+j,11)==0) bits=int(z'8000000000000000',int64)
        fun(i,j)=transfer(bits,0.0d0)
      enddo
    enddo
  end subroutine
end module

! Same original SPOF64 ABI, deterministic observer implementation only.
subroutine SPOF64(kpsys,iptrk,impx,ngeff,ngind,nreg,nmat,nun,mat,key,fun,source,title)
  use axmat_flusp64_window_observer, only: observe
  use iso_c_binding, only: c_ptr
  implicit none
  integer :: impx,ngeff,ngind(ngeff),nreg,nmat,nun,mat(nreg),key(nreg)
  type(c_ptr) :: kpsys(ngeff),iptrk
  real(kind(0.0d0)) :: fun(nun,ngeff),source(nun,ngeff)
  character(len=72) :: title
  call observe(kpsys,iptrk,impx,ngeff,ngind,nreg,nmat,nun,mat,key,fun,source,title)
end subroutine

program flusp64_window_observer_controls
  use iso_fortran_env, only: int32,int64
  use iso_c_binding, only: c_ptr
  use GANLIB, only: LCMOP,LCMCL,LCMLID,LCMDIL,LCMGET,LCMPUT
  use axmat_flusp64_window_observer
  implicit none
  interface
    subroutine FLUSP64(jpsys,npsys,iptrk,impx,ngrp,nmat,nreg,nun,mat,vol,key, &
      title,ileak,b2,nmerg,imerg,difhet,old,sun,fun)
      import c_ptr
      integer :: impx,ngrp,nmat,nreg,nun,npsys(ngrp),mat(nreg),key(nreg),ileak,nmerg,imerg(nmat)
      type(c_ptr) :: jpsys,iptrk
      real :: vol(nreg),b2(4),difhet(nmerg,ngrp)
      real(kind(0.0d0)) :: old(nun,ngrp),sun(nun,ngrp),fun(nun,ngrp)
      character(len=72) :: title
    end subroutine
    subroutine FLUSP64_REFERENCE(jpsys,npsys,iptrk,impx,ngrp,nmat,nreg,nun,mat,vol,key, &
      title,ileak,b2,nmerg,imerg,difhet,old,sun,fun)
      import c_ptr
      integer :: impx,ngrp,nmat,nreg,nun,npsys(ngrp),mat(nreg),key(nreg),ileak,nmerg,imerg(nmat)
      type(c_ptr) :: jpsys,iptrk
      real :: vol(nreg),b2(4),difhet(nmerg,ngrp)
      real(kind(0.0d0)) :: old(nun,ngrp),sun(nun,ngrp),fun(nun,ngrp)
      character(len=72) :: title
    end subroutine
  end interface
  integer,parameter :: nr0=7,nm0=4,nmrg0=3
  integer :: nun0
  character(len=80) :: mode,prefix
  character(len=72) :: title
  integer :: ng,id,step,nsteps,ileak,route,first,last,nactive,i,g,p,j,u,marker(1)
  integer :: nnun,nnr,mat(nr0),key(nr0),imerg(nm0)
  integer,allocatable :: np(:),np_saved(:),eg(:),es(:),rg(:),rs(:)
  integer :: mat_saved(nr0),key_saved(nr0),imerg_saved(nm0)
  real :: vol(nr0),b2(4),vol_saved(nr0),b2_saved(4)
  real,allocatable :: difhet(:,:),difhet_saved(:,:)
  real(kind(0.0d0)),allocatable :: flux(:,:,:),reference_flux(:,:,:),baseline(:,:,:),expected_source(:,:),ref_source(:,:)
  type(c_ptr) :: root,list,track,item
  integer(int64),parameter :: magic=int(z'41584657494E3133',int64)
  integer(int64) :: word
  integer(int64) :: caller_address
  call get_command_argument(1,mode)
  select case(trim(mode))
  case('all');id=1
  case('suffix');id=2
  case('interior');id=3
  case('scalar_first');id=4
  case('scalar_last');id=5
  case('scalar_one');id=6
  case('sparse');id=7
  case('empty_ileak0');id=8
  case('empty_ileak3');id=9
  case('transition');id=10
  case('unsupported_reference_active');id=11
  case('unsupported_candidate_active');id=12
  case('unsupported_reference_empty');id=13
  case('unsupported_candidate_empty');id=14
  case default
    error stop 90
  end select
  nun0=12;ng=8
  if(id==1) then
    nun0=1800;ng=370
  endif
  if(id==6) ng=1
  allocate(np(ng),np_saved(ng),difhet(nmrg0,ng),difhet_saved(nmrg0,ng))
  allocate(flux(nun0,ng,8),reference_flux(nun0,ng,8),baseline(nun0,ng,8))
  mat=[1,2,0,3,4,2,1];key=[1,0,4,5,1,nun0,nun0-1];imerg=[1,0,2,3]
  do i=1,nr0
    vol(i)=real(i)/8.0
  enddo
  do g=1,ng
    do i=1,nmrg0
      difhet(i,g)=(-1.0)**(i+g)*(real(i)/4.0+real(g)/128.0)
    enddo
    do p=1,8
      do i=1,nun0
        flux(i,g,p)=(-1.0d0)**(i+g+p)*(real(p,8)+real(g,8)/32.0d0+real(i,8)/1024.0d0)
        if(mod(i+g+p,17)==0) flux(i,g,p)=transfer(int(z'8000000000000000',int64),0.0d0)
      enddo
    enddo
  enddo
  reference_flux=flux
  title='V13 original sender contiguous output window observer scope only'
  call LCMOP(root,'V13-SYSTEM',0,1,0)
  list=LCMLID(root,'GROUP',ng)
  do g=1,ng
    item=LCMDIL(list,g);marker(1)=g
    call LCMPUT(item,'V13-GROUP',1,1,marker)
  enddo
  call LCMOP(track,'V13-TRACK',0,1,0)
  marker(1)=13713;call LCMPUT(track,'V13-TRACK',1,1,marker)
  ! Positive modes repeat twice, transition changes active set on each of 4 calls.
  nsteps=2;if(id==10) nsteps=4
  if(id>=11) nsteps=1
  open(newunit=u,file='wrapper_manifest.jsonl',status='new',action='write')
  do step=1,nsteps
    np=0;b2=0.0;ileak=0
    select case(id)
    case(1,11,12);np=1
    case(2);np(3:ng)=1;ileak=3;b2(4)=1.25
    case(3);np(2:5)=1
    case(4);np(1)=1;ileak=3;b2(4)=transfer(int(z'80000000',int32),0.0)
    case(5);np(ng)=1;ileak=3;b2(4)=-0.75
    case(6);np(1)=1
    case(7);np(1)=1;np(3)=1;np(ng)=1;ileak=3;b2(4)=1.25
    case(8,13,14)
    case(9);ileak=3;b2(4)=1.25
    case(10)
      ileak=3;b2(4)=1.25
      select case(step)
      case(1);np(3:ng)=1
      case(2);np(ng)=1
      case(3);np(1)=1;np(3)=1;np(ng)=1
      case(4)
      end select
    end select
    do g=1,ng
      if(np(g)/=0) np(g)=ng+1-g ! Group-object key differs from energy-group index.
    enddo
    if(id>=11) ileak=2
    nactive=count(np/=0);route=0
    if(nactive>0) then
      first=findloc(np/=0,.true.,dim=1)
      last=findloc(np/=0,.true.,dim=1,back=.true.)
      route=2;if(last-first+1==nactive) route=1
    endif
    allocate(eg(nactive),es(nactive),expected_source(nun0,nactive))
    j=0
    do g=1,ng
      if(np(g)==0) cycle
      j=j+1;eg(j)=g;es(j)=np(g);expected_source(:,j)=flux(:,g,8)
      if(ileak==3.and.b2(4)/=0.0) then
        do i=1,nr0
          if(key(i)==0) cycle
          if(mat(i)==0) cycle
          if(imerg(mat(i))==0) cycle
          expected_source(key(i),j)=expected_source(key(i),j)- &
            dble(difhet(imerg(mat(i)),g))*dble(b2(4))*flux(key(i),g,2)
        enddo
      endif
    enddo
    np_saved=np;mat_saved=mat;key_saved=key;imerg_saved=imerg
    vol_saved=vol;b2_saved=b2;difhet_saved=difhet;baseline=flux
    if(any(transfer(reference_flux,[0_int64],size(reference_flux))/= &
       transfer(flux,[0_int64],size(flux)))) error stop 91
    write(prefix,'(A,".s",I1)') trim(mode),step
    call raw_record(trim(prefix)//'.input.bin',0,0,eg,es,expected_source,flux)
    if(id>=11) then
      caller_address=0_int64
      if(nactive>0) caller_address=int(loc(flux(1,first,7)),int64)
      call configure(list,track,np,mat,key,nun0,nr0,nm0,title,caller_address,.false.)
      nnun=nun0;nnr=nr0
      if(id==11.or.id==13) then
        call FLUSP64_REFERENCE(list,np,track,0,ng,nm0,nnr,nnun,mat,vol,key, &
          title,ileak,b2,nmrg0,imerg,difhet,flux(1,1,2),flux(1,1,8),flux(1,1,7))
      else
        call FLUSP64(list,np,track,0,ng,nm0,nnr,nnun,mat,vol,key, &
          title,ileak,b2,nmrg0,imerg,difhet,flux(1,1,2),flux(1,1,8),flux(1,1,7))
      endif
      ! Genuine GANLIB XABORT must terminate first; this is not an expected PASS.
      error stop 92
    endif
    caller_address=0_int64
    if(nactive>0) caller_address=int(loc(reference_flux(1,first,7)),int64)
    call configure(list,track,np,mat,key,nun0,nr0,nm0,title,caller_address,.false.)
    nnun=nun0;nnr=nr0
    call FLUSP64_REFERENCE(list,np,track,0,ng,nm0,nnr,nnun,mat,vol,key, &
      title,ileak,b2,nmrg0,imerg,difhet,reference_flux(1,1,2),reference_flux(1,1,8),reference_flux(1,1,7))
    call check_readonly(reference_flux)
    call check_observation()
    if(nnun/=nun0.or.nnr/=nr0) error stop 93
    allocate(rg(nactive),rs(nactive),ref_source(nun0,nactive))
    rg=observed_groups;rs=observed_systems;ref_source=observed_source
    call raw_record(trim(prefix)//'.reference.bin',1,calls,rg,rs,ref_source,reference_flux)
    caller_address=0_int64
    if(nactive>0) caller_address=int(loc(flux(1,first,7)),int64)
    call configure(list,track,np,mat,key,nun0,nr0,nm0,title,caller_address,route==1)
    nnun=nun0;nnr=nr0
    call FLUSP64(list,np,track,0,ng,nm0,nnr,nnun,mat,vol,key, &
      title,ileak,b2,nmrg0,imerg,difhet,flux(1,1,2),flux(1,1,8),flux(1,1,7))
    call check_readonly(flux)
    call check_observation()
    if(nnun/=nun0.or.nnr/=nr0) error stop 94
    if(any(rg/=observed_groups).or.any(rs/=observed_systems)) error stop 95
    if(any(transfer(ref_source,[0_int64],size(ref_source))/= &
       transfer(observed_source,[0_int64],size(observed_source)))) error stop 96
    if(any(transfer(reference_flux,[0_int64],size(reference_flux))/= &
       transfer(flux,[0_int64],size(flux)))) error stop 97
    call raw_record(trim(prefix)//'.candidate.bin',2,calls,observed_groups,observed_systems,observed_source,flux)
    write(u,'(A,I0,A,I0,A,I0,A)') '{"schema":"AXMAT_FLUSP64_WINDOW_WRAPPER_OBSERVER_CONTROL_V1","case_id":', &
      id,',"step":',step,',"expected_route":',route,',"bitwise_passed":true,"solver_math_credit":false}'
    deallocate(eg,es,expected_source,rg,rs,ref_source)
  enddo
  close(u)
  call LCMCL(track,2);call LCMCL(root,2)
  write(*,'(A)') 'AXMAT_FLUSP64_WINDOW_WRAPPER_OBSERVER_CONTROL_V1 OBSERVER_ONLY '//trim(mode)
contains
  subroutine check_observation()
    integer :: q,want_calls
    want_calls=0;if(nactive>0) want_calls=1
    if(calls/=want_calls) error stop 98
    if(any(observed_groups/=eg).or.any(observed_systems/=es)) error stop 99
    if(any(transfer(observed_source,[0_int64],size(observed_source))/= &
       transfer(expected_source,[0_int64],size(expected_source)))) error stop 100
    do q=1,ng
      item=LCMDIL(list,q);call LCMGET(item,'V13-GROUP',marker)
      if(marker(1)/=q) error stop 101
    enddo
    if(.not.c_associated(list,expected_list).or..not.c_associated(track,expected_track)) error stop 108
    if(title/=expected_title) error stop 109
  end subroutine
  subroutine check_readonly(a)
    real(kind(0.0d0)),intent(in) :: a(nun0,ng,8)
    integer :: q,v
    if(any(np/=np_saved).or.any(mat/=mat_saved).or.any(key/=key_saved).or.any(imerg/=imerg_saved)) error stop 102
    if(any(transfer(vol,[0_int32],size(vol))/=transfer(vol_saved,[0_int32],size(vol)))) error stop 103
    if(any(transfer(b2,[0_int32],size(b2))/=transfer(b2_saved,[0_int32],size(b2)))) error stop 104
    if(any(transfer(difhet,[0_int32],size(difhet))/= &
       transfer(difhet_saved,[0_int32],size(difhet)))) error stop 105
    do v=1,8
      do q=1,ng
        if(v==7.and.np(q)/=0) cycle
        if(any(transfer(a(:,q,v),[0_int64],nun0)/= &
           transfer(baseline(:,q,v),[0_int64],nun0))) error stop 106
      enddo
    enddo
  end subroutine
  subroutine raw_record(path,who,ncalls,groups,systems,source,a)
    character(len=*),intent(in) :: path
    integer,intent(in) :: who,ncalls,groups(:),systems(:)
    real(kind(0.0d0)),intent(in) :: source(:,:),a(nun0,ng,8)
    integer :: f
    integer(int64) :: header(18),address_fields(4)
    address_fields=0_int64
    if(who/=0) address_fields=[expected_caller_address,observed_fun_address, &
      merge(1_int64,0_int64,expected_direct),merge(1_int64,0_int64,observed_direct)]
    header=[magic,1_int64,int(id,int64),int(who,int64),int(step,int64),int(nun0,int64), &
      int(ng,int64),int(nr0,int64),int(nm0,int64),int(nmrg0,int64),int(nactive,int64), &
      int(ncalls,int64),int(ileak,int64),int(route,int64),address_fields]
    open(newunit=f,file=path,status='new',access='stream',form='unformatted',action='write')
    write(f) header,int(np,int64),int(mat,int64),int(key,int64),int(imerg,int64)
    write(f) int(transfer(vol,[0_int32],size(vol)),int64),int(transfer(b2,[0_int32],size(b2)),int64)
    write(f) int(transfer(difhet,[0_int32],size(difhet)),int64)
    write(f) title
    write(f) transfer(a,[0_int64],size(a)),int(groups,int64),int(systems,int64)
    write(f) transfer(source,[0_int64],size(source))
    close(f)
  end subroutine
end program
