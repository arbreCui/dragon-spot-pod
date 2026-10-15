program verify_native_A_archive64
  ! Genuine readonly XSM checks. No transport, clone of physical library, or seal publication.
  use GANLIB
  use SPOR64_BOOT64, only: SPOR64_BOOT64_READ_NATIVE, ROOT64_LOADED
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT,SPOR64_RCONTRACT_LOAD
  use AXMAT_NATIVE_PRODUCER_CHAIN, only: AXMAT_LOAD_WARM_NATIVE64, &
      AXMAT_SEED64_LOADED,AXMAT_SEED64_REFUSED
  use SPOR64_VERIFY, only: EXACT_INVENTORY,CHARACTER_RECORD_MATCHES,RECORD_MATCHES
  use, intrinsic :: iso_fortran_env, only: int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: ng=370,nu=14,nr=8
  type(c_ptr) :: archive,flux,track,system,material,contract,bind,seal
  type(c_ptr) :: fg,sg,sm,clone,child
  real(real64), allocatable :: admitted(:,:),loaded(:,:)
  real(real64) :: k,f64(nu),s64(nu),gates(3),limits(3),cutoff64
  real(real32) :: f32(nu),s32(nu),cutoff(4)
  integer :: n,t,status,plane,epoch,g,i,j,key(nr),terms(3),flux_non32,source_non32
  character(len=512) :: filename
  character(len=32) :: mode
  character(len=12) :: signature
  character(len=16) :: kbits
  character(len=26) :: numbers(4)
  type(SPOR64_ROUTE_CONTRACT) :: route
  logical :: valid
  character(len=12), parameter :: route_names(6)= &
      ['SIGNATURE   ','CASE-NAME   ','EPS-TERMINAL','FLU-CAPS    ','FLU-ACCE    ','FLU-OPTION  ']
  character(len=12), parameter :: bind_names(3)=['SIGNATURE   ','PLANE       ','EPOCH       ']
  if(command_argument_count()/=2) error stop 'mode and exact relative filename required'
  call get_command_argument(1,mode);call get_command_argument(2,filename)
  if(len_trim(filename)==0.or.len_trim(filename)>72) error stop 'LCM filename limit'
  if(mode/='native'.and.mode/='case'.and.mode/='loader_controls') error stop 'declared readonly mode'
  call LCMOP(archive,trim(filename),2,2,0)
  call require(archive,'SIGNATURE',3,3)
  call LCMGTC(archive,'SIGNATURE',12,signature)
  if(signature/='L_ARCHIVE') error stop 'L_ARCHIVE required'
  call require(archive,'LISTDIM',1,1);call LCMGET(archive,'LISTDIM',n)
  if(n/=1) error stop 'only plane1 single snapshot scope'
  if(mode=='case') then
    contract=object(archive,'RCONTRACT');bind=object(archive,'BOOT_BIND')
    call check_case(contract,bind)
    call LCMCL(archive,1)
    write(*,'(A)') '{"schema":"ACTUAL_CURRENT_WARM_A_CASE_CLE_READBACK_V1",'// &
      '"case":"AXNCASE64_current_standard_CLE_positive","all_actual_assertions_completed":true,'// &
      '"case_name":"R64WARM-A-V1 ","plane":1,"epoch":0,"record_inventory_exact":true,'// &
      '"archive_read_only":true,"transport_executed":false,"producer_qualified":false}'
    stop
  endif
  flux=object(archive,'FLUX')
  if(mode=='loader_controls') then
    call AXMAT_LOAD_WARM_NATIVE64(flux,nu,ng,loaded,k,status)
    if(status/=AXMAT_SEED64_LOADED.or..not.allocated(loaded)) error stop 'actual baseline typed seed'
    if(any(shape(loaded)/=[nu,ng])) error stop 'actual full warm extent'
    call require(flux,'FLUX64',ng,10);fg=LCMGID(flux,'FLUX64')
    do g=1,ng
      call item(fg,g,nu,4);call LCMGDL(fg,g,f64)
      if(any(transfer(f64,[0_int64],nu)/=transfer(loaded(:,g),[0_int64],nu))) &
        error stop 'actual baseline all370 native bits'
    enddo
    deallocate(loaded)
    do j=1,7
      call LCMOP(clone,'WARM-LOADER-CONTROL',0,1,0)
      call LCMEQU(flux,clone)
      select case(j)
      case(1)
        call LCMDEL(clone,'FLUX64')
      case(2)
        child=LCMGID(clone,'FLUX64');call LCMGDL(child,1,f64)
        call LCMPDL(child,1,nu,2,real(f64,real32))
      case(3)
        child=LCMGID(clone,'SOUR');call LCMGDL(child,1,s32)
        s32(1)=s32(1)+1.0_real32;call LCMPDL(child,1,nu,2,s32)
      case(4)
        call LCMDEL(clone,'SPOT-KEFF64')
      case(5)
        child=LCMGID(clone,'FLUX64');call LCMGDL(child,1,f64)
        call LCMPDL(child,1,nu-1,4,f64(:nu-1))
      case(6)
        child=LCMGID(clone,'SOUR64');call LCMGDL(child,1,s64)
        call LCMPDL(child,1,nu,2,real(s64,real32))
      case(7)
        call LCMGET(clone,'K-EFFECTIVE',f32(1))
        f32(1)=f32(1)+1.0_real32;call LCMPUT(clone,'K-EFFECTIVE',1,2,f32(1))
      end select
      allocate(loaded(2,3));loaded=73.0_real64;k=42.0_real64
      call AXMAT_LOAD_WARM_NATIVE64(clone,nu,ng,loaded,k,status)
      if(status/=AXMAT_SEED64_REFUSED.or.allocated(loaded).or.transfer(k,0_int64)/=0_int64) &
        error stop 'actual loader refusal/full output reset'
      call LCMCL(clone,2)
    enddo
    call LCMCL(archive,1)
    write(*,'(A)') '{"schema":"ACTUAL_CURRENT_WARM_A_LOADER_CONTROLS_V1",'// &
      '"all_actual_assertions_completed":true,"actual_loader_calls":8,"actual_refusals":7,'// &
      '"groups":370,"unknowns":14,"archive_read_only":true,"transport_executed":false,'// &
      '"producer_qualified":false,"online_BOOT_qualified":false}'
    stop
  endif
  track=object(archive,'TRACK');system=object(archive,'SYSTEM')
  material=object(archive,'MICROLIB2');contract=object(archive,'RCONTRACT')
  bind=object(archive,'BOOT_BIND');call check_case(contract,bind)
  call SPOR64_BOOT64_READ_NATIVE(flux,track,system,material,contract,1,0,admitted,status)
  if(status/=ROOT64_LOADED.or..not.allocated(admitted)) error stop 'complete actual Native READ refused'
  if(any(shape(admitted)/=[nu,ng])) error stop 'all unknowns including surface currents required'
  call require(flux,'SOUR64',ng,10);sg=LCMGID(flux,'SOUR64')
  call require(flux,'SOUR',ng,10);sm=LCMGID(flux,'SOUR')
  call require(flux,'KEYFLX',nr,1);call LCMGET(flux,'KEYFLX',key)
  if(any(key<1).or.any(key>nu)) error stop 'valid scalar key map'
  do i=1,nr
    if(count(key==key(i))/=1) error stop 'unique scalar key map'
  enddo
  flux_non32=0;source_non32=0
  do g=1,ng
    call item(sg,g,nu,4);call item(sm,g,nu,2)
    call LCMGDL(sg,g,s64);call LCMGDL(sm,g,s32)
    if(.not.all(ieee_is_finite(s64)).or..not.all(ieee_is_finite(real(s64,real32)))) &
      error stop 'finite full native source and mirror'
    if(any(transfer(s32,[0_int32],nu)/=transfer(real(s64,real32),[0_int32],nu))) &
      error stop 'exact full source mirror'
    flux_non32=flux_non32+count(transfer(admitted(:,g),[0_int64],nu)/= &
      transfer(real(real(admitted(:,g),real32),real64),[0_int64],nu))
    source_non32=source_non32+count(transfer(s64,[0_int64],nu)/= &
      transfer(real(s32,real64),[0_int64],nu))
  enddo
  if(any(admitted(key,:)<=0.0_real64)) error stop 'positive scalar native flux'
  call require(track,'REAL-PARAM',4,2);call LCMGET(track,'REAL-PARAM',cutoff)
  if(transfer(cutoff(1),0_int32)/=transfer(2.5e-8_real32,0_int32).or.any(cutoff(2:4)/=0.0)) &
      error stop 'actual MCCG original cutoff'
  call require(flux,'SPOT-KEFF64',1,4);call LCMGET(flux,'SPOT-KEFF64',k)
  call require(flux,'ROOT64-SEAL',-1,0);seal=LCMGID(flux,'ROOT64-SEAL')
  call require(seal,'GATE64',3,4);call LCMGET(seal,'GATE64',gates)
  call require(seal,'LIMIT64',3,4);call LCMGET(seal,'LIMIT64',limits)
  call require(seal,'TERM-INT',3,1);call LCMGET(seal,'TERM-INT',terms)
  if(any(gates<0.0_real64).or.any(gates>=limits).or.terms(3)/=1) error stop 'genuine strict seal gate'
  if(terms(1)<2.or.terms(1)>500.or.terms(2)<1.or.terms(2)>740) error stop 'original caps'
  ! No imposed positive non32 count: native arithmetic may legitimately round exactly.
  write(kbits,'(Z16.16)') transfer(k,0_int64)
  write(numbers(1),'(ES26.17E3)') k
  do i=1,3
    write(numbers(i+1),'(ES26.17E3)') gates(i)
  enddo
  call LCMCL(archive,1)
  write(*,'(A,I0,A,I0,A,I0,A,I0,A)') &
    '{"schema":"ACTUAL_NEW_WARM_A_COMPLETE_NATIVE_TERMINAL_READBACK_V1","status":"PASS",'// &
    '"plane":1,"epoch":0,"groups":370,"unknowns":14,"scalar_regions":8,'// &
    '"full_native_read_status":3,"all370_ROOT_FLUX64_FLUX64_REF_bits_equal":true,'// &
    '"full_source64_type4_finite_and_exact_mirror":true,"archive_read_only":true,'// &
    '"keff64":'//trim(adjustl(numbers(1)))//',"keff64_bits":"'//kbits// &
    '","residual64":['//trim(adjustl(numbers(2)))//','//trim(adjustl(numbers(3)))// &
    ','//trim(adjustl(numbers(4)))//'],"strict_terminal_gate_passed":true,"outer_iterations":', &
    terms(1),',"inner_iterations":',terms(2),',"flux_non32_roundtrip_count":',flux_non32, &
    ',"source_non32_roundtrip_count":',source_non32, &
    ',"three_plane_qualified":false,"GLOBAL_qualified":false,"rank_qualified":false,'// &
    '"online_BOOT_qualified":false,"AAA_qualified":false,"ABA_admitted":false,"goal_complete":false}'
