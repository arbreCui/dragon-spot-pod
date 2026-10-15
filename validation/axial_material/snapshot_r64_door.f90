subroutine AXMAT_MCCG_DOOR64(jpsys,npsys,iptrk,iftrak,impx,ngrp,nmat,nreg,nun, &
    mat,vol,keyflx,title,ileak,b2,nmerg,imerg,difhet,old,source,flux)
  use GANLIB
  use, intrinsic :: iso_fortran_env, only: real32,real64,int32,int64
  use SPOR64_A8, only: DOORFV64
  use SPOR64_RCONTRACT, only: SPOR64_ROUTE_CONTRACT
  implicit none
  type(c_ptr) :: jpsys,iptrk
  integer :: iftrak,impx,ngrp,nmat,nreg,nun,ileak,nmerg
  integer :: npsys(ngrp),mat(nreg),keyflx(nreg),imerg(nmat)
  real(real32) :: vol(nreg),b2(4),difhet(nmerg,ngrp),control(4)
  real(real64) :: old(nun,ngrp),source(nun,ngrp),flux(nun,ngrp)
  real(real64) :: leakage(ngrp)
  character(len=72) :: title
  type(SPOR64_ROUTE_CONTRACT) :: contract
  integer(int64) :: cutoff
  logical :: ok
  integer :: n,t
  if(ngrp/=370.or.nmat/=8.or.nreg/=8.or.nun/=14.or.ileak/=0) &
    call XABORT('AXMAT SNAPSHOT: unsupported radial problem')
  if(any(b2/=0.0_real32)) call XABORT('AXMAT SNAPSHOT: nonzero buckling')
  call LCMLEN(iptrk,'REAL-PARAM',n,t)
  if(n/=4.or.t/=2) call XABORT('AXMAT SNAPSHOT: missing controls')
  call LCMGET(iptrk,'REAL-PARAM',control)
  if(control(1)/=2.5e-8_real32.or.any(control(2:4)/=0.0_real32)) &
    call XABORT('AXMAT SNAPSHOT: undeclared radial tolerance')
  ! Only eps_mccg_bits is consumed by the A8 door. This local object is
  ! not a route/lifecycle contract and is never supplied to B2B or B2C.
  contract%eps_mccg_bits=transfer(control(1),0_int32)
  leakage=0.0_real64
  call DOORFV64(jpsys,npsys,iptrk,iftrak,impx,ngrp,nun,keyflx,title, &
    leakage,source,flux,contract,cutoff,ok)
  if(.not.ok) call XABORT('AXMAT SNAPSHOT: true inner terminal failed')
end subroutine
