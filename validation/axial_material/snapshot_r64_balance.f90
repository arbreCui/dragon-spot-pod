subroutine AXMAT_BALANCE64(ipmacr,ngrp,ileak,nmat,nreg,icreb,nun,nanis, &
    mat,vol,key,xstrc,xsdia,xcsou,igdeb,b2,nmerg,imerg,difhet,keycur,matalb,albedo,surfac,flux)
  use GANLIB
  use SPOR64_A9, only: FLUBAL64
  use, intrinsic :: iso_fortran_env, only: real32,real64
  use, intrinsic :: ieee_arithmetic, only: ieee_is_finite
  implicit none
  type(c_ptr) :: ipmacr,groups,g
  integer :: ngrp,ileak,nmat,nreg,icreb,nun,nanis,igdeb,nmerg
  integer :: mat(nreg),key(nreg),imerg(nmat),keycur(icreb),matalb(icreb)
  real(real32) :: vol(nreg),xstrc(0:nmat,ngrp),xsdia(0:nmat,0:nanis,ngrp)
  real(real32) :: b2(4),difhet(nmerg,ngrp),albedo(6),surfac(icreb)
  real(real64) :: xcsou(ngrp),flux(nun,ngrp),leakage(ngrp)
  integer :: njj(nmat,ngrp),ijj(nmat,ngrp),ipos(nmat,ngrp),nscat(ngrp),ig,n,t
  real(real32),allocatable :: scat(:,:)
  logical :: ok
  if(ngrp/=370.or.ileak/=0.or.nmat/=8.or.nreg/=8.or.nun/=14.or.icreb/=6) &
    call XABORT('AXMAT REBALANCE: unsupported scope')
  if(any(b2/=0).or..not.all(ieee_is_finite(flux))) call XABORT('AXMAT REBALANCE: invalid input')
  allocate(scat(nmat*ngrp,ngrp));scat=0;leakage=0
  groups=LCMGID(ipmacr,'GROUP')
  do ig=1,ngrp
    g=LCMGIL(groups,ig)
    call LCMLEN(g,'NJJS00',n,t)
    if(n/=nmat.or.t/=1) call XABORT('AXMAT REBALANCE: bad sparse counts')
    call LCMGET(g,'NJJS00',njj(:,ig));call LCMGET(g,'IJJS00',ijj(:,ig));call LCMGET(g,'IPOS00',ipos(:,ig))
    call LCMLEN(g,'SCAT00',n,t)
    if(n<1.or.n>nmat*ngrp.or.t/=2) call XABORT('AXMAT REBALANCE: bad scattering')
    nscat(ig)=n;call LCMGET(g,'SCAT00',scat(:n,ig))
  enddo
  if(.not.all(ieee_is_finite(scat))) call XABORT('AXMAT REBALANCE: nonfinite scattering')
  call FLUBAL64(mat,vol,key,xstrc,xsdia(:,0,:),leakage,xcsou,igdeb, &
      keycur,matalb,albedo,surfac,njj,ijj,ipos,nscat,scat,flux,ok)
  if(.not.ok) call XABORT('AXMAT REBALANCE: double balance failed')
  deallocate(scat)
end subroutine
