module SPOR64_BOOT_PROJECTX64
  ! New epoch-zero projection. No SOLVED/e0 marker, no CONT/e1 shortcut.
  ! All scalars use the canonical REAL64 state. Native non-scalar unknowns
  ! are kept bitwise from the corresponding complete radial archive item.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated,c_null_ptr
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use SPOR64_VERIFY, only: EMPTY_ROOT,RECORD_MATCHES,LIST_ITEM_IS_DIRECTORY
  use SPOR64_XSM_STORE64, only: EMPTY_XSM_ROOT
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT
  use SPOR64_BOOT_CONTEXT64_V2, only: SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK, &
      SPOR64_BOOT_CONTEXT64_READ
  use SPOR64_B2H, only: SPOR64_B2H_RECONSTRUCT
  implicit none
  private
  integer, parameter, public :: SPOR64_BOOT_PROJECT_REFUSED=1
  integer, parameter, public :: SPOR64_BOOT_PROJECT_COMMITTED=2
  integer, parameter :: NG=370,NP=3,NS=40
  integer, parameter :: kind_guard=1/merge(1,0, &
      kind(1)==int32.and.kind(1.0)==real32.and.dp==real64)
  character(len=12), parameter :: archive_signature='L_ARCHIVE'
  character(len=12), parameter :: flux_signature='L_FLUX'
  character(len=12), parameter :: macro_name='MACRO0',track_name='TRACK'
  character(len=12), parameter :: system_name='SYSTEM'
  character(len=16), parameter :: project_state='PROJECTED-BOOT'
  public :: SPOR64_BOOT_PROJECT_ARCHIVE
