program test_actual_AB_warm_ingress64
  ! Read-only actual archive check of the NEW typed ingress. No kernel solve.
  use GANLIB
  use AXMAT_NATIVE_PRODUCER_CHAIN, only: AXMAT_LOAD_WARM_NATIVE64, AXMAT_SEED64_LOADED
  use, intrinsic :: iso_fortran_env, only: int32,int64,real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  integer, parameter :: ng=370,nu=14,nr=8
  type(c_ptr) :: archive,objects,flux,track,fg64,fg32,sg64,sg32
  real(real64), allocatable :: loaded(:,:)
  real(real64) :: keff,saved_keff,f64(nu),s64(nu)
  real(real32) :: f32(nu),s32(nu)
  integer :: status,n,t,g,i,key(nr),flux_low_bits,source_low_bits,groups_checked
  character(len=512) :: filename
  character(len=12) :: signature
  character(len=1) :: case_name
  if(command_argument_count()/=2) error stop 'two exact arguments required'
  call get_command_argument(1,filename)
  call get_command_argument(2,case_name)
  if(len_trim(filename)>72.or.len_trim(filename)==0) error stop 'LCM filename bound'
  if(case_name/='A'.and.case_name/='B') error stop 'declared A/B case'
  call LCMOP(archive,trim(filename),2,2,0)
  call require(archive,'SIGNATURE',3,3)
  call LCMGTC(archive,'SIGNATURE',12,signature)
  if(signature/='L_ARCHIVE') error stop 'archive signature'
  call require(archive,'LISTDIM',1,1)
  call LCMGET(archive,'LISTDIM',n)
  if(n/=1) error stop 'one actual offline snapshot'
  call require(archive,'FLUX',1,10)
  objects=LCMGID(archive,'FLUX');flux=LCMGIL(objects,1)
  call require(archive,'TRACK',1,10)
  objects=LCMGID(archive,'TRACK');track=LCMGIL(objects,1)
  call require(track,'KEYFLX',nr,1)
  call LCMGET(track,'KEYFLX',key)
  if(any(key<1).or.any(key>nu)) error stop 'scalar map bound'
  do i=1,nr
    if(count(key==key(i))/=1) error stop 'unique scalar map'
  enddo
  call AXMAT_LOAD_WARM_NATIVE64(flux,nu,ng,loaded,keff,status)
  if(status/=AXMAT_SEED64_LOADED) error stop 'actual new loader refusal'
  if(.not.allocated(loaded)) error stop 'loader allocation'
  if(any(shape(loaded)/=[nu,ng])) error stop 'full typed shape'
  if(.not.all(ieee_is_finite(loaded)).or.any(loaded(key,:)<=0.0_real64)) &
    error stop 'actual scalar field'
  call require(flux,'SPOT-KEFF64',1,4)
  call LCMGET(flux,'SPOT-KEFF64',saved_keff)
  if(transfer(keff,0_int64)/=transfer(saved_keff,0_int64)) error stop 'native keff bits'
  call require(flux,'FLUX64',ng,10);fg64=LCMGID(flux,'FLUX64')
  call require(flux,'FLUX',ng,10);fg32=LCMGID(flux,'FLUX')
  call require(flux,'SOUR64',ng,10);sg64=LCMGID(flux,'SOUR64')
  call require(flux,'SOUR',ng,10);sg32=LCMGID(flux,'SOUR')
  flux_low_bits=0;source_low_bits=0;groups_checked=0
  do g=1,ng
    call require_item(fg64,g,nu,4);call LCMGDL(fg64,g,f64)
    call require_item(fg32,g,nu,2);call LCMGDL(fg32,g,f32)
    call require_item(sg64,g,nu,4);call LCMGDL(sg64,g,s64)
    call require_item(sg32,g,nu,2);call LCMGDL(sg32,g,s32)
    if(.not.all(ieee_is_finite(f64)).or..not.all(ieee_is_finite(s64))) error stop 'finite native pair'
    do i=1,nu
      if(transfer(loaded(i,g),0_int64)/=transfer(f64(i),0_int64)) error stop 'full native ingress bits'
      if(transfer(real(f64(i),real32),0_int32)/=transfer(f32(i),0_int32)) error stop 'exact flux mirror'
      if(transfer(real(s64(i),real32),0_int32)/=transfer(s32(i),0_int32)) error stop 'exact source mirror'
      if(transfer(f64(i),0_int64)/=transfer(real(f32(i),real64),0_int64)) flux_low_bits=flux_low_bits+1
      if(transfer(s64(i),0_int64)/=transfer(real(s32(i),real64),0_int64)) source_low_bits=source_low_bits+1
    enddo
    groups_checked=groups_checked+1
  enddo
  if(groups_checked/=ng.or.flux_low_bits==0) error stop 'real data must expose mirror round trip'
  call LCMCL(archive,1)
  write(*,'(A,A,A,I0,A,I0,A)') &
    '{"schema":"ACTUAL_NEW_REAL64_WARM_INGRESS_V1","case":"',case_name, &
    '","status":"PASS","groups":370,"unknowns":14,"scalar_regions":8,"flux_values":5180,'// &
    '"native_flux_bits_equal":true,"native_keff_bits_equal":true,"flux_non32_roundtrip_count":', &
    flux_low_bits,',"source_non32_roundtrip_count":',source_low_bits, &
    ',"archive_read_only":true,"transport_executed":false,"producer_qualified":false,'// &
    '"online_BOOT_qualified":false,"original_seventeen_controls_qualified":false,"goal_complete":false}'
contains
  subroutine require(p,name,length,type_code)
    type(c_ptr), intent(in) :: p
    character(len=*), intent(in) :: name
    integer, intent(in) :: length,type_code
    integer :: actual_length,actual_type
    call LCMLEN(p,name,actual_length,actual_type)
    if(actual_length/=length.or.actual_type/=type_code) error stop 'exact named record shape/type'
  end subroutine require
  subroutine require_item(p,index,length,type_code)
    type(c_ptr), intent(in) :: p
    integer, intent(in) :: index,length,type_code
    integer :: actual_length,actual_type
    call LCMLEL(p,index,actual_length,actual_type)
    if(actual_length/=length.or.actual_type/=type_code) error stop 'exact list item shape/type'
  end subroutine require_item
end program test_actual_AB_warm_ingress64
