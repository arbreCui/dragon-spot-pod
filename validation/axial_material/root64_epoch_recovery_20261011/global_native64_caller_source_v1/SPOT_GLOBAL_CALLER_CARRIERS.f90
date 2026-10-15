module SPOT_GLOBAL_CALLER_CARRIERS
  ! Numerical ingress only. Stored coherence is never an external qualification.
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: int32,real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  private
  integer, parameter :: kind_guard=1/merge(1,0, &
    kind(1)==int32.and.kind(1.0)==real32.and.kind(0.0d0)==real64.and.dp==real64)
  public :: SPOT_GLOBAL_LOAD_B2_NATIVE64,SPOT_GLOBAL_LOAD_WARM64
contains
  logical function record_is(ip,name,n,t)
    type(c_ptr),intent(in)::ip
    character(len=*),intent(in)::name
    integer,intent(in)::n,t
    integer::length,kind
    call LCMLEN(ip,name,length,kind)
    record_is=length==n.and.kind==t
  end function

  subroutine SPOT_GLOBAL_LOAD_B2_NATIVE64(ip,b2,ok)
    type(c_ptr),intent(in)::ip
    real(real64),intent(out)::b2(4)
    logical,intent(out)::ok
    real(real32)::mirror
    b2=0.0_real64;ok=.false.
    if(.not.c_associated(ip))return
    if(.not.record_is(ip,'SPOT-B2H64',4,4))return
    if(.not.record_is(ip,'B2  B1HOM',1,2))return
    call LCMGET(ip,'SPOT-B2H64',b2)
    call LCMGET(ip,'B2  B1HOM',mirror)
    if(.not.all(ieee_is_finite(b2)).or..not.ieee_is_finite(mirror))return
    if(transfer(real(b2(4),real32),0_int32)/=transfer(mirror,0_int32))return
    ok=.true.
  end subroutine

  subroutine SPOT_GLOBAL_LOAD_WARM64(ip,nunk,ngrp,nreg,keys,initial_flux64,keff64,ok)
    type(c_ptr),intent(in)::ip
    integer,intent(in)::nunk,ngrp,nreg,keys(nreg)
    real(real64),intent(out)::initial_flux64(nunk,ngrp),keff64
    logical,intent(out)::ok
    integer::state(40),saved_keys(nreg),ig,i,length,kind
    real(real32)::mirror(nunk),k32
    real(real64)::source(nunk)
    type(c_ptr)::native,legacy,nsour,lsour
    initial_flux64=0.0_real64;keff64=0.0_real64;ok=.false.
    if(.not.c_associated(ip).or.nunk<=0.or.ngrp<=0.or.nreg<=0)return
    if(.not.record_is(ip,'STATE-VECTOR',40,1))return
    call LCMGET(ip,'STATE-VECTOR',state)
    if(state(1)/=ngrp.or.state(2)/=nunk.or.state(3)/=1)return
    if(state(6)/=2.and.state(6)/=3)return
    if(state(7)/=0.and.state(7)/=3)return
    if(.not.record_is(ip,'KEYFLX',nreg,1))return
    call LCMGET(ip,'KEYFLX',saved_keys)
    if(any(saved_keys/=keys).or.any(keys<0).or.any(keys>nunk))return
    if(.not.record_is(ip,'SPOT-KEFF64',1,4))return
    if(.not.record_is(ip,'K-EFFECTIVE',1,2))return
    call LCMGET(ip,'SPOT-KEFF64',keff64)
    call LCMGET(ip,'K-EFFECTIVE',k32)
    if(.not.ieee_is_finite(keff64).or.keff64<=0.0_real64)return
    if(.not.ieee_is_finite(k32))return
    if(transfer(real(keff64,real32),0_int32)/=transfer(k32,0_int32))return
    if(.not.record_is(ip,'FLUX64',ngrp,10))return
    if(.not.record_is(ip,'FLUX',ngrp,10))return
    if(.not.record_is(ip,'SOUR64',ngrp,10))return
    if(.not.record_is(ip,'SOUR',ngrp,10))return
    native=LCMGID(ip,'FLUX64');legacy=LCMGID(ip,'FLUX')
    nsour=LCMGID(ip,'SOUR64');lsour=LCMGID(ip,'SOUR')
    do ig=1,ngrp
      call LCMLEL(native,ig,length,kind)
      if(length/=nunk.or.kind/=4)return
      call LCMLEL(legacy,ig,length,kind)
      if(length/=nunk.or.kind/=2)return
      call LCMGDL(native,ig,initial_flux64(:,ig))
      call LCMGDL(legacy,ig,mirror)
      if(.not.all(ieee_is_finite(initial_flux64(:,ig))).or..not.all(ieee_is_finite(mirror)))return
      do i=1,nunk
        if(transfer(real(initial_flux64(i,ig),real32),0_int32)/=transfer(mirror(i),0_int32))return
      enddo
      call LCMLEL(nsour,ig,length,kind)
      if(length/=nunk.or.kind/=4)return
      call LCMLEL(lsour,ig,length,kind)
      if(length/=nunk.or.kind/=2)return
      call LCMGDL(nsour,ig,source)
      call LCMGDL(lsour,ig,mirror)
      if(.not.all(ieee_is_finite(source)).or..not.all(ieee_is_finite(mirror)))return
      do i=1,nunk
        if(transfer(real(source(i),real32),0_int32)/=transfer(mirror(i),0_int32))return
      enddo
    enddo
    ok=.true.
  end subroutine
end module SPOT_GLOBAL_CALLER_CARRIERS
