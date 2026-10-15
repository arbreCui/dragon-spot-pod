!-----------------------------------------------------------------------
!
! Purpose:
!   NEW SOURCE: complete native64 dynamic B1 dependency chain.
!   Full original HOM64 formulas, loops, guards and order retained.
!   FLUX, homogenized coefficients, PHI, B2 and live leakage stay DP.
!   Static material/geometry inputs keep the original REAL ABI.
!   No compiler, numeric, transport or physical qualification here.
!
!-----------------------------------------------------------------------
subroutine SPOT_B1HOM_NATIVE64(ipmacr,leaksw,nunkno,option,calculation_type,ngro, &
                   ipas,nbm,nfissi,vol,mat,keyflx,flux,refkef,impx, &
                   dhom,gamma,alam1,inorm,b2,leak1d)
  use GANLIB
  implicit none

  type(c_ptr), intent(in) :: ipmacr
  logical, intent(in) :: leaksw
  integer, intent(in) :: nunkno,ngro,ipas,nbm,nfissi,impx,inorm
  integer, intent(in) :: mat(ipas),keyflx(ipas)
  character(len=4), intent(in) :: option,calculation_type
  real, intent(in) :: vol(ipas)
  double precision, intent(in) :: leak1d(ngro)
  double precision, intent(inout) :: flux(nunkno,ngro,2)
  double precision, intent(in) :: refkef
  double precision, intent(inout) :: dhom(ngro),gamma(ngro)
  double precision, intent(inout) :: alam1
  double precision, intent(inout) :: b2(4)

  integer :: i,l,ian,ngroin
  integer :: idel(2)
  integer, allocatable :: ijj0(:),ijj1(:),njj0(:),njj1(:)
  double precision, allocatable :: st(:),sa(:),sfnu(:),xhi(:)
  double precision, allocatable :: scat0(:),scat1(:)
  double precision, allocatable :: phi(:)
  double precision :: b2old,b2hom,caet,a2,normalizer
  logical :: lfissi

  external :: B1HXS1,SPOT_B1HXS2_NATIVE64,SPOT_B1DIF_NATIVE64

  if (leaksw) call XABORT('SPOT_B1HOM_NATIVE64: FUNDAMENTAL MODE EXPECTED.')
  if (inorm /= 1) call XABORT('SPOT_B1HOM_NATIVE64: DIFFON NORMALIZATION EXPECTED.')

  ian=0
  if ((option == 'B1').or.(option == 'P1')) then
    ian=1
  else if ((option == 'B0TR').or.(option == 'P0TR')) then
    ian=-1
  endif

  allocate(ijj0(ngro),ijj1(ngro),njj0(ngro),njj1(ngro))
  call B1HXS1(ipmacr,ngro,nbm,ian,nfissi,ijj0,ijj1,njj0,njj1,idel)

  allocate(st(ngro),sa(ngro),sfnu(ngro),xhi(ngro),phi(ngro))
  allocate(scat0(idel(1)),scat1(idel(2)))
  call SPOT_B1HXS2_NATIVE64(nunkno,ipmacr,ipas,ngro,nbm,ian,nfissi,vol,mat,keyflx, &
              flux(:,:,1),lfissi,ijj0,ijj1,njj0,njj1,idel,phi,sa,st,sfnu, &
              xhi,scat0,scat1,ngroin,inorm)

  b2old=b2(4)
  b2hom=b2old
  call SPOT_B1DIF_NATIVE64(option,calculation_type,ngro,st,sfnu,xhi,leak1d,ijj0, &
             ijj1,njj0,njj1,scat0,scat1,refkef,lfissi,impx,dhom, &
             gamma,b2hom,alam1,caet,a2,phi)
  b2(4)=b2hom

  if (calculation_type /= 'DIFF') then
    do i=1,ngro
      flux(:,i,2)=flux(:,i,2)+(b2(4)-b2old)* &
                    dhom(i)*flux(:,i,1)
    enddo

    do i=1,ngro
      normalizer=0.0d0
      do l=1,ipas
        normalizer=normalizer+real(vol(l),dp)*flux(keyflx(l),i,1)
      enddo
      if (normalizer == 0.0d0) &
        call XABORT('SPOT_B1HOM_NATIVE64: ZERO GROUP NORMALIZATION.')
      caet=phi(i)/normalizer
      flux(:,i,:)=flux(:,i,:)*caet
    enddo
  endif

  deallocate(scat1,scat0,phi,xhi,sfnu,sa,st)
  deallocate(njj1,njj0,ijj1,ijj0)
end subroutine SPOT_B1HOM_NATIVE64
