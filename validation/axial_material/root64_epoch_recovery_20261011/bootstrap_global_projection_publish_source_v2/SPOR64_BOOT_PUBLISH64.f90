module SPOR64_BOOT_PUBLISH64
  ! New bootstrap protocol. The caller passes the actual strict-return values
  ! from SPOT_GLOBAL_NATIVE_DRIVER64 after completing the original headers.
  ! Full context consistency is independently checked, never used as proof
  ! of a solve. External Source, commands, input and output pins remain needed.
  use GANLIB
  use, intrinsic :: iso_c_binding, only: c_ptr,c_associated,c_null_ptr
  use, intrinsic :: iso_fortran_env, only: int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  use SPOR64_VERIFY, only: EMPTY_ROOT,RECORD_MATCHES,EXACT_INVENTORY
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  use SPOR64_BOOT_CANONICAL64_V2, only: SPOR64_BOOT_CANONICAL64_CHECK
  use SPOR64_BOOT_CONTEXT64_V2, only: SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK
  implicit none
  private
  integer, parameter, public :: SPOR64_BOOT_GLOBAL_REFUSED=1
  integer, parameter, public :: SPOR64_BOOT_GLOBAL_PUBLISHED=2
  integer, parameter :: NG=370,NP=3,NS=40
  integer, parameter :: kind_guard=1/merge(1,0, &
      kind(1)==int32.and.kind(1.0)==real32.and.dp==real64)
  character(len=12), parameter :: global_names(21)= &
      ['SIGNATURE   ','VERSION     ','NPLANE      ','EPOCH       ', &
       'ROLE        ','STATE       ','CASE        ','KEFF64      ', &
       'RHO64       ','NORM64      ','RESIDUALS   ','COUNTERS    ', &
       'INNER-STATE ','CAPS        ','TERM-EPS    ','AX          ', &
       'AXTRACK     ','AXSYSTEM    ','AXMACRO     ','ARCHIVE     ', &
       'RCON        ']
  character(len=12), parameter :: global_signature='L_GLOBAL64'
  character(len=12), parameter :: global_role='GLOBAL-K64'
  character(len=12), parameter :: global_state='GLOBAL-DONE'
  public :: SPOR64_BOOT_GLOBAL_PUBLISH