contains
  function object(root,name) result(p)
    type(c_ptr), intent(in) :: root
    character(len=*), intent(in) :: name
    type(c_ptr) :: p,list
    call require(root,name,1,10);list=LCMGID(root,name)
    call item(list,1,-1,0);p=LCMGIL(list,1)
  end function object
  subroutine check_case(p,b)
    type(c_ptr), intent(in) :: p,b
    call SPOR64_RCONTRACT_LOAD(p,route,valid)
    if(.not.valid.or..not.EXACT_INVENTORY(p,route_names).or..not.EXACT_INVENTORY(b,bind_names)) &
      error stop 'exact case/bind schema'
    if(route%case_name/='R64WARM-A-V1 '.or.route%flu_option/='B0  '.or. &
      route%flu_maxout/=500.or.route%flu_maxinr/=740.or.route%flu_acce_free/=3.or.route%flu_acce_accel/=3) &
      error stop 'retained case caps/names'
    if(route%eps_radial_bits/=transfer(2.5e-7_real32,0_int32).or. &
      route%eps_axial_bits/=transfer(5e-8_real32,0_int32).or. &
      route%eps_mccg_bits/=transfer(2.5e-8_real32,0_int32)) error stop 'retained case eps bits'
    if(.not.CHARACTER_RECORD_MATCHES(b,'SIGNATURE',3,12,'L_BOOTBIND')) error stop 'binding signature'
    call require(b,'PLANE',1,1);call require(b,'EPOCH',1,1)
    call LCMGET(b,'PLANE',plane);call LCMGET(b,'EPOCH',epoch)
    if(plane/=1.or.epoch/=0) error stop 'explicit independent plane1/e0'
  end subroutine check_case
  subroutine require(p,name,length,type_code)
    type(c_ptr), intent(in) :: p
    character(len=*), intent(in) :: name
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type
    call LCMLEN(p,name,actual_length,actual_type)
    if(actual_length/=length.or.actual_type/=type_code) error stop 'exact named record type/extent'
  end subroutine require
  subroutine item(p,index,length,type_code)
    type(c_ptr), intent(in) :: p
    integer, intent(in) :: index,length,type_code
    integer :: actual_length,actual_type
    call LCMLEL(p,index,actual_length,actual_type)
    if(actual_length/=length.or.actual_type/=type_code) error stop 'exact list item type/extent'
  end subroutine item
end program verify_native_A_archive64
