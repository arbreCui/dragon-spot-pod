!-----------------------------------------------------------------------
!
!Purpose:
! solution of the SN equations with the synthesis Proper orthogonal
! tracking (SPOT) method.
!
!Copyright:
! Copyright (C) 2025 Ecole Polytechnique de Montreal
! This library is free software; you can redistribute it and/or
! modify it under the terms of the GNU Lesser General Public
! License as published by the Free Software Foundation; either
! version 2.1 of the License, or (at your option) any later version
!
!Author(s): A. Hebert
!
!Parameters: input
! nreg2d  number of meshes in the xy plane.
! nfloor  number of axial floors.
! ielem   degree of the spatial approximation (=1: diamond scheme).
! nmat    number of material mixtures.
! nsnap   number of snapshots.
! ischm   method of spatial discretisation:
!         =1: High-Order Diamond Differencing (HODD) - default;
!         =2: Discontinuous Galerkin finite element method (DG).
! npq     number of SN directions.
! nsct    maximum number of spherical harmonics moments of the flux
!         (1: isotropic scattering in LAB; 2: linearly anisotropic).
! mat1d   snapshot index assigned to each floor.
! vol1d   width of each floor.
! mat     material mixture index in each region.
! vol     volumes of each region.
! keyflx  index of flux components in unknown vector.
! total   macroscopic total cross sections.
! db2     radial DB2 leakage on each snapshot.
! ncode   axial boundary condition indices.
! zcode   axial albedos.
! qext    legendre components of the fixed source.
! lfixup  flag to enable negative flux fixup.
! du      first direction cosines ($\mu$).
! w       weights.
! pl      discrete values of the spherical harmonics corresponding
!         to the 1D SN quadrature.
! xnei    SN boundary fluxes on the input plane.
!
!Parameters: output
! flux    Legendre components of the flux.
! cour    net currents on boundary meshes.
! xnei    SN boundary fluxes on the exit plane.
!
!-----------------------------------------------------------------------
!
subroutine SPOT1P(nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct, &
& lfixup,mat1d,vol1d,mat,keyflx,total,sgas,db2,ncode,zcode,qext, &
& du,w,pl,flux,cour,xnei)
  !----
  !  subroutine arguments
  !----
  integer nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,mat1d(nfloor), &
  & mat(nfloor,nreg2d),keyflx(nfloor,nreg2d),ncode(2)
  real vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct),zcode(2), &
  & qext(ielem,nsct,nfloor,nreg2d),du(npq),w(npq),pl(nsct,npq), &
  & flux(ielem,nsct,nfloor,nreg2d),cour(nfloor+1,nreg2d),xnei(npq,nreg2d)
  logical lfixup
  double precision db2(nsnap,nreg2d)
  !----
  !  local variables and allocatable arrays
  !----
  double precision, allocatable, dimension(:,:) :: AA,shoot
  double precision, allocatable, dimension(:,:,:) :: BB,afb
  double precision, allocatable, dimension(:,:,:,:) :: funk
  !
  allocate(afb(npq,nfloor+1,nreg2d),AA(npq,nreg2d),BB(npq,npq,nreg2d),funk(ielem,nfloor,npq,nreg2d), &
  & shoot(npq,npq+1))
  !----
  !  set matrix AA
  !----
  afb(:npq,:nfloor+1,:nreg2d)=0.0d0
  call swap(nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,lfixup,mat1d,vol1d,mat,keyflx, &
  & total,sgas,qext,du,w,pl,db2,afb,funk)
  AA(:npq,:nreg2d)=afb(:npq,nfloor+1,:nreg2d)
  !----
  !  set matrix BB
  !----
  do ico=1,npq
    afb(:npq,:nfloor+1,:nreg2d)=0.0d0
    afb(ico,1,:nreg2d)=1.0d0
    call swap(nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,lfixup,mat1d,vol1d,mat,keyflx, &
    & total,sgas,qext,du,w,pl,db2,afb,funk)
    do k2d=1,nreg2d
      BB(:npq,ico,k2d)=afb(:npq,nfloor+1,k2d)-AA(:npq,k2d)
    enddo
  enddo
  !----
  !  parallel shooting method
  !----
  !$omp parallel do private(shoot,ico,ip,ier)
  do k2d=1,nreg2d
    shoot(:npq,:npq)=0.0d0
    shoot(:npq,npq+1)=AA(:npq,k2d)
    if((ncode(1).eq.1).and.(ncode(2).eq.1)) then
      ! void boundary conditions
      do ico=1,npq/2
        shoot(:npq/2,ico)=-BB(:npq/2,ico,k2d)
      enddo
      do ico=npq/2+1,npq
        shoot(ico,ico)=1.0d0
      enddo
    else if((ncode(1).eq.4).and.(ncode(2).eq.4)) then
      ! tran boundary conditions
      do ico=1,npq/2
        shoot(ico,ico)=zcode(2)
        shoot(:npq,ico)=shoot(:npq,ico)-BB(:npq,ico,k2d)
      enddo
      do ico=npq/2+1,npq
        shoot(ico,ico)=1.0d0
        shoot(:npq,ico)=shoot(:npq,ico)-zcode(1)*BB(:npq,ico,k2d)
      enddo
    else
      call XABORT('SPOT1P: non supported type of boundary conditions.')
    endif
    !----
    !  shooting method solution.
    !----
    call ALSBD(npq,1,shoot,ier,npq)
    if(ier.ne.0) call XABORT('SPOT1P: singular matrix.')
    do ip=1,npq
      xnei(ip,k2d)=real(shoot(ip,npq+1))
    enddo
    !----
    !  flux reconstruction.
    !----
    if((ncode(1).eq.1).and.(ncode(2).eq.1)) then
      ! void boundary conditions
      afb(:npq/2,1,k2d)=shoot(:npq/2,npq+1)
      afb(npq/2+1:npq,1,k2d)=0.0d0
    else if((ncode(1).eq.4).and.(ncode(2).eq.4)) then
      ! tran boundary conditions
      afb(:npq/2,1,k2d)=shoot(:npq/2,npq+1)
      afb(npq/2+1:npq,1,k2d)=zcode(1)*shoot(npq/2+1:npq,npq+1)
    endif
    cour(1,k2d)=0.0 ! set inlet current
    do ip=1,npq
      cour(1,k2d)=cour(1,k2d)+w(ip)*real(afb(ip,1,k2d))*pl(2,ip)
    enddo
  enddo ! k2d
  !$omp end parallel do
  !----
  !  recompute SN flux with target boundary fluxes
  !----
  call swap(nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,lfixup,mat1d,vol1d,mat,keyflx, &
  & total,sgas,qext,du,w,pl,db2,afb,funk)
  !----
  !  compute Legendre moments of the flux.
  !----
  flux(:ielem,:nsct,:nfloor,:nreg2d)=0.0
  do ifloor=1,nfloor
    do k2d=1,nreg2d
      cour(ifloor+1,k2d)=0.0
      do ip=1,npq
        if(w(ip).eq.0.0) cycle
        do k=1,nsct
          do iel=1,ielem
            flux(iel,k,ifloor,k2d)=flux(iel,k,ifloor,k2d)+w(ip)*real(funk(iel,ifloor,ip,k2d))* &
            & pl(k,ip)
          enddo
        enddo
        cour(ifloor+1,k2d)=cour(ifloor+1,k2d)+w(ip)*real(afb(ip,ifloor+1,k2d))*pl(2,ip)
      enddo
    enddo
  enddo
  deallocate(shoot,funk,BB,AA,afb)
  return
  contains
  subroutine swap(nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,lfixup,mat1d,vol1d,mat,keyflx, &
    & total,sgas,qext,du,w,pl,db2,afb,funk)
    ! perform swapping over the domain for many angles
    !----
    !  subroutine arguments
    !----
    integer,intent(in) :: nreg2d,nfloor,ielem,nmat,nsnap,ischm,npq,nsct,mat1d(nfloor), &
    & mat(nfloor,nreg2d),keyflx(nfloor,nreg2d)
    real,intent(in) :: vol1d(nfloor),total(0:nmat),sgas(0:nmat,nsct),qext(ielem,nsct,nfloor,nreg2d), &
    & du(npq),w(npq),pl(nsct,npq)
    logical,intent(in) :: lfixup
    double precision,intent(in) :: db2(nsnap,nreg2d)
    double precision,intent(inout) :: afb(npq,nfloor+1,nreg2d)
    double precision,intent(out) :: funk(ielem,nfloor,npq,nreg2d)
    !----
    !  local variables and allocatable arrays
    !----
    parameter(rlog=1.0e-8)
    double precision ssss,sig(4,4),qqq(4)
    double precision, allocatable, dimension(:) :: q
    double precision, allocatable, dimension(:,:) :: sigt_m
    !
    if(ischm.eq.2) call XABORT('swap: DG not implemented.')
    iepq=ielem*npq
    allocate(q(ielem),sigt_m(iepq,iepq+1))
    !----
    !  parallel SPOT flux solution over radial positions.
    !----
    !$omp parallel do private(ifloor,isnap,ip,jnd1,ibm,volume,il,i,j,q,sig,qqq,ie1,ie2,ier,ssign)
    do k2d=1,nreg2d
      do ifloor=1,nfloor
        sigt_m(:iepq,:iepq+1)=0.0d0
        isnap=mat1d(ifloor)
        volume=vol1d(ifloor)
        jnd1=keyflx(ifloor,k2d)
        ibm=mat(ifloor,k2d)
        if(ibm.eq.0) cycle
        do ip=1,npq
          if(w(ip).eq.0.0) cycle
          do ie1=1,ielem
            q(ie1)=0.0
            do il=0,nsct-1
              q(ie1)=q(ie1)+qext(ie1,il+1,ifloor,k2d)*pl(il+1,ip)/2.0
            enddo
          enddo
          if(ielem.eq.1) then
            sig(1,1)=total(ibm)*volume+2.d0*du(ip)
            qqq(1)=q(1)*volume+2.d0*du(ip)*afb(ip,ifloor,k2d)
          else if(ielem.eq.2) then
            sig(1,1)=total(ibm)*volume
            sig(1,2)=2.d0*sqrt(3.d0)*du(ip)
            qqq(1)=q(1)*volume
            sig(2,1)=sig(1,2)
            sig(2,2)=-total(ibm)*volume-6.d0*du(ip)
            qqq(2)=-q(2)*volume+2.d0*sqrt(3.d0)*du(ip)*afb(ip,ifloor,k2d)
          else if(ielem.eq.3) then
            sig(1,1)=total(ibm)*volume+2.d0*du(ip)
            sig(1,2)=0.d0
            sig(1,3)=2.d0*sqrt(5.d0)*du(ip)
            qqq(1)=q(1)*volume+2.d0*du(ip)*afb(ip,ifloor,k2d)
            sig(2,1)=sig(1,2)
            sig(2,2)=-total(ibm)*volume
            sig(2,3)=-2.d0*sqrt(15.d0)*du(ip)
            qqq(2)=-q(2)*volume
            sig(3,1)=sig(1,3)
            sig(3,2)=sig(2,3)
            sig(3,3)=total(ibm)*volume+10.d0*du(ip)
            qqq(3)=q(3)*volume+2.d0*sqrt(5.d0)*du(ip)*afb(ip,ifloor,k2d)
          endif
          do ie1=1,ielem
            ssign=1.0
            if(mod(ie1,2).eq.0) ssign=-1.0
            i=(ip-1)*ielem+ie1
            do ie2=1,ielem
              j=(ip-1)*ielem+ie2
              sigt_m(i,j)=sig(ie1,ie2)
            enddo
            do jp=1,npq
              ssss=ssign*w(jp)*volume/2.0
              j=(ip-1)*ielem+ie1
              do il=0,nsct-1
                sigt_m(i,j)=sigt_m(i,j)-ssss*real(2*il+1)*sgas(ibm,il+1)*pl(il+1,jp)
              enddo
              sigt_m(i,j)=sigt_m(i,j)+ssss*db2(isnap,k2d)*pl(1,jp)
            enddo ! jp
            sigt_m(i,iepq+1)=qqq(ie1)
          enddo
        enddo ! ip
        !----
        !  flux calculation on axial floor with scattering reduction.
        !----
        call ALSBD(iepq,1,sigt_m,ier,iepq)
        if(ier.ne.0) call XABORT('SPOT1P-swap: singular matrix.')
        !
        do ip=1,npq
          funk(:ielem,ifloor,ip,k2d)=0.0
          if(w(ip).eq.0.0) cycle
          do ie1=1,ielem
            i=(ip-1)*ielem+ie1
            funk(ie1,ifloor,ip,k2d)=sigt_m(i,iepq+1)
          enddo
          if(ielem.eq.1) then
            if(lfixup.and.(funk(1,ifloor,ip,k2d).le.rlog)) funk(1,ifloor,ip,k2d)=0.0
            afb(ip,ifloor+1,k2d)=2.d0*funk(1,ifloor,ip,k2d)-afb(ip,ifloor,k2d)
          else if(ielem.eq.2) then
            afb(ip,ifloor+1,k2d)=afb(ip,ifloor,k2d)+2.d0*sqrt(3.d0)*funk(2,ifloor,ip,k2d)
          else if(ielem.eq.3) then
            afb(ip,ifloor+1,k2d)=2.d0*funk(1,ifloor,ip,k2d)+2.d0*sqrt(5.d0)*funk(3,ifloor,ip,k2d)-afb(ip,ifloor,k2d)
          endif
          if(lfixup.and.(afb(ip,ifloor+1,k2d).le.rlog)) afb(ip,ifloor+1,k2d)=0.d0
        enddo ! ip
      enddo ! ifloor
    enddo ! k2d
    !$omp end parallel do
    deallocate(sigt_m,q)
  end subroutine swap
end subroutine SPOT1P