contains
  subroutine SPOR64_BOOT_GLOBAL_PUBLISH(ipout,ipax,ipaxtrack,ipaxsystem, &
      ipaxmacro,iparchive,ipcontract,terminal_flux64,terminal_source64, &
      terminal_keff64,terminal_resid64,terminal_counters, &
      terminal_inner_state,terminal_valid,status)
    type(c_ptr), intent(in) :: ipout,ipax,ipaxtrack,ipaxsystem,ipaxmacro
    type(c_ptr), intent(in) :: iparchive,ipcontract
    real(real64), intent(in) :: terminal_flux64(:,:),terminal_source64(:,:)
    real(real64), intent(in) :: terminal_keff64,terminal_resid64(3)
    integer, intent(in) :: terminal_counters(2),terminal_inner_state
    logical, intent(in) :: terminal_valid
    integer, intent(out) :: status
    type(c_ptr) :: inputs(6),stage,child
    type(SPOR64_ROUTE_CONTRACT) :: contract,checked_contract
    integer :: i,sv(NS),caps(2),version,epoch,nplane
    real(real32) :: eps32(5),case_eps32
    real(real64) :: eps64(3),keff64,rho64,norm64
    logical :: ok,exists,stage_open
    character(len=72), parameter :: stage_file='BOOT-GLOBAL64-STAGE.xsm'

    status=SPOR64_BOOT_GLOBAL_REFUSED
    stage=c_null_ptr;stage_open=.false.
    inputs=[ipax,ipaxtrack,ipaxsystem,ipaxmacro,iparchive,ipcontract]
    if(.not.terminal_valid.or.terminal_inner_state/=1) return
    if(.not.c_associated(ipout)) return
    do i=1,size(inputs)
      if(.not.c_associated(inputs(i))) return
      if(c_associated(ipout,inputs(i))) return
    enddo
    if(.not.EMPTY_ROOT(ipout)) return
    if(any(.not.ieee_is_finite(terminal_flux64)).or. &
       any(.not.ieee_is_finite(terminal_source64)).or. &
       .not.ieee_is_finite(terminal_keff64).or.terminal_keff64<=0.0_real64.or. &
       any(.not.ieee_is_finite(terminal_resid64)).or. &
       any(terminal_resid64<0.0_real64)) return
    call SPOR64_RCONTRACT_LOAD(ipcontract,contract,ok)
    if(.not.ok) return
    if(.not.RECORD_MATCHES(ipax,'STATE-VECTOR',NS,1)) return
    if(.not.RECORD_MATCHES(ipax,'EPS-CONVERGE',5,2)) return
    call LCMGET(ipax,'STATE-VECTOR',sv)
    call LCMGET(ipax,'EPS-CONVERGE',eps32)
    if(sv(1)/=NG.or.sv(2)<=0) return
    if(any(shape(terminal_flux64)/=[sv(2),NG]).or. &
       any(shape(terminal_source64)/=[sv(2),NG])) return
    if(any(.not.ieee_is_finite(eps32)).or.any(eps32(1:3)<=0.0_real32)) return
    case_eps32=transfer(contract%eps_axial_bits,0.0_real32)
    do i=1,3
      if(transfer(eps32(i),0_int32)/=transfer(case_eps32,0_int32)) return
    enddo
    eps64=real([eps32(3),eps32(2),eps32(1)],real64)
    caps=[sv(12),sv(11)]
    if(any(caps<=0).or.terminal_counters(1)<2.or. &
       terminal_counters(2)<1.or.any(terminal_counters>caps)) return
    if(any(terminal_resid64>=eps64)) return
    ! Check raw native fields, before looking at any canonical labels.
    if(.not.FIELD_MATCHES(ipax,'FLUX64',terminal_flux64)) return
    if(.not.FIELD_MATCHES(ipax,'SOUR64',terminal_source64)) return
    if(.not.RECORD_MATCHES(ipax,'SPOT-KEFF64',1,4)) return
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-KEFF',1,4)) return
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-RHO',1,4)) return
    if(.not.RECORD_MATCHES(ipax,'SPOT-X-NORM',1,4)) return
    call LCMGET(ipax,'SPOT-KEFF64',keff64)
    if(.not.SAME64(keff64,terminal_keff64)) return
    call LCMGET(ipax,'SPOT-X-KEFF',keff64)
    if(.not.SAME64(keff64,terminal_keff64)) return
    call LCMGET(ipax,'SPOT-X-RHO',rho64)
    call LCMGET(ipax,'SPOT-X-NORM',norm64)
    if(.not.ieee_is_finite(rho64).or..not.ieee_is_finite(norm64)) return
    if(rho64<=0.0_real64.or.norm64<=0.0_real64) return
    if(.not.SAME64(rho64,1.0_real64/terminal_keff64)) return
    call SPOR64_BOOT_CANONICAL64_CHECK(ipax,ipaxtrack,ipaxsystem,ipaxmacro,ok)
    if(.not.ok) return

    ! This short path belongs to one fresh, bounded host cwd. It is a private
    ! disk-backed tree so all physical records can be retained without a
    ! second giant in-memory archive. A pre-existing stage is never reused.
    inquire(file=trim(stage_file),exist=exists)
    if(exists) return
    call LCMOP(stage,stage_file,0,2,0)
    stage_open=.true.
    if(.not.EMPTY_ROOT(stage)) goto 900
    version=1;epoch=0;nplane=NP
    call LCMPTC(stage,'SIGNATURE',12,global_signature)
    call LCMPUT(stage,'VERSION',1,1,version)
    call LCMPUT(stage,'NPLANE',1,1,nplane)
    call LCMPUT(stage,'EPOCH',1,1,epoch)
    call LCMPTC(stage,'ROLE',12,global_role)
    call LCMPTC(stage,'STATE',12,global_state)
    call LCMPTC(stage,'CASE',12,contract%case_name)
    call LCMPUT(stage,'KEFF64',1,4,terminal_keff64)
    call LCMPUT(stage,'RHO64',1,4,rho64)
    call LCMPUT(stage,'NORM64',1,4,norm64)
    call LCMPUT(stage,'RESIDUALS',3,4,terminal_resid64)
    call LCMPUT(stage,'COUNTERS',2,1,terminal_counters)
    call LCMPUT(stage,'INNER-STATE',1,1,terminal_inner_state)
    call LCMPUT(stage,'CAPS',2,1,caps)
    call LCMPUT(stage,'TERM-EPS',3,4,eps64)
    child=LCMDID(stage,'AX');call LCMEQU(ipax,child)
    child=LCMDID(stage,'AXTRACK');call LCMEQU(ipaxtrack,child)
    child=LCMDID(stage,'AXSYSTEM');call LCMEQU(ipaxsystem,child)
    child=LCMDID(stage,'AXMACRO');call LCMEQU(ipaxmacro,child)
    child=LCMDID(stage,'ARCHIVE');call LCMEQU(iparchive,child)
    child=LCMDID(stage,'RCON');call LCMEQU(ipcontract,child)
    if(.not.EXACT_INVENTORY(stage,global_names)) goto 900
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(stage,ipax,ipaxtrack,ipaxsystem, &
        ipaxmacro,iparchive,ipcontract,checked_contract,ok)
    if(.not.ok) goto 900
    if(checked_contract%case_name/=contract%case_name) goto 900
    ! Recheck the caller's fresh root after the complete private preflight.
    ! Copy a tree without lifecycle markers. Only this caller commits it,
    ! with EPOCH as the last output mutation after the complete payload.
    if(.not.EMPTY_ROOT(ipout)) goto 900
    call LCMDEL(stage,'STATE')
    call LCMDEL(stage,'EPOCH')
    call LCMEQU(stage,ipout)
    call LCMPTC(ipout,'STATE',12,global_state)
    call LCMPUT(ipout,'EPOCH',1,1,epoch)
    call SPOR64_BOOT_CONTEXT64_GLOBAL_CHECK(ipout,ipax,ipaxtrack,ipaxsystem, &
        ipaxmacro,iparchive,ipcontract,checked_contract,ok)
    if(.not.ok) call XABORT('BOOT GLOBAL64: COMMITTED OUTPUT READBACK FAILED.')
    status=SPOR64_BOOT_GLOBAL_PUBLISHED