contains
  subroutine SPOR64_BOOT_PROJECT_ARCHIVE(ipout,ipglobal,ipax,ipaxtrack, &
      ipaxsystem,ipaxmacro,iparchive,ipcontract,requested_rank,status)
    type(c_ptr), intent(in) :: ipout,ipglobal,ipax,ipaxtrack
    type(c_ptr), intent(in) :: ipaxsystem,ipaxmacro,iparchive,ipcontract
    integer, intent(in) :: requested_rank
    integer, intent(out) :: status
    type(SPOR64_ROUTE_CONTRACT) :: contract,checked_contract
    type(c_ptr) :: inputs(7),stage,child,root_auth
    type(c_ptr) :: tracks,libraries,fluxes,out_tracks,out_libraries,out_fluxes
    type(c_ptr) :: track,library,seed,plane,auth,seed_flux,native,roots,mirrors
    integer :: i,p,g,a,nmode,nreg,nunk,nmat,n,t,istat,epoch,nplane
    integer :: dims(4),ax_track_state(NS),track_state(NS),seed_state(NS),sv(NS)
    integer, allocatable :: rank(:),off(:),boff(:),key(:),imerge(:)
    logical, allocatable :: seen(:)
    real(real32) :: eps32(5)
    real(real32), allocatable :: basis(:),basis_slice(:,:),volume32(:),mirror(:)
    real(real64) :: keff,rho,total_volume
    real(real64) :: leak(NG*NP)
    real(real64), allocatable :: coordinates(:),values(:),projected(:)
    real(real64), allocatable :: coordinate_slice(:),volume64(:),weight64(:)
    logical :: ok,exists,stage_open
    ! ipout is the exclusively owned fresh PRIVATE XSM stage; no public target exists.

    status=SPOR64_BOOT_PROJECT_REFUSED
    stage=c_null_ptr;stage_open=.false.
    inputs=[ipglobal,ipax,ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract]
    ! The owning host supplies the exact rank of its independently frozen
    ! case contract. No default, rank reduction, or mixed-rank fallback.
    if(requested_rank/=1.and.requested_rank/=2) return
    if(.not.c_associated(ipout)) return
    do i=1,size(inputs)
      if(.not.c_associated(inputs(i))) return
      if(c_associated(ipout,inputs(i))) return
    enddo
    if(.not.EMPTY_XSM_ROOT(ipout)) return
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(ipglobal,ipax,ipaxtrack,ipaxsystem, &
        ipaxmacro,iparchive,ipcontract,contract,ok)
    if(.not.ok) return
    do i=1,NP
      if(i==1) then
        if(.not.RECORD_MATCHES(iparchive,'TRACK',NP,10)) return
      else if(i==2) then
        if(.not.RECORD_MATCHES(iparchive,'MICROLIB2',NP,10)) return
      else
        if(.not.RECORD_MATCHES(iparchive,'FLUX',NP,10)) return
      endif
    enddo
    tracks=LCMGID(iparchive,'TRACK')
    libraries=LCMGID(iparchive,'MICROLIB2')
    fluxes=LCMGID(iparchive,'FLUX')
    call LCMGET(ipax,'SPOT-X-DIMS',dims)
    call LCMGET(ipaxtrack,'STATE-VECTOR',ax_track_state)
    if(any(dims(1:3)/=[1,NG,NP]).or.dims(4)<=0) return
    allocate(rank(NG),off(NG+1),boff(NG+1),coordinates(dims(4)),stat=istat)
    if(istat/=0) return
    call LCMGET(ipax,'SPOT-X-RANK',rank)
    call LCMGET(ipax,'SPOT-X-OFF',off)
    call LCMGET(ipax,'SPOT-X-BOFF',boff)
    ! The separate rank1 and original rank2 experiments keep independent
    ! admission. Matching this requested rank does not certify either gate.
    if(any(rank/=requested_rank)) return
    if(boff(NG+1)<=0) return
    allocate(basis(boff(NG+1)),stat=istat)
    if(istat/=0) return
    call LCMGET(ipax,'SPOT-X-A',coordinates)
    call LCMGET(ipax,'SPOT-X-BASIS',basis)
    call LCMGET(ipax,'SPOT-X-L',leak)
    call LCMGET(ipglobal,'KEFF64',keff)
    call LCMGET(ipglobal,'RHO64',rho)

    stage=ipout
    ! The owning host prohibits opening/admitting this private file until closed0 readback.
    if(.not.EMPTY_ROOT(stage)) goto 900
    nplane=NP;epoch=0
    call LCMPTC(stage,'SIGNATURE',12,archive_signature)
    call LCMPUT(stage,'LISTDIM',1,1,nplane)
    call LCMPUT(stage,'SPOT-ITER-K',1,4,keff)
    child=LCMDID(stage,'GLOBAL64');call LCMEQU(ipglobal,child)
    out_tracks=LCMLID(stage,'TRACK',NP)
    out_libraries=LCMLID(stage,'MICROLIB2',NP)
    out_fluxes=LCMLID(stage,'FLUX',NP)
    root_auth=LCMDID(stage,'SPOT-R64')
    call LCMPUT(root_auth,'RHO',1,4,rho)
    call LCMPUT(root_auth,'NPLANE',1,1,nplane)

    do p=1,NP
      if(.not.LIST_ITEM_IS_DIRECTORY(tracks,p).or. &
         .not.LIST_ITEM_IS_DIRECTORY(libraries,p).or. &
         .not.LIST_ITEM_IS_DIRECTORY(fluxes,p)) goto 900
      track=LCMGIL(tracks,p);library=LCMGIL(libraries,p);seed=LCMGIL(fluxes,p)
      if(.not.RECORD_MATCHES(track,'STATE-VECTOR',NS,1)) goto 900
      call LCMGET(track,'STATE-VECTOR',track_state)
      nreg=track_state(1);nunk=track_state(2);nmat=track_state(4)
      if(nreg<=0.or.nreg/=ax_track_state(6).or.nunk<=nreg.or.nmat<=0) goto 900
      if(.not.RECORD_MATCHES(track,'KEYFLX',nreg,1).or. &
         .not.RECORD_MATCHES(track,'VOLUME',nreg,2)) goto 900
      if(.not.RECORD_MATCHES(seed,'STATE-VECTOR',NS,1).or. &
         .not.RECORD_MATCHES(seed,'FLUX64',NG,10)) goto 900
      call LCMGET(seed,'STATE-VECTOR',seed_state)
      if(seed_state(1)/=NG.or.seed_state(2)/=nunk) goto 900
      allocate(key(nreg),imerge(nmat),seen(nunk),volume32(nreg), &
          volume64(nreg),weight64(nreg),values(nunk),mirror(nunk), &
          projected(nreg),basis_slice(nreg,requested_rank), &
          coordinate_slice(requested_rank),stat=istat)
      if(istat/=0) goto 900
      call LCMGET(track,'KEYFLX',key)
      seen=.false.
      do i=1,nreg
        if(key(i)<1.or.key(i)>nunk) goto 900
        if(seen(key(i))) goto 900
        seen(key(i))=.true.
      enddo
      call LCMGET(track,'VOLUME',volume32)
      if(any(.not.ieee_is_finite(volume32)).or.any(volume32<=0.0_real32)) goto 900
      volume64=real(volume32,real64)
      total_volume=sum(volume64)
      if(.not.ieee_is_finite(total_volume).or.total_volume<=0.0_real64) goto 900
      weight64=volume64/total_volume
      child=LCMDIL(out_tracks,p);call LCMEQU(track,child)
      child=LCMDIL(out_libraries,p);call LCMEQU(library,child)
      plane=LCMDIL(out_fluxes,p)
      auth=LCMDID(plane,'SPOT-R64')
      native=LCMLID(auth,'FLUX',NG)
      roots=LCMLID(plane,'ROOT-FLUX64',NG)
      mirrors=LCMLID(plane,'FLUX',NG)
      seed_flux=LCMGID(seed,'FLUX64')
      do g=1,NG
        call LCMLEL(seed_flux,g,n,t)
        if(n/=nunk.or.t/=4) goto 900
        call LCMGDL(seed_flux,g,values)
        if(any(.not.ieee_is_finite(values))) goto 900
        nmode=rank(g)
        do a=1,nmode
          basis_slice(:,a)=basis(boff(g)+(a-1)*nreg+1:boff(g)+a*nreg)
        enddo
        coordinate_slice=coordinates(off(g)+(p-1)*nmode+1:off(g)+p*nmode)
        call SPOR64_B2H_RECONSTRUCT(basis_slice,coordinate_slice,projected,ok)
        if(.not.ok) goto 900
        do i=1,nreg
          values(key(i))=projected(i)
        enddo
        if(any(abs(values)>real(huge(0.0_real32),real64))) goto 900
        mirror=real(values,real32)
        if(any(.not.ieee_is_finite(mirror))) goto 900
        call LCMPDL(native,g,nunk,4,values)
        call LCMPDL(roots,g,nunk,4,values)
        call LCMPDL(mirrors,g,nunk,2,mirror)
      enddo
      ! Explicit original TYPE-S0 / REBA / INIT-ON seed header. Native-K64
      ! headers and seals are never copied onto an unsolved projection.
      sv=0;sv(1)=NG;sv(2)=nunk;sv(3)=1
      sv(8)=contract%flu_acce_free;sv(9)=contract%flu_acce_accel
      sv(10)=1;sv(11)=contract%flu_maxinr;sv(12)=contract%flu_maxout
      sv(17)=nmat;sv(18)=1
      eps32=0.0_real32
      eps32(1:3)=transfer(contract%eps_radial_bits,0.0_real32)
      imerge=1
      call LCMPTC(plane,'SIGNATURE',12,flux_signature)
      call LCMPUT(plane,'STATE-VECTOR',NS,1,sv)
      call LCMPUT(plane,'EPS-CONVERGE',5,2,eps32)
      call LCMPUT(plane,'IMERGE-LEAK',nmat,1,imerge)
      call LCMPUT(plane,'KEYFLX',nreg,1,key)
      call LCMPTC(plane,'OPTION',4,contract%flu_option)
      call LCMPTC(plane,'LINK.MACRO',12,macro_name)
      call LCMPTC(plane,'LINK.TRACK',12,track_name)
      call LCMPTC(plane,'LINK.SYSTEM',12,system_name)
      call LCMPUT(plane,'LEAK1D64',NG,4,leak((p-1)*NG+1:p*NG))
      call LCMPUT(plane,'SPOT-LEAK1D',NG,2,real(leak((p-1)*NG+1:p*NG),real32))
      call LCMPUT(plane,'VOLUME64',nreg,4,volume64)
      call LCMPUT(plane,'WEIGHT64',nreg,4,weight64)
      call LCMPUT(auth,'RHO',1,4,rho)
      call LCMPUT(auth,'PLANE',1,1,p)
      call LCMPTC(auth,'STATE',16,project_state)
      call LCMPUT(auth,'EPOCH',1,1,epoch)
      deallocate(coordinate_slice,basis_slice,projected,mirror,values,weight64, &
          volume64,volume32,seen,imerge,key)
    enddo
    call LCMPTC(root_auth,'STATE',16,project_state)
    call LCMPUT(root_auth,'EPOCH',1,1,epoch)
    call SPOR64_BOOT_CONTEXT64_READ(stage,ipglobal,ipax,ipaxtrack,ipaxsystem, &
        ipaxmacro,iparchive,ipcontract,checked_contract,ok)
    if(.not.ok) goto 900
    if(checked_contract%case_name/=contract%case_name) goto 900
    if(.not.c_associated(stage,ipout)) goto 900
    ! Root lifecycle records are omitted from the payload copy. Even though
    ! plane payloads are complete, the archive is uncommitted until this
    ! caller writes STATE and then EPOCH as its last output mutation.
    call LCMDEL(root_auth,'STATE')
    call LCMDEL(root_auth,'EPOCH')
    ! Single private target: the complete payload is already here.
    ! STATE then EPOCH are rewritten last, followed by the same full context readback.
    root_auth=LCMGID(ipout,'SPOT-R64')
    call LCMPTC(root_auth,'STATE',16,project_state)
    call LCMPUT(root_auth,'EPOCH',1,1,epoch)
    call SPOR64_BOOT_CONTEXT64_READ(ipout,ipglobal,ipax,ipaxtrack,ipaxsystem, &
        ipaxmacro,iparchive,ipcontract,checked_contract,ok)
    if(.not.ok) call XABORT('BOOT PROJECT64: COMMITTED OUTPUT READBACK FAILED.')
    status=SPOR64_BOOT_PROJECT_COMMITTED
900 continue
    ! The owning CLE/host alone closes and owns this output. On refusal it is
    ! unqualified partial private data, never an externally published archive.
    if(status/=SPOR64_BOOT_PROJECT_COMMITTED.and.c_associated(stage)) then
      call LCMLEN(stage,'SPOT-R64',n,t)
      if(n==-1.and.t==0) then
        root_auth=LCMGID(stage,'SPOT-R64')
        call LCMLEN(root_auth,'STATE',n,t)
        if(n>0) call LCMDEL(root_auth,'STATE')
        call LCMLEN(root_auth,'EPOCH',n,t)
        if(n>0) call LCMDEL(root_auth,'EPOCH')
      endif
    endif
  end subroutine SPOR64_BOOT_PROJECT_ARCHIVE
end module SPOR64_BOOT_PROJECTX64
