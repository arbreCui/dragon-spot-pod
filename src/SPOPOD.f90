!-----------------------------------------------------------------------
!
! Purpose:
!   Build a volume-orthonormal POD basis from normalized 2D scalar-flux
!   snapshots.  The retained modes are the radial trial functions used
!   directly by the axial SPOD equations.
!
! For w_i=V_i/sum(V), each snapshot is first normalized by
!
!        sum_i w_i p_i^k = 1.
!
! The thin SVD is applied to X_i^k=sqrt(w_i) p_i^k.  If X=U S Z^T,
! the physical basis is B_i^a=U_i^a/sqrt(w_i), and therefore
!
!        sum_i w_i B_i^a B_i^b = delta_ab.
!
! RANK_REQ is the requested number of axial modes.  RANK_REQ=0 keeps
! the full numerical snapshot rank.
!
!-----------------------------------------------------------------------
subroutine SPOPOD(nreg2d,nsnap,phi,vol,rank_req,nmode,basis,coeff, &
                  sigma,rec_err,ortho_err,impx,igr)
  implicit none
  integer, parameter :: dp=kind(1.0d0), iunout=6

  integer, intent(in) :: nreg2d,nsnap,rank_req,impx,igr
  real, intent(in) :: phi(nreg2d,nsnap),vol(nreg2d)
  integer, intent(out) :: nmode
  real, intent(out) :: basis(nreg2d,nsnap),coeff(nsnap,nsnap)
  double precision, intent(out) :: sigma(nsnap),rec_err,ortho_err

  integer :: j,k,a,numerical_rank
  double precision :: vtot,vsum,s1,tol,norm_full,norm_diff,inner
  double precision, allocatable :: x(:,:),z(:,:),shape(:,:),recon(:,:)
  double precision, allocatable :: weight(:)
  external :: ALSVDF

  if (nreg2d <= 0 .or. nsnap <= 0) &
    call XABORT('SPOPOD: INVALID SNAPSHOT DIMENSIONS.')
  if (rank_req < 0) call XABORT('SPOPOD: NEGATIVE RANK REQUEST.')
  if (nreg2d < nsnap) &
    call XABORT('SPOPOD: NREG2D MUST BE GREATER THAN OR EQUAL TO NSNAP.')
  if (any(vol <= 0.0)) call XABORT('SPOPOD: NONPOSITIVE RADIAL VOLUME.')

  allocate(weight(nreg2d),shape(nreg2d,nsnap),x(nreg2d,nsnap))
  allocate(z(nsnap,nsnap),recon(nreg2d,nsnap))
  vtot=sum(real(vol,dp))
  weight=real(vol,dp)/vtot

  do k=1,nsnap
    vsum=sum(weight*real(phi(:,k),dp))
    if (vsum <= 0.0d0) call XABORT('SPOPOD: NONPOSITIVE SNAPSHOT FLUX.')
    shape(:,k)=real(phi(:,k),dp)/vsum
    x(:,k)=sqrt(weight)*shape(:,k)
  enddo

  call ALSVDF(x,nreg2d,nsnap,nreg2d,nsnap,sigma,z)
  s1=sigma(1)
  tol=real(max(nreg2d,nsnap),dp)*epsilon(1.0d0)*s1
  numerical_rank=count(sigma > tol)
  if (numerical_rank <= 0) call XABORT('SPOPOD: ZERO SNAPSHOT RANK.')
  if (rank_req == 0) then
    nmode=numerical_rank
  else
    nmode=min(rank_req,numerical_rank)
  endif

  basis=0.0
  coeff=0.0
  do a=1,nmode
    basis(:,a)=real(x(:,a)/sqrt(weight))
    do k=1,nsnap
      coeff(a,k)=real(sigma(a)*z(k,a))
    enddo
  enddo

  recon=0.0d0
  do k=1,nsnap
    do a=1,nmode
      recon(:,k)=recon(:,k)+real(basis(:,a),dp)*real(coeff(a,k),dp)
    enddo
  enddo
  norm_full=sqrt(sum(spread(weight,2,nsnap)*shape*shape))
  norm_diff=sqrt(sum(spread(weight,2,nsnap)*(recon-shape)*(recon-shape)))
  rec_err=norm_diff/norm_full

  ortho_err=0.0d0
  do a=1,nmode
    do j=1,nmode
      inner=sum(weight*real(basis(:,a),dp)*real(basis(:,j),dp))
      if (a == j) inner=inner-1.0d0
      ortho_err=max(ortho_err,abs(inner))
    enddo
  enddo

  if (impx >= 2) write(iunout,100) igr,nmode,numerical_rank, &
    rec_err,ortho_err
  if (impx >= 2) write(iunout,110) sigma

  deallocate(weight,recon,z,x,shape)
  return
100 format(' SPOPOD: group',I5,' modes=',I3,'/',I3, &
           ' reconstruction error=',1P,E11.4,' orthogonality error=',E11.4)
110 format(' SPOPOD: singular values',1P,100E12.4)
end subroutine SPOPOD