900 continue
    if(stage_open) call LCMCL(stage,2)
  end subroutine SPOR64_BOOT_GLOBAL_PUBLISH

  logical function FIELD_MATCHES(object,name,values) result(ok)
    type(c_ptr), intent(in) :: object
    character(len=*), intent(in) :: name
    real(real64), intent(in) :: values(:,:)
    type(c_ptr) :: list
    real(real64), allocatable :: group(:)
    integer :: ig,i,n,t,istat
    ok=.false.
    if(size(values,2)/=NG.or.size(values,1)<=0) return
    if(.not.RECORD_MATCHES(object,name,NG,10)) return
    list=LCMGID(object,name)
    allocate(group(size(values,1)),stat=istat)
    if(istat/=0) return
    do ig=1,NG
      call LCMLEL(list,ig,n,t)
      if(n/=size(group).or.t/=4) return
      call LCMGDL(list,ig,group)
      do i=1,size(group)
        if(.not.SAME64(group(i),values(i,ig))) return
      enddo
    enddo
    ok=.true.
  end function FIELD_MATCHES

  pure logical function SAME64(a,b)
    real(real64), intent(in) :: a,b
    SAME64=transfer(a,0_int64)==transfer(b,0_int64)
  end function SAME64
end module SPOR64_BOOT_PUBLISH64
